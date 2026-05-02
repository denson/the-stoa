# acb-008 — Skill affordances: testid attrs + window.STOA_STATE bridge

**Author:** Denson Smith (Colonel) via Major Pliny.
**Status:** Spec locked, ready for build.
**Project:** The Stoa: agent-character-builder, v0.2 Phase 1 prerequisite.
**Working dir:** `C:/Users/denso/claude_projects/agent-character-builder/`.
**Pipeline mechanism:** **Build-only** — POLYBIUS dispatches ADA directly. No DAEDALUS, no ARGUS gate. VERA verifies, CATO craft-reviews. ~1hr scope.
**Source brief:** `agents/follow-ups/acb-NNN-skill-affordances.md` (NNN resolved to 008 here).

---

## §1 — Goal

Land two mechanical app-side affordances so downstream Claude Code skill consumers (acb-007 `agent-design-tutor`, validated via Chrome MCP) can drive the web app deterministically:

1. **Stable selectors.** Every load-bearing interactive element gets a `data-testid` attribute under a consistent naming convention.
2. **Runtime state bridge.** A read-only `window.STOA_STATE` object exposing the small set of top-level React state fields the skill needs.

Both are mechanical; no design judgment, no architectural risk. The success state is "a Chrome MCP script can target every UI surface by testid and read current state without DOM-scraping."

## §2 — Why this scope, why now

**Phase 1 prereq.** Per `agents/pliny-plans/acb-roadmap-v0.2-onward.md`, this is the first Phase 1 ticket to dispatch. It unblocks downstream consumers:

- **acb-006** (in-app tutorial) — the tutorial overlay needs stable selectors to anchor explanations onto specific UI elements.
- **acb-007** (`agent-design-tutor` Claude Code skill) — **hard sequence constraint: acb-008 lands BEFORE acb-007.** The skill cannot drive the web app without these affordances.

**Validation context.** Colonel performed Chrome MCP validation on 2026-05-01 and confirmed both affordances are necessary. Inline-styled elements + dynamic content offer no reliable hooks today; `data-testid` is the standard remedy. State-via-DOM-scraping is fragile; a single read-only object is the standard remedy.

**Why now (vs deferral).** The brief is concrete, the work is mechanical, the cost is ~1hr. Deferring it blocks Phase 1's vertical-slice demo. Per fix-now discipline, work this small ships in the current session.

## §3 — In scope

### Part A — `data-testid` attributes

Apply the following testids verbatim from the brief. Naming convention: kebab-case for the static prefix (entity-then-id pattern); identifier suffix preserved as-is from the data layer (`MAJOR_PLINY` stays uppercase, `dispatch-lieutenant` stays kebab, `inter-agent-comms` stays kebab — no re-casing). The convention comment in `src/Components.tsx:11-31` is the canonical statement of this rule.

| Surface | Element | testid |
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

**Naming convention documentation.** Add a short comment block at the top of `src/Components.tsx` (preferred — the components file is where reusable UI lives and where future contributors will look) describing the convention: kebab-case, entity-then-id, identifier preserved as-is. One paragraph; not a separate doc file.

**Implementation notes for ADA — structural realities of the current code:**

1. **`ThemeToggle` is a component**, exported from `src/Components.tsx` (line 138). The `theme-toggle` testid lives on the rendered button inside `ThemeToggle`, not in the `Header` JSX in `App.tsx`.
2. **Tab buttons, "Back to Team", Settings gear, palette result rows are `<div onClick>` or bare lucide icons**, not real `<button>` elements. The a11y refactor (acb-005) will fix that. For now, attach `data-testid` to the existing element (div / SVG wrapper). Don't pre-empt acb-005 by changing element types.
3. **Settings gear (line 119 of `App.tsx`)** is a bare `<Settings />` lucide SVG with no wrapping element. Wrap it in a `<span data-testid="settings-button">…</span>` (or equivalent minimal wrapper) — do NOT convert it to a real button (that's acb-005's territory). The wrapper exists solely to host the testid; preserve the current visual exactly.
4. **`palette-result-{resultId}` disambiguation.** The CommandPalette (`src/App.tsx` line 759) renders two result groups: officers (keyed by `o.name`) and skills (keyed by `s.name`). Officer and skill names could collide. Use `palette-result-officer-{name}` for officer rows and `palette-result-skill-{name}` for skill rows so consumers can address either type unambiguously. This is a load-bearing refinement of the brief's `palette-result-{resultId}` template, not a deviation.
5. **`SkillCard.callable_by` chips** (in `src/Components.tsx` ~line 399) are an interactive-looking surface NOT named in the brief. **Out of scope for this arc.** If acb-007 needs them later, file a follow-up. (Surfaced as a flag below.)

