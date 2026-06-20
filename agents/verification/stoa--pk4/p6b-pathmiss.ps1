# VERA P6(b) PATH-miss case — both bw AND bash pwsh-unreachable => $bwExit=$null
# => the PATH-miss message (NOT the old benign-unconditional string). (stoa--pk4)
$ErrorActionPreference = 'Stop'
$wt = 'C:\Users\denso\claude_projects\the-stoa\.claude\worktrees\arc-68-build'
$record = Join-Path $wt 'substrate\skills\team-launcher\record-seat.ps1'

$gitDir  = 'C:\Program Files\Git\mingw64\bin'   # git only (for the read); NO bash, NO bw
$pwshDir = 'C:\Program Files\PowerShell\7'
$origPath = $env:PATH
# Exclude BOTH the bw dir AND the git\usr\bin dir (where bash + cygpath live).
$env:PATH = "$gitDir;$pwshDir;C:\Windows\System32;C:\Windows"

$bw   = Get-Command bw   -ErrorAction SilentlyContinue
$bash = Get-Command bash -ErrorAction SilentlyContinue
Write-Host ("SHIM-STATE: Get-Command bw = {0}; Get-Command bash = {1}" -f `
  $(if($bw){"NON-NULL -- SHIM FAILED"}else{'$null (OK)'}), `
  $(if($bash){"NON-NULL -- SHIM FAILED"}else{'$null (OK)'}))
if ($bw -or $bash) { $env:PATH = $origPath; throw 'P6b PATH-miss SHIM FAILED: bw or bash still resolvable.' }

Set-Location $wt
$out = & $record -Seat probePathMiss -Name probePathMiss -SessionId '00000000-0000-0000-0000-000000000000' `
  -Project probe -Machine 'M' -Role team-architect -Tier project 2>&1
$exit = $LASTEXITCODE
$env:PATH = $origPath
Write-Host "--- record-seat output ---"
$out | ForEach-Object { Write-Host $_ }
Write-Host ("EXIT=$exit")
