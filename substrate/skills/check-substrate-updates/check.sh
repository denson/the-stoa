#!/usr/bin/env bash
#
# check.sh — substrate-update drift detection (Option Small, single-bit "differs?").
#
# Reads substrate/consumer-workspaces.txt (or one workspace passed via
# --workspace), and for each registered workspace classifies every deployed
# substrate file as CURRENT (byte-equal to source-after-substitutions) or
# DIFFERS (anything else). No four-category classification — PRINCIPAL memory
# + the workspace's git history of .claude/ is canonical for "did I change
# this or did upstream change this."
#
# Usage:
#   check.sh                              # scan all workspaces in registry
#   check.sh --workspace <path>           # scan a single workspace
#   check.sh --registry <path>            # use a non-default registry file
#   check.sh --quiet                      # suppress per-file lines for CURRENT workspaces
#
# Output: human-readable per-workspace summary; exit code is always 0 on
# successful execution. Drift is informational, not failure.

set -euo pipefail

# ----- locate substrate (this script lives in <substrate>/skills/check-substrate-updates/) ---

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SUBSTRATE_DIR="$(cd "${SCRIPT_DIR}/../.." && pwd)"
DEFAULT_REGISTRY="${SUBSTRATE_DIR}/consumer-workspaces.txt"

# ----- argument parsing ------------------------------------------------------

WORKSPACE_OVERRIDE=""
REGISTRY="$DEFAULT_REGISTRY"
QUIET=0

while [ "$#" -gt 0 ]; do
  case "$1" in
    --workspace)
      [ "$#" -ge 2 ] || { echo "check.sh: error: --workspace requires a path" >&2; exit 2; }
      WORKSPACE_OVERRIDE="$2"
      shift 2
      ;;
    --registry)
      [ "$#" -ge 2 ] || { echo "check.sh: error: --registry requires a path" >&2; exit 2; }
      REGISTRY="$2"
      shift 2
      ;;
    --quiet)
      QUIET=1
      shift
      ;;
    -h|--help)
      sed -n '/^# check\.sh/,/^# Drift is informational.*$/p' "$0" | sed 's/^# \{0,1\}//'
      exit 0
      ;;
    *)
      echo "check.sh: error: unknown argument: $1 (try --help)" >&2
      exit 2
      ;;
  esac
done

# ----- substrate-source arrays (mirror substrate/install.sh) -----------------
#
# Mirrors install.sh's CAPTAIN_NAMES, TEMPLATE_NAMES, SKILL_NAMES arrays
# (see install.sh ~lines 109–142 as of c37cf5a). Sourcing install.sh as bash
# would execute it (it has top-level side effects); maintaining the mirror
# here is the documented choice (design §2.3). If install.sh adds or removes
# a name, this list must be updated to match.

CAPTAIN_NAMES=(
  DAEDALUS
  ARGUS
  ADA
  VERA
  CATO
  STRABO
  BARTLEBY
  HERALD
  CURATOR
  ZENO
)

TEMPLATE_NAMES=(
  paste-instruction-template.md
  onboarding-questions.md
  consent-prompts.md
  polling-cron-prompt-template.md
  activation-paste-cheatsheet.md
  autonomous-mode-activation-template.md
)

SKILL_NAMES=(
  agent-author
  check-substrate-updates
)

# ----- helpers ---------------------------------------------------------------

# normalize_lf: read stdin, strip \r before \n. Used on both deployed and
# source-after-substitutions sides before byte-compare so checkout-on-Windows
# CRLF doesn't false-positive as drift.
normalize_lf() {
  tr -d '\r'
}

