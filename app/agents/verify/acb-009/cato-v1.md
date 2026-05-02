# CATO Final Review — acb-009-router-url-state v1

**Reviewer:** CATO (`CATO_agent_character_builder`)
**Target:** Implementation by ADA, post-VERA verification, with POLYBIUS-issued Override 1 + Override 2.
**Verdict:** **`pass-with-nits` — fix-and-ship.**

---

## Summary

Diff is structurally faithful to spec + design + reconciliation overrides. Severity counts: **0 blocker / 1 concern / 4 nits**. Three minimal fixes recommended before commit; once landed, ship it.

## Findings

### F1 — design.md not reconciled to post-ARGUS state — concern (documentation hygiene)

- **Severity:** concern
- **Category:** documentation hygiene
- **Where:** `agents/design/acb-009/design.md:32` (D9) and `:168-181` (§5 helper pseudocode).
- **What:** Design.md still shows the pre-ARGUS state — D9 names `setSearchParamsStripDefaults` as a hook, and §5 shows `useCallback`-bearing pseudocode. POLYBIUS Override 2 (drop `useCallback`; pure top-level `stripDefaultSearchParams`) is reflected in the *code* (`App.tsx:97-103`, `App.tsx:1129` comment) but NOT in the design artifact. Future readers reconstructing the arc will be misled.
- **Suggested fix:** append a `§14 — Post-ARGUS reconciliation` section to design.md noting Overrides 1+2 verbatim, OR strike-through D9/§5 pseudocode and replace inline. **Addressed in ADA revision.**

### F2 — `tabFromPath` `startsWith("/skill")` is fragile-by-coincidence — nit (craft)

- **Severity:** nit
- **Category:** craft
- **Where:** `src/App.tsx:42-51`.
- **What:** Currently correct because the route table is exact, but `/skillset/:x` would resolve to `"skills"` tab silently if added.
- **Suggested fix:** `pathname === "/skills" || pathname.startsWith("/skill/")` for skills; same shape for meta. **Addressed in ADA revision.**

### F3 — Naming-convention drift across pure helpers — nit (cleared)

- **Severity:** nit
- **Category:** naming consistency
- **Where:** `src/App.tsx:97` (`stripDefaultSearchParams`) and `parseRosterParam`/`parseArchetypeParam`.
- **What:** Verb-first naming convention across all four helpers. **CLEAN as-is**; flagged for completeness only.

### F4 — `buildPreservedQuery` and `stripDefaultSearchParams` overlap on default-strip logic — nit (defer)

- **Severity:** nit
- **Category:** craft (DRY)
- **Where:** `src/App.tsx:73-83` (`buildPreservedQuery`) and `:97-103` (`stripDefaultSearchParams`).
- **What:** Both helpers reimplement parts of the default-strip logic. If a future arc adds a third stripped default, both must change.
- **Suggested fix:** **accept-and-defer.** YAGNI — no current consumer; speculative. Re-evaluate when `?step=` or similar lands.

### F5 — Stale JSDoc opener on `stripDefaultSearchParams` — nit (doc accuracy)

- **Severity:** nit
- **Category:** doc accuracy
- **Where:** `src/App.tsx:88-96` (the JSDoc above `stripDefaultSearchParams`).
- **What:** Opens with "Returns a setter that wraps `setSearchParams`…" — that was true of the pre-Override-2 hook shape. Current implementation returns a `URLSearchParams`, not a setter.
- **Suggested fix:** rewrite the opening sentence to match the actual signature. **Addressed in ADA revision.**

## Disposition of VERA's three forward-looking concerns

1. **STOA_STATE post-commit timing for acb-007** — **accept-and-document.** JSDoc at `App.tsx:1358-1363` already documents the microtask wait. acb-007 authors will read it. No action.
2. **`buildPreservedQuery` preserves only `roster`+`archetype`** — **accept-silently.** YAGNI. No current consumer; speculative. Re-evaluate when `?step=` actually lands.
3. **`tabFromPath` `startsWith("/skill")`** — **fix-now** (= F2 above). Per global fix-now discipline: see-it-once-fix-it-once. **Addressed in ADA revision.**

## Cold-read scan (CATO's distinct value-add)

### A. Code style + craft — minor finding (F2, F5; both addressed in ADA revision)

Route components are right-sized; placeholders worth their own components (mirrors structure for v0.3 expansion). Pure helpers follow verb-first naming.

### B. Scope drift — CLEAN

`git diff --stat` against `data/`, `scripts/`, `Components.tsx`, `hooks/`, `styles/` is empty. New `agents/verify/acb-009/probe*.mjs` files are VERA's verification artifacts.

### C. Hidden regression vectors — CLEAN

- No `useTheme()` consumer outside `<App>` subtree.
- `paletteOpen` survives migration (`App.tsx:1292`).
- `<Navigate replace>` for `*` is correct (no spurious history entry for fallback redirects).
- `stripDefaultSearchParams` strips ONLY `roster=default` and empty `archetype` (verified line 99-101).
- STOA_STATE JSDoc updated for URL-driven source (line 1343-1348).

### D. Documentation hygiene — concern (F1, addressed in ADA revision)

Design.md decisions table not initially reconciled to post-ARGUS state. Spec §3 `react-router-dom` deviation IS captured in design D6 + R9. Follow-up brief is concrete (test shape, deps, sequence constraint, DoD).

### E. acb-007 / acb-006 consumer lens — CLEAN

URL surface is ergonomic; pure `stripDefaultSearchParams` is *easier* for a skill consumer than a hook (no React-context dependency to mock). Override 2 helped this.

## Verdict

**`pass-with-nits` — fix-and-ship.** Three minimal fixes (F1, F2, F5) addressed in ADA revision. F3 is CLEAN; F4 deferred (YAGNI). All accepted. Ship.
