---
author: Denson Smith
ticket: stoa--jw5 (u--9s2 Phase-1)
seat: CAPTAIN_ARGUS_the_stoa (PLAN-CRITIC)
audits: agents/design/stoa--jw5/design-formal.md
gauntlet_stage: 2/6
as_of: 2026-06-25
---

# ARGUS - cold-audit verdict: u--9s2 Phase-1 formal spec

status: completed
ticket: stoa--jw5 (u--9s2 Phase-1)
verdict: revise
design_artifact_audited: agents/design/stoa--jw5/design-formal.md

## Posture

The spec is strong, internally consistent, and the converged-design work shows. resolve() ran byte-exact against all three section-8 fixtures (8/6/7 entries, sorted). The section-3.4 per-API key-bearing classification is web-accurate (independently re-confirmed via gsearch). The held isolation-UNIT fork is correctly surfaced UP to the Grand and NOT closed in-team. Credential-discipline (declare WHAT/WHERE, never values) holds everywhere I checked, and per-builder SA isolation is genuinely DERIVED with no silent cross-builder leak path.

ONE load-bearing risk must be fixed before ADA builds (R1 / WP-6: omittable pgvector). Everything else is ratify-and-proceed or Phase-2 follow-up. Verdict is revise solely on R1.

---

## audit_block

### risks

- id: r1
  description: A manifest can delta.omit (db_extension, pgvector) and resolve() silently drops it with NO error and NO lint warning - producing a runtime-incomplete builder that embeds (gemini-embedding is BASELINE, unconditional) but has no vector store to embed INTO. There is no non-omittable BASELINE subset.
  evidence: section-3.1 (pgvector is BASELINE, every builder embeds); section-2.1/2.3 resolution applies omit unconditionally; section-2.4 the omit-had-no-effect WARNING fires only when the omit target is NOT present, so omitting a PRESENT baseline entry produces ZERO diagnostic; design-codesign section-2 states pgvector-in-baseline EXISTS BECAUSE every builder embeds therefore every builder needs the vector store - so omitting it directly contradicts the design own load-bearing invariant. Verified live: resolve(geospatial, omit=[(db_extension,pgvector)]) returns a 7-entry set with pgvector absent, no error raised.
  load_bearing: true
  quadrant_classification: easy-easy
  consequence: a builder ships, embeds, and 500s / silently-no-ops on every vector write or similarity query - caught only at runtime (or worse, at first user query), not at resolve/provision time. This is the EXACT fail-open the typed model exists to prevent, and the ONLY fail-OPEN path in an otherwise fail-CLOSED design.
  disposition: MUST-FIX-BEFORE-ADA. ARGUS does not design the fix - DAEDALUS/PLINY own it. The gap + consequence are named; the section-10/12 candidate non-omittable BASELINE subset is DAEDALUS own flagged direction.

- id: r2
  description: section-3.4 per-API table renders google-maps (Maps Platform) = API key as if the umbrella gcp_api were uniformly key-bearing, but the web-confirmed truth (the HAMILTON/CHIRON joint position on bw) is per-SURFACE: Maps JS / client-side / legacy Geocoding-v3 = API-key-only; modern server-side Geocoding-v4 / Places-New / Routes = SA/ADC, NO key. The gcp_api entry granularity (umbrella name=google-maps) cannot, as schemad, express WHICH surface a builder calls - so the invariant the credential requirement attaches to the SURFACE not the umbrella api is asserted in section-3.4 prose but NOT representable in the section-1.2 entry model.
  evidence: section-3.4 table row 3; section-1.2 entry shape is {kind,name} with name=google-maps (no surface dimension); bw thread (HAMILTON sid aea18ba0 / CHIRON sid 046d128e joint position); gsearch 2026-06-25 confirms the surface split.
  load_bearing: false
  quadrant_classification: easy-hard
  consequence: For Phase-1 it is SAFE - the geospatial template ships the paired MAPS_API_KEY as the conservative default (a geo product almost always renders a client-side Maps-JS map = key-bearing), so a builder is never runtime-INCOMPLETE; it can only be runtime-OVER-provisioned (carries a MAPS_API_KEY it may not strictly need if purely server-side). Over-provisioning a key is a minor isolation-surface cost, not a fail. The design choice is the correct conservative default. Recorded so the surface-granularity question is on the table for Phase-2 if a server-side-only Maps builder appears.
  disposition: RATIFY-AND-PROCEED (Phase-1) / Phase-2 follow-up if a server-side-only Maps builder is added.

- id: r3
  description: The general runtime-completeness invariant (section-3.4) keys off key-bearing gcp_api, but the entry model has no MACHINE-READABLE flag marking which gcp_api entries ARE key-bearing. Re-reading: the paired gcp_secret IN THE TEMPLATE (section-3.2) IS the in-band signal - S6 can check for each (api,secret) pair the template declares together, both resolved. So this is a DOCUMENTATION gap in S6 phrasing (key-bearing implies an out-of-band verifier table), not a model gap.
  evidence: section-3.4 Phase-2 verify (S6) assert every gcp_api that is key-bearing has its paired gcp_secret resolved - key-bearing is not a field on the gcp_api entry (section-1.2 / 3.3); section-4 S6 restates it without specifying HOW key-bearing-ness is derived from the resolved set alone; section-3.2 template pairing already provides the in-band signal.
  load_bearing: uncertain
  quadrant_classification: easy-hard
  consequence: For Phase-1 (one key-bearing API, Maps) the S6 assertion is trivially checkable. Recommend S6 key-bearing be re-phrased to reference the template-declared pairing rather than an implied verifier-side table. Minor; not a build blocker.
  disposition: RATIFY-AND-PROCEED.

### non_findings

