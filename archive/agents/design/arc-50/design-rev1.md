# Arc 50 design-rev1 — the enforcement layer, Stage 2 (the judgment tier)

Author: Denson Smith
Ticket: stoa--xyb.7 (parent epic stoa--xyb — the-stoa debloat)
Seat: CAPTAIN_DAEDALUS_the-stoa
Arc: 50 (debloat Arc 7 — BUILD arc, additive enforcement machinery; NOT a cut — no lossless-line-floor)
Worktree branch: arc-50/build (from 2d17a6a — includes all 4 relocation cuts + Stage-1 deterministic hooks)
Design basis: `agents/design/arc-46/design-rev1.md` (Stage-1 design; carries the FULL enforcement-layer design including the Stage-2 components) + the Stage-1 ARGUS verdict `agents/verdicts/stoa--xyb.5/ARGUS-2026-05-23T08-17-31Z.md`

---

## 1. Problem restatement (pre-work gate, §6.1)

Stage 1 (Arc 46) shipped the **deterministic tier** of the enforcement layer: three PreToolUse hard gates + a Stop self-check, source-only, default-OFF, isolation-tested. Those gates carry the load-bearing footguns (author-field, clean-tree-before-branch, no-`-m`-in-bw-comment) on the `permissionDecision:"deny"` channel — a channel the deterministic tier needs because it must fire *before* the action and *independent of the model's compacted context*.

Stage 2 is the **judgment tier**: the part of the enforcement layer that cannot be made fully deterministic because it requires judgment, but whose *trigger* can still be harness-owned. It has four components per the brief:

1. **CAPTAIN_NOMOS** — a ground-truth auditor that checks an ORCHESTRATOR OUTPUT (activation paste, arc-close, commit, directive — the outputs that today have NO independent checker) against bw GROUND TRUTH and returns `CONFORMANT / DIVERGENT / UNVERIFIABLE` with a per-divergence classification that drives re-decompose routing.
2. **PostToolUse-on-Agent checker trigger** — a hook that fires in the PARENT (orchestrator) context when a sub-agent returns and (best-effort) injects the instruction to run NOMOS, with a recursion guard so it never fires NOMOS-on-NOMOS.
3. **bw-ground-truth detection** + the **§7.7 drop-vs-unlock decision** — how NOMOS detects "output diverges from ground truth," and the load-bearing adjudication of whether that detection requires unlocking op-disc §7.7's mechanical-enforcement hard-lock.
4. **re-decompose remediation + 3 guardrails** (size-derail→split vs wrong-spec/blocked/impossible→escalate; attempt-cap N=2; granularity floor) — integrated into `substrate/modules/incomplete-unverifiable-routing.md` (the relocated MAJOR_PLINY §5.6).
5. **SessionStart(matcher:compact) reprime** (Stage-1 ARGUS R2, deferred to Stage 2) — a hook that re-injects engagement context after compaction, since PostCompact is side-effect-only.
6. **install.sh wiring** — NOMOS joins `CAPTAIN_NAMES`; the two new hooks join the candidate `settings-hooks.json` behind `--enable-hooks` DEFAULT-OFF.

The same HARD SAFETY CONSTRAINT as Stage 1 extends here: every component ships as substrate SOURCE; nothing arms a hook in the LIVE session's `settings.json`; NOMOS as a new role file is inert until deployed AND invoked.

**Imported assumptions named at the gate (real briefs have implicit scope):**

- **(A1) The deterministic tier carries the load-bearing footguns; the judgment tier is a backstop, not a guarantee.** Stage 2's mechanisms (NOMOS dispatch via injected instruction, the re-decompose loop) all rest on the orchestrator *acting on* model-facing context, which a derailed orchestrator might not. The design treats Stage 2 as defense-in-depth layered on top of the working deterministic tier, never as the primary enforcement. This is restated as a constraint that shapes the entire web-finding response (§2, §5.2, §9 WP1).
- **(A2) "additionalContext reaches the model" is NOT a safe assumption as of 2026-05-23.** The Stage-1 design and ARGUS verdict both treated PostToolUse `additionalContext` (and, for ARGUS R2, SessionStart(compact) `additionalContext`) as a working injection channel. Live web verification (§2) shows that channel is broken across multiple current versions. This is the single most consequential finding of this design and it reshapes both component 2 and component 5: they are built best-effort on `additionalContext` AND backed by the *working* channels (`permissionDecision:"deny"`, Stop `decision:"block"`+`reason`, and CLAUDE.md / cron).
- **(A3) The §7.7 collision is real and resolves to DROP for a judgment agent — but the reason matters.** ARGUS r1+r2 (load-bearing) named the collision: §7.7 scopes the seat-tag to POLYBIUS-only (PLINY/CAPTAIN outputs are case-4 UNTAGGED by canon), AND §7.7 Future-scope hard-locks the mechanical-enforcement layer "until non-compliance recurs." This design adopts PLINY's lean (DROP the seat-tag canary; NOMOS uses direct bw-state comparison) and argues that a judgment agent reading bw-state does NOT trigger §7.7's hard-lock at all (§5.3). UNLOCK is surfaced as the PRINCIPAL-gated alternative with an explicit recommendation that it is NOT needed.
- **(A4) NOMOS is agent-judgment, not a mechanical skill — but the brief mandates I prove it.** The brief (and the Arc-3 peer ratification) require me to FIRST rule out the LIEUTENANT/skill alternative before committing the seat. §4 does this analysis explicitly and states the call. If that call is wrong, it is a brief-scope question for ARGUS, not a silent design choice.

If any of A1–A4 is wrong, it is a brief bug, not a design bug — flagged for ARGUS (§10).

**Restatement-gate divergence note (§6.1):** my restatement does NOT diverge from the brief's scope, but it RE-WEIGHTS it. The brief leads with NOMOS; the web verification forced the additionalContext-is-broken finding (A2) to the front, because two of the six components (the PostToolUse-on-Agent trigger and the SessionStart-compact reprime) are built on the broken channel. I treat that as the load-bearing design problem and design the others around it. ARGUS should confirm this re-weighting is correct and not a smoothing of the brief's NOMOS-first framing.

---

## 2. Web-verified hook surface (per global rule + Stage-1 "verify at build time")

Verified 2026-05-23 (latest Claude Code version per the changelog: **v2.1.150, 2026-05-23**). The Stage-1 mapping was pulled 2026-05-23 morning; this is the same day but Stage 2 leans on TWO surfaces Stage 1 did not exercise (PostToolUse-on-Agent `additionalContext` in the parent, and SessionStart(matcher:compact) `additionalContext`), so both were re-verified against current docs AND the live issue tracker. **The global rule is exactly for this case: the docs say a channel works; the issue tracker says it is broken in shipping versions. Both questions were asked, in that order.**

Sources read:
- Authoritative capability docs: `https://code.claude.com/docs/en/hooks` + `https://code.claude.com/docs/en/agent-sdk/hooks` (verbatim field tables).
- Changelog (fix-status check): `https://code.claude.com/docs/en/changelog` (latest v2.1.150, 2026-05-23).
- Live issue tracker (the load-bearing check): GitHub `anthropics/claude-code` issues #15174, #19432, #55889, #32026, #5812.

