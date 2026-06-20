# Arc 68 (stoa--pk4) rev3 — P6(b) BUCKET 2 (resolution-failure) probe — CORRECTED trigger.
#
# METHODOLOGY NOTE (VERA finding): the design's P6(b) bucket-2 setup ("PATH with neither bw NOR
# git") does NOT reach the resolution-failure bucket — record-seat.ps1 line 93 runs `& git show`
# FIRST (under $ErrorActionPreference='Stop'), so removing git terminates the script before the
# Resolve-GitBashWithBw / fix(b) logic. To exercise bucket 2 faithfully we must keep `git`
# RESOLVABLE (so the line-93 read survives) but make Resolve-GitBashWithBw return $null — i.e.
# NO git-derived bash candidate has `command -v bw` succeed, and bw is NOT on the pwsh PATH.
#
# We do this with a THROWAWAY git shim whose dir has no bin\bash.exe nearby and whose --exec-path
# points at a bash-less dir, so the walk-up + exec-path derivation find ZERO bash candidates.

$ErrorActionPreference = 'Continue'
$repo = 'C:\Users\denso\claude_projects\the-stoa\.claude\worktrees\arc-68-build'
$rec  = Join-Path $repo 'substrate\skills\team-launcher\record-seat.ps1'
$origPath = $env:PATH

# Throwaway shim dir (no bash.exe anywhere up its tree; isolated under temp).
$shimRoot = Join-Path ([System.IO.Path]::GetTempPath()) ("vera-gitshim-" + [guid]::NewGuid().ToString('N'))
$shimBin  = Join-Path $shimRoot 'shimbin'
New-Item -ItemType Directory -Force -Path $shimBin | Out-Null
# A git shim that: answers `show` (empty -> "no manifest yet" path, exit 0-ish via our stub)
# and `--exec-path` (points at a bash-less dir). Implemented as git.cmd so Get-Command git finds it.
$gitCmd = @'
@echo off
if "%1"=="--exec-path" ( echo SHIMROOT/nowhere & exit /b 0 )
rem `show` of a beadwork path: emit nothing, exit 1 -> record-seat treats as "no manifest yet"
exit /b 1
'@
$gitCmd = $gitCmd -replace 'SHIMROOT', ($shimRoot -replace '\\','/')
Set-Content -Path (Join-Path $shimBin 'git.cmd') -Value $gitCmd -Encoding ASCII

# PATH: shim git only (+ system32 for the broken WSL bash, to mirror the real failing shape).
# NO real git, NO bw, NO git-bash bin dir.
$env:PATH = $shimBin + ';C:\windows\system32'
Write-Host ('  bw  = {0}' -f $(if(Get-Command bw -ErrorAction SilentlyContinue){'PRESENT (bad)'}else{'<null> OK'}))
$gitResolved = (Get-Command git -ErrorAction SilentlyContinue).Source
Write-Host ('  git = {0} (shim)' -f $gitResolved)
Write-Host ('  bash= {0}' -f (Get-Command bash -ErrorAction SilentlyContinue).Source)

$uuid = [guid]::NewGuid().ToString()
$out2 = & $rec -Seat probeResFail -Name probeResFail -SessionId $uuid -Project probe -Machine $(hostname) -Role team-architect -Composition custom-agent -Tier project 3>&1 2>&1
$exit2 = $LASTEXITCODE
$env:PATH = $origPath
# cleanup the throwaway shim
Remove-Item -Recurse -Force $shimRoot -ErrorAction SilentlyContinue

$out2str = ($out2 | Out-String)
Write-Host ('  record-seat exit = {0}' -f $exit2)
Write-Host '  --- output emitted ---'
Write-Host $out2str
$b2_hasResMsg  = $out2str -match 'PATH/RESOLUTION failure'
$b2_hasWslNote = $out2str -match 'is NOT git-bash and is intentionally skipped'
$b2_hasBwErr   = $out2str -match 'bw resolved and ran'
$b2_hasBenign  = $out2str -match 'expected on a workspace without the registry ticket'
Write-Host ('  bucket2 asserts: PATH/RESOLUTION msg={0}, WSL-skip note={1}, NOT bw-error={2}, NOT benign={3}, exit1={4}' -f `
  $b2_hasResMsg, $b2_hasWslNote, (-not $b2_hasBwErr), (-not $b2_hasBenign), ($exit2 -eq 1))
$bucket2Pass = $b2_hasResMsg -and $b2_hasWslNote -and (-not $b2_hasBwErr) -and (-not $b2_hasBenign) -and ($exit2 -eq 1)
if ($bucket2Pass) { Write-Host 'P6(b) BUCKET 2 PASS' } else { Write-Host 'P6(b) BUCKET 2 FAIL' }
