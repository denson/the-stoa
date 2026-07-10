#!/usr/bin/env bash
# P4 — DC3 false-green discrimination (M3; F5 fixture; rev3 N3 POSIX export).
# This machine is now TRUE-GREEN for 'bw' (bw.cmd in .local\bin is on the registry PATH),
# so a literal-'bw' naive-vs-correct both exit 0 — the false-green state the design assumed
# no longer holds. To faithfully exercise the reassign-from-registry DISCRIMINATION mechanism
# (the shipped _ps_callable_probe technique), use an isolated unique-named stub that is
# git-bash-PATH-visible but ABSENT from the registry — the exact asymmetry check (b) defeats.
set -u
NAME="bwveraprobe$$"
stub="$(mktemp -d)"                       # POSIX /tmp-style path (mktemp -d output)
printf '@echo %s 9.9.9\r\n@exit /b 0\r\n' "$NAME" > "$stub/$NAME.cmd"
echo "stub dir (POSIX form) = $stub"
echo "stub contains: $(ls "$stub")"

echo
echo "-- confirm the stub dir is ABSENT from the registry User+Machine PATH (never written):"
win_stub="$(cygpath -w "$stub")"
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command \
  "\$u=[System.Environment]::GetEnvironmentVariable('Path','User'); \$m=[System.Environment]::GetEnvironmentVariable('Path','Machine'); Write-Output ('STUB_IN_REGISTRY=' + ((\"\$m;\$u\") -like ('*' + '$win_stub' + '*')))"

echo
echo "-- POSIX-form export onto git-bash PATH (N3): export PATH=<posix-stub>:\$PATH"
export PATH="$stub:$PATH"

echo
echo "===== (i) check (a) binary present: stub file exists on git-bash PATH ====="
command -v "$NAME" >/dev/null 2>&1 && echo "  check(a) PASS: $NAME resolvable from git-bash" || echo "  check(a): git-bash command -v miss (cmd stub) — file present at $stub/$NAME.cmd"
ls -la "$stub/$NAME.cmd" >/dev/null 2>&1 && echo "  stub present: YES"

echo
echo "===== (ii) NAIVE powershell -Command inherits git-bash PATH -> resolves stub -> EXIT 0 (false-green LIVE) ====="
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "$NAME --version" 2>/dev/null
echo "  NAIVE exit=$?  (expect 0 — the false-green a naive check would report green on)"

echo
echo "===== (iii) CORRECT check (b): reassign \$env:PATH from REGISTRY-only (shipped technique) -> stub NOT seen -> EXIT 1 ====="
correct="\$u = [System.Environment]::GetEnvironmentVariable('Path','User'); \$m = [System.Environment]::GetEnvironmentVariable('Path','Machine'); \$env:PATH = [System.Environment]::ExpandEnvironmentVariables(\"\$m;\$u\"); \$c = Get-Command $NAME -ErrorAction SilentlyContinue; if (\$c) { Write-Output ('LEAKED ' + \$c.Source); exit 0 } else { exit 1 }"
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "$correct"
echo "  CORRECT exit=$?  (expect 1 — registry-reassign does NOT see the git-bash-only stub)"

echo
echo "-- teardown stub dir --"
rm -rf "$stub" && echo "stub removed"
echo
echo "-- P4 discrimination: NAIVE=0 (false-green) vs CORRECT=1 (caught). A build that shipped the"
echo "   naive form would exit 0 at check(b) and FAIL P4. Shipped _ps_callable_probe uses the CORRECT form."