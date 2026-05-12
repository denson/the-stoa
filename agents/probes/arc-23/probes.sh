#!/usr/bin/env bash
# Arc 23 — content probes for substrate edits.
#
# Authored by: Denson Smith (ADA Phase 2 build).
# Purpose: input to Phase 3 VERA verification. VERA may add more probes;
# these are the minimal grep-style content assertions that confirm the
# Phase 2 substrate edits landed in the expected places with the expected
# load-bearing strings.
#
# Exits 0 on all-pass; non-zero on any failure (per-probe diagnostic to stderr).
# Run from the arc-23/build worktree root (the worktree at
# .claude/worktrees/arc-23-build, where the substrate edits live).

set -u

FAIL=0
PASS_COUNT=0
FAIL_COUNT=0

probe() {
  # $1 = probe label
  # $2 = command (string, eval'd)
  # $3 = expected behavior ("nonzero-count" | "exit-zero")
  local label="$1"
  local cmd="$2"
  local expected="$3"
  local out
  out=$(eval "$cmd" 2>&1)
  local rc=$?
  case "$expected" in
    nonzero-count)
      # cmd is a grep -c style command; "passes" if output > 0
      # When grep -c is run against multiple files, output is per-file;
      # we treat pass as "at least one line has a positive count and rc<=1".
      if [[ "$out" =~ ^[0-9]+$ ]]; then
        if [[ "$out" -gt 0 ]]; then
          PASS_COUNT=$((PASS_COUNT + 1))
          printf 'PASS  %s\n' "$label"
          return 0
        fi
      else
        # multi-file output; pass if any line ends in :N where N>0
        if echo "$out" | grep -Eq ':[1-9][0-9]*$'; then
          PASS_COUNT=$((PASS_COUNT + 1))
          printf 'PASS  %s\n' "$label"
          return 0
        fi
      fi
      FAIL_COUNT=$((FAIL_COUNT + 1))
      FAIL=1
      printf 'FAIL  %s\n      cmd=%s\n      out=%s\n' "$label" "$cmd" "$out" >&2
      return 1
      ;;
    exit-zero)
      if [[ $rc -eq 0 ]]; then
        PASS_COUNT=$((PASS_COUNT + 1))
        printf 'PASS  %s\n' "$label"
        return 0
      fi
      FAIL_COUNT=$((FAIL_COUNT + 1))
      FAIL=1
      printf 'FAIL  %s\n      cmd=%s\n      rc=%s\n      out=%s\n' "$label" "$cmd" "$rc" "$out" >&2
      return 1
      ;;
    *)
      printf 'FAIL  %s (unknown expectation: %s)\n' "$label" "$expected" >&2
      FAIL=1
      FAIL_COUNT=$((FAIL_COUNT + 1))
      return 1
      ;;
  esac
}

echo "==> Arc 23 substrate-edit content probes"

# ---------- operating-disciplines.md structural probes ----------

probe "op-disc §15 top-level heading present" \
  "grep -c '^## 15\\.' substrate/operating-disciplines.md" \
  nonzero-count

probe "op-disc §16 top-level heading present" \
  "grep -c '^## 16\\.' substrate/operating-disciplines.md" \
  nonzero-count

probe "op-disc §17 top-level heading present" \
  "grep -c '^## 17\\.' substrate/operating-disciplines.md" \
  nonzero-count

probe "op-disc §6.7 N=1 rule subsection present" \
  "grep -c '^### 6\\.7' substrate/operating-disciplines.md" \
  nonzero-count

probe "op-disc §8.4 substrate-edit smoke beats subsection present" \
  "grep -c '^### 8\\.4' substrate/operating-disciplines.md" \
  nonzero-count

probe "op-disc §8.5 probe coverage of fallback chains subsection present" \
  "grep -c '^### 8\\.5' substrate/operating-disciplines.md" \
  nonzero-count

probe "op-disc §8.3 activation-paste subsection preserved (Arc 21)" \
  "grep -c '^### 8\\.3' substrate/operating-disciplines.md" \
  nonzero-count

# ---------- CAPTAIN verifier role-file structural probes ----------

probe "CAPTAIN_VERA.md §5.7 quadrant-per-probe present" \
  "grep -c '^### 5\\.7' substrate/CAPTAIN_VERA.md" \
  nonzero-count

probe "CAPTAIN_VERA.md §5.8 STRABO-claim verification present" \
  "grep -c '^### 5\\.8' substrate/CAPTAIN_VERA.md" \
  nonzero-count

probe "CAPTAIN_CATO.md §6.7 quadrant-per-finding present" \
  "grep -c '^### 6\\.7' substrate/CAPTAIN_CATO.md" \
  nonzero-count

