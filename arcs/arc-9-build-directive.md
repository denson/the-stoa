# Arc 9 build directive

**Audience:** the fresh Claude Code session opened to build Arc 9 deliverables.
**Authored by:** user-tier Chief-of-Staff (POLYBIUS-equivalent) + the PRINCIPAL (Denson Smith).
**Status:** active directive.
**Builds on:** Arc 8 (commit `52b08ae` directive in agent-substrate; commit `da5520d` in agent-character-builder applied v2 substrate to that project).

**You are MAJOR_PLINY for the agent-substrate Arc 9 engagement.** The user-tier Chief-of-Staff (POLYBIUS-equivalent) wrote this directive; you receive it and execute. Per v2 §4, MAJOR_PLINY is the orchestrator role — top-level Claude Code session at MAJOR rank.

Read `MAJOR_PLINY.md` (this directive's home repo, agent-substrate's Arc-4 v2-shape file) and assume the orchestrator role.

**Your one job for this engagement:** update agent-character-builder (The Stoa) to align with v2 architecture. Specifically: data model, gen-data adapter that reads from agent-substrate canonical, sample data wiring, display logic, and Vitest scaffold. Then return cleanly.

**Open Claude Code in `~/claude_projects/agent-character-builder/`** (not agent-substrate) — the work happens there. Directive lives in agent-substrate per the established pattern (read from `~/claude_projects/agent-substrate/arcs/arc-9-build-directive.md`).

