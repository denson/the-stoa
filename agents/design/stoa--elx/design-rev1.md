<!-- author: Denson Smith -->
<!-- ticket: stoa--elx (arc-75) -->
<!-- from: CAPTAIN_DAEDALUS_the-stoa (ARCHITECT) — Phase A design deliverable -->
<!-- consumes: substrate/arcs/arc-75-build-directive.md + beadwork:attachments/stoa--elx/plan-bw-bootstrap-v2.md (Grand-GATED) -->

# Design rev1 — bw bootstrap into the Stoa install process (OS-split obtention + registry-safe Windows PATH)

## Problem restatement

The Stoa substrate treats `bw` (beadwork) as its durable bus + memory layer, but the install
process never obtains it: `install.sh` calls `bw init` (L473) yet never installs the binary, and
the onboarding skill (`skills/install-stoa/SKILL.md`) explicitly names `bw` a prerequisite and
tells the operator to STOP if it is missing. On a fresh Windows machine this fails *silently* in a
specific way: `bw.exe` can be present and working from git-bash (where `~`-relative dirs resolve via
MSYS) while PowerShell/cmd cannot see it at all, because the binary's directory is not on the
**Windows USER PATH**. This is a PATH problem, not an extension problem (`PATHEXT` already includes
`.EXE`). This arc makes a working, **PowerShell-callable** `bw` a deterministic outcome of standing
a machine up, via one idempotent OS-split helper (`substrate/bootstrap-bw.sh`) wired into two in-repo
consumers: an opt-in `install.sh --bootstrap-bw` pre-flight (DC6) and a guided, consented reversal
of the onboarding skill's Beat 1 (DC7). Unix obtention delegates to upstream's installer; Windows
obtention is ours end-to-end (download + SHA256-verify + extract + registry-safe PATH append). The
Windows USER PATH mutation is the design crux — it MUST be registry-safe and fail-loud, and ARGUS
cold-audits it.

**Assumptions imported into this restatement (named per §6.1):**
- The dedicated dir is `~/.local/bin` (I CONFIRM this below — DC2), unifying the Unix install dir,
  upstream's preferred no-sudo dir, and (on the reference machine) an already-PATH'd dir.
- The third consumer (u--9s2 cookie-cutter) has NO in-repo call-site this arc; the helper is built
  `--yes`-ready for it, but its wiring lands in u--9s2 (DC8 scope guard).
- "Byte-unchanged when the flag is absent" (DC6) is interpreted as: the `--dry-run` OUTPUT of the
  built `install.sh` invoked WITHOUT `--bootstrap-bw` is byte-identical to the pre-arc `install.sh`
  `--dry-run` output. The `--help` output DOES change (the flag is documented there per DC6); the
  header edit does not reach the dry-run output path.

## Ground-truth re-confirmation (this session, against worktree HEAD + upstream)

**Upstream (jallum/beadwork, PUBLIC, verified 2026-07-09):**
- `releases/latest` tag = **`v0.13.2`** (via `gh api repos/jallum/beadwork/releases/latest`) — this
  EQUALS the floor `>=0.13.2`. Floor-via-latest holds: latest clears the floor. **No premise drift.**
- Release assets confirmed present: `beadwork_0.13.2_windows_amd64.zip`,
  `beadwork_0.13.2_windows_arm64.zip`, the four `*_darwin_* / *_linux_*` `.tar.gz`, and
  `beadwork_0.13.2_checksums.txt`.
