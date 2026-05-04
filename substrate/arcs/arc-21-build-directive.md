# Arc 21 build directive — POLYBIUS-pair coordination protocol + downstream-handoff discipline

**Audience:** the fresh Claude Code session opened to build Arc 21 deliverables (MAJOR_PLINY).
**Authored by:** project-tier MAJOR_POLYBIUS (the-stoa) + the PRINCIPAL (Denson Smith).
**Status:** active directive.
**Bw ticket:** `stoa--pbz`.
**Builds on:** Arcs 1-20 (the-stoa main `e5c2854`). Arc 20 closed the user-tier install convention; Arc 21 hardens the cross-tier coordination + downstream-handoff disciplines surfaced when those installs went live.

**Your one job:** land five empirical disciplines into substrate so every future POLYBIUS instance inherits them. The disciplines all surfaced during the ariadne--m20 autonomous-mode coordination on 2026-05-04 (closed at `a161630` in workspace bw); each is concrete, anchored to a lived moment, and currently captured only in user-tier feedback memories that don't propagate.

This is a multi-concern arc (two distinct deliverable parts). Per MAJOR_POLYBIUS §5.4, external review (CAPTAIN_ARGUS cold-audit) ran on this directive before dispatch — incorporated revisions are reflected in the locked decisions below.

---

## Comms — direct async via bw

POLYBIUS will be polling `stoa--pbz` while you work. Surface-and-wait discipline (Arc 18): poll only when you've surfaced a question and are waiting on a response. Otherwise execute autonomously.

bw command syntax: `bw comment <id> "text"` — positional, no `-m` flag.

---

## Read first

1. **`substrate/operating-disciplines.md`** — the team-wide disciplines doc (landed `de8fecd` via stoa--vz9). You'll add §7 (coordination protocol) and §8 (positive-references-only) here.
2. **`substrate/MAJOR_POLYBIUS.md`** — current source of truth for §5.1 (paste-instruction templating), §7.1 (visibility), §7.4 (polling capability + consent). You'll edit all three sections.
3. **`substrate/MAJOR_PLINY.md`** — confirm whether PLINY has any bw-write conventions that need parallel clarification (§7.1 write-boundary work). Likely no-op; verify and report.
4. **`substrate/install.sh`** — current `next-steps` output block (lines ~850-893 per stoa--xh2 reference). You'll restructure this block to make the activation paste prominent and mode-correct.
5. **`substrate/templates/paste-instruction-template.md`** — current template; audit for negative-framing language; rewrite if any present.
6. **stoa-- ticket bodies** for the five children: `bw show stoa--ivc`, `bw show stoa--ay1`, `bw show stoa--blg`, `bw show stoa--xh2`, `bw show stoa--m5m`. Each carries the empirical anchor and the proposed substrate shape. Read them before designing.
7. **ariadne--m20 thread** (workspace bw, closed) — `cd /c/Users/denso/claude_projects/ariadne-core-workspace && bw show ariadne--m20`. The radio-check protocol was demonstrated live in this thread (initialization handshake `21:08:17Z` + `21:10:02Z`, periodic heartbeats, closure handshake `21:21:43Z` + `21:28:35Z`). The lived sequence is the case study for §7.

---

## Phase A — Architectural decisions (LOCKED pre-dispatch by POLYBIUS)

You do NOT need to surface these as Phase A calls. Settled during directive authoring.

### A1. One arc, two parts — LOCKED

The two parts are distinct concerns but share substrate touchpoints (operating-disciplines.md, MAJOR_POLYBIUS.md §5.1/§7.1/§7.4, install.sh, templates/). Bundling reduces churn; §5.4 external review covers the multi-concern risk.

### A2. operating-disciplines.md is the canonical home for universal team patterns — LOCKED

Where a discipline applies to any seat (POLYBIUS, PLINY, pair-programmer Major) coordinating async via bw — it goes in operating-disciplines.md. Where it's POLYBIUS-specific (e.g., the §5.1 paste-templating discipline applies to POLYBIUS authoring activation pastes, not to anyone else), it stays in MAJOR_POLYBIUS.md.

Mapping:
- Radio-check + adaptive cadence + cross-tier-write-boundaries → operating-disciplines.md (universal team protocol)
- MAJOR_POLYBIUS §7.1 expansion → role-file (POLYBIUS-tier-specific framing of the universal rule, with a back-reference to operating-disciplines.md)
- Positive-references-only → operating-disciplines.md (any seat authoring a downstream brief) AND a §5.5 cross-reference in MAJOR_POLYBIUS for the activation-paste-specific application
- Activation-paste cheatsheet → substrate/templates/ (operational reference, not a discipline)

### A3. Polling cron prompt template — LOCKED as substrate/templates/polling-cron-prompt-template.md

A reusable template for the cron prompt POLYBIUS configures when polling a shared coordination ticket. Includes radio-check loop logic (heartbeat, alarm-on-silence, closure handshake) AND cadence-tag detection (active/default/quiet). The ad-hoc form in `HUMAN_relay_m20_autonomous_mode_2026-05-04.md` is the input; the template is the substrate-shipped form.

