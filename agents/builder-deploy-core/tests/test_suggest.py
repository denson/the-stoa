# author: Denson Smith
# ticket: stoa--fdf (u--9s2 Phase-2 increment 2.2)
# seat-built-by: CAPTAIN_ADA_the_stoa (EXECUTOR)
# design-ground-truth: agents/design/stoa--fdf/design-rev2.md §3 (the machine-checkable probe spec) —
#                      P1 (choreography 8/6/7) / P2a-f (fail-closed + over/under) / P3 (module-identity) /
#                      P4a/P4b (evidence + contract) / P5b (P3 provenance) / P6 (engine runs on fixtures) ;
#                      preserves the prototype's 35-check floor (agents/design/stoa--jw5/suggest-check/run.py).
#
# The §3 SUGGEST probe suite. VERA re-executes this independently (self-report is NOT verification).
# Probe-ids are stable so the verdict can cite them. The 35-check prototype floor is preserved as the
# curated-dict choreography checks (test_prototype_floor_*), re-run against the SAME logic now packaged;
# the fixture-driven probes (P1/P6) add the real-examiner path the prototype could not exercise.

from __future__ import annotations

from pathlib import Path

import pytest

from builder_deploy_core import dataload
from builder_deploy_core.suggest import (
    INERT,
    build_presentation,
    check_contract,
    confirm,
    confirm_presented,
    declare_from_confirm,
    examine,
    is_declare,
    suggest,
    tag_declare,
)
from builder_deploy_core.suggest.suggest import HINT_FIELDS

_FIXTURES = Path(__file__).resolve().parent / "fixtures" / "suggest-projects"


# ---------------------------------------------------------------------------
# Shared DATA + fixtures (session-scoped; the real shipped data/ tree).
# ---------------------------------------------------------------------------
@pytest.fixture(scope="session")
def detection_hints():
    return dataload.load_detection_hints()


@pytest.fixture(scope="session")
def tables():
    catalog, categories = dataload.load_catalog()
    return {
        "catalog": catalog,
        "categories": categories,
        "baseline": dataload.load_baseline(),
        "library": dataload.load_library(),
    }


# ===========================================================================
# PROTOTYPE 35-CHECK FLOOR (curated signal dicts) — preserves the stoa--jw5 suggest-check/run.py logic
# now that suggest()/confirm() are packaged. These are the §29.1 EXAMINE dicts verbatim from the
# prototype, so the SAME 35 assertions hold against the promoted code (a REGRESSION target, hit not
# re-derived). The fixture-driven P1/P6 below add the real-examiner path on top.
# ===========================================================================

# (label, project_signals (curated EXAMINE dict), expected DECLARE (§23 set), expected resolved len (§8))
_PROTO_FIXTURES = [
    (
        "prospector",
        {"sdk_imports": ["@googlemaps/js-api-loader"], "url_patterns": ["maps.googleapis.com"],
         "config_keys": [], "data_signals": ["spatial-data"]},
        ["google-maps", "spatial-db"], 8,
    ),
    (
        "scienceclaw",
        {"sdk_imports": ["google.cloud.documentai"], "url_patterns": ["documentai.googleapis.com"],
         "config_keys": [], "data_signals": []},
        ["document-parsing"], 6,
    ),
    (
        "labstat_bls",
        {"sdk_imports": ["google.cloud.documentai"], "url_patterns": ["api.bls.gov"],
         "config_keys": ["BLS_OEWS_API_KEY"], "data_signals": []},
        ["bls-oews", "document-parsing"], 7,
    ),
]


def _resolve_from_declare(declare_services, tables):
    from builder_deploy_core.discovery.generate import generate
    from builder_deploy_core.resolution.resolve import resolve
    manifest, _called = generate(declare_services, tables["catalog"], tables["categories"], tables["baseline"])
    resolved = resolve(manifest, tables["baseline"], tables["library"])
    return manifest, resolved


