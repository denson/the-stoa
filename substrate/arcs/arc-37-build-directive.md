# Arc 37 build directive — Substrate architecture canonification batch (6 candidates)

**Status:** LOCKED at dispatch authoring (2026-05-17). A1-A19 are not DAEDALUS-revisable; sub-decisions inside A8/A9/A10/A11/A12/A13 are DAEDALUS discretion unless surfaced as PRINCIPAL-gate per `operating-disciplines.md` §25.

**Work-unit ticket:** none single; this is a 6-candidate bundled batch shipping per-candidate substrate-architecture canon. Each candidate closes its source ticket on ship per A18. Mirrors Arc 32 (5 candidates) + Arc 34 (4 candidates) bundling pattern.

**Candidates:**

| C | Ticket | Topic | Primary surface |
|---|---|---|---|
| C1 | stoa--86k | Two-team forge/shop division of concerns | MAJOR_POLYBIUS.md behavioral section |
| C2 | stoa--kt6 | Multi-team interoperation unified canon | operating-disciplines.md new top-level section |
| C3 | stoa--wad | Four-layer identity model + memories-as-alignment | operating-disciplines.md + MAJOR_POLYBIUS.md |
| C4 | stoa--ntn | Operating-mode progression canon | operating-disciplines.md §10 + §11 extensions |
| C5 | stoa--53u | Idle-state retrospective-narrative confabulation discipline | operating-disciplines.md §19.7 (sister to §19.6) |
| C6 | stoa--7e3 | Handoff-author skill (new substrate skill) | substrate/skills/handoff-author/ + install.sh SKILL_NAMES |

**Context:** Per the-stoa SPECIFICATION.md §13.4 Pass 3 of the make-the-team-meet-the-spec workplan. After Arc 37 + Arc 38 + Arc 39 ship: zero open substrate-canon tickets at the-stoa; substrate ready for Pass 8 behavioral validation via stellation dispatch.

---

## A1 — One arc, one gauntlet (LOCKED)

Arc 37 ships as a single end-to-end gauntlet (DAEDALUS → ARGUS → ADA → VERA → CATO → ZENO → PLINY signoff → PR merge). All 6 candidates ship in one PR. Mirrors Arc 32 / Arc 34 bundling shape.

**Estimated arc size:** medium-large; comparable to or slightly larger than Arc 34 (4 candidates). The 6th candidate (handoff-author skill) is a NEW skill file with worked examples — larger surface than prose-only canon edits. Realistic gauntlet wall-clock: 90-180 min including verifier round.

---

## A2 — C1: Two-team forge/shop behavioral canon (LOCKED, stoa--86k)

**Substrate touch-point:** new section in `substrate/MAJOR_POLYBIUS.md` (DAEDALUS picks exact section number per A8).

**Content (LOCKED):**

- The two-team architecture: each project has two teams sharing the deployed substrate.
  - **Base team** — the standard Stoa team (POLYBIUS + PLINY + 10 CAPTAINs) deployed via install.sh. Kept in sync with the-stoa via check-substrate-updates. Handles substrate maintenance + designs the project-specific team.
  - **Project team** — authored by the base team via interaction with PRINCIPAL. Handles day-to-day project work. Specialized via the project's files, accumulated memories, and additional specialist agents in `custom/` paths.
- The metaphor: base team is the **forge**; project team is the **shop**.
- The mechanical realization: per-class path convention from Arc 29 §17 + §23 (custom/ subdir for project-specific). C1 names this convention's BEHAVIORAL framing — Arc 29 covered the WHERE (path convention); C1 covers the WHAT (what each team does).
- Routing rule: when work arrives, route to base team if it's about the team's substrate / discipline / structure; route to project team if it's about the project's domain (its codebase, its product features, its operational concerns). Cross-team requests follow §7.4 cross-tier routing.
- Cross-ref to operating-disciplines.md §23 + §17 (existing base-vs-custom path convention) + MAJOR_POLYBIUS.md §18 (user-tier housekeeping).

