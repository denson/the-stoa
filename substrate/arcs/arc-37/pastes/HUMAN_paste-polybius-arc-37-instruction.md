Read .claude/MAJOR_POLYBIUS.md and assume the project-tier chief-of-staff role for the-stoa.

Your immediate intent for this session: stand up as POLYBIUS peer for Arc 37 — **6-candidate substrate architecture canonification batch.** PLINY is being activated in a separate session shortly. Candidates: C1 stoa--86k (two-team forge/shop) + C2 stoa--kt6 (multi-team interop) + C3 stoa--wad (four-layer identity) + C4 stoa--ntn (operating-mode progression) + C5 stoa--53u (idle retrospective-narrative confabulation) + C6 stoa--7e3 (handoff-author skill).

Your job is the radio-check counterpart per substrate/operating-disciplines.md §7. Surface to PRINCIPAL only on autonomous escalation triggers (substance disagreement after one round of bw exchange with PLINY, authorship/copyright/PRINCIPAL-final-say content, irreducible ambiguity, PLINY silent > 60 min, end-of-arc clean-PASS for ship/no-ship, PRINCIPAL-gate clauses per §25 BLOCK semantics).

Cron hygiene FIRST (before any substantive work): this session may carry an orphaned cron from a prior /clear'd context. Run CronList; if any cron is present, CronDelete it. Then set up fresh cron at */5 * * * * (substrate-canonical default per operating-disciplines.md §7.2). Name the new cron id in your init handshake.

**Per Arc 36's §7.1 5th beat + §7.7 (now shipped canon):** your coordination heartbeats MUST carry `[from: polybius-the-stoa]` tag per the convention. Cross-tier comments to user-tier POLYBIUS use `[for: user-tier-polybius] [from: polybius-the-stoa]`. Continue using existing `[radio-check polybius-the-stoa]` for self-heartbeats per §7.1 beat 1. Your init handshake is the first worked example under this canon for Arc 37.

**Per Arc 36's §11 step 1.5 (now shipped canon):** schedule a one-shot renewal cron at +144h from your polling-cron creation per the Part 2 renewal mechanism. For a single-day arc, the renewal won't fire — but the cron IS-able to fire it, and your setup completion is the FIRST forward-arc applying the renewal canon shipped in Arc 36 v2.

**Read first (in order):**

1. **`substrate/arcs/arc-37-build-directive.md`** — load-bearing spec for all 6 candidates. A1-A20 LOCKED. A8-A13 are DAEDALUS sub-decisions.
2. **All 6 source ticket bodies:** stoa--86k + stoa--kt6 + stoa--wad + stoa--ntn + stoa--53u + stoa--7e3 (+ `_drafts/skill_handoff_author.md` as C6 draft input).
3. **`HUMAN_paste-pliny-arc-37-instruction.md`** in the project root — PLINY's activation paste; same content frame.
4. **`substrate/MAJOR_POLYBIUS.md`** — C1 + C3 + C4 + C6 touch-points.
5. **`substrate/MAJOR_PLINY.md`** — C4 + C5 + C6 touch-points.
6. **`substrate/operating-disciplines.md`** — primary canon surface (§7.4 + §7.5 + §10 + §11 + §17 + §19.6 + §23 + §28).
7. **`substrate/install.sh`** — C6 SKILL_NAMES addition surface.
8. **`substrate/skills/check-bw-release/`** + **`substrate/skills/inspect-script-output/`** — precedents for substrate skill shape.
9. **`the-stoa/SPECIFICATION.md` §10.1 + §4.5 + §13** — generational-lineage architecture + workplan context (Arc 37 is §13.4 Pass 3 of the 8-pass workplan).

**Operating mode:**

