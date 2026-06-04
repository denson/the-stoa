Read .claude/MAJOR_PLINY.md and assume the orchestrator role (PLINY_the-stoa) for the-stoa.

## the-stoa is the forge (activate from .claude/, build edits substrate/)
Activate from `.claude/MAJOR_PLINY.md`; CAPTAINs are the `_the_stoa` registry seats in `.claude/agents/` (12 incl. NOMOS). Arcs EDIT `substrate/` source (re-deploys to `.claude/` via install.sh after landing). bw is now **0.13.1** (concurrent-write fix).

## Cron hygiene FIRST
This session may carry an orphaned cron from a prior /clear. Run `CronList`; `CronDelete` any present. Then surface-and-wait per `MAJOR_PLINY.md §6.2`.

## Pre-branch hygiene (§5.9 — before each arc-build branch)
- `git branch | grep -E '^\s*arc-[0-9]+/build$'` must be empty
- `git fetch origin main` ; `git log --oneline main..origin/main` (empty) ; `git log --oneline origin/main..main` (empty)
- main was last synced at `3ce9545` by user-tier; expect clean. If either check fails, surface to POLYBIUS_the-stoa.

## The engagement — the revision ROUND (batched), not one arc
Epic: `stoa--ikr` — READ IT FIRST for scope (A+B+C; D deferred), drive-mode, sequence. DONE: `stoa--x4j` / `stoa--g38` / `stoa--rwp`. You run the REMAINING tickets as arcs, in this suggested order:
1. **`stoa--2i5`** (install.sh consumer .gitignore management) — bucket C, mechanical → autonomous-ship on clean PASS.
2. **save-verdict/Windows cluster** as ONE arc: `stoa--wq0` (Windows git-bash heredoc/`/tmp` fail — THE Windows-tester blocker, highest value) + `stoa--xxy` (receipt filename collision + the sub-agent-writes-to-main-root facet) + `stoa--7b1.2` (ship a .gitignore for `__pycache__`) + `stoa--7ap` (Windows worktree-remove orphan-dir — verify dir-gone not just registration). Bucket B; surface the design if a real judgment call appears, else autonomous-ship.
3. **Bucket A (PRINCIPAL-GATED)**, sequence-critical: `stoa--3c9` (tool-selection discipline) → `stoa--yfv` Arc B (`.1` keystone first: verdict threat-coverage assertion, then `.2`/`.5`/`.6`) → `stoa--h2z` (needs 3c9 + yfv.1) → `stoa--0hl` (team-deploy canon). Surface the design at the HARD STOP to POLYBIUS_the-stoa → user-tier for the ship.

## Gauntlet
Full pipeline per arc: DAEDALUS → ARGUS → [HARD STOP] → ADA → VERA → CATO → NOMOS → ZENO. Keep arc diffs scoped.

## Drive mode (per stoa--ikr)
- Bucket B + C: autonomous-ship on clean PASS (hand back to POLYBIUS_the-stoa, who ships).
- Bucket A: HITL — surface design at HARD STOP + ship to user-tier; do NOT autonomous-ship canon.

## Coordination
- Surface to **POLYBIUS_the-stoa (floor-manager)**, NOT user-tier direct.
- Three polling disciplines: D-A copy CAPTAIN outputs to the arc's bw ticket; D-B read bw between dispatches; D-C Monitor during surface-and-wait (~2-3 min).
- **De-collision:** user-tier POLYBIUS may drive some round items directly via in-session workflows. BEFORE starting an arc, check its ticket + `stoa--ikr` for an in-progress note so two seats don't double-run the same ticket.

## What you do NOT do
- Do NOT merge/push/cleanup outside the arc-build worktree.
- Do NOT surface to PRINCIPAL except emergencies — surface to the floor-manager.
- Do NOT skip the HARD STOP on bucket-A arcs. Do NOT touch the bw binary.

## Close signal
At round end: `CLOSE ME — round gauntlet complete; awaiting POLYBIUS_the-stoa + user-tier close-gate`.

## Recovery
If this session compacts or /clears, re-read this file + `.claude/MAJOR_PLINY.md` + `bw show stoa--ikr`.
