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
# mechanical deploy: drops the two MAJOR role files, deploys the 12 CAPTAIN
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
#   ./install.sh --target user [--modify-claude-md] [--no-captains] [--no-templates] [--prune-obsolete] [--enable-hooks] [--enable-env-block] [--bootstrap-bw] [--dry-run]
#   ./install.sh --target project --project-dir <path> [--modify-claude-md] [--no-captains] [--no-templates] [--prune-obsolete] [--enable-hooks] [--enable-env-block] [--bootstrap-bw] [--dry-run]
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
# CAPTAIN envelopes: by default the script deploys the 12 CAPTAIN_*.md sub-agent
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
# POLYBIUS invokes via the Skill tool — handoff-author, team-launcher, etc.
# Skills are deployed unsuffixed at every tier (including
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
# Hooks (Arc 46 / stoa--xyb.5): the script deploys substrate/hooks/*.sh (the
# deterministic enforcement tier — PreToolUse / Stop shell-command hooks +
# _hooklib.sh + README.md) to <target>/.claude/hooks/, GLOB-discovered (mirrors
# modules), unsuffixed, chmod +x. Deploying the SCRIPTS is INERT: Claude Code
# only fires hooks REGISTERED in a .claude/settings.json, which this script
# NEVER auto-writes. Arming is a SEPARATE, operator-gated, DEFAULT-OFF step
# (--enable-hooks): at project tier it merges the candidate settings-hooks.json
# block into the TARGET's settings.json (never the running session); at user
# tier it does NOT auto-write ~/.claude/settings.json (which IS the running
# config) but prints a manual-merge runbook. When --enable-hooks is OFF (the
# default), the scripts + candidate template deploy and NOTHING is armed. This
# is the HARD SAFETY CONSTRAINT: no install auto-arms a hook in a live session.
# Subproject-tier hook deploy is deferred (Arc 46 §11). The attribution-advisory
# skill's SECONDARY check reads a PRINCIPAL-identity allow-list seeded at
# .claude/hooks/principal-identity.
#
# Arc C (stoa--xyb.14) adds TWO more candidate mechanisms, BOTH default-OFF,
# BOTH mirroring the inert-candidate + separate-arming posture above:
#   (1) op-disc §13 — a settings 'env' block (settings-env-block.json carrying
#       PYTHONUTF8/PYTHONIOENCODING for the Windows UTF-8 fix). The candidate JSON
#       always deploys (inert); --enable-env-block (step 5e) merges it into the
#       TARGET's settings.json (project tier) or prints a manual-merge runbook
#       (user tier — never auto-writes the running config). DEFAULT OFF.
#   (2) op-disc §28 — a prepare-commit-msg git hook (substrate/githooks/). It
#       deploys as an INERT candidate to <dest>/.claude/githooks-candidate/ (step
#       5f) and is NEVER auto-armed into any .git/hooks/. Unlike --enable-hooks,
#       the git hook has NO install.sh arming flag at all (arming a git hook means
#       writing into a .git/hooks/ dir, which install.sh must never do — it would
#       arm git-commit behavior in whatever repo install runs against). The
#       candidate README's manual two-method runbook is the ONLY arming path.
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
# all 12 CAPTAINs are deployed with the same suffix. Subproject mode does NOT
# modify any CLAUDE.md (parent's stays as-is; sub-project does not get its own),
# does NOT redeploy templates (sub-project reads parent's at <parent>/.claude/
# templates/), and does NOT run bw init (sub-project shares parent's bw repo).
# --modify-claude-md and --templates-related flags are rejected in this mode.
#
# Transient-path .gitignore (Arc 55 / stoa--2i5): after deploying, the script
# writes a canonical <target>/.claude/.gitignore so a consumer's `git status`
# is not polluted by the transient runtime state the substrate generates inside
# .claude/. Ignored paths (relative to .claude/): scheduled_tasks.lock (cron
# lock), worktrees/ (per-arc-build worktree residue), .substrate-last-check
# (check-substrate-updates state), and __pycache__/ + *.pyc (skill bytecode
# regenerated at consumer runtime). The file is full-overwrite idempotent
# (rewritten verbatim on every run) and honors --dry-run. The deploy artifact
# .substrate-manifest is NOT ignored — it is read by check.sh/apply.sh and is
# meant to be visible.
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
ENABLE_HOOKS=0          # Arc 46: arm enforcement hooks. DEFAULT OFF (HARD SAFETY CONSTRAINT). When 0, hook scripts + the candidate settings-hooks.json deploy but NO hook is registered in any settings.json.
ENABLE_ENV_BLOCK=0      # Arc C (stoa--xyb.14 / op-disc §13): merge the candidate settings-env-block.json (PYTHONUTF8/PYTHONIOENCODING) into the TARGET's settings.json. DEFAULT OFF (same posture as --enable-hooks). When 0, the candidate env-block JSON deploys but NO env var is ever written into a running config.
BOOTSTRAP_BW=0          # Arc 75 (stoa--elx): opt-in bw bootstrap pre-flight (substrate/bootstrap-bw.sh). DEFAULT OFF → install.sh --dry-run output is byte-unchanged when the flag is absent.

# Source files live next to this script.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC_POLYBIUS="${SCRIPT_DIR}/MAJOR_POLYBIUS.md"
SRC_PLINY="${SCRIPT_DIR}/MAJOR_PLINY.md"
SRC_CHIRON="${SCRIPT_DIR}/MAJOR_CHIRON.md"
SRC_HAMILTON="${SCRIPT_DIR}/MAJOR_HAMILTON.md"
SRC_OPERATING_DISCIPLINES="${SCRIPT_DIR}/operating-disciplines.md"
SRC_TEMPLATES_DIR="${SCRIPT_DIR}/templates"
SRC_SKILLS_DIR="${SCRIPT_DIR}/skills"
SRC_MODULES_DIR="${SCRIPT_DIR}/modules"
SRC_HOOKS_DIR="${SCRIPT_DIR}/hooks"

# Enforcement-hook library (Arc 46 / stoa--xyb.5; debloat Arc 3 — Stage 1). The
# deterministic tier of the enforcement layer: harness-owned PreToolUse / Stop
# shell-command hooks that enforce load-bearing footguns (authorship field,
# clean-tree-before-branch, no-`-m`-in-bw-comment) even after the model's context
# compacts. Deployed unsuffixed (shared tooling, like modules/templates).
# GLOB-DISCOVERED from substrate/hooks/*.sh (mirrors the modules glob class,
# stoa--xyb.4) so authoring a new hook needs NO install.sh edit. No HOOK_NAMES
# array (glob, not manifest).
#
# CRITICAL SAFETY (design-rev1 §8 / HARD SAFETY CONSTRAINT): deploying the hook
# SCRIPTS is INERT — Claude Code only fires hooks that are REGISTERED in a
# .claude/settings.json. This install NEVER auto-writes a live settings.json.
# Arming the hooks is a separate, operator-gated, DEFAULT-OFF step (--enable-hooks).
# When the flag is OFF (the default), the scripts + the candidate
# settings-hooks.json template deploy but NOTHING is registered. See the
# --enable-hooks handling far below + substrate/hooks/README.md §5.

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
  settings-hooks.json
  settings-env-block.json
)

