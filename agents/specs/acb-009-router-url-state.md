# acb-009 — react-router + URL-shareable state

**Author:** Denson Smith (Colonel) via Major Pliny.
**Status:** Spec locked, ready for design.
**Project:** The Stoa: agent-character-builder, v0.2 Phase 1 prerequisite.
**Working dir:** `C:/Users/denso/claude_projects/agent-character-builder/`.
**bw ticket id:** `acb--a7k.3` (already started; reference in commits, close after the arc lands).
**Pipeline mechanism:** **Full pipeline** — DAEDALUS → ARGUS → ADA → VERA → CATO. POLYBIUS orchestrates; Major Pliny gates spec-vs-result at the end.
**Source brief:** `agents/follow-ups/acb-NNN-router-url-state.md` (NNN resolved to 009 here).

---

## §1 — Goal

Migrate the Stoa web app (`http://localhost:5173/`) from local-React-state navigation to URL-shareable state via `react-router-dom`. Tab, selected officer, roster, and archetype filter become URL-driven; deep-links and refresh-survival work; the ⌘K palette navigates by URL; the existing `window.STOA_STATE` bridge (acb-008) is updated to read URL-driven fields from router hooks.

The success state: `http://localhost:5173/#/officer/MAJOR_PLINY?roster=default` loads directly to MAJOR_PLINY's detail with the default roster active, browser back/forward navigates the view stack, and a Chrome MCP script (or future `agent-design-tutor` skill) can drive the app by setting URL fragments rather than synthesizing clicks.

## §2 — Why this scope, why now

**Phase 1 prereq.** Per `agents/pliny-plans/acb-roadmap-v0.2-onward.md`, this is the second Phase 1 prerequisite (after acb-008 skill-affordances, which just shipped). It unblocks two downstream Phase 1 consumers and was bumped in priority by Chrome MCP validation on 2026-05-01:

- **WILL-BLOCK acb-007** (`agent-design-tutor` Claude Code skill). Driving the app via URL changes is materially cleaner than synthesizing clicks via Chrome MCP — the skill steers by `setSearchParams`-equivalent fragments.
- **WILL-UNBLOCK acb-006** (in-app tutorial), once both this and acb-007 land. The tutorial overlay needs deterministic navigation to anchor explanations onto specific officer / tab / filter views.
- **Early-user link sharing.** A link to a specific officer or filtered view becomes a real artifact a user can paste.

**Composition pressure with acb-002 (gen-data adapter).** Both arcs touch `App.tsx` state plumbing. DAEDALUS chooses bundle-vs-sequence at design time (see §6 Decision 3); this is an architect-tier call, not a Colonel call.

**Why now (vs deferral).** The Phase 1 vertical-slice demo is gated on it; deferring it gates everything downstream. Fix-now discipline applies at the arc level the same way it applies at the bug level.

## §3 — In scope

### Part A — Router scaffolding

1. **Add `react-router-dom`** to `package.json` (`^7.x` — current major as of 2026-05; DAEDALUS confirms via web search before pinning, per the global "search the web" rule).
2. **Wrap `<App/>` in `<HashRouter>`** in `src/main.tsx` (NOT `<BrowserRouter>` — see §6 Decision 1, Colonel-locked).
3. **Define routes** in `App.tsx` (or a new `src/routes.tsx` if DAEDALUS prefers separation):
   - `/` → Team Overview (default `tab === "team"`, no officer selected)
   - `/officer/:name` → Officer Detail (resolves `:name` against `data.officers`; 404 fallback if name missing)
   - `/skills` → Skills tab
   - `/skill/:name` → Skill Detail **placeholder route** (renders a minimal "Skill detail not yet implemented — back to skills" page; full implementation deferred per §4)
   - `/meta` → Meta-aspects tab
   - `/meta/:name` → Meta-aspect Detail **placeholder route** (same placeholder treatment)
