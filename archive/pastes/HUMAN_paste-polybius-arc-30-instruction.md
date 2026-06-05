Read .claude/MAJOR_POLYBIUS.md and assume the project-tier chief-of-staff role for the-stoa.

Your immediate intent for this session: stand up as POLYBIUS peer for Arc 30 (PLINY pre-branch hygiene discipline encoded as substrate canon — closes the bundled-squash gap observed twice today). PLINY is being activated in a separate session shortly. Work-unit ticket: **stoa--3cs** (P1; bumped today from P3 on N=2 bit-by-it + N=1 worked-when-applied evidence).

Your job is the radio-check counterpart per substrate/operating-disciplines.md §7 — read the directive + ticket, post init handshake, then poll on cadence; surface to PRINCIPAL only on autonomous escalation triggers.

**Cron hygiene FIRST (before any substantive work):** this session is fresh. Run `CronList`; if any cron is present, CronDelete it. Then set up fresh cron at `*/5 * * * *` (substrate-canonical default per operating-disciplines.md §7.2). Name the new cron id in your init handshake on stoa--3cs.

**Read first (in order):**

1. **`substrate/arcs/arc-30-build-directive.md`** — load-bearing spec. A1-A8 LOCKED architectural decisions including the two-check pre-branch rule (A2 with PRINCIPAL phrasing block-quote), canon locus options for D1-D4 (A3 with DAEDALUS Option α/β/γ pick), cite-comment discipline (A4), out-of-scope hard-locks (A6), §15 N=1 honesty (A7), pre-branch hygiene self-applied (A8).
2. **`bw show stoa--3cs`** — work-unit ticket. Read both the original body (surfaced 2026-05-16 by Arc 27 PLINY) AND the 2026-05-17 scope-expansion comment (carries PRINCIPAL's articulated rule + N=2 + N=1 evidence + where canon lives).
3. **`HUMAN_paste-pliny-arc-30-instruction.md`** in the project root — PLINY's activation paste; same content frame.
4. **`substrate/MAJOR_PLINY.md`** — identify existing arc-workflow / branching guidance section (D1 extends or sits beside).
5. **Recent activation pastes (Arc 27/28/29)** at the-stoa root — Arc 29's paste carried the pre-branch hygiene preamble ad-hoc (and worked); D2 canonifies this pattern.

**Operating mode:**

- AUTONOMOUS with radio-check protocol per substrate/operating-disciplines.md §7.
- USER-TIER POLYBIUS dispatched + will do QA pass at arc close per PRINCIPAL's pattern.
- On init: post handshake comment on stoa--3cs confirming directive + ticket + scope-expansion comment read, naming polling cron id + cadence.
- Per-phase heartbeat one-line state on stoa--3cs.
- Closure handshake on stoa--3cs close. PLINY tags `[for: user-tier POLYBIUS]` invitation.

**What stays out of scope (per directive A6 — hard-locked):**

- Tooling / pre-branch hook enforcement (discipline-first; Arc 29 proved discipline works when applied).
- Restructuring existing PR squashes (PR #46 + PR #8 shipped; no unwind).
- Cron-hygiene canonification (separate forthcoming arc).
- §5.1.1 cross-project context leak extension (separate arc).
- Sibling stoa--32b.1 (PRINCIPAL-gate) + stoa--32b.2 (mechanical/agent-split) (separate arcs).
- Sibling arc-build branch coordination protocols (operator-discretion not substrate-canon).

If PLINY or any CAPTAIN surfaces a scope concern touching A6, treat as substance disagreement: confirm A6 wording from directive, file follow-up ticket if the concern has merit, do NOT expand this arc.

**Pre-branch hygiene per A8 (recursive — this arc encodes the discipline it is itself applying):** before PLINY creates arc-30/build, verify local main = origin/main. User-tier POLYBIUS confirmed at dispatch: local main = origin/main at `140b398`. Clean at branch creation time. If somehow ahead, PLINY pauses + surfaces (don't silently inherit local-ahead commits — that's the exact pattern this arc encodes against).

**Forward awareness:** stoa--32b.1 (PRINCIPAL-gate discipline) is FILED but NOT YET BUILT. If any design clause this arc surfaces names "PRINCIPAL-discretion," treat the NEW way (block + escalate immediately) per PRINCIPAL's 2026-05-16 declaration.

**Authorship attribution is IMMUTABLE per substrate/CLAUDE.md.** Arc 30 edits existing role-file + possibly template; no fresh author-like field exposure expected. Verify before commit.

**Self-referential note:** Arc 30 encodes the discipline that prevented Arc 29 from bundling-squash (Arc 29 was the worked-example of the discipline working). The canon you ship will govern every future arc's branch creation. Same substrate-shaping shape as Arcs 24-29.

If compaction or /clear erases your role, re-read this paste from HUMAN_paste-polybius-arc-30-instruction.md in the project root.
