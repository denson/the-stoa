# acb-001 — Dark mode

**Author:** Denson Smith (Colonel) via Major Pliny.
**Status:** Spec locked, ready for design.
**Project:** The Stoa: agent-character-builder, v0.1 alpha → v0.2 batch-3 first half.
**Working dir:** `C:/Users/denso/claude_projects/agent-character-builder/`.
**Pipeline mechanism:** Task-tool sub-agent cascade from Major Pliny's session. Sequential dispatch DAEDALUS → ARGUS → ADA → VERA → CATO via `subagent_type: <NAME>_agent_character_builder`. No `bw`, no Session B, no worktrees — overkill for a small mechanical-after-design integration.

---

## §1 — Goal

**Wire dark mode end-to-end** for the running app at `http://localhost:5173/`, while preserving v0.1 light-mode pixel-perfect parity. The dark token set already exists in `src/styles/tokens.css` (lines 131–173, scoped under `:root[data-theme="dark"], .theme-dark`); this arc makes it actually toggleable, persistent, and reactive across every screen.

## §2 — Why this scope, why this batch

`onboarding-v1/inventory.md` §3 finding #3 named the load-bearing constraint: dark tokens are defined but `palette` JS constants in `Components.tsx` hardcode the light hex values, so toggling `data-theme` alone is not sufficient. The cleanest fix is to delete the `palette` const entirely and rewrite every reference to `var(--token-name)`. This arc does that.

`DESIGN_PRINCIPLES.md` calls dark mode first-class. v0.1 only shipped light. This is the smallest arc that closes that commitment.

The accessibility pass (originally bundled with dark mode in inventory §5 batch 3) is **deferred to acb-004**. Combining them risks scope creep on the verify gate; we'd rather ship one clean toggle arc and follow with a focused a11y arc.

## §3 — In scope

1. **Theme toggle button** in the header. Sun icon when dark, moon icon when light, or vice versa per `lucide-react` convention. Click flips theme. Located adjacent to or replacing the "New agent" CTA region per DAEDALUS's design call.
2. **`data-theme` attribute management.** Toggle sets `document.documentElement.setAttribute("data-theme", "dark"|"light")`.
3. **localStorage persistence.** User's choice is read on app boot; written on every toggle. Key: `acb-theme` (or DAEDALUS picks; document the choice in the design).
4. **System preference hydration.** On first load with no stored choice, read `window.matchMedia("(prefers-color-scheme: dark)").matches`. Stored choice always wins over system preference.
5. **Delete the `palette` const in `src/Components.tsx`** (lines 29–53 per inventory). Every `palette.X` reference in inline styles across `App.tsx` + `Components.tsx` becomes `var(--<token>)`.
6. **`useDark()` hook** (or theme context). Components that need to render archetype colors per-mode call `useDark()` to pick the right entry from the `[light, dark]` pair. Pattern reference: `design_handoff_character_builder/ui/Components.jsx` (the dirty working tree carries the JSX prototype of exactly this hook — read-only design reference).
7. **`archColors` map** (in `Components.tsx`, NOT in `data/sample.ts`) holds the `[light, dark]` pairs per archetype. `data.archetypes` keeps the existing light-mode-only string-per-archetype shape; the dark-variant shift is a presentation concern that lives in the components layer.
8. **Rank pills use rank tokens directly.** `--rank-major`, `--rank-major-bg`, `--rank-captain`, `--rank-captain-bg`, `--rank-lieutenant`, `--rank-lieutenant-bg` — all defined for both light and dark in `src/styles/tokens.css` (lines 47–52 light, 153–158 dark). No JS branching needed for ranks.
9. **No layout/structural changes.** This arc is a styling + state-mgmt arc. Component shape stays identical.

## §4 — Out of scope (do NOT touch)

- **agent-team-team data wiring** (`scripts/gen-data.ts`, schema adapter) → deferred to **acb-002**.
- **URL-shareable state** (react-router migration) → deferred to **acb-003**.
- **Accessibility pass** (divs-as-buttons, semantic landmarks, focus management, `aria-live`) → deferred to **acb-004**.
- **Tailwind refactor** → deferred (later v0.2 arc).
- **Markdown renderer overhaul** (gap §3.12 in inventory) → not in this arc.
- **Brand-asset swap** (real fonts/logo) → arc #6 in v0.2 plan, not this arc.
- **New views or components.** No skill detail page, no meta-aspect drilldown, no compose wizard.

## §5 — Definition of done (the 7 success criteria VERA verifies)

