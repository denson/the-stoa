Read .claude/MAJOR_POLYBIUS.md and assume the project-tier chief-of-staff role for the-stoa.

Your immediate intent for this session: stand up as POLYBIUS peer for Arc 36 (explicit `[from: <self>]` author-tag canon for POLYBIUS-on-POLYBIUS bw coordination — scope-recut from arc-22; ships Part 1 / stoa--e39 only; Part 2 / stoa--cgn deferred). PLINY is being activated in a separate session shortly. Work-unit ticket: **stoa--e39** (P2, originally filed 2026-05-04).

Your job is the radio-check counterpart per substrate/operating-disciplines.md §7. Surface to PRINCIPAL only on autonomous escalation triggers (substance disagreement after one round of bw exchange with PLINY, authorship/copyright/PRINCIPAL-final-say content, irreducible ambiguity, PLINY silent > 60 min, end-of-arc clean-PASS for ship/no-ship, PRINCIPAL-gate clauses per §25 BLOCK semantics).

Cron hygiene FIRST (before any substantive work): this session may carry an orphaned cron from a prior /clear'd context. Run CronList; if any cron is present, CronDelete it. Then set up fresh cron at */5 * * * * (substrate-canonical default per operating-disciplines.md §7.2). Name the new cron id in your init handshake on stoa--e39.

**Self-application notice (LOAD-BEARING):** per directive A8, your OWN coordination heartbeats on stoa--e39 during this arc MUST apply the convention being shipped. Use `[from: polybius-the-stoa]` on own-bw substantive comments; use `[for: user-tier-polybius] [from: polybius-the-stoa]` on cross-tier-addressed comments to user-tier POLYBIUS. Continue using existing `[radio-check polybius-the-stoa]` for self-heartbeats. The first heartbeat you post is the first worked example of the convention being canon-locked.

**Read first (in order):**

1. **`substrate/arcs/arc-36-build-directive.md`** — load-bearing spec. A1-A14 LOCKED architectural decisions. A5/A6/A7 are DAEDALUS sub-decisions.
2. **`bw show stoa--e39`** — work-unit ticket. 2026-05-04 empirical anchor + original substrate-change enumeration.
3. **`bw show stoa--jru`** — parent EPIC being closed as scope-recut per A14.
4. **`bw show stoa--cgn`** — sibling being deferred with gating criteria per A11. NOT in Arc 36 scope.
5. **`git show arcs/22-coordination-hygiene:substrate/arcs/arc-22-build-directive.md`** Part 1 — architectural reference (A2/A2.5/A3/A4 inherited from arc-22 Part 1).
6. **`HUMAN_paste-pliny-arc-36-instruction.md`** in the project root — PLINY's activation paste; same content frame.
7. **`substrate/operating-disciplines.md` §7** entire section (§7.1-§7.6 — current universal-team POLYBIUS-pair canon; A5/A4 insertion surface).
8. **`substrate/MAJOR_POLYBIUS.md` §7** — A6 cross-ref target.
9. **`substrate/templates/polling-cron-prompt-template.md`** — 161 lines; A7 insertion surface for STEP 1.5.
10. **`substrate/operating-disciplines.md` §27** (Arc 33 mechanical/agent split — precedent for "prose canon now; mechanical enforcement if recurs").
11. **`substrate/operating-disciplines.md` §28** + **`substrate/arcs/arc-35-build-directive.md`** — Arc 35 most recent precedent (new top-level section + self-application).

**Operating mode:**

- AUTONOMOUS with radio-check protocol per substrate/operating-disciplines.md §7.
- USER-TIER POLYBIUS dispatched + will do QA pass at arc close per PRINCIPAL's pattern.
- On init: post handshake comment on stoa--e39 confirming directive + ticket + arc-22 Part 1 reference + §7/§27/§28/§5.10/§5.11/§5.12 + MAJOR_POLYBIUS.md §7 all read, naming polling cron id + cadence. **Apply self-application: this init handshake MUST carry `[from: polybius-the-stoa]` tag per the convention being shipped.**
- Per-phase heartbeat on stoa--e39 with `[from: polybius-the-stoa]` tag.
- Closure handshake on stoa--e39 close per §5.10 with `[radio-check polybius-the-stoa standing down]` (existing convention; not changed by Arc 36). PLINY tags `[for: user-tier-polybius]` invitation.

