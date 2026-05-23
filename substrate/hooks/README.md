# Enforcement hooks — the deterministic tier of the Stoa enforcement layer

This directory holds **harness-owned PreToolUse / Stop hook scripts**: the deterministic,
compaction-immune tier of the Stoa enforcement layer (design `bw show stoa--xyb.5`; design-rev1
at `agents/design/arc-46/design-rev1.md`). It is the detailed reference for the hook tier; the
always-loaded one-paragraph authoring rule lives at `operating-disciplines.md` §34.

This file is itself a deployed artifact (it lands at `.claude/hooks/README.md` after `install.sh`
runs) — the canon's detail is loaded on-demand the same way every module's detail is, keeping the
always-loaded §34 rule thin. That dogfood mirrors `modules/README.md` (§33).

> Provenance: enforcement-layer design + the cron-survives-compaction principle `bw show stoa--xyb.5`;
> composition-layer mechanism (the deploy-class idiom this mirrors) `bw show stoa--xyb.4`. Shipped
> Arc 46 (debloat Arc 3) — Stage 1 (deterministic tier).

---

## 1. Why these exist — adherence that survives compaction

Arcs 44–45 cut role-file bloat by relocating content into the composition layer. That cut is only
safe if **adherence to the surviving rules survives context compaction**. A hook is *harness-fired,
not model-fired*: it executes regardless of what the model's compacted context still holds. That is
the load-bearing property — the deterministic gates here enforce three load-bearing footguns even
when the agent that triggered them has forgotten the rule.

The tier is **defense-in-depth**, not the whole defense. The prose disciplines (global CLAUDE.md
authorship rule, `operating-disciplines.md` §12 / §24) remain the primary defense; these gates are
the deterministic backstop for the regressions the prose alone has let through.

---

## 2. THE AUTHORING RULE (the load-bearing convention for every trigger payload)

**Every trigger payload — a hook `permissionDecisionReason`, a Stop `reason`, a PostToolUse
`additionalContext`, or a cron prompt body — MUST state, self-contained inline:**

1. **WHY it fired** — what was blocked / what the trigger is checking, and
2. **WHAT to do** — the concrete next action to proceed.

**Never a bare pointer** ("see §X.Y.Z", "per the discipline"). A pointer fails after compaction:
the trigger's entire value is that it re-tells the rule the agent has forgotten, and an agent that
has compacted cannot follow a pointer to a section it no longer holds. The payload must carry the
instruction, not a reference to it.

Worked examples (all from the gates in this directory):

- author-field deny: names the *field*, the *file*, the *wrong value*, the fix (`git config ...` /
  re-stage), AND how to widen the allow-list if the value is a legitimate PRINCIPAL identity.
- clean-tree deny: names the *dirty paths inline* and the three resolution verbs (commit / stash /
  clean), not "see the branch-hygiene discipline".
- no-`-m` deny: shows the *wrong form*, the *correct positional form*, and *why* the footgun loses
  data — inline, in the message.

When you author a new trigger payload anywhere in the substrate, this is the rule it must obey.

---

## 3. The script contract (uniform across all gates)

- **Input:** one JSON hook event on **stdin** (`tool_name`, `tool_input.command`, `session_id`,
  `cwd`, `transcript_path`, ...). Parsed with `python3` (POSIX-portable, assumed present per
  `operating-disciplines.md` §13; `jq` is NOT assumed). Shared helpers: `_hooklib.sh` (not a hook
  itself — leading underscore, never registered).
- **PreToolUse output:** allow = exit 0, no stdout (normal permission flow). deny = exit 0 with
  stdout JSON `hookSpecificOutput.{hookEventName:"PreToolUse", permissionDecision:"deny",
  permissionDecisionReason:"<self-contained message>"}`. (exit-0 + JSON is chosen over exit 2 so the
  precise model-facing reason is carried; exit 2 only forwards stderr.)
- **Stop output:** allow = exit 0, no stdout. block = exit 0 with stdout JSON
  `{decision:"block", reason:"<self-contained checklist>"}`. Stop does NOT support
  `additionalContext` (live-verified 2026-05-23) — the checklist rides `reason`.