- `checksums.txt` format = `<sha256>␠␠<filename>` (two spaces). The windows amd64 line:
  `165ae24adc8ea8674df0f673554433a94a7aa9c4fdd395a61149632e6713e295  beadwork_0.13.2_windows_amd64.zip`
  (matches NOMOS's 2026-06-27 read); windows arm64 = `3a9fc99d...`.
- Upstream `install.sh` (raw main) re-read this session, STILL: OS-gate `linux|darwin) ;; *) fail`
  (L24); `INSTALL_DIR` honored first (L11-13), else `~/.local/bin` only if already on PATH (L13-14),
  else `/usr/local/bin` sudo (L16); latest-only via API (L37); asset `.tar.gz` (L40); `tar -xzf`
  (L50); `chmod +x` (L60); **no checksum, no PATH setup.** All directive claims still TRUE.

**Worktree HEAD (cfd683d7 base; branch `stoa--elx/build`) — every cited anchor re-grounded:**
- `substrate/install.sh` = **2120 lines** (confirmed; directive-era 2116 is stale, PLINY's
  re-ground to 2120 is correct).
- Header comment `# install.sh — ...` at L3; `# Usage:` at L25; the three usage command lines at
  **L26-28**; `./install.sh --help` at **L29**; header end-anchor `# Dry-run:` at **L135**.
- `usage()` at **L272**, body: `sed -n '/^# install\.sh — /,/^# Dry-run:.*$/p' "$0" | sed 's/^# \{0,1\}//'`
  — it renders the L3-135 header block, so editing the L26-28 Usage lines is what surfaces in
  `--help`.
- Flag DEFAULTS block at **L146-152** (`MODIFY_CLAUDE_MD=0` L146, `DRY_RUN=0` L147,
  `WITH_CAPTAINS=1` L148, `PRUNE_OBSOLETE=0` L150, `ENABLE_HOOKS=0` L151, `ENABLE_ENV_BLOCK=0` L152).
- Argument-parse `while [ "$#" -gt 0 ]` loop at **L654**, `case` arms through **L748**; the
  `--dry-run)` arm is the MULTI-LINE form at **L701-704** (NOT the one-liner
  `--dry-run) DRY_RUN=1; shift ;;` PLINY's brief sketched — I design to the shipped multi-line
  style); `--enable-hooks)` L717-727; `-h|--help)` at **L742-744**; unknown-arg `err` at L745-746.
- `bw init` call site at **L473**, inside the `scaffold_user_tier()` FUNCTION (defined L444-478),
  which is CALLED at **L777** during target-resolution. Dry-run prints `[dry-run] cd ... bw init`
  (L470) rather than executing.
- Section boundaries: functions L272-650; arg-parse L652-749; validation/resolution L751-914
  (scaffold_user_tier invoked L777); plan L916-990; execute L992+.
- `skills/install-stoa/SKILL.md` = **251 lines**, at the REPO ROOT (per stoa--sok — do NOT move).
  Beat 1 "verify bw is installed" at **L37-51** (STOP language L47-51); "What you must NOT do" list
  L233-242, with the two reversal targets at **L237** ("Do not proceed if bw isn't installed") and
  **L238** ("Do not try to install bw itself ... Out of scope here"); the PRESERVE targets: dry-run
  discipline **L235 + L240**, and the bw-init separation **L241** ("Do not auto-initialize bw after
  install").

**Drift flags (design-to-ship-reality):** (1) install.sh 2116→2120 (PLINY already re-grounded).
(2) PLINY's brief described the boolean-flag arms as one-liners; shipped arms are multi-line — I
match the shipped multi-line style. No load-bearing drift; no premise contradicted.

---

## DC1 — `substrate/bootstrap-bw.sh` (the one shared idempotent core)

A single POSIX-ish bash script (runs under git-bash on Windows, under sh/bash on Unix). Structure:

```
main:
  parse flags: --yes, --check, --dry-run   (mutually compatible; --check implies no-mutation)
  detect_os()        # uname -s → linux | darwin | windows (MINGW*|MSYS*|CYGWIN*)
  detect_arch()      # uname -m → amd64 (x86_64|amd64) | arm64 (aarch64|arm64)
  FLOOR=0.13.2
  if bw_present && version_ge "$(bw_installed_version)" "$FLOOR":
      HAVE_BINARY=1        # but do NOT early-exit yet on Windows (DC3)
  case "$OS" in
    linux|darwin) unix_obtain ;;      # DC4 — delegate to upstream
    windows)      windows_obtain ;;   # DC5 — ours end-to-end
  esac
  ensure_on_path       # DC2 (windows: registry) | shell-rc (unix)
  verify               # DC3 two-independent-checks (windows) | single check (unix)
```

Helper facts:
- `version_ge A B` → `[ "$(printf '%s\n%s' "$B" "$A" | sort -V | head -1)" = "$B" ]` (A>=B).
- `bw_installed_version` → `bw --version 2>/dev/null | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1`.
- **Skip-before-download (idempotent):** obtention DOWNLOAD is skipped when `HAVE_BINARY=1`. On
  Windows the PATH-ensure + DC3 verify STILL run even when the binary is present (this machine's
  prior state: binary present, PowerShell blind). On Unix, `HAVE_BINARY=1` skips the upstream
  invocation entirely (binary + PATH already good) but still ensures the shell-rc line.
- `--check` = report-only: prints OS/arch, bw-present, version, >=floor, dir-on-registry-PATH (Win),
  PowerShell-callable (Win). Mutates nothing, downloads nothing. Exit 0 iff fully provisioned.
- `--dry-run` = prints each planned action ("would download …", "would append … to USER PATH",
  "would verify …") with no write/download.
- `--yes` = non-interactive: suppresses the pre-mutation confirm prompt; on any unsafe condition it
  FAILS LOUD (non-zero exit + manual step) rather than hanging. This is the u--9s2-ready mode.
- Interactive default (no `--yes`): before the Windows PATH mutation, print the exact planned change
  (dir + old/new PATH length) and ask for confirmation. install.sh's `--bootstrap-bw` invokes the
  helper WITH `--yes` (the flag itself is the opt-in consent); the skill invokes `--dry-run` first,
  then `--yes` after showing the PRINCIPAL the release source + SHA + PATH change.

---

## DC2 — Windows USER PATH mutation (the crux; DAEDALUS-owned; ARGUS cold-audits)

### Dir choice — CONFIRMED `~/.local/bin`
Constraint: ONE dir resolvable from BOTH git-bash and PowerShell.
- git-bash form: `$HOME/.local/bin` (`/c/Users/<name>/.local/bin`).
- Windows native form (for the registry + PowerShell): derive via `cygpath -w "$HOME/.local/bin"`
  → `C:\Users\<name>\.local\bin`. Fallback if `cygpath` absent: `"${USERPROFILE}\\.local\\bin"`
  from the env var, or sed-translate `$HOME`.
- Rationale (confirming the plan's recommendation): unifies the Unix install dir, upstream's
  preferred no-sudo dir, and — per the stoa--elx trail — a dir ALREADY on this machine's Windows
  User PATH (the Grand's session `bw.cmd` shim lives there). Idempotent no-op on the reference box.
- Rejected: `~/bin` (not on this machine's PATH, less standard); a new `~/.stoa/bin` (non-standard,
  doesn't unify with Unix/upstream).

### The registry-safe append — exact mechanism
**NEVER `setx`.** `setx` has three defects that clobber PATH: (a) it truncates any value longer than
**1024 chars**; (b) `setx PATH "%PATH%;dir"` EXPANDS `%PATH%`, merging the SYSTEM path into the USER
path (duplication/growth toward the truncation cliff); (c) it writes `REG_SZ`, freezing any
`%USERPROFILE%`-style tokens elsewhere in the value into literals (a `REG_EXPAND_SZ` → `REG_SZ`
downgrade). We use a **read → parse → idempotent-absent-check → length-check → `reg add`** flow that
avoids all three.

```sh
win_ensure_on_path() {
  local dir_win="$1"                         # C:\Users\<name>\.local\bin (from cygpath -w)
  # 1. READ current USER PATH + its TYPE. Key/value may be ABSENT on a fresh machine.
  #    reg query line format: "    Path    REG_EXPAND_SZ    <value>"  (or REG_SZ).
  local raw type cur
  if raw="$(reg query "HKCU\\Environment" /v Path 2>/dev/null)"; then
    type="$(printf '%s\n' "$raw" | grep -oE 'REG_(EXPAND_)?SZ' | head -1)"
    # value = everything after the type token on the Path line (preserve embedded spaces):
    cur="$(printf '%s\n' "$raw" | sed -n 's/.*REG_\(EXPAND_\)\?SZ[[:space:]]\{1,\}//p' | head -1)"
  else
    type="REG_EXPAND_SZ"; cur=""             # absent USER PATH → treat as empty, default type
  fi

  # 2. IDEMPOTENT-ABSENT check (case-insensitive; tolerate trailing backslash + trailing ';').
  local hay=";${cur};"; local needle=";${dir_win};"
  if printf '%s' "$hay" | grep -qiF "$needle"; then
     log "USER PATH already contains $dir_win — no change"; return 0
  fi

  # 3. Build new value (append; our segment is a LITERAL, safe under either type).
  local new
  if [ -z "$cur" ]; then new="$dir_win"; else new="${cur%;};${dir_win}"; fi

  # 4. LENGTH-CHECK before any write. Ceiling = 2047 (conservative USER-PATH ceiling; legacy
  #    Win32 APIs that read the composed PATH into fixed buffers misbehave beyond this).
  if [ "${#new}" -gt 2047 ]; then
     fail_loud_path "$dir_win" "$cur"        # DC2 fail-loud branch — see below. NO WRITE.
     return 1
  fi

  # 5. WRITE preserving the ORIGINAL type (never downgrade REG_EXPAND_SZ → REG_SZ). reg add does
  #    NOT expand %PATH% (we pass a string WE built from the parsed value, not %PATH%), does not
  #    truncate at 1024. In --dry-run/--check, print instead of writing.
  reg add "HKCU\\Environment" /v Path /t "$type" /d "$new" /f >/dev/null \
     || { fail_loud_path "$dir_win" "$cur"; return 1; }

  # 6. Best-effort broadcast so Explorer-spawned shells refresh (does not affect DC3, which
  #    reads the registry directly). Non-fatal if it fails.
  powershell.exe -NoProfile -Command \
    'Add-Type -Namespace W -Name N -MemberDefinition "[DllImport(\"user32.dll\",SetLastError=true)] public static extern IntPtr SendMessageTimeout(IntPtr h,uint m,UIntPtr w,string l,uint f,uint t,out UIntPtr r);"; [UIntPtr]$r=[UIntPtr]::Zero; [void][W.N]::SendMessageTimeout([IntPtr]0xffff,0x1A,[UIntPtr]::Zero,"Environment",2,5000,[ref]$r)' \
    >/dev/null 2>&1 || true
}
```

Key points for the audit:
- We WRITE the whole value ourselves via `reg add` — we never let the shell expand `%PATH%`.
- We PRESERVE the read type. Our appended segment is a literal absolute path (valid under `REG_SZ`
  and `REG_EXPAND_SZ`); we do not introduce a `%token%`, so no expansion dependency, and we do not
  rewrite OTHER entries' tokens (they survive because we re-emit the exact parsed value + our
  suffix under the SAME type).
- Idempotent: re-run finds the needle, returns 0, no write. This is the reference-machine path.

### Fail-loud branch (`fail_loud_path`)
Fires on: length-check exceeded (step 4) OR `reg add` failure (step 5) OR (interactive) declined
consent. It prints a NON-ZERO-exit, one-shot manual step and does NOT write:

```
FAIL: could not safely add  C:\Users\<name>\.local\bin  to your Windows USER PATH.
bw.exe is installed but PowerShell/cmd cannot resolve it until this dir is on your USER PATH.
SAFEST manual fix (clobber-free, preserves %-tokens):
  Press Win, type "Edit environment variables for your account", open it →
  select "Path" under "User variables" → New → paste:  C:\Users\<name>\.local\bin  → OK.
Then open a NEW PowerShell and confirm:  bw --version
```
We deliberately point at the GUI editor (which preserves `REG_EXPAND_SZ` and cannot truncate) rather
than a PowerShell `SetEnvironmentVariable` one-liner — the latter writes `REG_SZ` and would
re-introduce a smaller version of the token-freeze risk in the very fallback meant to be safe.

### Shim fallback (`bw.cmd`) — LAST resort only
Only when the registry append cannot be done safely AND some OTHER dir is ALREADY on the User PATH:
drop a `bw.cmd` forwarder (`@echo off` + `"%~dp0..\.local\bin\bw.exe" %*`, or an absolute forward)
into that already-PATH'd dir. This makes bw PowerShell-callable with zero PATH mutation. It is a
fallback, never the default (the trail RATIFIED PATH-append as default, shim demoted).

---

## DC3 — two-independent-checks (mandatory; the false-green killer)

Two checks, run SEPARATELY; (b) runs EVEN WHEN (a) passes:

- **(a) binary present** (git-bash side): `[ -x "$WIN_BW_DIR/bw.exe" ]` (or `command -v bw` from
  git-bash). This is the check that FALSE-GREENS on its own — bw runs from git-bash while PowerShell
  is blind.
- **(b) PowerShell-callable** (the durable check): a PowerShell probe that reconstructs the User +
  Machine PATH **from the registry** (what a FRESH login shell composes) and resolves `bw` against
  it. This is the load-bearing subtlety: a `powershell.exe` spawned by install.sh INHERITS
  git-bash's env block (which does NOT contain the just-written registry change and MAY contain
  MSYS-only resolution) — so a naive `powershell -Command "bw --version"` is unreliable in BOTH
  directions. Reading the registry-backed User/Machine PATH via `[System.Environment]` is exactly
  what a new session does:

```powershell
# invoked as: powershell.exe -NoProfile -Command <this>
$u = [System.Environment]::GetEnvironmentVariable('Path','User')
$m = [System.Environment]::GetEnvironmentVariable('Path','Machine')
$env:PATH = [System.Environment]::ExpandEnvironmentVariables("$m;$u")   # expands REG_EXPAND_SZ tokens
$c = Get-Command bw -ErrorAction SilentlyContinue
if ($c) { Write-Output ("PS-CALLABLE " + $c.Source); exit 0 } else { exit 1 }
```
`GetEnvironmentVariable(...,'User'/'Machine')` reads the registry-backed values directly (not the
process env block); `ExpandEnvironmentVariables` handles `REG_EXPAND_SZ` `%tokens%`. If `bw.exe` is
in `~/.local/bin` but that dir is NOT on the registry User PATH, this probe EXITS 1 — the exact
false-green this machine exhibited — even though git-bash `bw --version` succeeds.

- **Idempotent-skip requires BOTH (a) AND (b).** A machine with (a)-pass / (b)-fail does NOT skip;
  it proceeds to `win_ensure_on_path`. After the append, (b) is re-run and must pass, else fail-loud.
- **Unix** has no PowerShell surface: a single check `bw --version` with `~/.local/bin` on PATH
  suffices (delegated to upstream + shell-rc).

---

## DC4 — Unix obtention (delegate to upstream; do NOT reinvent)

```sh
unix_obtain() {
  mkdir -p "$HOME/.local/bin"
  ensure_shell_rc_path "$HOME/.local/bin"      # append 'export PATH="$HOME/.local/bin:$PATH"'
                                               # to ~/.bashrc/~/.zshrc/~/.profile if absent (idempotent, marker-guarded)
  if [ "$HAVE_BINARY" = 1 ]; then
    log "bw >= $FLOOR already present — skipping upstream install"; return 0
  fi
  # Pin INSTALL_DIR so upstream's first branch (L11-13) honors it regardless of current PATH state.
  curl -fsSL https://raw.githubusercontent.com/jallum/beadwork/main/install.sh \
    | INSTALL_DIR="$HOME/.local/bin" sh
}
```
- **Version = floor-via-latest** (upstream is latest-only, no pin hook; latest always clears the
  floor). Idempotent skip if already `>= FLOOR`.
- **Checksum = ACCEPT upstream's no-checksum HTTPS posture** (Grand ACCEPTED §4a). Stated as a
  DELIBERATE, RECORDED ASYMMETRY in a helper comment on the Unix branch:
  `# ASYMMETRY (recorded, Grand-accepted §4a): Unix inherits upstream's HTTPS-only, no-checksum`
  `# posture — forcing SHA256 parity here means wrapping/replacing the upstream installer, which`
  `# the OS-split directive forbids. Windows (ours end-to-end) is STRICTER: it SHA256-verifies.`
- Helper does NOT re-implement `tar -xzf`/download on the Unix branch — it curls upstream and pipes
  to `sh` (VERA probe P6 asserts this).

---

## DC5 — Windows obtention (ours end-to-end; SHA256 fail-closed)

```sh
windows_obtain() {
  local dir_win; dir_win="$(cygpath -w "$HOME/.local/bin" 2>/dev/null || printf '%s\\.local\\bin' "$USERPROFILE")"
  local dir_posix="$HOME/.local/bin"; mkdir -p "$dir_posix"
  if [ "$HAVE_BINARY" = 1 ]; then log "bw >= $FLOOR present — skipping download"; else
    local ver; ver="$(latest_version)"                    # curl API + sed, like upstream; else FLOOR
    version_ge "$ver" "$FLOOR" || fail "latest $ver < floor $FLOOR — aborting"
    local base="beadwork_${ver}_windows_${ARCH}"           # ARCH ∈ {amd64, arm64}
    local url="https://github.com/jallum/beadwork/releases/download/v${ver}"
    local tmp; tmp="$(mktemp -d)"
    curl -fsSL -o "$tmp/$base.zip"       "$url/$base.zip"          || fail "download failed: $base.zip"
    curl -fsSL -o "$tmp/checksums.txt"   "$url/beadwork_${ver}_checksums.txt" || fail "download failed: checksums.txt"

    # SHA256 verify — FAIL-CLOSED (no extraction on mismatch). Cross-platform hash compute:
    local want got
    want="$(grep -F "$base.zip" "$tmp/checksums.txt" | awk '{print $1}' | tr 'A-F' 'a-f')"
    if command -v sha256sum >/dev/null 2>&1; then
      got="$(sha256sum "$tmp/$base.zip" | awk '{print $1}' | tr 'A-F' 'a-f')"
    else
      got="$(powershell.exe -NoProfile -Command "(Get-FileHash -Algorithm SHA256 '$(cygpath -w "$tmp/$base.zip")').Hash" | tr -d '\r' | tr 'A-F' 'a-f')"
    fi
    [ -n "$want" ] || { rm -rf "$tmp"; fail "no checksum line for $base.zip"; }
    if [ "$want" != "$got" ]; then
      rm -rf "$tmp"                                         # DELETE, no extraction
      fail "SHA256 MISMATCH for $base.zip (want $want got $got) — aborting, nothing extracted"
    fi

    # Extract ONLY bw.exe (zip also has CHANGELOG/LICENSE/README). Expand-Archive ships with
    # Windows PowerShell 5+ (present on all supported Windows). Extract to temp, move bw.exe.
    powershell.exe -NoProfile -Command "Expand-Archive -Force -Path '$(cygpath -w "$tmp/$base.zip")' -DestinationPath '$(cygpath -w "$tmp/x")'" \
      || { rm -rf "$tmp"; fail "extraction failed"; }
    mv -f "$tmp/x/bw.exe" "$dir_posix/bw.exe" || { rm -rf "$tmp"; fail "bw.exe not found in archive"; }
    rm -rf "$tmp"
  fi
  win_ensure_on_path "$dir_win"                            # DC2
}
```
- **Download tool:** `curl -fsSL` (ships with git-bash and modern Windows).
- **checksums.txt parse:** `grep -F "<base>.zip"` → `awk '{print $1}'`; format is two-space
  `<hash>␠␠<file>`, field 1 is the hash. Normalized to lowercase both sides
  (`Get-FileHash` returns uppercase; `sha256sum`/checksums.txt lowercase).
- **Fail-closed:** any download failure, missing checksum line, or hash mismatch → `rm -rf "$tmp"`
  (no extraction) + non-zero exit. VERA probe P5.

---

## DC6 — `install.sh` opt-in `--bootstrap-bw` (default OFF; absent = byte-unchanged)

Four minimal edits, each guarded so the absent-flag `--dry-run` output is byte-identical to pre-arc.

**(1) Default** — add after L152 (in the L146-152 defaults block), matching the commented style:
```sh
BOOTSTRAP_BW=0          # Arc 75 (stoa--elx): opt-in pre-flight — obtain a PowerShell-callable bw
                        # via substrate/bootstrap-bw.sh BEFORE the deploy body. DEFAULT OFF. When 0,
                        # nothing bootstrap-related runs or prints (byte-unchanged install behavior).
```

**(2) Case arm** — insert immediately BEFORE the `-h|--help)` arm at L742, matching the shipped
multi-line style:
```sh
    --bootstrap-bw)
      BOOTSTRAP_BW=1
      shift
      ;;
```

**(3) Pre-flight invocation** — insert as a GUARDED block right AFTER the arg-parse loop closes
(after `done` at L749) and BEFORE `# ----- validation` at L751. Rationale for THIS placement (not
the bw-init site, not the execute body): the pre-flight must make bw available BEFORE
`scaffold_user_tier` runs `bw init` (called L777, inside the validation/resolution section) —
otherwise a fresh-machine `--target user --bootstrap-bw` would hit `bw init` with no bw. Placement
after the parse loop also keeps it target-independent (bootstrap is OS/arch-based, needs no TARGET).
```sh
# ----- Arc 75 (stoa--elx): optional bw bootstrap pre-flight ------------------
# Opt-in via --bootstrap-bw (default OFF). Delegates the OS split to the helper;
# install.sh does NOT re-implement obtention. --dry-run is passed through.
if [ "$BOOTSTRAP_BW" -eq 1 ]; then
  _bootstrap="${SCRIPT_DIR}/bootstrap-bw.sh"
  [ -x "$_bootstrap" ] || err "--bootstrap-bw: helper not found/executable at $_bootstrap"
  if [ "$DRY_RUN" -eq 1 ]; then
    "$_bootstrap" --dry-run
  else
    "$_bootstrap" --yes
  fi
fi
```
(`SCRIPT_DIR` already exists in install.sh — it is used at L514 `cd "$SCRIPT_DIR"`; confirm the
variable name at build against the shipped definition and reuse it, do not re-derive.)

**(4) `--help` / usage** — extend the Usage lines at L26-28 (user + project rows) to include
`[--bootstrap-bw]`, e.g. append it into the optional-flag group alongside `[--enable-hooks]`. This
changes `--help` output (intended, DC6) but NOT the `--dry-run` output path.

**Why absent-flag output is byte-unchanged:** `BOOTSTRAP_BW=0` ⇒ the pre-flight block's `if` is
false (emits nothing), the case arm is never taken, and NO plan-section line is added (I deliberately
do NOT add a plan echo for bootstrap — keeping the plan section untouched guarantees the dry-run
diff is empty when the flag is absent). The only source additions are inert-when-off. VERA probe P7.

---

## DC7 — onboarding skill canon reversal (`skills/install-stoa/SKILL.md`)

Reverse the OBTENTION canon while PRESERVING the bw-init separation and the dry-run discipline.

**Beat 1 (L37-51) rewrite** — from "STOP, bw is a prereq" to "detect; if missing, drive the guided,
consented bootstrap":
- Keep the L39 fact that `install.sh` does NOT run `bw init` (that is the SEPARATE bw-init concern —
  preserve).
- Keep `bw --version` as the detector.
- Replace the STOP blockquote (L49) + the "Do not try to install bw from this skill" line (L51)
  with a guided branch: if `bw` is missing, OFFER to run `substrate/bootstrap-bw.sh`, and BEFORE
  running it, SHOW the PRINCIPAL: (i) the release source (`github.com/jallum/beadwork`, PUBLIC,
  pinned `>=0.13.2`), (ii) on Windows, that it SHA256-verifies the download against upstream
  `checksums.txt`, and (iii) that it will append `~/.local/bin` (native `C:\Users\...\.local\bin`)
  to the Windows USER PATH via a registry-safe append (never `setx`), or fail loud with a manual
  step. Run `bootstrap-bw.sh --dry-run` FIRST (preserving the skill's dry-run-first discipline),
  show the planned actions, get consent, THEN run for real. If the PRINCIPAL declines, fall back to
  the old behavior (name bw as a prereq and pause).

**"What you must NOT do" edits:**
- **L237** ("Do not proceed if bw isn't installed. … Do not try to install bw from this skill.") →
  REVERSE to: "If bw isn't installed, OFFER the guided bootstrap (Beat 1) with the PRINCIPAL in the
  loop — show the source + SHA256 + PATH change, dry-run first, get consent. Only pause if they
  decline."
- **L238** ("Do not try to install bw itself. … Out of scope here.") → REVERSE / REMOVE: bootstrap
  is now IN scope via the consented helper.
- **L241** ("Do not auto-initialize bw after install.") → **PRESERVE UNCHANGED.** This is the
  bw-INIT separation (POLYBIUS runs `bw init` interactively; install.sh deliberately does not) — a
  DIFFERENT concern from binary OBTENTION. DC7 reverses obtention canon ONLY.
- **L235 + L240** (dry-run discipline) → PRESERVE.
- **L239** ("Do not modify the PRINCIPAL's git config or any system files") → NUANCE, do not blanket
  reverse: the bootstrap DOES modify the Windows USER PATH, but only through the consented helper
  behind an explicit offer. Reword to carve out the consented PATH append (helper-mediated,
  registry-safe, fail-loud) while keeping the general "no unrelated system-file changes" spirit.

**Reversal justification (record in the skill's rationale prose):** bw is fundamental to the
substrate; it fails SILENTLY on fresh Windows (git-bash-green / PowerShell-blind); obtention is
public + pinned + SHA256-verified (Windows) + self-updating (`bw upgrade`); the one-helper opt-in
design preserves the separation-of-concerns spirit (a discrete `bootstrap-bw.sh`, not core-install
bloat; `bw init` stays POLYBIUS's interactive job).

---

## DC8 — honest stance + scope guard + threat posture

**Honest stance.** This is a real, bounded trust surface: the helper DOWNLOADS an executable, PLACES
it on PATH, and MUTATES the Windows USER PATH. Named mitigations: Windows SHA256-verify (fail-closed)
+ HTTPS/TLS on every fetch + following upstream's canonical TLS path on Unix + registry-safe append
+ fail-loud. **No over-claim of "fully sandboxed."** The checksum ASYMMETRY (Windows verifies; Unix
inherits upstream HTTPS-only) is STATED, not hidden (helper comment + DC4 above). Honest residual:
SHA256-verify defends against MITM / CDN-tamper / corruption, NOT a full GitHub-account/release
compromise (the hash and the artifact share one origin) — bounded by GitHub release security.

**Scope guard.** This arc delivers the helper + the TWO in-repo consumers (DC6 install.sh flag, DC7
onboarding skill) ONLY. The THIRD consumer (u--9s2 cookie-cutter, non-interactive builder stand-up)
has NO in-repo call-site — the helper is built `--yes`-ready, but its call-site lands in u--9s2, NOT
here. The historical arc-19 "do not install bw" directive is superseded-in-spirit, NOT edited
(history stays). `bw upgrade` / `bw-upgrade.md` unchanged (helper bootstraps the FIRST binary only;
ongoing upgrades stay `bw upgrade`).

### Threat→mitigation map (A3; §6.12 — all four are named-threat-ratified via the Grand's hard conditions + directive DC8)

`M1 (supply-chain download tamper) → attacker MITMs the download or serves a trojaned artifact from
a compromised CDN path → DEFEATED-BY: Windows SHA256-verify against upstream checksums.txt,
FAIL-CLOSED (no extraction on mismatch) + HTTPS/TLS on zip+checksums fetch; Unix inherits upstream's
canonical HTTPS path (recorded asymmetry §4a). Residual (honest): a full GitHub-release compromise
serves both a bad artifact AND a matching hash — out of scope, bounded by GitHub security.`

`M2 (Windows USER PATH clobber/truncation) → a naive setx truncates PATH >1024 chars, or expands
%PATH% merging system into user, or downgrades REG_EXPAND_SZ→REG_SZ freezing %-tokens → user loses
PATH entries → DEFEATED-BY: registry read→parse-type→idempotent-absent-check→length-check(≤2047)→
reg add preserving original type; never setx; never %PATH% expansion (we emit a string we built from
the parsed value).`

`M3 (PowerShell-blind false-green) → verify runs a git-bash-only bw --version that succeeds while the
registry User PATH still lacks the dir → install reports success but downstream PowerShell substrate
flows fail silently → DEFEATED-BY: two-independent-checks; check (b) reconstructs User+Machine PATH
from the REGISTRY (System.Environment) and resolves bw, and runs EVEN WHEN (a) passes; idempotent
skip requires BOTH.`

`M4 (fail-loud-not-firing) → an unsafe PATH condition (length>ceiling / reg add error / declined
consent) silently proceeds or no-ops, leaving PATH clobbered or bw uncallable behind a green result
→ DEFEATED-BY: explicit fail_loud_path branch — non-zero exit + exact GUI manual step + NO write; in
--yes (u--9s2) mode it fails loud rather than hanging.`

**threat_coverage:**
- `M1 → defeats_via_probe: P5 (SHA256 fail-closed on corrupted zip)`
- `M2 → defeats_via_probe: P2 (registry-safe append against a THROWAWAY value) + P3 (length-check/fail-loud)`
- `M3 → defeats_via_probe: P4 (git-bash-green / PowerShell-blind false-green demonstrably caught)`
- `M4 → defeats_via_probe: P3 (oversized throwaway PATH → fail-loud, non-zero, no write)`

---

## Verification probes (§3 — concrete, VERA-re-executable; threat-anchored per §6.13)

All Windows-mutation probes use a THROWAWAY registry value / probe dir — NEVER this machine's real
`HKCU\Environment` Path (it already has a working bw; untouchable per the directive out-of-scope).

- **P1 — idempotent skip on THIS machine (legit-unaffected).** `bootstrap-bw.sh --check` then
  `--dry-run`: assert bw detected `>= 0.13.2`, DOWNLOAD skipped, `win_ensure_on_path` reports the
  dir already present (no write), DC3 (a)+(b) both PASS, ZERO mutation. (Idempotent/regression-floor.)
- **P2 — registry-safe append, THROWAWAY (M2 attack-blocked half + legit-unaffected half).** Drive
  `win_ensure_on_path` against a synthetic fixture value (pure-string function test, or a throwaway
  key `HKCU\Environment_stoa_test` deleted on teardown): (a) absent-dir fixture → appended exactly
  once; (b) present-dir fixture → NO-OP (idempotent); (c) a fixture containing `%USERPROFILE%`-style
  tokens → tokens PRESERVED and type NOT downgraded; (d) assert the code path contains NO `setx` and
  NO `%PATH%` expansion (grep the helper). NEVER touches the real Path.
- **P3 — length-check / fail-loud (M2 + M4 attack-blocked).** Feed an oversized throwaway PATH
  (> 2047 after append) → assert fail_loud_path fires: non-zero exit, exact GUI manual-step string
  printed, and NO write occurred (throwaway value unchanged).
- **P4 — DC3 false-green demonstrably CAUGHT (M3 attack-blocked).** Place a stub `bw.exe` in a
  throwaway dir that is NOT on the reconstructed registry PATH → assert check (a) PASSES but check
  (b) EXITS 1, and the helper does NOT skip / does NOT report green. (This reproduces the machine's
  prior git-bash-green/PowerShell-blind state without touching real PATH.)
- **P5 — SHA256 fail-closed (M1 attack-blocked).** Corrupt the downloaded zip (flip a byte) OR feed
  a checksums.txt with a wrong hash → assert the helper ABORTS before extraction, non-zero exit, NO
  `bw.exe` placed, temp dir removed. Legit-unaffected half: a correct zip verifies and extracts.
- **P6 — Unix delegates to upstream (DC4).** On a linux/darwin run (or a `uname`-mocked branch):
  assert the helper invokes upstream `install.sh` with `INSTALL_DIR="$HOME/.local/bin"` and does NOT
  re-implement download/extract on the Unix branch (grep: no `tar -xzf` of a bw tarball, no release
  zip logic on that branch); idempotent skip when `>= floor`.
- **P7 — install.sh absent-flag byte-unchanged (DC6 regression bar).**
  `diff <(built install.sh --target user --dry-run) <(pre-arc install.sh --target user --dry-run)`
  → EMPTY. Repeat for `--target project --project-dir <tmp>`. (Assert on REAL dry-run output, not a
  claim.)
- **P8 — flag documented + wired.** `install.sh --help | grep -- '--bootstrap-bw'` present; and
  `install.sh --target user --dry-run --bootstrap-bw` shows the pre-flight delegating to the helper
  in dry-run (helper prints planned actions, no mutation).
- **P9 — standing regression bar.** `npm run gen-data` deterministic (worktree `git diff` empty per
  the gen-data-worktree-diff discipline) + the FULL app vitest suite green. (Even though no role
  files change, the full suite is the bar.)
- **P10 — authorship + conformance (close-gate).** `Author=` Denson Smith zero-foreign on build
  commit(s); §28.9 seat trailer present; NOMOS CONFORMANT on the final commit.

---

## Self-assessed weak points (§6.2 — where the design is thin; probe hardest here)

1. **DC3 child-process env-inheritance is the subtlest, most mis-buildable spot.** The correct
   PowerShell-callability check reads the registry-backed User+Machine PATH via `[System.Environment]`
   and resolves bw against it — NOT a naive `powershell -Command "bw --version"`, which inherits
   git-bash's env block and can false-green (MSYS resolution) OR false-red (registry change not in
   the inherited block). If ADA implements the naive form, the whole DC3 guarantee collapses while
   LOOKING correct. *Why this shape anyway:* it is the only check that verifies the DURABLE state a
   fresh PowerShell session will see; the probe (P4) is designed to catch a naive implementation.
   **ARGUS: audit that the probe actually exercises the registry-reconstructed path, not a child
   powershell.**
2. **The fail-loud manual fallback deliberately avoids a PowerShell one-liner.** `SetEnvironmentVariable(...,'User')` writes `REG_SZ`, which would re-introduce a smaller token-freeze
   risk in the very fallback meant to be safe — so I point at the GUI editor instead. *Why this
   shape anyway:* the GUI preserves `REG_EXPAND_SZ` and cannot truncate. Weakness: it is a
   human-hands step (not scriptable), which slightly dents the u--9s2 non-interactive promise for the
   can't-append edge case — but that edge case is rare (append normally succeeds) and u--9s2 runs on
   machines that mandate human-in-loop setup anyway.
3. **Supply-chain residual is real and NOT closed.** SHA256-verify shares one origin (GitHub) with
   the artifact; a full release/account compromise defeats it. I state this rather than over-claim.
   *Why this shape anyway:* the Grand ACCEPTED the HTTPS posture (§4a); matching Unix's inherited
   posture, Windows is strictly stricter (adds the hash). ARGUS should confirm the honest-stance
   language is not weasel-worded.
4. **`cygpath` / `Expand-Archive` / `reg` tool-presence assumptions.** The Windows branch assumes
   git-bash ships `cygpath` and `curl`, and Windows ships `reg`, `powershell.exe`, and
   `Expand-Archive` (PS 5+). All hold on standard Win10/11 + Git-for-Windows, but a stripped
   environment could lack one. Fallbacks are specified (USERPROFILE for cygpath; Get-FileHash for
   sha256sum) but not for every tool. *Why this shape anyway:* the target IS Git-for-Windows on
   Win10/11 (the substrate's only Windows runtime); broadening further is speculative scope.
5. **arm64 Windows is designed but UN-EXERCISABLE here.** `checksums.txt` ships `windows_arm64.zip`
   and arch detection maps `uname -m` → `arm64`, but the reference machine is amd64; VERA cannot
   drive the arm64 asset path. *Why this shape anyway:* the asset exists upstream and the code is
   symmetric with amd64; the residual is test-coverage, not design.
6. **Version-parse brittleness (inherited).** Parsing `bw --version` and the GitHub API `tag_name`
   via grep/sed mirrors upstream's own brittle sed; a future bw `--version` format change could
   misfire the skip-if-present compare. *Why this shape anyway:* worst case is a redundant re-download
   of latest (still floor-satisfying); the floor semantics bound the blast radius.

## Out of scope (deliberately not addressed)

- The u--9s2 cookie-cutter call-site — helper is `--yes`-ready; wiring lands in u--9s2 (DC8).
- Mutating THIS machine's real Windows USER PATH during build/verify — throwaway probes only.
- Changes to `bw upgrade` / `bw-upgrade.md` — the helper bootstraps the FIRST binary only.
- Editing the historical arc-19 directive — superseded-in-spirit, not rewritten.
- Moving `install-stoa` into `substrate/skills/` — it stays at the repo root (stoa--sok).
- Any real provisioning / money / credentials — N/A (public download, no creds).
- A `bw init` in install.sh — the no-bw-init posture (SKILL.md L241) is PRESERVED, not touched.
