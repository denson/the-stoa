author: Denson Smith
ticket: stoa--jw5 (u--9s2 Phase-1)
seat: CAPTAIN_VERA_the_stoa (VERIFIER) — TARGETED gauntlet stage 4/6

status: completed
ticket: stoa--jw5
verdict: pass
design_artifact_verified_against: agents/design/stoa--jw5/design-formal.md (sections 16-23, KEY-DISCOVERY PROCESS addition)
build_verified: agents/design/stoa--jw5/discovery-check/ (catalog.py, generate.py, validate.py, run.py, RESULTS.md) — untracked tree on main worktree; resolve.py reused from ../resolution-check/

probes_executed:
- probe_id: p1
  description: Independently re-execute discovery-check/run.py (generation G1-G4 -> resolve -> 8/6/7 + manifest-equivalence + V1-V5 + negative probes).
  quadrant_classification: easy-easy — code probe; run harness, assert exit + output.
  command_or_method: python agents/design/stoa--jw5/discovery-check/run.py
  expected: exit 0; prospector 8 / scienceclaw 6 / labstat_bls 7; each generated manifest EQUIVALENT to the section-8 hand-authored; V1-V5 PASS; NEG-1/NEG-2 fail-closed.
  observed: exit 0. 8/6/7 EXACT; all three GENERATED == section-8 hand-authored (equivalent); V1-V5 PASS on all 3; NEG-1 V5 FAIL (shadow bls-oews), NEG-2 generate() raises UncatalogedServiceError + V1 FAIL; section-2-constraint check PASS (resolve module from ../resolution-check).
  result: pass
- probe_id: p2
  description: Independently re-execute the regression resolution-check/run.py (the section-2 constraint — gated Part-1 machinery still holds).
  quadrant_classification: easy-easy — code probe; run harness, assert exit + output.
  command_or_method: python agents/design/stoa--jw5/resolution-check/run.py
  expected: exit 0; 8/6/7 + section-8.4 BaselineOmitError fail-closed + section-3.4 runtime-completeness + section-5.A SA-scope all hold.
  observed: exit 0. 8/6/7 EXACT; section-8.4 raised BaselineOmitError naming (db_extension, pgvector); section-3.4 runtime-completeness held; section-5.A SA-scope subset held. No regression introduced by the addition.
  result: pass
- probe_id: p3
  description: INDEPENDENT hand-derivation of labstat_bls generation (NOT via ADA run.py) — call generate() directly, hand-check vs my own derivation, confirm resolves to 7.
  quadrant_classification: easy-easy — direct call + hand-derived expected value.
  command_or_method: python -c generate([document-parsing, bls-oews], CATALOG, CATEGORIES, BASELINE) + manual G1-G4 derivation.
  expected: manifest == {category: document-consuming, delta:{add:[{thirdparty_rest_key, BLS_OEWS_API_KEY}]}}; resolve len 7.
  observed: generate() output == my hand-derivation EXACTLY (MATCH True); resolve len 7; resolved set contains (thirdparty_rest_key, BLS_OEWS_API_KEY), zero (gcp_api, BLS_OEWS_API_KEY), S1 gcp_api list excludes it.
  result: pass
- probe_id: p4
  description: Confirm resolve.py REUSED UNMODIFIED (the section-2 constraint, executable).
  quadrant_classification: easy-easy — structural: write-call grep + mtime ordering + import-source assertion + sha.
  command_or_method: grep for open/write/edit in discovery-check (none); stat mtimes; sha256sum resolve.py; run.py section-2-constraint check (module file path == ../resolution-check/resolve.py).
  expected: discovery-check performs ZERO writes; resolve.py mtime predates all discovery files; imported resolve resolves to the resolution-check copy.
  observed: discovery-check has ZERO open()/write/edit calls — imports resolve only. resolve.py mtime 1782424623 (15:57) predates generate/catalog/validate/run (1782442882+ = 21:01+). sha256 resolve.py = 3764ca6e...5bca. run.py section-2-check PASS. The resolver is byte-stable and not written by discovery-check.
  result: pass
- probe_id: p5
  description: Confirm document/data -> document-consuming alias is a FAITHFUL byte-identical reproduction (not a real divergence).
  quadrant_classification: easy-easy — bundle entry-set equality.
  command_or_method: compare LIBRARY[document-consuming] vs LIBRARY[document/data] entry-sets; resolve both manifests.
  expected: both bundles == [(gcp_api, document-parsing)]; generated (document-consuming) and section-8.3 hand (document/data) resolve identically to the same 7-set.
  observed: document-consuming bundle == document/data bundle == [(gcp_api, document-parsing)] (BYTE-IDENTICAL True); generated manifest EQUIVALENT to section-8.3 hand-authored. Faithful alias, not a divergence.
  result: pass
- probe_id: p6
  description: THREAT attack-path — V2 anti-under-provision: DRIVE a manifest that DROPS a called service key and confirm V2 catches it; confirm correct manifest passes V2.
  quadrant_classification: easy-easy — drive broken-vs-correct manifest through V2.
  command_or_method: validate() a hand-broken {document-consuming, delta:{}} for declared [document-parsing, bls-oews] (BLS key dropped); then validate() the correctly-generated manifest.
  expected: V2 FAIL on the dropped-key manifest (called-but-unresolved BLS_OEWS_API_KEY); V2 PASS on the correct manifest.
  observed: (a) ATTACK BLOCKED — V2 FAIL "called-but-unresolved: [(thirdparty_rest_key, BLS_OEWS_API_KEY)]". (b) LEGIT NOT BROKEN — V2 PASS on the correct generated manifest (resolved superset-of called). Both halves hold.
  result: pass
