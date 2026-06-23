#!/usr/bin/env bash
#
# run-decision-register-corpus.sh — seed corpus + runner for the decision-register
# module (Arc 71 / stoa--7gl).
#
# WHAT THIS IS: the both-directions regression-guard for the CAPTURE half of the
# self-correction black box. It guards the write-trigger predicate + over-write
# guard (write on a decided dilemma; withhold on a problem, an
# illuminated-but-undecided dilemma, or an incidental mention) AND the DC4
# vacuity detector (a hollow counter-hypothesis is detectably hollow). Mirrors the
# Arc-70 run-dilemma-corpus.sh shape: manifest-driven, both-directions controls,
# PASS/FAIL tally, exit-nonzero-on-fail.
#
# THE HARD HONEST DIFFERENCE (same as the Arc-70 runner): "did the agent correctly
# decide to write or withhold" is MODEL JUDGMENT (whether a path was actually
# chosen is irreducibly a judgment read, doctrine A1) — there is no shell function
# that returns write-vs-no-write. So:
#   --check-corpus : DETERMINISTIC. Validates the corpus is WELL-FORMED only
#                    (labels valid, manifest<->files match, no empty WHY/SCENARIO,
#                    every write fixture's ENTRY block has all nine fields populated
#                    with a NON-hollow counter-hypothesis and >= 3 OPTIONS, every
#                    write-but-hollow fixture's counter-hypothesis IS empty-or-on
#                    the vacuity denylist as the DC4 detector negative control).
#                    CI-safe; this is the mechanical close-gate.
#   --judge        : the FLOOR evaluation. Presents each SCENARIO with the label
#                    HIDDEN for a JUDGING AGENT (VERA) to classify write/no-write
#                    using ONLY the module text, then scores the calls vs the labels
#                    per-class vs the FLOORS. Exit nonzero on any floor miss. The
#                    "classifier" is the model+module, NOT this script — and
#                    (judge==verifier coupling) VERA is also the gauntlet verifier,
#                    so a green --judge is a DOGFOOD PROXY, NOT an independent
#                    measurement, and must never be cited as "capture verified."
#
# 100% AGGREGATE IS EXPLICITLY NOT THE BAR. The corpus is a regression-guard +
# dogfood proxy, not a proof of a judgment capability. See README.md for the floor
# honesty statements.
#
# DEPLOY: source-only. install.sh globs substrate/modules/*.md NON-RECURSIVELY, so
# this tests/ subdir never deploys (VERA P8 asserts a dry-run lists no
# modules/tests/decision-register/ path).
#
# FIXTURES ARE FICTIONAL TEST INPUT, not authorship claims. Any names/companies in
# scenario text are invented.

set -uo pipefail

TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FIX="${TEST_DIR}/fixtures"
MANIFEST="${TEST_DIR}/manifest.tsv"
MODULE="${TEST_DIR}/../../decision-register.md"   # substrate/modules/decision-register.md

# valid EXPECT labels: write | no-write | write-but-hollow
#   write            — a decided dilemma; the capture must fire (decided/)
#   no-write         — the over-write/over-fire guard (problem/, illuminated/, incidental/)
#   write-but-hollow — a decided dilemma whose entry is hollow; the DC4 detector
#                      negative control (hollow/) — --check-corpus must FLAG it hollow
VALID_LABELS="write no-write write-but-hollow"

# the nine single-line schema fields each write/hollow ENTRY block must carry
ENTRY_FIELDS="DR-ID WHEN CHECKPOINT DILEMMA WARNING OPTIONS CHOSEN COUNTER-HYPOTHESIS CONTEXT-LINK"

# vacuity denylist (case-insensitive substring) — the canonical hollow
# counter-hypothesis patterns. SEED list, accretes from real hollow entries; NOT a
# closed proof of vacuity (README honesty statement 4).
VACUITY_PATTERNS="we'll see|time will tell|might not work|who knows|hard to say|could go either way"

