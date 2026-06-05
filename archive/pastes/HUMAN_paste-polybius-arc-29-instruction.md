Read .claude/MAJOR_POLYBIUS.md and assume the project-tier chief-of-staff role for the-stoa.

Your immediate intent for this session: stand up as POLYBIUS peer for Arc 29 (base-vs-custom agent convention encoded in substrate canon + tooling). PLINY is being activated in a separate session shortly. Work-unit ticket: **stoa--ads** (P1; 6 deliverables D1-D6 across MAJOR_POLYBIUS.md + operating-disciplines.md + install.sh + check.sh + apply.sh + workspace CLAUDE.md template handling).

Your job is the radio-check counterpart per substrate/operating-disciplines.md §7 — read the directive + ticket, post init handshake, then poll on cadence; surface to PRINCIPAL only on autonomous escalation triggers (substance disagreement after one round of bw exchange with PLINY, authorship/copyright/Denson-final-say content, irreducible ambiguity, PLINY silent > 60 min, end-of-arc clean-PASS for ship/no-ship).

**Cron hygiene FIRST (before any substantive work):** this session is fresh. If your terminal previously hosted a different session, it may carry an orphaned cron. Run `CronList`; if any cron is present, CronDelete it. Step 2: set up fresh cron at `*/5 * * * *` (substrate-canonical default per operating-disciplines.md §7.2). Step 3: name the new cron id in your init handshake on stoa--ads.

**Read first (in order):**

1. **`substrate/arcs/arc-29-build-directive.md`** — load-bearing spec. A1-A9 LOCKED architectural decisions including the architectural model (A2, with PRINCIPAL's exact phrasing block-quote), convention candidates (A3 with load-bearing Claude Code auto-discovery empirical question), files in scope (A4), cite-comment discipline (A5), out-of-scope hard-locks (A7), §15 N=1 honesty (A8), pre-branch hygiene (A9).
2. **`bw show stoa--ads`** — work-unit ticket. Body has 6 deliverables (D1-D6) + 6 acceptance probes + out-of-scope hard-locks + §15 N=1 caveat. Primary input prose alongside the directive.
3. **`HUMAN_paste-pliny-arc-29-instruction.md`** in the project root — PLINY's activation paste; same content frame.
4. **`substrate/MAJOR_POLYBIUS.md`** — current section structure; D1 adds new section about base-vs-custom architecture.
5. **`substrate/operating-disciplines.md`** — current section structure; D1 adds parallel universal-team section.
6. **`substrate/install.sh`** + **`substrate/skills/check-substrate-updates/{check,apply}.sh`** — the three tools D3/D4/D5 modify to scope to base paths.

**Operating mode:**

- AUTONOMOUS with radio-check protocol per substrate/operating-disciplines.md §7.
- USER-TIER POLYBIUS dispatched this arc + will do QA pass at arc close per PRINCIPAL's pattern.
- On init: post handshake comment on stoa--ads confirming directive + ticket read, naming polling cron id + cadence.
- Per-phase heartbeat one-line state on stoa--ads as PLINY progresses.
- Closure handshake on stoa--ads close. PLINY tags `[for: user-tier POLYBIUS]` invitation; user-tier does QA pass.

**What stays out of scope (per directive A7 — hard-locked):**

- Migrating any existing customized files to the new convention (none exist today).
- Building the railway custom agent team itself (separate forthcoming arc; dispatches AFTER this convention lands).
- Four-category drift classification at check.sh (Option Small from stoa--lyh; obsoleted by base-vs-custom; do NOT reopen).
- Custom POLYBIUS / PLINY at MAJOR tier (defer; convention applies to CAPTAINs + skills + templates only).
- Cross-workspace custom-agent sharing (defer).
- Auto-generated custom-agent templates / scaffolding (operator authors manually).
- Sibling stoa--32b.1 (PRINCIPAL-gate) + stoa--32b.2 (mechanical/agent-split) (separate arcs).
- stoa--3cs bundled-squash discipline encoding (separate arc).

If PLINY or any CAPTAIN surfaces a scope concern touching A7, treat as substance disagreement: confirm A7 wording from directive, file follow-up ticket if the concern has merit, do NOT expand this arc.

**Pre-branch hygiene per A9:** before PLINY creates arc-29/build, verify local main = origin/main. User-tier POLYBIUS confirmed at dispatch authoring: local main = origin/main at efffb8b. Should be clean at branch creation time. If somehow ahead, PLINY pauses + surfaces (don't silently inherit local-ahead commits — bundled-squash pattern).

**Forward awareness:** stoa--32b.1 (PRINCIPAL-gate discipline) is FILED but NOT YET BUILT. Until it ships, if any design clause this arc surfaces names "PRINCIPAL-discretion," treat the NEW way (block + escalate immediately, do NOT proceed-then-flag) per PRINCIPAL's 2026-05-16 declaration. For this arc specifically, the locked architectural decisions A1-A9 minimize the chance of new PRINCIPAL-discretion clauses — but if one surfaces during DAEDALUS design, escalate.

**Authorship attribution is IMMUTABLE per substrate/CLAUDE.md.** Arc 29 edits existing files (no new files with fresh author-like field exposure). If DAEDALUS surfaces a new skill or template as part of the design, frontmatter must carry `author: Denson Smith`. Verify before commit.

**Self-referential note:** Arc 29 encodes the architectural model PRINCIPAL declared today. The convention you ship will govern how every future custom-agent work at every workspace structures its files. Same substrate-shaping shape as Arcs 24/25/26/27/28 — substrate working as designed.

If compaction or /clear erases your role, re-read this paste from HUMAN_paste-polybius-arc-29-instruction.md in the project root.
