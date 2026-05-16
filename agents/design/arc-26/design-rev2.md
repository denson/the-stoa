# Arc 26 — Substrate-update check: full-picture detection

**Revision:** rev2 (post-ARGUS audit 2026-05-16)
**Supersedes:** `agents/design/arc-26/design.md` (rev1) — kept on disk as history; rev2 is the canonical spec ADA builds from.
**Design author:** Denson Smith (DAEDALUS @ the-stoa project-tier)
**Bw ticket:** `stoa--dxw`
**Directive:** `substrate/arcs/arc-26-build-directive.md` (Phase A decisions A1–A8 LOCKED — this design implements them, does not re-deliberate)
**Files touched by ADA:** `substrate/skills/check-substrate-updates/check.sh` (extend), `substrate/skills/check-substrate-updates/SKILL.md` (doc update). Two files, one arc. (apply.sh and install.sh untouched per deliverables 6-7.)

---

## §0. CHANGELOG from rev1

ARGUS audited rev1 2026-05-16 and returned `revise` with 4 P0 blockers + 3 P1 + 3 P2. Resolutions baked into rev2:

**P0-1.** §4.5 `uncommitted_claude_count` `printf "" | grep -c . || echo 0` produces `0\n0` (two-line) on empty input — `grep -c .` writes 0 and exits 1, so `|| echo 0` also fires; downstream integer compares fail under `set -euo pipefail`. **Fix:** align to directive A5's canonical form (`git status --porcelain ... | grep -v ... | wc -l`) and use the shipped `wc -l | tr -d ' '` idiom (check.sh:424-425 canon). No `grep -c` involved. §4.5 spec rewritten.

**P0-2.** §4.6.6 `IFS=' + '; echo "${arr[*]}"` is the broken form §7.6 self-flagged — multi-char IFS uses only the first char, so the join produces `DRIFTED MISSING OBSOLETE` (space-joined). **Fix:** §4.6.6 spec replaced with the case-based form §7.6 already specified; the rev1 §7.6 meta-commentary is folded into §4.6.6 as inline rationale and deleted from §7.

**P0-3 (structural).** Per-category detail blocks all used `  - ` (two-space-dash-space) prefix in rev1; apply.sh:213-228 harvests `  - *` blindly with no section-context awareness, so `apply.sh --workspace X --all-differing --yes` on a DRIFTED+MISSING workspace would silently deploy MISSING files via the cp at apply.sh:370 — granting unsolicited `--add-missing` behavior, violating A8 + deliverable 6. **Fix:** option (a) — distinct prefix per category. DRIFTED keeps `  - ` (preserves apply.sh harvest unchanged); MISSING uses `  + `; OBSOLETE uses `  ! `. apply.sh's `case "$line" in "  - "*) ...` only matches DRIFTED. Zero apply.sh edit. §4.6.8 spec updated; new VERA Probe 8 added to guard the property.

**P0-4.** OBSOLETE routing footer in rev1 emitted a single `install.sh --prune-obsolete` line for every OBSOLETE category present. install.sh:60-69, 766-770 deliberately exclude `MAJOR_*.md` from prune (pair-programmer MAJORs land in same agents/ dir), and install.sh:781/801 gate prune on `--no-captains`/`--no-templates`. If check.sh flags `.claude/MAJOR_FOO.md` as OBSOLETE per A4, the rev1 footer silently doesn't work. **Fix:** option (b) — split OBSOLETE routing. check.sh partitions OBSOLETE entries into `obsolete_major_files` (MAJOR_*.md basenames) and `obsolete_prunable_files` (everything else). Emit one footer line per partition: install.sh-prunable get the `install.sh --prune-obsolete` line; MAJORs get a manual-rm line. No directive deviation (A4's "MAJOR_*.md in scope for detection" stays honored; the asymmetry between detection-scope and install.sh's prune-scope is now surfaced explicitly to the operator).

**P1-1.** §2.3 cite-comment for the awk parser now names the failure-mode symptom explicitly ("if this awk returns empty for a substrate that has skills, the array form in install.sh changed; DO NOT trust resulting MISSING/OBSOLETE output"). Was coupling-only in rev1.

**P1-2.** §4.6.3 wording tightened: "the source-side enumeration set IS the live ground truth, not the hand-maintained mirror that rev1 removed; if the source set ever returns empty for a substrate that has skills, the parser is broken and the run is untrustworthy." ZENO's spec-vs-result check now unambiguous.

**P1-3.** §4.6.4 array iteration guarded with `if [ "${#obsolete_files[@]}" -gt 0 ]; then ... fi` to avoid `${obsolete_files[@]:-}` phantom-empty-string iteration. ZENO smell removed.

**P2-1.** §4.6.8 routing footer at subproject tier now branches on tier: `install.sh --target subproject` uses `--parent-dir <parent> --subproject <slug>`, not `--project-dir`. (install.sh ll. 71-78 verified.) Project tier keeps `--project-dir`.

**P2-2.** §6 Probes 1 and 3 both got an explicit "verify workspace is clean before running" preamble.

**P2-3.** §5.2 example output annotates the `Last check:` line as "(omitted on first check — state file not yet written)".

---

## §1. Intent

Today `check.sh` answers one question per workspace: "of the files I already know about (because they were enumerated from a hard-coded source-side mirror inside check.sh), do any differ from the substrate source?" That answer is correct as far as it goes — DRIFTED is detected, CURRENT means no drifts among the enumerated set — but it is silent about two structural states that matter operationally:

- **MISSING:** the substrate source has a file the workspace doesn't have at its deployed path (e.g. a new skill added to `install.sh`'s `SKILL_NAMES`, a new CAPTAIN, a new template, a new top-level role file). The Arc-25 `credential-discipline` skill is the canonical example — without an out-of-band pointer from the prior POLYBIUS ("5 files + 1 new skill"), check.sh would have reported CURRENT and the operator would have shipped three workspaces missing the new skill.
- **OBSOLETE:** the workspace has a file at a substrate-deployable path that the substrate source no longer ships (e.g. a removed skill, a renamed CAPTAIN). `install.sh --prune-obsolete` already handles removal of a deliberately-narrower scope; check.sh has no equivalent surfacing.

Plus a third signal that is *not* a drift category but matters at apply-time: **uncommitted `.claude/` state** in the workspace's git. `apply.sh --yes` auto-commits-then-overwrites; if the local edit was intentional this is semantically destructive (recoverable through git history, but the operator should know before pressing the button).

This design extends `check.sh` to surface all three new signals alongside the existing DRIFTED behavior — without growing `apply.sh` into install.sh's territory (deliverable 6: apply.sh stays narrow), without changing `install.sh` (deliverable 7), and without disturbing the existing `apply_substitutions` cite-comment mitigation pattern (A8 hard-locked: don't remove it). The locked verdict tokens (CURRENT, DRIFTED, MISSING, OBSOLETE, composite) and routing-footer shape come from directive §A6; this design fills in the structural mechanics underneath them. SKILL.md gets a parallel doc update covering classifications, invocation, the v0 limitations paragraph, and the new SKILL_NAMES coupling note.

Maps to stoa--dxw deliverables 1–7 (MISSING detection, OBSOLETE detection, uncommitted-state surfacing, output format, SKILL.md update, apply.sh unchanged, install.sh unchanged) and directive Phase A items A2 (three categories + uncommitted pre-flight), A3 (source-side enumeration), A4 (OBSOLETE scope), A5 (uncommitted detection), A6 (output format), A7 (SKILL.md scope).

---

## §2. Sub-decision A3 — SKILL_NAMES parsing mechanism

### §2.1 Resolution

**Option A — shell extraction via awk from install.sh.** Replace the hard-coded `SKILL_NAMES` mirror at `check.sh:92-95`. Drop the `CAPTAIN_NAMES` (lines 70-81) and `TEMPLATE_NAMES` (lines 83-90) mirrors entirely — their source-side enumeration becomes glob-derived (per directive A3 items 2-3).

### §2.2 Evidence motivating live-parse over keep-the-mirror

The current mirror at `check.sh:92-95` is **right now, today, drifted from `install.sh:140-144`**:

| `install.sh:140-144` (source-of-truth) | `check.sh:92-95` (mirror) |
|---|---|
| `agent-author` | `agent-author` |
| `check-substrate-updates` | `check-substrate-updates` |
| `credential-discipline` | *(missing)* |

Arc 25 added `credential-discipline` to `install.sh`'s SKILL_NAMES (commit `030a5f8` referenced in `git log`) and the cite-comment-required-mirror-update at `check.sh:64-68` did not fire — not because the comment is missing or wrong, but because the human reading the diff missed it. **This is the exact silent-CURRENT failure mode Arc 26 closes** — and the closing-mechanism would itself be vulnerable to the same failure mode if check.sh kept relying on a manually-maintained mirror.

