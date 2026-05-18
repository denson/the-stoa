# Arc 39 design — save-verdict promotion + PRINCIPAL-intent probe canon (2 bundled candidates)

**Author seat:** CAPTAIN_DAEDALUS_the-stoa
**Branch:** `arc-39/build` (worktree at `.claude/worktrees/arc-39-build/`)
**Work-units:** C1 stoa--utn (save-verdict skill promotion to substrate) + C2 stoa--ezj (PRINCIPAL-intent probe discipline canon)
**Directive (LOCKED):** `substrate/arcs/arc-39-build-directive.md` (A1-A22 LOCKED; A2/A4/A6/A9 DAEDALUS-discretion)
**Operating mode:** AUTONOMOUS (peer = MAJOR_PLINY_the-stoa via stoa--utn coordination ticket; user-tier POLYBIUS via QA at arc close per A18)
**Status:** DAEDALUS draft for ARGUS audit.

---

## §1.0 — Brief (restatement-gate per CAPTAIN_DAEDALUS §6.1)

Arc 39 is Pass 5 of the SPECIFICATION.md §13 workplan and bundles two P3 candidates per §13.6: **C1 stoa--utn** promotes the user-tier `save-verdict` skill to substrate with the Python helpers that the user-tier SKILL.md procedure invokes against vapor (no `_save_verdict.py` and no `_lib/byte_copy.py` exist on disk; Arc 23 ratified Option A — extend the user-tier SKILL.md schema only — and deferred substrate promotion to this ticket); **C2 stoa--ezj** lands the PRINCIPAL-intent probe discipline canon by extending `MAJOR_PLINY.md` §7.2 (verify-then-execute), adding a POLYBIUS-side relay-discipline analog at `MAJOR_POLYBIUS.md`, and cross-referencing `operating-disciplines.md` §19 (confabulation) — with the 2026-05-13 category-before-option refinement folded in. Both candidates ship in one gauntlet under A1 LOCKED; each candidate's source ticket closes on ship with cross-ref + audit comment per A18.

**Restatement-gate (§6.1) imported-assumption disclosure:**

1. **The directive's "op-disc §5.7 verdict discussion" reference does not resolve to an existing locus.** `operating-disciplines.md` §5 is the single-paragraph "Suppress plausible-source citation without verification" — no §5.7 subsection, no verdict discussion in §5. The substantive home for the verdict-shape vocabulary the save-verdict skill enforces is `operating-disciplines.md` §15 (verification-complexity awareness), specifically **§15.4** (the two new verdict shapes — INCOMPLETE + UNVERIFIABLE). I'm treating "op-disc §5.7" as a typo for §15.4 and resolving the cross-ref there. ARGUS should sanity-check this resolution; if PLINY's intent was a different locus, surface as `[for: daedalus-the-stoa]` and I'll rev.

2. **The user-tier SKILL.md's "lieutenant" / "request bead" / "reply bead" / "PULSE_REVIEW" terminology is mostly compatible with the-stoa taxonomy.** "lieutenant" survives as the substrate-canonical name for the SKILL tier (verified at `substrate/skills/agent-author/SKILL.md` line 36 + `substrate/MAJOR_PLINY.md` line 564); I retain it. "Officer" generalizes to the verdict-saving CAPTAINs (ARGUS / VERA / CATO) and I will modernize the prose to use "CAPTAIN" where the user-tier text said "Officer." "PULSE_REVIEW" is a gauntlet-era name with no in-substrate referent today; I will rewrite the affected sentence to name the discipline rather than a non-existent skill (per A4 ii). "request bead" / "reply bead" survive as the bw-comment vocabulary and I retain them.

3. **A9 pick is ε (fold-in WITH explicit canonical-probe-sequence).** The user-tier weak lean is γ-or-ε; PRINCIPAL's 2026-05-13T03:08:13Z comment on stoa--ezj already spells the 3-step canonical sequence (category → shape-within-category → specifics-within-shape) in clean enumeration. ε is the cleaner canonical phrasing — it lands the sequence as numbered steps rather than embedded prose. Cost is one extra paragraph; benefit is grep-able structure for future seats.