@pytest.mark.parametrize("label,signals,expected_declare,exp_len", _PROTO_FIXTURES)
def test_prototype_floor_choreography(label, signals, expected_declare, exp_len, detection_hints, tables):
    """35-floor: curated EXAMINE dict -> suggest -> propose(+evidence) -> confirm(accept) -> DECLARE==§23
    -> unchanged generate->resolve == §8 (8/6/7). Mirrors suggest-check/run.py §29.1 block verbatim."""
    expected = sorted(expected_declare)
    proposed, evidence, unknown = suggest(signals, detection_hints)
    assert proposed == expected, f"{label}: proposed={proposed}"
    assert all(sid in evidence and evidence[sid] for sid in proposed), f"{label}: evidence={evidence}"
    # curated dicts carry ONLY cataloged tokens -> no unknown (the prototype property).
    assert unknown == [], f"{label}: unknown={unknown}"
    declare = confirm(proposed, {"action": "confirm"})
    assert is_declare(declare) and declare == expected, f"{label}: DECLARE={declare}"
    _m, resolved = _resolve_from_declare(declare, tables)
    assert len(resolved) == exp_len, f"{label}: resolved={len(resolved)}"


def test_prototype_floor_labstat_bls_inference(detection_hints, tables):
    """35-floor: the labstat_bls DWP-3 case — bls-oews INFERRED from a url_pattern/config_key (no SDK)."""
    signals = _PROTO_FIXTURES[2][1]
    proposed, evidence, _ = suggest(signals, detection_hints)
    assert "bls-oews" in proposed, proposed
    bls_ev = evidence.get("bls-oews", [])
    assert any(surface in ("url_patterns", "config_keys") for (surface, _t, _h) in bls_ev), bls_ev
    declare = confirm(proposed, {"action": "confirm"})
    _m, resolved = _resolve_from_declare(declare, tables)
    assert ("thirdparty_rest_key", "BLS_OEWS_API_KEY") in resolved
    assert ("gcp_api", "BLS_OEWS_API_KEY") not in resolved


def test_prototype_floor_failclosed_branch(detection_hints, tables):
    """35-floor SAFETY (a): §29.2 fail-closed no-confirm branch -> INERT -> nothing flows downstream."""
    signals = _PROTO_FIXTURES[0][1]
    proposed, _, _ = suggest(signals, detection_hints)
    assert proposed == ["google-maps", "spatial-db"], proposed
    for human_action in ({"action": "reject"}, {"action": "no_response"},
                         {"action": "edits_pending"}, None):
        result = confirm(proposed, human_action)
        assert result is INERT and not is_declare(result), f"{human_action}: {result!r}"
        flowed = False
        if is_declare(result):  # MUST NOT execute for INERT
            flowed = True
            _resolve_from_declare(result, tables)
        assert flowed is False, f"{human_action}: INERT reached generate()"


def test_prototype_floor_over_proposal(detection_hints, tables):
    """35-floor SAFETY (b): OVER-proposal (curated stray maps URL) -> human EDIT removes -> not in DECLARE."""
    over_signals = {
        "sdk_imports": ["google.cloud.documentai"],
        "url_patterns": ["documentai.googleapis.com", "maps.googleapis.com"],
        "config_keys": [], "data_signals": [],
    }
    proposed, _, _ = suggest(over_signals, detection_hints)
    assert "google-maps" in proposed and "document-parsing" in proposed, proposed
    edited = [s for s in proposed if s != "google-maps"]
    declare = confirm(proposed, {"action": "confirm", "set": edited})
    assert declare == ["document-parsing"], declare
    _m, resolved = _resolve_from_declare(declare, tables)
    assert len(resolved) == 6
    assert ("gcp_api", "google-maps") not in resolved
    assert ("gcp_secret", "MAPS_API_KEY") not in resolved


