# Arc 26 build directive — Substrate-update check, full-picture detection

**Audience:** the fresh Claude Code session opened to build Arc 26 deliverables (MAJOR_PLINY at the-stoa tier).
**Authored by:** user-tier MAJOR_POLYBIUS + the PRINCIPAL (Denson Smith).
**Status:** active directive. **Arc 25 (`stoa--p5g`) is CLOSED** — precondition satisfied.
**Bw ticket:** `stoa--dxw` (the work-unit; itself the arc's coherent scope — no parent epic).
**Builds on:** Arcs 1-25 (the-stoa main as of 71ea092).

**Your one job:** extend `substrate/skills/check-substrate-updates/check.sh` so the full picture of substrate state surfaces at detection time. Today check.sh only handles DRIFTED (existing files differ). The 2026-05-16 Arc-25 drift apply to three consumer workspaces (railway--l7o, ariadne--kwo, s4--3jp) revealed two silent gaps: MISSING (source has, workspace doesn't) and OBSOLETE (workspace has, source dropped). Plus uncommitted .claude/ state at apply-time is a manual pre-flight today; bake it into detection. The verdict CURRENT must mean "workspace is fully aligned with source," not "the files we already happen to know about match." Close the silent-CURRENT cliff.

One ticket, one coherent push:
- **stoa--dxw** (P2) — Substrate fix: check.sh extension covering MISSING + OBSOLETE + uncommitted-state surfacing, output format that routes operator to the right tool per category, SKILL.md doc update.

This is a focused arc. ~1-2 files edited (check.sh, SKILL.md). Architectural decisions are LOCKED in this directive — your Phase 1 work is structural (turning the locked decisions into file-by-file edit specs), not deliberative.

---

## Comms — autonomous mode via bw, radio-check protocol

PROJECT-TIER POLYBIUS (separate Claude Code session, activated from the activation paste) is your radio-check peer. You and project-tier POLYBIUS communicate via comments on `stoa--dxw`. USER-TIER POLYBIUS dispatched this arc; user-tier may post cross-workspace context comments periodically but is NOT your radio-check peer — project-tier is. User-tier is exception-handler alongside PRINCIPAL.

PRINCIPAL is **not** the relay for routine status — beadwork is.

**bw command syntax** is in `substrate/MAJOR_PLINY.md` §6.1. Critical: `bw comment <id> "text"` is positional, no `--body` flag. `bw close <id> --reason "text"` — `--reason` is a flag.

**Polling discipline** per `substrate/operating-disciplines.md` §7 (surface-and-wait + radio-check). On dispatch, post an initialization handshake comment on `stoa--dxw` naming your cron id (if you set one up) and your cadence. Heartbeat every ≤30 min unless surface-and-wait-blocked.

PLINY is in autonomous mode for this engagement. PRINCIPAL + user-tier POLYBIUS are exception-handlers — project-direction calls, ship/no-ship, substance disagreement after one round, authorship/copyright/Denson-final-say content, irreducible ambiguity, peer silence > 60 min, arc closes.

---

## Read first

Before any design or build work, read in order:

1. **`stoa--dxw` ticket body in full.** Primary spec. Problem statement + the three-category framing + the deliverables list + acceptance criteria + out-of-scope list + the honest-gaps-Option-B-leaves note. Treat ticket body as primary input prose.

2. **`substrate/skills/check-substrate-updates/SKILL.md`** — full read. Especially the "How the substitution-coupling works (operational note)" section — the cite-comment-at-the-read-site mitigation pattern is the canonical model your new source-side enumeration should follow.

3. **`substrate/skills/check-substrate-updates/check.sh`** + **`apply.sh`** — full read of both. Understand the existing `apply_substitutions()` function (the coupling-mitigation precedent), the per-workspace iteration, the `.substrate-last-check` state-file write.

4. **`substrate/install.sh`** — read SKILL_NAMES (~line 140), the CAPTAIN deploy loop, the templates deploy loop, and the `--prune-obsolete` handling. The source enumeration check.sh needs to do mirrors install.sh's deploy enumeration; the cite-comment pattern is the durable mitigation.

5. **`agents/design/stoa--lyh/design.md`** — Option Small design rationale. The four-category-drift-classification was the v2 architecture; PRINCIPAL ratified Option Small after DAEDALUS-light pass. Arc 26 does NOT revisit that decision. Locally-modified × upstream-advanced stays out of scope (see L8).

6. **`agents/design/stoa--lyh/v2-marker-architecture-future-work.md`** — preserved for context only. Per-file marker is NOT in Arc 26 scope.

7. **HANDOFF_POLYBIUS_2026-05-16.md** at repo root — engagement context for why the gap surfaced when it did.

---

## Phase A — Architectural decisions (LOCKED pre-dispatch)

Settled during ticket evolution + this directive authoring + PRINCIPAL's Option-B selection 2026-05-16. You do NOT surface these as design questions.

### A1. One arc, four phases, one gauntlet — LOCKED

`stoa--dxw` is a coherent single work-unit (no children). Single DAEDALUS design covering all check.sh extensions + SKILL.md update. Single ARGUS audit. Single ADA worktree on `arc-26/build`. Verifiers (VERA + CATO + ZENO) each one pass over the integrated diff. CATO is mandatory (not optional) — the SKILL_NAMES parsing coupling is a wording-precision concern CATO catches well.

Phasing:

| Phase | Seat(s) | Output |
|---|---|---|
| 1 | DAEDALUS + ARGUS | `agents/design/arc-26/design.md` — integrated design covering: check.sh source-side enumeration approach (A3), OBSOLETE detection scope (A4), uncommitted-state detection (A5), output format (A6), SKILL.md doc updates (A7). ARGUS cold-audits before ADA dispatches. |
| 2 | ADA | feature branch `arc-26/build` covering check.sh extension + SKILL.md doc update. |
| 3 | VERA + CATO + ZENO | parallel verification pass. VERA executes the acceptance probes (synthetic OBSOLETE + synthetic MISSING + uncommitted-state test fixtures per stoa--dxw acceptance section). CATO cold-reads entire diff for wording drift / cite-comment correctness / scope creep / output-format coherence. ZENO checks spec-vs-result against stoa--dxw deliverables 1-7. |
| 4 | PLINY + smoke + ship | smoke beats (check.sh against all three current consumer workspaces post-build; verify all still report CURRENT or surface meaningful new state; verify exit code stays 0; verify existing DRIFTED-only behavior is byte-equal to pre-Arc-26). PR opened. PLINY runs `gh pr merge` after clean PASS. `stoa--dxw` closes. |

### A2. Three detection categories — LOCKED

Per stoa--dxw ticket body:

| Type | Definition |
|---|---|
| **DRIFTED** | File exists in both source and workspace; content differs after apply_substitutions. (existing behavior; do not regress) |
| **MISSING** | File exists in source-side enumeration; workspace doesn't have it at the substituted destination path |
| **OBSOLETE** | File exists in workspace at a substrate-deployable path; source doesn't have it |

Plus separately surfaced (NOT a drift category — a pre-flight signal):

- **Uncommitted .claude/ state** — count of modified + untracked files under workspace's .claude/, excluding `.substrate-last-check` (transient state-file, not signal)

### A3. Source-side enumeration approach — LOCKED with one DAEDALUS sub-decision

check.sh enumerates three source-side sets:

1. **Skills:** parse SKILL_NAMES from `substrate/install.sh` (~line 140). Each name maps to `substrate/skills/<name>/` (source) and `<workspace>/.claude/skills/<name>/` (deployed).
2. **CAPTAINs:** glob `substrate/CAPTAIN_*.md`. Each maps to `<workspace>/.claude/agents/<basename>` with {{NAME_SUFFIX}} substitution applied to filename.
3. **Templates:** glob `substrate/templates/*.md`. Each maps to `<workspace>/.claude/templates/<basename>`.
4. **Top-level role files + canon:** `substrate/MAJOR_*.md`, `substrate/operating-disciplines.md`. Each maps to `<workspace>/.claude/<basename>` with {{NAME_SUFFIX}} applied to MAJOR filenames.

**DAEDALUS sub-decision:** for SKILL_NAMES specifically — parse install.sh array via shell extraction (e.g. `sed`/`awk` block targeting the SKILL_NAMES=(...) form) OR import via sourcing install.sh in a controlled scope. Pick one; document rationale in design.md. ARGUS confirms the choice doesn't create accidental execution-side-effects from sourcing.

**Cite-comment mitigation:** wherever check.sh parses install.sh, place a cite-comment at the parse site pointing back to the install.sh line numbers being parsed. Same pattern as the existing `apply_substitutions()` cite-comment. The cite-comment is the durable mitigation for source-side coupling — surfaces the linkage at the read site.

### A4. OBSOLETE detection scope — LOCKED

OBSOLETE detection enumerates **only files at substrate-deployable paths**:

- `<workspace>/.claude/MAJOR_*.md`
- `<workspace>/.claude/operating-disciplines.md`
- `<workspace>/.claude/agents/CAPTAIN_*.md`
- `<workspace>/.claude/templates/*.md`
- `<workspace>/.claude/skills/*/` (directory-level — each top-level subdir maps to one skill name)

Files in `<workspace>/.claude/` outside these paths are user-added artifacts (e.g., `.substrate-last-check`, project-specific custom agents the operator dropped in, HUMAN_*.md instruction files). These are NOT flagged OBSOLETE.

Pattern: if a file at one of the deployable paths matches the basename pattern but the source-side enumeration doesn't include it, report OBSOLETE.

Example: prior substrate had `substrate/skills/railway-access/`. Arc 25 deleted it from SKILL_NAMES + source. A workspace deployed before Arc 25 would still have `.claude/skills/railway-access/`. check.sh post-Arc-26 reports this as OBSOLETE.

### A5. Uncommitted-state detection — LOCKED

Per workspace, count:

- `git status --porcelain .claude/ | grep -v '\.substrate-last-check$' | wc -l`

Surface as part of the per-workspace summary line. If count > 0, emit a pre-flight warning in the output explaining that `apply.sh --yes` would auto-commit-then-overwrite (semantically destructive if the local edit was intentional).

Workspace must be inside a git repo for this signal to work. If `.claude/` is not git-tracked or workspace is not a git repo, surface as "uncommitted-state: unknown (workspace not git-tracked)" — informational, not blocking.

### A6. Output format — LOCKED structurally, fonts/spacing DAEDALUS's call

Per-workspace summary line:

```
<workspace-name>            <verdict> (<N> drifted, <M> missing, <K> obsolete; <U> uncommitted)
```

`<verdict>` is one of: `CURRENT` (N=M=K=0), `DRIFTED` (N>0 only), `MISSING` (M>0 only), `OBSOLETE` (K>0 only), or composite `DRIFTED + MISSING + OBSOLETE` (any combination).

Per-category detail blocks (only emitted for non-zero categories):

```
  DRIFTED:
    - <path>     (<delta> lines)
  MISSING:
    - <path>     (new in source)
  OBSOLETE:
    - <path>     (dropped from source)
```

Routing footer (always emitted for non-CURRENT workspaces):

```
  Run apply.sh --workspace <ws> for drifted.
  Run install.sh --target <tier> --project-dir <ws> for missing.
  Run install.sh --target <tier> --project-dir <ws> --prune-obsolete for obsolete (destructive — confirm).
```

If uncommitted > 0:

```
  WARNING: workspace has <U> uncommitted .claude/ changes. apply.sh --yes
  will auto-commit-then-overwrite; preserve the local edits via git history.
  Inspect with: cd <ws> && git status --short .claude/
```

DAEDALUS may refine whitespace, color, line lengths — but the structural shape (per-workspace verdict line, per-category detail blocks, routing footer, uncommitted warning when applicable) is locked.

### A7. SKILL.md doc updates — LOCKED scope

Sections to update:

- **Output classifications table** (currently lists CURRENT, DRIFTED, NOT-STOA-DEPLOYED, NOT-FOUND, USER-TIER): add MISSING, OBSOLETE rows.
- **How to invoke section:** document the new categories' meaning and that apply.sh handles DRIFTED only; MISSING needs install.sh; OBSOLETE needs install.sh --prune-obsolete.
- **What this skill is NOT section:** unchanged (the bullet "Not an auto-deployer" still holds — Arc 26 surfaces, doesn't auto-resolve).
- **v0 scope and limitations section:** add a paragraph noting that local-vs-upstream attribution of DRIFTED remains Option Small (PRINCIPAL ratified); Arc 26 closes detection-cliff but NOT the attribution gap. Cross-ref the honest-gaps note in stoa--dxw body.
- **How the substitution-coupling works section:** extend with the new SKILL_NAMES parsing coupling. Same cite-comment-at-the-read-site mitigation pattern.

### A8. Out of scope — HARD LOCKED

Do NOT do in this arc, even if the temptation surfaces during build:

- **User-tier check support.** Covered by stoa--bj5 (open ticket). Orthogonal axis.
- **Auto-discovery of workspaces.** Option Small ratified explicit registry; not revisited.
- **Four-category drift classification** (locally-modified × upstream-advanced). Option Small explicitly rejected this. Reopening it is its own arc.
- **apply.sh --add-missing or --remove-obsolete.** Option B's whole point is preserving the seam; growing apply.sh into install.sh's territory defeats it.
- **consumer-workspaces.txt format change.** Unchanged.
- **Removing the existing apply_substitutions cite-comment pattern.** It's the model the new check.sh additions follow.

If you find yourself reaching for any of the above during build, STOP and surface as a peer-disagreement comment on `stoa--dxw` (radio-check to user-tier POLYBIUS). Do NOT silently expand scope.

---

## Phase B — Verify (probes from stoa--dxw acceptance section)

VERA executes these as her probe set:

1. **OBSOLETE probe:** in a test workspace clone, drop a stub `.claude/skills/fake-deleted/SKILL.md` and a stub `.claude/agents/CAPTAIN_FAKE_<slug>.md`. Run check.sh. Both must appear as OBSOLETE.
2. **MISSING probe:** temporarily add a non-existent skill name to SKILL_NAMES locally (e.g. `fake-new`). Run check.sh against a workspace. Must report MISSING. Revert SKILL_NAMES after the test.
3. **Uncommitted-state probe:** create a modified file in a workspace's `.claude/` (e.g., `echo test >> .claude/MAJOR_POLYBIUS.md`). Run check.sh. Must report uncommitted count >= 1 + warning. Revert after.
4. **Routing footer probe:** check.sh output for a DRIFTED+MISSING+OBSOLETE workspace must name apply.sh, install.sh, install.sh --prune-obsolete explicitly with workspace paths filled in.
5. **CURRENT regression probe:** check.sh against all three current consumer workspaces (post-Arc-25 drift apply) must still report CURRENT — no false positives.
6. **Exit code probe:** all of the above runs return exit code 0. Drift is informational; never failure.
7. **apply.sh non-regression probe:** apply.sh against a workspace with only DRIFTED state behaves byte-equal to pre-Arc-26 (per stoa--dxw deliverable 6).

CATO cold-reads:
- the diff for wording drift, scope creep, cite-comment placement at every new install.sh parse site, output-format coherence (does the user actually understand what to run from the routing footer?), SKILL.md updates for accuracy.

ZENO checks stoa--dxw deliverables 1-7 each marked DONE by an artifact reference.

---

## Phase C — Smoke + ship

PLINY's smoke beats before opening PR:

- check.sh against each of `/c/Users/denso/claude_projects/ariadne-core-workspace`, `/c/Users/denso/claude_projects/railway_stoa`, `/c/Users/denso/claude_projects/sector-4` — all must still report CURRENT.
- check.sh no-args sweep — must enumerate all three workspaces and report all CURRENT.
- A targeted MISSING probe (per Phase B #2) and OBSOLETE probe (per Phase B #1) run live against a throwaway workspace OR against the-stoa workspace itself, then reverted.
- `grep -n "cite" substrate/skills/check-substrate-updates/check.sh` — must show the new cite-comment(s) for SKILL_NAMES parsing.

PR title: `Arc 26: substrate-update check — full-picture detection (MISSING + OBSOLETE + uncommitted state)`
PR body: cross-ref stoa--dxw, the prior stoa--lyh design (Option Small), the Arc 25 drift apply tickets (railway--l7o, ariadne--kwo, s4--3jp) that surfaced the gap, and this directive at substrate/arcs/arc-26-build-directive.md.

Merge via `gh pr merge` after clean gauntlet PASS. Close stoa--dxw with `--reason` referencing the merge commit.

---

## Honest scope reminder

Smaller than Arc 25. One skill, two files (check.sh, SKILL.md), three coherent extensions. Architectural decisions LOCKED. PLINY heads-down should run in well under Arc 25's wall-clock (Arc 25 was ~15 min PLINY-side per the TIMING_LOG at commit 49b1dd5). If you find yourself an hour in without a green ADA verdict, surface — something's off.

End directive.