4. **The "MCP-confabulation fifth-subtype" anchor (2026-05-13T21:25:30Z on stoa--ezj) is OUT OF SCOPE for Arc 39.** That comment proposes extending the discipline cluster from 4 disciplines to 5 by adding "verify documentation against empirical reality before authoring artifacts that assume documented capability works." Ezj is currently scoped to the 4-discipline cluster (ioy / nvl / 53u / ezj). Adding the 5th MCP-subtype would (a) widen ezj canon beyond what the directive A20 hard-locks, and (b) require its own empirical anchoring + 4-discipline-cluster reframing. Surface for separate future ticket; do not absorb into Arc 39.

None of (1)-(4) exceed DAEDALUS discretion per `operating-disciplines.md` §25.3 BLOCK semantics — they are calibration sub-decisions within the directive's locked envelope. PRINCIPAL would not pull workflow back through PRINCIPAL-gate for any of them. Restatement converges with the brief; no `refused` route.

---

## §1.1 — DAEDALUS sub-decision summary (A2 / A4 / A6 / A9)

| ID | Sub-decision | DAEDALUS pick | Aligns with user-tier lean? | One-line rationale |
|---|---|---|---|---|
| A2 | `_lib/byte_copy.py` scope | **α — single-skill private** at `substrate/skills/save-verdict/_lib/byte_copy.py` | ✅ yes | User-tier SKILL.md "Preservation discipline" already names cross-skill share with COPY_ARTIFACT + TRANSCRIBE_BW_TO_DISK; A20 hard-locks both out of Arc 39 scope; β would create an unused-shared-lib state; α keeps Arc 39 tight + lets sp1 refactor with full N=3 consumer context. |
| A4 | SKILL.md modernization | **ii — lift-and-modernize** at promotion time | ✅ yes | Modernizing at promotion avoids a second touch later AND removes save-verdict from sp1's scope. Modernization is targeted (PULSE_REVIEW reference + "Officer" → CAPTAIN + verdict-path example reframed for the-stoa's `agents/verdicts/<ticket>/` convention + obsolete 2026-05-12 executable-enforcement caveat block removed). |
| A6 | utn substrate-canon cross-refs | **CAPTAIN_VERA + CAPTAIN_CATO + CAPTAIN_ARGUS + `operating-disciplines.md` §15.4** | ✅ yes (with §5.7 → §15.4 resolution per §1.0 disclosure 1) | The verdict-saving seats are the verdict-class CAPTAINs (ARGUS plan-critic / VERA falsifier / CATO craft-review); ADA / DAEDALUS / ZENO do NOT save verdicts (they consume verdicts or author other artifact classes). §15.4 is the substantive home for the verdict-shape vocabulary save-verdict enforces. |
| A9 | ezj category-before-option fold-in | **ε — fold-in WITH explicit canonical-probe-sequence** | ✅ yes (weakly leans ε) | PRINCIPAL's 2026-05-13 comment already spells the 3-step sequence cleanly; ε lifts the sequence verbatim as numbered canon rather than embedding it as prose. Cost is one extra paragraph; benefit is grep-able structure. |

**Substance disagreements with directive or user-tier leans:** none. All four picks align. No PRINCIPAL-gate (§25.3 BLOCK) surface engaged. ARGUS is the right next reader.

---

## §2 — C1: save-verdict skill promotion (stoa--utn)

### §2.1 — Files this candidate creates / modifies

**New directory tree under `substrate/skills/save-verdict/`:**

| Path | Purpose | Author source |
|---|---|---|
| `substrate/skills/save-verdict/SKILL.md` | Prose canon for the skill (procedure, input contract, failure modes). Lift-and-modernize from `~/.claude/skills/save-verdict/SKILL.md` per A4 ii. MUST carry `author: Denson Smith` YAML frontmatter per A17. | User-tier SKILL.md (143 lines) modernized per §2.3 below. |
| `substrate/skills/save-verdict/_save_verdict.py` | Python helper implementing the SKILL.md procedure steps 1-9. ~150-250 LOC. | NEW authoring per §2.4 below; spec'd in SKILL.md prose at user-tier (steps 1-9 + failure modes + exit codes). |
| `substrate/skills/save-verdict/_lib/byte_copy.py` | `write_with_verify` primitive (sha256 round-trip write). ~30-60 LOC. Private to save-verdict per A2 α; cross-skill share deferred to sp1. | NEW authoring per §2.5 below; spec'd in user-tier SKILL.md "Preservation discipline" section. |

