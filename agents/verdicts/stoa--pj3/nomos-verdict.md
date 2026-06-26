---
author: Denson Smith
ticket: stoa--pj3 (u--9s2 Phase-2 increment 2.1)
seat: CAPTAIN_NOMOS_the_stoa (GROUND-TRUTH AUDITOR) — gauntlet stage 6/6
as_of: 2026-06-26
---

# NOMOS ground-truth audit — arc-75/build (stoa--pj3, u--9s2 Phase-2 inc 2.1)

verdict: CONFORMANT
ticket: stoa--pj3
checked_output: arc-75/build deliverable + provenance — three commits on arc-75/build (off main 9ddeb9e):
  8467d10 (build: agents/builder-deploy-core/ — promoted resolution+discovery CORE + TOML DATA + locked suite),
  34a6c9a (design rev1+rev2: agents/design/stoa--pj3/), cd456bf (ARGUS+VERA+CATO verdicts: agents/verdicts/stoa--pj3/).
  Audited against: directive (beadwork:attachments/stoa--pj3/u9s2-phase2-inc1-directive.md, DoD section 5 items 1-9),
  Phase-1 design (agents/design/stoa--jw5/design-formal.md), build spec (design-rev2.md),
  proven prototypes (stoa--jw5/{resolution-check,discovery-check}/), and the bw thread ratifications.

divergences: NONE.

## DoD 1-9 confirmation (independently spot-checked, NOT taken on VERA/CATO word)

DoD 1 RESOLVER — CONFORMANT. Live-ran shipped builder_deploy_core.resolution.resolve against committed TOML DATA +
  fixture manifests: prospector=8, scienceclaw=6, labstat_bls=7 (8/6/7 reproduced). Section 8.4: omitting each of
  the 5 BASELINE entries raised BaselineOmitError — guard fired 5/5.

DoD 2 GENERATOR — CONFORMANT. python -m builder_deploy_core.discovery: each builder generate-then-resolve to 8/6/7,
  manifest-equivalent to the section 8 fixtures; alias-aware (document/data is DATA file document-data.toml;
  labstat_bls G2-selects document-consuming -> resolves to 7, section 8.3-equivalent).

DoD 3 VALIDATOR — CONFORMANT. V1-V5 PASS on every generated manifest; NEG-1 (undeclared shadow -> V5 fail-closed)
  and NEG-2 (uncataloged declared -> UncatalogedServiceError + V1 fail) both held (live entrypoint).

DoD 4 RESOLVED-SET PROPERTIES — CONFORMANT. derive_sa_scope and check_runtime_completeness byte-identical to
  prototype (extract+diff). Live: SCOPE_BEARING_KINDS = {gcp_api,gcp_secret,thirdparty_rest_key}; KEY_BEARING_PAIRING
  = google-maps -> MAPS_API_KEY. labstat_bls BLS_OEWS_API_KEY resolves as thirdparty_rest_key, mints ZERO gcp_api.

DoD 5 DATA EXTERNALIZED — CONFORMANT-by-ratification (see Probe 3). baseline / category templates / catalog / kinds
  are real on-disk TOML DATA files read by the resolver/generator as parameters. Logic modules (resolve.py /
  generate.py / validate.py / errors.py) are DATA-LITERAL-FREE; the only in-module literals are dataload.py
  EXPECTED_BASELINE (design-rev2 section 2.4.1 load-validation SSoT, by-design) + discovery __main__ harness
  expected-result assertions (test expectations, not resolution data).

DoD 6 PURITY + section-2-CONSTRAINT — CONFORMANT. AST import surface = stdlib only (__future__/pathlib/sys/tomllib)
  + intra-package; ZERO os/subprocess/socket/requests/urllib/time/getenv. dataload reads only
  Path(__file__).parent.parent/data via tomllib. The two purity-grep hits are comments, not calls. section-2-
  constraint: discovery/validate.py:24 + discovery/__main__.py:18 import the SINGLE resolver; ZERO def resolve under
  discovery; module identity holds (resolution.resolve IS the resolution-package callable). Re-implements nothing.

DoD 7 FULL-SUITE REGRESSION — CONFORMANT. Bespoke locked suite ran live 40/40 PASS. VERA P9 full the-stoa suite GREEN
  (gen-data 4/12/8; vitest 41/41; vite build OK); corroborated by diff scope: arc-75/build touches ONLY agents/
  (ZERO substrate/, ZERO app/) so the core cannot regress the roster/app. agents.ts side-effect was pre-existing
  stoa--fii drift (reverted by PLINY).

DoD 8 AUTHORSHIP — CONFORMANT. Author audit across 92 committed files: 91 author-like lines all Denson Smith, ZERO
  foreign. Commit Author = denson <densonsmith2@gmail.com> (PRINCIPAL) on all three — NOT overridden; build commit
  carries Co-Authored-By CAPTAIN_ADA_the-stoa seat trailer (clean op-disc section 28 provenance).

DoD 9 HOME PROPOSAL SURFACED + RATIFIED — CONFORMANT. Surfaced (DAEDALUS proposes -> ARGUS critiques ->
  Polybius_the_Stoa ratifies), routed UP, RATIFIED 21:32:33Z: HOME-DEFER (build 2.1 in the-stoa under agents/;
  permanent HOME deferred to 2.3, Option B leading; NOT escalated to Grand). Not silently baked.

## Probe 2 — the three permitted logic-edits ONLY (CONFORMANT)

