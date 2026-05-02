# onboarding-v1 — project inventory

**Author:** Denson Smith (via DAEDALUS_agent_character_builder, dispatched by Major Pliny under `tier2-project-onboarding` Phase 2 of 3).
**Project:** The Stoa: agent-character-builder, v0.1 alpha.
**Working dir:** `C:/Users/denso/claude_projects/agent-character-builder/`.
**Sibling repo:** `C:/Users/denso/claude_projects/agent-team-team/`.
**Inputs consumed:** `agents/design/onboarding-v1/daedalus-brief.md` (Major Pliny + the Colonel); the repo itself (read end-to-end where shape was load-bearing). No upstream researcher artifact.

---

## Restatement

The Colonel and Major Pliny want a single 5-minute-readable inventory artifact that captures: (a) the meta-product framing of agent-character-builder, (b) what shipped in v0.1 alpha with concrete paths, (c) where v0.1 is rough, (d) the full v0.2 work-arc catalog (the README's six arcs plus the Colonel's three additions = nine arcs) with explicit dependencies between arcs, (e) my analysis of the Colonel's recommended first-three-arc ordering, and (f) any Tier-0 capability requests that aren't in the project itself yet. The artifact's purpose is to serve as the shared reference Major Pliny + the Colonel will use in Phase 3 to pick which arc to dispatch first.

**Imported assumptions (declared so they can be challenged):** the Colonel's three gap-fill answers in the brief — generator-side adapter, single-user-localhost audience for v0.2, defer CI to v0.3 — are load-bearing inputs, not re-litigated here. Phase 1 survey claims by Major Pliny are taken as load-bearing context but cross-checked against the repo. The README's roadmap is taken as authoritative on the original six arcs.

---

## §1 — What this project IS

