---
name: validate-spec
description: |
  Run the 7 mechanical checks defined at SPECIFICATION.md §13.11 against the current substrate state — every §-reference resolves, every cited stoa--<id> ticket exists with claimed status, every open ticket is placed in some §13.x section, git status clean modulo §12.4 ignorables, _drafts/ empty or justified, check-substrate-updates shows no drift (with A21 LOOSE pre-ratification for ariadne / sector-4 / railway_stoa per stoa--3na), and §28 Co-Authored-By trailers present on post-Arc-35 squash-merges with explicit bb12806 carve-out. Emits a structured Markdown artifact at agents/observation/spec-validation/mechanical-check-results.md with per-check verdict + independent evidence trail (per Arc 42 A20 motivated-reasoning mitigation: every PASS is reproducible from the recorded commands). Drift is informational — the artifact carries the verdict, not the exit code. STRANGE-verdict items route to inline POLYBIUS triage (see below); pre-flagged A21 PRINCIPAL-gate triggers escalate to user-tier-polybius. Triggers on "validate the spec", "run mechanical checks", "does the substrate meet spec", "Pass 9 mechanical-check", "spec-validation run".
author: Denson Smith
---

# validate-spec — mechanical-check pass for SPECIFICATION.md

## Why this skill exists

`SPECIFICATION.md` is the durable contract for what "the team meets the spec" means. Without a mechanical-check pass, the team's confidence that substrate state matches spec rests on whichever agent last looked at whichever surface — and the surfaces (§-refs, bw tickets, git state, cross-workspace drift, trailer canon) drift independently. Pass 9 of the workplan (per `SPECIFICATION.md` §13.11) is the **mechanical-check pass that validates substrate state matches spec**.

This skill ships the mechanical half of the §27 mechanical-script / agent-inspection split pattern for spec-validation. Mechanical script (this skill) runs the 7 deterministic checks and emits structured evidence. Agent inspection (POLYBIUS, per the inline triage block below) reads the strangeness findings and routes them — fix-inline for routine technical-tier items, surface to user-tier for the 3 pre-flagged A21 PRINCIPAL-gate triggers.

The build-then-use design is deliberate: this skill is authored at Arc 42 AND run once against `SPECIFICATION.md` as part of the same ship, with the run's artifact committed alongside the skill (per A26 self-application). Evidence-of-use, not just evidence-of-existence.

## When to invoke

Invoke when:

- The PRINCIPAL asks to validate the spec / "run the mechanical checks" / "are we still meeting spec".
- A substrate canon edit has landed and you want to confirm none of the 7 mechanical invariants broke.
- Pre-stellation (Pass 10) sanity sweep — confirm spec-met BEFORE behavioral validation.
- After a multi-arc autonomous engagement closes — confirm the team's bookkeeping is intact.

Do **not** invoke for:

