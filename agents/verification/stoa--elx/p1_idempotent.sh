#!/usr/bin/env bash
# P1 — idempotent skip on THIS machine. --check then --dry-run. ZERO mutation.
# Real-key sha256 guard before/after (read-only reads of the real key are permitted).
set -u
WT="C:/Users/denso/claude_projects/the-stoa/.claude/worktrees/arc-75-build"
HELPER="$WT/substrate/bootstrap-bw.sh"

realsha() {
  powershell.exe -NoProfile -ExecutionPolicy Bypass -Command \
    "\$wk=[Microsoft.Win32.Registry]::CurrentUser.OpenSubKey('Environment',\$false); \$v=\$wk.GetValue('Path',\$null,[Microsoft.Win32.RegistryValueOptions]::DoNotExpandEnvironmentNames); \$k=\$wk.GetValueKind('Path'); \$wk.Close(); \$b=[System.Text.Encoding]::Unicode.GetBytes(\$v); \$s=[System.Security.Cryptography.SHA256]::Create().ComputeHash(\$b); \$h=(\$s|ForEach-Object{\$_.ToString('x2')}) -join ''; Write-Output ('REALKEY KIND='+\$k+' LEN='+\$v.Length+' SHA256='+\$h)"
}

echo "===== REAL KEY BEFORE P1 ====="; realsha
echo
echo "######## P1a — bootstrap-bw.sh --check (report only, NO mutation) ########"
bash "$HELPER" --check
echo
echo "######## P1b — bootstrap-bw.sh --dry-run (planned actions, NO mutation) ########"
bash "$HELPER" --dry-run
echo
echo "===== REAL KEY AFTER P1 (MUST be byte-identical to BEFORE) ====="; realsha