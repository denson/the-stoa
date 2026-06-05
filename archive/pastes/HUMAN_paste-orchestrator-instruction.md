# MAJOR_PLINY activation — Arc 17

Read `~/.claude/MAJOR_PLINY.md` and assume the orchestrator role for the the-stoa Arc 17 engagement. Run `bw prime` at activation per the role file's §4 checklist.

## Engagement

Read `substrate/arcs/arc-17-build-directive.md` (commit `fa710b2` on `the-stoa` main) and execute per the directive. The work is medium-sized: add three POLYBIUS authoring capabilities to the substrate (§11 pair-programmer authoring + §12 prototyping methodology + LIEUTENANT_agent_author skill), extend `install.sh` (skills deployment + staleness fix folding in `stoa--w1t`), reframe planning v2 spec §4. Phase A decisions are LOCKED pre-dispatch (no surface needed).

## Comms — direct async with POLYBIUS via bw (proven in Arc 16)

POLYBIUS (user-tier CoS, separate Claude Code session) and you both communicate via comments on the Arc 17 bw epic. PRINCIPAL is **not** the relay for routine status — beadwork is.

**bw command syntax** is taught in your role file at `MAJOR_PLINY.md` §6.1 — read it. Critical: `bw comment <id> "text"` is positional, NO `-m` flag. The Arc 16 lesson is now substrate-resident.

**Polling — surface-and-wait pattern only** (still aspirational in spec; operationally proven in Arc 16):
- You do NOT poll during normal heads-down work, including between phases when nothing is blocked
- You DO poll **only when you've surfaced a question to POLYBIUS via bw and are waiting for the answer to proceed.** The trigger is: "I sent a comment with a question; I cannot continue without the response; I am now waiting."
- When that trigger fires: set up `CronCreate` with `*/5 * * * *` cadence; cancel via `CronDelete <job-id>` the moment you read POLYBIUS's response and resume working.
- Phase transitions where nothing is blocked: just write the status comment and continue. No polling needed.

POLYBIUS is polling the-stoa bw every 5 min from its session — your phase-transition comments will be picked up within ~5 min, and POLYBIUS will respond via bw if anything needs your attention. If POLYBIUS spots a problem mid-flight that needs course correction, POLYBIUS writes to bw; you'll see it the next time you naturally check bw (or when you hit a real surface and start polling). Don't burn polling tokens defensively.

## Activation steps

1. Read `~/.claude/MAJOR_PLINY.md`, confirm rank MAJOR / mnemonic PLINY / role ORCHESTRATOR
2. Run `bw prime` (per §4 checklist step 3)
3. Read `substrate/arcs/arc-17-build-directive.md`
4. File the Arc 17 epic: `bw create "[EPIC] Arc 17 — POLYBIUS authoring capabilities + agent-authoring skill + skills deployment" -t epic -p 1`
5. Comment activation on the epic: `bw comment <epic-id> "PLINY active for Arc 17. Working tree clean (or noted state); on main, last commit fa710b2. Phase A decisions are LOCKED per directive (no surface needed). Beginning Phase A: install.sh extensions for skills deployment + staleness detection."`
6. Begin work — heads-down per the suggested phasing (A: install.sh, B: agent-author skill, C: §11 + §12, D: spec §4 reframe, E: smoke + ship)

## Out of scope (per directive)

- Stoa LIEUTENANT slot rendering — moved to Arc 17.1 follow-up
- Arc 18 (polling capability + consent in role files)
- Authoring specific named pair-programmers (ATTICUS etc.)
- Modifying historical artifacts
- Modifying the case study + KG drafts at `docs/case-study/` — already current

Standby, run.
