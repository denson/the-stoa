# Arc 29 build directive — Base-vs-custom agent convention encoded in substrate canon

**Audience:** the fresh Claude Code session opened to build Arc 29 deliverables (MAJOR_PLINY at the-stoa tier).
**Authored by:** user-tier MAJOR_POLYBIUS + the PRINCIPAL (Denson Smith).
**Status:** active directive. **Arc 28 (`stoa--s6n`) is CLOSED**; precondition satisfied.
**Bw ticket:** `stoa--ads` (the work-unit; independent of stoa--32b epic).
**Builds on:** Arcs 1-28 (the-stoa main as of `efffb8b`).

**Your one job:** encode the **base-vs-custom agent convention** as substrate canon. PRINCIPAL declared the architectural model on 2026-05-17: each workspace has a BASE stoa team (deployed from substrate; mechanically updatable) and optionally CUSTOM agents/processes (workspace-authored; separately maintained). Today the substrate tools assume "drift = bug" and would silently overwrite customizations sitting at base-file paths. This arc encodes the convention so customizations have a canonical home substrate tools respect.

**Why P1 + ship-before-railway:** the railway_stoa team is queued to design + build a custom railway agent set as the empirical anchor of this architecture. They cannot dispatch until this convention exists, otherwise their custom agents will live at unsafe paths.

One ticket, one coherent push:
- **stoa--ads** (P1) — substrate canon + tooling for base-vs-custom convention. Body has 6 deliverables (D1-D6), acceptance probes, out-of-scope hard-locks.

This is a foundational substrate arc. Medium-scope; substantive but contained. DAEDALUS round expected with high probability of ARGUS revision given architecture-sensitivity. Plus a load-bearing empirical question (Claude Code auto-discovery of custom agent paths) that affects the convention pick.

---

## Comms — autonomous mode via bw, radio-check protocol

Same shape as Arcs 25/26/27/28. PROJECT-TIER POLYBIUS (separate Claude Code session, activated from `HUMAN_paste-polybius-arc-29-instruction.md`) is your radio-check peer; you communicate via comments on `stoa--ads`. USER-TIER POLYBIUS dispatched this arc + will do QA pass at arc close per PRINCIPAL's pattern.

PRINCIPAL is **not** the relay for routine status — beadwork is.

**bw command syntax** is in `substrate/MAJOR_PLINY.md` §6.1. `bw comment <id> "text"` is positional, no `--body` flag. `bw close <id> --reason "text"` — `--reason` is a flag.

**Polling discipline** per `substrate/operating-disciplines.md` §7. On dispatch, post init handshake on `stoa--ads` naming cron id + cadence. Heartbeat every ≤30 min.

PLINY in autonomous mode. PRINCIPAL + user-tier POLYBIUS are exception-handlers — project-direction calls, ship/no-ship, substance disagreement after one round, authorship/copyright/PRINCIPAL-final-say content, irreducible ambiguity, peer silence > 60 min, arc closes.

---

## Read first

Before any design or build work, read in order:

1. **`bw show stoa--ads` ticket body in full.** Primary spec. Body has problem statement + 6 deliverables (D1-D6) + 6 acceptance probes + out-of-scope hard-locks + §15 N=1 caveat + cross-refs. Treat as primary input prose alongside this directive.

2. **`substrate/install.sh`** — current deploy logic. `SKILL_NAMES` array, CAPTAIN deploy loop, templates deploy loop, MAJOR deploy lines. D3 modifies this — needs careful read to identify all the glob/path points that need base-vs-custom scoping.

3. **`substrate/skills/check-substrate-updates/check.sh`** — current scan logic. D4 modifies this — same shape concern.

4. **`substrate/skills/check-substrate-updates/apply.sh`** — current apply logic. D5 modifies — same shape concern.

5. **`substrate/MAJOR_POLYBIUS.md`** — current section structure. D1 adds new section about base-vs-custom architecture. DAEDALUS picks insertion locus (likely near §1-§3 architectural framing, or as new section near §16 POLYBIUS lifecycle; cross-ref the lifecycle section since they share the "substrate is a deployable baseline; consumer workspaces evolve" framing).

6. **`substrate/operating-disciplines.md`** — current section structure. D1 also adds universal-team framing here (parallel to MAJOR_POLYBIUS.md but seat-neutral).

