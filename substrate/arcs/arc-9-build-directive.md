# Arc 9 build directive

**Audience:** the fresh Claude Code session opened to build Arc 9 deliverables.
**Authored by:** user-tier Chief-of-Staff (POLYBIUS-equivalent) + the PRINCIPAL (Denson Smith).
**Status:** active directive.
**Builds on:** Arc Z (consolidation into `the-stoa`, 2026-05-02).

**Note on supersedure:** The original mega-Arc-9 plan (data model + adapter + display + tests + Vitest in one arc, against agent-substrate as a separate repo) is now archived at `substrate/arcs/superseded/arc-9-build-directive-mega-original.md`. Per PRINCIPAL direction 2026-05-02, the mega-plan was split into 5 smaller arcs (Arc 9-13). This is the canonical Arc 9 directive: narrow scope, TypeScript types + data model only, against the unified `the-stoa` repo.

**You are MAJOR_PLINY for the the-stoa Arc 9 engagement.** The user-tier Chief-of-Staff (POLYBIUS-equivalent) wrote this directive; you receive it and execute. Per planning v2 §4, MAJOR_PLINY is the orchestrator role.

Read `substrate/MAJOR_PLINY.md` (the v2-shape orchestrator role file, came in via Arc Z subtree merge from agent-substrate Arc 4) and assume the orchestrator role.

