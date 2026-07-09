# author: Denson Smith
# ticket: stoa--q7f (u--9s2 Phase-1 increment 2.4)
# seat-built-by: CAPTAIN_ADA_the_stoa (EXECUTOR)
# design-ground-truth: design-rev4.md §2.1 (LANE_REGISTRY / MULTI_LANE_NODES), §2.3 (per-op scopes as lane
#                       principals), §2.4 (INV-LANE startup checks); rev2 §1.2.1 (INV-DEST), §1.3/§1.3.1
#                       (PROVIDER_REGISTRY shape + INV-RESP); design-rev6.md §5.1a (INV-RESP recursive NODE
#                       grammar: OBJECT/SCALAR/PASS_WHOLE; PASS_WHOLE_ALLOWLIST loader placement guard).
#
# The CLOSED, server-side registries + the STARTUP loader self-checks. `load_registry` runs INV-DEST,
# INV-RESP and INV-LANE and either returns a validated `Core` config or RAISES LoaderError (refuse to
# serve, fail-loud). These are code, not caller data.

from __future__ import annotations

import re
import string
from dataclasses import dataclass

from secure_core.errors import LoaderError
from secure_core.redact import SCALAR, PASS_WHOLE, PASS_WHOLE_ALLOWLIST
from secure_core.slots import FIXED, ENUM

# The tailnet cap domain (illustrative — the EXACT strings are pinned at build against the deployed tailnet
# policy `grants` block: V-ENC-LANE, design §2.1/§6 wp#4). The SHAPE is <domain>/cap/<lane>-core-client.
CAP_DOMAIN = "example.ts.net"

# The secret-bearing kinds that ride the pass-through as SLOT NAMES only (never values).
SECRET_SLOT_NAMES = ("GCP_SA_KEY_B64", "POSTGRES_PASSWORD", "TS_AUTHKEY")

_FORMATTER = string.Formatter()
_OPERATORS_PRINCIPAL = "operators"


def default_lane_registry() -> dict[str, str]:
    """§2.1 LANE_REGISTRY — cap-name -> lane principal. Server-side code, NOT caller data. Each lane's
    client tag is granted its OWN per-lane capability NAME; a control-plane-resolved cap yields its lane
    principal by EXPLICIT MEMBERSHIP only (identity.resolve_principal)."""
    return {
        f"{CAP_DOMAIN}/cap/science-core-client": "lane:science",
        f"{CAP_DOMAIN}/cap/newswire-core-client": "lane:newswire",
    }


