# Arc 43 build directive — substrate-canon-update: META-discipline harvest from Pass 10 stellation + validate-spec parser refinement

## Context

Arc 43 is post-Pass-10 substrate-canon evolution. Stellation Pass 10 (Arcs 1-5 shipped clean 2026-05-18) generated 7+ META-discipline candidates with substantial empirical anchors. Plus Arc 42 first-run identified validate-spec parser limitations (WP-1 residue per stoa--4zj). Both consolidated for Arc 43 to land before PRINCIPAL's next heavy-lift product engagement (beadworks + ghost project) so the gauntlet ships with maximally-sharpened design-phase discipline.

**Two source tickets bundled per Arc 37/38/40 precedent:**

- **C1: stoa--yl1 (P3)** — Consolidate 3 base + 7 accreted META-discipline extensions to CAPTAIN_DAEDALUS.md §6 (filed Pass 8 with 3 candidates; expanded to 7+ via Pass 10 accretion comments). **Canon-promotion-ripe**: §6.9.3'' COMPLETENESS CLAUSE alone has 6+ empirical anchors across orthogonal defect-classes.
- **C2: stoa--4zj (P3)** — validate-spec parser refinement (Arc 42 first-run WP-1 residue): check-1 §-ref resolver heading-skip heuristic + check-2 claim-status disambiguation.

## Candidate enumeration (the substance)

### C1: stoa--yl1 consolidated META-discipline catalog

**Original 3 base candidates (filed Pass 8 post-Arc-42):**

1. **§6.9.3' round-trip-adjacent-prose** — live-round-trip prose adjacent to probe-specs (parentheticals, "or equivalently" clauses, algorithmic justifications) through probe's actual semantics. Anchors N=3 (Arc 2 r4 + Arc 3 r4 + Arc 3 ADA Phase 4.5).
2. **§6.2.1' canonical-code-block-fix** — when §6.2 self-catch names a defect, the fix MUST land at the §2.X canonical code-block ADA reads as authoritative, NOT only in §11 step-list reference. Anchors N=4 (Arc 3 r1 + Arc 3 rev2 o1 + Arc 3 VERA Probe L + Arc 4 WP13).
3. **§6.9.3'' live-RT-probes-at-authoring** — LIVE-RUN probes at design-authoring time when structurally roundtrippable; prose-auditing alone insufficient. Anchors N=4 (Arc 3 r4 + Arc 3 ARGUS-rev2 + Arc 4 rev1 F/I/L + Arc 4 ARGUS-rev2).

**7 accreted candidates (filed Pass 10 stellation):**

4. **§6.9.3'' COMPLETENESS CLAUSE + SIBLING-DEFECT-CLASS EXTENSION** — when applying COMPLETENESS to one defect-class, audit for related-but-different defect-classes too (grep-anchored AND Vitest-assertion-stub AND POSIX/Windows AND hex-escape — sibling shapes of the same root: under-specified probe). Anchors N=6 across orthogonal defect-classes (Arc 4 rev1 r3 x27 + Arc 4 rev2 r2 POSIX/Windows + Arc 4 VERA F/K2/L2 + Arc 5 ARGUS-rev1 r2 stub-Vitest + Arc 5 ARGUS-rev2 SIBLING-class catalog). **Cost-multiplier math at both anchors**: 60× for skipping vs ~60s for applying. **Strongest possible canon-promotion evidence.**
5. **§6.X qualitative-acceptance-anchor surface** — SSoT-with-WHY pattern (motionVocabulary.ts at stellation Arc 4) enables systematic §6 anti-pattern audit at cold-read. Arc 4 CATO independently verified the surface enables systematic verification. **§6.Y motion-vocabulary SSoT may merge into §6.X** per Arc 4 ARGUS rev1 r8 observation.
6. **§6.Z three-surface reduced-motion architecture** — Arc 4 origin (MotionConfig + @media reduced-motion + useReducedMotion); may merge with §6.X per ARGUS rev1 r8.
7. **WP13 API-docs-examples-don't-generalize-to-differently-shaped-elements** — DAEDALUS-rev2 picked attrX/attrY based on motion docs SVG-component generic example; ARGUS-rev2 caught SVG `<g>` has no native x/y per MDN+SVG2 spec. Discipline: ground-check chosen API against actual element-type attribute surface, not just docs example. **Two anchors**: Arc 4 rev2 r1 attrX/attrY + Arc 5 §6.4 motion layoutId NOT supported on SVG.
8. **ADA Dev1 motion-animate-vs-SVG-attr scope** — motion's animate-prop overlaps SVG-attribute-driven prop → motion wins in jsdom; resolution: scope reduction. Build-discipline candidate.
9. **ADA Dev2 AnimatePresence-popLayout jsdom timing** — popLayout exit doesn't complete in jsdom (rAF doesn't drive motion's animation loop); resolution: expectStarHidden helper accepting EITHER testid-absent OR opacity-zero. Test-surface-discipline candidate.

