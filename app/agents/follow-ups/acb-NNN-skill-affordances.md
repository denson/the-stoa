# Brief: testid attrs + window.STOA_STATE bridge for Claude Code skill consumption

**Status:** Brief filed (not dispatched). 2026-05-01.
**Suggested ticket id:** `acb-NNN-skill-affordances`. Number assigned in roadmap.
**Pipeline shape:** **build-only** — no design needed; ADA-direct.
**Effort:** ~1hr.
**Sequence constraint:** lands BEFORE acb-007 (agent-design-tutor skill) so the skill can consume them.

## Background

Chrome MCP validation (Colonel, 2026-05-01) confirmed the agent-design-tutor skill (acb-007) needs reliable affordances to drive the web app:

1. **Stable selectors.** Inline-styled elements + dynamic content currently offer no reliable hooks. The skill needs `data-testid` on every load-bearing interactive element so Chrome MCP scripts can target them deterministically.
2. **Runtime state bridge.** A read-only `window.STOA_STATE` object exposing the small set of fields a tutorial / skill needs to know: `{ dark, currentTab, selectedOfficer, roster, archetypeFilter }`. Avoids DOM-scraping for state.

Both are mechanical app-side affordances; no design judgment, no architectural risk.

## In scope

### Part A — `data-testid` attributes

Apply a consistent naming convention across these surfaces:

| Surface | Element | Suggested testid |
|---|---|---|
| Header | Theme toggle button | `theme-toggle` |
| Header | "New agent" button | `new-agent-button` |
| Header | Settings gear | `settings-button` |
| Header | Search trigger | `search-trigger` |
| Tab bar | Each tab button | `tab-{team\|skills\|meta}` |
| FilterSidebar | Each archetype filter chip | `filter-archetype-{archetypeName}` |
| FilterSidebar | "All" / "Clear" buttons | `filter-clear` |
| TeamView | Each officer card | `officer-card-{officerName}` |
| OfficerDetail | "Back to Team" link | `back-to-team` |
| OfficerDetail | Each callable-lieutenant chip | `lieutenant-chip-{lieutenantName}` |
| SkillsView | Each skill card | `skill-card-{skillName}` |
| MetaView | Each meta-aspect card | `meta-card-{metaAspectName}` |
| CommandPalette | Search input | `palette-input` |
| CommandPalette | Each result row | `palette-result-{resultId}` |

Naming convention: kebab-case; entity-then-id; lowercase identifiers (snake-case officer/skill names preserved as-is). Document the convention at the top of `App.tsx` or `Components.tsx`.

### Part B — `window.STOA_STATE` bridge

In `App.tsx`, add a `useEffect` that mirrors the relevant React state to a read-only-by-convention `window.STOA_STATE` object on every change:

```ts
useEffect(() => {
  (window as any).STOA_STATE = {
    dark,
    currentTab: tab,
    selectedOfficer: selected,
    roster,
    archetypeFilter,
    // (whatever other top-level state the skill needs)
  };
}, [dark, tab, selected, roster, archetypeFilter]);
```

Single-object replace per render (not in-place mutation), so observers can detect changes via reference equality.

Document the exposed shape in a JSDoc comment block above the effect.

## Out of scope

- TypeScript ambient declaration for `window.STOA_STATE` (`declare global { interface Window { STOA_STATE: ... } }`). Could be a follow-up if any TS code consumes it; for now skill consumers read it via JS where typing isn't needed.
- Mutation API (`window.STOA_DISPATCH({...})`). Read-only bridge for v1; if the skill needs to drive state changes, that's a separate brief.
- Event-stream version (`window.STOA_EVENTS`). YAGNI.

## Definition of done

1. Every surface in the testid table has a `data-testid` attribute.
2. `window.STOA_STATE` is populated and updates on relevant React state changes.
3. Manual probe: in browser devtools, `document.querySelectorAll('[data-testid]').length` returns a substantial count; `window.STOA_STATE` returns the expected shape.
4. No TypeScript regression (`tsc --noEmit` clean).
5. No visual regression (testid attributes don't affect rendering).

## Composition

- **Composes with acb-NNN-router-url-state** if both land in the same arc — the URL state and `STOA_STATE` overlap (both expose tab / selected / roster / archetypeFilter). If router lands first, `STOA_STATE` reads from `useParams()` / `useSearchParams()` instead of local state. If this brief lands first, the bridge migrates when router does.
- **Lands BEFORE acb-007** (hard sequence constraint).
