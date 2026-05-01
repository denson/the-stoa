# Handoff: agent-character-builder UI

## Overview

This is the design handoff for **agent-character-builder**, the first product in **The Stoa** family — a power-user web app for browsing, composing, and authoring teams of AI agents (officers, lieutenants, skills, meta-aspects). The handoff covers the click-thru shell: header + tab bar, Team browse, Officer detail, Skill library, Meta-aspect index, and a ⌘K command palette.

## About the Design Files

The files in this bundle (`ui/index.html`, `ui/App.jsx`, `ui/Components.jsx`, `ui/data.jsx`) are **design references created in HTML** — a working prototype showing intended look, structure, and behavior. **They are not production code to copy directly.**

The task is to **recreate these designs in the target codebase's existing environment** — using its component library, routing, state management, and data layer. If the codebase already has primitives (Button, Chip, Sidebar, Modal), use those and re-skin them to match these tokens; do not import the prototype's components verbatim.

If no production codebase exists yet, React + Vite + TypeScript is the natural target (the prototype is plain JSX and ports cleanly).

## Fidelity

**High-fidelity (hifi).** Final colors, typography, spacing, and interaction states are committed. Recreate pixel-perfect.

The two open variables are:
1. **Real brand fonts** — the prototype uses Inter + JetBrains Mono as substitutes. If real brand fonts ship later, swap them in `colors_and_type.css` (`--font-display`, `--font-mono`).
2. **Real logo / wordmark** — the placeholder marks in `assets/` are stand-ins.

Everything else (color tokens, rank pills, archetype accent colors, type ramp, spacing) is final.

---

## Screens / Views

### 1. Team Overview (default landing view)

**Purpose:** Browse the active roster of officers. Filter by archetype or switch rosters from the left sidebar.

**Layout:**
- Sticky header (60px tall, includes logo + product chip + search + "New agent" CTA + tab bar).
- Below the header: two-column layout.
  - Left: Filter sidebar, fixed `width: 220px`, `background: var(--bg-sunken)`, right border `1px solid var(--border-1)`.
  - Right: Officer grid, `padding: 24px 28px`, `display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 14px;`.

**Officer Card (`OfficerCard`):**
- `background: var(--bg-surface)`, hover state `var(--bg-app)`, transition `background 180ms`.
- `border: 1px solid var(--border-1)`, `border-left: 3px solid <archetype color>` (left accent only — DO NOT add accents on other sides).
- `border-radius: 10px`, `padding: 16px 18px 14px`, `box-shadow: 0 1px 2px rgba(20,18,12,0.04)`.
- Vertical stack, `gap: 8px`:
  1. Rank pill + archetype label inline (gap 8px, wraps).
  2. Officer name — `JetBrains Mono`, `font-weight: 700`, `font-size: 14.5px`, `letter-spacing: 0.02em`, `color: var(--fg-1)`.
  3. Role description — `Inter`, `font-size: 12.5px`, `color: var(--fg-2)`, `line-height: 1.45`, `text-wrap: pretty`.
- Cursor `pointer`. Whole card opens Officer Detail on click.

**Rank pill (`RankPill`):**
- `JetBrains Mono`, `font-size: 10px`, `font-weight: 600`, `letter-spacing: 0.06em`, `text-transform: uppercase`.
- `padding: 2px 7px`, `border-radius: 999px`, `border: 1px solid <ring>`.
- Three rank styles (bg / fg / border):
  - **major**: `#F5EBD3` / `#8A6B2C` / `#E5D6A8`
  - **captain**: `#ECEDEF` / `#5C5F66` / `#D9DBDF`
  - **lieutenant**: `#F2E2D5` / `#8A4A2C` / `#E5C9B3`

**Archetype label (`ArchetypeText`):**
- Inline mono text, `font-size: 10.5px`, color = archetype color (see Design Tokens), format: `<archetype>-archetype` lowercase. Example: `architect-archetype`.

**Filter Sidebar:**
- Two sections: **Roster** and **Archetype**, each with an uppercase label (`Inter`, `11px`, `weight 600`, `letter-spacing 0.08em`, `color: var(--fg-3)`, `margin-bottom: 8px`).
- Selectable items: `font-size: 12.5px`, `padding: 6px 10px`, `border-radius: 6px`, cursor pointer.
- Active state: `background: var(--accent-soft)` (`#E6EBF3`), `color: var(--accent)` (`#2B4A7F`), `font-weight: 500`.
- Archetype rows include an 8×8px square swatch in the archetype color, gap 8px before label.

### 2. Officer Detail