# apply_substitutions <source-file> <deployed-rel-path> <tier> <slug>
#
# Mirrors install.sh substitutions (lines ~613–617 + ~658 in install.sh as of c37cf5a).
# If install.sh adds a new {{...}} placeholder, this function must be updated to match.
#
# Substitutions are FILE-CLASS-SCOPED — install.sh only sed-substitutes the MAJOR
# and CAPTAIN files; templates and skills are deployed verbatim via `cp` / `cp -R`
# (install.sh ~lines 681, 711). Templates and skills MUST NOT be substituted at
# check time, otherwise prose that documents the placeholder (e.g., consent-prompts.md
# referencing `{{NAME_SUFFIX}}`) creates false-positive drift. See design §2.4 table.
#
# Substitution policy by deployed-relative path:
#   .claude/MAJOR_POLYBIUS*.md      : NAME_SUFFIX (and USER_TIER_DIR at user-tier; out of v0 scope)
#   .claude/MAJOR_PLINY*.md         : NAME_SUFFIX
#   .claude/agents/CAPTAIN_*.md     : NAME_SUFFIX
#   everything else                 : verbatim passthrough (no sed)
#
# Reads the source file, writes (substituted-or-verbatim) content to stdout.
apply_substitutions() {
  local source_file="$1"
  local dep_rel="$2"
  local tier="$3"
  local slug="$4"
  local name_suffix=""

  case "$tier" in
    project|subproject) name_suffix="_${slug}" ;;
  esac

  case "$dep_rel" in
    .claude/MAJOR_POLYBIUS*.md|.claude/MAJOR_PLINY*.md|.claude/agents/CAPTAIN_*.md)
      # Same sed shape install.sh uses; the '|' delimiter for USER_TIER_DIR is
      # documented but USER_TIER_DIR substitution at user-tier is out of v0 scope
      # (see SKILL.md / design §10.2).
      sed "s/{{NAME_SUFFIX}}/${name_suffix}/g" "$source_file"
      ;;
    *)
      # Templates and skills (and any future verbatim-deployed file class) — no substitution.
      cat "$source_file"
      ;;
  esac
}

