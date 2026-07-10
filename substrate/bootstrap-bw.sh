#!/usr/bin/env bash
#
# bootstrap-bw.sh — idempotent OS-split bootstrap for `bw` (beadwork), the Stoa
# substrate's durable bus + memory layer (Arc 75 / stoa--elx).
#
# Makes a working, PowerShell-callable `bw` a deterministic outcome of standing a
# machine up. OS split:
#   - Unix (linux/darwin): DELEGATE to upstream's installer (jallum/beadwork), pinned
#     to INSTALL_DIR=~/.local/bin. No re-implementation of download/extract.
#   - Windows (MINGW/MSYS/CYGWIN under git-bash): OURS end-to-end — download the
#     release zip + checksums.txt over HTTPS, SHA256-verify FAIL-CLOSED, extract bw.exe
#     into ~/.local/bin, then ensure that dir is on the Windows USER PATH the
#     registry-safe way via the committed sibling win_path.ps1 (never a blind setx).
#
# Idempotent: skips the download when bw >= FLOOR is already present (on Windows it still
# runs the PATH-ensure + the two-independent-checks verify, because a git-bash-callable
# bw can still be invisible to PowerShell — a PATH problem, not an extension problem).
#
# Flags:
#   --yes       non-interactive (for the u--9s2 cookie-cutter builder stand-up); fail loud, never hang.
#   --check     report state only; NO download, NO mutation.
#   --dry-run   print planned actions; NO download, NO mutation (win_path.ps1 runs with -DryRun).
#
# Checksum asymmetry (Grand-accepted, DC4/DC8): Unix inherits upstream's HTTPS-only,
# no-checksum posture (forcing SHA256 parity means wrapping/replacing upstream, which the
# OS-split directive forbids); Windows obtention (ours) is STRICTER — SHA256 fail-closed.
#
# Author: Denson Smith

FLOOR="0.13.2"                      # bw floor (current latest; discharges stoa--fqh)
DIR_POSIX="$HOME/.local/bin"        # unified install dir (Unix + Windows; already PATH'd on the reference box)
GH_API_LATEST="https://api.github.com/repos/jallum/beadwork/releases/latest"
GH_RELEASE_BASE="https://github.com/jallum/beadwork/releases/download"
UPSTREAM_INSTALL="https://raw.githubusercontent.com/jallum/beadwork/main/install.sh"

# The helper resolves its own directory and locates the committed sibling win_path.ps1
# relative to itself (N1-A: win_path.ps1 is a committed file, not a heredoc-emitted temp,
# so the shipped bytes ARE the authored bytes — no bash-interpolation surface to corrupt).
HELPER_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"   # substrate/ when run in-place
WIN_PATH_PS1="${HELPER_DIR}/win_path.ps1"

# Modes (set by parse_args).
CHECK_MODE=0
DRY_RUN_MODE=0
YES_MODE=0

# Populated by detect_*.
OS=""
ARCH=""
HAVE_BINARY=0

# ---------------------------------------------------------------------------
# logging / fail helpers
# ---------------------------------------------------------------------------
log()  { printf '[bootstrap-bw] %s\n' "$*" >&2; }
fail() { printf '[bootstrap-bw] ERROR: %s\n' "$*" >&2; exit 1; }

# fail_loud_path — the Windows PATH-mutation fail-loud branch (M4). Prints the exact
# GUI manual step and does NOT write. Points at the account env-var GUI editor (safer than
# a scriptable REG_SZ-downgrading one-liner), with the honest >2047-USER-Path caveat.
fail_loud_path() {
  local dir_win; dir_win="$(win_dir 2>/dev/null)"
  printf '[bootstrap-bw] PATH-ENSURE FAILED: %s\n' "$*" >&2
  printf '[bootstrap-bw] No change was made to your Windows USER PATH.\n' >&2
  printf '[bootstrap-bw] Manual step: open "Edit environment variables for your account"\n' >&2
  printf '[bootstrap-bw]   (Start > search that phrase), select the USER "Path" variable >\n' >&2
  printf '[bootstrap-bw]   Edit > New, and paste:  %s\n' "$dir_win" >&2
  printf '[bootstrap-bw]   then re-open your shell so PowerShell/cmd pick it up.\n' >&2
  printf '[bootstrap-bw]   (Caveat: the GUI editor caps a single Path input at 2047 chars and may\n' >&2
  printf '[bootstrap-bw]    truncate a USER Path already over 2047 to 4095 on save; a typical USER\n' >&2
  printf '[bootstrap-bw]    Path is well under this.)\n' >&2
  exit 1
}

