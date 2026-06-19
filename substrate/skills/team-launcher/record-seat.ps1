#requires -Version 7
<#
.SYNOPSIS
  Record (or refresh) one seat row in the durable Stoa seat registry (stoa--p7c / Arc 67, DC2).

.DESCRIPTION
  The registry is a JSONL manifest attached on the `beadwork` branch at
  `attachments/stoa--reg/seat-registry.jsonl` — one JSON object per line, one row per active seat.
  This helper performs a read-modify-rewrite-attach:
    1. `git show beadwork:attachments/stoa--reg/seat-registry.jsonl` -> the current manifest
       (empty if the attachment does not yet exist).
    2. Drop any existing line whose (seat, machine) matches the seat being recorded (idempotent
       re-record / liveness refresh — re-recording a seat REPLACES its row, never appends a dup).
    3. Append the new JSON row to a temp file (existing rows preserved verbatim).
    4. `bw attach stoa--reg <temp> --name seat-registry.jsonl` (overwrites the stored path; commits
       to beadwork with a single-line intent).

  Callable STANDALONE, without spawning a live agent session:
    - the launcher calls it per seat after a launch (terminal path; it minted the SessionId);
    - a desktop seat calls it on activation with its `$CLAUDE_CODE_SESSION_ID`-discovered sid
      (the self-record fallback — see the team-launcher SKILL.md);
    - VERA calls it directly with a synthetic row to exercise the real round-trip (probe P3).

  Identity/signing convention for the recorded seats: `operating-disciplines.md` §28.9.

.PARAMETER Seat
  The canonical ROLE_slug mnemonic (the `[for:]` routing address), e.g. POLYBIUS_the-stoa.
.PARAMETER Name
  The human-friendly, space-free, non-unique display name, e.g. Polybius_the_Stoa.
.PARAMETER SessionId
  The per-machine session-id (the unique handle). May be empty for a not-yet-discovered seat.
.PARAMETER Project
  Project slug, e.g. the-stoa.
.PARAMETER Machine
  Hostname (disambiguates per-machine ids).
.PARAMETER Role
  Free-form role label, e.g. floor-manager / orchestrator.
.PARAMETER Tier
  Tier label, e.g. project / user.

.EXAMPLE
  ./record-seat.ps1 -Seat POLYBIUS_the-stoa -Name Polybius_the_Stoa `
    -SessionId 88cd8c37-f3ff-4904-9b0e-efafaad48f70 -Project the-stoa `
    -Machine $(hostname) -Role floor-manager -Tier project
#>
param(
  [Parameter(Mandatory)] [string] $Seat,
  [Parameter(Mandatory)] [string] $Name,
  [string] $SessionId,
  [Parameter(Mandatory)] [string] $Project,
  [Parameter(Mandatory)] [string] $Machine,
  [string] $Role = '',
  [string] $Tier = ''
)

$ErrorActionPreference = 'Stop'

$ticket    = 'stoa--reg'
# `bw attach <id> <file> --name <attachName>` stores bytes at attachments/<id>/<attachName>.
# So --name is the path-UNDER-attachments/<id>/ (just the filename here); the full read path
# on the beadwork branch is attachments/<id>/<attachName>. Do NOT pass the full attachments/...
# path as --name or it doubles (attachments/<id>/attachments/<id>/<file>).
$attachName = 'seat-registry.jsonl'
$readPath   = "attachments/$ticket/$attachName"

# --- 1. Read the current manifest from the beadwork branch (empty if absent) ---
# `git show` exits non-zero if the path does not exist on the branch; treat that as "no manifest yet".
$current = & git show "beadwork:$readPath" 2>$null
if ($LASTEXITCODE -ne 0) { $current = @() }

# Normalize to an array of non-empty trimmed lines.
$lines = @()
if ($current) {
  $lines = @($current) | ForEach-Object { $_ } | Where-Object { $_ -ne $null -and ([string]$_).Trim().Length -gt 0 }
}

# --- 2. Drop any existing row matching (seat, machine) — idempotent replace ---
$kept = @()
foreach ($line in $lines) {
  $keep = $true
  try {
    $obj = $line | ConvertFrom-Json -ErrorAction Stop
    if ($obj.seat -eq $Seat -and $obj.machine -eq $Machine) { $keep = $false }
  } catch {
    # Unparseable line: keep it verbatim (do not silently discard foreign content).
    $keep = $true
  }
  if ($keep) { $kept += $line }
}

# --- 3. Build the new row + append ---
$row = [ordered]@{
  seat        = $Seat
  name        = $Name
  session_id  = if ([string]::IsNullOrEmpty($SessionId)) { $null } else { $SessionId }
  project     = $Project
  machine     = $Machine
  role        = $Role
  tier        = $Tier
  launched_at = [DateTime]::UtcNow.ToString('yyyy-MM-ddTHH:mm:ssZ')
  status      = 'alive'
}
$newLine = ($row | ConvertTo-Json -Compress -Depth 4)
$kept += $newLine

# --- 4. Write to a temp file + attach (overwrites the stored path; commits to beadwork) ---
# Fixed-name temp file (no $VAR in any destructive op); the attach overwrites the stored path verbatim.
$tmp = Join-Path ([System.IO.Path]::GetTempPath()) "stoa-seat-registry.jsonl"
# Join with `\n` and a trailing newline; write UTF8-no-BOM so the JSONL stays clean.
$content = ($kept -join "`n") + "`n"
[System.IO.File]::WriteAllText($tmp, $content, (New-Object System.Text.UTF8Encoding($false)))

& bw attach $ticket $tmp --name $attachName
if ($LASTEXITCODE -ne 0) { throw "bw attach failed for $ticket ($readPath); seat '$Seat' not recorded." }

Write-Host ("recorded seat '{0}' (name {1}, sid {2}, machine {3}) -> {4}" -f $Seat, $Name, $(if($SessionId){$SessionId}else{'<null>'}), $Machine, $readPath) -ForegroundColor Green
