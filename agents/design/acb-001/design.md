# acb-001 — Dark mode integration design

**Author:** Denson Smith (Colonel) via DAEDALUS dispatch.
**Status:** Design v2, ready for ADA implementation.
**Spec:** `agents/specs/acb-001-darkmode.md` (locked).
**Project:** The Stoa: agent-character-builder, v0.1 alpha → v0.2 batch-3 first half.
**Working dir:** `C:/Users/denso/claude_projects/agent-character-builder/`.

---

## §0 — Restatement of the brief

PLINY (per spec §1) is asking me to design the integration plan for an end-to-end dark-mode toggle that:
1. Adds a sun/moon button to the persistent header that flips the app between light and dark modes without page reload.
2. Persists the user's choice to `localStorage` and hydrates from `prefers-color-scheme` on first load.
3. Eliminates the `palette` JS const in `src/Components.tsx` (lines 29–53), rewriting every `palette.X` reference across `App.tsx` + `Components.tsx` to `var(--<token>)` so that the existing dark token block in `tokens.css` actually does its job.
4. Routes archetype accent colors through a `[light, dark]` pair lookup (`archColors` map + `useDark()` hook) in the components layer; `data.archetypes` stays light-mode-only.
5. Preserves v0.1 light-mode pixel-perfect parity (no visual regressions).

I write the design only. ADA executes; VERA verifies; CATO reviews.

**Imported assumptions** (surfaced because the restatement gate requires it):
- The current `tsconfig.json` / Vite setup compiles `.ts/.tsx` with strict types as-is — no toolchain change needed for the new `useTheme.ts` hook file.
- The Lucide `Sun` and `Moon` named exports exist in `lucide-react` (they do; verified by inspecting `src/Components.tsx:7-21` import shape — Lucide's API is stable and these names are canonical).
- `index.html` is editable (it is — `index.html:1-15`).
- `data-theme="dark"` set on `<html>` before paint will be honored by `tokens.css:131` (`:root[data-theme="dark"]`), which it is — that selector is exactly what bootstraps a no-FOUC dark first paint.

If any of these are wrong, the design needs revision; none are believed wrong.

---

## §0.5 — Colonel locks (post-DAEDALUS, pre-ARGUS gate)

The Colonel reviewed DAEDALUS's surfaced concerns about light-mode visual changes and ruled. These decisions **override** the body of this design.md where they conflict; the body sections have been edited surgically to match. ARGUS reads this section first.

### Lock 1 — Rank-pill borders: ADD TOKENS, preserve warm-tint rank coding

**Colonel decision:** Option (C) — add `--rank-major-border`, `--rank-captain-border`, `--rank-lieutenant-border` to **both** the `:root` (light) and `:root[data-theme="dark"]` (dark) blocks of `src/styles/tokens.css`. The warm-tint per-rank border is an intentional visual signal (rank coding via color); flattening it loses information.

**Implication:**
- `tokens.css` is now in the edit set (no longer "no edits"). See updated §1 + new §3.6.
- `rankStyles` border values are `var(--rank-major-border)` / `var(--rank-captain-border)` / `var(--rank-lieutenant-border)`, NOT `var(--border-2)`. See updated §3.2.
- §6 Q1 is RESOLVED — token addition is the right answer.

**Spec edit (already applied to `agents/specs/acb-001-darkmode.md`):** §5 #6 changed from "light mode pixel-perfect parity preserved" to "no unintentional visual regressions; intentional consolidations documented in design.md are OK." The rank-border preservation is the canonical example of when a token addition is the right answer instead of consolidating.

### Lock 2 — Meta-chip: ACCEPT CONSOLIDATION

**Colonel decision:** Accept the consolidation. Drop hardcoded lavender in favor of `accent-soft-2 / fg-1 / border-2`. Section headers handle the semantic disambiguation; the lavender was incidental, not load-bearing. Reads cleaner in both modes.

**Implication:**
- No new meta-chip tokens needed.
- §3.2 `chipVariants.meta` rewrite stands.
- §5.6 is locked at resolution #1.
- §6 Q2 is RESOLVED — consolidation is the right answer.

**Spec note:** The meta-chip consolidation is the canonical example of an approved intentional consolidation in spec §5 #6.

### Lock 3 — Card-hover background: ACCEPT prototype's `--bg-inset` (third intentional consolidation)

**Architect decision (DAEDALUS v2, post-ARGUS F3):** Card-hover state changes from `palette.bgApp` (production v0.1) to `var(--bg-inset)` (JSX prototype). Applies to both `OfficerCard` and `SkillCard`.

**Rationale:** the prototype's `bg-inset` is the conventional hover direction in both modes (lighter than surface in dark mode, where production's `bgApp` was darker than surface and reads inverted). In light mode, `bg-app` (`#FAF9F6`) is almost imperceptible against `bg-surface` (`#FFFFFF`); `bg-inset` (`#ECE9E1`) is a clear hover state. In dark mode, `bg-app` (`#14130F`) is *darker* than `bg-surface` (`#1B1A16`) so hovering "down" reads as inverted, while `bg-inset` (`#221F1A`) goes "up" — the conventional direction. This is a small light-mode visible change in `OfficerCard` and `SkillCard` hover states. The JSX prototype is the named reference per spec §9; honoring its hover choice is consistent with the rest of the port.

**Implication:**
- §3.2 `OfficerCard` and `SkillCard` rows: hover background is `var(--bg-inset)`, NOT `var(--bg-app)`.
- §5.1 updated: a third intentional consolidation is on the books, alongside meta-chip (Lock 2) and rank-border-token-add (Lock 1).
- VERA's light-mode parity gate per spec §5 #6 treats this as approved, not a regression.

---

## §0.6 — Dispositions of ARGUS v1 findings

ARGUS audited design v1 (`agents/design/acb-001/argus-v1.md`, verdict PASS-WITH-CONCERNS, 0 blocker / 6 concern / 8 nit). The Colonel routed the architect-tier findings (F1, F2, F3) back to DAEDALUS rather than personally adjudicating. Each finding is dispositioned below; design body sections have been edited surgically per the disposition.