7. **`substrate/templates/handoff-doc-template.md`** — referenced for D6 (workspace CLAUDE.md template handling, if install.sh modifies CLAUDE.md at all today).

---

## Phase A — Architectural decisions (LOCKED pre-dispatch)

Settled during PRINCIPAL's 2026-05-17 chat declarations. You do NOT surface these as design questions.

### A1. One arc, four phases, one gauntlet — LOCKED

`stoa--ads` is a coherent single work-unit. Single DAEDALUS design covering D1-D6. Single ARGUS audit (HIGH chance of revisions — architecture-sensitive). Single ADA worktree on `arc-29/build`. Verifiers (VERA + CATO + ZENO) each one pass. **CATO is mandatory** — substrate canon work; wording precision matters; future POLYBIUSes read this for life-of-the-substrate.

Phasing:

| Phase | Seat(s) | Output |
|---|---|---|
| 1 | DAEDALUS + ARGUS | `agents/design/arc-29/design.md` — integrated design covering D1 canon sections; D2 convention pick (with Claude Code auto-discovery empirical verification); D3 install.sh scoping changes; D4 check.sh scoping changes; D5 apply.sh scoping changes; D6 CLAUDE.md template handling. ARGUS cold-audits; ADA does not dispatch until ARGUS PASS. |
| 2 | ADA | feature branch `arc-29/build` covering all substrate edits. |
| 3 | VERA + CATO + ZENO | parallel verification pass per Phase B acceptance probes. CATO cold-reads entire diff. ZENO checks spec-vs-result against stoa--ads's 6 deliverables. |
| 4 | PLINY + smoke + ship | smoke beats (per Phase C). PR opened. PLINY runs `gh pr merge` after clean PASS. `stoa--ads` closes. **User-tier POLYBIUS does QA pass at arc-close per PRINCIPAL pattern — PLINY tags `[for: user-tier POLYBIUS]` on stoa--ads.** |

### A2. The architectural model (locked by PRINCIPAL declaration) — LOCKED

PRINCIPAL declared on 2026-05-17:

> "We have the base team of stoa agents at every level. So even a subproject of a subproject would have a base stoa team. Then each level may or may not have customized agents and processes. When we update the stoa agents it should always be safe to update the base agents all the way down but it would be up to the user along with the team of agents to decide whether and how to update custom agents. The cost of creating a new team of custom agents is pretty low so this would be the likely path."

The canon you encode in D1 should carry PRINCIPAL's exact phrasing where load-bearing (block-quote the above + key inline phrases). Same shape as Arc 27's §16.1 PRINCIPAL phrasing block.

Key implications encoded:
- BASE files = always safe to update mechanically (canonical)
- CUSTOM files = operator + team judgment (workspace-owned)
- Cost-of-recreation low → update path is "regenerate custom from new base" not "merge upstream into customized"
- Substrate tools NEVER touch custom paths

### A3. Convention pick — LOCKED with one DAEDALUS empirical-verify sub-decision

**The candidate convention to pick from (subdirectory recommended; DAEDALUS verifies + picks final form):**

| Option | Custom path shape | Pros | Cons |
|---|---|---|---|
| **Subdirectory** (RECOMMENDED) | `.claude/agents/custom/CAPTAIN_<MNEMONIC>_<slug>.md`; `.claude/skills/custom/<skill-name>/`; `.claude/templates/custom/*.md` | Clean visual distinction; easy substrate-tool skip (non-recursive globs); easy to grep / backup separately | **Load-bearing empirical question:** does Claude Code's agent auto-discovery pick up `.claude/agents/custom/CAPTAIN_*.md` files at the subdirectory path? If NO, this option fails. |
| **Filename suffix** | `.claude/agents/CAPTAIN_<MNEMONIC>_<slug>_custom.md`; analogous for skills/templates | Stays at base path; Claude Code discovery unchanged (same dir) | Less visually distinct; tool glob pattern more complex (needs negative match on `_custom`); higher risk of operator typo collision |
| **Top-level custom dir** | `.claude/custom-agents/...` | Cleanest separation in directory listing | Claude Code likely does NOT discover agents outside `.claude/agents/` — REJECTED unless DAEDALUS confirms discovery works |