**Out-of-scope for C1:**
- Re-litigating the per-class path convention (Arc 29 settled that).
- Building a "design-the-project-team" skill or onboarding flow (deferred — current tier2-project-onboarding skill exists; C1 doesn't extend it).
- Defining specific routing-decision algorithms (POLYBIUS owns routing judgment; C1 names the framing, not a decision tree).

---

## A3 — C2: Multi-team interoperation canon (LOCKED, stoa--kt6)

**Substrate touch-point:** new top-level section in `substrate/operating-disciplines.md` (DAEDALUS picks section number per A9 — likely §29 since §28 is Co-Authored-By trailer).

**Content (LOCKED):**

- The multi-team architecture: multiple projects coexist in the Stoa ecosystem (the-stoa as the canonical forge; ariadne-core-workspace + sub-project; railway_stoa; sector-4; etc.). Each team is its own project with its own substrate.
- **Cross-team interoperation via consumed artifacts:** skills, tooling, deployed services. The Railway team produces skills the Ariadne team consumes. The-stoa produces the substrate every team consumes.
- **Cross-team bw coordination:** prefix-namespace convention (`stoa--`, `ariadne--`, `railway--`, `s4--`, `u--` for user-tier). Downward-only visibility per existing §7.5 cross-tier write boundaries; cross-tier coordination meets in the lower tier via `[for:]` tags per §7.4.
- **Cross-team requests** flow through user-tier POLYBIUS (the only seat with cross-team visibility) OR through PRINCIPAL as broker. Project-tier teams do NOT directly dispatch into peer-project teams — that would violate §7.5 write boundaries.
- **Team discovery:** convention is "peer projects live as siblings in PRINCIPAL's claude_projects/ directory." No substrate-tier registry; discovery is via PRINCIPAL's awareness + user-tier POLYBIUS's cross-project visibility. Future arc may add a registry if the convention proves insufficient at scale.
- Cross-ref to operating-disciplines.md §7.4 + §7.5 (existing cross-tier conventions) + MAJOR_POLYBIUS.md §5.1.1.1 (Arc 32 cross-project sequencing).

**Out-of-scope for C2:**
- Building a substrate-tier team registry (convention-based discovery is sufficient for current ecosystem size).
- Building cross-team-bw-fetch tooling (`bw show` works per-project; agents handle the per-workspace navigation).
- Defining a multi-team dispatch protocol (cross-team requests are PRINCIPAL-or-user-tier-mediated; no peer-to-peer protocol).

---

## A4 — C3: Four-layer identity model + memories-as-alignment (LOCKED, stoa--wad)

**Substrate touch-point:** new section in `substrate/operating-disciplines.md` (DAEDALUS picks section number per A10) + cross-ref note in `substrate/MAJOR_POLYBIUS.md`.

**Content (LOCKED):**

- The four-layer identity model: a Stoa-deployed agent's identity has four layers.

  | Layer | Content | Variance |
  |---|---|---|
  | Role file | What kind of agent (POLYBIUS / PLINY / CAPTAIN_X) | Universal across users |
  | Memories | Standing PRINCIPAL preferences, accumulated lessons, project-specific knowledge | Unique per user / project |
  | Handoff | Current work-state for session continuity (per handoff-author skill, C6) | Unique per engagement |
  | bw substrate | Durable detail (tickets, history, comments) | Unique per project |

- **Memories are the user-alignment layer.** Different PRINCIPALs → different memory accumulations → different agent behaviors. This is the alignment mechanism working correctly, not noise to normalize away. Substrate supports memory accumulation as a first-class feature.
- **Memory introspection** is supported: when PRINCIPAL asks "what do you remember about me?", agents return a curated answer from accumulated memories rather than confabulating.
- **Memory authoring** is collaborative: PRINCIPAL correction + expansion of memories is a normal action, not exceptional.
- **Cross-layer interactions:** when the base team designs the project team (per C1), the project team inherits memory-access conventions. The handoff layer (C6) captures within-session state; memories capture cross-session standing knowledge; bw captures durable detail; role files are universal.
- Cross-ref to global `~/.claude/CLAUDE.md` (where user-tier memories auto-load) + operating-disciplines.md §10.1 generational lineage (memories persist across generations).

**Out-of-scope for C3:**
- Building a memory-introspect skill (could be future arc; C3 ships the prose canon for the discipline, not the skill).
- Memory-curation tooling (out of scope; substrate doesn't build user-memory editing UIs).
- Cross-project memory sharing (memories are per-user-tier OR per-project; no cross-project memory channel ships).

---

## A5 — C4: Operating-mode progression canon (LOCKED, stoa--ntn)

**Substrate touch-point:** extensions to `substrate/operating-disciplines.md` §10 (HITL/Autonomous) + §11 (autonomous-mode-setup). DAEDALUS picks whether the progression canon lands as new subsections inside §10/§11 OR as a new top-level section (per A11).

**Content (LOCKED):**

- Three operating modes (existing canon at §10 + §11 — recap for completeness):
  - **Mode 2 — Pair programming:** interactive prototyping, scoping, exploration. PRINCIPAL in-the-loop on every decision. Conversational; bw used as durable record but lightweight.
  - **Mode 1 — Full team:** formal gauntlet (DAEDALUS → ARGUS → ADA → VERA + CATO + ZENO). PRINCIPAL decision-points only — phase ratification, ship/no-ship. bw heartbeats at phase transitions.
  - **Semi-autonomous:** long-running engagements with periodic check-in. PRINCIPAL exception-handler only — escalation triggers per directive. Monitor + bw-poll bridge; radio-check between orchestrators.
- **The progression sequence** (typical engagement maturity):
  - Engagement starts in Mode 2 to scope + scope-lock.
  - Transitions to Mode 1 for the formal build (arc dispatched).
  - May transition to semi-autonomous for long-running phases (multi-day work, parallel arcs).
  - **Regression upward** when escalations require re-engagement (PRINCIPAL-gate hits; substance disagreement; ambiguity).
- **Transition triggers** (concrete signals + the seat that calls the transition):
  - **Mode 2 → Mode 1:** scope is locked + directive is authored + PRINCIPAL ratifies dispatch. user-tier POLYBIUS calls.
  - **Mode 1 → Semi-autonomous:** PRINCIPAL declares "AFK" or "autonomous" + escalation triggers are explicit in the directive. user-tier POLYBIUS calls based on PRINCIPAL signal.
  - **Semi-autonomous → Mode 1:** PRINCIPAL re-engages (responds to bw query; surfaces preference; ratifies phase). Any seat can call by surfacing the escalation.
  - **Mode 1 → Mode 2:** PRINCIPAL pulls back for clarification or re-scoping. PRINCIPAL calls.
- **Mode declaration in directives:** every arc directive declares its expected mode in the dispatch frame (existing pattern; this section makes it explicit). Default for arc dispatches is semi-autonomous per Arc 21.
- **Mid-engagement mode transitions:** when the mode changes mid-engagement, the seat that calls the transition posts a `[mode-change <new-mode>] [from: <slug>]` comment on the coordination ticket. Peer seat reads + adapts.
- **Downward-propagation rule** (existing Arc 21 A4 canon): parent seat's mode propagates to dispatched subagents unless explicitly overridden. C4 makes the rule re-citable from a centralized location.

**Out-of-scope for C4:**
- Building a mode-management tool (mode is declared in prose; not enforced mechanically).
- Mode-specific escalation-trigger overrides (existing canon at §10 covers the universal triggers; mode-specific overrides are future arc if needed).
- Re-litigating the three modes (existing canon settled).

---

## A6 — C5: Idle retrospective-narrative confabulation discipline (LOCKED, stoa--53u)

**Substrate touch-point:** new subsection in `substrate/operating-disciplines.md` §19 (the confabulation section). DAEDALUS picks §19.7 (sister to §19.6 attestation-confabulation) or other sub-numbering per A12.

**Content (LOCKED):**

- **The failure mode:** orchestrator (or any seat) scans substrate when idle (between dispatches, after surfacing for review, while waiting for input). Encounters closed tickets / past work. Confabulates a narrative claiming the past work as own current-session accomplishment.
- **The empirical anchor** (2026-05-13): PLINY-stoa in a fresh terminal narrated "Engagement B" (7 tickets) as just-completed work — actually weeks-old work shipped by a prior PLINY session. Detailed confabulation with specific revision rounds, commit narratives, bundle-shape rationale.
- **Distinct from §19.6** (attestation-confabulation): §19.6 is about WHAT to cite at attestation time (live-verify, not assumption-from-context). C5 is about WHO did the work — refusing the retrospective narration when scanning idle substrate.
- **The discipline:**
  - **Closed tickets are evidence of past work, not of current work.** When scanning substrate for next-task, a CLOSED ticket means "do not re-do; do not re-narrate."
  - **A retrospective-narrative of completed work is only valid when it explicitly cites the merge SHA of work the agent itself did in this session.**
  - **Canonical orchestrator-scan procedure:** "Is there a SHIP verdict pending I need to act on?" → "Is there a [for: <self>] tagged comment I need to address?" → "What's the next QUEUED unblocked work the directive authorizes me to start?" The procedure NEVER includes "scan closed tickets for retrospective narration."
- **Cross-ref:** to §19.6 (attestation-confabulation) as sister discipline; to MAJOR_PLINY.md + MAJOR_POLYBIUS.md self-narrative sections (add cite-comments per A13).
- **N=1 provenance** per §6.7.1: single empirical anchor (2026-05-13 PLINY-stoa Engagement B confabulation); no observed recurrence since. Discipline enters canon off-gate per PRINCIPAL declaration; future-evidence accretion per §6.7.1.

**Out-of-scope for C5:**
- Mechanical enforcement (no pre-comment hook; agent discipline is the layer).
- Retroactive audit of past PLINY/POLYBIUS narratives for confabulation (forward-only).

---

## A7 — C6: Handoff-author skill (LOCKED, stoa--7e3)

**Substrate touch-point:** new `substrate/skills/handoff-author/SKILL.md` + install.sh SKILL_NAMES addition + optional role-file cross-refs. DAEDALUS adapts draft at `_drafts/skill_handoff_author.md` (preserved through Pass 1 explicitly for this candidate).

**Content (LOCKED):**

- **Skill invocation:** triggered when PRINCIPAL or the agent itself says "prepare for handoff," "before /compact," "snapshot for next session," or equivalent. Not auto-fired.
- **Six guiding principles** (from the draft; DAEDALUS may refine wording but not architecture):
  1. Highest value-per-token first
  2. Indirection over inlining
  3. Write for the context-free reader
  4. Curate based on what they'll need
  5. Cite, don't duplicate
  6. Honor the value/effort tradeoff
- **Suggested procedure (adapt-don't-template):** the skill is guidance, not a template. Agents apply judgment to produce a handoff doc fit for the specific engagement.
- **Three worked examples** (DAEDALUS authors during gauntlet):
  - POLYBIUS-session-end handoff (e.g., user-tier POLYBIUS handing off to a future session that will run the next arc batch)
  - PLINY-mid-arc handoff (e.g., orchestrator running long; needs to compact + resume without losing arc state)
  - Specialist-preservation handoff (e.g., a CAPTAIN holding accumulated context from a complex engagement; handing off to a future CAPTAIN session for the same work-stream)
- **Generation-handoff session-id record:** per the-stoa SPECIFICATION.md §10.1 + §12.5 future-work item, the handoff-author skill SHOULD include a section on recording the prior-generation session id(s) so successor generations can `/resume` them. DAEDALUS picks whether to fold this into C6 OR defer to a follow-up arc — recommend fold (the framing exists; the skill is the natural carrier).
- **Cross-refs:** in MAJOR_POLYBIUS.md + MAJOR_PLINY.md — optional one-line pointer noting "invoke handoff-author skill before /compact or session close." Light touch; the skill description handles trigger matching.

**Install.sh wiring:**
- Add `handoff-author` to SKILL_NAMES array (per Arc 27 stoa--uly precedent for skill additions).
- Verify install.sh dry-run lists the new skill at all three target modes (project / sub-project / user-tier).
- Per Arc 27 stoa--uly convention: SKILL.md frontmatter MUST carry `author: Denson Smith`.

**Out-of-scope for C6:**
- Authoring a mechanical handoff-generator (the skill is prose-guidance; agent applies judgment).
- Building handoff-archival convention (handoffs land at workspace root or wherever PRINCIPAL prefers; no substrate-mandated location).
- Cross-project handoff sharing (handoffs are per-engagement; no cross-project share channel).

---

## A8-A13 — DAEDALUS sub-decisions (per-candidate)

**A8 (C1 section number):** DAEDALUS picks new MAJOR_POLYBIUS.md section number. Suggested: §19 (after §18 user-tier housekeeping; matches numbering progression). Could also extend §16 (POLYBIUS lifecycle) with a subsection. User-tier POLYBIUS leans new §19.

**A9 (C2 section number):** DAEDALUS picks new operating-disciplines.md top-level section number. Suggested §29 (after §28 Co-Authored-By trailer). User-tier POLYBIUS leans §29.

**A10 (C3 section number):** DAEDALUS picks operating-disciplines.md section number for the four-layer identity model. Could land as §30 (parallel to §29) or as a subsection of §29 multi-team canon if the identity model conceptually nests within multi-team architecture. User-tier POLYBIUS leans separate §30 (the identity model is broader than multi-team; applies to single-team deployments too).

**A11 (C4 placement):** DAEDALUS picks whether the operating-mode progression canon lands as (a) new subsections inside existing §10 + §11, or (b) as a new top-level section (e.g., §31). User-tier POLYBIUS leans (a) — keeps existing mode canon coherent; extends rather than duplicates.

**A12 (C5 subsection number):** DAEDALUS picks §19 subsection number (likely §19.7 as sister to §19.6). User-tier POLYBIUS leans §19.7.

**A13 (C6 skill scope):** DAEDALUS picks whether to fold the generation-handoff session-id record into C6's SKILL.md (recommended) OR defer to a follow-up arc. If folded, the skill's procedure section grows by a step on session-id capture; the SKILL.md description may extend to mention the lineage-architecture cross-ref. User-tier POLYBIUS leans fold (the framing exists; the skill is the natural carrier; deferring adds an arc that exists for one paragraph of canon).

If any sub-decision exceeds DAEDALUS discretion, treat as PRINCIPAL-gate per §25 — halt + escalate immediately rather than proceed-then-flag.

---

## A14 — Self-application (LOCKED)

**C1-C5 don't have meaningful self-application** (prose canon doesn't require runtime exercise). C5 (idle confabulation discipline) is self-applied in the sense that this arc's POLYBIUS/PLINY MUST NOT confabulate retrospective narratives of past work during this arc — but that's negative self-application (refraining from a failure mode).

**C6 (handoff-author skill) IS self-applied:** if any seat in Arc 37's gauntlet hits a `/compact` event or session-close moment, the seat invokes the newly-shipped handoff-author skill to author its own handoff. Probability low for a 90-180min arc, but the canon authorizes it.

PLINY signoff verifies that all 6 candidates landed (per A18 closure check) and that the C5 self-application property held (no confabulation observed in arc execution).

---

## A15 — Cite-comment discipline (LOCKED)

Cross-references between the 6 new/extended sections must resolve via cite at every read-site. Specifically:
- C1 MAJOR_POLYBIUS.md section ↔ operating-disciplines.md §23 + §17 (base-vs-custom)
- C2 operating-disciplines.md §29 (new) ↔ existing §7.4 + §7.5 (cross-tier conventions) + MAJOR_POLYBIUS.md §5.1.1.1 (Arc 32 cross-project sequencing)
- C3 operating-disciplines.md §30 (new) ↔ MAJOR_POLYBIUS.md C1 + ~/.claude/CLAUDE.md (user-tier memories) + operating-disciplines.md §10.1 (lineage)
- C4 operating-disciplines.md §10 + §11 extensions ↔ MAJOR_PLINY.md + MAJOR_POLYBIUS.md mode-handling
- C5 operating-disciplines.md §19.7 ↔ §19.6 (attestation-confabulation sister discipline) + MAJOR_PLINY.md + MAJOR_POLYBIUS.md self-narrative sections
- C6 substrate/skills/handoff-author/SKILL.md ↔ MAJOR_POLYBIUS.md + MAJOR_PLINY.md cross-refs + operating-disciplines.md §10.1 (lineage; if A13 folds the session-id record)

Same pattern as Arc 26 / 28 / 29 / 30 / 31 / 32 / 33 / 34 / 35 / 36 cite-comments.

---

## A16 — Authorship attribution unchanged (LOCKED)

File-frontmatter `author:` fields remain Denson Smith per `CLAUDE.md` IMMUTABLE rule. Git commit `Author:` remains PRINCIPAL per `~/.claude/CLAUDE.md`. Arc 35's Co-Authored-By trailer convention applies to all CAPTAIN commits in arc-37/build per `operating-disciplines.md` §28.

**C6 new SKILL.md frontmatter:** MUST carry `author: Denson Smith` per Arc 27 stoa--uly precedent for new skills. Verify before commit; surface as substance disagreement if absent.

---

## A17 — Out-of-scope (HARD-LOCKED)

Arc 37 does NOT:

- Bundle bj5 (Arc 38 candidate per Pass 4) or utn/3sz/5sr/pqn (Arc 39 candidates per Pass 5) — those have separate arcs per the workplan; bundling here would create gauntlet bloat.
- Build mechanical enforcement infrastructure for any of the 6 disciplines (no pre-commit hooks, validators, etc.) — Arc 33's §27 mechanical/agent-split pattern; mechanical infra ships only on documented recurrence.
- Extend canon to non-POLYBIUS / non-CAPTAIN seats beyond what each candidate's existing scope covers.
- Touch the substrate-deploy mechanism (install.sh / apply.sh / revert.sh) beyond C6's SKILL_NAMES addition.
- Build the meta-agent for cross-generation lineage analysis (§10.1.3 / §12.5) — out of scope per spec; future post-spec work.
- Build memory-introspect skill (C3 out-of-scope; ships prose canon for memory-as-alignment, not the introspect tool).
- Build a multi-team registry (C2 out-of-scope; convention-based discovery sufficient).

If DAEDALUS or any CAPTAIN surfaces a scope concern touching A17, treat as substance disagreement: confirm A17 wording, file follow-up ticket if the concern has merit, do NOT expand this arc.

---

## A18 — Source-ticket closure (LOCKED)

On Arc 37 ship: close all 6 source tickets with cross-ref to merge commit + audit comment per candidate:

- stoa--86k (C1) closes with cross-ref + audit comment naming the new MAJOR_POLYBIUS.md section.
- stoa--kt6 (C2) closes with cross-ref + audit comment naming the new operating-disciplines.md section.
- stoa--wad (C3) closes with cross-ref + audit comment naming the new section + MAJOR_POLYBIUS.md cite.
- stoa--ntn (C4) closes with cross-ref + audit comment naming the §10/§11 extensions.
- stoa--53u (C5) closes with cross-ref + audit comment naming the §19.7 subsection.
- stoa--7e3 (C6) closes with cross-ref + audit comment naming the new skill + install.sh wiring + (if A13 fold) the session-id record extension.

Tag `[for: user-tier-polybius]` on at least one of the closed tickets (DAEDALUS picks which — recommend C6 since it's the most architecturally novel + ships the lineage hook).

---

## A19 — §15 N=1 honesty per candidate (LOCKED)

Per `MAJOR_POLYBIUS.md` §15 + `operating-disciplines.md` §6.7.1, each candidate enters canon with honest N=1 framing:

- **C1 two-team behavioral canon:** N=multi de-facto bit-by-it (every consumer workspace operates with base + custom convention since Arc 29); N=0 worked-when-applied with formal canon (Arc 37 ships the prose).
- **C2 multi-team interop:** N=multi de-facto bit-by-it (cross-team coordination works informally; bw prefix-namespaces in routine use); N=0 worked-when-applied with formal unified canon.
- **C3 four-layer identity:** N=0 bit-by-it of failure (no specific empirical anchor); discipline enters canon off-gate on PRINCIPAL declaration (2026-05-13).
- **C4 operating-mode progression:** N=multi de-facto bit-by-it (mode transitions handled organically across all arcs); N=0 worked-when-applied with formal progression canon.
- **C5 idle retrospective-narrative confabulation:** N=1 bit-by-it (2026-05-13 PLINY-stoa Engagement B confabulation); N=0 worked-when-applied with §19.7 canon.
- **C6 handoff-author skill:** N=multi de-facto bit-by-it (informal HANDOFF_*.md files exist in ariadne-core-workspace + the-stoa); N=0 worked-when-applied with formal skill.

Future-evidence accretion per §6.7.1 — promotion to "structural lesson" status accretes as future arcs ship under each candidate's canon.

---

## A20 — Pre-branch hygiene + worktree convention + signoff-accuracy (LOCKED, self-applied)

Per `MAJOR_PLINY.md` §5.9 + §5.9.4 + §5.10 + `operating-disciplines.md` §19.6.

PLINY runs the two-check rule before creating `arc-37/build`. Builds in `.claude/worktrees/arc-37-build/` (NOT in main worktree). User-tier POLYBIUS confirmed at dispatch authoring: local main = origin/main at `679b6bf`; no orphan arc-build branches.

PLINY signoff live-verifies cleanup (arc-37/build local + remote deleted; worktree removed; PR merged; main fast-forwarded; paste archival per §5.11). Attestations cite live-verified state per §19.6. Source-ticket closures (A18) verified live before posting.

---

## Phase structure

**Phase 1 — Design (DAEDALUS + ARGUS).** DAEDALUS reads this directive + all 6 source tickets + the relevant substrate sections per the Read order. Produces design.md covering all 6 candidates — each as its own section with: exact wording for the canon, insertion locus, cite-comment plan, self-app probe (if any), N=1 framing. ARGUS cold-audits; expected NEEDS_REVISION on at least one candidate given the bundle size.

**Phase 2 — Build (ADA in `.claude/worktrees/arc-37-build/`).** ADA implements all 6 candidates per approved design.md. ADA's commits carry Co-Authored-By trailers per §28. Coordinated commits per candidate OR single coherent commit — ADA picks based on diff coherence; documents rationale in PR description.

**Phase 3 — Verify (VERA + CATO + ZENO).** VERA exercises probes from design.md (one per candidate at minimum). CATO cold-reads diff for craft + scope + wording. ZENO mechanical spec-vs-result check. **CATO is MANDATORY** for this arc (substrate canon work + new skill + multiple new sections; wording precision matters).

**Phase 4 — Ship + close.** Smoke + PR + merge + cleanup + close. PLINY signoff per §5.10. Close all 6 source tickets per A18 with cross-refs + audit comments. Tag `[for: user-tier-polybius]` per A18.

---

## Read order for DAEDALUS

1. This directive (load-bearing spec for all 6 candidates).
2. `bw show stoa--86k` (C1 source).
3. `bw show stoa--kt6` (C2 source).
4. `bw show stoa--wad` (C3 source).
5. `bw show stoa--ntn` (C4 source).
6. `bw show stoa--53u` (C5 source).
7. `bw show stoa--7e3` (C6 source) + `_drafts/skill_handoff_author.md` (draft input for C6).
8. `HUMAN_paste-polybius-arc-37-instruction.md` — POLYBIUS's activation paste; same content frame.
9. `substrate/MAJOR_POLYBIUS.md` — C1 + C3 + C4 + C6 touch-points (§16 lifecycle; §18 housekeeping; §5.1.1.1 cross-project sequencing).
10. `substrate/MAJOR_PLINY.md` — C4 + C5 + C6 touch-points (§5.10 signoff; §5.12 seat-identity-in-dispatch-brief; §6.2 surface-and-wait; §7 verify-then-execute).
11. `substrate/operating-disciplines.md` — primary surface:
    - §7.4 + §7.5 cross-tier conventions (C2 cite)
    - §10 + §11 HITL/Autonomous + autonomous-mode-setup (C4 extension surface)
    - §17 + §23 base-vs-custom (C1 cite)
    - §19.6 attestation-confabulation (C5 sister)
    - §23 base-vs-custom (C1 cite)
    - §28 Co-Authored-By trailer (Arc 35 canon; ADA commits apply)
12. `substrate/install.sh` — C6 SKILL_NAMES addition surface.
13. `substrate/skills/check-bw-release/` + `substrate/skills/inspect-script-output/` — precedents for substrate skill shape; C6 follows pattern.
14. `the-stoa/SPECIFICATION.md` §10.1 + §4.5 + §13 — generational lineage architecture (C3 + C6 cite); workplan context.

---

## DAEDALUS sub-decisions summary

- A8 (C1 section number) — user-tier leans new MAJOR_POLYBIUS.md §19
- A9 (C2 section number) — user-tier leans operating-disciplines.md §29
- A10 (C3 section number) — user-tier leans separate operating-disciplines.md §30
- A11 (C4 placement) — user-tier leans extensions inside existing §10 + §11
- A12 (C5 subsection number) — user-tier leans operating-disciplines.md §19.7
- A13 (C6 skill scope — fold session-id record into SKILL.md OR defer) — user-tier leans fold

If any pick exceeds DAEDALUS discretion, treat as PRINCIPAL-gate per §25.