1. **F1: Skill-chip border (`#B7C5DA` → `--border-2`) is an unflagged hue-changing consolidation.** **Disposition:** `accept-as-recommended` (option b). **Rationale:** add a new `--accent-soft-border` token to both modes rather than collapsing the cool-blue accent-family border into the warm-grey neutral border. This aligns with the Lock 1 precedent (rank-border tokens preserve a deliberate visual signal); the accent-tinted skill-chip border is the third reinforcement of the chip's "belongs to accent family" semantic. Light value `#B7C5DA` preserves v0.1 pixel-for-pixel; dark value `#3A4F6E` (justification in §3.6). Also restores cross-chip differentiation that addresses F7's residual concern. **Design-section impact:** §3.2 token table updated (skill-chip border row now maps to `var(--accent-soft-border)`); §3.6 amended to add the new token to both blocks; §1 file table unchanged (tokens.css already in edit set); §4 token coverage table extended.
2. **F2: "Zero FOUC" is a production-build property, not a Vite-dev property.** **Disposition:** `accept-as-recommended` (option a). **Rationale:** add `<link rel="stylesheet" href="/src/styles/tokens.css">` to `index.html`'s `<head>` so tokens are render-blocking in dev. Spec §5 #2 verification runs in dev (`http://localhost:5173/`); the FOUC claim must hold in the verification environment. Vite serves the linked CSS asset; the `@import "./tokens.css"` inside `index.css` continues to work but becomes a no-op for tokens (browsers dedup by URL). No double-load issue. **Design-section impact:** §2.2 FOUC mechanism amended (now describes both inline-script + render-blocking-link); §3.5 `index.html` patch updated to include the `<link>` tag; §1 file table summary line for `index.html` updated; §5.2 amended.
3. **F3: Card-hover direction (production's `bgApp` vs prototype's `bg-inset`).** **Disposition:** `accept-as-recommended` (option b). **Rationale:** port the prototype's `bg-inset` hover direction. `bg-app` is darker than `bg-surface` in dark mode, so production's hover-into-`bg-app` reads as inverted vs the conventional lighter-on-hover direction. In light mode, `bg-app` is barely distinguishable from `bg-surface` while `bg-inset` is a clear hover state. The JSX prototype is the named reference per spec §9; honoring its choice is consistent with the rest of the port. Promoted to a third Colonel-precedent intentional consolidation under §0.5 Lock 3. **Design-section impact:** new §0.5 Lock 3 entry; §3.2 OfficerCard row hover token changed from `var(--bg-app)` to `var(--bg-inset)`; §3.2 SkillCard row hover token changed similarly; §5.1 updated to list three intentional consolidations.
4. **F4: `--fg-on-accent` swap on Button danger is a slight semantic overload.** **Disposition:** `accept` (option a). **Rationale:** `--fg-on-accent` is overloaded but reasonable for any "white-ish text on a saturated colored bg." Light value is byte-identical `#FFFFFF`; dark value `#FAF9F6` is sub-perceptible against the danger-red `#D17878`. If a future arc needs a distinct `--fg-on-danger` token, the substitution is one-line. Documented in §3.2 commentary. **Design-section impact:** §3.2 Button row commentary already notes the overload; no further edits required beyond a clarifying note.
5. **F5: Dispatch brief carried an inverted `--fg-on-accent` claim.** **Disposition:** `accept` (parent-session note only). **Rationale:** brief defect, not design defect. The design's mapping is correct (light `#FFFFFF`, dark `#FAF9F6`). **Design-section impact:** none.
6. **F6: Dark rank-border hexes are designer-judgment values.** **Disposition:** `accept` as-is. **Rationale:** ARGUS confirms each border is on-hue with its rank family and has adequate contrast against its dark `--rank-*-bg`. Not muddy. A formula-derived approach (e.g., OKLCH lightness shift) would land in the same neighborhood and could be a follow-up tokens-system arc — not blocking. Confirmed in §3.6 self-flag note. **Design-section impact:** none beyond a confirmatory note in §3.6.
7. **F7: Meta-chip vs skill-chip in light mode are visually similar pale-blue family.** **Disposition:** `accept` (Colonel-locked consolidation; verification responsibility on VERA). **Rationale:** the Colonel's Lock 2 stands; section headers ("Callable lieutenants" vs "Required reading" in `DetailSidebar`) are the load-bearing disambiguator. F1's resolution (adding `--accent-soft-border` to skill-chip) restores some cross-chip visual differentiation as a side benefit. VERA explicitly checks header presence and prominence per §6. **Design-section impact:** §6 amended to call out VERA's cross-chip-header check; F1 cross-reference noted.
8. **F8: `data.archetypes` becomes redundant post-refactor.** **Disposition:** `defer-to-followup`. **Rationale:** ticket already filed at `agents/follow-ups/acb-002-followup-archetypes-dedup.md` per ARGUS suggestion. acb-002 already touches the data layer and the cleanup composes naturally there. Spec §4 explicitly excludes edits to `src/data/sample.ts` in this arc. **Design-section impact:** §6 Q8 amended to point at the filed follow-up.
9. **F9: `OfficerCard` testability — requires `<ThemeProvider>` ancestor post-refactor.** **Disposition:** `accept`. **Rationale:** v0.2 has no Vitest scaffold (acb-002 brings it for adapter testing only); component-level visual or behavioral tests are not in scope. The fix when v0.3 component tests arrive is a `renderWithTheme` test helper — a 5-line wrapper. Document the requirement in a JSDoc comment on `OfficerCard`. **Design-section impact:** §3.2 OfficerCard row gains a JSDoc note in its signature description.
10. **F10: localStorage key `"acb-theme"` duplicated in two places.** **Disposition:** `accept`. **Rationale:** drift risk is real but small; introducing a constants module for a single key is overkill. If a future arc adds a second client-side localStorage key, extract both at that point. **Design-section impact:** §6 Q4 confirms the disposition explicitly.
11. **F11: `<StrictMode>` + Context double-effect is idempotent — verification.** **Disposition:** `accept`. **Rationale:** confirmed by ARGUS reading the §2.1 sketch; both invocations write the same value. No defect. **Design-section impact:** §5.3 amended to note ARGUS confirmation.
12. **F12: Inline `matchMedia` is a one-shot read; spec §10 #5 honored.** **Disposition:** `accept`. **Rationale:** confirmed by ARGUS reading the §3.5 inline script body. No `addEventListener("change", …)` call. **Design-section impact:** §5.5 amended to note ARGUS confirmation.
13. **F13: Sun/Moon imports are additive surface only.** **Disposition:** `accept`. **Rationale:** confirmed; same package as existing icons. **Design-section impact:** none.
14. **F14: Inline ES5 script vs TypeScript universe.** **Disposition:** `accept`. **Rationale:** standard pattern; simpler than extracting to a pre-bundled JS asset. **Design-section impact:** none.

