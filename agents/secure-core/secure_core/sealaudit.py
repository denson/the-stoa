# author: Denson Smith
# ticket: stoa--q7f (u--9s2 Phase-1 increment 2.4)
# seat-built-by: CAPTAIN_ADA_the_stoa (EXECUTOR)
# design-ground-truth: design-rev4.md §3.1 (fail-CLOSED seal-audit; the CONSTRAINED synthetic exemption =
#                       INTERSECTION of path-bound AND shape-clean) + §5.2 (P-M7). Mitigates M7 (secret-value
#                       leakage into code/config/catalog/logs / build-artifact key-exfil).
#
# `seal_audit(tree_paths, emitted_logs)` — a DETERMINISTIC build-time gate. Scans every tracked file + every
# emitted log line and RAISES SealAuditError (build FAILS non-zero) on ANY secret-VALUE shape-match. It is
# fail-CLOSED: an ambiguous high-entropy blob it cannot classify is a FAILURE, not waved through. Absence of
# a finding is the only pass.
#
# The `SEAL_AUDIT_SYNTHETIC_` exemption is NECESSARY-BUT-NOT-SUFFICIENT, gated behind the INTERSECTION of:
#   (i)  path-bound  — the match is INSIDE the designated fixtures path; and
#   (ii) shape-clean — the demarked body matches NO real-secret shape.
# A real-SHAPED marked value FAILS even when marked (the marker cannot launder a real shape); a marked value
# OUTSIDE the fixtures path FAILS. Bare slot NAMES (no bound value) are allowed everywhere (a name is not a
# value).

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from secure_core.errors import SealAuditError

# The designated fixtures path SEGMENT (design §3.1: e.g. tests/fixtures/seal_audit/). A marked value is
# path-bound iff its file path contains this segment. `emitted_logs` are NEVER path-bound (a log line is not
# in the fixtures dir), so a marker in a log always FAILS the path-bound test.
FIXTURES_SEGMENT = "tests/fixtures/seal_audit"

SYNTHETIC_MARKER = "SEAL_AUDIT_SYNTHETIC_"

# -- real-secret VALUE shapes (design §3.1) --------------------------------------------------------
# Each entry: (kind, compiled regex). A match anywhere (outside an exempt marked+path-bound+shape-clean
# span) FAILS the build.
_REAL_SHAPES: list[tuple[str, re.Pattern]] = [
    ("tailscale_authkey", re.compile(r"tskey-(?:auth-|client-|api-)?[A-Za-z0-9]{6,}")),
    ("pem_private_key", re.compile(r"-----BEGIN (?:RSA |EC )?PRIVATE KEY-----")),
    ("anthropic_key", re.compile(r"sk-ant-(?:oat01-)?[A-Za-z0-9_-]{8,}")),
    ("postgres_inline_pw", re.compile(r"postgres(?:ql)?://[^:/@\s]+:[^@/\s]{3,}@")),
]

# A base64 blob above a length floor resembling an SA-key JSON (SA keys base64 are long). 100+ chars of the
# base64 charset. A sha256 hex digest (exactly 64 hex) is NOT this shape (too short + hex, not b64 blob) —
# see _is_recognized_digest.
_B64_BLOB = re.compile(r"[A-Za-z0-9+/]{100,}={0,2}")
# ambiguous high-entropy hex blob >= 100 hex chars (fail-closed: cannot classify -> FAIL).
_HEX_BLOB = re.compile(r"\b[0-9a-fA-F]{100,}\b")
# a recognized value-free digest: exactly-64 lowercase hex (a sha256 params_digest). Classifiable as SAFE.
_SHA256_HEX = re.compile(r"\b[0-9a-f]{64}\b")

