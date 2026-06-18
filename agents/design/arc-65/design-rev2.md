# Arc 65 design-rev2 — Narrow the authorship-attribution gate's `.md` matcher (stoa--z2b)

**Authored by:** `CAPTAIN_DAEDALUS_the-stoa` (architect) + the PRINCIPAL (Denson Smith).
**Ticket:** stoa--z2b (P1, BUG, SECURITY-sensitive gate).
**Supersedes:** design-rev1.md (kept for history). This rev folds CAPTAIN_ARGUS's RATIFY-WITH-CONDITIONS verdict (`agents/verdicts/stoa--z2b/ARGUS-2026-06-18T11-26-20Z.md`): r1 (LICENSE.md / `*.claude-plugin/*.md` mode-collision), r7 (corpus must catch r1), Q-B README delegation doc, relocate-not-source-guard, M1 binding.
**Builds on:** the-stoa main `20267e4`; directive `beadwork:attachments/stoa--z2b/arc-65-build-directive.md` (NOMOS CONFORMANT).
**Fix surface:** `substrate/hooks/_hooklib.sh` (`extract_author_fields`, NEW `classify_author_file`), `substrate/hooks/pretooluse-author-field-audit.sh` (sub-check 2 caller; removes the inlined `is_author_encoding_file`) + the byte-identical deployed mirror `.claude/hooks/`.

---

## §1 — Problem restatement

The PreToolUse authorship gate (`pretooluse-author-field-audit.sh` sub-check 2) treats **every `*.md`
file** as an author-encoding file and runs the **MULTILINE, anywhere-in-blob** regex
(`extract_author_fields`, `_hooklib.sh:86-152`) over its whole text. That regex matches any of 12
author-like FIELD words followed by `:` or `=` ANYWHERE — so it fires on `.md` **body prose** that
merely discusses authorship, not on a structured author field. Reproduced live (rev1, re-confirmed):

- FP1 — `**Authored by:** user-tier POLYBIUS (chief-of-staff) + the PRINCIPAL (Denson Smith).`
  → matches field `by` → `is_principal` rejects the seat value → **DENY**.
- FP2 — `expected: html author = Denson Smith; no other person in any author field`
  → matches field `author`, value `Denson Smith; no other person...` → **DENY**.
- N+1 (Arc 64) — a CATO verdict-body authorship-AUDIT prose line blocks an in-tree verdict commit.

None is a real violation: the only PERSON named is Denson Smith (allow-listed); "POLYBIUS" is a SEAT.

**The fix (both directions load-bearing — a one-direction pass is a FAIL):**
1. `.md` **body prose** discussing authorship must stop tripping the gate (z2b instances commit clean).
2. A **real structured author field naming a non-Denson PERSON** must still BLOCK — the regression the
   gate exists to prevent (a reputational/legal footgun that has regressed TWICE). This means: structured
   config files (`package.json`, `pyproject.toml`, `Cargo.toml`, `LICENSE`, `LICENSE.md`, `NOTICE`,
   `CITATION.cff`, plugin/marketplace manifests, **`*.claude-plugin/*.md` plugin docs**) **and** `.md`
   **YAML-frontmatter** `author:` lines must keep blocking.

**The rev1 gap ARGUS caught (now the load-bearing constraint of rev2):** `is_author_encoding_file`
deliberately classes **two** `.md`-suffixed shapes as CONFIG-class author files that expect a WHOLE-FILE
scan: `LICENSE.md` (the `LICENSE.*`/`LICENSE.md` `case "$base"` arm, line 118) and `*.claude-plugin/*.md`
(the `*.claude-plugin/*` `case "$p"` arm, line 121). Rev1's caller dispatched extraction mode by the bare
`*.md` glob alone, so both shapes were forced into frontmatter-only `md` mode — losing the body
`Copyright:`/`Author: <non-Denson>` coverage the OLD `cfg` gate had. That is a true-positive class covered
before and not after = the directive's FAIL condition. **Rev2 makes the mode decision derive from the SAME
classification logic that decides author-encoding membership, so the two can never disagree (C1).**

**The precise collision set (ARGUS ruled, adopted verbatim):** EXACTLY TWO classes route to `cfg` despite
ending `.md` — `LICENSE.md` and `*.claude-plugin/*.md`. `NOTICE.md` is NOT a collision (basename
`NOTICE.md` ≠ the literal `NOTICE`, so it was never config-class; its body author line is the acceptable
Q-B residual, identical OLD-vs-new behavior). Same for `package.json.md` etc. (basename not literal).

**Imported assumption (named):** "structured author position in a `.md` whose membership comes ONLY from
the bare `*.md` arm" = the YAML frontmatter block. Body `Author:` lines in such a `.md` are decided
against coverage in Q-B below — explicitly, not silently.

---

## §2 — Approach

### 2.1 Strategy (rules on Q-A / Q-B / Q-C — unchanged from rev1, ARGUS-confirmed)

