---
author: Denson Smith
ticket: stoa--pj3 (u--9s2 Phase-2 increment 2.1)
seat: CAPTAIN_VERA_the_stoa (VERIFIER)
gauntlet-stage: 4/6
operating-mode: autonomous
as_of: 2026-06-26
---

# VERA verification verdict — stoa--pj3 builder-deploy-core promotion

status: completed
ticket: stoa--pj3
verdict: pass
design_artifact_verified_against: agents/design/stoa--pj3/design-rev2.md (probes P1–P11, §3)
build_verified: arc-75/build worktree, commit 8467d10 (agents/builder-deploy-core/)

## Verification posture

Every probe was re-executed INDEPENDENTLY against the built deliverable — I did not
rely on ADA's self-report. Beyond re-running the 40-case bespoke pytest suite, I
(a) confirmed the test files actually ASSERT what each probe claims (not vacuous
passes), (b) re-derived the 8/6/7 resolved sets via a direct `resolve()` call
outside the test harness, (c) confirmed the P11 corrupt fixtures genuinely contain
the claimed corruption (4-entry baseline, 6-entry baseline, empty scope_bearing,
dangling category ref — anti-vacuous), (d) confirmed the two frozen functions
(`derive_sa_scope`, `check_runtime_completeness`) are byte-identical to the
VERIFIED Phase-1 prototype on read, and (e) ran the FULL existing the-stoa suite.
Env: Python 3.11.4, tomllib OK, pytest 8.3.5; gen-data/vitest/vite via npm.

