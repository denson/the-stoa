# Follow-up: acb-009 — route-resolution Vitest test

**Title:** acb-009 follow-up — route-resolution Vitest test
**Status:** Filed during acb-009 (2026-05-01). Deferred pending acb-002 Vitest scaffold.
**Severity:** Low — runtime DoD criteria 1, 2, 3, 4, 6 pass; this discharges the only deferred criterion (DoD #5).
**Pipeline shape:** build-only, ADA-direct, ~30min once acb-002 is in.
**Sequence constraint:** WILL BE BLOCKED BY acb-002 (Vitest scaffold). Dispatch this follow-up after acb-002's scaffold lands.
**Source:** acb-009 spec §5 DoD #5; design §1 (DAEDALUS verdict: sequence-with-follow-up); ARGUS findings reconciled by POLYBIUS as Override 1 (file NOW, not optionally).

## Background

acb-009 migrates the Stoa app's navigation state (`tab`, `selected`, `roster`, `archetypeFilter`) from local React state to URL-driven state via `react-router@^7.14.2` (HashRouter). Spec §5 DoD #5 commits to "at least one route-resolution Vitest test green" — minimum viable: render `<App>` inside a `MemoryRouter` with `initialEntries={["/officer/MAJOR_PLINY"]}` and assert the OfficerDetail renders for MAJOR_PLINY.

acb-009 ships without this test because the Vitest scaffold (`vitest.config.ts`, RTL setup, test dir convention) does not yet exist in the repo. acb-002 (gen-data adapter) is the natural owner of the scaffold — it has its own adapter-fixture round-trip test as part of its DoD. Adding a half-scaffold in acb-009 would race acb-002's full scaffold for ownership of `vitest.config.ts`; that's a discipline-break.

Runtime confidence for acb-009 was established via VERA's manual probes and an ADA-side headless-Chrome smoke run (10 probes, all PASS): direct deep-link, refresh-survival, back/forward, palette URL navigation, STOA_STATE shape preservation. The Vitest test is a CI-discoverability win, not a correctness blocker for this arc.

## Why filed now

Per `C:\Users\denso\.claude\CLAUDE.md` lines 67-69:

> Known bugs do not cross session boundaries without a written plan. If a session closes with a known bug still open, there is a ticket with a plan already written for the next session to execute against.

This deferral is structural (acb-002 owns the scaffold), not optional. POLYBIUS's Override 1 reconciled ARGUS's R11 finding by striking design §1's "ADA optionally files…" hedge — the brief lands as a discoverable disk artifact during acb-009, not in someone's memory.

## Concrete plan

1. **Wait for acb-002 to land.** Do not dispatch this follow-up until acb-002 has installed Vitest + React Testing Library + jsdom and shipped a working `npm test` (or `npm run test`) entry point.

2. **Add one new test file** at the path acb-002 establishes as the test convention (likely `src/__tests__/routing.test.tsx`, or co-located `src/App.test.tsx` — defer to acb-002's choice).

3. **Test shape (~20 lines including imports):**

   ```tsx
   import { render, screen } from "@testing-library/react";
   import { MemoryRouter } from "react-router";
   import { ThemeProvider } from "../hooks/useTheme";
   import App from "../App";

   describe("acb-009 route resolution", () => {
     it("/officer/MAJOR_PLINY renders the MAJOR_PLINY detail view", () => {
       render(
         <MemoryRouter initialEntries={["/officer/MAJOR_PLINY"]}>
           <ThemeProvider>
             <App />
           </ThemeProvider>
         </MemoryRouter>
       );
       // OfficerDetail renders the officer name in an <h1>
       const heading = screen.getByRole("heading", { level: 1, name: "MAJOR_PLINY" });
       expect(heading).toBeInTheDocument();
     });
   });
   ```

   **Note:** wrap in `<MemoryRouter>`, NOT `<HashRouter>` — `MemoryRouter` accepts `initialEntries`, which is the standard test-time pattern. The production app still uses `HashRouter` (in `src/main.tsx`).

   **Note:** `ThemeProvider` wrap is required — `App` calls `useTheme()` and would crash without it. ADA sees the same pattern in `src/main.tsx`.

4. **Definition of done:**
   - `npm test` runs and the new test passes.
   - The test demonstrates that `/officer/MAJOR_PLINY` routing resolves to the OfficerDetail render path.
   - Discharges acb-009 spec §5 DoD #5.

## Out of scope for this follow-up

- Adding tests for other routes (`/skills`, `/meta`, `/skill/:name`, `/meta/:name`, the `*` 404 fallback). One route-resolution test is the spec commitment; broader test coverage is its own brief.
- Adding tests for `STOA_STATE` shape — runtime probe is sufficient until/unless a regression points at the bridge.
- Adding tests for query-param round-trips (`?roster=`, `?archetype=`) or default-stripping. Those would be valuable but are not the spec commitment for acb-009.
- Refactoring `App` to be more test-friendly (e.g., separating route definitions to a separate file). Out of scope; the existing structure tests fine with `<MemoryRouter>`.

## Composition

- **WILL BE BLOCKED BY acb-002** — the Vitest scaffold is acb-002's deliverable.
- **Composes with acb-006** (in-app tutorial), acb-007 (`agent-design-tutor` skill) — both consume the URL-driven state acb-009 established. A passing route-resolution test gives downstream arcs a regression-safety net.
- **No relationship to acb-005 (a11y arc)** — that arc's element-type changes are independent of routing.
