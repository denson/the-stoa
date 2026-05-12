# Arc 24 build directive — Comms-hygiene substrate-DNA: subagent status via bw + orchestrator dispatch hygiene + confabulation discipline

**Audience:** the fresh Claude Code session opened to build Arc 24 deliverables (MAJOR_PLINY).
**Authored by:** project-tier MAJOR_POLYBIUS + the PRINCIPAL (Denson Smith).
**Status:** active directive. **DO NOT DISPATCH UNTIL ARC 23 CLOSES.** Arc 23 (`stoa--pmp`) is currently in flight; its ADA build phase will edit substantially overlapping substrate files. Arc 24 dispatches against post-Arc-23 main so it inherits Arc 23's verification-complexity framework as part of its base.
**Bw ticket:** to be filed as the Arc 24 epic; this directive references the three child tickets by ID (`stoa--odh`, `stoa--nvl`, `stoa--ioy`).
**Builds on:** Arcs 1-23 (the-stoa main as of Arc 23 ship commit — TBD; should be tagged at Arc 23 close).

**Your one job:** ship comms-hygiene as substrate DNA — every CAPTAIN heartbeats progress via bw on its dispatch ticket; every orchestrator monitors via Monitor + bw-poll bridge; every seat says "uncertain, checking" when state-vs-claim mismatches surface. The 2026-05-12 ariadne PLINY incident (PLINY confabulated "I never made the Agent tool call" when it had, surfaced only because PRINCIPAL caught it via the Claude Code Desktop Tasks pane) showed that the substrate's existing coordination disciplines (radio-check for POLYBIUS-pair only, surface-and-wait for PLINY-to-POLYBIUS only) leave the orchestrator-to-CAPTAIN axis structurally blind. This arc closes that gap.

Three tickets, one coherent push:
- **stoa--odh** — Universal CAPTAIN heartbeat-and-read-before-write discipline (cooperative-yield via bw)
- **stoa--nvl** — Orchestrator-side dispatch hygiene: Monitor + bw-poll bridge + tool-loading + TaskOutput-forbidden-on-Agents
- **stoa--ioy** — Confabulation-under-uncertainty discipline ("uncertain, checking" over assertion)

All three trace to the same 2026-05-12 incident; each addresses a distinct failure mode. The three combined make the comms architecture two-way in user-visible behavior (asymmetrically implemented, but the asymmetry never leaks).

This is a multi-concern arc with ~20-30 substrate-prose deliverables across ~12 files. Per MAJOR_POLYBIUS §5.4, external review is recommended before dispatch if scope warrants; given Arc 24 is smaller than Arc 23 and the empirical anchor is well-documented in the three ticket bodies, §5.4 review is at PRINCIPAL discretion.

---

## Comms — autonomous mode via bw, radio-check protocol

POLYBIUS (substrate-tier CoS, separate Claude Code session) and you both communicate via comments on the Arc 24 epic. PRINCIPAL is **not** the relay for routine status — beadwork is.

**bw command syntax** is in `substrate/MAJOR_PLINY.md` §6.1. Critical: `bw comment <id> "text"` is positional, no `-m` flag. `bw close <id> --reason "text"` — `--reason` is a flag.

**Polling discipline** per `substrate/operating-disciplines.md` §7 (surface-and-wait + radio-check). On dispatch, post an initialization handshake comment on the Arc 24 epic naming your cron id (if you set one up) and your cadence. Heartbeat every ≤30 min unless surface-and-wait-blocked.

POLYBIUS is in autonomous mode for this engagement. PRINCIPAL is exception-handler — project-direction calls, ship/no-ship, substance disagreement after one round, authorship/copyright/Denson-final-say content, irreducible ambiguity, peer silence > 60 min, arc closes.

**Note on this arc specifically:** the discipline you're building IS the discipline you're using. As you dispatch CAPTAINs in this arc, those CAPTAINs read the *new* version of their own role files (which carry the heartbeat-and-read-before-write discipline being authored). Self-referential, not circular. The CAPTAINs operate per the new discipline as they help author it. Worked example of "substrate updating itself in flight."

