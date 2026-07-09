# CAPTAIN_NOMOS ground-truth audit -- arc stoa--p0e

Seat: CAPTAIN_NOMOS_the_stoa (subagent) | caller-sid 822aa122-41c9-4a76-9a87-cfe6e4fdf4c5
Dispatched by: PLINY_the-stoa | operating-mode: autonomous
Audited output: the arc stoa--p0e orchestrator output -- the 3-commit build set on stoa--p0e/build plus the PLINY hand-back stream culminating in HAND-BACK 9 (2026-07-09T20:53:41Z), against bw tickets stoa--p0e + stoa--dps and the repo at branch HEAD b34e5e94.

## VERDICT: DIVERGENT

Every enumerated build/retirement/advisory/bw/invariant claim (probes A-E) is CONFORMANT against ground truth. The build deliverable is sound. The single divergence is a verifier-coverage overclaim in the orchestrator HAND-BACK 9 summary (CATO-PASS across all 3 commits), which the bw+git record contradicts and which the FM (POLYBIUS_the-stoa v3) itself flagged at 2026-07-09T20:56:32Z and is holding the close on. Because at least one claim in the orchestrator output contradicts ground truth, the overall verdict is DIVERGENT; the output must not propagate to CLOSE / Decider hand-up carrying that claim.

## Per-item table

### A. Commit set + authorship/trailers -- CONFORMANT
All 3 commits exist on stoa--p0e/build. git show -s:
- c528f886 retire deny-gate + advisory. Author denson <densonsmith2@gmail.com> (PRINCIPAL, NOT overridden); trailer Co-Authored-By: CAPTAIN_ADA_the-stoa <captain-ada@the-stoa.local> present.
- 141a4341 gen-data regen. Same Author; same ADA trailer present.
- b34e5e94 CATO c1/c2/c3 polish. Same Author; same ADA trailer present.
Each also carries Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>. Author field is the PRINCIPAL on all three; no override. CONFORMANT.

### B. Retirement reality (repo at branch HEAD) -- CONFORMANT
- pretooluse-author-field-audit registration ABSENT (grep -c = 0) from BOTH .claude/settings.json and substrate/templates/settings-hooks.json.
- Both surviving Bash gates registered (grep -c = 1 each) in BOTH files: pretooluse-clean-tree-before-branch, pretooluse-no-dash-m-bw-comment.
- Stop/PostToolUse/SessionStart entries intact (grep -cE = 3 each file).
- substrate/hooks/pretooluse-author-field-audit.sh ABSENT from source; substrate/v1-historical/hooks/pretooluse-author-field-audit.sh PRESENT. git diff --find-renames --name-status 96a71a88..HEAD shows R100 (rename, NOT delete+add).
- author-gate tests + all tp/fp/control fixtures + run-author-gate-tests.sh moved to substrate/v1-historical/hooks/tests/ (all R100 renames).
- run-stop-self-check-tests.sh + fixtures/stop-event-orchestrator.json REMAIN under substrate/hooks/tests/.
- substrate/hooks/_hooklib.sh byte-unchanged vs 96a71a88: diff 0 lines; blob hash identical (baseline 34c7291346... == branch 34c7291346...).
- substrate/install.sh: grep -c of the deny-message string = 0; attribution-advisory present in SKILL_NAMES (line 238, array opens line 229).
- .claude/hooks/principal-identity: grep -c of the deny-message string = 0 AND grep -c pretooluse-author-field-audit = 0; allow-list VALUES denson / densonsmith2@gmail.com / Denson Smith all still present.
CONFORMANT.

### C. Advisory shipped -- CONFORMANT
- substrate/skills/attribution-advisory/ advise.sh + SKILL.md + tests/ all present.
- app/src/data/generated/agents.ts contains the attribution-advisory skill entry (grep -c = 3, matching the 0->3 delta VERA/CATO verified).
CONFORMANT.

### D. bw ground truth -- CONFORMANT
- stoa--dps is CLOSED (bw list shows the closed check marker) with ADA superseded-by-retirement close comment (2026-07-09T20:07:46Z): the PEP 621 fix is MOOT because the deny-gate is retired, not fixed.
- PRINCIPAL-gate ratification evidence on stoa--p0e: the [PRINCIPAL RULING -- SCOPE RESHAPE: deny-gates RETIRED] comment from Polybius the Decider (user-tier), timestamp 2026-07-09T09:07:01Z, authorizing the retirement. PLINY A1 ratification-restatement present (RADIO-CHECK read-back + HAND-BACK 2/3 A1 restatement, all M-item classifications ARGUS-CONFIRMED). FM design-close PASS present: POLYBIUS_the-stoa v3 DESIGN-CLOSE VERDICT PASS on design-rev2 (20:46:58Z) + ADA GREENLIGHT. ARGUS M-item confirmations present (all 6 M-items confirmed; retirement carve-out a genuine ARGUS confirmation).
- Gauntlet verdicts attached on the beadwork branch under attachments/stoa--p0e/verdicts/: argus-design-rev1.md, vera-build.md, vera-reverify.md, cato-build-20260709T203818Z.md, vera-reverify-polish.md (all 5 present, git ls-tree beadwork).
CONFORMANT.

### E. Invariant preservation -- CONFORMANT
- CLAUDE.md UNCHANGED in the branch diff: git diff 96a71a88..stoa--p0e/build -- CLAUDE.md = 0 lines. Authorship doctrine (invariant 6) not edited.
- No merge to main / no push: branch NOT in git branch --merged main; git merge-base --is-ancestor stoa--p0e/build main = false (not an ancestor of main); main == origin/main @ 96a71a88 (no advance).
CONFORMANT.

