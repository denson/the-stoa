# author: Denson Smith
# ticket: stoa--q7f (u--9s2 Phase-1 increment 2.4)
# seat-built-by: CAPTAIN_ADA_the_stoa (EXECUTOR)
# design-ground-truth: design-rev6.md §5.1a (INV-RESP recursive NODE grammar + PASS_WHOLE_ALLOWLIST). rev2
#                       §1.3.1 established the INV-RESP allow-list; rev5 made it RECURSIVE to schema depth;
#                       rev6 completes the by-construction generality on the other two node types:
#                         (r1) the SCALAR node drops any object/dict at ANY depth via a RECURSIVE dict-scan;
#                         (r2) PASS_WHOLE placement is deny-by-default via PASS_WHOLE_ALLOWLIST.
#
# The response allow-list serializer. This is the M2 response-surface guard as a BUILD-TIME-VERIFIED
# property: whatever the upstream returns, the caller receives ONLY the fields the op declared, at EVERY
# depth. A credential echoed into ANY undeclared field/subfield/header — at any depth, incl. an object
# smuggled under a SCALAR slot or a mis-marked whole-pass field — never reaches the caller.
#
# The recursive NODE grammar (design-rev6 §5.1a). A `response_schema` is a NODE tree; every declared key maps
# to EXACTLY ONE node type — there is NO bare `list[str]` "keep these, pass each whole" leaf (that leaf WAS
# the depth-2 bug). A node is one of:
#   1. OBJECT node — a `dict[str, node]`. Applied to a dict: keep ONLY declared keys, recurse each; DROP every
#      undeclared key. Applied to a list: apply element-wise (each element a dict filtered by this node; a
#      non-dict element dropped). Applied to a scalar: structurally unexpected -> DROP.
#   2. SCALAR leaf — the value passes IFF it contains NO object (dict/mapping) at ANY depth: a JSON primitive
#      (str/num/bool/null), or a (recursively) array of primitives. A value carrying a mapping ANYWHERE under
#      it — including nested inside a list, doubly-nested — is structurally unexpected: the WHOLE value is
#      DROPPED. This is a RECURSIVE DICT-SCAN, NOT a shallow top-level check (r1). A credential cannot ride an
#      undeclared sub-key of an object smuggled under a SCALAR slot.
#   3. PASS_WHOLE leaf — the ONE explicit, documented whole-passthrough exception; the value passes whole
#      regardless of type. Deny-by-default placement (r2): a field may be PASS_WHOLE ONLY IF its schema-root-
#      relative dotted path is in PASS_WHOLE_ALLOWLIST, which the loader enforces at LOAD (registry.py
#      `_check_inv_resp`) — a schema marking any non-allowlisted field PASS_WHOLE refuses to load.

from __future__ import annotations


class _NodeMarker:
    """A response_schema leaf-node marker. Identity-compared (`node is SCALAR`), never instantiated by
    callers — the two module singletons SCALAR and PASS_WHOLE are the only instances.

    Copy-safe singletons: `copy.copy` / `copy.deepcopy` return the SAME instance (a registry dict is a natural
    thing to deep-copy — probes do it — and the identity checks in redact_response + the loader MUST survive
    that; a fresh marker instance would silently defeat `node is SCALAR`/`is PASS_WHOLE` and misfire the
    grammar). `__reduce__` keeps pickle round-trips singleton too."""

    __slots__ = ("name",)

    def __init__(self, name: str) -> None:
        self.name = name

    def __repr__(self) -> str:  # pragma: no cover - debug aid
        return f"<{self.name}>"

    def __copy__(self) -> "_NodeMarker":
        return self

    def __deepcopy__(self, memo) -> "_NodeMarker":
        return self

    def __reduce__(self):
        return (_marker_by_name, (self.name,))


def _marker_by_name(name: str) -> "_NodeMarker":
    """Pickle/copy reconstructor — returns the existing singleton, never a new instance."""
    return {"SCALAR": SCALAR, "PASS_WHOLE": PASS_WHOLE}[name]


# The two leaf-node markers. OBJECT nodes are plain `dict[str, node]` values (no marker needed).
SCALAR = _NodeMarker("SCALAR")
PASS_WHOLE = _NodeMarker("PASS_WHOLE")