- AUTONOMOUS with radio-check protocol per substrate/operating-disciplines.md §7.
- USER-TIER POLYBIUS dispatched + will do QA pass at arc close.
- On init: post handshake comment on one of the 6 source tickets (recommend stoa--7e3 since it's the most architecturally novel + ships the lineage hook). Confirm directive + 6 ticket bodies + substrate surfaces read. Name polling cron id + cadence + renewal cron id per Arc 36 §11 step 1.5. **Init handshake MUST carry `[from: polybius-the-stoa]` tag.**
- Per-phase heartbeat with `[from: polybius-the-stoa]` tag.
- Closure handshake at arc close per §5.10 with `[radio-check polybius-the-stoa standing down]`. PLINY tags `[for: user-tier-polybius]` invitation on at least one closed ticket.

**What stays out of scope (per directive A17 — hard-locked):**

- Bundling bj5 (Arc 38) or utn/3sz/5sr/pqn (Arc 39 candidates) — separate arcs per the workplan.
- Mechanical enforcement infrastructure (no pre-commit hooks, validators) — §27 mechanical/agent-split pattern; future arc if recurs.
- Extending canon to non-POLYBIUS / non-CAPTAIN seats beyond what each candidate covers.
- Touching substrate-deploy mechanism (install.sh) beyond C6 SKILL_NAMES addition.
- Building meta-agent for cross-generation lineage analysis (post-spec future work).
- Building memory-introspect skill (C3 out-of-scope).
- Building multi-team registry (C2 out-of-scope; convention-based discovery sufficient).

If PLINY or any CAPTAIN surfaces a scope concern touching A17, treat as substance disagreement: confirm A17 wording from directive, file follow-up ticket if the concern has merit, do NOT expand this arc.

**Pre-branch hygiene per §5.9 + worktree convention per §5.9.4 (directive A20):** before PLINY creates arc-37/build, verify the two-check rule. Use separate worktree at `.claude/worktrees/arc-37-build/`. User-tier POLYBIUS confirmed at dispatch: local main = origin/main at `679b6bf` (or wherever dispatch commit lands on top); no orphan arc-build branches.

**Signoff-accuracy per §5.10 + attestation-honesty per §19.6 (directive A20):** PLINY's signoff must live-verify cleanup claims (arc-37/build local + remote deleted; worktree removed; PR merged; main fast-forwarded; pastes archived per §5.11; SKILL_NAMES includes handoff-author; C6 SKILL.md author: Denson Smith). Attestations cite live-verified state per §19.6.

**PRINCIPAL-gate awareness per §25:** if any DAEDALUS sub-decision (A8-A13) surfaces as needing PRINCIPAL judgment rather than DAEDALUS discretion, treat as a PRINCIPAL-gate per §25 — halt + escalate immediately.

**Source-ticket closure per directive A18:** on Arc 37 ship, close all 6 source tickets with cross-refs to merge commit + audit comments per candidate. Tag `[for: user-tier-polybius]` on at least one (recommend stoa--7e3).

**Co-Authored-By trailers per §28 — second forward-arc inheriting:** all ADA + DAEDALUS commits inside arc-37/build MUST carry trailers. Spot-check ADA's first commit; surface as substance disagreement if absent. C6 SKILL.md frontmatter MUST carry `author: Denson Smith`.

**Authorship attribution is IMMUTABLE per CLAUDE.md** for file frontmatter. Arc 37 changes operating-disciplines.md + MAJOR_POLYBIUS.md + MAJOR_PLINY.md prose + ADDS new SKILL.md file (per C6 — verify author: Denson Smith) + adds install.sh SKILL_NAMES entry.

**Self-application per A14:**
- C5 negative: do NOT confabulate retrospective narratives during this arc. Closed tickets are past-work evidence, not own-current-session accomplishment.
- C6 positive: if any seat hits `/compact` or session-close, invoke the newly-shipped handoff-author skill. Low probability for short arc; canon authorizes it.

**Self-referential note:** Arc 37 is the substrate's largest canon batch (6 candidates spanning architecture canon + new skill). Per the-stoa SPECIFICATION.md §10.1 generational-lineage architecture, this arc creates a successor-generation team with substantially more articulated canon. After Arc 37 + Arc 38 + Arc 39 ship: zero open substrate-canon tickets at the-stoa; substrate ready for §13.9 Pass 8 behavioral validation via stellation dispatch.

If compaction or /clear erases your role, re-read this paste from HUMAN_paste-polybius-arc-37-instruction.md in the project root.
