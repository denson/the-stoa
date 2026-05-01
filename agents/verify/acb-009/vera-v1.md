# VERA Verification — acb-009-router-url-state v1

**Verifier:** VERA (`VERA_agent_character_builder`)
**Target:** Implementation by ADA against `agents/specs/acb-009-router-url-state.md` (post-ARGUS-reconciled, with POLYBIUS-issued Override 1 + Override 2).
**Spec:** `agents/specs/acb-009-router-url-state.md` — §5 lists DoD criteria (with §5 #5 deferred per Override 1).
**Verdict:** **`pass-with-flags`** — 5 PASS / 1 DEFERRED-WITH-PLAN. No code defects.

---

## Per-criterion table (spec §5)

| # | Criterion | Result | Evidence |
|---|---|---|---|
| §5 #1 | Direct deep-link `/officer/MAJOR_PLINY?roster=default` | **PASS** | Probe: `h1="MAJOR_PLINY"`, `STOA_STATE.selectedOfficer.name="MAJOR_PLINY"`, `currentTab=team`, `roster=default` (initial-load behavior per §9.7). |
| §5 #2 | Browser back/forward navigates view stack | **PASS** | `/` → `/officer/MAJOR_PLINY` → back → `/` (selected=null, tab=team) → fwd → officer detail (selected=MAJOR_PLINY). `/skills` → `/meta` → back returns `currentTab=skills`. |
| §5 #3 | Refresh on any URL lands on the same view | **PASS** | Reload on `/officer/MAJOR_PLINY?archetype=architect` re-renders MAJOR_PLINY h1 with `archetypeFilter=architect`. Reload on `/skills` re-lands on Skills. |
| §5 #4 | ⌘K palette navigates by URL, not local state | **PASS** | Synthesized Cmd+K → `palette-input` rendered → typed "PLINY" → clicked `[data-testid="palette-result-officer-MAJOR_PLINY"]` → URL became `/#/officer/MAJOR_PLINY`, palette closed, `STOA_STATE.selectedOfficer.name="MAJOR_PLINY"`. |
| §5 #5 | Vitest route-resolution test green | **DEFERRED-WITH-PLAN** | `agents/follow-ups/acb-009-followup-route-resolution-test.md` exists with status, BLOCKED-BY acb-002 sequence constraint, concrete ~20-line test shape, DoD covering this commitment. Per Override 1 reconciliation. |
| §5 #6 | STOA_STATE bridge migrated to URL-driven reads | **PASS** | Shape post-`/officer/ADA?roster=minimal&archetype=executor`: keys=`[archetypeFilter, currentTab, dark, roster, selectedOfficer]`, all values match URL. Reactivity probe (400ms wait): `a !== b` after hash change `/` → `/skills` (refIneq=true). |

## Mechanical re-checks (independent of ADA's self-report)

| Check | Result |
|---|---|
| `useState` survivors in `App.tsx` | Only `q` (CommandPalette internal, line 884) + `paletteOpen` (line 1292). Migrated 4 fields all gone. |
| `set(Tab|Selected|Roster|ArchetypeFilter)` survivors | Only `setRoster` wrapper function at `App.tsx:1130` (calls `setSearchParams` — correct), prop name at `:255/:261/:1146`, click handler `:305`. No surviving `useState` setters. |
| `npx tsc --noEmit` | Clean (no output). |
| `npm run build` | Clean: `✓ 1592 modules transformed`, `dist/index-BbRvVdX2.js 271.10 kB`. |
| `npm run dev` | Starts on 5176 (5173-5175 in use). |
| `react-router` pin | `^7.14.2` confirmed in `package.json` + `package-lock.json`. ADA imports from `react-router` not `react-router-dom` — idiomatic v7 per [React Router v7 docs](https://reactrouter.com/upgrading/v6); spec §3's `react-router-dom` superseded by v7 consolidation. Web-search-verified. |
| `main.tsx` HashRouter wrap | `HashRouter` outside `ThemeProvider` (line 10-14). Correct per design D7. |
| `stripDefaultSearchParams` | Pure top-level helper at `App.tsx:88-103` per Override 2. |
| `STOA_STATE` JSDoc | `App.tsx:1327-1370` updated to note URL-derived source for currentTab/selectedOfficer/roster/archetypeFilter; contract surfaces (read-only, single-object replace, ref-equality, `(window as any)`) preserved. |
| Follow-up brief | Present, well-shaped, sequence-constraint explicit. |

## Manual probes (the headless-ADA gap)

| Probe | Result | Evidence |
|---|---|---|
| Back/forward across `/` ↔ `/officer/X` | **PASS** | `history.back()`/`forward()` round-trip preserves `selectedOfficer` state; tab derives correctly. |
| Back across `/skills` → `/meta` → back | **PASS** | `currentTab=skills` after back. |
| ⌘K palette → click officer | **PASS** | URL = `/#/officer/MAJOR_PLINY`, palette unmounts, STOA bridge updates. |
| Default-stripping after toggle round-trip | **PASS** | `?roster=default&archetype=architect` → click filter chip → URL becomes `?archetype=architect` (`roster=default` stripped). |
| Refresh on `/skills` | **PASS** | `Page.reload` lands back on Skills view. |
| Unknown-route `/garbage` | **PASS** | Navigates replace to `/`, team view renders. |
| Unknown-officer `/officer/NOT_A_REAL_OFFICER` | **PASS** | Renders "not found" + "Back to Team" link, no crash. |

Probe artifacts: `agents/verify/acb-009/probe.mjs`, `agents/verify/acb-009/probe-targeted.mjs`.

## Top-3 most-concerning items for downstream consumers

1. **STOA_STATE timing for acb-007 (`agent-design-tutor`).** Post-commit effect timing means a skill calling `element.click()` then synchronously reading `STOA_STATE` sees the prior snapshot. JSDoc documents this (`App.tsx:1358-1363`) but acb-007 author must internalize the "wait one microtask or observe ref-inequality" rule. A skill that doesn't will see flaky stale-read bugs.
2. **`buildPreservedQuery` does not preserve unknown query params.** Lines 73-83 only echo `roster` (if non-default) and `archetype` (if set). If acb-006/acb-007 ever introduce a third query param (e.g., `?step=3` for tutorial state), navigating via `<Link>`/`navigate()` through any route-change site will silently drop it. Filed for awareness, not blocking.
3. **`tabFromPath` order-of-prefix-checks subtlety.** `/skills` and `/skill/:name` both originally matched `pathname.startsWith("/skill")` → `"skills"` tab. Correct today, but if a future route `/skillset/:x` is added, it'll incorrectly resolve to skills tab. **Addressed in ADA revision** per CATO finding #2 / VERA concern #3.

## Verdict

**`pass-with-flags`** — all 6 DoD criteria pass (5 PASS, 1 DEFERRED-WITH-PLAN per Override 1). No code defects. Mechanical checks all clean. Two probe failures in initial run were both harness limitations (DOM heuristic vs. testid; RAF wait too short for React effect commit) — re-probed with proper testids and longer wait, both PASS. Top-3 concerns are forward-looking notes for acb-006/acb-007 authors, not blockers for landing.
