# Brief: testid identifier escaping for special characters

**Status:** Brief filed (not dispatched). 2026-05-01.
**Suggested ticket id:** `acb-NNN-testid-special-char-escaping`. Number assigned at dispatch time.
**Pipeline shape:** **build-only** — ADA-direct after a small data-layer audit. No design needed.
**Effort:** ~30min (audit) + ~30min (fix if any names trip the audit).
**Surfaced by:** VERA verification of acb-008 (2026-05-01), top-3 concerns #2.
**Sequence constraint:** lands BEFORE acb-007 (`agent-design-tutor` skill) if any current name fails the audit; otherwise opportunistic — can fold into the first arc that touches data-layer naming.

## Background

acb-008 landed `data-testid` attributes whose identifiers interpolate runtime data: `officer-card-${officer.name}`, `skill-card-${skill.name}`, `meta-card-${name}`, `lieutenant-chip-${l}`, `palette-result-officer-${name}`, `palette-result-skill-${name}`, `filter-archetype-${name}`. The naming convention documented in `Components.tsx:11-31` says identifiers are preserved as-is.

If any current or future officer/skill/meta-aspect/archetype name contains a character that breaks CSS attribute selectors — space, `"`, `\`, `]`, `:`, `/`, `#`, `>`, `+`, `~`, `*`, or non-ASCII — then `document.querySelector('[data-testid="officer-card-foo bar"]')` will fail or behave unpredictably. acb-007 (`agent-design-tutor` Claude Code skill) is the downstream consumer that drives the app via Chrome MCP using these selectors; this is exactly the failure mode that breaks the skill.

## In scope

### Phase 1 — audit

Grep all data-layer names that flow into a testid:

```
grep -E '"name"\s*:' src/data/sample.ts
```

For each name, check:
- ASCII-only? (no unicode)
- No spaces, `"`, `\`, `]`, `[`, `:`, `/`, `#`, `>`, `+`, `~`, `*`, `,`, `;`, `(`, `)`, `=`, `!`, `?`, `@`?
- No leading digit? (CSS selector quirk in some contexts)

Today the names are all snake_case ASCII (`MAJOR_PLINY`, `dispatch-lieutenant`, `inter-agent-comms`) so the audit likely passes for v0.1 sample data. acb-002's adapter from `agent-team-team/definitions/` may surface names that fail.

### Phase 2 — fix (only if audit fails)

Two strategies, pick one:

**A. Slug-and-document.** Apply a `testidSafe(name)` helper that replaces unsafe chars with `-`, document in the convention comment. Risk: collisions if two names slugify to the same string — vanishingly rare in practice but possible.

**B. Escape via attribute-selector quoting.** Don't change the testid; document in the convention that consumers MUST quote identifiers in attribute selectors (`[data-testid='officer-card-foo bar']`). Risk: shifts complexity to consumers.

DAEDALUS calls if Phase 2 triggers; current best guess is A (slug-and-document) because Chrome MCP scripts read better with simple selectors.

## Out of scope

- Changing the convention itself (kebab-case, entity-then-id).
- Adding `data-testid` to surfaces not already covered by acb-008.
- Mutation API (`STOA_DISPATCH`) — separate brief if needed.

## Definition of done

1. Audit script (one-shot bash + grep, can live inline in this ticket — no need to commit) run against `src/data/sample.ts` and `agent-team-team/definitions/` (post-acb-002).
2. If audit passes: comment added to `Components.tsx:11-31` convention block stating "all current data-layer identifiers are testid-safe; if any future name introduces special chars, escape per [strategy]." Done.
3. If audit fails: implement chosen strategy; re-run audit; pass.
4. acb-008's existing testids continue to work for all currently-named data.

## Composition

- **Composes with acb-002** (gen-data + adapter): the adapter is the natural place to apply `testidSafe(name)` if Strategy A is picked. Bundle if both arcs are open.
- **Hard sequence constraint vs acb-007**: if audit fails, fix lands BEFORE acb-007. If audit passes, no constraint.

## Open question

None for now — Phase 1 is a 5-minute grep. Run it before deciding whether to escalate.

## Why this isn't acb-008's problem to solve

acb-008's spec §3 says identifiers preserve as-is. Today's data is all safe. The failure mode is a future name nobody has written yet. Per fix-now-or-plan-now discipline, this is the "plan now" half: concrete next step (run audit), concrete trigger (any unsafe char), concrete strategy (slug-and-document, or document-and-quote).
