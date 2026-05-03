# Claude Design brief — interactive information-flow knowledge graph

**Audience for the brief:** Claude Design (claude.ai/design).
**Driven by:** PRINCIPAL Denson Smith (paste this brief + upload `kg-spec.md` into the Claude Design session).
**Source spec:** `the-stoa/docs/case-study/kg-spec.md` (248 lines, 8 sections).
**Target consumer:** **interactive React component** that lives in the Stoa app at `/#/architecture` (or similar route) AND is embeddable in the case study mini-site at §2.

---

## What to make

An **interactive knowledge graph visualization** of the information flow through the recursive three-role agent architecture. NOT a static diagram — the relationships (cycles, decision points, feedback loops, recursion) ARE the architecture; flattening them to a DAG loses what's load-bearing.

The component supports **5 visualization modes** (see source spec §5 + §5.1) toggleable via in-component controls:

| mode | what it shows | priority |
|---|---|---|
| **Static explore** (default) | All seats + edges visible; hover for tooltip; click for detail | P0 |
| **Trust patterns** | Three load-bearing trust patterns highlightable individually or together (HUMAN↔POLYBIUS paramount; HUMAN↔PLINY fallback; HUMAN↔POLYBIUS↔PLINY preferred load distribution) | P0 |
| **Information-flow** | Continuous animation of a brief flowing through gauntlet; verdicts return; loop-backs fire | P1 |
| **Recursion** | Multi-tier view: same shape replicated at user / project / sub-project tiers; cross-tier edges visible | P1 (frontier-design candidate) |
| **Tour** | Driven by external script (POLYBIUS narrating via Chrome MCP) — sequenced reveals, camera moves, node highlights | P2 (later arc) |

P0 is the load-bearing minimum. P1 is the next round if scope allows. P2 lands when the POLYBIUS tour script is authored.

---

## Use The Stoa design system

The Claude Design environment should already have The Stoa design tokens. Use those for color, typography, rank pills (HUMAN / COLONEL / MAJOR / CAPTAIN / LIEUTENANT each have distinct visual treatment), dark + light mode.

If not loaded: tokens at `the-stoa/app/design_handoff_character_builder/tokens/colors_and_type.css`.

---

## Nodes

Per source spec §1. Three categories:

### Humans
- **HUMAN_PRINCIPAL** — the human served. Distinctive visually (only HUMAN-rank node; sits at top); different shape/surface from agent nodes.

### Agents
- **MAJOR_POLYBIUS** (CHIEF-OF-STAFF) — between HUMAN and the rest of the team
- **MAJOR_PLINY** (ORCHESTRATOR) — the dispatch hub; visually central among CAPTAINs; **decision-point node**
- **CAPTAIN_DAEDALUS** (ARCHITECT)
- **CAPTAIN_ARGUS** (PLAN-CRITIC) — *no Write/Edit* (structural badge)
- **CAPTAIN_ADA** (EXECUTOR)
- **CAPTAIN_VERA** (VERIFIER)
- **CAPTAIN_CATO** (REVIEWER) — *no Write/Edit* (structural badge)
- **CAPTAIN_STRABO** (SCOUT)
- **CAPTAIN_BARTLEBY** (FILE-CLERK) — *no WebSearch/WebFetch* (structural badge)
- **CAPTAIN_HERALD** (INTAKE)
- **CAPTAIN_CURATOR** (SYNTHESIST)
- **CAPTAIN_ZENO** (SPEC-CHECKER) — *no Write/Edit, no WebSearch/WebFetch* (structural badge)

### Infrastructure
- **LIEUTENANTs** — collapsed category-node by default (skills are reusable; no per-skill rendering needed in roster view); expand-on-click to show individual skills
- **BEADWORK** — sits as a **substrate at the bottom of the frame**; every agent has a thin connecting edge down to it; pulses accumulate visibly during animation modes (this is what makes the "durable memory" claim *seen* rather than diagrammed)
- **ARTIFACTS** — the things being built (code, docs, role files); produced by ADA, reviewed by VERA/CATO

---

## Edge types (channels)

Per source spec §2. 12 channel types with direction / durability / sync hints:

- **direct_dialog** (HUMAN ↔ POLYBIUS) — bidirectional conversation; **THE LOAD-BEARING EDGE**: thicker, with a subtle pulse indicating its persistent-memory nature
- **paste_instruction** (POLYBIUS → PLINY, one-way handoff)
- **agent_dispatch** (PLINY → CAPTAIN, brief in)
- **captain_verdict** (CAPTAIN → PLINY, verdict back; decision-point)
- **skill_invocation** (CAPTAIN ↔ LIEUTENANT, helper call)
- **beadwork_write** (any → BEADWORK, durable; pulse down)
- **beadwork_read** (any ← BEADWORK, durable)
- **cross_tier_handoff** (POLYBIUS_a ↔ POLYBIUS_b, recursive)
- **escalation** (CAPTAIN → POLYBIUS, scope-exceeds-gauntlet)
- **principal_surface** (POLYBIUS → PRINCIPAL, project-direction calls)
- **artifact_write** (ADA → ARTIFACTS)
- **artifact_read** (any ← ARTIFACTS)

---

## Decision points + loops (5 explicit)

Per source spec §3. The cycles ARE the architecture — flattening loses what's load-bearing:

1. **ARGUS risk-back** — DAEDALUS design → ARGUS audit → PLINY decision → loop back to DAEDALUS (if risk) or forward to ADA
2. **VERA fail-back** — ADA build → VERA verify → PLINY decision → loop back to ADA (if fail) or forward to CATO
3. **CATO revision-back** — CATO review → PLINY decision → loop back to ADA (if revisions) or autonomous ship
4. **CAPTAIN_ZENO spec-drift loop** — CAPTAIN_ZENO mechanical check → PLINY → re-dispatch (if drift)
5. **Escalation chain** — CAPTAIN → POLYBIUS via beadwork → PRINCIPAL via direct_dialog (if project-direction)

**Visual treatment for loops:** distinctly colored back-edges (vs forward dispatch edges); animate the trip-wire moment so it's visible — verdict arrives at PLINY, PLINY visibly decides, back-edge activates if loop fires.

---

## Trust patterns (Mode 2 — load-bearing)

This mode is THE architectural value claim made visible. Three patterns toggleable individually or simultaneously:

| pattern | edges | annotation |
|---|---|---|
| **Pattern 1 — HUMAN ↔ POLYBIUS** (paramount) | the `direct_dialog` edge thickest, glowing, "the persistent-memory channel" | the channel the architecture is built around |
| **Pattern 2 — HUMAN ↔ PLINY** (fallback) | direct edge dashed/lighter; "fallback when bw isn't viable, or for urgent direct comms" | rare-by-design but real |
| **Pattern 3 — HUMAN ↔ POLYBIUS ↔ PLINY** (preferred load distribution) | path highlighted as sequence; "PRINCIPAL strategic; POLYBIUS validates+guides+authors directives; PLINY runs the team" | the mode the architecture optimizes for |

When a pattern is selected, dim the rest. When all three are toggled, show all in their distinct treatments.

---

## Recursion (Mode 4)

Per source spec §4. The same graph shape replicates at every tier (user / project / sub-project). Two strong rendering patterns:

- **Zoom-out reveal** — start at one tier, camera pulls back, same shape appears at parent tier, pulls back again — fractal
- **Side-by-side stack** — multiple tiers vertically; cross-tier edges visibly connect same node positions across tiers

**The recursion is the point** — a static diagram flattens what's most important. This is the mode where Claude Design's frontier capabilities (shaders / 3D / dynamic visualization) might genuinely earn the credit cost. Worth experimenting if scope allows; not blocking.

**Asymmetric visibility cone:** higher-tier POLYBIUS sees down (downward visibility cone visible); lower-tier POLYBIUS doesn't see up by default (no upward cone).

---

## Constraints

- **Dark mode + light mode** both first-class
- **Decision points are visually distinct** — PLINY isn't just another node; it's a *gate*. Different shape (diamond?) or visible "decision basin" treatment
- **Loops are visually distinct from forward edges** — color, dash pattern, or pulse direction
- **CAPTAIN tool-constraints visible** — small badges on ARGUS/CATO ("no edit"), BARTLEBY/HERALD/CAPTAIN_ZENO ("no web") — these are structural, not incidental
- **BEADWORK as substrate, not just-another-node** — horizontal substrate at bottom; pulses accumulate during animations
- **NOT A DAG** — cycles + decision points are the load-bearing structure; any rendering that flattens them is wrong

---

## Output shape

Interactive React component. Should embed cleanly in:
1. The Stoa app at `/#/architecture` (full-page view)
2. The case study mini-site §2 (smaller embedded version with link to full view)

Component API rough sketch:

```tsx
<KGVisualization
  mode={mode}            // "static" | "trust-patterns" | "info-flow" | "recursion" | "tour"
  highlightedPattern?={1 | 2 | 3 | "all"}  // for trust-patterns mode
  tourScript?={...}      // for tour mode (POLYBIUS-driven)
  onModeChange={fn}
/>
```

Implementation freedom: react-flow, d3, cytoscape, native canvas, WebGL — all reasonable. Claude Design picks during the iteration loop based on what fits the visual treatment.

---

## Handoff back

Same pattern as the case-study brief: Claude Design produces handoff bundle → PRINCIPAL → Claude Code (this seat) → implementation in `the-stoa/app/src/`.

The handoff should include: component code, tokens used, any data structures (e.g., the node/edge JSON shape — the source spec already has this defined; the implementation can adopt it directly).

---

## Forward note — hypergraph

Source spec §8 forward-flags the hypergraph successor: a future visualization where edges connect arbitrary numbers of nodes (not just two). Designed-with-the-hypergraph-in-mind means the production component might support both binary-edge mode (this work) and hyperedge mode (a later arc) — but **don't try to handle hyperedges yet.** Get the binary-edge KG right first.

---

## What to AVOID

- Static diagrams that flatten the cycles. The cycles are the point.
- Generic "graph" libraries' default styles — The Stoa has a design system; use it.
- Treating LIEUTENANT skills as agents in the visualization (they're a category-node, not individual seats — until the user expands them).
- Overloading the static-explore default with too many simultaneous modes. Each mode is its own toggleable view.
- Replacing the §N section numbering or the empirical-signal citations from the spec source. They're load-bearing.

---

## After this design pass

1. PRINCIPAL iterates with Claude Design (visual + interaction)
2. P0 modes (Static + Trust Patterns) ship first; P1 modes (Information-flow + Recursion) iterate next
3. Handoff bundle → Claude Code → implementation in Stoa app
4. POLYBIUS tour script (`substrate/templates/tour-script.md`) wires Mode 5 — separate later work

Standby.
