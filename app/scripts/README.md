# app/scripts

Build-time scripts for The Stoa. Run via `npm run …`; not shipped to the browser.

## `gen-data.ts`

Reads canonical role files (`MAJOR_*.md`, `CAPTAIN_*.md`) from `substrate/`,
validates their frontmatter against a Zod schema, and emits a typed module at
`app/src/data/generated/agents.ts` shaped to `StoaDataV2` (see
`app/src/data/types-v2.ts`).

### When to run

It runs automatically before `npm run dev` and `npm run build` via the
`predev` / `prebuild` hooks in `package.json`. Re-run manually any time the
canonical substrate changes:

```bash
cd app
npm run gen-data
```

The generated file (`app/src/data/generated/agents.ts`) is committed to git
per the localhost-only deployment posture (decided 2026-05-02). Re-run after
substrate edits, then commit the regenerated file.

### Source path override

By default the adapter reads from `<repo-root>/substrate/`. To point it at a
different substrate copy:

```bash
AGENT_SUBSTRATE_PATH=/some/other/substrate npm run gen-data
```

(No `VITE_` prefix — this is a Node build script, not client code.)

### What it validates

- Every CAPTAIN role file has YAML frontmatter with `name`, `description`,
  `tools` (string or array; comma-split if string), and an optional `model`.
- Every role file's body contains a `| **Descriptive role** | XXX |` row from
  which the descriptive role is extracted.
- The assembled `StoaDataV2` object passes its own Zod self-check before it
  is written to disk.

A schema-mismatch is treated as signal — a malformed role file fails the
build with a descriptive error rather than silently propagating a broken
record. Don't auto-fix the role file; surface the error to the PRINCIPAL.

## `schemas.ts`

The Zod schemas used by `gen-data.ts`. Two layers:

1. `frontmatterSchema` — validates raw YAML frontmatter pulled out of a
   CAPTAIN role file.
2. The output schemas (`agentSchema`, `humanSchema`, `*SlotSchema`,
   `stoaDataV2Schema`) — mirror the TypeScript types in
   `app/src/data/types-v2.ts` and validate the assembled output before it is
   serialized.

`types-v2.ts` is canonical; the schemas mirror those types.
