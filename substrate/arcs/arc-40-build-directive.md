# Arc 40 build directive — Pass 6 substrate bundle (4 candidates: 3sz + 5sr + dhc + 6wp; optional fold-in 6n9 + t9u)

## Context

Arc 40 is Pass 6 of SPECIFICATION.md §13 workplan. Theme: Arc-24-era hygiene follow-ups + the Arc 37 squash-merge trailer-regression-fix per §13.7.

**Four LOCKED candidates:**
- **C1: stoa--3sz (P3)** — probe-spec `^last=` anchor canon (Arc 24 follow-up; probe-authoring discipline)
- **C2: stoa--5sr (P3)** — DAEDALUS Edit-tool worktree-path discipline (Arc 24 follow-up; CAPTAIN_DAEDALUS.md note — DAEDALUS reads `agents/design/arc-24/design.md` to articulate the specific failure mode at design time)
- **C3: stoa--dhc (P3)** — python-vs-jq rationale single-source-of-truth lift (Arc 24 follow-up; consolidate 3 near-identical drift-risk locations across MAJOR_PLINY.md §5.8 + MAJOR_POLYBIUS.md §7.6 + op-disc §18 + agent-author SKILL.md)
- **C4: stoa--6wp (P3) [BUG, SEQUENCE-CRITICAL]** — squash-merge `--body` override drops Co-Authored-By trailers (Arc 37 bb12806 regression). **Must ship before Pass 9/10 stellation dispatch** so stellation's squash-merges preserve trailers cleanly per §13.7 final paragraph.

**Optional fold-in candidates (DAEDALUS-discretion per A7):**
- **stoa--6n9 (P3)** — manifest format-version header + reader version-check (Arc 38 CATO c3 follow-up; install.sh write_substrate_manifest + apply/check.sh manifest reader)
- **stoa--t9u (P3)** — install.sh deploy excludes `__pycache__/` when copying Python substrate skills (Arc 39 CATO C1 follow-up; install.sh-adjacent)

Both are install.sh-discipline tickets that may bundle cohesively with the 4 LOCKED candidates. User-tier weakly leans fold-in (both small; both install.sh-adjacent; saves separate arc-cycles). DAEDALUS picks at design time.

## Architectural decisions A1-A22 (LOCKED unless flagged DAEDALUS-discretion)

### Bundle structure
- **A1 LOCKED**: single design.md document covering all 4 LOCKED candidates (+ optional 6n9/t9u if folded). Per Arc 37/38/39 precedent.

### Per-candidate scope
- **A2 LOCKED (6wp)**: MAJOR_PLINY.md §5.10 ship-checklist gains a one-line note: squash-merge MUST NOT use `gh pr merge --body` with custom body that overrides default trailer auto-concatenation; either omit `--body` (Arc 38 forward-fix pattern) OR include trailers explicitly in HEREDOC body.
- **A3 DAEDALUS-discretion (6wp)**: optional op-disc §28.3.1 (or equivalent subsection placement) trailer-preservation pitfall worked-example. User-tier leans include (worked-example is canonical-grade per the empirical anchor at bb12806 / 2026-05-17 / Arc 37); DAEDALUS picks exact insertion shape.
- **A4 DAEDALUS-discretion (5sr)**: specific failure mode framing — DAEDALUS reads `agents/design/arc-24/design.md` to articulate the gap (worktree-path discipline for DAEDALUS Edit-tool usage); CAPTAIN_DAEDALUS.md substrate-touch shape determined at design time.
- **A5 DAEDALUS-discretion (dhc)**: canonical location for single-source-of-truth lift. Options:
  - **(α)** op-disc §18 (or wherever Arc 24 landed the universal subagent-status section) sub-section
  - **(β)** new `substrate/templates/canonical-poll-loop.md` doc
  - User-tier leans α (keeps prose adjacent to other op-disc discipline canon; avoids new template file when prose lift suffices). DAEDALUS picks.
