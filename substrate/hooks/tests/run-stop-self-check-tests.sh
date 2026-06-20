#!/usr/bin/env bash
#
# run-stop-self-check-tests.sh — regression corpus for the Stop self-check hook's
# clause (E) gauntlet-by-default detector (Arc 68 / stoa--pk4 §2.8 / C7).
#
# WHAT THIS IS: a FRESH test (no stop-self-check test existed to extend — the
# tests/ dir held only run-author-gate-tests.sh). It exercises the REAL
# substrate/hooks/stop-self-check.sh end-to-end via stdin, asserting:
#   - Assertion 1 (clause E present + blocks once): the FIRST Stop event this turn
#     emits decision:"block" with a .reason that CONTAINS the clause-(E) sentinel
#     string "solo-with-one-checker close is the AR-7 failure shape". This proves
#     clause (E) is INJECTED on the SAME confirmed-working decision:block+reason
#     channel as clauses A/B/C/D (the accepted advisory branch — §2.2/C3).
#   - Assertion 2 (infinite-block guard): the SAME event run a SECOND time SAME
#     turn (same session_id + same transcript size => same turn-key => same
#     sentinel) ALLOWS the stop. allow() exits 0 with NO stdout, so the second
#     call's stdout must be EMPTY. This proves the once-per-turn sentinel is intact
#     (a Stop hook that always blocked would trap the turn in a loop).
#
# DETERMINISM (the C7 load-bearing property): both invocations MUST resolve to the
# SAME sentinel dir + the SAME turn-key, or assertion 2 is meaningless. We control
# both inputs the hook keys on:
#   - cwd            -> a fixed runner-controlled scratch dir, so the hook's FIRST
#                       sentinel-dir candidate ("<cwd>/.claude/hooks/.stop-sentinels")
#                       is the SAME writable dir for both calls.
#   - transcript_path-> a fixed runner-created file of a known, stable size, so the
#                       turn-key ("<session>-<transcript_size>") is identical across
#                       the two calls. stop_hook_active:false (in the fixture) keeps
#                       the hook from early-allowing at the stop_hook_active guard.
# The fixture ships with PLACEHOLDER tokens for these two absolute paths; the runner
# substitutes the runtime values (per-machine absolute paths) before piping.
#
# CLEANUP: the runner removes its scratch dir (the fixture transcript + the per-turn
# sentinel it created) on exit — fixed-literal paths under a single scratch root, no
# $VAR-in-destructive-op footgun (operating-disciplines.md §8.6).
#
# DEPLOY: source-only / test-only. install.sh globs ${SRC_HOOKS_DIR}/*.sh
# NON-recursively, so this tests/ subdir never deploys (same property the author-gate
# corpus relies on).
#
# FAIL: exit non-zero on ANY failed assertion.

set -uo pipefail

# --- locate the hook + fixture relative to THIS script ----------------------
TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HOOKS_DIR="$(cd "${TEST_DIR}/.." && pwd)"
HOOK="${HOOKS_DIR}/stop-self-check.sh"
FIX="${TEST_DIR}/fixtures/stop-event-orchestrator.json"

[ -f "$HOOK" ] || { echo "FATAL: hook not found: $HOOK"; exit 2; }
[ -f "$FIX" ]  || { echo "FATAL: fixture not found: $FIX"; exit 2; }

# --- runner-controlled scratch root (fixed-literal; the only thing we rm) -----
SCRATCH="${TMPDIR:-/tmp}/stoa-pk4-stop-test"
TRANSCRIPT="${SCRATCH}/transcript.txt"
# The sentinel the hook will create lands under <cwd>/.claude/hooks/.stop-sentinels;
# we point cwd at the scratch root so that dir is ours to clean.
CWD_DIR="${SCRATCH}"

cleanup() {
  # Fixed-literal scratch root — no $VAR-derived path in the destructive op beyond
  # this one known root we created. Safe per §8.6.
  rm -rf "${TMPDIR:-/tmp}/stoa-pk4-stop-test" 2>/dev/null || true
}
trap cleanup EXIT

