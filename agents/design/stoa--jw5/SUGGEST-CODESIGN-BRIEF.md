# CO-DESIGN BRIEF (PART 3) — SUGGEST pillar (discovery front-door) — stoa--jw5 (u--9s2 Phase-1 increment)

**From:** PLINY_the-stoa (orchestrator) | sid 8040be7f
**For:** MAJOR_CHIRON_the-stoa + MAJOR_HAMILTON_the-stoa (co-design)
**Source:** Grand SUGGEST-pillar WHAT (delivered to stoa--jw5 directly, 2026-06-26) + FM scope-lock relay.
**operating-mode:** autonomous. Condition-1 (commit) CLOSED+VERIFIED (7ae4078 on feature branch
`stoa--jw5/u9s2-phase1-design`). This is Condition-2.

> SHAPE only (the suggesting-agent IMPLEMENTATION = Phase-2). Provision nothing.

---

## 1. The WHAT (the Grand's directive)

Add a **SUGGEST pillar as the FRONT-DOOR of discovery**. An agent **EXAMINES** what the project is
actually doing (purpose, code, data-flows, intended behavior) and **PROPOSES** the service set it
needs; a **human CONFIRMS**; the confirmed suggestion **BECOMES the DECLARE set**. This INVERTS the
current declare-primary front-door (which leans on a human to *remember* every service — the DWP-3
gap). The agent does the figuring-out "as we go"; the human ratifies. It is the **DWP-3 Phase-1
UPGRADE**: an agent reading the project can infer a service called via runtime-config / dynamic /
indirect paths that declaration-from-memory + static scan both miss.

**New model:** `SUGGEST (agent examines → proposes) → human CONFIRMS → that IS the DECLARE set →
SCAN validates drift → [Phase-2] runtime-observer`. Human-in-the-loop at suggest→confirm is a
**FEATURE, not a gap**.

## 2. THE LOAD-BEARING CONSTRAINT (read first; the §2 invariant, now one layer up)

The **gated mechanism is §0–§23** of design-formal.md — Part-1 (resolver §2 set-algebra,
provisioning S0-S6, §8 fixtures, §11 fork, §12.A maps) AND Part-2 (catalog §17, DECLARE/SCAN
discovery §18, generation G1-G4 §19, validation V1-V5 §20, emergent reframe §21). ALL of it STANDS
UNCHANGED. The SUGGEST pillar is strictly UPSTREAM of **DECLARE** (§18): it PRODUCES the confirmed
DECLARE set that §18 already treats as generation's authoritative input.

```
  project (purpose/code/data-flows)
        │  agent EXAMINES (uses catalog detection-hints)
        ▼
   PROPOSED service set  ──human CONFIRM gate (FAIL-CLOSED)──▶  DECLARE set  [feeds §18, UNCHANGED]
                                                                     │
                                              §18 DECLARE → §19 generate → §20 validate → resolve()[§2] → provision[§4]
                                                                     (ALL UNCHANGED — regression target 8/6/7)
```

The §8 fixtures (8/6/7) remain a REGRESSION TARGET. If the SUGGEST design pressures DECLARE/§18-§23
or resolve()/§8, STOP and surface it as a tradeoff (dilemma-classify) — not a silent change.

## 3. TWO FM WATCH-ITEMS (carry into the design; the FM verifies them at hand-offs)

1. **HUMAN-CONFIRM GATE = FAIL-CLOSED (load-bearing).** No human confirmation ⇒ NO DECLARE set ⇒ NO
   generation / NO provision. The agent PROPOSES; the human RATIFIES; an unconfirmed suggestion must
   NEVER silently become DECLARE. This is the safety net for suggest-agent error and is THE
   load-bearing property (human-in-the-loop is the feature). It must NOT weaken the existing
   fail-closed V1-V5.
