# Arc 60 build directive — stoa--rdh: land the 3 new substrate skills + install.sh SKILL_NAMES wiring

**Ticket:** `stoa--rdh` (standalone ROADMAP). **Phase 1** of the "finish the Stoa → build the Marianne walkthrough" re-scope (PRINCIPAL, 2026-06-05). Phase 2 = `stoa--uob`/`sok`/`gis` (built using the skills this arc lands).
**Driver:** PLINY_the-stoa
**Drive mode:** **HITL / PRINCIPAL-gated, CO-DRIVEN — autonomous mode is PAUSED this engagement** (blocked on `stoa--x4j`: autonomous-mode gauntlet silently blocks on a sub-agent permission prompt). No polling-cron autonomy; the team advances only while user-tier/PRINCIPAL is in the loop. HARD STOP (post-ARGUS) surfaces the design to POLYBIUS_the-stoa floor-manager → user-tier. Do NOT autonomous-ship; user-tier holds close-gate + merge.
**Worktree:** `.claude/worktrees/arc-60-build` (branch `arc-60/build`)
**Gauntlet:** DAEDALUS → ARGUS → **[HARD STOP]** → ADA → VERA → CATO → NOMOS → ZENO

## Context — what this arc is
Three LIEUTENANT skills were authored during the debloat engagement (2026-06-04/05) and held UNCOMMITTED because substrate canon needs an arc, not a direct-to-main. This arc version-controls them + wires deployment per-skill by readiness. They exist NOW as untracked dirs under `substrate/skills/`:
- `decision-surface/` — dilemma-vs-problem decision-support logic + `worked-example-debloat.md`. **`status: DRAFT (v0.1)`**, carries 6 open questions in its own frontmatter.
- `interactive-html-preview/` — verified Preview build→serve→render→verify mechanics. Consumer-general; ready.
- `team-launcher/` — verified `wt`/`claude` launch mechanics; pairs with `launch-team.ps1` at the the-stoa repo root. **the-stoa-specific** (see §4).

`substrate/install.sh` is already modified (held): `interactive-html-preview` added to `SKILL_NAMES`. That held change is CORRECT as-is (see §2); do not revert it.

## What "done" is — land all 3 in-repo; DEPLOY per-skill by readiness (the load-bearing precision)

1. **Commit all 3 skill dirs** to `substrate/skills/`. Authorship: all 3 already carry `author: Denson Smith` — VERIFY unchanged; make NO author-field edits.

2. **`interactive-html-preview` → WIRE into `SKILL_NAMES` (DEPLOY).** Verified + consumer-general (the render layer decision-surface depends on). This is exactly the existing held `install.sh` change — keep it.

3. **`decision-surface` → LAND in-repo, HOLD OUT of `SKILL_NAMES` (do NOT deploy yet).** It's DRAFT; its own open-Q #6 says "gauntlet-ship = add to `SKILL_NAMES` once the open questions settle," and Phase 2 (building the consumer surface) is where they settle. So: commit the dir; do NOT add it to `SKILL_NAMES` this arc. (PRINCIPAL-confirmed: land DRAFT, finish in Phase 2.)

4. **`team-launcher` → DAEDALUS design decision (justify it).** As written it is the-stoa-specific: it references `launch-team.ps1` at the repo root + `HUMAN_paste-*-init.md` activation files that do NOT deploy into a consumer `.claude/`. Deploying it as-is hands a consumer a skill with dangling references. Two options:
   - **(a) HOLD out of `SKILL_NAMES`** — land in-repo as a builder-tier/the-stoa-internal skill, defer consumer-generalization to a later arc. **← recommended for this arc's tight scope.**
   - **(b) GENERALIZE** (deploy the launcher + de-the-stoa the paste refs) so it's consumer-safe, then wire it.
   Recommend (a); flag generalization as a follow-up ticket if (a).

5. **gen-data stays valid.** `app/scripts/gen-data.ts` reads `substrate/skills/` as LIEUTENANTs + validates frontmatter against a Zod schema. Run `cd app && npm run gen-data`; confirm no Zod error and the new skills appear. (Pre-verified green 2026-06-05 with all 3 dirs present; re-confirm post-edit.)

6. **install.sh smoke-test against a synthetic parent.** With the FINAL `SKILL_NAMES`, run `install.sh --target project --project-dir <scratch> --dry-run` then for real, confirming: validation passes (every named skill dir exists), the deployed skills land, no obsolete-file warnings for the new ones. (Committed-state install verified green from a clean clone on Windows/git-bash 2026-06-05; re-verify with the new manifest.)

## Scope / constraints
- **IN:** `substrate/skills/{decision-surface,interactive-html-preview,team-launcher}/` (commit); `substrate/install.sh` `SKILL_NAMES` (interactive-html-preview only this arc — the held +1 line is correct). `app/src/data/generated/agents.ts` ONLY as a regenerated gen-data output (never hand-edited).
- **OUT:** finishing decision-surface's 6 open questions (Phase 2); generalizing team-launcher for consumer deploy (later arc, if §4 picks (a)); the `sp1` 7–8 ported utility skills (deferred); ANY role-file / operating-disciplines / template edits (this arc is skills + install.sh only — the surgical autonomous-pause is a SEPARATE change, not this arc).
- **Voice:** substrate v2 (PRINCIPAL/HUMAN; no second-person-for-human).
- **Authorship:** the 3 skills already say `author: Denson Smith` — VERIFY unchanged; NO author-field edits anywhere.
- **Per-CAPTAIN seat-identity** per §28.
- **Autonomous mode PAUSED** (drive-mode header) — co-driven only; no polling-cron autonomy.

## Probes (VERA — refine)
- **P1 (the Marianne path):** a fresh-clone dry-run + real `install.sh --target project` to a scratch project succeeds; install.sh validation passes; every `SKILL_NAMES` entry resolves to a deployed `<dest>/.claude/skills/<name>/SKILL.md`.
- **P2:** `decision-surface` is committed to `substrate/skills/` BUT absent from `SKILL_NAMES` AND absent from the scratch deploy (land-but-don't-deploy holds on all three checks).
- **P3:** `interactive-html-preview` IS in `SKILL_NAMES` and DOES deploy.
- **P4:** team-launcher matches DAEDALUS's decision — if held: in-repo, not in `SKILL_NAMES`, not deployed; if generalized: the deployed copy has NO dangling repo-root references.
- **P5:** `gen-data` runs clean (Zod valid), all skills present in `agents.ts`; `npm run build` succeeds (no app regression).
- **P6:** authorship — `author: Denson Smith` on all 3 skills, unchanged; no author-field touched anywhere in the diff.

## HARD STOP note (post-ARGUS, before ADA)
Confirm: (1) per-skill `SKILL_NAMES` wiring is correct — DEPLOY interactive-html-preview, HOLD decision-surface (DRAFT), team-launcher per justified decision; (2) no consumer receives a skill with dangling refs; (3) gen-data + install smoke-test both green; (4) authorship unchanged; (5) autonomous mode stays PAUSED (co-driven). This is a low-risk additive arc — the one real design call is §4 (team-launcher).
