status: completed
ticket: stoa--q7f
verdict: revise
design_artifact_audited: agents/design/stoa--q7f/design-rev3.md (arc-77/build worktree)

audit_block:
  risks:
  - id: r1
    description: Request-time principal resolution has NO explicit fail-closed invariant or probe for the no-resolvable-principal case (an absent App-Capabilities header AND no allowlisted User-Login, or a cap outside LANE_REGISTRY). A build that resolves an unresolved principal to a permissive DEFAULT (e.g. LANE_REGISTRY.get(cap, DEFAULT) or treating an empty App-Capabilities as a benign class) would pass P-M4 as specified yet grant cross-lane or unauthorized access. The design applies fail-loud probes to INV-BIND/DEST/RESP and the INV-LANE STRUCTURAL clauses precisely because it does not trust the implementer to avoid one mistake, but it does NOT extend that discipline to request-time principal resolution.
    evidence: rev3 section 2.1 names ONLY the two happy resolution branches (operator-login to operators; lane cap to lane:name) with no stated else to 403; section 2.4 INV-LANE clauses 1-3 all guard registry/serve CONFIG consistency at STARTUP (unknown-principal scope, serve-caps == LANE_REGISTRY, principal disjointness) - none is a request-time unresolvable-principal to 403 invariant; section 2.5 / 5.2 P-M4(a) exercises a MAPPED cross-lane denial (lane:newswire to generate_grounded = 403) plus the structural loader case, but does NOT exercise the unmapped/absent to permissive-default failure mode.
    load_bearing: true
    quadrant_classification: easy-easy
  - id: r2
    description: The SEAL_AUDIT_SYNTHETIC_ marker is specified as an UNCONDITIONAL allow-list token - any secret-shaped value carrying the prefix passes the seal-audit, with no constraint binding the marker to non-real values. As specified it is a universal bypass: a real or real-shaped secret prefixed with SEAL_AUDIT_SYNTHETIC_ is waved through, re-opening M7 (the exact threat the gate closes). P-M7(a) plants only UNMARKED secrets (correctly refused) and P-M7(b) codifies marked-to-pass as CORRECT behavior, so the marked-real-shaped bypass path is unprobed - the probe cannot catch this failure because it treats marked-to-pass as the expected outcome.
    evidence: rev3 section 3.1 allow-list bullet (marked-synthetic fixtures are the only secret-shaped things that may pass; the marker is the sole discriminator); section 5.2 / 3.1 P-M7(a) plants UNMARKED values, P-M7(b) asserts marked fixtures PASS. Also DAEDALUS section 6 weak-point 2 explicitly hands this to ARGUS.
    load_bearing: true
    quadrant_classification: easy-easy
  - id: r3
    description: Multi-cap resolution is under-specified. Section 2.1 says the core extracts the capability name(s) - plural - and maps to THE lane principal - singular. The rule when an App-Capabilities header carries MULTIPLE mapped caps (union-of-scopes vs first-match vs reject-ambiguous) is not stated. A union rule would grant a two-cap node both lanes access; whether that is an intended two-lane node or an accidental-grant fail-open is unspecified, and this directly determines the cross-lane boundary.
    evidence: rev3 section 2.1 (plural caps mapped to a singular principal); section 2.4 / section 6 weak-point 4 V-ENC-LANE lists the build-time cap-string confirmations but does NOT name the multi-cap header case.
    load_bearing: uncertain
    quadrant_classification: easy-easy
  - id: r4
    description: Cross-lane DATA-tenancy in the SHARED embeddings/store surface is neither addressed nor explicitly scoped out. The reframe makes one core plus one pgvector store serve multiple lanes (science plus the newswire STORE consumer, which is DEFINED as a store consumer). The multi-lane authz closes cross-lane API-EGRESS (which lane may CALL which op) but is silent on cross-lane DATA isolation within the shared store (whether lane:newswire can read lane:science rows). The design should EXPLICITLY scope this out rather than leave it silent.
    evidence: rev3 section 2.3 (embed scoped to both lanes); rev2 section 4 step 4 (the pgvector DB is the shared home for BOTH the KG store AND skill/retrieval embeddings); rev3 section 7 out-of-scope list does not name store-data tenancy.
    load_bearing: uncertain
    domain_blind_spot: This is the store/DB layer, arguably outside the pass-through service this arc builds; surfaced for explicit scoping - does NOT block the pass-through build.
    quadrant_classification: hard-hard

  non_findings:
  - Carry faithfulness (directive C) - CLEARED. INV-DEST / INV-RESP / INV-BIND, the two-phase audit, and M1-M6 / P-M1..P-M6 are all carried into rev3 section 5 with NONE silently weakened. The rev2 scopes generalization from class [operators,builders] to lane principals [operators,lane:science,...] is a TIGHTENING to deny-by-default per lane, not a weakening (the broad builders class becomes specific lanes). Redirect-OFF, chunk_schema streaming, and INV-RESP refuse-to-load-on-no-schema all carried.
  - Probe falsification (directive C) - CLEARED. P-M1(a) structural, P-M3(a) in-process, P-M4(a) structural, and P-M7(a) each assert non-zero exit / refuse-to-serve / build-fail, so they DO falsify a warnings-only / log-and-continue implementation (the one residual is r1, a request-time RESOLUTION clause, not one of these structural clauses).
  - Future-lane ZERO-access-by-default - CLEARED. Section 2.3: a new lane principal is in no existing op scopes until an explicit audited edit; onboarding grants zero access by default.
  - Per-lane cap-NAME choice (section 2.2) - CLEARED. Sound and a genuinely stronger fail-closed boundary than the rejected shared-cap-with-lane-field option, because it keeps which-lanes-are-served at the fail-closed serve invocation rather than a trusted payload field.
  - Honest residual placement (section 2.5) - CLEARED. skill_id = caller-declared attribution (NOT a boundary); the tag to control-plane cap to lane principal IS the trusted boundary; the reframe adds NO new trust assumption beyond rev2 verified per-tag cap resolution applied N times. Correct and honest (the multi-cap nuance is r3).
  - Seal-audit fail-closed-on-ambiguity - CLEARED. A high-entropy unclassifiable match to FAIL is genuinely CLOSED (section 3.1); the residual is the marker bypass (r2), not the ambiguity posture.
  - M7 distinct from M2 - CLEARED. M2 is the runtime response/log channel (INV-RESP allow-list); M7 is the at-rest build-artifact/repo/log channel (seal-audit shape-scan). Distinct surfaces, distinct mitigations, correctly named as separate threats.
  - Workflow-vs-app-code (directive D, section 4) - CLEARED. Application code is the CORRECT call: every security element is a deterministic code leaf with no LLM-fuzzy residual; a workflow raises the reliability of a fuzzy verdict and cannot make a deterministic invariant more exact. No step warrants a workflow; none was manufactured.
  - Authorship - CLEARED. rev3 frontmatter and the carried catalog TOMLs (vertex-gemini, tailscale) name Denson Smith throughout.
  - Scope fence (directive F) - CLEARED. Section 0 / 3.2 / 5.3 step 5 / 7 commit to NO real infra, NO secrets, NO money, nothing merged/pushed; sos--1bk is named as a Phase-2 reference and executed for nothing. PLINY and the FM independently verified the worktree carries only the untracked design doc, 0 commits ahead of base, nothing pushed.

  threat_coverage_assessment: Every threat-ratified mitigation (M1-M7) carries a SPEC-d threat-anchored probe (no fully-mapless mitigation) - P-M1..P-M7 each specify (a) attack-blocked and (b) legit-unaffected. TWO probes are PRESENT-BUT-INCOMPLETE on a named attack sub-path: P-M4 omits the no-resolvable-principal to permissive-default path (r1), and P-M7 omits the marked-real-shaped bypass path (r2). This is design-time probe-SPEC adequacy only (no executed probe exists pre-build); whether an EXECUTED probe genuinely exercises each attack path is VERA/CATO tier-ii at/after build. Threat-ENUMERATION completeness stays unmechanized ARGUS judgment: the design honestly does not claim M1-M7 is complete (cross-provider key confusion, timing/error-class side-channels named as residual), and r4 surfaces one NEW shared-surface the reframe introduces (cross-lane store-data tenancy) currently left silent.