**Substrate state going in:**
- `agent-character-builder/.claude/` has v2-shape substrate already deployed (Arc 8 landed it). MAJOR_POLYBIUS, MAJOR_PLINY, 10 CAPTAIN envelopes, templates/ all present.
- `agent-character-builder/CLAUDE.md` references MAJOR_POLYBIUS.md
- The React app continues to function (verified by Arc 8's smoke test); this arc must preserve that

---

## Architectural context (for external reviewers — Codex/Gemini second-opinion this directive)

Brief recap of the v2 architecture this directive depends on. Full spec at:
https://github.com/denson/user-beadwork/blob/main/plans/three-role-recursive-architecture.md

**The five ranks:**
- HUMAN — actual humans (the human is the PRINCIPAL — descriptive role)
- COLONEL — RESERVED for a future high-autonomy agent rank above MAJOR; not currently populated
- MAJOR — top-level Claude Code session (POLYBIUS = chief-of-staff; PLINY = orchestrator)
- CAPTAIN — sub-agents in `.claude/agents/`
- LIEUTENANT — skills in `skills/`

**Naming convention** (per v2 §3):
- File: `RANK_MNEMONIC[_<project>].md`
- Three pieces: rank + mnemonic name + descriptive role
- For humans: HUMAN rank, name (when known), PRINCIPAL descriptive role

**The Stoa's job:**
The Stoa (agent-character-builder) is the visualization/edit web app for the canonical agent definitions in agent-substrate. The Stoa is NOT a runtime — agents run in Claude Code sessions. The Stoa is the editor for canonical agents that get deployed via install.sh.

**Source-of-truth model:**
- agent-substrate is canonical
- The Stoa reads from agent-substrate's role files
- Edits in The Stoa (future feature) modify agent-substrate; install.sh re-runs propagate to project deploys
- Per-project overrides are NOT supported; specialization is via sub-projects (Arc 10)

---

## Read first

1. **`plans/three-role-recursive-architecture.md` in user-beadwork — v2 spec.**
   - §3 (naming + PRINCIPAL framework) — drives data model design
   - §9 (Roster table) — what each agent's structural properties are
   - §11 (The Stoa) — explicit data-model implications

2. **agent-substrate canonical role files** (the source the adapter will read):
   - `~/claude_projects/agent-substrate/MAJOR_POLYBIUS.md`
   - `~/claude_projects/agent-substrate/MAJOR_PLINY.md`
   - `~/claude_projects/agent-substrate/CAPTAIN_*.md` (10 files)
   
   These are the v2-shape canonical envelopes (re-authored in Arcs 4-5). Read 1-2 of them to understand the format the adapter will parse.

3. **agent-character-builder current state:**
   - `src/data/sample.ts` — current inline sample data (v1-shape; needs v2 update + adapter)
   - `src/data/types.ts` (or similar) — current TypeScript types
   - `src/Components.tsx` and `src/App.tsx` — current display logic
   - `package.json` — what's installed, what scripts exist
   - `vite.config.ts` — Vite configuration
   - Existing tests if any (npm test or vitest run to check)

4. **Existing acb-* beadwork in agent-character-builder** — check `bw list --all` for context on Phase 1 work that shipped (acb-001 dark mode, acb-008 skill affordances, acb-009 router-url-state). Don't touch those; just orient.

5. **`u--7yg` design inputs:**
   - `u--7yg.13` (three-role architecture)
   - `u--7yg.20` (terminology fix — Colonel → PRINCIPAL/HUMAN/COLONEL-reserved)
   - `u--7yg.21` (`.claude/`-gitignored discipline; relevant since we're operating in a project where that's true)

---

## What Arc 9 is

Per v2 §11 + acb-002's original intent (now superseded by this arc): make The Stoa accurately reflect canonical agent-substrate. Today The Stoa shows hard-coded sample data (v1 shape, with old roster + Colonel terminology). After Arc 9, The Stoa shows live v2-shape canonical agents read from agent-substrate.

This is a substantively bigger arc than Arcs 4-7 (which were focused substrate-internal work). Arc 9 spans:
- TypeScript type system (data model)
- Build-time data generation (adapter)
- React component logic (display)
- Test infrastructure (Vitest)
- Build pipeline integration (Vite + the gen-data step)

---

## Deliverables

### 1. Data model update (`src/data/types.ts` or equivalent)

TypeScript types encoding the v2 rank ladder + PRINCIPAL framework:

```typescript
// Conceptual shape — actual definition is your call
type Rank = 'HUMAN' | 'COLONEL' | 'MAJOR' | 'CAPTAIN' | 'LIEUTENANT';

type Agent = {
  rank: Rank;
  mnemonic: string;        // e.g., "POLYBIUS", "DAEDALUS"
  descriptiveRole: string; // e.g., "CHIEF-OF-STAFF", "ARCHITECT"
  body: string;            // markdown body content from the role file
  tools: string[];         // from frontmatter
  disciplines: string[];   // referenced disciplines (u--7yg.* IDs)
  filename: string;        // canonical filename (without _<project> suffix)
  // ... other fields needed for display
};

type Human = {
  rank: 'HUMAN';
  name?: string;           // learned through onboarding
  descriptiveRole: 'PRINCIPAL';
};

type RankSlot = {
  rank: Rank;
  reserved?: boolean;      // true for COLONEL
  agents: Agent[];
};
```

The COLONEL rank gets a slot but may have zero agents (reserved). The display should make this visible (rank exists; empty for now).

### 2. gen-data adapter (`scripts/gen-data.ts` or equivalent)

A TypeScript script that reads agent-substrate's role files and emits the data structure The Stoa consumes. Design choices:

- **Source path:** read from `~/claude_projects/agent-substrate/` by default, configurable via env var (e.g., `VITE_AGENT_SUBSTRATE_PATH`). Document this in package.json scripts.
- **Format parser:** role files are markdown with optional YAML frontmatter. Extract frontmatter (rank, tools, etc.) + body content + parse the role identity from the filename pattern.
- **Output:** TypeScript file at `src/data/generated/agents.ts` (or similar), git-ignored if regenerated at build time.
- **Build-time invocation:** add a script to `package.json` that runs gen-data before vite build / vite dev.

Decisions you make should be defensible against external review (Codex/Gemini). Document them inline in gen-data.ts comments.

### 3. Sample data wiring

Replace inline `src/data/sample.ts` with the adapter-generated equivalent. Two paths:
- **(a)** Generated TypeScript file replaces sample.ts entirely; sample.ts goes away
- **(b)** sample.ts re-exports from generated; gradually migrates

Either is fine. Minimum: app reads from generated data, not from hard-coded inline data.

### 4. Display updates (`src/Components.tsx`, `src/App.tsx`)

Update the display to render the v2 rank ladder:
- Show all five ranks (HUMAN, COLONEL, MAJOR, CAPTAIN, LIEUTENANT)
- COLONEL slot displays as reserved/empty (e.g., grayed out, "Reserved for future agent rank")
- HUMAN slot displays the human PRINCIPAL (currently just "Denson the PRINCIPAL" or hardcoded for the dev environment; Arc 11+ might learn this dynamically)
- Agent cards display with mnemonic + descriptive role + rank prefix in the filename

The existing UX (officer overview, archetype filter, command palette, etc.) should continue to work — just with v2 data.

### 5. Vitest scaffold

Add Vitest as the test runner (if not already configured). Tests for:
- gen-data adapter: given a sample role file, parses correctly into the Agent type
- Data model invariants (e.g., COLONEL slot is always reserved)
- Display logic smoke tests (a representative component renders without crashing)

This is foundation; full test coverage is downstream work.

### 6. Build pipeline

Verify:
- `npm run dev` starts Vite cleanly with adapter-generated data
- `npm run build` produces a working production bundle
- `npm test` runs the Vitest suite

### 7. Smoke test

After all changes:
- React app continues to function (load the dev server, browse the team view, click an agent, verify routing works per acb-009)
- Display shows v2 ranks (visible HUMAN at top, COLONEL reserved-empty, MAJOR with POLYBIUS + PLINY, CAPTAIN with the 10 envelopes, LIEUTENANT with skills if applicable)
- No regression in acb-001 (dark mode), acb-008 (testid affordances), acb-009 (router-url-state)

---

## Definition of done

- All deliverables above committed to `agent-character-builder` main
- React app continues to function (smoke test passes)
- `npm test` passes
- gen-data adapter reads from agent-substrate cleanly
- Display renders v2 rank ladder with COLONEL reserved-empty, HUMAN as PRINCIPAL framework
- bw beadwork epic for Arc 9 closed (file in agent-substrate per established pattern)
- Pushed to origin

---

## Out of scope

- **Sub-project spawning** — Arc 10
- **Stoa edit functionality** (write-back to canonical) — separate future arc; Arc 9 is read-only display
- **Re-authoring substrate** — Arcs 4-7 already shipped them
- **Architecture changes** — v2 is the spec; don't deviate
- **Modifying the substrate or install.sh** — Arc 9 consumes canonical; doesn't modify it

---

## Voice discipline

Less load-bearing than Arcs 4-6 (which were prose) but still relevant:
- Prop names, label strings, UI text should use v2 vocabulary (PRINCIPAL not Colonel; ranks in correct order)
- TypeScript type names should be v2-aligned
- Comment voice in code matches v2 register

`grep -i "colonel"` after work: any matches are deliberate (e.g., the label for the reserved COLONEL slot in the rank ladder display).

---

## Beadwork

`bw` is initialized in agent-substrate (`as-` prefix). File a new epic for Arc 9:

```bash
cd ~/claude_projects/agent-substrate
bw create "[EPIC] Arc 9 — Stoa data model + display + gen-data adapter aligned with v2" -t epic -p 1
```

File children for each deliverable. Close as you go. Push beadwork branch from agent-substrate when done.

The PROJECT-LEVEL beadwork in agent-character-builder (acb- prefix) stays untouched per visibility asymmetry (`u--7yg.14`); this is system-architecture work routed through agent-substrate.

---

## Discipline

- HITL default (v2 §7)
- Principal-as-router (`u--7yg.1`)
- Verify-then-execute (`u--7yg.10`, `u--7yg.18`)
- One job per agent (`u--7yg.17`) — your one job is Arc 9
- Wait-for-quiescence (`u--7yg.15`)
- Autonomous-ship on clean PASS (`u--7yg.11`)
- Voice discipline (v2 §6)

**Special concern: don't break the React app.** acb-001 + acb-008 + acb-009 work shipped recently. The smoke test before commit is load-bearing.

---

## Operating mode

**Human-in-the-loop** (v2 §7). Surface for input at:
- Adapter design choices that have ambiguity (parser format, source path config, build pipeline integration)
- Display design choices (how to render the reserved COLONEL slot specifically — visual treatment)
- Smoke test results before commit
- Done

For Arc 9: this is a substantive arc; surface more than you would for routine work. The build session may want to phase: Phase A (data model + types), Phase B (adapter), Phase C (display + sample wiring), Phase D (Vitest + smoke test). Surface between phases if any uncertainty.

---

## How to surface back

Either:
- Comment on a beadwork ticket in agent-substrate (`as--*`)
- Write a short hand-back report; PRINCIPAL will relay

For Arc 9 specifically: hand-back reports useful especially for design decisions in the adapter (so PRINCIPAL can review the parser approach, source-path strategy, etc.).

Standby, run.