**Purpose:** Read the full officer body (markdown), see tools / lieutenants / required reading / model tier / file path. Edit / Clone / View JSON / Add to roster.

**Layout:**
- Two-column, no left filter sidebar.
- Main column: `flex: 1`, `padding: 24px 32px`, `max-width: 920px`.
- Right metadata sidebar: `width: 260px`, `padding: 24px 24px 24px 16px`, `border-left: 1px solid var(--border-1)`, `background: var(--bg-surface)`, sticky `top: 110px`.

**Main column:**
1. Back link — `Inter`, `12px`, `var(--fg-3)`, content `← Back to Team`, cursor pointer.
2. Rank pill + archetype label inline.
3. H1 officer name — `JetBrains Mono`, `font-weight: 700`, `font-size: 30px`, `letter-spacing: 0.01em`, `color: var(--fg-1)`.
4. Role description — `Inter`, `15px`, `color: var(--fg-2)`, `line-height: 1.55`, `max-width: 68ch`, `text-wrap: pretty`.
5. Action button row, `gap: 8px`, all secondary except the last (primary "Add to roster"):
   - `Edit` (icon: edit), `Clone` (icon: copy), `View JSON` (icon: code), `Add to roster` (icon: plus).
6. `border-top: 1px solid var(--border-1)`, `padding-top: 20px`, then rendered markdown body.

**Markdown body styles:**
- H2: `Inter`, `24px`, weight 600, `letter-spacing: -0.02em`, margin-top 24, margin-bottom 10, color `var(--fg-1)`.
- H3: `Inter`, `18px`, weight 600, margin-top 22, margin-bottom 8, color `var(--fg-1)`.
- Paragraph: `Inter`, `14.5px`, color `var(--fg-2)`, `line-height: 1.65`, `max-width: 68ch`, `margin-bottom: 12px`, `text-wrap: pretty`.
- Ordered list: same paragraph type, `padding-left: 22px`, list items `margin-bottom: 4px`.
- Inline code: `JetBrains Mono`, `0.88em`, `background: var(--bg-inset)`, `border: 1px solid var(--border-1)`, `padding: 1px 5px`, `border-radius: 3px`, `color: var(--fg-1)`.
- Bold (`**...**`): `color: var(--fg-1)`, `font-weight: 600`.

**Right sidebar sections:**
- Each section starts with an uppercase label (`Inter`, 10.5px, weight 600, `letter-spacing: 0.08em`, color `var(--fg-3)`, margin-bottom 8).
- **Tools** — flex-wrap chips of tool names, each `Chip variant="tool"`. Section heading shows count in dim mono after the label.
- **Callable lieutenants** — `Chip variant="skill"` (blue tone).
- **Required reading** — `Chip variant="meta"` (purple tone).
- **Model tier** — single `JetBrains Mono` `13px` value (e.g. `opus`).
- **Body path** — `JetBrains Mono` `11px`, `color: var(--fg-2)`, `word-break: break-all`, `line-height: 1.5`. Example: `definitions/bodies/daedalus.md`.