**Open Claude Code in `~/claude_projects/the-stoa/`** (the unified repo's root). Operate from there; the work touches `app/` primarily.

**Your one job for this engagement:** add v2 TypeScript types to `the-stoa/app/src/data/` encoding the v2 rank ladder + PRINCIPAL framework. Additive — don't break existing types or consuming code. The React app must continue to function. Then return cleanly.

---

## Read first

1. **Planning v2 spec** at `~/claude_projects/user-beadwork/plans/three-role-recursive-architecture.md`:
   - §2 (the five ranks — including reserved COLONEL)
   - §3 (naming convention + PRINCIPAL framework)
   - §11 (The Stoa — data-model implications)

2. **the-stoa repo state:**
   - `the-stoa/substrate/` — canonical role files (MAJOR_POLYBIUS, MAJOR_PLINY, 10 CAPTAINs, templates/, install.sh)
   - `the-stoa/app/` — React/Vite app
   - `the-stoa/app/src/data/` — current data types + sample data (this is what you'll be extending)

3. **The existing data types in `app/src/data/`:**
   - Read `types.ts` (or whatever file holds the type defs) to understand the v1 shape
   - Read `sample.ts` (or equivalent) to understand current data
   - **Don't break these.** Arc 9 is additive — new v2 types alongside existing v1 types. Arc 11 swaps sample.ts to the new shape; Arc 12 swaps display.

4. **`u--7yg` design inputs:**
   - `u--7yg.13` (three-role architecture)
   - `u--7yg.20` (terminology fix — Colonel → reserved-future-rank; PRINCIPAL is human's role)
   - `u--7yg.22` (Arc Z operational lessons — for general cross-repo discipline awareness)

---

## What Arc 9 is

Per planning v2 §11, The Stoa's data model needs to encode the v2 rank ladder. Arc 9 is the **narrow first step**: define the TypeScript types only. No adapter yet (Arc 10). No sample-data wiring (Arc 11). No display updates (Arc 12). No tests (Arc 13).

The smaller-chunks discipline (per `u--7yg.15` + the empirical signal that mega-arcs surface defects late): each arc surfaces issues earlier and lets us learn before the next dispatch.

---

## Deliverables

### 1. v2 TypeScript types in `app/src/data/`

Add the v2 type definitions. Suggested file: `app/src/data/types-v2.ts` (additive — exists alongside whatever v1 types are in the existing file).

Encode at minimum:

```typescript
// the rank ladder (planning v2 §2)
export type Rank = 'HUMAN' | 'COLONEL' | 'MAJOR' | 'CAPTAIN' | 'LIEUTENANT';

// agent record (planning v2 §3)
export type Agent = {
  rank: Exclude<Rank, 'HUMAN'>;  // agents are MAJOR or below
  mnemonic: string;               // e.g., "POLYBIUS", "DAEDALUS"
  descriptiveRole: string;        // e.g., "CHIEF-OF-STAFF", "ARCHITECT"
  body: string;                   // markdown body content
  tools: string[];                // from frontmatter
  filename: string;               // canonical filename without project suffix
  // ...add fields the planning doc + role files require
};

// human record (planning v2 §3 PRINCIPAL framework)
export type Human = {
  rank: 'HUMAN';
  name?: string;                  // learned through onboarding
  descriptiveRole: 'PRINCIPAL';   // hardcoded — PRINCIPAL is the only human role
};

// rank slot — for display (planning v2 §11)
export type RankSlot = {
  rank: Rank;
  reserved?: boolean;             // true for COLONEL
  agents: Agent[];                // empty array for COLONEL until populated
};

// reserved-COLONEL semantics: type-level enforcement that the COLONEL slot
// is currently empty (until a future agent rank claims it)
export type ColonelSlot = RankSlot & {
  rank: 'COLONEL';
  reserved: true;
  agents: [];  // empty tuple — typescript enforces zero agents at COLONEL rank for now
};
```

JSDoc each type so they're self-documenting (especially the COLONEL reserved-rank semantics — it's the most non-obvious part of the model).

### 2. Don't break existing code

The React app must compile and run after Arc 9. Means:
- Existing `types.ts` (or equivalent) stays as is
- Existing `sample.ts` stays as is, still consumes v1 types
- Existing components stay as is, still consume v1 types
- New v2 types coexist; nothing imports them yet (Arc 10 starts using them)

### 3. README note (optional but helpful)

If `app/src/data/` has a README or similar, append a brief note explaining the v1/v2 transition: "v2 types live in types-v2.ts; will replace v1 types as Arcs 10-12 wire the adapter, sample data, and display."

### 4. Smoke test

After adding the new types:
- `cd app/ && npm run build` (or `npm run dev` then check the page loads) — verify TypeScript compiles cleanly with no errors
- `npm test` if Vitest is configured (it isn't yet — Arc 13 — so skip)
- Manual: open the dev server, browse the app, confirm acb-001/008/009 work continues to function

---

## Definition of done

- v2 type definitions exist in `app/src/data/` (in `types-v2.ts` or equivalent)
- Existing v1 types + sample data + components untouched
- TypeScript compiles cleanly (`npm run build` succeeds)
- React app continues to function (smoke test)
- bw beadwork epic for Arc 9 closed (file in the-stoa with the freshly-initialized prefix)
- Committed + pushed to `the-stoa` main (autonomous-ship per `u--7yg.11`)

---

## Out of scope

- **gen-data adapter** — Arc 10 (uses Zod to parse role files into v2 types)
- **Sample data wiring** — Arc 11 (swap sample.ts to v2 types, optionally adapter-generated)
- **Display updates** — Arc 12 (components consume v2 types, render rank ladder + COLONEL reserved-empty slot + PRINCIPAL framework)
- **Vitest scaffold** — Arc 13
- **Sub-project spawning** — Arc 14
- **Modifying existing v1 types** — leave them; they're consumed by sample.ts + components which are out of scope until Arc 11/12

---

## Beadwork

`bw` is **not yet initialized in the-stoa** (per Arc Z's brief — defer to first arc that operates here). Arc 9 initializes bw:

```bash
cd ~/claude_projects/the-stoa
bw init --prefix stoa-
```

Then file the Arc 9 epic:

```bash
bw create "[EPIC] Arc 9 — v2 TypeScript types + data model" -t epic -p 1
```

File children for: types-v2.ts, smoke test pass, optional README note. Close as you go. Push the beadwork branch alongside main.

---

## Discipline

- HITL default (planning v2 §7) — supervising via user-tier CoS in Claude Desktop
- Principal-as-router (`u--7yg.1`) — surface only project-direction calls
- Verify-then-execute (`u--7yg.10`, `u--7yg.18`)
- One job per agent (`u--7yg.17`) — your one job is Arc 9; resist scope creep into Arc 10's adapter
- Wait-for-quiescence (`u--7yg.15`)
- Autonomous-ship on clean PASS (`u--7yg.11`) — push is part of the ship sequence
- Voice discipline (planning v2 §6) — prop names, type names, comments use v2 vocabulary (PRINCIPAL not Colonel; ranks in correct order)

**`grep -i "colonel"` after work:** any matches should be deliberate (e.g., the COLONEL Rank literal, the ColonelSlot type, JSDoc explaining that COLONEL is reserved). No reflexive Colonel-as-human leakage.

---

## Operating mode

**Human-in-the-loop** (planning v2 §7). Surface for input at:
- (a) ambiguity that needs PRINCIPAL input — likely places: how exactly to encode the reserved-COLONEL semantics in TypeScript (literal type, branded type, etc.); whether to add fields to the Agent type beyond what the v2 spec explicitly names
- (b) work product ready for review (optional — autonomous push for clean self-validation)
- (c) done

For Arc 9: this is a small focused arc (types only). If your TypeScript type design feels straightforward against v2 §3, autonomous push is correct. If you have a real design ambiguity (e.g., "the v2 spec says X but it's not clear how to encode that in TypeScript"), surface.

---

## How to surface back

Either:
- Comment on a beadwork ticket in this repo (`stoa--*`)
- Write a short hand-back report; PRINCIPAL will relay

Standby, run.
