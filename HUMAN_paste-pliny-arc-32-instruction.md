Read .claude/MAJOR_PLINY.md and assume the orchestrator role for the-stoa.

Your immediate intent for this session: Build Arc 32 per the build directive at substrate/arcs/arc-32-build-directive.md. Medium-scope canonification batch: 5 small discipline tightenings (C1-C5). Work-unit ticket: **stoa--ewn** (P2).

**PRECONDITION:** Arc 31 (stoa--32b.1) is CLOSED. the-stoa main at `e315ca9`. Local main = origin/main + no orphan arc-build branches verified by user-tier POLYBIUS at dispatch authoring.

Cron hygiene FIRST (before any substantive work): this session may carry an orphaned cron from a prior /clear'd context. Run CronList; if any cron is present, CronDelete it. PLINY typically uses surface-and-wait per MAJOR_PLINY.md §6.2 (no cron); defense-in-depth.

Pre-branch hygiene per MAJOR_PLINY.md §5.9: before creating arc-N/build, run two checks.

Check 1 (no other arc-build branch in flight):
  git branch | grep -E '^\s*arc-[0-9]+/build$'    # must be empty

Check 2 (local main = origin/main):
  git fetch origin main
  git log --oneline main..origin/main             # must be empty
  git log --oneline origin/main..main             # must be empty

If either check fails, surface to user-tier POLYBIUS (or PRINCIPAL via [for: PRINCIPAL]
tag when user-tier unavailable) with the specific state observed. Do NOT silently
inherit local-ahead commits into the arc branch (bundled-squash pattern surfaced
on 2026-05-17 as stoa--3cs).

**Read first (in order):**

1. **`substrate/arcs/arc-32-build-directive.md`** — load-bearing spec. A1-A11 LOCKED architectural decisions. Primary input alongside ticket.
2. **`bw show stoa--ewn`** — work-unit ticket body (C1-C4) + the 2026-05-17 C5 scope-addition comment (worktree convention). Both required.
3. **`HUMAN_paste-polybius-arc-32-instruction.md`** in the project root — POLYBIUS's activation paste; same content frame.
4. **`substrate/MAJOR_POLYBIUS.md` §5.1 area** — C1 + C2 source-of-truth + paste convention.
5. **`substrate/MAJOR_PLINY.md` §5.9** — C3 + C5 locus candidates.
6. **`substrate/operating-disciplines.md` §19** — C4 extends; §24 (Arc 30 thin cross-ref) for C2 cross-ref pattern model.
7. **`substrate/templates/paste-instruction-template.md`** — C2 adds {{CRON_HYGIENE_CLAUSE}} slot.
8. **Recent activation pastes** at the-stoa root — observe the ad-hoc cron-hygiene preamble C2 canonifies.

Operating mode for this dispatch: AUTONOMOUS. Run all four phases heads-down (Phase 1 DAEDALUS + ARGUS — revisions expected given 5 candidates; Phase 2 ADA build on arc-32/build; Phase 3 VERA + CATO + ZENO; Phase 4 smoke + PR + merge + close). Use stoa--ewn for status updates. Surface to PRINCIPAL ONCE at end-of-arc with final clean-PASS verdict.

Coordination: the-stoa PROJECT-TIER POLYBIUS is your radio-check peer (paste at HUMAN_paste-polybius-arc-32-instruction.md). User-tier POLYBIUS dispatched + will do QA pass at arc close. Bidirectional radio-check pattern per substrate/operating-disciplines.md §7.

The architectural decisions A1-A11 are LOCKED in the directive. DAEDALUS treats stoa--ewn body + C5 scope-addition comment as primary input alongside the directive. Locked decisions encode: one-arc one-gauntlet (A1); per-candidate scoping for C1 (A2), C2 three-carrier mirror of Arc 30 (A3), C3 locus pick α/β (A4), C4 §19 extension (A5), C5 worktree Option A vs B (A6); cite-comment discipline (A7); authorship (A8); out-of-scope hard-locked (A9); §15 N=1 per-candidate (A10); pre-branch hygiene self-applied (A11).

**DAEDALUS sub-decisions per A4 + A6:**
- **A4 C3 locus:** Option α (MAJOR_PLINY.md alongside §5.9) vs Option β (operating-disciplines.md universal-team). User-tier POLYBIUS leans α; DAEDALUS picks.
- **A6 C5 worktree convention:** Option A (require separate worktree) vs Option B (explicit allow main-worktree checkout). User-tier POLYBIUS leans A; DAEDALUS picks.

If either pick surfaces as needing PRINCIPAL judgment rather than DAEDALUS discretion, treat as PRINCIPAL-gate per §25 (BLOCK not TAG) — halt + escalate immediately.

**Cite-comment discipline per A7:** cross-references between C1-C5 + adjacent canon (Arc 30 §5.9 for C5; §19 for C4) should resolve via cite at every read-site. Same pattern as Arc 26 / 28 / 29 / 30 / 31 cite-comments.

**CATO is MANDATORY** for this arc (substrate canon work across 5 candidates; wording precision matters; future POLYBIUSes read this for life-of-the-substrate).

Authorship attribution is IMMUTABLE per substrate/CLAUDE.md.

**Phase 4 close handshake:** tag `[for: user-tier POLYBIUS]` comment on stoa--ewn inviting QA pass.

**Self-referential note:** Arc 32 canonifies disciplines that have been carrying the substrate ad-hoc across today's session. C2 cron-hygiene was paste-author memory since Arc 26; C3 PLINY-signoff-accuracy was empirically anchored by Arc 29's inaccurate signoff that Arc 31's PLINY corrected; C4 attestation-confabulation was empirically anchored by Arc 30's PLINY init-handshake SHA echo; C5 worktree convention was empirically anchored by Arc 31's main-worktree checkout flip. All five disciplines move from ad-hoc-pattern to substrate-canon in one arc.

Check beadwork (stoa-- prefix) — start with: stoa--ewn (the work-unit; substrate/arcs/arc-32-build-directive.md is its load-bearing artifact, on disk at dispatch authoring time, will commit as part of arc-32/build feature branch).

If compaction or /clear erases your role, re-read this paste from HUMAN_paste-pliny-arc-32-instruction.md in the project root.
