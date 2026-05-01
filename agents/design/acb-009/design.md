# acb-009 — react-router + URL-shareable state — DESIGN

**Author:** Denson Smith (Colonel) via DAEDALUS.
**Status:** Design draft. ARGUS critiques next.
**Spec:** `agents/specs/acb-009-router-url-state.md` (read verbatim).
**Source brief:** `agents/follow-ups/acb-NNN-router-url-state.md`.
**Working dir:** `C:/Users/denso/claude_projects/agent-character-builder/`.
**Pipeline:** DAEDALUS (this) → ARGUS → ADA → VERA → CATO → Major Pliny gate. POLYBIUS orchestrates.

---

## Restatement (pre-gate, problem in own words)

Migrate `src/App.tsx`'s navigation state (`tab`, `selected`, `roster`, `archetypeFilter`) from local React `useState` to URL-driven state via `react-router` v7 `<HashRouter>`. Update the existing `window.STOA_STATE` bridge (acb-008) to read URL-driven fields from router hooks while preserving its contract surfaces verbatim. Modal state (`paletteOpen`) stays local. Add minimal placeholder routes for `/skill/:name` and `/meta/:name`. Deep-links and refresh-survival work; the ⌘K palette navigates by URL.

**Imported assumption flagged:** I am explicitly choosing to defer the §5 DoD #5 Vitest test to an immediate follow-up rather than bundle a scaffold here (see §1). The spec authorized this call but framed it as bundle-vs-sequence; I'm picking a third option (sequence-with-follow-up) and ARGUS should evaluate.

---

## §0 — Decisions table

| # | Decision | Authority | Rationale (one-line) |
|---|----------|-----------|---------------------|
| D1 | `<HashRouter>` (not `<BrowserRouter>`) | Colonel-locked (spec §6.1) | Static-deploy-friendly; no server rewrite tax |
| D2 | `STOA_STATE` migration in this arc | Colonel-locked (spec §6.2) | Bridge must mirror canonical truth; URL is canonical post-arc |
| D3 | `paletteOpen` stays local | Colonel-locked (spec §6.4) | Modal overlay, not a navigation target |
| D4 | Default-strip query params | Colonel-locked (spec §6.5) | Cleaner URLs in common case |
| D5 | **Sequence acb-009 first; defer Vitest test to follow-up** | DAEDALUS call (spec §6.3) | See §1 — bundling acb-002 doubles diff scope; partial Vitest scaffold composes poorly with acb-002's full scaffold |
| D6 | **`react-router@^7.14.2`**, importing from `react-router` (not `react-router-dom`) | DAEDALUS call (spec §9.1) | v7 unifies the package; current stable as of 2026-05-01. See §2 |
| D7 | **`<HashRouter>` wraps OUTSIDE `<ThemeProvider>` in `src/main.tsx`** | DAEDALUS call | Routing concern is independent of theme; nesting order doesn't matter for v1 but outer-router is the React-Router-docs convention |
| D8 | **Single `App.tsx` file holds `<Routes>`; no separate `src/routes.tsx`** | DAEDALUS call | Route count is small (5 paths); extracting saves no readability and adds an indirection |
| D9 | **Default-stripping via a `setSearchParamsStripDefaults` helper** in App scope | DAEDALUS call | One implementation, called from all setter sites; consistency is what CATO will check |
| D10 | **Placeholder routes are inline mini-components** in `App.tsx`, not new files | DAEDALUS call | ~15 LoC each; hoisting to files is premature given they'll be replaced in v0.3 |
| D11 | **All `navigate()` callsites live INSIDE the routed components** (not as props passed down) | DAEDALUS call | Components grab `useNavigate()` directly; cleaner than threading callbacks through props (which is what the current `setX`-via-prop pattern is) |
| D12 | **`useEffect` for `STOA_STATE` reads `useLocation()`, `useParams()`, `useSearchParams()` directly** | DAEDALUS call | Effect runs after commit; hook reads are the canonical source post-migration |

---

## §1 — Bundle-or-sequence verdict

**Verdict: SEQUENCE acb-009 first, defer Vitest test to immediate follow-up arc.**

The spec framed this as bundle-vs-sequence between acb-009 and acb-002 (gen-data adapter). I considered three options:

1. **Bundle acb-002 + acb-009.** One arc covering data adapter + state plumbing migration. Rejected: doubles the diff size (gen-data is its own ~300-LoC adapter + fixture work; state plumbing is its own ~150-LoC refactor). ARGUS critique surface explodes; ADA's blast radius covers two unrelated concerns; VERA verifies twice as many DoD criteria; CATO reviews two scopes of craft. The "one refactor pass is cheaper than two" argument assumes the two passes overlap, but they don't: gen-data touches `App.tsx` at the data-source line (`const data = SAMPLE_DATA;` → async fetch + loading state), while acb-009 touches the state-plumbing lines. Different sites, no real composition advantage from bundling.

2. **Add a minimal Vitest scaffold to acb-009.** Rejected: a half-scaffold here (a single `vitest.config.ts` + RTL setup just to support the route-resolution test) would then have to be reconciled with acb-002's full scaffold (adapter fixture round-trip test) when acb-002 lands. Two configs racing for ownership is a discipline-break. Either arc owns the scaffold; partial doesn't compose.

