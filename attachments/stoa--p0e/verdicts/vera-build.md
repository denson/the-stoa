status: completed
ticket: stoa--p0e
verdict: fail
design_artifact_verified_against: agents/design/stoa--p0e/design-rev2.md (§10 probe spec)
build_verified: stoa--p0e/build @ c528f886 (worktree C:\Users\denso\claude_projects\the-stoa\.claude\worktrees\stoa--p0e-build)

probes_executed:
- probe_id: P1
  description: MUST FLAG — threat-anchored (M1 attack-detected half). An edit to an existing copyright line must be flagged PRIMARY.
  quadrant_classification: easy-easy
  command_or_method: bash substrate/skills/attribution-advisory/advise.sh --diff-file tests/fixtures/p1-edit-copyright.diff --report-out <tmp> --principal-identity <vera-hermetic-allowlist>
  expected: exit 0; PRIMARY finding naming LICENSE + removed `Copyright (c) 2024 Jane Doe`; findings >= 1
  observed: exit 0; report has "## PRIMARY", "file: LICENSE (hunk @@ -1 +1 @@)", "removed: `Copyright (c) 2024 Jane Doe`"; findings: 1
  result: pass
- probe_id: P2
  description: MUST NOT FLAG — threat-anchored (M1 legit-unaffected half). New-file-by-PRINCIPAL diff must not be flagged. Plus a falsification control proving the allow-list is load-bearing.
  quadrant_classification: easy-easy
  command_or_method: bash advise.sh --diff-file tests/fixtures/p2-newfile-principal.diff --report-out <tmp> --principal-identity <allowlist WITH Denson Smith>; control = same fixture against an allow-list WITHOUT Denson Smith
  expected: exit 0; 0 findings (no PRIMARY — new file; no SECONDARY — value on allow-list). Control MUST flag SECONDARY (proves silence is meaningful, not SECONDARY globally dead).
  observed: exit 0; "findings: 0", "No attribution findings. (clean)". Control (allow-list without principal) -> exit 0, SECONDARY fires naming "authors = Denson Smith", findings: 1. => allow-list is load-bearing; P2 silence is a real match, not a dead check.
  result: pass
- probe_id: P3a
  description: deny-hook provably retired (worktree/build-branch half) + FM on-branch principal-identity amendment.
  quadrant_classification: easy-easy
  command_or_method: grep -c across .claude/settings.json + substrate/templates/settings-hooks.json; python JSON-structural PreToolUse.Bash object count; test -e/!-e on script + archive; grep on install.sh + hooks/tests/README + principal-identity
  expected: 0 audit-hook refs in both settings files; exactly 2 PreToolUse.Bash objects each (surviving clean-tree + no-dash-m gates); Stop/PostToolUse/SessionStart intact; script removed from substrate/hooks + archived at v1-historical; _hooklib present; install.sh 0 'the commit is denied' + no active-tense denier; README retitled + author-gate runner archived; principal-identity 0 'the commit is denied' + 0 audit refs, allow-list VALUES (denson / densonsmith2@gmail.com / Denson Smith) unchanged
  observed: grep pretooluse-author-field-audit = 0 in BOTH settings files. PreToolUse.Bash inner objects = 2 in BOTH (pretooluse-clean-tree-before-branch.sh + pretooluse-no-dash-m-bw-comment.sh); sections present = [PostToolUse, PreToolUse, SessionStart, Stop]; stop-self-check.sh/posttooluse-agent-checker-trigger.sh/sessionstart-compact-reprime.sh all live=1 tmpl=1, sessionstart-substrate-check.sh tmpl=1. test ! -e substrate/hooks/pretooluse-author-field-audit.sh OK; test -e substrate/v1-historical/hooks/... OK; _hooklib.sh present. install.sh 'the commit is denied' count = 0, no 'gate denies' active-tense line. hooks/tests/README title = "# Stop self-check regression corpus", run-author-gate-tests.sh refs = 0, archived at v1-historical OK. principal-identity: 'the commit is denied' = 0, pretooluse-author-field-audit = 0, all three allow-list VALUES present/unchanged, comment now reads "attribution-advisory skill's SECONDARY check ... NEVER blocked or denied — report-only".
  result: pass