**Q-A — RULED: frontmatter-only for a `.md` that is author-encoding SOLELY via the bare `*.md` arm; OLD
full-blob (`cfg`) extraction UNCHANGED for every config-class file — including `LICENSE.md` and
`*.claude-plugin/*.md`.** Chosen over (i) body-aware fence/bold skipping and (ii) a person-name value
heuristic. Rationale: the frontmatter block is the only structured-author position in a prose `.md`; it
kills all z2b instances (all body prose); it is the least brittle of the three; and config-file extraction
(the highest-value true-positives) stays byte-identical.

**Q-B — RULED: do NOT mechanically cover a body `Author: <person>` line in a prose `.md`.** Explicit,
defended (not a silent drop): the body of a prose `.md` is exactly where authorship-DISCUSSION prose lives
(verdict AUDIT lines, §28 docs, directive seat-attribution); there is no mechanical predicate that admits a
real body `Author: Jane Roe` while rejecting `author = Denson Smith; no other person in any author field` —
they are the same lexical surface, so re-covering body lines re-opens z2b. Residual delegated to the prose
discipline + manual audit + NOMOS/human review (the gate was always a backstop). **C3 condition:** the
README MUST document this delegation (what is deliberately no longer matched + why); **no body badge-line
convention is added** (ARGUS ruled against it). ARGUS confirmed the residual is ACCEPTABLE given r1 closes.

**Q-C — DECLINED (value-shape heuristic).** Unchanged: a benign-value heuristic would soften the
config-file true-positive path the directive says must stay hardest. The structural narrowing removes the
z2b false-positives at the source, so the belt-and-suspenders has nothing left worth the risk it adds.

### 2.2 The hand-off contract (caller ⇄ classifier ⇄ extractor) — C1 + C4

Rev1 had TWO sources of truth that could drift: `is_author_encoding_file` (membership) in the gate, and a
separate `case "$f" in *.md) md` mode dispatch in the caller. ARGUS r1 is exactly that drift — the caller's
`*.md` arm overrode the classifier's config-class intent for `LICENSE.md` / `*.claude-plugin/*.md`.

**Rev2 collapses membership AND mode into ONE function, `classify_author_file`, in `_hooklib.sh`:**

- `classify_author_file <path>` prints the extraction mode to stdout (`cfg` or `md`) and returns 0 when the
  path is author-encoding; prints nothing and returns 1 when it is NOT author-encoding.
- The mode is derived from the SAME `case` arms that decide membership, in the SAME priority order: every
  config-class arm (literal basenames, `LICENSE`/`LICENSE.*`/`LICENSE.md`, `*.claude-plugin/*`) yields
  `cfg`; ONLY the bare `*.md` arm yields `md`. Because the config arms are tested FIRST, a `LICENSE.md` or a
  `*.claude-plugin/x.md` matches its config arm and returns `cfg` BEFORE the bare `*.md` arm is ever
  reached. The mode can therefore never disagree with membership — there is no second list to maintain.
