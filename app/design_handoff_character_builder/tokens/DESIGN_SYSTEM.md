# The Stoa — Design System

> **The Stoa**: where teams of AI agents are designed, not assembled.

This system is the visual + interaction language for **The Stoa** and its first product, **agent‑character‑builder** — a power‑user web app for browsing, composing, and authoring AI agent teams.

The metaphor: a *stoa* is a Greek colonnade where philosophers (Stoics, originally) gathered to think out loud. Our agents have **character** — distinct roles, ranks, and disciplines drawn from a classical/military vocabulary (Major, Captain, Lieutenant; Pliny, Daedalus, Vera, Argus). The system holds those two registers together: dev‑tool restraint at the surface, classical grain underneath.

---

## Index

| File | What's in it |
|---|---|
| `colors_and_type.css` | All design tokens — color, type, spacing, shadow, radius, motion. Light + dark mode. |
| `README.md` | This file. Brand context, content + visual foundations, iconography. |
| `SKILL.md` | Agent‑Skills‑compatible front matter; lets this system be installed as a Claude Code skill. |
| `fonts/` | Webfont files (currently empty — see Font substitution flag below). |
| `assets/` | Logos, marks, illustrations, brand textures. |
| `assets/icons/` | The icon system (Lucide via CDN — see Iconography). |
| `preview/` | Cards rendered in the project's Design System tab. One concept per card. |
| `ui_kits/character-builder/` | Pixel‑level recreation of the agent‑character‑builder app: `index.html` + JSX components. |

Source materials this system was distilled from:

- `agent-character-builder/BRIEF.md` — full product brief (read‑only mount).
- `agent-character-builder/DESIGN_PRINCIPLES.md` — aesthetic + UX rules.
- `agent-character-builder/data-samples/` — real officer / skill / meta‑aspect JSON + body markdown.

---

## Content fundamentals

The voice is **plain, direct, and quietly confident.** It assumes a technical reader — developers, AI engineers, researchers — who tolerates density and dislikes marketing varnish.

### Tone & casing

- **Sentence case** for headers, buttons, labels. (`Build a new agent`, not `Build A New Agent`.) Officer/skill identifiers are the only exception — they are TRADITIONALLY UPPER‑CASE‑MONO (`MAJOR_PLINY`, `DAEDALUS`) and that distinction is load‑bearing visual signal in the app.
- **Second person ("you")** in agent‑authored prose ("You are Major Pliny, the spec keeper…"). The system addresses agents as people with seats and duties, not robots.
- **First person plural ("we")** sparingly, in onboarding and docs ("we build agents *with* character").
- Periods on full sentences, not on labels or chip text.

### Vibe (specific examples to imitate)

- ✅ "12 officers" — not "Meet the team of 12 officers!"
- ✅ "Build a new agent" — not "Create your hero!"
- ✅ "Deploy" — not "Launch your team into the wild!"
- ✅ "Session A spec keeper; orchestrates project‑level work via the team in Session B." (terse, technical, comma‑joined clauses)
- ✅ "Writes plans, not code." (clipped, declarative)
- ❌ "Empower your team to ship faster." (banned)
- ❌ "Your AI dream team awaits." (banned)
- ❌ Emoji in body copy. Allowed only inside fenced code samples or status indicators where a glyph carries information (✓ ✗) — and even there a real icon is preferred.

### Punctuation & rhythm

- The em‑dash — used freely — is a feature, not a bug. The voice is essayistic.
- Lists are scannable: short stems, bold lead‑ins for the noun, then a sentence of explanation.
- Bullets end without periods if they are fragments. Sentences get periods.
- Backticks (`` `like this` ``) are mandatory for: officer names, skill names, file paths, tool names, JSON keys, CLI invocations.

### Headings and IA

- Three primary tabs (`Team`, `Skills`, `Meta‑aspects`). Title‑case nouns; never verbed ("Browse Skills" — no).
- Action labels are imperative verbs: `Edit`, `Clone`, `Add to roster`, `Deploy`, `View JSON`.
- Empty states are informational, not cute. ("No officers match this filter." — full stop.)

### Profanity / cuteness budget

- None. Zero whimsy. No mascots, no animals, no "rocket ship to launch," no dancing emoji. Wit is allowed when it's *true* — e.g. "agents with character — not stupid robots" — but never as a substitute for substance.

---

## Visual foundations

The system answers the question: **what does a power tool look like when it has been thought about for a long time?** Linear's restraint, Notion's prose comfort, Anthropic Console's sense of calm — with a faint editorial / classical accent.

### Colors

