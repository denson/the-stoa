#!/usr/bin/env bash
#
# pretooluse-author-field-audit.sh — PreToolUse hard gate (design-rev1 §5.1a).
#
# Blocks a `git commit` whose author-like fields name someone other than the
# PRINCIPAL, per the authorship-attribution discipline (global CLAUDE.md
# "Authorship attribution"; operating-disciplines.md). This gate is a
# DETERMINISTIC BACKSTOP for that prose discipline — not its replacement. The
# discipline remains the primary defense; this gate catches the regression the
# prose alone has let through twice.
#
# REGISTRATION (settings-hooks.json template): PreToolUse, narrowed to git
# commits via the doc-blessed `if: "Bash(git commit*)"` permission-rule matcher
# (ARGUS r7; live-verified 2026-05-23). The `if` field decides WHICH commands
# invoke this script; the script still inspects tool_input.command to build the
# precise, self-contained deny message (the authoring rule needs the actual
# file/field/value names). The in-script `git commit` re-check below is the
# defense-in-depth for any deploy that registers the script without the `if`.
#
# FAIL-OPEN (design §4 / ARGUS R5): on any script error (no python3, malformed
# event, no git, unreadable allow-list) this allows the commit. A buggy gate
# degrades to today's no-enforcement baseline, never bricks the running team.
#
# PRINCIPAL allow-list: `.claude/hooks/principal-identity` (one name or email
# per line; '#' comments + blank lines ignored), written at install time from
# the install's PRINCIPAL identity. A value not on the list is treated as
# "not the PRINCIPAL" -> deny, with a message stating how to widen the list.
# NOTE: this allow-list is the GATE'S CONFIG (data the gate reads to decide),
# NOT an author-like field of any repo artifact — it is exempt from the
# author-field audit it performs (it names the PRINCIPAL precisely because it
# IS the PRINCIPAL identity reference).

set -uo pipefail

# Resolve this script's own directory so we can source the sibling lib by the
# DEPLOYED absolute path (works regardless of cwd at hook-fire time).
HOOK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd 2>/dev/null)" || exit 0
# shellcheck source=/dev/null
. "${HOOK_DIR}/_hooklib.sh" 2>/dev/null || exit 0

read_stdin_event

CMD="$(event_field tool_input.command)" || allow
[ -n "$CMD" ] || allow

# Only act on a `git commit`. (Defense-in-depth with the `if` matcher.) Match
# a git invocation that contains the `commit` subcommand; covers `git commit`,
# `git commit -m ...`, `git -c x=y commit`. Does NOT gate `git push` (author
# correctness is a commit-time property).
case "$CMD" in
  *git*commit*) : ;;
  *) allow ;;
esac

# cwd of the tool call (where the commit runs). Fall back to PWD if absent.
CWD="$(event_field cwd)" || CWD=""
[ -n "$CWD" ] || CWD="$(pwd)"

# Allow-list of accepted PRINCIPAL identity tokens (names + emails), lower-cased.
# The list is deployed as a SIBLING of this script (install.sh writes it to the
# same .claude/hooks/ dir), so HOOK_DIR is the primary, most-reliable lookup —
# it resolves regardless of the commit's cwd. Fall back to the cwd's tier and
# the user tier for non-standard layouts. Missing list => FAIL-OPEN (we cannot
# adjudicate without the PRINCIPAL identity; do not block).
ALLOWLIST=""
for cand in "${HOOK_DIR}/principal-identity" "${CWD}/.claude/hooks/principal-identity" "${HOME}/.claude/hooks/principal-identity"; do
  if [ -f "$cand" ]; then ALLOWLIST="$cand"; break; fi
done
[ -n "$ALLOWLIST" ] || allow   # no identity reference deployed -> fail-open

# Read accepted tokens (lower-cased, trimmed; skip comments + blanks).
ACCEPTED="$(sed -e 's/#.*$//' -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//' "$ALLOWLIST" 2>/dev/null \
  | tr '[:upper:]' '[:lower:]' | grep -v '^$')" || allow

# is_principal <value> : 0 if the lower-cased value matches an accepted token.
is_principal() {
  local v
  v="$(printf '%s' "$1" | tr '[:upper:]' '[:lower:]' | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')"
  [ -n "$v" ] || return 0   # empty value is not a wrong-name claim
  local tok
  while IFS= read -r tok; do
    [ -n "$tok" ] || continue
    [ "$v" = "$tok" ] && return 0
  done <<EOF
$ACCEPTED
EOF
  return 1
}