1. **Toggle present.** Dev server at `http://localhost:5173/` shows a working sun/moon toggle in the header (visible on every view: Team / Officer Detail / Skill Library / Meta-aspects).
2. **Toggle works.** Clicking flips the theme; every surface re-renders in the new mode without page reload. No flash of unstyled content.
3. **Persistence.** Choice survives a full page reload (close tab, reopen, theme is preserved).
4. **System hydration.** First load with cleared localStorage reads `prefers-color-scheme` and applies it.
5. **Dark mode reads correctly on every screen.** Manual check: Team Overview (cards, rank pills, archetype chips, filter sidebar), Officer Detail (markdown body left pane, metadata sidebar right pane, action buttons), Skill Library (cards + `callable_by` chips), Meta-aspects (cards), ⌘K palette (open over each view, dark surfaces, dark search results). VERA visits each and confirms.
6. **No unintentional visual regressions in light mode.** Intentional consolidations documented in `design.md` are OK and approved by the Colonel up-front. Compare against `git stash` of pre-arc tree if needed; CATO's review checks for *unintended* drift.

   **Approved consolidations & token additions for acb-001 (Colonel sign-off, gate after DAEDALUS):**
   - **Meta-chip color** — *consolidation approved.* Drops hardcoded lavender (`#F1EEF7 / #5B4D86 / #E0DAEC`) in favor of the prototype's `accent-soft-2 / fg-1 / border-2`. Reads cleaner in both modes; section headers handle the semantic disambiguation. **This is the canonical example of an approved intentional consolidation.**
   - **Rank-pill borders** — *token addition, not consolidation.* The warm-tint per-rank border is an intentional visual signal (rank coding via color); flattening it would lose information. ADA adds `--rank-major-border`, `--rank-captain-border`, `--rank-lieutenant-border` to both `:root` (light) and `:root[data-theme="dark"]` (dark) blocks of `src/styles/tokens.css`. **This is the canonical example of when a token addition is the right answer instead of consolidating.**
7. **No `palette` const survives in `Components.tsx`.** No inline-style hex value that maps to a token survives — all map to `var(--…)`. This is a grep-able post-condition: `grep -E '#[0-9A-Fa-f]{3,6}' src/App.tsx src/Components.tsx` should return only token-definition lines (if any) and SVG-internal colors that are intentionally constant; everything that's a "color of UI chrome" is a CSS variable.

## §6 — Locked architectural decisions (Colonel's calls)

### Decision 1 — `palette` const deletion

**Decision:** Delete it entirely. `tokens.css` is the sole source of truth for theme-aware color.

**Rationale:** The noisy diff is the *correct* diff — it documents the architectural improvement. No sync burden, dark-mode swap is automatic, no palette/tokens drift possible. Every `palette.bgApp` → `var(--bg-app)`, every `palette.fg1` → `var(--fg-1)`, etc. Rank pills use `--rank-major`/`--rank-major-bg`/etc. (full names, not the abbreviated `rankMaj` style of the old JS const).

**Risk acknowledged:** the diff will touch nearly every styled element in `App.tsx` and `Components.tsx`. CATO's review must guard against unintended visual changes — the diff size makes regressions easy to miss. Mitigation: ARGUS pre-critique gate explicitly asks "does the integration preserve v0.1 pixel-perfect parity in light mode?"

### Decision 2 — archetype color layering

**Decision:** `data.archetypes` (in `src/data/sample.ts`) stays as a light-mode-only `string-per-archetype` map. The `[light, dark]` pair logic lives in `src/Components.tsx` as an `archColors` map.

**Rationale:** dark-variant shift is a **presentation concern, not a data concern**. The data layer describes the team; the components layer decides how to render under different themes. The JSX prototype at `design_handoff_character_builder/ui/Components.jsx` already does it this way — DAEDALUS reads that prototype and ports the pattern.

**Implementation pattern (reference, not prescription):**

```tsx
const archColors = {
  orchestrator: ["#5B4D86", "#9D8FCB"],
  architect:    ["#2E6E63", "#6FB5A8"],
  verifier:     ["#785637", "#C29A75"],
  // ...
};

function useDark() {
  const [dark, setDark] = React.useState(() =>
    document.documentElement.getAttribute("data-theme") === "dark");
  React.useEffect(() => {
    const obs = new MutationObserver(() =>
      setDark(document.documentElement.getAttribute("data-theme") === "dark"));
    obs.observe(document.documentElement, { attributes: true, attributeFilter: ["data-theme"] });
    return () => obs.disconnect();
  }, []);
  return dark;
}
```

DAEDALUS may swap MutationObserver for a React Context if cleaner — the constraint is reactive consumption of theme by the component layer, not the specific mechanism. **Document the choice in `design.md`.**

## §7 — Pipeline plan

