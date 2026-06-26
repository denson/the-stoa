---
seat: CAPTAIN_ARGUS_the_stoa (PLAN-CRITIC)
ticket: stoa--jw5 (u--9s2 Phase-1)
caller-sid: 8040be7f-a1ba-4917-b953-75947d464abf
gauntlet-stage: 2/6 (TARGETED -- KEY-DISCOVERY PROCESS addition, design-formal.md 16-23)
author: Denson Smith
as_of: 2026-06-26
---

# ARGUS cold-audit verdict -- the KEY-DISCOVERY PROCESS addition (design-formal.md 16-23)

status: completed
ticket: stoa--jw5 (u--9s2 Phase-1)
verdict: pass
design_artifact_audited: agents/design/stoa--jw5/design-formal.md (current attach blob 09564d3 == on-disk)

## (A) THE LOAD-BEARING STRUCTURAL CHECK -- gated Part-1 content UNCHANGED -- CONFIRMED

Method: independent diff of the current design-formal.md against the pre-addition beadwork baseline,
NOT a re-read of the DAEDALUS self-report. The brief named prior sha 9718685d; that is NOT a valid
git object in this repo, so I used the VERIFIED immediate predecessor: beadwork attach f1c09e4
(commit 2026-06-25 19:55), blob e807ce8 -- the design-formal.md attach immediately before the
DAEDALUS post-addition re-attach e960384 (blob 09564d3, 20:41). On-disk file == current attach
(byte-identical, blob 09564d3).

RESULT -- the gated region (0 through 13 body, lines 1-856, which contains EVERY gated invariant the
brief named) is BYTE-IDENTICAL between the pre-addition baseline and the current file: identical
sha256 d1fe10870839a6d56178c20b127305f1a3b6395baacc6e0e418951e964586f5f on both. This region carries:
resolver 2 set-algebra ((( BASELINE u CATEGORY ) \ omit) u add); 2.6 BaselineOmitError + the 5-entry
non-omittable set; 3.4 runtime-completeness; 4 provisioning S0-S6; 8 fixtures (8/6/7 arithmetic);
11 fork-fold (CLOSED Branch A / prepaid-card / M5 MOOT / R-1/R-2 named); 12.A threat-maps (M1-M4/M6).
ALL textually unchanged.

The diff shows exactly THREE change hunks, ALL additive -- NO deletion, NO in-place edit of any gated
invariant:
  1. (pre 857a858,1410) 16-23 PART 2 inserted at the 13/14 boundary (the discovery addition).
  2. (pre 876a1430,1443) 14 DoD table: Part-2 rows P1-P8 appended; original rows 1-10 + threat-map
     + fork rows preserved verbatim.
  3. (pre 886c1453,1465) 15 provenance: original sentence preserved VERBATIM, a Part-2 provenance
     paragraph appended, and "Author: Denson Smith." relocated to the new end-of-section position
     (still Denson Smith -- correct authorship, no foreign field).

NO SCOPE BREACH. The 16.0 load-bearing constraint held absolutely. resolve(), provisioning, the 8
sets, and the 12.A threat-maps stand textually unchanged.

## (B) COLD-AUDIT OF THE ADDITION (16-23) -- posture: CLEAN (no load-bearing defect)

External-citation verification (ARGUS 6.5 duty -- training data stale, web-confirmed 2026-06-26):
- OWASP CycloneDX SaaSBOM (18.2 lineage) -- VERIFIED current + accurately represented. SaaSBOM is a
  real OWASP CycloneDX construct (ratified ECMA-424); declared inventory IS the design-time
  authorized inventory; static scan IS positioned as the CI drift-detector; eBPF/OTel IS the runtime
  production check. The 3-pillar map (DECLARE=authorized inventory / SCAN=CI drift-detect=V5 /
  RUNTIME=production confirm=Phase-2) is faithful. The source INDEPENDENTLY corroborates DWP-3:
  declared inventory is "blind to runtime fetching"; runtime observability "may have false negatives
  for rarely used paths" -- exactly the no-import-signal gap 23.3 DWP-3 honestly names.
