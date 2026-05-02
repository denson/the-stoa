# Arc 11 build directive

**Audience:** the fresh Claude Code session opened to build Arc 11 deliverables.
**Authored by:** user-tier Chief-of-Staff (POLYBIUS-equivalent) + the PRINCIPAL (Denson Smith).
**Status:** active directive.
**Builds on:** Arc 9 (commit `97e9126`, types-v2.ts) + Arc 10 (commit `1282fe8`, gen-data adapter + generated/agents.ts).

**You are MAJOR_PLINY for the the-stoa Arc 11 engagement.** The user-tier Chief-of-Staff (POLYBIUS-equivalent) wrote this directive; you receive it and execute. Per planning v2 §4, MAJOR_PLINY is the orchestrator role.

Read `substrate/MAJOR_PLINY.md` and assume the orchestrator role.

**Open Claude Code in `~/claude_projects/the-stoa/`** (the unified repo's root). Operate from there; the work is in `app/src/data/`.

**Your one job for this engagement:** rewrite `app/src/data/sample.ts` to consume the generated v2 data (`app/src/data/generated/agents.ts`) instead of inline hardcoded data. Components still consume v1 types; sample.ts becomes a v2→v1 transform shim. The React app must continue to function. Resolves carry-forward `stoa--ggy`. Then return cleanly.

---

## Read first

1. **Arc 9's `app/src/data/types-v2.ts`** — v2 type definitions
2. **Arc 10's `app/src/data/generated/agents.ts`** — generated v2 data (12 agents)
3. **Existing `app/src/data/sample.ts`** — current inline v1 sample data; this is what you're rewriting
4. **Existing `app/src/data/types.ts` (or equivalent)** — v1 type definitions; sample.ts and components consume these
5. **Components that consume sample.ts** — read enough to understand what they import (e.g., `SAMPLE_DATA`, the shape they expect, what fields they use)
6. **Carry-forward ticket `stoa--ggy`** in this repo's bw — concretely names lines 11, 91, 110 in sample.ts as the Colonel-as-human strings to resolve

---

## What Arc 11 is

Arc 10 shipped the generated v2 data. Arc 11 makes sample.ts use it.

Arc 11 is the **sample-data swap**: sample.ts no longer has hardcoded inline data; it imports the v2 data from generated/agents.ts and transforms it into the v1 shape that components currently consume. Components are NOT updated in this arc (that's Arc 12).

This is a temporary shim by design — sample.ts becomes a thin v2→v1 transform layer. When Arc 12 updates components to consume v2 types directly, the shim gets removed and sample.ts either disappears or becomes a one-line re-export.

The shim approach lets Arc 11 ship without breaking components. Small-chunks discipline preserved.

---

## Deliverables

### 1. Rewrite `app/src/data/sample.ts`

Replace inline hardcoded data with:
1. Import the generated v2 data: `import { stoaData } from './generated/agents';` (or whatever export name Arc 10's adapter uses)
2. Transform v2 → v1 shape — write a transform function or inline mapping that converts the v2 `Agent` type to whatever shape the v1 `SAMPLE_DATA` (or equivalent) expects
3. Export the same name(s) the components currently import, with the transformed data

The transform handles fields like:
- v2 `Agent.rank` + `Agent.mnemonic` + `Agent.descriptiveRole` → whatever v1 fields exist (`name`, `archetype`, etc.)
- v2 `Agent.body` → v1 body content if components display it
- v2 `Agent.tools` → v1 tools field if present
- HUMAN slot → if v1 had a human concept, transform; otherwise omit
- COLONEL reserved-empty slot → omit from v1 output (v1 didn't know about it)

If the transform reveals fields v1 expected that v2 doesn't provide, OR vice versa — surface those gaps. They're either Arc 12 concerns or schema-extension concerns for Arc 9/10 backports.

### 2. Strip the inline Colonel-as-human strings

The carry-forward `stoa--ggy` ticket flags three strings in v1 sample.ts at lines 11, 91, 110. After the rewrite, those strings are GONE because sample.ts no longer has inline data — it consumes from generated/agents.ts which is v2-clean.

Verify with `grep -i "colonel" app/src/data/sample.ts` — should return zero (or only deliberate references like a comment "v1 had Colonel-as-human strings; resolved in Arc 11").

### 3. Verify components still compile + render

- `cd app && npm run build` — TypeScript compiles cleanly
- `npm run dev` — Vite serves clean; React app renders; components show data
- Manually browse the app — verify the data displayed matches what was there before (ranks/mnemonics/roles all correct from v2 source)

### 4. Close `stoa--ggy`

After verification, close the carry-forward ticket:

```bash
bw close stoa--ggy -m "Resolved in Arc 11. sample.ts no longer has inline data; consumes from generated/agents.ts (Arc 10) which is v2-voice. The three flagged Colonel-as-human strings are gone."
```

---

## Definition of done

- `app/src/data/sample.ts` rewritten as v2→v1 transform shim
- No inline Colonel-as-human strings remain (`grep -i "colonel" app/src/data/sample.ts` clean)
- Components still consume the same exported name(s); no component changes required
- TypeScript compiles cleanly (`npm run build`)
- React app continues to function (`npm run dev` + manual browse)
- `stoa--ggy` closed
- bw `stoa--*` epic for Arc 11 closed
- Committed + pushed to `the-stoa` main (autonomous-ship per `u--7yg.11`)

---

## Out of scope

- **Component updates** — Arc 12 (components migrate from v1 types to v2 types; sample.ts shim is removed at that point)
- **types-v2.ts modifications** — Arc 9 territory; if v1 components consume fields v2 doesn't have, surface as Arc 9-followup or accept a TODO in the transform
- **Modifying generated/agents.ts** — Arc 10 territory; that's the adapter's output
- **Vitest scaffold** — Arc 13
- **Sub-project spawning** — Arc 14
- **Schema design choice #1 from Arc 10's hand-back** (description field) — that's an Arc 12 concern when display surfaces descriptions; leave it for now

---

## Voice discipline

`grep -i "colonel" app/src/data/sample.ts` after work — should return zero or only deliberate references (e.g., a comment explaining the v1 → v2 transition).

The transform's prose (function names, comments) uses v2 vocabulary.

---

## Beadwork

`bw` initialized with `stoa-` prefix. File a new epic:

```bash
cd ~/claude_projects/the-stoa
bw create "[EPIC] Arc 11 — sample.ts swap to consume generated v2 data" -t epic -p 1
```

File children for: read-pass on sample.ts/components/types, transform implementation, smoke test, stoa--ggy closing. Close as you go.

---

## Discipline

- HITL default (planning v2 §7)
- Principal-as-router (`u--7yg.1`)
- Verify-then-execute (`u--7yg.10`, `u--7yg.18`)
- One job per agent (`u--7yg.17`) — your one job is Arc 11; resist scope creep into Arc 12's component updates
- Wait-for-quiescence (`u--7yg.15`)
- Autonomous-ship on clean PASS (`u--7yg.11`)
- Voice discipline (planning v2 §6)

**Special concern:** the v2→v1 transform might reveal fields v1 expected that v2 doesn't provide (e.g., `archetype`, `description`, etc.). If so:
- (a) If a synthesizable mapping exists (e.g., v1 archetype maps from v2 descriptiveRole), implement it
- (b) If no clean mapping exists, surface to PRINCIPAL — could be Arc 9 schema gap, Arc 12 scope, or accept a temporary `???` placeholder
- DO NOT modify types-v2.ts or generated/agents.ts to add fields ad-hoc; surface first

---

## Operating mode

**Human-in-the-loop** (planning v2 §7). Surface for input at:
- (a) v1↔v2 mapping gaps that need a design call
- (b) work product ready for review (optional — autonomous push for clean self-validation)
- (c) done

For Arc 11: this is a smaller arc than Arc 10 (no new dependencies, no new pipeline). The transform is the only design surface. If the mapping is straightforward, autonomous push.

---

## How to surface back

Either:
- Comment on a beadwork ticket in this repo (`stoa--*`)
- Write a short hand-back report; PRINCIPAL will relay

Standby, run.
