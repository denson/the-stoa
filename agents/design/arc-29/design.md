# Arc 29 design — Base-vs-custom agent convention encoded in substrate canon

**Ticket:** `stoa--ads`
**Branch:** `arc-29/build`
**Date:** 2026-05-17
**Status:** AWAITING ARGUS cold-audit
**Directive:** `substrate/arcs/arc-29-build-directive.md` (A1–A9 LOCKED)
**Authored by:** CAPTAIN_DAEDALUS_the_stoa, on behalf of the PRINCIPAL (Denson Smith).

---

## §0 — Executive summary

PRINCIPAL declared on 2026-05-17 that every workspace at every nesting level carries a **base stoa team** (deployed from substrate; mechanically updatable) plus optionally **custom agents and processes** (workspace-authored; separately maintained). Today the substrate tools (`install.sh`, `check.sh`, `apply.sh`) assume any file at a base path IS canonical and will overwrite it. The footgun has not bitten yet — no consumer workspace has customized — but the railway_stoa custom team arc is queued to dispatch next and will customize. This arc must ship first so customizations have a canonical home substrate tools respect.

Arc 29 ships six deliverables in one coherent push: D1 adds parallel canon sections (`MAJOR_POLYBIUS.md` §17 + `operating-disciplines.md` §23) that name the architectural model and the per-class convention paths. D2 locks the per-class convention picks — subdirectory for CAPTAINs and templates; **directory-name prefix** for skills (forced by the empirical asymmetry: Claude Code scans `.claude/agents/` recursively but `.claude/skills/` only at one level). D3 scopes `install.sh`'s deploy + staleness-detection loops to base paths only and adds operator-visibility log lines when custom files coexist. D4 scopes `check.sh`'s workspace-side enumeration to base paths only so custom files never appear in DRIFTED/MISSING/OBSOLETE verdicts. D5 hardens `apply.sh` with an explicit refusal at any custom-path target. D6 adds a separate marker-bounded block to the install.sh-managed `CLAUDE.md` append that names the convention paths for the operator.

The load-bearing structural property: the **per-class asymmetry** that PLINY's empirical verification pinned down (Claude Code subagent scan recursive; skill scan single-level; templates have no Claude Code constraint) blocks a uniform subdirectory convention. The design names that asymmetry inline rather than smoothing it, and the cite-comment shape (`u--7yg`-style "cite at the read site") fires at every scoping site so a future maintainer who edits one of the three substrate tools sees the discipline at the read site instead of at code-review time.

§15 N=1 honesty (per `MAJOR_POLYBIUS.md` §15) is named explicitly in both canon sections: PRINCIPAL declared the convention 2026-05-17; substrate canon enters off-gate on that declaration; empirical anchor accretes when railway_stoa builds its custom team using the convention. If the convention turns out wrong-shaped during that build, future arcs revise. Same provenance shape as Arc 27 §16.6 and Arc 28 §22.3.

---

## §1 — Architectural model (the load-bearing frame)

### 1.1 PRINCIPAL's declaration (verbatim, 2026-05-17)

> "We have the base team of stoa agents at every level. So even a subproject of a subproject would have a base stoa team. Then each level may or may not have customized agents and processes. When we update the stoa agents it should always be safe to update the base agents all the way down but it would be up to the user along with the team of agents to decide whether and how to update custom agents. The cost of creating a new team of custom agents is pretty low so this would be the likely path."

### 1.2 The four implications encoded by this arc

1. **BASE files are mechanically updatable by construction.** They live at canonical paths the substrate tools own (`.claude/MAJOR_*.md`, `.claude/agents/CAPTAIN_*.md` at the agents/ root, `.claude/templates/*.md` at the templates/ root, `.claude/skills/<name>/SKILL.md`). `install.sh` deploys them; `check.sh` checks them; `apply.sh` updates them. Overwriting a base file is always safe because the source is canonical.

2. **CUSTOM files are workspace-owned and substrate tools never touch them.** They live at a separate per-class path (D2 below). Re-running `install.sh` does not delete them; `check.sh` does not flag them as DRIFTED or OBSOLETE; `apply.sh` refuses to write them. Their lifecycle is entirely the workspace's stoa team's responsibility.

3. **Cost-of-recreation is low → regenerate-from-new-base is the update path.** When substrate advances and a custom agent wants the new capability, the cheap path is to recreate the custom agent fresh against the new base (operator + team), NOT to attempt a three-way merge of upstream changes into the customization. This is PRINCIPAL's framing on cost, and it removes a class of design problem (drift classification for custom files) by construction.

4. **Substrate tools see only base; custom is operator-owned.** This collapses the four-category drift classification that `stoa--lyh` Option Small punted on (locally-modified × upstream-advanced × per-file-class) into a clean two-category world: substrate manages base, operator manages custom, and the two never overlap on disk because the path convention separates them.

### 1.3 Why this arc precedes railway_stoa

The next planned work IS the railway_stoa team building a custom railway agent set. Without this convention, those custom agents would land at base paths and the next `install.sh --yes` from substrate would delete them silently. The arc must ship before the railway_stoa custom team arc dispatches, otherwise the empirical anchor for the architecture writes itself into a broken state.

---

## §2 — Per-class convention picks (D2 finalized)

### 2.1 The empirical asymmetry (PLINY pre-resolved, web-fetched 2026-05-17 from official Claude Code docs)

Three file classes; three different Claude Code discovery behaviors. The naive single-uniform-convention is not viable. The findings (cited verbatim in the dispatch brief):

| Class | Claude Code behavior | Source |
|---|---|---|
| **Subagents** | `.claude/agents/` and `~/.claude/agents/` scanned **recursively**; identity comes only from YAML `name:` field; subdirectory path does NOT affect identity or invocation; **silent name-collision drops one** | https://code.claude.com/docs/en/sub-agents — "Choose the subagent scope" |
| **Skills** | `.claude/skills/<skill-name>/SKILL.md` — discovery is **single-level only**; skill at `.claude/skills/custom/<name>/SKILL.md` would NOT be discovered (`custom` would itself be the skill name and `<name>/SKILL.md` would not be the entrypoint) | https://code.claude.com/docs/en/skills — "Where skills live" table |
| **Templates** | No Claude Code involvement; pure substrate convention; only substrate tools (`install.sh`, `check.sh`, `apply.sh`) read this directory | n/a — substrate-internal |

### 2.2 The picks