# a secret NAME bound to a NON-EMPTY, NON-placeholder VALUE (NAME=value / NAME: value). The NAME alone is a
# documented placeholder and is allowed; a value bound to it is refused.
_SECRET_NAMES = r"(?:GCP_SA_KEY_B64|POSTGRES_PASSWORD|TS_AUTHKEY|GEMINI_API_KEY|ANTHROPIC_API_KEY|CLAUDE_CODE_OAUTH_TOKEN|GCP_SA_KEY)"
# placeholder VALUES that are allowed (a name pointing at a slot, not a real value).
_PLACEHOLDER = re.compile(r"^(?:|\"\"|''|<[^>]*>|\$\{[^}]*\}|\{\{[^}]*\}\}|None|null|nil|xxx+|\.\.\.|CHANGEME|REDACTED|slot|name-only)$", re.IGNORECASE)
_NAME_VALUE = re.compile(
    r"\b" + _SECRET_NAMES + r"\b\s*[:=]\s*(?P<val>[^\s,;#]+)"
)


@dataclass(frozen=True)
class SealFinding:
    path: str
    kind: str
    reason: str


def _is_recognized_digest(blob: str) -> bool:
    """A blob classifiable as a value-free digest (sha256 hex) -> SAFE, not a secret. Everything else that
    trips the high-entropy floor is UNCLASSIFIED -> fail-closed FAIL."""
    return bool(_SHA256_HEX.fullmatch(blob))


def _demarked_matches_real_shape(body: str) -> str | None:
    """If `body` (a marker-stripped token) matches a real-secret shape, return its kind; else None."""
    for kind, rx in _REAL_SHAPES:
        if rx.search(body):
            return kind
    if _B64_BLOB.fullmatch(body):
        return "base64_blob"
    if _HEX_BLOB.fullmatch(body) and not _is_recognized_digest(body):
        return "hex_blob"
    return None


# A marked VALUE's body starts with an alphanumeric (a real secret/fixture body begins with a value char),
# and runs until whitespace or a quote/backtick delimiter. This distinguishes a marked value (the marker
# immediately followed by a value token) from a mere MENTION of the marker in source/docs (the constant
# definition, a backtick-quoted reference, or the marker followed by a placeholder/quote/space) — the latter
# is not a value and is not scanned as one. NOTE (self-hygiene): this scanner's OWN source must never write
# the marker literal directly adjacent to a value token, or it would flag itself; references use the
# SYNTHETIC_MARKER constant instead.
_MARKER_TOKEN = re.compile(re.escape(SYNTHETIC_MARKER) + r"[A-Za-z0-9][^\s\"'`]*")


def _marker_spans(line: str) -> list[tuple[int, int, str]]:
    """Every SEAL_AUDIT_SYNTHETIC_<value-body> token span in the line, with its demarked body. A marker not
    followed by a value char (a documentation mention / the constant definition) is NOT a marked value."""
    spans = []
    for m in _MARKER_TOKEN.finditer(line):
        token = m.group(0)
        body = token[len(SYNTHETIC_MARKER):]
        spans.append((m.start(), m.end(), body))
    return spans