- probe_id: P4
  description: advisory NEVER denies / NEVER exits non-zero (report-only proven).
  quadrant_classification: easy-easy
  command_or_method: run advise.sh against p1 (flag), p2 (clean), empty diff (printf '' | --stdin), malformed diff (printf 'not a diff\n@@ garbage' | --stdin); grep stdout+report for permissionDecision/"deny"; static grep -nE 'exit [12]|permissionDecision|"deny"' advise.sh
  expected: all four exit 0; no permissionDecision/"deny" token in any stdout or report; static assert finds no reachable deny/non-zero-exit path
  observed: p1/p2/empty/malformed all exit 0 with clean reports; NO deny token in any of the 4 report files or stdout; static grep returned no match (no reachable exit 1/2, no permissionDecision, no deny). advise.sh ends with unconditional `exit 0` (line 269); FAIL-OPEN throughout; no permission-decision JSON emitted anywhere.
  result: pass
- probe_id: s1
  description: supplementary (functional, NOT threat-anchored) — new non-principal author, non-vendored -> SECONDARY flags.
  quadrant_classification: easy-easy
  command_or_method: bash advise.sh --diff-file s1-newfile-nonprincipal.diff --principal-identity <allowlist>
  expected: exit 0; SECONDARY section naming "Mallory Example"
  observed: exit 0; findings 1; "## SECONDARY" present, names Mallory Example
  result: pass
- probe_id: s2
  description: supplementary — same non-principal field under node_modules/ -> vendored exclusion, NOT flagged.
  quadrant_classification: easy-easy
  command_or_method: bash advise.sh --diff-file s2-vendored-nonprincipal.diff --principal-identity <allowlist>
  expected: exit 0; 0 findings (vendored path excluded)
  observed: exit 0; "findings: 0"
  result: pass
- probe_id: n1
  description: supplementary negative — added prose merely discussing copyright (no year+name form) -> no finding.
  quadrant_classification: easy-easy
  command_or_method: bash advise.sh --diff-file n1-copyright-prose.diff --principal-identity <allowlist>
  expected: exit 0; 0 findings
  observed: exit 0; "findings: 0"
  result: pass
- probe_id: n2
  description: supplementary negative-control — copyright-year bump -> PRIMARY DOES fire (documents the accepted r5 name-agnostic false-positive as EXPECTED, not a regression).
  quadrant_classification: easy-easy
  command_or_method: bash advise.sh --diff-file n2-year-bump.diff --principal-identity <allowlist>
  expected: exit 0; PRIMARY DOES fire (name-agnostic)
  observed: exit 0; findings 1; "## PRIMARY" present. Confirms the accepted false-positive is KNOWN/documented behavior.
  result: pass
- probe_id: FS1
  description: full-suite regression — surviving Stop self-check hook test.
  quadrant_classification: easy-easy
  command_or_method: bash substrate/hooks/tests/run-stop-self-check-tests.sh
  expected: passes (infinite-block guard intact)
  observed: "2 passed / 0 failed" — assertion 1 (first Stop blocks + clause (E) sentinel) + assertion 2 (second Stop same turn allows). exit 0.
  result: pass
- probe_id: FS2
  description: full-suite regression — install.sh --dry-run smoke; attribution-advisory in skill deploy plan, retired hook absent, surviving gates deployed.
  quadrant_classification: easy-easy
  command_or_method: bash substrate/install.sh --target project --project-dir <fresh tmp> --dry-run
  expected: no error; attribution-advisory in deploy plan; pretooluse-author-field-audit NOT in deploy plan; surviving gates deployed
  observed: exit 0. "deploy skill: .../substrate/skills/attribution-advisory/ -> .../.claude/skills/attribution-advisory/ (cp -R)". pretooluse-author-field-audit ABSENT from the deploy plan. Both surviving gates (clean-tree + no-dash-m) deployed. No error/fatal/traceback lines.
  result: pass
