#!/usr/bin/env bash
# Arc 23 — VERA supplementary probes for Phase 3 verification.
#
# Authored by: Denson Smith (CAPTAIN_VERA, Arc 23 Phase 3 verification).
# Purpose: extend ADA's content probes (probes.sh, 49/49 PASS) with the
# hard-easy and authorship probes the verification-complexity framework
# (op-disc §15) directs VERA to author for this arc.
#
# Run from the arc-23-build worktree root.
#
# Quadrant classification (per op-disc §15.1) per probe is in the
# per-probe label comments below. Most are easy-easy (file contains
# string). A handful are hard-easy (the work is in identifying what to
# compare across files; once identified, verification is cheap).

set -u

FAIL=0
PASS_COUNT=0
FAIL_COUNT=0

probe() {
  # $1 = label
  # $2 = command (eval'd)
  # $3 = expected ("nonzero-count" | "zero-count" | "exit-zero")
  local label="$1"
  local cmd="$2"
  local expected="$3"
  local out
  out=$(eval "$cmd" 2>&1)
  local rc=$?
  case "$expected" in
    nonzero-count)
      if [[ "$out" =~ ^[0-9]+$ ]] && [[ "$out" -gt 0 ]]; then
        PASS_COUNT=$((PASS_COUNT + 1))
        printf 'PASS  %s\n' "$label"
        return 0
      fi
      if echo "$out" | grep -Eq ':[1-9][0-9]*$'; then
        PASS_COUNT=$((PASS_COUNT + 1))
        printf 'PASS  %s\n' "$label"
        return 0
      fi
      FAIL_COUNT=$((FAIL_COUNT + 1))
      FAIL=1
      printf 'FAIL  %s\n      cmd=%s\n      out=%s\n' "$label" "$cmd" "$out" >&2
      return 1
      ;;
    zero-count)
      # passes if grep -c returned 0 OR multi-file output had no nonzero counts
      if [[ "$out" =~ ^[0-9]+$ ]] && [[ "$out" -eq 0 ]]; then
        PASS_COUNT=$((PASS_COUNT + 1))
        printf 'PASS  %s\n' "$label"
        return 0
      fi
      if [[ -z "$out" ]]; then
        PASS_COUNT=$((PASS_COUNT + 1))
        printf 'PASS  %s\n' "$label"
        return 0
      fi
      # multi-file: pass iff no line ends in :N>0
      if ! echo "$out" | grep -Eq ':[1-9][0-9]*$'; then
        PASS_COUNT=$((PASS_COUNT + 1))
        printf 'PASS  %s\n' "$label"
        return 0
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

echo "==> Arc 23 VERA supplementary probes"

# ============================================================
# Block A — design §3.5 row-by-row string-discipline cross-file
# Quadrant: hard-easy (cross-file string consistency; work is in
# identifying the constraint; once identified, mechanical to check).
# ============================================================

# Row 1: 'operating-disciplines.md §15' anchor in all four verifier role files.
# Note: ZENO uses the same anchor; row's "every file's new section" wording
# in design §3.5 applies to all four.
for f in CAPTAIN_VERA.md CAPTAIN_CATO.md CAPTAIN_ARGUS.md CAPTAIN_ZENO.md; do
  probe "design §3.5 row 1: 'operating-disciplines.md §15' anchor in $f" \
    "grep -c 'operating-disciplines.md\` §15\\|operating-disciplines.md §15' substrate/$f" \
    nonzero-count
done

# Row 2: full quadrant enumeration (easy-easy / hard-easy / easy-hard / hard-hard)
# Required: VERA §5.7, CATO §6.7, ARGUS §6.6 (full strategy-list)
# ZENO §6.6 references only hard-hard quadrant by design §3.5 row 2 note.
probe "design §3.5 row 2: full quadrant labels in VERA" \
  "grep -c 'easy-easy.*hard-easy.*easy-hard.*hard-hard\\|easy-easy | hard-easy | easy-hard | hard-hard' substrate/CAPTAIN_VERA.md" \
  nonzero-count
