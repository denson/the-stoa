---
author: Denson Smith
---
# NOMOS conformance verdict — KEY-DISCOVERY PROCESS addition (stoa--jw5, TARGETED gauntlet stage 6/6)

verdict: CONFORMANT
ticket: stoa--jw5 (u--9s2 Phase-1)
checked_output: the KEY-DISCOVERY PROCESS addition (Phase-1 design revision) — design-formal.md §16–§23
  (on disk + re-attached to beadwork, current sha 6cf59595) + the discovery-check/ harness
  (catalog/generate/validate/run.py + RESULTS.md, reusing resolution-check/resolve.py UNMODIFIED) + the
  three discovery verdicts (argus/vera/cato-discovery-verdict.md) + the bw stage echoes.

## Per-dimension result

1. NEW-SCOPE COVERAGE — CONFORMANT. Every relayed scope element present: §17 service→key catalog
   (record schema + structural invariants + Phase-1/2); §18 DECLARE-primary + SCAN-validator discovery;
   §19 manifest GENERATION (G1–G4 deterministic); §20 manifest VALIDATION (V1–V5 fail-closed before S0);
   §21 EMERGENT-TEMPLATES reframe; §22 catalog seed + emergent categories; §23 three worked examples VIA
   discovery (prospector/scienceclaw/labstat_bls). Tier placement honored (catalog = T1; declaration = T3).

2. FALSIFICATION TEST (re-run FIRST-HAND) — CONFORMANT. Ran BOTH harnesses myself:
   - discovery-check/run.py exit 0: generation produces manifests the UNCHANGED resolve() resolves to
     8/6/7 (§8.1/8.2/8.3), each EQUIVALENT to the §8 hand-authored manifest; V1–V5 PASS on all 3;
     NEG-1 (undeclared-but-scanned bls-oews) → V5 FAIL fail-closed; NEG-2 (uncataloged declared service)
     → generate() RAISES UncatalogedServiceError + V1 FAIL fail-closed.
   - resolution-check/run.py exit 0 (regression): 8/6/7 exact + §8.4 BaselineOmitError + §3.4
     runtime-completeness + §5.A SA-scope all hold. NO regression from the addition.

3. §2 CONSTRAINT (gated Part-1 textually unchanged; resolve.py reused unmodified) — CONFORMANT.
   - resolve.py sha = 3764ca6e (matches the brief; mtime 15:57 predates all discovery files 21:01–21:03;
     discovery-check has zero write/open/provision/net calls; imported resolve.__module__=resolve from
     ../resolution-check). resolve.py UNMODIFIED, proven structurally.
   - GATED MECHANISM/INVARIANT sections (§0–§11: resolver §2 set-algebra, §2.6 BaselineOmitError, §3.4
     runtime-completeness, §4 provisioning S0–S6, §8 fixtures 8/6/7, §11 fork-fold) are BYTE-IDENTICAL to
     the immediate pre-fold beadwork attach (e960384): `diff head -804 disk vs predecessor` = NO DIFF.
   - The ONLY gated-region delta vs the pre-fold baseline is confined to §12.B.1 (the designated
     residual-recording target): the R-3 catalog-integrity line + the relay-set update to the COMPLETE
     { held-fork (RESOLVED), M5 (MOOT), R-1, R-2, R-3 }. This is the DAEDALUS R-3 doc-fold, FM-verified
     additive-only at sha 6cf59595. ARGUS's d1fe1087 byte-proof was the PRE-fold state; the fold then
     edited only §12.B.1; my diff confirms §0–§11 mechanism content is untouched. The §2.4/§2.6 NOTE
     paragraph still exists on disk (line 858, shifted +3 by the fold) — not a deletion. CONFORMANT.

4. RESIDUALS HONESTLY CARRIED — CONFORMANT. §12.B.1 relay package = COMPLETE set
   { held-fork (RESOLVED — Branch A/prepaid card), M5 (MOOT), R-1 (prune-on-removal), R-2
   (manifest-integrity), R-3 (catalog-integrity) }; R-1/R-2/R-3 named as the live Phase-2 residuals.
   R-3 catalog-integrity recorded (fleet-wide SoT, wider blast radius than R-2; §35.5 named residual).
   DWP-3 honestly scoped (V5 = import-detectable drift only; raw runtime-config no-import-signal →
   Phase-2 runtime observer; NOT over-claimed). No overclaim of discovery completeness.

