#requires -Version 7
<#
.SYNOPSIS
  Launch a Stoa agent team (POLYBIUS + PLINY by default) in terminals — consumer-generic.
  Derives the project dir + slug from where it is deployed, so it works in ANY workspace
  with no editing. Defaults to SAY-TRIGGER activation: each pane is pre-seeded with the bare
  word ("polybius" / "pliny") so the workspace CLAUDE.md auto-loads the role.

  Layouts:
    Panes   (DEFAULT) - side-by-side split panes in ONE Windows Terminal window
    Tabs              - one tab per seat in ONE Windows Terminal window
    Windows           - one separate OS window per seat (no wt needed; fallback target)

  Each session runs:  claude --dangerously-skip-permissions --model <model> --name <seat> [<say-word>]

.DESCRIPTION
  stoa--h8w: this is the consumer-generic successor to the the-stoa-specific root launcher.
  It ships INSIDE the team-launcher skill subtree so install.sh deploys it to every workspace.

  Project + slug resolution (when -ProjectDir is not passed): walk up from this script's
  location to the first ancestor containing a `.claude/` dir (the workspace root). Slug
  defaults to that dir's leaf name (e.g. `origindex` -> seats POLYBIUS_origindex / PLINY_origindex).

  Activation:
    say   (DEFAULT) - pre-seed the bare word ("polybius"/"pliny") as claude's positional prompt;
                      the workspace CLAUDE.md say-trigger loads the role. Works in all layouts.
    paste           - open sessions ready for a manual activation paste (the-stoa-style). With
                      -AutoPaste + -Layout Windows, feeds each seat's Paste file as the first prompt.

  wt mechanics verified against Microsoft's Windows Terminal docs + smoke test (2026-06-04):
    split-pane -V => side-by-side; ';' delimits wt commands; Start-Process => non-blocking.

.EXAMPLE
  ./launch-team.ps1                  # panes, say-trigger, project+slug auto-derived
.EXAMPLE
  ./launch-team.ps1 -Layout Tabs
.EXAMPLE
  ./launch-team.ps1 -DryRun          # print the wt/pwsh command without opening anything
.EXAMPLE
  ./launch-team.ps1 -ProjectDir C:\path\to\proj -Slug proj
.EXAMPLE
  ./launch-team.ps1 -Activation paste -Layout Windows -AutoPaste

.NOTES
  Model: 'opus' is an alias; if rejected, pass -Model 'claude-opus-4-8'.
  Paths/names with SPACES are not quoted by this script — keep them space-free.
  If a pane's say-trigger pre-seed ever misfires, the pane is still named + in the project dir
  at a ready claude prompt — just type the bare word yourself.
  Seat-name scheme (POLYBIUS_<slug>) is interim; adopt the formal Role_Project_Instance id when
  stoa--p7c lands.
#>
param(
  [string]   $ProjectDir,
  [string]   $Slug,
  [string]   $Model      = 'opus',
  [ValidateSet('Panes','Tabs','Windows')]
  [string]   $Layout     = 'Panes',
  [ValidateSet('say','paste')]
  [string]   $Activation = 'say',
  [object[]] $Seats,
  [switch]   $AutoPaste,
  [switch]   $DryRun,
  [int]      $StaggerSeconds = 4
)

# --- Resolve the project dir: param, else walk up from the script to the workspace root ---
if (-not $ProjectDir) {
  $d = $PSScriptRoot
  while ($d -and -not (Test-Path -LiteralPath (Join-Path $d '.claude'))) {
    $parent = Split-Path $d -Parent
    if ($parent -eq $d) { $d = $null; break }
    $d = $parent
  }
  $ProjectDir = if ($d) { $d } else { (Get-Location).Path }
}
if (-not (Test-Path -LiteralPath $ProjectDir)) { throw "ProjectDir not found: $ProjectDir" }
$ProjectDir = (Resolve-Path -LiteralPath $ProjectDir).Path

# --- Slug (seat suffix / titles): param, else the project dir leaf ---
if (-not $Slug) { $Slug = Split-Path $ProjectDir -Leaf }

# --- claude on PATH ---
$claude = Get-Command claude -ErrorAction SilentlyContinue
if (-not $claude) { throw "claude not found on PATH." }
$claudeExe = $claude.Source