| File class | Custom path convention | Why this shape |
|---|---|---|
| **Custom CAPTAINs** | `.claude/agents/custom/CAPTAIN_<MNEMONIC>_<slug>.md` | Subdirectory works because Claude Code scans `.claude/agents/` recursively. Visual parallelism with base CAPTAINs. Easy to skip from substrate-tool globs (non-recursive `${DEST_AGENTS_DIR}/CAPTAIN_*.md` at the agents/ root will not match files at `custom/CAPTAIN_*.md`). Easy to grep / backup / list. |
| **Custom skills** | `.claude/skills/custom-<skill-name>/SKILL.md` | Subdirectory does NOT work for skills (single-level discovery). The forced fallback is directory-name prefix `custom-`. Substrate tools skip any skill whose dirname starts with `custom-`. Visual cue stays present (operator sees `custom-` in the directory listing). |
| **Custom templates** | `.claude/templates/custom/*.md` | Substrate-internal — no Claude Code constraint. Subdirectory `custom/` matches the CAPTAIN shape for visual parallelism. Substrate tools (only `install.sh`'s staleness scan today touches templates dir) skip the subdirectory cleanly. |

### 2.3 The silent-collision discipline for custom CAPTAINs (load-bearing footgun)

Claude Code identifies subagents by YAML `name:` field, NOT by filename. If a custom CAPTAIN declares `name: CAPTAIN_DAEDALUS` (same as the base), one of the two files is silently dropped from the active roster — no warning. The substrate canon (D1 §3) MUST specify:

- **Custom-agent `name:` fields use a distinct slug suffix.** The convention is `name: CAPTAIN_<MNEMONIC>_<custom-slug>` (e.g., `name: CAPTAIN_DEPLOYER_railway`). The filename mirrors the name for operator legibility. The `<custom-slug>` MUST NOT match the project slug `install.sh` already uses for project-tier base agents (e.g., a workspace named `railway_stoa` already has base `CAPTAIN_DAEDALUS_railway_stoa`; a custom agent at that workspace named `CAPTAIN_DAEDALUS_railway_stoa` would collide).
- **Worked failure-mode example (canon prose):** operator authors `.claude/agents/custom/CAPTAIN_DAEDALUS.md` with frontmatter `name: CAPTAIN_DAEDALUS`. Claude Code's scan finds both this file and `.claude/agents/CAPTAIN_DAEDALUS.md` (base); both declare the same `name:`; one is silently dropped on session start. The custom agent intermittently activates or doesn't, depending on scan order. The operator's mental model — "I added a custom agent and it's not running" — never points at the collision because Claude Code emits no warning. Fix: rename to `CAPTAIN_DAEDALUS_<custom-slug>` in both the filename and the `name:` field.

### 2.4 Rejected alternatives (named for ARGUS's cold-audit context)

- **Filename suffix `_custom`** (`.claude/agents/CAPTAIN_DAEDALUS_custom.md`). Rejected for CAPTAINs because subdirectory works and is cleaner visually; rejected for skills because skill identity is the directory name not a filename (`SKILL.md` is the fixed entrypoint), so a suffix on a file inside the skill dir does nothing. The directory-name prefix `custom-` for skills is the same idea applied at the level where it has effect.
- **Top-level `.claude/custom-agents/`**. Rejected for CAPTAINs because Claude Code only scans `.claude/agents/` — agents outside that path are not discovered.
- **No convention; substrate tools maintain an exclusion-list of base names.** Rejected because the exclusion-list lives in substrate code, not in the workspace; operator who customizes locally has no path-level signal to read. Convention-at-the-path is the more operator-legible mitigation.
- **Subdirectory `.claude/skills/custom/<name>/SKILL.md` despite single-level discovery.** Rejected — the docs are explicit; this path would not be discovered.

---

## §3 — D1 canon section design

### 3.1 `substrate/MAJOR_POLYBIUS.md` — new §17

**Insertion locus:** between current line 962 (end of §16.8 cross-references — last line is `- \`operating-disciplines.md\` §12 (bw cookbook)...`) and current line 963 (the `---` separator before final `Standby, run.` at line 965). New section slots in BEFORE the file's terminator; §16's `Standby, run.` closer moves to be §17's closer (one `Standby, run.` at the end of the file overall).

Numbering: §17 (continues the existing 1-16 numbered run). Title: **"Base vs custom agents"**.

**Rationale for §17 placement (not §1-§3 architectural framing, not nested under §16):** §16 carries "POLYBIUS session lifecycle" (handoff, compaction, decay-not-termination) — adjacent topic ("substrate is a baseline; consumer workspaces evolve") but distinct concern (lifecycle vs. customization). Nesting under §16 would muddy the lifecycle frame. §1-§3 are seat-orientation (who/what/what-not) — too early-in-the-file for an architectural framing the operator may not need on first read; better as a numbered section a reader gets to once seat-orientation is established. §17 sits at the natural extension point of the numbered run; the file's existing `Standby, run.` closer carries it.

**Section prose (verbatim — ADA pastes this; the §15 N=1 provenance block at §17.5 carries today's date 2026-05-17):**

```markdown
## 17. Base vs custom agents

Every workspace at every nesting level carries a BASE stoa team and may optionally carry CUSTOM agents and processes. The two coexist on disk via a per-class path convention; substrate tools manage base; the workspace's stoa team manages custom.

### 17.1 Source-of-truth declaration (2026-05-17, PRINCIPAL)

PRINCIPAL declared the architectural model during the 2026-05-17 substrate-architecture conversation (captured at `stoa--ads` ticket body):

> "We have the base team of stoa agents at every level. So even a subproject of a subproject would have a base stoa team. Then each level may or may not have customized agents and processes. When we update the stoa agents it should always be safe to update the base agents all the way down but it would be up to the user along with the team of agents to decide whether and how to update custom agents. The cost of creating a new team of custom agents is pretty low so this would be the likely path."

Per §15 (N=1 honest-scope discipline) and `operating-disciplines.md` §6.7.1 — substrate canon enters off-gate on PRINCIPAL's project-direction declaration; supporting evidence accretes over time as future workspaces customize against the convention. Do not over-generalize beyond what PRINCIPAL named.

### 17.2 What BASE files are

BASE files are deployed from substrate via `install.sh` and live at canonical paths the substrate tools own. They are always safe to overwrite mechanically because the substrate source is canonical for them.

| Class | Canonical base path |
|---|---|
| MAJORs | `.claude/MAJOR_POLYBIUS*.md`, `.claude/MAJOR_PLINY*.md` (subproject-tier may carry `_<slug>` suffix per `install.sh` convention) |
| Operating disciplines | `.claude/operating-disciplines.md` |
| CAPTAINs | `.claude/agents/CAPTAIN_<MNEMONIC>*.md` (directly under `.claude/agents/`, NOT in any subdirectory) |
| Templates | `.claude/templates/*.md` (directly under `.claude/templates/`, NOT in any subdirectory) |
| Skills | `.claude/skills/<skill-name>/` (where `<skill-name>` does NOT start with `custom-`) |

Substrate tooling — `install.sh`, `check.sh`, `apply.sh` — scopes its globs to these paths. The cite-comment at every scoping site references this section.

### 17.3 What CUSTOM files are

CUSTOM files are authored by the workspace's stoa team (operator + agents). Substrate tools never touch them. Their lifecycle, naming, content, and discipline are owned by the workspace.

| Class | Custom path convention |
|---|---|
| Custom CAPTAINs | `.claude/agents/custom/CAPTAIN_<MNEMONIC>_<custom-slug>.md` |
| Custom skills | `.claude/skills/custom-<skill-name>/SKILL.md` |
| Custom templates | `.claude/templates/custom/*.md` |

The asymmetry (subdirectory for CAPTAINs and templates; directory-name prefix for skills) is forced by Claude Code's discovery behavior. CAPTAIN discovery is recursive (`.claude/agents/` scanned recursively per https://code.claude.com/docs/en/sub-agents); skill discovery is single-level (`.claude/skills/<name>/SKILL.md` only — `.claude/skills/custom/<name>/SKILL.md` would not be discovered, because `custom` would itself be the skill name). Templates have no Claude Code involvement and follow the CAPTAIN shape for visual parallelism.

### 17.4 Custom CAPTAIN name discipline (silent-collision footgun)

Claude Code identifies subagents by their YAML `name:` frontmatter field, NOT by filename. When two subagents within one scope (either `.claude/agents/` or `~/.claude/agents/`) declare the same `name:`, Claude Code silently keeps one and discards the other without warning.

**The convention:** custom CAPTAIN `name:` fields MUST be distinct from base CAPTAIN names. Use a slug suffix:

- Filename: `.claude/agents/custom/CAPTAIN_DEPLOYER_railway.md`
- Frontmatter: `name: CAPTAIN_DEPLOYER_railway`

For workspaces deployed at project tier (where base CAPTAINs already carry a project-slug suffix like `CAPTAIN_DAEDALUS_railway_stoa`), the custom-slug MUST be distinct from the project slug. A custom `CAPTAIN_DAEDALUS_railway_stoa` at workspace `railway_stoa` would collide with the base.

**Worked failure-mode example.** Operator authors `.claude/agents/custom/CAPTAIN_DAEDALUS.md` with frontmatter `name: CAPTAIN_DAEDALUS` at a user-tier deployment. The base `.claude/agents/CAPTAIN_DAEDALUS.md` also declares `name: CAPTAIN_DAEDALUS`. On session start, Claude Code scans both, finds two subagents with the same name, and silently drops one. The custom agent intermittently activates or doesn't, depending on scan order. The operator's mental model — "I added a custom agent and it's not running" — never points at the collision because no warning is emitted. The fix: rename to `CAPTAIN_DAEDALUS_<distinct-slug>` in both the filename AND the `name:` field.

**Casing note (docs-vs-empirical divergence).** Claude Code's published docs (https://code.claude.com/docs/en/sub-agents — "Supported frontmatter fields") describe the `name:` field as "lowercase letters and hyphens." The substrate's base CAPTAINs use uppercase + underscore (`CAPTAIN_DAEDALUS`, `CAPTAIN_ARGUS`, etc., with the workspace-slug suffix appended at install time) and have worked in production across all Arcs 1–28. Custom CAPTAINs should match the BASE convention (uppercase + underscore, with the workspace-slug suffix) rather than the docs-literal lowercase-and-hyphens form, so the name space remains visually parallel and the silent-collision discipline above operates against a single naming shape rather than two. The divergence from docs is empirical, not theoretical; if a future Claude Code release tightens the parser to reject non-lowercase names, this convention rotates and substrate seats need rename. The cross-reference for the convention table is `operating-disciplines.md` §23 below.

### 17.5 N=1 provenance + accretion path

Per §15 honest-scope: PRINCIPAL declared this discipline 2026-05-17 (project-direction authority, captured at `stoa--ads` thread). §15 defers to `operating-disciplines.md` §6.7.1 as the canon-promotion gate (multiple observations + controlled comparison + substrate-level pattern); §15 does not carve out a separate "PRINCIPAL-declaration shortcut." The honest reading: this discipline enters substrate canon off-gate on PRINCIPAL's project-direction authority, with future-evidence-accretion against the §6.7.1 gate still required for promotion to "structural lesson" status. Substrate canon goes in now because PRINCIPAL named it; structural-lesson confidence accretes over future workspace customizations.

The supporting evidence at the time of this writing:

- PLINY's 2026-05-17 empirical verification of Claude Code auto-discovery behavior (web-fetched against https://code.claude.com/docs/en/sub-agents and https://code.claude.com/docs/en/skills) — the source-of-truth for the per-class asymmetry that shapes the convention.
- Arc 29 (`stoa--ads`) ticket body — carries PRINCIPAL's 2026-05-17 declaration verbatim and the deliverable list this section encodes.
- The forthcoming railway_stoa custom team arc — empirical anchor; dispatches AFTER this convention lands; the first real workload exercising the per-class convention.

The convention is in NOW because PRINCIPAL named it today; promotion to "structural lesson" status with multi-workspace empirical backing is a future arc's work, not this one's. If the convention turns out wrong-shaped during the railway_stoa build (e.g., the directory-name prefix `custom-` for skills creates a confusion the subdirectory shape would not have, or the silent-collision discipline misses a case), future arcs revise this section. Same N=1 framing as Arc 27's §16.6 and Arc 28's `operating-disciplines.md` §22.3.

### 17.6 Cross-references

- `operating-disciplines.md` §23 (Base vs custom — universal-team framing) — the team-wide cut of this discipline; every seat reads that section, this one is POLYBIUS-specific.
- `MAJOR_POLYBIUS.md` §14 (substrate-update check) — the daily-cadence mechanism is what catches drift on BASE files; the check by construction does not flag CUSTOM files.
- `MAJOR_POLYBIUS.md` §15 (N=1 honest-scope) — the gate this section's claims pass through.
- `substrate/install.sh`, `substrate/skills/check-substrate-updates/check.sh`, `substrate/skills/check-substrate-updates/apply.sh` — the three substrate tools that scope-to-base via cite-comments referencing this section.
- `stoa--ads` (this arc's ticket); forthcoming railway_stoa custom team arc (empirical anchor).
```

### 3.2 `substrate/operating-disciplines.md` — new §23

**Insertion locus:** between current line 1029 (end of §22.5 cross-references — last line is `- \`substrate/skills/check-bw-release/SKILL.md\` — Step 1 operationalization.`) and current line 1030 (the `---` separator before the `Agent-regime inverses` block at line 1032). The numbered-disciplines run §1-§22 today; §23 extends the run; the `Agent-regime inverses` + `Empirical lineage` blocks stay at file tail intact.

Numbering: §23. Title: **"Base vs custom agents (universal-team framing)"**.

**Section prose (verbatim — ADA pastes this; the §15 N=1 provenance block at §23.4 mirrors POLYBIUS §17.5):**

```markdown
## 23. Base vs custom agents (universal-team framing)

Every workspace at every nesting level carries a BASE stoa team (deployed from substrate; mechanically updatable via `install.sh` / `apply.sh`) and may optionally carry CUSTOM agents and processes (workspace-authored; substrate tools never touch them). Every seat reads this section; it carries the universal-team framing. `MAJOR_POLYBIUS.md` §17 carries the POLYBIUS-specific refinement (custom-CAPTAIN authoring discipline, name-collision footgun, daily-cadence implications).

### 23.1 Source-of-truth declaration (2026-05-17, PRINCIPAL)

PRINCIPAL declared the architectural model during the 2026-05-17 substrate-architecture conversation (captured at `stoa--ads` ticket body):

> "We have the base team of stoa agents at every level. So even a subproject of a subproject would have a base stoa team. Then each level may or may not have customized agents and processes. When we update the stoa agents it should always be safe to update the base agents all the way down but it would be up to the user along with the team of agents to decide whether and how to update custom agents. The cost of creating a new team of custom agents is pretty low so this would be the likely path."

### 23.2 The per-class path convention

| Class | Base path (substrate tools manage) | Custom path (workspace owns) |
|---|---|---|
| MAJORs | `.claude/MAJOR_POLYBIUS*.md`, `.claude/MAJOR_PLINY*.md` | (custom MAJORs out of scope for Arc 29; future arc) |
| Operating disciplines | `.claude/operating-disciplines.md` | (n/a) |
| CAPTAINs | `.claude/agents/CAPTAIN_*.md` (directly under agents/) | `.claude/agents/custom/CAPTAIN_<MNEMONIC>_<slug>.md` |
| Templates | `.claude/templates/*.md` (directly under templates/) | `.claude/templates/custom/*.md` |
| Skills | `.claude/skills/<name>/` (where `<name>` does NOT start with `custom-`) | `.claude/skills/custom-<name>/SKILL.md` |

The asymmetry (subdirectory for CAPTAINs and templates; directory-name prefix for skills) is forced by Claude Code's discovery behavior:

- **CAPTAINs:** `.claude/agents/` is scanned **recursively** (https://code.claude.com/docs/en/sub-agents); subdirectory works.
- **Skills:** `.claude/skills/<skill-name>/SKILL.md` is **single-level** (https://code.claude.com/docs/en/skills); subdirectory would not be discovered.
- **Templates:** no Claude Code involvement; substrate-internal convention; follows CAPTAIN shape for visual parallelism.

### 23.3 The discipline, by seat

- **POLYBIUS:** reads this section + `MAJOR_POLYBIUS.md` §17. When the team customizes, authors land at the custom paths above. When substrate advances and a custom agent wants new behavior, the typical update path is regenerate-fresh-from-new-base (per PRINCIPAL's cost framing) rather than merge-upstream-into-customization.
- **PLINY:** dispatches CAPTAINs by `name:` field; never assumes a filename. When a custom CAPTAIN exists, dispatching it is identical to dispatching a base CAPTAIN — the path the file lives at is irrelevant to invocation. PLINY's dispatch envelopes name the CAPTAIN by mnemonic + slug (e.g., `CAPTAIN_DEPLOYER_railway`).
- **Every CAPTAIN:** when designing, executing, or verifying, the seat reads the workspace's actual files (base + custom) as the operational truth. The substrate-tool scoping (D3/D4/D5 below) governs what `install.sh` / `check.sh` / `apply.sh` see, NOT what the running team sees. Custom agents and base agents both run.
- **Authoring custom files:** the workspace's stoa team authors them via standard agent-author skill or by hand. Substrate tools NEVER create or modify them. There is no `install.sh --with-custom` flag and no auto-generated custom scaffolding (out of scope per Arc 29 A7).

### 23.4 N=1 provenance + accretion path

Per §6.7.1 honest-scope: PRINCIPAL declared this discipline 2026-05-17 (project-direction authority, captured at `stoa--ads` thread). §6.7.1 defers to the canon-promotion gate (multiple observations + controlled comparison + substrate-level pattern); §6.7.1 does not carve out a separate "PRINCIPAL-declaration shortcut." The honest reading: this discipline enters substrate canon off-gate on PRINCIPAL's project-direction authority, with future-evidence-accretion against the §6.7.1 gate still required for promotion to "structural lesson" status.

The supporting evidence at the time of this writing:

- PLINY's 2026-05-17 empirical verification of Claude Code auto-discovery behavior (web-fetched against https://code.claude.com/docs/en/sub-agents and https://code.claude.com/docs/en/skills) — the source-of-truth for the per-class asymmetry the convention encodes.
- Arc 29 (`stoa--ads`) ticket body — carries PRINCIPAL's 2026-05-17 declaration verbatim.
- The forthcoming railway_stoa custom team arc — empirical anchor; the first real workload exercising the per-class convention; dispatches AFTER this arc lands.

The convention is in NOW because PRINCIPAL named it today; structural-lesson confidence accretes over future workspace customizations. If the convention turns out wrong-shaped during the railway_stoa build, future arcs revise this section. Same N=1 framing as Arc 27's `MAJOR_POLYBIUS.md` §16.6 and Arc 28's §22.3.

### 23.5 Cross-references

- `MAJOR_POLYBIUS.md` §17 (Base vs custom — POLYBIUS-specific refinement, including the silent-collision footgun for custom CAPTAIN authoring).
- §6.7.1 (the N=1 canon-promotion gate this section enters off-gate on PRINCIPAL declaration).
- §8.1 (positive references only) — the authoring discipline this section follows: it names "customize at `<custom-path>`" rather than "don't customize at `<base-path>`."
- §8.2 (scaffolding and guardrails) — this section pre-resolves the per-class convention picks and names the silent-collision failure mode as a worked example, per the scaffolding discipline.
- `substrate/install.sh`, `substrate/skills/check-substrate-updates/check.sh`, `substrate/skills/check-substrate-updates/apply.sh` — the three substrate tools whose scoping-to-base is governed by this section; cite-comments at every scoping site reference this section AND the POLYBIUS §17 sibling.
- `stoa--ads` (this arc); forthcoming railway_stoa custom team arc (empirical anchor).
```

---

## §4 — D3 install.sh modifications

`install.sh` already mostly scopes correctly to base — the CAPTAIN deploy loop iterates `CAPTAIN_NAMES` and writes only to `${DEST_AGENTS_DIR}/CAPTAIN_<NAME>${NAME_SUFFIX}.md` at the agents/ root (not in any subdirectory); templates and skills similarly iterate hardcoded arrays. The work in D3 is in TWO places: (a) the staleness-detection loops (the `obsolete_files[]` scans at lines 781-838) glob ALL files at the destination dirs and would currently flag custom files as obsolete; (b) operator-visibility log lines that surface "custom files coexist at <path>; not touched" when a base file is being deployed and a sibling custom directory has content.

### 4.1 Scoping sites + changes

**Site 1: CAPTAIN staleness scan (install.sh:783-801)**

Current loop: `for f in "${DEST_AGENTS_DIR}/CAPTAIN_"*"${NAME_SUFFIX}.md"; do` — globs the agents/ root for CAPTAIN_*.md files. Per the docs (recursive scan + identity-by-name), this glob already does NOT match files at `${DEST_AGENTS_DIR}/custom/CAPTAIN_*.md` because the `*` is a single path-segment glob, not recursive. **No code change needed for correctness**; the existing glob is naturally base-scoped. Add a cite-comment naming the discipline so a future maintainer who "improves" the glob to recursive (e.g., `**/CAPTAIN_*.md`) sees the discipline at the read site.

Change shape (insert as comment block immediately before line 783):

```bash
  # CITE: this glob is single-path-segment (NOT recursive) — it matches
  # CAPTAIN_*.md files directly under ${DEST_AGENTS_DIR} but NOT files at
  # ${DEST_AGENTS_DIR}/custom/CAPTAIN_*.md. That non-recursion IS the base-vs-
  # custom scoping; see substrate/operating-disciplines.md §23 + substrate/
  # MAJOR_POLYBIUS.md §17. If a future change makes this glob recursive
  # (e.g., to find sub-directory CAPTAINs for some other reason), the
  # base-vs-custom invariant breaks — custom CAPTAINs would be classified
  # as obsolete and pruned by --prune-obsolete. The discipline is at the
  # path-shape level: substrate tools see only base; custom is operator-owned.
```

**Site 2: templates staleness scan (install.sh:803-820)**

Current loop: `for f in "${DEST_TEMPLATES_DIR}"/*; do` then `[ -f "$f" ] || continue` — globs all files directly under templates/. Same property: not recursive; `custom/` subdirectory entries are directories (not files), so the `[ -f "$f" ] || continue` filter skips them. **Correct by construction**; add the cite-comment for the same reason as Site 1.

Change shape (insert as comment block immediately before line 803):

```bash
  # CITE: this glob is single-path-segment + file-only (the `[ -f "$f" ]`
  # filter skips directories). It does NOT recurse into
  # ${DEST_TEMPLATES_DIR}/custom/, where custom templates live per the
  # base-vs-custom convention (substrate/operating-disciplines.md §23 +
  # substrate/MAJOR_POLYBIUS.md §17). If a future change makes this glob
  # recursive, custom templates would be flagged as obsolete; the discipline
  # is at the path-shape level.
```

**Site 3: skills staleness scan (install.sh:822-838)**

Current loop: `for d in "${DEST_SKILLS_DIR}"/*/; do` then `base=$(basename "$d")` — globs subdirectories directly under skills/, then matches `base` against `SKILL_NAMES[]`. **This is the load-bearing scoping site for D3** because the convention for skills is **directory-name prefix** `custom-`, not subdirectory. Any directory under `.claude/skills/` whose name starts with `custom-` would currently be flagged as obsolete (not in `SKILL_NAMES`) and removed by `--prune-obsolete`.

Change shape (replace the loop body at line 824-836):

```bash
  for d in "${DEST_SKILLS_DIR}"/*/; do
    base=$(basename "$d")
    # CITE: skip workspace-owned custom skills per the base-vs-custom convention.
    # Claude Code skill discovery is single-level (.claude/skills/<name>/SKILL.md);
    # custom skills use directory-name prefix `custom-` (substrate/operating-
    # disciplines.md §23 + substrate/MAJOR_POLYBIUS.md §17). Substrate tools
    # never touch custom paths. If this prefix-check is removed, every custom
    # skill in the workspace would be classified as obsolete and pruned by
    # --prune-obsolete — the silent-overwrite footgun this convention exists
    # to prevent.
    case "$base" in
      custom-*) continue ;;
    esac
    found=0
    for s in "${SKILL_NAMES[@]}"; do
      if [ "$s" = "$base" ]; then
        found=1
        break
      fi
    done
    if [ "$found" -eq 0 ]; then
      obsolete_files+=("${d%/}")
    fi
  done
```

**Site 4: NEW operator-visibility check (after staleness scan, before line 870 final summary)**

Add a read-only scan that surfaces (informationally) what custom files coexist. Logging only; no behavior change. Operator sees "custom files coexist; not touched" as positive confirmation the convention is working.

Change shape (insert after line 868 `fi` of the obsolete-files block, before line 870 `echo`):

```bash
# Operator visibility: surface custom files that coexist at the convention
# paths. Read-only; substrate tools never touch these. The discipline is at
# substrate/operating-disciplines.md §23 + substrate/MAJOR_POLYBIUS.md §17.
# Surfacing the count tells the operator "the convention is working —
# substrate updates left your customizations alone." Silence here would
# leave the operator wondering whether the convention is in effect.
#
# Gating: CAPTAIN/template count blocks gate on WITH_CAPTAINS / WITH_TEMPLATES
# respectively, mirroring the existing CAPTAIN-staleness-scan gate at
# install.sh:783 and the templates-staleness-scan gate at install.sh:803.
# Skills count is always-print: there is no --no-skills deploy flag, so no
# corresponding gate exists upstream. The shape preserves "opt-out means
# substrate stays silent" for the operator who passed --no-captains or
# --no-templates — they get no count line for the class they opted out of.
custom_captain_count=0
custom_template_count=0
custom_skill_count=0
if [ "$WITH_CAPTAINS" -eq 1 ] && [ -d "${DEST_AGENTS_DIR}/custom" ]; then
  shopt -s nullglob
  for f in "${DEST_AGENTS_DIR}/custom/CAPTAIN_"*.md; do
    custom_captain_count=$((custom_captain_count + 1))
  done
  shopt -u nullglob
fi
if [ "$WITH_TEMPLATES" -eq 1 ] && [ -n "${DEST_TEMPLATES_DIR:-}" ] && [ -d "${DEST_TEMPLATES_DIR}/custom" ]; then
  shopt -s nullglob
  for f in "${DEST_TEMPLATES_DIR}/custom/"*; do
    [ -f "$f" ] || continue
    custom_template_count=$((custom_template_count + 1))
  done
  shopt -u nullglob
fi
if [ -d "$DEST_SKILLS_DIR" ]; then
  shopt -s nullglob
  for d in "${DEST_SKILLS_DIR}/custom-"*/; do
    custom_skill_count=$((custom_skill_count + 1))
  done
  shopt -u nullglob
fi
total_custom=$((custom_captain_count + custom_template_count + custom_skill_count))
if [ "$total_custom" -gt 0 ]; then
  echo
  echo "Custom files coexist at convention paths (not touched by substrate):"
  [ "$custom_captain_count"  -gt 0 ] && echo "  - ${custom_captain_count}  custom CAPTAIN(s) at ${DEST_AGENTS_DIR}/custom/"
  [ "$custom_template_count" -gt 0 ] && echo "  - ${custom_template_count} custom template(s) at ${DEST_TEMPLATES_DIR}/custom/"
  [ "$custom_skill_count"    -gt 0 ] && echo "  - ${custom_skill_count}  custom skill(s) at ${DEST_SKILLS_DIR}/custom-*/"
fi
```

**Gating rationale (resolved from §10.7 Q2; ARGUS Finding 3).** The CAPTAIN count block gates on `WITH_CAPTAINS` and the templates count block gates on `WITH_TEMPLATES`; this matches the existing CAPTAIN/template staleness-scan gating at install.sh:783 + :803, preserves the "opt-out means substrate stays silent" shape, and prevents the asymmetry where an operator running with `--no-captains` would still see CAPTAIN-custom-count output. Always-print (vs `--verbose` gating) is sustained: operator confidence in "the convention is working" is the design intent for the visibility block; gating it behind `--verbose` would defeat the purpose. Skills count remains always-print because there is no `--no-skills` flag to mirror.

### 4.2 D3 probe spec (ADA validates after applying the change)

```bash
# Smoke 1: existing globs do not match custom paths (regression baseline).
bash -n substrate/install.sh  # syntax check

# Smoke 2: with a stub custom CAPTAIN at the convention path, install.sh does
# not flag it as obsolete and does not delete it.
SYNTHETIC_PARENT="$(mktemp -d)"
SYNTHETIC_PROJECT="${SYNTHETIC_PARENT}/probe_project"
mkdir -p "$SYNTHETIC_PROJECT"
bash substrate/install.sh --target project --project-dir "$SYNTHETIC_PROJECT"
mkdir -p "${SYNTHETIC_PROJECT}/.claude/agents/custom"
echo "---
name: CAPTAIN_PROBE_custom
---
stub" > "${SYNTHETIC_PROJECT}/.claude/agents/custom/CAPTAIN_PROBE_custom.md"
mkdir -p "${SYNTHETIC_PROJECT}/.claude/skills/custom-probe"
echo "stub" > "${SYNTHETIC_PROJECT}/.claude/skills/custom-probe/SKILL.md"
mkdir -p "${SYNTHETIC_PROJECT}/.claude/templates/custom"
echo "stub" > "${SYNTHETIC_PROJECT}/.claude/templates/custom/probe.md"

# Re-install; assert custom files still present + operator-visibility line printed.
output="$(bash substrate/install.sh --target project --project-dir "$SYNTHETIC_PROJECT" 2>&1)"
[ -f "${SYNTHETIC_PROJECT}/.claude/agents/custom/CAPTAIN_PROBE_custom.md" ] || { echo "FAIL: custom CAPTAIN deleted"; exit 1; }
[ -f "${SYNTHETIC_PROJECT}/.claude/skills/custom-probe/SKILL.md" ]           || { echo "FAIL: custom skill deleted"; exit 1; }
[ -f "${SYNTHETIC_PROJECT}/.claude/templates/custom/probe.md" ]              || { echo "FAIL: custom template deleted"; exit 1; }
echo "$output" | grep -q "Custom files coexist at convention paths"          || { echo "FAIL: operator-visibility line missing"; exit 1; }

# Smoke 3: --prune-obsolete does NOT remove custom files (load-bearing).
bash substrate/install.sh --target project --project-dir "$SYNTHETIC_PROJECT" --prune-obsolete
[ -f "${SYNTHETIC_PROJECT}/.claude/agents/custom/CAPTAIN_PROBE_custom.md" ] || { echo "FAIL: --prune-obsolete deleted custom CAPTAIN"; exit 1; }
[ -f "${SYNTHETIC_PROJECT}/.claude/skills/custom-probe/SKILL.md" ]           || { echo "FAIL: --prune-obsolete deleted custom skill"; exit 1; }
[ -f "${SYNTHETIC_PROJECT}/.claude/templates/custom/probe.md" ]              || { echo "FAIL: --prune-obsolete deleted custom template"; exit 1; }
rm -rf "$SYNTHETIC_PARENT"
echo "D3 smoke PASS"
```

### 4.3 D3 cite-comment grep verification

```bash
grep -c "base-vs-custom convention" substrate/install.sh  # expect >= 3 (Sites 1, 2, 3)
grep -n "operating-disciplines.md §23"     substrate/install.sh  # expect >= 3
grep -n "MAJOR_POLYBIUS.md §17"            substrate/install.sh  # expect >= 3
grep -n "case .base. in"                   substrate/install.sh | grep "custom-"  # expect 1 (Site 3 skill skip)
```

---

## §5 — D4 check.sh modifications

`check.sh` has TWO enumeration functions: `enumerate_deployed()` (lines ~298-354) emits the source-side ground truth (what substrate ships); `enumerate_workspace_substrate_paths()` (lines ~377-425) emits the workspace-side scan for OBSOLETE detection. The source-side enumeration is already scoped by construction (it globs `${SUBSTRATE_DIR}/CAPTAIN_*.md` and only emits paths at the base path shape) — no change needed there. The work is in `enumerate_workspace_substrate_paths()`, where the workspace-side globs would currently pick up custom files and flag them as OBSOLETE.

### 5.1 Scoping sites + changes

**Site 1: workspace CAPTAINs glob (check.sh:400-404)**

Current loop:
```bash
  if [ -d "${ws}/.claude/agents" ]; then
    for f in "${ws}/.claude/agents/CAPTAIN_"*.md; do
      echo ".claude/agents/$(basename "$f")"
    done
  fi
```

Same property as install.sh Site 1: single-path-segment glob; `custom/` subdirectory not matched. **Correct by construction**; add the cite-comment.

Change shape (insert comment immediately before line 400, inside the `if [ -d "${ws}/.claude/agents" ]`):

```bash
  if [ -d "${ws}/.claude/agents" ]; then
    # CITE: this glob is single-path-segment (NOT recursive). It matches
    # CAPTAIN_*.md directly under .claude/agents/ but NOT files at
    # .claude/agents/custom/CAPTAIN_*.md (the custom convention path per
    # substrate/operating-disciplines.md §23 + substrate/MAJOR_POLYBIUS.md §17).
    # That non-recursion IS the base-vs-custom scoping for OBSOLETE detection.
    # If this glob is made recursive, custom CAPTAINs would surface as OBSOLETE
    # and the operator would be routed to --prune-obsolete (which D3 already
    # scopes to base, so no actual deletion would occur — but the false OBSOLETE
    # flag would mislead). The discipline is path-shape, defense at every read site.
    for f in "${ws}/.claude/agents/CAPTAIN_"*.md; do
      echo ".claude/agents/$(basename "$f")"
    done
  fi
```

**Site 2: workspace templates glob (check.sh:406-412)**

Current loop globs `${ws}/.claude/templates/*` with the `[ -f "$f" ] || continue` filter. Same property; correct by construction. Add cite-comment:

```bash
  if [ -d "${ws}/.claude/templates" ]; then
    # CITE: single-path-segment + file-only glob (the `[ -f ]` filter skips
    # directories, including .claude/templates/custom/ where custom templates
    # live per the base-vs-custom convention — substrate/operating-disciplines.md
    # §23 + substrate/MAJOR_POLYBIUS.md §17). If a future change recurses or
    # removes the file-only filter, custom templates would be flagged as OBSOLETE.
    for f in "${ws}/.claude/templates/"*; do
      [ -f "$f" ] || continue
      echo ".claude/templates/$(basename "$f")"
    done
  fi
```

**Site 3: workspace skills glob (check.sh:415-419) — load-bearing**

Current loop: `for d in "${ws}/.claude/skills/"*/; do echo ".claude/skills/$(basename "$d")/"; done`. Globs ALL skill subdirectories. **This is the load-bearing scoping site for D4** because custom skills use directory-name prefix `custom-`; without filtering, every custom skill in the workspace would be flagged as OBSOLETE on every check.

Change shape (replace lines 415-419):

```bash
  if [ -d "${ws}/.claude/skills" ]; then
    # CITE: skip workspace-owned custom skills per the base-vs-custom convention.
    # Custom skills use directory-name prefix `custom-` (forced by Claude Code's
    # single-level skill discovery — substrate/operating-disciplines.md §23 +
    # substrate/MAJOR_POLYBIUS.md §17). Substrate tools never see custom paths.
    # Without this case-skip, every custom skill in the workspace would be
    # classified as OBSOLETE on every check.sh run, polluting the verdict and
    # routing the operator to --prune-obsolete (which D3 also scopes correctly,
    # so no deletion — but the false OBSOLETE noise is the bug).
    local d base
    for d in "${ws}/.claude/skills/"*/; do
      base="$(basename "$d")"
      case "$base" in
        custom-*) continue ;;
      esac
      echo ".claude/skills/${base}/"
    done
  fi
```

(The existing code declares `local d` at line 416; the design extends that declaration to `local d base` so the new `base` variable is symmetric with `d`. **ADA:** declare `local base` for consistency with the `local d` declaration above — under process substitution the leak surface is zero, but the shellcheck-clean shape ships. Combined one-line declaration `local d base` is the minimal-diff form.)

**Site 4 (forward-looking cite at check.sh:392 — MAJOR glob)**

The workspace MAJORs glob at `check.sh:392` is single-path-segment by construction (same shape as the CAPTAIN glob at Site 1) and is therefore naturally safe against any future `.claude/agents/custom/MAJOR_*.md` files. Sites 1, 2, and 3 above all carry cite-comments naming the base-vs-custom discipline; leaving the MAJOR site silent would create a 1-of-4-sites gap a future maintainer would have to re-discover. **Custom MAJORs at POLYBIUS/PLINY tier are A7-hard-locked out of Arc 29** (per §10.2 + §10.5; deferred to a future arc that explicitly designs around the orchestrator-tier coordination implications), so no scoping change is needed here — the existing glob is correct by construction. The defensive cite-comment ships only to keep the read-site discipline complete.

Change shape: **no functional change** at check.sh:392. **ADA adds the following cite-comment only**, immediately before the existing MAJOR loop:

```bash
  # CITE: MAJOR glob is single-path-segment by design — matches MAJOR_*.md
  # directly under .claude/agents/ but NOT files at .claude/agents/custom/
  # MAJOR_*.md. Custom MAJORs are OUT OF SCOPE per Arc 29 A7 hard-lock
  # (operating-disciplines.md §23 + MAJOR_POLYBIUS.md §17 base-vs-custom
  # convention applies to CAPTAINs + skills + templates only; the POLYBIUS/
  # PLINY orchestrator tier is deferred to a future arc). If a future arc
  # adds custom MAJOR support, this glob site needs the same case-skip
  # treatment as the CAPTAIN site at line 400 (the .claude/agents/custom/
  # subdirectory convention). The cite is forward-looking; the glob itself
  # is correct as written and needs no change in this arc.
```

The grep verification in §5.3 should expect `>= 4` (one cite per Site) rather than `>= 3` after this addition; see §5.3 update below.

### 5.2 D4 probe spec

```bash
# Smoke 1: syntax check.
bash -n substrate/skills/check-substrate-updates/check.sh

# Smoke 2: against a workspace with custom files, check.sh does not flag them as OBSOLETE.
# Use the synthetic parent from §4.2 D3 probe (already has custom files seeded).
output="$(bash substrate/skills/check-substrate-updates/check.sh --workspace "$SYNTHETIC_PROJECT" 2>&1)"
echo "$output" | grep -E "OBSOLETE|custom"  # should NOT show custom paths in OBSOLETE block
echo "$output" | grep "custom/CAPTAIN_PROBE_custom" && { echo "FAIL: custom CAPTAIN in check.sh output"; exit 1; }
echo "$output" | grep "skills/custom-probe"        && { echo "FAIL: custom skill in check.sh output"; exit 1; }
echo "$output" | grep "templates/custom/probe"     && { echo "FAIL: custom template in check.sh output"; exit 1; }
echo "D4 smoke PASS"

# Smoke 3: the-stoa workspace itself shows CURRENT (no false positives from
# the convention change against a workspace with no customizations).
bash substrate/skills/check-substrate-updates/check.sh --workspace . 2>&1 | grep "CURRENT\|DRIFTED"
```

### 5.3 D4 cite-comment grep verification

```bash
grep -c "base-vs-custom convention" substrate/skills/check-substrate-updates/check.sh  # expect >= 4 (Sites 1, 2, 3 + Site 4 forward-looking MAJOR cite)
grep -n "operating-disciplines.md §23"     substrate/skills/check-substrate-updates/check.sh  # expect >= 4
grep -n "MAJOR_POLYBIUS.md §17"            substrate/skills/check-substrate-updates/check.sh  # expect >= 4
```

---

## §6 — D5 apply.sh modifications

`apply.sh` reads file paths via `--files` (operator passes a path), via `--all-differing` (harvested from `check.sh` DRIFTED block), and resolves each through `source_path_for_deployed()` which returns empty for unknown paths (apply then skips). After D4, `check.sh` output never contains custom paths, so the `--all-differing` path is naturally safe. The `--files` direct path could still be operator-passed for any path. The discipline: **apply.sh refuses any path under a custom convention prefix with an explicit error**, surfacing the discipline at the rejection site rather than silently skipping (which would let the operator believe their intent was honored).

### 6.1 Scoping sites + changes

**Site 1: explicit refusal at the per-file walk (apply.sh:278-289, top of the for-loop)**

Current loop opens with:
```bash
for dep in "${FILES[@]}"; do
  src_rel="$(source_path_for_deployed "$dep" "$TIER" "$SLUG")"
  if [ -z "$src_rel" ]; then
    echo "apply.sh: skipping (not a substrate-derived path): $dep"
    continue
  fi
```

Add an EXPLICIT refusal BEFORE the source-path lookup, with a friendly error message. Refusal (not skip) because the operator's intent — "apply this file" — is mismatched against the convention; silent skip would mislead.

Change shape (replace lines 278-282 with this expanded prelude):

```bash
for dep in "${FILES[@]}"; do
  # CITE: explicit refusal at custom-convention paths. Substrate tools never
  # touch custom files (substrate/operating-disciplines.md §23 + substrate/
  # MAJOR_POLYBIUS.md §17). check.sh's --all-differing harvester already
  # filters these out (D4); this guard catches the direct --files <path>
  # surface where an operator could pass a custom path explicitly. Refusal
  # (not skip) because the operator's stated intent — "apply this file" —
  # is mismatched against the convention; a silent skip would mislead.
  case "$dep" in
    .claude/agents/custom/*|\
    .claude/skills/custom-*|\
    .claude/templates/custom/*)
      echo "apply.sh: refusing to apply to custom-path file (substrate tools never touch custom — see substrate/operating-disciplines.md §23): $dep" >&2
      continue
      ;;
  esac
  src_rel="$(source_path_for_deployed "$dep" "$TIER" "$SLUG")"
  if [ -z "$src_rel" ]; then
    echo "apply.sh: skipping (not a substrate-derived path): $dep"
    continue
  fi
```

The case pattern matches `.claude/agents/custom/anything`, `.claude/skills/custom-anything`, and `.claude/templates/custom/anything`. The trailing `*` after `custom-` covers any skill name following the prefix; the `*` after `custom/` covers any file or sub-path.

### 6.2 D5 probe spec

```bash
# Smoke 1: syntax check.
bash -n substrate/skills/check-substrate-updates/apply.sh

# Smoke 2: --files against a custom path REFUSES (does not silently skip).
output="$(bash substrate/skills/check-substrate-updates/apply.sh \
  --workspace "$SYNTHETIC_PROJECT" \
  --files .claude/agents/custom/CAPTAIN_PROBE_custom.md \
  --yes 2>&1)"
echo "$output" | grep "refusing to apply to custom-path file" \
  || { echo "FAIL: apply.sh did not refuse custom path"; exit 1; }
[ -f "${SYNTHETIC_PROJECT}/.claude/agents/custom/CAPTAIN_PROBE_custom.md" ] \
  || { echo "FAIL: custom CAPTAIN modified by apply.sh"; exit 1; }
echo "$(stat -c '%Y' "${SYNTHETIC_PROJECT}/.claude/agents/custom/CAPTAIN_PROBE_custom.md")"

# Smoke 3: --all-differing against a workspace with custom files does not produce
# any custom-path entries in the apply set (D4 already filters at check.sh source).
bash substrate/skills/check-substrate-updates/apply.sh --workspace "$SYNTHETIC_PROJECT" --all-differing --yes 2>&1 \
  | grep "custom" && { echo "FAIL: --all-differing harvested custom paths"; exit 1; }
echo "D5 smoke PASS"
```

### 6.3 D5 cite-comment grep verification

```bash
grep -c "custom-path" substrate/skills/check-substrate-updates/apply.sh  # expect >= 2 (case + error message)
grep -n "operating-disciplines.md §23" substrate/skills/check-substrate-updates/apply.sh  # expect >= 1
grep -n "case .dep. in" substrate/skills/check-substrate-updates/apply.sh | grep "custom"  # expect 1
```

---

## §7 — D6 workspace CLAUDE.md handling

### 7.1 The pick: option (b) — separate marker-bounded block

Three candidates were named in the dispatch brief: (a) extend the existing POLYBIUS reference block; (b) add a separate marker-bounded "base-vs-custom" block alongside the POLYBIUS reference; (c) leave install.sh CLAUDE.md handling unchanged. Pick: **(b)**.

Rationale:
- **Independent idempotency.** Each marker-bounded block is independently idempotent (`install.sh` already uses the marker-grep-then-skip pattern at line 721). Extending the POLYBIUS block (option a) would force one of two awkward outcomes: either the marker check sees the existing partial block and skips even though the base-vs-custom content is new (bug), or the block is re-appended in full (loses the operator's customizations between markers, if any). Separate markers separately checkable, separately appendable.
- **Operator visibility without manual action.** Option (c) hides the convention from the operator's project `CLAUDE.md` view; they would only see it if they read substrate role files directly. The convention is a workspace-level concern; surfacing it in the workspace's `CLAUDE.md` is the right reading-context.
- **Authored once at first install, skipped on re-install.** Same shape as the POLYBIUS reference block; no behavior change for operators who already opted into `--modify-claude-md` (the consent flag still gates the entire append behavior).

The new block is gated by the same `--modify-claude-md` flag as the POLYBIUS block. Operators who declined the consent flag get neither block. The gating is intentional: `install.sh` does NOT modify any `CLAUDE.md` without explicit consent.

### 7.2 The marker text + block prose

Add a second marker constant near line 151 (alongside `CLAUDE_MD_MARKER`):

```bash
CLAUDE_MD_BASE_VS_CUSTOM_MARKER="<!-- agent-substrate: base-vs-custom convention -->"
```

After the existing POLYBIUS-block append logic (after line 750 `fi`), add a second idempotent append:

```bash
# Separate marker-bounded block: base-vs-custom convention paths. Gated by
# the same --modify-claude-md consent flag as the POLYBIUS reference block
# above. Independent marker so the two blocks are separately idempotent.
# Discipline reference: substrate/operating-disciplines.md §23 + substrate/
# MAJOR_POLYBIUS.md §17.
if [ "$MODIFY_CLAUDE_MD" -eq 1 ]; then
  if [ -f "$DEST_CLAUDE_MD" ] && grep -Fq "$CLAUDE_MD_BASE_VS_CUSTOM_MARKER" "$DEST_CLAUDE_MD" 2>/dev/null; then
    log "CLAUDE.md already references base-vs-custom convention — skipping append (idempotent)"
  else
    BVC_BLOCK="

${CLAUDE_MD_BASE_VS_CUSTOM_MARKER}
## Customize your stoa team — base vs custom

This workspace carries a BASE stoa team deployed from substrate. To customize agents, skills, or templates, author them at the conventional custom paths below. Substrate updates (\`install.sh\` re-runs, \`check-substrate-updates\` applies) leave custom files untouched.

| Class | Custom path |
|---|---|
| Custom CAPTAINs | \`.claude/agents/custom/CAPTAIN_<MNEMONIC>_<slug>.md\` |
| Custom skills | \`.claude/skills/custom-<skill-name>/SKILL.md\` |
| Custom templates | \`.claude/templates/custom/*.md\` |

Custom CAPTAIN \`name:\` frontmatter MUST be distinct from base agent names (Claude Code silently drops one on collision). The convention is \`name: CAPTAIN_<MNEMONIC>_<distinct-slug>\`.

See \`.claude/MAJOR_POLYBIUS.md\` §17 (POLYBIUS-specific) and \`.claude/operating-disciplines.md\` §23 (universal-team framing) for the full discipline.
"
    if [ "$DRY_RUN" -eq 1 ]; then
      echo "[dry-run] would append base-vs-custom convention block to: $DEST_CLAUDE_MD"
      printf '%s\n' "$BVC_BLOCK" | sed 's/^/[dry-run]   /'
    else
      # Backup already done in the POLYBIUS-block branch above; only append here.
      printf '%s\n' "$BVC_BLOCK" >> "$DEST_CLAUDE_MD"
      echo "appended base-vs-custom convention block to: $DEST_CLAUDE_MD"
    fi
  fi
fi
```

The backup of `CLAUDE.md` to `.bak` already happens once in the POLYBIUS-block branch (line 743-746); the second append (this block) does NOT re-backup (single-shot backup per run is the existing convention).

### 7.3 D6 probe spec

```bash
# Smoke 1: with --modify-claude-md against a fresh project, BOTH blocks land.
SYNTHETIC_FRESH="$(mktemp -d)"
bash substrate/install.sh --target project --project-dir "$SYNTHETIC_FRESH" --modify-claude-md
grep -q "<!-- agent-substrate: POLYBIUS reference -->" "${SYNTHETIC_FRESH}/CLAUDE.md" \
  || { echo "FAIL: POLYBIUS marker missing"; exit 1; }
grep -q "<!-- agent-substrate: base-vs-custom convention -->" "${SYNTHETIC_FRESH}/CLAUDE.md" \
  || { echo "FAIL: base-vs-custom marker missing"; exit 1; }

# Smoke 2: re-install is idempotent (both markers still single-instance).
bash substrate/install.sh --target project --project-dir "$SYNTHETIC_FRESH" --modify-claude-md
[ "$(grep -c "<!-- agent-substrate: POLYBIUS reference -->" "${SYNTHETIC_FRESH}/CLAUDE.md")" -eq 1 ] \
  || { echo "FAIL: POLYBIUS marker duplicated"; exit 1; }
[ "$(grep -c "<!-- agent-substrate: base-vs-custom convention -->" "${SYNTHETIC_FRESH}/CLAUDE.md")" -eq 1 ] \
  || { echo "FAIL: base-vs-custom marker duplicated"; exit 1; }

# Smoke 3: without --modify-claude-md, neither block is added.
SYNTHETIC_NO_CONSENT="$(mktemp -d)"
bash substrate/install.sh --target project --project-dir "$SYNTHETIC_NO_CONSENT"
[ ! -f "${SYNTHETIC_NO_CONSENT}/CLAUDE.md" ] || ! grep -q "agent-substrate" "${SYNTHETIC_NO_CONSENT}/CLAUDE.md" \
  || { echo "FAIL: blocks added without --modify-claude-md consent"; exit 1; }
rm -rf "$SYNTHETIC_FRESH" "$SYNTHETIC_NO_CONSENT"
echo "D6 smoke PASS"
```

---

## §8 — Acceptance probes (consolidated; VERA + ZENO)

The directive's Phase B names 8 probes. Each maps to a runnable check below. Probes 1-4 reuse the synthetic-project fixture from §4.2; Probe 5 is the live Claude Code session test deferred to VERA's real-session execution (substrate prose alone cannot verify session-level behavior).

### Probe 1: Custom-file preservation under install.sh

```bash
# Already in §4.2 D3 Smoke 2. PASS = custom files present after re-install.
```

### Probe 2: Base-path overwrite (failure-mode demonstration)

```bash
# Drop a stub at a BASE path (mimicking the silent-overwrite footgun); verify
# install.sh overwrites it. This probe demonstrates WHY the convention exists.
echo "OPERATOR_CUSTOMIZED_BASE_AGENT" > "${SYNTHETIC_PROJECT}/.claude/agents/CAPTAIN_DAEDALUS_probe_project.md"
bash substrate/install.sh --target project --project-dir "$SYNTHETIC_PROJECT"
grep -q "OPERATOR_CUSTOMIZED_BASE_AGENT" "${SYNTHETIC_PROJECT}/.claude/agents/CAPTAIN_DAEDALUS_probe_project.md" \
  && { echo "FAIL: base-path overwrite did NOT occur — the footgun is gone (unexpected); investigate"; exit 1; }
echo "Probe 2 PASS: base-path overwrite occurred as designed; convention exists to prevent operator authoring at base paths"
```

### Probe 3: check.sh scope (DRIFTED/MISSING/OBSOLETE apply only to base)

```bash
# Already in §5.2 D4 Smoke 2. PASS = no custom paths appear in check.sh output.
```

### Probe 4: apply.sh scope (--yes safe against custom)

```bash
# Already in §6.2 D5 Smoke 2 + Smoke 3. PASS = custom paths refused (--files) or filtered (--all-differing).
```

### Probe 5: Claude Code agent auto-discovery at convention path (LOAD-BEARING LIVE)

```bash
# Substrate-tool probes cannot verify session-level Claude Code behavior.
# VERA executes this in a real Claude Code session against the synthetic-project
# fixture from Probe 1:
#
# 1. cd $SYNTHETIC_PROJECT
# 2. claude  (open Claude Code in the project)
# 3. PRINCIPAL or VERA invokes the Task tool with subagent_type = CAPTAIN_PROBE_custom
# 4. PASS = the stub custom agent activates and returns its stub output
# 5. FAIL = "no such subagent" error — convention is wrong-shaped for this scope
#
# If FAIL, surface to MAJOR_PLINY immediately; the convention pick (D2 §2.2) may
# need to pivot from subdirectory to filename-suffix `_custom` for CAPTAINs, and
# all downstream D3/D4/D5 cite-comments adjust accordingly. The empirical
# verification PLINY did from the docs (web-fetched 2026-05-17) is the
# strongest signal we have absent the live test; this probe is the final
# confirmation against the actual Claude Code build.
```

### Probe 6: Cross-consistency between canon texts

```bash
# All three locations describe the convention identically.
grep -A 12 "## 17. Base vs custom"  substrate/MAJOR_POLYBIUS.md     > /tmp/canon-pol.txt
grep -A 12 "## 23. Base vs custom"  substrate/operating-disciplines.md > /tmp/canon-od.txt
grep -A 12 "base-vs-custom convention" substrate/install.sh > /tmp/install-cites.txt
# Visual inspection: per-class paths match across both canon files; install.sh
# cite-comments reference §17 + §23 consistently. CATO cold-reads this; VERA
# verifies the grep counts.
[ "$(grep -c 'agents/custom/CAPTAIN_'  substrate/MAJOR_POLYBIUS.md)" -ge 1 ] || exit 1
[ "$(grep -c 'agents/custom/CAPTAIN_'  substrate/operating-disciplines.md)" -ge 1 ] || exit 1
[ "$(grep -c 'skills/custom-'          substrate/MAJOR_POLYBIUS.md)" -ge 1 ] || exit 1
[ "$(grep -c 'skills/custom-'          substrate/operating-disciplines.md)" -ge 1 ] || exit 1
[ "$(grep -c 'templates/custom/'       substrate/MAJOR_POLYBIUS.md)" -ge 1 ] || exit 1
[ "$(grep -c 'templates/custom/'       substrate/operating-disciplines.md)" -ge 1 ] || exit 1
echo "Probe 6 PASS"
```

### Probe 7: Cite-comments present at every scoping site

```bash
# install.sh: 3 cite sites + 1 operator-visibility block
[ "$(grep -c 'operating-disciplines.md §23' substrate/install.sh)" -ge 3 ] || exit 1
[ "$(grep -c 'MAJOR_POLYBIUS.md §17'        substrate/install.sh)" -ge 3 ] || exit 1
# check.sh: 4 cite sites (Sites 1, 2, 3 + Site 4 forward-looking MAJOR cite at check.sh:392)
[ "$(grep -c 'operating-disciplines.md §23' substrate/skills/check-substrate-updates/check.sh)" -ge 4 ] || exit 1
[ "$(grep -c 'MAJOR_POLYBIUS.md §17'        substrate/skills/check-substrate-updates/check.sh)" -ge 4 ] || exit 1
# apply.sh: 1 cite site (one refusal point)
[ "$(grep -c 'operating-disciplines.md §23' substrate/skills/check-substrate-updates/apply.sh)" -ge 1 ] || exit 1
echo "Probe 7 PASS"
```

### Probe 8: CURRENT regression on existing registered workspaces

```bash
# Workspaces without customizations should report whatever they reported pre-Arc-29.
# the-stoa itself will show DRIFTED on the edited substrate files (POLYBIUS.md +
# operating-disciplines.md + install.sh + check.sh + apply.sh); that is the
# expected diff of this arc's own edits, not a regression.
bash substrate/skills/check-substrate-updates/check.sh 2>&1 | tee /tmp/check-output.txt
# Inspect: ariadne-core-workspace, railway_stoa, sector-4 (or whatever the
# registry currently contains) should still show their pre-Arc-29 verdicts.
# the-stoa-self entry (if present) shows DRIFTED on the 5 substrate files.
```

---

## §9 — ADA build sequence (recommended order)

Partial-build states must not break existing tooling. The order below sequences edits so that at every commit the substrate is internally consistent.

1. **D1 first** — `substrate/MAJOR_POLYBIUS.md` §17 + `substrate/operating-disciplines.md` §23. Pure additive prose; no code change; cannot break anything. Lands the canon that all subsequent cite-comments reference.

2. **D6 next** — `substrate/install.sh` CLAUDE.md base-vs-custom block. Adds the second marker + the second append branch. Gated by `--modify-claude-md` so non-consent installs are unchanged. Smoke test against a synthetic project before continuing.

3. **D3 third** — `substrate/install.sh` cite-comments at Sites 1, 2 + the load-bearing Site 3 skill skip + Site 4 operator-visibility block. After this commit, `install.sh` correctly handles a workspace with custom files at all three convention paths.

4. **D4 fourth** — `substrate/skills/check-substrate-updates/check.sh` cite-comments at Sites 1, 2 + the load-bearing Site 3 skill skip + Site 4 forward-looking cite at check.sh:392 (MAJOR glob; no functional change, defensive comment only). After this commit, `check.sh` does not flag custom files as OBSOLETE.

5. **D5 last** — `substrate/skills/check-substrate-updates/apply.sh` explicit refusal at custom paths. Lands after D4 so that `--all-differing` is naturally safe (D4 has already filtered check.sh output); the explicit refusal at `apply.sh` covers the `--files` direct-path surface.

Each commit is a logical unit; ADA may bundle adjacent commits if review is cleaner that way (e.g., D3+D4+D5 as "substrate tool scoping" if the diff is compact). The split is a recommendation, not a hard requirement.

After the last commit, run all D3/D4/D5/D6 smoke tests against the synthetic fixture (§4.2 + §5.2 + §6.2 + §7.3), then check.sh against the live registered workspaces (Probe 8). VERA runs the acceptance probes (§8); CATO cold-reads the diff; ZENO checks D1-D6 each marked DONE by artifact reference.

---

## §10 — Weak points + open questions (self-assessed, per §6.2)

### 10.1 The custom-skill prefix `custom-` may collide with operator naming

If an operator already has a skill they named with a `custom-` prefix for unrelated reasons (e.g., `custom-tooling-helper`), Arc 29's substrate tools will now silently treat it as out-of-scope (skipped during install.sh staleness scan; not included in check.sh OBSOLETE scan). For a previously-tracked skill this could surface as "skill silently no longer flagged"; for a never-tracked skill this is fine.

**Why this shape anyway:** the prefix is the cleanest available option given Claude Code's single-level skill discovery. The alternative (no convention; substrate exclusion-list in code) is worse because it hides the discipline from the workspace. The collision risk is low (`custom-` is a deliberate substrate-namespace claim; operators rarely use it as a casual prefix), and the failure mode is "skill silently treated as workspace-owned," which is what the operator probably wants anyway. ARGUS may want to flag this risk in cold audit; PRINCIPAL adjudication may be appropriate if the risk feels load-bearing.

### 10.2 Custom MAJORs at POLYBIUS/PLINY tier are deferred (A7 hard-lock)

The convention covers CAPTAINs + skills + templates. Whether custom MAJORs make sense is a separate design question. A workspace that wants a custom MAJOR cannot land it under Arc 29's convention; the design is silent on this. **Why this shape anyway:** PRINCIPAL's declaration named base vs custom for the team-as-whole; MAJORs are the persistent-memory + orchestrator seats and customizing them touches lifecycle concerns the convention does not currently address (e.g., a custom POLYBIUS' relationship to the substrate POLYBIUS' lifecycle modes §16.2). Deferred to a future arc with its own design pass.

### 10.3 The cite-comment discipline rests on grep, not enforcement

The cite-comments at every scoping site surface the discipline at the read site, but a future maintainer can still ignore the cite-comment and "improve" the glob to recursive (e.g., `**/CAPTAIN_*.md` instead of `*/CAPTAIN_*.md`) without removing the cite-comment. The discipline is "read the cite before editing," which is operator-attention-bound. **Why this shape anyway:** the alternative (a runtime guard inside install.sh that checks for the cite-comment's presence) would be ceremony-for-its-own-sake; the cite-comment is the same shape used at `apply_substitutions()` and `parse_skill_names_from_install()` in `check.sh` (Arc 26 precedent), and the pattern has held across Arcs 26-28. Empirical track record: no regression has surfaced from a missed cite read. Future arc could promote to runtime guard if a regression appears.

### 10.4 Probe 5 (live Claude Code auto-discovery) is deferred to VERA

PLINY's empirical verification from the docs is strong but not equivalent to running the actual Claude Code build against a custom CAPTAIN at the convention path. If the docs prose is accurate but a specific Claude Code version on disk has a bug (e.g., recursive scan disabled by some compatibility flag), the convention fails for that operator and the substrate would silently no-op the custom CAPTAIN. **Why this shape anyway:** substrate-design work cannot fire Claude Code; the live probe is VERA's seat to execute against a real session. The empirical verification surfaced no contradiction in the docs prose, so the convention is the right starting bet.

### 10.5 Suppressed A7 reaches (recorded for PLINY routing)

Three temptations surfaced during design that I deliberately did NOT design against, per A7:

- **Auto-generated custom scaffolding** (e.g., `install.sh --scaffold-custom-captain DEPLOYER railway`). Surfaced because the silent-collision discipline (§17.4) is a footgun that a scaffolding command would mitigate. Suppressed per A7; the scaffolding belongs in a future arc that pairs with the agent-author skill.
- **A four-state drift classification at check.sh** that explicitly names "BASE-DRIFTED, BASE-MISSING, BASE-OBSOLETE, CUSTOM-PRESENT" with an explicit CUSTOM-PRESENT section in the verdict. Surfaced because the current output now has an asymmetry: install.sh prints the operator-visibility "custom files coexist" line (§4.1 Site 4), check.sh does not. Suppressed per A7 (the `stoa--lyh` Option Small punt is hard-locked); the asymmetry can be revisited in a future arc once empirical signal arrives.
- **Cross-workspace custom-agent sharing** (a custom CAPTAIN at one workspace re-deployed to another). Surfaced because the railway_stoa team will want this once their custom DEPLOYER is hardened. Suppressed per A7; explicit sibling arc.

### 10.6 The §15 N=1 honesty rests on the railway_stoa arc landing

The provenance block (§17.5 + §23.4) names the railway_stoa arc as the empirical anchor. If that arc slips or pivots, the substrate canon sits with N=1-from-declaration-only for longer than expected. **Why this shape anyway:** the canon is in NOW because PRINCIPAL named it; the railway arc is the structural-promotion-evidence path, not the canon-existence gate. If railway slips, the canon stays in and a different workspace's first customization becomes the empirical anchor. The §15 framing accommodates this.

### 10.7 Open questions for ARGUS

- **Q1:** Is `.claude/agents/custom/` the right shape, or would `.claude/agents/_custom/` (leading underscore) better signal "substrate-namespace" to a future operator? Leading-underscore is a Unix convention for "hidden" / "internal"; subdirectory `custom/` is more directly readable. I picked `custom/` for readability; ARGUS may prefer the underscore for namespace-claim strength.
- **Q2:** *(Resolved revision-round-2.)* The operator-visibility block in install.sh (§4.1 Site 4) prints unconditionally when ANY custom files exist. Should it instead be gated by a `--verbose` flag or always-print? ARGUS sustained always-print (operator confidence in "the convention is working" is the design intent); the related gating-asymmetry concern (CAPTAIN/template count blocks must respect `WITH_CAPTAINS` / `WITH_TEMPLATES`) was absorbed in §4.1 Site 4 itself — see the "Gating rationale" note there.
- **Q3:** Should `apply.sh`'s refusal at custom paths exit non-zero (per-file) or continue (just refuse this one, proceed with others)? Current design (`continue`) matches the existing "skipping (not a substrate-derived path)" shape at apply.sh:281. ARGUS may want exit-non-zero so an operator's typo is harder to miss.
- **Q4:** Is option (b) for D6 (separate marker block) right, or should the convention be in the substrate canon only (option c, no `CLAUDE.md` modification)? I picked (b) for operator visibility; ARGUS may judge that workspace `CLAUDE.md` should stay sparse.

---

End design.