def default_provider_registry() -> dict:
    """§2.3 PROVIDER_REGISTRY — Vertex as the FIRST provider (generate_grounded + embed), both auth adc_sa.
    `scopes` are LANE PRINCIPALS (deny-by-default): generate_grounded is science+operators ONLY; embed is
    the shared embeddings surface (science + newswire + operators). url_slots are FIXED/ENUM ONLY (INV-DEST);
    param_schema is a closed key allow-list disjoint from url_slots; response_schema is the per-op allow-list
    (INV-RESP)."""
    return {
        "vertex": {
            "auth": "adc_sa",  # server-side ADC (SA key), never an API key
            "operations": {
                "generate_grounded": {
                    "method": "POST",
                    "url": (
                        "https://{location}-aiplatform.googleapis.com/v1/projects/{project}"
                        "/locations/{location}/publishers/google/models/{model}:generateContent"
                    ),
                    "url_slots": {
                        "location": ENUM(["us-central1", "us-east4"]),
                        "project": FIXED("proj-sos_core"),  # server-pinned to the core's OWN GCP project
                        "model": ENUM(["gemini-2.5-flash", "gemini-2.5-pro"]),
                    },
                    "param_schema": {"contents": list, "tools": dict},  # closed; disjoint from url_slots
                    # INV-RESP recursive NODE grammar (design-rev6 §5.1a). OBJECT nodes are plain dicts;
                    # SCALAR/PASS_WHOLE are leaf markers. `candidates` is an OBJECT node applied element-wise
                    # to the candidates list. `content` is the ONE documented PASS_WHOLE exception (the model
                    # product — {parts, role}; NOT credential-bearing, the ADC bearer is a request-side
                    # Authorization header, never in a response body); its path `candidates.content` is the
                    # sole entry in PASS_WHOLE_ALLOWLIST. `groundingMetadata` is a RECURSED OBJECT node (NOT
                    # PASS_WHOLE), so an undeclared sub-key at ANY depth is dropped by construction. The exact
                    # grounding sub-keys are pinned at build against the real Vertex surface (V-RESP-GROUNDING);
                    # the INVARIANT regardless of exact keys is: groundingMetadata recurses, never whole-passes.
                    "response_schema": {
                        "candidates": {                       # OBJECT node — applied element-wise to the list
                            "content": PASS_WHOLE,            # DOCUMENTED exception: model product; passes whole
                            "finishReason": SCALAR,           # enum string leaf
                            "groundingMetadata": {            # nested OBJECT node — RECURSED; undeclared sub-key DROPPED
                                "webSearchQueries": SCALAR,   # list[str]
                                "retrievalQueries": SCALAR,   # list[str]
                                "groundingChunks": {          # OBJECT node (element-wise over the list)
                                    "web": {"uri": SCALAR, "title": SCALAR},
                                    "retrievedContext": {"uri": SCALAR, "title": SCALAR, "text": SCALAR},
                                },
                                "groundingSupports": {
                                    "segment": {"startIndex": SCALAR, "endIndex": SCALAR, "text": SCALAR},
                                    "groundingChunkIndices": SCALAR,
                                    "confidenceScores": SCALAR,
                                },
                                "searchEntryPoint": {"renderedContent": SCALAR, "sdkBlob": SCALAR},
                                "retrievalMetadata": {
                                    "webSearchQueries": SCALAR,
                                    "googleSearchDynamicRetrievalScore": SCALAR,
                                },
                            },
                        },
                        "usageMetadata": {                    # OBJECT node over the dict value
                            "promptTokenCount": SCALAR,
                            "candidatesTokenCount": SCALAR,
                            "totalTokenCount": SCALAR,
                        },
                    },
                    "stream": False,
                    "scopes": ["operators", "lane:science"],
                },
                "embed": {
                    "method": "POST",
                    "url": (
                        "https://{location}-aiplatform.googleapis.com/v1/projects/{project}"
                        "/locations/{location}/publishers/google/models/{model}:predict"
                    ),
                    "url_slots": {
                        "location": ENUM(["us-central1", "us-east4"]),
                        "project": FIXED("proj-sos_core"),
                        "model": ENUM(["text-embedding-005", "text-multilingual-embedding-002"]),
                    },
                    "param_schema": {"instances": list},
                    # INV-RESP recursive NODE grammar (design-rev6 §5.1a). `predictions` is an OBJECT node
                    # applied element-wise to the predictions list.
                    # DRIFT NOTE (ADA, ground-check per brief §GROUNDING + §5.3): design-rev6 §5.1a writes
                    # `{"predictions": {"embeddings": SCALAR}}` calling embeddings "a primitive vector". The
                    # CURRENT (web-verified) Vertex :predict response returns `embeddings` as an OBJECT
                    # {"values": [float,...], "statistics": {"token_count": int, "truncated": bool}} — NOT a
                    # bare vector. Declaring embeddings SCALAR would drop the WHOLE embeddings value (the
                    # recursive dict-scan drops it because it carries a mapping), breaking the embed feature.
                    # Built to ship/real reality (brief: shipped/real reality is canon; flag drift): embeddings
                    # is a RECURSED OBJECT node declaring `values` (SCALAR) + `statistics` (OBJECT). INV-RESP
                    # still holds by construction — an undeclared sub-key at any depth is dropped. The exact
                    # keys are the V-RESP-GROUNDING build-pin the design itself mandates. Flagged to PLINY.
                    "response_schema": {
                        "predictions": {                      # OBJECT node — element-wise over the list
                            "embeddings": {                   # OBJECT node (real Vertex shape), RECURSED
                                "values": SCALAR,             # list[float] — the embedding vector
                                "statistics": {               # OBJECT node
                                    "token_count": SCALAR,
                                    "truncated": SCALAR,
                                },
                            },
                        },
                    },
                    "stream": False,
                    "scopes": ["operators", "lane:science", "lane:newswire"],
                },
            },
        },
    }


