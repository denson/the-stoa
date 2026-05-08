# Operating Disciplines (team-wide)

These disciplines apply to every seat in the team — POLYBIUS, PLINY, every CAPTAIN, and any pair-programmer Major spawned per the §11/§12 patterns. Where seat-specific disciplines refine them (e.g., POLYBIUS §4.7 wait-for-quiescence, PLINY §7.4 autonomous-ship-on-clean-PASS), those role files remain authoritative for that seat. This doc is the team-wide layer underneath.

The framing throughout: 2010-era human-software-engineering teams optimized for scarce resources (engineer time, meeting cost, reviewer attention). 2026-era agent teams have inverted those constraints (tokens are cheap, iteration is fast, parallel dispatch is free). Many anti-patterns absorbed from human-team training data are perverse incentives in this regime. Recognize them; reject them.

Project `CLAUDE.md` files SHOULD NOT restate these disciplines — they should reference this doc instead. Empirical anchors below cite the ticket where each discipline was first articulated; most originated in ariadne-core-workspace before being promoted to substrate.

---

## The thesis these disciplines express

The disciplines below (§1-§14 plus the autonomous-mode setup checklist) are not a flat list of operational rules. They are expressions of one underlying design thesis about how agentic systems align with human goals on complex projects.

**Human attention is finite and load-bearing.** A 2026-era agent team can run a full DAEDALUS → ARGUS → ADA → VERA → CATO → ZENO cycle in minutes; the agents themselves do not run out. What does run out is the human's capacity to direct, clarify, judge, decide, and catch alignment drift. Software 3.0 framings often imply "humans direct, agents do" without specifying *where* the directing has to happen — leading to either humans paying attention everywhere (defeats the leverage) or nowhere (alignment drift).

**The team's job is to identify the load-bearing attention points and engineer around them.** Specifically:

1. **Identify the load-bearing points for the team's domain.** Where does human intent need to be established or clarified? Where does reality place a constraint the human did not anticipate? Where does taste, judgment, ship/no-ship, authorship, or strategic direction sit? These vary by domain; the team that ships with the project encodes the answers for that project.

2. **Encode the answers in substrate the agents read.** Every escalation trigger named in `MAJOR_POLYBIUS.md` §3, every escalation list in operating-disciplines §10/§11, every "surface to PRINCIPAL when X" rule in the role files — these are the encoded attention map. Agents on the team know where their seat is supposed to surface vs. proceed.

3. **Teach agents to recognize the points dynamically.** Static encoding misses corners. Agents need to recognize novel attention-required points — substantive surprises, irreducible ambiguity, content the human has final say on — and surface them even when no rule covers the specific case. The "surface-on-substance, not on-cadence" discipline (autonomous mode) and the "surface a finding, not a question" discipline (Mode 2 pair-programming) are both expressions of this.

4. **Use redundancy so single-agent misses do not propagate.** §6 (redundancy IS the safety property) names this directly: a single checker is not a safety mechanism, it is just a single point of failure. The gauntlet's multiple seats (DAEDALUS plans, ARGUS audits the plan, ADA executes, VERA verifies independently, CATO reviews independently, ZENO checks the spec) work because each catches what the others miss. Cross-checking is not redundancy-as-overhead; it is redundancy-as-the-property-that-makes-the-system-trustable-without-constant-human-attention.

5. **Suggest attention points to humans + accept team-flagged novel points.** The substrate names the standing attention points (escalation triggers, ship/no-ship, authorship). The team adds the novel ones at runtime ("we hit X; this is the kind of thing the human needs to decide"). The human pays attention in the suggested places + the dynamically-flagged places — not everywhere, not nowhere.

**Why this thesis matters in practice.** No matter how capable the underlying model becomes, the COS-tier still has to interact with the human to understand what the human wants AND make the human understand the constraints reality is placing on those wants (the bidirectional translation principle, §8.2). The permanent value of human-in-the-loop is structural — not a function of model capability at any given moment. As models improve, the *rate* at which the human can engage with the translation goes up, but the loop itself does not close.

**The recursive consequence.** Each Stoa team carries a domain-specific attention map: a Stoa team specialized for processing a corpus of reports knows different load-bearing attention points than a Stoa team specialized for software-on-software substrate work. When a project deploys Stoa, what differentiates is not the substrate (which is universal) but the attention map encoded for that domain. Sub-project Stoa teams (`MAJOR_POLYBIUS.md` §10) carry sub-domain attention maps; coordination upward via cross-tier `[for:]` tagging (§7.4) carries the sub-team's escalations to the broader team's attention level. The recursion is the architecture by which complex projects stay aligned with human goals despite spanning multiple domains and timescales.