**Summary:** 3 `accept-as-recommended` (F1, F2, F3 — all architect-tier, all accept ARGUS's recommended option), 9 `accept` (F4, F6, F7, F9, F10, F11, F12, F13, F14), 1 `defer-to-followup` (F8 → `acb-002-followup-archetypes-dedup`), 1 parent-session note only (F5 — brief defect, not design defect). Total: 14 dispositions for 14 findings. No overrides of ARGUS's recommendations. No findings escalated back to the Colonel. New tokens added: `--rank-major-border`, `--rank-captain-border`, `--rank-lieutenant-border` (Lock 1, light + dark = 6 declarations) and `--accent-soft-border` (F1, light + dark = 2 declarations). Total new files: 1 (`src/hooks/useTheme.tsx`); total edited files: 5 (unchanged from v1).

---

## §1 — Files touched

| Path | Edit type | One-line summary |
|---|---|---|
| `src/Components.tsx` | **heavy** | Delete `palette` const (lines 29–53). Add `archColors` map + `useDark()`-style consumption pattern. Rewrite every styled element to `var(--…)` + tokens. Rewrite `RankPill` to use `--rank-*-bg` / `--rank-*` / `--border-2`. Rewrite `Chip` variants to use tokens. Rewrite `Button` variants to use tokens (incl. `--fg-on-accent`, `--danger`). `OfficerCard` accepts `archetype` and resolves color via `useTheme()` instead of receiving `archColor` prop. |
| `src/App.tsx` | **heavy** | Replace every `palette.X` reference with `var(--…)` in inline styles. Remove `palette` from imports (line 10). Remove `archColor` / `archetypes` prop drilling for `OfficerCard` and `OfficerDetail` — both now consume archetype color via the new context-aware `ArchetypeText` / via local `useTheme()` calls. Header gains a `<ThemeToggle/>` slot in the right cluster (between "New agent" and the Settings icon). `App` is wrapped in `<ThemeProvider>`. |
| `src/main.tsx` | **light** | Wrap `<App/>` in `<ThemeProvider>` (one import + one tag). No theme-bootstrap code lives here — bootstrap is in `index.html` for FOUC reasons (see §2.2). |
| `src/hooks/useTheme.tsx` | **new** | New file. Exports `ThemeProvider` (React Context provider) and `useTheme()` hook returning `{ dark: boolean; toggle: () => void; setDark: (d: boolean) => void }`. Provider owns the React state, syncs `data-theme` on `<html>`, and writes to `localStorage` on every change. |
| `index.html` | **light** | (1) Add a `<link rel="stylesheet" href="/src/styles/tokens.css">` in `<head>` so tokens are render-blocking in dev (per ARGUS F2 / §0.6 disposition #2). (2) Add a synchronous inline `<script>` in `<head>` (~10 lines) that reads `localStorage["acb-theme"]` (with `try/catch`) or falls back to `matchMedia("(prefers-color-scheme: dark)")`, then sets `document.documentElement.dataset.theme` before HTML body paints. The link + inline-script combination delivers zero FOUC in BOTH dev (`npm run dev`) and prod (`npm run build && npm run preview`). |
| `src/styles/tokens.css` | **light** | (1) Add three new rank-border tokens to both blocks: `--rank-major-border`, `--rank-captain-border`, `--rank-lieutenant-border` (per §0.5 Lock 1). (2) Add `--accent-soft-border` to both blocks (per ARGUS F1 / §0.6 disposition #1) — light `#B7C5DA` (preserves v0.1 skill-chip border), dark `#3A4F6E` (mid-blue, on-hue with the dark accent family). Rationale: Colonel-locked decision per §0.5 Lock 1 plus DAEDALUS architect-tier accept of ARGUS F1 to preserve the cool-blue accent-family border on skill chips rather than consolidate to `--border-2`. See §3.6. |

**Total new files:** 1 (`src/hooks/useTheme.tsx`).
**Total edited files:** 5 (`Components.tsx`, `App.tsx`, `main.tsx`, `index.html`, `tokens.css`).
**Out-of-scope files explicitly NOT touched:** `src/data/sample.ts`, `src/data/types.ts`, `src/data/adapter.ts` (per spec §4 + decision 2).

---

## §2 — Architecture

### §2.1 — `useDark()` mechanism: React Context, not MutationObserver

**Choice: React Context.** `src/hooks/useTheme.tsx` exports a `<ThemeProvider>` and a `useTheme()` hook.

```tsx
// src/hooks/useTheme.tsx (sketch)
import { createContext, useContext, useEffect, useState } from "react";
import type { ReactNode } from "react";

type ThemeCtx = { dark: boolean; toggle: () => void; setDark: (d: boolean) => void };

const Ctx = createContext<ThemeCtx | null>(null);

export function ThemeProvider({ children }: { children: ReactNode }) {
  // Read initial state from <html data-theme="...">. The inline bootstrap
  // script in index.html has already set this before React mounts, so this
  // initializer always returns the correct value (no FOUC, no flash).
  const [dark, setDarkState] = useState(
    () => document.documentElement.dataset.theme === "dark"
  );

  useEffect(() => {
    document.documentElement.dataset.theme = dark ? "dark" : "light";
    try {
      localStorage.setItem("acb-theme", dark ? "dark" : "light");
    } catch {
      // localStorage disabled / quota exceeded — silently noop. Choice still
      // applies for the current session via React state.
    }
  }, [dark]);

  const value: ThemeCtx = {
    dark,
    setDark: setDarkState,
    toggle: () => setDarkState((d) => !d),
  };
  return <Ctx.Provider value={value}>{children}</Ctx.Provider>;
}

export function useTheme(): ThemeCtx {
  const v = useContext(Ctx);
  if (!v) throw new Error("useTheme called outside ThemeProvider");
  return v;
}
```

**Why Context over MutationObserver (the JSX-prototype default):**

1. **Single source of truth.** With Context, `dark` lives in React state; the toggle button calls `toggle()` and every consumer re-renders immediately. With MutationObserver, the source of truth is a DOM attribute, the toggle is a side-effect that mutates the attribute, and every consumer subscribes to a DOM mutation event — a needless round-trip.
2. **Works cleanly under `<StrictMode>`.** `main.tsx:7` wraps `<App/>` in `<StrictMode>`, which double-invokes effect mounts in dev. A MutationObserver subscribed in an effect double-subscribes (and double-unsubscribes), which is fine but noisy. A Context provider does not have this property.
3. **Eliminates the bootstrap-vs-state-race edge case.** If a consumer calls `useDark()` before the App-level effect has run that sets `data-theme`, MutationObserver-based hooks see the wrong initial value (light, by default). With our setup, the inline `index.html` script sets `data-theme` synchronously before React mounts, AND the Context provider reads from the same DOM attribute on first render — both paths converge on the correct value.
4. **Cheaper.** No DOM observer, no event-listener lifecycle. Just `useContext`.

**The JSX prototype uses MutationObserver because** it has no top-level `<App/>` provider scaffold — it's a single-file inline-script demo, where wrapping in a provider would be a structural shift. In the production codebase we already wrap in `<StrictMode>` and adding `<ThemeProvider>` is a one-line addition. Different constraint, different right answer.

**Public API of `useTheme()`** for component authors:
- `dark: boolean` — current mode. Components like `ArchetypeText`, `OfficerCard`, `FilterSidebar` call this to pick from `archColors[archetype][dark ? 1 : 0]`.
- `toggle(): void` — wired to the `<ThemeToggle/>` button click.
- `setDark(d: boolean): void` — exposed for any future programmatic flip (not used in v0.2; included for API completeness).

### §2.2 — Theme bootstrap location: inline script + render-blocking stylesheet in `index.html`

**Choice: render-blocking `<link rel="stylesheet" href="/src/styles/tokens.css">` immediately followed by a synchronous inline `<script>` in `index.html`'s `<head>`, before the `<script type="module" src="/src/main.tsx">` tag.** This is a two-part FOUC mitigation; both parts are required.

```html
<!-- index.html, inside <head>, before the module script -->
<script>
  (function () {
    try {
      var stored = localStorage.getItem("acb-theme");
      var dark = stored
        ? stored === "dark"
        : window.matchMedia &&
          window.matchMedia("(prefers-color-scheme: dark)").matches;
      document.documentElement.setAttribute(
        "data-theme",
        dark ? "dark" : "light"
      );
    } catch (e) {
      // localStorage / matchMedia unavailable — default to light.
      document.documentElement.setAttribute("data-theme", "light");
    }
  })();
</script>
```

**Why inline-in-head + render-blocking link:**

| Option | FOUC behavior (dev) | FOUC behavior (prod) | Verdict |
|---|---|---|---|
| Inline `<script>` + `<link rel="stylesheet">` for tokens.css in `<head>` (this design) | Zero. The `<link>` is render-blocking; the inline script sets `data-theme` synchronously; `:root[data-theme="dark"]` resolves on first paint. | Zero. Same mechanism; production also extracts CSS via Vite's build to a `<link>` in `<head>` (would have been render-blocking anyway). | **Chosen.** |
| Inline `<script>` only, tokens.css imported via `index.css` via `main.tsx` | Possible flash. ES modules are deferred per the HTML spec; in Vite dev mode CSS travels through the module graph and is injected via `<style>` after JS evaluates. Window between body parse and CSS injection where browser may paint with no CSS variables defined → browser-default white background regardless of `data-theme` attribute. | Zero — Vite production extracts CSS to a `<link>` in `<head>` automatically. | Rejected — fails dev parity with prod. ARGUS F2. |
| Synchronous block at top of `src/main.tsx` | Flash. Vite serves `main.tsx` as `<script type="module">`, async by default; body paints before main.tsx's first line. | Flash. Same async-module property. | Rejected. |
| App-level `useEffect` | Worst flash. Module loads, React parses, `<App/>` mounts in light mode, *then* effect runs. Visible flash on every cold load when stored choice is dark. | Same. | Rejected. |

**FOUC mitigation summary (post-ARGUS F2):** TWO mechanisms in tandem. (1) The render-blocking `<link rel="stylesheet" href="/src/styles/tokens.css">` in `<head>` ensures the CSS variable definitions are loaded and applied before first paint, in BOTH dev and prod. Browsers dedup CSS by URL, so the existing `@import "./tokens.css"` inside `src/styles/index.css` becomes a no-op (the link tag's load satisfies it). (2) The inline `<script>` runs synchronously between the `<link>` parse and any module evaluation, setting `data-theme` on `<html>` before body paint. Together: tokens are defined for both modes before paint AND the correct mode is selected before paint → `:root[data-theme="dark"]` resolves correctly on first paint, no flash. The inline script is ~10 lines of vanilla JS, blocks parsing for sub-millisecond, and is the standard pattern (Vercel, Tailwind docs, Linear, GitHub all do this).

**Why not duplicate the bootstrap in main.tsx + index.html "for safety":** because the React initial state (`useState(() => document.documentElement.dataset.theme === "dark")` inside `ThemeProvider`) reads the value the inline script already set. Duplication invites drift between the two paths. Single source of truth: index.html sets the attribute; ThemeProvider reads it.

### §2.3 — Toggle button placement: new slot in header right cluster

**Choice: insert `<ThemeToggle/>` between the "New agent" Button and the Settings gear in the header right cluster.**

Current header right cluster (`src/App.tsx:80-120`):
```
Search trigger → "New agent" Button → Settings gear
```

New header right cluster:
```
Search trigger → "New agent" Button → ThemeToggle → Settings gear
```

**Rationale:**
- Matches the JSX prototype exactly (`design_handoff_character_builder/ui/App.jsx:27`).
- Reading order is correct: search (find) → primary CTA (create) → mode controls (theme + settings) clusters mode-related controls together visually.
- Header is `position: sticky; top: 0; z-index: 10` (`src/App.tsx:46-49`), so toggle is visible on Team / Officer Detail / Skills / Meta-aspects — passes the spec §5 #1 visibility requirement.
- Does NOT replace "New agent" (the primary CTA stays primary).
- Does NOT crowd the search input: header has plenty of horizontal room and the toggle is icon-only (~26px wide + 10px gap).

`<ThemeToggle/>` styling matches the JSX prototype (`design_handoff_character_builder/ui/Components.jsx:221-230`):
```tsx
function ThemeToggle() {
  const { dark, toggle } = useTheme();
  return (
    <button
      onClick={toggle}
      title={dark ? "Switch to light" : "Switch to dark"}
      style={{
        background: "transparent",
        border: "1px solid var(--border-1)",
        borderRadius: 6,
        padding: "5px 8px",
        cursor: "pointer",
        color: "var(--fg-2)",
        display: "inline-flex",
        alignItems: "center",
      }}
    >
      {dark ? <Sun size={14} /> : <Moon size={14} />}
    </button>
  );
}
```

**Icon convention: show the *target* mode.** Currently dark → render `<Sun/>` (click to go light). Currently light → render `<Moon/>` (click to go dark). This matches GitHub, Vercel, Linear, and MDN, and the JSX prototype (`Components.jsx:227`). Title attribute confirms: "Switch to light" / "Switch to dark".

### §2.4 — `archColors` map placement

Per spec §6 decision 2: `archColors` lives in `Components.tsx` (NOT `data/sample.ts`), keyed by `Archetype` from `data/types.ts`.

```tsx
// src/Components.tsx (new export)
import type { Archetype } from "./data/types";

export const archColors: Record<Archetype, [string, string]> = {
  orchestrator: ["#5B4D86", "#9D8FCB"],
  architect:    ["#2E6E63", "#6FB5A8"],
  verifier:     ["#785637", "#C29A75"],
  executor:     ["#4A6E2E", "#8FB575"],
  reviewer:     ["#6E2E4A", "#C7889F"],
  "plan-critic":["#6E4A2E", "#C29A75"],
  researcher:   ["#2E4A6E", "#7CA1D4"],
  curator:      ["#4A2E6E", "#A88FCB"],
  intake:       ["#6E6E2E", "#C2C275"],
  scout:        ["#2E6E4A", "#75C29A"],
};

export function archColorFor(archetype: Archetype, dark: boolean): string {
  return archColors[archetype][dark ? 1 : 0];
}
```

`data.archetypes` (`src/data/sample.ts:124-135`) stays unchanged — still a `Record<Archetype, string>` of the light-mode-only colors. **It is no longer referenced** by `App.tsx` after this arc (the `archetypes` prop drilling collapses) — but we leave it in the data shape for the Filter Sidebar's "All / Archetype list" enumeration (`Object.keys(archetypes)` is still the canonical list of archetypes for that UI). The colors in `data.archetypes` become functionally redundant with `archColors[arch][0]` in the components layer — flagged in §5 as a self-assessed weak point, with a deliberate decision to leave it for now.

---

## §3 — Edit plan per file

### §3.1 — `src/hooks/useTheme.tsx` (NEW)

Create the file with the exact contents of the sketch in §2.1. Key details for ADA:

- File extension is `.tsx` (not `.ts`) because JSX is used in the provider's return.
- `import { createContext, useContext, useEffect, useState } from "react";` — no extra packages.
- `import type { ReactNode } from "react";` — type-only import.
- Export both `ThemeProvider` and `useTheme`.
- Initial state: `useState(() => document.documentElement.dataset.theme === "dark")`. The lazy initializer matters — running this synchronously inside the useState argument-fn ensures we read `data-theme` after the inline bootstrap script has set it.
- Effect dependency array: `[dark]`.
- localStorage write wrapped in `try { … } catch { /* noop */ }` per spec §10 #4 defensive read.
- localStorage key: **`"acb-theme"`** (string literal; not extracted to a constant — used in only two places, here and in `index.html`'s inline script).

### §3.2 — `src/Components.tsx` (HEAVY)

**Delete:**
- Lines 29–53: the entire `palette` const + its `as const` export.
- Line 14 import `ArrowRight`, `X`, `Filter`, `Check`, `FileText`, `Package`, `Users` — only if these are unused after the refactor; verify before deleting (this is a pre-existing cleanup but in scope of "what palette references are deleted"). **Actually leave the icon imports alone** — they're in the `icons` re-export at line 370; not part of palette deletion. Only `palette` is deleted.

**Add (new exports, after the imports block):**
- `archColors` map, typed `Record<Archetype, [string, string]>`.
- `archColorFor(archetype, dark)` helper.

**Add (top of file, alongside other imports):**
- `import { useTheme } from "./hooks/useTheme";`

**Rewrite per-component:**

| Component | Edit |
|---|---|
| `Mark` (line 58–70) | `style={{ color: palette.fg1 }}` → `style={{ color: "var(--fg-1)" }}`. |
| `Button` (line 87–124) | `variants.primary`: `palette.accent` → `"var(--accent)"`; `color: "#fff"` → `color: "var(--fg-on-accent)"`; `borderColor: palette.accent` → `"var(--accent)"`. `variants.secondary`: `palette.fg1` → `"var(--fg-1)"`; `palette.border2` → `"var(--border-2)"`. `variants.ghost`: `palette.fg1` → `"var(--fg-1)"`. `variants.danger`: `"#9B3A3A"` → `"var(--danger)"` (×2: bg + border); `color: "#fff"` → `"var(--fg-on-accent)"`. **Per ARGUS F4 / §0.6 disposition #4:** `--fg-on-accent` is semantically overloaded for the danger variant (the token is named for accent buttons), but the visual impact is sub-perceptible — light-mode value is byte-identical `#FFFFFF`, dark-mode value `#FAF9F6` is near-white on a saturated danger red. Accepted as overload. If a future arc adds a distinct `--fg-on-danger` token, the substitution is one-line. |
| `rankStyles` (line 129–133) | Replace the entire object: `major: { bg: "var(--rank-major-bg)", fg: "var(--rank-major)", border: "var(--rank-major-border)" }`; same shape for `captain` and `lieutenant` with the matching token names. **Borders use the new `--rank-*-border` tokens** (added to `tokens.css` per §3.6 + §0.5 Lock 1) — preserves the v0.1 warm-tint per-rank border coding in both modes. |
| `RankPill` (line 135–156) | No structural change; just consumes the rewritten `rankStyles`. Border stays `1px solid ${s.border}` template-literal — `s.border` is now a `var(--…)` string, which works inside template literals fine (CSS resolves the variable). |
| `ArchetypeText` (line 161–174) | **Signature change.** Currently `({ archetype, color }: { archetype: Archetype; color: string })`. New: `({ archetype }: { archetype: Archetype })`. Internal: `const { dark } = useTheme(); const color = archColorFor(archetype, dark);`. Style line: `color` (the resolved hex). |
| `chipVariants` (line 181–185) | Rewrite all three: `tool: { bg: "var(--bg-inset)", fg: "var(--fg-2)", border: "var(--border-1)" }`. `skill: { bg: "var(--accent-soft)", fg: "var(--accent)", border: "var(--accent-soft-border)" }` (was `"#B7C5DA"`). `meta: { bg: "var(--accent-soft-2)", fg: "var(--fg-1)", border: "var(--border-2)" }` (was hardcoded `#F1EEF7` / `#5B4D86` / `#E0DAEC`). **Per ARGUS F1 / §0.6 disposition #1:** the skill-chip border now routes through a NEW `--accent-soft-border` token (added to `tokens.css` per §3.6) rather than collapsing to `--border-2`. Light value `#B7C5DA` preserves v0.1 pixel-for-pixel; dark value `#3A4F6E` is on-hue with the dark accent family. The accent-tinted border is the third reinforcement of the chip's "belongs to accent family" semantic (alongside `accent-soft` bg and `accent` fg). The meta-chip rewrite matches the JSX prototype line 104 exactly — it deliberately drops the lavender tint in favor of an accent-soft-2 / fg-1 pair that has correct contrast in both modes. **The meta-chip change is a small visible style change to meta chips; flagged in §5.** The skill-chip change is now token-preserving in light mode (no visual regression). |
| `Chip` (line 187–218) | No structural change; consumes rewritten `chipVariants`. |
| `OfficerCard` (line 223–280) | **Signature change.** Currently `({ officer, archColor, onClick }: { officer: Officer; archColor: string; onClick?: () => void })`. New: `({ officer, onClick }: { officer: Officer; onClick?: () => void })`. **Per ARGUS F9 / §0.6 disposition #9:** add a JSDoc comment above the function declaration: `/** Officer card. Requires a <ThemeProvider> ancestor (consumes useTheme() for archetype color resolution). When v0.3 component tests arrive, wrap with a renderWithTheme helper. */`. Internal: `const { dark } = useTheme(); const archColor = archColorFor(officer.archetype, dark);`. Style block: every `palette.bgSurface` → `"var(--bg-surface)"`, `palette.border1` → `"var(--border-1)"`, `palette.fg1` / `palette.fg2` → `var(...)` equivalents. **Hover background per ARGUS F3 / §0.5 Lock 3 / §0.6 disposition #3:** `hover ? palette.bgApp : palette.bgSurface` becomes `hover ? "var(--bg-inset)" : "var(--bg-surface)"` (NOT `var(--bg-app)`). This ports the JSX prototype's hover direction; reads correctly in both modes. `boxShadow: "0 1px 2px rgba(20,18,12,0.04)"` → `"var(--shadow-1)"` (uses the tokenized shadow which is theme-aware). The `<ArchetypeText archetype={officer.archetype} color={archColor}/>` call drops the `color` prop: `<ArchetypeText archetype={officer.archetype}/>`. |
| `SkillCard` (line 285–363) | Same rewrite pattern as `OfficerCard` for every `palette.X` reference. **Hover background per ARGUS F3 / §0.5 Lock 3 / §0.6 disposition #3:** `hover ? palette.bgApp : palette.bgSurface` becomes `hover ? "var(--bg-inset)" : "var(--bg-surface)"` (NOT `var(--bg-app)`). No archetype color (skills aren't archetyped). |

**Token mapping reference (full table for ADA):**

| `palette.X` (delete) | New CSS variable |
|---|---|
| `bgApp` | `var(--bg-app)` |
| `bgSurface` | `var(--bg-surface)` |
| `bgSunken` | `var(--bg-sunken)` |
| `bgInset` | `var(--bg-inset)` |
| `fg1` | `var(--fg-1)` |
| `fg2` | `var(--fg-2)` |
| `fg3` | `var(--fg-3)` |
| `fg4` | `var(--fg-4)` |
| `border1` | `var(--border-1)` |
| `border2` | `var(--border-2)` |
| `border3` | `var(--border-3)` (currently unused; dead palette key — fine to drop with no replacement needed) |
| `accent` | `var(--accent)` |
| `accentHover` | `var(--accent-hover)` (currently unused; dead palette key) |
| `accentSoft` | `var(--accent-soft)` |
| `rankMajBg` | `var(--rank-major-bg)` |
| `rankMaj` | `var(--rank-major)` |
| `rankMajBorder` | `var(--rank-major-border)` (token added in §3.6) |
| `rankCapBg` | `var(--rank-captain-bg)` |
| `rankCap` | `var(--rank-captain)` |
| `rankCapBorder` | `var(--rank-captain-border)` (token added in §3.6) |
| `rankLtBg` | `var(--rank-lieutenant-bg)` |
| `rankLt` | `var(--rank-lieutenant)` |
| `rankLtBorder` | `var(--rank-lieutenant-border)` (token added in §3.6) |
| Hardcoded `"#fff"` (Button primary/danger) | `var(--fg-on-accent)` |
| Hardcoded `"#9B3A3A"` (Button danger) | `var(--danger)` |
| Hardcoded `"#B7C5DA"` (skill chip border) | `var(--accent-soft-border)` (NEW token added in §3.6 per ARGUS F1) |
| Hardcoded `"#F1EEF7"` (meta chip bg) | `var(--accent-soft-2)` |
| Hardcoded `"#5B4D86"` (meta chip fg) | `var(--fg-1)` |
| Hardcoded `"#E0DAEC"` (meta chip border) | `var(--border-2)` |

### §3.3 — `src/App.tsx` (HEAVY)

**Imports change:**
- Drop `palette` from the `./Components` import line (currently line 10).
- Add `import { useTheme } from "./hooks/useTheme";`
- Add `import { Sun, Moon } from "lucide-react";` (or extend the existing lucide-react import line).

**`Header` component:**
- Add `<ThemeToggle/>` between the `Button variant="primary"` ("New agent") and the `<Settings/>` icon (between `App.tsx:115` and `App.tsx:116`). The `<ThemeToggle/>` component is a small new local component; either define it inline at the top of `App.tsx` or export it from `Components.tsx`. **Choice: define it as a small named export in `Components.tsx`** alongside the other UI primitives — it's a UI primitive, not an app shell concern. Then `App.tsx` imports it: `import { ..., ThemeToggle } from "./Components";`.
- Every `palette.X` in the Header's inline styles gets the var-substitution (per the table in §3.2). Specifically lines 50, 51, 62, 71, 74, 87, 88, 93, 103, 104, 118, 134 (×2), 136, 147 (×2).

**`FilterSidebar` component:**
- The archetype-color swatch (line 237: `<span style={{ width: 8, height: 8, background: c, borderRadius: 1 }}/>`) currently reads `c` from `Object.entries(archetypes)`, which is the light-only color from `data.archetypes`. **Rewrite:** drop the destructured `c`; instead `const { dark } = useTheme();` at the top of the component, and `background: archColorFor(a, dark)` for the swatch. Drop the `archetypes` prop in favor of using `Object.keys(archColors)` (imported from `Components.tsx`) for the archetype list — `archColors` is now the canonical archetype-list source, not `data.archetypes`. **Alternative kept: keep `archetypes` prop for the *list of archetype keys* but compute color via `archColorFor`.** Recommended: keep the prop (minimal API change), drop only the color usage.
- Every `palette.X` → token (lines 190, 199, 200, 208, 209).

**`TeamView`:**
- Drop `archetypes` and `archColor` prop drilling for `OfficerCard`. Currently (line 297): `<OfficerCard archColor={archetypes[o.archetype]} ... />`. New: `<OfficerCard officer={o} onClick={...}/>` — `OfficerCard` resolves its own archetype color via `useTheme()`.
- Drop `archetypes: ArchetypeColors` from `TeamView` props.
- Replace `palette.fg1` / `palette.fg3` token uses (lines 271, 280).

**`OfficerDetail`:**
- Drop the `archColor: string` prop. Internal: `const { dark } = useTheme(); const archColor = archColorFor(officer.archetype, dark);` — actually, it's only consumed by `<ArchetypeText archetype={...} color={archColor}/>` (line 588), and `ArchetypeText` is now self-resolving (per §3.2). So `OfficerDetail` doesn't need `archColor` at all — just call `<ArchetypeText archetype={officer.archetype}/>`. Drop the prop and the variable.
- Every `palette.X` → token (many; per the grep table).

**`DetailSidebar`, `BodyMarkdown`, `InlineMD`, `SkillsView`, `MetaView`, `CommandPalette`:**
- Pure mechanical `palette.X` → `var(--…)` swap per the §3.2 table. No structural changes. Cite ranges:
  - `InlineMD`: lines 332, 333, 336, 355.
  - `BodyMarkdown`: lines 384, 400, 420, 443.
  - `DetailSidebar`: lines 466, 474, 475, 486, 524, 535.
  - `OfficerDetail` (the parts that aren't already covered): lines 568, 597, 606, 629.
  - `SkillsView`: lines 653, 662.
  - `MetaView`: lines 697, 707, 708, 718, 728, 739.
  - `CommandPalette`: lines 813, 814, 823, 829, 841, 849, 850, 853, 868, 888, 896, 906, 924, 926, 941, 949, 959.
- One subtle case: `CommandPalette` line 799 has `background: "rgba(20,18,12,0.35)"` (light backdrop). The JSX prototype uses `"rgba(20,18,12,0.45)"` (slightly more opacity). In dark mode this rgba is barely visible (the underlying surface is already `#14130F`); however the `backdrop-filter: blur(12px)` does the heavy lifting visually, so the rgba value is acceptable in both modes. **Leave as-is.** Flagged in §5 as a minor parity-edge.
- Another subtle case: `CommandPalette` `boxShadow` line 816 uses an inline `"0 4px 12px rgba(20,18,12,0.07), 0 12px 32px rgba(20,18,12,0.05)"`. There's a `--shadow-3` token (line 79 light; line 171 dark) that maps exactly to this purpose. **Replace with `var(--shadow-3)`** to get theme-aware shadows. Same treatment for the card `boxShadow: "0 1px 2px rgba(20,18,12,0.04)"` in `OfficerCard` and `SkillCard` → `var(--shadow-1)`.

**`App` component (root):**
- Line 1007: `<div style={{ background: palette.bgApp, minHeight: "100vh", color: palette.fg1 }}>` → `<div style={{ background: "var(--bg-app)", minHeight: "100vh", color: "var(--fg-1)" }}>`.
- Add `useTheme` consumption only if needed (it's not needed in `App` itself — the children consume it).
- Pass `<ThemeToggle/>` no props; it consumes `useTheme()` directly.

### §3.4 — `src/main.tsx` (LIGHT)

```tsx
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import App from "./App";
import { ThemeProvider } from "./hooks/useTheme";
import "./styles/index.css";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <ThemeProvider>
      <App />
    </ThemeProvider>
  </StrictMode>
);
```

Two adds: import `ThemeProvider` and wrap `<App/>`. No theme bootstrap logic here — that's in `index.html` per §2.2.

### §3.5 — `index.html` (LIGHT)

Two additions to `<head>` (per ARGUS F2 / §0.6 disposition #2 + the existing FOUC-bootstrap design):

1. **`<link rel="stylesheet" href="/src/styles/tokens.css">`** — render-blocking, ensures CSS variables are defined for both modes before first paint in BOTH dev and prod.
2. **Inline bootstrap `<script>`** — runs synchronously, sets `data-theme` on `<html>` before body paint.

Place the `<link>` before the `<script>` so the stylesheet starts loading first. Both go BEFORE the closing `</head>` (and before the `<script type="module" src="/src/main.tsx">` — though that's actually in `<body>`, so order is naturally correct). The exact patch:

```html
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/mark.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>The Stoa — agent-character-builder</title>
    <meta name="description" content="Where teams of AI agents are designed, not assembled." />
    <link rel="stylesheet" href="/src/styles/tokens.css" />
    <script>
      (function () {
        try {
          var stored = localStorage.getItem("acb-theme");
          var dark = stored
            ? stored === "dark"
            : window.matchMedia &&
              window.matchMedia("(prefers-color-scheme: dark)").matches;
          document.documentElement.setAttribute(
            "data-theme",
            dark ? "dark" : "light"
          );
        } catch (e) {
          document.documentElement.setAttribute("data-theme", "light");
        }
      })();
    </script>
  </head>
```

**Why the `<link>` doesn't cause a double-load with `index.css`'s `@import "./tokens.css"`:** browsers dedup CSS by URL. The dev server serves `/src/styles/tokens.css` at exactly one canonical URL; the link tag and the `@import` (which Vite resolves to the same `/src/styles/tokens.css` URL in dev) hit the same resource. After the link tag's load completes, the `@import` is satisfied from cache or treated as already-loaded. No double-application of styles, no perf regression. Vite production extracts CSS to a single bundled `<link>` automatically; the explicit `<link>` in `<head>` aligns dev with prod for spec §5 #2 verification, which runs in dev (`http://localhost:5173/`).

**`index.css` is left intact** — its `@import "./tokens.css"` line stays, so any post-arc developer reading `src/styles/index.css` still sees the dependency declared in source. The `<link>` tag in `index.html` is the FOUC mitigation; the `@import` is the source-level declaration. Both are correct; the browser dedup makes them harmless together.

No other changes to `index.html`.

### §3.6 — `src/styles/tokens.css` (LIGHT — token additions only)

Two token-addition tasks, each per a §0.5 Lock plus an ARGUS finding disposition:

**Task A — rank-border tokens (per §0.5 Lock 1).** Add three rank-border tokens to **both** the `:root` (light, ~line 52 area) and `:root[data-theme="dark"]` (dark, ~line 158 area) blocks. Place each new token immediately after its corresponding `--rank-*-bg` line so the rank tokens stay grouped.

Light block additions (preserving v0.1 hexes — was `palette.rankMajBorder` / `rankCapBorder` / `rankLtBorder`):

```css
--rank-major-border: #E5D6A8;
--rank-captain-border: #D9DBDF;
--rank-lieutenant-border: #E5C9B3;
```

Dark block additions (matched to the dark `--rank-*-bg` tonal family — these are new design values):

```css
--rank-major-border: #4A3F1F;
--rank-captain-border: #3A3B3D;
--rank-lieutenant-border: #4A3326;
```

Rationale for dark values: the dark `--rank-*-bg` tokens at `tokens.css:154-158` are deep saturated tints of the rank's accent color. The dark borders are chosen to be ~1.5× darker than the bg (closer to the surface bg `#1A1916`), echoing the light-mode relationship where `#E5D6A8` is ~1.3× darker than `--rank-major-bg` `#FAF1D2`. This keeps the rank-coded border subtly visible on dark surfaces without competing with the bg's tonal hue. **Per ARGUS F6 / §0.6 disposition #6:** ARGUS confirmed each border is on-hue with its rank family and has adequate contrast against its dark `--rank-*-bg`. Not muddy. Accepted as-is.

**Task B — `--accent-soft-border` token (per ARGUS F1 / §0.6 disposition #1).** Add `--accent-soft-border` to **both** the `:root` (light) and `:root[data-theme="dark"]` (dark) blocks. Place each immediately after `--accent-soft-2` so the accent-soft tokens stay grouped (light: ~line 44; dark: ~line 151).

Light block addition (preserves v0.1 skill-chip border hex pixel-for-pixel):

```css
--accent-soft-border: #B7C5DA;
```

Dark block addition (mid-blue, on-hue with the dark accent family):

```css
--accent-soft-border: #3A4F6E;
```

Rationale for dark value `#3A4F6E`: the dark accent family runs `--accent` `#7CA1D4` (mid-blue, prominent), `--accent-soft` `#1F2A3E` (deep-blue surface), `--accent-soft-2` `#2A3A55` (slightly elevated deep-blue). The skill-chip border in dark mode needs to sit between `--accent-soft` (the chip's own bg) and `--accent` (the chip's fg) in luminance — visible as a border without competing with the fg or merging into the bg. `#3A4F6E` is the on-hue mid-luminance pick: ~25% brighter than `--accent-soft` bg `#1F2A3E` (visible as a border) and ~30% darker than `--accent` fg `#7CA1D4` (subtler than the fg text). The alternative `#42547A` from ARGUS F1 is also defensible (slightly lighter, slightly more prominent); `#3A4F6E` chosen for restraint — borders should read as borders, not as a third visual element competing with the fg text. Same on-hue + contrast reasoning as the dark rank-border picks above.

**Self-flag for ARGUS / VERA:** the dark `--accent-soft-border` hex is a designer-judgment value (like the dark rank-border hexes). If VERA finds insufficient contrast on a dark surface, the fix is a one-line tweak — trivial. NOT load-bearing for the broader design.

No other changes to `tokens.css`. The dark token block at lines 131–173 already covers every other used token (per §4 audit, extended below).

---

## §4 — Token coverage check

Audit: every `palette.X` reference in current code (`src/Components.tsx` + `src/App.tsx`) maps cleanly to an existing CSS variable defined in BOTH the light block (`tokens.css:20-125`) AND the dark block (`tokens.css:131-173`).

| Used `palette.X` | Light token (line) | Dark token (line) | Status |
|---|---|---|---|
| `bgApp` | `--bg-app` (22) | `--bg-app` (132) | OK |
| `bgSurface` | `--bg-surface` (23) | `--bg-surface` (133) | OK |
| `bgSunken` | `--bg-sunken` (24) | `--bg-sunken` (134) | OK |
| `bgInset` | `--bg-inset` (25) | `--bg-inset` (135) | OK |
| `fg1` | `--fg-1` (28) | `--fg-1` (137) | OK |
| `fg2` | `--fg-2` (29) | `--fg-2` (138) | OK |
| `fg3` | `--fg-3` (30) | `--fg-3` (139) | OK |
| `fg4` | `--fg-4` (31) | `--fg-4` (140) | OK |
| `border1` | `--border-1` (35) | `--border-1` (143) | OK |
| `border2` | `--border-2` (36) | `--border-2` (144) | OK |
| `accent` | `--accent` (40) | `--accent` (147) | OK |
| `accentSoft` | `--accent-soft` (43) | `--accent-soft` (150) | OK |
| `rankMaj` | `--rank-major` (47) | `--rank-major` (153) | OK |
| `rankMajBg` | `--rank-major-bg` (48) | `--rank-major-bg` (154) | OK |
| `rankCap` | `--rank-captain` (49) | `--rank-captain` (155) | OK |
| `rankCapBg` | `--rank-captain-bg` (50) | `--rank-captain-bg` (156) | OK |
| `rankLt` | `--rank-lieutenant` (51) | `--rank-lieutenant` (157) | OK |
| `rankLtBg` | `--rank-lieutenant-bg` (52) | `--rank-lieutenant-bg` (158) | OK |
| Hardcoded `"#fff"` (button text on accent) | `--fg-on-accent` (32) | `--fg-on-accent` (141) | OK — replaces hardcode |
| Hardcoded `"#9B3A3A"` (button danger) | `--danger` (71) | `--danger` (164) | OK — replaces hardcode |
| Shadow `"0 1px 2px rgba(20,18,12,0.04)"` (cards) | `--shadow-1` (77) | `--shadow-1` (169) | OK — replaces hardcode |
| Shadow `"0 4px 12px ..."` (modal) | `--shadow-3` (79) | `--shadow-3` (171) | OK — replaces hardcode |

**Gaps found: ZERO load-bearing** for existing tokens. Every used color, border, and shadow has a defined token in both modes for the unmodified surfaces.

**Rank-pill borders — token addition (per §0.5 Lock 1, §3.6 Task A):** `--rank-major-border`, `--rank-captain-border`, `--rank-lieutenant-border` are added to BOTH the light `:root` block AND the dark `:root[data-theme="dark"]` block of `tokens.css`. Light values reuse the v0.1 hexes (`#E5D6A8`, `#D9DBDF`, `#E5C9B3`); dark values match the dark `--rank-*-bg` tonal family (`#4A3F1F`, `#3A3B3D`, `#4A3326`). This preserves the v0.1 warm-tint rank-coded borders in light mode (no visible regression) and extends the same rank-coded signal to dark mode.

**Skill-chip border — token addition (per ARGUS F1 / §0.6 disposition #1, §3.6 Task B):** `--accent-soft-border` is added to BOTH blocks. Light value `#B7C5DA` reuses the v0.1 skill-chip border hex (pixel-perfect parity preserved); dark value `#3A4F6E` is on-hue with the dark accent family. The skill-chip's accent-tinted border (third reinforcement of the "belongs to accent family" semantic) is preserved across modes rather than collapsed to the warm-grey `--border-2`. Side benefit: cross-chip differentiation between skill (accent border) and meta (`--border-2`) restored, mitigating ARGUS F7's residual concern.

Coverage now: 100% — every `palette.X` reference and every previously-hardcoded color has a matching theme-aware token in both modes, with no flatten-to-`--border-2` fallbacks for accent-family or rank-family borders.

**Unused tokens that exist:** `--accent-press` (light + dark), `--success`, `--success-bg`, `--warning`, `--warning-bg`, `--info`, `--info-bg`, `--shadow-2`, `--shadow-focus`, all `--arch-*` tokens. Not used in this arc; no edits required to them.

---

## §5 — Risk handling (per spec §10)

### §5.1 — Diff blast radius is large

**Spec risk:** "Almost every styled element changes. Mitigation: ARGUS critique gate; CATO final review explicitly checks light-mode parity."

**Design response:**
- The diff is mechanical and table-driven (§3.2 token table). ADA executes a deterministic substitution; there is no judgment call inside the substitution.
- Three places in the diff are NOT pure substitution and need extra ADA care:
  1. `ArchetypeText` signature change (drops `color` prop, gains `useTheme()` call). Touches every call site (`OfficerCard`, `OfficerDetail`).
  2. `OfficerCard` signature change (drops `archColor` prop). Touches every call site (`TeamView`).
  3. `OfficerDetail` signature change (drops `archColor` prop). Touches every call site (`App`).
- Light-mode parity is verified by VERA (manual visual inspection of every screen against pre-arc baseline; spec §5 #6) and CATO (diff hygiene + regression scan; spec §7 step 5). The grep post-condition (`grep -E '#[0-9A-Fa-f]{3,6}' src/App.tsx src/Components.tsx`) is a hard mechanical check; ADA must run it before declaring done.
- **Three deliberate intentional consolidations in this arc** (post-ARGUS v1):
  1. **Meta-chip color** (Lock 2 / §5.6) — Colonel-approved upfront. Drops hardcoded lavender in favor of `accent-soft-2 / fg-1 / border-2`. Small light-mode visible change in `DetailSidebar` "Required reading" chips.
  2. **Card-hover background** (Lock 3, post-ARGUS F3 / §0.6 disposition #3) — DAEDALUS-architect-decision (Colonel routed F3 to architect-tier). `OfficerCard` and `SkillCard` hover go from `palette.bgApp` (production v0.1) to `var(--bg-inset)` (JSX prototype). Small light-mode visible change in card hover state, more prominent than v0.1's barely-perceptible `bgApp` hover. Reads correctly in both modes (lighter-than-surface direction is consistent).
  3. ~~**Skill-chip border** consolidation~~ — REJECTED in v2 (per ARGUS F1 / §0.6 disposition #1). Instead of consolidating `#B7C5DA` to `--border-2`, added a new `--accent-soft-border` token that preserves the v0.1 light-mode hex pixel-for-pixel and extends the accent-family border to dark mode. NOT a consolidation; a token addition. Listed here only to mark that the v1 design's silent consolidation was caught and reversed.
- **Rank-pill borders are NOT a deliberate change** — token addition (§0.5 Lock 1, §3.6 Task A) preserves the v0.1 warm-tint rank coding pixel-perfect in light mode and extends the same signal to dark.

### §5.2 — FOUC risk

**Spec risk:** "If theme is applied after React mounts, users see a flash of light mode before dark."

**Design response (post-ARGUS F2):** **two mechanisms in tandem in `index.html`** (§2.2 + §3.5). (1) `<link rel="stylesheet" href="/src/styles/tokens.css">` makes the CSS variable definitions render-blocking in BOTH dev and prod. (2) The inline `<script>` synchronously sets `data-theme` on `<html>` before body paint. Together: tokens are defined for both modes before paint AND the correct mode is selected before paint → `:root[data-theme="dark"]` resolves correctly on first paint, no flash. Verified by VERA per spec §5 #2 ("No flash of unstyled content"), running on `npm run dev` per the spec.

**Why the v1 design's inline-script-only approach was insufficient (ARGUS F2):** spec §5 #2 verification runs in dev. In Vite dev mode, CSS imported through `main.tsx` → `index.css` → `tokens.css` travels the module graph and is injected via `<style>` tags after the JS module evaluates. The inline script set `data-theme` correctly, but the CSS variables that consume `[data-theme="dark"]` weren't loaded yet, so a window existed where the browser could paint with no CSS variables defined (browser-default white background, regardless of `data-theme`). The render-blocking `<link>` closes that window. Production was already FOUC-free (Vite extracts CSS to a `<link>` automatically), but dev wasn't — and dev is the verification environment.

**Edge case considered:** if the inline script throws (e.g., extremely strict CSP that blocks inline scripts), the `try/catch` falls back to setting `data-theme="light"` and the app loads in light mode. This is a graceful degradation, not a crash. CSP is not configured anywhere in this project (verified by inspecting `index.html` — no `<meta http-equiv="Content-Security-Policy">`); Vite dev server doesn't add one by default. Production deploys will need to whitelist `'unsafe-inline'` or use a nonce; not relevant for v0.2 localhost.

### §5.3 — Hook reactivity edge cases

**Spec risk:** "MutationObserver-based `useDark()` is reactive but may have subtle timing bugs with React's render cycle. Mitigation: DAEDALUS may prefer React Context with a setter wired to the toggle button; pick whichever is simpler and document why."

**Design response:** Chose Context (§2.1). Eliminates the timing-bug class entirely:
- No DOM observer → no race between mutation event and React reconciliation.
- No multiple subscribers → no "dispatcher fanout" cost; `useContext` is a direct read.
- Toggle button updates state, effect syncs DOM + localStorage, all consumers re-render in the same React commit.

**Remaining hook concerns:**
- `useTheme()` throws if called outside `<ThemeProvider>` — explicit and helpful failure mode rather than a silent default-to-light. ADA should ensure every component that needs the hook is rendered under the provider (`main.tsx` wraps `<App/>`, so this is guaranteed).
- Under `<StrictMode>`, the `useEffect` in `ThemeProvider` runs twice on mount in dev. Both runs set `data-theme` to the same value (the initial `dark` state), so this is idempotent. No bug. **Per ARGUS F11 / §0.6 disposition #11:** ARGUS confirmed by reading the §2.1 sketch — both invocations write the same value of `dark`, so `dataset.theme = ...` and `localStorage.setItem(...)` are both pure functions of state. Verified.

### §5.4 — localStorage safety (quota / SSR / private browsing)

**Spec risk:** "Not a real concern (this is a single-user-localhost app, no SSR), but `try/catch` the localStorage read on boot defensively."

**Design response:**
- `index.html` inline script: wrapped in `try/catch`; falls back to `matchMedia` then to `light`.
- `useTheme.tsx` provider's effect: `try/catch` on the `setItem` call; silently noops on failure (the React state still works for the current session).
- Private-browsing mode in some browsers throws on `localStorage.setItem` even though `getItem` succeeds — both call sites are wrapped, so this is handled.
- No SSR concern (Vite + React + localhost; no Node runtime executes the bootstrap script).

### §5.5 — System preference change mid-session

**Spec risk:** "If the user changes OS theme while the app is open and they have NO stored choice, should the app react? Decision: no. First-load hydration only; once the user touches the toggle (or even on first render with system preference applied), we lock it in localStorage."

**Design response:** Honors the spec decision exactly. Concrete behavior:
- First load with no localStorage entry: bootstrap reads `matchMedia` → sets `data-theme` → React mounts → `ThemeProvider`'s effect runs → writes `localStorage["acb-theme"]`. From this point forward, the user's OS preference change does NOT affect the app — the stored choice wins.
- This means: a user who has never toggled the theme and changes their OS theme between sessions WILL see the change reflected on next page reload (because the stored value matches the previous OS preference, and on a new load with stored="dark" + OS just changed to light, the app keeps "dark"). That's the spec's chosen behavior; the user can fix it by toggling.
- **NOT implemented:** a `matchMedia(...).addEventListener("change", ...)` listener that updates the app live. Out of scope for v0.2 per spec §10 #5. **Per ARGUS F12 / §0.6 disposition #12:** ARGUS confirmed by reading the §3.5 inline script body — `window.matchMedia(...).matches` is a one-shot read of the `.matches` property on the returned MediaQueryList. No `.addEventListener("change", ...)` call. Spec §10 #5 honored.

### §5.6 — Intentional consolidation: meta-chip color (Colonel-approved)

**Status: RESOLVED at Colonel-lock gate (§0.5 Lock 2).** The current production meta-chip uses hardcoded `#F1EEF7` bg / `#5B4D86` fg / `#E0DAEC` border (a soft lavender). The JSX prototype uses `accent-soft-2` / `fg-1` / `border-2` (a soft accent-blue tint). My design ports the JSX prototype.

**Colonel decision: accept the consolidation.** Rationale: the lavender was an incidental choice in the v0.1 port, not a load-bearing semantic signal. Section headers handle the meta-vs-skill semantic disambiguation; the chip variant just needs to read as "informational pill." The accent-soft-2 / fg-1 / border-2 pattern is the canonical theme-aware shape, has correct contrast in both modes, and removes a set of hardcoded hexes that would otherwise need their own tokens.

**This is the canonical example of an approved intentional consolidation per spec §5 #6** (which now reads "no unintentional visual regressions; intentional consolidations documented in design.md are OK"). VERA and CATO know to expect this small light-mode visible change in `DetailSidebar` "Required reading" chips (`App.tsx:512`) and treat it as approved, not a regression.

---

## §6 — ARGUS findings dispositioned (post-v1 audit)

All open questions from v1 have been adjudicated. See §0.6 for the full disposition list. Below: the v1 numbered questions, each annotated with how it was resolved.

1. **~~Rank-pill border change~~** — RESOLVED at §0.5 Lock 1; ARGUS F6 confirms dark hexes are visually correct (on-hue + adequate contrast). Accepted as-is per §0.6 disposition #6.

2. **~~Meta-chip color change~~** — RESOLVED at §0.5 Lock 2; ARGUS F7 confirms consolidated meta-chip reads correctly in both modes. **VERA verification gate (post-ARGUS F7 / §0.6 disposition #7):** VERA explicitly checks that the section headers above each chip group ("Callable lieutenants" vs "Required reading" in `DetailSidebar` Officer Detail right pane) are intact and visually prominent in BOTH modes. They are the load-bearing cross-chip disambiguator. F1's resolution (adding `--accent-soft-border` to skill-chip) restores some cross-chip visual differentiation as a side benefit — the skill chip now has a visibly accent-tinted border while the meta chip uses the neutral `--border-2`.

3. **`OfficerCard`'s API regression** — RESOLVED per ARGUS F9 / §0.6 disposition #9. Accepted: v0.2 has no Vitest scaffold, so component-isolation testing is not in scope. JSDoc note added to `OfficerCard` signature description (§3.2) so v0.3+ readers know the `<ThemeProvider>` ancestor requirement upfront. When v0.3 component tests arrive, the fix is a `renderWithTheme` test helper — a 5-line wrapper.

4. **Bootstrap script duplication risk** — RESOLVED per ARGUS F10 / §0.6 disposition #10. Accepted: drift risk is real but small; introducing a constants module for a single key is overkill. If a future arc adds a second client-side localStorage key, extract both at that point.

5. **`<StrictMode>` + Context double-effect** — RESOLVED per ARGUS F11 / §0.6 disposition #11. Confirmed idempotent by ARGUS reading the §2.1 sketch. Both invocations write the same value of `dark` (a pure function of state). No RUNNER probe needed.

6. **Inline ES5 script vs TypeScript universe** — RESOLVED per ARGUS F14 / §0.6 disposition #14. Accepted: standard pattern (Vercel, Next.js, GitHub all do this). Simpler than extracting to a pre-bundled JS asset.

7. **`<Sun/>` + `<Moon/>` icons** — RESOLVED per ARGUS F13 / §0.6 disposition #13. Accepted additive surface. Same package as existing icons.

8. **Dropped prop drilling: `data.archetypes` redundancy** — RESOLVED per ARGUS F8 / §0.6 disposition #8. Deferred to follow-up ticket `acb-002-followup-archetypes-dedup` (already filed at `agents/follow-ups/acb-002-followup-archetypes-dedup.md`). acb-002 already touches the data layer and the cleanup composes naturally there. Spec §4 explicitly excludes edits to `src/data/sample.ts` in this arc; deferring honors the spec scope.

**New findings introduced by ARGUS v1, dispositioned in v2:**

- **F1 (skill-chip border consolidation, unflagged):** RESOLVED — added `--accent-soft-border` token (§3.6 Task B). Light pixel-perfect; dark `#3A4F6E`. Not a consolidation; a token addition.
- **F2 (FOUC dev/prod parity):** RESOLVED — added render-blocking `<link>` to `index.html` (§3.5). FOUC-free in both dev and prod.
- **F3 (card-hover direction):** RESOLVED — promoted to §0.5 Lock 3; ports prototype's `bg-inset` hover.
- **F4 (`--fg-on-accent` overload on danger):** RESOLVED — accepted overload (§3.2 Button row). Sub-perceptible visual impact.
- **F5 (dispatch-brief inversion):** parent-session note only; no design.md edit.
- **F6 (dark rank-border hexes):** RESOLVED — ARGUS confirmed visually correct.

---

**End of design v2. ARGUS v1 findings dispositioned per §0.6. ADA executes against this v2 spec; VERA verifies per spec §5; CATO reviews.**
