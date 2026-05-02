# Arc Z build directive — consolidate agent-substrate + agent-character-builder into the-stoa

**Audience:** the fresh Claude Code session opened to build Arc Z deliverables.
**Authored by:** user-tier Chief-of-Staff (POLYBIUS-equivalent) + the PRINCIPAL (Denson Smith).
**Status:** active directive.
**Builds on:** Arcs 1-8 of agent-substrate (last commit `52b08ae`); agent-character-builder commit `da5520d`.
**Note:** "Arc Z" naming because this is a pre-Arc 9 consolidation arc that resets the substrate-as-its-own-repo assumption. After Arc Z, the renumbered Arc 9-13 sequence dispatches against the unified repo.

**You are MAJOR_PLINY for the Arc Z engagement.** The user-tier Chief-of-Staff (POLYBIUS-equivalent) wrote this directive; you receive it and execute. Per planning v2 §4, MAJOR_PLINY is the orchestrator role.

Read `MAJOR_PLINY.md` (this directive's home repo, `~/claude_projects/agent-substrate/MAJOR_PLINY.md`) and assume the orchestrator role.

**Your one job for this engagement:** create a unified `the-stoa` private GitHub repo containing both `agent-substrate` (substrate canonical) and `agent-character-builder` (The Stoa app), preserving git history from both source repos. Archive the source repos with deprecation notes. Update internal references that pointed at the old paths. Then return cleanly.

**Open Claude Code in `~/claude_projects/agent-substrate/`** (where this directive lives) — operate cross-repo from there.

---

## Architectural rationale (decided 2026-05-02)

The architecture has localhost-only deployment posture for the foreseeable future (per PRINCIPAL direction tracked in user-beadwork). Two separate repos for substrate canonical + Stoa app added cross-repo coordination overhead with no deployment-side benefit. Unified repo:

- The Stoa is *the editor* for canonical agents; canonical-and-editor in the same repo matches that relationship
- gen-data adapter (Arc 10) reads from same-repo paths, no env var or submodule
- Single git history; coordinated commits
- Aligns with planning v2 §11 source-of-truth model

Consolidation **before** the smaller Arc 9-13 sequence dispatches. Cost is mechanical (file moves + git subtree merges); cost of consolidating later is "rewrite adapter against new paths" + cognitive overhead of "current arc was built against now-deprecated structure."

---

## Read first

1. **Planning v2** at `~/claude_projects/user-beadwork/plans/three-role-recursive-architecture.md` — §11 (The Stoa) describes the source-of-truth model that motivates consolidation. §14 currently lists Arc 9 = "The Stoa data model + display alignment" — this Arc Z precedes that and changes the working repo to `the-stoa`.

2. **agent-substrate current state:**
   - `~/claude_projects/agent-substrate/`
   - Contents at root: `MAJOR_POLYBIUS.md`, `MAJOR_PLINY.md`, 10 `CAPTAIN_*.md`, `templates/`, `install.sh`, `README.md`, `arcs/` (1-9 + Z directives), `v1-historical/` (archived role files)

3. **agent-character-builder current state:**
   - `~/claude_projects/agent-character-builder/`
   - Vite/React app; 4 commits ahead of where Arc 8 deployed v2 substrate
   - `.claude/` is gitignored (per `u--7yg.21`); the deployed substrate isn't tracked in this project's git history; only `CLAUDE.md` is

4. **`u--7yg.21`** — `.claude/-gitignored` discipline note; relevant for understanding what's tracked vs not in agent-character-builder

---

## Deliverables

### 1. Create new private GitHub repo: `the-stoa`

```bash
gh repo create the-stoa --private --description "The Stoa — unified agent substrate + visualization/edit web app (localhost-only)"
```

### 2. Set up local working copy with subtree-merged history

```bash
cd ~/claude_projects
git clone https://github.com/denson/the-stoa.git
cd the-stoa
git checkout -b main
echo "# the-stoa" > README.md
git add README.md
git commit -m "Initial commit"
git push -u origin main
```

### 3. Subtree-merge both source repos to preserve history

```bash
# agent-substrate → substrate/
git subtree add --prefix=substrate ../agent-substrate main

# agent-character-builder → app/
git subtree add --prefix=app ../agent-character-builder main
```

**Verify:** after each subtree add, `git log` should show the source repo's commits prefixed under their respective subdirectories. History preserved.

### 4. Final layout

```
the-stoa/
├── README.md                    # describes the unified repo
├── substrate/                   # was agent-substrate
│   ├── MAJOR_POLYBIUS.md
│   ├── MAJOR_PLINY.md
│   ├── CAPTAIN_*.md (10 files)
│   ├── templates/
│   ├── install.sh
│   ├── arcs/                    # arc directives history
│   ├── v1-historical/
│   └── README.md                # substrate-internal README; rename or merge into top-level
└── app/                         # was agent-character-builder
    ├── src/
    ├── package.json
    ├── vite.config.ts
    ├── index.html
    ├── CLAUDE.md                # the project's CLAUDE.md (substrate-deployed reference)
    ├── .claude/                 # deployed substrate; gitignored, regenerable via install.sh
    └── README.md                # app-internal README; rename or merge
```

### 5. Update internal references

Anywhere in the new repo that referenced the old separate-repos paths:

- **`substrate/install.sh`** — reads templates from a relative path; check that it still resolves correctly when the repo is at `~/claude_projects/the-stoa/substrate/` instead of `~/claude_projects/agent-substrate/`. If it uses `$0`-relative or `dirname` style path resolution, it should still work; if it has hardcoded paths, update.
- **`substrate/arcs/*.md`** — directive files reference `agent-substrate` and `agent-character-builder` as separate repos. **Don't retrofit historical directives** (per Arc 6's discipline that historical artifacts stay as records). New directives use the-stoa-relative paths.
- **`substrate/README.md`** — likely needs a header note ("This was agent-substrate; now part of the-stoa") OR it should be merged into the new top-level README.
- **`app/README.md`** — same.
- **`app/CLAUDE.md`** — references `.claude/MAJOR_POLYBIUS.md`. That path is still correct relative to `app/CLAUDE.md` since `.claude/` lives inside `app/` after consolidation.

