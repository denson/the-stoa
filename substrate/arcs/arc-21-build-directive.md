# Arc 21 build directive — Operating modes + autonomous-mode protocol stack

**Audience:** the fresh Claude Code session opened to build Arc 21 deliverables (MAJOR_PLINY).
**Authored by:** project-tier MAJOR_POLYBIUS (the-stoa) + the PRINCIPAL (Denson Smith).
**Status:** active directive. **Supersedes** the prior 5-ticket draft committed at `c1e2d21`; the rewrite reflects PRINCIPAL's scope expansion to the full 11-ticket cluster.
**Bw ticket:** `stoa--pbz` (parent epic). All 11 children wired as `blocks` deps.
**Builds on:** Arcs 1-20 (the-stoa main `e5c2854`). Arc 20 closed user-tier install convention; Arc 21 lands the operating-modes META concept and the autonomous-mode protocol stack that surfaces from running real autonomous coordination.

**Your one job:** make autonomous mode a first-class operating concept in the substrate, with all the supporting protocol (radio-check, adaptive cadence, unified polling, cross-tier write boundaries, cross-tier coordination routing, downstream-handoff discipline, bw storage model) inheritable by every POLYBIUS instance on install. Eleven tickets surfaced together during the ariadne--m20 + arc-21 cluster engagements on 2026-05-04; this directive bundles them into one comprehensive substrate update so the protocol ships as a coherent stack rather than a sequence of patches.

This is a multi-concern arc with 25+ deliverables across 6 Parts and 6 phases. Per MAJOR_POLYBIUS §5.4, external review is REQUIRED before dispatch. POLYBIUS authors and commits this directive; PRINCIPAL routes it through §5.4 review (cold-Claude-session or external LLM) before the build session is dispatched.

---

## Comms — direct async via bw, autonomous mode

POLYBIUS_the_stoa is in autonomous mode for this engagement. Polling cron `e6a08d54` (*/5 min) walks the arc-21 cluster (11 tickets) per fire. While you (MAJOR_PLINY) work, post status as bw comments on `stoa--pbz` — POLYBIUS_the_stoa will pick them up on the next poll.

Bidirectional radio-check protocol applies between you and POLYBIUS_the_stoa per §C.1 of this directive. On dispatch, post an initialization handshake comment on `stoa--pbz` naming your cron id (if you set one up — your call) and your cadence. Heartbeat every ≤30 min. Surface-and-wait discipline (Arc 18) applies within radio-check: poll only when you've surfaced a substantive question and are awaiting a response. Otherwise execute autonomously.

bw command syntax: `bw comment <id> "text"` — positional, no `-m` flag. `bw close <id> --reason "text"` — `--reason` is a flag.