**Files modified:**

| Path | Change | Reason |
|---|---|---|
| `substrate/install.sh` (line ~142, `SKILL_NAMES` array) | Append `save-verdict` to the array | A5 LOCKED — wires the new skill into the install loop. The skill-deploy loop at lines 785-799 already handles nested `_lib/` subdirectories cleanly via `cp -R "$src_skill"/. "$dest_skill"/`. |
| `substrate/CAPTAIN_VERA.md` | Cross-ref insertion at the verdict-emit section | A6 — VERA emits PASS / FAIL / NEEDS-REVISIONS / INCOMPLETE / UNVERIFIABLE verdicts; cite the canonical save-verdict skill at the seat that emits them. |
| `substrate/CAPTAIN_CATO.md` | Cross-ref insertion at the verdict-emit section | A6 — same rationale at the craft-review seat. |
| `substrate/CAPTAIN_ARGUS.md` | Cross-ref insertion at the verdict-emit section | A6 — same rationale at the plan-critic seat. |
| `substrate/operating-disciplines.md` §15.4 | One-paragraph cross-ref to the new save-verdict skill as the canonical write-path for INCOMPLETE + UNVERIFIABLE verdict bodies | A6 — §15.4 introduces the two new verdict shapes; the cross-ref tells readers HOW to write them to disk canonically. Resolves the directive's "op-disc §5.7" reference per §1.0 disclosure 1. |

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
| Line 137 | "...the aggregation that picks 'which is the verdict-of-record' is PULSE_REVIEW or the caller's judgment." | "...the aggregation that picks 'which is the verdict-of-record' is the caller's judgment (PLINY at arc close; POLYBIUS at retrospective)." | PULSE_REVIEW reference dropped per above; canonical aggregators named explicitly. |
| Lines 131-132 (entire "Caveat on executable enforcement (2026-05-12)" block) | "**Caveat on executable enforcement (2026-05-12).** The validation behavior above is canon-establishing in this SKILL.md prose. The executable Python helper (`_save_verdict.py`) referenced in the **Procedure** section is not yet authored on disk; the shape-conformance exit-4 paths above are spec for the future helper, not currently executable. A follow-up substrate ticket (per Arc 23 design §10.1) will author the helper and promote both SKILL.md and helper to `substrate/skills/save-verdict/`, exercising the `operating-disciplines.md` §8.4 install.sh smoke beat against the promotion." | **DELETE the entire block.** | Arc 39 IS the follow-up ticket the caveat anticipates; once the helper exists on disk and is deployed, the caveat is obsolete. |
| Line 143 (Preservation discipline section) | "Source-of-truth at `skills/save-verdict/SKILL.md` + `skills/save-verdict/_save_verdict.py`. Shares `skills/_lib/byte_copy.py` with COPY_ARTIFACT and TRANSCRIBE_BW_TO_DISK." | "Source-of-truth at `substrate/skills/save-verdict/SKILL.md` + `substrate/skills/save-verdict/_save_verdict.py` + `substrate/skills/save-verdict/_lib/byte_copy.py`. Deployed at all 3 install tiers (user / project / subproject) via `substrate/install.sh` `SKILL_NAMES` array. Cross-skill share of `_lib/byte_copy.py` with COPY_ARTIFACT + TRANSCRIBE_BW_TO_DISK deferred to stoa--sp1 per Arc 39 directive A2 α + A20." | Reflects substrate paths post-promotion; documents the deferred share decision. |
| YAML frontmatter (lines 1-4) | `---\nname: save-verdict\ndescription: "..."\n---` | `---\nname: save-verdict\ndescription: "..."\nauthor: Denson Smith\n---` | A17 IMMUTABLE — frontmatter `author: Denson Smith` MUST be present per CLAUDE.md global rule. Matches precedent at `substrate/skills/handoff-author/SKILL.md` line 7. |

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
- Per project CLAUDE.md `op-disc §13` Windows note: set `PYTHONUTF8=1` is required for Python invocations on Windows; the skill assumes the caller's environment respects this (the SKILL.md procedure section already documents the env-var contract — no skill-side workaround needed).
- Importable AS a module: `from save_verdict import main` should work for callers that prefer in-process invocation over subprocess. Module-vs-script flexibility costs ~3 lines (the `if __name__ == "__main__": sys.exit(main())` idiom); benefit is testability + future call-sites that don't want subprocess overhead.
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
- Per A2 α: file is PRIVATE to save-verdict (under `substrate/skills/save-verdict/_lib/`, NOT under `substrate/skills/_lib/`). The `_lib/` directory + `__init__.py` (empty) make this a proper Python package for `from _lib.byte_copy import write_with_verify` style imports from sibling `_save_verdict.py`.
- Empty `__init__.py` at `substrate/skills/save-verdict/_lib/__init__.py` is the simplest import path. Alternative: relative imports (`from ._lib.byte_copy import …`); requires `_save_verdict.py` to be run as a module (`python -m save_verdict`) which complicates the SKILL.md invocation. Stick with `_lib/__init__.py` + `sys.path` manipulation in `_save_verdict.py` (1-liner: `sys.path.insert(0, str(pathlib.Path(__file__).parent))`).

