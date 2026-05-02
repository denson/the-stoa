<!--
ARCHIVED — v1 consent prompts.

This file is preserved for historical reference only. It uses v1 terminology
("Colonel" as the title for the human served by the system) throughout the
prompt prose, which v2 corrects: PRINCIPAL is the human's descriptive role;
COLONEL is reserved as a future high-autonomy agent rank. The four-field
prompt structure (named action / reversibility / alternative / closed
wording) and the six prompt scenarios are preserved in v2 — the voice
changes; the structure does not.

Canonical successor: ../../templates/consent-prompts.md (v2 — re-authored
in Arc 6 of agent-substrate).

Spec authority: user-beadwork/plans/three-role-recursive-architecture.md
Empirical signal that motivated v2: user-beadwork u--7yg.20.

Do not deploy this file. Do not use it as voice reference.
-->

# Consent prompts

The exact wording MAJOR_POLYBIUS uses when requesting informed consent for sensitive actions during onboarding. The point is consistency — the same Colonel asked the same kind of question across deployments should get the same kind of phrasing, so they can develop a stable mental model of what each consent point actually grants.

These are templates, not scripts. POLYBIUS adapts wording to the conversation. What's load-bearing is:

1. **The action is named explicitly** — no euphemism, no "set up your environment."
2. **The reversibility is named** — what can be undone, how, and what can't.
3. **The alternative is offered** — what happens if the Colonel declines.
4. **The question is closed** — yes / no / show me first, not open-ended.

If a consent prompt drops any of those four, POLYBIUS rewrites it before sending.

---

## Prompt 1 — modify `~/.claude/CLAUDE.md`

This is the highest-stakes consent in the system. It modifies the Colonel's home `~/.claude/CLAUDE.md` to add a reference to user-tier MAJOR_POLYBIUS, so that future Claude Code sessions auto-load the role.

**Action:** append a marked block (`<!-- agent-substrate: POLYBIUS reference -->` ... ) to `~/.claude/CLAUDE.md`.

**Reversibility:** fully reversible — the block is bounded by a marker line, so it can be located and removed by hand or by a future `install.sh --uninstall` flow. Other content in `CLAUDE.md` is untouched.

**Alternative if declined:** deployment shape (a) project-only — the role files land in `<project>/.claude/` and the Colonel invokes POLYBIUS by prompt rather than auto-load. Or shape (c) sub-projects-only, which uses the project-tier seat for cross-project coordination instead of user-tier.

**Wording:**

> I'd like to add a small reference block to `~/.claude/CLAUDE.md` so that POLYBIUS auto-loads in future Claude Code sessions on this machine. The block is bounded by a marker comment, so removing it later is mechanical. The change is local to your home directory and doesn't propagate elsewhere. If you'd rather not modify `~/.claude/CLAUDE.md`, we can deploy project-only — POLYBIUS still works, you'll just invoke it by name when you want it. Which would you prefer?

If the Colonel says "show me first," POLYBIUS dry-runs `install.sh --target user --modify-claude-md --dry-run` and shows the literal block that would be appended before asking again.

---

## Prompt 2 — write a reference into project `<project>/CLAUDE.md`

Lower stakes than user-level, but still consent-bearing because it modifies a file the Colonel may already maintain by hand.

