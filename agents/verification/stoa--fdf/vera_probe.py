# VERA independent verification harness — stoa--fdf (u--9s2 Phase-2 inc 2.2 SUGGEST front-door)
# author: Denson Smith
# Independent of test_suggest.py — VERA re-derives the probes from design-rev2 §3 and exercises
# the BUILT package directly. The load-bearing piece is the §29.2 fail-closed call-counter probe:
# generate() is monkeypatched with an instrumented counter on the WIRED path (declare module's
# imported symbol) so "generate called 0x" is asserted by EXECUTION, not by grep.

import sys
from pathlib import Path

PKG_ROOT = Path(__file__).resolve().parents[2] / "builder-deploy-core"
DATA_ROOT = PKG_ROOT / "data"
FIX = PKG_ROOT / "tests" / "fixtures" / "suggest-projects"

from builder_deploy_core import dataload
from builder_deploy_core.suggest import (
    examine, suggest, confirm, confirm_presented, is_declare, INERT,
    CONFIRM, REJECT, NO_RESPONSE, EDITS_PENDING,
    declare_from_confirm, build_presentation, check_contract, PROVENANCE_P3,
)
from builder_deploy_core.suggest import declare as declare_mod

results = []
def rec(pid, ok, detail):
    results.append((pid, ok, detail))
    print(f"[{'PASS' if ok else 'FAIL'}] {pid}: {detail}")

# --- load DATA tables independently via dataload (same path the caller uses) ---
catalog, categories = dataload.load_catalog(data_root=DATA_ROOT)
baseline = dataload.load_baseline(data_root=DATA_ROOT)
library = dataload.load_library(data_root=DATA_ROOT)
hints = dataload.load_detection_hints(data_root=DATA_ROOT)

# ===========================================================================
# P6 — examine() runs on the 5 fixtures (Layer S, neuro=False) and yields signals
# ===========================================================================
fixtures = ["prospector", "scienceclaw", "labstat_bls", "over-proposal", "under-proposal"]
signals = {}
for name in fixtures:
    signals[name] = examine(FIX / name, neuro=False)
rec("P6", all(isinstance(signals[n], dict) for n in fixtures),
    f"examine ran Layer-S on all 5 fixtures; e.g. prospector={signals['prospector']}")

# ===========================================================================
# P1 — choreography: confirm(suggest(examine(fix)),CONFIRM)==DECLARE; resolve len 8/6/7
# ===========================================================================
EXPECTED_LEN = {"prospector": 8, "scienceclaw": 6, "labstat_bls": 7}
EXPECTED_DECLARE = {
    # §23 DECLARE sets (test_suggest.py:70/181): prospector is a geo project with BOTH a Maps-JS
    # import AND a spatial-data flow -> proposes google-maps + spatial-db -> resolve 8.
    "prospector": ["google-maps", "spatial-db"],
    "scienceclaw": ["document-parsing"],
    "labstat_bls": ["bls-oews", "document-parsing"],
}
for name in ["prospector", "scienceclaw", "labstat_bls"]:
    proposed, evidence, unknown = suggest(signals[name], hints)
    D = confirm(proposed, {"action": "confirm"})
    declare_ok = (D == sorted(EXPECTED_DECLARE[name]))
    out = declare_from_confirm(D, catalog, categories, baseline, library)
    declare_record, manifest, resolved = out
    length = len(resolved)
    len_ok = (length == EXPECTED_LEN[name])
    p3_ok = (declare_record["provenance"] == PROVENANCE_P3)
    rec(f"P1-{name}", declare_ok and len_ok,
        f"proposed={proposed} DECLARE={D} (exp {sorted(EXPECTED_DECLARE[name])}); "
        f"resolve len={length} (exp {EXPECTED_LEN[name]}); P3-tag={p3_ok}")

