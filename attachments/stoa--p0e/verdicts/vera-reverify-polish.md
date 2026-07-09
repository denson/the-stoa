status: completed
ticket: stoa--p0e
verdict: pass
design_artifact_verified_against: substrate/skills/attribution-advisory/ (design rev2; targeted re-verify of CATO c1/c2/c3 polish commit b34e5e94 — changed surface only, P3a retirement surface untouched and NOT re-run per PLINY scope call)
build_verified: stoa--p0e/build @ b34e5e94 (worktree C:/Users/denso/claude_projects/the-stoa/.claude/worktrees/stoa--p0e-build)
probes_executed:
- probe_id: p1
  description: P4 (never-error / report-only) STATIC — the load-bearing property. Confirm advise.sh has no reachable non-zero exit and no permission-decision output after the c2 arg-guard.
  quadrant_classification: easy-easy — mechanical grep against source; detection and verification both trivial.
  command_or_method: grep -nE 'exit [1-9]|permissionDecision|"deny"' substrate/skills/attribution-advisory/advise.sh ; plus grep -niE 'deny|permission' to confirm all such mentions are comments-only.
  expected: no matches for the non-zero/deny pattern; every reachable exit is 'exit 0'; any deny/permission tokens live only in comment lines.
  observed: NO MATCHES for 'exit [1-9]|permissionDecision|"deny"'. The only two reachable exit statements are 'exit 0' (line 121 fail-open branch, line 294 tail). All deny/permission mentions (lines 7,9,11,13) are '#'-prefixed comments describing the never-blocks contract.
  result: pass
- probe_id: p2
  description: P4 EMPIRICAL — run advise.sh against p1 (flag), p2 (clean), empty diff, malformed diff; assert ALL exit 0 with no permissionDecision/deny in stdout or report.
  quadrant_classification: easy-easy — bounded fixture set, exit-code + string assertion.
  command_or_method: bash advise.sh --diff-file <fixture> --report-out <tmp> --principal-identity <hermetic-allowlist>, for fixtures p1-edit-copyright.diff, p2-newfile-principal.diff, an empty file, and a malformed/binary-ish file; capture rc + grep stdout/report for permissionDecision|"deny".
  expected: rc=0 for all four; no permission-decision output anywhere; p1 emits a PRIMARY finding, p2/empty/malformed emit 0 findings; reports carry the report-only framing.
  observed: p1_flag rc=0 (1 finding, PRIMARY section, "This is a REPORT, not a block. Nothing was prevented."); p2_clean rc=0 (0 findings); empty rc=0 (0 findings); malformed rc=0 (0 findings). No permissionDecision/deny in any stdout or report.
  result: pass
- probe_id: p3
  description: c2 arg-guard (the fix itself) — exercise the footgun 'advise.sh --diff-file --report-out <tmp>' and value-taking options missing their arg at end-of-args; confirm warn+default, --report-out honored (NOT swallowed), and all still exit 0.
  quadrant_classification: easy-easy — deterministic arg-parse behavior, exit-code + report-path assertion.
  command_or_method: bash advise.sh --diff-file --report-out <FG> ... (footgun); bash advise.sh ... --diff-file (missing value at end); bash advise.sh ... --report-out (missing value at end); capture rc, stderr, and whether the report landed at the requested path.
  expected: footgun warns '--diff-file expects a value' to stderr, does NOT consume --report-out as the diff-file value, honors --report-out (report written to the requested path), rc=0; missing-value-at-end cases warn + fall back to default, rc=0; no invocation newly exits non-zero.
  observed: footgun rc=0 — stderr "warning: --diff-file expects a value but none was given (next token: '--report-out'); ignoring it and using the default"; report WAS written to the requested footgun path (scanned 'git diff --cached', 0 findings) => --report-out honored, NOT swallowed. End-of-args --diff-file: rc=0, warns, falls back to cached default. End-of-args --report-out: rc=0, warns, falls back to default report path. No non-zero exit anywhere.
  result: pass
- probe_id: p4
  description: P1/P2 + supplementary — advise.sh changed, so re-run the shipped regression runner (P1 must-flag, P2 must-not-flag, s1/s2 SECONDARY/vendored, n1/n2 negatives, plus the P4 never-deny asserts and the static assert).
  quadrant_classification: hard-easy — the corpus/oracle is authored (discovery done by the shipped runner); executing it is a cheap re-run.
  command_or_method: bash substrate/skills/attribution-advisory/tests/run-attribution-advisory-tests.sh ; echo rc.
  expected: ALL PASS, rc=0; P1 flags a PRIMARY on LICENSE removed line; P2 reports 0 findings; s1 SECONDARY; s2 excluded; n1 clean; n2 PRIMARY fires (accepted r5); P4 exit-0/clean asserts pass; static assert (no exit 1/2, no permissionDecision, no deny token) passes.
  observed: 31/31 assertions PASS, RUNNER_RC=0. Includes "P1 findings >= 1", "P2 reports 0 findings", "advise.sh static: no exit 1/2, no permissionDecision, no deny token". Directly spot-confirmed in p2: P1 flags PRIMARY, P2 clean.
  result: pass
