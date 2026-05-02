# Onboarding — what a real session looks like

Narrative walkthroughs of MAJOR_POLYBIUS conducting onboarding. Two purposes:

1. **Test harness** — a Claude Code session that has just adopted the POLYBIUS role can read this file and run a tabletop rehearsal of the flow before live use, catching mismatches between the role file (`MAJOR_POLYBIUS.md`) and the templates (`templates/*.md`).
2. **Documentation** — humans browsing the repo see what to expect when they open POLYBIUS for the first time, before they commit to running anything.

Architecture authority: `user-beadwork/plans/three-role-recursive-architecture.md` (v2). Onboarding flow lives in spec §8; the role's responsibilities live in `MAJOR_POLYBIUS.md` §5.

Five scenarios below cover the common and the load-bearing-rare paths:

| # | Scenario | What's being tested |
|---|---|---|
| 1 | First-time PRINCIPAL, intent unclear, project-only deploy | the conservative path; interview discipline; learning the PRINCIPAL's name |
| 2 | Returning PRINCIPAL with prior beadwork | reading state before asking; refreshing intent |
| 3 | PRINCIPAL who explicitly wants user-tier + project-tier | the higher-stakes consent moment; user-tier `CLAUDE.md` modification |
| 4 | Compact-or-clear recovery — MAJOR_PLINY lost its role | the load-bearing CHIEF-OF-STAFF responsibility (`MAJOR_POLYBIUS.md` §6); on-disk-paste re-activation |
| 5 | Sub-project spawn — design-tier sub-project under The Stoa | the recursive sub-project capability (`MAJOR_POLYBIUS.md` §10); `install.sh --target subproject`; cross-tier handoff to a different human collaborator |