def test_prototype_floor_under_proposal(detection_hints, tables):
    """35-floor SAFETY (c): UNDER-proposal (curated missed BLS) -> human EDIT adds -> in DECLARE."""
    under_signals = {
        "sdk_imports": ["google.cloud.documentai"],
        "url_patterns": [], "config_keys": [], "data_signals": [],
    }
    proposed, _, _ = suggest(under_signals, detection_hints)
    assert proposed == ["document-parsing"], proposed
    added = sorted(set(proposed) | {"bls-oews"})
    declare = confirm(proposed, {"action": "confirm", "set": added})
    assert declare == ["bls-oews", "document-parsing"], declare
    _m, resolved = _resolve_from_declare(declare, tables)
    assert len(resolved) == 7
    assert ("thirdparty_rest_key", "BLS_OEWS_API_KEY") in resolved


# ===========================================================================
# P6 — the engine RUNS on the §29.1 project fixtures (Layer S, neuro=False) and produces the expected
# signals feeding P1. (existence + fixtures + evidence-bearing proposals; NOT accuracy.)
# ===========================================================================

# (fixture-name, expected proposed DECLARE set, expected resolved len)
_FIXTURE_CASES = [
    ("prospector", ["google-maps", "spatial-db"], 8),
    ("scienceclaw", ["document-parsing"], 6),
    ("labstat_bls", ["bls-oews", "document-parsing"], 7),
]


@pytest.mark.parametrize("name,expected_declare,exp_len", _FIXTURE_CASES)
def test_p6_engine_runs_on_fixtures(name, expected_declare, exp_len, detection_hints):
    """P6: examine(fixture_dir) (Layer S, neuro=False) extracts the four signal surfaces and feeds a
    proposal == the §23 set. The engine exists, runs hermetically (no network/model), produces signals."""
    signals = examine(_FIXTURES / name)            # neuro=False default — Layer S only, hermetic
    assert set(signals.keys()) == set(HINT_FIELDS), signals.keys()
    assert "_sources" not in signals, "neuro=False must not attach a provenance map"
    proposed, evidence, _unknown = suggest(signals, detection_hints)
    assert proposed == sorted(expected_declare), f"{name}: proposed={proposed}; signals={signals}"
    assert all(evidence.get(sid) for sid in proposed), f"{name}: evidence={evidence}"


def test_p6_examine_is_ast_not_grep(detection_hints):
    """P6 (AST-not-grep discipline, §28): a commented-out import / a string-mention is NOT flagged.
    prospector's map.js has a commented `import {documentai} from "google.cloud.documentai"` that must
    NOT contribute document-parsing; scienceclaw's parse.py has a commented `import google.maps`."""
    pros = examine(_FIXTURES / "prospector")
    assert "google.cloud.documentai" not in pros["sdk_imports"], pros["sdk_imports"]
    sci = examine(_FIXTURES / "scienceclaw")
    assert "google.maps" not in sci["sdk_imports"], sci["sdk_imports"]
    # and the proposals reflect it (no document-parsing for prospector, no google-maps for scienceclaw)
    pros_p, _, _ = suggest(pros, detection_hints)
    sci_p, _, _ = suggest(sci, detection_hints)
    assert "document-parsing" not in pros_p, pros_p
    assert "google-maps" not in sci_p, sci_p


# ===========================================================================
# P1 — full choreography on the REAL fixtures: examine -> suggest -> confirm_presented -> P3 DECLARE ->
# unchanged generate->resolve == 8/6/7 byte-identical to the §23 sets.
# ===========================================================================
@pytest.mark.parametrize("name,expected_declare,exp_len", _FIXTURE_CASES)
def test_p1_choreography_fixtures(name, expected_declare, exp_len, detection_hints, tables):
    """P1: for each fixture, confirm_presented(suggest(examine(fixture)), CONFIRM) == the §23 DECLARE
    set byte-identical; then unchanged generate(D)->resolve() len == 8/6/7."""
    signals = examine(_FIXTURES / name)
    proposed, evidence, _ = suggest(signals, detection_hints)
    presentation = build_presentation(proposed, evidence, tables["catalog"])
    declare = confirm_presented(presentation, proposed, {"action": "confirm"})
    assert is_declare(declare), f"{name}: confirm produced INERT"
    assert declare == sorted(expected_declare), f"{name}: DECLARE={declare}"
    out = declare_from_confirm(declare, tables["catalog"], tables["categories"],
                               tables["baseline"], tables["library"])
    assert out is not None
    record, _manifest, resolved = out
    assert record["provenance"] == "P3"
    assert len(resolved) == exp_len, f"{name}: resolved={len(resolved)}"


