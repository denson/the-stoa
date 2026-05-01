# Brief: react-router with URL-shareable state

**Status:** Brief filed (not dispatched). 2026-05-01.
**Suggested ticket id:** `acb-NNN-router-url-state`. Number assigned in roadmap.
**Pipeline shape:** **full pipeline** — touches every screen; user-visible navigation surface; CATO review on link-share UX matters.
**Effort:** M (medium); per inventory §5 batch 2.
**Sequence constraint:** Phase 1 prerequisite. Composes with acb-002 (both touch App.tsx state plumbing).

## Background

Already on the v0.2 roadmap as inventory §5 batch 2; **bumped in priority** by the Chrome MCP validation (Colonel, 2026-05-01). URL-shareable state means:

- The in-app tutorial (acb-006) can navigate the app deterministically by linking to specific officers / tabs / filters.
- The agent-design-tutor Claude Code skill (acb-007) can drive the app via URL changes (cleaner than synthesizing clicks via Chrome MCP).
- Early-user sharing of links to specific officers / filtered views works.

## In scope (per inventory §5 batch 2)

1. Add `react-router-dom` to `package.json`.
2. Wrap `<App/>` in `<BrowserRouter>` (or `<HashRouter>` if static-deploy-friendly is preferred — DAEDALUS calls).
3. Routes:
   - `/` → Team Overview
   - `/officer/:name` → Officer Detail
   - `/skill/:name` → Skill Detail (placeholder if not yet built)
   - `/meta` → Meta-aspects
   - `/meta/:name` → Meta-aspect Detail (placeholder)
4. Query params:
   - `?roster=default`
   - `?archetype=architect`
5. `useParams` / `useSearchParams` replace local state for `tab`, `selected`, `roster`, `archetypeFilter`.
6. `paletteOpen` stays in local state (modal, not shareable; deliberate choice per inventory).

## Out of scope

- Full skill / meta-aspect detail page implementations — placeholder routes are fine for now; v0.3 or follow-up arc fleshes them out.
- Server-side rendering — single-user-localhost doesn't need it.

## Definition of done (per inventory §5 batch 2)

1. `/officer/MAJOR_PLINY?roster=default` loads directly to MAJOR_PLINY's detail with the default roster active.
2. Browser back/forward navigates view stack correctly.
3. Refreshing any URL lands on the same view.
4. ⌘K palette navigates by setting URL, not local state.
5. `npm test` adds at least one route-resolution test (e.g., `/officer/X` renders the right officer).

## Composition

- **Composes with acb-002** (gen-data + adapter): both touch App.tsx state plumbing. DAEDALUS calls whether to bundle into one arc or sequence them. Bundling argument: one full state-plumbing refactor pass is cheaper than two. Sequencing argument: each arc's diff stays smaller, easier to review.
- **Composes with acb-NNN-skill-affordances**: `window.STOA_STATE` reads from URL state once router lands; if router lands first, `STOA_STATE` migrates from `useState` reads to `useParams/useSearchParams` reads.

## Open question

`<BrowserRouter>` vs `<HashRouter>`? BrowserRouter is the default and gives clean URLs (`/officer/PLINY`); HashRouter (`/#/officer/PLINY`) works on static-file hosts that don't rewrite to `index.html`. Current deploy target is unknown; DAEDALUS picks per acb-002's deploy decision (if acb-002 emits to a static `public/` artifact and we plan to serve via plain static, HashRouter is safer; if we control the server, BrowserRouter wins).
