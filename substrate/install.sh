#!/usr/bin/env bash
#
# install.sh — minimal template installer for the three-role agent substrate.
#
# Drops MAJOR_POLYBIUS.md and MAJOR_PLINY.md to a chosen target (user-tier ~/.claude/
# or a project-tier <project>/.claude/). Optionally appends a one-line reference
# to MAJOR_POLYBIUS.md in the target's CLAUDE.md, but only with an explicit
# informed-consent flag.
#
# Per the architecture spec (three-role-recursive-architecture.md §8): this is
# the TEMPLATE. MAJOR_POLYBIUS rewrites a session-specific install per user
# conversation at deploy time. This script does only the non-conversational
# mechanical deploy: drops the two MAJOR role files, deploys the 11 CAPTAIN
# sub-agent envelopes (unless --no-captains), deploys the templates/ runtime
# tooling (unless --no-templates), deploys LIEUTENANT skills under
# <DEST>/.claude/skills/ (always — POLYBIUS invokes them via the Skill tool;
# no opt-out flag), deploys the instruction-module library under
# <DEST>/.claude/modules/ (always — glob-discovered from substrate/modules/*.md;
# no opt-out flag; subproject mode excepted), and optionally appends a
# marker-bounded reference block to CLAUDE.md when the consent flag is set.
# It does NOT run `bw init` or
# write the paste-instruction; POLYBIUS handles those interactively with the
# PRINCIPAL in the loop.
#
# Usage:
#   ./install.sh --target user [--modify-claude-md] [--no-captains] [--no-templates] [--prune-obsolete] [--dry-run]
#   ./install.sh --target project --project-dir <path> [--modify-claude-md] [--no-captains] [--no-templates] [--prune-obsolete] [--dry-run]
#   ./install.sh --target subproject --parent-dir <path> --subproject <slug> [--no-captains] [--prune-obsolete] [--dry-run]
#   ./install.sh --help
#
# Idempotency: re-running with the same flags is safe. Files are overwritten
# in place; CLAUDE.md appends are guarded by a marker check so the reference is
# added at most once.
#
# CLAUDE.md safety: when --modify-claude-md is given AND the target CLAUDE.md
# exists, the script copies it to <CLAUDE.md>.bak BEFORE the append, so the
# pre-modification content is recoverable in-run if anything goes wrong. The
# backup is single-shot (overwritten on each subsequent run); git is the
# long-term archive — the .bak file is for "oops" recovery only.
#
# CAPTAIN envelopes: by default the script deploys the 11 CAPTAIN_*.md sub-agent
# envelopes from this directory to <target>/.claude/agents/. At project-tier the
# files are suffixed with _<sanitized-project> (e.g. CAPTAIN_DAEDALUS_my_project.md)
# and the {{NAME_SUFFIX}} slot in the YAML frontmatter's `name:` field is filled
# accordingly; at user-tier the files are unsuffixed and {{NAME_SUFFIX}} expands
# to empty. Pass --no-captains to skip CAPTAIN deployment.
#
# Templates: by default the script deploys templates/*.md from this directory to
# <target>/.claude/templates/. These are POLYBIUS's runtime working tools
# (paste-instruction template, onboarding-questions, consent-prompts) — shared
# tooling, not agent-shaped, deployed unsuffixed at both tiers. Pass
# --no-templates to skip. (Subproject mode never deploys templates — the
# sub-project shares its parent's runtime tooling; see below.)
#
# Skills: the script deploys skills/<name>/ subdirectories from this directory
# to <target>/.claude/skills/<name>/. Skills are LIEUTENANT-tier helpers
# POLYBIUS invokes via the Skill tool — agent-author for drafting new role
# files, etc. Skills are deployed unsuffixed at every tier (including
# subproject — Claude Code loads skills from <project>/.claude/skills/ or
# ~/.claude/skills/, NOT from a parent directory, so a subproject must have
# its own skills/ dir to invoke them). There is no --no-skills opt-out:
# skills are universal helpers and skipping the deploy leaves POLYBIUS unable
# to use them.
#
# Modules: the script deploys substrate/modules/*.md from this directory to
# <target>/.claude/modules/. These are composition-layer instruction modules an
# orchestrator delivers to a sub-agent at dispatch time (Read .claude/modules/<X>.md)
# — shared tooling, deployed unsuffixed, GLOB-discovered (no manifest array) so
# authoring a new module needs no install.sh edit (Arc 44 / stoa--xyb.4). Always
# deployed at user + project tiers (no --no-modules opt-out, mirrors skills);
# subproject-tier deploy is a tracked Arc-2-gating open question (stoa--xyb.4 §6).
#
# Staleness detection: after deploying, the script scans the destination for
# files no longer in the substrate source — typically left over from a
# renamed CAPTAIN, removed template, removed skill, or removed module. By default this is
# warn-only (lists obsolete files for the human to rm manually). Pass
# --prune-obsolete to remove them automatically. MAJOR_*.md files are
# deliberately not scanned (pair-programmer Majors land in the same agents/
# directory and cannot be reliably distinguished from substrate-canonical
# MAJORs by filename alone).
#
# Subproject mode: --target subproject deploys a sub-project under an existing
# parent project. Required flags: --parent-dir <path-to-parent-project> and
# --subproject <slug>. The sub-project lives at <parent>/<subproject>/, sharing
# the parent's git repo and beadwork. Both MAJOR_POLYBIUS.md and MAJOR_PLINY.md
# are deployed with the _<subproject> filename suffix (parallel to CAPTAINs);
# all 11 CAPTAINs are deployed with the same suffix. Subproject mode does NOT
# modify any CLAUDE.md (parent's stays as-is; sub-project does not get its own),
# does NOT redeploy templates (sub-project reads parent's at <parent>/.claude/
# templates/), and does NOT run bw init (sub-project shares parent's bw repo).
# --modify-claude-md and --templates-related flags are rejected in this mode.
#
# Dry-run: --dry-run prints every action without writing anything.

set -euo pipefail

# ----- defaults --------------------------------------------------------------

TARGET=""
PROJECT_DIR=""
PARENT_DIR=""
SUBPROJECT=""
USER_TIER_DIR=""        # Arc 20: user-tier directory (where user-beadwork lives + projects sit; default ~/stoa_projects/)
MODIFY_CLAUDE_MD=0
DRY_RUN=0
WITH_CAPTAINS=1
WITH_TEMPLATES=1
PRUNE_OBSOLETE=0

# Source files live next to this script.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC_POLYBIUS="${SCRIPT_DIR}/MAJOR_POLYBIUS.md"
SRC_PLINY="${SCRIPT_DIR}/MAJOR_PLINY.md"
SRC_OPERATING_DISCIPLINES="${SCRIPT_DIR}/operating-disciplines.md"
SRC_TEMPLATES_DIR="${SCRIPT_DIR}/templates"
SRC_SKILLS_DIR="${SCRIPT_DIR}/skills"
SRC_MODULES_DIR="${SCRIPT_DIR}/modules"

# Instruction-module library (Arc 44 / stoa--xyb.4). Composable on-demand
# reference content an orchestrator names in a dispatch (Read .claude/modules/<X>.md)
# or that the team reads when authoring/relocating modules. Deployed unsuffixed
# (shared tooling, like templates). GLOB-DISCOVERED from substrate/modules/*.md
# (per stoa--xyb.4 r4 / PLINY decision) so authoring a new module needs NO
# install.sh edit — the file class the epic is designed to grow continuously.
# No MODULE_NAMES array (glob, not manifest).

# Template filenames POLYBIUS uses at runtime. Shared tooling — deployed
# unsuffixed at both user-tier and project-tier.
TEMPLATE_NAMES=(
  paste-instruction-template.md
  onboarding-questions.md
  consent-prompts.md
  polling-cron-prompt-template.md
  activation-paste-cheatsheet.md
  autonomous-mode-activation-template.md
  handoff-doc-template.md
)

# The 11 CAPTAIN envelope source files. Order is the gauntlet pipeline order
# (DAEDALUS through CATO) followed by the support seats; ordering only affects
# log output, not correctness.
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
  TIRO
)