# ===========================================================================
# P2a-d — fail-closed: the 4 no-confirm actions on the prospector fixture proposal -> INERT, and
# declare_from_confirm() short-circuits (generate is NEVER called — asserted by a call-counter).
# ===========================================================================
@pytest.mark.parametrize("label,human_action", [
    ("P2a-reject", {"action": "reject"}),
    ("P2b-no_response", {"action": "no_response"}),
    ("P2c-edits_pending", {"action": "edits_pending"}),
    ("P2d-none", None),
])
def test_p2_failclosed(label, human_action, detection_hints, tables, monkeypatch):
    """P2a-d: a no-confirm action -> INERT; declare_from_confirm short-circuits, generate() NOT called.
    The 'generate NOT called' is asserted by EXECUTION via a call-counter on the imported generate."""
    import builder_deploy_core.suggest.declare as declare_mod

    calls = {"generate": 0}
    real_generate = declare_mod.generate

    def _counting_generate(*a, **k):
        calls["generate"] += 1
        return real_generate(*a, **k)

    monkeypatch.setattr(declare_mod, "generate", _counting_generate)

    signals = examine(_FIXTURES / "prospector")
    proposed, evidence, _ = suggest(signals, detection_hints)
    presentation = build_presentation(proposed, evidence, tables["catalog"])
    result = confirm_presented(presentation, proposed, human_action)
    assert result is INERT and not is_declare(result), f"{label}: {result!r}"

    out = declare_from_confirm(result, tables["catalog"], tables["categories"],
                               tables["baseline"], tables["library"])
    assert out is None, f"{label}: INERT produced a non-None wiring output: {out}"
    assert calls["generate"] == 0, f"{label}: generate() was called {calls['generate']}x for an INERT result"


# ===========================================================================
# P2e — over-proposal fixture: human EDIT removes google-maps -> DECLARE==[document-parsing]; resolve==6.
# ===========================================================================
def test_p2e_over_proposal_fixture(detection_hints, tables):
    """P2e: over-proposal fixture proposes google-maps (stray maps URL); human EDIT removes it ->
    DECLARE==[document-parsing]; resolve()==6; NO (gcp_api,google-maps) and NO (gcp_secret,MAPS_API_KEY)."""
    signals = examine(_FIXTURES / "over-proposal")
    proposed, evidence, _ = suggest(signals, detection_hints)
    assert "google-maps" in proposed and "document-parsing" in proposed, proposed
    presentation = build_presentation(proposed, evidence, tables["catalog"])
    edited = [s for s in proposed if s != "google-maps"]
    declare = confirm_presented(presentation, proposed, {"action": "confirm", "set": edited})
    assert declare == ["document-parsing"], declare
    record, _m, resolved = declare_from_confirm(
        declare, tables["catalog"], tables["categories"], tables["baseline"], tables["library"])
    assert len(resolved) == 6
    assert ("gcp_api", "google-maps") not in resolved
    assert ("gcp_secret", "MAPS_API_KEY") not in resolved


# ===========================================================================
# P2f — under-proposal fixture: human EDIT adds bls-oews -> DECLARE==[bls-oews,document-parsing]; resolve==7.
# ===========================================================================
def test_p2f_under_proposal_fixture(detection_hints, tables):
    """P2f: under-proposal fixture misses bls-oews; human EDIT adds it -> DECLARE==[bls-oews,
    document-parsing]; resolve()==7; (thirdparty_rest_key,BLS_OEWS_API_KEY) present."""
    signals = examine(_FIXTURES / "under-proposal")
    proposed, evidence, _ = suggest(signals, detection_hints)
    assert proposed == ["document-parsing"], proposed
    presentation = build_presentation(proposed, evidence, tables["catalog"])
    added = sorted(set(proposed) | {"bls-oews"})
    declare = confirm_presented(presentation, proposed, {"action": "confirm", "set": added})
    assert declare == ["bls-oews", "document-parsing"], declare
    record, _m, resolved = declare_from_confirm(
        declare, tables["catalog"], tables["categories"], tables["baseline"], tables["library"])
    assert len(resolved) == 7
    assert ("thirdparty_rest_key", "BLS_OEWS_API_KEY") in resolved


