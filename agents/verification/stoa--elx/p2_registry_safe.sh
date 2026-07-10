#!/usr/bin/env bash
# P2 — registry-safe append, THROWAWAY key, driving the SHIPPED substrate/win_path.ps1.
# HARD SAFETY: KeyName=Environment_stoa_test ONLY. Trap teardown ALWAYS deletes it.
set -u
WT="C:/Users/denso/claude_projects/the-stoa/.claude/worktrees/arc-75-build"
PS1_POSIX="$WT/substrate/win_path.ps1"
PS1_WIN="$(cygpath -w "$PS1_POSIX")"
KEY="Environment_stoa_test"
DIR='C:\Users\denso\.local\bin'          # the real dir (never written to the REAL Environment key here)
OTHER='C:\Some\Other\dir'

teardown() {
  powershell.exe -NoProfile -ExecutionPolicy Bypass -Command \
    "try { [Microsoft.Win32.Registry]::CurrentUser.DeleteSubKeyTree('$KEY',\$false) } catch {}; \$g = [Microsoft.Win32.Registry]::CurrentUser.OpenSubKey('$KEY'); Write-Output ('TEARDOWN_GONE=' + (\$null -eq \$g))" 2>/dev/null
}
trap teardown EXIT

# seed KEY with a Path value of a given kind. $1=value $2=kind(String|ExpandString)
seed() {
  powershell.exe -NoProfile -ExecutionPolicy Bypass -Command \
    "\$k=[Microsoft.Win32.Registry]::CurrentUser.CreateSubKey('$KEY'); \$k.SetValue('Path','$1',[Microsoft.Win32.RegistryValueKind]::$2); \$k.Close()" >/dev/null 2>&1
}
# read back RAW (unexpanded) value + kind.
readback() {
  powershell.exe -NoProfile -ExecutionPolicy Bypass -Command \
    "\$k=[Microsoft.Win32.Registry]::CurrentUser.OpenSubKey('$KEY',\$false); if (\$null -eq \$k){Write-Output 'RB_ABSENT'; exit} \$v=\$k.GetValue('Path',\$null,[Microsoft.Win32.RegistryValueOptions]::DoNotExpandEnvironmentNames); \$kd=\$k.GetValueKind('Path'); \$k.Close(); Write-Output ('RB_KIND='+\$kd+' RB_VALUE='+\$v)"
}
run() { # $@ passed to win_path.ps1
  powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$PS1_WIN" "$@"
  echo "EXIT=$?"
}

echo "######## P2(a) absent-dir seed (REG_SZ) -> expect appended once, exit 0 ########"
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "[Microsoft.Win32.Registry]::CurrentUser.DeleteSubKeyTree('$KEY',\$false)" >/dev/null 2>&1
seed "$OTHER" String
echo "-- before:"; readback
echo "-- invoke shipped win_path.ps1:"; run -Dir "$DIR" -KeyName "$KEY" -Ceiling 4095
echo "-- after:"; readback

echo
echo "######## P2(b) present-dir seed -> expect present, NO write, exit 0 ########"
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "[Microsoft.Win32.Registry]::CurrentUser.DeleteSubKeyTree('$KEY',\$false)" >/dev/null 2>&1
seed "$OTHER;$DIR" String
echo "-- before:"; readback
echo "-- invoke:"; run -Dir "$DIR" -KeyName "$KEY" -Ceiling 4095
echo "-- after (must equal before):"; readback

echo
echo "######## P2(c) REG_EXPAND_SZ seed w/ %USERPROFILE% token, append absent dir -> kind+token preserved ########"
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "[Microsoft.Win32.Registry]::CurrentUser.DeleteSubKeyTree('$KEY',\$false)" >/dev/null 2>&1
seed '%USERPROFILE%\Documents' ExpandString
echo "-- before:"; readback
echo "-- invoke (append $DIR):"; run -Dir "$DIR" -KeyName "$KEY" -Ceiling 4095
echo "-- after (kind must stay ExpandString, %USERPROFILE% token intact + ;$DIR appended):"; readback

echo
echo "######## P2(d) token-form-stored entry, expanded -Dir -> present, NO double-append (F8) ########"
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "[Microsoft.Win32.Registry]::CurrentUser.DeleteSubKeyTree('$KEY',\$false)" >/dev/null 2>&1
seed '%USERPROFILE%\.local\bin' ExpandString
echo "-- before:"; readback
echo "-- invoke with expanded -Dir=$DIR (should match the token form):"; run -Dir "$DIR" -KeyName "$KEY" -Ceiling 4095
echo "-- after (must be unchanged — no double-append):"; readback

echo
echo "######## P2(e)/P2b key ABSENT / read failure -> RESULT=fail_read exit 3, NO write ########"
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "[Microsoft.Win32.Registry]::CurrentUser.DeleteSubKeyTree('Environment_stoa_test_absent',\$false)" >/dev/null 2>&1
echo "-- invoke against a never-created key:"; run -Dir "$DIR" -KeyName "Environment_stoa_test_absent" -Ceiling 4095
echo "-- confirm the absent key was NOT created by the run:"
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "\$k=[Microsoft.Win32.Registry]::CurrentUser.OpenSubKey('Environment_stoa_test_absent'); Write-Output ('ABSENT_KEY_STILL_ABSENT=' + (\$null -eq \$k))"
