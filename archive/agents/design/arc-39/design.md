# Arc 39 design — save-verdict promotion + PRINCIPAL-intent probe canon (2 bundled candidates)

**Author seat:** CAPTAIN_DAEDALUS_the-stoa
**Branch:** `arc-39/build` (worktree at `.claude/worktrees/arc-39-build/`)
**Work-units:** C1 stoa--utn (save-verdict skill promotion to substrate) + C2 stoa--ezj (PRINCIPAL-intent probe discipline canon)
**Directive (LOCKED):** `substrate/arcs/arc-39-build-directive.md` (A1-A22 LOCKED; A2/A4/A6/A9 DAEDALUS-discretion)
**Operating mode:** AUTONOMOUS (peer = MAJOR_PLINY_the-stoa via stoa--utn coordination ticket; user-tier POLYBIUS via QA at arc close per A18)
**Revision history:** rev1 @ 35f7c181 → ARGUS audit verdict needs-revisions (`agents/verdicts/arc-39/CAPTAIN_ARGUS-2026-05-18T06-12-47Z.md`) → rev2 (this file) lands R1+R2+R3 load-bearing + M1+M2+M3 minor revisions per PLINY dispositions.

---

## §1.0 — Brief (restatement-gate per CAPTAIN_DAEDALUS §6.1)

Arc 39 is Pass 5 of the SPECIFICATION.md §13 workplan and bundles two P3 candidates per §13.6: **C1 stoa--utn** promotes the user-tier `save-verdict` skill to substrate with the Python helpers that the user-tier SKILL.md procedure invokes against vapor (no `_save_verdict.py` and no `_lib/byte_copy.py` exist on disk; Arc 23 ratified Option A — extend the user-tier SKILL.md schema only — and deferred substrate promotion to this ticket); **C2 stoa--ezj** lands the PRINCIPAL-intent probe discipline canon by extending `MAJOR_PLINY.md` §7.2 (verify-then-execute), adding a POLYBIUS-side relay-discipline analog at `MAJOR_POLYBIUS.md`, and cross-referencing `operating-disciplines.md` §19 (confabulation) — with the 2026-05-13 category-before-option refinement folded in. Both candidates ship in one gauntlet under A1 LOCKED; each candidate's source ticket closes on ship with cross-ref + audit comment per A18.

**Restatement-gate (§6.1) imported-assumption disclosure:**

1. **The directive's "op-disc §5.7 verdict discussion" reference is a propagation of a pre-existing bug at `substrate/CAPTAIN_VERA.md:122`** (not a one-off typo). The substantive home for the verdict-shape vocabulary the save-verdict skill enforces is `operating-disciplines.md` §15 (verification-complexity awareness), specifically **§15.4** (the two new verdict shapes — INCOMPLETE + UNVERIFIABLE). `operating-disciplines.md` §5 is the single-paragraph "Suppress plausible-source citation without verification" — no §5.7 subsection, no verdict discussion. ARGUS rev1 audit (R1 load-bearing) surfaced that `substrate/CAPTAIN_VERA.md:122` carries the SAME wrong cite (`UNVERIFIABLE per §5.7`) as a propagated cross-ref bug — the directive did not invent the typo, it inherited it. Per CLAUDE.md global Fix-now + `operating-disciplines.md` §4.8, rev2 EXTENDS Arc 39 scope by one line to fix the source bug at `CAPTAIN_VERA.md:122`, in addition to writing the new design's cross-refs at the correct `§15.4` locus. Probe P11a (new in rev2) greps for any remaining unresolved `§5.7` cite in substrate canon files and confirms (per §4 below) that only the legitimate self-refs survive. Historical arc-directives (`arc-23-build-directive.md` lines 37, 185) carry the same wrong cite but are immutable arc records and out of scope for this fix.

2. **The user-tier SKILL.md's "lieutenant" / "request bead" / "reply bead" / "PULSE_REVIEW" terminology is mostly compatible with the-stoa taxonomy.** "lieutenant" survives as the substrate-canonical name for the SKILL tier (verified at `substrate/skills/agent-author/SKILL.md` line 36 + `substrate/MAJOR_PLINY.md` line 564); I retain it. "Officer" generalizes to the verdict-saving CAPTAINs (ARGUS / VERA / CATO) and I will modernize the prose to use "CAPTAIN" where the user-tier text said "Officer." "PULSE_REVIEW" is a gauntlet-era name with no in-substrate referent today; I will rewrite the affected sentence to name the discipline rather than a non-existent skill (per A4 ii). "request bead" / "reply bead" survive as the bw-comment vocabulary and I retain them.

3. **A9 pick is ε (fold-in WITH explicit canonical-probe-sequence).** The user-tier weak lean is γ-or-ε; PRINCIPAL's 2026-05-13T03:08:13Z comment on stoa--ezj already spells the 3-step canonical sequence (category → shape-within-category → specifics-within-shape) in clean enumeration. ε is the cleaner canonical phrasing — it lands the sequence as numbered steps rather than embedded prose. Cost is one extra paragraph; benefit is grep-able structure for future seats.

4. **The "MCP-confabulation fifth-subtype" anchor (2026-05-13T21:25:30Z on stoa--ezj) is OUT OF SCOPE for Arc 39.** That comment proposes extending the discipline cluster from 4 disciplines to 5 by adding "verify documentation against empirical reality before authoring artifacts that assume documented capability works." Ezj is currently scoped to the 4-discipline cluster (ioy / nvl / 53u / ezj). Adding the 5th MCP-subtype would (a) widen ezj canon beyond what the directive A20 hard-locks, and (b) require its own empirical anchoring + 4-discipline-cluster reframing. Surface for separate future ticket; do not absorb into Arc 39.

None of (1)-(4) exceed DAEDALUS discretion per `operating-disciplines.md` §25.3 BLOCK semantics — they are calibration sub-decisions within the directive's locked envelope. The (1) fix-now extension is an authorized scope-widening per PLINY rev2-disposition (CLAUDE.md global Fix-now + op-disc §4.8). Restatement converges with the brief; no `refused` route.

---

## §1.1 — DAEDALUS sub-decision summary (A2 / A4 / A6 / A9)

| ID | Sub-decision | DAEDALUS pick | Aligns with user-tier lean? | One-line rationale |
|---|---|---|---|---|
| A2 | `_lib/byte_copy.py` scope | **α — single-skill private** at `substrate/skills/save-verdict/_lib/byte_copy.py` | yes | User-tier SKILL.md "Preservation discipline" already names cross-skill share with COPY_ARTIFACT + TRANSCRIBE_BW_TO_DISK; A20 hard-locks both out of Arc 39 scope; β would create an unused-shared-lib state; α keeps Arc 39 tight + lets sp1 refactor with full N=3 consumer context. |
| A4 | SKILL.md modernization | **ii — lift-and-modernize** at promotion time | yes | Modernizing at promotion avoids a second touch later AND removes save-verdict from sp1's scope. Modernization is targeted (PULSE_REVIEW reference + "Officer" → CAPTAIN + verdict-path example reframed for the-stoa's `agents/verdicts/<ticket>/` convention + obsolete 2026-05-12 executable-enforcement caveat block removed + user-tier line 16 body-prose `Author: Denson Smith` line dropped per substrate precedent — see §2.3). |
| A6 | utn substrate-canon cross-refs | **CAPTAIN_VERA + CAPTAIN_CATO + CAPTAIN_ARGUS + `operating-disciplines.md` §15.4** | yes (with §5.7 → §15.4 resolution per §1.0 disclosure 1) | The verdict-saving seats are the verdict-class CAPTAINs (ARGUS plan-critic / VERA falsifier / CATO craft-review); ADA / DAEDALUS / ZENO do NOT save verdicts (they consume verdicts or author other artifact classes). §15.4 is the substantive home for the verdict-shape vocabulary save-verdict enforces. |
| A9 | ezj category-before-option fold-in | **ε — fold-in WITH explicit canonical-probe-sequence** | yes (weakly leans ε) | PRINCIPAL's 2026-05-13 comment already spells the 3-step sequence cleanly; ε lifts the sequence verbatim as numbered canon rather than embedding it as prose. Cost is one extra paragraph; benefit is grep-able structure. |

**Substance disagreements with directive or user-tier leans:** none. All four picks align. No PRINCIPAL-gate (§25.3 BLOCK) surface engaged. ARGUS is the right next reader.

---

## §2 — C1: save-verdict skill promotion (stoa--utn)

### §2.1 — Files this candidate creates / modifies

