# Arc 33 design — Mechanical-script / agent-inspection split — rev2

**Ticket:** `stoa--32b.2` (child of `stoa--32b` epic; sibling to `stoa--32b.1` shipped as Arc 31)
**Branch:** `arc-33/build` (worktree at `.claude/worktrees/arc-33-build/` per `MAJOR_PLINY.md` §5.9.4)
**Date:** 2026-05-17
**Status:** rev2 — supersedes `design.md` (rev1, kept as history per Arc 26 / Arc 32 precedent). ADA builds against rev2 only.
**Directive:** `substrate/arcs/arc-33-build-directive.md` (A1-A10 LOCKED)
**Authored by:** CAPTAIN_DAEDALUS_the_stoa, on behalf of the PRINCIPAL (Denson Smith).

---

## §0 — Rev2 changelog (what moved from rev1)

ARGUS cold-audit on rev1 returned REVISE-REQUIRED (2 P0 + 4 P1 + 2 P2). Rev2 resolves each finding with the picks below; the load-bearing structural changes are 0a + 0c + 0d.

- **§0a — P0-1 + P0-2 (folded resolution).** The scan helper renamed to `scan_name_collisions` (was `scan_base_path_custom_markers`). Mechanism: read `name:` field values across BOTH base paths AND custom paths within each scope (e.g., `.claude/agents/` + `.claude/agents/custom/`); flag any value that appears more than once. This grounds detection in `MAJOR_POLYBIUS.md` §17.4 (silent-collision footgun = duplicate `name:` field values within one scope) — there is NO `CUSTOM_` magic token; the canonical custom convention `name: <CAPTAIN>_<slug>` is correctly distinct from base by design, and a workspace that follows the convention triggers no finding. The scan reads custom paths but only to collect `name:` for cross-comparison; it does not flag custom files as strange in their own right. Strange fixture is now a duplicate-name collision: base `name: CAPTAIN_DAEDALUS_synthetic` AND custom `name: CAPTAIN_DAEDALUS_synthetic` (both files declare the same value within one scope). Per-arc cross-references at §4.4 + §6.2 + §7.1.
- **§0b — P1-1 (line numbers).** Live state at HEAD `b600df7` verified by Read on `substrate/operating-disciplines.md` lines 1280-1290: §26 closing `---` at line **1282**, blank at **1283**, `## Agent-regime inverses` heading at line **1284** (NO `---` opening that section). All three rev1 loci (§3.3 / §6.1 / §11) were inconsistent and wrong. Rev2 cites the single ground truth at §3.3 + §6.1 + §11 + §6.2 ADA insertion-locus prose: new §27 text inserts after line **1282** (the existing closing `---`) and before line **1283** (currently blank); the blank line absorbs into §27's own structure and §27 ends with a new `---` before the existing line **1284** (`## Agent-regime inverses`). Same numbers in all three loci.
- **§0c — P1-2 (file-disambiguation).** Every bare `§17.x` reference in design prose and in the SKILL.md authoring spec carries the `MAJOR_POLYBIUS.md` prefix where the source is POLYBIUS §17 (base-vs-custom); `operating-disciplines.md` prefix where the source is op-disc §17 (AI-team OSS-dep calculus — not used in this arc, but disambiguation discipline is universal). Rev2 §2 inputs table, §4.4 scoping discipline, §6.2 prose outline, §7 probes all carry explicit file prefixes.
- **§0d — P1-3 (fixture deployment).** Pick **(c) self-test mode**: NO tracked fixture files ship under `substrate/skills/inspect-script-output/`. The skill's `check.sh` carries a `--self-test` mode that builds a synthetic fixture tree in `$(mktemp -d)`, runs the inspection logic against it, asserts the expected outcomes (CLEAN path + STRANGE path), cleans up the temp dir, and exits 0/1 based on assertion results. Three load-bearing properties: (1) zero consumer-workspace pollution — no install.sh modification needed beyond the SKILL_NAMES append already required for A2 Option α; (2) the worked-example probe surface still exists for VERA-4 / VERA-5 to exercise; (3) fewer tracked files = smaller surface for CATO-1 authorship audit and ZENO file-count check. Rationale for (c) over (a) modify-install.sh-with-exclusion-pattern and (b) move-fixtures-outside-skill at §4.1.
- **§0e — P1-4 (β level distinction).** Rev2 §3.1 carries one explicit paragraph distinguishing seat-level β (CAPTAIN_VERA envelope-extension — rejected on domain-and-one-job grounds) from probe-level β (VERA probes that happen to do post-mechanical inspection — rejected on dispatch-scope grounds). Both rejections grounded and named so future arcs do not re-derive from scratch.
- **§0f — P2-1 (VERA-7 grep regex).** Rev1 had literal `N` / `M` placeholders. Rev2 §7.1 VERA-7 uses concrete `27\.[1-7]` regex (matching the §27.1 through §27.7 sub-sections this arc lands).
- **§0g — P2-2 (line-count framing).** Rev2 §6.2 §27.6 + §10 q4 explicitly frame: Arc 26 (`stoa--dxw`) is the **489 → 893** ship-line anchor specifically; the current `check-substrate-updates/check.sh` live count of 934 lines is downstream of Arc 26 — it includes Arc 29's base-vs-custom additions. The N=1 evidence cites the Arc 26 anchor (489 → 893) for the script-bloat empirical claim, not the live 934.
- **§0h — What stays from rev1.** A1-A10 LOCKED still in force. A2 = Option α (new skill). A3 = `inspect-script-output`. A4 = new top-level §27 in op-disc.md (NOT folded under §11). A6 authorship `Denson Smith` in SKILL.md frontmatter. A7 hard-locks unchanged. A8 N=1 framing unchanged. §2 inputs table line-range citations carry forward (verified accurate at HEAD `b600df7`).

---

## §1 — Intent (restatement per CAPTAIN_DAEDALUS §6.1 gate)

Arc 33 encodes the **mechanical-script / agent-inspection split** as a substrate pattern. Today's substrate puts recognition-of-strangeness inside scripts (Arc 26 grew `check.sh` from 489 → 893 lines to anticipate three new drift categories; further accretion from Arc 29 brought the live count to 934); PRINCIPAL declared 2026-05-16 that the recognition layer should move to an LLM-grade inspection-agent run after the mechanical script, with POLYBIUS triaging findings against the §25 PRINCIPAL-gate discipline. This arc ships the substrate **component** for that inspection layer (a new POLYBIUS-invokable skill), the **worked-example deployment** against the substrate-update flow (via a self-test mode that exercises a synthetic planted-strangeness tree in a temp dir at runtime), and the **discipline-doc canon** for when-to-apply the 3-step pattern. No mechanical enforcement of any specific discipline (§25 / §19.6 / `MAJOR_PLINY.md` §5.10 / `MAJOR_POLYBIUS.md` §17 / §23) is shipped — those integrations are future-arc work per A7.

**Restatement convergence with brief (per §6.1):** the directive's "your one job" sentence (line 9) names *encode the split as a substrate pattern + worked example + discipline-doc addition*. The restatement above matches that scope. The one assumption imported beyond the directive's literal text: the worked example is a **self-test deployment** of the skill — it exercises the inspection-agent shape against a synthetic strangeness fixture built at runtime, but does NOT auto-run after any production substrate operation. That distinction (worked-example-as-runtime-self-test vs. worked-example-as-production-integration) is the design's load-bearing reading of A7's hard-locked "no mechanical enforcement" boundary. If ARGUS reads the boundary differently, the worked-example scope is the place to push back.

**Imported assumptions named (per §6.1 + Arc 32 §2 model):**

- **A2 pick (α new skill) treated as DAEDALUS discretion, not PRINCIPAL-gate.** Directive A2 (line 81) explicitly delegates. Both seat-level β (VERA envelope) and probe-level β (VERA probes do post-mechanical-inspection) are rejected with explicit grounds at §3.1. Not a §25 gate.
- **A3 pick (`inspect-script-output`) treated as DAEDALUS discretion.** Directive A3 (line 91) explicitly delegates. User-tier POLYBIUS lean recorded; matches DAEDALUS's pick on naming-honesty grounds (verb-first; names the action). Not a §25 gate.
- **A4 pick (new top-level §27) treated as DAEDALUS discretion.** Directive A4 (line 105) gives two candidates (§11 area OR new top-level after §26). Folding under §11 would re-conflate the cadence-vs-gate axes §25.2 explicitly distinguishes. Top-level locus parallel to §23 / §25 / §26. Not a §25 gate.
- **A8 §15 N=1 framing.** §6.2 §27.6 carries the framing per scope-refresh comment + Arc 27/28/29/30/31/32 model. Empirical anchors named honestly: N=2 bit-by-it of make-script-comprehensive (Arc 26's 489 → 893 anchor + Arc 28's check-bw-release-build-time check.sh extensions — line-count anchor is the Arc 26 ship specifically; current 934 is downstream of Arc 26); N=1 small-scope precedent (check-bw-release Arc 28); discipline enters substrate canon off-gate on PRINCIPAL's 2026-05-16 declaration.
- **A6 authorship immutability.** New SKILL.md frontmatter carries `author: Denson Smith`. Per P1-3 resolution (no tracked fixture files), the rev1 fixtures/README.md authorship concern dissolves. §7.2 verification probe confirms.
- **A7 hard lock.** No edits to `check-substrate-updates/check.sh` or `check-bw-release/check.sh`. No new CAPTAIN seat. No multi-skill rollout. No PRINCIPAL-gate / attestation / signoff / scope mechanical enforcement. §4.5 names this explicitly inside the new SKILL.md.
- **The scope is comparable to Arc 29 / Arc 32.** Multi-file substrate canon + new skill component. Heavier than a discipline-only canonification arc (Arc 32 was 5 small candidates); roughly equivalent in surface to Arc 29's base-vs-custom convention. Per rev2 §0d, the runtime-fixture pick is **lighter** than rev1's tracked-fixture-tree (5 fewer files in the ship).

