# Sectioned retrospective — Substrate-update architecture reframe (2026-05-16 session)

**Companion to:** `HANDOFF_POLYBIUS_2026-05-16.md` at repo root (the inbound engagement handoff that opened this session — read that for the morning's pre-engagement state).
**Purpose of this document:** semantic-chunked record of the 2026-05-16 user-tier POLYBIUS session, structured for vector-DB / hypergraph ingestion later. Each `## §N` section is a self-contained retrieval unit. The load-bearing sections are §7 / §8 / §9 — two PRINCIPAL observations and their synthesis. The earlier sections (§1-§6) are the empirical trail that produced the observations.

**Section schema** (carried from prior retros):
- **Phase:** name + temporal anchor (commit hash where applicable)
- **Goal at start:** what state the phase began in
- **Key exchanges:** paraphrased; quoted only for load-bearing PRINCIPAL phrasing
- **Decisions:** bulleted, each with rationale
- **Artifacts produced:** files / commits / URLs
- **Failure modes caught:** the empirical-beat trail
- **Discipline reinforced / surfaced:** `u--7yg` references where applicable; new disciplines flagged where they emerged

---

## §1 — Engagement open

**Phase:** Session pickup from 2026-05-16 user-tier handoff
**Anchor:** the-stoa main at `71ea092` (Arc 25 shipped 2026-05-15 → 16 via prior POLYBIUS session)

**Goal at start:** PRINCIPAL pasted `HANDOFF_POLYBIUS_2026-05-16.md` to a fresh user-tier session. Recommended menu of 5 next-steps; PRINCIPAL chose menu item 2 ("Apply Arc-25 drift in consumer workspaces"). Three pointer tickets ready: `railway--l7o`, `ariadne--kwo`, `s4--3jp`.

**Key exchanges:**
- PRINCIPAL gave bare project-direction choice; everything else routed at user-tier per "user-tier approves technical-tier decisions itself."

**Artifacts produced:** none new this phase.

**Discipline reinforced:** Handoff-as-substrate (handoff doc + bw pointer tickets carried the durable context across sessions; no need for relay-channel queries until much later).

---

## §2 — Arc-25 drift apply across 3 consumer workspaces

**Phase:** check.sh → apply.sh --yes per workspace
**Anchor:** workspace commits `86e4141` (railway_stoa), `677150f` (ariadne-core-workspace), `3dbc0c6` (sector-4)

**Goal at start:** Three consumer workspaces drifted 5 files behind upstream (operating-disciplines.md §20 + 4 CAPTAIN envelopes). Pointer tickets explicitly anticipated a gap: "5 files + 1 new skill."

**Key exchanges:**
- Verified drift surface was exactly Arc 25 via `git diff --stat 50d70f2..71ea092 -- substrate/` (zero substrate-file changes post-Arc-25-ship).
- `apply.sh --yes` against all three with clean `.claude/` git status verified beforehand (only `.substrate-last-check` modified; safe to auto-bundle).

**Decisions:**
- Used `--yes` rather than per-file walk: PRINCIPAL approved macro action; each workspace's git status was clean; pointer ticket scope exactly matched check.sh output.
- Followed up with `install.sh --target project` per workspace to deploy the NEW `credential-discipline` skill — apply.sh handles existing-file drift only, not new files.

**Artifacts produced:** workspace commits `86e4141`, `677150f`, `3dbc0c6`; sector-4 added to consumer-workspaces.txt at the-stoa commit `b879803`.

**Failure modes caught:** sector-4 missing from registry (no-args check.sh sweep would have silently skipped it). Caught manually via handoff naming the workspace; fixed in same commit batch.

**Discipline reinforced:** Fix-now (§4.8) — registry gap fixed inline rather than deferred.

---

## §3 — Apply-vs-install asymmetry surfaced; Option B selected

**Phase:** Substrate-design discussion triggered by §2 observation
**Anchor:** discussion → stoa--dxw filed → Option B chosen

**Goal at start:** The §2 work surfaced that check.sh / apply.sh are deployed-file-centric (iterate what's in workspace `.claude/`), while install.sh is source-centric (iterate what substrate THINKS should be deployed). When substrate ADDS a new file, check.sh reports CURRENT for the workspace even though it's missing the addition. The verdict lies.

**Key exchanges:**
- PRINCIPAL: "I want to talk more about this." Then "I want to fix the system so the full picture surfaces."
- PRINCIPAL probed for completeness: "How sure are we that Option B will at least surface any issues that might need my attention to resolve and how likely is it to allow you to resolve issues without my help?"
- Agent answered honestly: ~80-85% autonomous on routine drift-apply; remaining 15-20% genuinely needs PRINCIPAL judgment (local-vs-upstream attribution, OBSOLETE removal, uncommitted-edit conflicts). Reframed Option B from "two categories" to "three categories + uncommitted-state pre-flight."
- PRINCIPAL: "Ok, go with option B."

**Decisions:**
- Option B over Option A (apply.sh growing `--add-missing`): preserves the seam; avoids the source-side coupling apply.sh was explicitly designed around.
- Three detection categories: DRIFTED + MISSING + OBSOLETE; uncommitted-state as pre-flight.
- check.sh output routes operator to apply.sh / install.sh / install.sh --prune-obsolete per category; apply.sh stays narrow.

**Artifacts produced:** `stoa--dxw` ticket; `substrate/arcs/arc-26-build-directive.md` (Arc 25 template adapted; 8 LOCKED architectural decisions; ~1-2 files in scope).

**Discipline reinforced:** Bidirectional translation (`operating-disciplines.md` §8.2) — PRINCIPAL's "fix the system so the full picture surfaces" reframed scope from missing-detection to full-picture-detection. Agent corrected its own initial framing (option 2 → Option B with three categories) after PRINCIPAL named completeness as the goal.

---

## §4 — Arc 26 dispatch + execution (autonomous mode)

**Phase:** PLINY + project-tier POLYBIUS dispatched at the-stoa; user-tier POLYBIUS exception-handler
**Anchor:** dispatch 09:34Z → ship 09:54Z; PR #6 merged at `6ccfd0e`

**Goal at start:** PRINCIPAL shut down stale the-stoa sessions; new fresh sessions ready; user-tier POLYBIUS authored two activation pastes (`HUMAN_paste-pliny-arc-26-instruction.md` + `HUMAN_paste-polybius-arc-26-instruction.md`).

**Key exchanges:**
- PRINCIPAL: "They appear to be off and running can you verify?" → user-tier POLYBIUS confirmed via reading `stoa--dxw` init handshakes from both project-tier seats.
- PRINCIPAL: "I'm going afk I may be back soon and I might sleep for a long time. Depends on my sleep disorder."
- User-tier POLYBIUS entered autonomous-mode-exception-handler per role file §13.4; set polling cron `870a9a65` at `*/7 * * * *`; posted handshake on `stoa--dxw`.

**Decisions:**
- User-tier polling cadence `*/7` (off-minute to avoid fleet alignment per CronCreate hygiene).
- Push-notification triggers locked: arc-close (one-shot summary), authorship issues (always), substance disagreement, irreducible ambiguity, peer-silence > 60 min, smoke-test failure with directive-spec mismatch.
- User-tier resolves at user-tier without waking PRINCIPAL for: A8 scope-creep (recite directive), technical-tier substance disagreement (adjudicate via A1-A8).
- User-tier did NOT comment on `stoa--dxw` for routine status — that's project-tier POLYBIUS's job; user-tier comments reserved for cross-workspace context.

**Arc 26 timeline (PLINY side):**
- 09:34Z: dispatch + init handshakes
- 09:34Z-09:43Z: Phase 1 (DAEDALUS PASS → ARGUS REVISE w/ 4 P0 → DAEDALUS rev2 PASS → ARGUS round 2 PASS)
- 09:43Z-09:47Z: Phase 2 (ADA build; one in-flight defect fix — pipefail defang on empty grep — ARGUS missed on text-only review)
- 09:47Z-09:50Z: Phase 3 (VERA + CATO + ZENO parallel; VERA 8/8 PASS; ZENO 7/7 + 8/8 + 10/10 PASS; CATO conditional-pass w/ 2 P1 + 4 P2)
- 09:50Z-09:53Z: ADA polish round (all 6 CATO findings + 1 self-caught follow-on)
- 09:53Z-09:54Z: Phase 4 smoke + PR + squash-merge + close

**Artifacts produced:** Arc 26 merge commit `6ccfd0e`; `agents/design/arc-26/design.md` + `design-rev2.md`; check.sh 489→893 lines; SKILL.md 174→post-polish-sized.

**Failure modes caught (substrate working as designed):**
- ARGUS round 1 caught 4 P0 design defects pre-build (apply.sh harvest-pattern collision; broken IFS-join; broken grep-count idiom; incomplete OBSOLETE routing for MAJORs)
- ADA caught one defect ARGUS round 2 missed on text-only review (real-execution: pipefail propagating from empty grep)
- CATO caught 6 wording-precision findings post-build (frontmatter staleness; classifications-table routing not tier-branched; --help sed regex; --quiet dead flag; etc.)
- VERA Probe 8 caught the apply.sh-coupling-to-distinct-prefixes structural fence holding

**Discipline reinforced:** Multi-layer verification catches different defect classes (text-audit catches text bugs; build-validation catches execution bugs; cold-read catches drift; spec-check catches deliverable gaps). All four layers fired in Arc 26.

---

## §5 — User-tier autonomous polling; closure detection; arc ship-push

**Phase:** Three cron fires during PRINCIPAL AFK
**Anchor:** cron `870a9a65`; fires at ~09:40Z, ~09:47Z, ~09:54Z

**Goal at start:** PRINCIPAL asleep; user-tier watching from outside the project-tier coordination loop.

**Key exchanges (cron-internal):**
- Fire #1: Phase 1 in motion; silent.
- Fire #2: Phase 2 + 3 returns; CATO findings dispatched to polish round; silent. Noted "sector-4 cleanup deferred to project-tier POLYBIUS for routing" as future PRINCIPAL surface but not yet escalation.
- Fire #3: Arc closed; PushNotification sent ("Arc 26 SHIPPED: stoa--dxw closed PASS; merged 6ccfd0e (PR #6). check.sh now surfaces MISSING + OBSOLETE + uncommitted. stoa--501 sector-4 cleanup awaits your discretion on wake."); CronDelete; engagement over.

**Decisions:**
- Mobile push didn't deliver (Remote Control inactive); desktop push only. Acceptable — durable substrate (closed bw ticket + merged PR) is the canonical record; push is a wake-up hint.
- User-tier POLYBIUS did NOT preemptively act on `stoa--501` (sector-4 cleanup) — project-tier POLYBIUS had already routed it as PRINCIPAL-discretion; user-tier posted awareness ack and stood by.

**Artifacts produced:** PushNotification; awareness comment on `stoa--501`; cron `870a9a65` cancelled.

**Discipline reinforced:** No-agent-fatigue + autonomous-ship (§4.6) — PLINY shipped autonomously per directive Phase 4; user-tier did not gate. Both PRINCIPAL-AFK pattern and clean-PASS-autonomous-ship worked as designed.

---

## §6 — PRINCIPAL wake; sector-4 revert decision

**Phase:** PRINCIPAL returned from sleep; reviewed open items
**Anchor:** `stoa--501` REVERT chosen; sector-4 reset to `3dbc0c6` then clean re-apply

**Goal at start:** PRINCIPAL awake; 3 follow-ups in bw (`stoa--501` P3 sector-4, `stoa--8x5` P4 gitignore, `stoa--sc8` P4 registry) + 2 housekeeping items I'd surfaced (orphan arc designs, untracked HUMAN paste files). PRINCIPAL chose `stoa--501` first; the keep-vs-revert framing.

**Key exchanges:**
- PRINCIPAL: "R" (chose revert without expanding).
- User-tier POLYBIUS executed: `git reset --hard 3dbc0c6` (back to clean post-Arc-25 state) → `apply.sh --yes` against current the-stoa → re-check.sh verified CURRENT.

**Decisions:**
- Hard reset: PRINCIPAL approved R, which explicitly includes the destructive reset. Pre-existing untracked `agents/design/s4--bbz/design.md` preserved (git reset --hard doesn't touch untracked).
- Clean re-apply against the-stoa current (`2e0e2ce` = `6ccfd0e` content): replaces 4 probe commits with 2 legitimate operator-authorized apply commits (`b76b05a` snapshot + `ff61574` apply).

**Artifacts produced:** sector-4 commits `b76b05a` + `ff61574`; `stoa--501` closed with REVERT disposition; the-stoa housekeeping commit `b56b3e3` (.gitignore narrowed + registry add) — followed by the install.sh-driven deploy of 8 MISSING files into the-stoa's own .claude/ (meta-loop closure).

**Failure mode REVEALED (load-bearing — sets up §7):** the `stoa--sc8` housekeeping (adding the-stoa to consumer-workspaces.txt) immediately surfaced 8 MISSING files in the-stoa's own `.claude/`. Until that registry add, no-args check.sh swept past the-stoa silently. The substrate-canonical workspace was the most-drifted workspace, and the drift was structurally invisible.

**Discipline reinforced:** Verify-then-execute (§4.3) — registry add was verified to do what stoa--sc8 promised (pick up the-stoa); discovered 8 MISSING during verification; closed loop in same engagement rather than deferring.

---

## §7 — Observation 1: PRINCIPAL gates wait for PRINCIPAL

**Phase:** Substrate-discipline reframe (PRINCIPAL surfaced)
**Anchor:** PRINCIPAL message after sector-4 revert: *"First, something that needs to be surfaced to a human needs to wait until the human comes back not bypassed because the human is afk."*

**The observation, stated cleanly:**

The substrate today has two patterns that look related but are NOT equivalent:
- **Autonomous mode** = "PRINCIPAL is exception-handler; routine work proceeds; surface to PRINCIPAL only on escalation triggers."
- **PRINCIPAL-discretion tags** = "this needs PRINCIPAL judgment."

Arc 26's VERA Probe 8 collided them. The probe's design clause `PRINCIPAL-discretion per design §6` was treated by the quality chain as a "proceed-and-let-PRINCIPAL-disposition-after" marker rather than a "block-until-PRINCIPAL-present" gate. PRINCIPAL was AFK at design time; the chain shipped; the post-hoc `stoa--501` was the cleanup. **Should have been pre-hoc authorization.**

**The rule, declared by PRINCIPAL:**

> A design clause that names PRINCIPAL as the deciding seat is a BLOCK, not a TAG. Autonomous mode does not get to skip past it. PRINCIPAL-AFK on a PRINCIPAL-gated decision means the workflow waits.

**Why this matters structurally:**

The substrate's discipline-of-attention (per `MAJOR_POLYBIUS.md` §3 "operationalize where human attention is required") names where human input is load-bearing. Autonomous mode is a *cadence* discipline (when to surface during normal work) — it is NOT a *gate-override* discipline (it does not relax authorization-required moments). Today the substrate conflated them. The fix is to separate them cleanly.

**Implications:**

- **Vocabulary discipline at design time:** "PRINCIPAL-discretion per design §X" must mean "this workflow PAUSES until PRINCIPAL is here." If a design clause needs PRINCIPAL judgment, the design must wait for PRINCIPAL. Post-hoc cleanup is not equivalent to pre-hoc authorization.
- **Autonomous-mode wiring:** when an autonomous-mode workflow encounters a PRINCIPAL-gated clause, it should HALT and escalate immediately — not proceed-then-flag. The polling-cron-prompt template's escalation step needs an explicit case for this.
- **CAPTAIN envelope updates (DAEDALUS especially):** designs that contain PRINCIPAL-gating clauses must surface that gating to PRINCIPAL at design ratification time, not defer to post-build cleanup.
- **N=1 caveat (§15):** today's observation is one case. PRINCIPAL declared the discipline (rather than the substrate inducing it from accreted evidence), so the §6.7.1 three-condition gate doesn't apply the same way — PRINCIPAL's project-direction authority is the right source for this kind of rule. The supporting evidence is the Arc 26 case + the consistent shape of the substrate's existing operator-intent discipline elsewhere (apply.sh consent gates, install.sh --dry-run, credential-discipline canon — all "operator authorizes BEFORE execution").

**Discipline surfaced (new):** PRINCIPAL-gates-wait-for-PRINCIPAL. Distinct from autonomous-mode escalation cadence. To be encoded in `operating-disciplines.md` + CAPTAIN envelopes + autonomous-mode-activation template.

---

## §8 — Observation 2: Mechanical scripts; agents for intelligent inspection

**Phase:** Substrate-architecture reframe (PRINCIPAL surfaced)
**Anchor:** PRINCIPAL message in same exchange: *"Second, I think we are spending way too much time trying to get script workflows perfect when the answer is to run the script, then run an agent with a script to check what happened including anything strange and then let polysibius fix any of the strangeness with human approval if necessary."*

**The observation, stated cleanly:**

Arc 26 was the "make check.sh smarter" approach. ~20 min of full gauntlet to add three drift categories + a routing footer to a bash script. Every new edge case = more script logic = more gauntlet to verify. The script has to anticipate every shape of strangeness it might encounter and emit it correctly.

PRINCIPAL's alternative architecture, stated as a 3-step pattern:

1. **Mechanical script** runs (apply.sh / install.sh — the deterministic, narrow part).
2. **Inspection agent** runs a verification script + reads the resulting state + surfaces anything strange — including things the script wasn't pre-programmed to notice.
3. **POLYBIUS** routes strangeness — fixes routinely, escalates to PRINCIPAL when judgment is needed (per §7's discipline).

**The cost calculus that justifies it:**

Agent tokens are cheap; iteration is fast; a fresh agent reading post-mechanical state with the brief "tell me what's surprising" is much more flexible than a bash script trying to enumerate categories of surprise. Same logic as the fix-now discipline (`MAJOR_POLYBIUS.md` §4.8) — the 2010 instinct (perfect-the-script) is wrong for 2026 with cheap agent passes.

**Where intelligence lives — the structural shift:**

Today's substrate has intelligence-in-script (check.sh tries to anticipate; apply.sh has the consent walk; install.sh has --dry-run + --prune-obsolete). Arc 26's check.sh extensions ADDED intelligence in this layer.

PRINCIPAL's pattern says: keep scripts mechanical; move recognition-of-strangeness to an agent layer that the substrate dispatches after any mechanical operation. The agent can notice things the script wasn't pre-programmed for (e.g., "sector-4 just got 4 commits from a probe — that's unusual for a substrate-update operation, even though check.sh sees CURRENT").

**Implications for Arc 26 specifically:**

check.sh's extensions (MISSING + OBSOLETE + uncommitted-state + routing footer) are NOT WRONG — they catch the silent-CURRENT cliff that was the immediate failure mode. But they're the wrong layer of intelligence for the long run. The forward pattern is:

- Keep check.sh narrower (deployed-file-centric is fine; doesn't need to grow source-side parsing for every new substrate file class)
- Add an inspection-agent layer that POLYBIUS dispatches after any mechanical substrate operation
- That agent reads the result + git state + workspace state + surfaces strangeness intelligently (LLM-grade recognition, not pattern-match)

**Implications for the substrate broadly:**

Beyond substrate-update, this pattern probably applies to:
- Probe execution (VERA): mechanical probe runs + inspection agent reads result + flags anomalies (rather than the probe ITSELF having to enumerate failure modes)
- Build verification (ADA): build runs + inspection agent reads build artifacts + flags unexpected state (rather than test grammar having to anticipate everything)
- Deploy operations (any credentialed CI flow): workflow runs + inspection agent reads CI output + flags surprises (rather than CI smoke-test bash having to be comprehensive)

**N=1 caveat (§15):** today's observation is one instance. PRINCIPAL is making an architectural claim, not inducing one from evidence. The Arc 26 work today is the empirical anchor; future arcs would test whether the inspection-agent pattern actually shifts the cost-to-comprehensive-coverage trajectory PRINCIPAL is predicting. Substrate canon can accrete supporting evidence over time per §6.7.1.

**Discipline surfaced (new):** mechanical-script / agent-inspection split. Distinct from check-substrate-updates' current architecture. To be encoded as a substrate pattern with worked examples (probably starting with substrate-update flow itself).

---

## §9 — Synthesis: tighter substrate-update flow

**Phase:** How the two observations combine
**Anchor:** PRINCIPAL's two-observation message + this section's synthesis

**The connection:**

Observation 1 (§7) is about discipline: PRINCIPAL gates wait for PRINCIPAL. It governs WHEN human input is required.

Observation 2 (§8) is about architecture: agents do intelligent inspection; scripts stay mechanical. It governs HOW post-execution recognition happens.

Together, they describe a tighter substrate-update flow:

1. **Mechanical script** runs (apply.sh / install.sh / etc. — deterministic, narrow).
2. **Inspection agent** reads result + state + flags anything strange.
3. **POLYBIUS triage** — routes findings:
   - Routine technical-tier findings → POLYBIUS fixes inline (per fix-now §4.8 + user-tier-approves-tech-decisions discipline).
   - PRINCIPAL-gate findings → workflow PAUSES until PRINCIPAL is present (per §7's discipline). Autonomous mode does not relax this.
4. **PRINCIPAL** disposition on the gated cases — actual authorization, not post-hoc cleanup.

**What changes vs today's flow:**

- check.sh / apply.sh / install.sh stay roughly as-is (or get LIGHTER over time as intelligence moves to inspection-agent).
- New substrate component: post-execution inspection agent (skill? CAPTAIN envelope addition? template?).
- Autonomous-mode discipline gains an explicit pause-on-gate trigger.
- Design-time vocabulary tightens: "PRINCIPAL-discretion per design §X" stops being a valid post-hoc-disposition marker; becomes a pause-the-workflow marker.

**What this would have changed about today:**

- Arc 26 might not have needed to ship a more-complex check.sh — an inspection-agent layer post-apply.sh would have noticed "MISSING file detected" without check.sh having to enumerate categories.
- VERA Probe 8's design would have been challenged at DAEDALUS time: "this probe mutates a real workspace; PRINCIPAL is AFK; therefore the probe waits OR uses a throwaway clone." The post-hoc `stoa--501` ticket wouldn't have been needed.

**Discipline reinforced:** Bidirectional translation (`operating-disciplines.md` §8.2) — PRINCIPAL's two observations re-described intent that the substrate had partially missed; the substrate's response (this retro + the forthcoming epic + child tickets) folds the new intent in.

---

## §10 — Forward path

**Phase:** What we file from here
**Anchor:** Forthcoming `stoa--` epic + 2 child tickets

**Decided in conversation:** retrospective doc (this file) first, then ONE `stoa--` epic with both disciplines as child tickets.

**Epic + children to file (after this retro lands):**

- **Epic:** Substrate-update architecture: principal-gate discipline + mechanical-script/agent-inspection split (cross-refs this retro).
- **Child 1:** PRINCIPAL-gate discipline — `operating-disciplines.md` section + CAPTAIN envelope updates (DAEDALUS especially) + autonomous-mode-activation template update + polling-cron-prompt template update.
- **Child 2:** Mechanical-script / agent-inspection split — new substrate-tier inspection-agent skill (or CAPTAIN envelope addition); worked-example pointer at substrate-update flow; revisit Arc 26's check.sh additions for "what could move to inspection-agent layer eventually."

**Open scope questions for the epic:**

- Should Child 1 reopen the autonomous-mode discipline at `operating-disciplines.md` §10/§11 (a significant edit), or accrete as a new short section that cross-refs?
- Should Child 2 start with the inspection-agent as a skill (POLYBIUS-invocable) or as a new CAPTAIN seat (gauntlet-pipeline component)? The former is lighter; the latter is more structural.
- Probe-design discipline (probes-mutating-real-workspaces require explicit per-execution authorization OR throwaway clone) is a sub-case of Child 1 — fold in, or its own ticket?

**§15 caveat reminder:** both child tickets carry empirical anchor of N=1 (Arc 26's specific failures). Promotion to full substrate canon should accrete additional evidence over time per §6.7.1. The arc that builds them should NOT auto-promote retrospective observations to structural claims; that's the §15 honest-scope discipline.

**Disciplines reinforced across the session:**

- Fix-now (§4.8): registry add, gitignore narrowing, orphan-arc-design tracking, paste-file tracking — all done inline rather than deferred.
- Verify-then-execute (§4.3): registry add was verified to do what `stoa--sc8` promised; surfaced 8 MISSING; closed loop.
- User-tier-approves-tech-decisions: PRINCIPAL only gated on Option A vs B + REVERT-vs-KEEP + capture-method. Everything else (file commits, propagation, cleanup) ran at user-tier.
- Autonomous-ship (§4.6): PLINY shipped Arc 26 autonomously per directive Phase 4; user-tier did not gate.
- N=1 honesty (§15): both observations from today flagged as N=1; accretion path named rather than auto-promoting.

**Engagement closed at:** ~17:40Z (this retro), with the housekeeping commits already landed and the epic + child tickets queued for next action.

End retrospective.