### §2.6 — install.sh wiring (A5 LOCKED)

Single edit at `substrate/install.sh` line ~142 in the `SKILL_NAMES=( … )` array. After the existing `handoff-author` entry, append `save-verdict`:

```sh
SKILL_NAMES=(
  agent-author
  check-substrate-updates
  credential-discipline
  check-bw-release
  inspect-script-output
  handoff-author
  save-verdict        # NEW Arc 39 (stoa--utn)
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

Cross-refs: `operating-disciplines.md` §19 (confabulation — PRINCIPAL-intent extrapolation is a confabulation subtype); `MAJOR_POLYBIUS.md` §[N] (relay-side analog — when relaying work items from PLINY to PRINCIPAL, POLYBIUS surfaces unprobed-intent gaps explicitly); four-discipline-cluster siblings `stoa--ioy` (general "uncertain, checking"), `stoa--nvl` (verify-tool-availability), `stoa--53u` (idle-state retrospective-narrative confabulation).
```

**Substitution note for the `§[N]` placeholder:** ADA substitutes the actual section number assigned in §3.2 below.

### §3.2 — MAJOR_POLYBIUS.md relay-side analog

**File:** `substrate/MAJOR_POLYBIUS.md`
**Section:** new subsection `### 4.9 PRINCIPAL-intent probe at relay time` under existing `## 4. Disciplines` (currently runs §4.1-§4.8, ending at line 119)
**Position:** appended after existing §4.8 (Fix-now), BEFORE the `## 5. Onboarding flow` section heading at line 141.
**Adjacency rationale:** §4.3 (Verify-then-execute) is POLYBIUS's verify-then-execute home; §4.9 is the relay-time specialization (the moment POLYBIUS relays a PLINY-authored work item back to PRINCIPAL is the canonical surface where unprobed-intent gaps get caught). Sibling to §4.3 in concept; placed at section-end so existing §4.1-§4.8 numbering is unbroken.

**Exact prose to add (canon-grade; ADA lifts verbatim):**

