author: Denson Smith
ticket: stoa--jw5 (u--9s2 Phase-1)
seat: CAPTAIN_CATO_the_stoa (REVIEWER) — TARGETED gauntlet stage 5/6

status: completed
ticket: stoa--jw5
verdict: pass
diff_reviewed: agents/design/stoa--jw5/ KEY-DISCOVERY PROCESS addition — design-formal.md §16-§23 + discovery-check/ harness (catalog.py, generate.py, validate.py, run.py, RESULTS.md), against the FROZEN gated Part-1 §0-§13 + resolution-check/resolve.py
design_artifact_compared_against: agents/design/stoa--jw5/design-formal.md §16-§23 (cross-checked vs discovery-codesign.md)

concerns: []

follow_ups:
- none. (The ≥2-builder emergence-detection OWNER, the V5 scanner impl, the catalog DATA, and the generator/runtime-observer code are all NAMED Phase-2 in §16.1/§18.4/§21.3 — correctly scoped out, not omissions.)

verifier_coverage_assessment: |
  VERA exercised the load-bearing cases and her pass is justified by the evidence. I re-ran BOTH harnesses
  first-hand (discovery-check/run.py exit 0 -> 8/6/7 EXACT + V1-V5 + NEG-1/NEG-2 fail-closed; resolution-check/run.py
  exit 0 regression) and independently RE-DROVE both threat-coverage probes out-of-harness:
  - p6 (V2 anti-under-provision): I hand-built the dropped-key manifest {document-consuming, delta:{}} for declared
    [document-parsing, bls-oews] -> V2 BLOCKED it ("called-but-unresolved: [(thirdparty_rest_key, BLS_OEWS_API_KEY)]")
    AND the correct generated manifest PASSED V2. Drove the actual attack-path, not a happy-path proxy. Both halves hold.
  - p7 (V5 drift fail-closed): I drove scan_detected=[google-maps,spatial-db,bls-oews] vs declared=[google-maps,spatial-db]
    -> V5 BLOCKED ("shadow service(s) detected but not declared: ['bls-oews']") AND the no-drift positive PASSED V5.
    Both halves hold.
  item-11 mechanical cross-check (seat-side grep, NOT a free pass on VERA self-policing): both cited defeats_via_probe ids
  (p6, p7) appear in VERA's probes_executed set {p1..p7} with non-empty probe_evidence. No empty binding (§36 T-a/T-b clean).
  VERA's resolve.py-unmodified structural proof is sound and I re-confirmed it: sha256 3764ca6e (matches VERA's cited sha);
  discovery-check performs ZERO open()/write calls (imports resolve only); resolve.py mtime 15:57 predates all discovery
  files (21:01-21:03); the imported resolve.__module__ resolves to ../resolution-check/resolve.py. The structural proof is
  conclusive for this arc (a file never opened cannot have been edited); the untracked-tree caveat VERA noted is correct and
  is captured durably via bw attach, not a defect.

