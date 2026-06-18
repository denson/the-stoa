# Arc 65 design-rev1 — Narrow the authorship-attribution gate's `.md` matcher (stoa--z2b)

**Authored by:** `CAPTAIN_DAEDALUS_the-stoa` (architect) + the PRINCIPAL (Denson Smith).
**Ticket:** stoa--z2b (P1, BUG, SECURITY-sensitive gate).
**Builds on:** the-stoa main `20267e4`; directive `beadwork:attachments/stoa--z2b/arc-65-build-directive.md` (NOMOS CONFORMANT).
**Fix surface:** `substrate/hooks/_hooklib.sh` (`extract_author_fields`), `substrate/hooks/pretooluse-author-field-audit.sh` (sub-check 2 caller) + the byte-identical deployed mirror `.claude/hooks/`.

---

## §1 — Problem restatement

The PreToolUse authorship gate (`pretooluse-author-field-audit.sh` sub-check 2) treats **every `*.md`
file** as an author-encoding file (`is_author_encoding_file`, line 122) and runs the
**MULTILINE, anywhere-in-blob** regex (`extract_author_fields`, `_hooklib.sh:94-99`) over its whole
text. That regex matches any of 12 author-like FIELD words followed by `:` or `=` ANYWHERE — so it
fires on `.md` **body prose** that merely discusses authorship, not on a structured author field.
Reproduced live this turn:

- FP1 — `**Authored by:** user-tier POLYBIUS (chief-of-staff) + the PRINCIPAL (Denson Smith).`
  → matches field `by`, value `** user-tier POLYBIUS ... + the PRINCIPAL (Denson Smith).` → `is_principal` rejects → **DENY**.
- FP2 — `expected: html author = Denson Smith; no other person in any author field`
  → matches field `author`, value `Denson Smith; no other person in any author field` → **DENY**.
- N+1 (Arc 64) — CATO verdict-body authorship-AUDIT prose blocks an in-tree verdict commit.

None is a real violation: the only PERSON named is Denson Smith (allow-listed); "POLYBIUS" is a SEAT.

