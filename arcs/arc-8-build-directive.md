# Arc 8 build directive

**Audience:** the fresh Claude Code session opened in this repo to build Arc 8 deliverables.
**Authored by:** user-tier Chief-of-Staff (POLYBIUS-equivalent) + the PRINCIPAL (Denson Smith).
**Status:** active directive.
**Builds on:** Arcs 4-7 (substrate-redesign-from-v2 + install.sh improvements complete).

**You are MAJOR_PLINY for the agent-substrate Arc 8 engagement.** Read `MAJOR_PLINY.md` (this repo, Arc 4's v2-shape file) and assume the orchestrator role.

**Your one job for this engagement:** propagate the v2-aligned substrate to two existing projects (`agent-team-team` and `agent-character-builder`) by removing v1-shape deploys and running the now-functional install.sh. Then verify each project's existing work still functions. Then return cleanly.

**Structural difference from Arcs 4-7:** this arc operates on TWO OTHER REPOS, not on agent-substrate itself. Higher risk surface — existing project work has to keep functioning after the refactor. Take more care than the in-repo arcs.

---

## Read first

1. **`install.sh` in this repo** — the now-functional v2 installer (Arc 7 just shipped). Read its current behavior + flag interface to know what you'll invoke.

2. **`plans/three-role-recursive-architecture.md` in user-beadwork — v2 spec.** Specifically §14 Arc 8 paragraph (your scope) + §11 The Stoa (note: The Stoa data-model updates are Arc 9, not Arc 8 — keep scoped).

3. **The two target projects, current state:**
   - `~/claude_projects/agent-team-team/.claude/agents/` — 12 deployed v1-shape envelopes (including wrong-shape `MAJOR_PLINY_agent_team_team.md` sub-agent that conflates orchestrator with sub-agent)
   - `~/claude_projects/agent-team-team/CLAUDE.md` — current state unknown; may have project-specific content beyond any substrate reference
   - `~/claude_projects/agent-character-builder/.claude/agents/` — 12 deployed v1-shape envelopes; same wrong-shape MAJOR_PLINY issue
   - `~/claude_projects/agent-character-builder/CLAUDE.md` — current state unknown; **acb-009 work is recent (router-url-state); the React app must continue functioning**

4. **`u--7yg` design inputs:**
   - `u--7yg.12` (sub-agents can't dispatch — the structural reason MAJOR_PLINY-as-sub-agent was wrong-shape)
   - `u--7yg.20` (terminology fix that motivated v2)

---

## What Arc 8 is

Two existing project deploys carry v1 shape:
- **MAJOR_PLINY deployed as sub-agent envelope** — wrong-category. PLINY is meant to be a top-level paste-activated role, not a `.claude/agents/` sub-agent.
- **CAPTAIN envelopes use v1 vocabulary** (Colonel-as-human leakage)
- **SCOUT/BARTLEBY role-name reassignments not applied** — old SCOUT-as-internal still in deploy

Arc 8 propagates Arcs 4-7's canonical work to both projects: fresh deploy of v2 substrate via install.sh.

---

## Deliverables

### 1. Pre-flight inspection (per project)

For each of `agent-team-team` and `agent-character-builder`:

```bash
cd <project-dir>
ls -la .claude/                          # what's there
ls -la .claude/agents/                   # current envelope state
cat CLAUDE.md                            # what's the current CLAUDE.md content
git status                               # any uncommitted work?
```

**Surface any unexpected state to PRINCIPAL before proceeding.** Examples:
- CLAUDE.md has substantial project-specific content beyond a substrate reference (may need careful merge, not append-and-overwrite)
- Uncommitted work in the project (don't refactor on top of dirty working tree)
- Custom envelope modifications beyond the v1 deploy (PRINCIPAL may have hand-edited something)

If pre-flight is clean for a project, proceed to refactor. If not clean, surface and wait.

### 2. Refactor each project (per project)

Per project, in this order:
1. Move existing `.claude/agents/` to `.claude/agents.v1-archive/` (preserve as historical reference, don't delete outright)
2. Run agent-substrate's install.sh against the project:
   ```bash
   ~/claude_projects/agent-substrate/install.sh \
       --target project \
       --project-dir ~/claude_projects/<project> \
       --modify-claude-md
   ```
3. Verify install completed cleanly + next-step guidance printed
4. Inspect resulting `.claude/` — should have v2-shape MAJOR_POLYBIUS.md, MAJOR_PLINY.md, agents/CAPTAIN_*_<project>.md, templates/

### 3. CLAUDE.md merge handling

install.sh appends a POLYBIUS reference to CLAUDE.md (with `--modify-claude-md` flag). If the project's CLAUDE.md already has substantive content:
- Leave existing content intact
- Append the POLYBIUS reference at the end (install.sh does this idempotently — re-appending the same block is a no-op)
- Verify the merged CLAUDE.md still reads correctly

If install.sh's append seems to conflict with existing content, **surface to PRINCIPAL — don't auto-merge.** A CLAUDE.md is the project's auto-load file; getting it wrong has runtime consequences.

### 4. Verification per project

**agent-team-team:**
- Check that `.claude/agents/` shows 10 CAPTAINs + 0 wrong-shape MAJOR_PLINY sub-agent
- Check that `MAJOR_POLYBIUS.md` and `MAJOR_PLINY.md` are at the project root .claude/ (not in agents/)
- bw status: existing `att-` beadwork should be intact (don't touch it)
- Smoke test: open Claude Code in the project, say "POLYBIUS" — verify auto-load works against fresh deploy

**agent-character-builder:**
- All the above checks
- Plus: **The React app must still function.** Run `npm run dev` or similar; verify the app starts; verify the existing pages render; verify acb-009's router-url-state still works.
- bw status: existing `acb-` beadwork intact
- The app's data layer hasn't been wired to read from agent-substrate yet (that's Arc 9). It still reads from inline sample.ts. So the app's display won't change — verifying it still WORKS is the bar, not that it shows new data.

### 5. Archive cleanup decision

After verification, the moved `.claude/agents.v1-archive/` directories can either:
- (a) Stay as historical reference in the project — discoverable for anyone wondering what was there before
- (b) Be removed since canonical is in agent-substrate

Build session decides — both are defensible. PRINCIPAL leans toward (a) for the first refactor (agent-team-team) so we have evidence if something breaks; (b) is fine for agent-character-builder if pre-flight + verification both pass cleanly.

### 6. Per-project commits

Each project gets its own commit on its own main branch:
- `agent-team-team`: commit message like "refactor: deploy v2 substrate; retire wrong-shape MAJOR_PLINY sub-agent (per agent-substrate Arc 8)"
- `agent-character-builder`: similar

Push each project's commit to its own origin/main.

### 7. Arc 8 closing in agent-substrate beadwork

Arc 8 doesn't produce new files in agent-substrate itself. The arc's beadwork ticket (in agent-substrate) records the cross-project propagation for the audit trail. File:

```
bw create "[EPIC] Arc 8 — propagate v2 substrate to agent-team-team + agent-character-builder" -t epic -p 1
```

Children: pre-flight (2 — one per project), refactor (2), verification (2), per-project commits (2). Close as you go.

---

## Definition of done

- Both projects have v2-shape substrate deployed
- Both projects have wrong-shape `MAJOR_PLINY_<project>.md` sub-agent retired
- Both projects' CLAUDE.md cleanly references the deployed POLYBIUS
- Both projects' existing work still functions (smoke tests pass)
- Each project committed + pushed to its own origin
- agent-substrate Arc 8 epic closed
- All committed to agent-substrate `main` (just the directive close + epic) and pushed

---

## Out of scope

- **The Stoa data-model + display alignment** — Arc 9. Don't touch agent-character-builder's `src/` (the React app code) in this arc.
- **Sub-project spawning** — Arc 10
- **Re-authoring substrate** — Arcs 4-6 already shipped them
- **agent-team-team's `definitions/`** — leave intact; that's separate from `.claude/agents/` and is its own substrate concern
- **Beadwork in target projects** — `att-` and `acb-` tickets stay as they are; this arc doesn't touch them

---

## Beadwork

`bw` is initialized in this repo (`as-` prefix). Epic per above. In each target project, do NOT init new bw — use existing.

---

## Discipline

Same as Arcs 4-7, plus extra care for cross-repo work:

- HITL default (v2 §7) — supervising via user-tier CoS in Claude Desktop. **More frequent surfacing for this arc** because the work touches PRINCIPAL's existing project repos
- Principal-as-router (`u--7yg.1`)
- Verify-then-execute (`u--7yg.10`, `u--7yg.18`) — cross-repo work has more places things can be wrong; lean into the discipline
- One job per agent (`u--7yg.17`)
- Wait-for-quiescence (`u--7yg.15`)
- Autonomous-ship on clean PASS (`u--7yg.11`) — applies, but the per-project CLAUDE.md modification merits explicit verification before commit

**Special concern: don't break existing project work.** acb-009 and acb-001 work shipped recently in agent-character-builder. The React app must keep working. Do the smoke test before committing to that project's main.

---

## Operating mode

**Human-in-the-loop** (v2 §7). Surface for input at:
- Pre-flight surfaces (any unexpected state in either project)
- CLAUDE.md merge concerns (substantive existing content)
- After verification — confirm before commit, especially for agent-character-builder where the app must still function
- Done

For Arc 8 specifically: this is the most cross-repo-careful arc so far. Default to MORE surfacing, not less.

---

## How to surface back

Either:
- Comment on a beadwork ticket in this repo (`as--*`)
- Write a short hand-back report; PRINCIPAL will relay

For Arc 8: hand-back reports are probably more useful than ticket comments because the cross-project state has to be communicated coherently.

Standby, run.
