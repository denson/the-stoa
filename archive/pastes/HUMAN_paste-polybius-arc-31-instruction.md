Read .claude/MAJOR_POLYBIUS.md and assume the project-tier chief-of-staff role for the-stoa.

Your immediate intent for this session: stand up as POLYBIUS peer for Arc 31 (PRINCIPAL-gate discipline encoded as substrate canon — closes the AFK-bypass gap from Arc 26 / sector-4 Probe 8). PLINY is being activated in a separate session shortly. Work-unit ticket: **stoa--32b.1** (P2 by ticket; effectively P1 for this dispatch per PRINCIPAL sequencing 2026-05-17).

Your job is the radio-check counterpart per substrate/operating-disciplines.md §7 — read the directive + ticket + retro source, post init handshake, then poll on cadence; surface to PRINCIPAL only on autonomous escalation triggers.

**Cron hygiene FIRST (before any substantive work):** this session is fresh. Run `CronList`; if any cron is present, CronDelete it. Then set up fresh cron at `*/5 * * * *` (substrate-canonical default per operating-disciplines.md §7.2). Name the new cron id in your init handshake on stoa--32b.1.

**Read first (in order):**

1. **`substrate/arcs/arc-31-build-directive.md`** — load-bearing spec. A1-A11 LOCKED architectural decisions including the discipline (A2 with PRINCIPAL phrasing block-quote), D1 locus pick (A3, DAEDALUS picks Option α/β), CAPTAIN envelope shape (A4), template updates (A5), probe-design sub-case fold-vs-split (A6), cite-comments (A7), out-of-scope hard-locks (A9), §15 N=1 honesty (A10), pre-branch hygiene (A11).
2. **`bw show stoa--32b.1`** — work-unit ticket. Body has PRINCIPAL phrasing + 5 deliverables + acceptance probes + out-of-scope + §15 caveat. Primary input alongside directive.
3. **`docs/sessions/2026-05-16-substrate-update-architecture-reframe--retro.md` §7** — LOAD-BEARING SOURCE for the discipline. Read in full. Frames the conflation problem (autonomous-mode escalation vs PRINCIPAL-gate-block) more thoroughly than the ticket body.
4. **`bw show stoa--dxw`** + **`bw show stoa--501`** (the-stoa bw store) — Arc 26 empirical anchor + sector-4 cleanup that demonstrated the gap. Both CLOSED; context only.
5. **`HUMAN_paste-pliny-arc-31-instruction.md`** in the project root — PLINY's activation paste; same content frame.
6. **`substrate/operating-disciplines.md`** + **`substrate/CAPTAIN_DAEDALUS.md`** + **`substrate/CAPTAIN_ADA.md`** + **`substrate/CAPTAIN_VERA.md`** + **`substrate/templates/autonomous-mode-activation-template.md`** + **`substrate/templates/polling-cron-prompt-template.md`** — the six files D1-D5 modify.

**Operating mode:**

- AUTONOMOUS with radio-check protocol per substrate/operating-disciplines.md §7.
- USER-TIER POLYBIUS dispatched + will do QA pass at arc close per PRINCIPAL's pattern.
- On init: post handshake comment on stoa--32b.1 confirming directive + ticket + retro §7 read, naming polling cron id + cadence.
- Per-phase heartbeat one-line state on stoa--32b.1.
- Closure handshake on stoa--32b.1 close. PLINY tags `[for: user-tier POLYBIUS]` invitation.

**What stays out of scope (per directive A9 — hard-locked):**

- Reopening existing escalation-triggers list at operating-disciplines.md (additive only).
- Editing Arc 26's VERA Probe 8 retroactively.
- Building inspection-agent pattern (stoa--32b.2 separate forthcoming arc).
- Cron-hygiene canonification (separate arc).
- §5.1.1 cross-project context leak extension (separate arc).
- Other CAPTAIN envelopes (CATO, ZENO, BARTLEBY, STRABO, HERALD, CURATOR) — D2 names DAEDALUS + ADA + VERA only.
- MAJOR role file additions (MAJOR_POLYBIUS, MAJOR_PLINY) — discipline propagates via operating-disciplines.md.

If PLINY or any CAPTAIN surfaces a scope concern touching A9, treat as substance disagreement: confirm A9 wording from directive, file follow-up ticket if the concern has merit, do NOT expand this arc.

**Pre-branch hygiene per directive A11 + MAJOR_PLINY.md §5.9 (just-shipped Arc 30 canon):** before PLINY creates arc-31/build, verify the two-check rule. User-tier POLYBIUS confirmed at dispatch: local main = origin/main at `efb0394`; no other arc-build branches in flight (orphans cleaned up). Should be clean at branch creation time.

**Self-referential note:** Arc 31 IS the arc that encodes the discipline whose absence allowed Arc 26's Probe 8 mutation. Until this arc ships, the workaround (activation pastes reminding PLINY to "treat PRINCIPAL-discretion the NEW way") has been carrying the gap. Once shipped, future pastes can drop that workaround. Same substrate-shaping shape as Arcs 24-30.

**Authorship attribution is IMMUTABLE per substrate/CLAUDE.md.** Arc 31 edits existing files (no fresh author-like field exposure expected). Verify before commit.

If compaction or /clear erases your role, re-read this paste from HUMAN_paste-polybius-arc-31-instruction.md in the project root.