| Behavior Stage 2 rests on | Docs say | Live issue-tracker reality | Verdict for this design |
|---|---|---|---|
| **PostToolUse with matcher `Agent` fires in the PARENT context on sub-agent return** | Docs do not *explicitly* spell out parent-context firing for an `Agent` matcher, BUT the SDK guidance is explicit: *"If you need to inject context into the parent agent after a subagent returns, use a PostToolUse hook on the Agent tool instead"* — i.e. the doc-blessed pattern for parent-context inject-on-return IS PostToolUse-on-Agent. `agent_type` / `agent_id` are populated to identify the returning sub-agent. | The firing itself is not reported broken. SubagentStop confirmed CANNOT inject (validates choosing PostToolUse-on-Agent over SubagentStop, as Stage 1 found). | **Trigger fires — CONFIRMED. But its PAYLOAD channel is the broken one (next row).** |
| **PostToolUse `additionalContext` actually reaches the model** | Docs: *"For PostToolUse hooks, you can set `additionalContext` to append information to the tool result."* Claimed working. | **BROKEN in shipping versions.** Issue #55889 (OPEN, `bug`+`has repro`, v2.1.123, regression from v2.1.9 where it was "added but not actually wired up"): for the Bash matcher, `additionalContext` AND top-level `systemMessage` AND plain stdout are ALL dropped — not injected into model context. Scope is *documented as Bash matcher*; whether the `Agent` matcher is also affected is NOT confirmed either way by the issue. No changelog fix through v2.1.150. Companion: #19432 (PreToolUse additionalContext dropped, Jan 2026). | **DO NOT DEPEND ON IT.** The PostToolUse-on-Agent trigger is built best-effort on `additionalContext`, and its real-reliability backstop is the Stop self-check's working `reason` channel (§5.2). Flagged WP1 (§9). |
| **`permissionDecision:"deny"` + `permissionDecisionReason` reach the model** | Docs: yes. | **CONFIRMED WORKING** even in the broken-injection versions: #55889's reporter explicitly notes *"`permissionDecision:'deny'` blocks commands successfully and `permissionDecisionReason` reaches the model on deny."* This is why the Stage-1 deterministic gates are unaffected by the injection bug — they use `deny`, not `additionalContext`. | **The deterministic tier is SAFE.** Stage 2 leans on this for nothing new, but it confirms the layer's load-bearing footguns still fire. |
| **Stop `decision:"block"` + `reason` reach the model** | Docs: yes (Stop supports top-level `decision`/`reason`, NOT `additionalContext`). | Not reported broken. The Stop block channel is distinct from the additionalContext channel; #55889 is specific to additionalContext/systemMessage/stdout on Pre/PostToolUse. | **WORKING — this is the resilient channel.** The Stage-1 Stop self-check already rides `reason` and already carries a "dispatch NOMOS" reminder (clause A, written to degrade gracefully pre-NOMOS). Stage 2 makes that clause non-vacuous. |
| **SessionStart matcher `compact` injects `additionalContext` after compaction** | Docs: matcher `compact` is supported ("Auto or manual compaction"); SessionStart `additionalContext` is "String added to Claude's context at the start of the conversation." Claimed working. | **BROKEN.** Issue #15174 (closed-as-DUPLICATE, v2.0.72–v2.0.76): SessionStart hooks with the `compact` matcher EXECUTE successfully but their output is **NOT injected into context after compaction completes**. Documented impact: *"Blocks multi-agent orchestration systems that need role reminders."* The issue's own workaround: *"Add reminders directly to CLAUDE.md, which DOES get loaded after compaction."* No changelog fix through v2.1.150. | **DO NOT DEPEND ON IT.** The SessionStart-compact reprime is designed but explicitly marked best-effort, and the *reliable* post-compaction reprime is CLAUDE.md + cron (§5.5). This materially changes ARGUS R2's premise — see §5.5 + WP2 (§9). |
| **PostCompact event (instant post-compaction reprime)** | Docs: PostCompact exists, "After context compaction completes... No decision control" — side-effect-only, cannot inject. | Issue #32026 is a *feature request* for a more capable PostCompact hook — i.e. the community wants what does not exist. Confirms PostCompact cannot carry the reprime. | **Unchanged from Stage 1 (ARGUS r3 correction holds): PostCompact cannot inject; route the reprime elsewhere.** |

