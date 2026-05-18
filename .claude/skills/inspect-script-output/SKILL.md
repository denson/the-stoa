---
name: inspect-script-output
description: Inspect post-mechanical-script workspace state for strangeness — anomalies the script wasn't pre-programmed to surface. Reads the workspace's deployed-file tree, git HEAD, and any optional script-output artifact, and emits a structured strangeness report POLYBIUS triages per operating-disciplines.md §27. Per A7 boundary, this skill establishes the 3-step pattern component; per-discipline mechanical enforcement (operating-disciplines.md §25 PRINCIPAL-gate / §19.6 attestation / MAJOR_PLINY.md §5.10 signoff / MAJOR_POLYBIUS.md §17 base-vs-custom) is incremental future-arc work. Triggers on requests like "inspect substrate state after apply", "check post-install workspace strangeness", "run inspection agent on substrate update", "post-script state inspection".
author: Denson Smith
---

# inspect-script-output — the inspection-agent layer of the 3-step substrate-update pattern

## Why this skill exists

The substrate's mechanical-script-then-agent-inspection split (canonical home: `operating-disciplines.md` §27) names a three-step pattern: **1. mechanical script runs → 2. inspection agent reads result + workspace state and surfaces anything strange → 3. POLYBIUS triages findings against the §25 PRINCIPAL-gate discipline.** This skill is the substrate's worked-example deployment of step 2 for the substrate-update flow.