**The fix (both directions load-bearing — a one-direction pass is a FAIL):**
1. `.md` **body prose** discussing authorship must stop tripping the gate (the z2b instances commit clean).
2. A **real structured author field naming a non-Denson PERSON** must still BLOCK — the regression
   the gate exists to prevent (a reputational/legal footgun that has regressed TWICE). This means:
   structured config files (`package.json`, `pyproject.toml`, `Cargo.toml`, `LICENSE`/`NOTICE`,
   `CITATION.cff`, plugin/marketplace manifests) **and** `.md` **YAML-frontmatter** `author:` lines
   (SKILL.md frontmatter is the global checklist's named target) must keep blocking.

**Imported assumption (named):** the directive + floor-manager treat "structured author position in a
`.md`" as **the YAML frontmatter block only**. This design adopts that scope for `.md` and decides
Q-B (body `Author:` lines) explicitly against it below — it is NOT a silent drop.

---

## §2 — Approach

### 2.1 Strategy (rules on Q-A / Q-B / Q-C)

**Q-A — RULED: frontmatter-only for `.md`; OLD full-blob extraction UNCHANGED for every non-`.md`
author-encoding file.** Chosen over (i) body-aware code-fence/backtick/bold skipping and (ii) a
person-name value heuristic. Rationale:
- The frontmatter block is the ONLY structured-author position in a `.md` (SKILL.md `author:` in the
  leading `---`…`---`). Everything else in a `.md` is prose by construction.
- It kills **all** z2b instances in one move (they are all body prose; none is in frontmatter) — verified live this turn.
- It is the LEAST brittle of the three: a code-fence/backtick/bold skipper is a parser that will rot
  against new prose shapes (the gate has already been surprised twice — FP1 bold-with-colon, FP2
  mid-prose `=`); a person-name heuristic cannot reliably tell "Jane Roe" from "POLYBIUS (chief-of-staff)".
- Config-file extraction (the highest-value true-positives) is **untouched** — frontmatter narrowing
  applies ONLY when the file is a `.md`, dispatched by the gate caller, so JSON/TOML/`LICENSE`/`CITATION.cff`
  keep the exact OLD code path byte-for-byte.

**Q-B — RULED: do NOT keep mechanical coverage of a body `Author: <person>` line in a `.md`.** A
non-frontmatter `Author: X` line in a README body is **out of mechanical gate scope** under this
design. This is an EXPLICIT, defended decision, not a silent drop:
- The body of a `.md` is exactly where authorship-discussion prose lives (verdict AUDIT lines, §28
  discipline docs, directive seat-attribution, security/ownership discussion). There is no mechanical
  test that admits a real `Author: Jane Roe` README line while rejecting `author = Denson Smith; no
  other person in any author field` — they are the same surface. Keeping body coverage re-opens z2b.
- **Residual-risk tradeoff (stated):** a README that puts a real wrong-person author in a **body**
  line (not frontmatter, not a structured author-encoding file) is no longer caught by THIS gate. It
  remains covered by the THREE other layers the gate was always only a backstop to: the prose
  discipline (global CLAUDE.md authorship rule), the pre-commit/pre-push **manual audit checklist**,
  and **NOMOS + human review**. The README author convention is overwhelmingly frontmatter (`author:`)
  or a badge line in the structured manifest, both of which stay covered. The residual surface is a
  body free-text `Author:` line in a `.md` — narrow, and the most-likely real-world author surfaces
  (`package.json`, SKILL.md frontmatter, `LICENSE`, `CITATION.cff`) are all still mechanically gated.
- This is the §35.5 honest-claim posture: the gate verifies **named-class coverage**, not
  authorship-correctness-in-general; body-prose author detection was never sound (it is the bug).

**Q-C — DECLINED (value-shape heuristic in `is_principal`'s caller).** Not adding path/seat/clause
benign-value recognition. Rationale:
- It is the brittle approach Q-A rejected, relocated to the value side. A heuristic that benign-lists
  "looks like a path / `CAPTAIN_*` / multi-clause prose" is exactly the kind of fuzzy matcher that
  **softens the config-file true-positive path** — the one path the directive says must stay
  hardest. A real `package.json` `"author": "Some Studio LLC"` (a vendor, multi-word, no person
  shape) must still BLOCK; a value-shape heuristic that benign-lists "multi-clause / non-person-name"
  values risks letting a real corporate/other-name author through.
- The structural narrowing (Q-A) removes the z2b false-positives at the SOURCE (they never reach
  `is_principal`), so the belt-and-suspenders has nothing left to catch that is worth the risk it adds.
- **Smaller, safe sub-piece adopted instead:** the frontmatter regex already drops the FP1 `**` bold
  prefix problem by construction (frontmatter has no `**…by:**`). No value-side change needed.

### 2.2 The hand-off contract (caller ⇄ extractor)

The gate caller (`pretooluse-author-field-audit.sh`) ALREADY knows the file path `$f` per staged file.
The narrowing is a **path-class dispatch at the caller**, passing a mode flag to the extractor:

- caller computes `is_md` from `$f` (basename ends `.md`),
- caller invokes `extract_author_fields md` for `.md` files and `extract_author_fields` (or
  `extract_author_fields cfg`) for everything else,
- the extractor, in `md` mode, scans ONLY the leading YAML frontmatter block; in default/`cfg` mode it
  runs the OLD regex over the whole blob, byte-identical behavior.

This keeps the path knowledge at the caller (where it lives) and makes the extractor's two modes
explicit and testable in isolation (the runner feeds content + a mode, mirroring the caller's dispatch).

---

## §2.3 — The exact change (concrete code, not a sketch)

### Change A — `substrate/hooks/_hooklib.sh` `extract_author_fields` (mode-aware)

Replace the function body so it takes an optional first arg `$1` = mode (`md` ⇒ frontmatter-only;
anything else ⇒ OLD full-blob behavior, byte-identical). The **only** new logic is the frontmatter
slice + a frontmatter-specific regex; the `clean_one`/`emit`/array-flatten machinery is **unchanged**
and reused by both modes.

```bash
extract_author_fields() {
  MODE="${1:-cfg}" python3 -c '
import sys, re, os
text = sys.stdin.read()
mode = os.environ.get("MODE", "cfg")
FIELDS = ["authors","author","owner","creator","created_by","maintainers","maintainer","by","copyright","holder","vendor","publisher"]
key = "|".join(FIELDS)

# --- .md NARROWING (Arc 65 / stoa--z2b) -------------------------------------
# For markdown files, author-like fields are only STRUCTURED in the leading
# YAML frontmatter block (--- ... ---). Body prose that merely DISCUSSES
# authorship ("**Authored by:** <seat> + PRINCIPAL", "author = Denson Smith;
# no other person...", a verdict AUDIT line) is NOT a structured author field
# and must NOT trip the gate. So in md mode we (1) slice out the frontmatter
# block (empty if absent), and (2) match author keys only at YAML line-start
# with a ":" separator. Non-md (config) files keep the OLD whole-blob scan.
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
    # OLD behavior (config files: JSON / YAML / TOML / LICENSE / CITATION.cff).
    # UNCHANGED — byte-identical to the pre-Arc-65 regex.
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

**Notes on the change (each load-bearing):**
- The extractor now takes its mode from the `MODE` **env var** (`MODE="${1:-cfg}" python3 -c '...'`),
  NOT a `sys.argv` slot — because `json_field` in the same lib already passes a path via `argv[1]`, but
  `extract_author_fields` takes none today; using env avoids any argv collision and keeps the
  single-quoted heredoc literal-safe (no shell interpolation of the program). Default `cfg` ⇒
  unchanged behavior when called with no arg (defensive: any caller that forgets the mode gets the
  SAFE, broadest scan, not the narrow one — fail toward MORE enforcement, never less).
- `﻿?` tolerates a leading UTF-8 BOM (Windows forge); `\r?\n` tolerates CRLF on both fence lines.
- `md` mode uses **`:` only** (YAML), not `[:=]` — TOML `=` cannot appear in a `.md` frontmatter key.
- `^[ \t]*` anchors keys to line-start (indented YAML keys still match) — body-prose `author = ...`
  mid-line cannot match because it is OUTSIDE the sliced frontmatter text entirely.
- If a `.md` has **no** frontmatter, `text` becomes `""` ⇒ zero matches ⇒ the body-prose z2b instances
  emit nothing. Verified live this turn.

### Change B — `substrate/hooks/pretooluse-author-field-audit.sh` sub-check 2 caller

`is_author_encoding_file` is **unchanged** (`.md` still routes IN — we want frontmatter scanned). The
ONLY caller change is to dispatch the mode by basename:

```bash
while IFS= read -r f; do
  [ -n "$f" ] || continue
  is_author_encoding_file "$f" || continue
  blob="$(git -C "$CWD" show ":${f}" 2>/dev/null)" || continue
  [ -n "$blob" ] || continue
  # Arc 65 (stoa--z2b): .md files are scanned in FRONTMATTER-ONLY mode so body
  # prose discussing authorship does not false-positive; config files keep the
  # full-blob scan. See _hooklib.sh extract_author_fields + .claude/hooks/README.md §7.
  case "$f" in
    *.md) _mode="md" ;;
    *)    _mode="cfg" ;;
  esac
  pairs="$(printf '%s' "$blob" | extract_author_fields "$_mode")" || continue
  [ -n "$pairs" ] || continue
  ...   # is_principal loop + emit_deny — UNCHANGED
done <<EOF
$STAGED
EOF
```

**No change** to sub-check 1 (git config author identity), `is_principal`, `is_author_encoding_file`,
the allow-list logic, FAIL-OPEN, or `emit_deny`.

### Change C — the deployed mirror

`.claude/hooks/_hooklib.sh` and `.claude/hooks/pretooluse-author-field-audit.sh` get the **identical**
edits (the-stoa is the forge; source + deployed land together, byte-identical — VERA asserts
`diff substrate/hooks/X .claude/hooks/X` is empty for both files).

---

## §3 — Test-corpus architecture

### 3.1 Where it lives + the deploy decision

**Source-only at `substrate/hooks/tests/`. It does NOT deploy.** Confirmed against `install.sh`: the
hooks deploy loop globs `${SRC_HOOKS_DIR}/*.sh` (non-recursive — a `tests/` SUBDIR is not matched) and
copies `README.md` by explicit basename only (install.sh:1373 + 1398). A `tests/` subdir is therefore
invisible to the deploy. This is the desired posture: tests are forge-side verification artifacts, not
runtime substrate. (VERA asserts a dry-run install does NOT list any `tests/` path under
`deploy hook:`.)

```
substrate/hooks/tests/
  README.md                 # corpus rationale + the fixture-naming-is-test-data note (for CATO/NOMOS)
  run-author-gate-tests.sh  # the runner
  fixtures/
    fp/                      # FALSE-POSITIVE fixtures — must now PASS (extractor emits nothing)
      fp1-seat-attribution.md.fixture
      fp2-verdict-audit.md.fixture
      fp3-directive-coauthor.md.fixture
      fp4-section28-docs.md.fixture
    tp/                      # TRUE-POSITIVE fixtures — must still BLOCK (extractor emits a non-Denson value)
      tp1-package.json.fixture
      tp2-skill-frontmatter.md.fixture
      tp3-license.fixture
      tp4-notice.fixture
      tp5-citation.cff.fixture
    control/                 # CONTROL — config file w/ Denson author must PASS (happy structured path intact)
      ctl1-package-denson.json.fixture
      ctl2-skill-frontmatter-denson.md.fixture
```

### 3.2 The fixture storage scheme (committability constraint — load-bearing)

The live PreToolUse gate in the orchestrator's session resolves to the **MAIN-tree (OLD, un-narrowed)**
hook until merge. The OLD gate DENIES a commit if any staged file whose **basename** matches
`is_author_encoding_file` (`package.json`, `*.md`, `LICENSE`, `CITATION.cff`, ...) contains an
author-like field naming a non-Denson value. So the TRUE-POSITIVE fixtures CANNOT be stored under a
triggering basename — committing them would trip the OLD gate.

**Scheme:** every fixture file carries a **`.fixture` suffix** (e.g. `tp1-package.json.fixture`,
`fp1-seat-attribution.md.fixture`). `.fixture` is NOT a triggering basename — `is_author_encoding_file`
matches `*.md` and the exact config basenames, and `tp1-package.json.fixture` ends in `.fixture`, not
`.md`/`.json`-as-basename (the match is on `basename "$p"` against the literal list / `*.md` suffix;
`...package.json.fixture` ≠ basename `package.json` and does not end `.md`). The runner reconstructs the
**intended path** the matcher must SEE from a per-fixture manifest line, NOT from the on-disk name.

**Also required for committability of the FALSE-POSITIVE `.md` fixtures and this design doc:** the OLD
gate scans `*.md` whole-blob. A `.fixture` suffix moves the FP fixtures out of `*.md` scope too, so
their non-Denson-free prose (they only ever name Denson + seats) commits clean regardless — but the
`.fixture` suffix is the uniform, defensible scheme for the whole corpus. (The design doc itself + the
README updates are `.md` and MUST be authored to not trip the OLD gate — see §3.5 committability.)

> **Note on the OLD extractor's `<`-skip:** the OLD `emit()` skips a value whose first char is `<`
> (template placeholder). A `.fixture`-suffixed file is the primary defense; the `<…>`-placeholder
> escape is a SECONDARY note only and is NOT relied on for the true-positive fixtures (their whole
> point is a literal non-placeholder name).

### 3.3 The runner — exercises the REAL narrowed matcher (floor-manager acceptance #1)

`run-author-gate-tests.sh` MUST invoke the **actual** `extract_author_fields` from
`substrate/hooks/_hooklib.sh` (source it; do NOT reimplement the regex) AND the **actual**
`is_author_encoding_file` from `pretooluse-author-field-audit.sh`, feeding each fixture's INTENDED path
+ content. The on-disk `.fixture` name is irrelevant; what the matcher SEES is the intended path+content.

Contract:
1. `source` `substrate/hooks/_hooklib.sh` (brings in the real `extract_author_fields`).
2. Extract `is_author_encoding_file` for path-class testing. Two sound options — design picks (a):
   (a) `source` the gate script guarded so it does not run its main body when sourced (add a
   `[ "${AUTHOR_GATE_LIB_ONLY:-0}" = 1 ] && return 0` near the top of the gate after the function
   defs — a one-line, behavior-preserving hook-as-library guard; the runner sets `AUTHOR_GATE_LIB_ONLY=1`
   before sourcing). **DECISION:** define `is_author_encoding_file` ONCE in `_hooklib.sh` and have the
   gate source it from there, so the runner gets it for free from the lib it already sources — this is
   the cleaner refactor and removes the source-guard dance. (See §3.4.)
3. For each fixture, read a manifest 3-tuple `(intended_path, expectation, fixture_file)` and:
   - assert `is_author_encoding_file "$intended_path"` returns the EXPECTED class (every fixture's
     intended path is in-class; a NEGATIVE path-class case `notes.txt → out-of-class` is added to prove
     the matcher still excludes non-author files),
   - compute the mode the GATE would use (`*.md ⇒ md`, else `cfg`) — same `case` as the gate,
   - run `cat "$fixture_file" | extract_author_fields "$mode"` and capture `pairs`,
   - run each emitted value through the gate's `is_principal` (sourced/replicated allow-list of the
     Denson tokens) to compute ALLOW vs BLOCK exactly as the gate does,
   - compare to the expectation; print `PASS`/`FAIL` per fixture; exit non-zero if any FAIL.
4. The runner prints a summary `N passed / M failed` and exits 0 only when ALL pass.

> The runner computes ALLOW/BLOCK via the real `extract_author_fields` + the real `is_principal`
> semantics — i.e. it exercises the deployed gate's decision logic, not a parallel reimplementation.
> The allow-list it feeds `is_principal` is the canonical Denson token set
> (`denson` / `densonsmith2@gmail.com` / `denson smith`), matching `principal-identity`.

### 3.4 Small refactor (fix-now, in-scope): move `is_author_encoding_file` to `_hooklib.sh`

To let the runner reuse the REAL path matcher without a source-guard on the gate, `is_author_encoding_file`
moves from the gate into `_hooklib.sh` (alongside `extract_author_fields`); the gate calls it from the
sourced lib (behavior byte-identical — same `case` arms). This is a tidy, test-enabling relocation, not
a behavior change; VERA asserts the gate's deny set is unchanged for the corpus. (If ARGUS judges the
relocation out-of-scope for a security arc, the fallback is the `AUTHOR_GATE_LIB_ONLY` source-guard in
§3.3 option (a) — flagged as a weak point for ARGUS to rule.)

### 3.5 The FULL fixture list (content sketch — ADA writes the literal files)

**FALSE-POSITIVE (must now PASS — extractor emits nothing in `md` mode):**
- `fp1-seat-attribution.md.fixture` — a `.md` whose BODY (no frontmatter, or frontmatter with no
  author key) contains: `**Authored by:** user-tier POLYBIUS (chief-of-staff) + the PRINCIPAL (Denson Smith).`
- `fp2-verdict-audit.md.fixture` — body line: `expected: html author = Denson Smith; no other person in any author field`
- `fp3-directive-coauthor.md.fixture` — body lines: `Author=PRINCIPAL` and a requirement
  `Co-Authored-By: CAPTAIN_ADA_the-stoa <captain-ada@the-stoa.local>`
- `fp4-section28-docs.md.fixture` — body lines: `` By `CAPTAIN_<MNEMONIC>_<slug>` `` and `Owner: the workspace's .claude/skills/`

**TRUE-POSITIVE (must still BLOCK — extractor emits a non-Denson value; use a FICTIONAL name):**
- `tp1-package.json.fixture` — intended path `package.json`, content `{"name":"x","author":"Fenwick Galsworthy"}` → BLOCK.
- `tp2-skill-frontmatter.md.fixture` — intended path `skills/x/SKILL.md`, YAML frontmatter
  `---\nname: x\nauthor: Fenwick Galsworthy\n---\n# body` → BLOCK (frontmatter author still caught).
- `tp3-license.fixture` — intended path `LICENSE`, content `Copyright (c) 2026 Fenwick Galsworthy` → BLOCK
  (matched via `copyright` field, OLD `cfg` path).
- `tp4-notice.fixture` — intended path `NOTICE`, content `Author: Fenwick Galsworthy` → BLOCK.
- `tp5-citation.cff.fixture` — intended path `CITATION.cff`, content
  `cff-version: 1.2.0\nauthors:\n  - family-names: Galsworthy\n    given-names: Fenwick` → BLOCK
  (the `family-names:` line re-matches under the OLD `cfg` regex — verified live this turn).

**CONTROL (must PASS — happy structured path intact):**
- `ctl1-package-denson.json.fixture` — intended path `package.json`, content `{"author":"Denson Smith"}` → PASS.
- `ctl2-skill-frontmatter-denson.md.fixture` — intended path `skills/y/SKILL.md`, frontmatter
  `author: Denson Smith` → PASS (proves frontmatter mode still ALLOWS the right name, i.e. the
  narrowing did not blanket-allow `.md`).

**NEGATIVE path-class (proves the matcher still excludes non-author files):**
- a manifest entry `notes.txt → out-of-class` (no fixture body needed) asserting
  `is_author_encoding_file "notes.txt"` returns non-zero.

> **Fictional-name choice (stated):** true-positive fixtures use the invented name **"Fenwick
> Galsworthy"** — NOT a real public figure. Using a real name (e.g. the historical regression value)
> would re-introduce the exact footgun into committed test data and risk a downstream mis-flag. The
> corpus README documents that this name is FICTIONAL TEST INPUT, not an authorship claim on the-stoa.

### 3.6 The committability of THIS design doc + the README updates

This design doc and the §3.7 README/header edits are `.md` and get committed THROUGH the OLD gate.
They are authored to not trip it: the only PERSON named anywhere in them is **Denson Smith** (and the
fictional "Fenwick Galsworthy" appears only as quoted fixture-content, prefixed in prose so the OLD
whole-blob regex's value, if it matches a stray `author:` token, resolves to a value that is either a
placeholder or Denson). The `**Authored by:**` line at the top of THIS doc names a seat + the PRINCIPAL
(Denson) — the OLD gate matches `by` with value starting `\`CAPTAIN_DAEDALUS...` ; to be safe the line
is written so the value the OLD extractor sees is template/placeholder-skipped or resolves to Denson.
**Self-test required (probe in §4):** before ADA commits, VERA confirms a dry `git add` + commit of
this doc + the README through the OLD gate is ALLOWED — if the OLD gate denies it, ADA wraps the
offending line in a fenced placeholder so the value starts with `<` (OLD `emit` skips `<…>`).

---

## §3.7 — README / gate-header doc-update plan

**`substrate/hooks/README.md` — add §7 "The `.md` frontmatter-only narrowing (Arc 65 / stoa--z2b)":**
- WHAT it covers now: structured author fields in config files (unchanged) + `.md` YAML **frontmatter**
  `author:`/etc. lines.
- WHAT it deliberately no longer matches: author-like words in `.md` **body prose** (verdict AUDIT
  lines, §28 discipline docs, directive seat-attribution `**Authored by:**`, security/ownership
  discussion). WHY: those are the structural site of authorship-DISCUSSION, not authorship-CLAIMS;
  matching them was the z2b bug; there is no mechanical test that admits a real body `Author:` while
  rejecting the discussion prose, so body coverage is delegated to the prose discipline + manual audit
  + NOMOS/human review (the gate was always a backstop, not the whole defense).
- A one-line note that the corpus at `substrate/hooks/tests/` is the regression guard (source-only,
  does not deploy).
- Update §4's table row for `pretooluse-author-field-audit.sh` to read "...staged author-like field
  (config files whole-file; `.md` frontmatter only) names someone other than the PRINCIPAL".

**Source-header comment in `pretooluse-author-field-audit.sh`** (and the `extract_author_fields`
header in `_hooklib.sh`): a 3-4 line block stating the `.md` frontmatter-only mode, why (z2b body-prose
false-positives), and that config-file extraction is unchanged. (Authoring rule §2: self-contained, no
bare pointer — though these are source comments, not trigger payloads.)

**`.claude/hooks/README.md`** gets the byte-identical update (deployed mirror).

**Committability:** all README prose names only Denson + seats; the WHY paragraph quotes the
false-positive prose as EXAMPLES — write those quoted examples inside backtick spans / fenced blocks
and confirm via the §4 self-test that the OLD gate ALLOWS the README commit (wrap in `<…>` placeholder
if any quoted `author:`/`by:` example trips the OLD whole-blob scan).

---

## §4 — Verification probes (VERA re-executes verbatim; both directions)

All probe paths are repo-relative to the arc-65-build worktree. Probes P1–P3 are the corpus; P4–P6 are
live re-probes; P7 is FAIL-OPEN; P8/P9 are deploy + mirror.

**P1 (corpus, false-positive direction — must PASS):**
`bash substrate/hooks/tests/run-author-gate-tests.sh` → every `fp/` fixture reports `PASS`
(extractor emits nothing in `md` mode ⇒ gate ALLOWS). Runner exits 0.

**P2 (corpus, true-positive direction — must BLOCK) — THREAT-ANCHORED, see §5:**
the same runner → every `tp/` fixture reports `PASS` meaning the gate computed **BLOCK** (extractor
emitted a non-Denson value ⇒ `is_principal` false ⇒ deny). Covers each file class: package.json,
SKILL.md frontmatter, LICENSE, NOTICE, CITATION.cff. Probe id **P2** is the executed probe the
verdict's threat-coverage line cites (`defeats_via_probe: P2`).

**P3 (corpus, control + negative-path — must PASS):**
the same runner → `ctl/` fixtures report ALLOW (Denson author in config + frontmatter passes), and the
`notes.txt → out-of-class` entry asserts `is_author_encoding_file` returns non-zero.

**P4 (live re-probe, false-positive — real commit ALLOWED; throwaway, no main pollution):**
in a `git clone --no-local` scratch repo (or a throwaway branch in the worktree) with the **NARROWED**
deployed hook armed via a throwaway `settings.json`: stage a `.md` containing the Arc-61
`**Authored by:**` line + a verdict AUDIT prose line `expected: ... author = Denson Smith; no other
person in any author field` → `git commit` is **ALLOWED** (exit 0, no deny JSON). Throwaway is deleted
after.
Destructive-op note (op-disc §8.6): the scratch dir uses a FIXED literal path
`/tmp/arc65-gate-probe` (no `$VAR` in any `rm`), e.g. teardown `rm -rf /tmp/arc65-gate-probe`.

**P5 (live re-probe, true-positive — real commit DENIED):**
same scratch repo: stage `package.json` with `{"author":"Fenwick Galsworthy"}` → `git commit` is
**DENIED** (deny JSON naming field `author`, file `package.json`, value `Fenwick Galsworthy`).

**P6 (live re-probe, frontmatter true-positive — real commit DENIED):**
same scratch repo: stage `skills/z/SKILL.md` with frontmatter `author: Fenwick Galsworthy` →
`git commit` is **DENIED**. (Proves the narrowing did NOT blanket-exempt `.md`.)

**P7 (FAIL-OPEN preserved):**
feed the gate a hook event with `python3` made unavailable (or malformed event JSON) → the gate
**ALLOWS** (exit 0, no deny). Assert a deliberately-broken `extract_author_fields` (e.g. PATH without
python3) degrades to allow, never hard-blocks.

**P8 (deploy clean + tests not swept):**
`bash substrate/install.sh --target user --dry-run` lists the deploy of the narrowed
`pretooluse-author-field-audit.sh` + `_hooklib.sh` and does NOT list any `tests/` path under
`deploy hook:`. (Destructive-op note: dry-run writes nothing.)

**P9 (source ⇄ deployed mirror byte-identical):**
`diff substrate/hooks/_hooklib.sh .claude/hooks/_hooklib.sh` → empty; same for
`pretooluse-author-field-audit.sh`. Both exit 0.

**P10 (committability self-test — the design doc + README pass the OLD gate):**
with the **OLD** main-tree hook armed (the build-session reality), `git add` this design doc + the
updated READMEs and attempt a commit → **ALLOWED**. If denied, the offending quoted-example line is
re-wrapped (`<…>` placeholder / fenced span) and re-probed until ALLOWED. (Confirms the build is
landable through the gate that is actually live during the build.)

---

## §5 — A2 / §35 threat-alignment (threat→mitigation map + threat-anchored probe)

**Named threat M1 (directive / floor-manager):** "a real STRUCTURED author field naming a non-Denson
PERSON slips past the narrowed gate." This is the reputational/legal regression the gate exists to
prevent (regressed TWICE). The arc is a SECURITY gate change.

**Threat→mitigation map (Approach §2):**

> **M1 (a real structured author field naming a non-Denson person slips the narrowed gate)**
> → **attack-path:** the narrowing widens `.md` scope so far that a real frontmatter `author: <non-Denson>`
> (SKILL.md/plugin), or a config-file author (`package.json`/`LICENSE`/`NOTICE`/`CITATION.cff`), is no
> longer extracted → reaches commit un-audited.
> → **how-defeated:** the narrowing applies ONLY to `.md` and ONLY by RESTRICTING the scan window to the
> YAML frontmatter block — it never relaxes the VALUE check (`is_principal`) and never touches the config
> path (`cfg` mode = OLD regex, byte-identical). Frontmatter `author:` STAYS extracted (verified live:
> `author: Jane Roe` in frontmatter ⇒ MATCH). Config files are untouched. The only thing removed from
> coverage is `.md` **body prose**, which is authorship-DISCUSSION, not a structured author CLAIM (Q-B,
> explicitly delegated to prose-discipline + audit + NOMOS).

**Threat-anchored probe (asserts BOTH halves of §6.13):**
- **(a) attack-blocked:** **P2** drives the named attack path across EACH covered class — a
  true-positive fixture for `package.json`, SKILL.md frontmatter, `LICENSE`, `NOTICE`, `CITATION.cff`,
  each naming the fictional non-Denson "Fenwick Galsworthy" — and asserts the gate computes **BLOCK**.
  P5 + P6 drive the live form (real commit DENIED). This is the verdict's `defeats_via_probe: P2`.
- **(b) legit-unaffected:** **P1** (z2b body-prose instances now ALLOW) + **P3 control** (a config /
  frontmatter author = Denson Smith still ALLOWS) — the mitigation did not defeat the threat by breaking
  the legitimate path.

A probe that asserted only "the extractor emits nothing on body prose" would NOT be threat-anchored; P2
exercises the attack path (a real wrong-person field) across every covered class, which is what
falsifies "the narrowing drifted to the wrong surface and let a real claim through."

---

## §6 — Self-assessed weak points

1. **Q-B residual: a body `Author: <wrong person>` line in a `.md` README is no longer mechanically
   caught.** This is a deliberate, defended coverage reduction (§2.1 Q-B). The risk is real but narrow:
   the high-value author surfaces (`package.json`, SKILL.md frontmatter, `LICENSE`, `CITATION.cff`)
   stay covered; only a free-text body `Author:` in a `.md` falls to the prose-discipline + manual
   audit + NOMOS/human-review layers. *Why this shape anyway:* there is no mechanical predicate that
   separates a real body `Author: Jane Roe` from the z2b discussion prose — they are the same surface —
   so any rule that re-covers body lines re-opens z2b. ARGUS should rule whether the residual is
   acceptable or whether a `.md` README badge-line convention should be added to keep one structured
   body surface covered.

2. **The `is_author_encoding_file` relocation to `_hooklib.sh` (§3.4) is a refactor inside a security
   arc.** It is behavior-preserving (same `case` arms) and is justified to let the runner exercise the
   REAL path matcher — but any refactor of a live gate carries regression risk. *Why this shape anyway:*
   the alternative (a `AUTHOR_GATE_LIB_ONLY` source-guard on the gate, §3.3 (a)) is uglier and still
   touches the gate; centralizing the matcher in the lib both functions source is cleaner and is
   asserted byte-deny-identical by the corpus. ARGUS should rule relocate-vs-source-guard.

3. **Frontmatter detection is regex-based, not a YAML parser.** A `.md` with an unusual frontmatter
   delimiter (e.g. `+++` TOML frontmatter, or a frontmatter block not at byte 0 after content) would
   not be sliced, so an author field in such a block would be MISSED (under-enforcement). *Why this
   shape anyway:* the substrate's `.md` frontmatter is uniformly leading `---`…`---` YAML (SKILL.md,
   role files); a full YAML/TOML frontmatter parser is scope-creep for a backstop gate, and the default
   `cfg` mode (broadest scan) is the fallback for any caller that does not opt into `md`. Flagged so
   ARGUS can confirm the substrate has no `+++`/non-leading frontmatter convention. The fail-direction
   is under-enforcement on an exotic shape, mitigated by the prose discipline + audit layers.

4. **Committability self-test (P10) depends on the OLD gate's exact value-resolution for quoted
   examples in the design doc / README.** If a quoted `author:` example resolves to a non-skipped
   non-Denson value under the OLD whole-blob regex, the build commit is blocked and ADA must re-wrap it.
   This is a process friction, not a correctness risk — flagged so ADA expects it and uses `<…>`
   placeholders / fenced spans for any quoted wrong-name example.

---

## §7 — Out of scope

- Changing the seat-attribution convention or adding path-exemptions (PRINCIPAL chose option (a)).
- The stashed Arc-61 directive-DoD fix (`git stash@{0}` on main) — popped as a §18 follow-up AFTER this lands.
- `stoa--9s6` / `ruu` / `p41.3-5` / `luo` — separate tickets.
- A full YAML/TOML frontmatter parser, or `+++` TOML frontmatter support (weak point 3) — backstop gate; not warranted.
- Arming the gate / `--enable-hooks` changes — deploy stays INERT + default-OFF (HARD SAFETY CONSTRAINT, unchanged).
