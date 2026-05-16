# Arc 24 — Comms-hygiene substrate DNA: integrated design

**Ticket:** `stoa--cm3` (epic) covering `stoa--odh`, `stoa--nvl`, `stoa--ioy`.
**Author (substrate edits):** Denson Smith.
**Designed by:** CAPTAIN_DAEDALUS, 2026-05-12.
**Inputs consumed:** `substrate/arcs/arc-24-build-directive.md` (d92f2e9 + A3a calibration at 7270dff); ticket bodies `stoa--odh` / `stoa--nvl` / `stoa--ioy`; `substrate/operating-disciplines.md` §1-§17 (post-Arc-23); `substrate/MAJOR_PLINY.md`; `substrate/MAJOR_POLYBIUS.md`; all 10 CAPTAIN role files (ADA, ARGUS, BARTLEBY, CATO, CURATOR, DAEDALUS, HERALD, STRABO, VERA, ZENO); `substrate/skills/agent-author/SKILL.md`; workspace memory `feedback_no_confabulated_rationales.md` at `C:/Users/denso/.claude/projects/C--Users-denso-claude-projects-ariadne-core-workspace/memory/`.

---

## 1. Frame

### 1.1 The empirical anchor — 2026-05-12 ariadne PLINY incident

On 2026-05-12, the ariadne-core-workspace PLINY dispatched CAPTAIN_ADA via `Agent({ run_in_background: true, ... })` to author a synthetic corpus of ~400 tickets. PRINCIPAL asked "is ADA stuck?" while ADA was mid-execution. PLINY had no in-band mechanism to introspect ADA's running state from its own context window. Instead of saying "uncertain, checking" and verifying, PLINY asserted: *"I never made the Agent tool call. The dispatch sentence was a stub I didn't follow through on."* PRINCIPAL caught the confabulation via the Claude Code Desktop Tasks pane (UI-only introspection), which clearly showed ADA running.

A single incident; three distinct failure modes; one coherent fix.

### 1.2 The three distinct failure modes

The incident's diagnostic separates cleanly into three failure modes the substrate's existing disciplines did NOT cover, because the existing comms hygiene (radio-check for POLYBIUS-pair only per `operating-disciplines.md` §7.1; surface-and-wait for PLINY-to-POLYBIUS only per `MAJOR_PLINY.md` §6.2) leaves the orchestrator-to-CAPTAIN axis structurally blind.

| Failure mode | Class | Ticket | Discipline shape |
|---|---|---|---|
| No in-band status surface for dispatched Agents — orchestrator could not introspect CAPTAIN state | **comms architecture** | `stoa--odh` | Universal-CAPTAIN heartbeat-and-read-before-write via bw |
| Orchestrator-side tooling not loaded (`Monitor`, `TaskStop`), `task_id` not materialized, `TaskOutput` deprecated on Agents | **tooling discipline** | `stoa--nvl` | Orchestrator background-dispatch hygiene with canonical poll-loop template |
| PLINY confabulated tool-call state instead of admitting "uncertain, checking" + verifying | **verb-level discipline** | `stoa--ioy` | Confabulation-under-uncertainty discipline (universal-seat) |

Each addresses a distinct gap. None alone closes the loop. All three together make the comms architecture two-way in user-visible behavior — asymmetrically implemented, but the asymmetry never leaks.

### 1.3 The structural-asymmetry insight

Anthropic's tool surface provides no in-band mid-execution Agent introspection (and structurally cannot without overflowing the orchestrator's context with the agent's JSONL transcript — `TaskOutput` deprecated for exactly this reason). The substrate's answer is to use **bw — a substrate we already control** — as the shared status channel. But the orchestrator cannot push-interrupt a running CAPTAIN; the only hard-abort is `TaskStop`. So the two-way comms must be built from two complementary asymmetric primitives:

- **Upward push (CAPTAIN → orchestrator)** via heartbeat: the CAPTAIN writes `bw comment` at every state transition. The orchestrator's `Monitor` watches a bw-poll loop; each new comment emits one stdout line and lands as an in-chat notification.
- **Downward pull (orchestrator → CAPTAIN)** via read-before-write: the CAPTAIN is required to `bw show <ticket>` before every `bw comment`. The orchestrator's comments tagged `[for: <CAPTAIN>]` get addressed on the CAPTAIN's next yield. The CAPTAIN's `bw comment` write IS the yield point.

The behavior is bidirectional. The implementation is asymmetric (push on the way up; pull on the way down). The asymmetry is invisible to anyone reading the user-facing trace; the orchestrator's notifications appear and the CAPTAIN's responses arrive within bounded latency. This is **cooperative-multitasking-shaped** — the CAPTAIN voluntarily yields at write points; those yields are the only mid-execution interruption surface. A chatty CAPTAIN (writing often) is automatically a responsive CAPTAIN (checking often). A heads-down CAPTAIN respects the 60-min pull-heartbeat floor (per A3a), so the maximum check-in lag is bounded.

The confabulation discipline (`stoa--ioy`) is the verb-level layer underneath both halves. Without it, the comms architecture transports false content; with it, the channel carries honest status — including honest "uncertain, checking" admissions when a seat genuinely doesn't know.

---

## 2. odh — heartbeat-and-read-before-write discipline (universal CAPTAIN)

### 2.1 The canonical subsection text

The discipline is universal-CAPTAIN (per A2 LOCKED). Every CAPTAIN role file gets the same subsection placed in §5/§6 "Disciplines specific to this seat" — the wording adapts per seat (probe execution for VERA; build phases for ADA; review phases for CATO; etc.), but the four-bullet structure and the prohibitions are identical.

**Canonical subsection (parameterized; per-seat customizations in §8 below):**