# source_path_for_deployed <deployed-relative-path> <tier> <slug>
#
# Maps a workspace-relative path under .claude/ to a substrate-relative path
# under substrate/. Returns empty string if the deployed path doesn't map to
# any known substrate source (e.g. a pair-programmer MAJOR PRINCIPAL added).
#
# Examples:
#   .claude/MAJOR_POLYBIUS.md            -> MAJOR_POLYBIUS.md
#   .claude/MAJOR_PLINY_my_proj.md       -> MAJOR_PLINY.md  (subproject suffix stripped)
#   .claude/operating-disciplines.md     -> operating-disciplines.md
#   .claude/agents/CAPTAIN_ADA.md        -> CAPTAIN_ADA.md
#   .claude/agents/CAPTAIN_ADA_my_proj.md-> CAPTAIN_ADA.md  (suffix stripped)
#   .claude/templates/<name>.md          -> templates/<name>.md
#   .claude/skills/<name>/<file>         -> skills/<name>/<file>
source_path_for_deployed() {
  local dep="$1"
  local tier="$2"
  local slug="$3"
  local suffix=""

  case "$tier" in
    project|subproject) suffix="_${slug}" ;;
  esac

  # Strip .claude/ prefix (paths come in as deployed-relative under .claude/).
  local rel="${dep#.claude/}"

  case "$rel" in
    MAJOR_POLYBIUS.md|MAJOR_POLYBIUS_*.md)
      echo "MAJOR_POLYBIUS.md"
      ;;
    MAJOR_PLINY.md|MAJOR_PLINY_*.md)
      echo "MAJOR_PLINY.md"
      ;;
    operating-disciplines.md)
      echo "operating-disciplines.md"
      ;;
    agents/CAPTAIN_*.md)
      # Extract mnemonic between CAPTAIN_ and ${suffix}.md (or .md for unsuffixed).
      local base="${rel#agents/CAPTAIN_}"
      if [ -n "$suffix" ]; then
        base="${base%${suffix}.md}"
      else
        base="${base%.md}"
      fi
      echo "CAPTAIN_${base}.md"
      ;;
    templates/*)
      echo "$rel"
      ;;
    skills/*)
      echo "$rel"
      ;;
    *)
      # Unknown deployed path — not substrate-derived.
      echo ""
      ;;
  esac
}

# detect_tier <workspace-abs-path>
#
# Echoes "<tier> <slug>" (space-separated) on stdout.
# Possible tiers: user, subproject, project, none
# Slug is empty for user and none tiers.
detect_tier() {
  local ws="$1"
  local ws_abs
  # Resolve to absolute path; on Windows MSYS / git-bash, $(cd && pwd) gives a
  # POSIX-shaped path which is what we want.
  if [ ! -d "$ws" ]; then
    echo "none "
    return 0
  fi
  ws_abs="$(cd "$ws" && pwd)"

  # User-tier: workspace IS ~/.claude (path resolves to $HOME/.claude). Out of
  # v0 scope but detected so we can surface a friendly message.
  if [ "$ws_abs" = "${HOME}/.claude" ] || [ "$ws_abs" = "${HOME}" ]; then
    echo "user "
    return 0
  fi

  if [ ! -d "${ws_abs}/.claude" ]; then
    echo "none "
    return 0
  fi

  # Subproject-tier: any MAJOR_POLYBIUS_<slug>.md present.
  local p
  for p in "${ws_abs}/.claude/MAJOR_POLYBIUS_"*.md; do
    if [ -f "$p" ]; then
      local base
      base="$(basename "$p")"
      # Strip MAJOR_POLYBIUS_ prefix and .md suffix.
      local slug="${base#MAJOR_POLYBIUS_}"
      slug="${slug%.md}"
      echo "subproject ${slug}"
      return 0
    fi
  done

  # Project-tier: unsuffixed MAJOR_POLYBIUS.md present.
  if [ -f "${ws_abs}/.claude/MAJOR_POLYBIUS.md" ]; then
    local slug
    slug="$(basename "$ws_abs" | tr '.-' '__')"
    echo "project ${slug}"
    return 0
  fi

  echo "none "
}

# enumerate_deployed <workspace-abs> <tier> <slug>
# Echoes one deployed-relative path per line for every file we expect to find
# at standard substrate-deploy locations. Existence is checked by the caller.
enumerate_deployed() {
  local ws="$1"
  local tier="$2"
  local slug="$3"
  local suffix=""

  case "$tier" in
    project|subproject) suffix="_${slug}" ;;
  esac

  # MAJOR files: subproject-tier suffixes both; project/user-tier do not.
  if [ "$tier" = "subproject" ]; then
    echo ".claude/MAJOR_POLYBIUS${suffix}.md"
    echo ".claude/MAJOR_PLINY${suffix}.md"
  else
    echo ".claude/MAJOR_POLYBIUS.md"
    echo ".claude/MAJOR_PLINY.md"
  fi

  echo ".claude/operating-disciplines.md"

  # CAPTAINs: suffixed at project/subproject, unsuffixed at user.
  local cap
  for cap in "${CAPTAIN_NAMES[@]}"; do
    echo ".claude/agents/CAPTAIN_${cap}${suffix}.md"
  done

  # Templates (unsuffixed at all tiers).
  local tn
  for tn in "${TEMPLATE_NAMES[@]}"; do
    echo ".claude/templates/${tn}"
  done

  # Skills: enumerate every file under each skill subtree in the source.
  local sn rel
  for sn in "${SKILL_NAMES[@]}"; do
    if [ -d "${SUBSTRATE_DIR}/skills/${sn}" ]; then
      while IFS= read -r f; do
        rel="${f#${SUBSTRATE_DIR}/}"
        echo ".claude/${rel}"
      done < <(find "${SUBSTRATE_DIR}/skills/${sn}" -type f)
    fi
  done
}

# read_state_file <workspace-abs>
# Echoes "<last_check_timestamp>|<last_check_against_sha>" or empty if absent.
read_state_file() {
  local ws="$1"
  local sf="${ws}/.claude/.substrate-last-check"
  [ -f "$sf" ] || { echo ""; return 0; }
  local ts="" sha=""
  while IFS='=' read -r k v; do
    case "$k" in
      last_check_timestamp)   ts="$v" ;;
      last_check_against_sha) sha="$v" ;;
    esac
  done < "$sf"
  echo "${ts}|${sha}"
}

# write_state_file <workspace-abs> <sha>
write_state_file() {
  local ws="$1"
  local sha="$2"
  local sf="${ws}/.claude/.substrate-last-check"
  local now
  now="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  cat > "$sf" <<EOF
last_check_timestamp=${now}
last_check_against_sha=${sha}
EOF
}

# substrate_head_sha: short SHA of the substrate repo HEAD (or "unknown").
substrate_head_sha() {
  if git -C "$SUBSTRATE_DIR" rev-parse --short HEAD >/dev/null 2>&1; then
    git -C "$SUBSTRATE_DIR" rev-parse --short HEAD
  else
    echo "unknown"
  fi
}

# check_workspace <workspace-input>
# Runs the per-workspace check; prints the summary block; updates state file.
check_workspace() {
  local ws_in="$1"
  local ws_abs
  if [ ! -e "$ws_in" ]; then
    printf "%-40s NOT-FOUND (path does not exist: %s)\n" "$(basename "$ws_in")" "$ws_in"
    return 0
  fi
  ws_abs="$(cd "$ws_in" && pwd)"
  local label
  label="$(basename "$ws_abs")"

  # Tier detection.
  local tier_line tier slug
  tier_line="$(detect_tier "$ws_abs")"
  tier="${tier_line%% *}"
  slug="${tier_line#* }"
  slug="${slug# }"  # trim leading space if slug empty

  if [ "$tier" = "none" ]; then
    printf "%-40s NOT-STOA-DEPLOYED (no .claude/MAJOR_POLYBIUS*.md found)\n" "$label"
    return 0
  fi

  if [ "$tier" = "user" ]; then
    printf "%-40s USER-TIER (out of v0 scope)\n" "$label"
    echo "  user-tier check is not supported in v0 (the {{USER_TIER_DIR}}"
    echo "  substitution can't be reliably re-derived without per-file markers)."
    echo "  Manually diff with:"
    echo "    cd \"${SUBSTRATE_DIR}\" && diff -u MAJOR_POLYBIUS.md \"${HOME}/.claude/MAJOR_POLYBIUS.md\""
    return 0
  fi

  # Enumerate deployed files and compare each.
  local differs_files=()
  local differs_deltas=()
  local current_count=0
  local missing_count=0
  local total=0

  local dep src_rel src_abs deployed_path
  while IFS= read -r dep; do
    [ -n "$dep" ] || continue
    total=$((total + 1))
    deployed_path="${ws_abs}/${dep}"
    if [ ! -f "$deployed_path" ]; then
      missing_count=$((missing_count + 1))
      continue
    fi
    src_rel="$(source_path_for_deployed "$dep" "$tier" "$slug")"
    if [ -z "$src_rel" ]; then
      # Unknown — shouldn't happen since enumerate_deployed only emits
      # substrate-derived paths. Skip defensively.
      continue
    fi
    src_abs="${SUBSTRATE_DIR}/${src_rel}"
    if [ ! -f "$src_abs" ]; then
      # Source file gone (deleted from substrate) — surface as DIFFERS so the
      # operator notices a file that should be removed.
      differs_files+=("$dep")
      differs_deltas+=("source-removed")
      continue
    fi

    # Byte-compare deployed (LF-normalized) to source-after-substitutions
    # (LF-normalized).
    local dep_norm src_norm
    dep_norm="$(normalize_lf < "$deployed_path")"
    src_norm="$(apply_substitutions "$src_abs" "$dep" "$tier" "$slug" | normalize_lf)"

    if [ "$dep_norm" = "$src_norm" ]; then
      current_count=$((current_count + 1))
    else
      # Compute line-count delta (source - deployed).
      local dep_lines src_lines delta sign
      dep_lines="$(printf '%s' "$dep_norm" | wc -l | tr -d ' ')"
      src_lines="$(printf '%s' "$src_norm" | wc -l | tr -d ' ')"
      delta=$((src_lines - dep_lines))
      if [ "$delta" -ge 0 ]; then
        sign="+"
      else
        sign=""
      fi
      differs_files+=("$dep")
      differs_deltas+=("${sign}${delta} lines")
    fi
  done < <(enumerate_deployed "$ws_abs" "$tier" "$slug")

  # Emit summary.
  local sha
  sha="$(substrate_head_sha)"
  local state ts last_sha
  state="$(read_state_file "$ws_abs")"
  ts="${state%%|*}"
  last_sha="${state##*|}"

  local n_differs=${#differs_files[@]}
  if [ "$n_differs" -eq 0 ]; then
    printf "%-40s CURRENT (all %d deployed files match current substrate)\n" "$label" "$current_count"
    if [ -n "$ts" ]; then
      printf "  Last check: %s (against substrate sha %s)\n" "$ts" "$last_sha"
    fi
  else
    printf "%-40s DRIFTED (%d files differ from current substrate)\n" "$label" "$n_differs"
    local i
    for ((i=0; i<n_differs; i++)); do
      printf "  - %-50s (%s)\n" "${differs_files[$i]}" "${differs_deltas[$i]}"
    done
    if [ -n "$ts" ]; then
      printf "\n  Last check: %s (against substrate sha %s)\n" "$ts" "$last_sha"
    fi
    printf "  Current substrate HEAD: %s\n" "$sha"
    printf "  Run 'apply.sh --workspace %s' to review and apply per-file.\n" "$ws_abs"
  fi

  # Update state file.
  write_state_file "$ws_abs" "$sha"
}

# ----- main ------------------------------------------------------------------

if [ -n "$WORKSPACE_OVERRIDE" ]; then
  check_workspace "$WORKSPACE_OVERRIDE"
  exit 0
fi

if [ ! -f "$REGISTRY" ]; then
  echo "check.sh: error: registry not found: $REGISTRY" >&2
  exit 2
fi

while IFS= read -r line || [ -n "$line" ]; do
  # Strip trailing CR (Windows line endings on the registry file).
  line="${line%$'\r'}"
  # Skip blank lines and comments.
  case "$line" in
    ""|\#*) continue ;;
  esac
  check_workspace "$line"
  echo
done < "$REGISTRY"