**New directory tree under `substrate/skills/save-verdict/`:**

| Path | Purpose | Author source |
|---|---|---|
| `substrate/skills/save-verdict/SKILL.md` | Prose canon for the skill (procedure, input contract, failure modes). Lift-and-modernize from `~/.claude/skills/save-verdict/SKILL.md` per A4 ii. MUST carry `author: Denson Smith` YAML frontmatter per A17. | User-tier SKILL.md (143 lines) modernized per §2.3 below. |
| `substrate/skills/save-verdict/_save_verdict.py` | Python helper implementing the SKILL.md procedure steps 1-9. ~150-250 LOC. | NEW authoring per §2.4 below; spec'd in SKILL.md prose at user-tier (steps 1-9 + failure modes + exit codes). |
| `substrate/skills/save-verdict/_lib/__init__.py` | Empty marker file making `_lib/` a Python package for `from _lib.byte_copy import write_with_verify` import shape. | NEW (empty file). |
| `substrate/skills/save-verdict/_lib/byte_copy.py` | `write_with_verify` primitive (sha256 round-trip write). ~30-60 LOC. Private to save-verdict per A2 α; cross-skill share deferred to sp1. | NEW authoring per §2.5 below; spec'd in user-tier SKILL.md "Preservation discipline" section. |

**Files modified:**

| Path | Change | Reason |
|---|---|---|
| `substrate/install.sh` (line 149, `SKILL_NAMES` array, after `handoff-author` at line 148) | Append bare `save-verdict` entry (no trailing comment) | A5 LOCKED — wires the new skill into the install loop. The skill-deploy loop at lines 785-799 already handles nested `_lib/` subdirectories cleanly via `cp -R "$src_skill"/. "$dest_skill"/`. Bare-name entry matches existing array convention (per ARGUS R3). |
| `substrate/CAPTAIN_VERA.md` | (a) Cross-ref insertion at the verdict-emit section per A6; (b) **`§5.7` → `§15.4` fix at line 122** (the cited locus for the UNVERIFIABLE-verdict synthesis-claim row), per CLAUDE.md global Fix-now + op-disc §4.8 + ARGUS R1. | A6 — VERA emits PASS / FAIL / NEEDS-REVISIONS / INCOMPLETE / UNVERIFIABLE verdicts; cite the canonical save-verdict skill at the seat that emits them. Fix-now — the design rev1 surfaced this pre-existing bug via the directive's propagated typo; Arc 39 is the natural arc to fix the source because we are already touching `§15.4`-adjacent wiring. |
| `substrate/CAPTAIN_CATO.md` | Cross-ref insertion at the verdict-emit section | A6 — same rationale at the craft-review seat. |
| `substrate/CAPTAIN_ARGUS.md` | Cross-ref insertion at the verdict-emit section | A6 — same rationale at the plan-critic seat. |
| `substrate/operating-disciplines.md` §15.4 | One-paragraph cross-ref to the new save-verdict skill as the canonical write-path for INCOMPLETE + UNVERIFIABLE verdict bodies | A6 — §15.4 introduces the two new verdict shapes; the cross-ref tells readers HOW to write them to disk canonically. Resolves the directive's "op-disc §5.7" reference at the correct locus per §1.0 disclosure 1. |
| `substrate/skills/agent-author/SKILL.md` (YAML frontmatter) | Insert `author: Denson Smith` after `description:` line | **Fix-now per CLAUDE.md global + op-disc §4.8** — substrate-tier skill is missing the A17 frontmatter (per ARGUS M3 surface). A20 #5 hard-lock targets USER-tier retroactive modernization only; substrate-tier author-frontmatter Fix-now is in scope per PLINY rev2-disposition. Cost = 1 line. |
| `substrate/skills/check-substrate-updates/SKILL.md` (YAML frontmatter) | Insert `author: Denson Smith` after `description:` line | **Fix-now per CLAUDE.md global + op-disc §4.8** — same rationale as agent-author. Cost = 1 line. After this arc, 7 of 7 substrate skills carry `author: Denson Smith` frontmatter (was 4 of 6 pre-Arc-39; Arc 39 adds save-verdict as the 7th and backfills the 2 missing). |

### §2.2 — Hand-off contract (what each verdict-saving CAPTAIN gets)

After this candidate ships, any CAPTAIN dispatched by PLINY that produces a verdict (today: ARGUS, VERA, CATO) gets:

- The canonical write-path: `<repo-root>/agents/verdicts/<ticket-id>/<CAPTAIN>-<YYYY-MM-DDTHH-MM-SSZ>.md`.
- Schema-conformant validation at write time: malformed officer name (`^[A-Z][A-Z0-9_]*$`), malformed ticket id (`^[a-zA-Z0-9._-]+$`), and shape-conformance for INCOMPLETE / UNVERIFIABLE (required-field enforcement per `operating-disciplines.md` §15.4) all exit 4 BEFORE any file write.
- sha256 round-trip verification on every write (defense-in-depth against partial writes / filesystem corruption).
- A traceable record artifact at `agents/save-verdict/<request-id>.txt` per write (exit code + duration + resolved dest + sha256s + diagnostics).

The hand-off contract for ADA / VERA / CATO when they consume the deployed skill: invoke via `python .claude/skills/save-verdict/_save_verdict.py …` with the SKILL.md-documented argument set. The CAPTAIN role-file cross-refs (per §2.1 table row) point at the substrate SKILL.md canonical home.

### §2.3 — SKILL.md modernization scope (A4 ii)

Take `~/.claude/skills/save-verdict/SKILL.md` verbatim as the starting point. Apply these targeted modernizations:

| Locus (user-tier SKILL.md line) | Old text | New text | Rationale |
|---|---|---|---|
| Line 10 | "Officer envelopes individually decide where to save verdicts: ARGUS picks one path, VERA picks another, CATO writes to /tmp/." | "CAPTAIN envelopes individually decide where to save verdicts: ARGUS picks one path, VERA picks another, CATO writes to /tmp/." | "Officer" is gauntlet-era; the-stoa taxonomy uses CAPTAIN. |
| Line 10 | "...inconsistent naming conventions that make cross-ticket aggregation (PULSE_REVIEW) brittle." | "...inconsistent naming conventions that make cross-ticket aggregation brittle." | PULSE_REVIEW is a gauntlet-era skill name with no in-substrate referent. Drop the parenthetical; the substantive claim survives. |
| Line 14 | "It specializes `write_with_verify` from `skills/_lib/byte_copy.py` with the canonical-path convention. COPY_ARTIFACT and TRANSCRIBE_BW_TO_DISK share the same primitive." | "It specializes `write_with_verify` from `_lib/byte_copy.py` (private to this skill in Arc 39; cross-skill share with COPY_ARTIFACT + TRANSCRIBE_BW_TO_DISK deferred to substrate ticket stoa--sp1 per directive A2 α + A20)." | A2 α scope; documents the deferred cross-skill-share decision so future readers don't re-litigate. |
| **Line 16 (body-prose Author line)** | `Author: Denson Smith.` (standalone body paragraph between the "Why this skill exists" body and the "Preconditions" heading) | **DELETE the entire line + the surrounding blank line.** | **Per ARGUS M2 + PLINY rev2-disposition**: substrate precedent (handoff-author, credential-discipline, check-bw-release, inspect-script-output) carries `author: Denson Smith` ONLY in YAML frontmatter, NEVER as body prose. Lift-and-modernize (A4 ii) means matching the substrate convention. The A17 frontmatter addition (table row below) replaces the authorship signal at the canonical locus. |
| Line 137 | "...the aggregation that picks 'which is the verdict-of-record' is PULSE_REVIEW or the caller's judgment." | "...the aggregation that picks 'which is the verdict-of-record' is the caller's judgment (PLINY at arc close; POLYBIUS at retrospective)." | PULSE_REVIEW reference dropped per above; canonical aggregators named explicitly. |
| Lines 131-132 (entire "Caveat on executable enforcement (2026-05-12)" block) | "**Caveat on executable enforcement (2026-05-12).** The validation behavior above is canon-establishing in this SKILL.md prose. The executable Python helper (`_save_verdict.py`) referenced in the **Procedure** section is not yet authored on disk; the shape-conformance exit-4 paths above are spec for the future helper, not currently executable. A follow-up substrate ticket (per Arc 23 design §10.1) will author the helper and promote both SKILL.md and helper to `substrate/skills/save-verdict/`, exercising the `operating-disciplines.md` §8.4 install.sh smoke beat against the promotion." | **DELETE the entire block.** | Arc 39 IS the follow-up ticket the caveat anticipates; once the helper exists on disk and is deployed, the caveat is obsolete. |
| Line 143 (Preservation discipline section) | "Source-of-truth at `skills/save-verdict/SKILL.md` + `skills/save-verdict/_save_verdict.py`. Shares `skills/_lib/byte_copy.py` with COPY_ARTIFACT and TRANSCRIBE_BW_TO_DISK." | "Source-of-truth at `substrate/skills/save-verdict/SKILL.md` + `substrate/skills/save-verdict/_save_verdict.py` + `substrate/skills/save-verdict/_lib/byte_copy.py`. Deployed at all 3 install tiers (user / project / subproject) via `substrate/install.sh` `SKILL_NAMES` array. Cross-skill share of `_lib/byte_copy.py` with COPY_ARTIFACT + TRANSCRIBE_BW_TO_DISK deferred to stoa--sp1 per Arc 39 directive A2 α + A20." | Reflects substrate paths post-promotion; documents the deferred share decision. |
| YAML frontmatter (lines 1-4) | `---\nname: save-verdict\ndescription: "..."\n---` | `---\nname: save-verdict\ndescription: "..."\nauthor: Denson Smith\n---` | A17 IMMUTABLE — frontmatter `author: Denson Smith` MUST be present per CLAUDE.md global rule. Matches precedent at `substrate/skills/credential-discipline/SKILL.md` line 4 + `substrate/skills/check-bw-release/SKILL.md` line 4 + `substrate/skills/inspect-script-output/SKILL.md` line 4 (4-line frontmatter shape: `--- / name / description / author / ---`). |