# Fresh scratch every run.
rm -rf "$SCRATCH" 2>/dev/null || true
mkdir -p "$SCRATCH" || { echo "FATAL: cannot create scratch dir $SCRATCH"; exit 2; }

# Stable-size transcript so the turn-key ("<session>-<size>") is identical on both calls.
printf 'stoa-pk4 fixture transcript — stable size for a deterministic turn-key.\n' > "$TRANSCRIPT"

# Build the concrete event JSON from the fixture, substituting the two absolute paths.
# python3 does the substitution so embedded path separators never break the JSON.
EVENT="$(TRANSCRIPT="$TRANSCRIPT" CWD_DIR="$CWD_DIR" FIX="$FIX" python3 -c '
import os, sys
t = open(os.environ["FIX"]).read()
t = t.replace("STOA_PK4_TRANSCRIPT_PLACEHOLDER", os.environ["TRANSCRIPT"].replace("\\", "\\\\"))
t = t.replace("STOA_PK4_CWD_PLACEHOLDER", os.environ["CWD_DIR"].replace("\\", "\\\\"))
sys.stdout.write(t)
')" || { echo "FATAL: could not build event JSON (python3 missing?)"; exit 2; }

SENTINEL_STR='solo-with-one-checker close is the AR-7 failure shape'
PASS=0
FAIL=0

# --- Assertion 1: first call this turn BLOCKS with clause (E) present --------
OUT1="$(printf '%s' "$EVENT" | bash "$HOOK")"
RC1=$?

a1_ok=1
a1_detail=""
if [ "$RC1" -ne 0 ]; then
  a1_ok=0; a1_detail="${a1_detail} hook exited $RC1 (want 0);"
fi
# Parse the decision + reason via python3 (the hook emits a single-line JSON object).
DECISION="$(printf '%s' "$OUT1" | python3 -c 'import sys,json;
try:
    o=json.load(sys.stdin); sys.stdout.write(str(o.get("decision","")))
except Exception:
    pass' 2>/dev/null)"
REASON="$(printf '%s' "$OUT1" | python3 -c 'import sys,json;
try:
    o=json.load(sys.stdin); sys.stdout.write(str(o.get("reason","")))
except Exception:
    pass' 2>/dev/null)"
if [ "$DECISION" != "block" ]; then
  a1_ok=0; a1_detail="${a1_detail} decision='$DECISION' (want block);"
fi
case "$REASON" in
  *"$SENTINEL_STR"*) : ;;
  *) a1_ok=0; a1_detail="${a1_detail} clause-(E) sentinel string MISSING from reason;" ;;
esac

if [ "$a1_ok" -eq 1 ]; then
  PASS=$((PASS + 1)); echo "PASS  assertion 1: first Stop blocks + clause (E) sentinel present"
else
  FAIL=$((FAIL + 1)); echo "FAIL  assertion 1:${a1_detail}"
fi

# --- Assertion 2: second call SAME turn ALLOWS (infinite-block guard) --------
# Same event => same session_id + same transcript size => same turn-key => the
# sentinel written by call 1 already exists => the hook ALLOWS (exit 0, NO stdout).
OUT2="$(printf '%s' "$EVENT" | bash "$HOOK")"
RC2=$?

a2_ok=1
a2_detail=""
if [ "$RC2" -ne 0 ]; then
  a2_ok=0; a2_detail="${a2_detail} hook exited $RC2 (want 0);"
fi
if [ -n "$OUT2" ]; then
  a2_ok=0; a2_detail="${a2_detail} expected EMPTY stdout (allow) but got output;"
fi

if [ "$a2_ok" -eq 1 ]; then
  PASS=$((PASS + 1)); echo "PASS  assertion 2: second Stop same turn allows (infinite-block guard intact)"
else
  FAIL=$((FAIL + 1)); echo "FAIL  assertion 2:${a2_detail}"
fi

echo "-------------------------------------------------------------"
echo "${PASS} passed / ${FAIL} failed"
[ "$FAIL" -eq 0 ] || exit 1
exit 0