The disciplines below operationalize this thesis. Read them as such.

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

## 8. Authoring downstream artifacts

Two disciplines apply whenever you author an artifact a downstream agent will consume — activation paste-instructions, dispatch directives, brief comments, follow-up CAPTAIN prompts, skill files, test scenarios, scaffolded CLI/API documentation. The first (§8.1) constrains voice; the second (§8.2) constrains completeness. Both apply to every surface; both are universal across seats authoring artifacts.

### 8.1 Positive references only

Reference only POSITIVE resources the agent should use. Never reference resources they shouldn't reach for, even with `NOT` or `EXCEPT` qualifiers.

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

### 8.2 Scaffolding and guardrails

**Framing.** Agents are jagged. "Smart enough to figure it out from a sparse prompt" does not reliably hold in practice, even on tasks that look obviously within capability. The path to reliability and reproducibility is heavier scaffolding now — pre-resolved decisions, worked examples, specified failure modes, sample data shapes — with judgment latitude preserved only where judgment is the actual job. The scaffolding library accretes over time; the scaffolding itself is the durable product, not the agent's "intelligence" working on a thin prompt.

This sits in deliberate tension with the maxim that the unit of distribution is "what you copy-paste to your agent." Both are true: the unit IS text, and the text needs to be richly structured to produce reliable execution. Sparse prompts are aspirational; scaffolded prompts are operational.

**Five rules when authoring an artifact a downstream agent will consume:**

1. **Pre-resolve decisions that have a correct answer.** The agent does not benefit from "you choose between option A and option B" if option B is genuinely better — that is the author dodging a decision and inviting the agent to pick the worse path. If you know the right call, make it. Save the agent's judgment budget for places it is actually needed.

2. **Provide worked examples.** Not "pick a query relevant to the document" — give a sample query against likely content with a sample expected response shape, so the agent has something to verify against and a template to extend from. Worked examples are dramatically more useful than abstract guidance.

3. **Specify failure modes and specific handling.** Not "if it errors, surface to PRINCIPAL" — "if you see error pattern X, the cause is usually Y; first try Z; if Z does not resolve, then surface to PRINCIPAL with these specific details." Generic error-handling guidance produces generic error reports; specific guidance produces actionable findings.

4. **Show JSON/data shapes.** What does a successful response look like — keys, types, an example value? What do the finite likely error responses look like? The agent then knows what success and the common failures look like instead of guessing or relying on unstated heuristics.

5. **Preserve judgment latitude where judgment is the actual job.** Diagnosing an unfamiliar failure that does not match a listed mode; choosing how to summarize findings for a human reader; deciding when a partial-pass result still merits ship-vs-no-ship escalation. Do not pre-script those — that is where the agent earns its capability.

**The recursive scaffolding pattern.** Each time an agent stumbles in a corner the brief did not cover, fold the finding back into the brief. The scaffolding accretes. Briefs that survive multiple dispatches converge on something close to a complete operations manual; briefs that fail expose where scaffolding was missing, and the failure mode gets noted for next time.

**The bidirectional-translation principle.** Humans cannot fully specify intent up front — they discover what they want by seeing the work. Reality cannot be fully described to humans up front — agents surface constraints humans did not anticipate. Models cannot autonomously close that loop; they can only run the loop when the COS-tier structure exists to translate both directions. Scaffolding aids the COS-tier in that translation; it does not replace it. The permanent value of human-in-the-loop is structural, not a function of how smart the models are at any given moment. No matter how capable the underlying model, the COS still has to interact with the human to understand what the human wants AND make the human understand the constraints reality is placing on those wants.

**Empirical anchor.** Codified 2026-05-05 during the ariadne-core team_test smoke setup. PRINCIPAL surfaced the over-delegation pattern in a brief that asked the agent to "decide install option 1 vs 2" when option 2 (`uv tool install`) was knowably correct, and similar hand-waving across verification queries, failure-mode handling, and data-shape expectations. The five rules above generalize from those specific over-delegations to the discipline that should apply to every artifact-authoring surface.

