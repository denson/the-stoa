# VERA P6(a) — FORCE + PROVE the bash-fallback writes a real stoa--reg row
# on a pwsh-bw-unreachable shim. (Arc 68 / stoa--pk4 C1, the load-bearing probe.)
#
# Faithful reproduction of the affected-machine shape "bw reachable to bash, NOT to pwsh":
#   - $env:PATH EXCLUDES the real bw.exe dir (C:\Users\denso\bin) => pwsh
#     Get-Command bw returns $null => record-seat.ps1 takes the bash-FALLBACK branch.
#   - $env:PATH KEEPS the bash + cygpath + git dirs => Get-Command bash/cygpath non-null.
#   - $env:BASH_ENV points at a script that prepends the bw dir to the BASH child's PATH.
#     `bash -c` sources $BASH_ENV for non-interactive shells, so the bash subprocess
#     (and ONLY it) can exec the real bw. This is exactly "bw on the bash PATH only".
$ErrorActionPreference = 'Stop'

$wt = 'C:\Users\denso\claude_projects\the-stoa\.claude\worktrees\arc-68-build'
$record = Join-Path $wt 'substrate\skills\team-launcher\record-seat.ps1'

$bashDir = 'C:\Program Files\Git\usr\bin'      # bash + cygpath
$gitDir  = 'C:\Program Files\Git\mingw64\bin'  # git
$pwshDir = 'C:\Program Files\PowerShell\7'
$origPath    = $env:PATH
$origBashEnv = $env:BASH_ENV
# EXCLUDE C:\Users\denso\bin so pwsh cannot resolve bw.exe.
$env:PATH = "$bashDir;$gitDir;$pwshDir;C:\Windows\System32;C:\Windows"
# Give ONLY the bash child the bw dir (sourced by bash -c via BASH_ENV).
$env:BASH_ENV = 'C:\Users\denso\AppData\Local\Temp\vera-bashenv.sh'

$bwResolved   = Get-Command bw   -ErrorAction SilentlyContinue
$bashResolved = Get-Command bash -ErrorAction SilentlyContinue
$cygResolved  = Get-Command cygpath -ErrorAction SilentlyContinue
Write-Host ("SHIM-STATE: Get-Command bw = {0}; Get-Command bash = {1}; Get-Command cygpath = {2}" -f `
  $(if($bwResolved){"NON-NULL ($($bwResolved.Source)) -- SHIM FAILED"}else{'$null (OK -- pwsh cannot resolve bw)'}), `
  $(if($bashResolved){"NON-NULL (OK)"}else{'$null -- SHIM FAILED'}), `
  $(if($cygResolved){"NON-NULL ($($cygResolved.Source))"}else{'$null'}))

if ($bwResolved)    { $env:PATH = $origPath; $env:BASH_ENV = $origBashEnv; throw 'P6a SHIM FAILED: bw is pwsh-resolvable; probe would pass via the Get-Command branch (invalid).' }
if (-not $bashResolved) { $env:PATH = $origPath; $env:BASH_ENV = $origBashEnv; throw 'P6a SHIM FAILED: bash not resolvable; fallback cannot run.' }

# Prove bash (and ONLY bash) reaches the real bw under the shim.
$bashSeesBw = & $bashResolved.Source -c 'command -v bw 2>/dev/null'
Write-Host ("BASH-SEES-BW: '{0}'  (the bash child resolves bw via BASH_ENV; pwsh does not)" -f $bashSeesBw)

Write-Host "`n--- Running record-seat.ps1 (MUST take the bash-fallback) ---"
Set-Location $wt
& $record -Seat probeFallback -Name probeFallback -SessionId ([guid]::NewGuid().ToString()) `
  -Project probe -Machine $(hostname) -Role team-architect -Composition custom-agent -Tier project
$recordExit = $LASTEXITCODE
Write-Host ("record-seat.ps1 EXIT = {0}" -f $recordExit)

$env:PATH = $origPath
$env:BASH_ENV = $origBashEnv
exit $recordExit