**Chip styles (3 variants):**
- Common: `JetBrains Mono`, `font-size: 11px`, `font-weight: 500`, `padding: 3px 9px`, `border-radius: 4px`, `border: 1px solid <ring>`, inline-flex with `gap: 6px`.
- **tool** — bg `var(--bg-inset)` (#ECE9E1), fg `var(--fg-2)`, border `var(--border-1)`.
- **skill** — bg `var(--accent-soft)` (#E6EBF3), fg `var(--accent)` (#2B4A7F), border `#B7C5DA`.
- **meta** — bg `#F1EEF7`, fg `#5B4D86`, border `#E0DAEC`.

### 3. Skill Library

**Purpose:** Browse callable skills (sub-agents, scripts, schema validators).

**Layout:**
- No sidebar.
- `padding: 24px 28px`, grid `repeat(auto-fill, minmax(280px, 1fr))`, `gap: 14px`.

**Skill Card:**
- Same surface treatment as Officer Card BUT no left-border accent (skills aren't archetyped).
- Header row, `justify-content: space-between`:
  - Name: `JetBrains Mono`, weight 600, `14px`, `var(--fg-1)`.
  - Kind tag: `JetBrains Mono`, `10px`, uppercase, `letter-spacing: 0.08em`, `var(--fg-3)`. Examples: `SKILL`, `SUBAGENT`.
- Description: `Inter`, `12.5px`, `var(--fg-2)`, `line-height: 1.45`, clamped to 3 lines (`-webkit-line-clamp: 3`).
- `callable_by` row (only if non-empty): inline label "callable by" (`Inter`, 10.5px, `var(--fg-3)`) followed by `Chip variant="tool"` per officer name.

### 4. Meta-aspects

**Purpose:** Read shared cross-cutting docs (envelope-lifecycle, inter-agent-comms, fix-now-discipline, discipline-catalog).

**Layout:**
- Single column, `max-width: 760px`, vertical stack of cards `gap: 8px`.
- Each card: `bg-surface`, `border: 1px solid var(--border-1)`, `border-radius: 10px`, `padding: 16px 18px`.
- Three lines per card:
  1. Slug — `JetBrains Mono`, weight 600, `13px`, `var(--fg-1)`.
  2. Title — `Inter`, `14px`, weight 500, `var(--fg-1)`.
  3. Summary — `Inter`, `13px`, `var(--fg-2)`, `line-height: 1.55`, `text-wrap: pretty`.

### 5. Header (persistent)

- Sticky, `background: var(--bg-surface)`, bottom border `1px solid var(--border-1)`, `z-index: 10`.
- Top row, `padding: 10px 24px 0`:
  - Logo mark (28px tall, `assets/mark.svg`).
  - Wordmark text "The Stoa" — `Inter`, weight 600, `15px`.
  - Product chip — `JetBrains Mono`, `11px`, `var(--fg-3)`, `padding: 2px 8px`, `background: var(--bg-inset)`, `border-radius: 4px`. Content: `character-builder`.
  - Right cluster (`margin-left: auto`, gap 10):
    - Search trigger — flex row with search icon + "Search…" placeholder + `⌘K` kbd hint inside a `var(--bg-sunken)` capsule, `border: 1px solid var(--border-1)`, `border-radius: 6px`, `padding: 5px 10px`.
    - "New agent" — primary Button, `size="sm"`, leading icon `plus`.
    - Settings icon (gear, 16px, `var(--fg-3)`).
- Tab bar, `padding: 4px 24px 0`, `margin-top: 6px`:
  - Each tab: `padding: 12px 14px`, `Inter` `13px`, `weight: 500`.
  - Inactive tabs: `var(--fg-3)`. Active: `var(--fg-1)` + `border-bottom: 2px solid var(--accent)`.
  - Count badge per tab: `JetBrains Mono`, `11px`, dim color (`var(--fg-3)` active / `var(--fg-4)` inactive).

### 6. Command Palette (⌘K)

**Trigger:** `Cmd+K` / `Ctrl+K`, or click the header search trigger.

**Backdrop:** `position: fixed; inset: 0; background: rgba(20,18,12,0.35); backdrop-filter: blur(12px);` Click outside or Esc to close.

**Panel:** centered top, `padding-top: 120px`, `width: 560px`, `bg-surface`, `border: 1px solid var(--border-1)`, `border-radius: 10px`, shadow `0 4px 12px rgba(20,18,12,0.07), 0 12px 32px rgba(20,18,12,0.05)`, overflow hidden.

**Input row:** `padding: 14px 16px`, bottom border, search icon + autofocus input + `esc` kbd hint.

**Results sections:**
- Section labels: uppercase mono-spaced labels, `padding: 10px 16px 4px`, `var(--fg-4)`.
- Result rows: `padding: 7px 16px`, hover `background: var(--accent-soft)`. Officer rows show name + ` rank · archetype` right-aligned in dim mono.
- Selecting an officer navigates to that officer's detail view.

---

## Interactions & Behavior

- **Tab nav** — clicking a tab clears any selected officer and switches view. Tab counts come from data lengths.
- **Officer card click** — sets `selected = officer`, switches main pane to detail. Filter sidebar hides on detail (full width main + right metadata).
- **Back link in detail** — clears `selected`, returns to grid.
- **Roster filter** — re-filters the officer array. Sample roster keys: `default` (all), `minimal` (PLINY, DAEDALUS, ADA, VERA), `user-level` (excludes the orchestration internals), `custom` (empty start).
- **Archetype filter** — single-select; "All" clears.
- **⌘K** — opens palette, autofocuses input, Esc closes. Live filter on officer name+role and skill name+description (case-insensitive substring). Top 5 officers + top 4 skills shown.
- **Hover states** — cards lighten background to `var(--bg-app)` over 180ms. Buttons inherit color transition over 180ms.
- **Active states** — sidebar item fills `var(--accent-soft)`, text becomes `var(--accent)`.
- **Sort order in Team grid** — major → captain → lieutenant.

## State Management

Top-level state (in `App`):
- `tab: "team" | "skills" | "meta"`
- `selected: Officer | null`
- `paletteOpen: boolean`
- `roster: "default" | "minimal" | "user-level" | "custom"`
- `archetypeFilter: string | null`

In production: lift roster + filter to a query-string state hook so views are URL-shareable. Officer / skill / meta data should come from the codebase's data store; the prototype reads from `data.jsx`.

## Design Tokens

All defined in `tokens/colors_and_type.css` — import that and use the variables. Highlights:

**Surface / foreground:**
- `--bg-app` `#FAF9F6` (parchment)
- `--bg-surface` `#FFFFFF`
- `--bg-sunken` `#F2F0EB`
- `--bg-inset` `#ECE9E1`
- `--fg-1` `#1B1A17` · `--fg-2` `#45433E` · `--fg-3` `#76736B` · `--fg-4` `#A6A39B`
- `--border-1` `#E4E1D8` · `--border-2` `#D4D0C5` · `--border-3` `#BFBAAD`

**Accent (primary action / link):**
- `--accent` `#2B4A7F` (deep ink-blue)
- `--accent-hover` `#233C68`
- `--accent-soft` `#E6EBF3`

**Archetype accent colors** (used as left-border on officer cards + dot in filter sidebar + ArchetypeText color):
| Archetype | Hex |
|---|---|
| orchestrator | `#5B4D86` |
| architect | `#2E6E63` |
| verifier | `#785637` |
| executor | `#4A6E2E` |
| reviewer | `#6E2E4A` |
| plan-critic | `#6E4A2E` |
| researcher | `#2E4A6E` |
| curator | `#4A2E6E` |
| intake | `#6E6E2E` |
| scout | `#2E6E4A` |

**Type:**
- Display / UI: `Inter` (substitute — final font TBD).
- Mono: `JetBrains Mono` (substitute — final font TBD).
- Type ramp lives in `colors_and_type.css` as `--text-xs … --text-3xl`.

**Radius:** 3 (chip) · 4 (chip large) · 6 (button / sidebar item) · 10 (card / modal) · 999 (rank pill).

**Shadow:**
- Card: `0 1px 2px rgba(20,18,12,0.04)`
- Modal: `0 4px 12px rgba(20,18,12,0.07), 0 12px 32px rgba(20,18,12,0.05)`

**Motion:** all transitions `180ms` cubic-bezier default.

## Assets

- `assets/mark.svg` — placeholder columnar mark. **Replace with the real brand mark.**
- `assets/wordmark.svg` — placeholder wordmark. **Replace.**
- `assets/peristyle.svg` — decorative pattern, currently unused in the click-thru.
- Icons in the prototype are inline SVGs in `Components.jsx > Icon`. **For production, use [Lucide React](https://lucide.dev) — every icon used (`users`, `package`, `file`, `search`, `edit`, `copy`, `code`, `plus`, `arrow-right`, `x`, `filter`, `settings`, `check`) maps 1:1 to a Lucide name.** Stroke width 2, `currentColor`.

## Files

- `ui/index.html` — entry point. Open this in a browser to see the live design.
- `ui/App.jsx` — top-level shell: Header, FilterSidebar, TeamView, OfficerDetail, SkillsView, MetaView, App.
- `ui/Components.jsx` — reusable: Icon, Mark, Button, RankPill, ArchetypeText, Chip, OfficerCard, SkillCard, CommandPalette.
- `ui/data.jsx` — sample roster, skills, meta-aspects, archetype color map, sample officer body markdown. Use this as the schema reference — production should mirror these field names.
- `tokens/colors_and_type.css` — all design tokens. Import or port into your codebase's token system.
- `tokens/DESIGN_SYSTEM.md` — broader brand context (voice, content fundamentals, visual foundations, iconography).
- `assets/` — logos + decorative pattern.

## Notes for the implementer

- **Voice / copy** — UI strings (button labels, empty states, error messages) should follow the **Content Fundamentals** section in `tokens/DESIGN_SYSTEM.md`: sentence case, no exclamation marks, no emoji, terse and declarative. "New agent" not "Create New Agent!".
- **Officer / skill schemas** — `data.jsx` is the schema reference. Field names (`rank`, `archetype`, `tools`, `lieutenants`, `reading`, `tier`) are load-bearing; align the production data layer to them.
- **Don't add** decorative gradients, glassmorphic blurs (except command palette backdrop), drop shadows beyond what's tokenized, rounded-left-border-only "tip cards", or emoji.
- **Density** — this is a power-user tool. Don't inflate paddings. Match the prototype's spacing exactly.