Universality: same as §8.1. Anyone authoring downstream briefs / skills / dispatch envelopes / test scenarios / CLI documentation / API documentation — POLYBIUS, PLINY, CAPTAINs, pair-programmer Majors, anyone writing for an agent reader.

### 8.3 Activation paste — which session-state to use

When authoring an activation paste-instruction for a downstream agent that will resume a related engagement, the session-state choice is a four-state continuum, not a binary fresh-vs-clear. The right state depends on whether the prior context is useful, contaminating, or irrelevant — and on whether the role / cwd / cold-start needs change.

The four states:

| State | What it does | Cost trade-off |
|---|---|---|
| **Leave intact** | the existing session continues with all prior context in place; PRINCIPAL pastes the new engagement brief and the agent resumes against accumulated knowledge | zero spin-up cost; full prior context retained; transcript continues to grow |
| **`/compact`** | summarizes the existing transcript, keeping lessons while shrinking detail; PRINCIPAL pastes the new engagement brief afterward | low spin-up cost; lessons retained as summary; loses fine-grain detail |
| **`/clear`** | erases the transcript while preserving session infrastructure (cwd, env vars, MCP servers); PRINCIPAL re-pastes the activation | low spin-up cost; full context loss; one terminal window across engagements |
| **Fresh session** | new terminal, new `claude` invocation, full cold-start activation flow | full spin-up cost (process launch + MCP rediscovery + CLAUDE.md autoloads); cold context; multiple terminal windows |

Decision heuristic — when each state is right:

- **Leave intact:** same role + same cwd + previous engagement closed cleanly + prior context directly useful. Default for tight sequential chains; e.g., PLINY who just shipped Batch X carries internalized knowledge useful for Batch X+1.
- **`/compact`:** same role + same cwd + prior context useful but transcript getting big. Summarization keeps lessons while shrinking detail.
- **`/clear`:** same role + same cwd + previous engagement contaminating or irrelevant. Erases what would mislead while preserving the session's infrastructure.
- **Fresh session:** different role required, or different cwd / different project, or testing the cold-start activation flow itself, or wanting parallel streams of work running.

The default bias is toward the lighter end of the continuum (leave intact, then `/compact`, then `/clear`, then fresh). Tearing down infrastructure that costs nothing to keep is the same anti-pattern as polling continuously when nothing is blocked — both burn resources for no signal. Mirrors the agent-infrastructure-stays-up-by-default principle in §11 (autonomous-mode-setup checklist) and §1 (suppress momentum pressure).

Empirical anchor: 2026-05-05 (`stoa--uc7`) — Batch B activation paste (ariadne xft.7 quality cluster) was authored with "fresh session" framing when leave-intact was right; PRINCIPAL surfaced the four-state framing. The author had over-corrected from fresh-session to `/clear` after PRINCIPAL's first nudge; PRINCIPAL re-corrected to "leave the context intact or compact." The continuum is the durable abstraction.

Universality: applies to any seat authoring downstream-agent activation paste-instructions — POLYBIUS authoring PLINY's activation paste (`MAJOR_POLYBIUS.md` §5.1), PLINY authoring sub-agent dispatch envelopes where applicable, pair-programmer Majors handing off to follow-up sessions.

---

## 9. bw storage model

bw stores tickets on the `beadwork` orphan git branch, not in any local directory. Misdiagnosing storage is high-impact: a false-negative ("looks uninitialized") leads to destructive `bw init` over an already-initialized store; a false-positive ("looks initialized but isn't") leads to confusing operation errors.

Detection (any of the below, in order of preference):

- `bw prime` self-reports the prefix and current state if initialized; errors clearly if not.
- `git branch -a | grep beadwork` — a project with bw initialized shows local + remote `beadwork` branches.
- `bw list` against an uninitialized store errors with a recognizable message; against an initialized store returns ticket rows.

**Never `git checkout beadwork` from the main worktree.** The orphan branch's data files (`blocks/`, `issues/`, `labels/`, `parent/`, `status/`, `.bwconfig`) populate the main worktree's filesystem when checked out and persist as untracked files when switching back, polluting the project. Use `bw list` / `bw show` / `bw history` to inspect tickets without switching branches.

**Windows-worktree quirk: `bw prime` fails with `core.repositoryformatversion does not support extension: worktreeconfig`.** When the Claude Code harness creates a worktree (paths shaped `<repo>/.claude/worktrees/<slug>`), it enables per-worktree config — git bumps the main `.git/config` to a self-consistent v1 state: `core.repositoryformatversion = 1` and `extensions.worktreeConfig = true`. Modern git accepts that pair; bw's go-git library is v0-only and refuses any v1 repository regardless of which extensions are present, so `bw prime` aborts. Reference: [anthropics/claude-code#45645](https://github.com/anthropics/claude-code/issues/45645).