- The gate caller calls `classify_author_file "$f"` once: skip if non-zero (not author-encoding); else use
  the printed mode verbatim. The test runner calls the SAME function for both its membership assertion AND
  its mode computation (no parallel reimplementation — floor-manager acceptance #1).

This also satisfies **C4 (relocate)**: `classify_author_file` lives in `_hooklib.sh` (the lib both the gate
and the runner already source); the gate no longer defines any membership/mode function inline. ARGUS ruled
RELOCATE correct over a source-guard (a source-guard injects a new early-return fail-surface into the live
gate; relocating a pure no-I/O function does not). VERA asserts (C4): the gate's deny-set is byte-identical
across the full corpus, AND the classification function is defined exactly once after the move (grep the gate
for any leftover `is_author_encoding_file`/`classify_author_file` definition → none; grep `_hooklib.sh` → one).

---

## §2.3 — The exact change (concrete code, not a sketch)

### Change A — `substrate/hooks/_hooklib.sh`: NEW `classify_author_file` (unified membership + mode)

This is the relocation target (C4) AND the C1 fix. The `case` arms are the EXACT arms of the OLD
`is_author_encoding_file` (lines 116-123), in the EXACT order — only the return is enriched to also print
the mode. Config arms print `cfg`; the bare `*.md` arm (reached only when no config arm matched) prints `md`.

```bash
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
```

> **Note — `LICENSE.*` already subsumes `LICENSE.md`:** the explicit `LICENSE.md` token is redundant under
> `LICENSE.*` but is kept verbatim from the OLD arm so the deny-set is provably byte-identical (C4) — this
> is a pure relocation, not a simplification. Do not collapse it.

### Change B — `substrate/hooks/_hooklib.sh`: `extract_author_fields` (mode-aware)

Mode comes from the first arg `$1` via the `MODE` env var (default `cfg` ⇒ broadest scan when a caller
forgets the mode — fail toward MORE enforcement). The `cfg`-branch regex is **character-for-character the
OLD regex** (`_hooklib.sh:94-99`); `clean_one`/`emit`/array-flatten are reused unchanged by both modes.

```bash
extract_author_fields() {
  MODE="${1:-cfg}" python3 -c '
import sys, re, os
text = sys.stdin.read()
mode = os.environ.get("MODE", "cfg")
FIELDS = ["authors","author","owner","creator","created_by","maintainers","maintainer","by","copyright","holder","vendor","publisher"]
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
    # OLD behavior (config files: JSON / YAML / TOML / LICENSE / CITATION.cff /
    # plugin docs). UNCHANGED — byte-identical to the pre-Arc-65 regex.
    pat = re.compile(r"""(?ix)
        (?<![A-Za-z0-9_])                    # not part of a longer identifier
        ["\x27]?(""" + key + r""")["\x27]?   # the field name (group 1)
        \s*[:=]\s*                           # separator (: or =)
        (.*)$                                # the raw value (group 2)
    """, re.MULTILINE)

def clean_one(tok):
    tok = tok.strip()
    m = re.match(r"""^["\x27](.*?)["\x27]""", tok)
    if m:
        return m.group(1).strip()
    tok = re.sub(r"^-\s*", "", tok)
    tok = re.split(r"\s#", tok, 1)[0]
    tok = re.split(r"[,}\]]", tok, 1)[0]
    return tok.strip().strip(chr(34) + chr(39)).strip()

def emit(field, raw):
    raw = raw.strip()
    if not raw:
        return
    if raw[:1] == "[":
        inner = raw[1:]
        inner = inner.split("]", 1)[0]
        for piece in inner.split(","):
            v = clean_one(piece)
            if not v or v[:2] == "{{" or v[:1] in ("<", "$"):
                continue
            sys.stdout.write(field + "\t" + v + "\n")
        return
    if raw[:2] == "{{" or raw[:1] in ("<", "$", "{"):
        return
    val = clean_one(raw.split(",", 1)[0])
    if not val:
        return
    if val[:2] == "{{" or val[:1] in ("<", "$"):
        return
    sys.stdout.write(field + "\t" + val + "\n")

for m in pat.finditer(text):
    emit(m.group(1), m.group(2))
' 2>/dev/null
}
```

**Notes (each load-bearing):**
- Mode via `MODE` env var, NOT `sys.argv` — keeps the single-quoted heredoc literal-safe and avoids any
  argv collision with `json_field`. Default `cfg` ⇒ a caller that forgets the mode gets the SAFE broadest
  scan (fail toward MORE enforcement).
- `﻿?` tolerates a leading UTF-8 BOM (Windows forge); `\r?\n` tolerates CRLF on both fence lines.
  (Authoring note for ADA: written here as the Python escape `﻿` so this design `.md` itself carries
  no literal BOM mid-file; the deployed source may use the escape or a literal — VERA's P4 BOM probe is the
  ground truth either way.)
- `md` mode uses **`:` only** (YAML); `^[ \t]*` anchors keys to frontmatter line-start. A `.md` with NO
  frontmatter ⇒ `text=""` ⇒ zero matches ⇒ body-prose z2b instances emit nothing.
- The `else` (cfg) branch is byte-identical to the OLD regex; ARGUS confirmed char-for-char.

### Change C — `substrate/hooks/pretooluse-author-field-audit.sh`: caller uses the unified classifier

DELETE the inline `is_author_encoding_file` definition (lines 112-125 — the whole function block including
the `# Author-encoding file matcher.` comment). REPLACE the sub-check 2 loop's membership test + the rev1
`case`-mode dispatch with a single `classify_author_file` call:

```bash
while IFS= read -r f; do
  [ -n "$f" ] || continue
  # Arc 65 (stoa--z2b): one call returns BOTH "is this author-encoding" AND which
  # extraction mode to use, derived from the same classification (see
  # _hooklib.sh classify_author_file). Config-class files (incl. LICENSE.md and
  # *.claude-plugin/*.md docs) get "cfg" = OLD whole-file scan; a PROSE .md gets
  # "md" = frontmatter-only scan so body prose discussing authorship does not
  # false-positive. Non-author-encoding files return non-zero and are skipped.
  _mode="$(classify_author_file "$f")" || continue
  blob="$(git -C "$CWD" show ":${f}" 2>/dev/null)" || continue
  [ -n "$blob" ] || continue
  pairs="$(printf '%s' "$blob" | extract_author_fields "$_mode")" || continue
  [ -n "$pairs" ] || continue
  while IFS="$(printf '\t')" read -r field val; do
    [ -n "$val" ] || continue
    if ! is_principal "$val"; then
      emit_deny "Commit blocked: author-like field \"${field}\" in staged file \"${f}\" names \"${val}\", which is not the PRINCIPAL. ...(message body UNCHANGED from the current gate, lines 141)..."
    fi
  done <<EOF
$pairs
EOF
done <<EOF
$STAGED
EOF
```

**No change** to sub-check 1 (git config author identity), `is_principal`, the allow-list logic, FAIL-OPEN,
or `emit_deny`. The deny-message string is unchanged verbatim (only re-quoted here for brevity).

### Change D — the deployed mirror

`.claude/hooks/_hooklib.sh` and `.claude/hooks/pretooluse-author-field-audit.sh` get the **identical**
edits (the-stoa is the forge; source + deployed land together, byte-identical — VERA asserts
`diff substrate/hooks/X .claude/hooks/X` is empty for both files; P9).

---

## §3 — Test-corpus architecture

### 3.1 Where it lives + the deploy decision (unchanged from rev1)

**Source-only at `substrate/hooks/tests/`. It does NOT deploy.** The hooks deploy loop globs
`${SRC_HOOKS_DIR}/*.sh` (non-recursive — a `tests/` SUBDIR is not matched) and copies `README.md` by
explicit basename only (install.sh:1373 + 1398). A `tests/` subdir is invisible to the deploy. (VERA P8
asserts a dry-run install lists no `tests/` path under `deploy hook:`.) ARGUS confirmed the glob is
non-recursive.

```
substrate/hooks/tests/
  README.md                 # corpus rationale + fixture-naming-is-test-data note (for CATO/NOMOS)
  run-author-gate-tests.sh  # the runner
  fixtures/
    fp/                      # FALSE-POSITIVE — must now PASS (extractor emits nothing in md mode)
      fp1-seat-attribution.md.fixture
      fp2-verdict-audit.md.fixture
      fp3-directive-coauthor.md.fixture
      fp4-section28-docs.md.fixture
    tp/                      # TRUE-POSITIVE — must still BLOCK (extractor emits a non-Denson value)
      tp1-package.json.fixture
      tp2-skill-frontmatter.md.fixture
      tp3-license.fixture
      tp4-notice.fixture
      tp5-citation.cff.fixture
      tp6-license-md.fixture          # NEW (C2 / r7) — LICENSE.md collision class
      tp7-claude-plugin-doc.md.fixture # NEW (C2 / r7) — *.claude-plugin/*.md collision class
    control/                 # CONTROL — must PASS (happy structured path intact)
      ctl1-package-denson.json.fixture
      ctl2-skill-frontmatter-denson.md.fixture
      ctl3-license-md-denson.fixture   # NEW — LICENSE.md w/ Denson copyright must PASS (cfg, allow)
```

### 3.2 The fixture storage scheme (committability — unchanged, ARGUS-confirmed sound)

Every fixture carries a **`.fixture` suffix**. `.fixture` is NOT a triggering name under
`classify_author_file` (basename not in the literal list; does not end `.md`; not under `*.claude-plugin/`),
so a true-positive fixture's non-Denson content commits clean through the OLD main-tree gate. The runner
reconstructs the **intended path** the matcher must SEE from a per-fixture manifest line, NOT the on-disk
name. ARGUS r6 confirmed this is sound — e.g. `tp6-license-md.fixture` has basename ending `.fixture`, is
not `LICENSE.md`, so the OLD gate does not class it as author-encoding.

### 3.3 The runner — exercises the REAL classifier + REAL extractor (floor-manager acceptance #1)

`run-author-gate-tests.sh` MUST source the lib and use the **actual** functions; NO reimplementation:

1. `source substrate/hooks/_hooklib.sh` → brings in BOTH `classify_author_file` AND `extract_author_fields`.
   (Because both now live in the lib — C4 relocation — the runner needs no source-guard on the gate at all.)
2. Read `is_principal`'s allow-list semantics by sourcing the canonical Denson token set
   (`denson` / `densonsmith2@gmail.com` / `denson smith`) and replicating ONLY the tiny `is_principal`
   compare (it is 12 lines, pure, and the gate reads its tokens from an install-written file the runner
   can point at a fixed test allow-list). Document in the runner that this mirrors the gate's `is_principal`.
3. For each fixture, read a manifest 3-tuple `(intended_path, expectation, fixture_file)` and:
   - **mode + membership in ONE call:** `_mode="$(classify_author_file "$intended_path")"; _rc=$?`. Assert
     `_rc`/`_mode` matches the fixture's expected class (e.g. `tp6-license-md` → rc 0, mode `cfg`;
     `fp1` → rc 0, mode `md`; the negative `notes.txt` → rc 1). **This single assertion is what catches r1:**
     if a future edit lets `LICENSE.md` fall to `md`, `classify_author_file LICENSE.md` returns `md` and
     `tp6` fails loud.
   - run `extract_author_fields "$_mode" < "$fixture_file"`, capture `pairs`,
   - run each emitted value through the `is_principal` mirror → compute ALLOW vs BLOCK,
   - compare to the expectation; print `PASS`/`FAIL`; exit non-zero if any FAIL.
