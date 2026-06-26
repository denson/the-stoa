# author: Denson Smith
# ticket: stoa--pj3 (u--9s2 Phase-2 increment 2.1)
# seat-built-by: CAPTAIN_ADA_the_stoa (EXECUTOR) — promoted VERBATIM from the VERIFIED Phase-1 prototype
# prototype-source: agents/design/stoa--jw5/resolution-check/resolve.py (19/19 VERIFIED)
# design-ground-truth: agents/design/stoa--pj3/design-rev2.md §2.1 / §2.1.1 ; §2.5/§3.1/§3.2/§3.4/§5.A
#
# Pure resolution logic for the u--9s2 composable key-provisioning model.
# Provisions NOTHING. Reads NO environment (no GCP, no network, no clock, no filesystem) — §2.3 purity.
# resolve(manifest, baseline, library) is implemented verbatim against §2.5 reference pseudocode.
#
# PROMOTION (the ONLY logic-byte edits vs the Phase-1 prototype, per design-rev2 §2.1):
#   (a) the `baseline=BASELINE, library=LIBRARY` literal defaults on resolve/resolve_with_lint are
#       DELETED — the caller now passes the dataload-loaded tables (the parameter seam, §2.1).
#   (b) the §3.3 kind-tables (KIND_ENUM / SCOPE_BEARING_KINDS / KEY_BEARING_PAIRING) are no longer
#       literal assignments; they are an _UNLOADED fail-closed sentinel populated once at import time
#       by resolution/__init__.py via dataload.load_kinds() (the import-time module-global seam, §2.1.1).
#   derive_sa_scope and check_runtime_completeness signatures + bodies are BYTE-UNCHANGED.

from __future__ import annotations

from builder_deploy_core.errors import BaselineOmitError, ResolutionError  # §2.1 errors home


# ---------------------------------------------------------------------------
# §2.1.1 fail-closed sentinel for the §3.3 kind-tables (populated at import by
# resolution/__init__.py). A read BEFORE dataload populates them RAISES rather
# than silently using an empty collection (which would be a silent fail-OPEN).
# ---------------------------------------------------------------------------
class _Unloaded:
    """A kind-table sentinel whose membership/iteration raises DataIntegrityError.

    This is the §2.1.1 load-order guard's teeth: even if some future caller imports resolve.py in a
    way that bypassed resolution/__init__.py population, the FIRST read of a kind-table raises rather
    than mis-resolves (fail-CLOSED, never an empty-table silent fail-OPEN)."""

    def _fail(self, *_a, **_k):
        from builder_deploy_core.errors import DataIntegrityError
        raise DataIntegrityError("kind-tables read before dataload populated them")

    __contains__ = _fail
    __iter__ = _fail
    __len__ = _fail
    def items(self):  # KEY_BEARING_PAIRING.items() in check_runtime_completeness
        self._fail()


_UNLOADED = _Unloaded()

# §3.3 kind enum + scope-bearing / gcloud-enable classification.
# Used by derive_sa_scope (§5.A) and check_runtime_completeness (§3.4).
# NOT literal assignments (§2.1.1): the _UNLOADED sentinel is replaced at import time by
#   resolve.KIND_ENUM, resolve.SCOPE_BEARING_KINDS, resolve.KEY_BEARING_PAIRING = dataload.load_kinds()
KIND_ENUM = _UNLOADED
SCOPE_BEARING_KINDS = _UNLOADED
KEY_BEARING_PAIRING = _UNLOADED


def warn(msg: str) -> None:
    """Lint surface (§2.4). Non-fatal; collected, not raised. Returned by resolve_with_lint."""
    # Kept as a side-effect-free hook here; run.py uses resolve_with_lint to capture lints.
    pass


def _baseline_set(baseline) -> set:
    """The NON-OMITTABLE BASELINE set (§2.6) — derived from the immutable BASELINE record."""
    return {(e["kind"], e["name"]) for e in baseline}