### A4. Cadence-switching is per-seat, not negotiated — LOCKED

Each peer reads complexity tags on incoming comments and adjusts ITS OWN cron unilaterally. There is no negotiation protocol.

**Worst-case staleness, named explicitly:**
- **Cadence-down** (active → default → quiet): both peers converge within one cycle of the new (slower) cadence. Bounded; not pathological.
- **Cadence-up** (quiet → active because complexity tag posted): the peer still on the slower cadence will not see the tag for up to one full cycle of its CURRENT cadence. If the current cadence is `*/30`, the active section runs at degraded responsiveness for up to 30 minutes before the second peer notices. This is the scenario PRINCIPAL flagged in stoa--ay1 ("impatience during active windows"), and it is NOT eliminated by the protocol — only bounded.

**Why we accept this:** the alternative (a synchronization protocol where peers negotiate cadence-up) is more failure-prone than the bounded delay. A handshake adds a per-transition round-trip and a new error class (orphaned cadence states if handshake fails). Protocol-induced bugs cost more than bounded staleness.

**Mitigation the doc must surface:** when a complexity tag is posted, the POSTING peer should ALSO post an explicit `[cadence: active]` comment on the same fire — that signals the new regime via two channels (tag + cadence-comment), reducing the chance a slow-cadence peer misses the transition. Worst-case staleness is unchanged; perceived responsiveness improves.

ARGUS critique surfaced this risk; the resolution is "bounded staleness is acceptable, name it explicitly so PRINCIPAL can calibrate expectations during active windows, and document the dual-channel mitigation."

### A5. Cloud cron is documented limitation, not a deliverable — LOCKED

Cloud scheduled tasks have a 1-hour minimum cadence; active/quiet regimes don't apply. The substrate doc names this limitation explicitly and points to the workaround (single fixed-hourly cloud cron + escalation to local active-cadence cron). No cloud-cron template ships in Arc 21.

### A6. Voice — LOCKED: PRINCIPAL/HUMAN throughout

All new substrate content uses PRINCIPAL/HUMAN. Reflexive leakage to "the user" or "Colonel" is a v1 regression — voice-discipline grep is part of VERA's verification (zero hits on `\b[Cc]olonel\b` and `\bthe user\b` outside template-slot examples).

### A7. install.sh next-steps restructure — LOCKED (with mode-aware activation)

The next-steps block prints a clearly demarcated ACTIVATION block per `--target` mode. **There are two activation PATTERNS, not one** (ARGUS cold-audit catch):

- **Auto-load pattern** — for `--target user` and `--target project --modify-claude-md`. CLAUDE.md references the role file; opening Claude in the activation dir auto-loads the role file's content into context, but the role's persona is triggered by saying "POLYBIUS" or "chief of staff" in-session. There is NO multi-line paste; the activation step is a verbal trigger.

- **Paste pattern** — for `--target project` (without `--modify-claude-md`) and `--target subproject`. No CLAUDE.md ref exists, so the role file does not auto-load. The activation step is a literal paste: `Read .claude/MAJOR_POLYBIUS<NAME_SUFFIX>.md and assume the role for this <project|sub-project>.`

**The current install.sh has a bug here:** lines 887-911 use `if [ "$TARGET" = "subproject" ]` to gate paste-pattern output, lumping `--target project` (with or without `--modify-claude-md`) into the auto-load branch. This silently fails for `--target project` without `--modify-claude-md` — the user is told to "say POLYBIUS" but no CLAUDE.md ref exists, so saying POLYBIUS does nothing. Fix this in B.5: gate on `($TARGET = subproject) OR ($TARGET = project AND MODIFY_CLAUDE_MD = 0)` for the paste branch.

Demarcation pattern (auto-load case):

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

Demarcation pattern (paste case):

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

The cheatsheet (B.3) is the authoritative four-pattern table; install.sh's per-mode output is generated from the same source-of-truth (don't drift).

---

## Deliverables

### Part A — POLYBIUS-pair coordination protocol

#### A.1 `substrate/operating-disciplines.md` — add §7 (coordination protocol)

**Location:** `the-stoa/substrate/operating-disciplines.md`

**Edit:** append a new top-level section after §6 (single-checker thinking) and before the "Agent-regime inverses" closer. Title: `## 7. Coordinating two POLYBIUS seats async via bw polling`.

**Required content (in order):**

1. **Framing** (~3-5 lines): when two POLYBIUS seats — typically user-tier + project-tier, or parent + sub-project — share a coordination ticket, polling makes bw a near-real-time async channel. Three sub-disciplines apply: peer-failure detection (radio-check), responsiveness adjustment (adaptive cadence), and explicit write boundaries.

2. **§7.1 Radio-check protocol** — covers stoa--ivc:
   - Initialization handshake (each seat posts `[radio-check <seat>]` naming cron id + cadence; both ack on first poll)
   - Routine heartbeats (every ≤30 min)
   - Missed-check escalation (peer silent > 60 min AND ticket open → surface to PRINCIPAL as "lost contact with peer")
   - Closure handshake (both sides post final standing-down + CronDelete on shared ticket close)
   - Cite ariadne--m20 timestamps as empirical anchor (initialization at 21:08-21:10, closure at 21:21-21:28).