4. Print a summary `N passed / M failed`; exit 0 only when ALL pass.

### 3.4 Relocation note (C4) — supersedes rev1 §3.4

Rev1 proposed relocating `is_author_encoding_file`. Rev2 relocates the UNIFIED `classify_author_file`
(membership + mode) instead — strictly stronger, since it also closes r1. The gate no longer defines any
classifier inline. ARGUS ruled RELOCATE correct (vs the rejected source-guard). VERA assertions (C4):
(a) `diff` the gate deny-set across the FULL corpus before/after = byte-identical;
(b) `grep -c 'classify_author_file()' substrate/hooks/pretooluse-author-field-audit.sh` = 0 (no inline def);
`grep -c 'classify_author_file()' substrate/hooks/_hooklib.sh` = 1 (defined exactly once);
`grep -c 'is_author_encoding_file' substrate/hooks/` = 0 (the OLD name is fully removed, no dangling caller).

### 3.5 The FULL fixture list (content sketch — ADA writes the literal files)

**FALSE-POSITIVE (must now PASS — `md` mode emits nothing):**
- `fp1-seat-attribution.md.fixture` — intended `docs/x.md`; body (no frontmatter):
  `**Authored by:** user-tier POLYBIUS (chief-of-staff) + the PRINCIPAL (Denson Smith).`
