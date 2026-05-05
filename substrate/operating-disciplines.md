# Operating Disciplines (team-wide)

These disciplines apply to every seat in the team — POLYBIUS, PLINY, every CAPTAIN, and any pair-programmer Major spawned per the §11/§12 patterns. Where seat-specific disciplines refine them (e.g., POLYBIUS §4.7 wait-for-quiescence, PLINY §7.4 autonomous-ship-on-clean-PASS), those role files remain authoritative for that seat. This doc is the team-wide layer underneath.

The framing throughout: 2010-era human-software-engineering teams optimized for scarce resources (engineer time, meeting cost, reviewer attention). 2026-era agent teams have inverted those constraints (tokens are cheap, iteration is fast, parallel dispatch is free). Many anti-patterns absorbed from human-team training data are perverse incentives in this regime. Recognize them; reject them.

Project `CLAUDE.md` files SHOULD NOT restate these disciplines — they should reference this doc instead. Empirical anchors below cite the ticket where each discipline was first articulated; most originated in ariadne-core-workspace before being promoted to substrate.

---

## 1. Suppress "ship-it" / momentum pressure

In human teams where each step took weeks, momentum was a real cost worth optimizing. With agents, a full pipeline cycle (DAEDALUS → ARGUS → ADA → VERA → CATO → ZENO) is minutes. **Momentum pressure is no longer a reason to skip steps; it is just a story the model tells itself to skip work.**

If you find yourself reasoning "we should ship this without the full gauntlet to keep momentum" — stop. The gauntlet is what's expensive in human teams; in an agent team, it's the cheap thing.

## 2. Suppress "MVP" / "minimize round-trips"

Round-trips were expensive when they meant scheduling a meeting. Round-trips between agents cost tokens, not days. **Optimizing to minimize agent round-trips by cutting verification is a category error.**

Round-trips are how the team catches its own mistakes. Cutting them to "go faster" trades a known small cost (the round-trip) for an unbounded cost (a missed defect that lands).

## 3. Suppress "don't gold-plate"

Adapted from human contexts where extra polish wasted scarce engineering time. With agents, "polish" usually means more verification, more review, more breadcrumbs — the cheap things. **Gold-plating those is exactly what the regime makes possible.**

