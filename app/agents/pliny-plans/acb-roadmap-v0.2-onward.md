# acb roadmap — v0.2 onward

**Author:** Denson Smith (Colonel) via Major Pliny.
**Status:** Living doc. 2026-05-01.
**Predecessors:** `agents/design/onboarding-v1/inventory.md` §5 (the initial three-batch v0.2 plan, partially superseded here).

---

## Three-layer vision

The Stoa is one product surface across three layers:

1. **Web app** — `localhost:5173` (later: deploy target). Visual character builder. Browse the canonical 12-officer roster, drill into officer detail, see required reading + callable lieutenants + meta-aspects. The "what is this team" surface.

2. **In-app tutorial** — overlay or guided content that teaches users HOW to design new agents. Not docs; an interactive walkthrough that uses real app state ("open the officer detail for MAJOR_PLINY; here's why the model tier is opus; now try editing it"). Lives inside the web app.

3. **Claude Code skill — `agent-design-tutor`** — packages the design flow as a callable thing inside Claude Code. When a user inside Claude Code wants to design a new agent for their project, the skill walks them through the same conceptual flow the in-app tutorial teaches, but via Claude conversation. With Chrome MCP available, the skill can drive the web app via the testid + `STOA_STATE` affordances.

The three layers share data (the StoaData adapter from acb-002) and share a conceptual flow (the agent-design ladder: archetype → rank → required reading → callable lieutenants → meta-aspects).

---

## Phase 0 — Foundation

**Status:** queued; dispatching next.

| Arc | Subject | Pipeline | Notes |
|---|---|---|---|
| **acb-002** | gen-data + adapter + Vitest scaffold | full pipeline | Reads `agent-team-team/definitions/`, applies field-name remap, composes `StoaData`, emits build artifact. App.tsx switches from `SAMPLE_DATA` to async fetch. First Vitest test green. |

**Why this is Phase 0:** every later arc assumes real data flowing from `agent-team-team`'s `definitions/`. Until the adapter exists, every arc that would touch data shape is gated.

**Composes with:**
- `acb-002-followup-archetypes-dedup` (filed) — `data.archetypes` cleanup. Falls out of acb-002's data-layer work for free.

**Definition of done:**
- Adapter reads `agent-team-team/definitions/`, applies field-name remap, composes StoaData.
- App.tsx switches from `SAMPLE_DATA` to async fetch with loading state + error boundary.
- First Vitest test green (adapter fixture round-trip).
- Existing UI behavior unchanged.

---

## Phase 1 — Vertical slice: "design a new pair-programmer Major"

**Goal:** end-to-end flow for ONE concrete agent-design scenario. Not a generic builder — a specific demo flow that exercises every layer of the three-layer vision.

**The flow:**
1. User opens the web app (or invokes the Claude Code skill).
2. User clicks "design a new agent" (UI affordance new in acb-004).
3. Edit form (acb-004) collects archetype, rank, required reading, callable lieutenants, meta-aspects.
4. View JSON modal (acb-003) shows the spec being assembled.
5. In-app tutorial (acb-006) annotates each field with WHY ("model tier opus because pair-programming requires multi-file synthesis").
6. Claude Code skill (acb-007) packages the same flow for use inside Claude Code, with optional Chrome MCP drive of the web app.

### Phase 1 prerequisites (briefs filed, sequence into Phase 1)

| Arc | Subject | Pipeline | Sequence | Notes |
|---|---|---|---|---|
| **acb-NNN-skill-affordances** | testid attrs + window.STOA_STATE bridge | build-only | **before acb-007 (hard)** | ~1hr ADA-direct. No design needed. Brief: `agents/follow-ups/acb-NNN-skill-affordances.md`. |
| **acb-NNN-router-url-state** | react-router + URL state for tab/selected/roster/archetypeFilter | full pipeline | **early** (acb-006/007 both want deterministic navigation) | Composes with acb-002 (both touch App.tsx state plumbing). Brief: `agents/follow-ups/acb-NNN-router-url-state.md`. |

### Phase 1 arcs