@dataclass(frozen=True)
class Core:
    """A VALIDATED core configuration — the output of load_registry after INV-DEST/RESP/LANE passed. Holding
    a Core instance is proof the config is consistent (the loader refused to serve otherwise)."""

    provider_registry: dict
    lane_registry: dict
    accept_app_caps: frozenset  # the serve --accept-app-caps set (== LANE_REGISTRY cap names)
    multi_lane_nodes: dict      # frozenset[cap] -> principal; deny-by-default otherwise (empty this arc)
    operators: frozenset        # the <CORE>_OPERATORS allowlist (operator logins)

    def known_principals(self) -> set[str]:
        return {_OPERATORS_PRINCIPAL} | set(self.lane_registry.values())

    def get_op(self, provider: str, operation: str) -> dict | None:
        prov = self.provider_registry.get(provider)
        if not prov:
            return None
        return prov.get("operations", {}).get(operation)


def _template_names(url: str) -> set[str]:
    """The set of {name} placeholders in a URL template."""
    return {
        field_name
        for _, field_name, _, _ in _FORMATTER.parse(url)
        if field_name is not None and field_name != ""
    }


def _check_inv_dest(provider_registry: dict) -> None:
    """INV-DEST (rev2 §1.2.1) — every outbound destination component comes ONLY from server-pinned
    FIXED/ENUM slots; params/skill_id are disjoint from url_slots; a free-form slot is not representable.
    Refuse to serve on any violation."""
    for pname, prov in provider_registry.items():
        for oname, op in prov.get("operations", {}).items():
            where = f"{pname}.{oname}"
            url = op.get("url")
            url_slots = op.get("url_slots", {})
            param_schema = op.get("param_schema", {})

            # (1) every url_slot value is a FIXED or ENUM instance — a free-form (plain str / other) slot is
            #     the canonical "caller-steerable host" attack and is NOT admissible.
            for sname, sval in url_slots.items():
                if not isinstance(sval, (FIXED, ENUM)):
                    raise LoaderError(
                        f"INV-DEST violation at {where}: url_slot {sname!r} is a free-form/open slot "
                        f"({type(sval).__name__}) — only FIXED/ENUM are representable; refusing to serve"
                    )

            # (2) every {name} in the template resolves to a declared url_slot (no dangling destination
            #     component that could be filled from elsewhere).
            names = _template_names(url or "")
            missing = names - set(url_slots)
            if missing:
                raise LoaderError(
                    f"INV-DEST violation at {where}: url template references undeclared slot(s) "
                    f"{sorted(missing)} — every destination component must be a server-pinned url_slot"
                )

            # (3) DISJOINTNESS — no url template name is a param_schema key, and url_slots ∩ param_schema
            #     names is empty. A params-derived destination (a param NAME used as a host component) is the
            #     exact SSRF-reopen the loader must refuse.
            param_keys = set(param_schema)
            overlap = names & param_keys
            if overlap:
                raise LoaderError(
                    f"INV-DEST violation at {where}: url template name(s) {sorted(overlap)} resolve to "
                    f"param_schema key(s) — params are structurally forbidden from the destination; refusing"
                )
            slot_param_overlap = set(url_slots) & param_keys
            if slot_param_overlap:
                raise LoaderError(
                    f"INV-DEST violation at {where}: url_slots and param_schema share name(s) "
                    f"{sorted(slot_param_overlap)} — the two namespaces must be disjoint"
                )