```markdown
### 4.9 PRINCIPAL-intent probe at relay time (`stoa--ezj`)

When relaying a work item PLINY has queued back to PRINCIPAL (for ratification, for the next-step disposition queue, for any decision PLINY has surfaced), check the work item for unprobed-intent gaps BEFORE the relay. If the work item depends on an upstream PRINCIPAL-intent decision that PLINY did not explicitly probe (deliverable shape, target audience, success criteria, scope boundaries), surface the gap explicitly in the relay rather than letting it propagate.

This is the relay-time analog of PLINY's `MAJOR_PLINY.md` §7.2 PRINCIPAL-intent extension. PLINY catches the gap at queuing time; POLYBIUS catches it at relay time. Both catches are necessary — PLINY's catch prevents the queued work from being designed on inferred-intent; POLYBIUS's catch prevents an inferred-intent work item from reaching PRINCIPAL framed as a settled decision.

**The canonical probe sequence (3 steps, category-first; per `MAJOR_PLINY.md` §7.2 PRINCIPAL-intent extension):**

1. **Category:** what SHAPE OF THING is this? (artifact, infrastructure, skill, doc, service, agent-loadable context, etc.)
2. **Shape-within-category:** now that we know it's [category], what shape?
3. **Specifics-within-shape:** now that we know it's a [shape], what are the substantive details?

When relaying a work item that names an option-set without first probing the category, the relay defaults to inheriting PLINY's category-assumption — which may be wrong. Probe category FIRST.

Empirical anchor: 2026-05-13 — when POLYBIUS asked PRINCIPAL to pin Q1 (deliverable shape) for a downstream work item, POLYBIUS offered four options: live walkthrough / recorded video / written doc / slide deck. PRINCIPAL selected "live walkthrough." Then PRINCIPAL clarified: the actual answer was a fifth option POLYBIUS didn't surface — "self-serve agent-testable demo where the user points their own agent at the corpus." All four options POLYBIUS offered were in the "human watches a presentation" category. The actual answer was in a different category entirely ("user actively drives an agent"). Substrate ticket: `stoa--ezj` (2026-05-13T03:08:13Z comment, captured by POLYBIUS as self-diagnosis).

Cross-refs: `MAJOR_PLINY.md` §7.2 (queuing-time analog); `operating-disciplines.md` §19 (confabulation — PRINCIPAL-intent extrapolation is a confabulation subtype); four-discipline-cluster siblings `stoa--ioy` / `stoa--nvl` / `stoa--53u`.
```

**Substitution note:** the `§[N]` placeholder in §3.1's MAJOR_PLINY.md insertion gets substituted with `§4.9` (the section number this candidate lands).

### §3.3 — operating-disciplines.md §19 cross-ref

**File:** `substrate/operating-disciplines.md`
**Section:** existing §19 (Confabulation-under-uncertainty discipline, lines 1077-1228)
**Insertion locus:** new bullet at the end of §19.2's "Three application patterns" — augmenting the "**2. State-vs-claim mismatch.**" pattern with a cross-ref to the PRINCIPAL-intent specialization at PLINY §7.2 + POLYBIUS §4.9.
**Exact insertion:** at the end of §19.2's pattern-2 paragraph (currently at line 1094, immediately before the "**3. Unfamiliar territory.**" bullet at line 1096).

**Exact prose to add (canon-grade; ADA lifts verbatim, appending to the end of §19.2 pattern 2 — the existing paragraph ends with "...from any source." at line 1094):**

```markdown

**PRINCIPAL-intent extrapolation as a state-vs-claim sub-pattern (Arc 39 / `stoa--ezj`).** When the work item you are about to queue or design depends on an upstream PRINCIPAL-intent decision that has not been probed, the inferred intent is a CLAIM you are about to act on without verification. The verification action is to probe PRINCIPAL explicitly rather than queuing on inferred intent. The category-first canonical probe sequence (3 steps: category → shape-within-category → specifics-within-shape) is documented at `MAJOR_PLINY.md` §7.2 (queuing-time application) and `MAJOR_POLYBIUS.md` §4.9 (relay-time application). PRINCIPAL-intent extrapolation joins the four-discipline cluster around "probe ground truth before designing on top of inferred state" — tool-state (`stoa--nvl`), retrospective-state (`stoa--53u`), PRINCIPAL-intent-state (`stoa--ezj`), and the general "uncertain, checking" parent (`stoa--ioy`).
```

### §3.4 — N=1 provenance + canon-promotion gate

Per `operating-disciplines.md` §6.7.1 + `MAJOR_POLYBIUS.md` §15 honest-scope: PRINCIPAL articulated the PRINCIPAL-intent probe discipline 2026-05-13 (project-direction authority) and the category-before-option refinement same day. §6.7.1 does not carve out a "PRINCIPAL-declaration shortcut" — the honest reading: this discipline enters substrate canon off-gate on PRINCIPAL's project-direction authority + the empirical anchor, with future-evidence-accretion against the §6.7.1 gate still required for promotion to "structural lesson" status. Same N=1 framing as Arc 35's §28.7, Arc 32's §19.6.4, Arc 37's §19.7, and the existing §19.6 itself.

