# agent-character-builder — project brief

A web app for browsing, understanding, composing, and authoring AI agent teams.

The play on words: we're building **agents with character** — distinct roles, personalities, and disciplines — not stupid robots. The app lets a user explore an existing team of agents, build new teams from a roster of officers, and author entirely new agents/skills with a React-style interface.

---

## Who uses this

Technical users — developers, AI engineers, researchers — who deploy multi-agent teams into their projects via the underlying agent-team-team Python toolkit. They:

1. Want to **understand** what's in an existing team (what each officer does, what skills are available, what disciplines apply).
2. Want to **compose** a project-specific team (pick a roster, configure paths, deploy).
3. Want to **author** new officers/skills when the existing roster doesn't cover what they need.

This is a power-user tool. Dense info displays preferred over white space. Monospace for officer names + code references; sans-serif for descriptions.

---

## The data model

Agent teams are defined as **JSON metadata + markdown bodies**:

- **Officers** — named agents (MAJOR_PLINY, DAEDALUS, VERA, etc.) with a role, archetype (orchestrator / architect / verifier / etc.), rank (major / captain / lieutenant), tools, callable lieutenants, and a body (the natural-language system prompt).
- **Skills** — reusable capabilities agents invoke (RUNNER, FORMAT_VALIDATE, dispatch-lieutenant, etc.). Each has a description, kind, and callable_by list.
- **Meta-aspects** — team-wide conventions every officer reads (envelope-lifecycle, inter-agent-comms, etc.).
- **Disciplines** — operational rules (T-team, P-pair-programmer, X-cross-cutting, M-meta).
- **Team** — a roster (named groupings of officers) + work-class adjustments (per-project-type roster mods).

The data lives in [data-samples/](./data-samples/). Browse it to see exactly what shape officer JSONs / skill JSONs / body markdown files take.

The full canonical 12-officer roster (Tier 2 default) + 15 skills + 7 meta-aspects already exists in the [agent-team-team](https://github.com/denson/agent-team-team) repo. The app reads from it.

---

## Three primary views

### 1. Team Overview (landing)

A grid of officer cards showing the canonical roster. Each card:
- Officer name (monospace, prominent): `MAJOR_PLINY`
- Archetype label: `orchestrator-archetype`
- Rank pill: `major` / `captain` / `lieutenant` (color-coded)
- One-line role summary
- Visual hierarchy: majors at top, captains in middle, lieutenants at bottom

Sidebar/filter controls:
- Roster picker (default 12-officer / minimal 4-officer / user-level 8-officer / custom)
- Filter by archetype
- Search by name

Click any card → **Officer Detail**.

### 2. Officer Detail

Full view of one officer:

- **Header**: name, archetype, rank, nickname, role summary
- **Sidebar metadata**: tools list (chips), callable lieutenants (chips, clickable to skill detail), required reading (chips, clickable to meta-aspect detail), model tier
- **Main pane**: rendered markdown of the officer's body (their full role description, instructions, conventions). This is long-form content; render it like a documentation page.
- **Action buttons** (top-right): Edit · Clone · View JSON · Add to roster

### 3. Skill Library

Grid of skill cards:
- Skill name (monospace): `runner`
- "Callable by" chips: `DAEDALUS`, `ARGUS`, `VERA`
- Description preview (3-line clamp)

Filter controls:
- By callable_by (which officer can invoke)
- By kind (skill / subagent / script)

Click → **Skill Detail** (similar shape to Officer Detail).

---

## Plus four supporting views

### 4. Team Builder (wizard)

Multi-step:

- **Step 1: Pick a roster** — visually preview each (`default`, `minimal`, `user-level`, or "custom: start from scratch")
- **Step 2: Apply adjustments** — work-class picker (web-app / cli-tool / library / docs-site / data-pipeline / ml-model / infrastructure / meta-team / mixed) shows resulting roster delta
- **Step 3: Configure project** — form for project_name, user_name, workspace_path, worktree_root, ticket_prefix
- **Step 4: Preview** — diff/list of files that will be written; deployed officer names with project suffix
- **Step 5: Deploy** — button triggers `bootstrap.py`; show progress and result

### 5. Agent Builder (form)

- Tabs: "New officer" / "New skill" / "New meta-aspect"
- Officer form: name (validated), archetype (dropdown of existing archetypes), rank (radio), nickname, role_summary (textarea), tools (multi-select of Claude Code tools: Bash, Read, Write, Edit, Grep, Glob, Agent, TodoWrite, WebSearch, WebFetch), callable_lieutenants (multi-select from skill library), required_reading (multi-select from meta-aspects)
- Body editor: monospace markdown textarea (or split-view: raw + rendered preview)
- Save button: writes JSON + body file to disk + offers to add to active roster

### 6. Meta-aspects + Disciplines view

Read-only docs-style page for team-wide conventions. List + drilldown.

### 7. Deploy Status

What's deployed where:
- User-level Tier-0 (`~/.claude/agents/`) status
- Project-level Tier-2 deploys (per project, with deploy timestamp + project-suffixed officer count)

---

## Stack preferences

- **React 19** + **TypeScript**
- **Vite** for dev/build
- **Tailwind CSS** for styling
- **shadcn/ui** or **Radix** for primitives (lean dev-tool, not consumer)
- **react-router** for routing
- Static-SPA initially (read JSON via fetch); add a thin Python/Node backend later for write/deploy operations

---

## Design language

Modern dev-tool aesthetic. Reference points: **Linear**, **Notion**, **Vercel dashboard**, **Stripe dashboard**, **Anthropic Console**. NOT a consumer app, NOT chat-style.

- Dense information layouts
- Monospace for code/identifiers; sans-serif for prose
- Subtle borders, restrained color palette, accent color for primary actions
- Card-based grids for browse views
- Tabular layouts where data is structured (officer roster, skill library)
- Markdown-rendered content for long-form bodies

Color palette suggestion: a calm primary (slate or indigo), one accent for actions (blue or emerald), rank-coded chips (e.g. major = gold, captain = silver, lieutenant = bronze — or whatever fits the design language).

See [DESIGN_PRINCIPLES.md](./DESIGN_PRINCIPLES.md) for more.

---

## Out of scope for v1

- Real-time multi-user editing
- Collaborative comments
- A backend REST API (we'll add later)
- Git integration UI (use git from terminal)
- Authentication (single-user local tool)
