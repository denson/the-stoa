# Arc 33 design — Mechanical-script / agent-inspection split

**Ticket:** `stoa--32b.2` (child of `stoa--32b` epic; sibling to `stoa--32b.1` shipped as Arc 31)
**Branch:** `arc-33/build` (worktree at `.claude/worktrees/arc-33-build/` per `MAJOR_PLINY.md` §5.9.4)
**Date:** 2026-05-17
**Status:** rev1 — AWAITING ARGUS cold audit
**Directive:** `substrate/arcs/arc-33-build-directive.md` (A1-A10 LOCKED)
**Authored by:** CAPTAIN_DAEDALUS_the_stoa, on behalf of the PRINCIPAL (Denson Smith).

---

## §1 — Intent (restatement per CAPTAIN_DAEDALUS §6.1 gate)

Arc 33 encodes the **mechanical-script / agent-inspection split** as a substrate pattern. Today's substrate puts recognition-of-strangeness inside scripts (Arc 26 grew `check.sh` from 489 → 934 lines to anticipate three new drift categories); PRINCIPAL declared 2026-05-16 that the recognition layer should move to an LLM-grade inspection-agent run after the mechanical script, with POLYBIUS triaging findings against the §25 PRINCIPAL-gate discipline. This arc ships the substrate **component** for that inspection layer (a new POLYBIUS-invokable skill), the **worked-example deployment** against the substrate-update flow (post-`apply.sh` / post-`install.sh` inspection with planted-strangeness probes), and the **discipline-doc canon** for when-to-apply the 3-step pattern. No mechanical enforcement of any specific discipline (§25 / §19.6 / §5.10 / §17 / §23) is shipped — those integrations are future-arc work per A7.

**Restatement convergence with brief (per §6.1):** the directive's "your one job" sentence (line 9) names *encode the split as a substrate pattern + worked example + discipline-doc addition*. The restatement above matches that scope. The one assumption imported beyond the directive's literal text: the worked example is a **probe-only deployment** of the skill — it ships with planted-strangeness test fixtures that demonstrate the inspection-agent shape, but does NOT auto-run after any production substrate operation. That distinction (worked-example-as-test-fixture vs. worked-example-as-production-integration) is the design's load-bearing reading of A7's hard-locked "no mechanical enforcement" boundary. If ARGUS reads the boundary differently, the worked-example scope is the place to push back.

**Imported assumptions named (per §6.1 + Arc 32 §2 model):**

