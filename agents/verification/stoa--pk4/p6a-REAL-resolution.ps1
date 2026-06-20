# VERA P6(a) RE-RUN against the REAL pwsh Get-Command bash resolution.
# (Per the FM's false-pass guard, stoa--pk4: a P6a PASS is valid ONLY if it
#  exercised the REAL pwsh Get-Command bash resolution and STILL wrote+round-
#  tripped a real row. This probe uses the registry-backed Machine+User PATH —
#  the PATH a freshly-launched pwsh terminal actually gets — NOT the Bash-tool-
#  inherited PATH that happens to front git-bash.)
$ErrorActionPreference = 'Stop'
$wt = 'C:\Users\denso\claude_projects\the-stoa\.claude\worktrees\arc-68-build'
$record = Join-Path $wt 'substrate\skills\team-launcher\record-seat.ps1'

$m = [Environment]::GetEnvironmentVariable('PATH','Machine')
$u = [Environment]::GetEnvironmentVariable('PATH','User')
$real = ($m.TrimEnd(';') + ';' + $u).TrimEnd(';')
$origPath = $env:PATH
$env:PATH = $real   # the REAL fresh-terminal PATH

$bw   = Get-Command bw   -ErrorAction SilentlyContinue
$bash = Get-Command bash -ErrorAction SilentlyContinue
$cyg  = Get-Command cygpath -ErrorAction SilentlyContinue
Write-Host ("REAL-RESOLUTION: Get-Command bw = {0}; Get-Command bash = {1}; Get-Command cygpath = {2}" -f `
  $(if($bw){$bw.Source}else{'NULL'}), $(if($bash){$bash.Source}else{'NULL'}), $(if($cyg){$cyg.Source}else{'NULL'}))

# git must still be reachable for record-seat's `git show` read step.
$git = Get-Command git -ErrorAction SilentlyContinue
Write-Host ("git = {0}" -f $(if($git){$git.Source}else{'NULL'}))

Write-Host "`n--- Running record-seat.ps1 against the REAL resolution (expect: FAIL on this machine per FM) ---"
Set-Location $wt
$out = & $record -Seat probeRealRes -Name probeRealRes -SessionId '00000000-0000-0000-0000-000000000000' `
  -Project probe -Machine 'M' -Role team-architect -Composition custom-agent -Tier project 2>&1
$exit = $LASTEXITCODE
$env:PATH = $origPath
Write-Host "--- record-seat output ---"
$out | ForEach-Object { Write-Host $_ }
Write-Host ("EXIT=$exit")