- Behavioral-correctness validation (that's Pass 10 stellation; this skill is mechanical only).
- Spec-meaning validation (does the spec say the right things?). This skill checks consistency of substrate state vs. spec claims; the spec's content quality is PRINCIPAL judgment.
- Cross-substrate utility-skill validation (those have their own per-skill probes; this skill is spec-targeted).
- Auto-fixing drift (this skill is read-only; remediation flows through `check-substrate-updates apply.sh` for substrate drift; through POLYBIUS for spec / bw ticket / git-state drift).

## How to invoke

```bash
bash substrate/skills/validate-spec/check.sh
```

Default behavior: runs against `SPECIFICATION.md` at the repo root; writes the artifact to `agents/observation/spec-validation/mechanical-check-results.md`. Both paths are resolved against the repo root (`git rev-parse --show-toplevel`).

Optional flags:

```bash
bash substrate/skills/validate-spec/check.sh \
  --spec <alternate-spec-path> \
  --write-artifact <alternate-artifact-path>
```

The script prints a per-check verdict line to stdout (one per check: `check-N: PASS|FAIL|STRANGE — <one-line evidence>`) and writes the full structured artifact with per-item tables + verbatim evidence trail. **Exit code is always 0 on successful execution per A20** (drift is informational; the artifact carries the verdict, not the exit code). Exit 2 reserved for "could not run" (python or git missing).

## The 7 mechanical checks

| # | Check | PASS criterion (load-bearing) |
|---|-------|-------------------------------|
| 1 | Every `§X` / `§X.Y` reference in `SPECIFICATION.md` resolves to its named canon file. | Every cited `<canon-file>.md §<anchor>` pair resolves: target file exists; target file contains a heading line whose §-anchor matches the cited value. Bare `§X` references default to `operating-disciplines.md` per `SPECIFICATION.md` line 7 "Reading note." |
| 2 | Every cited `stoa--<id>` ticket in `SPECIFICATION.md` exists in bw with claimed status. | Each unique ticket id grep-extracted from spec: (a) `bw show <id>` succeeds (ticket exists); (b) the status glyph on line 1 (`# ○` open / `# ✓` closed) matches what the surrounding prose claims (e.g., "closed", "DONE", "DROPPED", "deferred"). |
| 3 | `bw list --status open --all` tickets all placed in some §13.x ticket-placing section. | For each open ticket id, search `SPECIFICATION.md` §13.x bodies. Any open ticket NOT found in any §13.x section is a FAIL (the §12.3 / §12.5 dynamic-walk semantic check). |
| 4 | `git status` shows no uncommitted changes except §12.4-ignorable state files. | `git status --porcelain` filtered to remove `.claude/.substrate-last-check` (and any other §12.4-named ignorables); result must be empty. |
| 5 | `_drafts/` empty OR contains only in-flight-engagement docs per §12.4. | `_drafts/` is absent OR empty OR every file inside is referenced from an open `engagement coordination` ticket per `bw list --status open --all`. |
| 6 | `check-substrate-updates` returns "no drift" across registered consumer workspaces. **A21 LOOSE pre-ratification.** | Each per-workspace summary line carries a composite-status token (`CURRENT`, `DRIFTED + MISSING`, `NOT-STOA-DEPLOYED`, etc.). `CURRENT` = clean. A21 LOOSE pre-ratification per stoa--3na: ariadne / sector-4 / railway_stoa MAY emit any non-`CURRENT` composite (drift accepted as documented residue). Any workspace OUTSIDE the pre-named list emitting non-`CURRENT` = STRANGE (route to inspection triage; potentially A21 §25 trigger 1). `NOT-STOA-DEPLOYED` is informational — workspace exists in registry but has no `.claude/MAJOR_POLYBIUS*.md`; not a drift FAIL. |
| 7 | §28 Co-Authored-By trailers on post-Arc-35 squash-merge commits with EXPLICIT CARVE-OUT for `bb12806`; commits AT-OR-AFTER Arc 40 ship (`dbb5b81` ancestry) MUST carry trailers. | Walk `git log --first-parent main --grep='^Arc '` — for each squash-merge commit, `git log -1 --pretty='%(trailers:key=Co-Authored-By)'` MUST be non-empty UNLESS the commit SHA starts with `bb12806` (carve-out). For commits reachable from `dbb5b81` ancestry (post-Arc-40 timeline-position), missing trailer = substance disagreement (A21 §25 PRINCIPAL-gate trigger 2). For commits NOT reachable from `dbb5b81` (pre-canon), missing trailer is silent-failure-class closed by Arc 40 ship — recorded as PASS-PRE-CANON. |

## Artifact path contract

The skill writes to a single canonical path:

```
agents/observation/spec-validation/mechanical-check-results.md
```

Structure (per A7 LOCKED + A26):

- **Run metadata header** — ISO-8601 UTC timestamp, substrate SHA at run-time, spec path, skill subtree SHA at run-time. (Property 5.1: every run is reproducible against the same substrate SHA + spec SHA.)
- **Overall verdict** — `all-PASS (7/7)` / `<N>-of-7-PASS-with-strangeness` / `<N>-of-7-PASS-with-failure`.
- **Per-check results** — one section per check with verdict, summary, per-item table (truncated to 50 items in the inline JSON block; full data in the evidence trail at artifact bottom).
- **Strangeness section** — first-class output (Property 5.3): even a CLEAN run emits the section with `(none)` body, so POLYBIUS can identify no-strangeness as a structural property.
- **PRINCIPAL-gate findings** — explicit enumeration of which A21 trigger conditions fired (or `(no §25 trigger fired)` if none). (Property 5.4.)
- **Evidence trail per check** — verbatim commands the helper executed + raw stdout captured (truncated to 8000 chars per check for artifact size). A20 anti-motivated-reasoning property: every PASS is reproducible from the recorded commands.

## POLYBIUS triage protocol

When validate-spec emits a `mechanical-check-results.md` artifact with `STRANGE`-verdict items or non-empty `PRINCIPAL-gate findings`, POLYBIUS routes per `substrate/operating-disciplines.md` §27.2 step 3:

### Routine technical-tier findings → POLYBIUS fixes inline

Examples:

- **check-1 STRANGE item**: a §-reference's anchor includes a trailing alphabetic character (e.g., `§13.10a`) the helper's resolver didn't normalize. POLYBIUS updates the helper's resolver to handle the suffix; re-runs the skill; check-1 returns PASS. Routine fix-now per `substrate/MAJOR_POLYBIUS.md` §4.8.
- **check-3 STRANGE item**: an open ticket is mentioned in §13.x prose but the mention is a cross-ref-comment-only (not a section that "places" the ticket per §12.5 dynamic walk). POLYBIUS surfaces the ambiguity to user-tier (this is structurally a §12.3 audit finding the spec authoring chose to leave dynamic); MAY file a refinement ticket against §12.3 clarification.

### PRINCIPAL-gate findings → workflow PAUSES per `substrate/operating-disciplines.md` §25.3 BLOCK-not-TAG

Three pre-flagged gates (per Arc 42 directive A21):

1. **check-6 strict-vs-loose divergence.** Any workspace OUTSIDE the A21 LOOSE pre-named list (ariadne / sector-4 / railway_stoa per stoa--3na) emits a non-`CURRENT` composite. PLINY immediately surfaces to user-tier-polybius with `[for: user-tier-polybius]` + cite the artifact's check-6 table. Do NOT auto-resolve; PRINCIPAL chooses interpretation (strict per-workspace or extended LOOSE list).
2. **check-7 post-Arc-40 trailer-canon failure.** Any commit reachable from `dbb5b81` ancestry that emits empty trailers. Arc 40 §5.10 canon should have prevented this; failure indicates canon gap (NOT a typo to fix-and-ship). PLINY surfaces as `[for: user-tier-polybius]` + cite the failing commit SHA + the `substrate/MAJOR_PLINY.md` §5.10 canon site that should have prevented the failure. Substance disagreement; do NOT fix-and-ship; surface canon gap.
3. **Any mechanical check genuinely FAILS** (not STRANGE; FAIL). Surface with the failing evidence; PRINCIPAL ratifies fix-now-this-arc vs document-as-residue-and-ship vs spec-edit-and-re-run.

POLYBIUS is the seat that makes the routing call. The skill emits the structured artifact; POLYBIUS reads it and routes. PRINCIPAL is the exception-handler when the gate fires.

### First-run strangeness is GOOD signal

Per Arc 42 directive A20: the team is authoring its own falsification criteria. First-run-discovers-strangeness validates the criteria are actually checking something rather than rubber-stamping the team's existing assumptions. Do NOT auto-PASS items POLYBIUS cannot independently verify. Strangeness routes to triage (above) OR PRINCIPAL escalation (above).

### Future-arc accretion (A23 hard-lock 2 boundary)

If first-run strangeness frequency reveals manual POLYBIUS triage doesn't scale (e.g., 20+ strangeness items per run), a future arc may ship a separate `inspect-spec-validation-output` skill paralleling `substrate/skills/inspect-script-output/`. That's an Arc 43+ ticket per A23 — NOT a mid-arc scope expansion of this skill. The inline-triage shape (this section) is the Arc 42 directive-permitted shape.

## What this skill is NOT

- **Not a behavioral-validation skill.** Pass 10 stellation handles behavioral validation; this skill is Pass 9 mechanical-check only.
- **Not a fixer.** Read-only. Drift is informational; remediation routes through the appropriate other surface (`check-substrate-updates apply.sh`, POLYBIUS-led ticket cleanup, etc.).
- **Not a substitute for `check-substrate-updates`.** check-6 *invokes* check-substrate-updates and parses its output; the cross-workspace drift detection skill is canonical for the "is my substrate current" question. This skill aggregates check-substrate-updates into the broader spec-met verdict.
- **Not exit-code-driven.** Exit is always 0 on successful execution. The artifact carries the verdict. Operators reading exit codes alone will miss the strangeness routing.

## Related substrate

- `substrate/skills/check-substrate-updates/` — invoked by check-6 (composite-status parser parses its per-workspace output).
- `substrate/skills/inspect-script-output/` — precedent shape for the agent-inspection half of §27 (the A8 ε pick on this skill is inline triage, not a separate inspect-spec-validation-output skill; future-arc accretion noted above).
- `substrate/skills/save-verdict/` — Python-helper precedent (Arc 39 canon for script-invocation-contract + sys.path manipulation for sibling _lib).
- `substrate/operating-disciplines.md` §27 — mechanical-script / agent-inspection split pattern this skill follows.
- `substrate/operating-disciplines.md` §25 — PRINCIPAL-gate discipline (A21 routing partner).
- `substrate/operating-disciplines.md` §28 — Co-Authored-By trailer canon (check-7 verifies against).
- `substrate/CAPTAIN_DAEDALUS.md` §6.9 — probe-grounding discipline at the authoring seat (this skill's helpers self-apply: anchored regexes, ground-checked tool surfaces, live round-trip).
- `substrate/CAPTAIN_VERA.md` §5.11 — verification-side anchoring discipline (parallel canon to §6.9).
- `substrate/MAJOR_PLINY.md` §5.10 — squash-merge `--body` override discipline (Arc 40 ship; check-7 verifies against this canon).
- `substrate/MAJOR_PLINY.md` §6.2a — multi-arc autonomous mode (per stoa--bn8; relevant when running this skill as part of a multi-arc engagement closeout).
- `SPECIFICATION.md` §13.11 — Pass 9 spec (the structural requirements this skill implements).
- `SPECIFICATION.md` §13.13 — spec-met criteria 1-5.
- `SPECIFICATION.md` §13.16 — definition of done.
