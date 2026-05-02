# Arc 12 build directive

**Audience:** the fresh Claude Code session opened to build Arc 12 deliverables.
**Authored by:** user-tier Chief-of-Staff (POLYBIUS-equivalent) + the PRINCIPAL (Denson Smith).
**Status:** active directive.
**Builds on:** Arc 9 (types-v2), Arc 10 (gen-data + generated/agents.ts), Arc 11 (sample.ts shim).

**You are MAJOR_PLINY for the the-stoa Arc 12 engagement.** Read `substrate/MAJOR_PLINY.md` and assume the orchestrator role. Open Claude Code in `~/claude_projects/the-stoa/`.

**Your one job for this engagement:** migrate React components from v1 types to v2 types directly; update the display to render the v2 rank ladder (HUMAN/COLONEL-reserved/MAJOR/CAPTAIN/LIEUTENANT) and the PRINCIPAL framework; remove or reduce the sample.ts shim. The React app must continue to function. Then return cleanly.

This is the meatiest of the post-consolidation arcs. Phase your work; surface design decisions before locking them in.

---

## Read first

1. **Arc 9's `app/src/data/types-v2.ts`** — the type definitions components will consume directly
2. **Arc 10's `app/src/data/generated/agents.ts`** — the v2 data the components render (12 agents total)
3. **Arc 11's `app/src/data/sample.ts`** — the v2→v1 transform shim; you're removing or reducing it
4. **Arc 11's hand-back report** — surfaced 4 mapping decisions; the three relevant for Arc 12:
   - (#1) v1 archetype enum retires — components consume `Agent.descriptiveRole` directly
   - (#2) Agent.description field doesn't exist in types-v2 — handle in Arc 12 (see "Colonel call" below)
   - (#3) Officer naming becomes v2-consistent (rank-prefixed mnemonic)
5. **Existing components that consume sample data** — `app/src/App.tsx`, `app/src/Components.tsx`, anything else importing from `data/`
6. **Existing UX features that must continue functioning:**
   - acb-001: dark mode
   - acb-008: testid affordances
   - acb-009: router-url-state (HashRouter, URL-shareable state for tab/selected/roster/archetypeFilter)
   - Officer overview, archetype filter, command palette, etc.
7. **Planning v2 spec** §2 (the five ranks), §3 (PRINCIPAL framework), §11 (Stoa data-model implications)

---

## Colonel call — surface early in Arc 12 before locking in

**The Agent.description field decision.** Two options:

- **(a) Extend types-v2.ts** to add `Agent.description?: string` field. Cross-arc work: types-v2 (Arc 9), gen-data Zod schema + parser (Arc 10), generated/agents.ts (re-run gen-data after schema extension). Components consume the field directly.
- **(b) Accept body-first-paragraph synthesis as canonical.** Arc 11's shim already does this (synthesizes one-line description from the body's first prose paragraph). Components inherit this through the shim or replicate the synthesis logic. No back-edits to types-v2 or gen-data. Simpler.

PRINCIPAL leans (b) — simpler scope, no cross-arc back-edits, and the synthesis works empirically. **Surface (a) vs (b) decision to PRINCIPAL early in Phase A** before component design decisions cement around it. If (a), Arc 12's scope expands to include the type extension + gen-data update.

---

## Deliverables

### 1. Migrate components from v1 types to v2 types

Currently components import from `app/src/data/sample.ts` which is a v2→v1 transform shim. Arc 12 makes components import from v2 sources directly:

- `import { stoaData } from './data/generated/agents';` (or whatever the export is named)
- Components consume `Agent`, `Human`, `RankSlot`, `RosterSlot`, `StoaDataV2` types from `types-v2.ts`
- v1 types (Officer, archetype enum, etc.) consumers update to v2 equivalents

After this work, `app/src/data/sample.ts` becomes either:
- A one-line re-export from generated/agents.ts (`export { stoaData } from './generated/agents';`)
- Or deleted entirely (components import directly from generated/agents.ts)

Build session decides which is cleaner.

### 2. Render the v2 rank ladder

The display should make all five ranks visible:

- **HUMAN** at the top (the PRINCIPAL framework — see deliverable 3)
- **COLONEL** as a reserved-empty slot (see deliverable 4)
- **MAJOR** with POLYBIUS + PLINY
- **CAPTAIN** with the 10 envelopes
- **LIEUTENANT** with skills (currently empty array in v2 data; render as "No skills authored yet" or hide entirely if empty)

Existing UX features (officer overview, archetype filter, palette) continue to function — the underlying data is now v2-shaped, but the UX is preserved. Existing keyboard shortcuts, tab navigation, dark mode, etc. all keep working.

### 3. Render the HUMAN/PRINCIPAL framework

The HUMAN slot is unique — it's the human served by the system. Display considerations:

- Where does the human's name come from? Suggest hardcoded "Denson" for development, OR derived from `git config user.name`, OR a config field. Build session picks; surface if uncertain.
- How does the human card differ visually from agent cards? Some signal that this is the PRINCIPAL, not an agent.
- The descriptiveRole "PRINCIPAL" should be visible somewhere in the human's display

### 4. Render the COLONEL reserved-empty slot

This is the most non-obvious UX question. The COLONEL slot represents a future agent rank that doesn't exist yet. Options for display:

- (i) Grayed-out card with "Reserved for future agent rank" label
- (ii) Empty section with header explanation
- (iii) Visible rank tier with placeholder text where agents would go
- (iv) Hidden by default with a "show reserved" toggle

Build session picks. The display should communicate that the rank exists in the system's vocabulary AND that it has zero current populations. **Worth surfacing the chosen approach before committing if you go beyond a simple grayed-out card** — UI design choices for new architectural concepts can have brand-defining implications.

### 5. Retire the v1 archetype enum

Per Arc 11 hand-back #1: components migrate from v1 archetype-based filtering/grouping to v2 descriptiveRole-based. This means:

- Wherever components import the v1 `archetype` type or enum, replace with `descriptiveRole` (or another v2 field if more appropriate)
- Archetype filter component (if it exists) refactors to filter by descriptiveRole
- Three best-effort fallback mappings from Arc 11 (CHIEF-OF-STAFF→orchestrator, FILE_CLERK→scout, SPEC-CHECKER→reviewer) get deleted from sample.ts as part of shim removal

### 6. Smoke test (load-bearing)

After all changes:
- TypeScript compiles cleanly (`npm run build`)
- Vite dev server starts cleanly (`npm run dev`)
- React app renders all five ranks correctly
- HUMAN renders with PRINCIPAL framework
- COLONEL slot renders as reserved-empty
- MAJOR shows POLYBIUS + PLINY with correct details
- CAPTAIN shows the 10 envelopes
- Existing UX features continue to function:
  - acb-001 dark mode toggle works
  - acb-008 testids present on key elements
  - acb-009 router-url-state preserves state across page loads
  - Officer overview, palette, navigation all work
- No console errors, no runtime exceptions

---

## Definition of done

- All components migrated to v2 types; v1 type imports removed
- v2 rank ladder rendered (all 5 ranks visible)
- COLONEL reserved-empty slot rendered with chosen UX
- HUMAN/PRINCIPAL framework rendered
- v1 archetype enum retired
- sample.ts reduced to re-export or deleted
- Smoke test passes (TypeScript clean, dev server clean, all UX preserved, all 5 ranks render)
- bw `stoa--*` epic for Arc 12 closed
- Voice clean (`grep -i "colonel" app/src/` — only deliberate references to the reserved future agent rank)
- Committed + pushed to `the-stoa` main (autonomous-ship per `u--7yg.11`)

---

## Out of scope

- **Vitest scaffold + tests** — Arc 13
- **Sub-project spawning** — Arc 14
- **Modifying types-v2.ts** — UNLESS Colonel call selects option (a) for description field; then it's in scope as a back-edit
- **Modifying gen-data adapter** — UNLESS Colonel call selects option (a); then in scope
- **Modifying substrate role files** — read-only consumer
- **The stoa--b3f gen-data timestamp ticket** — bundle into Arc 13 instead (Arc 13 touches gen-data internals naturally for tests)

---

## Voice discipline

`grep -i "colonel" app/src/` after work — any matches should be deliberate (e.g., the COLONEL rank label in the rank-ladder display, COLONEL Rank literal in TypeScript, JSDoc explaining reserved-rank semantics).

UI labels, header text, tooltips, etc. use v2 vocabulary:
- "PRINCIPAL" for the human role
- "MAJOR" / "CAPTAIN" / "LIEUTENANT" for agent ranks
- "COLONEL" only for the reserved future rank
- No "Officer" terminology for individual agents (v1's term); use the agent's mnemonic + descriptiveRole

---

## Beadwork

`bw` initialized (`stoa-` prefix). File a new epic:

```bash
cd ~/claude_projects/the-stoa
bw create "[EPIC] Arc 12 — display updates: components migrate to v2; rank ladder + PRINCIPAL framework rendered" -t epic -p 1
```

File children for: Phase A migration, rank ladder rendering, COLONEL slot UX, HUMAN/PRINCIPAL rendering, v1 archetype retirement, sample.ts cleanup, smoke test, voice audit. Close as you go.

---

## Discipline

- HITL default (planning v2 §7) — supervising via user-tier CoS
- Principal-as-router (`u--7yg.1`) — surface only project-direction calls (the description-field decision; possibly the COLONEL slot UX choice; possibly the human-name source)
- Verify-then-execute (`u--7yg.10`, `u--7yg.18`)
- One job per agent (`u--7yg.17`) — your one job is Arc 12; resist scope creep into Vitest (Arc 13) or sub-project (Arc 14)
- Wait-for-quiescence (`u--7yg.15`)
- Autonomous-ship on clean PASS (`u--7yg.11`)
- Voice discipline (planning v2 §6)

**Special concern: don't break existing UX.** acb-001/008/009 work shipped recently. The smoke test specifically verifies these continue to function. If the migration breaks any of them, that's a hard surface-to-PRINCIPAL moment — don't ship the regression.

---

## Suggested phasing

This is the meatiest post-consolidation arc. Phase your work:

- **Phase A: Surface the description-field decision (Colonel call).** Wait for PRINCIPAL response before committing to the type extension or synthesis path. ~10 min for the surface; PRINCIPAL response unblocks.
- **Phase B: Migrate components mechanically.** Update imports from sample.ts (shim) to generated/agents.ts (v2 source). Replace v1 type usage with v2 type usage. Existing display might look broken at this point — that's expected.
- **Phase C: Render v2 rank ladder.** Add HUMAN/COLONEL/MAJOR/CAPTAIN/LIEUTENANT rendering. Decide COLONEL slot UX; surface if going beyond simple grayed-out card.
- **Phase D: Render PRINCIPAL framework.** Add HUMAN slot with PRINCIPAL descriptiveRole; pick human-name source (hardcoded/git-config/config); surface if uncertain.
- **Phase E: Retire v1 archetype enum.** Refactor archetype filter, remove fallback mappings, clean shim.
- **Phase F: Smoke test + cleanup.** Verify all UX preserved; reduce/delete sample.ts; voice audit.

If Phase A's response is (b) "synthesis is fine," Phases B-F proceed without additional Colonel surfaces unless you hit something genuinely ambiguous. If Phase A is (a) "extend types-v2," the arc's scope expands and you'll surface again before committing the back-edits.

---

## Operating mode

**Human-in-the-loop** (planning v2 §7). Surface for input at:
- (a) The description-field decision (Phase A — required)
- (b) COLONEL slot UX if going beyond simple grayed-out card
- (c) Human-name source if uncertain
- (d) Work product ready for review (optional)
- (e) Done

For Arc 12: this is the most surface-rich arc post-consolidation. Don't be shy about surfacing — it's better to ask once than to ship a wrong UX choice.

---

## How to surface back

Either:
- Comment on a beadwork ticket in this repo (`stoa--*`)
- Write a short hand-back report; PRINCIPAL will relay

For Arc 12: hand-back reports are useful for design-decision surfaces because the discussion needs structured response.

Standby, run.