| Arc | Subject | Pipeline | Notes |
|---|---|---|---|
| **acb-003** | View JSON modal | full pipeline | Picks up `acb-NNN-modal-overlay-token` opportunistically (modal-rendering territory). |
| **acb-004** | Edit form for new-agent design | full pipeline | Edit form layer that backs the View JSON modal. |
| **acb-005** | a11y pass (divs-as-buttons, semantic landmarks, focus management, aria-live for palette) | full pipeline | Standalone mechanical refactor pass; lands after acb-004 (Edit form) so acb-006's tutorial content sits on an a11y-correct foundation. Resolves the deferred-from-acb-001 a11y commitment (acb-001 spec §4). ARGUS+ADA scope, no big design. |
| **acb-006** | In-app tutorial content for the pair-programmer Major flow | full pipeline | Walkthrough UI + content. |
| **acb-007** | `agent-design-tutor` Claude Code skill | full pipeline | Packages the flow for Claude Code consumption. **Open: which pair-programmer Major?** Colonel's nominee: a project-specific pair-programmer (`RUSTACEAN`, `GO_GOPHER`, or similar). DAEDALUS picks when acb-007 dispatches — concrete, demo-friendly, doesn't collide with the canonical 12-officer roster. |

### Suggested sequence

1. **acb-NNN-skill-affordances** (build-only; lands fast; unblocks downstream).
2. **acb-NNN-router-url-state** (full pipeline; bundle with acb-002 if DAEDALUS prefers).
3. **acb-003** (View JSON modal).
4. **acb-004** (Edit form).
5. **acb-005** (a11y pass — lands after acb-004 so acb-006 tutorial content inherits a11y-correct foundation).
6. **acb-006** (in-app tutorial content).
7. **acb-007** (agent-design-tutor Claude Code skill).

DAEDALUS may reorder if dependencies suggest: e.g., router-url-state could land before or after acb-002, and acb-003/004 may bundle into one arc.

---

## Phase 2 — Scale-out

**Status:** placeholder. Direction-only; arcs not committed.

Tentative scope (expand as Phase 1 lands):
- More agent-design flows beyond pair-programmer Major (specialist Lieutenants, full team scaffolds).
- Multi-roster comparison view.
- Skill packaging for non-Claude-Code surfaces (Cursor? CLI?).
- Public deploy target (move off localhost).

---

## Open follow-ups (queued; not in any phase yet)

| Ticket | Plan | Resolution path |
|---|---|---|
| `acb-NNN-modal-overlay-token` | rgba modal backdrop → token-driven | Picked up opportunistically by acb-003 (modal territory). |
| `acb-002-followup-archetypes-dedup` | Drop dead `data.archetypes` | Composes with acb-002 (Phase 0). |
| `runtime-agent-tool-not-exposed` | Investigate envelope/runtime tool divergence | Independent; parked. |

---

## Resolved questions

- **2026-05-01 — a11y pass arc number → acb-005.** Resolution: option (a), standalone arc. Rationale per Colonel: a11y is a focused mechanical refactor pass (divs-as-buttons → proper buttons, semantic landmarks, focus management, aria-live for palette). Bundling with acb-006 (tutorial content) mixes work types; parking to Phase 2 risks dropping it. Standalone ticket, ARGUS+ADA scope, no big design. Sequenced after acb-004 (Edit form) so acb-006's tutorial content sits on an a11y-correct foundation.

### Note on stale reference in acb-001 spec

`agents/specs/acb-001-darkmode.md` §4 still references "acb-004" for the deferred a11y pass. That spec text is preserved as the historical record (committed acb-001 spec is not edited post-merge). **This roadmap is the canonical forward-looking source:** the deferred a11y commitment is fulfilled by **acb-005**, not acb-004 (which is now the Edit form arc).

---

## Roadmap revision history

- **2026-05-01** — Initial draft. Phase 0 + Phase 1 vertical slice + Phase 2 placeholder. Two prerequisite briefs filed (skill-affordances, router-url-state). Open question: a11y arc number.
- **2026-05-01** — a11y arc resolved to acb-005, scheduled between acb-004 and acb-006.