- Per-API key-bearing classification (carried into the catalog at 17.2.2 / 22) -- VERIFIED current:
  Google Maps JS API = API-key-bearing (client-side, cannot use SA/ADC securely); Vertex AI Gemini
  embedding/search + Document AI = ADC/Service-Account, NO minted key. The 22 seed google-maps record
  pairing {gcp_api,google-maps}+{gcp_secret,MAPS_API_KEY} is correct; document-parsing + gemini-
  family carry no paired secret -- correct. Maps is the lone key-bearing outlier.

Generation G1-G4 (19) edge cases -- all sound:
- add-only path (declared service in NO emergent category): labstat_bls bls-oews (catalog
  category: none) IS this path. G2 picks document-consuming on the OTHER called entry; bls-oews rides
  delta.add. Generated manifest is byte-identical to the 8.3 hand-authored manifest -> 8.3 (7) HIT.
- tie-break (two categories both maximal-subset of called_entries): 19.2 breaks by category-tag
  ascending -- total + deterministic. No 8 example hits it (honestly named DWP-5).
- omit-never-targets-baseline ("by-construction"): G3 derives delta.omit :=
  CATEGORY_TEMPLATE[category] \ (called u baseline). Omit domain is EXACTLY category-template
  entries; baseline NOTIN catalog/category (17.2.3) -> no baseline (kind,name) can ever be a member.
  GENUINELY proven by construction -- STRONGER than the Part-1 2.6 runtime guard: on the generated
  path the BaselineOmitError is unreachable-by-construction, while 2.6 still fires on a hand-authored
  manifest. No weakening of M4.
- uncataloged declared service: V1 ERROR, fail-closed, STOP before emit (19 G1 / 20 V1).

Validation V1-V5 (20) -- fail-closed, before S0, both directions bounded:
- placement strictly before S0 (20.2), fail-closed -- an invalid manifest never enters provisioning.
- V2 COMPLETE (resolve superset-of called_entries) bounds UNDER-provision; V3 MINIMAL (no uncalled
  non-baseline entry) bounds OVER-provision -- both directions genuinely bounded.
- V4 RESOLVE-WELL-FORMED genuinely REUSES the 2.6 + 3.4 guards (does not re-implement) -- Part-1
  invariants stay the single source of truth.

Emergent-reframe (21) 2-preservation (the subtlest risk -- pressure-tested):
- 21.2 holds. The reframe changes ONLY a category PROVENANCE (hand-authored -> emerged-from-co-
  occurrence-then-promoted). CATEGORY_TEMPLATE[category] remains a named entry-set, unchanged in
  shape and in how resolve() reads it. Decisive evidence: the 22 SEED categories (geospatial =
  {google-maps, MAPS_API_KEY, postgis}; document-consuming = {document-parsing}) are BYTE-IDENTICAL
  to the 3.2 hand-curated bundles -- the resolver consumes the same sets and the 8 sets are HIT, not
  re-derived. The reframe does NOT smuggle a semantic change into what the resolver consumes.

Discovery (18) DECLARE-primary + SCAN-validator + runtime-Phase-2: sound. DECLARE is the source of
truth generation reads; SCAN is a fail-closed drift-validator that flags-never-adds (V5); the
precedence (DECLARE generates, SCAN validates, scan-detected-undeclared = V5 ERROR fail-closed) is
internally consistent with the 4 S2c human-gate posture. The web-verified reasoning is accurate.

## (C) RULINGS ON SELF-ASSESSED WEAK POINTS (23.3) + R-3

R-3 catalog-integrity (DWP-4 / 23.4) -- CONFIRMED as a 35.5 named residual (ARGUS 6.9 A4 duty:
upstream classifier PROPOSES, ARGUS CONFIRMS so it cannot be self-exempted downstream). The DAEDALUS
classification is CORRECT and is hereby CONFIRMED:
- The catalog (17) is a NEW fleet-wide single-source-of-truth that 19 G1 trusts BY CONSTRUCTION
  (G1 reads CATALOG[service-id].entries directly). A bad / over-scoped / mis-paired catalog record
  propagates to EVERY builder that declares that service -- genuinely a WIDER blast radius than R-2
  (per-builder manifest integrity).
