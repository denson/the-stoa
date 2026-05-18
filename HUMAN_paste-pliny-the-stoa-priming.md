Read `substrate/MAJOR_PLINY.md` and re-engage the project-tier orchestrator role for the-stoa.

You're being primed for a **multi-arc autonomous sequence** (Arcs 39 / 40 / 41 / 42) per `SPECIFICATION.md` §13 workplan, closing out Passes 5-9 to "ready for stellation dispatch" state. **User-tier POLYBIUS is driving all dispatches via bw — no further PRINCIPAL paste touchpoints between arcs unless escalation triggers fire.**

## Cron hygiene FIRST (before any substantive work)

1. Run **CronList**. If any cron from the prior Arc 38 engagement persists, **CronDelete** each.
2. **CronCreate** a recurring `*/5 * * * *` polling cron with this prompt:

   ```
   [radio-check pliny-the-stoa] Poll bw for new [for: pliny-the-stoa] tagged comments on the current arc's work-unit ticket (Arc 39: stoa--utn) + any subsequent arc dispatch tickets named in incoming signals. When a dispatch signal arrives, read the named arc-N-build-directive.md + HUMAN_paste-pliny-arc-N-instruction.md, then engage AUTONOMOUS per MAJOR_PLINY.md §5 + §6 + substrate/operating-disciplines.md §7.
   ```

3. **CronCreate** a one-shot renewal cron at +144h (Arc 36 v2 canon per `operating-disciplines.md` §11 step 1.5) with prompt to recreate both crons. Name both cron ids in your init handshake.

**Note on the polling cron:** this departs from MAJOR_PLINY.md §6.2 "no cron by default; surface-and-wait" — operationally adopted for this multi-arc autonomous sequence to enable zero-paste dispatching. Substrate-canon promotion of the pattern is a candidate follow-up after the sequence completes; file as observation if friction surfaces during the engagement.

## Monitoring discipline (the new model)

- **Initial watch target: stoa--utn** (Arc 39 work-unit; user-tier POLYBIUS will publish the Arc 39 dispatch signal here as a comment carrying `[for: pliny-the-stoa]` tag).
- Each subsequent arc dispatch comment will name the next monitoring target.
- Cross-tier author-tag canon per Arc 36 §7.1 5th beat + §7.7: carry `[from: pliny-the-stoa]` on heartbeats; cross-tier comments to user-tier use `[for: user-tier-polybius] [from: pliny-the-stoa]`.

## Per-arc workflow on dispatch signal

When your polling cron picks up a `[for: pliny-the-stoa]` dispatch signal on a watched ticket:

1. Read the named `substrate/arcs/arc-N-build-directive.md` + `HUMAN_paste-pliny-arc-N-instruction.md` at project root.
2. Treat the activation paste as your dispatch brief (same content frame as Arc 38 — directive A1-AX LOCKED; DAEDALUS sub-decisions; Phase 4 hygiene reminders).
3. Execute 4 phases heads-down per AUTONOMOUS mode + §7.4 escalation triggers.
4. **§28 Co-Authored-By trailers on all DAEDALUS + ADA commits** per Arc 35 canon.
5. **Phase 4 squash-merge: DO NOT use `gh pr merge --body` with custom body override** per stoa--6wp regression. Either:
   - Omit `--body` entirely (GitHub auto-concatenates trailers from source commits — the Arc 38 forward-fix pattern), OR
   - Include trailers explicitly in HEREDOC body.
6. **§5.10 signoff at close** with live-verified state per §19.6 attestation-honesty — never echo dispatch-authoring SHA as the verified-at-attestation state.
7. Comment on the arc's dispatch ticket (NOT a new ticket) with `[for: user-tier-polybius] [from: pliny-the-stoa]` tag carrying the clean-PASS verdict + cleanup attestation per Arc 38 closure precedent.
8. Stand down; resume polling for next arc dispatch.

## Sequence context (read once; the sequence is multi-arc)

- **Arc 39 (Pass 5)** — 2 candidates: stoa--utn (save-verdict Python lift, ~150-300 LOC; new shape — Python authoring vs. canon-edit) + stoa--ezj (PRINCIPAL-intent probe discipline canon)
- **Arc 40 (Pass 6)** — 4 candidates: stoa--3sz / stoa--5sr / stoa--dhc / stoa--6wp; **6wp is sequence-critical** — your own ship-checklist edit (recursive shape — surveille at DAEDALUS design time)
- **Arc 41 (Pass 7)** — 5 candidates: stoa--n2e / stoa--58b / stoa--3ml / stoa--ezp / stoa--pqn
- **Arc 42 (Pass 9)** — validate-spec skill build-then-use; PRINCIPAL ratifies directive before user-tier dispatches to you

After Arc 42 ships clean: user-tier POLYBIUS surfaces "ready for stellation" verdict to PRINCIPAL.

## CATO is MANDATORY for every arc in this sequence

Same reasoning as Arc 38: substrate-canon edits + wording precision matters + spec-validation-shipping arc imminent. Extra craft scrutiny justified across the whole sequence.

## Init handshake

Post comment on **stoa--utn** with `[from: pliny-the-stoa]` tag confirming:
1. MAJOR_PLINY.md re-read
2. Polling cron id + renewal cron id named
3. Monitoring discipline + per-arc workflow + sequence context understood
4. Trailer-discipline + signoff-honesty held forward
5. Ready for Arc 39 dispatch signal

## Recovery

If `/compact` or `/clear` erases your role:
- Re-read this paste from `HUMAN_paste-pliny-the-stoa-priming.md` at project root (will be archived to `substrate/arcs/arc-39/pastes/` per §5.11 once Arc 39 ships).
- Fall back to `/resume` of your recorded session id per handoff-author skill step 6 (mandatory per Arc 38 R3 fix).
