# Arc 10 build directive

**Audience:** the fresh Claude Code session opened to build Arc 10 deliverables.
**Authored by:** user-tier Chief-of-Staff (POLYBIUS-equivalent) + the PRINCIPAL (Denson Smith).
**Status:** active directive.
**Builds on:** Arc 9 (commit `97e9126`) — `app/src/data/types-v2.ts` shipped with v2 type definitions.

**You are MAJOR_PLINY for the the-stoa Arc 10 engagement.** The user-tier Chief-of-Staff (POLYBIUS-equivalent) wrote this directive; you receive it and execute. Per planning v2 §4, MAJOR_PLINY is the orchestrator role.

Read `substrate/MAJOR_PLINY.md` and assume the orchestrator role.

**Open Claude Code in `~/claude_projects/the-stoa/`** (the unified repo's root). Operate from there; the work touches `app/` primarily, with `substrate/*.md` as read-only input.

**Your one job for this engagement:** build the `gen-data` adapter that reads role files from `substrate/`, parses them with Zod schema validation, and emits a typed TypeScript data file consumable by `app/src/data/`. Then return cleanly.

---

## Read first

1. **Planning v2 spec** at `~/claude_projects/user-beadwork/plans/three-role-recursive-architecture.md`:
   - §3 (naming convention — MAJOR_*.md and CAPTAIN_*.md filename patterns the adapter parses)
   - §9 (Roster — the full set of canonical agents the adapter expects to find in `substrate/`)
   - §11 (The Stoa data-model implications)

2. **Arc 9's deliverable** at `app/src/data/types-v2.ts` — the type definitions the adapter will produce data conformant to. Read in full:
   - `Rank`, `AgentRank`, `Agent`, `Human`, `RankSlot`, `HumanSlot`, `ColonelSlot`, `AgentSlot`, `RosterSlot`, `StoaDataV2`
   - JSDoc on each type — the COLONEL reserved-rank semantics is load-bearing

3. **Substrate role files** at `substrate/MAJOR_*.md` and `substrate/CAPTAIN_*.md`:
   - Read 2-3 to understand the actual file format (YAML frontmatter + markdown body)
   - Frontmatter typically has: `name`, `description`, `tools` (these are Claude Code's required sub-agent metadata)
   - Markdown body contains the role definition prose
   - `superseded/` subdir contains historical directives, NOT canonical role files — exclude from adapter input

4. **`u--7yg` design inputs:**
   - `u--7yg.20` (terminology fix; voice discipline)
   - The Codex/Gemini external review surfaced Zod for parsing rigor (filed in conversation log; key takeaway: schema validation at ingestion boundary catches malformed role files at build time)

5. **Discipline carry-forward:** `stoa--ggy` ticket flags v1 Colonel-as-human leakage in `app/src/data/sample.ts` (lines 11, 91, 110). NOT in scope for Arc 10 — Arc 11 sample-data swap handles it. Don't touch sample.ts.

---

## What Arc 10 is

The adapter is the bridge between canonical substrate (markdown role files with YAML frontmatter) and The Stoa's data model (TypeScript). It runs as a build-time Node script; output is committed (per localhost-only deployment posture). Subsequent arcs consume the adapter's output:
- Arc 11 wires sample data to use adapter output
- Arc 12 updates display to consume v2 types

Arc 10 produces the adapter; doesn't yet wire it into the React app's render path.

---

## Deliverables

### 1. Dependencies

Install required npm packages (in `app/`):

```bash
cd app
npm install --save-dev zod gray-matter
```

- **`zod`** — schema validation library (per Codex/Gemini second-opinion review). Schema = source of truth; TypeScript types derived from schema; runtime validation with descriptive errors.
- **`gray-matter`** — markdown parser that splits YAML frontmatter from body cleanly. Standard tool; lighter than full-blown markdown-AST libraries.

(If a reasonable Zod-equivalent or gray-matter-equivalent is already in dependencies, you can use that instead — surface the choice if it differs from the recommendation.)

### 2. The adapter script: `app/scripts/gen-data.ts`

A Node TypeScript script that:

1. **Resolves the substrate path.** Default: `../substrate/` (relative to repo root, since `app/` and `substrate/` are siblings in the-stoa). Configurable via `AGENT_SUBSTRATE_PATH` env var (NO `VITE_` prefix — this is a build script, not client code).

2. **Discovers role files.** Reads `<substrate-path>/MAJOR_*.md` and `<substrate-path>/CAPTAIN_*.md` (top-level only; exclude subdirectories like `v1-historical/`, `templates/`, `arcs/`, `superseded/`).

3. **Parses each file.** Use `gray-matter` to split frontmatter from body. Schema-validate the frontmatter with Zod. Extract:
   - From frontmatter: `name`, `description`, `tools`, plus anything else the role file format provides
   - From filename: derive `rank` (parse the `MAJOR_` / `CAPTAIN_` prefix), `mnemonic` (the part after the prefix, before `.md`)
   - From body: the markdown role-definition content (string)
   - **Descriptive role:** the body or frontmatter likely names this; if not directly available, infer from a header in the body or accept as a TODO field for now (surface to Colonel if the field isn't readily extractable)

4. **Builds a `StoaDataV2` object** matching the type from `types-v2.ts`. Ranks present: HUMAN (synthesized from PRINCIPAL config — likely a stub for now since no Human data lives in substrate), COLONEL (reserved-empty), MAJOR (POLYBIUS + PLINY), CAPTAIN (the 10), LIEUTENANT (skills — out of scope for Arc 10; produce empty array for now).

5. **Writes the output** to `app/src/data/generated/agents.ts` as a TypeScript file with:
   - Header comment noting it's auto-generated, with regeneration command
   - Imports from `../types-v2`
   - A single named export (e.g., `export const stoaData: StoaDataV2 = { ... };`)
   - Pretty-printed for readable diffs

6. **Validates output** against the Zod schema before writing — fail loudly on schema mismatch with descriptive error (which file, which field, what was expected vs. found).

### 3. Zod schemas

Define schemas in the adapter (or a sibling file `app/scripts/schemas.ts`). The schemas should:
- Match the TypeScript types in `app/src/data/types-v2.ts`
- Validate frontmatter shape (name string, description string, tools array of strings)
- Be the single source of truth for what a valid role file looks like

If the Zod-derived types diverge from `types-v2.ts`, decide which is canonical and reconcile. Default: `types-v2.ts` is canonical (Arc 9 is upstream of Arc 10 in the dependency chain); Zod schemas mirror those types.

### 4. Build pipeline integration

Wire the adapter into `app/package.json`:

```json
{
  "scripts": {
    "gen-data": "tsx scripts/gen-data.ts",
    "prebuild": "npm run gen-data",
    "predev": "npm run gen-data"
  }
}
```

- `tsx` is a common TypeScript-execution helper; install if not present (`npm install --save-dev tsx`)
- `prebuild` and `predev` mean `npm run dev` and `npm run build` automatically regenerate before running
- `npm run gen-data` is the manual regeneration command

### 5. Generated file commit policy

The output `app/src/data/generated/agents.ts` is **committed** to git (per localhost-only deployment posture, decided 2026-05-02). Reasoning: avoids the "remote build server can't access local agent-substrate" problem; the file is a build artifact that's also a deploy artifact. Re-run `npm run gen-data` after substrate changes; commit the regenerated file.

**Add to `.gitignore` exclusions:** if `.gitignore` ignores `**/generated/`, add an exception (`!app/src/data/generated/agents.ts`) OR document that the generated dir is tracked. Build session decides which is cleaner.

### 6. Documentation

- README note in `app/scripts/` (or comment block at the top of `gen-data.ts`) explaining: what the script does, when to re-run it, how to override `AGENT_SUBSTRATE_PATH`
- Brief mention in top-level `the-stoa/README.md` that the adapter pipeline exists and is auto-run on dev/build

### 7. Smoke test

After the adapter is built:

- `cd app && npm run gen-data` — runs cleanly; produces `app/src/data/generated/agents.ts`
- Inspect the output: 12 agents present (2 MAJORs + 10 CAPTAINs), COLONEL slot reserved-empty, HUMAN slot stub, structure matches `StoaDataV2`
- `npm run build` — TypeScript still compiles (the new generated file has correct types; doesn't break v1 code)
- `npm run dev` — Vite still starts; React app continues to function (acb-001/008/009 work unaffected since sample.ts and components still use v1 types)
- Delete `agents.ts` and re-run `npm run gen-data` — verifies idempotency
- Test with `AGENT_SUBSTRATE_PATH=/some/other/path` — verifies env var override (graceful failure if path doesn't exist)

---

## Definition of done

- `app/scripts/gen-data.ts` exists and runs cleanly
- `app/src/data/generated/agents.ts` is generated, committed, and matches `StoaDataV2` type
- Zod schemas defined and validate role files at build time (descriptive errors on malformed input)
- `npm run gen-data` works manually; `predev` and `prebuild` hooks auto-run it
- All 12 canonical role files (2 MAJORs + 10 CAPTAINs) parse successfully
- npm run build succeeds; npm run dev still serves the app cleanly
- bw `stoa--*` epic for Arc 10 closed
- Committed + pushed to `the-stoa` main (autonomous-ship per `u--7yg.11`)

---

## Out of scope

- **Sample data wiring** — Arc 11 (`sample.ts` swaps to consume `agents.ts`)
- **Display updates** — Arc 12 (components consume v2 types)
- **Vitest scaffold** — Arc 13 (formal tests for the adapter live there)
- **Sub-project spawning** — Arc 14
- **Modifying types-v2.ts** — leave it; Arc 9 is upstream
- **Modifying substrate/ files** — read-only consumer
- **The Colonel-as-human strings in sample.ts** (`stoa--ggy`) — defer to Arc 11

---

## Voice discipline

Less load-bearing here (build script + generated output, not prose). Still:
- Comments in `gen-data.ts` use v2 vocabulary (PRINCIPAL not Colonel)
- Generated file's header comment uses v2 voice
- `grep -i "colonel"` after work — any matches should be deliberate (e.g., a comment saying "COLONEL slot intentionally reserved-empty per planning v2 §2"). No reflexive Colonel-as-human leakage.

---

## Beadwork

`bw` initialized in the-stoa with `stoa-` prefix (Arc 9 did this). File a new epic:

```bash
cd ~/claude_projects/the-stoa
bw create "[EPIC] Arc 10 — gen-data adapter with Zod schema validation" -t epic -p 1
```

File children for: dependencies installed, adapter script, Zod schemas, build pipeline integration, generated file output, smoke test pass, documentation. Close as you go. Push beadwork branch alongside main.

---

## Discipline

- HITL default (planning v2 §7)
- Principal-as-router (`u--7yg.1`) — surface only project-direction calls
- Verify-then-execute (`u--7yg.10`, `u--7yg.18`) — directive-spec contradictions get surfaced
- One job per agent (`u--7yg.17`) — your one job is Arc 10; resist scope creep into Arc 11's sample-wiring or Arc 12's display
- Wait-for-quiescence (`u--7yg.15`)
- Autonomous-ship on clean PASS (`u--7yg.11`)
- Voice discipline (planning v2 §6)

**Special concern:** if a role file fails Zod validation during `gen-data` run, that's signal — the role file is malformed. **Don't auto-fix the role file.** Surface to PRINCIPAL with the descriptive error; PRINCIPAL decides whether to fix the role file or refine the schema. Schema-validation-as-truth-test is the load-bearing property.

---

## Operating mode

**Human-in-the-loop** (planning v2 §7). Surface for input at:
- (a) ambiguity in role file format vs. types-v2.ts (e.g., descriptive role isn't directly extractable — how to handle)
- (b) Zod schema design choices (strict vs. lenient on optional fields)
- (c) work product ready for review (optional — autonomous push for clean self-validation)
- (d) done

For Arc 10: this is meaty (multiple deliverables, build pipeline integration, schema design). Phase your work if helpful — Phase A: dependencies + types/schemas; Phase B: parser + validator; Phase C: output writing + pipeline integration; Phase D: smoke test + docs. Surface between phases if you hit anything unexpected.

---

## How to surface back

Either:
- Comment on a beadwork ticket in this repo (`stoa--*`)
- Write a short hand-back report; PRINCIPAL will relay

For Arc 10: schema design questions are worth surfacing before they propagate. Don't ship a schema you're not confident in.

Standby, run.
