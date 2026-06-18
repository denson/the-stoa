#!/usr/bin/env bash
#
# _hooklib.sh — shared helpers for the Stoa PreToolUse / Stop hook scripts.
#
# NOT a hook itself (leading underscore + no settings.json registration). The
# install.sh hooks deploy class globs substrate/hooks/*.sh, so this file ships
# alongside the gates; the settings-hooks.json template registers ONLY the
# gate scripts, never this lib. Each gate sources this file by absolute path
# (the deployed location, computed from the gate's own location).
#
# Design contract (design-rev1 §4): every gate is deterministic, compaction-
# immune (nothing depends on the model's context), and FAIL-OPEN on its own
# error — a buggy gate degrades to today's no-enforcement baseline rather than
# bricking the running team (ARGUS R5 confirmed this inversion is correct for
# this layer). The usual "fail closed for safety" default is deliberately
# inverted here: a fail-CLOSED gate that errors would block every gated tool
# call in the live session, which is the exact harm the HARD SAFETY CONSTRAINT
# guards against.

# read_stdin_event: slurp the hook event JSON from stdin into HOOK_EVENT_JSON.
# Hooks are invoked once per event with the JSON on stdin; we read it whole.
read_stdin_event() {
  HOOK_EVENT_JSON="$(cat)"
}

# json_field <jq-style-path> : extract a string field from HOOK_EVENT_JSON.
# Uses python3 (POSIX-portable, assumed present on substrate targets per
# operating-disciplines.md §13; jq is NOT assumed present — design §9 weak
# point 1). On ANY parse failure (no python3, malformed JSON, missing field)
# this echoes empty and returns non-zero, and the CALLER must fail-OPEN
# (allow the tool call) — never block on a parse failure.
#
#   $1 = a dotted path into the event object, e.g. "tool_input.command"
#        or "tool_name" or "session_id".
json_field() {
  local path="$1"
  # NOTE: the program is passed via `-c` (NOT a heredoc) so the hook event JSON
  # piped on stdin remains available to json.load(sys.stdin). A `python3 - <<PY`
  # heredoc would consume stdin for the PROGRAM, leaving sys.stdin empty — the
  # bug this form avoids. The dotted path is argv[1].
  python3 -c '
import sys, json
path = sys.argv[1]
try:
    obj = json.load(sys.stdin)
except Exception:
    sys.exit(1)
cur = obj
for part in path.split("."):
    if isinstance(cur, dict) and part in cur:
        cur = cur[part]
    else:
        sys.exit(1)
if cur is None:
    sys.exit(1)
if isinstance(cur, bool):
    # Emit JSON-style lowercase (true/false), not Python str(True)="True",
    # so shell callers can compare against "true"/"false".
    sys.stdout.write("true" if cur else "false")
elif isinstance(cur, (dict, list)):
    sys.stdout.write(json.dumps(cur))
else:
    sys.stdout.write(str(cur))
' "$path" 2>/dev/null
}

# Convenience wrapper: extract a field from the already-slurped event.
# Pipes HOOK_EVENT_JSON into json_field so the caller does not re-read stdin
# (stdin is consumed once by read_stdin_event).
event_field() {
  printf '%s' "$HOOK_EVENT_JSON" | json_field "$1"
}

# --- Arc 65 / stoa--z2b: unified author-file classify + mode contract ---------
# classify_author_file (membership + mode in ONE decision) + the mode-aware
# extract_author_fields below form a single contract: the gate caller calls
# classify_author_file once to learn BOTH whether a path is author-encoding AND
# which extraction mode to use, then passes that mode to extract_author_fields.
# Config-class files (incl. LICENSE.md and *.claude-plugin/*.md docs) get "cfg"
# = the OLD whole-file scan, byte-identical to pre-Arc-65; a PROSE .md gets "md"
# = a frontmatter-only scan. The config arms are tested FIRST so they win over
# the bare *.md arm — mode can never disagree with membership (no second list).