def _validate_resp_node(node, path: str, where: str) -> None:
    """INV-RESP recursive NODE-grammar validation (design-rev6 §5.1a). The schema node tree is walked in
    lock-step with the dotted FIELD path (schema-root-relative; list indices are NOT part of the path — an
    OBJECT node applied element-wise still yields the field path). Every node must be exactly one of:
      - OBJECT (a `dict[str, node]`) — recurse each child;
      - SCALAR — a leaf marker, OK;
      - PASS_WHOLE — a leaf marker, OK ONLY IF its dotted `path` is in PASS_WHOLE_ALLOWLIST (r2, deny-by-
        default) — a non-allowlisted PASS_WHOLE placement REFUSES TO LOAD (fail-CLOSED at load).
    A bare `list` node (the legacy depth-2 form) or ANY unrecognized node type -> REFUSE TO LOAD (the
    regression fails closed AT LOAD, not at runtime)."""
    if node is PASS_WHOLE:
        if path not in PASS_WHOLE_ALLOWLIST:
            raise LoaderError(
                f"INV-RESP violation at {where}: field {path!r} is marked PASS_WHOLE but is NOT in "
                f"PASS_WHOLE_ALLOWLIST {sorted(PASS_WHOLE_ALLOWLIST)} — PASS_WHOLE placement is "
                f"deny-by-default; refusing to load (fail-closed at load)"
            )
        return
    if node is SCALAR:
        return
    if isinstance(node, dict):
        for key, child in node.items():
            child_path = f"{path}.{key}" if path else key
            _validate_resp_node(child, child_path, where)
        return
    # a bare list (legacy depth-2 "keep these, pass each whole" leaf) or any other unrecognized node type.
    raise LoaderError(
        f"INV-RESP violation at {where}: response_schema node at {path or '<root>'!r} is a "
        f"{type(node).__name__} — the recursive NODE grammar allows ONLY an OBJECT dict, SCALAR, or "
        f"PASS_WHOLE leaf; a bare list is the legacy depth-2 form and is refused; refusing to load"
    )


def _check_inv_resp(provider_registry: dict) -> None:
    """INV-RESP (rev2 §1.3.1 + design-rev6 §5.1a) — an op with NO response_schema (and no chunk_schema if
    streaming) is opaque pass-through and REFUSES TO LOAD. There is no 'just forward the body' escape hatch
    (that reopens M2). In addition, the declared schema's NODE tree is recursively validated: a bare-list
    (legacy depth-2) node or a non-allowlisted PASS_WHOLE placement refuses to load (fail-CLOSED at load)."""
    for pname, prov in provider_registry.items():
        for oname, op in prov.get("operations", {}).items():
            where = f"{pname}.{oname}"
            if op.get("stream"):
                chunk_schema = op.get("chunk_schema")
                if not chunk_schema:
                    raise LoaderError(
                        f"INV-RESP violation at {where}: streaming op declares no chunk_schema — opaque "
                        f"chunk pass-through forbidden; refusing to load"
                    )
                _validate_resp_node(chunk_schema, "", where)
            else:
                response_schema = op.get("response_schema")
                if not response_schema:
                    raise LoaderError(
                        f"INV-RESP violation at {where}: op declares no response_schema — opaque body "
                        f"pass-through forbidden; refusing to load"
                    )
                _validate_resp_node(response_schema, "", where)