# PASS_WHOLE_ALLOWLIST (design-rev6 §5.1a, r2) — server-side, code, NOT caller data. The ONLY schema-root-
# relative dotted-path fields that may be marked PASS_WHOLE. Deny-by-default: a new PASS_WHOLE placement
# requires an explicit, audited entry here (consistent with INV-LANE / INV-PRINCIPAL / seal-audit
# deny-by-default). This arc = the single model-product field. The OBJECT node `candidates` is applied
# element-wise to the list, so the field path is `candidates.content` — list indices are NOT part of the path.
PASS_WHOLE_ALLOWLIST = frozenset({"candidates.content"})

# Sentinel: a node applied to a structurally-unexpected value yields _DROP, meaning "omit this key entirely"
# (distinct from a legitimately-present None/empty value).
_DROP = object()


def _scalar_ok(value) -> bool:
    """SCALAR by-construction rule (r1) — True IFF `value` contains NO mapping (dict) at ANY depth. A RECURSIVE
    dict-scan: a JSON primitive passes; a list/tuple passes IFF every element (recursively) passes; ANY dict
    found anywhere -> False (the whole value is dropped by the caller). A shallow top-level `isinstance(value,
    dict)` check is NON-CONFORMANT: it would pass a list-containing-a-dict and leave the SCALAR-slot smuggle
    path open."""
    if isinstance(value, dict):
        return False
    if isinstance(value, (list, tuple)):
        return all(_scalar_ok(v) for v in value)
    return True  # str / int / float / bool / None


def _apply_node(node, value):
    """Redact `value` against a single `node`. Returns the redacted value, or `_DROP` to omit the key."""
    if node is PASS_WHOLE:
        return value  # the one documented whole-passthrough (placement guarded at LOAD by the loader)
    if node is SCALAR:
        return value if _scalar_ok(value) else _DROP  # recursive dict-scan: drop any mapping at any depth
    if isinstance(node, dict):
        return _apply_object(node, value)  # OBJECT node
    # An unrecognized node type should never reach here — the loader (_check_inv_resp) refuses to serve a
    # response_schema carrying a bare-list/unknown node. Fail CLOSED at runtime regardless: drop.
    return _DROP


def _apply_object(node: dict, value):
    """OBJECT node application. dict value -> filter to declared keys; list value -> element-wise over dict
    elements (non-dict elements dropped); scalar value -> structurally unexpected -> _DROP."""
    if isinstance(value, list):
        return [_filter_dict(node, elem) for elem in value if isinstance(elem, dict)]
    if isinstance(value, dict):
        return _filter_dict(node, value)
    return _DROP


def _filter_dict(node: dict, value: dict) -> dict:
    """Keep ONLY declared keys of `value`, each recursively filtered by its child node; DROP every undeclared
    key (the by-construction property — a credential in ANY undeclared key at ANY depth is dropped here)."""
    out: dict = {}
    for key, child in node.items():
        if key not in value:
            continue
        redacted = _apply_node(child, value[key])
        if redacted is not _DROP:
            out[key] = redacted
    return out


def redact_response(response_schema: dict, upstream_body: dict) -> dict:
    """Allow-list serialize `upstream_body` against the recursive NODE-grammar `response_schema`.

    `response_schema` is an OBJECT node (a `dict[str, node]`) at the root; `redact_response` recurses the node
    tree in lock-step with the value tree. At each level it keeps ONLY declared keys and recurses their values;
    at a SCALAR leaf it passes a pure-primitive value (dropping any value carrying a mapping at any depth); at
    a PASS_WHOLE leaf it passes the value whole. Every UNDECLARED key at EVERY depth is dropped by
    construction. A non-dict upstream body has no declared shape -> emit nothing (never pass opaque)."""
    if not isinstance(upstream_body, dict):
        return {}
    return _filter_dict(response_schema, upstream_body)


def error_envelope(status: int, provider_error_class: str) -> dict:
    """rev2 §1.3.1 — an upstream error is returned as `{status, provider_error_class}` ONLY. Never the raw
    upstream error body, never upstream headers (M2)."""
    return {"status": status, "provider_error_class": provider_error_class}
