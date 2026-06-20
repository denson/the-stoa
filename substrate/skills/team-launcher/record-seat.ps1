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
.PARAMETER Composition
  Arc 68 (stoa--pk4, DC4): the team composition this seat belongs to — one of
  'standard' | 'custom-agent' | 'custom-workflow' | 'custom-agent+workflow'.
  Optional; defaults to 'standard' so every existing caller writes a valid row.
.PARAMETER Gauntlet
  Arc 68 (stoa--pk4, DC4): the gauntlet posture at launch — 'required' (default)
  or 'waived:<reason>' (set by the launcher's -GauntletWaiver flag, a POLYBIUS/
  PRINCIPAL action; a seat cannot self-grant it). Optional; defaults to 'required'.
.PARAMETER ChainRole
  Arc 68 (stoa--pk4, DC4): this seat's place in the chain — e.g. floor-manager |
  orchestrator | team-architect | workflow-architect. Optional; falls back to $Role.
.PARAMETER Ticket
  Arc 68 (stoa--pk4, C5): the bw ticket the registry is attached to. Defaults to
  'stoa--reg' (the ONE registry). Parameterized so verification can drive a bogus
  ticket to exercise the real attach-failure branch distinctly from the PATH-miss
  branch — every existing caller's behavior is preserved by the default.

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
  [string] $Tier = '',
  # --- Arc 68 (stoa--pk4) DC4 additive fields (all optional, safe defaults) ---
  [string] $Composition = 'standard',
  [string] $Gauntlet    = 'required',
  [string] $ChainRole   = '',
  # --- Arc 68 (stoa--pk4) C5: parameterized registry ticket (default = the ONE registry) ---
  [string] $Ticket      = 'stoa--reg'
)

$ErrorActionPreference = 'Stop'

# C5 (stoa--pk4): the registry ticket is the -Ticket param (default 'stoa--reg').
# Used throughout below ($readPath, the attach, the warning strings) so a probe can
# drive a bogus ticket without editing the script under test.
$ticket    = $Ticket
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
# Arc 68 (stoa--pk4) DC4: composition/gauntlet/chain_role are ADDITIVE optional
# fields on the SAME stoa--reg row-shape (does NOT rebuild the Arc-67 schema).
# chain_role falls back to $Role when not passed; JSONL tolerates older rows that
# omit these keys, so a caller that does not pass them still writes a valid row.
$chainRoleVal = if ([string]::IsNullOrEmpty($ChainRole)) { $Role } else { $ChainRole }
$row = [ordered]@{
  seat        = $Seat
  name        = $Name
  session_id  = if ([string]::IsNullOrEmpty($SessionId)) { $null } else { $SessionId }
  project     = $Project
  machine     = $Machine
  role        = $Role
  tier        = $Tier
  composition = $Composition
  gauntlet    = $Gauntlet
  chain_role  = $chainRoleVal
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

# `bw attach` FAILURE is non-fatal here (defense-in-depth: record-seat.ps1 is ALSO called
# standalone for the consumer desktop self-record path). On a workspace without the stoa--reg
# ticket the attach fails -> Write-Warning + exit non-zero, but WITHOUT an unhandled terminating
# throw (the launcher's try/catch OR a caller's exit-code check then handles it gracefully).
# The SUCCESS path is unchanged: write the row, Write-Host, implicit exit 0.
#
# Arc 68 (stoa--pk4) fix (a) — RESOLVE bw even when it is on the bash PATH only.
# The pre-Arc-68 bug: `& bw` in pwsh threw CommandNotFound on a machine where bw is
# installed under git-bash only (on the bash PATH, not the pwsh PATH); the collapsed
# catch then mis-labeled that total registry-write failure as the benign "no registry
# ticket" case (a fail-OPEN that HID a real failure). The resolution below tries the
# pwsh PATH first, then falls back to git-bash, converting the Windows temp path to a
# git-bash-acceptable POSIX form first. $bwExit distinguishes the three outcomes:
#   0     -> success
#   <N>   -> bw ran but the attach exited non-zero (real attach error / no such ticket)
#   $null -> bw could NOT be resolved any way (a PATH/resolution failure, NOT a missing ticket)
$bwExit = $null
$attachThrew = ''
try {
  $bwCmd = Get-Command bw -ErrorAction SilentlyContinue
  if ($bwCmd) {
    # bw is on the pwsh PATH — invoke it directly.
    & $bwCmd.Source attach $ticket $tmp --name $attachName
    $bwExit = $LASTEXITCODE
  } else {
    # bw NOT on the pwsh PATH — the affected-machine case (bw is on the bash PATH only).
    $bash = Get-Command bash -ErrorAction SilentlyContinue
    if ($bash) {
      # git-bash bw does NOT reliably accept a Windows backslash path (C:\Users\...\Temp\...).
      # Convert $tmp to a git-bash-acceptable POSIX form BEFORE handing it to bash:
      #   cygpath -u is the robust tool when present; else a deterministic C:\ -> /c/ transform.
      $cyg = Get-Command cygpath -ErrorAction SilentlyContinue
      if ($cyg) {
        $tmpBash = (& $cyg.Source -u $tmp).Trim()
      } else {
        # Backslashes -> slashes, then a leading drive letter "C:" -> "/c".
        $tmpBash = $tmp -replace '\\','/' -replace '^([A-Za-z]):', '/$1'
      }
      # r1-robust (stoa--pk4 C1/C4): pass the ticket, the converted path, and the
      # attach-name as POSITIONAL args to `bash -c '<script>' bash "$1" "$2" "$3"`.
      # There is NO string interpolation of the values into the bash script body, so
      # the apostrophe-in-Windows-username case (e.g. C:\Users\O'Brien\...) cannot break
      # the quoting — the safety here is STRUCTURAL (no interpolation), not a quote-wrap
      # that relied on the (false) claim that a Windows path cannot contain a single quote.
      & $bash.Source -c 'bw attach "$1" "$2" --name "$3"' bash $ticket $tmpBash $attachName
      $bwExit = $LASTEXITCODE
    } else {
      # No bw resolvable any way -> distinct from a bw error (stays $null).
      $bwExit = $null
    }
  }
} catch {
  $attachThrew = $_.Exception.Message
}

# Arc 68 (stoa--pk4) fix (b) — fail-LOUD with the REAL error; distinguish the THREE cases
# so a CommandNotFound/PATH-miss can NEVER again hide behind the benign "no registry ticket" label.
$attachOk = $false; $failReason = ''
if ($attachThrew) {
  $failReason = "bw attach threw: $attachThrew"
} elseif ($bwExit -eq 0) {
  $attachOk = $true
} elseif ($null -eq $bwExit) {
  $failReason = "bw NOT FOUND on the pwsh PATH or via bash - this is a PATH/resolution failure, NOT a missing-ticket case. On this machine bw may be on the bash PATH only; the launcher must invoke it pwsh-resolvably (Arc 68 / stoa--pk4)."
} else {
  $failReason = "bw attach to '$ticket' exited $bwExit (e.g. no such ticket on THIS bw store, or a bw error). If '$ticket' genuinely does not exist on this workspace's bw store, this is the benign no-registry-ticket case; otherwise it is a real attach failure."
}
if (-not $attachOk) {
  Write-Warning "record-seat: could not record seat '$Seat' to '$ticket'. $failReason"
  exit 1
}

Write-Host ("recorded seat '{0}' (name {1}, sid {2}, machine {3}) -> {4}" -f $Seat, $Name, $(if($SessionId){$SessionId}else{'<null>'}), $Machine, $readPath) -ForegroundColor Green