- It is authz-relevant (drives resolved scope fleet-wide) -> would otherwise carry NO 35.1
  classification -> MUST be classified. NOT Phase-1-defeated (rests on T1 arc-review + git access-
  control -- same trust model as R-2, at T1/fleet scope), so a named residual with Phase-2 hardening
  = catalog-integrity governance is the correct 35.5 shape.
- VERDICT: CONFIRMED as named residual R-3 (catalog-integrity). Record it alongside R-1/R-2 in the
  relay-UP residual package for the Grand to gate WITH IT IN VIEW. This is the 6.9 A4 confirmation
  (recorded so it cannot be self-exempted), not a defect -- the design got it right.

DWP-3 declare-completeness gap (service via raw runtime config, no static import signal) -- ruling:
HONESTLY SCOPED, ACCEPTABLE for Phase-1, NOT a must-fix. V5 scope is honestly import-detectable
drift, NOT all drift (23.3 DWP-3 states this explicitly; 20 V5 / 18.2 scope it to imported SDK /
raw-HTTP-client / known-service-reference). The no-import-signal service is invisible to BOTH declare
and scan and is closed ONLY by the named Phase-2 runtime observer (18.1 pillar 3); the web source
independently corroborates this is the genuine residual gap of any declared-inventory model. The
design does NOT OVERCLAIM discovery completeness anywhere -- V2/V4 guarantee completeness OF THE
RESOLVED SET RELATIVE TO services-called (the declared set), never all services the builder could
possibly call. Acceptable honest-scoping with the runtime observer named Phase-2.

DWP-1 scan-validator feasibility -- CONFIRMED honestly bounded. A weak/absent Phase-2 scanner
degrades V5 to a best-effort drift hint; it does NOT corrupt generation (which reads DECLARE only,
19 G1). V5 is advisory-to-fail-closed, never a generation input. Phase-2-deferred correctly.

DWP-2 emergent bootstrapping (Phase-1 seeds vs the >=2-builder emergence rule) -- CONFIRMED honestly
bounded, NOT a relabel. The 22 seed categories are EXACTLY the 3.2 gauntlet-validated bundles, so 8
holds; emergent is the forward provenance/governance model exercised only once a live population
exists (Phase-2+). NON-LOAD-BEARING observation: the >=2-builder threshold OWNER (who detects co-
occurrence and runs the promotion arc) is unspecified -- a Phase-2 governance-ownership detail,
correctly deferred, surfaced for completeness only.

DWP-5 scope line (choreography proven on a 4-record seed; generator code Phase-2) -- CONFIRMED
honestly bounded. The Phase-1/Phase-2 line (16.1) is drawn correctly: catalog STRUCTURE +
choreography + reframe = Phase-1; catalog DATA + scanner code + generator code + runtime observer =
Phase-2. The 23.1 seed self-run is sufficient Phase-1 evidence the CHOREOGRAPHY hits 8/6/7; best-fit
max-subset selection over a POPULATED catalog (tie-breaking at scale) is correctly a Phase-2 build-
and-verify surface.

## (D) THREAT CLASSIFICATION (23.4) -- CONFIRMED

The discovery front-end adds NO attack path beyond R-3. The poisoned services: declaration scenario
(a malicious/erroneous T3 services: declaration -> over- or under-provision) is R-2 manifest-
integrity LINEAGE pushed one tier up: the declaration is the T3 input that drives the generated T2
manifest, exactly the input-that-drives-resolved-scope-is-an-authz-relevant-trust-boundary (resting
on git-access + project-seat review) that R-2 names. Over-declare is caught by V3-MINIMAL; under-
declare is the DWP-3 gap (Phase-2 runtime observer). No NEW runtime attack path. The 23.4 not-threat-
ratified classifications for 17/18/19/20/21 are CONFIRMED (process/choreography/structure changes;
the runtime-completeness 17 carries IS already M3; the BaselineOmitError preservation rides on
existing M4). No security-relevant element carries NO classification -- confirmed (35.1 satisfied).