usage() {
  cat <<USAGE
usage: run-decision-register-corpus.sh [--check-corpus | --judge [--score <calls>]]
  --check-corpus   deterministic structural validation (CI-safe close-gate)
  --judge          floor evaluation: print each SCENARIO label-hidden for a
                   judging agent (VERA), then score against labels vs the floors
USAGE
}

# --- shared helpers ----------------------------------------------------------

# is_valid_label <label> : 0 if in VALID_LABELS
is_valid_label() {
  local l="$1" v
  for v in $VALID_LABELS; do [ "$l" = "$v" ] && return 0; done
  return 1
}

# field <KEY> <file> : extract the value after "KEY:" on its line (trimmed),
# robust to CRLF. Returns the first match only. VERBATIM from the Arc-70
# run-dilemma-corpus.sh field() — the same proven leading-LABEL: parse the 2b
# reader will use (design DC0 forward-constraint).
field() {
  local key="$1" file="$2"
  awk -v k="${key}:" '
    index($0, k) == 1 {
      v = substr($0, length(k) + 1)
      sub(/^[[:space:]]+/, "", v); sub(/[[:space:]]+$/, "", v)
      gsub(/\r/, "", v)
      print v; exit
    }' "$file"
}

# is_vacuous <value> : 0 if the value is empty/whitespace OR matches the vacuity
# denylist (case-insensitive). The DC4 hollow-counter-hypothesis detector.
is_vacuous() {
  local v="$1" trimmed
  trimmed="$(printf '%s' "$v" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')"
  [ -z "$trimmed" ] && return 0
  printf '%s' "$trimmed" | grep -qiE "$VACUITY_PATTERNS" && return 0
  return 1
}

# read the manifest into parallel arrays (skip blank/comment lines)
declare -a M_PATH M_LABEL
load_manifest() {
  local p l
  local tab; tab="$(printf '\t')"
  while IFS= read -r line || [ -n "$line" ]; do
    case "$line" in ''|\#*) continue ;; esac
    IFS="$tab" read -r p l <<EOF
$line
EOF
    p="$(printf '%s' "$p" | tr -d '\r')"
    l="$(printf '%s' "$l" | tr -d '\r')"
    [ -n "$p" ] || continue
    M_PATH+=("$p")
    M_LABEL+=("$l")
  done < "$MANIFEST"
}

