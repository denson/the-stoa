#!/usr/bin/env bash
# P6 — Unix delegates to upstream (DC4). Static trace + dry-run drive of shipped unix_obtain.
set -u
WT="C:/Users/denso/claude_projects/the-stoa/.claude/worktrees/arc-75-build"
H="$WT/substrate/bootstrap-bw.sh"

echo "===== STATIC: Unix branch delegates, does NOT reimplement extract ====="
echo "-- unix_obtain pins INSTALL_DIR to \$HOME/.local/bin and pipes upstream install.sh:"
grep -n 'INSTALL_DIR="\$DIR_POSIX" sh\|UPSTREAM_INSTALL\|curl -fsSL "\$UPSTREAM_INSTALL"' "$H"
echo
echo "-- NO tar -xzf / unzip anywhere in the helper (Windows uses Expand-Archive; Unix delegates):"
if grep -n -E 'tar +-x|tar +[a-z]*x[a-z]*z|unzip ' "$H"; then echo "  !!! FOUND reimplemented extract"; else echo "  NONE — good (no tar/unzip reimplementation)"; fi
echo
echo "-- idempotent skip when >= floor (HAVE_BINARY=1) on the Unix branch:"
grep -n 'HAVE_BINARY = 1 .*skipping upstream install' "$H"

echo
echo "===== DRY-RUN DRIVE: shipped unix_obtain on a linux branch (no network, no mutation) ====="
SRC="$(mktemp).sh"; sed '/^main "\$@"$/d' "$H" > "$SRC"; source "$SRC"
DIR_POSIX="$(mktemp -d)"; DRY_RUN_MODE=1; CHECK_MODE=0; HAVE_BINARY=0; OS=linux
echo "-- HAVE_BINARY=0 (would install):"
unix_obtain
echo
echo "-- HAVE_BINARY=1 (idempotent skip):"
HAVE_BINARY=1; unix_obtain
rm -rf "$DIR_POSIX" "$SRC"