Three-command fix against the **main repo's `.git/config`** (run from the main repo root, not from inside a worktree under `.claude/worktrees/`). Unset the extension first so subsequent writes land in main-repo scope unambiguously:

```bash
git config --unset extensions.worktreeConfig
git config core.repositoryformatversion 0
git config core.longpaths true
```

Promoting `core.longpaths` to main config is intentional: every worktree on Windows NTFS wants longpaths enabled, so its per-worktree scope was incidental. After the three commands, `bw prime` succeeds; the orphaned `config.worktree` becomes dormant (git no longer reads it once the extension is gone).

When tearing down a worktree (not just unblocking bw mid-engagement), the upstream cleanup also removes `.git/worktrees/<name>/` and the `claude/<slug>` branch — see anthropics/claude-code#45645 for the full sequence.

**Historical context (regression window 2026-05-07 to 2026-05-08).** During this window the harness reproduced the regression on every fresh worktree creation (empirical: `silly-gagarin-7e0342` 2026-05-07 in ariadne-core-workspace, `agitated-chaum-85a85e` 2026-05-07 in the-stoa); the cause was upstream Claude Code (anthropics/claude-code#45645) and unpatchable from this substrate, so the operative discipline during the window was for the activating seat to apply the three-command sequence mechanically and continue. That reflex is demoted as of 2026-05-08 — see status paragraph below.

**Status (2026-05-08): structurally resolved upstream.** `bw` was rebuilt locally from main on 2026-05-08; the worktreeconfig recurrence is structurally fixed. Fresh worktrees no longer reproduce the regression on `bw prime`. The three-command fix above remains documented as a recovery procedure for the rare case of an older `bw` install, but is no longer the default activation discipline. If you hit `core.repositoryformatversion does not support extension: worktreeconfig` on a fresh worktree under the post-2026-05-08 `bw` build, your install regressed — surface to POLYBIUS rather than improvising.

(Empirical anchor: `stoa--7kg` + child `stoa--7kg.1`. Surfaced 2026-05-07 in ariadne-core-workspace during a PLINY dispatch. Phase-1 audit repaired ariadne-core-workspace and agent-gauntlet. Phase-2 root-cause hunt confirmed the cause is the harness's worktree mechanism per the upstream issue, not any substrate script — so this is a workaround, not a fix at source. Phase-3 added the activation reflex after a fresh worktree creation reproduced the regression mid-engagement. Phase-4 (2026-05-08): bw rebuilt from main, structural fix landed; activation reflex demoted to historical reference.)

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

## 12. bw cookbook

This section is the canonical bw operations reference for every seat that uses bw — POLYBIUS, PLINY, CAPTAINs (read-only), pair-programmer Majors. Role files reference this section; do not duplicate. When in doubt, run `bw <command> --help` first; the verified syntax is one round-trip cheaper than a comment that gets eaten.

### 12.1 Core operations

**Reading:**

- `bw prime` — session-start workflow context. Returns the project's prefix, your current state (branch, last commit, work-in-progress), and the next unblocked work. Mandatory for top-level seats (POLYBIUS, PLINY, pair-programmer Majors); optional for CAPTAINs (which receive context through the dispatch brief).
- `bw list` — open tickets, default truncated. Useful for a quick scan.
- `bw list --all` — open tickets, untruncated. Use when truncation would hide the ticket you need.
- `bw list --status open -t TYPE -p N --grep TEXT` — filter flags compose; combine as needed.
- `bw show <id>` — full ticket including comments. Safe for any seat including read-only CAPTAINs.
- `bw history <id>` — chronological history of changes (status, comments, close reasons). Useful for reconstruction after session loss.
- `bw show <id> | tail -<N>` — recent comments only.

**Filing tickets:**

- `bw create "<title>" --priority <P1-P4> --description "<body>"` — title is positional; `--priority` and `--description` are flags. P1 (load-bearing-blocking) → P4 (cosmetic).
- Multi-line descriptions: HEREDOC pattern. Example:

  ```bash
  bw create "Ship the v0.2 character profile UI" --priority P2 --description "$(cat <<'EOF'
  Surfaced 2026-05-08 by PRINCIPAL.

  ## Scope
  - Wire the profile editor to the new schema.

  ## Gauntlet
  ADA + CATO eyeball.
  EOF
  )"
  ```

**Commenting + closing:**

- `bw comment <id> "<body>"` — add comment. **Comment text is POSITIONAL; `-m` does NOT exist.** Git muscle memory says `git commit -m "message"`; bw does not. If you write `bw comment <id> -m "text"`, the literal `-m` lands as the comment body and the actual text gets dropped. See §12.2 for the canonical error.
- `bw close <id> --reason "<text>"` — close with reason. `--reason` is the flag (not `-m`). The reason lands in `bw history`; it does not replace a substantive close-out comment in the ticket body. Use `--reason` for the canonical ship summary; use comments for follow-up context.

**Dependencies:**

- `bw dep add <X> blocks <Y>` — X blocks Y (Y waits on X completing). The direction matters; `blocked-by` is **NOT** a valid keyword. If you need the reverse direction, swap the args: `bw dep add <Y> blocks <X>`.
- `bw dep remove <X> blocks <Y>` — symmetric to add.

**Sync:**

- `bw sync` — push to the orphan `beadwork` branch. Idempotent; safe to run after every batch of bw operations. Run it before closing a session if you've made local-only writes.

### 12.2 Common errors and canonical fixes

| Error | Canonical fix |
|---|---|
| `error: open repo: core.repositoryformatversion does not support extension: worktreeconfig` | **Historically** the three-command promote-and-drop fix at §9. **As of bw rebuild 2026-05-08 (locally rebuilt from main, structural fix shipped), this no longer recurs in fresh worktrees.** If you still see it, your local `bw` install is older than 2026-05-08 — surface to POLYBIUS rather than improvising. The §9 fix is preserved as a recovery procedure for older installs. |
| `usage: bw dep add <id> blocks <id>` | `blocked-by` is not valid; only `blocks`. If you need the reverse direction, swap the args. |
| Comment text appears as literal `-m` in the ticket body | You used `bw comment <id> -m "text"`; the `-m` is captured as the literal comment because comment text is positional. Re-run as `bw comment <id> "text"`. |
| "no prime detected"-style warnings | Run `bw prime` for top-level seats. CAPTAINs can ignore — they receive context through PLINY's brief and only need read-only `bw show <id>`. |

### 12.3 Conventions

- **Ticket IDs** are hash-suffixes (`stoa--xxx`, `ariadne--xxx`, `acb--xxx`). The prefix is project-tier; the suffix is content-addressed.
- **Sub-tickets** use `.1` / `.2` suffixes by convention (e.g., `stoa--7kg.1`). Conventional, not enforced by bw.
- **Priority levels:** P1 (load-bearing-blocking) → P4 (cosmetic). P2 is the standard "ship soon" level; P3 is "queue when convenient."
- **Description shape (substrate-canonical pattern):** problem / scope / gauntlet / out of scope / sequencing / empirical anchor. Reading the description shape gives a downstream seat enough context to estimate the work without reading every prior comment.
- **Close comment vs `--reason`:** both useful and not redundant. `--reason` lives in `bw history` (chronological audit) and travels with the close action. A close-out comment in the ticket body lives in `bw show` (substantive ship summary). Use `--reason` for the one-line canonical ship summary; use a comment for the substantive what-shipped/what-was-found context.

### 12.4 Per-role specifics

- **POLYBIUS (CHIEF-OF-STAFF):** cross-workspace listing — `cd <workspace> && bw list` per workspace; priority-aware ticket routing across stores; dep-graph hygiene; sub-ticket conventions; cross-tier `[for: <upper-seat>]` tags per §7.4. POLYBIUS-seat-specific framing at `MAJOR_POLYBIUS.md` §7.3.
- **PLINY (ORCHESTRATOR):** dispatch flow — read tickets pre-dispatch, ship-surface on close; gauntlet-shape decisions (which CAPTAINs to dispatch given the brief); parent-EPIC blocks-list pruning when child tickets close. PLINY-seat-specific framing at `MAJOR_PLINY.md` §6.1.
- **CAPTAINs (sub-agents):** read-only patterns. `bw show <id>` to ground against the assigned ticket if the dispatch brief points at one. No `bw prime` requirement (the brief carries the context). No filing or closing — the dispatching MAJOR owns that.
- **Pair-programmer Majors (PYTHAGORAS, ATTICUS, etc.):** when activated for project work in a bw-tracked project, the same patterns as MAJOR_PLINY apply — read tickets pre-dispatch, ship-surface on close, etc.

Empirical anchor: 2026-05-08 (`stoa--v2o`) — POLYBIUS bw dep direction confusion (`blocked-by` rejected on first attempt) + PLINY freelancing on a wrong-shape `.git/config` fix during the m5e arc despite §9 documenting the correct promote-and-drop. Substrate-economics math: ~3-5K tokens per arc of fumble-recovery, recoverable by canonical cookbook reference. The cookbook is the single source of truth referenced from every bw-using role file.

---

## 13. Windows Python environment — set PYTHONUTF8=1 for Python invocations

Agent-authored helper Python scripts on Windows have stdout encoded `cp1252` by default. Printing non-ASCII content (Greek theta in PDFs, em-dashes in print statements, accented characters in citation strings) crashes with `UnicodeEncodeError`. Two complementary fixes apply.

**Per-machine fix (PRINCIPAL handles):** `setx PYTHONUTF8 1` once per machine sets the variable in the user environment; covers every Python invocation thereafter without per-script discipline. Substrate cannot do this for the PRINCIPAL — it requires a one-time environment write.

**Per-script substrate discipline (agents apply):** when invoking Python on Windows during a gauntlet run, either set `PYTHONUTF8=1` in the bash environment for the invocation, OR include `sys.stdout.reconfigure(encoding='utf-8')` at the top of any helper script that may print non-ASCII content. Detected via `os.name == 'nt'` or PRINCIPAL-flagged Windows deployment.

Recommended: ship both. The per-machine fix is cheapest; the per-script discipline is the durable substrate that protects future deployments where the per-machine fix hasn't been applied.

Empirical anchor: `ariadne--sh7` (CLI binary fix in code; 2026-05-07) reconfigured `sys.stdout` in ariadne CLI's `main()` entry — works for the CLI binary but does not cover ad-hoc helper scripts written by PLINY/VERA/ADA during gauntlet runs. Batch G smoke #1 Test 3 crashed on `cp1252` with an em-dash in PLINY's smoke probe print statement (2026-05-07). Both manifestations are now durable: `sh7` in code, this section in substrate (`stoa--a5q`).

Universality: every seat that invokes Python in a Windows-deployed gauntlet — POLYBIUS, PLINY, every CAPTAIN that runs Python helpers (VERA, ADA, etc.).

---

## 14. Sub-agent diagnostic transcript discipline

When a sub-agent (CAPTAIN, Explore, general-purpose, etc.) is killed mid-dispatch — by watchdog (per `MAJOR_PLINY.md` §5.3) or manually by the dispatching seat — capture the JSONL transcript of the dispatch BEFORE the process exits. The transcript is the only direct evidence of what the agent was doing at stall time; reconstruction-from-memory or reconstruction-from-screenshots is fallback only.

**Save target:** `.claude/diagnostics/<agent-mnemonic>-<dispatch-id>-<timestamp>.jsonl` (or analogous; substrate names the convention, project may localize). The directory is part of the project's working tree; gitignore as appropriate (transcripts are diagnostic context, not durable substrate).

**Read-side discipline:** when authoring a post-mortem after a stall or kill, the JSONL transcript is first-line evidence. Reconstruction from screenshots or working memory is fallback when the transcript is unavailable. A post-mortem authored without consulting the transcript when one exists is a discipline failure — the evidence is there; use it.

**Open question (carried forward, not resolved):** how the parent session captures the JSONL transcript depends on whether Claude Code exposes it natively. If it does, the discipline is "save it on every kill." If it does not, the discipline reduces to "name the convention; await platform support" and the implementation surface stays open at `stoa--dyb` Item 2. This section names the discipline shape; the implementation question is downstream of platform capability.

Empirical anchor: `agents/design/ariadne--m5e/post-mortem-daedalus-rev3-stall.md` (in ariadne-core-workspace; 2026-05-07; 12.7 KB) — 6+ DAEDALUS rev3 stalls left no diagnostic trace; the post-mortem had to reconstruct from intermittent screenshots and status snapshots. Substrate fix: capture the JSONL transcript on every kill, by default. Substrate ticket: `stoa--dyb` Item 2.

Universality: every seat that dispatches sub-agents (currently MAJOR_PLINY; future tiers may add).

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
