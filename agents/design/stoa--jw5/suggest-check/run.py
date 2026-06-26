# author: Denson Smith
# ticket: stoa--jw5 (u--9s2 Phase-1)
# seat-built-by: CAPTAIN_ADA_the_stoa (EXECUTOR) — exercises the SUGGEST front-door's testable core
# design-ground-truth: agents/design/stoa--jw5/design-formal.md §24-§31 (the SUGGEST front-door) —
#                       §24 SUGGEST / §25 detection_hints / §26 fail-closed confirm gate /
#                       §29 the three worked examples VIA SUGGEST + the §29.2 fail-closed no-confirm branch.
#
# Exercises the SUGGEST -> CONFIRM -> DECLARE front-door against the §29.1 three worked examples, then
# feeds each CONFIRMED DECLARE set into the UNCHANGED Part-2 generate() (§19) and the UNCHANGED Part-1
# resolve() (§2) and ASSERTS:
#   (1) confirm(suggest(examine(project))) == the §23 DECLARE set (byte-identical);
#   (2) the unchanged generate(DECLARE) -> resolve() hits the §8 set 8/6/7;
#   (3) SAFETY: the §29.2 fail-closed NO-CONFIRM branch -> ⊥ (INERT) -> NOTHING flows downstream;
#   (4) SAFETY: OVER-PROPOSAL (a hint hallucinates an extra service) -> human REMOVES -> not in DECLARE;
#   (5) SAFETY: UNDER-PROPOSAL (a called service the agent missed) -> human ADDS -> in DECLARE.
#
# THE §2 CONSTRAINT (load-bearing): generate.py (Part-2) AND resolve.py (Part-1) are UNCHANGED. Both are
# IMPORTED from ../discovery-check and ../resolution-check UNMODIFIED — never reimplemented, never edited.
# SUGGEST is strictly UPSTREAM of DECLARE (§24.0): feeding the CONFIRMED DECLARE into the unchanged
# generate()->resolve() and getting 8/6/7 (== the §23 DECLARE sets) IS the proof that SUGGEST is purely
# an upstream front-door.
#
# Self-report is NOT verification — VERA re-runs + adds the fail-closed safety probe. Provisions nothing.
# Run: python run.py  (exit 0 = all held).

from __future__ import annotations

import os
import sys

# --- import the UNCHANGED Part-1 resolver from ../resolution-check (no copy, no edit) ---
_HERE = os.path.dirname(os.path.abspath(__file__))
_RESOLUTION_CHECK = os.path.normpath(os.path.join(_HERE, "..", "resolution-check"))
_DISCOVERY_CHECK = os.path.normpath(os.path.join(_HERE, "..", "discovery-check"))
for _p in (_RESOLUTION_CHECK, _DISCOVERY_CHECK, _HERE):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from resolve import (  # noqa: E402  — the UNCHANGED §2 resolver (REUSED, not reimplemented)
    BASELINE,
    LIBRARY,
    resolve,
)
from generate import generate  # noqa: E402  — the UNCHANGED §19 generation (REUSED, not reimplemented)
from catalog import CATALOG as DISCOVERY_CATALOG, CATEGORIES  # noqa: E402  — Part-2 catalog (for generate)

# --- the SUGGEST front-door (this dir) ---
from catalog_hints import CATALOG_HINTS  # noqa: E402  — §22 seed + §25 detection_hints
from suggest import suggest  # noqa: E402  — §24 examine->match->propose
from confirm import confirm, is_declare, INERT  # noqa: E402  — §26 fail-closed gate


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