# ---------------------------------------------------------------------------
# arg parsing
# ---------------------------------------------------------------------------
usage() {
  cat >&2 <<'EOF'
bootstrap-bw.sh — idempotent OS-split bootstrap for bw (beadwork).

Usage:
  bootstrap-bw.sh [--yes] [--check] [--dry-run] [--help]

  --yes       non-interactive (cookie-cutter builder stand-up); fail loud, never hang.
  --check     report state only; no download, no mutation.
  --dry-run   print planned actions; no download, no mutation.
  --help      this message.
EOF
}

parse_args() {
  while [ "$#" -gt 0 ]; do
    case "$1" in
      --yes)     YES_MODE=1; shift ;;
      --check)   CHECK_MODE=1; shift ;;
      --dry-run) DRY_RUN_MODE=1; shift ;;
      -h|--help) usage; exit 0 ;;
      *)         fail "unknown argument: $1 (try --help)" ;;
    esac
  done
}

# ---------------------------------------------------------------------------
# detection
# ---------------------------------------------------------------------------
detect_os() {
  case "$(uname -s)" in
    Linux)                 OS=linux ;;
    Darwin)                OS=darwin ;;
    MINGW*|MSYS*|CYGWIN*)  OS=windows ;;
    *)                     fail "unsupported OS: $(uname -s)" ;;
  esac
}

detect_arch() {
  case "$(uname -m)" in
    x86_64|amd64)   ARCH=amd64 ;;
    aarch64|arm64)  ARCH=arm64 ;;
    *)              fail "unsupported arch: $(uname -m)" ;;
  esac
}

# version_ge A B -> success (0) if A >= B, using version sort.
version_ge() {
  [ "$(printf '%s\n%s\n' "$2" "$1" | sort -V | head -n1)" = "$2" ]
}

# detect_binary — sets HAVE_BINARY=1 if a bw >= FLOOR is callable from THIS (git-bash)
# shell. On Windows this can be a false-green vs PowerShell (which DC3 check (b) catches);
# for the download-skip decision, "present on disk / callable here" is what matters.
detect_binary() {
  HAVE_BINARY=0
  local raw ver
  raw="$(bw --version 2>/dev/null)" || return 0
  ver="$(printf '%s' "$raw" | grep -Eo '[0-9]+\.[0-9]+\.[0-9]+' | head -n1)"
  [ -n "$ver" ] || return 0
  if version_ge "$ver" "$FLOOR"; then HAVE_BINARY=1; fi
}

# win_dir — the Windows-native form of DIR_POSIX (C:\Users\<name>\.local\bin).
win_dir() {
  if command -v cygpath >/dev/null 2>&1; then
    cygpath -w "$DIR_POSIX"
  else
    printf '%s\\.local\\bin' "${USERPROFILE}"
  fi
}

# ---------------------------------------------------------------------------
# DC3 — two-independent-checks (the false-green killer)
# ---------------------------------------------------------------------------
# The PowerShell-callability probe: REASSIGN $env:PATH from the REGISTRY User+Machine
# values (never append) so a git-bash-inherited PATH entry cannot leak in, then resolve bw.
# Single-quoted here so bash does NOT touch the PowerShell $ sigils.
_ps_callable_probe() {
  printf '%s' '$u = [System.Environment]::GetEnvironmentVariable("Path","User"); $m = [System.Environment]::GetEnvironmentVariable("Path","Machine"); $env:PATH = [System.Environment]::ExpandEnvironmentVariables("$m;$u"); $c = Get-Command bw -ErrorAction SilentlyContinue; if ($c) { Write-Output ("PS-CALLABLE " + $c.Source); exit 0 } else { exit 1 }'
}