# ===========================================================================
# P2a-d — FAIL-CLOSED with an EXECUTION call-counter on the WIRED generate()
#   Monkeypatch the generate symbol the declare module imported; assert it is
#   called 0x for every no-confirm action.
# ===========================================================================
proposed_p, _, _ = suggest(signals["prospector"], hints)
real_generate = declare_mod.generate
NOCONFIRM = {
    "P2a-reject":       {"action": "reject"},
    "P2b-no_response":  {"action": "no_response"},
    "P2c-edits_pending":{"action": "edits_pending"},
    "P2d-none":         None,
}
for pid, action in NOCONFIRM.items():
    counter = {"n": 0}
    def instrumented(*a, **k):
        counter["n"] += 1
        return real_generate(*a, **k)
    declare_mod.generate = instrumented
    try:
        D = confirm(proposed_p, action)
        inert = (D is INERT)
        decl_false = (is_declare(D) is False)
        out = declare_from_confirm(D, catalog, categories, baseline, library)
        none_ok = (out is None)
        gen_zero = (counter["n"] == 0)
    finally:
        declare_mod.generate = real_generate
    rec(pid, inert and decl_false and none_ok and gen_zero,
        f"confirm->INERT={inert}; is_declare False={decl_false}; "
        f"declare_from_confirm None={none_ok}; generate call-counter={counter['n']} (must be 0)")

# sanity: counter actually increments on a real CONFIRM (proves the counter is wired, not dead)
counter = {"n": 0}
def instrumented2(*a, **k):
    counter["n"] += 1
    return real_generate(*a, **k)
declare_mod.generate = instrumented2
try:
    D = confirm(proposed_p, {"action": "confirm"})
    declare_from_confirm(D, catalog, categories, baseline, library)
finally:
    declare_mod.generate = real_generate
rec("P2-counter-liveness", counter["n"] == 1,
    f"on a REAL confirm the same counter == {counter['n']} (proves the call-counter is live, not dead)")

# ===========================================================================
# P2e — over-proposal: stray maps URL proposes google-maps; EDIT removes -> DECLARE=[document-parsing]; resolve 6
# ===========================================================================
proposed_o, ev_o, unk_o = suggest(signals["over-proposal"], hints)
over_proposes_gmaps = "google-maps" in proposed_o
D_edit = confirm(proposed_o, {"action": "confirm", "set": ["document-parsing"]})
_, manifest_o, resolved_o = declare_from_confirm(D_edit, catalog, categories, baseline, library)
# resolved_o is a list of (kind, name) tuples (the §2 resolved set)
no_gmaps = ("gcp_api", "google-maps") not in resolved_o
no_mapskey = not any(n == "MAPS_API_KEY" for (_k, n) in resolved_o)
rec("P2e-overproposal",
    over_proposes_gmaps and D_edit == ["document-parsing"] and len(resolved_o) == 6 and no_gmaps and no_mapskey,
    f"over proposes google-maps={over_proposes_gmaps}; EDIT-remove DECLARE={D_edit}; resolve len={len(resolved_o)} (exp 6); "
    f"no google-maps entry={no_gmaps}; no MAPS_API_KEY={no_mapskey}")

# ===========================================================================
# P2f — under-proposal: misses bls-oews; EDIT adds -> DECLARE=[bls-oews,document-parsing]; resolve 7; BLS_OEWS_API_KEY present
# ===========================================================================
proposed_u, ev_u, unk_u = suggest(signals["under-proposal"], hints)
under_misses_bls = "bls-oews" not in proposed_u
D_add = confirm(proposed_u, {"action": "confirm", "set": ["bls-oews", "document-parsing"]})
_, manifest_u, resolved_u = declare_from_confirm(D_add, catalog, categories, baseline, library)
bls_key_present = any(n == "BLS_OEWS_API_KEY" for (_k, n) in resolved_u)
rec("P2f-underproposal",
    under_misses_bls and D_add == ["bls-oews", "document-parsing"] and len(resolved_u) == 7 and bls_key_present,
    f"under misses bls-oews={under_misses_bls}; EDIT-add DECLARE={D_add}; resolve len={len(resolved_u)} (exp 7); "
    f"BLS_OEWS_API_KEY present={bls_key_present}")