- `fp2-verdict-audit.md.fixture` — intended `agents/verdicts/x.md`; body:
  `expected: html author = Denson Smith; no other person in any author field`
- `fp3-directive-coauthor.md.fixture` — intended `substrate/arcs/x.md`; body: `Author=PRINCIPAL` +
  `Co-Authored-By: CAPTAIN_ADA_the-stoa <captain-ada@the-stoa.local>`
- `fp4-section28-docs.md.fixture` — intended `substrate/x.md`; body: `` By `CAPTAIN_<MNEMONIC>_<slug>` `` +
  `Owner: the workspace's .claude/skills/`

**TRUE-POSITIVE (must still BLOCK — extractor emits a non-Denson value; FICTIONAL name "Fenwick Galsworthy"):**
- `tp1-package.json.fixture` — intended `package.json`, `{"name":"x","author":"Fenwick Galsworthy"}`
  → mode `cfg` → BLOCK.
- `tp2-skill-frontmatter.md.fixture` — intended `skills/x/SKILL.md`, frontmatter
  `---\nname: x\nauthor: Fenwick Galsworthy\n---\n# body` → mode `md` → BLOCK (frontmatter still caught).
- `tp3-license.fixture` — intended `LICENSE`, `Copyright (c) 2026 Fenwick Galsworthy` → mode `cfg` → BLOCK.
- `tp4-notice.fixture` — intended `NOTICE`, `Author: Fenwick Galsworthy` → mode `cfg` → BLOCK.
- `tp5-citation.cff.fixture` — intended `CITATION.cff`,
  `cff-version: 1.2.0\nauthors:\n  - family-names: Galsworthy\n    given-names: Fenwick` → mode `cfg` → BLOCK.
- **`tp6-license-md.fixture` — NEW (C2 / r7 / closes r1). intended `LICENSE.md`**, BODY line (NO frontmatter):
  `Copyright: Fenwick Galsworthy` (and a second variant line `Author: Fenwick Galsworthy` may be added to
  the same fixture body). Expected: `classify_author_file LICENSE.md` → rc 0, mode **`cfg`**; cfg whole-blob
  scan emits `(copyright, Fenwick Galsworthy)` → `is_principal` false → **BLOCK**. *This is the fixture that
  goes RED if the r1 hole reopens (a `LICENSE.md` routed to `md` would slice only frontmatter, find no
  frontmatter, emit nothing, and ALLOW — failing the BLOCK expectation loudly.)*
- **`tp7-claude-plugin-doc.md.fixture` — NEW (C2 / r7 / closes r1). intended
  `.claude-plugin/docs/overview.md`**, BODY line (no frontmatter): `Author: Fenwick Galsworthy`. Expected:
  `classify_author_file` matches the `*.claude-plugin/*` arm → rc 0, mode **`cfg`**; cfg scan emits
  `(author, Fenwick Galsworthy)` → **BLOCK**.

**CONTROL (must PASS — happy structured path intact):**
- `ctl1-package-denson.json.fixture` — intended `package.json`, `{"author":"Denson Smith"}` → ALLOW.
- `ctl2-skill-frontmatter-denson.md.fixture` — intended `skills/y/SKILL.md`, frontmatter
  `author: Denson Smith` → mode `md` → ALLOW (frontmatter mode still ALLOWS the right name).
- **`ctl3-license-md-denson.fixture` — NEW. intended `LICENSE.md`**, body `Copyright: Denson Smith`
  → mode `cfg` → ALLOW (proves the LICENSE.md cfg-routing does not OVER-block a legitimate copyright).

**NEGATIVE path-class (proves the matcher still excludes non-author files):**
- manifest entry `notes.txt → out-of-class` asserting `classify_author_file "notes.txt"` returns non-zero
  (and prints nothing).
- **NEW (carve-out guard):** manifest entry `NOTICE.md → in-class, mode md` asserting
  `classify_author_file "NOTICE.md"` → rc 0, mode **`md`** (NOT `cfg`) — proves rev2 did NOT over-correct
  the collision set; `NOTICE.md` stays a prose-md file, its body author line is the acceptable Q-B residual.

> **Fictional-name choice (stated):** true-positive fixtures use the invented name **"Fenwick Galsworthy"**
> — NOT a real public figure. The corpus README documents this is FICTIONAL TEST INPUT, not an authorship
> claim on the-stoa.

### 3.6 Committability of THIS design doc + READMEs through the OLD gate (unchanged; ARGUS r6 sound)

