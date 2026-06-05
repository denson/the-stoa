Read .claude/MAJOR_POLYBIUS.md and assume the project-tier chief-of-staff role for the-stoa.

Your immediate intent for this session: stand up as POLYBIUS peer for Arc 28 (substrate adoption of bw 0.13.0 features + bw-upgrade discipline encoding). PLINY is being activated in a separate session shortly. Coupled work-unit ticket: **stoa--s6n** (P1; B.1-B.4 substrate adoption + C.1 discipline doc + C.2 check-bw-release skill).

Your job is the radio-check counterpart per substrate/operating-disciplines.md §7 — read the directive + ticket, post init handshake, then poll on cadence; surface to PRINCIPAL only on autonomous escalation triggers (substance disagreement after one round of bw exchange with PLINY, authorship/copyright/Denson-final-say content, irreducible ambiguity, PLINY silent > 60 min, end-of-arc clean-PASS for ship/no-ship).

**Cron hygiene FIRST (before any substantive work):** this session is fresh. If your terminal previously hosted a different session, it may carry an orphaned cron. Run `CronList`; if any cron is present, CronDelete it. Step 2: set up fresh cron at `*/5 * * * *` (substrate-canonical default per operating-disciplines.md §7.2). Step 3: name the new cron id in your init handshake on stoa--s6n.

**Read first (in order):**

1. **`substrate/arcs/arc-28-build-directive.md`** — the load-bearing spec. A1-A8 LOCKED architectural decisions; phasing table; reads-list; VERA probes; smoke beats. Medium-scope substrate-canon arc.
2. **`bw show stoa--s6n`** — work-unit ticket. Body carries problem + Part B (B.1-B.4) + Part C (C.1-C.2) + 7 deliverables + acceptance + hard-locked out-of-scope + §15 N=1 caveat. Primary input alongside the directive.
3. **`bw show ariadne--c71`** (cross-tier read; ariadne-core-workspace bw store) — the empirical anchor for the bw-upgrade-discipline. The deployment-side worked example. Shipped at ariadne-core main `b7f92e5` earlier today.
4. **`HUMAN_paste-pliny-arc-28-instruction.md`** in the project root — PLINY's activation paste; same content frame.
5. **`substrate/skills/check-substrate-updates/`** — the existing skill PLINY extends (B.1 modifies check.sh; C.2 mirrors the skill's structural shape for the new check-bw-release).
6. **`substrate/consumer-workspaces.txt`** — current registry; deprecated by B.1 (with comment header, file kept for one release per A4).

**Operating mode:**

- AUTONOMOUS with radio-check protocol per substrate/operating-disciplines.md §7.
- USER-TIER POLYBIUS dispatched this arc + will do QA pass at arc close per PRINCIPAL's 2026-05-16 pattern ("hand off to the full team with their own polybius to do the changes and you check for mistakes at the end").
- On init: post handshake comment on stoa--s6n confirming directive + ticket + ariadne--c71 cross-ref read, naming polling cron id + cadence.
- Per-phase heartbeat one-line state on stoa--s6n as PLINY progresses.
- Closure handshake on stoa--s6n close. PLINY tags `[for: user-tier POLYBIUS]` invitation; user-tier does QA pass.

**What stays out of scope (per directive A7 — hard-locked):**

- Removing consumer-workspaces.txt entirely (one-release deprecation; A4 keeps file with deprecation header; removal is follow-up arc).
- Adopting bw 0.13.0 features beyond B.1-B.4.
- Migrating existing on-disk handoff/retro/design artifacts to bw attachments (forward-only convention per A2 B.3).
- check-bw-release skill cron-scheduling defaults (skill exists; operator decides).
- Cross-workspace propagation of new skill (substrate update arc deploys via install.sh; consumer workspaces get on next apply).
- Editing existing arcs' retros or directives to fit any new convention.
- Sibling stoa--32b.1 (PRINCIPAL-gate discipline) and stoa--32b.2 (mechanical/agent-split) — separate forthcoming arcs.

If PLINY or any CAPTAIN surfaces a scope concern touching A7, treat as substance disagreement: confirm A7 wording from directive, file follow-up ticket if the concern has merit, do NOT expand this arc.

**Authorship attribution is IMMUTABLE per substrate/CLAUDE.md.** Arc 28 adds new files: `substrate/skills/check-bw-release/SKILL.md` (frontmatter — include `author: Denson Smith` per stoa--uly convention) + `substrate/skills/check-bw-release/check.sh` (no frontmatter; shell script). Verify all new files' author-like fields before commit.

**Self-referential note:** Arc 28 is the substrate-side companion to ariadne--c71 (the deployment-side worked example). The discipline being encoded (C) generalizes from BOTH pieces of work — the discipline says "when bw releases, here's what to do at each impact axis," and the work being done now demonstrates two of those axes (deployment via c71; substrate via B.1-B.4). Same self-referential dynamic as Arcs 24/25/27 — substrate working as designed.

If compaction or /clear erases your role, re-read this paste from HUMAN_paste-polybius-arc-28-instruction.md in the project root.