### Part B — `window.STOA_STATE` bridge

In `src/App.tsx`, add a `useEffect` that mirrors top-level React state to a read-only-by-convention `window.STOA_STATE` object. Single-object replace per render (not in-place mutation), so observers can detect changes via reference equality.

The exposed fields, mapped to current state names in `App.tsx` (lines 981-985):

```ts
useEffect(() => {
  (window as any).STOA_STATE = {
    dark,                       // from useTheme()
    currentTab: tab,            // local state, line 981
    selectedOfficer: selected,  // local state, line 982
    roster,                     // local state, line 984
    archetypeFilter,            // local state, line 985
  };
}, [dark, tab, selected, roster, archetypeFilter]);
```

`dark` is read via the existing `useTheme()` hook (`src/hooks/useTheme.tsx`) inside `App`.

Add a JSDoc block above the effect documenting the exposed shape, the read-only-by-convention contract, and the reference-equality observation pattern. Keep it concise.

## §4 — Out of scope (do NOT touch)

- **TypeScript ambient declaration** for `window.STOA_STATE` (`declare global { interface Window { STOA_STATE: ... } }`). The cast `(window as any)` is intentional v1; consumers read it from JS where typing isn't needed. Follow-up if any TS consumer emerges.
- **Mutation API** (`window.STOA_DISPATCH({...})`). Read-only bridge only. If the skill needs to drive state changes, that's a separate brief.
- **Event-stream version** (`window.STOA_EVENTS`). YAGNI per the brief.
- **`SkillCard.callable_by` chip testids.** Not named in the brief; flagging for a follow-up if acb-007 needs them.
- **Element-type changes** (div → button, SVG → button-wrapped). That's acb-005's a11y arc.
- **Router migration.** This arc reads from React state; when acb-009 (router-url-state) lands, the bridge migrates to `useParams()` / `useSearchParams()` then.

## §5 — Definition of done (the 5 criteria VERA verifies)

1. **Every surface in the §3 testid table has a `data-testid` attribute.** VERA checks each row by inspecting the rendered DOM at `http://localhost:5173/` (use RUNNER for dev server).
2. **`window.STOA_STATE` is populated and reactive.** Open the app; in browser devtools console, `window.STOA_STATE` returns the expected shape `{ dark, currentTab, selectedOfficer, roster, archetypeFilter }`. Toggle theme → `dark` flips. Click a tab → `currentTab` updates. Click an officer card → `selectedOfficer` populates. Each transition produces a NEW object (reference inequality).
3. **Manual probe substantial-count check.** `document.querySelectorAll('[data-testid]').length` returns a substantial count consistent with the table (≥10 in the default Team view; more after navigating into officer detail / skills / meta / palette open).
4. **No TypeScript regression.** `tsc --noEmit` is clean.
5. **No visual regression.** Wrapping the Settings icon in a span and adding testid attributes must not affect rendering. Compare against pre-arc tree (eyeball + CATO review).

## §6 — Pipeline plan

**Build-only.** Deviation from the standard full pipeline (DAEDALUS → ARGUS → ADA → VERA → CATO) is justified by the work shape: every decision is locked at the spec layer (testid table verbatim from Colonel; bridge snippet verbatim from brief). No design judgment is delegated; nothing for ARGUS to pre-critique. POLYBIUS dispatches ADA directly.