probe "design §3.5 row 2: full quadrant labels in CATO" \
  "grep -c 'easy-easy.*hard-easy.*easy-hard.*hard-hard\\|easy-easy | hard-easy | easy-hard | hard-hard' substrate/CAPTAIN_CATO.md" \
  nonzero-count
probe "design §3.5 row 2: full quadrant labels in ARGUS" \
  "grep -c 'easy-easy.*hard-easy.*easy-hard.*hard-hard\\|easy-easy | hard-easy | easy-hard | hard-hard' substrate/CAPTAIN_ARGUS.md" \
  nonzero-count
probe "design §3.5 row 2: hard-hard reference in ZENO (informational quadrant)" \
  "grep -c 'hard-hard' substrate/CAPTAIN_ZENO.md" \
  nonzero-count

# Row 3: bare INCOMPLETE / bare UNVERIFIABLE
# bare INCOMPLETE required: VERA, CATO, ARGUS (ZENO exempt per design §3.5)
# bare UNVERIFIABLE required: all four
# ZENO uses 'UNVERIFIABLE quadrant' qualifier form
probe "design §3.5 row 3: bare INCOMPLETE in VERA" \
  "grep -c '\\bINCOMPLETE\\b' substrate/CAPTAIN_VERA.md" \
  nonzero-count
probe "design §3.5 row 3: bare INCOMPLETE in CATO" \
  "grep -c '\\bINCOMPLETE\\b' substrate/CAPTAIN_CATO.md" \
  nonzero-count
probe "design §3.5 row 3: bare INCOMPLETE in ARGUS" \
  "grep -c '\\bINCOMPLETE\\b' substrate/CAPTAIN_ARGUS.md" \
  nonzero-count
probe "design §3.5 row 3: bare UNVERIFIABLE in VERA" \
  "grep -c '\\bUNVERIFIABLE\\b' substrate/CAPTAIN_VERA.md" \
  nonzero-count
probe "design §3.5 row 3: bare UNVERIFIABLE in CATO" \
  "grep -c '\\bUNVERIFIABLE\\b' substrate/CAPTAIN_CATO.md" \
  nonzero-count
probe "design §3.5 row 3: bare UNVERIFIABLE in ARGUS" \
  "grep -c '\\bUNVERIFIABLE\\b' substrate/CAPTAIN_ARGUS.md" \
  nonzero-count
probe "design §3.5 row 3: UNVERIFIABLE quadrant qualifier in ZENO" \
  "grep -c 'UNVERIFIABLE quadrant\\|UNVERIFIABLE per' substrate/CAPTAIN_ZENO.md" \
  nonzero-count

# Row 4: verifier-spins-forever required in VERA and ARGUS; CATO/ZENO exempt.
probe "design §3.5 row 4: verifier-spins-forever in VERA" \
  "grep -c 'verifier-spins-forever' substrate/CAPTAIN_VERA.md" \
  nonzero-count
probe "design §3.5 row 4: verifier-spins-forever in ARGUS" \
  "grep -c 'verifier-spins-forever' substrate/CAPTAIN_ARGUS.md" \
  nonzero-count

# Row 5: quadrant_classification: schema field in VERA, CATO, ARGUS (ZENO exempt).
probe "design §3.5 row 5: quadrant_classification: in VERA" \
  "grep -c 'quadrant_classification:' substrate/CAPTAIN_VERA.md" \
  nonzero-count
probe "design §3.5 row 5: quadrant_classification: in CATO" \
  "grep -c 'quadrant_classification:' substrate/CAPTAIN_CATO.md" \
  nonzero-count
probe "design §3.5 row 5: quadrant_classification: in ARGUS" \
  "grep -c 'quadrant_classification:' substrate/CAPTAIN_ARGUS.md" \
  nonzero-count