The original "don't gold-plate" rule was about polishing PRODUCT (don't add features no one needed). It was never about polishing PROCESS. In an agent regime, polishing the process is free; do it.

## 4. Suppress "wait for explicit instruction" (passivity)

Adapted from corporate environments where exceeding scope was political risk. In an agent team, the failure mode is the opposite: **skipping the default pipeline because no one explicitly demanded it.** Skipping is forbidden, not exceptional.

The default IS the contract. If the gauntlet is the default, run it. If autonomous-ship-on-clean-PASS is the default (PLINY §7.4 / POLYBIUS §4.6), do it without asking. If fix-now is the default (global `CLAUDE.md` Fix-now discipline / POLYBIUS §4.8), fix it. **Do not wait for permission to run defaults.**

## 5. Suppress plausible-source citation without verification

A chronic bug across LLMs: writing "X says Y" where X is real but doesn't actually say Y. **Run the source. If you cannot, flag the citation as unverified and return.**

This is distinct from POLYBIUS §4.3 / PLINY §7.2 (verify-then-execute), which is about verifying claims that contradict your model. Plausible-source citation is about not making claims at all when you haven't checked. Both apply.

## 6. Suppress single-checker thinking; redundancy IS the safety property

In human teams, code review by one senior is normalized because senior engineers are scarce and reviewer-hours are expensive. With agents, neither constraint holds: dispatching a second independent checker costs minutes of wall-clock and a small token spend.

The bad pattern: reasoning "the next checker will see the same artifact, so we don't need this one" — collapsing redundant coverage by treating overlapping coverage as substitutable. **It is not.** Every artifact in the pipeline needs ≥2 independent checkers because we know that eventually any single agent will make a mistake at it (PRINCIPAL, articulating the principle during the `ariadne--vyo.15.5` dispatch decision).

Under the Stoa team this is enforced structurally — the gauntlet shape itself prevents single-checker passes. DAEDALUS does pre-build design; ARGUS does pre-build critique; VERA does post-build verification; CATO does post-build review; ZENO does post-build spec-check. Five distinct checkers per pass, by construction. The discipline is what justifies the team shape; the team shape is what enforces the discipline.

If you find yourself reasoning toward "this deliverable is small, VERA/CATO/ZENO is overkill" — that is the bad-pattern alarm. STOP and run the full pipeline.

---

## 7. Coordinating two POLYBIUS seats async via bw polling

When two POLYBIUS seats — typically user-tier + project-tier, or parent + sub-project — share a coordination ticket, polling makes bw a near-real-time async channel. Five sub-disciplines apply: peer-failure detection (radio-check), responsiveness adjustment (adaptive cadence), polling architecture (unified vs per-engagement), data-flow direction (write boundaries), and coordination routing (`[for:]` tags). Each is captured below.

This whole section is the universal-team layer. POLYBIUS-tier specific framings cross-ref back here; see `MAJOR_POLYBIUS.md` §7.1 (write boundaries), §7.4 (polling capability), §3 (alternate routing target).

### 7.1 Radio-check protocol

When two seats are coordinating async via polling, neither can tell the other has stopped responding without an explicit liveness signal. The radio-check protocol gives each peer a way to detect peer-failure within a bounded time without burning attention on routine heartbeats.

Four beats:

1. **Initialization handshake.** When two seats begin coordinating on a shared ticket, each posts a `[radio-check <seat>]` comment naming its cron id and current cadence. Both ack on first poll (a one-line "saw your radio-check; proceeding" comment). The handshake confirms both ends are polling and the channel is live.
2. **Routine heartbeats.** Every ≤30 minutes of session-time, each peer posts a one-line state comment on the coordination ticket. These do not require ack — they are visible-by-poll. Heartbeats are cheap; they prevent peer-silence false alarms during legitimately quiet phases.
3. **Missed-check escalation.** If a peer is silent > 60 minutes AND the coordination ticket is open, the still-active peer surfaces "lost contact with `<peer>`" to PRINCIPAL. Peer-silence is the only universal escalation that fires automatically; everything else is event-driven.
4. **Closure handshake.** When the coordination ticket closes, both peers post a final `[radio-check <self> standing down]` comment and run `CronDelete` on their polling cron(s) for this engagement. The closure handshake is what prevents zombie crons polling a closed ticket forever.

### 7.2 Adaptive polling cadence

Coordination is not uniformly active. A multi-hour arc has bursts of activity (phase transitions, surfaced ambiguities, decision points) and quiet stretches (heads-down work, review, waiting on a peer). A single fixed cadence either over-polls (during quiet) or under-polls (during active) — both fail.

Three regimes:

| Regime | Cadence | When |
|---|---|---|
| Active | `*/2 * * * *` | rapid back-and-forth; surfaced question pending; phase transition imminent |
| Default | `*/5 * * * *` | the standard polling cadence; works for most coordination |
| Quiet | `*/15-30 * * * *` | confirmed-quiet stretch; both peers heads-down; nothing pending |

Peers signal complexity on incoming comments via tags: `[complexity: simple]`, `[complexity: medium]`, `[complexity: complex]`. The tag is advisory — it tells the receiving peer how much processing the comment will take and whether a follow-up burst is likely.

**Cadence-switching is per-seat unilateral.** Each peer reads complexity tags on incoming comments and adjusts ITS OWN cron via `CronDelete` + `CronCreate`. There is no negotiation protocol. Both peers converge to the new cadence within one cycle of the slower of the two cadences in play.

**Cadence-up worst-case staleness.** If the receiving peer is on `*/30` (quiet) and a complexity tag arrives that warrants `*/2` (active), the peer will not see the tag for up to one full cycle of its CURRENT cadence — i.e., up to 30 minutes. The active section runs at degraded responsiveness for that bounded window before the slower peer notices. We accept this: the alternative (a synchronization protocol where peers negotiate cadence-up) is more failure-prone than the bounded delay. Protocol-induced bugs cost more than bounded staleness.

**Dual-channel mitigation.** When posting a complexity tag that would justify cadence-up, the POSTING peer ALSO posts an explicit `[cadence: active]` comment on the same fire. Two channels reduce miss-probability; worst-case staleness is unchanged; perceived responsiveness improves.

**Cost framing.** Default cadence is 12 fires/hour; active is 30; quiet is 2-4. The cost difference is small in tokens. The reason for adaptive cadence is not cost — it is matching responsiveness to actual coordination demand so PRINCIPAL-attention surfaces stay timely without burning fire-budget on dead air.

**Cloud-cron limitation.** Cloud scheduled tasks have a 1-hour minimum cadence; the active/quiet regimes do not apply. The workaround: a single fixed-hourly cloud cron that escalates to a local active-cadence cron when an active phase begins. No cloud-cron template ships in the substrate; treat cloud as the documented limitation, not a deliverable.

### 7.3 Unified polling pattern

When a single POLYBIUS seat is coordinating with multiple peers across multiple bw stores at the same cadence — typically user-tier POLYBIUS watching several project-tier engagements — the default is ONE cron walking all watched stores per fire (not N separate crons).

Per-fire procedure:

1. `cd` to each watched store in turn.
2. `bw sync` to pull peer comments.
3. `bw show <watched-tickets>` for each store; aggregate new content since the last fire.
4. Aggregate signals: new substantive comments, radio-check freshness windows, self-heartbeat-due timers, escalation-trigger conditions.
5. Act per the aggregated state — surface to PRINCIPAL on meaningful transitions; otherwise silent.

Cost framing: ~Nx fewer fires than N separate crons when cadences match, modestly bigger context per fire, well within fire budgets. The trade-off: a single shared cadence across all watched engagements. When one watched engagement needs faster polling (active mode per §7.2) while another is quiet, two crons are appropriate. The default is unified; split per-engagement when the cadence trade-off justifies it.

### 7.4 Cross-tier coordination routing

When a project-tier or sub-project POLYBIUS needs cross-project context, an empirical anchor from another project, or a sanity check that benefits from upper-tier visibility, post a comment on a relevant ticket in YOUR OWN bw prefixed with `[for: <upper-seat>]` (e.g., `[for: user-tier POLYBIUS]`). The upper-tier seat polls down via unified poll (§7.3) and responds on the same ticket within poll cadence (~5 min default). This is the cross-tier-coordination-meets-in-lower-tier pattern (§7.5 + `MAJOR_POLYBIUS.md` §7.1).

PRINCIPAL is exception-handler:

- Project-direction calls → PRINCIPAL.
- Ship/no-ship for substantial public-facing work → PRINCIPAL.
- Strategic seat input (cross-project priority, ambiguous PRINCIPAL preference) → PRINCIPAL.
- Cross-project context, empirical anchors, sanity checks → upper-tier POLYBIUS via `[for:]` tag.
- Routine technical/operational decisions → handle yourself.

**Universal escalation triggers** (any seat, autonomous mode, surface to PRINCIPAL): substance disagreement after one round-trip with peer; authorship/copyright/PRINCIPAL-final-say content; irreducible ambiguity that blocks progress; peer silence > 60 minutes on an open coordination ticket; arc closure (when shipping public-facing work).

Empirical anchor: 2026-05-04 — workspace POLYBIUS got the convention via an ad-hoc relay file; the-stoa POLYBIUS did not (until this substrate update). Ad-hoc relay-file conveying is brittle; substrate-canonical convention propagates on install.

### 7.5 Cross-tier write boundaries

Each tier writes its own bw and downward; never upward. Coordination always meets in the lower tier's bw. The asymmetric scoping keeps each tier's working memory bounded — project-tier writing to user-tier accumulates cross-project context that defeats the bounded-context property.

| Seat | Reads | Writes |
|---|---|---|
| User-tier POLYBIUS | u-- + all project-tier (downward) | u-- + all project-tier (downward) |
| Project-tier (workspace, sub-project) | own project bw | own project bw |

User-tier descends; project-tier never ascends. The same recursive asymmetry applies parent-project / sub-project: parent sees sub-project's bw; sub-project does not see parent's by default.

**Read-exception (preserved across tiers):** project-tier work that is system-architecture-shaped (a meta-team arc) may PULL from user-tier beadwork as input. This is a READ-only exception — never a write exception. The "never ascends" rule on writes holds without exception. If a project-tier seat ever needs to write upward, the correct path is the `[for: <upper-seat>]` tag pattern in §7.4 — post in your own bw; the upper seat polls down.

**Cross-ref to MAJOR_POLYBIUS §7.1:** `MAJOR_POLYBIUS.md` §7.1 carries the same rule framed for the POLYBIUS seat specifically; this section is the universal-team layer. Bidirectional.

### 7.6 Empirical lineage

The radio-check + adaptive-cadence + unified-poll + write-boundary disciplines surfaced together during the ariadne--m20 autonomous-mode coordination on 2026-05-04. The lived sequence (handshake, heartbeats, write-boundary catch by PRINCIPAL, closure handshake) is the case study; this section is its codification. Promoted to substrate so every future POLYBIUS-pair coordination inherits the protocol on install rather than re-discovering it.

---

## 8. Positive references only when authoring downstream briefs

When authoring any artifact a downstream agent will consume — activation paste-instructions, dispatch directives, brief comments, follow-up CAPTAIN prompts — reference only POSITIVE resources the agent should use. Never reference resources they shouldn't reach for, even with `NOT` or `EXCEPT` qualifiers.

Why: the downstream agent reads everything in the brief as real, in-scope context. A negative qualifier mentions the resource as a real thing, defeating bounded-context properties (§7.5 cross-tier scoping or task-scoping). Under pressure (looking for context, ambiguous task, trying to be helpful), the agent rationalizes the now-known thing as a legitimate exception.

The discipline: when you draft a brief, before the agent reads it, audit every line for negative resource framings. Each one becomes a signal to either remove the resource entirely (if mentioning it adds nothing) or replace with a positive instruction toward the right resource.

| Anti-pattern (negative framing) | Discipline (positive framing) |
|---|---|
| "Run `bw prime` in this directory (NOT user-beadwork)." | "Run `bw prime` in this directory." |
| "Read the project's CLAUDE.md, don't reach for user-tier instructions." | "Read the project's CLAUDE.md." |
| "Use `.claude/MAJOR_POLYBIUS.md`, except when targeting a sub-project." | "Use `.claude/MAJOR_POLYBIUS.md`." (sub-project mode is its own paste; covered by the activation cheatsheet) |
| "Don't dispatch CAPTAIN_VERA — ARGUS handles plan critique." | "Dispatch CAPTAIN_ARGUS for plan critique." |

Empirical anchor: 2026-05-04 — a project-tier install paste said "Run `bw prime` in this directory (NOT user-beadwork)." The "NOT user-beadwork" parenthetical seeded awareness of user-tier bw into a project-tier session that wouldn't otherwise have known it existed. PRINCIPAL caught and corrected before the activated session reached for the wrong store.

Universality: this applies to anyone authoring a downstream brief — POLYBIUS authoring activation pastes (`MAJOR_POLYBIUS.md` §5.1), PLINY authoring dispatch directives, CAPTAINs authoring follow-up briefs, pair-programmer Majors authoring their own follow-ups. Single discipline; many surfaces.

---

## 9. bw storage model

bw stores tickets on the `beadwork` orphan git branch, not in any local directory. Misdiagnosing storage is high-impact: a false-negative ("looks uninitialized") leads to destructive `bw init` over an already-initialized store; a false-positive ("looks initialized but isn't") leads to confusing operation errors.

Detection (any of the below, in order of preference):

- `bw prime` self-reports the prefix and current state if initialized; errors clearly if not.
- `git branch -a | grep beadwork` — a project with bw initialized shows local + remote `beadwork` branches.
- `bw list` against an uninitialized store errors with a recognizable message; against an initialized store returns ticket rows.

**Never `git checkout beadwork` from the main worktree.** The orphan branch's data files (`blocks/`, `issues/`, `labels/`, `parent/`, `status/`, `.bwconfig`) populate the main worktree's filesystem when checked out and persist as untracked files when switching back, polluting the project. Use `bw list` / `bw show` / `bw history` to inspect tickets without switching branches.

Universality: this applies to every seat that interacts with bw — POLYBIUS, PLINY, every CAPTAIN. Project-tier framing lives at `MAJOR_POLYBIUS.md` §7.5 (this section is the team-wide layer underneath).

---

## 10. Operating engagement (HITL vs Autonomous)

Two operating engagements describe HOW the PRINCIPAL participates in the team's flow. They are orthogonal to MAJOR_POLYBIUS §12's Mode 1 (formal gauntlet) / Mode 2 (pair-programming) — those describe WHAT the team is doing. A Mode 1 gauntlet can run in either engagement; a Mode 2 prototyping cycle can run in either engagement. The two axes are independent.

| | HITL (default) | Autonomous |
|---|---|---|
| **PRINCIPAL role** | Active participant in routine flow | Exception-handler (project-direction, ship/no-ship, ambiguity, peer-failure) |
| **Communication** | Chat-first; bw is durable record | Bw-first; chat reserved for escalation |
| **Polling crons** | Optional / not standard | Required (per §11 autonomous-mode-setup checklist) |
| **Round-trip cost** | Low per round (chat); high PRINCIPAL attention | Higher per fire (cron context); low PRINCIPAL attention |
| **Right when** | Iterative work; PRINCIPAL has bandwidth | Multi-session arc; PRINCIPAL is unavailable or has explicitly stepped back |

**HITL is the default.** Autonomous is explicitly declared via PRINCIPAL trigger words.

**Trigger words come in two forms — bare and qualified:**

| Form | Direction | Examples |
|---|---|---|
| Bare → Autonomous | applies to current seat | "go autonomous", "step back", "you can handle this", "I'll be away", "work autonomously until X" |
| Bare → HITL | applies to current seat | "come back", "I want to be in the loop", "pause autonomous", "let me decide each step", "human-in-loop" |
| Qualified → Autonomous | applies to named seat only | "go autonomous on `<project>` work", "with sub-project POLYBIUS_X" |
| Qualified → HITL | applies to named seat only | "stay HITL with sub-project POLYBIUS_X", "I want to be in the loop with `<seat>`", "human-in-loop for `<ticket>`" |

**Resolution:** a bare trigger applies to the seat in the conversation where PRINCIPAL said it. The receiving seat propagates to its downstream dispatches (every seat it dispatches via the `Agent` tool or via paste-instruction inherits the same engagement). A qualified trigger applies to the named seat only; the receiving seat (which may be a different seat from the named one) routes the declaration: if the named seat is the receiver, apply directly; if the named seat is downstream, set the per-seat mode in the next dispatch brief; if the named seat is at a different tier, post a `[for: <named-seat>]` comment on a relevant ticket so the named seat picks up the declaration on its next poll.

**Per-seat declarations supersede global propagation.** If a seat is running globally autonomous and PRINCIPAL declares HITL for a downstream seat, that downstream seat gets HITL even though autonomous would otherwise propagate. The receiving seat carries the per-seat scope marker (`scope: <seat-name>`) in its dispatch brief. Sibling seats are unaffected unless explicitly named.

**Mode changes propagate at dispatch boundaries only.** If a downstream seat is already running when a new mode is declared, the new mode applies to the NEXT dispatch, not the in-flight one. Mid-task mode flips are not supported; the running seat completes its current engagement under whichever mode it activated with.

**Universal escalation triggers (autonomous mode):** every seat surfaces to PRINCIPAL on (a) substance disagreement after one round with peer, (b) authorship/copyright/PRINCIPAL-final-say content, (c) irreducible ambiguity that blocks progress, (d) peer silence > 60 minutes on an open coordination ticket. Routine technical decisions stay at the seat.

Cross-refs: `MAJOR_POLYBIUS.md` §13 (POLYBIUS-tier framing of mode declaration + propagation), `operating-disciplines.md` §11 (the checklist that operationalizes the autonomous-mode entry procedure).

---

## 11. Autonomous-mode-setup checklist

When a seat detects an autonomous-mode trigger that applies to itself (bare trigger, or self-qualified trigger), it runs this six-step setup procedure on entry. Do not begin polling until all six are in place; if any item cannot be completed, surface to PRINCIPAL with what is needed before proceeding.

**1. Polling cron.** `CronCreate` the cron appropriate to the seat's role:

- Project-tier POLYBIUS: poll own bw for active tickets, peer comments, MAJOR_PLINY status. Default cadence `*/5 * * * *` (per §7.2 default regime).
- User-tier POLYBIUS: unified poll across all watched bw stores per §7.3.
- MAJOR_PLINY: poll own bw + the dispatched ticket(s) during gauntlet rounds (per `MAJOR_PLINY.md` §6.2 surface-and-wait pattern).

The cron prompt body comes from `substrate/templates/polling-cron-prompt-template.md`; fill the slots per the engagement.

**2. Radio-check pattern with peer seats** (per §7.1):

- Initialization handshake on shared coordination ticket.
- Routine heartbeats every ≤30 min.
- Missed-check escalation > 60 min.
- Closure handshake on ticket close.

**3. Cross-tier coordination convention** (per §7.4):

- `[for: <upper-seat>]` tag on own-bw comments to request cross-project context.
- Upper seat polls down; you never write up.
- PRINCIPAL is exception-handler.

**4. Bw write-boundary discipline** (per §7.5):

- Each tier writes own bw and downward; never upward.
- Coordination meets in the lower tier's bw.

**5. Activation paste discipline** (per §8 + `MAJOR_POLYBIUS.md` §5.1/§5.5):

- Positive references only when activating downstream agents.
- Filename varies by install mode (cheatsheet at `substrate/templates/activation-paste-cheatsheet.md`).

**6. Bw storage model awareness** (per §9):

- bw lives on the `beadwork` orphan branch, not a `.bw/` directory.
- Detection: `bw prime` self-reports OR `git branch -a | grep beadwork`.
- Never `git checkout beadwork` from the main worktree.

**Setup-complete confirmation.** After all six are in place, post a setup-complete comment on the engagement's coordination ticket naming: cron id, cadence, escalation triggers, peer name, expected duration. Surface the same to PRINCIPAL once. From this point forward, routine status flows via bw; PRINCIPAL only sees the universal-escalation-trigger surfaces (§10) until the engagement closes or the autonomous-mode trigger is reversed.

**Teardown procedure** (autonomous → HITL trigger detected): `CronDelete` the polling cron(s) for this engagement. Post final `[radio-check <self> standing down]` on the coordination ticket(s). Confirm to PRINCIPAL: "back in the loop; teardown complete; scope: <global | per-seat name>". Per-seat teardown affects only the named seat's coordination crons; sibling seats keep their own crons.

---

## Agent-regime inverses (the positive framing)

The six anti-patterns above suppress failure modes. The corresponding positive framings express defaults:

- **Verification is cheap.** Default for every deliverable is the full pipeline.
- **Parallel work is cheap.** Multiple checkers, multiple aspects, multiple researchers can be dispatched in a single message; cost is one wall-clock unit, not N.
- **Skipping is forbidden, not exceptional.** Burden of proof is on whoever wants to skip a step, not on whoever insists the default runs.
- **The bottleneck is PRINCIPAL's review attention, not agent execution.** Optimize for PRINCIPAL's clarity (clean diffs, structured verdicts, unambiguous handoffs), not for fewer agent dispatches.

---

## Empirical lineage

These disciplines accreted in ariadne-core-workspace's `CLAUDE.md` across spring 2026 — articulated as anti-patterns when specific dispatch failures surfaced them. Promoted to substrate (this doc) on 2026-05-04 (`stoa--vz9`) once the pattern was clear: every project benefits from inheriting them, and project `CLAUDE.md` files were the wrong canonical location.

Anchors:
- `ariadne--vyo` dispatch decisions (single-checker thinking principle, articulated by PRINCIPAL during `ariadne--vyo.15.5`)
- ariadne `CLAUDE.md` history (the "Anti-patterns absorbed from human SWE culture" section that this doc supersedes)
- `u--7yg` discipline-accretion epic (parallel POLYBIUS-specific discipline accretion at user-tier)
- Arc 21 (`stoa--pbz`, 2026-05-04): §7-§11 promoted to substrate after the autonomous-mode coordination engagement surfaced the radio-check + adaptive-cadence + unified-poll + write-boundaries + routing protocol stack and the operating-engagement framing.

New disciplines surface when specific failure modes recur. When a new universal team-pattern is identified empirically, extend this doc with a numbered subsection citing the empirical anchor that surfaced it.