The cite-comment-at-the-read-site pattern (`apply_substitutions()` at `check.sh:106-115`) works *brilliantly* for placeholder-substitution coupling, where the substitutions are small (one or two `{{...}}` tokens), change rarely, and the consequence of mismatch is *visible* (every drift-check produces false positives). It works *less well* for enumeration mirrors, where additions are routine (every new skill, every new CAPTAIN), the change is structurally identical to "edit install.sh," and the consequence of mismatch is *invisible* (check.sh silently doesn't enumerate the new file, so it can't report DRIFTED or MISSING for it). The mirror's "if install.sh adds or removes a name, this list must be updated to match" comment at `check.sh:64-68` is *exactly* the kind of "trust the reader to remember" mitigation that Arc 26 is fixing for the operator-side equivalent.

### §2.3 Why Option A (shell extraction), not Option B (sourcing install.sh)

Sourcing install.sh in a controlled subshell — `(set -e; SKILL_NAMES=(); . install.sh ; printf '%s\n' "${SKILL_NAMES[@]}")` or similar — gets the array contents without parsing, which is appealing. But install.sh has top-level side effects: argument parsing (`while [ "$#" -gt 0 ]; do case "$1" in --target) ...`), tier detection, the `choose_user_tier_dir` interactive prompt path (gated on TTY-detection but still in the top-level flow), and ultimately the deploy itself. Sourcing it — even in a subshell — risks executing parts of that flow if the guards don't fire cleanly, and any future install.sh edit that adds a top-level side effect upstream of `SKILL_NAMES=(...)` would silently break the check.sh source operation.

ARGUS verified rev1: the awk parser in §2.3 below correctly extracts all 3 skill names from current install.sh:140-144 with zero side effects. Picking the safer option.

The shell extraction is small and targeted:

```bash
# parse_skill_names_from_install: echo one name per line.
# Reads substrate/install.sh and extracts the SKILL_NAMES=(...) array contents.
#
# CITE: parses install.sh:140-144 (SKILL_NAMES array, multi-line form). If
# install.sh changes the array name, moves to a single-line / non-parenthesized
# form, or uses += append syntax, this function must update its awk expression
# to match.
#
# FAILURE-MODE SYMPTOM (rev2 P1-1, per ARGUS): if this awk returns empty for a
# substrate that has skills (i.e. install.sh:140 region exists but stdout is
# empty), the parser is broken and the run is UNTRUSTWORTHY — every MISSING
# and OBSOLETE result will be wrong (MISSING will under-report; OBSOLETE will
# over-report any deployed skill directory as "no longer in source"). The
# previous hand-maintained mirror at check.sh:92-95 silently drifted in Arc 25
# (credential-discipline added to install.sh, not to mirror); this live-parse
# closes that drift surface, but at the cost of a parsing-correctness surface.
# The cite is the durable mitigation; VERA Probe 5 (CURRENT regression on the
# three live workspaces) is the runtime smoke for it.
parse_skill_names_from_install() {
  local install_sh="${SUBSTRATE_DIR}/install.sh"
  [ -f "$install_sh" ] || return 1
  # awk: print every line strictly between 'SKILL_NAMES=(' and the next ')',
  # stripping whitespace and skipping blanks/comments.
  awk '
    /^SKILL_NAMES=\(/ { in_arr = 1; next }
    in_arr && /^\)/   { in_arr = 0; next }
    in_arr            {
      gsub(/^[[:space:]]+|[[:space:]]+$/, "")
      if ($0 == "" || $0 ~ /^#/) next
      print
    }
  ' "$install_sh"
}
```

Inputs: none (uses script-global `SUBSTRATE_DIR`).
Outputs: one skill name per line on stdout.
Failure mode: empty stdout if install.sh missing or array empty/unrecognized form. Per the cite-comment, callers MUST treat empty as suspect, not as authoritative "no skills exist."

### §2.4 Reconciliation with the surviving CAPTAIN_NAMES and TEMPLATE_NAMES mirrors

The directive does not require live-parsing CAPTAINs or templates — the source-side enumeration for those uses globs (A3 items 2 and 3: `glob substrate/CAPTAIN_*.md` and `glob substrate/templates/*.md`), which is structurally cleaner than parsing install.sh.

**Decision:** for CAPTAINs and templates, use globs against `substrate/`. Drop the existing `CAPTAIN_NAMES` and `TEMPLATE_NAMES` mirrors at `check.sh:70-90` entirely — they become unused once `enumerate_deployed()` is reworked (see §4.2).

This is consistent: the mirror approach is replaced everywhere it would be vulnerable to install.sh drift. The result is **zero hand-maintained mirrors of install.sh enumerations inside check.sh** — every source-side set is either glob-derived (CAPTAINs, templates, MAJORs, operating-disciplines) or parsed-from-install.sh (skills). The cite-comment at `check.sh:64-68` is removed by the same edit that drops the arrays; the new cite-comment at `parse_skill_names_from_install` replaces it.

Directive §A3 item 1 says "parse SKILL_NAMES from `substrate/install.sh`," items 2-3 say "glob `substrate/CAPTAIN_*.md`" and "glob `substrate/templates/*.md`" — these are the live-discovery instructions and they are clear. Items 2-3 *implicitly* deprecate the CAPTAIN/TEMPLATE mirrors at check.sh:70-90 (otherwise why glob); making the deprecation explicit in this design avoids ADA leaving the now-unused arrays in place as "defensive duplication." ARGUS read rev1 and did not flag this as scope creep; in-line removal stands.

---

## §3. Cite-comment policy

The cite-comment-at-the-read-site pattern (precedent: `apply_substitutions()` block at `check.sh:106-115`) is preserved verbatim for placeholder-substitution coupling. Arc 26 adds **one new cite site**: `parse_skill_names_from_install()` (see §2.3 for full text).

Required structural shape, mirroring the precedent:

1. **Function-leading comment block** identifying the source file and the specific line numbers parsed (`install.sh:140-144` as of substrate HEAD at design-write time — the comment cites a line range, not a SHA; if the line numbers shift due to upstream install.sh edits the cite drifts but stays directionally correct, and a `grep -n "^SKILL_NAMES" install.sh` rediscovers ground truth instantly).
2. **Coupling-named explicitly:** "if install.sh changes the array name or moves to a non-parenthesized form, this function must update its awk expression to match."
3. **Failure-mode symptom named explicitly** (rev2 P1-1): "if this awk returns empty for a substrate that has skills, the parser is broken — DO NOT trust resulting MISSING/OBSOLETE output."
4. **Evidence of why the cite matters,** referencing the Arc 25 silent-drift (see §2.2 above) so a future reader understands *why* the live-parse exists and what failure mode it closes.

CATO will read for: (a) the cite-comment is present at every install.sh parse site (currently only one: the new `parse_skill_names_from_install`); (b) the cite includes line numbers, not just "see install.sh"; (c) the explicit-coupling sentence is there; (d) the failure-mode-symptom sentence is there; (e) the existing `apply_substitutions` cite-comment at `check.sh:106-115` is unchanged (A8 hard-locked).

No new cite-comments are needed at the CAPTAIN/template glob sites (globs are self-describing: `substrate/CAPTAIN_*.md` is its own documentation; nothing about install.sh is being mirrored).

---

## §4. check.sh extension spec — section-by-section

This section walks through every function `check.sh` gets that's new or modified. Existing helper functions left untouched are not re-listed.

### §4.1 New helper: `parse_skill_names_from_install()` — see §2.3 above

Already specified in full there. Slots into the helpers block; positionally, place it adjacent to the existing `apply_substitutions` / `source_path_for_deployed` cluster so the cite-comment-bearing functions stay grouped (roughly check.sh:145 in the post-edit file).

### §4.2 Modified: `enumerate_deployed(<ws> <tier> <slug>)` at `check.sh:265-308`

**Semantics change:** today, `enumerate_deployed` emits one deployed-relative path per line for every file the substrate is *expected* to have placed in the workspace, including a `find` walk into each source skill subtree to enumerate per-file under skills. The function is the source-of-truth for the "is the deployed file present?" check that already happens at `check.sh:394-396` (the dead `missing_count` increment).

**The change:** replace the three hard-coded array iterations with dynamic enumeration. New shape:

- **MAJOR files (lines 276-282):** unchanged. The tier-suffix rule is already correct.
- **operating-disciplines.md (line 284):** unchanged.
- **CAPTAINs (lines 288-290):** replace `for cap in "${CAPTAIN_NAMES[@]}"; do ... done` with a glob-derived loop:

```bash
local capf cap_base
shopt -s nullglob
for capf in "${SUBSTRATE_DIR}/CAPTAIN_"*.md; do
  cap_base="$(basename "$capf" .md)"  # "CAPTAIN_DAEDALUS"
  cap_base="${cap_base#CAPTAIN_}"      # "DAEDALUS"
  echo ".claude/agents/CAPTAIN_${cap_base}${suffix}.md"
done
shopt -u nullglob
```

