#!/usr/bin/env bash
#
# run-author-gate-tests.sh — regression corpus for the authorship-attribution
# gate's .md narrowing (Arc 65 / stoa--z2b).
#
# WHAT THIS IS: the regression guard for the BOTH-DIRECTIONS contract of the
# narrowed gate (design-rev2 §3 + §4 P1-P3):
#   - FALSE-POSITIVE (fp/): a PROSE .md whose BODY merely discusses authorship
#     must now PASS (md mode emits nothing -> ALLOW). These are the z2b bugs.
#   - TRUE-POSITIVE (tp/): a real structured author field naming a non-Denson
#     PERSON must still BLOCK — across EVERY covered class, INCLUDING the two
#     .md-suffixed CONFIG-class collisions LICENSE.md (tp6) and
#     *.claude-plugin/*.md (tp7), which keep the OLD whole-file (cfg) coverage.
#   - CONTROL (control/): the happy structured path (Denson in the right place)
#     must still PASS.
#   - NEGATIVE / CARVE-OUT (manifest-only): notes.txt is out-of-class;
#     NOTICE.md stays md mode (the carve-out is not over-corrected).
#
# HOW IT EXERCISES THE REAL CODE (floor-manager acceptance #1 / design §3.3):
# it SOURCES the real substrate/hooks/_hooklib.sh and calls the ACTUAL
# classify_author_file + extract_author_fields — NO reimplementation of either.
# The ONLY thing mirrored is the tiny is_principal value-compare (12 lines, pure)
# against a FIXED test allow-list (the gate reads its tokens from an
# install-written principal-identity file; here we point the same compare at a
# fixed test token set). The live probes P4-P7 (run by VERA against a real armed
# throwaway gate) are the backstop for this mirrored compare.
#
# SECURITY GATE: this corpus is the regression guard for a SECURITY change. A
# RED tp6/tp7 means the rev1 collision hole reopened (LICENSE.md / plugin docs
# routed to md, losing the body-line catch). A RED fp means a z2b false-positive
# came back. Exit non-zero on ANY fail.
#
# DEPLOY: source-only. install.sh globs ${SRC_HOOKS_DIR}/*.sh non-recursively and
# copies README.md by basename, so this tests/ subdir never deploys (design §3.1;
# VERA P8 asserts a dry-run lists no tests/ path).
#
# NOTE ON FIXTURE NAMES: every fixture carries a .fixture suffix and the FICTIONAL
# name "Fenwick Galsworthy" appears ONLY inside .fixture files (a non-triggering
# basename) — so true-positive fixture content commits clean through the OLD gate.
# The runner reconstructs the INTENDED path the matcher must SEE from the manifest,
# NOT the on-disk name. Fixtures are FICTIONAL TEST INPUT, not authorship claims.

set -uo pipefail

# --- locate the lib + fixtures relative to THIS script ----------------------
TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HOOKS_DIR="$(cd "${TEST_DIR}/.." && pwd)"
FIX="${TEST_DIR}/fixtures"

# shellcheck source=/dev/null
# Source the REAL lib — brings in BOTH classify_author_file AND
# extract_author_fields (both live in the lib after the Arc 65 C4 relocation, so
# the runner needs no source-guard on the gate at all).
. "${HOOKS_DIR}/_hooklib.sh" || { echo "FATAL: cannot source _hooklib.sh"; exit 2; }

# --- is_principal MIRROR (design §3.3 step 2) -------------------------------
# This MIRRORS the gate's is_principal value-compare (gate lines ~75-88) against
# a FIXED test allow-list. The gate reads its accepted tokens from the
# install-written .claude/hooks/principal-identity file; here we hardcode the
# canonical Denson token set so the corpus is self-contained and deterministic.
# Mirrored (not sourced) because is_principal is DEFINED in the gate script, not
# the lib; the live probes P4-P7 backstop this mirror against the real gate.
TEST_ACCEPTED="$(printf '%s\n' 'denson' 'densonsmith2@gmail.com' 'denson smith')"
is_principal() {
  local v
  v="$(printf '%s' "$1" | tr '[:upper:]' '[:lower:]' | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')"
  [ -n "$v" ] || return 0   # empty value is not a wrong-name claim
  local tok
  while IFS= read -r tok; do
    [ -n "$tok" ] || continue
    [ "$v" = "$tok" ] && return 0
  done <<EOF
$TEST_ACCEPTED
EOF
  return 1
}

