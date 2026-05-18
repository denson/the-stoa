# Arc 41 build directive — Pass 7 substrate bundle (4 candidates: n2e + 58b + 3ml + pqn)

## Context

Arc 41 is Pass 7 of SPECIFICATION.md §13 workplan — the FINAL arc in the make-the-team-meet-the-spec sequence before Pass 8 reconciliation + Pass 9 validate-spec mechanical-check. Theme per §13.8: cross-references + audits + Arc 36 follow-ups; tight bundle of small canon-edits.

**Four LOCKED candidates** (ezp absorbed by Arc 39 M3 widening, dropped from §13.8 enumeration):
- **C1: stoa--n2e (P3)** — substrate cross-ref add: MAJOR_POLYBIUS.md escalation triggers → operating-disciplines.md §20.3 (refusal-as-signal)
- **C2: stoa--58b (P3)** — substrate cross-ref add: MAJOR_PLINY.md dispatch section (§5 or §6) → operating-disciplines.md §20 (credential discipline)
- **C3: stoa--3ml (P4)** — trivial 1-sentence edit: operating-disciplines.md Thesis line 13 references `§1-§17` — UPDATE to current section range (substrate now has §1-§31 post-Arc-38 §31 add; DAEDALUS verifies current count at design time)
- **C4: stoa--pqn (P4)** — Arc 36 v2 follow-ups (3 items): VERA probe-regex tightening (5 items in arc-36 VERA verdict; design.md edit at agents/design/stoa--jru/ OR equivalent), bug #40228 surveillance note, organic `[from:]` adoption observation

**After Arc 41 ships: zero open P2 substrate-canon tickets at the-stoa** per §13.8 (this gate is currently already true; Arc 41 ship maintains it).

## What's explicitly OUT of Arc 41 scope

- **stoa--mn3** (Arc 40 VERA methodology concerns; design.md probe-spec fixes for agents/design/arc-40/design.md). PLINY-lean per the ticket body is α direct-to-main housekeeping commit per `MAJOR_POLYBIUS.md` §18.1 user-tier lane (design.md is past its review window; cleanest as separate housekeeping commit). user-tier POLYBIUS handles separately after Arc 41 close.
- All A20 hard-locks from Arc 39 + Arc 40 continue to apply.

## Architectural decisions A1-A18 (LOCKED unless flagged DAEDALUS-discretion)

### Bundle structure
- **A1 LOCKED**: single design.md document covering all 4 candidates. Per Arc 37/38/39/40 precedent. Sections per candidate + universal §28/§5.10/§5.11 disciplines.

### Per-candidate scope
- **A2 LOCKED (n2e)**: cross-ref text added to MAJOR_POLYBIUS.md escalation-triggers section. DAEDALUS picks exact wording + insertion locus; sub-paragraph or bullet form acceptable. Target: §20.3 refusal-as-signal canon.
- **A3 LOCKED (58b)**: cross-ref text added to MAJOR_PLINY.md §5 (gauntlet pipeline) or §6 (Communication) — DAEDALUS picks which section based on dispatch-brief-authoring locus. Target: op-disc §20 credential discipline.
- **A4 LOCKED (3ml)**: 1-sentence edit at operating-disciplines.md Thesis line 13. **DAEDALUS verifies current section count at design time** (substrate currently has §1-§31 post-Arc-38 §31 add; ticket text "§1-§20" was authored post-Arc-25 and is now itself stale). Final wording: `§1-§<N>` where N matches current file structure.
- **A5 DAEDALUS-discretion (pqn 3 items)**: per-item scope per ticket:
  - **Item 1**: VERA probe-regex tightening — read VERA verdict for arc-36 (`agents/verdicts/stoa--jru/CAPTAIN_VERA-*.md` OR equivalent path; DAEDALUS locates), enumerate 5 items, refine probes in arc-36 design.md. **OR α direct-to-main housekeeping** per §18.1 (design.md edits — same lane mn3 takes). DAEDALUS picks ε in-arc-build (PLINY-lean since this is a multi-edit refinement that benefits from gauntlet review) vs. ζ direct-to-main (lower friction; consistent with mn3 routing). User-tier weakly leans ε in-arc-build for craft scrutiny.
  - **Item 2**: bug #40228 surveillance — add a 1-line cross-ref in op-disc §11 step 1.5 (or equivalent renewal-cron canon site) noting bug-watch state without baking in a recovery-discipline canon change (the watch is observation-only until Anthropic fixes upstream). DAEDALUS picks placement.
  - **Item 3**: organic `[from:]` adoption observation — file an observation comment on stoa--myd (multi-checker convergence accretion P4) OR a fresh observation ticket capturing the Arc 36-37-38-39-40 organic adoption pattern. NOT a canon-promotion in this arc (per pqn ticket Item 3 "low priority" + A2.5 hard-locked scope intentionally). Observation-only.

