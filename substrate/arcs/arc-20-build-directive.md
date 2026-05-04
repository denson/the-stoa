# Arc 20 build directive — user-tier install convention + dir choice + placeholder substitution

**Audience:** the fresh Claude Code session opened to build Arc 20 deliverables.
**Authored by:** user-tier Chief-of-Staff (POLYBIUS-equivalent) + the PRINCIPAL (Denson Smith).
**Status:** active directive.
**Builds on:** Arcs 1-19 (the-stoa main `e31b264`). Arc 19.x sequence (10+ patches) shipped distribution-readiness for the cold-clone audience; Arc 20 closes the install-side gap.

**Your one job:** make `install.sh --target user` deliver a working user-tier setup — directory, user-beadwork init, role-file substitution — without requiring the PRINCIPAL to debug the post-install state. Empirically: a fresh POLYBIUS spawned from home directory currently fails to find user-beadwork because the substrate doesn't ship a coherent user-tier-dir convention. This arc fixes that.

This is small but structural. Substrate edits + install.sh extension + skill update. Comparable in scope to Arc 14 (sub-project spawning) — substantive but contained.

---

## Comms — direct async via bw

POLYBIUS will be polling `stoa--<this-arc-id>` while you work. PLINY follows the surface-and-wait discipline (Arc 18): poll only when you've surfaced a question and are waiting for the response. Otherwise execute autonomously.

bw command syntax discipline: `bw comment <id> "text"` — positional, no `-m` flag (Arc 16.1 §6.1).

---

## Read first

1. **`substrate/install.sh`** — the current install script. You'll be extending the `--target user` path with an interactive dir-choice prompt + scaffolding logic.
2. **`substrate/MAJOR_POLYBIUS.md`** §7.5 (Arc 19.11) — currently hardcodes `~/claude_projects/user-beadwork/`. You'll replace with `{{USER_TIER_DIR}}` placeholder.
3. **`substrate/MAJOR_POLYBIUS.md`** §9 activation checklist — currently has hardcoded user-tier path; same placeholder swap.
4. **`skills/install-stoa/SKILL.md`** Beat 3 (tier choice) + Beat 4 (target path) — currently doesn't address user-tier-dir-choice. You'll add that beat.
5. **`docs/sessions/2026-05-03-stoa-v0.1.0-shipped.md`** + retrospective — context for why Arc 20 surfaced (user-tier install convention gap caught during fresh-POLYBIUS spawn tests).
6. **`gauntlet.config.example.yaml`** at agent-gauntlet repo (cross-repo reference) — shows the placeholder/template substitution pattern you'll mirror for `{{USER_TIER_DIR}}`.

---

## Phase A — Architectural decisions (LOCKED pre-dispatch by PRINCIPAL)

You do NOT need to surface these as Phase A calls. Settled during directive review:

### A1. Default user-tier dir name — LOCKED: `~/stoa_projects/`

Descriptive (explains the purpose), portable across platforms (`~/` resolves correctly on Windows/macOS/Linux), and matches the substrate brand. Existing PRINCIPAL has `~/claude_projects/` (named pre-Stoa); detection logic accommodates that case.

### A2. Strict scaffolding — LOCKED

Install runs `mkdir -p <chosen-dir>` + `git init` + `bw init` at the chosen location. NEVER clobber existing directories — if `<chosen-dir>/user-beadwork/` already exists with `.git/` and `.bw/`, skip the init and treat as found-existing.

### A3. Install-time substitution — LOCKED

Substrate template files (currently `substrate/MAJOR_POLYBIUS.md`) get a `{{USER_TIER_DIR}}` placeholder; install.sh substitutes the user's chosen path before deploying to `~/.claude/`. Mirror the existing agent-gauntlet template pattern.

### A4. Detection-with-confirmation — LOCKED

Install scans common locations for existing `user-beadwork/`:

```
~/stoa_projects/user-beadwork/
~/claude_projects/user-beadwork/
~/projects/user-beadwork/
~/Code/user-beadwork/
```