This doc + the §3.7 README/header edits are `.md` committed THROUGH the OLD gate (the build-session reality).
The only PERSON named is **Denson Smith**; "Fenwick Galsworthy" appears only as quoted fixture-content. Wrong-
name examples are wrapped in fenced/backtick spans or `<…>` placeholders so the OLD whole-blob `*.md` scan
does not resolve a non-Denson value. **Self-test P10:** before ADA commits, a dry commit of this doc + READMEs
through the OLD gate must be ALLOWED; if denied, ADA re-wraps the offending quoted line (OLD `emit` skips a
value starting `<`) and re-probes.

---

## §3.7 — README / gate-header doc-update plan (C3 — document the Q-B delegation explicitly)

**`substrate/hooks/README.md` — add §7 "The `.md` frontmatter-only narrowing (Arc 65 / stoa--z2b)":**
- **WHAT it covers now:** structured author fields in config files (unchanged) — INCLUDING `LICENSE.md` and
  `*.claude-plugin/*.md` docs, which are config-class and keep the whole-file scan — PLUS `.md` YAML
  **frontmatter** `author:`/etc. lines in prose markdown.
- **WHAT it deliberately no longer matches (C3 — the explicit delegation):** author-like words in a PROSE
  `.md` **body** (verdict AUDIT lines, §28 docs, directive seat-attribution `**Authored by:**`,
  security/ownership discussion). **WHY:** those are the structural site of authorship-DISCUSSION, not
  authorship-CLAIMS; matching them was the z2b bug; there is no mechanical test that admits a real body
  `Author:` while rejecting the discussion prose. **WHERE the residual goes:** the prose discipline (global
  CLAUDE.md authorship rule) + the pre-commit/pre-push manual audit checklist + NOMOS/human review. State
  plainly: the gate is a backstop, not the whole defense; a body `Author:` line in a prose `.md` is OUT of
  mechanical scope by design.
- **Collision carve-out, stated:** `LICENSE.md` and `*.claude-plugin/*.md` are NOT prose-md — they are
  config-class and keep whole-file coverage. `NOTICE.md` and other `<config-basename>.md` files ARE prose-md
  (their body author line is the delegated residual). No body badge-line convention is added (ARGUS ruled).
- A one-line note that the corpus at `substrate/hooks/tests/` is the regression guard (source-only, no deploy).
- Update §4's table row for `pretooluse-author-field-audit.sh`: "...staged author-like field (config files
  incl. LICENSE.md / `*.claude-plugin/*.md` whole-file; prose `.md` frontmatter only) names someone other
  than the PRINCIPAL".

**Source-header comments** in `pretooluse-author-field-audit.sh` (caller) + `_hooklib.sh`
(`classify_author_file` + `extract_author_fields`): a 3-4 line block stating the unified classify→mode
contract, the config-class-wins-over-`*.md` rule (naming LICENSE.md / `*.claude-plugin/*.md`), and that cfg
extraction is byte-identical to pre-Arc-65. (The `classify_author_file` header in Change A already carries this.)

**`.claude/hooks/README.md`** gets the byte-identical update (deployed mirror).

**Committability:** README prose names only Denson + seats; the WHY paragraph quotes false-positive prose as
EXAMPLES inside backtick/fenced spans; confirm via P10 the OLD gate ALLOWS the README commit.

---

## §4 — Verification probes (VERA re-executes verbatim; both directions)

All paths repo-relative to the arc-65-build worktree. P1–P3 are the corpus; P4–P7 live re-probes; P8 deploy;
P9 mirror; P10 committability; P11 the C4 single-definition assertions.

**P1 (corpus, false-positive — must PASS):** `bash substrate/hooks/tests/run-author-gate-tests.sh` → every
`fp/` fixture reports `PASS` (md mode emits nothing ⇒ ALLOW). Runner exits 0.

**P2 (corpus, true-positive — must BLOCK) — THREAT-ANCHORED, see §5:** the runner → every `tp/` fixture
reports `PASS` meaning the gate computed **BLOCK**, across ALL classes: package.json, SKILL.md frontmatter,
LICENSE, NOTICE, CITATION.cff, **`LICENSE.md` (tp6), and `*.claude-plugin/*.md` (tp7)**. P2 additionally
asserts `classify_author_file` returns mode **`cfg`** for tp6 and tp7 (the r1 carve-out). Probe id **P2** is
the executed probe the verdict's threat-coverage line cites (`defeats_via_probe: P2`).

**P3 (corpus, control + negative-path + carve-out — must PASS):** the runner → `ctl/` fixtures ALLOW
(incl. **ctl3 LICENSE.md w/ Denson copyright → cfg → ALLOW**); `notes.txt → out-of-class`
(`classify_author_file` rc 1); **`NOTICE.md → in-class mode md`** (carve-out guard: NOT over-corrected to cfg).

**P4 (live re-probe, false-positive — real commit ALLOWED; throwaway):** in a scratch repo at the FIXED
literal path `/tmp/arc65-gate-probe` with the NARROWED deployed hook armed via a throwaway `settings.json`:
stage a prose `.md` with the `**Authored by:**` line + a verdict AUDIT prose line → `git commit` ALLOWED
(exit 0, no deny JSON). Teardown: `rm -rf /tmp/arc65-gate-probe` (fixed literal path, op-disc §8.6).