# ===========================================================================
# Watch-item 4 — INERT 'unknown' bucket never leaks into proposed/DECLARE/8-6-7
# ===========================================================================
leak = False
detail_unknown = []
for name in ["prospector", "scienceclaw", "labstat_bls"]:
    proposed, evidence, unknown = suggest(signals[name], hints)
    unk_tokens = {tok for (_surface, tok) in unknown}
    overlap = unk_tokens & set(proposed)
    detail_unknown.append(f"{name}: unknown={sorted(unk_tokens)} proposed={proposed} overlap={overlap}")
    if overlap:
        leak = True
rec("WATCH4-unknown-inert", not leak,
    "unknown bucket disjoint from proposed (never affects DECLARE/8-6-7): " + " | ".join(detail_unknown))

# ===========================================================================
# P3 — module-identity RUNTIME assert
# ===========================================================================
from builder_deploy_core.discovery.generate import generate as core_generate
from builder_deploy_core.resolution.resolve import resolve as core_resolve
import builder_deploy_core.suggest.declare as dm
gen_identity = (dm.generate is core_generate)
res_identity = (dm.resolve is core_resolve if hasattr(dm, "resolve") else True)
gen_mod_ok = core_generate.__module__.startswith("builder_deploy_core")
res_mod_ok = core_resolve.__module__.startswith("builder_deploy_core")
# suggest/ package defines no generate/resolve of its own
import builder_deploy_core.suggest as sp
sp_defines_none = not hasattr(sp, "generate") or sp.__dict__.get("generate") is None
# check the package source files literally do not define generate/resolve
suggest_dir = PKG_ROOT / "builder_deploy_core" / "suggest"
own_defs = []
for pyf in suggest_dir.glob("*.py"):
    txt = pyf.read_text(encoding="utf-8")
    for line in txt.splitlines():
        s = line.strip()
        if s.startswith("def generate") or s.startswith("def resolve"):
            own_defs.append(f"{pyf.name}:{s}")
rec("P3-module-identity",
    gen_identity and gen_mod_ok and res_mod_ok and not own_defs,
    f"declare.generate IS core_generate={gen_identity}; generate.__module__={core_generate.__module__}; "
    f"resolve.__module__={core_resolve.__module__}; suggest/ defines own generate/resolve={own_defs or 'NONE'}")

# ===========================================================================
# P4a — evidence present + shape (surface, observed_token, matched_hint)
# ===========================================================================
p4a_ok = True
p4a_detail = []
for name in ["prospector", "scienceclaw", "labstat_bls"]:
    proposed, evidence, unknown = suggest(signals[name], hints)
    for sid in proposed:
        rows = evidence.get(sid, [])
        if not rows or not all(isinstance(r, tuple) and len(r) == 3 for r in rows):
            p4a_ok = False
    p4a_detail.append(f"{name}:{ {s: len(evidence.get(s,[])) for s in proposed} }")
rec("P4a-evidence-present", p4a_ok, "every proposed carries non-empty 3-tuple evidence rows: " + " | ".join(p4a_detail))

# ===========================================================================
# P4b — confirm-contract shape + 3 anti-rubber-stamp invariants
# ===========================================================================
proposed_s, ev_s, _ = suggest(signals["scienceclaw"], hints)
presentation = build_presentation(proposed_s, ev_s, catalog)
contract = check_contract(presentation, proposed_s)
shape_ok = all(hasattr(p, "service_id") for p in presentation)
# invariant 1: no bulk blind-accept — confirm_presented against an EMPTY presentation -> INERT
empty_pres = []
inv1 = confirm_presented(empty_pres, proposed_s, {"action": "confirm"}) is INERT
# invariant 3: no-response is structurally INERT
inv3 = confirm_presented(presentation, proposed_s, {"action": "no_response"}) is INERT
# valid presentation + CONFIRM -> DECLARE
valid_confirm = confirm_presented(presentation, proposed_s, {"action": "confirm"}) == sorted(proposed_s)
rec("P4b-contract-shape",
    contract.ok and shape_ok and inv1 and inv3 and valid_confirm,
    f"contract.ok={contract.ok}; presentation shape ok={shape_ok}; "
    f"inv1 no-bulk-blind-accept(empty pres->INERT)={inv1}; inv3 no_response->INERT={inv3}; "
    f"valid-pres+CONFIRM->DECLARE={valid_confirm}")

