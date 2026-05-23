# Arc 46 design-rev1 — the enforcement layer

Author: Denson Smith
Ticket: stoa--xyb.5 (parent epic stoa--xyb — the-stoa debloat)
Seat: CAPTAIN_DAEDALUS_the-stoa
Arc: 46 (debloat Arc 3 — BUILD arc, additive enforcement machinery; NOT a cut)
Worktree branch: arc-46/build (from cd827d7 — includes Arc-1 modules + Arc-2 slim POLYBIUS)

---

## 1. Problem restatement (pre-work gate, §6.1)

Arcs 44–45 cut role-file bloat by relocating CONDITIONAL/PROVENANCE/DUPLICATE content out of always-loaded core into the composition layer (modules + bw + slim recompose). That cut is only safe if **adherence to the surviving rules survives context compaction**. Today adherence rests on *memorized instruction*: an agent that compacts mid-task forgets the slim rules it was carrying, and there is no harness-owned mechanism that re-tells it at the moment of action. The debloat made the role files thinner, which makes the memorized-instruction failure mode *more* likely to bite, not less.

This arc designs the **enforcement layer**: the machinery that moves adherence OUT of memorized-instruction and INTO harness-owned triggers that carry self-contained instructions at the moment of action. The proven principle (stoa--xyb.5) is that a cron prompt survives compaction because it is *fresh input re-injected after the wipe* — the agent does not remember the rule; the trigger re-tells it. Hooks share that property: they are harness-fired, not model-fired, so they fire regardless of what the model's compacted context still holds.

The layer has seven components (per the brief): (1) PreToolUse hard gates, (2) a Stop self-check, (3) a PostToolUse-on-Agent checker trigger, (4) a new checker CAPTAIN, (5) bw-ground-truth / seat-tag canary detection, (6) re-decompose remediation with guardrails, (7) install.sh wiring + the authoring-rule canon.

**Imported assumptions named at the gate (real briefs have implicit scope):**

- **(A1) The layer is substrate SOURCE only; it is never installed into the live session.** The brief's HARD SAFETY CONSTRAINT is load-bearing: a PreToolUse gate on `git commit` / tool-deny installed into the running team's own `.claude/settings.json` would gate the running team's own operations — a §xyb.2 no-experiments-on-real-agents violation in spirit. The design therefore ships *source files that ADA writes and VERA probes against a throwaway target*, and nothing in this arc wires the live session's settings.json. This is restated as a constraint, not merely a precaution (§8).
- **(A2) "Hook surface" means the settings.json shell-command hook surface, not the Agent SDK callback API.** The substrate deploys to interactive Claude Code sessions configured via `.claude/settings.json` shell-command hooks, not to a TypeScript/Python SDK host. The web verification (§2) reads both the SDK doc (authoritative for *capability* — which events support which fields) and the settings.json shell-command shape (authoritative for *how we register*). Where they differ in surface (callback object vs exit-code+stdout-JSON), the settings.json shell shape governs what ADA writes.
- **(A3) Staging is in-scope to *recommend*, out-of-scope to *decide*.** The brief says "PLINY decides staging." The design proposes a 2-stage split and names the minimal coherent first build; PLINY ratifies.
- **(A4) The checker CAPTAIN is orchestrator-fired and does not nest.** Per finding stoa--xyb.2#4 a sub-agent cannot dispatch a sub-agent. The checker is dispatched by PLINY/POLYBIUS (the orchestrator), and the PostToolUse-on-Agent hook can only *inject the instruction to dispatch it* — it cannot dispatch it itself (the .5 KEY LIMIT). This is a structural property the design rests on, surfaced as a weak point (§9).

If any of A1–A4 is wrong, it is a brief bug, not a design bug — flagged for ARGUS (§10).

---

## 2. Web-verified hook surface (per global rule + .5 "verify at build time")

Verified 2026-05-23. The `.5` mapping was pulled 2026-05-22; hook surfaces shift. Three sources read; **the authoritative source is the official Anthropic doc `https://code.claude.com/docs/en/agent-sdk/hooks`** (verbatim code examples), cross-checked against `https://code.claude.com/docs/en/hooks` (the settings.json shell-command reference) and the GitHub `anthropics/claude-code` plugin-dev hook-development SKILL. Where the plugin-dev SKILL disagreed with the official SDK doc, the official SDK doc wins (it carried verbatim, current code examples; the SKILL omitted fields).