# ZENO is exempt — confirm it does NOT introduce a quadrant_classification field
probe "design §3.5 row 5: ZENO has NO quadrant_classification schema field" \
  "grep -c 'quadrant_classification:' substrate/CAPTAIN_ZENO.md" \
  zero-count

# ============================================================
# Block B — section-anchor cross-references resolve.
# Quadrant: easy-easy (string presence).
# ============================================================

probe "PLINY §5.6 cross-refs VERA §5.7 anchor" \
  "grep -c 'CAPTAIN_VERA.md\` §5.7' substrate/MAJOR_PLINY.md" \
  nonzero-count
probe "PLINY §5.6 cross-refs CATO §6.7 anchor" \
  "grep -c 'CAPTAIN_CATO.md\` §6.7' substrate/MAJOR_PLINY.md" \
  nonzero-count
probe "PLINY §5.6 cross-refs ARGUS §6.6 anchor" \
  "grep -c 'CAPTAIN_ARGUS.md\` §6.6' substrate/MAJOR_PLINY.md" \
  nonzero-count
probe "PLINY §5.6 cross-refs ZENO §6.6 anchor" \
  "grep -c 'CAPTAIN_ZENO.md\` §6.6' substrate/MAJOR_PLINY.md" \
  nonzero-count
probe "POLYBIUS §15 cross-refs op-disc §6.7.1" \
  "grep -c '§6.7.1' substrate/MAJOR_POLYBIUS.md" \
  nonzero-count
probe "PLINY §7.8 cross-refs op-disc §6.7.1" \
  "grep -c '§6.7.1' substrate/MAJOR_PLINY.md" \
  nonzero-count
probe "STRABO §6.6 cross-refs op-disc §15" \
  "grep -c 'operating-disciplines.md\` §15' substrate/CAPTAIN_STRABO.md" \
  nonzero-count

# ============================================================
# Block C — design-LOCKED specifics land verbatim.
# Quadrant: hard-easy (find the locked specific in design, check it lands).
# ============================================================

# A6: free-form prose, not JSONSchema — save-verdict file at user-tier
probe "save-verdict A6: caller-side enforcement language at user-tier" \
  "grep -c 'caller-side' $HOME/.claude/skills/save-verdict/SKILL.md" \
  nonzero-count

# A7: 10× INCOMPLETE budget — op-disc §15.5
probe "op-disc §15.5: 10× INCOMPLETE multiplier present" \
  "grep -c '10× the dispatch.s normal probe budget\\|10×.*normal probe budget' substrate/operating-disciplines.md" \
  nonzero-count

# A7: ~1× UNVERIFIABLE budget — op-disc §15.5
probe "op-disc §15.5: ~1× UNVERIFIABLE budget present" \
  "grep -c '1× normal probe budget' substrate/operating-disciplines.md" \
  nonzero-count

# A8: sampling YAML canonical form — keyword 'full' or bare integer
probe "VERA §5.8: 'sampling: full' canonical form" \
  "grep -c 'sampling: full' substrate/CAPTAIN_VERA.md" \
  nonzero-count
probe "PLINY §5.5: 'sampling: full' canonical form" \
  "grep -c 'sampling: full' substrate/MAJOR_PLINY.md" \
  nonzero-count
# Confirm the discarded YAML-awkward form 'sampling: N=3' is NOT used
probe "VERA §5.8: discarded 'sampling: N=3' form absent" \
  "grep -c 'sampling: N=3' substrate/CAPTAIN_VERA.md" \
  zero-count
probe "PLINY §5.5: discarded 'sampling: N=3' form absent" \
  "grep -c 'sampling: N=3' substrate/MAJOR_PLINY.md" \
  zero-count

# Save-verdict file at user-tier has the 4 new INCOMPLETE/UNVERIFIABLE failure modes
probe "save-verdict: INCOMPLETE failure mode (coverage_description)" \
  "grep -c 'INCOMPLETE verdict requires coverage_description' $HOME/.claude/skills/save-verdict/SKILL.md" \
  nonzero-count