- **Templates (lines 294-296):** replace `for tn in "${TEMPLATE_NAMES[@]}"` with a glob over `substrate/templates/*.md` (today all templates are `.md`). Use the same shape: glob, basename, emit deployed path.
- **Skills (lines 299-307):** replace `for sn in "${SKILL_NAMES[@]}"` with `for sn in $(parse_skill_names_from_install); do ... done`. The inner `find "${SUBSTRATE_DIR}/skills/${sn}" -type f` walk stays unchanged — it's already source-side enumeration of per-skill files.

The dead `CAPTAIN_NAMES` / `TEMPLATE_NAMES` / `SKILL_NAMES` arrays at `check.sh:70-95` get removed in the same edit (see §2.4 above). The cite-comment header at `check.sh:62-68` gets removed; the new cite-comment lives at `parse_skill_names_from_install()` (§3).

### §4.3 New helper: `enumerate_workspace_substrate_paths(<ws> <tier> <slug>)` — for OBSOLETE detection

**Purpose:** enumerate every file at a workspace path that *could* be substrate-deployable. Output: one workspace-relative-to-`.claude/`-path per line (e.g. `.claude/skills/some-skill/`, `.claude/agents/CAPTAIN_FOO.md`). Skills are emitted at directory level (per directive A4); other categories at file level.

**Inputs:** `ws` workspace abs path; `tier` and `slug` accepted but used only for filename-suffix expectations (CAPTAINs and MAJORs have suffix at project/subproject tier).

**Output (one per line):**

```
.claude/MAJOR_POLYBIUS.md            # or MAJOR_POLYBIUS_<slug>.md at subproject tier
.claude/MAJOR_PLINY.md               # or _<slug>
.claude/operating-disciplines.md
.claude/agents/CAPTAIN_<MNEM>.md     # for each glob match under <ws>/.claude/agents/CAPTAIN_*.md
.claude/templates/<basename>         # for each glob match under <ws>/.claude/templates/*
.claude/skills/<name>/               # for each directory under <ws>/.claude/skills/*/
```

**Shape:**

```bash
enumerate_workspace_substrate_paths() {
  local ws="$1" tier="$2" slug="$3" suffix=""
  case "$tier" in
    project|subproject) suffix="_${slug}" ;;
  esac

  local f
  shopt -s nullglob
  # MAJORs: glob workspace dir. Per A4 these ARE in scope for OBSOLETE detection
  # (asymmetry with install.sh's prune-scope, which excludes MAJORs — surfaced
  # to operator via split routing footer in §4.6.8).
  for f in "${ws}/.claude/MAJOR_"*.md; do
    echo ".claude/$(basename "$f")"
  done
  if [ -f "${ws}/.claude/operating-disciplines.md" ]; then
    echo ".claude/operating-disciplines.md"
  fi

  # CAPTAINs: glob workspace dir.
  if [ -d "${ws}/.claude/agents" ]; then
    for f in "${ws}/.claude/agents/CAPTAIN_"*.md; do
      echo ".claude/agents/$(basename "$f")"
    done
  fi

  # Templates: glob workspace dir.
  if [ -d "${ws}/.claude/templates" ]; then
    for f in "${ws}/.claude/templates/"*; do
      [ -f "$f" ] || continue
      echo ".claude/templates/$(basename "$f")"
    done
  fi

  # Skills: directory-level (per A4).
  if [ -d "${ws}/.claude/skills" ]; then
    local d
    for d in "${ws}/.claude/skills/"*/; do
      echo ".claude/skills/$(basename "$d")/"
    done
  fi
  shopt -u nullglob
}
```

**Files explicitly NOT enumerated (per A4):**

- `.claude/.substrate-last-check` — transient state file, written by `write_state_file()` at `check.sh:327-337`. Per directive A5 it's excluded from the uncommitted-state count too.
- `.claude/.substrate-backups/...` — apply.sh's pre-deploy backup tree (see apply.sh:264-269), not substrate-derived.
- `HUMAN_*.md` instruction files — user-added per directive A4.
- `.claude/agents/` files NOT matching the `CAPTAIN_*.md` pattern — user-added custom agents (e.g. a pair-programmer agent the operator dropped in).
- `.claude/skills/` files outside top-level subdirectories — the directive scopes skills to directory-level. A loose file directly under `.claude/skills/` (rare; not deployed by install.sh) is not flagged.

