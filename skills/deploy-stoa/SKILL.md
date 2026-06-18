---
name: deploy-stoa
description: "Agent-facing router for getting the Stoa substrate onto a TARGET PROJECT. Its load-bearing job is DETECT-then-BRANCH: probe whether a Stoa is already deployed at the target and route accordingly — FRESH (no .claude/MAJOR_POLYBIUS*.md present) -> guided install via install-stoa / install.sh --target project; EXISTING (already deployed) -> the UPDATE path (check-substrate-updates: read-only check.sh -> consent-gated apply.sh -> revert.sh net), never a blind install.sh re-run. Routes to bootstrap-stoa when git/bw prerequisites are missing. Use when an agent is told 'install the stoa into <project>', 'update the stoa here', 'get the stoa current in this repo', 'is the stoa installed here', 'add the stoa to <project>', or any deploy/update-into-a-project request. Re-running install.sh over an existing deployment is the silent-overwrite footgun this skill exists to prevent."
author: Denson Smith
---

# deploy-stoa — put the Stoa onto a project, or bring an existing one current

**Agent-execution shape.** An agent (you) is told to get the Stoa onto, or current in, a target project — the executor is *always* an agent, supervised by a human who approves the consent gates. You drive; surface the branch you take and each consent gate to your supervising human. **Your ONE load-bearing job is the detect-then-branch** — everything else routes to an existing skill:

- a Stoa is **NOT** deployed at the target → **FRESH install** (Step 3).
- a Stoa **IS** already deployed → **UPDATE** via `check-substrate-updates` (Step 4) — *never* a blind `install.sh` re-run.
- git or bw prerequisites are missing → **`bootstrap-stoa` first** (Step 2 note).

Why the branch matters: re-running `install.sh` over an existing deployment overwrites any local edits to the standard seats and can't show you what it changed before it changes it. The update skill reconciles drift with per-file consent + a revert net. Picking the wrong branch is the silent-overwrite footgun this skill prevents.

> **Dependency citation.** `bw` (beadwork) is **jallum's** tool — https://github.com/jallum/beadwork. The Stoa is built *on* it. The Stoa substrate + this skill are Denson Smith's (MIT) — metadata, not something to recite in install narration.

---

## Step 1 — locate + sanity-check the target

Get the target project path (absolute, or relative to where the session opened). Confirm it's a git repo — the deployed `.claude/` and the optional `CLAUDE.md` reference are far easier to track + roll back under version control:

```bash
TARGET="<path>"                       # the project to deploy into
git -C "$TARGET" rev-parse --git-dir >/dev/null 2>&1 && echo "GIT REPO: yes" || echo "GIT REPO: no"
```

If it isn't a git repo, offer to `git init` first (recommended) or proceed without — don't hard-block, but surface the trade-off.

(For **user-tier** "set up the Stoa on this machine from scratch" — not a project — this is the wrong skill; use `bootstrap-stoa`.)

---

## Step 2 — DETECT: is a Stoa already deployed here?

The decisive probe. The MAJOR role files are the core of any deployment, so their presence is the signal:

```bash
ls "$TARGET"/.claude/MAJOR_POLYBIUS*.md "$TARGET"/.claude/MAJOR_PLINY*.md 2>/dev/null
```

- **Any match → EXISTING Stoa → go to Step 4 (UPDATE).**
- **No match → FRESH → go to Step 3 (INSTALL).**

The `*` wildcard is load-bearing: project-tier deploys the MAJORs **unsuffixed** (`MAJOR_POLYBIUS.md`), sub-project tier deploys them **suffixed** (`MAJOR_POLYBIUS_<slug>.md`); the glob catches both. A bare `.claude/` with no MAJOR role files (e.g. a project that only has Claude Code settings) correctly reads as FRESH.

**Prerequisite probe (either branch):**

```bash
git --version >/dev/null 2>&1 && echo "GIT ok"  || echo "GIT MISSING"
bw  --version >/dev/null 2>&1 && echo "BW ok"   || echo "BW MISSING"
```

If git or `bw` is missing, **route to `bootstrap-stoa`** to install the prerequisites first, then come back here. Do not try to install git/bw from this skill.

---

## Step 3 — FRESH install path (no Stoa at the target)

You (the agent) drive the installer directly. **Dry-run first, always** — show the plan before any real write, even when told "just do it":

