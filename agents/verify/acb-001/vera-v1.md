# VERA Verification — acb-001-darkmode v1

**Verifier:** VERA (`VERA_agent_character_builder`)
**Target:** Implementation by ADA against `agents/design/acb-001/design.md` v2.
**Spec:** `agents/specs/acb-001-darkmode.md` (§5 — seven success criteria).
**Verdict:** **PASS with NEEDS-COLONEL-EYEBALL** for §5 #5 visual readability.

---

## Per-criterion table

| # | Criterion | Result | Evidence |
|---|---|---|---|
| §5 #1 | Toggle present (every view) | **PASS** | `<ThemeToggle/>` in `Header` cluster (App.tsx:118), between primary "New agent" Button (115) and Settings gear (119); Header is sticky and renders on every view. |
| §5 #2 | Toggle works, no flash | **PASS (code-level)** | `useTheme.tsx:25-37` — `toggle()` flips `dark`, effect with `[dark]` dep writes `data-theme` to `<html>`; React re-renders all `useTheme()`/`useDark()` consumers. |
| §5 #3 | Persistence | **PASS** | `useTheme.tsx:32` — `localStorage.setItem("acb-theme", ...)` in try/catch on every change. Lazy initializer (line 26) reads from `<html data-theme>` set by `index.html:13-21` inline script via `localStorage.getItem("acb-theme")` round-trip. |
| §5 #4 | System hydration | **PASS** | `index.html:13-17` — `localStorage.getItem("acb-theme")` falls back to `window.matchMedia("(prefers-color-scheme: dark)").matches`. |
| §5 #5 | Dark reads correctly on every screen | **PARTIAL — CODE PASS / EYEBALL PENDING** | All 27 unique tokens consumed by App.tsx + Components.tsx have BOTH light AND dark definitions in tokens.css. All 10 archetypes referenced in sample.ts have `[light, dark]` pairs in `archColors` (Components.tsx:42-51). `--accent-soft-border` has dark `#3A4F6E` (tokens.css:156). **"Reads correctly" requires Colonel eyeball.** |
| §5 #6 | No unintentional light-mode regressions | **PASS** | All 21 palette substitutions byte-identical to v0.1 hex (verified via diff vs `git show d56d876:src/Components.tsx`). Three approved consolidations match design.md: Lock 2 meta-chip, Lock 3 card-hover (`bgApp` → `bg-inset`), F1 skill-chip border (token added, light hex `#B7C5DA` byte-identical). Inline `"#fff"` → `var(--fg-on-accent)` light = `#FFFFFF`; `"#9B3A3A"` → `var(--danger)` light = `#9B3A3A`. |
| §5 #7 | No `palette` const + no inline hex | **PASS** | `grep -n 'palette\.' src/`: ZERO matches. `grep -nE '#[0-9A-Fa-f]{3,6}' src/*.tsx`: 11 matches, all inside `archColors` map declaration (Components.tsx:42-51) plus one comment (line 118). No stray inline-style hex. |

## Auxiliary checks (ARGUS dispositions)

| Check | Result |
|---|---|
| F1 — `--accent-soft-border` token added (light + dark) | **PASS** — tokens.css:45 (`#B7C5DA` light, byte-identical to v0.1) and :156 (`#3A4F6E` dark). Consumed via `chipVariants.skill.border` (Components.tsx:223). |
| F2 — FOUC zero in Vite dev | **PASS** — served HTML has `<link rel="stylesheet" href="/src/styles/tokens.css">` BEFORE the inline `<script>` bootstrap, both in `<head>`. Tokens render-block before bootstrap runs. |
| F7 — DetailSidebar section headers intact | **PASS** — Tools (App.tsx:488), Callable lieutenants (501), Required reading (513), Model tier (523), Body path (534) — all `<div style={sectionLabel}>` with uppercase, `var(--fg-3)`, fontWeight 600. |
| Lock 1 — rank-pill borders preserved as new tokens | **PASS** — 8 occurrences of `--rank-*-border` in tokens.css (4 tokens × 2 blocks). RankPill consumes via `var(--rank-{rank}-border)` (Components.tsx:165-167). |

## Mechanical post-condition re-checks (independent of ADA's self-report)

- `grep 'palette\.'` → **0 matches**
- `grep -E '#[0-9A-Fa-f]{3,6}' src/*.tsx` → 11 matches, all in `archColors` map + 1 comment
- `grep 'var(--' src/*.tsx | wc -l` → **91**
- Rank/accent-soft border tokens in tokens.css → **8 matches** (4 × 2 blocks)
- `data-theme` in index.html + useTheme.tsx → present
- `<link rel="stylesheet">` in index.html → present at :9 (before bootstrap script)
- Dev server: `http://localhost:5173/` → 200; tokens.css / App.tsx / Components.tsx / useTheme.tsx / main.tsx / mark.svg all 200; dev log clean (Vite ready in 473ms, zero errors/warnings)
- `ThemeProvider` wraps `<App/>` in main.tsx — `useTheme` consumers always inside provider

## Top 3 most concerning items

1. **§5 #5 visual aspect requires Colonel eyeball** — "reads correctly on every screen" cannot be falsified by code-level audit alone. Mechanical contract satisfied; perceptual judgment pending.
2. **`rgba(20,18,12,0.35)` modal backdrop in App.tsx:801** — a hardcoded warm-paper rgba preserved from v0.1, not flagged by hex-literal grep because it's `rgba()`. Minor: in dark mode it becomes a translucent warm-grey film over the dark backdrop — still serves as a darkening overlay, but not theme-aware. NOT a §5 #7 violation (post-condition specifies hex). Suggested follow-up ticket: introduce `--modal-overlay` token, define for both modes.
3. **`data.archetypes` in sample.ts still carries v0.1 light hex strings** — explicitly deferred to acb-002 per ARGUS F8 disposition. Values are dead; only keys consumed for FilterSidebar enumeration. Documented in Components.tsx:37 comment.

## Ask for the Colonel — eyeball checklist (dev server at http://localhost:5173/)

1. **Team Overview** (`team` tab) — toggle to dark; verify OfficerCard contrast, RankPill readable, ArchetypeText readable, hover → `bg-inset`, FilterSidebar archetype dots use dark hex.
2. **Officer Detail** — markdown body, code chips, DetailSidebar tools/lieutenants/meta chips. Skill chips use new `--accent-soft-border` (`#3A4F6E`).
3. **Skill Library** (`skills` tab) — SkillCards + `callable_by` tool chips.
4. **Meta-aspects** (`meta` tab) — cards.
5. **⌘K palette** open over each view — modal surface, warm rgba backdrop, section headers visible.
6. **Toggle in each view** — no flash, instant repaint.
7. **Hard reload (Ctrl+Shift+R)** while in dark — dark persists, zero flash.