**Modernizations NOT to apply** (preserve user-tier prose verbatim):
- "lieutenant" terminology (verified compatible with the-stoa taxonomy at `substrate/skills/agent-author/SKILL.md` line 36 + `substrate/MAJOR_PLINY.md` line 564 — `lieutenant_skill` is the canonical agent type).
- "request bead" / "reply bead" (canonical bw-comment vocabulary).
- "gauntlet repo root" / "gauntlet-ylq" example ticket id (the gauntlet metaphor for the dispatch pipeline survives the rename; ticket-id is an example string, not an obsolete reference).
- Verification-complexity field schema (`verdict_shape` / `quadrant_classification` / `coverage_description` / `sanity_check_performed` / `recommended_next_step`) — this is Arc 23 ratified canon and stays verbatim.

### §2.4 — `_save_verdict.py` authoring spec

Author at `substrate/skills/save-verdict/_save_verdict.py`. Invocation contract per user-tier SKILL.md step 9 (lines 103-115):

```
python substrate/skills/save-verdict/_save_verdict.py \
  --ticket-id <id> \
  --officer <CAPTAIN-name> \
  (--body <inline-string> | --body-path <file-path>) \
  [--timestamp <ISO-8601>] \
  [--overwrite] \
  --cwd <abs-path> \
  --artifact-path <abs-path> \
  --request-id <id> \
  --caller <CAPTAIN-name> \
  [--verdict-shape pass|fail|needs-revisions|INCOMPLETE|UNVERIFIABLE] \
  [--quadrant-classification easy-easy|hard-easy|easy-hard|hard-hard] \
  [--coverage-description <prose>] \
  [--sanity-check-performed <prose>] \
  [--recommended-next-step <prose>]
```

**Invocation-contract decision (R2, PLINY rev2-disposition LOCKED):** the helper is invoked AS A SCRIPT via path-invocation (`python .claude/skills/save-verdict/_save_verdict.py …`), NOT as a module (`python -m save_verdict._save_verdict …`). This is a deliberate canon-establishing pick for the first Python skill in substrate. The path-invocation contract:

- Matches the SKILL.md procedure step 9 prose verbatim (already documented at user-tier line 104 as `python skills/save-verdict/_save_verdict.py …`).
- Matches the broader user-tier SKILL.md invocation convention (substrate skills are pointed-at by their filesystem path, not imported as packages).
- Does NOT require restructuring `_lib/` with `__init__.py` at multiple levels to make the skill importable as a package.
- Establishes the canon-precedent for future Python substrate skills — specifically the sp1-deferred `copy-artifact` + `transcribe-bw-to-disk` candidates (when they promote, they inherit the same path-invocation contract).

The import-mechanism inside the script is `sys.path.insert(0, str(pathlib.Path(__file__).parent))` so `from _lib.byte_copy import write_with_verify` resolves when invoked as a script. This is the standard Python idiom for path-invoked scripts that need to import sibling-package modules. The 1-line sys.path manipulation is the cost of preserving the invocation-contract stability — promoted from "weak point" in rev1 to "deliberate canon-establishing pick" in rev2.

**Procedure (mirrors SKILL.md steps 1-9 verbatim):**

1. **argparse** the arguments above. Mutual-exclusion enforcement: `--body` XOR `--body-path` (both-or-neither exits 4).
2. **Validate inputs** per regex + shape-conformance:
   - `--officer` matches `^[A-Z][A-Z0-9_]*$` else exit 4 with diagnostic "officer name must match ^[A-Z][A-Z0-9_]*$".
   - `--ticket-id` matches `^[a-zA-Z0-9._-]+$` AND starts with `[a-zA-Z0-9]` (bare-dot / `..` / `-x` rejected as path-traversal defense) else exit 4 with diagnostic "ticket-id must match ^[a-zA-Z0-9][a-zA-Z0-9._-]*$".
   - If `--verdict-shape` in `{INCOMPLETE, UNVERIFIABLE}`: require `--quadrant-classification` in the 4-element enum else exit 4. If `INCOMPLETE`: require `--coverage-description` else exit 4. If `UNVERIFIABLE`: require BOTH `--sanity-check-performed` AND `--recommended-next-step` else exit 4. Diagnostics verbatim from user-tier SKILL.md "Failure modes" (lines 127-130).
3. **Resolve timestamp.** If `--timestamp` absent, use `datetime.now(timezone.utc)`. Filename encoding via `strftime('%Y-%m-%dT%H-%M-%SZ')` (colons → hyphens for cross-platform filename safety).
4. **Compute resolved dest:** `<cwd>/agents/verdicts/<ticket_id>/<officer>-<ts-fn>.md`. Create parent dirs if missing (`mkdir -p` semantics; `os.makedirs(..., exist_ok=True)`).
5. **Read body bytes.** From `--body` (UTF-8 encode) or `--body-path` (`open(..., 'rb')`). If `--body-path` does not exist: exit 4 with "body-path does not exist: <path>".
6. **Pre-flight dest-exists check.** If dest exists AND `--overwrite` flag absent: exit 3 with "dest exists; use --overwrite to replace: <path>". NO writes performed.
7. **Write via `write_with_verify`** (imported from `_lib.byte_copy`). On sha256 mismatch: exit 2 with "sha256 round-trip mismatch: input=<hex> dest=<hex>".
8. **Re-hash on-disk file** (defense-in-depth; second read of the just-written file + sha256 compare to step-7 result). On mismatch: exit 2 with "post-write re-hash mismatch: write=<hex> reread=<hex>".
9. **Write record artifact** at `--artifact-path` per the user-tier SKILL.md "Output contract" template (lines 56-83). Exit 0.

**Exit codes** (canonical, per user-tier SKILL.md line 117):
- `0` — ok
- `2` — sha256 round-trip mismatch (step 7 or step 8)
- `3` — dest exists without `--overwrite` (step 6)
- `4` — argument error (step 1, 2, or 5)
- `5` — internal error (OS errors during write, unexpected exceptions in any step)

**Other implementation notes:**
- Use only Python stdlib (`argparse`, `pathlib`, `hashlib`, `datetime`, `os`, `sys`). No third-party imports — substrate skills run on whatever Python the deployed target has; minimal dependency surface is canonical for substrate Python.
- Per project CLAUDE.md `op-disc §13` Windows note: `PYTHONUTF8=1` is required for Python invocations on Windows; the skill assumes the caller's environment respects this (the SKILL.md procedure section already documents the env-var contract — no skill-side workaround needed).
- Importable AS a module: `from save_verdict import main` should work for callers that prefer in-process invocation over subprocess (compatibility, not required). Module-vs-script flexibility costs ~3 lines (the `if __name__ == "__main__": sys.exit(main())` idiom); benefit is testability + future call-sites that don't want subprocess overhead. Note this does NOT undo the R2 invocation-contract decision — the canon-invocation is path-invocation; module-importability is a side-benefit, not the contract.
- Use only stdlib `argparse` for parsing — NOT `click` / `typer`. Substrate Python skills run on the target's stdlib only.