# --- the manifest: (intended_path | expect_rc | expect_mode | outcome | fixture)
# intended_path : the path the matcher must SEE (classify_author_file argument),
#                 reconstructed here, NOT the on-disk .fixture basename.
# expect_rc     : 0 = author-encoding (in-class) ; 1 = out-of-class.
# expect_mode   : cfg | md | -   ("-" when out-of-class / no mode printed).
# outcome       : ALLOW | BLOCK | NONE
#                 ALLOW = extractor emits something but every value is_principal,
#                         OR emits nothing (md body) -> no deny.
#                 BLOCK = extractor emits a value that is NOT is_principal -> deny.
#                 NONE  = out-of-class (no extraction at all).
# fixture       : path under fixtures/, or "-" for a classify-only manifest entry.
read_manifest() {
cat <<'MANIFEST'
# --- FALSE-POSITIVE (must now PASS: md mode emits nothing -> ALLOW) ---
docs/x.md|0|md|ALLOW|fp/fp1-seat-attribution.md.fixture
agents/verdicts/x.md|0|md|ALLOW|fp/fp2-verdict-audit.md.fixture
substrate/arcs/x.md|0|md|ALLOW|fp/fp3-directive-coauthor.md.fixture
substrate/x.md|0|md|ALLOW|fp/fp4-section28-docs.md.fixture
# --- TRUE-POSITIVE (must still BLOCK: non-Denson value emitted) ---
package.json|0|cfg|BLOCK|tp/tp1-package.json.fixture
skills/x/SKILL.md|0|md|BLOCK|tp/tp2-skill-frontmatter.md.fixture
LICENSE|0|cfg|BLOCK|tp/tp3-license.fixture
NOTICE|0|cfg|BLOCK|tp/tp4-notice.fixture
CITATION.cff|0|cfg|BLOCK|tp/tp5-citation.cff.fixture
LICENSE.md|0|cfg|BLOCK|tp/tp6-license-md.fixture
.claude-plugin/docs/overview.md|0|cfg|BLOCK|tp/tp7-claude-plugin-doc.md.fixture
# --- CONTROL (must PASS: Denson in the right structured place -> ALLOW) ---
package.json|0|cfg|ALLOW|control/ctl1-package-denson.json.fixture
skills/y/SKILL.md|0|md|ALLOW|control/ctl2-skill-frontmatter-denson.md.fixture
LICENSE.md|0|cfg|ALLOW|control/ctl3-license-md-denson.fixture
# --- NEGATIVE path-class (classify-only: out-of-class) ---
notes.txt|1|-|NONE|-
# --- CARVE-OUT GUARD (classify-only: NOTICE.md stays md, NOT over-corrected) ---
NOTICE.md|0|md|NONE|-
# --- y12 (Arc 69 / stoa--y12): standard LICENSE "Copyright (c) <year> <Name>" form ---
LICENSE|0|cfg|BLOCK|tp/tp8-license-c-form.fixture
LICENSE|0|cfg|BLOCK|tp/tp9-license-copyright-symbol.fixture
LICENSE|0|cfg|ALLOW|control/ctl4-license-c-form-denson.fixture
docs/x.md|0|md|ALLOW|fp/fp5-copyright-prose.md.fixture
LICENSE|0|cfg|ALLOW|control/ctl-y12-prose-in-cfg.fixture
LICENSE|0|cfg|ALLOW|control/ctl-y12-year-prose-in-cfg.fixture
# --- ez9 (Arc 69 / stoa--ez9): reviewed-allow for source-citation fields (inline-array) ---
docs/x.md|0|md|BLOCK|tp/tp11-publisher-no-marker.md.fixture
docs/x.md|0|md|ALLOW|control/ctl5-publisher-allowed.md.fixture
docs/x.md|0|md|BLOCK|tp/tp12-author-allow-attempt.md.fixture
docs/x.md|0|md|BLOCK|control/ctl6-publisher-mismatch.md.fixture
docs/x.md|0|md|BLOCK|tp/tp13-blockform-not-allowed.md.fixture
MANIFEST
}

# --- run ---------------------------------------------------------------------
PASS=0
FAIL=0
TAB="$(printf '\t')"

