# author: Denson Smith
# ticket: stoa--jw5 (u--9s2 Phase-1)
# seat-built-by: CAPTAIN_ADA_the_stoa (EXECUTOR) — exercises the KEY-DISCOVERY addition's testable core
# design-ground-truth: agents/design/stoa--jw5/design-formal.md §16-§23 (the KEY-DISCOVERY PROCESS addition)
#
# Exercises the manifest GENERATION (§19 G1-G4) against the §23.1 three worked examples, then feeds each
# GENERATED manifest into the UNCHANGED Part-1 resolve() (§2) and ASSERTS it resolves to 8/6/7 (§8.1/8.2/8.3).
# Also asserts each generated manifest is EQUIVALENT to the Part-1 hand-authored §8 manifest (fixtures.py),
# runs V1-V5 (§20), and adds negative probes (undeclared-drift -> V5; uncataloged service -> V1).
#
# THE §2 CONSTRAINT (load-bearing): the resolver is UNCHANGED. resolve() is IMPORTED from
# ../resolution-check/resolve.py UNMODIFIED — never reimplemented, never edited. Feeding a GENERATED
# manifest into the unchanged resolve() and getting 8/6/7 IS the proof that discovery is purely upstream.
#
# Self-report is NOT verification — VERA re-runs. Provisions nothing. Run: python run.py  (exit 0 = all held).

from __future__ import annotations

import os
import sys

# --- import the UNCHANGED Part-1 resolver from ../resolution-check (no copy, no edit) ---
_HERE = os.path.dirname(os.path.abspath(__file__))
_RESOLUTION_CHECK = os.path.normpath(os.path.join(_HERE, "..", "resolution-check"))
if _RESOLUTION_CHECK not in sys.path:
    sys.path.insert(0, _RESOLUTION_CHECK)

from resolve import (  # noqa: E402  — the UNCHANGED §2 resolver + its guards (REUSED, not reimplemented)
    BASELINE,
    LIBRARY,
    BaselineOmitError,
    check_runtime_completeness,
    resolve,
)
from fixtures import (  # noqa: E402  — the §8 hand-authored manifests + expected 8/6/7 sets
    LABSTAT_BLS_EXPECTED,
    LABSTAT_BLS_MANIFEST,
    PROSPECTOR_EXPECTED,
    PROSPECTOR_MANIFEST,
    SCIENCECLAW_EXPECTED,
    SCIENCECLAW_MANIFEST,
)

# --- the discovery harness (this dir) ---
from catalog import CATALOG, CATEGORIES  # noqa: E402
from generate import UncatalogedServiceError, generate  # noqa: E402
from validate import validate  # noqa: E402


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


def _manifests_equivalent(gen, hand):
    """Two manifests are EQUIVALENT iff they resolve identically AND carry the same category-layer
    membership. Because document-consuming and its alias document/data have BYTE-IDENTICAL templates
    (§3.2 / WP-4), a generated `document-consuming` manifest and a hand-authored `document/data`
    manifest are equivalent: resolve() yields the same set, and the category entry-sets are equal.
    We assert equivalence at the resolved-set + category-entry-set level (the §23.1 claim: the
    GENERATED manifest resolves to the §8 set byte-for-byte; for labstat_bls §23.1 explicitly
    generates `document-consuming` while §8.3 hand-authored `document/data` — same alias bundle)."""
    rg = resolve(gen, BASELINE, LIBRARY)
    rh = resolve(hand, BASELINE, LIBRARY)
    same_resolved = (rg == rh)
    # category-layer membership equality (alias-aware): the entry-set of each manifest's category
    gen_cat_entries = sorted((e["kind"], e["name"]) for e in LIBRARY.get(gen["category"], []))
    hand_cat_entries = sorted((e["kind"], e["name"]) for e in LIBRARY.get(hand["category"], []))
    same_cat_bundle = (gen_cat_entries == hand_cat_entries)
    # delta equality (as resolved deltas — order-insensitive)
    def _delta_idents(m, key):
        return sorted((e["kind"], e["name"]) for e in (m.get("delta") or {}).get(key, []))
    same_add = _delta_idents(gen, "add") == _delta_idents(hand, "add")
    same_omit = _delta_idents(gen, "omit") == _delta_idents(hand, "omit")
    return same_resolved and same_cat_bundle and same_add and same_omit, rg


