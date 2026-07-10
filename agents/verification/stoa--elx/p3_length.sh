#!/usr/bin/env bash
# P3 — composed-length fail-loud (M2 + M4). THROWAWAY key. Trap teardown.
set -u
WT="C:/Users/denso/claude_projects/the-stoa/.claude/worktrees/arc-75-build"
PS1_WIN="$(cygpath -w "$WT/substrate/win_path.ps1")"
KEY="Environment_stoa_test"
DIR='C:\Users\denso\.local\bin'
OTHER='C:\Some\Other\dir'

teardown() {
  powershell.exe -NoProfile -ExecutionPolicy Bypass -Command \
    "try { [Microsoft.Win32.Registry]::CurrentUser.DeleteSubKeyTree('$KEY',\$false) } catch {}; \$g=[Microsoft.Win32.Registry]::CurrentUser.OpenSubKey('$KEY'); Write-Output ('TEARDOWN_GONE=' + (\$null -eq \$g))" 2>/dev/null
}
trap teardown EXIT
readback() {
  powershell.exe -NoProfile -ExecutionPolicy Bypass -Command \
    "\$k=[Microsoft.Win32.Registry]::CurrentUser.OpenSubKey('$KEY',\$false); \$v=\$k.GetValue('Path',\$null,[Microsoft.Win32.RegistryValueOptions]::DoNotExpandEnvironmentNames); \$k.Close(); Write-Output ('RB_VALUE='+\$v)"
}

echo "######## P3 — small ceiling forces composed>ceiling -> fail_length exit 4, NO write ########"
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "[Microsoft.Win32.Registry]::CurrentUser.DeleteSubKeyTree('$KEY',\$false)" >/dev/null 2>&1
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "\$k=[Microsoft.Win32.Registry]::CurrentUser.CreateSubKey('$KEY'); \$k.SetValue('Path','$OTHER',[Microsoft.Win32.RegistryValueKind]::String); \$k.Close()" >/dev/null 2>&1
echo "-- before:"; readback
echo "-- invoke with -Ceiling 10 (composed Machine+;+newUser >> 10):"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$PS1_WIN" -Dir "$DIR" -KeyName "$KEY" -Ceiling 10
echo "EXIT=$?"
echo "-- after (MUST be unchanged — no write on fail_length):"; readback

echo
echo "######## P3 legit half — normal ceiling 4095 appends (write happens) ########"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$PS1_WIN" -Dir "$DIR" -KeyName "$KEY" -Ceiling 4095
echo "EXIT=$?"
echo "-- after (now appended):"; readback

echo
echo "######## P3 wrapper — fail_loud_path routes rc=4 -> GUI manual step, NO write (static) ########"
echo "-- win_ensure_on_path case arm for rc 3/4/5:"
grep -n '3|4|5)' substrate/bootstrap-bw.sh
echo "-- fail_loud_path prints the GUI editor step:"
grep -n 'Edit environment variables\|No change was made\|exit 1' substrate/bootstrap-bw.sh | head -6