classifications_confirmed (directive E):
  - seal-audit = threat-ratified (mitigates M7): CONFIRMED. It breaks a real key-exfil attack path (a secret VALUE in a build artifact/repo/log); its A3 map row and threat-anchored P-M7 are present (section 5.2). ARGUS confirms the M7 mitigation classification.
  - DC3 mock-emit = NOT threat-ratified: CONFIRMED (carried from rev2 section 2.7; emit-only, value-free, mock, no runtime attack path; op-disc section 35.5 carve-out). The seal-audit GATE now also scanning those TOMLs does NOT change the emit classification - the gate is the threat-ratified part; the emit is not.
  - workflow-vs-app-code call = NOT threat-ratified: CONFIRMED, and the carve-out is CORRECT not self-asserted - the CALL is a build-engine decision with no runtime attack path; its threat-relevant consequence (the seal-audit is deterministic code) is covered under M7.

daedalus_residual_questions_answered:
  - INV-LANE clause 2 fail-closed on a lane un-served-by-omission: YES at STARTUP (serve-caps == LANE_REGISTRY refuses to serve on mismatch), but that is a CONFIG check, NOT the request-time no-principal fail-closed - see r1.
  - P-M4 falsifies an unmapped-cap to permissive-default build: NO as written - see r1. P-M4(a) tests a MAPPED cap denied by scope plus the structural loader case; the unmapped/absent to default path is unprobed.
  - future lane gets ZERO access by default: YES - confirmed sound.
  - honest residual correctly placed: YES - confirmed (r3 multi-cap nuance aside).
  - seal-audit fail-closed genuinely closed AND marker narrow enough not to be a bypass: fail-closed-on-ambiguity YES; marker narrow enough NO - see r2.

summary: design-rev3 faithfully carries the rev2 gated shape (INV-DEST/RESP/BIND, two-phase audit, M1-M6 / P-M1..P-M6 - nothing silently weakened) and folds the three arc-77 canons cleanly; the multi-lane reframe is a coherent, correctly-TIGHTENED generalization of rev2 verified per-tag cap resolution, and the honest residual is correctly placed. The SHAPE is sound and cleared. TWO load-bearing gaps hold it at REVISE, both in the exact class the directive asked ARGUS to push on - the falsification probe catches the happy/mapped path but not the dangerous failure: (r1) request-time principal resolution has no explicit fail-closed invariant/probe for the no-resolvable-principal case, so a build that resolves an unresolved principal to a permissive default would pass P-M4 yet be cross-lane-broken; (r2) the SEAL_AUDIT_SYNTHETIC_ marker is an unconditional allow-list token - a universal bypass that re-opens M7 - and P-M7 codifies marked-to-pass as correct. Both are DAEDALUS OWN section 6 open questions handed to ARGUS. r3 (multi-cap resolution) and r4 (cross-lane store-data tenancy) are uncertain-severity surfaces to name and scope. Overall posture: MINOR-TO-MODERATE revisions - two precise probe/invariant tightenings, NOT a structural redesign; scope fence held.

gap_or_blocker: none (status completed)