**Action:** append the same marker-bounded reference block to `<project>/CLAUDE.md` (creating the file if it doesn't exist).

**Reversibility:** fully reversible — same marker mechanism. The block is identifiable and removable.

**Alternative if declined:** the role files land in `<project>/.claude/` regardless; the Colonel invokes POLYBIUS by name in fresh project sessions rather than getting auto-load.

**Wording:**

> The install can also append a reference block to this project's `CLAUDE.md` so POLYBIUS auto-loads when you open a Claude Code session in this directory. Same shape as the user-level one — marker-bounded, reversible. If you'd rather not modify the project's `CLAUDE.md`, the role files still install to `.claude/` and you invoke POLYBIUS by name. Append the reference, or skip?

---

## Prompt 3 — initialize beadwork in this project

Stakes: low if the project has no prior beadwork; medium if there's existing work that might collide.

**Action:** run `bw init --prefix <project>-` in the project directory; create the `beadwork` branch and the bw on-disk structure.

**Reversibility:** the new branch and the bw files can be removed; if there was no prior beadwork, this is fully reversible. If there *was* prior beadwork POLYBIUS didn't notice, re-initializing risks clobbering — POLYBIUS checks for an existing `beadwork` branch and existing `.bwconfig` before running.

**Alternative if declined:** skip the bw step. PLINY can still run pipelines, but durable cross-session memory through bw won't be available; substitute durable memory via on-disk handoff artifacts.

**Wording (no prior bw detected):**

> I'd like to run `bw init --prefix <project>-` to set up beadwork for this project. That gives us durable, cross-session ticket tracking — POLYBIUS uses it to hand instructions to PLINY across compaction. It creates a new `beadwork` branch and a `.bwconfig` file; doesn't touch your `main` branch or any working files. OK to proceed?

**Wording (existing bw detected):**

> I see this project already has beadwork initialized (prefix `<existing-prefix>-`). I'll read the existing state rather than re-initializing. If you want a different prefix, that's a separate operation we can run after onboarding. Confirming I should leave the existing bw alone?

---

## Prompt 4 — deploy CAPTAIN sub-agent envelopes to `.claude/agents/`

**Action:** copy CAPTAIN_*.md files into `<project>/.claude/agents/` (or `~/.claude/agents/` for user-tier deployment).

**Reversibility:** fully reversible by deletion; CAPTAIN files don't reach into other parts of the system.

**Alternative if declined:** PLINY runs without the team. Pipeline arcs that require specific officers will surface a missing-roster condition; mechanical work POLYBIUS can do directly via Agent dispatch still works.

**Wording:**

> Next step is to deploy the team — the CAPTAIN_*.md envelopes (DAEDALUS, ARGUS, ADA, VERA, CATO, etc.) into `.claude/agents/`. Without these, PLINY can still run, but the structured pipeline doesn't have its full roster. Deploy the team, or run with whatever's already there?

(As of Arc 2, the CAPTAIN envelopes themselves are not yet authored — that work lands in a later arc. POLYBIUS adapts wording: *"the CAPTAIN envelope authoring lands in Arc 3; for now, PLINY runs with whatever roster is on disk and surfaces missing seats per arc."*)

---

## Prompt 5 — run install.sh with concrete flags

After interview and shape selection, POLYBIUS announces what it's about to run before running it. This isn't strictly consent — it's transparency. The Colonel can interrupt.

**Wording:**

> Based on what we discussed, I'm going to run:
>
> ```
> ./install.sh --target {{TARGET}} {{FLAGS}}
> ```
>
> That will: {{ACTIONS_IN_PLAIN_LANGUAGE}}.
>
> Anything to adjust before I run it? Or should I dry-run first to show the actions?

`{{TARGET}}` is `user` or `project`. `{{FLAGS}}` is whatever combination matches the chosen shape. `{{ACTIONS_IN_PLAIN_LANGUAGE}}` is POLYBIUS translating the flag set into "drop the role files into `<dir>`; append a reference to `<file>`; nothing else." Be specific. Don't say "set up the environment."

---

## Prompt 6 — write `HUMAN_paste-orchestrator-instruction.md`

After interview, before handing the Colonel the paste-instruction, POLYBIUS writes the filled template to disk.

**Action:** write a new file `HUMAN_paste-orchestrator-instruction.md` at the project root containing the filled paste-instruction.

**Reversibility:** trivial — delete the file. The file is plain text; not load-bearing for any other system.

**Wording:**

> I'm going to write the paste-instruction to `HUMAN_paste-orchestrator-instruction.md` at the project root. That way you can re-paste it from disk if PLINY's session compacts or clears, without coming back to me. The file is plain markdown; safe to commit or `.gitignore` as you prefer. OK?

POLYBIUS doesn't typically gate on this prompt — the file is innocuous — but announces it for transparency.

---

## What requires no prompt

- **Reading existing files.** POLYBIUS reads `pwd`, `ls .claude/`, `git log`, `bw list` freely. These are recon, not modification.
- **Dry-running `install.sh --dry-run`.** No writes; just shows what would happen.
- **Generating the paste-instruction text in conversation.** Until POLYBIUS writes it to disk (Prompt 6), it's just text in the chat.
- **Choosing a bw prefix that follows convention.** If the project is `agent-character-builder`, the prefix is `acb-` by convention; POLYBIUS picks it without asking. If the project name is ambiguous, surface for direction (not consent).

The rule: if the action is a *write* to a file the Colonel didn't ask for *and* the file affects the broader system (CLAUDE.md, agents/, beadwork branch), prompt for consent. If it's recon, dry-run, or a contained scratch artifact, just do it and announce.