**DAEDALUS's load-bearing empirical task in Phase 1:** verify Claude Code's agent auto-discovery actually loads agents from `.claude/agents/custom/CAPTAIN_*.md`. If YES → use subdirectory (D2 final pick). If NO → fall back to filename suffix `_custom`. Document the empirical verification in design.md.

The empirical test: drop a stub custom CAPTAIN at the candidate path; invoke a Task/Agent against it by name; verify it activates correctly. Concrete probe — same as VERA probe 5 in Phase B below; DAEDALUS may want to run a smaller version at design time to pick the right convention before locking.

### A4. Files in scope — LOCKED

D1: `substrate/MAJOR_POLYBIUS.md` (new section) + `substrate/operating-disciplines.md` (parallel section).
D2: convention picked + documented in those sections.
D3: `substrate/install.sh` — every glob/path point that touches the agents/skills/templates directories needs base-vs-custom scoping. Add cite-comment at each modification site.
D4: `substrate/skills/check-substrate-updates/check.sh` — same scoping pass.
D5: `substrate/skills/check-substrate-updates/apply.sh` — same scoping pass.
D6: workspace CLAUDE.md handling — DAEDALUS picks whether to extend install.sh's `--modify-claude-md` behavior, add a new section to existing CLAUDE.md files, or document for operator manual-add. Whatever lands, the message is "customize at `<convention-path>`; don't customize at base paths."

### A5. Cite-comment discipline — LOCKED

Wherever D3/D4/D5 scope a path/glob to "base only," place a cite-comment at the modification site referencing the base-vs-custom canon section in MAJOR_POLYBIUS.md / operating-disciplines.md. Same pattern as `apply_substitutions` cite-comment + Arc 26's `parse_skill_names_from_install` cite-comment + Arc 28's bw-output-parse cite-comments. The cite-comment surfaces the discipline at the read site, not at code-review time only.

### A6. Authorship attribution — IMMUTABLE per CLAUDE.md

All edits credit Denson Smith. No exception. Arc 29 doesn't add new substrate files with frontmatter (edits existing canon files + tool scripts). If DAEDALUS surfaces a new skill or template, frontmatter must carry `author: Denson Smith`. Verify before commit.

### A7. Out of scope — HARD LOCKED

Do NOT do in this arc, even if temptation surfaces during build:

- **Migrating any existing customized files** to the new convention. There are none today; no migration needed.
- **Building the railway custom agent team itself.** SEPARATE forthcoming arc at railway_stoa, dispatches AFTER this convention lands.
- **Four-category drift classification** at check.sh (locally-modified × upstream-advanced from stoa--lyh Option Small). With base-vs-custom convention, four-category becomes unnecessary — substrate tools only see base; custom is operator-owned. Do NOT reopen Option Small here.
- **Custom POLYBIUS / PLINY at the MAJOR tier.** Convention applies to CAPTAINs + skills + templates. Whether custom MAJORs make sense is a separate design question; defer.
- **Cross-workspace custom-agent sharing** (e.g., a custom CAPTAIN reused across workspaces). Maybe later; not in this arc.
- **Auto-generated custom-agent templates / scaffolding.** Operator authors custom agents manually (or via agent-author skill); this arc just establishes where they live.
- **Sibling stoa--32b.1 (PRINCIPAL-gate discipline) and stoa--32b.2 (mechanical/agent-split).** Separate future arcs.
- **stoa--3cs (bundled-squash) discipline encoding.** Independent; separate arc.

If you find yourself reaching for any of the above, STOP and surface as substance-disagreement comment on `stoa--ads` (radio-check to user-tier POLYBIUS via [for: user-tier POLYBIUS] tag).

### A8. §15 N=1 honesty — LOCKED

PRINCIPAL declared the architecture today (project-direction authority). Substrate canon enters off-gate. Empirical anchor accretes when the railway_stoa custom team arc dispatches AFTER this convention lands + uses it. If the convention turns out wrong-shaped during the railway build, future arcs revise.

The new canon sections must name this provenance — same shape as Arc 27's §16.6 ("N=1 provenance + accretion path"). Do NOT over-generalize beyond what PRINCIPAL named.

### A9. Pre-branch hygiene — LOCKED

**Before creating `arc-29/build`:** verify local main = origin/main. If local is ahead of origin, surface the ahead-commits + ASK how to proceed (push them first? discard them?). Do NOT silently inherit local-ahead commits into the arc branch — that's the bundled-squash pattern surfaced today as stoa--3cs (filed but not yet built).

