# Information-flow knowledge graph — spec

**Purpose:** the visual + interactive representation of how information flows through the three-role recursive agent architecture. Feeds two consumers:

1. **Claude Design** — for the visual prototype pass (interactive web component, styled to The Stoa design system)
2. **Claude Code** — for production implementation as a React component in The Stoa app (`/#/architecture`)

**Architecture authority:** `user-beadwork/plans/three-role-recursive-architecture.md` (v2). This spec describes the *graph shape* of the architecture; the spec describes *the architecture itself*.

**This is NOT a DAG.** The system has cycles, decision points, and feedback loops. Any rendering that flattens it into a forward-only sequence loses the load-bearing parts.

---

## 1. Nodes

Three categories: humans, agents, infrastructure.

### 1.1 Humans

| id | rank | descriptive_role | visual_treatment_hint |
|---|---|---|---|
| `human_principal` | HUMAN | PRINCIPAL | distinctive — the only HUMAN-rank node; sits at the top; differentiates visually from agents (different shape, different surface treatment) |

### 1.2 MAJORs

| id | rank | descriptive_role | mnemonic | visual_treatment_hint |
|---|---|---|---|---|
| `major_polybius` | MAJOR | CHIEF-OF-STAFF | POLYBIUS | sits between HUMAN and the rest of the team; the conversational-with-PRINCIPAL seat |
| `major_pliny` | MAJOR | ORCHESTRATOR | PLINY | the dispatch hub; visually central among the CAPTAINs; the decision-point node |

### 1.3 CAPTAINs

| id | rank | descriptive_role | mnemonic | tools_constraint |
|---|---|---|---|---|
| `captain_daedalus` | CAPTAIN | ARCHITECT | DAEDALUS | (full toolkit) |
| `captain_argus` | CAPTAIN | PLAN-CRITIC | ARGUS | **no Write/Edit** (structural — surfaces risks but cannot fix) |
| `captain_ada` | CAPTAIN | EXECUTOR | ADA | (full toolkit) |
| `captain_vera` | CAPTAIN | VERIFIER | VERA | (full toolkit) |
| `captain_cato` | CAPTAIN | REVIEWER | CATO | **no Write/Edit** (structural — reviews but does not modify) |
| `captain_strabo` | CAPTAIN | SCOUT | STRABO | external/web research |
| `captain_bartleby` | CAPTAIN | FILE-CLERK | BARTLEBY | **no WebSearch/WebFetch** (structural — internal repo recon only) |
| `captain_herald` | CAPTAIN | INTAKE | HERALD | brief drafting; no WebSearch/WebFetch |
| `captain_curator` | CAPTAIN | SYNTHESIST | CURATOR | cross-ticket synthesis |
| `captain_zeno` | CAPTAIN | SPEC-CHECKER | ZENO | **no Write/Edit, no WebSearch/WebFetch** (structural) |

**Visual treatment hint for CAPTAINs:** arranged around MAJOR_PLINY (the dispatch hub). Tool-constraint annotations should be visible (a "no edit" badge or similar) — it's a load-bearing structural choice that ARGUS and CATO physically cannot fix what they review.

### 1.4 LIEUTENANTs (skills)

Skills are reusable across ranks; they're not seats. Represent as a single category-node with a count, OR as a few representative leaf-nodes off whatever CAPTAIN invokes them.

| id | name | category |
|---|---|---|
| `lieutenant_runner` | RUNNER | tool-mediated probe execution |
| `lieutenant_format_validate` | FORMAT_VALIDATE | structured-artifact schema check |
| `lieutenant_pulse_review` | PULSE_REVIEW | empirical-record aggregation |
| `lieutenant_cite_check` | CITE_CHECK | citation validity |
| `lieutenant_dispatch` | dispatch-lieutenant | helper-dispatch from another CAPTAIN |
| `lieutenant_arc_management` | arc-management | arc lifecycle helpers |

(Visualize collapsed into a single LIEUTENANTs node by default; expand on click.)

### 1.5 Infrastructure

| id | name | role |
|---|---|---|
| `beadwork` | BEADWORK | durable substrate; the message bus + memory; everyone reads/writes |
| `artifacts` | ARTIFACTS | the things being built (code, docs, role files, etc.); produced by ADA, reviewed by VERA/CATO |