derive_sa_scope + check_runtime_completeness: signatures + bodies BYTE-IDENTICAL to prototype (function-extract +
equality: 594 / 755 chars identical). resolve / resolve_with_lint bodies byte-identical MODULO the permitted default
deletion (baseline=BASELINE, library=LIBRARY -> baseline, library). The only other logic changes are exactly the two
ratified-design ones: (a) section 2.1.1 import-time module-global treatment of the section 3.3 kind-tables via an
_UNLOADED fail-closed sentinel (membership/iteration raise DataIntegrityError — verified live on all 4 ops); (b)
discovery sys.path-hack -> real intra-package import. No other logic-byte change smuggled in.

## Probe 3 RULING — TOML-vs-directive-.yaml = RATIFIED SUPERSESSION (CONFORMANT-by-ratification)

The directive literally names .yaml (baseline.yaml, categories/NAME.yaml in section 3.1/3.2/5.5/17.1); the shipped
DATA is .toml (ZERO .yaml/.yml in the deliverable). This is NOT a divergence. Polybius_the_Stoa RATIFIED the
supersession on stoa--pj3 at 2026-06-26T21:32:33Z: YAML-to-TOML ENDORSED, supersedes the directive literal .yaml;
the supervisor states .yaml was incidental shorthand for externalized DATA that CONFLICTS with its own section 2.3
zero-dependency purity (YAML needs PyYAML, a hidden third-party dep; the stdlib has no YAML parser), and DAEDALUS
choosing TOML via stdlib tomllib resolves the conflict correctly (ARGUS web-verified tomllib stdlib since 3.11;
requires-python >= 3.11 makes zero-dep unconditional; JSON the documented sub-3.11 fallback). Proceed TOML-primary.
Relayed down by the FM at 21:33:35Z with the explicit close-gate instruction to cite this ratification at the NOMOS
step. Per durable ground-truth on the thread, the TOML delta reads as a ratified supersession of the directive
literal, classified CONFORMANT-by-ratification, NOT a divergence.

## Probe 5 — scope fidelity (CONFORMANT)

Directive section 2 OUT-list honored: NO SUGGEST (24-31), NO provisioning choreography S0-S6 / real deploy, NO
scienceclaw acceptance, NO R-1/R-2/R-3, ZERO infra. Confirmed by AST (no gcloud/Railway/credentials/network/clock/
subprocess/os.environ) + diff scope (only agents/). Nothing smuggled beyond {directive} union {Phase-1 design}.

## Probe 7/9 — commit-SHA + ticket-state + gauntlet completeness (CONFORMANT)

Three claimed commits exist on arc-75/build with the claimed contents (8467d10 / 34a6c9a / cd456bf), merge-base =
main 9ddeb9e. All six gauntlet stages ran (DAEDALUS -> ARGUS -> ADA -> VERA -> CATO -> NOMOS); the three pre-NOMOS
verdicts are committed (cd456bf) AND attached to bw (attachments/stoa--pj3/verdicts/{argus,vera,cato}-verdict.md).
PLINY no-re-ARGUS-of-rev2 scope decision recorded on the thread (21:37:32Z, justified per-engagement section 7.8
call). Follow-up stoa--jd5 (CATO c2/f1, pyproject parent-relative package-data glob) filed with a concrete plan,
correctly blocked on the deferred 2.3 HOME — a legitimate fix-now-deferral, not a handwave.

## Probe 8 — cross-reference integrity (CONFORMANT)

Design/directive section refs resolve; prototype dirs exist on main with the cited files; no dangling reference.

ground_truth_consulted: bw show stoa--pj3 (full thread incl. the 21:32:33Z ratification + 21:33:35Z relay); bw show
  stoa--jd5; git show beadwork:attachments/stoa--pj3/u9s2-phase2-inc1-directive.md; git -C WORKTREE log/show/ls-tree/
  diff/grep main..HEAD on 8467d10/34a6c9a/cd456bf; git show main:agents/design/stoa--jw5/resolution-check/resolve.py
  (prototype frozen-fn diff); live execution in the worktree of builder_deploy_core.resolution + .discovery +
  dataload corrupt-tree rejection (6/6 DataIntegrityError) + the _Unloaded sentinel (4/4 ops raise) + pytest (40/40);
  AST import-surface scan; author-field scan over 92 committed files; git ls-tree beadwork attachments/stoa--pj3/.

summary: Full ground-truth audit of the arc-75/build deliverable for u--9s2 Phase-2 increment 2.1. All nine DoD items
  are satisfied by the SHIPPED code, independently spot-checked rather than accepted on the VERA/CATO verdicts:
  resolve reproduces 8/6/7 live, the section 8.4 baseline-omit guard fires for all 5 entries, dataload rejects all 6
  corrupt DATA trees with DataIntegrityError, the section 2.1.1 fail-closed sentinel raises on every pre-load
  kind-table read, the purity grep is clean (AST-confirmed stdlib-only imports), the logic modules are
  data-literal-free, authorship is Denson Smith across all 92 files with zero foreign, and the diff touches only
  agents/ (zero substrate/app, so the full suite cannot regress). The two frozen functions are byte-identical to the
  prototype and the only logic-byte changes are exactly the three ratified-design edits. The load-bearing delta —
  shipped TOML DATA vs the directive literal .yaml — is a ratified supersession (Polybius_the_Stoa 21:32:33Z,
  YAML-to-TOML ENDORSED-supersedes on section 2.3 zero-dependency purity grounds), classified
  CONFORMANT-by-ratification, NOT a divergence. The HOME decision was surfaced and ratified-deferred to 2.3, not
  silently baked. The gauntlet ran all six stages with all prior verdicts committed and attached. No divergence on
  any probe. The deliverable may propagate to the close-gate.

gap_or_blocker: none.
