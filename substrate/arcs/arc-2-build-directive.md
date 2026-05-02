# Arc 2 build directive

**Audience:** the fresh Claude Code session opened in this repo to build Arc 2 deliverables.
**Authored by:** user-level Chief-of-Staff + Colonel (Denson Smith).
**Status:** active directive.
**Builds on:** Arc 1 (commit `8e4aaab` — `MAJOR_POLYBIUS.md`, `MAJOR_PLINY.md`, `install.sh`).

You are the Arc 2 build session for agent-substrate. One focused job: build POLYBIUS's interactive onboarding flow. Then return cleanly.

---

## Read first

1. **Arc 1 outputs in this repo:**
   - `MAJOR_POLYBIUS.md` (the role file you'll be extending)
   - `MAJOR_PLINY.md` (the orchestrator role; POLYBIUS hands off to it)
   - `install.sh` (the mechanical deploy script POLYBIUS calls during onboarding)
   - `arcs/arc-1-build-directive.md` (what Arc 1 built; useful context)

2. **Architecture spec — primary source of truth:**
   https://github.com/denson/user-beadwork/blob/main/plans/three-role-recursive-architecture.md
   
   Read in full: §8 (onboarding flow — your core spec for this arc), §10.1 (custom paste-instruction templating), §4 (MAJOR_POLYBIUS responsibilities), §3 (naming convention — make sure your filenames match the spec, including the rank prefix on `MAJOR_*.md`), §6 (communication channels POLYBIUS uses with MAJOR_PLINY).

3. **Skim** `u--7yg.13`, `u--7yg.18`, and Arc 1's `as--unw` epic + closing comments. The `u--7yg.18` observation specifically demonstrated verify-then-execute working when a build session caught a directive-spec contradiction; you may run into similar situations.

---

## What Arc 2 is

Per planning doc §12: build the interactive onboarding flow that lives inside POLYBIUS. When a fresh user prompts POLYBIUS (or POLYBIUS auto-loads via a project's `CLAUDE.md` reference), POLYBIUS walks the user through setting up the team — interview, install, `bw init`, paste-instruction handoff to MAJOR_PLINY.

Arc 1 shipped the role-file scaffolding. Arc 2 ships the flow that lives inside it.

---

## Deliverables

### 1. Extended `MAJOR_POLYBIUS.md`

Extend the existing role file with a clear, executable-by-a-fresh-Claude-session procedure for onboarding. After Arc 2, a fresh Claude Code session reading `MAJOR_POLYBIUS.md` should know exactly how to:

- Greet a new user appropriately (one-time-first-meeting tone)
- Interview the user about intent + scope (what project, what kind of work, comfort level with user-level CLAUDE.md modification)
- Propose deployment options (project-only, user-level + project-level, sub-projects-only) with the trade-offs explained
- Get informed consent for any user CLAUDE.md modification before doing it
- Run `install.sh` with the right flags based on user choice
- Run `bw init --prefix <project>-` at the appropriate tier
- Hand the user a custom paste-instruction (per §10.1) that activates MAJOR_PLINY with the session's specific intent
- Stand by post-handoff for ad-hoc work, surface back when project-direction calls arise, remind MAJOR_PLINY to re-load its role after compact/clear

Keep the voice consistent with Arc 1's `MAJOR_POLYBIUS.md`. Extend, don't rewrite.

### 2. `templates/` directory

A directory holding artifacts POLYBIUS uses during onboarding:

- **`templates/paste-instruction-template.md`** — the template for the MAJOR_PLINY activation paste, with substitution slots (e.g., `{{PROJECT_NAME}}`, `{{SESSION_INTENT}}`, `{{BW_PREFIX}}`). POLYBIUS fills these per session.
- **`templates/onboarding-questions.md`** — the questions POLYBIUS asks during the interview phase, with rationale for each (so a future POLYBIUS reading the template understands why each question matters).
- **`templates/consent-prompts.md`** — the exact wording POLYBIUS uses when requesting informed consent for sensitive actions (modifying user CLAUDE.md, etc.). Keeps the consent language consistent across deployments.

### 3. `ONBOARDING.md`

An end-to-end walkthrough doc showing what a real onboarding session looks like, narrative-style. Two purposes:
- **Test harness** — POLYBIUS-equipped sessions can read this and run a tabletop rehearsal of the flow
- **Documentation** — humans browsing the repo see exactly what to expect when they open POLYBIUS for the first time

Cover at minimum:
- A first-time user opening MAJOR_POLYBIUS, intent unclear → POLYBIUS interviews, suggests starting small with project-only deploy
- A returning user with prior beadwork → POLYBIUS reads existing state, picks up appropriately
- A user who explicitly wants user-level + project-level → POLYBIUS confirms with informed consent, runs install with `--target user --modify-claude-md`
- The compact-or-clear recovery scenario (POLYBIUS notices MAJOR_PLINY lost its role, re-issues paste-instruction)

---

## Definition of done

- `MAJOR_POLYBIUS.md` extended with the onboarding flow; voice consistent with Arc 1's
- `templates/` directory exists with the three template files; each template has clear substitution syntax + rationale
- `ONBOARDING.md` written; walks through the four scenarios above end-to-end
- A fresh Claude Code session reading `MAJOR_POLYBIUS.md` could plausibly walk a hypothetical user through onboarding without further instruction (validate this by your own dry read)
- `README.md` updated to point at the new templates and ONBOARDING.md
- All committed to `main`; bw beadwork epic closed

---

## Out of scope

- **Authoring the 10 CAPTAIN envelope files** (DAEDALUS, ARGUS, ADA, VERA, CATO, BARTLEBY, STRABO, HERALD, CURATOR, CAPTAIN_PLINY). POLYBIUS knows how to deploy them once they exist; the actual envelope authoring is its own arc (likely Arc 3 in a renumbered sequence; will figure out arc numbering after this).
- **Refactoring `agent-team-team` and `agent-character-builder`'s wrong-shape deploys.** Separate arc.
- **Skill-creation specifics.** POLYBIUS knows it can author skills when needed; the actual skill-authoring workflow is a later arc.
- **Sub-project spawning mechanics.** Separate arc.

---

## Beadwork

`bw` is already initialized in this repo (`as-` prefix from Arc 1). File a new epic for Arc 2:

```
bw create "[EPIC] Arc 2 — POLYBIUS interactive onboarding flow" -t epic -p 1
```

File children for each deliverable. Close them as you go. Push `beadwork` branch when done.

If you find any contradictions between this directive and the architecture spec, surface them rather than picking silently — `u--7yg.18` documented exactly that pattern catching a real directive-author error in Arc 1. Same discipline applies here.

---

## Discipline

Same disciplines as Arc 1:

- **HITL default** — Colonel (via user-tier CoS in Claude Desktop) is supervising. Surface at: ambiguity, before-commit review, done.
- **Colonel-as-router** (`u--7yg.1`) — don't gate Colonel on technical-tier decisions; surface only project-direction calls.
- **Verify-then-execute** (`u--7yg.10`, `u--7yg.18`) — if directive contradicts spec, surface the contradiction; don't silently pick.
- **Second-guess → detection** (`u--7yg.2`) — convert hedges to trip-wires before voicing them.
- **One job per agent** (`u--7yg.17`) — your one job is Arc 2. Don't pre-empt Arcs 3-5.
- **Wait-for-quiescence** (`u--7yg.15`) — if the design intent for any sub-piece is still actively refining mid-build, surface it; don't barrel forward.

---

## How to surface back

Either:
- Comment on a beadwork ticket in this repo (Colonel has visibility per `u--7yg.14`)
- Write a short hand-back report; Colonel will relay

For mid-arc questions: file the question on the relevant `as--*` ticket and ping Colonel by hand-back. For done: hand-back a summary like Arc 1's, listing what landed and any flags worth Colonel awareness.

Standby, run.