3. **§7.2 Adaptive polling cadence** — covers stoa--ay1:
   - Three regimes: active (`*/2`), default (`*/5`), quiet (`*/15-30`)
   - Complexity tags on comments: `[complexity: simple|medium|complex]`
   - Cadence-switching is per-seat, unilateral (per A4); peers converge within one cycle
   - Cost framing (fires/hour) and net-cost argument
   - Cloud-cron limitation per A5 — name the 1-hour minimum and the escalation-to-local-cron workaround.

4. **§7.3 Cross-tier write boundaries** — covers stoa--blg:
   - The implicit-but-unstated rule (table form, **same shape as MAJOR_POLYBIUS.md §7.1** — the two are the canonical pair):

     | Seat | Reads | Writes |
     |---|---|---|
     | User-tier POLYBIUS | u-- + all project-tier (downward) | u-- + all project-tier (downward) |
     | Project-tier (workspace, sub-project) | own project bw | own project bw |

   - Coordination always meets in the lower tier's bw. User-tier descends; project-tier never ascends.
   - Why: the asymmetric scoping is what keeps each tier's working memory bounded; project-tier writing to u-- accumulates cross-project context that defeats the bounded-context property.
   - Read-exception: project-tier work that is system-architecture-shaped may PULL user-tier bw as input (read-only); never write up. Mirror of MAJOR_POLYBIUS §7.1 read-exception.
   - **Cross-ref to MAJOR_POLYBIUS §7.1:** "MAJOR_POLYBIUS §7.1 carries the same rule framed for the POLYBIUS seat specifically; this section is the universal-team layer." Bidirectional pointer with §7.1's cross-ref to here.
   - Empirical anchor: 2026-05-04 PRINCIPAL caught a proposal that had workspace POLYBIUS polling u-- — the proposal was wrong; the correction is now in substrate.

5. **Empirical lineage subsection** at the end of §7 — three-line note: "The radio-check + adaptive-cadence + write-boundary disciplines surfaced together during the ariadne--m20 autonomous-mode coordination on 2026-05-04. The lived sequence (handshake, heartbeats, write-boundary catch by PRINCIPAL, closure handshake) is the case study; this section is its codification."

**Length target:** ~80-120 lines for the whole §7 block. Tight prose; tables where they earn it; cross-refs back to MAJOR_POLYBIUS §7.4 for the polling-capability framing that this builds on.

#### A.2 `substrate/MAJOR_POLYBIUS.md` §7.1 — expand visibility into read+write rules (reconcile Exception clause)

**Location:** `substrate/MAJOR_POLYBIUS.md` lines 246-252 (current §7.1 block).

**Edit:** restructure the existing visibility text into a read-AND-write rules block. Use a table mirroring operating-disciplines.md §7.3 (consistent shape; one canonical source for the rule, two readers).

Current §7.1 says only that user-tier sees project-tier and not vice-versa, with an "Exception" clause at line 250 ("project-tier work that is system-architecture-shaped (a meta-team arc) may pull from user-tier beadwork as input"). The Exception is READ-only by intent ("pull as input"), but the new write-rules table risks contradicting it unless the Exception is explicitly scoped to reads.

New §7.1 says:

| Seat | Reads | Writes |
|---|---|---|
| User-tier POLYBIUS | u-- + all project-tier (downward) | u-- + all project-tier (downward) |
| Project-tier POLYBIUS (workspace, sub-project) | own project bw | own project bw |

Plus the following bullets:

- "Cross-tier coordination meets in the lower tier's bw. User-tier descends to coordinate; project-tier never ascends. The asymmetric scoping keeps each tier's working memory bounded — see operating-disciplines.md §7.3 for the universal-team framing."

- "**Read-exception (preserved from prior §7.1):** project-tier work that is system-architecture-shaped (a meta-team arc) may PULL from user-tier beadwork as input. This is a READ-only exception — never a write exception. The 'never ascends' rule on writes holds without exception. If a project-tier seat ever needs to write upward, the correct path is: surface to PRINCIPAL, who relays via user-tier."

- "Recursive asymmetry (preserved): parent-project sees sub-project beadworks; sub-project does not see parent's by default. The same read-exception + no-write-up rule applies recursively."

The reconciliation is mechanical: keep the substance of the old Exception, but explicitly mark it READ-only and contrast it against the no-write-up rule.

#### A.3 `substrate/MAJOR_POLYBIUS.md` §7.4 — cross-ref to operating-disciplines.md §7 + reference template by name

**Location:** `substrate/MAJOR_POLYBIUS.md` §7.4 (lines ~291-303).

**Edit:** two changes:

1. **At the end of §7.4** add a single paragraph referencing the new operating-disciplines.md §7 for the radio-check + adaptive-cadence protocols. §7.4 stays focused on the polling-capability + consent discipline (POLYBIUS-specific); §7 in operating-disciplines.md handles the coordination protocol details (any seat doing peer-polling).

   Cross-ref text:

   > When you set up polling for a coordination engagement with another POLYBIUS seat — peer-to-peer rather than one-shot — the radio-check + adaptive-cadence + write-boundary protocols in operating-disciplines.md §7 apply. Read those before scheduling the cron; the polling-cron-prompt template at `substrate/templates/polling-cron-prompt-template.md` wires the radio-check loop into the cron prompt directly.

2. **In the existing "What the cron prompt does at each fire" paragraph** (current lines ~301-302), update the prose to reference the template by NAME — not just by path — so a future POLYBIUS reading §7.4 has the canonical reference name. Suggested edit: change "Self-contained instructions to read the relevant bw tickets..." to "The polling-cron-prompt template (substrate/templates/polling-cron-prompt-template.md) provides the canonical fire-loop: read the relevant bw tickets..."

This addresses stoa--ivc Acceptance: "cron prompts referenced by name in role files."

#### A.4 `substrate/templates/polling-cron-prompt-template.md` (new file)

**Location:** `the-stoa/substrate/templates/polling-cron-prompt-template.md` — new file.

**Required content:**

1. **Header / purpose** (~5 lines): what this template is for; when POLYBIUS uses it; how it's customized per engagement.
2. **Slots:**
   - `{{COORDINATION_TICKET}}` — bw ticket id of the shared ticket
   - `{{PEER_SEAT_NAME}}` — descriptive name of the peer (e.g., "workspace POLYBIUS", "user-tier POLYBIUS")
   - `{{SELF_SEAT_NAME}}` — own seat descriptive name
   - `{{CRON_ID}}` — the cron id this prompt is wired to (filled in after CronCreate returns)
   - `{{ALARM_THRESHOLD_MINUTES}}` — default 60
   - `{{HEARTBEAT_INTERVAL_MINUTES}}` — default 30