```bash
# 1) show the plan
bash substrate/install.sh --target project --project-dir "$TARGET" --dry-run
# 2) on confirmation, the real run (drop --dry-run).
bash substrate/install.sh --target project --project-dir "$TARGET" [--modify-claude-md]
```

`--modify-claude-md` is the one consent-bearing flag — it appends a marker-bounded POLYBIUS auto-load block to `<TARGET>/CLAUDE.md` (it `.bak`s first). Surface it to your supervising human and add it only on an explicit yes.

For a **sub-project** under an already-deployed parent: `--target subproject --parent-dir <parent> --subproject <slug>` (see `install.sh --help`).

After a real install, verify: the MAJORs + CAPTAIN envelopes exist at `<TARGET>/.claude/`, the `CLAUDE.md` reference landed (if requested), and no obsolete-file warnings went unaddressed.

`install-stoa` carries the fuller reference detail (tier descriptions, the literal `--modify-claude-md` block, the smoke test) if you want it — but the install itself is the command above, run by you.

---

## Step 4 — EXISTING update path (a Stoa is already deployed)

This is an **UPDATE, not a fresh install.** Re-running `install.sh` here would overwrite any local edits to the standard seats and gives you no diff to consent to. Use `check-substrate-updates` instead — read-only scan, then consent-gated apply, with a revert net.

```bash
# 1) READ-ONLY: what would change? (DRIFTED / MISSING / OBSOLETE + uncommitted-.claude/ count)
bash substrate/skills/check-substrate-updates/check.sh --workspace "$TARGET"

# 2) Surface the verdict to the PRINCIPAL. Then consent-gated apply (per-file diff + consent):
bash substrate/skills/check-substrate-updates/apply.sh --workspace "$TARGET"

# 3) If the apply went wrong, undo the most recent one:
bash substrate/skills/check-substrate-updates/revert.sh --workspace "$TARGET"
```

Read the categories before applying:
- **MISSING** — source-side additions the deployment hasn't picked up (e.g. new seats like CHIRON/HAMILTON, new skills). Usually the point of an update.
- **DRIFTED** — a deployed file differs from source-after-substitutions. Could be an upstream advance, a local edit, or both — `apply.sh` shows the diff so the PRINCIPAL decides per file.
- **OBSOLETE** — a workspace file at a substrate-deployable path no longer in source. **Eyeball these for genuine local customizations** (a custom `*_<slug>` agent the project authored has no source counterpart and must NOT be removed) — `apply.sh`'s per-file consent is what protects them.

`apply.sh` has a git pre-commit safety net and warns when role files (MAJOR_*/CAPTAIN_*) are touched. Note: deployed agent defs are read at session start, so any running agent in the target picks up the changes only on its next session.

---

## Hard rules

1. **Never skip the detect-then-branch (Step 2).** Existing deployment + blind `install.sh` re-run = the silent-overwrite footgun. The whole reason this skill exists is to route existing → the update path.
2. **Existing → `check-substrate-updates` (consent + revert), not `install.sh`.** `install.sh` is the deploy mechanism (fresh / re-deploy); the update skill is for reconciling drift with consent and a diff.
3. **Fresh → dry-run `install.sh` first, always** — show the plan before the real write, even on "just do it."
4. **`--modify-claude-md` only with explicit consent** — it's the one flag that writes outside `.claude/`.
5. **git/bw missing → `bootstrap-stoa` first.** Don't install prerequisites from this skill.
6. **OBSOLETE ≠ delete-on-sight.** A genuine local customization with no source counterpart is protected by per-file consent — never auto-prune it.
7. **Voice:** don't call the human "the user" — PRINCIPAL, or their name once captured. Credit `bw` to jallum where provenance comes up; don't credit Denson Smith in install narration (metadata only).

## Cross-references

- `skills/install-stoa/SKILL.md` — the guided FRESH-install dialog (Step 3 routes here for a human-co-driven install).
- `substrate/skills/check-substrate-updates/` (`check.sh` / `apply.sh` / `revert.sh`) — the UPDATE path (Step 4 routes here).
- `skills/bootstrap-stoa/SKILL.md` — installs git + bw prerequisites and does user-tier zero-to-running (Step 2 routes here when prerequisites are missing).
- `substrate/install.sh` — the mechanical installer (`--help` for the canonical flag set + all three tiers).
- `skills/stoa-intro/SKILL.md` — the visual tour, for an exploratory human who wants to understand the Stoa before deploying.