### 6. New top-level README

A unified README explaining:
- What the-stoa is (substrate + The Stoa app, unified)
- Layout (substrate/, app/)
- How to use install.sh (still in substrate/install.sh; runs against project-tier targets)
- How to run The Stoa app (cd app/; npm run dev)
- Localhost-only deployment posture
- Pointer to user-beadwork for canonical planning artifacts

### 7. Smoke tests

After consolidation:
- **Substrate:** `cd substrate/ && bash install.sh --help` — verify install.sh still loads + shows help
- **Substrate dry-run:** `cd substrate/ && bash install.sh --target project --project-dir /tmp/test-stoa-z --modify-claude-md --dry-run` — verify install plan looks right (templates path resolves; CAPTAIN naming derives correctly; etc.)
- **App:** `cd app/ && npm install && npm run dev` — verify Vite starts; verify HTTP 200 on /, /src/main.tsx, etc.; verify the React app continues to function

If any smoke test fails, surface to the PRINCIPAL before committing.

### 8. Archive source repos

For each of `agent-substrate` and `agent-character-builder`:

- Add a top-level `ARCHIVED.md` file:
  ```markdown
  # ARCHIVED — superseded by the-stoa
  
  This repo was consolidated into [the-stoa](https://github.com/denson/the-stoa) as of 2026-05-02 (planning v2 + Arc Z). The contents live at:
  
  - `agent-substrate` → `the-stoa/substrate/`
  - `agent-character-builder` → `the-stoa/app/`
  
  Git history preserved via `git subtree`. New work happens in the-stoa.
  
  Local working copies (`~/claude_projects/agent-substrate` and `~/claude_projects/agent-character-builder`) can be removed; the GitHub repos stay as historical record.
  ```
- Commit + push the ARCHIVED.md to each source repo
- (Optional) On GitHub, archive the repo via `gh repo archive denso/agent-substrate` and `gh repo archive denso/agent-character-builder` (this marks them read-only)

### 9. user-beadwork update

`user-beadwork/plans/three-role-recursive-architecture.md` references `agent-substrate` and `agent-character-builder` as separate repos throughout. Update §11 (The Stoa) and §14 (Arc sequence) to reflect the consolidated `the-stoa` reality. Don't rewrite the whole doc — surgical edits to the affected sections. Commit + push to user-beadwork main.

### 10. Renumber arc sequence in planning v2

§14 in user-beadwork's planning doc currently lists Arc 9 = "The Stoa data model + display alignment." Per the smaller-chunks decision (replacing the original mega-Arc-9 plan with 5 smaller arcs):

