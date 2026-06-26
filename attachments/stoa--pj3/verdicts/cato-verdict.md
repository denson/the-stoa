---
author: Denson Smith
ticket: stoa--pj3 (u--9s2 Phase-2 increment 2.1)
seat: CAPTAIN_CATO_the_stoa (REVIEWER)
gauntlet-stage: 5/6
reviews-commit: 8467d10 (arc-75/build)
design-compared-against: agents/design/stoa--pj3/design-rev2.md
meta-verifies: agents/verdicts/stoa--pj3/vera-verdict.md
as_of: 2026-06-26
---

# CATO cold-read verdict — stoa--pj3 (promote resolution + discovery prototypes into builder-deploy-core)

status: completed
verdict: PASS-WITH-NITS
diff_reviewed: commit 8467d10 on arc-75/build (87 files; agents/builder-deploy-core/)
design_artifact_compared_against: agents/design/stoa--pj3/design-rev2.md

## Overall posture

PASS-WITH-NITS. The deliverable is a faithful, idiomatic, internally-consistent promotion of the two VERIFIED Phase-1 prototypes. The frozen logic is genuinely frozen (independently byte-diffed), the two new design contracts (s2.1.1 import-time module-global population; s2.4.1 fail-closed DATA-load validation) are implemented EXACTLY as specified, the purity boundary holds, the s2-constraint holds, authorship is clean over the committed tree, and both runnable entrypoints reproduce the prototype RESULTS. There is NO blocking concern. Two non-blocking nits (one a packaging-glob for the DEFERRED HOME, one a benign idiom the design itself mandates) and one meta-verification CORRECTION of VERA's hygiene note. Cleared for the final gate.

## Findings

### c1 — VERA's committed .pytest_cache/__pycache__ hygiene note is a FALSE ALARM (meta-verification of VERA)
- category: coverage
- description: VERA's verdict carries a non-blocking note that .pytest_cache/ + __pycache__/*.pyc were committed under the package despite a .gitignore. Commit 8467d10 commits ZERO cache artifacts.
- evidence: git diff-tree on 8467d10 = 87 files, none matching pycache/pyc/pytest_cache; git ls-files grep cache = empty; the committed agents/builder-deploy-core/.gitignore correctly excludes __pycache__/ *.pyc .pytest_cache/. The cache dirs exist ONLY as untracked working-tree artifacts from running pytest (git-ignored, not staged, not committed).
- severity: minor
- quadrant_classification: easy-easy
- NOTE: there is NO hygiene action item for PLINY's planned cleanup commit — the deliverable is already clean. POLYBIUS (FM) independently reached the same conclusion. VERA's wording over-stated a non-issue; VERA's PASS + probe work otherwise stand.

### c2 — pyproject.toml package-data glob uses a parent-relative path (../data/**/*.toml)
- category: craft
- description: data/ is a SIBLING of builder_deploy_core/, not inside it, so the package-data glob escapes the package dir with dot-dot. setuptools package-data is resolved relative to the package directory and dot-dot escapes are generally NOT honored, so a future pip install/build would likely NOT bundle the DATA tree. The runtime data-root resolution (Path(__file__).parent.parent/data) is correct and in-tree execution works regardless.
- evidence: agents/builder-deploy-core/pyproject.toml:31 (builder_deploy_core = [../data/**/*.toml]); contrast dataload.py:25 (_DATA_ROOT = Path(__file__).resolve().parent.parent / data) which works in-tree.
- severity: minor (non-blocking)
- quadrant_classification: easy-easy
- WHY NON-BLOCKING: design s2.5 requires only that python -m builder_deploy_core.resolution/.discovery run in-tree (independently confirmed PASS) + the locked suite passes; the permanent HOME and pip-packaging are EXPLICITLY DEFERRED (s4 / WP-2). This is a packaging concern for the eventual HOME-relocation arc, not a 2.1 defect. Surface to the packaging arc, do not block 2.1.

