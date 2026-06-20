# Arc 68 (stoa--pk4) rev3 — P6(b) 4-bucket attribution probe (VERA RE-PROVE).
# Drives the two FAIL buckets that distinguish a resolution failure from a bw error:
#   Bucket 2 (resolution-failure, NEW): no bw on pwsh PATH AND no git-derivable git-bash
#            -> Resolve-GitBashWithBw returns $null -> LOUD resolution-failure message.
#   Bucket 3 (bw-error): bw resolvable, but the attach genuinely errors (invalid ticket id,
#            confirmed exit 1 on bw 0.13.1) -> bw-error message, distinct from bucket 2.
# Asserts the two messages are DISTINCT and that bucket 2 does NOT emit the benign/bw-error language.

$ErrorActionPreference = 'Continue'
$repo = 'C:\Users\denso\claude_projects\the-stoa\.claude\worktrees\arc-68-build'
$rec  = Join-Path $repo 'substrate\skills\team-launcher\record-seat.ps1'
$origPath = $env:PATH

Write-Host '########## P6(b) BUCKET 2 — resolution-failure (no git-derivable bw-bash) ##########'
# Minimal PATH: only system32 (carries the BROKEN WSL bash, NO git, NO bw). So:
#   Get-Command bw   -> null (not on PATH)
#   Get-Command git  -> null (removed)  => Resolve-GitBashWithBw finds no candidate => $null
#   Get-Command bash -> WSL system32 shadow (but it is NEVER a candidate; not git-derived)
$env:PATH = 'C:\windows\system32'
Write-Host ('  bw  = {0}' -f $(if(Get-Command bw -ErrorAction SilentlyContinue){'PRESENT (bad)'}else{'<null> OK'}))
Write-Host ('  git = {0}' -f $(if(Get-Command git -ErrorAction SilentlyContinue){'PRESENT (bad)'}else{'<null> OK'}))
Write-Host ('  bash= {0}' -f (Get-Command bash -ErrorAction SilentlyContinue).Source)

$uuid = [guid]::NewGuid().ToString()
$out2 = & $rec -Seat probeResFail -Name probeResFail -SessionId $uuid -Project probe -Machine $(hostname) -Role team-architect -Composition custom-agent -Tier project 3>&1 2>&1
$exit2 = $LASTEXITCODE
$env:PATH = $origPath
$out2str = ($out2 | Out-String)
Write-Host ('  record-seat exit = {0}' -f $exit2)
Write-Host '  --- warning emitted ---'
Write-Host $out2str
$b2_hasResMsg  = $out2str -match 'PATH/RESOLUTION failure'
$b2_hasWslNote = $out2str -match 'is NOT git-bash and is intentionally skipped'
$b2_hasBwErr   = $out2str -match 'bw resolved and ran'
$b2_hasBenign  = $out2str -match 'expected on a workspace without the registry ticket'
Write-Host ('  bucket2 asserts: PATH/RESOLUTION msg={0}, WSL-skip note={1}, NOT bw-error={2}, NOT benign={3}, exit1={4}' -f `
  $b2_hasResMsg, $b2_hasWslNote, (-not $b2_hasBwErr), (-not $b2_hasBenign), ($exit2 -eq 1))
$bucket2Pass = $b2_hasResMsg -and $b2_hasWslNote -and (-not $b2_hasBwErr) -and (-not $b2_hasBenign) -and ($exit2 -eq 1)

Write-Host ''
Write-Host '########## P6(b) BUCKET 3 — bw-error (genuinely-erroring attach: invalid ticket id) ##########'
# Full real PATH (bw resolvable directly or via git-bash). Drive a genuine bw error via an
# invalid ticket id (confirmed exit 1 on bw 0.13.1). bucket 3 = $bwExit non-zero.
$uuid3 = [guid]::NewGuid().ToString()
$out3 = & $rec -Seat probeBwErr -Name probeBwErr -SessionId $uuid3 -Project probe -Machine $(hostname) -Role team-architect -Composition custom-agent -Tier project -Ticket 'not a valid id!!!' 3>&1 2>&1
$exit3 = $LASTEXITCODE
$out3str = ($out3 | Out-String)
Write-Host ('  record-seat exit = {0}' -f $exit3)
Write-Host '  --- warning emitted ---'
Write-Host $out3str
$b3_hasBwErr   = $out3str -match "bw attach to 'not a valid id!!!' exited"
$b3_hasAutoNote= $out3str -match 'may AUTO-CREATE'
$b3_hasResMsg  = $out3str -match 'PATH/RESOLUTION failure'
Write-Host ('  bucket3 asserts: bw-error msg={0}, auto-create NOTE={1}, NOT resolution msg={2}, exit1={3}' -f `
  $b3_hasBwErr, $b3_hasAutoNote, (-not $b3_hasResMsg), ($exit3 -eq 1))
$bucket3Pass = $b3_hasBwErr -and $b3_hasAutoNote -and (-not $b3_hasResMsg) -and ($exit3 -eq 1)

Write-Host ''
Write-Host '########## P6(b) DISTINCTNESS ##########'
$distinct = $bucket2Pass -and $bucket3Pass -and ($b2_hasResMsg -ne $b3_hasResMsg) -and ($b2_hasBwErr -ne $b3_hasBwErr)
Write-Host ('  bucket2 (resolution-failure) PASS = {0}' -f $bucket2Pass)
Write-Host ('  bucket3 (bw-error)          PASS = {0}' -f $bucket3Pass)
Write-Host ('  buckets distinct            = {0}' -f $distinct)
if ($bucket2Pass -and $bucket3Pass -and $distinct) { Write-Host 'P6(b) PASS' } else { Write-Host 'P6(b) FAIL' }
