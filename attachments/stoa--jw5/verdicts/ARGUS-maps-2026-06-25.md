status: completed
ticket: stoa--jw5 (u--9s2 Phase-1)
verdict: revise
design_artifact_audited: agents/design/stoa--jw5/design-formal.md
scope: TIGHT A2-gate pass (op-disc 35.4 maps-confirm + ONE 35.5 enumeration ruling). NOT a full re-audit; stage-2 cold-audit already discharged all WPs except WP-6 (now fixed via 2.4/2.6 BaselineOmitError + 8.4 fixture).

audit_block:
  maps_confirm:
  - id: M1
    classification: CONFIRMED (correct) WITH a mandated honesty-qualification (see r1)
    attack_path: compromised key / over-scoped SA in builder A reads/spends/exfiltrates builder B resources
    how_defeated_breaks_path: YES on INITIAL provision. 5.A derived union-scope (scope-bearing resolved entries ONLY) + bijective 1-SA-to-1-builder + per-secret secretAccessor (never project-wide) + S3 injects only this builder key + Branch-A project blast-radius genuinely break the cross-builder lateral-movement path, GIVEN an honest manifest. A real defeat, not a happy-path proxy.
    caveat: subtractive-direction gap (r1) -- re-run after a manifest removal leaves a stale grant. M1 how-defeated as written overclaims; must be qualified.
  - id: M2
    classification: CONFIRMED (correct)
    attack_path: secret VALUE lands in agent transcript / argv / disk -> exfiltratable from agent context
    how_defeated_breaks_path: YES. 4 emit-then-apply (value-free spec naming SLOTS only) + S2c human-population GATE (BLOCK not improvised value) + STDIN/keyring/SecretManager only (never argv/logs) + S3 this-builder-key-only. This IS the op-disc 20 CI-mediated correct shape (agents author spec, CI/human applies via short-lived creds, no value in agent-reachable scope). Breaks the path, not a proxy.
  - id: M3
    classification: CONFIRMED (correct)
    attack_path: key-bearing API surface (Maps) resolves enabled-but-keyless -> deploys then 401s at call time
    how_defeated_breaks_path: YES. 3.4 runtime-completeness invariant (every app-called key-bearing surface resolves to BOTH enablement AND paired gcp_secret) + S6 verifies the template-declared (gcp_api,gcp_secret) in-band pairing is resolved + populated. Per-API key-bearing table web-confirmed at stage 2 (Maps = only minted-key API; Vertex-family + Document AI = SA-role/ADC). Breaks the path.
  - id: M4
    classification: CONFIRMED (correct)
    attack_path: manifest delta.omit drops a baseline necessity (pgvector) -> silent drop -> builder embeds with no vector store -> runtime 500s (the lone former fail-OPEN path)
    how_defeated_breaks_path: YES. 2.4 BaselineOmitError HARD fail-closed, evaluated at step 0 BEFORE the omit subtraction (pseudocode L155-159: illegal = omit_set AND baseline_set; if illegal raise). 2.6 non-omittable set is DERIVED from the baseline record (not a per-entry allowlist) so it fires for ALL 5 baseline entries and generalizes to every future one. 8.4 negative fixture pins the regression (MUST raise, named, fail-closed, before any partial set). Breaks the path; confirmed fires for all 5, not just pgvector.
  - id: M6
    classification: CONFIRMED (correct)
    attack_path: unauthorized party reaches a builder mesh trigger / curated data (no-auth, loopback-WhoIs spoof, or Funnel exposure)
    how_defeated_breaks_path: YES. 7/S5 T1 scaffold: 0600 AF_UNIX socket + tailscale serve header-trust identity (Tailscale-User-Login, NEVER WhoIs-on-loopback) + deny-by-default + per-builder OPERATORS/group:operators allowlist + Funnel OFF. Breaks the path.
  - id: M5
    classification: CONFIRMED honestly bounded as op-disc 35.5 NAMED RESIDUAL (NOT overclaimed)
    finding: 12.B records M5 as best-achievable, explicitly NOT a hard defeat; 5.B carries the honest (a)-(d) menu with VERA-verbatim citations; no GA hard-dollar cap exists at per-SA OR per-project granularity (platform limitation, STRABO-cited/VERA-confirmed). Correct residual shape. NOT overclaimed anywhere I read.
    section_36_corroboration: FM idx62 binding CONFIRMED -- 36 does NOT fire on M5. 36 fires only for a named threat with a probe-bound-not-executed (T-a) or no-probe-specified (T-b) COVERAGE gap. M5 is residual-by-platform-limitation: the cap does not exist anywhere to probe, so there is no un-probed coverage gap and no remediation arc/spawn-gate is owed. M5 rides UP with the held-fork premise-correction the Grand already owns.

  not_threat_ratified_confirm:
    ruling: CONFIRMED correct for all six 12.C entries -- none hides a security-relevant change that SHOULD carry an M-n.
    detail: typed-entry taxonomy (enabling structure) / resolution-rule add-wins+identity+purity (correctness machinery; M1+M4 RIDE on its purity but the rule itself is not a control) / access-layer SHAPE-CONTENT boundary (security is M6; boundary is structural) / DECIDE-A pgvector-to-baseline (folds into M4) / category graduation governance (process) / stoa--reg note (later-merge, no runtime path) -- each correctly classified not-threat-ratified (no runtime attack path). No carve-out is WRONG; none has a hidden runtime attack path.

  risks:
  - id: r1
    description: M1 how-defeated + the 5.A scope-is-a-pure-function-of-the-manifest invariant OVERCLAIM in the SUBTRACTIVE direction. S0-S6 is create-or-get (additive); S6 asserts each RESOLVED entry is PRESENT but does NOT assert live-state == resolved-set, so a re-provision after a manifest DROPS an entry leaves a stale SA secretAccessor/grant standing -- a residual over-grant that weakens M1 (isolation) on re-run. The invariant holds on initial provision; it breaks subtractively on re-run.
    evidence: design-formal.md 4 S6 (L348/L350 converges-and-cannot-widen-scope asserts the manifest-driven resolve, NOT live-cloud-state vs resolved-set) + 5.A (L362 SA scope = mechanical union of scope-bearing resolved entries; L366 lists manifest-edit + resolver-edit as the only widening paths but is SILENT on revoke-on-removal) + 12.A M1 how-defeated cell (L686) + HAMILTON idx63.
    load_bearing: true
    quadrant_classification: easy-easy (concrete: a removed entry whose SA grant persists; a downstream reconcile probe is trivial once specified)
  - id: r2
    description: Manifest INTEGRITY/AUTHORSHIP is a trust boundary that carries NO classification anywhere in 12 (neither M-n nor an explicit not-threat-ratified-with-reason). M1 defeats cross-builder leakage GIVEN an honest manifest, but whoever authors/edits a builder manifest controls its resolved scope (a tampered manifest can delta.add a broader scope or another builder catalog key) -- authz-relevant (the manifest DRIVES resolved scope) and security-relevant, so per op-disc 35.1 it must carry a classification, not be left unclassified.
    evidence: design-formal.md 12 (no entry for manifest integrity in 12.A/12.B/12.C) + 5.A L365-367 (the manifest is the authz input but its integrity is unstated) + CHIRON manifest-trust-boundary candidate + FM 35.1 must-carry-a-classification binding.
    load_bearing: true
    quadrant_classification: hard-easy (CHIRON/trust-boundary lens surfaced it; once named, classifying + naming as a 35.5 residual is cheap)

  enumeration_ruling_prune_on_removal:
    ruling: PHASE-2 builder-lifecycle follow-up (accepted Phase-1 simplification), NOT a Phase-1 M1 enumeration item -- CONDITIONAL on the M1 honesty-qualification (r1) being folded.
    reasoning: Phase-1 deliverable is INITIAL-PROVISION correctness -- the design provisions nothing and every worked example (8.1-8.4) is an initial resolution. On initial provision M1 holds completely (the SA is created with exactly the union-derived scope; no stale state exists yet). The stale-grant gap is a RE-PROVISION-AFTER-EDIT lifecycle property -- the deprovision/reconcile surface 13 already defers to the Phase-2 build arc. Reconcile/prune (S6 asserts live-state == resolved-set, DELETES extra grants) is a DESTRUCTIVE op against live cloud IAM; specifying it inside a Phase-1 spec that provisions nothing and has no teardown surface is premature. Defer is correct -- but the 35.5 honesty constraint binds the deferral: acceptable ONLY if M1 stops claiming the subtractive property it does not yet have.
    m1_honesty_edit_daedalus_owes: (1) 5.A -- qualify the scope-is-a-pure-function-of-the-manifest / a-re-run-cannot-widen-scope claim: scope is a pure function of the manifest ON INITIAL PROVISION; a re-run after a manifest REMOVAL converges the ADD-direction but does NOT prune a dropped-entry SA grant -- the dropped grant stands until reconcile. (2) 12.A M1 how-defeated cell -- append the residual: holds on initial provision; a re-provision after a manifest removal leaves a stale secretAccessor/grant until reconcile; reconcile/prune-on-removal is a NAMED Phase-2 builder-lifecycle residual. (3) S6 (or 13 + 10) -- name reconcile/prune-on-removal (S6 asserts live-state == resolved-set, no extra grants) as the explicit Phase-2 builder-lifecycle follow-up. (4) classify r2 (manifest integrity) as a 35.5 NAMED RESIDUAL (Phase-1 integrity rests on repo/git access-control + project-seat review; Phase-2 manifest-approval governance is the hardening) so it carries a classification per 35.1.

  non_findings:
  - M2 vs op-disc 20 anti-patterns -- checked: emit-then-apply value-free spec + CI-via-WIF/human-one-shot + STDIN-only is the CORRECT CI-mediated shape; no per-call op / file-on-disk / env-injection / op-run-wrapper / local-MCP-broker anti-pattern present, no refusal-as-signal route-around. Clean, not a finding.
  - M4 guard fires for only pgvector? -- checked pseudocode L155 (baseline_set derived from the WHOLE baseline record): fires for all 5 baseline entries, generalizes to future ones. Not a finding (the WP-6 fix working as designed).
  - M5 mistaken for a 36 coverage gap? -- checked: platform-limitation residual, not an un-probed mitigation gap; 36 correctly does not fire (FM idx62 corroborated). Not a finding.
  - Other resolution edges still fail-OPEN? -- add-and-omit (add-wins KEPT), unknown-category (ERROR fail-closed), empty/absent delta (no-op) all fail-closed or benign; the only former fail-OPEN path (baseline omit) is now closed by 2.4/2.6. Not a finding.

  threat_coverage_assessment: design-time probe-SPEC adequacy is ADEQUATE for the CONFIRMED set -- 8.4 specs a threat-anchored M4 probe (raises BaselineOmitError), and 8.1/8.3 spec M3/M1-adjacent resolved-set assertions; PLINY has queued VERA threat-coverage probes for M1-M4/M6 driving the SPECIFIC attack-paths. ONE producer-side gap: once r1 is folded, the Phase-2 reconcile/prune residual will need its own threat-anchored probe AT PHASE-2 (out of Phase-1 probe scope by this ruling) -- flagged so it is not silently dropped at the Phase-2 build.