3. **Sequence acb-009 first; defer the route-resolution test to a follow-up that lands AFTER acb-002's scaffold.** Selected. The follow-up is small (one Vitest file, ~30 LoC) and has a concrete plan (see below). The spec's §5 DoD #5 is amended to: VERA verifies criteria 1-4 + 6 in this arc; criterion 5 (the Vitest test) is satisfied by the follow-up, gated on acb-002 landing.

**Follow-up brief (concrete plan per fix-now discipline):**

- **Ticket id (suggested):** `acb-009-followup-route-resolution-test`.
- **Sequence constraint:** lands AFTER acb-002 (which provides the Vitest scaffold).
- **Scope:** one new file `src/__tests__/routing.test.tsx` (or wherever acb-002 places tests) using `MemoryRouter` with `initialEntries={['/officer/MAJOR_PLINY']}` and React Testing Library, asserting that the rendered output contains `MAJOR_PLINY` in the right element.
- **Pipeline:** ADA-direct (build-only). No design judgment needed; the test shape is fixed.
- **Effort:** ~30 minutes.
- **Filed when:** at the moment acb-002 dispatches, this follow-up gets queued behind it.

This satisfies fix-now discipline: there's a concrete plan, not a handwave. The deferral is structural (Vitest scaffold doesn't exist yet), not optional.

**ARGUS audit note:** if ARGUS judges that sequencing-with-follow-up is wrong here (e.g., judges that runtime VERA probes are insufficient and the route-resolution test is load-bearing for THIS arc), the bundle path is still available — the spec sanctions either choice. Argue against my call if you see something I missed.

---

## §2 — react-router version pin

**Pinned: `react-router@^7.14.2`** (current stable major as of 2026-05-01).

**Package change:**
```jsonc
// package.json — dependencies
"react-router": "^7.14.2"
```

**Note: package is `react-router`, NOT `react-router-dom`.** v7 unified the two; `react-router-dom` is no longer needed. Imports come from `react-router`:

```text
// New imports in src/App.tsx (and src/main.tsx for HashRouter):
import {
  HashRouter,
  Routes,
  Route,
  Link,
  useParams,
  useSearchParams,
  useNavigate,
  useLocation,
  Navigate,
} from "react-router";
```

