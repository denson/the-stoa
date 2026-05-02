# Arc 13 build directive

**Audience:** the fresh Claude Code session opened to build Arc 13 deliverables.
**Authored by:** user-tier Chief-of-Staff (POLYBIUS-equivalent) + the PRINCIPAL (Denson Smith).
**Status:** active directive.
**Builds on:** Arcs 9-12 — substrate redesigned, gen-data adapter live, sample.ts retired, components consume v2 types directly.

**You are MAJOR_PLINY for the the-stoa Arc 13 engagement.** Read `substrate/MAJOR_PLINY.md` and assume the orchestrator role. Open Claude Code in `~/claude_projects/the-stoa/`.

**Your one job for this engagement:** scaffold Vitest as the test runner for `app/`, author baseline tests for the load-bearing build-time + helper code (gen-data adapter, derive.ts), and resolve `stoa--b3f` (the gen-data timestamp churn). Then return cleanly.

This is a smaller arc than Arcs 10-12. Modest scope, clean independent pieces.

---

## Read first

1. **Arc 10's `app/scripts/gen-data.ts`** + `app/scripts/schemas.ts` — the build-time adapter you'll author tests for
2. **Arc 12's `app/src/data/derive.ts`** — the synthesis helper lifted from the retired sample.ts (now consumed directly by components); also worth a baseline test
3. **Arc 12's `app/src/data/generated/agents.ts`** — the deterministic output of gen-data; tests should verify shape + invariants
4. **Existing `app/package.json`** — current test setup (likely none yet) + dev dependencies
5. **`stoa--b3f` ticket** in this repo's bw — concrete plan for the gen-data timestamp fix; Arc 11's build session filed it after reverting the temporary fix to keep that arc scope-pure
6. **Planning v2 spec** §11 — The Stoa data-model implications (tests should verify the v2 invariants encoded there: 5 ranks, COLONEL reserved-empty, etc.)

---

## What Arc 13 is

Two related deliverables:

### Part A: Vitest scaffold

Standard test infrastructure for the `app/` package:
- Install Vitest + necessary support packages (`@vitest/ui` optional)
- Configure Vitest (probably co-located in `vite.config.ts` since Vite ships with Vitest support)
- Add `test` script to `package.json` (`npm test` runs Vitest)
- Author baseline tests covering at minimum:
  - **gen-data adapter (Arc 10)** — fixture-based test: feed it a synthetic role file, verify the parsed output matches expected `StoaDataV2` shape; verify Zod validation rejects malformed input descriptively
  - **derive.ts (Arc 12)** — test the body-first-paragraph synthesis on a few representative inputs (short body, multi-paragraph body, edge cases)
  - **generated/agents.ts shape invariant** — test that the actual generated file has 5 ranks, COLONEL slot is reserved-empty, MAJOR has POLYBIUS + PLINY, CAPTAIN has the 10 envelopes
