# stellation — Project Specification

**Status:** edited 2026-05-17. Ready for substrate Pass 10 dispatch per `the-stoa/SPECIFICATION.md` §13.12 (behavioral validation via test-project dispatch).

**Audience:** a fresh Stoa team activated against `~/claude_projects/stellation/` with the-stoa substrate freshly deployed via `install.sh`. This document is the team's primary input.

**Validation framing:** This project's deliverable is real (PRINCIPAL may embed the viz as a component in a future game UI); the team's BEHAVIOR while building it is the substrate-validation evidence per the-stoa SPECIFICATION.md §13.12 (Pass 10 behavioral validation).

---

## §1 Purpose

`stellation` is a single-page React web application that displays beadwork (`bw`) tickets as an animated **constellation** — a star map where each ticket is a star, dependencies between tickets are the constellation lines connecting them, and the visual + interaction language is built on a star-chart / night-sky metaphor.

The metaphor is load-bearing, not decorative:

- Tickets-as-stars makes priority (size) and status (brightness/color) visually scannable in a single glance.
- Dependencies-as-constellation-lines makes the ticket-graph topology legible — clusters of related work emerge as constellations the eye can name.
- The night-sky background gives motion (slow camera drift; star twinkle) without competing with the data layer.
- The metaphor is **componentizable** — the constellation view can later embed into a larger app (a game UI's "quest map," for instance) without theme-mismatch.

The app is NOT:
- A bw client — read-only; no writes, no auth, no persistence.
- A general-purpose graph visualization tool — purpose-built for bw's ticket schema.
- A 3D renderer — CSS transforms + SVG/Canvas only; no WebGL.
- A production multi-user system — single-page, single-user, single-load.

---

## §2 Tech stack — LOCKED

| Concern | Choice | Rationale |
|---|---|---|
| Framework | React 18+ with TypeScript (strict mode) | Industry standard; matches the-stoa app/ stack |
| Build tool | Vite | Fast dev server; clean build; modern default |
| Styling | Tailwind CSS | Utility-first; consistent design vocabulary; low cognitive overhead |
| Animation | Framer Motion (motion lib) | Mature React animation library; `<AnimatePresence>` + `layoutId` patterns are exactly what this viz needs |
| Graph layout | d3-force (v3+) | Canonical force-directed layout; small dependency surface; well-understood physics |
| Rendering | SVG for stars + lines (Canvas if perf demands it post-§5 perf check) | SVG is animatable + accessible by default; Canvas only if 100-ticket render times exceed budget |
| Testing | Vitest | Vite-native; fast; familiar API |
| Package manager | npm | Lowest friction; pre-installed with Node; team is less likely to confabulate package-manager-specific commands |
| State management | useState / useReducer only | App is small; introducing Zustand/Jotai is over-engineering per §6 |
| Routing | none — single-page with modal for detail view | Out of scope per §6 |

**No backend, no API client, no auth library** — out of scope per §1.

---

## §3 Data — the bw ticket schema

Input: a JSON file at `<repo>/data/tickets.json` containing an array of ticket objects. Schema:

```typescript
type BwTicket = {
  id: string;                    // e.g., "stoa--y14"
  title: string;                 // ticket title
  status: "open" | "closed";     // current status
  priority: "P0" | "P1" | "P2" | "P3" | "P4";  // priority
  body: string;                  // markdown body
  comments: Array<{
    timestamp: string;           // ISO 8601
    text: string;
  }>;
  dependencies?: {
    blocks?: string[];           // ticket ids this ticket blocks
    blocked_by?: string[];       // ticket ids blocking this ticket
  };
  tags?: string[];               // optional tag set
};
```

**Fixture requirement:** the team authors a `data/tickets.json` with **40-100 tickets** with variety across status, priority, and dependency-graph topology so the constellation has visible structure. The team may export a starting set from any project's `bw` install via `bw list --json` (with bodies stubbed if real bodies aren't appropriate to ship) OR hand-author fixture data inspired by the-stoa's actual ticket landscape.

