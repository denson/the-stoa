status: completed
ticket: stoa--p0e
verdict: pass
diff_reviewed: 96a71a88..stoa--p0e/build (commits c528f886 retirement+advisory, 141a4341 gen-data regen) — FULL diff incl app/src/data/generated/agents.ts
design_artifact_compared_against: agents/design/stoa--p0e/design-rev2.md (+ PRINCIPAL SCOPE-RESHAPE ruling stoa--p0e 2026-07-09T09:07:01Z)
concerns:
- id: c1
  category: hygiene
  description: SKILL.md line 6 says the tool "Runs anywhere python3 + a POSIX shell are present", but advise.sh requires bash (shebang #!/usr/bin/env bash + set -o pipefail, which is not POSIX sh). Wording is slightly inaccurate; all invocation examples correctly say "bash advise.sh", so behavior is unaffected.
  evidence: substrate/skills/attribution-advisory/SKILL.md:6 vs advise.sh:1,41
  severity: minor
  quadrant_classification: easy-easy
- id: c2
  category: craft
  description: Arg parser consumes the next flag as a value when an option is given without its argument (e.g. "--diff-file --report-out X" makes DIFF_FILE="--report-out" and silently writes to the DEFAULT report path). This is by-design never-error / ignore-unknown-args robustness and is harmless under report-only, but a malformed invocation fails silently rather than warning.
  evidence: advise.sh:55-64 (shift 2 with no lookahead guard); reproduced empirically (rc=0, wrote default report)
  severity: minor
  quadrant_classification: easy-easy
- id: c3
  category: hygiene
  description: Running advise.sh from the substrate SOURCE tree with no --report-out resolves WORKSPACE three levels up to the repo root and writes .claude/attribution-advisory-report.md into the working tree (untracked). Harmless report artifact; the test runner always passes --report-out to scratch so it never pollutes. Informational.
  evidence: advise.sh:43-52 (WORKSPACE = SCRIPT_DIR/../../..)
  severity: minor
  quadrant_classification: easy-easy
follow_ups:
- Wiring advise.sh into the gauntlet close-gate (CATO/NOMOS) as an automatic review step — touches role files; correctly deferred by design §8 (out of scope this arc).
- Teaching check-substrate-updates hook-awareness to auto-flag the retired orphan script OBSOLETE — separate tooling arc; design §8. The orphan is inert-when-unregistered so this is not urgent.
- Extract the attribution term set to a shared data file if the _hooklib.sh vs advise.sh mirror (W3) is ever observed to drift; design §8.
verifier_coverage_assessment: >
  VERA covered the full design §10 probe spec — P1 (attack-detected: PRIMARY flags LICENSE + removed "Copyright (c) 2024 Jane Doe"), P2 (legit-unaffected: 0 findings WITH a load-bearing allow-list falsification control), P3a retirement asserts, P4 never-denies + static assert, s1/s2/n1/n2 supplementary, and FS1/FS2/FS3 regression floors. I independently re-ran the full suite (31/31 PASS) and FS1 (2/0 PASS), and EXTENDED coverage with adversarial probes VERA did not run: (a) command-injection via crafted diff content carrying $(...) and backticks — NO injection (diff content is read from a file into a fixed python -c program, never eval-ed); (b) ReDoS / catastrophic-backtracking on a 5000-char copyright name-run and a long field value — sub-second, no backtracking (the name-run and \s+ token classes are disjoint, so no ambiguity); (c) --report-out to a nonexistent nested dir — mkdir path works; (d) malformed/missing-arg invocations — never error, always exit 0. No surface VERA missed changes the verdict. Threat coverage for the sole threat-ratified mitigation M1 is intact: VERA cites defeats_via_probe P1 + P2, both present in its executed set with non-empty evidence; I independently drove both the attack-detected (P1 flags) and legit-unaffected (P2 clean) halves. SECONDARY/M2 is correctly not-threat-ratified (best-effort courtesy; §35.5 self-carve-out — no threat-coverage line owed).
summary: >
  Clean, disciplined, tightly-scoped diff that does exactly what design-rev2 specifies and nothing more. Retirement is complete and correct: the deny-hook registration is gone from BOTH .claude/settings.json and substrate/templates/settings-hooks.json (only the intended first object removed; surviving gates intact — 5 refs in live settings, 6 in the template incl. sessionstart-substrate-check; Stop/PostToolUse/SessionStart untouched); the script + author-gate corpus are archived to v1-historical via pure R100 renames (git mv, not delete); _hooklib.sh is byte-for-byte untouched; all 5 install.sh comment sites are corrected with NO surviving falsehood (zero "the commit is denied" / zero active-tense denier language outside history); README, tests/README, RETIREMENT.md, and the on-branch principal-identity comment fix are all accurate with allow-list VALUES unchanged. The advisory advise.sh is correct (PRIMARY name-agnostic removed-attribution classifier + SECONDARY new-non-PRINCIPAL-field classifier with vendored exclusion and fail-open allow-list), secure (no injection, no ReDoS), and structurally report-only (only exit 0 at lines 96/269; no reachable non-zero exit, no permissionDecision/deny — verified statically AND empirically across flagging/clean/empty/malformed inputs). agents.ts is exactly the 7-insert/0-delete attribution-advisory LIEUTENANT entry — no smuggled roster change. Authorship audit clean throughout (SKILL.md, RETIREMENT.md, design all author: Denson Smith; no non-PRINCIPAL authorship field anywhere). Both ADA deviations are acceptable: the bash shebash (dev-1) is MORE correct than the design text since the script uses set -o pipefail which is not POSIX sh and matches the surviving gates; the added --principal-identity flag / STOA_PRINCIPAL_IDENTITY_FILE env (dev-2) is necessary and additive (hermetic test allow-list) and does not touch the report-only property. The three findings are all minor/informational (a POSIX-shell wording nit, a silent-on-malformed-arg footgun, and a source-tree default-report-path note) — none blocking, none requiring revision. Overall posture: clean / ready for the final gate.