The MAJOR_PLINY.md §7.2 extension carries the empirical anchor in the prose; the MAJOR_POLYBIUS.md §4.9 carries it from the relay-side; the op-disc §19.2 cross-ref carries the four-discipline-cluster framing. The provenance is internally consistent across all three insertion sites; ARGUS should sanity-check the cross-refs resolve in all three directions.

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

**P9 — A17 frontmatter check: `author: Denso Smith` present in deployed SKILL.md (ZENO).**

```bash
grep -E "^author: Denson Smith$" substrate/skills/save-verdict/SKILL.md && echo "frontmatter OK"
```

**Acceptance:** match count = 1; "frontmatter OK" printed.

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

### §4.2 — C2 ezj probes (canon-prose grep + cross-ref resolution)

**P12 — MAJOR_PLINY.md §7.2 PRINCIPAL-intent extension prose lands (ZENO).**

```bash
grep -nE "PRINCIPAL-intent probe|stoa--ezj|category-first canonical probe sequence" substrate/MAJOR_PLINY.md | head -5
```

**Acceptance:** at least one match per of (a) "PRINCIPAL-intent probe" phrase; (b) "stoa--ezj" cross-ref; (c) "category" + "shape" + "specifics" 3-step canonical sequence keywords. Diff against pre-Arc-39 MAJOR_PLINY.md confirms the prose is new (not just a re-grep of pre-existing text).

**P13 — MAJOR_POLYBIUS.md §4.9 relay-side analog prose lands (ZENO).**

```bash
grep -nE "^### 4\.9 PRINCIPAL-intent probe at relay time|relay-time analog|stoa--ezj" substrate/MAJOR_POLYBIUS.md | head -5
```

**Acceptance:** `### 4.9 PRINCIPAL-intent probe at relay time` heading present; "relay-time analog" phrase present; "stoa--ezj" cross-ref present.

**P14 — op-disc §19.2 PRINCIPAL-intent cross-ref lands (ZENO).**

```bash
grep -nE "PRINCIPAL-intent extrapolation|stoa--ezj|four-discipline cluster" substrate/operating-disciplines.md | head -5
```

**Acceptance:** at least one match per of (a) "PRINCIPAL-intent extrapolation" phrase; (b) "stoa--ezj" cross-ref; (c) the four-discipline-cluster names (ioy / nvl / 53u / ezj).

**P15 — Cross-refs in §3.1 + §3.2 + §3.3 reciprocate (ZENO).**

```bash
# PLINY.md §7.2 cites POLYBIUS §4.9 + op-disc §19
grep -nE "MAJOR_POLYBIUS\.md §4\.9|operating-disciplines\.md §19" substrate/MAJOR_PLINY.md
# POLYBIUS.md §4.9 cites PLINY §7.2 + op-disc §19
grep -nE "MAJOR_PLINY\.md §7\.2|operating-disciplines\.md §19" substrate/MAJOR_POLYBIUS.md
# op-disc §19.2 cites PLINY §7.2 + POLYBIUS §4.9
grep -nE "MAJOR_PLINY\.md §7\.2|MAJOR_POLYBIUS\.md §4\.9" substrate/operating-disciplines.md
```

**Acceptance:** all three grep blocks return at least one match each. Cross-refs resolve in all three directions (PLINY → POLYBIUS + op-disc; POLYBIUS → PLINY + op-disc; op-disc → PLINY + POLYBIUS).

### §4.3 — Universal disciplines probes

**P16 — A12 trailer on ADA + DAEDALUS commits (ZENO).**

```bash
git log --pretty='%h %s%n%(trailers:key=Co-Authored-By)' arc-39/build | head -40
```

**Acceptance:** at least one commit shows trailer `Co-Authored-By: CAPTAIN_DAEDALUS_the-stoa <captain-daedalus@the-stoa.local>` (this design commit). At least one ADA commit (after build phase) shows trailer `Co-Authored-By: CAPTAIN_ADA_the-stoa <captain-ada@the-stoa.local>`. ZENO spot-checks one of each per A12 LOCKED.

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

