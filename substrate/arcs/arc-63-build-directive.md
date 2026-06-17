# Arc 63 build directive — Skills-housekeeping pass A: SessionStart triggers + gauntlet-setup port

**Audience:** the fresh Claude Code session opened to build Arc 63 (PLINY_the-stoa via the gauntlet).
**Prepared at:** the user-tier POLYBIUS (chief-of-staff) seat, with the PRINCIPAL.
**Status:** DRAFT — pending PRINCIPAL go + NOMOS verification before dispatch. Decisions Q1–Q5 resolved (PRINCIPAL "go with your leans", 2026-06-17).
**Builds on:** the-stoa main `588bd88` (post-HAMILTON). Charter: `stoa--p41` (dispositions #2 + #5) + the coordination epic `stoa--p41.2`. Sibling: `stoa--92e` (gauntlet-setup port). This is **pass A** of a two-pass split; **pass B** (modules + save-verdict rewrite, Arc 64) is a SEPARATE later arc and OUT OF SCOPE here.

**You are MAJOR_PLINY for the Arc 63 engagement.** Read `substrate/MAJOR_PLINY.md` and assume the orchestrator role. Open Claude Code in `C:\Users\denso\claude_projects\the-stoa\`.

**Your one job:** move `check-substrate-updates` + `check-bw-release` off the orchestrator skill-menu onto a deterministic **SessionStart trigger**, and **port the `gauntlet-setup` skill into the substrate** — one coherent `install.sh`/`SKILL_NAMES` pass. Then return cleanly.

---

## Comms — async with user-tier POLYBIUS via bw

Coordinate on the epic `stoa--p41.2`. Surface to the floor-manager (POLYBIUS_the-stoa), not user-tier direct. `bw comment <id> "text"` is **positional, no `-m`**. Run `bw prime` at activation. Asymmetric polling (don't poll while working; do when waiting).

---

## Read first (the spec)

1. **`stoa--p41`** disposition #2 (SessionStart trigger + its guardrails) + #5 (KEPT skills) + the BLAST-RADIUS/app notes. **`stoa--p41.2`** (the epic — the full two-workstream scope + the resolved Q1–Q5).
2. **`stoa--92e`** — the gauntlet-setup port spec (copy `~/.claude/skills/gauntlet-setup/SKILL.md` → `substrate/skills/gauntlet-setup/SKILL.md` + add to `SKILL_NAMES`).
3. **`substrate/install.sh`** — `SKILL_NAMES` (the skill-deploy list) + the SessionStart-hook deploy path + `substrate/templates/settings-hooks.json` (the CANDIDATE hook-registration block).
4. **`.claude/hooks/README.md`** + `sessionstart-compact-reprime.sh` — the existing SessionStart command-hook pattern to mirror. **`.claude/hooks/` is the deploy target; the live `settings.json` is NEVER auto-written (HARD SAFETY CONSTRAINT below).**
5. **`substrate/skills/check-substrate-updates/`** (`check.sh` / `apply.sh` / `revert.sh`) + **`check-bw-release/check.sh`** — the existing check logic. Existing modules `substrate-update-check.md` + `bw-upgrade.md` carry the guidance.
6. **The Stoa app** — `app/scripts/gen-data-lib.ts` (`discoverSkillFiles` renders every `substrate/skills/<name>/` as a LIEUTENANT) + `app/src/data/__tests__/generated.test.ts` (the LIEUTENANT assertions).

---

## Verified premise (do NOT re-derive — but DO empirically confirm)

The substrate's hook docs say SessionStart `additionalContext` is "upstream-broken, no fix through v2.1.150." **That note is STALE.** Web-verified 2026-06-17 (gsearch): the v2.1.123 regression (issue #55889, all context-injection channels dropped) **was fixed** in subsequent releases **for `type:"command"` hooks defined in `.claude/hooks/` / settings.json** — which is exactly the substrate's hook type. Still broken ONLY for plugin-distributed hooks (#12151) and `mcp_tool`-type hooks — neither applies here.

**RESIDUAL (DAEDALUS must close):** local build is **v2.1.170** — past the last-known-broken 2.1.150 but the exact fix-version is unpinned. So:
- **P-EMPIRICAL (mandatory probe):** DAEDALUS/VERA must empirically confirm a `type:"command"` SessionStart hook's `additionalContext` actually reaches the model on the local build — not assume it from the search.
- **P-FALLBACK (mandatory design):** the trigger must be robust if surfacing regresses — the check **runs** and writes a drift-signal artifact (a file) that a RELIABLE carrier reads (the Stop self-check and/or CLAUDE.md, the substrate's proven channels), with `additionalContext` as the primary (now-working) carrier. Surfacing must never depend on additionalContext ALONE.
- **Doc-fix:** correct the stale "no fix through v2.1.150" note in `.claude/hooks/README.md` + `substrate/templates/settings-hooks.json` `_comment` to reflect the verified state.

---

## Settled — do NOT re-litigate (Q1–Q5 resolved)

- **Q3 = SPLIT.** This is pass A (SessionStart + gauntlet-setup port). Modules/save-verdict are pass B (Arc 64) — OUT.
- **Q4 = FOLD `stoa--92e` into pass A.** One `install.sh`/`SKILL_NAMES` pass.
- **Q5 = committed directive** (this file).
- Disposition #2 guardrails (LOCKED): THROTTLE (cache ~once/day per workspace), SURFACE-ON-SIGNAL-ONLY (silent when current; one line on drift/new-release), NON-BLOCKING (never gate session boot on a network call; fail-open on any error).
- **HARD SAFETY CONSTRAINT (inviolable):** no Arc auto-writes a live `settings.json`. The SessionStart trigger deploys as a command-hook script in `.claude/hooks/` + a registration entry in the CANDIDATE `settings-hooks.json`; arming it stays the existing operator-gated `--enable-hooks` step (DEFAULT OFF), targeting the install TARGET, never the running build session.

---

## Deliverables

1. **SessionStart trigger** — a `type:"command"` hook script (mirror `sessionstart-compact-reprime.sh`) that runs the `check-substrate-updates` + `check-bw-release` CHECK logic under the disposition-#2 guardrails (throttle/silent-when-current/non-blocking) and surfaces drift via `additionalContext` + the P-FALLBACK signal-file. Register it in `substrate/templates/settings-hooks.json` (candidate only).
2. **Retire the 2 check skills from the orchestrator menu** — remove `check-substrate-updates` + `check-bw-release` from `install.sh` `SKILL_NAMES`. **Design question for DAEDALUS:** the CHECK becomes the trigger, but `check-substrate-updates` also ships `apply.sh`/`revert.sh` (operator-invoked drift application) — decide their fate (keep as an operator-path tool vs fold), surface to the floor-manager before building. Do NOT silently drop the apply/revert capability.
3. **Port `gauntlet-setup` into the substrate (`stoa--92e`)** — copy `~/.claude/skills/gauntlet-setup/SKILL.md` → `substrate/skills/gauntlet-setup/SKILL.md`; add `gauntlet-setup` to `SKILL_NAMES`. (Net `SKILL_NAMES`: −2 check skills +1 gauntlet-setup.)
4. **Keep the app green** — `discoverSkillFiles` renders skills as LIEUTENANTs, so the net LIEUTENANT delta is −1: update `app/src/data/__tests__/generated.test.ts` to match the post-arc skill roster; `npm run gen-data && npm run build && npm test` green.
5. **Doc-fix** the stale SessionStart "broken" note (per Verified premise).

---

## Verification / Definition of done

- `substrate/install.sh --target user --dry-run` AND a **REAL (non-dry-run) subproject recompose** both pass (Arc-61 lesson: a `--dry-run` early-returns before the awk FAIL-LOUD Checks A–E; this arc adds no owned module, so the recompose should be unaffected — CONFIRM via a real recompose, not a dry-run).
- **P-EMPIRICAL green:** a real probe shows the SessionStart command-hook's `additionalContext` reaches the model on the local build; AND the P-FALLBACK signal-file path works independent of it.
- `cd app && npm run gen-data && npm run build && npm test` all green.
- `gauntlet-setup` deploys to a synthetic consumer's `.claude/skills/` (install dry-run confirms the landing path).
- **No live `settings.json` is written** by any build step (grep the diff — only `.claude/hooks/` + `templates/settings-hooks.json` change).
- Authorship: the commit keeps the PRINCIPAL's configured git identity as its author, plus the §28 seat-identity trailer for the building CAPTAIN (ADA); no author-like field in any changed file names a non-PRINCIPAL person.
- **NOMOS CONFORMANT** on the final commit. Committed + pushed; `stoa--p41.2` updated with the landing SHA + the pass-A close (the epic stays open for pass B).

---

## Out of scope

- **Pass B (Arc 64):** `save-verdict` / `validate-spec` / `inspect-script-output` → modules; the save-verdict Bash-only rewrite (sha256 kept inline) + attach-at-write; the no-Write review-seat tension (`stoa--7b1.1`). SEPARATE arc.
- **`credential-discipline`** (deferred until the new project version lands).
- The worktree-teardown ownership question (`stoa--9s6`) — separate.

## Discipline

- Full gauntlet (DAEDALUS → ARGUS → ADA → VERA → CATO → NOMOS) — this touches `install.sh` tooling + a hook + the app. Surface the design-lock (esp. the apply/revert fate + the P-EMPIRICAL/P-FALLBACK design) to the floor-manager before ADA.
- Verify-then-execute; web-verify any further tooling premise against current docs (gsearch), not memory.
- Fix-now for small related defects; ticket-with-plan if scope-different.

Standby, run.