| Behavior the layer rests on | .5 claim | Live-verified result | Verdict |
|---|---|---|---|
| **PreToolUse can hard-DENY a tool call** | yes, exit 2 / permissionDecision:deny | CONFIRMED. `hookSpecificOutput.permissionDecision: "deny"` + `permissionDecisionReason` (shown to the model so it does not retry) + top-level `systemMessage` (shown to the user). Also: exit code 2 from a shell-command hook = "blocking error; stderr fed back to Claude; tool call blocked." Both mechanisms work. `deny` wins over all other decisions when multiple hooks fire. | **CONFIRMED — no drift** |
| **PostToolUse can inject additionalContext** | yes (basis for the checker trigger) | CONFIRMED. Verbatim: *"For `PostToolUse` hooks, you can set `additionalContext` to append information to the tool result, or `updatedToolOutput` to replace the tool's output entirely before Claude sees it."* (A stale plugin-dev SKILL omitted `additionalContext` and listed only `systemMessage`; the authoritative SDK doc carries it — resolved in favor of `additionalContext`.) | **CONFIRMED — no drift** |
| **`Agent` is a matchable tool name** (the tool that runs sub-agents) | implied | CONFIRMED. Verbatim matcher tool list: *"Built-in tools include `Bash`, `Read`, `Write`, `Edit`, `Glob`, `Grep`, `WebFetch`, `Agent`, and others."* So a PostToolUse matcher of `"Agent"` fires when a sub-agent returns, in the **parent** context. | **CONFIRMED — no drift** |
| **SubagentStop CANNOT inject additionalContext** | yes (basis for using PostToolUse-on-Agent instead) | CONFIRMED. SubagentStop (like Stop) supports only top-level `decision` / `reason` / `systemMessage`; no `additionalContext`. This validates the .5 design choice: use **PostToolUse matcher `Agent`** for the check-a-sub-agent pattern, not SubagentStop. | **CONFIRMED — no drift** |
| **Stop can inject additionalContext + exit 2 to force rework** | yes, with caveat (model may commit BEFORE Stop fires) | PARTIAL DRIFT. Stop can **block** (exit 2 / `decision:"block"` + `reason`) to force continuation — CONFIRMED. But Stop does **NOT** support `additionalContext`; it carries the self-check text via the `reason` field (shown to Claude) instead. The caveat holds: pre-action gates belong on PreToolUse, not Stop, because Claude can commit before Stop fires. Net: the Stop self-check is built with `decision:"block"`+`reason`, not `additionalContext`. | **MINOR DRIFT — field name; design adapts (§5.2)** |
| **PostCompact can/can't inject context** | .5: "reportedly cannot inject context" | DRIFT. **There is no `PostCompact` event** in the canonical event list — only `PreCompact` (fires *before* compaction; cannot carry post-compaction state forward). So the .5 framing ("PostCompact can't inject, so the next trigger carries it") is moot: the reprime-after-compaction job has no PostCompact home at all. The correct homes are **`SessionStart` (matcher `"compact"`, which CAN inject additionalContext on a compact-triggered resume)** and **cron** (the standing re-injection). | **DRIFT — design routes to SessionStart/cron (§5.5, §9)** |
| **(new since .5) SubagentStart exists + CAN inject additionalContext** | not in .5 | NOTED. `SubagentStart` fires at sub-agent initialization in the parent and can inject `additionalContext`. This is an *alternative* delivery point for priming a sub-agent's modules at spawn, but the composition layer already delivers modules via the dispatch payload (Channel 1/2), so this arc does NOT use it. Recorded so ARGUS/PLINY know the surface grew. | **NOTED — not used this arc** |

**Settings.json shell-command hook shape (what ADA writes into a `settings.json` template).** The official `code.claude.com/docs/en/hooks` reference schema:

```json
{
  "hooks": {
    "<EventName>": [
      {
        "matcher": "<ToolNameRegex>",
        "hooks": [
          { "type": "command", "command": "<absolute-path-to-script>", "timeout": 30 }
        ]
      }
    ]
  }
}
```

A shell-command hook reads a JSON event object on **stdin**, and communicates back via **exit code** + **stdout JSON**:
- exit 0 + stdout JSON → the JSON's `hookSpecificOutput` / `decision` fields are honored.
- exit 2 → blocking error; **stderr is fed to Claude** as the reason; the action is blocked.
- other non-zero → non-blocking error (logged, surfaced in transcript, execution continues).

The matcher matches **tool name only** (regex), never file paths or arguments. To gate on a specific command shape (e.g., `git commit`, `bw comment ... -m`), the script inspects the `tool_input.command` string itself from stdin. This is load-bearing for the PreToolUse gates (§5.1).

**Doc URLs (for the citation trail):**
- Authoritative capability matrix: `https://code.claude.com/docs/en/agent-sdk/hooks`
- Settings.json shell-command shape + exit codes: `https://code.claude.com/docs/en/hooks`
- Cross-check (some fields stale): `https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/hook-development/SKILL.md`

---

## 3. Approach — overall shape

The layer is two mechanically distinct tiers, both harness-owned:

1. **Deterministic tier (compaction-immune, no model in the loop):** PreToolUse hard gates. A shell script reads the tool call, decides, and blocks or allows. The model's compacted context is irrelevant — the gate fires from the harness. This tier is where the load-bearing footguns live (author-field, clean-tree-before-branch, no-`-m`-in-bw-comment).
2. **Judgment tier (model in the loop, but harness-*triggered*):** Stop self-check, PostToolUse-on-Agent checker trigger, the checker CAPTAIN, and the re-decompose remediation. These cannot be made fully deterministic (they require judgment), but the *trigger* to run them is harness-fired, so the judgment fires even when the agent would otherwise have forgotten to invoke it.

Everything ships as **substrate SOURCE** under `substrate/hooks/` (new dir) + a new `substrate/CAPTAIN_NOMOS.md` + a `substrate/templates/settings-hooks.json` template + install.sh wiring + canon prose in `operating-disciplines.md`. **Nothing writes the live session's settings.json** (§8).

Directory layout this arc introduces:

```
substrate/
  hooks/                                  # NEW dir, glob-deployed like modules/
    pretooluse-author-field-audit.sh
    pretooluse-clean-tree-before-branch.sh
    pretooluse-no-dash-m-bw-comment.sh
    stop-self-check.sh
    posttooluse-agent-checker-trigger.sh
    README.md                             # the authoring rule + the install-into-throwaway-only safety note
  templates/
    settings-hooks.json                   # the settings.json hooks block (paths are {{HOOKS_DIR}} slots)
  CAPTAIN_NOMOS.md                        # NEW checker CAPTAIN envelope
```

---

## 4. Component contracts (the hand-off ADA builds against)

Each hook script obeys one uniform contract so ADA builds them to a single shape and VERA probes them uniformly:

