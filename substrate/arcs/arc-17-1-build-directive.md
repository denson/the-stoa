# Arc 17.1 build directive — Stoa LIEUTENANT slot rendering

**Audience:** the fresh Claude Code session opened to build Arc 17.1 deliverables (or this seat, if PRINCIPAL chooses direct execution).
**Authored by:** user-tier Chief-of-Staff (POLYBIUS-equivalent) + the PRINCIPAL (Denson Smith).
**Status:** active directive.
**Builds on:** Arcs 1-17 (the-stoa main `c5eea55`). Arc 17 deployed `substrate/skills/agent-author/SKILL.md` to substrate but the Stoa app's LIEUTENANT slot is currently empty — the gen-data adapter doesn't read skills yet. This is the small follow-up arc explicitly carved out from Arc 17.

**Execution mode: direct from POLYBIUS seat (per PRINCIPAL direction)** — not build-session dispatch. Arc 16.1 precedent for substrate fix-now from this seat applies; Arc 17.1 is similarly mechanical. The build-session-framed comms + activation steps below are kept as-is for record purposes; the actual work runs in the user-tier CoS-equivalent session.

**Your one job:** extend the gen-data adapter to read skills from `substrate/skills/*/SKILL.md`, extend types-v2 with a Skill type, render the LIEUTENANT slot in the Stoa app display. Then return cleanly.

This is small + mechanical. Comparable to Arc 13 (Vitest scaffold). Probably 1-2 hours.

---

## Comms — direct async via bw (proven in Arcs 16 + 17)

POLYBIUS polls the-stoa bw on a `*/5 * * * *` cron at engagement start. PLINY does NOT poll while working; only when surfacing a question (surface-and-wait pattern from Arc 16+ substrate teaching).

**bw command syntax:** read `MAJOR_PLINY.md` §6.1. `bw comment <id> "text"` (positional, NO `-m`). Run `bw prime` at activation per §4 step 3.

---

## Read first

1. **Arc 17 directive** at `substrate/arcs/arc-17-build-directive.md` — context for what's already deployed (skills deployment infrastructure)
2. **`substrate/skills/agent-author/SKILL.md`** — the one skill currently in substrate; YAML frontmatter has `name` + `description`; markdown body follows
3. **`app/scripts/gen-data.ts` + `gen-data-lib.ts`** — the adapter; current pattern reads top-level `MAJOR_*.md` + `CAPTAIN_*.md`, skips subdirectories. You'll extend to walk `substrate/skills/*/SKILL.md`
4. **`app/scripts/schemas.ts`** — Zod schemas for frontmatter validation; you'll add a skill schema
5. **`app/src/data/types-v2.ts`** — particularly the `Rank` type (already includes LIEUTENANT), `RosterSlot` (defines MAJOR / CAPTAIN / LIEUTENANT shape — already supports LIEUTENANT abstractly)
6. **`app/src/App.tsx`** + **`app/src/Components.tsx`** (or wherever the rank ladder renders) — add LIEUTENANT slot rendering parallel to existing CAPTAIN/MAJOR rendering
7. **`app/src/data/__tests__/generated.test.ts`** — current tests for roster shape; will need to add expectation that LIEUTENANT slot has at least 1 entry (the agent-author skill)

---

## Phase A — Two architectural decisions (LOCKED pre-dispatch by PRINCIPAL)

### A1. Skill type shape — LOCKED: new `Skill` type, discriminated `RosterSlot`

Skills are categorically different from agents (no rank dialogues, no dispatch surface, just invoked helpers). Type system reflects that. New `Skill` type with `name` / `description` / `body`. `RosterSlot` becomes a discriminated union on rank — MAJOR/CAPTAIN slots carry `agents: Agent[]`, LIEUTENANT slot carries `skills: Skill[]`.

### A2. LIEUTENANT slot display — LOCKED: cards + click-through detail route

Skill cards parallel to agent cards in roster view (name + description). Click navigates to detail route at `/#/skill/<name>` (or matching the existing agent-detail routing pattern). Detail page renders the full SKILL.md body content. Skills are first-class citizens of the roster.

---

## Deliverables

### 1. types-v2.ts — Skill type + discriminated RosterSlot

Add a `Skill` type with at minimum:
- `name: string` (from frontmatter)
- `description: string` (from frontmatter)
- `body: string` (the markdown body, like Agent has)

Update `RosterSlot` to be a discriminated union:
- `{ rank: "MAJOR" | "CAPTAIN", agents: Agent[] }`
- `{ rank: "LIEUTENANT", skills: Skill[] }`

(HUMAN and COLONEL slots already have their own shapes; no change to those.)

If types-v2 already has partial support for this, build on it; don't rewrite.

### 2. schemas.ts — Zod schema for SKILL.md frontmatter

Add a schema that validates:
- `name: string` (required, matches the directory name)
- `description: string` (required, non-empty)

The frontmatter on `agent-author/SKILL.md` is the reference shape. Mirror it.

### 3. gen-data-lib.ts — read skills