5. SCOPE BOUNDARY — CONFORMANT. SHAPE-only: §16.1/§17.5/§19.4/§20.3 Phase-1-vs-Phase-2 sections name
   catalog DATA, scanner, generator, runtime-observer ALL as Phase-2; cookie-cutter not built; nothing
   provisioned (harness pure — no provision/net/write).

6. AUTHOR ATTRIBUTION — CONFORMANT. `author: Denson Smith` frontmatter on design-formal.md +
   catalog/generate/validate/run.py + argus/vera/cato-discovery-verdict.md. No foreign author-like
   field; all "author" prose in design-formal.md is manifest-authoring-discipline description, not an
   attribution field.

7. bw-RECORD CONSISTENCY — CONFORMANT. Verdict files (verdict: pass / posture CLEAN) match the bw
   stage echoes (ARGUS PASS, ADA PASS, VERA pass, CATO pass). design-formal.md disk sha 6cf59595 ==
   latest beadwork attach (f1e0728) byte-for-byte. Threat-coverage bindings (discovery-completeness p6
   V2 anti-under-provision / p7 V5 drift) are in probes_executed with NON-EMPTY probe_evidence +
   attack_path_exercised (both halves: attack BLOCKED + legit NOT broken). No empty binding / §36 T-a/T-b
   shape.

8. §36 NON-TRIGGER — CONFORMANT. §23.4 classifies every discovery element (catalog/declare-scan/G1-G4/
   V1-V5/emergent = not-threat-ratified; T3-declaration = R-2 lineage; catalog-SoT = R-3 named residual).
   No named threat has an un-probed coverage gap that SHOULD have a probe. R-3 + DWP-3 are honest
   surfaced-not-defeated residuals (§35.5 — no Phase-1 defeat-probe owed), NOT un-probed mitigations.

divergences: NONE.

ground_truth_consulted:
- bw show stoa--jw5 (dispatch ticket — full upstream gauntlet stage echoes)
- python discovery-check/run.py (exit 0; 8/6/7; V1-V5; NEG-1/NEG-2 fail-closed)  [FIRST-HAND]
- python resolution-check/run.py (exit 0; regression 8/6/7 + BaselineOmitError + §3.4 + §5.A)  [FIRST-HAND]
- sha256sum resolution-check/resolve.py = 3764ca6e
- sha256sum design-formal.md = 6cf59595 == git show f1e0728:.../design-formal.md (latest beadwork attach)
- diff head -804 (disk) vs git show e960384:.../design-formal.md (pre-fold attach) = NO DIFF (gated §0–§11)
- diff head -856 (disk) vs e960384 / f1c09e4 = only §12.B.1 R-3 fold hunks
- git log beadwork -- attachments/stoa--jw5/design-formal.md (attach order: f1e0728>e960384>f1c09e4>b269682)
- grep author fields (design-formal.md:2 + 4 harness py + 3 verdicts = Denson Smith)
- discovery-check write/open/provision/net audit = none
- vera-discovery-verdict.md threat_coverage (p6/p7 bindings non-empty)
- design-formal.md §12.B.1 / §23.4 / §16.1/§17.5/§19.4/§20.3 sections

summary: The KEY-DISCOVERY PROCESS addition is CONFORMANT to the new-scope directive and internally
  consistent across bw + on-disk artifacts. The load-bearing checks all converge first-hand: both
  harnesses pass (8/6/7 + V1–V5 + negative probes fail-closed + clean regression); the §2 constraint
  holds (resolve.py sha 3764ca6e unmodified; gated mechanism sections §0–§11 byte-identical to the
  pre-fold baseline; the only gated-region delta is the FM-verified additive R-3 doc-fold into the
  designated §12.B.1 residual target); residuals honestly carried (R-1/R-2/R-3 Phase-2; DWP-3 not
  over-claimed); SHAPE-only scope; author = Denson Smith throughout; threat-coverage bindings non-empty
  with both attack-path halves observed. The discovery addition is purely upstream of the unchanged,
  already-Grand-gated resolver. No blocker for the Grand's gate on the addition. NOTE (not a divergence):
  the whole agents/design/stoa--jw5/ tree is untracked on main — expected; durable capture is via bw
  attach, PLINY does not merge/push.

gap_or_blocker: none.
