# author: Denson Smith
# ticket: stoa--pj3 (u--9s2 Phase-2 increment 2.1)
# seat-built-by: CAPTAIN_ADA_the_stoa (EXECUTOR) — promoted VERBATIM from the VERIFIED Phase-1 prototype
# prototype-source: agents/design/stoa--jw5/discovery-check/validate.py (VERIFIED)
# design-ground-truth: agents/design/stoa--pj3/design-rev2.md §2.1 / §2.3 (the §2-constraint edge) ;
#                       §20 (V1-V5) / §20.2 / §18
#
# VALIDATE(services_called, generated_manifest) runs V1-V5 per §20, fail-closed, strictly BEFORE S0.
# V4 REUSES the §2 guards (resolve + BaselineOmitError + check_runtime_completeness) from the resolution
# package — it does NOT re-implement them (§20.2: Part-1 invariants stay the single source of truth).
#
# PROMOTION — the §2-constraint edge (design-rev2 §2.3, logic-edit (c)): the Phase-1 prototype received
# resolve / BaselineOmitError / check_runtime_completeness as INJECTED parameters (via run.py's sys.path
# hack). The promotion replaces that with a REAL intra-package IMPORT of the single resolver. There is NO
# copy of the resolution algorithm anywhere under discovery/; the dependency is one-directional
# discovery -> resolution. The V1-V5 algorithm bodies are otherwise verbatim.
#
# Provisions NOTHING; reads no environment.

from __future__ import annotations

# THE §2-CONSTRAINT EDGE (§2.3): import the SINGLE resolver + its guard, never reimplement.
from builder_deploy_core.errors import BaselineOmitError, ValidationError  # noqa: F401 (ValidationError = §20 error home)
from builder_deploy_core.resolution.resolve import check_runtime_completeness, resolve


def _ent(e):
    return (e["kind"], e["name"])


def _entset(entries):
    return {_ent(e) for e in entries}


def validate(
    services_called,
    generated_manifest,
    catalog,
    called_entries,
    baseline,
    library,
    scan_detected=None,      # §18/§20 V5: the set of service-ids a static scan detected (drift cross-check)
    declared_services=None,  # §18: the DECLARED services: set (V5 compares scan vs declare)
):
    """Run V1-V5 (§20). Returns a list of (check_id, PASS/FAIL, detail).

    Fail-closed posture: each failing check appends a FAIL row AND (for the fail-closed checks)
    the caller treats any FAIL as "manifest rejected, never enters S0". V4 reuses the §2 guards
    (resolve + check_runtime_completeness + BaselineOmitError) IMPORTED from the resolution package.
    """
    results = []
    called_set = set(called_entries)
    declared_services = set(declared_services if declared_services is not None else services_called)
    scan_detected = set(scan_detected if scan_detected is not None else [])

    # ---- V1: EVERY-SERVICE-CATALOGED (§20) ----
    uncataloged = [sid for sid in services_called if sid not in catalog]
    results.append((
        "V1 every-service-cataloged",
        not uncataloged,
        "all cataloged" if not uncataloged else f"uncataloged service(s): {sorted(uncataloged)}",
    ))

    # ---- V2: COMPLETE — resolve(gen) ⊇ called_entries (anti-under-provision; §3.4/M3 lineage) ----
    # (only meaningful if the manifest resolves; guarded so a V4 raise doesn't crash V2.)
    v2_ok = False
    v2_detail = ""
    try:
        resolved = set(resolve(generated_manifest, baseline, library))
        missing = called_set - resolved
        v2_ok = not missing
        v2_detail = "resolved ⊇ called" if v2_ok else f"called-but-unresolved: {sorted(missing)}"
    except BaselineOmitError as e:
        v2_detail = f"resolve raised BaselineOmitError: {e}"
    results.append(("V2 complete (resolve ⊇ called)", v2_ok, v2_detail))

    # ---- V3: MINIMAL — resolved \ BASELINE has NO entry for an UNCALLED non-baseline service ----
    # i.e. every non-baseline resolved entry traces to a CALLED service's catalog entries.
    v3_ok = False
    v3_detail = ""
    try:
        resolved = set(resolve(generated_manifest, baseline, library))
        baseline_set = _entset(baseline)
        non_baseline_resolved = resolved - baseline_set
        # the union of catalog entries across CALLED services = the legitimately-callable non-baseline set
        callable_entries = set()
        for sid in services_called:
            rec = catalog.get(sid)
            if rec:
                callable_entries |= _entset(rec["entries"])
        bloat = non_baseline_resolved - callable_entries
        v3_ok = not bloat
        v3_detail = "no uncalled entry provisioned" if v3_ok else f"uncalled (bloat) entries: {sorted(bloat)}"
    except BaselineOmitError as e:
        v3_detail = f"resolve raised BaselineOmitError: {e}"
    results.append(("V3 minimal (no uncalled entry)", v3_ok, v3_detail))

    # ---- V4: RESOLVE-WELL-FORMED — REUSE the §2 guards (no re-implementation) ----
    # (a) resolve raises NO BaselineOmitError (§2.6)
    # (b) §3.4 runtime-completeness holds (every key-bearing surface has its paired credential)
    v4_ok = False
    v4_detail = ""
    try:
        resolved_list = resolve(generated_manifest, baseline, library)
        rc_ok, rc_missing = check_runtime_completeness(resolved_list)
        v4_ok = rc_ok
        v4_detail = "resolve well-formed; §3.4 runtime-completeness holds" if rc_ok \
            else f"runtime-completeness FAIL: missing pairings {rc_missing}"
    except BaselineOmitError as e:
        v4_detail = f"resolve raised BaselineOmitError (§2.6 guard fired): {e}"
    results.append(("V4 resolve-well-formed (REUSES §2.6/§3.4 guards)", v4_ok, v4_detail))

    # ---- V5: NO-UNDECLARED-DRIFT (the scan pillar, §18) ----
    # any scan-detected service-call that is undeclared -> ERROR (reconcile declaration or waive).
    undeclared_drift = scan_detected - declared_services
    v5_ok = not undeclared_drift
    results.append((
        "V5 no-undeclared-drift (scan ⊆ declared)",
        v5_ok,
        "no shadow service" if v5_ok else f"shadow service(s) detected but not declared: {sorted(undeclared_drift)}",
    ))

    return results