- **A2 pick (α new skill) treated as DAEDALUS discretion, not PRINCIPAL-gate.** Directive A2 (line 81) explicitly delegates: *"DAEDALUS picks final form. If picking Option α, document why not β or γ (so future arcs reading this know the deferral rationale)."* No project-direction material rests on the choice; the picks rest on empirical precedent (check-bw-release / check-substrate-updates) and the §5.10 / §19.6 / §23 / §25 disciplines the skill would mechanically respect. Not a §25 gate.
- **A3 pick (`inspect-script-output`) treated as DAEDALUS discretion.** Directive A3 (line 91) explicitly delegates: *"DAEDALUS picks final form."* User-tier POLYBIUS lean recorded; matches DAEDALUS's pick on naming-honesty grounds (the name describes what the skill does, not the pattern it embodies). Not a §25 gate.
- **A4 pick (new top-level §27) treated as DAEDALUS discretion.** Directive A4 (line 105) gives two candidates (§11 area OR new top-level after §26). Folding the inspection-agent canon under §11 (autonomous-mode-setup) would re-conflate the cadence-vs-gate axes §25 explicitly distinguishes; the pattern needs its own top-level locus parallel to §23 / §25 / §26 (each PRINCIPAL-declared 2026-05-17 discipline gets its own home). Not a §25 gate.
- **A8 §15 N=1 framing.** §6.2 below carries the framing per scope-refresh comment + Arc 27/28/29/30/31/32 model. Empirical anchors named honestly: N=2 bit-by-it of make-script-comprehensive (Arc 26 + Arc 28's check.sh extensions); N=1 small-scope precedent (check-bw-release); discipline enters substrate canon off-gate on PRINCIPAL's 2026-05-16 declaration.
- **A6 authorship immutability.** The new SKILL.md frontmatter carries `author: Denson Smith` explicitly (§5 below). The new test fixtures, the new operating-disciplines.md section, the install.sh SKILL_NAMES append — none introduce other author names. §7.2 verification probe confirms.
- **A7 hard lock.** No edits to `check-substrate-updates/check.sh` or `check-bw-release/check.sh`. No new CAPTAIN seat. No multi-skill rollout. No PRINCIPAL-gate / attestation / signoff / scope mechanical enforcement. §4.5 names this explicitly inside the new SKILL.md so future readers of the skill itself land on the boundary.
- **The scope is comparable to Arc 29 / Arc 32.** Multi-file substrate canon + new skill component. Heavier than a discipline-only canonification arc (Arc 32 was 5 small candidates); roughly equivalent in surface to Arc 29's base-vs-custom convention.

---

## §2 — Inputs (read-first artifacts and their roles)

| Artifact | Role in this design |
|---|---|
| `substrate/arcs/arc-33-build-directive.md` (213 lines) | Load-bearing spec. A1-A10 LOCKED. Architectural decisions NOT re-opened. |
| `bw show stoa--32b.2` body + 2026-05-17T19:14:17Z scope-refresh comment | Primary input prose alongside directive. The refresh comment locks A2 lean toward Option α and A3 lean toward `inspect-script-output`; both treated here as DAEDALUS-discretion picks with rationale named. |
| `docs/sessions/2026-05-16-substrate-update-architecture-reframe--retro.md` §8 (load-bearing source for 3-step pattern; §9 synthesis) | The PRINCIPAL declaration. §8 is the canonical articulation of "mechanical scripts; agents for intelligent inspection"; §9 synthesizes with §7's gate discipline (now shipped as §25). §15 N=1 framing in §6.2 cites these sections. |
| `substrate/operating-disciplines.md` §25 (lines 1163-1262) — PRINCIPAL-gate | The triage-step partner. Step 3 of the 3-step pattern hands gated findings to PRINCIPAL per §25.3 BLOCK-not-TAG. The new SKILL.md prose cites §25 at the triage-step description. |
| `substrate/operating-disciplines.md` §19.6 (lines 849-894) — attestation-confabulation | Future-integration candidate (NOT shipped here per A7). The new SKILL.md mentions §19.6 in its "what the inspection-agent layer would mechanically enforce" futures list. The skill itself does NOT check attestations in this arc. |
| `substrate/operating-disciplines.md` §23 (lines 1085-1138) — base-vs-custom universal | The scoping discipline the inspection-agent layer MUST respect. The skill inspects BASE workspace state only (paths matching §23.2 base-paths); CUSTOM paths are operator-owned. §4.4 below names this. |
| `substrate/operating-disciplines.md` §6.7.1 (lines 81-93) — N=1 promotion gate | §6.2 honesty framing defers to §6.7.1 per A8; same shape as Arc 27/28/29/30/31/32 sections. |
| `substrate/MAJOR_PLINY.md` §5.10 (lines 422-460) — signoff-accuracy | Future-integration candidate (NOT shipped here per A7). The new SKILL.md mentions §5.10 in its futures list (the inspection-agent layer could verify post-signoff cleanup claims). |
| `substrate/MAJOR_PLINY.md` §5.9 + §5.9.4 (lines 329-421 area) | Self-applied for this arc per A9: worktree at `.claude/worktrees/arc-33-build/` confirmed; pre-branch hygiene PASS per PLINY's init handshake. |
| `substrate/MAJOR_POLYBIUS.md` §17 (lines 1050-1121) — base-vs-custom POLYBIUS refinement | The POLYBIUS-tier cut of the §23 scoping discipline; cross-ref from new SKILL.md to §17 alongside §23. |
| `substrate/skills/check-bw-release/SKILL.md` (122 lines) + `check.sh` (222 lines) | Small inspection-shape skill precedent (Arc 28). The new SKILL.md frontmatter shape, the env-var fixture mechanism, the per-workspace state pattern, the cite-comment discipline at API boundaries all copy from this skill. **Author: Denson Smith confirmed in frontmatter** (line 4). |
| `substrate/skills/check-substrate-updates/SKILL.md` (202 lines) + `check.sh` (934 lines) | The larger inspection-shape skill — the NEGATIVE empirical anchor for script-bloat. NOT modified per A7. Referenced in §6.2 as the empirical anchor for "what intelligence-in-script grows into." |
| `substrate/install.sh` lines 141-146 (SKILL_NAMES array) | The deploy register. Option α append target. Live state confirmed: array currently lists `agent-author / check-substrate-updates / credential-discipline / check-bw-release` (4 entries). Append target is line 146 (between `check-bw-release` and the closing `)`). |
| `agents/design/arc-32/design.md` | Style + structure model for substrate-canon design artifacts (§1 restatement-gate framing, §3 per-candidate scoping, §4 deliverables, §5 authorship audit, §6 N=1 framing, §7 verification probes, §8 self-assessed weak points). |

**Live ground state at design-authoring time (per §19.6 attestation-honesty):**

- `git rev-parse HEAD` in main worktree = `b600df7` (matches PLINY's init handshake on `stoa--32b.2`); `git rev-parse origin/main` = `b600df7`; identical.
- arc-33/build worktree exists at `.claude/worktrees/arc-33-build/`; current branch in that worktree is `arc-33/build`.
- `agents/design/arc-33/` is created by this design write (did not exist prior); `design.md` is the first file in it.

---

## §3 — Architectural decisions resolved (A2 / A3 / A4 picks)

### §3.1 — A2 pick: Option α (new substrate-tier skill)

**Pick:** Option α. New substrate-tier skill at `substrate/skills/inspect-script-output/` mirroring the shape of `substrate/skills/check-bw-release/`.

**Rationale (why not β, why not γ):**

- **Option β (CAPTAIN_VERA envelope extension) rejected.** VERA is *verifier-of-arc-deliverables* — its envelope is shaped around "did the build under this dispatch ship the artifact the spec asked for, run the probes the design named, produce the verdict in the verdict shape." That domain is different from *verifier-of-mechanical-script-outputs in production substrate operations*. The two domains share the word "verify" but the contracts are structurally different: VERA's probes are scoped to the dispatch's build artifacts; the inspection-agent's scope is the workspace state surrounding any mechanical substrate operation. Folding the two into one CAPTAIN envelope would either narrow VERA's gauntlet-pipeline role or over-broaden the inspection-agent role; neither serves clarity. The directive's A2 risk-note (line 76) — *"VERA is verifier-of-arc-deliverables; inspection-agent is verifier-of-mechanical-script-outputs; different domains"* — is the operative reason.

- **Option γ (new CAPTAIN seat e.g. CAPTAIN_INSPECTOR) deferred.** A new CAPTAIN seat is a structural pipeline component PLINY dispatches as a phase; weight comparable to introducing CAPTAIN_ARGUS or CAPTAIN_CATO. The 3-step pattern at retro §8/§9 names POLYBIUS as the dispatcher (not PLINY); the inspection-agent runs AFTER a mechanical operation by POLYBIUS invocation, not as part of a gauntlet phase. A CAPTAIN seat would be the right shape if the inspection layer were a gauntlet-pipeline component; today it is a POLYBIUS-invoked post-mechanical layer. If the skill pattern proves out across 2-3 future arcs (per A7's "incremental adoption" boundary) AND a gauntlet-pipeline integration becomes warranted, a future arc can promote the skill to a CAPTAIN seat — the deferral is intentional.

- **Option α justifications:**
  1. **Empirical precedent.** check-bw-release (Arc 28) shipped as a small inspection-shape skill and is working without script-bloat. The shape is known.
  2. **Lightest deploy.** Append one entry to `install.sh` SKILL_NAMES (line 146). No changes to PLINY's gauntlet pipeline, no new CAPTAIN role-file deployment, no rename / scope-rotation in any existing envelope.
  3. **Lightest deprecate.** If the pattern doesn't prove out (per A8 N=1 caveat), removing the skill is one `install.sh --prune-obsolete` and one removal from SKILL_NAMES — no envelope rewriting.
  4. **POLYBIUS-invokable matches the 3-step pattern.** Step 3 (POLYBIUS triage) presupposes POLYBIUS as the operator of Steps 1 and 2. A skill is the natural invocation shape for a POLYBIUS-run helper.

### §3.2 — A3 pick: skill name = `inspect-script-output`; worked-example domain = substrate-update flow (LOCKED)

**Pick:** `inspect-script-output`.

**Rationale (vs. the other three candidates):**

- `script-output-inspection` — verbose; reads as the name of an academic discipline rather than a skill that runs. Rejected on voice grounds.
- `post-script-inspection` — clear about temporal trigger but ambiguous about target. "Post-script" is more abstract than "script-output"; the latter names the artifact the skill reads. Rejected on specificity grounds.
- `inspection-agent` — names the **pattern** rather than the **action**. The skill IS one instance of the inspection-agent pattern; naming the skill after the pattern would conflate the two and make future skills awkward to name (e.g., the deploy-inspection skill at some future arc would also be an "inspection-agent" and the namespace would collide). Rejected on naming-discipline grounds.
- `inspect-script-output` — verb-first; names the action; reads cleanly in a POLYBIUS invocation (*"POLYBIUS, run `inspect-script-output` against the post-apply state"*); leaves namespace room for future inspection skills with similar verb-first shapes (`inspect-deploy-output`, `inspect-build-artifacts` etc., if/when those land).

**Worked-example domain (LOCKED per A3):** substrate-update flow. The skill ships with a check script that inspects post-`apply.sh` / post-`install.sh` state. Per directive A3 paragraph 4 + the strangeness-categories enumeration:

- **Unauthorized commits** (e.g., probe-residue from prior gauntlets — sector-4 probe-mutation case from Arc 26 / `stoa--501` is the canonical worked example);
- **File states inconsistent with intent** (custom files at base paths violating §23.2 / §17.2 base-paths-only scoping; base files modified locally where the apply operation should have left them clean);
- **Drift verdict mismatching detailed state** (CURRENT verdict but unexpected file mtimes; DRIFTED verdict with no detail lines; etc.);
- **Cleanup claims not executed** (post-signoff verification candidate per §5.10 — NOT shipped this arc, named in futures list);
- **Attestation claims not live-verified** (post-attestation verification candidate per §19.6 — NOT shipped this arc, named in futures list);
- **PRINCIPAL-gate clauses encountered but not paused-on** (post-execution audit candidate per §25 — NOT shipped this arc, named in futures list).

**Critical distinction (load-bearing for A7 boundary):** the skill SHIPS WITH probes for the first three categories (the categories the inspection-skill mechanically CAN check in this arc's scope). The last three categories are named in the SKILL.md "Strangeness categories" table with the explicit note *"future-arc work — this arc establishes the skill component; per-discipline mechanical enforcement is incremental across future arcs per directive A7."* The probe surface for the first three categories is what makes the skill empirically demonstrate the inspection-agent pattern; the last three are documented so future arcs reading the skill know the integration roadmap.

### §3.3 — A4 pick: new top-level §27 in operating-disciplines.md after §26

**Pick:** new top-level section `## 27. Mechanical-script / agent-inspection split` inserted after §26 (Activation-paste cron hygiene; ends at line 1281 with the `---` separator) and before the `## Agent-regime inverses` section (line 1284).

**Rationale (vs. folding under §11 autonomous-mode-setup):**

- **§11 is cadence-axis canon; §27 is architecture-axis canon.** §25.2 explicitly distinguishes the two axes — *"§10 + §11 govern WHEN to surface during routine work (cadence axis); §25 governs WHETHER PRINCIPAL input is structurally required for a step (authorization axis)."* The inspection-agent split is neither cadence nor gate — it is a *structural architecture* discipline (where intelligence lives across the mechanical / recognition / triage layers). Folding it under §11 would inherit cadence-relaxation framing the discipline does not want; the same conflation §25 was created to prevent.
- **Top-level locus parallel to §23 / §25 / §26.** Each PRINCIPAL-declared 2026-05-16 / 2026-05-17 discipline has its own top-level home: §23 base-vs-custom (universal-team), §25 PRINCIPAL-gate, §26 activation-paste cron hygiene (thin cross-ref). §27 mechanical-script / agent-inspection split follows the same shape. The pattern is "PRINCIPAL declared 2026-05-1X; substrate accretes a top-level canon section; cross-refs to related disciplines; §6.7.1 N=1 promotion path."
- **§27 cross-refs to §11 (and §10) anyway.** The new section cross-references §10 + §11 (cadence axis) per §25's pattern of explicitly disambiguating against adjacent disciplines. Readers landing at §11 who hit a cross-ref pointer to §27 find the architecture canon one line away; the inverse reader (landing at §27) finds the cadence canon at §10/§11 via §27's cross-ref block.
- **Numbering room.** §26 ends at line 1281; the trailing `## Agent-regime inverses` (line 1284) is a non-numbered closing section. Inserting §27 between §26 and the closing section keeps numbering monotonic and does not require renumbering downstream sections (there are none).

---

## §4 — The new skill: `inspect-script-output`

### §4.1 — File set ADA will build

```
substrate/skills/inspect-script-output/
  SKILL.md                            # ~180-220 lines (see §4.2 outline)
  check.sh                            # ~200-260 lines (see §4.3 outline)
  fixtures/
    README.md                         # ~30-40 lines; describes the fixture mechanism
    synthetic-apply-clean/            # one fixture directory (clean post-apply state)
      .claude/
        MAJOR_POLYBIUS_synthetic.md   # representative base file (placeholder content; substrate-recognizable header)
        operating-disciplines.md      # representative base file (placeholder content)
        agents/
          CAPTAIN_DAEDALUS_synthetic.md   # representative base CAPTAIN
        skills/
          check-substrate-updates/
            SKILL.md                  # representative deployed skill
      .git-HEAD-fixture               # one-line file: simulated HEAD SHA (no real .git/)
    synthetic-apply-strange/          # one fixture directory (strange post-apply state)
      .claude/
        MAJOR_POLYBIUS_synthetic.md   # planted: file is at base path BUT begins with "name: CUSTOM_AGENT" custom-marker
        operating-disciplines.md      # representative base file (clean)
        agents/
          CAPTAIN_DAEDALUS_synthetic.md
          custom/
            CAPTAIN_DAEDALUS_synthetic.md   # planted: filename collision with base (silent-collision case per §17.4)
        skills/
          check-substrate-updates/
            SKILL.md
      .git-HEAD-fixture
      .planted-strangeness.md         # one-line documentation of what was planted for the probe to find
```

**Why no real `.git/` in fixtures:** the skill's mechanical check is filesystem-state inspection, not git operations. The `.git-HEAD-fixture` is a one-line text file the skill reads via env-var override (see §4.3) when invoked against a fixture; production invocations read real `git rev-parse HEAD`. Fixture mode is signalled by `INSPECT_SCRIPT_OUTPUT_FIXTURE_MODE=1`. This mirrors the env-var fixture mechanism check-bw-release uses (`BW_RELEASE_CHECK_LATEST_OVERRIDE` / `BW_RELEASE_CHECK_BASELINE_OVERRIDE`); per directive A3 prose, copy the env-var fixture mechanism explicitly.

**Why two fixtures (clean + strange):** the clean fixture exercises the "no strangeness detected; output is one-line CLEAN message" code path. The strange fixture exercises the "strangeness detected; output enumerates planted items with sufficient detail for POLYBIUS triage" code path. Both paths are smoke-tested per §7.4.

### §4.2 — SKILL.md outline (frontmatter + sections)

**Frontmatter (verbatim — per A6 authorship immutability + Arc 27 stoa--uly convention copied from check-bw-release):**

```yaml
---
name: inspect-script-output
description: Inspect post-mechanical-script workspace state for strangeness — anomalies the script wasn't pre-programmed to surface. Reads the workspace's deployed-file tree, git HEAD, and any optional script-output artifact, and emits a structured strangeness report POLYBIUS triages per operating-disciplines.md §27. Per A7 boundary, this skill establishes the 3-step pattern component; per-discipline mechanical enforcement (§25 PRINCIPAL-gate / §19.6 attestation / §5.10 signoff / §17 base-vs-custom) is incremental future-arc work. Triggers on requests like "inspect substrate state after apply", "check post-install workspace strangeness", "run inspection agent on substrate update", "post-script state inspection".
author: Denson Smith
---
```

**Section outline** (ADA writes verbatim per ARGUS pass; lengths approximate):

1. `# inspect-script-output — the inspection-agent layer of the 3-step substrate-update pattern` (header)
2. `## Why this skill exists` — the script-bloat empirical anchor (Arc 26 / 489 → 934 lines; PRINCIPAL's 2026-05-16 declaration verbatim); the 3-step pattern (1. mechanical script → 2. inspection agent → 3. POLYBIUS triage); cross-ref to `operating-disciplines.md` §27 as the canonical home. ~25 lines.
3. `## When to use this skill` — invocation triggers (after `apply.sh` or `install.sh` runs against a registered workspace; before posting a §5.10 signoff that names a workspace cleanup claim); explicit "do not invoke" boundary (not a substitute for `check.sh`; not a mechanical PRINCIPAL-gate enforcer in this arc per A7). ~20 lines.
4. `## What the skill ships` — file list (SKILL.md + check.sh + fixtures/); per-workspace state file location convention copied from check-bw-release §"State-file location" pattern (skills-parent directory; substrate-tier vs consumer-tier resolution); no `.gitignore` line needed (runtime-filtered same mechanism as check-bw-release). ~25 lines.
5. `## How to invoke` — three worked invocations: standard call (`<skill-dir>/check.sh --workspace <abs-path>`), fixture-mode (`INSPECT_SCRIPT_OUTPUT_FIXTURE_MODE=1 <skill-dir>/check.sh --workspace <skill-dir>/fixtures/synthetic-apply-clean`), explicit-categories (`<skill-dir>/check.sh --workspace <abs-path> --only base-vs-custom`). ~30 lines.
6. `## Strangeness categories` — table with two columns: category name + shipped-this-arc | future-arc. Shipped: unauthorized-commits (git-history scan vs. recent apply baseline), file-state-vs-intent (base-path-with-custom-marker scan per §17 / §23), drift-verdict-mismatch (cross-check check.sh output if available against detailed file mtimes). Future-arc (explicit "NOT shipped this arc per A7"): cleanup-claims-not-executed (§5.10 partner), attestation-claims-not-verified (§19.6 partner), PRINCIPAL-gate-clauses-encountered-but-not-paused (§25 partner). ~40 lines.
7. `## How to test` — three worked test invocations against the fixture mechanism: at-clean (CLEAN output), at-strange (strangeness report with at least the planted custom-collision item surfaced), at-real-workspace (production invocation with no overrides). Test-fixture env-var documented inline. ~30 lines.
8. `## State-file shape` — one-line per-workspace baseline at `<skills-parent>/.inspect-script-output-last-run` recording the last-inspected HEAD SHA + ISO-8601 timestamp. Used to scope unauthorized-commits scan to commits-since-last-run. ~15 lines.
9. `## Per-workspace deployment` — pattern copied verbatim-shape from check-bw-release §"Per-workspace deployment". ~15 lines.
10. `## POLYBIUS triage protocol` — how POLYBIUS routes the strangeness report per §27 step 3: routine technical-tier findings → POLYBIUS fixes inline (per fix-now §4.8 + user-tier-approves-tech-decisions); PRINCIPAL-gate findings → workflow PAUSES per §25.3 BLOCK-not-TAG. Cross-ref to `operating-disciplines.md` §27 (the canonical pattern home) + §25 (gate discipline that governs triage step) + `MAJOR_POLYBIUS.md` §4.8 (fix-now). ~25 lines.
11. `## What this skill is NOT` — explicit non-scopes: not an auto-fixer (POLYBIUS triage is human-judgment-grade); not a substitute for `check.sh` (it inspects POST-mechanical state; `check.sh` detects drift); not a CAPTAIN-pipeline component (it is POLYBIUS-invoked; cross-ref §3.1 deferral rationale). ~20 lines.
12. `## Related` — `operating-disciplines.md` §27 (the canonical pattern home); §25 (gate discipline); §23 + `MAJOR_POLYBIUS.md` §17 (base-vs-custom scoping the skill respects); §19.6 + `MAJOR_PLINY.md` §5.10 (futures); `substrate/skills/check-bw-release/` (sibling structural model); `substrate/skills/check-substrate-updates/` (the script-bloat empirical anchor — referenced, NOT modified per A7); `stoa--32b.2` (this arc); `docs/sessions/2026-05-16-substrate-update-architecture-reframe--retro.md` §8 (load-bearing source). ~15 lines.

**Estimated total:** 180-220 lines. Comparable to check-bw-release (122 lines, smaller-scope skill) and check-substrate-updates (202 lines, more complex skill).

### §4.3 — check.sh outline (executable scaffold)

```bash
#!/usr/bin/env bash
# check.sh — inspect post-mechanical-script workspace state for strangeness.
# [Header copies the structural shape of check-bw-release/check.sh:1-29 inline help text]
set -euo pipefail

# Locate skills-parent dir for state-file (same mechanism as check-bw-release lines 33-47)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_PARENT_DIR="$(cd "${SCRIPT_DIR}/../.." && pwd)"
STATE_FILE="${SKILLS_PARENT_DIR}/.inspect-script-output-last-run"

# Argument parsing — --workspace <abs-path> required; --only <category-list>
# optional; --since <SHA> optional; -h | --help. See check-bw-release lines
# 49-74 for the argparse shape.

# Helpers:
#
# read_git_head <workspace>: echo the workspace's HEAD SHA.
#   - Fixture mode (INSPECT_SCRIPT_OUTPUT_FIXTURE_MODE=1): read from
#     <workspace>/.git-HEAD-fixture (one-line text file).
#   - Production: cd <workspace> && git rev-parse HEAD.
#   - Defang per check-bw-release lines 113-127 model: { ...; } || true at
#     pipeline boundary so set -euo pipefail does not propagate.
#
# scan_unauthorized_commits <workspace> <baseline-sha>: enumerate commits in
# <workspace>'s .claude/ between <baseline-sha> and HEAD; surface any commit
# message NOT matching a substrate-canonical pattern (apply-from-substrate,
# install-from-substrate, prune-from-substrate). This is the "sector-4 probe
# residue" case from Arc 26 / stoa--501 canonical worked example.
#   - Fixture mode: no-op (fixtures have no real .git/).
#
# scan_base_path_custom_markers <workspace>: walk .claude/ subtree; per file
# at a base path (per §23.2 + §17.2), check the first 5 lines for known
# custom-frontmatter markers (e.g., 'name: CUSTOM_' or 'name: <CAPTAIN>_<slug>'
# patterns that would collide with base per §17.4 silent-collision footgun).
# This is the planted-strange-fixture worked example.
#
# scan_drift_verdict_mismatch <workspace>: if check-substrate-updates is
# deployed AND a recent check.sh output is cached, compare its verdict
# against an mtime sweep of .claude/ — surface any inconsistency. Skips
# silently if check-substrate-updates is not deployed at the workspace.
#
# emit_report <findings>: write the strangeness report to stdout; CLEAN if
# findings empty; STRANGENESS DETECTED with per-category sections if not.

# Main dispatch:
#   1. Argument validation
#   2. Determine workspace path (resolve, exists, has .claude/)
#   3. Read baseline from state file (or initialize silently on first run)
#   4. Run selected scan helpers (all categories, or per --only)
#   5. emit_report
#   6. Update state file with current HEAD + timestamp
#   7. exit 0 (drift is informational; never blocks — same exit-code
#      discipline as check-bw-release and check-substrate-updates)
```

**Estimated length:** 200-260 lines including the inline help text (sed-extracted via `--help` per check-bw-release lines 66-67 pattern), the four scan helpers (~30-50 lines each), the argument parser (~30 lines), the report emitter (~30 lines).

### §4.4 — Scope discipline the skill respects

The skill INSPECTS base-path state only. Workspace files at custom paths (per §23.2 / §17.3 custom paths: `.claude/agents/custom/`, `.claude/skills/custom-*/`, `.claude/templates/custom/`) are EXCLUDED from all four scan helpers. Cite-comment at the scan-helpers top references §23 (universal-team) + `MAJOR_POLYBIUS.md` §17 (POLYBIUS-tier refinement). The cite mirrors the cite-comment discipline at `substrate/skills/check-substrate-updates/check.sh` apply_substitutions and parse_skill_names_from_install (per Arc 26).

**Rationale:** if the skill scanned custom paths, it would surface "strangeness" for every workspace customization (per §23.3 "custom authoring is the workspace's responsibility"). That noise would defeat the inspection-agent purpose. The skill is a BASE-state inspector; custom-state inspection is operator-and-workspace-team owned.

### §4.5 — Explicit A7 boundary inside SKILL.md

The "Strangeness categories" section (§4.2 item 6 above) carries an explicit note:

> **A7 boundary (per `substrate/arcs/arc-33-build-directive.md`):** this skill establishes the inspection-agent COMPONENT and the 3-step pattern's worked example. Per-discipline mechanical enforcement (§25 PRINCIPAL-gate / §19.6 attestation-confabulation / §5.10 signoff-accuracy / §17 base-vs-custom / etc.) is INCREMENTAL future-arc work. The skill's shipped scan helpers cover the first three categories above; the last three are deliberately deferred — a future arc dispatches the relevant integration per use case.

This makes the boundary legible at the skill itself, not just in the directive — future readers of the skill land on the limit without having to chase upward.

---

## §5 — Authorship audit (per A6 + substrate/CLAUDE.md)

New files added by this arc, with their author-like fields:

| File | Author-like field | Value |
|---|---|---|
| `substrate/skills/inspect-script-output/SKILL.md` | YAML frontmatter `author:` | `Denson Smith` |
| `substrate/skills/inspect-script-output/check.sh` | None (shebang scripts do not carry author frontmatter; PLINY commit Author: governs git-side attribution) | n/a |
| `substrate/skills/inspect-script-output/fixtures/README.md` | None (skill-internal docs convention; no frontmatter) | n/a |
| `substrate/skills/inspect-script-output/fixtures/*` | None (synthetic fixture content; placeholder substrate-shape files) | n/a |
| `substrate/operating-disciplines.md` new §27 | None (file-level authorship is the substrate's; no per-section author field exists in op-disc.md today) | n/a |
| `substrate/install.sh` SKILL_NAMES append | None (config file; PLINY commit Author: governs) | n/a |

**Verification probe in §7:** explicit grep against the new SKILL.md frontmatter for `author: Denson Smith` (probe §7.5). If any field surfaces a different name, ADA STOPS per substrate/CLAUDE.md "stop and ask" discipline; the probe is the gate that prevents silent regression.

---

## §6 — operating-disciplines.md new §27 (prose ADA pastes)

### §6.1 — Insertion locus + structural shape

**Insert between line 1281 (existing `---` closing §26) and line 1283 (existing `---` opening `## Agent-regime inverses`).** New text: a `---` separator + `## 27. Mechanical-script / agent-inspection split` heading + ~140-180 lines of canon prose + a final `---` separator before the existing `## Agent-regime inverses` section.

The new section follows the standard PRINCIPAL-declared-discipline shape (§23 / §25 / §26 / Arc 32's §5.10): one-paragraph framing → numbered sub-sections (§27.1 discipline, §27.2 the 3-step pattern, §27.3 when-to-apply + boundary, §27.4 per-seat behavior, §27.5 worked example pointer, §27.6 N=1 provenance + accretion path, §27.7 cross-references).

### §6.2 — Prose outline (ADA writes verbatim; word-counts approximate; ARGUS audits the wording)

**Opening paragraph (~5 lines).** Names the split: mechanical scripts stay narrow; recognition-of-strangeness moves to an LLM-grade inspection-agent run after the mechanical operation; POLYBIUS triages findings against §25 gate discipline. Distinct from §11 (autonomous-mode-setup cadence axis) and §25 (PRINCIPAL-gate authorization axis) — this section is an *architecture axis* discipline (where intelligence lives across mechanical / recognition / triage layers).

**§27.1 The discipline (PRINCIPAL declaration) (~15 lines).** PRINCIPAL declared 2026-05-16 after Arc 26 ship + `stoa--501` revert sequence. The declaration verbatim (from `bw show stoa--32b.2` body):

> *"We are spending way too much time trying to get script workflows perfect when the answer is to run the script, then run an agent with a script to check what happened including anything strange and then let polybius fix any of the strangeness with human approval if necessary."*

This is project-direction authority per §6.7.1 honest-scope framing (see §27.6 for the N=1 accretion path). The load-bearing source for the architectural framing is `docs/sessions/2026-05-16-substrate-update-architecture-reframe--retro.md` §8 (PRINCIPAL's prose on where intelligence lives) and §9 (synthesis with §7's gate discipline now shipped as §25).

**§27.2 The 3-step pattern (~25 lines).** A numbered list with one-line per step + one-line per step on which seat owns it:

1. **Mechanical script** runs (`apply.sh` / `install.sh` / deploy workflows / etc.) — deterministic, narrow. Stays small over time; does NOT grow recognition logic. Owner: the workspace's `.claude/skills/` deployed scripts; or `substrate/install.sh` at substrate-tier.
2. **Inspection agent** runs a verification script + reads result + workspace state + surfaces anything strange — including things the script wasn't pre-programmed to enumerate. LLM-grade recognition, not pattern-match. Owner: POLYBIUS-invoked skill (worked example: `substrate/skills/inspect-script-output/`); SHOULD respect base-vs-custom scoping per §23 / `MAJOR_POLYBIUS.md` §17.
3. **POLYBIUS triage** — routes findings:
   - **Routine technical-tier findings** → POLYBIUS fixes inline per fix-now `MAJOR_POLYBIUS.md` §4.8 + user-tier-approves-tech-decisions discipline.
   - **PRINCIPAL-gate findings** → workflow PAUSES per §25.3 BLOCK-not-TAG; autonomous mode does NOT relax. Owner: POLYBIUS; PRINCIPAL is exception-handler.

Distinguishing property vs. intelligence-in-script: the script enumerates KNOWN strangeness; the inspection agent finds NOVEL strangeness (the things the script wasn't pre-programmed to notice).

**§27.3 When to apply + A7 boundary (~20 lines).** When to apply: substrate-update flow (post-`apply.sh` / post-`install.sh`); deploy workflows (when one lands at this team in the future); future script-based workflows where the recognition surface is unbounded or grows. Discipline framing (verbatim per directive A4 prose): *"when designing a script-based workflow, prefer mechanical-narrow + inspection-agent over make-script-comprehensive."*

**A7 boundary (load-bearing — names what this arc DOES NOT do):**

- This arc establishes the COMPONENT (the skill at `substrate/skills/inspect-script-output/`) + the worked-example deployment (substrate-update flow) + this canon section.
- This arc does NOT mechanically enforce §25 / §19.6 / §5.10 / §17 — per-discipline integration is INCREMENTAL future-arc work where each discipline's specific check is integrated against the inspection-agent layer per use case.
- This arc does NOT unwind Arc 26's `check.sh` additions. `check.sh` stays as-is; the inspection-agent pattern is the *forward* shape. Future migration of `check.sh` intelligence into the inspection-agent layer is a separate arc when the pattern proves out.
- This arc does NOT build inspection-agents for every existing script. Worked example is ONE; concrete adoption is incremental.
- This arc does NOT promote the skill to a CAPTAIN seat (CAPTAIN_INSPECTOR) — that is Option γ deferred per directive A2 to a future arc when the skill pattern proves out and warrants gauntlet-pipeline integration.

**§27.4 Per-seat behavior summary (~12 lines + table).** Three-column table: Seat | Role in the 3-step pattern | Cross-ref.

| Seat | Role | Cross-ref |
|---|---|---|
| Mechanical-script author (DAEDALUS designing; ADA building) | Design scripts to STAY mechanical-narrow. When a new recognition surface is needed, design the inspection-agent layer, not a script extension. | `CAPTAIN_DAEDALUS.md` §6 (one-job-per-agent), `CAPTAIN_ADA.md` (build envelope) |
| Inspection-agent (skill or CAPTAIN) | Read post-mechanical state; surface strangeness; respect §23/§17 scoping. | `substrate/skills/inspect-script-output/SKILL.md` (worked example) |
| POLYBIUS (triage) | Route routine findings to fix-now; route PRINCIPAL-gate findings to PAUSE per §25.3. | `MAJOR_POLYBIUS.md` §4.8 (fix-now), `operating-disciplines.md` §25 (gate discipline) |
| PRINCIPAL | Disposition on gated findings per §25.3; project-direction calls on architectural promotions. | `operating-disciplines.md` §25 |

**§27.5 Worked example pointer (~10 lines).** This arc ships `substrate/skills/inspect-script-output/` as the substrate-update-flow worked example. The skill ships with two fixtures (synthetic-apply-clean + synthetic-apply-strange); the planted-strangeness fixture exercises §17.4 silent-collision detection as the canonical worked example (drawing from Arc 26 / `stoa--501` sector-4 probe-residue case). See SKILL.md "How to test" section for the test invocations.

**§27.6 N=1 provenance + accretion path (~25 lines per §A8 + Arc 27/28/29/30/31/32 N=1 framing model).** Per §6.7.1 honest-scope: PRINCIPAL declared this discipline 2026-05-16 (project-direction authority, captured at `docs/sessions/2026-05-16-substrate-update-architecture-reframe--retro.md` §8 and at `bw show stoa--32b.2` ticket body). §6.7.1 defers to the canon-promotion gate (multiple observations + controlled comparison + substrate-level pattern); §6.7.1 does not carve out a separate "PRINCIPAL-declaration shortcut." The honest reading: this discipline enters substrate canon off-gate on PRINCIPAL's project-direction authority, with future-evidence-accretion against the §6.7.1 gate still required for promotion to "structural lesson" status.

Supporting evidence at the time of this writing (per scope-refresh comment 2026-05-17):

- **N=2 bit-by-it of make-script-comprehensive (negative anchor):** Arc 26 (`stoa--dxw`) extended `check.sh` from 489 → 893 lines to add MISSING + OBSOLETE + uncommitted-state detection; Arc 28 (`stoa--s6n`) added further check.sh logic for the bw-upgrade discipline. Each arc added more script logic to handle more edge cases. Two observations of the same pattern at the same script.
- **N=1 small-scope inspection-shape precedent (positive anchor):** `substrate/skills/check-bw-release/` (Arc 28) ships a small inspection-shape skill that's working without script-bloat. Single instance today; this arc's worked example accretes the second instance.
- **N=multi cross-discipline coverage:** §25 + §19.6 + §5.10 + §17 + §5.9.4 all benefit from mechanical-script-then-agent-inspection enforcement at future arcs. Today none are mechanically enforced (per A7); the pattern's future-arc adoption is the accretion path against §6.7.1.

The discipline is in NOW because PRINCIPAL named it; structural-lesson confidence accretes over future arcs that apply the pattern at new domains (deploy workflows, build verification, etc.) AND across the per-discipline mechanical-enforcement integrations the A7 boundary defers. Do NOT over-generalize beyond what PRINCIPAL named — the pattern is *prefer mechanical-narrow + inspection-agent over make-script-comprehensive WHEN designing script-based workflows*, not *all scripts must have inspection-agents now*. Same N=1 framing as Arc 27's `MAJOR_POLYBIUS.md` §16.6, Arc 28's `operating-disciplines.md` §22.3, Arc 29's §17.5, Arc 30's `MAJOR_PLINY.md` §5.9.3, Arc 31's `operating-disciplines.md` §25.6, and Arc 32's §19.6 / §5.10 / §5.9.4.

**§27.7 Cross-references (~15 lines).**

- §10 (operating engagement — cadence axis) + §11 (autonomous-mode-setup checklist) — the cadence-discipline canon this section is *distinct from* (architecture axis, not cadence axis). Same disambiguation shape §25 uses.
- §25 (PRINCIPAL-gate discipline) — the triage-step partner; Step 3 of the 3-step pattern hands gated findings to PRINCIPAL per §25.3 BLOCK-not-TAG. Folding §25 into §27 would conflate gate-axis with architecture-axis disciplines; the two cross-reference each other and stand as separate loci.
- §19.6 (attestation-confabulation) — future-integration partner; the inspection-agent layer is the WHERE that COULD verify attestation claims at attestation time. NOT shipped this arc per A7.
- §23 (base-vs-custom universal) + `MAJOR_POLYBIUS.md` §17 (POLYBIUS refinement) — the scoping discipline the inspection-agent layer MUST respect; the skill at `substrate/skills/inspect-script-output/` scans base paths only.
- §6.7.1 (the N=1 canon-promotion gate this section enters off-gate on PRINCIPAL's 2026-05-16 declaration).
- `MAJOR_PLINY.md` §5.10 (signoff-accuracy) — future-integration partner; the inspection-agent layer COULD verify cleanup claims pre-signoff. NOT shipped this arc per A7.
- `MAJOR_POLYBIUS.md` §4.8 (fix-now) — the routine-finding routing rule for Step 3 of the 3-step pattern.
- `substrate/skills/inspect-script-output/` — this arc's worked-example deployment.
- `substrate/skills/check-bw-release/` (Arc 28) — small-scope precedent for inspection-shape skills.
- `substrate/skills/check-substrate-updates/` (Arc 26 + 29) — the script-bloat empirical anchor referenced but NOT modified per A7.
- `stoa--32b.2` (this arc's work-unit ticket); `stoa--32b.1` (sibling Arc 31 / §25); `stoa--dxw` (Arc 26 empirical anchor); `stoa--501` (post-hoc cleanup); `stoa--s6n` (Arc 28 / check-bw-release precedent).
- `docs/sessions/2026-05-16-substrate-update-architecture-reframe--retro.md` §8 + §9 (load-bearing source).

---

## §7 — Verification probes (VERA / CATO / ZENO ownership)

Per directive Phase B (lines 169-186) + Phase C (lines 190-198). Each probe names a category, the seat that owns it, the concrete command/check, and the expected output. Quadrant classifications per `operating-disciplines.md` §15 inline.

### §7.1 — VERA probes (verifier-of-arc-deliverables)

**Probe VERA-1 — substrate component present (easy-easy).** Verify the skill directory and required files exist.
- `ls substrate/skills/inspect-script-output/` → directory exists; lists `SKILL.md`, `check.sh`, `fixtures/`.
- `ls substrate/skills/inspect-script-output/fixtures/` → lists `README.md`, `synthetic-apply-clean/`, `synthetic-apply-strange/`.
- `test -x substrate/skills/inspect-script-output/check.sh` → executable bit set.
- Expected: all three checks PASS.

**Probe VERA-2 — install.sh SKILL_NAMES append (easy-easy).** Verify the deploy register updated.
- `grep -n 'inspect-script-output' substrate/install.sh` → matches line at SKILL_NAMES append point (after line 145 `check-bw-release`).
- `awk '/^SKILL_NAMES=\(/,/^\)/' substrate/install.sh | grep -c 'inspect-script-output'` → returns `1`.
- Expected: PASS.

**Probe VERA-3 — operating-disciplines.md §27 present + structure intact (easy-easy).** Verify the canon section landed.
- `grep -n '^## 27\. Mechanical-script / agent-inspection split' substrate/operating-disciplines.md` → matches exactly once.
- `grep -n '^### 27\.[1-7]' substrate/operating-disciplines.md` → returns 7 lines (§27.1 through §27.7).
- `grep -c 'inspection-agent\|inspection agent\|mechanical-script' substrate/operating-disciplines.md` → ≥ 12 (the new §27 prose contains many references; bound is loose to allow ARGUS / CATO wording revisions without re-tuning).
- Expected: PASS.

**Probe VERA-4 — synthetic-inspection smoke beat (CLEAN path) (easy-easy).** Verify the skill runs against the clean fixture and emits CLEAN.
```bash
INSPECT_SCRIPT_OUTPUT_FIXTURE_MODE=1 \
  substrate/skills/inspect-script-output/check.sh \
    --workspace substrate/skills/inspect-script-output/fixtures/synthetic-apply-clean
```
- Expected stdout: line containing `CLEAN — no strangeness detected` (exact phrasing per ADA's SKILL.md authoring; probe accepts the canonical CLEAN-message prefix).
- Expected exit code: 0.

**Probe VERA-5 — synthetic-inspection smoke beat (STRANGE path) (easy-easy).** Verify the skill runs against the strange fixture and surfaces at least the planted custom-collision item.
```bash
INSPECT_SCRIPT_OUTPUT_FIXTURE_MODE=1 \
  substrate/skills/inspect-script-output/check.sh \
    --workspace substrate/skills/inspect-script-output/fixtures/synthetic-apply-strange
```
- Expected stdout: block beginning `STRANGENESS DETECTED` (per emit_report contract); the block contains at least one finding referencing the planted file `.claude/agents/custom/CAPTAIN_DAEDALUS_synthetic.md` with a `name:` collision flag against the base `.claude/agents/CAPTAIN_DAEDALUS_synthetic.md`.
- Expected exit code: 0 (drift is informational per §4.3 + check-bw-release exit-code discipline).

**Probe VERA-6 — base-vs-custom scoping respected (hard-easy).** Verify the skill EXCLUDES custom paths from its scans (the scoping discipline per §4.4).
- Inspect `check.sh` source for cite-comment at the scan helpers referencing `operating-disciplines.md` §23 / `MAJOR_POLYBIUS.md` §17.
- Inspect `check.sh` source for the path-filter logic that skips `.claude/skills/custom-*`, `.claude/agents/custom/`, `.claude/templates/custom/`.
- Behavioral cross-check: add a synthetic `.claude/skills/custom-test/` to the clean fixture (one-line SKILL.md), re-run probe VERA-4; expected output still CLEAN (the custom path is excluded from scan).
- Expected: all three checks PASS.

**Probe VERA-7 — cross-refs resolve (easy-easy).** Verify every cross-ref the new SKILL.md + new §27 names points at a section/file that actually exists.
- Extract all `operating-disciplines.md §N.M` mentions from the new SKILL.md; for each, `grep -n "^### N\.M\b\|^## N\.\b"` in op-disc.md → match.
- Extract all `MAJOR_POLYBIUS.md §N` and `MAJOR_PLINY.md §N` mentions from new §27 + SKILL.md; for each, grep the corresponding file → match.
- Extract all `stoa--XXX` ticket IDs from new §27 + SKILL.md; for each, `bw show <id> 2>&1` → does not error.
- Expected: all matches PASS; no broken cross-refs.

**Probe VERA-8 — check.sh against the-stoa workspace (regression sanity).** Verify the existing check-substrate-updates skill correctly reports the-stoa workspace as DRIFTED on the substrate files this arc edits (sanity that the substrate edits actually landed; sanity that the deploy mechanism is consistent).
- `substrate/skills/check-substrate-updates/check.sh --workspace /c/Users/denso/claude_projects/the-stoa`
- Expected: DRIFTED or DRIFTED + MISSING for `.claude/operating-disciplines.md` (new §27 added) + `.claude/install.sh` (SKILL_NAMES append) + MISSING for `.claude/skills/inspect-script-output/` (new skill).

### §7.2 — CATO probes (cold-read for wording drift, scope creep, attribution)

**CATO-1 — Authorship audit.** Per directive A6 + Phase B item 7. Verify `grep -A 1 '^author:' substrate/skills/inspect-script-output/SKILL.md` returns exactly `author: Denson Smith`; no other author-like field surfaces a different name anywhere in the arc's diff. CATO sweeps the diff with `git diff main...arc-33/build | grep -i -E 'author|owner|creator|maintainer|by:|copyright'` → every match should be either the new SKILL.md frontmatter (Denson Smith) or pre-existing prose-text mentions (not author-like fields).

**CATO-2 — Wording-drift across the new SKILL.md + new §27 + ticket body.** Per Phase B Cato cold-read item. Verify the 3-step pattern language matches between (a) ticket body, (b) retro §8, (c) new §27, (d) new SKILL.md. The three-step phrasing should be consistent — "mechanical script → inspection agent → POLYBIUS triage" or substantively equivalent. Drift between the four loci is a CATO finding.

**CATO-3 — A7 scope-creep audit.** Per directive A7 hard-locks. CATO cold-reads the diff for any of: edits to `check-substrate-updates/check.sh` (any line); edits to `check-bw-release/check.sh` (any line); new CAPTAIN_*.md file; new sibling-ticket edits; any mechanical enforcement of §25 / §19.6 / §5.10 / §17 in the new check.sh (verify by absence: the scan helpers cover unauthorized-commits / base-path-custom-markers / drift-verdict-mismatch ONLY, per §4.2 item 6 shipped-this-arc subset). Any A7 violation is a CATO P0 finding.

**CATO-4 — §15 N=1 honesty audit.** Per directive A8. CATO cold-reads the new §27.6 + new SKILL.md "Why this skill exists" for over-generalization. The substrate canon must say "PRINCIPAL declared 2026-05-16; this enters off-gate on project-direction authority; future-evidence-accretion against §6.7.1 still required" — NOT "the inspection-agent pattern IS the substrate-canonical approach" or any structural-claim overreach. CATO flags any sentence reading as universal-claim where the framing should be N=1-with-accretion-path.

**CATO-5 — 3-step pattern clarity.** Per Phase B CATO cold-reads item. Verify future POLYBIUSes reading the new §27 can identify (a) which step they are at, (b) which seat owns each step, (c) how to invoke step 2 (pointer to skill), (d) how step 3 routes per §25. Cold-read with no prior context; if any of the four is ambiguous, CATO finding.

**CATO-6 — Inspection-skill domain scope clarity.** Per Phase B CATO cold-reads item. Verify the new SKILL.md "When to use this skill" and "What this skill is NOT" sections make it clear what is in-scope (mechanical-script output inspection) vs. out-of-scope (CAPTAIN-driven verification — that's still VERA/CATO/etc.'s pipeline-time work). If a reader could confuse the inspection-agent layer with the gauntlet's verifier seats, CATO finding.

### §7.3 — ZENO probes (deliverable spec-check)

**ZENO-1 — D1 (substrate component) DONE.** Per ticket body deliverable 1 + directive A2. Cite: `substrate/skills/inspect-script-output/` exists with SKILL.md + check.sh + fixtures/.

**ZENO-2 — D2 (worked-example deployment) DONE.** Per ticket body deliverable 2 + directive A3 LOCKED. Cite: SKILL.md "Strangeness categories" section names the substrate-update-flow worked example explicitly; check.sh implements the scan for the shipped-this-arc strangeness categories; fixtures/synthetic-apply-* provide the planted-strangeness probe surface.

**ZENO-3 — D3 (operating-disciplines.md addition) DONE.** Per ticket body deliverable 3 + directive A4. Cite: `operating-disciplines.md` §27 added; 3-step pattern + when-to-apply + cross-refs all present per §6.2 outline above.

**ZENO-4 — D4 (Arc 26 forward-migration plan) deliberately PARTIAL per A7.** Ticket body deliverable 4 names "possibly: revisit Arc 26's check.sh additions" with the explicit "NOT a regression of Arc 26 ... a forward-migration plan if the inspection-agent pattern proves out." A7 hard-locks "no unwinding Arc 26." The new §27.3 A7-boundary clause names this deferral explicitly. ZENO confirms PARTIAL with the deferral cited; this is honest scoping per directive A7, not a deliverable gap.

### §7.4 — Phase C smoke beats (PLINY pre-PR)

Per directive Phase C lines 194-198. PLINY runs before opening PR:

- `grep -n "mechanical-script\|inspection-agent\|inspection agent" substrate/operating-disciplines.md` → matches in new §27.
- `ls substrate/skills/inspect-script-output/` → SKILL.md + check.sh + fixtures/.
- `grep -n "inspect-script-output" substrate/install.sh` → matches SKILL_NAMES append.
- **Synthetic-inspection smoke beat:** run VERA-4 (CLEAN fixture) + VERA-5 (STRANGE fixture); both PASS.
- `substrate/skills/check-substrate-updates/check.sh --workspace .` → expected DRIFTED + MISSING on substrate files this arc edits (sanity).

### §7.5 — Authorship probe summary

CATO-1 above is the load-bearing authorship gate. PLINY-side smoke probe: `grep -i -E 'author|owner|creator|maintainer' substrate/skills/inspect-script-output/SKILL.md` → expected exact match `author: Denson Smith` and nothing else. Any other author-like field surfacing is a PRE-PR blocker; PLINY does not open the PR until the gap is fixed.

---

## §8 — Self-assessed weak points (per CAPTAIN_DAEDALUS §6.2)

Auditing this design honestly for what ARGUS is likely to catch on cold-read.

- **Weak point 1: §4.3 check.sh scope is broader than the worked example strictly needs.** The four scan helpers (unauthorized-commits / base-path-custom-markers / drift-verdict-mismatch / [implicit] state-file management) bundle three scan domains into one skill. A tighter design would ship only ONE scan helper (the planted-custom-collision-detector via base-path-custom-markers) and defer the other two to follow-up arcs. The bundle is justified by "demonstrate the inspection-agent pattern's generality at worked-example scope" — but a critic could read it as over-promising what one arc delivers. **Why this shape anyway:** the directive A3 strangeness-categories enumeration names six categories explicitly; shipping a skill that only addresses one (custom-collision) would under-deliver against the worked-example domain LOCK. The compromise: ship three of six (the three with concrete mechanical-check shape today), defer the other three to A7-named future-arc work, document the boundary explicitly inside the skill (§4.5).

- **Weak point 2: The fixture mechanism has no real `.git/`.** The strangeness category "unauthorized commits" relies on git-history scan, but the fixtures use a `.git-HEAD-fixture` text file in place of a real `.git/` directory. The scan_unauthorized_commits helper is no-op in fixture mode; the smoke beats (VERA-4 / VERA-5) do not exercise that code path. A real-workspace VERA probe (against the-stoa or a registered consumer workspace) would exercise it, but no such probe is in §7.1's first six probes. **Why this shape anyway:** including a real `.git/` in the fixture directory tree creates a nested git repo problem (the substrate's own git tracks the fixture's git, or doesn't, ambiguously); the env-var fixture mechanism check-bw-release uses for upstream-API mock is the established precedent for "fixture as text file." A real-workspace probe is added as VERA-8 (regression sanity against the-stoa), which incidentally exercises the unauthorized-commits scan against the workspace's real history. The gap (no fixture-mode exercise of the unauthorized-commits scan) is acknowledged; the cost is that a defect in that helper's logic might not surface until VERA-8 fires against a workspace state that doesn't have any unauthorized commits to detect.

- **Weak point 3: §27 in operating-disciplines.md does not name the inspection-agent's failure modes.** The new canon section describes the pattern and the 3-step shape, but does not enumerate what could go wrong with the pattern itself (e.g., inspection-agent confabulates strangeness; inspection-agent misses strangeness; POLYBIUS triage routes wrong; etc.). PRINCIPAL-declared-discipline sections typically do not enumerate their own failure modes (§23, §25, §26 don't), so the omission is shape-consistent — but a critic could note that future arcs evaluating "did the pattern prove out" would benefit from explicit named failure-mode anchors. **Why this shape anyway:** A8 explicitly says "do NOT over-generalize beyond what PRINCIPAL named" — and PRINCIPAL named the pattern, not its failure modes. Adding speculative failure modes risks the §15 over-generalization the directive guards against. The honest framing is: the pattern's failure modes accrete empirically as future arcs apply the pattern; today's §27 names the pattern and the A7 boundary.

- **Weak point 4: A2 deferral rationale for Option β leans on a verbal distinction (verifier-of-arc-deliverables vs. verifier-of-mechanical-script-outputs) that ARGUS could push back on.** The two roles do share the verb "verify." A counter-argument: VERA's envelope already runs probes; extending VERA with a post-mechanical-inspection sub-discipline AT THE PROBE LEVEL (rather than the seat level) could be lighter than a new skill. **Why this shape anyway:** VERA's probes are scoped per-dispatch — VERA runs the probes the DAEDALUS design named, not a generic post-mechanical-script-checker. Folding generic post-mechanical inspection into VERA's envelope would require VERA to run probes outside any dispatch's scope; that breaks the one-job-per-agent contract VERA's envelope inherits from `operating-disciplines.md` §6.7. The skill-shape preserves the per-invocation contract (POLYBIUS invokes the skill on demand; the skill's scope is the invocation's `--workspace` argument; no envelope rewriting needed). If ARGUS wants β with concrete invocation contract worked out, that is a substantive design conversation, not a passing critique — and the design would need to surface to PLINY because re-opening A2 is the LOCKED-decision frame.

- **Weak point 5: The §27 canon section is long (~140-180 lines).** This is in line with §25 (110 lines) and §23 (75 lines) for PRINCIPAL-declared canon sections, but is at the upper end. A leaner version (one consolidated paragraph per sub-section rather than the §27.1 → §27.7 explicit sub-numbering) is plausible. **Why this shape anyway:** the directive A4 explicitly names sub-content items (3-step pattern + when-to-apply + cross-refs + §15 N=1 framing); the §27.1 → §27.7 structure makes each item legible and grep-able. Following the §25 / §23 sub-numbering precedent keeps the canon's section shapes parallel — readers landing at §27 find the same structural shape they find at §23 / §25, which lowers reading cost over time.

- **Weak point 6: The "Strangeness categories" table in SKILL.md (§4.2 item 6) bundles three shipped + three deferred categories into one table — the table itself is a load-bearing surface ADA could get wrong.** If the deferred categories table-row prose is ambiguous about "deferred per A7 to future arc" vs. "not implemented yet but would-be-nice", the A7 boundary leaks. **Why this shape anyway:** the table is the discoverable surface for the integration roadmap; surfacing the deferred categories where the shipped categories are listed gives future readers an at-a-glance view of "what this skill could grow into per arc-by-arc adoption." The mitigation is the §4.5 explicit A7 boundary inside SKILL.md, which makes the deferral framing explicit and load-bearing. CATO-3 audits this surface specifically.

- **Weak point 7: No probe exercises the §27 cross-refs against the new SKILL.md cross-refs from the OPPOSITE direction.** VERA-7 verifies cross-refs in the new artifacts point at existing targets; it does not verify that the new SKILL.md is reachable FROM the existing canon (i.e., §27 cross-refs include `substrate/skills/inspect-script-output/SKILL.md`). **Why this shape anyway:** §27.7 cross-references explicitly lists the skill path (per §6.2 outline); VERA-3 grep verifies the §27 prose includes the bullet. The combined VERA-3 + VERA-7 probes cover the bidirectionality, but the framing is "VERA-3 confirms §27 mentions the skill" + "VERA-7 confirms the skill mentions §27" rather than one explicit bidirectional probe. Acceptable per the probe-budget; ARGUS could ask for an explicit bidirectional probe to consolidate.

---

## §9 — Out of scope (deliberate; cross-ref A7)

Items NOT addressed by this design, with one-line rationale each:

- **Unwinding Arc 26's `check.sh` extensions.** A7 hard-lock; documented at §27.3 A7-boundary clause inside the new canon section.
- **Refactoring `check-bw-release/`.** A7 hard-lock; positive precedent, referenced not modified.
- **CAPTAIN_INSPECTOR new seat (Option γ).** Deferred per A7 to future arc when skill pattern proves out and gauntlet-pipeline integration is warranted; §3.1 deferral rationale.
- **CAPTAIN_VERA envelope extension (Option β).** Rejected on domain-distinct grounds at §3.1; if revisit, A2 LOCK re-opens.
- **Mechanical enforcement of §25 / §19.6 / §5.10 / §17 / §23.** A7 hard-lock; this arc establishes the COMPONENT, per-discipline integration is incremental future-arc work; §4.5 + §27.3 + §6.2 outline name this explicitly.
- **Multi-skill rollout (inspection-skill for deploy workflows, etc.).** A7 hard-lock; one worked example (substrate-update flow), incremental adoption at future arcs.
- **User-tier inspection support.** The skill defers user-tier scope-resolution the same way check-substrate-updates does (per its v0 scope note); future-arc work when user-tier inspection demand surfaces.
- **Cron-cadence default for the skill.** Per check-bw-release Arc 28 directive A7 precedent: operator picks; no scheduling defaults shipped.
- **Migration of any existing skill's intelligence to the inspection-agent layer.** A7 hard-lock; forward-only adoption.
- **Revisiting sibling tickets `stoa--32b.1` (PRINCIPAL-gate) / `stoa--k36` / `stoa--f37` / `stoa--ize` / `stoa--3qi` etc.** A7 hard-lock; separate.

---

## §10 — Residual questions for ARGUS

Items DAEDALUS explicitly wants ARGUS to pressure-test during cold audit (not blockers; surfacing for transparency):

1. **Is the "Strangeness categories" table's shipped/deferred split (3+3) honest about what this arc delivers?** Weak point 6 names this; CATO-3 audits scope-creep but ARGUS reads the design ahead of the build — ARGUS is the right seat to push back if the shipped subset over-promises or the deferred subset is too thinly scoped.

2. **Should the new §27 carry an explicit "this discipline is distinct from §11 cadence-axis" disambiguation paragraph?** §25 does this for the gate-vs-cadence distinction (§25.2 two-axis table). §27 is a third axis (architecture) the substrate now distinguishes; the §27 opening paragraph names this distinction but does not table-format it. ARGUS reads whether the disambiguation needs the §25-shape table format or whether the prose framing suffices.

3. **Is the A2 Option β rejection prose at §3.1 detailed enough?** Future arcs reading the design will want to know why VERA-extension was rejected; the prose at §3.1 grounds the rejection on "verifier-of-arc-deliverables vs. verifier-of-mechanical-script-outputs" domain split + one-job-per-agent (`operating-disciplines.md` §6.7 + `MAJOR_PLINY.md` §7.1). If ARGUS reads the grounding as too thin, a future arc re-opening A2 would have less to push back against.

4. **The §27.6 N=1 supporting evidence cites Arc 26's check.sh growth as "489 → 893 lines."** The actual current line count of `check-substrate-updates/check.sh` is 934 lines (per live verification at §2 design-time read of the file). The directive's prose (line 12) says "~20 min full-gauntlet to extend check.sh with 3 detection categories + routing footer" — the line count itself is not in the directive, but is in the retro §8 (line 202: "Arc 26 was the 'make check.sh smarter' approach. ~20 min of full gauntlet to add three drift categories + a routing footer to a bash script"). The "489 → 893" came from retro §4 line 106 (Arc 26 timeline: "check.sh 489→893 lines"). The post-polish line count growing to 934 (per live measurement) means Arc 26 + the rev2 polish + the Arc 29 base-vs-custom additions accreted further. Cite the directive-prose framing ("script-bloat empirical anchor") and the retro §4 line count ("489 → 893") rather than the current live count — the current live count includes Arc 29's additions which are not the Arc-26 script-bloat anchor specifically. ARGUS reads whether this framing is honest enough or whether the canon should cite the live count.

5. **The dispatch brief says "Phase C smoke beats specified per install.sh SKILL_NAMES check + grep + synthetic-inspection probe."** §7.4 covers these. Should the synthetic-inspection probe be a Phase C beat (PLINY runs) OR a Phase B beat (VERA runs)? §7.1 VERA-4 / VERA-5 covers it as a Phase B beat AND §7.4 re-runs it as a Phase C beat. The redundancy is intentional per `operating-disciplines.md` §6 ("redundancy IS the safety property"); ARGUS confirms or proposes consolidation.

---

## §11 — Phase plan for ADA (Phase 2)

For ADA's build phase, the load-bearing file-set:

1. **NEW** `substrate/skills/inspect-script-output/SKILL.md` (~180-220 lines per §4.2 outline). YAML frontmatter per §4.2; section outline per §4.2 items 1-12. Author: Denson Smith.
2. **NEW** `substrate/skills/inspect-script-output/check.sh` (~200-260 lines per §4.3 outline). Executable bit set. Cite-comments per §4.4 scoping discipline.
3. **NEW** `substrate/skills/inspect-script-output/fixtures/README.md` (~30-40 lines).
4. **NEW** `substrate/skills/inspect-script-output/fixtures/synthetic-apply-clean/` (file tree per §4.1).
5. **NEW** `substrate/skills/inspect-script-output/fixtures/synthetic-apply-strange/` (file tree per §4.1; `.planted-strangeness.md` documents what was planted for the probe to find).
6. **MODIFY** `substrate/install.sh` line 145 area — append `inspect-script-output` to SKILL_NAMES array. Single-line addition between line 145 (`check-bw-release`) and line 146 (`)`).
7. **MODIFY** `substrate/operating-disciplines.md` — insert new §27 between line 1282 (existing closing `---` after §26) and line 1283 (existing `## Agent-regime inverses`). New text per §6.2 outline; ~140-180 lines including the new closing `---` separator before the inverses section.

Total: 5 new files + 1 file-tree of fixtures + 2 file modifications. Comparable scope to Arc 29 / Arc 32. ADA's per-worktree venv (per `MAJOR_PLINY.md` §5.4) NOT needed — no Python in this arc.

---

## §12 — Cross-references

- `substrate/arcs/arc-33-build-directive.md` (A1-A10 LOCKED spec)
- `bw show stoa--32b.2` (ticket body + 2026-05-17 scope-refresh comment)
- `docs/sessions/2026-05-16-substrate-update-architecture-reframe--retro.md` §8 + §9 (load-bearing source)
- `substrate/operating-disciplines.md` §25 + §19.6 + §23 + §17 + §6.7.1 + §11 + §26 (the cross-ref network the new §27 plugs into)
- `substrate/MAJOR_PLINY.md` §5.10 + §5.9 + §5.9.4 (futures candidate + self-applied disciplines)
- `substrate/MAJOR_POLYBIUS.md` §17 + §4.8 (futures candidate + Step 3 routing)
- `substrate/skills/check-bw-release/SKILL.md` + `check.sh` (Arc 28 small-scope inspection-shape precedent; positive empirical anchor)
- `substrate/skills/check-substrate-updates/SKILL.md` + `check.sh` (Arc 26 + 29 script-bloat negative empirical anchor; referenced NOT modified per A7)
- `substrate/install.sh` lines 141-146 (SKILL_NAMES append target)
- `agents/design/arc-32/design.md` (style + structure model)
- `stoa--32b` (parent epic), `stoa--32b.1` / Arc 31 (sibling — §25 PRINCIPAL-gate), `stoa--dxw` / Arc 26 (empirical anchor), `stoa--501` (post-hoc cleanup), `stoa--s6n` / Arc 28 (check-bw-release precedent), `stoa--ads` / Arc 29 (base-vs-custom), `stoa--ewn` / Arc 32 (sibling canonification)
- `CAPTAIN_DAEDALUS_the_stoa.md` §6.1 (restatement gate; §1 above), §6.2 (self-assessed weak points; §8 above), §6.6 (credential-discipline — not applicable to this arc, named for completeness)

End design.
