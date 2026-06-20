# Arc 68 design-rev3 — Launcher-correctness: ROBUST git-bash resolution for the record-seat bw-fallback

**Ticket:** `stoa--pk4` · **Author:** Denson Smith (the PRINCIPAL) · **Seat:** CAPTAIN_DAEDALUS_the_stoa
**Builds on:** design-rev2 (VERA-PASS on everything except the load-bearing C1/P6(a)) + as-built `8f3f2f9` on `arc-68/build`.
**Supersedes:** design-rev2 **ONLY** for §2.6 (the record-seat bw-resolution call site + fix(b) buckets) and §4 P6 (the P6(a)/P6(b) probes). **Everything else in rev2 STANDS VERA-PASS by reference** — §2.0/§2.0b/§2.1/§2.2/§2.3/§2.4/§2.5/§2.7/§2.8, §3 out-of-scope, §4 P1–P5/P7–P9 + full-suite backstop, §5 threat map, §6 W1–W4, §7 RQ1/RQ3/RQ4. Do NOT re-build any of those.
**Status:** focused FAIL-fix design hand-back. The C1 premise rev2 rested on (`Get-Command bash` resolves git-bash) is FALSIFIED on the target machine; this revision replaces it with a premise web-verified AND machine-verified this turn.

---

## §0 Changes from rev2 (changelog — one line per fold, for fast ADA/VERA/CATO diff)