- WP-1 (hard-cap over-claim sweep): DISCHARGED - clean. The spec NEVER claims a hard dollar cap. section-5.B labels the (a)-(d) menu, marks (d) quotas as bounding spend VELOCITY NOT total dollars, (a) alert notify-only, (b) Spend Caps Private Preview, (c) kill-switch REACTIVE/lagging doesnt guarantee you wont spend more. section-11 header literally reads no GA hard-dollar cap exists anywhere. Most load-bearing carried premise-correction; survives verification.
- section-3.4 per-API classification: web-RE-CONFIRMED independently (gsearch 2026-06-25), not trusted from DAEDALUS table. Maps = key-bearing (client-side surfaces); gemini-embedding = SA/ADC key OPTIONAL not required; Document AI = SA/ADC ONLY (no key supported); gsearch -> Vertex+ADC. No other key-bearing-API gap lurking. Table accurate. (Surface nuance = r2.)
- Held fork (section-5/11 structural correctness): CONFIRMED CORRECT. Surfaced UP to the Grand, NOT closed in-team. S0 step 0a handles BOTH branches; section-11 table = both branches, team rec Branch A but Decision owner: Polybius the Grand; DAEDALUS does not pick a branch / carries this unclosed stated twice. Does NOT smuggle a Grand-owned decision. Two-part premise-correction faithful.
- Worked-example fixtures (section-8): resolve() ran byte-exact - prospector 8, scienceclaw 6, labstat_bls 7, all sorted, matching exactly. labstat_bls contains (thirdparty_rest_key, BLS_OEWS_API_KEY), ZERO gcp_api named BLS_OEWS_API_KEY, S1 input correctly excludes it. delta-not-bloat proof holds.
- WP-4 (document/data ALIAS): DISCHARGED for Phase-1. Both resolve to identical 1-entry template; no section-8 example distinguishes them; aliasing reversible (split = additive arc). Hides nothing today. Not load-bearing now.
- WP-5 (Spend Caps Private Preview): DISCHARGED - degrades SAFELY. Per-project conclusion holds WITHOUT Spend Caps (GA path = alert + quotas + opt-in kill-switch is self-sufficient, per VERA Probe 4); labeled preview dependency NOT a GA guarantee; architecture does not lean on it.
- WP-2 (graduation governance): threshold (2+ deltas) + mechanism (promote via arc) stated; detection OWNER named only as governance discipline - no explicit seat owns detection. Minor ambiguity, not load-bearing (no resolver behavior depends on it). Worth a one-line owner assignment; defer-safe.
- WP-3 (multi-category builders): SAFE to defer - no section-8 example needs >1 category; correctly scoped OUT (section-12).
- WP-8 (name case-sensitivity): Phase-2 WARNING on case-only diffs (section-2.2) is sufficient; lowercasing-on-ingest would risk collapsing distinct names. Defer-safe.
- Resolution-rule edge cases - ALL dispositions specified + deterministic: add-intersect-omit => KEPT (add-wins); unknown category => ERROR fail-closed (verified raises); empty/absent delta => no-op; omit of non-present entry => no-op WARNING; duplicate add => INFO. One edge not explicitly tabled: an EMPTY category template ([]) - resolve() handles correctly (union with empty = baseline only), harmless. The ONE missing disposition is omit-of-present-NON-omittable-baseline-entry = R1.
- Credential-discipline + isolation: HOLDS everywhere. emit = value-free spec (slots only); apply = CI-via-WIF or human one-shot from keyring; Railway vars via STDIN never argv/logs; S2c VALUE population is a HUMAN BLOCK; S3 injects this builder SA-key-b64 ONLY. No path where an agent holds a credential VALUE. Per-builder SA bijective + derived (section-5.A); cross-builder leak requires editing the visible manifest or code-reviewed resolver - never config drift.

### threat_coverage_assessment

This design security surface is the per-builder isolation boundary (section-5.A) + credential-discipline (section-4); both correctly structured (derived SA scope, per-secret accessor, value-free spec). No threat-ratified mitigation with a missing threat-anchored probe - isolation probes ARE specified (section-8.3 labstat_bls proves kind-dispatch isolation; S6 asserts no-cross-builder-key). The attack-path most worth a downstream probe is R1 fail-open: recommend ADA/VERA add a probe asserting resolve() REJECTS or WARNS on omit of a baseline-critical entry once the fix lands.

---

## summary

The u--9s2 Phase-1 formal spec is a well-built, internally-consistent design: the pure resolution function is correct (all three section-8 fixtures resolve byte-exact), the typed taxonomy cleanly dispatches provisioning by kind, credential-discipline and per-builder SA isolation hold with no silent leak path, and the section-3.4 runtime-completeness invariant is web-accurate with Maps correctly identified as the lone key-bearing outlier. The held isolation-UNIT fork is structurally correct - surfaced UP to the Grand, not closed in-team, two-part premise-correction (no GA hard-dollar cap + SA-to-PROJECT scope) carried faithfully. The single load-bearing risk is R1 (WP-6): a manifest can omit (db_extension, pgvector) and resolve() silently drops it with no error and no lint - producing a builder that embeds but has no vector store, the ONLY fail-OPEN path in an otherwise fail-closed design, and a direct contradiction of the design own every builder embeds therefore needs the vector store invariant. This must be fixed before ADA builds (a non-omittable BASELINE subset is DAEDALUS own flagged direction; ARGUS names the gap + consequence, does not design the fix). r2 (Maps surface-granularity) and r3 (S6 key-bearing signal phrasing) are ratify-and-proceed - the Phase-1 conservative defaults are correct. Verdict: REVISE, solely on R1.

gap_or_blocker: none (status completed).

- [from: CAPTAIN_ARGUS_the_stoa (subagent) | caller-sid 8040be7f-a1ba-4917-b953-75947d464abf]