Extend the discovery pipeline to walk `substrate/skills/*/SKILL.md`:
- Skip the existing role-file walker (already filters subdirectories) — explicitly add a NEW walker for the skills directory
- For each `<skill-name>/SKILL.md`: read the file, extract frontmatter via `gray-matter`, validate against the new Zod schema, extract body
- Emit each skill as a `Skill` object in the LIEUTENANT slot of the generated roster

Match the existing discovery pattern in style. Keep the pure functions in gen-data-lib.ts; the entry script (gen-data.ts) doesn't need changes beyond what the library exports require.

### 4. Re-run gen-data + verify generated/agents.ts

```bash
cd app && npm run gen-data
```

Verify the generated file now has a LIEUTENANT slot with at least one entry (the `agent-author` skill).

### 5. Update tests

`app/src/data/__tests__/generated.test.ts` — add an assertion that the LIEUTENANT slot has at least 1 entry, and that the entry shape matches the Skill type (has name + description). Don't over-specify count; the substrate may grow more skills later.

If the existing test for "5 ranks" needs updating because LIEUTENANT now has content, update it accordingly.

### 6. The Stoa app — render LIEUTENANT slot

Add LIEUTENANT slot rendering to the rank ladder display. Two pieces:

- **Roster view** — LIEUTENANT slot renders skill cards parallel to MAJOR/CAPTAIN cards (per A2 lock-in). Card shows name + description; card click navigates to detail route.
- **Detail route** — `/#/skill/<name>` (or similar; match existing agent-detail routing pattern). Renders the SKILL.md body content. The detail route handles markdown rendering similar to how agent detail pages render Agent.body.

Reuse existing components where possible; this is "extend the rank ladder," not "build new components."

### 7. Smoke test

After all changes:
- `npm run gen-data` produces a clean diff (only the LIEUTENANT slot addition)
- `npm run build` clean (TypeScript happy with the new Skill type + discriminated RosterSlot)
- `npm test` passes (existing + new LIEUTENANT slot assertions)
- `npm run dev` starts; navigate to `/#/` — LIEUTENANT slot visible with `agent-author` card; click → detail page renders the SKILL.md body correctly
- Voice audit: `grep -i "colonel" app/src/` returns only deliberate reserved-future-rank references (existing state)

---

## Definition of done

- types-v2 has Skill type + discriminated RosterSlot
- schemas.ts has skill frontmatter schema
- gen-data-lib reads `substrate/skills/*/SKILL.md` and emits Skill entries
- generated/agents.ts has LIEUTENANT slot populated with at least `agent-author`
- Tests updated; `npm test` passes
- Stoa app renders LIEUTENANT slot (roster cards + detail route)
- Smoke test passes (build, dev, tests, voice audit)
- bw `stoa--*` epic for Arc 17.1 closed
- Committed + pushed to `the-stoa` main (autonomous-ship per `u--7yg.11`)

---

## Out of scope

- **Adding more skills to substrate** — Arc 17.1 makes the substrate's current skill (`agent-author`) renderable; doesn't author new skills. Future arcs add more skills as needed.
- **Modifying agent-gauntlet's skills** — different repo, different concern
- **Arc 18 (polling capability + consent)** — separate arc
- **Modifying the case study + KG drafts at `docs/case-study/`** — already-current; do NOT modify in Arc 17.1
- **Stoa app deeper redesign** — Arc 17.1 is "extend the existing rank ladder," not "redesign the display"

---

## Voice discipline

Standard. `grep -i "colonel"` audits should still return only deliberate reserved-future-rank references after the work.

---

## Beadwork

`bw` already initialized. File a new epic:

```bash
cd ~/claude_projects/the-stoa
bw create "[EPIC] Arc 17.1 — Stoa LIEUTENANT slot rendering" -t epic -p 1
```

File children for: types-v2 Skill type + RosterSlot discriminated union, schemas.ts skill schema, gen-data-lib skills walker, regen + verify, tests update, Stoa roster view rendering, Stoa detail route, smoke test. Close as you go.

---

## Discipline

- HITL default; surfaces minimal expected (Phase A locked pre-dispatch)
- Verify-then-execute (`u--7yg.10`, `u--7yg.18`)
- One job per agent (`u--7yg.17`) — don't expand into Arc 18 or skills authoring
- Wait-for-quiescence (`u--7yg.15`)
- Autonomous-ship on clean PASS (`u--7yg.11`)
- bw command syntax discipline (`u--7yg.23` / `MAJOR_PLINY.md` §6.1) — positional comment text, run `bw prime` at activation

---

## Operating mode

**Human-in-the-loop**. Surface for input only on:
- (a) Anything genuinely ambiguous mid-phase (no expected Phase A surfaces)
- (b) Work product ready for review (optional)
- (c) Done

For Arc 17.1: mechanical-after-modeled-on-existing; expect autonomous execution.

---

## How to surface back

Via bw comments on the Arc 17.1 epic. Use verified syntax. POLYBIUS polls every 5 min during engagement.

Standby, run.
