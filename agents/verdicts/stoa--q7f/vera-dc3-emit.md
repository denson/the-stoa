status: completed
ticket: stoa--q7f
verdict: pass
design_artifact_verified_against: agents/design/stoa--q7f/design-rev2.md §2 (DC3 mock-emit)
build_verified: branch arc-76/build (worktree arc-76-build); uncommitted DC3 build (2 TOMLs + demo + roster-pin test)

probes_executed:
- probe_id: p1
  description: Condition 1 — ADA built ONLY DC3; no core-service/INV-*/PROVIDER_REGISTRY/frozen-file edits.
  command_or_method: git status + git diff HEAD --stat in worktree; enumerate untracked.
  expected: changed tracked set == {test_dataload.py (M)} + untracked {vertex-gemini.toml, tailscale.toml, demo/}; no edits to spec/port/mock/resolve/dataload/baseline/kinds.
  observed: exactly that set. Other untracked dirs (agents/design, agents/research, agents/verdicts) are gauntlet artifacts, not core code. Frozen files all zero-diff (p4).
  result: pass
  quadrant_classification: easy-easy — git status detects the change-set mechanically; verifying scope is a direct read.
- probe_id: p2
  description: Condition 2 — 3-wall tripwire (W1 no-I/O grep, W2 single concrete Provisioner, W3 emit_spec no-provisioner).
  command_or_method: grep -rnE no-I/O-imports over provision/ (W1); Provisioner.__subclasses__() (W2); inspect.signature(emit_spec) (W3).
  expected: W1 empty (exit 1); W2 == [MockProvisioner]; W3 params == [resolved, builder_slug].
  observed: W1 exit 1 (empty); W2 subclasses == ['MockProvisioner']; W3 params == ['resolved','builder_slug'].
  result: pass
  quadrant_classification: easy-easy — grep + introspection, mechanical.
- probe_id: p3
  description: Condition 3 — assert_value_free passes on BOTH the ProvisioningSpec AND the resulting RunLedger.
  command_or_method: independent python probe; emit_spec on the composed set; assert_value_free(spec); drive populated MockProvisioner; assert_value_free(ledger).
  expected: both pass; no ValueLeakError; ledger.terminal == OK.
  observed: assert_value_free(spec) PASS; ledger.terminal == StepStatus.OK; assert_value_free(RunLedger) PASS.
  result: pass
  quadrant_classification: easy-easy — invoke the guard, observe pass/raise.
- probe_id: p4
  description: Condition 4 — frozen resolve.py (and all frozen files) byte-identical.
  command_or_method: git diff HEAD per frozen file | wc -l for resolve.py/spec.py/port.py/mock.py/dataload.py/baseline.toml/kinds.toml.
  expected: zero diff-lines on every frozen file.
  observed: resolve.py 0, spec.py 0, port.py 0, mock.py 0, dataload.py 0, baseline.toml 0, kinds.toml 0.
  result: pass
  quadrant_classification: easy-easy — diff line count, mechanical.
- probe_id: p5
  description: Condition 5 — emitted ProvisioningSpec == design §2.5 field-for-field (golden equality).
  command_or_method: INDEPENDENT python probe — compose resolved set from loaded catalog+baseline (NOT demo code), call emit_spec, dump every RAW field, compare by eye to §2.5 (did NOT trust the demo hand-typed EXPECTED_SPEC).
  expected: every field == §2.5 (apis sorted; 3 secret_slots all populated=False with exact acquisition values; railway_vars; db_extensions; sa_scope sorted; needs_postgis_base_image=False; budget_boundary_required=True).
  observed: ALL fields match §2.5 exactly — apis=(aiplatform,gemini-embedding,gemini-search); slots GCP_SA_KEY_B64/gcp_secret/mint-via-gcp-console, POSTGRES_PASSWORD/gcp_secret/generate-locally, TS_AUTHKEY/thirdparty_rest_key/mint-via-thirdparty, all populated=False; railway_vars=(DATABASE_URL,); db_extensions=(pgvector,); 6 sa_scope tuples sorted; needs_postgis_base_image=False; budget_boundary_required=True.
  result: pass
  quadrant_classification: easy-easy — re-derive + field compare against a fully-specified golden.
- probe_id: p6
  description: Condition 6 — both TOMLs validate clean under BOTH load_catalog AND load_detection_hints.
  command_or_method: independent python probe loading both records via load_catalog() and load_detection_hints().
  expected: vertex-gemini + tailscale present in both loaders; no DataIntegrityError.
  observed: both present under load_catalog AND load_detection_hints; clean load.
  result: pass
  quadrant_classification: easy-easy — call both loaders, assert membership.
- probe_id: p7
  description: Condition 7 — FULL builder_deploy_core suite green; NOT made green by a weakened test.
  command_or_method: python -m pytest -q (full suite); + git diff HEAD on test_dataload.py scrutinized for weakening.
  expected: 105 passed / 0 failed; the only test edit is a roster-pin set-equality growth (4->6); no unrelated assertion relaxed/deleted.
  observed: 105 passed / 0 failed. test_dataload.py diff = TWO set-equality assertions grew {4 services} -> {6 services} (added vertex-gemini+tailscale). ALL other assertions UNCHANGED — inner surface-key shape, per-token isinstance, spot-check tokens, and the load_catalog no-leak assertion (record.keys()=={entries,gcp_api,category} + detection_hints not in record). Set-equality is STRICTER than a count, so the update is mandatory, not a weakening.
  result: pass
  quadrant_classification: easy-easy — run suite + read the diff.
