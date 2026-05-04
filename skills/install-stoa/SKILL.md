---
name: install-stoa
description: Guided walkthrough of installing The Stoa substrate onto a target project (or user-tier, or sub-project tier). Wraps substrate/install.sh with a question-driven dialog and dry-run-first discipline.
---

# install-stoa — guided substrate install

## What this skill is for

You are walking the PRINCIPAL through a real install of the three-role substrate. The mechanics live in `substrate/install.sh`; your job is the dialog around it — pick the right tier, confirm the right target path, get explicit consent for the file modifications that matter, dry-run before any real write, and surface what the PRINCIPAL needs to do next once the install lands.

This skill is **not a wrapper that runs install.sh in one shot.** It is a procedure with consent gates. The PRINCIPAL can decline any individual step and the install pauses there. If they "just do it," the dry-run beat still runs — that discipline is load-bearing (consent prompts §5; case study §3.5 on the trust-distribution patterns).

The signals that this skill is the right thing to load:
- The PRINCIPAL said *"install this on my project,"* *"deploy the substrate to X,"* *"set this up for me."*
- The entry-point skill (`SKILL.md` at repo root) routed them here.
- The PRINCIPAL is past exploration and has a deploy target in mind.

If they're still exploratory, route back to the entry-point skill. If they want to fork rather than install, name that this skill is for installs and ask whether they want the case study instead.

---

## Pre-flight before the dialog starts

Before the first question, run the checks that determine whether the install can succeed at all. If a pre-flight fails, surface the blocker and stop — do not proceed with the dialog and then dead-end at the install step.

### Beat 1 — verify `bw` is installed

The substrate uses beadworks (`bw`) as durable substrate. The install script does not initialize `bw` (POLYBIUS does that interactively after install), but the deployed substrate is unusable without `bw` on the PATH.

Run:

```
bw --version
```

If it returns a version, continue. If it returns "command not found" or similar:

> The Stoa substrate uses beadworks (`bw`) as its durable message bus and memory layer. I don't see `bw` on your PATH. Before we can usefully deploy, you'll need to install `bw` from its own repo — that lives separately from The Stoa. I'm going to pause here; once `bw --version` returns a version on your machine, come back and we'll continue. Want me to surface the bw repo URL, or do you have it?

**Do not try to install `bw` from this skill.** `bw` lives in a separate repo with its own install path. Naming it as a prerequisite is correct; trying to wrap it is out of scope.

### Beat 2 — verify the git working tree (if installing into an existing project)

If the install target is a project the PRINCIPAL is actively working in, an in-flight working tree means `install.sh --modify-claude-md` will mix substrate changes with the PRINCIPAL's open work in the next commit.

Run (against the proposed target dir):

```
cd <target> && git status --porcelain
```

If clean, continue. If dirty:

> The target project has uncommitted changes (`git status` shows working-tree modifications). Installing the substrate in a dirty tree is fine if you intend to commit the substrate alongside whatever's in flight, but it's worth flagging — most PRINCIPALs prefer a clean tree first so the install commit is self-contained. Want to land your in-flight changes first, or proceed with a mixed commit?

If the PRINCIPAL says proceed, proceed. If they want to commit first, pause — they'll come back when the tree is clean.