probes_executed:
- probe_id: P1
  description: resolution exact sets 8/6/7 byte-for-byte (§8.1/8.2/8.3, DoD #1)
  quadrant_classification: easy-easy
  command_or_method: python -m pytest tests/test_resolution.py + an independent direct resolve() of all 3 builders
  expected: prospector→8, scienceclaw→6, labstat_bls→7, exact (kind,name) sets
  observed: test_resolution_exact_set[prospector/scienceclaw/labstat_bls] PASSED; independent direct resolve printed exactly the §8.1/8.2/8.3 sets (8/6/7, byte-for-byte incl. pgvector baseline + postgis + google-maps/MAPS_API_KEY pairing)
  result: pass
- probe_id: P2
  description: §8.4 BaselineOmitError parametrized over ALL 5 baseline entries (R1-close generalization, DoD #1)
  quadrant_classification: easy-easy
  command_or_method: python -m pytest tests/test_resolution.py (canonical pgvector + parametrized entry0..entry4)
  expected: omit of EACH of the 5 baseline entries raises BaselineOmitError naming that entry, no set returned
  observed: test_baseline_omit_canonical_pgvector PASSED + test_baseline_omit_guard_fires_for_every_baseline_entry[entry0..entry4] all 5 PASSED; verified parametrization is over dataload.EXPECTED_BASELINE (all 5, not just pgvector)
  result: pass
- probe_id: P3
  description: generate→resolve→8/6/7 + manifest-equivalence to §8 hand-authored, alias-aware (DoD #2)
  quadrant_classification: easy-easy
  command_or_method: python -m pytest tests/test_discovery.py -k generate
  expected: each builder's services→{category,delta} resolves to 8/6/7 == its §8 hand-authored twin
  observed: test_generate_resolves_to_exact_set[all 3] + test_generated_equivalent_to_hand_authored[all 3] + test_labstat_generated_delta_add PASSED
  result: pass
- probe_id: P4
  description: V1–V5 pass on positives; NEG-1 (V5 fail-closed) + NEG-2 (UncatalogedServiceError + V1 fail) (DoD #3)
  quadrant_classification: easy-easy
  command_or_method: python -m pytest tests/test_discovery.py (validate + neg cases)
  expected: V1–V5 all PASS on the 3 positives; NEG-1 trips V5; NEG-2 raises UncatalogedServiceError + trips V1
  observed: test_validate_all_pass[all 3] + test_neg1_v5_fails_on_undeclared_drift + test_neg2_generate_raises_uncataloged + test_neg2_v1_fails_naming_uncataloged PASSED
  result: pass
- probe_id: P5
  description: resolved-set properties — SA-scope §5.A, runtime-completeness §3.4, kind-dispatch §3.3 (DoD #4)
  quadrant_classification: easy-easy
  command_or_method: python -m pytest tests/test_resolution.py + independent derive_sa_scope print
  expected: SA-scope excludes railway_var/db_extension; prospector carries BOTH (gcp_api,google-maps) AND (gcp_secret,MAPS_API_KEY); labstat_bls BLS_OEWS_API_KEY is thirdparty_rest_key, mints no gcp_api, excluded from S1
  observed: test_runtime_completeness[all 3] + test_prospector_carries_both_maps_pairing + test_labstat_kind_dispatch + test_sa_scope_is_scope_bearing_subset[all 3] PASSED; independent SA-scope print confirms only gcp_api/gcp_secret/thirdparty_rest_key entries appear, railway_var/db_extension excluded
  result: pass
- probe_id: P6
  description: DATA externalized + READ (DoD #5) — resolver reflects a mutated DATA root; zero data literals in logic modules
  quadrant_classification: easy-easy
  command_or_method: python -m pytest tests/test_dataload.py::test_data_is_read_from_disk + independent tmp-data-root mutation + grep for literal table assignments
  expected: load_catalog reflects an added seed in a tmp data root; shipped root unchanged; ZERO BASELINE=/LIBRARY=/CATALOG=/SCOPE_BEARING_KINDS=/KEY_BEARING_PAIRING= literals in resolve.py/generate.py/validate.py
  observed: test PASSED; independent mutation — 'probe-seed' in tmp catalog = True, absent from shipped = True; grep for data-literal assignments in the 3 logic modules = ZERO (kind globals are the _UNLOADED sentinel + import-time population)
  result: pass
- probe_id: P7
  description: purity boundary (DoD #6) — no environment read outside dataload.py
  quadrant_classification: easy-easy
  command_or_method: grep -rn -E "os.environ|open(|socket|requests|urllib|subprocess|time.time|datetime.now|random" over builder_deploy_core/
  expected: only open()/tomllib.load inside dataload.py scoped to data/; everything else zero
  observed: the only hits are two descriptive comment lines + the single real open() at dataload.py:68 (scoped to _DATA_ROOT, resolved relative to __file__, never env/CWD); tomllib/open appear ONLY in dataload.py source; zero os.environ/socket/network/clock/random anywhere
  result: pass
- probe_id: P8
  description: §2-constraint (DoD #6) — discovery imports the single resolver, never re-implements
  quadrant_classification: easy-easy
  command_or_method: python -m pytest tests/test_discovery.py -k constraint + grep "def resolve" under discovery/
  expected: V4's resolve.__module__ == builder_deploy_core.resolution.resolve; ZERO def resolve under discovery/
  observed: test_constraint_resolve_is_resolution_module + test_constraint_discovery_defines_no_resolve PASSED; independent grep "def resolve" under discovery/ = ZERO; independent import check: discovery.validate.resolve.__module__ == builder_deploy_core.resolution.resolve
  result: pass
- probe_id: P9
  description: full existing the-stoa suite GREEN (DoD #7) — gen-data + vitest + vite build; the FM full-suite watch-item
  quadrant_classification: easy-easy
  command_or_method: cd app && npm install && npm run gen-data && npm test && npm run build
  expected: roster derivation + vitest + vite build stay GREEN; new core (under agents/, outside app/) breaks nothing
  observed: gen-data clean (roster 4 MAJOR / 12 CAPTAIN / 8 LIEUTENANT, COLONEL reserved-empty, HUMAN stub); vitest 41 passed (3 files); vite build OK (1595 modules transformed, built in 12.63s). ONE diff to app/src/data/generated/agents.ts = a single line in the team-launcher LIEUTENANT skill body (the stoa--fii radio-check §38 recovery cross-ref), PRE-EXISTING substrate drift NOT regenerated into this worktree snapshot — arc-75 build (8467d10) touched ZERO substrate/ + ZERO app/ files, confirming the new Python core is structurally incapable of touching the app roster. Drift is a close-gate/main-self-apply breadcrumb, NOT a build defect.
  result: pass
- probe_id: P10
  description: authorship (DoD #8) — every author-like field = Denson Smith; ZERO foreign
  quadrant_classification: easy-easy
  command_or_method: grep author|owner|creator|maintainer|copyright|by over agents/builder-deploy-core/ + pyproject author block inspection
  expected: every author-like field reads Denson Smith; zero foreign name
  observed: pyproject authors = [{ name = "Denson Smith" }]; every module header # author: Denson Smith; zero foreign author/maintainer/copyright field. Residual grep hits were the phrase "hand-authored" (manifest provenance prose, not an attribution field) — not foreign authorship.
  result: pass
- probe_id: P11
  description: DATA load-validation fail-closed (DoD #5; the r2 fix) — each corrupt tree raises DataIntegrityError naming the breached invariant, no partial table
  quadrant_classification: easy-easy
  command_or_method: python -m pytest tests/test_dataload.py + independent inspection of each corrupt fixture's actual content
  expected: 6 corrupt trees each raise DataIntegrityError; canonical baseline-missing-pgvector returns NO 4-entry baseline
  observed: test_corrupt_tree_raises_data_integrity[baseline-missing-pgvector / baseline-extra-entry / kinds-empty-scope-bearing / category-malformed-entry / catalog-missing-key / dangling-reference] all 6 PASSED + test_baseline_missing_pgvector_returns_no_partial_baseline PASSED. ANTI-VACUOUS: independently confirmed baseline-missing-pgvector/baseline.toml has exactly 4 [[entry]] blocks with no pgvector line; baseline-extra-entry has 6; kinds-empty-scope-bearing has scope_bearing = []; dangling-reference catalog names category = "nonexistent-category". The fixtures genuinely contain the corruption — the loader raises fail-closed before any degraded table escapes.
  result: pass

threat_coverage: []
# §35.5 not-threat-ratified carve-out CONFIRMED by ARGUS (no runtime attack path at t0;
# reads only in-repo, version-controlled, gauntlet-gated DATA; provisions nothing). No
# threat-anchored probe owed. P7 (purity) + the §2.4.1/P11 fail-closed checks are CORRECTNESS
# probes, not threat-defeat. Empty threat_coverage list is the valid §35.5 carve-out state.

methodology_concerns:
- NIT (CATO/close-gate, not a verdict-blocker): the build commit includes .pytest_cache/ and __pycache__/*.pyc artifacts under agents/builder-deploy-core/. A .gitignore is present at the package root; these should be ignored/untracked. Non-functional, but a hygiene item for CATO's craft review or a trailing cleanup commit.
- OBSERVATION (not a defect): P9 surfaced a pre-existing agents.ts drift (team-launcher radio-check line). This is the documented "gen-data regen re-derives the whole roster and surfaces pre-existing drift" pattern; it is unrelated to this arc and is a main-self-apply breadcrumb for the close-gate, not a build problem. Recorded so the close-gate regenerates .claude/ on main after merge.

falsifying_evidence_summary: (empty — no probe falsified any design claim)

verification_artifacts_path: agents/verdicts/stoa--pj3/vera-verdict.md (probe outputs recorded inline above; all probes re-runnable via `python -m pytest agents/builder-deploy-core/tests/` and the `app/` npm suite)

## Ruling on the two ADA flags

FLAG 1 — document/data alias-exclusion drift: **FAITHFUL (correct promotion, NOT a defect).**
Independently verified all three sub-claims:
(a) Matches the prototype: discovery-check/catalog.py CATEGORIES = {geospatial, document-consuming} only (NO document/data); the build's dataload._ALIAS_CATEGORIES = {"document/data"} excludes exactly that alias from the discovery CATEGORIES bundle while resolve's LIBRARY keeps all three. Independent check: resolve LIBRARY keys = [document-consuming, document/data, geospatial]; discovery CATEGORIES keys = [document-consuming, geospatial].
(b) labstat_bls still G2-selects document-consuming → resolves to the 7-entry §8.3 set, and the document/data alias resolves to the SAME 6-entry set as document-consuming (manifest-equivalent — independently confirmed: `document/data` resolves to 6 entries == document-consuming).
(c) The exclusion breaks no other builder's generation (all 3 builders resolve to 8/6/7; the equivalence + validate suites pass). Excluding the alias from G2 best-fit correctly avoids double-counting a same-size competing subset, exactly as ADA argued.

FLAG 2 — resolve name-shadowing in resolution/__init__.py: **NO functional breakage** (craft call is CATO's).
Independently verified: the package attribute builder_deploy_core.resolution.resolve is the re-exported FUNCTION (callable, __name__ == "resolve"); the submodule remains importable via its full dotted path (Python's import system uses sys.modules, unaffected by the attribute shadow). All consumer paths bind correctly — `from builder_deploy_core.resolution import resolve` IS the same object as `from builder_deploy_core.resolution.resolve import resolve`, and discovery.validate.resolve.__module__ == builder_deploy_core.resolution.resolve. The 40-pass suite + the §2-constraint module-identity probe corroborate. Functionally clean; readability/craft is for CATO's cold-read.

## Summary

The build was exercised by (1) the full 40-case bespoke pytest suite re-run independently
(40 passed in 0.26s), (2) direct out-of-harness re-derivation of the 8/6/7 resolved sets +
SA-scope, (3) anti-vacuous inspection of the P11 corrupt fixtures, (4) read-level
byte-identity confirmation of the two frozen functions vs the VERIFIED prototype, (5) a
purity/authorship/§2-constraint grep battery, and (6) the FULL existing the-stoa app suite
(gen-data + vitest 41/41 + vite build). The load-bearing probes were P2 (the R1-close
all-5-baseline-entry guard generalization), P11 (the r2 fail-closed DATA-load-validation
fix — the canonical baseline-missing-pgvector case correctly raises before a 4-entry
baseline can escape and silently disarm the §8.4 guard), and P9 (the full-suite watch — the
new core touched zero substrate/app files, so the roster is structurally untouched). Every
probe P1–P11 PASSED. Both ADA flags adjudicated: alias-exclusion is FAITHFUL, name-shadowing
has no functional breakage. The only methodology concerns are a committed-artifact hygiene
nit (.pytest_cache/__pycache__) for CATO and a pre-existing unrelated gen-data drift
breadcrumb for the close-gate — neither blocks the verdict. Overall: PASS.