A "found" hit requires: directory named `user-beadwork`, has `.git/`, has been bw-initialized (`.bw/` or whatever bw's marker file is). On hit, prompt PRINCIPAL: "Found existing user-beadwork at `<path>`. Use this? Your user-tier dir would be `<parent>`. [Y/n]". User confirms → install records `USER_TIER_DIR=<parent>` and skips scaffolding. User declines → fall through to default-prompt flow.

If detection finds zero matches → straight to default-prompt with `~/stoa_projects/` as the suggestion.
If detection finds multiple matches → surface all, let user pick canonical OR "create new."

---

## Deliverables

### 1. `substrate/install.sh` — extend `--target user` flow

**Location:** `the-stoa/substrate/install.sh` (existing file; extending, not replacing)

**New behavior when `--target user` is invoked:**

1. **Detection phase:** check the four common locations from A4 for existing `user-beadwork/`. Build list of matches.
2. **User-tier dir prompt:**
   - If 1 match found → `Found existing user-beadwork at <path>. Use this? [Y/n]`. Y → set `USER_TIER_DIR=<parent>`, skip scaffolding. n → fall through to "where do you want it?" prompt.
   - If multiple matches → list all, plus "create new at ~/stoa_projects/". User picks one.
   - If zero matches → `Where do you want your user-tier directory? [default: ~/stoa_projects/]`. Accept input or fall to default.
3. **Scaffolding phase** (only if not using existing user-beadwork):
   - `mkdir -p <chosen-dir>`
   - `cd <chosen-dir> && mkdir user-beadwork && cd user-beadwork && git init && bw init`
   - Surface what was created: print absolute path of new user-beadwork
4. **Substitution phase:**
   - Resolve `<chosen-dir>` to absolute path (handle `~/` expansion)
   - Substitute `{{USER_TIER_DIR}}` → resolved absolute path in role file content before writing to `~/.claude/MAJOR_POLYBIUS.md`
   - Other role files (MAJOR_PLINY.md, CAPTAIN_*.md) — check if they contain `{{USER_TIER_DIR}}`; substitute if so. (For Arc 20, only MAJOR_POLYBIUS.md needs the placeholder — but the substitution logic should handle any file that contains it for future-proofing.)
5. **Output phase — "Next steps":**
   - "Your user-tier directory is `<chosen-dir>`."
   - "Open Claude Code in `<chosen-dir>` for user-tier POLYBIUS sessions."
   - "user-beadwork is at `<chosen-dir>/user-beadwork/` (durable memory layer)."

**Cross-platform considerations:**

- `~/` expansion: bash handles natively; just use `~/` in path strings, let shell resolve.
- Windows users running bash via Git Bash / WSL: paths still work via `~/`.
- macOS/Linux: standard.
- Don't hardcode `/c/Users/...` style paths anywhere; always `~/`.

**`--dry-run` behavior:** print all the `mkdir`/`git init`/`bw init` commands that WOULD run without executing. Print the substitution that WOULD happen. Don't write any files.

**Idempotency:** re-running `install.sh --target user` after an initial install should be safe. If `USER_TIER_DIR` was already chosen and recorded somewhere durable (see deliverable #5), re-use it without prompting; otherwise re-run detection + prompt.

### 2. `substrate/MAJOR_POLYBIUS.md` — placeholder swap + activation refinement

**Location:** `the-stoa/substrate/MAJOR_POLYBIUS.md`

**Edits:**

1. **§7.5 (per-tier bw locations)** — replace hardcoded `~/claude_projects/user-beadwork/` with `{{USER_TIER_DIR}}/user-beadwork/`. Add a parenthetical: "(this path is set at substrate install time; see your deployed role file for the resolved value)."
2. **§9 step 2 (activation checklist)** — same swap. The deployed role file will have the resolved path; the source template has the placeholder.
3. **§9 step 1** — add a cwd check beat:

```
1. Confirm your seat in one short sentence: "I'm MAJOR_POLYBIUS, the CHIEF-OF-STAFF for this <tier>." Don't recite the whole role file.

1a. **Check cwd.** If you are at user-tier and your cwd is the home directory (or any directory other than {{USER_TIER_DIR}}), suggest to the PRINCIPAL: "I work better from {{USER_TIER_DIR}} where I can see your projects laterally and reach user-beadwork in one cd. Want me to wait while you open a session there, or proceed from here?" Don't refuse to operate from the wrong cwd — just surface the convention.
```

(Renumber subsequent steps accordingly.)

**Voice discipline:** PRINCIPAL/HUMAN throughout (Arc 19.x discipline holds). The placeholder is for the path only; surrounding prose stays as-is.

### 3. `skills/install-stoa/SKILL.md` — add user-tier-dir-choice beat

**Location:** `the-stoa/skills/install-stoa/SKILL.md`

**Edit:** in Beat 3 (tier choice), when the PRINCIPAL picks `user`, add a sub-beat that:
- Runs the detection scan
- Surfaces the found locations + the default option to PRINCIPAL
- Captures the choice
- Passes the chosen path to install.sh as the user-tier dir

If picking `project` or `subproject`, no change to the existing Beat 3 behavior — those tiers don't use `USER_TIER_DIR`.

**New sub-beat content (sketch):**

```
### Beat 3a — User-tier directory choice (only if --target user)

The user-tier chief-of-staff needs a "home directory" — where user-beadwork
(durable memory) lives, and where you'll typically open Claude Code for
user-tier work.

1. Run install.sh's detection (or use `find` / `ls` directly to scan common
   locations: ~/stoa_projects/, ~/claude_projects/, ~/projects/, ~/Code/).
2. Surface findings:
   - If one detected: "Found existing user-beadwork at <path>. Use this?
     [Y/n] Your user-tier dir would be <parent>."
   - If multiple: list them all, ask PRINCIPAL to pick or create new
   - If none: "I'll create one at ~/stoa_projects/ (default), or you can
     pick another location. Where would you like? [default: ~/stoa_projects/]"
3. Confirm choice with PRINCIPAL before invoking install.sh.
4. install.sh handles the actual mkdir + git init + bw init + substitution.
```

### 4. `docs/case-study/case-study.md` — appendix update (single line)

**Location:** `the-stoa/docs/case-study/case-study.md`

**Edit:** append a single line to the appendix listing Arc 20:

```
- **Arc 20 — User-tier install convention + dir choice + placeholder substitution.** install.sh now interactively asks where the user wants their user-tier directory (default `~/stoa_projects/`), scaffolds it (mkdir + git init + bw init), and substitutes `{{USER_TIER_DIR}}` in the deployed role file. Closes the install-side gap caught when fresh POLYBIUS spawns from home directory failed to find user-beadwork. Substrate edits at `substrate/MAJOR_POLYBIUS.md` §7.5 + §9; install.sh extension; install-stoa skill Beat 3a.
```

### 5. (Optional, if it falls out cleanly) — `~/.claude/stoa-config.json` for re-install idempotency

If install.sh re-runs and needs to know the previously-chosen `USER_TIER_DIR` without re-prompting, write it to `~/.claude/stoa-config.json` on first install:

```json
{
  "user_tier_dir": "/Users/denso/stoa_projects",
  "installed_at": "2026-05-04T...",
  "substrate_version": "v0.1.0+arc-20"
}
```

On re-install, read this file first; only re-prompt if missing or PRINCIPAL passes `--reset-config`.

This is OPTIONAL — if it complicates the install flow, defer to a later arc. The minimum viable Arc 20 doesn't need this — re-running install.sh just re-prompts.

---

## Phase B — Smoke test

After all deliverables are in place, run a smoke test before committing:

1. **Detection scan logic:** unit-test the four-location scan. Mock the filesystem state to verify each branch (zero matches / one match / multiple matches / matches-but-not-bw-initialized).
2. **Prompt flow:** dry-run the install with simulated input (echo piped or expect-style). Verify each branch produces the expected output + state.
3. **Substitution:** verify the deployed `~/.claude/MAJOR_POLYBIUS.md` contains the resolved absolute path, NOT the literal `{{USER_TIER_DIR}}` token. Round-trip-check by `grep "{{USER_TIER_DIR}}"` against the deployed file — should return zero hits.
4. **Idempotency:** run install.sh twice. Second run should not error or clobber existing state.
5. **Cross-platform basic check:** verify `~/` expansion works as expected. Run on whatever shell environment is available; if Windows-only, document the macOS/Linux path-handling expectation.
6. **Activation flow:** after install, simulate a fresh POLYBIUS session in the chosen user-tier dir + run `bw prime` from `<USER_TIER_DIR>/user-beadwork/`. Should succeed without "not a git repo" error.

If smoke fails on any beat, surface to POLYBIUS via `bw comment <ticket-id> "smoke fail: <which beat> — <details>"` and wait for guidance.

---

## Phase C — Ship

Clean PASS → autonomous ship per `u--7yg.11`. Otherwise surface back to POLYBIUS via the bw ticket.

**Commit message shape:**

```
Arc 20: user-tier install convention + dir choice + {{USER_TIER_DIR}} substitution

Closes the install-side gap caught when fresh POLYBIUS spawns from home
directory couldn't find user-beadwork. install.sh --target user now:

1. Detects existing user-beadwork at common locations (~/stoa_projects/,
   ~/claude_projects/, ~/projects/, ~/Code/) and offers to use it
2. If none found, prompts PRINCIPAL for user-tier directory choice
   (default ~/stoa_projects/) and scaffolds: mkdir + git init + bw init
3. Substitutes {{USER_TIER_DIR}} placeholder in deployed
   ~/.claude/MAJOR_POLYBIUS.md with resolved absolute path

substrate/MAJOR_POLYBIUS.md §7.5 + §9 use the placeholder; activation
checklist gains a cwd-check step that suggests navigating to the
user-tier dir if currently elsewhere.

skills/install-stoa/SKILL.md Beat 3 walks PRINCIPAL through the
dir-choice flow.

case-study.md appendix updated.

Closes stoa--<ticket-id>.
```

Push to origin/main on clean PASS. The arc directive itself (`substrate/arcs/arc-20-build-directive.md`) was committed by POLYBIUS before dispatch — don't include it in your commit.

---

## Out of scope

- Touching the Stoa app at `app/`. No app changes in Arc 20.
- Modifying the case study or KG spec beyond the appendix one-liner.
- Cross-repo work (user-beadwork, agent-gauntlet, ariadne-core-workspace). All work in the-stoa.
- Rewriting how install.sh handles `--target project` or `--target subproject`. Arc 20 is user-tier-specific.
- Adding `~/.claude/stoa-config.json` for re-install idempotency unless it falls out cleanly. The minimum viable Arc 20 just re-prompts on re-install; durable config is a v0.2 candidate.

---

## Surface back when done

`bw comment <ticket-id> "Arc 20 shipped at commit <sha>, pushed to origin/main. Smoke test passed: <brief summary of beats>. Files added: <list>. Files modified: <list>. {{USER_TIER_DIR}} substitution verified: zero literal-placeholder hits in deployed role file. Detection logic tested across <N> branches."`

Then close the ticket: `bw close <ticket-id>`.