def _scan_line(line: str, path: str, path_bound: bool) -> list[SealFinding]:
    findings: list[SealFinding] = []
    exempt_spans: list[tuple[int, int]] = []

    # 1. classify every marked token FIRST (they gate the real-shape scan).
    for start, end, body in _marker_spans(line):
        real_kind = _demarked_matches_real_shape(body)
        if real_kind is not None:
            # (a.2) a real-SHAPED marked value FAILS even when marked — the marker cannot launder a shape.
            findings.append(SealFinding(path, f"marked_real_shape:{real_kind}",
                                        "marked value's demarked body matches a real-secret shape (fail)"))
        elif not path_bound:
            # (a.2) a marked (shape-clean) value OUTSIDE the fixtures path FAILS — mis-placed.
            findings.append(SealFinding(path, "marked_out_of_path",
                                        "SEAL_AUDIT_SYNTHETIC_ marker outside the designated fixtures path (fail)"))
        else:
            # path-bound AND shape-clean -> EXEMPT. Exclude this span from the real-shape scan below.
            exempt_spans.append((start, end))

    def _in_exempt(pos: int) -> bool:
        return any(s <= pos < e for (s, e) in exempt_spans)

    # 2. real-secret VALUE shapes (outside exempt spans).
    for kind, rx in _REAL_SHAPES:
        for m in rx.finditer(line):
            if _in_exempt(m.start()):
                continue
            findings.append(SealFinding(path, kind, f"real-secret shape {kind} matched"))

    # 3. NAME=value bindings (a slot name bound to a non-placeholder value). Check the VALUE's position
    #    against the exempt spans (the NAME sits before an exempt marker value; the value is what matters).
    for m in _NAME_VALUE.finditer(line):
        if _in_exempt(m.start("val")):
            continue  # the bound value is an exempt (path-bound + shape-clean) marked fixture
        val = m.group("val").strip("\"'")  # strip surrounding quotes (TOML/JSON) before classifying
        if _PLACEHOLDER.match(val):
            continue  # a documented placeholder / slot name / ${...} reference — allowed (a name is not a value)
        findings.append(SealFinding(path, "secret_name_bound_value",
                                    f"secret slot NAME bound to a non-placeholder VALUE ({val[:8]}…)"))

    # 4. fail-CLOSED on ambiguous high-entropy blobs (base64 >= 100 / non-digest hex >= 100).
    for m in _B64_BLOB.finditer(line):
        if _in_exempt(m.start()):
            continue
        findings.append(SealFinding(path, "base64_blob",
                                    "high-entropy base64 blob (>=100) — unclassified, fail-closed"))
    for m in _HEX_BLOB.finditer(line):
        if _in_exempt(m.start()):
            continue
        if _is_recognized_digest(m.group(0)):
            continue  # a value-free sha256 digest — recognized SAFE
        findings.append(SealFinding(path, "hex_blob",
                                    "high-entropy hex blob (>=100, not a sha256 digest) — fail-closed"))

    return findings


def _is_path_bound(path: str, fixtures_dir: Path | None) -> bool:
    p = str(path).replace("\\", "/")
    if FIXTURES_SEGMENT in p:
        return True
    if fixtures_dir is not None:
        try:
            Path(path).resolve().relative_to(fixtures_dir.resolve())
            return True
        except (ValueError, OSError):
            return False
    return False


def scan_findings(tree_paths, emitted_logs=None, fixtures_dir=None) -> list[SealFinding]:
    """Return every SealFinding (empty list == clean). `tree_paths` are file paths; `emitted_logs` are log
    strings (NEVER path-bound). `fixtures_dir` optionally pins the designated fixtures path (else the
    FIXTURES_SEGMENT substring test is used)."""
    findings: list[SealFinding] = []
    for path in tree_paths:
        path_bound = _is_path_bound(path, fixtures_dir)
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as fh:
                for line in fh:
                    findings.extend(_scan_line(line.rstrip("\n"), str(path), path_bound))
        except (OSError, UnicodeError):
            # An unreadable tracked file is itself suspicious -> fail-closed.
            findings.append(SealFinding(str(path), "unreadable", "tracked file unreadable — fail-closed"))
    for i, line in enumerate(emitted_logs or []):
        # emitted logs are NEVER path-bound (a marker in a log always fails the path-bound test).
        findings.extend(_scan_line(str(line), f"<emitted-log#{i}>", path_bound=False))
    return findings


def seal_audit(tree_paths, emitted_logs=None, fixtures_dir=None) -> None:
    """The build GATE. Raises SealAuditError (build FAILS non-zero) if ANY finding. Absence of a finding is
    the only pass (fail-closed)."""
    findings = scan_findings(tree_paths, emitted_logs=emitted_logs, fixtures_dir=fixtures_dir)
    if findings:
        raise SealAuditError(findings)
