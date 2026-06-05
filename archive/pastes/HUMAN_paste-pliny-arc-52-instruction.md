Read .claude/MAJOR_PLINY.md and assume the orchestrator role (PLINY_the-stoa) for the-stoa substrate Arc 52.

## the-stoa is the forge (activate from .claude/, build edits substrate/)
the-stoa self-deploys its substrate to `.claude/` — activate from `.claude/MAJOR_PLINY.md` (your role); the CAPTAINs you dispatch are the `_the_stoa` registry seats (in `.claude/agents/`). NOTE: the BUILD edits the `substrate/` SOURCE canon (role files / operating-disciplines), which re-deploys to `.claude/` via `install.sh` after the arc lands — activate from `.claude/`, build against `substrate/`.

## Cron hygiene FIRST (before any substantive work)
This session may carry an orphaned cron from a prior /clear. Run `CronList`; `CronDelete` any present. Then proceed surface-and-wait per `MAJOR_PLINY.md §6.2`.

## Pre-branch hygiene (per MAJOR_PLINY.md §5.9 — before creating arc-52/build)
- Check 1: `git branch | grep -E '^\s*arc-[0-9]+/build$'`   # must be empty
- Check 2: `git fetch origin main` ; `git log --oneline main..origin/main` (empty) ; `git log --oneline origin/main..main` (empty)
- main was just synced (arc-52 dispatch artifacts) by user-tier POLYBIUS — expect it clean. If either check fails, surface to POLYBIUS_the-stoa (floor-manager) with the specific state observed; do NOT silently inherit local-ahead commits.

## Your seat
You run the gauntlet: dispatch CAPTAINs in sequence — **DAEDALUS → ARGUS → [HARD STOP] → ADA → VERA → CATO → NOMOS → ZENO** — enforcing design → audit → HARD STOP → build → verify → review → judgment → spec-check.

## The arc
Arc 52 = Threat-defeat hardening, **ARC A (prevention layer)**, a substrate-canon edit. Read FIRST, in full:
1. The directive: `substrate/arcs/arc-52-threat-defeat-prevention-directive.md` (authoritative scope + locked decisions).
2. `stoa--yfv` (epic + coordination ticket): the "RESTRUCTURE ACCEPTED" comment (accepted scope) + the external-review comment — **external review is already done and incorporated; do NOT re-run it**.
3. For incident context: `u--ith` + `u--tgc` in user-beadwork.

**Scope is PREVENTION only** — A1 (unconditional ratification restatement, the keystone), A2 (gate-item design-fold), A3 (DAEDALUS threat→mitigation map + ARGUS design-smell), A4 (definitions incl. gate-origin + upstream owner). Detection (#4 probes / #5 verdict assertion / #6 close-gate re-derivation / #7 culture) is **Arc B — OUT of scope**. Carve the hardening arc itself OUT of "threat-ratified" (no self-reference) per the directive's locked decisions.

## Chain of command (THREE-tier)
- **user-tier POLYBIUS** authored the directive; holds close-gate + merge.
- **POLYBIUS_the-stoa (floor-manager)** — independent verification + relay. YOU surface to the floor-manager, **NOT user-tier direct**.
- **You (PLINY_the-stoa)** orchestrate; dispatch CAPTAINs.

## Polling disciplines (all three)
- **D-A (copy-all-output):** echo every CAPTAIN's significant outputs to bw on `stoa--yfv`.
- **D-B (poll-at-breakpoints):** read bw between every CAPTAIN dispatch (floor-manager / user-tier may have posted direction).
- **D-C (poll-during-surface-and-wait):** run a Monitor (or sleep loop) during surface-and-wait at ~2-3 min cadence.

## Operating mode: HITL
Surface the DAEDALUS design at the **HARD STOP** to POLYBIUS_the-stoa (floor-manager) before build. Do NOT autonomous-ship — substrate-canon + security. The floor-manager + user-tier gate the design before build.

## Hand-back
At ZENO PASS (gauntlet complete), post on `stoa--yfv` addressed to **POLYBIUS_the-stoa (floor-manager)** — NOT user-tier direct. The floor-manager runs final independent verification + relays up.

## What you do NOT do
- Do NOT merge, push, or apply anything outside the arc-build worktree.
- Do NOT surface to PRINCIPAL except emergencies — surface to the floor-manager.
- Do NOT skip the HARD STOP. Do NOT re-run external review (done).

## Close signal
At arc end: `CLOSE ME — arc-52 gauntlet complete; awaiting POLYBIUS_the-stoa verification + user-tier close-gate + merge`.

## Recovery
If this session compacts or /clears, re-read this file (`HUMAN_paste-pliny-arc-52-instruction.md`) and `.claude/MAJOR_PLINY.md` to recover your seat.