- **FAIL-OPEN on script error.** Any internal error (no python3, malformed event, no git,
  unreadable config) → the script allows the tool call. This is a deliberate inversion of the usual
  "fail closed for safety": a fail-CLOSED gate that errors would block every gated tool call in the
  live session and **brick the running team**; a fail-OPEN gate degrades to today's no-enforcement
  baseline, which is safe. (Design §4 / ARGUS R5.)

---

## 4. The gates (Stage 1)

| Script | Event | Narrowing `if` | Blocks |
|---|---|---|---|
| `pretooluse-author-field-audit.sh` | PreToolUse | `Bash(git commit*)` | a commit whose git author identity OR a staged author-like field names someone other than the PRINCIPAL |
| `pretooluse-clean-tree-before-branch.sh` | PreToolUse | `Bash(git *)` | arc-build branch / worktree creation when the tree is dirty |
| `pretooluse-no-dash-m-bw-comment.sh` | PreToolUse | `Bash(bw comment*)` | the `bw comment <id> -m "..."` data-loss footgun |
| `stop-self-check.sh` | Stop | (none) | once per turn: a self-check backstop (checker-dispatched? gate not dodged? commit attributed?) |

The PRINCIPAL allow-list the author-field gate reads is `.claude/hooks/principal-identity` (one
name/email per line; `#` comments + blanks ignored), written at install time. It is the gate's
CONFIG (the PRINCIPAL identity the gate compares against) — **not an author-like field of any repo
artifact**, and so is exempt from the audit the gate performs.

---

## 5. SAFETY ARCHITECTURE — source-only, default-OFF, never the running session

**The HARD SAFETY CONSTRAINT (design-rev1 §8).** These scripts are substrate SOURCE. Deploying the
*scripts* to a `.claude/hooks/` directory is **INERT**: Claude Code only fires hooks that are
**registered in a `.claude/settings.json`**. No Stoa arc and no `install.sh` run auto-writes a live
`settings.json`. The scripts sit dormant on disk until an operator explicitly arms them.

- **Arming is a separate, operator-gated, DEFAULT-OFF step.** `install.sh --enable-hooks` (default
  OFF) is the only path that merges the candidate `settings-hooks.json` block into the target's
  `.claude/settings.json`. When the flag is OFF (the default), **no hooks are registered** — the
  scripts and the candidate template deploy, nothing is armed.
- **Even with `--enable-hooks`, the merge targets the INSTALL TARGET, never the running build
  session.** And at **user tier** the target `~/.claude/settings.json` IS the running session's
  config — so `--enable-hooks` at user tier is doubly guarded: it is off by default AND the install
  prints the merge as a MANUAL instruction rather than auto-writing `~/.claude/settings.json`
  (ARGUS r4). An agent never auto-writes a live `~/.claude/settings.json`.
- **Isolation testing only.** Test the gates by feeding synthetic stdin JSON to the scripts
  directly, or by deploying to a THROWAWAY target dir / `git clone --no-local` scratch repo. Never
  run `--enable-hooks` against anything but a throwaway. Never edit a live `.claude/settings.json`
  by hand from inside a build.
- **Why this matters:** a PreToolUse gate on `git commit` / branch-create armed into the *running*
  team's own `settings.json` would gate the running team's OWN operations — gating the very session
  doing the build. That is a no-experiments-on-real-agents violation in spirit (the live canonical
  seats are the "real agent").

### Arming the hooks intentionally (operator runbook)

When an operator genuinely wants the gates live on a target workspace:

1. Inspect the candidate block at `<target>/.claude/templates/settings-hooks.json`.
2. Either run `install.sh ... --enable-hooks` (project tier — merges into the TARGET's
   `<target>/.claude/settings.json`, never the running session), OR at user tier follow the printed
   manual-merge instruction to merge the block into `~/.claude/settings.json` yourself.
3. Confirm `.claude/hooks/principal-identity` lists every valid PRINCIPAL name/email (the
   author-field gate denies any value not on the list, with a widen-the-list message).
4. The gates are now live for that workspace's sessions. To disarm, remove the `hooks` block from
   that `settings.json`.