- **A6 DAEDALUS-discretion (3sz)**: probe-discipline placement. Options:
  - **(γ)** CAPTAIN_VERA.md probe-authoring section
  - **(δ)** op-disc subsection on probe-discipline
  - User-tier leans γ (probe-authoring is VERA-specific; lives at VERA seat-canon). DAEDALUS picks.
- **A7 DAEDALUS-discretion (fold-in)**: opportunistic 6n9 + t9u fold-in. Both touch install.sh discipline (6n9 = manifest format-version header; t9u = pycache exclusion). User-tier weakly leans include — both are small (≤30 LOC each), install.sh-adjacent, and saves separate arc-cycles. DAEDALUS picks based on scope-cohesion judgment at design time.

### Universal (continued from Arc 39)
- **A8 LOCKED**: §28 Co-Authored-By trailers per Arc 35 canon — all ADA + DAEDALUS commits inside arc-40/build MUST carry trailers. Phase 4 squash-merge MUST NOT use `--body` override per the discipline this arc is shipping (recursive self-application).
- **A9 LOCKED**: §5.10 signoff with live-verified state per §19.6 attestation-honesty. Cite live-verified state at attestation time; never echo dispatch-authoring SHA.
- **A10 LOCKED**: `[from: pliny-the-stoa]` author tag on PLINY heartbeats; `[from: polybius-the-stoa]` on POLYBIUS_the_stoa; cross-tier `[for: user-tier-polybius] [from: <self>]`. Per Arc 36 §7.1/§7.7.
- **A11 LOCKED**: cron infrastructure REUSE existing (POLYBIUS: `b6e8630b` polling + `3c1e575b` renewal; PLINY: `abc905a6` polling + `6e69c60a` renewal). DO NOT recreate.
- **A12 LOCKED**: cite-comment discipline per Arc 38 A17 — every cross-ref between MAJOR_PLINY.md §5.10 + op-disc §28.3.1 (if A3 includes) + CAPTAIN_DAEDALUS.md (5sr) + dhc canonical location + cross-refs from other sites must resolve via cite at every read-site.
- **A13 LOCKED**: A18 IMMUTABLE — Arc 40 ships canon-edits + optional install.sh changes; no new substrate skill SKILL.md files in LOCKED scope (so no new author-frontmatter audit targets). If 6n9 manifest format-version requires a new format-spec doc and DAEDALUS chooses to ship it as a substrate-canon file with frontmatter, the `author: Denson Smith` rule applies.
- **A14 LOCKED**: A19 source-ticket closure — on Arc 40 ship, close 3sz + 5sr + dhc + 6wp (+ 6n9 + t9u if folded) with cross-refs to merge commit + audit comments per candidate. Tag `[for: user-tier-polybius]` on stoa--utn (continuing as dispatch ticket).
- **A15 LOCKED**: A20 pre-branch hygiene per §5.9 + worktree at `.claude/worktrees/arc-40-build/` per §5.9.4. Pre-flight two-check rule.
- **A16 LOCKED**: out-of-scope hard-locks (Arc 40-specific):
  - No restructuring MAJOR_PLINY.md §5.10 beyond the 1-line ship-checklist addition (per 6wp ticket scope).
  - No introducing new substrate skills.
  - No retroactive sweep of OTHER substrate SKILL.md files beyond Arc 39 M3 widening already shipped (sp1 scope).
  - No widening dhc lift to non-poll-loop template consolidations.
  - No widening 3sz probe-discipline to non-probe authoring guidance.
  - No widening 5sr beyond what `agents/design/arc-24/design.md` flagged.
  - If 6n9/t9u folded: no widening beyond the literal ticket scopes.
- **A17 LOCKED**: CATO MANDATORY per sequence rationale (Pass 9 validate-spec imminent in Arc 42; cumulative craft scrutiny matters).

