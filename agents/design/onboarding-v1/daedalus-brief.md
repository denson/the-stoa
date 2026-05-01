# Brief for DAEDALUS_agent_character_builder — onboarding-v1 inventory

**Routine:** `tier2-project-onboarding` (Phase 2 of 3).
**Dispatcher:** Major Pliny (Session A).
**Project:** The Stoa: agent-character-builder (v0.1 alpha).
**Working directory:** `C:/Users/denso/claude_projects/agent-character-builder/`.
**Sibling repo (load-bearing for arc #1):** `C:/Users/denso/claude_projects/agent-team-team/`.

You have not seen the prior conversation between Major Pliny and the Colonel. This brief is everything you need.

---

## Your single deliverable

**Artifact:** `agents/design/onboarding-v1/inventory.md` (write to this exact path; the parent directory already exists).

Six required sections, in this order:

### §1 — What this project IS

One paragraph, plain English. Land the **meta-product framing**: this is an app whose domain object is the same kind of agent team that builds it. Don't be cute about it; just say it cleanly.

### §2 — Current artifacts (v0.1 alpha)

What shipped. Cover:

- **Code:** React 19 + Vite 6 + TypeScript stack; the three views (Team Overview / Officer Detail / Skill Library + Meta-aspects); the ⌘K command palette; the inline sample data in `src/data/sample.ts`.
- **Design-handoff bundle:** `design_handoff_character_builder/` (preserved as design reference; the JSX prototype is read-only).
- **Deployed agent team:** `.claude/agents/` (12 officers, all suffixed `_agent_character_builder`).
- **Team-meta-aspects substrate:** `agents/aspects/_meta/` (canonical 7 docs; verify count by reading the directory).
- **Key docs:** `README.md`, `BRIEF.md`, `DESIGN_PRINCIPLES.md`.

Brief, factual, with paths. Don't quote the docs at length — cite paths.

### §3 — Current gaps

What's missing or rough. Be specific — these gaps are the seeds for the work-arcs in §4. Cover at least:

- Schema divergence: `data-samples/` (real `agent-team-team` shape — `model_tier`, `callable_lieutenants`, `required_reading`) vs `src/data/sample.ts` + `src/data/types.ts` (design-handoff shape — `tier`, `lieutenants`, `reading`). No adapter exists yet.
- No real-data pipeline: `src/data/sample.ts` is the only data source; `scripts/gen-data.ts` does not exist.
- Light-mode-only: `DESIGN_PRINCIPLES.md` calls dark mode first-class; v0.1 ships only light tokens.
- Accessibility: divs-as-buttons; missing semantic landmarks (`<header>` / `<main>` / `<aside>` / `<nav>`); focus management on view changes; no `aria-live` for the command palette.
- No test scaffold: no Vitest config, no test files.
- No CI: no `.github/workflows/`.
- No URL-shareable state: `roster` / `archetypeFilter` / `selected` are local React state, not in URL.
- No compose-team flow: the "New agent" CTA in the header is wired but the multi-step wizard doesn't exist.
- No agent-author form: officer / skill creation has no UI.
- Brand assets: placeholder columnar logo + Inter / JetBrains Mono substitutes; final fonts and logo not yet integrated.
- Inline styles throughout: `src/Components.tsx` and `src/App.tsx` use inline styles; design tokens live in `src/styles/tokens.css` but Tailwind / CSS-modules refactor not done.

Read the source to confirm these and add anything else you spot.

### §4 — v0.2 work-arc catalog (9 arcs)

List all nine v0.2 arcs with one-paragraph descriptions each. The README's roadmap names six; the Colonel added three (dark mode, accessibility pass, Vitest scaffold). The full nine:

1. **Real-data wiring + adapter** — `scripts/gen-data.ts` builds `/data.json` from sibling `agent-team-team/` at build time; performs field-name remap (see Colonel answer #1 below for the architectural call).
2. **URL-shareable state** — `react-router` migration; `roster` / `archetypeFilter` / `selected` move to query params.
3. **Compose-team wizard** — multi-step flow behind the "New agent" header CTA; final step shells out to `agent-team-team/bootstrap.py`.
4. **Agent-author form** — form-driven officer / skill creation; writes back to sibling repo's `definitions/officers/<NAME>.json` + `definitions/bodies/<name>.md`.
5. **Tailwind refactor** — inline styles → utility classes; design tokens become theme extensions.
6. **Real brand assets** — final fonts + logo + wordmark; replace placeholders.
7. **Dark mode** — token + media-query work; first-class per `DESIGN_PRINCIPLES.md`. **(Colonel-added.)**
8. **Accessibility pass** — `<button>` migration; semantic landmarks; focus management; `aria-live` on palette. **(Colonel-added.)**
9. **Vitest scaffold** — config + first tests against the gen-data adapter from arc #1. **(Colonel-added.)**

For each arc, name **dependencies between arcs** explicitly — e.g., arc #3 (compose-team wizard) and arc #4 (agent-author form) both depend on arc #1 (real-data wiring) for the schema substrate; arc #5 (Tailwind) is mostly independent but touches every component file so should not run concurrently with arcs that change component shape.

### §5 — Recommended first three arcs

The Colonel has proposed this ordering (you may critique but should default to it if you don't have a strong reason to reorder):

1. **gen-data + adapter + Vitest scaffold** (arcs #1 + #9 combined; Vitest gets exercised immediately by testing the adapter)
2. **URL-shareable state** (arc #2; via react-router)
3. **Dark mode + a11y pass** (arcs #7 + #8 combined; same touch surface — every component)

Restate the ordering with **your analysis of why this ordering is sound** (or, if you disagree with any of the three after seeing the dependencies, flag the disagreement explicitly with reasoning — but default to the Colonel's order). For each, include:

- **Scope sketch** — what gets built, what doesn't.
- **Key files touched** — concrete paths.
- **Success criteria** — how we know it's done.
- **Rough effort estimate** — S / M / L.
- **Officer pipeline shape** — full-pipeline (design → critique → build → verify → review) / design-first / build-only / etc. Use your judgment of the rubric (see `skills/tier2-task-routing/SKILL.md` if you want to consult it; otherwise infer from the work shape).

### §6 — Tier-0 capability requests

Anything the team needs that isn't in the project itself. Examples might include:

- A skill for running `vite` / `vitest` cleanly under PowerShell-on-Windows (the Colonel's environment is Windows + PowerShell + MSIX-installed Claude — see global `~/.claude/CLAUDE.md` for the env notes; bash is available via the Bash tool, but native Windows shell wrinkles exist).
- A runner / lieutenant that knows how to spawn the dev server in the background.
- An aspect doc for "how this team uses the sibling `agent-team-team` repo as build input" — load-bearing because arc #1 depends on filesystem-path coupling that isn't documented anywhere yet.

If there are no Tier-0 requests, **state so explicitly** ("none surfaced; the deployed roster + skills cover the v0.2 arcs as scoped"). An empty section without that explicit defense reads as a missing-pass.

---

## Phase 1 survey recap (Major Pliny's read of the project)

The Stoa: agent-character-builder is a power-user web app for browsing / composing / authoring teams of AI agents (officers + skills + meta-aspects) defined in the sibling `agent-team-team` repo. v0.1 alpha is a click-thru shell: React 19 + Vite 6 + TypeScript, three views (Team / Skills / Meta-aspects) plus a ⌘K palette, all driven by inline sample data in `src/data/sample.ts`. Design language committed at hi-fi (Linear / Vercel / Stripe register) via `design_handoff_character_builder/`. Field-name divergence between design-handoff schema (`tier`, `lieutenants`, `reading`) and real `agent-team-team` JSON (`model_tier`, `callable_lieutenants`, `required_reading`) — adapter layer needed. Project-level team already deployed in `.claude/agents/` (12 officers, all suffixed `_agent_character_builder`). Team-meta-aspects substrate (`agents/aspects/_meta/`) ships canonical 7 docs. README's v0.2 roadmap names six work-arcs: real-data wiring + adapter, URL-shareable state, compose-team wizard, agent-author form, Tailwind refactor, real brand assets. **The project is a meta-product — its domain object IS the same kind of agent team that's building it.**

You may re-read any file you need; do not assume this recap is sufficient for your inventory.

---

## Colonel's answers to the three gap-fill questions (load-bearing — respect these)

### 1. Real-data wiring path

**(a) Source location:** Sibling repo on filesystem at `C:/Users/denso/claude_projects/agent-team-team/`. Default `scripts/gen-data.ts` to look at `../agent-team-team/`, configurable via env var (e.g., `AGENT_TEAM_TEAM_PATH`) for users with non-standard layout. **NOT** a git submodule (overhead + version coupling). **NOT** npm-published yet (premature; revisit when schema stabilizes and external users exist).

**(b) Adapter location:** Generator-side. `scripts/gen-data.ts` applies the field-name remapping and emits `/data.json` with the **design-schema shape** (`lieutenants`, `reading`, `tier`). The React app's `types.ts` only knows one shape. Rationale: simpler runtime types, transform happens once at build (not on every render), future consumers (CLI, API) each choose their own consumption shape from the `agent-team-team` source.

### 2. Audience and deployment story

v0.2-era audience: **a small circle of early users** (other beadwork users the Colonel wants to share with for feedback), all running on **localhost**. Single-user-localhost still — no auth, no hosted runtime — but design needs to handle "more than just me looking at it on my machine."

- **URL-shareable state:** matters somewhat (people will share screenshots / discuss links in chat). **Include in v0.2.**
- **Compose-team wizard "Step 5: shell out to bootstrap.py":** fine for v0.2 since it's localhost; everyone has their own `agent-team-team` copy. Subprocess call is safe.

### 3. What's NOT in the v0.2 roadmap that should be

**Add to v0.2:**

- **Dark mode.** `DESIGN_PRINCIPLES.md` calls it first-class; v0.1 only ships light. Mostly token + media-query work; low effort, load-bearing for the design's stated commitment.
- **Accessibility pass.** Divs-as-buttons is real. Replace with proper `<button>`, add semantic landmarks (`<header>` / `<main>` / `<aside>` / `<nav>`), fix focus management on view changes, add `aria-live` for the command palette.
- **Vitest scaffold.** The gen-data adapter is the natural first thing to test (input: `agent-team-team` JSON, output: design-shape JSON, verify the field rename works). Adding the scaffold now means subsequent arcs can write tests without per-arc setup.

**Defer to v0.3:**

- **CI (`.github/workflows/`).** Not load-bearing for localhost early-user feedback; pick up when sharing widens beyond the early circle.

**Recommended ordering for the first three arcs** (you may critique but should default to this):

1. gen-data + adapter + Vitest scaffold
2. URL-shareable state
3. Dark mode + a11y pass

This means the v0.2 work-arc list is **nine arcs** (the README's six + dark mode + a11y + Vitest scaffold), with the three above as the first arcs.

---

## Tone and length guidance

- **Inventory should be readable in 5 minutes.** Each section tight.
- **§4 (work-arc catalog) can be the longest section** since it's the shopping menu.
- **Don't pad. Don't write a manifesto.**
- Cite paths, not quotations.
- Use your normal design-artifact discipline — restate the problem at the top, name self-assessed weak points before returning, surface anything you noticed that isn't covered by the brief.

## Operational notes

- **No `bw` ticket exists** — this project's bw isn't initialized yet (`bw list` errors with "beadwork not initialized"). That's fine for the onboarding routine; the first ticket gets filed in Phase 3 after the Colonel picks an arc. **Skip the `bw start` / `bw show` boot steps in your envelope.**
- **No researcher artifact upstream** — STRABO has not been dispatched. You're working from this brief plus your own reads of the repo.
- **No design-time TypeScript validation needed** — your output is a markdown inventory, not a TS-bearing design.
- **No RUNNER probes needed** — §4's verification probes don't apply; this isn't a build-design dispatch.
- **The standard Daedalus return format applies** — restate the problem at the top of `inventory.md`, list self-assessed weak points in your final return block, etc.
- **Write the inventory to `agents/design/onboarding-v1/inventory.md`** (absolute: `C:/Users/denso/claude_projects/agent-character-builder/agents/design/onboarding-v1/inventory.md`). The parent directory exists; just write the file.

When you finish, post your standard return block. Major Pliny will read the inventory and report to the Colonel.

---

**Authored by Major Pliny on behalf of the Colonel (Denson Smith). All artifacts and metadata in this project are authored by Denson Smith per the workspace authorship rule.**
