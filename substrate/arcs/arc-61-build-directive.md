# Arc 61 build directive — MAJOR_CHIRON seat + agent-author retirement + POLYBIUS §11 relocation

**Audience:** the fresh Claude Code session opened to build Arc 61.
**Authored by:** user-tier POLYBIUS (chief-of-staff) + the PRINCIPAL (Denson Smith).
**Status:** FINALIZED — all open design items (O1/O2/O3) resolved by PRINCIPAL 2026-06-16; NOMOS-verified; dispatch-ready. NOT yet dispatched — activate on PRINCIPAL go.
**Builds on:** current the-stoa main (`5699292`). Charter: `stoa--p41` (read it + ALL its comments — the CHIRON charter, the model-philosophy refinement, the retire-decision, and the BLAST-RADIUS finding are the spec). Sibling seat `MAJOR_HAMILTON` (`stoa--yh2`) is a SEPARATE arc — out of scope here.

**You are MAJOR_PLINY for the the-stoa Arc 61 engagement.** Read `substrate/MAJOR_PLINY.md` and assume the orchestrator role. Open Claude Code in `C:\Users\denso\claude_projects\the-stoa\`.

**Your one job:** land **MAJOR_CHIRON** (the design-time TEAM-ARCHITECT seat) and execute the coupled cascade that comes with it — retire the `agent-author` skill (its capability is now inlined in `MAJOR_CHIRON.md` §7), relocate POLYBIUS §11 (authoring → CHIRON), resolve the `pair-programmer-authoring.md` module + install.sh recompose coupling, fix the dangling references, and keep the Stoa app + its tests green. Then return cleanly.

**This is a LARGE arc.** It touches substrate canon (two MAJOR role files), install.sh tooling INCLUDING the FAIL-LOUD subproject-recompose machinery, a module, the Stoa app's `gen-data` adapter + tests, and 4–5 cross-references. Run the full gauntlet (DAEDALUS design → ARGUS → ADA → VERA → CATO → NOMOS). Surface the open decisions (below) before locking the build.

---

## Comms — async with POLYBIUS via bw (`stoa--*`)

Coordinate via comments on the Arc 61 epic (file under / linked to `stoa--p41`). PRINCIPAL is not the relay for routine status — beadwork is. Asymmetric polling: don't poll while working; do poll when waiting (between phases / after surface) via `CronCreate */5`. `bw comment <id> "text"` is **positional, no `-m`**. Run `bw prime` at activation.

---

## Read first (the spec)

1. **`stoa--p41`** — the charter. Read the body + every comment. The load-bearing ones: the CHIRON charter, the model-assignment philosophy (performance-first / saturation-gated), the **retire-agent-author decision**, and the **BLAST-RADIUS finding** (the full cascade this arc must handle coherently).
2. **`substrate/MAJOR_CHIRON.md`** — the v1 seat draft (working tree, uncommitted). This is the seat to land; review/refine, don't re-derive. §7 is the inlined agent-author capability (skill-shape, but instruction — exclusive by construction).
3. **`docs/major-chiron.html`** — the rendered view of the role file (regenerate if the `.md` changes).
4. **`substrate/arcs/arc-17-build-directive.md`** — the arc that BUILT what you're relocating (POLYBIUS §11/§12 + the agent-author skill + the LIEUTENANT deploy). This is your "what's being undone" map.
5. **`substrate/install.sh`** — `SKILL_NAMES` (line ~227) + the **FAIL-LOUD subproject-recompose machinery** (`recompose_module_inline`, ~line 1014; Checks A/B/C/D/E). Understand the marker↔module↔ownership-partition coupling BEFORE editing §11.
6. **`substrate/modules/pair-programmer-authoring.md`** — currently POLYBIUS §11's detail module; it **invokes the agent-author skill** (line ~39) and is `MODULE-INLINE`-coupled to POLYBIUS §11.
7. **The Stoa app** — `app/scripts/gen-data.ts` (the adapter that reads skills into the roster) + `app/src/data/__tests__/generated.test.ts` (the LIEUTENANT-slot expectation, from Arc 17.1).

---

## Settled — do NOT re-litigate

From the charter:
- **CHIRON is a MAJOR, design-time TEAM-ARCHITECT.** Answers to POLYBIUS (who keeps review-literacy + roster control); does not command PLINY; co-designs with HAMILTON.
- **The agent-author capability is inlined into `MAJOR_CHIRON.md` §7** (developed skill-shape, lives as instruction). Exclusivity is **by construction** — no scoping mechanism needed (this dissolved the earlier (a)/(b) question).
- **The standalone `agent-author` skill is RETIRED** (capability now lives in CHIRON §7).
- **POLYBIUS sheds the authoring tool, keeps the review-literacy.**

Resolved by PRINCIPAL 2026-06-16 (were the open design items O1/O2/O3):
- **O1 → RE-HOME the module.** `pair-programmer-authoring.md` re-homes as a **CHIRON-owned** module (slim-core): `MAJOR_CHIRON.md` hosts it via a MODULE-INLINE-markered stub; the install.sh recompose **ownership partition reassigns it POLYBIUS → CHIRON**; the module's "Invoke the agent-author skill" line (~:39) repoints to CHIRON §7. All FAIL-LOUD recompose checks (A/B/C/D/E) must be green at a subproject dry-run. *Fallback only if DAEDALUS finds the module's unique content (lineage + pair-programmer framing) thin and mostly subsumed by §7: fold essentials into §7 + retire — surface that to POLYBIUS first.*
- **O2 → DEPLOY EVERYWHERE.** `MAJOR_CHIRON` deploys at ALL tiers (user + project + subproject), suffixed `CHIRON_<slug>` at project/subproject parallel to POLYBIUS/PLINY. Standing-but-dormant architect — available wherever a team lives, engaged only for design work.
- **O3 → slot stays populated.** Removing `agent-author` does NOT empty the LIEUTENANT slot: `gen-data-lib.ts` `discoverSkillFiles` renders ALL substrate skills (12 → 11 remain), so the count-assertion still passes. The ONLY app change is `app/src/data/__tests__/generated.test.ts:92` (`toContain("agent-author")`).

---

## Deliverables (the coupled cascade — land together)

1. **Land `MAJOR_CHIRON.md`** — review/refine the draft to final; regenerate `docs/major-chiron.html`.
2. **Wire CHIRON deploy in `install.sh`** — deploy `MAJOR_CHIRON` at ALL tiers (user + project + subproject), suffixed `CHIRON_<slug>` at project/subproject parallel to POLYBIUS/PLINY (O2=B). Add the deploy step alongside the existing MAJOR deploys; add the recompose ownership-partition entry assigning the re-homed `pair-programmer-authoring` module to CHIRON (per D5).
3. **Retire `agent-author`** — `git rm -r substrate/skills/agent-author/`; remove `agent-author` from `install.sh` `SKILL_NAMES`.
4. **Relocate POLYBIUS §11** — rewrite the §11 stub to point authoring at CHIRON (POLYBIUS reviews, doesn't author); update §3.5 **routing-map** (line ~71) + **relocation-index** (line ~84); fix the §7.6 cross-ref (line ~260, "pair-programmer activation flows (§11)").
5. **Re-home `pair-programmer-authoring.md` to CHIRON (O1)** — remove the §11 `MODULE-INLINE` marker from `MAJOR_POLYBIUS.md` (the module no longer inlines there); add a `MODULE-INLINE`-markered host stub in `MAJOR_CHIRON.md`; reassign the recompose ownership-partition POLYBIUS → CHIRON; repoint the module's "Invoke the agent-author skill" line (~:39) to CHIRON §7. Verify all FAIL-LOUD recompose checks (A/B/C/D/E) green at user AND subproject dry-runs.
6. **Fix dangling refs** — `operating-disciplines.md` (~§955 "via the agent-author skill"), `skills/check-substrate-updates/SKILL.md:58`, `skills/handoff-author/SKILL.md:185`, `install.sh:57` comment.
7. **Keep the app green (O3)** — update `app/src/data/__tests__/generated.test.ts:92` (drop/adjust the `toContain("agent-author")` assertion; the slot stays populated by the other 11 skills, so the count-assertion still passes — no adapter change needed). Then `npm run gen-data && npm run build && npm test` in `app/` all green.

---

## Verification / Definition of done

- `substrate/install.sh --target user --dry-run` AND a **subproject-tier dry-run** both pass (the recompose FAIL-LOUD checks stay green — this is the highest-risk surface).
- `cd app && npm run gen-data && npm run build && npm test` all pass.
- `grep -rn "agent-author" substrate/ app/` returns only the INTENDED CHIRON references (no dangling pointers to the retired skill).
- Voice audit: `grep -rni "colonel" substrate/ --exclude-dir=v1-historical` returns only deliberate reserved-rank refs; `grep -rni "the user" substrate/MAJOR_CHIRON.md` only the §7 voice-rule definitions.
- **NOMOS CONFORMANT** on the final commit (the orchestrator-output check).
- Committed + pushed to `the-stoa` main; `p41` updated with the landing SHA (do NOT close `p41` — it carries the other, separate skill re-homings).

---

## Out of scope

- **`MAJOR_HAMILTON`** (`stoa--yh2`) — its own arc. CHIRON lands independently (co-design coupling does not block the build).
- **The other `p41` skill re-homings** — check-substrate-updates/check-bw-release → SessionStart triggers; save-verdict/validate-spec/inspect-script-output → modules; credential-discipline. Each is a SEPARATE deliverable, NOT this arc. This arc is CHIRON + agent-author + §11 only.
- **A full POLYBIUS canon audit** beyond the §11 cascade (e.g., §17 base-vs-custom) — flag anything found via fix-now/ticket, don't expand scope.
- **`substrate/v1-historical/`** and archived arc directives.

---

## Discipline

- Run the full gauntlet — this touches canon + tooling + app; it is NOT mechanical.
- Verify-then-execute (`u--7yg.10`); One-job-per-agent (`u--7yg.17`) — resist drifting into HAMILTON or the other re-homings.
- Fix-now for small related defects (`stoa--8o4`); ticket-with-plan if scope-different.
- The recompose machinery is FAIL-LOUD by design — do not silence a check to make a dry-run pass; fix the underlying marker/module/partition consistency.
- bw syntax (`MAJOR_PLINY.md` §6.1): positional `bw comment`; `bw prime` at activation; `--reason` on close.

## Suggested phasing

- **Phase A — design (DAEDALUS).** Resolve O1/O2/O3 with POLYBIUS; produce the concrete edit plan for the recompose-partition + the app. Surface for a Colonel call before build.
- **Phase B — canon + tooling (ADA).** Land MAJOR_CHIRON, retire the skill, relocate §11, module fate, recompose-partition, refs, install.sh deploy.
- **Phase C — app (ADA).** gen-data + test green.
- **Phase D — verify (ARGUS/VERA/CATO/ZENO + NOMOS).** Recompose dry-runs, app build/test, voice audit, grep-for-dangling, ground-truth.
- **Phase E — ship.** Commit + push; update `p41` with the SHA.

Standby, run.