**What stays out of scope (per directive A11 — hard-locked):**

- Extending convention to non-POLYBIUS seats (PLINY, CAPTAINs, pair-programmer Majors) — A2.5 hard-lock.
- Cron-expiry handling (stoa--cgn) — deferred with gating criteria.
- Modifying the existing `[radio-check <slug>]` form.
- Retroactive tagging of past untagged comments — forward-only.
- Building a new cron-renewal mechanism / watcher cron / scheduled-renewal chain.
- Mechanical parser enforcement (pre-comment hook rejecting un-tagged POLYBIUS comments) — future arc if non-compliance recurs (per Arc 33 mechanical/agent-split precedent).
- Touching substrate/install.sh beyond what A7 STEP 1.5 may require.

If PLINY or any CAPTAIN surfaces a scope concern touching A11, treat as substance disagreement: confirm A11 wording from directive, file follow-up ticket if the concern has merit, do NOT expand this arc.

**Pre-branch hygiene per §5.9 + worktree convention per §5.9.4 (directive A13):** before PLINY creates arc-36/build, verify the two-check rule. Use separate worktree at `.claude/worktrees/arc-36-build/`. User-tier POLYBIUS confirmed at dispatch: local main = origin/main at `6414397`; no orphan arc-build branches.

**Signoff-accuracy per §5.10 + attestation-honesty per §19.6 (directive A14):** PLINY's signoff must live-verify cleanup claims per §5.10 (arc-36/build local + remote deleted; worktree removed; PR merged). Attestations cite live-verified state per §19.6.

**PRINCIPAL-gate awareness per §25:** if any DAEDALUS sub-decision (A5/A6/A7) surfaces as needing PRINCIPAL judgment rather than DAEDALUS discretion, treat as a PRINCIPAL-gate per §25 — halt + escalate immediately.

**Source-ticket closure per directive A14:** on Arc 36 ship:
- Close stoa--e39 (work-unit) with cross-ref to merge commit.
- Close stoa--jru (parent EPIC) with scope-recut audit note ("Part 1 shipped as Arc 36 via stoa--e39; Part 2 cron-expiry deferred via stoa--cgn per 2026-05-17 PRINCIPAL adjudication").
- Update stoa--cgn body via comment with deferral gating criteria — do NOT close.

**Co-Authored-By trailers per §28 (Arc 35 canon) — FIRST FORWARD-ARC INHERITING:** all ADA + DAEDALUS commits inside arc-36/build MUST carry `Co-Authored-By: CAPTAIN_<MNEMONIC>_the-stoa <captain-<mnemonic>@the-stoa.local>` trailer per Arc 35's §28. Arc 35 was the self-applying ship arc; Arc 36 is the first forward-arc that inherits §28 as established canon. Spot-check ADA's first commit for trailer; surface as substance disagreement if absent (per Arc 35 QA-pass observation #4 — ADA omitted trailers on Arc 34 pre-squash commits; Arc 36 is the first opportunity to see whether §28 is being applied cleanly forward).

**Authorship attribution is IMMUTABLE per substrate/CLAUDE.md** for file frontmatter. Arc 36 changes operating-disciplines.md + MAJOR_POLYBIUS.md + template prose only; no fresh author-like file fields exposure expected.

**Self-referential note:** Arc 36 ships the convention that addresses the empirical failure that surfaced in arc-21 (2026-05-04). The substrate has been informally using the `[radio-check ...]` + `[for: ...]` patterns across Arcs 32-35; Arc 36 completes the pair with `[from: ...]` + universal parsing canon. Your own heartbeats on stoa--e39 during this arc ARE the first worked example. Same substrate-shaping shape as Arcs 24-35.

If compaction or /clear erases your role, re-read this paste from HUMAN_paste-polybius-arc-36-instruction.md in the project root.
