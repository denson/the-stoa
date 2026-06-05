# Arc 26 — Substrate-update check: full-picture detection

**Design author:** Denson Smith (DAEDALUS @ the-stoa project-tier)
**Bw ticket:** `stoa--dxw`
**Directive:** `substrate/arcs/arc-26-build-directive.md` (Phase A decisions A1–A8 are LOCKED — this design implements them, does not re-deliberate)
**Files touched by ADA:** `substrate/skills/check-substrate-updates/check.sh` (extend), `substrate/skills/check-substrate-updates/SKILL.md` (doc update). Two files, one arc.

---

## §1. Intent

Today `check.sh` answers one question per workspace: "of the files I already know about (because they were enumerated from a hard-coded source-side mirror inside check.sh), do any differ from the substrate source?" That answer is correct as far as it goes — DRIFTED is detected, CURRENT means no drifts among the enumerated set — but it is silent about two structural states that matter operationally:

- **MISSING:** the substrate source has a file the workspace doesn't have at its deployed path (e.g. a new skill added to `install.sh`'s `SKILL_NAMES`, a new CAPTAIN, a new template, a new top-level role file). The Arc-25 `credential-discipline` skill is the canonical example — without an out-of-band pointer from the prior POLYBIUS ("5 files + 1 new skill"), check.sh would have reported CURRENT and the operator would have shipped three workspaces missing the new skill.
- **OBSOLETE:** the workspace has a file at a substrate-deployable path that the substrate source no longer ships (e.g. a removed skill, a renamed CAPTAIN). install.sh's `--prune-obsolete` already handles removal; check.sh has no equivalent surfacing.

Plus a third signal that is *not* a drift category but matters at apply-time: **uncommitted `.claude/` state** in the workspace's git. `apply.sh --yes` auto-commits-then-overwrites; if the local edit was intentional this is semantically destructive (recoverable through git history, but the operator should know before pressing the button).

This design extends `check.sh` to surface all three new signals alongside the existing DRIFTED behavior — without growing `apply.sh` into install.sh's territory (deliverable 6: apply.sh stays narrow), without changing `install.sh` (deliverable 7), and without disturbing the existing apply_substitutions cite-comment mitigation pattern (A8 hard-locked: don't remove it). The locked verdict tokens (CURRENT, DRIFTED, MISSING, OBSOLETE, composite) and routing footer come from directive §A6; this design fills in the structural mechanics underneath them. SKILL.md gets a parallel doc update covering classifications, invocation, the v0 limitations paragraph, and the new SKILL_NAMES coupling note.

Maps to stoa--dxw deliverables 1–7 (MISSING detection, OBSOLETE detection, uncommitted-state surfacing, output format, SKILL.md update, apply.sh unchanged, install.sh unchanged) and directive Phase A items A2 (three categories + uncommitted pre-flight), A3 (source-side enumeration), A4 (OBSOLETE scope), A5 (uncommitted detection), A6 (output format), A7 (SKILL.md scope).

---

## §2. Sub-decision A3 — SKILL_NAMES parsing mechanism

### §2.1 Resolution: **Option A — shell extraction via sed/awk from install.sh.** Replace the hard-coded `SKILL_NAMES` mirror at `check.sh:92-95`. Keep the `CAPTAIN_NAMES` (lines 70-81) and `TEMPLATE_NAMES` (lines 83-90) mirrors **only as fallback ground-truth for the parsed values to validate against** (see §2.4).

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

ARGUS will read this section for execution-side-effects risk; the answer is: shell extraction has none, sourcing has a tractable-but-real surface. Pick the safer option.

The shell extraction is small and targeted:

