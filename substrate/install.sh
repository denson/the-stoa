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
# mechanical deploy: drops the two MAJOR role files, deploys the 10 CAPTAIN
# sub-agent envelopes (unless --no-captains), deploys the templates/ runtime
# tooling (unless --no-templates), deploys LIEUTENANT skills under
# <DEST>/.claude/skills/ (always — POLYBIUS invokes them via the Skill tool;
# no opt-out flag), and optionally appends a marker-bounded reference block
# to CLAUDE.md when the consent flag is set. It does NOT run `bw init` or
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
# CAPTAIN envelopes: by default the script deploys the 10 CAPTAIN_*.md sub-agent
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
# Staleness detection: after deploying, the script scans the destination for
# files no longer in the substrate source — typically left over from a
# renamed CAPTAIN, removed template, or removed skill. By default this is
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
# all 10 CAPTAINs are deployed with the same suffix. Subproject mode does NOT
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
USER_TIER_DIR=""        # Arc 20: user-tier directory (where user-beadwork lives + claude_projects sit)
MODIFY_CLAUDE_MD=0
DRY_RUN=0
WITH_CAPTAINS=1
WITH_TEMPLATES=1
PRUNE_OBSOLETE=0

# Source files live next to this script.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC_POLYBIUS="${SCRIPT_DIR}/MAJOR_POLYBIUS.md"
SRC_PLINY="${SCRIPT_DIR}/MAJOR_PLINY.md"
SRC_TEMPLATES_DIR="${SCRIPT_DIR}/templates"
SRC_SKILLS_DIR="${SCRIPT_DIR}/skills"

# Template filenames POLYBIUS uses at runtime. Shared tooling — deployed
# unsuffixed at both user-tier and project-tier.
TEMPLATE_NAMES=(
  paste-instruction-template.md
  onboarding-questions.md
  consent-prompts.md
)

# The 10 CAPTAIN envelope source files. Order is the gauntlet pipeline order
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
)

# LIEUTENANT skill source directories (under skills/). Each is a directory
# containing SKILL.md (and optionally other files) — the whole subtree is
# copied to <DEST>/.claude/skills/<name>/. Always deployed (no opt-out flag);
# Claude Code loads skills from <project>/.claude/skills/ or
# ~/.claude/skills/, so a deployed substrate that omits skills leaves
# POLYBIUS unable to invoke them.
SKILL_NAMES=(
  agent-author
)

# Marker line written into CLAUDE.md when --modify-claude-md is used; presence
# of this marker is how subsequent runs detect that the reference is already
# installed.
CLAUDE_MD_MARKER="<!-- agent-substrate: POLYBIUS reference -->"

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

  if [ "$num_candidates" -eq 1 ]; then
    found_parent="$candidates"
    if [ -t 0 ] && [ -t 1 ]; then
      printf "Found existing user-beadwork at %s/user-beadwork/\n" "$found_parent" >&2
      printf "Use this as your user-tier directory? Your user-tier dir would be %s. [Y/n] " "$found_parent" >&2
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
      printf "Found multiple existing user-beadwork directories:\n" >&2
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
      printf "Where do you want your user-tier directory? [default: ~/stoa_projects/] " >&2
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
    # runtime tooling at <parent>/.claude/templates/. If the user explicitly
    # passed --no-templates that's harmless and consistent; if they didn't,
    # we silently force it (the default would be to deploy templates).
    WITH_TEMPLATES=0
    DEST_DIR="${PARENT_DIR}/${SUBPROJECT}/.claude"
    DEST_CLAUDE_MD=""  # not used in subproject mode
    DEST_AGENTS_DIR="${PARENT_DIR}/${SUBPROJECT}/.claude/agents"
    DEST_TEMPLATES_DIR=""  # not used in subproject mode
    DEST_SKILLS_DIR="${PARENT_DIR}/${SUBPROJECT}/.claude/skills"
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

[ -f "$SRC_POLYBIUS" ] || err "source file not found: $SRC_POLYBIUS"
[ -f "$SRC_PLINY" ]    || err "source file not found: $SRC_PLINY"

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
echo "  deploy CAPTAINs  : $([ "$WITH_CAPTAINS" -eq 1 ] && echo "yes (10 envelopes to ${DEST_AGENTS_DIR})" || echo "no (--no-captains)")"
if [ "$WITH_CAPTAINS" -eq 1 ] && [ -n "$NAME_SUFFIX" ]; then
  echo "  CAPTAIN suffix   : ${NAME_SUFFIX} (slug: ${PROJECT_SLUG})"