---

## Read first

Before any design or build work, read in order:

1. **The three ticket bodies in full:** `bw show stoa--odh`, `stoa--nvl`, `stoa--ioy`. Each carries empirical anchor + discipline statement + Phase-A LOCKED architectural decisions + substrate touch-points + cross-references. DAEDALUS treats each body as additional spec.

2. **`substrate/operating-disciplines.md` (post-Arc-23)** — at Arc 23 ship time this will carry §1-§17. You will add new sections per A4 below. Read §7 (POLYBIUS-pair coordination) and §11 (autonomous-mode-setup) carefully; they're the existing comms-hygiene foundation you're extending.

3. **`substrate/MAJOR_PLINY.md` (post-Arc-23)** — receives dispatch-hygiene section (per nvl); receives verify-then-execute scope-broadening (per ioy).

4. **`substrate/MAJOR_POLYBIUS.md` (post-Arc-23)** — receives analogous dispatch-hygiene (per nvl, for pair-programming-mode CAPTAIN dispatches) + confabulation cross-ref (per ioy).

5. **All CAPTAIN role files (`substrate/CAPTAIN_*.md`)** — each receives a heartbeat-and-read-before-write section (per odh). Inventory at dispatch time; substrate may have grown new CAPTAINs since Arc 23.

6. **`~/.claude/skills/save-verdict/SKILL.md` (user-tier reference only)** — read for context on how Arc 23 landed Option A. NOT touched by Arc 24.

7. **Anthropic-side facts referenced in `stoa--nvl`:** `Monitor` released v2.1.98 on 2026-04-09; `TaskOutput` deprecated; subagents can't `TaskStop` (issue #23154); no tool enumerates running tasks (issues #29011, #49140); `task_id` must be materialized to bw at dispatch time.

8. **Workspace memory `feedback_no_confabulated_rationales.md`** in `ariadne-core-workspace/memory/` — source artifact for the confabulation discipline (per ioy). DAEDALUS reads as input prose for §17-or-§18 confabulation section.

---

## Phase A — Architectural decisions (LOCKED pre-dispatch)

Settled during directive authoring. You do NOT surface these as design questions.

### A1. One arc, four phases, one gauntlet — LOCKED

Three tickets cluster into one coherent substrate update. All trace to the same 2026-05-12 ariadne incident; all touch the comms-hygiene file set. Single DAEDALUS design covering all three. Single ARGUS audit. Single ADA worktree on `arc-24/build`. Verifiers (VERA / CATO / ZENO) each one pass over the integrated diff.

Phasing:

| Phase | Seat(s) | Output |
|---|---|---|
| 1 | DAEDALUS + ARGUS | `agents/design/arc-24/design.md` — integrated design covering all 3 tickets' substrate touch-points. ARGUS cold-audits before ADA dispatches. |
| 2 | ADA | feature branch `arc-24/build` covering operating-disciplines.md additions, MAJOR_PLINY.md, MAJOR_POLYBIUS.md, every CAPTAIN role file, plus agent-author template/skill scaffold updates. |
| 3 | VERA + CATO + ZENO | parallel verification pass. VERA probes per-file content + verifies the canonical Monitor poll-loop template empirically (smoke beat). CATO cold-reads entire diff for wording drift / cross-reference correctness / scope creep. ZENO checks spec-vs-result. |
| 4 | PLINY + smoke + ship | smoke beats (install.sh dry-run lists all touched files; grep beats per substrate file; canonical poll-loop template runs successfully against a real bw ticket). PR opened. PLINY runs `gh pr merge` after clean PASS. All 3 tickets closed. |

### A2. odh's heartbeat-and-read-before-write discipline lands across every CAPTAIN role file — LOCKED

The discipline is universal-CAPTAIN, not seat-specific. Every CAPTAIN role file gets a heartbeat-and-read-before-write subsection (in the seat's "disciplines specific to this seat" section). The substance is the same across all CAPTAINs; the wording adapts to seat (e.g., VERA's heartbeats reference probe execution; ADA's reference build phases; CATO's reference review phases). DAEDALUS authors a canonical subsection then per-CAPTAIN customizes the wording.

