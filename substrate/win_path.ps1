# win_path.ps1 — registry-safe Windows USER PATH append (Arc 75 / stoa--elx).
#
# The security crux of the bw-bootstrap helper. Reads HKCU\Environment Path via the
# .NET registry API (never reg.exe, never setx), appends $Dir only if absent, preserves
# the original value kind (REG_SZ / REG_EXPAND_SZ and its %tokens%), and gates on the
# EXPANDED composed (Machine + ";" + User) length against the Win10/11 4095-char
# login-truncation cliff. Fails LOUD (non-zero exit, no write) on read failure / length
# breach / any exception — a failed read is NEVER treated as "empty PATH".
#
# Invoked by bootstrap-bw.sh via -File (not -Command):
#   powershell.exe -NoProfile -ExecutionPolicy Bypass -File win_path.ps1 \
#     -Dir <C:\...\.local\bin> -KeyName Environment [-DryRun] -Ceiling 4095
# Exit codes: 0 present/appended/would_append; 3 fail_read; 4 fail_length; 5 fail_exception.
#
# Author: Denson Smith
param([Parameter(Mandatory=$true)][string]$Dir, [string]$KeyName='Environment',
      [int]$Ceiling=4095, [switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = [Microsoft.Win32.Registry]::CurrentUser
try {
  # 1. OPEN the key. Key ABSENT is a READ FAILURE, NOT "empty PATH" (F2).
  $wk = $root.OpenSubKey($KeyName, $true)
  if ($null -eq $wk) { Write-Output 'RESULT=fail_read'; exit 3 }              # FAIL LOUD, no write
  # 2. READ raw (UNEXPANDED) value + kind. $null value = PROVABLY absent (fresh Path) → legit empty.
  $cur = $wk.GetValue('Path', $null, [Microsoft.Win32.RegistryValueOptions]::DoNotExpandEnvironmentNames)
  if ($null -eq $cur) { $cur=''; $kind=[Microsoft.Win32.RegistryValueKind]::ExpandString }
  else { $kind = $wk.GetValueKind('Path') }                                   # PRESERVE original type
  # 3. IDEMPOTENT-ABSENT check — per-entry, case-insensitive, trailing-\ tolerant, AND token-expanded
  #    (F8: a REG_EXPAND_SZ entry stored as %USERPROFILE%\.local\bin must match the expanded $Dir).
  $dExp = [System.Environment]::ExpandEnvironmentVariables($Dir).TrimEnd('\')
  $present = $false
  foreach ($e in ($cur -split ';')) {
    if ($e.Trim() -eq '') { continue }
    $eRaw = $e.Trim().TrimEnd('\')
    $eExp = [System.Environment]::ExpandEnvironmentVariables($e.Trim()).TrimEnd('\')
    if (($eRaw -ieq $Dir.TrimEnd('\')) -or ($eExp -ieq $dExp)) { $present = $true }
  }
  if ($present) { $wk.Close(); Write-Output 'RESULT=present'; exit 0 }        # idempotent no-op
  # 4. BUILD new user value (our segment is a LITERAL absolute path — safe under either kind).
  $newUser = if ($cur -eq '') { $Dir } else { $cur.TrimEnd(';') + ';' + $Dir }
  # 5. COMPOSED length gate (F3): Machine + ";" + newUser, EXPANDED, vs the Win10/11 4095 cliff.
  $m = [System.Environment]::GetEnvironmentVariable('Path','Machine'); if ($null -eq $m) { $m='' }
  $composed = [System.Environment]::ExpandEnvironmentVariables("$m;$newUser")
  if ($composed.Length -gt $Ceiling) { $wk.Close(); Write-Output "RESULT=fail_length composed=$($composed.Length)"; exit 4 }
  # 6. WRITE preserving kind (or report in dry-run). reg-add-class semantics; no %PATH% expansion.
  if ($DryRun) { $wk.Close(); Write-Output "RESULT=would_append kind=$kind"; exit 0 }
  $wk.SetValue('Path', $newUser, $kind)
  $wk.Close()
  Write-Output 'RESULT=appended'; exit 0
} catch { Write-Output "RESULT=fail_exception $($_.Exception.Message)"; exit 5 }
finally { if ($null -ne $wk) { $wk.Close() } }
