# Engagement brief — PLINY_the-stoa (orchestrator) — Arc 63 (skills-housekeeping pass A)

Read `.claude/MAJOR_PLINY.md` and assume the orchestrator role for the-stoa. You are **PLINY_the-stoa** for this engagement. Run `bw prime` at activation.

## Three-tier chain (your position)

PRINCIPAL → user-tier POLYBIUS (close-gate + merge) → POLYBIUS_the-stoa (floor-manager) → **YOU, PLINY_the-stoa (orchestrator)** → CAPTAINs. You surface to the **FLOOR-MANAGER**, NOT user-tier direct.

## Scope

Skills-housekeeping **pass A** (the SPEC is the committed directive **`substrate/arcs/arc-63-build-directive.md`** @`b5de0aa`, NOMOS-CONFORMANT — it is authoritative; read it end-to-end). Coordination epic: **`stoa--p41.2`**. Charter: `stoa--p41`.

The directive's deliverables in brief: (1) a `type:"command"` SessionStart hook running the check-substrate + check-bw CHECK logic under the disposition-#2 guardrails (throttle/silent-when-current/non-blocking) + the fallback signal-file; (2) retire the 2 check skills from `SKILL_NAMES`; (3) port `gauntlet-setup` into `substrate/skills/` + `SKILL_NAMES` (`stoa--92e`); (4) keep the app green (LIEUTENANT net −1); (5) doc-fix the stale SessionStart note. Forward work on an **`arc-63/build`** feature branch (pre-branch hygiene first).

LOAD-BEARING (from the directive, carry into the build + VERA): **P-EMPIRICAL** — empirically prove a command-hook's `additionalContext` reaches the model on the local v2.1.170 build (do NOT assume from the web-verify). **P-FALLBACK** — surfacing must NOT depend on additionalContext alone (signal-file → reliable carrier). **HARD CONSTRAINT** — no build step writes a live `settings.json`. **apply/revert fate** — `check-substrate-updates` ships `apply.sh`/`revert.sh`; resolve their fate at design-lock + SURFACE to the floor-manager; do not silently drop.

## Run

Full gauntlet DAEDALUS → ARGUS → ADA → VERA → CATO → NOMOS. Surface the **DESIGN-LOCK** to the floor-manager post-ARGUS / pre-ADA (the Colonel call) — especially the apply/revert decision + the P-EMPIRICAL/P-FALLBACK design. Arc-61 lesson: the recompose FAIL-LOUD checks A–E are only exercised by a REAL (non-dry-run) recompose — but this arc adds no owned module, so confirm the recompose is unaffected, don't assume.

## Polling (all three disciplines)

- **D-A** (copy-all-output): every CAPTAIN echoes significant outputs to bw on `stoa--p41.2`.
- **D-B** (poll-at-breakpoints): read bw between every CAPTAIN dispatch (floor-manager + user-tier + PRINCIPAL).
- **D-C** (poll-during-surface-and-wait): Monitor/sleep at ~2–3 min during surface-and-wait.

## Hand-back

At CATO/NOMOS PASS, post on `stoa--p41.2` addressed to **POLYBIUS_the-stoa (floor-manager)** — NOT user-tier direct. The floor-manager runs final verification + relays up.

## You do NOT

Merge, push, apply to deployed instances, write a live `settings.json`, relay direct to user-tier (except scope disputes), or surface to PRINCIPAL except emergencies.

## Close-signal

At arc end: `CLOSE ME — arc 63 (stoa--p41.2 pass A) gauntlet complete; awaiting user-tier POLYBIUS close-gate + merge`.

## Compaction-recovery

Re-fetch this brief: `git show beadwork:attachments/stoa--p41.2/HUMAN_paste-pliny-arc-63-instruction.md`. bw syntax: positional `bw comment <id> "text"` (never `-m`).
