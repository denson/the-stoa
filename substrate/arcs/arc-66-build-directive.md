# Arc 66 build directive — check-substrate-updates blind to CHIRON/HAMILTON (hardcoded MAJOR enumeration)

**Audience:** the fresh Claude Code session opened to build Arc 66.
**Authored by:** user-tier POLYBIUS the Stoa "A2A monitor" (chief-of-staff fork) + the PRINCIPAL (Denson Smith).
**Status:** FINALIZED — diagnosis verified against current main; dispatch-ready.
**Builds on:** current the-stoa main (`3b0bc4f`). Charter ticket: `stoa--5ju` (read it + comments).

**You are MAJOR_PLINY for the the-stoa Arc 66 engagement.** Read `.claude/MAJOR_PLINY.md` and assume the orchestrator role. Open Claude Code in `C:\Users\denso\claude_projects\the-stoa\`.

**Your one job:** fix `check-substrate-updates` (and the install.sh manifest writer) so that **CHIRON + HAMILTON — and any future MAJOR — are visible to the update path**. Today the update path silently omits the design layer when bringing an existing-Stoa project current. Make the MAJOR set auto-discovered, not hardcoded.

---

## Why this matters (the live trigger)

Surfaced by the live CHIRON/HAMILTON shakedown (`u--k8z` / `nws-oq8`, 2026-06-18): A2A ran the `deploy-stoa` update path against an existing-Stoa project; the read-only `check.sh` reported CHIRON + HAMILTON as **neither drifted nor missing**. So `deploy-stoa`'s EXISTING-project branch (→ `check-substrate-updates`) **does not deliver the design layer** — `apply.sh` would bring the arc-63–65 drift but silently skip CHIRON/HAMILTON. A *fresh* `install.sh` deploys them; the gap is the **update path only**. The shakedown is **PAUSED** awaiting this fix on main (pause-to-fix; do NOT work around).

---

## Verified diagnosis (do NOT re-derive — confirm, then fix)

Confirmed against current main. The MAJOR set is hardcoded in several places while CAPTAINs/templates/skills are auto-discovered:

- **PRIMARY — `check.sh` `enumerate_deployed()` (`substrate/skills/check-substrate-updates/check.sh:401-408`).** Hardcodes the expected MAJOR set to `POLYBIUS` + `PLINY`. CAPTAINs are `glob substrate/CAPTAIN_*.md`, templates are glob, skills are `parse install.sh SKILL_NAMES` — MAJORs are the lone hardcoded anomaly. CHIRON/HAMILTON never enumerated ⇒ invisible to MISSING detection. **This is the root cause of the symptom.**
- **SECONDARY (same hardcoded-POLYBIUS/PLINY pattern; needed for full correctness once the seats deploy):**
  - `check.sh` `source_path_for_deployed()` (`:294-298`) — deployed-MAJOR→source map; needed for DRIFTED detection.
  - `check.sh` `apply_substitutions()` (`:119`, the `.claude/MAJOR_POLYBIUS*.md|...PLINY*.md|...CAPTAIN_*.md` case) — needed for subproject-tier NAME_SUFFIX byte-compare.
  - `install.sh` `write_substrate_manifest()` (`:540-544`) — emits manifest lines for POLYBIUS/PLINY only; needed for deploy-time manifest completeness. (This was the locus A2A originally cited — real, but NOT the cause of the MISSING-detection symptom, because the manifest does not drive `enumerate_deployed`.)

---

## Fix shape (the intended approach — DAEDALUS refines)

**Make MAJOR enumeration glob-derived**, mirroring the CAPTAIN auto-discovery already in `enumerate_deployed()` (glob `${SUBSTRATE_DIR}/MAJOR_*.md`), so any future MAJOR auto-discovers and this bug class cannot recur. Apply the same de-hardcoding to `source_path_for_deployed()`, the `apply_substitutions()` case, and `write_substrate_manifest()`.

**CRITICAL tier/suffix check (DAEDALUS must resolve before ADA builds):** MAJOR suffix rules are not uniform. Verify against `install.sh` `DEST_*` logic (`:955-963`) exactly how CHIRON/HAMILTON are suffixed at each tier (user / project / subproject) and make every enumeration site match that reality. Do not assume CHIRON/HAMILTON follow the POLYBIUS/PLINY suffix pattern — confirm it. A wrong suffix here produces false MISSING/OBSOLETE pairs (the silent-overwrite-adjacent footgun).

---

## Deliverables

1. `check.sh` `enumerate_deployed()` — MAJOR set glob-derived from `substrate/MAJOR_*.md`, tier/suffix-correct.
2. `check.sh` `source_path_for_deployed()` + `apply_substitutions()` — handle every MAJOR (not just POLYBIUS/PLINY).
3. `install.sh` `write_substrate_manifest()` — emit manifest lines for every MAJOR (glob-derived or explicitly including CHIRON/HAMILTON), suffix-correct per tier.
4. Keep the app green and the existing FAIL-LOUD subproject recompose green.

---

## Definition of done

- **REAL (non-dry-run) probe:** deploy current substrate to a throwaway dir via `install.sh --target project`; remove the deployed `MAJOR_CHIRON.md` + `MAJOR_HAMILTON.md` (simulating a pre-design-layer deployment); run `check.sh --workspace <throwaway>` → **CHIRON + HAMILTON now report MISSING** (pre-fix they do not — capture that falsification baseline first); `apply.sh` delivers them; re-run `check.sh` → clean. Repeat the relevant slice at subproject tier to exercise the suffix path.
- The existing FAIL-LOUD subproject recompose Checks A–E stay green via a **real** recompose (probe V3) — `--dry-run` early-returns before the awk checks and cannot exercise them.
- `cd app && npm run gen-data && npm run build && npm test` green. (Expected app-neutral — this is tooling, not role files — but a regen re-derives the whole roster, so assert from the full run, not from "no role file changed.")
- `grep` shows no remaining hardcoded `POLYBIUS`/`PLINY`-only MAJOR list at the four loci.
- **NOMOS CONFORMANT** on the final commit.
- Committed + pushed to `the-stoa` main; `stoa--5ju` updated with the landing SHA + closed.

---

## Out of scope

- The role files (`MAJOR_*.md`) themselves — untouched.
- Any broader `check-substrate-updates` refactor beyond the MAJOR-enumeration completeness fix.
- `deploy-stoa` / `install-stoa` skills — they are correct; the bug is downstream in `check-substrate-updates`.
- The `u--k5s` CRLF `agents.ts` item — separate, do not fold in.
- zeotek_newswire (A2A's project) — do NOT touch; the probe uses a throwaway.

---

## Discipline

- Run the full gauntlet (DAEDALUS design → ARGUS → ADA → VERA → CATO → NOMOS) — this is FAIL-LOUD-adjacent tooling with tier/suffix subtleties; not mechanical.
- Verify-then-execute; the FAIL-LOUD recompose is FAIL-LOUD by design — do not silence a check to make it pass.
- bw syntax: positional `bw comment`; `bw prime` at activation; `--reason` on close.
- Hand back at CATO PASS to the floor-manager (POLYBIUS_the-stoa), not direct to user-tier.

Standby, run.

---

## Post-landing close-gate correction (2026-06-18, user-tier POLYBIUS close-gate; merge `c761db9`)

Two corrections to the verified-diagnosis + DoD above, per the "directive DoD must match tool reality" discipline (Arc-61 `cde20b3` precedent):

1. **The locus-list under-enumerated — the fix is 6 loci, not 4.** The diagnosis named 4 loci (check.sh ×3 + install.sh manifest) and believed them complete. It missed `apply.sh`'s OWN duplicate copies of two of those functions, carrying the IDENTICAL hardcoded MAJOR enumeration: **`apply.sh:97`** (`apply_substitutions` case) + **`apply.sh:185-186`** (`source_path_for_deployed`). `apply.sh` (the writer half of check-substrate-updates) was always in-scope — the problem statement (L16) names its skip behaviour as part of the bug, the DoD (L51) expects its delivery, and it is not in Out-of-scope. The gap was the locus-list, not the scope. Caught by VERA's V2 (DRIFTED-delivery FAIL), fixed by the in-scope EXPAND (`9e1768a`).
2. **DoD L51 mechanism correction.** "`apply.sh` delivers them" is mechanically imprecise: `apply.sh --all-differing` harvests **DRIFTED-prefix lines only** (check.sh prefix invariant; apply.sh:306). **MISSING** seats (the CHIRON/HAMILTON existing-project case A2A hit) are delivered by an **`install.sh` re-run** per check.sh's routing footer, NOT apply.sh. The visibility-flip (CHIRON/HAMILTON → MISSING) is the falsification baseline; apply.sh's role is the **DRIFTED**-MAJOR delivery path (now fixed at both tiers).

Lesson: at DIAGNOSIS time, grep ALL files of the affected subsystem for the bug pattern (not just the obvious file) AND verify the tool's flag-set + category-routing before writing the DoD. See `feedback-directive-dod-must-match-tool-reality`.