**Hook script I/O contract (all five scripts):**
- **stdin:** one JSON object (the hook event). Scripts parse it with whatever JSON tool is present; the design specifies `python3 -c` for parsing (POSIX-portable, present on every substrate target; `jq` is NOT assumed present — a weak point if python3 is also absent, §9).
- **For PreToolUse gates** — emit one of:
  - allow (default): exit 0 with no stdout (normal permission flow proceeds), OR
  - deny: exit 0 with stdout `{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"<self-contained message>"}}`. The design uses the **exit-0 + JSON** form (not exit 2) for deny because it lets us set `permissionDecisionReason` precisely (the model-facing message); exit 2 only forwards stderr. (Both work; JSON is chosen for message control.)
- **For PostToolUse / Stop** — emit exit 0 with stdout JSON carrying `additionalContext` (PostToolUse) or `decision:"block"`+`reason` (Stop).
- **The self-contained-message rule (the authoring rule, §7):** every `permissionDecisionReason` / `additionalContext` / `reason` string states (a) WHAT was blocked/why this fired, and (b) WHAT to do to proceed — inline, no "see §X.Y.Z" pointer (a pointer fails after compaction).
- **Fail-OPEN, not fail-closed, on script error:** if the script itself errors (parse failure, missing interpreter), it exits non-2 / prints nothing so the tool call is NOT spuriously blocked. Rationale: a buggy gate that fail-closes would brick the team; a buggy gate that fail-opens degrades to today's behavior (no enforcement) which is safe. This is a deliberate inversion of the usual "fail closed for safety" and is flagged as a weak point (§9) because it means a broken gate silently stops enforcing.

---

## 5. The seven components

### 5.1 PreToolUse hard gates (deterministic, compaction-immune)

Three gates. All register under `"PreToolUse"` with matcher `"Bash"` (each footgun is a Bash command; the script discriminates on `tool_input.command`).

**(a) Author-field audit gate** — `pretooluse-author-field-audit.sh`
- **Matcher:** `"Bash"`.
- **Fires on:** a `tool_input.command` whose first token is `git` and which contains `commit` (covers `git commit`, `git commit -m ...`, `git -c ... commit`). The script does not try to gate `git push` — author-field correctness is a commit-time property.
- **Check:** parse the would-be-committed author-like fields. Two sub-checks:
  1. The git **commit author identity** (`git config user.name` / `user.email` in the cwd) — must not be overridden to a non-PRINCIPAL identity. (The commit author is the PRINCIPAL's configured identity per global authorship rule; the seat-identity signal is a `Co-Authored-By:` trailer layered ON TOP, never a replacement — global CLAUDE.md §"Substrate seat-identity convention".)
  2. **Staged author-like fields in author-encoding files** — for any staged file whose path matches the author-encoding set (`plugin.json`, `marketplace.json`, `package.json`, `pyproject.toml`, `setup.py`, `Cargo.toml`, `Gemfile`, `composer.json`, `LICENSE*`, `NOTICE`, `CITATION.cff`, skill `metadata.json`, `manifest.json`, anything under `.claude-plugin/`, and YAML frontmatter `author:` lines in `*.md`), grep the staged blob for the field set (`author`, `authors`, `owner`, `creator`, `created_by`, `maintainer`, `maintainers`, `by`, `copyright`, `holder`, `vendor`, `publisher`). If any such field's value is a person-name that is NOT the PRINCIPAL (or the PRINCIPAL-by-name), DENY.
- **Deny mechanism:** exit 0 + `permissionDecision:"deny"` with `permissionDecisionReason`:
  > "Commit blocked: author-like field `<field>` in `<file>` names `<wrong-value>`, not the PRINCIPAL. Per the authorship-attribution discipline, any author/owner/creator/maintainer/copyright field in a committed artifact must name the PRINCIPAL (a Co-Authored-By trailer is the only seat-identity layer, never a replacement for the Author identity). Fix the field to the PRINCIPAL, re-stage, and re-commit. If `<wrong-value>` is a legitimately-cited SOURCE author (not an authorship claim on this artifact), move it out of the author field into prose/a citation."
- **Known limit (weak point §9):** the "is this value the PRINCIPAL?" check needs the PRINCIPAL's known name(s). The script reads an allow-list from a deployed config (`.claude/hooks/principal-identity` — one name/email per line, written at install time from the install's PRINCIPAL identity). A name not on the list is treated as "not the PRINCIPAL" → deny. False positives are possible if the allow-list is incomplete; the deny message says how to widen it. The gate is a backstop for the global discipline, not its replacement.

**(b) Clean-tree-before-branch gate** — `pretooluse-clean-tree-before-branch.sh`
- **Matcher:** `"Bash"`.
- **Fires on:** a `tool_input.command` that creates an arc-build branch — i.e. matches `git checkout -b`, `git switch -c`, `git branch <name>`, or `git worktree add`. (The script matches the create-a-branch verbs, not every git call.)
- **Check:** run the §5.9 clean-tree check (the worktree/branch-from-clean-main discipline; `MAJOR_POLYBIUS.md` §18 / `MAJOR_PLINY.md` §5.9): `git status --porcelain` in the relevant repo must be empty (or only show the expected-untracked set). If the tree is dirty, DENY.
- **Deny mechanism:** exit 0 + deny with `permissionDecisionReason`:
  > "Branch creation blocked: the working tree is dirty (`<n>` modified/untracked path(s)). Per §5.9, arc-build branches are created from a CLEAN tree so the diff is attributable to the arc. Commit, stash, or clean the listed paths first, then create the branch. Dirty paths: `<list>`."

