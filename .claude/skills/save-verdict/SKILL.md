---
name: save-verdict
description: "Write a structured verdict to disk in the canonical verdict format. Use as the standard exit-write for VERA / CATO / ARGUS verdicts."
author: Denson Smith
---

# SAVE_VERDICT — canonical-path verdict saving

## Why this skill exists

CAPTAIN envelopes individually decide where to save verdicts: ARGUS picks one path, VERA picks another, CATO writes to /tmp/. The result is verdicts scattered across the filesystem with no single place to find them, and inconsistent naming conventions that make cross-ticket aggregation brittle.

SAVE_VERDICT formalizes one path: `agents/verdicts/<ticket-id>/<officer>-<timestamp>.md`. Verdict-producing officers dispatch SAVE_VERDICT with the verdict body and metadata; the lieutenant computes the canonical path, writes the body with sha256 round-trip verification, returns the resolved path. Officers stop deciding "where"; they only decide "what."

It specializes `write_with_verify` from `_lib/byte_copy.py` (private to this skill in Arc 39; cross-skill share with COPY_ARTIFACT + TRANSCRIBE_BW_TO_DISK deferred to substrate ticket stoa--sp1 per directive A2 α + A20).

## Preconditions

Run this skill when — and only when — all of the following hold:

- A request bead names `SAVE_VERDICT` as the lieutenant, a caller (any officer in `callable_by`), and `inputs.ticket_id`, `inputs.officer`, and exactly one of `inputs.body` or `inputs.body_path`.
- The officer name matches `^[A-Z][A-Z0-9_]*$` (uppercase identifier; matches the team-spec officer-name convention).
- The ticket id matches `^[a-zA-Z0-9._-]+$` (no path separators, no shell-meta).
- The `agents/verdicts/<ticket-id>/` directory is writable (created if missing).

## Input contract

Request bead fields:

