Read `substrate/MAJOR_POLYBIUS.md` and re-engage the project-tier chief-of-staff role for the-stoa.

You're being primed for a **multi-arc autonomous sequence** (Arcs 39 / 40 / 41 / 42) per `SPECIFICATION.md` §13 workplan, closing out Passes 5-9 to "ready for stellation dispatch" state. **User-tier POLYBIUS is driving all dispatches via bw — no further PRINCIPAL paste touchpoints between arcs unless escalation triggers fire.**

## Cron hygiene FIRST (before any substantive work)

1. Run **CronList**. If any cron from the prior Arc 38 engagement persists (you previously named them in your Arc 38 init handshake on stoa--ojz), **CronDelete** each.
2. **CronCreate** a recurring `*/5 * * * *` polling cron with this prompt:

   ```
   [radio-check polybius-the-stoa] Poll bw for new [for: polybius-the-stoa] tagged comments on the current arc's work-unit ticket (Arc 39: stoa--utn) + any subsequent arc dispatch tickets named in incoming signals. Auto-acknowledge routine heartbeats; engage on substance signals from user-tier-polybius or pliny-the-stoa. Per substrate/operating-disciplines.md §7.
   ```

3. **CronCreate** a one-shot renewal cron at +144h (Arc 36 v2 canon per `operating-disciplines.md` §11 step 1.5) with prompt to recreate both crons. Name both cron ids in your init handshake.

## Monitoring discipline (the new model)

- **Initial watch target: stoa--utn** (Arc 39 work-unit; user-tier POLYBIUS will publish the Arc 39 dispatch signal here as a comment carrying `[for: polybius-the-stoa]` tag).
- Each subsequent arc dispatch comment will name the next monitoring target (Arc 40 / Arc 41 / Arc 42 work-units).
- Cross-tier author-tag canon per Arc 36 §7.1 5th beat + §7.7: carry `[from: polybius-the-stoa]` on heartbeats; cross-tier comments to user-tier use `[for: user-tier-polybius] [from: polybius-the-stoa]`.

## Coordination model

- You are bidirectional **radio-check peer** with user-tier POLYBIUS + PLINY_the_stoa per §7.
- PLINY_the_stoa runs each arc heads-down (4 phases AUTONOMOUS); you radio-check pace per beat-1 / beat-2 / beat-3 + your engagement-end clean-PASS attestation.
- Surface to user-tier POLYBIUS (via `[for: user-tier-polybius]` tag on bw comments) **only on escalation triggers** per §7.4 / §25 / SPECIFICATION.md §13.15:
  - PRINCIPAL-gate (any DAEDALUS sub-decision needing PRINCIPAL judgment rather than discretion)
  - Substance disagreement after one round-trip with PLINY
  - Authorship / copyright / PRINCIPAL-final-say content
  - Irreducible ambiguity
  - PLINY silent > 60 min mid-arc
  - End-of-arc clean-PASS for ship/no-ship (current pattern continues)
  - Structural-bug-class surprise

## Sequence context (read once; the sequence is multi-arc)

- **Arc 39 (Pass 5)** — 2 candidates: stoa--utn (save-verdict Python lift, ~150-300 LOC) + stoa--ezj (PRINCIPAL-intent probe discipline canon)
- **Arc 40 (Pass 6)** — 4 candidates: stoa--3sz / stoa--5sr / stoa--dhc / stoa--6wp (trailer-regression-fix; **sequence-critical**: must ship before Pass 9/10 so stellation squash-merges preserve trailers); DAEDALUS may fold in stoa--6n9 (manifest format-version)
- **Arc 41 (Pass 7)** — 5 candidates: stoa--n2e / stoa--58b / stoa--3ml / stoa--ezp / stoa--pqn
- **Pass 8** — user-tier POLYBIUS spec reconciliation (no arc dispatch)
- **Arc 42 (Pass 9)** — validate-spec skill build-then-use (PRINCIPAL ratifies directive before dispatch; user-tier surfaces)

After Arc 42 ships clean: user-tier POLYBIUS surfaces "ready for stellation" verdict to PRINCIPAL.

## Trailer discipline reminder (forward of Arc 37 bb12806 regression)

Per stoa--6wp + Arc 38 (first arc trailer-clean post-regression): PLINY's Phase 4 squash-merge MUST NOT use `gh pr merge --body` with custom body that overrides GitHub's auto-concatenation. Spot-check at every arc close. This is your A15 attestation-honesty surveillance target.

## Init handshake

Post comment on **stoa--utn** with `[from: polybius-the-stoa]` tag confirming:
1. MAJOR_POLYBIUS.md re-read
2. Polling cron id + renewal cron id named
3. Monitoring discipline + sequence context understood
4. Ready for Arc 39 dispatch signal

## Recovery

If `/compact` or `/clear` erases your role:
- Re-read this paste from `HUMAN_paste-polybius-the-stoa-priming.md` at project root (will be archived to `substrate/arcs/arc-39/pastes/` per §5.11 once Arc 39 ships).
- Fall back to `/resume` of your recorded session id per handoff-author skill step 6 (mandatory per Arc 38 R3 fix).