```bash
# parse_skill_names_from_install: echo one name per line.
# Reads substrate/install.sh and extracts the SKILL_NAMES=(...) array contents.
# CITE: parses install.sh:140-144 (SKILL_NAMES array). If install.sh changes
# the array name or moves to a non-parenthesized form, this function must
# update its sed expression to match. The previous hand-maintained mirror
# at check.sh:92-95 silently drifted in Arc 25 (credential-discipline added
# to install.sh, not to mirror); this live-parse closes that drift surface.
parse_skill_names_from_install() {
  local install_sh="${SUBSTRATE_DIR}/install.sh"
  [ -f "$install_sh" ] || return 1
  # awk: print every line strictly between 'SKILL_NAMES=(' and the next ')',
  # stripping whitespace and skipping blanks/comments. Multi-line array form
  # is the only form install.sh uses (verified install.sh:140-144).
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
Failure mode: empty stdout if install.sh missing or array empty/unrecognized form. The caller treats empty as "no skills enumerated" and the existing CURRENT/DRIFTED logic continues to function — no crash, no false positive.

### §2.4 Reconciliation with the surviving CAPTAIN_NAMES and TEMPLATE_NAMES mirrors

The directive does not require live-parsing CAPTAINs or templates — the source-side enumeration for those uses globs (A3 items 2 and 3: `glob substrate/CAPTAIN_*.md` and `glob substrate/templates/*.md`), which is structurally cleaner than parsing install.sh.

**Decision:** for CAPTAINs and templates, use globs against `substrate/`. Drop the existing `CAPTAIN_NAMES` and `TEMPLATE_NAMES` mirrors at `check.sh:70-90` entirely — they become unused once `enumerate_deployed()` is reworked (see §4.2).

This is consistent: the mirror approach is replaced everywhere it would be vulnerable to install.sh drift. The result is **zero hand-maintained mirrors of install.sh enumerations inside check.sh** — every source-side set is either glob-derived (CAPTAINs, templates, MAJORs, operating-disciplines) or parsed-from-install.sh (skills). The cite-comment at `check.sh:64-68` is removed by the same edit that drops the arrays; the new cite-comment at `parse_skill_names_from_install` replaces it.

The honest mismatch with the directive: directive §A3 item 1 says "parse SKILL_NAMES from `substrate/install.sh`," items 2-3 say "glob `substrate/CAPTAIN_*.md`" and "glob `substrate/templates/*.md`" — these are the live-discovery instructions and they are clear. Items 2-3 *implicitly* deprecate the CAPTAIN/TEMPLATE mirrors at check.sh:70-90 (otherwise why glob); making the deprecation explicit in this design avoids ADA leaving the now-unused arrays in place as "defensive duplication." If ARGUS reads this as scope creep beyond directive §A3, the fallback is: keep the mirrors as unused-but-not-removed, ADA flags them with a comment, follow-up arc removes. Either way passes the structural intent.

---

## §3. Cite-comment policy

The cite-comment-at-the-read-site pattern (precedent: `apply_substitutions()` block at `check.sh:106-115`) is preserved verbatim for placeholder-substitution coupling. Arc 26 adds **one new cite site**: `parse_skill_names_from_install()` (see §2.3 for full text). Required structural shape, mirroring the precedent:

1. **Function-leading comment block** identifying the source file and the specific line numbers parsed (`install.sh:140-144` as of substrate HEAD at design-write time — the comment cites a line range, not a SHA; if the line numbers shift due to upstream install.sh edits the cite drifts but stays directionally correct, and a `grep -n "^SKILL_NAMES" install.sh` rediscovers ground truth instantly).
2. **Coupling-named explicitly:** "if install.sh changes the array name or moves to a non-parenthesized form, this function must update its sed/awk expression to match." Same shape as the existing `apply_substitutions` cite-comment.
3. **Evidence of why the cite matters,** referencing the Arc 25 silent-drift (see §2.2 above) so a future reader understands *why* the live-parse exists and what failure mode it closes.

CATO will read for: (a) the cite-comment is present at every install.sh parse site (currently only one: the new `parse_skill_names_from_install`); (b) the cite includes line numbers, not just "see install.sh"; (c) the explicit-coupling sentence is there; (d) the existing `apply_substitutions` cite-comment at `check.sh:106-115` is unchanged (A8 hard-locked).

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
for capf in "${SUBSTRATE_DIR}/CAPTAIN_"*.md; do
  [ -f "$capf" ] || continue
  cap_base="$(basename "$capf" .md)"  # "CAPTAIN_DAEDALUS"
  cap_base="${cap_base#CAPTAIN_}"      # "DAEDALUS"
  echo ".claude/agents/CAPTAIN_${cap_base}${suffix}.md"
done
```

- **Templates (lines 294-296):** replace `for tn in "${TEMPLATE_NAMES[@]}"` with a glob over `substrate/templates/*.md` (or `*` if non-`.md` templates ever ship; today they're all `.md`). Use the same shape: glob, basename, emit deployed path.
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

  # MAJORs and operating-disciplines: emit only if present, since we don't
  # want to double-count with enumerate_deployed (which already enumerates
  # the expected MAJOR paths). The OBSOLETE flow asks "is this present
  # workspace file substrate-derived?"; an absent expected MAJOR is a
  # MISSING, not an OBSOLETE.
  local f
  for f in "${ws}/.claude/MAJOR_"*.md; do
    [ -f "$f" ] || continue
    echo ".claude/$(basename "$f")"
  done
  if [ -f "${ws}/.claude/operating-disciplines.md" ]; then
    echo ".claude/operating-disciplines.md"
  fi

  # CAPTAINs: glob workspace dir.
  if [ -d "${ws}/.claude/agents" ]; then
    for f in "${ws}/.claude/agents/CAPTAIN_"*.md; do
      [ -f "$f" ] || continue
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
      [ -d "$d" ] || continue
      echo ".claude/skills/$(basename "$d")/"
    done
  fi
}
```

**Files explicitly NOT enumerated (per A4):**

- `.claude/.substrate-last-check` — transient state file, written by `write_state_file()` at `check.sh:327-337`. Per directive A5 it's excluded from the uncommitted-state count too.
- `.claude/.substrate-backups/...` — apply.sh's pre-deploy backup tree (see apply.sh:264-269), not substrate-derived.
- `HUMAN_*.md` instruction files — user-added per directive A4.
- `.claude/agents/` files NOT matching the `CAPTAIN_*.md` pattern — user-added custom agents (e.g. a pair-programmer agent the operator dropped in).
- `.claude/skills/` files outside top-level subdirectories — the directive scopes skills to directory-level. A loose file directly under `.claude/skills/` (rare; not deployed by install.sh) is not flagged.

**Important precedent for the no-MAJOR-prune scope:** install.sh's prune logic at `install.sh:767-770` *deliberately excludes* MAJOR_*.md files from obsolete detection because "pair-programmer Majors (PYTHAGORAS, ATTICUS, etc.) land in the same directory and cannot be reliably distinguished from substrate-canonical MAJORs by filename." Directive A4 specifies `.claude/MAJOR_*.md` is in scope for OBSOLETE detection — this is a deliberate divergence from install.sh's conservatism (check.sh is informational and surfaces, install.sh's prune is destructive). The asymmetry is acceptable because check.sh OBSOLETE is FYI (operator decides whether to run `install.sh --prune-obsolete`, and install.sh's stricter scope means the actual prune leaves the pair-programmer MAJOR alone even if check.sh flagged it). **ARGUS will probably surface this asymmetry — the design's answer is: surfacing more is safe; pruning more would not be. The routing footer points the operator at `install.sh --prune-obsolete` which has the stricter scope.**

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

### §4.5 New helper: `uncommitted_claude_count(<ws>)` — for A5

**Purpose:** count uncommitted `.claude/` files in the workspace, excluding the transient state file. Per directive A5.

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
# Sibling-not-shared with apply.sh's git_uncommitted_claude (apply.sh:184-189)
# — apply.sh returns the file LIST (multi-line for display); check.sh needs
# only the COUNT (for the summary line). Inlined per the design §9.2 note
# in apply.sh:74 ("shared shape with check.sh; inlined per design §9.2").
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
  # Count porcelain lines, excluding .substrate-last-check.
  git -C "$ws" status --porcelain -- .claude 2>/dev/null \
    | grep -v '\.substrate-last-check$' \
    | grep -c . || echo 0
}
```

The `grep -c . || echo 0` idiom handles the empty-stdout case (grep returns exit 1 on no match, which would trip `set -e`; the `|| echo 0` defangs it). Verified pattern; same shape as elsewhere in the script.

### §4.6 Modified: `check_workspace(<ws-input>)` at `check.sh:350-466`

This is the orchestration function; it gets the most structural change. New variables, new detection passes, new emission. Walking the post-edit shape top-to-bottom:

#### §4.6.1 Setup (lines 351-380, unchanged)

`ws_abs`, `label`, `tier`/`slug` detection, the NOT-FOUND / NOT-STOA-DEPLOYED / USER-TIER early returns stay byte-equal.

#### §4.6.2 Detection-pass arrays (replacing the existing `differs_files` / `differs_deltas` / `current_count` / `missing_count` / `total` setup at lines 383-387)

Replace with:

```bash
local drifted_files=()        # was differs_files
local drifted_deltas=()       # was differs_deltas
local missing_files=()        # NEW — populated by the existing-but-now-surfaced detection
local obsolete_files=()       # NEW
local current_count=0
local total=0
```

The renaming `differs` → `drifted` is for output-format consistency with the locked verdict token `DRIFTED`. Internal-only rename; no external interface depends on it (apply.sh harvests deployed paths from the human-readable output, not from variable names).

#### §4.6.3 Pass 1 — DRIFTED + MISSING (extends the existing loop at lines 389-435)

The existing `while IFS= read -r dep; do ... done < <(enumerate_deployed ...)` loop is the right place for both DRIFTED and MISSING — it already iterates the expected-deployed set, already checks `[ ! -f "$deployed_path" ]`, and already counts `missing_count` (which is currently dead). Extending it to *surface* MISSING is a small change:

- At the existing `[ ! -f "$deployed_path" ]` test (line 394): instead of incrementing the dead `missing_count`, append to `missing_files` and `continue`. The reason needs to be "new in source" not just "absent" — but for v0 this is fine, since the source-side enumeration is what generated `dep` (the file is in install.sh's SKILL_NAMES or in `substrate/CAPTAIN_*.md` or in `substrate/templates/*.md` — its presence in the source set IS the "in source" part of the definition).
- The existing `source-removed` sentinel at lines 405-410 — when the source file is *gone* despite being enumerated as an expected deployed — is **a category-error case under the new model**. With the new live-parsing enumeration, this case is now impossible for skills (parse_skill_names_from_install only emits names whose source exists) and very rare for CAPTAINs/templates/MAJORs (since enumerate_deployed now globs the source side directly). If it ever does happen — racing-edit during a substrate-update where install.sh's SKILL_NAMES references a skill directory that was just deleted from `substrate/skills/` — the right surfacing is OBSOLETE-of-the-deployed-workspace-file. Decision: in the `[ ! -f "$src_abs" ]` branch, append to `obsolete_files` instead of `differs_files`. This deduplicates with Pass 2 (§4.6.4) naturally: Pass 2 enumerates the workspace's deployed files and asks "is the source still present?" If the answer is no, we get OBSOLETE — the same answer Pass 1 would now produce for the same file. Either pass will catch it; the union is the same set. To avoid double-emission, Pass 2 should skip any file already in `obsolete_files`.

#### §4.6.4 Pass 2 — OBSOLETE (new)

After Pass 1 completes, walk the workspace-side enumeration:

```bash
local ws_dep
while IFS= read -r ws_dep; do
  [ -n "$ws_dep" ] || continue
  # Skip if Pass 1 already flagged this as obsolete (deduplication).
  local already_obsolete=0
  local of
  for of in "${obsolete_files[@]:-}"; do
    [ "$of" = "$ws_dep" ] && { already_obsolete=1; break; }
  done
  [ "$already_obsolete" -eq 1 ] && continue

  if ! is_substrate_source_present "$ws_dep" "$tier" "$slug"; then
    obsolete_files+=("$ws_dep")
  fi
done < <(enumerate_workspace_substrate_paths "$ws_abs" "$tier" "$slug")
```

The deduplication-against-Pass-1 prevents double-reporting in the racing-edit edge case. For all non-edge-case workflows, Pass 1's `obsolete_files` is empty and Pass 2 is the sole populator.

#### §4.6.5 Pass 3 — uncommitted (new, single call)

```bash
local uncommitted
uncommitted="$(uncommitted_claude_count "$ws_abs")"
```

`$uncommitted` is either an integer or the literal `unknown`.

#### §4.6.6 Verdict computation (replacing lines 445-447)

```bash
local n_drifted=${#drifted_files[@]}
local n_missing=${#missing_files[@]}
local n_obsolete=${#obsolete_files[@]}
local verdict_parts=()
local verdict

if [ "$n_drifted" -eq 0 ] && [ "$n_missing" -eq 0 ] && [ "$n_obsolete" -eq 0 ]; then
  verdict="CURRENT"
else
  [ "$n_drifted"  -gt 0 ] && verdict_parts+=("DRIFTED")
  [ "$n_missing"  -gt 0 ] && verdict_parts+=("MISSING")
  [ "$n_obsolete" -gt 0 ] && verdict_parts+=("OBSOLETE")
  # Join with " + " (locked composite form per directive A6).
  verdict="$(IFS=' + '; echo "${verdict_parts[*]}")"
fi
```

The `IFS=' + '` join with `echo "${verdict_parts[*]}"` is a known bash idiom; produces `DRIFTED + MISSING` for two-element, `DRIFTED + MISSING + OBSOLETE` for three-element, single-token for one-element. Token order matches directive A6: drifted, missing, obsolete.

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

Note: per directive A6 the format string says `<verdict> (<N> drifted, <M> missing, <K> obsolete; <U> uncommitted)` — CURRENT case includes the all-zeros explicit form rather than the existing "all N deployed files match" prose. This is the locked structural shape; the prose is replaced.

#### §4.6.8 Emission — non-CURRENT case (replacing lines 451-462)

```bash
else
  printf "%-40s %s (%d drifted, %d missing, %d obsolete%s)\n" \
    "$label" "$verdict" "$n_drifted" "$n_missing" "$n_obsolete" "$uncommitted_suffix"

  # Per-category detail blocks (only for non-zero categories).
  if [ "$n_drifted" -gt 0 ]; then
    echo "  DRIFTED:"
    local i
    for ((i=0; i<n_drifted; i++)); do
      printf "    - %-50s (%s)\n" "${drifted_files[$i]}" "${drifted_deltas[$i]}"
    done
  fi
  if [ "$n_missing" -gt 0 ]; then
    echo "  MISSING:"
    local m
    for m in "${missing_files[@]}"; do
      printf "    - %-50s (new in source)\n" "$m"
    done
  fi
  if [ "$n_obsolete" -gt 0 ]; then
    echo "  OBSOLETE:"
    local o
    for o in "${obsolete_files[@]}"; do
      printf "    - %-50s (dropped from source)\n" "$o"
    done
  fi

  # Pre-existing state-info lines, retained from check.sh:457-460.
  echo
  if [ -n "$ts" ]; then
    printf "  Last check: %s (against substrate sha %s)\n" "$ts" "$last_sha"
  fi
  printf "  Current substrate HEAD: %s\n" "$sha"

  # Routing footer (per directive A6). Only the lines for non-zero categories
  # are emitted; this is implicit in the directive ("always emitted for
  # non-CURRENT workspaces" — but emitting an apply.sh suggestion for a
  # MISSING-only workspace is operator-confusing). Conditional per-category.
  echo
  local tier_arg="$tier"  # "project" or "subproject" — install.sh --target value
  if [ "$n_drifted" -gt 0 ]; then
    printf "  Run apply.sh --workspace %s for drifted.\n" "$ws_abs"
  fi
  if [ "$n_missing" -gt 0 ]; then
    printf "  Run install.sh --target %s --project-dir %s for missing.\n" "$tier_arg" "$ws_abs"
  fi
  if [ "$n_obsolete" -gt 0 ]; then
    printf "  Run install.sh --target %s --project-dir %s --prune-obsolete for obsolete (destructive — confirm).\n" "$tier_arg" "$ws_abs"
  fi

  emit_uncommitted_warning_if_needed "$uncommitted" "$ws_abs"
fi
```

**Design choice on routing footer conditionality:** the directive A6 phrasing "Routing footer (always emitted for non-CURRENT workspaces)" reads as "always emit the whole routing block." Reading the block contents, emitting an apply.sh line when there's no DRIFTED would actively confuse the operator (they'd run apply.sh and get nothing-to-apply). I interpret "always emitted" as "the routing footer block always appears in non-CURRENT cases," and the per-category-conditional lines within it are the only sensible reading. CATO will read this; if the literal directive interpretation is intended, ADA flips the conditionals. **Honest mismatch flagged.**

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

Verbatim from directive A6's warning text (one minor wording adjustment: the directive's "preserve the local edits via git history" is preserved as-is; readers should understand that the auto-committed pre-state is preserved as a recoverable git commit, not lost). The `cd <ws>` and `git status --short` invocation matches what apply.sh does internally at apply.sh:246, so the operator's exploration command parallels the tool's own check.

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
| `OBSOLETE` | At least one workspace file at a substrate-deployable path is no longer in the substrate source. Typically: a removed/renamed skill or CAPTAIN. Routing: `install.sh --target <tier> --project-dir <ws> --prune-obsolete` (destructive — confirm). |
| `NOT-STOA-DEPLOYED` | (unchanged) |
| `NOT-FOUND` | (unchanged) |
| `USER-TIER (out of v0 scope)` | (unchanged) |

Plus a paragraph immediately after the table:

> Verdicts compose: a workspace with both new-source-additions and locally-drifted files reads as `DRIFTED + MISSING`; all three is `DRIFTED + MISSING + OBSOLETE`. The summary line includes per-category counts and a per-workspace uncommitted-`.claude/`-state count (separately surfaced — see §uncommitted-state below).

### §5.2 "How to invoke" section at SKILL.md:62-126

**Current:** sub-sections for "Check all registered workspaces" (with example output), "Check a single workspace," "Apply updates to a workspace," "Revert the most recent apply."

**Change:** **rewrite the example output** under "Check all registered workspaces" to match the new locked format. **Insert** a new sub-section between the existing "Check all registered workspaces" and "Check a single workspace" called "What the output is telling you," documenting category routing.

**Sketch — new example output (replaces SKILL.md:72-86):**

```
railway_stoa            DRIFTED + MISSING (3 drifted, 1 missing, 0 obsolete; 0 uncommitted)
  DRIFTED:
    - .claude/operating-disciplines.md     (+101 lines)
    - .claude/MAJOR_PLINY.md               (+12 lines)
    - .claude/MAJOR_POLYBIUS.md            (+8 lines)
  MISSING:
    - .claude/skills/credential-discipline/   (new in source)

  Last check: 2026-05-14T19:00Z (against substrate sha c37cf5a)
  Current substrate HEAD: 71ea092

  Run apply.sh --workspace /c/Users/denso/claude_projects/railway_stoa for drifted.
  Run install.sh --target project --project-dir /c/Users/denso/claude_projects/railway_stoa for missing.

ariadne-core-workspace  CURRENT (0 drifted, 0 missing, 0 obsolete; 0 uncommitted)
  Last check: 2026-05-14T19:00Z (against substrate sha 71ea092)

agent-gauntlet          NOT-STOA-DEPLOYED (no .claude/MAJOR_POLYBIUS*.md found)
```

**Sketch — new sub-section "What the output is telling you":**

A short prose block summarizing: DRIFTED → apply.sh; MISSING → install.sh; OBSOLETE → install.sh --prune-obsolete (destructive); uncommitted-`.claude/`-state warning → resolve before any apply.sh --yes invocation (or accept the auto-commit-then-overwrite path).

### §5.3 "What this skill is NOT" section at SKILL.md:161-166

**Change:** unchanged content (directive A7 says "unchanged"; the "Not an auto-deployer" bullet still holds — Arc 26 surfaces, doesn't auto-resolve). No edit.

### §5.4 "v0 scope and limitations" section at SKILL.md:31-47

**Change:** **add one paragraph** to the existing "Other v0 simplifications, all by design (Option Small)" list (currently three bullets). New bullet:

**Sketch:**

- **No drift attribution.** When a file is `DRIFTED`, the skill does not classify *why* (local edit vs upstream advance vs both). Arc 26 closes the silent-CURRENT cliff (MISSING + OBSOLETE detection) but does not revisit Option Small's attribution gap; the operator's memory + `git log -- .claude/` remains the canonical source for "did I change this or did upstream change this." Cross-ref the honest-gaps note in `stoa--dxw` body.

### §5.5 "How the substitution-coupling works (operational note)" section at SKILL.md:145-147

**Change:** **append** a paragraph documenting the new SKILL_NAMES live-parse coupling.

**Sketch:**

> Arc 26 added a second coupling: `check.sh` live-parses `SKILL_NAMES` from `install.sh` (around line 140) to enumerate which skills the substrate ships. The parse is `awk`-based and assumes the multi-line `SKILL_NAMES=(...)` array form. If `install.sh` ever changes the array name or moves to a non-parenthesized form, the `parse_skill_names_from_install()` function in `check.sh` must update its `awk` expression to match. The cite-comment at that function points back to the parsed `install.sh` line range; same mitigation pattern as `apply_substitutions()`. The Arc-25 silent-drift (the `credential-discipline` skill was added to `install.sh`'s array but the prior hand-maintained mirror in `check.sh` was not updated — and the bug surfaced only at an Arc-25 apply, not at any check.sh run between) motivated the live-parse choice over keeping the mirror.

### §5.6 "Daily check cadence" section at SKILL.md:128-139

**Change:** **unchanged.** Cadence semantics don't change in Arc 26.

### §5.7 "Related" section at SKILL.md:168-175

**Change:** **add** a bullet pointing at this design and the Arc 26 directive.

**Sketch:**

- Arc 26 design: `agents/design/arc-26/design.md` (full-picture detection — MISSING + OBSOLETE + uncommitted state).
- Arc 26 directive: `substrate/arcs/arc-26-build-directive.md`.

---

## §6. VERA probe-spec section

Restating the 7 probes from stoa--dxw / directive Phase B as executable commands or instructions. VERA reads this as her probe set.

### Probe 1 — OBSOLETE detection

```bash
# Setup: pick a throwaway test workspace clone. The-stoa itself does NOT have
# .claude/ deployed (it's the substrate source, not a consumer), so use one
# of the existing consumer workspaces to a temporary copy or use a sandbox.
# Example using sector-4:
TEST_WS=/c/Users/denso/claude_projects/sector-4
cd "$TEST_WS"
mkdir -p .claude/skills/fake-deleted
echo "# Stub skill that does not exist in substrate source" > .claude/skills/fake-deleted/SKILL.md

# Pre-existing in sector-4: CAPTAIN files with _sector_4 suffix. Stub a fake CAPTAIN matching that.
echo "stub" > .claude/agents/CAPTAIN_FAKE_sector_4.md

# Run check.sh:
cd /c/Users/denso/claude_projects/the-stoa
substrate/skills/check-substrate-updates/check.sh --workspace "$TEST_WS"

# Expected: verdict includes OBSOLETE; per-category block lists both
# .claude/skills/fake-deleted/ and .claude/agents/CAPTAIN_FAKE_sector_4.md
# under OBSOLETE.

# Cleanup:
rm -rf "$TEST_WS/.claude/skills/fake-deleted" "$TEST_WS/.claude/agents/CAPTAIN_FAKE_sector_4.md"
```

PASS criteria: verdict contains `OBSOLETE` token; OBSOLETE detail block lists exactly the two stubbed paths (no false-positives flagging user-added files like `HUMAN_*.md` or `.substrate-last-check`).

### Probe 2 — MISSING detection

```bash
# Temporarily add a non-existent skill name to install.sh's SKILL_NAMES.
# IMPORTANT: revert after — DO NOT commit this edit.
cd /c/Users/denso/claude_projects/the-stoa
# Edit substrate/install.sh, add a new line "  fake-new" between agent-author and the closing ).
# (Manually with editor, or with sed for the test.)

substrate/skills/check-substrate-updates/check.sh --workspace /c/Users/denso/claude_projects/sector-4

# Expected: verdict includes MISSING; per-category block lists
# .claude/skills/fake-new/<file>(s) under MISSING (one entry per file that
# would be enumerated under substrate/skills/fake-new/ — but since fake-new
# doesn't exist as a substrate source dir, enumerate_deployed's find will
# emit zero entries, so the count is 0 and MISSING does not trigger).

# CORRECTION: this probe needs a substrate-side fake skill DIR too. Modify:
mkdir -p substrate/skills/fake-new
echo "stub" > substrate/skills/fake-new/SKILL.md
# Then re-run check.sh as above; expected: MISSING block lists
# .claude/skills/fake-new/SKILL.md.

# Cleanup:
git checkout substrate/install.sh
rm -rf substrate/skills/fake-new
```

PASS criteria: verdict contains `MISSING` token; MISSING detail block lists `.claude/skills/fake-new/SKILL.md` with annotation `(new in source)`.

**Honest probe correction noted above** — the original probe text "temporarily add a non-existent skill name to SKILL_NAMES" elides that the source dir must also exist for the find-walk inside enumerate_deployed to emit anything. VERA should run the corrected form.

### Probe 3 — Uncommitted-state detection

```bash
TEST_WS=/c/Users/denso/claude_projects/sector-4
cd "$TEST_WS"
echo "# test edit" >> .claude/operating-disciplines.md

cd /c/Users/denso/claude_projects/the-stoa
substrate/skills/check-substrate-updates/check.sh --workspace "$TEST_WS"

# Expected: summary line includes "; 1 uncommitted" (or more); WARNING
# block appears below routing footer with the directive A6 text and the
# `cd <ws> && git status --short .claude/` inspection command.

# Cleanup:
cd "$TEST_WS"
git checkout .claude/operating-disciplines.md
```

PASS criteria: summary line shows the count; warning block is emitted; exit code 0.

### Probe 4 — Routing footer

For a workspace with all three categories set, verify all three routing-footer lines appear with correct `--workspace` / `--target` / `--project-dir` values filled in. Construct the synthetic state by combining probes 1 and 2 (OBSOLETE stub + MISSING-add) and an actual DRIFTED file (e.g. modify a deployed CAPTAIN file in the test workspace).

PASS criteria: all three lines emitted (`apply.sh --workspace ...`, `install.sh --target project --project-dir ... for missing`, `install.sh --target project --project-dir ... --prune-obsolete for obsolete (destructive — confirm)`). Workspace path is the absolute resolved path, not a relative.

### Probe 5 — CURRENT regression

```bash
cd /c/Users/denso/claude_projects/the-stoa
substrate/skills/check-substrate-updates/check.sh
```

All three currently-registered workspaces (ariadne-core-workspace, railway_stoa, sector-4 — see `substrate/consumer-workspaces.txt`) must report `CURRENT` with all-zero counts: `CURRENT (0 drifted, 0 missing, 0 obsolete; 0 uncommitted)`. Per directive Phase B probe 5 — no false positives.

PASS criteria: three CURRENT lines; exit code 0.

### Probe 6 — Exit code

Every invocation in probes 1-5 (including the DRIFTED + MISSING + OBSOLETE composite) must return exit code 0. Verify with `echo $?` after each.

### Probe 7 — apply.sh non-regression

```bash
# Setup a DRIFTED-only test in a throwaway dir or via sector-4. The simplest:
# modify a single deployed file in a workspace, run apply.sh, verify behavior
# matches pre-Arc-26.
# Compare apply.sh output and resulting commit message against the pattern at
# apply.sh:390 — "chore(substrate): apply substrate updates from the-stoa <sha>: <files>"
```

PASS criteria: apply.sh output and side effects are byte-equal in shape to pre-Arc-26 (the only allowed change is that apply.sh:215's `check_out="$("${SCRIPT_DIR}/check.sh" --workspace "$WORKSPACE" 2>/dev/null || true)"` and the line-parsing at 216-228 still successfully extract DRIFTED paths from the new check.sh output format).

**Important sub-check:** apply.sh:217 specifically matches output lines beginning with `"  - "` (two-space indent + dash + space). The new check.sh output format uses **four-space indent** under the `DRIFTED:` header: `    - <path>     (<delta> lines)`. **This will break apply.sh's harvest loop.** Either: (a) the new check.sh format uses two-space indent for the per-file lines (matching the existing format precisely — keep `  - `), OR (b) apply.sh's harvest loop accepts both two-space and four-space prefixes. Recommend (a): use two-space indent (`  - <path>`) for the per-file lines inside the per-category blocks. The category header (`DRIFTED:`, `MISSING:`, `OBSOLETE:`) sits at two-space indent (matching directive A6's per-category-block visual nesting), and the per-file lines sit at the same two-space indent for the `- <path>` form. **Adjust the §4.6.8 emission accordingly:** use `"  - %-50s (%s)\n"` not `"    - %-50s (%s)\n"`. This preserves apply.sh non-regression. ARGUS and CATO will both want to verify this.

---

## §7. Self-assessed weak points

Six. The first two are load-bearing for the gauntlet; the rest are smaller risks ADA and the verifiers should know about.

### §7.1 apply.sh harvest-loop coupling on the per-file indentation (HIGH — caught in §6 Probe 7)

**Weak point:** apply.sh:217 matches the literal pattern `"  - "` (two-space indent + dash + space) to harvest DRIFTED file paths from check.sh output. Per-category-block nesting under `DRIFTED:` looks visually like it wants four-space indent for the per-file lines. **If ADA emits four-space-indented per-file lines, apply.sh --all-differing breaks silently** — it produces "no DIFFERS files in check.sh output" and exits with nothing applied, even though check.sh correctly reports DRIFTED.

**Mitigation:** §6 Probe 7 calls this out; §4.6.8 specifies two-space indent (`"  - %-50s (%s)\n"`). The per-category block headers (`DRIFTED:`, `MISSING:`, `OBSOLETE:`) sit at two-space indent and the per-file lines under them ALSO sit at two-space indent — visually less-nested than a strict four-space would be, but **machine-compatible with apply.sh's existing harvest pattern.** The alternative (extending apply.sh's harvest loop to accept both two-space and four-space) would touch apply.sh, violating deliverable 6 (apply.sh unchanged in behavior). Two-space wins.

**Why this shape anyway:** the structural coupling between check.sh's output format and apply.sh's harvest is an existing seam (apply.sh:215 calls check.sh as a subprocess and parses its human-readable output — that's the design). The seam is preserved by keeping the per-file line shape identical. CATO will read for this; if CATO surfaces "the visual nesting under DRIFTED: header should be four-space," the answer is: the seam is load-bearing, the visual is aesthetic, the seam wins.

### §7.2 Routing-footer conditionality vs the directive's "always emitted" wording (MEDIUM — flagged §4.6.8)

**Weak point:** directive A6 says "Routing footer (always emitted for non-CURRENT workspaces)" with three lines (apply.sh, install.sh, install.sh --prune-obsolete). Literal reading: emit all three regardless of which categories are non-empty. My interpretation: emit only the lines for non-zero categories. If ARGUS reads the directive literally and disagrees, the design loses one round.

**Why this shape anyway:** emitting `Run apply.sh --workspace <ws> for drifted.` on a workspace with zero drifted files actively confuses the operator (they run apply.sh, get nothing-to-apply, wonder what just happened). The directive's intent (from the surrounding context and the ticket body's deliverable 4) is operator-routing, and operator-routing wants conditional. If ARGUS insists on literal, ADA flips three `if` blocks to unconditional emission — small change.

### §7.3 Removal of CAPTAIN_NAMES and TEMPLATE_NAMES arrays as "implicit per A3" (MEDIUM)

**Weak point:** directive §A3 items 2-3 say "glob substrate/CAPTAIN_*.md" and "glob substrate/templates/*.md" but do not *explicitly* say "drop the existing hard-coded mirrors at check.sh:70-90." This design takes the implicit step. If ARGUS reads this as scope creep beyond the directive, the design loses.

**Why this shape anyway:** the existing arrays become *unreachable* once enumerate_deployed switches to globs (no remaining code references them). Leaving unreachable code is a small wart; consistent-with-§A3 cleanup is honest. Fallback: ADA leaves the arrays as unused-but-not-removed with a TODO comment ("unused as of Arc 26; remove in follow-up"), and a follow-up arc removes them. Either way passes the structural intent; the in-line removal saves a follow-up ticket.

### §7.4 The check.sh-to-install.sh awk parse is sensitive to install.sh's array form (LOW)

**Weak point:** the awk script in §2.3 assumes `SKILL_NAMES=(` on its own line followed by one-name-per-line followed by `)` on its own line. If install.sh ever moves SKILL_NAMES to `SKILL_NAMES=( agent-author check-substrate-updates )` (single line) or `SKILL_NAMES+=(...)` form, the parse silently returns empty.

**Why this shape anyway:** install.sh:140-144 has used the multi-line form since the skill array was introduced (verified by reading the file). The cite-comment at the function explicitly names "the multi-line array form is the only form install.sh uses (verified install.sh:140-144)" so a future install.sh-editor sees the coupling. Silent-empty is the correct fallback: the existing CURRENT/DRIFTED logic for non-skill categories continues to function (it doesn't depend on the SKILL list at all), and a sanity-check at VERA time (Probe 2) would catch the form-change. Mitigations beyond cite-comment would require parsing bash AST (no).

### §7.5 The `is_substrate_source_present` skill check calls `parse_skill_names_from_install` per workspace-file — performance (LOW)

**Weak point:** Pass 2 of `check_workspace` walks every workspace file, and for each file under `.claude/skills/*/` calls `is_substrate_source_present`, which calls `parse_skill_names_from_install` (which runs awk on install.sh). This is N-files × M-awk-invocations.

**Why this shape anyway:** at typical scale (3 consumer workspaces × ~3 skills × ~3 files-per-skill ≈ 30 invocations total) the overhead is bounded — awk on a 964-line file completes in milliseconds. If scale grows past ~100 workspaces, caching `parse_skill_names_from_install` output into a script-global array at the top of `check_workspace` (once per workspace, used many times in Pass 2) is a one-liner. Not worth doing now per Option-Small simplicity.

### §7.6 The composite-verdict join idiom `IFS=' + '; echo "${verdict_parts[*]}"` is bash-only (LOW)

**Weak point:** `IFS=' + '` (multi-char IFS) behavior in `${arr[*]}` join uses **only the first character of IFS** as separator. The join produces `DRIFTED MISSING OBSOLETE` not `DRIFTED + MISSING + OBSOLETE`.

**Mitigation in the actual code (§4.6.6) — the idiom must be written differently.** The correct shape:

```bash
local verdict
case "${#verdict_parts[@]}" in
  1) verdict="${verdict_parts[0]}" ;;
  2) verdict="${verdict_parts[0]} + ${verdict_parts[1]}" ;;
  3) verdict="${verdict_parts[0]} + ${verdict_parts[1]} + ${verdict_parts[2]}" ;;
