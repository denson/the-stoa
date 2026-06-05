Read .claude/MAJOR_PLINY.md and assume the orchestrator role for the-stoa.

Your immediate intent for this session: Build Arc 33 per the build directive at substrate/arcs/arc-33-build-directive.md. Substantive multi-file substrate arc + new substrate component (per DAEDALUS pick at A2/A3): the **mechanical-script / agent-inspection split** — structural enforcement layer for Arc 31's §25 PRINCIPAL-gate prose discipline. Work-unit ticket: **stoa--32b.2** (P2).

**PRECONDITION:** Arc 32 (stoa--ewn) is CLOSED. the-stoa main at `84f1f86`. Local main = origin/main + no orphan arc-build branches verified by user-tier POLYBIUS at dispatch authoring.

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

**Worktree convention per Arc 32 §5.9.4 (directive A9):** create arc-33/build in separate worktree: `git worktree add .claude/worktrees/arc-33-build arc-33/build`. Main worktree stays on main. User-tier POLYBIUS can operate concurrently without checkout collision.

**Read first (in order):**

1. **`substrate/arcs/arc-33-build-directive.md`** — load-bearing spec. A1-A10 LOCKED architectural decisions. Primary input alongside ticket.
2. **`bw show stoa--32b.2`** — work-unit ticket body + 2026-05-17 scope-refresh comment (carries intervening-arc context). BOTH required.
3. **`docs/sessions/2026-05-16-substrate-update-architecture-reframe--retro.md` §8** — LOAD-BEARING source for the 3-step pattern. DAEDALUS treats as primary prose input.
4. **`HUMAN_paste-polybius-arc-33-instruction.md`** in the project root — POLYBIUS's activation paste; same content frame.
5. **`substrate/operating-disciplines.md` §25** (Arc 31 PRINCIPAL-gate; what this arc enforces mechanically) + **§19.6** (Arc 32 attestation-confabulation) + **§17 / §23** (Arc 29 base-vs-custom; inspection must respect).
6. **`substrate/MAJOR_PLINY.md` §5.10** (Arc 32 signoff-accuracy) + **§5.9 / §5.9.4** (Arc 30 + Arc 32; self-applied).
7. **`substrate/skills/check-bw-release/`** (Arc 28; small inspection-shape skill PRECEDENT) + **`substrate/skills/check-substrate-updates/`** (Arcs 26 + 29; the script-bloat NEGATIVE anchor).
8. **`substrate/install.sh` SKILL_NAMES** — A2 Option α requires append.

Operating mode for this dispatch: AUTONOMOUS. Run all four phases heads-down (Phase 1 DAEDALUS + ARGUS — REVISIONS LIKELY given architecture-sensitivity + multiple DAEDALUS picks; Phase 2 ADA build in .claude/worktrees/arc-33-build/ per §5.9.4; Phase 3 VERA + CATO + ZENO; Phase 4 smoke + PR + merge + close). Use stoa--32b.2 for status updates. Surface to PRINCIPAL ONCE at end-of-arc with final clean-PASS verdict.

Coordination: the-stoa PROJECT-TIER POLYBIUS is your radio-check peer (paste at HUMAN_paste-polybius-arc-33-instruction.md). User-tier POLYBIUS dispatched + will do QA pass at arc close. Bidirectional radio-check pattern per substrate/operating-disciplines.md §7.

The architectural decisions A1-A10 are LOCKED in the directive. DAEDALUS treats stoa--32b.2 body + 2026-05-17 scope-refresh comment + retro §8 as primary input alongside the directive. Locked decisions encode: one-arc one-gauntlet (A1); substrate-component-shape pick α/β/γ (A2 — lean Option α new skill); skill naming + worked-example domain (A3 — lean inspect-script-output, substrate-update flow domain); operating-disciplines.md pattern documentation (A4); cross-refs (A5); authorship (A6); out-of-scope hard-locked (A7); §15 N=1 honesty per refresh comment empirical anchors (A8); pre-branch + worktree-convention self-applied (A9); signoff-accuracy + attestation-honesty self-applied (A10).

**DAEDALUS sub-decisions:**
- **A2:** Option α (new skill) vs β (CAPTAIN_VERA extension) vs γ (new CAPTAIN seat). User-tier POLYBIUS leans α. If you pick differently, document rationale in design.md.
- **A3:** skill naming (lean `inspect-script-output`) + worked-example domain (LOCKED to substrate-update flow).
- **A4:** operating-disciplines.md insertion locus (near §11 or new top-level after §26).

If any sub-decision surfaces as needing PRINCIPAL judgment rather than DAEDALUS discretion, treat as PRINCIPAL-gate per §25 (BLOCK not TAG) — halt + escalate immediately.

**Cite-comment discipline per A5:** cross-refs between new substrate component + §25 / §19.6 / §5.10 / §17 + new operating-disciplines.md section must resolve via cite at every read-site. Same pattern as Arc 26 / 28 / 29 / 30 / 31 / 32 cite-comments.

**CATO is MANDATORY** for this arc (substrate canon + new substrate skill; wording precision matters; this is the substrate's biggest architectural arc remaining).

Authorship attribution is IMMUTABLE per substrate/CLAUDE.md: all edits credit Denson Smith. Arc 33 ADDS NEW skill files (per A6 if Option α picked). SKILL.md frontmatter MUST carry `author: Denson Smith` per Arc 27 stoa--uly convention. Verify ALL new files before commit.

**Phase 4 close handshake per Arc 32 §5.10:**
- Verify cleanup actually executed (arc-33/build local + remote deleted; worktree removed; PR merged)
- Verify each verification via live state inspection (not assumption-from-context per §19.6)
- Post `[for: user-tier POLYBIUS]` comment on stoa--32b.2 inviting QA pass

**Self-referential note:** Arc 33 is the structural enforcement layer for Arc 31's §25 prose discipline. The inspection-agent component you ship will be how future arcs MECHANICALLY verify what current arcs RELY ON AGENT RECOGNITION for. Strongest substrate-shaping arc remaining at the-stoa. Same self-referential dynamic as Arcs 24-32.

Check beadwork (stoa-- prefix) — start with: stoa--32b.2 (the work-unit; substrate/arcs/arc-33-build-directive.md is its load-bearing artifact, on disk at dispatch authoring time, will commit as part of arc-33/build feature branch).

If compaction or /clear erases your role, re-read this paste from HUMAN_paste-pliny-arc-33-instruction.md in the project root.
