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
  - `cwd: <repo-relative-path>` — optional. Default = gauntlet repo root.
  - `verdict_shape: <pass | fail | needs-revisions | INCOMPLETE | UNVERIFIABLE>` — optional. Default unset (caller's body carries the shape). When set to `INCOMPLETE` or `UNVERIFIABLE`, additional fields below are required per the verification-complexity framework at `operating-disciplines.md` §15.
  - `quadrant_classification: <easy-easy | hard-easy | easy-hard | hard-hard>` — REQUIRED when `verdict_shape` is `INCOMPLETE` or `UNVERIFIABLE`. The verifier's classification of the claim per `operating-disciplines.md` §15.1.
  - `coverage_description: <free-form prose>` — REQUIRED when `verdict_shape` is `INCOMPLETE`. Describes what was checked, what was NOT checked, the bound used (iterations / state-space subset / time budget), and the verifier's confidence interval.
  - `sanity_check_performed: <free-form prose>` — REQUIRED when `verdict_shape` is `UNVERIFIABLE`. Describes what cheap check WAS performed within ~1× normal probe budget to confirm the quadrant classification.
  - `recommended_next_step: <free-form prose>` — REQUIRED when `verdict_shape` is `UNVERIFIABLE`. Describes the recommended operator action (operator judgment / deferred long-running suite / accept-risk-with-mitigations / etc.).

The validation enforcement is **caller-side per shape**: the skill accepts the inputs, validates that required fields are present for the named shape, fails loud (exit 4) if not, and writes the verdict body. The skill does NOT embed the verification-complexity framework; the framework's semantics live in `operating-disciplines.md` §15, and the verifying CAPTAIN's role file teaches the seat to produce conformant bodies.

## Output contract

Resolved path: `<cwd>/agents/verdicts/<ticket-id>/<officer>-<timestamp-filename-safe>.md`.

SAVE_VERDICT writes a single text record at `agents/save-verdict/<request-id>.txt`:

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

1. **Resolve cwd** to gauntlet repo root by default.
2. **Validate inputs.** Officer matches `^[A-Z][A-Z0-9_]*$`; ticket id matches `^[a-zA-Z0-9._-]+$`; exactly one of `body` / `body_path` is provided. **Shape conformance:** when `verdict_shape` is provided, validate per the verification-complexity framework at `operating-disciplines.md` §15.4. If `verdict_shape` is `INCOMPLETE` or `UNVERIFIABLE`, require `quadrant_classification` from the enum `{easy-easy, hard-easy, easy-hard, hard-hard}`. If `INCOMPLETE`, require `coverage_description`. If `UNVERIFIABLE`, require both `sanity_check_performed` and `recommended_next_step`. Missing-required-field or out-of-enum cases exit 4 with the diagnostics enumerated in **Failure modes** below.
3. **Resolve timestamp.** If not provided, use `datetime.now(timezone.utc)`. Encode for filename as `strftime('%Y-%m-%dT%H-%M-%SZ')`.
4. **Compute resolved dest.** `<cwd>/agents/verdicts/<ticket_id>/<officer>-<ts-fn>.md`.
5. **Read body bytes.** From `--body` (encode UTF-8) or `--body-path` (read bytes).
6. **Pre-flight:** if dest exists and not `--overwrite`, fail (exit 3) with no writes.
7. **Write via `write_with_verify`.** Asserts sha256 round-trip.
8. **Re-hash** the on-disk file as defense-in-depth.
9. **Write record artifact.**

```bash
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

Exit codes per `_save_verdict.py` docstring: 0 ok / 2 sha256 mismatch / 3 dest exists / 4 argument error / 5 internal error.

## Failure modes

- **Both `body` and `body_path` given** (or neither). Exit 4 with a diagnostic naming which.
- **Officer or ticket id contains invalid chars.** Exit 4. Path-traversal defense. Ticket-ids must start with `[a-zA-Z0-9]`; bare-dot inputs (`.`, `..`) and leading-dash inputs (`-x`) are rejected at exit 4 before dest path construction.
- **`body_path` does not exist.** Exit 4.
- **Dest exists, no `--overwrite`.** Exit 3. Common when an officer accidentally re-dispatches with the same timestamp; caller picks `overwrite: true` or a different timestamp.
- **OS error during write** (perms, disk-full). Exit 5.
- **sha256 round-trip mismatch.** Exit 2. Should not happen on healthy filesystems.
- **`verdict_shape: INCOMPLETE` without `coverage_description`.** Exit 4 with diagnostic "INCOMPLETE verdict requires coverage_description per operating-disciplines.md §15.4."
- **`verdict_shape: UNVERIFIABLE` without `sanity_check_performed` OR without `recommended_next_step`.** Exit 4 with diagnostic "UNVERIFIABLE verdict requires sanity_check_performed AND recommended_next_step per operating-disciplines.md §15.4."
- **`verdict_shape: INCOMPLETE | UNVERIFIABLE` without `quadrant_classification`.** Exit 4 with diagnostic "INCOMPLETE / UNVERIFIABLE verdicts require quadrant_classification per operating-disciplines.md §15.4."
- **`quadrant_classification:` value not in the enum.** Exit 4 with diagnostic "quadrant_classification must be one of: easy-easy, hard-easy, easy-hard, hard-hard."

## What this skill is NOT

- **Not a verdict format validator.** Does not parse the body to confirm it is a "valid verdict." Whatever bytes the caller hands over is what gets saved. Format conformance is FORMAT_VALIDATE's seat (or the caller's own check).
- **Not a verdict-of-record register.** Per ticket there can be multiple SAVE_VERDICT calls (each round of an officer's verdict, each re-run after revision). The aggregation that picks "which is the verdict-of-record" is the caller's judgment (PLINY at arc close; POLYBIUS at retrospective).
- **Not a bw-poster.** Writing the verdict to a bw comment is `bw comment <id>`; SAVE_VERDICT writes to disk. Both can happen — disk for durable artifact, bw comment for the message bus.
- **Not a substitute for COPY_ARTIFACT.** If the caller already has the verdict text in a file at an arbitrary path and just wants to copy it somewhere, COPY_ARTIFACT is the right tool. SAVE_VERDICT specializes for the canonical-path convention.

## Preservation discipline

Source-of-truth at `substrate/skills/save-verdict/SKILL.md` + `substrate/skills/save-verdict/_save_verdict.py` + `substrate/skills/save-verdict/_lib/byte_copy.py`. Deployed at all 3 install tiers (user / project / subproject) via `substrate/install.sh` `SKILL_NAMES` array. Cross-skill share of `_lib/byte_copy.py` with COPY_ARTIFACT and TRANSCRIBE_BW_TO_DISK deferred to stoa--sp1 per Arc 39 directive A2 α + A20.
