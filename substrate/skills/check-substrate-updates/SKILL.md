---
name: check-substrate-updates
description: Check whether deployed substrate files in registered consumer workspaces are still byte-equal to the current the-stoa source (after expected install.sh substitutions). Reports per workspace whether each deployed file is CURRENT or DIFFERS — single-bit drift detection only; PRINCIPAL memory + the workspace's git history of .claude/ is the canonical source for "did I change this or did upstream change this." When drift is found, apply.sh walks the operator through per-file consent + diff display, with git pre-commit safety net and a running-agent warning when role files (MAJOR_*.md, CAPTAIN_*.md) are touched. revert.sh undoes the most recent apply. Triggers on requests like "check substrate for updates", "is my substrate current", "review substrate updates", "apply substrate updates", "did upstream the-stoa advance".
---

# check-substrate-updates — drift detection between the-stoa canon and consumer workspaces

## Why this skill exists

The substrate (`MAJOR_POLYBIUS.md`, `MAJOR_PLINY.md`, `operating-disciplines.md`, the 10 CAPTAIN envelopes, templates, skills) is canonical at the-stoa repo and deployed via `install.sh` into consumer workspaces (project directories where Claude Code sessions activate). Once deployed, those workspaces silently drift as the-stoa evolves — there is no built-in notification.

Before this skill, the only drift-detection path was: manually run `install.sh --dry-run` against each workspace and eyeball the diff. That doesn't scale (one consumer workspace today; more soon) and is easy to forget.

This skill answers, per workspace: "are deployed substrate files still byte-equal to current the-stoa source (after expected sed substitutions), or do some files differ?" Differs is differs; the skill does not classify *why* (local edit vs upstream advance vs both). PRINCIPAL memory + the workspace's git history of `.claude/` is the canonical source for that distinction. Drift output is informational — never blocks the working team.

## When to use this skill

Invoke when:

- The PRINCIPAL asks "check substrate for updates" / "is my substrate current" / similar.
- POLYBIUS sees that `<workspace>/.claude/.substrate-last-check` is more than 24h old AND `last_check_against_sha` differs from current the-stoa HEAD (daily-cadence trigger; see `MAJOR_POLYBIUS.md`).
- A substrate ship just landed and the operator wants to see which consumer workspaces are now stale.
- The PRINCIPAL is ready to apply previously-detected drift ("apply substrate updates").

Do **not** invoke for:

- Auto-deploying without operator confirmation (explicitly out of scope; see `agents/design/stoa--lyh/design.md`).
- Multi-machine substrate sync (cross-machine canon is a separate concern).
- Semantic compatibility checking ("are my modifications still compatible with the new role-file structure"). User judgment is canonical.

## v0 scope and limitations

v0 supports **project-tier and subproject-tier** consumer workspaces (workspaces deployed via `install.sh --target project` or `--target subproject`).

v0 does **not** support **user-tier** check (`~/.claude/`). The `{{USER_TIER_DIR}}` substitution at user-tier (install.sh ~line 613) cannot be reliably re-derived without per-file source markers, which Option Small explicitly skipped. `check.sh` detects user-tier and surfaces a friendly message rather than erroring; for now, manually diff with:

```
cd substrate && diff -u MAJOR_POLYBIUS.md ~/.claude/MAJOR_POLYBIUS.md
```

User-tier check support is documented as future work in `agents/design/stoa--lyh/design.md` §10.2 and will pick one of the substitution strategies described there when the need is real.

Other v0 simplifications, all by design (Option Small):

- **No four-category drift classification.** The two-axis classification (locally-modified × upstream-advanced) was the v2 architecture; PRINCIPAL ratified Option Small after a DAEDALUS-light pass. The single-bit "differs?" answer is enough — when drift surfaces, the operator consults their own memory or `git log -- .claude/` to disambiguate cause.
- **Explicit registry, no auto-discovery.** Consumer workspaces are listed in `substrate/consumer-workspaces.txt`. Add a workspace by appending its absolute path; the registry is intentionally explicit so a workspace doesn't get scanned without the operator opting in.
- **No marker insertion.** `install.sh` is unchanged in this engagement (other than appending `check-substrate-updates` to `SKILL_NAMES`). The future-work design at `agents/design/stoa--lyh/v2-marker-architecture-future-work.md` preserves the marker-based architecture for revisit.

## What the skill ships

```
substrate/skills/check-substrate-updates/
  SKILL.md       # this file
  check.sh       # per-workspace drift detection
  apply.sh       # per-file consent + diff + git pre-commit + running-agent warning
  revert.sh      # undo the most recent apply
substrate/consumer-workspaces.txt   # registry seed (one absolute path per line)
```

`check-substrate-updates` is in `SKILL_NAMES` in `substrate/install.sh` so the skill deploys to every consumer workspace alongside `agent-author`.

## How to invoke

### Check all registered workspaces

```bash
substrate/skills/check-substrate-updates/check.sh
```

Reads `substrate/consumer-workspaces.txt`, scans each workspace, and prints a per-workspace summary:

```
ariadne-core-workspace            DRIFTED (3 files differ from current substrate)
  - .claude/operating-disciplines.md     (+156 lines)
  - .claude/MAJOR_PLINY.md                (+86 lines)
  - .claude/MAJOR_POLYBIUS.md             (+2 lines)

  Last check: 2026-05-04T18:22Z (against substrate sha 7134c92)
  Current substrate HEAD: c37cf5a
  Run 'apply.sh --workspace <path>' to review and apply per-file.

agent-team-on-beadwork            CURRENT (all 18 deployed files match current substrate)
  Last check: 2026-05-08T19:00Z (against substrate sha c37cf5a)

agent-gauntlet                    NOT-STOA-DEPLOYED (no .claude/MAJOR_POLYBIUS*.md found)
```

