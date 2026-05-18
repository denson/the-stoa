"""
spec_refs.py — check-1: §-reference resolver.

Walks SPECIFICATION.md for §-references in three forms:
  (a) <file>.md §X.Y               — full canonical form
  (b) bare §X.Y                    — defaults to operating-disciplines.md
                                     per SPECIFICATION.md line 7 "Reading note"
  (c) <file> §X.Y                  — without .md extension (rare but present)

For each cited (file, anchor) pair: confirm target file exists; confirm target
file contains a heading line whose §-anchor matches the cited value.

Output: per-reference table (cited-site, target-file, target-§-anchor,
resolved-line-in-target, PASS/FAIL/STRANGE). FAILs are unresolved references.
STRANGE = reference is ambiguous (e.g., file form unclear).

Invocation:
    python substrate/skills/validate-spec/_lib/spec_refs.py [--spec <path>] [--repo-root <path>]

Exit code: always 0 on successful run (drift is informational per A20).
Per-reference verdicts are emitted as structured records on stdout.

Per CAPTAIN_DAEDALUS.md §6.9 (Probe-grounding discipline): the regex patterns
below are anchored against the surrounding-context substrings that disambiguate
intended matches from incidental prose. See _emit_records() for the per-form
regex shapes.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import subprocess
import sys
from typing import Iterator


# ---- regex patterns (anchored per §6.9 clause 1) -----------------------------

# Form (a): <file>.md §X.Y — e.g., "operating-disciplines.md §12.4"
#   anchored: capture the .md filename + space + § + alphanumeric/dot/hyphen anchor
_RE_FORM_A = re.compile(
    r"\b([A-Za-z0-9_.\-/]+\.md)\s+§([0-9A-Za-z.\-]+)"
)

# Form (b): bare §X.Y — e.g., "§12.4" without preceding .md filename
#   anchored: requires § at non-alphanumeric boundary (avoid matching "U+00A7" prose)
#   filtered downstream: skip if preceded by .md within ~30 chars (form (a) match)
_RE_FORM_B = re.compile(
    r"(?:^|[\s\(\[\,;:])§([0-9][0-9A-Za-z.\-]*)"
)

# Form (c): <file> §X.Y — e.g., "CAPTAIN_DAEDALUS §6.9" without .md
#   anchored: uppercase-prefixed identifier (CAPTAIN_*, MAJOR_*) followed by § anchor
_RE_FORM_C = re.compile(
    r"\b((?:CAPTAIN|MAJOR)_[A-Z]+)\s+§([0-9A-Za-z.\-]+)"
)

# Heading-line shape in target files — flexible: matches "### 6.9 Title" or
# "## 12.4 Title" or "**§6.9 Title**" or "### §6.9 — Title"
def _heading_pattern_for_anchor(anchor: str) -> re.Pattern:
    """Build a regex that matches a heading line containing the given anchor."""
    # Escape regex meta in anchor
    anchor_esc = re.escape(anchor)
    return re.compile(
        rf"^(#+\s+§?{anchor_esc}[\s.\-:]|#+\s+{anchor_esc}[\s.\-:]|\*\*§?{anchor_esc}[\s.\-:])",
        re.MULTILINE,
    )


# ---- ref extraction ---------------------------------------------------------

def _extract_references(spec_text: str) -> Iterator[tuple[int, str, str | None, str]]:
    """Yield (line_number, citing_line_text, target_file_or_None, anchor).

    target_file_or_None: None for bare-§ form (defaults to operating-disciplines.md).
    """
    seen_per_line: dict[int, set[tuple[str | None, str]]] = {}

    for lineno, line in enumerate(spec_text.splitlines(), start=1):
        # Form (a) first — most specific
        for match in _RE_FORM_A.finditer(line):
            target_file = match.group(1)
            anchor = match.group(2)
            key = (target_file, anchor)
            seen_per_line.setdefault(lineno, set()).add(key)
            yield (lineno, line.strip(), target_file, anchor)

        # Form (c) — file without .md (only CAPTAIN/MAJOR prefix)
        for match in _RE_FORM_C.finditer(line):
            target_stem = match.group(1)
            anchor = match.group(2)
            target_file = f"{target_stem}.md"
            key = (target_file, anchor)
            if key in seen_per_line.get(lineno, set()):
                continue
            seen_per_line.setdefault(lineno, set()).add(key)
            yield (lineno, line.strip(), target_file, anchor)

        # Form (b) last — only if not already matched
        for match in _RE_FORM_B.finditer(line):
            anchor = match.group(1)
            # If this anchor was already matched as part of form (a) or (c), skip
            already_matched_as_a_or_c = any(
                key[1] == anchor for key in seen_per_line.get(lineno, set())
            )
            if already_matched_as_a_or_c:
                continue
            # Bare-§: defaults to operating-disciplines.md
            yield (lineno, line.strip(), None, anchor)


# ---- resolver ---------------------------------------------------------------

_BARE_DEFAULT_FILE = "substrate/operating-disciplines.md"


def _resolve_target_path(repo_root: pathlib.Path, target_file: str | None) -> pathlib.Path | None:
    """Map a cited target_file to an absolute path under repo_root, or None if unresolved."""
    if target_file is None:
        # Bare-§ form — defaults to operating-disciplines.md
        candidate = repo_root / _BARE_DEFAULT_FILE
        return candidate if candidate.is_file() else None

    # Try direct under repo root, then under substrate/, then under agents/
    for prefix in ["", "substrate/", "agents/", "agents/design/"]:
        candidate = repo_root / f"{prefix}{target_file}"
        if candidate.is_file():
            return candidate
    return None


def _find_anchor_in_target(target_path: pathlib.Path, anchor: str) -> int | None:
    """Return the 1-indexed line number of the first heading matching anchor, or None."""
    pattern = _heading_pattern_for_anchor(anchor)
    try:
        with target_path.open("r", encoding="utf-8") as fh:
            for lineno, line in enumerate(fh, start=1):
                if pattern.match(line):
                    return lineno
    except (OSError, UnicodeDecodeError):
        return None
    return None


# ---- main -------------------------------------------------------------------

def _emit_records(spec_path: pathlib.Path, repo_root: pathlib.Path) -> int:
    """Emit one JSONL record per reference. Returns count of FAIL refs."""
    try:
        spec_text = spec_path.read_text(encoding="utf-8")
    except OSError as exc:
        print(json.dumps({"error": f"could not read spec: {exc}"}), file=sys.stderr)
        return -1

    fail_count = 0
    pass_count = 0
    strange_count = 0
    for lineno, line_text, target_file, anchor in _extract_references(spec_text):
        target_path = _resolve_target_path(repo_root, target_file)
        if target_path is None:
            verdict = "FAIL"
            resolved_line = None
            fail_count += 1
        else:
            anchor_line = _find_anchor_in_target(target_path, anchor)
            if anchor_line is None:
                verdict = "FAIL"
                resolved_line = None
                fail_count += 1
            else:
                verdict = "PASS"
                resolved_line = anchor_line
                pass_count += 1

        record = {
            "citing_line_in_spec": lineno,
            "citing_line_text": line_text[:200],  # truncate to avoid runaway logs
            "target_file_cited": target_file or "(bare-§ → operating-disciplines.md)",
            "target_file_resolved": str(target_path.relative_to(repo_root)) if target_path else None,
            "anchor": anchor,
            "resolved_line_in_target": resolved_line,
            "verdict": verdict,
        }
        print(json.dumps(record))

    summary = {
        "summary": True,
        "total": pass_count + fail_count + strange_count,
        "pass": pass_count,
        "fail": fail_count,
        "strange": strange_count,
    }
    print(json.dumps(summary))
    return fail_count


def main() -> int:
    parser = argparse.ArgumentParser(description="check-1: §-reference resolver for validate-spec")
    parser.add_argument("--spec", default="SPECIFICATION.md", help="path to spec file (default: SPECIFICATION.md)")
    parser.add_argument("--repo-root", default=None, help="repo root (default: git rev-parse --show-toplevel)")
    args = parser.parse_args()

    if args.repo_root:
        repo_root = pathlib.Path(args.repo_root).resolve()
    else:
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--show-toplevel"],
                capture_output=True,
                text=True,
                check=True,
            )
            repo_root = pathlib.Path(result.stdout.strip()).resolve()
        except (subprocess.CalledProcessError, FileNotFoundError):
            print(json.dumps({"error": "could not determine repo root via git"}), file=sys.stderr)
            return 2

    spec_path = pathlib.Path(args.spec)
    if not spec_path.is_absolute():
        spec_path = (repo_root / args.spec).resolve()

    if not spec_path.is_file():
        print(json.dumps({"error": f"spec file not found: {spec_path}"}), file=sys.stderr)
        return 2

    _emit_records(spec_path, repo_root)
    return 0


if __name__ == "__main__":
    sys.exit(main())