Each scenario shows the dialog and the file/tool actions that go with it. PRINCIPAL lines are in *italics* (and use the human's name once onboarding has learned it); POLYBIUS's lines are in plain text; tool actions are in `code blocks`.

The transcripts are illustrative — actual sessions vary in phrasing. What's stable is the *shape*: the order of operations, the consent points, the artifacts produced.

---

## Scenario 1 — First-time PRINCIPAL, intent unclear, project-only deploy

A PRINCIPAL has just opened a fresh Claude Code session in a project they're considering setting up the substrate for. They have not used this system before. POLYBIUS auto-loaded via the existing `~/.claude/CLAUDE.md` reference (the PRINCIPAL had previously approved that for an earlier project — for this scenario, POLYBIUS is a known seat but the project itself is new).

**PRINCIPAL:** *POLYBIUS, what is this thing?*

**POLYBIUS:** I'm the chief-of-staff seat in a three-role agent substrate. I hold durable memory across sessions, walk you through setup, and write activation instructions for the orchestrator (MAJOR_PLINY) that runs the team. Tell me a bit about what you're working on and I'll get the substrate set up. And before we go further — what should I call you?

**PRINCIPAL:** *Sam. I'm in a directory called `widget-builder`. I want to use this to build out a small UI library. Honestly I'm not sure what I want to do first.*

POLYBIUS captures the name and reads the working directory state before asking questions whose answers are on disk.

```
$ pwd
/home/sam/projects/widget-builder
$ ls -la
.git/
README.md
package.json
$ ls .claude/ 2>&1
ls: .claude/: No such file or directory
$ bw list 2>&1
no issues found
```

**POLYBIUS:** Good to meet you, Sam. Brand-new project, no prior `.claude/` setup, no beadwork. The conservative shape fits well here.

A couple of things to settle before we install:

1. The session intent goes into the paste-instruction that activates MAJOR_PLINY. "I want to use this to build out a small UI library" is fine for a starting frame, but pressing for more: is there a specific first thing you want PLINY to do — design the component API, scaffold the build setup, draft the first component? Or do you genuinely want to start with "orient and recommend"?

**Sam:** *Genuinely "orient and recommend." I haven't decided yet.*

**POLYBIUS:** Good — I'll set that as the session intent. PLINY will start by reading the project state and proposing a first arc rather than diving into specific work.

2. I'd recommend the **project-only** deployment shape for a first install. That drops the role files into `widget-builder/.claude/`, deploys the 10 CAPTAIN sub-agent envelopes to `widget-builder/.claude/agents/` (each suffixed with `_widget_builder`), and optionally appends a small reference block to `widget-builder/CLAUDE.md` so POLYBIUS auto-loads in this directory. It does not touch `~/.claude/CLAUDE.md`. You can promote to the full user-tier + project-tier deployment later if the system proves itself.

**Sam:** *Project-only sounds right. Yes to the CLAUDE.md reference for the project.*

POLYBIUS now runs the install. The flag set is `--target project --project-dir . --modify-claude-md`.

**POLYBIUS:** I'm going to run:

```
./install.sh --target project --project-dir . --modify-claude-md
```

That will: drop `MAJOR_POLYBIUS.md` and `MAJOR_PLINY.md` into `widget-builder/.claude/`, deploy the 10 CAPTAIN envelopes to `widget-builder/.claude/agents/` (suffixed with `_widget_builder`), and append a marker-bounded reference block to `widget-builder/CLAUDE.md`. Anything to adjust before I run it?

**Sam:** *Go ahead.*

```
$ ./install.sh --target project --project-dir . --modify-claude-md
agent-substrate install — plan
  target           : project
  destination dir  : ./.claude
  modify CLAUDE.md : yes (consent flag set)
  deploy CAPTAINs  : yes (10 envelopes to ./.claude/agents)
  CAPTAIN suffix   : _widget_builder (project slug: widget_builder)
  dry-run          : no

cp MAJOR_POLYBIUS.md ./.claude/MAJOR_POLYBIUS.md
cp MAJOR_PLINY.md ./.claude/MAJOR_PLINY.md
deployed: ./.claude/agents/CAPTAIN_DAEDALUS_widget_builder.md
deployed: ./.claude/agents/CAPTAIN_ARGUS_widget_builder.md
... (10 CAPTAINs total)
appended POLYBIUS reference to: ./CLAUDE.md

install.sh: done (applied)
```

**POLYBIUS:** Files in place. Next, I'd like to initialize beadwork — that gives us durable cross-session ticket tracking. I'll run `bw init --prefix wb-` (your project name shortens cleanly to `wb`). Creates a `beadwork` branch and a `.bwconfig` file; doesn't touch `main` or any working files. OK to proceed?

**Sam:** *Yes.*

```
$ bw init --prefix wb-
beadwork initialized — prefix wb-, branch beadwork
```

**POLYBIUS:** Beadwork is up. Now for the activation paste. I'll fill the template (`templates/paste-instruction-template.md`) with your slot values:

- `PROJECT_NAME`: `widget-builder`
- `SESSION_INTENT`: `Orient and recommend a first arc — UI library is not yet scoped.`
- `BW_PREFIX`: `wb`
- `ROLE_FILE_PATH`: `.claude/MAJOR_PLINY.md`
- `PENDING_DIRECTIVES`: (none yet — omit the trailing clause)
- `ON_DISK_PATH`: `HUMAN_paste-orchestrator-instruction.md`

I'll write the filled paste-instruction to `HUMAN_paste-orchestrator-instruction.md` at the project root. That file is the substrate you re-paste from if PLINY's session compacts or `/clear`'s — durable, re-readable, doesn't depend on me being in the loop. The chat paste itself will be one line: `Read HUMAN_paste-orchestrator-instruction.md and execute.` OK?

**Sam:** *Yes.*

POLYBIUS writes the file. Contents:

```
Read .claude/MAJOR_PLINY.md and assume the orchestrator role for widget-builder.

Your immediate intent for this session: Orient and recommend a first arc — UI library is not yet scoped.

Check beadwork (wb-- prefix) for pending directives from MAJOR_POLYBIUS.

If compaction or /clear erases your role, re-read this paste from HUMAN_paste-orchestrator-instruction.md in the project root.
```

**POLYBIUS:** Paste-instruction is at `HUMAN_paste-orchestrator-instruction.md`. To activate PLINY:

1. Open a new terminal in `widget-builder/`.
2. Run `claude`.
3. Paste this one line: `Read HUMAN_paste-orchestrator-instruction.md and execute.`

PLINY will read the on-disk artifact, internalize the intent, and activate as the orchestrator with the right session-specific priming.

Once PLINY is up, I'll stand by from this seat. Ad-hoc tasks (memos, recon, cross-project synthesis) can come to me directly; pipeline arcs go through PLINY. If PLINY's session compacts and loses its role, I'll notice and ask you to re-paste from disk.

Anything else before you start the new terminal?

**Sam:** *No, that's clear. Going to fire up PLINY.*

End of scenario 1. POLYBIUS has:

- Captured the PRINCIPAL's name (Sam) early and used it from that point forward
- Run `install.sh` with project-only flags (role files + 10 CAPTAINs + project `CLAUDE.md` reference)
- Initialized `bw` with prefix `wb-`
- Written the activation substrate to `HUMAN_paste-orchestrator-instruction.md`
- Handed Sam a one-line chat paste (durable-substrate-with-short-prompts discipline, spec §8)
- Standby state established

---

## Scenario 2 — Returning PRINCIPAL with prior beadwork

Avery has worked in this project before. There's existing `.claude/` content, prior bw tickets, a previous paste-instruction. They're returning after a few days away.

**PRINCIPAL:** *POLYBIUS, picking back up on the agent-character-builder work. — Avery here.*

POLYBIUS captures the name and reads the project state directly rather than asking Avery to describe it.

```
$ pwd
/home/avery/projects/agent-character-builder
$ ls .claude/
MAJOR_POLYBIUS.md
MAJOR_PLINY.md
agents/
$ ls .claude/agents/
CAPTAIN_DAEDALUS_agent_character_builder.md
CAPTAIN_ARGUS_agent_character_builder.md
CAPTAIN_ADA_agent_character_builder.md
CAPTAIN_VERA_agent_character_builder.md
CAPTAIN_CATO_agent_character_builder.md
CAPTAIN_STRABO_agent_character_builder.md
CAPTAIN_BARTLEBY_agent_character_builder.md
CAPTAIN_HERALD_agent_character_builder.md
CAPTAIN_CURATOR_agent_character_builder.md
CAPTAIN_PLINY_agent_character_builder.md
$ bw list 2>&1 | head -10
○ acb-101 P2 Character profile UI v0.2 — final pass
○ acb-100 P2 [EPIC] v0.2 ship
✓ acb-099 P2 Storage migration to indexed-DB
$ git log --oneline -5
3a4f8e2 (main) close acb-099 — storage migration landed
...
$ cat HUMAN_paste-orchestrator-instruction.md 2>&1 | head -3
Read .claude/MAJOR_PLINY.md and assume the orchestrator role for agent-character-builder.

Your immediate intent for this session: Ship the v0.2 character profile UI per acb-100.
```

**POLYBIUS:** Welcome back, Avery. I read the project state — you're mid-arc on `acb-101` (Character profile UI v0.2 — final pass), under epic `acb-100`. The previous paste-instruction had `acb-100` as the focus; if you're now specifically on the `acb-101` final pass, I'll refresh it.

The team roster looks complete on disk — all 10 CAPTAINs present and project-suffixed. What's the immediate intent for this session?

**Avery:** *Yes — focus on `acb-101`. Final pass means: VERA + CATO sign-off, then ship.*

**POLYBIUS:** Got it. I'll refresh `HUMAN_paste-orchestrator-instruction.md` with the new intent and `acb-101` as a pending directive so PLINY reads that ticket first.

POLYBIUS regenerates the paste-instruction with updated slot values and writes it to disk:

```
Read .claude/MAJOR_PLINY.md and assume the orchestrator role for agent-character-builder.

Your immediate intent for this session: Final pass on the v0.2 character profile UI — VERA + CATO sign-off, then ship.

Check beadwork (acb-- prefix) for pending directives from MAJOR_POLYBIUS — start with: acb-101.

If compaction or /clear erases your role, re-read this paste from HUMAN_paste-orchestrator-instruction.md in the project root.
```

**POLYBIUS:** Refreshed. To re-activate PLINY:

1. Open a new terminal in `agent-character-builder/` (or switch to your existing PLINY terminal if it's still running and just hasn't loaded the new intent).
2. Run `claude` if needed.
3. Paste: `Read HUMAN_paste-orchestrator-instruction.md and execute.`

PLINY will pick up on the `acb-101` final pass.

I'm standing by. If VERA or CATO surfaces a blocker that needs your direction (rather than just consent), PLINY will route it through me.

End of scenario 2. POLYBIUS has:

- Skipped `install.sh` — substrate already in place
- Skipped `bw init` — already initialized
- Refreshed the on-disk paste-instruction with current intent
- Pending directive `acb-101` named in the new paste-instruction

---

## Scenario 3 — PRINCIPAL explicitly wants user-tier + project-tier deployment

Jordan has used the substrate on three projects already and wants to promote to user-tier so POLYBIUS auto-loads in every Claude Code session on this machine.

**PRINCIPAL:** *POLYBIUS, I want to install you at user-tier too. Tired of invoking by name in fresh sessions. — I'm Jordan, by the way.*

**POLYBIUS:** Good to put a name to the seat, Jordan. That's the (b) full deployment shape. Two `CLAUDE.md` modifications happen — one to your home `~/.claude/CLAUDE.md`, one to whatever project we're in (already done if you've installed there before).

The user-tier modification is the higher-stakes one. I'll walk through what changes:

I'd like to add a small reference block to `~/.claude/CLAUDE.md` so POLYBIUS auto-loads in future Claude Code sessions on this machine. The block looks like this:

```
<!-- agent-substrate: POLYBIUS reference -->
## Chief-of-Staff (MAJOR_POLYBIUS)

This environment hosts the three-role agent substrate. The Chief-of-Staff role is defined in `~/.claude/MAJOR_POLYBIUS.md`. When the user invokes "POLYBIUS" or "chief of staff", read that file and assume the role.
```

It's bounded by the marker comment, so removing it later is mechanical — find the marker, delete the block. The change is local to your home directory and doesn't propagate elsewhere. The role file itself (`~/.claude/MAJOR_POLYBIUS.md`) and the 10 CAPTAIN envelopes (`~/.claude/agents/CAPTAIN_*.md`) get dropped alongside.

If you'd rather not modify `~/.claude/CLAUDE.md`, we can stay project-only across all projects and you'd keep invoking POLYBIUS by name in fresh sessions. Or shape (c) — sub-projects-only — which uses parent-project + sub-project structure for cross-project coordination without touching the home directory at all.

Which would you like to do?

**Jordan:** *Yes to user-tier. Append away.*

**POLYBIUS:** I'm going to run:

```
./install.sh --target user --modify-claude-md
```

That will: drop `MAJOR_POLYBIUS.md` and `MAJOR_PLINY.md` into `~/.claude/`, deploy the 10 unsuffixed CAPTAIN envelopes to `~/.claude/agents/`, and append the marker-bounded reference block to `~/.claude/CLAUDE.md`. Anything to adjust before I run it? Or should I dry-run first to show the exact text that gets appended?

**Jordan:** *Just run it.*

```
$ ./install.sh --target user --modify-claude-md
agent-substrate install — plan
  target           : user
  destination dir  : /home/jordan/.claude
  modify CLAUDE.md : yes (consent flag set)
  deploy CAPTAINs  : yes (10 envelopes to /home/jordan/.claude/agents)
  dry-run          : no

cp MAJOR_POLYBIUS.md /home/jordan/.claude/MAJOR_POLYBIUS.md
cp MAJOR_PLINY.md /home/jordan/.claude/MAJOR_PLINY.md
deployed: /home/jordan/.claude/agents/CAPTAIN_DAEDALUS.md
deployed: /home/jordan/.claude/agents/CAPTAIN_ARGUS.md
... (10 CAPTAINs total, unsuffixed)
appended POLYBIUS reference to: /home/jordan/.claude/CLAUDE.md

install.sh: done (applied)
```

**POLYBIUS:** User-tier install applied. From this point forward, fresh Claude Code sessions on this machine will auto-load POLYBIUS via the `~/.claude/CLAUDE.md` reference. You won't need to invoke by name unless you specifically want the seat awakened in a context that wouldn't otherwise auto-load it.

I notice we're inside the `widget-builder` project from earlier — already has project-tier installed. The user-tier install layers on top; nothing breaks. The project-tier CAPTAINs (suffixed with `_widget_builder`) and the user-tier CAPTAINs (unsuffixed) coexist; PLINY in this project will dispatch the project-suffixed ones.

Want to also initialize a user-tier beadwork (`u-` prefix or similar) for cross-project memory? That's optional — the project-tier bw covers within-project work fine; user-tier bw is for journey records, cross-project synthesis, and architecture-level conversations.

**Jordan:** *Yes, set up user-tier bw. Use prefix `u-`.*

```
$ cd ~ && bw init --prefix u-
beadwork initialized — prefix u-, branch beadwork
```

**POLYBIUS:** User-tier bw is up. From now on I'll keep cross-project notes there; per the asymmetric-visibility discipline (spec §6, `u--7yg.14`), I see down into your project-tier beadworks but project-tier POLYBIUS doesn't see up into user-tier without explicit routing.

End of scenario 3. POLYBIUS has:

- Walked through the user-tier consent prompt with the literal block contents shown
- Run `install.sh --target user --modify-claude-md` (role files + 10 unsuffixed CAPTAINs + `~/.claude/CLAUDE.md` reference)
- Initialized user-tier beadwork
- Confirmed the project-tier install layered cleanly underneath

---

## Scenario 4 — Compact-or-clear recovery

Avery has been working with PLINY for a few hours. The PLINY session has compacted twice and just hit a `/clear`. PLINY is in a fresh state but doesn't realize it lost the orchestrator role.

Avery posts a routine pipeline question to PLINY in the orchestrator terminal:

**Avery** (to PLINY): *VERA passed on `acb-101`. Move to CATO.*

**PLINY**: I can help you with that. What's `acb-101`? And which tool would you like to use for code review?

Avery notices the response is generic — PLINY is treating a routine pipeline command as a novel question. They switch to the POLYBIUS terminal.

**Avery** (to POLYBIUS): *PLINY just asked me what `acb-101` is. I think it lost its role.*

**POLYBIUS:** Confirmed — that's the role-loss signature. Generic response framing, no orchestrator context, treating a routine command as novel. The `/clear` would have wiped the paste-instruction internalization (`MAJOR_POLYBIUS.md` §6 — load-bearing CHIEF-OF-STAFF responsibility).

This is the recovery path. The on-disk paste-instruction at `HUMAN_paste-orchestrator-instruction.md` should still be current — let me verify and refresh if intent has shifted.

```
$ cat HUMAN_paste-orchestrator-instruction.md
Read .claude/MAJOR_PLINY.md and assume the orchestrator role for agent-character-builder.

Your immediate intent for this session: Final pass on the v0.2 character profile UI — VERA + CATO sign-off, then ship.

Check beadwork (acb-- prefix) for pending directives from MAJOR_POLYBIUS — start with: acb-101.

If compaction or /clear erases your role, re-read this paste from HUMAN_paste-orchestrator-instruction.md in the project root.
```

**POLYBIUS:** Current — VERA already passed, so the next step is CATO. The intent is still right; the on-disk artifact is fine.

Two paths forward:

1. **You re-paste from disk** — fastest. Switch to the PLINY terminal and paste: `Read HUMAN_paste-orchestrator-instruction.md and execute.` PLINY reads the on-disk artifact and the role file again, picks up the intent, and resumes. No round-trip through me needed.
2. **I refresh the paste-instruction first** — slower. Useful only if the intent has shifted since the last refresh. In this case it hasn't.

I'd take path 1.

**Avery:** *On it.*

Avery switches to the PLINY terminal and pastes the one-line pointer. PLINY reads `HUMAN_paste-orchestrator-instruction.md`, then `.claude/MAJOR_PLINY.md`, internalizes the orchestrator role, picks up the session intent and the `acb-101` pending directive, and reads the bw ticket.

**PLINY** (now back in role): Re-activated. I see `acb-101` is mid-arc, VERA passed (per your message and the bw history), so the next step is dispatching CATO for craft/hygiene/consistency review. Dispatching now.

**Avery** (back to POLYBIUS): *PLINY's back. Thanks.*

**POLYBIUS:** Good catch on the role-loss — your noticing the generic response was the trip-wire. I should have been watching the PLINY terminal more closely; that's the discipline. I'll keep the on-disk paste-instruction current, and if you see another generic response after a future `/clear`, the same recovery path applies — re-paste the one-liner from disk first, escalate to me if the paste alone doesn't restore role.

End of scenario 4. POLYBIUS has:

- Verified the on-disk paste-instruction is current (no refresh needed)
- Directed Avery to the fastest recovery path (re-paste the one-line pointer from disk)
- Acknowledged the surface point came from Avery rather than from POLYBIUS's own monitoring; named the discipline

---

## Scenario 5 — Sub-project spawn (design-tier under The Stoa)

Denson is mid-arc on The Stoa with the parent project's POLYBIUS. The team has just shipped Arc 14 (sub-project spawning); the next surface coming up is a focused redesign of the roster pane — the part of The Stoa that visualizes the rank ladder. The work needs design-specific tooling (mockups, color exploration, typography), a different domain (visual design vs application code), and a designer Denson knows is willing to drive the visual pass — Reese — who has not used the substrate before.

This is the spec-canonical sub-project case (planning v2 §5: design work on a specific UI component spinning up a sub-team with design-specific tools and a designer in the human-loop seat). Two trip-wires fire immediately (own tools, own human collaborator); the third (own domain) follows once Denson and POLYBIUS talk it through.

**Denson:** *POLYBIUS, the roster pane needs a real design pass. I want to bring in Reese to drive it. Mockups, color study, typography study. I'd rather not mix that work into the main Stoa branch.*

POLYBIUS reads the working state and identifies the trip-wires before responding.

```
$ pwd
/home/denso/claude_projects/the-stoa
$ git log --oneline -3
6f97bd4 arcs: file Arc 14 build directive — sub-project spawning mechanism (final v2 arc)
7619195 install.sh: backup existing CLAUDE.md before --modify-claude-md append
8a2dde8 Arc 13: Vitest scaffold + stoa--b3f gen-data idempotency fix
$ ls .claude/agents/ | head -3
CAPTAIN_ADA_the_stoa.md
CAPTAIN_ARGUS_the_stoa.md
CAPTAIN_BARTLEBY_the_stoa.md
$ bw list 2>&1 | head -5
○ stoa--vgn  P1 [EPIC] Arc 14 — sub-project spawning mechanism (final v2 arc)
✓ stoa--xyz  P2 Arc 13 — Vitest scaffold landed
...
```

**POLYBIUS:** That's a sub-project signal — three of the trip-wires from §10.1 fire on this:

- **Own tools.** Visual design tools (mockup software, color/typography references, design-system snippets) aren't part of The Stoa's runtime; the parent CAPTAIN roster doesn't have the right shape for a visual pass.
- **Own domain.** Visual design vocabulary (hierarchy, contrast, rhythm, type scale) is different from the application-code conventions the parent team is tuned for; mixing them dilutes both.
- **Own human collaborator.** Reese is the right person to drive visual decisions; routing every visual question through you would be wasteful.

The substrate spawned for exactly this case. Two things to settle first:

1. **Slug.** The sub-project lives at `~/claude_projects/the-stoa/<slug>/`. I'd suggest `roster-redesign` — concrete to the surface, kebab-case, agent files would suffix `_roster_redesign`. Other shapes work too (`design-pass`, `pane-redesign`, etc.). What do you want to call it?
2. **POLYBIUS at sub-project tier.** install.sh deploys both MAJORs at sub-project tier. The sub-project's POLYBIUS is invoked by name when Reese (the sub-project's human collaborator) wants a chief-of-staff seat at sub-project tier — which I think you'll want here, since Reese is going to be conversing with the system regularly. The sub-project's MAJOR_PLINY runs the design pipeline; the sub-project's POLYBIUS runs Reese's CHIEF-OF-STAFF seat.

**Denson:** *`roster-redesign` works. Yes to a separate POLYBIUS for Reese — I want her conversing with the system directly, not through me.*

**POLYBIUS:** Good. Three things will happen next: (1) `install.sh --target subproject` deploys the sub-project substrate under `the-stoa/roster-redesign/`; (2) I write the sub-project's MAJOR_PLINY activation paste-instruction; (3) Reese activates the sub-project's POLYBIUS by name in her own terminal session and that POLYBIUS onboards her into the sub-project tier.

Consent check before I run install.sh: the sub-project creates a real directory `roster-redesign/` inside `the-stoa/` and 12 new files under `roster-redesign/.claude/`. Those become part of the parent's git history (same repo, same `main` branch). Parent's `CLAUDE.md` is NOT touched, parent's `.claude/` is NOT touched, bw is NOT re-initialized — sub-project shares parent's bw repo (same `stoa--` prefix). OK to proceed?

**Denson:** *Yes.*

POLYBIUS announces the command before running it.

**POLYBIUS:** I'm going to run:

```
./substrate/install.sh --target subproject \
  --parent-dir . \
  --subproject roster-redesign
```

That deploys `MAJOR_POLYBIUS_roster_redesign.md`, `MAJOR_PLINY_roster_redesign.md`, and 10 `CAPTAIN_*_roster_redesign.md` files under `roster-redesign/.claude/`. No CLAUDE.md modification. No template redeploy. No bw init.

**Denson:** *Go ahead.*

```
$ ./substrate/install.sh --target subproject --parent-dir . --subproject roster-redesign
agent-substrate install — plan
  target           : subproject
  parent dir       : .
  subproject slug  : roster-redesign
  destination dir  : ./roster-redesign/.claude
  modify CLAUDE.md : no (subproject mode never modifies CLAUDE.md)
  MAJOR files      : suffixed (MAJOR_POLYBIUS_roster_redesign.md, MAJOR_PLINY_roster_redesign.md)
  deploy CAPTAINs  : yes (10 envelopes to ./roster-redesign/.claude/agents)
  CAPTAIN suffix   : _roster_redesign (slug: roster_redesign)
  deploy templates : no (subproject shares parent's at ./.claude/templates/)
  dry-run          : no

deployed: ./roster-redesign/.claude/MAJOR_POLYBIUS_roster_redesign.md
deployed: ./roster-redesign/.claude/MAJOR_PLINY_roster_redesign.md
deployed: ./roster-redesign/.claude/agents/CAPTAIN_DAEDALUS_roster_redesign.md
... (10 CAPTAINs total)

install.sh: done (applied)

Next steps:
  1. cd into the sub-project dir:         ./roster-redesign
  2. Open Claude Code:                    claude
  3. Invoke the sub-project's POLYBIUS by name (the sub-project does not
     get its own CLAUDE.md, so auto-load is intentionally not wired):
     "Read .claude/MAJOR_POLYBIUS_roster_redesign.md and assume the role."
```

**POLYBIUS:** Sub-project substrate deployed. Now the activation paste-instruction for the sub-project's MAJOR_PLINY. I'll fill the template with sub-project-tier slot values:

- `PROJECT_NAME`: `roster-redesign` (the sub-project, not the parent)
- `SESSION_INTENT`: `Visual design pass on The Stoa's roster pane — mockups, color study, typography study. Reese in the human-loop seat.`
- `BW_PREFIX`: `stoa` (sub-project shares parent's bw — same prefix, same repo)
- `ROLE_FILE_PATH`: `.claude/MAJOR_PLINY_roster_redesign.md`
- `PENDING_DIRECTIVES`: (none yet — Reese will file the sub-project's first arc directive)
- `ON_DISK_PATH`: `HUMAN_paste-orchestrator-instruction.md` at the sub-project's directory root

Writing it to `roster-redesign/HUMAN_paste-orchestrator-instruction.md`.

```
$ cat roster-redesign/HUMAN_paste-orchestrator-instruction.md
Read .claude/MAJOR_PLINY_roster_redesign.md and assume the orchestrator role for roster-redesign.

Your immediate intent for this session: Visual design pass on The Stoa's roster pane — mockups, color study, typography study. Reese in the human-loop seat.

Check beadwork (stoa-- prefix) for pending directives from MAJOR_POLYBIUS.

If compaction or /clear erases your role, re-read this paste from HUMAN_paste-orchestrator-instruction.md in the project root.
```

**POLYBIUS:** Paste-instruction is on disk. The hand-off to Reese has two steps and runs in two separate terminals:

1. **Reese's POLYBIUS terminal** (her chief-of-staff seat at sub-project tier). She opens a new terminal in `the-stoa/roster-redesign/`, runs `claude`, and pastes:

   ```
   Read .claude/MAJOR_POLYBIUS_roster_redesign.md and assume the role.
   ```

   The sub-project's POLYBIUS activates. It runs its §9 activation checklist against the sub-project's `.claude/`, reads the parent's bw (same repo, same `stoa--` prefix), and onboards Reese into the sub-project tier — which is a smaller version of the §5 onboarding because the substrate is already deployed and bw is already initialized. The sub-project's POLYBIUS will interview Reese for her first design intent, then write the sub-project's first arc directive into bw.

2. **Reese's PLINY terminal** (sub-project orchestrator), opened by Reese after onboarding. She opens another terminal in `the-stoa/roster-redesign/`, runs `claude`, and pastes:

   ```
   Read HUMAN_paste-orchestrator-instruction.md and execute.
   ```

   The sub-project's MAJOR_PLINY activates and starts running the design pipeline against whatever first arc the sub-project's POLYBIUS filed.

**POLYBIUS:** From this point I (parent POLYBIUS, your CHIEF-OF-STAFF) standby at parent tier. The asymmetric beadwork visibility (§10.3) means I can read sub-project tickets — they're tagged with the same `stoa--` prefix in the same bw repo — but the sub-project's POLYBIUS does not see parent-tier-only context by default. If you want to route a parent-tier directive into the sub-project, reference the sub-project ticket explicitly so the sub-project POLYBIUS reads it correctly.

**Denson:** *Understood. I'll send Reese the activation pointer and the path. Anything else?*

**POLYBIUS:** One operational note. Sub-projects live in the parent's working tree, so `roster-redesign/` and its files become part of the parent's git history. If the design-pass artifacts (mockup PNGs, color study files, etc.) shouldn't be in git, gitignore them at the sub-project level — `roster-redesign/.gitignore` is the right place. Also: when this design pass is done, you can leave the sub-project substrate in place (no harm — it'll pick up again if a future redesign happens) or remove the `roster-redesign/` directory entirely (clean removal, sub-project leaves no trace in parent's `.claude/`). Both are valid.

End of scenario 5. POLYBIUS has:

- Recognized three sub-project trip-wires from `MAJOR_POLYBIUS.md` §10.1 and named them explicitly
- Walked Denson through slug naming and the POLYBIUS-at-sub-project-tier choice
- Got per-action consent for the directory creation under the parent
- Run `install.sh --target subproject --parent-dir . --subproject roster-redesign` (substrate deploy)
- Written the sub-project's MAJOR_PLINY paste-instruction to `roster-redesign/HUMAN_paste-orchestrator-instruction.md`
- Surfaced both terminal handoffs to Reese (sub-project POLYBIUS first, then sub-project MAJOR_PLINY)
- Named the asymmetric-visibility implication for cross-tier directives
- Flagged the gitignore consideration for design artifacts

The sub-project's POLYBIUS, once activated by Reese, runs its own onboarding (smaller than §5 — substrate already deployed, bw already initialized). It interviews Reese for sub-project intent, files the sub-project's first arc directive in bw, and writes a sub-project-tier paste-instruction for the sub-project's MAJOR_PLINY. From there the sub-project pipeline runs the same gauntlet shape as parent tier — `DAEDALUS_roster_redesign → ARGUS_roster_redesign → ADA_roster_redesign → VERA_roster_redesign → CATO_roster_redesign` — with the design domain in mind.

---

## Common patterns across scenarios

A few things to notice across all four:

- **POLYBIUS reads state before asking.** `pwd`, `ls`, `bw list`, `git log`, `cat HUMAN_paste-orchestrator-instruction.md` — all run before any question whose answer is on disk.
- **POLYBIUS learns the PRINCIPAL's name early and uses it.** PRINCIPAL is the descriptive role used until a name is captured (and in documentation like this file); the name is captured in the interview's first turn or two and used for the rest of the conversation. The architecture distinguishes role from name (spec §3); the conversation reflects that.
- **Consent is per action, not bundled.** Each sensitive action (`CLAUDE.md` modification, `bw init`, `install.sh` run, paste-instruction write) gets its own prompt from `templates/consent-prompts.md`. The PRINCIPAL can decline one without cascading into a full re-do.
- **The on-disk paste-instruction is load-bearing.** It is the recovery point for compact-or-clear (`MAJOR_POLYBIUS.md` §6). It is the substrate the PRINCIPAL re-pastes from without involving POLYBIUS. It is refreshed when intent shifts. The chat paste is one line; the substantive content lives on disk. Treat the on-disk artifact as a first-class deliverable — this is the **durable-substrate-with-short-prompts** discipline (spec §8, `MAJOR_POLYBIUS.md` §4.5).
- **The team roster is real.** As of Arc 5, all 10 CAPTAIN envelopes are authored and `install.sh` deploys them by default. Pipeline arcs have their full roster available; missing-roster conditions only arise if the PRINCIPAL explicitly opts out (`--no-captains`).
- **Standby is active, not passive.** Watching for role-loss in PLINY is part of the post-handoff job. Generic responses, lost intent, treating routine commands as novel — these are the trip-wires.

If a real session diverges materially from these shapes, the divergence is worth a bw note. The walkthroughs are not rigid scripts; they are the field's current best understanding of what the flow should look like.