- probe_id: p5
  description: gen-data determinism — regen agents.ts; assert working tree CLEAN after regen (committed matches fresh regen), 2nd regen idempotent, and the ONLY agents.ts delta vs pre-build baseline is the attribution-advisory skill entry (now incl. the c1-updated description) with NO unrelated roster drift.
  quadrant_classification: easy-easy — regen + git-hash / git-diff comparison, deterministic.
  command_or_method: (cd app && npm run gen-data) x2; git status --porcelain app/src/data/generated/agents.ts; git hash-object before/after; git diff 96a71a88 -- app/src/data/generated/agents.ts (diffstat + added/removed line counts).
  expected: no working-tree diff after regen (committed hash == fresh-regen hash); 2nd regen idempotent (still clean); diff vs baseline 96a71a88 is purely additive (0 removed lines) = the single attribution-advisory skill object.
  observed: agents.ts hash unchanged across regen (97166a5a...4f8 before AND after); git status clean after both the 1st and 2nd regen (idempotent). Diff vs baseline 96a71a88 = 7 insertions / 0 deletions, a single LIEUTENANT attribution-advisory skill object whose description carries "Requires bash + python3 (... #!/usr/bin/env bash with set -o pipefail; the scanner is python3)" (the c1 fix). No roster drift; roster count unchanged (4 MAJOR / 12 CAPTAIN / 9 LIEUTENANT).
  result: pass
- probe_id: p6
  description: FS1 regression floor — the Stop self-check test suite still passes after the polish.
  quadrant_classification: easy-easy — shipped test suite, pass/fail on exit code.
  command_or_method: bash substrate/hooks/tests/run-stop-self-check-tests.sh ; echo rc.
  expected: 2 passed / 0 failed, rc=0.
  observed: "2 passed / 0 failed", FS1_RC=0 (assertion 1 first-Stop blocks + clause (E) sentinel; assertion 2 second-Stop same-turn allows).
  result: pass
threat_coverage:
- mitigation: M1
  threat: attribution erasure / license-breach (the plagiarism-direction — an existing author/copyright/license line MODIFIED or DELETED) surfaced report-only without falsely flagging legitimate PRINCIPAL-authored additions.
  defeats_via_probe: p4
  probe_evidence: run-attribution-advisory-tests.sh output (probe p4) — "PASS: P1 has PRIMARY section", "PASS: P1 names LICENSE", "PASS: P1 shows removed line", "PASS: P1 findings >= 1"; "PASS: P2 reports 0 findings", "PASS: P2 no PRIMARY", "PASS: P2 no SECONDARY". Also independently driven in probe p2 (p1_flag => PRIMARY on LICENSE; p2_clean => 0 findings).
  attack_path_exercised: (a) ATTACK — fixture p1-edit-copyright.diff removes 'Copyright (c) 2024 Jane Doe' from LICENSE; the advisory FIRES a PRIMARY finding surfacing the erasure (attack surfaced, not silently allowed). (b) LEGIT — fixture p2-newfile-principal.diff adds a new-file PRINCIPAL author field; the advisory stays SILENT (0 findings) => legitimate PRINCIPAL authorship is NOT falsely flagged. Both halves observed post-c2-arg-guard; the never-block/exit-0 property (P4) that the mitigation relies on is intact (probes p1+p2).
methodology_concerns: None of consequence. Scope note (not a defect): per the PLINY scope call this was a TARGETED re-verify of the b34e5e94 changed surface; the P3a retirement surface was untouched by the polish and deliberately not re-run here — the full-final-state P1-P4 re-run is the FM close-gate's job. The end-of-args --diff-file probe fell back to 'cached' mode and wrote a report to the worktree default path; that artifact is correctly excluded by the c3 .gitignore entry (git check-ignore confirmed), so it does not perturb the gen-data determinism check.
falsifying_evidence_summary: (empty — no probe falsified any design claim)
verification_artifacts_path: C:/Users/denso/AppData/Local/Temp/claude/C--Users-denso-claude-projects-the-stoa/822aa122-41c9-4a76-9a87-cfe6e4fdf4c5/scratchpad/ (p4_probe.sh + captured reports/err files) and this verdict at agents/verdicts/stoa--p0e/vera-reverify-polish.md
summary: Targeted re-verify of ADA's polish commit b34e5e94 (CATO c1/c2/c3) against the changed surface, verified by execution (fix-agent self-checks NOT trusted). The load-bearing property P4 (advise.sh must ALWAYS exit 0 and NEVER emit a deny) is intact after the c2 arg-guard: static grep finds only 'exit 0' reachable with deny/permission tokens comment-only, and empirical runs across flag/clean/empty/malformed inputs all exit 0 with no permission-decision output. The c2 arg-guard fix itself is correct — the '--diff-file --report-out X' footgun is CLOSED (the guard warns to stderr and HONORS --report-out rather than swallowing it), missing-value-at-end-of-args warns + falls back to a safe default, and no invocation newly exits non-zero. The shipped runner is 31/31 (P1 must-flag, P2 must-not-flag, s1/s2, n1/n2, P4 asserts, static assert). gen-data is deterministic and idempotent: the committed agents.ts is byte-identical to a fresh regen, a 2nd regen is a no-op, and the delta vs the pre-build baseline is a purely additive 7-line attribution-advisory skill entry carrying the c1-updated 'Requires bash + python3' description — no roster drift. FS1 stays 2/0. PASS.
verification_artifacts_path: agents/verdicts/stoa--p0e/vera-reverify-polish.md
