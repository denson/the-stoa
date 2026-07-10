#!/usr/bin/env bash
# P7 — install.sh absent-flag byte-unchanged (DC6 / rev3 N4) across user|project|subproject
# + the no-target pre-flight-ordering probe. Pre-arc baseline from git show cfd683d7.
set -u
WT="C:/Users/denso/claude_projects/the-stoa/.claude/worktrees/arc-75-build"
SUB="$WT/substrate"
BUILT="$SUB/install.sh"
# Stage pre-arc install.sh in the SAME dir so SCRIPT_DIR resolves identically (fair byte-diff).
PREARC="$SUB/install.prearc.$$.sh"
git -C "$WT" show cfd683d7:substrate/install.sh > "$PREARC"
cleanup() { rm -f "$PREARC"; }
trap cleanup EXIT

PROJDIR="$(mktemp -d)"; PARENTDIR="$(mktemp -d)"; mkdir -p "$PARENTDIR/.claude"

echo "===== pre-arc baseline SHA: $(git -C "$WT" show cfd683d7:substrate/install.sh | sha256sum | cut -c1-16) ====="
run_diff() {
  local label="$1"; shift
  local a b
  a="$(bash "$PREARC" "$@" 2>&1)"
  b="$(bash "$BUILT" "$@" 2>&1)"
  if [ "$a" = "$b" ]; then
    echo "  [$label] BYTE-IDENTICAL ($(printf '%s' "$b" | wc -l) lines)"
  else
    echo "  [$label] !!! DIFF:"
    diff <(printf '%s' "$a") <(printf '%s' "$b") | head -40
  fi
}

echo "===== absent-flag --dry-run byte-unchanged across all 3 targets ====="
run_diff "user"       --target user --dry-run
run_diff "project"    --target project --project-dir "$PROJDIR" --dry-run
run_diff "subproject" --target subproject --parent-dir "$PARENTDIR" --subproject veraprobe --dry-run

echo
echo "===== no-target probe: --bootstrap-bw with NO --target -> errors on target-required, pre-flight does NOT fire ====="
# real-key sha256 guard around it
before="$(powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "\$wk=[Microsoft.Win32.Registry]::CurrentUser.OpenSubKey('Environment',\$false); \$v=\$wk.GetValue('Path',\$null,[Microsoft.Win32.RegistryValueOptions]::DoNotExpandEnvironmentNames); \$wk.Close(); \$b=[System.Text.Encoding]::Unicode.GetBytes(\$v); (([System.Security.Cryptography.SHA256]::Create().ComputeHash(\$b)|ForEach-Object{\$_.ToString('x2')}) -join '')")"
out="$(bash "$BUILT" --bootstrap-bw --dry-run 2>&1)"; rc=$?
echo "  exit=$rc"
echo "  output:"; printf '%s\n' "$out" | sed 's/^/    /'
echo "  contains 'target is required'? $(printf '%s' "$out" | grep -qi 'target is required' && echo YES || echo NO)"
echo "  pre-flight fired (any [bootstrap-bw] line)? $(printf '%s' "$out" | grep -q '\[bootstrap-bw\]' && echo 'YES (BAD)' || echo 'NO (correct — pre-flight sits after the target check)')"
after="$(powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "\$wk=[Microsoft.Win32.Registry]::CurrentUser.OpenSubKey('Environment',\$false); \$v=\$wk.GetValue('Path',\$null,[Microsoft.Win32.RegistryValueOptions]::DoNotExpandEnvironmentNames); \$wk.Close(); \$b=[System.Text.Encoding]::Unicode.GetBytes(\$v); (([System.Security.Cryptography.SHA256]::Create().ComputeHash(\$b)|ForEach-Object{\$_.ToString('x2')}) -join '')")"
echo "  real-key sha256 unchanged? $([ "$before" = "$after" ] && echo YES || echo 'NO (MUTATION!)')"
rm -rf "$PROJDIR" "$PARENTDIR"