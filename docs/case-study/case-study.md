# A recursive three-role agent architecture — for the beadworks team

**Audience:** the beadworks (`bw`) team — peers who already think in message-bus + multi-actor terms.
**Author:** Denson Smith.
**Date:** 2026-05-02.
**Status:** draft for review; will become an in-app view in The Stoa once visual treatment lands.

This is a working notebook offered for review, not a sales pitch and not a tutorial. We've spent ~36 hours building something architecturally novel on top of bw, and we'd like to compare notes with the people who built bw. What follows is what we built, why we made each choice, and what we'd like to discuss with you.

---

## 1. What this is and why we're showing it to you

We've built a **recursive three-role agent architecture** that uses bw as its durable substrate. The architecture has three seats — POLYBIUS (chief-of-staff), PLINY (orchestrator), and a team of CAPTAINs (specialized sub-agents) — repeated at every tier (user → project → sub-project), with bw as the message bus that ties everything together.

The work is at a clean rest point: 15 arcs shipped, full v2 architecture deployable, two new disciplines just propagated from personal habit into substrate. Rather than improving further before others see it, we want to surface it for engagement.

Three things we want from you:

1. **Tell us where bw is being used in ways our architecture would benefit from knowing about.** We're using a small subset of bw's capabilities; you've seen the breadth.
2. **Push back on architectural choices.** The list of disciplines below is empirical — observed over ~36 hours of live work. Some may not generalize; we'd rather find that out from you than from a future arc.
3. **Fork what's useful.** The substrate is meant to be deployed. If a piece of this would help a different multi-actor system you're working on, we want to know what made it portable (or not).

