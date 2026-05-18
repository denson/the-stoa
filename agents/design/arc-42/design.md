# Arc 42 design — Pass 9 validate-spec mechanical-check (build-then-use) + 4 fold-ins

## §0 Restatement (per CAPTAIN_DAEDALUS.md §6.1)

Arc 42 is Pass 9 of `SPECIFICATION.md` §13 workplan — the **mechanical-check pass that validates substrate state matches spec**. This arc authors `substrate/skills/validate-spec/` (build), runs it against `SPECIFICATION.md` (use), captures the run at `agents/observation/spec-validation/mechanical-check-results.md` (artifact), and bundles four fold-in candidates that cohere with the build:

- **C1 LOCKED** — validate-spec skill (SKILL.md + check.sh + Python helpers) implementing the **7 mechanical checks LOCKED at directive A5**, plus the inline POLYBIUS triage block per A8 ε.
- **A10 fold-in (stoa--1lm)** — extend `CAPTAIN_VERA.md` §5.11 anchoring discipline to DAEDALUS-authored design.md probes. Lands as a **new `CAPTAIN_DAEDALUS.md` §6.9** that cross-refs §5.11 (parallel-section pattern; canon home stays §5.11).
- **A11 fold-in (stoa--bn8)** — amend `MAJOR_PLINY.md` §6.2 to permit polling-cron for multi-arc autonomous engagements. Adds a third mode ("multi-arc autonomous") to the existing default-mode / surface-and-wait pattern.
- **A12 fold-in (stoa--mn3)** — 5 design.md probe-spec fixes: Arc 40 m1+m2 (install.sh flag drift + bw output regex) and Arc 41 m_4.5.2+m_4.12.2+m_4.12.3 (case-class character / word-boundary FP / enumeration over-match). The new §6.9 canon (A10) is self-applied to these fixes at the moment the canon ships.
- **A13 fold-in (stoa--6k1)** — delete P10 in `agents/design/arc-25/design.md` §9.3 as redundant with P11 (4-way convergent observation already on the ticket).

Read against the brief, this restatement converges with directive A1 LOCKED + A6/A8/A10-A13 DAEDALUS-discretion + A5 LOCKED. The non-trivial imported assumptions are:

1. **A12 mn3 cleanup applies the new A10 canon** — directive frames A12 as "complementary to A10 if 1lm folded"; my read is that the cleanest shape is to ship A10 first in the design and reference §6.9 from the mn3 fix-rationale in the design specs (self-application at design time per directive's stoa--bbi observation surface).
2. **A8 ε ("inline triage block") is `validate-spec/SKILL.md`'s own triage section, not a separate document** — directive permits ε as "inline triage block in `validate-spec` SKILL.md instructing POLYBIUS to triage strangeness manually"; design specifies the structural shape of that block per §6 below.
3. **A6 β ("shell + Python") is per-check-driven** — directive permits α-or-β; design uses shell orchestration for checks 4/5 (file-system / git-status; trivially-shell), and Python helpers for checks 1/2/3/6/7 (parsers + bw-output ingestion + git trailer detection — patterns where shell-only would replicate save-verdict's pre-promotion brittleness).

No restatement divergence; proceed to design.

---

## §1 Per-candidate scopes

### §1.1 C1 — `substrate/skills/validate-spec/` skill build (LOCKED)

**Path:** `substrate/skills/validate-spec/`

**Shape (A6 β — shell orchestrator + Python helpers):**

```
substrate/skills/validate-spec/
  SKILL.md                # frontmatter (author: Denson Smith per A19 IMMUTABLE)
                          # + Why this skill exists
                          # + When to invoke / NOT to invoke
                          # + How to invoke (single shell command)
                          # + 7 checks enumerated with per-check semantics
                          # + Artifact-path contract
                          # + Inline POLYBIUS triage block (A8 ε) — strangeness routing
                          # + What this skill is NOT
                          # + Related
  check.sh                # POSIX shell orchestrator — invokes each Python helper or
                          # inline shell-only check; aggregates results; writes the
                          # artifact at agents/observation/spec-validation/mechanical-check-results.md
                          # Exit 0 on successful execution (drift is informational per A20);
                          # exit 2 reserved for "could not run" (e.g., bw not installed).
  _lib/                   # Python helpers (per save-verdict R2 canon — script invocation
                          # contract, sys.path manipulation for sibling _lib)
    __init__.py
    spec_refs.py          # check-1: §-reference resolver
    bw_tickets.py         # check-2 + check-3: bw ticket existence + status + §13 placement walk
    drift_check.py        # check-6: invoke check-substrate-updates/check.sh; parse output
    trailers.py           # check-7: git log trailer-detection with bb12806 carve-out
  _check_runner.py        # main entrypoint per save-verdict pattern (invoked by check.sh
                          # via python <path>); emits structured per-check records to stdout
                          # which check.sh aggregates into the artifact.
```

**Why shell-orchestrator + Python helpers (A6 β rationale):**

- Checks 4 (`git status`-clean) and 5 (`_drafts/` empty-or-justified) are 2-3 shell lines each; pure shell.
- Checks 1 (every §-ref resolves) and 2 (every ticket cited has claimed status) require regex scanning + per-match lookup against external state (canon files / bw); this is exactly where the Arc 40 m1/m2 + Arc 41 m_4.5.2 defects show up — shell parsing is fragile against the patterns substrate prose carries (em-dashes vs ASCII, case-class character drift, anchored vs unanchored). Python's `re` module + `subprocess` keeps the parsing structural.
- Checks 3 (open tickets all placed in §13.x), 6 (cross-workspace drift via `check-substrate-updates`), and 7 (post-Arc-40 trailer presence) need ingestion of multi-line tool output — `bw list --status open --all`, `bash substrate/skills/check-substrate-updates/check.sh`, `git log --pretty='%(trailers...)'`. Python's iterator + structured-output composition is the same shape save-verdict's `_save_verdict.py` ships.
- Pure-Python (A6 γ) was rejected: check.sh as the single invocation surface mirrors check-substrate-updates / inspect-script-output / save-verdict precedent; deviating breaks operator muscle memory.
- Pure-shell (A6 α) was rejected: would produce a 600+-line check.sh with regex-parsing logic the team JUST surfaced as a structural defect-source (the mn3 5-finding cluster IS the empirical anchor). Shipping the validate-spec skill in shell-only would walk into the same trap the §6.9 canon (A10 fold-in) is shipping to prevent.

**Invocation contract:**

```bash
bash substrate/skills/validate-spec/check.sh [--spec <path>] [--write-artifact <path>]
```

Defaults: `--spec SPECIFICATION.md` (repo root); `--write-artifact agents/observation/spec-validation/mechanical-check-results.md`. Both default to repo-relative paths resolved against `git rev-parse --show-toplevel`.

The script prints a per-check summary to stdout (one line per check: `check-N: PASS|FAIL|STRANGE — <one-line evidence>`) AND writes the structured artifact (see §1.1.b below). Exit code is **always 0 on successful execution** per A20 (drift is informational; the artifact carries the verdict, not the exit code).

### §1.1.a Per-check semantics (A5 LOCKED — DAEDALUS designs implementation; CANNOT reframe what counts as PASS)

| # | Check | PASS criterion | Evidence trail (recorded in artifact) |
|---|-------|----------------|---------------------------------------|
| 1 | Every `§X` / `§X.Y` reference in `SPECIFICATION.md` resolves to its named canon file. | Every cited `<canon-file>.md §<anchor>` pair resolves: target file exists; target file contains a heading line whose §-anchor extracts to the cited value. Bare `§X` references (no file prefix) resolve against `operating-disciplines.md` per `SPECIFICATION.md` line 7 "Reading note." | Per-reference table: (cited site in SPECIFICATION.md, target file, target §-anchor, resolved-line-in-target, PASS/FAIL). FAILs list the unresolved (file, anchor, citing-line) triples. |
| 2 | Every cited `stoa--<id>` ticket in `SPECIFICATION.md` exists in bw with claimed status. | Each unique ticket id grep-extracted from SPECIFICATION.md: (a) `bw show <id>` succeeds (ticket exists); (b) the status glyph on line 1 (`# ○` open / `# ✓` closed) matches what `SPECIFICATION.md`'s surrounding prose claims (e.g., "closed", "DONE", "DROPPED", "deferred"). | Per-ticket table: (ticket, claim, actual-glyph, PASS/FAIL/STRANGE). STRANGE = ticket exists but surrounding-prose claim is ambiguous (no machine-resolvable claim near the citation); routes to inspection triage per A8/A9. |
| 3 | `bw list --status open --all` tickets all placed in some §13.x ticket-placing section. | For each open ticket id, search `SPECIFICATION.md` §13.x bodies for the ticket id. Any open ticket NOT found in any §13.x section is a FAIL (the §12.3 / §12.5 dynamic-walk semantic check). | Per-ticket table: (open ticket, §13.x section(s) where mentioned, PASS/FAIL). FAILs are "unplaced tickets" surfacing as §12.3 audit findings. |
| 4 | `git status` shows no uncommitted changes except §12.4-ignorable state files. | `git status --porcelain` output filtered to remove `.claude/.substrate-last-check` + any other §12.4-named ignorable; result must be empty. | Verbatim filtered output (or `(clean)` literal). FAIL = any non-ignorable line remaining. |
| 5 | `_drafts/` empty OR contains only in-flight-engagement docs per §12.4. | `_drafts/` is absent OR empty OR every file inside is referenced from an open `engagement coordination` ticket per `bw list --status open --all \| grep -i 'engagement coordination'`. | Per-file table for each `_drafts/` resident: (path, referencing-ticket OR `(no reference)`). Absent-directory case records `_drafts/: not present` and PASS. |
| 6 | `check-substrate-updates` returns "no drift" across registered consumer workspaces. **A21 LOOSE pre-ratification.** | `bash substrate/skills/check-substrate-updates/check.sh` output is parsed: substrate-authoring tier (the-stoa @ project-tier `.claude/`) MUST be CURRENT; ariadne / sector-4 / railway_stoa MAY be drifted per stoa--3na PRINCIPAL-ratified loose interpretation. ANY workspace OTHER than those three drifted = FAIL (canon gap). ANY one of those three CURRENT = even better (no carve-out needed). | Per-workspace table: (workspace, verdict, drift-state). If a non-3na-named workspace surfaces drifted, mark STRANGE (route to inspection triage) — the directive's a-priori list is current-at-Arc-42-time scope-hint, not authoritative; new workspaces could be registered between directive ratification and Arc 42 ship. Strict-vs-loose interpretation = **A21 §25 PRINCIPAL-gate**: if the LOOSE pre-ratification has diverged from PRINCIPAL's current preference, PLINY surfaces with `[for: user-tier-polybius]` before the artifact ships. |
| 7 | §28 Co-Authored-By trailers on post-Arc-35 squash-merge commits with EXPLICIT CARVE-OUT for `bb12806`; commits AFTER Arc 40 ship (`dbb5b81` onwards) MUST carry trailers. | Walk `git log --first-parent main --grep='^Arc ' --pretty='%H %s'` — for each squash-merge commit, `git log -1 --pretty='%(trailers:key=Co-Authored-By)'` MUST be non-empty UNLESS the commit SHA equals `bb12806*` (carve-out). For commits authored AFTER `dbb5b81` (Arc 40), missing trailer = substance disagreement (A21 §25 PRINCIPAL-gate). | Per-commit table: (sha, subject, trailer-count, PASS/FAIL/CARVE-OUT). FAILs include the post-Arc-40 timeline-position annotation so PLINY can distinguish "pre-Arc-40 missing" (silent failure being closed by Arc 40 ship; not a §25 escalation) from "post-Arc-40 missing" (canon-after-canon-was-shipped; substance disagreement). |

**Empirical-anchor honesty: trailer-key case sensitivity.** Live ground-check at design time (Arc 38/39/40/41 ships): `git log -1 --pretty='%(trailers:key=Co-Authored-By)' dbb5b81` emits `Co-authored-by: CAPTAIN_DAEDALUS_the-stoa ...` (lowercase-by) — git canonicalizes the trailer-token case in the output. The Python helper at `trailers.py` MUST use a case-insensitive trailer-key match (the `git interpret-trailers` default canonicalizes input but the `pretty` formatter prints what git stored after canonicalization; the helper sees `Co-authored-by:` regardless of what the commit author wrote). Probe verifying this at §3 below.

### §1.1.b Artifact format (per A7 LOCKED + A26 SELF-APPLICATION)

`agents/observation/spec-validation/mechanical-check-results.md` — Markdown structured:

```markdown
# validate-spec — mechanical-check results

**Run timestamp (UTC):** <ISO-8601>
**Substrate SHA at run-time:** <git rev-parse HEAD short>
**Spec path:** <resolved absolute path to SPECIFICATION.md>
**Skill SHA at run-time:** <git rev-parse HEAD:substrate/skills/validate-spec/ short>

## Overall verdict

<one of: all-PASS | <N>-of-7-PASS-with-strangeness | <N>-of-7-PASS-with-failure | UNRUNNABLE>

## Per-check results

### check-1 — every §-ref in SPECIFICATION.md resolves

Verdict: PASS | FAIL | STRANGE
Cited references scanned: <int>
Resolved: <int>
Unresolved (FAIL): <int>

[per-reference table; details under collapsed-summary if PASS-clean, full enumeration if any FAIL or STRANGE]

### check-2 — every cited stoa--* ticket exists with claimed status

[same structure]

### check-3 — every open ticket placed in some §13.x section

[same structure]

### check-4 — git status clean modulo §12.4 ignorables

[same structure]

### check-5 — _drafts/ empty or justified

[same structure]

### check-6 — check-substrate-updates shows no drift across workspaces

**A21 LOOSE pre-ratification (per Arc 42 directive A21):** ariadne / sector-4 / railway_stoa drift state is PASS-with-documented-residue per stoa--3na (substrate-authoring tier the-stoa @ project-tier .claude/ IS clean).

[per-workspace table; explicit "residue accepted per A21" annotation on the three deferred workspaces]

### check-7 — §28 Co-Authored-By trailers on post-Arc-35 squash-merge commits

**Explicit carve-out per A5 + §13.11 + A21:** bb12806 (Arc 37) is a known historical exception per CLAUDE.md no-force-push rule.

**Post-Arc-40 trailer-canon test (per A21):** commits AFTER dbb5b81 must carry trailers; any missing = substance disagreement.

[per-commit table; explicit "carve-out" annotation on bb12806; explicit "post-Arc-40-canon-test" annotation on commits in the post-dbb5b81 timeline-position]

## Strangeness for inspection-agent triage (per A8 ε / §27.2 step 2)

<per-finding triage stub for STRANGE-verdict items; POLYBIUS routes per A9 / §27.2 step 3>

## PRINCIPAL-gate findings (per A21 / §25)

<empty section if no §25 trigger fired; populated entries describe the gate, the evidence, and the surfacing posture>

## Evidence trail per check

[for each check, the verbatim command(s) the helper executed, with raw output captured. A20 "no PASS-trust-me" mitigation: every PASS is reproducible from the recorded commands.]
```

The artifact is committed by ADA as part of the build; CATO audits the artifact for honesty per A24.

### §1.2 A10 fold-in (stoa--1lm) — extend §5.11 anchoring discipline to DAEDALUS-authored design.md probes

**Landing site:** `substrate/CAPTAIN_DAEDALUS.md` — **new §6.9** added immediately after the existing §6.8 (Canonical-template wording-alignment discipline) and before the existing §7 (Verdict format). Mirrors the placement pattern §6.8 used for its §5.11 sibling.

**Why a new section vs extending §5.11 in CAPTAIN_VERA.md:**

- §5.11 lives at the **verification** seat — it tells VERA what to do when it sees a probe-spec with an unanchored regex (surface as `methodology_concerns:` rather than executing the underspecified probe).
- The 5-finding mn3 cluster + DAEDALUS §6.4 Arc 41 observation diagnose the problem at the **authoring** seat — DAEDALUS hand-types probes during design without live round-trip, and the defects accrete.
- The cleanest shape is a **parallel discipline at the authoring seat** (DAEDALUS §6.9) that cross-refs §5.11 — same pattern §6.8 (DAEDALUS canonical-template wording) takes for its §5.11 sibling. §5.11 stays the canon home for the verification-side property; §6.9 carries the authoring-side property.

**§6.9 content shape (DAEDALUS authors; cite-checked at design time):**

> ### 6.9 Probe-grounding discipline for design.md probes (extends §5.11 to the authoring seat)
>
> When you author a verification probe in design.md, the probe is a load-bearing instruction to ADA-at-build-time and VERA-at-verify-time. A probe with a regex that doesn't match its target — or matches more than the intended target — produces a misleading PASS that the gauntlet then ratifies. The §5.11 discipline at `CAPTAIN_VERA.md` catches this at verify-time when the verifier notices the under-anchoring; the discipline below catches it at authoring-time before the brittle probe ships into the design.
>
> **The discipline (at probe-authoring time).** Before submitting any design.md probe whose body contains a regex or grep pattern against substrate prose, the canon file structure, or shipped tool output:
>
> 1. **Anchor the regex.** Use `^` (line-start), `$` (line-end), word-boundaries `\b`, OR a unique surrounding-context substring that disambiguates the intended single-or-bounded match from incidental documentation prose. Bare-substring patterns that match anywhere in the file are the empirical defect-source (mn3 m_4.12.2 anchor: `\bthe user\b` matching `the user-tier-POLYBIUS`).
>
> 2. **Character-class completeness.** When matching tool-flag or command-name patterns, account for case-flag combinations and shell-metacharacter context explicitly. `[a-z]*` does NOT match uppercase letters (mn3 m_4.5.2 anchor: `grep -[a-z]*i[a-z]*` cannot match `grep -ciE`); use `[a-zA-Z]*` or apply `grep -i` at the outer scope.
>
> 3. **Live round-trip at authoring time.** Run every probe command literally against the current substrate state during design draft. A probe that emits zero matches against the very state it's being authored for is structurally broken, not under-specified — fix at design-time, don't ship to ADA.
>
> 4. **Ground-check against shipped tool surface.** Do not assume tool flags or output shapes from memory. Verify against the shipped script source OR live tool output (mn3 m1 anchor: `install.sh --no-bw-init` / `--dest` cited flags that don't exist; mn3 m2 anchor: `bw show <id> \| grep '^Status:.*closed'` cited a status-line shape bw doesn't emit). The §5.2 `MAJOR_PLINY.md` grounding-check preamble names this for ADA-build-time; this clause names it for DAEDALUS-authoring-time.
>
> 5. **Enumeration vs invocation context.** When a probe greps for risky shell tokens (credentials, dangerous commands), scope the grep to the relevant context (bash-code-block, git-diff +-line, or rejection-context exclusion) rather than whole-file. Whole-file greps false-positive on the substrate's own canon documenting the anti-pattern (mn3 m_4.12.3 anchor: credential-discipline probe over-matched on enumeration-context lines vs actual invocations).
>
> If you cannot apply one of (1)-(5) for structural reasons, surface the gap in your verdict's `self_assessed_weak_points:` field per §6.2 — that surfaces the probe-spec brittleness to ARGUS during plan critique, before ADA inherits it.
>
> **Empirical anchor.** Arcs 40-41 accumulated 5 design.md probe-spec defects (filed at `stoa--mn3`; canon-promotion proposal at this section per `stoa--1lm`): Arc 40 m1 (install.sh non-existent flag) + m2 (bw output shape drift); Arc 41 m_4.5.2 (case-class character drift) + m_4.12.2 (word-boundary FP on hyphenated compound) + m_4.12.3 (whole-file grep over-match on enumeration context). All 5 substantively PASSed (VERA / ADA caught the drift and reverified with corrected patterns); the recurrent failure mode is hand-typed probes that don't live-round-trip at authoring time. Discipline-shipped arc: Arc 42 (`stoa--1lm`).
>
> **Cross-refs:** `CAPTAIN_VERA.md` §5.11 (verification-side sibling — when a probe ships with under-anchoring despite this discipline, §5.11 catches it at verify-time); `CAPTAIN_DAEDALUS.md` §6.2 (self-assessed-weak-points pre-ratification — probe-spec brittleness you cannot eliminate at authoring belongs in this field); `MAJOR_PLINY.md` §5.2 (the grounding-check preamble for ADA-build-time; the §5.2 preamble is the build-seat sibling to this authoring-seat discipline).

### §1.3 A11 fold-in (stoa--bn8) — amend §6.2 to permit polling-cron for multi-arc autonomous engagements

**Landing site:** `substrate/MAJOR_PLINY.md` §6.2 (existing "Surface-and-wait polling pattern (Arc 18)").

**Edit shape:** existing §6.2 prose is preserved as the **default mode**; section title and structure expand to name three modes. New text added below the existing CronCreate template and "Anti-pattern" block (the existing prose stays; new prose layers on top of it).

**Proposed new §6.2 structure (DAEDALUS authors; ADA wires per spec):**

The existing §6.2 title `### 6.2 Surface-and-wait polling pattern (Arc 18)` is preserved as the default mode header. The existing prose (lines 622-648 inclusive: heads-down-vs-surface-and-wait + CronCreate template + Anti-pattern + Empirical proof + §19.7 cross-ref) STAYS verbatim. Immediately after the existing prose (after the §19.7 cross-ref line), add the following new subsection:

> #### 6.2a Multi-arc autonomous mode (per stoa--bn8, Arcs 39-41 proto-canon evidence)
>
> The surface-and-wait default above is the right shape for single-arc dispatches, first-contact engagements, and any context where PRINCIPAL is actively driving. When PRINCIPAL has explicitly delegated a **multi-arc engagement** to user-tier (typically via priming-paste establishing the cross-tier coordination), polling-cron-at-PLINY is permitted as an alternative mode — same hygiene as `MAJOR_POLYBIUS.md` polling per `operating-disciplines.md` §7.2 + §11 step 1.5 renewal.
>
> **When this mode applies (load-bearing — do NOT widen):**
>
> - PRINCIPAL has explicitly delegated multi-arc work to user-tier (priming-paste named the engagement; user-tier POLYBIUS is the coordination authority).
> - The engagement spans ≥2 arcs (single-arc work stays under the surface-and-wait default — the polling-cron overhead does not earn its cost on a single arc).
> - PLINY's cron monitors a named coordination ticket for `[for: pliny-the-stoa]` dispatch signals (NOT a free-polling cron that scans bw broadly).
>
> **The standby pattern (within a multi-arc engagement, between arcs):**
>
> Between arcs in a multi-arc engagement, PLINY's polling-cron remains active but PLINY is idle awaiting next dispatch. The cron auto-acknowledges routine heartbeats via comment-only posts (no engagement-substance); PLINY engages on substance only when a `[for: pliny-the-stoa]` dispatch signal lands. Same standby-cadence-keeps-channel-warm pattern §11 establishes for POLYBIUS-side polling.
>
> **Reuse existing cron infrastructure.** Do NOT create new crons for a multi-arc engagement if a prior priming established them — reuse jobids from the priming-paste (e.g., PLINY-side polling + renewal pair created at activation). Same `MAJOR_PLINY.md` Arc 36 / Arc 38 / Arc 41 directive `A9 LOCKED` pattern.
>
> **Empirical anchor.** 2026-05-18 multi-arc autonomous sequence (Arcs 39+40+41) priming established polling-cron-at-PLINY for cross-tier bw-signal dispatch; the pattern HELD CLEANLY across all 3 arcs (zero PRINCIPAL paste touchpoints on routine dispatch; cross-tier `[for:]` signal routing scaled cleanly; per-arc triple-attestation held end-to-end; wall-clock pace ~30 min average per arc). Source ticket: `stoa--bn8`. Discipline-shipped arc: Arc 42. Cross-ref `stoa--bbi` (refined-principle thesis evidence for proto-canon-promotion).

The change is **additive** — the surface-and-wait default is preserved verbatim; the new mode is opt-in and gated on the conditions above. The §6.2 title gets no edit (the existing "Surface-and-wait polling pattern (Arc 18)" remains the default-mode name; §6.2a is the new mode-specific subsection).

### §1.4 A12 fold-in (stoa--mn3) — 5 design.md probe-spec fixes (housekeeping; self-application of §6.9 canon at A10 ship time)

**Five sites** to edit, all in `agents/design/arc-40/design.md` and `agents/design/arc-41/design.md`:

**mn3 fix-1 — Arc 40 design.md p15** (install.sh `--no-bw-init` flag drift)
- **Current** (arc-40 design.md line 522): `bash substrate/install.sh --target project --dest "$TEMPDIR/test" --no-bw-init >/dev/null 2>&1 && \`
- **Fix:** replace `--dest "$TEMPDIR/test" --no-bw-init` with `--target project --project-dir "$TEMPDIR/test-project"`, and pre-create `$TEMPDIR/test-project` before the install.sh invocation (install.sh does not auto-create per shipped behavior).
- **Self-application:** the new §6.9 clause 4 (ground-check against shipped tool surface) is exactly the discipline that catches this. Cite §6.9 in the fix-rationale comment.

**mn3 fix-2 — Arc 40 design.md p18** (install.sh same flag drift)
- **Current** (arc-40 design.md line 553): same `--dest ... --no-bw-init` shape.
- **Fix:** same as fix-1.

**mn3 fix-3 — Arc 40 design.md p24** (bw output shape `^Status:.*closed` doesn't exist)
- **Current** (arc-40 design.md line 604): `for t in stoa--3sz stoa--5sr stoa--6wp stoa--6n9 stoa--t9u; do bw show "$t" 2>&1 | grep -c "^Status:.*closed"; done | paste -sd+ - | bc`
- **Fix:** replace `grep -c "^Status:.*closed"` with `head -1 \| grep -c '^# ✓'` (anchored against actual bw line-1 closed-glyph shape). Alternative form: `bw list --closed --all \| grep -c "<id>"` per-ticket. Pick the head-1 form (simpler aggregation across the list).
- **Self-application:** §6.9 clause 4 again — bw output shape verified against live ground-check.

**mn3 fix-4 — Arc 41 design.md §4.5.2** (case-class character drift)
- **Current** (arc-41 design.md line 548): `grep -cE 'grep -[a-z]*i[a-z]* '`
- **Fix:** `grep -cE 'grep -[a-zA-Z]*i[a-zA-Z]* '` (case-class completeness per §6.9 clause 2).

**mn3 fix-5 — Arc 41 design.md §4.12.2 + §4.12.3** (word-boundary FP + enumeration over-match)
- **§4.12.2 current** (arc-41 design.md line 766): `grep -cE '\b[Cc]olonel\b|\bthe user\b'`
- **§4.12.2 fix:** `grep -cE '\b[Cc]olonel\b|\bthe user[ .,;:!?\n]'` (separator-anchored per §6.9 clause 1; covers sentence-ending punctuation + space + newline). Alternative `grep -vE 'user-tier'` exclusion form was considered and rejected — it doesn't distinguish "user-tier" valid mentions from "the user" voice violations; the separator-anchor catches "the user " (voice violation) without false-positive on "the user-tier" (substrate-canonical noun).
- **§4.12.3 current** (arc-41 design.md line 775): `grep -cE 'op (read|run)|gcloud |gh auth |aws |kubectl |vercel |railway |fly '` against git-diff +-lines (the +-line scoping is correct; the enumeration-context exclusion is what's missing).
- **§4.12.3 fix:** wrap the existing git-diff scope with an additional `grep -vE` that excludes lines whose context is enumeration-rejection-prose (the existing §4.5.3 pattern: `grep -vE 'rejected|anti-pattern|Option 2|do not propose'`). Per §6.9 clause 5.

All 5 fixes carry a 1-line cite-comment pointing to §6.9 (the new canon they exemplify). Self-application at design time per A20 honesty discipline + stoa--bbi observation surface.

### §1.5 A13 fold-in (stoa--6k1) — delete P10 in arc-25 design.md §9.3

**Edit site:** `agents/design/arc-25/design.md` line 716.

**Edit shape:** delete the P10 row entirely (the table row containing `| P10 | ...`). The §9.3 table loses one row; surrounding rows P11, P11b, P12 stay verbatim. No prose elsewhere in arc-25 design.md references P10 by anchor (grep-verified at design time during draft); deletion is local.

**Why deletion vs rewrite-as-alternation:** 4-way convergent observation across ADA + VERA + CATO + ZENO (per ticket body) recommended (a) delete as redundant with P11, OR (b) rewrite as alternation. The discoverability property P10 was probing IS fully covered by P11 (`grep -l "credential-discipline" <4 files>`) at the same 4 in-scope CAPTAIN envelopes; rewriting P10 as an alternation `grep` adds a probe that ratifies the same property P11 already does. The cleaner shape is deletion (Occam's; the redundant probe has no work to do). The ticket body lists (a) as the canonical recommendation.

---

## §2 Universal disciplines (per A14-A26)

### §2.1 A14 LOCKED — §28 Co-Authored-By trailers (mandatory for all ADA + DAEDALUS commits)

Every commit ADA + DAEDALUS lands inside `arc-42/build` MUST carry the seat-identity trailer per `operating-disciplines.md` §28 + `MAJOR_PLINY.md` §5.10 + `CAPTAIN_ADA.md` §5.5. Trailer format:

```
Co-Authored-By: CAPTAIN_<MNEMONIC>_the-stoa <captain-<mnemonic>@the-stoa.local>
```

DAEDALUS commits carry `CAPTAIN_DAEDALUS_the-stoa <captain-daedalus@the-stoa.local>`. ADA commits carry `CAPTAIN_ADA_the-stoa <captain-ada@the-stoa.local>`.

**Use HEREDOC body** for every commit message per global `~/.claude/CLAUDE.md` example pattern. No `--body` override at squash-merge time (the §5.10 canon shipped Arc 40 prevents the bb12806 regression class).

Probe at §3 verifies (spot-check) on DAEDALUS + ADA commits.

### §2.2 A15 LOCKED — §5.10 signoff with live-verified state per §19.6

PLINY's Phase 4 signoff on stoa--utn MUST live-verify the artifact existence + check-results before posting. No attestation-confabulation per §19.6: cite live `cat agents/observation/spec-validation/mechanical-check-results.md \| head -<N>` output OR equivalent live ground-check.

### §2.3 A16 LOCKED — `[from: <self-seat-slug>]` author tags

All bw comments by PLINY / POLYBIUS_the_stoa / CAPTAINs carry author tag per Arc 36 §7.1/§7.7. DAEDALUS uses `[from: daedalus-the-stoa]`; ADA uses `[from: ada-the-stoa]`. Cross-tier comments to user-tier POLYBIUS carry `[for: user-tier-polybius] [from: <self-seat-slug>]`.

### §2.4 A17 LOCKED — cron infrastructure REUSE existing

Do NOT create new crons. Reuse from priming:
- POLYBIUS: `b6e8630b` (polling) + `3c1e575b` (renewal)
- PLINY: `abc905a6` (polling) + `6e69c60a` (renewal)

### §2.5 A18 LOCKED — cite-comment discipline at every read-site

Every cross-ref the design ships (CAPTAIN_DAEDALUS.md §6.9 → §5.11; MAJOR_PLINY.md §6.2a → §11 step 1.5 renewal; mn3 fix-rationale comments → §6.9; etc.) must resolve via cite at the read site. Spot-check via probe at §3.

### §2.6 A19 LOCKED — A18 IMMUTABLE — `substrate/skills/validate-spec/SKILL.md` MUST carry `author: Denson Smith`

Frontmatter shape:
```yaml
---
name: validate-spec
description: <one-line description per substrate-skill convention>
author: Denson Smith
---
```

Probe at §3 verifies. Per `CAPTAIN_DAEDALUS.md` §8 authorship-attribution-immutable + global `~/.claude/CLAUDE.md` audit checklist.

### §2.7 A20 LOCKED — motivated-reasoning mitigations woven into design

Per directive A20 + this design's response:

- **Each check has an INDEPENDENT EVIDENCE TRAIL recorded in the artifact** per §1.1.b artifact format ("Evidence trail per check" section). No PASS-trust-me; every PASS reproduces from the recorded commands.
- **First-run-discovers-strangeness is GOOD signal.** The artifact's "Strangeness for inspection-agent triage" section is a first-class output, not an exception. STRANGE-verdict items route to POLYBIUS triage per A8 ε / §27.2 step 2-3 (NOT auto-PASS).
- **Strangeness routes to inspection triage OR PRINCIPAL escalation.** §6 below specifies the inline triage block; A21 §25 PRINCIPAL-gate routing for the 3 pre-flagged trigger conditions.
- **CATO MANDATORY per A24.** Honesty audit on both the implementation AND the mech-check-results artifact (see §5 self-assessed weak points — the artifact is where motivated-PASS would hide; CATO reads BOTH artifact text AND check.sh+_lib code).

### §2.8 A21 LOCKED — Pass-9 specific §25 PRINCIPAL-gates (pre-flagged)

Three trigger conditions; when any fires, PLINY immediately surfaces to user-tier-polybius with `[for: user-tier-polybius]` tag — do NOT auto-resolve:

1. **check-6 strict-interpretation divergence from PRINCIPAL's a priori LOOSE.** If validate-spec finds a workspace OTHER than ariadne / sector-4 / railway_stoa drifted (i.e., a workspace not pre-named in stoa--3na), OR if PRINCIPAL's current preference has shifted toward strict interpretation, surface as `[for: user-tier-polybius]` + cite the artifact's check-6 table.
2. **check-7 trailer-canon-failure (post-Arc-40 commit missing trailer).** Any commit AFTER `dbb5b81` (Arc 40 ship) that emits empty trailers = substance disagreement. Arc 40 §5.10 canon should have prevented this; failure indicates canon gap (NOT a typo to fix-and-move-on). Surface as `[for: user-tier-polybius]` + cite the failing commit SHA + the §5.10 canon site that should have prevented.
3. **ANY mechanical check genuinely FAILS** (not STRANGE; FAIL — the falsification criteria the team authored against itself). Surface with the failing evidence; PRINCIPAL ratifies fix-now-this-arc vs document-as-residue-and-ship vs spec-edit-and-re-run.

### §2.9 A22 LOCKED — source-ticket closure on Arc 42 ship

Close on ship per A22:
- **C1 implicit close** = Pass 9 done = validate-spec skill exists at substrate/skills/validate-spec/ + ran once against SPECIFICATION.md + artifact landed at agents/observation/spec-validation/mechanical-check-results.md. The implicit-close marker = a `stoa--utn` comment by PLINY at Phase 4 ship attesting all three conditions live-verified.
- **A10 stoa--1lm close** = CAPTAIN_DAEDALUS.md §6.9 lands.
- **A11 stoa--bn8 close** = MAJOR_PLINY.md §6.2a lands.
- **A12 stoa--mn3 close** = all 5 fixes commit.
- **A13 stoa--6k1 close** = P10 row deletion commits.

Total source tickets closed: **C1 implicit + 4 folded = 5 closures attributable to Arc 42 ship**. Tag `[for: user-tier-polybius]` on stoa--utn at ship time (continuing as the long-running engagement coordination ticket through end of sequence).

### §2.10 A23 LOCKED — hard-locks (out-of-scope; surface PRINCIPAL-gate if pressure to violate)

- No restructuring 7 mechanical checks beyond A5 LOCKS.
- No widening A8/A9 inspection-agent shape into heavy separate skill (no δ pick mid-arc).
- No building Pass 10 stellation infrastructure (separate concern per §13.12).

If brief-time pressure surfaces to violate any of these, PLINY surfaces as `[for: user-tier-polybius]` per A21 trigger condition 3.

### §2.11 A24 LOCKED — CATO MANDATORY

CATO must cold-read BOTH the validate-spec implementation (check.sh + _lib/*.py) AND the mech-check-results artifact for craft + scope + honesty. The artifact is the highest-motivated-reasoning-risk surface in this arc — CATO audits the artifact's per-check evidence trail against the verbatim commands recorded.

### §2.12 A25 LOCKED — paste archival per §5.11 / Arc 41 A16 wording-clarification

After Arc 42 ship: archive the 2 HUMAN_paste-* activation pastes to `substrate/arcs/arc-42/pastes/`. Directive itself stays at `substrate/arcs/arc-42-build-directive.md` (NOT archived).

### §2.13 A26 LOCKED — SELF-APPLICATION TARGET

The build deliverable INCLUDES running validate-spec against SPECIFICATION.md and capturing results. ADA executes the run as part of build commits. The skill ships with **evidence-of-use, not just evidence-of-existence**. Probe at §3 verifies the artifact exists AND captures all 7 checks.

### §2.14 ADA brief preamble (per MAJOR_PLINY.md §5.2 — reproduce verbatim)

Ground-check every concrete example in this design against the shipped code, specifically:

- JSON example shapes (response bodies, request bodies)
- Function/method signatures (parameter names, types, return types)
- Error message text (exact string match)
- Line ranges in path:line citations
- HTTP response codes
- Wire-protocol constants (header names, status codes, envelope keys)

If a design example contradicts the shipped code, the shipped code is canon — flag the design drift but build to ship reality.

**Specific high-risk surfaces for this arc:**

- **bw output shape** (check-2, check-3 helpers): bw show line-1 = `# ○ <id> — <subject>` (open) or `# ✓ <id> — <subject>` (closed). Glyphs are Unicode (`○` = U+25CB; `✓` = U+2713). Helper code should match against these glyphs verbatim, not "Status:" line.
- **git trailer key case-canonicalization**: `%(trailers:key=Co-Authored-By)` formatter emits `Co-authored-by:` (lowercase-by) regardless of commit-author input. Helper code at `trailers.py` MUST use case-insensitive trailer-key match.
- **install.sh flag surface** (mn3 fix-1 + fix-2): correct shape is `--target <tier> --project-dir <path>`; pre-create `--project-dir` (install.sh does NOT auto-create).
- **bb12806 SHA prefix**: 7-char short SHA. Helper should match `git log --first-parent main` walk's full SHA prefix-matching `bb12806*`, not the literal string (avoids brittleness if git default short-SHA length changes).
- **check-substrate-updates output shape**: parse the per-workspace summary lines (format documented in `substrate/skills/check-substrate-updates/SKILL.md` lines 71-89 — `<workspace-name>   <status>   (N drifted, N missing, N obsolete; N uncommitted)`). The substrate-authoring tier the-stoa appears as `the-stoa` in registry (check `substrate/consumer-workspaces.txt`).

---

## §3 Verification probes

All probes apply CAPTAIN_DAEDALUS.md §6.9 anchoring discipline (self-application: this arc ships the §6.9 canon, so the design's own probes comply with it). Each probe runs from repo root unless noted.

### §3.1 C1 validate-spec skill exists with correct structure

**P1 — SKILL.md exists with correct frontmatter author**
```bash
test -f substrate/skills/validate-spec/SKILL.md && \
  awk '/^---$/{f=!f; next} f' substrate/skills/validate-spec/SKILL.md | grep -E '^author: Denson Smith$'
# Expected: one match (frontmatter parsed via awk between --- delimiters; author field anchored)
```

**P2 — check.sh exists and is executable in shape**
```bash
test -f substrate/skills/validate-spec/check.sh && \
  head -1 substrate/skills/validate-spec/check.sh | grep -E '^#!/usr/bin/env (bash|sh)$'
# Expected: shebang line matches one of the two POSIX-conventional forms
```

**P3 — Python helper module structure exists per A6 β design**
```bash
for f in _check_runner.py _lib/__init__.py _lib/spec_refs.py _lib/bw_tickets.py _lib/drift_check.py _lib/trailers.py; do
  test -f "substrate/skills/validate-spec/$f" || echo "MISSING: $f"
done
# Expected: no MISSING output (every named helper file exists)
```

### §3.2 A4 install.sh wiring

**P4 — validate-spec in SKILL_NAMES at deploy-loop**
```bash
awk '/^SKILL_NAMES=\(/,/^\)/' substrate/install.sh | grep -cE '^[[:space:]]+validate-spec[[:space:]]*$'
# Expected: 1 (validate-spec appears exactly once in the SKILL_NAMES array; anchored to leading-whitespace + word)
```

### §3.3 A26 self-application artifact

**P5 — artifact exists at canonical path**
```bash
test -f agents/observation/spec-validation/mechanical-check-results.md && echo OK
# Expected: OK
```

**P6 — artifact captures all 7 checks (per §1.1.b structure)**
```bash
for n in 1 2 3 4 5 6 7; do
  grep -cE "^### check-$n " agents/observation/spec-validation/mechanical-check-results.md
done | paste -sd+ - | bc
# Expected: 7 (one ### check-N section per check, anchored at line-start)
```

**P7 — artifact captures run metadata (timestamp + substrate SHA + spec path + skill SHA)**
```bash
grep -cE '^\*\*(Run timestamp \(UTC\)|Substrate SHA at run-time|Spec path|Skill SHA at run-time):\*\*' \
  agents/observation/spec-validation/mechanical-check-results.md
# Expected: 4 (all 4 metadata lines present; literal-anchored)
```

**P8 — artifact captures the bb12806 carve-out attestation explicitly**
```bash
grep -cE 'bb12806' agents/observation/spec-validation/mechanical-check-results.md
# Expected: >=2 (at least once in check-7 carve-out annotation prose; at least once in evidence trail)
```

### §3.4 A5 7 mechanical checks — each implementation site

**P9 — check.sh dispatches all 7 checks**
```bash
grep -cE '\bcheck-[1-7]\b' substrate/skills/validate-spec/check.sh
# Expected: >=7 (each check named at least once in the orchestrator; word-boundary anchored)
```

**P10 — check-1 §-ref helper exists and uses regex anchoring**
```bash
grep -cE 're\.(compile|search|match|finditer)' substrate/skills/validate-spec/_lib/spec_refs.py
# Expected: >=1 (Python re module in use for §-ref parsing — structural property)
```

**P11 — check-2/3 bw helper subprocess-invokes bw**
```bash
grep -cE 'subprocess|bw show|bw list' substrate/skills/validate-spec/_lib/bw_tickets.py
# Expected: >=1 (helper calls bw)
```

**P12 — check-7 trailer helper uses case-insensitive trailer-key match (load-bearing per §1.1.a empirical-anchor honesty)**
```bash
grep -cE '(?i)co-authored-by|re\.IGNORECASE|lower\(\)' substrate/skills/validate-spec/_lib/trailers.py
# Expected: >=1 (case-insensitive matching present; matches one of three idioms — inline-flag, IGNORECASE constant, or .lower() normalization)
```

**P13 — check-7 helper recognizes bb12806 carve-out**
```bash
grep -cE "bb12806" substrate/skills/validate-spec/_lib/trailers.py
# Expected: >=1 (carve-out SHA appears in the helper, indicating it's structurally aware of the historical exception)
```

### §3.5 A10 fold-in — CAPTAIN_DAEDALUS.md §6.9 lands

**P14 — §6.9 section exists with correct title**
```bash
grep -cE '^### 6\.9 Probe-grounding discipline' substrate/CAPTAIN_DAEDALUS.md
# Expected: 1
```

**P15 — §6.9 carries cross-ref to §5.11 (canon home)**
```bash
awk '/^### 6\.9 /,/^### [67]\./' substrate/CAPTAIN_DAEDALUS.md | grep -cE 'CAPTAIN_VERA\.md.*§5\.11'
# Expected: >=1 (cite to §5.11 within §6.9 body; awk-scoped to the §6.9 section)
```

**P16 — §6.9 names the 5 mn3-finding anchors (empirical-anchor honesty)**
```bash
awk '/^### 6\.9 /,/^### [67]\./' substrate/CAPTAIN_DAEDALUS.md | grep -cE 'm1|m2|m_4\.5\.2|m_4\.12\.2|m_4\.12\.3'
# Expected: >=5 (each of the 5 mn3 findings named in the empirical-anchor block; awk-scoped to §6.9)
```

### §3.6 A11 fold-in — MAJOR_PLINY.md §6.2a lands

**P17 — §6.2a subsection exists**
```bash
grep -cE '^#### 6\.2a Multi-arc autonomous mode' substrate/MAJOR_PLINY.md
# Expected: 1
```

**P18 — §6.2a preserves the surface-and-wait default (verbatim prose preserved)**
```bash
grep -cE '^### 6\.2 Surface-and-wait polling pattern \(Arc 18\)' substrate/MAJOR_PLINY.md
# Expected: 1 (the default-mode header stays verbatim; A11 is additive)
```

**P19 — §6.2a cross-refs to §7.2 and §11 step 1.5 (cite-discipline)**
```bash
awk '/^#### 6\.2a /,/^### [67]\./' substrate/MAJOR_PLINY.md | grep -cE 'operating-disciplines\.md.*§(7\.2|11)'
# Expected: >=1 (cite to op-disc §7.2 OR §11 within the §6.2a body)
```

### §3.7 A12 fold-in — mn3 5 design.md probe-spec fixes

**P20 — arc-40 design.md p15 + p18 no longer cite `--no-bw-init` (mn3 fix-1 + fix-2 applied)**
```bash
grep -cE '\-\-no-bw-init' agents/design/arc-40/design.md
# Expected: 0 (flag drift removed; word-boundary anchored on the literal flag string)
```

**P21 — arc-40 design.md p15 + p18 use `--project-dir` (mn3 fix shape)**
```bash
grep -cE '\-\-project-dir' agents/design/arc-40/design.md
# Expected: >=2 (both p15 and p18 use the correct flag; literal-anchored)
```

**P22 — arc-40 design.md p24 no longer cites the non-existent `^Status:.*closed` shape (mn3 fix-3)**
```bash
grep -cE 'grep -c "\\^Status:' agents/design/arc-40/design.md
# Expected: 0 (the broken shape removed; literal-anchored to the specific pattern)
```

**P23 — arc-40 design.md p24 uses `# ✓` glyph anchor (mn3 fix-3 shape)**
```bash
grep -cE "head -1.*grep.*'#" agents/design/arc-40/design.md
# Expected: >=1 (the fixed shape uses head -1 + grep on `#` glyph line; bounded substring anchor)
```

**P24 — arc-41 design.md §4.5.2 uses case-class completeness (mn3 fix-4)**
```bash
grep -cE 'grep -\[a-zA-Z\]\*i\[a-zA-Z\]\*' agents/design/arc-41/design.md
# Expected: >=1 (the corrected character class with uppercase; literal-anchored on the post-fix shape)
```

**P25 — arc-41 design.md §4.12.2 uses separator-anchored 'the user' pattern (mn3 fix-5a)**
```bash
grep -cE "the user\[ \.,;:!\?\\\\n\]" agents/design/arc-41/design.md
# Expected: >=1 (separator-anchored character class; literal-anchored on the post-fix shape)
```

**P26 — arc-41 design.md §4.12.3 uses enumeration-context exclusion (mn3 fix-5b)**
```bash
awk '/§4\.12\.3/,/§4\.13|^## /' agents/design/arc-41/design.md | grep -cE 'rejected|anti-pattern|Option 2|do not propose'
# Expected: >=1 (the §4.5.3-style exclusion clause present in the tightened §4.12.3 probe; awk-scoped)
```

### §3.8 A13 fold-in — arc-25 design.md P10 deletion

**P27 — P10 row deleted from arc-25 design.md §9.3**
```bash
awk '/^### §9\.3 /,/^### §9\.4/' agents/design/arc-25/design.md | grep -cE '^\| P10 \|'
# Expected: 0 (P10 row absent from §9.3 table; awk-scoped to that subsection)
```

**P28 — P11, P11b, P12 rows preserved (verify deletion is local, not over-broad)**
```bash
awk '/^### §9\.3 /,/^### §9\.4/' agents/design/arc-25/design.md | grep -cE '^\| (P11|P11b|P12) \|'
# Expected: 3 (the three sibling rows survived the P10 deletion)
```

### §3.9 A14 trailer check + A22 source-ticket closure

**P29 — DAEDALUS commit on arc-42/build carries seat-identity trailer**
```bash
git log --first-parent arc-42/build main..arc-42/build --pretty='%(trailers:key=Co-Authored-By)' \
  | grep -cE -i 'CAPTAIN_DAEDALUS_the-stoa'
# Expected: >=1 (at least one commit on arc-42/build carries the DAEDALUS trailer; case-insensitive per git canonicalization observed at design-time)
```

**P30 — ADA commit on arc-42/build carries seat-identity trailer**
```bash
git log --first-parent arc-42/build main..arc-42/build --pretty='%(trailers:key=Co-Authored-By)' \
  | grep -cE -i 'CAPTAIN_ADA_the-stoa'
# Expected: >=1 (at least one commit on arc-42/build carries the ADA trailer)
```

**P31 — A22 source ticket closure count (run after Phase 4 ship; ADA's pre-ship run will record OPEN, post-ship will record CLOSED)**
```bash
for t in stoa--1lm stoa--bn8 stoa--mn3 stoa--6k1; do
  bw show "$t" 2>&1 | head -1 | grep -cE '^# ✓'
done | paste -sd+ - | bc
# Expected: 4 (post-ship — all 4 folded tickets closed; uses # ✓ glyph anchor per ground-checked bw output shape)
```

### §3.10 A18 IMMUTABLE — frontmatter author field

**P32 — substrate/skills/validate-spec/SKILL.md frontmatter author is Denson Smith (per A19)**

(Identical to P1 — repeated as A19-specific check for ZENO clarity; P1 satisfies if both pass against the same file.)

### §3.11 A25 paste archival post-arc

**P33 — Arc 42 activation pastes archived to substrate/arcs/arc-42/pastes/**
```bash
ls substrate/arcs/arc-42/pastes/HUMAN_paste-*.md 2>&1 | grep -c 'HUMAN_paste-'
# Expected: 2 (PLINY priming paste + POLYBIUS_the_stoa priming paste)
```

**P34 — Arc 42 directive STAYS at substrate/arcs/ (not archived)**
```bash
test -f substrate/arcs/arc-42-build-directive.md && echo OK
# Expected: OK (per Arc 41 A16 wording-clarification: directive itself stays at substrate/arcs/, NOT archived to pastes/)
```

### §3.12 Mechanical-check first-run honesty (per A20 / A26)

**P35 — check.sh invocation succeeds (exit 0) when run during ADA build**

Run during ADA build phase:
```bash
bash substrate/skills/validate-spec/check.sh 2>&1; echo "exit=$?"
# Expected: exit=0 (skill runs successfully; drift is informational per A20 — the artifact carries the verdict not the exit code)
```

**P36 — All 7 checks emit a recognizable per-check verdict line to stdout**
```bash
bash substrate/skills/validate-spec/check.sh 2>&1 | grep -cE '^check-[1-7]: (PASS|FAIL|STRANGE)'
# Expected: 7 (one verdict line per check; anchored at line-start)
```

**Total: 36 probes (P1-P36).**

---

## §4 Self-assessed weak points

Per CAPTAIN_DAEDALUS.md §6.2 — honest surfacing of where ARGUS should look hardest.

**Weak point 1 — Implementation-shape risk for spec §-reference parsing (check-1).**
Spec prose carries §-references in three distinct forms: (a) `<file>.md §X.Y` form (full canonical), (b) bare `§X` form (defaults to operating-disciplines.md per SPECIFICATION.md line 7), (c) `<file> §X` form without the .md (rare but present). My §3 probes for check-1 (P10) verify the helper uses `re.compile`-class regex but do NOT structurally validate that all three forms are recognized. The risk: the helper covers only form (a) and STRANGE-categorizes all bare-§ references as unresolved, generating noise the inspection-triage block has to absorb. **Why this shape anyway:** writing the spec for all three resolver forms in the design.md inflates the design with parser semantics that belong in the helper code; the §3 P10 probe is structural (regex is in use) rather than exhaustive (all forms work). ARGUS should flag if my treatment of (b)+(c) is insufficiently named.

**Weak point 2 — check-6 LOOSE pre-ratification edge cases.**
The directive's a-priori LOOSE list (ariadne / sector-4 / railway_stoa drift acceptable per stoa--3na) is current-at-Arc-42-time scope-hint. If the consumer-workspaces.txt registry has gained a new workspace between directive ratification (2026-05-18 morning) and Arc 42 ship (later same day), OR if any of the three pre-named workspaces have been re-applied since directive draft, the check-6 logic's PRINCIPAL-gate trigger condition could either over-fire (mark a now-clean workspace STRANGE) or under-fire (silently swallow a new workspace's drift). **Why this shape anyway:** the A21 §25 gate trigger 1 catches the over-fire case by routing to user-tier-polybius rather than auto-resolving; the under-fire case is genuinely harder — the helper has no canonical way to distinguish "new workspace registered between directive and Arc-42-ship" from "pre-named workspace that drifted." The cleanest mitigation is the check-6 helper recording ALL workspaces' raw verdicts in the artifact (not just the deviant ones) so CATO's honesty audit can spot a silent-swallow. The design at §1.1.b artifact format does require per-workspace tables for check-6 — but ARGUS should sanity-check whether that's sufficient.

**Weak point 3 — check-7 trailer-grep idempotency across squash-merge body shapes.**
Live ground-check at design-time: `git log -1 --pretty='%(trailers:key=Co-Authored-By)' <sha>` emits empty for bb12806, non-empty (lowercase-by canonicalized) for the 4 post-Arc-35 ships. But the §6wp Arc 40 fix specifically targets the `--body` override regression at squash-merge time — a future Arc could regress by reverting to the override pattern, and the trailer-key formatter would emit empty silently (not differently — it's not "broken trailer", it's "no trailer at all"). The §3 probe P12 verifies case-insensitive trailer-key match in the helper, but does NOT verify the helper distinguishes "this commit was authored before §5.10 canon shipped (pre-dbb5b81 timeline)" from "this commit was authored after canon shipped but trailer absent (post-dbb5b81 = §25 escalation)". **Why this shape anyway:** my §1.1.a check-7 spec names this timeline-position distinction explicitly ("post-Arc-40 timeline-position annotation") and the A21 gate trigger 2 captures the escalation routing — but ARGUS should sanity-check whether the helper's date-vs-SHA-ordering logic is sufficient (commit dates can be rewritten; SHA-ancestry from dbb5b81 is structural — the helper SHOULD use ancestry not date).

**Weak point 4 — Fold-in scope-cohesion (5 candidates in one arc).**
The bundled scope (C1 + 4 fold-ins) is the largest single arc in the substrate's history (Arc 36 v2 at 5 candidates was comparable; Arc 25 at 4 was prior largest). CATO is mandatory per A24 specifically for the mech-check-results artifact honesty audit — but CATO will ALSO read the full diff, which now includes 7 files modified across (a) new substrate skill, (b) CAPTAIN_DAEDALUS.md canon addition, (c) MAJOR_PLINY.md canon addition, (d) 5 design.md edits across 3 design directories, (e) install.sh wiring. CATO craft-and-scope audit could surface the cohesion concern (is this one arc or 2-3?). **Why this shape anyway:** the directive A10-A13 explicitly invites the 5-candidate fold-in as "complementary" — A10 (1lm canon) provides the canon basis for A12 (mn3 cleanup) at the moment §6.9 ships; A11 (bn8) pairs with the current cron-driven engagement (first arc where polling-cron-PLINY is canonical, not operational); A13 (6k1) is a 1-probe deletion. Splitting into Arc 42 (C1 only) + Arc 43 (1lm+bn8+mn3+6k1) loses the self-application surface (the validate-spec skill IS a DAEDALUS-authored probe set per directive's stoa--bbi observation; shipping it WITHOUT the §6.9 canon means the skill's own probes can't cite the canon they exemplify). The cohesion bet is that the 5 candidates form a single coherent gauntlet target; if CATO disagrees, the right shape is a directive revision, not a probe revision.

**Weak point 5 — §6.9 self-application recursion (this design's own probes per §6.9).**
The A10 fold-in ships §6.9, which extends the §5.11 anchoring discipline to DAEDALUS-authored design.md probes. My §3 probes try to comply with the new canon at design-time (anchored regex, awk-scoping where applicable, ground-checked tool surfaces). But there's a subtle recursion: §6.9 clause 3 ("live round-trip at authoring time") requires me to have actually run every probe command literally against the current substrate state during draft. I have ground-checked the key shapes (bw output, git trailers, install.sh flags, _drafts/ absence, git status clean) but I have NOT literally run every one of the 36 probes against a build-state that doesn't yet exist (the validate-spec skill, the mn3-fixed design files, the §6.9 canon, the §6.2a canon). **Why this shape anyway:** the probes target post-ADA-build state; live round-trip at DAEDALUS-time would require building the artifact, which is ADA's seat. The §6.9 canon's clause 3 is satisfied for probes targeting pre-build state (I did run those); probes targeting post-build state (the structural majority) are deferred to ADA's pre-commit live-execution per the §5.2 grounding-check preamble inherited at §2.14. ARGUS should flag if this is too generous a reading of §6.9 clause 3 — strict reading might require this design to refuse all post-build-state probes until ADA build is partial-done, which would invert the gauntlet's seat-ordering. The honest framing: §6.9 clause 3 names a discipline for probes against EXISTING substrate state; design-time probes for not-yet-built state are §6.9 clause 4 ground-check + ADA's §5.2 live-execution territory.

**Weak point 6 — Inspection-agent triage shape (A8 ε inline) underestimating first-run strangeness frequency.**
A8 ε picks inline triage in validate-spec SKILL.md (POLYBIUS reads strangeness, triages manually) over A8 δ (separate `inspect-spec-validation-output` skill paralleling `inspect-script-output`). User-tier weakly leans ε; I pick ε. The risk: first-run-against-SPECIFICATION.md might surface 10-20 STRANGE-verdict items (38 ticket-ids in spec × ambiguity in surrounding-prose claim resolution; bare-§ resolver ambiguity per weak-point-1; 7 cross-workspace check-6 verdicts with mixed strict/loose interpretation). 20 strangeness items routed to manual POLYBIUS triage = the script-bloat anti-pattern's manual-triage cousin. **Why this shape anyway:** A23 hard-lock 2 ("No widening A8/A9 inspection-agent shape into heavy separate skill") explicitly forbids the δ pick mid-arc — if first-run reveals strangeness frequency justifying separate skill, that's an Arc 43+ ticket per A23 (NOT a mid-arc scope expansion). The ε pick is the directive-permitted shape; if it proves to scale poorly, the empirical anchor for a future δ-pick arc is the very first-run-strangeness count from THIS arc. ARGUS should flag if I'm under-pricing the operational cost of 20-item manual POLYBIUS triage.

---

## §5 Mech-check artifact specification (per A7 LOCKED + A26)

(Cross-ref: §1.1.b above defines the artifact format inline; this section names the **structural properties** the artifact MUST satisfy so VERA / CATO can probe them as separate concerns from the format itself.)

**Property 5.1 — Run metadata captured at every run.**
Every artifact run captures: (a) ISO-8601 UTC timestamp; (b) substrate SHA via `git rev-parse HEAD`; (c) spec file absolute path; (d) skill subtree SHA via `git rev-parse HEAD:substrate/skills/validate-spec/`. Probe P7 verifies. Property satisfies A20 reproducibility — any future re-run against the same substrate SHA + spec SHA should produce identical results (modulo bw / consumer-workspace state which is external).

**Property 5.2 — Per-check verdict + evidence trail.**
Every check writes: (a) verdict line (PASS / FAIL / STRANGE); (b) per-item table for items the check enumerates over (per-reference / per-ticket / per-workspace / per-commit); (c) verbatim command(s) the helper executed, in the "Evidence trail per check" section at artifact bottom. A20 anti-motivated-reasoning property: every PASS is reproducible from recorded commands.

**Property 5.3 — Strangeness section is first-class output.**
The artifact's "Strangeness for inspection-agent triage" section is structurally required (not exception-only). Even a CLEAN run emits the section header with `(none)` body. This lets POLYBIUS's structured re-read identify "no strangeness" as a structural property, not infer it from section absence.

**Property 5.4 — PRINCIPAL-gate section captures A21 trigger states.**
The artifact's "PRINCIPAL-gate findings" section explicitly enumerates which of the 3 A21 trigger conditions fired (or did not). Empty section = section header present with `(no §25 trigger fired)` body. Populated entries: trigger-condition-N + evidence + surfacing-posture (filed comment ID on stoa--utn).

**Property 5.5 — Explicit carve-out attestation visible to grep.**
Per A7 LOCKED: bb12806 carve-out attestation must be greppable in the artifact (probe P8). The attestation is NOT a passing-mention; it's a structured statement of (a) which SHA is carved out, (b) why (the §6wp empirical anchor), (c) the explicit timeline scope (pre-Arc-40 timeline-position; post-Arc-40 missing trailer ≠ carve-out, ≠ §25 gate trigger 2).

---

## §6 Inspection-agent triage shape (A8 ε — inline triage block in SKILL.md)

Per A8 ε pick: the validate-spec SKILL.md carries an **inline triage block** that instructs POLYBIUS (and any other reader) how to route the artifact's strangeness findings. NOT a separate `inspect-spec-validation-output` skill (deferred to future arc per A23 hard-lock 2 if first-run strangeness frequency justifies).

**Shape (DAEDALUS authors; ADA copies verbatim into SKILL.md):**

The triage block appears as a SKILL.md subsection titled `## POLYBIUS triage protocol` (parallel to the inspect-script-output skill's SKILL.md section of the same name — operator muscle-memory preserved). Body:

> When validate-spec emits a mechanical-check-results.md artifact with `STRANGE`-verdict items or non-empty `PRINCIPAL-gate findings`, POLYBIUS routes per `operating-disciplines.md` §27.2 step 3:
>
> **Routine technical-tier findings → POLYBIUS fixes inline.**
>
> Examples:
> - check-1 STRANGE item: a §-reference's anchor includes a trailing alphabetic character (e.g., `§13.10a`) the helper's resolver didn't normalize. POLYBIUS updates the helper's resolver to handle the suffix; re-runs the skill; check-1 returns PASS. Routine fix-now per `MAJOR_POLYBIUS.md` §4.8.
> - check-3 STRANGE item: an open ticket is mentioned in §13.x prose but the mention is a cross-ref-comment-only (not a section that "places" the ticket per §12.5 dynamic walk). POLYBIUS surfaces the ambiguity to user-tier (this is structurally a §12.3 audit finding the spec authoring chose to leave dynamic); MAY file a refinement ticket against §12.3 clarification.
>
> **PRINCIPAL-gate findings → workflow PAUSES per `operating-disciplines.md` §25.3 BLOCK-not-TAG.**
>
> Three pre-flagged gates (per Arc 42 directive A21):
>
> 1. **check-6 strict-vs-loose divergence.** PLINY immediately surfaces to user-tier-polybius with `[for: user-tier-polybius]` + cite the artifact's check-6 table. Do NOT auto-resolve; PRINCIPAL chooses interpretation.
> 2. **check-7 post-Arc-40 trailer-canon failure.** PLINY surfaces as `[for: user-tier-polybius]` + cite the failing commit SHA + the `MAJOR_PLINY.md` §5.10 canon site that should have prevented the failure. Substance disagreement; do NOT fix-and-ship; surface canon gap.
> 3. **Any mechanical check genuinely FAILS** (not STRANGE; FAIL). Surface with the failing evidence; PRINCIPAL ratifies fix-now-this-arc vs document-as-residue-and-ship vs spec-edit-and-re-run.
>
> POLYBIUS is the seat that makes the routing call. The skill emits the structured artifact; POLYBIUS reads it and routes. PRINCIPAL is the exception-handler when the gate fires.
>
> **First-run strangeness is GOOD signal (per Arc 42 directive A20).** The team is authoring its own falsification criteria; first-run-discovers-strangeness validates the criteria are actually checking something rather than rubber-stamping the team's existing assumptions. Do NOT auto-PASS items POLYBIUS cannot independently verify. Strangeness routes to triage (above) OR PRINCIPAL escalation (above).
>
> **Future-arc accretion (A23 hard-lock 2 boundary).** If first-run strangeness frequency reveals manual POLYBIUS triage doesn't scale (e.g., 20+ strangeness items per run), a future arc may ship a separate `inspect-spec-validation-output` skill paralleling `substrate/skills/inspect-script-output/`. That's an Arc 43+ ticket per A23 — NOT a mid-arc scope expansion of this skill. The ε pick (inline triage) is the directive-permitted shape for Arc 42 ship.

---

## §7 Out of scope

Bullet list of related concerns this design deliberately does not address:

- **Building Pass 10 stellation behavioral-validation infrastructure** — per A23 hard-lock 3 + §13.12 (separate concern; PRINCIPAL drives setup per §13.12).
- **Restructuring the 7 mechanical checks beyond A5 LOCKS** — per A23 hard-lock 1. If first-run reveals a check is structurally wrong (e.g., check-3's §13.x placement walk produces noise the spec design intentionally tolerates), the right shape is a SPECIFICATION.md edit + re-run, not a check-restructure.
- **Widening A8/A9 inspection-agent shape into heavy separate skill** — per A23 hard-lock 2. δ pick deferred to Arc 43+ if first-run strangeness frequency justifies (see weak-point 6).
- **Extending validate-spec to non-spec-met checks** (e.g., consumer-workspace product-feature validation; non-substrate-canon checks) — per §13.14 hard-lock.
- **Building meta-agent for cross-generation lineage analysis** (§10.1 property 3 / §12.5) — per §13.14 hard-lock.
- **Shipping deferred-with-gating items (stoa--tvc + stoa--myd per §13.9)** — they have explicit gating criteria; spec-met is achieved with them open-with-plan.
- **stoa--lyw `/resume` invocation discipline canon** — per §13.14 (sufficient for spec-met as recording-only).
- **stoa--sp1 cross-substrate utility skill ports** — Arc 43+ per §13.9a (NOT a blocker for spec-met / stellation dispatch).
- **stoa--3na consumer-workspace apply sessions** — per A21 LOOSE pre-ratification + §13.13 criterion 4 stoa--3na disposition; ariadne / sector-4 / railway_stoa drift is accepted as documented residue at Arc 42 ship.
- **Promoting validate-spec to user-tier or making it a CAPTAIN seat** — per A23 hard-lock 2 spirit (substrate skill is the right shape at Arc 42; CAPTAIN-seat promotion is Arc 43+ if pattern proves out).

---

## §8 Cross-references

- `substrate/arcs/arc-42-build-directive.md` — the LOCKED directive this design builds against.
- `SPECIFICATION.md` §13.11 — Pass 9 spec (the validate-spec skill's structural requirements).
- `SPECIFICATION.md` §13.13 — spec-met criteria 1-5 (what "the team meets the spec" means).
- `SPECIFICATION.md` §13.16 — definition of done.
- `SPECIFICATION.md` §12.1-§12.5 — current-state contracts that mech-checks validate against.
- `substrate/skills/check-substrate-updates/` — precedent shape (mechanical script half of §27 pattern).
- `substrate/skills/inspect-script-output/` — precedent shape (inspection-agent half of §27 pattern); the parallel "POLYBIUS triage protocol" SKILL.md section is the operator-muscle-memory target.
- `substrate/skills/save-verdict/` — Python-helper precedent (Arc 39; canon for script-invocation-contract + sys.path manipulation for sibling _lib).
- `substrate/operating-disciplines.md` §27 — mechanical-script / agent-inspection split pattern (the shape validate-spec follows).
- `substrate/CAPTAIN_VERA.md` §5.11 — anchoring discipline (verification-side sibling to the new CAPTAIN_DAEDALUS.md §6.9 this arc ships).
- `substrate/MAJOR_PLINY.md` §6.2 — surface-and-wait default mode (existing canon; §6.2a is the new mode this arc adds).
- `substrate/MAJOR_PLINY.md` §5.10 — squash-merge `--body` override discipline (Arc 40 ship; the canon check-7 verifies against).
- `substrate/operating-disciplines.md` §28 — Co-Authored-By trailer canon.
- `substrate/operating-disciplines.md` §25 — PRINCIPAL-gate discipline (A21 routing partner).
- `agents/design/arc-40/design.md` — mn3 fix-1 (p15), fix-2 (p18), fix-3 (p24) sites.
- `agents/design/arc-41/design.md` — mn3 fix-4 (§4.5.2), fix-5 (§4.12.2 + §4.12.3) sites.
- `agents/design/arc-25/design.md` §9.3 — 6k1 P10 deletion site.
- bw tickets: stoa--utn (engagement coordination); stoa--1lm (A10); stoa--bn8 (A11); stoa--mn3 (A12); stoa--6k1 (A13); stoa--3na (check-6 LOOSE pre-ratification); stoa--bbi (refined-principle accretion observation surface).