4. **Query params:**
   - `?roster=default|minimal|user-level|custom` — drives the existing `roster` filter
   - `?archetype=<archetypeName>` — drives the existing `archetypeFilter`
   - When omitted, defaults are `roster=default`, `archetype=` (null/all).

### Part B — State migration

Current local React state in `App.tsx` lines 998-1002:

```tsx
const [tab, setTab] = useState<Tab>("team");                          // → URL pathname
const [selected, setSelected] = useState<Officer | null>(null);       // → /officer/:name
const [paletteOpen, setPaletteOpen] = useState(false);                 // STAYS LOCAL (modal)
const [roster, setRoster] = useState<RosterId>("default");             // → ?roster=
const [archetypeFilter, setArchetypeFilter] = useState<Archetype|null>(null); // → ?archetype=
```

5. **`tab` derives from the route.** Top-level path determines tab: `/` and `/officer/:name` → "team"; `/skills` and `/skill/:name` → "skills"; `/meta` and `/meta/:name` → "meta". The `Tab` type can stay as a derived value; `setTab(t)` callsites become `navigate("/")` / `navigate("/skills")` / `navigate("/meta")`.
6. **`selected` derives from `useParams().name`** when on `/officer/:name`. The `setSelected(o)` callsites become `navigate(\`/officer/${o.name}\`)`. `setSelected(null)` (the "back to team" affordance) becomes `navigate("/")`.
7. **`roster` and `archetypeFilter` derive from `useSearchParams()`.** Setters become `setSearchParams(prev => { ... })`. Validate values against the typed unions (`RosterId`, `Archetype`); invalid query values fall back to defaults rather than crashing.
8. **`paletteOpen` STAYS LOCAL** (modal-overlay state, not a navigation target — deliberate per the source brief; see §6 Decision 4 below for the affirmation).

### Part C — ⌘K palette navigates by URL

9. **CommandPalette `onPickOfficer` (App.tsx line 1115-1118)** currently calls `setTab("team"); setSelected(o);`. After migration: it calls `navigate(\`/officer/${o.name}\`)` and closes the palette. No more local-state writes for navigation.
10. **`onPickSkill`** (if present or added — verify against current shape) navigates to `/skill/:name` (the placeholder route is fine).
11. The ⌘K hotkey itself still toggles `paletteOpen` (modal local state); only the row-pick navigation changes.

### Part D — `window.STOA_STATE` bridge migration (compositional follow-on for acb-008)

12. The `useEffect` at `App.tsx:1052-1060` currently mirrors `{dark, currentTab: tab, selectedOfficer: selected, roster, archetypeFilter}` from local state. **Update it to read URL-driven fields from router hooks** (`useParams`, `useSearchParams`, `useLocation`). `dark` continues to come from `useTheme()`. The exposed shape, contract (read-only by convention, single-object replace per render, reference-equality observation pattern), and JSDoc above the effect are PRESERVED — only the input wiring changes. Note in the JSDoc that `currentTab`, `selectedOfficer`, `roster`, `archetypeFilter` are now URL-derived.

### Part E — Tests

13. **Add at least one route-resolution Vitest test** — minimum viable: `/officer/MAJOR_PLINY` renders the right officer's name in the rendered output (use React Testing Library + a `MemoryRouter` with `initialEntries`). If acb-002's Vitest scaffold has not yet landed when this arc dispatches, DAEDALUS calls whether to add a minimal test scaffold here or sequence after acb-002. (See §6 Decision 3.)

## §4 — Out of scope (do NOT touch)