---

## §2 — Inputs (read-first artifacts and their roles)

| Artifact | Role in this design |
|---|---|
| `substrate/arcs/arc-33-build-directive.md` (213 lines) | Load-bearing spec. A1-A10 LOCKED. Architectural decisions NOT re-opened. |
| `bw show stoa--32b.2` body + 2026-05-17T19:14:17Z scope-refresh comment | Primary input prose alongside directive. The refresh comment locks A2 lean toward Option α and A3 lean toward `inspect-script-output`; both treated here as DAEDALUS-discretion picks with rationale named. |
| `docs/sessions/2026-05-16-substrate-update-architecture-reframe--retro.md` §8 (load-bearing source for 3-step pattern; §9 synthesis) | The PRINCIPAL declaration. §8 is the canonical articulation of "mechanical scripts; agents for intelligent inspection"; §9 synthesizes with §7's gate discipline (now shipped as §25). §15 N=1 framing in §6.2 §27.6 cites these sections. |
| `substrate/operating-disciplines.md` §25 (lines 1163-1262) — PRINCIPAL-gate | The triage-step partner. Step 3 of the 3-step pattern hands gated findings to PRINCIPAL per §25.3 BLOCK-not-TAG. The new SKILL.md prose cites op-disc §25 at the triage-step description. |
| `substrate/operating-disciplines.md` §19.6 (lines 849-894) — attestation-confabulation | Future-integration candidate (NOT shipped here per A7). New SKILL.md mentions op-disc §19.6 in its futures list. |
| `substrate/operating-disciplines.md` §23 (lines 1085-1138) — base-vs-custom universal | The scoping discipline the inspection-agent layer respects. §4.4 names this. |
| `substrate/operating-disciplines.md` §6.7.1 (lines 81-93) — N=1 promotion gate | §6.2 §27.6 honesty framing defers to op-disc §6.7.1 per A8. |
| `substrate/MAJOR_PLINY.md` §5.10 (lines 422-460) — signoff-accuracy | Future-integration candidate (NOT shipped here per A7). New SKILL.md mentions `MAJOR_PLINY.md` §5.10 in its futures list. |
| `substrate/MAJOR_PLINY.md` §5.9 + §5.9.4 (lines 329-421 area) | Self-applied for this arc per A9: worktree at `.claude/worktrees/arc-33-build/` confirmed; pre-branch hygiene PASS per PLINY's init handshake. |
| `substrate/MAJOR_POLYBIUS.md` §17 (lines 1050-1121) — base-vs-custom POLYBIUS refinement | POLYBIUS-tier refinement of op-disc §23 scoping. Cross-ref from new SKILL.md to MAJOR_POLYBIUS.md §17 alongside op-disc §23. **Load-bearing for rev2 §0a:** `MAJOR_POLYBIUS.md` §17.4 (lines 1088-1101) defines the silent-collision footgun semantic as **duplicate `name:` field values within one scope** (NOT a magic token prefix); rev2's `scan_name_collisions` helper grounds detection in that canon. |
| `substrate/install.sh` lines 141-146 (SKILL_NAMES array) | The deploy register. Append target between line 145 (`check-bw-release`) and line 146 (`)`). Per rev2 §0d, this is the ONLY install.sh modification this arc requires. |
| `substrate/install.sh` lines 709-724 (skill-tree `cp -R` deploy loop) | The mechanism that motivated rev2 §0d: `cp -R "$src_skill"/. "$dest_skill"/` deploys EVERYTHING under each named skill dir. Tracked fixture files would propagate to every consumer workspace; runtime self-test fixture mode dissolves the concern. |
| `substrate/skills/check-bw-release/SKILL.md` (122 lines) + `check.sh` (222 lines) | Small inspection-shape skill precedent (Arc 28). The new SKILL.md frontmatter shape, the per-workspace state pattern, and the cite-comment discipline at API boundaries all copy from this skill. Layout precedent: ships SKILL.md + check.sh ONLY — no fixtures/ directory. Rev2 §0d aligns with this precedent. **Author: Denson Smith** confirmed in frontmatter (line 4). |
| `substrate/skills/check-substrate-updates/SKILL.md` (202 lines) + `check.sh` (934 lines live) | Larger inspection-shape skill — the NEGATIVE empirical anchor for script-bloat. NOT modified per A7. Live line count (934) is downstream of Arc 26's 489 → 893 ship and Arc 29's base-vs-custom additions; §6.2 §27.6 cites Arc 26 specifically. Layout precedent: ships SKILL.md + apply.sh + check.sh + revert.sh ONLY — no fixtures/ directory. Rev2 §0d aligns. |
| `agents/design/arc-32/design.md` | Style + structure model for substrate-canon design artifacts. |
| `agents/design/arc-33/design.md` (rev1) | History per Arc 26 / Arc 32 rev-supersession precedent. ADA does NOT build against rev1; rev2 supersedes. |

**Live ground state at design-authoring time (per §19.6 attestation-honesty):**