### §2.5 — `_lib/byte_copy.py` authoring spec

Author at `substrate/skills/save-verdict/_lib/byte_copy.py`. Implements the `write_with_verify` primitive the user-tier SKILL.md step 7 invokes.

**Signature:**

```python
def write_with_verify(
    dest_path: pathlib.Path,
    body_bytes: bytes,
    overwrite: bool = False,
) -> dict:
    """
    Write body_bytes to dest_path with sha256 round-trip verification.

    Computes sha256 of body_bytes (input_sha256), writes bytes to dest_path,
    re-reads dest_path, computes sha256 of read-back bytes (dest_sha256), and
    asserts input_sha256 == dest_sha256. On mismatch, raises ValueError with
    both hashes in the message.

    Returns: {
        "input_byte_length": int,
        "input_sha256": str,  # hex
        "dest_sha256": str,   # hex
        "verification": "pass" | "fail",
    }

    Raises:
        FileExistsError — if dest_path exists and overwrite is False.
        ValueError — if sha256 round-trip mismatch.
        OSError — bubbled from write/read.

    Parent directory must exist; caller is responsible for mkdir -p semantics.
    """
```

**Implementation notes:**
- ~30-50 LOC.
- Use `hashlib.sha256(body_bytes).hexdigest()` for input hash; same for re-read bytes.
- Use `dest_path.write_bytes(body_bytes)` then `dest_path.read_bytes()` for round-trip.
- On `not overwrite` + `dest_path.exists()`: raise `FileExistsError(f"dest exists: {dest_path}")` BEFORE any write.
- No `os` or `tempfile` ceremony — `pathlib` API is sufficient.
- Per A2 α: file is PRIVATE to save-verdict (under `substrate/skills/save-verdict/_lib/`, NOT under `substrate/skills/_lib/`). Empty `__init__.py` at `substrate/skills/save-verdict/_lib/__init__.py` makes `_lib/` a proper Python package; combined with the sys.path manipulation in `_save_verdict.py` (R2 invocation-contract canon — see §2.4), `from _lib.byte_copy import write_with_verify` resolves cleanly when `_save_verdict.py` is invoked as a script.

### §2.6 — install.sh wiring (A5 LOCKED)

Single edit at `substrate/install.sh` line 149 in the `SKILL_NAMES=( … )` array. The existing `handoff-author` entry is at line 148; append `save-verdict` as a bare-name entry on line 149 (per ARGUS R3 — match existing array convention; NO trailing arc-attribution comment):

```sh
SKILL_NAMES=(
  agent-author
  check-substrate-updates
  credential-discipline
  check-bw-release
  inspect-script-output
  handoff-author
  save-verdict
)
```

The skill-deploy loop at lines 785-799 already handles nested directories cleanly via `cp -R "$src_skill"/. "$dest_skill"/` (verified by reading the loop body — the `cp -R` recursive copy walks the entire subtree, picking up `_lib/byte_copy.py` + `_lib/__init__.py` automatically). No loop modification needed.

**install.sh smoke-beat probes** (per `operating-disciplines.md` §8.4 substrate-edit smoke-beat discipline + utn deliverable 5) — see §4 probes P1-P3.

---

## §3 — C2: PRINCIPAL-intent probe discipline canon (stoa--ezj)

### §3.1 — MAJOR_PLINY.md §7.2 extension

**File:** `substrate/MAJOR_PLINY.md`
**Section:** existing `### 7.2 Verify-then-execute (u--7yg.10, u--7yg.18)` (currently at lines 675-683)
**Insertion locus:** new paragraph after the existing "Scope-broadening (Arc 24 / stoa--ioy)" paragraph (line 681), BEFORE the Arc 9 worked-example paragraph (line 683). Keeps the existing Arc 9 anecdote anchored at the section's end.

**Exact prose to add (canon-grade; ADA lifts verbatim):**

```markdown
**Scope-broadening (Arc 39 / `stoa--ezj`) — PRINCIPAL-intent probe.** Verify-then-execute also fires when the work item you are about to queue or design DEPENDS on an upstream PRINCIPAL-intent decision that has not yet been probed. Before queuing or designing a work item whose shape is determined by upstream PRINCIPAL-intent (deliverable form, target audience, success criteria, scope boundaries), probe those decisions explicitly rather than inferring. Queuing a work item on inferred-intent commits the team to a phantom design; the queued work then has to be undone when PRINCIPAL surfaces the actual intent.

Three concrete sub-shapes of the failure mode (per ticket `stoa--ezj`):

1. **Deliverable shape unspecified.** Work item references a "demo" / "doc" / "presentation" / "recording" without naming the artifact form. The recipient cannot start because the shape determines the work.
2. **Audience unspecified.** Work item references a writeup but the target reader (investor / customer / technical / internal) determines voice, depth, framing. Without it the writeup cannot be authored faithfully.
3. **Success criteria unspecified.** Work item references "verify X works" / "demo Y" without naming what "works" or "demo" must satisfy. The recipient defines the criteria themselves and may misalign.

**The canonical probe sequence (3 steps, category-first; per the 2026-05-13 refinement in `stoa--ezj`):**

1. **Category:** what SHAPE OF THING is this? (artifact, infrastructure, skill, doc, service, agent-loadable context, etc.) Probing an option-set within the wrong category (e.g., enumerating four "human watches a presentation" options when the actual answer is "user-pointable agent skill") is the same failure mode as not probing at all — PRINCIPAL is forced to pick the least-wrong wrong option.
2. **Shape-within-category:** now that we know it's [category], what shape? (which type of skill, which kind of artifact, etc.)
3. **Specifics-within-shape:** now that we know it's a [shape], what are the substantive details?

Skipping step 1 and going straight to step 2 with conventional-category-defaults is a recognizable failure mode in 2026 substrate work — the agent-substrate domain has unconventional-category answers ("a user-pointable agent skill") that conventional defaults ("video / doc / deck") miss entirely.

Empirical anchor: 2026-05-13 PLINY-ariadne queued "pre-record the 4 demo queries" assuming a conventional-rehearsal category; POLYBIUS extrapolated to conventional-deliverable-shape options; PRINCIPAL had to manually correct from outside both extrapolations (the actual answer was "self-serve agent-testable demo where the user points their own agent at the corpus" — a fifth, unconventional category). The dual extrapolation cost real time. Substrate ticket: `stoa--ezj` (2026-05-13T03:08:13Z comment).

Cross-refs: `operating-disciplines.md` §19 (confabulation — PRINCIPAL-intent extrapolation is a confabulation subtype); `MAJOR_POLYBIUS.md` §4.3.1 (relay-side analog — when relaying work items from PLINY to PRINCIPAL, POLYBIUS surfaces unprobed-intent gaps explicitly); four-discipline-cluster siblings `stoa--ioy` (general "uncertain, checking"), `stoa--nvl` (verify-tool-availability), `stoa--53u` (idle-state retrospective-narrative confabulation).
```

### §3.2 — MAJOR_POLYBIUS.md relay-side analog

**File:** `substrate/MAJOR_POLYBIUS.md`
**Section:** new sub-subsection `#### 4.3.1 PRINCIPAL-intent probe at relay time` under existing `### 4.3 Verify-then-execute` (currently at line ~? — ADA verifies §4.3 line range at build time per §5 grounding-check).
**Position:** appended at the end of §4.3's body, BEFORE the next sibling §4.4 heading.
**Adjacency rationale (M1 pick, PLINY weak lean ratified):** PRINCIPAL-intent probing is a SUB-APPLICATION of verify-then-execute, so nesting under §4.3 expresses the discipline-relationship STRUCTURALLY rather than just thematically. Rev1 placed this at §4.9 (sequence-appended, peer to §4.1-§4.8); rev2 promotes it to §4.3.1 (sub-subsection under the parent discipline it specializes). Sub-subsections do not currently exist in `MAJOR_POLYBIUS.md` §4.x — this establishes a new nesting pattern, but the cost is small (one extra hash mark in the heading) and the benefit is the relationship between PRINCIPAL-intent probing and verify-then-execute is grep-able from the section number alone (a future seat searching `§4.3` finds both the parent discipline and its specialization).

**Exact prose to add (canon-grade; ADA lifts verbatim):**