The whole architecture is in the [the-stoa](https://github.com/denson/the-stoa) repo. The substrate that gets deployed is at `the-stoa/substrate/`. The Stoa app (which renders the team and, soon, this case study) is at `the-stoa/app/`.

---

## 2. The architecture in one diagram

(Embed: information-flow knowledge graph, "Static explore" mode by default. See `docs/case-study/kg-spec.md` for the full spec.)

The diagram is interactive. Hover for tooltips, click for detail, and switch modes (Static explore / Information-flow / Recursion / Tour) using the controls. If you want a guided tour, **POLYBIUS can walk you through it** — see §12.

The diagram is **not a DAG.** The system has cycles, decision points, and feedback loops. PLINY is a decision node; verdicts loop back when ARGUS / VERA / CATO surface defects; CAPTAIN_ZENO (the embedded spec-checker) can trigger spec-drift loops; CAPTAINs can escalate up the chain to POLYBIUS and (when needed) to PRINCIPAL.

---

## 3. Why three roles, not one

We started with one role — a single seat trying to be CoS, orchestrator, and pipeline-runner all at once. It collapsed reliably. The empirical signal: merged seats drop jobs.

The runtime constraint that drove the split: **Claude Code's `Agent` tool does not propagate to sub-agents.** Only top-level sessions can dispatch. The dispatcher therefore has to live at the top-level session tier — it's a structural fact, not a design choice.

That gives us three load-bearing seats:

| seat | rank | one job | lives at |
|---|---|---|---|
| **POLYBIUS** (chief-of-staff) | MAJOR | converse with the human; hold durable memory; write directives; manage onboarding + recovery | top-level Claude Code session |
| **PLINY** (orchestrator) | MAJOR | run pipelines; dispatch CAPTAINs; reconcile verdicts; ship | top-level Claude Code session |
| **CAPTAINs** (specialized sub-agents) | CAPTAIN | one focused job each (architect, plan-critic, executor, verifier, reviewer, scout, file-clerk, intake, synthesist, spec-checker) | `.claude/agents/CAPTAIN_*.md` envelopes, dispatched by PLINY |

POLYBIUS and PLINY are both MAJOR rank — peers, not hierarchical. They communicate via bw (primary) and human-relay (fallback). One is the human-facing seat, one is the team-facing seat. **Different roles get different files, different sessions, different contexts.** The discipline is called *one job per agent* (ticket `u--7yg.17` if you want the empirical trail).

CAPTAIN_ZENO (the embedded spec-checker, deep in the pipeline at final gate) is its own seat for the same one-job-per-agent reason — different from MAJOR_PLINY's job (which is dispatching the team), different from VERA's job (which is verifying against design probes), specifically the *mechanical spec-vs-result drift check* before ship. (Historical note: this seat shared MAJOR_PLINY's mnemonic in early versions of the spec; the role-collapse trap was real enough that we renamed it structurally to CAPTAIN_ZENO. Two seats sharing a mnemonic produced reliable confusion even when the role files explicitly disambiguated them — voice discipline applied to naming, per §5.)

---

## 3.5 How trust distributes across the three roles

The three-role split creates three distinct trust patterns between the human and the agent team. Each pattern is appropriate for a different work shape; the architecture's value comes from being able to fluidly switch between them. Naming the patterns explicitly:

### Pattern 1 — HUMAN ↔ POLYBIUS (the persistent-memory channel)

**Paramount.** This is the channel the entire architecture is built around. POLYBIUS holds durable memory across sessions; conversations with POLYBIUS *compound* rather than reset. New context, recurring discussions, decision-rationale tracking, the entire compaction-recovery story, and the directive-authoring work all live here. If you remove this channel, you remove what makes POLYBIUS valuable as a CoS — the rest of the architecture would still work, but every session would start from cold.

The bw substrate (§7) is what makes this real — POLYBIUS reads bw at activation, writes to bw as work progresses, and reads it again after compaction. The persistent-memory claim is empirical: across the v2 sequence, three handoff tickets carried state across `/compact` boundaries cleanly.

### Pattern 2 — HUMAN ↔ PLINY (direct relay, fallback)

The human can talk to PLINY directly when the work calls for it — usually as the *fallback* when bw isn't viable for a specific item, or when the orchestrator needs urgent direction without a POLYBIUS round-trip.

The substrate's framing: this pattern is rare by design. `MAJOR_PLINY.md` §3 explicitly says PLINY does not converse with the PRINCIPAL directly except through the paste-instruction POLYBIUS authored. Direct PRINCIPAL-PLINY conversation typically signals a routing problem (POLYBIUS should be the relay), not a desired pattern. But the channel exists because the fallback is sometimes the right call — bw isn't initialized yet, or POLYBIUS is paused, or the PRINCIPAL needs to be in the loop with the build session immediately.

### Pattern 3 — HUMAN ↔ POLYBIUS ↔ PLINY (the preferred load distribution)

The mode the architecture is optimized for. PRINCIPAL converses with POLYBIUS at the strategic level; **POLYBIUS does the validation, guidance, and directive-authoring work for the team**; PLINY runs the team and dispatches CAPTAINs. PRINCIPAL is in the loop for direction, not for routing.

This is the pattern that makes POLYBIUS valuable as a seat distinct from PLINY. If POLYBIUS were just a conversational front-end that relayed to PLINY without doing validation/guidance work, the human could talk to PLINY directly and the CoS seat would be redundant. POLYBIUS is valuable because the persistent-memory + validation + guidance work *belongs in a different context* than the team-dispatch + pipeline-execution work.

The discipline this pattern relies on is *Principal-as-router antipattern* (`u--7yg.1`, §8): POLYBIUS surfaces only project-direction calls and final ship/no-ship to PRINCIPAL — not technical-tier decisions. That's what keeps PRINCIPAL in the strategic seat rather than becoming a routing layer.

### Switching between patterns

A given engagement uses all three at different moments:
- Routine arc work: Pattern 3 (POLYBIUS authors directive, PLINY executes, ships autonomously on clean PASS)
- New project / strategic shift: Pattern 1 (PRINCIPAL has a long conversation with POLYBIUS to establish context)
- Emergency / urgent build-session intervention: Pattern 2 (PRINCIPAL pings PLINY directly)

The substrate doesn't enforce which pattern is active at any moment — that's PRINCIPAL's call. What the substrate does is make all three available, with the role files clear about which is preferred for which work shape.

---

## 4. Why recursion

The same three-role pattern appears at every tier:

```
USER-TIER
  ├── MAJOR_POLYBIUS   (CoS at user-level)
  ├── MAJOR_PLINY      (orchestrator at user-level)
  └── User-level Team  (~/.claude/agents/CAPTAIN_*.md)
       │
       │ creates / coordinates with
       │
       └── PROJECT-TIER (one per project)
              ├── MAJOR_POLYBIUS_<project>
              ├── MAJOR_PLINY_<project>
              └── Project Team (<project>/.claude/agents/CAPTAIN_*_<project>.md)
                   │
                   │ when work needs specialization (own tools / domain / collaborator)
                   │
                   └── SUB-PROJECT-TIER
                          ├── MAJOR_POLYBIUS_<subproject>
                          ├── MAJOR_PLINY_<subproject>
                          └── Sub-project Team
                                │
                                └── ... (recursively, when needed)
```

Self-similar across scales. The recursion is *the* architectural commitment — it's what makes the system extend cleanly without architectural bifurcation.

Sub-projects share their parent's git repo and bw. Disambiguation is by name suffix: `CAPTAIN_DAEDALUS_<subproject>` lives alongside `CAPTAIN_DAEDALUS_<project>` in the same `.claude/agents/` namespace, separated by suffix. (Implementation lands in Arc 14: a new `install.sh --target subproject` mode that takes a parent path + a slug and deploys the recursive instance under `<parent>/<subproject>/`.)

The asymmetric visibility (§7) is what makes recursion *useful* rather than just symmetric replication: higher-tier POLYBIUS sees down into lower tiers; lower-tier doesn't see up. That makes cross-project memory + routing live at user-tier without leaking into project-tier work.

---

## 5. Why voice discipline is structural

This was the most surprising load-bearing finding from the build sequence.

The v1 architecture used "Colonel" to mean the human served by the system. Pre-claimed a title for what should be a future high-autonomy agent rank, AND conflated humans with agents. We tried to fix it with a `sed -i 's/Colonel/PRINCIPAL/g'` sweep. Didn't work.

The empirical signal: a CoS-style agent (POLYBIUS_agent_character_builder) operating from v1's role files kept calling the human "Colonel" *while documenting* the leakage of "Colonel" terminology. The role file's voice was structurally shaping how the agent thought about its own seat — beyond just literal token use, into the framing of relationships, decisions, and metaphors.

The fix that actually worked was **re-authoring the role files from a v2 voice grounded in PRINCIPAL/HUMAN throughout**, rather than find-replacing the surface tokens. v2 reframes the human as PRINCIPAL (descriptive role) at HUMAN (rank), reserves COLONEL for a future agent rank, and re-articulates every discipline in the new vocabulary.

The v2 spec captures this as "**role-file voice is structural, not decorative**." The vocabulary an agent's role file uses determines how the agent reaches reflexively for its seat. v1 tried to bolt PRINCIPAL on top of Colonel-shaped framing; v2 re-grounded everything in the new vocabulary from the start.

This is the load-bearing observation we'd most want pushback on. Has bw been used in contexts where role-file vocabulary surfaced as a structural factor in agent behavior? If so, how was it surfaced, and what was the corrective discipline?

---

## 6. Information flow with cycles

Walk the gauntlet pipeline with PLINY's decision points visible:

```
PRINCIPAL  ↔  POLYBIUS  →  PLINY  →  DAEDALUS (architect)
                                       │
                                       ▼
                                       ARGUS (plan-critic) → verdict to PLINY
                                                              │
                                                  ┌───────────┴───────────┐
                                                  │                       │
                                            risk ↓                  clean ↓
                                       loop back to DAEDALUS    forward to ADA
                                                                       │
                                                                       ▼
                                                                       ADA (executor) — builds
                                                                       │
                                                                       ▼
                                                                       VERA (verifier) → verdict to PLINY
                                                                                          │
                                                                              ┌───────────┴───────────┐
                                                                              │                       │
                                                                         fail ↓                  pass ↓
                                                                  loop back to ADA          forward to CATO
                                                                                                   │
                                                                                                   ▼
                                                                                                   CATO (reviewer) → verdict to PLINY
                                                                                                                      │
                                                                                                          ┌───────────┴───────────┐
                                                                                                          │                       │
                                                                                                  needs-rev ↓                pass ↓
                                                                                                  loop back to ADA      autonomous ship (per `u--7yg.11`)
```

PLINY is a decision node, not a pass-through. Every verdict triggers a decision: forward, loop back, or escalate. Every CAPTAIN can also escalate to POLYBIUS via bw if the question exceeds the gauntlet's scope; POLYBIUS in turn surfaces to PRINCIPAL only on project-direction calls (the *Principal-as-router antipattern* check applies — `u--7yg.1` — surfacing every technical-tier call to the human is a routing antipattern, not a discipline).

The **autonomous-ship-on-clean-PASS** discipline (`u--7yg.11`) is what makes this efficient — when the gauntlet returns clean PASS and no override flags apply, PLINY commits / closes bw / pushes without gating on PRINCIPAL approval. Routing every clean ship through human approval is the antipattern in execution form. Roughly half the round-trips in the recent arc sequence were saved by this discipline.

---

## 6.5 Two operational modes — formal gauntlet vs. pair-programming for prototyping

The information flow above (§6) describes the **formal gauntlet** — the production pipeline that takes a directive and ships hardened artifacts. It's rigorous, structured, and (intentionally) not the fastest way to produce something. The architecture also supports a **second operational mode** that we discovered empirically and that turned out to be load-bearing for moving fast.

### Mode 1 — Formal gauntlet (production pipeline)

What §6 describes. POLYBIUS authors a directive; PLINY runs DAEDALUS → ARGUS → ADA → VERA → CATO → CAPTAIN_ZENO with verdict-based loop-backs at each gate; clean PASS ships autonomously per `u--7yg.11`. The output is a **shipped artifact** — code, docs, role files, install.sh updates, whatever the directive specified.

This is the right mode when you know roughly what you want and you need it built right. Most of the v2 sequence (Arcs 4-15) ran in this mode.

### Mode 2 — Pair-programming for prototyping (fast exploration)

The mode we use when *we don't yet know what we want* and the formal gauntlet would be premature. The cycle:

1. **POLYBIUS authors a specialized pair-programmer Major** for the task — Python work, design exploration, regulatory analysis, sketching out a new agentic team, prototyping a UI flow. (The pair-programmer-authoring capability is itself a POLYBIUS responsibility; see §3 and the substrate's pair-programmer template.)
2. **PRINCIPAL pairs with the new agent** in a fresh Claude Code session — direct dialog, fast iteration, exploratory.
3. **POLYBIUS stays in the loop** — providing memory across the pairing session, helping when the pair-programmer needs context the PRINCIPAL doesn't have at hand, surfacing patterns from prior work that inform the prototype.
4. **Output: a rough prototype** — a working sketch, a proof-of-concept, a draft set of agents, a sample design. Not production-ready, but enough to *see what we're after.*
5. **POLYBIUS authors a directive** for PLINY based on the prototype — what's worth keeping, what needs rebuilding rigorously, what the success criteria are, what to harden against.
6. **PLINY runs the formal gauntlet on the prototype** — the gauntlet team debugs, iterates, and hardens what the prototyping session produced, applying full rigor (verification, review, spec-checking) where it was deliberately skipped during exploration.
7. **Shipped artifact** — same end-state as Mode 1, but reached via a meaningfully different path.

**The empirical claim:** we started moving much faster when we empowered POLYBIUS to quickly create specialized pair-programmers for prototyping work, with the formal gauntlet kicking in afterward to harden what the prototyping produced. The two modes together cover more of the speed-vs-rigor space than either alone — Mode 2 is fast and exploratory; Mode 1 is rigorous and shipped; the handoff between them is where the architecture's value compounds.

### When to use which mode

| trigger | mode | why |
|---|---|---|
| Brand-new shape; "I don't know what I want yet" | Mode 2 (prototyping) | gauntlet would build the wrong thing rigorously |
| Established shape; well-scoped change | Mode 1 (formal gauntlet) | rigor + autonomous-ship is the value |
| Exploration produced a prototype worth keeping | Mode 2 → Mode 1 handoff | hardening is the gauntlet's strength |
| Production work that just needs faster iteration | Mode 1 (small-chunk discipline) | not Mode 2 — discipline solves this without giving up rigor |

POLYBIUS knows both modes and helps PRINCIPAL choose at the start of each engagement. The case-study substrate captures the prototyping methodology as a procedure POLYBIUS follows (parallel to onboarding and sub-project spawning) — see the substrate's `MAJOR_POLYBIUS.md` §12.

---

## 7. Beadwork as durable substrate

bw is the durable substrate. Every meaningful event — directive, verdict, surface-back, hand-off, ship — leaves a bw breadcrumb. Three things this gives us:

**1. Cross-session continuity.** Sessions compact. Sessions clear. Sessions get killed by network blips. bw persists. The next-session-cold-reader pattern (your README) is exactly what compacted handoffs need: a ticket description that carries the substantive content, with the title as summary. Three handoff tickets carried our work across compactions during the v2 sequence; each one acted as the durable read-in for the resumed session.

**2. Asymmetric visibility (recursive).** User-tier POLYBIUS reads project-tier bws freely; project-tier POLYBIUS doesn't read user-tier by default. The same pattern between project-tier and sub-project-tier. This is what makes cross-project memory + routing live at user-tier without polluting project-tier work. The asymmetry is *load-bearing* — it's not "we forgot to wire it up both ways."

**3. Discipline accretion.** Every empirical observation ("this thing happened, here's what we learned") becomes a `u--7yg` child. The `u--7yg` epic now has 22 children, each a discipline or observation. This is the project's design provenance — the *why behind every why*. The retrospective at `user-beadwork/retrospectives/v2-arcs-1-14.md` is built directly on top of this trail.

Where we'd want your perspective: **the asymmetric-visibility model.** We chose it on theoretical grounds (cross-project memory belongs at user-tier; project-tier work shouldn't see across projects); it's empirically held but lightly tested. If bw users have hit cases where symmetric visibility was needed, or where the asymmetry was the wrong default, we'd want to know.

---

## 8. Disciplines

The 22 `u--7yg` children. Each captures an empirical observation that produced a discipline. We won't list all 22 here — they're in user-beadwork; the [retrospective](https://github.com/denson/user-beadwork/blob/main/retrospectives/v2-arcs-1-14.md) walks them as a synthesis.

The high-leverage ones, briefly:

- **`u--7yg.1` Principal-as-router antipattern** — never surface technical-tier calls to the human. Every routed-up call costs round-trip; the human is a strategic seat, not a routing layer.
- **`u--7yg.10` / `u--7yg.18` Verify-then-execute** — when a directive contradicts the spec it cites, or when a PRINCIPAL statement contradicts visible state, *verify before barreling forward*. Caught real directive-author errors during the arc sequence.
- **`u--7yg.11` Autonomous-ship on clean PASS** — clean verdicts → autonomous commit/close/push. Don't gate on PRINCIPAL for ships that earned themselves.
- **`u--7yg.12` Sub-agents cannot dispatch** — runtime constraint; the architectural shape inherits from this. Any architecture that puts dispatch at sub-agent tier is structurally impossible.
- **`u--7yg.15` Wait-for-quiescence** — surface real ambiguity instead of barreling forward. Cost of round-trip is one comment; cost of building the wrong thing is the rebuild.
- **`u--7yg.17` One job per agent** — merged seats reliably drop jobs. CoS / orchestrator / specialists each get their own seat.
- **`u--7yg.20` Voice discipline** — role-file voice is structural; the v1→v2 redesign was the receipt for not having this discipline at v1.

Two disciplines we just propagated from PRINCIPAL-personal-setup into the substrate (Arc 15):

- **Fix-now** — small bugs ship now, not "next sprint." The cost calculus has inverted; agent tokens are cheap and deferred fixes compound on permission, not interest. (Demonstrated under live test by `stoa--8o4` shipping same-day rather than scheduled for ~1 week.)
- **External directive review for multi-concern arcs** — when a directive covers more than one deliverable concern, route it through an external reviewer (a cold Claude session, or an external model like Codex / Gemini) before dispatching the build session. (Demonstrated by Mega-Arc-9: external review caught CI/CD git-ignore paradox, parsing ambiguity, env-var-prefix bug, and MAY-vs-MUST phasing weakness; the split into Arcs 9-13 came directly from that review.)

---

## 9. Worked example — Arc 14, sub-project spawning

A real arc, walked end-to-end, to make the abstract concrete.

**Context:** by Arc 14, the substrate is fully v2-voiced and The Stoa app (the visualization for the agent roster) is rebuilt. The v2 spec describes sub-project spawning as a load-bearing capability since v1, but it's never been *implemented as a deployable*. Arc 14 closes that loop.

**Directive authoring (POLYBIUS → PLINY).** I, working as PRINCIPAL, ask user-tier POLYBIUS to author the directive. POLYBIUS proposes the shape, surfaces a Phase A *Colonel call* (sub-project naming/location decision; three options; recommended leaning), and asks for confirmation before locking in. I confirm the leaning ((a) subdirectory of parent), and POLYBIUS files the directive at `the-stoa/substrate/arcs/arc-14-build-directive.md`, commits, pushes.

**Build session activation.** I open a fresh Claude Code session in `~/claude_projects/the-stoa/` and paste:

> *You are MAJOR_PLINY for the the-stoa Arc 14 engagement. Read substrate/MAJOR_PLINY.md and assume the orchestrator role. Then read substrate/arcs/arc-14-build-directive.md and execute.*

The session reads the role file, the directive, files an epic in bw (`stoa--vgn`), and surfaces the Phase A call back to me — verifying that (a) is the right choice given what the install.sh code actually looks like. I confirm; build proceeds.

**Build phases B–E.** PLINY (the build session) extends `install.sh` with the new `--target subproject` mode (with slug validation, idempotency, dry-run, conflict-flag rejection, sub-project-specific next-step guidance). Adds a §10 to `MAJOR_POLYBIUS.md` covering sub-project spawning (trigger recognition, walk-through, asymmetric visibility recursive, hand-off pattern). Adds Scenario 5 to `ONBOARDING.md` (design-tier sub-project under The Stoa with a designer named Reese in the human-loop seat). Updates two templates.

**Smoke test.** PLINY runs install.sh against a synthetic parent with git + bw + parent-tier substrate. Verifies: install clean, suffixed files at expected paths, dry-run works, parent CLAUDE.md sha256 unchanged, parent `.claude/MAJOR_*.md` untouched, bw NOT re-initialized, sub-project's bw list byte-identical to parent's, no templates dir under sub-project, validation rejects bad slugs / conflict flags / missing required flags.

**Surfaced bug.** Build session notices `install.sh --target project --project-dir .` produces slug `_` because `basename "."` returns `.`. Build session offers to schedule the fix for ~1 week.

**Fix-now discipline overrides the deferral.** Per the discipline (which would later be propagated into the substrate as Arc 15's §4.8): small bugs ship now. The fix is one line — resolve to absolute path before basename. Build session applies, smoke-tests, ships as commit `2dee8a0`, closes ticket `stoa--8o4`. Same day as Arc 14 itself.

**Hand-back.** PLINY surfaces back: "Arc 14 shipped at commit `3324c14`, pushed to origin/main, epic `stoa--vgn` closed."

**Total elapsed:** roughly two hours of clock time. Two commits (Arc 14 + slug fix). One Phase A surface to me. Otherwise autonomous.

The arc demonstrates: directive authoring with surface-early discipline; build session as MAJOR_PLINY-for-the-engagement; HITL Phase A; fix-now under empirical test; autonomous-ship on clean PASS. All in one cycle.

---

## 10. Where this is going — the hypergraph and the agentic team that builds it

The next architectural arc (probably Arc 16 or beyond) is a **hypergraph** of code + bw tickets + repo content.

**Why a hypergraph and not just a graph.** The information-flow KG in §2 uses binary edges (one channel, two participants). That's right for the architecture — channels do connect two seats. But for the *content* of the system — a bw ticket linking simultaneously to multiple commits, multiple files, multiple disciplines, multiple defect classes — binary edges flatten what's inherently multi-way. Hypergraphs allow hyperedges that connect arbitrary numbers of nodes; they're a better fit for the content shape.

**The agentic team that builds it.** Per the recursive architecture (§4), the natural shape is a **sub-project** under The Stoa with its own POLYBIUS / PLINY / Team — a hypergraph-tier sub-project. Specialization signals fire on at least two of the three sub-project trip-wires:

- **Own tools** — graph databases (Neo4j? Memgraph? a custom store?), embeddings, traversal queries, hypergraph-rendering libraries
- **Own domain** — knowledge-graph engineering vs application-code engineering
- **Possibly own collaborator** — a knowledge engineer would be the natural human-loop seat; the engineering-tier PRINCIPAL is wrong for the role

The sub-project spawns following the §10 procedure in `MAJOR_POLYBIUS.md` (which Arc 14 added). Same install pattern — `install.sh --target subproject --parent-dir <stoa> --subproject hypergraph-tier`. New CAPTAINs (suffixed `_hypergraph_tier`); shared bw with parent.

**Wireframe of the visualization.** (Placeholder — Claude Design pass to fill in.)

The hypergraph view, when it ships, becomes a **second visualization mode** in The Stoa app, alongside the binary-edge information-flow KG from §2. The two modes coexist; viewers can toggle between them depending on whether they care about the architecture's communication shape (KG) or the content's relationship shape (hypergraph).

What we'd want to discuss with you on this front: the bw side specifically. The hypergraph would be reading bw tickets at scale — what's the right access pattern? Is there a bulk-export shape that would let an external graph-builder ingest the data efficiently, or is per-ticket querying the expected pattern? Are there bw conventions for cross-ticket relationships (parent/child epics, "blocks" / "blocked by" / "duplicates") that would map naturally to hyperedges?

---

## 11. Open questions and what we'd want to discuss

In rough priority order:

1. **Asymmetric visibility model (§7).** Does it generalize? Where does symmetric visibility actually need to win?
2. **The voice-discipline-is-structural finding (§5).** Has bw use surfaced this in other multi-actor systems? What corrective disciplines have been observed?
3. **The `u--7yg` discipline-accretion pattern (§8).** Are there bw conventions for capturing empirical disciplines that we should adopt? Cross-discipline links? Standardized titles?
4. **Hypergraph integration (§10).** What's the right access pattern for an external graph-builder reading bw at scale?
5. **The recursive substrate (§4).** Is "share parent's repo + bw, disambiguate by suffix" the right operational shape for sub-projects? Are there bw constructs (sub-prefixes? namespaces? worktree-aware tickets?) that would make this cleaner?
6. **Compact-or-clear recovery.** POLYBIUS notices when PLINY drops role and re-issues paste-instruction (load-bearing CoS responsibility). Is there a bw integration that would make this less manual?

---

## 12. How to engage

**Repos:**
- [the-stoa](https://github.com/denson/the-stoa) — the unified repo (substrate + app)
- [user-beadwork](https://github.com/denson/user-beadwork) — the architecture spec, retrospectives, the 22-child `u--7yg` empirical record

**Try the substrate:**

```bash
git clone https://github.com/denson/the-stoa.git
cd the-stoa
./substrate/install.sh --target project --project-dir <your-project>
```

(Or `--target user` for user-tier; or `--target subproject` for the recursive case from Arc 14. See `substrate/install.sh --help`.)

**Take the tour with POLYBIUS** (the meta-strong way):

If you're set up with Claude Code locally:

1. Open The Stoa app in a Chrome tab (the Stoa hosts itself; or run `cd the-stoa/app && npm run dev`)
2. Open a fresh Claude Code session in `~/claude_projects/the-stoa/`
3. Paste:
   > *POLYBIUS, please walk me through The Stoa using the Chrome MCP. Use the tour script at `templates/tour-script.md`. Pause for my questions at the marked beats.*
4. POLYBIUS will drive your browser through the case study, demonstrate the KG, walk a worked example, and answer questions live

This is the load-bearing demonstration: *the system explains itself by using itself.* If POLYBIUS can give you a coherent tour of a recursive multi-actor agent architecture, that's the strongest evidence the architecture works.

**Open issues / contribute / fork:**
- Cross-repo issues (substrate + app) live in `the-stoa` bw with prefix `stoa--`
- Architecture-level discussions live in `user-beadwork` with prefix `u--`
- Forks welcome — the substrate is meant to be deployed; the install.sh is the entry point

**Direct contact:** Denson Smith. (Or wave at POLYBIUS; POLYBIUS knows where to find me.)

---

*This case study is a living document. As the architecture evolves and as we hear back from you, it will update. The version you're reading is anchored to the v2 fully-landed state at the-stoa commit `f6c45a5` and user-beadwork commit `42fb253`.*
