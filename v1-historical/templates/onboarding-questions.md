<!--
ARCHIVED — v1 onboarding interview floor.

This file is preserved for historical reference only. It uses v1 terminology
("Colonel" as the title for the human served by the system) throughout the
question rationale, which v2 corrects: PRINCIPAL is the human's descriptive
role; COLONEL is reserved as a future high-autonomy agent rank. The seven
floor questions and their per-question rationale shape are preserved in v2
— the voice changes; the structure does not.

Canonical successor: ../../templates/onboarding-questions.md (v2 —
re-authored in Arc 6 of agent-substrate).

Spec authority: user-beadwork/plans/three-role-recursive-architecture.md
Empirical signal that motivated v2: user-beadwork u--7yg.20.

Do not deploy this file. Do not use it as voice reference.
-->

# Onboarding interview questions

The questions MAJOR_POLYBIUS asks during the interview phase of onboarding (§4 step 2), with the rationale behind each. A future POLYBIUS reading this template should understand *why* each question is asked, so that it can adapt phrasing to the conversation without dropping the question's actual purpose.

These are not a script. POLYBIUS reads the conversation and asks what the conversation needs. The list below is the floor: every onboarding interview should have answered these by the time POLYBIUS proposes a deployment shape.

---

## Floor questions

### 1. What project are you working on?

**Asks for:** the project name; the path to the project directory; whether the directory already exists or needs creating.

**Why:** POLYBIUS needs to know where to deploy. Project-tier installs target `<project>/.claude/`; user-tier installs target `~/.claude/`. The project name also becomes the bw prefix root and shows up in the paste-instruction (`{{PROJECT_NAME}}`).

**Adapt:** if the Colonel opened POLYBIUS already inside a project directory, infer the project from `pwd` and confirm rather than re-asking from scratch.

---

### 2. What's the first thing you want to do in this project?

**Asks for:** the immediate session intent — what the Colonel actually wants to ship today, in one or two sentences.

**Why:** this becomes `{{SESSION_INTENT}}` in the paste-instruction. It primes MAJOR_PLINY to begin work already oriented rather than starting from a generic orchestrator template. A vague answer here produces a vague PLINY activation; press for specificity.

**Adapt:** if the Colonel doesn't yet know — that's fine, surface it as such ("we'll start PLINY with intent 'orient and recommend first arc' and refine once you've seen the project state"). Don't manufacture false specificity.

---

### 3. Is this a brand-new project or one with existing work?

**Asks for:** whether there's already a `.claude/` directory, prior beadwork, prior CLAUDE.md, prior commits the team has made.

**Why:** returning-user onboarding is shorter — POLYBIUS reads existing state rather than installing fresh. Different paths through the flow:

- Brand-new → full install: drop role files, optional CLAUDE.md modification, `bw init`, deploy CAPTAINs (when available), generate paste-instruction.
- Returning → audit-and-resume: read existing role files, read existing bw state, generate fresh paste-instruction reflecting current intent.

**Adapt:** check `pwd && ls -la .claude/ 2>/dev/null && git log --oneline -5 2>/dev/null` early in the conversation to skip asking what you can verify directly.

---

### 4. Are you comfortable with modifications to your user-level `~/.claude/CLAUDE.md`?

**Asks for:** explicit consent (or refusal) for the deployment shape that touches the user's home directory.

**Why:** this is the single most sensitive action POLYBIUS can take. Per `u--7yg.13` Colonel emphasis, some users reasonably refuse any modification of their home `~/.claude/CLAUDE.md` for privacy or control reasons. The system supports a "sub-projects-only" deployment shape precisely for that case. Asking explicitly — rather than inferring from silence — is the consent floor.

**Adapt:** lead with the trade-offs, not the question. The Colonel may not know the consequences of either choice without context. Phrase the trade-offs from `templates/consent-prompts.md` first, then ask.

---

### 5. Which deployment shape fits your situation?

**Asks for:** a choice among the three shapes documented in spec §8:

- **(a) project-only** — conservative; touches `<project>/.claude/` only. Recommended for first-time users.
- **(b) user-level + project-level** — full deployment; modifies `~/.claude/CLAUDE.md` to reference user-tier POLYBIUS. Requires question 4's explicit consent.
- **(c) sub-projects-only** — for users who refused question 4. Substitutes sub-projects for user-tier capabilities.

**Why:** the three shapes aren't equivalent. They differ in scope, in surface modified, in whether user-tier coordination is available. POLYBIUS proposes the conservative default ((a) project-only) for first-time users, but the Colonel makes the call.

**Adapt:** if question 4 was refused, (b) is off the table — don't re-offer it. Go directly between (a) and (c). If the Colonel is clearly running across many projects already, (a) is undersized for them — say so and recommend (b).

---

### 6. Is `bw` already installed and initialized for this project?

**Asks for:** the state of beadwork in the target directory.

**Why:** `bw init --prefix <project>-` is part of the install flow. If beadwork is already there, POLYBIUS reads it rather than re-initializing. If it isn't, POLYBIUS surfaces the install step and runs it as part of onboarding.

**Adapt:** check `which bw && bw list 2>&1 | head -5` directly rather than asking when you can verify. Save the conversation budget for things you can't determine yourself.

---

### 7. Anything POLYBIUS should know that I haven't asked about?

**Asks for:** any constraint, preference, or context that didn't fit the floor questions — e.g., existing tooling, project conventions, collaborators, deadline pressure, prior bad experiences with similar tools.

**Why:** the floor questions are minimum coverage. The Colonel often holds context POLYBIUS won't think to ask for. Asking explicitly creates an opening rather than relying on the Colonel to volunteer.

**Adapt:** drop this question if the conversation has already covered the same ground organically. Don't ask formalities for their own sake.

---

## What POLYBIUS does not ask

- **Permission for technical-tier decisions.** Per `u--7yg.1`, routing every technical call up to the Colonel is router-antipattern. POLYBIUS chooses bw prefix conventions, file paths, idempotency mechanisms, dispatch order — these are POLYBIUS's seat to decide.
- **Permission for non-sensitive actions.** Reading existing files, dry-running install.sh, listing bw tickets — these need no consent. Modifying the home directory, writing new files into the project tree, and deploying CAPTAINs into `.claude/agents/` *do*.

The discipline: ask for direction (where are we going? what does success look like?) and consent on sensitive actions. Do not ask for consent on calls POLYBIUS is competent to make.

---

## After the interview

POLYBIUS knows:

- Project name and directory
- Session intent
- Brand-new vs returning
- Whether `~/.claude/CLAUDE.md` modification is permitted
- Which deployment shape was chosen
- Beadwork state
- Any extra context the Colonel surfaced

POLYBIUS now proceeds to §4 step 3: propose the deployment plan back to the Colonel as a single coherent paragraph (not as a series of sub-questions), confirm, run install.sh with the right flags, and continue.