- `git rev-parse HEAD` in main worktree = `b600df7` (matches PLINY's init handshake on `stoa--32b.2`); `git rev-parse origin/main` = `b600df7`; identical.
- arc-33/build worktree exists at `.claude/worktrees/arc-33-build/`; current branch in that worktree is `arc-33/build`.
- `agents/design/arc-33/design.md` (rev1, 528 lines) exists; `design-rev2.md` (this file) is the new rev2 artifact in the same dir.
- `substrate/operating-disciplines.md` line 1282 = `---`; line 1283 = blank; line 1284 = `## Agent-regime inverses` (verified by Read at design-authoring time).
- `substrate/install.sh` SKILL_NAMES = `agent-author / check-substrate-updates / credential-discipline / check-bw-release` (4 entries; append target between line 145 and line 146).
- `substrate/install.sh` lines 709-724 = `cp -R` loop over `${SKILL_NAMES[@]}` (verified by Read).
- `substrate/MAJOR_POLYBIUS.md` §17.4 silent-collision footgun semantic = "duplicate `name:` field values within one scope" (verified by Read at lines 1088-1101).

---

## §3 — Architectural decisions resolved (A2 / A3 / A4 picks)

### §3.1 — A2 pick: Option α (new substrate-tier skill); explicit seat-vs-probe-level β distinction

**Pick:** Option α. New substrate-tier skill at `substrate/skills/inspect-script-output/` mirroring the shape of `substrate/skills/check-bw-release/`.

**Rationale (why not β, why not γ):**

- **Option β — two distinct readings, both rejected (rev2 §0e expansion):**
  - **Seat-level β (CAPTAIN_VERA envelope extension) rejected on domain + one-job grounds.** VERA is *verifier-of-arc-deliverables* — its envelope is shaped around "did the build under this dispatch ship the artifact the spec asked for, run the probes the design named, produce the verdict in the verdict shape." That domain is different from *verifier-of-mechanical-script-outputs in production substrate operations*. Folding generic post-mechanical inspection into VERA's envelope would extend VERA into a second domain; the one-job-per-agent contract VERA's envelope inherits from `operating-disciplines.md` §6.7 says one CAPTAIN does one job. A VERA expanded to two domains rotates the envelope contract every future arc needs to reason about.
  - **Probe-level β (VERA probes that happen to do post-mechanical inspection) rejected on dispatch-scope grounds.** At the probe level, a VERA probe today IS "execute command, check output" — structurally similar to what the new skill's check.sh does. The grounds for rejection are NOT "different shape" but **different scope**: VERA's probes are scoped to the dispatch's build artifacts (the probes the DAEDALUS design names in §7); they fire once, against the artifacts of that single arc. The inspection-agent layer's probes are scoped to **workspace state surrounding any mechanical substrate operation** — they fire repeatedly, across arcs, against operator-invoked production substrate operations, not against any single dispatch's build artifacts. Re-using VERA probes for that purpose would either (a) bind VERA's per-dispatch probe-list to operator-invokable production operations (rotating VERA's dispatch contract for every future check), or (b) require a new "standing probe" sub-category in VERA's envelope that crosses dispatches (a substantial envelope re-shape). Both are heavier than a skill that POLYBIUS invokes on demand. The skill-shape preserves the per-invocation contract.
  - **Both β readings deferred together as out-of-scope.** Either β requires re-opening A2's LOCKED decision; per §25 PRINCIPAL-gate framing, that would be project-direction work, not DAEDALUS discretion. The skill-shape is the LIGHTER pick at both seat and probe level; a future arc with empirical evidence that the skill-shape is wrong-shaped can re-open A2 with grounds.

- **Option γ (new CAPTAIN seat e.g. CAPTAIN_INSPECTOR) deferred.** A new CAPTAIN seat is a structural pipeline component PLINY dispatches as a phase; weight comparable to introducing CAPTAIN_ARGUS or CAPTAIN_CATO. The 3-step pattern at retro §8/§9 names POLYBIUS as the dispatcher (not PLINY); the inspection-agent runs AFTER a mechanical operation by POLYBIUS invocation, not as part of a gauntlet phase. A CAPTAIN seat would be the right shape if the inspection layer were a gauntlet-pipeline component; today it is a POLYBIUS-invoked post-mechanical layer. If the skill pattern proves out across 2-3 future arcs AND gauntlet-pipeline integration becomes warranted, a future arc can promote the skill to a CAPTAIN seat — the deferral is intentional.

- **Option α justifications:**
  1. **Empirical precedent.** check-bw-release (Arc 28) shipped as a small inspection-shape skill and is working without script-bloat.
  2. **Lightest deploy.** Append one entry to `install.sh` SKILL_NAMES (line 146). Per rev2 §0d, NO additional install.sh modification needed (no fixture exclusion pattern).
  3. **Lightest deprecate.** If the pattern doesn't prove out (per A8 N=1 caveat), removing the skill is one `install.sh --prune-obsolete` and one removal from SKILL_NAMES.
  4. **POLYBIUS-invokable matches the 3-step pattern.** Step 3 (POLYBIUS triage) presupposes POLYBIUS as the operator of Steps 1 and 2.

### §3.2 — A3 pick: skill name = `inspect-script-output`; worked-example domain = substrate-update flow (LOCKED)

**Pick:** `inspect-script-output`. Worked-example domain (LOCKED per A3): substrate-update flow.

**Rationale (vs. the other three candidates):** unchanged from rev1 — verb-first; names the action; reads cleanly in a POLYBIUS invocation; leaves namespace room for future `inspect-*` skills. The three rejected candidates (`script-output-inspection`, `post-script-inspection`, `inspection-agent`) are documented inline at the new SKILL.md "Why this skill exists" preamble paragraph for future readers.

**Worked-example domain (LOCKED per A3):** substrate-update flow. The skill ships with a check script + a `--self-test` mode that builds a synthetic strangeness tree in `$(mktemp -d)` at invocation time and exercises the inspection logic against it. Per directive A3 paragraph 4 + the strangeness-categories enumeration:

- **Unauthorized commits** (e.g., probe-residue from prior gauntlets — sector-4 probe-mutation case from Arc 26 / `stoa--501` is the canonical worked example);
- **File states inconsistent with intent** — specifically **silent-collision `name:` duplicates per `MAJOR_POLYBIUS.md` §17.4** (e.g., a custom CAPTAIN file declaring a `name:` value already declared by a base CAPTAIN within the same scope; Claude Code silently drops one on discovery);
- **Drift verdict mismatching detailed state** (CURRENT verdict but unexpected file mtimes; DRIFTED verdict with no detail lines; etc.);
- **Cleanup claims not executed** (post-signoff verification candidate per `MAJOR_PLINY.md` §5.10 — NOT shipped this arc, named in futures list);
- **Attestation claims not live-verified** (post-attestation verification candidate per `operating-disciplines.md` §19.6 — NOT shipped this arc, named in futures list);
- **PRINCIPAL-gate clauses encountered but not paused-on** (post-execution audit candidate per `operating-disciplines.md` §25 — NOT shipped this arc, named in futures list).

**Critical distinction (load-bearing for A7 boundary):** the skill SHIPS WITH scan helpers for the first three categories. The last three categories are named in the SKILL.md "Strangeness categories" table with the explicit note *"future-arc work — this arc establishes the skill component; per-discipline mechanical enforcement is incremental across future arcs per directive A7."*

### §3.3 — A4 pick: new top-level §27 in operating-disciplines.md after §26

**Pick:** new top-level section `## 27. Mechanical-script / agent-inspection split` inserted after the line **1282** `---` (closing §26) and before line **1284** (`## Agent-regime inverses`). Live state at HEAD `b600df7` verified: line 1282 = `---`; line 1283 = blank; line 1284 = `## Agent-regime inverses` heading (NO `---` opening that section). The blank at 1283 absorbs into the new §27 block; §27's own closing `---` then separates §27 from the existing `## Agent-regime inverses` section.

**Rationale (vs. folding under §11 autonomous-mode-setup):** unchanged from rev1 — §11 is cadence-axis canon; §27 is architecture-axis canon; folding would re-conflate the two axes §25.2 explicitly distinguishes. Top-level locus parallel to §23 / §25 / §26 (each PRINCIPAL-declared 2026-05-1X discipline gets its own home).

---

## §4 — The new skill: `inspect-script-output`

### §4.1 — File set ADA will build (rev2: runtime fixtures, no tracked fixture tree)

```
substrate/skills/inspect-script-output/
  SKILL.md                            # ~180-220 lines (see §4.2 outline)
  check.sh                            # ~260-340 lines (see §4.3 outline) — includes --self-test mode
```

That is the entire skill file set. **No `fixtures/` directory ships under this skill.** Per rev2 §0d (P1-3 resolution), the self-test fixture tree is generated at runtime in `$(mktemp -d)` inside the `--self-test` code path; the temp dir is removed before `check.sh --self-test` returns.

**Rationale for runtime-fixture pick (c) over alternatives (a) and (b):**

- **(a) Modify install.sh to add a `fixtures/`-exclusion pattern in the `cp -R` loop (lines 709-724).** Adds non-trivial logic to install.sh for one skill's benefit, when no other skill needs fixtures today. Future arcs adding a fixture-needing skill would either re-use the pattern (carrying the install.sh complexity forward as the multi-skill case) or proliferate per-skill exclusion patterns. The install.sh touch this arc already needs (SKILL_NAMES append) is mechanical and one-line; adding a fixture-exclusion pattern is meaningfully more design — and per A7 directive scope-discipline, that design should not piggyback on this arc.
- **(b) Move fixtures outside the skill directory entirely (e.g., `substrate/skill-fixtures/inspect-script-output/`).** Creates a new top-level substrate convention for one consumer. Future fixture-needing skills face the same question (use this dir? create their own?); answering it requires a new convention design that A7 does not authorize. Also the skill loses local-discoverability of its fixtures (a future reader of the skill must walk up out of `substrate/skills/` to find the test surface).
- **(c) Runtime-generate fixtures via `--self-test`.** Picked. Zero ship-tree changes; zero consumer-workspace pollution; the fixture surface lives inside the check.sh code (a `build_self_test_tree` function builds it from heredocs into a `mktemp -d` location, runs the inspection against it, asserts CLEAN-path + STRANGE-path, cleans up). The fixture surface is **self-documenting in code** — a reader of check.sh sees both the planted strangeness AND the assertion against it in one place. This also lets ADA build a STRANGE-path assertion against multiple planted-strangeness types if the skill's scan helpers grow; today the planted strangeness is one silent-collision case.

**The runtime self-test tree shape (synthetic; built inside `$(mktemp -d)` at `--self-test` invocation):**

```
<mktemp-dir>/
  clean/
    .claude/
      MAJOR_POLYBIUS_self_test.md             # representative base file
      operating-disciplines.md                # representative base file
      agents/
        CAPTAIN_DAEDALUS_self_test.md         # name: CAPTAIN_DAEDALUS_self_test
        custom/
          CAPTAIN_DEPLOYER_self_test.md       # name: CAPTAIN_DEPLOYER_self_test_custom (distinct slug; correctly-conventioned)
    .git-HEAD-fixture                          # one-line synthetic HEAD SHA
  strange/
    .claude/
      MAJOR_POLYBIUS_self_test.md
      operating-disciplines.md
      agents/
        CAPTAIN_DAEDALUS_self_test.md         # name: CAPTAIN_DAEDALUS_self_test
        custom/
          CAPTAIN_DAEDALUS_self_test.md       # name: CAPTAIN_DAEDALUS_self_test (DUPLICATE — planted silent-collision per §17.4)
    .git-HEAD-fixture
```

The CLEAN tree exercises the no-strangeness code path: a correctly-conventioned custom CAPTAIN (`name: CAPTAIN_DEPLOYER_self_test_custom`) lives alongside a base CAPTAIN (`name: CAPTAIN_DAEDALUS_self_test`), no collision, no strangeness; expected output is the CLEAN message. The STRANGE tree exercises the silent-collision code path: a custom CAPTAIN file declares `name: CAPTAIN_DAEDALUS_self_test` (the EXACT value declared by the base CAPTAIN `.claude/agents/CAPTAIN_DAEDALUS_self_test.md` in the same scope); the scan_name_collisions helper detects the duplicate value and emits a strangeness finding citing both file paths.

**Why no real `.git/` in the runtime tree:** the skill's mechanical check is filesystem-state inspection, not git operations. The `.git-HEAD-fixture` is a one-line text file the skill reads via the same env-var mechanism check-bw-release uses for upstream-API mock. The `--self-test` mode sets `INSPECT_SCRIPT_OUTPUT_FIXTURE_MODE=1` automatically inside the test function; production invocations leave the env-var unset and read real `git rev-parse HEAD`.

### §4.2 — SKILL.md outline (frontmatter + sections)

**Frontmatter (verbatim — per A6 authorship immutability + Arc 27 stoa--uly convention copied from check-bw-release):**

```yaml
---
name: inspect-script-output
description: Inspect post-mechanical-script workspace state for strangeness — anomalies the script wasn't pre-programmed to surface. Reads the workspace's deployed-file tree, git HEAD, and any optional script-output artifact, and emits a structured strangeness report POLYBIUS triages per operating-disciplines.md §27. Per A7 boundary, this skill establishes the 3-step pattern component; per-discipline mechanical enforcement (operating-disciplines.md §25 PRINCIPAL-gate / §19.6 attestation / MAJOR_PLINY.md §5.10 signoff / MAJOR_POLYBIUS.md §17 base-vs-custom) is incremental future-arc work. Triggers on requests like "inspect substrate state after apply", "check post-install workspace strangeness", "run inspection agent on substrate update", "post-script state inspection".
author: Denson Smith
---
```

**Section outline** (ADA writes verbatim per ARGUS pass; lengths approximate):

1. `# inspect-script-output — the inspection-agent layer of the 3-step substrate-update pattern` (header)
2. `## Why this skill exists` — script-bloat empirical anchor (Arc 26 / 489 → 893 lines as the ship-anchor specifically; live 934 is downstream of Arc 26 per Arc 29 additions); PRINCIPAL's 2026-05-16 declaration verbatim; the 3-step pattern (1. mechanical script → 2. inspection agent → 3. POLYBIUS triage); cross-ref to `operating-disciplines.md` §27 as canonical home. ~25 lines.
3. `## When to use this skill` — invocation triggers (after `apply.sh` or `install.sh` runs against a registered workspace; before posting a `MAJOR_PLINY.md` §5.10 signoff that names a workspace cleanup claim); explicit "do not invoke" boundary (not a substitute for `check.sh`; not a mechanical PRINCIPAL-gate enforcer in this arc per A7). ~20 lines.
4. `## What the skill ships` — file list: SKILL.md + check.sh (no fixtures dir; self-test mode generates fixtures at runtime); per-workspace state file location convention copied from check-bw-release; no `.gitignore` line needed. ~25 lines.
5. `## How to invoke` — three worked invocations: standard call (`<skill-dir>/check.sh --workspace <abs-path>`), self-test mode (`<skill-dir>/check.sh --self-test` — builds and tears down its own synthetic tree; no `--workspace` argument needed in this mode), explicit-categories (`<skill-dir>/check.sh --workspace <abs-path> --only name-collisions`). ~30 lines.
6. `## Strangeness categories` — table with two columns: category name + shipped-this-arc | future-arc. Shipped: unauthorized-commits (git-history scan vs. recent apply baseline), name-collisions (silent-collision `name:` duplicates per `MAJOR_POLYBIUS.md` §17.4), drift-verdict-mismatch. Future-arc (explicit "NOT shipped this arc per A7"): cleanup-claims-not-executed (`MAJOR_PLINY.md` §5.10 partner), attestation-claims-not-verified (`operating-disciplines.md` §19.6 partner), PRINCIPAL-gate-clauses-encountered-but-not-paused (`operating-disciplines.md` §25 partner). ~40 lines.
7. `## How to test` — `<skill-dir>/check.sh --self-test` is the single canonical test path; documents what the self-test asserts (CLEAN path + STRANGE path, both via the runtime-built synthetic tree); points to the `build_self_test_tree` function in check.sh for the planted-strangeness specifics. ~25 lines.
8. `## State-file shape` — one-line per-workspace baseline at `<skills-parent>/.inspect-script-output-last-run` recording the last-inspected HEAD SHA + ISO-8601 timestamp. ~15 lines.
9. `## Per-workspace deployment` — pattern copied verbatim-shape from check-bw-release. ~15 lines.
10. `## POLYBIUS triage protocol` — how POLYBIUS routes the strangeness report per `operating-disciplines.md` §27 step 3: routine technical-tier findings → POLYBIUS fixes inline per `MAJOR_POLYBIUS.md` §4.8 + user-tier-approves-tech-decisions; PRINCIPAL-gate findings → workflow PAUSES per `operating-disciplines.md` §25.3 BLOCK-not-TAG. ~25 lines.
11. `## What this skill is NOT` — explicit non-scopes: not an auto-fixer; not a substitute for `check.sh`; not a CAPTAIN-pipeline component; cross-ref §3.1 deferral rationale. ~20 lines.
12. `## Related` — `operating-disciplines.md` §27 (canonical pattern home); `operating-disciplines.md` §25 (gate discipline); `operating-disciplines.md` §23 + `MAJOR_POLYBIUS.md` §17 (base-vs-custom scoping); `MAJOR_POLYBIUS.md` §17.4 (silent-collision footgun — load-bearing for name-collisions scan); `operating-disciplines.md` §19.6 + `MAJOR_PLINY.md` §5.10 (futures); `substrate/skills/check-bw-release/` (sibling structural model); `substrate/skills/check-substrate-updates/` (script-bloat empirical anchor — referenced, NOT modified per A7); `stoa--32b.2` (this arc); `docs/sessions/2026-05-16-substrate-update-architecture-reframe--retro.md` §8 (load-bearing source). ~15 lines.

**Estimated total:** 180-220 lines.

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

# Argument parsing — --workspace <abs-path> (required UNLESS --self-test);
# --only <category-list> optional; --since <SHA> optional; --self-test (runs
# the self-test mode, builds + tears down a temp synthetic tree, asserts
# CLEAN + STRANGE paths, exits 0/1 based on assertion results, no --workspace
# needed); -h | --help. See check-bw-release lines 49-74 for argparse shape.

# === Scan helpers ===
#
# read_git_head <workspace>: echo the workspace's HEAD SHA.
#   - Fixture mode (INSPECT_SCRIPT_OUTPUT_FIXTURE_MODE=1, set by --self-test):
#     read from <workspace>/.git-HEAD-fixture (one-line text file).
#   - Production: cd <workspace> && git rev-parse HEAD.
#   - Defang per check-bw-release lines 113-127 model.
#
# scan_unauthorized_commits <workspace> <baseline-sha>: enumerate commits in
# <workspace>'s .claude/ between <baseline-sha> and HEAD; surface any commit
# message NOT matching a substrate-canonical pattern (apply-from-substrate,
# install-from-substrate, prune-from-substrate). This is the "sector-4 probe
# residue" case from Arc 26 / stoa--501 canonical worked example.
#   - Fixture mode: no-op (the synthetic tree has no real .git/).
#
# scan_name_collisions <workspace>: detect silent-collision name-duplicates
# per MAJOR_POLYBIUS.md §17.4 (lines 1088-1101). For each Claude-Code-relevant
# scope, walk all files in that scope (BOTH base and custom paths) and
# extract YAML frontmatter `name:` field values. Within one scope, if any
# `name:` value appears more than once across the collected files, that is
# a silent-collision finding. Emit one finding per collision-set with all
# colliding file paths cited.
#   - Scope = .claude/agents/ — Claude Code scans this dir recursively per
#     https://code.claude.com/docs/en/sub-agents, so base files at
#     .claude/agents/CAPTAIN_*.md and custom files at .claude/agents/custom/
#     CAPTAIN_*_<slug>.md share one name-space. The scan collects from BOTH
#     subtrees and cross-checks for duplicate name: values.
#   - Cite-comment at the helper top references operating-disciplines.md
#     §23 (universal base-vs-custom) + MAJOR_POLYBIUS.md §17 (POLYBIUS-tier
#     refinement) + MAJOR_POLYBIUS.md §17.4 (the silent-collision footgun
#     this helper specifically encodes). Mirror the cite-comment discipline
#     at substrate/skills/check-substrate-updates/check.sh apply_substitutions
#     + parse_skill_names_from_install (per Arc 26).
#   - SCOPE NOTE: the helper reads custom paths to collect name: values for
#     cross-comparison; it does NOT flag custom files as strange in their
#     own right. Workspace customization is operator-owned per §23.3; the
#     §17.4 silent-collision footgun is a SCOPE-LEVEL defect both base and
#     custom contributors share, and detection of it serves both.
#
# scan_drift_verdict_mismatch <workspace>: if check-substrate-updates is
# deployed AND a recent check.sh output is cached, compare its verdict
# against an mtime sweep of .claude/ — surface any inconsistency. Skips
# silently if check-substrate-updates is not deployed at the workspace.
#
# emit_report <findings>: write the strangeness report to stdout; CLEAN
# message if findings empty; STRANGENESS DETECTED with per-category sections
# if not.

# === Self-test mode ===
#
# build_self_test_tree <mktemp-root>: write the CLEAN + STRANGE synthetic
# trees into <mktemp-root>/clean/ and <mktemp-root>/strange/ per §4.1 shape.
# Files written via heredocs inline; representative base + custom CAPTAIN
# files with deliberate name: values; clean tree has distinct names, strange
# tree has duplicate name: CAPTAIN_DAEDALUS_self_test in base and custom.
# Also writes <mktemp-root>/<tree>/.git-HEAD-fixture with a synthetic SHA.
#
# run_self_test: top-level for --self-test mode.
#   1. ROOT=$(mktemp -d) ; trap "rm -rf $ROOT" EXIT
#   2. build_self_test_tree "$ROOT"
#   3. Set INSPECT_SCRIPT_OUTPUT_FIXTURE_MODE=1 ; run the four scan helpers
#      against "$ROOT/clean" ; assert emit_report output starts with the
#      CLEAN prefix.
#   4. Run the four scan helpers against "$ROOT/strange" ; assert
#      emit_report output contains "STRANGENESS DETECTED" AND contains a
#      finding referencing both .claude/agents/CAPTAIN_DAEDALUS_self_test.md
#      AND .claude/agents/custom/CAPTAIN_DAEDALUS_self_test.md.
#   5. Print one PASS line per assertion; exit 0 if all PASS, exit 1
#      otherwise. EXIT trap cleans up the temp dir.

# === Main dispatch ===
#   1. Argument validation (if --self-test: skip --workspace requirement;
#      run run_self_test; exit with its result).
#   2. Determine workspace path (resolve, exists, has .claude/).
#   3. Read baseline from state file (or initialize silently on first run).
#   4. Run selected scan helpers (all categories, or per --only).
#   5. emit_report.
#   6. Update state file with current HEAD + timestamp.
#   7. exit 0 (drift is informational; never blocks — same exit-code
#      discipline as check-bw-release and check-substrate-updates).
```

**Estimated length:** 260-340 lines including the inline help text (sed-extracted via `--help` per check-bw-release lines 66-67 pattern), the four scan helpers (~30-50 lines each), the build_self_test_tree function with inline heredocs (~60-80 lines), the run_self_test function (~30 lines), the argument parser (~30 lines), the report emitter (~30 lines). Longer than rev1's ~200-260 estimate because of the build_self_test_tree heredocs that previously lived as tracked fixture files.

### §4.4 — Scope discipline the skill respects

The skill respects `operating-disciplines.md` §23 (universal base-vs-custom) + `MAJOR_POLYBIUS.md` §17 (POLYBIUS-tier refinement). **Cite-comments at every scan-helper-top reference both file-disambiguated sections AND `MAJOR_POLYBIUS.md` §17.4 specifically for the scan_name_collisions helper.**

**The scope-respecting rule, by scan helper:**

- **scan_unauthorized_commits:** walks `.claude/` commit history. Does NOT distinguish base vs. custom commits — any unauthorized commit to `.claude/` is a finding regardless of which subtree it touched. Rationale: an unauthorized commit at a custom path is still a substrate-state-anomaly worth POLYBIUS triage; per `operating-disciplines.md` §23.3 custom authoring is the workspace's responsibility, but unauthorized commits (not landed via a substrate-canonical operation) are by definition outside the operator's intentional authoring path.
- **scan_name_collisions:** reads `.claude/agents/` recursively (BOTH `.claude/agents/CAPTAIN_*.md` base files AND `.claude/agents/custom/CAPTAIN_*_<slug>.md` custom files) to collect `name:` field values for cross-comparison per `MAJOR_POLYBIUS.md` §17.4. The helper reads custom paths but does NOT flag custom files as strange in their own right; it flags only the duplicate-name strangeness §17.4 names. Per `operating-disciplines.md` §23 + `MAJOR_POLYBIUS.md` §17, custom file content authoring is workspace-owned; the silent-collision footgun is a scope-level defect both parties share, and detection serves both.
- **scan_drift_verdict_mismatch:** consumes `check-substrate-updates/check.sh` output, which itself is scoped to BASE files per its own cite-comments (per `operating-disciplines.md` §23.5 + `MAJOR_POLYBIUS.md` §17.6). The verdict-mismatch check inherits that scoping — it does not separately walk custom paths.

**Rev2 §0a load-bearing distinction:** rev1 said "scan helpers EXCLUDE custom paths" — that was a single-rule overreach. Rev2 corrects: only the scan helpers that flag FILE CONTENT exclude custom paths (today's set: none of the three shipped scan helpers flag custom file content as strange in its own right); helpers that read custom paths for CROSS-COMPARISON purposes (today's set: scan_name_collisions) do read custom paths. The discipline is "do not flag custom file content as strange"; it is NOT "do not read custom paths at all."

### §4.5 — Explicit A7 boundary inside SKILL.md

The "Strangeness categories" section (§4.2 item 6 above) carries an explicit note:

> **A7 boundary (per `substrate/arcs/arc-33-build-directive.md`):** this skill establishes the inspection-agent COMPONENT and the 3-step pattern's worked example. Per-discipline mechanical enforcement (`operating-disciplines.md` §25 PRINCIPAL-gate / `operating-disciplines.md` §19.6 attestation-confabulation / `MAJOR_PLINY.md` §5.10 signoff-accuracy / `MAJOR_POLYBIUS.md` §17 base-vs-custom / etc.) is INCREMENTAL future-arc work. The skill's shipped scan helpers cover the first three categories above (unauthorized-commits / name-collisions / drift-verdict-mismatch); the last three are deliberately deferred — a future arc dispatches the relevant integration per use case.

---

## §5 — Authorship audit (per A6 + substrate/CLAUDE.md)

New files added by this arc, with their author-like fields:

| File | Author-like field | Value |
|---|---|---|
| `substrate/skills/inspect-script-output/SKILL.md` | YAML frontmatter `author:` | `Denson Smith` |
| `substrate/skills/inspect-script-output/check.sh` | None (shebang scripts; PLINY commit Author: governs git-side attribution) | n/a |
| `substrate/operating-disciplines.md` new §27 | None (file-level authorship is the substrate's; no per-section author field in op-disc.md) | n/a |
| `substrate/install.sh` SKILL_NAMES append | None (config file; PLINY commit Author: governs) | n/a |

Per rev2 §0d, the rev1 `fixtures/README.md` + `fixtures/synthetic-apply-*` files DROP from the ship — no authorship concerns surface from them.

**Verification probe in §7:** explicit grep against the new SKILL.md frontmatter for `author: Denson Smith` (probe §7.5). If any field surfaces a different name, ADA STOPS per `substrate/CLAUDE.md` "stop and ask" discipline.

---

## §6 — operating-disciplines.md new §27 (prose ADA pastes)

### §6.1 — Insertion locus + structural shape

**Insert after line 1282 (existing `---` closing §26) and before line 1284 (existing `## Agent-regime inverses` heading).** Live state verified at HEAD `b600df7`: line 1282 = `---`, line 1283 = blank, line 1284 = `## Agent-regime inverses` (NO `---` opening that section). The blank at 1283 absorbs into the new §27 block; the new text starts with `## 27. Mechanical-script / agent-inspection split` heading and ends with a `---` separator before the existing `## Agent-regime inverses` section.

New text: a `## 27. Mechanical-script / agent-inspection split` heading + ~140-180 lines of canon prose + a final `---` separator. The §27 prose follows the standard PRINCIPAL-declared-discipline shape (§23 / §25 / §26 / Arc 32's §5.10): one-paragraph framing → numbered sub-sections (§27.1 discipline, §27.2 the 3-step pattern, §27.3 when-to-apply + boundary, §27.4 per-seat behavior, §27.5 worked example pointer, §27.6 N=1 provenance + accretion path, §27.7 cross-references).

### §6.2 — Prose outline (ADA writes verbatim; word-counts approximate; ARGUS audits the wording)

**Opening paragraph (~5 lines).** Names the split: mechanical scripts stay narrow; recognition-of-strangeness moves to an LLM-grade inspection-agent run after the mechanical operation; POLYBIUS triages findings against §25 gate discipline. Distinct from §11 (autonomous-mode-setup cadence axis) and §25 (PRINCIPAL-gate authorization axis) — this section is an *architecture axis* discipline (where intelligence lives across mechanical / recognition / triage layers).

**§27.1 The discipline (PRINCIPAL declaration) (~15 lines).** PRINCIPAL declared 2026-05-16 after Arc 26 ship + `stoa--501` revert sequence. The declaration verbatim (from `bw show stoa--32b.2` body):

> *"We are spending way too much time trying to get script workflows perfect when the answer is to run the script, then run an agent with a script to check what happened including anything strange and then let polybius fix any of the strangeness with human approval if necessary."*

This is project-direction authority per §6.7.1 honest-scope framing (see §27.6 for the N=1 accretion path). The load-bearing source for the architectural framing is `docs/sessions/2026-05-16-substrate-update-architecture-reframe--retro.md` §8 (PRINCIPAL's prose on where intelligence lives) and §9 (synthesis with §7's gate discipline now shipped as §25).

**§27.2 The 3-step pattern (~25 lines).** A numbered list with one-line per step + one-line per step on which seat owns it:

1. **Mechanical script** runs (`apply.sh` / `install.sh` / deploy workflows / etc.) — deterministic, narrow. Stays small over time; does NOT grow recognition logic. Owner: the workspace's `.claude/skills/` deployed scripts; or `substrate/install.sh` at substrate-tier.
2. **Inspection agent** runs a verification script + reads result + workspace state + surfaces anything strange — including things the script wasn't pre-programmed to enumerate. LLM-grade recognition, not pattern-match. Owner: POLYBIUS-invoked skill (worked example: `substrate/skills/inspect-script-output/`); respects base-vs-custom scoping per §23 / `MAJOR_POLYBIUS.md` §17.
3. **POLYBIUS triage** — routes findings:
   - **Routine technical-tier findings** → POLYBIUS fixes inline per fix-now `MAJOR_POLYBIUS.md` §4.8 + user-tier-approves-tech-decisions discipline.
   - **PRINCIPAL-gate findings** → workflow PAUSES per §25.3 BLOCK-not-TAG; autonomous mode does NOT relax. Owner: POLYBIUS; PRINCIPAL is exception-handler.

Distinguishing property vs. intelligence-in-script: the script enumerates KNOWN strangeness; the inspection agent finds NOVEL strangeness (the things the script wasn't pre-programmed to notice).

**§27.3 When to apply + A7 boundary (~20 lines).** When to apply: substrate-update flow (post-`apply.sh` / post-`install.sh`); deploy workflows (when one lands at this team in the future); future script-based workflows where the recognition surface is unbounded or grows. Discipline framing (verbatim per directive A4 prose): *"when designing a script-based workflow, prefer mechanical-narrow + inspection-agent over make-script-comprehensive."*

**A7 boundary (load-bearing — names what this arc DOES NOT do):**

- This arc establishes the COMPONENT (the skill at `substrate/skills/inspect-script-output/`) + the worked-example deployment (substrate-update flow, via `--self-test` runtime fixture) + this canon section.
- This arc does NOT mechanically enforce §25 / §19.6 / `MAJOR_PLINY.md` §5.10 / `MAJOR_POLYBIUS.md` §17 — per-discipline integration is INCREMENTAL future-arc work.
- This arc does NOT unwind Arc 26's `check.sh` additions. `check.sh` stays as-is; the inspection-agent pattern is the *forward* shape. Future migration of `check.sh` intelligence into the inspection-agent layer is a separate arc when the pattern proves out.
- This arc does NOT build inspection-agents for every existing script. Worked example is ONE; concrete adoption is incremental.
- This arc does NOT promote the skill to a CAPTAIN seat (CAPTAIN_INSPECTOR) — that is Option γ deferred per directive A2 to a future arc.

**§27.4 Per-seat behavior summary (~12 lines + table).** Three-column table: Seat | Role in the 3-step pattern | Cross-ref.

| Seat | Role | Cross-ref |
|---|---|---|
| Mechanical-script author (DAEDALUS designing; ADA building) | Design scripts to STAY mechanical-narrow. When a new recognition surface is needed, design the inspection-agent layer, not a script extension. | `CAPTAIN_DAEDALUS.md` §6, `CAPTAIN_ADA.md` (build envelope) |
| Inspection-agent (skill or CAPTAIN) | Read post-mechanical state; surface strangeness; respect §23 / `MAJOR_POLYBIUS.md` §17 scoping. | `substrate/skills/inspect-script-output/SKILL.md` (worked example) |
| POLYBIUS (triage) | Route routine findings to fix-now; route PRINCIPAL-gate findings to PAUSE per §25.3. | `MAJOR_POLYBIUS.md` §4.8 (fix-now), `operating-disciplines.md` §25 |
| PRINCIPAL | Disposition on gated findings per §25.3; project-direction calls on architectural promotions. | `operating-disciplines.md` §25 |

**§27.5 Worked example pointer (~10 lines).** This arc ships `substrate/skills/inspect-script-output/` as the substrate-update-flow worked example. The skill's `--self-test` mode builds a synthetic strangeness tree in a temp dir at runtime; the planted-strangeness case exercises `MAJOR_POLYBIUS.md` §17.4 silent-collision detection (duplicate `name:` field values within one Claude-Code scope). No fixture files are tracked under the skill directory — the test surface lives inside the check.sh code (`build_self_test_tree` function) and is exercised via `check.sh --self-test`.

**§27.6 N=1 provenance + accretion path (~25 lines per §A8 + Arc 27/28/29/30/31/32 N=1 framing model).** Per §6.7.1 honest-scope: PRINCIPAL declared this discipline 2026-05-16 (project-direction authority, captured at `docs/sessions/2026-05-16-substrate-update-architecture-reframe--retro.md` §8 and at `bw show stoa--32b.2` ticket body). §6.7.1 defers to the canon-promotion gate (multiple observations + controlled comparison + substrate-level pattern); §6.7.1 does not carve out a separate "PRINCIPAL-declaration shortcut." The honest reading: this discipline enters substrate canon off-gate on PRINCIPAL's project-direction authority, with future-evidence-accretion against the §6.7.1 gate still required for promotion to "structural lesson" status.

Supporting evidence at the time of this writing (per scope-refresh comment 2026-05-17):

- **N=2 bit-by-it of make-script-comprehensive (negative anchor):** Arc 26 (`stoa--dxw`) extended `check.sh` from **489 → 893 lines** to add MISSING + OBSOLETE + uncommitted-state detection (the load-bearing script-bloat anchor cited here); Arc 28 (`stoa--s6n`) added further check.sh logic for the bw-upgrade discipline. The current live line count of `substrate/skills/check-substrate-updates/check.sh` is **934** lines — that count is downstream of Arc 26 (it includes Arc 29's base-vs-custom additions); the cited 489 → 893 anchor is the Arc 26 ship specifically.
- **N=1 small-scope inspection-shape precedent (positive anchor):** `substrate/skills/check-bw-release/` (Arc 28) ships a small inspection-shape skill that's working without script-bloat. Single instance today; this arc's worked example accretes the second instance.
- **N=multi cross-discipline coverage:** §25 + §19.6 + `MAJOR_PLINY.md` §5.10 + `MAJOR_POLYBIUS.md` §17 + `MAJOR_PLINY.md` §5.9.4 all benefit from mechanical-script-then-agent-inspection enforcement at future arcs. Today none are mechanically enforced (per A7); the pattern's future-arc adoption is the accretion path against §6.7.1.

The discipline is in NOW because PRINCIPAL named it; structural-lesson confidence accretes over future arcs that apply the pattern at new domains (deploy workflows, build verification, etc.) AND across the per-discipline mechanical-enforcement integrations the A7 boundary defers. Do NOT over-generalize beyond what PRINCIPAL named — the pattern is *prefer mechanical-narrow + inspection-agent over make-script-comprehensive WHEN designing script-based workflows*, not *all scripts must have inspection-agents now*. Same N=1 framing as Arc 27's `MAJOR_POLYBIUS.md` §16.6, Arc 28's `operating-disciplines.md` §22.3, Arc 29's `MAJOR_POLYBIUS.md` §17.5, Arc 30's `MAJOR_PLINY.md` §5.9.3, Arc 31's `operating-disciplines.md` §25.6, and Arc 32's `operating-disciplines.md` §19.6 / `MAJOR_PLINY.md` §5.10 / `MAJOR_PLINY.md` §5.9.4.

**§27.7 Cross-references (~15 lines).**

- §10 (operating engagement — cadence axis) + §11 (autonomous-mode-setup checklist) — the cadence-discipline canon this section is *distinct from* (architecture axis, not cadence axis). Same disambiguation shape §25 uses.
- §25 (PRINCIPAL-gate discipline) — the triage-step partner; Step 3 of the 3-step pattern hands gated findings to PRINCIPAL per §25.3 BLOCK-not-TAG. Folding §25 into §27 would conflate gate-axis with architecture-axis disciplines; the two cross-reference each other and stand as separate loci.
- §19.6 (attestation-confabulation) — future-integration partner; the inspection-agent layer is the WHERE that COULD verify attestation claims at attestation time. NOT shipped this arc per A7.
- §23 (base-vs-custom universal) + `MAJOR_POLYBIUS.md` §17 (POLYBIUS refinement, including §17.4 silent-collision footgun) — the scoping discipline the inspection-agent layer respects + the load-bearing canon for the name-collisions scan helper.
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
- `ls substrate/skills/inspect-script-output/` → directory exists; lists exactly `SKILL.md` and `check.sh` (no `fixtures/` dir per rev2 §0d).
- `test -x substrate/skills/inspect-script-output/check.sh` → executable bit set.
- Expected: both checks PASS.

**Probe VERA-2 — install.sh SKILL_NAMES append (easy-easy).** Verify the deploy register updated.
- `grep -n 'inspect-script-output' substrate/install.sh` → matches line at SKILL_NAMES append point (after line 145 `check-bw-release`).
- `awk '/^SKILL_NAMES=\(/,/^\)/' substrate/install.sh | grep -c 'inspect-script-output'` → returns `1`.
- Expected: PASS.

**Probe VERA-3 — operating-disciplines.md §27 present + structure intact (easy-easy).** Verify the canon section landed.
- `grep -n '^## 27\. Mechanical-script / agent-inspection split' substrate/operating-disciplines.md` → matches exactly once.
- `grep -n '^### 27\.[1-7]' substrate/operating-disciplines.md` → returns 7 lines (§27.1 through §27.7).
- `grep -c 'inspection-agent\|inspection agent\|mechanical-script' substrate/operating-disciplines.md` → ≥ 12.
- Expected: PASS.

**Probe VERA-4 — self-test mode runs and PASSES (easy-easy).** Verify the skill's self-test asserts both CLEAN and STRANGE paths successfully.
```bash
substrate/skills/inspect-script-output/check.sh --self-test
```
- Expected stdout: ≥ 2 lines beginning `PASS` (one for the CLEAN-path assertion, one for the STRANGE-path assertion).
- Expected exit code: 0.
- Expected side-effect: no temp dir survives (`trap "rm -rf $ROOT" EXIT` per §4.3 outline).

**Probe VERA-5 — self-test STRANGE-path finding cites both colliding files (medium-easy).** Verify the STRANGE-path assertion specifically detects the planted silent-collision per `MAJOR_POLYBIUS.md` §17.4 — duplicate `name:` value across base + custom files within the `.claude/agents/` scope.
- Run `check.sh --self-test 2>&1` and inspect output for the STRANGE-path branch.
- Expected: the STRANGE-path PASS line is preceded by a finding block citing both `.claude/agents/CAPTAIN_DAEDALUS_self_test.md` AND `.claude/agents/custom/CAPTAIN_DAEDALUS_self_test.md` as the colliding pair with `name: CAPTAIN_DAEDALUS_self_test`.
- Expected exit code: 0.

**Probe VERA-6 — base-vs-custom scoping respected (hard-easy).** Verify the skill's scope discipline per §4.4 rev2 distinction: scan_name_collisions DOES read custom paths (for cross-comparison), other scan helpers DO NOT flag custom file content as strange in its own right.
- Inspect `check.sh` source for cite-comments at each scan helper referencing `operating-disciplines.md` §23 + `MAJOR_POLYBIUS.md` §17 (all helpers) AND `MAJOR_POLYBIUS.md` §17.4 specifically at scan_name_collisions.
- Inspect `check.sh` source for the SCOPE NOTE at scan_name_collisions top per §4.3 outline ("reads custom paths to collect name: values for cross-comparison; does NOT flag custom files as strange in their own right").
- Behavioral cross-check (extends the self-test): the CLEAN tree includes a correctly-conventioned custom CAPTAIN (`name: CAPTAIN_DEPLOYER_self_test_custom`) — its presence MUST NOT trigger a finding (VERA-4 PASS on the CLEAN path already implies this; this probe sanity-confirms by reading the build_self_test_tree heredoc to verify the correctly-conventioned custom file is in the CLEAN tree).
- Expected: all three checks PASS.

**Probe VERA-7 — cross-refs resolve (easy-easy).** Verify every cross-ref the new SKILL.md + new §27 names points at a section/file that actually exists.
- Extract all `operating-disciplines.md §<n>.<m>` mentions from the new SKILL.md; for each, `grep -n '^### <n>\.<m>\b\|^## <n>\.\b' substrate/operating-disciplines.md` → match. The concrete regex for the new §27 sub-sections: `grep -n '^### 27\.[1-7]\b' substrate/operating-disciplines.md` → returns 7 lines.
- Extract all `MAJOR_POLYBIUS.md §<n>` and `MAJOR_PLINY.md §<n>` mentions from new §27 + SKILL.md; for each, grep the corresponding file → match. Concrete spot-checks: `grep -n '^### 17\.4' substrate/MAJOR_POLYBIUS.md` → returns 1 line (the silent-collision footgun section); `grep -n '^### 5\.10' substrate/MAJOR_PLINY.md` → returns 1 line.
- Extract all `stoa--XXX` ticket IDs from new §27 + SKILL.md; for each, `bw show <id> 2>&1` → does not error.
- Expected: all matches PASS; no broken cross-refs.

**Probe VERA-8 — check.sh against the-stoa workspace (regression sanity).** Verify the existing check-substrate-updates skill correctly reports the-stoa workspace as DRIFTED on the substrate files this arc edits (sanity that the substrate edits actually landed; sanity that the deploy mechanism is consistent).
- `substrate/skills/check-substrate-updates/check.sh --workspace /c/Users/denso/claude_projects/the-stoa`
- Expected: DRIFTED or DRIFTED + MISSING for `.claude/operating-disciplines.md` (new §27 added) + `.claude/install.sh` (SKILL_NAMES append) + MISSING for `.claude/skills/inspect-script-output/` (new skill).

### §7.2 — CATO probes (cold-read for wording drift, scope creep, attribution)

**CATO-1 — Authorship audit.** Per directive A6 + Phase B item 7. Verify `grep -A 1 '^author:' substrate/skills/inspect-script-output/SKILL.md` returns exactly `author: Denson Smith`; no other author-like field surfaces a different name anywhere in the arc's diff. CATO sweeps the diff with `git diff main...arc-33/build | grep -i -E 'author|owner|creator|maintainer|by:|copyright'` → every match should be either the new SKILL.md frontmatter (Denson Smith) or pre-existing prose-text mentions (not author-like fields).

**CATO-2 — Wording-drift across the new SKILL.md + new §27 + ticket body.** Per Phase B Cato cold-read item. Verify the 3-step pattern language matches between (a) ticket body, (b) retro §8, (c) new §27, (d) new SKILL.md. The three-step phrasing should be consistent — "mechanical script → inspection agent → POLYBIUS triage" or substantively equivalent. Drift between the four loci is a CATO finding.

**CATO-3 — A7 scope-creep audit.** Per directive A7 hard-locks. CATO cold-reads the diff for any of: edits to `check-substrate-updates/check.sh` (any line); edits to `check-bw-release/check.sh` (any line); new CAPTAIN_*.md file; new sibling-ticket edits; install.sh modifications BEYOND the one-line SKILL_NAMES append (per rev2 §0d, no fixture-exclusion pattern shipped); any mechanical enforcement of §25 / §19.6 / `MAJOR_PLINY.md` §5.10 / `MAJOR_POLYBIUS.md` §17 in the new check.sh (verify by absence: scan helpers cover unauthorized-commits / name-collisions / drift-verdict-mismatch ONLY, per §4.2 item 6 shipped-this-arc subset). Any A7 violation is a CATO P0 finding.

**CATO-4 — §15 N=1 honesty audit.** Per directive A8. CATO cold-reads the new §27.6 + new SKILL.md "Why this skill exists" for over-generalization. The substrate canon must say "PRINCIPAL declared 2026-05-16; this enters off-gate on project-direction authority; future-evidence-accretion against §6.7.1 still required" — NOT "the inspection-agent pattern IS the substrate-canonical approach" or any structural-claim overreach. CATO flags any sentence reading as universal-claim where the framing should be N=1-with-accretion-path.

**CATO-5 — 3-step pattern clarity.** Per Phase B CATO cold-reads item. Verify future POLYBIUSes reading the new §27 can identify (a) which step they are at, (b) which seat owns each step, (c) how to invoke step 2 (pointer to skill), (d) how step 3 routes per §25. Cold-read with no prior context; if any of the four is ambiguous, CATO finding.

**CATO-6 — Inspection-skill domain scope clarity.** Per Phase B CATO cold-reads item. Verify the new SKILL.md "When to use this skill" and "What this skill is NOT" sections make it clear what is in-scope (mechanical-script output inspection) vs. out-of-scope (CAPTAIN-driven verification — that's still VERA/CATO/etc.'s pipeline-time work).

### §7.3 — ZENO probes (deliverable spec-check)

**ZENO-1 — D1 (substrate component) DONE.** Per ticket body deliverable 1 + directive A2. Cite: `substrate/skills/inspect-script-output/` exists with SKILL.md + check.sh (no fixtures dir per rev2 §0d).

**ZENO-2 — D2 (worked-example deployment) DONE.** Per ticket body deliverable 2 + directive A3 LOCKED. Cite: SKILL.md "Strangeness categories" section names the substrate-update-flow worked example explicitly; check.sh implements the scan for the shipped-this-arc strangeness categories; `check.sh --self-test` exercises the planted silent-collision strangeness via the runtime-built synthetic tree.

**ZENO-3 — D3 (operating-disciplines.md addition) DONE.** Per ticket body deliverable 3 + directive A4. Cite: `operating-disciplines.md` §27 added; 3-step pattern + when-to-apply + cross-refs all present per §6.2 outline above.

**ZENO-4 — D4 (Arc 26 forward-migration plan) deliberately PARTIAL per A7.** Ticket body deliverable 4 names "possibly: revisit Arc 26's check.sh additions" with the explicit "NOT a regression of Arc 26 ... a forward-migration plan if the inspection-agent pattern proves out." A7 hard-locks "no unwinding Arc 26." The new §27.3 A7-boundary clause names this deferral explicitly. ZENO confirms PARTIAL with the deferral cited.

### §7.4 — Phase C smoke beats (PLINY pre-PR)

Per directive Phase C lines 194-198. PLINY runs before opening PR:

- `grep -n "mechanical-script\|inspection-agent\|inspection agent" substrate/operating-disciplines.md` → matches in new §27.
- `ls substrate/skills/inspect-script-output/` → SKILL.md + check.sh.
- `grep -n "inspect-script-output" substrate/install.sh` → matches SKILL_NAMES append.
- **Synthetic-inspection smoke beat:** run `substrate/skills/inspect-script-output/check.sh --self-test`; both CLEAN-path and STRANGE-path assertions PASS; exit 0.
- `substrate/skills/check-substrate-updates/check.sh --workspace .` → expected DRIFTED + MISSING on substrate files this arc edits (sanity).

### §7.5 — Authorship probe summary

CATO-1 above is the load-bearing authorship gate. PLINY-side smoke probe: `grep -i -E 'author|owner|creator|maintainer' substrate/skills/inspect-script-output/SKILL.md` → expected exact match `author: Denson Smith` and nothing else. Any other author-like field surfacing is a PRE-PR blocker.

---

## §8 — Self-assessed weak points (per CAPTAIN_DAEDALUS §6.2)

Auditing rev2 honestly for what ARGUS is likely to catch on second-cold-read.

- **Weak point 1: scan_name_collisions detection logic correctness is implementation-load-bearing.** Rev2 grounds detection in `MAJOR_POLYBIUS.md` §17.4 (duplicate `name:` values within one scope). The helper must (a) correctly enumerate the scope's discovery-relevant subtrees (per §17.4: `.claude/agents/` recursive — both `.claude/agents/*.md` direct AND `.claude/agents/custom/**/*.md` recursive), (b) correctly extract YAML frontmatter `name:` field values (handle quoted/unquoted, leading whitespace, multi-doc YAML), (c) correctly cross-compare values across the collected set, (d) emit findings with both colliding paths cited. A bug in (b) — e.g., regex misses `name: "FOO"` quoted form — would yield false-negative on a real collision. **Why this shape anyway:** the alternative (relying on Claude Code's own runtime collision-detection behavior) is exactly what §17.4 names as the silent-collision footgun (the runtime is silent). VERA-5 + VERA-6 + the self-test STRANGE-path assertion cover the detection-correctness surface against the canonical case; if ADA's implementation handles edge cases (quoted values, etc.) the self-test should grow assertions for them.

- **Weak point 2: The self-test mode CANNOT exercise scan_unauthorized_commits.** The synthetic tree has no real `.git/` (`.git-HEAD-fixture` text file substitutes for HEAD SHA only, not for git-history walks). VERA-8 against the-stoa workspace exercises the helper against a real history, but if the workspace happens to have no unauthorized commits, the smoke beat doesn't exercise the strangeness-detected branch. **Why this shape anyway:** rev2 §0d picked runtime fixtures specifically to avoid consumer-workspace pollution; including a real `.git/` directory inside `$(mktemp -d)` would introduce a nested-git-repo problem at test-time (the temp dir would either be a git repo by accident or would need a `git init` step the self-test does today not perform). The gap is acknowledged; a future arc adding a deeper self-test for git-history scans is an honest follow-up.

- **Weak point 3: The §27 canon section is long (~140-180 lines).** In line with §25 (110 lines) and §23 (75 lines) for PRINCIPAL-declared canon sections, but at the upper end. **Why this shape anyway:** directive A4 explicitly names sub-content items (3-step pattern + when-to-apply + cross-refs + §15 N=1 framing); the §27.1 → §27.7 structure makes each item legible and grep-able. Following the §25 / §23 sub-numbering precedent keeps section shapes parallel.

- **Weak point 4: The "Strangeness categories" table in SKILL.md bundles three shipped + three deferred categories.** Load-bearing surface ADA could get wrong if the deferred-row prose is ambiguous about "deferred per A7" vs. "not implemented yet but would-be-nice." **Why this shape anyway:** the table is the discoverable surface for the integration roadmap; the §4.5 explicit A7 boundary inside SKILL.md makes the deferral framing explicit. CATO-3 audits this surface specifically.

- **Weak point 5: The self-test runs at every `--self-test` invocation; there is no caching / opt-out.** A POLYBIUS who runs `--self-test` repeatedly pays the (small) cost of building + tearing down the synthetic tree each time. **Why this shape anyway:** the self-test is the canonical test surface; caching would invite stale-test-passes (a code change in check.sh that broke a scan helper might still PASS against a cached assertion). The cost is in-context cheap (heredocs into mktemp + four scan helpers against ~6 small files); the discipline-property of run-fresh-every-time is worth more than the cycles saved.

- **Weak point 6: Rev2 §0d's `--self-test` pick removes the discoverable "fixtures live HERE" convention rev1 ship would have established.** A future inspection-shape skill needing tracked fixtures (if the use case arises) would face the same install.sh-deploy-pollution question rev2 just answered. The answer for those future skills is: either pick `--self-test` again (the substrate's runtime-fixture convention), OR design a tracked-fixture mechanism then (and probably modify install.sh with the exclusion pattern that rev2 §0d chose not to ship). **Why this shape anyway:** A7 directive scope-discipline says no scope-creep this arc; the install.sh-exclusion-pattern design is meaningfully more than a one-line SKILL_NAMES append. If/when a future skill genuinely needs tracked fixtures, that arc designs the convention.

- **Weak point 7: The probe-level β rejection at §3.1 (rev2 §0e) is grounded in "different dispatch scope" — a future arc could push back that operator-invokable POLYBIUS skills are themselves a kind of out-of-dispatch surface and the distinction is thin.** The counter-counter: POLYBIUS-invoked skills are an established substrate convention (check-substrate-updates / check-bw-release / agent-author / credential-discipline all live as POLYBIUS-invokable skills); VERA's per-dispatch probe-list is also an established convention; expanding VERA's probe-list contract to a third "standing operator-invokable" category is structurally heavier than adding one more skill to the existing skill-convention. **Why this shape anyway:** the lighter-weight reading wins on operating-disciplines.md §6 redundancy + simplest-shape grounds.

---

## §9 — Out of scope (deliberate; cross-ref A7)

Items NOT addressed by this design, with one-line rationale each:

- **Unwinding Arc 26's `check.sh` extensions.** A7 hard-lock; documented at §27.3 A7-boundary clause.
- **Refactoring `check-bw-release/`.** A7 hard-lock; positive precedent, referenced not modified.
- **CAPTAIN_INSPECTOR new seat (Option γ).** Deferred per A7 to future arc when skill pattern proves out and gauntlet-pipeline integration is warranted.
- **CAPTAIN_VERA envelope extension (Option β).** Both seat-level β AND probe-level β rejected at §3.1 (rev2 §0e); if revisit, A2 LOCK re-opens.
- **Mechanical enforcement of `operating-disciplines.md` §25 / §19.6 / `MAJOR_PLINY.md` §5.10 / `MAJOR_POLYBIUS.md` §17 / `operating-disciplines.md` §23.** A7 hard-lock; this arc establishes the COMPONENT.
- **Multi-skill rollout (inspection-skill for deploy workflows, etc.).** A7 hard-lock; one worked example.
- **User-tier inspection support.** Skill defers user-tier scope-resolution same as check-substrate-updates.
- **Cron-cadence default for the skill.** Per check-bw-release Arc 28 directive A7 precedent: operator picks.
- **Migration of any existing skill's intelligence to the inspection-agent layer.** A7 hard-lock; forward-only adoption.
- **install.sh fixture-exclusion-pattern design.** Per rev2 §0d, runtime self-test mode dissolves the need; A7 scope-discipline says no piggyback design.
- **Tracked-fixture-mechanism convention for future inspection-shape skills.** Per rev2 §8 weak point 6, deferred to a future arc that genuinely needs tracked fixtures.
- **Revisiting sibling tickets `stoa--32b.1` / `stoa--k36` / `stoa--f37` / `stoa--ize` / `stoa--3qi` etc.** A7 hard-lock; separate.

---

## §10 — Residual questions for ARGUS (rev2 re-audit)

Items DAEDALUS explicitly wants ARGUS to pressure-test during cold re-audit (not blockers; surfacing for transparency):

1. **Is the rev2 §0d self-test pick honest about test-coverage scope?** §8 weak point 2 names this: scan_unauthorized_commits is NOT exercised by `--self-test` because the synthetic tree has no real `.git/`. VERA-8 covers it against the-stoa workspace, but that's a workspace-specific probe not a self-contained skill-validation. ARGUS pressure-tests whether the test-coverage gap is honestly framed or if it warrants a stronger mitigation.

2. **Is the scan_name_collisions detection logic correctness (§8 weak point 1) ADA-buildable from §4.3's outline + the canon at `MAJOR_POLYBIUS.md` §17.4, or does it need a more detailed pseudo-code spec?** The outline names the (a)-(d) sub-tasks but does not pseudo-code the YAML-`name:` extraction regex. ARGUS reads whether the spec is concrete enough or if ADA would benefit from a sketch like `grep -E '^name: *"?([A-Z_]+)"?' file | awk ...`.

3. **Is the §3.1 explicit seat-vs-probe-level β paragraph (rev2 §0e) detailed enough?** The probe-level grounds rest on "different dispatch scope" — §8 weak point 7 names the counter ARGUS could push. ARGUS reads whether the grounding is sufficient or if a future arc re-opening A2 at the probe level would have too little to push back against.

4. **Does the "Strangeness categories" table's shipped/deferred 3+3 split honestly represent what this arc delivers?** Same question as rev1 q1, carried forward. The rev2 shipped subset (unauthorized-commits / name-collisions / drift-verdict-mismatch) replaces rev1's (unauthorized-commits / base-path-custom-markers / drift-verdict-mismatch); name-collisions is the canon-grounded replacement per rev2 §0a. ARGUS pressure-tests whether the swap is honest.

5. **Should the new §27 carry an explicit §25.2-shape disambiguation table for the cadence-vs-gate-vs-architecture three-axis distinction?** Same question as rev1 q2. §25.2 has a two-axis table; §27 introduces a third axis (architecture) but the §27 opening paragraph names the distinction in prose, not table format. ARGUS reads whether prose suffices or table is warranted.

---

## §11 — Phase plan for ADA (Phase 2)

For ADA's build phase, the load-bearing file-set (per rev2 §0d, simplified):

1. **NEW** `substrate/skills/inspect-script-output/SKILL.md` (~180-220 lines per §4.2 outline). YAML frontmatter per §4.2; section outline per §4.2 items 1-12. Author: Denson Smith.
2. **NEW** `substrate/skills/inspect-script-output/check.sh` (~260-340 lines per §4.3 outline). Executable bit set. Cite-comments per §4.4 scoping discipline (every helper top; `MAJOR_POLYBIUS.md` §17.4 specifically at scan_name_collisions). Includes `--self-test` mode with `build_self_test_tree` + `run_self_test` per §4.3 outline.
3. **MODIFY** `substrate/install.sh` line 145 area — append `inspect-script-output` to SKILL_NAMES array. Single-line addition between line 145 (`check-bw-release`) and line 146 (`)`). NO additional install.sh modification (no fixture-exclusion pattern per rev2 §0d).
4. **MODIFY** `substrate/operating-disciplines.md` — insert new §27 between line 1282 (existing closing `---` after §26) and line 1284 (existing `## Agent-regime inverses` heading). The blank line at 1283 absorbs into the new block. New text per §6.2 outline; ~140-180 lines including the new closing `---` separator before the inverses section.

Total: **2 new files + 2 file modifications.** Comparable scope to Arc 32 (substrate canonification batch); LIGHTER than Arc 29 (no new convention design beyond canon-grounding). ADA's per-worktree venv (per `MAJOR_PLINY.md` §5.4) NOT needed — no Python in this arc.

---

## §12 — Cross-references

- `substrate/arcs/arc-33-build-directive.md` (A1-A10 LOCKED spec)
- `bw show stoa--32b.2` (ticket body + 2026-05-17 scope-refresh comment + ARGUS rev1 verdict comments)
- `docs/sessions/2026-05-16-substrate-update-architecture-reframe--retro.md` §8 + §9 (load-bearing source)
- `substrate/operating-disciplines.md` §25 + §19.6 + §23 + §6.7.1 + §11 + §26 (the cross-ref network the new §27 plugs into)
- `substrate/MAJOR_PLINY.md` §5.10 + §5.9 + §5.9.4 (futures candidate + self-applied disciplines)
- `substrate/MAJOR_POLYBIUS.md` §17 + §17.4 + §4.8 (futures candidate + Step 3 routing; §17.4 load-bearing for scan_name_collisions)
- `substrate/skills/check-bw-release/SKILL.md` + `check.sh` (Arc 28 small-scope inspection-shape precedent; positive empirical anchor; layout precedent for ship-tree shape)
- `substrate/skills/check-substrate-updates/SKILL.md` + `check.sh` (Arc 26 + 29 script-bloat negative empirical anchor; referenced NOT modified per A7)
- `substrate/install.sh` lines 141-146 (SKILL_NAMES append target) + 709-724 (cp -R deploy loop motivating rev2 §0d)
- `agents/design/arc-32/design.md` (style + structure model)
- `agents/design/arc-33/design.md` (rev1 — history; ADA does NOT build against rev1)
- `stoa--32b` (parent epic), `stoa--32b.1` / Arc 31 (sibling — §25 PRINCIPAL-gate), `stoa--dxw` / Arc 26 (empirical anchor — 489 → 893 line-count anchor), `stoa--501` (post-hoc cleanup), `stoa--s6n` / Arc 28 (check-bw-release precedent), `stoa--ads` / Arc 29 (base-vs-custom — live 934 count downstream of this arc), `stoa--ewn` / Arc 32 (sibling canonification)
- `CAPTAIN_DAEDALUS_the_stoa.md` §6.1 (restatement gate; §1 above), §6.2 (self-assessed weak points; §8 above), §6.6 (credential-discipline — not applicable to this arc)

End rev2 design.