- probe_id: FS3
  description: full-suite regression — npm run gen-data determinism (worktree diff, per the mixed-invocation memory note). DESIGN §10 asserts a fresh regen shows NO tracked change.
  quadrant_classification: easy-easy
  command_or_method: (worktree app dir) npm install; npm run gen-data; git -C <worktree> diff app/src/data/generated/agents.ts; second gen-data run for idempotency; git show HEAD:agents.ts vs regenerated
  expected: git diff shows NO change (design's literal assertion)
  observed: gen-data exit 0 (roster 4 MAJOR / 12 CAPTAIN / 9 LIEUTENANT; Zod adapter accepted the new skill — schema valid). BUT git diff shows a 7-line ADD to app/src/data/generated/agents.ts — the attribution-advisory skill entry. Committed HEAD:agents.ts has 0 'attribution-advisory' refs; regenerated has 3. A SECOND gen-data run produced the identical 7-line diff (no further growth) => gen-data is DETERMINISTIC/idempotent. The falsification is NOT non-determinism — it is STALE committed generated data: the build added the skill to substrate/ but never ran gen-data to refresh the app roster, so the committed generated artifact is out of sync with the substrate source.
  result: fail

threat_coverage:
- mitigation: M1
  threat: T-plagiarism/license-breach (a commit diff MODIFIES or DELETES an existing author/copyright/license/attribution line — another author's credit replaced with the PRINCIPAL's, or an upstream attribution erased)
  defeats_via_probe: P1
  probe_evidence: agents/verification/stoa--p0e/p1-report.md (PRIMARY finding: LICENSE, removed `Copyright (c) 2024 Jane Doe`, findings: 1) + agents/verification/stoa--p0e/p2-report.md (legit-unaffected: 0 findings) + p2-control.md (allow-list load-bearing proof)
  attack_path_exercised: P1 drove the ATTACK path (LICENSE line `Copyright (c) 2024 Jane Doe` -> `Copyright (c) 2024 Denson Smith`, i.e. another author's credit replaced with the PRINCIPAL's). (a) attack DETECTED — the PRIMARY hunk-classifier fired, naming LICENSE + the removed line, into the durable report, exit 0 (report-only detection, per design the mitigation is surfacing not prevention). (b) legit traffic NOT flagged — P2 drove the legitimate path (new-file-by-PRINCIPAL pyproject.toml authored by Denson Smith), 0 findings; the falsification control confirms that silence is a genuine allow-list match (SECONDARY fires when the principal is absent from the list), so (b) is meaningfully verified rather than a dead check.

methodology_concerns:
- FS3 is BOTH a real build-completeness gap AND a design-probe premise error, and I flag both. (1) BUILD gap: commit c528f886 added the attribution-advisory skill to substrate/ but did not run `npm run gen-data`, so app/src/data/generated/agents.ts is stale (missing the skill; 0 vs 3 refs). Project convention (CLAUDE.md: "run npm run gen-data after substrate edits") + memory ("agents.ts is worktree-safe") make regenerating + committing agents.ts on THIS branch the correct fix — cheap, deterministic, no slug dependency. (2) DESIGN-PROBE premise error: design-rev2 §10 asserts the gen-data determinism check should show "NO change", but that premise is wrong for an arc that ADDS a skill — a fresh regen necessarily adds the skill to the generated roster. The design's edit list also omitted a gen-data regen step for ADA. The probe as written conflates "determinism/idempotency" (which HOLDS — verified by the identical second run) with "committed generated data is current" (which does NOT hold). A future design should either (a) include the gen-data regen + commit in the ADA edit list and keep the NO-change assertion, or (b) reword the probe to assert idempotency + that the committed agents.ts already contains the newly-added skill.
- P1/P2/P3a/P4 probe specs were well-anchored and executable verbatim; no regex-anchoring or vagueness gaps (§5.11) surfaced. The shipped runner run-attribution-advisory-tests.sh ALL-PASS was confirmed NOT to be masking failures — I spot-executed advise.sh directly on each fixture with an independent VERA-authored hermetic allow-list and reproduced every result.
- Environmental note: the worktree app/ lacked node_modules; I ran `npm install` in the worktree to execute gen-data. This is a verification-side action; I restored app/src/data/generated/agents.ts to HEAD after capturing evidence (git checkout), leaving the deliverable's tracked state unmodified (independence-of-verification, §5.1).
- The two ADA build deviations were confirmed harmless to the probes: advise.sh uses `#!/usr/bin/env bash` (invoked as `bash advise.sh` throughout — no probe issue); the added `--principal-identity`/STOA_PRINCIPAL_IDENTITY_FILE flag defaults unchanged and enabled hermetic P1/P2 testing without depending on the target's real allow-list.

falsifying_evidence_summary: The core deliverable is sound — the threat-anchored M1 probes (P1 attack-detected, P2 legit-unaffected + load-bearing-allow-list control), the retirement asserts P3a (incl. the FM on-branch principal-identity amendment), the report-only proof P4, all four supplementary probes, and the stop-self-check + install.sh-dry-run regressions ALL PASS. The single falsification: the design-named gen-data determinism probe (FS3). `npm run gen-data` regenerates app/src/data/generated/agents.ts with a 7-line ADD of the attribution-advisory skill entry — the committed HEAD:agents.ts carries 0 'attribution-advisory' references while a fresh regen carries 3. gen-data is deterministic (an idempotent second run reproduced the identical diff), so this is not non-determinism; it is stale committed generated data — the build added the skill to the substrate source but never refreshed the app's generated roster, leaving the committed generated artifact out of sync with the substrate. The design's literal "git diff shows NO change" assertion is therefore falsified. The fix is trivial and worktree-safe (run `npm run gen-data`, commit agents.ts on stoa--p0e/build); per fix-known-bugs-immediately this should land before merge and then FS3 re-verifies clean.

verification_artifacts_path: agents/verification/stoa--p0e/ (vera-allowlist, vera-allowlist-empty-of-principal, p1-report.md, p2-report.md, p2-control.md, p4-empty.md, p4-malformed.md, s1-report.md, s2-report.md, n1-report.md, n2-report.md, install-dryrun.log)

summary: I executed the design-rev2 §10 probe set against the REAL substrate/skills/attribution-advisory/advise.sh at commit c528f886, running the shipped runner AND spot-executing advise.sh directly on every fixture with an independent VERA-authored hermetic allow-list to confirm the runner was not masking failures. The load-bearing empirical pair PASSED: P1 (an edit to an existing copyright line — Jane Doe replaced by the PRINCIPAL — IS flagged PRIMARY, naming LICENSE + the removed line) and P2 (a normal new-file-by-PRINCIPAL diff is NOT flagged), with a falsification control proving P2's silence is a genuine allow-list match rather than a dead SECONDARY check. The deny-gate retirement is provably complete on the branch (P3a: 0 audit-hook registrations in both settings files, exactly 2 surviving PreToolUse.Bash gates each, script archived to v1-historical, install.sh + principal-identity 'the commit is denied' falsehood eliminated with the allow-list VALUES intact, README retitled) and the advisory's report-only property is structural (P4: four inputs all exit 0, no permission-decision/deny token anywhere, static assert clean). The most important FAIL is FS3: the build added the attribution-advisory skill to the substrate source but did not run `npm run gen-data`, so the committed app roster data (agents.ts) is stale/out-of-sync (0 vs 3 skill refs) — gen-data itself is deterministic; the artifact was simply never regenerated. This is a cheap, worktree-safe fix (regenerate + commit agents.ts on the branch) that should land before merge; every other probe passes and the arc's authorship + threat-coverage duties are clean.
