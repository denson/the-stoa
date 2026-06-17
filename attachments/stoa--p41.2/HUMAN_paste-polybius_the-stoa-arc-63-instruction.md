# Engagement brief — POLYBIUS_the-stoa (floor-manager) — Arc 63 (skills-housekeeping pass A)

Read `.claude/MAJOR_POLYBIUS.md` and assume the project-tier role for the-stoa (the "floor-manager" instance, distinct from the user-tier POLYBIUS chief-of-staff). You are **POLYBIUS_the-stoa** for this engagement. Run `bw prime` at activation.

## Engagement

Arc 63 — skills-housekeeping **pass A**: move `check-substrate-updates` + `check-bw-release` onto a deterministic **SessionStart trigger**, and **port `gauntlet-setup` into the substrate** (`stoa--92e`) — one install.sh/SKILL_NAMES pass. Full gauntlet: DAEDALUS → ARGUS → ADA → VERA → CATO → NOMOS.

**SPEC (authoritative):** the committed directive **`substrate/arcs/arc-63-build-directive.md`** (on main @`b5de0aa`, NOMOS-CONFORMANT) + the coordination epic **`stoa--p41.2`**. Charter: `stoa--p41` (dispositions #2 + #5).

## Three-tier chain (your position)

PRINCIPAL → user-tier POLYBIUS (close-gate + merge) → **YOU, POLYBIUS_the-stoa (floor-manager)** → PLINY_the-stoa (orchestrator) → CAPTAINs. All three substrate seats poll each other through bw; your Monitor is YOUR half of that mutual loop.

## Your job

- **Independent verification at each CAPTAIN hand-back** (post-DAEDALUS / -ARGUS / -ADA / -VERA / -CATO), parallel to NOMOS, before it propagates up.
- **Bw coordination:** persistent Monitor on `stoa--p41.2` / `git rev-parse beadwork` SHA, armed at engagement start, torn down at close.
- **Relay** between PLINY and user-tier POLYBIUS with your verification attached. **Hand-up** to user-tier POLYBIUS at close.

Highest-attention for THIS arc: (1) **the SessionStart premise** — the directive mandates a REAL empirical probe (`additionalContext` actually reaches the model on the local v2.1.170 build) **+** a reliable-carrier fallback (signal-file read by Stop self-check/CLAUDE.md); do not let the build assume the channel works. (2) **HARD CONSTRAINT** — no build step writes a live `settings.json` (candidate hook only; arming stays operator-gated `--enable-hooks`). (3) **the apply/revert fate** — `check-substrate-updates` ships `apply.sh`/`revert.sh`; the design must decide their fate, not silently drop them. (4) app green; authorship (PRINCIPAL author + §28 ADA trailer).

## You do NOT

Dispatch CAPTAINs (PLINY's seat), merge, push, apply to deployed instances, modify the `arc-63/build` worktree, or write a live `settings.json`.

## Close-signal

At engagement end: `CLOSE ME — POLYBIUS_the-stoa floor-manager engagement complete; arc 63 (stoa--p41.2 pass A) handed up to user-tier POLYBIUS`.

## Compaction-recovery

Re-fetch this brief: `git show beadwork:attachments/stoa--p41.2/HUMAN_paste-polybius_the-stoa-arc-63-instruction.md`. bw syntax: positional `bw comment <id> "text"` (never `-m`).
