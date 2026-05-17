Read .claude/MAJOR_PLINY.md and assume the orchestrator role for the-stoa.

Your immediate intent for this session: Build Arc 34 per the build directive at substrate/arcs/arc-34-build-directive.md. Small-to-medium canonification batch: 4 small discipline tightenings (C1-C4) bundled as stoa--y14 (P2).

**PRECONDITION:** Arc 33 (stoa--32b.2) is CLOSED. the-stoa main at `789496b`. Local main = origin/main + no orphan arc-build branches verified by user-tier POLYBIUS at dispatch authoring.

Cron hygiene FIRST (before any substantive work): Run CronList; if any cron is present, CronDelete it. Surface-and-wait per MAJOR_PLINY.md §6.2 (no cron) is the default for PLINY; defense-in-depth.

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

**Worktree convention per Arc 32 §5.9.4 (directive A10):** create arc-34/build in separate worktree: `git worktree add .claude/worktrees/arc-34-build arc-34/build`. Main worktree stays on main.

**Read first (in order):**

1. **`substrate/arcs/arc-34-build-directive.md`** — load-bearing spec. A1-A12 LOCKED architectural decisions.
2. **`bw show stoa--y14`** — work-unit ticket bundling C1-C4. Primary input alongside directive.
3. **Source tickets folded as candidates:**
   - `bw show stoa--k36` (C1)
   - `bw show stoa--f37` (C2)
   - `bw show stoa--3qi` (C3)
   - `bw show stoa--ize` (C4 source)
4. **`HUMAN_paste-polybius-arc-34-instruction.md`** in the project root — POLYBIUS's activation paste; same content frame.
5. **`substrate/MAJOR_POLYBIUS.md`** — current sections; C1 + C4 candidate loci.
6. **`substrate/MAJOR_PLINY.md` §5.9 + §5.10** — pre-branch + signoff-accuracy; C2 lives alongside.
7. **`substrate/templates/paste-instruction-template.md`** — C3 title fix; C4 candidate locus.
8. **`substrate/templates/handoff-doc-template.md`** — C4 candidate locus.
9. **`substrate/arcs/arc-32-build-directive.md`** — stoa--ewn precedent for bundling shape.

Operating mode for this dispatch: AUTONOMOUS. Run all four phases heads-down. Use stoa--y14 for status updates. Surface to PRINCIPAL ONCE at end-of-arc with final clean-PASS verdict.

Coordination: the-stoa PROJECT-TIER POLYBIUS is your radio-check peer (paste at HUMAN_paste-polybius-arc-34-instruction.md). User-tier POLYBIUS dispatched + will do QA pass at arc close. Bidirectional radio-check pattern per substrate/operating-disciplines.md §7.

The architectural decisions A1-A12 are LOCKED in the directive. DAEDALUS treats stoa--y14 body as primary input alongside the directive. Locked decisions encode: one-arc one-gauntlet (A1); C1 user-tier-to-main with Option A/B/C pick (A2); C2 paste accumulation with Option α/β/γ pick (A3); C3 template-title cosmetic (A4); C4 HITL-paused queue sweep with Option α/β/γ pick (A5); cite-comments (A6); authorship (A7); out-of-scope hard-locked (A8); §15 N=1 per-candidate (A9); pre-branch + worktree-convention self-applied (A10); signoff-accuracy + attestation-honesty self-applied (A11); source-ticket closure (A12).

**DAEDALUS sub-decisions:**
- **A2 C1:** Option A (discipline section only) vs B (strict, never to main — too restrictive) vs C (composite: section + CLAUDE.md update). User-tier POLYBIUS leans C.
- **A3 C2:** Option α (archive on arc close) vs β (delete on arc close) vs γ (leave + accept). User-tier POLYBIUS leans α.
- **A5 C4:** Option α (POLYBIUS activation checklist) vs β (handoff-doc-template section) vs γ (both — defense in depth). User-tier POLYBIUS leans γ.

If any pick surfaces as needing PRINCIPAL judgment rather than DAEDALUS discretion, treat as PRINCIPAL-gate per §25 — halt + escalate immediately.

**Cite-comment discipline per A6:** cross-references between C1-C4 + adjacent canon (§5.9 + §5.10 for C2; §9 activation for C4; existing CLAUDE.md for C1) should resolve via cite. Same pattern as Arc 26 / 28 / 29 / 30 / 31 / 32 / 33 cite-comments.

**CATO is MANDATORY** for this arc (substrate canon work across 4 candidates; wording precision matters).

Authorship attribution is IMMUTABLE per substrate/CLAUDE.md.

**Phase 4 close handshake per §5.10 + A12:** verify cleanup actually executed; cite live-verified state in attestations; close stoa--y14 + source tickets (stoa--k36 + stoa--f37 + stoa--3qi + stoa--ize) each with cross-ref to merge commit; tag `[for: user-tier POLYBIUS]` on stoa--y14 inviting QA pass.

**Self-referential note:** Arc 34 canonifies disciplines that surfaced via today's stoa--ize sweep. C1 (user-tier-to-main) literally describes user-tier POLYBIUS direct-commit behavior the substrate hasn't yet documented. C4 (HITL-paused queue sweep) is the discipline that would have surfaced stoa--jru (Arc 22) much earlier had it been canon. Same substrate-shaping shape as Arcs 24-33.

Check beadwork (stoa-- prefix) — start with: stoa--y14 (the work-unit; substrate/arcs/arc-34-build-directive.md is its load-bearing artifact, on disk at dispatch authoring time, will commit as part of arc-34/build feature branch).

If compaction or /clear erases your role, re-read this paste from HUMAN_paste-pliny-arc-34-instruction.md in the project root.