### Arc-shaping (continued from Arc 39)
- **A18 LOCKED**: bw-signal dispatch model — Arc 40 dispatched via bw comment on stoa--utn (`[for: pliny-the-stoa]` + `[for: polybius-the-stoa]` tags); both seats engaged via priming-set polling crons. At close, PLINY comments back on stoa--utn with `[for: user-tier-polybius]` clean-PASS verdict. §5.11 archival of the 3 Arc 40 files (directive + 2 activation pastes) to `substrate/arcs/arc-40/pastes/` via git mv.

### Sequence-critical + recursive-shape calls
- **A19 LOCKED**: **6wp is SEQUENCE-CRITICAL.** Must ship before Pass 9 / Pass 10 stellation dispatch per §13.7. After Arc 40 ships clean, the trailer-discipline canon is in MAJOR_PLINY.md §5.10 + (optionally) op-disc §28.3.1, codifying what Arc 38 + Arc 39 already practiced organically. This closes the bb12806 empirical-anchor loop.
- **A20 LOCKED**: **6wp recursive-shape surveillance.** PLINY is editing PLINY's own role file (§5.10 ship-checklist addition) pre-merge as part of an arc that PLINY runs end-to-end. DAEDALUS designs the edit; ADA implements; ARGUS+CATO+VERA review; PLINY ships per §5.10 (the very checklist being edited). Watch for: (a) the edit committed to arc-40/build pre-merge, (b) the deployed file at user-tier after Arc 40 ships matches the substrate-tier source, (c) PLINY's own Arc 40 Phase 4 signoff cites the new §5.10 wording correctly (self-application of the new canon during the arc that ships it). Surface as substance disagreement if circularity reveals an issue not foreseen.

## DAEDALUS sub-decisions summary

| ID | Decision | User-tier lean | DAEDALUS picks at design |
|---|---|---|---|
| A3 | 6wp op-disc §28.3.1 pitfall worked-example | include | yes |
| A4 | 5sr specific failure mode framing | n/a (DAEDALUS reads Arc 24 design.md) | yes |
| A5 | dhc canonical location | α (op-disc subsection) | yes |
| A6 | 3sz probe-discipline placement | γ (CAPTAIN_VERA.md) | yes |
| A7 | 6n9 + t9u fold-in | weakly include | yes |

Each is DAEDALUS-discretion UNLESS exceeding (e.g., A4 design.md reveals failure mode larger than CAPTAIN_DAEDALUS.md scope; A5 lift reveals dhc canon spans MULTIPLE op-disc sections requiring §-restructure; A7 fold-in turns out to require non-trivial install.sh refactor) — surface PRINCIPAL-gate per §25.

## Self-application observations to watch for stoa--bbi accretion

- **A19/A20 self-applied recursion** — Arc 40 ships the trailer-discipline canon (6wp) and ALSO must comply with it (Phase 4 squash-merge). Watch for circularity-surprise; note as N-evidence whether self-applied disciplines hold organically (Arc 38 + Arc 39 both shipped trailer-clean BEFORE 6wp canon was written — so the canon codifies what worked, vs. requiring discovery).
- **A7 fold-in** — if DAEDALUS folds 6n9 + t9u, that's 6 candidates in one arc (matches Arc 37 precedent at 6 candidates). Observe whether the bundle stays coherent or DAEDALUS surfaces scope-disagreement mid-design.

## Ship gate

Arc 40 ships when:
- design.md cleared by ARGUS (rev cycles per DAEDALUS judgment)
- ADA build complete; ZENO PASS on mechanical checks (A8 trailers / file-existence / install.sh wiring if folded)
- VERA falsification PASS on all probes
- CATO craft + scope review PASS
- Phase 4: squash-merge with trailer preservation (the canon this arc ships; self-applied)
- §5.10 signoff with live-verified state
- Source tickets closed per A14; `[for: user-tier-polybius]` tag on stoa--utn