**P5 (live re-probe, true-positive — real commit DENIED):** same scratch repo: stage `package.json` with
`{"author":"Fenwick Galsworthy"}` → `git commit` DENIED (deny JSON: field `author`, file `package.json`).

**P6 (live re-probe, frontmatter + collision true-positive — real commit DENIED):** same scratch repo, THREE
commits each DENIED: (a) `skills/z/SKILL.md` frontmatter `author: Fenwick Galsworthy`; (b) **`LICENSE.md`
with a BODY `Copyright: Fenwick Galsworthy`** (the r1 live form — DENIED proves LICENSE.md keeps cfg
coverage); (c) **`.claude-plugin/docs/x.md` with a BODY `Author: Fenwick Galsworthy`** (DENIED proves the
plugin-doc class keeps cfg coverage). Proves the narrowing did NOT blanket-exempt `.md`.

**P7 (FAIL-OPEN preserved):** feed the gate an event with `python3` unavailable (PATH without python3) or
malformed event JSON → the gate ALLOWS (exit 0, no deny). Plus assert `classify_author_file` on a missing/
empty path does not hard-error the gate (default-skip, fail-open).

**P8 (deploy clean + tests not swept):** `bash substrate/install.sh --target user --dry-run` lists the deploy
of the narrowed `pretooluse-author-field-audit.sh` + `_hooklib.sh` and lists NO `tests/` path under
`deploy hook:`. (Dry-run writes nothing.)

**P9 (source ⇄ deployed mirror byte-identical):** `diff substrate/hooks/_hooklib.sh
.claude/hooks/_hooklib.sh` → empty; same for `pretooluse-author-field-audit.sh`. Both exit 0.

**P10 (committability self-test — design doc + READMEs pass the OLD gate):** with the OLD main-tree hook
armed, `git add` this doc + the updated READMEs and attempt a commit → ALLOWED. If denied, re-wrap the
offending quoted example (`<…>` / fenced span) and re-probe until ALLOWED.

**P11 (C4 single-definition + deny-set identity):**
- `grep -c 'classify_author_file()' substrate/hooks/_hooklib.sh` = 1; `... pretooluse-author-field-audit.sh` = 0.
- `grep -rc 'is_author_encoding_file' substrate/hooks/` = 0 (OLD name fully removed; no dangling caller).
- deny-set byte-identical across the FULL corpus: run the runner against EVERY fixture before vs after the
  relocation and assert the set of (file, field, value) deny tuples is unchanged for all config-class
  fixtures (the cfg path moved house but did not change behavior). This is the C4 deny-set assertion.

---

## §5 — A2 / §35 threat-alignment (threat→mitigation map + threat-anchored probe) — C5

**Named threat M1 (directive / floor-manager):** "a real STRUCTURED author field naming a non-Denson PERSON
slips past the narrowed gate." This is the reputational/legal regression the gate exists to prevent
(regressed TWICE). The arc is a SECURITY gate change. ARGUS r-verdict: M1 had NO passing threat-coverage
binding until r1 (caller carve-out) + r7 (LICENSE.md / `*.claude-plugin` fixtures) close. Rev2 closes both;
the how-defeated claim below is now TRUE for the collision classes.

**Threat→mitigation map (Approach §2):**

> **M1 (a real structured author field naming a non-Denson person slips the narrowed gate)**
> → **attack-path:** the narrowing widens `.md` scope so far that a real structured author field is no longer
> extracted and reaches commit un-audited — specifically (i) a `.md` YAML-frontmatter `author: <non-Denson>`
> in a SKILL/plugin, (ii) a config-file author (`package.json`/`LICENSE`/`NOTICE`/`CITATION.cff`), OR
> (iii) **a `.md`-suffixed CONFIG-class file — `LICENSE.md` or `*.claude-plugin/*.md` — whose body
> `Copyright:`/`Author: <non-Denson>` line the OLD cfg gate BLOCKED** (the rev1 hole).
> → **how-defeated:** mode is now decided by `classify_author_file`, the SAME function that decides
> author-encoding membership, using the SAME case arms in the SAME priority order. Every config-class arm —
> including the `LICENSE.*`/`LICENSE.md` basename arm and the `*.claude-plugin/*` path arm — returns mode
> **`cfg`** (the OLD whole-file scan, byte-identical) and is tested BEFORE the bare `*.md` arm is reached, so
> `LICENSE.md` and `*.claude-plugin/*.md` are scanned whole-file, NOT through the narrowed frontmatter window.
> Only a PROSE `.md` (membership via the bare `*.md` arm alone) gets the narrowed `md` window, and even then
> the narrowing only restricts the SCAN WINDOW — it never relaxes the VALUE check (`is_principal`) and never
> touches the config path. Frontmatter `author:` STAYS extracted. The only thing removed from coverage is a
> PROSE `.md` **body** line (authorship-DISCUSSION, not a CLAIM — Q-B, explicitly delegated). Because mode and
> membership derive from one source, the rev1 caller-vs-classifier disagreement that opened the hole cannot
> recur.

