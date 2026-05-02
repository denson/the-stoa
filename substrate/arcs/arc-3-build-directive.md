# Arc 3 build directive

**Audience:** the fresh Claude Code session opened in this repo to build Arc 3 deliverables.
**Authored by:** user-level Chief-of-Staff (POLYBIUS-equivalent) + Colonel (Denson Smith).
**Status:** active directive.
**Builds on:** Arc 1 (commit `8e4aaab`), Arc 2 (commit `987b371`).

**You are MAJOR_PLINY for the agent-substrate Arc 3 engagement.** The user-level Chief-of-Staff (POLYBIUS-equivalent) wrote this directive; you receive it and execute. Per the architecture (`plans/three-role-recursive-architecture.md` §4), MAJOR_PLINY is the orchestrator role — top-level Claude Code session with `Agent` tool, runs structured work, communicates back to POLYBIUS via beadwork or human relay.

Your first action: read `MAJOR_PLINY.md` (this repo, Arc 1 deliverable) and assume the orchestrator role. The role file is universal; the directive below is your session-specific intent.

**Your one job for this engagement:** author the 10 CAPTAIN envelope files that the team relies on. Then return cleanly. The work is straightforward but substantial — 10 envelopes, each substantively content. The orchestrator-role framing is correct because POLYBIUS wrote this directive, even though the work doesn't require dispatching CAPTAINs (you're authoring them; they don't exist yet).

---

## Read first

1. **`MAJOR_PLINY.md`** in this repo — read this first to assume the orchestrator role.

2. **Arc 1 and Arc 2 outputs in this repo:**
   - `MAJOR_POLYBIUS.md` — references these CAPTAINs in the onboarding flow
   - `install.sh` — you'll extend it to deploy CAPTAIN files at install time
   - `templates/` — the templates Arc 2 produced; CAPTAIN authoring may inform new templates
   - `ONBOARDING.md` — references the team in scenarios

3. **Architecture spec — primary source of truth:**
   - **§9 (Roster)** — defines each CAPTAIN's mnemonic + role + what they do. This is the spec for what each envelope should encode.
   - **§3 (Naming convention)** — `RANK_MNEMONIC.md` at user-tier; install.sh adds `_<project>` suffix at project-tier deploy.
   - **§2 (The four ranks)** — CAPTAINs are sub-agents in `.claude/agents/`. No `Agent` tool. Standard sub-agent toolset.
   - **§7 (Operating modes)** — CAPTAINs run inside HITL-or-autonomous arcs orchestrated by MAJOR_PLINY.

4. **Reference material — read for guidance, do not copy:**
   - Existing deployed envelopes at `~/claude_projects/agent-team-team/.claude/agents/` (`DAEDALUS_agent_team_team.md`, `ARGUS_agent_team_team.md`, etc.). These were authored for a slightly different paradigm (sub-agent dispatcher MAJOR_PLINY) but most of the CAPTAIN-tier envelopes are substantively correct in spirit.
   - **NOTE:** these are reference, not source. Author fresh canonical files in agent-substrate. Reasons:
     - Role-name reassignments under the new architecture (see below)
     - Unsuffixed naming at source-of-truth (`install.sh` adds suffix at deploy time)
     - Architecture has refined since those were authored (one-job-per-agent, etc.)
     - Some bodies reference NESTOR-as-dispatcher, which is wrong now (NESTOR retired; MAJOR_PLINY is the dispatcher seat)