# --- Sub-check 1: commit author identity (git config in the cwd) ------------
# The commit Author: must stay the PRINCIPAL's configured identity (global rule:
# never override Author:; the seat-identity signal is a Co-Authored-By trailer
# layered ON TOP, never a replacement). If the configured author name/email is
# not the PRINCIPAL, DENY.
AUTHOR_NAME="$(git -C "$CWD" config user.name 2>/dev/null)" || AUTHOR_NAME=""
AUTHOR_EMAIL="$(git -C "$CWD" config user.email 2>/dev/null)" || AUTHOR_EMAIL=""

if [ -n "$AUTHOR_NAME" ] && ! is_principal "$AUTHOR_NAME"; then
  emit_deny "Commit blocked: git author name is set to \"${AUTHOR_NAME}\", which is not the PRINCIPAL. Per the authorship-attribution discipline the commit Author: must stay the PRINCIPAL's configured identity (a Co-Authored-By: trailer is the only seat-identity layer, never a replacement for Author:). Fix with: git config user.name \"<PRINCIPAL name>\". If \"${AUTHOR_NAME}\" IS a valid PRINCIPAL identity this gate does not yet know about, add it (one per line) to the allow-list at: ${ALLOWLIST}"
fi
if [ -n "$AUTHOR_EMAIL" ] && ! is_principal "$AUTHOR_EMAIL"; then
  emit_deny "Commit blocked: git author email is set to \"${AUTHOR_EMAIL}\", which is not the PRINCIPAL. The commit Author: must stay the PRINCIPAL's configured identity. Fix with: git config user.email \"<PRINCIPAL email>\". If \"${AUTHOR_EMAIL}\" IS a valid PRINCIPAL identity, add it to the allow-list at: ${ALLOWLIST}"
fi

# --- Sub-check 2: staged author-like fields in author-encoding files --------
# For staged files whose path matches the author-encoding set, scan the STAGED
# blob (not the worktree) for an author-like field assigned a person-name that
# is not the PRINCIPAL.
STAGED="$(git -C "$CWD" diff --cached --name-only 2>/dev/null)" || STAGED=""
[ -n "$STAGED" ] || allow   # nothing staged -> nothing to audit -> allow

# Author-encoding file matcher. Path basename / suffix tests.
is_author_encoding_file() {
  local p="$1" base
  base="$(basename "$p")"
  case "$base" in
    plugin.json|marketplace.json|package.json|pyproject.toml|setup.py|Cargo.toml|Gemfile|composer.json|NOTICE|CITATION.cff|metadata.json|manifest.json) return 0 ;;
    LICENSE|LICENSE.*|LICENSE.md) return 0 ;;
  esac
  case "$p" in
    *.claude-plugin/*) return 0 ;;
    *.md) return 0 ;;   # YAML frontmatter author: lines live in *.md
  esac
  return 1
}

while IFS= read -r f; do
  [ -n "$f" ] || continue
  is_author_encoding_file "$f" || continue
  # Read the STAGED version of the file (the blob being committed), not the
  # worktree — the audit is on what is ACTUALLY being committed.
  blob="$(git -C "$CWD" show ":${f}" 2>/dev/null)" || continue
  [ -n "$blob" ] || continue
  # Field-anchored extraction (handles JSON / YAML / TOML; emits field<TAB>value
  # per author-like assignment). See _hooklib.sh extract_author_fields.
  pairs="$(printf '%s' "$blob" | extract_author_fields)" || continue
  [ -n "$pairs" ] || continue
  while IFS="$(printf '\t')" read -r field val; do
    [ -n "$val" ] || continue
    if ! is_principal "$val"; then
      emit_deny "Commit blocked: author-like field \"${field}\" in staged file \"${f}\" names \"${val}\", which is not the PRINCIPAL. Per the authorship-attribution discipline, any author/owner/creator/maintainer/copyright field in a committed artifact must name the PRINCIPAL (a Co-Authored-By trailer is the only seat-identity layer, never a replacement). Fix the field to the PRINCIPAL, re-stage, and re-commit. If \"${val}\" is a legitimately-CITED SOURCE author (not an authorship claim on this artifact), move it out of the author field into prose or a citation. If \"${val}\" IS a valid PRINCIPAL identity this gate does not know, add it to the allow-list at: ${ALLOWLIST}"
    fi
  done <<EOF
$pairs
EOF
done <<EOF
$STAGED
EOF

# No wrong-name found -> allow the commit.
allow