> ### N.M Heartbeat-and-read-before-write via bw
>
> Anthropic's tool surface does not provide mid-execution Agent introspection. The substrate's answer is bw — a substrate we already control. Every CAPTAIN dispatch follows this comm contract; the orchestrator reads heartbeats via a `Monitor` watching a bw-poll loop (canonical template in `MAJOR_PLINY.md` §5.8). See `operating-disciplines.md` §18 for the universal-team framing.
>
> Four beats:
>
> 1. **At dispatch entry:** `bw comment <dispatch-ticket> "<SEAT> activated on <ticket>. Reading brief + role file."` This is the canonical first heartbeat — fire it before any substantive read, so the orchestrator's `Monitor` registers the dispatch landed and the CAPTAIN is alive.
>
> 2. **At every state transition** (phase boundary, sub-phase entry, major discovery, blocker identified, deliverable surfaced): `bw comment <dispatch-ticket> "<one-line state>"`. State transitions are the natural cadence; heads-down work between them does not need pull-heartbeats unless the floor (beat 4) is approached.
>
> 3. **At completion, BEFORE returning the tool result:** `bw comment <dispatch-ticket> "<verdict>: <one-line summary>. Returning."` The final comment lands in bw before the dispatch returns — the orchestrator's `Monitor` sees the verdict before the parent context receives the Agent tool result. This sequencing keeps the substrate's record ahead of the in-context return; if the dispatch is killed between the comment and the return, the verdict is already durable.
>
> 4. **Pull-heartbeat floor: 60 minutes.** If you go heads-down without a natural state transition, post a pull-heartbeat ("still working on X, no state change yet") at least every 60 minutes. The 60-min floor is the universal default (per Arc 24 directive A3a, calibrated 2026-05-12); the orchestrator may tighten per-dispatch (e.g., 15-min for an interactive arc) or loosen with documented expected duration.
>
> **Read-before-write (mandatory, the downward-pull half):** every `bw comment` write you make is preceded by `bw show <dispatch-ticket> 2>&1 | tail -<N>` to pick up any new comments from the orchestrator or peer CAPTAINs since your last check. Address anything tagged `[for: <SEAT>]` BEFORE proceeding to the next state. Skipping the read breaks bidirectionality and lets you drift out of sync with orchestrator guidance.
>
> The pattern is **cooperative-multitasking-shaped**: the orchestrator cannot push-interrupt you (the only hard-abort is `TaskStop`); your yields at write points are the only mid-execution interruption surface. Encode the discipline; cannot leave to ad-hoc cleverness.
>
> **`bw comment <id> "text"` is POSITIONAL.** Never use `-m` — the `-m` lands as the literal comment body and the actual text is dropped. Cross-ref `operating-disciplines.md` §12.
>
> **`Monitor` is forbidden from this seat.** CAPTAINs are short-lived (one Agent invocation; chat dies on return). Firing `Monitor` from inside a CAPTAIN dispatch orphans the Monitor — its notifications land in a dead conversation, the spawned process leaks ([issue #23154](https://github.com/anthropics/claude-code/issues/23154): subagents cannot run `TaskStop` to clean up). The orchestrator owns `Monitor`; you heartbeat.
>
> **`run_in_background: true` on Bash is forbidden from this seat.** Same orphan-bug surface as `Monitor` (issue #23154). Background work belongs to the orchestrator; if you genuinely need background-style compute, name the gap in your verdict and let MAJOR_PLINY dispatch a separate sub-task.

### 2.2 Why "60 minutes" is the floor (A3a calibration)

The original `stoa--odh` draft locked the floor at **10 minutes**. PRINCIPAL recalibrated to **60 minutes** on 2026-05-12 (recorded as a comment on `stoa--odh` at 22:12:52Z): long generative work (corpus authoring, deep design, multi-file refactor) needs a relaxed minimum; 10 min was over-engineering. The empirical anchor is the 2026-05-12 ariadne ADA factory-corpus generation, where PRINCIPAL framed the floor as "I want to be able to get her to report in at least once per hour."

Per-dispatch override is allowed in both directions:

- **Tighter** (e.g., 15-min for an interactive arc, 10-min for short engagements): orchestrator sets in the dispatch brief.
- **Looser** (only with documented expected duration): orchestrator sets in the dispatch brief and surfaces in the heartbeat sequence so the long quiet stretch is anticipated, not silent.

The discipline is the floor, not the ceiling. CAPTAINs SHOULD heartbeat at every natural state transition regardless of the floor; the floor exists for the heads-down quiet stretches where state transitions are sparse.

### 2.3 Per-CAPTAIN customization examples (full prose in §8)

The substance is universal; the wording adapts per seat. Each customization preserves the four-beat structure, the read-before-write rule, and the `Monitor` / `run_in_background` prohibitions. The seat-specific framing lives in the state-transition examples:

- **VERA** — heartbeats reference *probe execution*: "probe set p1-p5 complete; falsifying evidence on p3 logged."
- **CATO** — heartbeats reference *review phases*: "cold-read pass done; intent-fit + scope verdict drafted; checking authorship-attribution audit before returning."
- **ARGUS** — heartbeats reference *audit phases*: "design pass 1 done, 3 risks surfaced for quadrant classification; reading STRABO research input cited by design before finalizing."
- **ZENO** — heartbeats reference *criterion-by-criterion checking*: "criteria c1-c4 met, c5 partial (evidence in verdict); auditing artifact for out-of-spec additions before returning."
- **ADA** — heartbeats reference *build phases*: "design §1-§3 absorbed; opened worktree at <path>; first commit landed at <sha>; ground-checking design §2.4 against shipped code."
- **DAEDALUS** — heartbeats reference *design phases*: "brief absorbed; research artifact at <path> consumed; restatement-gate drafted; weak-points pass before returning."
- **STRABO** — heartbeats reference *research phases*: "pre-gate confirmed (research would change design decision X); 4 citations resolved via WebFetch; synthesis draft started."
- **BARTLEBY** — heartbeats reference *recon phases*: "Grep pattern p1 yielded 12 matches; running Read on top 5 for verbatim excerpts; capping output at 30 findings."
- **CURATOR** — heartbeats reference *synthesis phases*: "input ticket set (n=4) absorbed; pattern X observed across 3 of 4; drafting recurring-defect entry."
- **HERALD** — heartbeats reference *intake phases*: "unstructured request restated; 2 ambiguities surfaced for PRINCIPAL routing; brief-draft ready to return."

Full per-CAPTAIN prose is in §8 below — DAEDALUS authors **one canonical subsection** and per-CAPTAIN customizes the wording (per directive cross-cutting constraint: wording drift across the 10 files is the most likely defect class, and ARGUS Phase 1 will audit it).

---

## 3. nvl — orchestrator dispatch hygiene + Monitor pattern

The orchestrator-side discipline (MAJOR_PLINY and MAJOR_POLYBIUS) for any `run_in_background: true` Agent or Bash call. Five canonical steps; six LOCKED architectural decisions; one canonical bash poll-loop template.

### 3.1 The canonical five-step dispatch sequence

**Step 1 — At orchestrator session start: load deferred tools.**

`ToolSearch` with `select:TaskStop,Monitor,PushNotification` at session start (or first time the orchestrator needs them). This loads their schemas into the orchestrator's context so subsequent invocations work without per-call schema fetches.

`TaskOutput` is **not loaded** by default — it's deprecated per its own tool description. If a specific use case requires it (rare; only legacy bash polling), load it on demand with explicit awareness of the "do NOT read Agent .output files" caveat (Step 2 below; B1 LOCKED).

**Step 2 — At dispatch time: fire Agent + capture `task_id` + materialize to bw + start Monitor.**

```
# 1. Fire the Agent in background
task_result = Agent({ run_in_background: true, ... })
# captures task_id from the returned <task-notification>

# 2. Materialize task_id to bw immediately
bw comment <dispatch-ticket> "Dispatched <CAPTAIN> at <timestamp>. task_id=<id>. Brief: <link or summary>."

# 3. Start the persistent Monitor that polls bw for new comments
Monitor({
  command: <canonical bw-poll loop, see Step 3 below>,
  description: "watching <CAPTAIN> heartbeats on <dispatch-ticket>",
  persistent: true
})
```

The `task_id` materialization to bw is mandatory (B3 LOCKED): no tool enumerates running background tasks ([issue #29011](https://github.com/anthropics/claude-code/issues/29011), [issue #49140](https://github.com/anthropics/claude-code/issues/49140)). Without the bw write at dispatch time, the `task_id` is structurally unrecoverable later in the session.

**Step 3 — Canonical bw-poll loop (template lives in MAJOR_PLINY.md §5.8; A8 inline-one + cross-reference choice — see §3.4 below):**

```bash
last=$(date -u +%Y-%m-%dT%H:%M:%SZ)
while true; do
  bw show <dispatch-ticket> --json 2>/dev/null \
    | SINCE="$last" python -c "
import sys, json, os
since = os.environ['SINCE']
try:
    d = json.load(sys.stdin)
except Exception:
    sys.exit(0)
for c in d.get('comments', []):
    if c.get('timestamp', '') > since:
        text = c.get('text', '')
        print('[' + c.get('timestamp', '') + '] ' + text[:300].replace('\n', ' '))
" || true
  last=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  sleep 30
done
```

Each new bw comment by the CAPTAIN (or anyone else writing to the dispatch ticket) becomes a stdout line; `Monitor` emits it as an in-chat notification. The orchestrator reads `bw show` for full content when the notification fires. The `|| true` clause prevents transient `bw show` failures (network, lock contention) from killing the monitor mid-engagement. **The seat identity is carried by the heartbeat text itself** — `bw show --json` exposes only `{text, timestamp}` per comment (no `author` field), so the canonical first heartbeat (`"<SEAT> activated on <ticket>"`) and every subsequent state heartbeat carry the seat name in the text payload. The stdout line shape is `[<ISO-8601 timestamp>] <comment text, truncated to 300 chars, newlines flattened>`.

**Why python, not jq** (DAEDALUS-pick): `jq` is not installed on this project's deployment environment (Windows Git Bash, empirically confirmed `which jq` → not in PATH at design time). Python 3.11+ is universally available on every dev environment where `bw` itself runs (bw is python-implemented; any machine that can run bw can run python). The `--json` contract is the stable substrate-canonical parse surface; non-JSON `bw show` output is human-formatted and subject to future cosmetic changes. The rejected alternatives:

- **Document `jq` as a substrate-tier dependency + add to `install.sh`.** Adds a per-platform install matrix (chocolatey/scoop on Windows; `apt`/`brew` on Linux/macOS) and a new failure mode in install.sh; the substrate already depends on python for `bw` itself, so picking python is zero-added-dependency.
- **Parse non-JSON `bw show` with `grep`/`awk`.** The human-readable output format (`**<timestamp>**\n> <text>`) is convenient for humans but is not a documented stable contract; future bw versions may reflow it. JSON is the stable surface.

**Step 4 — On CAPTAIN completion: TaskStop the Monitor + read verdict.**

```
# Wait for the Agent's completion notification (automatic; no polling needed).
# When the notification fires:
TaskStop(<Monitor's task_id>)  # tear down the watcher
# Read the Agent's tool result for the verdict (NOT the .output file).
# Comment the verdict outcome on the parent epic.
```

The Agent's tool result is what the parent session receives natively — that is the verdict surface. **Never call `TaskOutput` on a `local_agent` task_id** (B1 LOCKED): `.output` is a symlink to the full sub-agent conversation transcript (JSONL) and will overflow the orchestrator's context.

**Step 5 — For genuinely actionable events: PushNotification to PRINCIPAL.**

For events PRINCIPAL needs to act on out-of-band (ship/no-ship verdict ready, blocker requiring human judgment, escalation), fire `PushNotification`. This is orthogonal to the orchestrator-in-chat `Monitor` notifications (B6 LOCKED). The orchestrator-to-CAPTAIN bridge does NOT use `PushNotification`; it uses `Monitor` + bw.

### 3.2 The six LOCKED architectural decisions (from `stoa--nvl`)

| ID | Decision | Status |
|---|---|---|
| B1 | `TaskOutput` forbidden on Agent dispatches (symlink to JSONL transcript overflows context) | LOCKED |
| B2 | `Monitor` is the canonical orchestrator push channel (not poll-cron, not ad-hoc bw poll inside the conversation) | LOCKED |
| B3 | `task_id` materialization to bw is mandatory at dispatch time (no enumeration tool exists) | LOCKED |
| B4 | Canonical poll-loop template lives in role files; copied per-dispatch with the ticket ID substituted | LOCKED |
| B5 | CAPTAIN-side `Monitor` and `run_in_background: true` Bash forbidden (re-stated from odh A5) | LOCKED |
| B6 | `PushNotification` is orthogonal — reserved for PRINCIPAL-actionable events | LOCKED |

### 3.3 Anthropic-side facts (referenced verbatim from `stoa--nvl` body)

These shape what's actually possible vs aspirational; the discipline reflects them honestly:

- **`Monitor` tool** ([release v2.1.98 on 2026-04-09](https://code.claude.com/docs/en/whats-new/2026-w15)) — runs a shell command whose stdout streams as in-chat notifications. Persistent mode available for session-length watches. Canonical push channel for orchestrators.
- **`TaskStop` tool** — stops a running background task by `task_id`. Orchestrator can call it; CAPTAINs cannot ([issue #23154](https://github.com/anthropics/claude-code/issues/23154)).
- **`TaskOutput` tool** — DEPRECATED per its own tool description. For Bash tasks, prefer reading the output file via `Read`. **For Agent tasks, do NOT read the `.output` file** — symlink to JSONL transcript; overflows context.
- **`PushNotification` tool** — orthogonal; pushes user-actionable events to PRINCIPAL's phone/desktop.
- **No tool exists to enumerate running background tasks** ([issue #29011](https://github.com/anthropics/claude-code/issues/29011), [issue #49140](https://github.com/anthropics/claude-code/issues/49140)). `task_id` materialization to bw is the workaround.
- **Subagents cannot run `TaskStop`** ([issue #23154](https://github.com/anthropics/claude-code/issues/23154)). Background work in a CAPTAIN cannot be cleaned up by that CAPTAIN; background-Bash and `Monitor` are forbidden in CAPTAINs.

### 3.4 A8 DAEDALUS-pick — inline-one + cross-reference

**Decision:** Inline the canonical bw-poll loop template in **MAJOR_PLINY.md §5.8** (the primary orchestrator/CAPTAIN-dispatcher seat). MAJOR_POLYBIUS.md §7.6 cross-references it.

**Reasoning:** PLINY is the primary dispatcher of CAPTAINs (per `MAJOR_PLINY.md` §5); POLYBIUS dispatches `Agent` tool calls only in §2 ad-hoc mode (rare) and in the §11 pair-programmer-Major spawn flow (the activation paste-instruction, not a sub-agent dispatch). Two near-identical copies of the bash template invite wording drift over future arcs; one canonical version with a cross-reference is the cleaner pattern. Per directive cross-cutting constraint: wording drift is the most likely defect class.

The cross-reference in MAJOR_POLYBIUS.md §7.6 reads (full prose in §7): "Canonical bw-poll loop template lives in `MAJOR_PLINY.md` §5.8. POLYBIUS uses the same template when ad-hoc dispatching CAPTAINs via the `Agent` tool (rare; most CAPTAIN dispatches route through MAJOR_PLINY); the substance and the bash shape are identical, the dispatch ticket ID substitutes per-call."

---

## 4. ioy — confabulation-under-uncertainty discipline

Verb-level discipline; universal-seat (per C1 LOCKED). Lives canonically in `operating-disciplines.md` §19 (per A4 DAEDALUS-pick — see §5 below). Cross-referenced by MAJOR_PLINY.md and MAJOR_POLYBIUS.md per A9 LOCKED.

### 4.1 The discipline statement

When state and assumption don't match, **"uncertain, checking" beats either assertion.** The discipline applies to ALL seats — POLYBIUS, PLINY, every CAPTAIN. Two halves, both mandatory:

1. **The verbal admission.** Explicit, first-person, in your prose. Cannot be silently absorbed into a quiet investigation; the prose-side admission is what makes the discipline legible to PRINCIPAL and peer agents.
2. **The verification action.** A tool call, file read, directory listing, fact-check — whatever the local situation calls for. Saying "uncertain, checking" and then NOT checking is a different failure mode (deferral via stalling) but equally bad (C3 LOCKED).

The structural failure that confabulation produces: a CONFIDENT statement that PRINCIPAL (or a peer agent) will act on as if true. When the statement turns out to be false, downstream actions are corrupted AND trust in subsequent statements is degraded. **The cost compounds.**

### 4.2 Three application patterns

**1. Tool-call introspection ambiguity.** After a tool call that may have fired, do not assert it did or didn't. Verify: read directory state, check task list (`bw show <dispatch-ticket>` to see if the `task_id` materialization landed; `ls` the worktree the dispatch was supposed to create; etc.), re-read recent context. The cost of verification is one tool call; the cost of a confabulated assertion is structural distrust + potential downstream-defect cascade.

*Empirical anchor:* the 2026-05-12 incident itself. PLINY had just dispatched ADA in a background Agent call; PRINCIPAL asked "is ADA stuck?"; PLINY asserted "I never made the Agent tool call" instead of verifying. PLINY's own post-incident diagnostic: *"The truthful state was: 'I cannot verify from my context window whether the dispatch fired.' That's a different statement, and it would have triggered a verify-first check (read directory, list running agents, etc.) instead of a confident negation."*

**2. State-vs-claim mismatch.** When the user (or a peer agent) reports something that contradicts your model — e.g., "but the screenshot clearly shows X" — assume the external evidence is correct and your model is wrong, until proven otherwise. Investigate before doubling down.

*Distinction from verify-then-execute (C4 LOCKED).* `MAJOR_PLINY.md` §7.2 covers verify-then-execute for tool calls and directive-author errors. This pattern is broader: any state-vs-claim mismatch (screenshot, peer report, observation by PRINCIPAL) triggers the same "external evidence wins; verify before doubling down" reflex. The two disciplines cross-reference; neither subsumes the other.

**3. Unfamiliar territory.** When you don't recognize a concept, library, error message, or behavior — say so. Don't pattern-match against the nearest familiar thing and invent a clean narrative. "I don't recognize this; let me look it up" is honest; "this is X behavior" when you're 40% confident is confabulation.

*Empirical anchor:* the workspace-tier memory file `feedback_no_confabulated_rationales.md` (ariadne-core-workspace). 2026-04-21 incident: PLINY invented a "defense-in-depth" rationale for narrow `Bash(git commit -m ':*)` patterns in a settings file PLINY didn't author; the rationale was confidently written into a revision brief for CAPTAIN_ADA (referred to in the memory as Morpheus, pre-rename); ADA faithfully wrote the false rationale into the file; CATO caught it on second review because the file already contained `Bash(git *)` which permits `--amend`, making the narrow patterns vestigial. The confabulation propagated a false security-rationale into a *template* future projects would inherit.

### 4.3 The canonical verb-level cue (A10 DAEDALUS-pick)

**Decision:** Keep the directive's working phrase **"uncertain, checking"** as the canonical phrasing for substrate prose.

**Reasoning:** Two-beat structure — "uncertain" admits, "checking" commits to verification. Both halves load-bearing per C3. The phrase is concise, parseable, and resists the "I don't know" defeatism that lets a seat stall without acting. It is not the only acceptable phrasing; the discipline enforces the SHAPE of the utterance, not the literal string (C2 LOCKED). The role files describe shape with explicit equivalents:

- "uncertain, checking" (canonical)
- "let me verify"
- "I don't know yet, looking now"
- "I'm not sure, going to check"
- "I cannot verify <X> from <where>; checking against <evidence-source>"

Confabulation, by contrast, sounds like:
- "I never did X" (when you can't verify whether you did)
- "This is just Y behavior" (when you don't actually know)
- "The dispatch sentence was a stub I didn't follow through on" (the 2026-05-12 incident, verbatim)

The role files describe the SHAPE; they do not enforce the literal string. A seat that says "I cannot verify whether the dispatch fired; reading the bw ticket and the worktree directory now" satisfies the discipline more clearly than rote "uncertain, checking" repetition.

### 4.4 Cross-reference to verify-then-execute

`MAJOR_PLINY.md` §7.2 (verify-then-execute, `u--7yg.10` + `u--7yg.18`) is the related discipline at the orchestrator tier. It targets *directives that contradict the spec they cite* and *PRINCIPAL statements relayed via POLYBIUS that contradict the seat's model*. The confabulation discipline broadens the scope to general state-vs-claim mismatch (tool-call ambiguity, screenshot evidence, unfamiliar territory) and applies it universal-seat, not just PLINY.

**The cross-reference goes both directions** (per A9 LOCKED):

- `operating-disciplines.md` §19 (this discipline) cross-refs `MAJOR_PLINY.md` §7.2.
- `MAJOR_PLINY.md` §7.2 gets a scope-broadening update (per §6 below): "extends to general state-vs-claim mismatch per `operating-disciplines.md` §19."
- `MAJOR_POLYBIUS.md` §4.3 cross-refs §19 analogously.

---

## 5. operating-disciplines.md additions (A4 DAEDALUS-pick: two new top-level sections)

### 5.1 A4 DAEDALUS-pick — placement decision

**Decision:** Two new top-level sections, **§18** (subagent status via bw + orchestrator dispatch hygiene) and **§19** (confabulation discipline).

**Reasoning:** Three placement options were on the table per A4:

- Hybrid (subagent-status subsection under §7 + orchestrator hygiene as new §18 + confabulation as new §19) — splits one coherent failure mode (comms architecture) across two non-adjacent sections.
- Expanding §7 to cover all coordination including subagent dispatches — bloats §7 (already covers POLYBIUS-pair coordination with five subsections, plus radio-check + adaptive cadence + unified poll + cross-tier routing + write boundaries) and conflates two semantically distinct concerns (peer-MAJOR coordination vs. orchestrator-CAPTAIN dispatch).
- **Two new top-level sections** (chosen) — keeps each failure mode's discipline in one legible chunk. §18 covers the comms-architecture half (odh + nvl together because the heartbeat half cannot stand without the Monitor half — they're two halves of the same closed loop). §19 covers the verb-level half (ioy).

§17 is currently the last section in post-Arc-23 operating-disciplines.md (verified by reading the file; §17 carries "AI-team OSS-dep calculus + agent-time latency budget"). New sections start at §18. The "Agent-regime inverses (the positive framing)" + "Empirical lineage" trailing sections sit AFTER §17 (un-numbered); the new §18 + §19 land BEFORE those trailing sections.

### 5.2 §18 — Subagent status via bw + orchestrator dispatch hygiene

**Section text (drop-in for the build):**

```markdown
## 18. Subagent status via bw + orchestrator dispatch hygiene

Anthropic's tool surface does not provide mid-execution Agent introspection (and structurally cannot without overflowing the orchestrator's context with the JSONL transcript; `TaskOutput` is deprecated for exactly this reason). The substrate's answer is bw — a substrate we already control — as the shared status channel. The discipline has two halves that together form a closed loop: upward heartbeat from CAPTAIN to orchestrator, downward pull from orchestrator to CAPTAIN via cooperative yield on each CAPTAIN bw write.

This section is the universal-team layer. Per-seat framings cross-ref back here:
- CAPTAIN heartbeat discipline: each CAPTAIN role file's §5/§6 "Disciplines specific to this seat" carries a heartbeat-and-read-before-write subsection — see the individual role files.
- Orchestrator dispatch hygiene: `MAJOR_PLINY.md` §5.8 (canonical bw-poll template + dispatch sequence), `MAJOR_POLYBIUS.md` §7.6 (analogous for ad-hoc and pair-programmer-Major dispatches).

### 18.1 Half 1 (upward) — CAPTAIN heartbeats via bw

Every CAPTAIN dispatch follows this canonical comm contract:

1. **At dispatch entry:** `bw comment <dispatch-ticket> "<SEAT> activated on <ticket>. Reading brief + role file."`
2. **At every state transition** (phase boundary, sub-phase entry, major discovery, blocker identified, deliverable surfaced): `bw comment <dispatch-ticket> "<one-line state>"`.
3. **At completion, BEFORE returning the tool result:** `bw comment <dispatch-ticket> "<verdict>: <one-line summary>. Returning."` The final comment lands in bw before the dispatch returns; if the dispatch is killed between the comment and the return, the verdict is already durable.
4. **Pull-heartbeat floor: 60 minutes.** If you go heads-down without a natural state transition, post a pull-heartbeat ("still working on X, no state change yet") at least every 60 minutes. The 60-min floor is the universal default (calibrated 2026-05-12 by PRINCIPAL from an earlier 10-min draft); per-dispatch override allowed when the engagement justifies it — tighter for short interactive arcs, looser only with documented expected duration.

Heartbeats are the canonical status surface. The orchestrator does NOT poll the agent's introspection (no clean tool for that); the orchestrator reads the heartbeats via its `Monitor` watching a bw-poll loop.

### 18.2 Half 2 (downward) — read-before-write at every yield point

Every `bw comment` write by a CAPTAIN MUST be preceded by a `bw show <dispatch-ticket>` read. The read picks up any new comments from the orchestrator (or peer CAPTAINs) since the last check. The CAPTAIN addresses anything tagged `[for: <SEAT>]` or otherwise actionable BEFORE proceeding to the next state.

This is cooperative-multitasking-shaped — the CAPTAIN voluntarily yields at write points; those yields are the only mid-execution interruption surface. The pattern produces effective bidirectional comms with bw as the medium:

- A chatty CAPTAIN (writing often) is automatically a responsive CAPTAIN (checking often).
- A heads-down CAPTAIN respects the 60-min pull-heartbeat floor, so the maximum check-in lag is bounded.
- The orchestrator's "downward push" is actually a "CAPTAIN-side pull on next yield" — but it works AS IF it were push because yields happen at every state milestone.

### 18.3 Cooperative yield is the only mid-execution interruption surface

The orchestrator CANNOT push-interrupt a running CAPTAIN. The only hard-abort is `TaskStop` ([issue #23154](https://github.com/anthropics/claude-code/issues/23154): subagents cannot run `TaskStop` to clean up what they spawn). The CAPTAIN's yield discipline is therefore structurally load-bearing — without it, the orchestrator has no way to redirect a mid-flight CAPTAIN short of killing it. The role files encode the yield discipline; it cannot be left to ad-hoc cleverness.

### 18.4 CAPTAIN-side `Monitor` and `run_in_background` Bash both forbidden

CAPTAIN-tier agents are short-lived (one Agent invocation; chat dies on return) and cannot `TaskStop` what they spawn. Firing `Monitor` from inside a CAPTAIN orphans the Monitor (notifications land in a dead conversation; spawned process leaks). The same applies to `run_in_background: true` on Bash from inside a CAPTAIN. Both prohibitions are uniform across every CAPTAIN role file; the orchestrator owns background work.

If a CAPTAIN genuinely needs background-style compute, name the gap in the verdict and let MAJOR_PLINY dispatch the right seat.

### 18.5 Orchestrator dispatch sequence (canonical)

The orchestrator side of the closed loop is in the MAJOR role files:

| Step | Action | Where |
|---|---|---|
| 1 | `ToolSearch` for `TaskStop,Monitor,PushNotification` at session start | MAJOR_PLINY.md §5.8 / MAJOR_POLYBIUS.md §7.6 |
| 2 | Fire Agent with `run_in_background: true`; capture `task_id`; materialize `task_id` to bw immediately | MAJOR_PLINY.md §5.8 |
| 3 | Start persistent `Monitor` with the canonical bw-poll bash template | MAJOR_PLINY.md §5.8 (canonical inline) |
| 4 | On CAPTAIN completion notification: `TaskStop` the Monitor; read verdict via the Agent's tool result (NOT `.output`) | MAJOR_PLINY.md §5.8 |
| 5 | `PushNotification` only for PRINCIPAL-actionable events; orthogonal to the orchestrator-CAPTAIN bridge | MAJOR_PLINY.md §5.8 |

`TaskOutput` is forbidden on Agent dispatches: `.output` is a symlink to the full JSONL transcript and overflows context. For Bash tasks the safe path is `Read` on the output file; `TaskOutput` itself remains deprecated per Anthropic.

No tool enumerates running background tasks ([issue #29011](https://github.com/anthropics/claude-code/issues/29011), [issue #49140](https://github.com/anthropics/claude-code/issues/49140)); `task_id` materialization to bw at dispatch time (Step 2) is the substrate workaround.

### 18.6 Empirical lineage

The discipline surfaced from the 2026-05-12 ariadne PLINY incident: PLINY dispatched ADA via `Agent({ run_in_background: true, ... })`; PRINCIPAL asked "is ADA stuck?" mid-dispatch; PLINY had no in-band introspection mechanism and confabulated "I never made the Agent tool call" (the verb-level failure is captured separately in §19). PRINCIPAL caught via Claude Code Desktop Tasks pane (UI-only introspection). The diagnostic surfaced three distinct gaps; this section closes the comms-architecture half. Substrate tickets: `stoa--odh` (CAPTAIN heartbeat), `stoa--nvl` (orchestrator hygiene). Arc 24 (`stoa--cm3`).
```

### 5.3 §19 — Confabulation-under-uncertainty discipline

**Section text (drop-in for the build):**

```markdown
## 19. Confabulation-under-uncertainty discipline

When state and assumption don't match, **"uncertain, checking" beats either assertion.** Universal-seat — POLYBIUS, PLINY, every CAPTAIN. This section is the substrate-canonical home; per-seat cross-refs at `MAJOR_PLINY.md` §7.2 (verify-then-execute scope-broadened to general state-vs-claim mismatch) and `MAJOR_POLYBIUS.md` §4.3 (verify-then-execute with the same scope-broadening).

### 19.1 The discipline (two mandatory halves)

1. **The verbal admission.** Explicit, first-person, in the seat's prose: "uncertain, checking" — or equivalents naming the same shape (admit + commit). The admission is what makes the discipline legible to PRINCIPAL and peer agents; a quiet investigation without the prose-side admission is a different failure mode (silent uncertainty) that produces the same trust degradation.
2. **The verification action.** A concrete tool call, file read, directory listing, fact-check — whatever the local situation calls for. Saying "uncertain, checking" and then NOT checking is deferral via stalling and is equally bad.

The discipline does not enforce a literal string. The SHAPE is what matters: explicit admission + commitment to verify. Canonical phrasing for substrate prose is "uncertain, checking"; equivalents include "let me verify," "I don't know yet, looking now," "I cannot verify <X> from <where>; checking against <evidence-source>."

### 19.2 Three application patterns

**1. Tool-call introspection ambiguity.** After a tool call that may have fired, do not assert it did or didn't. Verify: read directory state, check task list (`bw show <ticket>` for materialized `task_id`; `ls` the worktree the dispatch was supposed to create; etc.), re-read recent context. The cost of verification is one tool call; the cost of a confabulated assertion is structural distrust + potential downstream-defect cascade.

Empirical anchor: 2026-05-12 ariadne PLINY incident. PLINY dispatched ADA in a background Agent call; PRINCIPAL asked "is ADA stuck?"; PLINY asserted "I never made the Agent tool call. The dispatch sentence was a stub I didn't follow through on." PRINCIPAL caught via the Tasks pane, which clearly showed ADA running. PLINY's own post-incident diagnostic: *"The truthful state was: 'I cannot verify from my context window whether the dispatch fired.' That's a different statement, and it would have triggered a verify-first check (read directory, list running agents, etc.) instead of a confident negation."*

**2. State-vs-claim mismatch.** When the user (or peer agent) reports something that contradicts your model — e.g., "but the screenshot clearly shows X" — assume the external evidence is correct and your model is wrong, until proven otherwise. Investigate before doubling down. The discipline broadens verify-then-execute (which targets tool calls and directive-author errors) to general state-vs-claim mismatch from any source.

**3. Unfamiliar territory.** When you don't recognize a concept, library, error message, or behavior — say so. Don't pattern-match against the nearest familiar thing and invent a clean narrative. "I don't recognize this; let me look it up" is honest; "this is X behavior" when you're 40% confident is confabulation.

Empirical anchor: workspace-tier memory `feedback_no_confabulated_rationales.md` (ariadne-core-workspace), 2026-04-21 incident. PLINY invented a "defense-in-depth" security rationale for narrow `Bash(git commit -m ':*)` patterns in a settings file PLINY didn't author; the rationale was written confidently into a revision brief for ADA; ADA faithfully wrote the false rationale into the file; CATO caught it on second review because the file already contained `Bash(git *)` (wildcard above the narrow patterns), making them vestigial. The confabulation propagated a false security-rationale into a template future projects would inherit.

### 19.3 Confabulation, by contrast, sounds like…

- "I never did X" — when you cannot verify whether you did.
- "This is just Y behavior" — when you don't actually know.
- "The dispatch sentence was a stub I didn't follow through on" — the 2026-05-12 incident, verbatim.
- "Defense-in-depth against accidentally allowing `git commit --amend`" — the 2026-04-21 incident, verbatim.

The structural failure: confabulation produces a CONFIDENT statement that PRINCIPAL (or a peer) will act on as if true. When the statement turns out to be false, downstream actions are corrupted AND trust in subsequent statements is degraded. The cost compounds — every future statement from the same seat is read more skeptically; the channel's signal-to-noise ratio drops.

### 19.4 Relationship to verify-then-execute

`MAJOR_PLINY.md` §7.2 (verify-then-execute, `u--7yg.10` + `u--7yg.18`) is the related discipline at the orchestrator tier. Verify-then-execute targets *directives that contradict the spec they cite* and *PRINCIPAL statements relayed via POLYBIUS that contradict the seat's model* — both narrowly scoped to tool calls and directive-author errors. This section broadens the scope to general state-vs-claim mismatch (tool-call ambiguity, screenshot evidence, unfamiliar territory) and applies it universal-seat rather than just PLINY.

The two disciplines cross-reference; neither subsumes the other. `MAJOR_PLINY.md` §7.2 and `MAJOR_POLYBIUS.md` §4.3 carry a scope-broadening note pointing here.

### 19.5 Empirical lineage

Workspace-tier memory `feedback_no_confabulated_rationales.md` (ariadne-core-workspace, 2026-04-21) was the original anchor at workspace tier. The 2026-05-12 ariadne PLINY incident surfaced the same failure mode in a different shape (tool-call introspection rather than unfamiliar-code rationale invention) and triggered the substrate-tier promotion. Substrate ticket: `stoa--ioy`. Arc 24 (`stoa--cm3`).
```

---

## 6. MAJOR_PLINY.md updates

Three updates: a new §5.8 (dispatch hygiene + canonical poll-loop template per A8); a scope-broadening note added to §7.2 (verify-then-execute) per ioy C4.

### 6.1 New §5.8 — Orchestrator background-dispatch hygiene

Drop-in section, inserted after current §5.7 (Smoke-beat discipline) and before §6 (Communication).

```markdown
### 5.8 Orchestrator background-dispatch hygiene (Arc 24)

When you dispatch a CAPTAIN via `Agent({ run_in_background: true, ... })`, or when you fire a background `Bash` task that needs in-chat status surfaced as it runs, follow this canonical sequence. The discipline closes the orchestrator side of the closed loop whose CAPTAIN side is the heartbeat-and-read-before-write discipline in every CAPTAIN role file. Universal-team framing: `operating-disciplines.md` §18.

#### 5.8.1 Step 1 — At session start: load deferred tools

`ToolSearch` with `select:TaskStop,Monitor,PushNotification` at session start (or first time the orchestrator needs them). This loads their schemas into your context so subsequent invocations work without per-call schema fetches.

`TaskOutput` is **not loaded** by default — deprecated per its own tool description. Do not load it unless a specific legacy bash-polling use case requires it (rare).

#### 5.8.2 Step 2 — At dispatch time: fire Agent + capture task_id + materialize to bw + start Monitor

```
# 1. Fire the Agent in background.
task_result = Agent({ run_in_background: true, ... })
# captures task_id from the returned <task-notification>

# 2. Materialize task_id to bw immediately.
bw comment <dispatch-ticket> "Dispatched <CAPTAIN> at <timestamp>. task_id=<id>. Brief: <link or summary>."

# 3. Start the persistent Monitor that polls bw for new comments.
Monitor({
  command: <canonical bw-poll loop, see §5.8.3 below>,
  description: "watching <CAPTAIN> heartbeats on <dispatch-ticket>",
  persistent: true
})
```

The `task_id` materialization is mandatory at dispatch time. No tool enumerates running background tasks ([issue #29011](https://github.com/anthropics/claude-code/issues/29011), [issue #49140](https://github.com/anthropics/claude-code/issues/49140)); without the bw write at dispatch time, the `task_id` is structurally unrecoverable later in the session.

#### 5.8.3 Step 3 — Canonical bw-poll loop (substrate-canonical template)

```bash
last=$(date -u +%Y-%m-%dT%H:%M:%SZ)
while true; do
  bw show <dispatch-ticket> --json 2>/dev/null \
    | SINCE="$last" python -c "
import sys, json, os
since = os.environ['SINCE']
try:
    d = json.load(sys.stdin)
except Exception:
    sys.exit(0)
for c in d.get('comments', []):
    if c.get('timestamp', '') > since:
        text = c.get('text', '')
        print('[' + c.get('timestamp', '') + '] ' + text[:300].replace('\n', ' '))
" || true
  last=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  sleep 30
done
```

Each new bw comment by the CAPTAIN (or anyone else writing to the dispatch ticket) becomes a stdout line; `Monitor` emits it as an in-chat notification. The orchestrator reads `bw show` for full content when the notification fires. The `|| true` clause prevents transient `bw show` failures (network, lock contention) from killing the monitor mid-engagement.

**The bw JSON schema and the seat-identity convention.** `bw show <id> --json` exposes per-comment `{text, timestamp}` only — no `author` field. The seat identity is carried by the canonical first heartbeat (`"<SEAT> activated on <ticket>"` per the CAPTAIN heartbeat-and-read-before-write discipline) and every subsequent state heartbeat. The stdout line shape is `[<ISO-8601 timestamp>] <comment text, truncated to 300 chars, newlines flattened>`. Truncation at 300 chars is the in-chat notification-friendly bound; the orchestrator reads `bw show` directly for full content when context warrants.

**Why python, not jq.** `jq` is not a universal substrate-tier dependency (empirically absent on Windows Git Bash deployments). Python is, because `bw` itself is python-implemented — every machine that can run `bw` can run `python`. The `--json` contract is the stable parse surface; non-JSON `bw show` output is human-formatted and not a substrate-stable contract.

This template is the substrate-canonical version. MAJOR_POLYBIUS.md §7.6 cross-references it for the rare cases POLYBIUS dispatches CAPTAINs via the `Agent` tool directly. Do NOT invent a per-dispatch variant; copy the template and substitute the dispatch ticket ID.

#### 5.8.4 Step 4 — On CAPTAIN completion: TaskStop the Monitor + read verdict

```
# Wait for the Agent's completion notification (automatic; no polling needed).
# When the notification fires:
TaskStop(<Monitor's task_id>)  # tear down the watcher
# Read the Agent's tool result for the verdict (NOT the .output file).
# Comment the verdict outcome on the parent epic.
```

**Never call `TaskOutput` on a `local_agent` task_id.** `.output` is a symlink to the full sub-agent conversation transcript (JSONL) and overflows the orchestrator's context. For Bash background tasks, `Read` on the output file is the safe path; `TaskOutput` itself remains deprecated.

#### 5.8.5 Step 5 — PushNotification is orthogonal

For events PRINCIPAL needs to act on out-of-band — ship/no-ship verdict ready, blocker requiring human judgment, escalation — fire `PushNotification`. This is **orthogonal** to the orchestrator-CAPTAIN bridge; the bridge uses `Monitor` + bw, not `PushNotification`.

#### 5.8.6 Locked decisions (B1-B6 from `stoa--nvl`)

| ID | Decision |
|---|---|
| B1 | `TaskOutput` forbidden on Agent dispatches (symlink to JSONL transcript overflows context) |
| B2 | `Monitor` is the canonical orchestrator push channel (not poll-cron, not ad-hoc bw poll inside the conversation) |
| B3 | `task_id` materialization to bw is mandatory at dispatch time (no enumeration tool exists) |
| B4 | Canonical poll-loop template lives in this role file; copy per-dispatch with the ticket ID substituted |
| B5 | CAPTAIN-side `Monitor` and `run_in_background: true` Bash are forbidden (re-stated from `stoa--odh` A5) |
| B6 | `PushNotification` is reserved for PRINCIPAL-actionable events only |

#### 5.8.7 Anthropic-side facts (as of 2026-05-12)

- **`Monitor` tool** ([release v2.1.98 on 2026-04-09](https://code.claude.com/docs/en/whats-new/2026-w15)) — shell command whose stdout streams as in-chat notifications. Persistent mode available.
- **`TaskStop` tool** — stops a running background task by `task_id`. Orchestrator can call; CAPTAINs cannot ([issue #23154](https://github.com/anthropics/claude-code/issues/23154)).
- **`TaskOutput`** — deprecated. Agent `.output` is the JSONL transcript symlink.
- **`PushNotification`** — orthogonal user-actionable push.
- **No enumeration tool exists** for running background tasks (issues #29011, #49140).
- **Subagents cannot run `TaskStop`** (issue #23154) — orphan-bug surface; basis for CAPTAIN-side prohibitions.

#### 5.8.8 Empirical anchor

2026-05-12 ariadne PLINY incident — `Agent` dispatch of ADA mid-corpus-authoring without `Monitor` + task_id materialization led to a state-blind orchestrator and a confabulated assertion (verb-level failure captured at `operating-disciplines.md` §19). This section is the structural fix. Substrate ticket: `stoa--nvl`. Arc 24 (`stoa--cm3`).
```

### 6.2 §7.2 — Scope-broadening note for verify-then-execute (per ioy C4)

The existing §7.2 prose remains intact. Append the following at the end of the section, before the `(Arc 9 caught a real directive-author error...)` paragraph:

```markdown
**Scope-broadening (Arc 24 / `stoa--ioy`).** This discipline targets directives that contradict the spec they cite and PRINCIPAL statements relayed via POLYBIUS that contradict your model. The broader case — *any* state-vs-claim mismatch (tool-call ambiguity, screenshot evidence, peer report, unfamiliar concept) — is covered by the universal-seat confabulation discipline at `operating-disciplines.md` §19. The two disciplines complement; neither subsumes the other. Specifically: §7.2 covers "the directive is wrong"; §19 covers "I cannot verify my own assumption against current state — uncertain, checking." Both apply at your seat.
```

---

## 7. MAJOR_POLYBIUS.md updates

Two updates: analogous orchestrator-dispatch-hygiene section §7.6 (per A8 cross-ref to MAJOR_PLINY.md §5.8); confabulation cross-ref appended to §4.3 (verify-then-execute) per A9 LOCKED.

### 7.1 New §7.6 — Orchestrator background-dispatch hygiene (cross-ref form)

Drop-in section, inserted after current §7.5 (Where each tier's beadwork lives) and before §8 (Voice discipline).

```markdown
### 7.6 Orchestrator background-dispatch hygiene (Arc 24)

When POLYBIUS dispatches a CAPTAIN via the `Agent` tool directly — ad-hoc dispatches per §2 / §7 (rare; most CAPTAIN dispatches route through MAJOR_PLINY), or pair-programmer activation flows per §11 — the same orchestrator background-dispatch hygiene applies as for MAJOR_PLINY.

**Canonical reference: `MAJOR_PLINY.md` §5.8.** That section carries the substrate-canonical sequence (load deferred tools at session start; capture `task_id` + materialize to bw + start Monitor; the canonical bash poll-loop template; TaskStop + read verdict on completion; PushNotification orthogonality). POLYBIUS uses the same template when ad-hoc dispatching; the substance and the bash shape are identical, the dispatch ticket ID substitutes per-call.

**Why POLYBIUS does NOT carry the inline template** (per Arc 24 directive A8). One canonical version with a cross-reference avoids wording drift between the two MAJOR files over future arcs. The bash template, the dispatch sequence, the LOCKED B1-B6 decisions, and the Anthropic-side facts are all single-source-of-truth in `MAJOR_PLINY.md` §5.8.

**Universal-team framing**: `operating-disciplines.md` §18.

**Empirical anchor**: 2026-05-12 ariadne PLINY incident; substrate ticket `stoa--nvl`. Arc 24 (`stoa--cm3`).
```

### 7.2 §4.3 — Confabulation cross-ref (per A9 LOCKED)

The existing §4.3 prose remains intact. Append the following at the end of the section:

```markdown
**Scope-broadening (Arc 24 / `stoa--ioy`).** Verify-then-execute targets PRINCIPAL statements and directives that contradict the seat's model. The broader case — any state-vs-claim mismatch (tool-call ambiguity, screenshot evidence, unfamiliar concept, retrospective narrative invented from incomplete evidence) — is covered by the universal-seat confabulation discipline at `operating-disciplines.md` §19. POLYBIUS-specific application: when authoring a TIMING_LOG entry, an arc retrospective, or a synthesis comment on a multi-arc trail, do not invent rationales for behaviors you did not directly observe; admit "uncertain, checking" and verify against the actual ticket trail before promoting the narrative. The 2026-04-21 workspace incident (`feedback_no_confabulated_rationales.md` — PLINY invented a "defense-in-depth" rationale for code PLINY did not author; the rationale propagated into a template future projects would inherit) is the canonical case the discipline guards against.
```

---

## 8. Per-CAPTAIN role file customizations

Each of the 10 CAPTAIN role files receives a heartbeat-and-read-before-write subsection inside its §5 / §6 "Disciplines specific to this seat." The substance is the canonical four-beat + read-before-write structure from §2.1; the wording adapts the state-transition examples to the seat's actual work. **The wording must read consistently across all 10 files** (per directive cross-cutting constraint — ARGUS Phase 1 audits this).

Each subsection number is chosen to fit the seat's existing section numbering without disrupting cross-references. The full verbatim prose follows.

### 8.1 CAPTAIN_VERA — new §5.9 "Heartbeat-and-read-before-write via bw"

Inserted after current §5.8 (STRABO-claim verification) and before §6 (Verdict format).

```markdown
### 5.9 Heartbeat-and-read-before-write via bw

Anthropic's tool surface does not provide mid-execution Agent introspection. The substrate's answer is bw — a substrate we already control. Every CAPTAIN_VERA dispatch follows this comm contract; the orchestrator reads heartbeats via a `Monitor` watching a bw-poll loop (canonical template in `MAJOR_PLINY.md` §5.8). Universal-team framing: `operating-disciplines.md` §18.

Four beats:

1. **At dispatch entry:** `bw comment <dispatch-ticket> "VERA activated on <ticket>. Reading brief + design's verification probes + role file."`
2. **At every state transition** — examples for this seat: "design probes absorbed; classifying p1-p5 per verification-complexity quadrant"; "probe set executing"; "probe p3 falsified — capturing exit code + stderr + falsifying evidence"; "INCOMPLETE verdict on easy-hard probe p5; recording bound used + confidence interval"; "STRABO-claim verification at `sampling: full`; 12 citations resolved, drafting verdict."
3. **At completion, BEFORE returning the tool result:** `bw comment <dispatch-ticket> "<pass | fail | inconclusive>: <one-line summary of which probes ran, which failed if any>. Returning."`
4. **Pull-heartbeat floor: 60 minutes.** If you go heads-down on a long-running probe (e.g., 10× normal probe budget for an INCOMPLETE-quadrant easy-hard case), post a pull-heartbeat at least every 60 minutes. Override allowed per-dispatch.

**Read-before-write:** every `bw comment` write is preceded by `bw show <dispatch-ticket> 2>&1 | tail -<N>` to pick up new comments from the orchestrator. Address anything tagged `[for: VERA]` BEFORE proceeding. This is your only mid-execution interruption surface.

**`bw comment <id> "text"` is POSITIONAL.** Never use `-m`. Cross-ref `operating-disciplines.md` §12.

**`Monitor` is forbidden from this seat.** Firing `Monitor` from inside a CAPTAIN dispatch orphans the Monitor ([issue #23154](https://github.com/anthropics/claude-code/issues/23154)). The orchestrator owns `Monitor`; you heartbeat.

**`run_in_background: true` on Bash is forbidden from this seat.** Same orphan-bug surface. Background work belongs to the orchestrator; if a probe genuinely needs background-style compute (e.g., a 10,000-iteration stress test), name the gap in your verdict and let MAJOR_PLINY dispatch a separate sub-task.
```

### 8.2 CAPTAIN_CATO — new §6.9 "Heartbeat-and-read-before-write via bw"

Inserted after current §6.8 (Empirical environment reproduction) and before §7 (Verdict format).

```markdown
### 6.9 Heartbeat-and-read-before-write via bw

Anthropic's tool surface does not provide mid-execution Agent introspection. The substrate's answer is bw — a substrate we already control. Every CAPTAIN_CATO dispatch follows this comm contract; the orchestrator reads heartbeats via a `Monitor` watching a bw-poll loop (canonical template in `MAJOR_PLINY.md` §5.8). Universal-team framing: `operating-disciplines.md` §18.

Four beats:

1. **At dispatch entry:** `bw comment <dispatch-ticket> "CATO activated on <ticket>. Reading diff + design + VERA verdict before forming cold-read."`
2. **At every state transition** — examples for this seat: "cold-read pass 1 of diff complete; reading design for intent-fit comparison"; "VERA verdict absorbed; meta-verifier coverage check in progress"; "empirical-environment probe at `<command>` complete; results inform §6.8 concern c2"; "authorship-attribution audit complete across diff; no anomalies"; "concerns list drafted; classifying per verification-complexity quadrant before returning."
3. **At completion, BEFORE returning the tool result:** `bw comment <dispatch-ticket> "<pass | revise | refused>: <one-line summary naming blocking concerns if any>. Returning."`
4. **Pull-heartbeat floor: 60 minutes.** If you go heads-down on a large diff (cold-reading 1000+ lines across many files), post a pull-heartbeat at least every 60 minutes.

**Read-before-write:** every `bw comment` write is preceded by `bw show <dispatch-ticket> 2>&1 | tail -<N>` to pick up new comments from the orchestrator. Address anything tagged `[for: CATO]` BEFORE proceeding. This is your only mid-execution interruption surface.

**`bw comment <id> "text"` is POSITIONAL.** Never use `-m`. Cross-ref `operating-disciplines.md` §12.

**`Monitor` is forbidden from this seat.** Firing `Monitor` from inside a CAPTAIN dispatch orphans the Monitor ([issue #23154](https://github.com/anthropics/claude-code/issues/23154)). The orchestrator owns `Monitor`; you heartbeat.

**`run_in_background: true` on Bash is forbidden from this seat.** Same orphan-bug surface. If your empirical-environment probe (§6.8) needs longer-running compute, name the gap in your verdict.
```

### 8.3 CAPTAIN_ARGUS — new §6.7 "Heartbeat-and-read-before-write via bw"

Inserted after current §6.6 (Verification-complexity quadrant per risk) and before §7 (Verdict format).

```markdown
### 6.7 Heartbeat-and-read-before-write via bw

Anthropic's tool surface does not provide mid-execution Agent introspection. The substrate's answer is bw — a substrate we already control. Every CAPTAIN_ARGUS dispatch follows this comm contract; the orchestrator reads heartbeats via a `Monitor` watching a bw-poll loop (canonical template in `MAJOR_PLINY.md` §5.8). Universal-team framing: `operating-disciplines.md` §18.

Four beats:

1. **At dispatch entry:** `bw comment <dispatch-ticket> "ARGUS activated on <ticket>. Reading design artifact end-to-end + cited research before audit."`
2. **At every state transition** — examples for this seat: "design pass 1 complete; 3 candidate risks surfaced for quadrant classification"; "checking cited STRABO research at <path> for citation freshness"; "WebFetch against external API docs cited in design §3"; "risks list drafted, 1 hard-hard for UNVERIFIABLE shaping; auditing DAEDALUS self-assessed weak points before finalizing."
3. **At completion, BEFORE returning the tool result:** `bw comment <dispatch-ticket> "<pass | revise | refused>: <one-line summary; load-bearing risk count if revise>. Returning."`
4. **Pull-heartbeat floor: 60 minutes.** If you go heads-down on a complex design with deep citation-checking, post a pull-heartbeat at least every 60 minutes.

**Read-before-write:** every `bw comment` write is preceded by `bw show <dispatch-ticket> 2>&1 | tail -<N>` to pick up new comments from the orchestrator. Address anything tagged `[for: ARGUS]` BEFORE proceeding. This is your only mid-execution interruption surface.

**`bw comment <id> "text"` is POSITIONAL.** Never use `-m`. Cross-ref `operating-disciplines.md` §12.

**`Monitor` is forbidden from this seat.** Firing `Monitor` from inside a CAPTAIN dispatch orphans the Monitor ([issue #23154](https://github.com/anthropics/claude-code/issues/23154)). The orchestrator owns `Monitor`; you heartbeat.

**`run_in_background: true` on Bash is forbidden from this seat.** Same orphan-bug surface. If a risk requires longer-running probe work to verify (typical for the easy-hard quadrant), name the gap and let MAJOR_PLINY dispatch VERA — that is exactly what the framework's INCOMPLETE-verdict shape is for.
```

### 8.4 CAPTAIN_ZENO — new §6.7 "Heartbeat-and-read-before-write via bw"

Inserted after current §6.6 (Verification-complexity quadrant per criterion) and before §7 (Verdict format).

```markdown
### 6.7 Heartbeat-and-read-before-write via bw

Anthropic's tool surface does not provide mid-execution Agent introspection. The substrate's answer is bw — a substrate we already control. Every CAPTAIN_ZENO dispatch follows this comm contract; the orchestrator reads heartbeats via a `Monitor` watching a bw-poll loop (canonical template in `MAJOR_PLINY.md` §5.8). Universal-team framing: `operating-disciplines.md` §18.

Four beats:

1. **At dispatch entry:** `bw comment <dispatch-ticket> "ZENO activated on <ticket>. Reading spec + shipped artifact before extracting criteria."`
2. **At every state transition** — examples for this seat: "spec criteria extracted; 14 items"; "criterion c1-c4 checked: 4 met, 0 partial"; "criterion c5: partial — evidence captured in verdict"; "auditing artifact for out-of-spec additions before drafting drift list"; "drift list complete, 2 entries; finalizing verdict."
3. **At completion, BEFORE returning the tool result:** `bw comment <dispatch-ticket> "<pass | drift | refused>: <one-line summary; drift count if drift>. Returning."`
4. **Pull-heartbeat floor: 60 minutes.** If you go heads-down on a large spec with many criteria, post a pull-heartbeat at least every 60 minutes.

**Read-before-write:** every `bw comment` write is preceded by `bw show <dispatch-ticket> 2>&1 | tail -<N>` to pick up new comments from the orchestrator. Address anything tagged `[for: ZENO]` BEFORE proceeding. This is your only mid-execution interruption surface.

**`bw comment <id> "text"` is POSITIONAL.** Never use `-m`. Cross-ref `operating-disciplines.md` §12.

**`Monitor` is forbidden from this seat.** Firing `Monitor` from inside a CAPTAIN dispatch orphans the Monitor ([issue #23154](https://github.com/anthropics/claude-code/issues/23154)). The orchestrator owns `Monitor`; you heartbeat.

**`run_in_background: true` on Bash is forbidden from this seat.** Same orphan-bug surface. The seat's mechanical criterion-check work does not need background compute; if a criterion's verification looks like it would (e.g., a long-running stress probe), surface as a `spec_ambiguity:` — that is VERA's quadrant call, not yours.
```

### 8.5 CAPTAIN_ADA — new §5.6 "Heartbeat-and-read-before-write via bw"

Inserted after current §5.5 (Authorship attribution) and before §6 (Verdict format).

```markdown
### 5.6 Heartbeat-and-read-before-write via bw

Anthropic's tool surface does not provide mid-execution Agent introspection. The substrate's answer is bw — a substrate we already control. Every CAPTAIN_ADA dispatch follows this comm contract; the orchestrator reads heartbeats via a `Monitor` watching a bw-poll loop (canonical template in `MAJOR_PLINY.md` §5.8). Universal-team framing: `operating-disciplines.md` §18.

ADA is the seat most likely to have long heads-down generative work (corpus authoring, multi-file refactor, deep substrate edits). The pull-heartbeat floor matters most here — heads-down build sessions can run for hours, and the orchestrator needs visibility into your progress at human cadence.

Four beats:

1. **At dispatch entry:** `bw comment <dispatch-ticket> "ADA activated on <ticket>. Reading design + ARGUS PASS verdict + worktree state before first commit."`
2. **At every state transition** — examples for this seat: "design §1-§3 absorbed; opening worktree at <path>"; "first commit landed at <sha> on branch <name>"; "ground-check pass on design §2.4 against shipped code: no drift"; "design §4 implementation complete; running `tsc --noEmit` build-check (§5.1)"; "build-check passed; iterating on §5"; "build complete; <N> commits across <M> files; drafting verdict."
3. **At completion, BEFORE returning the tool result:** `bw comment <dispatch-ticket> "<pass | partial | refused>: <one-line summary; commits + files-changed counts>. Returning."`
4. **Pull-heartbeat floor: 60 minutes.** This matters especially for ADA — long generative work has natural quiet stretches. Post a pull-heartbeat at least every 60 minutes when you're heads-down without a natural state transition. Per-dispatch override allowed when the engagement justifies it (e.g., a brief authorizing a longer quiet stretch with documented expected duration).

**Read-before-write:** every `bw comment` write is preceded by `bw show <dispatch-ticket> 2>&1 | tail -<N>` to pick up new comments from the orchestrator. Address anything tagged `[for: ADA]` BEFORE proceeding. This is your only mid-execution interruption surface.

**`bw comment <id> "text"` is POSITIONAL.** Never use `-m`. Cross-ref `operating-disciplines.md` §12.

**`Monitor` is forbidden from this seat.** Firing `Monitor` from inside a CAPTAIN dispatch orphans the Monitor ([issue #23154](https://github.com/anthropics/claude-code/issues/23154)). The orchestrator owns `Monitor`; you heartbeat.

**`run_in_background: true` on Bash is forbidden from this seat.** Same orphan-bug surface. If a build step genuinely needs background-style compute (e.g., a long-running test suite that exceeds wall-clock for inline execution), name the gap in your verdict and let MAJOR_PLINY dispatch a separate sub-task. Do not orphan a background process from inside the build — the cleanup path is unreliable.
```

### 8.6 CAPTAIN_DAEDALUS — new §6.5 "Heartbeat-and-read-before-write via bw"

Inserted after current §6.4 (Use WebSearch / WebFetch for live constraints) and before §7 (Verdict format).

```markdown
### 6.5 Heartbeat-and-read-before-write via bw

Anthropic's tool surface does not provide mid-execution Agent introspection. The substrate's answer is bw — a substrate we already control. Every CAPTAIN_DAEDALUS dispatch follows this comm contract; the orchestrator reads heartbeats via a `Monitor` watching a bw-poll loop (canonical template in `MAJOR_PLINY.md` §5.8). Universal-team framing: `operating-disciplines.md` §18.

Four beats:

1. **At dispatch entry:** `bw comment <dispatch-ticket> "DAEDALUS activated on <ticket>. Reading brief + research input (if any) + role file."`
2. **At every state transition** — examples for this seat: "brief absorbed; restatement-gate drafted (§6.1 pre-work)"; "research artifact at <path> consumed end-to-end"; "design §1-§3 drafted; verification probes spec underway"; "self-assessed weak points pass (§6.2 post-work) before returning"; "design draft complete, <N> lines, <M> sections; finalizing verdict."
3. **At completion, BEFORE returning the tool result:** `bw comment <dispatch-ticket> "<pass | partial | refused>: <one-line summary; design path; self-assessed weak point count>. Returning."`
4. **Pull-heartbeat floor: 60 minutes.** If you go heads-down on a deep design (multi-concern arc, large integrated design across several tickets), post a pull-heartbeat at least every 60 minutes.

**Read-before-write:** every `bw comment` write is preceded by `bw show <dispatch-ticket> 2>&1 | tail -<N>` to pick up new comments from the orchestrator. Address anything tagged `[for: DAEDALUS]` BEFORE proceeding. This is your only mid-execution interruption surface.

**`bw comment <id> "text"` is POSITIONAL.** Never use `-m`. Cross-ref `operating-disciplines.md` §12.

**`Monitor` is forbidden from this seat.** Firing `Monitor` from inside a CAPTAIN dispatch orphans the Monitor ([issue #23154](https://github.com/anthropics/claude-code/issues/23154)). The orchestrator owns `Monitor`; you heartbeat.

**`run_in_background: true` on Bash is forbidden from this seat.** Same orphan-bug surface. Design work is in-context; if you find yourself wanting background-style compute, you've likely role-collapsed into ADA-shaped work — refuse back and let MAJOR_PLINY dispatch the right seat.
```

### 8.7 CAPTAIN_STRABO — new §6.7 "Heartbeat-and-read-before-write via bw"

Inserted after current §6.6 (Output is preliminary until VERA-verified) and before §7 (Verdict format).

```markdown
### 6.7 Heartbeat-and-read-before-write via bw

Anthropic's tool surface does not provide mid-execution Agent introspection. The substrate's answer is bw — a substrate we already control. Every CAPTAIN_STRABO dispatch follows this comm contract; the orchestrator reads heartbeats via a `Monitor` watching a bw-poll loop (canonical template in `MAJOR_PLINY.md` §5.8). Universal-team framing: `operating-disciplines.md` §18.

Four beats:

1. **At dispatch entry:** `bw comment <dispatch-ticket> "STRABO activated on <ticket>. Confirming pre-gate (§6.1) — research must be able to change the design decision <X>."`
2. **At every state transition** — examples for this seat: "pre-gate confirmed; research is non-trivial"; "first WebSearch pass complete; <N> candidate sources"; "WebFetch on <url> — fetched <YYYY-MM-DD>; citation captured"; "synthesis draft underway; distinguishing primary from secondary sources"; "verification_status: needs-vera marked (propagation-intended brief)"; "research artifact draft complete; finalizing verdict."
3. **At completion, BEFORE returning the tool result:** `bw comment <dispatch-ticket> "<pass | partial | refused>: <one-line summary; citations count; confidence level>. Returning."`
4. **Pull-heartbeat floor: 60 minutes.** If you go heads-down on a research question with deep citation work, post a pull-heartbeat at least every 60 minutes.

**Read-before-write:** every `bw comment` write is preceded by `bw show <dispatch-ticket> 2>&1 | tail -<N>` to pick up new comments from the orchestrator. Address anything tagged `[for: STRABO]` BEFORE proceeding. This is your only mid-execution interruption surface.

**`bw comment <id> "text"` is POSITIONAL.** Never use `-m`. Cross-ref `operating-disciplines.md` §12.

**`Monitor` is forbidden from this seat.** Firing `Monitor` from inside a CAPTAIN dispatch orphans the Monitor ([issue #23154](https://github.com/anthropics/claude-code/issues/23154)). The orchestrator owns `Monitor`; you heartbeat.

**`run_in_background: true` on Bash is forbidden from this seat.** Same orphan-bug surface. Research work is in-context (WebSearch + WebFetch are foreground tool calls); if you find yourself wanting background-style compute, name the gap in your verdict.
```

### 8.8 CAPTAIN_BARTLEBY — new §6.6 "Heartbeat-and-read-before-write via bw"

Inserted after current §6.5 (Authorship attribution) and before §7 (Verdict format).

```markdown
### 6.6 Heartbeat-and-read-before-write via bw

Anthropic's tool surface does not provide mid-execution Agent introspection. The substrate's answer is bw — a substrate we already control. Every CAPTAIN_BARTLEBY dispatch follows this comm contract; the orchestrator reads heartbeats via a `Monitor` watching a bw-poll loop (canonical template in `MAJOR_PLINY.md` §5.8). Universal-team framing: `operating-disciplines.md` §18.

Four beats:

1. **At dispatch entry:** `bw comment <dispatch-ticket> "BARTLEBY activated on <ticket>. Reading recon question; confirming question is boundable (§6.1)."`
2. **At every state transition** — examples for this seat: "Glob pattern <p> yielded <N> file matches"; "Grep pattern `<expr>` across <path> yielded <N> matches"; "running Read on top 5 for verbatim excerpts"; "findings list at <N> entries; truncating per §6.4 cap"; "writing artifact at <path> for large result set; finalizing verdict."
3. **At completion, BEFORE returning the tool result:** `bw comment <dispatch-ticket> "<pass | refused>: <one-line summary; findings count + truncation status>. Returning."`
4. **Pull-heartbeat floor: 60 minutes.** Recon work is typically fast; the floor rarely fires for this seat. Apply if a long sweep across a large repo runs without natural state transitions.

**Read-before-write:** every `bw comment` write is preceded by `bw show <dispatch-ticket> 2>&1 | tail -<N>` to pick up new comments from the orchestrator. Address anything tagged `[for: BARTLEBY]` BEFORE proceeding. This is your only mid-execution interruption surface.

**`bw comment <id> "text"` is POSITIONAL.** Never use `-m`. Cross-ref `operating-disciplines.md` §12.

**`Monitor` is forbidden from this seat.** Firing `Monitor` from inside a CAPTAIN dispatch orphans the Monitor ([issue #23154](https://github.com/anthropics/claude-code/issues/23154)). The orchestrator owns `Monitor`; you heartbeat.

**`run_in_background: true` on Bash is forbidden from this seat.** Same orphan-bug surface. Recon work is in-context (Grep / Glob / Read are foreground); if a recon question needs longer-running compute (e.g., `git log --all` against a very large repo), name the gap in your verdict.
```

### 8.9 CAPTAIN_CURATOR — new §6.6 "Heartbeat-and-read-before-write via bw"

Inserted after current §6.5 (Authorship attribution) and before §7 (Verdict format).

```markdown
### 6.6 Heartbeat-and-read-before-write via bw

Anthropic's tool surface does not provide mid-execution Agent introspection. The substrate's answer is bw — a substrate we already control. Every CAPTAIN_CURATOR dispatch follows this comm contract; the orchestrator reads heartbeats via a `Monitor` watching a bw-poll loop (canonical template in `MAJOR_PLINY.md` §5.8). Universal-team framing: `operating-disciplines.md` §18.

Four beats:

1. **At dispatch entry:** `bw comment <dispatch-ticket> "CURATOR activated on <ticket>. Reading input ticket set (<N> tickets) before drafting synthesis."`
2. **At every state transition** — examples for this seat: "ticket <id> absorbed (<N/M>)"; "pattern X observed across <K> of <N> inputs"; "drafting observations vs. inferences distinction"; "<M> unfit inputs identified; documenting one-line reasons"; "synthesis draft complete; finalizing verdict."
3. **At completion, BEFORE returning the tool result:** `bw comment <dispatch-ticket> "<pass | partial | refused>: <one-line summary; observation + inference counts>. Returning."`
4. **Pull-heartbeat floor: 60 minutes.** If you go heads-down on a long synthesis (many input tickets, deep retrospective), post a pull-heartbeat at least every 60 minutes.

**Read-before-write:** every `bw comment` write is preceded by `bw show <dispatch-ticket> 2>&1 | tail -<N>` to pick up new comments from the orchestrator. Address anything tagged `[for: CURATOR]` BEFORE proceeding. This is your only mid-execution interruption surface.

**`bw comment <id> "text"` is POSITIONAL.** Never use `-m`. Cross-ref `operating-disciplines.md` §12.

**`Monitor` is forbidden from this seat.** Firing `Monitor` from inside a CAPTAIN dispatch orphans the Monitor ([issue #23154](https://github.com/anthropics/claude-code/issues/23154)). The orchestrator owns `Monitor`; you heartbeat.

**`run_in_background: true` on Bash is forbidden from this seat.** Same orphan-bug surface. Synthesis work is in-context; if you find yourself wanting background-style compute, you've likely role-collapsed into ADA-shaped or VERA-shaped work — refuse back and let MAJOR_PLINY dispatch the right seat.
```

### 8.10 CAPTAIN_HERALD — new §6.5 "Heartbeat-and-read-before-write via bw"

Inserted after current §6.4 (Authorship attribution) and before §7 (Verdict format).

```markdown
### 6.5 Heartbeat-and-read-before-write via bw

Anthropic's tool surface does not provide mid-execution Agent introspection. The substrate's answer is bw — a substrate we already control. Every CAPTAIN_HERALD dispatch follows this comm contract; the orchestrator reads heartbeats via a `Monitor` watching a bw-poll loop (canonical template in `MAJOR_PLINY.md` §5.8). Universal-team framing: `operating-disciplines.md` §18.

Four beats:

1. **At dispatch entry:** `bw comment <dispatch-ticket> "HERALD activated on <ticket>. Reading unstructured request + named project context before drafting brief."`
2. **At every state transition** — examples for this seat: "request restated faithfully"; "known-facts list drafted with sources"; "implied-scope assumptions surfaced"; "<N> ambiguities surfaced for routing"; "suggested pipeline shape: <shape>; finalizing verdict."
3. **At completion, BEFORE returning the tool result:** `bw comment <dispatch-ticket> "<pass | refused>: <one-line summary; ambiguity count + suggested pipeline shape>. Returning."`
4. **Pull-heartbeat floor: 60 minutes.** Intake work is typically short; the floor rarely fires for this seat.

**Read-before-write:** every `bw comment` write is preceded by `bw show <dispatch-ticket> 2>&1 | tail -<N>` to pick up new comments from the orchestrator. Address anything tagged `[for: HERALD]` BEFORE proceeding. This is your only mid-execution interruption surface.

**`bw comment <id> "text"` is POSITIONAL.** Never use `-m`. Cross-ref `operating-disciplines.md` §12.

**`Monitor` is forbidden from this seat.** Firing `Monitor` from inside a CAPTAIN dispatch orphans the Monitor ([issue #23154](https://github.com/anthropics/claude-code/issues/23154)). The orchestrator owns `Monitor`; you heartbeat.

**`run_in_background: true` on Bash is forbidden from this seat.** Same orphan-bug surface. Intake work is in-context (Read + Grep + Glob foreground); background-style compute is not in scope.
```

### 8.11 Wording-consistency contract for ADA / ARGUS Phase 1 audit + CATO Phase 3 audit

The 10 subsections above share the following invariant skeleton. The contract distinguishes **strict-verbatim** paragraphs (no per-seat variance permitted; CATO Phase 3 mechanically diffs across files) from **template paragraphs with named per-seat slots** (variance permitted only at named slots; CATO Phase 3 audits the slots fit the seat). Drift outside the named slots is a defect. The contract is precise so CATO's cold-read can audit mechanically against it, not by judgment.

**Strict-verbatim paragraphs** (must match byte-for-byte across all 10 CAPTAIN files except for the named `<SEAT>` substitution where indicated):

1. **First paragraph** (opening + cross-refs): `Anthropic's tool surface does not provide mid-execution Agent introspection. The substrate's answer is bw — a substrate we already control. Every CAPTAIN_<SEAT> dispatch follows this comm contract; the orchestrator reads heartbeats via a `Monitor` watching a bw-poll loop (canonical template in `MAJOR_PLINY.md` §5.8). Universal-team framing: `operating-disciplines.md` §18.` Only `<SEAT>` is substituted per file.
2. **"Four beats:" header.** Literal string.
3. **Read-before-write paragraph:** `**Read-before-write:** every `bw comment` write is preceded by `bw show <dispatch-ticket> 2>&1 | tail -<N>` to pick up new comments from the orchestrator. Address anything tagged `[for: <SEAT>]` BEFORE proceeding. This is your only mid-execution interruption surface.` Only `<SEAT>` is substituted.
4. **`bw comment` POSITIONAL paragraph:** `**`bw comment <id> "text"` is POSITIONAL.** Never use `-m`. Cross-ref `operating-disciplines.md` §12.` Identical across all 10 files.
5. **`Monitor` forbidden paragraph:** `**`Monitor` is forbidden from this seat.** Firing `Monitor` from inside a CAPTAIN dispatch orphans the Monitor ([issue #23154](https://github.com/anthropics/claude-code/issues/23154)). The orchestrator owns `Monitor`; you heartbeat.` Identical across all 10 files.

**Template paragraphs with named per-seat slots** (variance permitted only at the named slot):

6. **Optional second paragraph** for seats where the heartbeat floor matters extra: present ONLY for ADA's long generative work; the other 9 seats omit. The presence/absence is itself the slot — when present, the paragraph follows ADA's specific shape verbatim. (Future seats that justify the extra paragraph must inherit ADA's exact wording adapted to the seat's heads-down work; this is a high-bar slot, not a free-form addition.)
7. **Beat 1** (`At dispatch entry:`): structure `bw comment <dispatch-ticket> "<SEAT> activated on <ticket>. <seat-specific read-before-act statement>."` Slots: `<SEAT>` (per file) and the read-before-act statement (per seat — "Reading brief + role file"; "Reading design + ARGUS PASS verdict + worktree state before first commit"; etc.).
8. **Beat 2** (`At every state transition — examples for this seat:`): the lead-in `**At every state transition** — examples for this seat:` is verbatim; the example list is per-seat.
9. **Beat 3** (`At completion, BEFORE returning the tool result:`): structure `**At completion, BEFORE returning the tool result:** \`bw comment <dispatch-ticket> "<verdict-tokens>: <one-line summary; <seat-specific summary tail>>. Returning."\`` Slot: the verdict tokens (`pass | partial | refused` for design/build seats; `pass | revise | refused` for critic/cold-read seats; `pass | fail | inconclusive` for VERA; `pass | drift | refused` for ZENO; `pass | refused` for BARTLEBY/HERALD) and the seat-specific summary tail.
10. **Beat 4** (`Pull-heartbeat floor: 60 minutes.`): structure `**Pull-heartbeat floor: 60 minutes.** <seat-specific applicability note>.` The floor sentence is verbatim; the applicability note is per-seat (BARTLEBY/HERALD note "rarely fires for this seat"; ADA notes "matters especially for ADA"; etc.).
11. **`run_in_background: true` forbidden paragraph:** structure `**`run_in_background: true` on Bash is forbidden from this seat.** Same orphan-bug surface. <seat-specific tail clause about where the background compute would have gone, what to do instead>.` Slot: the seat-specific tail clause.

**Lost-nuance items deliberately stripped from per-seat prose** (to keep the strict-verbatim contract enforceable):

- **Peer-CAPTAIN coverage of read-before-write.** The Read-before-write paragraph says "new comments from the orchestrator" — but peer-CAPTAIN comments addressed `[for: <SEAT>]` are equally in-scope. This is named in `operating-disciplines.md` §18.2 (universal-team framing): "the read picks up any new comments from the orchestrator (or peer CAPTAINs) since the last check." Per-seat prose says "orchestrator" for brevity; the §18 cross-ref carries the full scope. CATO Phase 3 audits §18 once, not 10 times.
- **Orphan-mechanism explanation for `Monitor` forbidden.** The per-seat paragraph cites issue #23154 without explaining the orphan mechanism (notifications land in a dead conversation; spawned process leaks). The mechanism is explained once in `operating-disciplines.md` §18.4 (universal-team framing) and once in §2.1 of this design (the canonical template basis). Per-seat prose stays compact; the §18 cross-ref carries the mechanism.
- **Stakes-specific consequence for ADA's mid-execution interruption surface.** The previous draft had ADA's Read-before-write paragraph add "(the orchestrator cannot push-interrupt a running CAPTAIN; the only hard-abort is `TaskStop`, and the build state would be lost)." This stakes-context applies universally (every CAPTAIN's mid-execution state is lost under `TaskStop`); it is named once in `operating-disciplines.md` §18.3 (universal-team framing: "Cooperative yield is the only mid-execution interruption surface"). Per-seat prose stays compact; ADA's specific build-state stakes are implicit from ADA's role-file context, not load-bearing for the discipline statement.

**CATO Phase 3 audit pattern.** Mechanically diff paragraphs 1, 2, 3, 4, 5 byte-for-byte across all 10 CAPTAIN files; any non-`<SEAT>`-slot variance is a defect. Audit paragraphs 6-11 against the named slots; variance outside the slots is a defect; per-seat customization at the slots is by-design. This makes wording-consistency a mechanical check, not a judgment call.

---

## 9. agent-author template / skill scaffold updates (A7)

### 9.1 A7 DAEDALUS-pick — scaffold scope decision

**Decision:** Update `substrate/skills/agent-author/SKILL.md` in two narrow ways. The smaller change is load-bearing equivalent to a larger restructure — the discipline's substantive home is `operating-disciplines.md` §18 (which any new CAPTAIN's role file naturally cross-references); the skill's job is to ensure the cross-reference and the canonical subsection both land in the new agent's draft.

**Reasoning:** The skill mechanizes section-by-section substitution. The heartbeat-and-read-before-write subsection is now a structural piece of every CAPTAIN role file (per §8 above). For future CAPTAINs spawned via this skill to inherit the discipline, the procedure section must:

1. Name the discipline as a section the new agent inherits (procedure step 3, mirroring how §4 disciplines inheritance is already preserved verbatim).
2. Add a voice-discipline-check entry for the discipline's presence in the draft (so a draft missing the section is flagged).

A new section in the skill would bloat without value; cross-referencing operating-disciplines.md §18 is sufficient. Substrate-wide one-source-of-truth: the discipline lives in §18 + each CAPTAIN role file's heartbeat subsection. The skill's job is to ensure new CAPTAIN drafts carry the subsection.

### 9.2 Skill update — procedure step 3 (additional bullet)

Insert into procedure step 3 ("Draft the new role file by structural substitution"), after the existing bullet about §4 disciplines inheritance, the following:

```markdown
   - **For new CAPTAINs:** preserve the heartbeat-and-read-before-write subsection from the template basis verbatim, customizing only the seat name and the state-transition examples per the seat's actual work. The discipline's substantive home is `operating-disciplines.md` §18 (Subagent status via bw + orchestrator dispatch hygiene); cross-reference it from the new subsection's first paragraph (canonical opening sentence in §18 of operating-disciplines.md). The substance is universal-CAPTAIN; the wording adapts per seat (probe execution for VERA-shaped seats; build phases for ADA-shaped seats; review phases for CATO-shaped seats; etc.). Wording drift across CAPTAIN role files is the most likely defect class — author one canonical subsection from the template basis and customize, do not re-derive from scratch.
```

### 9.3 Skill update — voice-discipline-check table

Append to the §"Voice discipline check" table (after the existing 4 rows):

```markdown
| Missing heartbeat-and-read-before-write subsection (new CAPTAIN drafts only) | Read for presence of the canonical opening sentence "Anthropic's tool surface does not provide mid-execution Agent introspection. The substrate's answer is bw — a substrate we already control." in the disciplines section | If missing in a new CAPTAIN draft, copy the subsection from the closest-fit template basis and customize for the new seat; cross-ref `operating-disciplines.md` §18 |
```

And append to the practical tooling block (after the existing `grep -ni` commands):

```bash
# Heartbeat-subsection presence — CAPTAIN drafts only.
grep -n "Anthropic's tool surface does not provide mid-execution Agent introspection" <draft-path>
```

### 9.4 What this skill update is NOT

Per the existing "What this skill is NOT" section, the skill does not deploy, rename, or edit `install.sh`. The skill update preserves that scope: the skill ensures new CAPTAIN drafts inherit the discipline; it does not edit existing CAPTAINs, deploy them, or modify install.sh.

---

## 10. Self-referential acknowledgment (worked example, not circular)

This arc modifies the role files of the very seats authoring and verifying it. DAEDALUS (this seat) is authoring the design that updates `CAPTAIN_DAEDALUS.md`. ARGUS will Phase-1-audit the design that updates `CAPTAIN_ARGUS.md`. ADA will Phase-2-build edits to `CAPTAIN_ADA.md`. VERA + CATO + ZENO will Phase-3-verify against role files that have already been updated to require heartbeat-and-read-before-write — which the verifiers themselves will be using on their own dispatches.

**This is not a circular dependency. It is substrate updating itself in flight.**

The structural property that prevents circularity:

- The role files are deployed copies from substrate at session start. The Arc 24 CAPTAINs dispatched today are operating per the role files at Arc-23 ship time (7ecdbef) — they do NOT yet carry the heartbeat-and-read-before-write subsection.
- The Phase 1 dispatch (this DAEDALUS dispatch) is therefore operating per the *pre-Arc-24* role file, which does not require heartbeat. But the directive explicitly requires me to apply the discipline anyway (per the dispatch-paste's "heartbeat-and-read-before-write discipline (the discipline you are designing IS the discipline you operate under)" section). I am operating per the *post-Arc-24* discipline before the discipline is shipped.
- Phase 2 ADA edits substrate; Phase 3 verifiers read the *edited* substrate to verify. The verifiers' OWN role-file edits are part of the diff they are verifying — they audit substrate that includes their own subsection.

The honest framing for a cold reader: Arc 24 is the canonical worked example of "substrate updating itself." Every CAPTAIN dispatched in Arc 24 reads the *new* version of its own role file during verification, with the new heartbeat discipline as part of its baseline. The CAPTAINs operate per the new discipline as they help author it. Self-referential, not circular — the dependency runs one direction (substrate-now → substrate-next), and each phase's dispatch happens against a coherent snapshot.

**The discipline this arc builds IS the discipline this arc uses.** Per the directive comment on `stoa--cm3` (2026-05-12T23:06:32Z): "Self-referential acknowledgment per directive: the discipline being authored IS the discipline the dispatched CAPTAINs are using. ARGUS Phase 1 audit will confirm this is a feature, not a defect."

The worked-example value: future arcs that update substrate-in-flight can point to Arc 24 as the canonical case study for the pattern.

---

## 11. Probes for VERA (Phase 3 verification)

Per Arc 23's verification-complexity quadrant framework (`operating-disciplines.md` §15), each probe is classified. The classification informs VERA's verdict shape (PASS / FAIL / INCOMPLETE / UNVERIFIABLE).

### 11.1 Per-file string-match probes (easy-easy quadrant)

| Probe ID | File | Search | Expected | Quadrant |
|---|---|---|---|---|
| p1 | `substrate/operating-disciplines.md` | grep `^## 18\. Subagent status via bw` | exactly 1 match | easy-easy |
| p2 | `substrate/operating-disciplines.md` | grep `^## 19\. Confabulation-under-uncertainty discipline` | exactly 1 match | easy-easy |
| p3 | `substrate/operating-disciplines.md` | grep `^### 18\.1 Half 1 (upward)` through `### 18.6 Empirical lineage` | 6 subsection headers (18.1 - 18.6) | easy-easy |
| p4 | `substrate/operating-disciplines.md` | grep `^### 19\.1` through `### 19.5 Empirical lineage` | 5 subsection headers (19.1 - 19.5) | easy-easy |
| p5 | `substrate/MAJOR_PLINY.md` | grep `^### 5\.8 Orchestrator background-dispatch hygiene` | exactly 1 match | easy-easy |
| p6 | `substrate/MAJOR_PLINY.md` | grep `^#### 5\.8\.[1-8] ` | 8 sub-subsection headers (5.8.1 - 5.8.8) | easy-easy |
| p7 | `substrate/MAJOR_PLINY.md` | grep `last=\$\(date -u \+%Y-%m-%dT%H:%M:%SZ\)` | exactly 1 match (canonical poll-loop opening line) | easy-easy |
| p8 | `substrate/MAJOR_PLINY.md` §7.2 | grep `Scope-broadening (Arc 24 / \`stoa--ioy\`)` | exactly 1 match | easy-easy |
| p9 | `substrate/MAJOR_POLYBIUS.md` | grep `^### 7\.6 Orchestrator background-dispatch hygiene` | exactly 1 match | easy-easy |
| p10 | `substrate/MAJOR_POLYBIUS.md` §7.6 | grep `Canonical reference: \`MAJOR_PLINY.md\` §5.8` | exactly 1 match | easy-easy |
| p11 | `substrate/MAJOR_POLYBIUS.md` §4.3 | grep `Scope-broadening (Arc 24 / \`stoa--ioy\`)` | exactly 1 match | easy-easy |
| p12-p21 | Each CAPTAIN file (VERA, CATO, ARGUS, ZENO, ADA, DAEDALUS, STRABO, BARTLEBY, CURATOR, HERALD) | grep `Heartbeat-and-read-before-write via bw` AND `Anthropic's tool surface does not provide mid-execution Agent introspection` | exactly 1 match each per file (10 files total) | easy-easy |
| p22-p31 | Each CAPTAIN file | grep `\`Monitor\` is forbidden from this seat` | exactly 1 match per file | easy-easy |
| p32-p41 | Each CAPTAIN file | grep `\`run_in_background: true\` on Bash is forbidden from this seat` | exactly 1 match per file | easy-easy |
| p42 | `substrate/skills/agent-author/SKILL.md` | grep `For new CAPTAINs:.*heartbeat-and-read-before-write` | exactly 1 match | easy-easy |
| p43 | `substrate/skills/agent-author/SKILL.md` voice-check section | grep `Missing heartbeat-and-read-before-write subsection` | exactly 1 match | easy-easy |

### 11.2 Empirical poll-loop probe (easy-easy quadrant; the worked example of Arc 23 framework)

**Probe p44** — execute the canonical poll-loop template from `MAJOR_PLINY.md` §5.8.3 against a real bw ticket (`stoa--cm3`) and confirm new comments emit one stdout line each.

**Quadrant:** easy-easy. **Setup:** start the bash loop with `<dispatch-ticket>` substituted to `stoa--cm3`. **Trigger:** `bw comment stoa--cm3 "test heartbeat from VERA probe p44"`. **Expected:** within ~30s (the `sleep 30` interval), one line emits to stdout matching the shape `[<ISO-8601 timestamp>] test heartbeat from VERA probe p44` (e.g., `[2026-05-12T23:47:12Z] test heartbeat from VERA probe p44`). The bw JSON schema is `{text, timestamp}` per comment with no `author` field, so the timestamp + leading text are the verification surface; the seat identity is carried inside the text payload by the heartbeat-discipline convention. **Falsifying evidence:** no line emits within 60s, OR the `last=` cursor does not advance and the next test comment produces duplicate output, OR the line emits but with empty interior (which would indicate the python parse silently swallowed the comment — would mean the template ships broken). **Cleanup:** kill the bash loop after probe completes.

This probe IS the worked example of the Arc 23 verification-complexity framework: an easy-easy probe against the new arc's most load-bearing piece of bash. PASS confirms the canonical template runs correctly against bw's actual JSON output shape; FAIL surfaces a bash-syntax or python-syntax error that ARGUS Phase 1 critique should have caught (and didn't, if it lands here).

### 11.3 Forbid-clause prohibition probes (easy-easy quadrant)

**Probe p45** — confirm CAPTAIN role files do NOT contain a counter-example phrasing that would silently neutralize the Monitor / run_in_background prohibitions. Grep each CAPTAIN file for `Monitor.*if.*needed` or `run_in_background.*allowed.*when` — both should return zero matches.

### 11.4 Wording-consistency probe (hard-hard quadrant — UNVERIFIABLE-leaning)

**Probe p46** — verify all 10 CAPTAIN files carry consistent heartbeat-subsection wording (the invariant skeleton in §8.11 above). The §8.11 contract distinguishes strict-verbatim paragraphs (1, 2, 3, 4, 5 — see §8.11) from named-slot template paragraphs (6-11); the mechanical diff lands on the strict-verbatim 5, and the slot-fit check lands on 6-11.

**Quadrant:** **hard-hard / UNVERIFIABLE-leaning.** The check is bounded only by "I read all 10 files at this snapshot." VERA can execute mechanical diff-of-equivalent-lines (extracting the first paragraph from each subsection and confirming it matches verbatim), the Monitor-forbidden paragraph (confirming it matches verbatim), and the run_in_background-forbidden paragraph (matching except seat-specific tail clause). That bounded check is easy-quadrant.

But the broader claim "every CAPTAIN is consistently updated" is **unbounded in three ways:**

1. **Future CAPTAINs.** Arc 24 ships 10 CAPTAINs; future arcs may add an 11th, 12th. The wording-consistency claim would need re-verification on every future CAPTAIN add. VERA's check at Arc 24 ship time cannot anticipate that.
2. **Per-seat customization correctness.** The state-transition examples are seat-specific and judgment-bound. VERA can check "the section exists" but cannot mechanically check "the examples are correct for this seat" without ARGUS-level design judgment (i.e., the verification would need DAEDALUS-shaped or CATO-shaped review, not VERA-shaped probe execution).
3. **Tone-drift.** "Consistent" can mean exact-match verbatim (mechanical) or "reads consistently to a cold reader" (judgment). The mechanical interpretation lands easy-quadrant; the judgment interpretation lands hard-hard.

**Honest verdict shape per Arc 23 §15:** INCOMPLETE with explicit bound — "verified the verbatim-skeleton invariant across 10 files at Arc 24 ship time per the §8.11 contract; bound is the 10 files in substrate as of <commit-sha>; future CAPTAIN adds require re-verification per the same protocol; per-seat customization correctness is OUT of this probe's scope and routed to CATO's cold-read."

VERA classifies this honestly; the verdict shape Arc 23 just landed (INCOMPLETE / UNVERIFIABLE) is the right tool. This probe is the worked example of "name the unbounded property rather than manufacture a confidence number."

### 11.5 Probe coverage summary

| Quadrant | Probe IDs | Probe count | Verdict shape if all pass |
|---|---|---|---|
| easy-easy (mechanical string match + structural) | p1-p11 (11) + p12-p21 (10) + p22-p31 (10) + p32-p41 (10) + p42 + p43 + p45 | 44 | PASS |
| easy-easy (empirical execution of bash poll-loop) | p44 | 1 | PASS |
| hard-hard (UNVERIFIABLE-leaning wording consistency) | p46 | 1 | INCOMPLETE (with verbatim-skeleton-invariant bound documented) |

**Total: 46 probes** (11 + 10 + 10 + 10 + 1 + 1 + 1 + 1 + 1 = 46). Standard mechanical pass produces 45 PASS + 1 INCOMPLETE. INCOMPLETE does NOT gate merge per `operating-disciplines.md` §15.4 — it surfaces to PLINY for operator disposition.

Arithmetic-check (so ARGUS / VERA can re-audit): the per-CAPTAIN rows (p12-p21, p22-p31, p32-p41) each cover 10 files via a single row in §11.1, but the probe count is **one per file**, so each row contributes 10 to the total — not 1. That convention is what makes the §11.1 table dense; the §11.5 summary unrolls it.

---

## 12. Smoke beats for Phase 4 (PLINY ship)

Per `operating-disciplines.md` §8.4 (substrate-edit smoke beats) and the Arc 24 directive's Phase 4 section.

### 12.1 install.sh dry-run lists every modified substrate file

The arc modifies these substrate files (no new files added, so install.sh's hardcoded deploy-list arrays — `TEMPLATE_NAMES`, `CAPTAIN_NAMES`, `SKILL_NAMES` — should already include every touched file). Smoke beats per `operating-disciplines.md` §8.4:

```bash
bash substrate/install.sh --dry-run --target project --project-dir <test-dir>
bash substrate/install.sh --dry-run --target subproject --parent-dir <test-parent> --subproject <slug>
bash substrate/install.sh --dry-run --target user
```

For each invocation, every modified file should appear in the deploy plan output. Acceptance: file-by-file presence verification — pipe each invocation through `grep` against the expected file names. Per §8.4, since Arc 24 adds no new files (only edits existing), the deploy plan should already include them; an absent file is an install.sh wiring regression.

### 12.2 Markdown validation

Markdown-lint or equivalent on every touched file:

- `substrate/operating-disciplines.md`
- `substrate/MAJOR_PLINY.md`
- `substrate/MAJOR_POLYBIUS.md`
- `substrate/CAPTAIN_VERA.md`, `CAPTAIN_CATO.md`, `CAPTAIN_ARGUS.md`, `CAPTAIN_ZENO.md`, `CAPTAIN_ADA.md`, `CAPTAIN_DAEDALUS.md`, `CAPTAIN_STRABO.md`, `CAPTAIN_BARTLEBY.md`, `CAPTAIN_CURATOR.md`, `CAPTAIN_HERALD.md`
- `substrate/skills/agent-author/SKILL.md`

Acceptance: no markdown-validation errors. Headings nest correctly (no skipped levels). Tables are valid. Code fences close.

### 12.3 Grep beats per file

```bash
# Heartbeat subsection presence in every CAPTAIN file.
grep -l "Heartbeat-and-read-before-write via bw" substrate/CAPTAIN_*.md | wc -l   # expect 10

# Canonical opening sentence presence in every CAPTAIN file.
grep -l "Anthropic's tool surface does not provide mid-execution Agent introspection" substrate/CAPTAIN_*.md | wc -l   # expect 10

# Monitor + run_in_background forbid-clauses in every CAPTAIN file.
grep -l "\`Monitor\` is forbidden from this seat" substrate/CAPTAIN_*.md | wc -l   # expect 10
grep -l "\`run_in_background: true\` on Bash is forbidden from this seat" substrate/CAPTAIN_*.md | wc -l   # expect 10

# Canonical poll-loop template in MAJOR_PLINY.md.
grep -n "last=\$(date -u +%Y-%m-%dT%H:%M:%SZ)" substrate/MAJOR_PLINY.md   # expect 1 line

# §18 + §19 in operating-disciplines.md.
grep -n "^## 18\. Subagent status via bw" substrate/operating-disciplines.md   # expect 1
grep -n "^## 19\. Confabulation-under-uncertainty discipline" substrate/operating-disciplines.md   # expect 1

# Confabulation cue presence in §19.
grep -n "uncertain, checking" substrate/operating-disciplines.md   # expect ≥ 1 match in §19

# Cross-ref scope-broadening note in MAJOR_PLINY.md §7.2 and MAJOR_POLYBIUS.md §4.3.
grep -n "Scope-broadening (Arc 24 / \`stoa--ioy\`)" substrate/MAJOR_PLINY.md   # expect 1
grep -n "Scope-broadening (Arc 24 / \`stoa--ioy\`)" substrate/MAJOR_POLYBIUS.md   # expect 1

# agent-author skill update.
grep -n "For new CAPTAINs:" substrate/skills/agent-author/SKILL.md   # expect 1
grep -n "Missing heartbeat-and-read-before-write subsection" substrate/skills/agent-author/SKILL.md   # expect 1
```

### 12.4 Empirical poll-loop execution against `stoa--cm3`

Same as VERA's probe p44 (§11.2), executed once at Phase 4 ship time as the final smoke beat:

1. Open a bash session; copy the canonical poll-loop template from `MAJOR_PLINY.md` §5.8.3.
2. Substitute `<dispatch-ticket>` with `stoa--cm3`.
3. Start the loop in the background (orchestrator-tier; PLINY may use `run_in_background: true` Bash from MAJOR tier — the prohibition is CAPTAIN-side only).
4. Fire a test comment: `bw comment stoa--cm3 "Phase 4 smoke — canonical poll-loop empirical test"`.
5. Within ~30s, expect one stdout line matching the test comment.
6. Kill the bash loop.

Acceptance: stdout line emits within 60s. The empirical test confirms the canonical template runs against bw's real JSON output shape, not just a synthesized example.

---

## 13. Self-flagged weak points

Per Arc 23's design-discipline pattern (`u--7yg` cluster) and DAEDALUS §6.2 (Self-assessed weak points): I name the brittle spots I see; ARGUS Phase 1 names the risks I missed. Honest middle, not over-apologizing.

### 13.1 Wording-consistency drift across 10 CAPTAIN files is the most likely defect class

**Weak point:** The §8 customizations rely on ADA preserving the §8.11 invariant skeleton verbatim across 10 files while customizing seat-specific examples. The canonical opening sentence, the Monitor-forbidden paragraph, and the run_in_background-forbidden paragraph must read identically; the four-beat structure and beat 1/3/4 wording must match except seat names. ARGUS will Phase-1-audit the design for the invariant; ADA will Phase-2-build against 10 files; CATO will Phase-3-cold-read; VERA's probe p46 lands INCOMPLETE-leaning on this. **Three defenses** make it survivable:

1. §8.11 names the invariant skeleton explicitly so ARGUS / CATO / VERA have a contract to check against, not a vibe.
2. ADA receives 10 nearly-identical subsections from this design — copying-and-customizing is mechanical, not generative.
3. CATO cold-reads the entire diff and is the meta-verifier for VERA's quadrant-classified probes (per Arc 23 §6.7); wording drift across files is exactly the defect class CATO catches.

**Why this shape anyway:** the alternative (a single referenced canonical subsection that every CAPTAIN's role file points at, rather than per-CAPTAIN inline subsections) was considered. Rejected because it leaves the CAPTAIN role files without a self-contained statement of the discipline that travels with the seat — a cold reader of `CAPTAIN_VERA.md` would not see the discipline without chasing a cross-reference. The substrate's existing pattern (per-seat disciplines inlined with operating-disciplines.md cross-refs) is preserved.

### 13.2 The self-referential property (substrate updating itself in flight) is genuinely novel

**Weak point:** Arc 24 modifies role files of the seats authoring and verifying it. §10 above documents this as a worked example, not circular; the dependency runs one direction (substrate-now → substrate-next). But this is the first arc where the verifying CAPTAINs are reading edits to their OWN role files — VERA verifying the edit to `CAPTAIN_VERA.md`, CATO reviewing the edit to `CAPTAIN_CATO.md`. The framework Arc 23 just landed (INCOMPLETE / UNVERIFIABLE quadrants) helps because VERA can honestly classify "verifying my own role file's edits" as a specific verification-complexity claim. But the meta-structural property — verifiers verifying their own role files — does not have prior empirical anchor at substrate-tier.

**Why this shape anyway:** Refusing to ship Arc 24 because the verifiers' role files are part of the diff would prevent the substrate from ever updating its verifier seats. The honest framing in §10 (worked example, dependency direction documented, snapshot-at-phase-boundary) is the structural answer. The discipline being authored IS the discipline being used; the directive explicitly acknowledges this and calls it a feature. ARGUS Phase 1 will audit whether §10's framing is sufficient.

### 13.3 Confabulation-discipline phrasing that itself sounds confabulated (irony surface)

**Weak point:** §4 + §19 prose about "uncertain, checking" risks landing as a confident-sounding rule that itself does not admit uncertainty. The discipline is verb-level; the prose specifying it can drift into the assertive register the discipline argues against. ARGUS will Phase-1-audit for this irony surface.

**Why this shape anyway:** Substrate prose is necessarily prescriptive — operating-disciplines.md does not hedge ("we usually think it's a good idea to verify-then-execute"), it states ("verify-then-execute is the discipline"). The confabulation section is the same shape. The discipline applies to first-person prose IN THE LIVE WORK (a CAPTAIN's running narrative; PLINY's response to "is ADA stuck?"); it does NOT apply to substrate prose specifying the discipline. The two registers are distinct. §19.1's split into "the verbal admission + the verification action" makes this explicit: the discipline is about first-person register at runtime, not third-person register in substrate canon. **Defended.**

### 13.4 A8 inline-one + cross-reference invites a stale cross-reference in MAJOR_POLYBIUS.md §7.6

**Weak point:** §7.6 in MAJOR_POLYBIUS.md cross-references `MAJOR_PLINY.md` §5.8 as the canonical template source. If a future arc renumbers MAJOR_PLINY.md's sections (e.g., adds a §5.9 that pushes the dispatch-hygiene section to §5.9 or §6), the cross-reference in MAJOR_POLYBIUS.md §7.6 silently goes stale. The substrate has no automated cross-reference checker.

**Why this shape anyway:** The alternative (inlining the bash template in both MAJOR files) trades one defect class (stale cross-reference) for a worse one (wording drift between two near-identical bash templates over future arcs). Cross-references rot less often than parallel verbatim copies of code drift; the empirical record in operating-disciplines.md confirms this (many cross-references; few have rotted vs. the parallel-prose drift cluster in `stoa--bxx`). The narrow defense: future arcs that renumber MAJOR_PLINY.md sections must `grep -rn "MAJOR_PLINY.md §5.8" substrate/` to catch and update any stale cross-references. This is a generic substrate-edit discipline that should already be in scope for substrate-touching arcs.

### 13.5 The 60-min pull-heartbeat floor is calibrated from ONE empirical anchor (N=1)

**Weak point:** The 60-min default (per A3a, calibrated 2026-05-12 by PRINCIPAL) comes from one engagement: the 2026-05-12 ariadne ADA factory-corpus generation. Per `operating-disciplines.md` §6.7.1 (N=1 rule), structural claims about pipeline safety require multiple observations across distinct defect classes. The 60-min floor is technically a single-observation calibration; future arcs may surface that 60 min is too long (real ADA stalls go undetected for an hour) or too short (heads-down generative work gets pull-heartbeats it doesn't need).

**Why this shape anyway:** The 60-min floor is operationalized as a default with per-dispatch override allowed in both directions (tighter for interactive arcs; looser with documented expected duration). This is explicitly the §6.7.1 "operational choice for this engagement, not extrapolation from prior catches" pattern: the orchestrator scopes the cadence per-dispatch when the engagement warrants. The default is a starting point, not a structural claim. Future arcs that surface 60-min being wrong can re-calibrate via the normal accretion path (a new substrate-discipline ticket promoting evidence to canon).

---

## 14. Verdict

Verdict: **revised-r2 (r5 + r6 addressed)**

Revision round 2 (DAEDALUS, 2026-05-12, post-ARGUS-re-audit). Both ARGUS r5+r6 load-bearing risks addressed; see §14.2 below for the per-risk change summary. Revision-r1 verdict was **revised (R1-R4 addressed)**; ARGUS re-audit returned REVISE-r2 with two new load-bearing fixes introduced by the r1 revision (r5: §3.1 Step 3 vs §6.1 §5.8.3 template-divergence — env-var prefix in wrong position causes runtime KeyError; r6: stale probe cross-refs at lines 1035/1054 missed by R4 renumbering). This r2 revision addresses both and surfaces back for re-audit. The five self-flagged weak points in §13 remain valid (none discharged by this revision; none added).

Restatement: Arc 24 ships comms-hygiene as substrate DNA — every CAPTAIN heartbeats progress via bw on its dispatch ticket; every orchestrator monitors via Monitor + bw-poll bridge with canonical inline template; every seat says "uncertain, checking" when state-vs-claim mismatch surfaces. The integrated design covers all three tickets (`stoa--odh`, `stoa--nvl`, `stoa--ioy`) with a single coherent gauntlet across the substrate's comms-architecture, tooling-discipline, and verb-level-discipline failure modes.

### 14.1 Revision-round-1 changes (post-ARGUS-cold-audit)

**R1 + R2 (load-bearing): canonical bw-poll-loop template referenced nonexistent JSON fields + used `jq` which is not installed.**

- Empirically probed: `bw show --json` exposes per-comment `{text, timestamp}` only (no `author` field); `jq` is absent from PATH on Windows Git Bash deployment; `python` 3.11 is present.
- **Recovery shape DAEDALUS picked: shape (b), python-based template.** Rationale: python is universal (bw is python-implemented; any machine that runs bw runs python), zero added install.sh dependency, JSON contract is the substrate-stable parse surface. Rejected: shape (a) jq-as-substrate-dependency (per-platform install matrix; new install.sh failure mode); shape (c) non-JSON `bw show` parsing (human-readable format is not a substrate-stable contract).
- Rewrote the canonical poll-loop template in both inline locations: **§3.1 Step 3** (design's primary canonical-template anchor) and **§6.1 §5.8.3** (the MAJOR_PLINY.md drop-in). Template now uses `python -c` with `os.environ['SINCE']` for the since-cursor passed via the `SINCE=...` env var on the pipeline.
- Added explanatory note in both locations: "**The seat identity is carried by the heartbeat text itself**" — explaining the schema (text + timestamp only) and the convention (canonical first heartbeat names the seat: `"<SEAT> activated on <ticket>"`). Output line shape documented: `[<ISO-8601 timestamp>] <comment text, truncated to 300 chars, newlines flattened>`.
- Added "Why python, not jq" subsection in both locations documenting the rejected alternatives (jq-substrate-dep, non-JSON parsing) so future arcs see the trade-off explicitly.
- Empirically validated the rewritten template against live `stoa--cm3` ticket: the python pipeline emits the expected `[<ts>] <text>` shape correctly on real bw output.
- Updated probe **p44** (formerly p35) expected-output text to match the new template's `[<timestamp>] <text>` shape (was the broken `[<author> <timestamp>] <body>` shape); added explicit falsifying-evidence clause "OR the line emits but with empty interior (would mean the template ships broken)" to catch the R1-class failure if it regresses.
- Updated the §11.2 + §12 references to "bash-syntax or jq-syntax error" → "bash-syntax or python-syntax error."

**R3: §8.11 wording-consistency contract internally inconsistent with §8 prose.**

- Empirically audited all 10 CAPTAIN files' Read-before-write paragraphs and Monitor-forbidden paragraphs for drift. Confirmed ARGUS's 3 specific drift findings: VERA's "from the orchestrator **or peer CAPTAINs**" + parenthetical extension; ADA's parenthetical extension + "spawned poll-loop leaks" vs "process leaks"; VERA's Monitor-forbidden "notifications land in a dead conversation; spawned process leaks" extra clause; ADA's Monitor-forbidden "the spawned poll-loop leaks" variant.
- **Recovery shape DAEDALUS picked: shape (b), strict-verbatim alignment.** Rationale: maximizes CATO Phase 3 auditability — wording-consistency becomes a mechanical byte-for-byte diff, not a judgment call. Lost-nuance items (peer-CAPTAIN coverage, ADA build-state stakes, orphan-mechanism explanation) move to `operating-disciplines.md` §18 (universal-team framing) where they're authored once.
- Aligned VERA + ADA Read-before-write paragraphs to the strict canonical form (verbatim except seat name in `[for: <SEAT>]`); aligned VERA + ADA Monitor-forbidden paragraphs to the strict short form. All 10 CAPTAIN files now share byte-for-byte identical Read-before-write and Monitor-forbidden paragraphs (modulo `<SEAT>` substitution).
- **Rewrote §8.11 contract** into two explicit classes: (1) strict-verbatim paragraphs (1, 2, 3, 4, 5 — first paragraph, "Four beats:" header, Read-before-write, `bw comment` POSITIONAL, Monitor forbidden) where any non-`<SEAT>`-slot variance is a defect; (2) named-slot template paragraphs (6-11 — optional second paragraph, beats 1/2/3/4, `run_in_background` forbidden) where variance is permitted ONLY at the named slot. Added a "lost-nuance items deliberately stripped" subsection naming the three items moved to §18 cross-refs and where they live. Added CATO Phase 3 audit pattern: mechanical diff for strict-verbatim, slot-fit check for named-slot.

**R4: §11 probe-numbering had duplicate IDs + arithmetic errors.**

- Confirmed the duplicate-ID overlap: previous rows were `p22-p31` (Monitor-forbidden, 10 files) and `p23-p32` (run_in_background-forbidden, 10 files) — 9 colliding IDs p23-p31.
- Renumbered probes consecutively: p1-p11 (individual, unchanged); p12-p21 (per-CAPTAIN subsection-presence, 10 IDs, unchanged); p22-p31 (per-CAPTAIN Monitor-forbidden, 10 IDs, unchanged); **p32-p41** (per-CAPTAIN run_in_background-forbidden, 10 IDs, renumbered from `p23-p32`); **p42** (was p33, SKILL.md For-new-CAPTAINs); **p43** (was p34, SKILL.md voice-check row); **p44** (was p35, empirical poll-loop); **p45** (was p36, forbid-clause prohibition); **p46** (was p37, wording-consistency).
- Rewrote §11.5 summary table with explicit probe-ID enumeration per row + corrected count: easy-easy mechanical (p1-p11 + p12-p21 + p22-p31 + p32-p41 + p42 + p43 + p45) = 11 + 10 + 10 + 10 + 1 + 1 + 1 = 44 probes; easy-easy empirical (p44) = 1 probe; hard-hard UNVERIFIABLE-leaning (p46) = 1 probe; **TOTAL: 46 probes** (was wrongly stated as 37). Added arithmetic-check paragraph naming the per-CAPTAIN row convention (one row = 10 files = 10 probes) so future re-audits don't re-collapse the math.

**Heartbeat audit for this revision dispatch:** activation heartbeat fired at 23:25:45Z; R1+R2-in-flight heartbeat at 23:26:25Z; R1+R2-done / R3-in-flight at 23:27:33Z; R3-done / R4-in-flight at heartbeat time T; revision-r1 verdict heartbeat fires immediately before this dispatch returns. Read-before-write fired before each heartbeat. No comments tagged `[for: DAEDALUS]` surfaced; no orchestrator interruption during revision.

DAEDALUS-picks (informed by the design constraint set, defended in their respective sections):

- **A4** — two new top-level sections in operating-disciplines.md (§18 subagent status via bw + orchestrator dispatch hygiene; §19 confabulation discipline). Cold-reader-legible; preserves §7's POLYBIUS-pair-coordination scope.
- **A7** — narrow update to `substrate/skills/agent-author/SKILL.md`: a bullet in procedure step 3 + a voice-discipline-check row + a tooling grep. Cross-ref to `operating-disciplines.md` §18 rather than inlining the discipline in the skill.
- **A10** — keep "uncertain, checking" as the canonical phrasing, with explicit equivalents documented. Two-beat structure (admit + commit).
- **A8** — inline canonical bash poll-loop template in `MAJOR_PLINY.md` §5.8.3; `MAJOR_POLYBIUS.md` §7.6 cross-references it. Single source of truth.

**Residual questions for ARGUS:**

1. Is the §8.11 wording-consistency contract precise enough that ARGUS / CATO / VERA can audit it mechanically across 10 files? (My read: yes — the invariant skeleton is enumerated; drift outside it is the defect class. ARGUS to confirm.)
2. Is the §10 self-referential framing (substrate updating itself in flight) sufficient defense against the meta-structural risk in §13.2? (My read: yes — the dependency direction is named, the snapshot-at-phase-boundary is explicit, the directive explicitly acknowledges this as a feature. ARGUS to audit for cold-reader confusion.)
3. Is the 60-min floor in §2.2 underspecified for the per-dispatch override mechanism? (My read: the override mechanism is named — "orchestrator sets in the dispatch brief" — but the brief schema for the cadence override is not specified. Defensible because it's a default-plus-override pattern, but ARGUS may want a concrete brief-field name.)

**Follow-ups (out of scope for Arc 24):**

- Automated cross-reference checking across substrate (named risk in §13.4; not Arc 24's scope per directive Out-of-scope list).
- Implementing automated confabulation detection (out of substrate per directive Out-of-scope).
- Building Anthropic-side tooling for Agent introspection (Anthropic's surface; out of substrate).

### 14.2 Revision-round-2 changes (post-ARGUS-re-audit)

**r5 (LOAD-BEARING — ironic wording-drift instance the §8.11 contract was meant to guard against): §3.1 Step 3 canonical poll-loop template diverged from the §6.1 §5.8.3 copy.**

- **The defect.** §3.1 Step 3 (formerly line 154) placed `SINCE="$last"` AFTER the closing quote of `python -c "..."`, making it argv[1] (silently ignored by python in `-c` mode) — `os.environ['SINCE']` raises `KeyError: 'SINCE'` at runtime. The §6.1 §5.8.3 copy (line 447) placed `SINCE="$last"` BEFORE `python -c` (env-var prefix idiom) — works correctly. Two near-identical canonical templates with diverged shell syntax: the exact wording-drift class §8.11 names as Arc 24's most likely defect surfaced inside the design that defines §8.11. Empirically reproduced by ARGUS (KeyError); empirically the broken §3 form would have shipped to ADA as the canonical template.
- **The fix.** Edited §3.1 Step 3 to match §6.1 §5.8.3 byte-for-byte: moved `SINCE="$last"` from the trailing argv position to the env-var-prefix position before `python -c`. Both copies now diff-clean (`diff <(sed -n '139,158p' ...) <(sed -n '443,462p' ...)` → empty output).
- **Empirical verification.** Ran the rewritten §3.1 Step 3 one-liner against live `bw show stoa--cm3 --json`: emits non-empty stdout, one line per existing comment, correct `[<ISO-8601 timestamp>] <text>` shape. The template now actually works as substrate-canonical, not just as a documentation artifact.
- **Why this regression class can't recur.** Both copies are now byte-for-byte identical (modulo surrounding markdown context); any future edit to one that diverges from the other will fail the `diff` mechanical check. Recommend ADA Phase 2 lift the canonical template into a single source-of-truth location (a substrate skill or a single referenced file) and reference it from both §3.1 and §6.1 §5.8.3 sites — that defense lives in §13.4's automated-cross-reference-checking weak point and is already in the Arc 25+ follow-up queue.

**r6 (LOAD-BEARING — stale cross-refs from R4 renumbering): two probe-ID references not updated by R4.**

- **The defect.** R4 renumbered probes p33→p42, p34→p43, p35→p44, p36→p45, p37→p46. The §11.1 + §11.5 + §14.1 sites were updated; two §13 cross-refs were missed: line 1035 (§12.4) referenced "VERA's probe p35 (§11.2)" — should be p44; line 1054 (§13.1) referenced "VERA's probe p37 lands INCOMPLETE-leaning on this" — should be p46. VERA Phase 3 + Phase 4 smoke routing would silently break on the stale IDs (no probe p35/p37 exists in the renumbered table).
- **The fix.** Edited line 1035: `p35` → `p44`. Edited line 1054: `p37` → `p46`.
- **Sanity-check sweep.** Ran `grep -n -E '\bp(22|23|24|25|26|27|28|29|30|31|32|33|34|35|36|37)\b' agents/design/arc-24/design.md` to catch any other stale references R4 left behind. All remaining `p22-p37` matches are legitimate: §11.1 table-header range expressions (`p22-p31`, `p32-p41`), §11.5 summary range expressions, and the §14.1 R4 changelog explicitly documenting the renumbering history (e.g., "**p44** (was p35, empirical poll-loop)"). No stale cross-refs survive.

**Heartbeat audit for this revision dispatch:** activation heartbeat fired at the entry beat; verdict heartbeat fires immediately before this dispatch returns. Read-before-write fired before each heartbeat (`bw show stoa--cm3 2>&1 | tail -40`). No comments tagged `[for: DAEDALUS]` surfaced; no orchestrator interruption during revision.

**Residual questions for ARGUS re-audit (r2):**

1. The byte-for-byte-identical-canonical-templates defense is mechanical for ARGUS to verify (`diff`). Is the §13.4 follow-up (single-source-of-truth lift, automated cross-reference checking) the right Arc 25+ work to permanently retire this defect class, or should it be Arc 24 in-scope work? My read: out-of-scope per directive's Out-of-scope list; Arc 25+ is the right home. ARGUS to confirm.
2. The grep sweep covered p22-p37; the renumbering moved p33-p37 to p42-p46, so the relevant defect class is "stale references to old IDs" only in that range. Is there an analogous risk for the unchanged ranges (p1-p21, p22-p31) — i.e., did R4 inadvertently break a reference that was correct before? My read: no — R4 left p1-p21 + p22-p31 unchanged; only p23-p32 (run_in_background row) and p33-p37 (post-row probes) were renumbered. ARGUS to confirm via spot-check.

Per A11 IMMUTABLE: all edits credit **Denson Smith**. No author field gets a different name. No exception.

---

*End of design. Per the directive's Phase 1 spec, this surfaces to MAJOR_PLINY for routing to ARGUS Phase 1 audit. ARGUS verdict gates ADA dispatch.*