summary: TIGHT A2-gate maps-confirm. M1-M4/M6 classifications are all CORRECT and every how-defeated mechanism genuinely BREAKS its named attack-path (not a happy-path proxy) -- verified against the cited live sections (5.A, 4 S0-S6, 3.4, 2.4/2.6, 7). M5 is honestly bounded as an op-disc 35.5 named residual and is NOT overclaimed; the FM binding that 36 does not fire on M5 is corroborated (platform-limitation residual, not an un-probed coverage gap). The 12.C not-threat-ratified list is correctly classified -- no security-relevant change hides in it. TWO load-bearing risks force a revise, both about HONESTY rather than a broken mechanism: r1 -- M1 + the 5.A pure-function invariant overclaim in the SUBTRACTIVE direction (a re-provision after a manifest removal leaves a stale grant; S6 never asserts live-state==resolved-set). I RULE reconcile/prune-on-removal a Phase-2 builder-lifecycle follow-up (Phase-1 = initial-provision correctness; reconcile is a destructive op against live IAM with no Phase-1 teardown surface), CONDITIONAL on M1 being qualified so it stops claiming the subtractive property. r2 -- manifest integrity/authorship is an unclassified trust boundary that must carry a 35.5 named-residual classification per 35.1. The exact DAEDALUS edits are enumerated in m1_honesty_edit_daedalus_owes. Posture: structurally sound design, two honesty-qualification edits owed; no mechanism is broken. Once folded, both r1 and r2 JOIN the relay-UP package (M5 + held-fork) so the Grand sees the COMPLETE residual set.
