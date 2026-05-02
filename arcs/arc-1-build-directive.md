# Arc 1 build directive

**Audience:** the fresh Claude Code session opened in this repo to build Arc 1 deliverables.
**Authored by:** user-level Chief-of-Staff + Colonel (Denson Smith).
**Status:** active directive.

You are the Arc 1 build session for agent-substrate. One focused job: produce the three deliverables for Arc 1 and return cleanly.

---

## Read first

1. **`README.md`** in this repo — explains what gets deployed and why.

2. **The architecture spec** — primary source of truth:
   https://github.com/denson/user-beadwork/blob/main/plans/three-role-recursive-architecture.md
   
   (or clone user-beadwork locally and read at `~/claude_projects/user-beadwork/plans/three-role-recursive-architecture.md`)
   
   Read sections 2 (the four ranks), 3 (naming), 4 (the two MAJORs), 5 (tiers/sub-projects), 6 (communication), 7 (operating modes — HITL is default, autonomous opt-in), 8 (onboarding flow), 9 (roster), §12 Arc 1 (what you're building).

3. **Skim** user-beadwork epic `u--7yg` + its children for the empirical inputs that produced the architecture. You don't need them all memorized; just know they exist as design rationale if questions arise.

---

## Arc 1 deliverables

Three files, all in this repo (`agent-substrate`):

### 1. `POLYBIUS.md` — the Chief-of-Staff role file

Defines what the seat does, how it operates, what it's responsible for. Per planning doc §4 (MAJOR_POLYBIUS), §8 (onboarding), §6 (communication), §7 (HITL default; must remind orchestrator after compact/clear), §10.1 (custom paste-instruction templating).

**Voice:** scholarly, precise, not chatty. POLYBIUS is the thoughtful coordinator. Reach for the disciplines `u--7yg.1`, `u--7yg.2`, `u--7yg.10`, `u--7yg.11`, `u--7yg.14`, `u--7yg.17` and weave them in.

### 2. `MAJOR_PLINY.md` — the Orchestrator role file

Defines what the seat does. Per planning doc §4 (MAJOR_PLINY), §6 (Agent tool dispatch + beadwork comms), §9 (the team it dispatches).

**Voice:** workmanlike, structured. PLINY runs the gauntlet pipeline.

### 3. `install.sh` — minimal install script

Drops `POLYBIUS.md` and `MAJOR_PLINY.md` to the chosen target (user-tier `~/.claude/` or project-tier `<project>/.claude/`), with informed-consent flag for modifying the user's `CLAUDE.md` to reference `POLYBIUS.md`.

Per planning doc §8: this is the TEMPLATE; POLYBIUS customizes the actual install script per user feedback at run time. Don't try to handle every edge case — just the basic shape.

---

## Definition of done

- All three files committed to this repo's `main` branch
- `README.md` updated to point at the deliverables
- `POLYBIUS.md` and `MAJOR_PLINY.md` are well-formed role definitions a fresh Claude Code session could read and assume the role
- `install.sh` runs cleanly in dry-run mode (validation only, no actual writes); idempotent
- A README section explaining how to test the install (manually, on a throwaway directory)

---

## Out of scope

- **Arc 2** (POLYBIUS interactive onboarding flow) — that's the next arc
- **Arc 3** (refactoring existing wrong-shape deploys in `agent-team-team` and `agent-character-builder`) — separate arc
- **Arc 4-5** — separate arcs
- Don't try to deploy the team CAPTAINs (DAEDALUS/ARGUS/etc.) here; that's Arc 2's interactive deploy

---

## Beadwork

`bw init --prefix as-` in this repo. File an epic for Arc 1 tracking (`as--XX [EPIC] Arc 1 — core deployable`). File children for each of the three deliverables. Close them as you go. Push `beadwork` branch when done.

---

## Discipline

This is a small focused build, not a full gauntlet pipeline. You don't need to dispatch DAEDALUS / ARGUS / VERA / CATO. Write the files directly per the spec, validate each against the planning doc, commit. Total scope ~3 files + a README update.

Apply **Colonel-as-router** (`u--7yg.1`) and **second-guess→detection** (`u--7yg.2`) disciplines while working: don't surface technical-tier decisions to Colonel unless they're genuinely project-direction.

- **Examples of NOT surfacing:** which exact wording in the role file, exact bash syntax in install.sh, formatting choices in markdown
- **Examples of DO surfacing:** a structural ambiguity in the spec that requires Colonel decision; a deliverable that turns out to need more than one arc to land properly; an assumption you discovered was wrong

---

## Operating mode

**Human-in-the-loop** (per planning doc §7 — HITL is default for new work). Colonel (via user-tier Chief-of-Staff in Claude Desktop) is supervising.

Surface for input at:
- (a) ambiguity that needs Colonel input
- (b) work product ready for Colonel review before commit
- (c) done

---

## How to surface back

Either:
- Comment on a beadwork ticket in this repo (`as--*`); user-tier CoS has visibility into project beadworks per `u--7yg.14`
- Write a short hand-back report; Colonel will relay

Standby, run.