# LIEUTENANT skill source directories (under skills/). Each is a directory
# containing SKILL.md (and optionally other files) — the whole subtree is
# copied to <DEST>/.claude/skills/<name>/. Always deployed (no opt-out flag);
# Claude Code loads skills from <project>/.claude/skills/ or
# ~/.claude/skills/, so a deployed substrate that omits skills leaves
# POLYBIUS unable to invoke them.
SKILL_NAMES=(
  agent-author
  check-substrate-updates
  credential-discipline
  check-bw-release
  inspect-script-output
  handoff-author
  save-verdict
  validate-spec
)

# Marker line written into CLAUDE.md when --modify-claude-md is used; presence
# of this marker is how subsequent runs detect that the reference is already
# installed.
CLAUDE_MD_MARKER="<!-- agent-substrate: POLYBIUS reference -->"

# Second marker for the base-vs-custom convention block (Arc 29; D6).
# Independent from CLAUDE_MD_MARKER so the two appends are separately
# idempotent: the existence-check uses this marker, the POLYBIUS block uses
# its own. See substrate/operating-disciplines.md §23 + substrate/
# MAJOR_POLYBIUS.md §17 for the discipline this block surfaces to the operator.
CLAUDE_MD_BASE_VS_CUSTOM_MARKER="<!-- agent-substrate: base-vs-custom convention -->"

# ----- helpers ---------------------------------------------------------------

usage() {
  sed -n '/^# install\.sh/,/^# Dry-run:.*$/p' "$0" | sed 's/^# \{0,1\}//'
  exit "${1:-0}"
}

err() {
  echo "install.sh: error: $*" >&2
  exit 2
}

log() {
  if [ "$DRY_RUN" -eq 1 ]; then
    echo "[dry-run] $*"
  else
    echo "$*"
  fi
}

run_or_print() {
  # Echo a command in dry-run mode; otherwise execute it.
  if [ "$DRY_RUN" -eq 1 ]; then
    echo "[dry-run] $*"
  else
    eval "$@"
  fi
}

# ----- Arc 20: user-tier directory detection + scaffolding -------------------
#
# The user-tier chief-of-staff (POLYBIUS) needs a directory under which it
# operates: where user-beadwork (durable memory) lives, and where cross-project
# coordination happens. Common conventions vary by user (~/stoa_projects/,
# ~/claude_projects/, ~/projects/, ~/Code/, custom).
#
# detect_user_beadwork: scan four common locations for an existing
# user-beadwork that is git-init'd and bw-init'd. bw's marker is the
# 'beadwork' orphan branch (not a .bw/ directory — bw stores ticket data
# on that branch, leaving main for repo-shaped artifacts). Echoes parent
# paths of detected user-beadwork dirs (one per line). Empty stdout = no
# matches.
detect_user_beadwork() {
  for parent in "${HOME}/stoa_projects" "${HOME}/claude_projects" "${HOME}/projects" "${HOME}/Code"; do
    candidate="${parent}/user-beadwork"
    if [ -d "$candidate" ] && [ -d "$candidate/.git" ]; then
      if git -C "$candidate" rev-parse --verify --quiet beadwork >/dev/null 2>&1; then
        echo "$parent"
      fi
    fi
  done
}