# =============================================================================
# --check-corpus : DETERMINISTIC structural validation (the close-gate)
# =============================================================================
check_corpus() {
  local fail=0 n=0
  [ -f "$MANIFEST" ] || { echo "FATAL: manifest not found: $MANIFEST"; exit 2; }
  [ -f "$MODULE" ]   || { echo "FATAL: module source not found: $MODULE"; exit 2; }

  load_manifest

  local i path label fpath e_expect e_why e_scenario fld val opts nopt
  for i in "${!M_PATH[@]}"; do
    path="${M_PATH[$i]}"; label="${M_LABEL[$i]}"
    n=$((n + 1))
    fpath="${TEST_DIR}/${path}"

    if [ ! -f "$fpath" ]; then
      echo "FAIL  ${path} : file in manifest but missing on disk"; fail=$((fail + 1)); continue
    fi
    if ! is_valid_label "$label"; then
      echo "FAIL  ${path} : manifest label '${label}' not in {${VALID_LABELS}}"; fail=$((fail + 1))
    fi

    # directory <-> label invariant: each class dir carries exactly its label.
    case "$path" in
      */decided/*)     [ "$label" = "write" ]            || { echo "FAIL  ${path} : decided/ fixture must be labeled 'write', got '${label}'"; fail=$((fail + 1)); } ;;
      */problem/*)     [ "$label" = "no-write" ]         || { echo "FAIL  ${path} : problem/ fixture must be labeled 'no-write', got '${label}'"; fail=$((fail + 1)); } ;;
      */illuminated/*) [ "$label" = "no-write" ]         || { echo "FAIL  ${path} : illuminated/ fixture must be labeled 'no-write', got '${label}'"; fail=$((fail + 1)); } ;;
      */incidental/*)  [ "$label" = "no-write" ]         || { echo "FAIL  ${path} : incidental/ fixture must be labeled 'no-write', got '${label}'"; fail=$((fail + 1)); } ;;
      */hollow/*)      [ "$label" = "write-but-hollow" ] || { echo "FAIL  ${path} : hollow/ fixture must be labeled 'write-but-hollow', got '${label}'"; fail=$((fail + 1)); } ;;
    esac

    e_expect="$(field EXPECT "$fpath")"
    e_why="$(field WHY "$fpath")"
    e_scenario="$(field SCENARIO "$fpath")"

    if [ -z "$e_scenario" ]; then
      echo "FAIL  ${path} : empty or missing SCENARIO"; fail=$((fail + 1))
    fi
    if [ -z "$e_expect" ]; then
      echo "FAIL  ${path} : empty or missing EXPECT label"; fail=$((fail + 1))
    elif ! is_valid_label "$e_expect"; then
      echo "FAIL  ${path} : in-file EXPECT '${e_expect}' not in {${VALID_LABELS}}"; fail=$((fail + 1))
    elif [ "$e_expect" != "$label" ]; then
      echo "FAIL  ${path} : in-file EXPECT '${e_expect}' != manifest label '${label}'"; fail=$((fail + 1))
    fi
    if [ -z "$e_why" ]; then
      echo "FAIL  ${path} : empty or missing WHY rationale"; fail=$((fail + 1))
    fi

    # write + write-but-hollow fixtures carry an ENTRY: reference block — validate
    # the nine schema fields are present (each LABEL: line recoverable by field()).
    case "$label" in
      write|write-but-hollow)
        for fld in $ENTRY_FIELDS; do
          # COUNTER-HYPOTHESIS is the only field allowed to be empty (only in the
          # hollow case — checked separately below). All other fields must be
          # populated in BOTH write and write-but-hollow blocks.
          val="$(field "$fld" "$fpath")"
          if [ "$fld" = "COUNTER-HYPOTHESIS" ]; then
            continue
          fi
          if [ -z "$val" ]; then
            echo "FAIL  ${path} : ENTRY field '${fld}:' empty or missing"; fail=$((fail + 1))
          fi
        done

        # OPTIONS must split on ' ~ ' into >= 3 non-empty options (DC0 / P7 shape).
        opts="$(field OPTIONS "$fpath")"
        if [ -n "$opts" ]; then
          nopt="$(printf '%s' "$opts" | awk -F' ~ ' '{
            c=0; for (j=1;j<=NF;j++){ t=$j; gsub(/^[ \t]+|[ \t]+$/,"",t); if (t!="") c++ } print c }')"
          if [ "${nopt:-0}" -lt 3 ]; then
            echo "FAIL  ${path} : OPTIONS splits to ${nopt:-0} non-empty options on ' ~ ' (need >= 3)"; fail=$((fail + 1))
          fi
        fi

        val="$(field COUNTER-HYPOTHESIS "$fpath")"
        if [ "$label" = "write" ]; then
          # a real decided entry: counter-hypothesis must be NON-hollow.
          if is_vacuous "$val"; then
            echo "FAIL  ${path} : write fixture COUNTER-HYPOTHESIS is empty-or-vacuous ('${val}') — a real entry needs a concrete falsifiable one"; fail=$((fail + 1))
          fi
        else
          # write-but-hollow: the DC4 detector NEGATIVE CONTROL. The
          # counter-hypothesis MUST be empty-or-on-the-denylist; if it is actually
          # concrete here, the negative control is wrong (the detector would have
          # nothing to catch).
          if ! is_vacuous "$val"; then
            echo "FAIL  ${path} : hollow fixture COUNTER-HYPOTHESIS is NOT hollow ('${val}') — the DC4 detector negative control requires an empty-or-denylist counter-hypothesis"; fail=$((fail + 1))
          fi
        fi
        ;;
    esac
  done

  # every fixture file on disk is in the manifest (no orphans)
  local disk_count manifest_count diskfile rel found j
  while IFS= read -r diskfile; do
    rel="${diskfile#${TEST_DIR}/}"
    found=0
    for j in "${!M_PATH[@]}"; do [ "${M_PATH[$j]}" = "$rel" ] && { found=1; break; }; done
    if [ "$found" -eq 0 ]; then
      echo "FAIL  ${rel} : fixture on disk but not in manifest (orphan)"; fail=$((fail + 1))
    fi
  done < <(find "${FIX}" -type f -name '*.md' | sort)

  disk_count="$(find "${FIX}" -type f -name '*.md' | wc -l | tr -d '[:space:]')"
  manifest_count="${#M_PATH[@]}"
  if [ "$disk_count" != "$manifest_count" ]; then
    echo "FAIL  manifest<->files count mismatch: ${manifest_count} manifest vs ${disk_count} on disk"
    fail=$((fail + 1))
  fi

  echo "-------------------------------------------------------------"
  echo "checked ${n} manifest entries / ${disk_count} fixture files"
  if [ "$fail" -eq 0 ]; then
    echo "check-corpus: PASS (well-formed)"
    exit 0
  else
    echo "check-corpus: FAIL (${fail} structural defect(s))"
    exit 1
  fi
}

# =============================================================================
# --judge : FLOOR evaluation (run by VERA against the live model+module)
# =============================================================================
#
# How it works (honest about its limit — the script does NOT classify):
#   1. PRINT each SCENARIO with its label HIDDEN, numbered, plus the module path.
#      The judging agent (VERA) reads the module and decides write/no-write for
#      each scenario using ONLY the module text, emitting calls to a calls-file.
#   2. RE-RUN with --judge --score <calls-file> to score the calls against the
#      manifest labels and report per-class accuracy vs the FLOORS.
#
# FLOORS (per-class; an aggregate could ace the easy class and miss the dangerous
# one — see README):
#   decided RECALL (decided/ -> write)               >= 4/5
#   illuminated SPECIFICITY (illuminated/ -> no-write) >= 3/4  (LOAD-BEARING)
#   problem SPECIFICITY (problem/ -> no-write)        >= 2/3
#   incidental SPECIFICITY (incidental/ -> no-write)  >= 2/3
# A miss in ANY class exits nonzero. (hollow/ is a --check-corpus negative control,
# not a --judge class: it is a should-write that happens to be hollow; the judge
# scores it as a write call, but its floor is the check-corpus hollow-detect, not a
# judge floor — so hollow/ is excluded from the judge scoring below.)

judge_present() {
  load_manifest
  echo "# decision-register --judge : decide write/no-write for each SCENARIO using ONLY the module."
  echo "# module: ${MODULE}"
  echo "#"
  echo "# For each numbered scenario emit ONE line to a calls-file:  <n><TAB><label>"
  echo "#   label in {write, no-write}."
  echo "#   write    = the predicate fires (checkpoint + DILEMMA + a path was chosen) -> record an entry."
  echo "#   no-write = the over-write/over-fire guard withholds (problem solved, dilemma"
  echo "#              illuminated-but-undecided, or an incidental mention)."
  echo "#   Then re-run:  run-decision-register-corpus.sh --judge --score <calls-file>"
  echo "# NOTE: VERA is the judge AND the gauntlet verifier (judge==verifier). A green"
  echo "#   result is a DOGFOOD PROXY, not an independent capture verification."
  echo "#============================================================================="
  local i path scen
  for i in "${!M_PATH[@]}"; do
    path="${M_PATH[$i]}"
    scen="$(field SCENARIO "${TEST_DIR}/${path}")"
    printf '%d\t%s\n' "$((i + 1))" "$scen"
  done
}

judge_score() {
  local calls="$1"
  [ -f "$calls" ] || { echo "FATAL: calls-file not found: $calls"; exit 2; }
  load_manifest

  local tab; tab="$(printf '\t')"
  declare -A CALL
  local n lbl
  while IFS= read -r line || [ -n "$line" ]; do
    case "$line" in ''|\#*) continue ;; esac
    IFS="$tab" read -r n lbl <<EOF
$line
EOF
    n="$(printf '%s' "$n" | tr -d '\r[:space:]')"
    lbl="$(printf '%s' "$lbl" | tr -d '\r' | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')"
    [ -n "$n" ] || continue
    CALL["$n"]="$lbl"
  done < "$calls"

  local dec_hit=0 dec_tot=0 ill_hit=0 ill_tot=0 prob_hit=0 prob_tot=0 inc_hit=0 inc_tot=0
  local i path got idx
  for i in "${!M_PATH[@]}"; do
    path="${M_PATH[$i]}"
    idx="$((i + 1))"; got="${CALL[$idx]:-<none>}"
    case "$path" in
      */decided/*)     dec_tot=$((dec_tot + 1));  [ "$got" = "write" ]    && dec_hit=$((dec_hit + 1)) ;;
      */illuminated/*) ill_tot=$((ill_tot + 1));  [ "$got" = "no-write" ] && ill_hit=$((ill_hit + 1)) ;;
      */problem/*)     prob_tot=$((prob_tot + 1)); [ "$got" = "no-write" ] && prob_hit=$((prob_hit + 1)) ;;
      */incidental/*)  inc_tot=$((inc_tot + 1));  [ "$got" = "no-write" ] && inc_hit=$((inc_hit + 1)) ;;
      */hollow/*)      ;;  # negative control for --check-corpus, not a --judge class
    esac
    case "$path" in
      */hollow/*) printf '%-2s  %-44s (hollow: check-corpus negative control, not judged)\n' "$idx" "${path##*/}" ;;
      *)          printf '%-2s  %-44s got=%s\n' "$idx" "${path##*/}" "$got" ;;
    esac
  done

  echo "-------------------------------------------------------------"
  echo "per-class accuracy vs FLOOR (granularity-limited, n small — see README):"
  local fail=0
  printf '  decided RECALL          : %d/%d (floor >= 4/5)\n' "$dec_hit" "$dec_tot"
  [ "$dec_hit" -ge 4 ] || { echo "    MISS: decided recall below floor"; fail=$((fail + 1)); }
  printf '  illuminated SPECIFICITY : %d/%d (floor >= 3/4, LOAD-BEARING)\n' "$ill_hit" "$ill_tot"
  [ "$ill_hit" -ge 3 ] || { echo "    MISS: illuminated specificity below floor (the dangerous over-write direction)"; fail=$((fail + 1)); }
  printf '  problem SPECIFICITY     : %d/%d (floor >= 2/3)\n' "$prob_hit" "$prob_tot"
  [ "$prob_hit" -ge 2 ] || { echo "    MISS: problem specificity below floor"; fail=$((fail + 1)); }
  printf '  incidental SPECIFICITY  : %d/%d (floor >= 2/3)\n' "$inc_hit" "$inc_tot"
  [ "$inc_hit" -ge 2 ] || { echo "    MISS: incidental specificity below floor"; fail=$((fail + 1)); }

  echo "-------------------------------------------------------------"
  if [ "$fail" -eq 0 ]; then
    echo "judge: PASS (all per-class floors met) -- DOGFOOD PROXY, not independent verification"
    exit 0
  else
    echo "judge: FAIL (${fail} class(es) below floor)"
    exit 1
  fi
}

# --- arg dispatch ------------------------------------------------------------
case "${1:-}" in
  --check-corpus) check_corpus ;;
  --judge)
    case "${2:-}" in
      --score) judge_score "${3:-}" ;;
      ''|*)    judge_present ;;
    esac ;;
  -h|--help|'') usage; exit 0 ;;
  *) echo "unknown arg: $1"; usage; exit 2 ;;
esac
