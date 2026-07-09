status: completed
ticket: stoa--p0e
verdict: pass
verification_type: targeted re-verify after fix (FM-affirmed scope reduction; coverage-floor conditions honored)
design_artifact_verified_against: agents/design/stoa--p0e/ (design rev2 §10 probe spec) — FS3 determinism assertion + FS1/FS2 regression floors
build_verified: stoa--p0e/build @ 141a4341 (ADA fix commit; c528f886 = build, 96a71a88 = pre-build baseline)
prior_verdict: agents/verdicts/stoa--p0e/vera-build.md (FAILed on FS3 only; P1/P2/P3a/P4 + supplementary + FS1/FS2 PASSED and are structurally isolated from a gen-data regen — NOT re-run, per FM-affirmed scope)

probes_executed:
- probe_id: FS3
  description: gen-data determinism — the fix ran npm run gen-data so committed agents.ts matches a fresh regen (closes the stale-data gap the prior verdict falsified).
  quadrant_classification: easy-easy
  quadrant_rationale: bug surfaces mechanically (stale committed data = a git diff after regen); verifying the fix is a bounded run-twice-and-diff, not an intractable state-space search.
  command_or_method: |
    (cd app && npm run gen-data)   # RUN 1 — canonical: tsx scripts/gen-data.ts, app/node_modules present
    git -C <worktree> diff -- app/src/data/generated/agents.ts   # assert CLEAN (committed == fresh regen)
    git diff 96a71a88 141a4341 -- app/src/data/generated/agents.ts   # assert net delta scoped to attribution-advisory
    (cd app && npm run gen-data)   # RUN 2 — assert idempotent (empty diff)
  expected: regen exit 0; working tree CLEAN after regen (committed matches fresh regen); net delta vs baseline = attribution-advisory skill entry ONLY (7-line / 0->3-ref add); 2nd regen idempotent (no further diff).
  observed: |
    RUN 1 exit 0 — "discovered 16 role file(s); wrote .../agents.ts; roster: 4 MAJOR / 12 CAPTAIN / 9 LIEUTENANT".
    git diff after RUN 1: EMPTY (working tree clean; committed agents.ts already matches a fresh regen — determinism holds, stale-data gap closed).
    Net delta 96a71a88 -> 141a4341 on agents.ts: EXACTLY the 7 added lines of the attribution-advisory LIEUTENANT skill entry (rank/name/description/body/filename block), 0->3 attribution-advisory refs. NO other roster change.
    RUN 2 exit 0; git diff EMPTY (idempotent); agents.ts blob hash 2e1e674f (matches committed blob + ADA-reported hash).
  result: pass
- probe_id: FS1
  description: regression floor — stop-self-check hook test suite still passes after the fix.
  quadrant_classification: easy-easy
  quadrant_rationale: run the suite, check exit code + assertion tally; fully mechanical.
  command_or_method: bash substrate/hooks/tests/run-stop-self-check-tests.sh
  expected: 2 passed / 0 failed, exit 0.
  observed: "PASS assertion 1 (first Stop blocks + clause (E) sentinel present); PASS assertion 2 (second Stop same turn allows); 2 passed / 0 failed"; exit 0.
  result: pass
- probe_id: FS2
  description: regression floor — install.sh dry-run still clean; attribution-advisory in deploy plan; retired deny-gate hook absent.
  quadrant_classification: easy-easy
  quadrant_rationale: run the dry-run against a throwaway target, grep the emitted plan; mechanical.
  command_or_method: bash substrate/install.sh --target project --project-dir <throwaway> --dry-run  (valid target form; throwaway target created + removed after)
  expected: exit 0; >=1 attribution-advisory deploy-plan line; 0 pretooluse-author-field-audit (retired hook) lines; 0 error/fatal lines; surviving gates present.
  observed: exit 0; 185 plan lines; attribution-advisory = 2 plan lines (deploy skill cp -R + pycache cleanup); pretooluse-author-field-audit = 0 (retired hook absent); error/fatal/no-such/denied lines = 0; 4 surviving-gate refs (clean-tree / no-dash-m / pretooluse).
  result: pass

threat_coverage:
- mitigation: M1
  threat: T-attribution-erasure (plagiarism / license-breach direction — an existing author/copyright/license line modified or deleted)
  defeats_via_probe: (carried forward — not re-executed in this targeted re-verify)
  probe_evidence: agents/verdicts/stoa--p0e/vera-build.md (prior full verdict — P1 must-flag + P2 must-not-flag executed WITH recorded evidence + a falsification control proving the allow-list is load-bearing)
  attack_path_exercised: M1 coverage was established + evidenced in the prior full verdict (P1 drove the attack path: a diff hunk MODIFYING/DELETING an existing copyright line -> PRIMARY fires; P2 confirmed a PRINCIPAL new-file does NOT fire). The FS3 gen-data fix touches ONLY app/src/data/generated/agents.ts, which is STRUCTURALLY ISOLATED from the M1 surface (advise.sh / principal-identity allow-list / settings). M1 coverage is therefore UNAFFECTED by this fix and is NOT re-executed here. NOTE: because no threat-anchored probe is in this dispatch's re-verify scope, this verdict's save-guard TRM_COUNT=0 (no new threat-ratified mitigation declared/executed); the binding lives in the prior verdict. This carry-forward is surfaced, not hidden.

methodology_concerns:
- FS2 required an EXISTING throwaway target dir (--target project --project-dir <path>, path must exist) — created + removed a throwaway target rather than mutating any real workspace (§25.5). No PRINCIPAL-gated / real-workspace-mutating probe in scope.
- Verdict body authored via the Write tool (this harness provides Write to the seat) rather than printf-redirection; on-disk integrity is the harness write + the sha256 recorded below for the durability/attach-failure contingency. Semantics identical to the canonical save-verdict round-trip.
- Scope-reduction is FM-affirmed on the record (P1/P2/P3a/P4 + supplementary NOT re-run — orthogonal to a gen-data regen). Both FM coverage-floor conditions honored: (1) the ACTUAL full gen-data regen was run so any pre-existing roster drift would surface — NONE surfaced (net delta = attribution-advisory only); (2) CATO cold-reads the full final diff incl. agents.ts as the backstop.

falsifying_evidence_summary: (empty — pass)

verification_artifacts_path: agents/verification/stoa--p0e/ (probe transcripts captured inline above; gen-data run outputs + git-diff evidence recorded in this verdict)

summary: TARGETED RE-VERIFY of ADA fix commit 141a4341 PASSES. FS3 (the fix): the ACTUAL canonical npm run gen-data was run (not asserted-away) — after regen the working tree is CLEAN, proving the committed agents.ts already matches a fresh regen, so the design's gen-data determinism assertion the prior verdict falsified now HOLDS and the stale-data gap is closed. The net agents.ts delta vs the pre-build baseline (96a71a88) is EXACTLY the 7-line attribution-advisory skill entry (0->3 refs) — no pre-existing roster drift surfaced (the FM's fix-scope constraint holds: the regen re-derives the whole roster and produced nothing but the attribution-advisory delta). A second regen is idempotent (blob 2e1e674f). FS1 (stop-self-check 2/0) and FS2 (install.sh --dry-run clean, exit 0, attribution-advisory in the deploy plan, retired pretooluse-author-field-audit hook absent, 0 error lines) remain green. The single falsification from the prior verdict is closed; core deliverable coverage (P1-P4 + supplementary) carries forward from vera-build.md unaffected (structurally isolated from a gen-data-only fix). Verdict: pass.