**The Stoa: agent-character-builder is a power-user web app whose domain object is the same kind of agent team that builds it.** It is a meta-product: developers / AI engineers / researchers use it to browse, compose, and author multi-agent teams (officers + skills + meta-aspects) defined in the sibling [`agent-team-team`](https://github.com/denson/agent-team-team) Python toolkit, and the agent team that authors *this* app — twelve officers deployed under `.claude/agents/` with `_agent_character_builder` suffixes, who routine work through Major Pliny / the Colonel — is itself a `bootstrap.py` deployment of that toolkit. The visual + interactive layer (this repo) wraps the data + deploy layer (`agent-team-team`); the app exists so a user can see a team before they ship one.

---

## §2 — Current artifacts (v0.1 alpha)

**Stack:** React 19 + Vite 6 + TypeScript 5.7 (`@vitejs/plugin-react-swc`), `lucide-react` for icons, inline styles + CSS custom properties for design tokens. Three npm scripts: `dev` (vite), `build` (`tsc -b && vite build`), `preview` (vite preview). `typecheck` script available (`tsc -b --noEmit`). `package.json` carries no test framework, no router, no form library, no markdown library — the lean v0.1 surface. (`package.json`)

**App shell.** Single `src/App.tsx` (1,059 lines) hosts all four screens — `Header`, `FilterSidebar`, `TeamView`, `OfficerDetail` (with hand-rolled `BodyMarkdown` + `InlineMD` mini-parser), `SkillsView`, `MetaView`, `CommandPalette` — plus the top-level `App` component that owns local state (`tab`, `selected`, `paletteOpen`, `roster`, `archetypeFilter`). Reusable primitives — `Button`, `Chip`, `RankPill`, `OfficerCard`, `SkillCard`, `Mark` (placeholder logo), `ArchetypeText`, the `palette` constant — live in `src/Components.tsx` (386 lines). Entry point `src/main.tsx`.

**Three views + ⌘K palette.**
- **Team Overview** — 12-officer card grid with roster picker (`default` / `minimal` / `user-level` / `custom`) and archetype filter, sorted major → captain → lieutenant. Roster definitions are hardcoded in `App.tsx` lines 998–1003, not data-driven.
- **Officer Detail** — two-pane: rendered markdown body on the left (hand-rolled renderer in `App.tsx` lines 310–457; supports `#`/`##` headings, `1.`-numbered lists, inline `` ` ``-code, `**bold**` — no code blocks, links, tables, or `###`+ headings), metadata sidebar on the right with chips for tools / lieutenants / required reading and a model-tier line. Action buttons (Edit / Clone / View JSON / Add to roster) are wired to no handlers.
- **Skill Library** — 10-skill card grid with `callable_by` chips. No filter UI yet (despite `BRIEF.md` calling for `callable_by` and `kind` filters).
- **Meta-aspects** — read-only card list of 4 entries (envelope-lifecycle, inter-agent-comms, fix-now-discipline, discipline-catalog). No drilldown view.
- **⌘K palette** — global cross-cutting search across officers + skills, ⌘/Ctrl-K to open, Esc to close, click-row to navigate.

**Inline sample data.** All three views read from `SAMPLE_DATA` in `src/data/sample.ts` (152 lines) — 12 officers, 10 skills, 4 meta-aspects, archetype color map, and a single `bodyPreview` string used as the body for *every* selected officer (`App.tsx` line 1039). Type interfaces in `src/data/types.ts` (`Officer`, `Skill`, `MetaAspect`, `StoaData`, `Archetype` union, `Rank` union).

**Design tokens.** `src/styles/tokens.css` defines a complete light + dark token set (surfaces, text, borders, accent, rank coding, archetype hints, shadows, radii, spacing, type scale, motion) plus `:root[data-theme="dark"]` and `.theme-dark` overrides. Three font families requested via Google Fonts: Inter (sans), JetBrains Mono (mono), Cormorant Garamond (serif, "sparingly for editorial flourishes"). `src/styles/index.css` imports tokens.

**Design-handoff bundle.** `design_handoff_character_builder/` (preserved as design reference per its own README, JSX prototype is read-only): `assets/` (SVG logo + wordmark + peristyle pattern), `tokens/` (design system docs + CSS tokens), `ui/` (original JSX prototype). `Components.tsx`'s comment block explicitly notes that inline styles are preserved for pixel-perfect parity with this prototype.

**Deployed agent team.** `.claude/agents/` carries 12 officers, all suffixed `_agent_character_builder`: ADA, ARGUS, CAPTAIN_PLINY, CATO, CURATOR, DAEDALUS, HERALD, MAJOR_PLINY, NESTOR, SCOUT, STRABO, VERA. Deployment manifest at `team-definition.json` (project-level, scope `default`, work_class `mixed`). Bootstrap was performed by sibling `agent-team-team/bootstrap.py`.

**Team-meta-aspects substrate.** `agents/aspects/_meta/` carries seven canonical docs (verified by directory listing): `design-time-tool-validation.md`, `discipline-catalog.md`, `envelope-lifecycle.md`, `fix-now-discipline.md`, `inter-agent-comms.md`, `pair-programmer-disciplines.md`, `pliny-dispatch-economy.md`.

**Skills substrate.** `skills/` carries 15 skills (verified): `1password-secrets`, `arc-management`, `cite-check`, `copy-artifact`, `dispatch-lieutenant`, `edit-json`, `format-validate`, `pulse-review`, `runner`, `save-verdict`, `spawn-pair-programmer`, `team-status`, `tier2-project-onboarding`, `tier2-task-routing`, `transcribe-bw-to-disk`. (Sample data ships only 10 of these as cards; see §3.)

**Data-shape examples.** `data-samples/` carries representative real-shape JSON for `officers/` (5 examples), `skills/` (4 examples), `meta-aspects/` (3 examples), `bodies/` (4 markdown files). These are the schema-truth references the v0.2 adapter will target.

**Key docs.** `README.md` (project overview + roadmap), `BRIEF.md` (Claude Design input — primary feature spec including the four supporting views not yet built), `DESIGN_PRINCIPLES.md` (aesthetic + UX rules — explicitly calls dark mode first-class).

---

## §3 — Current gaps

These are the seeds for §4. Each gap is verified against the source, not just the brief.

1. **Schema divergence between design shape and real shape.** `src/data/types.ts` uses `tier`, `lieutenants`, `reading`, archetype-without-suffix (`"architect"`); `data-samples/officers/DAEDALUS.json` uses `model_tier`, `callable_lieutenants`, `required_reading`, archetype-with-suffix (`"architect-archetype"`), plus `body_path` and `consult_on_demand` fields the design types don't model. No adapter yet. (`src/data/types.ts` vs `data-samples/officers/DAEDALUS.json`)

2. **No real-data pipeline.** `src/data/sample.ts` is the only data source; `scripts/gen-data.ts` does not exist (verified — `scripts/` directory absent). `public/` exists but holds no `data.json`.

3. **Dark mode tokens defined but not wired.** `src/styles/tokens.css` lines 131–173 carry a complete dark token set under `:root[data-theme="dark"], .theme-dark`. **No code in `src/` sets `data-theme`, no `prefers-color-scheme` media query, no theme toggle, no theme provider.** (`grep -E "data-theme|prefers-color-scheme|matchMedia" src/` returned no matches.) Furthermore, the `palette` constant in `src/Components.tsx` (lines 29–53) hardcodes the *light-mode hex values* as JS constants, and inline styles throughout `App.tsx` and `Components.tsx` reference `palette.bgApp` / `palette.fg1` / etc. directly rather than CSS variables. This means dark mode cannot ship by toggling `data-theme` alone — it requires either replacing `palette.X` references with `var(--X)` in inline styles, OR a dual-palette switch wired through React context. (Load-bearing for arc dependency analysis in §4.)

4. **Accessibility absent across the board.** `grep -E "aria-|role=|tabIndex|onKeyDown|onKeyPress" src/` returned **no matches**. Concrete gaps:
   - **Divs-as-buttons** — tab bar (`App.tsx` lines 124–153), filter sidebar items (lines 215–240), command-palette rows (lines 875–911 + 932–965), "← Back to Team" (lines 564–577) are all `<div onClick={…}>`. No keyboard activation, no focus, no role.
   - **Missing semantic landmarks.** `<aside>` is used for `FilterSidebar` and `DetailSidebar`; `<header>` is used; `<main>` and `<nav>` are absent.
   - **No focus management on view changes.** Switching tabs or selecting an officer doesn't move focus.
   - **No `aria-live` on the command palette** — search results appear/disappear silently.
   - **No `aria-pressed` / `aria-current` on tab indicators or filter chips.**
   - **Markdown content has no `prose` wrapper / heading hierarchy** beyond hand-rolled `<h2>` / `<h3>`; the page-level `<h1>` for "Team Overview" coexists with body-rendered `<h2>` headings without semantic nesting awareness.

5. **No test scaffold.** No `vitest.config.ts`, no `*.test.ts(x)` files, no test directory, no `@testing-library/react` in `package.json`.

6. **No CI.** `.github/` directory absent. No workflows, no lint config, no automated `tsc` / `vite build` enforcement.

7. **No URL-shareable state.** `tab`, `selected`, `roster`, `archetypeFilter`, `paletteOpen` are all local React state in `App.tsx`. No `react-router` (or `wouter`, or hand-rolled router) in `package.json` or `src/`.

8. **No compose-team flow.** `Header` renders a "New agent" CTA (`App.tsx` line 113) but it has no `onClick`. The five-step wizard described in `BRIEF.md` §4 doesn't exist.

9. **No agent-author form.** The "Edit / Clone / Add to roster" buttons on Officer Detail (`App.tsx` lines 615–628) have no handlers. Tabs for "New officer" / "New skill" / "New meta-aspect" described in `BRIEF.md` §5 don't exist.

10. **Brand assets are placeholders.** Logo is the columnar `Mark` SVG in `Components.tsx` lines 58–69 (placeholder per its own comment). Fonts are Google-Fonts-served Inter + JetBrains Mono substitutes per `tokens.css` line 7 + README §Stack. No wordmark integrated. `design_handoff_character_builder/assets/` carries the design-side SVGs but they're not pulled into `src/`.

11. **Inline styles throughout.** Every component in `App.tsx` and `Components.tsx` is styled via `style={{ … }}` literals; there's no Tailwind, CSS-modules, or styled-components. Tokens live in `tokens.css` but most code references them via the duplicate `palette` JS constant rather than `var(--…)`. `Components.tsx` line 1–4 explicitly notes inline styles are preserved for pixel-fidelity with the design handoff.

12. **Hand-rolled markdown renderer (subtle gap).** `App.tsx` lines 310–457 ship a 150-line `BodyMarkdown` + `InlineMD` parser that supports `#` / `##`, numbered lists, inline `` ` ``-code, and `**bold**` — and nothing else. Code blocks (triple-backtick), bullet lists, links, tables, horizontal rules, headings beyond `##`, blockquotes are all unrendered. Real officer bodies include all of these. v0.2 wiring will surface this gap immediately.

13. **`bodyPreview` is one shared string for all officers (subtle gap).** `App.tsx` line 1039 passes `data.bodyPreview` to `OfficerDetail` regardless of which officer was selected. Every officer's "body" in v0.1 is the same DAEDALUS-flavored placeholder text; only the `{{OFFICER_NAME}}` / `{{NICKNAME}}` placeholder substitution differs.

14. **Sample data has narrower coverage than canonical (subtle gap).** Sample has 10 skills + 4 meta-aspects; the deployed substrate has 15 skills + 7 meta-aspects (verified by listing `skills/` and `agents/aspects/_meta/`). v0.2 wiring will surface 5 additional skills and 3 additional meta-aspects.

15. **Roster definitions are hardcoded in the React app (subtle gap).** `App.tsx` lines 998–1003 hand-codes `minimal` / `user-level` / `default` / `custom` as literal name lists. `team-definition.json` carries the deployed roster but no roster-definition catalog. v0.2's adapter scope must decide: do roster definitions come from `agent-team-team/`, or do they remain in the React app?

---

## §4 — v0.2 work-arc catalog (9 arcs)

The README's roadmap names six arcs; the Colonel added three (#7 dark mode, #8 a11y, #9 Vitest scaffold). All nine are in scope for v0.2 by the brief.

### Arc #1 — Real-data wiring + adapter

`scripts/gen-data.ts` is added (Node script run via `tsx` or compiled, hooked into `npm run build` as a prebuild step). Reads `../agent-team-team/definitions/` (default) or `$AGENT_TEAM_TEAM_PATH/definitions/` (override), walks `officers/*.json` + `skills/*.json` + `meta-aspects/*.json` + `bodies/*.md`, applies the field-name remap (`model_tier` → `tier`, `callable_lieutenants` → `lieutenants`, `required_reading` → `reading`, archetype `"X-archetype"` → `"X"`), composes per-officer body text from `body_path`, emits `public/data.json` (or similar) in the existing design-shape `StoaData` format. App switches from `import { SAMPLE_DATA } from "./data/sample"` to `await fetch("/data.json")` with a loading state. **Dependencies:** none upstream — this is the substrate-establishment arc. **Downstream blockers for:** #3, #4, #9 (and any later arc that wants to assert against real officer/skill counts).

### Arc #2 — URL-shareable state

`react-router` (or `wouter` if want lighter) added to `package.json`. Routes: `/` (Team Overview), `/officer/<NAME>` (Officer Detail), `/skill/<name>` (Skill Detail when it exists), `/meta` (Meta-aspects). Query params: `?roster=<id>&archetype=<id>`. `tab` / `selected` / `roster` / `archetypeFilter` move from local state to URL-derived state via `useParams` / `useSearchParams`. `paletteOpen` stays local (modal state, not shareable). Browser back/forward works; refreshing on a deep link lands on the right view. **Dependencies:** independent of #1 in principle — could land first against sample data — but landing #1 first means tests written under #9 can exercise routing against real data shape. **Downstream blockers for:** #3, #4 (both wizards / forms benefit from routable steps).

### Arc #3 — Compose-team wizard

Multi-step flow behind the "New agent" CTA. Five steps per `BRIEF.md` §4: roster pick → work-class adjustments → project metadata form → preview diff → deploy via `bootstrap.py` subprocess. Final step shells out (`child_process.spawn` from a thin Node bridge OR direct `fetch` against a future tiny backend; for v0.2 single-user-localhost the Colonel approved subprocess). Wizard state probably lives in URL (`/compose/<step>`) plus a Zustand-or-similar store for cross-step form data. **Dependencies:** **arc #1 (schema substrate)** — wizard preview needs the real officer-roster shape. **Arc #2 (routing)** — wizard steps want their own URLs. **Should not run concurrently with #5 (Tailwind)** since the wizard adds many new components and Tailwind refactors all components.

### Arc #4 — Agent-author form

Form-driven officer / skill / meta-aspect creation per `BRIEF.md` §5. Tabs for "New officer" / "New skill" / "New meta-aspect"; per-form fields validate; markdown body editor with raw + preview tabs; on save, writes back to `agent-team-team/definitions/officers/<NAME>.json` + `agent-team-team/definitions/bodies/<name>.md`. Same subprocess-pattern question as #3: write directly via Node fs (single-user-localhost is OK) or via a thin backend. **Dependencies:** **arc #1 (schema substrate)** — form fields enumerate from the canonical archetypes / tools / meta-aspects. **Arc #2 (routing)** — `/author/officer/new` etc. **Should not run concurrently with #5** for the same reason as #3.

### Arc #5 — Tailwind refactor

Inline styles → utility classes (or CSS modules, if the project decides to skip Tailwind). Design tokens become Tailwind theme extensions (`tailwind.config.ts` references `tokens.css` custom properties). Touches every file in `src/` — `App.tsx`, `Components.tsx`, every view. The `palette` JS constant in `Components.tsx` either disappears (replaced by Tailwind classes pulling from CSS vars) or shrinks to non-style helpers. **Dependencies:** independent of #1–#4 in principle (no shared shape), but **touches every component file** so should not run concurrently with arcs that add components (#3, #4) or refactor component shape (#8 a11y). **Strong synergy with #7 dark mode** — see arc #7 dependency note below.

### Arc #6 — Real brand assets

Final fonts (license + load), final logo SVG (replace `Mark` placeholder), final wordmark, integrate per the design-handoff bundle's `assets/` reference. May involve self-hosting fonts (currently Google-Fonts-served per `tokens.css`). Touches `tokens.css` (font families), `Components.tsx` (`Mark` component), and adds `public/fonts/` if self-hosted. **Dependencies:** independent of all other arcs; mostly an asset-swap. Can land at any time; least sensitive to ordering.

### Arc #7 — Dark mode (Colonel-added)

Wire the dark token set already in `tokens.css`: add a theme toggle (header-icon button), respect `prefers-color-scheme: dark` on first load, persist user choice to `localStorage`, set `data-theme` on `<html>` / `<body>`. **The non-trivial part** (per §3 finding #3): inline styles in `App.tsx` / `Components.tsx` reference the JS `palette` constant which holds light hex values. To switch to dark cleanly, those `style={{ background: palette.bgApp }}` references must become either `style={{ background: "var(--bg-app)" }}` (CSS-variable mode) or use a `useTheme()` hook that returns the right palette. Either way, **arc #7 includes a CSS-variable-or-context refactor of inline styles**, which means **arc #7 partially overlaps with arc #5** (Tailwind, which would do the inline-style refactor anyway via utility classes). **Two viable orderings:**
- **(a)** Land #5 (Tailwind) first; #7 then collapses to a token-toggle + `prefers-color-scheme` wire-up (small).
- **(b)** Land #7 with a narrower CSS-variable refactor of inline styles only (no Tailwind); #5 later replaces that with utility classes.

The Colonel's recommended ordering does **(b)** by combining #7 with #8 in the third batch. Defensible (see §5 analysis).

### Arc #8 — Accessibility pass (Colonel-added)

Replace divs-as-buttons with `<button>` elements (tab bar, filter sidebar items, command-palette rows, "Back to Team"); add `<main>` / `<nav>` semantic landmarks; add `aria-label` / `aria-pressed` / `aria-current` where appropriate; manage focus on view changes (move focus to `<main>` heading, or to a known target); add `aria-live="polite"` to the command-palette results list; ensure keyboard nav works (Tab through cards, Enter to drill, Esc to back out per `DESIGN_PRINCIPLES.md` §Interactions). **Dependencies:** **shares touch surface with #5 (Tailwind)** — both rewrite every component — so the two should be sequential, not concurrent. **Synergistic with #7 (dark mode)** — both are component-level polish work. **Should land before #3 / #4** so the new wizard / form components are built a11y-correct from the start (cheaper than retrofitting).

### Arc #9 — Vitest scaffold (Colonel-added)

Add `vitest`, `@testing-library/react`, `@testing-library/jest-dom`, `jsdom` to `devDependencies`; `vitest.config.ts` (or extend `vite.config.ts`); `npm test` script; first tests against the **gen-data adapter from arc #1** (input: `agent-team-team/definitions/X.json` fixture, output: `StoaData` shape, assert field rename worked). **Dependencies:** **arc #1 must exist for the scaffold to have a meaningful first test target**; the brief explicitly couples #1 + #9 in batch 1. Future arcs pick up component tests (a11y assertions for #8, routing assertions for #2, wizard-step assertions for #3 / #4).

### Inter-arc dependency summary

```
#1 (real-data + adapter) ─────────► #3 (wizard), #4 (author form), #9 (vitest)
#2 (URL state)            ─────────► #3 (wizard), #4 (author form)
#5 (Tailwind)             ◄─sequential─► #8 (a11y); pre-requisite for clean #7 (dark mode)
                                       — do NOT run concurrently with #3, #4, #8
#7 (dark mode)            ─────────► strong synergy with #5; if #5 lands first, #7 is small
#8 (a11y)                 ─────────► sequential with #5; should precede #3 / #4
#6 (brand assets)         ─────────► no dependencies; can land any time
#9 (vitest scaffold)      ─────────► depends on #1 for first meaningful test
```

---

## §5 — Recommended first three arcs

The Colonel proposed the following ordering. **I default to it; my analysis below confirms the ordering is sound, with one caveat I want flagged for the third batch.**

### Batch 1 — Arcs #1 + #9: gen-data + adapter + Vitest scaffold (combined)

**Why this ordering is sound.** Arc #1 is the substrate everything else needs; landing it first means all subsequent arcs can assume real data shape. Bundling #9 with #1 means the Vitest scaffold gets exercised immediately by the most-testable thing in the codebase: a pure I/O transform with deterministic input and output. Adapter tests are the easy on-ramp for a test culture; setup costs amortize across all later arcs.

**Scope sketch.**
- Add `scripts/gen-data.ts` (Node script, uses `node:fs/promises` + `node:path`).
- Add adapter logic: read `definitions/officers/*.json`, `definitions/skills/*.json`, `definitions/meta-aspects/*.json`, `definitions/bodies/*.md`; apply field-name remap; archetype-suffix strip; compose `StoaData` shape; emit `public/data.json` (build-time) or `src/data/generated.ts` (compile-time embed — pick one, brief leaves it open).
- Wire env var `AGENT_TEAM_TEAM_PATH` with default `../agent-team-team`.
- Switch `App.tsx` from `import { SAMPLE_DATA }` to `await fetch("/data.json")` with a `<LoadingSkeleton />` and error boundary.
- Add `vitest`, `@testing-library/react`, `@testing-library/jest-dom`, `jsdom` to devDependencies.
- `vitest.config.ts` (or merge into `vite.config.ts`).
- First test file: `scripts/gen-data.test.ts` — feed in a fixture officer JSON, assert output matches `StoaData['officers'][0]` shape.

**Out of scope.** Per-officer body markdown rendering improvements (gap §3.12) — touch surface invites scope creep. Roster-definitions-from-real-data (gap §3.15) — preserve current hardcoded rosters; arc #3 (wizard) is the natural place to revisit.

**Key files touched.** `package.json` (deps + scripts), `vite.config.ts` or new `vitest.config.ts`, `scripts/gen-data.ts` (new), `scripts/gen-data.test.ts` (new), `src/data/sample.ts` (deleted or marked deprecated), `src/App.tsx` (data-loading), `public/data.json` (new build artifact), `.gitignore` (probably ignore `public/data.json` since it's generated). Possibly `tsconfig.json` (if `scripts/` needs a separate tsconfig for Node).

**Success criteria.**
- `npm install && npm run build && npm run dev` against a clean clone (with `agent-team-team` at sibling path) shows the same 12-officer / 15-skill / 7-meta-aspect roster the deployed `.claude/agents/` reflects — no inline sample data referenced.
- `npm test` runs the adapter test suite green.
- Setting `AGENT_TEAM_TEAM_PATH=/some/other/path` overrides the source location.
- Field-name remap is unit-tested end-to-end (input `model_tier`, output `tier`; etc.).
- TypeScript compiles (`npm run typecheck` exits 0).
- Existing UI behavior is unchanged for the user (rosters / filters / officer detail still render).

**Rough effort estimate:** **M** (medium). The adapter logic is small and pure; the Vitest scaffold is mechanical; the data-loading refactor in `App.tsx` is the biggest piece (loading state, error handling, switching from sync `SAMPLE_DATA` to async fetch). Probably 1–2 work cycles.

**Officer pipeline shape:** **full pipeline** — design (DAEDALUS) → critique (ARGUS) → build (ADA) → verify (VERA) → review (CATO). Justification: this arc establishes the data substrate every later arc depends on; a schema-shape regression here is catastrophic for everything downstream. Full-pipeline insurance is warranted for the substrate-establishment arc. (Note: the Colonel may choose to compress to design + build + verify if confidence is high; my recommendation is full pipeline for the foundation, lighter pipelines for later arcs.)

### Batch 2 — Arc #2: URL-shareable state (react-router)

**Why this ordering is sound.** With the data substrate landed, the next-most-leveraged change is making the app's state shareable — enables the v0.2 sharing-with-early-users scenario the Colonel called out, and unblocks #3 / #4 which both want routable steps. Doing this before #3 / #4 means those wizards/forms are built routing-aware from the start, avoiding a retrofit.

**Scope sketch.**
- Add `react-router-dom` to `package.json`.
- Wrap `App` in `<BrowserRouter>` (or `<HashRouter>` if simpler for static deploy).
- Routes: `/` → Team Overview, `/officer/:name` → Officer Detail, `/skill/:name` → Skill Detail (placeholder if not yet built), `/meta` → Meta-aspects, `/meta/:name` → Meta-aspect Detail (placeholder).
- Query params: `?roster=default&archetype=architect`.
- `useParams` / `useSearchParams` replace local state for `tab` / `selected` / `roster` / `archetypeFilter`.
- `paletteOpen` stays in local state (modal, not shareable; explicit choice).

**Out of scope.** The skill / meta-aspect detail pages themselves — placeholder routes are fine for now; v0.3 or a follow-up arc fleshes them out. Server-side rendering — single-user-localhost doesn't need it.

**Key files touched.** `package.json`, `src/main.tsx` (Router wrapper), `src/App.tsx` (massive — most of the arc's churn lives here), possibly `src/Routes.tsx` (new) if the route table is extracted.

**Success criteria.**
- `/officer/MAJOR_PLINY?roster=default` loads directly to MAJOR_PLINY's detail with the default roster active.
- Browser back/forward navigates view stack correctly.
- Refreshing any URL lands on the same view.
- ⌘K palette navigates by setting URL, not local state.
- `npm test` adds at least one route-resolution test (e.g., `/officer/X` renders the right officer).

**Rough effort estimate:** **M** (medium). `react-router` integration in a single-file App is mostly mechanical, but the state migration touches every screen.

**Officer pipeline shape:** **full pipeline** — routing changes are user-visible across every view; CATO's review on link-share UX matters here.

### Batch 3 — Arcs #7 + #8: dark mode + accessibility (combined)

**Why this ordering is sound — with caveat.** Both arcs touch every component file, and bundling them lets a single rewrite pass through the codebase pay both costs at once. Dark mode and a11y also share an audience: the same "small circle of early users" who'll share screenshots and links will also include people who notice when buttons aren't real buttons.

**Caveat — load-bearing for the design.** The clean way to ship dark mode requires the inline styles to stop hardcoding light hex values from the `palette` JS constant (gap §3.3). There are two viable paths:

- **(a) Do a CSS-variable-only refactor inside this batch** — replace `style={{ background: palette.bgApp }}` with `style={{ background: "var(--bg-app)" }}` throughout `App.tsx` + `Components.tsx`, drop most of the `palette` JS constant, then dark mode is "set `data-theme`". This is the path the Colonel's ordering implies. Cost: medium. Risk: visual regressions during the refactor; tight diff review needed.
- **(b) Land #5 (Tailwind) first**, get utility-class styling for free, then dark mode is `dark:` variants. Cost: high (full Tailwind migration is its own arc). Risk: defers dark mode further.

The Colonel chose **(a)** by putting dark mode + a11y in batch 3 ahead of Tailwind. **I default to that choice** — Tailwind is a larger swing and shouldn't gate a small dark-mode win — but **the design step for batch 3 must explicitly call out the inline-style → CSS-variable refactor as in-scope**. If it's left implicit, the executor will discover mid-build that dark mode "doesn't work" because hex values are hardcoded, and the arc spirals.

**Scope sketch.**
- **CSS-variable refactor.** Replace `palette.X` references in inline styles with `var(--X)` (or shrink `palette` to a thin wrapper). `Components.tsx` line 29–53 is the centroid.
- **Dark mode toggle.** Header gets a sun/moon icon button (lucide-react has both). Click toggles `data-theme="dark"` on `<html>`. Persist in `localStorage`. First-load reads `prefers-color-scheme`.
- **a11y refactor — divs-as-buttons.** Tab bar (`App.tsx` 124–153), `FilterSidebar` items (215–240), command-palette rows (875–965), "Back to Team" link (564–577) become real `<button>` (or `<a>` for the back link) elements. Strip `cursor: pointer`; add focus styles.
- **a11y refactor — semantic landmarks.** Wrap the main content in `<main>`. Wrap the tab bar in `<nav>`. Existing `<aside>` and `<header>` stay.
- **a11y refactor — focus management.** When tab changes or officer is selected, move focus to the new region's heading. When officer is deselected, focus returns to the just-clicked card.
- **a11y refactor — `aria-live` palette.** Wrap the palette result list in `aria-live="polite"`.
- **a11y refactor — `aria-pressed` / `aria-current`.** Tab indicators get `aria-current="page"`; filter chips get `aria-pressed="true|false"`.

**Out of scope.** Tailwind (that's arc #5). Markdown renderer overhaul (gap §3.12) — separate arc. Real brand fonts (#6).

**Key files touched.** `src/App.tsx` (heavy), `src/Components.tsx` (heavy), `src/styles/tokens.css` (light — maybe verify `[data-theme="dark"]` selector), `src/main.tsx` (theme initial-load logic), possibly `src/hooks/useTheme.ts` (new), possibly a small `src/a11y.test.tsx` for keyboard-nav assertions.

**Success criteria.**
- Theme toggle visible in header; clicking it switches to dark; persists across reload.
- `prefers-color-scheme: dark` is respected on first visit.
- Tab through the app with keyboard only — every interactive element is focusable, focus order is sane, focus indicators are visible.
- Screen reader (NVDA on Windows; VoiceOver on macOS for the Mac users in the early circle) reads tab-bar buttons as "Team, button, current page", filter items as buttons, palette as a live region.
- `npm test` adds at least three a11y assertions: `<button>` for tab bar, `<main>` landmark exists, palette has `aria-live`.
- Lighthouse / axe-core scan shows zero a11y violations.
- Visual regression: side-by-side screenshots of light and dark modes match the design-handoff dark-mode previews (if such previews exist; if not, eyeball against `tokens.css` semantic intent).

**Rough effort estimate:** **L** (large) — combined arc spans many files; the inline-style → CSS-variable refactor alone is a mechanical-but-tedious sweep, and the a11y work has design judgment in every component.

**Officer pipeline shape:** **full pipeline** — both dark mode and a11y are user-facing surface changes that touch every view; CATO's review on craft + accessibility matters; VERA verifies via screen-reader probes + Lighthouse runs.

---

## §6 — Tier-0 capability requests

Three capability gaps surfaced during inventory; one is load-bearing for arc #1, two are quality-of-life for the agent team operating in this project.

### (a) Aspect doc: "How this team uses the sibling `agent-team-team` repo" — load-bearing for arc #1

**Why.** Arc #1's adapter depends on a filesystem-path coupling (default `../agent-team-team`, override via `AGENT_TEAM_TEAM_PATH`) that is not documented anywhere in `agents/aspects/_meta/` or `BRIEF.md` or `README.md`. The brief calls this out explicitly. Without an aspect doc, every officer who touches data wiring (DAEDALUS at design, ADA at build, VERA at verify, CATO at review) re-derives the convention from the source code — exactly the duplication an aspect doc exists to prevent.

**Recommended shape.** New file `agents/aspects/_meta/sibling-agent-team-team-coupling.md`. Cover: where the sibling repo lives by convention, the env-var override, the field-name remap table (`model_tier` ↔ `tier`, etc.), the archetype-suffix strip rule, what files in `definitions/` the adapter reads, what the adapter does NOT do (e.g., does not modify the sibling repo — read-only at build time), and what the `bootstrap.py` subprocess relationship looks like for arcs #3 / #4.

**Owner.** This aspect doc itself is a small DAEDALUS design + ADA write task; could be folded into arc #1's design step (the design.md for arc #1 *is* the load-bearing description, and the aspect doc is its persistent home for future officers).

### (b) Skill / lieutenant: "Run vite/vitest under PowerShell-on-Windows-MSIX"

**Why.** The Colonel's environment is Windows + PowerShell + MSIX-installed Claude Desktop (per `~/.claude/CLAUDE.md` env notes). Vite's dev server is fine in bash; vitest with watch mode and Windows path handling can have wrinkles (CRLF line endings, path separators in snapshot tests, `node_modules/.vite/` permission quirks under MSIX sandboxing). The agent team will hit these the first time they run `npm test` or `npm run dev` from a non-bash shell.

**Recommended shape.** Either:
- A small skill `skills/run-frontend/SKILL.md` that wraps `npm run dev` / `npm test` invocations with the right shell context (forces `bash` via the Bash tool, sets `CI=true` for tests to disable watch, captures output to a known location), OR
- A lieutenant entry in the team-spec for "frontend-runner" callable by ADA / VERA, modeled on RUNNER but with frontend-specific defaults (vitest non-watch mode, vite preview port logging).

If the existing RUNNER skill (`skills/runner/SKILL.md`) already handles this cleanly via shell-string passthrough, this request collapses to a documentation note rather than a new skill. **Recommend: spike the existing RUNNER first; only build a new skill if a real wrinkle surfaces.**

### (c) Lieutenant: dev-server-spawning helper (background mode)

**Why.** Several arcs (especially #2 routing, #7 dark mode, #8 a11y) benefit from interactive testing — the verifier wants to spawn `npm run dev`, hit a URL, and probe behavior, then kill the server. The Bash tool's `run_in_background` parameter handles this in principle, but a thin wrapper that knows "wait for `localhost:5173` to be ready, then return the PID" would be reusable across arcs.

**Recommended shape.** A skill `skills/spawn-dev-server/SKILL.md` callable by VERA (and maybe ADA for smoke checks): starts `npm run dev` in the background via Bash, polls `http://localhost:5173/` for readiness with a timeout, returns a structured `{ pid, url, ready_at }` record. A companion teardown step kills the PID.

**Recommend: defer until arc #2 or arc #7 surfaces the actual need.** Building it speculatively before a probe needs it is the wrong cost order; the existing Bash `run_in_background` may suffice. File a Tier-0 ticket-with-plan for the moment a verifier hits the friction, not before.

### Net assessment

**(a) is load-bearing for arc #1** and should be authored as part of arc #1's design step (not as a separate ticket). **(b) and (c) are quality-of-life** and should be deferred until a concrete arc surfaces friction with the existing tooling — file a ticket-with-plan when the friction surfaces, not speculatively. The deployed roster (12 officers) + skills (15 skills) + meta-aspects (7 docs) cover the v0.2 arcs as scoped; no new role-class or new envelope-discipline is required.

---

## §7 — Self-assessed weak points

Per Daedalus discipline, the brittle spots in this inventory I want flagged for the Colonel + Major Pliny to read before acting:

1. **The §5 batch-3 caveat is the load-bearing call.** Combining dark mode + a11y in the third batch is sensible *only if* the arc's design step explicitly includes the inline-style → CSS-variable refactor as in-scope. If left implicit, the executor will hit "dark mode doesn't actually toggle" mid-build and the arc spirals. I flagged this in §5 batch 3, but it deserves emphasis in any dispatch brief that batch generates: **the design.md for arc #7+#8 must include "CSS-variable refactor of inline styles" as an explicit deliverable, not a footnote.**

2. **Pipeline-shape recommendations are my judgment, not the rubric.** The brief invited me to consult `skills/tier2-task-routing/SKILL.md` if I wanted; I deferred to inference from work shape rather than reading that skill. If the Colonel or Major Pliny know the rubric judges differently — e.g., that Tailwind refactors are "build-only, no design phase needed because the design lives in `tokens.css`" — those calls override my §5 recommendations.

3. **Effort estimates are coarse (S / M / L).** I called batch 1 "M", batch 2 "M", batch 3 "L". The Colonel's calibration of S / M / L for this team in this project may differ from mine; treat these as ranks-relative-to-each-other rather than absolute time predictions.

4. **I did not validate that `tier2-project-onboarding` Phase 3 expects a numbered ticket-arc selection from this inventory.** The brief says "Major Pliny will read the inventory and report to the Colonel." If Phase 3 expects me to pre-rank the nine arcs by recommended-first-execution rather than just-three, I've under-delivered. Defaulted to the brief's literal request (first three).

5. **The §3 gap list may not be exhaustive.** I read `App.tsx` end-to-end, `Components.tsx` only the first 80 lines + grep pass, and `package.json` / `tokens.css` / `BRIEF.md` / `DESIGN_PRINCIPLES.md` / `README.md` end-to-end. A gap that lives only in the un-read parts of `Components.tsx` (e.g., a primitive that has its own a11y issue I didn't surface) is missed. Mitigation: arc #8's design step should grep `src/Components.tsx` for the same `aria-` / `role=` / `tabIndex` patterns I grep'd globally and surface anything specific to the primitives.

6. **I am taking the Colonel's three gap-fill answers as load-bearing without re-litigating them.** Specifically: (a) generator-side adapter, (b) single-user-localhost audience, (c) defer CI to v0.3. If any of those decisions shift before arc #1 is dispatched, the ordering and scoping in §4 / §5 may need revisiting — particularly (c), since adding CI in v0.2 would slot naturally into batch 1 alongside Vitest. Surfaced for explicit re-confirmation before Phase 3 dispatch.

7. **I have not exercised the app.** I did not `npm run dev` and click around. The §3 gaps are sourced from reading code + greps + the brief's authority; a runtime check might surface gaps invisible to static reading (e.g., a layout bug at narrow viewports, a console warning about deprecated React APIs, a flash-of-unstyled-content). For a 5-minute-readable inventory this is the right cost order, but it's worth knowing the gap list is static-analysis-grade, not exercise-grade.

---

**End of inventory. Major Pliny: read this, summarize for the Colonel, and pick batch 1 (or override) to dispatch in Phase 3.**