# The 12 CAPTAIN envelope source files. Order is the gauntlet pipeline order
# (DAEDALUS through CATO) followed by the support seats; ordering only affects
# log output, not correctness.
CAPTAIN_NAMES=(
  DAEDALUS
  ARGUS
  ADA
  VERA
  CATO
  NOMOS
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
  credential-discipline
  handoff-author
  workflow-composer
  interactive-html-preview
  decision-surface
  team-launcher
  gauntlet-setup
  whoami
  attribution-advisory
)
# Arc 63 / stoa--p41.2: check-substrate-updates + check-bw-release were REMOVED
# from SKILL_NAMES (retired from the model-invokable skill menu — their SKILL.md
# files were deleted so gen-data no longer renders them as LIEUTENANTs). They are
# NOT dropped: their scripts (check.sh / apply.sh / revert.sh) stay on disk and
# deploy to consumer .claude/skills/check-*/ via the Option-C carve-out below
# (deploy block + prune-scan exemption). Their drift detection now fires via the
# SessionStart(startup|resume) substrate-check hook. gauntlet-setup was PORTED in
# this same pass (net -2 +1 = 9 entries).
# Arc 64 / stoa--p41.2 (pass B): save-verdict + validate-spec + inspect-script-output
# were REMOVED from SKILL_NAMES (9 -> 6). save-verdict was a Python skill, now fully
# git rm'd and rewritten as the Bash-only module .claude/modules/save-verdict.md (no
# retained script — absent from the carve-out + prune-exemption below). validate-spec
# + inspect-script-output keep their callable scripts (check.sh / _check_runner.py /
# _lib) as retained OPERATOR TOOLS: their SKILL.md was removed so gen-data no longer
# renders them as LIEUTENANTs, and they are added BY NAME to the Option-C carve-out
# (deploy block + prune-scan exemption below), same mechanism as the Arc-63 check-*
# dirs. credential-discipline STAYS (out of scope / deferred). Resulting 6 entries.

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
  sed -n '/^# install\.sh — /,/^# Dry-run:.*$/p' "$0" | sed 's/^# \{0,1\}//'
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

  # FAIL-LOUD PRE-CHECK (stoa--3nh / Arc 69 c1). Count the MAJOR_*.md glob BEFORE
  # the `{ ... } > "$manifest"` redirect opens, and err() (exit 2) if zero — so the
  # manifest path is NEVER opened/truncated/written on the zero-MAJOR abort path.
  # A post-brace assert (the earlier shape) could not satisfy this: the brace-group
  # redirect commits the (header-only) file to disk the instant it opens, BEFORE any
  # post-brace guard can fire — leaving a partial manifest as the live artifact. The
  # pre-redirect check is the only placement that genuinely leaves no partial file.
  local srcmaj maj_precount=0
  shopt -s nullglob
  for srcmaj in "${SCRIPT_DIR}/MAJOR_"*.md; do
    maj_precount=$((maj_precount + 1))
  done
  shopt -u nullglob
  [ "$maj_precount" -ge 1 ] || err "write_substrate_manifest: zero MAJOR_*.md globbed from ${SCRIPT_DIR} — substrate checkout incomplete; refusing to write a manifest missing every MAJOR mapping."

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
    # MAJOR files: glob substrate/MAJOR_*.md so any future MAJOR auto-discovers
    # in the manifest. NAME_SUFFIX substitution for all; subproject tier suffixes
    # the deployed filename, project + user do not (mirror install.sh SUFFIX_MAJORS
    # + check.sh enumerate_deployed). USER_TIER_DIR is a POLYBIUS-only placeholder
    # (only MAJOR_POLYBIUS.md carries {{USER_TIER_DIR}}), emitted at user-tier only.
    # (zero-MAJOR is already guarded by the pre-redirect maj_precount check above,
    #  so this loop is only reached when at least one MAJOR_*.md exists.)
    local majname dep_name
    shopt -s nullglob
    for srcmaj in "${SCRIPT_DIR}/MAJOR_"*.md; do
      majname="$(basename "$srcmaj" .md)"        # "MAJOR_POLYBIUS"
      if [ "$tier" = "subproject" ]; then
        dep_name=".claude/${majname}${name_suffix}.md"
      else
        dep_name=".claude/${majname}.md"
      fi
      printf "%s\t{{NAME_SUFFIX}}\t%s\n" "$dep_name" "${name_suffix}"
      if [ "$tier" = "user" ] && [ -n "$USER_TIER_DIR" ] && [ "$majname" = "MAJOR_POLYBIUS" ]; then
        printf "%s\t{{USER_TIER_DIR}}\t%s\n" "$dep_name" "$USER_TIER_DIR"
      fi
    done
    shopt -u nullglob
    # CAPTAINs (always NAME_SUFFIX — empty at user-tier; _<slug> at project/subproject).
    if [ "$WITH_CAPTAINS" -eq 1 ]; then
      for name in "${CAPTAIN_NAMES[@]}"; do
        printf ".claude/agents/CAPTAIN_%s%s.md\t{{NAME_SUFFIX}}\t%s\n" "$name" "${name_suffix}" "${name_suffix}"
      done
    fi
  } > "$manifest"
  # FAIL-LOUD (stoa--3nh / Arc 69 c1). The zero-MAJOR guard fires in the PRE-CHECK
  # above, BEFORE this brace-group redirect opens — so on a zero-MAJOR abort the
  # manifest path is never written and no partial artifact is ever left on disk.
  # (The earlier shape asserted AFTER the brace group, which could not work: the
  # redirect commits the header-only file the instant it opens, before any
  # post-brace guard can run. The pre-redirect check is the corrected mechanism.)
  # DIRECT-CALL SITE: write_substrate_manifest is called directly (not via
  # process-sub), so err()'s `exit 2` propagates and aborts install.sh — contrast
  # check.sh's enumerate_deployed, consumed via process-sub, which needs a sentinel.
  echo "wrote manifest: $manifest"
}

# write_substrate_gitignore <dest-dir>
#
# Writes <dest-dir>/.gitignore covering substrate-generated transient runtime
# paths so a consumer's `git status` is not polluted by cache/lock/worktree
# noise (Arc 55 / stoa--2i5). The file lives INSIDE .claude/, so entries are
# relative to .claude/ (e.g. `worktrees/`, NOT `.claude/worktrees/`) — a
# .gitignore ignores paths relative to its own directory, and getting that
# prefix wrong silently matches nothing.
#
# Idempotent by full-overwrite: the body is a fixed quoted heredoc, so
# re-running install.sh reproduces it verbatim — no duplicate lines possible
# (the same idempotency mechanism write_substrate_manifest uses above). The
# quoted delimiter (<<'EOF') is required so `*.pyc`, `$`, and `#` write
# literally under `set -euo pipefail` with no expansion. Honors --dry-run
# (prints intent, writes nothing).
write_substrate_gitignore() {
  local dest="$1"
  local gi="${dest}/.gitignore"

  if [ "$DRY_RUN" -eq 1 ]; then
    echo "[dry-run] write: $gi (substrate-transient paths: scheduled_tasks.lock, worktrees/, .substrate-last-check, .substrate-check-hook-stamp, .substrate-drift-signal, __pycache__/, *.pyc)"
    return 0
  fi

  cat > "$gi" <<'EOF'
# Stoa substrate — transient runtime state (auto-generated, do not commit).
# Written by install.sh (Arc 55 / stoa--2i5). Paths are relative to this
# .claude/ directory. Re-running install.sh regenerates this file verbatim.
# DO NOT EDIT MANUALLY — install.sh overwrites it on every run.

# Cron state — durable scheduled-task lock (CronCreate durable:true).
scheduled_tasks.lock

# Per-arc-build worktrees; transient/empty residue post-merge (Windows
# file-lock leaves orphan dirs — stoa--7ap).
worktrees/

# check-substrate-updates state file.
.substrate-last-check

# SessionStart substrate-check hook transients (Arc 63 / stoa--p41.2):
# the per-session-start throttle stamp and the P-FALLBACK drift signal the
# Stop self-check + CLAUDE.md read.
.substrate-check-hook-stamp
.substrate-drift-signal

# Skill bytecode — stripped at deploy, but regenerated when a consumer runs
# a skill (Arc 40 / stoa--t9u strips the deploy-time copy; this catches the
# consumer-runtime regeneration).
__pycache__/
*.pyc
EOF
  echo "wrote gitignore: $gi"
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
    --principal-name)
      # stoa--iyl: the PRINCIPAL's display NAME as it appears in author-like
      # fields (e.g. "Denson Smith", "Marianne <Lastname>") — distinct from the
      # git handle in `git config user.name` (which may be a short handle like
      # "denson"). Seeded into the attribution-advisory allow-list so the
      # advisory's SECONDARY check recognizes the PRINCIPAL's own authored
      # artifacts and does not false-report.
      [ "$#" -ge 2 ] || err "--principal-name requires a name"
      PRINCIPAL_NAME="$2"
      shift 2
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
    --enable-hooks)
      # Arc 46 (stoa--xyb.5): ARM the enforcement hooks by merging the candidate
      # settings-hooks.json block into the TARGET's settings.json. DEFAULT OFF.
      # This is the ONLY path that registers a hook. Even when set, it targets
      # the INSTALL TARGET, never the running build session. At USER tier (where
      # the target ~/.claude/settings.json IS the running config) it does NOT
      # auto-write — it prints the merge as a manual instruction (ARGUS r4 /
      # HARD SAFETY CONSTRAINT). See the enable-hooks handling below.
      ENABLE_HOOKS=1
      shift
      ;;
    --enable-env-block)
      # Arc C (stoa--xyb.14 / op-disc §13): ARM the Windows PYTHONUTF8 fix by
      # merging the candidate settings-env-block.json 'env' block into the
      # TARGET's settings.json. DEFAULT OFF — same safety posture as
      # --enable-hooks. The candidate env-block JSON always deploys (inert: a
      # candidate file sets no env var until merged into a live settings.json).
      # When this flag is set it targets the INSTALL TARGET's settings.json,
      # never the running build session's. At USER tier (where
      # ~/.claude/settings.json IS the running config) it does NOT auto-write —
      # it prints the merge as a manual instruction (ARGUS r4 / HARD SAFETY
      # CONSTRAINT). See the --enable-env-block handling below (step 5e).
      ENABLE_ENV_BLOCK=1
      shift
      ;;
    --bootstrap-bw)
      BOOTSTRAP_BW=1
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