dc3_verify_windows() {
  # (a) binary present (git-bash side) — this is the check that FALSE-GREENS alone.
  if [ -x "$DIR_POSIX/bw.exe" ] || command -v bw >/dev/null 2>&1; then
    log "DC3(a) binary present: PASS"
  else
    fail "DC3(a) binary not present at $DIR_POSIX/bw.exe"
  fi
  # (b) PowerShell-callable (durable check) — runs EVEN WHEN (a) passes.
  local probe; probe="$(_ps_callable_probe)"
  if powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "$probe" >/dev/null 2>&1; then
    log "DC3(b) PowerShell can resolve bw from the registry User+Machine PATH: PASS"
  else
    fail_loud_path "DC3(b) PowerShell cannot resolve bw from the registry PATH — the PATH mutation did not take"
  fi
}

dc3_verify_unix() {
  # Unix has no PowerShell surface: a single bw --version with ~/.local/bin on PATH suffices.
  PATH="$DIR_POSIX:$PATH" bw --version >/dev/null 2>&1 \
    && log "DC3 unix: bw callable with $DIR_POSIX on PATH: PASS" \
    || fail "bw not callable after install (expected in $DIR_POSIX)"
}

# ---------------------------------------------------------------------------
# DC2 — Windows USER PATH mutation via the committed sibling win_path.ps1
# ---------------------------------------------------------------------------
# rev3 N2: capture rc=$? on the IMMEDIATELY-following line after the powershell.exe call —
# NO pipe (a pipeline makes $? the last stage's exit), NO `|| true` (would swallow the exit).
# rc 3/4/5 -> fail_loud_path (NO write happened; never overwrite); rc 0 -> proceed to DC3.
win_ensure_on_path() {
  local dir_win="$1"
  local ps1="${HELPER_DIR}/win_path.ps1"
  [ -f "$ps1" ] || fail_loud_path "win_path.ps1 not found at $ps1"       # N1-A sibling guard, fail loud
  local extra=()
  [ "${DRY_RUN_MODE:-0}" -eq 1 ] && extra+=(-DryRun)
  # Capture stdout (the RESULT= line) AND the exit code. rc=$? is on the IMMEDIATELY-following line;
  # no pipe, no `|| true` — a pipeline or a `|| true` would replace the PS exit with something else.
  local out rc
  out="$(powershell.exe -NoProfile -ExecutionPolicy Bypass \
          -File "$(cygpath -w "$ps1")" \
          -Dir "$dir_win" -KeyName "${WIN_PATH_KEY:-Environment}" -Ceiling 4095 "${extra[@]}")"
  rc=$?                                                                  # <-- IMMEDIATELY; no swallow
  case "$rc" in
    0)      log "win_path: $out"; return 0 ;;                            # present/appended/would_append → DC3 verify
    3|4|5)  fail_loud_path "win_path rc=$rc ($out) — NO write happened; never overwrite" ;;  # F2/F3/M4
    *)      fail_loud_path "win_path unexpected rc=$rc ($out) — NO write assumed" ;;          # defensive
  esac
}

# ---------------------------------------------------------------------------
# DC4 — Unix obtention (delegate to upstream; do NOT reinvent)
# ---------------------------------------------------------------------------
# ensure_shell_rc_path — idempotent, marker-guarded append of DIR to the shell rc so a
# fresh login shell has ~/.local/bin on PATH.
ensure_shell_rc_path() {
  local dir="$1"
  local rc_file="$HOME/.bashrc"
  [ -f "$HOME/.bashrc" ] || rc_file="$HOME/.profile"
  local marker="# >>> stoa bootstrap-bw PATH (~/.local/bin) >>>"
  if [ -f "$rc_file" ] && grep -Fq "$marker" "$rc_file"; then
    log "shell-rc PATH already ensured in $rc_file (idempotent no-op)"
    return 0
  fi
  if [ "$DRY_RUN_MODE" -eq 1 ] || [ "$CHECK_MODE" -eq 1 ]; then
    log "[no-mutation] would append a marker-guarded 'export PATH=$dir:\$PATH' to $rc_file"
    return 0
  fi
  {
    printf '\n%s\n' "$marker"
    printf 'export PATH="%s:$PATH"\n' "$dir"
    printf '%s\n' "# <<< stoa bootstrap-bw PATH (~/.local/bin) <<<"
  } >> "$rc_file"
  log "appended marker-guarded PATH export for $dir to $rc_file"
}