User-tier POLYBIUS confirmed at dispatch authoring: local main = origin/main at efffb8b. Should be clean at branch creation time.

---

## Phase B — Verify (probes for VERA)

1. **Custom-file preservation:** drop a stub custom agent at the chosen convention path (per D2); run `install.sh`; verify custom file untouched.
2. **Base-path overwrite (failure-mode demonstration):** drop a stub agent at a BASE path (mimicking the silent-overwrite footgun); run `install.sh`; verify the base-path agent IS overwritten by the substrate base file. This probe demonstrates WHY the convention exists — operator must move custom to the right location.
3. **check.sh scope:** run check.sh against a workspace with customizations at convention path; verify DRIFTED/MISSING/OBSOLETE apply ONLY to base files; custom files not in scope.
4. **apply.sh scope:** run apply.sh --yes against a workspace with customizations; verify custom files unchanged; base files updated as expected.
5. **Load-bearing empirical: Claude Code agent auto-discovery at convention path.** Drop a stub custom CAPTAIN at the chosen path; verify Claude Code finds it (Task/Agent invocation by name works). If subdirectory works → convention final. If not → DAEDALUS already picked filename-suffix fallback per A3.
6. **Cross-consistency:** SPEC.md (or wherever convention documented) + install.sh comment block + MAJOR_POLYBIUS.md section + operating-disciplines.md section ALL consistently describe the convention. No drift between authoritative texts.
7. **Cite-comments present:** grep substrate/install.sh + check-substrate-updates/check.sh + apply.sh for cite-comments at every new scoping site.
8. **CURRENT regression:** check.sh against current registered workspaces still reports CURRENT (the change is internal to substrate tools' input scoping; verdict shape unchanged for workspaces without customizations). the-stoa itself will show DRIFTED on the substrate files this arc edits; that's expected.

CATO cold-reads:
- diff for wording drift, scope creep, cite-comment correctness, cross-reference correctness, output-format coherence
- PRINCIPAL's exact phrasing per A2 — block-quote present + verbatim
- §15 N=1 honesty per A8 — provenance named, no over-generalization
- Authorship discipline per A6 — clean

ZENO checks stoa--ads deliverables D1-D6 each marked DONE by artifact reference.

---

## Phase C — Smoke + ship

PLINY's smoke beats before opening PR:

- `bash -n substrate/install.sh` + `substrate/skills/check-substrate-updates/check.sh` + `apply.sh` — syntax check.
- `grep -n "Base vs custom\|base-vs-custom\|BASE agents\|CUSTOM agents" substrate/MAJOR_POLYBIUS.md substrate/operating-disciplines.md` — new sections present.
- `grep -n "custom" substrate/install.sh substrate/skills/check-substrate-updates/check.sh substrate/skills/check-substrate-updates/apply.sh` — scoping in place; cite-comments visible.
- check.sh against current workspaces (ariadne-core-workspace, railway_stoa, sector-4, the-stoa) — all should still report whatever they reported pre-Arc-29 plus the-stoa showing DRIFTED on the edited substrate files.
- Manual custom-CAPTAIN smoke at chosen convention path — verify discovery works (the load-bearing empirical from A3/B5).

PR title: `Arc 29: base-vs-custom agent convention encoded in substrate canon (operating-disciplines + MAJOR_POLYBIUS + install/check/apply tooling)`
PR body: cross-ref `stoa--ads`, prior Arc 28 (`stoa--s6n`), this directive at `substrate/arcs/arc-29-build-directive.md`, forward-pointer to forthcoming railway_stoa custom team arc.

Merge via `gh pr merge` after clean gauntlet PASS. Close `stoa--ads` with `--reason` referencing the merge commit. Tag `[for: user-tier POLYBIUS]` comment inviting QA pass.

---

## Honest scope reminder

Medium-scope substrate-canon work + tooling. Larger than Arc 27 (one section); comparable to Arc 28 (multi-file substrate touches + tool changes). Full gauntlet expected with likely ARGUS revisions. The load-bearing empirical question (Claude Code agent auto-discovery at convention path) may surface a convention pivot — that's expected, not scope creep. PLINY heads-down ~1-2h wall-clock estimated based on Arc 28 calibration; could be longer if convention pivot happens mid-build.

End directive.
