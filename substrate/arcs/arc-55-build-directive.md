# Arc 55 build directive — stoa--2i5: install.sh canonical .gitignore management

**Ticket:** `stoa--2i5` (P3, bucket C — hygiene/mechanical)
**Driver:** PLINY_the-stoa
**Drive mode:** autonomous (bucket C — autonomous-ship on clean PASS per `stoa--ikr`)
**Worktree:** `.claude/worktrees/arc-55-build` (branch `arc-55/build`)
**Gauntlet:** DAEDALUS → ARGUS → ADA → VERA → CATO → NOMOS → ZENO (no HARD STOP — bucket C is not PRINCIPAL-gated)

## Problem

`install.sh` deploys substrate to a consumer workspace but does NOT manage the consumer's
`.gitignore`. Substrate-generated transient paths then show as untracked noise in `git status`:

- `.claude/scheduled_tasks.lock` — durable cron state (CronCreate `durable: true`)
- `.claude/worktrees/` — per-arc-build worktree dir; transient/empty residue post-merge
  (Windows file-lock leaves orphan dirs — see `stoa--7ap`)
- `.substrate-last-check` — check-substrate-updates state file
- `__pycache__/` / `*.pyc` — skill bytecode (already stripped post-copy at deploy; but a
  consumer who *runs* a skill regenerates them)

This noise pollutes `git status`, risks accidental `git add .` of cache state, and is
identical-shape across every consumer workspace.

## Acceptance criteria (from the ticket — these are the spec)

1. `install.sh` emits (or offers) canonical `.gitignore` additions for substrate-generated
   transient paths.
2. Document in `install.sh --help` + substrate README which paths are transient
   (operator-readable).
3. Post-fix verification: fresh `install.sh` at a clean workspace + `git status` shows no
   untracked substrate-transient paths.

## Design latitude (DAEDALUS decides; user-tier weakly leans α-with-flag)

- **(α) Generate-or-append** — write a `.claude/.gitignore` covering the transient paths;
  optionally append a one-line `.claude/.gitignore` reference to the consumer root
  `.gitignore` behind an explicit `--manage-gitignore` flag (matches the existing
  `--modify-claude-md` / `--no-bw-init` consent-flag pattern).
- **(β) Document-only** — print the recommended lines at end of run + a
  `--print-gitignore-lines` flag for scripted append.
- **(γ) Self-contained `.claude/`** — relocate transient state under `.claude/_state/` and
  ship a one-liner ignore.

## Hard constraints

- **Consent before mutating consumer files.** Mutating the consumer's root `.gitignore`
  without a flag is the same class of overreach `--modify-claude-md` guards against. Any
  root-`.gitignore` write MUST be flag-gated. A `.claude/.gitignore` (substrate's own
  subtree) is lower-risk but still must be idempotent (re-running install.sh must not
  duplicate lines).
- **Idempotent.** Re-running install.sh produces no duplicate ignore entries.
- **Dry-run honored.** `--dry-run` must print the intended `.gitignore` action, write nothing.
- **All three tiers.** Behavior must be coherent at user / project / subproject tier
  (note `.claude/.gitignore` semantics — a `.gitignore` inside `.claude/` ignores paths
  relative to `.claude/`).
- **Scope-locked.** This arc touches `install.sh` + substrate README + `install.sh --help`
  ONLY. Do not pull in adjacent tickets (sp1, 3na, 7ap). The `__pycache__` consumer-side
  ignore is in scope (it's a transient path); the save-verdict `.gitignore` shipping is
  `stoa--7b1.2`, a DIFFERENT arc — do not absorb it.

## Precedents to read (existing install.sh transient-state hygiene)

- `write_substrate_manifest` (Arc 38) — existing structured-write-into-.claude precedent
- post-copy pycache cleanup `install.sh:1119-1134` (Arc 40) — existing transient-strip precedent
- arg-parse case block `install.sh:549-586`; `usage`/`--help` text near top (`install.sh:26-110`)

## Probes (VERA will run these; DAEDALUS refine)

- P1: fresh install.sh into a synthetic clean workspace, then `git status --porcelain` shows
  zero untracked substrate-transient paths (AC3).
- P2: run install.sh twice; the `.gitignore` artifact has no duplicated lines (idempotency).
- P3: `--dry-run` prints the intended gitignore action and writes nothing.
- P4: `install.sh --help` documents the transient paths (AC2); README updated (AC2).