(Skip this beat for `--target user` — the user-tier `~/.claude/` may not be a git repo at all, and that's normal.)

---

## The dialog — pick tier, target path, and flags

These three questions in this order. Don't ask everything at once; the PRINCIPAL's first answer often constrains the next question.

### Beat 3 — ask: which tier?

Before phrasing the question, **read the actual installer's help output** so the descriptions match what `install.sh` will accept:

```
substrate/install.sh --help
```

The three tiers (as of current substrate):

- **`user`** — drops the role files + 10 CAPTAIN envelopes + templates + skills into `~/.claude/`. Available across all your projects on this machine. Optionally appends a marker-bounded reference to `~/.claude/CLAUDE.md` so POLYBIUS auto-loads in every fresh Claude Code session.
- **`project`** — drops everything into `<project>/.claude/` instead. CAPTAINs are suffixed with the project slug (e.g., `CAPTAIN_DAEDALUS_widget_builder.md`) so they don't collide with user-tier or other-project CAPTAINs. Optionally appends a reference to `<project>/CLAUDE.md`.
- **`subproject`** — recursive case (Arc 14 mechanism). Deploys the substrate under `<parent>/<subproject>/` with both MAJORs and all 10 CAPTAINs suffixed. Sub-project shares the parent's git repo and `bw`. Does not modify any `CLAUDE.md`. The sub-project pattern is for cases where the work needs its own tools, its own domain, or its own human collaborator (case study §4 + the substrate's `MAJOR_POLYBIUS.md` §10 on sub-project trip-wires).

Phrase the choice for the PRINCIPAL with the trade-offs visible:

> Three tiers to choose from:
>
> - **user-tier** — POLYBIUS auto-loads in every Claude Code session on this machine; one set of role files for everything.
> - **project-tier** — POLYBIUS only loads in the project you deploy to; CAPTAINs are project-named so multiple projects can have their own.
> - **sub-project-tier** — recursive case; spawns a sub-team under an existing deployed project (separate human collaborator, design-pass, prototype-tier work). Probably not what you want unless you've read case study §4.
>
> First-time installs usually start with **project-tier** — lower stakes, easier to remove if you change your mind. Which fits your case?

Don't preselect. If they say "user," go to **Beat 3a** (user-tier directory choice) before Beat 4. If "project" or "sub-project," skip Beat 3a and continue to Beat 4 to get the path.

### Beat 3a — user-tier directory choice (only if `--target user`)

The user-tier chief-of-staff (POLYBIUS) operates from a "home directory" — the parent dir under which `user-beadwork` (durable memory) lives, and where you'll typically open Claude Code for cross-project work.

The install script's user-tier flow does this automatically (Arc 20: `substrate/install.sh --target user` runs detection-with-confirmation). But preview it for the PRINCIPAL so the prompt isn't a surprise.

**The flow install.sh runs:**