| Step | Officer | `subagent_type` | Deliverable | Gate |
|------|---------|-----------------|-------------|------|
| 1 | DAEDALUS | `DAEDALUS_agent_character_builder` | `agents/design/acb-001/design.md` — integration plan, files-touched list, hook-vs-context decision recorded, no edits yet | Major Pliny reads + reconciles |
| 2 | ARGUS | `ARGUS_agent_character_builder` | Critique of DAEDALUS plan against the two questions (parity + dark readability) | Major Pliny reconciles ARGUS findings into final plan |
| 3 | ADA | `ADA_agent_character_builder` | Edits to `src/Components.tsx`, `src/App.tsx`, possibly `src/main.tsx` (theme bootstrap) | Lands the changes |
| 4 | VERA | `VERA_agent_character_builder` | Verification against §5's seven criteria via `http://localhost:5173/` (RUNNER for dev server) | Pass / fail per criterion |
| 5 | CATO | `CATO_agent_character_builder` | Final craft review — diff hygiene, light-mode regression check, code style | Pass / needs-revision |
| 6 | Major Pliny | (this session) | Spec-vs-result + project-spirit gate; verdict to Colonel | PASS / NEEDS-REVISION / ESCALATE |

## §8 — Key files (likely touched)

- `src/Components.tsx` — heavy. `palette` const deleted, `archColors` map added, `useDark()` hook added, every styled element rewritten to use `var(--…)`.
- `src/App.tsx` — heavy. Every inline-style `palette.X` reference becomes `var(--…)`. Header gets the toggle button. Theme bootstrap in the App-level effect or moved to `main.tsx`.
- `src/main.tsx` — small. Theme bootstrap (read localStorage / system preference, set `data-theme` before React mounts to avoid FOUC).
- `src/styles/tokens.css` — likely no edits; tokens already exist for both modes. Verify the dark variants produce sufficient contrast for archetype text (DAEDALUS calls).
- Possibly `src/hooks/useTheme.ts` — new file if DAEDALUS chooses Context over MutationObserver.

## §9 — Reference sources

- **JSX prototype (load-bearing reference):** `design_handoff_character_builder/ui/Components.jsx` — the dirty working tree carries the exact pattern (`useDark()`, `archColors` map, `archColorFor()`, `v(name)` shorthand, sun/moon icons). DAEDALUS reads this end-to-end.
- **Design handoff README:** `design_handoff_character_builder/README.md` — calls out "rank pill colors are theme-aware via CSS variables; no JS branching needed."
- **Tokens:** `src/styles/tokens.css` (light: lines 1–124; dark: lines 131–173).
- **Design principles:** `DESIGN_PRINCIPLES.md` — the dark-mode-first-class commitment.
- **Inventory context:** `agents/design/onboarding-v1/inventory.md` §3 finding #3 (the dark-mode gap) and §5 batch 3 (the original combined arc; this spec narrows it to dark mode only, deferring a11y to acb-004).

## §10 — Risk inventory

1. **Diff blast radius is large.** Almost every styled element changes. Mitigation: ARGUS critique gate; CATO final review explicitly checks light-mode parity.
2. **FOUC risk.** If theme is applied after React mounts, users see a flash of light mode before dark. Mitigation: theme bootstrap moves to `main.tsx` or to an inline script in `index.html` that runs before React. DAEDALUS chooses; documents the choice.
3. **Hook reactivity edge cases.** MutationObserver-based `useDark()` is reactive but may have subtle timing bugs with React's render cycle. Mitigation: DAEDALUS may prefer React Context with a setter wired to the toggle button; pick whichever is simpler and document why.
4. **localStorage quota / SSR safety.** Not a real concern (this is a single-user-localhost app, no SSR), but `try/catch` the localStorage read on boot defensively.
5. **System preference change mid-session.** If the user changes OS theme while the app is open and they have NO stored choice, should the app react? **Decision: no.** First-load hydration only; once the user touches the toggle (or even on first render with system preference applied), we lock it in localStorage. Future-arc enhancement, not v0.2-blocker.

## §11 — Self-assessed weak points (Major Pliny's pre-spec gate)

Surfaced for the Colonel before dispatch:

1. **The "no `palette` const survives" success criterion is grep-able but the inverse — "every visual color choice routes through tokens" — is harder to verify mechanically.** A regression where someone hardcodes a hex inside a new inline style would slip past the grep. Mitigation: CATO's review specifically scans for new hex literals.
2. **No automated visual-regression test.** v0.1 has no Vitest scaffold (acb-002 brings it for adapter testing only; component visual regression is much later). Light-mode parity is verified by eyeball + CATO review. If the team wants a screenshot-diff harness, that's a Tier-0 ticket-with-plan, not blocking acb-001.
3. **Toggle button placement is a design call I'm leaving open for DAEDALUS.** Header has a "New agent" CTA. The toggle could live next to it, replace it temporarily, or get its own slot. DAEDALUS picks; the constraint is "visible from every view."
4. **The MutationObserver pattern from the JSX prototype is one valid choice but not the only one.** Context + a setter wired to the toggle is arguably cleaner. DAEDALUS chooses; the constraint is reactive consumption, not a specific mechanism.

---

**End of spec. DAEDALUS reads this verbatim, plus the JSX prototype reference, plus the inventory §3 finding #3 + §5 batch 3, and returns a design.md.**