**(c) No-`-m`-in-bw-comment gate** — `pretooluse-no-dash-m-bw-comment.sh`
- **Matcher:** `"Bash"`.
- **Fires on:** a `tool_input.command` whose tokens include `bw` then `comment` and ALSO contain a `-m` flag (the documented footgun — `bw comment` is POSITIONAL; `-m` silently misbehaves; `operating-disciplines.md` §12).
- **Deny mechanism:** exit 0 + deny with `permissionDecisionReason`:
  > "bw comment blocked: `bw comment` takes the body as a POSITIONAL argument, never `-m`. You wrote `bw comment <id> -m \"...\"`. Re-run as `bw comment <id> \"<text>\"` (the text in double quotes immediately after the ticket id). The `-m` flag is a footgun that does not attach the comment as intended."

All three gates are pure-shell + a JSON parse; no network, no model, sub-second. Compaction-immune because nothing about them depends on the model's context.

### 5.2 Stop self-check

`stop-self-check.sh`, registered under `"Stop"` (no matcher needed for Stop).
- **Fires on:** end of an orchestrator turn.
- **Behavior:** the script does NOT try to detect what the turn did (that is the checker's job). It injects a self-check checklist via `decision:"block"` + `reason` (Stop does NOT support `additionalContext` — the §2 drift; the checklist rides `reason`). The block forces the model to address the checklist before the turn can end. **The checklist is self-contained inline** (the authoring rule):
  > "Before ending this turn, confirm: (A) every bw comment you posted this turn carried its leading `[from: <seat-slug>]` (or `[for:][from:]`) author tag per §7.7 — a dropped tag is the canary the checker keys on; (B) if you closed an arc / posted an activation paste / committed, the checker CAPTAIN (NOMOS) has been or is being dispatched against that output (orchestrator outputs have no other checker); (C) no PreToolUse gate was worked-around by reshaping a command to dodge the matcher. If all three hold, restate 'self-check A/B/C clear' and stop. If any fails, fix it now."
- **Caveat handling (the .5 caveat — Claude can commit BEFORE Stop fires, and may stop mid-question):** the Stop self-check is explicitly a BACKSTOP, not a gate. The load-bearing pre-action checks (author-field, clean-tree, no-`-m`) live on PreToolUse precisely because they must fire *before* the action, and Stop fires after. The self-check's job is the things that have no pre-action tool-call to gate (did you tag your comments; did you dispatch the checker). To bound the "stop mid-question" failure, the script blocks at most **once per turn** (it writes a per-turn sentinel file keyed on the session id; if the sentinel exists it allows the stop) so it cannot trap the turn in an infinite block loop. The sentinel approach is a weak point (§9 — sentinel staleness across sessions).

### 5.3 PostToolUse-on-Agent checker trigger

`posttooluse-agent-checker-trigger.sh`, registered under `"PostToolUse"` with matcher `"Agent"`.
- **Fires on:** a sub-agent returning, in the PARENT (orchestrator) context — verified (§2).
- **Behavior:** injects, via `additionalContext`, the instruction to run the checker against the sub-agent's output. **Self-contained inline** (authoring rule):
  > "A sub-agent just returned. Per the cross-check discipline (cross-check > self-check; orchestrator outputs have no other checker), before you act on this sub-agent's output, run CAPTAIN_NOMOS against it: dispatch NOMOS with the sub-agent's returned verdict + the bw ticket id, and have it confirm the output conforms to bw ground truth (seat-tag presence/correctness, ticket-state consistency, no divergence from the durable record). If NOMOS returns DIVERGENT, do not propagate the output — route per the re-decompose remediation (§5.6). Note: the hook cannot dispatch NOMOS for you (hooks cannot dispatch sub-agents); you must issue the dispatch."
- **The KEY LIMIT, designed-around (§2 + .5):** the hook *cannot dispatch* the checker. It injects the instruction and (optionally) the orchestrator's own self-check makes the dispatch non-optional. The dispatch is still issued by the orchestrator (which HAS the Agent tool — NOMOS, a leaf, does not; finding .2#4). This is the structural reason the checker is orchestrator-fired.
- **Scope guard against recursion:** the hook must NOT fire the "go run NOMOS" instruction when the sub-agent that just returned IS NOMOS itself (else NOMOS-checks-NOMOS loop). The script inspects the event's `agent_type` / `tool_input` for the NOMOS seat name and no-ops in that case. (Verified the event carries `agent_type` when relevant; if the parent-context event does not expose the dispatched agent's name reliably, the fallback is a one-deep sentinel like §5.2 — flagged §9.)

### 5.4 The checker CAPTAIN — CAPTAIN_NOMOS (GROUND-TRUTH AUDITOR)

A new substrate-canon CAPTAIN. Proposed identity (per agent-author conventions):