def _check_inv_lane(
    provider_registry: dict,
    lane_registry: dict,
    accept_app_caps: frozenset,
    multi_lane_nodes: dict,
) -> None:
    """INV-LANE (design §2.4, STARTUP config) — refuse to serve on:
    (1) any scopes entry that is neither `operators` nor a KNOWN lane principal (typo'd/unknown lane);
    (2) serve --accept-app-caps set != LANE_REGISTRY cap-name set (an unmapped cap or a dead principal);
    (3) a lane principal that collides with the operator class OR looks like caller data (not `lane:*`).
    """
    known = {_OPERATORS_PRINCIPAL} | set(lane_registry.values())

    # (1) every scopes entry resolves to a known principal.
    for pname, prov in provider_registry.items():
        for oname, op in prov.get("operations", {}).items():
            for sc in op.get("scopes", []):
                if sc not in known:
                    raise LoaderError(
                        f"INV-LANE violation at {pname}.{oname}: scope {sc!r} is not a known principal "
                        f"(known={sorted(known)}) — refusing to serve"
                    )

    # (2) serve caps == LANE_REGISTRY cap-name set (no cap opted-in with no principal home; no registered
    #     lane principal left un-served by omission — the latter fails CLOSED: no header for that lane).
    cap_names = set(lane_registry)
    if set(accept_app_caps) != cap_names:
        raise LoaderError(
            f"INV-LANE violation: serve --accept-app-caps {sorted(accept_app_caps)} != LANE_REGISTRY "
            f"cap-name set {sorted(cap_names)} — every opted-in cap must have a lane principal home and "
            f"every registered lane principal must be served; refusing to serve"
        )

    # (3) lane principals are DISJOINT from the operator class and are derived-only-from-caps shaped
    #     (`lane:*`) — never bare caller-envelope data (a `skill_id` cannot masquerade as a lane).
    for cap, principal in lane_registry.items():
        if principal == _OPERATORS_PRINCIPAL:
            raise LoaderError(
                f"INV-LANE violation: lane principal for cap {cap!r} collides with the operator class"
            )
        if not principal.startswith("lane:"):
            raise LoaderError(
                f"INV-LANE violation: lane principal {principal!r} (cap {cap!r}) is not a `lane:*` "
                f"principal — lane identity must derive only from the control-plane cap, refusing to serve"
            )

    # (3b) a registered MULTI_LANE_NODES exception must map to a KNOWN principal and be keyed by a set of
    #      real cap names (its declared principal governs the node's scopes).
    for capset, principal in (multi_lane_nodes or {}).items():
        if principal not in known:
            raise LoaderError(
                f"INV-LANE violation: MULTI_LANE_NODES entry {sorted(capset)} maps to unknown principal "
                f"{principal!r} — refusing to serve"
            )
        unknown_caps = set(capset) - cap_names
        if unknown_caps:
            raise LoaderError(
                f"INV-LANE violation: MULTI_LANE_NODES entry references un-registered cap(s) "
                f"{sorted(unknown_caps)} — refusing to serve"
            )


def load_registry(
    provider_registry: dict | None = None,
    lane_registry: dict | None = None,
    accept_app_caps=None,
    multi_lane_nodes: dict | None = None,
    operators=None,
) -> Core:
    """The STARTUP loader (rev2 §1.2.1/§1.3.1 + rev4 §2.4). Runs INV-DEST, INV-RESP, INV-LANE and returns a
    validated Core, or RAISES LoaderError (refuse to serve, fail-loud). `accept_app_caps` defaults to the
    LANE_REGISTRY cap set (the consistent config); a probe passes a mismatched set to prove INV-LANE fires.
    """
    provider_registry = provider_registry if provider_registry is not None else default_provider_registry()
    lane_registry = lane_registry if lane_registry is not None else default_lane_registry()
    multi_lane_nodes = dict(multi_lane_nodes or {})
    if accept_app_caps is None:
        accept_app_caps = frozenset(lane_registry)
    else:
        accept_app_caps = frozenset(accept_app_caps)
    operators = frozenset(operators or ())

    _check_inv_dest(provider_registry)
    _check_inv_resp(provider_registry)
    _check_inv_lane(provider_registry, lane_registry, accept_app_caps, multi_lane_nodes)

    return Core(
        provider_registry=provider_registry,
        lane_registry=lane_registry,
        accept_app_caps=accept_app_caps,
        multi_lane_nodes={frozenset(k): v for k, v in multi_lane_nodes.items()},
        operators=operators,
    )


# A closed shape check for skill_id (rev2 §1.3 r6) — attribution label ONLY, never interpolated anywhere.
_SKILL_ID_RE = re.compile(r"^[a-z0-9_-]{1,64}$")


def valid_skill_id(skill_id) -> bool:
    return isinstance(skill_id, str) and bool(_SKILL_ID_RE.match(skill_id))