Exit code is always 0 on successful execution. Drift is informational, not failure.

### Check a single workspace

```bash
substrate/skills/check-substrate-updates/check.sh --workspace /c/Users/denso/claude_projects/ariadne-core-workspace
```

### Apply updates to a workspace

Walk the operator through every DIFFERS file with consent + diff display:

```bash
substrate/skills/check-substrate-updates/apply.sh --workspace <ws> --all-differing
```

Apply specific files:

```bash
substrate/skills/check-substrate-updates/apply.sh --workspace <ws> \
  --files .claude/MAJOR_PLINY.md \
  --files .claude/operating-disciplines.md
```

Skip prompts (auto-commits any uncommitted `.claude/` state in the workspace's git first, then writes + commits the apply):

```bash
substrate/skills/check-substrate-updates/apply.sh --workspace <ws> --all-differing --yes
```

When any role file (`MAJOR_*.md` or `CAPTAIN_*.md`) is in the apply set, `apply.sh` emits a tail block reminding the operator that currently-running agent sessions are operating on the role files they loaded at activation — file-on-disk has changed but in-context behavior has not. For role-file diffs > 50 lines (added + deleted), the message recommends `/clear` and a re-paste; smaller diffs surface the lighter "let it propagate organically" framing.

### Revert the most recent apply

```bash
substrate/skills/check-substrate-updates/revert.sh --workspace <ws>
```

If the workspace's `.claude/` is git-tracked: `git revert` of the apply commit. If not: restore from `<ws>/.claude/.substrate-backups/<latest-timestamp>/`. Per-file revert is supported via `--files`; a specific backup timestamp via `--timestamp`.

## Daily check cadence

POLYBIUS reads `<workspace>/.claude/.substrate-last-check` on activation. If `last_check_timestamp` is more than 24h old AND `last_check_against_sha` does not match the current the-stoa HEAD, POLYBIUS surfaces a non-modal "want me to check substrate for drift?" prompt. PRINCIPAL can answer at any time — there's no nag and no blocking.

The state file is written by `check.sh` at the end of every run; format:

```
last_check_timestamp=2026-05-08T19:00:00Z
last_check_against_sha=c37cf5a
```

The cadence section in `MAJOR_POLYBIUS.md` is the canonical place that documents this discipline.

## Adding a new consumer workspace to the registry

Append the absolute path of the workspace to `substrate/consumer-workspaces.txt`. One path per line; comments (`#`) and blank lines ignored. Run `check.sh` once to verify the workspace is detected with the correct tier (project / subproject / user) and that the deployed file list maps cleanly.

## How the substitution-coupling works (operational note)

`install.sh` substitutes `{{NAME_SUFFIX}}` and `{{USER_TIER_DIR}}` placeholders at deploy time (lines ~613–617 + ~658 in install.sh as of `c37cf5a`). For drift detection to produce comparable byte-strings, `check.sh` and `apply.sh` re-apply the same substitutions to the source side before comparing. Both scripts contain a single `apply_substitutions()` function with a cite-comment pointing at install.sh's substitution lines; **if `install.sh` adds a new `{{...}}` placeholder, that function in both scripts must be updated to match.** The cite-comment is the durable mitigation for the coupling — it surfaces the linkage at the read site, not at code-review time.

## Output classifications (what `check.sh` reports)

| Status | Meaning |
|---|---|
| `CURRENT` | Every deployed file is byte-equal to source-after-substitutions. |
| `DRIFTED` | At least one deployed file differs. The skill does NOT classify *why* (local mod vs upstream advance vs both); operator's memory + `git log -- .claude/` is the canonical source. |
| `NOT-STOA-DEPLOYED` | No `MAJOR_POLYBIUS*.md` found under `.claude/`. The path is in the registry but is not a stoa workspace. |
| `NOT-FOUND` | The path in the registry does not exist on disk. |
| `USER-TIER (out of v0 scope)` | Workspace path is `~/.claude` or `~`; user-tier check is future work. |

For DRIFTED workspaces, each differing file shows the deployed path and the line-count delta (`+N lines` means source is N lines longer than deployed; `-N lines` means deployed is longer). Negative delta + DRIFTED can indicate a deployed file the operator added content to locally; the operator's git history disambiguates.

## What this skill is NOT

- **Not an auto-deployer.** Drift output is FYI; `apply.sh` requires explicit invocation and walks per-file consent unless `--yes` is passed.
- **Not a substitute for git.** Workspace `.claude/` history is the canonical record of "what changed when"; this skill is for "is the workspace current with upstream right now."
- **Not a marker writer.** `install.sh` is not modified to insert per-file markers in this engagement (Option Small). The future-work design preserves the v2 marker architecture.
- **Not a multi-machine sync.** the-stoa is per-machine; cross-machine substrate canon is a separate concern.

## Related

- Design spec: `agents/design/stoa--lyh/design.md` (Option Small).
- Future-work reference: `agents/design/stoa--lyh/v2-marker-architecture-future-work.md` (per-file marker + 4-category model preserved for revisit).
- Beadwork ticket: `stoa--lyh`.
- Daily-cadence discipline: `MAJOR_POLYBIUS.md` (substrate-update check section).
- Cross-reference: `operating-disciplines.md` (durable-substrate / cross-session continuity section).