A **warm‑neutral** ground (papyrus, not pure white) keeps the screen calm during long reading sessions. A single **ink‑blue** accent carries primary actions; everything else is grayscale. Dark mode is first‑class — near‑black, never pure — with a softer steel‑blue accent.

- **App background:** warm off‑white `#FAF9F6` / dark `#14130F`.
- **Surface:** `#FFFFFF` / `#1B1A16` for cards. Borders are 1px and quiet.
- **Accent:** `#2B4A7F` (light) / `#7CA1D4` (dark). Used for primary buttons, links, active states, focus. Never for decoration.
- **Rank coding** (gold / silver / bronze) is the *only* place we let warm metallic color in. It's small — chips and dot indicators — never section background. Major = gold, Captain = silver, Lieutenant = bronze.
- **Archetype tints** are even quieter: a 1px left border or a 6px square on an officer card. Low‑contrast; never the dominant axis of the page.

### Type

Two faces, period.

- **Inter** for everything sans (UI, headings, prose). 400 / 500 / 600 / 700.
- **JetBrains Mono** for everything mono (officer names, skill names, paths, code, archetype labels, JSON snippets).
- **Cormorant Garamond** is permitted as an editorial flourish on slide covers and marketing surfaces only — never in app chrome.

5 sizes max in‑app: `xs/12 sm/13 md/14 lg/16 h3/20 h2/28 h1/36`. The display size (56px) lives on covers, not screens.

### Spacing

4‑px base. The scale is 4 / 8 / 12 / 16 / 24 / 32 / 48 / 64. Density tilts toward the lower half — power‑user views use 8 and 12 freely; only landing pages and slide covers reach 48+.

### Backgrounds

- **No gradients** for primary surfaces. The accent gradient is reserved for one place: the empty‑state background of the marketing/landing surface, and even there it's a soft 8% accent wash, never a saturated color sweep.
- **No full‑bleed photography.** This is not a consumer brand.
- **Texture** appears in exactly one place: a faint `peristyle.svg` colonnade pattern at 4% opacity, used as a watermark behind hero copy on slide covers. Off by default, opt‑in.
- **No hand‑drawn illustrations.** The brand drawing voice is a thin‑stroke geometric line, used sparingly as iconography.

### Animation

Quick and unshowy.

