# RUNNER — tool-mediated probe execution

## Why this skill exists

Across the v0.3 → early-v0.4 arc, design-time probe specifications kept being approved as text by DAEDALUS and ARGUS, then failed at ADA build / VERA verify / CATO review when the probe was actually executed. d45 closed this for TypeScript compile claims; RUNNER closes it for the broader class — bash, Python, file existence, hash-compare, grep-against-actual-string. The discipline that DAEDALUS specifies a probe AND records its actual output, and ARGUS re-runs the probe to verify the output has not drifted, is the cu5.22 §6c invariant generalized to all tool-runnable probes.

## Preconditions

Run this skill when — and only when — all of the following hold:

- A request bead exists naming `RUNNER` as the lieutenant, a caller (DAEDALUS, ARGUS, or VERA per `team-spec.yaml` `callable_by`), a `command` (the probe's verbatim shell-string), and an `expected_exit` (the integer the caller asserts the command will return; 0 if unspecified).
- The caller is in RUNNER's `callable_by` list per the active team-spec.
- The artifact path `{{ARTIFACTS_DIR}}/runner/{{REQUEST_ID}}.txt` is writable.

If any precondition fails, emit a failure reply bead and return without executing the command. Do not silently skip.

## Input contract

The request bead's fields:

- `lieutenant: RUNNER`
- `caller: <officer-name>` — DAEDALUS, ARGUS, or VERA.
- `prompt: <free-text task description>` — for human readability and audit; not parsed by the skill.
- `inputs:`
  - `command: <shell-string>` — the verbatim command to execute. Required.
  - `expected_exit: <int>` — the exit code the caller asserts the command will return. Default 0.
  - `expected_output_match: <regex>` — optional. If provided, RUNNER applies the regex to the combined stdout+stderr and records pass/fail. If omitted, RUNNER does not assert any output content.
  - `cwd: <repo-relative-path>` — optional. The working directory the command runs in. Default is the worktree root (resolved by the skill from the caller's environment).

**Fields deliberately NOT in the input contract** (rationale in `agents/design/gauntlet-cu6.2/design.md` §3(b)):

- `files: list[path]` — RUNNER runs in the existing worktree; files already exist or do not. There is no "make these files available" step. If the caller needs files materialized first, the caller orchestrates that as a separate dispatch.
- `timeout_seconds` — Bash already has a 120000ms default timeout (per Claude Code's Bash tool). RUNNER inherits that bound. A caller wanting a longer or shorter bound passes the timeout through the command itself (e.g., `timeout 60 <real-command>`). Adding an explicit `timeout_seconds` field would duplicate Bash's bound and create the "which timeout wins" ambiguity.

## Output contract

RUNNER writes a single text artifact at `{{ARTIFACTS_DIR}}/runner/{{REQUEST_ID}}.txt` containing:

```
=== RUNNER record ===
request_id: <request-id>
caller: <officer-name>
command: <verbatim command string>
cwd: <resolved cwd, absolute>
expected_exit: <int>
expected_output_match: <regex or "(none)">

=== execution ===
exit_code: <int>
duration_ms: <int>
stdout_first_100_lines:
~~~~
<verbatim stdout, head -n 100; or "(empty)">
~~~~
stdout_total_lines: <int>
stderr_first_100_lines:
~~~~
<verbatim stderr, head -n 100; or "(empty)">
~~~~
stderr_total_lines: <int>

=== assertion ===
exit_match: <pass | fail>  (pass IFF exit_code == expected_exit)
output_match: <pass | fail | n/a>  (n/a if expected_output_match was not provided; pass IFF the regex matches the combined stdout+stderr)
overall: <pass | fail>  (pass IFF exit_match == pass AND (output_match == pass OR output_match == n/a))
```

The 4-tilde fence around stdout/stderr is load-bearing: it lets the captured output contain its own 3-backtick fences (e.g., a probe that grep's a markdown file) without nested-fence collision. Same convention as d45's §N artifact-template (§2.1.f.iii of d45's design).

The reply bead returned to PLINY is a status line only:

```
RUNNER complete: request=<request-id> overall=<pass|fail> exit=<exit_code>/<expected_exit> artifact=<artifact-path>
```

The caller reads the full record from disk on re-wake.

## Procedure

1. **Resolve cwd.** Default to the worktree root (the directory containing `gauntlet.config.yaml`). If `inputs.cwd` is provided and is a relative path, resolve it relative to the worktree root.

2. **Capture the command and a high-resolution start timestamp.** `START=$(date +%s%N)` (nanoseconds). The duration calculation tolerates nanosecond resolution.

3. **Execute via Bash with combined output capture.** Run the command, redirect stdout to one temp file and stderr to another, capture exit code:

   ```bash
   STDOUT_FILE=$(mktemp)
   STDERR_FILE=$(mktemp)
   bash -c "$COMMAND" > "$STDOUT_FILE" 2> "$STDERR_FILE"
   EXIT_CODE=$?
   END=$(date +%s%N)
   DURATION_MS=$(( (END - START) / 1000000 ))
   ```

   Combined output is NOT merged at the bash level (unlike d45's `2>&1` for tsc). RUNNER preserves the stdout/stderr distinction in the record so the caller can see which stream a diagnostic landed on. The d45 `2>&1` was specific to tsc's stdout-error behavior (microsoft/TypeScript issue #615); the general case benefits from preserving the distinction.

4. **Head-truncate to 100 lines per stream.** Use `head -n 100`. Record total line counts separately so the caller can detect truncation. Larger output is preserved at the temp file path (logged in the record's `(full output preserved at <temp-path>)` footer if truncation occurred).

5. **Compute exit_match.** `exit_match: pass` IFF `EXIT_CODE == expected_exit`, else `fail`.

6. **Compute output_match if expected_output_match was provided.** Use Python's `re.search` (multiline, dot-doesn't-match-newline default) against the combined `<stdout> + "\n" + <stderr>` text. Record `pass | fail`. If not provided, record `n/a`.

7. **Compute overall.** `pass` IFF `exit_match == pass AND (output_match in {pass, n/a})`.

8. **Write the artifact.** Format the record per the output contract. Use UTF-8, LF line endings.

9. **Return a status line only.** Do NOT include the captured stdout/stderr in the return — only the artifact path and the overall verdict. The caller reads from disk.

## Failure modes

- **Command not found / shell parse error.** `bash -c` returns a non-zero exit; RUNNER records the exit code and stderr verbatim. If the caller's `expected_exit` was 0, `exit_match: fail` and the record's stderr makes the diagnosis cheap.
- **Long-running command.** Bash's default 120000ms timeout kicks in. The captured stderr will name the timeout; RUNNER records the resulting non-zero exit. Callers with longer-running probes prefix the command with `timeout <N>` to set a tighter bound, or accept Bash's default.
- **Output > 100 lines per stream.** RUNNER head-truncates and notes total line count. The full output stays in the temp file at `STDOUT_FILE`/`STDERR_FILE` (path logged in the record); a caller that needs the full output reads from the temp path.
- **Regex compile error in expected_output_match.** Python's `re.compile` raises; RUNNER records `output_match: fail (regex compile error: <message>)` and treats overall as fail. Caller sees the error in the record and re-dispatches with a corrected regex.
- **Worktree not found / cwd unresolvable.** RUNNER records `exit_code: -1, exit_match: fail (cwd unresolvable: <path>)` and exits without running the command. Caller re-dispatches with a valid cwd.

## What this skill is NOT

- Not a substitute for VERA's verification (RUNNER's overall verdict is "the command did what was asserted"; VERA designs *what to assert against*, which is the harder judgment).
- Not a replacement for d45's `tsc --noEmit` discipline. d45 stays the canonical TypeScript compile-validation path; RUNNER fills the gap for everything else (bash, Python, file checks, hash-compare, grep).
- Not a fix-loop helper. RUNNER reports the result; the caller decides whether to revise the design or escalate. RUNNER does NOT retry on failure, does NOT propose remediations, does NOT self-correct command syntax.

## Preservation discipline

This skill ships in every instantiated downstream team. The source-of-truth lives in agent-gauntlet's repo at `skills/runner/SKILL.md`; `render.py`'s `copy_skills()` step (added by cu6.2 §2.12) walks `skills/` and copies every skill into `_gauntlet_install/staging/skills/`; `_gauntlet_install/deploy.sh` then copies the staged tree into the target project. The required-reading entries pointing at this file in DAEDALUS and ARGUS commissions are preserved across renames and re-templating. A rendered DAEDALUS or ARGUS that does not name this file in its required-reading list has no exposure to the discipline — same preservation logic as `fix-now-discipline.md` and `design-time-tool-validation.md`.