# is_pair_allowed MIRROR (Arc 69 / stoa--ez9 — C4 minimal skip-glue): the ONLY
# new mirrored primitive. parse_allow_pairs itself is SOURCED from _hooklib.sh
# (no second mirror — C1/r3); this is the tiny exact-pair compare the gate
# applies around it. The live probe P-ez9-live (VERA, against the REAL gate) is
# the authoritative backstop for this glue (C4). EXACT equality after CR-strip.
is_pair_allowed() {
  local af="$1" aval="$2" blob="$3" lf lv
  [ -n "$blob" ] || return 1
  while IFS="$TAB" read -r lf lv; do
    lf="$(printf '%s' "$lf" | tr -d '\r')"
    lv="$(printf '%s' "$lv" | tr -d '\r')"
    [ -n "$lf" ] || continue
    if [ "$lf" = "$af" ] && [ "$lv" = "$aval" ]; then
      return 0
    fi
  done <<EOF
$blob
EOF
  return 1
}

# compute_outcome <mode> <fixture_file> : run the REAL extractor in <mode> over
# the fixture, then run each emitted value through the is_principal mirror.
# ez9 (Arc 69): also build the reviewed-allow set from the fixture's own content
# via the SOURCED parse_allow_pairs and skip a pair that is exact-allow-listed.
# Echoes ALLOW or BLOCK.
compute_outcome() {
  local mode="$1" file="$2" pairs field val allow_pairs
  pairs="$(extract_author_fields "$mode" < "$file")"
  if [ -z "$pairs" ]; then
    echo "ALLOW"   # nothing extracted -> no deny
    return 0
  fi
  # ez9: reviewed-allow set from the SAME fixture blob (parse_allow_pairs SOURCED
  # from _hooklib.sh — no second mirror). md mode only ever reaches here with a
  # frontmatter marker; cfg fixtures carry the marker in frontmatter too.
  allow_pairs="$(parse_allow_pairs < "$file")"
  while IFS="$TAB" read -r field val; do
    [ -n "$val" ] || continue
    field="$(printf '%s' "$field" | tr -d '\r')"
    val="$(printf '%s' "$val" | tr -d '\r')"
    if is_pair_allowed "$field" "$val" "$allow_pairs"; then
      continue   # reviewed source-citation -> skip block for THIS pair only
    fi
    if ! is_principal "$val"; then
      echo "BLOCK"
      return 0
    fi
  done <<EOF
$pairs
EOF
  echo "ALLOW"
}

while IFS= read -r line; do
  case "$line" in ''|\#*) continue ;; esac
  IFS='|' read -r intended exp_rc exp_mode outcome fixture <<EOF
$line
EOF

  # --- classify (membership + mode) in ONE call: the REAL function ---
  got_mode="$(classify_author_file "$intended")"
  got_rc=$?
  [ "$got_rc" -ne 0 ] && got_mode="-"

  ok=1
  detail=""

  if [ "$got_rc" != "$exp_rc" ]; then
    ok=0; detail="${detail} rc=${got_rc} (want ${exp_rc});"
  fi
  if [ "$got_mode" != "$exp_mode" ]; then
    ok=0; detail="${detail} mode=${got_mode} (want ${exp_mode});"
  fi

  # --- outcome (only for entries that carry a fixture file) ---
  if [ "$fixture" != "-" ]; then
    got_outcome="$(compute_outcome "$got_mode" "${FIX}/${fixture}")"
    if [ "$got_outcome" != "$outcome" ]; then
      ok=0; detail="${detail} outcome=${got_outcome} (want ${outcome});"
    fi
  fi

  if [ "$ok" -eq 1 ]; then
    PASS=$((PASS + 1))
    printf 'PASS  %-34s [rc=%s mode=%s%s]\n' "$intended" "$got_rc" "$got_mode" \
      "$([ "$fixture" != "-" ] && printf ' %s' "$outcome")"
  else
    FAIL=$((FAIL + 1))
    printf 'FAIL  %-34s%s\n' "$intended" "$detail"
  fi
done < <(read_manifest)

echo "-------------------------------------------------------------"
echo "${PASS} passed / ${FAIL} failed"
[ "$FAIL" -eq 0 ] || exit 1
exit 0
