# Design — forge-promotion of the workflow-composer skill (stoa--04n)

**Stage:** Gauntlet Stage A (design), produced by the `gauntlet-design` workflow run `wf_0c5fa492-e9e` (STRABO → DAEDALUS → ARGUS, linear single-target).
**Audit verdict:** PARTIAL (ARGUS) — 2 MAJOR findings to resolve before the build stage runs.
**Status:** HARD STOP. One MAJOR resolved at source (skill edited); remainder folds into the build stage. Not yet built.

> This design was itself the battle-test target of the new `workflow-composer` skill + the `/gauntlet-design` workflow. The gauntlet caught a category error in the skill it was promoting — see "Audit" below.

---

## 1. Goal

Promote the already-on-disk `substrate/skills/workflow-composer/SKILL.md` from an unwired source file into substrate canon, so `install.sh` deploys it to every consumer workspace and `check-substrate-updates` drift-checks it like any base skill. Run via the gauntlet, not direct-to-main, per `MAJOR_POLYBIUS.md` §18.2 (`substrate/skills/*` edits are arc-only).

## 2. Deploy wiring (verified against source by STRABO + ARGUS)

**Single required edit:** add `workflow-composer` to the `SKILL_NAMES` array in `substrate/install.sh` (currently 8 entries at `install.sh:198-207`; order is not alphabetized, so append).

That one edit is **sufficient and complete** because:
- The source-existence guard (`install.sh:716-720`) iterates `SKILL_NAMES`; the dir + `SKILL.md` already exist on disk, so no error trips.
- The deploy loop (`install.sh:1107-1136`) iterates `SKILL_NAMES`: `rm -rf` dest → `cp -R src/. dest/` → strip pycache. Single-file skill, no Python, deploys verbatim at every tier (user/project/subproject), unsuffixed, no sed substitution.
- **No `check.sh` edit is required for drift enrollment.** Both drift passes key off `parse_skill_names_from_install()` (`check.sh:250-264`), which live-awk-parses the `SKILL_NAMES` array anchored on the literal `^SKILL_NAMES=\(` pattern — not line numbers, not a glob. Adding the name auto-enrolls it: Pass 1 reports MISSING on un-redeployed workspaces; Pass 2 (`is_substrate_source_present`) classifies it substrate-derived, never false-OBSOLETE.

## 3. Scope decision (the load-bearing call)

Two things were conflated by the skill's own draft prose and are separated here:
- **THING 1 — the `workflow-composer` SKILL** (markdown guidance). Ships in this arc via the one-line `SKILL_NAMES` edit. Fully covered by existing skill deploy + drift infra.
- **THING 2 — a canonical `/gauntlet` WORKFLOW SCRIPT** in `.claude/workflows/`. **Deferred** to a separate future arc. There is no battle-tested script to promote yet, and building deploy infra for a non-existent artifact mixes scopes (`§18.4` / `§5.9` bundled-scope guard).

## 4. Build-stage changes (for ADA, when the arc runs)

1. **REQUIRED** — `substrate/install.sh`: add `workflow-composer` to `SKILL_NAMES`. (The whole deploy wiring.)
2. **RESOLVED AT SOURCE (no longer ADA's job)** — the skill's deployment-table overclaim. See "Audit / MAJOR-1 resolution" below; the skill was corrected by POLYBIUS in the working-tree prototype, so the build stage inherits a clean skill.
3. **SHOULD-FIX (folds in)** — `check.sh` stale cite `install.sh:140-144` → actual `install.sh:198-207`. **Correct ALL FOUR occurrences** (`check.sh:76, 228, 385, 435`), not just one (ARGUS MAJOR-2); the awk still functions (anchors on the literal pattern), so this is stale-comment hygiene, and the arc re-shifts the line numbers by adding an array entry. This is a `substrate/skills/check-substrate-updates/check.sh` edit (substrate tooling) and therefore correctly arc-gated.
4. After edits: `npm run gen-data` in `app/` (project CLAUDE.md). NOTE per ARGUS MINOR: gen-data globs `substrate/skills/` and already discovers the skill independent of `SKILL_NAMES`, so this validates frontmatter, not the deploy wiring — keep it as a guard, but it does not test the arc's actual change.

## 5. Verification probes (for VERA)

1. `grep -n 'workflow-composer' substrate/install.sh` hits inside the `SKILL_NAMES` region.
2. Dry-run install into a **throwaway** synthetic target (per `operating-disciplines.md` §25.5 — fresh clone, never a real workspace) exits 0 and lists the skill deploy.
3. Real deploy into a throwaway target lands `<target>/.claude/skills/workflow-composer/SKILL.md` byte-identical (LF-normalized).
4. Drift MISSING path: synthetic workspace missing only this skill reports it MISSING (`+`).
5. Drift no-false-OBSOLETE: synthetic workspace with it deployed does not report it OBSOLETE.
6. Parser smoke: `parse_skill_names_from_install` returns 9 names incl. workflow-composer.
7. Skill prose no longer asserts non-existent infra: `grep 'ships here via' SKILL.md` → no hit. (Now satisfied at source.)
8. Scope check: `grep -ic 'workflow' substrate/install.sh` still 0; no `workflows/*` case in `check.sh source_path_for_deployed` (THING 2 stayed deferred).
9. `npm run gen-data` exits 0 (frontmatter guard — see §4 note).
10. Authorship intact: `author: Denson Smith` unchanged.
11. Cite fix: no `install.sh:140` survives in `check.sh` (all 4 corrected).

## 6. Audit (ARGUS — PARTIAL)

**MAJOR-1 (high) — RESOLVED AT SOURCE.** The skill's deployment table asserted a canonical `/gauntlet` "ships here via install.sh, drift-checked like any base file." The docs (https://code.claude.com/docs/en/workflows#save-the-workflow-for-reuse) say workflows are saved via the runtime `/workflows`→`s` save dialog into `.claude/workflows/` or `~/.claude/workflows/` — there is **no install.sh deploy mechanism for workflows**. The original draft (and DAEDALUS's softened rewording) baked a probably-wrong infra model into canon. **Resolution:** POLYBIUS rewrote the skill's Deployment section to (a) name the runtime save flow as the actual mechanism, (b) mark install.sh-deploy-of-workflows as an open future question, not existing infra, (c) record the provenance honestly. This removes the premise at the source rather than softening it downstream.

**MAJOR-2 (high) — FOLDS INTO BUILD.** The stale `install.sh:140-144` cite exists at FOUR locations in `check.sh` (76, 228, 385, 435), not one. ADA fixes all four (§4 item 3).

**MINORs:** gen-data probe tests the wrong invariant (§4 note); residual delta-only tension at the constraint table + pattern list (RESOLVED — POLYBIUS reframed both as pointer-to-tool + delta); `is_substrate_source_present` skills branch lacks an `[ -e ]` existence test (latent, not load-bearing for this arc — candidate follow-up).

**NIT:** keep `SKILL.md:144/:150` forge-promotion framing consistent with the reworded deployment table (verified consistent post-edit).

## 7. Post-HARD-STOP disposition

- MAJOR-1 + the two delta-only MINORs: **resolved in the skill prototype now** (working-tree, uncommitted).
- MAJOR-2 + remaining MINORs: **specified into the build stage** above.
- The design is now clean enough to proceed to a build stage when PRINCIPAL approves; the build is a one-line `SKILL_NAMES` add + the 4-cite `check.sh` correction + `gen-data` guard, run through ADA → VERA → CATO → ZENO.
- The `is_substrate_source_present` `[ -e ]` asymmetry is logged as a candidate separate follow-up (latent, not this arc).