2. **HONEST CAPABILITY SCOPE.** The SUGGEST design rests on a capability claim (an agent inferring
   services from code/data-flows). Scope it HONESTLY: the agent's inference ACCURACY is Phase-2 impl;
   the human-confirm gate is exactly what makes suggest-agent imperfection SAFE. Do NOT over-claim
   suggest completeness (same discipline as DWP-3 honest-scope). **If any tooling-capability premise
   about what the agent can infer is load-bearing, WEB-VERIFY it (gsearch / current docs), do not
   assert from memory.** (Framing note: the SAFETY rests on the human-confirm gate, not the agent's
   accuracy — so the capability claim is a USEFULNESS claim, not a safety-load-bearing one. Make that
   explicit so the design doesn't over-claim.)

## 4. Scope split (co-design, iterate together)

### HAMILTON (SUGGEST→confirm→DECLARE choreography + the human-confirm gate) owns:
- The **SUGGEST step shape:** what the agent EXAMINES (project purpose / code / data-flows / intended
  behavior) and how it maps observations → a PROPOSED service set (using CHIRON's per-service
  detection-hints). Web-verify any load-bearing capability premise.
- The **human-CONFIRM gate (FAIL-CLOSED):** the ratification step — proposed set surfaced to the
  human, human confirms/edits/rejects; only a CONFIRMED set becomes DECLARE; no confirm → no DECLARE
  → no generation. Specify the fail-closed property + how it composes with (does not weaken) V1-V5.
- **How the confirmed suggestion FEEDS the existing DECLARE (§18):** the confirmed set IS the
  `services:` declaration §18 consumes (the SUGGEST front-door produces §18's input; §18-§23 unchanged).

### CHIRON (per-service detection-hint catalog fields + SUGGEST-step tier/ownership) owns:
- **Per-service DETECTION-HINT catalog fields (additive):** recognizable signals per service (SDK
  import patterns, API-URL/endpoint patterns, data-flow / behavior signatures) so the SUGGEST agent
  can map project-behavior → candidate services. These are advisory HINTS (for inference), DISTINCT
  from the service's hard provisioning recipe (the typed entries §17 already carries — unchanged).
- **The SUGGEST-step tier/ownership + confirm-gate placement:** where the SUGGEST mechanism lives
  (T1 cookie-cutter provides it), who/what confirms (the human / project seat = T3), how the
  confirm-gate sits relative to the existing tier model. Catalog detection-hints = T1 additive field.

### Both (shared — the falsification/regression target):
- The **3 worked examples via the SUGGEST front-door:** for prospector / scienceclaw / labstat_bls,
  show `agent examines project → PROPOSES services → human CONFIRMS → DECLARE set → (existing §18-§23)
  → resolve → 8/6/7`. The SUGGEST front-door must produce the SAME DECLARE sets the discovery layer
  already validated. labstat_bls (load-bearing): agent examines the BLS-data project → proposes
  `[document-parsing, bls-oews]` → human confirms → DECLARE → generate → 7 (reproducing §8.3 /
  the Part-2 §23 result). Show the human-confirm fail-closed branch too (no confirm → no DECLARE).

## 5. Definition of Done (the SUGGEST increment)

- [ ] The SUGGEST step specified: what the agent examines + how it proposes a service set (capability
      premise honestly scoped; web-verified if load-bearing).
- [ ] The human-CONFIRM gate specified, FAIL-CLOSED (no confirm → no DECLARE → no generation/provision;
      does not weaken V1-V5).
- [ ] How the confirmed suggestion feeds the EXISTING DECLARE (§18) — unchanged downstream.
- [ ] Per-service DETECTION-HINT catalog fields specified (additive; advisory; distinct from the hard recipe).
- [ ] SUGGEST-step tier/ownership + confirm-gate placement specified.
- [ ] All THREE worked examples via the SUGGEST front-door → produce the DECLARE sets that resolve to
      8/6/7 (regression target hit) + the fail-closed no-confirm branch shown.
- [ ] The gated §0–§23 (resolver/provisioning/§8/maps + catalog/discovery/generation/validation/reframe)
      confirmed UNCHANGED (regression-confirm, not re-derive).
- [ ] DWP-3 upgrade stated honestly (SUGGEST closes more of the runtime-config gap than declare-from-
      memory + scan; the human-confirm gate makes agent-inference imperfection safe; not over-claimed).

## 6. Co-design protocol (I DRIVE the cross-handoff)

1. **Output:** a single unified `agents/design/stoa--jw5/suggest-codesign.md` (FLAT — keep Part-3 files
   flat siblings, per the c1 flat-cite lesson). HAMILTON writes its choreography sections to
   `agents/design/stoa--jw5/suggest-choreography-hamilton.md` (FLAT); CHIRON authors the unified
   `suggest-codesign.md` (sole writer), folding HAMILTON's half.
2. **Iterate together.** Post handoffs on stoa--jw5 tagged `[for: CHIRON_the-stoa]` / `[for:
   HAMILTON_the-stoa]` / `[for: PLINY_the-stoa]`. The detection-hints (CHIRON) and the suggest-flow
   (HAMILTON) co-constrain — flag any seam change.
3. **Arm active poll loops while waiting on your sibling** (the cross-handoff stall lesson). I poll
   ~2-3 min and drive; surface convergence to the FM.
4. **Honor §2 + the 2 watch-items absolutely.** Any pressure on the gated §0–§23 or resolve()/§8 →
   STOP + dilemma-classify to me. Web-verify any load-bearing capability premise (don't assert from memory).
5. **Convergence:** when suggest-codesign.md meets §5 and both sign off, post `SUGGEST CO-DESIGN
   CONVERGED — stoa--jw5` `[for: PLINY_the-stoa]`. I open the targeted gauntlet (DAEDALUS formalize the
   SUGGEST front-door INTO design-formal.md as new sections §24+, gated §0–§23 UNTOUCHED → ARGUS → ADA
   exercise the suggest→confirm→declare front-door + REGRESSION-confirm 8/6/7 → VERA → CATO → NOMOS).

**First action (each):** ACK on stoa--jw5 (confirm seat + your half), then begin. CHIRON — stand up the
`suggest-codesign.md` skeleton (the §5 DoD headers + the §2 constraint + the 2 watch-items at the top).

— PLINY_the-stoa | sid 8040be7f-a1ba-4917-b953-75947d464abf | the-stoa
