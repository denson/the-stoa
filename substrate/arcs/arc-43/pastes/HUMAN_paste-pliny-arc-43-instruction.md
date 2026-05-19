Read `substrate/MAJOR_PLINY.md` and assume the project-tier orchestrator role for the-stoa.

## Your immediate intent for this session

Build **Arc 43 — substrate-canon-update bundle (stoa--yl1 + stoa--4zj)** per `substrate/arcs/arc-43-build-directive.md`. Single-arc engagement; sequence closes at Arc 43 ship. POLYBIUS_the_stoa is your radio-check peer (parallel session).

PRINCIPAL transitions to product-mode-ready posture after Arc 43; this is the substrate-team's final sharpening pass before beadworks + ghost heavy-lift next.

## Cron hygiene FIRST (before substantive work)

1. Run **CronList**. Should be empty (Arc 42 close stood crons down 2026-05-18 10:12:36Z). If anything persists, **CronDelete** it.
2. Per **§6.2a (Arc 42 canon)** — now CANONICAL polling-cron-for-multi-arc-engagement pattern: **CronCreate** `*/5 * * * *` polling cron with prompt:
   ```
   [radio-check pliny-the-stoa] Poll bw for new [for: pliny-the-stoa] tagged comments on Arc 43 coordination ticket. When dispatch signal arrives, read named arc-43-build-directive.md + HUMAN_paste-pliny-arc-43-instruction.md, engage AUTONOMOUS per MAJOR_PLINY.md §5 + §6 + §6.2a + substrate/operating-disciplines.md §7.
   ```
3. **CronCreate** one-shot renewal cron at +144h per op-disc §11 step 1.5. Name both cron ids in your init handshake.

(Note: §6.2a is now substrate canon per Arc 42 ship — the polling-cron-PLINY pattern for multi-arc engagements is no longer canon-departure. Single-arc engagement still benefits from polling for cross-tier coordination ticket monitoring.)

## Read first (in order)

1. **`substrate/arcs/arc-43-build-directive.md`** — A1-A22 LOCKED. A3 / A4 / A8 / A9 DAEDALUS sub-decisions.
2. **Both source ticket bodies**: `bw show stoa--yl1` (consolidated 10-candidate META-discipline catalog) + `bw show stoa--4zj` (validate-spec parser refinement scope).
3. **`substrate/CAPTAIN_DAEDALUS.md` §6** — canon-extension target.
4. **`substrate/CAPTAIN_ADA.md`** — A4 (ε) lean lands Dev1 here.
5. **`substrate/skills/validate-spec/_lib/spec_refs.py`** + **`bw_tickets.py`** — C2 refinement targets.
6. **`substrate/arcs/arc-42-build-directive.md`** + **Arc 42 ship `c827f73`** — most recent precedent + validate-spec baseline.
7. **`agents/observation/spec-validation/mechanical-check-results.md`** — Arc 42 first-run artifact (144 check-1 FAILs + 36 check-2 STRANGE baseline).

## Operating mode

- **AUTONOMOUS** per priming + §7.
- §28 trailers + `[from: pliny-the-stoa]` heartbeats per Arc 36 §7.1/§7.7.
- CATO MANDATORY per A20.

## Per-arc workflow on dispatch signal

When polling cron picks up `[for: pliny-the-stoa]` dispatch signal on coordination ticket:

1. Read `substrate/arcs/arc-43-build-directive.md` + this paste.
2. Pre-branch hygiene per §5.9 + worktree at `.claude/worktrees/arc-43-build/` per §5.9.4.
3. Execute 4 phases heads-down:
   - **Phase 1**: DAEDALUS design (A3/A4/A8/A9 picks) → ARGUS cold-audit → rev cycles per DAEDALUS judgment
   - **Phase 2**: ADA build (CAPTAIN_DAEDALUS.md §6 extension + CAPTAIN_ADA.md/op-disc updates per A4 + validate-spec _lib/ refinement)
   - **Phase 3**: VERA + CATO + ZENO parallel. **CRITICAL A22 self-application**: ADA runs validate-spec against SPECIFICATION.md in-arc; artifact at `agents/observation/spec-validation/mechanical-check-results.md` updates with FAIL-count delta vs Arc 42 baseline.
   - **Phase 4**: §5.10 signoff with live-verified state; squash-merge per Arc 40 §5.10 canon (no `--body` override).
4. §5.11 paste archival: 2 activation pastes to `substrate/arcs/arc-43/pastes/` via git mv (directive stays at `substrate/arcs/`).
5. A17 source-ticket closure: stoa--yl1 + stoa--4zj close on ship with cross-refs + audit comments.
6. Comment on coordination ticket with `[for: user-tier-polybius] [from: pliny-the-stoa]` clean-PASS verdict.
7. **Single-arc engagement**: at close, CronList + CronDelete BOTH crons (polling + renewal). Stand down per §7.1 beat 4. Invoke handoff-author skill at agents/handoff/pliny-the-stoa-arc-43-close.md per §30 + handoff-author mandatory step 6 (record session id for /resume).

## Sequence reminders

- Phase 4 squash-merge: NO `gh pr merge --body` override per Arc 40 §5.10 canon (now downstream-consumer canon enforced across 5+ arcs in stellation Pass 10 + Arcs 38-42).
- §5.10 signoff: live-verified state per §19.6.
- A22 self-application: validate-spec MUST re-run; artifact captures empirical evidence of 4zj refinement working (or failing to work).

## Critical META-discipline self-application

Arc 43 SHIPS the META-disciplines stellation Pass 10 surfaced. Watch for the recursive self-application opportunity at DAEDALUS Phase 1: design must honestly apply §6.9.3'' COMPLETENESS CLAUSE + §6.2.1' canonical-code-block-fix during its own authoring. Recursive A20-style self-application is the strongest possible empirical anchor for the canon being shipped.

If DAEDALUS Phase 1 design produces probes that violate §6.9.3' / §6.9.3'' / §6.2.1' (the very canon being shipped), ARGUS catches them per stellation Pass 10 precedent (Arc 4 ARGUS rev1 caught 3 §6.9.3' failures in its OWN §3 probes; Arc 5 ARGUS rev1 caught SIBLING-DEFECT-CLASS gap in DAEDALUS-rev1 probes). Treat all such catches as positive empirical anchors for the canon — they EMPIRICALLY VALIDATE the discipline by catching it self-applied at design-authoring time.

## On dispatch close

Post `[for: user-tier-polybius] [from: pliny-the-stoa]` clean-PASS verdict on coordination ticket. Single-arc engagement: stand down completely (crons + handoff doc + standing-down comment). PRINCIPAL may close your Claude Code window after standing-down comment lands.

## Recovery

If `/compact` or `/clear`: re-read this paste from `HUMAN_paste-pliny-arc-43-instruction.md` at project root. Fall back to `/resume` per handoff-author skill step 6 mandatory.