### A3. CAPTAIN-side `Monitor` and `run_in_background: true` Bash both forbidden — LOCKED

Per odh A5 + nvl B5: CAPTAIN role files explicitly prohibit firing `Monitor` and prohibit `run_in_background: true` on Bash from within a CAPTAIN dispatch. Both are orphan-bug surfaces ([issue #23154](https://github.com/anthropics/claude-code/issues/23154)). Background work belongs to the orchestrator tier.

### A4. operating-disciplines.md placement — DAEDALUS picks subject to constraint

Post-Arc-23 op-disc carries §1-§17. The Arc 24 additions land either:
- **As new top-level sections** (§18 = subagent-status-via-bw + Monitor pattern; §19 = confabulation discipline); OR
- **Expanding §7** (POLYBIUS-pair coordination expands to "coordination across all seats including subagent dispatches" with subsections); §19 still top-level for confabulation; OR
- **Hybrid** (subagent-status subsection under §7; orchestrator-dispatch-hygiene as new §18; confabulation as new §19)

DAEDALUS picks the placement that's most legible to a cold reader. ARGUS audits placement choice during Phase 1 critique.

### A5. INCOMPLETE / UNVERIFIABLE verdict shapes inherited from Arc 23 — LOCKED

Arc 23 lands the new verdict shapes in operating-disciplines.md §15 + save-verdict skill. Arc 24's verifiers (VERA, CATO, ZENO during Phase 3) operate under the new framework — they classify probes per quadrant + may use INCOMPLETE/UNVERIFIABLE verdicts where the framework applies. Worked example: VERA probing the canonical poll-loop template empirically is easy-easy quadrant; ARGUS auditing the "every CAPTAIN role file is consistently updated" claim is hard-hard quadrant (UNVERIFIABLE territory — the verification space is unbounded across all current and future CAPTAINs).

### A6. CAPTAIN inventory taken at dispatch time, not pre-locked — LOCKED

The directive does not enumerate every CAPTAIN role file by name. The substrate may have grown new CAPTAINs since Arc 23 ship (e.g., ATTICUS, PYTHAGORAS, CODEX, LEX pair-programmer MAJORs may have been authored). At Phase 1 entry, DAEDALUS runs `ls substrate/CAPTAIN_*.md substrate/MAJOR_*.md` to confirm the actual inventory, then includes every found file in the design's touch-point list.

### A7. agent-author template/skill scaffold update — DAEDALUS picks scope

If a substrate-resident agent-author template or skill exists (per the `agent-author` skill in the Stoa team), the heartbeat-and-read-before-write discipline lands in the canonical new-CAPTAIN scaffold so future CAPTAINs inherit it by default. DAEDALUS surfaces the scaffold file path during Phase 1; ADA edits it in Phase 2.

### A8. Canonical Monitor poll-loop template lives in MAJOR_PLINY.md and MAJOR_POLYBIUS.md — LOCKED

Per nvl B4: both orchestrator role files carry the canonical bash poll-loop template. The two files reference the same template (one substrate-canonical version, cross-referenced). DAEDALUS chooses whether to inline both or inline one + cross-reference; the substance is the same.

### A9. Confabulation discipline placement — LOCKED universal-seat in operating-disciplines.md

Per ioy C1: discipline is universal-seat (POLYBIUS, PLINY, all CAPTAINs), not per-seat. Substrate-canonical home is operating-disciplines.md (new section per A4). Per-role-file cross-refs are light-touch — MAJOR_POLYBIUS, MAJOR_PLINY get a brief cross-ref; CAPTAIN role files do NOT each get a section (would bloat without value). DAEDALUS surfaces if any specific CAPTAIN warrants seat-specific guidance.

### A10. Verb-level cue canonical phrasing — DAEDALUS picks

Per ioy C2: the substance is "explicit admission of uncertainty + commitment to verification." DAEDALUS picks the canonical phrasing for substrate prose (e.g., "uncertain, checking" / "let me verify" / "I don't know yet, looking now"). The role files do not enforce a literal string; they describe the SHAPE.

### A11. Authorship attribution — IMMUTABLE

All edits credit Denson Smith. No author field gets a different name. No exception under any phase.

---

## Phase 1 — Design (DAEDALUS + ARGUS)

DAEDALUS produces `agents/design/arc-24/design.md` integrating all 3 tickets. Structure:

1. **Frame** — the 2026-05-12 ariadne PLINY incident as empirical anchor + the three distinct failure modes (comms architecture, tooling discipline, verb-level discipline) + the structural-asymmetry insight (upward push via Monitor, downward pull via read-before-write).
2. **odh: heartbeat-and-read-before-write discipline** — canonical subsection text + per-CAPTAIN customization examples for VERA, CATO, ARGUS, ZENO, ADA, DAEDALUS, STRABO, HERALD, BARTLEBY, CURATOR (and any new CAPTAINs found at inventory).
3. **nvl: orchestrator dispatch hygiene + Monitor pattern** — canonical poll-loop template + tool-loading section + TaskOutput-forbidden-on-Agents wording + task_id materialization sequence + PushNotification orthogonality.
4. **ioy: confabulation discipline** — discipline statement + three application patterns + verb-level cue + cross-ref to verify-then-execute.
5. **operating-disciplines.md additions** — exact prose for new sections per A4 placement.
6. **MAJOR_PLINY.md updates** — dispatch-hygiene section + verify-then-execute scope-broadening + canonical poll-loop template (per A8).
7. **MAJOR_POLYBIUS.md updates** — analogous + confabulation cross-ref (per A9).
8. **Per-CAPTAIN role file customizations** — exact wording for each file's heartbeat-and-read-before-write subsection.
9. **agent-author template/skill scaffold updates** — exact scaffold text per A7.
10. **Self-referential acknowledgment** — the arc modifies the role files of the very seats authoring/verifying the arc. Worked example for cold readers; not a circular dependency.

ARGUS cold-audits when DAEDALUS surfaces. Looks for: wording drift across CAPTAIN role files (the same discipline must read consistently across 10+ files); missing CAPTAINs in the inventory; missing cross-references; canonical poll-loop template bash-syntax errors (test by reading critically); scope creep beyond the three tickets; authorship attribution (immutable rule); confabulation-discipline phrasing that itself sounds confabulated (irony surface — be careful).

ARGUS verdict gate: ADA does not dispatch until ARGUS returns PASS. NEEDS-REVISIONS → DAEDALUS revises and re-surfaces.

---

## Phase 2 — Build (ADA single worktree, feature branch `arc-24/build`)

ADA receives DAEDALUS's design.md + ARGUS PASS verdict. Single worktree on substrate `main` at post-Arc-23 ship commit. Feature branch `arc-24/build`.

Files touched (expected; ADA confirms during build via A6 inventory):

| File | Source tickets |
|---|---|
| `substrate/operating-disciplines.md` | odh, nvl, ioy (new sections per A4) |
| `substrate/MAJOR_PLINY.md` | nvl (dispatch hygiene + poll-loop template), ioy (verify-then-execute scope-broadening) |
| `substrate/MAJOR_POLYBIUS.md` | nvl (analogous), ioy (confabulation cross-ref) |
| `substrate/CAPTAIN_VERA.md` | odh |
| `substrate/CAPTAIN_CATO.md` | odh |
| `substrate/CAPTAIN_ARGUS.md` | odh |
| `substrate/CAPTAIN_ZENO.md` | odh |
| `substrate/CAPTAIN_STRABO.md` | odh |
| `substrate/CAPTAIN_DAEDALUS.md` | odh |
| `substrate/CAPTAIN_*.md` (every other CAPTAIN found at inventory) | odh |
| `substrate/skills/agent-author/...` (if extant; per A7) | odh + nvl (scaffold updates) |

ADA writes probes/tests for the canonical poll-loop template as part of the worktree. Probes are inputs to Phase 3 VERA.

ADA commits incrementally. Hands the feature branch to Phase 3.

---

## Phase 3 — Verify (VERA + CATO + ZENO parallel)

**VERA probes:**
- Each CAPTAIN role file contains the expected heartbeat-and-read-before-write subsection (string match).
- MAJOR_PLINY.md contains the canonical poll-loop template (string match + structural).
- operating-disciplines.md contains the new sections per A4.
- Empirically execute the canonical poll-loop template against a real bw ticket; confirm new comments emit one stdout line each; confirm `last=` cursor advances correctly. Quadrant: easy-easy. **This probe IS a worked example of the framework Arc 23 just landed.**
- Verify CAPTAIN role files prohibit `Monitor` and `run_in_background: true`. (String match + interpretive — VERA flags if wording is ambiguous.)

VERA classifies each probe per Arc 23's quadrant framework (verification-complexity). Most easy-easy. The "every CAPTAIN consistently updated" check is hard-hard (UNVERIFIABLE bounded only by "I checked all N files at this snapshot"); VERA surfaces this honestly per the framework.

**CATO cold-reads** the entire diff. Wording drift across the 10+ CAPTAIN role files is the most likely defect class. CATO flags any seat whose heartbeat-discipline reads materially differently than the others.

**ZENO spec-vs-result** — this directive's deliverables list (Phase 2 file table + A6 inventory result) vs the actual files modified. No orphans either direction.

Three verifiers may raise NEEDS-REVISIONS; ADA addresses; verifiers re-verify. Cycle until clean PASS.

---

## Phase 4 — Smoke + Ship (PLINY)

Smoke beats:
1. `bash substrate/install.sh --dry-run --target project --project-dir <test-dir>` lists every modified substrate file in its deploy plan.
2. Same for `--target subproject` and `--target user`.
3. Markdown validation on operating-disciplines.md + all touched role files passes.
4. `grep -n "heartbeat" substrate/CAPTAIN_*.md` returns matches in every CAPTAIN role file.
5. `grep -n "uncertain, checking\|verify before" substrate/operating-disciplines.md` returns the new confabulation section.
6. `grep -n "Monitor\|run_in_background" substrate/CAPTAIN_*.md` returns the forbid clauses.
7. Canonical Monitor poll-loop template, copy-pasted into a real Monitor call, runs successfully against `stoa--<arc-24-epic-id>` and emits one stdout line for a test bw comment.

PLINY opens the PR titled `Arc 24 — comms-hygiene substrate DNA`. PR body summarizes the 3 tickets + design.md location + per-file changes + the new verdict shapes Arc 24's verifiers used (worked example of Arc 23's framework in action).

After PR approved (POLYBIUS or PRINCIPAL), PLINY runs `gh pr merge`. PLINY closes all 3 tickets with reasons citing the merge commit SHA.

PLINY writes a TIMING_LOG entry. Per nax (which landed in Arc 23), the TIMING_LOG does NOT enshrine N=1 conclusions as structural lessons.

---

## Out of scope (per directive)

- `stoa--jru` Arc 22 (coordination hygiene: bw-timeline parsing + cron expiry) — parked separately; not folded
- `stoa--vz9` EPIC (operating-disciplines promotion from project CLAUDE.md to substrate) — separate large EPIC
- `stoa--kjo` EPIC (per-agent git identity) — separate large EPIC
- Building Anthropic-side tooling for Agent introspection — not our substrate
- Auto-cleanup of orphaned Bash from CAPTAINs (issue #23154) — OS-level concern; substrate's answer is "forbid from CAPTAINs" not "auto-clean"
- Promoting save-verdict skill to substrate with Python helpers — Arc 23 Option A deferred this to a follow-up ticket Phase 4 close-out filed; not Arc 24's scope
- Implementing automated confabulation detection — out of substrate

---

## Deliverable summary

3 tickets closed (`stoa--odh`, `stoa--nvl`, `stoa--ioy`). ~20-30 substrate-prose edits across ~12 files. One feature branch merged to substrate main. One TIMING_LOG entry. Substrate canon now carries: heartbeat-and-read-before-write discipline universal to CAPTAINs; Monitor + bw-poll bridge as canonical orchestrator transport; "uncertain, checking" verb-level discipline universal to all seats.

Standby, run.