- probe_id: p7
  description: THREAT attack-path — V5 drift fail-closed: an imported-SDK service NOT in the services declaration -> V5 fail-closed.
  quadrant_classification: easy-easy — drive undeclared-but-scanned service through V5.
  command_or_method: validate() prospector manifest with scan_detected=[google-maps, spatial-db, bls-oews] but declared=[google-maps, spatial-db].
  expected: V5 FAIL naming the shadow bls-oews (does not silently under-provision).
  observed: ATTACK BLOCKED — V5 FAIL "shadow service(s) detected but not declared: [bls-oews]". Fail-closed confirmed.
  result: pass

threat_coverage:
- mitigation: M3-lineage (DISCOVERY-COMPLETENESS / anti-under-provisioning spine, section 20.2)
  threat: T-under-provision (a required service CALLED-but-its-key-missing -> runtime 401/500; the M3-lineage under-provisioning the addition prevents)
  defeats_via_probe: p6
  probe_evidence: agents/design/stoa--jw5/discovery-check/run.py V2 rows + the independent driven probe (p6 observed) — V2 FAIL on dropped-key manifest "called-but-unresolved: [(thirdparty_rest_key, BLS_OEWS_API_KEY)]"; V2 PASS on correct manifest.
  attack_path_exercised: Drove a manifest that DROPPED the called bls-oews key (the under-provision attack). (a) V2 BLOCKS it (called-but-unresolved BLS_OEWS_API_KEY); (b) legit correct manifest is NOT rejected (V2 PASS resolved superset-of called). Both (a)/(b) observed.
- mitigation: M3-lineage (DRIFT fail-closed, V5 scan pillar section 18/20)
  threat: T-drift (an imported-SDK service used but UNDECLARED -> silent under-provision)
  defeats_via_probe: p7
  probe_evidence: p7 observed + NEG-1 in run.py — V5 FAIL "shadow service(s) detected but not declared: [bls-oews]".
  attack_path_exercised: Drove an imported-but-undeclared bls-oews (scan_detected superset-of declared). (a) V5 BLOCKS it fail-closed (shadow service named); (b) the no-drift positives all V5-PASS. Both halves observed.

methodology_concerns: |
  No concerns of consequence. Three notes (all NON-blocking, none changes the verdict):
  (1) resolve.py-unmodified is verified STRUCTURALLY (zero write-calls in discovery-check + mtime ordering + import-source assertion + sha), NOT by a committed-baseline diff, because the entire agents/design/stoa--jw5/ tree is untracked on the main worktree (?? per git status) — there is no committed Part-1 resolve.py to diff against. The structural proof is conclusive for THIS arc (discovery-check cannot have edited a file it never opens), but the close-gate should note the tree is uncommitted.
  (2) DWP-3 residual is HONESTLY scoped: V5 catches import-detectable drift only; a service reached purely via raw runtime-config with NO import signal is invisible to declare+scan and is closed only by the Phase-2 runtime observer (section 18.1 pillar 3). p7 confirms V5 detects the import-bearing case; the design does NOT over-claim discovery completeness. No Phase-1 probe owed for the runtime-config case (Phase-2 residual) — confirmed correctly classified.
  (3) R-3 catalog-integrity (section 35.5 named residual): the catalog is a fleet-wide T1 SoT; a bad record propagates to every declaring builder (wider blast radius than R-2). Confirmed classified in section 12.B.1 / 23.4 as a Phase-2-hardened residual resting on Phase-1 catalog-authoring discipline. No Phase-1 probe owed.

falsifying_evidence_summary: ""

verification_artifacts_path: agents/design/stoa--jw5/ (discovery-check/run.py re-executed; resolution-check/run.py re-executed; independent hand-derivation + V2/V5 attack-path probes run inline via python -c against the unchanged resolver). No new artifact files written (independence — VERA does not modify the build).

summary: |
  INDEPENDENTLY verified the KEY-DISCOVERY PROCESS addition (sections 16-23) by re-executing both
  harnesses first-hand (not trusting ADA) AND writing my own out-of-harness probes. Manifest GENERATION
  (G1-G4) over the seed catalog produces, for the 3 declared builders, manifests the UNCHANGED resolver
  resolves to 8/6/7 EXACT, each EQUIVALENT to the section-8 hand-authored fixtures. I hand-derived
  labstat_bls generation independently (G1 union -> G2 document-consuming -> G3 +BLS_OEWS_API_KEY delta
  -> 7) and generate() matched my derivation byte-for-byte. resolve.py is REUSED UNMODIFIED — proven
  structurally (discovery-check has ZERO write/open calls; resolve.py mtime predates all discovery
  files; the imported resolve resolves to ../resolution-check/resolve.py; sha 3764ca6e). The
  document/data->document-consuming alias is byte-identical (both = [(gcp_api, document-parsing)]), a
  faithful reproduction not a divergence. V1-V5 hold; negative probes fail-closed (V5 drift, V1/generate
  uncataloged). The load-bearing THREAT probe drove the actual attack-path, not a happy-path proxy: I
  built a manifest that DROPPED the called bls-oews key and confirmed V2 BLOCKS it while the correct
  manifest passes (anti-under-provision); and drove an undeclared-but-imported service confirming V5
  fail-closed. Regression (section-2 constraint) confirmed: resolution-check/run.py exit 0 (8/6/7 +
  BaselineOmitError + section-3.4 + section-5.A) — the addition introduced NO regression. DWP-3
  (runtime-config no-import-signal -> Phase-2 observer) and R-3 (catalog-integrity section-35.5
  residual) are honestly classified and not over-claimed; no Phase-1 probe owed for either. VERDICT: pass.

[from: CAPTAIN_VERA_the_stoa (subagent) | caller-sid 8040be7f-a1ba-4917-b953-75947d464abf]
