# author: Denson Smith
# ticket: stoa--jw5 (u--9s2 Phase-1)
# seat-built-by: CAPTAIN_ADA_the_stoa (EXECUTOR) — exercises the KEY-DISCOVERY addition's testable core
# design-ground-truth: agents/design/stoa--jw5/design-formal.md §20 (VALIDATION V1-V5) / §20.2 (placement
#                       + anti-under-provisioning spine) / §18 (scan pillar -> V5)
#
# VALIDATE(services_called, generated_manifest) runs V1-V5 per §20, fail-closed, strictly BEFORE S0.
# V4 REUSES the §2 guards (resolve + BaselineOmitError + check_runtime_completeness) from the UNCHANGED
# Part-1 resolve.py — it does NOT re-implement them (§20.2: Part-1 invariants stay the single source of
# truth). resolve is passed in by the caller (run.py imports it from the unchanged module).
#
# Provisions NOTHING; reads no environment.

from __future__ import annotations


class ValidationError(Exception):
    """§20 V1-V5 ERROR — a generated manifest that fails a validation check. fail-closed (never enters S0)."""


def _ent(e):
    return (e["kind"], e["name"])


def _entset(entries):
    return {_ent(e) for e in entries}


def validate(
    services_called,
    generated_manifest,
    catalog,
    called_entries,
    resolve,                 # the UNCHANGED Part-1 resolve(manifest, baseline, library)
    baseline,
    library,
    baseline_omit_error,     # resolve.BaselineOmitError (the §2.6 guard exception class)
    check_runtime_completeness,
    scan_detected=None,      # §18/§20 V5: the set of service-ids a static scan detected (drift cross-check)
    declared_services=None,  # §18: the DECLARED services: set (V5 compares scan vs declare)
):
    """Run V1-V5 (§20). Returns a list of (check_id, PASS/FAIL, detail).

    Fail-closed posture: each failing check appends a FAIL row AND (for the fail-closed checks)
    the caller treats any FAIL as "manifest rejected, never enters S0". V4 reuses the §2 guards.
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
    except baseline_omit_error as e:
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
    except baseline_omit_error as e:
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
    except baseline_omit_error as e:
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