**Visual treatment hint for BEADWORK:** sits as a substrate at the bottom of the frame — every agent has a thin connecting edge down to it. As actions happen during animation, pulses run down those edges into BEADWORK, which visibly *accumulates*. This is the "durable memory" claim made visual.

---

## 2. Edge types (channels)

Each channel has: id, name, direction, durability, sync/async, visual treatment.

| id | name | direction | durability | sync | visual_treatment_hint |
|---|---|---|---|---|---|
| `direct_dialog` | direct dialog | bidirectional | session-only | sync | thick, conversational; pulses both directions; the only human ↔ agent channel |
| `paste_instruction` | paste-instruction handoff | one-way (POLYBIUS → PLINY) | on disk (the artifact at `HUMAN_paste-orchestrator-instruction.md`) | async | distinctive — represents activation, not message-passing |
| `agent_dispatch` | Agent-tool dispatch | one-way (PLINY → CAPTAIN) | one-shot | sync (within the dispatch turn) | brief packet flowing forward |
| `captain_verdict` | verdict return | one-way (CAPTAIN → PLINY) | one-shot | sync | verdict packet flowing back; arrives at PLINY's decision point |
| `skill_invocation` | skill invocation | bidirectional (CAPTAIN ↔ LIEUTENANT) | one-shot | sync | helper call; thinner than dispatch |
| `beadwork_write` | beadwork write | one-way (any → BEADWORK) | durable | async | pulse down to BEADWORK; substrate visibly accumulates |
| `beadwork_read` | beadwork read | one-way (any ← BEADWORK) | durable | async | pulse up from BEADWORK |
| `cross_tier_handoff` | cross-tier coordination | bidirectional (POLYBIUS_a ↔ POLYBIUS_b) | beadwork-mediated | async | only at tier-boundaries; visible on recursion view |
| `escalation` | scope escalation | one-way (CAPTAIN → POLYBIUS) | beadwork-mediated | async | upward-routing edge when work exceeds gauntlet scope |
| `principal_surface` | surface to PRINCIPAL | one-way (POLYBIUS → PRINCIPAL) | conversation | sync | becomes a `direct_dialog` exchange when fired; visualize as the trigger that starts a conversation |
| `artifact_write` | artifact write | one-way (ADA → ARTIFACTS) | durable | async | side-effect pulse |
| `artifact_read` | artifact read | one-way (any ← ARTIFACTS) | durable | async | side-effect pulse |

---

## 3. Decision points and loops

This is what makes the graph cyclic. Each loop has a trigger (verdict shape), a decision node (PLINY for most, POLYBIUS for escalations), and possible outcomes.

### 3.1 ARGUS risk-back loop

```
DAEDALUS produces design → ARGUS audits → ARGUS returns risk verdict to PLINY
  PLINY decides:
    - clean ARGUS verdict → forward to ADA
    - ARGUS surfaces real risk → loop back to DAEDALUS for re-design
```

**Visual treatment hint:** dashed back-edge from PLINY → DAEDALUS, activated when ARGUS verdict carries risk. Pulse animation traces the loop.

### 3.2 VERA fail-back loop

```
ADA builds → VERA verifies → VERA returns verdict to PLINY
  PLINY decides:
    - VERA pass → forward to CATO
    - VERA fail → loop back to ADA for fix
```

### 3.3 CATO revision-back loop

```
VERA passes → CATO reviews diff → CATO returns verdict to PLINY
  PLINY decides:
    - CATO pass → ship (autonomous if clean PASS, per `u--7yg.11`)
    - CATO needs-revisions → loop back to ADA for revisions
```

### 3.4 CAPTAIN_ZENO spec-drift loop

```
At final gate before ship → CAPTAIN_ZENO runs mechanical spec-vs-result check
  CAPTAIN_ZENO returns verdict to MAJOR_PLINY
    - clean → ship
    - drift → loop back to MAJOR_PLINY for re-dispatch (typically to ADA)
```

### 3.5 Escalation chain

```
CAPTAIN encounters out-of-scope question → escalation edge to MAJOR_POLYBIUS via beadwork
  MAJOR_POLYBIUS handles, OR
  MAJOR_POLYBIUS surfaces to PRINCIPAL via direct_dialog (project-direction call only — Principal-as-router antipattern check applies)
```