- **C1 RESOLUTION FIX (load-bearing — the FAIL).** rev2 fix(a) used `Get-Command bash`. On the target machine WSL's `C:\windows\system32\bash.exe` (distro-less, BROKEN) SHADOWS git-bash on the fresh-terminal PATH, so the fallback invoked the wrong bash → `execvpe(/bin/bash) No such file` → exit 1 → no row written. **rev3 §2.6 fix(a) replaces `Get-Command bash` with a `Resolve-GitBashWithBw` helper that derives git-bash FROM `git` (which is never shadowed by WSL), walks up from `git.exe` to find `bin\bash.exe`/`usr\bin\bash.exe`, and selects the FIRST candidate where `command -v bw` succeeds — explicitly skipping the WSL shadow.** Web-verified + machine-verified (sources + evidence in §2.6).
- **LOGIN-SHELL fold (FM `[for: DAEDALUS]` build detail).** rev2/as-built invoked `bash -c` (non-login). The FM flagged — and the design now folds — that bw lives at `/c/Users/denso/bin/bw`, a dir added to PATH by the **login profile**; a non-login `-c` may not have it on PATH even via the right bash. **rev3 uses `bash -lc` (login shell) for BOTH the `command -v bw` resolution gate AND the attach invocation**, so the gate proves bw resolves in the exact context the attach uses.
- **PATH-transform fix (git-bash mount form, not WSL).** rev2's deterministic fallback produced `/C/...` (uppercase). git-bash's mount form is **lowercase** `/c/...` (WSL uses `/mnt/c/...`). rev3 §2.6 lowercases the drive letter in the deterministic fallback, and prefers `cygpath -u` THROUGH the resolved git-bash (which emits whatever mount form THAT bash understands). Web-verified + round-trip-proven.
- **fix(b) BUCKET FIX (kills the surviving mis-attribution — CONSEQUENCE 2).** rev2 fix(b) had three buckets (success / exit-N / `$null` no-bash). A wrong/broken bash that exits non-zero fell into the **exit-N (bw-error)** bucket and was mislabeled a benign bw/ticket error. **rev3 adds a distinct RESOLUTION-FAILURE bucket: when no bash carrying bw could be resolved (`Resolve-GitBashWithBw` returns `$null` OR the resolved bash's `command -v bw` gate failed), report it AS a resolution/PATH failure, loudly** — never as a bw/ticket error. The four buckets are enumerated in §2.6 fix(b).
- **P6(a) REWRITE (FORCE the git-derived resolution + PROVE a real row through the WSL-shadow PATH).** rev2 P6(a) shimmed `bw` unreachable and assumed `Get-Command bash` would reach git-bash. rev3 P6(a) makes the WSL-shadow PATH the DEFAULT real env it runs under (prepend `system32` so `Get-Command bash` resolves the WSL shadow), proves `Resolve-GitBashWithBw` STILL resolves the bw-carrying git-bash THROUGH the shadow, and round-trips a real `stoa--reg` row. The false-pass guard (do not front git-bash directly) is restated.
- **P6(b) INJECTION-TRIGGER FIX (VERA methodology flag).** rev2 P6(b) used `-Ticket bogus--nope` to drive the bw-error bucket, but bw 0.13.1 **auto-creates** that attachment (exit 0) — it does NOT error. rev3 P6(b) re-targets the bw-error bucket to a genuinely-erroring trigger (a syntactically-invalid ticket id OR a nonexistent attach source file — both confirmed exit 1 this turn) and adds a distinct sub-case for the NEW resolution-failure bucket.

---

## §1 Problem restatement (rev3-scoped)

The Arc-68 record-seat bw-fallback must write a real `stoa--reg` row on the affected Windows machine, where `bw` is on git-bash's PATH only and pwsh's `Get-Command bash` resolves a **broken, distro-less WSL launcher** that shadows git-bash. rev2's fix resolved the wrong bash, so (1) the registry-write still failed on the exact machine the bug manifests, and (2) fix(b) mislabeled that resolution failure as a benign bw/ticket error — partially defeating the whole point of the fix (killing the mis-attribution hazard). rev3 must: (Q1) resolve git-bash robustly WITHOUT touching `Get-Command bash`, deriving it from `git` (un-shadowed) and confirming `command -v bw` succeeds; (Q2) hand bw a path in git-bash's mount form (`/c/...` lowercase, via cygpath-through-that-bash or a deterministic transform); (Q3) add a fix(b) bucket so a wrong/broken-bash / no-bw-bash failure reports AS a resolution error, loudly; (Q4) rewrite P6(a) to FORCE the git-derived resolution through the WSL-shadow PATH and PROVE a real row, and fix P6(b)'s injection trigger (bw auto-creates `bogus--nope`, so it does not error).

**Imported assumptions (named, per §6.1) — rev3-specific (rev2's A1–A4 still hold by reference):**
- A5: `git` is on the pwsh PATH on any machine that runs the launcher (the launcher and the whole substrate already shell out to `git` everywhere — `record-seat.ps1` itself calls `& git show`). If `git` is NOT pwsh-resolvable, the registry-write was never going to work, and rev3 reports it as a resolution failure (the correct, loud outcome). VERIFIED on the target machine: `Get-Command git` → `C:\Program Files\Git\mingw64\bin\git.exe`.
- A6: the bw-carrying bash is a Git-for-Windows bash co-located under the same install root as `git`. VERIFIED: from `git.exe` the walk-up finds `C:\Program Files\Git\bin\bash.exe`, whose `command -v bw` = `/c/Users/denso/bin/bw`. (If a consumer installed bw under a DIFFERENT bash entirely, the `command -v bw` gate still selects it ONLY if it is reachable from a git-derived bash; otherwise rev3 reports a resolution failure loudly — the honest, non-mis-attributing outcome. Named as W5'.)

---

## §2.6 (SUPERSEDES rev2 §2.6) — record-seat ROBUST git-bash resolution + fix(b) buckets

**Scope:** this replaces ONLY the bw-resolution block (`record-seat.ps1` ~L162–L199 as-built at 8f3f2f9) and the fix(b) attribution block (~L201–L216). The `-Ticket` param (C5), the DC4 additive fields, the read-modify-rewrite logic, the temp-file write, and the success `Write-Host` are UNCHANGED (all VERA-PASS). The two launcher warning strings (`launch-team.ps1` L360/L363) are UNCHANGED — they already echo record-seat's specific cause (VERA-PASS P6(c)).

### Q1 — robust git-bash resolution (web-verified + machine-verified)

**Premise (web-verified — sources cited):**
- Git-for-Windows install layout: `git` on the pwsh PATH lives under the Git install tree; the bash to invoke programmatically from PowerShell is `<GitRoot>\bin\bash.exe` (the wrapper bash that sets `MSYSTEM`/PATH then launches the real `usr\bin\bash.exe`). Source: gitforwindows.org + Stack Overflow "Git for Windows directory layout / which bash.exe to invoke from PowerShell" — https://gitforwindows.org/ and https://stackoverflow.com/questions/tagged/git-for-windows (layout: `cmd\git.exe` wrapper, `bin\bash.exe` wrapper, `usr\bin\bash.exe` real, `mingw64\libexec\git-core` = `git --exec-path`).
- `git --exec-path` outputs `<GitRoot>\mingw64\libexec\git-core`; stripping that tail yields the install root, from which `bin\bash.exe` / `usr\bin\bash.exe` are reachable. Source: same.
- WSL bash uses `/mnt/c/...`; git-bash (MSYS2) uses `/c/...` (lowercase drive). `cygpath` is the git-bash/MSYS2 path tool; WSL uses `wslpath`. Source: Stack Overflow / MSYS2 docs "git bash /c vs WSL /mnt/c mount path; cygpath vs wslpath".
- `command -v <cmd>` exits 0 iff the command is found (POSIX builtin). Source: POSIX Shell & Utilities / Stack Overflow "command -v exit code".

**Machine-verified THIS turn (the verify-the-PREMISE-on-the-target lesson, executed):**
- `Get-Command git` → `C:\Program Files\Git\mingw64\bin\git.exe` (NOT `cmd\git.exe` — so a naive "strip `\cmd\git.exe`" derivation would give the WRONG root). `Get-Command git` is UNAFFECTED by the WSL shadow (git is never named `bash`).
- Reconstructing the WSL-shadow PATH (`system32` prepended): `Get-Command bash` → `C:\windows\system32\bash.exe` (the broken WSL launcher) — confirming rev2's FAIL; `Get-Command git` STILL → the git-bash git.exe (un-shadowed).
- Walk-up from `git.exe` resolves `C:\Program Files\Git\bin\bash.exe`; `command -v bw` through it (via `-lc`) → `/c/Users/denso/bin/bw`, exit 0. PROVEN under the reconstructed WSL-shadow PATH.

**The resolution helper (exact PowerShell — add near the top of `record-seat.ps1`, after the param block / before the bw-invocation block):**

```powershell
# Arc 68 (stoa--pk4) rev3 / C1: resolve a git-bash that ACTUALLY carries bw, WITHOUT touching
# `Get-Command bash` (which on this and many Windows machines resolves WSL's distro-less,
# broken C:\windows\system32\bash.exe — it SHADOWS git-bash on the PATH). `git` is never
# shadowed by WSL, so we derive git-bash FROM git's own location, then SELECT the first
# candidate where `command -v bw` succeeds in the SAME login-shell invocation the attach uses.
function Resolve-GitBashWithBw {
  $cands = New-Object System.Collections.Generic.List[string]
  $git = Get-Command git -ErrorAction SilentlyContinue
  if ($git) {
    # Walk up from git.exe's dir (git may be at cmd\git.exe OR mingw64\bin\git.exe — do NOT
    # assume a fixed depth); at each level look for the wrapper bash, then the real bash.
    $dir = Split-Path -Parent $git.Source
    for ($i = 0; $i -lt 6 -and $dir; $i++) {
      foreach ($rel in @('bin\bash.exe','usr\bin\bash.exe')) {
        $c = Join-Path $dir $rel
        if ((Test-Path $c) -and -not $cands.Contains($c)) { $cands.Add($c) }
      }
      $dir = Split-Path -Parent $dir
    }
    # Belt-and-suspenders: derive from `git --exec-path` (handles non-standard git.exe placement).
    $ep = (& $git.Source --exec-path 2>$null)
    if ($ep) {
      $epDir = ($ep -replace '/','\').TrimEnd('\')
      for ($j = 0; $j -lt 6 -and $epDir; $j++) {
        foreach ($rel in @('bin\bash.exe','usr\bin\bash.exe')) {
          $c = Join-Path $epDir $rel
          if ((Test-Path $c) -and -not $cands.Contains($c)) { $cands.Add($c) }
        }
        $epDir = Split-Path -Parent $epDir
      }
    }
  }
  # Select the FIRST candidate where bw resolves IN THE LOGIN SHELL (-lc) the attach will use.
  foreach ($c in $cands) {
    & $c -lc 'command -v bw >/dev/null 2>&1' 2>$null
    if ($LASTEXITCODE -eq 0) { return $c }
  }
  # No git-bash carrying bw could be resolved -> distinct from a bw error (see fix(b) bucket).
  return $null
}
```

> **Why walk-up + `command -v bw` gate, not a fixed `<GitRoot>\bin\bash.exe` path:** machine-verified, `Get-Command git` resolved `mingw64\bin\git.exe`, so a fixed "strip `\cmd\git.exe`" would land on `mingw64` and miss `<GitRoot>\bin\bash.exe`. The walk-up tolerates either git.exe placement. The `command -v bw` gate is the load-bearing correctness check: it GUARANTEES the chosen bash actually reaches bw (per the FM/user-tier "resolve a bash where `command -v bw` succeeds" guidance), so even a future machine with an exotic layout either resolves a working bash or reports a resolution failure — it can never silently pick a bw-less bash.

### Q2 — git-bash mount-path form (cygpath-through-the-resolved-bash; deterministic lowercase-`/c/` fallback)

**The path transform (exact PowerShell — inside the fallback branch, using the resolved `$bash`):**

```powershell
# Convert the Windows temp path to the form THIS git-bash understands. cygpath -u THROUGH the
# resolved bash is robust (it emits git-bash's own mount form). Deterministic fallback: backslashes
# -> slashes, leading "X:" -> "/x" (LOWERCASE drive = git-bash mount form, NOT WSL's /mnt/c).
$tmpBash = $null
& $bash -lc 'command -v cygpath >/dev/null 2>&1' 2>$null
if ($LASTEXITCODE -eq 0) {
  $tmpBash = (& $bash -lc 'cygpath -u "$1"' bash $tmp 2>$null).Trim()
}
if ([string]::IsNullOrWhiteSpace($tmpBash)) {
  $tmpBash = $tmp -replace '\\','/'
  $tmpBash = [regex]::Replace($tmpBash, '^([A-Za-z]):', { param($m) '/' + $m.Groups[1].Value.ToLower() })
}
```

> **Machine-verified:** cygpath confirmed at `/usr/bin/cygpath` in the resolved git-bash. `cygpath -u` of the Windows temp path returned `/tmp/stoa-seat-registry.jsonl` (git-bash mounts `%TEMP%` at `/tmp`, which resolves to the SAME underlying file as `/c/.../Temp/...` — no divergence; the FM independently confirmed this). The deterministic fallback produced `/c/Users/denso/AppData/Local/Temp/stoa-seat-registry.jsonl` and a `cat` round-trip through git-bash exited 0. Either form reads the same file.

**The attach invocation (LOGIN shell, positional args — keeps the FM-adopted apostrophe-safe positional form, switches `-c` → `-lc`):**

```powershell
# LOGIN shell (-lc): bw lives at /c/Users/<user>/bin/bw, added to PATH by the login profile;
# a non-login -c may not have it on PATH even via the right bash (FM build detail). Positional
# args (no interpolation of values into the script body) keep the apostrophe-in-username case safe.
& $bash -lc 'bw attach "$1" "$2" --name "$3"' bash $ticket $tmpBash $attachName
$bwExit = $LASTEXITCODE
```

### Q3 — fix(b) attribution buckets (FOUR cases — kills the surviving mis-attribution)

The full resolve-and-invoke block + fix(b) attribution (replaces as-built ~L162–L216). `$bwExit` distinguishes the four outcomes; the NEW bucket is **resolution failure**:

```powershell
$bwExit = $null
$attachThrew = ''
$resolvedBash = $null
try {
  $bwCmd = Get-Command bw -ErrorAction SilentlyContinue
  if ($bwCmd) {
    # bw is directly on the pwsh PATH — invoke it directly.
    & $bwCmd.Source attach $ticket $tmp --name $attachName
    $bwExit = $LASTEXITCODE
  } else {
    # bw NOT on the pwsh PATH — resolve a git-bash that CARRIES bw (skips the WSL shadow).
    $resolvedBash = Resolve-GitBashWithBw
    if ($resolvedBash) {
      # ... Q2 path transform sets $tmpBash ...
      & $resolvedBash -lc 'bw attach "$1" "$2" --name "$3"' bash $ticket $tmpBash $attachName
      $bwExit = $LASTEXITCODE
    } else {
      # No git-bash carrying bw could be resolved (e.g. only a broken/WSL bash is present,
      # or git-bash has no bw). This is a RESOLUTION failure, NOT a bw/ticket error. Leave
      # $bwExit = $null and $resolvedBash = $null to route the distinct fix(b) bucket below.
      $bwExit = $null
    }
  }
} catch {
  $attachThrew = $_.Exception.Message
}

# fix(b) — FOUR buckets so a wrong/broken-bash or no-bw-bash failure reports AS a resolution
# error (LOUD), and can NEVER again hide behind the benign "no registry ticket" / bw-error label.
$attachOk = $false; $failReason = ''
if ($attachThrew) {
  $failReason = "bw attach threw: $attachThrew"
} elseif ($bwExit -eq 0) {
  $attachOk = $true
} elseif ($null -eq $bwExit) {
  # BUCKET: resolution failure (no bw on pwsh PATH AND no git-bash carrying bw resolvable).
  $failReason = "bw could NOT be resolved: not on the pwsh PATH, and no git-bash carrying bw was found (a git-bash derived from 'git' where 'command -v bw' succeeds). This is a PATH/RESOLUTION failure, NOT a missing-ticket or bw-error case. On this machine bw is on the git-bash PATH only; note WSL's C:\windows\system32\bash.exe (if present) is NOT git-bash and is intentionally skipped (Arc 68 / stoa--pk4 rev3)."
} else {
  # BUCKET: bw RAN (via the resolved git-bash or the pwsh PATH) but the attach exited non-zero.
  $failReason = "bw attach to '$ticket' exited $bwExit (bw resolved and ran, but the attach failed: e.g. an invalid ticket id, or a real bw/store error). NOTE: a non-existent ticket may AUTO-CREATE on this bw version rather than error, so a non-zero exit here is a genuine bw/store error, not the benign no-ticket case."
}
if (-not $attachOk) {
  Write-Warning "record-seat: could not record seat '$Seat' to '$ticket'. $failReason"
  exit 1
}
```

**The four buckets, explicitly:**
1. **success** (`$bwExit -eq 0`) — row written.
2. **resolution failure** (`$null -eq $bwExit`, NEW wording) — bw is not on the pwsh PATH AND no git-bash carrying bw could be resolved (covers VERA's wrong-bash/WSL-broken case: `Resolve-GitBashWithBw` returns `$null` because the only bash candidates either don't exist as git-bash OR fail the `command -v bw` gate). Reported LOUDLY as a resolution/PATH failure. **This is the bucket that kills CONSEQUENCE 2.**
3. **bw-error** (`$bwExit` non-zero) — bw resolved and ran but the attach failed (invalid ticket id / store error). The benign-no-ticket language is REMOVED (bw auto-creates a missing ticket, so a non-zero exit here is a genuine error).
4. **threw** (`$attachThrew`) — an unexpected pwsh exception.

> **Why the WSL-broken case now lands in bucket 2, not bucket 3:** rev2 invoked the WSL bash and let it exit 1, which fell into bucket 3 (bw-error). rev3 NEVER invokes the WSL bash — `Resolve-GitBashWithBw` derives candidates from `git` (not `Get-Command bash`) and gates each on `command -v bw`; the WSL launcher is never a candidate (it isn't under git's install tree) and could not pass the gate anyway (it's distro-less/broken). So when only a broken/WSL bash is present, `Resolve-GitBashWithBw` returns `$null` → bucket 2 (resolution failure), reported correctly.

### Threat note (§35.5 carve-out re-confirmed)

The git-bash path is derived from `git`'s own system-controlled install location (`Get-Command git`), NOT from any untrusted/agent-controlled input; the temp path is a fixed-literal filename under `GetTempPath()`; the attach interpolands are passed POSITIONALLY (no interpolation into the bash script body). No new attack path is introduced. The **`not threat-ratified (process change, no runtime attack path)`** classification (rev2 §5, ARGUS-CONFIRMED) STANDS for rev3 — DAEDALUS PROPOSES it unchanged; ARGUS confirms on re-check (the PLINY routing notes a full ARGUS re-run may be skipped for this localized fix unless something novel surfaces; nothing novel surfaced — the resolution reads only system-controlled locations). No threat-anchored probe required (§6.13 / §35.5).

---

## §4 P6 (SUPERSEDES rev2 §4 P6) — record-seat resolution probes

> P1–P5, P7–P9, and the full-suite backstop are UNCHANGED from rev2 (all VERA-PASS); re-run them as the regression set. Only P6 is revised.

**P6 — record-seat ROBUST-resolution probe (the C1 FAIL-fix; the load-bearing real-execution probe).**

- **(a) FORCE the git-derived resolution THROUGH the WSL-shadow PATH + PROVE a real row round-trips (C1/rev3 — NON-NEGOTIABLE).** The whole point: prove the resolution reaches the bw-carrying git-bash even when `Get-Command bash` resolves the broken WSL shadow (the real fresh-terminal env on this machine). Procedure:
  1. **Establish the real-failure baseline (the env rev2 failed under):** in the probe pwsh, set `$env:PATH = 'C:\windows\system32;' + $env:PATH` (so `Get-Command bash` resolves `C:\windows\system32\bash.exe`, the broken WSL launcher), and ensure `bw` is NOT directly on the pwsh PATH (assert `Get-Command bw -ErrorAction SilentlyContinue` is `$null`). ASSERT `(Get-Command bash).Source` is the WSL `system32\bash.exe` — i.e. the probe is genuinely running under the shadow that broke rev2. **FALSE-PASS GUARD (restated from the FM/user-tier guard on this ticket): the probe MUST NOT front git-bash directly, prepend git-bash ahead of system32, or shim `bw` onto the pwsh PATH — a pass that bypasses the WSL-shadow resolution is REJECTED. The valid test exercises the REAL `Resolve-GitBashWithBw` derivation through the shadow.**
  2. ASSERT `Resolve-GitBashWithBw` (called directly, or as exercised by `record-seat.ps1`) returns a git-bash whose `& $resolved -lc 'command -v bw'` prints a bw path and exits 0 — proving it SKIPPED the WSL shadow and found the bw-carrying git-bash.
  3. Run `record-seat.ps1 -Seat probeFallback -Name probeFallback -SessionId <uuid> -Project probe -Machine $(hostname) -Role team-architect -Composition custom-agent -Tier project` under that WSL-shadow PATH. With `bw` pwsh-unreachable, execution MUST take the resolve-git-bash fallback, convert `$tmp` to the git-bash mount form, and attach via `bash -lc`.
  4. **ASSERT a real row round-trips:** `git show beadwork:attachments/stoa--reg/seat-registry.jsonl | ConvertFrom-Json | Where seat -eq probeFallback` returns the row; ASSERT `record-seat.ps1` exited 0 and emitted the success `Write-Host`.
  5. CLEANUP: remove the `probeFallback` row via the existing read-modify-rewrite (restore `stoa--reg` to its baseline sha); restore `$env:PATH`.
  FALSIFIES "the resolution still grabs the wrong/broken bash through the WSL shadow / cannot write a real row on the affected machine." A pass here is the C1 proof rev2 owed.

- **(b) Error-attribution: the FOUR buckets are distinct AND a resolution failure reports AS a resolution failure (kills CONSEQUENCE 2).**
  - **resolution-failure bucket (the NEW, load-bearing case):** shim BOTH `bw` AND any git-bash unreachable from the resolution — e.g. set `$env:PATH` to a minimal value that contains neither `bw` nor `git` (so `Resolve-GitBashWithBw` finds no candidate and returns `$null`), OR (closer to the real failure shape) leave only the broken WSL `system32\bash.exe` reachable and remove git from PATH so `Resolve-GitBashWithBw` returns `$null`. ASSERT `record-seat.ps1` exits 1 and the warning is the **resolution-failure** message (`PATH/RESOLUTION failure, NOT a missing-ticket or bw-error case` … `WSL's C:\windows\system32\bash.exe … is NOT git-bash and is intentionally skipped`). ASSERT it does NOT emit the bw-error/benign language. **This is the assertion that proves the WSL-broken failure no longer mis-buckets as a bw/ticket error.**
  - **bw-error bucket (genuinely-erroring trigger — VERA methodology-flag fix):** with `bw` resolvable (real PATH or via the resolved git-bash), drive a GENUINE bw error. `-Ticket bogus--nope` does NOT work (bw 0.13.1 auto-creates the attachment → exit 0). Use instead a **syntactically-invalid ticket id** (`-Ticket "not a valid id!!!"`, confirmed exit 1 this turn) OR a condition where bw runs but the attach fails (confirmed exit 1 this turn). ASSERT the warning is the `bw attach to '<ticket>' exited <N>` (bucket 3) message, distinct from the resolution-failure message, and that the message carries the auto-create NOTE (so a future reader does not re-introduce the benign-no-ticket mislabel).
  FALSIFIES "the resolution failure still mis-buckets as a bw/ticket error (CONSEQUENCE 2 survives)" + "the buckets are not distinguishable / P6(b) has no genuinely-erroring bw trigger."

- **(c)** Grep `record-seat.ps1`: ASSERT the old collapsed message `expected on a workspace without the registry ticket` does NOT appear (VERA-PASS, carried). ADDITIONALLY ASSERT the resolution-failure bucket text (`PATH/RESOLUTION failure` + the WSL-skip note) is present and is the message reached when `Resolve-GitBashWithBw` returns `$null` — i.e. the new bucket is wired, not orphaned.

---

## §6 Self-assessed weak points (rev3-specific; rev2 W1–W4 stand by reference)

- **W5' — `Resolve-GitBashWithBw` assumes the bw-carrying bash is reachable from a git-derived bash.** If a consumer installed bw under a bash entirely unrelated to git (no git-derived candidate has `command -v bw` succeed), `Resolve-GitBashWithBw` returns `$null` → the resolution-failure bucket fires. *Why this shape anyway:* on the target machine (and the standard Git-for-Windows + bw-under-git-bash setup) this resolves correctly, machine-verified; and the failure mode is the CORRECT, loud one (a resolution failure reported AS a resolution failure), not a silent mis-attribution — strictly better than rev2. If a real consumer hits the exotic split-install case, the fix is additive (accept an explicit `-BashPath` override or widen the candidate set), localized to this helper. NAMED, not hidden.
- **W6' — the `command -v bw` gate runs git-bash up to N times at resolution (one `-lc` per candidate).** On the normal machine there is exactly one viable candidate, so it's a single extra `bash -lc 'command -v bw'` before the attach. *Why this shape anyway:* the gate is the load-bearing correctness guarantee (it is WHY the WSL bash can never be selected); the cost is one cheap login-shell probe on the fallback path only (the pwsh-PATH-has-bw fast path skips it entirely). Bounded, fallback-only.
- **W7' — login-shell (`-lc`) is now load-bearing and machine-verified on ONE machine.** On THIS machine both `-lc` and `-c` resolved bw (so `/c/Users/denso/bin` is on a non-login PATH too); the FM flagged the general case where bw is login-profile-only. *Why this shape anyway:* `-lc` is the strictly-safer choice (sources the login profile that the FM identified as where bw's dir is added), and the `command -v bw` gate uses the SAME `-lc` form, so whatever the chosen invocation's PATH, the gate proves bw resolves in it before the attach runs — the gate makes `-lc`-vs-`-c` self-correcting. VERA P6(a) re-proves the actual invocation resolves bw.

---

## §7 Residual questions for ARGUS (rev3-specific; rev2 RQ1/RQ3/RQ4 stand by reference)

- RQ2' (§2.6 / §35.5): re-confirm the `not threat-ratified (process change, no runtime attack path)` carve-out STILL holds after rev3's resolution change — the new code reads only `Get-Command git` (system-controlled install location), `Test-Path` on derived paths, and `command -v bw` through a git-derived bash; no untrusted input reaches the resolution; the attach interpolands stay positional (no script-body interpolation). My judgment: carve-out holds, no new attack path. PLINY noted a full ARGUS re-run may be skipped for this localized fix; flagging for the confirm regardless.
- RQ5' (W5'): is the resolution-failure-bucket-on-exotic-split-install behavior acceptable as the honest residual, or does the floor-manager want an explicit `-BashPath` override folded now? My call: the loud resolution-failure outcome is correct and sufficient; an override is additive-later, not needed for the target machine. Flagged for belt+suspenders preference.

---

## §8 What VERA must still empirically prove (the build-time-verified unknowns rev3 names)

1. **P6(a) under the REAL WSL-shadow PATH** — `Resolve-GitBashWithBw` resolves the bw-carrying git-bash THROUGH the shadow and a real `probeFallback` row round-trips (exit 0). This is the C1 proof. (DAEDALUS machine-verified the resolution + a cat round-trip this turn under a reconstructed shadow PATH, but VERA owns the full `record-seat.ps1` real-row round-trip + the false-pass-guard-clean execution.)
2. **P6(b) resolution-failure bucket** — a no-git-bash / broken-WSL-only env produces the resolution-failure message, NOT the bw-error message (CONSEQUENCE 2 killed).
3. **P6(b) bw-error bucket** — a genuinely-erroring trigger (invalid ticket id / failed attach) produces the distinct bw-error message; confirm the chosen trigger actually exits non-zero on the live bw version.
4. **Cleanup** — `stoa--reg` restored to its exact baseline sha after the probe rows (the existing P6(a) cleanup discipline).
