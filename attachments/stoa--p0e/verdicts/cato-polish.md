status: completed
ticket: stoa--p0e
verdict: pass
diff_reviewed: b34e5e94 (git diff 141a4341..b34e5e94) — polish delta ONLY (advise.sh, SKILL.md, .gitignore, app/src/data/generated/agents.ts)
design_artifact_compared_against: substrate/skills/attribution-advisory/{SKILL.md,advise.sh} + prior CATO cold-read (agents/verdicts/stoa--p0e/cato-build-*.md; findings c1/c2/c3)
scope_note: LIGHT targeted re-glance of a polish delta, NOT a re-audit. VERA already ran the behavioral pass (re-verify PASS, runner 31/31). This is the craft/security cold-read of the c2 arg-guard change to advise.sh — the security surface VERA behavioral probes do not replicate.
resolution_of_prior_findings:
- c1 RESOLVED: SKILL.md and the regenerated agents.ts description now say "Requires bash + python3" with accurate rationale (bash shebang + pipefail); the false "runs anywhere ... a POSIX shell" claim is gone.
- c2 RESOLVED: the _val_ok / _warn_opt arg-guard closes the silent next-flag-swallow footgun; a value-taking option whose argument is missing or is itself a --flag now warns to stderr and falls back to the safe default without consuming the next token.
- c3 RESOLVED: /.claude/attribution-advisory-report.md is added to .gitignore; git check-ignore confirms the bare-run report is ignored (.gitignore:38) and it no longer appears in git status.
concerns:
- id: c1-nit
  category: hygiene
  description: The SKILL.md and agents.ts description say "set -o pipefail" but advise.sh:41 is "set -uo pipefail" (the description omits the -u nounset). Incomplete, not incorrect — the load-bearing "requires bash" claim rests correctly on pipefail plus the bash shebang.
  evidence: substrate/skills/attribution-advisory/SKILL.md description parenthetical vs advise.sh:41 (set -uo pipefail)
  severity: minor
  quadrant_classification: easy-easy
follow_ups: none — the delta is scoped exactly to the three prior findings; no out-of-scope drift or opportunistic change observed.
arg_guard_security_assessment: CLEAN. (1) No injection: _warn_opt uses the safe printf '%s\n' idiom with all interpolated data in the %s argument, so a value containing %s or backslashes cannot inject into the format string; option values are assigned literally with no eval or command substitution (probe 3: a --report-out value of $(touch pwned) did NOT execute — no pwned file, rc=0). (2) No new reachable non-zero exit and no permission-decision emission: static grep finds only exit 0 (lines 121, 294) and zero deny/permissionDecision/hookSpecificOutput tokens; the guard adds only stderr warnings. (3) shift arithmetic is safe: the true-branch shift 2 runs only when _val_ok guaranteed $2 is set, and the false-branch shift 1 runs with the flag still on the stack — no over-shift. (4) No unbounded/backtracking regex and no path-handling change introduced by the guard (the guard does no regex; REPORT_OUT is still quoted throughout). (5) Consistent: the identical guard is applied to all four value-taking options (--diff-file, --range, --report-out, --principal-identity); --stdin and the unknown-arg case are unchanged. The report-only / always-exit-0 (P4) invariant is PRESERVED.
empirical_probes:
- footgun (--diff-file --report-out X --stdin): warned to stderr, HONORED --report-out (report written at the honored path), rc=0.
- missing-value-at-end (--report-out with no following token): warned "next token: <end-of-args>", used default, rc=0.
- shell-metacharacter value (--report-out '$(touch pwned)'): assigned literally, no command executed, no pwned file, rc=0.
- flag-shaped mid-stream value (--report-out --range ...): fell back to default + warned, rc=0.
verifier_coverage_assessment: VERA behavioral re-verify (P4 static+empirical, footgun, runner 31/31, gen-data determinism, FS1) covered the load-bearing functional cases on this delta. My independent cold-read plus four adversarial arg-guard probes (footgun swallow, missing-value-at-end, shell-metacharacter value, flag-shaped mid-stream value) all returned rc=0 with no permission-decision output and no command execution; static grep confirms no reachable non-zero exit and no deny/permissionDecision token. No coverage gap on the polish delta.
summary: The polish delta is small (+35/-6, 4 files) and scoped exactly to my three prior findings. c1 (doc accuracy), c2 (arg-guard), and c3 (gitignore) are all RESOLVED. The new _val_ok / _warn_opt arg-guard is clean: safe printf %s idiom (no format-string injection), literal value assignment with no eval/command-substitution (metacharacter probe did not execute), safe shift arithmetic given the guard precondition, a consistent pattern across all four value-taking options, and — the security-critical point — the load-bearing report-only / always-exit-0 (P4) invariant is preserved (only exit 0 reachable, no permission-decision emitted). Only one minor non-blocking doc-nit remains (description says "set -o pipefail" where the script is "set -uo pipefail"). Overall posture: clean, ready for final gate.