# resolve_path: expand leading ~ to $HOME and convert to absolute path.
# Used to canonicalize user input from interactive prompt or --user-tier-dir.
resolve_path() {
  case "$1" in
    "~"|"~/")     echo "$HOME" ;;
    "~/"*)        echo "${HOME}/${1#~/}" ;;
    /*)           echo "$1" ;;
    *)            echo "$(cd "$(dirname "$1")" 2>/dev/null && pwd)/$(basename "$1")" ;;
  esac
}

# choose_user_tier_dir: detection-with-confirmation hybrid prompt for the
# user-tier directory. Sets the global USER_TIER_DIR variable on success.
# Skipped if --user-tier-dir was already passed on the command line OR if
# stdin is not a TTY (non-interactive shell — fall back to default).
choose_user_tier_dir() {
  if [ -n "$USER_TIER_DIR" ]; then
    log "user-tier dir provided via --user-tier-dir: $USER_TIER_DIR"
    return 0
  fi

  candidates="$(detect_user_beadwork)"
  num_candidates=$(echo -n "$candidates" | grep -c '^' || true)

  # Frame the question as "where do your Claude Code projects live?" — POLYBIUS operates
  # from the user-tier directory and needs to see all your projects to coordinate them.
  # The right answer is wherever you already keep Claude Code projects; if you don't have
  # an existing projects directory, the install creates ~/stoa_projects/ as the default.
  if [ -t 0 ] && [ -t 1 ]; then
    printf "\n" >&2
    printf "Where do your Claude Code projects live?\n" >&2
    printf "Stoa installs there — POLYBIUS (the user-tier chief-of-staff) operates from this\n" >&2
    printf "directory and needs to see your projects laterally to coordinate them.\n" >&2
    printf "\n" >&2
  fi

  if [ "$num_candidates" -eq 1 ]; then
    found_parent="$candidates"
    if [ -t 0 ] && [ -t 1 ]; then
      printf "Detected existing user-beadwork at %s/user-beadwork/.\n" "$found_parent" >&2
      printf "This looks like where your Claude Code projects already live.\n" >&2
      printf "Install Stoa with %s as your user-tier dir? [Y/n] " "$found_parent" >&2
      read -r answer
      case "$answer" in
        ""|y|Y|yes|Yes|YES) USER_TIER_DIR="$found_parent" ;;
        *) USER_TIER_DIR="" ;;  # fall through to default-prompt below
      esac
    else
      # Non-interactive: pick the detected one
      USER_TIER_DIR="$found_parent"
      log "non-interactive: using detected user-beadwork parent: $USER_TIER_DIR"
    fi
  elif [ "$num_candidates" -gt 1 ]; then
    if [ -t 0 ] && [ -t 1 ]; then
      printf "Detected multiple existing user-beadwork directories — these are likely\n" >&2
      printf "existing places where your Claude Code projects live. Pick one, or pick\n" >&2
      printf "'create new' to install Stoa fresh:\n" >&2
      i=1
      while IFS= read -r line; do
        [ -n "$line" ] || continue
        printf "  %d) %s/user-beadwork/\n" "$i" "$line" >&2
        i=$((i+1))
      done <<EOF
$candidates
EOF
      printf "  %d) create new at ~/stoa_projects/\n" "$i" >&2
      printf "Pick a number [1-%d]: " "$i" >&2
      read -r answer
      # Map answer to selection
      sel_num=1
      USER_TIER_DIR=""
      while IFS= read -r line; do
        [ -n "$line" ] || continue
        if [ "$answer" = "$sel_num" ]; then
          USER_TIER_DIR="$line"
          break
        fi
        sel_num=$((sel_num+1))
      done <<EOF
$candidates
EOF
      # If "create new" picked OR no match
      if [ -z "$USER_TIER_DIR" ] && [ "$answer" = "$i" ]; then
        USER_TIER_DIR=""  # fall through to default-prompt
      fi
    else
      # Non-interactive with multiple matches: pick first
      USER_TIER_DIR="$(echo "$candidates" | head -1)"
      log "non-interactive: multiple candidates; picking first: $USER_TIER_DIR"
    fi
  fi

  # If still unset (zero candidates, OR user declined detected option, OR user picked "create new"):
  if [ -z "$USER_TIER_DIR" ]; then
    if [ -t 0 ] && [ -t 1 ]; then
      printf "Tell me where your Claude Code projects live.\n" >&2
      printf "If you have an existing projects directory (e.g., ~/projects/, ~/dev/,\n" >&2
      printf "~/Code/), enter that path — Stoa installs there alongside your projects.\n" >&2
      printf "If you don't have one yet, the default ~/stoa_projects/ will be created.\n" >&2
      printf "Path [default ~/stoa_projects/]: " >&2
      read -r answer
      if [ -z "$answer" ]; then
        USER_TIER_DIR="${HOME}/stoa_projects"
      else
        USER_TIER_DIR="$(resolve_path "$answer")"
      fi
    else
      USER_TIER_DIR="${HOME}/stoa_projects"
      log "non-interactive: defaulting to $USER_TIER_DIR"
    fi
  fi

  # Canonicalize: ensure absolute path, no trailing slash
  USER_TIER_DIR="$(resolve_path "$USER_TIER_DIR")"
  USER_TIER_DIR="${USER_TIER_DIR%/}"
  echo "user-tier dir: $USER_TIER_DIR"
}

# scaffold_user_tier: create the directory + initialize user-beadwork as a
# git+bw repo. Idempotent: skip steps that are already done. Never clobbers
# existing user-beadwork.
scaffold_user_tier() {
  [ -n "$USER_TIER_DIR" ] || err "scaffold_user_tier called without USER_TIER_DIR set"

  if [ ! -d "$USER_TIER_DIR" ]; then
    run_or_print "mkdir -p \"$USER_TIER_DIR\""
    log "created user-tier directory: $USER_TIER_DIR"
  else
    log "user-tier directory already exists: $USER_TIER_DIR"
  fi

  bw_dir="${USER_TIER_DIR}/user-beadwork"
  bw_initialized=0
  if [ -d "$bw_dir" ] && [ -d "$bw_dir/.git" ]; then
    if git -C "$bw_dir" rev-parse --verify --quiet beadwork >/dev/null 2>&1; then
      bw_initialized=1
    fi
  fi
  if [ "$bw_initialized" -eq 1 ]; then
    log "user-beadwork already exists at $bw_dir (git+bw initialized) — skipping init"
  elif [ -d "$bw_dir" ]; then
    log "user-beadwork directory exists at $bw_dir but is not fully initialized — surface to PRINCIPAL"
    echo "install.sh: warning: $bw_dir exists but lacks .git/ or the 'beadwork' bw orphan branch. Skipping init to avoid clobbering. PRINCIPAL: verify state and run 'cd $bw_dir && git init && bw init' manually if appropriate." >&2
  else
    if [ "$DRY_RUN" -eq 1 ]; then
      echo "[dry-run] mkdir -p \"$bw_dir\""
      echo "[dry-run] cd \"$bw_dir\" && git init"
      echo "[dry-run] cd \"$bw_dir\" && bw init"
    else
      mkdir -p "$bw_dir"
      ( cd "$bw_dir" && git init >/dev/null 2>&1 && bw init >/dev/null 2>&1 ) \
        || err "failed to initialize user-beadwork at $bw_dir (git init or bw init failed)"
      echo "initialized user-beadwork at $bw_dir (git + bw)"
    fi
  fi
}

# ----- Arc 38 (bj5 / A8): substrate-manifest writer --------------------------
#
# write_substrate_manifest <dest-dir> <tier> <slug>
#
# Writes <dest-dir>/.substrate-manifest recording every substitution applied to
# deployed files in this run. Used by substrate/skills/check-substrate-updates/
# check.sh + apply.sh at user-tier (where the {{USER_TIER_DIR}} substitution
# can't be reliably reverse-derived; bj5 design §2.2). Project-tier +
# subproject-tier workspaces also get the manifest written (uniform behavior;
# check.sh continues to derive substitutions from the workspace basename at
# those tiers and the manifest is informational).
#
# Format: tab-separated triples (<deployed-rel-path>\t<token>\t<replacement>),
# preceded by a header block recording tier + deployed_at + substrate_sha.
#
# CITE: format invariant — companion read-sites at
# substrate/skills/check-substrate-updates/check.sh + apply.sh
# apply_substitutions_from_manifest(). If this writer rotates the format, both
# readers must update their parsers to match. The cite-at-the-read-site
# discipline is the durable mitigation for the install.sh / check.sh / apply.sh
# format coupling (design §2.2 + §2.7).
write_substrate_manifest() {
  local dest="$1"
  local tier="$2"
  local slug="$3"
  local manifest="${dest}/.substrate-manifest"
  local name_suffix=""

  case "$tier" in
    project|subproject) name_suffix="_${slug}" ;;
  esac

  local now sha
  now="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  sha="$(cd "$SCRIPT_DIR" && git rev-parse --short HEAD 2>/dev/null || echo unknown)"

  if [ "$DRY_RUN" -eq 1 ]; then
    echo "[dry-run] write: $manifest (tier=$tier, deployed_at=$now, substrate_sha=$sha)"
    return 0
  fi

  {
    echo "# Stoa substrate deploy manifest — substitutions applied to deployed files."
    echo "# Written by install.sh at deploy time. Read by check.sh + apply.sh to normalize."
    echo "# Format: <deployed-relative-path>\t<token>\t<replacement>"
    echo "# DO NOT EDIT MANUALLY. install.sh rewrites this file on every re-run."
    # CITE: format-version contract per Arc 40 / stoa--6n9. The `# format=v1`
    # line is parser-visible (matched by check.sh + apply.sh
    # apply_substitutions_from_manifest header-scan) AND comment-safe
    # (pre-fix readers' `""|\#*) continue ;;` skip rule ignores it). Any
    # install.sh that bumps the format to v2 MUST update both readers'
    # header-scan in the same arc; the readers' version-rejection error
    # names the upgrade path. Companion read-sites:
    #   substrate/skills/check-substrate-updates/check.sh
    #   substrate/skills/check-substrate-updates/apply.sh
    echo "# format=v1"
    echo "#"
    echo "# tier=${tier}"
    echo "# deployed_at=${now}"
    echo "# substrate_sha=${sha}"
    echo ""
    # MAJOR_POLYBIUS.md: NAME_SUFFIX always; USER_TIER_DIR at user-tier only.
    # Subproject-tier suffixes the MAJOR filename; project + user tiers do not.
    if [ "$tier" = "subproject" ]; then
      printf ".claude/MAJOR_POLYBIUS%s.md\t{{NAME_SUFFIX}}\t%s\n" "${name_suffix}" "${name_suffix}"
      printf ".claude/MAJOR_PLINY%s.md\t{{NAME_SUFFIX}}\t%s\n" "${name_suffix}" "${name_suffix}"
    else
      printf ".claude/MAJOR_POLYBIUS.md\t{{NAME_SUFFIX}}\t%s\n" "${name_suffix}"
      printf ".claude/MAJOR_PLINY.md\t{{NAME_SUFFIX}}\t%s\n" "${name_suffix}"
      if [ "$tier" = "user" ] && [ -n "$USER_TIER_DIR" ]; then
        printf ".claude/MAJOR_POLYBIUS.md\t{{USER_TIER_DIR}}\t%s\n" "$USER_TIER_DIR"
      fi
    fi
    # CAPTAINs (always NAME_SUFFIX — empty at user-tier; _<slug> at project/subproject).
    if [ "$WITH_CAPTAINS" -eq 1 ]; then
      for name in "${CAPTAIN_NAMES[@]}"; do
        printf ".claude/agents/CAPTAIN_%s%s.md\t{{NAME_SUFFIX}}\t%s\n" "$name" "${name_suffix}" "${name_suffix}"
      done
    fi
  } > "$manifest"
  echo "wrote manifest: $manifest"
}

# ----- argument parsing ------------------------------------------------------

while [ "$#" -gt 0 ]; do
  case "$1" in
    --target)
      [ "$#" -ge 2 ] || err "--target requires a value (user|project|subproject)"
      TARGET="$2"
      shift 2
      ;;
    --project-dir)
      [ "$#" -ge 2 ] || err "--project-dir requires a path"
      PROJECT_DIR="$2"
      shift 2
      ;;
    --parent-dir)
      [ "$#" -ge 2 ] || err "--parent-dir requires a path"
      PARENT_DIR="$2"
      shift 2
      ;;
    --subproject)
      [ "$#" -ge 2 ] || err "--subproject requires a slug"
      SUBPROJECT="$2"
      shift 2
      ;;
    --user-tier-dir)
      # Arc 20: optional override for user-tier directory choice. If passed,
      # skip the interactive detection-with-confirmation prompt. The path is
      # the parent directory under which user-beadwork lives (and where
      # cross-project state for the user-tier chief-of-staff seat operates).
      # Resolved to absolute path during validation.
      [ "$#" -ge 2 ] || err "--user-tier-dir requires a path"
      USER_TIER_DIR="$2"
      shift 2
      ;;
    --modify-claude-md)
      MODIFY_CLAUDE_MD=1
      shift
      ;;
    --dry-run)
      DRY_RUN=1
      shift
      ;;
    --no-captains)
      WITH_CAPTAINS=0
      shift
      ;;
    --no-templates)
      WITH_TEMPLATES=0
      shift
      ;;
    --prune-obsolete)
      PRUNE_OBSOLETE=1
      shift
      ;;
    -h|--help)
      usage 0
      ;;
    *)
      err "unknown argument: $1 (try --help)"
      ;;
  esac
done

# ----- validation ------------------------------------------------------------

[ -n "$TARGET" ] || err "--target is required (user|project|subproject)"

# Tracks whether MAJOR_POLYBIUS.md / MAJOR_PLINY.md should be deployed with the
# _<slug> filename suffix. True only in subproject mode — at user-tier and
# project-tier the MAJORs land unsuffixed (the project's CLAUDE.md auto-loads
# them by canonical name).
SUFFIX_MAJORS=0

case "$TARGET" in
  user)
    DEST_DIR="${HOME}/.claude"
    DEST_CLAUDE_MD="${HOME}/.claude/CLAUDE.md"
    DEST_AGENTS_DIR="${HOME}/.claude/agents"
    DEST_TEMPLATES_DIR="${HOME}/.claude/templates"
    DEST_SKILLS_DIR="${HOME}/.claude/skills"
    DEST_MODULES_DIR="${HOME}/.claude/modules"
    PROJECT_SLUG=""
    NAME_SUFFIX=""
    # Arc 20: choose user-tier dir (interactive prompt or --user-tier-dir override),
    # then scaffold it (mkdir + init user-beadwork as git+bw repo if not already).
    # USER_TIER_DIR will be substituted into MAJOR_POLYBIUS.md at deploy time.
    choose_user_tier_dir
    scaffold_user_tier
    ;;
  project)
    [ -n "$PROJECT_DIR" ] || err "--project-dir is required when --target=project"
    [ -d "$PROJECT_DIR" ] || err "project directory does not exist: $PROJECT_DIR"
    DEST_DIR="${PROJECT_DIR}/.claude"
    DEST_CLAUDE_MD="${PROJECT_DIR}/CLAUDE.md"
    DEST_AGENTS_DIR="${PROJECT_DIR}/.claude/agents"
    DEST_TEMPLATES_DIR="${PROJECT_DIR}/.claude/templates"
    DEST_SKILLS_DIR="${PROJECT_DIR}/.claude/skills"
    DEST_MODULES_DIR="${PROJECT_DIR}/.claude/modules"
    # Project slug = basename(resolved-absolute-path) with hyphens and dots
    # normalized to underscores. This becomes both the file-suffix and the
    # {{NAME_SUFFIX}} value in CAPTAIN frontmatter so MAJOR_PLINY can dispatch
    # by the deployed name. Resolve to absolute path first so --project-dir .
    # produces the actual containing-directory name (e.g. widget_builder)
    # rather than an underscore (basename "." returns "."). Fixes stoa--8o4.
    PROJECT_SLUG="$(basename "$(cd "$PROJECT_DIR" && pwd)" | tr '.-' '__')"
    NAME_SUFFIX="_${PROJECT_SLUG}"
    ;;
  subproject)
    [ -n "$PARENT_DIR" ]  || err "--parent-dir is required when --target=subproject"
    [ -n "$SUBPROJECT" ]  || err "--subproject is required when --target=subproject"
    [ -d "$PARENT_DIR" ]  || err "parent directory does not exist: $PARENT_DIR"
    # Sanity-check the parent dir actually looks like a deployed project — we
    # don't require it, but a missing .claude/ on the parent is a strong hint
    # the human pointed at the wrong path.
    if [ ! -d "${PARENT_DIR}/.claude" ]; then
      echo "install.sh: warning: parent directory has no .claude/ — is ${PARENT_DIR} actually a deployed project? proceeding anyway." >&2
    fi
    # Subproject slug validation: must be a safe single-segment directory name.
    # Reject empty, path separators, leading dots, and parent-traversal forms.
    case "$SUBPROJECT" in
      ""|.|..)             err "invalid --subproject slug: $SUBPROJECT" ;;
      */*|*\\*)            err "--subproject slug must not contain path separators: $SUBPROJECT" ;;
      .*)                  err "--subproject slug must not start with '.': $SUBPROJECT" ;;
    esac
    case "$SUBPROJECT" in
      *[!A-Za-z0-9._-]*)   err "--subproject slug must contain only [A-Za-z0-9._-]: $SUBPROJECT" ;;
    esac
    # Subproject mode incompatible with --modify-claude-md: the sub-project
    # does not get its own CLAUDE.md, and the parent's must not be touched.
    [ "$MODIFY_CLAUDE_MD" -eq 0 ] || err "--modify-claude-md is not valid with --target=subproject (sub-project does not get its own CLAUDE.md, and the parent's must not be modified by this run)"
    # Subproject mode forces no-templates: the sub-project shares the parent's
    # runtime tooling at <parent>/.claude/templates/. If the human explicitly
    # passed --no-templates that's harmless and consistent; if they didn't,
    # we silently force it (the default would be to deploy templates).
    WITH_TEMPLATES=0
    DEST_DIR="${PARENT_DIR}/${SUBPROJECT}/.claude"
    DEST_CLAUDE_MD=""  # not used in subproject mode
    DEST_AGENTS_DIR="${PARENT_DIR}/${SUBPROJECT}/.claude/agents"
    DEST_TEMPLATES_DIR=""  # not used in subproject mode
    DEST_SKILLS_DIR="${PARENT_DIR}/${SUBPROJECT}/.claude/skills"
    # Modules: subproject-tier deploy is a TRACKED Arc-2-gating open question
    # (stoa--xyb.4 §6 — Read-tool relative-path resolution at subproject tier is
    # web-confirmed contested). Arc 1 wires user + project tiers only; empty here
    # so the deploy step's [ -n "$DEST_MODULES_DIR" ] guard skips subproject
    # cleanly, mirroring DEST_TEMPLATES_DIR above. Do NOT assert subproject deploy
    # works until a live Read-resolution probe passes.
    DEST_MODULES_DIR=""  # not used in subproject mode (see stoa--xyb.4 §6)
    # Sub-project slug = SUBPROJECT with hyphens and dots normalized to
    # underscores. Same rule as project mode so the suffix is a valid agent
    # name component (CAPTAIN frontmatter `name:` can't contain hyphens or
    # dots in the slug part). The directory itself keeps the raw slug.
    PROJECT_SLUG="$(echo "$SUBPROJECT" | tr '.-' '__')"
    NAME_SUFFIX="_${PROJECT_SLUG}"
    SUFFIX_MAJORS=1
    ;;
  *)
    err "--target must be 'user', 'project', or 'subproject' (got: $TARGET)"
    ;;
