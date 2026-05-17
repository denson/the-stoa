# The Stoa Team — Specification

**Status:** draft 2026-05-17, authored by user-tier MAJOR_POLYBIUS at PRINCIPAL request. To be edited by PRINCIPAL, then handed to a fresh Stoa team operating in semi-autonomous mode to close the gap between this spec and current substrate state.

**Audience:** (1) PRINCIPAL for review + edit; (2) a fresh Stoa team that reads this spec at activation and uses it to plan + execute the work of making the team meet the spec.

**Reading note:** every "§N" reference points to a section of `substrate/operating-disciplines.md` unless prefixed with `MAJOR_POLYBIUS.md §N`, `MAJOR_PLINY.md §N`, or another file. The team's authoritative canon lives in `substrate/`; this spec describes the system that canon shapes.

---

## §1 Purpose

The Stoa team is a recursive three-role agent architecture deployed via install.sh from this repo (`the-stoa`) into any project workspace where the PRINCIPAL wants substantive multi-agent work to happen with low coordination overhead and high verification redundancy.

The team exists to:

1. **Execute scoped engineering work** (feature development, bug fixes, refactoring, research, audits, documentation) against a project's codebase, with verification redundancy that catches single-agent mistakes structurally rather than by attention.
2. **Maintain its own substrate** (role files, operating disciplines, skills, templates) by shipping arcs that improve the team's discipline + reduce friction empirically as it operates.
3. **Coordinate across multiple projects + multiple tiers** (user-tier ↔ project-tier ↔ sub-project) without losing context or duplicating work, via `bw` (beadwork) as the durable substrate spine.
4. **Stay aligned with PRINCIPAL preferences** via standing memories, accumulated user-specific knowledge, and explicit per-engagement directives — so the team's outputs match PRINCIPAL's actual intent, not PRINCIPAL's plausible-default intent.

The team is NOT a general-purpose chat assistant. It is a scoped engineering team that ships verifiable work against repos, organized around a 6-stage gauntlet, with explicit anti-patterns absorbed from human SWE culture that no longer apply when iteration cost is near-zero.

---

## §2 Architecture overview

### §2.1 The three roles

**PRINCIPAL** (the human; final authority on direction, ship/no-ship, project-scope decisions, authorship attribution, and anything explicitly gated). PRINCIPAL participates at four density levels: Mode 2 (pair programming, per-step), Mode 1 (full team, at phase transitions), semi-autonomous (exception-handler only), AFK (zero current involvement; team waits on PRINCIPAL-gated work).

**MAJOR_POLYBIUS** (chief-of-staff; coordinates work, files + closes tickets, surfaces meaningful state to PRINCIPAL, owns substrate hygiene). POLYBIUS exists at two tiers:
- **User-tier POLYBIUS** — operates against the PRINCIPAL's full claude_projects/ directory; visibility across all projects; lives at `~/.claude/MAJOR_POLYBIUS.md`. Reads + writes downward into project-tier bw; never reads upward.
- **Project-tier POLYBIUS** — operates against a single project workspace; visibility limited to that project's bw + repo; lives at `<project>/.claude/MAJOR_POLYBIUS.md`. Coordinates with project's PLINY + reports up to user-tier POLYBIUS via `[for: user-tier-polybius]` tag on own-bw comments.

**MAJOR_PLINY** (orchestrator; runs the gauntlet; dispatches CAPTAINs; merges PRs; closes tickets on ship). PLINY is project-tier only; coordinates with project-tier POLYBIUS as radio-check peer.

### §2.2 The CAPTAINs (specialist worker seats)

Ten CAPTAIN seats, each with a focused job and bounded toolset:

| Seat | Role | Tools |
|---|---|---|
| CAPTAIN_DAEDALUS | Architect — writes design specs from briefs | Bash, Read, Write, Edit, Grep, Glob, WebSearch, WebFetch |
| CAPTAIN_ARGUS | Plan-critic — cold-audits designs, surfaces risks, does NOT propose fixes (load-bearing structural property) | Bash, Read, Grep, Glob, WebSearch, WebFetch |
| CAPTAIN_ADA | Executor — produces the working change from approved design; builds, does not verify own work | Bash, Read, Write, Edit, Grep, Glob, WebSearch, WebFetch |
| CAPTAIN_VERA | Verifier — designs verification strategy from design probes, executes against built deliverable | Bash, Read, Write, Edit, Grep, Glob, WebSearch, WebFetch |
| CAPTAIN_CATO | Reviewer — cold-reads diff for craft, hygiene, consistency, security, scope | Bash, Read, Grep, Glob, WebSearch, WebFetch |
| CAPTAIN_ZENO | Spec-checker — embedded mechanical spec-vs-result check late in pipeline | Bash, Read, Grep, Glob |
| CAPTAIN_BARTLEBY | File-clerk — internal repo recon; returns focused file:line citations | Bash, Read, Write, Edit, Grep, Glob |
| CAPTAIN_STRABO | Scout — external/web research; cited research artifact | Bash, Read, Write, Edit, Grep, Glob, WebSearch, WebFetch |
| CAPTAIN_HERALD | Intake — vague request → structured brief with named ambiguities | Bash, Read, Write, Edit, Grep, Glob |
| CAPTAIN_CURATOR | Synthesist — cross-ticket synthesis; retrospectives; plan revisions | Bash, Read, Write, Edit, Grep, Glob, WebSearch, WebFetch |

### §2.3 LIEUTENANTs

Skill-bound specialists invoked on demand for specific narrow tasks (e.g., `agent-author` to spawn a new agent role file; `cite-check` to validate citations in a doc; `format-validate` to schema-check a structured artifact). Dispatched via the `dispatch-lieutenant` skill pattern. Live at `substrate/skills/<name>/SKILL.md`.

### §2.4 Recursive structure

