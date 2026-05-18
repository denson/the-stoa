---
name: check-bw-release
description: Check for new bw upstream releases and surface the 3-axis impact-classification template when one is found. Queries the bw GitHub releases API for the current latest tag, compares to a per-workspace baseline stored at .bw-release-last-check (in the skills-parent directory — substrate/ at substrate-tier, <workspace>/.claude/ at consumer-tier), and prints either a "current" message or a "new release detected" message with changelog pointer + axis template + suggested next action (per operating-disciplines.md §22 bw-upgrade discipline). Single-target skill (checks one upstream feed); per-workspace baselines (mirrors check-substrate-updates' per-workspace state-file pattern). Operator decides whether to cron it; no scheduling defaults. Triggers on requests like "is there a new bw release", "check bw for updates", "bw release check", "new bw version", "did bw upgrade".
author: Denson Smith
---

# check-bw-release — Step 1 (Trigger) of the bw-upgrade discipline

## Why this skill exists

The bw-upgrade discipline at `operating-disciplines.md` §22 names a 5-step process: **Trigger → Review → File tickets → Dispatch → Verification.** Steps 2-5 are POLYBIUS judgment; Step 1 (Trigger detection) is mechanical and is the one step worth a skill. Without a skill, the operator has to remember to visit the releases page periodically; with the skill, the check is one command and the output cues the operator into Steps 2-5 (axis classification template, suggested next action, cross-ref to §22 in the discipline doc). This skill operationalizes Step 1 only — see `operating-disciplines.md` §22 for the discipline this skill participates in.

## When to use this skill

Invoke when:

- The PRINCIPAL asks "is there a new bw release" / "check bw for updates" / similar.
- An operator wants a periodic upstream-release check (the skill is safe to invoke on any cadence — it ships with no rate-limiting beyond GitHub's own 60/hour unauthenticated cap, which is far above any plausible check cadence).
- Before kicking off a new substrate-adoption arc, sanity-check that the baseline tag is still current.

Do **not** invoke for:

- Classifying features into axes (that's `operating-disciplines.md` §22 Step 2 — POLYBIUS judgment).
- Filing tickets per axis (that's §22 Step 3 — POLYBIUS judgment).
- Auto-applying upgrades (out of scope; if/when an arc warrants auto-apply, that's a future skill's job).

## What the skill ships

Three things:

1. `SKILL.md` — this file.
2. `check.sh` — the executable shell script.
3. A per-workspace state file written at first invocation.

**State-file location.** The skill writes `.bw-release-last-check` in the directory **two levels above the script** (i.e., the skills-parent directory). At substrate-tier (the-stoa repo), that resolves to `substrate/.bw-release-last-check`. At consumer-tier (after `install.sh` deploys the skill subtree to `<workspace>/.claude/skills/check-bw-release/`), it resolves to `<workspace>/.claude/.bw-release-last-check`. Per-workspace baselines mirror the `check-substrate-updates` pattern (state file at `<workspace>/.claude/.substrate-last-check`); each workspace's baseline drifts independently as that workspace's operator runs the skill.

**No `.gitignore` line is needed.** The state file is filtered at RUNTIME by the same `grep -v` mechanism `check-substrate-updates/check.sh:489-500` uses for its own state file — so it does not show up in the uncommitted-changes counts that other skills compute. Operators MAY commit the file (no harm; it is just a tag), but the default mode is untracked-and-runtime-filtered.

## How to invoke

Three worked invocations:

- `<skill-dir>/check.sh` — the standard call.
  - Substrate-tier: `substrate/skills/check-bw-release/check.sh`
  - Consumer-tier: `<workspace>/.claude/skills/check-bw-release/check.sh`
- `<skill-dir>/check.sh --force-check` — no-op today; reserved for forward-compat if a future arc adds caching.
- `<skill-dir>/check.sh --baseline v0.12.3` — override the stored baseline for this invocation. Test-only or recovery use (if the state file is lost / corrupted).

## What the output is telling you

Two cases:

- **CURRENT.** `Current bw release: v0.13.0 (baseline matches). No action needed.` Skill exits 0.
- **NEW RELEASE DETECTED.** Multi-line output naming the new tag, the prior baseline, a pointer to the GitHub release-notes URL, the 3-axis classification template (verbatim copy of `operating-disciplines.md` §22.2 axes as a checklist), and a suggested next action (`file one ticket per impact axis touched per operating-disciplines.md §22 Step 3`). Skill exits 0.

The exit code is **always 0 on successful execution** — drift is informational, never blocks. Same exit-code discipline as `check-substrate-updates/check.sh`.

## How to test

Three worked invocations against the env-var fixture mechanism:

- **At-current** (baseline matches upstream-latest):

  ```bash
  BW_RELEASE_CHECK_LATEST_OVERRIDE=v0.13.0 \
  BW_RELEASE_CHECK_BASELINE_OVERRIDE=v0.13.0 \
    <skill-dir>/check.sh
  ```
  Expected: `Current bw release: v0.13.0 (baseline matches). No action needed.`

- **New-release-detected** (upstream-latest is ahead of baseline):

  ```bash
  BW_RELEASE_CHECK_LATEST_OVERRIDE=v0.99.0 \
  BW_RELEASE_CHECK_BASELINE_OVERRIDE=v0.13.0 \
    <skill-dir>/check.sh
  ```
  Expected: `NEW BW RELEASE DETECTED` block with v0.99.0 / v0.13.0 / release-notes URL / 3-axis checklist / suggested next action.

- **Live** (no overrides, no `--baseline`):

  ```bash
  <skill-dir>/check.sh
  ```
  Expected today (against bw 0.13.0): `current`.

Both env vars are scoped to a single invocation (no file state to clean up between tests). The mechanism is documented inline in `check.sh` at the env-var read sites.

## State-file shape

One line, just the tag (e.g., `v0.13.0\n`). First invocation writes baseline = upstream-latest — no "new release detected" message on first run; the skill's job is to surface **changes**, not initial state. The bootstrap is silent except for one suffix line (`(baseline bootstrapped on first invocation)`) so the operator can tell the file was just created. There is **no `--init` flag**; first invocation IS the init.

A timestamp is not stored — the file's `mtime` is the timestamp if one is ever needed.

## Per-workspace deployment + baseline independence

This skill follows the per-workspace deployment pattern of `check-substrate-updates`: `install.sh` deploys the skill subtree to `<workspace>/.claude/skills/check-bw-release/`, and each workspace runs the skill against its own baseline. There is **no cross-workspace coordination**; an upstream advance is detected independently at each workspace the first time that workspace runs the skill after the advance.

- The substrate-tier copy at `the-stoa/substrate/skills/check-bw-release/` runs against `substrate/.bw-release-last-check`.
- Consumer copies run against `<workspace>/.claude/.bw-release-last-check`.

The canonical "did upstream advance since our last bw-upgrade arc shipped?" question is answered by looking at the **substrate-tier baseline** — that is the workspace where bw-upgrade arcs are dispatched. Consumer copies are convenience invocations; their baselines are local-context-only. Operators picking which workspace's baseline to advance is a workspace-local decision.

## Cron cadence

Out of scope per Arc 28 directive A7. Operator picks; the polling-cron-prompt template at `substrate/templates/polling-cron-prompt-template.md` is adaptable if the operator decides to cron-schedule.

## What this skill is NOT

- **Not an upgrader.** Step 1 only. Steps 2-5 are POLYBIUS judgment (and standard arcs).
- **Not a classifier.** Axis classification is POLYBIUS judgment per §22 Step 2; the skill prints the template, the operator fills it in.
- **Not a multi-source release tracker.** bw only; if/when other upstreams (jq, etc.) need similar tracking, file a follow-up.
- **Not authenticated.** No GitHub token required; rate limit is 60/hour unauthenticated, far above any plausible check cadence.
- **Not a cross-workspace coordinator.** Each workspace's baseline drifts independently. If operator wants a single canonical baseline, run the skill only at the substrate-tier copy and ignore consumer-tier copies — the per-workspace pick is "first-class everywhere," not "canonical at one place."

## Related

- `operating-disciplines.md` §22 (bw-upgrade discipline) — the 5-step process this skill operationalizes Step 1 of.
- `MAJOR_POLYBIUS.md` §16.8 (bw 0.13.0 available primitives) — the substrate-side adoption shape produced by the 0.12.3 → 0.13.0 run-through.
- `substrate/skills/check-substrate-updates/` — sibling structural model, INCLUDING the per-workspace state-file pattern this skill mirrors (state file at `<workspace>/.claude/.substrate-last-check`).
- `ariadne--c71` — deployment-side worked example for the 0.12.3 → 0.13.0 release.
- `stoa--s6n` — this arc; substrate-side worked example (including the registry-descope worked example that grounds §22 Step 2's "verify changelog claims empirically" sub-bullet).