summary: |
  The KEY-DISCOVERY PROCESS addition (§16-§23 + the discovery-check harness) is a clean PASS — no blocking,
  recommended-revision, or minor concerns. SHAPE of the cold-read by dimension:
  (1) CRAFT/HYGIENE: generate.py implements §19 G1-G4 faithfully — best-fit MAX-SUBSET emergent category with a
  category-tag-ascending tie-break (sorted(categories)), delta.add = called\(baseline|category), delta.omit =
  category\(called|baseline), and omit-never-baseline holds BY CONSTRUCTION (category_set disjoint from baseline_set
  because baseline is not in any catalog/category record, §17.2.3 — strictly stronger than the Part-1 §2.6 runtime
  guard). validate.py V1-V5 per §20; V4 genuinely REUSES resolve/BaselineOmitError/check_runtime_completeness from the
  unchanged resolve.py (passed in, not re-implemented). catalog.py = the §22 seed records with the §3.4 pairing carried
  in the google-maps record (BOTH (gcp_api,google-maps) AND (gcp_secret,MAPS_API_KEY) in one record — §17.2.2). The
  harness is PURE (no open/network/subprocess/provisioning; only the §2.6 typed except-blocks, which record detail and
  never silently swallow). No dead code, no TODO/FIXME, no debug leftovers.
  (2) CONSISTENCY: discovery-codesign.md -> design-formal.md §16-§23 -> harness -> RESULTS.md -> VERA verdict are
  consistent across catalog records, G1-G4, V1-V5, and the 3 worked examples. The one apparent drift — labstat_bls G2
  yields category document-consuming while §8.3's hand-authored fixture used the alias document/data — is a FAITHFUL
  byte-identical alias (LIBRARY[document-consuming] == LIBRARY[document/data] == [(gcp_api,document-parsing)]; I confirmed
  both resolve to the same 7-set first-hand). Per §22 only geospatial + document-consuming are seeded, so a faithful
  max-subset G2 correctly picks document-consuming. Not a divergence — pre-flagged by ADA/FM/VERA/ARGUS, confirmed.
  (3) §2 CONSTRAINT (load-bearing): resolve.py is REUSED UNMODIFIED (sha 3764ca6e; mtime predates all discovery files;
  zero writes; imported from ../resolution-check) and the regression (resolution-check/run.py) still exits 0 with 8/6/7
  + BaselineOmitError + §3.4 + §5.A. The addition is purely UPSTREAM of resolve(); the gated §0-§13 is untouched (ARGUS
  proved this byte-identical, sha256 d1fe1087, at stage 2 — I did not re-diff the gated region, relying on that load-bearing
  structural proof; the harness side confirms it operationally by feeding GENERATED manifests into the unchanged resolver).
  (4) SECURITY/HONESTY: credential-discipline HELD — catalog declares key NAME/slot only (MAPS_API_KEY, BLS_OEWS_API_KEY
  are env-var slot names), never values. R-3 catalog-integrity is HONESTLY NAMED (surfaced-not-solved): a fleet-wide T1
  SoT with wider blast radius than R-2, classified §12.B.1/§23.4, ARGUS-confirmed as a §35.5 named residual — no Phase-1
  probe owed. DWP-3 is HONESTLY SCOPED: V5 = import-detectable drift only; a service reached purely via raw runtime-config
  with no import signal is closed only by the named Phase-2 runtime observer (§18.1 pillar 3). The design does NOT overclaim
  discovery completeness anywhere — V2/V4 guarantee completeness of the RESOLVED SET relative to the DECLARED services, never
  all services a builder could call. M5-moot / held-fork-closed (Part-1 fold) consistent with §11/§12.B.1.
  (5) SCOPE: SHAPE-only and correct. Catalog DATA, scanner impl, generator code, and runtime observer are all NAMED Phase-2
  (§16.1/§17.5/§18.4/§19.4/§21.3). Nothing provisioned; the cookie-cutter itself is not built; the harness exercises only the
  testable choreography against the 4-record seed.
  (6) AUTHOR ATTRIBUTION: author: Denson Smith on design-formal.md, all 5 discovery-check files (4 .py + RESULTS.md), and
  both verdicts. No author-like field names anyone other than the PRINCIPAL anywhere in the artifact set.
  META-VERIFY-VERA CONCLUSION: VERA's pass is justified by the evidence; both threat-coverage probes drove the actual
  attack-paths (BLOCKED + LEGIT-not-broken, both halves, re-driven by me); no empty/probe-id-without-execution binding;
  resolve.py-unmodified structural proof sound. POSTURE: CLEAN — ready for NOMOS / the final gate. R-3 carried as a named
  residual for the Grand to gate with in view.

[from: CAPTAIN_CATO_the_stoa (subagent) | caller-sid 8040be7f-a1ba-4917-b953-75947d464abf]
