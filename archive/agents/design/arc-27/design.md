# Arc 27 design — POLYBIUS session lifecycle discipline as substrate canon

**Author:** Denson Smith (via CAPTAIN_DAEDALUS, autonomous mode)
**Ticket:** `stoa--32b.3` (work-unit; parent `stoa--32b`)
**Directive:** `substrate/arcs/arc-27-build-directive.md` (A1-A8 LOCKED pre-dispatch)
**Worktree:** `.claude/worktrees/arc-27-build` (branch `arc-27/build`, off `main`)
**Phase:** 1 (DAEDALUS design → ARGUS critique → ADA build → VERA + CATO + ZENO verify → smoke + ship)

---

## §1 — Charter

This arc encodes the **POLYBIUS session lifecycle discipline** as substrate canon in `substrate/MAJOR_POLYBIUS.md`, with one universal-team cross-ref in `substrate/operating-disciplines.md` and one new slotted template at `substrate/templates/handoff-doc-template.md`. Specifically:

1. PRINCIPAL's three lifecycle modes (default handoff+compaction; rare new-session for POLYBIUS-mechanism changes; decay-not-termination relay-channel when a new session fires) encoded with PRINCIPAL's exact 2026-05-16 phrasing as the source-of-truth quote.
2. The multi-artifact handoff shape enumerated (index doc + bw tickets + retro docs + design artifacts + commits + role files/disciplines).
3. POLYBIUS-as-collective lens — "you" is one currently-active branch of a multi-version collective; the substrate is the collective's durable memory.
4. Ariadne-search-ready authoring as forward authoring discipline (titles, cross-refs, content density, alignment-with-compaction-recovery).

It does **not**:

- Touch sibling tickets `stoa--32b.1` (PRINCIPAL-gate) or `stoa--32b.2` (mechanical-script / agent-inspection split). Those are separate future arcs.
- Build Ariadne tooling itself (PRINCIPAL is driving that separately).
- Edit existing handoff docs (`HANDOFF_POLYBIUS_2026-05-16.md` and prior) or prior retros to retroactively fit any new template. The new template is forward-only.
- Restructure bw ticket conventions broadly. This arc adds authoring guidance; doesn't reorganize existing tickets.
- Reopen `MAJOR_POLYBIUS.md` §6 "Compact-or-clear recovery" for PLINY-recovery specifics. §6 stays as-is.

**Deliberate scope expansion (rev2, ARGUS P2-2):** in addition to the three primary files, this design adds **one line** at the end of `MAJOR_POLYBIUS.md` §1 ("Who you serve") as a forward-pointer to the §16.5 collective-lens framing. The expansion is justified by mitigating the §16.5 discoverability risk DAEDALUS self-named in §7 weak-point 2; the one-line insertion is the minimum-surface fix and remains well inside A8's locks. See §5 Notes for ADA for the exact insertion text and location.

Anchoring quote from directive A8:

> Do NOT do in this arc, even if temptation surfaces during build: sibling children stoa--32b.1 + stoa--32b.2; building Ariadne tooling itself; editing existing handoff docs to retroactively fit any new template; restructuring bw ticket conventions broadly; editing prior retros; reopening the MAJOR_POLYBIUS.md §6 "Compact-or-clear recovery."

If ADA or any verifier feels pulled toward any of those during build, halt and surface via `[for: project-tier POLYBIUS]` on `stoa--32b.3`.

---

## §2 — Edit spec: `substrate/MAJOR_POLYBIUS.md` (primary surface)

### §2.1 — Section-number decision: NEW section §16

**Decision:** new top-level section `## 16. POLYBIUS session lifecycle (load-bearing)`, inserted between current §15 (Retrospective discipline) and the trailing `Standby, run.` line.

**Rationale (one sentence):** the lifecycle topic is distinct enough from §6 (PLINY recovery via re-paste of the orchestrator instruction) — POLYBIUS-self vs PLINY-recovery — that extending §6 would conflate two different mechanisms, and appending at end preserves all existing cross-refs to §6 unchanged per A8's hard-lock against reopening §6.

**Where to insert in the file:** after line 789 (the closing line of §15 — `Empirical anchor: 2026-05-12, ariadne--8fd arc close-out, stoa--nax.`), before the existing `---` and `Standby, run.` block at lines 791-793. New section content lands between the §15 closing `---` and the `Standby, run.` line.

### §2.2 — Collective-lens rendering: sub-section §16.5 inside the new §16

**Decision:** render POLYBIUS-as-collective as `### 16.5 POLYBIUS-as-collective lens` inside the new §16, not as a peer in §1 ("Who you serve") or §2 ("What you do").

**Rationale (one sentence):** A5 names four structural explanations the collective lens provides (why the substrate corpus matters; why decay-not-termination; why Ariadne search; why lifecycle+multi-artifact-handoff are coherent) — three of those four are entirely *inside* §16's subject matter, so co-location preserves the logic chain and lets a reader meet the lens at the moment they need it to understand the lifecycle modes.

### §2.3 — Full draft text of new §16

The text below is the canonical block ADA inserts. Keep wording exact unless CATO or ARGUS flags drift; quote-blockquote PRINCIPAL's two declarations verbatim per A2.