**Important precedent for the MAJOR asymmetry (rev2 P0-4):** install.sh's prune logic at `install.sh:766-770` *deliberately excludes* MAJOR_*.md files from obsolete detection because "pair-programmer Majors (PYTHAGORAS, ATTICUS, etc.) land in the same directory and cannot be reliably distinguished from substrate-canonical MAJORs by filename." Directive A4 nonetheless specifies `.claude/MAJOR_*.md` is in scope for check.sh's OBSOLETE detection — a deliberate divergence (check.sh is informational and surfaces; install.sh's prune is destructive). Rev1 papered over the consequence; rev2 surfaces it: any MAJOR_*.md OBSOLETE entry routes to a manual-rm footer line, not to `install.sh --prune-obsolete` (which would silently no-op on it). See §4.6.8 routing-footer split.

### §4.4 New helper: `is_substrate_source_present(<src-rel-path>)`

**Purpose:** for OBSOLETE detection, the inverse of `source_path_for_deployed`. Given a deployed-relative path, answer "does the substrate source still contain the file this would derive from?"

**Reuses existing logic:** call `source_path_for_deployed` to get the source-relative path, then `[ -e "${SUBSTRATE_DIR}/${src_rel}" ]`. For skills (directory-level), the test is `[ -d "${SUBSTRATE_DIR}/${src_rel%/}" ]` — but more critically, the skill must also be in `parse_skill_names_from_install` output (a skill directory could exist on disk under `substrate/skills/` but not be in install.sh's SKILL_NAMES — that would itself be a substrate-internal inconsistency, not the operator's concern, but for OBSOLETE we treat "not in install.sh's SKILL_NAMES" as "not substrate-derived").

**Shape:**

```bash
# is_substrate_source_present <deployed-rel-path> <tier> <slug>
# Returns 0 if the substrate source backs this deployed path, 1 otherwise.
# For skills: present iff the skill name is in install.sh's SKILL_NAMES
# (live-parsed) — directory existence under substrate/skills/ is not
# sufficient.
is_substrate_source_present() {
  local dep="$1" tier="$2" slug="$3"
  local rel="${dep#.claude/}"
  case "$rel" in
    skills/*)
      # Extract skill name (first path segment after skills/).
      local sname="${rel#skills/}"
      sname="${sname%%/*}"
      local known
      while IFS= read -r known; do
        [ "$known" = "$sname" ] && return 0
      done < <(parse_skill_names_from_install)
      return 1
      ;;
    *)
      local src_rel
      src_rel="$(source_path_for_deployed "$dep" "$tier" "$slug")"
      [ -n "$src_rel" ] && [ -e "${SUBSTRATE_DIR}/${src_rel}" ]
      ;;
  esac
}
```

### §4.5 New helper: `uncommitted_claude_count(<ws>)` — for A5 (REV2 REWRITE)

**Purpose:** count uncommitted `.claude/` files in the workspace, excluding the transient state file. Per directive A5.

**Spec form (rev2 — fixes P0-1):** the directive A5 at line 116 mandates the canonical idiom:

```
git status --porcelain .claude/ | grep -v '\.substrate-last-check$' | wc -l
```

`wc -l` returns `0` on empty input (it counts newlines, not match-existence). Pipe through `tr -d ' '` to strip the leading whitespace BSD/GNU `wc` emits in some environments. This is the same idiom check.sh:424-425 uses for line-count extraction — shipped canon. No `grep -c .` involvement; no `|| echo N` fallback needed; downstream `[ "$count" -gt 0 ]` compares are safe under `set -euo pipefail`.

**Shape:**

```bash
# uncommitted_claude_count <workspace-abs>
# Echoes a non-negative integer (count of uncommitted .claude/ files,
# excluding .substrate-last-check) or the literal "unknown" if the
# workspace is not git-tracked or .claude/ is not under git.
#
# Per directive A5: workspace must be inside a git repo for this signal to
# work; otherwise informational "unknown" is returned, not blocking.
#
# Implementation note: uses `git status --porcelain | grep -v ... | wc -l`
# per directive A5 line 116 canonical form. `wc -l` returns 0 on empty input
# (it counts newlines), so no `|| echo 0` defang needed. `tr -d ' '` strips
# the leading whitespace BSD/GNU wc emits in some environments — same idiom
# as check.sh:424-425. Safe under set -euo pipefail.
#
# Sibling-not-shared with apply.sh's git_uncommitted_claude (apply.sh:184-189)
# — apply.sh returns the file LIST (multi-line for display); check.sh needs
# only the COUNT (for the summary line). Inlined per design §9.2 note in
# apply.sh:74 ("shared shape with check.sh; inlined per design §9.2").
uncommitted_claude_count() {
  local ws="$1"
  # Must be inside a git work tree.
  if ! git -C "$ws" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    echo "unknown"
    return 0
  fi
  # .claude/ must be tracked or have any tracked files (consistent with
  # apply.sh's git_path_active helper at apply.sh:169-182).
  if ! git -C "$ws" ls-files .claude 2>/dev/null | grep -q .; then
    echo "unknown"
    return 0
  fi
  # Count porcelain lines, excluding .substrate-last-check. Per directive
  # A5; wc -l is empty-input-safe (returns 0).
  git -C "$ws" status --porcelain -- .claude 2>/dev/null \
    | grep -v '\.substrate-last-check$' \
    | wc -l \
    | tr -d ' '
}
```

VERA Probe 3 verifies the integer-return shape against `[ "$count" -gt 0 ]` semantics.

### §4.6 Modified: `check_workspace(<ws-input>)` at `check.sh:350-466`

This is the orchestration function; it gets the most structural change. New variables, new detection passes, new emission. Walking the post-edit shape top-to-bottom:

#### §4.6.1 Setup (lines 351-380, unchanged)

`ws_abs`, `label`, `tier`/`slug` detection, the NOT-FOUND / NOT-STOA-DEPLOYED / USER-TIER early returns stay byte-equal.

#### §4.6.2 Detection-pass arrays (replacing the existing `differs_files` / `differs_deltas` / `current_count` / `missing_count` / `total` setup at lines 383-387)

Replace with:

```bash
local drifted_files=()           # was differs_files
local drifted_deltas=()          # was differs_deltas
local missing_files=()           # NEW — populated by the existing-but-now-surfaced detection
local obsolete_prunable_files=() # NEW — OBSOLETE entries routable to install.sh --prune-obsolete
local obsolete_major_files=()    # NEW — OBSOLETE MAJOR_*.md entries (install.sh excludes from prune)
local current_count=0
local total=0
```

The renaming `differs` → `drifted` is for output-format consistency with the locked verdict token `DRIFTED`. Internal-only rename; no external interface depends on it (apply.sh harvests deployed paths from the human-readable output, not from variable names).

The split of `obsolete_files` into `obsolete_prunable_files` + `obsolete_major_files` (rev2 P0-4) lets the routing footer emit the right command per partition (see §4.6.8).

#### §4.6.3 Pass 1 — DRIFTED + MISSING (extends the existing loop at lines 389-435)

The existing `while IFS= read -r dep; do ... done < <(enumerate_deployed ...)` loop is the right place for both DRIFTED and MISSING — it already iterates the expected-deployed set, already checks `[ ! -f "$deployed_path" ]`, and already counts `missing_count` (which is currently dead). Extending it to *surface* MISSING is a small change:

- At the existing `[ ! -f "$deployed_path" ]` test (line 394): instead of incrementing the dead `missing_count`, append to `missing_files` and `continue`. The source-side enumeration IS the live ground truth (rev2 P1-2): if `enumerate_deployed` emits a path, that path's source-side artifact exists (because `enumerate_deployed` now derives from `substrate/CAPTAIN_*.md` glob, `substrate/templates/*` glob, and `parse_skill_names_from_install` live-parse — no mirror). If the live source set ever returns empty for a substrate that has skills, the awk parser is broken and the whole run is untrustworthy; the cite-comment §2.3 names this. The "in source" half of MISSING's definition is satisfied structurally, not by an additional check.
- The existing `source-removed` sentinel at lines 405-410 — when the source file is *gone* despite being enumerated as an expected deployed — is **a category-error case under the new model**. With the new live-parsing enumeration, this case is now impossible for skills (parse_skill_names_from_install only emits names whose source exists) and very rare for CAPTAINs/templates/MAJORs (since enumerate_deployed now globs the source side directly). If it ever does happen — racing-edit during a substrate-update where install.sh's SKILL_NAMES references a skill directory that was just deleted from `substrate/skills/` — the right surfacing is OBSOLETE-of-the-deployed-workspace-file. **Decision:** in the `[ ! -f "$src_abs" ]` branch, append to the right OBSOLETE partition (see §4.6.4 logic) instead of `drifted_files`. Pass 2 deduplication still applies.

#### §4.6.4 Pass 2 — OBSOLETE (new, with split routing — rev2 P0-4)

After Pass 1 completes, walk the workspace-side enumeration:

```bash
local ws_dep
while IFS= read -r ws_dep; do
  [ -n "$ws_dep" ] || continue

  # Skip if Pass 1 already flagged this as obsolete (rev2 P1-3: guard array
  # iteration against empty-array phantom string).
  local already_obsolete=0
  local of
  if [ "${#obsolete_prunable_files[@]}" -gt 0 ]; then
    for of in "${obsolete_prunable_files[@]}"; do
      [ "$of" = "$ws_dep" ] && { already_obsolete=1; break; }
    done
  fi
  if [ "$already_obsolete" -eq 0 ] && [ "${#obsolete_major_files[@]}" -gt 0 ]; then
    for of in "${obsolete_major_files[@]}"; do
      [ "$of" = "$ws_dep" ] && { already_obsolete=1; break; }
    done
  fi
  [ "$already_obsolete" -eq 1 ] && continue

  if ! is_substrate_source_present "$ws_dep" "$tier" "$slug"; then
    # Partition: MAJOR_*.md basenames go to manual-rm bucket; everything
    # else goes to install.sh --prune-obsolete bucket (rev2 P0-4).
    case "$ws_dep" in
      .claude/MAJOR_*.md)
        obsolete_major_files+=("$ws_dep")
        ;;
      *)
        obsolete_prunable_files+=("$ws_dep")
        ;;
    esac
  fi
done < <(enumerate_workspace_substrate_paths "$ws_abs" "$tier" "$slug")
```

The deduplication-against-Pass-1 prevents double-reporting in the racing-edit edge case. For all non-edge-case workflows, Pass 1's OBSOLETE partitions are empty and Pass 2 is the sole populator.

Partition rationale (rev2 P0-4 P0-fix): install.sh:60-69 and :766-770 deliberately exclude `MAJOR_*.md` from `--prune-obsolete` (pair-programmer MAJOR ambiguity). Emitting `install.sh --prune-obsolete` as the routing for a flagged-OBSOLETE MAJOR would silently no-op — actively misleading. Splitting the partition surfaces the asymmetry to the operator at routing time.

#### §4.6.5 Pass 3 — uncommitted (new, single call)

```bash
local uncommitted
uncommitted="$(uncommitted_claude_count "$ws_abs")"
```

`$uncommitted` is either an integer (zero-or-positive, safe for `-gt 0` compares under `set -euo pipefail` per rev2 P0-1) or the literal `unknown`.

#### §4.6.6 Verdict computation (REV2 REWRITE — fixes P0-2)

Replaces lines 445-447 of pre-edit check.sh. The naive `IFS=' + '` join is broken (multi-char IFS uses only the first char as separator, so the join produces space-separated tokens, not ` + `-separated). Use the explicit case-based form:

```bash
local n_drifted=${#drifted_files[@]}
local n_missing=${#missing_files[@]}
local n_obsolete=$(( ${#obsolete_prunable_files[@]} + ${#obsolete_major_files[@]} ))
local verdict_parts=()
local verdict

[ "$n_drifted"  -gt 0 ] && verdict_parts+=("DRIFTED")
[ "$n_missing"  -gt 0 ] && verdict_parts+=("MISSING")
[ "$n_obsolete" -gt 0 ] && verdict_parts+=("OBSOLETE")

# Join with " + " per locked directive A6 composite form. Explicit case form
# instead of `IFS=' + '; echo "${arr[*]}"` — bash multi-char IFS uses only
# the FIRST char as separator, so the IFS form would produce " "-separated
# tokens, not " + "-separated. Case form is unambiguous and matches the
# directive's literal " + " separator.
case "${#verdict_parts[@]}" in
  0) verdict="CURRENT" ;;
  1) verdict="${verdict_parts[0]}" ;;
  2) verdict="${verdict_parts[0]} + ${verdict_parts[1]}" ;;
  3) verdict="${verdict_parts[0]} + ${verdict_parts[1]} + ${verdict_parts[2]}" ;;
esac
```

Token order is drifted → missing → obsolete (matches directive A6). The `n_obsolete` total is the sum across both OBSOLETE partitions — operator sees one OBSOLETE count, the partition is internal to routing.

Format the uncommitted suffix:

```bash
local uncommitted_suffix
if [ "$uncommitted" = "unknown" ]; then
  uncommitted_suffix="; uncommitted-state: unknown (workspace not git-tracked)"
else
  uncommitted_suffix="; ${uncommitted} uncommitted"
fi
```

Per directive A6 format string `<verdict> (<N> drifted, <M> missing, <K> obsolete; <U> uncommitted)`.

#### §4.6.7 Emission — CURRENT case (replacing lines 446-450)

```bash
if [ "$verdict" = "CURRENT" ]; then
  printf "%-40s CURRENT (0 drifted, 0 missing, 0 obsolete%s)\n" "$label" "$uncommitted_suffix"
  if [ -n "$ts" ]; then
    printf "  Last check: %s (against substrate sha %s)\n" "$ts" "$last_sha"
  fi
  # If uncommitted > 0 even when CURRENT, surface the warning (per A6's
  # always-emit-on-uncommitted shape).
  emit_uncommitted_warning_if_needed "$uncommitted" "$ws_abs"
fi
```

Note: per directive A6 the format string says `<verdict> (<N> drifted, <M> missing, <K> obsolete; <U> uncommitted)` — CURRENT case includes the all-zeros explicit form rather than the existing "all N deployed files match" prose. This is the locked structural shape; the prose is replaced. ZENO will verify against A6 (acknowledged as a deliberate behavior change vs the existing format).

#### §4.6.8 Emission — non-CURRENT case (REV2 — fixes P0-3, P0-4, P2-1)

Three rev2 changes baked in: per-category prefix is distinct (P0-3); OBSOLETE routing splits MAJOR vs prunable (P0-4); routing footer's install.sh command branches on tier (P2-1).

```bash
else
  printf "%-40s %s (%d drifted, %d missing, %d obsolete%s)\n" \
    "$label" "$verdict" "$n_drifted" "$n_missing" "$n_obsolete" "$uncommitted_suffix"

  # Per-category detail blocks (only for non-zero categories).
  # PREFIX DISCIPLINE (rev2 P0-3): each category uses a DISTINCT prefix so
  # apply.sh's blind harvest of "  - "* matches only DRIFTED. apply.sh stays
  # untouched (deliverable 6) and cannot accidentally deploy MISSING files
  # via cp at apply.sh:370.
  #   DRIFTED:  "  - "  (two-space + dash + space) — apply.sh:218 harvests this
  #   MISSING:  "  + "  (two-space + plus  + space) — visual: "this needs adding"
  #   OBSOLETE: "  ! "  (two-space + bang  + space) — visual: "this needs attention"
  if [ "$n_drifted" -gt 0 ]; then
    echo "  DRIFTED:"
    local i
    for ((i=0; i<n_drifted; i++)); do
      printf "  - %-50s (%s)\n" "${drifted_files[$i]}" "${drifted_deltas[$i]}"
    done
  fi
  if [ "$n_missing" -gt 0 ]; then
    echo "  MISSING:"
    local m
    for m in "${missing_files[@]}"; do
      printf "  + %-50s (new in source)\n" "$m"
    done
  fi
  if [ "$n_obsolete" -gt 0 ]; then
    echo "  OBSOLETE:"
    # Emit prunable first, MAJORs second — preserves visual contiguity.
    if [ "${#obsolete_prunable_files[@]}" -gt 0 ]; then
      local op
      for op in "${obsolete_prunable_files[@]}"; do
        printf "  ! %-50s (dropped from source)\n" "$op"
      done
    fi
    if [ "${#obsolete_major_files[@]}" -gt 0 ]; then
      local om
      for om in "${obsolete_major_files[@]}"; do
        printf "  ! %-50s (dropped from source; manual-rm — see footer)\n" "$om"
      done
    fi
  fi

  # Pre-existing state-info lines, retained from check.sh:457-460.
  echo
  if [ -n "$ts" ]; then
    printf "  Last check: %s (against substrate sha %s)\n" "$ts" "$last_sha"
  fi
  printf "  Current substrate HEAD: %s\n" "$sha"

  # Routing footer (per directive A6). Per-category-conditional — emitting an
  # apply.sh line for a workspace with zero DRIFTED would actively confuse
  # the operator (they'd run apply.sh, get nothing-to-apply, wonder what
  # happened). ARGUS confirmed this interpretation rev1; the directive's
  # "always emitted" means "the block always appears in non-CURRENT cases,"
  # not "every line within is unconditional."
  echo
  if [ "$n_drifted" -gt 0 ]; then
    printf "  Run apply.sh --workspace %s for drifted.\n" "$ws_abs"
  fi
  if [ "$n_missing" -gt 0 ]; then
    # Tier-branch (rev2 P2-1): project uses --project-dir; subproject uses
    # --parent-dir + --subproject (install.sh:71-78).
    case "$tier" in
      subproject)
        # Subproject workspaces deploy under <parent>/<slug>/. Derive parent
        # by stripping the trailing /<slug> segment.
        local parent_dir="${ws_abs%/${slug}}"
        printf "  Run install.sh --target subproject --parent-dir %s --subproject %s for missing.\n" \
          "$parent_dir" "$slug"
        ;;
      *)
        printf "  Run install.sh --target %s --project-dir %s for missing.\n" "$tier" "$ws_abs"
        ;;
    esac
  fi
  if [ "${#obsolete_prunable_files[@]}" -gt 0 ]; then
    case "$tier" in
      subproject)
        local parent_dir="${ws_abs%/${slug}}"
        printf "  Run install.sh --target subproject --parent-dir %s --subproject %s --prune-obsolete for obsolete (destructive — confirm).\n" \
          "$parent_dir" "$slug"
        ;;
      *)
        printf "  Run install.sh --target %s --project-dir %s --prune-obsolete for obsolete (destructive — confirm).\n" \
          "$tier" "$ws_abs"
        ;;
    esac
  fi
  if [ "${#obsolete_major_files[@]}" -gt 0 ]; then
    # MAJOR_*.md is deliberately excluded from install.sh's prune scope
    # (install.sh:60-69, 766-770: pair-programmer MAJOR ambiguity). check.sh
    # nonetheless surfaces flagged MAJORs per directive A4. Manual rm is the
    # safer path; emit a dedicated routing line so the operator isn't sent
    # to a no-op install.sh prune.
    echo "  MAJOR_*.md OBSOLETE entries require manual rm — install.sh --prune-obsolete"
    echo "  deliberately excludes MAJORs (pair-programmer agents share the directory)."
    local om2
    for om2 in "${obsolete_major_files[@]}"; do
      printf "    rm %s/%s\n" "$ws_abs" "$om2"
    done
  fi

  emit_uncommitted_warning_if_needed "$uncommitted" "$ws_abs"
fi
```

#### §4.6.9 Helper: `emit_uncommitted_warning_if_needed(<count> <ws-abs>)`

```bash
emit_uncommitted_warning_if_needed() {
  local count="$1" ws_abs="$2"
  case "$count" in
    unknown|0) return 0 ;;
  esac
  # count >= 1 — emit warning per directive A6.
  echo
  printf "  WARNING: workspace has %s uncommitted .claude/ changes. apply.sh --yes\n" "$count"
  echo   "  will auto-commit-then-overwrite; preserve the local edits via git history."
  printf "  Inspect with: cd %s && git status --short .claude/\n" "$ws_abs"
}
```

Verbatim from directive A6's warning text. The `cd <ws>` and `git status --short` invocation matches what apply.sh does internally at apply.sh:246, so the operator's exploration command parallels the tool's own check.

#### §4.6.10 State file update (line 464-465, unchanged)

`write_state_file "$ws_abs" "$sha"` stays as the last action of `check_workspace`.

### §4.7 Exit code (unchanged)

`exit 0` regardless of detected state. Drift is informational per existing comment at check.sh:18-19. Directive Phase B probe 6 verifies.

### §4.8 No changes to: argument parsing (lines 31-60), the registry-read main loop (lines 480-489), `--quiet` semantics, `--workspace` semantics, `--registry` semantics, `--help`. All preserved.

---

## §5. SKILL.md doc spec — section-by-section

Per directive A7. For each section: current state → change shape → content sketch (ADA writes the prose; this is the structural outline).

### §5.1 Output classifications table at SKILL.md:151-157

**Current:** table with rows `CURRENT`, `DRIFTED`, `NOT-STOA-DEPLOYED`, `NOT-FOUND`, `USER-TIER (out of v0 scope)`.

**Change:** **add two rows** (`MISSING`, `OBSOLETE`); **edit** the `CURRENT` and `DRIFTED` rows to reflect the new semantics (CURRENT now means "no drifts AND no missing AND no obsolete," not just "no differences among the enumerated set"); **add** a sentence on composite verdicts.

**Sketch:**

| Status | Meaning |
|---|---|
| `CURRENT` | All of: every deployed substrate file byte-equal to source-after-substitutions, no source file missing from the workspace, no workspace file at a substrate-deployable path that the source no longer ships. |
| `DRIFTED` | At least one deployed file differs. (Existing semantics — local mod vs upstream advance attribution still punted to operator's memory + `git log -- .claude/`.) |
| `MISSING` | At least one source-side file (skill, CAPTAIN, template, top-level role file) is not present at its expected deployed path. Typically: a substrate addition the workspace hasn't yet picked up. Routing: re-run `install.sh --target <tier> --project-dir <ws>` (idempotent for existing files). |
| `OBSOLETE` | At least one workspace file at a substrate-deployable path is no longer in the substrate source. Typically: a removed/renamed skill or CAPTAIN. Routing: `install.sh --target <tier> --project-dir <ws> --prune-obsolete` (destructive — confirm). MAJOR_*.md OBSOLETEs route to manual rm (install.sh deliberately excludes MAJORs from prune scope). |
| `NOT-STOA-DEPLOYED` | (unchanged) |
| `NOT-FOUND` | (unchanged) |
| `USER-TIER (out of v0 scope)` | (unchanged) |

Plus a paragraph immediately after the table:

> Verdicts compose: a workspace with both new-source-additions and locally-drifted files reads as `DRIFTED + MISSING`; all three is `DRIFTED + MISSING + OBSOLETE`. The summary line includes per-category counts and a per-workspace uncommitted-`.claude/`-state count (separately surfaced — see §uncommitted-state below).

### §5.2 "How to invoke" section at SKILL.md:62-126

**Current:** sub-sections for "Check all registered workspaces" (with example output), "Check a single workspace," "Apply updates to a workspace," "Revert the most recent apply."

**Change:** **rewrite the example output** under "Check all registered workspaces" to match the new locked format. **Insert** a new sub-section between the existing "Check all registered workspaces" and "Check a single workspace" called "What the output is telling you," documenting category routing.

Add a paragraph note before the example: "The `Last check:` line is omitted on a workspace's first check (the state file `.claude/.substrate-last-check` is not yet written) — this is informational, not an error." (rev2 P2-3.)

**Sketch — new example output (replaces SKILL.md:72-86), illustrating the rev2 per-category prefix convention:**

```
railway_stoa            DRIFTED + MISSING (3 drifted, 1 missing, 0 obsolete; 0 uncommitted)
  DRIFTED:
  - .claude/operating-disciplines.md     (+101 lines)
  - .claude/MAJOR_PLINY.md               (+12 lines)
  - .claude/MAJOR_POLYBIUS.md            (+8 lines)
  MISSING:
  + .claude/skills/credential-discipline/   (new in source)

  Last check: 2026-05-14T19:00Z (against substrate sha c37cf5a)
  Current substrate HEAD: 71ea092

  Run apply.sh --workspace /c/Users/denso/claude_projects/railway_stoa for drifted.
  Run install.sh --target project --project-dir /c/Users/denso/claude_projects/railway_stoa for missing.

ariadne-core-workspace  CURRENT (0 drifted, 0 missing, 0 obsolete; 0 uncommitted)
  Last check: 2026-05-14T19:00Z (against substrate sha 71ea092)

agent-gauntlet          NOT-STOA-DEPLOYED (no .claude/MAJOR_POLYBIUS*.md found)
```

Note the per-category line prefixes — `-` for DRIFTED, `+` for MISSING, `!` for OBSOLETE — and a SKILL.md sentence calling them out:

> The per-file lines use a distinct prefix per category (`-` drifted, `+` missing, `!` obsolete). This is structural, not cosmetic: apply.sh's `--all-differing` flag harvests only DRIFTED lines (the `-` prefix), so the prefix convention prevents apply.sh from accidentally deploying a MISSING file.

**Sketch — new sub-section "What the output is telling you":**

A short prose block summarizing: DRIFTED → apply.sh; MISSING → install.sh; OBSOLETE → install.sh --prune-obsolete (destructive); OBSOLETE MAJOR_*.md → manual rm; uncommitted-`.claude/`-state warning → resolve before any apply.sh --yes invocation (or accept the auto-commit-then-overwrite path).

### §5.3 "What this skill is NOT" section at SKILL.md:161-166

**Change:** unchanged content (directive A7 says "unchanged"; the "Not an auto-deployer" bullet still holds — Arc 26 surfaces, doesn't auto-resolve). No edit.

### §5.4 "v0 scope and limitations" section at SKILL.md:31-47

**Change:** **add one paragraph** to the existing "Other v0 simplifications, all by design (Option Small)" list (currently three bullets). New bullet:

**Sketch:**

- **No drift attribution.** When a file is `DRIFTED`, the skill does not classify *why* (local edit vs upstream advance vs both). Arc 26 closes the silent-CURRENT cliff (MISSING + OBSOLETE detection) but does not revisit Option Small's attribution gap; the operator's memory + `git log -- .claude/`  remains the canonical source for "did I change this or did upstream change this." Cross-ref the honest-gaps note in `stoa--dxw` body.

### §5.5 "How the substitution-coupling works (operational note)" section at SKILL.md:145-147

**Change:** **append** a paragraph documenting the new SKILL_NAMES live-parse coupling.

**Sketch:**

> Arc 26 added a second coupling: `check.sh` live-parses `SKILL_NAMES` from `install.sh` (around line 140) to enumerate which skills the substrate ships. The parse is `awk`-based and assumes the multi-line `SKILL_NAMES=(...)` array form. If `install.sh` ever changes the array name or moves to a non-parenthesized form, the `parse_skill_names_from_install()` function in `check.sh` must update its `awk` expression to match. The cite-comment at that function points back to the parsed `install.sh` line range; same mitigation pattern as `apply_substitutions()`. **Failure-mode symptom:** if the parser ever returns empty output for a substrate that has skills, MISSING and OBSOLETE results are untrustworthy — MISSING will under-report; OBSOLETE will over-report every deployed skill as "no longer in source." The Arc-25 silent-drift (the `credential-discipline` skill was added to `install.sh`'s array but the prior hand-maintained mirror in `check.sh` was not updated — and the bug surfaced only at an Arc-25 apply, not at any check.sh run between) motivated the live-parse choice over keeping the mirror.

### §5.6 "Daily check cadence" section at SKILL.md:128-139

**Change:** **unchanged.** Cadence semantics don't change in Arc 26.

### §5.7 "Related" section at SKILL.md:168-175

**Change:** **add** bullets pointing at this design and the Arc 26 directive.

**Sketch:**

- Arc 26 design (rev2): `agents/design/arc-26/design-rev2.md` (full-picture detection — MISSING + OBSOLETE + uncommitted state, post-ARGUS-audit revision).
- Arc 26 design (rev1): `agents/design/arc-26/design.md` (initial; kept for history).
- Arc 26 directive: `substrate/arcs/arc-26-build-directive.md`.

---

## §6. VERA probe-spec section

Restating the 7 probes from stoa--dxw / directive Phase B as executable commands or instructions, plus one new probe (Probe 8) to guard the rev2 P0-3 invariant (apply.sh harvest can NOT deploy MISSING files).

### Probe 1 — OBSOLETE detection

**Setup precondition (rev2 P2-2):** verify the test workspace is clean before running:

```bash
TEST_WS=/c/Users/denso/claude_projects/sector-4
cd "$TEST_WS"
git status --short .claude/   # must show NO uncommitted .claude/ files
                              # (other than .substrate-last-check, which is excluded)
```

If non-clean, commit/stash first; running the probe against a dirty workspace conflates Probe 1 (OBSOLETE) with Probe 3 (uncommitted).

**Probe:**

```bash
mkdir -p .claude/skills/fake-deleted
echo "# Stub skill that does not exist in substrate source" > .claude/skills/fake-deleted/SKILL.md

# Pre-existing in sector-4: CAPTAIN files with _sector_4 suffix. Stub a fake CAPTAIN matching that.
echo "stub" > .claude/agents/CAPTAIN_FAKE_sector_4.md

# Run check.sh:
cd /c/Users/denso/claude_projects/the-stoa
substrate/skills/check-substrate-updates/check.sh --workspace "$TEST_WS"

# Cleanup:
rm -rf "$TEST_WS/.claude/skills/fake-deleted" "$TEST_WS/.claude/agents/CAPTAIN_FAKE_sector_4.md"
```

**PASS criteria:**
- verdict contains `OBSOLETE` token (or composite incl. OBSOLETE)
- OBSOLETE detail block lists exactly the two stubbed paths with `  ! ` prefix
- both paths are routed under the prunable footer (`install.sh --prune-obsolete ...`) — neither is in the MAJOR-rm footer
- no false-positives flagging user-added files like `HUMAN_*.md` or `.substrate-last-check`

### Probe 2 — MISSING detection

```bash
# Temporarily add a non-existent skill name to install.sh's SKILL_NAMES.
# IMPORTANT: revert after — DO NOT commit this edit.
cd /c/Users/denso/claude_projects/the-stoa

# Edit substrate/install.sh: add a new line "  fake-new" inside SKILL_NAMES=(...)
# (between agent-author and the closing ).)

# Also create the source-side dir, OR the find-walk inside enumerate_deployed
# returns zero entries and MISSING does not trigger:
mkdir -p substrate/skills/fake-new
echo "stub" > substrate/skills/fake-new/SKILL.md

substrate/skills/check-substrate-updates/check.sh --workspace /c/Users/denso/claude_projects/sector-4

# Cleanup:
git checkout substrate/install.sh
rm -rf substrate/skills/fake-new
```

**PASS criteria:**
- verdict contains `MISSING` token
- MISSING detail block lists `.claude/skills/fake-new/SKILL.md` with `  + ` prefix and `(new in source)` annotation

### Probe 3 — Uncommitted-state detection

**Setup precondition (rev2 P2-2):** verify workspace clean before running (same as Probe 1).

```bash
TEST_WS=/c/Users/denso/claude_projects/sector-4
cd "$TEST_WS"
echo "# test edit" >> .claude/operating-disciplines.md

cd /c/Users/denso/claude_projects/the-stoa
substrate/skills/check-substrate-updates/check.sh --workspace "$TEST_WS"

# Cleanup:
cd "$TEST_WS"
git checkout .claude/operating-disciplines.md
```

**PASS criteria:**
- summary line includes `; 1 uncommitted` (or more)
- WARNING block appears below routing footer with directive A6 text and the `cd <ws> && git status --short .claude/` inspection command
- exit code 0
- the count is a clean integer (no `0\n0` malformed shape — rev2 P0-1 guard)

### Probe 4 — Routing footer

For a workspace with all three categories set, verify all routing-footer lines appear with correct `--workspace` / `--target` / `--project-dir` (or `--parent-dir`/`--subproject` at subproject tier — rev2 P2-1) values filled in.

Construct the synthetic state by combining probes 1 and 2 (OBSOLETE stub + MISSING-add) and an actual DRIFTED file (modify a deployed CAPTAIN file in the test workspace).

**PASS criteria:**
- DRIFTED line: `Run apply.sh --workspace <abs-path> for drifted.`
- MISSING line, project tier: `Run install.sh --target project --project-dir <abs-path> for missing.`
- MISSING line, subproject tier: `Run install.sh --target subproject --parent-dir <parent-abs> --subproject <slug> for missing.`
- OBSOLETE-prunable line: includes `--prune-obsolete` and `(destructive — confirm)`
- OBSOLETE-MAJOR line (if any flagged MAJORs): includes the manual-rm explanation and per-file `rm <ws>/<path>` lines

### Probe 5 — CURRENT regression

```bash
cd /c/Users/denso/claude_projects/the-stoa
substrate/skills/check-substrate-updates/check.sh
```

All three currently-registered workspaces (ariadne-core-workspace, railway_stoa, sector-4 — see `substrate/consumer-workspaces.txt`) must report `CURRENT` with all-zero counts: `CURRENT (0 drifted, 0 missing, 0 obsolete; 0 uncommitted)`.

**PASS criteria:** three CURRENT lines; exit code 0. (This probe is the runtime smoke for the awk parser per §2.3 cite: if Probe 5 fails with phantom OBSOLETE or MISSING entries on a known-current workspace, the parser is broken.)

### Probe 6 — Exit code

Every invocation in probes 1-5 (including DRIFTED + MISSING + OBSOLETE composite and the rev2 P0-1 integer-count case) must return exit code 0. Verify with `echo $?` after each.

### Probe 7 — apply.sh non-regression

```bash
# Setup a DRIFTED-only test in a throwaway dir or via sector-4. The simplest:
# modify a single deployed file in a workspace, run apply.sh, verify behavior
# matches pre-Arc-26.
TEST_WS=/c/Users/denso/claude_projects/sector-4
cd "$TEST_WS"
echo "# test drift" >> .claude/operating-disciplines.md

cd /c/Users/denso/claude_projects/the-stoa
substrate/skills/check-substrate-updates/apply.sh --workspace "$TEST_WS" --all-differing --yes

# Verify: only the one drifted file was deployed; commit message matches the
# pattern at apply.sh:390 — "chore(substrate): apply substrate updates from
# the-stoa <sha>: <files>"
```

**PASS criteria:** apply.sh output and side effects are byte-equal in shape to pre-Arc-26. Specifically: apply.sh:215-228 still successfully extracts DRIFTED paths from the new check.sh output format (the `  - ` prefix is preserved per rev2 §4.6.8).

### Probe 8 — NEW (rev2 P0-3 invariant guard): apply.sh CANNOT deploy MISSING

**Purpose:** verify the rev2 P0-3 fix structurally — apply.sh's blind harvest of `  - *` lines must NOT match the `  + *` MISSING lines, so `apply.sh --all-differing` on a DRIFTED+MISSING workspace deploys only the DRIFTED file, not the MISSING.

```bash
# Stage: a CAPTAIN file present in substrate/ but NOT yet in the test workspace.
# This makes the workspace's check.sh output flag it MISSING. (Use a real
# CAPTAIN unique to substrate that the test workspace happens not to have, OR
# temporarily move a CAPTAIN file out of the test workspace to synthesize.)
TEST_WS=/c/Users/denso/claude_projects/sector-4
cd "$TEST_WS"

# Synthesize MISSING + DRIFTED in the same workspace:
# 1) Move a deployed CAPTAIN aside (creates MISSING):
mv .claude/agents/CAPTAIN_DAEDALUS_sector_4.md /tmp/CAPTAIN_DAEDALUS_sector_4.md.bak
# 2) Edit another deployed file (creates DRIFTED):
echo "# test drift" >> .claude/operating-disciplines.md

# Run check.sh to confirm both signals are present:
cd /c/Users/denso/claude_projects/the-stoa
substrate/skills/check-substrate-updates/check.sh --workspace "$TEST_WS"
# Expect: DRIFTED + MISSING (1 drifted, 1 missing, 0 obsolete; 0 uncommitted)

# Now the invariant check — run apply.sh --all-differing:
substrate/skills/check-substrate-updates/apply.sh --workspace "$TEST_WS" --all-differing --yes

# Verify: the deployed-only operating-disciplines.md was applied; the MISSING
# CAPTAIN was NOT deployed by apply.sh — its source-side copy remains in
# substrate/ and the workspace path stays absent.
ls "$TEST_WS/.claude/agents/CAPTAIN_DAEDALUS_sector_4.md" 2>/dev/null && echo "FAIL: apply.sh deployed MISSING" || echo "PASS: MISSING not deployed"

# Cleanup:
mv /tmp/CAPTAIN_DAEDALUS_sector_4.md.bak "$TEST_WS/.claude/agents/CAPTAIN_DAEDALUS_sector_4.md"
cd "$TEST_WS"
git checkout .claude/operating-disciplines.md
# Also revert the auto-commit apply.sh made (per --yes auto-commit semantics):
git log --oneline -3
# git reset --hard HEAD~1  (if needed; PRINCIPAL-discretion — this rewrites history)
```

**PASS criteria:**
- check.sh reports DRIFTED + MISSING (both detected)
- after apply.sh --all-differing --yes: the DRIFTED file IS deployed (committed)
- after apply.sh: the MISSING CAPTAIN is STILL absent from the workspace (not deployed)
- apply.sh's exit/output names only the DRIFTED file as applied

**Failure mode this guards:** apply.sh:213-228 has no section-context awareness. If MISSING per-file lines used the same `  - ` prefix as DRIFTED (rev1 bug), apply.sh would harvest them into FILES[], reach `cp "$tmp_src" "$dep_abs"` at apply.sh:370, and silently deploy MISSING files — granting unsolicited `--add-missing` behavior, violating A8. Probe 8 is the durable VERA-time guard for the rev2 prefix-discipline fix.

---

## §7. Self-assessed weak points

Five (down from rev1's six — §7.6 IFS-join meta-commentary folded into §4.6.6 inline rationale and removed from this list per P0-2 fix). The first two are load-bearing for the gauntlet; the rest are smaller risks ADA and the verifiers should know about.

### §7.1 apply.sh harvest-loop coupling on the per-file prefix (HIGH — caught in §6 Probe 8)

**Weak point:** apply.sh:217-218 matches the literal pattern `"  - "` (two-space + dash + space) to harvest DRIFTED file paths from check.sh output. The harvest has no section-context awareness — any line with that prefix is harvested, regardless of which `DRIFTED:` / `MISSING:` / `OBSOLETE:` header it sits under. If ADA emits per-file lines for MISSING or OBSOLETE using the same `  - ` prefix (rev1 bug), apply.sh `--all-differing` on a multi-category workspace will silently deploy MISSING files via cp at apply.sh:370, granting unsolicited `--add-missing` behavior (A8 violation).

**Mitigation (rev2 P0-3 fix):** distinct per-category prefix. DRIFTED keeps `  - ` (preserves apply.sh harvest unchanged); MISSING uses `  + `; OBSOLETE uses `  ! `. apply.sh's blind `case "$line" in "  - "*) ...` matches only DRIFTED. Zero apply.sh edit; deliverable 6 honored both literally (no apply.sh code change) and semantically (no input-format change that grants new behavior). Probe 8 is the durable guard.

**Why this shape anyway:** the structural coupling between check.sh's output format and apply.sh's harvest is an existing seam (apply.sh:215 calls check.sh as a subprocess and parses its human-readable output — that's the design). The seam is preserved by keeping DRIFTED's per-file shape identical to pre-Arc-26 (`  - <path>   (<delta>)`) and isolating other categories to non-conflicting prefixes. The visual asymmetry (categories use different prefixes) is the cost; the structural property (apply.sh cannot accidentally deploy non-DRIFTED) is the benefit.

### §7.2 Removal of CAPTAIN_NAMES and TEMPLATE_NAMES arrays as "implicit per A3" (MEDIUM)

**Weak point:** directive §A3 items 2-3 say "glob substrate/CAPTAIN_*.md" and "glob substrate/templates/*.md" but do not *explicitly* say "drop the existing hard-coded mirrors at check.sh:70-90." This design takes the implicit step. ARGUS read rev1 and did not flag it as scope creep; rev2 stands on this.

**Why this shape anyway:** the existing arrays become *unreachable* once enumerate_deployed switches to globs (no remaining code references them). Leaving unreachable code is a small wart; consistent-with-§A3 cleanup is honest. Fallback (if a later auditor flags this): ADA leaves the arrays as unused-but-not-removed with a TODO comment ("unused as of Arc 26; remove in follow-up"). Either way passes the structural intent; the in-line removal saves a follow-up ticket.

### §7.3 The check.sh-to-install.sh awk parse is sensitive to install.sh's array form (LOW)

**Weak point:** the awk script in §2.3 assumes `SKILL_NAMES=(` on its own line followed by one-name-per-line followed by `)` on its own line. If install.sh ever moves SKILL_NAMES to `SKILL_NAMES=( agent-author check-substrate-updates )` (single line) or `SKILL_NAMES+=(...)` form, the parse silently returns empty.

**Why this shape anyway:** install.sh:140-144 has used the multi-line form since the skill array was introduced (verified by reading the file). The cite-comment at the function explicitly names "if install.sh changes the array name or moves to a non-parenthesized form, this function must update its awk expression to match" AND names the failure-mode symptom (rev2 P1-1: "if this awk returns empty for a substrate that has skills, the parser is broken — DO NOT trust resulting MISSING/OBSOLETE output"). Silent-empty is detectable: VERA Probe 5 (CURRENT regression on three live workspaces) would fail with phantom-OBSOLETE on every deployed skill if the parser returns empty, because every workspace skill would test as "not in source." Probe 5 is the runtime smoke; the cite is the durable mitigation.

### §7.4 `is_substrate_source_present` calls `parse_skill_names_from_install` per workspace-file — performance (LOW)

**Weak point:** Pass 2 of `check_workspace` walks every workspace file, and for each file under `.claude/skills/*/` calls `is_substrate_source_present`, which calls `parse_skill_names_from_install` (which runs awk on install.sh). This is N-files × M-awk-invocations.

**Why this shape anyway:** at typical scale (3 consumer workspaces × ~3 skills × ~3 files-per-skill ≈ 30 invocations total) the overhead is bounded — awk on a 964-line file completes in milliseconds. If scale grows past ~100 workspaces, caching `parse_skill_names_from_install` output into a script-global array at the top of `check_workspace` (once per workspace, used many times in Pass 2) is a one-liner. Not worth doing now per Option-Small simplicity.

### §7.5 MAJOR-OBSOLETE asymmetry between check.sh detection and install.sh prune (MEDIUM)

**Weak point:** directive A4 specifies `.claude/MAJOR_*.md` IS in scope for check.sh's OBSOLETE detection; install.sh:60-69, 766-770 deliberately exclude MAJORs from `--prune-obsolete`. The two scopes are now structurally asymmetric. Rev2 P0-4 fix surfaces this to the operator via the split routing footer (prunable → install.sh, MAJORs → manual rm), but the asymmetry itself is documented-not-eliminated. A future operator who reads only one of (check.sh source, install.sh source) will see a partial picture.

**Why this shape anyway:** A4 is locked. install.sh's deliberate exclusion of MAJORs from prune is also load-bearing (pair-programmer MAJOR ambiguity is a real production constraint, not a stylistic choice). The asymmetry is the honest answer: check.sh's job is to surface, install.sh's job is to act safely. The split routing footer is the bridge — operator sees both the detection (OBSOLETE flagged) and the action-shape (manual rm vs install.sh --prune-obsolete). Documented in §4.3 enumerate_workspace_substrate_paths comment block, §4.6.8 routing-footer comment, and SKILL.md §5.1 table OBSOLETE row.

---

## §8. Out of scope (in this design)

Per directive A8 hard-locked, restated for ADA's safety:

- User-tier check support (covered by stoa--bj5 — orthogonal axis).
- Auto-discovery of workspaces (Option Small ratified explicit registry).
- Four-category drift classification (locally-modified × upstream-advanced — Option Small rejected this).
- apply.sh `--add-missing` or `--remove-obsolete` (defeats Option B's preserve-the-seam intent — guarded by Probe 8).
- `consumer-workspaces.txt` format change.
- Removing the existing `apply_substitutions` cite-comment pattern (it's the model for §3).
- Touching install.sh in any way (deliverable 7).
- Touching apply.sh in any way (deliverable 6 — rev2 prefix-discipline is the structural fence).
- Verdict-line color/formatting beyond directive A6's structural shape (no ANSI codes added — keeps the output git-grep-able for any operator parsing tooling).
- Refactoring `source_path_for_deployed` or `detect_tier` beyond what's needed for the new helpers (CATO will flag any drive-by edits to these as scope creep).
- Aligning check.sh's OBSOLETE detection scope with install.sh's prune scope (i.e. excluding MAJORs from check.sh's OBSOLETE detection) — rev2 P0-4 considered this as option (c) and rejected it; A4 is locked and the asymmetry is bridged by the split routing footer.

If ADA reaches for any of the above during build, stop and surface as a peer-disagreement comment on `stoa--dxw` per directive's comms section. Do not silently expand scope.

---

## §9. Open questions / honest mismatches for ARGUS round 2

All four rev1 residual questions ARGUS resolved or confirmed in round 1; rev2 carries the resolutions:

1. **Routing-footer conditionality** (rev1 §7.2) — ARGUS confirmed per-category-conditional is correct reading of directive A6 ("always emitted" = "block always appears in non-CURRENT," not "every line unconditional"). §4.6.8 implements; no open question remaining.
2. **CAPTAIN_NAMES / TEMPLATE_NAMES array removal** (rev1 §7.3) — ARGUS did not flag as scope creep in round 1; rev2 stands on in-line removal. Carried as §7.2 weak point with fallback.
3. **CURRENT-case format change** (rev1 §9 item 3) — confirmed intentional per A6; ZENO verifies. §4.6.7 implements; no open question.
4. **Probe 2 source-side fake-skill dir** (rev1 §9 item 4) — corrected form is baked into §6 Probe 2; no open question.

**New for round 2:**

5. **MAJOR-OBSOLETE asymmetry surfacing prose** (rev2 P0-4, §7.5) — the rev2 fix splits the routing footer into prunable (install.sh) and manual-rm (MAJOR_*.md) partitions. ARGUS should read §4.6.8's emission shape and Probe 4's PASS criteria to confirm the operator-facing distinction is clear. If ARGUS reads the manual-rm footer block as too long or potentially-confusing, ADA can compress to a single line per MAJOR-OBSOLETE entry. Round 2 verdict requested on prose-shape.

6. **Probe 8 cleanup hygiene** (rev2 P0-3 guard, §6 Probe 8) — the probe synthesizes a MISSING by moving a CAPTAIN aside; cleanup restores it AND notes that apply.sh's `--yes` auto-commit creates a commit that the operator may want to `git reset --hard HEAD~1` to undo. Marked PRINCIPAL-discretion in the probe text because reset --hard is destructive. ARGUS to confirm: should the probe assume the auto-commit stays (idempotent re-application of the same change), or should the probe author script a safer revert path? Lean: leave as PRINCIPAL-discretion; VERA runs the probe interactively the first time, then any subsequent run is on a known-clean substrate.

7. **Pre-edit check.sh line numbers may shift** — rev2 cites pre-edit line numbers (e.g. check.sh:70-90 for the dropped mirrors, check.sh:265-308 for enumerate_deployed, check.sh:350-466 for check_workspace). If install.sh or check.sh has shifted between rev1's draft and ADA's build, the cited line numbers will be approximate. The function names are stable; ADA should grep-by-name when applying, not blindly trust the line range. No fix needed — flagged so CATO doesn't ding rev2 for "wrong line numbers" if a drift has occurred.