probe "CAPTAIN_CATO.md §6.8 empirical-env reproduction present" \
  "grep -c '^### 6\\.8' substrate/CAPTAIN_CATO.md" \
  nonzero-count

probe "CAPTAIN_ARGUS.md §6.6 quadrant-per-risk present" \
  "grep -c '^### 6\\.6' substrate/CAPTAIN_ARGUS.md" \
  nonzero-count

probe "CAPTAIN_ZENO.md §6.6 quadrant-per-criterion present" \
  "grep -c '^### 6\\.6' substrate/CAPTAIN_ZENO.md" \
  nonzero-count

probe "CAPTAIN_STRABO.md §6.6 output-preliminary present" \
  "grep -c '^### 6\\.6' substrate/CAPTAIN_STRABO.md" \
  nonzero-count

# ---------- MAJOR PLINY structural probes ----------

probe "MAJOR_PLINY.md §5.5 post-STRABO VERA dispatch present" \
  "grep -c '^### 5\\.5' substrate/MAJOR_PLINY.md" \
  nonzero-count

probe "MAJOR_PLINY.md §5.6 INCOMPLETE/UNVERIFIABLE handling present" \
  "grep -c '^### 5\\.6' substrate/MAJOR_PLINY.md" \
  nonzero-count

probe "MAJOR_PLINY.md §5.7 smoke-beat discipline present" \
  "grep -c '^### 5\\.7' substrate/MAJOR_PLINY.md" \
  nonzero-count

probe "MAJOR_PLINY.md §7.8 no-narrowing-gauntlet-from-N=1 present" \
  "grep -c '^### 7\\.8' substrate/MAJOR_PLINY.md" \
  nonzero-count

# ---------- MAJOR POLYBIUS structural probes ----------

probe "MAJOR_POLYBIUS.md §15 TIMING_LOG / retrospective discipline present" \
  "grep -c '^## 15\\.' substrate/MAJOR_POLYBIUS.md" \
  nonzero-count

# ---------- §3.5 string-discipline probes ----------
# INCOMPLETE: bare uppercase verdict-shape label.
# Required in VERA, CATO, ARGUS (ZENO exempt per §3.5).

probe "string-discipline: INCOMPLETE in CAPTAIN_VERA.md" \
  "grep -c 'INCOMPLETE' substrate/CAPTAIN_VERA.md" \
  nonzero-count

probe "string-discipline: INCOMPLETE in CAPTAIN_CATO.md" \
  "grep -c 'INCOMPLETE' substrate/CAPTAIN_CATO.md" \
  nonzero-count

probe "string-discipline: INCOMPLETE in CAPTAIN_ARGUS.md" \
  "grep -c 'INCOMPLETE' substrate/CAPTAIN_ARGUS.md" \
  nonzero-count

# UNVERIFIABLE: required (in some form) in VERA, CATO, ARGUS, ZENO.

probe "string-discipline: UNVERIFIABLE in CAPTAIN_VERA.md" \
  "grep -c 'UNVERIFIABLE' substrate/CAPTAIN_VERA.md" \
  nonzero-count

probe "string-discipline: UNVERIFIABLE in CAPTAIN_CATO.md" \
  "grep -c 'UNVERIFIABLE' substrate/CAPTAIN_CATO.md" \
  nonzero-count

probe "string-discipline: UNVERIFIABLE in CAPTAIN_ARGUS.md" \
  "grep -c 'UNVERIFIABLE' substrate/CAPTAIN_ARGUS.md" \
  nonzero-count

probe "string-discipline: UNVERIFIABLE in CAPTAIN_ZENO.md" \
  "grep -c 'UNVERIFIABLE' substrate/CAPTAIN_ZENO.md" \
  nonzero-count

# verifier-spins-forever: required in VERA, ARGUS (CATO/ZENO exempt per §3.5).

probe "string-discipline: verifier-spins-forever in CAPTAIN_VERA.md" \
  "grep -c 'verifier-spins-forever' substrate/CAPTAIN_VERA.md" \
  nonzero-count

probe "string-discipline: verifier-spins-forever in CAPTAIN_ARGUS.md" \
  "grep -c 'verifier-spins-forever' substrate/CAPTAIN_ARGUS.md" \
  nonzero-count

# Quadrant labels: full enumeration in VERA, CATO, ARGUS (ZENO uses
# only the specific labels relevant to its narrow case).

probe "string-discipline: quadrant labels in CAPTAIN_VERA.md" \
  "grep -Ec 'easy-easy|hard-easy|easy-hard|hard-hard' substrate/CAPTAIN_VERA.md" \
  nonzero-count

probe "string-discipline: quadrant labels in CAPTAIN_CATO.md" \
  "grep -Ec 'easy-easy|hard-easy|easy-hard|hard-hard' substrate/CAPTAIN_CATO.md" \
  nonzero-count