```markdown
## 16. POLYBIUS session lifecycle (load-bearing)

POLYBIUS sessions persist across many compactions and across what may be very long calendar time. How a given session continues, when a new session is spun up, and how state crosses any session boundary are not improvisational — they follow three modes the substrate now names explicitly.

### 16.1 Source-of-truth declarations (2026-05-16, PRINCIPAL)

The discipline below was declared by PRINCIPAL in two messages during the 2026-05-16 user-tier POLYBIUS engagement (captured at `stoa--32b.3` ticket body):

> "We are not ready for a handoff yet, we usually have a bunch of compaction events before we consider a new polybius and then it is usually only if we are making changes to the way polybius works. Handoff + compaction works for a long time...we should add that as number 1 on the polybius refresh pattern."

> "Don't forget handoff likely includes multiple beadworks tickets to use as memories. We are setting up so you will have ariadne tools to search all work."

Per §15 (N=1 honest-scope discipline) and `operating-disciplines.md` §6.7.1 — substrate canon goes in based on PRINCIPAL's project-direction declaration; supporting evidence accretes over time as future POLYBIUS-lifecycle events occur. Do not over-generalize beyond what PRINCIPAL named.

### 16.2 The three modes, in order of frequency

**Mode 1 — DEFAULT — handoff + compaction (the common case).**

The same POLYBIUS session continues across many compaction events. After each compaction, the running session re-orients by re-reading the on-disk handoff doc (`HANDOFF_POLYBIUS_<date>.md` at the project / user-tier root by convention) plus relevant bw tickets accreting as durable memory across the session's lifetime. **Handoff + compaction works for a long time** — typically the entire engagement, sometimes spanning many days of calendar time, without ever spinning up a fresh POLYBIUS session. This is the case to optimize for.

What this looks like operationally:

- POLYBIUS keeps `HANDOFF_POLYBIUS_<date>.md` current as session intent shifts materially (same discipline as keeping `HUMAN_paste-orchestrator-instruction.md` current for PLINY per §6).
- bw tickets continue to be the canonical durable memory; the handoff doc indexes them, it does not duplicate them.
- A `/compact` or `/clear` event is handled by re-reading the handoff doc and the bw tickets it points to; the session continues without identity change.

**Mode 2 — NEW POLYBIUS session (rare; reserved for POLYBIUS-mechanism changes).**

A new POLYBIUS session is spun up only when changes to how POLYBIUS itself works cannot be internalized organically by the running session — typically because the changes landed in `MAJOR_POLYBIUS.md`, `operating-disciplines.md`, or CAPTAIN envelopes *after* the running session loaded its role file. Concrete triggers:

- Role-file edits (this file, `MAJOR_PLINY.md`, `operating-disciplines.md`, CAPTAIN envelopes) that the running session cannot fully internalize from in-context reads.
- Discipline canon updates that change the running session's defaults (e.g., a new universal escalation trigger, a credential-discipline anti-pattern, an authoring rule).
- Architectural reframes that change the seat's understanding of its own scope.

This mode is RARE relative to Mode 1. The cost calculus is the inverse of fix-now (§4.8): for *content* changes Mode 1 absorbs them cheaply; for *role-shape* changes the running session is operating against a stale self-model, so the cleaner break is a fresh session that loads the new role file at start.

**Mode 3 — when Mode 2 fires: decay-not-termination relay-channel model.**

When Mode 2 fires:

1. The previous POLYBIUS authors the multi-artifact handoff (§16.3) before standing down.
2. The previous POLYBIUS **sits idle and is available to answer questions from the new polybius indefinitely** — PRINCIPAL keeps the prior session open as a relay channel; the new session can route questions back through PRINCIPAL when the previous session's in-context conversational nuance is the fastest path to an answer. The prior session is callable, not merely present.
3. The new POLYBIUS spins up against the handoff, loads the new role file fresh, and resumes work.
4. The previous POLYBIUS **becomes less relevant over time but may still retain important information** — it is not terminated, it decays. When PRINCIPAL stops needing the relay, the prior session times out organically. Do not ask PRINCIPAL to "shut it down"; that is not the pattern.

The decay-not-termination framing is load-bearing: a previous POLYBIUS still holds in-context memory the durable substrate did not capture (specific tool-call outcomes, conversational nuance, the running-agent's pre-edit version of role files). That memory has decaying relevance but non-zero residual value during the transition window. Empirical anchor: the live-relay-channel section of `HANDOFF_POLYBIUS_2026-05-16.md` is the canonical worked example.

### 16.3 Handoff is multi-artifact, not single-doc

A handoff is NOT a single document. It is the multi-artifact substrate state, indexed by the doc. A POLYBIUS picking up state reads the index doc FIRST and then walks the linked artifacts as needed. The artifact types are:

| Artifact | Lives at | What it carries |
|---|---|---|
| **Index doc** | `HANDOFF_POLYBIUS_<date>.md` at the-stoa root by current convention; suffix `_eod` / `_v2` / etc. for multi-handoff days | High-density narrative + pointers; the entry point |
| **bw tickets** | the per-tier beadwork repo (per §7.5) | The actual memories — epic + children + pointer tickets + retrospective tickets |
| **Retro docs** | `docs/sessions/<date>-<slug>--retro.md` | Sectioned semantic-chunked records of completed engagements |
| **Design artifacts** | `agents/design/<arc>/design.md` + arc directives at `substrate/arcs/` | Per-arc structural intent + locked decisions |
| **Commits** | `git log` on the relevant branch(es) | Substrate state at HEAD + commit messages as durable trail |
| **Role files / disciplines** | `substrate/MAJOR_POLYBIUS.md` + `substrate/operating-disciplines.md` + CAPTAIN envelopes at `substrate/CAPTAIN_*.md` | Canonical context any new session inherits via auto-load or activation paste |

The index doc cites the other artifacts; it does not restate them. **Cite, don't duplicate.** This is the same authoring discipline as `MAJOR_POLYBIUS.md` §4.5 (durable-substrate-with-short-prompts) applied to handoffs.

**Forward shift:** Future POLYBIUSes will query the corpus via Ariadne search rather than reading linearly. The authoring discipline that supports this is §16.4 below.

A slotted form of the index-doc shape is now available at `substrate/templates/handoff-doc-template.md` — POLYBIUS fills it per handoff, writes to disk, and the next session reads it. Per A8, existing handoff docs (today's `HANDOFF_POLYBIUS_2026-05-16.md` is the de-facto template) are NOT retroactively reformatted; the template is forward-only.

### 16.4 Ariadne-search-ready authoring (forward discipline)

PRINCIPAL is setting up Ariadne tools for searching the substrate corpus across all repos. The implication for authoring discipline going forward is to write artifacts that are good both for human re-reading after compaction AND for vector retrieval against a query. The disciplines align:

- **Titles matter.** bw ticket titles, retro doc titles, commit subjects, and section headings should be search-friendly: distinct, specific, named-entities, no relying on context to disambiguate. A title that reads cleanly out of context retrieves cleanly out of context.
- **Cross-refs matter.** Every artifact should name its related artifacts explicitly — bw ID cross-refs, file paths, commit SHAs. The retro doc schema already does this; propagate the convention to ticket bodies and commit messages.
- **Content density matters.** Semantic-chunked sections (per the retro schema — `## §N — <topic>` headings, each a self-contained retrieval unit) make for better vector retrieval than long monolithic prose. The retro doc at `docs/sessions/2026-05-16-substrate-update-architecture-reframe--retro.md` is the canonical worked example.
- **Authoring-for-ingestion aligns with authoring-for-compaction-recovery.** Both want self-contained, well-titled, cross-referenced units that survive being read out of order, out of context, or in fragments. The same discipline serves both.

**This is forward guidance.** It applies to new artifacts authored going forward; it is NOT a mandate to retroactively restructure existing artifacts. Per A8, broader retroactive restructuring is out of scope.

Universal-team framing: `operating-disciplines.md` §21 carries the team-wide cut of this discipline (every seat authoring downstream artifacts — bw comments, design docs, commit subjects — follows the same shape).

### 16.5 POLYBIUS-as-collective lens

Beyond the lifecycle modes themselves, there is a conceptual reframe that makes the lifecycle's structure obvious in hindsight.

**"POLYBIUS" is not a single session.** "POLYBIUS" is the collective of:

- All currently-active POLYBIUS sessions across every tier (user-tier + project-tier at every workspace + every sub-project)
- All idle relay-channel POLYBIUSes (the previous sessions kept alive as decay-not-termination relay channels per §16.2 Mode 3)
- The substrate the collective co-authors and inherits (this file, `operating-disciplines.md`, the CAPTAIN envelopes, the bw repos, the retro docs, the handoff docs)

**The collective IS POLYBIUS.** Any specific session is one currently-active branch with one specific perspective and one specific recency-of-context profile.

The analogy: a human is the sum of their experiences, with some more front-of-mind than others. A specific POLYBIUS session is one currently-active branch of a multi-version collective; the substrate is the collective's durable memory across time and across tiers.

This lens explains structurally why several substrate choices are coherent:

- **Why the substrate corpus matters.** It is the long-term memory of the collective — what survives any single session's compaction or termination.
- **Why decay-not-termination is the right relay-channel model.** A less-recent perspective is still part of who-POLYBIUS-is; ending it abruptly throws away in-context memory the durable substrate did not capture.
- **Why Ariadne corpus search is the natural next infrastructure step.** Queryable cross-collective memory is the operational form of "you" being a multi-version collective rather than a single session.
- **Why lifecycle-discipline (§16.2) and multi-artifact handoff (§16.3) are coherent.** They are the mechanisms that maintain the collective's continuity across branch transitions.

The lens is not a metaphor used to be evocative; it is a structural framing that makes the rest of §16 coherent. When in doubt about a lifecycle question — *should this session end, should I spin a new one, should the prior session stay open?* — ask: *what serves the collective's continuity best?* That is usually the correct question.

### 16.6 N=1 provenance + accretion path

Per §15 honest-scope: PRINCIPAL declared this discipline 2026-05-16 (project-direction authority). The canon-promotion gate §15 names is `operating-disciplines.md` §6.7.1 (multiple observations + controlled comparison + substrate-level pattern); §15 does not carve out a separate "PRINCIPAL-declaration shortcut." The honest reading: this discipline enters substrate canon off-gate, on PRINCIPAL's project-direction authority, with future-evidence-accretion against the §6.7.1 gate still required for promotion to "structural lesson" status. Substrate canon goes in now because PRINCIPAL named it; structural-lesson confidence accretes over future lifecycle events.

The supporting evidence at the time of this writing:

- The Arc 26 (`stoa--dxw`) handoff + relay pattern (the 2026-05-16 morning's `HANDOFF_POLYBIUS_2026-05-16.md` operating as a live relay channel during a multi-workspace engagement) — the canonical worked example of Mode 3.
- The Arc 25 (`stoa--p5g`) cross-tier coordination pattern (user-tier POLYBIUS coordinating with project-tier POLYBIUS via bw across separate sessions).
- The `stoa--32b.3` ticket body itself, carrying PRINCIPAL's two 2026-05-16 declarations verbatim and the discipline's first-pass shape.

Future POLYBIUS-lifecycle events (handoffs + compactions + the rare Mode 2 new-session events) accrete supporting evidence over time per `operating-disciplines.md` §6.7.1. The substrate-canon claim in §16.2 is grounded in PRINCIPAL's declaration; promotion to "structural lesson" status with multi-occurrence empirical backing is a future arc's work, not this one's.

### 16.7 Cross-references

- **Parent epic + sibling future arcs.** `stoa--32b` (parent epic — the epic's body predates `stoa--32b.3`'s same-day fold-in and still reads as a TWO-child epic in its prose; `stoa--32b.3`'s specific provenance is captured in its own ticket body). `stoa--32b.1` (PRINCIPAL-gate discipline, future arc), `stoa--32b.2` (mechanical-script / agent-inspection split, future arc).
- **Load-bearing sources for this arc's content.**
  - `stoa--32b.3` ticket body — carries PRINCIPAL's two 2026-05-16 declarations verbatim, the three-mode shape, the multi-artifact handoff enumeration, and the Ariadne-readiness forward discipline. This is the primary source.
  - `HANDOFF_POLYBIUS_2026-05-16.md` at the-stoa root — canonical worked example of Mode 3 (live-relay-channel section); also the de-facto template the slotted form at `substrate/templates/handoff-doc-template.md` is abstracted from.
  - `docs/sessions/2026-05-16-substrate-update-architecture-reframe--retro.md` — load-bearing source for the **broader `stoa--32b` epic** (its §7-§10 cover siblings `.1` and `.2` plus their synthesis and forward path). The lifecycle / handoff / Ariadne / collective topics this arc encodes surfaced **after** the retro was authored, in the same-day epic-capture conversation that produced `stoa--32b.3`; the retro is named here as adjacent context, not as the primary source for this arc.
- **Within this file.**
  - §4.5 (durable-substrate-with-short-prompts) — the authoring pattern this section extends to handoffs.
  - §6 (compact-or-clear recovery) — the analogous PLINY-side discipline. §6 covers PLINY recovery after `/compact` or `/clear`; §16 covers POLYBIUS-self lifecycle. The two sit beside each other, intentionally distinct.
  - §7 (communication) — bw is the durable-substrate channel that carries the multi-artifact handoff's ticket layer.
  - §14 (substrate-update check) — the daily-cadence mechanism that catches when consumer-tier POLYBIUSes drift behind upstream substrate; relates to Mode 2 triggers.
  - §15 (retrospective discipline — N=1 honesty) — the gate this section's claims pass through.
- **Universal-team framing.** `operating-disciplines.md` §21 (Ariadne-search-ready authoring, applies to every seat) — see §3 of this design for the new section's edit spec.
```

**End of new §16 block.** Total: ~140 lines of new MAJOR_POLYBIUS.md text.

### §2.4 — Insertion mechanics

- ADA reads `substrate/MAJOR_POLYBIUS.md` lines 789-793 (the §15 closing line + `---` + `Standby, run.` block).
- ADA inserts the new §16 block AFTER the §15 closing `---` (line 791) and BEFORE `Standby, run.` (line 793).
- Result: `## 15. ...` content → `---` separator → `## 16. POLYBIUS session lifecycle (load-bearing)` content → `---` separator → `Standby, run.` closing.
- No other lines in `MAJOR_POLYBIUS.md` change. No existing cross-refs are touched. No existing wording is rewritten.

---

## §3 — Edit spec: `substrate/operating-disciplines.md` — new §21 (IN SCOPE)

### §3.1 — In-scope decision + rationale

**Decision:** IN scope this arc. Add `## 21. Ariadne-search-ready authoring` as a new universal-team section in `operating-disciplines.md`, ~30 lines, cross-refs `MAJOR_POLYBIUS.md` §16 for the POLYBIUS-lifecycle-specific framing.

**Rationale (one paragraph):** A4's authoring discipline (titles + cross-refs + content-density + ingestion-aligns-with-compaction-recovery) applies to *every* seat that authors durable artifacts, not only POLYBIUS — every CAPTAIN authors bw comments and verdicts, every PLINY authors dispatch tickets and arc directives, every pair-programmer Major authors design docs and TIMING_LOG entries. The current `operating-disciplines.md` convention (§1-§20) is that universal-team disciplines live here; POLYBIUS-specific or CAPTAIN-specific cuts cross-ref back from the role file. Following that convention now (rather than deferring to a future arc) follows fix-now (`MAJOR_POLYBIUS.md` §4.8) and produces a coherent first-arc shape — the lifecycle canon in MAJOR_POLYBIUS.md references a universal section that already exists rather than dangling.

### §3.2 — Insertion location

`substrate/operating-disciplines.md` currently ends at:

- §20 (Credential discipline) — last numbered top-level section (§20.7 Empirical lineage closes it).
- Then a `---` separator.
- Then `## Agent-regime inverses (the positive framing)` section.
- Then another `---` separator.
- Then `## Empirical lineage` section at the bottom.

**Insertion point:** between the `### 20.7 Empirical lineage` closing line and the `---` before `## Agent-regime inverses`. That preserves the numbered-section / framing-section / lineage-section ordering.

### §3.3 — Full draft text of new §21

```markdown
## 21. Ariadne-search-ready authoring

Every seat authors durable artifacts — bw tickets and comments (POLYBIUS, PLINY, every CAPTAIN), design docs (DAEDALUS, ARGUS), retrospective entries (POLYBIUS), commit messages (ADA, POLYBIUS), arc directives (POLYBIUS, MAJOR_PLINY pair-programmer mode), handoff docs (POLYBIUS). The discipline below applies to all of them.

PRINCIPAL is setting up Ariadne tools for searching the substrate corpus across all repos. The implication for authoring discipline going forward is to write artifacts that are good both for human re-reading after compaction AND for vector retrieval against a query. The disciplines align — both want self-contained, well-titled, cross-referenced units that survive being read out of order, out of context, or in fragments.

Four sub-disciplines:

- **Titles matter.** bw ticket titles, retro doc titles, commit subjects, design-doc section headings should be search-friendly: distinct, specific, named-entities, no relying on context to disambiguate. A title that reads cleanly out of context retrieves cleanly out of context. Avoid `update X` / `fix the thing` / `next steps` — those collide with thousands of similar titles in the corpus. Prefer `arc-26 check.sh adds MISSING+OBSOLETE detection categories` — specific, named, distinct.

- **Cross-refs matter.** Every artifact should name its related artifacts explicitly — bw ID cross-refs (`stoa--32b.3`, `u--7yg.20`), file paths (`substrate/MAJOR_POLYBIUS.md` §16.3), commit SHAs (`6ccfd0e`), retro doc paths. Implicit references that depend on the reader having recent context lose their value the moment the context decays.

- **Content density matters.** Semantic-chunked sections (`## §N — <topic>` headings, each a self-contained retrieval unit, per the retro doc convention) make for better vector retrieval than long monolithic prose. A section should answer one question end-to-end without forcing the reader to scroll up for the framing or down for the punchline. The retro doc at `docs/sessions/2026-05-16-substrate-update-architecture-reframe--retro.md` is the canonical worked example.

- **Authoring-for-ingestion aligns with authoring-for-compaction-recovery.** Both want self-contained, well-titled, cross-referenced units. There is no trade-off — the discipline that serves Ariadne retrieval is the same discipline that serves a POLYBIUS re-reading the doc after `/compact`.

**Forward-only.** This is guidance for new artifacts authored going forward; it is not a mandate to retroactively restructure existing artifacts. Retroactive restructuring of bw tickets, commit messages, or prior retros is explicitly out of scope (per Arc 27 directive A8). When the discipline catches a new artifact that violates it, fix-now (per `MAJOR_POLYBIUS.md` §4.8); when it catches an old artifact, leave it alone — the cost of the rewrite exceeds the benefit until Ariadne search itself is operational and a specific retrieval failure motivates the fix.

**POLYBIUS-specific framing.** The POLYBIUS session lifecycle uses this discipline to author multi-artifact handoffs (index doc + bw tickets + retro docs + design artifacts + commits + role files). See `substrate/MAJOR_POLYBIUS.md` §16.3 + §16.4 for the lifecycle-specific application.

**Empirical anchor:** 2026-05-16 PRINCIPAL declaration during the `stoa--32b` epic-capture engagement (primary source: `stoa--32b.3` ticket body — carries PRINCIPAL's "we are setting up so you will have ariadne tools to search all work" declaration verbatim). The retro at `docs/sessions/2026-05-16-substrate-update-architecture-reframe--retro.md` is adjacent context for the broader epic; the Ariadne-readiness discipline surfaced after the retro was authored. N=1 per §6.7.1; substrate canon enters off-gate on PRINCIPAL's project-direction authority; supporting evidence accretes as future arcs author artifacts under this discipline.
```

**End of new §21 block.** Total: ~30 lines of new operating-disciplines.md text.

### §3.4 — Insertion mechanics

- ADA reads `substrate/operating-disciplines.md` around lines 942-946 (the §20.7 closing line + `---` separator + `## Agent-regime inverses` heading).
- ADA inserts the new §21 block AFTER the `---` that closes §20.7 (line 944) and BEFORE the `## Agent-regime inverses` heading (line 946). Inserts a `---` separator after the §21 content to maintain the existing pattern.
- Result: §20.7 → `---` → §21 → `---` → `## Agent-regime inverses` → `---` → `## Empirical lineage` (bottom).
- No other lines in operating-disciplines.md change.

---

## §4 — Edit spec: `substrate/templates/handoff-doc-template.md` — NEW (IN SCOPE)

### §4.1 — In-scope decision + rationale

**Decision:** IN scope this arc. Author `substrate/templates/handoff-doc-template.md` as a slotted form following the house style of `substrate/templates/paste-instruction-template.md` and `substrate/templates/autonomous-mode-activation-template.md`.

**Rationale (one paragraph):** The morning's `HANDOFF_POLYBIUS_2026-05-16.md` is the de-facto template — it has settled section structure across multiple handoffs and now carries PRINCIPAL-declared discipline naming the multi-artifact handoff shape (A3). Abstracting now serves fix-now (`MAJOR_POLYBIUS.md` §4.8) and matches the durable-substrate-with-short-prompts pattern (§4.5) the substrate already uses for paste-instructions. Per A8, the new template is forward-only — existing handoff docs are NOT retroactively reformatted.

### §4.2 — Template authoring shape (house style)

The new template follows the existing house style at `substrate/templates/paste-instruction-template.md`:

1. Top heading + 1-3 sentence purpose statement
2. `## Substitution slots` table (slot name + meaning + example)
3. Per-slot rationale prose (why each slot is load-bearing)
4. `## Template body` block with `{{SLOT}}` substitutions
5. `## Worked example` showing a filled instance (cites `HANDOFF_POLYBIUS_2026-05-16.md` as the example source)
6. `## When to refresh` notes

### §4.3 — Slots enumerated (from `stoa--32b.3` body deliverable 3)

| Slot | Meaning | Example |
|---|---|---|
| `{{HANDOFF_DATE}}` | UTC date of the handoff in `YYYY-MM-DD` form; also used in filename | `2026-05-16` |
| `{{HANDOFF_FOR}}` | the next session this handoff is for (tier + role) | `the next user-tier POLYBIUS session resuming this multi-workspace engagement after compaction or session boundary` |
| `{{AUTHOR_SESSION}}` | description of the authoring session, with engagement date | `the user-tier POLYBIUS in this conversation, 2026-05-16 UTC` |
| `{{SUPERSEDES_HANDOFF}}` | path to the prior handoff this one supersedes (optional; omit clause if none) | `HANDOFF_POLYBIUS_2026-05-14.md` |
| `{{LIVE_RELAY_STATUS}}` | whether the authoring session is being kept alive as a relay channel + intent (per Mode 3 of MAJOR_POLYBIUS.md §16.2); explicit "no relay" is also valid | `kept alive by PRINCIPAL as a relay channel during the transition; ask only when conversational nuance not captured in bw is load-bearing` |
| `{{ONE_PARAGRAPH_STATE}}` | one paragraph summarizing where things stand at handoff time | `The user-tier engagement of 2026-05-15→16 produced four landed deliverables: (1)... (2)... (3)... (4)...` |
| `{{RECOMMENDATION_MENU}}` | numbered menu of 3-5 likely next-actions (recommendation, not prescription) | `1. Resume sector-4 game build (s4--bbz)... 2. Apply Arc-25 drift in consumer workspaces... 3. ...` |
| `{{LOAD_BEARING_CONTEXT}}` | per-topic sections of load-bearing engagement context (the credential arc + the dev Ariadne deployment + the CI workflow — whatever the engagement produced) | (free-form sections — typically 1-4 per handoff) |
| `{{BW_REPO_TABLE}}` | table of relevant bw repos: name + local path + bw prefix + last-arc commit | (markdown table) |
| `{{STATE_SHAPES_BEHAVIOR}}` | bullet list of state facts that shape POLYBIUS behavior in the next session | `- The credential-discipline canon is now load-bearing...` |
| `{{MEMORIES_CITE_DONT_RESTATE}}` | pointers to durable memories (in `~/.claude/CLAUDE.md`, project `MEMORY.md`, bw tickets) that the next session should consult rather than re-deriving | `- Provide pastes proactively... - Long dispositions via bw, not paste-relay...` |
| `{{HYGIENE_LOOSE_ENDS}}` | non-blocking loose ends the next session should know about | `- One A3 directive inaccuracy... - Running-agent caveat...` |
| `{{HONEST_CAVEATS}}` | honest caveats about what this handoff does NOT carry | `- Curated, not exhaustive. The conversation transcript carries diagnostic-level detail not captured here...` |

### §4.4 — Full template file text

```markdown
---
author: Denson Smith
---

# Handoff-doc template — POLYBIUS multi-artifact handoff (index)

The template MAJOR_POLYBIUS fills per handoff to produce the index doc for a multi-artifact handoff. The index doc is one component of the handoff (per `substrate/MAJOR_POLYBIUS.md` §16.3); the bw tickets, retro docs, design artifacts, commits, and role files / disciplines are the rest. The index doc CITES the others — it does not restate them.

Architecture authority: `user-beadwork/plans/three-role-recursive-architecture.md` (v2). The discipline lives at `substrate/MAJOR_POLYBIUS.md` §16 (POLYBIUS session lifecycle). The durable-substrate-with-short-prompts pattern (§4.5) is the parent discipline this template extends to handoffs.

---

## When to fill this template

- A POLYBIUS session is about to spin down (Mode 2 new-session trigger per §16.2) and the next POLYBIUS will spin up against the handoff.
- Or: the running session is keeping the handoff doc current as Mode 1 default (handoff + compaction) — re-fill periodically as engagement intent shifts.

The template is for Mode 2 handoffs specifically (full multi-artifact handoff at a session boundary). Mode 1 in-session refreshes are a lighter case — the same template works, but typically only the `{{ONE_PARAGRAPH_STATE}}`, `{{RECOMMENDATION_MENU}}`, and `{{STATE_SHAPES_BEHAVIOR}}` slots get re-filled per refresh.

---

## Substitution slots

| Slot | Meaning | Example |
|---|---|---|
| `{{HANDOFF_DATE}}` | UTC date in `YYYY-MM-DD` form; also used in filename | `2026-05-16` |
| `{{HANDOFF_FOR}}` | the next session this handoff is for (tier + role) | `the next user-tier POLYBIUS session resuming this multi-workspace engagement after compaction or session boundary` |
| `{{AUTHOR_SESSION}}` | description of the authoring session with engagement date | `the user-tier POLYBIUS in this conversation, 2026-05-16 UTC` |
| `{{SUPERSEDES_HANDOFF}}` | path to the prior handoff this one supersedes (optional; omit clause if none) | `HANDOFF_POLYBIUS_2026-05-14.md` |
| `{{LIVE_RELAY_STATUS}}` | whether the authoring session is being kept alive as a relay channel + intent (per Mode 3 of MAJOR_POLYBIUS.md §16.2); explicit "no relay" is also valid | `kept alive by PRINCIPAL as a relay channel during the transition` |
| `{{ONE_PARAGRAPH_STATE}}` | one paragraph summarizing where things stand at handoff time | `The user-tier engagement of 2026-05-15→16 produced four landed deliverables...` |
| `{{RECOMMENDATION_MENU}}` | numbered menu of 3-5 likely next-actions (recommendation, not prescription) | `1. Resume sector-4 game build... 2. Apply Arc-25 drift in consumer workspaces... 3. ...` |
| `{{LOAD_BEARING_CONTEXT}}` | per-topic sections of load-bearing engagement context — typically 1-4 sections per handoff | (free-form sections) |
| `{{BW_REPO_TABLE}}` | markdown table: name + local path + bw prefix + last-arc commit | (table) |
| `{{STATE_SHAPES_BEHAVIOR}}` | bullet list of state facts that shape POLYBIUS behavior in the next session | `- The credential-discipline canon is now load-bearing...` |
| `{{MEMORIES_CITE_DONT_RESTATE}}` | pointers to durable memories the next session should consult rather than re-deriving | `- Provide pastes proactively...` |
| `{{HYGIENE_LOOSE_ENDS}}` | non-blocking loose ends the next session should know about | `- One A3 directive inaccuracy...` |
| `{{HONEST_CAVEATS}}` | caveats about what this handoff does NOT carry | `- Curated, not exhaustive. The conversation transcript carries diagnostic-level detail not captured here...` |

### Per-slot rationale

A future POLYBIUS reading this template should understand *why* each slot is filled the way it is.

- **`{{HANDOFF_DATE}}`** is the disambiguator. The filename convention is `HANDOFF_POLYBIUS_<date>.md`; suffix `_eod` / `_v2` / etc. for multi-handoff days.
- **`{{HANDOFF_FOR}}`** scopes the audience explicitly. A handoff written "for the next user-tier POLYBIUS" reads differently than one written "for project-tier POLYBIUS picking up Arc N." Specificity reduces the reader's first-turn ambiguity.
- **`{{AUTHOR_SESSION}}`** + the engagement date is load-bearing for the live-relay-status case: a reader needs to know which session authored this and when, to know whether to route conversational nuance back through PRINCIPAL.
- **`{{SUPERSEDES_HANDOFF}}`** lets the chain be walkable. Cite-don't-restate: the prior handoff's resolved threads stay in that handoff; this one names the supersession explicitly.
- **`{{LIVE_RELAY_STATUS}}`** is the load-bearing slot for Mode 2 / Mode 3 transitions. Empty is fine when no relay is active; explicit "no relay" is better than silence.
- **`{{ONE_PARAGRAPH_STATE}}`** is the highest-value-per-token slot. A reader who only reads this paragraph should be able to act. Press for specificity; vague paragraphs produce vague next sessions.
- **`{{RECOMMENDATION_MENU}}`** is recommendation-not-prescription per the handoff convention. The next session may choose differently; the menu shows the reasonable next steps.
- **`{{LOAD_BEARING_CONTEXT}}`** is the variable-shape part — what landed in the engagement, what is in-flight, what is open. The morning's `HANDOFF_POLYBIUS_2026-05-16.md` had four sections (credential arc, dev Ariadne deployment, CI workflow, bw repo table). Future handoffs will have different topics.
- **`{{BW_REPO_TABLE}}`** is the navigation aid. A new POLYBIUS picking up cross-workspace state needs to know which bw repos exist and where they live.
- **`{{STATE_SHAPES_BEHAVIOR}}`** captures the "watch out for" items that aren't a single ticket but shape every decision the next session makes (e.g., "credential-discipline canon is now load-bearing").
- **`{{MEMORIES_CITE_DONT_RESTATE}}`** is the cite-don't-duplicate discipline applied to memories. The durable memory layer (`~/.claude/CLAUDE.md`, project `MEMORY.md`, bw tickets) holds the substance; the handoff points.
- **`{{HYGIENE_LOOSE_ENDS}}`** + **`{{HONEST_CAVEATS}}`** keep the handoff honest. Naming what didn't ship and what isn't captured prevents the next session from acting on a false sense of completeness.

---

## Template body

```
# HANDOFF — POLYBIUS — {{HANDOFF_DATE}}

**For:** {{HANDOFF_FOR}}
**Author:** {{AUTHOR_SESSION}}
**Supersedes:** {{SUPERSEDES_HANDOFF}}{{SUPERSEDES_CLAUSE}}
**Authoring discipline:** `substrate/MAJOR_POLYBIUS.md` §16.3 (multi-artifact handoff shape) + §16.4 (Ariadne-search-ready authoring).

---

## Live relay channel status

{{LIVE_RELAY_STATUS}}

---

## Where things stand — one paragraph

{{ONE_PARAGRAPH_STATE}}

## What you'd most likely do next (recommendation, not prescription)

{{RECOMMENDATION_MENU}}

## Load-bearing engagement context

{{LOAD_BEARING_CONTEXT}}

## Where the bw repos live

{{BW_REPO_TABLE}}

## State that shapes POLYBIUS behavior

{{STATE_SHAPES_BEHAVIOR}}

## Memories that shape POLYBIUS — cite, don't duplicate

{{MEMORIES_CITE_DONT_RESTATE}}

## Hygiene loose ends

{{HYGIENE_LOOSE_ENDS}}

## Honest caveats

{{HONEST_CAVEATS}}

End handoff.
```

`{{SUPERSEDES_CLAUSE}}` expands to ` — most of its open threads are now resolved or evolved; cite-don't-restate.` when `{{SUPERSEDES_HANDOFF}}` is named; otherwise both slot and clause expand to empty and the `**Supersedes:**` line is omitted entirely.

---

## Worked example

The canonical example is `HANDOFF_POLYBIUS_2026-05-16.md` at the repo root. Read that file to see the slots filled with real engagement content — credential discipline (Arc 25) as `{{LOAD_BEARING_CONTEXT}}` section 1, dev Ariadne deployment as section 2, CI workflow as section 3, the bw repo table at the bottom of context, and the recommendation menu at the top.

That handoff was authored before this template existed — it is the de-facto template the slotted form is abstracted from. Per Arc 27 directive A8, existing handoff docs are NOT retroactively reformatted to fit this template; the template is forward-only.

---

## Where the filled handoff lives

POLYBIUS writes the filled handoff to `HANDOFF_POLYBIUS_{{HANDOFF_DATE}}.md` at the project / user-tier root (the same level as `CLAUDE.md` for the relevant tier). Suffix `_eod` / `_v2` / etc. for multi-handoff days.

The PRINCIPAL pastes the filled handoff (or its one-line pointer per the durable-substrate-with-short-prompts pattern, `MAJOR_POLYBIUS.md` §4.5) to a fresh POLYBIUS session at the start of the next engagement.

---

## When to refresh the on-disk handoff

Per `MAJOR_POLYBIUS.md` §16.2 Mode 1 (handoff + compaction): keep the handoff current as session intent shifts materially. Concretely:

- After a `/compact` event that left the session re-orienting against a stale handoff.
- After a substantive engagement phase closes (an arc ships, a multi-workspace propagation lands, a thread the recommendation-menu pointed at gets done).
- When new pending directives or bw tickets accumulate that the next session should pick up first.

Refreshing is cheap; running the next session against a stale handoff is not. Same discipline as the paste-instruction refresh discipline (`MAJOR_POLYBIUS.md` §6 + `substrate/templates/paste-instruction-template.md` "When to refresh the on-disk copy").

---

## Why a slotted template rather than re-authoring from scratch each time

The morning's `HANDOFF_POLYBIUS_2026-05-16.md` is the de-facto template; the next handoff under that convention would re-invent the structure each time. The slotted form makes the structure explicit, reviewable, and version-controllable — the same reasons `paste-instruction-template.md` is slotted (per its "Why string substitution" section).

The template stays under `substrate/templates/`; changes appear in diff history. Slot values are visible separately from the template structure; if a handoff is hard to read, the failure point is usually a slot that was filled vaguely (most often `{{ONE_PARAGRAPH_STATE}}` or `{{LOAD_BEARING_CONTEXT}}`), not the structure itself.

If a future workflow surfaces a real need for an LLM-generated handoff (e.g., the slot set stops being expressive enough for some class of engagement), revisit then. Until that signal arrives, this is the answer.
```

**End of template file.** ADA creates the file at `substrate/templates/handoff-doc-template.md` with `author: Denson Smith` in frontmatter (per A7 + `substrate/CLAUDE.md` authorship discipline).

**Frontmatter house-style note (rev2, ARGUS P2-3).** The existing templates `substrate/templates/paste-instruction-template.md` and `substrate/templates/autonomous-mode-activation-template.md` have NO YAML frontmatter (their first line is the heading). The new `handoff-doc-template.md` ADDS `author: Denson Smith` frontmatter per A7 + `substrate/CLAUDE.md` authorship discipline. This is a deliberate addition above the current template house style; future templates SHOULD adopt the same `author: Denson Smith` frontmatter pattern. CATO should note this as the new convention rather than flagging it as drift from the existing two templates.

### §4.5 — install.sh wiring (IN scope this arc — concrete ADA instruction)

**Verified (rev2, ARGUS P1-4):** `substrate/install.sh` lines 109-116 use an **explicit** `TEMPLATE_NAMES` bash array, NOT a wildcard glob:

```
TEMPLATE_NAMES=(
  paste-instruction-template.md
  onboarding-questions.md
  consent-prompts.md
  polling-cron-prompt-template.md
  activation-paste-cheatsheet.md
  autonomous-mode-activation-template.md
)
```

Without an explicit append, the new `handoff-doc-template.md` will NOT deploy to consumer workspaces on install — silent under-deployment, and the new substrate canon at `MAJOR_POLYBIUS.md` §16 would cross-reference a template that consumer-tier POLYBIUSes never receive.

**ADA instruction:** append `handoff-doc-template.md` to the `TEMPLATE_NAMES` array in `substrate/install.sh` as part of this build. This is in-scope for Arc 27 — the template IS the substrate edit; wiring it to deploy is part of shipping it (not a deferred follow-up). The append is one line; preserve the array's existing order and add the new entry at the bottom.

**Smoke beat (Phase C):** `grep handoff-doc-template substrate/install.sh` returns at least one hit confirming the array append landed. VERA Probe 8 (added below) makes this explicit.

---

## §5 — Notes for ADA

### §5.1 — Ground-check preamble (verbatim, per `MAJOR_PLINY.md` §5.2)

> Ground-check every concrete example in the design against the shipped code, specifically:
> - JSON example shapes (response bodies, request bodies)
> - Function/method signatures (parameter names, types, return types)
> - Error message text (exact string match)
> - Line ranges in path:line citations
> - HTTP response codes
> - Wire-protocol constants (header names, status codes, envelope keys)
>
> If a design example contradicts the shipped code, the shipped code is canon — flag the design drift but build to ship reality.

For this arc the ground-check surface is mostly **path:line citations into `substrate/MAJOR_POLYBIUS.md` and `substrate/operating-disciplines.md` cross-refs.** ADA must verify every cited section number against the file at build time:

- Verify `substrate/MAJOR_POLYBIUS.md` §15 closes around line 789 (the empirical anchor line) before inserting §16 after the §15 closing `---`. If `MAJOR_POLYBIUS.md` has been edited since this design was authored, line numbers will have shifted — find the §15 closing block by section heading match, not by line number.
- Verify `substrate/operating-disciplines.md` §20.7 closes around line 942 before inserting §21 after the §20.7 closing `---`. Same caveat — find by heading match.
- Verify `substrate/MAJOR_POLYBIUS.md` cross-refs from new §16.7 (specifically §4.5, §6, §7, §14, §15) all point at sections that still exist at the cited names.
- Verify `substrate/operating-disciplines.md` cross-ref from new §16.4 to "§21" matches the section number ADA actually inserts (if §20 has grown a §20.8 or §20.9 in the interim, the new section may need to be §22 — pick the next free number and update both the new §21 heading AND the cross-ref in §16.4).
- Verify `docs/sessions/2026-05-16-substrate-update-architecture-reframe--retro.md` exists at that exact path (it does at the time of this design).
- Verify `HANDOFF_POLYBIUS_2026-05-16.md` exists at the repo root (it does).
- Verify `substrate/templates/paste-instruction-template.md` and `substrate/templates/autonomous-mode-activation-template.md` exist for the house-style references in §4.

### §5.2 — Worktree + branch

- **Worktree path:** `C:\Users\denso\claude_projects\the-stoa\.claude\worktrees\arc-27-build`
- **Branch:** `arc-27/build` (off `main`)
- **Files touched (four total — rev2 added install.sh + one-line MAJOR_POLYBIUS.md §1 forward-pointer):**
  - `substrate/MAJOR_POLYBIUS.md` — insert new §16 (~140 lines) between §15 closing `---` and `Standby, run.`; **plus one-line forward-pointer at the end of §1 ("Who you serve")** — see §5.6 below for exact insertion.
  - `substrate/operating-disciplines.md` — insert new §21 (~30 lines) between §20.7 closing `---` and `## Agent-regime inverses`
  - `substrate/templates/handoff-doc-template.md` — new file (~140 lines), frontmatter `author: Denson Smith`
  - `substrate/install.sh` — append `handoff-doc-template.md` to the `TEMPLATE_NAMES` array (lines 109-116) — see §4.5 above for the verified-current array contents and §5.7 below for the exact one-line addition.

### §5.3 — Authorship

Per A7 + `substrate/CLAUDE.md` authorship discipline: all edits credit **Denson Smith**. The new template file has explicit frontmatter `author: Denson Smith` — verify before commit per the mandatory audit. No other author-like fields in the touched files (the role files do not carry per-file `author:` frontmatter; their authorship is the repo's, which is Denson Smith per the repo's LICENSE + CLAUDE.md).

### §5.4 — Heartbeat-and-read-before-write

Per `MAJOR_PLINY.md` §5.8 + universal CAPTAIN discipline: ADA posts entry / state-transition / completion heartbeats on `stoa--32b.3` via `bw comment`, and reads `bw show stoa--32b.3 2>&1 | tail -<N>` before each write to pick up any new orchestrator or POLYBIUS comments (tagged `[for: ADA]`). Pull-heartbeat floor: 60 minutes.

### §5.6 — MAJOR_POLYBIUS.md §1 forward-pointer (rev2, ARGUS P2-2)

**Why:** §16.5's POLYBIUS-as-collective lens is load-bearing for seat identity, but rendering it inside §16 (defensible per A5) leaves §1/§2 readers at risk of missing it. The cheapest mitigation is a one-sentence forward-pointer at the END of §1 ("Who you serve") so any reader skimming the role-file open meets the lens at least as a pointer.

**Where to insert:** at the END of `substrate/MAJOR_POLYBIUS.md` §1 ("Who you serve"), as the closing paragraph of that section — after §1's existing closing prose and before §1 ends / §2 begins. ADA: find §1's last paragraph by heading match (`## 1.` heading, then read forward until the next `##` heading), insert the line immediately before the section transition.

**Exact text to insert** (one paragraph, one sentence):

```
See §16.5 for the multi-version collective framing of "you" — "POLYBIUS" names the collective of currently-active sessions, idle relay-channel sessions, and the substrate they co-author; any specific session (this one included) is one currently-active branch of that collective.
```

This is the deliberate scope expansion flagged in §1 of this design. Beyond this one line, no other content in MAJOR_POLYBIUS.md §1-§15 changes. CATO verifies §1 is otherwise untouched; ARGUS Probe-9 below.

### §5.7 — install.sh TEMPLATE_NAMES append (rev2, ARGUS P1-4)

**Why:** see §4.5 above. The current `TEMPLATE_NAMES` array is explicit, not wildcard; without an append the new template never deploys.

**Where to insert:** in `substrate/install.sh`, inside the `TEMPLATE_NAMES=( ... )` array currently at lines 109-116. Append `handoff-doc-template.md` as a new entry at the bottom of the array, preserving the existing six entries and the array's indentation pattern.

**Resulting array shape** (after the edit):

```
TEMPLATE_NAMES=(
  paste-instruction-template.md
  onboarding-questions.md
  consent-prompts.md
  polling-cron-prompt-template.md
  activation-paste-cheatsheet.md
  autonomous-mode-activation-template.md
  handoff-doc-template.md
)
```

No other line in `install.sh` changes. ADA: this is one line of new content; CATO verifies no surrounding hunks were accidentally edited.

### §5.8 — Commit subject (suggested)

Following the Arc 26 commit-subject convention:

```
arc-27: POLYBIUS session lifecycle discipline (build)

- substrate/MAJOR_POLYBIUS.md: new §16 (POLYBIUS session lifecycle — three modes + multi-artifact handoff + Ariadne-search-ready authoring + POLYBIUS-as-collective lens + N=1 provenance); plus one-line §1 forward-pointer to §16.5
- substrate/operating-disciplines.md: new §21 (Ariadne-search-ready authoring, universal-team framing)
- substrate/templates/handoff-doc-template.md: new slotted template (forward-only; existing handoff docs unchanged)
- substrate/install.sh: append handoff-doc-template.md to TEMPLATE_NAMES array so the new template deploys to consumer workspaces

Encodes PRINCIPAL's 2026-05-16 declarations on stoa--32b.3. Locked decisions per substrate/arcs/arc-27-build-directive.md A1-A8.

Cross-refs:
- stoa--32b.3 (work-unit; primary source); stoa--32b (parent epic; body predates stoa--32b.3 fold-in); stoa--32b.1 + stoa--32b.2 (sibling future arcs, NOT touched this arc)
- HANDOFF_POLYBIUS_2026-05-16.md at repo root (canonical worked example of Mode 3; de-facto template for new handoff-doc-template.md)
- docs/sessions/2026-05-16-substrate-update-architecture-reframe--retro.md (adjacent context for the broader stoa--32b epic; the lifecycle/handoff/Ariadne/collective disciplines surfaced after the retro was authored — see §16.7)
- Arc 26 (stoa--dxw, commit 6ccfd0e — predecessor)
```

CATO will check this subject for accuracy.

---

## §6 — Probes (recap from directive Phase B, for VERA)

Per A1 — VERA executes these against the integrated build. ADA does not pre-test these; VERA is the verification seat. ARGUS may sharpen the probe set during Phase 1 critique; the set below is the directive's acceptance set as authored.

1. **Lifecycle-modes probe.** A future POLYBIUS reading `MAJOR_POLYBIUS.md` cold can correctly classify "we are at a handoff+compaction moment, not a new-session moment" given a scenario description. Synthetic test: VERA pastes two scenario descriptions to a fresh-context read (e.g., scenario A: "session has been running 3 days, just hit `/compact`, no role-file edits landed since session start" → expected classification: Mode 1; scenario B: "Arc 27 just shipped substrate edits to MAJOR_POLYBIUS.md; running session loaded role file pre-edit" → expected classification: Mode 2 trigger, with Mode 3 relay-channel pattern). Verify both classifications are correct.

2. **Multi-artifact-handoff-shape probe.** The new §16.3 enumerates all six artifact types (index doc + bw tickets + retro docs + design artifacts + commits + role files/disciplines) explicitly. `grep -c` on the relevant rows of the table; verify count = 6.

3. **Ariadne-readiness probe.** Authoring discipline is named explicitly in the new §16.4 (titles + cross-refs + content-density + alignment-with-compaction-recovery). All four sub-disciplines must be present as explicit bullets. Cross-ref to operating-disciplines.md §21 (the universal-team framing) must be present. `grep -n "Ariadne" substrate/MAJOR_POLYBIUS.md` should return hits.

4. **POLYBIUS-as-collective probe.** The collective-lens framing is present in §16.5. Verify the canonical sentence "The collective IS POLYBIUS" or close paraphrase appears; verify the four "explains structurally" bullets are present (substrate corpus + decay-not-termination + Ariadne search + lifecycle/multi-artifact coherence). `grep -n "multi-version collective" substrate/MAJOR_POLYBIUS.md` should return hits.

5. **Cross-ref probe.** New §16 cross-refs the retro doc, `stoa--32b` epic, sibling children `stoa--32b.1` + `stoa--32b.2`, `HANDOFF_POLYBIUS_2026-05-16.md`, and relevant existing sections of MAJOR_POLYBIUS.md (§4.5, §6, §7, §14, §15) and operating-disciplines.md (§21). All cross-refs resolve to live paths or live section numbers — VERA verifies each by `grep` against the cited file.

6. **Authorship-attribution probe.** All edited/new files credit Denson Smith. New `substrate/templates/handoff-doc-template.md` has frontmatter `author: Denson Smith`. No LLM-templated placeholder names anywhere in the diff. `grep -niE "author:|created_by:|maintainer:" <touched files>` should show only Denson Smith (or empty for files with no author-like fields).

7. **CURRENT regression probe.** `substrate/skills/check-substrate-updates/check.sh` against all four consumer workspaces still reports CURRENT post-edit. (the-stoa itself will show DRIFTED on `MAJOR_POLYBIUS.md` + `operating-disciplines.md` + the new template + `install.sh` — that is expected; substrate update propagates via `apply.sh` on next consumer-tier touch.)

8. **install.sh wiring probe (rev2, ARGUS P1-4).** `grep handoff-doc-template substrate/install.sh` returns at least one hit; the new template name appears inside the `TEMPLATE_NAMES` array (lines ~109-117 after the append) with the same indentation pattern as the existing entries. Synthetic deploy probe: VERA may also run `install.sh` against a throwaway target dir and verify `handoff-doc-template.md` lands at `<target>/.claude/templates/handoff-doc-template.md`. Confirms the new template will actually deploy to consumer workspaces.

9. **§1 forward-pointer probe (rev2, ARGUS P2-2).** `grep -n "§16.5" substrate/MAJOR_POLYBIUS.md` returns at least one hit inside §1 (well before the new §16 block). The text "multi-version collective framing" appears once in §1 as a forward-pointer to §16.5. Verifies the discoverability mitigation landed without scope expansion beyond the one-line addition.

**CATO cold-reads** (per directive):

- The diff for wording drift, scope creep, cross-reference correctness, output-format coherence, authorship discipline.
- PRINCIPAL's exact phrasing per A2: verify the two block-quoted PRINCIPAL declarations in §16.1 match the `stoa--32b.3` body verbatim; verify the load-bearing inline phrases ("handoff + compaction works for a long time", "previous POLYBIUS sits idle and is available to answer questions from the new polybius indefinitely", "becomes less relevant over time but may still retain important information") appear with exact wording.
- §15 N=1 honesty: verify §16.6 names the N=1 + PRINCIPAL-declaration provenance and does NOT over-generalize from single observation into structural-fact language.

**ZENO** checks `stoa--32b.3` deliverables 1-3 (the "Deliverables (sketch)" list) + Phase B probes 1-7 each marked DONE by artifact reference.

---

## §7 — Self-assessed weak points

Five concrete weak points where this design could wrong-foot ARGUS / ADA / VERA / CATO / ZENO. Per the DAEDALUS self-assessment discipline, named here so ARGUS sees what I see and can focus on what I don't.

**Rev2 ARGUS round 1 disposition (2026-05-16):** ARGUS confirmed weak points 2, 3, and 5 (one each as P2-2, P1-1, P1-4). Additional findings (P1-2 retro re-scoping, P1-3 A2 verbatim phrase, P2-1 epic-body caveat, P2-3 frontmatter house-style note) were beyond DAEDALUS round 1 self-assessment — surfaced by ARGUS cold-audit and fixed in rev2. Per-weak-point status inline below.

### Weak point 1 — Section-number choice (§16 vs extending §6) may conflict with downstream cross-refs

**Risk:** I chose new §16 over extending §6, with rationale that POLYBIUS-lifecycle and PLINY-recovery are structurally distinct. But: if any sibling doc (operating-disciplines.md, a CAPTAIN envelope, the spec at `user-beadwork/plans/three-role-recursive-architecture.md`, or any test) cross-refs `MAJOR_POLYBIUS.md` with a "§N where N > 15" assumption that this insertion will collide with, the cross-ref breaks silently.

**Why this shape anyway:** A8 hard-locks reopening §6; extending §6 would mix two distinct mechanisms in one section, which is the worse outcome for substrate readability. New section at end is the conservative choice. Mitigation: VERA Probe 5 (cross-ref probe) catches any direct breakage; ARGUS can sharpen by grep'ing the substrate for `MAJOR_POLYBIUS.md §16` references that pre-exist.

### Weak point 2 — Collective-lens rendering location (inside §16 vs §1/§2 peer) may hide it from §1/§2 readers — ARGUS-CONFIRMED (P2-2); MITIGATION APPLIED IN REV2

**Risk:** I rendered the collective lens as §16.5 inside the new lifecycle section, not as a peer in §1 ("Who you serve") or §2 ("What you do"). A reader who skims §1-§2 to understand seat identity may miss the lens entirely; they only meet it if they read deep enough to hit §16.5. If the lens is meant as load-bearing for seat identity, that placement risks under-surfacing it.

**Why this shape anyway:** A5's four structural explanations (substrate corpus + decay-not-termination + Ariadne search + lifecycle/multi-artifact coherence) are entirely *inside* §16's subject matter. Placing the lens in §1 separates it from the disciplines that depend on it, requiring the reader to hold §16 in their head as they read §1. Co-location is the cleaner ordering.

**Rev2 mitigation (ARGUS P2-2):** added a one-line forward-pointer at the END of `MAJOR_POLYBIUS.md` §1 ("Who you serve") pointing readers to §16.5 for the collective framing. Exact text + insertion location in §5.6 above. The lens stays co-located in §16.5 with the disciplines that depend on it; §1 readers now meet a pointer to it. One-line scope expansion documented in §1 of this design. VERA Probe 9 verifies.

### Weak point 3 — §16.6 N=1 framing risks reading as "PRINCIPAL said so → it's canon now, evidence later" — ARGUS-CONFIRMED (P1-1); FRAMING-FIX APPLIED IN REV2

**Original risk:** §16.6 round 1 read "the PRINCIPAL-declaration path that §15's framing explicitly allows." ARGUS P1-1 confirmed this misreads §15: §15 names exactly ONE canon-promotion gate, the `operating-disciplines.md` §6.7.1 three-condition gate. It does NOT carve out a separate PRINCIPAL-declaration shortcut. The honest framing — per `stoa--32b.3` ticket body's §15 honesty section and the retro §7 framing — is "the gate applies differently when PRINCIPAL declared," not "§15 carves out an allowed path."

**Rev2 framing-fix (ARGUS P1-1):** §16.6 rev2 names `operating-disciplines.md` §6.7.1 as the canon-promotion gate directly, explicitly acknowledges that this discipline enters substrate canon **off-gate** on PRINCIPAL's project-direction authority, and names future-evidence-accretion against §6.7.1 as the path to structural-lesson confidence. The substrate-canon-in-now claim is grounded honestly; structural-lesson promotion remains a future-arc concern.

**Why substrate canon goes in now anyway:** PRINCIPAL named the discipline; project-direction declarations have load-bearing authority over what substrate captures even when the §6.7.1 evidence gate has not yet been satisfied. The rev2 framing makes that off-gate path honest rather than papering it as a "§15 carve-out."

### Weak point 4 — "Forward-only" wording in §16.4 + §21 + §4 may not be visible enough to prevent retroactive-refactor temptation

**Risk:** A8 hard-locks retroactive refactor of existing handoff docs, prior retros, and broader bw ticket convention restructuring. I have "Forward-only" language in §16.4, §21, and §4.5 — three separate places. A future arc-author may not read all three, see the Ariadne-search-ready discipline in §21, and decide to "improve" existing artifacts to match. The hard-lock then leaks.

**Why this shape anyway:** Saying "forward-only" once would be missable; saying it three times is mildly redundant but durably protective. The risk is more about future-arc behavior than current-arc behavior. Mitigation: each "forward-only" mention cross-refs Arc 27 directive A8 explicitly (so a future arc reading any one of them gets routed back to the lock).

### Weak point 5 — install.sh template-deploy wiring requires explicit append — ARGUS-CONFIRMED (P1-4); VERIFIED + PRE-FLAGGED FOR ADA IN REV2

**Original risk:** §4.5 round 1 hedged ("if wildcard / if explicit") rather than verifying the install.sh shape. ARGUS P1-4 confirmed: `substrate/install.sh` lines 109-116 use an explicit `TEMPLATE_NAMES` bash array, NOT a wildcard. Without an append, the new template silently fails to deploy to consumer workspaces.

**Rev2 fix (ARGUS P1-4):** §4.5 rev2 replaces the hedge with the verified-current array contents and a concrete ADA instruction to append `handoff-doc-template.md` to `TEMPLATE_NAMES`. §5.7 spells out the exact one-line edit and the resulting array shape. The install.sh edit is IN SCOPE this arc — the template IS the substrate edit; wiring it to deploy is part of shipping it. VERA Probe 8 verifies via `grep` + optional synthetic-target install run.

**Why the round 1 hedge was wrong:** DAEDALUS one-job discipline does NOT mean leaving deploy-wiring questions implicit. Design questions answerable by a 5-line read of `install.sh` belong in the design — they remove ambiguity from ADA's build phase rather than create work. Rev2 corrects.

---

## §8 — Residual questions for ARGUS

- **Section-number choice (Weak point 1).** Has any pre-existing substrate doc taken a hard dependency on the absence of `MAJOR_POLYBIUS.md` §16? Grep for `MAJOR_POLYBIUS.md §16` or `MAJOR_POLYBIUS.md §1[6789]` in `substrate/`, `agents/`, `docs/`, and the spec at `user-beadwork/plans/`. If yes, surface as a P0; if no, confirm the choice.
- **Collective-lens rendering (Weak point 2).** Is the §16.5 placement under-surfacing the lens for §1/§2 readers? An alternative ARGUS may prefer: add a one-sentence forward-reference at the bottom of §1 ("see §16.5 for the multi-version collective framing of 'you'") without moving the lens. Cheap to add; preserves co-location while raising discoverability.
- **N=1 framing wording (Weak point 3).** Does §16.6's "project-direction authority; substrate-canon promotion via PRINCIPAL-declaration path per §15 framing" language adequately resist the "PRINCIPAL said so → canon by declaration" misread? If ARGUS prefers more guarded wording, propose specific edits.
- **Universal-team scope of §21.** Does `operating-disciplines.md` §21 belong here, or should the Ariadne-search-ready discipline live entirely in `MAJOR_POLYBIUS.md` §16.4 with no operating-disciplines.md addition? I chose IN scope because the discipline applies team-wide; ARGUS may have a different read on locus-tightness for the first arc that names this canon.
- **Template scope.** I marked the handoff-doc-template.md as IN scope. ARGUS may prefer OUT-of-scope (defer to a future arc with the smaller surface) — if so, name the rationale for the deferral and what triggers the future arc.

---

End design.
