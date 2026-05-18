"""
bw_tickets.py — check-2 + check-3: bw ticket existence + status + §13 placement walk.

check-2: every cited stoa--<id> ticket in SPECIFICATION.md exists in bw with
         claimed status (compare bw show line-1 glyph against surrounding-prose claim).

check-3: bw list --status open --all tickets all placed in some §13.x ticket-placing
         section of SPECIFICATION.md (§12.3 / §12.5 dynamic walk).

bw show line-1 shape (live ground-check 2026-05-18):
    # ○ stoa--<id> — <subject>          (open)
    # ✓ stoa--<id> — <subject>          (closed)

Per CAPTAIN_DAEDALUS.md §6.9 clause 4 (ground-check shipped tool surface):
glyphs are Unicode (○ = U+25CB; ✓ = U+2713). NOT "Status:" line — bw does not
emit that shape at all.

Invocation:
    python substrate/skills/validate-spec/_lib/bw_tickets.py --mode {check-2|check-3} \\
        [--spec <path>] [--repo-root <path>]

Output: JSONL records on stdout. One record per ticket-check + summary.
Exit code: always 0 on successful run; 2 if bw unavailable.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import subprocess
import sys


# ---- regex patterns ---------------------------------------------------------

# stoa-- ticket id pattern (word-boundary anchored to avoid sub-word matches)
_RE_TICKET_ID = re.compile(r"\bstoa--[a-z0-9]+\b")

# bw show line-1 glyphs (live ground-checked)
_GLYPH_OPEN = "○"  # U+25CB
_GLYPH_CLOSED = "✓"  # U+2713

# Claim words near a ticket citation in SPECIFICATION.md prose
_CLAIM_OPEN_PATTERNS = re.compile(
    r"\b(open|in[- ]flight|deferred|in[- ]progress|active|tracking|pending)\b",
    re.IGNORECASE,
)
_CLAIM_CLOSED_PATTERNS = re.compile(
    r"\b(closed|done|shipped|dropped|completed|finished|landed|merged)\b",
    re.IGNORECASE,
)


def _git_repo_root() -> pathlib.Path | None:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True, text=True, check=True,
        )
        return pathlib.Path(result.stdout.strip()).resolve()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


# ---- bw helpers -------------------------------------------------------------

def _bw_show_line1(ticket_id: str) -> tuple[str | None, str | None]:
    """Return (line1, error) for bw show <ticket_id>. line1 is None on error."""
    try:
        result = subprocess.run(
            ["bw", "show", ticket_id],
            capture_output=True, text=True, timeout=30,
        )
    except FileNotFoundError:
        return None, "bw command not found"
    except subprocess.TimeoutExpired:
        return None, "bw show timed out"
    if result.returncode != 0:
        return None, f"bw show exit {result.returncode}: {result.stderr.strip()[:200]}"
    first_line = result.stdout.splitlines()[0] if result.stdout else ""
    return first_line, None


def _glyph_from_line1(line1: str) -> str | None:
    """Return 'open', 'closed', or None if no recognized glyph."""
    if _GLYPH_OPEN in line1:
        return "open"
    if _GLYPH_CLOSED in line1:
        return "closed"
    return None


def _bw_list_open_all() -> tuple[list[str], str | None]:
    """Return (list of open ticket ids, error)."""
    try:
        result = subprocess.run(
            ["bw", "list", "--status", "open", "--all"],
            capture_output=True, text=True, timeout=60,
        )
    except FileNotFoundError:
        return [], "bw command not found"
    except subprocess.TimeoutExpired:
        return [], "bw list timed out"
    if result.returncode != 0:
        return [], f"bw list exit {result.returncode}: {result.stderr.strip()[:200]}"

    ticket_ids: list[str] = []
    seen: set[str] = set()
    for line in result.stdout.splitlines():
        # bw list lines: "# ○ stoa--<id> — <subject>" or similar
        match = _RE_TICKET_ID.search(line)
        if match and match.group(0) not in seen:
            ticket_ids.append(match.group(0))
            seen.add(match.group(0))
    return ticket_ids, None


# ---- check-2: cited-ticket existence + status -------------------------------

def _extract_cited_tickets(spec_text: str) -> list[tuple[str, int, str]]:
    """Return [(ticket_id, line_number, surrounding_line_text), ...].

    One entry per unique (ticket_id, line_number) — same ticket on different lines
    yields separate entries (each may have a different surrounding-prose claim).
    """
    out: list[tuple[str, int, str]] = []
    seen: set[tuple[str, int]] = set()
    for lineno, line in enumerate(spec_text.splitlines(), start=1):
        for match in _RE_TICKET_ID.finditer(line):
            key = (match.group(0), lineno)
            if key in seen:
                continue
            seen.add(key)
            out.append((match.group(0), lineno, line.strip()))
    return out


def _classify_claim(line_text: str) -> str:
    """Return 'open', 'closed', or 'ambiguous' based on surrounding prose."""
    has_open = bool(_CLAIM_OPEN_PATTERNS.search(line_text))
    has_closed = bool(_CLAIM_CLOSED_PATTERNS.search(line_text))
    if has_closed and not has_open:
        return "closed"
    if has_open and not has_closed:
        return "open"
    return "ambiguous"


def _run_check_2(spec_path: pathlib.Path) -> None:
    spec_text = spec_path.read_text(encoding="utf-8")
    cited = _extract_cited_tickets(spec_text)

    pass_count = 0
    fail_count = 0
    strange_count = 0

    # Cache bw show results to avoid duplicate calls for repeated ticket ids
    glyph_cache: dict[str, tuple[str | None, str | None]] = {}

    for ticket_id, lineno, line_text in cited:
        if ticket_id not in glyph_cache:
            line1, err = _bw_show_line1(ticket_id)
            actual_glyph = _glyph_from_line1(line1) if line1 else None
            glyph_cache[ticket_id] = (actual_glyph, err)
        actual_glyph, err = glyph_cache[ticket_id]

        if err:
            verdict = "FAIL"
            fail_count += 1
            actual_status = None
        elif actual_glyph is None:
            verdict = "STRANGE"
            strange_count += 1
            actual_status = "no-glyph"
        else:
            actual_status = actual_glyph
            claim = _classify_claim(line_text)
            if claim == "ambiguous":
                verdict = "STRANGE"
                strange_count += 1
            elif claim == actual_status:
                verdict = "PASS"
                pass_count += 1
            else:
                verdict = "FAIL"
                fail_count += 1

        record = {
            "ticket": ticket_id,
            "citing_line_in_spec": lineno,
            "citing_line_text": line_text[:200],
            "actual_status": actual_status,
            "bw_error": err,
            "verdict": verdict,
        }
        print(json.dumps(record))

    summary = {
        "summary": True,
        "mode": "check-2",
        "total": pass_count + fail_count + strange_count,
        "pass": pass_count,
        "fail": fail_count,
        "strange": strange_count,
    }
    print(json.dumps(summary))


# ---- check-3: open-ticket §13.x placement walk ------------------------------

# §13.x section header in SPECIFICATION.md — matches "### §13.1" / "## §13.10" etc.
_RE_SECTION_13X = re.compile(r"^#+\s+§?13\.[0-9]+[a-z]?\b")
# Section boundary: any heading at the same level OR higher (#+)
_RE_ANY_SECTION = re.compile(r"^#+\s+")


def _collect_section_13x_bodies(spec_text: str) -> dict[str, str]:
    """Return {section_anchor (e.g., '13.1'): body_text} for each §13.x in spec."""
    sections: dict[str, list[str]] = {}
    current_anchor: str | None = None
    in_section = False

    for line in spec_text.splitlines():
        if _RE_SECTION_13X.match(line):
            # Extract anchor like "13.10" from heading
            match = re.search(r"§?(13\.[0-9]+[a-z]?)", line)
            if match:
                current_anchor = match.group(1)
                sections.setdefault(current_anchor, []).append(line)
                in_section = True
                continue
        if in_section and _RE_ANY_SECTION.match(line):
            # Boundary — but stay in if it's a nested §13.x sub-header
            sub_match = re.match(r"^#+\s+§?(13\.[0-9]+[a-z]?)\b", line)
            if sub_match and sub_match.group(1).startswith(current_anchor or ""):
                # Same major-section family; continue
                sections[current_anchor].append(line)
                continue
            # Heading at same or higher level outside §13 — end current section
            in_section = False
            current_anchor = None
            continue
        if in_section and current_anchor is not None:
            sections[current_anchor].append(line)

    return {anchor: "\n".join(body) for anchor, body in sections.items()}


def _run_check_3(spec_path: pathlib.Path) -> None:
    spec_text = spec_path.read_text(encoding="utf-8")
    section_bodies = _collect_section_13x_bodies(spec_text)

    open_tickets, err = _bw_list_open_all()
    if err:
        print(json.dumps({"error": err}), file=sys.stderr)
        summary = {
            "summary": True,
            "mode": "check-3",
            "bw_error": err,
            "total": 0,
            "pass": 0,
            "fail": 0,
        }
        print(json.dumps(summary))
        return

    pass_count = 0
    fail_count = 0

    for ticket_id in open_tickets:
        placing_sections = []
        for anchor, body in section_bodies.items():
            if ticket_id in body:
                placing_sections.append(anchor)

        if placing_sections:
            verdict = "PASS"
            pass_count += 1
        else:
            verdict = "FAIL"
            fail_count += 1

        record = {
            "ticket": ticket_id,
            "placing_sections": placing_sections,
            "verdict": verdict,
        }
        print(json.dumps(record))

    summary = {
        "summary": True,
        "mode": "check-3",
        "total": pass_count + fail_count,
        "pass": pass_count,
        "fail": fail_count,
        "open_tickets_scanned": len(open_tickets),
        "sections_walked": list(section_bodies.keys()),
    }
    print(json.dumps(summary))


# ---- main -------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description="check-2 + check-3: bw ticket existence + placement walk for validate-spec"
    )
    parser.add_argument("--mode", choices=["check-2", "check-3"], required=True)
    parser.add_argument("--spec", default="SPECIFICATION.md")
    parser.add_argument("--repo-root", default=None)
    args = parser.parse_args()

    if args.repo_root:
        repo_root = pathlib.Path(args.repo_root).resolve()
    else:
        repo_root = _git_repo_root()
        if repo_root is None:
            print(json.dumps({"error": "could not determine repo root via git"}), file=sys.stderr)
            return 2

    spec_path = pathlib.Path(args.spec)
    if not spec_path.is_absolute():
        spec_path = (repo_root / args.spec).resolve()

    if not spec_path.is_file():
        print(json.dumps({"error": f"spec file not found: {spec_path}"}), file=sys.stderr)
        return 2

    if args.mode == "check-2":
        _run_check_2(spec_path)
    else:
        _run_check_3(spec_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
