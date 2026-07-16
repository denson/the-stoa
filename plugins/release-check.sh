#!/usr/bin/env bash
# release-check.sh — ADVISORY authorship + namespace-resolution check for plugin
# releases. Report-only by design (deny-gates are retired doctrine, PRINCIPAL
# 2026-07-09): it prints findings and ALWAYS exits 0. Run before tag/push.
# Author: Denson Smith
set -u
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
FINDINGS=0
note() { echo "ADVISORY: $*"; FINDINGS=$((FINDINGS+1)); }

for mf in "$ROOT"/.claude-plugin/marketplace.json "$ROOT"/plugins/*/.claude-plugin/plugin.json; do
  [ -f "$mf" ] || continue
  echo "-- checking $mf"
  python - "$mf" <<'EOF' || true
import json, sys
p = sys.argv[1]
d = json.load(open(p, encoding="utf-8"))
def check_author(obj, where):
    a = obj.get("author") or obj.get("owner") or {}
    name = a.get("name", "")
    if name != "Denson Smith":
        print(f"ADVISORY: {where}: author/owner name is {name!r}, expected 'Denson Smith'")
    url = a.get("url", "")
    if url and not url.startswith("https://github.com/denson"):
        print(f"ADVISORY: {where}: author url {url!r} does not resolve into github.com/denson")
check_author(d, p)
for k in ("homepage", "repository"):
    v = d.get(k, "")
    if v and not v.startswith("https://github.com/denson"):
        print(f"ADVISORY: {p}: {k} {v!r} outside the github.com/denson namespace")
for pl in d.get("plugins", []):
    check_author(pl, f"{p}:plugins[{pl.get('name')}]")
EOF
done

# author-like fields anywhere in plugin content naming a non-PRINCIPAL person
grep -rniE '^(author|owner|maintainer|created.by)\s*[:=]' "$ROOT"/plugins/*/ 2>/dev/null \
  | grep -viE 'denson smith|denson|template|advisory|author-like|agent-author' | head -10 \
  | while read -r line; do echo "ADVISORY: author-like field to eyeball: $line"; done

echo "release-check complete (advisory; exit 0 always)."
exit 0
