# Arc 64 build directive — Skills-housekeeping pass B: verdict/spec/inspection skills → modules + save-verdict rewrite

**Audience:** the fresh Claude Code session opened to build Arc 64 (PLINY_the-stoa via the gauntlet).
**Prepared at:** the user-tier POLYBIUS (chief-of-staff) seat, with the PRINCIPAL.
**Status:** DRAFT — pending NOMOS verification before dispatch. Q1–Q5 resolved (PRINCIPAL "go with your leans"); pass A (Arc 63) landed at main `6857414`.
**Builds on:** the-stoa main `6857414` (post-pass-A). Charter: `stoa--p41` (disposition #3) + the coordination epic `stoa--p41.2` (Workstream B). This is **pass B** — the modules + save-verdict rewrite. Pass A (SessionStart triggers + gauntlet-setup) is DONE; credential-discipline is OUT (deferred).

**You are MAJOR_PLINY for the Arc 64 engagement.** Read `substrate/MAJOR_PLINY.md` and assume the orchestrator role. Open Claude Code in `C:\Users\denso\claude_projects\the-stoa\`.

**Your one job:** move `save-verdict` + `validate-spec` + `inspect-script-output` off the orchestrator skill-menu into **modules** the dispatched specialist Reads at dispatch; **rewrite save-verdict** as a Bash-only module that also **attaches the verdict to bw at write-time** (the verdict-preservation fix); and resolve the read-only-review-seat no-Write tension. Then return cleanly.

---

## Comms — async with user-tier POLYBIUS via bw

Coordinate on the epic `stoa--p41.2`. Surface to the floor-manager (POLYBIUS_the-stoa), not user-tier direct. `bw comment <id> "text"` is **positional, no `-m`**. Run `bw prime` at activation. Asymmetric polling.

---

## Read first (the spec)

1. **`stoa--p41`** disposition #3 (the modules disposition: save-verdict drops its script for Bash-only authoring baked into the module; retires `stoa--j2i`/`1ne`/`xyn`/`7b1.8`; resolve `stoa--7b1.1` in the same arc) + **`stoa--p41.2`** Workstream B.
2. **`substrate/skills/save-verdict/`** — `SKILL.md` + `_save_verdict.py` + `_lib`. Understand exactly what the script enforces today (canonical path computation `agents/verdicts/<ticket>/<officer>-<ts>.md`; sha256 round-trip; §15.4 verification-complexity shape validation; the threat-coverage empty-binding check `count>0 ⇒ ≥1 probe-id`, exit 4) BEFORE designing what the Bash-only module preserves vs drops.
3. **`substrate/skills/validate-spec/`** (`_check_runner.py` + `check.sh`) + **`substrate/skills/inspect-script-output/`** (`check.sh`). `inspect-script-output` relates to existing module `substrate/modules/mechanical-inspection-split.md`.
4. **The verdict-writing role files** — `substrate/CAPTAIN_VERA.md`, `CAPTAIN_ARGUS.md`, `CAPTAIN_CATO.md` ("Canonical verdict-save path" sections — they currently invoke the save-verdict skill via `python .../_save_verdict.py`). These repoint to the module.
5. **`stoa--7b1.1`** — the read-only-review-seat coherence tension (ARGUS/NOMOS/ZENO §4-no-Write vs §7-mandates-save-verdict; RECURRENCE-CLASS). Detail in `stoa--q3l` + `consolidated-substrate-friction.md`. **Fix once at the shared read-only-review-seat layer — affects ARGUS, NOMOS, ZENO together; do not patch one seat.**
6. **`substrate/install.sh`** — `SKILL_NAMES`; the module-deploy path; the FAIL-LOUD subproject-recompose machinery (`recompose_module_inline`, Checks A–E) IF any new module is subproject-deployed + MODULE-INLINE-coupled to a CAPTAIN role file.
7. **The Stoa app** — `app/scripts/gen-data-lib.ts` (`discoverSkillFiles` renders skills as LIEUTENANTs) + `app/src/data/__tests__/generated.test.ts`.

---

## Settled — do NOT re-litigate (Q1/Q2 resolved by PRINCIPAL)

- **Q1 → save-verdict drops the Python script** for Bash-only body-authoring baked into the module, **BUT the module keeps a lightweight inline sha256 round-trip check** — do not lose the integrity guarantee entirely.
- **Q2 → `validate-spec` + `inspect-script-output` keep their scripts CALLABLE** — the module is an instruction/when-to-use wrapper over the existing script, NOT a script-drop (only `save-verdict` was slated to drop code).
- **The Bash-only save-verdict module ADDS attach-at-write:** the verdict-writing seat attaches the written verdict to the coordination ticket on beadwork as part of the write, so a worktree teardown can never destroy it (the Arc-62 verdict-loss fix; `stoa--9s6` teardown-ownership is separate).
- **Retire** `stoa--j2i`/`1ne`/`xyn`/`7b1.8` (save-verdict Python-script bugs the Bash-only rewrite eliminates).

---

## Deliverables

1. **`save-verdict` → Bash-only module** (`substrate/modules/save-verdict.md`, the specialist Reads at dispatch): the canonical-path convention + the Bash-only body-authoring procedure (`printf` redirection, fully-quoting-safe) + the inline sha256 round-trip + **attach-to-bw-at-write**. `git rm` the `save-verdict` skill dir + its Python; remove `save-verdict` from `SKILL_NAMES`.
2. **`validate-spec` + `inspect-script-output` → modules** (instruction wrappers; scripts retained + callable). Remove both from `SKILL_NAMES`. `inspect-script-output` module coordinates with `mechanical-inspection-split.md`.
3. **Repoint the verdict-writing role files** — `CAPTAIN_VERA.md` / `CAPTAIN_ARGUS.md` / `CAPTAIN_CATO.md` "Canonical verdict-save path" sections: `Read .claude/modules/save-verdict.md` + follow its procedure, instead of invoking the skill.
4. **Resolve `stoa--7b1.1`** at the SHARED read-only-review-seat layer (ARGUS/NOMOS/ZENO): reconcile §4-no-Write with §7-mandates-save-verdict — the Bash-only module (author via `printf`, no Write tool) is the mechanism that dissolves the tension; make the §4/§7 language coherent for all three seats together.
5. **`install.sh`** — `SKILL_NAMES` −3 (save-verdict, validate-spec, inspect-script-output); deploy the 3 new modules. IF any module is subproject-deployed + MODULE-INLINE-coupled to a CAPTAIN role file, add the recompose ownership-partition entry + verify FAIL-LOUD Checks A–E green via a REAL recompose.
6. **Keep the app green** — `discoverSkillFiles` renders skills as LIEUTENANTs, so the net LIEUTENANT delta is −3: update `app/src/data/__tests__/generated.test.ts`; `npm run gen-data && npm run build && npm test` green.

---

## Verification / Definition of done

- **Attach-at-write probe (load-bearing):** a verdict written via the new `save-verdict` module lands on beadwork attached to its ticket (not just on worktree disk) — exercise it, do not assume.
- **No-Write-seat probe:** confirm a read-only-review seat (no Write tool, Bash only) can author + write + attach a verdict via the module's `printf` procedure — this is the `stoa--7b1.1` resolution working in practice.
- **sha256 integrity:** the module's inline round-trip catches a corrupted write (negative probe).
- `substrate/install.sh --target user --dry-run` passes; IF a module is subproject-recompose-owned, a **REAL (non-dry-run) subproject recompose** shows FAIL-LOUD Checks A–E green (Arc-61 lesson: a dry-run early-returns before the awk checks).
- `cd app && npm run gen-data && npm run build && npm test` all green.
- `grep -rn "skills/save-verdict\|skills/validate-spec\|skills/inspect-script-output" substrate/ app/` returns only intended module-pointer references (no dangling pointers to the retired skill dirs) outside `substrate/arcs/` + `substrate/v1-historical/`.
- Authorship: the build commit keeps the PRINCIPAL's configured git identity as its author, plus the §28 seat-identity trailer for the building CAPTAIN (ADA); no author-like field in any changed file names a non-PRINCIPAL person.
- **NOMOS CONFORMANT** on the final commit. Committed + pushed; `stoa--p41.2` updated with the landing SHA + the pass-B close. **This completes `p41.2`** — close the epic at pass-B landing (pass A + pass B both done; credential-discipline is a separate deferred item, not under this epic).

---

## Open design questions — surface to the floor-manager at design-lock (before ADA)

- **Q-A (save-verdict enforcement loss):** the Python enforced the §15.4 shape validation + the threat-coverage empty-binding check (exit 4) mechanically. Dropping it for a Bash-only module moves that to seat-side discipline. DAEDALUS: preserve the empty-binding check via a lightweight inline bash assert, or accept seat-side-only (document in the module + the seat role files)? Surface the tradeoff.
- **Q-B (7b1.1 shape):** the exact shared-review-seat §4/§7 reconciliation wording — propose it, do not just delete one clause.
- **Q-C (recompose coupling):** do the new modules need MODULE-INLINE markers + recompose ownership at subproject tier (like `pair-programmer-authoring`), or are they Read-at-dispatch-only (no subproject inlining)? This determines whether the FAIL-LOUD recompose machinery is in play.

---

## Out of scope

- **`credential-discipline`** (deferred until the new project version lands).
- Pass A (SessionStart triggers + gauntlet-setup) — DONE (Arc 63).
- The pass-A non-blocking follow-ups (`stoa--p41.3`/`p41.4`/`p41.5`) and the teardown-ownership question (`stoa--9s6`) — separate.
- The `z2b` authorship-gate fix — separate (this directive uses gate-safe prose as a stopgap).

## Discipline

- Full gauntlet (DAEDALUS → ARGUS → ADA → VERA → CATO → NOMOS) — touches `install.sh`, three CAPTAIN role files, the app, and a security-adjacent verdict-integrity mechanism. Surface the design-lock (Q-A/Q-B/Q-C) to the floor-manager before ADA.
- Verify-then-execute; web-verify any tooling premise against current docs (gsearch), not memory.
- Fix-now for small related defects; ticket-with-plan if scope-different.

Standby, run.
