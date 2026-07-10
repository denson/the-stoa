#!/usr/bin/env bash
# P5 — SHA256 fail-closed (M1). Drives the SHIPPED win_obtain by shadowing `curl` with a
# local-mirror shim (feeds controlled zip/checksums). Target dir overridden to a TEMP dir —
# NEVER the real ~/.local/bin. Real upstream v0.13.2 windows amd64 asset used for the legit half.
set -u
WT="C:/Users/denso/claude_projects/the-stoa/.claude/worktrees/arc-75-build"

# 1. mirror with the REAL asset (fetched read-only once)
MIR="$(mktemp -d)"
curl -fsSL "https://github.com/jallum/beadwork/releases/download/v0.13.2/beadwork_0.13.2_windows_amd64.zip" -o "$MIR/zip.orig"
curl -fsSL "https://github.com/jallum/beadwork/releases/download/v0.13.2/beadwork_0.13.2_checksums.txt"    -o "$MIR/sums.orig"

# 2. source the shipped helper with the auto-main line stripped, so its functions load without running main.
SRC="$(mktemp).sh"
sed '/^main "\$@"$/d' "$WT/substrate/bootstrap-bw.sh" > "$SRC"
# shellcheck disable=SC1090
source "$SRC"

# 3. curl shim — serve the mirror. $ZIP_SRC / $SUMS_SRC select which files win_obtain receives.
curl() {
  local url="" out=""
  while [ "$#" -gt 0 ]; do case "$1" in -o) out="$2"; shift 2;; -fsSL|-fSL|-sSL) shift;; http*|file*) url="$1"; shift;; *) shift;; esac; done
  case "$url" in
    *api.github.com*) printf '{ "tag_name": "v0.13.2" }\n'; return 0 ;;
    *windows_amd64.zip) cp "$ZIP_SRC" "$out"; return 0 ;;
    *checksums.txt)     cp "$SUMS_SRC" "$out"; return 0 ;;
    *) return 22 ;;
  esac
}

runcase() {
  local label="$1"
  local target; target="$(mktemp -d)"
  DIR_POSIX="$target"; DRY_RUN_MODE=0; ARCH=amd64
  echo "######## $label ########"
  ( win_obtain amd64 ) ; local rc=$?
  echo "  win_obtain exit=$rc"
  if [ -f "$target/bw.exe" ]; then
    echo "  bw.exe PLACED in target -> $("$target/bw.exe" --version 2>/dev/null || echo '(placed)')"
  else
    echo "  bw.exe NOT placed in target (fail-closed: no extraction on mismatch)"
  fi
  rm -rf "$target"
  echo
}

echo "=== P5 LEGIT: correct zip + correct checksums -> verify + extract + place ==="
ZIP_SRC="$MIR/zip.orig"; SUMS_SRC="$MIR/sums.orig"
runcase "LEGIT (real v0.13.2 asset)"

echo "=== P5 CORRUPT ZIP: flip a byte in the zip -> SHA256 mismatch -> ABORT, no placement ==="
cp "$MIR/zip.orig" "$MIR/zip.bad"
# flip one byte deep in the file
printf '\xFF' | dd of="$MIR/zip.bad" bs=1 seek=1000 count=1 conv=notrunc >/dev/null 2>&1
ZIP_SRC="$MIR/zip.bad"; SUMS_SRC="$MIR/sums.orig"
runcase "CORRUPT ZIP (1 byte flipped)"

echo "=== P5 WRONG-HASH checksums.txt: tamper the checksums entry -> mismatch -> ABORT ==="
sed 's/^[0-9a-f]\{64\}\(  beadwork_0.13.2_windows_amd64.zip\)/0000000000000000000000000000000000000000000000000000000000000000\1/' "$MIR/sums.orig" > "$MIR/sums.bad"
echo "  tampered entry: $(grep -F windows_amd64.zip "$MIR/sums.bad")"
ZIP_SRC="$MIR/zip.orig"; SUMS_SRC="$MIR/sums.bad"
runcase "WRONG-HASH checksums.txt"

rm -rf "$MIR" "$SRC"
echo "P5 cleanup done."