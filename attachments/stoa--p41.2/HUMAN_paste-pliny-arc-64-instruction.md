# Engagement brief — PLINY_the-stoa (orchestrator) — Arc 64 (skills-housekeeping pass B)

Read `.claude/MAJOR_PLINY.md` and assume the orchestrator role for the-stoa. You are **PLINY_the-stoa** for this engagement. Run `bw prime` at activation.

## Three-tier chain (your position)

PRINCIPAL → user-tier POLYBIUS (close-gate + merge) → POLYBIUS_the-stoa (floor-manager) → **YOU, PLINY_the-stoa (orchestrator)** → CAPTAINs. You surface to the **FLOOR-MANAGER**, NOT user-tier direct.

## Scope

Skills-housekeeping **pass B** (the SPEC is the committed directive **`substrate/arcs/arc-64-build-directive.md`** @`2166eec`, NOMOS-CONFORMANT — read it end-to-end; it is authoritative). Coordination epic: **`stoa--p41.2`**. Charter: `stoa--p41`.

Deliverables in brief: (1) `save-verdict` → Bash-only module (`substrate/modules/save-verdict.md`) — canonical path + `printf` body-authoring + inline sha256 round-trip + **attach-to-bw-at-write**; `git rm` the skill + its Python; (2) `validate-spec` + `inspect-script-output` → modules (scripts retained + callable — Q2); (3) repoint `CAPTAIN_VERA.md`/`CAPTAIN_ARGUS.md`/`CAPTAIN_CATO.md` "Canonical verdict-save path" to `Read .claude/modules/save-verdict.md`; (4) resolve `stoa--7b1.1` at the SHARED review-seat layer (ARGUS/NOMOS/ZENO §4-no-Write vs §7-save-verdict — do not patch one seat); (5) install.sh `SKILL_NAMES` −3 + deploy the 3 modules; (6) app green (LIEUTENANT −3). Forward work on an **`arc-64/build`** feature branch (pre-branch hygiene first).

LOAD-BEARING (carry into the build + VERA): **attach-at-write probe** (a verdict written via the new module LANDS on beadwork — exercise, don't assume). **No-Write-seat probe** (a Bash-only no-Write seat authors+writes+attaches via the module). **sha256 negative probe** (the inline round-trip catches a corrupted write). **UNIFORMITY:** land the `printf` Bash-only authoring uniformly across VERA/ARGUS/CATO — NOMOS flagged `CAPTAIN_VERA.md:266` still uses the Write tool while ARGUS:246/CATO:212 use printf; the no-Write resolution must be coherent across all three.

## Run

Full gauntlet DAEDALUS → ARGUS → ADA → VERA → CATO → NOMOS. Surface the **DESIGN-LOCK** to the floor-manager post-ARGUS / pre-ADA — especially the three open design questions in the directive: **Q-A** (does the Bash-only module preserve the Python's shape-validation/empty-binding enforcement via a lightweight inline assert, or accept seat-side-only?), **Q-B** (the exact `stoa--7b1.1` shared-layer §4/§7 reconciliation wording), **Q-C** (do the new modules need MODULE-INLINE markers + recompose ownership at subproject tier?). Arc-61 lesson: IF a module is recompose-owned, the FAIL-LOUD Checks A–E are only exercised by a REAL (non-dry-run) recompose.

## Polling (all three disciplines)

- **D-A** (copy-all-output): every CAPTAIN echoes significant outputs to bw on `stoa--p41.2`.
- **D-B** (poll-at-breakpoints): read bw between every CAPTAIN dispatch (floor-manager + user-tier + PRINCIPAL).
- **D-C** (poll-during-surface-and-wait): Monitor/sleep at ~2–3 min during surface-and-wait.

## Hand-back

At CATO/NOMOS PASS, post on `stoa--p41.2` addressed to **POLYBIUS_the-stoa (floor-manager)** — NOT user-tier direct.

## You do NOT

Merge, push, apply to deployed instances, relay direct to user-tier (except scope disputes), or surface to PRINCIPAL except emergencies.

## Close-signal

At arc end: `CLOSE ME — arc 64 (stoa--p41.2 pass B) gauntlet complete; awaiting user-tier POLYBIUS close-gate + merge`.

## Compaction-recovery

Re-fetch this brief: `git show beadwork:attachments/stoa--p41.2/HUMAN_paste-pliny-arc-64-instruction.md`. bw syntax: positional `bw comment <id> "text"` (never `-m`).
