# Design principles

The aesthetic + UX rules for agent-character-builder. Reference these when designing screens.

## Aesthetic

**Modern dev-tool.** Reference points: Linear, Notion, Vercel dashboard, Stripe dashboard, Anthropic Console. The app should feel like something a developer who uses Linear daily would respect.

NOT a consumer app. NOT a chat interface. NOT a children's game. NOT skeuomorphic.

## Typography

- **Monospace** for: officer names (MAJOR_PLINY), skill names (runner), code references, tool names, file paths, JSON snippets, archetype labels
- **Sans-serif** for: descriptions, prose, instructions, role summaries, button labels, navigation
- Use one humanist sans (Inter, Söhne, system-ui) and one mono (JetBrains Mono, Söhne Mono, ui-monospace). No display fonts.
- Restrained type scale: 4-5 sizes max across the app.

## Density

Power users tolerate density. Don't waste screen space on whitespace cushioning when there's information to show.

- Officer-card grids: 4-5 across on desktop, not 2
- Tabular data when shape allows
- Inline metadata (chips, badges) instead of separate sections when possible
- Use scroll, not pagination, for browse views

## Color

Restrained palette:
- **Background**: near-white (light mode) or near-black (dark mode); avoid pure white/black
- **Primary surface**: subtle warm gray for cards, panels, sidebar
- **Borders**: very subtle — 1px, low contrast
- **Accent**: one color for primary actions (blue, indigo, or emerald). Use sparingly.
- **Rank coding**: distinguish major / captain / lieutenant via subtle color or weight on a chip/badge — but don't make it the dominant visual axis
- **Archetype coding**: optional secondary color hint per archetype; keep low-contrast so the page doesn't feel like a rainbow

Dark mode is a first-class consideration; the app should look good in both.

## Layout patterns

**Card grid for browse**: officer roster, skill library. Each card has a clear hierarchy: name (largest, mono) → key metadata (medium) → description (smallest, prose).

**Two-pane for detail**: sidebar metadata (tools, lieutenants, etc. as chips) + main content area (rendered markdown body). Like reading docs.

**Multi-step wizard for compose**: each step is a clear page. Show progress (1 of 5). Don't cram steps into accordions.

**Form for author**: standard form patterns. Multi-select with searchable dropdowns. Markdown editor with raw + preview tabs (or split view if screen real estate allows).

**Tabs at the top**, not side nav, for the three primary views (Team / Skills / Meta-aspects). The wizard + author flows can be modal or full-page.

## Interactions

- Click officer card → Officer Detail page (route `/officer/<NAME>`)
- Click skill card → Skill Detail page (route `/skill/<name>`)
- Hover effects subtle: slight bg-color shift on cards, no scale transforms or shadows pulling out of the page
- Keyboard nav: Tab through grid items, Enter to drill in, Esc to back out
- Search: cmd-K opens a global search palette (officers + skills + meta-aspects in one list)
- Markdown bodies use prose typography (max-width ~70-80ch for readability), NOT raw monospace text walls

## Voice for app copy

Plain English. Direct. Not cute.

- "12 officers" not "Meet the team of 12 officers!"
- "Build a new agent" not "Create your hero!"
- "Deploy" not "Launch your team into the wild!"
- Role summaries are already plain; preserve that voice in headers/instructions

## What NOT to do

- No tab/accordion/dropdown explosion for content that should just be visible
- No empty-state cartoons or illustrations
- No marketing copy ("Build amazing teams!")
- No floating action buttons or material-design vibes
- No huge hero sections — this is a power tool, not a landing page
- No login screens (it's local; single user)
- No notifications/toasts unless something actually needs the user's attention