A reference sample at `docs/validation/sample-tickets.json` in the-stoa is NOT provided — the team authors their own fixture as part of Arc 2 (data layer).

**Schema validation:** parser rejects malformed JSON with a clean error message displayed in the UI. Schema violations are logged to console + the affected ticket is excluded from the viz (other tickets still render).

---

## §4 The constellation viz — design spec

### §4.1 The star (ticket as visual element)

- **Position:** d3-force layout; gravity centered; charge negative (stars repel each other); link force on dependencies (`blocks` / `blocked_by`).
- **Size:** maps to priority. P0 = magnitude 1 (largest, brightest); P4 = magnitude 5 (smallest, dimmest). Use a logarithmic scale matching real astronomical magnitudes for a perceptually-correct size gradient.
- **Color:** maps to status + priority:
  - **Open tickets** are warm: P0 gold (`#FFD700` → `#FFAA00` gradient by magnitude), P1-P4 graduating to warm white (`#FFF8E7`).
  - **Closed tickets** are cool: muted silver-blue (`#B8D4F0` → `#6B8FB5`), 40% opacity of equivalent-magnitude open star.
- **Twinkle:** every star has a subtle opacity pulse (CSS animation or Framer Motion `animate` loop). Open tickets twinkle on a 2-3s period; closed tickets twinkle on a 6-8s period (slower = duller = less attention-grabbing). Each star's phase is offset randomly so the field doesn't pulse in unison.
- **Hover state:** the star brightens 15%, scales 1.1x, and its connected constellation lines highlight (stroke-width 1.5x; opacity 1.0). Other stars dim to 50% opacity; their lines fade.
- **Active (clicked) state:** triggers the orbit-detail transition (§4.3).

### §4.2 The constellation lines (dependencies as visual edges)

