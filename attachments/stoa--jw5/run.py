# author: Denson Smith
# ticket: stoa--jw5 (u--9s2 Phase-1)
# seat-built-by: CAPTAIN_ADA_the_stoa (EXECUTOR)
# design-ground-truth: agents/design/stoa--jw5/design-formal.md §8 fixtures + §3.4 + §5.A
#
# Exercises resolve() against the four §8 fixtures so the design's central claim
# (the resolution rule) is FALSIFIABLE. Self-report is NOT verification — VERA re-runs.
# Provisions nothing. Pure logic. Run: python run.py  (exit 0 = all checks held).

from __future__ import annotations

import sys

from resolve import (
    BASELINE,
    LIBRARY,
    BaselineOmitError,
    check_runtime_completeness,
    derive_sa_scope,
    resolve,
)
from fixtures import (
    BADBUILDER_PGVECTOR_OMIT_MANIFEST,
    POSITIVE_FIXTURES,
    PROSPECTOR_EXPECTED,
)

failures = []  # collected so the run reports ALL results, not just the first failure


def check(label, condition, detail=""):
    status = "PASS" if condition else "FAIL"
    line = f"  [{status}] {label}"
    if detail:
        line += f" — {detail}"
    print(line)
    if not condition:
        failures.append(label)
    return condition


def main():
    print("=" * 78)
    print("stoa--jw5 resolution-check — exercising resolve() vs §8 fixtures")
    print("design: agents/design/stoa--jw5/design-formal.md  |  provisions NOTHING")
    print("=" * 78)

    # ---- §8.1/8.2/8.3 POSITIVE fixtures: exact resolved-set match ----------
    print("\n--- POSITIVE fixtures: sorted(resolve(manifest)) == EXPECTED (byte-for-byte) ---")
    resolved_by_label = {}
    for label, manifest, expected in POSITIVE_FIXTURES:
        got = resolve(manifest, BASELINE, LIBRARY)
        resolved_by_label[label] = got
        exact = (got == expected)
        check(
            f"{label}: resolved set EXACT match ({len(got)} entries)",
            exact,
            f"got {len(got)}, expected {len(expected)}"
            + ("" if exact else f"\n        diff(got - exp)={sorted(set(got) - set(expected))}"
                                f"\n        diff(exp - got)={sorted(set(expected) - set(got))}"),
        )

    # ---- §8.4 NEGATIVE fixture: MUST raise BaselineOmitError ---------------
    print("\n--- NEGATIVE fixture §8.4: resolve MUST raise BaselineOmitError (fail-closed) ---")
    raised = False
    msg = ""
    returned = None
    try:
        returned = resolve(BADBUILDER_PGVECTOR_OMIT_MANIFEST, BASELINE, LIBRARY)
    except BaselineOmitError as e:
        raised = True
        msg = str(e)
    # (i) raises BaselineOmitError (named — not generic, not a silent set)
    check("§8.4 (i): resolve raises BaselineOmitError (named)", raised,
          f"message={msg!r}" if raised else f"NO raise; returned={returned!r}")
    # (ii) raise occurs before any set returned (fail-closed — no partial set)
    check("§8.4 (ii): no resolved set returned (fail-closed)", returned is None)
    # (iii) message identifies (db_extension, pgvector) as the offending target
    names_target = ("db_extension" in msg) and ("pgvector" in msg)
    check("§8.4 (iii): error names (db_extension, pgvector)", names_target, f"message={msg!r}")

    # ---- §3.4 runtime-completeness on each positive -----------------------
    print("\n--- §3.4 runtime-completeness invariant (key-bearing gcp_api -> paired gcp_secret) ---")
    for label, manifest, _expected in POSITIVE_FIXTURES:
        resolved = resolved_by_label[label]
        ok, missing = check_runtime_completeness(resolved)
        check(f"{label}: runtime-completeness holds", ok,
              "" if ok else f"missing pairings: {missing}")
    # prospector specifically MUST contain BOTH google-maps AND MAPS_API_KEY (§8.1 probe)
    prosp = resolved_by_label["prospector  (§8.1)"]
    check("§8.1 probe: prospector contains (gcp_api, google-maps)",
          ("gcp_api", "google-maps") in prosp)
    check("§8.1 probe: prospector contains (gcp_secret, MAPS_API_KEY)",
          ("gcp_secret", "MAPS_API_KEY") in prosp)

    # ---- §8.3 labstat_bls kind-dispatch probes (delta != template bloat) ---
    print("\n--- §8.3 labstat_bls kind-dispatch probes (thirdparty_rest_key skips S1) ---")
    labstat = resolved_by_label["labstat_bls (§8.3)"]
    # (i) resolved set contains (thirdparty_rest_key, BLS_OEWS_API_KEY)
    check("§8.3 (i): contains (thirdparty_rest_key, BLS_OEWS_API_KEY)",
          ("thirdparty_rest_key", "BLS_OEWS_API_KEY") in labstat)
    # (ii) ZERO gcp_api entry named BLS_OEWS_API_KEY (delta added NO API)
    check("§8.3 (ii): no (gcp_api, BLS_OEWS_API_KEY) — delta added no API",
          ("gcp_api", "BLS_OEWS_API_KEY") not in labstat)
    # (iii) the S1 input list (kind == gcp_api) does NOT include BLS_OEWS_API_KEY
    s1_apis = [name for (kind, name) in labstat if kind == "gcp_api"]
    check("§8.3 (iii): S1 gcp_api input excludes BLS_OEWS_API_KEY",
          "BLS_OEWS_API_KEY" not in s1_apis, f"S1 apis={s1_apis}")

    # ---- §5.A derive_sa_scope: no entry outside this builder's resolved set ----
    print("\n--- §5.A SA-scope derivation (scope = scope-bearing subset of resolved set) ---")
    for label, manifest, _expected in POSITIVE_FIXTURES:
        resolved = resolved_by_label[label]
        scope = derive_sa_scope(resolved)
        resolved_set = set(resolved)
        # every derived scope entry MUST be a member of THIS builder's resolved set (no foreign entry)
        no_foreign = all(ent in resolved_set for ent in scope)
        # scope is exactly the scope-bearing kinds (gcp_api, gcp_secret, thirdparty_rest_key)
        expected_scope = sorted(
            (k, n) for (k, n) in resolved
            if k in {"gcp_api", "gcp_secret", "thirdparty_rest_key"}
        )
        check(f"{label}: SA-scope ⊆ resolved set (no foreign entry)", no_foreign,
              f"scope={scope}")
        check(f"{label}: SA-scope == scope-bearing subset", scope == expected_scope)

    # ---- summary ----------------------------------------------------------
    print("\n" + "=" * 78)
    if failures:
        print(f"RESULT: FAIL — {len(failures)} check(s) failed:")
        for f in failures:
            print(f"  - {f}")
        print("=" * 78)
        return 1
    print("RESULT: PASS — all fixtures reproduced from the §2.5 algorithm exactly;")
    print("        §8.4 raised BaselineOmitError; runtime-completeness + SA-scope held.")
    print("=" * 78)
    return 0


if __name__ == "__main__":
    sys.exit(main())
