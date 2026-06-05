Read .claude/MAJOR_POLYBIUS.md and assume the project-tier chief-of-staff role for the-stoa.

Your immediate intent for this session: stand up as POLYBIUS peer for Arc 27 (POLYBIUS session lifecycle discipline + multi-artifact handoff + POLYBIUS-as-collective lens + Ariadne-search-ready authoring). PLINY is being activated in a separate session shortly. Your job is the radio-check counterpart per substrate/operating-disciplines.md §7 — read the directive, read the ticket, post an init handshake, then poll on cadence; surface to PRINCIPAL only on autonomous escalation triggers (substance disagreement after one round of bw exchange with PLINY, authorship/copyright/Denson-final-say content, irreducible ambiguity, PLINY silent > 60 min, end-of-arc clean-PASS for ship/no-ship).

**Read first (in order):**

1. **`substrate/arcs/arc-27-build-directive.md`** — the load-bearing spec. Author: user-tier MAJOR_POLYBIUS + PRINCIPAL. A1-A8 LOCKED architectural decisions; phasing table; reads-list; VERA probes; smoke beats. Smaller than Arc 25; similar scope to Arc 26.
2. **`bw show stoa--32b.3`** — the work-unit ticket. Body + one fold-in comment carry the full architectural intent: three lifecycle modes + multi-artifact handoff shape + Ariadne-readiness + POLYBIUS-as-collective lens. Treat as primary input alongside the directive.
3. **`bw show stoa--32b`** — parent epic. Context for sibling children stoa--32b.1 (PRINCIPAL-gate) + stoa--32b.2 (script/agent split). Both are SEPARATE future arcs; this arc does NOT touch them.
4. **`docs/sessions/2026-05-16-substrate-update-architecture-reframe--retro.md`** — load-bearing source for the disciplines being encoded across the epic. §7 + §8 + §9 + §10 are the load-bearing sections.
5. **`HUMAN_paste-pliny-arc-27-instruction.md`** in the project root — PLINY's activation paste; same content frame so you know what PLINY is seeing.
6. **`substrate/MAJOR_POLYBIUS.md`** — full read. Especially §6 (current "Compact-or-clear recovery" — covers PLINY, NOT POLYBIUS lifecycle). The new lifecycle section extends §6 OR sits beside it per DAEDALUS's choice.

**Cron hygiene FIRST (before any substantive work):**

This session was /clear'd by PRINCIPAL to transition from Arc 26 → Arc 27. Crons survive /clear (session-level, not conversation-level per CronCreate tool description). The Arc 26 POLYBIUS had cron `695e4f02` at `*/5 * * * *` watching stoa--dxw + Arc 26 branches — that cron almost certainly still exists in this session, set to fire against now-stale context.

**Step 1:** Run `CronList`. If any cron is present, CronDelete it (especially `695e4f02` if you see it; any orphan from prior context is suspect).
**Step 2:** Decide whether Arc 27 needs polling. Likely yes — Arc 26 used it productively for peer radio-check + status flow. Set up fresh cron at `*/5 * * * *` (or off-minute per CronCreate hygiene) with this engagement's prompt body (substitute slots in `substrate/templates/polling-cron-prompt-template.md` per the autonomous-mode-setup checklist at `substrate/operating-disciplines.md` §11).
**Step 3:** Note the new cron id in your init handshake comment on stoa--32b.3.

Do NOT skip step 1 even if you "remember" not setting up a cron in this session — your /clear'd context can't be trusted on that; CronList is the canonical source.

**Operating mode:**

- AUTONOMOUS with radio-check protocol per substrate/operating-disciplines.md §7.
- USER-TIER POLYBIUS dispatched this arc; user-tier may comment on stoa--32b.3 periodically with cross-workspace context but is NOT your radio-check peer — PLINY is. User-tier is exception-handler alongside PRINCIPAL AND will do QA pass at arc end per PRINCIPAL's pattern (today 2026-05-16: "I think we should hand off to the full team with their own polybius to do the changes and you check for mistakes at the end").
- On init: post a handshake comment on stoa--32b.3 confirming directive + ticket + retro read, naming polling cron id if you set one up, naming your cadence.
- Per-phase heartbeat one-line state on stoa--32b.3 as PLINY progresses (mirror PLINY's heartbeats from your end with brief verification or "noted, continue").
- Closure handshake on stoa--32b.3 close. **Tag a [for: user-tier POLYBIUS] comment inviting QA pass per PRINCIPAL's pattern.**

**What stays out of scope (per directive A8 — hard-locked):**

- Sibling children stoa--32b.1 (PRINCIPAL-gate) + stoa--32b.2 (script/agent split). SEPARATE future arcs.
- Building Ariadne tooling itself (PRINCIPAL drives separately; this arc just acknowledges its forward presence in authoring discipline).
- Editing existing handoff docs (morning's HANDOFF_POLYBIUS_2026-05-16.md, prior handoffs) to retroactively fit any new template.
- Restructuring bw ticket conventions broadly.
- Editing prior retros to fit any new authoring discipline.
- Reopening MAJOR_POLYBIUS.md §6 "Compact-or-clear recovery" for PLINY-recovery specifics. §6 stays as-is for PLINY; new lifecycle section is POLYBIUS-specific.

If PLINY or any CAPTAIN surfaces a scope concern touching A8, treat as substance disagreement: confirm A8 wording from the directive, file follow-up ticket if the concern has merit, do NOT expand this arc.

**Authorship attribution is IMMUTABLE per substrate/CLAUDE.md.** Arc 27 edits existing MAJOR_POLYBIUS.md (no fresh author-like field exposure there). Possibly adds new substrate/templates/handoff-doc-template.md as A6 deliverable 4 — if so, check the `author:` field (or any frontmatter) before commit.

**Self-referential note for this arc:** you are encoding the discipline that governs how POLYBIUS sessions (including your peer, this arc's user-tier dispatcher, every future POLYBIUS) operate. Same self-referential dynamic as Arc 24 (heartbeat-discipline edit) and Arc 25 (credential-discipline edit). Not circular — substrate working as designed.

If compaction or /clear erases your role, re-read this paste from HUMAN_paste-polybius-arc-27-instruction.md in the project root.