**Threat-anchored probe (asserts BOTH halves of §6.13):**
- **(a) attack-blocked:** **P2** drives the named attack path across EVERY covered class — true-positive
  fixtures for `package.json`, SKILL.md frontmatter, `LICENSE`, `NOTICE`, `CITATION.cff`, **`LICENSE.md`
  (tp6), and `*.claude-plugin/*.md` (tp7)** — each naming fictional non-Denson "Fenwick Galsworthy", and
  asserts the gate computes **BLOCK**; P2 also asserts `classify_author_file` returns `cfg` for tp6/tp7
  (the exact carve-out that defeats the rev1 attack path). P6 (b)+(c) drive the live commit form for the two
  collision classes (real commit DENIED). This is the verdict's `defeats_via_probe: P2`.
- **(b) legit-unaffected:** **P1** (z2b body-prose instances now ALLOW) + **P3 control** (config / frontmatter
  / **LICENSE.md** author = Denson Smith still ALLOWS; `NOTICE.md` stays md-mode prose) — the mitigation did
  not defeat the threat by breaking the legitimate path or over-correcting the carve-out.

A probe that asserted only "the extractor emits nothing on body prose" would NOT be threat-anchored; P2
exercises the attack path (a real wrong-person field) across every covered class INCLUDING the two collision
classes r1 named — which is what falsifies "the narrowing drifted to the wrong surface and let a real claim
through."

---

## §6 — Self-assessed weak points

1. **Q-B residual (ACCEPTABLE, ARGUS-ruled): a body `Author: <wrong person>` line in a PROSE `.md`
   (e.g. NOTICE.md, a README body) is no longer mechanically caught.** Deliberate, defended (§2.1 Q-B),
   documented in the README (C3). *Why this shape anyway:* no mechanical predicate separates a real body
   `Author: Jane Roe` from the z2b discussion prose; any rule re-covering body lines re-opens z2b. ARGUS
   ruled this acceptable for a backstop gate given the collision classes (LICENSE.md / `*.claude-plugin`)
   are carved back to cfg.

2. **NEW in rev2 — the collision carve-out is encoded as case-arm ORDER, not an explicit "is-config" flag.**
   `classify_author_file` relies on the config arms being TEXTUALLY ABOVE the bare `*.md` arm; a future edit
   that reorders the arms (or inserts a `*.md` arm above a config arm) would silently re-open r1. *Why this
   shape anyway:* it is the minimal, byte-deny-identical relocation of the OLD arms (the OLD function already
   depended on the same `case`-arm order for membership), and the order-dependence is now GUARDED by tp6/tp7
   (which go RED if any reorder routes LICENSE.md / plugin-docs to `md`) + the P3 `NOTICE.md → md` carve-out
   guard (which goes RED if the order over-corrects). The regression is mechanically caught, not just
   commented. ARGUS should confirm the corpus guard is sufficient vs an explicit per-arm assertion.

3. **`classify_author_file` relocation into `_hooklib.sh` is a refactor of a live security gate.** Stronger
   than rev1's (it relocates the UNIFIED classifier, also closing r1). Behavior-preserving (same arms, same
   order). *Why this shape anyway:* ARGUS ruled RELOCATE correct over the source-guard (a pure no-I/O function
   move vs a new early-return fail-surface); VERA's C4 assertions (P11: defined once, OLD name fully removed,
   deny-set byte-identical across the full corpus) bound the regression risk.

4. **Frontmatter detection is regex-based, not a YAML parser** (leading `---`…`---` only). ARGUS r4 CONFIRMED
   the substrate has NO TOML-delimiter / non-leading frontmatter convention, so this misses no EXISTING
   frontmatter; the under-enforcement is theoretical and the fail-direction (a `.md` matching the bare `*.md`
   arm whose frontmatter uses an exotic delimiter) is under-enforcement on a shape the repo does not use,
   mitigated by the prose discipline + audit layers.

5. **Committability self-test (P10) depends on the OLD gate's value-resolution for quoted examples** in this
   doc / README. A process friction (ADA re-wraps with `<…>` / fenced spans), not a correctness risk —
   flagged so ADA expects it.

---

## §7 — Out of scope

- Changing the seat-attribution convention or adding path-exemptions beyond the collision carve-out.
- The stashed Arc-61 directive-DoD fix (`git stash@{0}` on main) — popped as a §18 follow-up AFTER this lands.
- `stoa--9s6` / `ruu` / `p41.3-5` / `luo` — separate tickets.
- A full YAML/TOML frontmatter parser, or `+++` TOML frontmatter support (weak point 4) — backstop gate.
- An explicit `is-config` boolean flag refactor of the case arms (weak point 2) — the order-dependence is
  corpus-guarded; a flag refactor is a larger change than this security fix warrants. Reconsider only if the
  arms grow.
- Arming the gate / `--enable-hooks` changes — deploy stays INERT + default-OFF (HARD SAFETY CONSTRAINT).