# the §23.1 three worked examples: declared services + expected resolved set + the §8 hand-authored manifest
GENERATION_FIXTURES = [
    # (label, services_called, expected_set, expected_len, hand_authored_manifest, expected_category)
    ("prospector  (§23.1/§8.1)", ["google-maps", "spatial-db"], PROSPECTOR_EXPECTED, 8,
     PROSPECTOR_MANIFEST, "geospatial"),
    ("scienceclaw (§23.1/§8.2)", ["document-parsing"], SCIENCECLAW_EXPECTED, 6,
     SCIENCECLAW_MANIFEST, "document-consuming"),
    ("labstat_bls (§23.1/§8.3)", ["document-parsing", "bls-oews"], LABSTAT_BLS_EXPECTED, 7,
     LABSTAT_BLS_MANIFEST, "document-consuming"),  # §23.1 generates document-consuming (alias of §8.3's document/data)
]


def main():
    print("=" * 86)
    print("stoa--jw5 discovery-check — exercising manifest GENERATION (§19 G1-G4) vs §23.1 examples")
    print("design: agents/design/stoa--jw5/design-formal.md §16-§23  |  resolver REUSED unmodified")
    print(f"resolve() imported from: {_RESOLUTION_CHECK}{os.sep}resolve.py (UNCHANGED — the §2 constraint)")
    print("=" * 86)

    generated = {}

    # ---- GENERATION + resolve-to-8/6/7 + manifest-equivalence ----
    print("\n--- §23.1 GENERATION: services-called -> generate() -> {category,delta} -> resolve() == 8/6/7 ---")
    for label, services, expected, exp_len, hand_manifest, exp_cat in GENERATION_FIXTURES:
        manifest, called_entries = generate(services, CATALOG, CATEGORIES, BASELINE)
        generated[label] = (manifest, called_entries, services, hand_manifest, expected)

        # G2 chose the expected category
        check(f"{label}: G2 category == {exp_cat!r}", manifest["category"] == exp_cat,
              f"got category={manifest['category']!r}")

        # the GENERATED manifest, fed to the UNCHANGED resolve(), hits the §8 set byte-for-byte
        resolved = resolve(manifest, BASELINE, LIBRARY)
        exact = (resolved == expected)
        check(f"{label}: resolve(GENERATED) == §8 set EXACT ({len(resolved)} entries, expect {exp_len})",
              exact and len(resolved) == exp_len,
              f"got {len(resolved)}"
              + ("" if exact else f"\n        diff(got-exp)={sorted(set(resolved)-set(expected))}"
                                  f"\n        diff(exp-got)={sorted(set(expected)-set(resolved))}"))

        # the GENERATED manifest is EQUIVALENT to the §8 hand-authored manifest
        equiv, _ = _manifests_equivalent(manifest, hand_manifest)
        check(f"{label}: GENERATED manifest EQUIVALENT to §8 hand-authored manifest", equiv,
              f"\n        generated={manifest}\n        hand={hand_manifest}")

    # ---- labstat_bls load-bearing probes (§23.1 / §8.3): bls-oews -> +BLS_OEWS_API_KEY, NO gcloud-enable ----
    print("\n--- §23.1 labstat_bls load-bearing: bls-oews DECLARED -> +BLS_OEWS_API_KEY delta, NO gcloud-enable ---")
    lab_manifest, _, _, _, _ = generated["labstat_bls (§23.1/§8.3)"]
    lab_resolved = resolve(lab_manifest, BASELINE, LIBRARY)
    # delta.add carries exactly the thirdparty_rest_key (the generated delta, mechanically derived)
    lab_add = sorted((e["kind"], e["name"]) for e in (lab_manifest.get("delta") or {}).get("add", []))
    check("labstat_bls: generated delta.add == [(thirdparty_rest_key, BLS_OEWS_API_KEY)]",
          lab_add == [("thirdparty_rest_key", "BLS_OEWS_API_KEY")], f"delta.add={lab_add}")
    # (i) resolved contains the thirdparty key
    check("labstat_bls (i): resolved contains (thirdparty_rest_key, BLS_OEWS_API_KEY)",
          ("thirdparty_rest_key", "BLS_OEWS_API_KEY") in lab_resolved)
    # (ii) ZERO gcp_api named BLS_OEWS_API_KEY (bls-oews record is gcp_api: none -> no API minted)
    check("labstat_bls (ii): no (gcp_api, BLS_OEWS_API_KEY) — bls-oews is gcp_api:none",
          ("gcp_api", "BLS_OEWS_API_KEY") not in lab_resolved)
    # (iii) S1 gcp_api input list excludes it
    s1 = [n for (k, n) in lab_resolved if k == "gcp_api"]
    check("labstat_bls (iii): S1 gcp_api input excludes BLS_OEWS_API_KEY",
          "BLS_OEWS_API_KEY" not in s1, f"S1 apis={s1}")

    # ---- V1-V5 on each positive ----
    print("\n--- §20 VALIDATION V1-V5 on each generated manifest (fail-closed, before S0) ---")
    for label, (manifest, called_entries, services, _hand, _exp) in generated.items():
        rows = validate(
            services_called=services,
            generated_manifest=manifest,
            catalog=CATALOG,
            called_entries=called_entries,
            resolve=resolve,
            baseline=BASELINE,
            library=LIBRARY,
            baseline_omit_error=BaselineOmitError,
            check_runtime_completeness=check_runtime_completeness,
            scan_detected=services,        # honest: scan sees exactly the declared services (no drift) for positives
            declared_services=services,
        )
        print(f"  {label}:")
        for cid, ok, detail in rows:
            check(f"    {cid}", ok, detail)

    # ---- NEGATIVE PROBE 1: undeclared-but-imported service -> V5 fail-closed ----
    print("\n--- NEGATIVE PROBE 1: scan detects an UNDECLARED service -> V5 FAIL (fail-closed) ---")
    # prospector declares [google-maps, spatial-db] but the scanner ALSO detects an undeclared 'bls-oews' import.
    np1_services = ["google-maps", "spatial-db"]
    np1_manifest, np1_called = generate(np1_services, CATALOG, CATEGORIES, BASELINE)
    np1_rows = validate(
        services_called=np1_services, generated_manifest=np1_manifest, catalog=CATALOG,
        called_entries=np1_called, resolve=resolve, baseline=BASELINE, library=LIBRARY,
        baseline_omit_error=BaselineOmitError, check_runtime_completeness=check_runtime_completeness,
        scan_detected=["google-maps", "spatial-db", "bls-oews"],   # scan saw an UNDECLARED bls-oews
        declared_services=np1_services,
    )
    v5_row = next(r for r in np1_rows if r[0].startswith("V5"))
    check("NEG-1: V5 FAILS on undeclared-but-scanned 'bls-oews' (fail-closed drift)",
          v5_row[1] is False, v5_row[2])

    # ---- NEGATIVE PROBE 2: a declared service NOT in the catalog -> V1 fail-closed ----
    print("\n--- NEGATIVE PROBE 2: a declared service NOT in the catalog -> V1 FAIL + generate() raises ---")
    np2_services = ["document-parsing", "totally-uncataloged-svc"]
    # generate() itself must raise UncatalogedServiceError (G1 fail-closed, do not emit)
    raised = False
    try:
        generate(np2_services, CATALOG, CATEGORIES, BASELINE)
    except UncatalogedServiceError as e:
        raised = True
        np2_msg = str(e)
    check("NEG-2: generate() RAISES UncatalogedServiceError (G1 fail-closed, no emit)", raised,
          np2_msg if raised else "did NOT raise")
    # and V1 independently FAILS for the same input (validation-side fail-closed) — generate a partial
    # manifest from the cataloged subset purely to exercise V1's own check.
    np2_partial, np2_called = generate(["document-parsing"], CATALOG, CATEGORIES, BASELINE)
    np2_rows = validate(
        services_called=np2_services, generated_manifest=np2_partial, catalog=CATALOG,
        called_entries=np2_called, resolve=resolve, baseline=BASELINE, library=LIBRARY,
        baseline_omit_error=BaselineOmitError, check_runtime_completeness=check_runtime_completeness,
    )
    v1_row = next(r for r in np2_rows if r[0].startswith("V1"))
    check("NEG-2: V1 FAILS naming the uncataloged service (fail-closed)",
          v1_row[1] is False, v1_row[2])

    # ---- §2-constraint proof: confirm resolve.py was reused unmodified ----
    print("\n--- §2 CONSTRAINT: resolve() reused UNMODIFIED (discovery is purely upstream) ---")
    check("resolve is the imported Part-1 callable (module from ../resolution-check)",
          getattr(resolve, "__module__", "") == "resolve"
          and os.path.normpath(os.path.dirname(sys.modules["resolve"].__file__)) == _RESOLUTION_CHECK,
          f"resolve.__module__={getattr(resolve, '__module__', None)}; "
          f"file={sys.modules['resolve'].__file__}")

    # ---- summary ----
    print("\n" + "=" * 86)
    if failures:
        print(f"RESULT: FAIL — {len(failures)} check(s) failed:")
        for f in failures:
            print(f"  - {f}")
        print("=" * 86)
        return 1
    print("RESULT: PASS — generation (§19 G1-G4) produced manifests that the UNCHANGED resolve() resolves")
    print("        to 8/6/7 (§8.1/8.2/8.3), each EQUIVALENT to the §8 hand-authored manifest;")
    print("        V1-V5 held; negative probes fail-closed (V5 drift, V1 uncataloged); resolver REUSED.")
    print("=" * 86)
    return 0


if __name__ == "__main__":
    sys.exit(main())