### Universal (continued from Arc 39 + Arc 40)
- **A6 LOCKED**: §28 Co-Authored-By trailers per Arc 35 canon — all ADA + DAEDALUS commits inside arc-41/build MUST carry trailers. Phase 4 squash-merge MUST follow MAJOR_PLINY.md §5.10 squash-merge-`--body` discipline shipped Arc 40 (no `--body` override OR include trailers in HEREDOC).
- **A7 LOCKED**: §5.10 signoff with live-verified state per §19.6 attestation-honesty.
- **A8 LOCKED**: `[from: pliny-the-stoa]` author tag on PLINY heartbeats; `[from: polybius-the-stoa]` on POLYBIUS_the_stoa; cross-tier `[for: user-tier-polybius] [from: <self>]`. Per Arc 36 §7.1/§7.7.
- **A9 LOCKED**: cron infrastructure REUSE existing (POLYBIUS: `b6e8630b` polling + `3c1e575b` renewal; PLINY: `abc905a6` polling + `6e69c60a` renewal). DO NOT recreate.
- **A10 LOCKED**: cite-comment discipline per Arc 38 A17 / Arc 39 / Arc 40 — every cross-ref between MAJOR_POLYBIUS.md escalation-triggers (n2e) + MAJOR_PLINY.md §5/§6 (58b) + op-disc Thesis line 13 (3ml) + Arc 36 design.md edits (pqn item 1) + op-disc §11 step 1.5 (pqn item 2) must resolve via cite at every read-site.
- **A11 LOCKED**: A18 IMMUTABLE — Arc 41 ships canon-edits + cross-refs; no new substrate skill SKILL.md files. No A18 targets unless pqn Item 3 organic-adoption observation creates a new substrate-canon file with frontmatter (unlikely; observation-comment-on-ticket is the lighter shape).
- **A12 LOCKED**: A19 source-ticket closure — on Arc 41 ship, close stoa--n2e + stoa--58b + stoa--3ml + stoa--pqn with cross-refs to merge commit + audit comments per candidate. Tag `[for: user-tier-polybius]` on stoa--utn (continuing as dispatch ticket through end of sequence).
- **A13 LOCKED**: A20 pre-branch hygiene per §5.9 + worktree at `.claude/worktrees/arc-41-build/` per §5.9.4. Pre-flight two-check rule.
- **A14 LOCKED**: out-of-scope hard-locks (Arc 41-specific):
  - No restructuring MAJOR_POLYBIUS.md escalation-triggers section beyond the n2e cross-ref add.
  - No restructuring MAJOR_PLINY.md §5/§6 beyond the 58b cross-ref add.
  - No editing op-disc Thesis beyond the line-13 sentence-level edit.
  - No widening pqn Item 3 organic-adoption observation into A2.5 scope expansion (explicit hard-lock per pqn ticket — A2.5 hard-locked intentionally).
  - No mn3 work (PLINY-lean is α direct-to-main per ticket body; user-tier handles post-Arc-41).
  - No introducing new substrate skills or canon sections.

### Arc-shaping (continued)
- **A15 LOCKED**: CATO MANDATORY per sequence rationale (Pass 9 validate-spec imminent next; Arc 41 is last canon-edit gauntlet before mechanical-check arc).
- **A16 LOCKED**: bw-signal dispatch model — Arc 41 dispatched via bw comment on stoa--utn with `[for: pliny-the-stoa]` + `[for: polybius-the-stoa]` tags. §5.11 archival of the 3 Arc 41 files (directive + 2 activation pastes) to `substrate/arcs/arc-41/pastes/` via git mv. **Wording clarification per Arc 40 POLYBIUS observation**: directive itself stays at `substrate/arcs/arc-41-build-directive.md` (NOT archived to pastes/ subdirectory); only HUMAN_paste-* one-time activation files get archived. (Pass 8 reconciliation will codify this in §5.11 canon wording if drift class persists.)

## DAEDALUS sub-decisions summary

| ID | Decision | User-tier lean | DAEDALUS picks at design |
|---|---|---|---|
| A5 Item 1 | pqn VERA probe-regex tightening lane | ε in-arc-build | yes |
| A5 Item 2 | pqn bug #40228 surveillance placement | DAEDALUS picks | yes |
| A5 Item 3 | pqn organic-adoption observation routing | observation-comment-on-ticket | yes |

Each is DAEDALUS-discretion UNLESS exceeding (e.g., pqn Item 1 spike reveals 5 items aren't bounded; pqn Item 3 reveals organic adoption HAS broken something requiring A2.5 scope revisit). Then surface as PRINCIPAL-gate per §25.

## Self-application observations to watch for stoa--bbi accretion

Arc 41 is the FINAL canon-edit arc before Pass 9 validate-spec. Observations to note:
- **Cross-ref completeness propagation**: do all 4 cross-refs land with reciprocating cites resolving at every read-site (per A10)?
- **Tightness pattern**: this is the smallest arc in the sequence (mostly 1-line cross-refs). Watch whether ARGUS/CATO find rev cycles on tight scope OR clean PASS-first reflects tighter directive design.
- **Sequence-end hygiene**: end-of-sequence verdict from POLYBIUS_the_stoa should observe whether the multi-arc autonomous-engagement cron-driven dispatch model held cleanly across all 3 arcs (39+40+41) — proto-canon-promotion case for the polling-cron-as-PLINY-default departure from §6.2 noted in priming.

## Ship gate

Arc 41 ships when:
- design.md cleared by ARGUS (rev cycles per DAEDALUS judgment; expect 0-1 cycle on tight scope)
- ADA build complete; ZENO PASS on mechanical checks
- VERA falsification PASS on probes
- CATO craft + scope review PASS
- Phase 4: squash-merge per MAJOR_PLINY.md §5.10 §28 trailer-preservation canon (no `--body` override)
- §5.10 signoff with live-verified state
- Source tickets closed per A12; `[for: user-tier-polybius]` tag on stoa--utn

**After Arc 41 ships clean** + user-tier QA pass → user-tier POLYBIUS runs Pass 8 spec-reconciliation (direct-to-main per §18.1) + drift sweep verification (§13.13 criterion 4 across ariadne/sector-4/railway) + handles mn3 (α direct-to-main per its own ticket-body lean) + handles pqn Item 1 if DAEDALUS picked ζ direct-to-main routing → then Pass 9 validate-spec directive authored for PRINCIPAL ratification before Arc 42 dispatch.