probe "string-discipline: quadrant labels in CAPTAIN_ARGUS.md" \
  "grep -Ec 'easy-easy|hard-easy|easy-hard|hard-hard' substrate/CAPTAIN_ARGUS.md" \
  nonzero-count

# quadrant_classification schema field: required in VERA, CATO, ARGUS;
# ZENO exempt (no schema field; discipline lives in evidence prose).

probe "string-discipline: quadrant_classification: in CAPTAIN_VERA.md" \
  "grep -c 'quadrant_classification:' substrate/CAPTAIN_VERA.md" \
  nonzero-count

probe "string-discipline: quadrant_classification: in CAPTAIN_CATO.md" \
  "grep -c 'quadrant_classification:' substrate/CAPTAIN_CATO.md" \
  nonzero-count

probe "string-discipline: quadrant_classification: in CAPTAIN_ARGUS.md" \
  "grep -c 'quadrant_classification:' substrate/CAPTAIN_ARGUS.md" \
  nonzero-count

# operating-disciplines.md §15 cross-reference present in all four verifier files.

probe "cross-ref: 'operating-disciplines.md §15' in CAPTAIN_VERA.md" \
  "grep -c 'operating-disciplines.md.*§15' substrate/CAPTAIN_VERA.md" \
  nonzero-count

probe "cross-ref: 'operating-disciplines.md §15' in CAPTAIN_CATO.md" \
  "grep -c 'operating-disciplines.md.*§15' substrate/CAPTAIN_CATO.md" \
  nonzero-count

probe "cross-ref: 'operating-disciplines.md §15' in CAPTAIN_ARGUS.md" \
  "grep -c 'operating-disciplines.md.*§15' substrate/CAPTAIN_ARGUS.md" \
  nonzero-count

probe "cross-ref: 'operating-disciplines.md §15' in CAPTAIN_ZENO.md" \
  "grep -c 'operating-disciplines.md.*§15' substrate/CAPTAIN_ZENO.md" \
  nonzero-count

# ---------- save-verdict user-tier extension probe ----------

probe "save-verdict SKILL.md contains INCOMPLETE or UNVERIFIABLE schema extension" \
  "grep -Ec 'INCOMPLETE|UNVERIFIABLE' \"$HOME/.claude/skills/save-verdict/SKILL.md\"" \
  nonzero-count

probe "save-verdict SKILL.md contains quadrant_classification field" \
  "grep -c 'quadrant_classification' \"$HOME/.claude/skills/save-verdict/SKILL.md\"" \
  nonzero-count

# ---------- 14u meta-application: install.sh dry-run smoke beat ----------
# Apply §8.4 discipline to Arc 23 itself: install.sh --dry-run for project mode
# should list every modified substrate file in its deploy plan.

INSTALL_TEST_DIR="${TMPDIR:-/tmp}/arc23-install-test-$$"
mkdir -p "$INSTALL_TEST_DIR"
DRY_RUN_OUT="$INSTALL_TEST_DIR/dry-run.out"
bash substrate/install.sh --dry-run --target project --project-dir "$INSTALL_TEST_DIR" >"$DRY_RUN_OUT" 2>&1
INSTALL_RC=$?

if [[ $INSTALL_RC -ne 0 ]]; then
  printf 'FAIL  install.sh --dry-run exited %s; see %s\n' "$INSTALL_RC" "$DRY_RUN_OUT" >&2
  FAIL=1
  FAIL_COUNT=$((FAIL_COUNT + 1))
else
  PASS_COUNT=$((PASS_COUNT + 1))
  printf 'PASS  install.sh --dry-run executed\n'
fi

for f in operating-disciplines.md CAPTAIN_VERA.md CAPTAIN_CATO.md CAPTAIN_ARGUS.md CAPTAIN_ZENO.md CAPTAIN_STRABO.md MAJOR_PLINY.md MAJOR_POLYBIUS.md; do
  if grep -q "$f" "$DRY_RUN_OUT" 2>/dev/null; then
    PASS_COUNT=$((PASS_COUNT + 1))
    printf 'PASS  install.sh dry-run lists %s\n' "$f"
  else
    FAIL_COUNT=$((FAIL_COUNT + 1))
    FAIL=1
    printf 'FAIL  install.sh dry-run does NOT list %s\n' "$f" >&2
  fi
done

rm -rf "$INSTALL_TEST_DIR"

# ---------- summary ----------

echo
echo "==> Probe summary"
echo "PASS: $PASS_COUNT"
echo "FAIL: $FAIL_COUNT"

if [[ $FAIL -eq 0 ]]; then
  echo "==> All probes passed."
  exit 0
fi

echo "==> One or more probes failed." >&2
exit 1