**Visual treatment for all loops:** distinctly colored back-edges (vs forward dispatch edges). Animation should make the loop *trip-wire moment* visible — the verdict arrives at PLINY, PLINY visibly decides, the back-edge activates if loop fires.

---

## 4. Recursion (multi-tier instances)

The same graph (sections 1-3) replicates at every tier. Three tiers are currently meaningful:

- **User-tier** — `~/.claude/` deploy; spans all of one PRINCIPAL's projects
- **Project-tier** — one per project; e.g., `~/claude_projects/the-stoa/.claude/`
- **Sub-project-tier** — one per sub-project; e.g., `<parent>/<subproject>/.claude/` (Arc 14 mechanism)

Cross-tier edges:

| from | to | edge_type | semantics |
|---|---|---|---|
| `major_polybius_user_tier` | `major_polybius_project_tier` | `cross_tier_handoff` | user-tier CoS coordinates with project-tier CoS |
| `major_polybius_project_tier` | `major_polybius_subproject_tier` | `cross_tier_handoff` | project CoS spawns / coordinates with sub-project CoS |

### 4.1 Asymmetric visibility

This is the load-bearing constraint that makes the recursion *useful* (not just symmetric):

- **Higher-tier POLYBIUS sees down** — user-tier POLYBIUS reads project-tier beadworks freely; project-tier POLYBIUS reads sub-project beadworks freely
- **Lower-tier POLYBIUS does NOT see up by default** — project-tier POLYBIUS does not read user-tier beadwork; sub-project POLYBIUS does not read parent-project beadwork
- **Exception:** when the lower-tier work is system-architecture-shaped (a meta-team arc), upper-tier beadwork is a valid input

**Visual treatment hint:** in the recursion view, render the visibility cone — higher-tier POLYBIUS has a downward "vision" indicator covering its sub-tiers; lower-tier POLYBIUSes don't have an upward one.

### 4.2 The fractal claim

The same graph shape appearing at every tier is *the* recursion point. A Claude Design pass should make this *seen*, not just diagrammed. Two strong patterns:

- **Zoom-out reveal** — start at one tier, camera pulls back, the same shape appears at the parent tier, pulls back again, the grandparent — fractal
- **Side-by-side stack** — render multiple tiers vertically; the cross-tier edges visibly connect the same node positions across tiers

The frontier-design hint from Claude Design's announcement (shaders / 3D) might serve this well — the recursion is the kind of thing that benefits from dynamic visualization rather than static diagram.

---

## 5. Visualization modes

The component should support multiple modes; the active mode changes what's rendered + animated:

| mode | what it shows | interactions |
|---|---|---|
| **Static explore** (default) | Single-tier view; all nodes + all edges visible; no animation | Hover for tooltip; click for detail; drag to rearrange (optional) |
| **Trust patterns** | Single-tier view; three load-bearing trust patterns highlightable individually or together; all other edges dimmed when a pattern is selected | Toggle Pattern 1 / 2 / 3 individually; show all simultaneously; hover for explanation of which work shape uses each pattern |
| **Information-flow** | Single-tier view; continuous animation showing a brief flowing through the gauntlet, verdicts returning, occasional loop-backs firing | Hover to pause; click to scrub timeline |
| **Recursion** | Multi-tier view (user / project / sub-project); the same shape replicated; cross-tier edges visible | Click a tier to zoom; toggle visibility cone |
| **Tour** | Driven by an external script (POLYBIUS narrating); camera moves + node highlights + sequential reveals controlled by tour beats | Read-only during tour; "play / pause / next" controls; the tour can also be scripted from `templates/tour-script.md` for the POLYBIUS-driven walkthrough |

The tour mode is the load-bearing one for the planned POLYBIUS-controlled walkthrough — POLYBIUS uses the Chrome MCP to drive the browser, navigating between modes and triggering specific node highlights as it narrates.

### 5.1 Trust patterns mode — the three load-bearing patterns

This mode exists because **the trust distribution between HUMAN, POLYBIUS, and PLINY is the architecture's value claim** (case study §3.5). The visualization needs to make these three patterns explicitly toggleable so a viewer can study each one in isolation:

| Pattern | Edges highlighted | What this shows |
|---|---|---|
| **Pattern 1 — HUMAN ↔ POLYBIUS** (paramount) | the `direct_dialog` edge between `human_principal` and `major_polybius` rendered thickest, possibly with a glow / annotation marking it "the persistent-memory channel" | the channel the architecture is built around — POLYBIUS holds durable memory; conversations compound rather than reset |
| **Pattern 2 — HUMAN ↔ PLINY** (fallback) | the direct edge between `human_principal` and `major_pliny` rendered as a fallback channel (different style — dashed, lighter); annotation: "fallback when bw isn't viable, or for urgent direct comms with the team" | the human-to-orchestrator direct path; rare by design but real |
| **Pattern 3 — HUMAN ↔ POLYBIUS ↔ PLINY** (preferred load distribution) | the path `human_principal` → `major_polybius` → `major_pliny` highlighted as a sequence; annotation: "PRINCIPAL strategic; POLYBIUS validates + guides + authors directives; PLINY runs the team" | the mode the architecture optimizes for |

A user toggling between the three patterns sees the architecture from three different angles — strategic (1), fallback (2), preferred-routine (3). All three patterns coexist; they're not alternatives. The user picks which to emphasize.

**Visual treatment hint for Pattern 1 specifically:** since this is the load-bearing channel, even in Static-explore mode the HUMAN ↔ POLYBIUS edge should be visually distinct (thicker stroke, possibly with a subtle pulse animation showing the durable nature). It's not just one edge among many — it's *the* edge that justifies the persistent-memory CoS seat existing.

---

## 6. Notes for the Claude Design pass

- **Use The Stoa design system.** Tokens already exist (`design_handoff_character_builder/tokens/`); brand consistency is automatic.
- **Decision points should be visually distinct** — PLINY is not just another node; it's a *gate* where verdicts trigger decisions. Consider a different shape (diamond?) or a visible "decision basin" treatment.
- **Loops should be visually distinct from forward edges** — color, dash pattern, or pulse direction. The cycles are the architecture; flattening them is the failure mode.
- **The bidirectional `direct_dialog` channel between HUMAN and POLYBIUS is THE load-bearing edge** — it's the persistent-memory channel that makes the CoS seat valuable; without it, POLYBIUS would just be a relay and PRINCIPAL could talk to PLINY directly. Visually thickest, possibly with a glow / annotation, possibly with a subtle pulse animation indicating its durable nature. See §5.1 for the trust-patterns visualization treatment.
- **CAPTAIN tool-constraints should be legible** — the "no Write/Edit" on ARGUS/CATO and "no WebSearch/WebFetch" on BARTLEBY/HERALD/CAPTAIN_ZENO are structural, not incidental. A small constraint badge on each affected node.
- **BEADWORK as substrate, not as just-another-node** — render as a horizontal substrate at the bottom of the frame; agents have thin connecting edges down to it; pulses accumulate visibly as actions occur.
- **Recursion view benefits from frontier treatment** — the announcement mentions shaders / 3D / built-in AI; the multi-tier fractal view is exactly where this would pay off. Static diagrams flatten what's most important.

---

## 7. What this spec does NOT specify

Deliberately left to the design pass:

- **Exact layout** — positions, distances, curves. Layout is design-tier judgment.
- **Specific colors beyond design-system tokens** — Claude Design should pick consistently from existing tokens.
- **Exact animation timings** — feel-out during iteration.
- **Whether to use react-flow / d3 / cytoscape / native canvas / WebGL** — implementation choice during Claude Code handoff.

---

## 8. Forward — the hypergraph

A near-future deliverable (planned but not yet scoped) is a **hypergraph** of code + bw tickets + repo content. Where the graph in this spec uses binary edges (one-channel, two-participants), the hypergraph supports **hyperedges** that connect arbitrary numbers of nodes — better suited to:

- A bw ticket linking simultaneously to multiple commits, multiple disciplines, multiple files
- A discipline (e.g., `u--7yg.10` verify-then-execute) applying simultaneously to multiple arcs, multiple roles, multiple defect classes
- A code symbol defined in one file but related semantically to multiple concepts and tickets

The hypergraph will be built by an agentic team (a sub-project under The Stoa per the recursive architecture). The KG component in this spec should be designed with the hypergraph successor in mind — the production component might support both binary-edge and hyperedge rendering, with the hypergraph mode arriving in a later arc.

For Claude Design's first pass: don't try to handle hyperedges yet. Get the binary-edge information-flow KG right first; the hypergraph is a separate visualization shape that gets its own design pass when the agentic-team arc spawns.