# ----- Arc 75 (stoa--elx): optional bw bootstrap pre-flight (after --target validation,
#        before the case dispatch — target-independent: runs for user|project|subproject) -----
if [ "$BOOTSTRAP_BW" -eq 1 ]; then
  _bootstrap="${SCRIPT_DIR}/bootstrap-bw.sh"
  [ -f "$_bootstrap" ] || err "--bootstrap-bw: helper not found at $_bootstrap"
  if [ "$DRY_RUN" -eq 1 ]; then bash "$_bootstrap" --dry-run; else bash "$_bootstrap" --yes; fi
fi

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
    DEST_HOOKS_DIR="${HOME}/.claude/hooks"
    DEST_SETTINGS_JSON="${HOME}/.claude/settings.json"   # user-tier: this IS the running config (ARGUS r4) — never auto-written
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
    DEST_HOOKS_DIR="${PROJECT_DIR}/.claude/hooks"
    DEST_SETTINGS_JSON="${PROJECT_DIR}/.claude/settings.json"   # project-tier target settings.json (only written with --enable-hooks)
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
    # Hooks: subproject-tier deploy is deferred, mirroring modules (Arc 46 /
    # stoa--xyb.5 §11 out-of-scope). Subproject .claude/settings.json resolution
    # for a dispatched sub-agent is the same contested-path question that deferred
    # subproject modules; empty here so the deploy step's [ -n "$DEST_HOOKS_DIR" ]
    # guard skips subproject cleanly, mirroring DEST_MODULES_DIR above.
    DEST_HOOKS_DIR=""    # not used in subproject mode (Arc 46 §11)
    DEST_SETTINGS_JSON="" # not used in subproject mode
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
[ -f "$SRC_CHIRON" ]                || err "source file not found: $SRC_CHIRON"
[ -f "$SRC_HAMILTON" ]              || err "source file not found: $SRC_HAMILTON"
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
# NON-RECURSIVE glob (`*.md`, not `**/*.md`): the FIRST subdir under substrate/modules/ is
# `tests/` (the dilemma-classifier seed corpus, Arc 70 / stoa--y1a — new layout precedent).
# That subdir is DEPLOY-SAFE precisely because this glob is non-recursive: `modules/tests/...`
# is never matched, so the test corpus is source-only and never lands at a target. (Same
# source-only pattern as substrate/hooks/tests/.)
_src_modules=( "${SRC_MODULES_DIR}"/*.md )
shopt -u nullglob
[ "${#_src_modules[@]}" -gt 0 ] || err "no module sources found: ${SRC_MODULES_DIR}/*.md"

# Hooks are always deployed at user + project tiers (no opt-out, mirrors
# modules; subproject-tier deferred). Source-dir must exist; glob-discover the
# hook sources (substrate/hooks/*.sh) and assert at least one exists so an empty
# or mis-pathed source dir fails loudly (the glob escape-hatch from the modules
# class, stoa--xyb.4). _src_hooks is reused by the plan line + deploy step. NOTE:
# deploying the SCRIPTS is inert — registration (arming) is a separate
# default-OFF step (--enable-hooks); see the HARD SAFETY CONSTRAINT note above.
[ -d "$SRC_HOOKS_DIR" ] || err "source hooks directory not found: $SRC_HOOKS_DIR"
shopt -s nullglob
_src_hooks=( "${SRC_HOOKS_DIR}"/*.sh )
shopt -u nullglob
[ "${#_src_hooks[@]}" -gt 0 ] || err "no hook sources found: ${SRC_HOOKS_DIR}/*.sh"

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
  # Glob-derive the MAJOR roster (POLYBIUS/PLINY/CHIRON/HAMILTON + any future
  # MAJOR) so this display string stays consistent with the fresh-DEPLOY
  # enumeration; the previous hardcoded 2-MAJOR list (POLYBIUS/PLINY) omitted
  # CHIRON/HAMILTON. Display-only; zero behavior change (stoa--kr7).
  _maj_list=""
  shopt -s nullglob
  for _mf in "${SCRIPT_DIR}/MAJOR_"*.md; do
    _mb="$(basename "$_mf" .md)"
    _maj_list="${_maj_list:+$_maj_list, }${_mb}${NAME_SUFFIX}.md"
  done
  shopt -u nullglob
  echo "  MAJOR files      : suffixed (${_maj_list})"
fi
echo "  deploy CAPTAINs  : $([ "$WITH_CAPTAINS" -eq 1 ] && echo "yes (12 envelopes to ${DEST_AGENTS_DIR})" || echo "no (--no-captains)")"
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
if [ -n "$DEST_HOOKS_DIR" ]; then
  # Count from the source glob (observable, mirrors the modules plan-line).
  echo "  deploy hooks     : yes (${#_src_hooks[@]} script(s) to ${DEST_HOOKS_DIR}) [INERT — not armed]"
else
  echo "  deploy hooks     : no (subproject mode — Arc 46 §11 out-of-scope)"
fi
if [ "$ENABLE_HOOKS" -eq 1 ]; then
  if [ "$TARGET" = "user" ]; then
    # User-tier is PRINT-ONLY: it emits a manual-merge runbook and NEVER auto-writes
    # ~/.claude/settings.json (which IS the running config — ARGUS r4 safety discipline).
    echo "  arm hooks        : YES (--enable-hooks) -> print manual-merge runbook for ${DEST_SETTINGS_JSON} (user-tier never auto-writes the running config)"
  else
    echo "  arm hooks        : YES (--enable-hooks) -> merge candidate block into ${DEST_SETTINGS_JSON} (target settings.json, never the running session)"
  fi
else
  echo "  arm hooks        : no (default OFF — scripts deploy inert; no settings.json written)"
fi
if [ "$ENABLE_ENV_BLOCK" -eq 1 ]; then
  if [ "$TARGET" = "user" ]; then
    echo "  arm env block    : YES (--enable-env-block) -> print manual-merge runbook for ${DEST_SETTINGS_JSON} (user-tier never auto-writes the running config)"
  else
    echo "  arm env block    : YES (--enable-env-block) -> merge candidate 'env' block into ${DEST_SETTINGS_JSON} (target settings.json, never the running session)"
  fi
else
  echo "  arm env block    : no (default OFF — candidate settings-env-block.json deploys inert; no settings.json written)"
fi
echo "  git hook (§28)   : candidate-only -> ${DEST_DIR}/githooks-candidate/prepare-commit-msg (INERT; never auto-armed into .git/hooks/ — manual arming per its README)"
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
  DEST_CHIRON="${DEST_DIR}/MAJOR_CHIRON${NAME_SUFFIX}.md"
  DEST_HAMILTON="${DEST_DIR}/MAJOR_HAMILTON${NAME_SUFFIX}.md"
else
  DEST_POLYBIUS="${DEST_DIR}/MAJOR_POLYBIUS.md"
  DEST_PLINY="${DEST_DIR}/MAJOR_PLINY.md"
  DEST_CHIRON="${DEST_DIR}/MAJOR_CHIRON.md"
  DEST_HAMILTON="${DEST_DIR}/MAJOR_HAMILTON.md"
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
  echo "[dry-run] deploy: $SRC_CHIRON -> $DEST_CHIRON (substitute {{NAME_SUFFIX}} -> '${NAME_SUFFIX}')"
  echo "[dry-run] deploy: $SRC_HAMILTON -> $DEST_HAMILTON (substitute {{NAME_SUFFIX}} -> '${NAME_SUFFIX}')"
else
  if [ -n "$USER_TIER_DIR" ]; then
    sed -e "s/{{NAME_SUFFIX}}/${NAME_SUFFIX}/g" -e "s|{{USER_TIER_DIR}}|${USER_TIER_DIR}|g" "$SRC_POLYBIUS" > "$DEST_POLYBIUS"
  else
    sed "s/{{NAME_SUFFIX}}/${NAME_SUFFIX}/g" "$SRC_POLYBIUS" > "$DEST_POLYBIUS"
  fi
  sed "s/{{NAME_SUFFIX}}/${NAME_SUFFIX}/g" "$SRC_PLINY" > "$DEST_PLINY"
  sed "s/{{NAME_SUFFIX}}/${NAME_SUFFIX}/g" "$SRC_CHIRON" > "$DEST_CHIRON"
  sed "s/{{NAME_SUFFIX}}/${NAME_SUFFIX}/g" "$SRC_HAMILTON" > "$DEST_HAMILTON"
  echo "deployed: $DEST_POLYBIUS"
  echo "deployed: $DEST_PLINY"
  echo "deployed: $DEST_CHIRON"
  echo "deployed: $DEST_HAMILTON"
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
# not a role file. DEPLOYED BEFORE the 2a-recompose block (debloat Arc 47 /
# design-arc-47 §6.5) so $DEST_OPERATING_DISCIPLINES exists when recompose
# re-inlines op-disc's 12 owned module bodies at subproject tier.
DEST_OPERATING_DISCIPLINES="${DEST_DIR}/operating-disciplines.md"
if [ "$DRY_RUN" -eq 1 ]; then
  echo "[dry-run] deploy: $SRC_OPERATING_DISCIPLINES -> $DEST_OPERATING_DISCIPLINES"
else
  cp "$SRC_OPERATING_DISCIPLINES" "$DEST_OPERATING_DISCIPLINES"
  echo "deployed: $DEST_OPERATING_DISCIPLINES"
fi

# 2a-recompose. Subproject-tier MODULE-INLINE recompose (debloat Arc 2 / design-arc-45 §6.5).
# ---------------------------------------------------------------------------------------------
# At user/project tier the slim core deploys AS-IS + the modules dir deploys (CHANNEL 2 Read
# resolves). At SUBPROJECT tier the modules dir is NOT deployed (DEST_MODULES_DIR="") AND a
# dispatched CAPTAIN's `Read .claude/modules/<X>.md` does not resolve reliably (claude-code
# #56686/#31546/#29423). So at subproject tier we RECOMPOSE: re-inline each module body into
# the deployed file at its paired `<!-- MODULE-INLINE:<name> -->` ... `<!-- /MODULE-INLINE:<name> -->`
# sentinel, producing a self-contained file (matching the existing self-contained-subproject
# pattern). The marker is machine-parseable (full-line HTML-comment), invisible at the tiers that
# do NOT recompose, and 1:1-auditable. FAIL-LOUD: any marker/module mismatch err()s (exit 2,
# aborts deploy) rather than shipping LOST CANON. Runs POST-sed/cp (markers are inert in the source;
# the sed substitutes only {{NAME_SUFFIX}}/{{USER_TIER_DIR}}, neither of which appears in a marker;
# op-disc is plain-cp'd so no substitution applies).
# THIS ARC recomposes FIVE files (debloat Arc 47 / design-arc-47 §6.4–§6.5 + debloat Arc 48 /
# design-arc-48 §6.4 + debloat Arc 6 / Arc 49 / design-arc-49 §6.4 + Arc 61): $DEST_POLYBIUS (Arc 2,
# now 4 owned modules), $DEST_OPERATING_DISCIPLINES (Arc 47, 12 owned modules), $DEST_PLINY (Arc 48,
# 11 owned modules), $DEST_DAEDALUS (Arc 6/Arc 49, 7 owned modules — the FOURTH owner), AND
# $DEST_CHIRON (Arc 61, 1 owned module — the FIFTH owner). The shared substrate/modules/ dir forces
# the MODULE-OWNERSHIP partition (ARGUS r3): each call passes its OWNED-module set for Checks B/D
# while Check A tests the GLOBAL existence set inside the function. The five owned-sets are
# basename-DISJOINT (design-arc-49 §3.8 / P-OWNERSHIP-NOCOLLIDE) so no marker is ambiguously owned.
# NOTE (design-arc-49 §6.5): the recompose CALLS run in a separate
# if-subproject block AFTER the CAPTAIN deploy loop (the fourth owner, CAPTAIN_DAEDALUS, deploys in
# that loop and has no dedicated DEST_* var); the function DEFINITION below stays here.
# Generality note: design §6.4/§6.5.
if [ "$TARGET" = "subproject" ]; then
  recompose_module_inline() {
    # $1 = role file to recompose in place.
    # $2 = OWNED module basenames (space-separated) THIS file owns — for Checks B/D
    #      (only the markers/modules THIS file owns). DISTINCT from the GLOBAL existence set.
    # MODULE-OWNERSHIP partition (debloat Arc 47 / design-arc-47 §6.4, ARGUS r3; extended to a
    # THIRD owner in debloat Arc 48 / design-arc-48 §6.4; FOURTH owner in debloat Arc 6 / Arc 49 /
    # design-arc-49 §6.4; FIFTH owner CHIRON in Arc 61): the shared substrate/modules/ dir now holds
    # modules owned by DIFFERENT role files (4 POLYBIUS + 12 op-disc + 11 PLINY + 7 DAEDALUS +
    # 1 CHIRON, basename-disjoint per design-arc-49 §3.8 — but SUPERSEDED for the two-owner modules
    # `dilemma-classifier` (Arc 70 / stoa--y1a) and `decision-register` (Arc 71 / stoa--7gl), see the
    # owned-set comment in §3b). Two distinct sets are required:
    #   - GLOBAL existence set (Check A): every real module source, owner-agnostic. A marker
    #     must reference a real module file REGARDLESS of owner — the Check A guarantee must NOT
    #     narrow with the owned-set. Built from the filesystem glob, NOT from arg 2.
    #   - OWNED consumption set (Checks B/D): only THIS role file modules. Built from arg 2.
    # Without the partition, recompose_module_inline "$DEST_POLYBIUS" Check B would false-positive
    # on the 12 op-disc modules (no POLYBIUS marker) and abort the subproject deploy.
    _role_file="$1"
    _owned_basenames="$2"

    # GLOBAL existence set: every real module source (excludes README.md, the composition-layer
    # reference doc — never a MODULE-INLINE target; design §6.5). Owner-agnostic; backs Check A only.
    _global_basenames=""
    for _src in "${SRC_MODULES_DIR}"/*.md; do
      [ -e "$_src" ] || continue
      _bn="$(basename "$_src" .md)"
      [ "$_bn" = "README" ] && continue
      _global_basenames="${_global_basenames} ${_bn}"
    done

    # In dry-run the upstream sed/cp only PRINTED its plan (did not write the deployed file),
    # so do not require the role file to exist — print the recompose plan and return.
    if [ "$DRY_RUN" -eq 1 ]; then
      echo "[dry-run] recompose (subproject): $_role_file <- inline OWNED module bodies at MODULE-INLINE markers (owned:${_owned_basenames:- none})"
      return 0
    fi

    [ -f "$_role_file" ] || err "recompose: role file not found: $_role_file"

    # awk state-machine (deterministic, single pass over the role file).
    # FAIL-LOUD checks (exit 2 via the trailing err() on non-zero awk exit):
    #   A — marker references a module source absent from the GLOBAL existence set (owner-agnostic).
    #   B — an OWNED module source exists with no marker in THIS file (would DROP a body at subproject tier).
    #   C — unbalanced markers (open with no matching close, or close with no open).
    #   D — zero markers in THIS file but OWNED relocatable modules exist (per-file; ARGUS F-B).
    #   E — a module BODY contains a literal MODULE-INLINE marker line (close-marker-in-body corruption; ARGUS F-A).
    _tmp="${_role_file}.recompose.tmp"
    awk -v modules_dir="${SRC_MODULES_DIR}" \
        -v global_list="${_global_basenames}" \
        -v owned_list="${_owned_basenames}" '
      # exit triggers the END block in POSIX awk; _aborting suppresses the END checks
      # so a failure prints exactly one diagnostic, not two.
      function fail(msg) { _aborting = 1; print "install.sh: error: recompose: " msg > "/dev/stderr"; exit 2 }
      BEGIN {
        # GLOBAL existence set (Check A): every real module source, owner-agnostic.
        ng = split(global_list, _g, " ")
        for (i = 1; i <= ng; i++) { if (_g[i] != "") global_exists[_g[i]] = 1 }
        # OWNED consumption set (Checks B/D): only the modules THIS role file owns.
        no = split(owned_list, _o, " ")
        for (i = 1; i <= no; i++) { if (_o[i] != "") { owned[_o[i]] = 1; consumed[_o[i]] = 0; nowned++ } }
        in_marker = 0; markers_seen = 0; _aborting = 0
      }
      # OPEN marker: full-line ^<!-- MODULE-INLINE:<name> -->$
      /^<!-- MODULE-INLINE:[^ ]+ -->$/ {
        if (in_marker) fail("nested open marker MODULE-INLINE:" cur " before close of MODULE-INLINE:" open_name " (unbalanced)")  # Check C
        name = $0; sub(/^<!-- MODULE-INLINE:/, "", name); sub(/ -->$/, "", name)
        if (!(name in global_exists)) fail("marker MODULE-INLINE:" name " has no module source at " modules_dir "/" name ".md")    # Check A (GLOBAL existence)
        # Emit the OPEN marker (kept — provenance + idempotent re-recompose anchor).
        print $0
        # Inline the ENTIRE module body, guarding against a body that itself contains a marker line.
        body_path = modules_dir "/" name ".md"
        while ((getline line < body_path) > 0) {
          if (line ~ /^<!-- \/?MODULE-INLINE:/) { close(body_path); fail("module " name ".md body contains a literal MODULE-INLINE marker line — would corrupt recompose; remove it from the module source") }  # Check E (ARGUS F-A)
          print line
        }
        close(body_path)
        if (name in owned) consumed[name] = 1   # consumed-tracking is OWNED-scoped (Check B iterates owned only)
        markers_seen++
        in_marker = 1; open_name = name
        next
      }
      # CLOSE marker: full-line ^<!-- /MODULE-INLINE:<name> -->$
      /^<!-- \/MODULE-INLINE:[^ ]+ -->$/ {
        cname = $0; sub(/^<!-- \/MODULE-INLINE:/, "", cname); sub(/ -->$/, "", cname)
        if (!in_marker) fail("close marker MODULE-INLINE:" cname " with no matching open (unbalanced)")                            # Check C
        if (cname != open_name) fail("close marker MODULE-INLINE:" cname " does not match open MODULE-INLINE:" open_name " (unbalanced)")  # Check C
        print $0  # emit the CLOSE marker (kept — idempotency anchor)
        in_marker = 0; open_name = ""
        next
      }
      # Inside a marker: SKIP the gap / previously-inlined body (idempotency — re-recompose replaces it).
      { if (in_marker) next; print }
      END {
        if (_aborting) exit 2  # a rule-level fail() already reported; do not re-run END checks
        if (in_marker) fail("open marker MODULE-INLINE:" open_name " never closed before EOF (unbalanced)")                         # Check C
        if (markers_seen == 0 && nowned > 0) fail("role file has zero MODULE-INLINE markers but " nowned " OWNED relocatable module(s) exist — bodies would be DROPPED at subproject tier")  # Check D (per-file, OWNED; ARGUS F-B)
        for (m in owned) { if (owned[m] && !consumed[m]) fail("OWNED module " m ".md exists but no MODULE-INLINE:" m " marker in the role file — body would be DROPPED at subproject tier") }  # Check B (OWNED)
      }
    ' "$_role_file" > "$_tmp" || {
      # FAIL-LOUD: recompose could not prove completeness. Remove BOTH the partial tmp AND the
      # slim $_role_file the upstream sed/cp wrote — install.sh NEVER leaves a partial/slim file
      # at subproject tier (design §6.5). The non-zero exit aborts the deploy entirely.
      rm -f "$_tmp" "$_role_file"
      exit 2
    }

    mv "$_tmp" "$_role_file"
    echo "recomposed (subproject): $_role_file (re-inlined OWNED module bodies at MODULE-INLINE markers)"
  }

  # NOTE (debloat Arc 6 / Arc 49 / design-arc-49 §6.5): the recompose CALLS moved to a new
  # if-subproject block AFTER the CAPTAIN deploy loop (below). The function DEFINITION stays here.
  # The fourth owner (CAPTAIN_DAEDALUS) deploys inside the CAPTAIN_NAMES loop and has no dedicated
  # DEST_* var, so its deployed file does not exist until the loop runs — the calls must follow it.
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

# 3b. Subproject module-recompose calls (debloat Arc 47 §6.4–§6.5 + Arc 48 §6.4 + Arc 6/Arc 49
# §6.4–§6.5). Placed AFTER the CAPTAIN deploy loop (above) because the FOURTH owner
# (CAPTAIN_DAEDALUS) deploys inside that loop with no dedicated DEST_* var — its suffixed file does
# not exist until the loop has run, so its recompose call must follow it (design-arc-49 §2.7.2-b /
# §6.5, option (i): the recompose FUNCTION definition stays in the §3a block above; only the CALLS
# moved here). The other three files (POLYBIUS / op-disc / PLINY) deploy earlier, so moving the
# calls later is harmless for them. recompose_module_inline() is defined above in the same
# TARGET=subproject gate, so it is always defined before these calls run.
if [ "$TARGET" = "subproject" ]; then
  # MODULE-OWNERSHIP owned-sets (design-arc-47 §6.4 / §3.8; FOURTH owner added Arc 6 / Arc 49). Each
  # role file's recompose call is scoped to the modules IT owns (Checks B/D); Check A still tests the
  # GLOBAL existence set (all 35 module sources minus README, owner-agnostic) inside the function.
  # TWO-OWNER MODULES (Arc 70 / stoa--y1a; Arc 71 / stoa--7gl): `dilemma-classifier` AND
  # `decision-register` are each INTENTIONALLY owned by BOTH POLYBIUS_MODULES and PLINY_MODULES — the
  # self-correction doctrine's multi-agent-redundancy property needs both the READ (classify) and the
  # WRITE (capture a decided dilemma) consulted at two seats (POLYBIUS spin-up/prioritization + PLINY
  # directive-lock), so each role file carries its own MODULE-INLINE:dilemma-classifier AND
  # MODULE-INLINE:decision-register marker pair. This SUPERSEDES the "basename-disjoint per
  # design-arc-49 §3.8" invariant noted at the recompose_module_inline() comment above (~L1101) FOR THESE
  # TWO MODULES: ownership is no longer disjoint across owners. Runtime-proven safe — recompose runs ONCE
  # PER FILE with that file's OWN owned-set (Checks B/D are per-file; Check A is owner-agnostic global
  # existence), so independent marker pairs in two files never collide. A future maintainer reading the
  # disjoint comment must read it as superseded for dilemma-classifier and decision-register.
  POLYBIUS_MODULES="onboarding sub-project-spawning pair-programming-prototyping substrate-update-check dilemma-classifier decision-register"
  OPDISC_MODULES="two-polybius-coordination autonomous-mode-setup sub-agent-transcript-discipline bw-fit-matrix oss-dep-and-latency credential-discipline-detail bw-upgrade mechanical-inspection-split multi-team-interop four-layer-identity substrate-component-design jsdom-timing-discipline"
  PLINY_MODULES="ada-brief-preamble sub-agent-watchdog per-worktree-venv post-strabo-vera incomplete-unverifiable-routing smoke-beat-deploy-check background-dispatch-hygiene pre-branch-hygiene arc-close-hygiene seat-identity-brief pliny-polling-pattern dilemma-classifier decision-register"
  DAEDALUS_MODULES="canonical-code-block-fix credential-flow-design principal-gate-design canonical-template-alignment probe-grounding ssot-with-why api-docs-dont-generalize"
  CHIRON_MODULES="pair-programmer-authoring"
  # CAPTAIN_DAEDALUS has NO dedicated DEST_* deploy var (it deploys in the CAPTAIN_NAMES loop above);
  # construct its deployed path here, mirroring the loop's dest= (CAPTAIN_${name}${NAME_SUFFIX}.md).
  DEST_DAEDALUS="${DEST_AGENTS_DIR}/CAPTAIN_DAEDALUS${NAME_SUFFIX}.md"
  recompose_module_inline "$DEST_POLYBIUS" "$POLYBIUS_MODULES"
  recompose_module_inline "$DEST_OPERATING_DISCIPLINES" "$OPDISC_MODULES"
  recompose_module_inline "$DEST_PLINY" "$PLINY_MODULES"
  # FIFTH owner (CHIRON, Arc 61) — UNGATED. CHIRON deploys unconditionally in the §2 MAJOR-deploy
  # block (always runs, like POLYBIUS/PLINY), so $DEST_CHIRON always exists at subproject tier when
  # this call runs. UNLIKE DAEDALUS (below), CHIRON is not a CAPTAIN and is not behind WITH_CAPTAINS,
  # so its call stays ungated next to the other three always-deploy owners.
  recompose_module_inline "$DEST_CHIRON" "$CHIRON_MODULES"
  # FOURTH owner gated on WITH_CAPTAINS: CAPTAIN_DAEDALUS deploys ONLY inside the
  # WITH_CAPTAINS-gated loop above, so under --no-captains its $DEST_DAEDALUS file
  # was never written. Recomposing it then would fire recompose_module_inline's
  # `[ -f "$_role_file" ] || err` (exit 2 + partial deploy) — a flag-interaction
  # regression (CATO c1 / ZENO d1). The other three owners (POLYBIUS/op-disc/PLINY)
  # deploy unconditionally, so their calls stay ungated. Match the CAPTAIN-loop idiom.
  if [ "$WITH_CAPTAINS" -eq 1 ]; then
    recompose_module_inline "$DEST_DAEDALUS" "$DAEDALUS_MODULES"
  fi
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

# 5a. Deploy operator-tool carve-out (Arc 63 / stoa--p41.2; design-rev2 §4.3
# Block 1; arc directive substrate/arcs/arc-63-build-directive.md). These two
# dirs are substrate-shipped OPERATOR TOOLS, not model-invokable skills: their
# SKILL.md was deleted in Arc 63 so gen-data does not render them as LIEUTENANTs
# and they were removed from SKILL_NAMES, but their drift-check + apply/revert
# scripts must still reach consumer workspaces so the SessionStart substrate-
# check hook (and on-demand apply/revert) can run them. They are NOT custom-*
# (those are operator-owned; these are substrate-shipped — design §4.2 rejects
# masquerading them as custom-). The carve-out deploys them by name, mirroring
# the SKILL_NAMES loop's copy+pycache-cleanup. Paired with the prune-scan
# exemption in step 7 (the obsolete scan would otherwise flag a dir not in
# SKILL_NAMES and delete it under --prune-obsolete in the same run).
# Arc 64 / stoa--p41.2 (pass B): validate-spec + inspect-script-output added by
# the same mechanism — their SKILL.md was removed (retired from the skill menu)
# but their check.sh / _check_runner.py / _lib stay callable operator tools, so
# they must reach consumer workspaces here and must be prune-exempt below.
# save-verdict is NOT here: it was fully git rm'd (Bash-only module, no script).
CARVEOUT_SKILL_DIRS=(check-substrate-updates check-bw-release validate-spec inspect-script-output)
for d in "${CARVEOUT_SKILL_DIRS[@]}"; do
  src_co="${SRC_SKILLS_DIR}/${d}"
  dest_co="${DEST_SKILLS_DIR}/${d}"
  [ -d "$src_co" ] || continue
  if [ "$DRY_RUN" -eq 1 ]; then
    echo "[dry-run] deploy operator-tool (carve-out, non-SKILL_NAMES): $src_co/ -> $dest_co/ (cp -R)"
    echo "[dry-run] post-copy pycache cleanup: $dest_co (find __pycache__/*.pyc -delete)"
  else
    rm -rf "$dest_co"
    mkdir -p "$dest_co"
    cp -R "$src_co"/. "$dest_co"/
    find "$dest_co" -type d -name __pycache__ -prune -exec rm -rf {} + 2>/dev/null || true
    find "$dest_co" -type f -name '*.pyc' -delete 2>/dev/null || true
    echo "deployed operator-tool (carve-out): $dest_co"
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

# 5c. Deploy enforcement hooks (Arc 46 / stoa--xyb.5; Stage 1). GLOB-discovered
# *.sh from substrate/hooks/, deployed unsuffixed (shared tooling, mirrors
# modules). Each GATE script is chmod +x'd at the destination (the harness runs
# them as commands); the underscore-prefixed _hooklib.sh is a SOURCED helper lib
# (never executed directly) so it deploys WITHOUT the exec bit. The hooks/README.md
# (authoring rule + safety note) and the _hooklib.sh shared helper ride along via
# the *.sh + README glob. Skipped in subproject mode (DEST_HOOKS_DIR empty — Arc 46 §11).
#
# CRITICAL SAFETY: this deploy is INERT. The scripts sit dormant on disk;
# Claude Code only fires hooks REGISTERED in a .claude/settings.json, which this
# step never writes. Arming is the separate default-OFF --enable-hooks step
# below (step 5d). Deploying the scripts to a throwaway target cannot arm a hook.
if [ -n "$DEST_HOOKS_DIR" ]; then
  if [ ! -d "$DEST_HOOKS_DIR" ]; then
    run_or_print "mkdir -p \"$DEST_HOOKS_DIR\""
  else
    log "hooks directory already exists: $DEST_HOOKS_DIR"
  fi
  # Deploy the *.sh scripts. The gate scripts (pretooluse-*.sh, stop-self-check.sh)
  # are the executable hooks the harness runs as commands, so they get chmod +x.
  # Underscore-prefixed files (e.g. _hooklib.sh) are SOURCED helper libraries — never
  # executed directly, never registered as a hook — so they deploy WITHOUT the exec bit.
  shopt -s nullglob
  for src in "${SRC_HOOKS_DIR}"/*.sh; do
    hname="$(basename "$src")"
    dest="${DEST_HOOKS_DIR}/${hname}"
    log "deploy hook: ${hname}"   # enumerate/log each deployed hook (observability, mirrors modules)
    case "$hname" in
      _*) _make_exec=0 ;;   # sourced lib (e.g. _hooklib.sh) — no exec bit
      *)  _make_exec=1 ;;   # gate script — executable
    esac
    if [ "$DRY_RUN" -eq 1 ]; then
      if [ "$_make_exec" -eq 1 ]; then
        echo "[dry-run] cp \"$src\" \"$dest\" && chmod +x \"$dest\""
      else
        echo "[dry-run] cp \"$src\" \"$dest\" (sourced lib — no chmod +x)"
      fi
    else
      cp "$src" "$dest"
      if [ "$_make_exec" -eq 1 ]; then
        chmod +x "$dest"
      else
        chmod -x "$dest"   # ensure the sourced lib is NOT executable even if its source mode carried +x
      fi
    fi
  done
  shopt -u nullglob
  # Deploy the hooks README (authoring rule + safety note travels with the scripts).
  if [ -f "${SRC_HOOKS_DIR}/README.md" ]; then
    if [ "$DRY_RUN" -eq 1 ]; then
      echo "[dry-run] cp \"${SRC_HOOKS_DIR}/README.md\" \"${DEST_HOOKS_DIR}/README.md\""
    else
      cp "${SRC_HOOKS_DIR}/README.md" "${DEST_HOOKS_DIR}/README.md"
      echo "deployed: ${DEST_HOOKS_DIR}/README.md"
    fi
  fi
  # Write the PRINCIPAL-identity allow-list the attribution-advisory skill reads,
  # IF it does not already exist (never clobber an operator-curated list). It is
  # the skill's CONFIG — the PRINCIPAL identity to compare against — NOT an author
  # field of any artifact. At project tier we cannot know the PRINCIPAL's name
  # mechanically, so we seed it from `git config` in the target if available,
  # else write a commented template the operator fills in. The advisory's
  # SECONDARY check is SKIPPED when the list is absent or empty (fail-open), so
  # an unfilled template never produces a false report — it just leaves the
  # SECONDARY check dormant until populated (PRIMARY still runs, name-agnostic).
  PRINCIPAL_ID_FILE="${DEST_HOOKS_DIR}/principal-identity"
  if [ -f "$PRINCIPAL_ID_FILE" ]; then
    log "principal-identity allow-list already exists (not clobbered): $PRINCIPAL_ID_FILE"
  elif [ "$DRY_RUN" -eq 1 ]; then
    echo "[dry-run] seed principal-identity allow-list: $PRINCIPAL_ID_FILE"
  else
    _seed_name="$(git config --global user.name 2>/dev/null || true)"
    _seed_email="$(git config --global user.email 2>/dev/null || true)"
    {
      echo "# Stoa attribution-advisory — PRINCIPAL identity allow-list."
      echo "# One accepted name or email per line ('#' comments + blanks ignored)."
      echo "# The attribution-advisory skill's SECONDARY check compares NEW author-like"
      echo "# field VALUES (added in a diff, outside vendored paths) against this list;"
      echo "# a value not on the list is REPORTED for review in the advisory report."
      echo "# It is NEVER blocked or denied — the advisory is report-only. This is the"
      echo "# SKILL'S CONFIG, not an author field of any repo artifact. Widen it when a"
      echo "# legit PRINCIPAL identity is missing. An ABSENT or EMPTY list SKIPS the"
      echo "# SECONDARY check (PRIMARY still runs, name-agnostic). Seeded from the"
      echo "# target's global git identity + any --principal-name passed at install."
      [ -n "$_seed_name" ]  && echo "$_seed_name"
      [ -n "$_seed_email" ] && echo "$_seed_email"
      [ -n "${PRINCIPAL_NAME:-}" ] && echo "$PRINCIPAL_NAME"
    } > "$PRINCIPAL_ID_FILE"
    echo "wrote principal-identity allow-list: $PRINCIPAL_ID_FILE (review + widen as needed)"
  fi
else
  log "hooks deployment skipped (subproject mode — Arc 46 §11)"
fi

# 5d. Arm enforcement hooks — DEFAULT OFF (--enable-hooks). THE ONLY PATH that
# registers a hook in a settings.json. HARD SAFETY CONSTRAINT (design-rev1 §8 /
# ARGUS r4):
#   - When ENABLE_HOOKS=0 (default): do NOTHING here. The scripts deployed above
#     are inert. No settings.json is written. This is the path every Stoa arc
#     and every routine install takes — the running team is never gated by its
#     own build.
#   - When ENABLE_HOOKS=1 at PROJECT tier: merge the candidate settings-hooks.json
#     block (with {{HOOKS_DIR}} substituted) into the TARGET's
#     <project>/.claude/settings.json — never the running build session's.
#   - When ENABLE_HOOKS=1 at USER tier: do NOT auto-write ~/.claude/settings.json
#     (it IS the running config — ARGUS r4). PRINT the manual-merge instruction
#     instead. An agent never auto-writes a live user-tier settings.json.
if [ "$ENABLE_HOOKS" -eq 1 ]; then
  if [ -z "$DEST_HOOKS_DIR" ] || [ -z "$DEST_SETTINGS_JSON" ]; then
    echo "install.sh: warning: --enable-hooks ignored in subproject mode (hooks not deployed at subproject tier — Arc 46 §11)." >&2
  else
    # Render the candidate block with {{HOOKS_DIR}} -> absolute deployed dir.
    _candidate="${DEST_TEMPLATES_DIR}/settings-hooks.json"
    if [ ! -f "$_candidate" ] && [ "$DRY_RUN" -eq 0 ]; then
      echo "install.sh: warning: --enable-hooks: candidate ${_candidate} not found (was --no-templates passed?). Cannot arm; scripts remain inert." >&2
    elif [ "$TARGET" = "user" ]; then
      # USER TIER: never auto-write the live ~/.claude/settings.json. Print the
      # manual-merge runbook (HARD SAFETY CONSTRAINT / ARGUS r4).
      echo
      echo "=========================================================================="
      echo "  --enable-hooks at USER tier: MANUAL merge required (safety)"
      echo "=========================================================================="
      echo "  ~/.claude/settings.json IS your running Claude Code config. This script"
      echo "  will NOT auto-write it. To arm the enforcement hooks, merge the 'hooks'"
      echo "  block from the candidate file into ~/.claude/settings.json yourself,"
      echo "  substituting {{HOOKS_DIR}} -> ${DEST_HOOKS_DIR}:"
      echo
      echo "    candidate: ${_candidate}"
      echo "    target   : ${DEST_SETTINGS_JSON}"
      echo
      echo "  Then verify ${DEST_HOOKS_DIR}/principal-identity lists every valid"
      echo "  PRINCIPAL name/email. To disarm later, remove the 'hooks' block."
      echo "=========================================================================="
    else
      # PROJECT TIER: merge into the target's settings.json (NOT the running
      # session). If the target has no settings.json, create it from the rendered
      # candidate; if it has one, we do NOT silently overwrite — print the merge
      # instruction (a JSON merge needs care; auto-overwriting an existing
      # settings.json could drop the operator's other config).
      if [ "$DRY_RUN" -eq 1 ]; then
        echo "[dry-run] --enable-hooks (project): would render ${_candidate} ({{HOOKS_DIR}} -> ${DEST_HOOKS_DIR}) into ${DEST_SETTINGS_JSON}"
      elif [ -f "$DEST_SETTINGS_JSON" ]; then
        echo
        echo "install.sh: --enable-hooks: ${DEST_SETTINGS_JSON} already exists."
        echo "  Not overwriting (would drop your other settings). Merge the 'hooks'"
        echo "  block from ${_candidate} into it manually, substituting"
        echo "  {{HOOKS_DIR}} -> ${DEST_HOOKS_DIR}."
      else
        sed "s|{{HOOKS_DIR}}|${DEST_HOOKS_DIR}|g" "$_candidate" > "$DEST_SETTINGS_JSON"
        echo "armed enforcement hooks: wrote ${DEST_SETTINGS_JSON} (project-tier target)"
        echo "  Verify ${DEST_HOOKS_DIR}/principal-identity lists every valid PRINCIPAL identity."
      fi
    fi
  fi
fi

# 5e. Arm the Windows PYTHONUTF8 settings 'env' block — DEFAULT OFF
# (--enable-env-block). op-disc §13 (stoa--xyb.14 / Arc C). Mirrors the step 5d
# --enable-hooks posture EXACTLY (same HARD SAFETY CONSTRAINT):
#   - When ENABLE_ENV_BLOCK=0 (default): do NOTHING here. The candidate
#     settings-env-block.json deployed in step 4 is inert — a candidate file sets
#     no env var until merged into a live settings.json. This is the path every
#     routine install takes; no running config is touched.
#   - When ENABLE_ENV_BLOCK=1 at PROJECT tier: write the candidate 'env' block as
#     the TARGET's settings.json IF it has none; if one already exists, do NOT
#     auto-merge (a JSON merge could drop operator config) — print the merge
#     instruction. Never the running build session's settings.json.
#   - When ENABLE_ENV_BLOCK=1 at USER tier: do NOT auto-write
#     ~/.claude/settings.json (it IS the running config — ARGUS r4). PRINT the
#     manual-merge runbook instead.
# No code executes at config time: the block is two static env-var literals.
if [ "$ENABLE_ENV_BLOCK" -eq 1 ]; then
  if [ -z "$DEST_SETTINGS_JSON" ]; then
    echo "install.sh: warning: --enable-env-block ignored in subproject mode (no target settings.json — Arc 46 §11)." >&2
  else
    _env_candidate="${DEST_TEMPLATES_DIR}/settings-env-block.json"
    if [ ! -f "$_env_candidate" ] && [ "$DRY_RUN" -eq 0 ]; then
      echo "install.sh: warning: --enable-env-block: candidate ${_env_candidate} not found (was --no-templates passed?). Cannot arm; env block not written." >&2
    elif [ "$TARGET" = "user" ]; then
      # USER TIER: never auto-write the live ~/.claude/settings.json. Print the
      # manual-merge runbook (HARD SAFETY CONSTRAINT / ARGUS r4).
      echo
      echo "=========================================================================="
      echo "  --enable-env-block at USER tier: MANUAL merge required (safety)"
      echo "=========================================================================="
      echo "  ~/.claude/settings.json IS your running Claude Code config. This script"
      echo "  will NOT auto-write it. To apply the Windows PYTHONUTF8 fix, merge the"
      echo "  'env' block from the candidate file into ~/.claude/settings.json:"
      echo
      echo "    candidate: ${_env_candidate}"
      echo "    target   : ${DEST_SETTINGS_JSON}"
      echo
      echo "  The 'env' block ({PYTHONUTF8, PYTHONIOENCODING}) applies to every"
      echo "  session + every spawned subprocess incl. the Bash tool. To remove"
      echo "  later, delete the two keys from the 'env' block."
      echo "=========================================================================="
    else
      # PROJECT TIER: write into the target's settings.json (NOT the running
      # session). No existing file -> create it from the candidate (which is the
      # bare 'env' block). Existing file -> do NOT silently overwrite (a JSON
      # merge needs care; auto-overwriting could drop the operator's other
      # config) — print the merge instruction. Idempotency: if the env block /
      # its _comment marker is already present, no-op.
      if [ "$DRY_RUN" -eq 1 ]; then
        echo "[dry-run] --enable-env-block (project): would write ${_env_candidate} 'env' block into ${DEST_SETTINGS_JSON}"
      elif [ -f "$DEST_SETTINGS_JSON" ]; then
        if grep -Fq "PYTHONUTF8" "$DEST_SETTINGS_JSON" 2>/dev/null; then
          echo "install.sh: --enable-env-block: ${DEST_SETTINGS_JSON} already carries PYTHONUTF8 — no-op (idempotent)."
        else
          echo
          echo "install.sh: --enable-env-block: ${DEST_SETTINGS_JSON} already exists."
          echo "  Not overwriting (would drop your other settings). Merge the 'env'"
          echo "  block from ${_env_candidate} into it manually."
        fi
      else
        cp "$_env_candidate" "$DEST_SETTINGS_JSON"
        echo "armed env block: wrote ${DEST_SETTINGS_JSON} (project-tier target — PYTHONUTF8/PYTHONIOENCODING)"
      fi
    fi
  fi
fi

# 5f. Deploy the §28 prepare-commit-msg git hook — as an INERT CANDIDATE ONLY
# (op-disc §28 / stoa--xyb.14 / Arc C). LIVE-attack-surface mechanism, so the
# posture is MORE conservative than --enable-hooks: there is NO arming flag.
# Arming a git hook means writing into a .git/hooks/ dir, which install.sh must
# NEVER do — it would arm git-commit behavior in whatever repo install runs
# against (including this build worktree). The candidate is deployed to
# <dest>/.claude/githooks-candidate/ and the colocated README's manual two-method
# runbook is the ONLY arming path. A script in githooks-candidate/ is NOT in any
# .git/hooks/ and is never fired by git. Skipped in subproject mode (consistent
# with the hooks-dir-empty subproject branch).
if [ -n "$DEST_DIR" ] && [ "$TARGET" != "subproject" ]; then
  _githooks_cand_dir="${DEST_DIR}/githooks-candidate"
  _src_githooks_dir="${SCRIPT_DIR}/githooks"
  if [ -f "${_src_githooks_dir}/prepare-commit-msg" ]; then
    if [ "$DRY_RUN" -eq 1 ]; then
      echo "[dry-run] mkdir -p \"${_githooks_cand_dir}\""
      echo "[dry-run] cp \"${_src_githooks_dir}/prepare-commit-msg\" \"${_githooks_cand_dir}/prepare-commit-msg\" && chmod +x (INERT candidate — NOT armed into .git/hooks/)"
      echo "[dry-run] cp \"${_src_githooks_dir}/README.md\" \"${_githooks_cand_dir}/README.md\""
      [ -f "${_src_githooks_dir}/.gitattributes" ] && echo "[dry-run] cp \"${_src_githooks_dir}/.gitattributes\" \"${_githooks_cand_dir}/.gitattributes\" (pins LF eol)"
    else
      mkdir -p "$_githooks_cand_dir"
      cp "${_src_githooks_dir}/prepare-commit-msg" "${_githooks_cand_dir}/prepare-commit-msg"
      chmod +x "${_githooks_cand_dir}/prepare-commit-msg"   # exec bit so a manual copy into .git/hooks/ is runnable; INERT here — not on any hook path
      [ -f "${_src_githooks_dir}/README.md" ] && cp "${_src_githooks_dir}/README.md" "${_githooks_cand_dir}/README.md"
      [ -f "${_src_githooks_dir}/.gitattributes" ] && cp "${_src_githooks_dir}/.gitattributes" "${_githooks_cand_dir}/.gitattributes"
      echo "deployed git-hook CANDIDATE (INERT, never auto-armed): ${_githooks_cand_dir}/prepare-commit-msg"
      echo "  To arm per-clone, follow ${_githooks_cand_dir}/README.md (copy into .git/hooks/ OR set core.hooksPath)."
    fi
  else
    echo "install.sh: warning: §28 git-hook candidate ${_src_githooks_dir}/prepare-commit-msg not found — skipping git-hook candidate deploy." >&2
  fi
else
  log "git-hook candidate deploy skipped (subproject mode — no .git/hooks layer at subproject tier, consistent with hooks deploy)"
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

If \`.claude/.substrate-drift-signal\` exists on disk, surface its contents to the PRINCIPAL at the start of the next orchestrator turn (substrate-drift was detected at session start; do not auto-apply).
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
      # CITE (Arc 63 / stoa--p41.2; design-rev2 §4.3 Block 2): these two dirs are
      # substrate-shipped OPERATOR TOOLS deployed by the step-5a carve-out, not
      # model-invokable skills (their SKILL.md was deleted in Arc 63) — so they
      # are intentionally NOT in SKILL_NAMES and would otherwise be flagged
      # obsolete and DELETED by --prune-obsolete in the same install run that
      # the carve-out deployed them. They are not custom-* either (those are
      # operator-owned); this named exemption is the honest skip for substrate-
      # shipped non-skill operator tools. A future generic mechanism (pass B+)
      # would replace both this and the step-5a carve-out.
      # Arc 64 / stoa--p41.2 (pass B): validate-spec + inspect-script-output added
      # for the same reason — retained operator-tool scripts (SKILL.md removed,
      # check.sh/_check_runner.py/_lib kept) deployed by the step-5a carve-out;
      # they must not be flagged obsolete + deleted in the run that deploys them.
      # save-verdict is NOT here (fully git rm'd — no retained script to exempt).
      check-substrate-updates|check-bw-release|validate-spec|inspect-script-output) continue ;;
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
# CITE: this glob is single-path-segment + file-only (the `[ -f "$f" ]`
# filter skips directories). It does NOT recurse into
# ${DEST_MODULES_DIR}/custom/, where custom modules live per the
# base-vs-custom convention (substrate/operating-disciplines.md §23 +
# substrate/MAJOR_POLYBIUS.md §17). If a future change makes this glob
# recursive, custom modules would be flagged as obsolete; the discipline
# is at the path-shape level.
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

# Hooks staleness (Arc 46 / stoa--xyb.5). GLOB-based against the SOURCE glob
# (substrate/hooks/*.sh) + the README, mirroring the modules scan. File-only
# single-segment shape. CARVE-OUTS: the gate's runtime CONFIG/STATE files are
# NOT substrate-source and must NOT be flagged obsolete —
#   - principal-identity  : operator-curated allow-list (the attribution-advisory skill's SECONDARY-check config)
#   - .stop-sentinels/    : per-turn loop-guard state (a directory; skipped by
#                           the [ -f ] file-only filter anyway, carved out for clarity)
# Skipped in subproject mode (DEST_HOOKS_DIR empty — Arc 46 §11).
if [ -n "${DEST_HOOKS_DIR:-}" ] && [ -d "$DEST_HOOKS_DIR" ]; then
  shopt -s nullglob
  declare -A _src_hook_set=()
  for s in "${SRC_HOOKS_DIR}"/*.sh; do _src_hook_set["$(basename "$s")"]=1; done
  _src_hook_set["README.md"]=1   # the README ships with the scripts
  for f in "${DEST_HOOKS_DIR}"/*; do
    [ -f "$f" ] || continue
    base=$(basename "$f")
    # Carve out the gate's runtime config/state (not substrate source).
    case "$base" in
      principal-identity) continue ;;
    esac
    if [ -z "${_src_hook_set[$base]:-}" ]; then obsolete_files+=("$f"); fi
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

# 7c-bis. Write canonical .claude/.gitignore for substrate-transient runtime
# paths (Arc 55 / stoa--2i5). Unconditional like the manifest write: $DEST_DIR
# is non-empty at all 3 tiers (user/project/subproject), so no [ -n ] guard is
# needed. The file lives inside .claude/, so entries are relative to .claude/.
write_substrate_gitignore "$DEST_DIR"

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
