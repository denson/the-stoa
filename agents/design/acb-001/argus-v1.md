# ARGUS Audit — acb-001 dark mode integration design v1

**Auditor:** ARGUS (`ARGUS_agent_character_builder`)
**Audit target:** `agents/design/acb-001/design.md` v1 (post-Colonel-locks §0.5).
**Spec:** `agents/specs/acb-001-darkmode.md` (post §5 #6 edit).
**Verdict:** **PASS-WITH-CONCERNS**

---

## Verdict summary

ADA may proceed pending DAEDALUS dispositioning the load-bearing findings (F1, F2, F3) and recording dispositions in design.md v2.

**Severity counts:** 0 blocker / 6 concern (F1, F2, F3, F7 + cross-chip note, F9 promotion-debatable) / 8 nit. F2 is concern because spec §5 #2 verification runs in dev and the FOUC claim is a production-only property as designed.

**Top 3 most load-bearing:**

1. **F1** — Skill-chip border `#B7C5DA` → `--border-2` is a hue-changing consolidation (cool blue → warm grey) that DAEDALUS did not flag in §0.5 / §5.1 / §5.6 / §6. Either flag it as a third intentional consolidation (Colonel sign-off needed) or add a new `--accent-soft-border` token. Spec §5 #6 contract requires this be explicit.
2. **F2** — "Zero FOUC" is a production-build property, not a Vite-dev property. Spec §5 #2 verification runs in dev (`http://localhost:5173/`). Add a `<link rel="stylesheet">` in `<head>` for tokens.css, OR scope the FOUC claim to production and verify on `npm run build && npm run preview`.
3. **F3** — Card-hover direction (`bgApp` vs `bg-inset`) — design ports production hover, not prototype hover. The prototype's `bg-inset` is the conventional hover direction in both modes; production's `bgApp` is a v0.1 choice. Pick one; document.

---

## Findings

### F1 — Skill-chip border consolidates a cool-blue hex into a warm-grey token (unflagged)

- **Severity:** concern
- **What:** `chipVariants.skill.border` is currently `"#B7C5DA"` (cool blue, on-hue with the accent family). Design §3.2 maps it to `var(--border-2)` which resolves to `#D4D0C5` light (warm grey). Different hue, different family.
- **Where:** `src/Components.tsx:183`; design §3.2 token-mapping table row "Hardcoded `"#B7C5DA"` (skill chip border) → `var(--border-2)`"; design §3.6 "Coverage now: 100% — every `palette.X` reference has a matching theme-aware token in both modes, with no fallback to `--border-2`" (this sentence is contradicted by §3.2 which DOES fall back skill-chip-border to `--border-2`).
- **Why it matters:** The skill chip's blue-tinted border was a deliberate visual signal (the chip "belongs" to the accent family — accent-soft bg, accent fg, accent-tinted border). Flattening to `--border-2` removes the third reinforcement of that signal in light mode. This is a silent consolidation that the spec §5 #6 policy requires DAEDALUS to flag explicitly. It is currently NOT flagged in §0.5 / §5.1 / §5.6 / §6. Either it should be promoted to a third Colonel-locked consolidation in §0.5 (with rationale), or a new token (`--accent-border` or `--accent-soft-border`) should be added to both modes.
- **Suggested fix:** DAEDALUS picks one and documents: (a) flag it as a third intentional consolidation (similar to meta-chip §0.5 Lock 2), or (b) add `--accent-soft-border` (light: `#B7C5DA`, dark: a complementary mid-blue ~ `#3A4F6E` or `#42547A`) to `tokens.css` and route the skill-chip border through it.

### F2 — "Zero FOUC" claim is true in production but not necessarily in Vite dev

- **Severity:** concern
- **What:** Design §2.2 claims "Zero. Script runs synchronously before body paint; `data-theme` is on `<html>` before the first pixel renders." This is half right. The inline script DOES set `data-theme` before paint, but the CSS rules that consume `:root[data-theme="dark"]` are inside `tokens.css`, which is loaded via `index.css` `@import`, which is itself loaded by `main.tsx` (a `<script type="module">`). ES modules are deferred per the HTML spec; in Vite dev mode, CSS travels through the module graph and is injected via `<style>` elements after JS evaluates. There is a window between body parse and CSS injection where the browser may paint with no CSS variables defined at all (browser-default white background, default text color), regardless of the `data-theme` attribute.
- **Where:** Design §2.2 (FOUC table); `index.html:1-15` (no `<link rel="stylesheet">` for tokens.css in `<head>`); `src/main.tsx:4` (`import "./styles/index.css"`); `src/styles/index.css:1` (`@import "./tokens.css"`); spec §5 #2 ("No flash of unstyled content").
- **Why it matters:** Spec §5 #2 is a VERA gate. If VERA tests on `npm run dev` (which is what the spec says: `http://localhost:5173/`), they may see a flash of unstyled (browser-default) content even with the inline script in place. In `npm run build`, Vite extracts CSS to a `<link rel="stylesheet">` in `<head>` which IS render-blocking, so production is genuinely FOUC-free — but spec §5 #2 verification runs in dev.
- **Suggested fix:** Either (a) add a `<link rel="stylesheet" href="/src/styles/tokens.css">` (or the post-build CSS asset) in `<head>` of `index.html` so tokens are render-blocking in dev too, or (b) revise design §2.2 to explicitly scope "Zero FOUC" as a production claim and document a one-frame brown-paper-bag flash as an accepted dev-only artifact with VERA's verification done on `npm run build && npm run preview`. Option (a) is the cleaner answer.

### F3 — Card-hover backgrounds: design ports production behavior, not the JSX prototype's

- **Severity:** concern
- **What:** Production `OfficerCard` (`Components.tsx:239`) hovers from `palette.bgSurface` to `palette.bgApp`. JSX prototype (`design_handoff_character_builder/ui/Components.jsx:119`) hovers from `var(--bg-surface)` to `var(--bg-inset)` — a noticeably darker tint. Design §3.2 specifies a pure mechanical substitution, which preserves the *production* hover (`bgApp`) — not the prototype's. Same divergence applies to `SkillCard` line 293.
- **Where:** `src/Components.tsx:239,293`; `design_handoff_character_builder/ui/Components.jsx:119,140`; design §3.2 OfficerCard / SkillCard rows.
- **Why it matters:** The design names the JSX prototype as "the reference" (spec §9 + design §0). The card-hover state is a real visible difference between prototype and production: `bgApp` (`#FAF9F6`) is almost imperceptible against `bgSurface` (`#FFFFFF`), while `bg-inset` (`#ECE9E1`) is a clear hover state. In dark mode, this matters more: dark `bg-app` = `#14130F`, dark `bg-surface` = `#1B1A16`, dark `bg-inset` = `#221F1A` — `bg-app` is *darker* than `bg-surface`, so hovering "down" into `bg-app` reads as inverted vs the light-mode direction. The prototype's `bg-inset` choice goes "up" (lighter than surface) in dark mode, which is the conventional hover direction.
- **Suggested fix:** DAEDALUS picks: (a) preserve production behavior and document the prototype divergence as a deliberate v0.1 carry-over (acceptable; spec §6 #6 anti-regression supports this), or (b) take the prototype's choice (`bg-inset` for hover) and flag it as a third intentional consolidation. The dark-mode inversion argues mildly for (b).

### F4 — `--fg-on-accent` swap on `Button danger` is a dark-mode tonal change, not flagged

- **Severity:** nit
- **What:** Production danger button text is `"#fff"` (Components.tsx:116). Design §3.2 maps it to `var(--fg-on-accent)`. Light-mode `--fg-on-accent` is `#FFFFFF` (byte-identical to `#fff`); dark-mode `--fg-on-accent` is `#FAF9F6` (warm off-white). The JSX prototype keeps hardcoded `"#fff"` for danger (`Components.jsx:78`). Naming-wise, `--fg-on-accent` is named for accent-colored buttons, not danger-colored ones; semantically it's a slight overload.
- **Where:** `src/Components.tsx:116`; design §3.2 Button row "(×2: bg + border)" notation also slightly off — the `color` is one usage, not two; the (×2) refers to bg + borderColor.
- **Why it matters:** Negligible visual impact (`#FFFFFF` vs `#FAF9F6` is sub-perceptible against `#D17878` danger-red), but the token semantics drift slightly. If a future design adds an `--fg-on-danger` token, the substitution would need to be redone.
- **Suggested fix:** Two acceptable paths: (a) accept and document — `--fg-on-accent` is an overloaded but reasonable choice for any "white-ish text on a saturated colored bg"; (b) hardcode `"#fff"` for danger to match the prototype exactly. Either is fine.

### F5 — Dispatch brief carries an inverted claim about light-mode `--fg-on-accent`

- **Severity:** nit (brief defect, not design defect)
- **What:** The ARGUS dispatch brief states "Light mode `--fg-on-accent` is `#FAF9F6` per design. That's NOT pure white." This is inverted. `tokens.css:32` (light block) sets `--fg-on-accent: #FFFFFF`, and `tokens.css:141` (dark block) sets `--fg-on-accent: #FAF9F6`. Light mode IS pure white. So the substitution `"#fff"` → `var(--fg-on-accent)` is byte-identical in light mode. The brief's worry is mis-grounded.
- **Where:** Dispatch brief Q3 final bullet; `src/styles/tokens.css:32,141`.
- **Why it matters:** Doesn't affect the design audit (the design's mapping is correct). Surfacing for the parent session so the brief itself doesn't propagate the inversion to subsequent dispatches.
- **Suggested fix:** None at design level. Parent-session self-correction: sanity-check token references against tokens.css before pasting into a dispatch.

### F6 — Dark rank-border hexes: distinguishable, but not derived from a formula

- **Severity:** nit
- **What:** `--rank-major-border` dark `#4A3F1F` (warm gold-brown), `--rank-captain-border` dark `#3A3B3D` (cool neutral grey), `--rank-lieutenant-border` dark `#4A3326` (warm red-brown). The major and lieutenant borders are both warm; on a small rank-pill surface the differentiation between gold-brown and red-brown is subtle but present. Each is on-hue with its rank family. Each has adequate contrast against its `--rank-*-bg`:
  - `#4A3F1F` on `#2D2614`: brighter, ~1.5–1.7× luminance ratio. OK.
  - `#3A3B3D` on `#232425`: brighter, similar ratio. OK.
  - `#4A3326` on `#2A1E16`: brighter, similar ratio. OK.
- **Where:** Design §3.6 dark block; concept in §0.5 Lock 1.
- **Why it matters:** DAEDALUS self-flagged as "designer-judgment values, not derived from a token-system formula." That's defensible for v0.2 (one-line tweak if VERA finds a problem). The borders meet the on-hue criterion and the contrast bar. They are NOT muddy.
- **Suggested fix:** Accept as-is. If a formula is desired post-v0.2, a "darken the bg by ~25-35% lightness in OKLCH" formula would land in the same neighborhood and could be a follow-up tokens-system arc — not blocking.

### F7 — Meta-chip vs skill-chip in light mode: visually similar pale-blue family

- **Severity:** concern (Colonel-locked consolidation; verification responsibility on VERA)
- **What:** Light meta-chip post-consolidation: bg `--accent-soft-2` (`#D2DBE9`), fg `--fg-1` (`#1B1A17`), border `--border-2` (`#D4D0C5`). Light skill-chip: bg `--accent-soft` (`#E6EBF3`), fg `--accent` (`#2B4A7F`), border (currently `#B7C5DA`, becoming `--border-2` per F1). Both bgs are pale blues from the same family (`accent-soft`/`accent-soft-2`). Distinguishable by saturation but not by hue. The Colonel-locked decision (§0.5 Lock 2) accepted this; section headers do the disambiguation.
- **Where:** Design §3.2 chip variants; tokens.css:43,44 (light); 150,151 (dark).
- **Why it matters:** The Colonel's lock is final on the consolidation decision; ARGUS's responsibility is to confirm the consolidated chip *reads correctly in both modes*. **It does** — fg/bg contrast is high in both modes. The concern that survives the Colonel lock is the *cross-chip* disambiguation (skill vs meta). Section headers ("Callable lieutenants" vs "Required reading" in `DetailSidebar`) are the load-bearing disambiguator; if those headers are present and visible, the consolidation works.
- **Suggested fix:** No change needed if the headers stay. VERA should specifically check that the section headers above each chip group are intact and visually prominent. If F1 is resolved by adding `--accent-soft-border` (option b), that would also restore some cross-chip visual differentiation.

### F8 — `data.archetypes` becomes redundant post-refactor; design defers cleanup explicitly

- **Severity:** nit
- **What:** Design §2.4 + §6 Q8 acknowledge that `data.archetypes` (`src/data/sample.ts:124-135`) is now functionally redundant with `archColors` in the components layer. Only `Object.keys(archetypes)` is used (for the FilterSidebar enumeration), and `archColors` could replace that. Design keeps `data.archetypes` to honor spec §4 ("`data/sample.ts` not edited per spec").
- **Where:** Design §2.4 last paragraph; §6 Q8.
- **Why it matters:** Real but small code smell. The redundancy could drift in future arcs (someone adds an archetype to one but not the other). Per `CLAUDE.md` fix-now-discipline, the right answer is a ticket-with-plan for cleanup in acb-002 (which already touches the data layer for the agent-team-team adapter).
- **Suggested fix:** File `acb-002-followup-archetypes-dedup` follow-up ticket: "delete `data.archetypes` from `data/sample.ts` and `ArchetypeColors` from `data/types.ts`; replace `Object.keys(archetypes)` in `FilterSidebar` with `Object.keys(archColors)`."

### F9 — `OfficerCard` testability: real but small concern

- **Severity:** nit
- **What:** Post-refactor, `OfficerCard` requires a `<ThemeProvider>` ancestor (consumes `useTheme()` for archetype color resolution). Pre-refactor, it was prop-only and could be rendered in any test harness with no setup.
- **Where:** Design §6 Q3 (self-flagged); §3.2 OfficerCard row.
- **Why it matters:** v0.2 has no Vitest scaffold (acb-002 brings it for adapter testing only). Component-level visual or behavioral tests are not in scope. So this concern is real for v0.3+ but not blocking.
- **Suggested fix:** Document the requirement in a JSDoc comment on `OfficerCard` ("requires ThemeProvider ancestor") and accept. When v0.3 component tests arrive, the fix is a `renderWithTheme` test helper — a 5-line wrapper.

### F10 — `localStorage["acb-theme"]` key duplicated in two places

- **Severity:** nit
- **What:** Hardcoded in `index.html` inline script and `src/hooks/useTheme.tsx` effect. Design §6 Q4 self-flags; "introducing [a constants module] for a single key feels overkill."
- **Where:** Design §3.1 (last bullet); §3.5 (inline script); §6 Q4.
- **Why it matters:** Drift risk. Both locations read/write the same key; a rename would need both edits. Acceptable for v0.2.
- **Suggested fix:** Acceptable as-is. If a future arc introduces a second client-side localStorage key, extract both at that point.

### F11 — `<StrictMode>` + Context double-effect: idempotent, confirmed

- **Severity:** nit (verification, not defect)
- **What:** Design §5.3 claim: "Both runs set `data-theme` to the same value (the initial `dark` state), so this is idempotent. No bug." Verified by reading the proposed `useTheme.tsx` sketch (§2.1): the effect reads from React state `dark`, writes `document.documentElement.dataset.theme = dark ? "dark" : "light"` and `localStorage.setItem(...)`. Both writes are pure functions of `dark`; double-invocation under `<StrictMode>` writes the same value twice. Idempotent.
- **Where:** Design §2.1 sketch, lines 102–104; §5.3.
- **Why it matters:** Confirming the design's claim so ADA doesn't second-guess.
- **Suggested fix:** None.

### F12 — Inline `matchMedia` in `index.html` does NOT create a change listener; spec §10 #5 honored

- **Severity:** nit (verification)
- **What:** Inline script (design §3.5) calls `window.matchMedia("(prefers-color-scheme: dark)").matches` — a one-shot read of the `.matches` property on the returned MediaQueryList. No `.addEventListener("change", ...)` call. Spec §10 #5 ("First-load hydration only; no live OS-theme listener") is honored.
- **Where:** Design §3.5 inline script body; spec §10 #5.
- **Why it matters:** Confirming for the Colonel.
- **Suggested fix:** None.

### F13 — Sun/Moon icon imports: additive, fine

- **Severity:** nit
- **What:** Adding `Sun, Moon` to the `lucide-react` import in `App.tsx` (or `Components.tsx`). No new package dependency; same import source as the existing icons.
- **Where:** Design §3.3 imports.
- **Why it matters:** Minimal surface change; no concern.
- **Suggested fix:** None.

### F14 — Inline ES5 script vs TypeScript universe: acceptable

- **Severity:** nit
- **What:** `index.html` inline script is plain ES5 (uses `var`, function expressions). It runs before any module evaluates, so it cannot share TypeScript types or constants. This is the standard pattern (Vercel, Next.js, GitHub all do this).
- **Where:** Design §3.5; §6 Q6.
- **Why it matters:** Acceptable trade-off vs. extracting to a pre-bundled JS asset (more complexity for no benefit).
- **Suggested fix:** None.

---

## End of audit