- **install.sh line numbers.** The `SKILL_NAMES` array is at line ~142 in the current source; the skill-deploy loop is at lines ~785-799. ADA verifies the actual line numbers at build time and flags if the design's line citations are stale.
- **User-tier SKILL.md line ranges in §2.3.** The modernization table cites line numbers in `~/.claude/skills/save-verdict/SKILL.md` (10, 14, 131-132, 137, 143). ADA reads the user-tier file at build time and verifies the cited lines match the cited content; if drift, the shipped user-tier content is canon — flag and proceed.
- **MAJOR_PLINY.md §7.2 line range.** Design §3.1 cites the existing §7.2 at lines 675-683 and names the insertion locus relative to "Scope-broadening (Arc 24 / stoa--ioy)" paragraph end at line 681. ADA verifies at build time.
- **MAJOR_POLYBIUS.md §4.8 line.** Design §3.2 places the new §4.9 immediately after existing §4.8 (Fix-now). ADA verifies §4.8 is the LAST §4.x subsection at build time.
- **op-disc §19.2 insertion locus.** Design §3.3 places the new bullet at the end of pattern 2, before pattern 3. ADA verifies the pattern-2 paragraph end at build time.

### §5.1 — §28 Co-Authored-By trailer discipline (A12 LOCKED)

Every DAEDALUS + ADA commit inside `arc-39/build` MUST carry the seat-identity trailer. The trailer format is canon per `operating-disciplines.md` §28 + `MAJOR_PLINY.md` §5.12:

- DAEDALUS commits: `Co-Authored-By: CAPTAIN_DAEDALUS_the-stoa <captain-daedalus@the-stoa.local>`
- ADA commits: `Co-Authored-By: CAPTAIN_ADA_the-stoa <captain-ada@the-stoa.local>`

Use HEREDOC commit messages to ensure verbatim trailer landing. NEVER use `-m` for commits with trailers (the trailer is part of the message body, not a separate field).

### §5.2 — A17 frontmatter discipline (IMMUTABLE)

New file `substrate/skills/save-verdict/SKILL.md` MUST carry `author: Denson Smith` in YAML frontmatter. Per CLAUDE.md global rule + the-stoa repo CLAUDE.md "Authorship attribution" section: ANY file with an `author` / `authors` / `owner` / `creator` / `maintainer` / `by` / `copyright` field MUST name Denson Smith. Precedent at `substrate/skills/handoff-author/SKILL.md` line 7 — verified pattern.

ADA reads the existing `substrate/skills/handoff-author/SKILL.md` frontmatter as the template and reproduces the exact `author: Denson Smith` line in the new SKILL.md frontmatter. ZENO mechanical-check probe P9 confirms.

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
5. **Retroactive modernization of OTHER user-tier obsolete skills.** sp1 scope.
6. **The MCP-confabulation 5th subtype** named at 2026-05-13T21:25:30Z on stoa--ezj. Surface as future ticket; do not absorb into Arc 39 ezj canon. Per §1.0 disclosure 4.
7. **Promoting `_lib/byte_copy.py` to `substrate/skills/_lib/`** (shared location). Deferred to sp1 per A2 α.

---

## §7 — Self-assessed weak points (per CAPTAIN_DAEDALUS §6.2)

Honest list. ARGUS reads for what I missed.

1. **Python `_save_verdict.py` import discipline for `_lib/byte_copy.py` is untested-against-deployment.** I spec'd `sys.path.insert(0, str(pathlib.Path(__file__).parent))` so `from _lib.byte_copy import write_with_verify` works when invoked as a script. The alternative (relative imports + `python -m`) is cleaner Python idiom but complicates the SKILL.md `python skills/save-verdict/_save_verdict.py …` invocation. My pick (sys.path manipulation) is functional but slightly ugly; ARGUS may flag as code-smell vs. a cleaner alternative. Defense: substrate skills are invoked-as-scripts canonically; sys.path manipulation is the simplest mechanism that preserves the invocation shape. If ARGUS prefers `python -m`, I can rev — but SKILL.md prose would need a parallel update to match.

