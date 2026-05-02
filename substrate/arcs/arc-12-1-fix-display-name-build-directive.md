# Arc 12.1 build directive — fix agent display name to use mnemonic only

**Audience:** the fresh Claude Code session opened to build Arc 12.1 deliverables.
**Authored by:** user-tier Chief-of-Staff (POLYBIUS-equivalent) + the PRINCIPAL (Denson Smith).
**Status:** active directive; small fix-up arc following Arc 12.
**Builds on:** Arc 12 (commit `15d7a46`).

**You are MAJOR_PLINY for the the-stoa Arc 12.1 engagement.** Read `substrate/MAJOR_PLINY.md` and assume the orchestrator role. Open Claude Code in `~/claude_projects/the-stoa/`.

**Your one job:** fix the agent display name to render only the mnemonic (e.g., "PLINY", "POLYBIUS", "DAEDALUS"), not the rank-prefixed filename stem (e.g., "MAJOR_PLINY"). The rank pill already conveys the rank — the prefix in the display name is redundant.

This is small. Probably 5-15 lines of component changes + smoke verification.

---

## What needs to change

PRINCIPAL eyeballed the running app at `localhost:5181/#/agent/MAJOR_PLINY` post-Arc-12 ship. The detail-page heading rendered `MAJOR_PLINY` directly under a `MAJOR` rank pill. Same redundancy on the agent cards in Team view.

Fix: components display `agent.mnemonic` (e.g., `PLINY`) instead of the rank-prefixed filename stem.

This applies to:
- Detail page heading
- Agent cards in Team / Major / Captain rank-section views
- Possibly the command palette result rows
- Anywhere else the rank-prefixed name is rendered

The rank pill stays where it is — that's the right place to communicate rank.

---

## Read first

1. **`app/src/data/types-v2.ts`** — confirm the `Agent.mnemonic` field exists and contains just the mnemonic (no rank prefix). If it doesn't (e.g., gen-data populates mnemonic with the full filename stem), the fix shifts upstream to gen-data and types-v2 — surface that finding before proceeding.
2. **`app/src/data/generated/agents.ts`** — verify what `mnemonic` actually contains in the generated data (should be `"PLINY"`, `"POLYBIUS"`, `"DAEDALUS"`, etc.; NOT `"MAJOR_PLINY"`).
3. **The components rendering agent names** — `app/src/App.tsx` and `app/src/Components.tsx` (or wherever the agent card / detail view live). Search for whatever field is currently being rendered (`filename`, `name`, etc.) and replace with `mnemonic`.

---

## Deliverables

### 1. Verify the data model has what we need

Check that `Agent.mnemonic` contains the bare mnemonic (e.g., `"PLINY"`). If gen-data is currently populating mnemonic with the filename stem (`"MAJOR_PLINY"`), surface to PRINCIPAL — that's a gen-data fix in `app/scripts/gen-data.ts` to derive the mnemonic correctly from the filename.

### 2. Update components to render `agent.mnemonic`

Find every place where the rank-prefixed name is currently displayed and swap to mnemonic:
- Detail page heading
- Agent cards in rank sections
- Command palette result text
- Any tooltips, breadcrumbs, etc. that show the agent's name

The route URL (`/agent/MAJOR_PLINY`) can stay rank-prefixed — that's a slug, not a display name. (Or if you'd rather harmonize routes too, surface it; not required for this arc.)

### 3. Smoke test

After the fix:
- `npm run build` — TypeScript clean
- `npm run dev` — starts cleanly
- Navigate to `/#/agent/MAJOR_PLINY` (or whatever the route slug is) — verify the detail heading shows `PLINY` under the `MAJOR` pill, not `MAJOR_PLINY`
- Browse Team view — verify agent cards show mnemonics (PLINY, POLYBIUS, DAEDALUS, ARGUS, ADA, VERA, CATO, STRABO, BARTLEBY, HERALD, CURATOR, PLINY)
- Note: PLINY appears twice (CAPTAIN_PLINY the spec-checker + MAJOR_PLINY the orchestrator). The rank pill differentiates them. Verify both display as just `PLINY` with their respective rank pills.

---

## Definition of done

- Display rendering uses `agent.mnemonic` everywhere agent names appear
- Both `MAJOR PLINY` and `CAPTAIN PLINY` render correctly (different ranks, same mnemonic — pills differentiate)
- TypeScript compiles cleanly
- Smoke verification on dev server passes
- bw `stoa--*` ticket for this fix closed
- Committed + pushed to `the-stoa` main (autonomous-ship per `u--7yg.11`)

---

## Out of scope

- **Route URL slug changes** — leave `/agent/MAJOR_PLINY` as is unless you have a specific reason to change; surface if you want to discuss
- **Anything else from Arc 13** (Vitest scaffold + stoa--b3f) — separate arc
- **gen-data adapter changes** — UNLESS the Agent.mnemonic field doesn't have what we need; then it's in scope for this fix-up

---

## Beadwork

```bash
cd ~/claude_projects/the-stoa
bw create "Fix agent display name to use mnemonic only (rank pill already conveys rank)" -t bug -p 2
```

Single ticket; close on ship.

---

## Discipline

Standard:
- HITL default
- Autonomous-ship on clean PASS (`u--7yg.11`) — push when smoke verifies
- Verify-then-execute — check the data model before changing components
- One job per agent — your one job is this fix; don't bundle Arc 13 work

Standby, run.