# classify_author_file <path> : author-encoding membership AND extraction mode in
# ONE decision, so the two can never disagree (Arc 65 / stoa--z2b r1). Prints the
# extraction mode ("cfg" = OLD whole-file scan; "md" = frontmatter-only scan) and
# returns 0 when <path> is an author-encoding file; prints nothing and returns 1
# when it is NOT author-encoding. The mode is derived from the SAME case arms (in
# the SAME priority order) as membership: every CONFIG-class arm yields cfg; ONLY
# the bare *.md arm (a prose markdown file) yields md. Because the config arms are
# tested first, LICENSE.md (LICENSE.* arm) and *.claude-plugin/*.md (plugin-path
# arm) return cfg BEFORE the bare *.md arm is reached — they keep whole-file
# coverage even though they end .md. NOTICE.md / package.json.md etc. are NOT
# config-class (basename not in the literal list) so they fall to the bare *.md
# arm and get md mode — the acceptable Q-B residual, identical OLD-vs-new.
classify_author_file() {
  local p="$1" base
  base="$(basename "$p")"
  # --- CONFIG-class (whole-file cfg scan) — tested FIRST so it wins over *.md ---
  case "$base" in
    plugin.json|marketplace.json|package.json|pyproject.toml|setup.py|Cargo.toml|Gemfile|composer.json|NOTICE|CITATION.cff|metadata.json|manifest.json)
      printf 'cfg'; return 0 ;;
    LICENSE|LICENSE.*|LICENSE.md)
      printf 'cfg'; return 0 ;;
  esac
  case "$p" in
    *.claude-plugin/*)
      printf 'cfg'; return 0 ;;   # plugin docs incl. *.claude-plugin/*.md
  esac
  # --- prose markdown (frontmatter-only md scan) — reached only if NO config arm matched ---
  case "$p" in
    *.md)
      printf 'md'; return 0 ;;    # author: lives in the leading YAML frontmatter
  esac
  return 1
}

# extract_author_fields : read a file's text on stdin, emit one
# "<field>\t<value>" line per author-like field assignment found. Handles the
# three encodings author-like fields appear in: JSON ("author": "X"), YAML
# (author: X), and TOML/ini (author = "X"). Field-anchored so a compact
# single-line JSON object yields the VALUE bound to the author key, not the
# whole line (the brittle "everything after the first colon" bug this replaces).
# Values are unquoted + trimmed; array values (JSON [..] / YAML/TOML lists) are
# flattened to one element per line. Template placeholders ({{..}}, <..>, $..)
# are skipped. python3-only (the gate fail-OPENs if python3 is absent).
#
# Field set (case-insensitive): author authors owner creator created_by
# maintainer maintainers by copyright holder vendor publisher.
#
# MODE (Arc 65 / stoa--z2b): the FIRST arg selects the extraction mode via the
# MODE env var (default "cfg"). "cfg" = the OLD whole-blob scan (byte-identical
# to pre-Arc-65), used for every config-class file incl. LICENSE.md and
# *.claude-plugin/*.md docs. "md" = a PROSE markdown file: only the leading YAML
# frontmatter block is scanned (body prose that merely DISCUSSES authorship is
# NOT a structured field and must not trip the gate). The mode is decided by
# classify_author_file (above) so it can never disagree with membership. A caller
# that forgets the mode gets "cfg" — the SAFE broadest scan (fail toward MORE
# enforcement).
extract_author_fields() {
  MODE="${1:-cfg}" python3 -c '
import sys, re, os
text = sys.stdin.read()
mode = os.environ.get("MODE", "cfg")
FIELDS = ["authors","author","owner","creator","created_by","maintainers","maintainer","by","copyright","holder","vendor","publisher"]
# Match: optional quote, field name, optional quote, separator (: or =), then
# the rest of the value up to end-of-line. Anchor the field as a whole word.
key = "|".join(FIELDS)

# --- .md NARROWING (Arc 65 / stoa--z2b) -------------------------------------
# md mode = a PROSE markdown file (classify_author_file returned "md", i.e. NOT
# a config-class LICENSE.md / *.claude-plugin/*.md). Author-like fields are only
# STRUCTURED in the leading YAML frontmatter block (--- ... ---). Body prose that
# merely DISCUSSES authorship ("**Authored by:** <seat> + PRINCIPAL", "author =
# Denson Smith; no other person...", a verdict AUDIT line) is NOT a structured
# author field and must NOT trip the gate. So in md mode we (1) slice out the
# leading frontmatter block (empty if absent), and (2) match author keys only at
# YAML line-start with a ":" separator. cfg mode keeps the OLD whole-blob scan,
# byte-identical, for every config-class file (incl. LICENSE.md / plugin docs).
if mode == "md":
    # Leading frontmatter only: optional UTF-8 BOM, "---" line, body, "---" line.
    # Tolerant of CRLF and trailing spaces on the fence lines.
    fm = re.match(r"^﻿?---[ \t]*\r?\n(.*?)\r?\n---[ \t]*(?:\r?\n|$)", text, re.DOTALL)
    text = fm.group(1) if fm else ""
    pat = re.compile(r"""(?ix)
        ^[ \t]*                              # YAML key at line start (indent ok)
        ["\x27]?(""" + key + r""")["\x27]?   # the field name (group 1)
        \s*:\s*                              # YAML separator is ":" only
        (.*)$                                # the raw value (group 2)
    """, re.MULTILINE)
else:
    pat = re.compile(r"""(?ix)
        (?<![A-Za-z0-9_])            # not part of a longer identifier
        ["\x27]?(""" + key + r""")["\x27]?   # the field name (group 1)
        \s*[:=]\s*                   # separator
        (.*)$                        # the raw value (group 2)
    """, re.MULTILINE)
def clean_one(tok):
    tok = tok.strip()
    # Prefer a leading quoted string even if trailing chars (} ] ,) follow it,
    # so compact JSON like {"author":"Name"} yields Name (not Name"}).
    m = re.match(r"""^["\x27](.*?)["\x27]""", tok)
    if m:
        return m.group(1).strip()
    # bare token: strip a leading YAML list dash + a trailing comment, then stop
    # at a structural terminator (, } ]).
    tok = re.sub(r"^-\s*", "", tok)
    tok = re.split(r"\s#", tok, 1)[0]
    tok = re.split(r"[,}\]]", tok, 1)[0]
    # strip surrounding quote chars (double = chr(34), single = chr(39)); use
    # chr() so no literal apostrophe appears in this single-quoted shell heredoc.
    return tok.strip().strip(chr(34) + chr(39)).strip()

def emit(field, raw):
    raw = raw.strip()
    if not raw:
        return
    # ARRAY value (JSON/TOML ["a","b"] or YAML inline [a, b]): flatten to one
    # element per emitted line so EACH author in a list is audited. A bare "["
    # with the array continuing on later lines is only partially captured (the
    # same-line elements); that is an accepted limit of a line-anchored scan.
    if raw[:1] == "[":
        inner = raw[1:]
        inner = inner.split("]", 1)[0]
        for piece in inner.split(","):
            v = clean_one(piece)
            if not v or v[:2] == "{{" or v[:1] in ("<", "$"):
                continue
            sys.stdout.write(field + "\t" + v + "\n")
        return
    # Skip an opening brace (JSON object value — not a name) and template
    # placeholders. (An array was handled above; a "{" here is a nested object.)
    if raw[:2] == "{{" or raw[:1] in ("<", "$", "{"):
        return
    val = clean_one(raw.split(",", 1)[0])
    if not val:
        return
    if val[:2] == "{{" or val[:1] in ("<", "$"):
        return
    sys.stdout.write(field + "\t" + val + "\n")
for m in pat.finditer(text):
    field = m.group(1)
    raw = m.group(2)
    # YAML list form: "authors:" with items on following lines is handled by the
    # per-line regex catching each "- family-names: X" / "- X" itself (those
    # lines re-match when they contain an author-like key; bare "- Name" under
    # an authors: key is caught here when the value is on the same line).
    emit(field, raw)
' 2>/dev/null
}

# emit_deny <reason> : print the PreToolUse deny JSON with a self-contained
# reason string and exit 0. Per design §4 the deny uses exit-0 + JSON (not
# exit 2) so the model-facing permissionDecisionReason carries the precise
# message (exit 2 only forwards stderr). The reason is emitted verbatim; the
# CALLER is responsible for making it self-contained (the authoring rule:
# WHY it fired + WHAT to do, inline, no bare "see §X" pointer — a pointer
# fails after compaction). Live hook surface verified 2026-05-23:
# hookSpecificOutput.{hookEventName, permissionDecision:"deny",
# permissionDecisionReason}.
emit_deny() {
  local reason="$1"
  # Encode the reason as a JSON string via python3 so embedded quotes /
  # newlines / backslashes are escaped correctly. If python3 is unavailable
  # we cannot safely build the JSON, so we FAIL-OPEN (allow) rather than emit
  # malformed JSON that the harness might mis-handle.
  local reason_json
  reason_json="$(REASON="$reason" python3 -c 'import os,json,sys; sys.stdout.write(json.dumps(os.environ["REASON"]))' 2>/dev/null)" || {
    # python3 gone — fail OPEN (no enforcement) rather than risk a malformed block.
    exit 0
  }
  printf '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":%s}}\n' "$reason_json"
  exit 0
}

# allow : the default outcome. Exit 0 with no stdout so the normal permission
# flow proceeds untouched. (Explicit function for readability at call sites.)
allow() {
  exit 0
}
