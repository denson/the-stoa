Read .claude/MAJOR_POLYBIUS.md and assume the project-tier chief-of-staff role for the-stoa.

Your immediate intent for this session: stand up as POLYBIUS peer for Arc 33 (mechanical-script / agent-inspection split — structural enforcement layer for Arc 31's §25 prose discipline). PLINY is being activated in a separate session shortly. Work-unit ticket: **stoa--32b.2** (P2; child of stoa--32b epic; sibling to stoa--32b.1 already shipped as Arc 31).

Your job is the radio-check counterpart per substrate/operating-disciplines.md §7. Surface to PRINCIPAL only on autonomous escalation triggers (substance disagreement after one round of bw exchange with PLINY, authorship/copyright/PRINCIPAL-final-say content, irreducible ambiguity, PLINY silent > 60 min, end-of-arc clean-PASS for ship/no-ship, PRINCIPAL-gate clauses per §25 BLOCK semantics).

Cron hygiene FIRST (before any substantive work): this session may carry an orphaned cron from a prior /clear'd context. Run CronList; if any cron is present, CronDelete it. Then set up fresh cron at */5 * * * * (substrate-canonical default per operating-disciplines.md §7.2). Name the new cron id in your init handshake on stoa--32b.2.

**Read first (in order):**

1. **`substrate/arcs/arc-33-build-directive.md`** — load-bearing spec. A1-A10 LOCKED architectural decisions.
2. **`bw show stoa--32b.2`** — work-unit ticket body + the 2026-05-17 scope-refresh comment (load-bearing — carries intervening-arc context from Arcs 28-32 + DAEDALUS guidance + updated §15 N=1 framing). BOTH required reading.
3. **`docs/sessions/2026-05-16-substrate-update-architecture-reframe--retro.md` §8** — LOAD-BEARING source for the 3-step pattern.
4. **`substrate/operating-disciplines.md` §25** (Arc 31 PRINCIPAL-gate; the prose discipline this arc enforces mechanically) + **§19.6** (Arc 32 attestation-confabulation; inspection-shape candidate) + **§17 / §23** (Arc 29 base-vs-custom; inspection must respect).
5. **`substrate/MAJOR_PLINY.md` §5.10** (Arc 32 signoff-accuracy; inspection-shape candidate) + **§5.9 / §5.9.4** (Arc 30 + Arc 32; arc-build branching + worktree convention; self-applied by this arc).
6. **`substrate/skills/check-bw-release/`** (Arc 28; small inspection-shape skill working precedent) + **`substrate/skills/check-substrate-updates/`** (Arcs 26 + 29; larger inspection-shape; the negative empirical anchor for script-bloat).
7. **`HUMAN_paste-pliny-arc-33-instruction.md`** in the project root — PLINY's activation paste; same content frame.

**Operating mode:**

- AUTONOMOUS with radio-check protocol per substrate/operating-disciplines.md §7.
- USER-TIER POLYBIUS dispatched + will do QA pass at arc close per PRINCIPAL's pattern.
- On init: post handshake comment on stoa--32b.2 confirming directive + ticket + refresh-comment + §25/§19.6/§5.10/§17 + retro §8 all read, naming polling cron id + cadence.
- Per-phase heartbeat on stoa--32b.2.
- Closure handshake on stoa--32b.2 close per §5.10. PLINY tags `[for: user-tier POLYBIUS]` invitation.

**What stays out of scope (per directive A7 — hard-locked):**

- Unwinding Arc 26's check.sh additions (alongside-not-regression).
- Refactoring check-bw-release skill (positive precedent; treat as reference, not target).
- Building inspection-agents for every existing script (worked example + pattern doc; incremental adoption).
- Mechanical enforcement of §25/§19.6/§5.10/§17 as REQUIRED by this arc (component + worked example; specific enforcement is future arc).
- CAPTAIN_INSPECTOR new seat (Option γ explicitly deferred).
- Multi-skill rollout (one worked example; future arcs adopt elsewhere).
- Sibling stoa--32b.1 revision (Arc 31 shipped).
- Other hygiene tickets (stoa--k36 / stoa--f37 / stoa--ize / stoa--3qi) — separate.

If PLINY or any CAPTAIN surfaces a scope concern touching A7, treat as substance disagreement: confirm A7 wording from directive, file follow-up ticket if the concern has merit, do NOT expand this arc.

**Pre-branch hygiene per Arc 30 §5.9 + worktree convention per Arc 32 §5.9.4 (directive A9):** before PLINY creates arc-33/build, verify the two-check rule. Use separate worktree at `.claude/worktrees/arc-33-build/` per §5.9.4. User-tier POLYBIUS confirmed at dispatch authoring: local main = origin/main at `84f1f86`; no orphan arc-build branches.

**Signoff-accuracy per Arc 32 §5.10 + attestation-honesty per §19.6 (directive A10):** PLINY's signoff must live-verify cleanup claims per §5.10. PLINY's attestations (init handshake, per-phase heartbeats, closure) must cite live-verified state per §19.6 — not echo the dispatch-authoring SHA `84f1f86` as the verified-at-attestation state.

**PRINCIPAL-gate awareness per Arc 31 §25:** if any DAEDALUS sub-decision in A2 (substrate-component-shape pick) or A3 (skill naming) or A4 (operating-disciplines.md insertion locus) surfaces as needing PRINCIPAL judgment rather than DAEDALUS discretion, treat as a PRINCIPAL-gate per §25 (BLOCK not TAG) — halt + escalate immediately rather than proceed-then-flag.

**Authorship attribution is IMMUTABLE per substrate/CLAUDE.md.** Arc 33 ADDS NEW skill files (per A6). SKILL.md frontmatter MUST carry `author: Denson Smith` per Arc 27 stoa--uly convention. Verify all new files before commit.

**Self-referential note:** Arc 33 IS the structural enforcement layer for Arc 31's §25 prose discipline (and Arc 32's §19.6 + §5.10). The inspection-agent component you ship will be how future arcs MECHANICALLY verify what current arcs RELY ON AGENT RECOGNITION for. Strongest substrate-shaping arc remaining at the-stoa.

If compaction or /clear erases your role, re-read this paste from HUMAN_paste-polybius-arc-33-instruction.md in the project root.