esac

[ -f "$SRC_POLYBIUS" ]              || err "source file not found: $SRC_POLYBIUS"
[ -f "$SRC_PLINY" ]                 || err "source file not found: $SRC_PLINY"
[ -f "$SRC_OPERATING_DISCIPLINES" ] || err "source file not found: $SRC_OPERATING_DISCIPLINES"

if [ "$WITH_CAPTAINS" -eq 1 ]; then
  for name in "${CAPTAIN_NAMES[@]}"; do
    [ -f "${SCRIPT_DIR}/CAPTAIN_${name}.md" ] || err "source file not found: ${SCRIPT_DIR}/CAPTAIN_${name}.md"
  done
fi

if [ "$WITH_TEMPLATES" -eq 1 ]; then
  [ -d "$SRC_TEMPLATES_DIR" ] || err "source templates directory not found: $SRC_TEMPLATES_DIR"
  for tname in "${TEMPLATE_NAMES[@]}"; do
    [ -f "${SRC_TEMPLATES_DIR}/${tname}" ] || err "source file not found: ${SRC_TEMPLATES_DIR}/${tname}"
  done
fi

# Skills are always deployed (no opt-out flag); source-side existence check
# fires unconditionally. Each skill must be a directory containing SKILL.md
# at minimum; other files (helper scripts, templates) are copied wholesale.
[ -d "$SRC_SKILLS_DIR" ] || err "source skills directory not found: $SRC_SKILLS_DIR"
for sname in "${SKILL_NAMES[@]}"; do
  [ -d "${SRC_SKILLS_DIR}/${sname}" ] || err "source skill directory not found: ${SRC_SKILLS_DIR}/${sname}"
  [ -f "${SRC_SKILLS_DIR}/${sname}/SKILL.md" ] || err "source skill SKILL.md not found: ${SRC_SKILLS_DIR}/${sname}/SKILL.md"