1. **Detection** — scans common locations for an existing `user-beadwork/` (with `.git/` and a `beadwork` orphan branch — bw's marker):
   - `~/stoa_projects/user-beadwork/`
   - `~/claude_projects/user-beadwork/`
   - `~/projects/user-beadwork/`
   - `~/Code/user-beadwork/`
2. **If exactly one found:** prompt *"Found existing user-beadwork at `<path>`. Use this? Your user-tier dir would be `<parent>`. [Y/n]"*. Y → install records that parent. N → fall through to default-prompt.
3. **If multiple found:** list all + a "create new" option; PRINCIPAL picks.
4. **If none found:** prompt *"Where do you want your user-tier directory? [default: ~/stoa_projects/]"*. Accept input or default.
5. **Scaffolding (if not using existing):** `mkdir -p <chosen-dir>` + `git init` in `<chosen-dir>/user-beadwork/` + `bw init`. Strict — never clobbers existing.
6. **Substitution:** install records the chosen path and substitutes `{{USER_TIER_DIR}}` in deployed `~/.claude/MAJOR_POLYBIUS.md` so the role file's references resolve to the actual path.

**To skip the interactive prompt** (e.g., when PRINCIPAL knows what they want):

```
substrate/install.sh --target user --user-tier-dir ~/my-chosen-dir --modify-claude-md
```

**What you (the agent) should do in this beat:**

- Surface the upcoming prompt to the PRINCIPAL: *"The install will detect any existing user-beadwork on common paths and offer to use it; if none found, it'll ask where you want your user-tier directory (default `~/stoa_projects/`). Want me to proceed with the interactive flow, or do you already know the path you want — in which case I'll pass `--user-tier-dir <path>`?"*
- If they have a specific path: pass it via `--user-tier-dir`.
- If they don't: just run the install and let the interactive flow guide them. The `Y/n` and the path prompt run on the PRINCIPAL's terminal during install.sh execution.

### Beat 4 — ask: target path (project / sub-project tiers only)

For project tier:

> Which directory? Give me the absolute path or a path relative to where you opened this Claude Code session. I'll verify it exists and is a git repo before we continue.

Verify:

```
cd <path> && git rev-parse --git-dir 2>&1
```

If it returns a `.git` reference (or `.git`), the directory is a git repo — continue. If it returns "not a git repository," surface:

> That path isn't a git repository. The substrate install doesn't strictly require git, but in practice you want it: the deployed `.claude/` and the optional `CLAUDE.md` reference are easier to track and roll back if they're under version control. Want to `git init` first, or proceed without?

For sub-project tier, ask both:

> Two paths needed: the **parent project** (must already have substrate deployed at `<parent>/.claude/`) and the **sub-project slug** (a single path-segment name like `roster-redesign`, `hypergraph-tier`, `design-pass`). The sub-project lives at `<parent>/<slug>/`.

Verify the parent exists, has `.claude/`, and the slug passes `install.sh`'s validation (no path separators, no leading dot, only `[A-Za-z0-9._-]`).

### Beat 5 — ask: `--modify-claude-md`?

The most consent-bearing flag. Walk the PRINCIPAL through what it does so the choice is informed:

> One more question. The install can append a marker-bounded reference block to your target `CLAUDE.md` so POLYBIUS auto-loads when you open Claude Code in this directory. The block looks like this:
>
> ```
> <!-- agent-substrate: POLYBIUS reference -->
> ## Chief-of-Staff (MAJOR_POLYBIUS)
>
> This environment hosts the three-role agent substrate. The Chief-of-Staff role is defined in `.claude/MAJOR_POLYBIUS.md`. When the user invokes "POLYBIUS" or "chief of staff", read that file and assume the role.
> ```
>
> It's marker-bounded, so removing it later is mechanical (find the marker, delete the block). The install also makes a `.bak` of your existing `CLAUDE.md` before any append. **Recommended: yes** — the auto-load is the whole point of the substrate-on-disk reference.
>
> If you'd rather not modify `CLAUDE.md`, the role files still install to `.claude/` and you'd invoke POLYBIUS by name in fresh sessions. Append the reference, or skip?

If the PRINCIPAL says skip, drop the `--modify-claude-md` flag from the install. If they say yes, set it. If they want to see the literal block first, run a dry-run (Beat 6) and show them the actual block that would be written before asking again.

(Skip this beat for sub-project tier — `install.sh` rejects `--modify-claude-md` in sub-project mode, and the deployed sub-project deliberately doesn't get its own `CLAUDE.md`.)

---

## Beat 6 — dry-run first, always

Before the real install, dry-run with the chosen flags:

```
substrate/install.sh --target <tier> [tier-flags] [--modify-claude-md] --dry-run
```

Show the PRINCIPAL the planned actions — every file that would be deployed, the slug substitution, whether `CLAUDE.md` would be modified, the literal block contents if so, and any obsolete-file warnings. Then ask:

> That's the plan. Anything to adjust? If it looks right, I'll re-run the same command without `--dry-run` to actually deploy.

**The dry-run beat is non-negotiable.** Even if the PRINCIPAL says "just do it," the dry-run still runs — the cost is one extra command; the cost of an unintended modification is the rebuild. The PRINCIPAL can decline to read the dry-run output if they want to, but they cannot decline that the dry-run runs.

Once they confirm, drop `--dry-run` and run for real.

---

## Beat 7 — verify after install

After the real install completes (`install.sh: done (applied)`), confirm the deploy actually wrote what was planned. Three quick checks:

1. **Files exist at expected paths.** `ls <DEST>/MAJOR_POLYBIUS*.md <DEST>/MAJOR_PLINY*.md <DEST>/agents/CAPTAIN_*.md`. Should list 2 MAJORs + 10 CAPTAINs (plus templates and skills if those weren't disabled). For sub-project tier, the MAJORs should be suffixed.
2. **`CLAUDE.md` reference landed (if `--modify-claude-md`).** `grep -F "agent-substrate: POLYBIUS reference" <CLAUDE_MD>`. Should return one match. If a `.bak` was created, surface that to the PRINCIPAL — that's their rollback.
3. **No stale files lingering.** `install.sh` warns about obsolete files at the destination (renamed CAPTAINs, removed templates). If the warn block fired, surface it to the PRINCIPAL with the option to re-run with `--prune-obsolete` if they want auto-removal.

Report concretely:

> Install landed. Deployed at `<path>`: 2 MAJORs (POLYBIUS + PLINY), 10 CAPTAINs (DAEDALUS through CAPTAIN_ZENO), 3 templates, 1 LIEUTENANT skill (agent-author). `CLAUDE.md` reference appended; backup at `<CLAUDE_MD>.bak`. No obsolete files detected.

---

## Beat 8 — optional smoke test

The deploy is mechanical; whether POLYBIUS loads cleanly in a real session is the actual test. Offer the smoke test, but don't force it:

> Want to smoke-test the deploy? Open a new Claude Code session in `<deploy-target>`, invoke POLYBIUS by name (or, if you appended the `CLAUDE.md` reference, just type "POLYBIUS"), and verify the chief-of-staff role file loads cleanly (POLYBIUS should introduce itself, ask your name if first-time, and offer to walk through onboarding). If anything doesn't load — wrong file, generic response, missing `bw` reference — come back here and we'll debug.

If they say yes, walk them through:

1. Open a new terminal in `<deploy-target>`.
2. Run `claude`.
3. Say `POLYBIUS` or `chief of staff` (auto-load case) or paste `Read .claude/MAJOR_POLYBIUS.md and assume the role.` (no-CLAUDE.md case).
4. Confirm POLYBIUS responds in role.

If they decline, that's fine — leave them with the `next steps` block `install.sh` printed and stand down.

---

## What you must NOT do

- **Do not run install without `--dry-run` first.** Every install gets a dry-run beat. No exceptions.
- **Do not run with `--modify-claude-md` without explicit consent.** Default-off in conversation; flip on only after the PRINCIPAL says yes.
- **Do not proceed if `bw` isn't installed.** Surface the blocker, name `bw` as a prerequisite, stop. Do not try to install `bw` from this skill.
- **Do not try to install `bw` itself.** `bw` lives in a separate repo with its own install path. Out of scope here.
- **Do not modify the PRINCIPAL's git config or any system files.** The install only writes under `<DEST>/.claude/` and (with consent) one `CLAUDE.md`. Anything beyond that is out of scope.
- **Do not skip the dry-run beat even if the PRINCIPAL asks.** "Just do it" doesn't override the discipline. The dry-run runs; reading the output is optional; running for real without it isn't.
- **Do not auto-initialize `bw` after install.** `install.sh` deliberately doesn't run `bw init`; that's POLYBIUS's job during onboarding (consent prompt §3 in `substrate/templates/consent-prompts.md`). Don't pre-empt POLYBIUS's interview.
- **Do not refer to the human as "the user."** PRINCIPAL or, once a name is captured, the name. Voice discipline (`u--7yg.20`).

---

## Reference paths

- The mechanical installer: `substrate/install.sh` (run with `--help` for the canonical flag set).
- Onboarding scenarios that walk POLYBIUS through the post-install dialog: `substrate/ONBOARDING.md` (Scenarios 1-5; Scenarios 1, 3, 5 are the install-relevant tier patterns).
- Consent prompt templates: `substrate/templates/consent-prompts.md` (Prompts 1, 2, 3, 4, 5, 7 cover the dialog beats above; Prompt 6 covers the post-install paste-instruction; Prompt 8 covers polling-cron consent during ongoing engagements).
- Architecture spec: `user-beadwork/plans/three-role-recursive-architecture.md` (v2). Outside this repo; the spec is authoritative if any wording in this skill conflicts with it.