# --- Default seats from slug + activation (floor-manager FIRST) ---
if (-not $Seats) {
  if ($Activation -eq 'say') {
    $Seats = @(
      @{ Name = "POLYBIUS_$Slug"; Say = 'polybius' },
      @{ Name = "PLINY_$Slug";    Say = 'pliny' }
    )
  } else {
    $Seats = @(
      @{ Name = "POLYBIUS_$Slug" },
      @{ Name = "PLINY_$Slug" }
    )
  }
}

# --- wt availability + fallback ---
$haveWt = [bool](Get-Command wt -ErrorAction SilentlyContinue)
if ($Layout -in @('Panes','Tabs') -and -not $haveWt) {
  Write-Warning "Windows Terminal (wt) not found - falling back to -Layout Windows."
  $Layout = 'Windows'
}
if ($AutoPaste -and $Layout -ne 'Windows') {
  Write-Warning "-AutoPaste is supported only in -Layout Windows; $Layout opens for manual paste."
}

function Get-SeatPrompt($seat) {
  if ($Activation -eq 'say' -and $seat.Say) { return [string]$seat.Say }
  return $null
}

if ($Layout -in @('Panes','Tabs')) {
  # One wt invocation: new-tab for seat 1, then split-pane (Panes) / new-tab (Tabs) for the rest.
  $wtArgs = @()
  $idx = 0
  foreach ($seat in $Seats) {
    $idx++
    $name = [string]$seat.Name
    if ($idx -eq 1) { $wtArgs += 'new-tab' }
    elseif ($Layout -eq 'Panes') { $wtArgs += @(';', 'split-pane', '-V') }
    else { $wtArgs += @(';', 'new-tab') }
    $wtArgs += @('--title', $name, '--startingDirectory', $ProjectDir,
                 $claudeExe, '--dangerously-skip-permissions', '--model', $Model, '--name', $name)
    $p = Get-SeatPrompt $seat
    if ($p) { $wtArgs += $p }   # positional bare-word prompt = say-trigger activation
    Write-Host ("[{0}] {1}  ({2}{3})" -f $idx, $name, $Layout, $(if($p){", say:'$p'"}else{''})) -ForegroundColor Green
  }
  if ($DryRun) {
    Write-Host ("[dry-run] wt {0}" -f ($wtArgs -join ' ')) -ForegroundColor Yellow
  } else {
    Start-Process wt -ArgumentList $wtArgs | Out-Null   # non-blocking
  }
}
else {
  # Windows: one pwsh window per seat (supports -AutoPaste in paste mode).
  $i = 0
  foreach ($seat in $Seats) {
    $i++
    $name = [string]$seat.Name
    $cmd  = "& '$claudeExe' --dangerously-skip-permissions --model $Model --name '$name'"
    $p = Get-SeatPrompt $seat
    if ($p) {
      $cmd += " '$p'"
    } elseif ($AutoPaste -and $seat.Paste) {
      $paste = Join-Path $ProjectDir $seat.Paste
      if (Test-Path -LiteralPath $paste) { $cmd += " (Get-Content -LiteralPath '$paste' -Raw)" }
      else { Write-Warning "Seat '$name': paste file missing ($paste) - opening for manual paste." }
    }
    $inner = "Set-Location -LiteralPath '$ProjectDir'; $cmd"
    if ($DryRun) {
      Write-Host ("[dry-run] pwsh -NoExit -Command: {0}" -f $inner) -ForegroundColor Yellow
    } else {
      Start-Process pwsh -WorkingDirectory $ProjectDir -ArgumentList '-NoExit','-Command',$inner | Out-Null
      if ($i -lt $Seats.Count -and $StaggerSeconds -gt 0) { Start-Sleep -Seconds $StaggerSeconds }
    }
    Write-Host ("[{0}] {1}  (Windows{2})" -f $i, $name, $(if($p){", say:'$p'"}else{''})) -ForegroundColor Green
  }
}

Write-Host ''
Write-Host ("Team launched ({0} layout, project '{1}')." -f $Layout, $Slug) -ForegroundColor Cyan
if ($Activation -eq 'say') {
  Write-Host 'Say-trigger: each pane was pre-seeded its bare word; the workspace CLAUDE.md auto-loads the role (floor-manager = left pane / first tab). If one did not fire, type the word yourself.' -ForegroundColor Cyan
} else {
  Write-Host 'Paste each activation file into its session - floor-manager first (left pane / first tab).' -ForegroundColor Cyan
}