- Arc 9: TypeScript types + data model
- Arc 10: gen-data adapter (with Zod schema validation)
- Arc 11: sample data wiring
- Arc 12: display updates (v2 rank ladder + PRINCIPAL framework)
- Arc 13: Vitest scaffold + smoke test
- Arc 14: sub-project spawning (was Arc 10)

Update §14 to reflect this. The original Arc 10-13 numbering shifts down.

---

## Definition of done

- `the-stoa` private GitHub repo created
- `agent-substrate` history merged into `the-stoa/substrate/` via subtree
- `agent-character-builder` history merged into `the-stoa/app/` via subtree
- Top-level README documents the unified repo
- All three smoke tests pass (substrate install.sh --help, install.sh --dry-run, app npm run dev)
- Both source repos have `ARCHIVED.md` with deprecation notes; pushed
- (Optional) Source repos archived on GitHub
- user-beadwork's planning v2 §11 + §14 updated to reflect consolidation + arc renumbering
- All committed + pushed (`the-stoa` main + `user-beadwork` main)
- bw beadwork not yet initialized in the-stoa (defer to first arc that operates there — Arc 9)

---

## Out of scope

- **Arc 9-13 work** — happens after Arc Z; against the unified repo
- **Sub-project spawning** — Arc 14
- **Updating individual `u--7yg.*` ticket descriptions in user-beadwork** that reference the old repo names. Old references stay as historical record. Future tickets use new names.
- **agent-team-team and other downstream projects** that have substrate deployed via install.sh — they don't need to know about the consolidation; they just continue using their `.claude/` deploys. Future install.sh runs come from `the-stoa/substrate/install.sh` instead of `agent-substrate/install.sh`.
- **Local working copy cleanup** of `~/claude_projects/agent-substrate/` and `~/claude_projects/agent-character-builder/` — the PRINCIPAL can remove these manually after verifying the-stoa works; not Arc Z's job to delete.

---

## Voice discipline

Less load-bearing here (mostly mechanical work). The new top-level README and ARCHIVED.md files should use v2 voice (PRINCIPAL framework; HUMAN/MAJOR/CAPTAIN/LIEUTENANT ranks where relevant). Don't introduce reflexive Colonel terminology.

---

## Beadwork

agent-substrate beadwork (`as-` prefix) is in agent-substrate's `beadwork` branch. After subtree-merging into the-stoa, that history goes with it (under `substrate/`'s git history). bw operations against the-stoa's beadwork aren't initialized yet — defer to the first arc that operates in the-stoa (Arc 9).

For Arc Z's tracking: file the epic in agent-substrate's existing bw before consolidation:

```bash
cd ~/claude_projects/agent-substrate
bw create "[EPIC] Arc Z — consolidate agent-substrate + agent-character-builder into the-stoa" -t epic -p 1
```

File children for each major step. Close as you go. Push agent-substrate's beadwork branch after Arc Z completes (preserves the record in source-repo history).

---

## Discipline

- HITL default (planning v2 §7) — supervising via user-tier CoS in Claude Desktop
- Principal-as-router (`u--7yg.1`) — surface only project-direction calls
- Verify-then-execute (`u--7yg.10`, `u--7yg.18`) — directive vs spec contradictions get surfaced
- One job per agent (`u--7yg.17`) — your one job is Arc Z; don't pre-empt Arcs 9-13
- Wait-for-quiescence (`u--7yg.15`)
- Autonomous-ship on clean PASS (`u--7yg.11`) — push is part of ship
- Voice discipline (planning v2 §6) — for new content (top-level README, ARCHIVED.md notices)

---

## Operating mode

**Human-in-the-loop** (planning v2 §7). Surface for input at:
- Smoke test results before final archives (especially the app's npm run dev — must continue to function)
- Any unexpected state during subtree-merge (history conflicts, etc.)
- user-beadwork edits to planning v2 §11/§14 — confirm scope before commit
- Done

For Arc Z specifically: cross-repo + new-repo + archives. More moving parts than Arcs 4-7. Surface checkpoints at: post-subtree-merge (verify history preserved), post-smoke-tests (verify nothing broken), pre-archive (verify the-stoa is operational before archiving sources).

---

## How to surface back

Either:
- Comment on a beadwork ticket in agent-substrate (`as--*`)
- Write a short hand-back report; PRINCIPAL will relay

Standby, run.
