#requires -Version 7
<#
.SYNOPSIS
  Launch an agent team in terminals, ready for you to paste each seat's activation
  instructions. Three layouts:
    Panes   (DEFAULT) - side-by-side split panes in ONE Windows Terminal window
    Tabs              - one tab per seat in ONE Windows Terminal window
    Windows           - one separate OS window per seat
  Each session runs:  claude --dangerously-skip-permissions --model <model> --name <seat>
  in the project directory. The seat name is set via claude's -n/--name flag (session
  display name + terminal title); you can also rename in-session with  /rename "<name>".

.DESCRIPTION
  wt syntax verified against Microsoft's Windows Terminal command-line docs + a smoke
  test, 2026-06-04. See the bundled `team-launcher` skill for the full mechanics/gotchas.
    - split-pane -V / --vertical  => side-by-side panes (-H => stacked).
    - ; delimits wt commands; Start-Process launches wt NON-blocking (a bare `wt`/`& wt`
      makes PowerShell wait for the window to close).

  Default seats are in ACTIVATION ORDER (floor-manager FIRST -> left pane / first tab):
    POLYBIUS_the-stoa  <- HUMAN_paste-polybius-the-stoa-init.md
    PLINY_the-stoa     <- HUMAN_paste-pliny-init.md

  Panes/Tabs require Windows Terminal (wt); if absent, falls back to Windows layout.

.EXAMPLE
  ./launch-team.ps1                         # side-by-side panes (default)
.EXAMPLE
  ./launch-team.ps1 -Layout Tabs
.EXAMPLE
  ./launch-team.ps1 -Layout Windows -AutoPaste
.EXAMPLE
  ./launch-team.ps1 -ProjectDir C:\path\to\proj -Seats @(@{Name='POLYBIUS_proj'},@{Name='PLINY_proj'})

.NOTES
  Model: 'opus' is an alias; if rejected, pass -Model 'claude-opus-4-8'.
  -AutoPaste (feed each seat's paste file as the initial prompt) is supported in
  -Layout Windows only; Panes/Tabs open for manual paste.
  Paths/names with SPACES are not quoted by this script — keep them space-free.
#>
param(
  [string]   $ProjectDir = 'C:\Users\denso\claude_projects\the-stoa',
  [string]   $Model      = 'opus',
  [ValidateSet('Panes','Tabs','Windows')]
  [string]   $Layout     = 'Panes',
  [object[]] $Seats      = @(
    @{ Name = 'POLYBIUS_the-stoa'; Paste = 'HUMAN_paste-polybius-the-stoa-init.md' },
    @{ Name = 'PLINY_the-stoa';    Paste = 'HUMAN_paste-pliny-init.md' }
  ),
  [switch]   $AutoPaste,
  [int]      $StaggerSeconds = 4
)

if (-not (Test-Path -LiteralPath $ProjectDir)) { throw "ProjectDir not found: $ProjectDir" }
$claude = Get-Command claude -ErrorAction SilentlyContinue
if (-not $claude) { throw "claude not found on PATH." }
$claudeExe = $claude.Source

$haveWt = [bool](Get-Command wt -ErrorAction SilentlyContinue)
if ($Layout -in @('Panes','Tabs') -and -not $haveWt) {
  Write-Warning "Windows Terminal (wt) not found - falling back to -Layout Windows."
  $Layout = 'Windows'
}
if ($AutoPaste -and $Layout -ne 'Windows') {
  Write-Warning "-AutoPaste is supported only in -Layout Windows; $Layout sessions will open for manual paste."
}

if ($Layout -in @('Panes','Tabs')) {
  # One wt invocation: new-tab for seat 1, then split-pane (Panes) or new-tab (Tabs) for the rest.
  $wtArgs = @()
  $idx = 0
  foreach ($seat in $Seats) {
    $idx++
    $name = [string]$seat.Name
    if ($idx -eq 1) {
      $wtArgs += 'new-tab'
    } elseif ($Layout -eq 'Panes') {
      $wtArgs += @(';', 'split-pane', '-V')      # -V = side-by-side (verified)
    } else {
      $wtArgs += @(';', 'new-tab')
    }
    $wtArgs += @('--title', $name, '--startingDirectory', $ProjectDir,
                 $claudeExe, '--dangerously-skip-permissions', '--model', $Model, '--name', $name)
    Write-Host ("[{0}] {1}  ({2})" -f $idx, $name, $Layout) -ForegroundColor Green
  }
  Start-Process wt -ArgumentList $wtArgs | Out-Null   # non-blocking
}
else {
  # Windows: one pwsh window per seat (supports -AutoPaste).
  $i = 0
  foreach ($seat in $Seats) {
    $i++
    $name  = [string]$seat.Name
    $paste = if ($seat.Paste) { Join-Path $ProjectDir $seat.Paste } else { $null }
    $cmd = "& '$claudeExe' --dangerously-skip-permissions --model $Model --name '$name'"
    if ($AutoPaste -and $paste -and (Test-Path -LiteralPath $paste)) {
      $cmd += " (Get-Content -LiteralPath '$paste' -Raw)"
    } elseif ($AutoPaste) {
      Write-Warning "Seat '$name': paste file missing ($paste) - opening for manual paste."
    }
    $inner = "Set-Location -LiteralPath '$ProjectDir'; $cmd"
    Start-Process pwsh -WorkingDirectory $ProjectDir -ArgumentList '-NoExit','-Command',$inner | Out-Null
    Write-Host ("[{0}] {1}  (Windows{2})" -f $i, $name, $(if($AutoPaste){', auto-paste'}else{''})) -ForegroundColor Green
    if ($i -lt $Seats.Count -and $StaggerSeconds -gt 0) { Start-Sleep -Seconds $StaggerSeconds }
  }
}

Write-Host ''
Write-Host ("Team launched ({0} layout)." -f $Layout) -ForegroundColor Cyan
if (-not ($AutoPaste -and $Layout -eq 'Windows')) {
  Write-Host 'Paste each activation file into its session - floor-manager first (left pane / first tab).' -ForegroundColor Cyan
}