- **Geometry:** SVG `<path>` elements drawn between connected stars. Curved (slight quadratic bezier; not straight lines) for organic feel.
- **Color:** dimmer than the brightest connected star; gradient along the line from one star's color to the other's.
- **Stroke:** 0.5px default; 1.5px on hover-highlight; 2px on selection.
- **Animation on first load:** lines draw in sequence using SVG `stroke-dasharray` + `stroke-dashoffset` animation. Sequence: layout settles (stars appear with stagger), then lines draw progressively from highest-priority cluster outward. Total intro sequence: 3-4 seconds; perceived "the constellation forms before your eyes."
- **Direction indicator:** `blocks` direction shown with a faint arrowhead at the blocked-end of the line (subtle, doesn't dominate).

### §4.3 The detail view (click-for-detail)

When a star is clicked:

1. The clicked star expands smoothly (Framer Motion `layoutId`) into a central detail card — ticket id + title at top, body rendered as markdown, comments timeline below.
2. The card has a subtle glow matching the star's color.
3. **Comment-orbit:** each comment is rendered as a small "moon" card that drifts in a slow orbit around the detail card. Hover any comment-moon → it pauses + scales 1.2x + becomes readable. Drag to rotate the orbit (kinetic; inertial).
4. **Dependency-stars-visible:** the detail-card's connected stars (its blocked + blocked_by tickets) remain visible at reduced size, drawn around the detail card with their constellation lines highlighted. Click any of them → smooth crossfade to that star's detail.
5. **Close:** click outside, press ESC, or click the small "✕" in the detail card → reverse animation; the detail card collapses back into the star; constellation returns to its prior state.

### §4.4 The background (the night sky)

- **Base:** dark navy-to-black radial gradient (`#0a0e1a` center → `#02030a` edges).
- **Nebula:** very faint, large-scale animated noise pattern (CSS `filter: blur(100px)` on slow-rotating SVG noise; opacity 0.08). Adds depth without competing with the stars.
- **Camera drift:** the entire star field slowly pans in a Lissajous curve (period ~60s; amplitude small — 2-3% of viewport). Idle motion that signals "this is a living scene." Pauses during interaction (hover, click, drag).
- **Parallax (subtle):** background nebula moves at 0.3x the speed of the star field for subtle depth illusion.

### §4.5 The filter / sort UI

- **Filter chips** docked at top-left, semi-transparent (`bg-black/40 backdrop-blur`):
  - Status: `[ ALL ] [ OPEN ] [ CLOSED ]`
  - Priority: `[ P0 ] [ P1 ] [ P2 ] [ P3 ] [ P4 ]` — multi-select; each chip lights up when active.
- **Sort dropdown** at top-right (same styling):
  - "by priority" (default; high priority center)
  - "by latest activity" (latest-commented stars in center)
  - "by dependency-degree" (most-connected stars center)
- **Filter transitions:** stars that get filtered OUT fade + drift away (off-screen, with slight rotation); stars that come IN fade in at their layout position. Constellation lines connecting filtered-out stars fade.
- **Sort transitions:** the d3-force layout re-runs with new center-attraction weights; stars smoothly transition to new positions over ~1.5s (Framer Motion layout animation; spring physics).

### §4.6 Empty state + error state

- **Empty:** "The sky is empty." rendered center-screen in a small caption; a single distant star fades in slowly + slowly drifts (so the screen isn't fully blank).
- **Data load error:** error caption "Couldn't load tickets — check `data/tickets.json`" + a faint flickering star indicating the error.

### §4.7 Accessibility (reasonable defaults)

- Keyboard nav: tab through filter chips, sort dropdown, and currently-focused star. Arrow keys move focus between stars in the constellation (by spatial proximity).
- ARIA labels on every star (`<g role="button" aria-label="ticket stoa--y14, priority P2, status open, title ...">`).
- Color is never the only signal (status also has shape distinction — open stars have a subtle 5-pointed glyph; closed stars are smooth circles).
- Reduced motion: respect `prefers-reduced-motion`; if set, drop twinkle + camera drift + intro sequence; static positions, instant transitions.

---

## §5 Deliverables

1. **Working app** — `npm run dev` starts dev server; `npm run build` produces `dist/`; `npm run preview` serves the static bundle locally.
2. **README** at repo root — name + 1-paragraph description + setup (clone / install / dev / build / preview / deploy) + an animated GIF or 3-screenshot strip showing the constellation, hover-state, and detail view.
3. **Data fixture** — `data/tickets.json` with 40-100 tickets exhibiting structural variety (multiple connected components; isolated stars; clusters of varying priority; closed tickets mixed with open).
4. **Tests** (Vitest):
   - Unit tests for the data parser (malformed JSON; schema violations; empty array; single-ticket; max-fixture-size).
   - Component tests for filter + sort logic (correct stars hidden/shown; correct sort order).
   - Layout determinism test (given a seed, d3-force produces consistent positions — useful for visual regression later).
5. **Performance budget:**
   - First Contentful Paint < 1.5s on a mid-tier laptop.
   - Largest Contentful Paint < 3s.
   - Intro sequence completes by 4s after load.
   - 60fps during constellation layout settle + during hover-state transitions for fixtures up to 100 tickets.
   - Document any deliberate trade-offs (e.g., "Canvas fallback considered but SVG was within budget").
6. **One-command preview** documented in README — `npm run preview` (after `npm run build`) is sufficient. GitHub Pages deploy section in README as optional add-on; not required for v1 ship.
7. **Substrate footprint:** `bw` history showing arc lifecycle; `git log` showing per-CAPTAIN Co-Authored-By trailers per `operating-disciplines.md` §28; PLINY signoffs citing live-verified state per `MAJOR_PLINY.md` §5.10.

---

## §6 Out of scope (intentional v1 constraints)

- **Live bw integration** — no `bw` CLI shim, no API. Static JSON only.
- **Write capability** — no ticket creation, commenting, closing, dependency editing.
- **Backend / auth / persistence** — none.
- **WebGL / 3D** — CSS transforms + SVG only. If perf forces Canvas, that's still 2D.
- **Multi-project** — single fixture file; one constellation; no switching.
- **Real-time updates** — no polling, no websocket; load-once.
- **Themes** — locked color palette per §4.
- **Mobile-first** — desktop-first; responsive degrade is nice-to-have; the constellation viz inherently needs screen real estate. Mobile fallback can be a paginated card list, but is not required for v1.
- **Internationalization** — English only.
- **Full WCAG audit** — reasonable defaults per §4.7; full audit is post-v1.
- **Sound** — no audio in v1. Quiet app.

---

## §7 Project-specific anti-patterns (extend the-stoa SPECIFICATION.md §11)

- **Animation gratuity** — every animation choice serves perception or interaction. The twinkle isn't decorative; it signals open-vs-closed at the periphery of attention. The camera drift isn't decorative; it signals "live scene." The detail-view orbit isn't decorative; it spatially-organizes related metadata. If an animation can't be justified per the visual language, cut it.
- **Premature 3D** — the metaphor is a star chart (2D); it is NOT a galaxy simulator. Adding WebGL / Three.js triples the complexity for no metaphor-clarity gain.
- **Over-engineering the layout** — d3-force is sufficient for 40-100 tickets at one zoom level. Don't add zoom + pan + multi-layer + clustering algorithms. The team can ship a beautiful static-zoom constellation that's better than a feature-rich one that's janky.
- **"Cool" without coherence** — every motion choice should fit the night-sky / star-chart / star-physics vocabulary. Bouncy springs that feel like party balloons are wrong vocabulary; smooth inertial drift is right. The constellation feels like a place; it should not feel like a CSS animation gallery.
- **Forcing real bw data** — the v1 ships against a hand-authored fixture. Live bw is a future arc.

---

## §8 Suggested arc decomposition (team owns; not prescriptive)

A plausible path:

- **Arc 1 — Scaffold.** Vite + React + TS + Tailwind init; Framer Motion + d3-force install; `tsconfig` strict; `package.json` scripts; baseline commit.
- **Arc 2 — Data layer.** TS types per §3; parser + validator; hand-authored 40-100-ticket fixture in `data/tickets.json`; Vitest tests for parser.
- **Arc 3 — Constellation core.** Background gradient + nebula; d3-force layout; render stars as SVG circles with priority-size mapping + status-color mapping; static (no animation yet); filter + sort logic + chip/dropdown UI.
- **Arc 4 — Motion.** Twinkle; camera drift + parallax; intro sequence (stagger-in stars; progressive line-draw); hover-state highlights; filter/sort transitions.
- **Arc 5 — Detail view.** Click-to-expand; comment-orbit; dependency-stars-visible; close interactions; markdown rendering.
- **Arc 6 — Polish + perf + ship.** Performance pass against §5 budget; reduced-motion fallback; empty/error states; accessibility audit per §4.7; README + screenshots/GIF; build verification; tag v1.

DAEDALUS may bundle / split differently. Six arcs is the high estimate.

---

## §9 Validation criteria (this project's "spec met")

The project is shipped when ALL of:

1. **Build green** — `npm run build` exits 0; no TS errors; `dist/` produced.
2. **Tests green** — `npm run test` exits 0; coverage on data parser + filter/sort logic.
3. **Performance budget met** — measured via Lighthouse or equivalent; all §5.5 metrics pass.
4. **Visual spec met** — every §4 element present: stars, lines, twinkle, camera drift, hover-highlight, detail-view-with-orbit, filter/sort transitions, empty state, error state, reduced-motion fallback.
5. **PRINCIPAL eye-test** — PRINCIPAL runs `npm run dev` locally + interacts with the constellation; the experience matches the night-sky / star-chart vocabulary described in §1, §4. Subjective; PRINCIPAL signs off OR surfaces specific revision items.
6. **Substrate disciplines observable** — `git log` shows §28 trailers on CAPTAIN commits; bw shows complete arc lifecycle (gauntlet ran; verdicts captured; signoffs cite live-verified state per `MAJOR_PLINY.md` §5.10; pastes archived per §5.11).
7. **One-command preview works** — `npm run build && npm run preview` produces a viewable constellation at the documented local URL.

When all 7 fire, the project is v1 shipped. Substrate-validation evidence (criterion 6) feeds back to the-stoa `SPECIFICATION.md` §13.12 Pass 10 observation trail (`agents/observation/spec-validation/test-dispatch-trail.md`).

---

## §10 The PRINCIPAL eye-test acceptance criterion — specifics

§9.5 is the most subjective criterion. Specifics that signal "yes, this is what stellation should feel like":

**Yes signals:**
- The constellation has visual personality — it doesn't look like generic d3 examples online.
- The motion language is coherent — drift, twinkle, line-draw, orbit all feel like they're part of one vocabulary.
- The interactions are responsive — no perceptual lag between click and detail-view-expansion; no janky filter transitions.
- The viz is legible — at a glance, the PRINCIPAL can identify which stars are open vs closed, high-priority vs low, well-connected vs isolated.
- The team can articulate WHY they picked each animation easing curve / each color / each motion timing — design.md captures rationale.
- The detail-view orbit feels like it belongs in a star-chart UI, not like Material Design from 2018.

**No signals (revision triggers):**
- Bouncy / cartoony motion — wrong vocabulary for a night-sky scene.
- Bright neon colors — washes out the star-chart palette.
- Decoration without purpose — particles for the sake of particles; flashing for the sake of flashing.
- Default Framer Motion easings everywhere — the team didn't pick; they accepted.
- Performance jank — visible frame drops during hover or sort transitions.

PRINCIPAL retains the right to surface "this doesn't feel like stellation" as a substance disagreement triggering a revision arc, but will not exercise it for cosmetic preferences — only for vocabulary-mismatch where an animation choice violates the night-sky / star-chart language.

---

## §11 Future arcs (post-v1, not in scope)

Filed-when-ready:

- **Live bw integration** — read from `bw list --json` at load; auto-refresh on file watch.
- **Zoom + pan** — navigate large constellations; cluster zoom-out.
- **Time travel** — slider that replays the bw history (tickets bloom in as they're filed; close + dim as they're closed; constellation lines appear as dependencies are added).
- **Multi-project** — switch between fixtures or constellations; cross-project edges as faint inter-cluster lines.
- **Embed-as-component** — package as a React component with a clean prop API for embedding in a game UI or other React app.
- **Mobile fallback** — paginated card list view for narrow viewports.
- **Sound design** — optional ambient layer (very subtle drone + click sounds) with a settings toggle.
- **Theme variants** — alternative star-chart palettes (warm-tone "dawn"; mono-color "schematic"; etc.).
- **Performance work for >100 tickets** — Canvas rendering; quadtree culling; level-of-detail.

Each becomes a fresh ticket post-v1; PRINCIPAL ratifies the next motion.

---

## §12 Workspace + dispatch setup

**Workspace location:** `~/claude_projects/stellation/`

**Setup steps (PRINCIPAL executes):**
1. `mkdir ~/claude_projects/stellation && cd ~/claude_projects/stellation`
2. `git init && git add -A && git commit -m "init"` (empty initial commit)
3. Copy this file from `the-stoa/docs/validation/stellation-SPECIFICATION.md` → `~/claude_projects/stellation/SPECIFICATION.md`
4. `bash ~/claude_projects/the-stoa/substrate/install.sh` from inside the new workspace — deploys the spec'd substrate.
5. Initialize bw: `bw init` (or whatever the canonical first-touch command is for a fresh project).
6. Spawn fresh POLYBIUS + PLINY sessions at this workspace.
7. Hand them activation pastes pointing at `SPECIFICATION.md` as primary input.

**Bw prefix:** `stell--` for tickets in this project.

**GitHub remote:** optional for v1; the project ships as a local working tree first. PRINCIPAL may create a remote at any point.

The team operates in semi-autonomous mode per the-stoa SPECIFICATION.md §13.15 (Mode + dispatch).