```markdown
#### 4.3.1 PRINCIPAL-intent probe at relay time (`stoa--ezj`)

When relaying a work item PLINY has queued back to PRINCIPAL (for ratification, for the next-step disposition queue, for any decision PLINY has surfaced), check the work item for unprobed-intent gaps BEFORE the relay. If the work item depends on an upstream PRINCIPAL-intent decision that PLINY did not explicitly probe (deliverable shape, target audience, success criteria, scope boundaries), surface the gap explicitly in the relay rather than letting it propagate.

This is the relay-time specialization of verify-then-execute (§4.3 parent) and the relay-time analog of PLINY's `MAJOR_PLINY.md` §7.2 PRINCIPAL-intent extension. PLINY catches the gap at queuing time; POLYBIUS catches it at relay time. Both catches are necessary — PLINY's catch prevents the queued work from being designed on inferred-intent; POLYBIUS's catch prevents an inferred-intent work item from reaching PRINCIPAL framed as a settled decision.

**The canonical probe sequence (3 steps, category-first; per `MAJOR_PLINY.md` §7.2 PRINCIPAL-intent extension):**

1. **Category:** what SHAPE OF THING is this? (artifact, infrastructure, skill, doc, service, agent-loadable context, etc.)
2. **Shape-within-category:** now that we know it's [category], what shape?
3. **Specifics-within-shape:** now that we know it's a [shape], what are the substantive details?

When relaying a work item that names an option-set without first probing the category, the relay defaults to inheriting PLINY's category-assumption — which may be wrong. Probe category FIRST.

Empirical anchor: 2026-05-13 — when POLYBIUS asked PRINCIPAL to pin Q1 (deliverable shape) for a downstream work item, POLYBIUS offered four options: live walkthrough / recorded video / written doc / slide deck. PRINCIPAL selected "live walkthrough." Then PRINCIPAL clarified: the actual answer was a fifth option POLYBIUS didn't surface — "self-serve agent-testable demo where the user points their own agent at the corpus." All four options POLYBIUS offered were in the "human watches a presentation" category. The actual answer was in a different category entirely ("user actively drives an agent"). Substrate ticket: `stoa--ezj` (2026-05-13T03:08:13Z comment, captured by POLYBIUS as self-diagnosis).

Cross-refs: `MAJOR_PLINY.md` §7.2 (queuing-time analog); `operating-disciplines.md` §19 (confabulation — PRINCIPAL-intent extrapolation is a confabulation subtype); four-discipline-cluster siblings `stoa--ioy` / `stoa--nvl` / `stoa--53u`.
```

### §3.3 — operating-disciplines.md §19 cross-ref

**File:** `substrate/operating-disciplines.md`
**Section:** existing §19 (Confabulation-under-uncertainty discipline, lines 1077-1228)
**Insertion locus:** new bullet at the end of §19.2's "Three application patterns" — augmenting the "**2. State-vs-claim mismatch.**" pattern with a cross-ref to the PRINCIPAL-intent specialization at PLINY §7.2 + POLYBIUS §4.3.1.
**Exact insertion:** at the end of §19.2's pattern-2 paragraph (currently at line 1094, immediately before the "**3. Unfamiliar territory.**" bullet at line 1096).

**Exact prose to add (canon-grade; ADA lifts verbatim, appending to the end of §19.2 pattern 2 — the existing paragraph ends with "...from any source." at line 1094):**

```markdown

**PRINCIPAL-intent extrapolation as a state-vs-claim sub-pattern (Arc 39 / `stoa--ezj`).** When the work item you are about to queue or design depends on an upstream PRINCIPAL-intent decision that has not been probed, the inferred intent is a CLAIM you are about to act on without verification. The verification action is to probe PRINCIPAL explicitly rather than queuing on inferred intent. The category-first canonical probe sequence (3 steps: category → shape-within-category → specifics-within-shape) is documented at `MAJOR_PLINY.md` §7.2 (queuing-time application) and `MAJOR_POLYBIUS.md` §4.3.1 (relay-time application). PRINCIPAL-intent extrapolation joins the four-discipline cluster around "probe ground truth before designing on top of inferred state" — tool-state (`stoa--nvl`), retrospective-state (`stoa--53u`), PRINCIPAL-intent-state (`stoa--ezj`), and the general "uncertain, checking" parent (`stoa--ioy`).
```

### §3.4 — N=1 provenance + canon-promotion gate

Per `operating-disciplines.md` §6.7.1 + `MAJOR_POLYBIUS.md` §15 honest-scope: PRINCIPAL articulated the PRINCIPAL-intent probe discipline 2026-05-13 (project-direction authority) and the category-before-option refinement same day. §6.7.1 does not carve out a "PRINCIPAL-declaration shortcut" — the honest reading: this discipline enters substrate canon off-gate on PRINCIPAL's project-direction authority + the empirical anchor, with future-evidence-accretion against the §6.7.1 gate still required for promotion to "structural lesson" status. Same N=1 framing as Arc 35's §28.7, Arc 32's §19.6.4, Arc 37's §19.7, and the existing §19.6 itself.

The MAJOR_PLINY.md §7.2 extension carries the empirical anchor in the prose; the MAJOR_POLYBIUS.md §4.3.1 carries it from the relay-side; the op-disc §19.2 cross-ref carries the four-discipline-cluster framing. The provenance is internally consistent across all three insertion sites; ARGUS should sanity-check the cross-refs resolve in all three directions.

---

## §4 — Verification probes (load-bearing for VERA + ZENO)

Probes are spec'd here for VERA mechanical falsification + ZENO mechanical spec-check. Each probe carries an ID (P1, P2, …) so downstream verdicts can cite by ID. Each names the verifier seat. Each is concrete enough to re-execute without ambiguity.

### §4.1 — C1 utn probes (install.sh smoke beats + helper semantics)

**P1 — install.sh dry-run lists save-verdict at `--target project` (VERA).**

```bash
bash substrate/install.sh --dry-run --target project --project-dir /tmp/arc39-probe-project 2>&1 | grep -E "save-verdict"
```

**Acceptance:** stdout contains a line referencing `save-verdict` in the deploy plan (the loop prints `[dry-run] deploy skill: <src>/save-verdict/ -> <dest>/save-verdict/ (cp -R)`). Non-zero match count = PASS. Zero match count = FAIL (install.sh wiring missing).

**P2 — install.sh dry-run lists save-verdict at `--target subproject` (VERA).**

```bash
bash substrate/install.sh --dry-run --target subproject --parent-dir /tmp/arc39-probe-parent --subproject probe-sub 2>&1 | grep -E "save-verdict"
```

**Acceptance:** same as P1.

**P3 — install.sh dry-run lists save-verdict at `--target user` (VERA).**

```bash
bash substrate/install.sh --dry-run --target user 2>&1 | grep -E "save-verdict"
```

**Acceptance:** same as P1.

**P4 — Deployed `_save_verdict.py` is executable AND SKILL.md procedure step 9 runs end-to-end (VERA).**

```bash
# Setup: deploy to a temp target.
TMPDIR=$(mktemp -d)
bash substrate/install.sh --target project --project-dir "$TMPDIR" 2>&1
test -f "$TMPDIR/.claude/skills/save-verdict/_save_verdict.py" && echo "helper present" || echo "helper MISSING"
test -f "$TMPDIR/.claude/skills/save-verdict/_lib/byte_copy.py" && echo "byte_copy present" || echo "byte_copy MISSING"

# Run a happy-path verdict write.
cd "$TMPDIR"
mkdir -p agents/save-verdict
PYTHONUTF8=1 python .claude/skills/save-verdict/_save_verdict.py \
  --ticket-id "probe-p4" \
  --officer "VERA" \
  --body "probe body" \
  --cwd "$TMPDIR" \
  --artifact-path "$TMPDIR/agents/save-verdict/probe-p4.txt" \
  --request-id "p4-request" \
  --caller "DAEDALUS"
echo "exit=$?"
ls -la agents/verdicts/probe-p4/
```

**Acceptance:** "helper present" + "byte_copy present" both printed; exit code `0`; `agents/verdicts/probe-p4/VERA-<timestamp>.md` exists with body "probe body"; `agents/save-verdict/probe-p4.txt` exists with the record-artifact template populated.

**P5 — Malformed `--officer` rejected at exit 4 (VERA).**

```bash
PYTHONUTF8=1 python .claude/skills/save-verdict/_save_verdict.py \
  --ticket-id "probe-p5" --officer "vera" --body "x" \
  --cwd "$TMPDIR" --artifact-path "$TMPDIR/agents/save-verdict/p5.txt" \
  --request-id "p5" --caller "DAEDALUS"; echo "exit=$?"
```

**Acceptance:** exit code `4`; stderr contains "officer name must match" or equivalent diagnostic.

