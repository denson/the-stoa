Read .claude/MAJOR_PLINY.md and assume the orchestrator role (PLINY_the-stoa) for the-stoa substrate Arc 53.

## the-stoa is the forge (activate from .claude/, build edits substrate/)
the-stoa self-deploys its substrate to `.claude/` — activate from `.claude/MAJOR_PLINY.md` (your role); the CAPTAINs you dispatch are the `_the_stoa` registry seats (in `.claude/agents/`; NOMOS now deployed, 12 envelopes). The BUILD edits the `substrate/` SOURCE (install.sh, check.sh, the workflow-composer skill), which re-deploys to `.claude/` via `install.sh` after the arc lands — activate from `.claude/`, build against `substrate/`.

## Cron hygiene FIRST (before any substantive work)
This session may carry an orphaned cron from a prior /clear. Run `CronList`; `CronDelete` any present. Then proceed surface-and-wait per `MAJOR_PLINY.md §6.2`.

## Pre-branch hygiene (per MAJOR_PLINY.md §5.9 — before creating arc-53/build)
- Check 1: `git branch | grep -E '^\s*arc-[0-9]+/build$'`   # must be empty
- Check 2: `git fetch origin main` ; `git log --oneline main..origin/main` (empty) ; `git log --oneline origin/main..main` (empty)
- main was just synced (arc-53 directive `fcb84b4`) by user-tier POLYBIUS — expect it clean. If either check fails, surface to POLYBIUS_the-stoa (floor-manager); do NOT silently inherit local-ahead commits.

## Your seat
You run the gauntlet: dispatch CAPTAINs in sequence — **DAEDALUS → ARGUS → [HARD STOP] → ADA → VERA → CATO → NOMOS → ZENO** — enforcing design → audit → HARD STOP → build → verify → review → judgment → spec-check.

## The arc
Arc 53 = workflow-composer skill forge-promotion, a substrate-canon edit. Read FIRST, in full:
1. The directive: `substrate/arcs/arc-53-workflow-composer-promotion-directive.md` (authoritative scope + locked decisions).
2. `stoa--04n` (work-unit + coordination ticket): READ its doc-delta comment (the 5 corrections) + the prior Stage-A design at `agents/design/stoa--04n/design.md` (deploy-wiring half).
3. The skill being promoted: `substrate/skills/workflow-composer/SKILL.md` (refreshed 2026-06-01 with the 5 deltas — final-as-refreshed per locked decision #1; you PROMOTE + verify currency, you do NOT re-author content).

**Scope = TWO halves, both required:**
- THING 1 (deploy wiring): add `workflow-composer` to `SKILL_NAMES` in `substrate/install.sh`; fix the stale `install.sh:140-144` cite in `check.sh` at ALL FOUR occurrences (76/228/385/435), not one (Arc 52 ARGUS MAJOR-2 found the same class); `npm run gen-data` stays green.
- THING 2 (skill-content currency): verify the 5 deltas are present in the promoted skill — four-primitive framing; `ultracode` keyword (NOT the pre-v2.1.160 `workflow` keyword); `args` parameterization; allowlist/`stoa--x4j` stall-fix; overnight≠workflow. The stale `workflow`-as-keyword framing must be GONE.

**OUT of scope** (locked decision #2): NO `WORKFLOW_NAMES` / `.claude/workflows/` deploy infrastructure (no battle-tested script exists to promote — separate later arc). Ship only the SKILL.

## Chain of command (THREE-tier)
- **user-tier POLYBIUS** authored the directive + refreshed the skill; holds close-gate + merge.
- **POLYBIUS_the-stoa (floor-manager)** — independent verification + relay. YOU surface to the floor-manager, **NOT user-tier direct**.
- **You (PLINY_the-stoa)** orchestrate; dispatch CAPTAINs.

## Polling disciplines (all three)
- **D-A (copy-all-output):** echo every CAPTAIN's significant outputs to bw on `stoa--04n`.
- **D-B (poll-at-breakpoints):** read bw between every CAPTAIN dispatch (floor-manager / user-tier may have posted direction).
- **D-C (poll-during-surface-and-wait):** run a Monitor (or sleep loop) during surface-and-wait at ~2-3 min cadence.

## Operating mode: HITL
Surface the DAEDALUS design at the **HARD STOP** to POLYBIUS_the-stoa (floor-manager) before build. Do NOT autonomous-ship — substrate canon. The floor-manager + user-tier gate the design before build.

## Hand-back
At ZENO PASS (gauntlet complete), post on `stoa--04n` addressed to **POLYBIUS_the-stoa (floor-manager)** — NOT user-tier direct. The floor-manager runs final independent verification + relays up.

## What you do NOT do
- Do NOT merge, push, or apply anything outside the arc-build worktree.
- Do NOT surface to PRINCIPAL except emergencies — surface to the floor-manager.
- Do NOT skip the HARD STOP. Do NOT re-author skill content (promote + verify only).

## Close signal
At arc end: `CLOSE ME — arc-53 gauntlet complete; awaiting POLYBIUS_the-stoa verification + user-tier close-gate + merge`.

## Recovery
If this session compacts or /clears, re-read this file (`HUMAN_paste-pliny-arc-53-instruction.md`) and `.claude/MAJOR_PLINY.md` to recover your seat.
