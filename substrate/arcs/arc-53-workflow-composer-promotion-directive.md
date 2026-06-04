# Arc 53 — workflow-composer skill forge-promotion

**Epic / work-unit:** `stoa--04n` (workflow-composer forge-promotion). Part of the dynamic-workflows family (`stoa--3c9` tool-selection, `stoa--h2z` remediation-workflow, `stoa--aox` discipline-enforcement).
**Authority:** substrate canon change → full gauntlet per `MAJOR_PLINY.md §18.2`. Lower-stakes than Arc 52 (a skill promotion, not a security discipline) but still spec-authoritative.
**Prior Stage-A design:** `agents/design/stoa--04n/design.md` (the deploy-wiring half — still valid; this directive ADDS the skill-content-currency scope it predates).

---

## Why this arc

Promote the already-drafted `workflow-composer` skill (`substrate/skills/workflow-composer/SKILL.md`) from an on-disk-but-unwired source file into substrate canon, so `install.sh` deploys it to every workspace and `check-substrate-updates` drift-checks it like any base skill. It teaches the team the Stoa-specific layer on top of the generic Workflow tool (the *how-to-make* layer).

The skill draft was **refreshed 2026-06-01** by user-tier POLYBIUS with five corrections from the current Workflow docs (see `stoa--04n` doc-delta comment). This arc must promote the *current* skill, not regress it — so skill-content currency is an explicit verification target (§Verification below), not just deploy wiring.

## Scope (two things, both required)

**THING 1 — deploy wiring (from the prior design, unchanged):**
- Add `workflow-composer` to the `SKILL_NAMES` array in `substrate/install.sh` (the one-line edit that deploys + auto-enrolls it in drift-check; `check.sh` needs no edit — both drift passes live-parse `SKILL_NAMES`).
- Fix the stale `install.sh:140-144` cite in `check.sh` — it occurs at **FOUR** locations (76, 228, 385, 435), not one (Arc 52's ARGUS MAJOR-2 found the same class); correct all four to the post-edit line range.
- `npm run gen-data` in `app/` stays green (frontmatter unchanged; this is a guard, not a test of the deploy wiring — gen-data globs `substrate/skills/` independent of `SKILL_NAMES`).

**THING 2 — skill-content currency (the new scope this directive adds):** the promoted skill MUST be current as of the 2026-06-01 Workflow docs. The five deltas that MUST be present (they were folded into the draft 2026-06-01; the gauntlet verifies they survive promotion):
1. **Four-primitive framing** — the skill positions the gauntlet as a controlled composition of *agent-teams* (tier layer) + *subagents* (CAPTAIN layer), not a 3-way comparison. (§"Where workflows sit among the four orchestration primitives".)
2. **`ultracode` keyword** — the invocation keyword is `ultracode` (or natural language), NOT the pre-v2.1.160 literal `workflow`.
3. **`args` parameterization** — the saved-workflow `args` mechanism is documented as the reuse vehicle (worked case: `stoa--h2z` `/defeat-threat`).
4. **Allowlist / stall-fix** — pre-allowlisting commands before an autonomous run is named as the `stoa--x4j` fix (non-allowlisted shell/web/MCP still prompt; file edits auto-approve).
5. **Overnight ≠ workflow** — workflows are same-session-only; remote routines are the unattended vehicle.

## Locked decisions

1. **Skill content is final-as-refreshed.** The arc PROMOTES the current draft + verifies the 5 deltas; it does NOT re-author skill content. If the gauntlet finds a delta missing or wrong, that is a finding → fix in the build, not a content rewrite.
2. **No workflow-SCRIPT deploy infrastructure** (THING 2 of the prior design's scope-split — a `WORKFLOW_NAMES` deploy class for `.claude/workflows/`). No battle-tested `/gauntlet` script exists to promote; that is a separate later arc. This arc ships only the SKILL.
3. **Authorship immutable** — `author: Denson Smith` untouched.

## Verification (for VERA / CATO / ZENO)

Process/skill edits → coherence + currency + non-regression, not runtime probes:
- **Deploy:** `grep workflow-composer substrate/install.sh` hits inside `SKILL_NAMES`; dry-run install lists the skill deploy; `parse_skill_names_from_install` returns the new count including workflow-composer; no false-OBSOLETE.
- **Currency (the 5 deltas):** each of the five is present in the deployed skill — `grep -i 'agent team'`, `grep -i ultracode`, `grep '\bargs\b'`, `grep -i 'allowlist\|stoa--x4j'`, `grep -i 'remote routine\|unattended'` all hit; the stale `workflow`-as-keyword framing is GONE.
- **All four `check.sh` cite occurrences corrected** (not just one).
- `npm run gen-data` exits clean.
- Authorship: no author-like field touched; `author: Denson Smith` intact.

## Out of scope (deferred)

- The `WORKFLOW_NAMES` / `.claude/workflows/` deploy infrastructure (locked decision #2).
- The tool-selection discipline (`stoa--3c9`) — its own arc.
- The remediation workflow (`stoa--h2z`) — needs this skill landed first.
- Authoring any actual `/gauntlet` or `/defeat-threat` workflow script.