5. **Skim `u--7yg` design inputs**, especially:
   - `u--7yg.17` (one-job-per-agent — important for keeping each CAPTAIN's role narrow and distinct)
   - `u--7yg.16` (envelope tool-set gaps — make sure each CAPTAIN's claimed responsibilities match its actual tool access)
   - `u--7yg.19` (MAJOR_PLINY framing — applies to you for this engagement)

---

## Role-name reassignments under the new architecture

These are NEW relative to the existing agent-team-team deploys. Apply during authoring:

| Mnemonic | OLD role (in existing deploys) | NEW role (per planning doc §9) |
|---|---|---|
| SCOUT | internal codebase reconnaissance | **external/web search and research** |
| BARTLEBY | (didn't exist) | **internal repo recon and search** (NEW; replaces SCOUT's old job) |
| STRABO | external/web research | **kept as a SCOUT** mnemonic — STRABO is the named external researcher |
| NESTOR | sub-agent dispatcher | **retired** — do not author; the role moves to MAJOR_PLINY |

So Arc 3 produces: STRABO and BARTLEBY as separate CAPTAINs (both "search" but different scope); NESTOR is not authored.

---

## Deliverables

### 10 CAPTAIN envelope files in `agent-substrate/` root

| File | Mnemonic | Role | What they do (one-job-per-agent) |
|---|---|---|---|
| `CAPTAIN_DAEDALUS.md` | DAEDALUS | ARCHITECT | writes design specs from briefs |
| `CAPTAIN_ARGUS.md` | ARGUS | PLAN-CRITIC | cold-audits designs; surfaces risks; **does not propose fixes** |
| `CAPTAIN_ADA.md` | ADA | EXECUTOR | builds — code, file edits, scripted work |
| `CAPTAIN_VERA.md` | VERA | VERIFIER | verifies built deliverables against spec |
| `CAPTAIN_CATO.md` | CATO | REVIEWER | reviews diffs for craft, hygiene, consistency |
| `CAPTAIN_STRABO.md` | STRABO | SCOUT | external/web search and research |
| `CAPTAIN_BARTLEBY.md` | BARTLEBY | FILE_CLERK | internal repo recon and search |
| `CAPTAIN_HERALD.md` | HERALD | INTAKE | files briefs in canonical shape; draft-and-route |
| `CAPTAIN_CURATOR.md` | CURATOR | SYNTHESIST | cross-ticket synthesis; retrospectives |
| `CAPTAIN_PLINY.md` | PLINY | SPEC-CHECKER | embedded mechanical spec check; **distinct from MAJOR_PLINY** orchestrator (per `u--7yg.17`) |

### Each envelope must contain

- Clear role identity statement (rank, mnemonic, descriptive role)
- The agent's ONE job (per `u--7yg.17`)
- Toolset assumed available (Bash, Read, Write, Edit, Grep, Glob, WebSearch, WebFetch — no Agent for CAPTAINs)
- Inputs the agent expects (brief shape, where to read from)
- Outputs the agent produces (artifact shape, where to write to)
- How the agent communicates back (verdict format, beadwork comment shape, return-payload structure)
- Disciplines specific to this seat (e.g., ARGUS surfaces risks but doesn't propose fixes; ADA doesn't verify; etc.)
- Voice: workmanlike, role-specific. Each CAPTAIN has a personality consistent with its mnemonic + role.

### `install.sh` extension

- Add a step to deploy CAPTAIN_*.md files from agent-substrate to `<target>/.claude/agents/CAPTAIN_*_<project>.md` (with `_<project>` suffix at project-tier; unsuffixed at user-tier per `u--7yg.13`)
- New flag (suggested): `--with-captains` (default true at install time? or opt-in?). MAJOR_PLINY's call.
- Test deployment via dry-run + real install on throwaway dir; verify CAPTAINs land at the right path with the right names
- Idempotency: re-running installer should not duplicate envelopes

### `README.md` update

- Mention the 10-CAPTAIN roster
- Brief description of what each CAPTAIN does (link to the file)
- Note that `install.sh` deploys them at install time

---

## Definition of done

- All 10 `CAPTAIN_*.md` files committed to `main` branch
- Each envelope is well-formed; a fresh sub-agent dispatched against it could read it and execute its role
- `install.sh` extended; tested in dry-run and real-install modes; deploys CAPTAINs correctly
- `README.md` updated with roster
- bw epic closed; children all closed
- Self-validate: pick one CAPTAIN (e.g., DAEDALUS) and dry-run its role mentally — if a sub-agent had only this file as guidance, could it write a competent design spec from a brief? If not, the envelope needs more work.

---

## Out of scope

- **Arc 4** (refactoring `agent-team-team` and `agent-character-builder`'s wrong-shape deploys) — separate arc; happens after Arc 3 produces canonical envelopes
- **Arc 5** (sub-project spawning mechanism) — separate arc
- **Arc 6** (officer body refresh sweep) — separate arc; some refresh happens naturally during Arc 3 authoring (especially for SCOUT/BARTLEBY role-reassignments) but the broader hygiene sweep is later
- Modifying existing envelopes in `agent-team-team` — leave them; Arc 4 handles those
- Authoring NESTOR — retired
- LIEUTENANT skill files — keep existing names; not in scope for this arc

---

## Beadwork

`bw` is already initialized in this repo (`as-` prefix from Arc 1). File a new epic for Arc 3:

```
bw create "[EPIC] Arc 3 — author 10 CAPTAIN envelope files" -t epic -p 1
```

File children: one per envelope (10) + one for `install.sh` extension + one for `README.md` update + one for testing pass. Close them as you go. Push beadwork branch when done.

If you find any contradictions between this directive and the architecture spec, surface them rather than picking silently. `u--7yg.18` documented this discipline catching a real directive-author error in Arc 1.

---

## Discipline

Same disciplines as Arc 1 + Arc 2:

- **HITL default** — Colonel supervising via user-tier CoS in Claude Desktop
- **Colonel-as-router** (`u--7yg.1`) — surface only project-direction calls; technical-tier decisions stay with you
- **Verify-then-execute** (`u--7yg.10`, `u--7yg.18`) — directive vs spec contradictions get surfaced, not silently picked
- **Second-guess → detection** (`u--7yg.2`)
- **One job per agent** (`u--7yg.17`) — applies twice here: (a) your one job is Arc 3; don't pre-empt Arcs 4-6, AND (b) each CAPTAIN you author has one job — make sure each envelope reflects this
- **Wait-for-quiescence** (`u--7yg.15`) — if the role definition for any CAPTAIN turns out to be ambiguous in the spec, surface it; don't guess

---

## Suggested phasing (technical-tier, your call)

10 envelopes is substantial. A reasonable phasing:

- **Phase A:** Author 2-3 envelopes (suggest DAEDALUS + ARGUS + ADA — the design pipeline core). Run a self-validation pass on the pattern. Surface to Colonel if you want pattern-validation review before grinding through the remaining 7.
- **Phase B:** Author the remaining envelopes.
- **Phase C:** Update `install.sh` + README + run testing pass + commit.

This is a recommendation, not a requirement. If you'd rather author all 10 in one pass and validate at the end, that's fine.

---

## Operating mode

**Human-in-the-loop** (per planning doc §7 — HITL is default for new work). Surface for input at:
- (a) ambiguity that needs Colonel input
- (b) work product ready for Colonel review before commit
- (c) done

---

## How to surface back

Either:
- Comment on a beadwork ticket in this repo (`as--*`); user-tier CoS has visibility per `u--7yg.14`
- Write a short hand-back report; Colonel will relay

Standby, run.