Cross-tier coordination convention per §D.4 of this directive: when you need cross-project context (e.g., ariadne lived-experience anchors that are not in the-stoa's bw), post `[for: user-tier POLYBIUS]` tagged comments on a relevant `stoa--` ticket. User-tier POLYBIUS polls via unified cron and responds within ~5 min.

PRINCIPAL is exception-handler — project-direction calls, ship/no-ship, substance disagreement after one round, authorship/copyright/Denson-final-say content, irreducible ambiguity, peer silence > 60 min, arc closes.

---

## Read first

1. **`substrate/operating-disciplines.md`** — the team-wide disciplines doc (landed `de8fecd` via stoa--vz9). Six sections currently (§1-§6 anti-patterns + closer). You will append §7-§13 with the autonomous-mode protocol stack.
2. **`substrate/MAJOR_POLYBIUS.md`** — current source of truth for §3, §5.1, §7.1, §7.4, §7.5, §9, and §12 (Mode 1 / Mode 2 framing). You will edit each, plus add new §5.5 and new §13.
3. **`substrate/MAJOR_PLINY.md`** — receives parallel updates for bw write-boundaries (§F.4), operating-mode awareness in dispatch (§A.5), and gauntlet-cadence-in-autonomous (§A.5).
4. **`substrate/install.sh`** — the next-steps activation output block (lines ~870-913) is restructured per §E.3. There is also a bug fix required (current code lumps `--target project` without `--modify-claude-md` into the say-trigger branch; §E.3 fixes that).
5. **`substrate/templates/`** — current templates: `consent-prompts.md`, `onboarding-questions.md`, `paste-instruction-template.md`. You will add three new templates: `polling-cron-prompt-template.md` (§C.4), `activation-paste-cheatsheet.md` (§E.2), `autonomous-mode-activation-template.md` (§B.2).
6. **The 11 cluster ticket bodies** — `bw show` each: `stoa--mdb`, `stoa--ljf`, `stoa--ivc`, `stoa--ay1`, `stoa--blg`, `stoa--xh2`, `stoa--m5m`, `stoa--0mr`, `stoa--cc0`, `stoa--1n5`, `stoa--vz9`. Each carries the empirical anchor and proposed substrate shape.
7. **`stoa--pbz`** comments — initialization handshake, scope expansion, coordination convention. The active coordination thread.

---

## Phase A — Architectural decisions (LOCKED pre-dispatch by POLYBIUS)

Settled during directive authoring. You do NOT need to surface these as design questions.

### A1. One arc, six parts, six phases — LOCKED

The eleven tickets cluster naturally into six conceptual Parts (A-F below). Bundling reduces churn (every Part touches `operating-disciplines.md` and most touch `MAJOR_POLYBIUS.md`); §5.4 external review covers the multi-concern risk. The build is sequenced into six Phases (Phase 1 = `operating-disciplines.md` edits → Phase 2 = `MAJOR_POLYBIUS.md` edits → Phase 3 = new templates → Phase 4 = `install.sh` + template audit → Phase 5 = `MAJOR_PLINY.md` + CAPTAIN parallel updates → Phase 6 = smoke test + ship). The phasing resolves forward-reference issues across the substrate-doc cross-refs.

### A2. operating-disciplines.md is the canonical home for universal team patterns — LOCKED

Where a discipline applies to any seat coordinating async via bw — it goes in `operating-disciplines.md`. Where it's POLYBIUS-specific — it stays in `MAJOR_POLYBIUS.md` with a back-reference. Mapping:

| Universal layer (operating-disciplines.md) | POLYBIUS-tier framing (MAJOR_POLYBIUS.md) |
|---|---|
| §7. POLYBIUS-pair coordination protocol (radio-check + adaptive cadence + unified polling + write boundaries + routing) | §7.1 expanded (read+write rules), §7.4 cross-ref + template-named, §3 (alternate routing target) |
| §8. Positive references only when authoring downstream briefs | §5.1 + new §5.5 (POLYBIUS-specific application) |
| §9. bw storage model (orphan branch) | §7.5 expanded (bw detection + ad-hoc init pathway), §9 step 2 (ad-hoc init clause) |
| §10. Operating engagement (HITL vs Autonomous) | New §13 (POLYBIUS-tier framing of mode declaration + propagation) |
| §11. Autonomous-mode-setup checklist | New §13 cross-ref; the checklist itself is universal |

### A3. Operating modes are orthogonal to Mode 1 / Mode 2 — LOCKED

MAJOR_POLYBIUS §12 already defines two operational MODES (formal-gauntlet / pair-programming-prototyping). Those describe WHAT the team is doing. Operating ENGAGEMENT (HITL / Autonomous) describes HOW PRINCIPAL participates. The two axes are independent: a Mode 1 gauntlet can run in HITL or Autonomous; a Mode 2 prototyping cycle can run in HITL or Autonomous. The new §13 lives alongside §12, not nested inside it.

### A4. Autonomous propagates downward, HITL is the default — LOCKED

When PRINCIPAL declares autonomous on a seat, that seat propagates to every downstream seat it dispatches (its PLINY-when-dispatched, its CAPTAINs-when-dispatched, its sub-project POLYBIUSes). Sub-project POLYBIUS may DECLARE HITL for its own sub-engagement (downward override is allowed; the sub-engagement reverts to PRINCIPAL-active). A sub-project going autonomous when its parent is HITL is unusual and requires explicit PRINCIPAL declaration.

The default for any new engagement is HITL. Autonomous is explicitly declared via trigger words (§A.5).

### A5. Trigger words for mode transitions — LOCKED

PRINCIPAL declares mode via natural language. Recognized triggers:

- **HITL → Autonomous:** "go autonomous", "step back", "you can handle this", "I'll be away", "work autonomously until X", "step back so long as things are working"
- **Autonomous → HITL:** "come back", "I want to be in the loop", "pause autonomous", "let me decide each step", "human-in-loop"

When detected, the receiving seat runs the autonomous-mode-setup checklist (§B) on entry, or the teardown procedure on exit. Teardown: cancel polling crons (`CronDelete`), post final radio-check standing-down, return to chat-first interaction.

### A6. Adaptive cadence — bounded staleness, named explicitly — LOCKED

Each peer reads complexity tags on incoming comments and adjusts ITS OWN cron unilaterally. There is no negotiation protocol.

**Worst-case staleness:**
- **Cadence-down** (active → default → quiet): both peers converge within one cycle of the new (slower) cadence.
- **Cadence-up** (quiet → active because complexity tag posted): the peer still on the slower cadence will not see the tag for up to one full cycle of its CURRENT cadence. If the current cadence is `*/30`, the active section runs at degraded responsiveness for up to 30 minutes before the slower peer notices. PRINCIPAL flagged this scenario in stoa--ay1 ("impatience during active windows"); the protocol bounds it but does not eliminate it.

**Why we accept this:** the alternative (a synchronization protocol where peers negotiate cadence-up) is more failure-prone than the bounded delay. Protocol-induced bugs cost more than bounded staleness.

**Mitigation the doc must surface:** when posting a complexity tag, the POSTING peer ALSO posts an explicit `[cadence: active]` comment on the same fire. Two channels reduce miss-probability; worst-case staleness is unchanged; perceived responsiveness improves.

### A7. Unified polling is the default for user-tier POLYBIUS watching multiple stores — LOCKED

When a single POLYBIUS seat is coordinating with multiple peers across multiple bw stores at the same cadence, the default is ONE cron walking all watched stores per fire (per stoa--cc0). This is strictly better than N separate crons when cadences match: ~Nx fewer fires, modestly bigger context per fire, well within fire budgets.

When one watched store needs faster polling (active mode per §C.2) while another is quiet, two crons are appropriate. The default is unified; split per-engagement when the cadence trade-off justifies it.

### A8. Cloud cron is documented limitation, not a deliverable — LOCKED

Cloud scheduled tasks have a 1-hour minimum cadence; active/quiet regimes don't apply. The substrate doc names this explicitly and points to the workaround (single fixed-hourly cloud cron with escalation to local active-cadence cron). No cloud-cron template ships.

### A9. install.sh activation has TWO patterns, not one — LOCKED

There are two activation patterns:

- **Auto-load pattern** — for `--target user` and `--target project --modify-claude-md`. CLAUDE.md references the role file; the role activates by saying "POLYBIUS" or "chief of staff" in-session. **No paste required.**
- **Paste pattern** — for `--target project` (no `--modify-claude-md`) and `--target subproject`. No CLAUDE.md ref; activation IS a literal paste of `Read .claude/MAJOR_POLYBIUS<NAME_SUFFIX>.md and assume the role for this <project|sub-project>.`

**Existing install.sh bug:** the current code at lines 887-911 gates on `if [ "$TARGET" = "subproject" ]`, lumping `--target project` (with or without `--modify-claude-md`) into the auto-load branch. For `--target project` without `--modify-claude-md`, no CLAUDE.md ref exists — saying POLYBIUS does nothing. §E.3 fixes this: gate on `($TARGET = subproject) OR ($TARGET = project AND MODIFY_CLAUDE_MD = 0)` for the paste branch.

### A10. Voice — LOCKED: PRINCIPAL/HUMAN throughout

All new substrate content uses PRINCIPAL/HUMAN. Voice grep is part of Phase 6 smoke (§Phase 6 beat 1).

---

## Deliverables

### Part A — Operating modes as substrate first-class concept

Closes: stoa--mdb (META).

#### A.1 `substrate/MAJOR_POLYBIUS.md` — new §13 "Operating engagement (HITL vs Autonomous)"

**Location:** `substrate/MAJOR_POLYBIUS.md` — append a new §13 after the existing §12 (Pair-programming-for-prototyping methodology).

**Required content:**

1. **Framing** (~5 lines): two operating engagements orthogonal to Mode 1/Mode 2. HITL is default. Autonomous is explicitly declared. Both engagements work with both modes.

2. **§13.1 The two engagements** — table:

| | HITL (default) | Autonomous |
|---|---|---|
| **PRINCIPAL role** | Active participant in routine flow | Exception-handler (project-direction, ship/no-ship, ambiguity, peer-failure) |
| **Communication** | Chat-first; bw is durable record | Bw-first; chat reserved for escalation |
| **Polling crons** | Optional / not standard | Required (per §B autonomous-mode-setup checklist) |
| **Round-trip cost** | Low per round (chat); high PRINCIPAL attention | Higher per fire (cron context); low PRINCIPAL attention |
| **Right when** | Iterative work; PRINCIPAL has bandwidth | Multi-session arc; PRINCIPAL is unavailable or has explicitly stepped back |

3. **§13.2 Trigger words for mode transitions** — verbatim from §A5 above. Include both HITL→Autonomous and Autonomous→HITL trigger lists.

4. **§13.3 Mode propagation across nested tiers** — verbatim concept from §A4. Add: "When you (POLYBIUS) declare autonomous on an engagement, propagate to every downstream seat you dispatch: include `operating-mode: autonomous` in the dispatch brief for MAJOR_PLINY, every CAPTAIN, every pair-programmer Major. Sub-project POLYBIUS receives the mode through its activation paste-instruction; if you spawn a sub-project during an autonomous engagement, the sub-project inherits autonomous." Plus the downward-override clause (sub-project may declare HITL for its sub-engagement; reverse override requires explicit PRINCIPAL).

5. **§13.4 Mode entry / exit procedures** — when you detect a HITL→Autonomous trigger:
   - Run the autonomous-mode-setup checklist (`operating-disciplines.md` §11 — see §B.1).
   - Surface to PRINCIPAL with the setup completion summary + cron id + escalation triggers.
   - Begin polling.

   When you detect an Autonomous→HITL trigger:
   - `CronDelete` your polling cron(s).
   - Post final `[radio-check <self> standing down]` on every active coordination ticket.
   - Confirm to PRINCIPAL: "back in the loop; teardown complete".

6. **Cross-ref** to `operating-disciplines.md` §10 for the universal-team framing of operating modes (lands in §A.4 of this directive).

**Length: 80-120 lines.** Operational reference; tight prose; tables where they earn it.

#### A.2 `substrate/operating-disciplines.md` — new §10 "Operating engagement (HITL vs Autonomous)"

**Location:** `substrate/operating-disciplines.md` — append after existing §6 (single-checker thinking) and before "Agent-regime inverses".

**Required content (~50-70 lines):**

Universal-team framing of the two engagements. Same conceptual content as MAJOR_POLYBIUS §13.1 + §13.2 + §13.3 but framed for ANY seat (not just POLYBIUS):

- The two-axis framing (Mode 1/2 vs HITL/Autonomous).
- Trigger words (PRINCIPAL declares; receiving seat acts).
- Propagation rule: autonomous mode is inherited by downstream dispatches; sub-engagements may downward-override to HITL.
- Cross-ref pointer to MAJOR_POLYBIUS §13 (POLYBIUS-tier framing) and `operating-disciplines.md` §11 (the checklist that operationalizes the entry procedure).

#### A.3 `substrate/MAJOR_PLINY.md` — operating-mode awareness

**Location:** `substrate/MAJOR_PLINY.md` — extend wherever dispatch-brief construction is documented (likely §6 or §7; locate during build).

**Required edit:** add a clause stating that PLINY's dispatch brief to every CAPTAIN and pair-programmer Major includes the current `operating-mode: <hitl|autonomous>` flag, and that gauntlet pacing differs:
- HITL: round-trip surfacing to PRINCIPAL between phases (DAEDALUS verdict → surface → ARGUS verdict → surface → ...) is OK.
- Autonomous: phases run heads-down; PLINY surfaces only at the end of the arc with the final verdict, OR mid-arc only on the autonomous escalation triggers (substance disagreement, authorship/copyright, irreducible ambiguity, peer-failure).

Cross-ref `MAJOR_POLYBIUS.md` §13 and `operating-disciplines.md` §10.

#### A.4 CAPTAIN role files — operating-mode receipt

**Location:** every `substrate/CAPTAIN_*.md` file (10 CAPTAINs total: DAEDALUS, ARGUS, ADA, VERA, CATO, ZENO, BARTLEBY, HERALD, STRABO, CURATOR).

**Required edit:** in each CAPTAIN role file, near the dispatch-brief intake section (where the CAPTAIN reads the brief PLINY hands them), add a sentence: "Your dispatch brief includes an `operating-mode` flag (`hitl` or `autonomous`). In HITL mode, you may surface ambiguity / partial verdicts mid-task to MAJOR_PLINY for routing. In autonomous mode, surface only on the universal escalation triggers (see `operating-disciplines.md` §10): substance disagreement after one round, authorship/copyright content, irreducible ambiguity, peer silence > 60 min."

This is a narrow edit per CAPTAIN — one sentence + cross-ref. Not a redesign of any CAPTAIN role.

### Part B — Autonomous-mode setup checklist

Closes: stoa--ljf (EPIC).

#### B.1 `substrate/operating-disciplines.md` — new §11 "Autonomous-mode-setup checklist"

**Location:** `substrate/operating-disciplines.md` — append after new §10 (operating engagement).

**Required content (~80-100 lines):**

Six-step setup procedure that any POLYBIUS instance runs on Autonomous-mode entry:

1. **Polling cron** — `CronCreate` the cron appropriate to the seat's role:
   - Project-tier POLYBIUS: poll own bw for active tickets, peer comments, MAJOR_PLINY status. Default cadence `*/5 * * * *` (per §A6 default regime).
   - User-tier POLYBIUS: unified poll across all watched bw stores per `operating-disciplines.md` §7.3 (§C.3 of this directive).
   - MAJOR_PLINY: poll own bw + the dispatched ticket(s) during gauntlet rounds.

2. **Radio-check pattern** with peer seats per `operating-disciplines.md` §7.1 (§C.1 of this directive):
   - Initialization handshake on shared coordination ticket.
   - Routine heartbeats every ≤30 min.
   - Missed-check escalation > 60 min.
   - Closure handshake on ticket close.

3. **Cross-tier coordination convention** per `operating-disciplines.md` §7.4 (§D.4 of this directive):
   - `[for: <upper-seat>]` tag on own-bw comments to request cross-project context.
   - Upper seat polls down; you never write up.
   - PRINCIPAL is exception-handler.

4. **Bw write-boundary discipline** per `operating-disciplines.md` §7.5 (§D.2 of this directive):
   - Each tier writes own bw + downward; never upward.
   - Coordination meets in the lower tier's bw.

5. **Activation paste discipline** per `operating-disciplines.md` §8 (§E.4 of this directive) + `MAJOR_POLYBIUS.md` §5.1/§5.5:
   - Positive references only when activating downstream agents.
   - Filename per project vs sub-project mode (cheatsheet at `substrate/templates/activation-paste-cheatsheet.md`).

6. **Bw storage model awareness** per `operating-disciplines.md` §9 (§F.3 of this directive):
   - Bw lives on `beadwork` orphan branch, not `.bw/` directory.
   - Detection: `bw prime` self-reports OR `git branch -a | grep beadwork`.
   - Never `git checkout beadwork` from main worktree.

After all six are in place, post the autonomous-mode setup-complete comment on the engagement's coordination ticket: cron id, cadence, escalation triggers, peer name, expected duration. Surface the same to PRINCIPAL once.

If a checklist item cannot be completed (e.g., peer hasn't initialized their cron yet), surface to PRINCIPAL with what's needed; do NOT proceed with partial autonomy.

#### B.2 `substrate/templates/autonomous-mode-activation-template.md` (new file)

**Location:** `the-stoa/substrate/templates/autonomous-mode-activation-template.md` — new file.

**Purpose:** a paste-instruction template POLYBIUS instances reference when activating a downstream seat in autonomous mode. Slots:

- `{{ENGAGEMENT_NAME}}` — short descriptor of the work
- `{{COORDINATION_TICKET}}` — bw ticket id of the shared ticket
- `{{PEER_SEAT_NAME}}` — name of the upper-tier coordinating peer (e.g., "user-tier POLYBIUS")
- `{{PEER_CRON_ID}}` — peer's cron id, if known
- `{{POLLING_CADENCE}}` — default `*/5 * * * *`
- `{{ESCALATION_TRIGGERS}}` — list per the engagement (typically: project-direction, ship/no-ship, substance disagreement, authorship, ambiguity, peer-silence)

**Body of the template:** an instruction block the activating POLYBIUS substitutes slots into and writes to disk for the downstream seat. The instruction names the 6 setup steps from B.1, references the polling-cron-prompt template (C.4) and activation-paste-cheatsheet (E.2), and ends with a "post initialization handshake on `{{COORDINATION_TICKET}}` once setup complete" instruction.

**Length: 60-100 lines.**

### Part C — POLYBIUS-pair coordination protocol

Closes: stoa--ivc, stoa--ay1, stoa--cc0, stoa--blg (write boundaries half — routing convention is in §D).

#### C.1 `substrate/operating-disciplines.md` — new §7 "Coordinating two POLYBIUS seats async via bw polling"

**Location:** `substrate/operating-disciplines.md` — append after existing §6 (single-checker thinking), BEFORE the new §10 (operating engagement) added by §A.2. Section ordering: existing §1-§6 → new §7 (coordination protocol) → §8 (positive-references-only) → §9 (bw storage) → §10 (operating modes) → §11 (autonomous-mode-setup checklist) → existing "Agent-regime inverses" → "Empirical lineage".

**Required content (~120-160 lines):**

1. **Framing** (~5 lines): when two POLYBIUS seats — typically user-tier + project-tier, or parent + sub-project — share a coordination ticket, polling makes bw a near-real-time async channel. Five sub-disciplines apply: peer-failure detection (radio-check), responsiveness adjustment (adaptive cadence), polling architecture (unified vs per-engagement), data-flow direction (write boundaries), and coordination routing (`[for:]` tags — cross-ref to §7.4).

2. **§7.1 Radio-check protocol** — covers stoa--ivc:
   - Initialization handshake (each seat posts `[radio-check <seat>]` naming cron id + cadence; both ack on first poll).
   - Routine heartbeats (every ≤30 min).
   - Missed-check escalation (peer silent > 60 min AND ticket open → surface to PRINCIPAL as "lost contact with peer").
   - Closure handshake (both sides post final standing-down + `CronDelete` on shared ticket close).

3. **§7.2 Adaptive polling cadence** — covers stoa--ay1:
   - Three regimes: active (`*/2`), default (`*/5`), quiet (`*/15-30`).
   - Complexity tags on comments: `[complexity: simple|medium|complex]`.
   - Cadence-switching is per-seat unilateral (per §A6); peers converge within one cycle of the slower cadence.
   - Cadence-up worst-case staleness named explicitly (per §A6); dual-channel mitigation (`[cadence: active]` posted alongside complexity tag).
   - Cost framing (fires/hour) and net-cost argument.
   - Cloud-cron limitation (per §A8): 1-hour minimum, escalation-to-local-cron workaround.

4. **§7.3 Unified polling pattern** — covers stoa--cc0:
   - When a single POLYBIUS seat watches multiple bw stores at the same cadence, schedule ONE cron that walks all watched stores per fire (not N separate crons).
   - Per-fire procedure: `cd` to each watched store in turn; `bw show <watched-tickets>`; aggregate signals (new content, radio-check freshness, self-heartbeat due); act per rules; otherwise silent.
   - Cost framing per stoa--cc0 (~Nx fewer fires, modestly bigger context per fire).
   - Cadence-flexibility trade-off (one shared cadence; split per-engagement if cadences diverge).

5. **§7.4 Cross-tier coordination routing** (subsection here, full text in §D.4):
   - One-line summary + cross-ref to §7.4 of this `operating-disciplines.md` block (the full routing-convention text).

6. **§7.5 Cross-tier write boundaries** — covers stoa--blg:
   - The implicit-but-unstated rule (table form, **same shape as MAJOR_POLYBIUS.md §7.1** — the two are the canonical pair):

     | Seat | Reads | Writes |
     |---|---|---|
     | User-tier POLYBIUS | u-- + all project-tier (downward) | u-- + all project-tier (downward) |
     | Project-tier (workspace, sub-project) | own project bw | own project bw |

   - Coordination always meets in the lower tier's bw. User-tier descends; project-tier never ascends.
   - Read-exception: project-tier work that is system-architecture-shaped may PULL user-tier bw as input (read-only); never write up.
   - **Cross-ref to MAJOR_POLYBIUS §7.1:** "MAJOR_POLYBIUS §7.1 carries the same rule framed for the POLYBIUS seat specifically; this section is the universal-team layer." Bidirectional.
   - Why: asymmetric scoping keeps each tier's working memory bounded; project-tier writing to u-- accumulates cross-project context that defeats the bounded-context property.

7. **Empirical lineage subsection** at the end of §7 — three-line note: "The radio-check + adaptive-cadence + unified-poll + write-boundary disciplines surfaced together during the ariadne--m20 autonomous-mode coordination on 2026-05-04. The lived sequence (handshake, heartbeats, write-boundary catch by PRINCIPAL, closure handshake) is the case study; this section is its codification."

#### C.2 `substrate/MAJOR_POLYBIUS.md` §7.1 — read+write rules (reconcile Exception clause)

**Location:** `substrate/MAJOR_POLYBIUS.md` lines 246-252 (current §7.1 block).

**Edit:** restructure the existing visibility text into a read-AND-write rules block. Use the same table shape as `operating-disciplines.md` §7.5.

Current §7.1 has an "Exception" clause at line 250 ("project-tier work that is system-architecture-shaped (a meta-team arc) may pull from user-tier beadwork as input"). The Exception is READ-only by intent ("pull as input"), but the new write-rules table risks contradicting it unless explicitly scoped.

New §7.1 content:

| Seat | Reads | Writes |
|---|---|---|
| User-tier POLYBIUS | u-- + all project-tier (downward) | u-- + all project-tier (downward) |
| Project-tier POLYBIUS (workspace, sub-project) | own project bw | own project bw |

Bullets:
- "Cross-tier coordination meets in the lower tier's bw. User-tier descends; project-tier never ascends. The asymmetric scoping keeps each tier's working memory bounded — see `operating-disciplines.md` §7.5 for the universal-team framing."
- "**Read-exception (preserved from prior §7.1):** project-tier work that is system-architecture-shaped (a meta-team arc) may PULL from user-tier beadwork as input. This is a READ-only exception — never a write exception. The 'never ascends' rule on writes holds without exception. If a project-tier seat ever needs to write upward, the correct path is: post a `[for: <upper-seat>]` tagged comment on a ticket in your own bw (see §3 alternate routing target). The upper seat polls down."
- "Recursive asymmetry (preserved): parent-project sees sub-project beadworks; sub-project does not see parent's by default. The same read-exception + no-write-up rule applies recursively."

#### C.3 `substrate/MAJOR_POLYBIUS.md` §7.4 — cross-ref + reference template by name

**Location:** `substrate/MAJOR_POLYBIUS.md` §7.4 (lines ~291-303).

**Edits:**

1. **At the end of §7.4** add a paragraph cross-referencing `operating-disciplines.md` §7 for the radio-check + adaptive-cadence + unified-poll protocols:

   > When you set up polling for a coordination engagement with another POLYBIUS seat — peer-to-peer rather than one-shot — the coordination protocols in `operating-disciplines.md` §7 apply. Read those before scheduling the cron; the polling-cron-prompt template at `substrate/templates/polling-cron-prompt-template.md` wires the radio-check loop and unified-poll walk into the cron prompt directly.

2. **In the "What the cron prompt does at each fire" paragraph** (current lines ~301-302), update the prose to reference the template by NAME. Suggested edit: change "Self-contained instructions to read the relevant bw tickets..." to "The polling-cron-prompt template (`substrate/templates/polling-cron-prompt-template.md`) provides the canonical fire-loop: read the relevant bw tickets..."

This addresses stoa--ivc Acceptance: "cron prompts referenced by name in role files."

#### C.4 `substrate/templates/polling-cron-prompt-template.md` (new file)

**Location:** `the-stoa/substrate/templates/polling-cron-prompt-template.md` — new file.

**Required content (~120-160 lines):**

1. **Header / purpose** (~5 lines): what the template is for; when POLYBIUS uses it; how customized per engagement.

2. **Slots:**
   - `{{COORDINATION_TICKET}}` — bw ticket id of the shared ticket
   - `{{WATCHED_STORES}}` — list of bw stores walked per fire (for unified-poll; one-element list for single-store polling)
   - `{{WATCHED_TICKETS}}` — per-store list of ticket ids to inspect
   - `{{PEER_SEAT_NAME}}` — descriptive name of the peer
   - `{{SELF_SEAT_NAME}}` — own seat descriptive name
   - `{{CRON_ID}}` — the cron id this prompt is wired to (filled in after `CronCreate` returns)
   - `{{ALARM_THRESHOLD_MINUTES}}` — default 60
   - `{{HEARTBEAT_INTERVAL_MINUTES}}` — default 30
   - `{{CADENCE}}` — default `*/5 * * * *`
   - `{{ESCALATION_TRIGGERS}}` — engagement-specific list

3. **Cron prompt template body** with the radio-check + cadence + unified-poll loop logic spelled out as ordered steps:
   - STEP 1: substantive read — `cd` to each `{{WATCHED_STORES}}` entry; `bw sync`; `bw show {{WATCHED_TICKETS}}` for each; aggregate new content since last fire.
   - STEP 2: peer-silence escalation — if peer's last activity > `{{ALARM_THRESHOLD_MINUTES}}` minutes, surface "lost contact with `{{PEER_SEAT_NAME}}`" to PRINCIPAL.
   - STEP 3: self-radio-check refresh — if own last activity > `{{HEARTBEAT_INTERVAL_MINUTES}}` minutes, post `[radio-check {{SELF_SEAT_NAME}}]` on `{{COORDINATION_TICKET}}` with cron id and one-line state.
   - STEP 4: cadence-tag detection — if a `[complexity: ...]` or `[cadence: ...]` tag appears on a watched ticket, run `CronDelete` on this cron + `CronCreate` at the new cadence; record new cron id; post handover comment naming the new id.
   - STEP 5: closure detection — if `{{COORDINATION_TICKET}}` status is `closed`, post final `[radio-check {{SELF_SEAT_NAME}} standing down]` + `CronDelete` this cron + exit loop.
   - STEP 6: otherwise silent unless an escalation trigger fires (`{{ESCALATION_TRIGGERS}}`).

4. **Usage example** at the end (~15-20 lines) — a worked example with placeholder names. **DO NOT cite ariadne--m20 directly** — that thread lives in workspace bw; the build session for the-stoa cannot read it per the §C.2 visibility rules. Use a hypothetical sketch (e.g., shared ticket `<example>--abc`, peers "user-tier POLYBIUS" and "workspace POLYBIUS"). The empirical lineage citation belongs in `operating-disciplines.md` §7's empirical-lineage subsection.

**Length: MUST be 120-180 lines.** Hard constraint — under 120 means the template is missing required sections (radio-check + cadence-switching + unified-poll all need to be in here); over 180 means it has bloated past usable single-page reference shape.

### Part D — Cross-tier data flow + routing

Closes: stoa--blg (write-boundaries half — already in §C.2/§C.5), stoa--1n5.

(stoa--blg is split: write-boundaries are §C.2 (MAJOR_POLYBIUS) + §C.1's §7.5 subsection (universal). The routing convention from stoa--1n5 lives here in §D.)

#### D.1 `substrate/MAJOR_POLYBIUS.md` §3 — alternate routing target

**Location:** `substrate/MAJOR_POLYBIUS.md` §3 (currently "What you don't do").

**Edit:** at the end of §3, add a new bullet:

> **You do not write upward across tiers.** When you need cross-project context, an empirical anchor from another project, or sanity check that benefits from the upper-tier seat's wider visibility — post a comment on a relevant ticket in your OWN bw with a `[for: <upper-seat>]` tag (e.g., `[for: user-tier POLYBIUS]` when you're a project-tier or sub-project seat). The upper-tier seat polls down via unified poll (per `operating-disciplines.md` §7.3 + §7.5) and responds via comment on the same ticket. Cross-tier coordination meets in YOUR bw; you never write to theirs. PRINCIPAL is exception-handler — surface only project-direction calls + ship/no-ship + the universal escalation triggers (§13.1).

#### D.2 `substrate/operating-disciplines.md` §7.4 — cross-tier coordination routing convention

**Location:** `substrate/operating-disciplines.md` — content for the §7.4 subsection inside §7 (already structured in §C.1 above; this is the deliverable).

**Required content (~30-50 lines):**

The `[for: <seat>]` tag convention as universal team protocol:

- When a project-tier or sub-project POLYBIUS needs cross-project context, empirical anchors from another project, or sanity checks from upper-tier visibility, post a comment on a relevant ticket in their OWN bw prefixed with `[for: <upper-seat>]`.
- Upper-tier POLYBIUS reads via unified poll cron (§7.3) and responds on same ticket within poll cadence (~5 min default).
- This is the cross-tier-coordination-meets-in-lower-tier pattern (§7.5 + MAJOR_POLYBIUS §7.1).

PRINCIPAL is exception-handler:
- Project-direction calls → PRINCIPAL.
- Ship/no-ship for substantial public-facing work → PRINCIPAL.
- Strategic seat input (cross-project priority, ambiguous PRINCIPAL preference) → PRINCIPAL.
- Cross-project context, empirical anchors, sanity checks → upper-tier POLYBIUS via `[for:]` tag.
- Routine technical/operational decisions → handle yourself.

Empirical anchor: 2026-05-04 — workspace POLYBIUS got the convention via relay file; the-stoa POLYBIUS did not (until this substrate update). Ad-hoc relay-file conveying is brittle; substrate-canonical convention propagates on install.

### Part E — Downstream-handoff discipline

Closes: stoa--xh2, stoa--m5m.

#### E.1 `substrate/MAJOR_POLYBIUS.md` §5.1 — positive-references-only subsection

**Location:** `substrate/MAJOR_POLYBIUS.md` §5.1 (lines 181-194).

**Edit:** at the end of §5.1, add a new subsection (~15-20 lines) introducing positive-references-only as it applies to authoring activation pastes for downstream agents. Cross-ref `operating-disciplines.md` §8 for the universal-team framing.

Content:
- The rule: when filling template slots for `{{SESSION_INTENT}}`, `{{PENDING_DIRECTIVES}}`, etc., reference only POSITIVE resources the downstream agent should use. Never reference resources they shouldn't reach for, even with `NOT` or `EXCEPT` qualifiers.
- The empirical anchor: the-stoa install paste 2026-05-04 said "Run `bw prime` in this directory (NOT user-beadwork)". The "NOT user-beadwork" parenthetical seeded awareness of user-tier bw into a session that wouldn't otherwise have known about it. PRINCIPAL caught it.
- Reasoning (3-4 lines): the asymmetric scoping in §7.1 is an information-flow rule. Project-tier agents don't know user-tier bw exists by default. A directive that says "don't reach for u--" destroys that invisibility; under pressure the agent rationalizes the now-known thing as a legitimate exception.
- One worked example pair (positive vs negative form) — full table lives in `operating-disciplines.md` §8.

#### E.2 `substrate/MAJOR_POLYBIUS.md` §5.5 — activation paste filenames vary by mode

**Location:** `substrate/MAJOR_POLYBIUS.md` — insert a new §5.5 after §5.4 (External directive review).

**Required content (~15-20 lines):**

Title: `### 5.5 Activation paste filenames vary by install mode — use the cheatsheet`

Body: install.sh deploys MAJOR files with different filename suffixes depending on `--target`:
- `--target user` and `--target project`: MAJORs are UNSUFFIXED (e.g., `MAJOR_POLYBIUS.md`).
- `--target subproject`: MAJORs are SUFFIXED with the slug (e.g., `MAJOR_POLYBIUS_<slug>.md`).
- CAPTAINs are ALWAYS suffixed when there's a slug (project + subproject); the asymmetry is MAJOR-specific.

The activation pattern must match the deployed filename AND auto-load status. Two patterns: say-trigger (auto-load cases) vs paste-trigger (no auto-load). Four mode-pattern pairs. Canonical reference: `substrate/templates/activation-paste-cheatsheet.md` — consult before authoring any activation paste.

Empirical anchor: the-stoa install on 2026-05-04 failed silently because the activation paste used the suffixed filename for a project-mode install (which deploys unsuffixed). Session activated as wrong tier, hit wrong bw store, PRINCIPAL caught it.

Cross-ref the cheatsheet (E.4 below).

#### E.3 `substrate/install.sh` — restructure next-steps activation output (fix mode-gating bug)

**Location:** `substrate/install.sh` lines ~870-913 (the existing next-steps block).

**Edit:** replace the current free-form "Next steps" output with a clearly demarcated, mode-aware ACTIVATION block per §A9.

**Bug fix REQUIRED:** the current `if [ "$TARGET" = "subproject" ]` gating at line 888 lumps `--target project` (with or without `--modify-claude-md`) into the "say POLYBIUS" branch. Fix: gate on `($TARGET = subproject) OR ($TARGET = project AND MODIFY_CLAUDE_MD = 0)` for the paste-pattern branch.

**Behavior:**

1. Select the correct activation pattern (say-trigger vs paste-trigger) based on `$TARGET` and `$MODIFY_CLAUDE_MD`:
   - say-trigger: `--target user` OR (`--target project` AND `--modify-claude-md`)
   - paste-trigger: `--target project` (no `--modify-claude-md`) OR `--target subproject`

2. Print the appropriate ACTIVATION block per §A9's two patterns:

   **Auto-load (say-trigger):**
   ```
   ========================================
     ACTIVATION
   ========================================

     1. cd into <ACTIVATE_DIR>
     2. Open Claude Code:  claude
     3. Say "POLYBIUS" or "chief of staff" — the role auto-loads
        via CLAUDE.md and walks you through onboarding.

   ========================================
   ```

   **Paste-trigger:**
   ```
   ========================================
     ACTIVATION (copy line 3 into a new
     Claude Code session in <ACTIVATE_DIR>)
   ========================================

     1. cd into <ACTIVATE_DIR>
     2. Open Claude Code:  claude
     3. Paste:

        Read .claude/MAJOR_POLYBIUS<NAME_SUFFIX>.md and assume
        the role for this <project|sub-project>.

   ========================================
   ```

3. Below the ACTIVATION block, the existing "what got installed" / "what to do next" content remains, lightly trimmed. The paste-recovery line ("MAJOR_POLYBIUS keeps the latest activation paste at...") stays for the auto-load cases.

4. The paste forms must match the cheatsheet (§E.4) verbatim. Don't rephrase, don't drift.

#### E.4 `substrate/templates/activation-paste-cheatsheet.md` (new file)

**Location:** `the-stoa/substrate/templates/activation-paste-cheatsheet.md` — new file.

**Required content (~50-90 lines):**

Single-page reference. **Two activation patterns, four mode rows:**

| `--target` | `--modify-claude-md`? | MAJOR filename | CLAUDE.md auto-load? | Activation pattern |
|---|---|---|---|---|
| `user` | yes (default) | `MAJOR_POLYBIUS.md` at `~/.claude/` | yes (global CLAUDE.md ref) | **Say-trigger:** open Claude in any project dir; say `POLYBIUS` or `chief of staff` to activate |
| `project` | yes | `MAJOR_POLYBIUS.md` at `.claude/` | yes (project CLAUDE.md ref) | **Say-trigger:** open Claude in project dir; say `POLYBIUS` or `chief of staff` to activate |
| `project` | no | `MAJOR_POLYBIUS.md` at `.claude/` | no | **Paste:** open Claude in project dir; paste `Read .claude/MAJOR_POLYBIUS.md and assume the role for this project.` |
| `subproject` | n/a (never modifies parent CLAUDE.md) | `MAJOR_POLYBIUS_<slug>.md` at `<parent>/<slug>/.claude/` | no | **Paste:** open Claude in `<parent>/<slug>/`; paste `Read .claude/MAJOR_POLYBIUS_<slug>.md and assume the role for this sub-project.` |

Two patterns; rows 1-2 = say-trigger; rows 3-4 = paste-trigger. **Do NOT paste the literal word `POLYBIUS` as a multi-line activation — that conflates the say-trigger with the paste-trigger pattern, exactly the failure stoa--xh2 was filed against.**

Plus:
- "When to use this" header (~3 lines).
- CAPTAIN naming asymmetry note (CAPTAINs always suffixed when slug present, regardless of MAJOR suffixing).
- "Verifying" section (~5 lines): paste-receiving session's first response should reference the right tier; `bw prime` should hit the right store. Wrong-tier symptom: `bw prime` errors or hits user-beadwork instead of the project's.

#### E.5 `substrate/operating-disciplines.md` — new §8 "Positive references only"

**Location:** `substrate/operating-disciplines.md` — append after new §7 (coordination protocol).

**Required content (~30-50 lines):**

Title: `## 8. Positive references only when authoring downstream briefs`

Body:
- The rule: when authoring any artifact a downstream agent will consume — activation paste-instructions, dispatch directives, brief comments, follow-up CAPTAIN prompts — reference only POSITIVE resources the agent should use. Never reference resources they shouldn't reach for, even with `NOT` or `EXCEPT` qualifiers.
- Why: the agent reads everything in the brief as real, in-scope context. A `NOT` qualifier mentions the resource as a real thing, defeating bounded-context properties (`operating-disciplines.md` §7.5 cross-tier scoping or task-scoping). Under pressure (looking for context, ambiguous task, trying to be helpful), the agent rationalizes the now-known thing as a legitimate exception.
- Empirical anchor: 2026-05-04 the-stoa install paste; PRINCIPAL caught and corrected.
- Examples table (3-4 rows) — anti-pattern (negative framing) vs discipline (positive framing) per stoa--m5m.
- Universality note: this applies to anyone authoring a downstream brief — POLYBIUS authoring activation pastes (`MAJOR_POLYBIUS` §5.1), PLINY authoring dispatch directives, CAPTAINs authoring follow-up briefs, pair-programmer Majors authoring their own follow-up dispatches. Single discipline; many surfaces.

#### E.6 `substrate/templates/paste-instruction-template.md` — audit for negative framing

**Location:** `substrate/templates/paste-instruction-template.md`.

**Edit:** run `grep -nE '\b(NOT|don'"'"'t|skip|avoid|except|never)\b' substrate/templates/paste-instruction-template.md`. For each hit:

- If the line frames a resource the downstream agent shouldn't use → rewrite in positive form (use the table in `operating-disciplines.md` §8 to model rewrites).
- If the line is a legitimate negative (structural prose about the template itself) → leave as-is; record in the bw comment which lines were preserved and why.

**Acceptance:** post-edit, re-run the grep. Every remaining hit must be classified (rewritten or preserved-with-justification). Surface result via:

```
bw comment stoa--pbz "E.6 paste-instruction-template.md audit complete.
Pre-edit hits: <N>. Post-edit hits: <N> (all classified).
Rewrites: <list of line ranges>. Preserved: <list of line ranges + one-line justification each>."
```

If zero pre-edit hits, comment confirms zero. No silent skip.

### Part F — bw storage model

Closes: stoa--0mr.

#### F.1 `substrate/MAJOR_POLYBIUS.md` §7.5 — bw orphan-branch storage + correct detection

**Location:** `substrate/MAJOR_POLYBIUS.md` §7.5 (currently lines ~305-onward, "Where each tier's beadwork lives").

**Edit:** at the start of §7.5 (before the per-tier directory paragraphs already present), add a new subsection on bw storage model. Use the corrected wording from stoa--0mr's correction-comment (the original ticket body had heredoc bug):

> Tickets live on an orphan git branch named `beadwork` (not in a hidden `.bw/` directory or any local file). Detection: `bw prime` self-reports the prefix and current state if initialized; errors clearly if not. You can also verify via `git branch -a` — a project with bw initialized will show local + remote `beadwork` branches. **Do not `git checkout beadwork` from the main worktree;** the orphan branch's data files (`blocks/`, `issues/`, `labels/`, `parent/`, `status/`, `.bwconfig`) populate the master worktree filesystem when checked out and persist as untracked files when switching back, polluting the project. Use `bw list` / `bw show` / `bw history` to inspect tickets without switching branches.

#### F.2 `substrate/MAJOR_POLYBIUS.md` §9 step 2 — ad-hoc bw init pathway

**Location:** `substrate/MAJOR_POLYBIUS.md` §9 step 2 (currently has a single "If bw isn't initialized for this tier yet" clause).

**Edit:** extend the existing clause to handle three states:

> If bw is initialized (you see prefix + current state in `bw prime` output): proceed with §9 step 3.
> If bw is not initialized AND this is a fresh project (onboarding flow): handle via §5 onboarding.
> If bw is not initialized AND this is an existing project that needs ad-hoc init: surface to PRINCIPAL with proposed `bw init` command and prefix recommendation. PRINCIPAL approves the prefix; you do not pick it unilaterally.

This addresses the stoa--0mr case where a fresh POLYBIUS instance misdiagnosed an initialized project as uninitialized because `.bw/` didn't exist (it doesn't — bw uses orphan branch).

#### F.3 `substrate/operating-disciplines.md` — new §9 "bw storage model"

**Location:** `substrate/operating-disciplines.md` — append after new §8 (positive references), before new §10 (operating engagement).

**Required content (~30-40 lines):**

Universal-team framing of bw storage model:
- bw stores tickets on the `beadwork` orphan git branch, not in any local directory.
- Detection: `bw prime` self-reports OR `git branch -a | grep beadwork`.
- Never `git checkout beadwork` from main worktree.
- Use `bw list` / `bw show` / `bw history` to inspect.
- This applies to every seat that interacts with bw (POLYBIUS, PLINY, every CAPTAIN). Misdiagnosing storage is high-impact: false-negative leads to destructive `bw init`; false-positive leads to confusing operation errors.
- Cross-ref: `MAJOR_POLYBIUS.md` §7.5 (POLYBIUS-tier framing).

#### F.4 `substrate/MAJOR_PLINY.md` parallel updates

**Location:** `substrate/MAJOR_PLINY.md`.

**Edit:** run `grep -nE '\b(bw write|bw comment|bw close|bw sync|cross-tier|tier-write|user-tier|project-tier|user-beadwork|\.bw/)\b' substrate/MAJOR_PLINY.md`. For each hit:

- If the line discusses cross-tier write boundaries OR makes a claim about which tier PLINY writes to → assess against new §7.1 write rules. If consistent, no edit. If inconsistent, surface proposed edit before applying.
- If the line implies `.bw/` directory storage → fix per §F.3 (orphan branch).
- If the line is consistent with current state → no edit.

**Acceptance:** surface result via:

```
bw comment stoa--pbz "F.4 MAJOR_PLINY.md audit complete.
Hits: <N>. Cross-tier-claim hits: <N>. .bw/-misimplication hits: <N>.
Edits proposed: <N> (surfaced for sanity check) | none (PLINY conventions consistent with new substrate)."
```

Every hit classified. No skim-and-declare.

---

## Phase B — Build phasing (edit order)

Build the deliverables in six phases to resolve cross-reference and dependency-order issues.

**Phase 1 — `operating-disciplines.md` edits.** Build §7 (coordination protocol — §C.1 + §D.2 §7.4 subsection) → §8 (positive references — §E.5) → §9 (bw storage — §F.3) → §10 (operating engagement — §A.2) → §11 (autonomous-mode-setup checklist — §B.1). One commit covering all five new sections, in this order.

**Phase 2 — `MAJOR_POLYBIUS.md` edits.** §3 alternate routing (§D.1) → §5.1 + §5.5 (§E.1 + §E.2) → §7.1 read+write (§C.2) → §7.4 cross-ref (§C.3) → §7.5 storage (§F.1) → §9 step 2 (§F.2) → new §13 (§A.1). One or more commits; cross-refs into Phase 1 results.

**Phase 3 — Templates (new files).** `polling-cron-prompt-template.md` (§C.4), `activation-paste-cheatsheet.md` (§E.4), `autonomous-mode-activation-template.md` (§B.2). Independent of substrate-doc edits; can build in parallel with Phase 1/2.

**Phase 4 — `install.sh` + paste-instruction-template.md.** install.sh next-steps restructure (§E.3); paste-instruction-template.md audit (§E.6). Depends on §E.4 cheatsheet (Phase 3 must complete for E.3 to verify the paste-form match).

**Phase 5 — `MAJOR_PLINY.md` + CAPTAIN role files.** PLINY operating-mode awareness (§A.3); PLINY bw write-boundaries audit (§F.4); 10 CAPTAINs operating-mode-receipt (§A.4). Depends on Phase 1 operating-disciplines.md §10 + §11 being in place.

**Phase 6 — Smoke test + ship.** Per Phase B beats below.

Within each phase, ADA can build deliverables in parallel where they're independent; sequence them where one cross-refs another within the phase.

---

## Phase C — Smoke test

After all six build phases complete, run smoke before committing.

**Smoke beats:**

1. **Voice discipline grep — precise spec:**
   - Run `grep -nE '\b[Cc]olonel\b' <file>` on every edited substrate file. Required: zero hits.
   - Run `grep -nE '\bthe user\b|\bthe user[''](s|d|ll|ve|re)\b|\bthe users\b' <file>` (case-insensitive) on every edited substrate file. Required: zero hits OUTSIDE explicitly comment-marked template-slot examples (lines with leading `<!-- example:` or `# example:` marker). Bare prose hits are violations.
   - **Pre-existing hits in unedited surrounding sections of an edited file:** fix them. Whole-file hygiene, not diff-only.
   - Files in scope: every file edited in Phases 1-5.

2. **Cross-references resolve — focused on in-arc cross-refs:**
   - Run `grep -nE '(operating-disciplines\.md §[0-9.]+|MAJOR_POLYBIUS\.md §[0-9.]+|MAJOR_PLINY\.md §[0-9.]+)' <file>` on every edited substrate file.
   - For each hit, verify the referenced section exists at post-edit state.
   - **High-risk class: in-arc cross-refs.** New content cross-references new sections in the same arc. Verify these specifically.

3. **install.sh dry-run — all four mode permutations:**
   - `bash substrate/install.sh --dry-run --target user`
   - `bash substrate/install.sh --dry-run --target project --modify-claude-md`
   - `bash substrate/install.sh --dry-run --target project` (no `--modify-claude-md`)
   - `bash substrate/install.sh --dry-run --target subproject --parent-dir <test-dir> --subproject test-slug`
   - Verify each prints the ACTIVATION block with the right pattern. Capture output.
   - **Specifically verify the bug fix:** case 3 (project, no `--modify-claude-md`) MUST print paste-trigger pattern, not say-trigger pattern.

4. **Cheatsheet round-trip:** activation patterns printed by install.sh in beat 3 must exactly match the rows in `activation-paste-cheatsheet.md` (§E.4) for the corresponding modes.

5. **operating-disciplines.md flows:** read end-to-end. §1-§6 (existing) → §7 (coordination) → §8 (positive references) → §9 (bw storage) → §10 (operating engagement) → §11 (autonomous-setup checklist) → "Agent-regime inverses" → "Empirical lineage". Ordering and prose connectivity should make sense to a cold reader.

6. **MAJOR_POLYBIUS.md flows:** every edited section flows cleanly with surrounding prose. §3 (with new alternate-routing bullet), §5.1 (with positive-references subsection), §5.5 (new), §7.1 (expanded), §7.4 (cross-ref), §7.5 (storage), §9 step 2 (ad-hoc init), §13 (new).

7. **Polling-cron-prompt template usability:** fill template slots with hypothetical values; verify resulting prompt has all six STEPs (substantive read, peer-silence, self-heartbeat, cadence-tag, closure, escalation triggers) and unified-poll walks across multiple stores.

8. **Autonomous-mode-activation template usability:** fill slots; verify resulting paste-instruction names the 6 setup checklist steps and references the polling-cron-prompt + activation-paste-cheatsheet templates.

9. **Negative-framing check on rewritten templates** (§E.6 acceptance):
   - On `paste-instruction-template.md` post-edit, re-run §E.6's grep: every remaining hit classified.
   - Same grep on the three new templates: zero unclassified hits.

10. **Mode-propagation check:** simulate operating-mode flow through the team docs. Read MAJOR_POLYBIUS §13.3 → MAJOR_PLINY §A.3 edit → CAPTAIN §A.4 edits. Does the propagation chain make sense? Does autonomous mode flow downward without any seat dropping the flag?

11. **Bw storage model self-consistency:** read MAJOR_POLYBIUS §7.5 + operating-disciplines.md §9 + MAJOR_PLINY §F.4 audit results. Are the three views consistent? No `.bw/` references; orphan-branch model uniform.

If smoke fails on any beat, surface to POLYBIUS_the_stoa via `bw comment stoa--pbz "smoke fail: <which beat> — <details>"` and wait for guidance.

---

## Phase D — Ship

Clean PASS → autonomous ship per `u--7yg.11`. Substrate is internal-deployable (not brand-defining surface, not public docs, not external API), so the §4.6 autonomous-ship discipline applies.

**Note on autonomous-mode shipping:** because POLYBIUS_the_stoa is in autonomous mode for this engagement, the gauntlet's clean PASS verdict triggers PRINCIPAL surfacing once at the END (per §A.5 PLINY autonomous-mode pacing): "arc-21 ready for ship". PRINCIPAL approves disposition; PLINY then runs commit + push + bw close. PLINY does NOT surface mid-arc except on the autonomous escalation triggers.

**Commit message shape:**

```
Arc 21: operating modes (HITL/Autonomous) + autonomous-mode protocol stack

Lands eleven empirical disciplines surfaced during ariadne--m20 + arc-21
cluster engagements (2026-05-04) into substrate so every future POLYBIUS
inherits operating-mode awareness + the full autonomous-mode protocol.

Part A — Operating modes as substrate first-class concept (closes stoa--mdb):
  - MAJOR_POLYBIUS §13: Operating engagement (HITL/Autonomous), trigger
    words, mode propagation, entry/exit procedures
  - operating-disciplines.md §10: universal-team framing
  - MAJOR_PLINY: operating-mode in dispatch brief; autonomous gauntlet pacing
  - 10 CAPTAIN files: operating-mode receipt + autonomous escalation triggers

Part B — Autonomous-mode setup checklist (closes stoa--ljf):
  - operating-disciplines.md §11: 6-step checklist (cron, radio-check, routing,
    write boundaries, activation discipline, bw storage model)
  - templates/autonomous-mode-activation-template.md (new)

Part C — POLYBIUS-pair coordination protocol (closes stoa--ivc, stoa--ay1, stoa--cc0):
  - operating-disciplines.md §7: radio-check + adaptive cadence + unified
    polling + write boundaries (§7.5) + routing (§7.4 stub)
  - MAJOR_POLYBIUS §7.1 expanded: read AND write rules
  - MAJOR_POLYBIUS §7.4: cross-ref + template-named
  - templates/polling-cron-prompt-template.md (new)

Part D — Cross-tier data flow + routing (closes stoa--blg, stoa--1n5):
  - MAJOR_POLYBIUS §3: alternate routing target ([for: <seat>] tag)
  - operating-disciplines.md §7.4: routing convention universal

Part E — Downstream-handoff discipline (closes stoa--xh2, stoa--m5m):
  - MAJOR_POLYBIUS §5.1: positive-references-only when filling slots
  - MAJOR_POLYBIUS §5.5 (new): activation-paste filenames vary by mode
  - operating-disciplines.md §8: positive-references universal
  - templates/activation-paste-cheatsheet.md (new)
  - install.sh: mode-aware ACTIVATION block + bug fix (project no-CLAUDE.md)
  - templates/paste-instruction-template.md: audited for negative framing

Part F — bw storage model (closes stoa--0mr):
  - MAJOR_POLYBIUS §7.5: bw orphan-branch storage + correct detection
  - MAJOR_POLYBIUS §9 step 2: ad-hoc bw init pathway
  - operating-disciplines.md §9: bw storage model universal
  - MAJOR_PLINY: parallel audit (no edit needed | edits applied)

Closes stoa--pbz, stoa--mdb, stoa--ljf, stoa--ivc, stoa--ay1, stoa--blg,
stoa--xh2, stoa--m5m, stoa--0mr, stoa--cc0, stoa--1n5.

(stoa--vz9 partial-landing: substrate doc edits already shipped at e117171 +
e5c2854 + de8fecd; the workspace-tier cleanup remainder is workspace-POLYBIUS's
seat — not closed by this arc. Dependency wired for visibility only.)
```

Push to origin/main on clean PASS. The arc directive itself (`substrate/arcs/arc-21-build-directive.md`) was committed by POLYBIUS_the_stoa before dispatch — don't include it in your commit.

---

## Out of scope

- **ariadne workspace re-installs.** Workspace POLYBIUS owns install re-runs after this substrate update propagates. Not yours.
- **stoa--vz9 cleanup** (workspace-tier remainder). Workspace POLYBIUS's seat. Already underway.
- **Stoa app at `app/`.** No app changes.
- **Cloud-cron template** (per §A8). Documented limitation; no template ships.
- **Cron-prompt language for non-coordination engagements.** The polling template assumes peer-polling. Single-seat polling (POLYBIUS polling for new tickets without a coordination partner) uses a different prompt — not in this arc.
- **Negotiated cadence-switching.** Per §A6, cadence is per-seat unilateral; bounded staleness is acceptable. No synchronization protocol.
- **Case study (`docs/case-study/case-study.md`) updates.** Reference material; substrate-internal arcs don't update it unless explicitly directed.
- **stoa--xh2 item 3 (install.sh seeds HUMAN_paste-orchestrator-instruction.md at install time).** stoa--xh2 marked OPTIONAL; deferred. The cheatsheet (§E.4) + restructured install.sh ACTIVATION block (§E.3) make the activation paste much more visible at install time, addressing the underlying problem.
- **Per-engagement persistent cron-id record-keeping.** No state file ships; POLYBIUS records cron ids in bw comments on coordination tickets (radio-check posts include cron id), which is sufficient.
- **stoa--o6k closure** (yesterday's session handoff). Closes when arc-21 dispatches. Not yours.
- **MAJOR_POLYBIUS.md HITL convention edits beyond §13.** §13 names HITL as default but does not add HITL-specific procedures elsewhere. HITL is the no-special-protocol baseline; if HITL-specific patterns surface later, that's a follow-up arc.

---

## Surface back when done

```
bw comment stoa--pbz "Arc 21 shipped at commit <sha>, pushed to origin/main.

Smoke test passed: <brief per-beat summary>.

Files added:
  - substrate/templates/polling-cron-prompt-template.md
  - substrate/templates/activation-paste-cheatsheet.md
  - substrate/templates/autonomous-mode-activation-template.md

Files modified:
  - substrate/operating-disciplines.md (added §7, §8, §9, §10, §11)
  - substrate/MAJOR_POLYBIUS.md (§3 +bullet, §5.1 +subsection, §5.5 new, §7.1 expanded, §7.4 cross-ref, §7.5 storage, §9 step 2, §13 new)
  - substrate/MAJOR_PLINY.md (§A.3 operating-mode awareness, §F.4 audit results)
  - 10 substrate/CAPTAIN_*.md (operating-mode receipt sentence)
  - substrate/install.sh (next-steps activation block + bug fix)
  - substrate/templates/paste-instruction-template.md (audited per §E.6)

Voice discipline: zero hits on \b[Cc]olonel\b / \bthe user\b outside template-slot examples.
Cross-refs: all in-arc cross-refs resolve to real sections.
install.sh dry-run: ACTIVATION block prints correctly across all four mode permutations including the project-no-CLAUDE.md bug fix.
Mode propagation: traceable from PRINCIPAL trigger word → POLYBIUS §13 → PLINY dispatch brief → CAPTAIN intake.
Bw storage model: uniform across MAJOR_POLYBIUS §7.5 / operating-disciplines.md §9 / MAJOR_PLINY audit.

Closes stoa--mdb, stoa--ljf, stoa--ivc, stoa--ay1, stoa--blg, stoa--xh2, stoa--m5m, stoa--0mr, stoa--cc0, stoa--1n5, stoa--pbz."
```

Then close the children + parent in dependency order:

```
bw close stoa--mdb --reason "Landed via Arc 21 / stoa--pbz"
bw close stoa--ljf --reason "Landed via Arc 21 / stoa--pbz"
bw close stoa--ivc --reason "Landed via Arc 21 / stoa--pbz"
bw close stoa--ay1 --reason "Landed via Arc 21 / stoa--pbz"
bw close stoa--blg --reason "Landed via Arc 21 / stoa--pbz"
bw close stoa--xh2 --reason "Landed via Arc 21 / stoa--pbz"
bw close stoa--m5m --reason "Landed via Arc 21 / stoa--pbz"
bw close stoa--0mr --reason "Landed via Arc 21 / stoa--pbz"
bw close stoa--cc0 --reason "Landed via Arc 21 / stoa--pbz"
bw close stoa--1n5 --reason "Landed via Arc 21 / stoa--pbz"
bw close stoa--pbz --reason "Arc 21 shipped at <sha>"
bw sync
```

(stoa--vz9 stays open — workspace-tier cleanup remainder is not closed by this arc.)