2. **install.sh `--dry-run` exit-code behavior is assumed-but-unprobed.** P1-P3 grep stdout for the `save-verdict` string; I assume dry-run exits 0 on success. If install.sh dry-run exits non-zero (e.g., for any deploy plan warning), the grep PASS may mask a structural FAIL. ARGUS should sanity-check whether install.sh dry-run has any non-zero exit conditions I should be guarding against. Defense: reading install.sh lines 785-799, the dry-run path is pure `echo` — no failure conditions until the actual `cp -R` which is gated by `DRY_RUN -ne 1`. Should exit 0 cleanly.

3. **`_save_verdict.py` should be importable as a module OR invokable as script** is an A20-adjacent design call I made unilaterally. The user-tier SKILL.md spec is invocation-only. I added "importable as module" capability for future call-sites; if ARGUS reads this as scope-creep, I'd cut it (3 lines saved). Defense: future-proofing has near-zero cost (the `if __name__ == "__main__":` idiom is Python stdlib boilerplate); cost is one line of design prose and ~3 lines of helper code.

4. **The "lieutenant" terminology decision (preserve, not modernize) rests on an internal-consistency argument I did not stress-test.** I verified "lieutenant" survives at `substrate/skills/agent-author/SKILL.md` + `substrate/MAJOR_PLINY.md`, but I did not check whether "lieutenant" appears with a DIFFERENT semantics elsewhere in substrate (e.g., as a deprecated term being phased out). ARGUS should grep all substrate role files + skills + operating-disciplines.md for "lieutenant" usage and confirm my retain-decision aligns with substrate-wide canon. If lieutenant is being deprecated and I missed the signal, the A4 ii lift would propagate a deprecating term.

5. **The op-disc "§5.7 → §15.4" cross-ref resolution rests on my interpretation of the directive's typo.** I'm 90% confident the intent was §15.4 (the substantive verdict-shape locus); 10% chance the directive author had a different locus in mind I didn't surface. ARGUS should sanity-check; if my resolution is wrong, the design's §2.1 + §4 P11 probe both need correction.

6. **MAJOR_POLYBIUS.md §4.9 placement (after §4.8, before §5 "Onboarding flow") creates a new subsection in a section whose existing 8 subsections cluster topically.** §4.1-§4.8 cover the named disciplines; §4.9 (PRINCIPAL-intent probe at relay time) is a §4.3 sibling-by-concept (both are verify-then-execute applications at POLYBIUS's seat). I picked sequence-numbering (§4.9 appended) over thematic grouping (§4.3.1 as a sub-subsection) because: (a) §4.3 is currently flat with no subsections, so creating §4.3.1 would establish a new nested pattern; (b) §4.x peer subsections (§4.1 Principal-as-router antipattern, §4.2 Second-guess → detection, etc.) are themselves topically diverse — the section is not topically tight. ARGUS may prefer §4.3.1; I'm open if ARGUS argues it.

---

## §8 — Sequencing + handoff to ARGUS

This design ships as a single commit on `arc-39/build` carrying the Co-Authored-By trailer. PLINY dispatches ARGUS for plan critique against this design after this commit lands. ARGUS reads §1.0 restatement-gate disclosures + §1.1 sub-decision table + §7 self-assessed weak points FIRST; that's the high-value-per-token surface for the critique. The §2 + §3 substance is then read for missed risks ARGUS sees that §7 didn't surface.

After ARGUS PASS (with any rev cycles), PLINY dispatches ADA for build per §2.1 table + §3.1-§3.3 prose. ADA invokes the ADA brief preamble from §5 verbatim. Build delivers all files in §2.1 + canon edits in §3.1-§3.3. Then VERA + CATO + ZENO per gauntlet. A22 CATO MANDATORY.

After Phase 3 clean (VERA + CATO + ZENO all PASS), PLINY ships per Phase 4 (squash-merge with trailer preservation; cleanup; A18 source-ticket closure + `[for: user-tier-polybius]` tag on stoa--utn; A13 §5.10 signoff with live-verified state; A11 §5.11 paste archival).

Done.