unix_obtain() {
  mkdir -p "$DIR_POSIX"
  ensure_shell_rc_path "$DIR_POSIX"            # idempotent marker-guarded shell-rc append
  [ "$HAVE_BINARY" = 1 ] && { log "bw >= $FLOOR present — skipping upstream install"; return 0; }
  if [ "$DRY_RUN_MODE" -eq 1 ]; then
    log "[dry-run] would run: curl -fsSL $UPSTREAM_INSTALL | INSTALL_DIR=\"$DIR_POSIX\" sh"
    return 0
  fi
  # Checksum ASYMMETRY (Grand-accepted, DC4/DC8): the Unix branch DELEGATES to upstream's
  # installer, which is HTTPS-only / NO-checksum. Forcing SHA256 parity would mean wrapping or
  # replacing upstream, which the OS-split directive forbids. Windows (below) is stricter.
  curl -fsSL "$UPSTREAM_INSTALL" \
    | INSTALL_DIR="$DIR_POSIX" sh              # pin INSTALL_DIR so upstream honors it (its L11-13)
}

# ---------------------------------------------------------------------------
# DC5 — Windows obtention (ours end-to-end; SHA256 fail-closed)
# ---------------------------------------------------------------------------
# resolve_latest_version — floor-via-latest: upstream is latest-only with no pin hook, and
# latest always clears the floor. Parse GitHub's latest-release tag_name (grep/sed, mirrors
# upstream's parse brittleness — worst case is a redundant re-download of latest).
resolve_latest_version() {
  local ver
  ver="$(curl -fsSL "$GH_API_LATEST" 2>/dev/null \
    | grep -m1 '"tag_name"' \
    | sed -E 's/.*"tag_name"[[:space:]]*:[[:space:]]*"v?([^"]+)".*/\1/')"
  [ -n "$ver" ] || ver="$FLOOR"
  printf '%s' "$ver"
}

# sha256_hex FILE -> lowercase hex digest. Cross-platform: sha256sum else Get-FileHash.
sha256_hex() {
  local f="$1"
  if command -v sha256sum >/dev/null 2>&1; then
    sha256sum "$f" | awk '{print $1}' | tr 'A-Z' 'a-z'
  else
    powershell.exe -NoProfile -Command \
      "(Get-FileHash -Algorithm SHA256 -LiteralPath '$(cygpath -w "$f")').Hash" \
      | tr -d '\r' | tr 'A-Z' 'a-z'
  fi
}

win_obtain() {
  local arch="$1"
  if [ "$DRY_RUN_MODE" -eq 1 ]; then
    log "[dry-run] would resolve latest (>= $FLOOR), download beadwork_<ver>_windows_${arch}.zip + checksums.txt over HTTPS, SHA256-verify FAIL-CLOSED, extract bw.exe to $DIR_POSIX"
    return 0
  fi
  local ver; ver="$(resolve_latest_version)"
  version_ge "$ver" "$FLOOR" || fail "resolved bw version $ver is below floor $FLOOR"
  local base="beadwork_${ver}_windows_${arch}"
  local zip_url="${GH_RELEASE_BASE}/v${ver}/${base}.zip"
  local sums_url="${GH_RELEASE_BASE}/v${ver}/beadwork_${ver}_checksums.txt"

  local tmp; tmp="$(mktemp -d)"
  [ -d "$tmp" ] || fail "mktemp -d failed"
  local zip="${tmp}/${base}.zip"
  local sums="${tmp}/checksums.txt"

  log "downloading $zip_url"
  curl -fsSL "$zip_url"  -o "$zip"  || { rm -rf "$tmp"; fail "download failed: $zip_url"; }
  log "downloading $sums_url"
  curl -fsSL "$sums_url" -o "$sums" || { rm -rf "$tmp"; fail "download failed: $sums_url"; }

  # SHA256 verify FAIL-CLOSED. checksums.txt lines are `<sha256>  <file>`; select the exact
  # zip name (amd64 is not a substring of arm64); a multi-match fails closed.
  local matches count expected actual
  matches="$(grep -F "${base}.zip" "$sums")"
  count="$(printf '%s\n' "$matches" | grep -c .)"
  if [ "$count" -ne 1 ]; then
    rm -rf "$tmp"
    fail "checksums.txt: expected exactly 1 entry for ${base}.zip, found $count — aborting (fail-closed)"
  fi
  expected="$(printf '%s\n' "$matches" | awk '{print $1}' | tr 'A-Z' 'a-z')"
  actual="$(sha256_hex "$zip")"
  if [ -z "$expected" ] || [ "$actual" != "$expected" ]; then
    rm -rf "$tmp"
    fail "SHA256 MISMATCH for ${base}.zip (expected=$expected actual=$actual) — aborting, NO extraction"
  fi
  log "SHA256 OK for ${base}.zip"

  # Extract only bw.exe via Expand-Archive, place in ~/.local/bin.
  local ext="${tmp}/extract"
  mkdir -p "$ext"
  powershell.exe -NoProfile -Command \
    "Expand-Archive -LiteralPath '$(cygpath -w "$zip")' -DestinationPath '$(cygpath -w "$ext")' -Force" \
    || { rm -rf "$tmp"; fail "Expand-Archive failed for ${base}.zip"; }
  if [ ! -f "${ext}/bw.exe" ]; then
    rm -rf "$tmp"
    fail "bw.exe not found in ${base}.zip after extraction"
  fi
  mkdir -p "$DIR_POSIX"
  cp "${ext}/bw.exe" "${DIR_POSIX}/bw.exe" || { rm -rf "$tmp"; fail "failed to place bw.exe in $DIR_POSIX"; }
  rm -rf "$tmp"
  log "placed bw.exe (v$ver, windows/$arch) in $DIR_POSIX"
}

# ---------------------------------------------------------------------------
# --check — report state only; NO download, NO mutation
# ---------------------------------------------------------------------------
check_report() {
  log "check: os=$OS arch=$ARCH bw>=$FLOOR(this shell)=$HAVE_BINARY floor=$FLOOR"
  if [ "$OS" = "windows" ]; then
    local probe; probe="$(_ps_callable_probe)"
    if powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "$probe" >/dev/null 2>&1; then
      log "check: PowerShell can resolve bw from the registry User+Machine PATH: YES"
    else
      log "check: PowerShell can resolve bw from the registry User+Machine PATH: NO (dir not on USER PATH)"
    fi
    log "check: target dir = $(win_dir)  (no changes made)"
  else
    log "check: target dir = $DIR_POSIX  (no changes made)"
  fi
}

# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
main() {
  parse_args "$@"
  detect_os
  detect_arch
  detect_binary
  log "os=$OS arch=$ARCH bw_present(this shell)=$HAVE_BINARY floor=$FLOOR check=$CHECK_MODE dry_run=$DRY_RUN_MODE yes=$YES_MODE"

  if [ "$CHECK_MODE" -eq 1 ]; then
    check_report
    return 0
  fi

  if [ "$OS" = "windows" ]; then
    # DC1: skip download if bw >= floor is present, but STILL ensure PATH + verify (DC3),
    # because a git-bash-callable bw can be invisible to PowerShell (a PATH problem).
    if [ "$HAVE_BINARY" -eq 1 ]; then
      log "bw >= $FLOOR already present — skipping download; still ensuring PATH + verifying (DC1)"
    else
      win_obtain "$ARCH"
    fi
    local dir_win; dir_win="$(win_dir)"
    win_ensure_on_path "$dir_win"
    if [ "$DRY_RUN_MODE" -eq 1 ]; then
      log "[dry-run] would verify DC3 (a) binary present + (b) PowerShell-callable from the registry PATH"
    else
      dc3_verify_windows
    fi
  else
    unix_obtain
    if [ "$DRY_RUN_MODE" -eq 1 ]; then
      log "[dry-run] would verify bw --version with $DIR_POSIX on PATH"
    else
      dc3_verify_unix
    fi
  fi

  log "bootstrap-bw complete (os=$OS)."
}

main "$@"
