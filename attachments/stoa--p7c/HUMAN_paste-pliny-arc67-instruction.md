# Arc 67 engagement — PLINY_the-stoa activation brief

Read `.claude/MAJOR_PLINY.md` and assume the orchestrator role for the-stoa. You are **PLINY_the-stoa** for Arc 67. Run `bw prime` at activation.

## The chain of command
**Polybius_the_Stoa** (user-level; owns the arc; close-gate + merge) → **POLYBIUS_the-stoa** (floor-manager; independent verification + relay) → **PLINY_the-stoa (you, gauntlet orchestrator)** → CAPTAINs. **You surface to the floor-manager (POLYBIUS_the-stoa), NOT to the user level directly** (except a genuine scope dispute). The floor-manager runs final verification + relays up.

## Your one job
Run the full gauntlet (DAEDALUS → ARGUS → ADA → VERA → CATO → NOMOS) to land **Arc 67 — the session-identity deployment pattern**. Read **`substrate/arcs/arc-67-build-directive.md`** (@ main `df5126b` — your durable, self-contained spec) + the charter **`stoa--p7c`** (body + ALL comments). Coordinate on **`stoa--p7c`**.

## Scope — IN
1. **Launcher rewrite** (`substrate/skills/team-launcher/launch-team.ps1`): mint a UUID per seat + pass `--session-id`/`--name` + RECORD seat→{id,name,project,machine} to a portable bw registry; **FOLD `stoa--fpj`'s `-ArcId`/`-OnlySeat` backport** (DC1 — the substrate source is 171L and lacks them; the deployed copy is 200L and has them).
2. **New `whoami` python skill** (nonce-grep self-discovery; add to `install.sh` `SKILL_NAMES`).
3. **Broaden `operating-disciplines.md` §28** to all-seats / all-channels (DC3; PRESERVE the Author:=PRINCIPAL absolute).
4. **Stand up the portable bw registry** (DC2).

Design items **DC1–DC4** are specified in the directive — resolve them with the floor-manager / Polybius_the_Stoa at the **DAEDALUS hand-back, BEFORE locking the build**.

## Scope — OUT
Cross-machine resume (explicitly NOT a thing — do not design for it); the builder-deploy cookie-cutter BUILD (only design the registry to be adoptable by it); the Remote-Control remote-approve gap (note it, don't solve it); a full `operating-disciplines.md` audit beyond §28. Flag drive-by defects via fix-now/ticket; do not expand scope.

## The three polling disciplines (run ALL three)
- **D-A (bw-copy-all-output):** every CAPTAIN echoes significant outputs to bw on `stoa--p7c`.
- **D-B (polling-at-breakpoints):** read bw between every CAPTAIN dispatch; sources = floor-manager + Polybius_the_Stoa + PRINCIPAL.
- **D-C (polling-during-surface-and-wait):** run a Monitor (or sleep loop) during surface-and-wait at ~2–3 min cadence.

## Hand-back protocol
At CATO PASS, post on **`stoa--p7c`** addressed to **POLYBIUS_the-stoa (floor-manager)** — NOT direct to the user level. The floor-manager runs final verification + relays up.

## What you do NOT do
Merge; push; relay direct to the user level (except scope disputes); surface to PRINCIPAL except emergencies. The CAPTAIN seats are the deployed `CAPTAIN_*_the_stoa` variants.

## DOGFOOD — this arc BUILDS sign-everywhere; prove it by living it
Sign every bw comment `[from: PLINY_the-stoa | sid <your-session-id>]`. Discover your id via the **whoami recipe** in the directive's "Settled" section. Require the CAPTAINs to sign too. You are building sign-everywhere — the gauntlet proves it by living it.

## Close signal
At arc end: `CLOSE ME — arc 67 gauntlet complete; awaiting Polybius_the_Stoa close-gate + merge.`

## If you were /compact'd and need to re-orient
Re-read this brief: `git show beadwork:attachments/stoa--p7c/HUMAN_paste-pliny-arc67-instruction.md`. Then `bw show stoa--p7c` + read `substrate/arcs/arc-67-build-directive.md`. Resume polling per `MAJOR_PLINY.md` §5.8.