| Step | Officer | Deliverable | Gate |
|------|---------|-------------|------|
| 1 | ADA | Edits to `src/App.tsx` and `src/Components.tsx` per §3 Parts A and B; testid-convention comment in `Components.tsx` | Lands the changes |
| 2 | VERA | Verification against §5's 5 criteria via `http://localhost:5173/` | Pass / fail per criterion |
| 3 | CATO | Final craft review — diff hygiene, no visual regression, no stray hex literals or new inline styles, idiomatic React | Pass / needs-revision |
| 4 | Major Pliny | Spec-vs-result + project-spirit gate; verdict to Colonel | PASS / NEEDS-REVISION / ESCALATE |

## §7 — Key files

- **`src/App.tsx`** — heaviest hits. Header (testids on toggle wrapper / new-agent / settings-wrapper / search trigger / tabs); FilterSidebar testids; TeamView officer-card testids; OfficerDetail back-to-team + lieutenant-chip testids; MetaView meta-card testids; CommandPalette palette-input + palette-result-officer/skill testids; the `useEffect` for `window.STOA_STATE`.
- **`src/Components.tsx`** — moderate. `ThemeToggle` gets `theme-toggle`; `SkillCard` (in SkillsView) gets `skill-card-{name}`; testid-convention comment block at top of file.
- **No new files.** No TS ambient declaration file. No separate convention doc.

## §8 — Composition

- **Composes with acb-009-router-url-state** (next dispatch). If acb-008 lands first (current sequence), `window.STOA_STATE` reads from local React state. When acb-009 lands, `STOA_STATE` migrates to read from `useParams()` / `useSearchParams()` for `currentTab`, `selectedOfficer`, `roster`, `archetypeFilter` — fields that become URL-driven. `dark` continues to come from `useTheme()`. The migration is a small follow-up edit inside acb-009's scope; flagging it now so DAEDALUS for acb-009 sees it.
- **Hard sequence: acb-008 lands BEFORE acb-007** (`agent-design-tutor` skill). The skill is the consumer that justifies these affordances; it cannot dispatch without them.
- **No data-shape coupling.** This arc does not depend on acb-002 (gen-data adapter); the testid surfaces are all on rendered components, and the state bridge mirrors React state regardless of where the data originates.

## §9 — Self-assessed weak points

Surfaced for POLYBIUS / Colonel before dispatch:

1. **`palette-result-{resultId}` disambiguation is a Major-Pliny refinement, not a Colonel decision.** The brief said `palette-result-{resultId}`; I expanded it to `palette-result-officer-{name}` / `palette-result-skill-{name}` to handle name collisions between officers and skills. If Colonel prefers a single namespace (e.g., `palette-result-{type}-{name}` worded differently, or unified `resultId = "officer:NAME"` style), flag back before ADA dispatches.
2. **Settings gear span-wrapping is a deliberate non-fix.** Per fix-now discipline I considered converting it to a real `<button>` here (it's a one-line change and the icon is already interactive). I did NOT, because acb-005 owns the systemic divs-as-buttons → real-buttons refactor and pre-empting it from this arc would smear scope. The minimal `<span data-testid>` wrapper preserves visual + behavior exactly. If Colonel wants the button conversion folded in here, it's a small additive change.
3. **`SkillCard.callable_by` chips are interactive-looking but not testid'd in the brief.** They're listed in the skills view but not in the table. I left them out (per brief verbatim) and flagged as a follow-up. If acb-007 will need them, the cheapest fix is to add `lieutenant-chip-on-skill-{skillName}-{officerName}` (or similar) right now — handful of lines. Decision deferred to Colonel.
4. **`window.STOA_STATE` is `(window as any)` cast, by design per §4.** The cast looks ugly in TS; CATO may flag it. The spec sanctions it; the alternative (ambient declaration) is explicit out-of-scope. Document this in the JSDoc block above the effect so the reader knows it's intentional.

---

**End of spec. ADA reads this verbatim plus the source brief at `agents/follow-ups/acb-NNN-skill-affordances.md` and lands the edits. VERA verifies against §5. CATO reviews craft. Major Pliny gates.**
