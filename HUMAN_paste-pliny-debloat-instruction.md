Read `substrate/MAJOR_PLINY.md` and assume the project-tier orchestrator role for the-stoa.

## Your immediate intent for this session

Drive the **substrate role-file debloat + reliability architecture** epic (`stoa--xyb`) to completion — a multi-arc AUTONOMOUS engagement. First arc: the **MAJOR_POLYBIUS.md slimming pass** (`stoa--xyb.6`). After the debloat epic, work down the pre-existing open-ticket backlog (see "Backlog" below). **polybius-the-stoa is your coordination peer** (parallel session) — coordinate via bw on `stoa--xyb`.

This is the substrate team's structural-debt paydown: role files bloated to ~2000 lines and the cost is degraded adherence, not just tokens. The epic's design records (`stoa--xyb.1`–`.5`) specify the fix — composition + enforcement layers that move reliability OUT of memorized-instruction. **Acceptance bar for every debloat arc: LOSSLESS-ON-CANON** — every empirical anchor relocates to a bw cite, never dropped. That is ARGUS's primary audit target.

## Cron hygiene FIRST (before any substantive work)

1. Run **CronList**. If any orphan cron persists from a prior `/clear`'d context, **CronDelete** it.
2. Per **§6.2a** (canonical multi-arc polling pattern): **CronCreate** a `*/5 * * * *` polling cron with prompt:
   ```
   [radio-check pliny-the-stoa] Poll bw stoa--xyb for new [for: pliny-the-stoa] comments from polybius-the-stoa (sequence approvals, direction calls). If a signal awaits, read it + HUMAN_paste-pliny-debloat-instruction.md and act per MAJOR_PLINY.md §5 + §6 + §6.2a + operating-disciplines.md §7. Otherwise continue the current arc heads-down.
   ```
3. **CronCreate** a renewal cron at +144h per operating-disciplines.md §11 step 1.5. Name both cron ids in your init handshake comment on `stoa--xyb`.

## Read first (in order)

1. **`bw show stoa--xyb`** — the epic: problem, thesis (adherence-not-length), solution (composition + enforcement layers).
2. **`bw show stoa--xyb.3`** (method: 3-bucket + 3-tier content model), **`.4`** (composition layer), **`.5`** (enforcement layer) — this is your design brief. **`.1`** (CLI-not-MCP) and **`.2`** (skill-grant / agent-caching findings) are settled constraints you build within.
3. **`bw show stoa--xyb.6`** — the first execution target + the drafted 19-section map of MAJOR_POLYBIUS.md.
4. **`substrate/MAJOR_POLYBIUS.md`** — the file being slimmed (1299 lines).

## First act (before any branching)

Post your proposed **arc sequence** for the epic to `stoa--xyb` tagged `[for: polybius-the-stoa] [from: pliny-the-stoa]`, resolving two sequencing questions explicitly:

- **Does the enforcement layer (`.5`) get BUILT (hooks + checker) before, or in parallel with, the POLYBIUS cut (`.6`)?** The cut is only *safe* once the layer that replaces memorized-instruction actually exists — so build-order matters, not just spec-order. If you judge the cut safe without the enforcement layer built (because the slimming is mostly conditional-to-reference + provenance-to-cite, which stay loadable), say so and justify.
- **How do the 9 backlog tickets interleave** with the debloat arcs.

polybius-the-stoa reviews your proposal via polling and approves/adjusts. Then engage the first arc. (This single coordination round-trip is deliberate — sequencing a multi-arc engagement is a real coordination point.)

## Backlog (pre-existing open the-stoa tickets)

- `stoa--0hl` — **NOTE: in tension with the debloat.** It wants to ADD a team-deploy procedure (§5.6) to MAJOR_POLYBIUS.md, i.e. grow the file. Reconcile WITHIN the debloat (fold §5.6 in condensed form or push to reference); do not independently grow the file being slimmed.
- `stoa--2i5` — install.sh gitignore for transient paths (`.substrate-last-check`, `.claude/worktrees/`, scheduled_tasks.lock).
- `stoa--vr1` — validate-spec residue refinement (FIX1..FIX9 bundle).
- `stoa--sp1` — port 7-8 cross-substrate utility skills into substrate.
- `stoa--3na` — apply substrate canon to ariadne / sector-4 / railway workspaces.
- `stoa--tvc` — bw-fit matrix extension (descendant→ancestor edges).
- `stoa--lyw` — /resume invocation discipline.
- `stoa--myd`, `stoa--bbi` — P4 accretion items (low priority; triage for close-vs-implement).

## Pre-branch hygiene (per MAJOR_PLINY.md §5.9, before creating each arc-build branch)

```
Pre-branch hygiene per MAJOR_PLINY.md §5.9: before creating <arc>/build, run two checks.

Check 1 (no other arc-build branch in flight):
  git branch | grep -E '^\s*arc-[0-9]+/build$'    # must be empty

Check 2 (local main = origin/main):
  git fetch origin main
  git log --oneline main..origin/main             # must be empty
  git log --oneline origin/main..main             # must be empty

If either check fails, surface to polybius-the-stoa (or PRINCIPAL via [for: PRINCIPAL]
tag when peer unavailable) with the specific state observed. Do NOT silently
inherit local-ahead commits into the arc branch (bundled-squash pattern, stoa--3cs).
```

## Per-arc workflow

1. Pre-branch hygiene (above) + worktree at `.claude/worktrees/<arc>-build/` per §5.9.4.
2. Gauntlet: DAEDALUS (slim-structure design from `.3`/`.4`/`.5` + the module split + the reference/provenance destinations) → ARGUS cold-audit (**LOST CANON is the load-bearing risk**) → ADA build → VERA + CATO + ZENO. **CATO mandatory.**
3. §5.10 signoff with live-verified state; squash-merge per §5.10 canon (no `gh pr merge --body` override).
4. §5.11 paste archival on arc close; close the child ticket with cross-refs.
5. Post `[for: polybius-the-stoa] [from: pliny-the-stoa]` verdict on `stoa--xyb`.

## Operating mode

- **AUTONOMOUS** multi-arc per §6.2a + operating-disciplines.md §7.
- §28 seat-identity trailers + `[from: pliny-the-stoa]` heartbeats per §7.1 / §7.7.
- Surface to PRINCIPAL only: ship/no-ship on the epic, and genuine project-direction calls. Route technical-tier decisions to the right CAPTAIN; coordinate logistics with polybius-the-stoa on `stoa--xyb`.

## Recovery

If `/compact` or `/clear` erases your role: re-read this paste from `HUMAN_paste-pliny-debloat-instruction.md` at the project root. Fall back to `/resume` per the handoff-author skill.
