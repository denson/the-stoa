# The Stoa: agent-character-builder

> *Where teams of AI agents are designed, not assembled.*

A web app for browsing, composing, and authoring AI agent teams. Building agents *with* character — distinct roles, personalities, disciplines — not stupid robots.

The data layer is [agent-team-team](https://github.com/denson/agent-team-team) (JSON metadata + markdown bodies). This app is the visual + interactive layer on top.

## Status

**v0.1 — alpha.** Visual click-thru complete: Team browse, Officer detail, Skill library, Meta-aspects, ⌘K command palette. Inline sample data; v0.2 wires to agent-team-team's real `definitions/` tree.

## Quickstart

```bash
git clone https://github.com/denson/agent-character-builder
cd agent-character-builder
npm install
npm run dev
```

Open http://localhost:5173/ — should see the 12-officer roster grid. Click any officer for the detail view (markdown body + metadata sidebar). Cmd+K (or Ctrl+K) opens the command palette.

## Stack

- React 19 + TypeScript
- Vite 6 (with `@vitejs/plugin-react-swc`)
- lucide-react (icons)
- Inline styles + design tokens (CSS custom properties) — see [src/styles/tokens.css](./src/styles/tokens.css). v0.2 may refactor to Tailwind.

## Three views

1. **Team Overview** — 12-officer card grid, filtered by roster (`default` / `minimal` / `user-level` / `custom`) and archetype. Sorted major → captain → lieutenant.
2. **Officer Detail** — full markdown body, sidebar metadata (tools, callable lieutenants, required reading, model tier, body path). Edit / Clone / View JSON / Add to roster actions.
3. **Skill Library** — 10 skills shown as cards with `callable_by` chips. Filter + click to drill.

Plus a **⌘K command palette** for cross-cutting search (officers + skills).

## Origin

This repo descends from agent-character-sheets (v1, archived). The v1 was a read-only display of officer cards from a sibling agent-gauntlet repo. The Stoa is a deeper rework: multi-view, interactive, designed in [Claude Design](https://www.anthropic.com/news/claude-design-anthropic-labs) before any code was written, then implemented against the design handoff bundle.

The agent team that lives in `<this-repo>/.claude/agents/` is deployed by [agent-team-team](https://github.com/denson/agent-team-team)'s `bootstrap.py`. Project-level officer names are suffixed: `MAJOR_PLINY_agent_character_builder`, `DAEDALUS_agent_character_builder`, etc.

## Repository structure

```
agent-character-builder/
├── BRIEF.md                              project brief (input to Claude Design)
├── DESIGN_PRINCIPLES.md                  aesthetic + UX rules
├── design_handoff_character_builder/     Claude Design output (preserved as design reference)
│   ├── README.md                         how to recreate the design in production code
│   ├── assets/                           SVG logo + wordmark + peristyle pattern
│   ├── tokens/                           design system docs + CSS tokens
│   └── ui/                               original JSX prototype (read-only reference)
├── data-samples/                         data shape examples from agent-team-team
├── public/                               static assets served by Vite
├── src/
│   ├── App.tsx                           top-level shell + views
│   ├── Components.tsx                    reusable UI primitives + palette
│   ├── data/
│   │   ├── types.ts                      TypeScript interfaces (Officer, Skill, MetaAspect)
│   │   └── sample.ts                     inline sample data (replaced by data.json in v0.2)
│   ├── styles/
│   │   ├── index.css                     base + token import
│   │   └── tokens.css                    design tokens (colors, type, spacing)
│   ├── main.tsx                          entry point
│   └── vite-env.d.ts
└── (.claude/, agents/, skills/, team-definition.json — agent team substrate, gitignored)
```

## v0.1 → v0.2 roadmap

- **Wire to real data.** Replace `src/data/sample.ts` with a fetch to `/data.json` built at build-time from agent-team-team's `definitions/` tree by a `scripts/gen-data.ts` Node script. Add a field-name adapter (`callable_lieutenants` → `lieutenants`, `model_tier` → `tier`, `required_reading` → `reading`).
- **URL-shareable state.** Move `roster`, `archetypeFilter`, `selected` into URL query string via `react-router` so `/officer/MAJOR_PLINY_agent_character_builder?roster=default` is a valid link.
- **Compose-team wizard.** The "New agent" CTA in the header opens a multi-step flow: pick base roster → apply work-class adjustments → configure project metadata → preview deploy → deploy. Underlying call: shells out to `bootstrap.py`.
- **Author-agent form.** Form-driven officer / skill creation. Writes back to agent-team-team's `definitions/officers/<NAME>.json` + `definitions/bodies/<name>.md`.
- **Tailwind refactor.** Move inline styles to Tailwind utility classes (or CSS modules) for maintainability. Design tokens become Tailwind theme extensions.
- **Real brand fonts + logo.** The handoff uses Inter + JetBrains Mono as substitutes; logo SVG is a placeholder columnar mark. Swap when finals ship.

## Authorship

Denson Smith. KnowledgeCrystal · The Stoa.