- Tests run cleanly: `npm test` passes; `npm run build` still works (test files don't accidentally end up in the production bundle)

### Part B: `stoa--b3f` fix (gen-data timestamp churn)

The gen-data script writes a `Generated: <ISO timestamp>` comment header in `generated/agents.ts` on every run. This means every developer's `npm run dev` or `npm run build` produces a one-line dirty git diff. Annoying churn that obscures real changes.

Two paths per the ticket's filed plan:

- **(preferred) Drop the timestamp comment entirely.** Git history is authoritative for "when was this regenerated." The header just notes it's auto-generated + gives the regen command. No timestamp.
- **(alternative) Replace with deterministic fingerprint** of the substrate contents (e.g., SHA-256 of all role files concatenated). Header changes only when content changes, not on every run. Slightly more clever but probably overkill.

Build session decides; the preferred path is simpler. Surface only if you want to discuss.

---

## Deliverables

### 1. Vitest installed + configured

```bash
cd app
npm install --save-dev vitest @vitest/ui
```

(or just `vitest` without the UI — UI is optional)

Configure in `vite.config.ts`:

```typescript
/// <reference types="vitest" />
import { defineConfig } from 'vite';

export default defineConfig({
  // ...existing config...
  test: {
    environment: 'node',  // for build scripts
    // (or 'jsdom' if testing components — but Arc 13 doesn't include component tests)
  },
});
```

`package.json` script:

```json
{
  "scripts": {
    "test": "vitest run",
    "test:watch": "vitest",
    "test:ui": "vitest --ui"
  }
}
```

### 2. Tests for `app/scripts/gen-data.ts`

At minimum:
- A fixture-based test: provide a synthetic role file (or use one of the canonical 12 from `substrate/`), run the parser, verify output shape
- An invariant test: parsed output validates against the Zod schema
- An error-path test: provide malformed input (missing required field, wrong type), verify Zod throws with descriptive error

Use Vitest's `describe` + `it` + `expect` patterns. Keep tests focused — Arc 13 is about scaffolding, not exhaustive coverage. Coverage expansion is downstream work.

### 3. Tests for `app/src/data/derive.ts`

At minimum:
- Test `deriveRoleSummary` (or whatever the synthesis helper is named) on representative inputs:
  - Short single-paragraph body → returns the paragraph
  - Multi-paragraph body → returns the first paragraph
  - Empty body → returns reasonable fallback (empty string or placeholder)

### 4. Generated-data shape invariant test

A test that imports `app/src/data/generated/agents.ts` and asserts:
- `stoaData.ranks` (or whatever the structure is) has exactly 5 entries
- HUMAN slot has 1 human (or whatever; depends on Arc 12's choice)
- COLONEL slot is reserved-empty
- MAJOR slot has POLYBIUS + PLINY
- CAPTAIN slot has 10 agents
- LIEUTENANT slot is currently empty (skills not yet authored in substrate)

This is a sanity-check test — verifies the gen-data pipeline produces what we expect. Catches regressions if substrate role files are accidentally deleted or duplicated.

### 5. `stoa--b3f` fix

Modify `app/scripts/gen-data.ts` to remove the timestamp from the generated file's header. Header should still note:
- The file is auto-generated
- The regeneration command (`npm run gen-data`)
- (Optional) Source path

Just no timestamp.

After fix:
- `npm run gen-data` is idempotent in the strict sense (same input → byte-identical output)
- Verify by running gen-data twice in a row with no substrate changes — git diff should be clean
- Close `stoa--b3f` ticket with verdict

### 6. Smoke test

After all changes:
- `npm test` runs cleanly — all tests pass
- `npm run build` still works (Vitest config doesn't break Vite's production bundle)
- `npm run dev` still works (Vite dev server unaffected)
- `npm run gen-data` is idempotent (no dirty diff after re-run)

---

## Definition of done

- Vitest installed + configured
- Baseline tests authored for gen-data, derive, and generated-data shape invariant
- `npm test` passes cleanly
- `stoa--b3f` resolved (timestamp removed from gen-data; idempotent regeneration verified)
- bw `stoa--*` epic for Arc 13 closed; `stoa--b3f` closed
- Committed + pushed to `the-stoa` main (autonomous-ship per `u--7yg.11`)

---

## Out of scope

- **Component-level tests** — defer to a future arc (probably an "Arc 13.1" or just additive over time as components evolve). Vitest can test React components with `@testing-library/react`, but Arc 13 is scaffolding, not coverage.
- **Sub-project spawning** — Arc 14
- **Modifying types-v2.ts, generated/agents.ts (other than gen-data fix), or substrate role files** — out of scope
- **CI integration** — running tests in GitHub Actions or similar isn't in scope; this is localhost-only deployment posture
- **Coverage expansion** — Arc 13 ships baseline; future arcs add more tests

---

## Voice discipline

Less load-bearing here (test code + script tweak). Tests should:
- Use v2 vocabulary in test names (`describe('the v2 rank ladder', ...)`, `it('renders the COLONEL slot as reserved', ...)`)
- Comments use v2 voice
- `grep -i "colonel" app/scripts app/src/data/__tests__` (or wherever tests live) — any matches deliberate (rank label, COLONEL slot test names)

---

## Beadwork

`bw` initialized (`stoa-` prefix). File a new epic:

```bash
cd ~/claude_projects/the-stoa
bw create "[EPIC] Arc 13 — Vitest scaffold + stoa--b3f cleanup" -t epic -p 1
```

Wire `stoa--b3f` as a child of this epic (or re-parent):

```bash
bw update stoa--b3f --parent <epic-id>
```

File children for: Vitest install + config, gen-data tests, derive tests, shape-invariant test, stoa--b3f fix, smoke test pass. Close as you go.

---

## Discipline

- HITL default (planning v2 §7)
- Principal-as-router (`u--7yg.1`) — surface only project-direction calls (unlikely to have any in Arc 13)
- Verify-then-execute (`u--7yg.10`, `u--7yg.18`)
- One job per agent (`u--7yg.17`) — your one job is Arc 13; resist scope creep into component tests or coverage expansion
- Wait-for-quiescence (`u--7yg.15`)
- Autonomous-ship on clean PASS (`u--7yg.11`)
- Voice discipline (planning v2 §6)

**Special concern: don't break existing dev/build.** Vitest config in vite.config.ts can interact with Vite's existing config in subtle ways. Smoke test verifies `npm run dev` and `npm run build` still work post-Vitest setup.

---

## Operating mode

**Human-in-the-loop** (planning v2 §7). Surface for input at:
- (a) Test design choices that aren't obvious (probably none for Arc 13's baseline scope)
- (b) `stoa--b3f` decision if you want to discuss preferred-path vs alternative-fingerprint
- (c) Work product ready for review (optional — autonomous push for clean self-validation)
- (d) Done

For Arc 13: this is mechanical work with established tooling (Vitest is well-documented). Autonomous push is the expected default unless you hit something genuinely surprising.

---

## How to surface back

Either:
- Comment on a beadwork ticket in this repo (`stoa--*`)
- Write a short hand-back report; PRINCIPAL will relay

Standby, run.
