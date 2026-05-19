Read `substrate/MAJOR_POLYBIUS.md` and assume the project-tier chief-of-staff role for the-stoa.

## Your immediate intent for this session

Stand up as POLYBIUS peer for **Arc 43 — substrate-canon-update bundle (stoa--yl1 + stoa--4zj)**. Single-arc engagement; sequence closes at Arc 43 ship. No further substrate-team arcs queued post-Arc-43 (PRINCIPAL transitioning to product-mode-ready posture for beadworks + ghost heavy-lift next).

PLINY_the_stoa is being spawned in parallel session.

## Cron hygiene FIRST (before substantive work)

1. Run **CronList**. Should be empty (Arc 42 close stood crons down 2026-05-18 10:12:36Z). If anything persists, **CronDelete** it.
2. **CronCreate** `*/5 * * * *` polling cron with prompt:
   ```
   [radio-check polybius-the-stoa] Poll bw for new [for: polybius-the-stoa] tagged comments on Arc 43 coordination ticket (user-tier-polybius will name the ticket in dispatch signal). Auto-acknowledge routine heartbeats; engage on substance. Per substrate/operating-disciplines.md §7 + §6.2a (Arc 42 canon).
   ```
3. **CronCreate** one-shot renewal cron at +144h per op-disc §11 step 1.5. Name both cron ids in your init handshake.

## Read first (in order)

1. **`substrate/arcs/arc-43-build-directive.md`** — load-bearing spec. A1-A22 LOCKED. A3 / A4 / A8 / A9 DAEDALUS sub-decisions.
2. **Both source ticket bodies**: `bw show stoa--yl1` (consolidated 10-candidate META-discipline catalog with full empirical anchor histories per Pass 8 + Pass 10 accretion comments) + `bw show stoa--4zj` (validate-spec parser refinement scope).
3. **`substrate/CAPTAIN_DAEDALUS.md` §6** — the canon extension target. §6.9 shipped Arc 42 is the parent for the new §6.9.3' / §6.9.3'' / etc. sub-sections.
4. **`substrate/CAPTAIN_ADA.md`** — A4 (ε) split-by-seat lean lands ADA Dev1 here.
5. **`substrate/skills/validate-spec/_lib/`** — C2 refinement target (spec_refs.py + bw_tickets.py per directive A7).
6. **`substrate/arcs/arc-42-build-directive.md`** + **Arc 42 ship `c827f73`** — Arc 42 §6.9 base canon precedent + validate-spec first-run baseline (144 check-1 FAILs + 36 check-2 STRANGE — Arc 43 expected to substantially reduce).
7. **`agents/observation/spec-validation/mechanical-check-results.md`** — Arc 42 baseline artifact; Arc 43 updates per A22 self-application.

## Operating mode

- **AUTONOMOUS** per priming + §7. PLINY runs Arc 43 heads-down (4 phases); you radio-check pace + Phase 4 spot-check.
- Surface to user-tier POLYBIUS (via `[for: user-tier-polybius]` tag) only on escalation triggers per §7.4 / §25 / §13.15.

## Phase 4 spot-check list at your seat (Arc 43-specific)

- A11 §28 trailers preserved on squash-merge body (now Arc 40 §5.10 canon enforced; should be uneventful)
- A17 source-ticket closures (yl1 + 4zj) with cross-refs + audit comments
- §5.11 paste archival (2 activation pastes to `substrate/arcs/arc-43/pastes/`; directive stays at `substrate/arcs/`)
- §5.10 signoff with live-verified state per §19.6
- **A22 SELF-APPLICATION verify** — validate-spec re-ran against SPECIFICATION.md in-arc + artifact captures FAIL-count delta vs Arc 42 baseline (144→? + 36→? expected substantial reduction; if reduction minimal, surface as substance signal for user-tier triage)
- **§6.X canon wording**: spot-check that COMPLETENESS CLAUSE captures the 6 empirical anchors faithfully + cost-multiplier math survives the edit

## A4 sub-decision surveillance

The A4 split-by-seat lean (WP13 → CAPTAIN_DAEDALUS.md; Dev1 → CAPTAIN_ADA.md; Dev2 → test-discipline canon) may surface no-clean-home for Dev2. If DAEDALUS proposes a new substrate/operating-disciplines.md section, verify the section number lands consistently (post §31 from Arc 38) + A18 IMMUTABLE not violated.

## What stays out of scope (per directive A19 hard-locks)

- No restructuring Arc 42 §6.9 base canon
- No widening yl1 candidates beyond the 7+ enumerated
- No expanding 4zj beyond check-1 + check-2 parser refinement
- No new substrate skills
- No beadworks/ghost project setup (post-Arc-43)
- No Pass 10 stellation Arc 6 polish (PRINCIPAL deferred indefinitely)

If PLINY or any CAPTAIN surfaces a scope concern touching A19, treat as substance disagreement per priming.

## Cross-tier author-tag canon (Arc 36 §7.1/§7.7)

- Your heartbeats: `[from: polybius-the-stoa]`
- Cross-tier to user-tier: `[for: user-tier-polybius] [from: polybius-the-stoa]`

## On dispatch close

Closure handshake on the Arc 43 coordination ticket per §5.10 — `[radio-check polybius-the-stoa Arc 43 closed; engagement complete]`. **This is the last substrate-team arc before product-mode-ready** — stand crons DOWN at close (CronList + CronDelete both; engagement is single-arc). PRINCIPAL may close your Claude Code window after standing-down comment lands.

## Recovery

If `/compact` or `/clear`: re-read this paste from `HUMAN_paste-polybius-arc-43-instruction.md` at project root (will archive to `substrate/arcs/arc-43/pastes/` per §5.11 at close). Fall back to `/resume` per handoff-author skill step 6 mandatory.
