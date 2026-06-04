"""
_save_verdict.py — canonical-path verdict writer for the save-verdict skill.

Implements SKILL.md procedure steps 1-9. See substrate/skills/save-verdict/SKILL.md
for the input contract, output contract, failure modes, and exit-code semantics.

Exit codes:
    0 — ok
    2 — sha256 round-trip mismatch (step 7 or step 8)
    3 — dest exists without --overwrite (step 6)
    4 — argument error (step 1, 2, or 5)
    5 — internal error (OS errors during write; unexpected exceptions)

Invocation contract (R2 LOCKED per Arc 39 design §2.4):
    python substrate/skills/save-verdict/_save_verdict.py --ticket-id ... --officer ... ...

The script invocation contract is canon; module-importability is a side-benefit
of the `if __name__ == "__main__"` idiom, not the contract.
"""

from __future__ import annotations

import argparse
import os
import pathlib
import re
import sys
import time
import traceback
from datetime import datetime, timezone

# R2 canon-establishing pick (Arc 39 design §2.4): invoke as script via path,
# import sibling _lib via sys.path manipulation. Establishes precedent for
# future Python substrate skills.
_SCRIPT_DIR = pathlib.Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from _lib.byte_copy import write_with_verify  # noqa: E402


# --- Regexes (path-traversal defense) ---
_OFFICER_RE = re.compile(r"^[A-Z][A-Z0-9_]*$")
# Ticket-ids must start with [a-zA-Z0-9]; bare-dot / ".." / leading-dash rejected.
_TICKET_RE = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9._-]*$")
# request-id composes the receipt filename (xxy facet-1); same path-traversal
# defense as ticket-id — no path separators, no leading-dash, no bare-dot.
_REQUEST_ID_RE = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9._-]*$")

_QUADRANT_ENUM = {"easy-easy", "hard-easy", "easy-hard", "hard-hard"}
_SHAPE_ENUM = {"pass", "fail", "needs-revisions", "INCOMPLETE", "UNVERIFIABLE"}


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="_save_verdict.py",
        description=(
            "Canonical-path verdict writer. See substrate/skills/save-verdict/"
            "SKILL.md for the full input/output contract."
        ),
    )
    p.add_argument("--ticket-id", required=True)
    p.add_argument("--officer", required=True)
    p.add_argument("--body", default=None)
    p.add_argument("--body-path", default=None)
    p.add_argument("--timestamp", default=None, help="ISO-8601 UTC; default = now")
    p.add_argument("--overwrite", action="store_true")
    p.add_argument("--cwd", required=True)
    # xxy facet-1 (r3): the receipt path is now computed canonically by the skill
    # (agents/save-verdict/<ticket>/<officer>-<request-id>.txt). --artifact-path is
    # RELAXED to optional and retained only as a back-compat no-op so the SKILL.md
    # step-9 example (which still passes it) does not self-break argparse at exit 4.
    # Its value is IGNORED; the canonical computed path always wins. See main().
    p.add_argument("--artifact-path", default=None)
    p.add_argument("--request-id", required=True)
    p.add_argument("--caller", required=True)
    p.add_argument(
        "--verdict-shape",
        default=None,
        help="One of: pass | fail | needs-revisions | INCOMPLETE | UNVERIFIABLE",
    )
    p.add_argument(
        "--quadrant-classification",
        default=None,
        help="One of: easy-easy | hard-easy | easy-hard | hard-hard",
    )
    p.add_argument("--coverage-description", default=None)
    p.add_argument("--sanity-check-performed", default=None)
    p.add_argument("--recommended-next-step", default=None)
    return p


def _exit_with(code: int, diagnostic: str) -> int:
    """Print diagnostic to stderr and return the exit code."""
    sys.stderr.write(diagnostic.rstrip() + "\n")
    return code


def _ts_filename(ts: datetime) -> str:
    """Encode timestamp as %Y-%m-%dT%H-%M-%SZ for cross-platform filename safety."""
    return ts.strftime("%Y-%m-%dT%H-%M-%SZ")


