# Arc 68 (stoa--pk4) — P4 composition round-trip through the NEW resolution (record-seat.ps1 changed).
# One real record-seat.ps1 call with the DC4 fields -> read back -> assert composition/gauntlet/
# chain_role round-trip; then idempotent re-record (same seat+machine REPLACES, never dups).
# Runs under the REAL WSL-shadow fallback (bw stripped from pwsh PATH) so P4 also re-confirms the
# DC4 fields survive the rev3 resolution path, not just the direct-bw fast path.

$ErrorActionPreference = 'Stop'
$repo = 'C:\Users\denso\claude_projects\the-stoa\.claude\worktrees\arc-68-build'
$rec  = Join-Path $repo 'substrate\skills\team-launcher\record-seat.ps1'
$origPath = $env:PATH

# Force the fallback (strip bw dir) + WSL shadow present — same real env as P6(a).
$stripped = ($env:PATH -split ';') | Where-Object { $_ -and ($_ -notlike '*denso\bin*') }
$env:PATH = 'C:\windows\system32;' + ($stripped -join ';')

$uuid = [guid]::NewGuid().ToString()
Write-Host '########## P4 — first record (DC4 fields) ##########'
& $rec -Seat probeP4 -Name probeP4 -SessionId $uuid -Project probe -Machine $(hostname) `
  -Role team-architect -Composition 'custom-agent+workflow' -Gauntlet 'waived:probe-test' -ChainRole 'team-architect' -Tier project
$e1 = $LASTEXITCODE
Write-Host ("  exit = {0}" -f $e1)

$row = git show beadwork:attachments/stoa--reg/seat-registry.jsonl | ConvertFrom-Json | Where-Object { $_.seat -eq 'probeP4' }
Write-Host '  --- row read back ---'
$row | ConvertTo-Json -Compress
$f_comp  = $row.composition -eq 'custom-agent+workflow'
$f_gaunt = $row.gauntlet    -eq 'waived:probe-test'
$f_chain = $row.chain_role  -eq 'team-architect'
Write-Host ("  composition round-trip={0}, gauntlet round-trip={1}, chain_role round-trip={2}" -f $f_comp,$f_gaunt,$f_chain)

Write-Host ''
Write-Host '########## P4 — idempotent re-record (same seat+machine) ##########'
$countBefore = (git show beadwork:attachments/stoa--reg/seat-registry.jsonl | ConvertFrom-Json | Where-Object { $_.seat -eq 'probeP4' } | Measure-Object).Count
& $rec -Seat probeP4 -Name probeP4 -SessionId $uuid -Project probe -Machine $(hostname) `
  -Role team-architect -Composition 'standard' -Gauntlet 'required' -ChainRole 'orchestrator' -Tier project
$e2 = $LASTEXITCODE
$rows2 = git show beadwork:attachments/stoa--reg/seat-registry.jsonl | ConvertFrom-Json | Where-Object { $_.seat -eq 'probeP4' }
$countAfter = ($rows2 | Measure-Object).Count
$f_idem = ($countAfter -eq 1)
$f_replaced = ($rows2.composition -eq 'standard' -and $rows2.chain_role -eq 'orchestrator')
Write-Host ("  rows before re-record={0}, after={1} (must stay 1)" -f $countBefore, $countAfter)
Write-Host ("  re-record REPLACED fields (composition=standard, chain_role=orchestrator): {0}" -f $f_replaced)

$env:PATH = $origPath
Write-Host ''
$p4pass = ($e1 -eq 0) -and $f_comp -and $f_gaunt -and $f_chain -and ($e2 -eq 0) -and $f_idem -and $f_replaced
if ($p4pass) { Write-Host 'P4 PASS' } else { Write-Host 'P4 FAIL' }