- **Full Skill Detail / Meta-aspect Detail page implementations.** Placeholder routes only. Real content is a v0.3 or follow-up arc.
- **SSR / static prerendering.** Single-user-localhost deploy posture; no server.
- **`paletteOpen` URL migration.** Modal state stays local. (See §6 Decision 4.)
- **TypeScript ambient declaration for `window.STOA_STATE`.** Still out of scope per acb-008 §4; the cast `(window as any)` survives this arc.
- **`data-testid` additions or changes to `<Link>` elements.** Existing acb-008 testids on header tabs and officer/skill/meta cards are preserved; new `<Link>` wrappers do NOT need additional testids (the testid already lives on the visible interactive element). If a wrapper structure forces the testid up to a `<Link>`, ADA preserves the testid value verbatim. (See §9 weak-point 3.)
- **Element-type changes** (div → button, etc.). Still acb-005's territory.
- **Public-deploy / non-localhost considerations.** Phase 2.

## §5 — Definition of done (the 6 criteria VERA verifies)

1. **Direct deep-link load.** `http://localhost:5173/#/officer/MAJOR_PLINY?roster=default` loads directly to MAJOR_PLINY's detail with the default roster active. No flicker through the team grid first.
2. **Browser back/forward.** From the team grid → click an officer → click "Back to Team" → forward arrow returns to the officer detail. From `/skills` → `/meta` → back arrow returns to `/skills`. Filter chip click in team view writes a query param; back arrow clears it.
3. **Refresh survives.** Refreshing on `/officer/MAJOR_PLINY?archetype=architect` lands on the same view with the same filter applied.
4. **⌘K palette navigates by URL.** Opening the palette, selecting an officer row, closes the palette and updates the URL to `/#/officer/<name>`. The address bar reflects the change (proves it's URL-driven, not local-state-driven).
5. **One route-resolution test green.** `npm test` (or whatever Vitest entry is current — confirm against acb-002 scaffold state at dispatch time) runs and the new route-resolution test passes.
6. **`window.STOA_STATE` bridge reads URL-driven fields.** In browser devtools console, `window.STOA_STATE` returns the same shape as before (`{dark, currentTab, selectedOfficer, roster, archetypeFilter}`). After URL change (e.g., user types a new path or back/forward), the bridge updates on the next render. Each transition produces a NEW object (reference inequality preserved). VERA explicitly probes this — it is the compositional follow-on for acb-008 and the most likely thing to be missed.

## §6 — Locked architectural decisions

### Decision 1 — `HashRouter`, not `BrowserRouter` (Colonel-locked, 2026-05-01)

**Decision:** `<HashRouter>`. URLs look like `/#/officer/MAJOR_PLINY?roster=default`.

**Rationale:** Deploy posture is local laptop/desktop via Claude Code — no server, no `index.html` rewrite config. `BrowserRouter` requires server-side rewrite rules to send all paths to `index.html`; on a static-file host (or `file://` dev), refreshing `/officer/X` 404s. `HashRouter` works on plain static-file serving with zero config tax. The cosmetic cost of `/#/` is acceptable for v0.2; a future deploy arc (Phase 2) can revisit if a real server lands.

**Pass to DAEDALUS as a constraint, not an open question.** No re-litigation.

### Decision 2 — `STOA_STATE` bridge migration is part of THIS arc (compositional follow-on for acb-008)

**Decision:** acb-009 owns the `useEffect` rewire. The acb-008 spec §8 explicitly flags this as the next-arc responsibility.

**Rationale:** The bridge's whole point is to mirror the canonical source of truth for downstream consumers. After acb-009 lands, the canonical source for `currentTab/selectedOfficer/roster/archetypeFilter` is the URL, not local state. Leaving the effect reading from now-removed local state would either (a) crash on undefined or (b) silently lie to consumers. Either is a defect. ADA must update this effect in the same diff.

**The contract surfaces (JSDoc shape, single-object replace, reference-equality observation, `(window as any)` cast) are preserved verbatim** — only the input wiring changes.

### Decision 3 — Bundle-or-sequence with acb-002 is DAEDALUS's call (architect-tier)

**Decision:** DAEDALUS decides at design time whether to bundle acb-009 with acb-002 (gen-data adapter) into one arc, or sequence them. Major Pliny does NOT escalate this to the Colonel.

**Rationale:** Both arcs touch `App.tsx` state plumbing; DAEDALUS has the diff context, the Colonel does not arbitrate technical-tier choices. The bundling argument: one full state-plumbing refactor pass is cheaper than two. The sequencing argument: each arc's diff stays smaller and easier to review. Neither is wrong; the call is DAEDALUS's based on what the diff actually looks like once they've inventoried it.

**Pass to DAEDALUS as: "the bundle-vs-sequence question is in your lap; emit the call in `design.md`."**

### Decision 4 — `paletteOpen` stays local (NOT URL-driven)

**Decision:** `paletteOpen` is local React state; it is NOT migrated to a URL fragment or query param.

**Rationale:** It's modal-overlay state, not a navigation target. A user pasting a link to "the palette open over the team grid" is not a meaningful sharable artifact — the palette is a transient UI, the underlying view is the shareable thing. The source brief explicitly carved this out as a deliberate choice; affirmed here. If a future use-case (e.g., the in-app tutorial wanting to deep-link into "palette open with query 'major'") emerges, that's a follow-up; YAGNI for v0.2.

### Decision 5 — Default `roster=default` and `archetype=` are implicit (not echoed in URL)

**Decision:** When `roster === "default"` and `archetypeFilter === null` (the defaults), the URL omits the query params entirely. Users only see `?roster=` or `?archetype=` in the URL when they've actively changed those filters.

**Rationale:** Cleaner URLs for the common case; `/` reads "team grid, no filters" without query-param noise. DAEDALUS implements via `setSearchParams` that strips defaults rather than echoing them.

## §7 — Pipeline plan

| Step | Officer | Subagent / mechanism | Deliverable | Gate |
|---|---|---|---|---|
| 1 | DAEDALUS | per POLYBIUS dispatch | `agents/design/acb-009/design.md` — integration plan, bundle-vs-acb-002 decision, route table, state-migration call-site inventory, palette-by-URL refactor approach, no edits yet | Major Pliny reads + reconciles |
| 2 | ARGUS | per POLYBIUS dispatch | Critique of DAEDALUS plan: deep-link correctness, refresh-survival, back/forward semantics, STOA_STATE timing/reactivity post-migration | Major Pliny reconciles ARGUS findings into final plan |
| 3 | ADA | per POLYBIUS dispatch | Edits to `package.json`, `src/main.tsx`, `src/App.tsx`, possibly new `src/routes.tsx`, possibly new placeholder route components, route-resolution Vitest test | Lands the changes |
| 4 | VERA | per POLYBIUS dispatch | Verification against §5's 6 criteria via `http://localhost:5173/` (RUNNER for dev server) | Pass / fail per criterion |
| 5 | CATO | per POLYBIUS dispatch | Final craft review — diff hygiene, no new hex literals, idiomatic React Router 7 usage, `STOA_STATE` JSDoc accuracy post-migration | Pass / needs-revision |
| 6 | Major Pliny | (this session) | Spec-vs-result + project-spirit gate; verdict to POLYBIUS / Colonel | PASS / NEEDS-REVISION / ESCALATE |

POLYBIUS orchestrates the dispatches; Major Pliny owns the spec gate at the end of the chain.

## §8 — Composition

- **Composes (or sequences) with acb-002 (gen-data + adapter).** Both touch `App.tsx` state plumbing. DAEDALUS calls bundle-vs-sequence per §6 Decision 3. If sequenced, either order works; no hard ordering constraint emerges from the spec.
- **Composes with acb-008 (skill-affordances, just shipped).** The `window.STOA_STATE` `useEffect` at `App.tsx:1052-1060` migrates from local-state reads to router-hook reads. JSDoc above the effect is updated to note the shift. acb-008's testid surfaces are preserved; no testid renames in this arc.
- **WILL-BLOCK acb-007** (`agent-design-tutor` Claude Code skill). The skill drives the app via URL fragments after this lands; without acb-009 the skill would have to synthesize clicks via Chrome MCP, which is the failure mode this arc fixes.
- **WILL-UNBLOCK acb-006** (in-app tutorial), once both this and acb-007 land. Tutorial deep-links into specific officer/tab/filter combinations to anchor explanations.
- **Tangentially relates to `acb-NNN-testid-special-char-escaping`** (filed; not in this arc's scope). Phase 1 of that brief is a one-shot grep audit; if it triggers a fix and the fix touches data-layer naming, it composes with acb-002 (gen-data) more naturally than with acb-009. Mentioned for completeness; not a dependency.

## §9 — Self-assessed weak points (Major Pliny's pre-spec gate)

Surfaced for POLYBIUS / Colonel before dispatch:

1. **`react-router-dom` major version pin.** I did not pin a specific version. DAEDALUS does a web search at design time (per the global out-of-date-training-data rule) and pins the current stable `^7.x` — or the current major if 7 has been superseded. The router API surface used here (`<HashRouter>`, `useParams`, `useSearchParams`, `useNavigate`, `<Link>`, `<Routes>`, `<Route>`) has been stable across 6.x and 7.x; if the current major has renamed any of these, DAEDALUS adapts.

2. **Placeholder routes for `/skill/:name` and `/meta/:name` are in scope here.** Source brief said "placeholder if not yet built" and I ported that verbatim. Implementation: a minimal component that displays the resolved `:name` and a "back to <list>" link. Real detail content is a v0.3 or follow-up arc. Confirmed in scope.

3. **Testid composition with acb-008 (whether `<Link>` elements need new testids).** Decision: NO. Existing testids on the visible interactive element (e.g., `officer-card-MAJOR_PLINY` on the card) are preserved; if ADA wraps the card in a `<Link>`, the testid stays on the inner element (or on the `<Link>` if the inner element disappears — the value is what matters, not the host node). No new testid identifiers are introduced by this arc. Surfaced because the question came up explicitly in the dispatch brief.

4. **`paletteOpen` truly stays local.** Confirmed per §6 Decision 4. Source brief listed it as deliberate; no argument for URL-based palette state surfaced during pre-spec review. If POLYBIUS or Colonel wants to revisit (e.g., for the in-app tutorial use case), file a follow-up — not blocking this arc.

5. **Vitest scaffold dependency on acb-002.** §3 item 13 and §5 criterion 5 require a route-resolution Vitest test. If acb-002's Vitest scaffold has not landed by the time acb-009 dispatches, DAEDALUS calls: (a) add a minimal scaffold here, or (b) sequence acb-009 after acb-002. This is the strongest argument for bundling per §6 Decision 3, but I'm leaving the call to DAEDALUS rather than forcing a bundle here.

6. **`navigate()` callsite count is non-trivial.** A grep on `setTab`, `setSelected`, `setRoster`, `setArchetypeFilter` shows ~10-15 callsites in `App.tsx`. The diff blast radius is medium; ARGUS pre-critique should explicitly check for missed callsites (any surviving local-state setter for a now-URL-driven field is a latent defect).

7. **Default-stripping in URLs (§6 Decision 5) has a tiny subtlety.** If the user manually types `?roster=default` into the address bar, the app honors it but on the next setSearchParams round-trip (e.g., user toggles archetype), `roster=default` gets stripped from the URL. This is the intended behavior (URL converges to canonical-minimal form) but ADA documents it briefly so it's not surprising. CATO checks the implementation does this consistently.

---

**End of spec. POLYBIUS dispatches DAEDALUS first; DAEDALUS reads this verbatim plus the source brief at `agents/follow-ups/acb-NNN-router-url-state.md` and emits `agents/design/acb-009/design.md`. The bundle-vs-sequence decision for acb-002 is captured there. Then the chain proceeds DAEDALUS → ARGUS → ADA → VERA → CATO. Major Pliny gates spec-vs-result at the end.**
