# Activation — MAJOR_PLINY, Arc 52 (Threat-defeat hardening, Arc A / prevention)

Assume the role of **MAJOR_PLINY** (the ORCHESTRATOR). Read your role file (`.claude/MAJOR_PLINY.md`, or `substrate/MAJOR_PLINY.md` if running from the substrate source) and operate as that seat for this session.

## Cron hygiene FIRST (before any substantive work)
This session may carry an orphaned cron from a prior /clear'd context. Run `CronList`; if any cron is present, `CronDelete` it. Then proceed surface-and-wait per `MAJOR_PLINY.md §6.2`. Defense-in-depth.

## Pre-branch hygiene (per MAJOR_PLINY.md §5.9 — run before creating arc-52/build)
Check 1 (no other arc-build branch in flight):
  `git branch | grep -E '^\s*arc-[0-9]+/build$'`    # must be empty
Check 2 (local main = origin/main):
  `git fetch origin main`
  `git log --oneline main..origin/main`             # must be empty
  `git log --oneline origin/main..main`             # must be empty
If either check fails, surface to user-tier POLYBIUS (or PRINCIPAL via `[for: PRINCIPAL]`) with the specific state observed. Do NOT silently inherit local-ahead commits into the arc branch.
NOTE: user-tier POLYBIUS has uncommitted working-tree files this session (the workflow-composer skill prototype, two docs/sessions/ files, agents/design/stoa--04n/, and this arc-52 directive + paste). Confirm with user-tier POLYBIUS which of those should be committed (the arc-52 directive + paste are §18.1 housekeeping that should land before/with dispatch) before creating the arc branch, so the arc squash doesn't bundle unrelated prototype work.

## Intent
Run **Arc 52 — Threat-defeat hardening, ARC A (prevention layer)** per the directive at:
  `substrate/arcs/arc-52-threat-defeat-prevention-directive.md`

This is **Arc A of a two-arc split** (Arc B = detection, dispatched separately AFTER Arc A lands). Read, in order:
1. The directive above (authoritative scope + locked decisions).
2. `bw show stoa--yfv` — the epic; READ the "RESTRUCTURE ACCEPTED" comment (the accepted Arc A/B structure) and the external-review comment (the findings this directive already incorporates).
3. For full incident context: `bw show u--ith` and `bw show u--tgc` in user-beadwork (the threat-defeat directive + incident capture).

## Scope (Arc A — prevention only)
A1 unconditional ratification restatement (keystone) · A2 gate-ratified items get a design pass · A3 DAEDALUS threat→mitigation map + ARGUS design-smell · A4 definitions ("named threat" incl. gate-origin; "threat-ratified mitigation"; upstream owner; no-classification = finding). Detection changes (#4/#5/#6/#7) are **out of scope — Arc B**.

## Gauntlet
Run the full pipeline: DAEDALUS (design the prevention-layer role-file/process edits) → ARGUS (audit) → **HARD STOP** → ADA (build) → VERA / CATO / ZENO (verify coherence + non-regression + `npm run gen-data` clean). **External review is already DONE** (cold-Claude, recorded on `stoa--yfv`) — do not re-run it; the directive already incorporates its prevention-first restructure.

## Operating mode: HITL
Surface the DAEDALUS design at the HARD STOP to user-tier POLYBIUS / PRINCIPAL before build. This is substrate-canon + security-discipline work — gate it; do not autonomous-ship. Coordinate status via bw comments on `stoa--yfv`.