def resolve(manifest, baseline, library):
    """§2.5 reference pseudocode, implemented verbatim.

    Returns the sorted resolved set of (kind, name) tuples (§2.3 deterministic order).
    Raises ResolutionError for an unknown category (§2.4).
    Raises BaselineOmitError if delta.omit targets any non-omittable baseline entry
    (§2.4 / §2.6) — evaluated at step 0, BEFORE the omit subtraction (fail-closed).
    Pure: reads no environment.
    """
    cat = manifest["category"]
    if cat not in library:
        raise ResolutionError(f"unknown category: {cat}")  # §2.4 ERROR, fail-closed

    delta = manifest.get("delta") or {}
    adds = [(e["kind"], e["name"]) for e in (delta.get("add") or [])]
    omits = [(e["kind"], e["name"]) for e in (delta.get("omit") or [])]

    add_set, omit_set = set(adds), set(omits)

    # step 0: GUARD — omit may ONLY target category-template entries (§2.4 / §2.6).
    # Fires BEFORE omit-subtraction, on omit ∩ baseline. HARD ERROR, not a silent drop.
    baseline_set = _baseline_set(baseline)  # the NON-OMITTABLE set, §2.6
    illegal = omit_set & baseline_set
    if illegal:  # WP-6 fix (former fail-OPEN path)
        raise BaselineOmitError(
            f"omit targets non-omittable baseline entry/entries: {sorted(illegal)}")

    for ident in (add_set & omit_set):  # §2.4 WARNING (add-wins) — lint only, never silently dropped
        warn(f"entry {ident} in both add and omit; kept (add-wins)")

    s = set(baseline_set)                                          # entries as (kind, name) tuples
    s |= {(e["kind"], e["name"]) for e in library[cat]}           # step 1: ∪ category
    s -= omit_set                                                 # step 2: \ omit (baseline omits already rejected)
    s |= add_set                                                  # step 3: ∪ add (add-wins, applied last)
    return sorted(s)                                              # §2.3 deterministic order


def resolve_with_lint(manifest, baseline, library):
    """Same as resolve() but also returns the lint list (§2.4 WARNING/INFO conditions).

    Returns (resolved_sorted, lints) where lints is a list of (level, message).
    Raises the same fail-closed errors as resolve().
    """
    lints = []
    cat = manifest["category"]
    if cat not in library:
        raise ResolutionError(f"unknown category: {cat}")

    delta = manifest.get("delta") or {}
    adds = [(e["kind"], e["name"]) for e in (delta.get("add") or [])]
    omits = [(e["kind"], e["name"]) for e in (delta.get("omit") or [])]
    add_set, omit_set = set(adds), set(omits)

    baseline_set = _baseline_set(baseline)
    illegal = omit_set & baseline_set
    if illegal:
        raise BaselineOmitError(
            f"omit targets non-omittable baseline entry/entries: {sorted(illegal)}")

    union_pre = baseline_set | {(e["kind"], e["name"]) for e in library[cat]}

    # §2.4 row 4 — add∩omit -> WARNING, resolved KEPT (add-wins)
    for ident in sorted(add_set & omit_set):
        lints.append(("WARNING", f"entry {ident} in both add and omit; kept (add-wins)"))
    # §2.4 row 5 — omit names a (kind,name) not in BASELINE∪CATEGORY -> WARNING (no-op subtract)
    for ident in sorted(omit_set - union_pre):
        lints.append(("WARNING", f"omit {ident} had no effect (not in baseline∪category)"))
    # §2.4 row 6 — add duplicates an entry already in BASELINE∪CATEGORY -> INFO (redundant add)
    for ident in sorted(add_set & union_pre):
        lints.append(("INFO", f"redundant add {ident} (already in baseline∪category)"))

    s = set(baseline_set)
    s |= {(e["kind"], e["name"]) for e in library[cat]}
    s -= omit_set
    s |= add_set
    return sorted(s), lints


def derive_sa_scope(resolved_set):
    """§5.A — SA scope = mechanical union of every scope-bearing resolved entry.

    Never hand-written; a pure function of the resolved set. Returns the sorted list of
    scope-bearing (kind, name) entries:
      - gcp_api            -> API role
      - gcp_secret         -> per-secret accessor
      - thirdparty_rest_key-> per-secret accessor (no GCP API enable)
    railway_var and db_extension are NOT scope-bearing and are excluded.
    """
    return sorted(
        (kind, name) for (kind, name) in resolved_set if kind in SCOPE_BEARING_KINDS
    )


def check_runtime_completeness(resolved_set):
    """§3.4 runtime-completeness invariant.

    For every key-bearing gcp_api in the resolved set (key-bearing iff a template-declared
    (gcp_api -> gcp_secret) pairing exists — the §3.2 in-band signal), assert its paired
    gcp_secret is also present in the resolved set.

    Returns (ok: bool, missing: list[ (api_ident, required_secret_ident) ]).
    ok == True means every key-bearing API has its paired secret resolved.
    """
    present = set(resolved_set)
    missing = []
    for api_ident, secret_ident in KEY_BEARING_PAIRING.items():
        if api_ident in present and secret_ident not in present:
            missing.append((api_ident, secret_ident))
    return (len(missing) == 0), missing