**Citation:** [react-router-dom on npm](https://www.npmjs.com/package/react-router-dom) — confirms 7.14.2 stable as of recent publish; [React Router HashRouter docs](https://reactrouter.com/api/declarative-routers/HashRouter) — confirms HashRouter is part of declarative mode and supported in v7; [useSearchParams docs](https://reactrouter.com/api/hooks/useSearchParams) and [useNavigate docs](https://reactrouter.com/api/hooks/useNavigate) — confirm both hooks are stable in v7. StrictMode compatibility confirmed via authentication guide examples that wrap routers in StrictMode.

**Why `^` not exact pin:** patch-level updates within 7.14.x are safe (semver). If a 7.15 lands during the design→build window with breaking changes (unlikely for a stable major), ADA pins to `~7.14.2` instead. Major Pliny / Colonel can override at gate.

---

## §3 — Routes table

| Path | Component | Params (URL/query) | Renders |
|------|-----------|--------------------|---------|
| `/` | `<TeamRoute>` (wraps `<TeamView>` + `<FilterSidebar>`) | `?roster=`, `?archetype=` | Team grid with filter sidebar |
| `/officer/:name` | `<OfficerRoute>` (wraps `<OfficerDetail>`) | `:name`, `?roster=`, `?archetype=` (preserved through navigation) | Officer detail |
| `/skills` | `<SkillsView>` | (none) | Skills list |
| `/skill/:name` | `<SkillPlaceholder>` | `:name` | Placeholder: name + "← back to Skills" link |
| `/meta` | `<MetaView>` | (none) | Meta-aspects list |
| `/meta/:name` | `<MetaPlaceholder>` | `:name` | Placeholder: name + "← back to Meta-aspects" link |
| `*` | `<NotFoundRoute>` | (none) | "Not found — return to team" link to `/` |

**Tab derivation:** `tab` is derived from `useLocation().pathname`:
- `/` or `/officer/...` → `"team"`
- `/skills` or `/skill/...` → `"skills"`
- `/meta` or `/meta/...` → `"meta"`
- otherwise → `"team"` (fallback, e.g., for `*`)

A `tabFromPath(pathname: string): Tab` helper lives at top of `App.tsx` (or in a `src/routing.ts` if ARGUS prefers extraction; my call is inline since it's 5 lines).

**Officer name → URL.** Officer `name` field is uppercase identifier (e.g., `MAJOR_PLINY`) per `data/types.ts`. URL encoding: passthrough — `MAJOR_PLINY` is URL-safe (uppercase + underscore). No `encodeURIComponent` needed for the canonical roster, but `<Link to={\`/officer/${o.name}\`}>` is the pattern; React Router internally encodes if needed (no manual encoding).

**404 handling for unknown `:name`.** If `useParams().name` resolves to a name not in `data.officers`, render a fallback inside `<OfficerRoute>`: "Officer not found — back to Team" link. Do NOT crash; do NOT silently render nothing.

---

## §4 — State migration table

Source-of-truth migration. Current state name → new source.

| Current | Site (App.tsx:line) | New source | New key |
|---------|---------------------|------------|---------|
| `tab` (useState<Tab>) | `App.tsx:998` | derived from `useLocation().pathname` via `tabFromPath()` | n/a (computed) |
| `selected` (useState<Officer\|null>) | `App.tsx:999` | `useParams().name` resolved against `data.officers` inside `<OfficerRoute>` | `:name` (path) |
| `paletteOpen` (useState<boolean>) | `App.tsx:1000` | **STAYS LOCAL** | n/a |
| `roster` (useState<RosterId>) | `App.tsx:1001` | `useSearchParams()` | `?roster=` |
| `archetypeFilter` (useState<Archetype\|null>) | `App.tsx:1002` | `useSearchParams()` | `?archetype=` |

**Validation:** `roster` and `archetypeFilter` are typed unions. The reads validate values against the type:
- `roster`: if `?roster=X` and `X` not in `["default","minimal","user-level","custom"]`, fall back to `"default"`.
- `archetypeFilter`: if `?archetype=X` and `X` not in `Object.keys(data.archetypes)`, fall back to `null`.

Validation lives in a small helper `parseRosterParam(s: string|null): RosterId` and `parseArchetypeParam(s: string|null, archetypes: ArchetypeColors): Archetype|null` in App scope.

**`useState`s removed from App component:** `tab`, `selected`, `roster`, `archetypeFilter`. Kept: `paletteOpen`.

---

## §5 — Navigation callsites

Every place currently calling a `setX` for a now-URL-driven field. Each becomes a `navigate(...)` or `setSearchParams(...)` call.

| # | Site (App.tsx:line) | Current code | New code | Notes |
|---|---------------------|--------------|----------|-------|
| 1 | `App.tsx:1076-1079` (Header `onTab` callback in `<App>`) | `setTab(t); setSelected(null);` | `navigate(\`/${t === "team" ? "" : t}\`)` (or `/`, `/skills`, `/meta`) | Tab click. `setSelected(null)` is implicit — going to `/` from `/officer/X` clears selection. |
| 2 | `App.tsx:1080` (Header `onSearch`) | `setPaletteOpen(true)` | unchanged (palette is local) | No URL change. |
| 3 | `App.tsx:1098` (TeamView `onPick={setSelected}`) | `setSelected(o)` | `navigate(\`/officer/${o.name}\${preserveQuery()}\`)` | Officer card click. Preserve current `?roster=` and `?archetype=` so back-to-team retains filter context. |
| 4 | `App.tsx:1103` (OfficerDetail `onBack`) | `setSelected(null)` | `navigate(\`/\${preserveQuery()}\`)` | "Back to Team" link. Preserve filters. |
| 5 | `App.tsx:1091` (FilterSidebar `setRoster` prop, callsite at sidebar:226) | `setRoster(r.id)` | `setSearchParamsStripDefaults(prev => { prev.set("roster", r.id); return prev; }, ["roster=default", "archetype="])` | Roster click. |
| 6 | `App.tsx:1093` (FilterSidebar `setArchetype` prop, callsites at sidebar:235 and sidebar:244) | `setArchetype(null)` / `setArchetype(a)` | `setSearchParamsStripDefaults(prev => { prev.set("archetype", a); return prev; }, ...)` or `prev.delete("archetype")` for null | Archetype clear / set. |
| 7 | `App.tsx:1115-1118` (CommandPalette `onPickOfficer`) | `setTab("team"); setSelected(o);` | `navigate(\`/officer/${o.name}\${preserveQuery()}\`); onClose();` | Palette officer pick. |
| 8 | (new) Skill row in palette `onPickSkill` (currently no handler — see Components/App.tsx:945-983) | n/a | `navigate(\`/skill/${s.name}\`); onClose();` | Adds palette-skill navigation. Currently the skill rows have no onClick — adding `onClick={() => onPickSkill(s)}` and an `onPickSkill` prop. |
| 9 | (new) `<SkillCard>` in `<SkillsView>` (Components.tsx — lookup needed) | n/a (or existing onClick) | wrap card in `<Link to={\`/skill/${s.name}\`}>` OR `onClick={() => navigate(...)}` | Skill card click → placeholder skill detail. ADA picks `<Link>` if structurally clean; falls back to `onClick + navigate` if `<Link>` breaks the existing flex/grid layout. **Testid preserved** per spec §4 + acb-008 §3 — `skill-card-{name}` stays on the visible interactive element. |
| 10 | (new) `<MetaCard>` in `<MetaView>` (App.tsx:716-762) | n/a (no onClick currently) | wrap card in `<Link to={\`/meta/${m.name}\`}>` OR `onClick={() => navigate(...)}` | Meta card click → placeholder meta detail. Same testid-preservation rule. |

**Total: ~10 callsites.** Spec §9.6 estimated 10-15; my count is 10 with two new affordances (skill-card and meta-card click navigation, items 9-10) added since the placeholders need an entry path. ARGUS audits for missed sites.

**`preserveQuery()` helper:** small helper that reads current `useSearchParams()` and returns a string like `"?roster=minimal"` (or `""` if defaults). Lives in App scope.

**`setSearchParamsStripDefaults` helper:** wraps `setSearchParams` with a post-update pass that deletes any param matching its default. Signature roughly:

```text
// Design-shape pseudocode (ADA refines to real code):
function useStripDefaultSearchParams() {
  const [params, setParams] = useSearchParams();
  return useCallback((updater: (p: URLSearchParams) => URLSearchParams) => {
    const next = updater(new URLSearchParams(params));
    if (next.get("roster") === "default") next.delete("roster");
    if (!next.get("archetype")) next.delete("archetype");
    setParams(next, { replace: false }); // push, not replace, so back-arrow works
  }, [params, setParams]);
}
```

(ADA refines; this is design-shape, not literal code.)

**`replace` vs push:** filter changes use push (default) so browser back-arrow undoes filter. Tab changes also push (so back returns to prior tab). The only `replace: true` site is the StrictMode-double-mount edge case if it surfaces — see §9 risks.

---

## §6 — STOA_STATE migration plan

Current `useEffect` at `App.tsx:1052-1060` reads from local `useState` values. Migrate to read from router hooks. **JSDoc above the effect (lines 1015-1051) is preserved verbatim with a single inserted paragraph noting the router-driven source.**

**Diff sketch (design-level — ADA refines):**

```text
// Design-shape pseudocode (ADA refines to real code in App.tsx):
// REMOVED (App.tsx:998-999, 1001-1002):
// const [tab, setTab] = useState<Tab>("team");
// const [selected, setSelected] = useState<Officer | null>(null);
// const [roster, setRoster] = useState<RosterId>("default");
// const [archetypeFilter, setArchetypeFilter] = useState<Archetype | null>(null);

// KEPT (App.tsx:1000):
// const [paletteOpen, setPaletteOpen] = useState(false);

// NEW — inside App, but only readable inside <Routes> children
// (App must move to be a child of <HashRouter> for hooks to work)

function App() {
  const data = SAMPLE_DATA;
  const { dark } = useTheme();
  const [paletteOpen, setPaletteOpen] = useState(false);

  // Router-driven state — read via hooks
  const location = useLocation();
  const params = useParams();        // empty at App level; populated inside routes
  const [searchParams] = useSearchParams();

  const tab: Tab = tabFromPath(location.pathname);
  const roster: RosterId = parseRosterParam(searchParams.get("roster"));
  const archetypeFilter: Archetype | null =
    parseArchetypeParam(searchParams.get("archetype"), data.archetypes);

  // selected — derived inside <OfficerRoute>, NOT here at App level.
  // For STOA_STATE we resolve it from the URL pathname:
  const selected: Officer | null = (() => {
    const m = location.pathname.match(/^\/officer\/([^/?]+)/);
    if (!m) return null;
    return data.officers.find((o) => o.name === m[1]) ?? null;
  })();

  // ⌘K hotkey effect — unchanged
  useEffect(() => { /* same */ }, []);

  /**
   * window.STOA_STATE — read-only-by-convention runtime state bridge for
   * downstream Claude Code skill consumers (acb-007 agent-design-tutor and
   * future Chrome MCP scripts). Mirrors the small set of top-level React
   * state fields the skill needs to drive the app deterministically without
   * DOM-scraping inline styles.
   *
   * Shape:
   *   {
   *     dark: boolean,                        // theme mode, from useTheme()
   *     currentTab: "team" | "skills" | "meta",
   *     selectedOfficer: Officer | null,      // null when on the team grid
   *     roster: RosterId,                     // active roster filter
   *     archetypeFilter: Archetype | null,    // active archetype chip, or null
   *   }
   *
   * Source of truth (post-acb-009): URL is canonical for currentTab,
   *   selectedOfficer, roster, and archetypeFilter — read via useLocation,
   *   useParams (resolved at App level by pathname-matching, since useParams
   *   only populates inside routed children), and useSearchParams. `dark`
   *   continues to come from useTheme(). The exposed shape and contract
   *   surfaces below are unchanged from acb-008.
   *
   * Contract:
   *   • Read-only by convention. Consumers MUST NOT mutate the object;
   *     mutations would be silently overwritten on the next render anyway.
   *     If a future arc needs a write API, that's a separate dispatch
   *     (`window.STOA_DISPATCH`); explicitly out of scope for acb-008/009.
   *   • Single-object replace per render — observers can detect changes via
   *     reference equality (`prev !== window.STOA_STATE`). We do not mutate
   *     in place. Each effect run produces a fresh object literal.
   *   • Timing: this effect runs after React's commit phase, so consumers
   *     reading STOA_STATE synchronously immediately after dispatching a UI
   *     event (e.g., right after `element.click()`) will see the prior
   *     snapshot. Wait one microtask (`await Promise.resolve()` or
   *     `setTimeout(0)`) — or observe for reference inequality on the next
   *     tick — before reading.
   *
   * The `(window as any)` cast is intentional v1; consumers read this from
   * plain JS where TS typing is not needed. Adding an ambient declaration
   * (`declare global { interface Window { STOA_STATE: ... } }`) is
   * explicitly out of scope per acb-008 §4 — follow-up if a TS consumer
   * emerges.
   */
  useEffect(() => {
    (window as any).STOA_STATE = {
      dark,
      currentTab: tab,
      selectedOfficer: selected,
      roster,
      archetypeFilter,
    };
  }, [dark, tab, selected, roster, archetypeFilter]);

  // ... rest of App
}
```

**Critical structural change:** `App` itself must be inside `<HashRouter>` for `useLocation`, `useParams`, `useSearchParams` to work. So `<HashRouter>` wraps `<App>` in `main.tsx` (see §8). `useParams()` at App level returns an empty object — that's fine; we resolve `selected` from `location.pathname` directly via regex (see the IIFE in the diff sketch). This is intentional: we want `selected` resolvable at App level for the STOA_STATE bridge, even though the routed `<OfficerRoute>` also reads `useParams()`.

**Effect deps unchanged in shape** — `[dark, tab, selected, roster, archetypeFilter]` — but the values now come from hooks rather than `useState`. React still re-renders on URL change (because `useLocation` + `useSearchParams` subscribe), so the deps trigger correctly.

**Object identity:** `selected` resolves through `data.officers.find(...)`, which returns the SAME `Officer` object reference if the URL hasn't changed (since `data.officers` is stable from `SAMPLE_DATA`). Effect deps are identity-compared; this means the effect doesn't re-run on every render — only on actual URL change. This matches acb-008's contract.

---

## §7 — Vitest scaffold (deferral)

**Per §1 verdict: deferred to follow-up `acb-009-followup-route-resolution-test`.** This arc does NOT add Vitest config, RTL, or any test files. Spec §5 DoD #5 is satisfied at the follow-up's landing, gated on acb-002's Vitest scaffold. The other 5 DoD criteria (1, 2, 3, 4, 6) are verified by VERA at runtime in this arc.

**ARGUS audit checklist for this deferral:**
- Is the runtime probe enough for THIS arc's confidence? (Deep-link, refresh, back/forward, palette URL navigation, STOA_STATE update — all VERA-probable.)
- Is the follow-up plan concrete enough? (One file, 30 LoC, fixed shape, ADA-direct.)
- Is there a session-boundary risk? (Per global rule, known bugs do not cross session boundaries without a written plan. Deferral here ships with a written plan; the plan will be filed as a brief at acb-002 dispatch time.)

If ARGUS judges deferral inadequate, the bundle path (Vitest scaffold added here) is the fallback.

---

## §8 — Files touched

| File | Action | Line-count delta (rough) |
|------|--------|--------------------------|
| `package.json` | add `react-router@^7.14.2` to dependencies | +1 line |
| `src/main.tsx` | wrap `<App>` in `<HashRouter>` (outside `<ThemeProvider>`) | +2 / -0 |
| `src/App.tsx` | remove 4 `useState` declarations; add router hook reads; refactor `<App>`'s render to use `<Routes>`; add `<TeamRoute>`, `<OfficerRoute>`, `<SkillPlaceholder>`, `<MetaPlaceholder>`, `<NotFoundRoute>` inline; rewrite all callsites in §5; update STOA_STATE effect | +100 / -40 (net ~+60) |
| `src/Components.tsx` | possibly wrap `<SkillCard>` body in `<Link>` (or add an `onClick` prop wired upstream) — preserves `skill-card-{name}` testid | +5 / -0 |
| `agents/follow-ups/acb-009-followup-route-resolution-test.md` | NEW — concrete plan for the deferred Vitest test | +30 (new file) |

**Total touched files: 4 source + 1 brief = 5.** Diff size ~150 LoC net. Medium blast radius; ARGUS critique surface is the routing seam, the STOA_STATE rewire, and the default-stripping helper.

**Files NOT touched (defensive list):** `src/data/*` (no data shape change), `src/hooks/useTheme.tsx` (theme is unchanged), `src/styles/*` (no visual change), `tsconfig.json` (no compiler config change), `vite.config.ts` (no build config change beyond what react-router brings in via npm).

---

## §9 — Risks

### R1 — Multiple `setSearchParams` calls in one tick don't compose (load-bearing footgun)

Per [React Router useSearchParams docs](https://reactrouter.com/api/hooks/useSearchParams): "Multiple calls to setSearchParams in the same tick will not build on the prior value." If a single user action triggers two filter changes (e.g., a future "set archetype AND clear roster" affordance), the second call clobbers the first.

**Current arc: not exercised.** Each callsite in §5 is a single setter per click. But the `setSearchParamsStripDefaults` helper is structured as a single call with an updater fn, so we're already on the right path.

**Mitigation:** the helper's updater-function pattern + single `setParams(next)` call per invocation makes this structurally impossible within one helper call. ADA preserves this discipline; if future code adds a multi-setter affordance, it batches into one updater-fn call.

**ARGUS audit note:** verify the helper signature forces single-call composition (no escape hatch where a caller can chain two `setParams` in a row).

### R2 — `useNavigate()` called during render warning

Per multiple v6/v7 issue threads, `navigate()` called during render produces warnings or no-ops. Current pattern in §5 puts `navigate()` inside `onClick` handlers (deferred until user interaction) — safe.

**Edge case:** the `<NotFoundRoute>` for `*`. If we use `<Navigate to="/" replace />` declaratively, that's safe; if we use `useEffect(() => navigate("/"), [])`, that's also safe. Avoid `navigate()` directly in the component body.

**Mitigation:** ADA uses `<Navigate>` declaratively for any auto-redirect, and `useEffect(() => navigate(...))` if behavior depends on state.

### R3 — StrictMode double-mount of effects

React 19 StrictMode double-invokes effects in dev. The STOA_STATE effect has been double-running since acb-008 — it's idempotent (overwrite same shape) so it's been fine. Nothing changes here.

**New concern:** `<HashRouter>` itself in StrictMode. Per [React Router authentication guide](https://blog.logrocket.com/authentication-react-router-v7/) examples, HashRouter is StrictMode-compatible. No new effect side-effects added.

**Mitigation:** none needed; if dev-only double-render artifacts surface, VERA flags during runtime probe.

### R4 — Hash collision with browser anchors

`HashRouter` uses `#/...` for routing. If someone adds an in-page anchor (`<a href="#some-id">`), it would conflict with router parsing. Currently no anchor-link usage in the app (verified by Grep on `href="#"`).

**Mitigation:** none needed for v1; if a future content section needs anchor scrolling, use `useNavigate()` with `state` or a programmatic scroll, not raw `#anchor`. Document in CATO craft review checklist.

**ARGUS audit note:** verify Grep `href="#` returns zero matches in current src/.

### R5 — Search-param escaping for archetype names

Archetype names are simple alphanumerics (`architect`, `lieutenant`, etc.) — URL-safe. Officer names (`MAJOR_PLINY`) — URL-safe (uppercase + underscore). Skill names: kebab-case (`dispatch-lieutenant`) — URL-safe. Meta-aspect names: kebab-case — URL-safe.

**Edge case flagged in spec §4:** `acb-NNN-testid-special-char-escaping` — adjacent ticket. If gen-data (acb-002) introduces a name with `/`, `?`, `#`, `&`, or `=`, URL paths break. None of these chars currently exist in the data.

**Mitigation:** none needed for v1 data; flagged for acb-002 to enforce identifier-safe naming if dynamic data is added.

### R6 — `<Link>` wrapping vs onClick+navigate — testid preservation

Per spec §4 + acb-008's testid surfaces: `officer-card-{name}`, `skill-card-{name}`, `meta-card-{name}` testids must survive. If we wrap the existing card with `<Link>`, the testid stays on the inner card div (preferred). If we replace the click handler with onClick+navigate, the testid stays on its current element (also fine).

**Decision per D11:** use `onClick={() => navigate(...)}` for cards (cleaner — preserves the existing card structure verbatim and matches the existing onClick pattern). Use `<Link>` for the placeholder route's "back" links and any future inline navigation. Do NOT mix — consistency across cards.

**Mitigation:** ADA preserves testid value verbatim regardless of approach; CATO checks; VERA confirms via testid query in DOM.

### R7 — `selected` resolved via pathname regex at App level (vs `useParams()` inside `<OfficerRoute>`)

This is a known awkwardness. `useParams()` only populates inside a routed child component. For STOA_STATE to expose `selectedOfficer` at App level, we either (a) regex the pathname (chosen, see §6 diff sketch), or (b) lift `selected` state into a context populated by `<OfficerRoute>` and consumed by App.

**Selected approach (a):** simpler — one regex match. Source of truth is still the URL.

**Risk:** regex drift. If routes change (e.g., add `/officers/:name` plural), the regex needs updating in lockstep. Mitigated by colocating the regex with the route definition (both in `App.tsx`) and a comment cross-referencing.

**ARGUS audit note:** verify the regex matches all officer-route paths the `<Routes>` defines, and only those.

### R8 — Default-stripping subtlety (spec §9.7)

If user manually types `?roster=default` into the address bar, the app honors it on initial load. On the next setSearchParams call (e.g., user toggles archetype), `roster=default` gets stripped. This is the intended behavior — URL converges to canonical-minimal form — but it can surprise.

**Mitigation:** ADA documents this in the `setSearchParamsStripDefaults` helper's JSDoc. CATO confirms doc presence. VERA does NOT need to probe this (it's a documented feature, not a bug).

### R9 — `react-router` package vs `react-router-dom` confusion

Spec §3 item 1 said "Add `react-router-dom`". v7 unified the packages; we install `react-router` instead. This is an intentional deviation from spec text, justified by the v7 reality.

**Mitigation:** documented in §2; D6 in decisions table; ARGUS confirms the package choice; CATO confirms imports use `react-router`.

### R10 — Loss of `setTab + setSelected(null)` atomicity

Currently `App.tsx:1076-1079` does `setTab(t); setSelected(null);` atomically (React batches). After migration: a single `navigate("/skills")` does both implicitly (the `/skills` URL has no `:name`, so `selected` resolves to `null`). Atomicity preserved structurally — the URL change is one operation.

**Mitigation:** none needed; the structural change makes atomicity automatic.

### R11 — Vitest deferral session-boundary risk

Per global "fix-now discipline" rule: known bugs don't cross session boundaries without a written plan. The Vitest test deferral has a written plan (§1 follow-up brief sketch), but the brief itself isn't filed as a markdown file in this arc.

**Mitigation:** §1 includes a concrete brief sketch; ADA optionally files `agents/follow-ups/acb-009-followup-route-resolution-test.md` as part of this arc's diff (recommended — it costs ~10 lines and discharges the discipline cleanly). If ADA doesn't, Major Pliny files it at gate.

**This is the risk I'd flag to ARGUS as the most concerning** — deferral without a filed brief is the exact pattern the discipline warns against.

---

## §10 — Open questions for ARGUS

1. **Is the Vitest deferral acceptable, or does ARGUS push for in-arc bundling?** (See §1 + §7.) My call: defer with concrete follow-up. Argue against if you see something I missed.

2. **Is `<Link>`-vs-`onClick+navigate` consistency the right craft call?** I picked `onClick+navigate` for cards (D11) since it preserves existing structure best. If ARGUS prefers `<Link>` everywhere for HTML correctness (right-click "open in new tab" works on `<Link>` but not `onClick`), call it out — it's a real UX tradeoff and I may have under-weighted it.

3. **Should `<HashRouter>` wrap inside or outside `<ThemeProvider>`?** D7 picked outside. Routing is theme-independent; outside is the docs convention. If ARGUS prefers inside (e.g., for a future theme-route coupling), argue.

4. **Does the regex-at-App-level approach for `selected` (R7) feel brittle enough to demand a context-lift refactor?** I went simpler-is-better; ARGUS may judge differently.

5. **Is `useStripDefaultSearchParams` the right helper shape, or should default-stripping live inline at each callsite?** Helper is DRY but adds an indirection. CATO will weigh in.

---

## §11 — Self-assessed weak points

1. **The Vitest deferral is the highest-risk choice in this design.** I am deferring spec §5 DoD #5 to a follow-up arc. The justification is structural (acb-002 owns the scaffold) and the follow-up has a concrete plan. But a deferral with a written plan is still a deferral, and ARGUS should beat hard on whether VERA's runtime probes are actually sufficient confidence for this arc to ship without the test. **Why this shape anyway:** bundling acb-002 doubles the diff scope and bundling a half-scaffold creates a config-merge problem with acb-002. The third option (sequence-with-follow-up) is the smallest cost to all three concerns.

2. **`selected` resolved via pathname regex at App level (R7) is a load-bearing simplification.** The simpler alternative — context-lifting from `<OfficerRoute>` — is more "correct" React but adds a context provider, a consumer, and a mental hop. The regex is 3 lines and lives next to the route definition. **Why this shape anyway:** App-level STOA_STATE needs `selected` resolvable without being inside the routed child; the regex achieves that with the smallest blast radius. If the routes ever get more complex (nested officer routes, plural paths), refactor to context — but that's premature now.

3. **The `useStripDefaultSearchParams` helper is a single-callsite pattern at v1.** Currently only the FilterSidebar calls it (5-6 callsites). Encapsulating in a hook may be over-engineering for one consumer. **Why this shape anyway:** the alternative — inline default-stripping at each call — risks inconsistent stripping logic (one site forgets to strip, URL gains stale `?roster=default`). The helper makes it structurally impossible. CATO may push for inlining; I'd push back, but it's a craft call I could lose without harm to correctness.

4. **`<Link>` vs `onClick+navigate` consistency is undecided across surfaces.** I picked `onClick+navigate` for cards (D11) but `<Link>` for placeholder back-buttons. The mix is defensible (cards have rich existing styling that `<Link>` would constrain; back-buttons are trivial) but ARGUS could argue for total consistency one way or the other. **Why this shape anyway:** card structure preservation is the priority; back-buttons are new and `<Link>` is the idiom for them.

5. **The route-resolution test deferral assumes acb-002 will land in finite time.** If acb-002 stalls indefinitely, the §5 DoD #5 stays unsatisfied. **Why this shape anyway:** acb-002 is Phase 0 and queued-next per the roadmap. Stalling indefinitely would be a separate problem; the deferral is structurally sound conditional on roadmap execution. If roadmap re-prioritization deprioritizes acb-002, this arc gets a follow-up directly to add a minimal Vitest scaffold.

6. **Skill/meta card click → placeholder route is technically NEW affordance, not just migration.** Currently `<SkillCard>` and `<MetaCard>` don't have onClick handlers (they're display-only). Adding navigation makes them interactive, which technically expands acb-009's scope beyond the spec's "migrate existing nav state" framing. **Why this shape anyway:** the placeholder routes (spec §3) need an entry path or they're unreachable. Spec implicitly requires the entry; making it explicit here. If ARGUS judges this as scope creep, we can land routes-only (placeholders unreachable except via direct URL) and add the entry-affordance in a follow-up — but that feels worse.

7. **The `data-testid` preservation approach for cards (R6) is "trust ADA to do the right thing".** I'm not specifying a literal diff — I'm specifying the rule "preserve testid value, structure flexes around it". ADA will pick the structurally cleanest path. **Why this shape anyway:** specifying literal markup pre-empts ADA's craft judgment; the rule is unambiguous and CATO verifies. But ARGUS could ask me to be more concrete; I'd resist (premature concretization is the failure mode in the other direction).

---

## §12 — Sequencing & gates

| Phase | Gate | Owner | Pass condition |
|-------|------|-------|---------------|
| Design lock | this artifact + ARGUS critique | Major Pliny via POLYBIUS | ARGUS findings reconciled; design-locked verdict |
| Build | source edits per §8 | ADA | All §5 callsites migrated; STOA_STATE effect rewired; placeholder routes functional |
| Verify | runtime DoD criteria 1-4 + 6 | VERA | All criteria pass at `localhost:5173` |
| Craft | diff hygiene | CATO | No new hex literals; idiomatic v7 usage; STOA_STATE JSDoc accurate; testids preserved |
| Spec gate | spec-vs-result | Major Pliny | Verdict to POLYBIUS / Colonel |
| Follow-up gate | route-resolution test (separate arc) | filed at acb-002 dispatch | Vitest test green |

---

---

### §13 — Design-time TypeScript compile validation (DAEDALUS-recorded)

**Trigger criterion satisfied:** (b) §8 file-tree section names `src/main.tsx`, `src/App.tsx`, `src/Components.tsx` (`.tsx` paths). Criterion (a) is NOT satisfied — all `tsx`/`ts`-shaped illustrative blocks in this design have been retagged `text` because they are design-shape fragments referencing a larger codebase, not standalone scaffoldable sources.

**Discipline scope qualifier (honest record):** the cu5.41 motivation for this discipline assumes a design's verbatim code blocks are the COMPLETE source set ADA scaffolds. This design's blocks are FRAGMENTS — diff sketches against the existing `src/App.tsx` / `src/Components.tsx`. Scaffolding them in isolation produces thousands of "cannot find name" errors that aren't real defects (they're missing-context errors). The closest meaningful pre-flight is to verify the CURRENT codebase typechecks clean — i.e., the baseline ADA will be diffing against has no pre-existing TS errors. That is what was run.

**Scaffold directory:** N/A — no isolated scaffold; the project's own checkout was used.

**Command:** `npm run typecheck` (= `tsc -b --noEmit`) at repo root `C:/Users/denso/claude_projects/agent-character-builder/`.

**Exit code:** 0

**Combined stdout+stderr:**

~~~~
> agent-character-builder@0.1.0 typecheck
> tsc -b --noEmit
~~~~

(no diagnostic output; tsc clean)

**Total combined output line count:** 2

**Design commit at run time:** 7d07eabed92ee2836dd908c805660de50123e0dd (HEAD before this design was committed; `agents/specs/acb-009-router-url-state.md` is untracked at this SHA — the spec itself was added in the working tree but not yet committed when typecheck ran).

**Notes:** The Phase-1 discipline's verbatim-block-scaffold protocol does not cleanly fit a design that's a diff sketch against an existing app. Two honest options were considered: (1) route to envelope-gap with rationale "design contains diff-fragments not standalone scaffolds"; (2) run the baseline typecheck on the existing codebase to confirm no pre-existing TS errors that would mask later defects. Option (2) was selected — it's the meaningful work the discipline's intent points at for this design shape. ARGUS at cold-audit re-runs `npm run typecheck` at HEAD; same exit-0 expected. The post-build typecheck (after ADA's edits land) is the canonical authority for the proposed-changes' correctness; this pre-flight covers the baseline.

If ARGUS judges this an inadequate substitute for the protocol-prescribed verbatim-scaffold run, route the design back as `discipline-skipped` and PLINY decides whether to (a) require the design's blocks be re-shaped as standalone scaffolds, or (b) accept the diff-against-existing-codebase pre-flight as the discipline's correct application here.

---

## §14 — Post-ARGUS reconciliation

ARGUS critiqued design v1 and surfaced two findings POLYBIUS reconciled into ADA overrides before build:

### Override 1 — File the deferred-Vitest follow-up brief in this arc

ARGUS F1 (procedural blocker) called out that design v1 §1 hedged ADA's responsibility to file `agents/follow-ups/acb-009-followup-route-resolution-test.md` with the word "optionally." Per `C:\Users\denso\.claude\CLAUDE.md:67-69` (fix-now-or-plan-now discipline), known deferrals crossing a session boundary require a ticket-with-plan as a discoverable artifact, not a paragraph in a sibling arc's design.md.

**Reconciled disposition:** ADA MUST file the brief as part of this arc's diff. ADA did. Brief lives at `agents/follow-ups/acb-009-followup-route-resolution-test.md`.

### Override 2 — Drop `useCallback` in `useStripDefaultSearchParams`

ARGUS F3 (footgun concern) called out that the `useCallback` wrapper around the helper had `[params, setParams]` as its dep array; `params` (a URLSearchParams) gets a fresh identity on every URL change, so the callback identity churns each navigation, defeating memoization purpose.

**Reconciled disposition:** ADA dropped the `useCallback` entirely. The helper is now a pure top-level function `stripDefaultSearchParams(params: URLSearchParams): URLSearchParams` at `src/App.tsx:97-103`, called inline at navigate sites. Memoization isn't load-bearing; the simpler shape is correct.

### Effect on D9 + §5

D9 in the §0 decisions table referenced `setSearchParamsStripDefaults` as a hook, and §5's pseudocode showed the `useCallback` shape. Both are now superseded by Override 2. Treat D9 + §5 as design v1 archive; the as-built reality is Override 2 + the in-code helper at `App.tsx:97-103`.

---

**End of design. ARGUS critiques next.**
