# Claude Design brief — case study mini-site

**Audience for the brief:** Claude Design (claude.ai/design).
**Driven by:** PRINCIPAL Denson Smith (paste this brief + upload `case-study.md` into the Claude Design session).
**Source content:** `the-stoa/docs/case-study/case-study.md` (359 lines, markdown).
**Target consumer of the output:** the **beadworks team** (peer-technical audience that thinks in message-bus + multi-actor coordination terms).

---

## What to make

A polished **long-form scrolling mini-site** rendering the case-study markdown as a readable, navigable single page. Not a slide deck. Not a multi-page site. One scrolling page with section anchors so a navigator can jump between sections (and so a POLYBIUS-driven tour can `scroll-to` specific sections via the Chrome MCP).

The case study explains what was built across a 36-hour engagement that produced a recursive three-role agent architecture on top of the beadworks tool. The tone is peer-to-peer technical: "here's what we built, here's why each choice, here's what we'd want to discuss with you" — explicitly NOT a sales pitch and NOT a 101 explainer.

---

## Use The Stoa design system

The Claude Design environment should already have The Stoa design tokens (the agent-character-builder design handoff was the seed). Use those tokens — typography, colors, rank pills, dark mode + light mode — for visual consistency with the running Stoa app. The case study mini-site will eventually embed in (or live alongside) the Stoa app at `/#/about` or similar.

If the design system isn't loaded automatically, the source tokens live in the repo at `the-stoa/app/design_handoff_character_builder/tokens/colors_and_type.css`.

---

## Section structure (already in the markdown)

12 numbered sections plus subsections — preserve the structure; the markdown is already cleanly sectioned:

1. What this is and why we're showing it to you
2. The architecture in one diagram (placeholder for embedded KG — see separate KG brief)
3. Why three roles, not one
3.5. How trust distributes across the three roles (three load-bearing patterns)
4. Why recursion
5. Why voice discipline is structural
6. Information flow with cycles
6.5. Two operational modes — formal gauntlet vs. pair-programming for prototyping
7. Beadwork as durable substrate
8. Disciplines (the 22 `u--7yg` empirical observations)
9. Worked example — Arc 14, sub-project spawning
10. Where this is going — the hypergraph and the agentic team that builds it
11. Open questions and what we'd want to discuss
12. How to engage

A floating table-of-contents on the side (or sticky top-right) helps long-page navigation. Section headers should be deep-linkable (`/#section-3-why-three-roles`).

---

## Visual rhythm / layout

**Long-form prose** dominates — this is a working notebook offered for review, not a marketing page. Wide reading column (640-720px) for prose; allow tables and code blocks to break out wider when content needs it.

**Tables matter** — the case study uses comparison tables in §3, §3.5, §6.5, §7, §8. Make them readable; consider zebra-striping for dense rows.

**Code blocks** — the case study has bash snippets in §12 (the engagement instructions). Treat as monospace blocks with The Stoa's mono token (JetBrains Mono).

**Pull quotes** — the empirical-claim quote in §6.5 ("we started moving much faster when…") is worth visual emphasis as a pull quote.

**Section headers** — preserve the §N numbering; this is field-notes-shaped, not marketing-shaped. The numbering is part of how the substrate cross-references itself.

---

## Embedded artifacts

The case study refers to **two embedded artifacts** that will land separately:

- **§2 — Information-flow KG visualization.** Placeholder for now; see separate `claude-design-brief-kg.md` for that piece. Leave a clearly-marked container/iframe slot in the layout.
- **§9 — Worked example illustrations.** Optional: a small inline diagram showing the Arc 14 dispatch → execution → ship flow could complement the prose. Not load-bearing; nice-to-have.

---

## Constraints

- **Dark mode + light mode** both first-class. The Stoa design system handles both; preserve the toggle.
- **Mobile-friendly** but the primary audience reads on desktop (technical peer review). Optimize for desktop; mobile is graceful degradation.
- **No bespoke fonts beyond The Stoa tokens** (Inter for prose, JetBrains Mono for code/identifiers).
- **Section anchors for the POLYBIUS tour.** Each `## N. Section Name` heading should produce a deep-linkable anchor that the Chrome MCP can navigate to via `window.location.hash = '#section-N'`.

---

## Handoff back

Claude Design produces a handoff bundle (HTML + tokens + maybe React component code). PRINCIPAL hands it to Claude Code (this seat or a build-session) to implement as a React view in `the-stoa/app/src/` rendered at `/#/about` (or similar route — naming TBD).

The handoff should include: HTML/JSX structure, CSS tokens used, any custom components, font imports if needed.

---

## What to AVOID

- Marketing-page conventions (hero with floating screenshot, CTA buttons, testimonial cards). This is field notes, not a pitch.
- Stock illustrations, icons that aren't structural (small icons next to section headers or in tables are fine).
- Excessive whitespace between sections. The substrate is dense; the design should respect that.
- Replacing the §N numbering with prose-only headers. The numbering is a load-bearing convention.

---

## After this design pass

1. PRINCIPAL reviews + iterates the design in Claude Design (inline comments, sliders, etc.)
2. PRINCIPAL accepts → exports the handoff bundle
3. PRINCIPAL hands bundle to Claude Code (this seat)
4. Claude Code implements as a React view in the Stoa app
5. Tour script (separate work — `substrate/templates/tour-script.md`) wires POLYBIUS to navigate the live page via Chrome MCP

Standby — PRINCIPAL drives the iteration loop in Claude Design.