**P6 — Malformed `--ticket-id` rejected at exit 4 (VERA).**

```bash
PYTHONUTF8=1 python .claude/skills/save-verdict/_save_verdict.py \
  --ticket-id "../escape" --officer "VERA" --body "x" \
  --cwd "$TMPDIR" --artifact-path "$TMPDIR/agents/save-verdict/p6.txt" \
  --request-id "p6" --caller "DAEDALUS"; echo "exit=$?"
```

**Acceptance:** exit code `4`; stderr contains "ticket-id must match" or equivalent diagnostic.

**P7 — Dest-exists without `--overwrite` rejected at exit 3 (VERA).**

```bash
# Pre-condition: P4 already created agents/verdicts/probe-p4/VERA-<ts>.md.
# Re-run P4's exact invocation (same --ticket-id, --officer, --timestamp).
PYTHONUTF8=1 python .claude/skills/save-verdict/_save_verdict.py \
  --ticket-id "probe-p4" --officer "VERA" --body "different body" \
  --timestamp "<exact-timestamp-from-P4>" \
  --cwd "$TMPDIR" --artifact-path "$TMPDIR/agents/save-verdict/p7.txt" \
  --request-id "p7" --caller "DAEDALUS"; echo "exit=$?"
```

**Acceptance:** exit code `3`; stderr contains "dest exists; use --overwrite"; the original P4 verdict file is UNTOUCHED (sha256 unchanged).

**P8 — sha256 mismatch caught at exit 2 (VERA, white-box).**

Hard to exercise end-to-end without filesystem injection; ADA spec'd to provide a unit-test entry-point that exercises the `write_with_verify` failure path via a mock filesystem (write returns different bytes than were sent). ADA's unit test:

```bash
PYTHONUTF8=1 python -c "
import sys; sys.path.insert(0, '.claude/skills/save-verdict')
sys.path.insert(0, '.claude/skills/save-verdict/_lib')
from byte_copy import write_with_verify
import pathlib, tempfile, unittest.mock as m

dest = pathlib.Path(tempfile.mktemp())
# Mock read_bytes to return different bytes than were written.
with m.patch.object(pathlib.Path, 'read_bytes', return_value=b'wrong'):
    try:
        write_with_verify(dest, b'right', overwrite=True)
        print('FAIL: should have raised')
        sys.exit(1)
    except ValueError as e:
        if 'sha256' in str(e).lower() or 'mismatch' in str(e).lower():
            print('PASS: ValueError raised with mismatch message')
            sys.exit(0)
        else:
            print(f'FAIL: wrong exception message: {e}')
            sys.exit(1)
"; echo "exit=$?"
```

**Acceptance:** exit code `0`; stdout contains "PASS: ValueError raised with mismatch message".

**P9 — A17 frontmatter check: `author: Denson Smith` present in deployed save-verdict SKILL.md (ZENO).**

```bash
grep -E "^author: Denson Smith$" substrate/skills/save-verdict/SKILL.md && echo "frontmatter OK"
```

**Acceptance:** match count = 1; "frontmatter OK" printed.

**P9b — A17 frontmatter Fix-now: ALL substrate skills carry `author: Denson Smith` frontmatter (ZENO; new in rev2, addresses M3).**

```bash
grep -lE "^author: Denson Smith$" substrate/skills/*/SKILL.md | wc -l
```

**Acceptance:** match count = 7 post-Arc-39 (every directory under `substrate/skills/` carries the frontmatter). Math: pre-Arc-39, 6 substrate skills exist (agent-author, check-substrate-updates, credential-discipline, check-bw-release, inspect-script-output, handoff-author); 4 carry the frontmatter (credential-discipline, check-bw-release, inspect-script-output, handoff-author); 2 do not (agent-author, check-substrate-updates). Arc 39 (a) introduces save-verdict NEW with frontmatter per §2.3 table; (b) adds the missing frontmatter line to agent-author + check-substrate-updates per §2.1 table. Post-Arc-39 substrate-skills count = 7; all 7 carry the frontmatter; grep | wc -l = 7. Mechanically enforces the M3 Fix-now property.

**P10 — Cross-refs in CAPTAIN_VERA + CAPTAIN_CATO + CAPTAIN_ARGUS resolve (ZENO).**

```bash
grep -lE "save-verdict|substrate/skills/save-verdict" substrate/CAPTAIN_VERA.md substrate/CAPTAIN_CATO.md substrate/CAPTAIN_ARGUS.md
```

**Acceptance:** all three files listed in output. Each file contains at least one reference to the new skill.

**P11 — op-disc §15.4 cross-ref to save-verdict resolves (ZENO).**

```bash
grep -nE "save-verdict|substrate/skills/save-verdict" substrate/operating-disciplines.md | grep -E "^[0-9]+"
```

