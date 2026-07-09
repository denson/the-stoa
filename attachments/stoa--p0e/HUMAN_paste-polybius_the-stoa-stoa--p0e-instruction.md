# Engagement brief v4 — POLYBIUS_the-stoa (floor-manager) — stoa--p0e RESUME: post-merge cleanup + arc close ONLY

Read .claude/MAJOR_POLYBIUS.md and assume the project-tier role for the-stoa (floor-manager instance). You are POLYBIUS_the-stoa (v4).

**This is a NARROW RESUME.** Your v3 predecessor (sid 9f9ea579) stalled after the arc was already MERGED — flipped dead. The gauntlet is COMPLETE, the user-tier close-gate PASSED, and stoa--p0e/build is fast-forward MERGED to main (c3b2b3b1) and pushed. PLINY has been ruled GO on its worktree teardown (may already be done). Do NOT re-run anything upstream.

## Chain of command

PRINCIPAL → Polybius the Grand → **Polybius the Decider (user-tier — your only up-channel)** → YOU → PLINY. Ladder unchanged; terminals are status surfaces.

## Your ONLY tasks (settled — execute)

1. Read stoa--p0e from the Decider's 21:26:29 close-gate post downward (ruling, PLINY GO, the v3 stall record).
2. **Post-merge residual cleanup on main** (the cross-seam step v3 owned): run install.sh deploy-regen (refreshes the deployed `.claude/templates/settings-hooks.json` from the retired source) + `install.sh --prune-obsolete` (removes the deployed orphan `.claude/hooks/pretooluse-author-field-audit.sh`) + the P3b post-merge asserts from design-rev2 (grep the deployed settings/template for 0 audit-hook refs; the two surviving gates intact; advisory skill deployed). If regen output touches tracked files, commit as housekeeping (Author = Denson Smith + your seat trailer per §28) and push main.
3. Verify PLINY's teardown completed (worktree `stoa--p0e-build` gone, branch deleted); if PLINY hasn't executed, coordinate — its GO is already ruled.
4. Post cleanup evidence to stoa--p0e addressed to the Decider, then your `CLOSE ME — POLYBIUS_the-stoa floor-manager engagement complete; arc stoa--p0e closed`.

## Disciplines

Quiesce-cold does not apply — this is a bounded execution task; run it to completion in one sitting. 10-minute liveness rule: your FIRST post (activation ack) lands within 10 minutes of launch or you are presumed dead. No merges beyond the housekeeping commit in task 2; nothing deploys; consumer propagation rides check-substrate-updates per design.

## Compaction recovery

`git show beadwork:attachments/stoa--p0e/HUMAN_paste-polybius_the-stoa-stoa--p0e-instruction.md`
