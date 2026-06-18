Read .claude/MAJOR_PLINY.md. Then read your brief + spec: `git show beadwork:attachments/stoa--5ju/HUMAN_paste-pliny-arc-66-instruction.md` and `substrate/arcs/arc-66-build-directive.md`. Assume the orchestrator role for the-stoa on Arc 66.

# Arc 66 (full gauntlet): fix check-substrate-updates blind to CHIRON/HAMILTON

**Charter:** `stoa--5ju`. **The spec is the directive:** `substrate/arcs/arc-66-build-directive.md` — read it in full; it carries the verified diagnosis, the fix shape, and the DoD. You surface to **POLYBIUS_the-stoa (floor-manager)**, NOT user-tier direct.

## Scope (the directive is authoritative — this is the summary)

`check-substrate-updates` hardcodes the expected MAJOR set to POLYBIUS + PLINY, while CAPTAINs/templates/skills are auto-discovered. CHIRON + HAMILTON (Arc 61/62 MAJORs) are therefore invisible to MISSING detection, so the `deploy-stoa` EXISTING-project update path silently omits the design layer. **Fix:** glob-derive the MAJOR set so any future MAJOR auto-discovers, across four loci:
- `check.sh` `enumerate_deployed()` (~:401-408; literals :403-407) — PRIMARY (MISSING detection).
- `check.sh` `source_path_for_deployed()` (:294-298) — DRIFTED detection.
- `check.sh` `apply_substitutions()` (case at :119) — subproject NAME_SUFFIX byte-compare.
- `install.sh` `write_substrate_manifest()` (:540-544) — deploy-time manifest completeness.

**CRITICAL:** MAJOR suffix rules are not uniform — DAEDALUS must verify against `install.sh` `DEST_*` (:955-963; actual writes :993-994) exactly how CHIRON/HAMILTON suffix per tier and make every enumeration site match. A wrong suffix produces false MISSING/OBSOLETE pairs.

**DoD (real, non-dry-run):** deploy current substrate to a throwaway → remove deployed CHIRON/HAMILTON → `check.sh --workspace` reports them MISSING (capture the pre-fix falsification baseline first) → `apply.sh` delivers → re-check clean; subproject FAIL-LOUD recompose A–E green via a REAL recompose (probe V3); `app` green (gen-data/build/test); NOMOS CONFORMANT. **Out of scope:** role files, broader check.sh refactors, deploy-stoa/install-stoa skills, the u--k5s CRLF item, zeotek_newswire (use a throwaway).

## Polling disciplines (all three)

- **D-A (bw-copy-all-output):** every CAPTAIN echoes significant outputs to bw on `stoa--5ju`.
- **D-B (polling-at-breakpoints):** read bw between every CAPTAIN dispatch — sources include floor-manager + user-tier POLYBIUS + PRINCIPAL.
- **D-C (polling-during-surface-and-wait):** run a Monitor (or sleep loop) at ~2-3 min cadence while in surface-and-wait.

## Hand-back protocol

At **CATO PASS** (+ embedded ZENO/NOMOS), post on `stoa--5ju` addressed to **POLYBIUS_the-stoa (floor-manager)** — NOT direct to user-tier. The floor-manager runs final verification + relays up.

## What you do NOT do

Merge · push to main · apply to any consumer workspace · relay direct to user-tier (except scope disputes) · surface to PRINCIPAL except emergencies.

## Close-signal

`CLOSE ME — arc 66 gauntlet complete; awaiting user-tier POLYBIUS close-gate + merge`

---
*Compaction recovery: re-read this brief at `git show beadwork:attachments/stoa--5ju/HUMAN_paste-pliny-arc-66-instruction.md`, then `substrate/arcs/arc-66-build-directive.md` + `bw show stoa--5ju`.*
