# Arc 68 (stoa--pk4) — P6/P4 CLEANUP: restore stoa--reg to EXACT baseline (2 real rows).
# Read-modify-rewrite-attach: keep only the rows whose seat is NOT a probe seat, write them
# back verbatim, re-attach via the same git-bash fallback (bw not on this Bash-tool pwsh PATH
# only if stripped; here bw IS on PATH so attach goes direct — either path overwrites the same
# stored attachment). Then assert the registry sha256 == baseline.

$ErrorActionPreference = 'Stop'
$baselineSha = 'f29a2166371cd31d1ba8646ffe282e6e69c712d31d17bd71b581c79d80465e97'
$probeSeats = @('probeFallback','probeP4','probeResFail','probeBwErr')

$current = git show beadwork:attachments/stoa--reg/seat-registry.jsonl
$lines = @($current) | Where-Object { $_ -and ([string]$_).Trim().Length -gt 0 }
$kept = @()
foreach ($l in $lines) {
  $obj = $l | ConvertFrom-Json
  if ($probeSeats -notcontains $obj.seat) { $kept += $l }
}
Write-Host ("  rows kept (must be 2 real rows): {0}" -f $kept.Count)
$kept | ForEach-Object { Write-Host ("    | " + (($_ | ConvertFrom-Json).seat)) }

$tmp = Join-Path ([System.IO.Path]::GetTempPath()) 'stoa-seat-registry-cleanup.jsonl'
$content = ($kept -join "`n") + "`n"
[System.IO.File]::WriteAllText($tmp, $content, (New-Object System.Text.UTF8Encoding($false)))

bw attach stoa--reg $tmp --name seat-registry.jsonl
Write-Host ("  re-attach exit = {0}" -f $LASTEXITCODE)
Remove-Item $tmp -ErrorAction SilentlyContinue

Write-Host ''
Write-Host '########## VERIFY baseline restored ##########'
$after = git show beadwork:attachments/stoa--reg/seat-registry.jsonl
$afterSha = ($after -join "`n") + "`n"  # not used for sha; use raw bytes below
$rawSha = (git show beadwork:attachments/stoa--reg/seat-registry.jsonl | Out-String)
# compute sha256 over the actual stored bytes
$bytes = [System.Text.Encoding]::UTF8.GetBytes((($after -join "`n") + "`n"))
$sha = [System.BitConverter]::ToString((New-Object System.Security.Cryptography.SHA256Managed).ComputeHash($bytes)).Replace('-','').ToLower()
Write-Host ("  reconstructed sha256 = {0}" -f $sha)
Write-Host ("  baseline       sha256 = {0}" -f $baselineSha)
Write-Host ("  rows now: {0}" -f (@($after) | Where-Object {$_ -and $_.Trim()}).Count)
$after | ForEach-Object { Write-Host ("    | " + (($_ | ConvertFrom-Json).seat)) }