**The synthesis that governs this design.** As of 2026-05-23 (v2.1.150), the `deny` and Stop-`block` channels work; the `additionalContext` injection channel is broken across multiple current versions with no shipped fix. Stage 1 is unaffected (it uses `deny`). Stage 2's two new hook payloads (PostToolUse-on-Agent and SessionStart-compact) BOTH ride the broken `additionalContext` channel. Therefore the design's load-bearing rule is: **build the additionalContext payloads (they are correct and will start working when the platform fixes the bug — forward-compatible), but make every Stage-2 behavior that MUST happen rest on a working channel (Stop `reason`, CLAUDE.md, cron, or the orchestrator's standing role-prompt) instead.** This is defense-in-depth applied to a platform bug, not a workaround that pretends the bug away.

**Doc URLs (citation trail):**
- `https://code.claude.com/docs/en/hooks` (matcher table; SessionStart additionalContext field; PostToolUse fields)
- `https://code.claude.com/docs/en/agent-sdk/hooks` (PostToolUse-on-Agent parent-inject guidance; agent_type/agent_id)
- `https://code.claude.com/docs/en/changelog` (latest v2.1.150 2026-05-23; no additionalContext-injection fix found)
- Issue #55889 (PostToolUse/PreToolUse additionalContext dropped, OPEN, v2.1.123)
- Issue #15174 (SessionStart compact not injected, closed-as-dup, v2.0.72–76)
- Issue #19432 (PreToolUse additionalContext dropped)
- Issue #32026 (PostCompact feature request — confirms PostCompact can't inject)

---

## 3. Approach — overall shape

Stage 2 adds the judgment tier on top of Stage 1's deterministic tier. Three structural moves:

1. **A new leaf CAPTAIN (NOMOS) that audits orchestrator outputs against bw ground truth.** It is the redundant-checker property the gauntlet already has for *deliverables* (VERA/CATO/ARGUS for diffs/builds/plans), extended to *orchestrator outputs* (activation pastes, arc-closes, commits, directives) which previously had no independent checker. NOMOS is audit-only (no Write/Edit/Agent/Web), mirroring VERA's independence-of-verification discipline.

2. **Harness-fired triggers that REMIND the orchestrator to dispatch NOMOS — built on two channels, one best-effort and one reliable.** The best-effort channel is PostToolUse-on-Agent `additionalContext` (correct, forward-compatible, currently broken per §2). The reliable channel is the Stage-1 Stop self-check `reason` (working today). The reminder rides both so it survives the platform bug.

3. **A re-decompose remediation loop with three guardrails, integrated into the existing INCOMPLETE/UNVERIFIABLE routing module** rather than bolted on as a parallel path. NOMOS's `DIVERGENT` verdict carries a per-divergence `classification` that the orchestrator routes on (split vs escalate).

Everything ships as substrate SOURCE:

```
substrate/
  CAPTAIN_NOMOS.md                                # NEW — the 12th CAPTAIN (authored slim from the start)
  hooks/
    posttooluse-agent-checker-trigger.sh          # NEW — best-effort NOMOS-dispatch reminder + recursion guard
    sessionstart-compact-reprime.sh               # NEW — best-effort post-compaction reprime
    stop-self-check.sh                             # MODIFIED — clause A made non-vacuous (NOMOS now exists)
    README.md                                      # MODIFIED — document the two new hooks + the additionalContext-bug caveat
  templates/
    settings-hooks.json                            # MODIFIED — add PostToolUse-on-Agent + SessionStart-compact registrations
  modules/
    incomplete-unverifiable-routing.md             # MODIFIED — add the DIVERGENT branch + the 3 guardrails
  install.sh                                        # MODIFIED — NOMOS in CAPTAIN_NAMES; "11 envelopes" -> "12"
```

**Nothing writes the live session's settings.json.** The two new hooks deploy as inert scripts + candidate registrations behind `--enable-hooks` (default OFF), exactly like Stage 1 (§8).

---

## 4. Component 1 prerequisite: is NOMOS a CAPTAIN, or a LIEUTENANT skill? (the hard pre-req)

The brief (and the Arc-3 peer ratification) require this analysis BEFORE committing the seat. The question: is ground-truth-checking **agent-judgment** (→ a CAPTAIN) or **mechanical** (→ a LIEUTENANT skill + orchestrator judgment)?

### 4.1 What the substrate distinguishes

The substrate has a clean three-way taxonomy (`substrate/skills/agent-author/SKILL.md` `agent_type`):
- **MAJOR** — PRINCIPAL-facing, substantive, reusable across sessions.
- **CAPTAIN** — a sub-agent dispatched one-shot for a task that requires *judgment* and runs in its own context window with its own tools (the gauntlet seats: design, critique, build, verify, review).
- **LIEUTENANT skill** — a *mechanical* helper: a deterministic procedure (a script, a checklist, a parser) invoked in-context, no separate context window, no independent judgment. Examples on disk: `validate-spec` (a parser), `save-verdict` (a file-writer), `check-bw-release` (a version check), `inspect-script-output`.

The dividing line is **judgment vs mechanism**. A skill is the right home when the task is a deterministic transform with a single correct output. A CAPTAIN is the right home when the task requires assessing, weighing, and classifying — when two competent runs could reasonably produce different (but defensible) outputs and the value is in the assessment.

### 4.2 The decomposition of NOMOS's job

NOMOS's job has two parts, and they fall on opposite sides of the line:

| Sub-task | Judgment or mechanism? | Could be a skill? |
|---|---|---|
| **Parse a bw timeline / `git log` / ticket state and extract facts** (what does the ticket actually say; what SHA was actually committed; what cleanup actually happened) | MECHANICAL — deterministic reads, single correct answer | YES — this part is skill-shaped |
| **Decide whether the orchestrator's CLAIM diverges from those facts, and how severely** (is "VERA returned PASS" a divergence when the ticket carries no PASS comment? is a missing seat-trailer a divergence or an accepted exception? does this divergence read as a size-derail or a wrong-spec?) | JUDGMENT — requires interpreting intent, weighing severity, classifying cause | NO — this is the assessment a skill cannot make |
| **Classify each divergence into SIZE-DERAIL / WRONG-SPEC / BLOCKED / IMPOSSIBLE** (the field that drives re-decompose routing) | JUDGMENT — the same divergence (a unit failed to complete) routes to *split* if it's a size-derail and to *escalate* if it's wrong-spec; only judgment distinguishes them | NO — this is the load-bearing judgment the whole remediation loop depends on |

The first row is skill-shaped. The second and third are not. **The re-decompose routing the brief requires (distinguish size-derail→split from wrong-spec/blocked/impossible→escalate; assess divergence severity) is precisely the judgment a mechanical skill cannot make.** A skill can grep for a missing tag; it cannot decide whether a missing tag *means* the orchestrator derailed or *means* a legitimate case-4 untagged PLINY comment (which §7.7 says is correct). That decision is interpretation, and getting it wrong sends the remediation loop down the wrong branch (splitting a wrong-spec task infinitely, or escalating a trivially-splittable size-derail to the PRINCIPAL needlessly).

### 4.3 The call: NOMOS is a CAPTAIN. Justification.

**NOMOS is a CAPTAIN.** Three reasons, in priority order:

1. **The load-bearing output is a judgment, not a transform.** The `classification` field that drives §5.4 routing is an assessment of *cause* (why did this diverge), which two competent auditors could weigh differently and which no deterministic rule produces. That is the definition of a CAPTAIN-shaped task.

2. **Independence-of-checking requires a separate context window.** NOMOS audits the orchestrator's output. If the check ran in-context as a skill the *orchestrator itself* invoked, it would be self-check, not cross-check — and the whole premise (stoa--xyb.5: a derailed orchestrator cannot reliably self-detect its own derailment) collapses. A CAPTAIN runs in its OWN context, dispatched by the orchestrator but reasoning independently of the orchestrator's (possibly compacted, possibly derailed) context. A skill cannot give that independence. This is the same reason VERA is a CAPTAIN and not a skill the builder runs on itself.

3. **One-job-per-agent argues for a distinct seat.** NOMOS's *subject* (orchestrator outputs — pastes, closes, directives) differs from every existing checker's subject (VERA: builds; CATO: diffs; ARGUS: plans; ZENO: static analysis). Folding orchestrator-output-auditing into CATO or ARGUS overloads a seat with a second job and a second subject. The seat-count cost (12th CAPTAIN) is real but is the correct cost of the one-job discipline.

**The skill-shaped part is NOT discarded — it is INSIDE NOMOS.** NOMOS's mechanical fact-extraction (parse the ticket, read the SHA, diff claimed-vs-actual) uses the same deterministic Bash/Grep operations a skill would. NOMOS is "a CAPTAIN whose first move is mechanical fact-gathering, whose load-bearing output is the judgment on top of those facts." This is exactly VERA's shape (mechanical probe execution → judgment verdict). We do NOT additionally author a separate LIEUTENANT skill for the fact-extraction: it would add a deploy artifact and a hand-off boundary for no gain, since NOMOS already has Bash/Read/Grep/Glob and the fact-extraction is a handful of commands inline. **If a future arc finds the fact-extraction is reused outside NOMOS, extracting it to a skill is a clean follow-up — noted out-of-scope (§11).**

### 4.4 CAPTAIN_NOMOS — the seat (authored slim from the start; NOT a cut target)

Per the agent-author conventions (`substrate/skills/agent-author/SKILL.md`) and voice-discipline (PRINCIPAL/HUMAN throughout, no COLONEL leakage, no second-person-as-instruction drift). The relocation cuts (Arcs 44–49) slimmed the EXISTING role files; NOMOS is authored slim from day one — it carries only the core seat sections, with CONDITIONAL detail cited to modules/op-disc rather than inlined.

| Field | Value |
|---|---|
| **Mnemonic** | NOMOS (Greek *nomos*, "law / that which is laid down as binding" — the seat checks output against the laid-down ground truth) |
| **Rank** | CAPTAIN |
| **Descriptive role** | GROUND-TRUTH AUDITOR |
| **Name (frontmatter)** | `CAPTAIN_NOMOS{{NAME_SUFFIX}}` |
| **description (frontmatter)** | "Ground-truth auditor; checks an orchestrator output (activation paste, arc-close, commit, directive) against bw ground truth and the repo, returns CONFORMANT / DIVERGENT / UNVERIFIABLE with a per-divergence classification that drives re-decompose routing." |
| **tools** | `Bash, Read, Grep, Glob` — NO `Write`/`Edit` (audit-only, mirrors VERA's independence discipline); NO `Agent` (a leaf, cannot nest — finding stoa--xyb.2#4); NO `WebSearch`/`WebFetch` (its ground truth is bw + the repo, not the web) |
| **model** | opus |
| **Lives at** | `.claude/agents/CAPTAIN_NOMOS{{NAME_SUFFIX}}.md` |
| **Activation** | dispatched one-shot by the orchestrator (PLINY / POLYBIUS) — NOT by a hook (hooks can't dispatch sub-agents), NOT by another CAPTAIN (can't-nest) |

**The role file's section skeleton** (ADA builds this; structural shape mirrors CAPTAIN_VERA.md, the closest audit-only sibling):

- **§1 Your one job** — check an orchestrator output against bw ground truth; return a conformance verdict. Cross-check, not self-check. Frame against the gauntlet: VERA checks builds, CATO checks diffs, ARGUS checks plans, NOMOS checks *orchestrator outputs* (the seat that had no checker).
- **§2 The brief you receive** — the output to audit (paste / close / commit / directive + its text), the bw ticket id(s) it makes claims about, and the operating-mode flag. If the output makes no checkable claim against bw, return `UNVERIFIABLE` with the reason, not a fake CONFORMANT.
- **§3 What you check (the conformance probes)** — §4.5 below.
- **§4 What you write** — NOTHING to the repo (audit-only). The verdict is the dispatch return + a bw breadcrumb comment on the ticket. Independence: NOMOS never edits the output it audits, never patches bw to make a claim true.
- **§5 Voice** — workmanlike auditor; report divergences without proposing fixes (proposing fixes is the orchestrator's re-decompose job, §5.4). State what the ground truth IS and how the claim diverges; do not editorialize.
- **§6 Disciplines** — leaf-seat heartbeat-and-read-before-write via bw (the CAPTAIN comm contract); fail-honest (UNVERIFIABLE when bw ground truth is insufficient, never a manufactured verdict); cite-the-ground-truth (every divergence names the exact `bw show <id>` / `git` evidence). These reference op-disc/modules rather than re-inlining.
- **§7 Verdict format** — §4.6 below.
- **§8 Authorship attribution** (immutable) — standard CAPTAIN block.

### 4.5 What NOMOS checks (the conformance probes)

NOMOS's audit is the bw-ground-truth detection (component 3). Per stoa--xyb.5: do NOT try to detect "compaction happened"; detect "output diverges from bw ground truth" — the checking layer IS the derailment detector (a derailed agent produces non-conforming output regardless of cause). Detection is external + comparison-based against the durable record (a derailed agent cannot self-detect).

The probes, in the **DROP** design (direct bw-state comparison; §5.3 explains why this is the right call vs the seat-tag canary):

1. **Ticket-state consistency.** The output's claims about ticket state (closed / blocked / verdict received) match `bw show <id>` ground truth. *Worked example:* an arc-close paste that says "VERA returned PASS" when the ticket carries no PASS verdict comment = DIVERGENT.
2. **Commit-SHA / claimed-vs-actual.** Claims of the form "PR #N squash-merged <SHA>", "branch deleted", "main == origin/main @ <SHA>" are checked against `git log` / `git rev-parse` / `git ls-remote` ground truth. *Worked example:* an arc-close claiming "worktree de-registered + orphan dir cleared" when `git worktree list` still shows the worktree = DIVERGENT.
3. **Claimed-cleanup verification.** Claims of remediation/cleanup (the stoa--501 Arc-26 anchor: an unauthorized sector-4 mutation claimed cleaned) are verified against actual repo/bw state, not taken on the orchestrator's word.
4. **PRINCIPAL-gate conformance (op-disc §25).** If the output crosses a PRINCIPAL-gating clause, ratification evidence exists in the bw record; else flag (this is the §25.3 gate-shape NOMOS audits at output time, the catch-point complement to DAEDALUS's design-time gate).

Each probe is mechanical fact-extraction (the skill-shaped part, §4.2) followed by the divergence judgment (the CAPTAIN-shaped part). The seat-tag canary is **explicitly NOT a NOMOS probe** (§5.3 — it would key on a POLYBIUS-only convention against untagged PLINY/CAPTAIN outputs, which is the ARGUS r1 mis-scope, and it is the hard-locked mechanical layer of ARGUS r2).

### 4.6 NOMOS verdict shape (consumed by the orchestrator + §5.4 routing)

```
verdict: <CONFORMANT | DIVERGENT | UNVERIFIABLE>
checked_output: <what was audited — the paste/close/commit/directive + its bw ticket id(s)>
divergences:
- type: <ticket-state | commit-sha | claimed-cleanup | principal-gate>
  detail: <one line: what the output claimed vs what bw/git ground truth shows>
  evidence: <the exact command(s) run + their output — bw show <id> / git rev-parse / git worktree list>
  classification: <SIZE-DERAIL | WRONG-SPEC | BLOCKED | IMPOSSIBLE>   # drives §5.4 routing
ground_truth_consulted: <bw ticket ids + git refs + commands run>
summary: <one paragraph: what was audited, what diverged, the load-bearing divergence if any>
```

- **CONFORMANT** → output may propagate.
- **DIVERGENT** → do NOT propagate; route per §5.4. Each divergence carries a `classification` (produced AT the checker, with the checker's evidence) so the orchestrator routes correctly — guardrail 1 of §5.4.
- **UNVERIFIABLE** → bw ground truth insufficient to decide; surfaces to operator (slots into the INCOMPLETE/UNVERIFIABLE routing module, §5.4).

---

## 5. The Stage-2 components in detail

### 5.1 (covered above) CAPTAIN_NOMOS — §4.

### 5.2 PostToolUse-on-Agent checker trigger — `posttooluse-agent-checker-trigger.sh`

Registered under `"PostToolUse"` with matcher `"Agent"`. Fires in the PARENT (orchestrator) context when a sub-agent returns (the doc-blessed parent-inject-on-return pattern, §2).

- **Behavior (best-effort):** emits `additionalContext` carrying the self-contained instruction to run NOMOS against the returned sub-agent's output. The payload obeys op-disc §34 (WHY it fired + WHAT to do, inline, no bare pointer):

  > "A sub-agent just returned. Per the cross-check discipline (orchestrator outputs and the propagation of sub-agent verdicts have no other independent checker), before you act on or propagate this sub-agent's output against bw, dispatch CAPTAIN_NOMOS with the returned verdict + the relevant bw ticket id(s) and have it confirm the output conforms to bw ground truth (ticket-state consistency, claimed-vs-actual commit SHAs, claimed cleanup, PRINCIPAL-gate evidence). If NOMOS returns DIVERGENT, do not propagate — route per the re-decompose remediation in `incomplete-unverifiable-routing.md`. This hook cannot dispatch NOMOS for you (hooks cannot dispatch sub-agents); you must issue the dispatch yourself."

- **THE CRITICAL CAVEAT (web finding, §2 / A2):** as of v2.1.150, PostToolUse `additionalContext` is **broken** (#55889) — it may not reach the model. **Therefore this hook is best-effort and is NOT the reliable carrier of the NOMOS reminder.** The reliable carrier is the Stage-1 **Stop self-check** (`decision:"block"`+`reason`, a working channel), whose clause A already says "the ground-truth checker (CAPTAIN_NOMOS) has been or is being dispatched against that orchestrator output." Stage 2 makes that clause non-vacuous (NOMOS now exists). So the design's actual guarantee is: *the Stop self-check (working channel) reminds the orchestrator to dispatch NOMOS at turn-end; the PostToolUse-on-Agent hook (best-effort channel) reminds it earlier, at sub-agent return, IF the platform injection bug is fixed.* The two together are forward-compatible and degrade gracefully to the working channel today. This is flagged WP1 (§9).

- **Recursion guard (designed-around the §2 uncertainty):** the hook must NOT fire the "run NOMOS" instruction when the sub-agent that just returned IS NOMOS itself (else NOMOS-checks-NOMOS loop). Primary mechanism: inspect the event's `agent_type` field (populated to identify the returning sub-agent per §2) for the NOMOS seat name (`CAPTAIN_NOMOS*`, case-insensitive, `{{NAME_SUFFIX}}`-tolerant) and no-op (allow, no additionalContext) on a match. **Fallback (because §2 could not CONFIRM the parent-context event reliably carries the returned agent's name):** a one-deep sentinel keyed on the session id (mirroring the Stage-1 Stop sentinel idiom) — if a NOMOS dispatch is in flight, suppress re-firing. ARGUS r5 (Stage 1) flagged exactly this uncertainty; the fallback is the mitigation. Flagged WP3 (§9).

- **Fail-OPEN** on script error (no python3, malformed event, missing field) — emit nothing, allow — consistent with the Stage-1 contract. A best-effort reminder that fails open simply does not remind; the Stop channel still does.

### 5.3 bw-ground-truth detection + the §7.7 DECISION (the load-bearing adjudication)

**The decision: DROP the seat-tag canary. NOMOS uses direct bw-STATE comparison (§4.5). NO §7.7 unlock is needed. UNLOCK is surfaced below as the PRINCIPAL-gated alternative and is NOT recommended.**

**The collision, restated (ARGUS Stage-1 r1 + r2, both load-bearing).** The Stage-1 design proposed the §7.7 seat-tag as NOMOS's primary canary. ARGUS found two collisions:
- **r1:** the seat-tag is **POLYBIUS-only by canon** (`operating-disciplines.md` §7.7 scope / `two-polybius-coordination.md` §7.7: "PLINY, CAPTAINs, and pair-programmer Majors are NOT required to author-tag"). But NOMOS audits **orchestrator (PLINY) outputs**, which are **case-4 UNTAGGED by canon**. Keying the primary canary on a tag that PLINY outputs are not required to carry would flag *correct* PLINY outputs as divergent — a false-positive generator.
- **r2:** the §7.7 **Future scope** paragraph **hard-locks** the mechanical-enforcement layer: *"The mechanical-enforcement layer (pre-comment hook, CI lint) is also hard-locked OUT per A14 — mechanical enforcement is a future arc IF non-compliance recurs."* A seat-tag canary (a mechanical pre-comment/parse check on the tag convention) IS that hard-locked layer.

**Why DROP is correct, and why it does not even touch the hard-lock.** The §7.7 hard-lock targets a specific thing: **mechanical enforcement OF THE SEAT-TAG CONVENTION** (a pre-comment hook or CI lint that mechanically checks tag presence/correctness). NOMOS in the DROP design does something categorically different:
- It does **not check the seat-tag convention at all** — it never greps for `[from: ...]` tags, never enforces tag presence, never extends the convention to PLINY/CAPTAIN outputs.
- It checks **bw STATE** — does the output's CLAIM about a ticket/commit/cleanup match the durable ground truth. That is a JUDGMENT agent reading the durable record and comparing facts, NOT a mechanical lint on a coordination convention.

So the §7.7 hard-lock is **not triggered** by the DROP design, on two independent grounds:
1. **Subject:** the hard-lock is about the seat-tag *convention*; NOMOS-DROP never touches the seat-tag convention.
2. **Mechanism:** the hard-lock is about *mechanical* enforcement (pre-comment hook, CI lint — deterministic, no judgment); NOMOS is a *judgment* agent (a CAPTAIN, §4), and op-disc §27's "mechanical-narrow + agent-inspection" pattern (cited in §7.7 itself) explicitly distinguishes agent-inspection from mechanical enforcement and treats agent-inspection as the *permitted* form alongside prose canon. NOMOS is agent-inspection, which §7.7 itself blesses; it is not the mechanical layer §7.7 locks.

**Therefore: no PRINCIPAL §7.7-unlock is required.** PLINY's lean (DROP) is not just expedient — it is the structurally correct reading. The DROP design routes *around* the collision rather than through it.

**The UNLOCK alternative (surfaced for PLINY/PRINCIPAL routing; NOT recommended).** UNLOCK would mean: treat this epic as the "non-compliance recurs" trigger, revise §7.7 to (a) extend the tag convention to PLINY/CAPTAIN outputs and (b) permit the mechanical seat-tag canary. This is PRINCIPAL-gated (it edits a hard-locked canon clause). I do **not** recommend it, because:
- It is strictly MORE than the job needs. bw-state comparison (DROP) detects every divergence the seat-tag would (a derailed orchestrator producing a wrong claim is caught by comparing the claim to ground truth) AND more (the seat-tag only catches *tagging* drift; bw-state catches *content* drift, which is the actual derailment signal).
- The seat-tag carries NOTHING bw-state cannot. The seat-tag's value is timeline-arithmetic attribution for POLYBIUS coordination (the e39 anchor) — a different job from auditing whether an orchestrator output is truthful. NOMOS does not need the tag for its job.
- It edits a PRINCIPAL-ratified hard-lock for no marginal detection gain — a bad trade.

**The explicit routing handle for PLINY (per the brief):** DROP needs no PRINCIPAL gate and ships clean on verification. The ONLY thing that would warrant surfacing to PRINCIPAL is if a concrete reason emerged that the seat-tag carries something bw-state cannot — I find none. PLINY can route this as DROP-no-gate.

### 5.4 re-decompose remediation + 3 guardrails (integrated into `incomplete-unverifiable-routing.md`)

When NOMOS returns DIVERGENT (or VERA returns INCOMPLETE/UNVERIFIABLE), the orchestrator remediates by **re-decomposing the failed unit into smaller pieces and re-dispatching** (an orchestrator job — can't-nest). Compaction-derailment correlates with task size; small-enough tasks never compact, so splitting both fixes this instance AND tunes granularity for next time (the reaction teaches the prevention — stoa--xyb.5). bw-as-memory makes fine decomposition cheap (state is read from bw, not carried in-head, so splits don't fragment context).

**The three guardrails (all load-bearing — without them the loop diverges):**

1. **Distinguish size-derail from wrong-spec/blocked/impossible.** Only a SIZE-DERAIL divergence is split. WRONG-SPEC / BLOCKED / IMPOSSIBLE divergences are ESCALATED, never split (splitting a wrong-spec task infinitely subdivides a task that can never pass). The classification is produced by NOMOS (§4.6 `classification` field) so the routing decision is made WITH the checker's evidence, not guessed by the orchestrator. This is why NOMOS must be a judgment agent (§4.3): the classification is the judgment.

2. **Attempt cap → escalate to PRINCIPAL.** A unit may be re-decomposed at most **N=2** times (configurable; default 2). On the 3rd divergence of the same unit lineage, the orchestrator STOPS splitting and escalates to PRINCIPAL via POLYBIUS. **Robustness against the orchestrator's own compaction (Stage-1 ARGUS R4):** the count is tracked on the unit's bw ticket as an explicit comment (`[re-decompose attempt: k/2 — lineage <root-ticket-id>]`) so it survives the orchestrator's compaction (the count is in bw, not in-head). To harden the read+increment step itself (which a derailed orchestrator could botch — ARGUS R4's deeper concern), the count is **re-derived, not remembered**: before each split the orchestrator COUNTS the existing `[re-decompose attempt:...]` comments for that lineage on the ticket (a bw read, not a remembered integer), so a mis-incremented or skipped write self-corrects on the next read rather than compounding. If the count read itself is UNVERIFIABLE (ticket unreadable), the orchestrator escalates rather than splits (fail-toward-escalation, the safe direction — escalation surfaces to a human; over-splitting does not).

3. **Granularity floor.** A unit is not split below the point where handoff/coordination overhead exceeds the work (default floor: a unit whose own dispatch brief + verdict would be longer than the work it describes). At the floor, escalate instead of split.

**Integration into the module (the relocated MAJOR_PLINY §5.6 — now `substrate/modules/incomplete-unverifiable-routing.md`).** The module today routes verifier INCOMPLETE/UNVERIFIABLE to operator disposition. This arc ADDS a new branch for NOMOS's DIVERGENT, placed alongside the existing INCOMPLETE/UNVERIFIABLE branches:

> **DIVERGENT verdict received (from CAPTAIN_NOMOS).**
> - PLINY reads the `classification` of each divergence in the NOMOS verdict.
> - **SIZE-DERAIL** divergences → re-decompose the failed unit (guardrail 1); before splitting, COUNT the existing `[re-decompose attempt:...]` comments for this unit's lineage on its bw ticket (guardrail 2 — re-derive, don't remember); if the count is already ≥ the cap (default 2) OR the unit is at the granularity floor (guardrail 3) OR the count read is UNVERIFIABLE, ESCALATE to PRINCIPAL via POLYBIUS instead of splitting. Otherwise split, re-dispatch, and post a fresh `[re-decompose attempt: k/2 — lineage <root>]` comment.
> - **WRONG-SPEC / BLOCKED / IMPOSSIBLE** divergences → do NOT split; surface to POLYBIUS → PRINCIPAL (the same operator-disposition path as INCOMPLETE/UNVERIFIABLE).
> - DIVERGENT does NOT gate merge autonomously (consistent with the INCOMPLETE/UNVERIFIABLE A6 LOCK in this module); it routes through operator judgment.

This keeps the new remediation INSIDE the existing verdict-routing protocol rather than bolting on a parallel path. The module's existing cross-refs (op-disc §15; the verifier seats' quadrant disciplines) are preserved; a NOMOS cross-ref is added (`CAPTAIN_NOMOS.md` §4/§7 for the verdict shape + classification field).

### 5.5 SessionStart(matcher:compact) reprime — `sessionstart-compact-reprime.sh` (Stage-1 ARGUS R2)

Registered under `"SessionStart"` with matcher `"compact"`. Stage-1 ARGUS R2 asked whether Stage 1 should add this reprime; the design deferred it to Stage 2. Here it is — **but the web finding (§2) materially changes ARGUS R2's premise.**

- **Intended behavior:** on a compact-triggered session resume, inject `additionalContext` re-priming the orchestrator with its standing engagement context (its seat, the open epic, the polling cadence, the "dispatch NOMOS on orchestrator outputs" reminder). The payload obeys op-disc §34 (self-contained inline). The actual engagement-specific content is read from a deployed reprime config (e.g. `.claude/hooks/reprime-context` if present) so the payload is not hard-coded to one engagement; absent the config it injects a generic role-reprime.

- **THE LOAD-BEARING CAVEAT (web finding, §2):** SessionStart(matcher:compact) `additionalContext` is **broken** (#15174, closed-as-duplicate, v2.0.72–76, no changelog fix through v2.1.150): the hook EXECUTES but its output is **NOT injected into context after compaction.** The issue's own documented impact is *"Blocks multi-agent orchestration systems that need role reminders"* — i.e. exactly this use case. **So this hook, AS DESIGNED, does not reliably do its job on current versions.** The design ships it anyway, for two reasons: (a) it is the CORRECT mechanism and is forward-compatible (it starts working the moment the platform fixes #15174); (b) it is harmless when broken (executes, output dropped, no side effect). But the design must NOT claim it as the post-compaction reprime guarantee.

- **The RELIABLE post-compaction reprime is CLAUDE.md + cron** — not this hook. The #15174 issue itself names the workaround: *"Add reminders directly to CLAUDE.md, which DOES get loaded after compaction."* The Stoa already has both reliable carriers:
  1. **CLAUDE.md / role-prompt:** the orchestrator's standing role file (loaded after compaction) carries its seat identity and the dispatch protocol. This is the platform-blessed post-compaction carrier.
  2. **The polling cron** (`substrate/templates/polling-cron-prompt-template.md`): a standing cron prompt is *fresh harness-fired input re-injected after the wipe* (the stoa--xyb.5 founding principle) — it survives compaction by construction, on a working channel (a prompt, not a hook additionalContext). The cron is the reliable standing reprime.

- **Design position (revising ARGUS R2's implicit premise):** the SessionStart-compact hook is shipped as a **best-effort, forward-compatible** reprime, NOT as the reprime guarantee. The guarantee lives in CLAUDE.md + cron. ARGUS R2 asked "should Stage 1 add SessionStart-compact?"; the honest Stage-2 answer is "yes, ship it, but know it is currently broken upstream and the real reprime is cron + CLAUDE.md." Flagged WP2 (§9). **ARGUS should weigh whether shipping a currently-broken-upstream hook is worth it vs. waiting for the platform fix** (my position: ship it — it is harmless when broken and forward-compatible, and shipping it documents the dependency so a future arc notices when #15174 closes).

- **Fail-OPEN / safe:** SessionStart hooks "run on every session, so keep them fast" (docs). The script is a fast read-config-and-emit; on any error it emits nothing (no reprime, no harm). It NEVER blocks session start.

### 5.6 install.sh wiring + canon touch-ups

**(a) Deploy CAPTAIN_NOMOS.** Add `NOMOS` to the `CAPTAIN_NAMES` array (`substrate/install.sh` ~L177). The existing CAPTAIN deploy loop (both the dry-run plan-line and the deploy loop) then covers it with ZERO new code — NOMOS deploys exactly like the other 11 CAPTAINs via the `WITH_CAPTAINS`-gated loop. Update the "11 envelopes" string in the dry-run plan echo (~L762) to "12".

**HEED THE ARC-6 RECOMPOSE LESSON (brief + Arc-6 CATO/ZENO BLOCKING):** Arc 6 found that a recompose call gated on `TARGET=subproject` but NOT on `WITH_CAPTAINS` broke `--target subproject --no-captains` (recompose hit a never-written file → exit 2 + partial deploy). **NOMOS is authored slim and relocates NOTHING** (no module extraction — its CONDITIONAL detail cites existing modules/op-disc, it does not own new modules). So NOMOS adds **no recompose call** and cannot reintroduce that failure mode. The probe-set MUST still include `--no-captains` (P11) to confirm NOMOS's addition did not perturb the no-captains path. This is a deliberate non-action: NOMOS does NOT join the owned-set partition (it owns no modules), so the 4-owner recompose machinery (POLYBIUS+op-disc+PLINY+DAEDALUS) is UNCHANGED.

**(b) Deploy the two new hooks.** They glob-deploy automatically via the existing `substrate/hooks/*.sh` deploy loop (`posttooluse-agent-checker-trigger.sh` + `sessionstart-compact-reprime.sh` are gate scripts → chmod +x; no new install.sh code needed — the glob already covers them). The modified `stop-self-check.sh` and `README.md` redeploy in place.

**(c) Register the two new hooks in the candidate `settings-hooks.json`.** Add two registration blocks to `substrate/templates/settings-hooks.json` (the CANDIDATE template — NOT the live settings.json):
```json
"PostToolUse": [
  { "matcher": "Agent",
    "hooks": [ { "type": "command", "command": "{{HOOKS_DIR}}/posttooluse-agent-checker-trigger.sh", "timeout": 30 } ] }
],
"SessionStart": [
  { "matcher": "compact",
    "hooks": [ { "type": "command", "command": "{{HOOKS_DIR}}/sessionstart-compact-reprime.sh", "timeout": 10 } ] }
]
```
The `{{HOOKS_DIR}}` slot is sed-substituted at `--enable-hooks` time exactly as the Stage-1 PreToolUse/Stop registrations are. **CRITICAL SAFETY:** this is a candidate-template edit; the live settings.json is never written by any Stoa arc (§8). The new registrations are armed only by the operator-gated, default-OFF `--enable-hooks` path, never by a routine install or any build in this arc.

**(d) Canon touch-ups (minimal — Stage 2 does NOT add a new always-loaded rule).** Op-disc §34 (the trigger-payload authoring rule) already covers the two new payloads (it enumerates `additionalContext` and applies to "every harness-owned trigger payload"). The detail home `substrate/hooks/README.md` is updated to: (1) add the two new hooks to the §4 gate table; (2) add a caveat subsection documenting the additionalContext-injection bug (#55889 / #15174) and the design's best-effort-plus-working-backstop posture, so a future reader knows WHY the PostToolUse-on-Agent + SessionStart-compact hooks are best-effort and WHEN to revisit (when the upstream issues close). The `incomplete-unverifiable-routing.md` module gets the DIVERGENT branch (§5.4). No new op-disc section is added.

---

## 6. Verification probes (what would falsify the design's behavior — VERA re-executes)

**All probes run against a THROWAWAY target, never the live session (§8).** Per op-disc §25.5 (probe-design sub-case): probes that read/mutate a git repo run in a `git clone --no-local` throwaway scratch repo created per-probe and deleted after, NOT in any operator-owned workspace. The throwaway target is scaffolded by `install.sh --target project --project-dir <tmp>`. No probe writes the running team's `.claude/settings.json`.

| # | Probe | Falsifies if |
|---|---|---|
| P1 | Inspect `substrate/CAPTAIN_NOMOS.md`: frontmatter `tools:` is exactly `Bash, Read, Grep, Glob` (NO `Agent`, `Write`, `Edit`, `WebSearch`, `WebFetch`); `name:` = `CAPTAIN_NOMOS{{NAME_SUFFIX}}`; `model: opus`; the envelope specifies the CONFORMANT/DIVERGENT/UNVERIFIABLE verdict shape + the per-divergence `classification` field (§4.6). | NOMOS has Agent/Write/Edit/Web, or omits the `classification` field §5.4 depends on |
| P2 | Voice-discipline check on `CAPTAIN_NOMOS.md`: PRINCIPAL/HUMAN throughout; no "Colonel" used as a human title; no second-person-as-instruction drift inconsistent with the other CAPTAIN files. | the role file leaks COLONEL-as-human or v1 voice |
| P3 | Deploy to a throwaway target with captains ON; assert `<tmp>/.claude/agents/CAPTAIN_NOMOS*.md` exists; assert the dry-run plan echo says "12" (not "11") envelopes. | NOMOS not deployed, or the count string not updated |
| P4 | `install.sh --target subproject ... --no-captains` against a throwaway; assert exit 0 and NO partial-deploy / no recompose error (the Arc-6 regression class). Then `--target subproject` WITH captains; assert exit 0. | adding NOMOS perturbed the no-captains or subproject path |
| P5 | Assert install.sh did NOT write/modify the LIVE session's `.claude/settings.json` (diff it before/after a deploy run, including a `--enable-hooks`-OFF run). **Structural safety probe (§8).** | the live settings.json changed |
| P6 | Feed `posttooluse-agent-checker-trigger.sh` a synthetic PostToolUse `Agent` event for a NON-NOMOS sub-agent; assert stdout JSON carries `additionalContext` with the run-NOMOS instruction AND the instruction is self-contained (no bare "see §" pointer — op-disc §34). | the trigger omits the instruction or emits a bare pointer |
| P7 | Feed the same script a NOMOS-return event (`agent_type` = `CAPTAIN_NOMOS*`); assert NO additionalContext emitted (recursion guard via agent_type). Then feed an event with the agent name ABSENT but a session-sentinel present; assert NO additionalContext (sentinel fallback). | the trigger fires on NOMOS-return (loop) or the fallback fails |
| P8 | Feed `sessionstart-compact-reprime.sh` a SessionStart `compact` event; assert it emits `hookSpecificOutput.{hookEventName:"SessionStart", additionalContext:...}` with a self-contained reprime payload, and exits 0 fast. Assert it NEVER blocks session start. NOTE the verdict must record that injection is upstream-broken (#15174) — the probe verifies the script EMITS correctly, not that the platform injects (the platform bug is out of the script's control). | the script blocks session start, emits malformed JSON, or carries a bare pointer |
| P9 | Inspect modified `stop-self-check.sh`: clause A still references NOMOS and still degrades gracefully if NOMOS is absent; `bash -n` exit 0; the working `decision:"block"`+`reason` channel is unchanged (Stage-1 regression guard). | the Stop self-check broke the working channel or the graceful-degrade wording |
| P10 | Inspect `substrate/templates/settings-hooks.json`: the PostToolUse-on-Agent + SessionStart-compact registrations are present with `{{HOOKS_DIR}}` slots; the JSON is valid (`python3 -m json.tool`); the file's `_comment` still names the source-only / never-live-settings.json safety constraint. | the registrations are missing/malformed or the safety comment was dropped |
| P11 | Inspect `substrate/modules/incomplete-unverifiable-routing.md`: the DIVERGENT branch is present with all 3 guardrails (size-derail-vs-escalate; attempt-cap N=2 with re-derive-don't-remember; granularity floor); the NOMOS cross-ref is added; the existing INCOMPLETE/UNVERIFIABLE branches + A6-LOCK + op-disc §15 cross-refs are PRESERVED (no-regression). | a guardrail is missing, or the module's existing content regressed |
| P12 | `bash -n` (syntax check) every `substrate/hooks/*.sh` (incl the two new + the modified Stop); run shellcheck if available. | any script has a syntax error |
| P13 | Dry exercise of NOMOS's probe logic (§4.5) against a synthetic orchestrator output: (a) an arc-close claiming "VERA returned PASS" against a throwaway ticket with NO PASS comment → assert the logic identifies a `ticket-state` divergence; (b) a close claiming a SHA that `git rev-parse` does not resolve → assert a `commit-sha` divergence; (c) a CONFORMANT output (claims match ground truth) → assert no divergence. | the bw-state comparison misses a real divergence or false-flags a conformant output |
| P14 | Grep every NEW/MODIFIED trigger payload string (the two new hooks + the modified Stop reason) for a bare "see §" pointer with no inline instruction; assert none (op-disc §34). | any payload is a bare pointer |
| P15 | **Canonical-template alignment (§6.8 / `canonical-template-alignment.md`):** the `settings-hooks.json` registration blocks for the four hooks share a canonical command-entry shape (`{type, [matcher], command:{{HOOKS_DIR}}/<script>, timeout}`); assert the new two are byte-aligned to that shape modulo the named slots (script name, matcher, timeout), OR any deliberate variance (e.g. the SessionStart timeout=10 vs 30) is named in the `_comment` / surrounding prose. | a new registration silently diverges from the canonical entry shape |

**Note on what is NOT VERA-checkable:** the upstream additionalContext-injection bug (#55889 / #15174) is OUT of the script's control — VERA verifies the scripts EMIT correct JSON (P6, P8), not that the platform injects it (which it currently does not). The design's resilience to that bug is structural (the Stop channel + cron carry the load), and P9 verifies the Stop channel is intact. This is the honest scope of the verification.

---

## 7. Safety architecture (extends Stage 1 §8 — do not violate)

**Stage 2 ships as substrate SOURCE only. No component arms a hook in the LIVE session's `.claude/settings.json`.** The Stage-1 architecture extends unchanged:

- **CAPTAIN_NOMOS.md is INERT until deployed AND invoked.** A new role file on disk does nothing until (a) `install.sh` deploys it to `.claude/agents/` AND (b) the orchestrator dispatches it. This arc writes the SOURCE file; it does not dispatch NOMOS against any live output. NOMOS cannot self-activate (it has no Agent tool; it is a leaf).
- **The two new hooks deploy as INERT scripts + CANDIDATE registrations.** Like Stage 1, deploying the scripts to `.claude/hooks/` is inert (Claude Code only fires hooks REGISTERED in a `settings.json`, which this arc never writes). The new registrations live in the CANDIDATE `settings-hooks.json`, armed only by the operator-gated, default-OFF `--enable-hooks` path — and at user tier even `--enable-hooks` only PRINTS a manual-merge runbook (never auto-writes `~/.claude/settings.json` — ARGUS Stage-1 r4).
- **Isolation-only VERA probe plan.** Every probe (§6) feeds synthetic stdin JSON to the scripts directly, OR deploys to a THROWAWAY target / `git clone --no-local` scratch repo, OR statically inspects a source file. NO probe runs `--enable-hooks` against anything but a throwaway; NO probe edits a live `.claude/settings.json`; NO probe dispatches NOMOS against a real orchestrator output (P13 uses a SYNTHETIC output against a THROWAWAY ticket). P5 is the structural probe VERA re-executes to confirm the live settings.json is byte-identical before/after any install.sh run in this arc.
- **Why this matters (unchanged from Stage 1):** a PostToolUse-on-Agent hook armed into the RUNNING team's own settings.json would inject "go run NOMOS" into the very session doing the build — and NOMOS dispatched against the build's own sub-agent returns would gate the build on its own checker. That is a no-experiments-on-real-agents violation in spirit (the live canonical seats are the "real agent" — `stoa--xyb.2` / MEMORY.md). The default-OFF posture + source-only build keeps the running team ungated by its own enforcement layer.

This is stated in the updated `substrate/hooks/README.md` (travels with the scripts) AND enforced by the `--enable-hooks`-default-OFF design AND checked by probe P5.

---

## 8. PRINCIPAL-gate surfacing (§6.7)

Stage 2 contains ONE clause with PRINCIPAL-gate shape: the **§7.7 UNLOCK alternative** (§5.3). Per the §6.7 discipline, I surface it at design-ratification time rather than as a post-hoc disposition:

- **The DROP path (recommended, §5.3) is NOT PRINCIPAL-gated.** It edits no hard-locked canon; it routes around the §7.7 collision (NOMOS-DROP never touches the seat-tag convention and is agent-inspection, not the locked mechanical layer). DROP ships clean on gauntlet verification per POLYBIUS's autonomous-ship posture for this arc.
- **The UNLOCK path IS PRINCIPAL-gated** (it would edit the §7.7 hard-lock). I do NOT recommend it and find NO concrete reason it is needed (§5.3). Per the brief, the ONLY surface-before-merge trigger for Stage 2 is "if DAEDALUS finds a concrete reason UNLOCK is needed." **I find none — so this design does not trigger the PRINCIPAL gate, and I state that explicitly here so PLINY can route DROP-no-gate with the gate-discipline discharged on the record.**

No other Stage-2 clause carries PRINCIPAL-gate shape. NOMOS's PRINCIPAL-gate-conformance PROBE (§4.5 probe 4) is NOMOS auditing OTHER outputs' gates — not a gate on this design itself.

---

## 9. Self-assessed weak points (post-work gate, §6.2)

1. **WP1 — the NOMOS-dispatch reminder's best-effort channel is currently broken upstream; the working backstop is a turn-end nudge, not a guarantee.** The PostToolUse-on-Agent hook rides `additionalContext` (#55889: broken on current versions). The reliable carrier is the Stop self-check `reason` (working), which fires at TURN-END, not at sub-agent-return. So on current versions, the NOMOS reminder arrives later (turn-end) than ideal (sub-agent-return), and even the Stop reminder is a nudge the orchestrator can read and not act on (the platform's "hooks can't dispatch sub-agents" limit). *Why this shape anyway:* this is a platform constraint, not a design choice — and it is exactly why the layer is defense-in-depth. The deterministic PreToolUse gates (Stage 1, on the WORKING `deny` channel) carry the load-bearing footguns and do NOT depend on model compliance at all; NOMOS is the judgment backstop for orchestrator-output truthfulness, which has no deterministic gate possible (it requires judgment). Building the additionalContext payload anyway is correct: it is forward-compatible (works the moment #55889 closes) and harmless when broken. The honest guarantee is "strong, not absolute" — the platform's own nature.

2. **WP2 — the SessionStart-compact reprime, as designed, does not reliably do its job on current versions (#15174).** I am shipping a hook whose additionalContext injection is upstream-broken (closed-as-duplicate, no fix through v2.1.150). *Why this shape anyway:* (a) it is the CORRECT mechanism, forward-compatible, and harmless when broken (executes, output dropped, no side effect); (b) the RELIABLE post-compaction reprime already exists and is unaffected — CLAUDE.md (loaded after compaction, the #15174 issue's own named workaround) + the polling cron (fresh harness-fired input that survives compaction by construction, the stoa--xyb.5 founding principle). The design explicitly does NOT claim SessionStart-compact as the reprime guarantee. But ARGUS should weigh whether shipping a known-broken-upstream hook is worth the surface — my position is yes (it documents the dependency so a future arc revisits when #15174 closes), but it is a legitimate "wait for the platform fix" call I am flagging rather than smoothing.

3. **WP3 — the PostToolUse-on-Agent recursion guard rests on a field whose parent-context population I could not fully confirm.** The primary guard (no-op when `agent_type` = NOMOS) depends on the parent-context PostToolUse-on-Agent event carrying the returned sub-agent's name. §2 confirmed `agent_type`/`agent_id` are populated "when the hook fires inside a subagent" but could NOT confirm the PARENT's on-return event reliably carries the returned agent's name (the same gap Stage-1 ARGUS r5 flagged). *Why this shape anyway:* the design carries a session-sentinel fallback (mirroring the Stage-1 Stop sentinel) so the guard holds even if `agent_type` is absent in the parent event; and the FAILURE mode if BOTH miss is bounded — a NOMOS-on-NOMOS reminder injected once, which the orchestrator reads and (per NOMOS's own one-job framing) recognizes as not-applicable (NOMOS is not an orchestrator output to re-audit). It is a degraded-but-bounded failure, not an infinite loop, because NOMOS is a leaf (it cannot dispatch a further NOMOS — no Agent tool). VERA should probe both the agent_type path AND the sentinel fallback (P7).

---

## 10. Residual questions for ARGUS

- **R1 (§7.7 DROP reasoning):** confirm the §5.3 argument that a JUDGMENT agent (NOMOS) doing bw-STATE comparison does NOT trigger §7.7's hard-lock — on BOTH grounds (subject: it never touches the seat-tag convention; mechanism: it is agent-inspection per §27, not the locked mechanical pre-comment-hook/CI-lint layer). If ARGUS reads the hard-lock as broader (e.g. "any new enforcement machinery touching coordination correctness"), the DROP-no-gate routing changes and PLINY must surface to PRINCIPAL.
- **R2 (NOMOS-vs-LIEUTENANT, §4):** confirm the call that NOMOS is a CAPTAIN (judgment) not a LIEUTENANT skill (mechanical), and specifically that the `classification` judgment (size-derail vs wrong-spec) is the load-bearing reason a skill is insufficient. If ARGUS judges the fact-extraction part should be a separately-deployed skill (vs inline-in-NOMOS), that is a buildable variant.
- **R3 (best-effort hooks worth shipping?):** the two new hooks (PostToolUse-on-Agent, SessionStart-compact) BOTH ride the upstream-broken `additionalContext` channel (WP1, WP2). Is shipping known-broken-upstream-but-forward-compatible hooks the right call, or should the design ship ONLY the working-channel mechanisms (Stop reminder + cron + CLAUDE.md) and DEFER the additionalContext hooks until #55889/#15174 close? My position: ship both, with the README caveat documenting the dependency. ARGUS adjudicates.
- **R4 (re-decompose cap robustness, Stage-1 R4 extended):** confirm the "re-derive the count from bw, don't remember it" hardening (§5.4 guardrail 2) is robust enough against orchestrator compaction, and that "fail-toward-escalation when the count read is UNVERIFIABLE" is the right safe direction.
- **R5 (recursion guard, Stage-1 r5 extended):** confirm the `agent_type` + session-sentinel double-guard (§5.2 / WP3) is sufficient given §2 could not confirm the parent-context event carries the returned agent name.

---

## 11. Out of scope

- **Brand-doc ripple (12th CAPTAIN).** The case study (`docs/case-study/`) and the app roster (`app/`) reference team size; adding NOMOS as the 12th CAPTAIN ripples into those. Per the brief, this is OUT of scope and tracked separately.
- **Extracting NOMOS's fact-extraction to a standalone LIEUTENANT skill.** §4.3 keeps it inline-in-NOMOS (a handful of Bash/Grep ops, no reuse outside NOMOS today). If a future arc finds the fact-extraction is reused elsewhere, extracting it to a skill is a clean follow-up — not this arc.
- **Fixing the upstream additionalContext-injection bugs (#55889, #15174).** Out of the Stoa's control (platform bugs). The design is resilient to them (working-channel backstops) and documents the dependency so a future arc revisits when they close.
- **The standing cron canary as a NEW mechanism.** The reliable post-compaction reprime reuses the EXISTING polling-cron-prompt-template; this arc does not redesign cron lifecycle (Stage-1 §11 carried this scope-out; it holds).
- **Live-session enablement.** Arming the hooks ON in any real (non-throwaway) session is operator-gated and out of this arc's build (§7).
- **Extending the seat-tag convention to PLINY/CAPTAIN outputs.** That is the §7.7 UNLOCK path, NOT recommended (§5.3), PRINCIPAL-gated, and explicitly not taken by this design.
- **The next debloat steps (.9 prose-compression, 3na propagation, final redeploy).** Sequenced after Stage 2 per POLYBIUS's capstone plan; not this arc.