### C2: stoa--4zj parser refinement

Two parser limitations from Arc 42 first-run mech-check-results.md (substantially documented per the ticket body):

1. **check-1 §-ref resolver** — bare-`§N.X` resolver over-matches the spec's own section headings (e.g., spec body reference `§13.11 Pass 9` matches against §13.11 heading AND narrative prose). Need: heuristic to skip refs that ARE spec's own headings.
2. **check-2 claim-status parser** — STRANGE classification rate (36 of 65 tickets) reflects ambiguous-prose patterns the parser can't disambiguate. Two options: tighter regex on `bw show <id>` output OR pivot to structured-frontmatter approach in §13.5-§13.9a candidate enumerations.

## Architectural decisions A1-A20 (LOCKED unless flagged DAEDALUS-discretion)

### Bundle structure
- **A1 LOCKED**: single design.md document covering C1 + C2. Per Arc 37/38/40/42 precedent.

### C1 yl1 — META-discipline canon landing
- **A2 LOCKED**: candidate landing at CAPTAIN_DAEDALUS.md §6 family (extending §6.9 shipped Arc 42). Section structure: §6.9.3' / §6.9.3'' (with COMPLETENESS CLAUSE + SIBLING-DEFECT-CLASS EXTENSION as sub-clauses) / §6.2.1' / §6.X qualitative-acceptance-anchor (and merged §6.Y/§6.Z per A3 below) / §6.10-ish API-docs-don't-generalize (per A4).
- **A3 DAEDALUS-discretion**: §6.Y motion-vocab-SSoT + §6.Z three-surface-reduced-motion merger:
  - **(α)** MERGE all 3 into §6.X qualitative-acceptance-anchor as a unified "SSoT-with-WHY pattern" discipline with motion-vocab + reduced-motion as worked examples
  - **(β)** Keep §6.X / §6.Y / §6.Z separate (3 sub-sections)
  - **(γ)** Hybrid: §6.X as parent discipline + §6.Y / §6.Z as named instances under it
  - User-tier leans (α) MERGE — cleanest canon shape; ARGUS rev1 r8 explicitly flagged the merger opportunity; the underlying discipline is one (SSoT-with-WHY enables qualitative-acceptance audit), with motion-vocab + reduced-motion as instances of the pattern.
- **A4 DAEDALUS-discretion**: WP13 + ADA Dev1 + ADA Dev2 landing location:
  - **(δ)** All 3 land at CAPTAIN_DAEDALUS.md §6 (extends design-time discipline canon)
  - **(ε)** WP13 at CAPTAIN_DAEDALUS.md §6; Dev1 at CAPTAIN_ADA.md (build-time discipline); Dev2 at test-discipline canon (new substrate/operating-disciplines.md section OR CAPTAIN_ADA.md test-discipline subsection)
  - **(ζ)** All 3 at CAPTAIN_DAEDALUS.md §6 but with cross-refs from CAPTAIN_ADA.md naming the build-time + test-surface-discipline implications
  - User-tier weakly leans (ε) split-by-seat — WP13 is design-time (DAEDALUS reads API docs); Dev1 is build-time (ADA writes the motion+SVG-attr code); Dev2 is test-surface (ADA writes the jsdom-mitigation). Different seats consume different canon.
- **A5 LOCKED**: §6.9.3'' COMPLETENESS CLAUSE + SIBLING-DEFECT-CLASS EXTENSION ships with the cost-multiplier math (60× anchor) + 6 empirical anchors enumerated. This IS the canon-promotion shape per Pass 10 evidence.
- **A6 LOCKED**: cite-comments per Arc 38 A17 — every new §6.X section that cross-refs to existing §6.9 or §6.2 must resolve via cite at every read-site. Same pattern as Arc 42 §6.9 ship.

