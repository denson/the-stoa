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

Eleven CAPTAIN seats, each with a focused job and bounded toolset:

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
| CAPTAIN_TIRO *(per Arc 38 / stoa--ojz; not yet shipped)* | bw substrate specialist — reads bw on delegation; advises other seats on bw read+write syntax; never writes for another seat | Bash, Read, Grep, Glob |

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

### §3.4 The two-team-per-project model (shipped Arc 37 as stoa--86k → MAJOR_POLYBIUS.md §19)

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

### §4.6 Substrate-specialist seats — bounded-context expertise for subsystems with gotchas

Some substrate subsystems accumulate enough operator-tripping gotchas (default-truncation flags, syntax variants, lifecycle quirks) that generalist agents reliably miss them under context-pressure. The pattern when this surfaces empirically: ship a dedicated specialist seat whose entire context is that subsystem.

**CAPTAIN_TIRO** (bw substrate specialist) is the first such seat (*spec'd 2026-05-17; ships in Arc 38 per stoa--ojz; descriptive paragraphs below use present-tense as forward design language*):

- **TIRO does reads directly** when delegated. Any seat dispatches TIRO with a query ("all open P2 tickets at the-stoa", "comment history on stoa--y14", "tickets blocked-by stoa--bj5"). TIRO runs the right bw subcommand with the right completeness flags (e.g., `bw list --status open --all` unhides the default truncation that bites generalist auditors) and returns a clean structured answer. The whole-context priming on bw mechanics fixes the "generalist forgets to apply the known gotcha" failure mode that the §12 cookbook alone doesn't prevent.
- **TIRO never writes for another seat.** Writes (create, comment, close, dep add, sync) are authored by the seat that owns the work. Reasons: (a) authorship attribution stays clean — a comment from POLYBIUS_the_stoa is genuinely from that seat, not via TIRO proxy; (b) Arc 36's `[from: <self-seat-slug>]` author-tag convention stays meaningful — proxy-writes would muddy the timeline-arithmetic that radio-check + heartbeat thresholds consume; (c) accountability for state changes stays with the seat making the change.
- **TIRO advises on write syntax.** Any seat can ask TIRO "what's the canonical command to close stoa--y14 with an audit comment?" and TIRO returns the syntax (positional `bw comment <id> "text"` not `-m` flag; `--reason` flag on close; HEREDOC pattern for multi-line; the dep-add direction gotcha; etc.). The asking seat then executes the command themselves.

The pattern generalizes: subsystems whose operator-tripping surface justifies a dedicated specialist seat get one. Candidates if the pattern proves valuable: git (Arc 37's squash-merge `--body` trailer-drop regression; gh CLI gotchas), cron (the `durable: true` non-persistence bug per anthropics/claude-code#40228; cadence-switching pitfalls), worktrees (Windows file-handle quirks). None of these are committed-to as future seats — they're noted candidates if the TIRO pattern proves valuable in practice.

**Empirical anchor for TIRO:** 2026-05-17 — user-tier POLYBIUS conducted three substrate audits over the course of the day, each citing "X open tickets" as live state. Each audit used `bw list 2>&1 | grep "^○"` without the `--all` flag; each returned a truncated subset; each subsequent audit "discovered" additional tickets that had been hidden the previous times. The cookbook at operating-disciplines.md §12.1 explicitly documents `--all` as the completeness flag; the operator knew the flag existed and did not apply it. This is the §19.6 attestation-confabulation failure mode applied to bw-audit attestations. **TIRO will ship as the structural fix at Arc 38 (stoa--ojz).**

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
- Verifies cleanup live per `MAJOR_PLINY.md` §5.10 signoff-accuracy (arc-N/build local + remote deleted; worktree removed; PR merged; main fast-forwarded).
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

### §6.7 Author-tag convention (Arc 36 v2 / stoa--e39 — shipped at `fcd68c0`)

POLYBIUS bw comments carry explicit `[from: <self-seat-slug>]` tags so bw-timeline parsing can attribute by tag, not by inference. Three forms: `[radio-check <slug>]` for self-heartbeats; `[for: <recipient>] [from: <sender>]` for cross-seat-addressed; `[from: <slug>]` for own-bw substantive.

---

## §7 Operating modes

### §7.1 Three modes (canonized at §10 + §11; full progression canon shipped Arc 37 / stoa--ntn at `bb12806`)

| Mode | Activity | PRINCIPAL involvement | Coordination |
|---|---|---|---|
| **Pair programming (Mode 2)** | Interactive prototyping, scoping, exploration | High — in-the-loop on every decision | Conversational; bw used as durable record |
| **Full team (Mode 1)** | Formal gauntlet | Decision-points only — phase ratification, ship/no-ship | bw heartbeats at phase transitions; explicit surfacing |
| **Semi-autonomous** | Long-running with periodic check-in | Exception-handler only — escalation triggers per directive | Monitor + bw-poll bridge; radio-check between orchestrators |

Mode propagates downward: parent seat's mode applies to dispatched subagents unless explicitly overridden (Arc 21 A4).

### §7.2 Progression pattern

Typical engagement starts in Mode 2 to scope, transitions to Mode 1 for build, may transition to semi-autonomous for long-running phases, and **regresses upward** when escalations require re-engagement. ("Upward" = toward higher PRINCIPAL involvement — toward Mode 2 / Mode 1; the autonomous-mode regime is structurally "deeper" / less PRINCIPAL-touched, so regression toward more PRINCIPAL contact is "up." Per `operating-disciplines.md` §10's matching gloss: "Regression upward is normal, not exceptional.")

### §7.3 Universal escalation triggers

Originally canonized at `operating-disciplines.md` §10 for autonomous-mode engagements; in practice the same triggers apply across all modes (in HITL/Mode-1/Mode-2 the triggers fire implicitly because PRINCIPAL is more in-the-loop already; in semi-autonomous they fire as discrete escalation events). The trigger list:

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
- `bw list` / `bw show <id>` / `bw history <id>` — reads (note: `bw list` truncates by default; `bw list --status open --all` unhides truncation for completeness audits)
- `bw create "<title>" --priority P0-P4 --description "<body>"` — file ticket
- `bw comment <id> "<body>"` — positional, no -m flag
- `bw close <id> --reason "<text>"` — close with reason
- `bw dep add <X> blocks <Y>` — dependency direction matters; blocked-by NOT valid
- `bw sync` — push to orphan beadwork branch

Conventions:
- Prefix per project: `stoa--`, `ariadne--`, `s4--`, `u--` (user-tier)
- Priority: P0 (highest blocking) → P4 (cosmetic/hygiene)
- Sub-tickets: `.1`, `.2` suffixes

**Specialist delegation (post-Arc-38):** for read queries (especially completeness audits) other seats delegate to **CAPTAIN_TIRO** per §4.6. TIRO's whole context is bw mechanics; the audit-completeness failure mode (operator forgets `--all` flag) is structurally absorbed by TIRO's bounded-context priming. Writes stay with the seat that owns the work; TIRO advises on write syntax when asked but does not execute writes on another seat's behalf. **Until Arc 38 ships TIRO**, seats use `bw` directly + apply `--all` per the cookbook for completeness audits — note the friction as Arc 38 empirical anchor reinforcement.

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

Each generation handoff produces a handoff doc (per the handoff-author skill) and records the prior generation's session id(s) so successor generations can `/resume` them. **Recording is mandatory per `substrate/skills/handoff-author/SKILL.md` step 6** (upgraded from optional → mandatory 2026-05-17 per SPEC_AUDIT C1 fix); the unrecoverable-id case (terminal closed before capture) is explicitly noted in the handoff so the successor knows the `/resume` option is unavailable for that lineage step. The *invocation* discipline (when to `/resume` vs spawn fresh; how to handle stale ids) is a separate canon gap tracked at `stoa--lyw` (see §12.5 lineage-architecture follow-up).

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

## §12 Current state — structure + queries (derived views, not authored snapshots)

**Structural change 2026-05-17 (post-SPEC_AUDIT_R2):** §12 was previously authored as enumerated snapshots of substrate state (37 arcs listed; 18 open tickets listed; commit history listed). SPEC_AUDIT R1 + R2 caught the same `§12 internal staleness` pattern twice at different inflection points: the snapshots drift whenever the source-of-truth (substrate canon, `bw`, `git`) advances faster than the spec is refreshed. The structural fix per SPEC_AUDIT_R2 closing observation: §12 is now **derived view** — each subsection describes WHAT COUNTS as the named state-class + the QUERY that returns current state. The spec carries the contracts; current state lives in `bw` + `git log` + `git status` + §13 (workplan bucketing); the `validate-spec` skill (per §13.11 Pass 9) renders combined views on demand.

This shape eliminates the §12-internal-staleness drift class by structural removal: §12 cannot drift from substrate state because it doesn't carry substrate state.

### §12.1 What counts as shipped

A change is "shipped" when its commit is on `origin/main` AND (for arc-shipped canon) the squash-merge PR is closed. Per Arc 35 §28: post-Arc-35 squash-merges carry per-CAPTAIN Co-Authored-By trailers (with the explicit `bb12806` carve-out per §13.11).

**Queries:**
- `git log --oneline main` — full commit history
- `gh pr list --state merged --limit 20` — recent merged PRs
- `git log --grep='^Arc' --oneline` — arc-ship commits (each arc PR title is prefixed `Arc N:`)

**Reference points for orientation** (not authoritative; refresh via queries above for current state): Arc 35 ship `6414397`; Arc 36 v2 ship `fcd68c0`; Arc 37 ship `bb12806`; Arc 38 ship `0b5f7f3`; Arc 39 ship `f1f222a`; Arc 40 ship `dbb5b81`; Arc 41 ship `6b6fb11`. The Arc 37 squash-merge `bb12806` body carries empty `%(trailers)` due to PLINY's `--body` override defeating GitHub's default trailer-concatenation; this was the empirical anchor for stoa--6wp (Arc 40 C4) shipped 2026-05-18, which structurally closed the regression class by codifying trailer-preservation discipline at MAJOR_PLINY.md §5.10 + op-disc §28.3.1. The §13.11 Pass 9 mechanical-check carves out `bb12806` as the known historical exception (the fix is forward-only per CLAUDE.md's no-force-push rule); Arcs 38 + 39 + 40 + 41 each shipped 10-11 trailers preserved through squash-merge, confirming the canon holds across downstream consumer arcs.

### §12.2 What counts as in flight

A change is "in flight" when an `arc-N/build` branch exists (locally or remotely) AND no PR has merged yet, OR when a non-arc engagement (spec audit, housekeeping pass) has authored a coordination ticket that isn't yet closed.

**Queries:**
- `git branch | grep -E '^\s*arc-[0-9]+/build$'` — local arc-build branches
- `git ls-remote --heads origin | grep arc-` — remote arc-build branches
- `gh pr list --state open` — PRs awaiting review/merge
- `bw list --status open --all | grep -i 'engagement coordination'` — non-arc engagement coord tickets

If all four return empty: nothing is in flight; the substrate is at a stable snapshot.

### §12.3 What counts as open

A bw ticket is "open" when `bw show <id>` shows `# ○` (not `# ✓`). Per `operating-disciplines.md` §12.1 cookbook + §4.6 TIRO empirical anchor: **ALWAYS use `bw list --status open --all` for completeness audits** (the unflagged `bw list` truncates by default; the `--all` flag unhides truncation; R1 + R2 + the fold-in commit + this commit are all empirical anchors for the audit-completeness failure mode that motivated CAPTAIN_TIRO at §4.6).

**Queries:**
- `bw list --status open --all` — all open tickets with prefix `stoa--`
- `bw show <id>` — full ticket detail (body + comments + dependencies)
- `bw history <id>` — chronological history

**Bucketing for the make-the-team-meet-the-spec workplan** lives throughout §13. The canonical source-of-truth for which §13.x sections enumerate ticket placements is §13 itself — walk §13 end-to-end to find ticket placements; do NOT rely on a §12-side enumeration of which §13.x sections place tickets (such an enumeration would itself drift whenever new §13.x sections place tickets, as SPEC_AUDIT_R3 NC7 demonstrated empirically). For a current-time accounting of open-tickets-by-bucket: run `bw list --status open --all`; walk §13 looking for any section that enumerates ticket placements (e.g., per-arc candidate lists, deferred-with-gating, Pass-N inline-handled items, explicitly-out-of-scope follow-ups); cross-reference each open ticket against the union of all such §13.x sections. Any open ticket NOT placed in any §13.x section is an unplaced ticket and surfaces as a §12.3 audit finding (the spec is missing a bucket for it).

### §12.4 What counts as working-tree clean

A working tree is "clean" when `git status` shows no uncommitted changes EXCEPT auto-modified state files like `.claude/.substrate-last-check` (modified each substrate-check skill run; ignorable churn) AND `_drafts/` contains only docs actively in use by an in-flight engagement.

**Queries:**
- `git status` — working tree state
- `ls _drafts/` — drafts directory contents
- `git log --oneline -20` — recent commit history (for context on what's been worked on)
- `git diff --stat` — magnitude of uncommitted changes if any

### §12.5 Known gaps the spec implies (authored content)

The canonical gap list lives throughout §13. Each ticket-placing §13.x section enumerates its candidates with the ticket id + scope + sequencing note. As candidates ship and tickets close, the §13.x section reads as historical; new candidates surface when fresh tickets are filed against new gaps. For a current accounting of which gaps exist + which are addressed by which §13.x section: walk all of §13 looking for sections that enumerate ticket placements (per SPEC_AUDIT_R3 NC7, do NOT rely on a §12-side enumeration of which §13.x sections place tickets — such an enumeration would itself drift whenever new §13.x sections place tickets; the dynamic walk is the safe path).

For the CURRENT list of gaps + their disposition: run `bw list --status open --all`; walk §13 looking for ticket-placing sections; cross-reference each open ticket against the union of §13.x placements. Any open ticket NOT placed in any §13.x section is a §12.5 audit finding (gap is real but not in the plan).

(The "Generation-handoff session-id record" item previously listed here is REMOVED — Arc 37 C6 / Arc 38 SKILL.md upgrade per C1 fix ships it as mandatory canon.)

---

## §13 Make-the-team-meet-the-spec workplan

This section is for the fresh team operating semi-autonomously to read at activation. Its job: read the spec, compare to current state (§12), identify the gaps that block "the team matches the spec," sequence the work to close them, execute via the standard arc lifecycle, and only AFTER all substrate-side work is done does the team enter the validation phase.

### §13.1 Sequencing principle — front-load everything before validation

Validation is the LAST step, not a check that runs alongside work. Every substrate gap, every canon insertion, every cleanup commit, every drift correction happens BEFORE the validation dispatch fires. The reason: validation surfaces what's broken; if the team validates against an in-flight state, the validation surfaces in-flight noise as if it were real failure.

The team works through Passes 1-9 below to drive the substrate to its "spec met" end state. Only then does Pass 10 (behavioral validation) run.

### §13.2 Pass 1 — Working-tree cleanup (no arcs; user-tier housekeeping) — DONE 2026-05-17

- Committed in-flight Phase 1B/1C/1D cleanup (broken path sweep + design.md refinements + worktree-dir + branch deletions).
- 2 untracked PDFs in `docs/case-study/` preserved under `docs/case-study/sources/`.
- Closed stoa--vz9 (audit-complete; missed bw close).
- Closed stoa--cye + stoa--k03 (work already done in Phase 1).
- Committed SPECIFICATION.md + stellation-SPECIFICATION.md.

### §13.3 Pass 2 — Arc 36 v2 (bundled coordination-hygiene) — DONE 2026-05-17

- Rewrote `substrate/arcs/arc-36-build-directive.md` + activation pastes to cover BOTH Part 1 (e39 author tags) + Part 2 (cgn cron-expiry) per original arc-22 bundling.
- Updated bw comments on jru/e39/cgn correcting the morning's deferral framing.
- Arc 36 v2 shipped at PR #16 squash-merge `fcd68c0`; paste archival at `8ced17c`.
- All 3 source tickets closed (stoa--e39 + stoa--cgn + stoa--jru).
- 5 DAEDALUS rev cycles; design grew 1033 → 2152 lines; complexity largely irreducible per A7/A10 LOCKED matrix (Option 3 in absence of CronUpdate primitive).
- One follow-up filed as stoa--pqn (P4): VERA probe-regex tightening + bug #40228 surveillance + organic adoption observation.

### §13.4 Pass 3 — Arc 37 (substrate architecture canonification batch, 6 candidates) — DONE 2026-05-17

- C1: stoa--86k two-team forge/shop division of concerns (MAJOR_POLYBIUS.md behavioral section)
- C2: stoa--kt6 multi-team interoperation unified canon (operating-disciplines.md new section)
- C3: stoa--wad four-layer identity model + memories-as-alignment (op-disc + MAJOR_POLYBIUS.md)
- C4: stoa--ntn operating-mode progression (extends §10/§11)
- C5: stoa--53u idle-state retrospective-narrative confabulation (op-disc §19.7 sister to §19.6)
- C6: stoa--7e3 handoff-author skill (new `substrate/skills/handoff-author/` from draft at `_drafts/skill_handoff_author.md`; install.sh wiring; role-file cross-refs; consider extending with generation-handoff session-id record per §12.5 future-work)

### §13.5 Pass 4 — Arc 38 (substrate architecture batch, 3 candidates) — DONE 2026-05-17

Shipped at PR #18 → main `0b5f7f3` + paste archival `54f8d46`. Three candidates landed:

- **C1: stoa--ojz — CAPTAIN_TIRO bw substrate specialist seat** (per §4.6) — `substrate/CAPTAIN_TIRO.md` (268 LOC) with read-direct + write-advisory split per SPECIFICATION.md §4.6 PRINCIPAL-lock; install.sh wiring at all 3 tiers (11 CAPTAINs); cross-refs at MAJOR_POLYBIUS §7.3 + MAJOR_PLINY §6.1 + op-disc §12.4 + CAPTAIN_ADA + CAPTAIN_CATO.
- **C2: stoa--bj5 — user-tier substrate drift detection** — `.substrate-manifest` (A8 γ pick) at `<workspace>/.claude/.substrate-manifest`; install.sh writes manifest at deploy; check.sh + apply.sh manifest-driven substitution; revert.sh tier-agnostic; friendly fallback when manifest absent.
- **C3: stoa--gq1 — substrate-component design principles** — `operating-disciplines.md` §31 (A11 α at line 1935) with N=2 honest framing (A13 ii: Ariadne + Stoa substrate as parallel anchors).

Follow-up filed: stoa--6n9 (P3) — manifest format-version header (CATO c3 follow-up; shipped Arc 40).

### §13.6 Pass 5 — Arc 39 (substantial mid-bundle, 2 candidates) — DONE 2026-05-18

Shipped at PR #19 → main `f1f222a`. Two candidates landed:

- **C1: stoa--utn — save-verdict skill promotion** — `substrate/skills/save-verdict/{SKILL.md, _save_verdict.py, _lib/byte_copy.py}` (Python helpers per Arc 23 SKILL.md procedure; ~300 LOC); install.sh SKILL_NAMES += save-verdict. A2 α pick (single-skill private `_lib/`), A4 ii pick (lift-and-modernize SKILL.md prose).
- **C2: stoa--ezj — PRINCIPAL-intent probe discipline canon** — `MAJOR_PLINY.md` §7.2 extension + `MAJOR_POLYBIUS.md` §4.3.1 relay-time analog + `operating-disciplines.md` §19.2 cross-ref; A9 ε pick (fold-in with explicit 3-step canonical probe sequence: category → shape-within-category → specifics-within-shape).

In-arc M3 Fix-now widening: 7/7 substrate skill SKILL.md files now carry `author: Denson Smith` frontmatter (subsumed stoa--ezp Arc 41 candidate; ezp closed by user-tier as already-resolved). Follow-up filed: stoa--t9u (P3) — install.sh `__pycache__/` exclude (CATO C1 follow-up; shipped Arc 40).

### §13.7 Pass 6 — Arc 40 (Arc 24 follow-ups + Arc 37 bug-fix) — DONE 2026-05-18

Shipped at PR #20 → main `dbb5b81`. Original directive scoped 4 LOCKED candidates + 2 optional fold-in (per SPEC_AUDIT W1 split). Final shipped scope: **3 LOCKED + 2 fold-in = 5 candidates**:

- **C1: stoa--3sz** — `CAPTAIN_VERA.md` §5.11 "Probe-spec regex anchoring discipline" (A6 γ pick).
- **C2: stoa--5sr** — `CAPTAIN_DAEDALUS.md` §6.8 "Canonical-template wording-alignment discipline" (A4 reframed from "Edit-tool worktree-path" after DAEDALUS read agents/design/arc-24/design.md and found the actual empirical anchor was wording-alignment, not Edit-tool mechanics; ARGUS verified as narrows-not-widens).
- **C4: stoa--6wp** [BUG, SEQUENCE-CRITICAL] — `MAJOR_PLINY.md` §5.10 squash-merge `--body` override discipline (A2) + `operating-disciplines.md` §28.3.1 worked-example with bb12806 empirical anchor (A3). **bb12806 regression class structurally closed via Arc 40 ship; downstream-consumed by Arc 41 first.**
- **Fold-in: stoa--6n9** — `install.sh` manifest `# format=v1` header + check.sh/apply.sh reader version-rejection (Arc 38 CATO c3 follow-up).
- **Fold-in: stoa--t9u** — `install.sh` `__pycache__/` exclusion when copying Python substrate skills (Arc 39 CATO C1 follow-up).

**C3 stoa--dhc DROPPED via §25 PRINCIPAL-gate (2026-05-18)**: DAEDALUS surfaced at design-rev1 that substrate already has single-source-of-truth for python-vs-jq rationale at `MAJOR_PLINY.md` §5.8.3; ticket's drift-across-4-sites premise was false against current canon. PRINCIPAL ratified option (a) close-as-already-resolved + strict scope (no narrower-α work). dhc closed by user-tier with cross-ref to merge commit + DAEDALUS finding. Cross-tier round-trip: ~4 min.

Follow-up filed: stoa--mn3 (P3) — Arc 40 + Arc 41 design.md probe-spec defects (5 findings; PLINY-lean α direct-to-main housekeeping). Plus stoa--1lm (P3) substrate-canon extension of §5.11 to DAEDALUS-authored design.md probes.

**A20 recursive-shape held all 3 parts**: PLINY's MAJOR_PLINY.md §5.10 edit committed pre-merge at `453b9e7`; deployed=source verified; PLINY's signoff cites the new §5.10 wording correctly while complying with it. **Self-applied canon held on its own ship-arc.**

### §13.8 Pass 7 — Arc 41 (cross-refs + audits + Arc 36 follow-ups) — DONE 2026-05-18

Shipped at PR #21 → main `6b6fb11`. Original directive scoped 5 candidates; **stoa--ezp absorbed by Arc 39 M3 Fix-now widening** (substrate-tier frontmatter sweep covered the 2-skill scope and 5 others) — closed by user-tier as already-resolved. Final shipped: **4 candidates**:

- **C1: stoa--n2e** — `MAJOR_POLYBIUS.md` line 832 (refusal-as-signal escalation bullet) + line 836 (cross-ref to op-disc §20.3).
- **C2: stoa--58b** — `MAJOR_PLINY.md` lines 140-146 (credential-discipline preamble for dispatch briefs; cite to op-disc §20).
- **C3: stoa--3ml** — `operating-disciplines.md` line 13 (Thesis sentence: §1-§17 → §1-§31; DAEDALUS verified current count at design time).
- **C4: stoa--pqn** — Arc 36 v2 follow-ups landed all 3 items: VERA probe-regex tightening (5 sites in arc-36 design.md per A5 ε in-arc-build), bug #40228 surveillance note at op-disc §11 step 1.5, organic `[from:]` adoption observation as comment on stoa--myd (per A14 hard-lock — NOT canon-promotion).

Follow-up filed: stoa--bn8 (P3) — substrate-canon amendment to MAJOR_PLINY.md §6.2 permitting polling-cron for multi-arc autonomous engagements (proto-canon-promotion evidence from this sequence per stoa--bbi).

**After Pass 7 (Arc 41) ship: zero open P2 substrate-canon tickets at the-stoa.** (Already true pre-Arc-41; ship maintains.) The deferred-with-gating items per §13.9 + the lineage-invocation follow-up `stoa--lyw` (P3 — sequencing flexible) + post-sequence-surfaced tickets per §13.10a (mn3 / sp1 / 1lm / bn8) all stay open without blocking spec-met. The "substrate-canon" boundary = open tickets whose deliverable is a canon change (role file / op-disc section / template / new substrate skill) — explicitly NOT engagement-coordination tickets, pure-documentation tickets (design.md edits in `agents/design/`), or accretion tickets gating on N-evidence.

### §13.9 Deferred-with-gating future-work (2 candidates; satisfies §13.13 criterion 1)

The following tickets stay open without an arc-ship plan; each has explicit gating criteria that trigger arc-ship when the gate fires. Per §13.13 spec-met criterion 1 ("every spec section either describes shipped canon or is explicitly marked future work with filed ticket + gating criteria"), filed-ticket-with-gating-criteria satisfies the spec-met requirement.

**Distinction from §11 anti-pattern "absorbed-by-X closures":** deferral-with-gating has *explicit trigger conditions* + a *filed ticket with a concrete fix-shape* — the discipline-gap is named, the gating criteria are falsifiable, and the next-action is committed. The §11 anti-pattern is closure-or-deferral *without* explicit criteria — "we'll get to it later" with no falsifiable trigger and no concrete fix-shape. The two are structurally distinct: gated-deferral commits to act when the gate fires; absorbed-by-X-closure relinquishes the action entirely. A fresh team should treat the two as different categories — gated-deferral is sanctioned per §13.13 criterion 1; absorbed-by-X-closure is rejected per §11.

- **stoa--tvc** (P3) — bw-fit matrix extension for descendant→ancestor block-edge projection-layer representation (operating-disciplines.md §16 extension). **Gating:** ≥2 ariadne arcs surface the descendant→ancestor empirical need (currently N=1 from factory-demo Phase 6). When the gate fires, file a focused arc directive against operating-disciplines.md §16 extension.
- **stoa--myd** (P4 ACCRETION) — multi-checker convergence framing for operating-disciplines.md §6 gauntlet value. **Gating:** N≥3 four-way convergent findings across future arcs per §6.7.1 canon-promotion gate (currently N=1 from Arc 25; one additional confirming instance noted Arc 40 ARGUS R1 BLOCKING vs user-tier QA independent catch — not yet promoted to N=2 per the specific 4-way convergence requirement).
- **stoa--bbi** (P4 ACCRETION) — substrate-principle refinement (structural fixes converge to a fixed-point, not zero). **Gating:** continuous N-evidence accretion as structural-fix arcs ship; no specific N-threshold; observation-only ticket capturing the refined-principle thesis empirically. Substantial accretion landed during Arcs 39+40+41 (8+ data points across save-verdict self-application + redundant-pair coverage + A20 recursive-shape + cross-tier feedback loop + DAEDALUS-authored-probe gap diagnosis); see ticket comments for sequence-level summary.

### §13.9a Post-sequence-surfaced tickets (filed Arcs 38+39+40+41 + Pass 8 spec-recon; not yet arc-scheduled)

Tickets surfaced during the make-the-team-meet-the-spec sequence that did NOT close in-sequence and have no current arc placement. Distinct from §13.9 (deferred-with-gating) — these have concrete fix-shapes and are queued for a future small-bundle arc OR direct-to-main housekeeping per their individual disposition. Each carries a concrete next-step plan per CLAUDE.md global "Fix known bugs immediately" doctrine.

- **stoa--lyw** (P3) — `/resume` invocation discipline canon (successor-decides-vs-spawn-fresh + stale-id handling). Recording half already mandatory per handoff-author skill step 6 (Arc 37 + Arc 38 R3 fix). Invocation-discipline half is the open work; sufficient for spec-met per §13.14 — fold into future small-bundle arc OR ship standalone post-spec-met.
- **stoa--sp1** (P3) — port 7-8 cross-substrate utility skills into the-stoa substrate (modernize + integrate with check-substrate-updates lifecycle). Filed Arc 38 user-tier QA. NOT a blocker for spec-met / stellation dispatch (Pass 10 fires fresh substrate at a new workspace; cross-substrate skills don't affect it). Arc 43+.
- **stoa--mn3** (P3) — Arc 40 + Arc 41 design.md probe-spec defects (5 findings: m1+m2 from Arc 40 VERA + m_4.5.2+m_4.12.2+m_4.12.3 from Arc 41 VERA). PLINY-lean per ticket body = α direct-to-main housekeeping per §18.1 (design.md edits past their review window; cleanest as housekeeping commit). User-tier handles Pass 8-adjacent.
- **stoa--1lm** (P3) — substrate-canon extension of CAPTAIN_VERA.md §5.11 anchoring discipline to DAEDALUS-authored design.md probes. Filed Pass 8 per DAEDALUS §6.4 (Arc 41 rev2) explicit canon-promotion proposal. Arc 42+ scope (substantive substrate-canon edit; not housekeeping).
- **stoa--bn8** (P3) — substrate-canon amendment to MAJOR_PLINY.md §6.2 permitting polling-cron for multi-arc autonomous engagements. Filed Pass 8 per Arcs 39-41 proto-canon-promotion evidence (the pattern held cleanly across 3 arcs; departs from §6.2 "no cron by default" current canon). Arc 42+ scope.

### §13.10 Pass 8 — Spec accuracy reconciliation (no arc; user-tier housekeeping)

The spec was written 2026-05-17 against the substrate state at that moment. Passes 1-7 shipped new canon. Walk the spec end-to-end against the post-Pass-7 substrate:

- Every §-reference resolves to its current location (line numbers may have shifted).
- Every cited ticket id has the correct status (closed vs open).
- §12 (the structural definitions + queries) is verified consistent with the post-Pass-7 substrate state: the QUERIES in §12.1-§12.4 still return useful answers; the §12.5 dynamic-walk-of-§13 instruction still resolves correctly; reference SHAs in §12.1 still anchor to the intended commits.
- §13.5-§13.10 + §13.14 (which collectively constitute the ticket-placement gap-list per §12.5) reflect post-Pass-7 reality — closed Passes are marked DONE; open candidates have current tickets + scope notes; any newly-surfaced gap not already placed in §13.x gets a fresh ticket + a §13.x bucket assignment. **(Known residue per SPEC_AUDIT_R4 NC8 / stoa--bbi: this enumeration is current-at-authoring-time scope-hint, not authoritative — Pass 8 reconciliation walks §13 dynamically per §12.5's instruction and updates this bullet's enumeration to match. PRINCIPAL accepted the soft-residual per option (b) 2026-05-17.)** **2026-05-18 Pass 8 execution outcome**: §13.5/§13.6/§13.7/§13.8 updated with DONE markers + ship commits + per-arc actual-scope notes (dhc dropped via §25; ezp absorbed by Arc 39); §12.1 reference points extended with Arc 38-41 ships; new §13.9a section added for 5 post-sequence-surfaced tickets (lyw + sp1 + mn3 + 1lm + bn8); stoa--bbi placement formalized in §13.9.
- Any spec section that turned out to be aspirational rather than describing shipped canon either (a) gets revised to match shipped reality, or (b) gets the new ticket filed + cross-referenced as future work.
- **stoa--6k1 handled inline** — Probe P10 spec refinement in `agents/design/arc-25/design.md` only (design-doc edit not substrate-canon edit); user-tier POLYBIUS edits during Pass 8 reconciliation; close on commit.

**Pass 8 execution status**: this Pass executed 2026-05-18 post-Arc-41 ship. The 2026-05-17 spec-audit (R1-R4 cadence) + Arc 38 spec-recon commit consumed some of Pass 8's scope ahead of time; the 2026-05-18 post-sequence pass covered the spec drift accreted during Arcs 38-41. Combined with the §13.9a bucket-placement for newly-surfaced tickets, Pass 8 criterion (§13.13 criterion 1 "every spec claim describes shipped canon OR is explicitly marked future work with filed ticket") is satisfied at sequence-end.

Commit the spec reconciliation as a direct-to-main per §18.1.

### §13.11 Pass 9 — Mechanical-check pass (substrate state matches spec)

Author + run a `validate-spec` skill following the §27 mechanical-script / agent-inspection split pattern. **Note:** the skill does NOT yet exist; the team authors it as part of Pass 9 (build-then-use, not use-existing) using `substrate/skills/check-substrate-updates/` and `substrate/skills/inspect-script-output/` as precedent shapes.

**Mechanical script checks:**
- Every §-reference in SPECIFICATION.md resolves (grep against canon file at named section).
- Every cited `stoa--*` ticket id exists in bw with the claimed status (use `bw list --all` for completeness; CAPTAIN_TIRO per §4.6 is the delegated specialist if available).
- `bw list --status open --all` returns tickets all placed in some §13.x ticket-placing section per the §12.3 + §12.5 dynamic walk (no unplaced tickets surface as §12.x audit findings; the `--all` flag is load-bearing for completeness audits per §4.6 empirical anchor).
- `git status` shows no uncommitted changes except ignorable auto-modified state files (e.g., `.claude/.substrate-last-check`) per §12.4's clean-state definition.
- `_drafts/` is empty OR contains only docs actively in use by an in-flight engagement per §12.4's clean-state definition.
- `check-substrate-updates` skill returns "no drift" across registered consumer workspaces (including user-tier per Arc 38 C2 / stoa--bj5).
- **§28 Co-Authored-By trailers present on post-Arc-35 squash-merge commits, with EXPLICIT CARVE-OUT for `bb12806` (Arc 37 squash-merge).** `bb12806` body carries empty `%(trailers)` due to PLINY's `gh pr merge --body` override defeating GitHub's default trailer-concatenation; this was the empirical anchor for stoa--6wp (Arc 40 C4, shipped 2026-05-18 at dbb5b81), which structurally codified the trailer-preservation discipline at MAJOR_PLINY.md §5.10 + op-disc §28.3.1. The check applies forward-only: commits authored AFTER stoa--6wp fix lands (Arc 40 ship onwards) must carry trailers. `bb12806` is named explicitly as a known historical exception per CLAUDE.md's no-force-push rule (the fix is forward-only by structural necessity, not by deferral). **Post-Arc-40 verification (live-verifiable at Pass 9 time)**: Arc 38 ship `0b5f7f3`, Arc 39 ship `f1f222a`, Arc 40 ship `dbb5b81`, Arc 41 ship `6b6fb11` each carry 10-11 §28 trailers preserved through squash-merge — canon held organically across all 4 downstream consumer arcs.

**Inspection-agent triage:**
- Any check reporting strangeness gets human-readable diagnosis from the inspection agent.
- POLYBIUS triages the diagnoses — fix-now items get fixed; escalations route to PRINCIPAL.

Pass 9 produces an artifact at `agents/observation/spec-validation/mechanical-check-results.md` capturing each check's pass/fail status + evidence trail, including the explicit `bb12806` carve-out attestation.

### §13.12 Pass 10 — Behavioral validation via test-project dispatch

The substrate is now at "spec met" mechanically (§13.2-§13.11 done). The team validates BEHAVIORALLY by dispatching itself against an unrelated test project:

**Test project:** `stellation` (PRINCIPAL ratified the name 2026-05-17) — a React app that displays beadwork tickets in a visually interesting animated way. Specification lives at `docs/validation/stellation-SPECIFICATION.md` (authored at this same time as a paired artifact to this spec). PRINCIPAL may rename if preferred at dispatch time; ratification window stays open through Pass 9 completion.

**Why this validates the substrate:** the test project is brand new + completely unrelated to substrate work + relatively simple in scope. A team can only deliver it well if the substrate disciplines they inherit actually work. The team's ability to:

- Run the arc lifecycle (§5) end-to-end without coaching
- Coordinate via the radio-check + bw-tag conventions (§6 / §7.1 / §7.4 / Arc 36 author tags)
- Self-apply disciplines (§28 trailers; §5.10 signoff; §5.11 paste archival; §19.6 attestation honesty)
- Reject anti-patterns (§11) when they arise organically in the work
- Hand off to PRINCIPAL at the right moments per §13.15 escalation triggers

— is the validation. If the substrate works, the test team ships the test project clean. If the substrate is broken, the test team's friction points surface the breaks.

**Setup steps:**
1. PRINCIPAL creates the test-project repo at `~/claude_projects/stellation/` and copies in the test-project spec.
2. PRINCIPAL runs `the-stoa/substrate/install.sh` from inside the test-project repo to deploy the spec'd substrate.
3. PRINCIPAL spawns fresh POLYBIUS + PLINY sessions at the test-project workspace.
4. The test team operates per their deployed substrate against the test-project spec — semi-autonomous mode; PRINCIPAL exception-handler.

**Observation hooks (the validation evidence):**
- Test-team coordination on bw — does it follow §7 conventions?
- Test-team commit history — do CAPTAIN commits carry §28 trailers? (The stoa--6wp Arc 40 fix should make this reliable for stellation's squash-merges.)
- Test-team signoff comments — do they live-verify per §5.10?
- Test-team paste archival — do they archive per §5.11?
- Test-team escalations — when ambiguity surfaces, does the team surface per §25 PRINCIPAL-gate semantics rather than improvise?
- PRINCIPAL's experience — does the team feel like the team described in this spec, or does it feel like something else?

Pass 10 produces an artifact at `agents/observation/spec-validation/test-dispatch-trail.md` capturing the observation evidence + the substrate-side learnings (any place the test team hit friction that surfaces a spec/canon gap).

If Pass 10 surfaces real substrate gaps, the gaps return to Pass 4-7 (file ticket + ship as Arc 42+) and Pass 9/10 re-run after.

### §13.13 What "meeting the spec" looks like — final definition

The team has met the spec when ALL of:

1. **Substrate-state matches spec** — every claim in this document either describes shipped canon (§13.10 reconciliation done) or is explicitly marked future work with filed ticket + gating criteria (per §13.9 deferred-with-gating).
2. **No deferred-without-plan tickets** — no open P2 at the-stoa is in "awaiting-architectural-decision" or "deferred-without-plan" state.
3. **Working tree clean** — per §12.4's clean-state definition: `_drafts/` is empty or contains only docs for an in-flight engagement; `git status` shows no uncommitted changes except ignorable auto-modified state files; no accumulated cleanup debt.
4. **No substrate drift** — `check-substrate-updates` shows source-canon-and-deployed-instances byte-equal across consumer workspaces (including user-tier post-bj5 ship per Arc 38 C2).
5. **Mechanical-check passes** — Pass 9 produces all-green at `agents/observation/spec-validation/mechanical-check-results.md`, including the `bb12806` carve-out attestation per §13.11.
6. **Behavioral validation passes** — Pass 10 test-project dispatch produces a working `stellation` build that meets its own spec, the test team's observation trail shows substrate disciplines were applied, and PRINCIPAL signs off on the test-dispatch experience as "substrate-as-described."

### §13.14 What's explicitly out of scope for "make-the-team-meet-the-spec"

The fresh team should NOT, while closing the spec gaps:

- Build product features for any non-validation consumer workspace (ariadne, sector-4, railway) — those are post-spec work motions.
- Extend conventions to non-POLYBIUS / non-CAPTAIN seats without explicit scope expansion via fresh ticket + PRINCIPAL ratification.
- Build mechanical enforcement infrastructure (pre-commit hooks, validators, etc.) beyond what existing canon authorizes — the script/agent split (§27) is the model; mechanical infra ships only on documented recurrence.
- Touch the substrate-deploy mechanism (install.sh / apply.sh / revert.sh) beyond what the Pass 4-7 candidates + Pass 10 validation require.
- Build the meta-agent for cross-generation lineage analysis (§10.1 property 3 / §12.5) — out of scope for spec-meeting; framing is described; implementation is post-spec.
- Ship the deferred-with-gating items (stoa--tvc + stoa--myd per §13.9) — they have explicit gating criteria; spec-met is achieved with them open-with-plan.
- Build the `/resume` invocation discipline canon (stoa--lyw per §12.5) before spec-met — the recording half (mandatory at handoff-author SKILL.md step 6) is sufficient for spec-met; the invocation half is operational guidance that can ship in a future arc after Pass 10.

### §13.15 Mode + dispatch

The team operates Passes 1-10 in **semi-autonomous mode** per §7. PRINCIPAL is exception-handler:

- DAEDALUS sub-decisions that hit PRINCIPAL-gate criteria → BLOCK + surface immediately per §25.
- Substance disagreement after one round-trip with peer → surface.
- Authorship / copyright / PRINCIPAL-final-say content → surface.
- End-of-arc clean-PASS for ship/no-ship → surface (Mode 1 ratification at decision points).
- Pass 10 test-dispatch substrate-friction surfaces → surface as soon as observed.

User-tier POLYBIUS QA passes happen at end of EACH arc per the established pattern (per §5.6 — QA pass invitation post-merge; live-verification; signoff with notes-for-the-record; follow-up ticket filing).

### §13.16 Definition of done

The fresh team's job ends when:

- Pass 9 (mechanical-check) shows all-green (including the `bb12806` carve-out attestation).
- Pass 10 (test-project behavioral validation) shows the test team shipped the test project to its spec; observation trail captures the substrate-disciplines-applied evidence.
- A user-tier POLYBIUS QA pass on Pass 10 signs off "substrate-as-described; spec met behaviorally."
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
- **§12 Current state** — does the structural definitions + queries shape match how substrate state should be referenced from this spec? Any contracts in §12.1-§12.4 you want sharpened? Any queries that should be added / removed?
- **§13 Workplan** — is the gap-closure sequence right? Are the per-arc candidate counts sized correctly (Arc 38: 3; Arc 39: 2; Arc 40: 4; Arc 41: 5)?
- **§13.13 Definition of "meeting the spec"** — are the criteria the right ones?

Free-form edits + corrections welcome anywhere. After your edits, the fresh team activates via standard dispatch pattern with this file as primary input.
