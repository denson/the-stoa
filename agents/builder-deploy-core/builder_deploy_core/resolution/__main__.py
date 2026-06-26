# author: Denson Smith
# ticket: stoa--pj3 (u--9s2 Phase-2 increment 2.1)
# seat-built-by: CAPTAIN_ADA_the_stoa (EXECUTOR)
# design-ground-truth: agents/design/stoa--pj3/design-rev2.md §2.5 (runnability) ;
#                       prototype RESULTS: agents/design/stoa--jw5/resolution-check/run.py
#
# `python -m builder_deploy_core.resolution` reproduces the Phase-1 resolution-check RESULTS pass-lines
# against the DATA-externalized core. The authoritative pass/fail is the tests/ suite (§2.6); this is
# the runnable reproduction surface. Provisions nothing; reads only the package's own data/ tree.

from __future__ import annotations

import sys

from builder_deploy_core import dataload
from builder_deploy_core.resolution.resolve import (
    BaselineOmitError,
    check_runtime_completeness,
    derive_sa_scope,
    resolve,
)

# The §8 fixtures (manifests + expected sets), transcribed from the Phase-1 prototype fixtures.py.
PROSPECTOR_MANIFEST = {"builder": "prospector", "category": "geospatial", "delta": {}}
PROSPECTOR_EXPECTED = [
    ("db_extension", "pgvector"),
    ("db_extension", "postgis"),
    ("gcp_api", "gemini-embedding"),
    ("gcp_api", "gemini-search"),
    ("gcp_api", "google-maps"),
    ("gcp_secret", "MAPS_API_KEY"),
    ("gcp_secret", "POSTGRES_PASSWORD"),
    ("railway_var", "DATABASE_URL"),
]
SCIENCECLAW_MANIFEST = {"builder": "scienceclaw", "category": "document-consuming", "delta": {}}
SCIENCECLAW_EXPECTED = [
    ("db_extension", "pgvector"),
    ("gcp_api", "document-parsing"),
    ("gcp_api", "gemini-embedding"),
    ("gcp_api", "gemini-search"),
    ("gcp_secret", "POSTGRES_PASSWORD"),
    ("railway_var", "DATABASE_URL"),
]
LABSTAT_BLS_MANIFEST = {
    "builder": "labstat_bls",
    "category": "document/data",
    "delta": {"add": [{"kind": "thirdparty_rest_key", "name": "BLS_OEWS_API_KEY"}]},
}
LABSTAT_BLS_EXPECTED = [
    ("db_extension", "pgvector"),
    ("gcp_api", "document-parsing"),
    ("gcp_api", "gemini-embedding"),
    ("gcp_api", "gemini-search"),
    ("gcp_secret", "POSTGRES_PASSWORD"),
    ("railway_var", "DATABASE_URL"),
    ("thirdparty_rest_key", "BLS_OEWS_API_KEY"),
]
BADBUILDER_PGVECTOR_OMIT_MANIFEST = {
    "builder": "badbuilder_pgvector_omit",
    "category": "document-consuming",
    "delta": {"omit": [{"kind": "db_extension", "name": "pgvector"}]},
}
POSITIVE_FIXTURES = [
    ("prospector  (§8.1)", PROSPECTOR_MANIFEST, PROSPECTOR_EXPECTED),
    ("scienceclaw (§8.2)", SCIENCECLAW_MANIFEST, SCIENCECLAW_EXPECTED),
    ("labstat_bls (§8.3)", LABSTAT_BLS_MANIFEST, LABSTAT_BLS_EXPECTED),
]

failures = []


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
    baseline = dataload.load_baseline()
    library = dataload.load_library()

    print("=" * 78)
    print("builder_deploy_core.resolution — exercising resolve() vs §8 fixtures (DATA-externalized)")
    print("design: agents/design/stoa--pj3/design-rev2.md  |  provisions NOTHING")
    print("=" * 78)

    print("\n--- POSITIVE fixtures: sorted(resolve(manifest)) == EXPECTED (byte-for-byte) ---")
    resolved_by_label = {}
    for label, manifest, expected in POSITIVE_FIXTURES:
        got = resolve(manifest, baseline, library)
        resolved_by_label[label] = got
        exact = (got == expected)
        check(f"{label}: resolved set EXACT match ({len(got)} entries)", exact,
              f"got {len(got)}, expected {len(expected)}")

    print("\n--- NEGATIVE fixture §8.4: resolve MUST raise BaselineOmitError (fail-closed) ---")
    raised, msg, returned = False, "", None
    try:
        returned = resolve(BADBUILDER_PGVECTOR_OMIT_MANIFEST, baseline, library)
    except BaselineOmitError as e:
        raised, msg = True, str(e)
    check("§8.4 (i): resolve raises BaselineOmitError (named)", raised)
    check("§8.4 (ii): no resolved set returned (fail-closed)", returned is None)
    check("§8.4 (iii): error names (db_extension, pgvector)",
          ("db_extension" in msg) and ("pgvector" in msg))

    print("\n--- §3.4 runtime-completeness invariant ---")
    for label, manifest, _expected in POSITIVE_FIXTURES:
        ok, missing = check_runtime_completeness(resolved_by_label[label])
        check(f"{label}: runtime-completeness holds", ok, "" if ok else f"missing: {missing}")
    prosp = resolved_by_label["prospector  (§8.1)"]
    check("§8.1 probe: prospector contains (gcp_api, google-maps)", ("gcp_api", "google-maps") in prosp)
    check("§8.1 probe: prospector contains (gcp_secret, MAPS_API_KEY)", ("gcp_secret", "MAPS_API_KEY") in prosp)

    print("\n--- §8.3 labstat_bls kind-dispatch probes ---")
    labstat = resolved_by_label["labstat_bls (§8.3)"]
    check("§8.3 (i): contains (thirdparty_rest_key, BLS_OEWS_API_KEY)",
          ("thirdparty_rest_key", "BLS_OEWS_API_KEY") in labstat)
    check("§8.3 (ii): no (gcp_api, BLS_OEWS_API_KEY)", ("gcp_api", "BLS_OEWS_API_KEY") not in labstat)
    s1_apis = [name for (kind, name) in labstat if kind == "gcp_api"]
    check("§8.3 (iii): S1 gcp_api input excludes BLS_OEWS_API_KEY", "BLS_OEWS_API_KEY" not in s1_apis)

    print("\n--- §5.A SA-scope derivation ---")
    for label, manifest, _expected in POSITIVE_FIXTURES:
        resolved = resolved_by_label[label]
        scope = derive_sa_scope(resolved)
        resolved_set = set(resolved)
        no_foreign = all(ent in resolved_set for ent in scope)
        expected_scope = sorted(
            (k, n) for (k, n) in resolved
            if k in {"gcp_api", "gcp_secret", "thirdparty_rest_key"})
        check(f"{label}: SA-scope ⊆ resolved set (no foreign entry)", no_foreign)
        check(f"{label}: SA-scope == scope-bearing subset", scope == expected_scope)

    print("\n" + "=" * 78)
    if failures:
        print(f"RESULT: FAIL — {len(failures)} check(s) failed:")
        for f in failures:
            print(f"  - {f}")
        print("=" * 78)
        return 1
    print("RESULT: PASS — all fixtures reproduced from the §2.5 algorithm exactly (DATA-externalized);")
    print("        §8.4 raised BaselineOmitError; runtime-completeness + SA-scope held.")
    print("=" * 78)
    return 0


if __name__ == "__main__":
    sys.exit(main())