# ---------------------------------------------------------------------------
# §29.1 SUGGEST fixtures: the EXAMINE output (what the agent observed the project doing) per builder,
# bucketed by the four §24 surfaces. These mirror the §29.1 EXAMINE/MATCH lines verbatim.
# ---------------------------------------------------------------------------
SUGGEST_FIXTURES = [
    # (label, project_signals, expected_DECLARE (§23 set), expected_resolved_len (§8 set))
    (
        "prospector  (§29.1/§8.1)",
        {  # geo project: renders a client-side map, runs spatial queries (§29.1)
            "sdk_imports":  ["@googlemaps/js-api-loader"],     # surface (i)  Maps-JS SDK import -> google-maps
            "url_patterns": ["maps.googleapis.com"],           # surface (ii) maps URL pattern   -> google-maps
            "config_keys":  [],
            "data_signals": ["spatial-data"],                  # surface (iii) spatial-data flow -> spatial-db
        },
        ["google-maps", "spatial-db"],                         # == §23 prospector DECLARE
        8,
    ),
    (
        "scienceclaw (§29.1/§8.2)",
        {  # doc-consuming project (§29.1)
            "sdk_imports":  ["google.cloud.documentai"],       # surface (i)  parse-SDK import -> document-parsing
            "url_patterns": ["documentai.googleapis.com"],     # surface (ii) parse URL        -> document-parsing
            "config_keys":  [],
            "data_signals": [],
        },
        ["document-parsing"],                                  # == §23 scienceclaw DECLARE
        6,
    ),
    (
        "labstat_bls (§29.1/§8.3)",
        {  # doc/data project calling a BLS REST endpoint — the load-bearing DWP-3 case (§29.1)
            "sdk_imports":  ["google.cloud.documentai"],       # surface (i)  doc-parse SDK -> document-parsing
            "url_patterns": ["api.bls.gov"],                   # surface (ii) BLS-OEWS base-URL -> bls-oews (the DWP-3 infer)
            "config_keys":  ["BLS_OEWS_API_KEY"],              # surface (i)  BLS config key   -> bls-oews
            "data_signals": [],
        },
        ["bls-oews", "document-parsing"],                      # == §23 labstat_bls DECLARE (sorted)
        7,
    ),
]


def _resolve_from_declare(declare_services):
    """The UNCHANGED downstream: DECLARE -> generate() (§19) -> {category,delta} -> resolve() (§2).

    Both generate() and resolve() are the imported Part-2/Part-1 callables, UNMODIFIED. This is the
    exact §18->§19->§2 path §24.0 says runs UNCHANGED on the confirmed DECLARE."""
    manifest, _called = generate(declare_services, DISCOVERY_CATALOG, CATEGORIES, BASELINE)
    resolved = resolve(manifest, BASELINE, LIBRARY)
    return manifest, resolved


