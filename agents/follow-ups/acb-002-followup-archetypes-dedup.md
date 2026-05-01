# Follow-up: Delete `data.archetypes` redundancy after acb-001 lands

**Status:** Open. Filed during acb-001-darkmode dispatch (2026-04-30).
**Severity:** Low — code-smell, not a bug.
**Suggested ticket id:** `acb-002-followup-archetypes-dedup` (dispatch when acb-002 lands).

## Background

acb-001 introduces `archColors: Record<Archetype, [string, string]>` in `src/Components.tsx` as the canonical archetype-color source (theme-aware, light + dark pairs). After acb-001 ships, `data.archetypes` (`src/data/sample.ts`) becomes functionally redundant:

- It still holds a single light-mode color per archetype.
- Its colors are no longer used for rendering (the components layer pulls from `archColors` via `useTheme()`).
- Only `Object.keys(archetypes)` is referenced (in `FilterSidebar`, for the archetype enumeration).

ARGUS F8 in `agents/design/acb-001/argus-v1.md` flagged this as a real-but-small code smell: drift risk if a future arc adds an archetype to one map but not the other.

## Why deferred (not fixed in acb-001)

- acb-001 spec §4 explicitly excludes edits to `src/data/sample.ts` and `src/data/types.ts`.
- acb-002 already touches the data layer (gen-data adapter for the agent-team-team integration).
- The cleanup composes naturally with the acb-002 schema changes.

## Concrete plan

1. **Delete `data.archetypes`** from `src/data/sample.ts`.
2. **Delete `ArchetypeColors`** type alias from `src/data/types.ts`.
3. **Remove `archetypes` field** from the `StoaData` interface in `src/data/types.ts`.
4. **Remove `archetypes` prop** from `FilterSidebar`'s signature in `src/App.tsx`.
5. **Replace `Object.keys(archetypes)`** in `FilterSidebar` with `Object.keys(archColors)` (imported from `Components.tsx`).
6. **Verify** no other consumer reads `data.archetypes` (grep `archetypes\[` and `archetypes\.` across `src/`).
7. **Run** `tsc --noEmit` to catch any leftover references.

## Out of scope for this follow-up

- Restructuring `archColors` — its current shape is fine.
- Moving `archColors` into the data layer — explicitly contradicted by spec §6 decision 2 of acb-001 (presentation concern lives in components).