def _parse_iso8601(s: str) -> datetime:
    """
    Parse an ISO-8601 string permissively. Accepts trailing 'Z' or +HH:MM offset.
    Returns timezone-aware datetime in UTC.
    """
    raw = s.strip()
    # Normalize trailing 'Z' to '+00:00' for fromisoformat (Python <3.11 compat).
    if raw.endswith("Z"):
        raw = raw[:-1] + "+00:00"
    dt = datetime.fromisoformat(raw)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def _write_record_artifact(
    artifact_path: pathlib.Path,
    *,
    request_id: str,
    caller: str,
    ticket_id: str,
    officer: str,
    timestamp_iso: str,
    body_source: str,
    overwrite: bool,
    cwd_abs: pathlib.Path,
    exit_code: int,
    duration_ms: int,
    resolved_dest: pathlib.Path,
    input_byte_length,
    input_sha256: str,
    dest_sha256: str,
    verification: str,
    diagnostics: str,
) -> None:
    """
    Emit the record artifact per SKILL.md "Output contract" template. Best-effort:
    on failure the caller already has the canonical verdict on disk; the record
    artifact is observability, not part of the verdict guarantee.
    """
    diag_lines = diagnostics.splitlines() if diagnostics else []
    head = "\n".join(diag_lines[:50]) if diag_lines else "(none)"
    overall = "pass" if exit_code == 0 and verification == "pass" else "fail"

    body = (
        f"=== SAVE_VERDICT record ===\n"
        f"request_id: {request_id}\n"
        f"caller: {caller}\n"
        f"ticket_id: {ticket_id}\n"
        f"officer: {officer}\n"
        f"timestamp: {timestamp_iso}\n"
        f"body_source: {body_source}\n"
        f"overwrite: {'true' if overwrite else 'false'}\n"
        f"cwd: {cwd_abs}\n"
        f"\n"
        f"=== execution ===\n"
        f"exit_code: {exit_code}\n"
        f"duration_ms: {duration_ms}\n"
        f"resolved_dest: {resolved_dest}\n"
        f"input_byte_length: {input_byte_length}\n"
        f"input_sha256: {input_sha256}\n"
        f"dest_sha256: {dest_sha256}\n"
        f"verification: {verification}\n"
        f"diagnostics_first_50_lines:\n"
        f"~~~~\n"
        f"{head}\n"
        f"~~~~\n"
        f"diagnostics_total_lines: {len(diag_lines)}\n"
        f"\n"
        f"=== assertion ===\n"
        f"overall: {overall}\n"
    )

    try:
        artifact_path.parent.mkdir(parents=True, exist_ok=True)
        artifact_path.write_bytes(body.encode("utf-8"))
    except OSError as e:
        # Best-effort. Surface to stderr but do not flip the overall exit code,
        # because the canonical verdict is already on disk.
        sys.stderr.write(f"warning: record-artifact write failed: {e}\n")


