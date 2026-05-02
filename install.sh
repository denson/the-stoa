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
# sub-agent envelopes (unless --no-captains), and optionally appends a
# marker-bounded reference block to CLAUDE.md when the consent flag is set.
# It does NOT run `bw init`, create skills, or write the paste-instruction;
# POLYBIUS handles those interactively with the Colonel in the loop.
#
# Usage:
#   ./install.sh --target user [--modify-claude-md] [--no-captains] [--dry-run]
#   ./install.sh --target project --project-dir <path> [--modify-claude-md] [--no-captains] [--dry-run]
#   ./install.sh --help
#
# Idempotency: re-running with the same flags is safe. Files are overwritten
# in place; CLAUDE.md appends are guarded by a marker check so the reference is
# added at most once.
#
# CAPTAIN envelopes: by default the script deploys the 10 CAPTAIN_*.md sub-agent
# envelopes from this directory to <target>/.claude/agents/. At project-tier the
# files are suffixed with _<sanitized-project> (e.g. CAPTAIN_DAEDALUS_my_project.md)
# and the {{NAME_SUFFIX}} slot in the YAML frontmatter's `name:` field is filled
# accordingly; at user-tier the files are unsuffixed and {{NAME_SUFFIX}} expands
# to empty. Pass --no-captains to skip CAPTAIN deployment.
#
# Dry-run: --dry-run prints every action without writing anything.

set -euo pipefail

# ----- defaults --------------------------------------------------------------

TARGET=""
PROJECT_DIR=""
MODIFY_CLAUDE_MD=0
DRY_RUN=0
WITH_CAPTAINS=1

# Source files live next to this script.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC_POLYBIUS="${SCRIPT_DIR}/MAJOR_POLYBIUS.md"
SRC_PLINY="${SCRIPT_DIR}/MAJOR_PLINY.md"

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
      [ "$#" -ge 2 ] || err "--target requires a value (user|project)"
      TARGET="$2"
      shift 2
      ;;
    --project-dir)
      [ "$#" -ge 2 ] || err "--project-dir requires a path"
      PROJECT_DIR="$2"
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
    -h|--help)
      usage 0
      ;;
    *)
      err "unknown argument: $1 (try --help)"
      ;;
  esac
done

# ----- validation ------------------------------------------------------------

[ -n "$TARGET" ] || err "--target is required (user|project)"

case "$TARGET" in
  user)
    DEST_DIR="${HOME}/.claude"
    DEST_CLAUDE_MD="${HOME}/.claude/CLAUDE.md"
    DEST_AGENTS_DIR="${HOME}/.claude/agents"
    PROJECT_SLUG=""
    NAME_SUFFIX=""
    ;;
  project)
    [ -n "$PROJECT_DIR" ] || err "--project-dir is required when --target=project"
    [ -d "$PROJECT_DIR" ] || err "project directory does not exist: $PROJECT_DIR"
    DEST_DIR="${PROJECT_DIR}/.claude"
    DEST_CLAUDE_MD="${PROJECT_DIR}/CLAUDE.md"
    DEST_AGENTS_DIR="${PROJECT_DIR}/.claude/agents"
    # Project slug = basename(project-dir) with hyphens and dots normalized to
    # underscores. This becomes both the file-suffix and the {{NAME_SUFFIX}}
    # value in CAPTAIN frontmatter so MAJOR_PLINY can dispatch by the deployed
    # name.
    PROJECT_SLUG="$(basename "$PROJECT_DIR" | tr '.-' '__')"
    NAME_SUFFIX="_${PROJECT_SLUG}"
    ;;
  *)
    err "--target must be 'user' or 'project' (got: $TARGET)"
    ;;
esac

[ -f "$SRC_POLYBIUS" ] || err "source file not found: $SRC_POLYBIUS"
[ -f "$SRC_PLINY" ]    || err "source file not found: $SRC_PLINY"

if [ "$WITH_CAPTAINS" -eq 1 ]; then
  for name in "${CAPTAIN_NAMES[@]}"; do
    [ -f "${SCRIPT_DIR}/CAPTAIN_${name}.md" ] || err "source file not found: ${SCRIPT_DIR}/CAPTAIN_${name}.md"
  done
fi

# ----- plan ------------------------------------------------------------------

echo "agent-substrate install — plan"
echo "  target           : $TARGET"
echo "  destination dir  : $DEST_DIR"
echo "  modify CLAUDE.md : $([ "$MODIFY_CLAUDE_MD" -eq 1 ] && echo "yes (consent flag set)" || echo "no")"
echo "  deploy CAPTAINs  : $([ "$WITH_CAPTAINS" -eq 1 ] && echo "yes (10 envelopes to ${DEST_AGENTS_DIR})" || echo "no (--no-captains)")"
if [ "$WITH_CAPTAINS" -eq 1 ] && [ -n "$NAME_SUFFIX" ]; then
  echo "  CAPTAIN suffix   : ${NAME_SUFFIX} (project slug: ${PROJECT_SLUG})"
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
run_or_print "cp \"$SRC_POLYBIUS\" \"$DEST_DIR/MAJOR_POLYBIUS.md\""
run_or_print "cp \"$SRC_PLINY\" \"$DEST_DIR/MAJOR_PLINY.md\""

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

# 4. Optionally append reference to CLAUDE.md (informed consent required).
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
      echo "[dry-run] would append POLYBIUS reference block to: $DEST_CLAUDE_MD"
      echo "[dry-run] block contents:"
      printf '%s\n' "$BLOCK" | sed 's/^/[dry-run]   /'
    else
      printf '%s\n' "$BLOCK" >> "$DEST_CLAUDE_MD"
      echo "appended POLYBIUS reference to: $DEST_CLAUDE_MD"
    fi
  fi
else
  log "CLAUDE.md modification skipped (no --modify-claude-md flag; consent not given)"
fi

echo
echo "install.sh: done ($([ "$DRY_RUN" -eq 1 ] && echo "dry-run, no writes" || echo "applied"))"