**The empirical anchor.** Arc 26 (`stoa--dxw`) extended `substrate/skills/check-substrate-updates/check.sh` from **489 to 893 lines** to add MISSING + OBSOLETE + uncommitted-state detection — three new known-strangeness categories the script learned to pre-enumerate. The live line-count today is 934 lines (downstream of Arc 26 via Arc 29's base-vs-custom additions); the 489 → 893 jump specifically is the Arc 26 ship anchor for the script-bloat empirical claim. PRINCIPAL declared 2026-05-16 (after the Arc 26 ship + `stoa--501` revert sequence) that this trajectory is the wrong shape: the recognition layer belongs in an LLM-grade inspection-agent run AFTER the mechanical script, not inside the script. PRINCIPAL declaration verbatim (from `bw show stoa--32b.2` ticket body):

> *"We are spending way too much time trying to get script workflows perfect when the answer is to run the script, then run an agent with a script to check what happened including anything strange and then let polybius fix any of the strangeness with human approval if necessary."*

**Why a verb-first skill name (`inspect-script-output`).** Three alternative names considered and rejected: `script-output-inspection` (noun-first; reads heavier in a POLYBIUS invocation), `post-script-inspection` (loses the "what is being inspected" anchor), `inspection-agent` (over-generalizes — this skill inspects script outputs specifically, not arbitrary agent-driven state). `inspect-script-output` is verb-first, names the action, reads cleanly in a POLYBIUS invocation, and leaves namespace room for future `inspect-*` skills.

## When to use this skill

Invoke when:

- An operator has just run `apply.sh` or `install.sh` against a registered workspace and wants the post-mechanical state inspected before posting any signoff that names a workspace cleanup claim (`MAJOR_PLINY.md` §5.10 partner).
- A POLYBIUS session is doing a periodic substrate-state check and wants the strangeness surface beyond what `check-substrate-updates/check.sh` pre-enumerates.
- Before kicking off a new substrate-adoption arc, sanity-check that the workspace is in a clean recognizable state (no silent name collisions, no unauthorized commits to `.claude/`, no drift verdicts that mismatch the underlying file state).

Do **not** invoke for:

- Substituting for `substrate/skills/check-substrate-updates/check.sh`. That skill computes the *known-strangeness* drift verdict; this skill scans for *novel* strangeness on top of it. Run both.
- Auto-fixing anything. This skill is informational only; emit_report writes to stdout and exits 0. Triage and fix routing is Step 3 (POLYBIUS judgment per `operating-disciplines.md` §27.2 step 3).
- Mechanically enforcing `operating-disciplines.md` §25 (PRINCIPAL-gate), §19.6 (attestation-confabulation), `MAJOR_PLINY.md` §5.10 (signoff-accuracy), or `MAJOR_POLYBIUS.md` §17 (base-vs-custom) — those integrations are A7-deferred future-arc work (see "Strangeness categories" below).

## What the skill ships

Two files:

1. `SKILL.md` — this file.
2. `check.sh` — the executable shell script, including a `--self-test` mode that generates its own synthetic strangeness fixture at runtime.

**No `fixtures/` directory.** Per Arc 33 design `agents/design/arc-33/design-rev2.md` §0d, the self-test mode builds a synthetic CLEAN + STRANGE tree in `$(mktemp -d)` at invocation time and cleans up before returning. This avoids polluting consumer workspaces with deployed fixture files (the `install.sh` `cp -R` loop deploys the whole skill subtree per skill name).

**Per-workspace state file.** Written at `<skills-parent>/.inspect-script-output-last-run` — same parent-dir mechanism as `check-bw-release/.bw-release-last-check`. At substrate-tier (the-stoa repo): `substrate/.inspect-script-output-last-run`. At consumer-tier (after `install.sh` deploy): `<workspace>/.claude/.inspect-script-output-last-run`. One line per workspace recording last-inspected HEAD SHA + ISO-8601 timestamp.

**No `.gitignore` line is needed.** The state file is filtered at runtime by the same `grep -v` mechanism `check-substrate-updates/check.sh` uses for its own state file.

## How to invoke

Three worked invocations:

- **Standard call (production):**
  ```bash
  <skill-dir>/check.sh --workspace <abs-path>
  ```
  Substrate-tier example: `substrate/skills/inspect-script-output/check.sh --workspace /c/Users/denso/claude_projects/the-stoa`
  Consumer-tier example: `<workspace>/.claude/skills/inspect-script-output/check.sh --workspace <workspace>`

- **Self-test (CI / smoke / development):**
  ```bash
  <skill-dir>/check.sh --self-test
  ```
  Builds and tears down its own synthetic CLEAN + STRANGE tree in `$(mktemp -d)`; asserts the CLEAN path emits the CLEAN message and the STRANGE path emits a finding citing both colliding file paths. No `--workspace` argument needed in this mode. Exits 0 if all assertions PASS, exits 1 otherwise. This is the canonical test path; run it after editing `check.sh` to verify the scan helpers still behave.

- **Subset of categories (debugging):**
  ```bash
  <skill-dir>/check.sh --workspace <abs-path> --only name-collisions
  ```
  Restricts the run to one category. Useful when triaging a specific surface or when re-running after a fix to verify the strangeness is gone. Comma-separated list accepted (`--only unauthorized-commits,name-collisions`).

The exit code is **always 0 on successful execution in production mode** — drift is informational, never blocks. Same exit-code discipline as `check-bw-release/check.sh` and `check-substrate-updates/check.sh`. Only `--self-test` exits 1 (and only when an assertion fails — that is a development signal, not a substrate-state signal).

## Strangeness categories

This skill ships scan helpers for three categories and explicitly defers three more to future arcs.

| Category | Status |
|---|---|
| **unauthorized-commits** — git-history scan of `.claude/` for commits not matching a substrate-canonical pattern (apply-from-substrate / install-from-substrate / prune-from-substrate). Worked example: sector-4 probe-mutation residue from Arc 26 / `stoa--501`. | Shipped this arc |
| **name-collisions** — silent-collision `name:` duplicates within one Claude-Code scope per `MAJOR_POLYBIUS.md` §17.4. The helper reads BOTH base paths (e.g., `.claude/agents/CAPTAIN_*.md`) AND custom paths (e.g., `.claude/agents/custom/CAPTAIN_*_<slug>.md`) within each scope and flags any `name:` value that appears more than once across the collected set. | Shipped this arc |
| **drift-verdict-mismatch** — if `check-substrate-updates` is deployed AND a recent `check.sh` output is cached, compare its verdict against an mtime sweep of `.claude/` and surface any inconsistency (CURRENT verdict with unexpected mtimes; DRIFTED verdict with no detail lines; etc.). | Shipped this arc |
| **cleanup-claims-not-executed** — `MAJOR_PLINY.md` §5.10 signoff-accuracy partner: verify any cleanup claim PLINY makes in a signoff against the actual filesystem state pre-signoff. | Deferred — future arc |
| **attestation-claims-not-live-verified** — `operating-disciplines.md` §19.6 attestation-confabulation partner: verify attestation claims (e.g., "tests pass", "PR open at URL X") against live state at attestation time. | Deferred — future arc |
| **PRINCIPAL-gate-clauses-encountered-but-not-paused-on** — `operating-disciplines.md` §25 PRINCIPAL-gate partner: scan an agent's transcript / verdict / commit-message-set for §25 trigger clauses that were encountered but not honored with a pause. | Deferred — future arc |

> **A7 boundary (per `substrate/arcs/arc-33-build-directive.md`):** this skill establishes the inspection-agent COMPONENT and the 3-step pattern's worked example. Per-discipline mechanical enforcement (`operating-disciplines.md` §25 PRINCIPAL-gate / `operating-disciplines.md` §19.6 attestation-confabulation / `MAJOR_PLINY.md` §5.10 signoff-accuracy / `MAJOR_POLYBIUS.md` §17 base-vs-custom / etc.) is INCREMENTAL future-arc work. The skill's shipped scan helpers cover the first three categories above (unauthorized-commits / name-collisions / drift-verdict-mismatch); the last three are deliberately deferred — a future arc dispatches the relevant integration per use case.

## How to test

`<skill-dir>/check.sh --self-test` is the single canonical test path. It exercises both the CLEAN path (a correctly-conventioned tree with no strangeness — expected output is the CLEAN message) and the STRANGE path (a tree with a planted silent-collision per `MAJOR_POLYBIUS.md` §17.4 — expected output is a finding block citing both colliding file paths).

The fixture tree is built inline by the `build_self_test_tree` function in `check.sh`. A reader of `check.sh` sees both the planted strangeness AND the assertion against it in one place; the test surface is **self-documenting in code**. If a future arc extends the scan helpers (e.g., adds quoted-`name:` handling or a multi-doc YAML case), the self-test grows assertions inline next to the new helper logic.

The self-test runs fresh every invocation (no caching). The cost is small — heredocs into `mktemp -d` and four scan helpers against ~6 small files. The discipline-property of run-fresh-every-time is worth more than the cycles saved; a cached test pass could mask a regression in a scan helper.

## State-file shape

One line at `<skills-parent>/.inspect-script-output-last-run`:

```
<HEAD-SHA> <ISO-8601-timestamp>
```

Example: `b600df7c0785475955e64132e767ebbb35e6f2f9 2026-05-17T20:30:00Z`

The state file's role is auditing — POLYBIUS can grep across consumer workspaces to see which workspaces have had a recent inspection and which haven't. First invocation bootstraps the file silently; the skill does not emit a "first run" message (mirrors `check-bw-release`'s silent-bootstrap discipline).

A future arc that wants per-category last-run tracking could extend the format to multi-line; today's one-line shape is the minimum.

## Per-workspace deployment

This skill follows the per-workspace deployment pattern established by `check-substrate-updates` and `check-bw-release`:

- `install.sh` deploys the skill subtree to `<workspace>/.claude/skills/inspect-script-output/`.
- Each workspace runs the skill against its own state file at `<workspace>/.claude/.inspect-script-output-last-run`.
- There is no cross-workspace coordination — each workspace's inspection cadence and state are local.

The substrate-tier copy at `the-stoa/substrate/skills/inspect-script-output/` runs against `substrate/.inspect-script-output-last-run`; consumer copies run against `<workspace>/.claude/.inspect-script-output-last-run`. Operators picking which workspace to inspect (and on what cadence) is a workspace-local decision; the skill is safe to invoke at any cadence (no upstream API calls, no rate limits).

## POLYBIUS triage protocol

When the skill emits a STRANGENESS DETECTED report, POLYBIUS routes findings per `operating-disciplines.md` §27.2 step 3:

- **Routine technical-tier findings → POLYBIUS fixes inline.** Per `MAJOR_POLYBIUS.md` §4.8 (fix-now) + the user-tier-approves-tech-decisions discipline. Example: a drift-verdict-mismatch caused by a stale `check.sh` cache → POLYBIUS clears the cache and re-runs the check. No PRINCIPAL pause required.
- **PRINCIPAL-gate findings → workflow PAUSES per `operating-disciplines.md` §25.3 BLOCK-not-TAG.** Autonomous mode does NOT relax. Example: an unauthorized commit on `.claude/` that touches a file under the §25 PRINCIPAL-gate scope → POLYBIUS halts and surfaces to PRINCIPAL; no remediation proceeds until PRINCIPAL disposition.

POLYBIUS is the seat that makes the routing call. The skill emits the structured strangeness report; POLYBIUS reads it and routes. PRINCIPAL is the exception-handler when the gate fires.

## What this skill is NOT

- **Not an auto-fixer.** Emits report, exits 0. Step 3 (triage) is POLYBIUS judgment.
- **Not a substitute for `check-substrate-updates/check.sh`.** That skill computes the known-strangeness drift verdict (DRIFTED + MISSING + OBSOLETE); this skill scans for *novel* strangeness layered on top. Run both — they are complementary, not duplicative.
- **Not a CAPTAIN-pipeline component.** The 3-step pattern names POLYBIUS as the dispatcher, not PLINY; the inspection layer runs as an operator-invokable skill, not as a gauntlet phase. Option γ (new CAPTAIN_INSPECTOR seat) is deferred per Arc 33 design `agents/design/arc-33/design-rev2.md` §3.1 to a future arc if the skill pattern proves out across multiple domains AND gauntlet-pipeline integration is warranted.
- **Not a multi-source release tracker.** Single-workspace per invocation. Cross-workspace audit is a POLYBIUS-driven walk of the registered consumer-workspace list, not a per-invocation feature.
- **Not authenticated.** No GitHub token, no API key. The skill reads filesystem state and (optionally) git history; no network calls.
- **Not a CAPTAIN_VERA envelope extension.** Both seat-level β (extending VERA's envelope) and probe-level β (re-using VERA probes for post-mechanical inspection) were rejected at Arc 33 design `agents/design/arc-33/design-rev2.md` §3.1 on one-job-per-agent and dispatch-scope grounds.

## Related

- `operating-disciplines.md` §27 — the canonical home for the 3-step mechanical-script / agent-inspection split pattern.
- `operating-disciplines.md` §25 — PRINCIPAL-gate discipline; the triage-step partner for Step 3.
- `operating-disciplines.md` §23 + `MAJOR_POLYBIUS.md` §17 — base-vs-custom universal scoping; the discipline the inspection-agent layer respects.
- `MAJOR_POLYBIUS.md` §17.4 — silent-collision footgun (duplicate `name:` field values within one scope); load-bearing canon for the `scan_name_collisions` helper.
- `operating-disciplines.md` §19.6 + `MAJOR_PLINY.md` §5.10 — future-integration partners (attestation-confabulation + signoff-accuracy); deferred per A7.
- `MAJOR_POLYBIUS.md` §4.8 — fix-now routing for routine-tier findings in Step 3.
- `substrate/skills/check-bw-release/` — sibling structural model (small-scope inspection-shape skill; positive empirical anchor for the inspection-shape pattern).
- `substrate/skills/check-substrate-updates/` — script-bloat empirical anchor (489 → 893 line ship in Arc 26; live 934 downstream of Arc 29). Referenced, NOT modified per A7.
- `stoa--32b.2` — this arc's work-unit ticket.
- `stoa--32b` — parent epic (substrate-update architecture reframe).
- `stoa--32b.1` — sibling Arc 31 (PRINCIPAL-gate discipline shipped as `operating-disciplines.md` §25).
- `docs/sessions/2026-05-16-substrate-update-architecture-reframe--retro.md` §8 + §9 — load-bearing source (PRINCIPAL declaration + synthesis with §7's gate discipline now shipped as §25).