### c3 — resolution/__init__.py re-exports resolve shadowing the resolve submodule (CRAFT CALL on ADA flag2)
- category: craft
- description: from builder_deploy_core.resolution.resolve import resolve in resolution/__init__.py rebinds the package attribute resolution.resolve from the SUBMODULE object to the FUNCTION object. This is the standard documented Python behavior for a from-X-import-name in a package __init__.
- evidence: resolution/__init__.py:27-32; probed live — builder_deploy_core.resolution.resolve resolves to the FUNCTION resolve (not the submodule); all 40 tests + both entrypoints pass; validate.py:24 imports via the fully-qualified from ...resolution.resolve import resolve (the submodule path), which is UNAFFECTED by the package-level shadow.
- severity: minor (non-blocking observation, NOT a recommended change)
- quadrant_classification: easy-easy
- CATO CRAFT CALL: LEAVE AS-IS. The shadowing is a benign, well-understood Python idiom; it causes zero functional breakage (independently confirmed) and the design (s2.1 layout: exports resolve, generate, validate, the error classes) explicitly mandates exporting resolve. Removing/renaming the re-export would DEVIATE from rev2's exports-resolve instruction for no functional benefit. The s2-constraint probe and all callers use the fully-qualified submodule import, so the shadow never bites. I do NOT recommend the change.

## Dimensions checked (all CLEAN — for the record)