3. **Cron prompt template body** with the radio-check loop logic spelled out as ordered steps:
   - STEP 1: substantive read (check coordination ticket for new comments since last poll)
   - STEP 2: peer-silence escalation (if peer's last activity > {{ALARM_THRESHOLD_MINUTES}} min, surface "lost contact with {{PEER_SEAT_NAME}}" to PRINCIPAL)
   - STEP 3: self-radio-check refresh (if own last activity > {{HEARTBEAT_INTERVAL_MINUTES}} min, post `[radio-check {{SELF_SEAT_NAME}}]` comment)
   - STEP 4: cadence-tag detection (read latest comment for `[complexity: ...]`; if regime change, CronDelete this cron + CronCreate new at the new cadence; record new cron id; post handover comment)
   - STEP 5: closure detection (if {{COORDINATION_TICKET}} status is `closed`, post final `[radio-check {{SELF_SEAT_NAME}} standing down]` + CronDelete this cron + exit loop)
4. **Usage example** at the end (~10 lines): a worked example of the template filled out for a hypothetical engagement, showing how POLYBIUS adapts the template for a specific shared ticket. **DO NOT cite ariadne--m20 directly** — the m20 thread lives in workspace bw, which the the-stoa build session cannot read per §7.1 visibility rules. Use a sketch with placeholder names (e.g., shared ticket `<example>--abc`, peers "user-tier POLYBIUS" and "workspace POLYBIUS"). The empirical lineage citation belongs in operating-disciplines.md §7 (A.1), where it's a passing reference, not a worked example.

**Length: MUST be 80-120 lines.** Length target is a hard constraint — under 80 means the template is missing required sections; over 120 means it has bloated past usable single-page reference shape.

### Part B — Downstream-handoff discipline

#### B.1 `substrate/MAJOR_POLYBIUS.md` §5.1 — add positive-references-only subdiscipline

**Location:** `substrate/MAJOR_POLYBIUS.md` §5.1 (lines 181-194).

**Edit:** at the end of §5.1, add a new subsection (~15-20 lines) introducing the positive-references-only discipline as it applies to authoring activation pastes for downstream agents. Cross-ref to operating-disciplines.md §8 for the universal-team framing (which lands in B.4).

Required content:
- The rule: when filling template slots for `{{SESSION_INTENT}}`, `{{PENDING_DIRECTIVES}}`, etc., reference only POSITIVE resources the downstream agent should use. Never reference resources the agent shouldn't reach for, even with `NOT` or `EXCEPT` qualifiers.
- The empirical anchor: the-stoa install paste authored 2026-05-04 said "Run `bw prime` in this directory (NOT user-beadwork)". The "NOT user-beadwork" parenthetical seeded awareness of user-tier bw into a session that wouldn't otherwise have known about it. PRINCIPAL caught it.
- The reasoning (3-4 lines): the asymmetric scoping in §7.1 is an information-flow rule. Project-tier agents don't know user-tier bw exists by default. A directive that says "don't reach for u--" destroys that invisibility — it teaches the agent that u-- exists and where to find it, which under pressure can be rationalized into "this is a legitimate exception."
- One worked example pair (positive vs negative form) — full table lives in operating-disciplines.md §8.

#### B.2 `substrate/MAJOR_POLYBIUS.md` §5.5 (new subsection)

**Location:** `substrate/MAJOR_POLYBIUS.md` — insert a new §5.5 after §5.4 (External directive review for multi-concern arcs).

**Required content (~15-20 lines):**

Title: `### 5.5 Activation paste filenames vary by install mode — use the cheatsheet`

Body: install.sh deploys MAJOR files with different filename suffixes depending on `--target`:
- `--target user` and `--target project`: MAJORs are UNSUFFIXED (e.g., `MAJOR_POLYBIUS.md`)
- `--target subproject`: MAJORs are SUFFIXED with the slug (e.g., `MAJOR_POLYBIUS_<slug>.md`)
- CAPTAINs are ALWAYS suffixed when there's a slug (project + subproject)

The activation paste must match the deployed filename. The four mode-paste pairs are the canonical reference at `substrate/templates/activation-paste-cheatsheet.md` — consult before authoring any activation paste.

Empirical anchor: the-stoa install on 2026-05-04 failed silently because the activation paste used the suffixed filename for a project-mode install (which deploys unsuffixed). Session activated as wrong tier, hit wrong bw store, PRINCIPAL caught it.

Cross-ref the cheatsheet (B.3 below).

#### B.3 `substrate/templates/activation-paste-cheatsheet.md` (new file)

**Location:** `the-stoa/substrate/templates/activation-paste-cheatsheet.md` — new file.

**Required content:**

Single-page reference. **Two activation patterns, four mode rows** (ARGUS cold-audit catch — the column is "Activation pattern", not "Activation paste"; auto-load cases use a SAY-trigger, not a paste):

| `--target` | `--modify-claude-md`? | MAJOR filename | CLAUDE.md auto-load? | Activation pattern |
|---|---|---|---|---|
| `user` | yes (default) | `MAJOR_POLYBIUS.md` at `~/.claude/` | yes (global CLAUDE.md ref) | **Say-trigger:** open Claude in any project dir; say `POLYBIUS` or `chief of staff` to activate |
| `project` | yes | `MAJOR_POLYBIUS.md` at `.claude/` | yes (project CLAUDE.md ref) | **Say-trigger:** open Claude in project dir; say `POLYBIUS` or `chief of staff` to activate |
| `project` | no | `MAJOR_POLYBIUS.md` at `.claude/` | no | **Paste:** open Claude in project dir; paste `Read .claude/MAJOR_POLYBIUS.md and assume the role for this project.` |
| `subproject` | n/a (never modifies parent CLAUDE.md) | `MAJOR_POLYBIUS_<slug>.md` at `<parent>/<slug>/.claude/` | no | **Paste:** open Claude in `<parent>/<slug>/`; paste `Read .claude/MAJOR_POLYBIUS_<slug>.md and assume the role for this sub-project.` |

Two patterns; rows 1-2 = say-trigger; rows 3-4 = paste-trigger. **Do NOT paste the literal word `POLYBIUS` as a multi-line activation — that conflates the say-trigger with the paste-trigger pattern, exactly the failure stoa--xh2 was filed against.**

Plus:
- A "When to use this" header (~3 lines)
- The CAPTAIN naming asymmetry note (CAPTAINs always suffixed when slug is present, regardless of MAJOR suffixing).
- A "Verifying" section (~5 lines): how to confirm an activation worked. The paste-receiving session's first response should (a) reference the right tier and (b) `bw prime` should hit the right store (project-tier session shows `stoa--` prefix or whatever the project prefix is, NOT `u--`). If session activates as the wrong tier, the symptom is `bw prime` either failing or hitting the user-beadwork store instead of the project's.

**Length: MUST be 50-90 lines.** Operational reference, no preamble bloat.

#### B.4 `substrate/operating-disciplines.md` — add §8 (positive-references-only universal)

**Location:** `substrate/operating-disciplines.md` — append after §7 (coordination protocol).

**Required content:**

Title: `## 8. Positive references only when authoring downstream briefs`

Body (~30-40 lines):
- The rule: when authoring any artifact a downstream agent will consume — activation paste-instructions, dispatch directives, brief comments, follow-up CAPTAIN prompts — reference only POSITIVE resources the agent should use. Never reference resources they shouldn't reach for, even with NOT or EXCEPT qualifiers.
- Why: the agent reads everything in the brief as real, in-scope context. A "NOT" qualifier mentions the resource as a real thing — defeating the bounded-context property of asymmetric scoping (operating-disciplines.md §7.3) or task-scoping. Under pressure (looking for context, ambiguous task, trying to be helpful), the agent can rationalize the now-known thing as a legitimate exception.
- Empirical anchor: 2026-05-04 the-stoa install paste; PRINCIPAL caught and corrected.
- Examples table — anti-pattern (negative framing) vs discipline (positive framing); 3-4 rows from stoa--m5m.
- Universality note: this applies to anyone authoring a downstream brief — POLYBIUS authoring activation pastes (MAJOR_POLYBIUS §5.1), PLINY authoring dispatch directives, CAPTAINs authoring follow-up briefs, pair-programmer Majors authoring their own follow-up dispatches. Single discipline; many surfaces.

#### B.5 `substrate/install.sh` — restructure next-steps activation output (fix mode-gating bug)

**Location:** `substrate/install.sh` lines ~870-913 (the existing next-steps block).

**Edit:** replace the current free-form "Next steps" output with a clearly demarcated, mode-aware ACTIVATION block per A7.

**Bug fix required (ARGUS cold-audit catch):** the current `if [ "$TARGET" = "subproject" ]` gating at line 888 lumps `--target project` (with or without `--modify-claude-md`) into the "say POLYBIUS" branch. This silently fails for `--target project` without `--modify-claude-md` because no CLAUDE.md ref exists, so saying POLYBIUS does nothing. Fix: gate on `($TARGET = subproject) OR ($TARGET = project AND MODIFY_CLAUDE_MD = 0)` for the paste-pattern branch.

**Behavior:**

1. Select the correct activation pattern (say-trigger vs paste-trigger) based on `$TARGET` and `$MODIFY_CLAUDE_MD`:
   - say-trigger: `--target user` OR (`--target project` AND `--modify-claude-md`)
   - paste-trigger: `--target project` (no `--modify-claude-md`) OR `--target subproject`

2. Print the appropriate ACTIVATION block per A7's two patterns (auto-load demarcation OR paste demarcation).

3. The paste forms must match the cheatsheet (B.3) verbatim. Don't rephrase, don't drift.

4. Below the ACTIVATION block, the existing "what got installed" / "what to do next" content remains, lightly trimmed. The paste-recovery line ("MAJOR_POLYBIUS keeps the latest activation paste at...") stays for the auto-load cases (recovery after /compact still applies).

**Idempotency:** running install.sh again should re-print the same ACTIVATION block; nothing accumulates.

**Smoke (Phase B beat 3) covers all four mode permutations.** See B.5's verification.

#### B.6 `substrate/templates/paste-instruction-template.md` — audit for negative framing

**Location:** `substrate/templates/paste-instruction-template.md`.

**Edit:** run `grep -nE '\b(NOT|don'"'"'t|skip|avoid|except|never)\b' substrate/templates/paste-instruction-template.md`. For each hit:

- If the line frames a resource the downstream agent shouldn't use → rewrite in positive form (the table in operating-disciplines.md §8 has anti-pattern → discipline pairs to model rewrites on).
- If the line is a legitimate negative (e.g., "this section never references", structural prose about the template itself) → leave as-is; record in the bw comment which lines were preserved and why.

**Acceptance:** post-edit, re-run the same grep on the file. Every remaining hit must be classified (rewritten or preserved-with-justification). Surface result via:

```
bw comment stoa--pbz "B.6 paste-instruction-template.md audit complete.
Pre-edit hits: <N>. Post-edit hits: <N> (all classified).
Rewrites: <list of line ranges>. Preserved: <list of line ranges + one-line justification each>."
```

If zero pre-edit hits exist, comment confirms zero hits. No silent skip.

#### B.7 `substrate/MAJOR_PLINY.md` — write-boundary check (mechanical)

**Location:** `substrate/MAJOR_PLINY.md`.

**Edit:** run `grep -nE '\b(bw write|bw comment|bw close|bw sync|cross-tier|tier-write|user-tier|project-tier|user-beadwork)\b' substrate/MAJOR_PLINY.md`. For each hit:

- If the line discusses cross-tier write boundaries OR makes a claim about which tier PLINY writes to → assess whether the claim is consistent with the new §7.1 write rules. If consistent, no edit. If inconsistent, surface the proposed edit before applying via `bw comment stoa--pbz "B.7 MAJOR_PLINY.md inconsistency at line <N>: <quote>. Proposed edit: <text>. Awaiting POLYBIUS sanity check."` and wait.
- If the line discusses bw operations within PLINY's own tier → no edit.

**Acceptance:** surface result via:

```
bw comment stoa--pbz "B.7 MAJOR_PLINY.md write-boundary audit complete.
Hits: <N>. Cross-tier-claim hits: <N>. Edits proposed: <N> (all surfaced for sanity check) | none (PLINY conventions are tier-local, consistent with new §7.1)."
```

The acceptance is "every hit classified," not "skim and declare." If the grep returns N hits, the comment lists N classifications.

---

## Phase B — Smoke test

After all deliverables are in place, run a smoke test before committing.

**Edit-order constraint** (ARGUS cold-audit catch — applies during build, not just smoke): build operating-disciplines.md edits FIRST (A.1, B.4 — adding §7 and §8). Then build MAJOR_POLYBIUS.md edits (A.2, A.3, B.1, B.2 — which cross-reference operating-disciplines.md sections). This avoids forward-reference bugs where MAJOR_POLYBIUS.md cites a section that doesn't yet exist when its edit lands. Templates (A.4, B.3) and install.sh (B.5) can build in any order, but commit only after the substrate-doc cross-refs are valid.

**Smoke beats:**

1. **Voice discipline grep — precise spec:**
   - Run `grep -nE '\b[Cc]olonel\b' <file>` on every edited substrate file. Required: zero hits, full stop. (Case-sensitive on the leading capital — "Colonel" the rank, not "colonel-something" hyphenated word, but the regex treats both.)
   - Run `grep -nE '\bthe user\b|\bthe user[''](s|d|ll|ve|re)\b|\bthe users\b' <file>` (case-insensitive) on every edited substrate file. Required: zero hits OUTSIDE explicitly comment-marked template-slot examples. The exemption applies only to lines with a leading `<!-- example:` or `# example:` marker; bare prose hits are violations.
   - **If a pre-existing hit surfaces in unedited surrounding sections of an edited file:** fix it. The discipline applies to whole-file hygiene, not just diff hygiene. Treat the cleanup as in-scope, not scope-expansion.
   - Files in scope: substrate/operating-disciplines.md, substrate/MAJOR_POLYBIUS.md, substrate/MAJOR_PLINY.md (only if B.7 edited it), substrate/templates/polling-cron-prompt-template.md, substrate/templates/activation-paste-cheatsheet.md, substrate/templates/paste-instruction-template.md (only if B.6 edited it), substrate/install.sh.

2. **Cross-references resolve — focused on in-arc cross-refs:**
   - Run `grep -nE '(operating-disciplines\.md §[0-9]+|MAJOR_POLYBIUS\.md §[0-9.]+|MAJOR_PLINY\.md §[0-9.]+)' <file>` on every edited substrate file.
   - For each hit, verify the referenced section number exists in the target file at the post-edit state.
   - **High-risk class: in-arc cross-refs.** New content in operating-disciplines.md §7/§8 is referenced from MAJOR_POLYBIUS.md §7.1/§5.1; new content in MAJOR_POLYBIUS.md §5.5 is referenced from B.3 cheatsheet. Verify these specifically; they are the most likely to drift if the edit-order constraint isn't followed.

3. **install.sh dry-run — all four mode permutations:**
   - `bash substrate/install.sh --dry-run --target user`
   - `bash substrate/install.sh --dry-run --target project --modify-claude-md`
   - `bash substrate/install.sh --dry-run --target project` (no --modify-claude-md)
   - `bash substrate/install.sh --dry-run --target subproject --parent-dir <test-dir> --subproject test-slug`
   - Verify each prints the ACTIVATION block with the right pattern (say-trigger for cases 1+2, paste-trigger for cases 3+4). Capture each output.
   - **Specifically verify the bug fix:** case 3 (project, no --modify-claude-md) MUST print the paste-trigger pattern, not the say-trigger pattern. This is the regression-prevention check for the ARGUS-surfaced bug.

4. **Cheatsheet round-trip:** the activation patterns printed by install.sh in beat 3 must exactly match the rows in `activation-paste-cheatsheet.md` (B.3) for the corresponding modes. No silent divergence — verify by inspection.

5. **operating-disciplines.md flows:** read end-to-end after edits. §1-§6 (existing) → §7 (new coordination) → §8 (new positive-references) → "Agent-regime inverses" (existing closer) → "Empirical lineage" (existing closer). Ordering and prose connectivity should make sense to a cold reader.

6. **MAJOR_POLYBIUS.md flows:** §5.1 → §5.2 → §5.3 → §5.4 → §5.5 (new) ordering reads cleanly; §7.1 (expanded with read-exception preserved) → §7.2 → §7.3 → §7.4 (with new cross-ref + template-named) → §7.5 reads cleanly. The §7.1 Exception clause must be visibly preserved with READ-only scoping.

7. **Polling-cron-prompt template usability:** the template's worked example (sketch using placeholder names per A.4 — NOT ariadne--m20 directly) must produce a coherent cron prompt when slots are filled. Inspect: does the resulting prompt have all five STEPs (substantive read, peer-silence escalation, self-radio-check refresh, cadence-tag detection, closure detection)?

8. **Negative-framing check on rewritten templates** (B.6 acceptance, restated as smoke):
   - On `substrate/templates/paste-instruction-template.md`, post-edit, run the B.6 grep again: every remaining hit must be classified (rewritten or preserved-with-justification per the bw comment from B.6).
   - Same grep on `substrate/templates/polling-cron-prompt-template.md` (new file — must not introduce negative framing): zero unclassified hits.

If smoke fails on any beat, surface to POLYBIUS via `bw comment stoa--pbz "smoke fail: <which beat> — <details>"` and wait for guidance.

---

## Phase C — Ship

Clean PASS → autonomous ship per `u--7yg.11`. Substrate is internal-deployable (not brand-defining surface, not public docs, not external API), so the §4.6 autonomous-ship discipline applies.

**Commit message shape:**

```
Arc 21: POLYBIUS-pair coordination protocol + downstream-handoff discipline

Lands five empirical disciplines surfaced during ariadne--m20 (workspace,
closed 2026-05-04 at a161630) into substrate so every future POLYBIUS
inherits them.

Part A — POLYBIUS-pair coordination protocol:
  - operating-disciplines.md §7: radio-check + adaptive cadence + cross-tier
    write boundaries (closes stoa--ivc, stoa--ay1, stoa--blg)
  - MAJOR_POLYBIUS.md §7.1 expanded: read AND write rules per tier
  - MAJOR_POLYBIUS.md §7.4: cross-ref to coordination protocol
  - templates/polling-cron-prompt-template.md (new)

Part B — Downstream-handoff discipline:
  - MAJOR_POLYBIUS.md §5.1: positive-references-only when filling slots
  - MAJOR_POLYBIUS.md §5.5 (new): activation-paste filenames vary by mode
  - operating-disciplines.md §8: positive-references universal
  - templates/activation-paste-cheatsheet.md (new)
  - install.sh next-steps: prominent ACTIVATION block per --target mode
  - templates/paste-instruction-template.md: audited for negative framing
    (closes stoa--xh2, stoa--m5m)

Closes stoa--pbz, stoa--ivc, stoa--ay1, stoa--blg, stoa--xh2, stoa--m5m.
```

Push to origin/main on clean PASS. The directive itself (`substrate/arcs/arc-21-build-directive.md`) was committed by POLYBIUS before dispatch — don't include it in your commit.

---

## Out of scope

- **ariadne workspace re-installs.** Workspace POLYBIUS owns the install re-run after this substrate update propagates. Not yours.
- **stoa--vz9 cleanup.** The remaining workspace-tier cleanup on stoa--vz9 (removing the "Anti-patterns absorbed from human SWE culture" section from ariadne CLAUDE.md) is workspace POLYBIUS's seat. Already underway in workspace bw — not yours.
- **Stoa app at `app/`.** No app changes.
- **Cloud cron template.** Per A5, cloud cron is documented as a limitation; no template ships.
- **Cron-prompt language for non-coordination engagements.** The polling template assumes peer-polling. Single-seat polling (e.g., POLYBIUS polling for new tickets without a coordination partner per §7.4 footnote) uses a different prompt — not in this arc.
- **Negotiated cadence-switching.** Per A4, cadence is per-seat unilateral; eventual-convergence with bounded staleness is acceptable. Don't add a synchronization protocol.
- **Case study (`docs/case-study/case-study.md`) updates.** The case study is reference material; substrate-internal arcs don't update it unless explicitly directed. (One-line appendix entry per Arc 20's pattern is OUT for Arc 21 — let the case study's update lag the substrate by one batch.)
- **stoa--o6k closure.** Session handoff ticket; closes when this arc dispatches (POLYBIUS's seat, not yours).
- **stoa--xh2 item 3 (install.sh seeds HUMAN_paste-orchestrator-instruction.md at install time).** stoa--xh2 lists this as OPTIONAL; it is deliberately deferred — the cheatsheet (B.3) + restructured install.sh ACTIVATION block (B.5) make activation paste content much more visible to PRINCIPAL at install time, which addresses the underlying problem. Seeding the file at install time is a v0.2 candidate, not Arc 21.
- **Per-engagement persistent cron-id record-keeping.** The polling-cron-prompt template (A.4) doesn't ship a state file for tracking engagement→cron-id mappings across compaction. POLYBIUS handles this via bw comments on the coordination ticket itself (radio-check posts include cron id); a separate state file is over-engineering for the observed pattern.

---

## Surface back when done

```
bw comment stoa--pbz "Arc 21 shipped at commit <sha>, pushed to origin/main.

Smoke test passed: <brief per-beat summary>.

Files added:
  - substrate/templates/polling-cron-prompt-template.md
  - substrate/templates/activation-paste-cheatsheet.md

Files modified:
  - substrate/operating-disciplines.md (added §7, §8)
  - substrate/MAJOR_POLYBIUS.md (§5.1 extended, §5.5 added, §7.1 expanded, §7.4 cross-ref)
  - substrate/MAJOR_PLINY.md (<edit summary or 'no edit needed per audit'>)
  - substrate/install.sh (next-steps activation block)
  - substrate/templates/paste-instruction-template.md (<edit summary or 'audited, no negative framing found'>)

Voice discipline: zero hits on \b[Cc]olonel\b / \bthe user\b outside template-slot examples.
Cross-refs: all resolve to real section numbers.
install.sh dry-run: ACTIVATION block prints correctly across all four mode permutations.

Closes stoa--ivc, stoa--ay1, stoa--blg, stoa--xh2, stoa--m5m, stoa--pbz."
```

Then close the children + parent in dependency order:

```
bw close stoa--ivc --reason "Landed via Arc 21 / stoa--pbz"
bw close stoa--ay1 --reason "Landed via Arc 21 / stoa--pbz"
bw close stoa--blg --reason "Landed via Arc 21 / stoa--pbz"
bw close stoa--xh2 --reason "Landed via Arc 21 / stoa--pbz"
bw close stoa--m5m --reason "Landed via Arc 21 / stoa--pbz"
bw close stoa--pbz --reason "Arc 21 shipped at <sha>"
bw sync
```