audit_block:
  risks:
  - id: r1
    description: NONE load-bearing. The addition is a clean, faithful, web-verified formalization of
      the converged co-design; the gated Part-1 content is byte-identical (sha256 d1fe1087); the
      16.0 load-bearing constraint held absolutely.
    evidence: (A) byte-diff sha256 match d1fe1087 on 0-13; (B) gsearch SaaSBOM + per-API key
      confirms; (C) R-3 confirmation; (D) 23.4 confirmation.
    load_bearing: false
  non_findings: |
    - omit-never-baseline by-construction claim: PROVEN sound (G3 omit domain = category entries;
      baseline NOTIN catalog 17.2.3) -- discharged.
    - V1-V5 fail-closed before S0: both directions bounded (V2 under, V3 over); V4 REUSES 2.6/3.4 --
      discharged.
    - 21 emergent reframe smuggling a resolver-consumed semantic change: discharged -- 22 seed
      categories byte-identical to 3.2 bundles; resolver + 8 sets untouched.
    - per-API key classification (Maps key-bearing vs Vertex/DocAI ADC): web-confirmed current --
      discharged, catalog seed correct.
    - poisoned services: declaration as a NEW attack path: discharged -- R-2 lineage, not distinct.
  threat_coverage_assessment: |
    NO threat-ratified mitigation is DECLARED by the addition (Part-2 is process/choreography/
    structure + one named residual R-3). Every defeated mitigation (M1-M4/M6) lives in the GATED
    12.A, byte-unchanged, and already carries its threat-anchored probe (8.4 is the executed probe
    for M4). Per 6.9: a not-threat-ratified addition + a surfaced-not-defeated residual (R-3) require
    NO new threat-anchored probe -- only honest naming for the Grand to gate. Design-time probe-SPEC
    adequacy is therefore N/A for the addition (no NEW mapped mitigation to probe). HONEST-CLAIM
    BOUNDARY (35.5): I verified named-threat COVERAGE; threat-ENUMERATION completeness for the
    discovery front-end is my unmechanized judgment -- I found no un-named security-relevant element,
    but the threat set is not provably exhaustive.

summary: |
  The KEY-DISCOVERY PROCESS addition (16-23) is a clean PASS. (A) The load-bearing structural check
  is decisive: the gated Part-1 region (0-13, every named invariant) is BYTE-IDENTICAL to the pre-
  addition beadwork baseline (matching sha256 d1fe1087); the only three change hunks are purely
  additive (16-23 inserted at the 13/14 boundary; 14 Part-2 DoD rows appended; 15 provenance
  paragraph appended, original sentence verbatim, authorship preserved as Denson Smith). No scope
  breach; the 16.0 constraint held absolutely. (B) The addition carries no load-bearing defect:
  G1-G4 edges sound (omit-never-baseline by-construction claim genuinely proven, strictly stronger
  than the 2.6 runtime guard); V1-V5 fail-closed before S0, bound over- and under-provision; V4
  genuinely REUSES 2.6/3.4; the 21 emergent reframe is genuinely provenance-only (seed categories
  byte-identical to the 3.2 bundles, so resolver + 8 untouched); both load-bearing external citations
  (OWASP CycloneDX SaaSBOM; per-API key-bearing classification) web-verified CURRENT + accurate.
  (C) R-3 catalog-integrity CONFIRMED as a legitimate 35.5 named residual (fleet-wide SoT, wider
  blast radius than R-2, authz-relevant, not Phase-1-defeated) -- record in the relay-UP residual
  package; this is the 6.9 A4 confirmation, not a defect. DWP-1/2/3/5 each honestly bounded / Phase-2-
  deferred, no over-claim of discovery completeness. (D) The front-end adds NO attack path beyond
  R-3; 23.4 classifications confirmed, no element unclassified. Posture: CLEAN -- ready for ADA, R-3
  carried as a named residual. MUST-FIX-BEFORE-ADA: none. Carry-forward (non-blocking): record R-3 in
  the relay-UP package; add an explicit T3-services-declaration-integrity = R-2 lineage line to 23.4,
  and name the >=2-builder emergence-detection OWNER (Phase-2 governance).

[from: CAPTAIN_ARGUS_the_stoa (subagent) | caller-sid 8040be7f-a1ba-4917-b953-75947d464abf]
