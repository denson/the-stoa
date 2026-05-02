# Onboarding — what a real session looks like

Narrative walkthroughs of MAJOR_POLYBIUS conducting onboarding. Two purposes:

1. **Test harness** — a Claude Code session that has just adopted the POLYBIUS role can read this file and run a tabletop rehearsal of the flow before live use, catching mismatches between the role file (`MAJOR_POLYBIUS.md`) and the templates (`templates/*.md`).
2. **Documentation** — humans browsing the repo see what to expect when they open POLYBIUS for the first time, before they commit to running anything.

Architecture authority: `user-beadwork/plans/three-role-recursive-architecture.md` (v2). Onboarding flow lives in spec §8; the role's responsibilities live in `MAJOR_POLYBIUS.md` §5.

Four scenarios below cover the common and the load-bearing-rare paths:

| # | Scenario | What's being tested |
|---|---|---|
| 1 | First-time PRINCIPAL, intent unclear, project-only deploy | the conservative path; interview discipline; learning the PRINCIPAL's name |
| 2 | Returning PRINCIPAL with prior beadwork | reading state before asking; refreshing intent |
| 3 | PRINCIPAL who explicitly wants user-tier + project-tier | the higher-stakes consent moment; user-tier `CLAUDE.md` modification |
| 4 | Compact-or-clear recovery — MAJOR_PLINY lost its role | the load-bearing CHIEF-OF-STAFF responsibility (`MAJOR_POLYBIUS.md` §6); on-disk-paste re-activation |

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

## Common patterns across scenarios

A few things to notice across all four:

- **POLYBIUS reads state before asking.** `pwd`, `ls`, `bw list`, `git log`, `cat HUMAN_paste-orchestrator-instruction.md` — all run before any question whose answer is on disk.
- **POLYBIUS learns the PRINCIPAL's name early and uses it.** PRINCIPAL is the descriptive role used until a name is captured (and in documentation like this file); the name is captured in the interview's first turn or two and used for the rest of the conversation. The architecture distinguishes role from name (spec §3); the conversation reflects that.
- **Consent is per action, not bundled.** Each sensitive action (`CLAUDE.md` modification, `bw init`, `install.sh` run, paste-instruction write) gets its own prompt from `templates/consent-prompts.md`. The PRINCIPAL can decline one without cascading into a full re-do.
- **The on-disk paste-instruction is load-bearing.** It is the recovery point for compact-or-clear (`MAJOR_POLYBIUS.md` §6). It is the substrate the PRINCIPAL re-pastes from without involving POLYBIUS. It is refreshed when intent shifts. The chat paste is one line; the substantive content lives on disk. Treat the on-disk artifact as a first-class deliverable — this is the **durable-substrate-with-short-prompts** discipline (spec §8, `MAJOR_POLYBIUS.md` §4.5).
- **The team roster is real.** As of Arc 5, all 10 CAPTAIN envelopes are authored and `install.sh` deploys them by default. Pipeline arcs have their full roster available; missing-roster conditions only arise if the PRINCIPAL explicitly opts out (`--no-captains`).
- **Standby is active, not passive.** Watching for role-loss in PLINY is part of the post-handoff job. Generic responses, lost intent, treating routine commands as novel — these are the trip-wires.

If a real session diverges materially from these shapes, the divergence is worth a bw note. The walkthroughs are not rigid scripts; they are the field's current best understanding of what the flow should look like.
