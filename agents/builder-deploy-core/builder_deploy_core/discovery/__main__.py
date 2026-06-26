# author: Denson Smith
# ticket: stoa--pj3 (u--9s2 Phase-2 increment 2.1)
# seat-built-by: CAPTAIN_ADA_the_stoa (EXECUTOR)
# design-ground-truth: agents/design/stoa--pj3/design-rev2.md §2.5 (runnability) ;
#                       prototype RESULTS: agents/design/stoa--jw5/discovery-check/run.py
#
# `python -m builder_deploy_core.discovery` reproduces the Phase-1 discovery-check RESULTS pass-lines
# against the DATA-externalized core, with the resolver REUSED via real intra-package import (§2-constraint).
# The authoritative pass/fail is the tests/ suite (§2.6). Provisions nothing; reads only data/.

from __future__ import annotations

import sys

from builder_deploy_core import dataload
from builder_deploy_core.discovery.generate import UncatalogedServiceError, generate
from builder_deploy_core.discovery.validate import validate
from builder_deploy_core.resolution.resolve import resolve

# §8 hand-authored manifests (for equivalence), from the Phase-1 prototype fixtures.py.
PROSPECTOR_MANIFEST = {"builder": "prospector", "category": "geospatial", "delta": {}}
PROSPECTOR_EXPECTED = [
    ("db_extension", "pgvector"), ("db_extension", "postgis"),
    ("gcp_api", "gemini-embedding"), ("gcp_api", "gemini-search"), ("gcp_api", "google-maps"),
    ("gcp_secret", "MAPS_API_KEY"), ("gcp_secret", "POSTGRES_PASSWORD"), ("railway_var", "DATABASE_URL"),
]
SCIENCECLAW_MANIFEST = {"builder": "scienceclaw", "category": "document-consuming", "delta": {}}
SCIENCECLAW_EXPECTED = [
    ("db_extension", "pgvector"), ("gcp_api", "document-parsing"), ("gcp_api", "gemini-embedding"),
    ("gcp_api", "gemini-search"), ("gcp_secret", "POSTGRES_PASSWORD"), ("railway_var", "DATABASE_URL"),
]
LABSTAT_BLS_MANIFEST = {
    "builder": "labstat_bls", "category": "document/data",
    "delta": {"add": [{"kind": "thirdparty_rest_key", "name": "BLS_OEWS_API_KEY"}]},
}
LABSTAT_BLS_EXPECTED = [
    ("db_extension", "pgvector"), ("gcp_api", "document-parsing"), ("gcp_api", "gemini-embedding"),
    ("gcp_api", "gemini-search"), ("gcp_secret", "POSTGRES_PASSWORD"), ("railway_var", "DATABASE_URL"),
    ("thirdparty_rest_key", "BLS_OEWS_API_KEY"),
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
    catalog, categories = dataload.load_catalog()

    print("=" * 86)
    print("builder_deploy_core.discovery — manifest GENERATION (§19 G1-G4) vs §23.1 examples")
    print("design: agents/design/stoa--pj3/design-rev2.md  |  resolver REUSED via intra-package import")
    print("=" * 86)

    fixtures = [
        ("prospector  (§23.1/§8.1)", ["google-maps", "spatial-db"], PROSPECTOR_EXPECTED, 8,
         PROSPECTOR_MANIFEST, "geospatial"),
        ("scienceclaw (§23.1/§8.2)", ["document-parsing"], SCIENCECLAW_EXPECTED, 6,
         SCIENCECLAW_MANIFEST, "document-consuming"),
        ("labstat_bls (§23.1/§8.3)", ["document-parsing", "bls-oews"], LABSTAT_BLS_EXPECTED, 7,
         LABSTAT_BLS_MANIFEST, "document-consuming"),
    ]
    generated = {}

    print("\n--- §23.1 GENERATION: services -> generate() -> {category,delta} -> resolve() == 8/6/7 ---")
    for label, services, expected, exp_len, hand, exp_cat in fixtures:
        manifest, called = generate(services, catalog, categories, baseline)
        generated[label] = (manifest, called, services)
        check(f"{label}: G2 category == {exp_cat!r}", manifest["category"] == exp_cat,
              f"got {manifest['category']!r}")
        resolved = resolve(manifest, baseline, library)
        check(f"{label}: resolve(GENERATED) == §8 set EXACT ({len(resolved)}, expect {exp_len})",
              resolved == expected and len(resolved) == exp_len, f"got {len(resolved)}")
        # equivalence: generated and hand-authored resolve identically (alias-aware)
        check(f"{label}: GENERATED ≡ §8 hand-authored (resolve identical)",
              resolve(manifest, baseline, library) == resolve(hand, baseline, library))

    print("\n--- §20 VALIDATION V1-V5 (fail-closed, before S0) ---")
    for label, (manifest, called, services) in generated.items():
        rows = validate(
            services_called=services, generated_manifest=manifest, catalog=catalog,
            called_entries=called, baseline=baseline, library=library,
            scan_detected=services, declared_services=services)
        print(f"  {label}:")
        for cid, ok, detail in rows:
            check(f"    {cid}", ok, detail)

    print("\n--- NEGATIVE PROBE 1: scan detects an UNDECLARED service -> V5 FAIL ---")
    np1_services = ["google-maps", "spatial-db"]
    np1_manifest, np1_called = generate(np1_services, catalog, categories, baseline)
    np1_rows = validate(
        services_called=np1_services, generated_manifest=np1_manifest, catalog=catalog,
        called_entries=np1_called, baseline=baseline, library=library,
        scan_detected=["google-maps", "spatial-db", "bls-oews"], declared_services=np1_services)
    v5 = next(r for r in np1_rows if r[0].startswith("V5"))
    check("NEG-1: V5 FAILS on undeclared-but-scanned 'bls-oews'", v5[1] is False, v5[2])

    print("\n--- NEGATIVE PROBE 2: a declared service NOT in the catalog -> V1 FAIL + generate raises ---")
    np2_services = ["document-parsing", "totally-uncataloged-svc"]
    raised = False
    try:
        generate(np2_services, catalog, categories, baseline)
    except UncatalogedServiceError:
        raised = True
    check("NEG-2: generate() RAISES UncatalogedServiceError (G1 fail-closed)", raised)
    np2_partial, np2_called = generate(["document-parsing"], catalog, categories, baseline)
    np2_rows = validate(
        services_called=np2_services, generated_manifest=np2_partial, catalog=catalog,
        called_entries=np2_called, baseline=baseline, library=library)
    v1 = next(r for r in np2_rows if r[0].startswith("V1"))
    check("NEG-2: V1 FAILS naming the uncataloged service", v1[1] is False, v1[2])

    print("\n--- §2 CONSTRAINT: resolve() reused via intra-package import ---")
    check("resolve is the resolution-package callable",
          resolve.__module__ == "builder_deploy_core.resolution.resolve")

    print("\n" + "=" * 86)
    if failures:
        print(f"RESULT: FAIL — {len(failures)} check(s) failed:")
        for f in failures:
            print(f"  - {f}")
        print("=" * 86)
        return 1
    print("RESULT: PASS — generation produced manifests the resolver resolves to 8/6/7, each ≡ §8;")
    print("        V1-V5 held; negatives fail-closed (V5 drift, V1 uncataloged); resolver REUSED.")
    print("=" * 86)
    return 0


if __name__ == "__main__":
    sys.exit(main())