def main():
    print("=" * 92)
    print("stoa--jw5 suggest-check — exercising the SUGGEST->CONFIRM->DECLARE front-door (§24-§31)")
    print("design: agents/design/stoa--jw5/design-formal.md §24-§31  |  generate()+resolve() REUSED unmodified")
    print(f"generate() imported from: {_DISCOVERY_CHECK}{os.sep}generate.py (UNCHANGED — Part-2 §19)")
    print(f"resolve()  imported from: {_RESOLUTION_CHECK}{os.sep}resolve.py (UNCHANGED — Part-1 §2)")
    print("=" * 92)

    # =======================================================================
    # §29.1 — the three worked examples VIA SUGGEST (regression target 8/6/7)
    # examine -> suggest() -> propose+evidence -> confirm(accept) -> DECLARE == §23 -> generate->resolve == §8
    # =======================================================================
    print("\n--- §29.1 SUGGEST FRONT-DOOR: examine -> suggest -> confirm -> DECLARE == §23 -> resolve == 8/6/7 ---")
    for label, project_signals, expected_declare, exp_len in SUGGEST_FIXTURES:
        expected_declare_sorted = sorted(expected_declare)

        # S-2/S-3: examine -> match catalog detection_hints -> propose + evidence (INERT recommendation)
        proposed, evidence, unknown = suggest(project_signals, CATALOG_HINTS)
        check(f"{label}: suggest() proposed == §23 service set {expected_declare_sorted}",
              proposed == expected_declare_sorted, f"proposed={proposed}")
        # every candidate carries evidence (the §24 S-3 PRESENT-evidence input — WHY proposed)
        check(f"{label}: every proposed service carries detection-hint evidence",
              all(sid in evidence and evidence[sid] for sid in proposed),
              f"evidence keys={sorted(evidence)}")
        # the seed signals are all cataloged (no spurious unknown for the worked examples)
        check(f"{label}: no unknown (uncataloged) signal in the worked-example examine",
              unknown == [], f"unknown={unknown}")

        # §26 C-2: human CONFIRMS the proposal unedited -> the confirmed set IS the §18 DECLARE
        declare = confirm(proposed, {"action": "confirm"})
        check(f"{label}: confirm(accept) -> DECLARE produced (not INERT)", is_declare(declare))
        check(f"{label}: DECLARE == §23 set {expected_declare_sorted} (byte-identical)",
              declare == expected_declare_sorted, f"DECLARE={declare}")

        # the UNCHANGED generate()->resolve() on the confirmed DECLARE hits the §8 set 8/6/7
        manifest, resolved = _resolve_from_declare(declare)
        check(f"{label}: generate(DECLARE)->resolve() == {exp_len} entries (§8 target HIT)",
              len(resolved) == exp_len, f"got {len(resolved)}; manifest={manifest}")

    # labstat_bls load-bearing: the agent INFERRED bls-oews from a URL/config signal (DWP-3 upgrade)
    print("\n--- §29.1 labstat_bls load-bearing: agent INFERS bls-oews from URL/config (the DWP-3 upgrade) ---")
    lab_signals = SUGGEST_FIXTURES[2][1]
    lab_proposed, lab_evidence, _ = suggest(lab_signals, CATALOG_HINTS)
    check("labstat_bls: bls-oews PROPOSED (inferred from BLS url_pattern + config_key, no SDK import)",
          "bls-oews" in lab_proposed, f"proposed={lab_proposed}")
    bls_ev = lab_evidence.get("bls-oews", [])
    check("labstat_bls: bls-oews evidence cites the url_pattern AND/OR config_key signal",
          any(surface in ("url_patterns", "config_keys") for (surface, _t, _h) in bls_ev),
          f"evidence={bls_ev}")
    lab_declare = confirm(lab_proposed, {"action": "confirm"})
    _lab_manifest, lab_resolved = _resolve_from_declare(lab_declare)
    check("labstat_bls: resolved contains (thirdparty_rest_key, BLS_OEWS_API_KEY)",
          ("thirdparty_rest_key", "BLS_OEWS_API_KEY") in lab_resolved)
    check("labstat_bls: NO (gcp_api, BLS_OEWS_API_KEY) — bls-oews is gcp_api:none (no gcloud-enable)",
          ("gcp_api", "BLS_OEWS_API_KEY") not in lab_resolved)

    # =======================================================================
    # SAFETY PROBE (a) — §29.2 the FAIL-CLOSED NO-CONFIRM branch (the load-bearing safety case)
    # =======================================================================
    print("\n--- SAFETY (a): §29.2 FAIL-CLOSED no-confirm branch -> ⊥ INERT -> NOTHING flows downstream ---")
    nc_signals = SUGGEST_FIXTURES[0][1]                       # the same prospector proposal
    nc_proposed, _, _ = suggest(nc_signals, CATALOG_HINTS)
    check("no-confirm: suggest() still PROPOSES [google-maps, spatial-db] (proposal is INERT)",
          nc_proposed == ["google-maps", "spatial-db"], f"proposed={nc_proposed}")

    for action_label, human_action in [
        ("REJECT",        {"action": "reject"}),
        ("no-response",   {"action": "no_response"}),
        ("edits-pending", {"action": "edits_pending"}),
        ("None",          None),
    ]:
        result = confirm(nc_proposed, human_action)
        # (1) confirm -> ⊥ INERT, NO DECLARE produced
        check(f"no-confirm/{action_label}: confirm() -> ⊥ INERT (NO DECLARE produced)",
              result is INERT and not is_declare(result), f"result={result!r}")
        # (2) assert NOTHING flows to generate — INERT must NOT be fed downstream (fail-closed gate)
        flowed_to_generate = False
        if is_declare(result):
            # this branch MUST NOT execute for an INERT result; if it did, the gate failed open.
            flowed_to_generate = True
            _resolve_from_declare(result)
        check(f"no-confirm/{action_label}: INERT NEVER reaches generate() (downstream stays dark)",
              flowed_to_generate is False)

    # =======================================================================
    # SAFETY PROBE (b) — OVER-PROPOSAL: a hint mis-proposes an extra service -> human REMOVES in confirm
    # =======================================================================
    print("\n--- SAFETY (b): OVER-PROPOSAL (hallucinated extra service) -> human REMOVES -> not in DECLARE ---")
    # scienceclaw's project ALSO carries a stray maps URL (e.g. a mock / a /billing dir aspiration) that
    # the agent mis-recognizes as google-maps — an over-proposal the code never actually calls (§28).
    over_signals = {
        "sdk_imports":  ["google.cloud.documentai"],          # real: document-parsing
        "url_patterns": ["documentai.googleapis.com",
                         "maps.googleapis.com"],              # HALLUCINATION signal -> mis-proposes google-maps
        "config_keys":  [],
        "data_signals": [],
    }
    over_proposed, over_evidence, _ = suggest(over_signals, CATALOG_HINTS)
    check("over-proposal: suggest() OVER-proposes google-maps (hallucinated from a stray maps URL)",
          "google-maps" in over_proposed and "document-parsing" in over_proposed,
          f"proposed={over_proposed}")
    # §26.2: the human REMOVES the hallucinated google-maps before confirming (EDIT-then-CONFIRM)
    edited_set = [s for s in over_proposed if s != "google-maps"]
    over_declare = confirm(over_proposed, {"action": "confirm", "set": edited_set})
    check("over-proposal: human EDIT removes google-maps -> DECLARE == [document-parsing] (no bloat)",
          over_declare == ["document-parsing"], f"DECLARE={over_declare}")
    # and the downstream resolves to the CORRECT §8.2 set (6) — no over-provision of MAPS_API_KEY/google-maps
    _om, over_resolved = _resolve_from_declare(over_declare)
    check("over-proposal: resolve(DECLARE) == 6 (§8.2) — NO google-maps/MAPS_API_KEY over-provisioned",
          len(over_resolved) == 6
          and ("gcp_api", "google-maps") not in over_resolved
          and ("gcp_secret", "MAPS_API_KEY") not in over_resolved,
          f"resolved({len(over_resolved)})={over_resolved}")

    # =======================================================================
    # SAFETY PROBE (c) — UNDER-PROPOSAL: a called service the agent MISSED -> human ADDS in confirm
    # =======================================================================
    print("\n--- SAFETY (c): UNDER-PROPOSAL (agent misses a called service) -> human ADDS -> in DECLARE ---")
    # labstat_bls, but the agent FAILS to trace the BLS endpoint (fully-dynamic dispatch it could not
    # follow — §28 under-proposal): it sees ONLY document-parsing and MISSES bls-oews.
    under_signals = {
        "sdk_imports":  ["google.cloud.documentai"],          # only the doc-parse SDK is visible
        "url_patterns": [],                                   # the BLS URL was built too dynamically to trace
        "config_keys":  [],
        "data_signals": [],
    }
    under_proposed, _, _ = suggest(under_signals, CATALOG_HINTS)
    check("under-proposal: suggest() MISSES bls-oews (only [document-parsing] proposed)",
          under_proposed == ["document-parsing"], f"proposed={under_proposed}")
    # §26.2: the human (who knows the project calls BLS) ADDS bls-oews before confirming
    added_set = sorted(set(under_proposed) | {"bls-oews"})
    under_declare = confirm(under_proposed, {"action": "confirm", "set": added_set})
    check("under-proposal: human EDIT adds bls-oews -> DECLARE == [bls-oews, document-parsing]",
          under_declare == ["bls-oews", "document-parsing"], f"DECLARE={under_declare}")
    # and the downstream now resolves to the CORRECT §8.3 set (7) — no under-provision
    _um, under_resolved = _resolve_from_declare(under_declare)
    check("under-proposal: resolve(DECLARE) == 7 (§8.3) — BLS_OEWS_API_KEY present (no under-provision)",
          len(under_resolved) == 7
          and ("thirdparty_rest_key", "BLS_OEWS_API_KEY") in under_resolved,
          f"resolved({len(under_resolved)})={under_resolved}")

    # =======================================================================
    # §2 CONSTRAINT proof: confirm generate.py + resolve.py were reused UNMODIFIED
    # =======================================================================
    print("\n--- §2 CONSTRAINT: generate() + resolve() reused UNMODIFIED (SUGGEST is purely upstream) ---")
    check("resolve is the imported Part-1 callable (module from ../resolution-check)",
          getattr(resolve, "__module__", "") == "resolve"
          and os.path.normpath(os.path.dirname(sys.modules["resolve"].__file__)) == _RESOLUTION_CHECK,
          f"resolve file={sys.modules['resolve'].__file__}")
    check("generate is the imported Part-2 callable (module from ../discovery-check)",
          getattr(generate, "__module__", "") == "generate"
          and os.path.normpath(os.path.dirname(sys.modules["generate"].__file__)) == _DISCOVERY_CHECK,
          f"generate file={sys.modules['generate'].__file__}")

    # ---- summary ----
    print("\n" + "=" * 92)
    if failures:
        print(f"RESULT: FAIL — {len(failures)} check(s) failed:")
        for f in failures:
            print(f"  - {f}")
        print("=" * 92)
        return 1
    print("RESULT: PASS — SUGGEST->CONFIRM->DECLARE front-door produced the §23 DECLARE sets byte-identical,")
    print("        which the UNCHANGED generate()->resolve() resolved to 8/6/7 (§8.1/8.2/8.3);")
    print("        FAIL-CLOSED no-confirm branch -> ⊥ INERT -> nothing flowed downstream (§29.2);")
    print("        over-proposal removed by confirm (no bloat); under-proposal added by confirm (no under-provision);")
    print("        generate.py + resolve.py REUSED UNMODIFIED (SUGGEST is purely upstream of DECLARE).")
    print("=" * 92)
    return 0


if __name__ == "__main__":
    sys.exit(main())