def main(argv=None) -> int:
    start_ns = time.perf_counter_ns()
    parser = _build_parser()
    try:
        args = parser.parse_args(argv)
    except SystemExit as e:
        # argparse already wrote to stderr; map its exit-2 (bad usage) to exit 4
        # to fit the skill's exit-code contract.
        return 4 if e.code is not None and e.code != 0 else 0

    # Step 1: body / body-path mutual exclusion (XOR).
    has_body = args.body is not None
    has_body_path = args.body_path is not None
    if has_body == has_body_path:
        # Both or neither.
        which = "both" if has_body else "neither"
        return _exit_with(
            4,
            f"argument error: exactly one of --body / --body-path is required ({which} given).",
        )

    # Step 2: input validation.
    if not _OFFICER_RE.match(args.officer):
        return _exit_with(
            4, "officer name must match ^[A-Z][A-Z0-9_]*$"
        )
    if not _TICKET_RE.match(args.ticket_id):
        return _exit_with(
            4, "ticket-id must match ^[a-zA-Z0-9][a-zA-Z0-9._-]*$"
        )
    # xxy facet-1 (r5): request_id now composes the receipt filename
    # (agents/save-verdict/<ticket>/<officer>-<request-id>.txt), so it must be
    # path-separator-safe — same path-traversal defense class as the officer /
    # ticket_id regex above. Reject path separators and shell-meta before the
    # receipt path is composed.
    if not _REQUEST_ID_RE.match(args.request_id):
        return _exit_with(
            4, "request-id must match ^[a-zA-Z0-9][a-zA-Z0-9._-]*$ "
            "(no path separators; it composes the receipt filename)"
        )

    # Shape-conformance validation per op-disc §15.4.
    shape = args.verdict_shape
    if shape is not None and shape not in _SHAPE_ENUM:
        return _exit_with(
            4,
            "verdict-shape must be one of: pass, fail, needs-revisions, INCOMPLETE, UNVERIFIABLE.",
        )
    if shape in ("INCOMPLETE", "UNVERIFIABLE"):
        if args.quadrant_classification is None:
            return _exit_with(
                4,
                "INCOMPLETE / UNVERIFIABLE verdicts require quadrant_classification "
                "per operating-disciplines.md §15.4",
            )
        if args.quadrant_classification not in _QUADRANT_ENUM:
            return _exit_with(
                4,
                "quadrant_classification must be one of: easy-easy, hard-easy, "
                "easy-hard, hard-hard.",
            )
    if shape == "INCOMPLETE" and not args.coverage_description:
        return _exit_with(
            4,
            "INCOMPLETE verdict requires coverage_description per operating-disciplines.md §15.4",
        )
    if shape == "UNVERIFIABLE":
        if not args.sanity_check_performed or not args.recommended_next_step:
            return _exit_with(
                4,
                "UNVERIFIABLE verdict requires sanity_check_performed AND "
                "recommended_next_step per operating-disciplines.md §15.4",
            )

    # Step 3: resolve timestamp.
    try:
        if args.timestamp:
            ts = _parse_iso8601(args.timestamp)
        else:
            ts = datetime.now(timezone.utc)
    except (ValueError, TypeError) as e:
        return _exit_with(4, f"could not parse --timestamp: {e}")
    ts_fn = _ts_filename(ts)
    timestamp_iso = ts.strftime("%Y-%m-%dT%H:%M:%SZ")

    # Step 4: compute resolved dest.
    try:
        cwd_abs = pathlib.Path(args.cwd).resolve()
    except OSError as e:
        return _exit_with(5, f"could not resolve --cwd: {e}")
    resolved_dest = cwd_abs / "agents" / "verdicts" / args.ticket_id / f"{args.officer}-{ts_fn}.md"

    # xxy facet-1: namespace the receipt per ticket+officer+request-id to stop the
    # flat-name collision (e.g. argus-rev2-reconfirm.txt overwrote across arcs). The
    # caller-supplied --artifact-path is RETAINED as an accepted-but-ignored arg
    # (back-compat for the SKILL.md step-9 example); the canonical computed path
    # always wins so two arcs/tickets cannot collide. ticket_id / officer /
    # request_id are all validated path-safe above (steps 2 + r5 guard).
    artifact_path = (
        cwd_abs / "agents" / "save-verdict" / args.ticket_id
        / f"{args.officer}-{args.request_id}.txt"
    )

    # Step 5: read body bytes.
    body_source = "inline" if has_body else "body_path"
    body_bytes: bytes
    try:
        if has_body:
            body_bytes = args.body.encode("utf-8")
        else:
            raw_bp = args.body_path
            # wq0 loud-fail: a bash-/tmp-style body-path is the Windows silent-green
            # trap. git-bash /tmp (MSYS) and Python /tmp resolve to DIFFERENT
            # locations on Windows; reject the ambiguous form outright so a path
            # mismatch FAILS LOUD rather than reading a stale file and writing a
            # green verdict with wrong content. The guard closes the one observed
            # dangerous FORM (/tmp); the SKILL.md "Authoring the body file"
            # procedure (Write-tool -> worktree-relative path) closes the general
            # case. See save-verdict SKILL.md.
            if (
                raw_bp.startswith("/tmp/")
                or raw_bp.startswith("/tmp\\")
                or raw_bp == "/tmp"
            ):
                return _exit_with(
                    4,
                    "body-path looks like a bash /tmp path (" + raw_bp + "): on "
                    "Windows git-bash this resolves differently than Python and "
                    "risks a silent-green wrong-content verdict. Author the body "
                    "via the Write tool to a worktree-relative path "
                    "(agents/verdicts/<ticket-id>/_body-<officer>.tmp.md) and pass "
                    "that. See save-verdict SKILL.md 'Authoring the body file'.",
                )
            body_path = pathlib.Path(raw_bp)
            if not body_path.exists():
                return _exit_with(4, f"body-path does not exist: {body_path}")
            body_bytes = body_path.read_bytes()
    except OSError as e:
        return _exit_with(5, f"could not read body bytes: {e}")
    except UnicodeEncodeError as e:
        return _exit_with(4, f"--body could not be UTF-8 encoded: {e}")

    # Ensure parent directory exists (mkdir -p semantics).
    try:
        resolved_dest.parent.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        return _exit_with(5, f"could not create dest parent: {e}")

    # Step 6: pre-flight dest-exists check.
    if resolved_dest.exists() and not args.overwrite:
        return _exit_with(
            3, f"dest exists; use --overwrite to replace: {resolved_dest}"
        )

    # Step 7: write via write_with_verify (sha256 round-trip).
    input_sha256 = ""
    dest_sha256 = ""
    input_byte_length = "(unknown)"
    verification = "skipped"
    diagnostics_for_artifact = ""

    # artifact_path was computed canonically in step 4 (xxy facet-1); the raw
    # --artifact-path arg is ignored.

    try:
        result = write_with_verify(
            resolved_dest, body_bytes, overwrite=args.overwrite
        )
        input_sha256 = result["input_sha256"]
        dest_sha256 = result["dest_sha256"]
        input_byte_length = result["input_byte_length"]
        verification = result["verification"]
    except FileExistsError as e:
        # Race: dest didn't exist at pre-flight but exists now. Treat as exit 3.
        return _exit_with(3, f"dest exists; use --overwrite to replace: {e}")
    except ValueError as e:
        # sha256 mismatch on round-trip.
        diagnostics_for_artifact = str(e)
        _write_record_artifact(
            artifact_path,
            request_id=args.request_id,
            caller=args.caller,
            ticket_id=args.ticket_id,
            officer=args.officer,
            timestamp_iso=timestamp_iso,
            body_source=body_source,
            overwrite=args.overwrite,
            cwd_abs=cwd_abs,
            exit_code=2,
            duration_ms=(time.perf_counter_ns() - start_ns) // 1_000_000,
            resolved_dest=resolved_dest,
            input_byte_length=input_byte_length or "(unknown)",
            input_sha256=input_sha256 or "(unknown)",
            dest_sha256=dest_sha256 or "(unknown)",
            verification="fail",
            diagnostics=diagnostics_for_artifact,
        )
        return _exit_with(2, str(e))
    except OSError as e:
        diagnostics_for_artifact = f"OSError during write: {e}"
        _write_record_artifact(
            artifact_path,
            request_id=args.request_id,
            caller=args.caller,
            ticket_id=args.ticket_id,
            officer=args.officer,
            timestamp_iso=timestamp_iso,
            body_source=body_source,
            overwrite=args.overwrite,
            cwd_abs=cwd_abs,
            exit_code=5,
            duration_ms=(time.perf_counter_ns() - start_ns) // 1_000_000,
            resolved_dest=resolved_dest,
            input_byte_length=input_byte_length or "(unknown)",
            input_sha256=input_sha256 or "(unknown)",
            dest_sha256=dest_sha256 or "(unknown)",
            verification="fail",
            diagnostics=diagnostics_for_artifact,
        )
        return _exit_with(5, diagnostics_for_artifact)
    except Exception as e:  # noqa: BLE001 — internal-error catch-all per exit code 5
        diagnostics_for_artifact = f"unexpected exception during write: {e}\n{traceback.format_exc()}"
        _write_record_artifact(
            artifact_path,
            request_id=args.request_id,
            caller=args.caller,
            ticket_id=args.ticket_id,
            officer=args.officer,
            timestamp_iso=timestamp_iso,
            body_source=body_source,
            overwrite=args.overwrite,
            cwd_abs=cwd_abs,
            exit_code=5,
            duration_ms=(time.perf_counter_ns() - start_ns) // 1_000_000,
            resolved_dest=resolved_dest,
            input_byte_length=input_byte_length or "(unknown)",
            input_sha256=input_sha256 or "(unknown)",
            dest_sha256=dest_sha256 or "(unknown)",
            verification="fail",
            diagnostics=diagnostics_for_artifact,
        )
        return _exit_with(5, diagnostics_for_artifact)

    # Step 8: re-hash on-disk file (defense-in-depth; second read).
    try:
        import hashlib

        reread = resolved_dest.read_bytes()
        post_write_sha = hashlib.sha256(reread).hexdigest()
        if post_write_sha != dest_sha256:
            msg = (
                f"post-write re-hash mismatch: write={dest_sha256} reread={post_write_sha}"
            )
            diagnostics_for_artifact = msg
            _write_record_artifact(
                artifact_path,
                request_id=args.request_id,
                caller=args.caller,
                ticket_id=args.ticket_id,
                officer=args.officer,
                timestamp_iso=timestamp_iso,
                body_source=body_source,
                overwrite=args.overwrite,
                cwd_abs=cwd_abs,
                exit_code=2,
                duration_ms=(time.perf_counter_ns() - start_ns) // 1_000_000,
                resolved_dest=resolved_dest,
                input_byte_length=input_byte_length,
                input_sha256=input_sha256,
                dest_sha256=dest_sha256,
                verification="fail",
                diagnostics=diagnostics_for_artifact,
            )
            return _exit_with(2, msg)
    except OSError as e:
        diagnostics_for_artifact = f"OSError during post-write re-hash: {e}"
        _write_record_artifact(
            artifact_path,
            request_id=args.request_id,
            caller=args.caller,
            ticket_id=args.ticket_id,
            officer=args.officer,
            timestamp_iso=timestamp_iso,
            body_source=body_source,
            overwrite=args.overwrite,
            cwd_abs=cwd_abs,
            exit_code=5,
            duration_ms=(time.perf_counter_ns() - start_ns) // 1_000_000,
            resolved_dest=resolved_dest,
            input_byte_length=input_byte_length,
            input_sha256=input_sha256,
            dest_sha256=dest_sha256,
            verification="fail",
            diagnostics=diagnostics_for_artifact,
        )
        return _exit_with(5, diagnostics_for_artifact)

    # Step 9: write record artifact (happy path).
    duration_ms = (time.perf_counter_ns() - start_ns) // 1_000_000
    _write_record_artifact(
        artifact_path,
        request_id=args.request_id,
        caller=args.caller,
        ticket_id=args.ticket_id,
        officer=args.officer,
        timestamp_iso=timestamp_iso,
        body_source=body_source,
        overwrite=args.overwrite,
        cwd_abs=cwd_abs,
        exit_code=0,
        duration_ms=duration_ms,
        resolved_dest=resolved_dest,
        input_byte_length=input_byte_length,
        input_sha256=input_sha256,
        dest_sha256=dest_sha256,
        verification=verification,
        diagnostics="",
    )

    # Reply-bead-shaped one-liner to stdout for callers that capture stdout.
    short_in = input_sha256[:12] if input_sha256 else "(unknown)"
    short_dest = dest_sha256[:12] if dest_sha256 else "(unknown)"
    sys.stdout.write(
        f"SAVE_VERDICT complete: request={args.request_id} overall=pass "
        f"dest={resolved_dest} input_sha256={short_in} dest_sha256={short_dest} "
        f"bytes={input_byte_length} artifact={artifact_path}\n"
    )

    return 0


if __name__ == "__main__":
    sys.exit(main())
