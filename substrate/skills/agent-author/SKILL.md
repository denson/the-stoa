---
name: agent-author
description: Draft a new agent role file (pair-programmer MAJOR, specialized CAPTAIN, or LIEUTENANT skill envelope) from a template basis, with voice-discipline check applied. POLYBIUS invokes this when authoring a new agent on-demand — examples include spawning a pair-programmer MAJOR for a fast-prototyping task (PYTHAGORAS for Python, ATTICUS for editorial, CODEX for TypeScript, LEX for regulation), adding a new specialized CAPTAIN to the substrate canon, or extending the substrate's LIEUTENANT roster. Reads a template existing role file as basis, substitutes the new agent's name / mnemonic / specialization / responsibilities, runs the v2 voice-discipline check (PRINCIPAL/HUMAN throughout, no COLONEL leakage, no second-person framing), and writes the draft directly to substrate for working-tree review before commit. Triggers on requests like "author a new agent", "draft a pair-programmer for X", "create a CAPTAIN for Y", "spawn ATTICUS / PYTHAGORAS / CODEX / LEX", or any phrasing that maps to "produce a new agent role file from a template".
---

# agent-author — draft a new agent role file with voice-discipline check applied

## Why this skill exists

POLYBIUS authors new agents on-demand: pair-programmer MAJORs spawned for substantive domain work (Python, regulation, design, code-at-large), specialized CAPTAINs added to the substrate canon when the gauntlet needs a new seat, LIEUTENANT skills when a mechanical helper would close a gap. Authoring these by hand is mostly mechanical — start from the closest-fit existing role file, swap in the new name / mnemonic / specialization, prune sections that don't apply, run the voice-discipline check that v2 made load-bearing.

Doing it by hand reliably drops the voice check. The v2 substrate enforces a specific vocabulary — PRINCIPAL / HUMAN throughout, COLONEL only for the reserved future agent rank, no second-person framing — and reflexive leakage from v1 ("Colonel" for the human, "you should" for the agent) keeps surfacing in hand-authored drafts. This skill mechanizes the substitution AND embeds the voice-discipline check as part of the procedure, so the check fires every time, not only when POLYBIUS happens to remember.

The output is a draft on disk. Review and commit are POLYBIUS's call (working-tree-vs-committed is the review gate; no `substrate/drafts/` staging overhead).

## When to use this skill

Invoke when:

- POLYBIUS has decided to author a new agent (a pair-programmer MAJOR for substantive domain work, a new substrate-canon CAPTAIN, or a new LIEUTENANT skill envelope).
- The PRINCIPAL has agreed to the spawn (project-direction call — see MAJOR_POLYBIUS.md §4.1).
- The closest-fit existing role file is identifiable as a template basis.

Do **not** invoke for:

- Renaming an existing agent (a rename is not authoring; it's an arc — see Arc 16's CAPTAIN_PLINY → CAPTAIN_ZENO pattern).
- Editing an existing agent's role file (use Edit directly).
- Deploying an authored agent to `.claude/agents/` (that's `install.sh` for substrate-canonical agents, or manual `cp` plus a paste-instruction for on-demand pair-programmer MAJORs).

## Inputs

POLYBIUS supplies these when invoking the skill:

| input | required | purpose |
|---|---|---|
| `agent_type` | yes | One of: `pair_programmer_major`, `substrate_captain`, `lieutenant_skill`. Determines section structure and template basis. |
| `name` | yes | Display name (e.g., `ATTICUS`, `CAPTAIN_FOO`, `agent-author`). For MAJORs and CAPTAINs this is the mnemonic in uppercase; for skills it is the kebab-case skill name. |
| `mnemonic` | for MAJORs/CAPTAINs | The single-word mnemonic (e.g., `ATTICUS`). Equal to `name` for MAJORs and the post-`CAPTAIN_` part for CAPTAINs. |
| `descriptive_role` | for MAJORs/CAPTAINs | One-word job description (e.g., `EDITORIAL-PAIR-PROGRAMMER`, `PYTHON-PAIR-PROGRAMMER`, `STATIC-ANALYZER`). |
| `specialization` | yes | What domain / task class this agent specializes in. Two to four sentences, plain prose. |
| `responsibilities` | yes | Bullet list: what this agent does. Mirror the §2 "What you do" structure of existing role files. |
| `non_responsibilities` | yes | Bullet list: what this agent explicitly does NOT do. Mirror the §3 "What you don't do" structure. The non-list is load-bearing for one-job-per-agent (`u--7yg.17`); skip it and the new seat will collapse into adjacent ones. |
| `template_basis` | yes | Path to the existing role file to use as structural template (see §"Template-basis selection" below). |
| `dest_path` | yes | Where to write the draft. See §"Destination" for the conventions. |

## Destination

The draft is written directly to disk at `dest_path`. Substrate is git-tracked, so the working tree IS the staging area — POLYBIUS reviews the draft in the working tree, edits in place, and commits when satisfied. There is no separate `drafts/` directory.

Conventional `dest_path` choices:

- **Substrate-canonical CAPTAIN** (rare; substrate-evolution arc): `substrate/CAPTAIN_<MNEMONIC>.md` in the substrate repo. After commit, install.sh deploys it (the `CAPTAIN_NAMES` array also needs a manual entry — that is a separate edit, not part of this skill).
- **Substrate-canonical MAJOR** (very rare; structural change to the substrate spec): `substrate/MAJOR_<MNEMONIC>.md` in the substrate repo. Coordinate with a parallel update to the architecture spec.
- **Pair-programmer MAJOR for project use** (the common case): `.claude/agents/<MNEMONIC>.md` in the active project, OR `~/.claude/agents/<MNEMONIC>.md` for cross-project reuse. Pair-programmer MAJORs deployed this way are NOT substrate-canonical; they live alongside the canonical POLYBIUS+PLINY in the agents/ directory but are project-authored.
- **LIEUTENANT skill** (substrate-evolution arc): `substrate/skills/<skill-name>/SKILL.md`. After commit, install.sh deploys it (the `SKILL_NAMES` array needs a manual entry).

If the destination file already exists, the skill stops and surfaces the conflict — overwrites are POLYBIUS's call, not the skill's.

## Procedure

1. **Validate inputs.** Confirm `agent_type` is one of the three values, `name` matches the convention for that type (uppercase identifier for MAJORs/CAPTAINs, kebab-case for skills), `template_basis` exists, `dest_path` does not exist (overwrite is a POLYBIUS-explicit decision after seeing the conflict).

2. **Read the template basis** with the Read tool. Capture its structure: section headers, the §1 "What you are" frame, the §2/§3 responsibility tables, the §4 "Disciplines" inheritance pattern (or skill-format equivalents).

3. **Draft the new role file** by structural substitution:
   - Replace the seat-identification table at the top (Rank, Mnemonic, Descriptive role, Lives at, Activation) with the new agent's values.
   - Rewrite §1 ("What you are") in the new agent's voice — same structural shape, new specialization content.
   - Replace §2 ("What you do") with the responsibilities list.
   - Replace §3 ("What you don't do") with the non-responsibilities list.
   - Preserve §4 ("Disciplines") inheritance lines verbatim where applicable — disciplines travel with rank (a new MAJOR inherits the MAJOR-tier disciplines; a new CAPTAIN inherits the CAPTAIN-tier disciplines).
   - **For new CAPTAINs:** preserve the heartbeat-and-read-before-write subsection from the template basis verbatim, customizing only the seat name and the state-transition examples per the seat's actual work. The discipline's substantive home is `operating-disciplines.md` §18 (Subagent status via bw + orchestrator dispatch hygiene); cross-reference it from the new subsection's first paragraph (canonical opening sentence in §18 of operating-disciplines.md). The substance is universal-CAPTAIN; the wording adapts per seat (probe execution for VERA-shaped seats; build phases for ADA-shaped seats; review phases for CATO-shaped seats; etc.). Wording drift across CAPTAIN role files is the most likely defect class — author one canonical subsection from the template basis and customize, do not re-derive from scratch.
   - For LIEUTENANT skills, follow the SKILL.md shape rather than the role-file shape (frontmatter, "Why this skill exists", "When to use", "Inputs", "Procedure", "What this skill is NOT").

4. **Run the voice-discipline check** on the draft (see §"Voice discipline check" below). Fix every match before writing.

5. **Write the draft** to `dest_path` with the Write tool.

6. **Surface the result to POLYBIUS** with: (a) the path written, (b) the voice-check result, (c) a one-line note on what POLYBIUS should review (typically: "voice-check clean; review §1 framing for fit, then commit").

## Voice discipline check

This is the dogfooding step. The substrate uses a specific vocabulary; the load-bearing v1→v2 transition (`u--7yg.20`) was the recognition that role-file voice is structural, not stylistic. New role files inherit the voice the substrate teaches them — drafts that leak v1 vocabulary teach the wrong vocabulary downstream.

Before writing the draft to disk, scan it for these patterns. Every match is a defect to fix:

| pattern | regex / token | fix |
|---|---|---|
| `Colonel` used to refer to the human | case-insensitive match on `colonel`, EXCEPT in deliberate references to the reserved future agent rank (e.g., "COLONEL is a reserved future agent rank") | replace with `PRINCIPAL` (or `HUMAN_<name>` if a specific person is named, or just `the human` if generic) |
| Second-person `you` referring to the human (not the agent reading the file) | hard to catch with regex; read for it | rewrite in the seat-voice (the agent talks ABOUT the PRINCIPAL, not TO the PRINCIPAL) |
| `the user` instead of `PRINCIPAL` / `HUMAN` | case-insensitive `the user` | replace with `PRINCIPAL` (preferred) or `HUMAN_<name>` (if specific) |
| Imperative second-person framing where seat-voice is correct | "You should X" → "The seat does X" | rewrite in third-person seat-voice; agents read role files about themselves, but the prose names what the seat does, not what the reader should do |
| Missing heartbeat-and-read-before-write subsection (new CAPTAIN drafts only) | Read for presence of the canonical opening sentence "Anthropic's tool surface does not provide mid-execution Agent introspection. The substrate's answer is bw — a substrate we already control." in the disciplines section | If missing in a new CAPTAIN draft, copy the subsection from the closest-fit template basis and customize for the new seat; cross-ref `operating-disciplines.md` §18 |

Practical tooling for the check:

```bash
# Colonel leakage — should match only deliberate reserved-rank references.
grep -ni "colonel" <draft-path>

# "the user" leakage — should match zero lines in a clean draft.
grep -ni "the user" <draft-path>

# Heartbeat-subsection presence — CAPTAIN drafts only.
grep -n "Anthropic's tool surface does not provide mid-execution Agent introspection" <draft-path>
```

Read the matched lines in context. If a `colonel` match is the deliberate "COLONEL is a reserved future agent rank" reference, accept it. Any other `colonel` match is a regression — fix it.

The voice check is non-optional. The substrate's voice discipline only stays load-bearing if every new agent file enforces it on authoring; skipping the check once teaches the substrate that the discipline is optional.

## Template-basis selection

| authoring case | template basis | reason |
|---|---|---|
| New pair-programmer MAJOR | A previously authored pair-programmer MAJOR (e.g., the deployed `~/.claude/agents/PYTHAGORAS.md` or `ATTICUS.md`), OR `MAJOR_POLYBIUS.md` for the structural shape if no pair-programmer exists yet | Pair-programmer MAJORs share section structure (seat-identification table, §1 frame, §2 "What you do" responsibilities, §6 communication channels). Starting from one already in the wild preserves the empirical voice; starting from POLYBIUS is the fallback. |
| New substrate-canonical CAPTAIN | The closest-fit existing CAPTAIN. For an architect-shaped seat, `CAPTAIN_DAEDALUS.md`; for a critic-shaped seat, `CAPTAIN_ARGUS.md` or `CAPTAIN_CATO.md`; for a builder-shaped seat, `CAPTAIN_ADA.md`; for a verifier-shaped seat, `CAPTAIN_VERA.md`; for a research/recon seat, `CAPTAIN_STRABO.md` or `CAPTAIN_BARTLEBY.md`; for a synthesis seat, `CAPTAIN_CURATOR.md`; for a spec-checker, `CAPTAIN_ZENO.md`. | CAPTAINs share the §4 disciplines inheritance and the §"What this CAPTAIN is NOT" structural slot; using a same-shape template makes the substitution more mechanical and the diff cleaner. |
| New LIEUTENANT skill | The closest-fit existing skill in `substrate/skills/` (currently only `agent-author/SKILL.md` ships in substrate; for a richer pattern reference look at `agent-gauntlet/skills/format-validate/SKILL.md` or `agent-gauntlet/skills/spawn-pair-programmer/SKILL.md`) | Skills follow the SKILL.md frontmatter convention. Substrate skills are procedural (POLYBIUS reads, follows); agent-gauntlet skills are often shell-out wrappers with a Python implementation. Pick the closer match. |

If no clear template basis exists, surface that to POLYBIUS instead of guessing — picking the wrong template basis bakes in structural defects the voice-check will not catch.

## What this skill is NOT

- **Not a deployer.** This skill writes a draft. Deploying a substrate-canonical CAPTAIN to user-tier or project-tier is `install.sh`'s job; deploying an on-demand pair-programmer MAJOR is `cp` plus a paste-instruction.
- **Not a renamer.** Renaming an existing agent (CAPTAIN_PLINY → CAPTAIN_ZENO in Arc 16) is an arc, not a single skill invocation. The arc updates references across substrate, app data, tests, and bw history.
- **Not a SKILL_NAMES / CAPTAIN_NAMES editor.** When a new substrate-canonical CAPTAIN or skill is authored, the corresponding array in `install.sh` needs a manual entry — that is a separate Edit, not part of this skill's output. The skill's surface to POLYBIUS should remind POLYBIUS to update the array.
- **Not a substitute for design judgment.** Choosing whether a new seat should exist at all (one-job-per-agent triggers, role-collapse risks, whether the work fits an existing seat better than a new one) is POLYBIUS-and-PRINCIPAL territory before this skill runs. The skill mechanizes the *authoring*, not the *decision to author*.
- **Not a generator from no template.** Every draft starts from a template basis. Authoring a brand-new structural shape (the first MAJOR-tier seat, the first CAPTAIN-tier seat) was substrate-design work, done with the architecture spec as authority. By the time this skill is invoked, a template basis exists.

## Surface back to POLYBIUS

After the draft is written, surface a short report to POLYBIUS:

```
agent-author draft written:
  dest_path:           <absolute path>
  agent_type:          <pair_programmer_major | substrate_captain | lieutenant_skill>
  template_basis:      <absolute path>
  voice_check:         <pass | fail>
  voice_check_notes:   <verbatim grep output for any flagged lines, or "(none)">
  next_steps_for_polybius:
    - Read the draft in the working tree and review for fit.
    - <Type-specific reminder, e.g., "Add MNEMONIC to install.sh CAPTAIN_NAMES if substrate-canonical."
                                      "Write paste-instruction if pair-programmer MAJOR."
                                      "Add skill-name to install.sh SKILL_NAMES if LIEUTENANT skill.">
    - Commit when satisfied. Working-tree-vs-committed is the review gate.
```

POLYBIUS's review-and-commit step is outside this skill's scope. The skill is done when the draft is on disk and the voice-check result is reported.