- Durations: **120 / 180 / 260ms.** Anything longer feels broken in a dev tool.
- Easing: standard `cubic-bezier(0.2, 0, 0, 1)` (Material's "standard"). No bouncy springs.
- Use cases: hover background fade (180ms), focus ring (120ms in), tab indicator slide (260ms with a small overshoot via `--ease-out`), modal scale‑in (180ms with opacity).
- No scroll‑triggered animations. No parallax. No marquees.

### Hover / press / focus

- **Hover** on cards: 4% surface darken (light) / 6% lighten (dark). No lift, no shadow growth, no scale.
- **Hover** on buttons: accent darkens by one step (`--accent-hover`).
- **Press** on buttons: accent darkens further (`--accent-press`); no shrink transform.
- **Focus**: a 3px tinted ring (`--shadow-focus`) — visible on keyboard, suppressed on mouse via `:focus-visible`.
- **Active link**: 1px underline drawn with `border-bottom`, never `text-decoration: underline` (which renders ugly under most fonts).

### Borders, radius, shadow

- **Borders 1px, low contrast** (`--border-1`). Ranks/states bump to `--border-2` or `--border-3` on focus. Never thicker than 1px in dev‑tool surfaces; 2px is reserved for dividing rules between hero sections on covers.
- **Radii**: 4 (chip), 6 (button/input — the default), 10 (card), 16 (large surface). The pill `999px` is for status pills only. **No fully‑rounded corners on anything bigger than a chip.**
- **Shadows**: three steps, all *very* soft. Light mode: `rgba(20,18,12, 0.04)` start. Dark mode: short, sharp. Cards in browse views use `--shadow-1`; menus/popovers use `--shadow-2`; modals/command palette use `--shadow-3`. **Never** combine border + heavy shadow.

### Layout rules

- **Tabs at the top** for primary nav, not a side rail. The three primary tabs sit on the app header.
- **Two‑pane** for detail views: left sidebar with metadata chips (sticky), right column with rendered markdown body, `max-width: 76ch`.
- **Card grid** for browse: 4–5 cards across at desktop. Cards are flat surfaces with a 1px border and a subtle hover, not floating.
- **Sticky** elements: app header, detail‑view sidebar. Nothing else floats. No FABs.

### Transparency / blur

- The command palette overlay uses a 60% surface tint with `backdrop-filter: blur(12px)` (light) / `blur(16px)` (dark). That is the *only* place blur is used.
- Disabled inputs/buttons use 60% opacity, not a different fill.

### Cards

- 1px border, `--radius-3` (10px), `--bg-surface`, `--shadow-1`.
- Internal padding: `space-4` (16px) on mobile, `space-5` (24px) on desktop.
- Header/body hierarchy: officer name (mono, h3) → metadata row (caption, chips) → role summary (1–2 lines, fg‑2). Footer optional; if present, a 1px top divider, `space-3` padding.

### Imagery vibe

When generic imagery is needed (rare): warm, grainy, slightly desaturated, with a film‑stock feel. Black‑and‑white architectural photography of colonnades is the canonical reference — cool stone, warm afternoon light. **No people**, **no AI‑generated abstract gradients**, **no isometric 3D illustrations**.

---

## Iconography

The brand is **icon‑light**. Icons appear only where they carry information you can't carry in a label — they never decorate.

### System

We use **Lucide** (https://lucide.dev) via CDN as the universal icon set. Reasons: (1) the codebase brief specifies Tailwind + shadcn/ui, and Lucide is shadcn's default icon system; (2) thin 2px stroke matches our editorial sensibility; (3) full coverage with no licensing surprises.

```html
<!-- via CDN -->
<script src="https://unpkg.com/lucide@latest"></script>
<i data-lucide="users-round"></i>
<script>lucide.createIcons();</script>
```

> **🚩 Substitution flagged.** The agent‑character‑builder codebase is pre‑development; no icon set is shipped yet. We've adopted Lucide as the default. **Confirm or override** when the implementation begins.

### Sizes

- **14px** inline beside text (button affordances, chip leading icons).
- **16px** default in row toolbars and menus.
- **20px** for tab icons and prominent affordances.
- **24px+** is reserved for empty‑state inline graphics and slide covers.
- Stroke weight 2 (Lucide default). Never two weights on the same screen.

### Color

Icons inherit `currentColor` and follow text contrast levels — `--fg-2` by default, `--fg-1` when active, `--accent` when on an action surface. **Never** filled tonal icons; **never** brand‑accent icons used decoratively.

### Emoji

Banned in product UI and marketing copy. The single carve‑out: status indicators in the README and SKILL.md frontmatter where ✓/✗/🚩 carry compact information for human readers scanning the document. Even there, prefer Lucide in the rendered product.

### Unicode glyphs as icons

Permitted only for: arrows in inline text (`→`), bullets (`·`), and the section delimiter (`§`). Everything else is a Lucide icon.

### Brand marks

The mark is the **stoa column** — a single hand‑set Doric column glyph, drawn as a flat black silhouette. It's the only piece of decorative SVG the system contains. Files in `assets/`:

- `mark.svg` — the column alone.
- `wordmark.svg` — column + "The Stoa" set in Inter Tight 600.
- `peristyle.svg` — repeating column pattern, used as the watermark texture.

---

## Components shorthand

Components are documented in the preview cards and recreated in `ui_kits/character-builder/`. The skeleton vocabulary is:

- **Button** — primary (accent fill), secondary (border, transparent fill), ghost (no border, hover fill), danger (red).
- **Chip** — pill or square; mono text by default. Variants: rank, archetype, tool, plain.
- **Input / Textarea** — 1px border, 6px radius, focus ring.
- **Card** — flat surface, 1px border, 10px radius. Hover is a 4% darken.
- **Tabs** — top‑aligned, underline indicator, accent.
- **Command palette** (⌘K) — modal overlay, blur backdrop, fuzzy‑filtered list.
- **Two‑pane detail** — sticky sidebar + scrollable prose pane (max‑width 76ch).
- **Wizard step header** — `1 of 5` counter + crumb trail; horizontal layout.

---

## Caveats / things I made up

- **Fonts:** Inter and JetBrains Mono are loaded from Google Fonts as substitutes. The brief says "Inter, Söhne, system‑ui" / "JetBrains Mono, Söhne Mono" — Söhne is licensed, so Inter is the open substitute. Override if you have Söhne.
- **Iconography:** Lucide chosen because the brief implies shadcn/ui (which uses Lucide) — confirm with the implementer.
- **Brand mark:** The "Doric column" mark is a system invention; the brand brief did not provide a logo. Treat it as a placeholder until the user provides a real mark.
- **Color palette:** "warm‑neutral + ink‑blue" is the design call. The brief said "calm primary (slate or indigo)"; ink‑blue sits between them and matches the editorial register. Override if you'd rather have indigo or emerald.

---

## Status

This system was generated against a **pre‑development** product brief. No production code exists yet. The UI kit in `ui_kits/character-builder/` is therefore a **first‑pass interpretation** of the BRIEF + DESIGN_PRINCIPLES — not a recreation of an existing app. When implementation begins, expect this system to evolve against real screens.