probe "save-verdict: UNVERIFIABLE failure mode (sanity_check + recommended_next)" \
  "grep -c 'UNVERIFIABLE verdict requires sanity_check_performed AND recommended_next_step' $HOME/.claude/skills/save-verdict/SKILL.md" \
  nonzero-count
probe "save-verdict: missing quadrant_classification failure mode" \
  "grep -c 'INCOMPLETE / UNVERIFIABLE verdicts require quadrant_classification' $HOME/.claude/skills/save-verdict/SKILL.md" \
  nonzero-count
probe "save-verdict: quadrant_classification enum check failure mode" \
  "grep -c 'quadrant_classification must be one of' $HOME/.claude/skills/save-verdict/SKILL.md" \
  nonzero-count

# Save-verdict file documents the 5 new input fields (verdict_shape + 4)
probe "save-verdict: input field verdict_shape: documented" \
  "grep -c 'verdict_shape:' $HOME/.claude/skills/save-verdict/SKILL.md" \
  nonzero-count
probe "save-verdict: input field quadrant_classification: documented" \
  "grep -c 'quadrant_classification:' $HOME/.claude/skills/save-verdict/SKILL.md" \
  nonzero-count
probe "save-verdict: input field coverage_description: documented" \
  "grep -c 'coverage_description:' $HOME/.claude/skills/save-verdict/SKILL.md" \
  nonzero-count
probe "save-verdict: input field sanity_check_performed: documented" \
  "grep -c 'sanity_check_performed:' $HOME/.claude/skills/save-verdict/SKILL.md" \
  nonzero-count
probe "save-verdict: input field recommended_next_step: documented" \
  "grep -c 'recommended_next_step:' $HOME/.claude/skills/save-verdict/SKILL.md" \
  nonzero-count

# Save-verdict caveat-paragraph about executable-not-yet-authored present
probe "save-verdict: 2026-05-12 executable-not-yet-authored caveat present" \
  "grep -c 'Caveat on executable enforcement (2026-05-12)' $HOME/.claude/skills/save-verdict/SKILL.md" \
  nonzero-count

# ============================================================
# Block D — authorship audit
# Quadrant: easy-easy. Per the PRINCIPAL's standing rule.
# ============================================================

# No literal "author: <not-Denson>" YAML frontmatter in any touched substrate file.
# Substrate role files use the PRINCIPAL convention (no author: line at all);
# probe is that no foreign author field has crept in.
for f in CAPTAIN_VERA.md CAPTAIN_CATO.md CAPTAIN_ARGUS.md CAPTAIN_ZENO.md CAPTAIN_STRABO.md MAJOR_PLINY.md MAJOR_POLYBIUS.md operating-disciplines.md; do
  probe "authorship: $f has no 'author:' YAML frontmatter line" \
    "grep -c '^author:' substrate/$f" \
    zero-count
done

# probes.sh authored by Denson Smith
probe "authorship: probes.sh credits Denson Smith" \
  "grep -c 'Authored by: Denson Smith' agents/probes/arc-23/probes.sh" \
  nonzero-count

# ============================================================
# Block E — branch / build-state invariants
# Quadrant: easy-easy. Read git state.
# ============================================================

probe "git: HEAD is on arc-23/build branch" \
  "git rev-parse --abbrev-ref HEAD | grep -c 'arc-23/build'" \
  nonzero-count
probe "git: no uncommitted changes" \
  "git status --porcelain | wc -l | tr -d ' '" \
  zero-count
probe "git: HEAD is ahead of main (≥1 commit)" \
  "git rev-list --count main..HEAD | awk '{print (\$1 > 0) ? \"yes\" : 0}' | grep -c yes" \
  nonzero-count

# ============================================================
# Block F — install.sh deploy-plan still resolves with new files preserved
# Quadrant: easy-easy. Re-run dry-run, confirm role files appear.
# (Duplicates the §8.4 smoke beat as a VERA-side independence check.)
# ============================================================

