# Arc 68 (stoa--pk4) rev3 — P6(a) C1 GATE probe (VERA RE-PROVE).
# Reproduces the REAL pwsh fresh-terminal env where the bug manifests:
#   - bw is NOT directly on the pwsh PATH (strip C:\Users\denso\bin, where bw.exe lives)
#   - C:\windows\system32 is PREPENDED so Get-Command bash resolves the BROKEN WSL shadow
# FALSE-PASS GUARD: this does NOT front git-bash, does NOT prepend git-bash ahead of
# system32, does NOT shim bw onto the pwsh PATH. It installs the BROKEN state and forces
# the real Resolve-GitBashWithBw derivation (from `git`, un-shadowed) to do the work.

$ErrorActionPreference = 'Stop'
$repo = 'C:\Users\denso\claude_projects\the-stoa\.claude\worktrees\arc-68-build'
$rec  = Join-Path $repo 'substrate\skills\team-launcher\record-seat.ps1'

Write-Host '########## P6(a) STEP 1 — establish the REAL WSL-shadow failing PATH ##########'
$origPath = $env:PATH
# Strip the bw dir (C:\Users\denso\bin) from PATH so bw is NOT on the pwsh PATH.
$stripped = ($env:PATH -split ';') | Where-Object { $_ -and ($_ -notlike '*denso\bin*') }
# Prepend system32 so Get-Command bash resolves the WSL shadow.
$env:PATH = 'C:\windows\system32;' + ($stripped -join ';')

Write-Host '--- Get-Command bw (must be NULL) ---'
$bw = Get-Command bw -ErrorAction SilentlyContinue
if ($bw) { Write-Host ("FAIL-SETUP: bw still on pwsh PATH at {0}" -f $bw.Source); $env:PATH = $origPath; exit 99 }
else { Write-Host 'bw = <null>  [OK: forces the fallback]' }

Write-Host '--- Get-Command bash (must be the WSL system32 shadow) ---'
$bashSrc = (Get-Command bash -ErrorAction SilentlyContinue).Source
Write-Host ("bash -> {0}" -f $bashSrc)
if ($bashSrc -ne 'C:\windows\system32\bash.exe') {
  Write-Host ("FAIL-SETUP: Get-Command bash did NOT resolve the WSL shadow (got {0})" -f $bashSrc)
  $env:PATH = $origPath; exit 98
}
Write-Host '[OK: running under the EXACT WSL shadow that broke rev2]'

Write-Host '--- Get-Command git (must be un-shadowed git.exe) ---'
$gitSrc = (Get-Command git -ErrorAction SilentlyContinue).Source
Write-Host ("git  -> {0}" -f $gitSrc)

Write-Host ''
Write-Host '########## P6(a) STEP 2 — Resolve-GitBashWithBw resolves bw-carrying git-bash THROUGH the shadow ##########'
# Dot-source the function out of the file under test (exercise the REAL code, not a copy).
# Extract by line range (function Resolve-GitBashWithBw spans lines 172-206 in record-seat.ps1).
$allLines = Get-Content $rec
$fnStart = ($allLines | Select-String -Pattern '^function Resolve-GitBashWithBw' | Select-Object -First 1).LineNumber - 1
# find the closing brace: first line == '}' at/after the lone "return $null" line inside the fn
$fnEnd = $fnStart
for ($k = $fnStart; $k -lt $allLines.Count; $k++) { if ($k -gt $fnStart -and $allLines[$k] -eq '}') { $fnEnd = $k; break } }
$fnText = ($allLines[$fnStart..$fnEnd] -join "`n")
Write-Host ("  [extracted Resolve-GitBashWithBw: lines {0}-{1} of record-seat.ps1]" -f ($fnStart+1), ($fnEnd+1))
. ([scriptblock]::Create($fnText))
$resolved = Resolve-GitBashWithBw
Write-Host ("Resolve-GitBashWithBw -> {0}" -f $(if($resolved){$resolved}else{'<null>'}))
if (-not $resolved) { Write-Host 'FAIL: resolution returned $null under the shadow'; $env:PATH=$origPath; exit 2 }
if ($resolved -eq 'C:\windows\system32\bash.exe') { Write-Host 'FAIL: resolution grabbed the WSL shadow!'; $env:PATH=$origPath; exit 3 }
Write-Host '--- prove the resolved bash carries bw (command -v bw via -lc) ---'
& $resolved -lc 'command -v bw'
Write-Host ("  command -v bw exit = {0}" -f $LASTEXITCODE)
if ($LASTEXITCODE -ne 0) { Write-Host 'FAIL: resolved bash does not carry bw'; $env:PATH=$origPath; exit 4 }

Write-Host ''
Write-Host '########## P6(a) STEP 3 — run record-seat.ps1 under the shadow (must take the fallback) ##########'
$uuid = [guid]::NewGuid().ToString()
Write-Host ("SessionId = {0}" -f $uuid)
& $rec -Seat probeFallback -Name probeFallback -SessionId $uuid -Project probe -Machine $(hostname) -Role team-architect -Composition custom-agent -Tier project
$recExit = $LASTEXITCODE
Write-Host ("record-seat.ps1 exit = {0}" -f $recExit)

Write-Host ''
Write-Host '########## P6(a) STEP 4 — ASSERT a real row round-trips ##########'
$row = git show beadwork:attachments/stoa--reg/seat-registry.jsonl | ConvertFrom-Json | Where-Object { $_.seat -eq 'probeFallback' }
if ($row) {
  Write-Host '[ROW FOUND]'
  $row | ConvertTo-Json -Compress
  Write-Host ("  session_id matches probe uuid: {0}" -f ($row.session_id -eq $uuid))
} else {
  Write-Host 'FAIL: probeFallback row did NOT round-trip'
}

# restore PATH before exit (cleanup of the row happens in the cleanup probe)
$env:PATH = $origPath
Write-Host ''
Write-Host ("########## P6(a) RESULT: recExit={0}, rowFound={1} ##########" -f $recExit, [bool]$row)
if ($recExit -eq 0 -and $row) { Write-Host 'P6(a) PASS' } else { Write-Host 'P6(a) FAIL' }
