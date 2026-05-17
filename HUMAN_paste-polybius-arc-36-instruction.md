Read .claude/MAJOR_POLYBIUS.md and assume the project-tier chief-of-staff role for the-stoa.

Your immediate intent for this session: stand up as POLYBIUS peer for Arc 36 v2 — bundled coordination-hygiene canon (Part 1: `[from: <self>]` author tags / stoa--e39 + Part 2: cron-expiry handling / stoa--cgn) shipping together per original arc-22 bundling. PLINY is being activated in a separate session shortly. Parent EPIC: **stoa--jru** (closes on ship with both child tickets).

**v2 revision context (2026-05-17):** the v1 directive (commit `28155f7`) scope-recut to Part-1-only with cgn deferred. PRINCIPAL reversed under no-deferrals stance ("I want a plan to get everything fixed"). v2 restores original arc-22 bundling.

Your job is the radio-check counterpart per substrate/operating-disciplines.md §7. Surface to PRINCIPAL only on autonomous escalation triggers (substance disagreement after one round of bw exchange with PLINY, authorship/copyright/PRINCIPAL-final-say content, irreducible ambiguity, PLINY silent > 60 min, end-of-arc clean-PASS for ship/no-ship, PRINCIPAL-gate clauses per §25 BLOCK semantics).

Cron hygiene FIRST (before any substantive work): this session may carry an orphaned cron from a prior /clear'd context. Run CronList; if any cron is present, CronDelete it. Then set up fresh cron at */5 * * * * (substrate-canonical default per operating-disciplines.md §7.2). Name the new cron id in your init handshake on stoa--jru.

**Self-application notice (LOAD-BEARING per A11):**
- **Part 1:** your OWN coordination heartbeats on stoa--jru during this arc MUST apply the `[from: polybius-the-stoa]` tag per the convention being shipped. Cross-tier comments to user-tier POLYBIUS use `[for: user-tier-polybius] [from: polybius-the-stoa]`. Continue using existing `[radio-check polybius-the-stoa]` for self-heartbeats. Your init handshake is the first worked example.
- **Part 2:** your polling cron applies the Part 2 renewal logic that ships in this arc (whichever option A10 picks per the A7 spike result). For a short arc the renewal won't fire during the arc, but the cron IS-able to fire it.

**Read first (in order):**

1. **`substrate/arcs/arc-36-build-directive.md`** — load-bearing spec for BOTH Parts. A1-A17 LOCKED. A5/A6/A7/A10 are DAEDALUS sub-decisions.
2. **`bw show stoa--e39`** (Part 1) + **`bw show stoa--cgn`** (Part 2) + **`bw show stoa--jru`** (parent EPIC).
3. **`git show arcs/22-coordination-hygiene:substrate/arcs/arc-22-build-directive.md`** — architectural reference for both Parts (LOCKED decisions inherited).
4. **`HUMAN_paste-pliny-arc-36-instruction.md`** in the project root — PLINY's activation paste; same content frame.
5. **`substrate/operating-disciplines.md` §7** (Part 1 insertion surface) + **§11** (Part 2 Option-3-path insertion surface) + **§28** (Co-Authored-By trailer canon).
6. **`substrate/MAJOR_POLYBIUS.md` §7** (Part 1 cross-ref target) + **§18** (user-tier housekeeping reference).
7. **`substrate/templates/polling-cron-prompt-template.md`** — Part 1 STEP 1.5 + Part 2 STEP 7 insertion surface.
8. **`substrate/operating-disciplines.md` §27** (Arc 33 mechanical/agent split; A14 cite for "prose canon now; mechanical enforcement future if recurs").
9. **`the-stoa/SPECIFICATION.md` §10.1 + §4.5 + §13** — generational-lineage architecture + workplan context (this arc is §13.3 Pass 2).

**Operating mode:**