- probe_id: p8
  description: Condition 8 — ZERO real infra/creds/money; emit-only/mock.
  command_or_method: grep demo + TOMLs for network/cred/CLI calls (requests/httpx/socket/subprocess/gcloud/railway/http(s)/api_key/token=); enumerate demo imports; confirm TOMLs hold slot NAMES only.
  expected: no real network/credential/CLI call; demo imports pure/in-package only; TOMLs hold NAMES, no values.
  observed: no I/O libs (only sys, pathlib.Path, builder_deploy_core.*); all grep hits are NAME literals (DATABASE_URL; tailscale/railway_var record/kind names); TOMLs carry GCP_SA_KEY_B64/TS_AUTHKEY as slot NAMES + config_keys identifiers, zero credential values.
  result: pass
  quadrant_classification: easy-easy — grep + import enumeration.
- probe_id: p9-D1
  description: Highest-risk D1 — resolve() category="none" finding; real finding vs papered-over step.
  command_or_method: read resolve.py:69-80 (category lookup); independent python probe — call resolve() with category=none (assert raises); list library categories; call resolve() on every REAL category and check no new-catalog leak; confirm directly-composed set == §2.4 and emit == §2.5.
  expected: resolve() raises ResolutionError(unknown category: none) because none not in library; real categories resolve unperturbed by the new records; directly-composed set == §2.4; emit on it == §2.5.
  observed: library == {document-consuming, document/data, geospatial}; none NOT in library; resolve(category=none) raised ResolutionError(unknown category: none) — structurally forced, no none-path (resolve.py:78-80). All 3 real categories resolve with new-catalog-leak=False. Directly-composed set == §2.4 (8 entries sorted); emit == §2.5 (p5). DISPOSITION: D1 is a REAL finding for the Grand at the provision gate — the cookie-cutter resolve() requires a known category; a category-less core stand-up composes baseline∪delta directly. ADA did NOT paper over a step (the resolve() path is genuinely unavailable) and documented the deviation in the demo header + hand-back.
  result: pass
  quadrant_classification: easy-easy — invoke resolve() with the failing input, observe the raise.
- probe_id: p10-testdiff
  description: Highest-risk — test_dataload.py modification; benign roster-pin vs regression-masking edit.
  command_or_method: git diff HEAD -- tests/test_dataload.py + full read of both modified functions.
  expected: ONLY the two catalog records added to set-equality roster pins; no other assertion relaxed/deleted/weakened.
  observed: ONLY two set-equality assertions grew 4->6 (admit vertex-gemini+tailscale). Inner shape assertion, per-token isinstance, spot-check tokens, and the load_catalog no-detection_hints-leak assertion are ALL byte-unchanged. Verdict: BENIGN forced roster-pin (set-equality is stricter than a count, so additive records MUST update it). NOT a masking edit.
  result: pass
  quadrant_classification: easy-easy — read the diff against the two functions.

threat_coverage: []
# §35.5 carve-out: DC3 is emit-only / value-free / mock — no runtime attack path (ARGUS CONFIRMED; design §2.7).
# The M1-M6 service mitigations + P-M* probes are DESIGN-TIME specs for the FUTURE gated core build, explicitly
# out of ADA's DC3 scope. No threat-ratified mitigation is in this build's scope; empty list valid per the carve-out.

methodology_concerns: Did NOT trust the demo self-assertions or its hand-typed EXPECTED_SPEC — independently re-composed the resolved set and re-derived emit_spec output RAW, comparing to design §2.5 directly (a demo that mistyped EXPECTED_SPEC to match a buggy emit would have passed its own asserts; my independent re-derivation closes that). D1 is a real expressiveness finding (cookie-cutter resolve() cannot express a category-less manifest) that the Grand should see when gating the REAL provision step — already surfaced by ADA/POLYBIUS up-chain; restated here so it is not lost. No coverage gaps in the 8 conditions.

falsifying_evidence_summary:

verification_artifacts_path: agents/verdicts/stoa--q7f/vera-dc3-emit.md (probe outputs inlined above; all probes re-run live against the worktree build)

summary: The DC3 mock-emit build was exercised by independently re-running every ADA-reported result against the arc-76-build worktree — NOT trusting the hand-back. All 8 FM hard conditions PASS and all three highest-risk falsification items resolve in the build favor. Load-bearing checks: (5) golden equality — I independently re-composed the resolved set and re-derived emit_spec RAW (bypassing the demo own EXPECTED_SPEC), and every field matches design §2.5 exactly; (7+test-diff) the test_dataload.py modification is a clean forced roster-pin (two set-equality assertions grew 4->6 to admit the additive records; every other assertion, including the critical load_catalog no-leak shape assertion, is byte-unchanged), so the green 105/0 suite was NOT made green by weakening a test; (D1) resolve() genuinely raises ResolutionError(unknown category: none) because none is not a library category — the bypass is structurally forced, ADA did not paper over a step, and D1 is a real finding the Grand needs at the provision gate (a category-less core stand-up composes baseline union delta directly). Frozen surface intact (resolve.py + all frozen files zero-diff), 3-wall tripwire holds, value-free on both spec and RunLedger, both TOMLs validate under both loaders, and the build touches zero real infra/creds/network/money. VERDICT: PASS.