esac
```

Or use `printf -v` with explicit format. **CATO must read for this bug in the design code.** The §4.6.6 code as written has the IFS issue; ADA should use the case-based explicit form (above) or equivalent. **Flagging in the design so ADA does not paste the broken idiom.**

---

## §8. Out of scope (in this design)

Per directive A8 hard-locked, restated for ADA's safety:

- User-tier check support (covered by stoa--bj5 — orthogonal axis).
- Auto-discovery of workspaces (Option Small ratified explicit registry).
- Four-category drift classification (locally-modified × upstream-advanced — Option Small rejected this).
- apply.sh `--add-missing` or `--remove-obsolete` (defeats Option B's preserve-the-seam intent).
- `consumer-workspaces.txt` format change.
- Removing the existing `apply_substitutions` cite-comment pattern (it's the model for §3).
- Touching install.sh in any way (deliverable 7).
- Touching apply.sh in any way (deliverable 6).
- Verdict-line color/formatting beyond directive A6's structural shape (no ANSI codes added — keeps the output git-grep-able for any operator parsing tooling).
- Refactoring `source_path_for_deployed` or `detect_tier` beyond what's needed for the new helpers (CATO will flag any drive-by edits to these as scope creep).

If ADA reaches for any of the above during build, stop and surface as a peer-disagreement comment on `stoa--dxw` per directive's comms section. Do not silently expand scope.

---

## §9. Open questions / honest mismatches

1. **Routing-footer conditionality** — see §7.2. ARGUS to resolve.
2. **CAPTAIN_NAMES / TEMPLATE_NAMES array removal** — see §7.3. ARGUS to resolve (in-line removal vs follow-up arc).
3. **CURRENT-case format change** — the existing `printf "%-40s CURRENT (all %d deployed files match current substrate)\n"` at check.sh:447 produces `CURRENT (all 18 deployed files match current substrate)`. The new format per A6 is `CURRENT (0 drifted, 0 missing, 0 obsolete; 0 uncommitted)`. This is a deliberate behavior change to match the locked output format — the existing prose is replaced. ZENO will verify against directive A6. Surfacing here in case it reads as a regression of the existing "informational deployed-count" signal; the count is implicit (zero of zero across categories), the operator's diagnostic question shifts from "how many files did you check" to "are any drifted/missing/obsolete" — which is the actual question the skill answers.
4. **Probe 2 needs source-side fake-skill dir** — see §6 Probe 2's correction note. Probe text from the directive/ticket body elides this; VERA's executable form needs the `mkdir -p substrate/skills/fake-new` step or the probe doesn't surface anything.
5. **Composite-verdict join idiom** — see §7.6. The naive bash IFS idiom is broken; ADA must use the explicit case-based form. CATO to verify in the diff.