## F. Divergence -- CATO-coverage overclaim in HAND-BACK 9

- type: ticket-state (claim about verifier/verdict-review state contradicted by the record)
- detail: PLINY HAND-BACK 9 (2026-07-09T20:53:41Z) asserts BUILD NOW FULLY VERA-PASS + CATO-PASS across all 3 commits (c528f886 build + 141a4341 gen-data-fix + b34e5e94 polish). Ground truth: CATO reviewed only 2 of the 3 commits. The polish commit b34e5e94, which MODIFIED the security surface advise.sh (the c2 arg-guard), has NO CATO coverage.
- evidence:
  - CATO verdict comment landed 2026-07-09T20:38:53Z and by its own text cold-read both commits (c528f886 + 141a4341 incl. agents.ts). Attached artifact: verdicts/cato-build-20260709T203818Z.md (sha 7138045b).
  - git show -s b34e5e94 -> author/commit date 2026-07-09T14:45:17-06:00 = 20:45:17Z, i.e. ~6.4 min AFTER the CATO verdict. CATO could not have reviewed it.
  - git ls-tree -r beadwork attachments/stoa--p0e/verdicts/ lists exactly: argus-design-rev1.md, cato-build-20260709T203818Z.md, vera-build.md, vera-reverify.md, vera-reverify-polish.md. NO cato-polish / cato re-glance verdict exists. The only polish coverage is VERA behavioral re-verify (vera-reverify-polish.md) + ADA self-check.
  - FM POLYBIUS_the-stoa v3 posted HOLD-BEFORE-CLOSE COVERAGE CORRECTION at 2026-07-09T20:56:32Z stating the HB9 CATO-PASS-across-all-3-commits claim is INACCURATE and must NOT propagate into the arc-record / NOMOS / Decider hand-up, and is holding the close until a targeted CATO re-glance of the b34e5e94 +35/-6 delta lands.
- classification: BLOCKED. The arc CLOSE is blocked pending the CATO polish re-glance of b34e5e94; the CATO-PASS-across-all-3-commits statement cannot stand until that verifier coverage exists. This is NOT a build defect and NOT a decomposition failure (SIZE-DERAIL): the build artifacts (probes A-E) are all CONFORMANT and the P4 frozen surface is preserved per VERA. It is a verifier-coverage gap plus an over-broad coverage statement in the orchestrator output. Route: obtain the missing CATO coverage on b34e5e94 (the FM already-issued HOLD), then restate the coverage claim accurately before CLOSE / Decider hand-up. NOMOS does not prescribe the fix beyond naming the gap; the FM has already routed it.

## ground_truth_consulted
- Repo (worktree stoa--p0e-build, branch stoa--p0e/build): git show -s --format (c528f886, 141a4341, b34e5e94: author + trailers + dates); git diff --find-renames --name-status 96a71a88..stoa--p0e/build; git rev-parse 96a71a88:substrate/hooks/_hooklib.sh vs branch; git diff 96a71a88..stoa--p0e/build -- CLAUDE.md; git branch --merged main; git merge-base --is-ancestor; git rev-parse main origin/main; git ls-tree -r beadwork attachments/stoa--p0e.
- grep -c probes on .claude/settings.json, substrate/templates/settings-hooks.json, substrate/install.sh, .claude/hooks/principal-identity, app/src/data/generated/agents.ts.
- bw: bw show stoa--p0e (full comment stream: PRINCIPAL RULING 09:07:01Z, FM design-close PASS 20:46:58Z, ARGUS M-items, PLINY HB9 20:53:41Z, FM HOLD 20:56:32Z); bw list --all (stoa--dps closed); bw show stoa--dps (superseded-by-retirement close comment).

## summary
Audited the arc stoa--p0e orchestrator output (the 3-commit build set c528f886 / 141a4341 / b34e5e94 plus the PLINY hand-back stream) against bw (stoa--p0e, stoa--dps) and the repo at branch HEAD. Every enumerated build claim is CONFORMANT: authorship is the PRINCIPAL with the ADA seat trailer on all three commits; the deny-gate is retired by pure R100 archive-renames with _hooklib byte-unchanged and both surviving gates intact; the report-only advisory + agents.ts entry shipped; stoa--dps is closed superseded-by-retirement; PRINCIPAL-gate ratification (Decider SCOPE-RESHAPE ruling + PLINY A1 + FM design-close PASS + ARGUS M-item confirmations) is on the record; all 5 gauntlet verdicts are attached; CLAUDE.md doctrine is untouched and nothing merged/pushed. The load-bearing divergence is not in the build: it is in the orchestrator coverage STATEMENT. HAND-BACK 9 claims CATO-PASS across all 3 commits, but the CATO verdict (20:38:53Z) predates the polish commit b34e5e94 (20:45:17Z) by ~6.4 min and never reviewed it, no CATO polish verdict is attached, and the FM already issued a HOLD-BEFORE-CLOSE (20:56:32Z) flagging exactly this overclaim. Overall DIVERGENT (classification BLOCKED): the build is clean but the close is correctly blocked until CATO covers b34e5e94 and the coverage claim is restated accurately. The NOMOS verdict itself must not be read as endorsing the all-3-commits-CATO-PASS claim.