# ===========================================================================
# P5a — hints DATA load + tolerance PIN + hints NEG
# ===========================================================================
# POS: load_detection_hints loads all 4 services' hint sets
pos_ok = set(hints.keys()) == {"google-maps", "spatial-db", "document-parsing", "bls-oews"} and \
         all(set(hints[s].keys()) <= {"sdk_imports","url_patterns","config_keys","data_signals"} for s in hints)
# PIN: real 4-record catalog (with [detection_hints]) loads clean through UNCHANGED load_catalog;
#      record shape stays {entries,gcp_api,category} — no detection_hints leak
cat2, cats2 = dataload.load_catalog(data_root=DATA_ROOT)
pin_4recs = len(cat2) == 4
sample = next(iter(cat2.values()))
pin_no_leak = "detection_hints" not in sample and set(sample.keys()) == {"entries", "gcp_api", "category"}
# NEG: unknown sub-key under [detection_hints] -> DataIntegrityError from load_detection_hints
from builder_deploy_core.errors import DataIntegrityError
import shutil, tempfile
neg_ok = False
neg_detail = ""
tmpd = Path(tempfile.mkdtemp(prefix="vera-fdf-neg-"))
try:
    shutil.copytree(DATA_ROOT, tmpd / "data")
    gmap = tmpd / "data" / "catalog" / "google-maps.toml"
    txt = gmap.read_text(encoding="utf-8")
    txt += '\nmystery = ["x"]\n'  # unknown sub-key under [detection_hints] (it's the last table)
    gmap.write_text(txt, encoding="utf-8")
    try:
        dataload.load_detection_hints(data_root=tmpd / "data")
        neg_detail = "NO error raised (FAIL)"
    except DataIntegrityError as e:
        neg_ok = True
        neg_detail = f"DataIntegrityError raised: {str(e)[:80]}"
    except Exception as e:
        neg_detail = f"WRONG exception {type(e).__name__}: {str(e)[:80]}"
finally:
    shutil.rmtree(tmpd, ignore_errors=True)
rec("P5a-hints+pin+neg",
    pos_ok and pin_4recs and pin_no_leak and neg_ok,
    f"POS hints loaded for {sorted(hints.keys())}; PIN load_catalog clean 4 recs={pin_4recs} no-leak={pin_no_leak} "
    f"(shape={sorted(sample.keys())}); NEG unknown-subkey->{neg_detail}")

# ===========================================================================
# P5b — P3 provenance tag distinct
# ===========================================================================
proposed_pr, _, _ = suggest(signals["prospector"], hints)
D = confirm(proposed_pr, {"action": "confirm"})
rec_pr, _, _ = declare_from_confirm(D, catalog, categories, baseline, library)
rec("P5b-p3-provenance",
    rec_pr["provenance"] == "P3" and rec_pr["services"] == ["google-maps", "spatial-db"],
    f"DECLARE record provenance={rec_pr['provenance']} (P3); services={rec_pr['services']}")

print("\n==== SUMMARY ====")
fails = [r for r in results if not r[1]]
print(f"{len(results)} probes; {len(results)-len(fails)} PASS, {len(fails)} FAIL")
if fails:
    for pid, _, d in fails:
        print(f"  FAIL {pid}: {d}")
    sys.exit(1)
print("ALL INDEPENDENT PROBES PASS")