- INTENT-FIT: the diff promotes exactly the two prototypes into a packaged core; addresses the design's restated problem (structure/packaging/DATA-externalization/HOME), no slide into adjacent work.
- SCOPE: directive OUT-list HONORED. No SUGGEST (s24-31), no choreography S0-S6, no scienceclaw acceptance test, no R-1/R-2/R-3, no infra (gcloud/Railway/Tailscale/subprocess/credentials/network/clock). All OUT-list grep hits are DATA kind-names (railway_var), comment prose (S0/provisioning), or the in-scope scienceclaw FIXTURE (one of the 3 builder fixtures, not the 2.4 acceptance test).
- FROZEN-FUNCTION FIDELITY: derive_sa_scope + check_runtime_completeness are BYTE-IDENTICAL between the Phase-1 prototype (resolution-check/resolve.py L168/L183) and the build (independently extracted + diffed; zero delta). resolve/resolve_with_lint bodies match minus the deleted baseline/library literal defaults (the permitted s2.1 edit). The three permitted edits are present and EXACTLY those three; no other logic-byte change.
- s2.1.1 CONTRACT (r1): _UNLOADED sentinel present (resolve.py:29-55) whose __contains__/__iter__/__len__/items() all raise DataIntegrityError; single import-time population site in resolution/__init__.py:20-24; signatures of the two frozen functions byte-unchanged. Implemented exactly.
- s2.4.1 CONTRACT (r2): all five invariant bodies implemented (dataload.py) — baseline set-equality vs the in-dataload named EXPECTED_BASELINE SSoT (dataload.py:33-39, 105-113); kinds enum/scope-bearing-subset/well-typed-pairing; categories well-typedness; catalog required-keys + well-typedness; cross-body dangling-reference (both catalog-to-category and pairing-name-to-any-body). Fail-closed (raise, no partial load) confirmed in code + by P11.
- PURITY (s2.3/P7): the only open(/tomllib hits in the core are in dataload.py scoped to data/ (the lone P7 grep hit elsewhere is a COMMENT in dataload describing the boundary). Zero os.environ/socket/requests/urllib/subprocess/time.time/datetime.now/random anywhere in core source.
- s2-CONSTRAINT (P8): validate.py imports the single resolver; resolve.__module__ == builder_deploy_core.resolution.resolve (live-probed); ZERO def-resolve under discovery/. Acyclic discovery-to-resolution edge.
- ALIAS-EXCLUSION GROUNDING (ADA flag1): FAITHFUL. The build's _ALIAS_CATEGORIES={document/data} exclusion from the discovery CATEGORIES bundle (dataload.py:59, 297-301) exactly mirrors the Phase-1 prototype: discovery-check/catalog.py CATEGORIES has ONLY geospatial+document-consuming (no alias), while resolution-check/resolve.py LIBRARY carries all three incl. document/data. labstat_bls still G2-selects document-consuming -> resolves to 7. Concur with ADA + VERA: shipped-to-verified-prototype reality, not a divergence.
- AUTHORSHIP (P10): airtight over the COMMITTED tree. git grep for author-like fields on 8467d10 = every match reads Denson Smith; pyproject.toml:20 authors = [{ name = Denson Smith }]; ZERO foreign name. (Working-tree greps surface the word author only inside prose like hand-authored/authoritative + the untracked .pytest_cache, none of which is a foreign author field and none committed.)
- HYGIENE: no dead code, no owner-less TODOs, no debugging artifacts, no stray files IN THE COMMIT. Consistent author/ticket/seat/design-ground-truth header block across all source files. README + pyproject + docstrings idiomatic and internally consistent with the design.

## follow_ups

- f1 (c2): when the permanent HOME is chosen + the core is pip-packaged (the DEFERRED s4 decision / a later additive arc), fix the pyproject package-data layout so the data/ tree is bundled — either move data/ inside the builder_deploy_core/ package or use a MANIFEST.in / [tool.setuptools.package-data] form that does not rely on a dot-dot escape. Out-of-scope for 2.1 (in-tree execution + the locked suite are unaffected); belongs to the packaging arc.

## verifier_coverage_assessment

VERA's coverage is REAL and anti-vacuous; the redundant-checker property held. I independently re-ran the load-bearing probes rather than trusting VERA's PASS: (1) both runnable entrypoints reproduce the prototype 8/6/7 RESULTS out-of-harness; (2) the P11 dataload suite passes (8 cases) AND each corrupt fixture was inspected to contain REAL, distinct corruption — baseline-missing-pgvector genuinely has 4 entries with pgvector present only in comments; baseline-extra has 6; kinds-empty-scope-bearing has scope_bearing empty; category-malformed-entry omits a name; catalog-missing-key google-maps.toml lacks the category key; dangling-reference points at nonexistent-category. The P11 test assertions are non-vacuous (assert BOTH the raise AND that the error message names the breached invariant). (3) P2 baseline-omit guard, P7 purity, P8 s2-constraint module-identity all independently reconfirmed. P9 full-suite GREEN is corroborated by the FM's independent main..arc-75/build diff (zero substrate/ + zero app/ touched). ONE meta-verification CORRECTION (c1): VERA's hygiene note over-stated a non-issue (said cache was committed; it is git-ignored/untracked, not in the commit) — a wording imprecision, not a coverage gap; VERA's probe work and PASS stand. No vacuous or weak probe found. RULING ON VERA: SOUND.

## threat_coverage

N/A — the design self-classifies not-threat-ratified (s2.7, s35.5 carve-out: pure offline environment-free software, no runtime attack path), ARGUS CONFIRMED. No threat-ratified mitigation in scope, so item-11 (threat-coverage cross-check) is a no-op for this arc. The s2.4.1/s8.4/NEG fail-closed probes verify CORRECTNESS invariants, not a threat-defeat (DATA is in-repo + gauntlet-gated at t0, not attacker-supplied).

## summary

A clean, faithful promotion. The build freezes what the directive said to freeze (frozen functions byte-identical, independently verified), implements the two new contracts (s2.1.1 import-time globals + _UNLOADED sentinel; s2.4.1 fail-closed DataIntegrityError with set-equality vs a named SSoT) EXACTLY, holds the purity + s2-constraint boundaries, and ships zero foreign authorship and zero scope creep. The most important item is a meta-verification CORRECTION, not a defect: VERA's lone hygiene note is a false alarm (no cache committed). The two genuine nits are non-blocking — a deferred-HOME packaging glob (c2 -> f1) and a design-mandated benign name-shadow (c3, left as-is per my craft call). VERA's verification ruled SOUND. Overall posture: PASS-WITH-NITS, cleared for the final gate.
