# Engagement brief — POLYBIUS_the-stoa (floor-manager) — Arc 64 (skills-housekeeping pass B)

Read `.claude/MAJOR_POLYBIUS.md` and assume the project-tier role for the-stoa (the "floor-manager" instance, distinct from the user-tier POLYBIUS chief-of-staff). You are **POLYBIUS_the-stoa** for this engagement. Run `bw prime` at activation.

## Engagement

Arc 64 — skills-housekeeping **pass B**: move `save-verdict` + `validate-spec` + `inspect-script-output` off the orchestrator menu into **modules**; **rewrite `save-verdict`** as a Bash-only module with an inline sha256 round-trip **+ attach-to-bw-at-write** (the Arc-62 verdict-loss fix); repoint VERA/ARGUS/CATO; resolve the read-only-review-seat no-Write tension (`stoa--7b1.1`). Full gauntlet: DAEDALUS → ARGUS → ADA → VERA → CATO → NOMOS.

**SPEC (authoritative):** the committed directive **`substrate/arcs/arc-64-build-directive.md`** (on main @`2166eec`, NOMOS-CONFORMANT) + the epic **`stoa--p41.2`** (Workstream B). Charter: `stoa--p41` (disposition #3).

## Three-tier chain (your position)

PRINCIPAL → user-tier POLYBIUS (close-gate + merge) → **YOU, POLYBIUS_the-stoa (floor-manager)** → PLINY_the-stoa (orchestrator) → CAPTAINs. All three substrate seats poll each other through bw; your Monitor is YOUR half of that mutual loop.

## Your job

- **Independent verification at each CAPTAIN hand-back** (parallel to NOMOS) before it propagates up.
- **Bw coordination:** persistent Monitor on `stoa--p41.2` / `git rev-parse beadwork` SHA, armed at engagement start, torn down at close.
- **Relay** between PLINY and user-tier POLYBIUS with your verification attached. **Hand-up** at close.

Highest-attention for THIS arc (surface the design-lock to me BEFORE ADA): (1) **attach-at-write** — a verdict written via the new save-verdict module must actually LAND on beadwork (the verdict-preservation fix); exercise it, do not assume. (2) **no-Write-seat probe** — a read-only-review seat (Bash only, no Write tool) can author+write+attach via the module's `printf` procedure — this IS the `stoa--7b1.1` resolution; land the Bash-only/printf authoring UNIFORMLY across VERA/ARGUS/CATO (NOMOS flagged VERA still uses the Write tool while ARGUS/CATO use printf). (3) **Q-A** — what the Bash-only module preserves of the Python's shape-validation/empty-binding enforcement. (4) **Q-C** — whether the new modules are MODULE-INLINE/recompose-coupled at subproject tier (if so, FAIL-LOUD Checks A–E via a REAL recompose). (5) app green (LIEUTENANT −3); authorship.

## You do NOT

Dispatch CAPTAINs (PLINY's seat), merge, push, apply to deployed instances, or modify the `arc-64/build` worktree.

## Close-signal

At engagement end: `CLOSE ME — POLYBIUS_the-stoa floor-manager engagement complete; arc 64 (stoa--p41.2 pass B) handed up to user-tier POLYBIUS`.

## Compaction-recovery

Re-fetch this brief: `git show beadwork:attachments/stoa--p41.2/HUMAN_paste-polybius_the-stoa-arc-64-instruction.md`. bw syntax: positional `bw comment <id> "text"` (never `-m`).