fi
if [ "$TARGET" = "subproject" ]; then
  echo "  deploy templates : no (subproject shares parent's at ${PARENT_DIR}/.claude/templates/)"
else
  echo "  deploy templates : $([ "$WITH_TEMPLATES" -eq 1 ] && echo "yes (${#TEMPLATE_NAMES[@]} files to ${DEST_TEMPLATES_DIR})" || echo "no (--no-templates)")"
fi
echo "  deploy skills    : yes (${#SKILL_NAMES[@]} skills to ${DEST_SKILLS_DIR})"
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
  else
    # Remove any pre-existing dest skill subtree before re-copying so a
    # removed file inside the skill (e.g., a deleted helper) does not
    # linger. The skill-level prune is targeted (only the named skill);
    # cross-skill staleness is handled in step 7.
    rm -rf "$dest_skill"
    mkdir -p "$dest_skill"
    cp -R "$src_skill"/. "$dest_skill"/
    echo "deployed skill: $dest_skill"
  fi
done

# 6. Optionally append reference to CLAUDE.md (informed consent required).
if [ "$MODIFY_CLAUDE_MD" -eq 1 ]; then
  if [ -f "$DEST_CLAUDE_MD" ] && grep -Fq "$CLAUDE_MD_MARKER" "$DEST_CLAUDE_MD" 2>/dev/null; then
    log "CLAUDE.md already references POLYBIUS — skipping append (idempotent)"
  else
    BLOCK="

${CLAUDE_MD_MARKER}
## Chief-of-Staff (MAJOR_POLYBIUS)

This environment hosts the three-role agent substrate. The Chief-of-Staff role is defined in \`.claude/MAJOR_POLYBIUS.md\`. When the user invokes \"POLYBIUS\" or \"chief of staff\", read that file and assume the role.
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
#
# Deliberately NOT scanned:
# - MAJOR_*.md files. Pair-programmer Majors (PYTHAGORAS, ATTICUS, etc.)
#   land in the same agents/ directory and cannot be reliably distinguished
#   from substrate-canonical MAJORs by filename. The renamed-MAJOR case is
#   rare; manual rm is the safer path.
# - Categories the current run did not deploy. If --no-captains was passed,
#   the user explicitly opted out of managing CAPTAINs this run; treating
#   their other CAPTAIN files as "obsolete" creates noise. Skills always
#   scan (no opt-out flag exists for skills).
#
# The scan is read-only inspection unless --prune-obsolete is set, so
# running it in dry-run mode is safe; removal in dry-run prints the rm
# command without executing.
obsolete_files=()

if [ "$WITH_CAPTAINS" -eq 1 ] && [ -d "$DEST_AGENTS_DIR" ]; then
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

  echo
  echo "Next steps:"
  if [ "$TARGET" = "subproject" ]; then
    echo "  1. cd into the sub-project dir:         ${ACTIVATE_DIR}"
    echo "  2. Open Claude Code:                    claude"
    echo "  3. Invoke the sub-project's POLYBIUS by name (the sub-project does not"
    echo "     get its own CLAUDE.md, so auto-load is intentionally not wired):"
    echo "     \"Read .claude/MAJOR_POLYBIUS${NAME_SUFFIX}.md and assume the role.\""
    echo
    echo "The sub-project shares the parent's git repo and bw — no bw init needed."
    echo "Templates live at ${PARENT_DIR}/.claude/templates/ (sub-project reads"
    echo "from there; nothing was deployed under ${DEST_DIR}/templates/)."
    echo
    echo "Once the sub-project's POLYBIUS is up, it will write its activation paste"
    echo "for the sub-project's MAJOR_PLINY at:"
    echo "  ${PASTE_PATH}"
  else
    echo "  1. cd into the activation dir: ${ACTIVATE_DIR}"
    echo "  2. Open Claude Code:           claude"
    echo "  3. Say \"POLYBIUS\" or \"chief of staff\" — the chief-of-staff"
    echo "     role file loads and walks you through onboarding."
    echo
    echo "After onboarding completes, MAJOR_POLYBIUS keeps the latest activation"
    echo "paste at:"
    echo "  ${PASTE_PATH}"
    echo "for re-paste recovery after a /compact or /clear."
  fi
fi