### C2 4zj — validate-spec parser refinement
- **A7 LOCKED**: refinement target = `substrate/skills/validate-spec/_lib/spec_refs.py` (check-1 resolver) + `substrate/skills/validate-spec/_lib/bw_tickets.py` (check-2 parser) per Arc 42 file structure.
- **A8 DAEDALUS-discretion**: check-1 heading-skip heuristic shape:
  - **(η)** Pre-build set of spec's own section headings from `^## §N|^### §N|^#### §N` pattern; for each ref like `§13.11`, check if it IS itself a heading in the set; if yes skip (it's self-reference, not cross-ref)
  - **(θ)** Treat all bare-§ refs at section-heading lines as self-references; only count refs in non-heading text as potential cross-refs
  - **(ι)** Hybrid: combine (η) + (θ) — exclude both spec-self-headings AND heading-line citations
  - User-tier leans (η) per the original stoa--4zj ticket text + simplicity.
- **A9 DAEDALUS-discretion**: check-2 claim-status parser refinement:
  - **(κ)** Tighten regex on `bw show <id>` output for claimed-status fields (non-canon-touching; probably won't get below ~10% STRANGE)
  - **(λ)** Pivot to structured-frontmatter approach: require frontmatter-style status annotations in §13.5-§13.9a candidate enumerations (e.g., `- **stoa--XXX (P3, status:closed)** — ...`); canon-touching but reduces STRANGE to near-zero
  - **(μ)** Hybrid: ship both — tighter regex for default + frontmatter-style for new candidate filings; gradual migration
  - User-tier weakly leans (μ) hybrid — preserves backward compat while encouraging tighter form for new tickets.
- **A10 LOCKED**: validate-spec re-runs against SPECIFICATION.md as part of arc (per Arc 42 A26 self-application). Artifact updates at `agents/observation/spec-validation/mechanical-check-results.md`. Acceptance: check-1 FAIL count drops substantially from 144 (Arc 42 baseline); check-2 STRANGE count drops from 36.

### Universal (continued from Arc 42)
- **A11 LOCKED**: §28 Co-Authored-By trailers per Arc 35 canon — all ADA + DAEDALUS commits. Phase 4 squash-merge per MAJOR_PLINY.md §5.10 (no `--body` override).
- **A12 LOCKED**: §5.10 signoff with live-verified state per §19.6.
- **A13 LOCKED**: `[from: pliny-the-stoa]` / `[from: polybius-the-stoa]` author tags per Arc 36 §7.1/§7.7. Cross-tier `[for: user-tier-polybius]` for surface-up.
- **A14 LOCKED**: cron infrastructure — fresh session crons (POLYBIUS_the_stoa + PLINY_the_stoa shut down post-Arc-42 at 10:12:36Z; this arc spawns fresh). Same shape as Arc 38 priming (polling */5 + +144h renewal). PLINY adopts polling-cron per §6.2a (Arc 42 ship) — no longer canon-departure, now canonical.
- **A15 LOCKED**: cite-comment discipline per Arc 38 A17 — every cross-ref between new §6.X sections + extended §6.9 + existing §6.2 must resolve via cite at every read-site.
- **A16 LOCKED**: A18 IMMUTABLE — Arc 43 ships canon-edits to existing files (CAPTAIN_DAEDALUS.md + possibly CAPTAIN_ADA.md + validate-spec Python helpers); no new substrate skill SKILL.md frontmatter files in LOCKED scope. If A4 picks (ε) with new substrate/operating-disciplines.md section for test-discipline, no new file frontmatter; if a new file ships, `author: Denson Smith` required.
- **A17 LOCKED**: A19 source-ticket closure — on Arc 43 ship: close stoa--yl1 + stoa--4zj with cross-refs to merge commit + audit comments per candidate. Tag `[for: user-tier-polybius]` on a coordination ticket (file new OR re-use closed stoa--utn).
- **A18 LOCKED**: A20 pre-branch hygiene per §5.9 + worktree at `.claude/worktrees/arc-43-build/` per §5.9.4. Pre-flight two-check rule.
- **A19 LOCKED**: out-of-scope hard-locks (Arc 43-specific):
  - No restructuring §6.9 base canon beyond extension + cross-ref additions (Arc 42 §6.9 base stays as-is)
  - No widening yl1 candidates beyond the 7+ enumerated (no new META-disciplines fold in mid-arc)
  - No expanding 4zj beyond check-1 + check-2 (other parser-class limitations stay deferred)
  - No new substrate skills (yl1 + 4zj both edit existing canon)
- **A20 LOCKED**: CATO MANDATORY per substrate-canon-update arc-shape — substrate canon evolves; CATO honesty audit ensures the META-discipline wording is structurally sound + the 4zj parser changes don't regress validate-spec accuracy.

### Arc-shaping (continued from Arc 42)
- **A21 LOCKED**: bw-signal dispatch model. POLYBIUS_the_stoa + PLINY_the_stoa sessions spawned fresh by PRINCIPAL paste; per Arc 42 §6.2a now-canonical pattern: PLINY adopts polling cron + surface-and-wait — both seats poll bw for `[for: <self>]` tagged comments. user-tier POLYBIUS dispatches Arc 43 via bw comment on the coordination ticket.
- **A22 LOCKED**: A26 SELF-APPLICATION TARGET — validate-spec MUST re-run against SPECIFICATION.md after C2 build lands; artifact captures FAIL-count delta vs Arc 42 baseline (144 check-1 + 36 check-2 STRANGE → expected substantial reduction). Ships with evidence-of-use, not just evidence-of-existence.

## DAEDALUS sub-decisions summary

| ID | Decision | User-tier lean | DAEDALUS picks |
|---|---|---|---|
| A3 | §6.X/§6.Y/§6.Z merger | (α) MERGE all into §6.X | yes |
| A4 | WP13/Dev1/Dev2 landing | (ε) split by seat (DAEDALUS / ADA / test-canon) | yes |
| A8 | check-1 heading-skip heuristic | (η) spec-self-headings set | yes |
| A9 | check-2 parser refinement | (μ) hybrid (regex + frontmatter migration) | yes |

If DAEDALUS judges any pick exceeds discretion (e.g., A4 split reveals test-discipline canon doesn't have a clean home), surface as PRINCIPAL-gate per §25.

## Self-application observations to watch for stoa--bbi accretion

- **Arc 43 is META-discipline canon itself** — the canon shipped by this arc improves future arcs' design-time discipline. Watch whether Arc 43's own design-phase honestly applies §6.9.3'' COMPLETENESS CLAUSE (sibling-defect-class audit at every fix) + §6.2.1' canonical-code-block-fix (canon lands at §6.X canonical site, not just §11 reference). Recursive self-application is the strongest possible empirical anchor.
- **validate-spec re-run** generates fresh first-run data — observe whether the 4zj refinement delivers the expected FAIL-count reduction AND whether ANY new STRANGE classifications surface (parser tightening may reveal new ambiguity surface).

## Ship gate

Arc 43 ships when:
- design.md cleared by ARGUS (rev cycles per DAEDALUS judgment; expect 0-2 cycles given META-discipline canon evolution is well-anchored)
- ADA build complete: CAPTAIN_DAEDALUS.md §6.X family extended; CAPTAIN_ADA.md / op-disc updates per A4 pick; validate-spec _lib/ Python helpers refined
- ADA runs validate-spec against SPECIFICATION.md; artifact updated with FAIL-count delta
- ZENO mechanical PASS
- VERA falsification PASS on probes
- **CATO craft + scope + HONESTY review** PASS (A20 mandatory — canon evolution requires craft scrutiny + verification that the META-discipline wording captures the empirical anchors faithfully)
- Phase 4: squash-merge per §5.10 (no `--body` override); cleanup; §5.11 paste archival
- §5.10 signoff with live-verified state
- Source tickets closed per A17; `[for: user-tier-polybius]` tag on coordination ticket

**After Arc 43 ships clean + user-tier QA pass** → substrate-team transitions to product-mode-ready posture with sharpened META-discipline canon. PRINCIPAL ratifies next motion (beadworks + ghost heavy-lift project).

## What's explicitly out of scope per §13.14 + Arc 43 A19

- **stoa--sp1 / stoa--2i5 / stoa--3na / stoa--lyw** — open tickets at the-stoa NOT in this arc; routed for future arcs OR direct-to-main housekeeping per individual ticket scope.
- **stoa--tvc / stoa--myd** — deferred-with-gating per §13.9; not actionable until gates fire.
- **stoa--bbi** — observation-only accretion; this arc generates additional N-evidence but doesn't close the ticket.
- **Pass 10 stellation Arc 6 polish** — PRINCIPAL deferred indefinitely; not this arc's scope.
- **Beadworks + ghost project setup** — post-Arc-43 ratification; not this arc.