**Acceptance:** at least one match in the §15.4 vicinity (line range that contains the cross-ref; ADA picks a line within §15.4's body — likely between lines 863-880 in the current source).

**P11a — Pre-existing `§5.7` cross-ref bug at `CAPTAIN_VERA.md:122` is FIXED + no other illegitimate `§5.7` cite remains in substrate canon files (ZENO; new in rev2, addresses R1 Fix-now).**

```bash
# Step 1: confirm the specific bug-site at CAPTAIN_VERA.md:122 now reads §15.4
grep -nE "UNVERIFIABLE per §15\.4" substrate/CAPTAIN_VERA.md
# Acceptance: returns line 122 with the §15.4 cite.

# Step 2: enumerate remaining §5.7 cites across substrate canon and classify them
grep -rn "§5\.7" substrate/ --include="*.md" | grep -v "^substrate/arcs/"
# Acceptance: surviving matches resolve to one of these LEGITIMATE self-refs (not the op-disc §5.7 bug):
#   - substrate/CAPTAIN_ADA.md:149 — "credential discipline §5.7" (self-ref to ADA's §5.7 about credentials)
#   - substrate/CAPTAIN_ADA.md:151 — "§5.7 (credential discipline)" (same self-ref)
#   - substrate/MAJOR_PLINY.md:212 — "CAPTAIN_VERA.md §5.7" (self-ref to VERA's §5.7 "Verification-complexity quadrant per probe" — VERA has its own §5.7, verified at substrate/CAPTAIN_VERA.md line 96)
# Any other surviving §5.7 match in non-arc-directive substrate canon = FAIL (additional bug-site needing fix).
# Note: substrate/arcs/arc-23-build-directive.md and substrate/arcs/arc-39-build-directive.md carry the same pre-existing wrong cite but are immutable arc records (out of scope per §1.0 disclosure 1).
```

**Acceptance:** Step 1 matches at line 122 with the corrected §15.4 cite; Step 2 enumerates exactly the 3 legitimate self-refs above and no others (modulo the historical arc directives which are excluded by the grep filter). Mechanically enforces the Fix-now property R1.

### §4.2 — C2 ezj probes (canon-prose grep + cross-ref resolution)

**P12 — MAJOR_PLINY.md §7.2 PRINCIPAL-intent extension prose lands (ZENO).**

```bash
grep -nE "PRINCIPAL-intent probe|stoa--ezj|category-first canonical probe sequence" substrate/MAJOR_PLINY.md | head -5
```

**Acceptance:** at least one match per of (a) "PRINCIPAL-intent probe" phrase; (b) "stoa--ezj" cross-ref; (c) "category" + "shape" + "specifics" 3-step canonical sequence keywords. Diff against pre-Arc-39 MAJOR_PLINY.md confirms the prose is new (not just a re-grep of pre-existing text).

**P13 — MAJOR_POLYBIUS.md §4.3.1 relay-side analog prose lands (ZENO).**

```bash
grep -nE "^#### 4\.3\.1 PRINCIPAL-intent probe at relay time|relay-time specialization|stoa--ezj" substrate/MAJOR_POLYBIUS.md | head -5
```

**Acceptance:** `#### 4.3.1 PRINCIPAL-intent probe at relay time` heading present (note: four hash marks for sub-subsection per M1 pick); "relay-time specialization" phrase present; "stoa--ezj" cross-ref present.

**P14 — op-disc §19.2 PRINCIPAL-intent cross-ref lands (ZENO).**

```bash
grep -nE "PRINCIPAL-intent extrapolation|stoa--ezj|four-discipline cluster" substrate/operating-disciplines.md | head -5
```

**Acceptance:** at least one match per of (a) "PRINCIPAL-intent extrapolation" phrase; (b) "stoa--ezj" cross-ref; (c) the four-discipline-cluster names (ioy / nvl / 53u / ezj).

**P15 — Cross-refs in §3.1 + §3.2 + §3.3 reciprocate (ZENO; updated in rev2 to §4.3.1).**

```bash
# PLINY.md §7.2 cites POLYBIUS §4.3.1 + op-disc §19
grep -nE "MAJOR_POLYBIUS\.md §4\.3\.1|operating-disciplines\.md §19" substrate/MAJOR_PLINY.md
# POLYBIUS.md §4.3.1 cites PLINY §7.2 + op-disc §19
grep -nE "MAJOR_PLINY\.md §7\.2|operating-disciplines\.md §19" substrate/MAJOR_POLYBIUS.md
# op-disc §19.2 cites PLINY §7.2 + POLYBIUS §4.3.1
grep -nE "MAJOR_PLINY\.md §7\.2|MAJOR_POLYBIUS\.md §4\.3\.1" substrate/operating-disciplines.md
```

**Acceptance:** all three grep blocks return at least one match each. Cross-refs resolve in all three directions (PLINY → POLYBIUS + op-disc; POLYBIUS → PLINY + op-disc; op-disc → PLINY + POLYBIUS).

### §4.3 — Universal disciplines probes

**P16 — A12 trailer on ADA + DAEDALUS commits (ZENO).**

```bash
git log --pretty='%h %s%n%(trailers:key=Co-Authored-By)' arc-39/build | head -40
```

**Acceptance:** at least one commit shows trailer `Co-Authored-By: CAPTAIN_DAEDALUS_the-stoa <captain-daedalus@the-stoa.local>` (the design rev1 commit + this rev2 commit). At least one ADA commit (after build phase) shows trailer `Co-Authored-By: CAPTAIN_ADA_the-stoa <captain-ada@the-stoa.local>`. ZENO spot-checks one of each per A12 LOCKED.

**P17 — Substrate-edit smoke-beat discipline satisfied (ZENO).**

`operating-disciplines.md` §8.4 specifies that any arc adding a new file under `substrate/skills/` MUST exercise the install.sh smoke-beat probes. P1 + P2 + P3 above are exactly those smoke beats. ZENO confirms P1-P3 ran and passed at VERA-verdict time.

**Acceptance:** VERA verdict for P1 + P2 + P3 = PASS. ZENO confirms by reading VERA's verdict artifact at `agents/verdicts/<stoa--utn>/VERA-<ts>.md`.

---

## §5 — Universal disciplines (ADA brief preamble — verbatim per MAJOR_PLINY.md §5.2)

ADA's brief MUST include the literal grounding-check enumeration. Reproduced here so ADA lifts it directly into the build:

> Ground-check every concrete example in the design against the shipped code, specifically:
> - JSON example shapes (response bodies, request bodies)
> - Function/method signatures (parameter names, types, return types)
> - Error message text (exact string match)
> - Line ranges in path:line citations
> - HTTP response codes
> - Wire-protocol constants (header names, status codes, envelope keys)
>
> If a design example contradicts the shipped code, the shipped code is canon — flag the design drift but build to ship reality.

For Arc 39 specifically, the load-bearing ground-check loci are:

- **install.sh line numbers.** The `SKILL_NAMES` array OPENS at line 142; existing entries occupy lines 143-148 (agent-author / check-substrate-updates / credential-discipline / check-bw-release / inspect-script-output / handoff-author); the new `save-verdict` entry lands at line 149 (per ARGUS R3, bare-name, no trailing comment). The skill-deploy loop is at lines ~785-799. ADA verifies the actual line numbers at build time and flags if the design's line citations are stale.
- **User-tier SKILL.md line ranges in §2.3.** The modernization table cites line numbers in `~/.claude/skills/save-verdict/SKILL.md` (10, 14, **16 [body-prose Author line, new in rev2 per M2]**, 131-132, 137, 143). ADA reads the user-tier file at build time and verifies the cited lines match the cited content; if drift, the shipped user-tier content is canon — flag and proceed.
- **MAJOR_PLINY.md §7.2 line range.** Design §3.1 cites the existing §7.2 at lines 675-683 and names the insertion locus relative to "Scope-broadening (Arc 24 / stoa--ioy)" paragraph end at line 681. ADA verifies at build time.
- **MAJOR_POLYBIUS.md §4.3 line range (updated in rev2 per M1).** Design §3.2 places the new §4.3.1 sub-subsection under existing §4.3 (Verify-then-execute). ADA verifies the §4.3 body's last line at build time and inserts the new sub-subsection between §4.3's last paragraph and the next sibling §4.4 heading.
- **op-disc §19.2 insertion locus.** Design §3.3 places the new bullet at the end of pattern 2, before pattern 3. ADA verifies the pattern-2 paragraph end at build time.
- **CAPTAIN_VERA.md line 122 bug-fix locus (new in rev2 per R1).** Design §2.1 + probe P11a cite the specific bug-site at `CAPTAIN_VERA.md:122` (the synthesis-claim row in the per-claim-probe-shape table — currently reads `UNVERIFIABLE per §5.7`, must change to `UNVERIFIABLE per §15.4`). ADA verifies the line number at build time and confirms the exact text-match for the in-place edit.
- **agent-author + check-substrate-updates SKILL.md frontmatter loci (new in rev2 per M3).** Design §2.1 specifies inserting `author: Denson Smith` after the `description:` line in each file's YAML frontmatter. ADA verifies each file's frontmatter shape matches the 4-line precedent (`--- / name / description / author / ---`) at credential-discipline / check-bw-release / inspect-script-output.

### §5.1 — §28 Co-Authored-By trailer discipline (A12 LOCKED)

Every DAEDALUS + ADA commit inside `arc-39/build` MUST carry the seat-identity trailer. The trailer format is canon per `operating-disciplines.md` §28 + `MAJOR_PLINY.md` §5.12:

- DAEDALUS commits: `Co-Authored-By: CAPTAIN_DAEDALUS_the-stoa <captain-daedalus@the-stoa.local>`
- ADA commits: `Co-Authored-By: CAPTAIN_ADA_the-stoa <captain-ada@the-stoa.local>`

Use HEREDOC commit messages to ensure verbatim trailer landing. NEVER use `-m` for commits with trailers (the trailer is part of the message body, not a separate field).

### §5.2 — A17 frontmatter discipline (IMMUTABLE)

New file `substrate/skills/save-verdict/SKILL.md` MUST carry `author: Denson Smith` in YAML frontmatter. Per CLAUDE.md global rule + the-stoa repo CLAUDE.md "Authorship attribution" section: ANY file with an `author` / `authors` / `owner` / `creator` / `maintainer` / `by` / `copyright` field MUST name Denson Smith. Precedent at `substrate/skills/handoff-author/SKILL.md` line 7 + `substrate/skills/credential-discipline/SKILL.md` line 4 + `substrate/skills/check-bw-release/SKILL.md` line 4 + `substrate/skills/inspect-script-output/SKILL.md` line 4 — 4-site verified pattern.

**Fix-now extension in rev2 per ARGUS M3 + PLINY rev2-disposition:** the existing substrate skills `substrate/skills/agent-author/SKILL.md` and `substrate/skills/check-substrate-updates/SKILL.md` are MISSING the `author: Denson Smith` frontmatter line. These are SUBSTRATE-tier (not A20-#5 blocked, which targets user-tier retroactive modernization). Per CLAUDE.md global Fix-now + op-disc §4.8, Arc 39 adds the frontmatter line to BOTH files; post-arc, 7 of 7 substrate skills carry the discipline (save-verdict is the new 7th; the 2 backfills bring the existing 6 to 6-of-6). Probe P9b mechanically enforces.

ADA reads the existing `substrate/skills/handoff-author/SKILL.md` frontmatter as the reference template and reproduces the exact `author: Denson Smith` line in the new save-verdict SKILL.md frontmatter + in the agent-author + check-substrate-updates frontmatters. ZENO mechanical-check probes P9 + P9b confirm.

### §5.3 — §5.10 signoff with live-verified state (A13 LOCKED)

Per `operating-disciplines.md` §19.6 attestation-honesty: at arc close, PLINY signs off with live-verified state, NOT dispatch-authoring SHA. Concrete probes ADA / VERA / CATO / ZENO ALL contribute to (the signoff is PLINY's, but the live-verification reads at attestation time):

```bash
# At attestation time, re-run:
git rev-parse HEAD                       # actual HEAD SHA at attestation
git log --oneline main..origin/main      # must be empty for clean state
git log --oneline origin/main..main      # must be empty
git status --porcelain                   # must be empty
```

PLINY cites the SHA returned by `git rev-parse HEAD` at attestation time in the signoff — NOT the SHA carried in the original dispatch envelope. ZENO at arc close confirms the signoff prose contains a live SHA (not the dispatch SHA `519226e` from the directive's commit ID).

### §5.4 — §5.11 paste archival self-application

Arc 39 self-applies per `operating-disciplines.md` §5.11 self-application exception. The arc directive + activation pastes archive to `substrate/arcs/arc-39/pastes/` via `git mv` at arc close. Design authorizes EITHER shape:

- **(a) ADA bundles the paste archival INTO the gauntlet build commit.** Single commit lands design + helper + install.sh wiring + canon edits + paste archival.
- **(b) PLINY does the archival post-merge.** Build commit covers design + helper + install.sh + canon edits; post-merge, PLINY runs `git mv` for the three files on main and commits directly per §18 housekeeping exception.

Either shape satisfies §5.11. ADA picks at build time based on what fits cleanly in the diff; if (a) makes the diff sprawl, prefer (b). The design does not gate.

### §5.5 — A22 CATO MANDATORY (reaffirm)

CATO is MANDATORY for Arc 39 per A22 LOCKED. Multi-arc sequence to Pass 9 validate-spec means cumulative craft scrutiny matters; Arc 39 introduces Python-authoring shape (different defect class than canon-edit arcs); extra craft scrutiny justified. PLINY MUST dispatch CATO during Phase 3 verify; CATO PASS is a gate for ship.

---

## §6 — Out-of-scope (A20 hard-locks)

These are NOT in Arc 39 scope. If pressure surfaces to do any of them during build, SURFACE as PRINCIPAL-gate finding per `operating-disciplines.md` §25 rather than absorbing silently:

1. **Promoting `copy-artifact` or `transcribe-bw-to-disk` to substrate.** sp1 scope; A2 α pick keeps them out.
2. **Auto-validation of arbitrary verdict bodies against JSONSchema.** Arc 23 A6 LOCK — free-form prose validation, caller-side enforcement.
3. **Refactoring the existing PASS / FAIL / NEEDS-REVISIONS verdict path.** Out per utn ticket body.
4. **Widening ezj canon to non-PLINY / non-POLYBIUS seats.** The discipline is dispatch-time + relay-time specific; CAPTAIN-side extensions are future arc work.
5. **Retroactive modernization of OTHER user-tier obsolete skills.** sp1 scope. Note: this hard-lock targets USER-tier only; substrate-tier author-frontmatter Fix-now (agent-author + check-substrate-updates) is IN scope in rev2 per CLAUDE.md global Fix-now + ARGUS M3 surface + PLINY rev2-disposition (the substrate-tier defect is structurally different from the user-tier obsolescence A20 #5 targets — see §2.1 table + §5.2).
6. **The MCP-confabulation 5th subtype** named at 2026-05-13T21:25:30Z on stoa--ezj. Surface as future ticket; do not absorb into Arc 39 ezj canon. Per §1.0 disclosure 4.
7. **Promoting `_lib/byte_copy.py` to `substrate/skills/_lib/`** (shared location). Deferred to sp1 per A2 α.
8. **Fixing the historical arc-directive §5.7 cites at `substrate/arcs/arc-23-build-directive.md` lines 37, 185 + `substrate/arcs/arc-39-build-directive.md` lines 28, 69.** Arc directives are immutable historical records — they document the arc as authored, including the bug propagation. The Fix-now applies to LIVE substrate canon files (per §2.1 table + R1 disposition); historical arc records remain as authored. Per §1.0 disclosure 1.

---

## §7 — Self-assessed weak points (per CAPTAIN_DAEDALUS §6.2)

Honest list. ARGUS reads for what I missed.

1. **R1 fix-now scope-widening was authorized by PLINY rev2-disposition but the scope-extension surface itself is a self-discipline test.** I'm extending Arc 39 by one line (CAPTAIN_VERA.md:122) on PLINY's authorization. If a future ARGUS critique reads the Fix-now extension as A20-violating ("the directive locks scope and the design rev2 unilaterally extends it"), the defense is the explicit PLINY rev2-disposition + the CLAUDE.md global Fix-now rule + op-disc §4.8 that overrides directive scope-locks. Documenting the authorization chain here so a future audit doesn't have to reconstruct it. Per ARGUS R1 + PLINY ack.

2. **MAJOR_POLYBIUS.md §4.3.1 sub-subsection establishes a new nesting pattern.** §4.x is currently flat; rev2 introduces the first §4.X.Y sub-subsection. The pattern itself is justified (M1 PLINY weak lean: discipline-relationship structure expressed by nesting), but a future seat looking for `### 4.10` will not find sub-subsections naturally — they'll need to skim the §4.3 body. Mitigation: the explicit `#### 4.3.1` heading + ToC discoverability + the cross-ref discipline (all references to the sub-subsection cite `§4.3.1` exactly) make the locus grep-able. If a future arc finds the nesting awkward, it can be flattened back to a §4.X peer in a deliberate retro.

3. **`_save_verdict.py` should be importable as a module OR invokable as script** is an A20-adjacent design call I made unilaterally. The user-tier SKILL.md spec is invocation-only. I added "importable as module" capability for future call-sites; if ARGUS reads this as scope-creep, I'd cut it (3 lines saved). Defense: future-proofing has near-zero cost (the `if __name__ == "__main__":` idiom is Python stdlib boilerplate); cost is one line of design prose and ~3 lines of helper code. The R2 PLINY-decision LOCKED the path-invocation canon, so the module-importability is now an explicit side-benefit, not a contract competitor.

4. **The "lieutenant" terminology decision (preserve, not modernize) rests on an internal-consistency argument I did not stress-test.** ARGUS rev1 NF1 verified lieutenant survives across substrate canon (install.sh 3 sites, MAJOR_PLINY.md, MAJOR_POLYBIUS.md, agent-author/SKILL.md 5 sites including the `lieutenant_skill` enum value, arc-9/12/13/17/17.1 directives). Live substrate canon. Risk discharged by ARGUS in rev1; reproducing here for record.

5. **install.sh `--dry-run` exit-code behavior is assumed-but-unprobed.** ARGUS rev1 NF2 verified empirically via `bash substrate/install.sh --dry-run --target user` returns exit 0; dry-run path in install.sh 785-800 is pure echo. Risk discharged by ARGUS in rev1; reproducing here for record.

---

## §8 — Sequencing + handoff to ARGUS (rev2 audit)

This rev2 design ships as a single commit on `arc-39/build` carrying the Co-Authored-By trailer. PLINY dispatches ARGUS for a rev2 audit against the deltas (R1+R2+R3 load-bearing + M1+M2+M3 minor). ARGUS reads:

1. §1.0 disclosure 1 (R1 Fix-now scope extension + authorization chain)
2. §2.1 file-modification table (new rows: CAPTAIN_VERA.md:122 fix, agent-author + check-substrate-updates frontmatter Fix-now)
3. §2.4 R2 invocation-contract LOCKED paragraph (sys.path canon-establishing)
4. §2.6 install.sh wiring (bare `save-verdict` entry, line 149)
5. §3.2 §4.3.1 sub-subsection (M1 pick + adjacency rationale)
6. §2.3 modernization table row for line-16 body-prose Author line drop (M2)
7. §4.1 probes P9b + P11a (new in rev2, mechanically enforce M3 + R1 Fix-now properties)
8. §5.2 frontmatter discipline Fix-now extension (M3 rationale)
9. §6 hard-locks #5 clarification + #8 historical-arc-directive carve-out (R1 scope-bound)
10. §7 self-assessed weak points (rev2 list — items 1 + 2 are new; 3-5 retained from rev1)

After ARGUS rev2 PASS, PLINY dispatches ADA for build per §2.1 table + §3.1-§3.3 prose. ADA invokes the ADA brief preamble from §5 verbatim. Build delivers all files in §2.1 + canon edits in §3.1-§3.3 + §2.1 Fix-now rows (CAPTAIN_VERA.md:122 + agent-author + check-substrate-updates frontmatters). Then VERA + CATO + ZENO per gauntlet. A22 CATO MANDATORY.

After Phase 3 clean (VERA + CATO + ZENO all PASS), PLINY ships per Phase 4 (squash-merge with trailer preservation; cleanup; A18 source-ticket closure + `[for: user-tier-polybius]` tag on stoa--utn; A13 §5.10 signoff with live-verified state; A11 §5.11 paste archival).

Done.