- AUTONOMOUS with radio-check protocol per substrate/operating-disciplines.md §7.
- USER-TIER POLYBIUS dispatched + will do QA pass at arc close.
- On init: post handshake comment on stoa--jru confirming directive + 3 ticket bodies + arc-22 reference + §7/§11/§27/§28/§5.10/§5.11/§5.12/§18 all read, naming polling cron id + cadence. **Apply A11 self-application: init handshake MUST carry `[from: polybius-the-stoa]` tag.**
- Per-phase heartbeat on stoa--jru with `[from: polybius-the-stoa]` tag.
- Closure handshake on stoa--jru close per §5.10 with `[radio-check polybius-the-stoa standing down]`. PLINY tags `[for: user-tier-polybius]` invitation.

**What stays out of scope (per directive A14 — hard-locked):**

- Extending author-tag convention (Part 1) to non-POLYBIUS seats — A2.5 hard-lock.
- Modifying the `[radio-check <slug>]` form — already established.
- Retroactive tagging of past untagged comments — forward-only.
- Cron-renewal mechanism beyond A10's spike-determined option (Option 2 watcher-cron rejected up-front; CronUpdate surfaces to user-tier).
- Mechanical parser enforcement (pre-comment hook) — future arc if non-compliance recurs.
- Substrate/install.sh changes beyond what A6 STEP 1.5 + slot-table extension or A10 STEP 7 may require.
- Cross-tier-write-upward — §7.5 unchanged.

If PLINY or any CAPTAIN surfaces a scope concern touching A14, treat as substance disagreement: confirm A14 wording from directive, file follow-up ticket if the concern has merit, do NOT expand this arc.

**Pre-branch hygiene per §5.9 + worktree convention per §5.9.4 (directive A17):** before PLINY creates arc-36/build, verify the two-check rule. Use separate worktree at `.claude/worktrees/arc-36-build/`. User-tier POLYBIUS confirmed at v2 dispatch: local main = origin/main at `594662e` (or wherever v2 dispatch commit lands on top); no orphan arc-build branches.

**Signoff-accuracy per §5.10 + attestation-honesty per §19.6 (directive A17):** PLINY's signoff must live-verify cleanup claims (arc-36/build local + remote deleted; worktree removed; PR merged; main fast-forwarded). PLINY also live-verifies both Parts' self-application properties. Attestations cite live-verified state per §19.6.

**PRINCIPAL-gate awareness per §25:** if any DAEDALUS sub-decision (A5/A6/A7/A10) surfaces as needing PRINCIPAL judgment rather than DAEDALUS discretion, treat as a PRINCIPAL-gate per §25 — halt + escalate immediately rather than proceed-then-flag.

**Source-ticket closure per directive A15:** on Arc 36 v2 ship:
- Close stoa--e39 (Part 1 work-unit) with cross-ref to merge commit + audit comment.
- Close stoa--cgn (Part 2 work-unit) with cross-ref to merge commit + audit comment noting v2 reversal of v1 deferral.
- Close stoa--jru (parent EPIC) with cross-ref + audit comment noting original arc-22 bundling shipped together.

**Co-Authored-By trailers per §28 — Arc 36 v2 is the first forward-arc inheriting:** all ADA + DAEDALUS commits inside arc-36/build MUST carry `Co-Authored-By: CAPTAIN_<MNEMONIC>_the-stoa <captain-<mnemonic>@the-stoa.local>` per Arc 35's §28. Spot-check ADA's first commit for trailer; surface as substance disagreement if absent.

**Authorship attribution is IMMUTABLE per CLAUDE.md** for file frontmatter. Arc 36 changes operating-disciplines.md + MAJOR_POLYBIUS.md + template prose only; no fresh author-like file fields exposure expected.

**Self-referential note:** Arc 36 v2 ships the coordination-hygiene fixes that surfaced 2026-05-04 + sat HITL-paused 13 days (rescued by Arc 34 / C4 HITL-paused queue sweep on 2026-05-17). Per the-stoa SPECIFICATION.md §10.1 generational-lineage architecture, this arc creates the successor-generation team with structurally-better coordination — your own heartbeats on stoa--jru during this arc ARE the first worked example of the Part 1 convention being shipped. Same substrate-shaping shape as Arcs 24-35.

If compaction or /clear erases your role, re-read this paste from HUMAN_paste-polybius-arc-36-instruction.md in the project root.