# ===========================================================================
# P3 — module-identity: generate/resolve are the IMPORTED 2.1 callables; suggest/ defines NEITHER.
# ===========================================================================
def test_p3_module_identity():
    """P3: builder_deploy_core.discovery.generate.generate and ...resolution.resolve.resolve are the
    IMPORTED 2.1 callables (their __module__ is the builder_deploy_core.* core module); the suggest/
    package defines NO generate/resolve of its own (assert absence)."""
    from builder_deploy_core.discovery.generate import generate as core_generate
    from builder_deploy_core.resolution.resolve import resolve as core_resolve
    from builder_deploy_core.suggest import declare as declare_mod

    assert core_generate.__module__ == "builder_deploy_core.discovery.generate", core_generate.__module__
    assert core_resolve.__module__ == "builder_deploy_core.resolution.resolve", core_resolve.__module__

    # the wiring imports the SAME object (module-identity, not a copy).
    assert declare_mod.generate is core_generate, "declare.py rebound generate (not module-identity)"
    assert declare_mod.resolve is core_resolve, "declare.py rebound resolve (not module-identity)"

    # the suggest/ package defines NO generate/resolve symbol of its own.
    import builder_deploy_core.suggest as suggest_pkg
    import builder_deploy_core.suggest.suggest as suggest_mod
    import builder_deploy_core.suggest.confirm as confirm_mod
    import builder_deploy_core.suggest.examine as examine_mod
    import builder_deploy_core.suggest.evidence as evidence_mod
    for mod in (suggest_pkg, suggest_mod, confirm_mod, examine_mod, evidence_mod):
        for name in ("generate", "resolve"):
            obj = getattr(mod, name, None)
            # the only place generate/resolve appear is declare.py, where they are the IMPORTED core
            # objects (asserted above). They must NOT be locally-DEFINED functions in any suggest module.
            if obj is not None:
                assert obj.__module__.startswith("builder_deploy_core.discovery") or \
                       obj.__module__.startswith("builder_deploy_core.resolution"), \
                    f"{mod.__name__}.{name} is not the imported core callable: {obj.__module__}"


# ===========================================================================
# P4a — evidence present: every proposed service carries non-empty (surface, token, hint) evidence.
# ===========================================================================
@pytest.mark.parametrize("name,expected_declare,_exp_len", _FIXTURE_CASES)
def test_p4a_evidence_present(name, expected_declare, _exp_len, detection_hints):
    """P4a: every proposed service in P1 carries non-empty evidence[sid]; each row is
    (surface, observed_token, matched_hint)."""
    signals = examine(_FIXTURES / name)
    proposed, evidence, _ = suggest(signals, detection_hints)
    for sid in proposed:
        rows = evidence.get(sid)
        assert rows, f"{name}/{sid}: no evidence"
        for row in rows:
            assert isinstance(row, tuple) and len(row) == 3, f"{name}/{sid}: bad evidence row {row!r}"
            surface, token, hint = row
            assert surface in HINT_FIELDS and isinstance(token, str) and isinstance(hint, str)