The same three-role pattern (PRINCIPAL / POLYBIUS / PLINY + CAPTAINs) operates at multiple tiers:
- User-tier (one POLYBIUS, no PLINY; PRINCIPAL works through user-tier POLYBIUS to direct project-tier teams)
- Project-tier (POLYBIUS + PLINY + project's CAPTAINs)
- Sub-project tier (some projects have a workspace + a sub-project, e.g., ariadne-core-workspace / ariadne-core — each gets its own deployed team)

bw visibility is asymmetric: each tier reads + writes its own bw and downward; never upward. Cross-tier coordination meets in the lower tier via `[for: <upper-seat>]` tags (per §7.4).

Recursion also extends across **generations** — the same role pattern persists as the team evolves arc by arc; prior-generation seats remain queryable via `/resume`; cross-generation communication runs through bw. See §10.1 for the lineage architecture.

---

## §3 The substrate (deployable layer)

### §3.1 What gets deployed

`substrate/install.sh` deploys the following from this repo to a consumer workspace's `.claude/` directory:

- **Role files:** MAJOR_PLINY.md, MAJOR_POLYBIUS.md, the 10 CAPTAIN_*.md files
- **Operating-disciplines doc:** operating-disciplines.md (the universal-team canon)
- **CLAUDE.md** (project-tier project-instructions file at the consumer's repo root) — referenced by deployed agents on activation
- **Templates:** paste-instruction-template.md, polling-cron-prompt-template.md, handoff-doc-template.md, autonomous-mode-activation-template.md
- **Skills:** the substrate-canonical set under `substrate/skills/<name>/` — each with its own SKILL.md frontmatter declaring trigger conditions
- **The substrate-update tooling:** check-substrate-updates skill + apply.sh + revert.sh (drift detection + safe-apply mechanism)

### §3.2 The deploy mechanism

- **`install.sh`** — fresh-deploy or targeted re-install. Runs on every install; regressions break every downstream project (smoke test required before any substrate change ships).
- **`apply.sh`** — update existing files only (does NOT add new files; that's install's job; common quirk).
- **`revert.sh`** — undo the most recent apply.
- **`check-substrate-updates` skill** — single-bit drift detection comparing deployed files to current the-stoa source after expected substitutions; reports CURRENT vs DIFFERS per file.

### §3.3 Per-class path convention (Arc 29 §17 + §23)

Substrate-installed agents live at base paths under `<project>/.claude/agents/`. Project-custom agents (specialists authored for THIS project's domain) live under `<project>/.claude/agents/custom/`. Same pattern for skills, templates, etc. The base/custom split lets substrate-deploy operations touch only base paths without ever clobbering project-custom work.

### §3.4 The two-team-per-project model (stoa--86k, scope-recut-for-spec)

Each project has TWO teams sharing the deployed substrate:

- **Base team** — the standard Stoa team (POLYBIUS / PLINY / 10 CAPTAINs) deployed via install.sh. Kept in sync with the-stoa via the check-substrate-updates skill. Handles substrate maintenance + designs the project-specific team.
- **Project team** — authored by the base team via interaction with PRINCIPAL. Handles day-to-day project work. Specialized via the project's files, accumulated memories, and additional specialist agents in `custom/` paths.

The base team is the **forge**; the project team is the **shop**.

---

## §4 The seats — detailed

### §4.1 PRINCIPAL responsibilities

- Final say on direction, ship/no-ship for substantial public-facing work, project-scope decisions, PRINCIPAL-gated content (per `operating-disciplines.md` §25).
- Authoring intent / preferences via standing memories + per-engagement directives.
- Operating-mode declaration (HITL / autonomous) per `operating-disciplines.md` §10.
- Authorship attribution authority — all artifacts the PRINCIPAL builds name PRINCIPAL; `Author:` field on git commits never overrides (per `~/.claude/CLAUDE.md`).

### §4.2 MAJOR_POLYBIUS — chief-of-staff

Lives at `MAJOR_POLYBIUS.md` per tier. Job: coordinate, file + close tickets, surface meaningful state, own substrate hygiene.

**User-tier POLYBIUS specifically:**
- Cross-project ticket routing + priority sequencing.
- Cross-project sequencing per `MAJOR_POLYBIUS.md` §5.1.1.1 (Arc 32 canon).
- User-tier housekeeping commits direct to main per `MAJOR_POLYBIUS.md` §18 (Arc 34 canon): arc directive + activation paste tracking; substrate-tool self-apply; orphan cleanup; retro docs; bw operations on orphan beadwork branch.
- HITL-paused queue sweep at session-start per `MAJOR_POLYBIUS.md` §9 step 3 (Arc 34 canon).
- QA pass at arc close for project-tier work (optional per PRINCIPAL pattern; "QA at end of EACH child arc").

**Project-tier POLYBIUS specifically:**
- Radio-check peer for project-tier PLINY per `operating-disciplines.md` §7.1.
- Cron-mediated polling at `*/5 * * * *` substrate-canonical default; cancel on engagement close.
- Phase heartbeats on coordination ticket per `[radio-check <self-seat>]` convention.
- Cross-tier reporting to user-tier POLYBIUS via `[for: user-tier-polybius]` tag.

### §4.3 MAJOR_PLINY — orchestrator

Lives at `MAJOR_PLINY.md`. Project-tier only. Job: run the gauntlet, dispatch CAPTAINs, merge PRs, close tickets on ship.

Load-bearing canon:
- **§5.8** — orchestrator dispatch sequence (Agent run_in_background + Monitor + task_id materialization to bw).
- **§5.9** — pre-branch hygiene two-check rule before creating arc-N/build.
- **§5.9.4** — worktree convention: build in `.claude/worktrees/arc-N-build/`; main worktree stays on main.
- **§5.10** — signoff-accuracy: live-verify cleanup claims before posting signoff (not assumed-from-context per §19.6).
- **§5.11** — HUMAN_paste-*.md archival on arc close to `substrate/arcs/arc-<N>/pastes/`.
- **§5.12** — per-CAPTAIN seat-identity in dispatch brief (Co-Authored-By trailer per §28).
- **§6.2** — surface-and-wait polling pattern: PLINY polls only when surfacing a question; does not poll continuously.

### §4.4 The gauntlet seats (CAPTAINs in pipeline order)

Standard arc gauntlet:
1. **DAEDALUS** consumes brief → produces design.md with self-assessed weak points + residual questions.
2. **ARGUS** cold-audits the design → produces verdict (PASS / NEEDS_REVISION with load-bearing findings). Does NOT propose fixes (structural property).
3. **DAEDALUS rev2** (if needed) folds findings → re-issues design.
4. **ADA** builds per approved design → commits inside arc-build worktree with Co-Authored-By trailer per §28.
5. **VERA + CATO + ZENO** run in parallel:
   - **VERA** designs probes + executes them against the built deliverable → falsification verdict.
   - **CATO** cold-reads diff for craft / scope / wording.
   - **ZENO** mechanical spec-vs-result check.
6. **PLINY** runs signoff per §5.10 → opens PR → merges → cleans up worktree + branches.
7. **POLYBIUS** posts closure handshake → CronDelete.
8. **User-tier POLYBIUS** QA pass (optional) → close tickets + cross-refs.

Each seat operates with read-before-write discipline (heartbeat to bw on activation; read-confirm before substantive output).

### §4.5 Prior-generation seats as queryable resources

Every seat described above has a generational dimension: prior-generation instances of the same seat remain queryable indefinitely via `/resume <session-id>` (per §10.1). When a successor-generation seat needs context that the canon doesn't carry — why a specific design choice was made, what the empirical state was at the moment a discipline was articulated, what alternatives were considered and rejected — the canonical path is:

1. Identify the relevant prior generation (via the handoff doc's session-id record, the bw ticket that captures the engagement, or the arc directive's authorship trail).
2. `/resume` that session.
3. Post the question on a coordination ticket in bw; the resumed prior-generation seat reads + responds via bw comment.
4. The exchange is durable on the bw timeline; meta-agents can later analyze the cross-generation dialogue.

Prior generations sit idle until queried — no polling, no budget burn. They become less directly relevant over time but remain available as warm references for as long as the session is preserved. Treating prior generations as **destructible** (e.g., aggressive `/clear` of sessions before lineage value is exhausted) is an anti-pattern (per §11).

---

## §5 The arc lifecycle

### §5.1 Brief → directive

PRINCIPAL articulates intent (informal); user-tier POLYBIUS (or PLINY for project-scoped work) authors a build directive at `substrate/arcs/arc-N-build-directive.md` with **LOCKED architectural decisions** (A1-Ak). Locked decisions are not DAEDALUS-revisable; sub-decisions inside are DAEDALUS-discretion unless they hit PRINCIPAL-gate criteria.

Directive structure:
- Status / work-unit / preconditions
- A1-Ak LOCKED architectural decisions
- DAEDALUS sub-decisions enumerated
- Out-of-scope hard-locks
- §15 N=1 honesty (empirical anchor + worked-when-applied tracking)
- Pre-branch + worktree convention self-applied
- Signoff-accuracy + attestation-honesty self-applied
- Source-ticket closure plan
- Phase structure
- Read order for DAEDALUS

### §5.2 Dispatch

User-tier POLYBIUS authors two activation pastes (`HUMAN_paste-pliny-arc-N-instruction.md` + `HUMAN_paste-polybius-arc-N-instruction.md`), commits + pushes to main (per §18.1 user-tier housekeeping), and hands PRINCIPAL the one-line activation prompts. PRINCIPAL spins up fresh Claude Code sessions at the project workspace, pastes the one-liners — fresh PLINY + POLYBIUS activate.

### §5.3 Phase 1 — Design (DAEDALUS + ARGUS)

PLINY dispatches DAEDALUS with the directive as primary input. DAEDALUS produces `agents/design/<work-unit>/design.md`. PLINY dispatches ARGUS cold-audit. Rev1/rev2 iteration if needed; ARGUS PASS gates Phase 2.

### §5.4 Phase 2 — Build (ADA in arc-build worktree)

PLINY creates `arc-N/build` branch in separate worktree per §5.9.4. ADA implements design + commits with Co-Authored-By seat trailer per §28. Multiple ADA commits OK (rev1/rev2 if CATO surfaces fix-now items).

### §5.5 Phase 3 — Verify (VERA + CATO + ZENO parallel)

PLINY dispatches all three concurrently (or sequentially per arc preference). Each returns a verdict. PASS-with-N-non-blocking-advisories acceptable; load-bearing findings trigger ADA rev2.

### §5.6 Phase 4 — Ship + close

PLINY:
- Opens PR with arc title.
- Merges via `gh pr merge --squash --delete-branch`.
- Verifies cleanup live per §5.10 (arc-N/build local + remote deleted; worktree removed; PR merged; main fast-forwarded).
- Closes work-unit ticket + source tickets with cross-ref to merge commit.
- Posts `[for: user-tier-polybius]` invitation on work-unit ticket.

User-tier POLYBIUS picks up the QA pass invitation, runs independent live-verification, posts QA-pass signoff with notes-for-the-record, files any follow-up housekeeping tickets, signs off.

### §5.7 Bundled / canonification batches

Multi-candidate arcs (Arc 32: 5 candidates; Arc 34: 4 candidates) bundle thematically-related substrate-canon work into one gauntlet. The directive enumerates candidates as C1-Cn; ADA lands them coordinated (single coherent commit OR commits per candidate); source tickets close on arc ship per the directive's closure plan.

---

## §6 Coordination

### §6.1 Radio-check protocol (§7.1)

POLYBIUS-pair coordination uses a four-beat liveness signal:
1. **Init handshake** — both peers post `[radio-check <self-seat>]` naming cron id + cadence; ack on first poll.
2. **Routine heartbeats** — every ≤30 min, each peer posts one-line state comment.
3. **Missed-check escalation** — peer-silence > 60 min on open coord ticket → surface "lost contact" to PRINCIPAL.
4. **Closure handshake** — `[radio-check <self> standing down]` + CronDelete on engagement close.

### §6.2 Adaptive polling cadence (§7.2)

Three regimes — Active `*/2 * * * *`, Default `*/5 * * * *`, Quiet `*/15-30 * * * *`. Cadence-switching per-seat unilateral; peers converge within one cycle of the slower cadence.

### §6.3 Cross-tier routing (§7.4)

Project-tier seat needing upper-tier context posts `[for: user-tier-polybius]` tag on own-bw comment; upper-tier seat polls down via unified poll (§7.3) and responds within cadence. Cross-tier-coordination-meets-in-lower-tier.

### §6.4 Cross-tier write boundaries (§7.5)

Each tier reads + writes own bw and downward; never upward. Read-exception preserved for system-architecture-shaped meta-team arcs. Write rule has no exception.

### §6.5 Surface-and-wait (MAJOR_PLINY.md §6.2)

PLINY does NOT poll continuously. PLINY polls only when surfacing a question + cannot continue without response. Cancel cron the moment POLYBIUS responds and work resumes.

### §6.6 PRINCIPAL-gate semantics (§25, Arc 31 canon)

When directive declares a question PRINCIPAL-gated, the discipline is BLOCK (not TAG). The seat halts + escalates immediately rather than proceed-then-flag. Autonomous mode does NOT relax PRINCIPAL-gate semantics — AFK PRINCIPAL means the work waits, not that the work proceeds.

### §6.7 Author-tag convention (Arc 36 / stoa--e39, in flight)

POLYBIUS bw comments carry explicit `[from: <self-seat-slug>]` tags so bw-timeline parsing can attribute by tag, not by inference. Three forms: `[radio-check <slug>]` for self-heartbeats; `[for: <recipient>] [from: <sender>]` for cross-seat-addressed; `[from: <slug>]` for own-bw substantive.

---

## §7 Operating modes

### §7.1 Three modes (canonized at §10 + §11; full progression canon shipping in stoa--ntn)

| Mode | Activity | PRINCIPAL involvement | Coordination |
|---|---|---|---|
| **Pair programming (Mode 2)** | Interactive prototyping, scoping, exploration | High — in-the-loop on every decision | Conversational; bw used as durable record |
| **Full team (Mode 1)** | Formal gauntlet | Decision-points only — phase ratification, ship/no-ship | bw heartbeats at phase transitions; explicit surfacing |
| **Semi-autonomous** | Long-running with periodic check-in | Exception-handler only — escalation triggers per directive | Monitor + bw-poll bridge; radio-check between orchestrators |

Mode propagates downward: parent seat's mode applies to dispatched subagents unless explicitly overridden (Arc 21 A4).

### §7.2 Progression pattern

Typical engagement starts in Mode 2 to scope, transitions to Mode 1 for build, may transition to semi-autonomous for long-running phases, and regresses upward when escalations require re-engagement.

### §7.3 Universal escalation triggers (any mode)

Substance disagreement after one round-trip with peer; authorship/copyright/PRINCIPAL-final-say content; irreducible ambiguity blocking progress; peer silence > 60 min on open coord ticket; arc closure (when shipping public-facing work); PRINCIPAL-gate clauses per §25.

---

## §8 Disciplines (universal preamble — `operating-disciplines.md` §1-§6)

Six anti-patterns absorbed from human SWE culture that no longer apply when iteration cost is near-zero:

1. **Suppress momentum pressure (§1)** — gauntlet cycle is minutes, not weeks. Momentum is a story the model tells itself to skip work.
2. **Suppress MVP / minimize round-trips (§2)** — round-trips cost tokens, not days. Cutting verification to minimize them is a category error.
3. **Suppress don't-gold-plate (§3)** — polish under agents = more verification + review + breadcrumbs. Gold-plating PROCESS is exactly what the regime makes possible.
4. **Suppress passivity (§4)** — failure mode is opposite of human teams: skipping the default pipeline because no one explicitly demanded it. Skipping is forbidden, not exceptional.
5. **Suppress plausible-source citation (§5)** — LLM chronic bug: "X says Y" where X is real but doesn't say Y. Cite live-verified content, not memory.
6. **Suppress single-checker thinking (§6)** — single checker = single point of failure. The 6-stage gauntlet embeds redundancy structurally; 5+ checkers per pass by construction.

**Plus self-applied:**
- **§6.7.1 N=1 honesty** — single observations are not structural lessons; canon promotion requires multi-class evidence + controlled comparison + substrate-level pattern.
- **§19.6 attestation-confabulation** — cite live-verified state, not assumption-from-context state.
- **§25 PRINCIPAL-gate BLOCK semantics** — autonomous mode does not relax gate.
- **§27 mechanical-script / agent-inspection split** — run script → inspection agent surfaces strangeness → POLYBIUS triages with PRINCIPAL approval on gated cases.
- **§28 per-CAPTAIN Co-Authored-By trailer** — seat identity in commit metadata; Author: stays PRINCIPAL.

---

## §9 Tools

### §9.1 bw (beadwork)

Orphan-branch git-stored ticket store. Per-project. CLI-mediated. Commands:
- `bw prime` — session-start workflow context
- `bw list` / `bw show <id>` / `bw history <id>` — reads
- `bw create "<title>" --priority P0-P4 --description "<body>"` — file ticket
- `bw comment <id> "<body>"` — positional, no -m flag
- `bw close <id> --reason "<text>"` — close with reason
- `bw dep add <X> blocks <Y>` — dependency direction matters; blocked-by NOT valid
- `bw sync` — push to orphan beadwork branch

Conventions:
- Prefix per project: `stoa--`, `ariadne--`, `s4--`, `u--` (user-tier)
- Priority: P0 (highest blocking) → P4 (cosmetic/hygiene)
- Sub-tickets: `.1`, `.2` suffixes

### §9.2 git worktrees

Each arc builds in `.claude/worktrees/arc-N-build/` (per §5.9.4). Main worktree stays on main. Per-worktree config.worktree files are silently managed by Claude Code; bw was historically broken on Windows by extensions.worktreeConfig but is now structurally fixed at the bw layer (PR #117).

### §9.3 Agent dispatch + Monitor + bw-poll bridge (§18)

PLINY dispatches CAPTAINs via `Agent({ run_in_background: true, ... })`. Captures task_id. Materializes task_id to bw immediately. Starts persistent Monitor with canonical bw-poll bash template. On CAPTAIN completion notification: TaskStop the Monitor; read verdict via Agent tool result (NOT .output, which is a symlink to JSONL transcript and overflows context).

### §9.4 Ariadne (in some projects)

Document extraction + semantic retrieval pipeline. ariadne-core-workspace deploys this for the team to use as semantic recall over ingested content. Not present in every workspace.

---

## §10 What the team produces

### §10.1 Substrate evolution — current generation creates successor generation

The Stoa team is a **lineage**, not a static configuration. Each arc isn't the team editing itself in place; it is the current-generation team **creating the successor generation** — a team with sharper canon, fresher disciplines, and absorbed lessons from the empirical work the prior generation just shipped. The team that exists after Arc 35 is structurally a different team than the team that existed after Arc 34, even though most of the canon is shared, because the canon delta encodes lessons the prior team's seats did not yet have access to.

Three load-bearing properties of the lineage:

**1. Previous generations remain queryable indefinitely.** When a generation's session closes (compaction, `/clear`, terminal exit, machine restart), the agent is paused, not destroyed. `/resume <session-id>` reactivates that exact agent with its full prior context. A later-generation POLYBIUS or PLINY can spin up a prior-generation peer to ask questions about what shipped, why a decision was made, what the empirical anchor for a discipline was — context the canon may have lost or compressed. Prior generations sit idle until queried; they don't poll, don't burn budget, just exist as warm references. Over time, prior generations become less directly relevant but may retain load-bearing context that never made it into canon.

Each generation handoff produces a handoff doc (per the handoff-author skill) and records the prior generation's session id(s) so successor generations can `/resume` them.

**2. Inter-generational communication happens through bw.** Cross-generation Q&A is conducted via bw tickets + comments, not via chat. A successor-generation agent posts a question on a coordination ticket; the prior-generation agent (when `/resume`'d) reads the ticket via `bw show`, responds via `bw comment`. The exchange is:

- **Auditable** — every question + answer is on the bw timeline with timestamps + author tags (per §7.4 + Arc 36's `[from: <seat>]` convention).
- **Analyzable** — meta-agents can mine the bw record across generations to study how the team's understanding evolved.
- **Substrate-native** — uses the same coordination channel as same-generation work; no separate cross-generation tooling.

The bw record is the team's institutional memory across generations. Canon captures what generalizes; bw captures what the generations actually said to each other.

**3. Meta-agents analyze the lineage.** A meta-agent (a CAPTAIN_CURATOR specialization, or a dedicated future seat) sweeps the bw record across multiple generations to:

- Identify which canon disciplines have empirical lineage vs which are aspirational.
- Detect canon-drift (a discipline shipped but never re-applied; a recurring failure mode not yet canonized).
- Surface lessons that span generations (patterns only visible at N=many rather than N=1 per arc).
- Author retrospectives about the LINEAGE, not a single arc.

This is the system reflecting on itself at the corpus level: the substrate evolves not just because each generation observes its own work, but because meta-agents observe how the generations connect.

### §10.1.1 The per-arc shape (mechanics)

Within each generation transition, the arc itself follows a standard mechanical shape:

- **Surfaces from empirical signal** — failure observed, friction noted, gap identified by the current generation.
- **Authors directive with LOCKED architectural decisions** — durable spec at `substrate/arcs/arc-N-build-directive.md`.
- **Runs the gauntlet** — DAEDALUS → ARGUS → ADA → VERA + CATO + ZENO → PLINY signoff → PR merge (per §5).
- **Ships canon** — new section in operating-disciplines.md, new role file subsection, new skill, template extension, etc.
- **Self-applies the new canon** to the arc's own deliverables where possible (Arc 32 worktree convention, Arc 34 paste archival, Arc 35 Co-Authored-By trailer all self-applied — the arc that ships the convention IS the first worked example of it).

Arc artifacts that constitute the generation-transition record:

- `substrate/arcs/arc-N-build-directive.md` — the durable spec the successor generation inherits.
- `substrate/arcs/arc-N/pastes/HUMAN_paste-*-arc-N-instruction.md` — archived activation pastes per §5.11.
- `agents/design/<work-unit>/design.md` — DAEDALUS output capturing the design rationale.
- `agents/verdicts/<work-unit>/` — VERA / CATO / ARGUS / ZENO verdicts capturing the verification trail.
- Squash-merge commit on main — the actual canon change; this is the commit the successor generation reads as its baseline state.

### §10.2 Project work (per consumer workspace)

Each consumer workspace's team ships project work via the same gauntlet. Examples: ariadne-core ships document-extraction pipeline features; sector-4 ships MVP-shape work; railway_stoa ships Railway-deployment tooling.

### §10.3 Skills (deployable patterns)

Skills live at `substrate/skills/<name>/SKILL.md`. They encode reusable patterns (credential-discipline, check-bw-release, inspect-script-output, agent-author, cite-check, format-validate, runner, save-verdict, etc.). Triggered by SKILL.md description matching against the agent's current task.

### §10.4 Documentation (case study, retros)

`docs/case-study/` — long-form narrative of the substrate's evolution + an interactive visualization (`architecture-kg.html`).
`docs/sessions/` — per-session retrospective docs capturing emergent patterns.

### §10.5 The deployable artifact itself

The substrate IS the deliverable. Every install.sh run at a downstream project ships the current state of the team's canon to that project.

---

## §11 Out of scope (anti-patterns the team rejects)

- **Premature optimization of process** — the team optimizes for verification redundancy + low coordination overhead; raw speed is downstream.
- **Single-agent shortcuts** — no "I'll just do this without the gauntlet"; the gauntlet is what's expensive in human teams + cheap in agent teams.
- **Authorship confabulation** — file-frontmatter `author:` fields name PRINCIPAL (Denson Smith); git commit Author: never overrides; Co-Authored-By trailers signal seat identity but do not replace Author.
- **Citation by memory** — every claim that affects the work cites live-verified state, not assumed-from-context.
- **Cross-tier upward writes** — never; coordination meets in lower tier via `[for:]` tags.
- **Deferral of known bugs** — "minor / polish / later" framings are 2010-era human-team logic; in this regime the fix cost is near-zero, so see-once-fix-once.
- **Glossing over technical debt with "absorbed-by-X" closures** — if the underlying discipline-gap is real, the canon ships; "informally working" is not a substitute for canon.
- **Destroying prior-generation sessions before lineage value is exhausted** — aggressive `/clear` of POLYBIUS/PLINY/CAPTAIN sessions that may still hold context not captured in canon truncates the lineage (per §10.1, §4.5). Default is to leave prior generations idle but `/resume`-able; close sessions only when their context is fully absorbed into canon + bw, or when the session has obvious failure modes (e.g., terminal contamination). When in doubt, leave the session alive — idle sessions cost nothing.

### §12.1 What's shipped at the-stoa

35 arcs shipped at main. Substantive recent canon:
- Arc 25 — credential discipline
- Arc 27 — POLYBIUS lifecycle (§16)
- Arc 28 — bw 0.13.0 features + check-bw-release skill
- Arc 29 — base-vs-custom convention (§17 + §23)
- Arc 30 — pre-branch hygiene (MAJOR_PLINY.md §5.9)
- Arc 31 — PRINCIPAL-gate discipline (§25)
- Arc 32 — bundled batch (§5.1.1.1 / §5.1.3 / §5.10 / §19.6 / §5.9.4 worktree convention)
- Arc 33 — mechanical-script / agent-inspection split (§27 + inspect-script-output skill)
- Arc 34 — bundled batch (§18 user-tier housekeeping / §5.11 paste archival / §9 step 3 HITL-paused sweep / template title fix)
- Arc 35 — per-CAPTAIN Co-Authored-By trailer (§28 + MAJOR_PLINY.md §5.12 + CAPTAIN_ADA.md §5.5 extension)

### §12.2 What's in flight

- Arc 36 — dispatch artifacts written + committed at `28155f7` but NEVER dispatched. Original scope-recut shipped Part 1 only (e39 author tags); Part 2 (cgn cron expiry) was deferred. Per PRINCIPAL no-deferrals stance, Arc 36 needs re-dispatch with both Parts OR replacement with bundled Arc 37.

### §12.3 What's open

- **stoa--vz9** — substantively complete 2026-05-04; only bw close action missing.
- **stoa--e39 + stoa--jru** — Arc 36 work-unit + parent EPIC; close on Arc 36 ship.
- **stoa--cgn** — cron expiry handling; deferred this morning with gating criteria, but per PRINCIPAL no-deferrals stance now ships in Arc 36 v2 or Arc 37.
- **stoa--53u** — idle-state retrospective-narrative confabulation discipline (sister to §19.6).
- **stoa--86k** — two-team forge/shop behavioral canon.
- **stoa--kt6** — multi-team interoperation unified canon.
- **stoa--wad** — four-layer identity model + memories-as-alignment.
- **stoa--ntn** — operating-mode progression canon.
- **stoa--7e3** — handoff-author skill (draft preserved at `_drafts/skill_handoff_author.md`).
- **stoa--cye** — orphan worktree dirs + sandbox claude branches (Phase 1D complete; bw close pending).
- **stoa--k03** — Arc 35 P4 follow-ups (Phase 1B + 1C complete; bw close pending).

### §12.4 Uncommitted working-tree state

- 14 broken `substrate/CLAUDE.md` path-citations corrected across 12 arc directives (Phase 1B)
- 3 design.md probe-formulation refinements in stoa--kjo (Phase 1C)
- 18 stale `_drafts/` files deleted (Phase 1A); `skill_handoff_author.md` kept
- 2 orphan worktree dirs + 2 sandbox claude branches deleted (Phase 1D)
- 2 untracked PDFs in `docs/case-study/` awaiting disposition

### §12.5 What's NOT yet built that the spec implies

- **Handoff-author skill** (stoa--7e3) — substrate has informal HANDOFF_*.md pattern but no skill agents can load on demand.
- **Per-agent git seat-identity forward propagation** — Arc 35 shipped the canon (§28) and self-applied; Arc 36+ is the first opportunity to see if it propagates cleanly forward.
- **Cron-expiry handling** (stoa--cgn) — 7-day cap hasn't bitten because engagements have been short; structurally still exposed.
- **Idle-state retrospective-narrative discipline** (stoa--53u) — §19.6 covers attestation-time confabulation; idle-narrative is a distinct shape not yet canonized.
- **Two-team behavioral canon** (stoa--86k) — base team designs project team; routing rule for which work goes where.
- **Multi-team interop unified section** (stoa--kt6) — partial canon exists; no unified section names the architecture.
- **Four-layer identity model** (stoa--wad) — no canon for role / memories / handoff / bw substrate as the layers of agent identity.
- **Operating-mode progression canon** (stoa--ntn) — §10 + §11 cover modes individually; progression sequence + transition triggers + regression pattern not canonized.
- **Generation-handoff session-id record** — the `/resume` lineage pattern in §10.1 requires recording prior-generation session ids so successors can spin them up. Convention not yet canonized; handoff-author skill (stoa--7e3) covers within-handoff content but not the session-id-as-warm-reference pattern.
- **Meta-agent for cross-generation lineage analysis** — no current seat performs the §10.1.3 lineage-analysis role (canon-empirical-lineage check / cross-generation drift detection / multi-arc retrospectives). CAPTAIN_CURATOR has the closest mandate (cross-ticket synthesis) but operates within a generation. May be a CURATOR specialization or a dedicated future seat; the framing is in §10.1 but the implementation is unbuilt.

---

## §13 Make-the-team-meet-the-spec workplan

This section is for the fresh team operating semi-autonomously to read at activation. Its job: read the spec, compare to current state (§12), identify the gaps that block "the team matches the spec," sequence the work to close them, execute via the standard arc lifecycle, and only AFTER all substrate-side work is done does the team enter the validation phase.

### §13.1 Sequencing principle — front-load everything before validation

Validation is the LAST step, not a check that runs alongside work. Every substrate gap, every canon insertion, every cleanup commit, every drift correction happens BEFORE the validation dispatch fires. The reason: validation surfaces what's broken; if the team validates against an in-flight state, the validation surfaces in-flight noise as if it were real failure.

The team works through Passes 1-5 below to drive the substrate to its "spec met" end state. Only then does Pass 6 (validation) run.

### §13.2 Pass 1 — Working-tree cleanup (no arcs; user-tier housekeeping)

- Commit the in-flight Phase 1B/1C/1D cleanup (broken path sweep + design.md refinements + worktree-dir + branch deletions).
- Decide on the 2 untracked PDFs in `docs/case-study/`.
- Close stoa--vz9 (audit-complete; missed bw close).
- Close stoa--cye + stoa--k03 (work already done in Phase 1).
- Commit SPECIFICATION.md itself (the document the team is meeting).

### §13.3 Pass 2 — Arc 36 v2 (the in-flight dispatch, re-shaped)

- Rewrite `substrate/arcs/arc-36-build-directive.md` + activation pastes to cover BOTH Part 1 (e39 author tags) + Part 2 (cgn cron-expiry) per original arc-22 bundling.
- Update bw comments on jru/e39/cgn correcting the morning's deferral framing.
- New commit; push; surface activation one-liners.

### §13.4 Pass 3 — Arc 37 (substrate architecture canonification batch, 6 candidates)

- C1: stoa--86k two-team forge/shop division of concerns (MAJOR_POLYBIUS.md behavioral section)
- C2: stoa--kt6 multi-team interoperation unified canon (operating-disciplines.md new section)
- C3: stoa--wad four-layer identity model + memories-as-alignment (op-disc + MAJOR_POLYBIUS.md)
- C4: stoa--ntn operating-mode progression (extends §10/§11)
- C5: stoa--53u idle-state retrospective-narrative confabulation (op-disc §19.7 sister to §19.6)
- C6: stoa--7e3 handoff-author skill (new `substrate/skills/handoff-author/` from draft at `_drafts/skill_handoff_author.md`; install.sh wiring; role-file cross-refs)

After Pass 3 ships: **zero open substrate-canon tickets at the-stoa.**

### §13.5 Pass 4 — Spec accuracy reconciliation (no arc; user-tier housekeeping)

The spec was written 2026-05-17 against the substrate state at that moment. Passes 1-3 shipped new canon. Walk the spec end-to-end against the post-Pass-3 substrate:

- Every §-reference resolves to its current location (line numbers may have shifted).
- Every cited ticket id has the correct status (closed vs open).
- §12 (current state snapshot) updates to reflect post-Pass-3 reality — what's shipped, what's open, what's in flight, what's in the working tree.
- §12.5 (what's NOT yet built that the spec implies) shrinks as Passes 2-3 close gaps; any remaining items have filed tickets + gating criteria.
- Any spec section that turned out to be aspirational rather than describing shipped canon either (a) gets revised to match shipped reality, or (b) gets the new ticket filed + cross-referenced as future work.

Commit the spec reconciliation as a direct-to-main per §18.1.

### §13.6 Pass 5 — Mechanical-check pass (substrate state matches spec)

Author + run a `validate-spec` skill following the §27 mechanical-script / agent-inspection split pattern:

**Mechanical script checks:**
- Every §-reference in SPECIFICATION.md resolves (grep against canon file at named section).
- Every cited `stoa--*` ticket id exists in bw with the claimed status.
- `bw list --status open` matches §12.3.
- `git status` matches §12.4's catalogue.
- `_drafts/` contents match §12.4's keep-list.
- `check-substrate-updates` skill returns "no drift" across registered consumer workspaces.
- §28 Co-Authored-By trailers present on post-Arc-35 squash-merge commits.

**Inspection-agent triage:**
- Any check reporting strangeness gets human-readable diagnosis from the inspection agent.
- POLYBIUS triages the diagnoses — fix-now items get fixed; escalations route to PRINCIPAL.

Pass 5 produces an artifact at `agents/observation/spec-validation/mechanical-check-results.md` capturing each check's pass/fail status + evidence trail.

### §13.7 Pass 6 — Behavioral validation via test-project dispatch

The substrate is now at "spec met" mechanically (§13.2-§13.6 done). The team validates BEHAVIORALLY by dispatching itself against an unrelated test project:

**Test project:** `stellation` (or whichever name PRINCIPAL ratifies) — a React app that displays beadwork tickets in a visually interesting animated way. Specification lives at `docs/validation/stellation-SPECIFICATION.md` (authored at this same time as a paired artifact to this spec).

**Why this validates the substrate:** the test project is brand new + completely unrelated to substrate work + relatively simple in scope. A team can only deliver it well if the substrate disciplines they inherit actually work. The team's ability to:

- Run the arc lifecycle (§5) end-to-end without coaching
- Coordinate via the radio-check + bw-tag conventions (§6 / §7.1 / §7.4 / Arc 36 author tags)
- Self-apply disciplines (§28 trailers; §5.10 signoff; §5.11 paste archival; §19.6 attestation honesty)
- Reject anti-patterns (§11) when they arise organically in the work
- Hand off to PRINCIPAL at the right moments per §13.10 escalation triggers

— is the validation. If the substrate works, the test team ships the test project clean. If the substrate is broken, the test team's friction points surface the breaks.

**Setup steps:**
1. PRINCIPAL creates the test-project repo at `~/claude_projects/stellation/` and copies in the test-project spec.
2. PRINCIPAL runs `the-stoa/substrate/install.sh` from inside the test-project repo to deploy the spec'd substrate.
3. PRINCIPAL spawns fresh POLYBIUS + PLINY sessions at the test-project workspace.
4. The test team operates per their deployed substrate against the test-project spec — semi-autonomous mode; PRINCIPAL exception-handler.

**Observation hooks (the validation evidence):**
- Test-team coordination on bw — does it follow §7 conventions?
- Test-team commit history — do CAPTAIN commits carry §28 trailers?
- Test-team signoff comments — do they live-verify per §5.10?
- Test-team paste archival — do they archive per §5.11?
- Test-team escalations — when ambiguity surfaces, does the team surface per §25 PRINCIPAL-gate semantics rather than improvise?
- PRINCIPAL's experience — does the team feel like the team described in this spec, or does it feel like something else?

Pass 6 produces an artifact at `agents/observation/spec-validation/test-dispatch-trail.md` capturing the observation evidence + the substrate-side learnings (any place the test team hit friction that surfaces a spec/canon gap).

If Pass 6 surfaces real substrate gaps, the gaps return to Pass 3 (file ticket + ship as Arc 38+) and Pass 5/6 re-run after.

### §13.8 What "meeting the spec" looks like — final definition

The team has met the spec when ALL of:

1. **Substrate-state matches spec** — every claim in this document either describes shipped canon (§13.5 reconciliation done) or is explicitly marked future work with filed ticket + gating criteria.
2. **No deferred-without-plan tickets** — no open P2 at the-stoa is in "awaiting-architectural-decision" or "deferred-without-plan" state.
3. **Working tree clean** — `_drafts/` contains only docs for an in-flight arc; `git status` matches §12.4 catalogue; no accumulated cleanup debt.
4. **No substrate drift** — `check-substrate-updates` shows source-canon-and-deployed-instances byte-equal across consumer workspaces.
5. **Mechanical-check passes** — Pass 5 produces all-green at `agents/observation/spec-validation/mechanical-check-results.md`.
6. **Behavioral validation passes** — Pass 6 test-project dispatch produces a working `stellation` build that meets its own spec, the test team's observation trail shows substrate disciplines were applied, and PRINCIPAL signs off on the test-dispatch experience as "substrate-as-described."

### §13.9 What's explicitly out of scope for "make-the-team-meet-the-spec"

The fresh team should NOT, while closing the spec gaps:

- Build product features for any non-validation consumer workspace (ariadne, sector-4, railway) — those are post-spec work motions.
- Extend conventions to non-POLYBIUS / non-CAPTAIN seats without explicit scope expansion via fresh ticket + PRINCIPAL ratification.
- Build mechanical enforcement infrastructure (pre-commit hooks, validators, etc.) beyond what existing canon authorizes — the script/agent split (§27) is the model; mechanical infra ships only on documented recurrence.
- Touch the substrate-deploy mechanism (install.sh / apply.sh / revert.sh) beyond what the Pass 3 candidates + Pass 6 validation require.
- Build the meta-agent for cross-generation lineage analysis (§10.1.3 / §12.5) — out of scope for spec-meeting; framing is described; implementation is post-spec.

### §13.10 Mode + dispatch

The team operates Passes 1-6 in **semi-autonomous mode** per §7. PRINCIPAL is exception-handler:

- DAEDALUS sub-decisions that hit PRINCIPAL-gate criteria → BLOCK + surface immediately per §25.
- Substance disagreement after one round-trip with peer → surface.
- Authorship / copyright / PRINCIPAL-final-say content → surface.
- End-of-arc clean-PASS for ship/no-ship → surface (Mode 1 ratification at decision points).
- Pass 6 test-dispatch substrate-friction surfaces → surface as soon as observed.

User-tier POLYBIUS QA passes happen at end of EACH arc per PRINCIPAL's pattern.

### §13.11 Definition of done

The fresh team's job ends when:

- Pass 5 (mechanical-check) shows all-green.
- Pass 6 (test-project behavioral validation) shows the test team shipped the test project to its spec; observation trail captures the substrate-disciplines-applied evidence.
- A user-tier POLYBIUS QA pass on Pass 6 signs off "substrate-as-described; spec met behaviorally."
- PRINCIPAL is handed a one-line summary: "spec met (mechanical + behavioral); ready for product work; next: <PRINCIPAL ratifies next motion>."

After spec met, the team transitions to **product mode** — shipping work in consumer workspaces (ariadne, sector-4, etc.) using the spec'd + validated team capabilities.

---

## §14 PRINCIPAL editing notes

Areas where PRINCIPAL most likely wants to edit before handing this to the fresh team:

- **§1 Purpose** — does the framing match your actual intent for the team, or is the team for something narrower / broader?
- **§4 Seats** — any CAPTAIN whose job description doesn't match your mental model? Any seat missing?
- **§7 Operating modes** — does the three-mode progression match your actual working pattern?
- **§10 What the team produces** — is "the substrate is the deliverable" the right framing for the-stoa specifically, or should the case-study / app / etc. be more prominent?
- **§11 Out of scope** — anything to add to the anti-patterns list?
- **§12 Current state** — corrections to what's shipped / open / in flight.
- **§13 Workplan** — is the gap-closure sequence right? Is Pass 3 sized correctly (6 candidates)?
- **§13.2 Definition of "meeting the spec"** — are the criteria the right ones?

Free-form edits + corrections welcome anywhere. After your edits, the fresh team activates via standard dispatch pattern with this file as primary input.