done

# Modules are always deployed (no opt-out flag, mirrors skills). Source-dir must
# exist; glob-discover the module sources and assert at least one (.md) exists so
# an empty or mis-pathed source dir fails loudly rather than silently deploying
# nothing (the glob escape-hatch from stoa--xyb.4 Decision A). _src_modules is
# reused by the plan line + deploy step below.
[ -d "$SRC_MODULES_DIR" ] || err "source modules directory not found: $SRC_MODULES_DIR"
shopt -s nullglob
_src_modules=( "${SRC_MODULES_DIR}"/*.md )
shopt -u nullglob
[ "${#_src_modules[@]}" -gt 0 ] || err "no module sources found: ${SRC_MODULES_DIR}/*.md"

# ----- plan ------------------------------------------------------------------

echo "agent-substrate install — plan"
echo "  target           : $TARGET"
if [ "$TARGET" = "subproject" ]; then
  echo "  parent dir       : $PARENT_DIR"
  echo "  subproject slug  : $SUBPROJECT"
fi
echo "  destination dir  : $DEST_DIR"
if [ "$TARGET" = "subproject" ]; then
  echo "  modify CLAUDE.md : no (subproject mode never modifies CLAUDE.md)"
else
  echo "  modify CLAUDE.md : $([ "$MODIFY_CLAUDE_MD" -eq 1 ] && echo "yes (consent flag set)" || echo "no")"
fi
if [ "$SUFFIX_MAJORS" -eq 1 ]; then
  echo "  MAJOR files      : suffixed (MAJOR_POLYBIUS${NAME_SUFFIX}.md, MAJOR_PLINY${NAME_SUFFIX}.md)"
fi
echo "  deploy CAPTAINs  : $([ "$WITH_CAPTAINS" -eq 1 ] && echo "yes (11 envelopes to ${DEST_AGENTS_DIR})" || echo "no (--no-captains)")"
if [ "$WITH_CAPTAINS" -eq 1 ] && [ -n "$NAME_SUFFIX" ]; then
  echo "  CAPTAIN suffix   : ${NAME_SUFFIX} (slug: ${PROJECT_SLUG})"
fi
if [ "$TARGET" = "subproject" ]; then
  echo "  deploy templates : no (subproject shares parent's at ${PARENT_DIR}/.claude/templates/)"
else
  echo "  deploy templates : $([ "$WITH_TEMPLATES" -eq 1 ] && echo "yes (${#TEMPLATE_NAMES[@]} files to ${DEST_TEMPLATES_DIR})" || echo "no (--no-templates)")"
fi
echo "  deploy skills    : yes (${#SKILL_NAMES[@]} skills to ${DEST_SKILLS_DIR})"
if [ -n "$DEST_MODULES_DIR" ]; then
  # Count from the source glob (observable; per stoa--xyb.4 r4). Guarded for the
  # subproject-skip case (DEST_MODULES_DIR empty), matching the templates pattern.
  echo "  deploy modules   : yes (${#_src_modules[@]} module(s) to ${DEST_MODULES_DIR})"
else
  echo "  deploy modules   : no (subproject mode — see stoa--xyb.4 §6 open question)"
fi
echo "  prune obsolete   : $([ "$PRUNE_OBSOLETE" -eq 1 ] && echo "yes (--prune-obsolete)" || echo "no (warn-only)")"
echo "  dry-run          : $([ "$DRY_RUN" -eq 1 ] && echo "yes" || echo "no")"
echo

# ----- execute ---------------------------------------------------------------

# 1. Ensure destination directory exists.
if [ ! -d "$DEST_DIR" ]; then
  run_or_print "mkdir -p \"$DEST_DIR\""
else
  log "destination directory already exists: $DEST_DIR"
fi

# 2. Copy MAJOR_POLYBIUS.md and MAJOR_PLINY.md (overwrite-on-existing — idempotent).
# In subproject mode the filenames carry the _<subproject> suffix so the
# parent project's deployed-name space and the sub-project's are visibly
# distinct when both appear in the same directory tree (e.g., during ls of
# the parent's working tree). The {{NAME_SUFFIX}} sed substitution is applied
# defensively so that if these files later grow placeholders parallel to the
# CAPTAINs, no separate code path is needed; today the source files contain
# no {{NAME_SUFFIX}} placeholder so the substitution is a no-op.
if [ "$SUFFIX_MAJORS" -eq 1 ]; then
  DEST_POLYBIUS="${DEST_DIR}/MAJOR_POLYBIUS${NAME_SUFFIX}.md"
  DEST_PLINY="${DEST_DIR}/MAJOR_PLINY${NAME_SUFFIX}.md"
else
  DEST_POLYBIUS="${DEST_DIR}/MAJOR_POLYBIUS.md"
  DEST_PLINY="${DEST_DIR}/MAJOR_PLINY.md"
fi
# Arc 20: also substitute {{USER_TIER_DIR}} placeholder. At user-tier this is
# the chosen user-tier dir from choose_user_tier_dir (above). At project-tier
# and subproject-tier, USER_TIER_DIR is empty — substituting empty here would
# corrupt the file, so the placeholder stays literal at project/subproject tiers
# (the role file's user-tier paths are operationally relevant only at user-tier;
# project-tier MAJOR_POLYBIUS doesn't need them resolved).
# Use a sed delimiter ('|') that doesn't appear in filesystem paths, so we can
# substitute paths (which contain '/') without per-character escaping. '|' is
# illegal in Windows paths and rare elsewhere; defensive guard surfaces if a
# user-tier path includes it.
if [ -n "$USER_TIER_DIR" ]; then
  case "$USER_TIER_DIR" in
    *"|"*) err "user-tier dir contains '|' which conflicts with sed delimiter; pick another path" ;;
  esac
fi

if [ "$DRY_RUN" -eq 1 ]; then
  echo "[dry-run] deploy: $SRC_POLYBIUS -> $DEST_POLYBIUS (substitute {{NAME_SUFFIX}} -> '${NAME_SUFFIX}'$([ -n "$USER_TIER_DIR" ] && echo ", {{USER_TIER_DIR}} -> '${USER_TIER_DIR}'"))"
  echo "[dry-run] deploy: $SRC_PLINY -> $DEST_PLINY (substitute {{NAME_SUFFIX}} -> '${NAME_SUFFIX}')"
else
  if [ -n "$USER_TIER_DIR" ]; then
    sed -e "s/{{NAME_SUFFIX}}/${NAME_SUFFIX}/g" -e "s|{{USER_TIER_DIR}}|${USER_TIER_DIR}|g" "$SRC_POLYBIUS" > "$DEST_POLYBIUS"
  else
    sed "s/{{NAME_SUFFIX}}/${NAME_SUFFIX}/g" "$SRC_POLYBIUS" > "$DEST_POLYBIUS"
  fi
  sed "s/{{NAME_SUFFIX}}/${NAME_SUFFIX}/g" "$SRC_PLINY" > "$DEST_PLINY"
  echo "deployed: $DEST_POLYBIUS"
  echo "deployed: $DEST_PLINY"
fi

# 2b. Deploy operating-disciplines.md — team-wide disciplines doc referenced
# from MAJOR_POLYBIUS §4 and MAJOR_PLINY §7. Lands as a sibling of the MAJOR
# files at <DEST_DIR>/operating-disciplines.md so the role-file references
# (which use the bare name "operating-disciplines.md") resolve in the deployed
# location. Same path semantics as the source repo (substrate/operating-
# disciplines.md is a sibling of substrate/MAJOR_*.md). Universal — deployed
# at all three target modes (user, project, subproject); each tier needs its
# own local copy because Claude Code role-file path resolution is relative to
# where the role file lives. No suffix on the filename: this is a shared doc,
# not a role file.
DEST_OPERATING_DISCIPLINES="${DEST_DIR}/operating-disciplines.md"
if [ "$DRY_RUN" -eq 1 ]; then
  echo "[dry-run] deploy: $SRC_OPERATING_DISCIPLINES -> $DEST_OPERATING_DISCIPLINES"
else
  cp "$SRC_OPERATING_DISCIPLINES" "$DEST_OPERATING_DISCIPLINES"
  echo "deployed: $DEST_OPERATING_DISCIPLINES"
fi

# 3. Deploy CAPTAIN sub-agent envelopes (default on; --no-captains skips).
if [ "$WITH_CAPTAINS" -eq 1 ]; then
  if [ ! -d "$DEST_AGENTS_DIR" ]; then
    run_or_print "mkdir -p \"$DEST_AGENTS_DIR\""
  else
    log "agents directory already exists: $DEST_AGENTS_DIR"
  fi

  for name in "${CAPTAIN_NAMES[@]}"; do
    src="${SCRIPT_DIR}/CAPTAIN_${name}.md"
    dest="${DEST_AGENTS_DIR}/CAPTAIN_${name}${NAME_SUFFIX}.md"

    # Substitute {{NAME_SUFFIX}} in the YAML frontmatter `name:` field.
    # At user-tier NAME_SUFFIX is empty; at project-tier it is _<project-slug>.
    # sed handles the transform; the source file is unchanged.
    if [ "$DRY_RUN" -eq 1 ]; then
      echo "[dry-run] deploy: $src -> $dest (substitute {{NAME_SUFFIX}} -> '${NAME_SUFFIX}')"
    else
      sed "s/{{NAME_SUFFIX}}/${NAME_SUFFIX}/g" "$src" > "$dest"
      echo "deployed: $dest"
    fi
  done
else
  log "CAPTAIN deployment skipped (--no-captains)"
fi

# 4. Deploy templates/ runtime tooling (default on; --no-templates skips).
# Templates are POLYBIUS's working tools — paste-instruction template,
# onboarding-questions, consent-prompts. Deployed unsuffixed at both tiers
# (they're shared tooling, not agent-shaped). Re-deploys overwrite in place,
# which is idempotent for unchanged source.
if [ "$WITH_TEMPLATES" -eq 1 ]; then
  if [ ! -d "$DEST_TEMPLATES_DIR" ]; then
    run_or_print "mkdir -p \"$DEST_TEMPLATES_DIR\""
  else
    log "templates directory already exists: $DEST_TEMPLATES_DIR"
  fi

  for tname in "${TEMPLATE_NAMES[@]}"; do
    src="${SRC_TEMPLATES_DIR}/${tname}"
    dest="${DEST_TEMPLATES_DIR}/${tname}"
    run_or_print "cp \"$src\" \"$dest\""
  done
else
  log "templates deployment skipped (--no-templates)"
fi

# 5. Deploy LIEUTENANT skills (always; A1 lock-in — no opt-out flag).
# Skills land at <DEST>/.claude/skills/<name>/. Each skill subtree is copied
# wholesale (cp -R) so SKILL.md plus any helper files / sub-templates ride
# along. Unsuffixed at every tier (skills are universal, not project-named);
# subproject mode deploys here too because Claude Code loads skills from the
# active project's .claude/skills/ — it doesn't walk up to a parent.
if [ ! -d "$DEST_SKILLS_DIR" ]; then
  run_or_print "mkdir -p \"$DEST_SKILLS_DIR\""
else
  log "skills directory already exists: $DEST_SKILLS_DIR"
fi

for sname in "${SKILL_NAMES[@]}"; do
  src_skill="${SRC_SKILLS_DIR}/${sname}"
  dest_skill="${DEST_SKILLS_DIR}/${sname}"
  if [ "$DRY_RUN" -eq 1 ]; then
    echo "[dry-run] deploy skill: $src_skill/ -> $dest_skill/ (cp -R)"
    echo "[dry-run] post-copy pycache cleanup: $dest_skill (find __pycache__/*.pyc -delete)"
  else
    # Remove any pre-existing dest skill subtree before re-copying so a
    # removed file inside the skill (e.g., a deleted helper) does not
    # linger. The skill-level prune is targeted (only the named skill);
    # cross-skill staleness is handled in step 7.
    rm -rf "$dest_skill"
    mkdir -p "$dest_skill"
    cp -R "$src_skill"/. "$dest_skill"/
    # Arc 40 / stoa--t9u: post-copy Python-bytecode cleanup. If the source
    # skill subtree contains __pycache__/ directories or stray *.pyc files
    # (e.g., because a deployed helper ran at least once in the source
    # worktree), cp -R copies them wholesale. Strip them after the copy so
    # target tiers carry no bytecode the consumer did not author. Two
    # finds (one per artifact class) for cleaner audit trail; `2>/dev/null
    # || true` defends against find/rm portability variance across Git
    # Bash / macOS / Linux without breaking deploy on any one platform's
    # find quirks. Source-side cleanliness is orthogonal (handled by the
    # source repo's .gitignore __pycache__/+*.pyc rule per Arc 39
    # f707bc6).
    find "$dest_skill" -type d -name __pycache__ -prune -exec rm -rf {} + 2>/dev/null || true
    find "$dest_skill" -type f -name '*.pyc' -delete 2>/dev/null || true
    echo "deployed skill: $dest_skill"
  fi
done

# 5b. Deploy instruction modules (Arc 44 / stoa--xyb.4; always — no opt-out,
# mirrors skills). GLOB-discovered flat .md files from substrate/modules/,
# deployed unsuffixed (shared tooling like templates). cp overwrites in place
# (idempotent for unchanged source). Enumerated/logged so the deploy is
# observable in stdout (per r4). Skipped in subproject mode (DEST_MODULES_DIR
# empty — TRACKED Arc-2-gating open question, stoa--xyb.4 §6).
if [ -n "$DEST_MODULES_DIR" ]; then
  if [ ! -d "$DEST_MODULES_DIR" ]; then
    run_or_print "mkdir -p \"$DEST_MODULES_DIR\""
  else
    log "modules directory already exists: $DEST_MODULES_DIR"
  fi
  shopt -s nullglob
  for src in "${SRC_MODULES_DIR}"/*.md; do
    mname="$(basename "$src")"
    dest="${DEST_MODULES_DIR}/${mname}"
    log "deploy module: ${mname}"   # enumerate/log each deployed module (r4 observability)
    run_or_print "cp \"$src\" \"$dest\""
  done
  shopt -u nullglob
else
  log "modules deployment skipped (subproject mode — see stoa--xyb.4 §6)"
fi

# 6. Optionally append reference to CLAUDE.md (informed consent required).
if [ "$MODIFY_CLAUDE_MD" -eq 1 ]; then
  if [ -f "$DEST_CLAUDE_MD" ] && grep -Fq "$CLAUDE_MD_MARKER" "$DEST_CLAUDE_MD" 2>/dev/null; then
    log "CLAUDE.md already references POLYBIUS — skipping append (idempotent)"
  else
    BLOCK="

${CLAUDE_MD_MARKER}
## Chief-of-Staff (MAJOR_POLYBIUS)

This environment hosts the three-role agent substrate. The Chief-of-Staff role is defined in \`.claude/MAJOR_POLYBIUS.md\`. When the PRINCIPAL invokes \"POLYBIUS\" or \"chief of staff\", read that file and assume the role.
"
    if [ "$DRY_RUN" -eq 1 ]; then
      if [ -f "$DEST_CLAUDE_MD" ]; then
        echo "[dry-run] would back up existing CLAUDE.md to: $DEST_CLAUDE_MD.bak"
      fi
      echo "[dry-run] would append POLYBIUS reference block to: $DEST_CLAUDE_MD"
      echo "[dry-run] block contents:"
      printf '%s\n' "$BLOCK" | sed 's/^/[dry-run]   /'
    else
      # Back up existing CLAUDE.md before any modification — safety net so the
      # pre-modification file is recoverable if the append produces unexpected
      # content. Single-shot backup (overwritten on each run); git history is
      # the long-term archive.
      if [ -f "$DEST_CLAUDE_MD" ]; then
        cp "$DEST_CLAUDE_MD" "$DEST_CLAUDE_MD.bak"
        echo "backed up existing CLAUDE.md to: $DEST_CLAUDE_MD.bak"
      fi
      printf '%s\n' "$BLOCK" >> "$DEST_CLAUDE_MD"
      echo "appended POLYBIUS reference to: $DEST_CLAUDE_MD"
    fi
  fi
else
  log "CLAUDE.md modification skipped (no --modify-claude-md flag; consent not given)"
fi

# 6b. Separate marker-bounded block: base-vs-custom convention paths (Arc 29; D6).
# Gated by the same --modify-claude-md consent flag as the POLYBIUS reference
# block above. Independent marker (CLAUDE_MD_BASE_VS_CUSTOM_MARKER) so the two
# blocks are separately idempotent — operator who edits between the two blocks
# without removing either marker re-runs cleanly. Discipline reference:
# substrate/operating-disciplines.md §23 + substrate/MAJOR_POLYBIUS.md §17.
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
      # Backup of CLAUDE.md already taken in the POLYBIUS-block branch above
      # (single-shot backup per run is the existing convention); only append
      # here.
      printf '%s\n' "$BVC_BLOCK" >> "$DEST_CLAUDE_MD"
      echo "appended base-vs-custom convention block to: $DEST_CLAUDE_MD"
    fi
  fi
fi

# 7. Staleness detection (stoa--w1t). Scans deployed dirs for files no longer
# in the substrate source — typically left over from a renamed CAPTAIN,
# removed template, or removed skill. Default is warn-only (lists obsolete
# paths so the human can rm manually if preferred); --prune-obsolete enables
# automatic removal.
#
# Scope:
# - CAPTAIN_*.md files in DEST_AGENTS_DIR whose mnemonic is no longer in
#   CAPTAIN_NAMES (suffix-aware: at user-tier the file is CAPTAIN_<MNEM>.md;
#   at project/subproject-tier it is CAPTAIN_<MNEM>${NAME_SUFFIX}.md).
# - Files in DEST_TEMPLATES_DIR not in TEMPLATE_NAMES.
# - Subdirectories of DEST_SKILLS_DIR not in SKILL_NAMES.
# - Files in DEST_MODULES_DIR not in the substrate/modules/*.md source glob.
#
# Deliberately NOT scanned:
# - MAJOR_*.md files. Pair-programmer Majors (PYTHAGORAS, ATTICUS, etc.)
#   land in the same agents/ directory and cannot be reliably distinguished
#   from substrate-canonical MAJORs by filename. The renamed-MAJOR case is
#   rare; manual rm is the safer path.
# - Categories the current run did not deploy. If --no-captains was passed,
#   the human explicitly opted out of managing CAPTAINs this run; treating
#   their other CAPTAIN files as "obsolete" creates noise. Skills always
#   scan (no opt-out flag exists for skills).
#
# The scan is read-only inspection unless --prune-obsolete is set, so
# running it in dry-run mode is safe; removal in dry-run prints the rm
# command without executing.
obsolete_files=()

if [ "$WITH_CAPTAINS" -eq 1 ] && [ -d "$DEST_AGENTS_DIR" ]; then
  # CITE: this glob is single-path-segment (NOT recursive) — it matches
  # CAPTAIN_*.md files directly under ${DEST_AGENTS_DIR} but NOT files at
  # ${DEST_AGENTS_DIR}/custom/CAPTAIN_*.md. That non-recursion IS the base-vs-
  # custom scoping; see substrate/operating-disciplines.md §23 + substrate/
  # MAJOR_POLYBIUS.md §17. If a future change makes this glob recursive
  # (e.g., to find sub-directory CAPTAINs for some other reason), the
  # base-vs-custom invariant breaks — custom CAPTAINs would be classified
  # as obsolete and pruned by --prune-obsolete. The discipline is at the
  # path-shape level: substrate tools see only base; custom is operator-owned.
  shopt -s nullglob
  for f in "${DEST_AGENTS_DIR}/CAPTAIN_"*"${NAME_SUFFIX}.md"; do
    base=$(basename "$f")
    mnemonic="${base#CAPTAIN_}"
    mnemonic="${mnemonic%${NAME_SUFFIX}.md}"
    found=0
    for n in "${CAPTAIN_NAMES[@]}"; do
      if [ "$n" = "$mnemonic" ]; then
        found=1
        break
      fi
    done
    if [ "$found" -eq 0 ]; then
      obsolete_files+=("$f")
    fi
  done
  shopt -u nullglob
fi

if [ "$WITH_TEMPLATES" -eq 1 ] && [ -n "$DEST_TEMPLATES_DIR" ] && [ -d "$DEST_TEMPLATES_DIR" ]; then
  # CITE: this glob is single-path-segment + file-only (the `[ -f "$f" ]`
  # filter skips directories). It does NOT recurse into
  # ${DEST_TEMPLATES_DIR}/custom/, where custom templates live per the
  # base-vs-custom convention (substrate/operating-disciplines.md §23 +
  # substrate/MAJOR_POLYBIUS.md §17). If a future change makes this glob
  # recursive, custom templates would be flagged as obsolete; the discipline
  # is at the path-shape level.
  shopt -s nullglob
  for f in "${DEST_TEMPLATES_DIR}"/*; do
    [ -f "$f" ] || continue
    base=$(basename "$f")
    found=0
    for t in "${TEMPLATE_NAMES[@]}"; do
      if [ "$t" = "$base" ]; then
        found=1
        break
      fi
    done
    if [ "$found" -eq 0 ]; then
      obsolete_files+=("$f")
    fi
  done
  shopt -u nullglob
fi

if [ -d "$DEST_SKILLS_DIR" ]; then
  shopt -s nullglob
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
  shopt -u nullglob
fi

# Modules staleness (Arc 44 / stoa--xyb.4). GLOB-based: compare the deployed
# .claude/modules/ against the SOURCE glob (substrate/modules/*.md), not an
# array — so the scan auto-covers any module Arc 2+ adds with no edit here. File-
# only single-segment shape (the `[ -f "$f" ]` filter skips directories), the
# same idiom the templates scan above uses. Skipped in subproject mode
# (DEST_MODULES_DIR empty — stoa--xyb.4 §6).
if [ -n "${DEST_MODULES_DIR:-}" ] && [ -d "$DEST_MODULES_DIR" ]; then
  shopt -s nullglob
  # Build the source basename set from the glob (no array to compare against).
  declare -A _src_module_set=()
  for s in "${SRC_MODULES_DIR}"/*.md; do _src_module_set["$(basename "$s")"]=1; done
  for f in "${DEST_MODULES_DIR}"/*; do
    [ -f "$f" ] || continue
    base=$(basename "$f")
    if [ -z "${_src_module_set[$base]:-}" ]; then obsolete_files+=("$f"); fi
  done
  shopt -u nullglob
fi

if [ "${#obsolete_files[@]}" -gt 0 ]; then
  echo
  echo "Obsolete files detected at destination (not in current substrate):"
  for f in "${obsolete_files[@]}"; do
    echo "  - $f"
  done
  echo
  echo "Note: at user-tier the destination may contain files from other"
  echo "substrates (e.g., agent-gauntlet skills installed via plugin) or"
  echo "manual additions. Review the list before running --prune-obsolete;"
  echo "this script cannot distinguish a substrate-rename leftover from a"
  echo "deliberate cross-substrate install. The stoa--w1t case (renamed"
  echo "CAPTAIN_PLINY → CAPTAIN_ZENO) is the canonical removal target."
  if [ "$PRUNE_OBSOLETE" -eq 1 ]; then
    echo
    echo "Removing (--prune-obsolete):"
    for f in "${obsolete_files[@]}"; do
      if [ "$DRY_RUN" -eq 1 ]; then
        echo "[dry-run] rm -rf \"$f\""
      else
        rm -rf "$f"
        echo "  removed: $f"
      fi
    done
  else
    echo
    echo "Run with --prune-obsolete to remove, or rm manually."
  fi
fi

# 7c. Write substrate manifest (Arc 38 / bj5 / A8). Records substitutions applied
# to deployed files so check.sh + apply.sh can normalize before diffing. Universal
# across all 3 tiers (the load-bearing user-tier case is the {{USER_TIER_DIR}}
# substitution in MAJOR_POLYBIUS.md; project-tier + subproject-tier write
# informational manifests with derivable {{NAME_SUFFIX}} entries).
write_substrate_manifest "$DEST_DIR" "$TARGET" "$PROJECT_SLUG"

# 7b. Operator visibility: surface custom files that coexist at the convention
# paths. Read-only; substrate tools never touch these. The discipline is at
# substrate/operating-disciplines.md §23 + substrate/MAJOR_POLYBIUS.md §17.
# Surfacing the count tells the operator "the convention is working —
# substrate updates left your customizations alone." Silence here would
# leave the operator wondering whether the convention is in effect.
#
# Gating: CAPTAIN/template count blocks gate on WITH_CAPTAINS / WITH_TEMPLATES
# respectively, mirroring the existing CAPTAIN-staleness-scan gate (above at
# the obsolete_files CAPTAIN loop) and the templates-staleness-scan gate
# (above at the obsolete_files templates loop). Skills count is always-print:
# there is no --no-skills deploy flag, so no corresponding gate exists
# upstream. The shape preserves "opt-out means substrate stays silent" for
# the operator who passed --no-captains or --no-templates — they get no
# count line for the class they opted out of.
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
  [ "$custom_captain_count"  -gt 0 ] && printf '  - %-3s custom %s at %s\n' "${custom_captain_count}"  "CAPTAIN(s)"  "${DEST_AGENTS_DIR}/custom/"
  [ "$custom_template_count" -gt 0 ] && printf '  - %-3s custom %s at %s\n' "${custom_template_count}" "template(s)" "${DEST_TEMPLATES_DIR}/custom/"
  [ "$custom_skill_count"    -gt 0 ] && printf '  - %-3s custom %s at %s\n' "${custom_skill_count}"    "skill(s)"    "${DEST_SKILLS_DIR}/custom-*/"
fi

echo
echo "install.sh: done ($([ "$DRY_RUN" -eq 1 ] && echo "dry-run, no writes" || echo "applied"))"

# 8. Next-step guidance on a real (non-dry-run) install. Tells the human what
# they actually do next, so they aren't left staring at a "done" line wondering
# how to activate the substrate. Suppressed in dry-run because nothing was
# actually deployed.
if [ "$DRY_RUN" -eq 0 ]; then
  case "$TARGET" in
    project)
      ACTIVATE_DIR="$PROJECT_DIR"
      PASTE_PATH="${PROJECT_DIR}/HUMAN_paste-orchestrator-instruction.md"
      ;;
    user)
      ACTIVATE_DIR="any project directory (this install is user-tier — available everywhere)"
      PASTE_PATH="<project>/HUMAN_paste-orchestrator-instruction.md (per-project, written at first use)"
      ;;
    subproject)
      ACTIVATE_DIR="${PARENT_DIR}/${SUBPROJECT}"
      PASTE_PATH="${PARENT_DIR}/${SUBPROJECT}/HUMAN_paste-orchestrator-instruction.md (written by sub-project POLYBIUS at first use)"
      ;;
  esac

  # Mode-aware ACTIVATION block. Two activation patterns per
  # MAJOR_POLYBIUS.md §5.5 + substrate/templates/activation-paste-cheatsheet.md:
  #   - say-trigger: --target user, OR --target project --modify-claude-md
  #   - paste-trigger: --target project (no --modify-claude-md), OR --target subproject
  # The previous version of this block lumped --target project (no --modify-claude-md)
  # into the say-trigger branch by gating only on $TARGET = subproject. That was the
  # arc-21 bug fix: project-mode without --modify-claude-md does not wire CLAUDE.md
  # auto-load, so saying POLYBIUS does nothing — activation IS the literal paste.
  echo
  if [ "$TARGET" = "subproject" ] || ( [ "$TARGET" = "project" ] && [ "$MODIFY_CLAUDE_MD" -eq 0 ] ); then
    # Paste-trigger pattern.
    # MAJOR filename suffixing is asymmetric with CAPTAIN suffixing: MAJORs
    # are suffixed only at sub-project tier, unsuffixed at project tier even
    # when CAPTAINs are suffixed there. The activation paste must match the
    # deployed filename, so gate on $TARGET = subproject (the only mode that
    # suffixes MAJORs) rather than on NAME_SUFFIX.
    if [ "$TARGET" = "subproject" ]; then
      ROLE_DESCRIPTOR="sub-project"
      MAJOR_PATH=".claude/MAJOR_POLYBIUS${NAME_SUFFIX}.md"
    else
      ROLE_DESCRIPTOR="project"
      MAJOR_PATH=".claude/MAJOR_POLYBIUS.md"
    fi
    echo "========================================"
    echo "  ACTIVATION (copy line 3 into a new"
    echo "  Claude Code session in ${ACTIVATE_DIR})"
    echo "========================================"
    echo
    echo "  1. cd into ${ACTIVATE_DIR}"
    echo "  2. Open Claude Code:  claude"
    echo "  3. Paste:"
    echo
    echo "     Read ${MAJOR_PATH} and assume"
    echo "     the role for this ${ROLE_DESCRIPTOR}."
    echo
    echo "========================================"
    echo
    if [ "$TARGET" = "subproject" ]; then
      echo "The sub-project shares the parent's git repo and bw — no bw init needed."
      echo "Templates live at ${PARENT_DIR}/.claude/templates/ (sub-project reads"
      echo "from there; nothing was deployed under ${DEST_DIR}/templates/)."
      echo
      echo "Once the sub-project's POLYBIUS is up, it will write its activation paste"
      echo "for the sub-project's MAJOR_PLINY at:"
      echo "  ${PASTE_PATH}"
    else
      echo "Activation is the literal paste — there is no CLAUDE.md auto-load wired"
      echo "in this mode (--modify-claude-md was not passed). For the say-trigger"
      echo "experience, re-run install.sh with --modify-claude-md."
      echo
      echo "After onboarding completes, MAJOR_POLYBIUS keeps the latest MAJOR_PLINY"
      echo "activation paste at:"
      echo "  ${PASTE_PATH}"
      echo "for re-paste recovery after a /compact or /clear."
    fi
  else
    # Say-trigger pattern (--target user, OR --target project --modify-claude-md).
    echo "========================================"
    echo "  ACTIVATION"
    echo "========================================"
    echo
    echo "  1. cd into ${ACTIVATE_DIR}"
    echo "  2. Open Claude Code:  claude"
    echo "  3. Say \"POLYBIUS\" or \"chief of staff\" — the role auto-loads"
    echo "     via CLAUDE.md and walks you through onboarding."
    echo
    echo "========================================"
    echo
    echo "After onboarding completes, MAJOR_POLYBIUS keeps the latest MAJOR_PLINY"
    echo "activation paste at:"
    echo "  ${PASTE_PATH}"
    echo "for re-paste recovery after a /compact or /clear."
  fi
fi