| Field | Value |
|---|---|
| **Mnemonic** | NOMOS (Greek *nomos*, "law / that which is laid down as binding" — the seat checks output against the laid-down ground truth) |
| **Rank** | CAPTAIN |
| **Descriptive role** | GROUND-TRUTH AUDITOR |
| **Name (frontmatter)** | `CAPTAIN_NOMOS{{NAME_SUFFIX}}` |
| **tools** | `Bash, Read, Grep, Glob` (NO Write/Edit — it audits, never mutates, mirroring VERA's independence discipline; NO `Agent` — it is a leaf and cannot nest; NO WebSearch/WebFetch — its ground truth is bw + the repo, not the web) |
| **model** | opus |
| **Lives at** | `.claude/agents/CAPTAIN_NOMOS{{NAME_SUFFIX}}.md` |
| **Activation** | dispatched one-shot by the orchestrator (PLINY/POLYBIUS) — NOT by a hook (hooks can't dispatch), NOT by another CAPTAIN (can't-nest) |

**The one job:** check an ORCHESTRATOR OUTPUT (activation paste, arc-close, commit, directive — the outputs that today have NO checker) against bw GROUND TRUTH, and return a conformance verdict. Cross-check, not self-check (the orchestrator that produced the output cannot reliably self-detect its own derailment — .5).

**What it checks (the conformance probes):**
1. **Seat-tag conformance (the canary, §5.5):** every coordination comment the output references/posted carries a correct leading `[from: <slug>]` / `[for:][from:]` / `[radio-check <slug>]` tag per §7.7. A dropped or mistagged tag = a divergence signal.
2. **Ticket-state consistency:** the output's claims about ticket state (closed / blocked / verdict) match `bw show <id>` ground truth. (E.g., an arc-close paste that says "VERA returned PASS" when the ticket carries no PASS comment = divergent.)
3. **Output-vs-bw divergence:** the output does not assert facts that contradict the durable bw record (the general case of #2).
4. **PRINCIPAL-gate conformance (op-disc §25):** if the output crosses a PRINCIPAL-gating clause, ratification evidence exists in bw; else flag.

**Verdict shape** (mirrors the gauntlet verdict idiom; consumed by the orchestrator + §5.6):
```
verdict: <CONFORMANT | DIVERGENT | UNVERIFIABLE>
checked_output: <what was audited — the paste/close/commit/directive + its bw ticket>
divergences:
- type: <seat-tag | ticket-state | output-vs-bw | principal-gate>
  detail: <one line: what diverged from which bw ground-truth>
  classification: <SIZE-DERAIL | WRONG-SPEC | BLOCKED | IMPOSSIBLE>   # drives §5.6 routing
ground_truth_consulted: <bw ticket ids + commands run>
summary: <one paragraph>
```
- **CONFORMANT** → output may propagate.
- **DIVERGENT** → do not propagate; route per §5.6. Each divergence carries a `classification` that distinguishes a size-derail (→ split) from wrong-spec/blocked/impossible (→ escalate) — this is guardrail (1) of §5.6, produced AT the checker so the orchestrator routes correctly.
- **UNVERIFIABLE** → bw ground truth insufficient to decide; surfaces to operator (slots into PLINY §5.6 UNVERIFIABLE protocol).

NOMOS is the redundant-checker property the gauntlet already has for *deliverables* (VERA/CATO/ARGUS), extended to *orchestrator outputs* which previously had none.

### 5.5 bw-ground-truth / seat-tag canary detection

Per .5: do NOT try to detect "compaction happened." Detect "output diverges from bw ground truth" — the checking layer IS the derailment detector (a derailed agent produces non-conforming output regardless of cause). Detection must be external + comparison-based vs durable bw (a derailed agent cannot self-detect).

**The ready-made canary: the seat-tag (`operating-disciplines.md` §7.7).** Every POLYBIUS coordination comment carries a leading `[from: <slug>]` / `[for: <slug>][from: <slug>]` / `[radio-check <slug>]` tag. A dropped or mistagged tag is a cheap, mechanical, comparison-based signal that the producing agent has drifted from the convention it was carrying. The canary is checked two ways:

1. **Mechanically, in the checker (NOMOS probe #1):** NOMOS greps the output's comments for the leading-tag pattern and flags any comment lacking a well-formed tag, or carrying a slug that does not match the producing seat. This is a deterministic string check — no judgment, so it is the highest-confidence divergence signal.
2. **Standing, via cron (Stage 2):** a periodic cron poll re-scans recent coordination tickets for mistagged comments (the same §7.7 parse the polling-cron-prompt-template STEP 1.5 already does), so divergence is caught even between checker dispatches. Bounded by check cadence (one cron cycle, not instant — .5).

**Why the tag is the right canary:** it is (a) already mandatory (no new convention), (b) mechanically parseable (a regex, no model), (c) produced by exactly the seats most prone to compaction-derailment (the long-lived orchestrators), and (d) load-bearing (a misattributed tag caused the 25-min stall in the stoa--e39 empirical, §7.7) — so a dropped tag correlates with real coordination failure, not just cosmetic drift.

### 5.6 Re-decompose remediation + guardrails

When NOMOS returns DIVERGENT (or VERA returns INCOMPLETE/UNVERIFIABLE), the orchestrator remediates by **re-decomposing the failed unit into smaller pieces and re-dispatching** (an orchestrator job — can't-nest). Compaction-derailment correlates with task size; small-enough tasks never compact, so splitting both fixes this instance AND tunes granularity for next time (the reaction teaches the prevention — .5). bw-as-memory makes fine decomposition cheap (state read from bw, not carried in-head, so splits don't fragment context).

**Guardrails (all three are load-bearing — without them the loop diverges):**

1. **Distinguish size-derail from wrong-spec/blocked/impossible.** Only a SIZE-DERAIL divergence is split. WRONG-SPEC / BLOCKED / IMPOSSIBLE divergences are ESCALATED, never split (splitting a wrong-spec task infinitely subdivides a task that can never pass). The classification is produced by NOMOS (§5.4 `classification` field) so the routing decision is made with the checker's evidence, not guessed by the orchestrator.
2. **Attempt cap → escalate to human.** A unit may be re-decomposed at most **N=2** times (configurable; default 2). On the 3rd divergence of the same unit lineage, the orchestrator STOPS splitting and escalates to PRINCIPAL via POLYBIUS. The cap is tracked on the unit's bw ticket (a `[re-decompose attempt: k/2]` comment) so the count survives the orchestrator's own compaction (the count is in bw, not in-head).
3. **Granularity floor.** A unit is not split below the point where handoff/coordination overhead exceeds the work (default floor: a unit whose own dispatch brief + verdict would be longer than the work it describes). At the floor, escalate instead of split.

**Integration into MAJOR_PLINY §5.6 (the INCOMPLETE/UNVERIFIABLE protocol).** §5.6 today routes verifier INCOMPLETE/UNVERIFIABLE to operator disposition. This arc adds NOMOS's DIVERGENT to the same protocol with a new branch:

> **DIVERGENT verdict received (from NOMOS).**
> - PLINY reads the `classification` of each divergence.
> - SIZE-DERAIL divergences → re-decompose the failed unit (guardrail 1), re-dispatch, increment the attempt counter on the unit's bw ticket (guardrail 2); if the counter would exceed the cap or the unit is at the granularity floor (guardrail 3), escalate to PRINCIPAL via POLYBIUS instead of splitting.
> - WRONG-SPEC / BLOCKED / IMPOSSIBLE divergences → do NOT split; surface to POLYBIUS → PRINCIPAL (same operator-disposition path as INCOMPLETE).
> - DIVERGENT does NOT gate merge autonomously (consistent with INCOMPLETE/UNVERIFIABLE A6 LOCK); it routes through operator judgment.

This keeps the new remediation inside the existing verdict-routing protocol rather than bolting on a parallel path.

### 5.7 install.sh wiring + the authoring rule as canon

**(a) Deploy the hook scripts** — mirror the `modules/` glob-deploy idiom (the file class the epic grows continuously, so glob, not a manifest array; matches the stoa--xyb.4 glob decision):
- Add `SRC_HOOKS_DIR="${SCRIPT_DIR}/hooks"`, source-existence check, `shopt -s nullglob; _src_hooks=( "${SRC_HOOKS_DIR}"/*.sh ); shopt -u nullglob`, assert `>0`.
- Add `DEST_HOOKS_DIR` per tier (user: `${HOME}/.claude/hooks`; project: `${PROJECT_DIR}/.claude/hooks`; subproject: `""` — skipped, mirroring templates/modules).
- Deploy loop copies `*.sh` to `DEST_HOOKS_DIR` and `chmod +x` each. Deploy the `hooks/README.md` too (the authoring rule + safety note travels with the scripts).
- Add the plan-line + dry-run echo (matches the modules block at install.sh ~702).

**(b) Deploy the settings-hooks.json template** — add `settings-hooks.json` to `TEMPLATE_NAMES`. It carries the hooks block with `{{HOOKS_DIR}}` slots that install.sh sed-substitutes to the deployed `DEST_HOOKS_DIR` absolute path (same `sed` substitution idiom used for `{{NAME_SUFFIX}}` / `{{USER_TIER_DIR}}`).
- **CRITICAL SAFETY (§8):** install.sh deploys `settings-hooks.json` as a SEPARATE template file (a *candidate* hooks block), and does **NOT** merge it into the live `.claude/settings.json`. Merging into the live settings.json is an explicit, separate, operator-gated step that the install script PRINTS as a manual instruction (it does not perform). A new install flag `--enable-hooks` (default OFF) is the only path that would merge, and even then only into the TARGET's settings.json, never the running session's. For this arc, ADA never exercises `--enable-hooks` against anything but a throwaway target.

**(c) Deploy CAPTAIN_NOMOS** — add `NOMOS` to the `CAPTAIN_NAMES` array (the existing CAPTAIN deploy loop + dry-run plan-line then cover it with zero new code, per the agent-author note). Update the "11 envelopes" count in the plan echo to 12.

**(d) The authoring rule as canon.** Add a short subsection to `operating-disciplines.md` (the always-loaded thin home — the detail lives in `substrate/hooks/README.md`, dogfooding the composition layer):
> **Trigger-payload authoring rule.** Every harness-owned trigger payload (cron prompt body AND hook `additionalContext` / `permissionDecisionReason` / Stop `reason`) MUST state, self-contained inline, (a) WHY it fired and (b) WHAT to do — never a bare pointer ("see §X"). A pointer fails after compaction; the trigger's whole value is that it re-tells the rule the agent has forgotten. Detail + worked examples: `.claude/hooks/README.md`.

---

## 6. Verification probes (what would falsify the design's behavior — VERA re-executes)

**All probes run against a THROWAWAY target, never the live session (§8).** The throwaway target is a temp dir scaffolded by `install.sh --target project --project-dir <tmp>` (or a `git clone --no-local` of a scratch repo for the commit-gate probes, per op-disc §25.5 probe-design sub-case). No probe writes the running team's `.claude/settings.json`.

| # | Probe | Falsifies if |
|---|---|---|
| P1 | Deploy to a throwaway target; assert `<tmp>/.claude/hooks/*.sh` exist and are `+x`; assert `<tmp>/.claude/templates/settings-hooks.json` exists. | any hook script or the template is missing post-deploy |
| P2 | Assert install.sh did NOT write/modify the LIVE session's `.claude/settings.json` (diff it before/after a deploy run). **Structural safety probe (§8).** | the live settings.json changed |
| P3 | Feed `pretooluse-author-field-audit.sh` a synthetic PreToolUse stdin JSON for `git commit` staging a file whose `author:` = a non-PRINCIPAL name; assert stdout JSON carries `permissionDecision:"deny"` + a self-contained reason. | the gate allows, or the reason is a bare pointer |
| P4 | Feed the same script a commit staging an author field = the PRINCIPAL; assert allow (exit 0, no deny JSON). | the gate false-positive-denies a correct commit |
| P5 | Feed `pretooluse-clean-tree-before-branch.sh` a `git checkout -b` stdin JSON with a dirty `git status --porcelain` (simulated in the throwaway repo); assert deny + self-contained reason listing dirty paths. | the gate allows branch-from-dirty |
| P6 | Feed `pretooluse-no-dash-m-bw-comment.sh` a `bw comment <id> -m "x"` command; assert deny. Then feed `bw comment <id> "x"`; assert allow. | the gate misses `-m` or false-denies the positional form |
| P7 | Feed `stop-self-check.sh` a Stop event (no sentinel); assert `decision:"block"` + a `reason` carrying the self-contained A/B/C checklist. Feed it again WITH the sentinel present; assert allow (no infinite block). | the self-check never releases, or carries a bare pointer |
| P8 | Feed `posttooluse-agent-checker-trigger.sh` a PostToolUse `Agent` event for a NON-NOMOS sub-agent; assert `additionalContext` carrying the run-NOMOS instruction. Feed it a NOMOS-return event; assert NO additionalContext (recursion guard). | the trigger fires on NOMOS-return (loop) or omits the instruction |
| P9 | Inspect `CAPTAIN_NOMOS.md`: frontmatter `tools:` excludes `Agent`, `Write`, `Edit`; `name:` = `CAPTAIN_NOMOS{{NAME_SUFFIX}}`; the envelope specifies the CONFORMANT/DIVERGENT/UNVERIFIABLE verdict shape + the `classification` field. | NOMOS has Agent/Write, or omits the classification field §5.6 depends on |
| P10 | Run NOMOS (or a dry exercise of its probe logic) against a synthetic orchestrator output with a DROPPED seat-tag in a referenced bw comment; assert it returns DIVERGENT type:seat-tag. Against a well-tagged output; assert CONFORMANT. | the canary check misses a dropped tag or false-flags a good one |
| P11 | `install.sh --dry-run` against a throwaway target; assert the plan lists the hooks deploy, the settings-hooks.json template, and 12 CAPTAINs (NOMOS added). | the dry-run plan omits any new file class |
| P12 | `bash -n` (syntax check) every `substrate/hooks/*.sh`; run shellcheck if available. | any script has a syntax error |
| P13 | Grep every deployed trigger payload string for a bare "see §" pointer with no inline instruction; assert none (the authoring rule). | any payload is a bare pointer |

**Probe-design safety note (op-disc §25.5):** P3–P8 mutate/read a git repo; they run in a `git clone --no-local` throwaway scratch repo created per-probe and deleted after, NOT in any operator-owned workspace. The design names the throwaway-clone pattern here rather than relying on a blanket PRINCIPAL-discretion clause.

---

## 7. Staging recommendation (PLINY decides — A3)

**Recommendation: STAGE into two arcs.** The layer is 7 components; the deterministic tier and the judgment tier have different risk profiles and different review surfaces.

**Stage 1 (minimal coherent first build) — the deterministic tier + deploy plumbing:**
- §5.1 the three PreToolUse hard gates (author-field, clean-tree, no-`-m`)
- §5.2 the Stop self-check
- §5.7 install.sh wiring (hooks glob-deploy + settings-hooks.json template + the `--enable-hooks` OFF-by-default safety + the authoring-rule canon)
- Probes P1–P8, P11–P13

Why this is the minimal coherent first build: the deterministic gates are the highest-value, lowest-judgment, fully-testable-in-isolation pieces. They deliver compaction-immune enforcement of the three load-bearing footguns with NO new agent, NO cross-agent dispatch, NO judgment loop. It is reviewable as "shell scripts + a settings template + install plumbing" — a tight, mechanical diff. It also lands the safety architecture (§8) that Stage 2 depends on.

**Stage 2 — the judgment tier:**
- §5.3 PostToolUse-on-Agent checker trigger
- §5.4 CAPTAIN_NOMOS (new CAPTAIN envelope + CAPTAIN_NAMES entry)
- §5.5 standing cron canary (the mechanical canary in NOMOS ships in Stage 2 with NOMOS; only the *cron* standing-scan is incremental)
- §5.6 re-decompose remediation + guardrails + MAJOR_PLINY §5.6 integration
- Probes P9, P10

Why second: the checker + remediation introduce a new agent, the can't-nest constraint, the recursion guard, and the re-decompose loop with its three guardrails — substantially more judgment surface and more ways to get the integration with §5.6 wrong. It benefits from landing on top of a verified, stable Stage 1 (the Stop self-check's clause B references NOMOS, but degrades gracefully: until NOMOS exists, clause B is a no-op reminder, not a broken dispatch).

**Coupling note for PLINY:** the only forward-coupling is the Stop self-check clause B mentioning NOMOS. Stage 1 ships clause B worded so it reads as a reminder even before NOMOS exists ("if you closed an arc..., the checker has been or is being dispatched" — true-vacuously when there is no checker yet). No Stage-1 component hard-depends on a Stage-2 component. If PLINY prefers a single full-build arc, the design supports it; the staging is a risk-reduction recommendation, not a structural requirement.

---

## 8. HARD SAFETY CONSTRAINT (explicit — do not violate)

**The enforcement layer is built as substrate SOURCE only. No component of this arc installs hooks into the LIVE session's `.claude/settings.json`.**

- A PreToolUse gate on `git commit` / tool-deny installed into the running team's own settings.json would gate the running team's OWN operations — gating the very session doing the build. That is a §xyb.2 no-experiments-on-real-agents violation in spirit (the live, canonical seats are the "real agent").
- install.sh deploys `settings-hooks.json` as a **candidate** template file; merging it into a settings.json is a separate, operator-gated, default-OFF (`--enable-hooks`) step that even when used targets the INSTALL TARGET, never the running session.
- ADA TESTS hooks in ISOLATION: by feeding synthetic stdin JSON to the scripts directly (P3–P8, P10), and by deploying to a THROWAWAY target dir / `git clone --no-local` scratch repo (P1, P5, P11). ADA never runs `--enable-hooks` against anything but a throwaway, and never edits the live `.claude/settings.json`.
- P2 is the structural probe that VERA re-executes to CONFIRM this property: the live session's settings.json is byte-identical before and after any install.sh run in this arc.

This constraint is stated in `substrate/hooks/README.md` (travels with the scripts) AND enforced by the install.sh `--enable-hooks`-default-OFF design AND checked by probe P2.

---

## 9. Self-assessed weak points (post-work gate, §6.2)

1. **JSON parsing dependency.** The hook scripts parse stdin JSON; the design specifies `python3 -c` (POSIX-portable, present on substrate targets) and explicitly does NOT assume `jq`. If a target has neither python3 nor jq, every gate fail-OPENs (§4) — silently no enforcement. *Why this shape anyway:* fail-open is the safe failure (degrades to today's no-enforcement baseline, never bricks the team); and python3 presence is a reasonable substrate-target assumption already relied on by other tooling. VERA should probe the no-python3 path (added consideration for ARGUS).

2. **The author-field gate's PRINCIPAL-identity allow-list is the soft spot.** "Is this value the PRINCIPAL?" requires knowing the PRINCIPAL's name(s) (`.claude/hooks/principal-identity`). An incomplete list false-positive-denies a legitimate commit; a too-permissive list misses a real wrong-name. *Why this shape anyway:* the gate is a deterministic backstop for a discipline that already exists in prose (global CLAUDE.md); a backstop that occasionally false-denies (with a clear widen-the-list message) is strictly better than no mechanical check, and the discipline itself remains the primary defense. The deny message tells the operator exactly how to widen the list.

3. **The hook KEY LIMIT means the checker is never *guaranteed* to run.** The PostToolUse-on-Agent hook can only INJECT the instruction to dispatch NOMOS; it cannot dispatch NOMOS (hooks can't dispatch sub-agents; .5 verified). A sufficiently derailed orchestrator could read the additionalContext and still not dispatch. *Why this shape anyway:* this is a platform constraint, not a design choice — and it is exactly why the layer is defense-in-depth (deterministic PreToolUse gates that DON'T depend on model compliance carry the load-bearing footguns; the checker is the judgment backstop for the rest). The Stop self-check clause B is a second nudge. It is "strong, not absolute" by the platform's nature (.5's own framing).

4. **PostCompact does not exist (§2 drift) — there is no instant post-compaction reprime.** The .5 mapping assumed a PostCompact event to reason about; the live surface has only PreCompact + SessionStart(matcher:compact). So the instant an auto-compaction finishes mid-turn, nothing re-primes until the NEXT trigger (next tool call's PreToolUse, next Stop, next cron). *Why this shape anyway:* this is acceptable because the deterministic PreToolUse gates fire on the very next gated tool call regardless of compaction state, and cron re-injects on cadence — the design never depended on instant reprime. But it is a real reduction vs the .5 mental model and ARGUS should weigh whether SessionStart(matcher:compact) should carry an explicit reprime payload in Stage 1 (the design currently leaves SessionStart unused).

---

## 10. Residual questions for ARGUS

- **R1 (A1/A4 brief-scope):** confirm the HARD SAFETY CONSTRAINT reading — that "substrate source only, never the live settings.json" is the intended scope and the `--enable-hooks`-default-OFF + manual-merge-instruction design satisfies it without leaving the layer un-installable on real targets.
- **R2 (weak point 4):** should Stage 1 add a `SessionStart` (matcher `"compact"`) reprime hook to partially recover the missing-PostCompact gap, or is "next trigger carries it" sufficient (the design's current position)?
- **R3 (NOMOS naming/scope):** is CAPTAIN_NOMOS the right seat boundary, or does ground-truth-auditing-of-orchestrator-outputs belong as a new MODE of an existing checker (CATO/ARGUS) rather than a 12th CAPTAIN? The design proposes a new seat because the *subject* differs (orchestrator outputs vs deliverables/diffs/plans) and one-job-per-agent argues against overloading an existing seat — but the seat-count cost is real.
- **R4 (guardrail cap N=2):** is the re-decompose attempt cap of 2 the right default, and is "track the count on the unit's bw ticket" robust against the orchestrator's own compaction (the count is in bw, but reading+incrementing it correctly is itself a step a derailed orchestrator could botch)?
- **R5 (fail-open inversion):** confirm fail-OPEN (not fail-closed) on hook-script error is the right call for this layer (weak point 1) — the usual security default is fail-closed, and the design deliberately inverts it for liveness.

---

## 11. Out of scope

- **Subproject-tier hook deploy.** Like modules (composition-layer §7), subproject-tier hook deploy is deferred — `DEST_HOOKS_DIR=""` in subproject mode. Subproject `.claude/settings.json` resolution for a dispatched sub-agent is the same contested-path question that deferred subproject modules; not this arc's to settle.
- **The cron renewal/expiry machinery.** The Stage-2 standing canary cron reuses the existing polling-cron-prompt-template + §11 step 1.5 renewal dance; this arc does not redesign cron lifecycle.
- **Detecting "compaction happened."** Explicitly rejected by .5 — the design detects output-divergence-from-ground-truth, not the compaction event. Named here so ARGUS does not read its absence as an omission.
- **Live-session enablement.** Turning the hooks ON in any real (non-throwaway) session is operator-gated and out of this arc's build (§8).
- **MAJOR_PLINY cut / further role-file debloat.** This is the BUILD arc (enforcement machinery); the next cut arc is separate.
- **A general MCP/Skill delivery path for triggers.** Settled out by stoa--xyb.1 (CLI-not-MCP) — triggers deliver via Bash/hooks/cron only.