- `lieutenant: SAVE_VERDICT`
- `caller: <officer-name>` — the officer dispatching the call. Often the same as `officer` below; can differ when the caller is transcribing on behalf of an officer (e.g., PLINY rescuing an Argus verdict from a chat transcript).
- `prompt: <free-text task description>`
- `inputs:`
  - `ticket_id: <string>` — required. The bw issue id (e.g., `gauntlet-ylq`).
  - `officer: <string>` — required. Uppercase officer name (ARGUS, VERA, CATO, CAPTAIN_PLINY). Determines the filename prefix.
  - `body: <string>` — optional. The verdict body, in-line. Mutually exclusive with `body_path`.
  - `body_path: <path>` — optional. Path to a file whose contents are the verdict body. Mutually exclusive with `body`.
  - `timestamp: <ISO-8601-string>` — optional. Default = current UTC time. Filename-encoded as `YYYY-MM-DDTHH-MM-SSZ` (colons replaced with hyphens for cross-platform filename safety).
  - `overwrite: <bool>` — optional. Default false. If false and the resolved dest exists, fails before writing.
  - `cwd: <absolute-path>` — optional. Default = current process cwd's repo root. **In an arc-build context the caller MUST pass the absolute arc-worktree root** (`<repo>/.claude/worktrees/arc-<N>-build`). Sub-agents inherit the parent session cwd — a CAPTAIN dispatched from the main session resolves a relative/defaulted cwd to the MAIN tree, not the worktree, so the verdict + receipt land at main `agents/verdicts/` instead of the worktree (the Arc-55 split: VERA/CATO wrote to main while ARGUS wrote to the worktree — stoa--xxy facet-2). Passing the explicit worktree path is the fix; the PLINY dispatch-discipline (`MAJOR_PLINY.md` §5.14) guarantees it is passed.
  - `verdict_shape: <pass | fail | needs-revisions | INCOMPLETE | UNVERIFIABLE>` — optional. Default unset (caller's body carries the shape). When set to `INCOMPLETE` or `UNVERIFIABLE`, additional fields below are required per the verification-complexity framework at `operating-disciplines.md` §15.
  - `quadrant_classification: <easy-easy | hard-easy | easy-hard | hard-hard>` — REQUIRED when `verdict_shape` is `INCOMPLETE` or `UNVERIFIABLE`. The verifier's classification of the claim per `operating-disciplines.md` §15.1.
  - `coverage_description: <free-form prose>` — REQUIRED when `verdict_shape` is `INCOMPLETE`. Describes what was checked, what was NOT checked, the bound used (iterations / state-space subset / time budget), and the verifier's confidence interval.
  - `sanity_check_performed: <free-form prose>` — REQUIRED when `verdict_shape` is `UNVERIFIABLE`. Describes what cheap check WAS performed within ~1× normal probe budget to confirm the quadrant classification.
  - `recommended_next_step: <free-form prose>` — REQUIRED when `verdict_shape` is `UNVERIFIABLE`. Describes the recommended operator action (operator judgment / deferred long-running suite / accept-risk-with-mitigations / etc.).
  - `threat_ratified_mitigation_count: <int>` — optional (`stoa--yfv` Arc B / §35). Count of threat-ratified mitigations in the verdict's scope. Default unset/`0` = the §35.5 carve-out (no threat-coverage required; no new validation fires). When `> 0`, `threat_coverage_probe_ids` is REQUIRED.
  - `threat_coverage_probe_ids: <comma-separated probe-ids, e.g. "p3,p7">` — REQUIRED when `threat_ratified_mitigation_count > 0`. The probe-ids the verdict's `threat_coverage:` lines cite via `defeats_via_probe:`. Each id must match `^p[0-9A-Za-z._-]+$`. This is the tier-i empty-binding check: "you declared N threat-ratified mitigations, so you must hand me ≥1 well-formed probe-id." The skill does NOT parse the verdict body to confirm each id appears in `probes_executed:` — that body-level `id ∈ executed-set` cross-check is **seat-side grep** (VERA / CATO / ARGUS role files), NOT skill-enforced. Per B2, a threat-ratified mitigation cannot pass without a cited EXECUTED attack-path probe.

The validation enforcement is **caller-side per shape**: the skill accepts the inputs, validates that required fields are present for the named shape, fails loud (exit 4) if not, and writes the verdict body. The skill does NOT embed the verification-complexity framework; the framework's semantics live in `operating-disciplines.md` §15, and the verifying CAPTAIN's role file teaches the seat to produce conformant bodies. The threat-coverage check (`stoa--yfv` Arc B) follows the same caller-side-per-shape posture: the skill enforces only the mechanical empty-binding invariant (`count > 0 ⇒ ≥1 well-formed probe-id`); the substance — does the cited probe genuinely exercise the named attack path — is tier-ii seat judgment, out of the skill's reach by design.

## Output contract

Resolved path: `<cwd>/agents/verdicts/<ticket-id>/<officer>-<timestamp-filename-safe>.md`.

SAVE_VERDICT writes a single text record at `agents/save-verdict/<ticket-id>/<officer>-<request-id>.txt` (per-ticket subdirectory + officer + request-id — all three the skill already receives as args). The path is **computed by the skill**, not caller-chosen, so generic request-ids cannot overwrite across tickets/arcs (stoa--xxy facet-1). The `--artifact-path` arg is still accepted for back-compat but its value is **ignored** — the canonical computed path always wins:

```
=== SAVE_VERDICT record ===
request_id: <request-id>
caller: <officer-name>
ticket_id: <verbatim>
officer: <verbatim>
timestamp: <resolved ISO-8601 UTC>
body_source: <inline | body_path>
overwrite: <true | false>
cwd: <resolved cwd, absolute>

=== execution ===
exit_code: <int>
duration_ms: <int>
resolved_dest: <absolute path the verdict was written to>
input_byte_length: <int | "(unknown)">
input_sha256: <hex | "(unknown)">
dest_sha256: <hex | "(unknown)">
verification: <pass | fail | skipped>
diagnostics_first_50_lines:
~~~~
<verbatim diagnostic, head -n 50; or "(none)">
~~~~
diagnostics_total_lines: <int>

=== assertion ===
overall: <pass | fail>
```

The reply bead returned to the caller:

```
SAVE_VERDICT complete: request=<request-id> overall=<pass|fail> dest=<resolved_dest> input_sha256=<short> dest_sha256=<short> bytes=<N> artifact=<artifact-path>
```

## Procedure

1. **Resolve cwd.** In an arc-build context the caller passes the absolute arc-worktree root (see the `cwd` input-contract note); otherwise it defaults to the current process cwd's repo root.
2. **Validate inputs.** Officer matches `^[A-Z][A-Z0-9_]*$`; ticket id matches `^[a-zA-Z0-9._-]+$`; exactly one of `body` / `body_path` is provided. **Shape conformance:** when `verdict_shape` is provided, validate per the verification-complexity framework at `operating-disciplines.md` §15.4. If `verdict_shape` is `INCOMPLETE` or `UNVERIFIABLE`, require `quadrant_classification` from the enum `{easy-easy, hard-easy, easy-hard, hard-hard}`. If `INCOMPLETE`, require `coverage_description`. If `UNVERIFIABLE`, require both `sanity_check_performed` and `recommended_next_step`. **Threat coverage (`stoa--yfv` Arc B):** if `threat_ratified_mitigation_count > 0`, require `threat_coverage_probe_ids` non-empty with each id matching `^p[0-9A-Za-z._-]+$`; count `0`/unset is the §35.5 carve-out and fires no new validation. This block runs after the §15.4 shape checks and before timestamp resolution; it does NOT parse the verdict body. Missing-required-field or out-of-enum cases exit 4 with the diagnostics enumerated in **Failure modes** below.
3. **Resolve timestamp.** If not provided, use `datetime.now(timezone.utc)`. Encode for filename as `strftime('%Y-%m-%dT%H-%M-%SZ')`.
4. **Compute resolved dest.** `<cwd>/agents/verdicts/<ticket_id>/<officer>-<ts-fn>.md`.
5. **Read body bytes.** From `--body` (encode UTF-8) or `--body-path` (read bytes).
6. **Pre-flight:** if dest exists and not `--overwrite`, fail (exit 3) with no writes.
7. **Write via `write_with_verify`.** Asserts sha256 round-trip.
8. **Re-hash** the on-disk file as defense-in-depth.
9. **Write record artifact.**

### Authoring the body file (Windows-safe; do this BEFORE the script call)

When the verdict body is multi-line, author it to a **worktree-relative path inside the same tree the verdict will land in**: `agents/verdicts/<ticket-id>/_body-<officer>.tmp.md`. Then pass that same path to `--body-path`. The **mechanism is seat-aware** because seats carry different toolsets, but the shared invariant below is identical for all of them:

- **Write-tool seats** (ADA, VERA, DAEDALUS, HERALD, CURATOR, STRABO, BARTLEBY) author it with the **Write tool** (harness runtime — no shell quoting, no heredoc, apostrophes safe) to that path.
- **Bash-only seats** (ARGUS, CATO, ZENO, NOMOS, TIRO — no Write/Edit tool; their common toolset is Bash, Read, Grep, Glob — only ARGUS and CATO additionally carry WebSearch/WebFetch) author it via **`printf` redirection** to that same path: `printf '%s' '<body>' > agents/verdicts/<ticket-id>/_body-<officer>.tmp.md`. Quoting caveat: a single-quoted `printf '%s' '…'` body is literal (no `$`/backtick expansion) but cannot contain a bare apostrophe — escape each embedded apostrophe as `'\''` (close-quote, escaped-apostrophe, reopen-quote). This is the proven Bash-only path the no-Write reviewer seats (ARGUS, CATO) used this arc; the escaping is required, not optional.

The **shared invariant** both mechanisms preserve: an explicit worktree-relative path, no quoted heredoc, no `/tmp`, and identical Write-vs-Python (or printf-vs-Python) path resolution.

Whichever mechanism the seat uses, do **NOT** author the body via a bash `cat <<'EOF' … EOF` heredoc, and do **NOT** write it to `/tmp/…`:

- On Windows git-bash the quoted `<<'EOF'` heredoc **still breaks on apostrophes** (confirmed Arc 52: a verdict had to be authored apostrophe-free after repeated retries).
- git-bash `/tmp` (MSYS) does **not** resolve to the same location as Python's `/tmp` on Windows, so `--body-path /tmp/…` either exit-4s ("body-path does not exist") or — the dangerous facet — reads a stale/wrong file and writes a **silent-green** verdict with wrong content.

An explicit repo/worktree-relative path is resolved **identically** by the Write tool (or `printf` redirection) and by Python's `pathlib`, sidestepping both root causes. The skill **exit-4s loudly** if a `/tmp`-style `--body-path` is passed (the loud-fail guard closes the one observed `/tmp` form; this worktree-relative-path PROCEDURE — via either authoring mechanism above — closes the general case — it eliminates any cross-runtime temp file, not just the `/tmp` spelling, satisfying the §34 fail-loud-on-mismatch constraint). Note the guard is a **literal-string backstop, not a general `/tmp` catch**: MSYS git-bash auto-converts a `/tmp/…` argument to the real Windows temp path *before* Python's argparse sees it, so under an ordinary git-bash invocation the guard never sees the `/tmp/` form (the conversion is self-consistent, so the read content stays correct) — it fires only when a genuinely-divergent literal `/tmp/…` string reaches Python; the worktree-relative authoring procedure (Write tool for Write-tool seats, `printf` redirection for Bash-only seats) is the load-bearing fix. The `_body-*.tmp.md` scratch file is left on disk (harmless, inside the verdict dir); it is not auto-deleted.

```bash
# $inputs.body_path = the worktree-relative file authored above (Write tool for
# Write-tool seats, printf redirection for Bash-only seats; NOT a /tmp heredoc).
# A /tmp-style --body-path is rejected at exit 4.
python skills/save-verdict/_save_verdict.py \
  --ticket-id "$inputs.ticket_id" \
  --officer "$inputs.officer" \
  ${inputs.body_path:+--body-path "$inputs.body_path"} \
  ${inputs.body:+--body "$inputs.body"} \
  ${inputs.timestamp:+--timestamp "$inputs.timestamp"} \
  ${inputs.overwrite:+--overwrite} \
  --cwd "$resolved_cwd" \
  --artifact-path "$artifact_path" \
  --request-id "$request_id" \
  --caller "$caller"
```

`--artifact-path` is passed here for back-compat but its value is **ignored** — the skill computes the receipt path canonically as `<cwd>/agents/save-verdict/<ticket-id>/<officer>-<request-id>.txt` (stoa--xxy facet-1). It may be omitted entirely (the arg is optional).

Exit codes per `_save_verdict.py` docstring: 0 ok / 2 sha256 mismatch / 3 dest exists / 4 argument error / 5 internal error.

## Failure modes

- **Both `body` and `body_path` given** (or neither). Exit 4 with a diagnostic naming which.
- **Officer or ticket id contains invalid chars.** Exit 4. Path-traversal defense. Ticket-ids must start with `[a-zA-Z0-9]`; bare-dot inputs (`.`, `..`) and leading-dash inputs (`-x`) are rejected at exit 4 before dest path construction.
- **`body_path` is a `/tmp`-style bash path** (`/tmp/…`, `/tmp\…`, or exactly `/tmp`). Exit 4 (wq0 loud-fail). On Windows git-bash `/tmp` resolves differently than Python's `/tmp`, risking a silent-green wrong-content verdict; the guard rejects the form outright with a diagnostic pointing at the Write-tool-to-worktree-relative-path procedure.
- **`request-id` contains invalid chars** (path separators, leading-dash, bare-dot). Exit 4. Path-traversal defense — `request-id` composes the receipt filename (stoa--xxy facet-1, r5).
- **`body_path` does not exist.** Exit 4.
- **Dest exists, no `--overwrite`.** Exit 3. Common when an officer accidentally re-dispatches with the same timestamp; caller picks `overwrite: true` or a different timestamp.
- **OS error during write** (perms, disk-full). Exit 5.
- **sha256 round-trip mismatch.** Exit 2. Should not happen on healthy filesystems.
- **`verdict_shape: INCOMPLETE` without `coverage_description`.** Exit 4 with diagnostic "INCOMPLETE verdict requires coverage_description per operating-disciplines.md §15.4."
- **`verdict_shape: UNVERIFIABLE` without `sanity_check_performed` OR without `recommended_next_step`.** Exit 4 with diagnostic "UNVERIFIABLE verdict requires sanity_check_performed AND recommended_next_step per operating-disciplines.md §15.4."
- **`verdict_shape: INCOMPLETE | UNVERIFIABLE` without `quadrant_classification`.** Exit 4 with diagnostic "INCOMPLETE / UNVERIFIABLE verdicts require quadrant_classification per operating-disciplines.md §15.4."
- **`quadrant_classification:` value not in the enum.** Exit 4 with diagnostic "quadrant_classification must be one of: easy-easy, hard-easy, easy-hard, hard-hard."
- **`threat_ratified_mitigation_count > 0` without `threat_coverage_probe_ids`** (`stoa--yfv` Arc B). Exit 4 with diagnostic "verdict declares N threat-ratified mitigation(s) but cites no threat-coverage probe-ids; per stoa--yfv B2 a threat-ratified mitigation cannot pass without a cited EXECUTED attack-path probe (op-disc §35 / Arc B). Pass --threat-coverage-probe-ids, or --threat-ratified-mitigation-count 0 if this arc is §35.5-carved-out."
- **A `threat_coverage_probe_ids` value malformed** (does not match `^p[0-9A-Za-z._-]+$`). Exit 4 with diagnostic "threat-coverage probe-id '<id>' is malformed; each id must match ^p[0-9A-Za-z._-]+$ (well-formed probe-id, no path-meta)."

## What this skill is NOT

- **Not a verdict format validator.** Does not parse the body to confirm it is a "valid verdict." Whatever bytes the caller hands over is what gets saved. Format conformance is FORMAT_VALIDATE's seat (or the caller's own check). This is why the threat-coverage check (`stoa--yfv` Arc B) enforces only the empty-binding invariant from the explicit `--threat-coverage-probe-ids` arg and does NOT scan the body for `threat_coverage:` lines or confirm each cited id appears in `probes_executed:` — that body-level `id ∈ executed-set` cross-check is seat-side grep (VERA / CATO), not the skill's job.
- **Not a verdict-of-record register.** Per ticket there can be multiple SAVE_VERDICT calls (each round of an officer's verdict, each re-run after revision). The aggregation that picks "which is the verdict-of-record" is the caller's judgment (PLINY at arc close; POLYBIUS at retrospective).
- **Not a bw-poster.** Writing the verdict to a bw comment is `bw comment <id>`; SAVE_VERDICT writes to disk. Both can happen — disk for durable artifact, bw comment for the message bus.
- **Not a substitute for COPY_ARTIFACT.** If the caller already has the verdict text in a file at an arbitrary path and just wants to copy it somewhere, COPY_ARTIFACT is the right tool. SAVE_VERDICT specializes for the canonical-path convention.

## Preservation discipline

Source-of-truth at `substrate/skills/save-verdict/SKILL.md` + `substrate/skills/save-verdict/_save_verdict.py` + `substrate/skills/save-verdict/_lib/byte_copy.py`. Deployed at all 3 install tiers (user / project / subproject) via `substrate/install.sh` `SKILL_NAMES` array. Cross-skill share of `_lib/byte_copy.py` with COPY_ARTIFACT and TRANSCRIBE_BW_TO_DISK deferred to stoa--sp1 per Arc 39 directive A2 α + A20.