# ===========================================================================
# P4b — contract shape + the three anti-rubber-stamp invariants (§4-#3).
# ===========================================================================
def test_p4b_contract_shape(detection_hints, tables):
    """P4b: the §2.5 confirm-contract: the CandidatePresentation for each candidate carries
    {service_id, entries_preview (the to-be-provisioned hard recipe), evidence rows, source tag}; the
    anti-rubber-stamp invariants hold (presentation materialized, per-candidate evidence, source flagged)."""
    signals = examine(_FIXTURES / "prospector")
    proposed, evidence, _ = suggest(signals, detection_hints)
    presentation = build_presentation(proposed, evidence, tables["catalog"])

    assert {cp.service_id for cp in presentation} == set(proposed)
    for cp in presentation:
        assert cp.service_id in proposed
        assert cp.entries_preview == tables["catalog"][cp.service_id]["entries"], cp.service_id
        assert cp.evidence, f"{cp.service_id}: empty evidence in presentation"
        assert cp.source in ("symbolic", "neuro"), cp.source

    contract = check_contract(presentation, proposed)
    assert contract.ok, contract.detail
    assert contract.presentation_materialized      # invariant 1: no bulk blind-accept
    assert contract.has_per_candidate_evidence     # per-candidate evidence
    assert contract.sources_flagged                # source provenance flagged


def test_p4b_invariant1_blocks_unpresented_confirm(detection_hints, tables):
    """P4b invariant 1 (NO bulk blind-accept): a CONFIRM against an EMPTY/un-materialized presentation
    is rejected -> INERT, even with an explicit {action: confirm}."""
    signals = examine(_FIXTURES / "prospector")
    proposed, _evidence, _ = suggest(signals, detection_hints)
    # no presentation materialized -> confirm_presented must fail closed.
    result = confirm_presented([], proposed, {"action": "confirm"})
    assert result is INERT, "an un-presented proposal was CONFIRMED (bulk blind-accept leaked)"


def test_p4b_invariant3_no_response_is_inert(detection_hints, tables):
    """P4b invariant 3 (no-response ≡ ⊥): even with a valid presentation, a no_response action -> INERT."""
    signals = examine(_FIXTURES / "prospector")
    proposed, evidence, _ = suggest(signals, detection_hints)
    presentation = build_presentation(proposed, evidence, tables["catalog"])
    assert confirm_presented(presentation, proposed, {"action": "no_response"}) is INERT
    assert confirm_presented(presentation, proposed, None) is INERT


# ===========================================================================
# P5b — P3 provenance: the confirmed DECLARE record is tagged P3, distinct from a hand-authored manifest.
# ===========================================================================
def test_p5b_p3_provenance(detection_hints, tables):
    """P5b: the confirmed DECLARE record is tagged P3 (agent-proposed + human-ratified)."""
    record = tag_declare(["document-parsing"])
    assert record["provenance"] == "P3"
    assert record["services"] == ["document-parsing"]

    # and the wired path tags it P3 too.
    signals = examine(_FIXTURES / "scienceclaw")
    proposed, evidence, _ = suggest(signals, detection_hints)
    presentation = build_presentation(proposed, evidence, tables["catalog"])
    declare = confirm_presented(presentation, proposed, {"action": "confirm"})
    out = declare_from_confirm(declare, tables["catalog"], tables["categories"],
                               tables["baseline"], tables["library"])
    wired_record, _m, _r = out
    assert wired_record["provenance"] == "P3"


# ===========================================================================
# Layer N — REPORTED-only, gate-inert: neuro=True attaches a provenance map; default examine is hermetic.
# (the named R-egress residual is REPORTED-only; this asserts the gated default never engages it.)
# ===========================================================================
def test_layer_n_is_reported_only_and_gate_inert():
    """The gated default (neuro=False) is hermetic Layer S (no _sources). neuro=True attaches a
    _sources provenance map but contributes nothing by default (no model wired in 2.2) — gate-inert."""
    gated = examine(_FIXTURES / "scienceclaw")                  # neuro=False default
    assert "_sources" not in gated
    reported = examine(_FIXTURES / "scienceclaw", neuro=True)   # REPORTED path
    assert "_sources" in reported
    # neuro adds nothing by default -> the symbolic signal surfaces are identical.
    for surface in HINT_FIELDS:
        assert reported[surface] == gated[surface], surface
    # every provenance tag is 'symbolic' (no model wired -> no neuro-sourced token in 2.2).
    assert all(src == "symbolic" for src in reported["_sources"].values())
