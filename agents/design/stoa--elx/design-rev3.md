<!-- author: Denson Smith -->
<!-- ticket: stoa--elx (arc-75) -->
<!-- from: CAPTAIN_DAEDALUS_the-stoa (ARCHITECT) — Phase A design deliverable, rev3 -->
<!-- supersedes: agents/design/stoa--elx/design-rev2.md (rev3 wins on any conflict; rev2 kept on disk) -->
<!-- consumes: design-rev2 (ARGUS RE-AUDIT = GO-WITH-CONDITIONS; F1-F9 CLOSED, verbatim intent preserved) + ARGUS rev2 non-load-bearing findings N1-N4 -->

# Design rev3 — bw bootstrap into the Stoa install process (OS-split obtention + registry-safe Windows PATH)

## Phase-D errata (PLINY per-arc design-canon audit, MAJOR_PLINY §6; added post-gauntlet 2026-07-10)

Two accuracy corrections from the Phase-C gauntlet (VERA PASS + CATO PASS-WITH-NITS + NOMOS CONFORMANT on build b698f4ef). Neither changed the built artifact; both are recorded here so the design canon matches shipped reality.

- **DC2.0 stale-machine-state claim.** DC2.0's empirical read of the reference machine's PATH registry value (REG_SZ / raw length 800 / `C:\Users\denso\.local\bin` first entry) is accurate. But the accompanying assumption that "bw ≥ 0.13.2 is present → the idempotent-skip is the reference-machine path" is STALE: VERA found the actual bw on PATH is **0.13.1** (below the 0.13.2 floor), so on this machine in its current state `HAVE_BINARY=0` and the helper would **OBTAIN**, not skip. The shipped `version_ge`/`HAVE_BINARY` logic correctly does NOT skip on a below-floor version (VERA unit-verified `version_ge "0.13.1" "0.13.2"` = false). The idempotent-skip narrative in DC1/DC2.0 applies to a genuinely ≥floor machine — not this reference box, which is itself exactly the below-floor state the floor + helper exist to fix (ties to stoa--fqh). No build defect; design-narrative correction only.
- **CATO NITs c1–c4 (behavior-neutral hygiene, CATO-rated shippable; documented post-gate polish).** c1 = `win_path.ps1` catch/exit-5 path omits `$wk.Close()` (process exits immediately, handle released by the OS, `SetValue` never reached on that path); c2 = the `-Broadcast` switch is a documented no-op stub (DC3 reads the registry directly); c3 = `bootstrap-bw.sh` `tmp="$(mktemp -d)"` unguarded (every downstream `rm -rf "$tmp"` is quoted → an empty `$tmp` is a harmless no-op); c4 = the `win_ensure_on_path` `rc=$?` is a non-local global (read immediately by the next `case`; matches this design's N2 sketch verbatim). All four are byte-neutral; c1/c2 live in the twice-ARGUS-audited byte-exact `win_path.ps1` crux, so the polish was deferred to a single reviewed commit AFTER the Grand's second gate to preserve the fully-gauntleted single-SHA provenance of the built artifact (deferral rationale retained for the record). **DISCHARGED:** c1–c4 were APPLIED in the post-gate polish commit (Grand-ratified fold-first sequence); the `win_path.ps1` body and the `win_ensure_on_path` wrapper embedded above are synced byte-exact to the shipped files after those edits (c1 = `finally { if ($null -ne $wk) { $wk.Close() } }`; c2 = `-Broadcast` param token + no-op stub removed; c3 = `[ -d "$tmp" ] || fail "mktemp -d failed"` guard in `win_obtain`, not embedded here; c4 = `local out rc`).

## What rev3 changes (delta from rev2)

rev2 passed ARGUS RE-AUDIT with **GO-WITH-CONDITIONS**: the two BLOCKING findings (F1 registry-read
mangling, F2 read-failure clobber) are structurally CLOSED — ARGUS independently reproduced the whole
DC2 PowerShell .NET mechanism end-to-end against throwaway keys — and F3-F9 are closed. **Nothing
already closed is re-litigated here:** the DC2 mechanism, the 4095 composed-PATH ceiling (ARGUS
web-confirmed exact), the F2 discrimination, and every discharged section carry over **verbatim in
intent**. rev3 is a TIGHT delta that folds ARGUS's four NEW non-load-bearing findings (N1-N4) into the
gated canon so the spec is authoritative for ADA/VERA. The four folds:

- **N1 (emission integrity — HIGHEST).** rev2 said the helper "writes `win_path.ps1` (heredoc)" but
  never pinned that the emitted script must be **byte-identical to the authored PowerShell source** (PS
  sigils `$wk`, `$($_.Exception.Message)`, `[Microsoft.Win32.Registry]::…` preserved). An UNQUOTED bash
  heredoc would let bash expand every `$`/`$()` → a corrupted script. **rev3 chooses option A: ship
  `substrate/win_path.ps1` as a COMMITTED FILE** alongside `substrate/bootstrap-bw.sh`; the helper
  invokes it via `-File "${HELPER_DIR}/win_path.ps1"`. This removes the emission-integrity risk class
  entirely (there is no emission step to corrupt). Deliverables list, DC1, and the DC2 invocation
  contract updated. **P2 now drives the SHIPPED `win_path.ps1`** (the actual artifact ADA commits), so
  the shipping path itself is under test.
- **N2 (bash-side exit-code capture).** rev2 gave the PS-exit→action map as a prose table but never
  wrote the bash wrapper. rev3 pins `win_ensure_on_path`: capture `rc=$?` on the **very next line**
  after the `powershell.exe` call (no pipe, no `|| true`), rc 3/4/5 → `fail_loud_path`, rc 0 → proceed
  to DC3. A concrete wrapper sketch is added to DC2 so ADA builds it exactly. (F2 is already closed by
  the .ps1 being the only writer; this is message-precision hardening.)
- **N3 (P4 fixture POSIX export).** rev3 pins that P4 exports the stub dir in **POSIX form** (`/c/…`,
  the `mktemp -d` output) via `export PATH=<posix-stub>:$PATH`, and that P4 **FIRST asserts the naive
  `powershell -Command "bw --version"` DOES resolve the stub (exit 0 — the false-green is live)** before
  asserting the correct registry-reassign check (b) does NOT (exit 1). Without the POSIX-form export the
  stub is mangled and both forms exit 1 → P4 false-passes and re-opens the F5 blind spot at the test
  layer.
- **N4 (pre-flight placement target-independence).** rev2's F6 fix could be read as satisfiable INSIDE
  the `user)` arm; rev3 pins the pre-flight block **AFTER the `[ -n "$TARGET" ] || err` check (L753) and
  BEFORE `case "$TARGET" in` (L761)** so it runs for `--target project|subproject` too (target-independent,
  the design's own rationale), still errors first on a missing `--target`, and still runs before `bw init`
  (L777) for the user path. DC6 edit (3) updated; absent-flag byte-unchanged re-confirmed at this placement.

**Ground-check (this session, shipped `substrate/install.sh` in the worktree):** L753 = `[ -n "$TARGET" ]
|| err "--target is required (user|project|subproject)"`; L761 = `case "$TARGET" in`; L777 = the
`scaffold_user_tier` call (where `bw init` fires); L155 = `SCRIPT_DIR=`. Confirmed against shipped
reality before citing.

### Deliverables (rev3 — updated for the N1-A committed-file fold)

1. `substrate/bootstrap-bw.sh` (NEW) — the idempotent OS-split helper (DC1-DC5), `--yes`/`--check`/`--dry-run`.
2. **`substrate/win_path.ps1` (NEW — added by N1-A)** — the registry-safe Windows PATH mutation script,
   the security crux, invoked by the helper via `-File`; authored verbatim as the §DC2 body, committed
   as a standalone auditable file (the highest-risk code in the arc lives as a reviewable file, not a
   heredoc). Author field / attribution: Denson Smith.
3. `substrate/install.sh` — the opt-in `--bootstrap-bw` flag (DC6) + `--help` entry; absent-flag behavior
   byte-unchanged.
4. `skills/install-stoa/SKILL.md` — the Beat 1 + "must NOT" canon reversal (DC7).
5. Charter `stoa--elx` updated with the landing SHA + per-DC disposition.

(The directive's original 4-item Deliverables list becomes 5 with `win_path.ps1`; this is the only new
deliverable rev3 introduces, and it is a extraction of already-designed §DC2 code into its own file —
not new scope.)

---

## What rev2 changes (delta from rev1)

rev1 went through ARGUS cold-audit and returned **NO-GO** with two BLOCKING findings (F1, F2) on
the DC2 core plus three SHOULD-FIX (F3, F4, F5) and four fold-ins (F6-F9). This is by-the-book: the
gauntlet broke the crux before build. rev2's delta is **entirely** the Windows PATH-mutation
mechanism and its probes; every rev1 section ARGUS discharged (Unix delegation, SHA256 compute,
checksums.txt uniqueness, DC6 byte-unchanged, DC7 skill reversal, scope, authorship) is preserved
verbatim in intent and repeated below only where a fold-in touches it.

**The single load-bearing change:** the DC2 registry read/parse/write is **no longer `reg.exe`
through git-bash**. It is a **PowerShell .NET-registry-API script** (`[Microsoft.Win32.Registry]`)
that the bash helper invokes via `-File`. This one decision resolves F1
(MSYS switch-mangling — there are no `/v /t /d /f` switches to mangle), dissolves F4 (no bash-side
CRLF parsing of `reg query` output), and cleanly resolves F2 (a provably-absent value is an
affirmative `$null` return; any read failure is a distinct non-zero exit that FAILS LOUD, never
falls through to overwrite). **I ran this mechanism end-to-end on this machine before writing rev2
— the empirical proof is §DC2.0 below.**

---

## Problem restatement

The Stoa substrate treats `bw` (beadwork) as its durable bus + memory layer, but the install process
never obtains it: `install.sh` calls `bw init` (inside `scaffold_user_tier`, L473) yet never installs
the binary, and the onboarding skill (`skills/install-stoa/SKILL.md`) names `bw` a prerequisite and
tells the operator to STOP if it is missing. On a fresh Windows machine this fails *silently* in a
specific way: `bw.exe` can be present and working from git-bash (where `~`-relative dirs resolve via
MSYS) while PowerShell/cmd cannot see it at all, because the binary's directory is not on the
**Windows USER PATH**. This is a PATH problem, not an extension problem (`PATHEXT` already includes
`.EXE`). This arc makes a working, **PowerShell-callable** `bw` a deterministic outcome of standing a
machine up, via one idempotent OS-split helper (`substrate/bootstrap-bw.sh`) wired into two in-repo
consumers: an opt-in `install.sh --bootstrap-bw` pre-flight (DC6) and a guided, consented reversal of
the onboarding skill's Beat 1 (DC7). Unix obtention delegates to upstream's installer; Windows
obtention is ours end-to-end (download + SHA256-verify + extract + registry-safe PATH append). The
Windows USER PATH mutation is the design crux — registry-safe, fail-loud, ARGUS-cold-audited.

**Assumptions imported into this restatement (named per §6.1):**
- The dedicated dir is `~/.local/bin` (CONFIRMED — DC2), unifying the Unix install dir, upstream's
  preferred no-sudo dir, and (on the reference machine) the dir ALREADY first on the Windows USER
  PATH — so the idempotent-skip is the reference-machine path.
- The third consumer (u--9s2 cookie-cutter) has NO in-repo call-site this arc; the helper is built
  `--yes`-ready for it, but its wiring lands in u--9s2 (DC8 scope guard).
- "Byte-unchanged when the flag is absent" (DC6) means: the `--dry-run` OUTPUT of the built
  `install.sh` invoked WITHOUT `--bootstrap-bw` is byte-identical to the pre-arc `install.sh`
  `--dry-run` output. The `--help` output DOES change (the flag is documented there); the header
  edit does not reach the dry-run output path.
- **Target Windows runtime is Git-for-Windows on Win10/11** (the substrate's only Windows runtime).
  The composed-PATH ceiling (F3) is the Win10/11 4095-char limit, not the legacy pre-Win10 2047.

---

## Ground-truth re-confirmation (this session, worktree HEAD + upstream + LIVE registry probes)

**Upstream (jallum/beadwork, PUBLIC):** unchanged from rev1's read — `releases/latest` = `v0.13.2`
(== floor `>=0.13.2`); assets `beadwork_0.13.2_windows_{amd64,arm64}.zip`, four `*.tar.gz`,
`beadwork_0.13.2_checksums.txt` (two-space `<sha256>␠␠<file>`); upstream `install.sh` still
UNIX-ONLY / latest-only / no-checksum / no-PATH-setup, honors `INSTALL_DIR`. No premise drift.

**Worktree HEAD (`stoa--elx/build`) — anchors re-confirmed this session (rev3 re-ground-checked):**
- `substrate/install.sh` = 2120 lines. `SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"`
  at **L155**. Arg-parse `while [ "$#" -gt 0 ]` L654 → `done` **L749**; `-h|--help)` arm **L742**.
  Validation section opens **L751**; `[ -n "$TARGET" ] || err "--target is required..."` at **L753**;
  **`case "$TARGET" in` at L761**; `scaffold_user_tier` defined L444, CALLED **L777** (this is where
  `bw init` fires). Flag DEFAULTS block L146-152. Header L3-135; `usage()` L272 renders the L3-135
  block via `sed`. (rev3 N4 uses the L753→L761 window; all four anchors re-confirmed this session.)
- `skills/install-stoa/SKILL.md` = 251 lines, repo ROOT (stoa--sok). Beat 1 L37-51; "must NOT" list
  L233-242; reversal targets L237/L238; PRESERVE targets L235/L240 (dry-run) + L241 (bw-init
  separation). (DC7 unchanged from rev1 — ARGUS discharged it.)

**LIVE registry ground-truth (read-only `[Microsoft.Win32.Registry]`, this session):**
- Real `HKCU\Environment` `Path`: **KIND=`REG_SZ` (String)**, raw length **800**, first entry
  **`C:\Users\denso\.local\bin`**, **no `%token%`** currently. (Matches ARGUS: real machine is
  REG_SZ, and `.local\bin` is already first → idempotent-skip is the reference path.)
- Machine `Path` length **1318**; User `Path` length **800**; **composed-expanded length = 2119.**
  This is the load-bearing F3 datum: **2119 > 2047, yet this machine works** — proving a 2047
  hard-gate would FALSE-FAIL a healthy machine (see F3).

---

## DC1 — helper shape + deliverables (rev3 N1-A: `win_path.ps1` is a committed sibling)

`substrate/bootstrap-bw.sh` is the idempotent OS-split helper (`--yes` / `--check` / `--dry-run`). On
Windows it obtains `bw.exe` (DC5) and ensures its dir is on the registry User PATH by invoking the
**committed sibling** `substrate/win_path.ps1` via `-File` (DC2). The helper resolves its own directory
robustly and locates the sibling script relative to itself:

```sh
HELPER_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"   # substrate/ when run in-place
WIN_PATH_PS1="${HELPER_DIR}/win_path.ps1"
[ -f "$WIN_PATH_PS1" ] || fail_loud_path "win_path.ps1 not found alongside bootstrap-bw.sh at $WIN_PATH_PS1"
```

**Why a committed file (N1 option A) over an emitted quoted heredoc (option B) — JUSTIFIED:**
1. **It removes the emission-integrity risk class entirely.** Option B (a quoted `<<'WIN_PATH_PS1'`
   heredoc) works only if ADA writes the delimiter with the quotes intact on BOTH the opening and the
   guard is exact; a single dropped quote silently re-opens the whole `$`/`$()`-expansion corruption
   class N1 names. Option A has **no emission step to get wrong** — the shipped bytes ARE the authored
   bytes, guaranteed by git, not by a build-time heredoc.
2. **The `.ps1` is the security crux** (the registry read/parse/write is the highest-risk code in the
   arc). A standalone, committed, directly-diffable file is the right home for it: ARGUS/CATO/VERA and a
   human reviewer audit it as a file, it carries its own git history, and its diffs are clean — versus
   being buried inside a bash heredoc where a reviewer reads it through two layers of quoting.
3. **The P2 probe drives the SHIPPED artifact directly** (`-File "${HELPER_DIR}/win_path.ps1"`),
   satisfying ARGUS's N1 pin — the emission/shipping path itself is under test — with the least
   indirection: the file VERA drives IS the file that ships. (Option B would force VERA to first emit
   the temp `.ps1` via the helper, then drive that, testing a copy at one remove.)
4. **Cost is one added deliverable file**, and it is an *extraction* of already-designed §DC2 code into
   its own file, not new scope. "One coherent slice" is preserved (helper + its sibling `.ps1` +
   install.sh flag + skill).

**The bounded downside, named honestly (see weak point 8):** `-File "${HELPER_DIR}/win_path.ps1"` now
depends on the sibling being co-located with the helper. If a future consumer copies `bootstrap-bw.sh`
WITHOUT its sibling, the invocation fails — but it **fails LOUD** (the `[ -f ]` guard above → `err`, or
powershell's own `-File not found` → non-zero → `fail_loud_path`), never a silent corruption. In this
arc both consumers (DC6 install.sh, DC7 skill) invoke the helper in-place from `substrate/`, so the
sibling always resolves.

---

## DC2.0 — F1 MECHANISM DECISION + EMPIRICAL git-bash ROUND-TRIP PROOF (the load-bearing rev2 core, CLOSED)

### The mechanism: PowerShell .NET registry API via a `-File` script (NOT `reg.exe`) — CLOSED by ARGUS RE-AUDIT

ARGUS F1 proved (read-only) that `reg query/reg add` from git-bash are MSYS-mangled: git-bash's MSYS
layer rewrites the `/v /t /d /f` switches (they look like POSIX absolute paths) before `reg.exe` sees
them, so `reg query "HKCU\Environment" /v Path` → `ERROR: Invalid syntax`. rev1's entire DC2
read/write was therefore **dead code**. Three candidate fixes: (a) an MSYS-exclusion prefix
(`MSYS_NO_PATHCONV=1` / `MSYS2_ARG_CONV_EXCL='*'`); (b) `cmd //c reg ...`; (c) the PowerShell .NET
registry API.

**I choose (c), PowerShell `[Microsoft.Win32.Registry]`, and JUSTIFY it over (a)/(b):**
- **(a)/(b) keep `reg.exe`**, which forces me to PARSE `reg query`'s human-formatted, **CRLF-laden**
  output in bash (F4: stray `\r` corrupts the adjacent PATH entry) and to reconstruct the value with
  `sed`/`grep` (fragile against locale/format variance — the same class of failure that produced F2's
  read-failed-vs-absent conflation). The exclusion prefix only un-breaks the invocation; the parsing
  fragility remains.
- **(c) has no switches to mangle** (no `/v /t /d`), returns the **raw value as a typed .NET string**
  (no CRLF, no reg-format parsing → **F4 dissolves**), reads the value **unexpanded** via
  `RegistryValueOptions::DoNotExpandEnvironmentNames` (so `%token%` entries are preserved, not frozen),
  reads the exact type via `GetValueKind()` and writes it back with `SetValue(...,$kind)` (no
  REG_EXPAND_SZ→REG_SZ downgrade), and distinguishes **absent** (`GetValue` → `$null`) from **read
  failure** (exception → non-zero exit) **structurally → F2 resolves**. It is also the exact surface
  DC3 check (b) already uses (`[System.Environment]`), so the crux uses one coherent toolchain.

**Invocation contract (rev3 N1-A — the helper invokes the COMMITTED sibling, does not emit, does not
depend on `reg.exe` at all):** the helper runs the shipped `substrate/win_path.ps1` via:
```
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$(cygpath -w "${HELPER_DIR}/win_path.ps1")" \
   -Dir "$dir_win" -KeyName "Environment" [-DryRun] -Ceiling 4095
```
The `-File` form (not `-Command`) means the script text is never an argv token git-bash can mangle;
the only args are `-Dir` (a native `C:\...\.local\bin`, **empirically passes through git-bash with
backslashes intact** — proven below), `-KeyName` (default `Environment`; **probes override to the
THROWAWAY `Environment_stoa_test`** — this is the test seam that lets VERA drive the EXACT real code
path without touching the real key), `-DryRun`, `-Ceiling`. **rev3 N1 change: `win_path.ps1` is a
committed file (`${HELPER_DIR}/win_path.ps1`), NOT a heredoc-emitted temp — so the shipped bytes are
the authored bytes by construction and there is no bash-interpolation surface to corrupt the PS sigils.**

### EMPIRICAL PROOF — the actual commands I ran (git-bash), and their output (CLOSED — ARGUS independently reproduced)

**(a) READ the real `HKCU\Environment` Path READ-ONLY** — `OpenSubKey('Environment',$false)` +
`GetValue('Path',$null,DoNotExpandEnvironmentNames)` + `GetValueKind`:
```
KIND=String   LEN=800   FIRST_ENTRY=C:\Users\denso\.local\bin   HAS_PERCENT_TOKEN=False
```
→ real key read intact, read-only, no mutation. (KIND=String confirms REG_SZ; type-preservation
writes String back → no downgrade.)

**(b) WRITE-preserving-type to the THROWAWAY key and read it back intact** — created
`HKCU\Environment_stoa_test`, seeded it `REG_EXPAND_SZ` with a `%USERPROFILE%\.local\bin;...` value
(the type-preservation HARD case — the real machine is REG_SZ, so I deliberately exercised the
harder ExpandString+token case), then ran the real design logic against it:
```
C1_KIND=ExpandString   C1_TOKEN_PRESERVED=True                       # read back RAW, kind + %token% intact
C2_AFTER_KIND=ExpandString   C2_TOKEN_STILL_THERE=True   C2_APPENDED_ONCE=1   # append preserves kind, token, exactly once
C3_PRESENT_ON_RERUN=True                                              # idempotent re-run detects present → no-op
```
Then the full parameterized `-File` script (the exact structure I spec below) against the throwaway:
```
=== real append ===   COMPOSED_LEN=1383 CEILING=4095   RESULT=appended kind=ExpandString value=...;C:\Users\denso\.local\bin   exit=0
=== dry-run ===       COMPOSED_LEN=1383 CEILING=4095   RESULT=would_append kind=ExpandString                                  exit=0
=== length fail ===   COMPOSED_LEN=1383 CEILING=10     RESULT=fail_length                                                     exit=4   (NO write)
=== idempotent ===    RESULT=present                                                                                          exit=0   (NO write)
```
`-Dir` arg survived git-bash intact: `ARG_DIR_RECEIVED=C:\Users\denso\.local\bin` (backslashes
preserved). Exit codes propagate to bash (`exit=$?`).

**(c) THROWAWAY TEARDOWN** — `DeleteSubKeyTree('Environment_stoa_test', ...)` in a **`finally` block**
(teardown ALWAYS runs, even on mid-script exception — a lesson from a test-diagnostic that threw
before an early teardown and left the key on disk; I cleaned it immediately and re-confirmed):
```
GONE=True                         # throwaway key deleted
REAL_KIND=String  REAL_LEN=800  REAL_FIRST=C:\Users\denso\.local\bin   # real key IDENTICAL to pre-test read → untouched
```

**Round-trip conclusion:** the mechanism reads the real key read-only, writes-preserving-type to a
throwaway key and reads it back intact (kind + `%token%`), gates on composed length, is idempotent,
dry-runs without writing, and tears the throwaway down unconditionally — all from git-bash, with the
real `HKCU\Environment` Path provably unchanged. rev1's dead-code invocation is replaced by a proven
one. **ADA builds against this exact structure, shipped as `substrate/win_path.ps1`.**

---

## DC2 — Windows USER PATH mutation (the crux; DAEDALUS-owned; CLOSED, carried verbatim in intent)

### Dir choice — CONFIRMED `~/.local/bin` (unchanged from rev1; discharged)
git-bash form `$HOME/.local/bin`; Windows-native form via `cygpath -w "$HOME/.local/bin"` →
`C:\Users\<name>\.local\bin` (fallback `"${USERPROFILE}\.local\bin"` if `cygpath` absent). Rejected
`~/bin` and `~/.stoa/bin` (non-unifying). On the reference box `.local\bin` is already first on the
User PATH → idempotent no-op.

### The registry-safe mutation — `win_path.ps1` (COMMITTED sibling; the mechanism proven in DC2.0)

**NEVER `setx`** (web-confirmed, do-not-relitigate: truncates >1024; expands `%PATH%` merging
system→user; downgrades REG_EXPAND_SZ→REG_SZ). The helper's `win_ensure_on_path "$dir_win"` builds
`dir_win` via `cygpath -w` and invokes the committed `win_path.ps1` per the DC2.0 contract. **This is
the exact body ADA commits as `substrate/win_path.ps1`** (validated end-to-end in DC2.0):

```powershell
param([Parameter(Mandatory=$true)][string]$Dir, [string]$KeyName='Environment',
      [int]$Ceiling=4095, [switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = [Microsoft.Win32.Registry]::CurrentUser
try {
  # 1. OPEN the key. Key ABSENT is a READ FAILURE, NOT "empty PATH" (F2).
  $wk = $root.OpenSubKey($KeyName, $true)
  if ($null -eq $wk) { Write-Output 'RESULT=fail_read'; exit 3 }              # FAIL LOUD, no write
  # 2. READ raw (UNEXPANDED) value + kind. $null value = PROVABLY absent (fresh Path) → legit empty.
  $cur = $wk.GetValue('Path', $null, [Microsoft.Win32.RegistryValueOptions]::DoNotExpandEnvironmentNames)
  if ($null -eq $cur) { $cur=''; $kind=[Microsoft.Win32.RegistryValueKind]::ExpandString }
  else { $kind = $wk.GetValueKind('Path') }                                   # PRESERVE original type
  # 3. IDEMPOTENT-ABSENT check — per-entry, case-insensitive, trailing-\ tolerant, AND token-expanded
  #    (F8: a REG_EXPAND_SZ entry stored as %USERPROFILE%\.local\bin must match the expanded $Dir).
  $dExp = [System.Environment]::ExpandEnvironmentVariables($Dir).TrimEnd('\')
  $present = $false
  foreach ($e in ($cur -split ';')) {
    if ($e.Trim() -eq '') { continue }
    $eRaw = $e.Trim().TrimEnd('\')
    $eExp = [System.Environment]::ExpandEnvironmentVariables($e.Trim()).TrimEnd('\')
    if (($eRaw -ieq $Dir.TrimEnd('\')) -or ($eExp -ieq $dExp)) { $present = $true }
  }
  if ($present) { $wk.Close(); Write-Output 'RESULT=present'; exit 0 }        # idempotent no-op
  # 4. BUILD new user value (our segment is a LITERAL absolute path — safe under either kind).
  $newUser = if ($cur -eq '') { $Dir } else { $cur.TrimEnd(';') + ';' + $Dir }
  # 5. COMPOSED length gate (F3): Machine + ";" + newUser, EXPANDED, vs the Win10/11 4095 cliff.
  $m = [System.Environment]::GetEnvironmentVariable('Path','Machine'); if ($null -eq $m) { $m='' }
  $composed = [System.Environment]::ExpandEnvironmentVariables("$m;$newUser")
  if ($composed.Length -gt $Ceiling) { $wk.Close(); Write-Output "RESULT=fail_length composed=$($composed.Length)"; exit 4 }
  # 6. WRITE preserving kind (or report in dry-run). reg-add-class semantics; no %PATH% expansion.
  if ($DryRun) { $wk.Close(); Write-Output "RESULT=would_append kind=$kind"; exit 0 }
  $wk.SetValue('Path', $newUser, $kind)
  $wk.Close()
  Write-Output 'RESULT=appended'; exit 0
} catch { Write-Output "RESULT=fail_exception $($_.Exception.Message)"; exit 5 }
finally { if ($null -ne $wk) { $wk.Close() } }
```

### The bash wrapper `win_ensure_on_path` — rev3 N2: exit-code capture PINNED

rev2 gave the exit→action map as a prose table but did not write the bash wrapper. **F2 is already
closed regardless — the ONLY writer is `win_path.ps1`, so a bash mis-map cannot clobber; the worst case
is a less-precise fail-loud message, itself backstopped by DC3 check (b).** rev3 pins the wrapper so
ADA builds the exit-code capture exactly. The load-bearing rule: **capture `rc=$?` on the very next
line after the `powershell.exe` call — NO pipe (`| tee`/`| grep`) between the call and `rc=$?` (a
pipeline makes `$?` the last stage's exit), NO `|| true` swallowing it.**

```sh
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
```

The PS-exit→action map the wrapper implements (unchanged from rev2; now bound to the wrapper above):

| PS exit | RESULT | Helper action |
|---|---|---|
| 0 | `present` | idempotent no-op; proceed to DC3 verify |
| 0 | `appended` / `would_append` | success (or dry-run); proceed to DC3 verify |
| 3 | `fail_read` (key absent) | **`fail_loud_path` — NO write happened; never overwrite** (F2) |
| 4 | `fail_length` | **`fail_loud_path` — composed > ceiling; NO write** (F3/M4) |
| 5 | `fail_exception` | **`fail_loud_path` — any error; NO write** (F2/M4) |

Key audit points:
- **F1 resolved:** no `reg.exe`, no `/v /t /d /f` switches, no MSYS mangling. Proven round-trip DC2.0.
- **F2 resolved:** a failed/ambiguous read is `fail_read`/`fail_exception` (distinct non-zero exit +
  no write); ONLY a *provably-absent value* (`$null` from a successfully-opened key) yields `cur=''`
  and a legitimate fresh single-entry Path. The rev1 "any-nonzero-exit → cur='' → overwrite whole
  USER PATH" clobber is structurally impossible. **rev3 N2:** the bash wrapper captures `rc=$?` with no
  `|| true` and routes 3/4/5 → `fail_loud_path`, 0 → proceed — so the bash side cannot even mis-report,
  let alone clobber.
- **F3 resolved:** the gate measures the **EXPANDED composed** `Machine + ";" + newUser` against
  **4095** (the web-confirmed Win10/11 login-truncation cliff; §F3 below), not user-only vs 2047.
- **F4 dissolved:** no bash-side parsing of `reg query` output → no stray `\r`.
- **F8 resolved:** the idempotent check compares BOTH the raw entry AND its token-expanded form
  against the expanded `$Dir`, per `;`-delimited entry with trailing-`\` tolerance — so a
  `%USERPROFILE%\.local\bin`-token entry matches the expanded `C:\Users\<name>\.local\bin` and we do
  NOT double-append.
- **Type preservation:** read `GetValueKind` → write same kind. Real machine is REG_SZ → writes
  REG_SZ (no downgrade); a REG_EXPAND_SZ machine keeps ExpandString (proven C1/C2 in DC2.0).

### Fail-loud branch (`fail_loud_path`) — unchanged intent from rev1
Fires on `fail_read` / `fail_length` / `fail_exception` (or, interactive, declined consent). Prints a
non-zero-exit, one-shot manual step and does NOT write. Points at the **GUI editor** ("Edit
environment variables for your account" → User `Path` → New → paste `C:\Users\<name>\.local\bin`),
NOT a PowerShell `SetEnvironmentVariable` one-liner (which writes REG_SZ, re-introducing a token-freeze
risk in the very fallback meant to be safe). **F3-honest caveat (record in the message):** the GUI
`sysdm.cpl`/account editor caps single-variable INPUT at 2047 chars and truncates a USER `Path`
already >2047 to 4095 on save; on the target machine the USER Path is 800 chars (well under 2047), so
the GUI step is safe here, but the message notes the >2047-user-Path corner honestly.

### Shim fallback (`bw.cmd`) — LAST resort only (unchanged from rev1; discharged)
Only when the registry append cannot be done safely AND some OTHER dir is ALREADY on the User PATH:
drop a `bw.cmd` forwarder there. Fallback, never default.

---

## F3 — composed-PATH length gate (web-verified; the 2047→4095 correction; CLOSED, ARGUS web-confirmed exact)

**Web-confirmed (current Win10/11 semantics, this session):** at login Windows composes
`ComposedPATH = SystemPATH + ";" + UserPATH` (the only auto-merged variable). The **legacy 2047**
figure is the `sysdm.cpl` GUI *input* cap, NOT the runtime cliff. The modern Win10/11 runtime buffer
limit for a single environment variable in the active block is **4095 chars**; if the composed PATH
exceeds 4095, the session manager **silently truncates the composed value at 4095, and because System
PATH is laid down first, the truncation lands in the USER portion** (partial/dropped user entries, no
warning).

**Why user-only-vs-2047 (rev1) was wrong — empirical:** this machine's **composed-expanded PATH is
already 2119** (Machine 1318 + User 800 + expansion), and it works. A 2047 hard-gate would FALSE-FAIL
a healthy machine; a user-only gate (800 < 2047) would MISS that composed is already 2119. Both rev1
readings were wrong in opposite directions.

**The fix (in `win_path.ps1` step 5):** read Machine PATH (`GetEnvironmentVariable('Path','Machine')`),
compose `Machine + ";" + newUser`, **expand** it, and gate the **expanded composed length** against
**`-Ceiling 4095`** (the real cliff). Our appended segment is a literal (same raw and expanded
length). On this machine, appending `.local\bin` would put composed at ~2144 << 4095 → safe (though
it idempotent-skips anyway, `.local\bin` already being present). The gate FAILS LOUD (exit 4, no
write) only when a genuine append would breach 4095 — the true truncation risk. (Note: `reg add`-class
writes themselves don't truncate below cmd's ~8191; the gap F3 closes is purely the *login-merge*
4095 cliff, which our write feeds.)

---

## DC3 — two-independent-checks (mandatory; the false-green killer) + F5 probe hardening (CLOSED)

Two checks, run SEPARATELY; (b) runs EVEN WHEN (a) passes:

- **(a) binary present** (git-bash side): `[ -x "$dir_posix/bw.exe" ]` (or `command -v bw` from
  git-bash). This is the check that FALSE-GREENS alone.
- **(b) PowerShell-callable** (durable check): a PowerShell probe that **reconstructs User + Machine
  PATH from the registry** and resolves `bw` against it — what a FRESH login shell composes.
  **Load-bearing detail (F5):** the probe must **REASSIGN** `$env:PATH` from registry-only values, so
  git-bash's inherited env block (which a child `powershell.exe` DOES inherit — empirically confirmed
  this session: a child powershell sees a dir exported only in git-bash's PATH) cannot leak in:
```powershell
$u = [System.Environment]::GetEnvironmentVariable('Path','User')
$m = [System.Environment]::GetEnvironmentVariable('Path','Machine')
$env:PATH = [System.Environment]::ExpandEnvironmentVariables("$m;$u")   # REASSIGN, not append
$c = Get-Command bw -ErrorAction SilentlyContinue
if ($c) { Write-Output ("PS-CALLABLE " + $c.Source); exit 0 } else { exit 1 }
```
If `bw.exe` is in `~/.local/bin` but that dir is NOT on the registry User PATH, this probe EXITS 1 —
the exact false-green this machine exhibited — even though git-bash `bw --version` succeeds.

- **Idempotent-skip requires BOTH (a) AND (b).** (a)-pass / (b)-fail does NOT skip; it proceeds to
  `win_ensure_on_path`, then re-runs (b), which must pass, else fail-loud.
- **Unix** has no PowerShell surface: single `bw --version` with `~/.local/bin` on PATH suffices.

**F5 — the P4 fixture must reproduce the git-bash-green / registry-blind ASYMMETRY.** ARGUS's F5: if
the stub dir is ALSO off git-bash's own PATH, a naive `powershell -c "bw --version"` would ALSO exit 1
and P4 would false-pass against the wrong implementation. **Fix — P4's fixture (empirically grounded;
rev3 N3 pins the POSIX-form export):** place a stub `bw.exe` in a throwaway dir created via
`mktemp -d` (which yields a **POSIX `/c/...` path**), **`export PATH="<posix-stub>:$PATH"` in the
git-bash session (so it IS on git-bash's inherited env)** WHILE that dir is **absent from the registry
User PATH** (never written). The POSIX form is load-bearing: a Windows-form export (`C:/...` or
`C:\...`) is mangled by git-bash's POSIX→Win translation, so a naive powershell would NOT resolve the
stub either → both naive and correct exit 1 → **P4 would false-PASS** and re-open the F5 blind spot at
the test layer. With the POSIX-form export:
- a **naive** `powershell.exe -Command "bw --version"` INHERITS git-bash's PATH → resolves the stub →
  exit 0 (**false-green** — this is what P4 must catch);
- the **correct** check (b), which REASSIGNS `$env:PATH` from registry-only, does NOT see the stub →
  `Get-Command bw` fails → **exit 1**.
P4 asserts the naive form exits 0 FIRST (proving the false-green is live), THEN asserts the correct
check exits 1; a build that implemented the naive form would exit 0 and FAIL P4. This makes P4
discriminate the real implementation from the false-green look-alike. (Confirmed this session that a
child `powershell.exe` inherits a git-bash-exported PATH entry — the asymmetry the fixture relies on is
real.)

---

## DC4 — Unix obtention (delegate to upstream; unchanged from rev1; ARGUS-discharged)

```sh
unix_obtain() {
  mkdir -p "$HOME/.local/bin"
  ensure_shell_rc_path "$HOME/.local/bin"      # idempotent marker-guarded shell-rc append
  [ "$HAVE_BINARY" = 1 ] && { log "bw >= $FLOOR present — skipping upstream install"; return 0; }
  curl -fsSL https://raw.githubusercontent.com/jallum/beadwork/main/install.sh \
    | INSTALL_DIR="$HOME/.local/bin" sh          # pin INSTALL_DIR so upstream honors it (its L11-13)
}
```
Floor-via-latest; idempotent skip if `>= FLOOR`. **Checksum ASYMMETRY (Grand-accepted §4a)** stated
as a recorded helper comment: Unix inherits upstream's HTTPS-only/no-checksum posture (forcing SHA256
parity means wrapping/replacing upstream, which the OS-split directive forbids); Windows (ours
end-to-end) is STRICTER. No `tar -xzf` reimplementation on the Unix branch (VERA P6).

## DC5 — Windows obtention (ours end-to-end; SHA256 fail-closed; unchanged from rev1; ARGUS-discharged)

Download `beadwork_${ver}_windows_${ARCH}.zip` + `beadwork_${ver}_checksums.txt` (both HTTPS),
SHA256-verify FAIL-CLOSED (no extraction on mismatch; `rm -rf "$tmp"` on any failure), extract only
`bw.exe` via `Expand-Archive`, place in `~/.local/bin`, then `win_ensure_on_path`. Cross-platform hash:
`sha256sum` else `Get-FileHash`; both normalized lowercase. checksums.txt parse: `grep -F "$base.zip"`
→ `awk '{print $1}'` (amd64 not a substring of arm64; multi-match fails closed). (Full body as rev1
§DC5 — unchanged.)

## DC6 — `install.sh` opt-in `--bootstrap-bw` (default OFF; absent = byte-unchanged) + F6/F7 fold-in + rev3 N4

Four minimal edits (rev1 (1)/(2)/(4) unchanged; (3) MOVED per F6 **and re-pinned per rev3 N4**;
invocation form changed per F7):

**(1) Default** — add after L152 in the L146-152 defaults block:
`BOOTSTRAP_BW=0   # Arc 75: opt-in bw bootstrap pre-flight; DEFAULT OFF → byte-unchanged when absent`

**(2) Case arm** — insert before `-h|--help)` at L742 (shipped multi-line style):
```sh
    --bootstrap-bw)
      BOOTSTRAP_BW=1
      shift
      ;;
```

**(3) Pre-flight invocation — MOVED per F6, PLACEMENT PINNED TARGET-INDEPENDENT per rev3 N4.** rev1
placed this after the parse-loop `done` (L749), i.e. BEFORE the target-required check at L753 — so
`install.sh --bootstrap-bw` with a missing/invalid `--target` would run a real download + PATH mutation
*before* erroring on the missing target. rev2's F6 fix placed it "after L753, before scaffold L777" —
correct on ordering but **satisfiable INSIDE the `user)` arm**, which would NOT run the pre-flight for
`--target project|subproject`, contradicting the design's own "target-independent" rationale. **rev3 N4
fix: place the guarded block AFTER `[ -n "$TARGET" ] || err "--target is required..."` (L753) and
BEFORE `case "$TARGET" in` (L761)** — in the L754-760 window, ahead of the `case` dispatch. This makes
the pre-flight:
- **target-independent** — it runs for `user`, `project`, AND `subproject` (it is above the `case`);
- **error-first on a missing `--target`** — L753 still runs before it, so a missing target errors with
  no download/mutation;
- **before `bw init`** — L777 (`scaffold_user_tier` → `bw init`) is inside the `user)` arm, downstream
  of the `case`, so bw is made available before `bw init` fires on the user path.
`SCRIPT_DIR` (L155) is in scope at L754+.
```sh
# ----- Arc 75 (stoa--elx): optional bw bootstrap pre-flight (after --target validation,
#        before the case dispatch — target-independent: runs for user|project|subproject) -----
if [ "$BOOTSTRAP_BW" -eq 1 ]; then
  _bootstrap="${SCRIPT_DIR}/bootstrap-bw.sh"
  [ -f "$_bootstrap" ] || err "--bootstrap-bw: helper not found at $_bootstrap"
  if [ "$DRY_RUN" -eq 1 ]; then bash "$_bootstrap" --dry-run; else bash "$_bootstrap" --yes; fi
fi
```
**F7 fold-in:** invoke via `bash "$_bootstrap"` (NOT `"$_bootstrap"` as an executable) — robust
regardless of whether the `+x` bit survived Windows checkout; the guard is `[ -f ]` not `[ -x ]`.

**(4) `--help` / usage** — extend the L26-28 Usage lines to include `[--bootstrap-bw]` alongside
`[--enable-hooks]`. Changes `--help` (intended) but NOT the `--dry-run` output path.

**Why absent-flag output is byte-unchanged — re-confirmed at the rev3 N4 placement:** `BOOTSTRAP_BW=0`
⇒ the pre-flight `if` is false (emits nothing), the case arm is never taken, NO plan-section line is
added. The block's placement (after L753, before `case` at L761) is still inside a **false `if` when
the flag is absent — the byte-unchanged property is placement-independent** (a false `if` emits nothing
wherever it sits; ARGUS confirmed the property holds regardless of placement). Moving the block from
inside the `user)` arm to above the `case` does NOT change any emitted byte on the absent-flag path.
VERA P7.

## DC7 — onboarding skill canon reversal (`skills/install-stoa/SKILL.md`; unchanged from rev1; ARGUS-discharged)

Beat 1 (L37-51): "STOP, bw is a prereq" → "detect; if missing, drive the guided consented bootstrap"
(show release source + Windows SHA256 + the registry-safe PATH append; `--dry-run` FIRST; consent;
then real; decline → fall back to prereq-pause). "Must NOT" edits: L237/L238 REVERSE (bootstrap now
in scope via consented helper); **L241 PRESERVE UNCHANGED** (bw-INIT separation — a DIFFERENT concern);
L235/L240 PRESERVE (dry-run); L239 NUANCE (carve out the consented, helper-mediated, registry-safe,
fail-loud PATH append; keep "no unrelated system-file changes"). Reversal justification recorded in
the skill. (Full body as rev1 §DC7 — unchanged.)

---

## DC8 — honest stance + scope guard + threat posture (F9 fold-in tightens M1)

**Honest stance.** Real, bounded trust surface: the helper DOWNLOADS an executable, PLACES it on
PATH, MUTATES the Windows USER PATH. Named mitigations: Windows SHA256-verify (fail-closed) +
HTTPS/TLS on every fetch + upstream's canonical TLS path on Unix + registry-safe append + fail-loud.
**No over-claim of "fully sandboxed."** Checksum asymmetry STATED (helper comment + DC4).

**Scope guard (unchanged).** Helper + `win_path.ps1` sibling + TWO in-repo consumers (DC6, DC7) ONLY;
the u--9s2 cookie-cutter call-site lands in u--9s2 (`--yes`-ready here). arc-19 "do not install bw"
superseded-in-spirit, NOT edited. `bw upgrade`/`bw-upgrade.md` untouched (helper bootstraps the FIRST
binary only).

### Threat→mitigation map (A3; §6.12 — named-threat-ratified via the Grand's hard conditions + directive DC8)

`M1 (supply-chain download tamper) → attacker tampers the fetched zip in transit or serves a corrupted
/ cache-poisoned object → DEFEATED-BY: HTTPS/TLS authenticates origin + integrity in transit (this is
what actually stops a network MITM); Windows SHA256-verify against upstream checksums.txt FAIL-CLOSED
(no extraction on mismatch) catches CORRUPTION and a SINGLE-OBJECT cache-poison/substitution where
the zip is swapped but checksums.txt is not. **F9-honest residual (tightened): SHA256's marginal
value over TLS is corruption + single-object tamper detection — NOT MITM (TLS owns that) and NOT a
full origin compromise (a GitHub-release/account compromise, or a channel tamper that swaps BOTH the
zip AND same-origin checksums.txt, defeats the hash — bounded by GitHub release security).** Unix
inherits upstream's HTTPS-only posture (recorded asymmetry §4a).`

`M2 (Windows USER PATH clobber/truncation) → a naive setx truncates PATH >1024, or expands %PATH%
merging system into user, or downgrades REG_EXPAND_SZ→REG_SZ freezing %-tokens; OR (rev1's own bug) a
failed read is mistaken for empty and the whole USER PATH is overwritten with one entry → user loses
PATH entries → DEFEATED-BY: PowerShell .NET-registry read (unexpanded, typed) → provably-absent-vs-
read-failure discrimination (fail_read/fail_exception FAIL LOUD, never overwrite) → token-aware
idempotent-absent check → EXPANDED-COMPOSED length gate ≤4095 → SetValue preserving original kind;
never setx; never %PATH% expansion. rev3 N2: the bash wrapper captures rc immediately (no || true) and
routes 3/4/5 → fail_loud — the bash side cannot mis-report a failure as a write.`

`M3 (PowerShell-blind false-green) → verify runs a git-bash-only bw --version that succeeds while the
registry User PATH still lacks the dir → install reports success but PowerShell substrate flows fail
silently → DEFEATED-BY: two-independent-checks; check (b) REASSIGNS $env:PATH from the REGISTRY
User+Machine values and resolves bw, runs EVEN WHEN (a) passes; idempotent skip requires BOTH.`

`M4 (fail-loud-not-firing) → an unsafe PATH condition (composed>ceiling / read failure / write error /
declined consent) silently proceeds or no-ops, leaving PATH clobbered or bw uncallable behind a green
result → DEFEATED-BY: explicit fail_loud_path on PS exit 3/4/5 — non-zero exit + exact GUI manual step
+ NO write; --yes (u--9s2) mode fails loud rather than hanging.`

**threat_coverage (defeats_via_probe — §6.13 threat-anchored):**
- `M1 → defeats_via_probe: P5 (SHA256 fail-closed on corrupted/mismatched zip; correct zip verifies)`
- `M2 → defeats_via_probe: P2 (registry-safe append + provably-absent-vs-read-failure + token-idempotent, THROWAWAY key, driving the SHIPPED win_path.ps1) + P3 (composed-length fail-loud, no write)`
- `M3 → defeats_via_probe: P4 (git-bash-green / registry-blind false-green demonstrably caught — F5 fixture, POSIX-form stub export)`
- `M4 → defeats_via_probe: P3 (composed>ceiling throwaway → fail_loud, non-zero, no write) + P2b (fail_read → no overwrite)`

---

## Verification probes (§3 — concrete, VERA-re-executable; threat-anchored per §6.13)

All Windows-mutation probes use `-KeyName Environment_stoa_test` (THROWAWAY, `finally`-torn-down) or a
pure-string fixture — NEVER this machine's real `HKCU\Environment` Path. **Teardown is in a `finally`
block so it runs even on a mid-script exception** (lesson from this session). **rev3 N1: the Windows PS
probes drive the SHIPPED `substrate/win_path.ps1` (the committed artifact ADA produces), via
`-File "${HELPER_DIR}/win_path.ps1"` — so the emission/shipping path itself is under test, not a
hand-authored copy.**

- **P1 — idempotent skip on THIS machine (M2/M3 legit-unaffected).** `bootstrap-bw.sh --check` then
  `--dry-run`: bw detected `>= 0.13.2`, DOWNLOAD skipped, `win_ensure_on_path` returns `RESULT=present`
  (dir already first on the real User PATH — read-only), DC3 (a)+(b) both PASS, ZERO mutation.
- **P2 — registry-safe append, THROWAWAY, driving the SHIPPED win_path.ps1 (M2 attack-blocked +
  legit-unaffected).** Invoke `-File "${HELPER_DIR}/win_path.ps1" -KeyName Environment_stoa_test` (the
  EXACT shipped code path): (a) absent-dir seed → appended exactly once, `RESULT=appended`; (b)
  present-dir seed → `RESULT=present`, no write; (c) REG_EXPAND_SZ seed with `%USERPROFILE%`-token →
  kind + token PRESERVED (read-back RAW equals seed + our literal); (d) token-form-stored entry
  (`%USERPROFILE%\.local\bin`) with expanded `-Dir` → detected present, NO double-append (F8); (e)
  **P2b:** seed the key ABSENT / force a read failure → `RESULT=fail_read` exit 3, NO write (F2 — never
  overwrite); (f) grep the helper + `win_path.ps1`: NO `setx`, NO `%PATH%` expansion, NO
  `reg add`/`reg query`. `finally` teardown; real key untouched.
- **P3 — composed-length fail-loud (M2 + M4).** `-File "${HELPER_DIR}/win_path.ps1" -KeyName
  Environment_stoa_test -Ceiling <small>` (or a seed whose composed-expanded > 4095) → `RESULT=fail_length`
  exit 4, `fail_loud_path` prints the exact GUI manual step, NO write (throwaway value unchanged).
  Legit half: a normal append under 4095 writes.
- **P4 — DC3 false-green demonstrably CAUGHT (M3; F5 fixture; rev3 N3 POSIX export).** Create a
  throwaway dir via `stub="$(mktemp -d)"` (yields a **POSIX `/c/...` path**), drop a stub `bw.exe` in
  it, `export PATH="$stub:$PATH"` in git-bash (POSIX form — ON git-bash's inherited env) WHILE that dir
  is absent from the registry User PATH. Assert IN ORDER: (i) check (a) PASSES; (ii) **FIRST** the naive
  `powershell.exe -Command "bw --version"` EXITS 0 — proving the false-green is LIVE (this is what a
  Windows-form export would have mangled away, false-passing P4); (iii) **THEN** the CORRECT check (b)
  (registry-REASSIGNED `$env:PATH`) EXITS 1; (iv) the helper does NOT skip / does NOT report green. A
  build that implemented the naive form would exit 0 at (iii) and FAIL P4. Never touches real PATH.
- **P5 — SHA256 fail-closed (M1).** Flip a byte in the zip OR feed a wrong-hash checksums.txt → helper
  ABORTS before extraction, non-zero exit, NO `bw.exe` placed, temp dir removed. Legit half: correct
  zip verifies + extracts.
- **P6 — Unix delegates to upstream (DC4).** linux/darwin (or `uname`-mocked): helper invokes upstream
  `install.sh` with `INSTALL_DIR="$HOME/.local/bin"`, NO `tar -xzf`/zip reimplementation on the Unix
  branch; idempotent skip when `>= floor`.
- **P7 — install.sh absent-flag byte-unchanged (DC6 regression bar; rev3 N4 placement).**
  `diff <(built install.sh --target user --dry-run) <(pre-arc install.sh --target user --dry-run)` →
  EMPTY; repeat `--target project --project-dir <tmp>` AND `--target subproject ...` (N4:
  target-independent placement means the byte-unchanged bar must hold across ALL targets). **Plus F6/N4
  probe:** `install.sh --bootstrap-bw` with NO `--target` → errors on `--target is required` with NO
  download and NO PATH mutation (assert the pre-flight did not fire before the target check — proving
  the block sits AFTER L753).
- **P8 — flag documented + wired.** `install.sh --help | grep -- '--bootstrap-bw'` present;
  `install.sh --target user --dry-run --bootstrap-bw` shows the pre-flight delegating to the helper in
  dry-run (planned actions, no mutation).
- **P9 — standing regression bar.** `npm run gen-data` deterministic (worktree `git diff` empty) + FULL
  app vitest suite green.
- **P10 — authorship + conformance (close-gate).** `Author=` Denson Smith zero-foreign (INCLUDING the
  new `win_path.ps1` — no author-like field naming anyone else); §28.9 seat trailer present; NOMOS
  CONFORMANT on the final commit.

---

## Self-assessed weak points (§6.2)

1. **The whole DC2 crux now depends on `powershell.exe` + the .NET registry API being present and
   invocable from git-bash.** This is a broader runtime assumption than rev1's `reg.exe`. *Why this
   shape anyway:* `powershell.exe` (Windows PowerShell 5.1) ships on every supported Win10/11, DC3
   already depends on it, and DC5's `Expand-Archive`/`Get-FileHash` already depend on it — so the
   helper's Windows branch is already powershell-bound; consolidating the registry work onto the same
   surface removes the reg.exe/MSYS class of failure entirely (proven DC2.0). If `powershell.exe` is
   truly absent the Windows branch cannot function at all, and that fails loud early.
2. **The 4095 ceiling is Win10/11-specific.** Pre-Win10 (Win7/8 without the hotfix) the cliff is 2047;
   the substrate's support matrix is Win10/11 only, so 4095 is correct here, but a pre-Win10 target
   would silently truncate between 2047 and 4095. *Why this shape anyway:* the substrate's only Windows
   runtime is Git-for-Windows on Win10/11; a lower ceiling would false-fail healthy Win10/11 machines
   (this one is composed=2119). I state the assumption rather than pick a wrong-for-the-target number.
3. **The GUI fail-loud fallback truncates a USER Path already >2047 on save (to 4095).** For the target
   machine (USER Path 800) this is a non-issue, but a machine with a >2047 USER Path that ALSO hit the
   fail-loud branch would risk GUI-truncation on the manual step. *Why this shape anyway:* the GUI is
   still safer than a scriptable REG_SZ-downgrading one-liner, the fail-loud branch is already the rare
   can't-append edge, and I state the corner in the message rather than hide it.
4. **P4's false-green discrimination rests on child-`powershell.exe` inheriting git-bash's exported
   PATH.** I confirmed this empirically this session, but if a future Git-for-Windows changed the child
   env-block behavior, the P4 fixture's "naive form would false-green" premise could weaken. *Why this
   shape anyway:* it is the observed behavior on the target runtime today, and the correct check (b) is
   robust regardless (it reassigns from the registry); P4 only needs the asymmetry to exist to *prove*
   discrimination, and it does. **rev3 N3 hardens P4's OWN integrity** (POSIX-form export so the stub is
   not mangled and the false-green is genuinely live), which is the test-layer complement to this.
5. **`cygpath` / `Expand-Archive` / `curl` tool-presence (inherited from rev1).** Fallbacks specified
   (USERPROFILE for cygpath; Get-FileHash for sha256sum) but not exhaustive. *Why this shape anyway:*
   target is Git-for-Windows on Win10/11; broadening is speculative scope.
6. **arm64 Windows designed but un-exercisable here (inherited).** Reference machine is amd64; VERA
   cannot drive the arm64 asset path. *Why this shape anyway:* the asset exists upstream and the code
   is arch-symmetric; the residual is test-coverage, not design.
7. **Version-parse brittleness (inherited).** Parsing `bw --version` / GitHub `tag_name` via grep/sed
   mirrors upstream; worst case is a redundant re-download of latest (still floor-satisfying).
8. **(rev3 N1-A) `-File "${HELPER_DIR}/win_path.ps1"` depends on the committed sibling being co-located
   with the helper.** If a future consumer copies `bootstrap-bw.sh` without `win_path.ps1`, the
   invocation breaks. *Why this shape anyway:* it fails LOUD (the `[ -f ]` guard → `err`, or powershell
   `-File not found` → non-zero → `fail_loud_path`), never a silent corruption; both in-arc consumers
   invoke the helper in-place from `substrate/` where the sibling always resolves; and the alternative
   (quoted-heredoc emission) trades this loud, localized failure for a silent-corruption class that
   depends on ADA getting a heredoc delimiter's quotes exactly right — a worse trade for the arc's
   highest-risk code.

## Residual questions for ARGUS (re-audit targets — N1-N4 folds)

- **R1 (carries from rev2, still live):** Confirm the `-File` (not `-Command`) invocation contract is
  the built form, and that `win_path.ps1` uses `DoNotExpandEnvironmentNames` on BOTH the read and the
  idempotent-check expansion — a build that reads expanded would freeze tokens on write-back.
- **R2 (N2):** Confirm the bash wrapper captures `rc=$?` on the line IMMEDIATELY after the
  `powershell.exe` call — no intervening pipe (`| tee`/`| grep`), no `|| true`. The sketch in DC2 is
  the build target; audit that ADA did not wrap the call in a pipeline (which would make `$?` the
  pipe's last stage) or swallow the exit.
- **R3 (N1):** Confirm option A (committed `substrate/win_path.ps1`) is the right call over option B
  (quoted heredoc). My justification: A removes the emission-integrity class entirely and makes the
  crux a directly-auditable file; the only cost is a co-location dependency that fails loud (weak point
  8). If you judge B preferable (fewer deliverables), the fallback is a `<<'WIN_PATH_PS1'` quoted
  heredoc with the delimiter quotes as a MUST — but A is my pick.
- **R4 (N3):** Confirm P4's POSIX-form stub export + the "assert naive exits 0 FIRST, then correct
  exits 1" ordering closes the F5 test-layer blind spot ARGUS demonstrated (a Windows-form export
  false-passing P4).
- **R5 (N4):** Confirm the pre-flight placement (after L753, before `case` at L761) is genuinely
  target-independent AND that the absent-flag byte-unchanged bar holds across `user|project|subproject`
  (P7 now diffs all three).
- **R6 (carries from rev2):** 4095 ceiling vs a safety margin (e.g. 4000) — I chose the exact
  web-confirmed 4095; your call to confirm or tighten.

## Out of scope (deliberately not addressed)

- The u--9s2 cookie-cutter call-site — helper is `--yes`-ready; wiring lands in u--9s2 (DC8).
- Mutating THIS machine's real Windows USER PATH during build/verify — throwaway `-KeyName` only.
- Changes to `bw upgrade` / `bw-upgrade.md` — the helper bootstraps the FIRST binary only.
- Editing the historical arc-19 directive — superseded-in-spirit, not rewritten.
- Moving `install-stoa` into `substrate/skills/` — stays at the repo root (stoa--sok).
- Any real provisioning / money / credentials — N/A (public download, no creds).
- A `bw init` in install.sh — the no-bw-init posture (SKILL.md L241) is PRESERVED, not touched.
- Pre-Win10 Windows PATH-length semantics (2047 cliff) — out of the substrate's support matrix.
