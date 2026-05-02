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
# tooling (unless --no-templates), and optionally appends a marker-bounded
# reference block to CLAUDE.md when the consent flag is set. It does NOT run
# `bw init`, create skills, or write the paste-instruction; POLYBIUS handles
# those interactively with the PRINCIPAL in the loop.
#
# Usage:
#   ./install.sh --target user [--modify-claude-md] [--no-captains] [--no-templates] [--dry-run]
#   ./install.sh --target project --project-dir <path> [--modify-claude-md] [--no-captains] [--no-templates] [--dry-run]
#   ./install.sh --target subproject --parent-dir <path> --subproject <slug> [--no-captains] [--dry-run]
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
MODIFY_CLAUDE_MD=0
DRY_RUN=0
WITH_CAPTAINS=1
WITH_TEMPLATES=1

# Source files live next to this script.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC_POLYBIUS="${SCRIPT_DIR}/MAJOR_POLYBIUS.md"
SRC_PLINY="${SCRIPT_DIR}/MAJOR_PLINY.md"
SRC_TEMPLATES_DIR="${SCRIPT_DIR}/templates"

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
  PLINY
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
    PROJECT_SLUG=""
    NAME_SUFFIX=""
    ;;
  project)
    [ -n "$PROJECT_DIR" ] || err "--project-dir is required when --target=project"
    [ -d "$PROJECT_DIR" ] || err "project directory does not exist: $PROJECT_DIR"
    DEST_DIR="${PROJECT_DIR}/.claude"
    DEST_CLAUDE_MD="${PROJECT_DIR}/CLAUDE.md"
    DEST_AGENTS_DIR="${PROJECT_DIR}/.claude/agents"
    DEST_TEMPLATES_DIR="${PROJECT_DIR}/.claude/templates"
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
if [ "$DRY_RUN" -eq 1 ]; then
  echo "[dry-run] deploy: $SRC_POLYBIUS -> $DEST_POLYBIUS (substitute {{NAME_SUFFIX}} -> '${NAME_SUFFIX}')"
  echo "[dry-run] deploy: $SRC_PLINY -> $DEST_PLINY (substitute {{NAME_SUFFIX}} -> '${NAME_SUFFIX}')"
else
  sed "s/{{NAME_SUFFIX}}/${NAME_SUFFIX}/g" "$SRC_POLYBIUS" > "$DEST_POLYBIUS"
  sed "s/{{NAME_SUFFIX}}/${NAME_SUFFIX}/g" "$SRC_PLINY"    > "$DEST_PLINY"
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

# 5. Optionally append reference to CLAUDE.md (informed consent required).
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

echo
echo "install.sh: done ($([ "$DRY_RUN" -eq 1 ] && echo "dry-run, no writes" || echo "applied"))"

# 6. Next-step guidance on a real (non-dry-run) install. Tells the human what
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