probe "install.sh dry-run completes (target=user)" \
  "bash substrate/install.sh --dry-run --target user > /dev/null 2>&1" \
  exit-zero
probe "install.sh user-target lists MAJOR_PLINY.md" \
  "bash substrate/install.sh --dry-run --target user 2>&1 | grep -c 'MAJOR_PLINY.md'" \
  nonzero-count
probe "install.sh user-target lists MAJOR_POLYBIUS.md" \
  "bash substrate/install.sh --dry-run --target user 2>&1 | grep -c 'MAJOR_POLYBIUS.md'" \
  nonzero-count
probe "install.sh user-target lists operating-disciplines.md" \
  "bash substrate/install.sh --dry-run --target user 2>&1 | grep -c 'operating-disciplines.md'" \
  nonzero-count

# ============================================================
# Block G — design §3.5 verbatim section-number alignment
# Quadrant: hard-easy (work was reading the design's table; verification is grep).
# ============================================================

# Section numbers per design §3 table:
probe "design alignment: VERA §5.7 lands at expected number" \
  "grep -c '^### 5.7 Verification-complexity quadrant per probe' substrate/CAPTAIN_VERA.md" \
  nonzero-count
probe "design alignment: VERA §5.8 STRABO-claim verification" \
  "grep -c '^### 5.8 STRABO-claim verification' substrate/CAPTAIN_VERA.md" \
  nonzero-count
probe "design alignment: CATO §6.7 lands at expected number" \
  "grep -c '^### 6.7 Verification-complexity quadrant per finding' substrate/CAPTAIN_CATO.md" \
  nonzero-count
probe "design alignment: CATO §6.8 lands at expected number" \
  "grep -c '^### 6.8 Empirical environment reproduction' substrate/CAPTAIN_CATO.md" \
  nonzero-count
probe "design alignment: ARGUS §6.6 lands at expected number" \
  "grep -c '^### 6.6 Verification-complexity quadrant per risk' substrate/CAPTAIN_ARGUS.md" \
  nonzero-count
probe "design alignment: ZENO §6.6 lands at expected number" \
  "grep -c '^### 6.6 Verification-complexity quadrant per criterion' substrate/CAPTAIN_ZENO.md" \
  nonzero-count
probe "design alignment: STRABO §6.6 lands at expected number" \
  "grep -c '^### 6.6 Output is preliminary until VERA-verified' substrate/CAPTAIN_STRABO.md" \
  nonzero-count
probe "design alignment: PLINY §5.5 post-STRABO VERA dispatch" \
  "grep -c '^### 5.5 Post-STRABO VERA dispatch' substrate/MAJOR_PLINY.md" \
  nonzero-count
probe "design alignment: PLINY §5.6 INCOMPLETE / UNVERIFIABLE handling" \
  "grep -c '^### 5.6 Dispatch protocol for INCOMPLETE and UNVERIFIABLE' substrate/MAJOR_PLINY.md" \
  nonzero-count
probe "design alignment: PLINY §5.7 smoke-beat discipline" \
  "grep -c '^### 5.7 Smoke-beat discipline' substrate/MAJOR_PLINY.md" \
  nonzero-count
probe "design alignment: PLINY §7.8 no-narrowing-gauntlet-from-N=1" \
  "grep -c '^### 7.8 No-narrowing-gauntlet-from-N=1' substrate/MAJOR_PLINY.md" \
  nonzero-count
probe "design alignment: POLYBIUS §15 retrospective discipline" \
  "grep -c '^## 15. Retrospective discipline' substrate/MAJOR_POLYBIUS.md" \
  nonzero-count

# ============================================================
# Summary
# ============================================================

echo
echo "==> VERA supplementary probe summary"
echo "PASS: $PASS_COUNT"
echo "FAIL: $FAIL_COUNT"

if [[ $FAIL -ne 0 ]]; then
  echo "==> Failures present."
  exit 1
fi

echo "==> All VERA supplementary probes passed."
exit 0
