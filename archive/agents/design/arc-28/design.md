# Arc 28 design — bw 0.13.0 substrate adoption (B.3 + B.4) + bw-upgrade discipline (C.1 + C.2)

**Ticket:** `stoa--s6n`
**Branch:** `arc-28/build`
**Worktree:** `C:\Users\denso\claude_projects\the-stoa-arc-28`
**Directive:** `substrate/arcs/arc-28-build-directive.md` (A1-A8) + `bw show stoa--s6n` 2026-05-17T02:59:14Z user-tier POLYBIUS adjudication + 2026-05-17T03:00:04Z project-tier POLYBIUS translated scope (the two comments override the directive's A2 B.1 / A2 B.2 / A4 wording per forward-only-no-retro-edit convention).
**Authored by:** CAPTAIN_DAEDALUS_the_stoa, on behalf of the PRINCIPAL (Denson Smith).

---

## §1 — Problem statement

bw upstream tagged 0.13.0 on 2026-05-11 (per `ariadne--c71`). The release shipped four candidate substrate-touching features: a host-local repository registry, cross-repo prefix resolution, ticket attachments, and a cursor-driven `bw recap` view. Ariadne already adopted 0.13.0 on the deployment side (Railway container Dockerfile bump at `ariadne-core` main `b7f92e5`; six gates green, including the `/api/bw` subprocess paths). This arc closes the substrate-side adoption decision in two parts:

**Part B (substrate adoption — what stands after adjudication):** document `bw attach` and `bw recap` in `MAJOR_POLYBIUS.md` §16 as **available primitives** (operator picks; not forced migration; existing on-disk handoff/retro/design artifacts stay where they are).

**Part C (the generalization):** encode a `bw-upgrade discipline` as a new `operating-disciplines.md` §22, and ship a lightweight `check-bw-release` skill at `substrate/skills/check-bw-release/` that operationalizes the discipline's first step (trigger detection).

### What was descoped, and why (the empirical hand the team played)

Directive A2 B.1 (`bw registry list` replaces `consumer-workspaces.txt`) and A2 B.2 (cross-repo prefix-resolution doc) were LOCKED pre-dispatch. PLINY ran a verify-then-execute probe per `operating-disciplines.md` §4.3 before drafting and surfaced (at `stoa--s6n` 2026-05-17T02:00:03Z) that on this Windows install `bw registry list` returns empty regardless of `registry.auto=true`, fresh `bw init`, every invocation path, every `bw sync`; `bw registry add` does not exist as a subcommand. The intended "auto-registers after every successful command" branch is firing into "silent on failure" (confirmed via `gh pr view 125 -R jallum/beadwork`). Project-tier POLYBIUS independently reproduced (02:03:15Z) and surfaced to user-tier authority.

User-tier POLYBIUS adjudicated 02:59:14Z (PRINCIPAL declaration): option (a) descope. B.1 + B.2 + A4 dropped; B.3 + B.4 + C stand; no follow-up ticket per §4.8 deferred-work-with-no-plan guidance (no concrete operational pain motivates a pre-filed ticket; if/when `consumer-workspaces.txt` becomes annoying we file then). The descope IS evidence for the discipline being encoded in C.1: today's surprise (changelog claim vs CLI reality) is the canonical worked example for the "verify changelog claims empirically before locking adoption decisions" sub-bullet that user-tier POLYBIUS flagged as optional and project-tier POLYBIUS' 03:00:04Z translated scope re-flagged as MANDATORY for this design.

### In scope: 4 deliverables

1. `substrate/MAJOR_POLYBIUS.md` — add `§16.8 bw 0.13.0 available primitives — attach + recap` (B.3 + B.4).
2. `substrate/operating-disciplines.md` — append new `§22 bw-upgrade discipline` (C.1).
3. `substrate/skills/check-bw-release/SKILL.md` + `check.sh` — new skill (C.2).
4. `substrate/install.sh` — append `check-bw-release` to the `SKILL_NAMES` array (deployment registration; the smoke beat at §5 verifies the append fires through `--dry-run`).

### Imported assumptions (named per §6.1 restatement gate)

- The descope of B.1+B.2 is treated as authoritative; this design does not re-derive the registry decision. If `bw registry list` starts working on Windows during the build window, ADA does not adopt it mid-arc — the descope holds for this arc and a future arc revisits per §22's own discipline.
- "Forward-only" is the universal frame for B.3+B.4: this design specifies what NEW artifacts MAY do; it specifies nothing about existing on-disk artifacts and explicitly refuses to recommend migration (A7 hard-lock).
- `MAJOR_POLYBIUS.md` is the right locus for both B.3 and B.4 (§16 POLYBIUS lifecycle, not §7 Communication). Rationale at §2.1.
- The N=1 honesty frame from Arc 27 §16.6 is the structural template C.1's "N=1 provenance + accretion path" subsection follows.
- The C.2 skill is shaped as a near-clone of `check-substrate-updates` in directory layout, state-file convention, cite-comment policy, and `--help` extraction style — operator muscle memory carries across the two skills.

---

## §2 — Architectural decisions

### 2.1 Section-placement decisions

**B.3 + B.4 placement: `MAJOR_POLYBIUS.md` §16.8 (single combined subsection), not split across §16 + §7.**

The directive (A2 B.4) explicitly allowed "and/or §7" for `bw recap`. The B.4 worked example named by the directive — "POLYBIUS picking up after compaction can run `bw recap` to see what's happened since its last read-point" — is a §16 lifecycle event, not a §7 communications-pattern event. `bw attach` (B.3) is unambiguously §16.3 multi-artifact-handoff adjacent. Splitting them would force a reader cross-walking the lifecycle to hop between §7 and §16; combining them at §16.8 keeps the lifecycle-relevant primitives co-located after the existing §16.7 Cross-references.

§16.7 currently terminates with `Standby, run.` (line 926 in the on-disk file). §16.8 inserts BEFORE that closer; the new closer for §16 stays `Standby, run.` after §16.8. The §16.7 Cross-references subsection itself gains one bullet pointing at the new §16.8.

**C.1 placement: `operating-disciplines.md` §22 (append after §21 Ariadne-search-ready authoring).**

The current operating-disciplines.md terminates at §21 (line 946-967) followed by an `Agent-regime inverses (positive framing)` block + `Empirical lineage` block at file tail (lines 968-991). C.1 inserts as `## 22. bw-upgrade discipline` AFTER §21 and BEFORE the `Agent-regime inverses` block — the file structure of "numbered disciplines, then the inverses block, then the lineage block" stays intact.

The path-of-least-disruption alternative would have been to nestle the discipline under §12 `bw cookbook` as `§12.N`. Rejected: §12 is operational cookbook (commands + worked examples); §22 is a process discipline (the 5-step Trigger→Review→File→Dispatch→Verify shape). Different shape, different reader expectation. §12 gets a forward-pointer added to §22 as a cross-ref (§22 cites §12 for cookbook commands; §12 stays unchanged in this arc per A7's "edit no more than necessary" implicit corollary).

### 2.2 C.2 skill design (concrete picks)

**State file format:** plain text, single line, just the tag (e.g., `v0.13.0\n`). Picked over the key=value form `check-substrate-updates` uses because there is exactly ONE piece of state worth persisting (the last-seen tag); a timestamp adds nothing actionable (the file's `mtime` is the timestamp). Simpler is better; the parse code is one `cat | tr -d '\n'`. State-file path: `substrate/.bw-release-last-check` (substrate-level per directive A3 C.2).

**GitHub API endpoint:** `https://api.github.com/repos/jallum/beadwork/releases/latest`. Picked over the `gh release view --latest -R jallum/beadwork` form because `gh` is not a guaranteed dependency on consumer workspaces, while `curl` is a universal substrate-script tool already in use (cf. ariadne's Dockerfile pattern). The API returns JSON; the field to parse is `tag_name` (cite-comment at the parse site per A5). No authentication required for public-repo release reads; rate limit is 60/hour unauthenticated which is far above any plausible check cadence. The endpoint is documented at https://docs.github.com/rest/releases/releases#get-the-latest-release (verified live 2026-05-17 via the Read tool's WebFetch capability is not required here — the endpoint is named in current GitHub REST docs and has been stable for years; if it ever rotates, the cite-comment surfaces the linkage at the read site, same mitigation pattern as `apply_substitutions`).

**Argument parsing:** mirror `check-substrate-updates/check.sh` shape — `set -euo pipefail`, while-case loop over `$@`, support `-h|--help` (extract the head-of-file comment via `sed -n /^# check\.sh/,/^# .*not failure\.$/p $0 | sed 's/^# \{0,1\}//'`). Two flags beyond `--help`:

- `--force-check` — bypass any rate-limiting/cache logic. The skill ships with no rate-limiter (state file is just a tag, not a timestamp), so `--force-check` is a no-op flag reserved for forward-compat if a future arc adds caching. Document it; the spec keeps the flag's surface stable across that future.
- `--baseline <tag>` — override the state file's stored tag for this invocation (testing-side use; lets fixtures inject a stale baseline without writing the state file).

No `--workspace` argument. The skill is single-target by nature (it checks one upstream releases feed, not per-workspace anything). Document explicitly that this is single-target.

**Test fixture mechanism:** environment variable override, **two** vars (one for upstream-latest mocking, one for baseline mocking):

- `BW_RELEASE_CHECK_LATEST_OVERRIDE=<tag>` — when set, skip the API call and use this as the upstream-latest tag. Picked over file-based mock because env-var override is grep-able, stateless (no file to clean up between tests), and idiomatic for shell-script fixtures (Arc 25 credential-discipline uses the same shape per its SKILL.md).
- `BW_RELEASE_CHECK_BASELINE_OVERRIDE=<tag>` — when set, skip reading the state file and use this as the baseline. Test-only; production callers never set it.

Both vars are scoped to a single invocation. Document the mechanism inline in `check.sh` at the env-var read site (cite-comment shape per A5) AND in `SKILL.md` "How to test" section with three worked invocations: (a) at-current (both vars set to v0.13.0 → "current"); (b) new-release-detected (LATEST_OVERRIDE=v0.99.0 + BASELINE_OVERRIDE=v0.13.0 → "new release detected" + axis template); (c) live (no overrides, no `--baseline`, against bw 0.13.0 → expect "current" today).

### 2.3 Cite-comment policy applied to C.2 parse site

A5 narrowed to one surface in this arc: the GitHub releases API JSON parse in `check.sh`. The cite-comment lives at the parse site (not at the top of the file) and names: the endpoint, the field parsed (`tag_name`), and the mitigation framing — same model as `check-substrate-updates/check.sh:135-156` `parse_skill_names_from_install`. Shape spec:

```bash
fetch_latest_release_tag() {
  # CITE: queries https://api.github.com/repos/jallum/beadwork/releases/latest
  # and parses the .tag_name field. If GitHub rotates the releases endpoint, or
  # if jallum/beadwork ever moves to a different org or repo name, this function
  # must update both the URL and (if the response shape changes) the parse. The
  # cite-at-the-read-site pattern is the durable mitigation for source-side
  # coupling — surfaces the linkage at the read site, not at code-review time.
  # Same mitigation pattern as check-substrate-updates/check.sh apply_substitutions
  # and parse_skill_names_from_install. See operating-disciplines.md §22 Step 2
  # for the broader "verify changelog claims empirically" discipline this skill
  # implements.
  #
  # FAILURE-MODE SYMPTOM: if curl returns non-200 or jq/python-json returns empty,
  # the function echoes empty string; caller treats empty as "could not check"
  # and exits with a friendly message (not a hard error — this is informational
  # tooling, not blocking).
  ...
}
```

The parse uses Python (`python3 -c "import json,sys; print(json.load(sys.stdin)['tag_name'])"`) rather than `jq`. Python is the substrate's established cross-platform dependency (see `operating-disciplines.md` §13 PYTHONUTF8=1 discipline); `jq` is not. Cite-comment names this trade-off at the parse site so a future maintainer doesn't "improve" it to `jq` without registering the dependency surface.

---

## §3 — File-by-file deliverable plan

### File 1: `substrate/MAJOR_POLYBIUS.md` — add §16.8

**Insertion locus:** between current line 923 (end of §16.7 Cross-references) and current line 924 (`---` separator preceding `Standby, run.`). New subsection slots in cleanly before the file's terminator.

**New heading + section spec (ADA authors the prose; this design names the load-bearing structure):**

```
### 16.8 bw 0.13.0 available primitives — attach + recap

Two primitives from bw 0.13.0 are available to POLYBIUS as forward-only
options. Neither is forced migration; existing on-disk handoff/retro/design
artifacts stay where they are (per A8 forward-only convention shared with
§16.4 Ariadne-search-ready authoring).

#### bw attach — multi-artifact ticket binding

  bw attach <ticket-id> <file-path> [--name <stored-path>]

Reads <file-path> from disk and stores its bytes at
attachments/<ticket-id>/<stored-path> on the beadwork ref; commits a
single-line intent comment ("attach <ticket-id> <stored-path>"). The
stored-path defaults to filepath.Base of <file-path>; --name takes a
verbatim path that may contain "/".

Use case (forward-only): when POLYBIUS authors a multi-artifact handoff
(§16.3), the index doc + linked artifacts can OPTIONALLY be bound to the
parent handoff ticket via bw attach rather than only living on disk. The
trade-off:
- on-disk: visible via filesystem + git diff; familiar to PRINCIPAL review;
  loses cohesion if the file is moved/renamed without updating the ticket.
- attached: cohesion with the ticket survives renames; less discoverable
  via filesystem grep; adds bytes to the beadwork ref.

POLYBIUS picks per artifact. Existing on-disk handoff/retro/design
artifacts are NOT migrated retroactively (A7 hard-lock).

#### bw recap — cursor-driven incremental activity view

  bw recap [WINDOW] [--since DATE] [--all] [--verbose] [--json] [--dry-run]

Summarizes activity across registered repos. First-time runs show the last
24 hours; subsequent runs show activity since the last recap (cursor-
driven). WINDOW tokens accepted: today, yesterday, week, durations like
15m / 1h / 3h30m / 24h / 2d / 7d / 2w. --since takes RFC3339 or
YYYY-MM-DD. --dry-run shows activity without advancing the cursor.

Use case (forward-only): POLYBIUS picking up after /compact (or a fresh
Mode 1 session-continue per §16.2) can run bw recap to see what has
landed across watched repos since the previous read-point. Pairs with
the handoff doc as a complementary signal: handoff says "what is the
current intent"; recap says "what has happened lately."

Caveat (this install, 2026-05-17): bw recap operates against the bw
registry. On Windows the registry has been empirically observed to
remain empty regardless of registry.auto=true (per stoa--s6n
2026-05-17T02:00:03Z probe trail; cross-ref §22 Step 2). When the
registry is empty, bw recap returns activity for ONLY the current
repo (the cwd-detected one). For multi-repo recap on this install,
invoke once per repo via cd-and-recap rather than relying on --all.
When/if the registry becomes populated, --all does the right thing
without skill change.

#### Cross-references

- §16.3 (handoff is multi-artifact, not single-doc) — the conceptual
  parent for bw attach's use case.
- §16.2 Mode 1 (handoff + compaction) — the lifecycle event bw recap
  serves.
- operating-disciplines.md §22 (bw-upgrade discipline) — the broader
  framing under which these primitives were adopted from bw 0.13.0.
- operating-disciplines.md §12 (bw cookbook) — for full bw command
  syntax and per-command flag reference.

Standby, run.  [REPLACES the existing closer at end of §16]
```

ADA verbatim-copies the `bw attach` and `bw recap` flag listings from `bw <cmd> --help` to keep them faithful to the installed CLI. The §16.7 Cross-references subsection gains one new bullet at its end:

```
- **§16.8 (bw 0.13.0 available primitives).** The two forward-only primitives — bw attach and bw recap — adopted from bw 0.13.0 per Arc 28 (stoa--s6n).
```

### File 2: `substrate/operating-disciplines.md` — append §22

**Insertion locus:** between current line 967 (end of §21's empirical-anchor paragraph) and current line 968 (`---` separator preceding the `Agent-regime inverses` block). The numbered-disciplines run §1-§21 today; §22 extends the run and the `Agent-regime inverses` + `Empirical lineage` blocks stay at file tail.

**New section spec (5 steps + 3 axes + N=1 anchor + verify-changelog-empirically sub-bullet + empirical-anchor pointer; ADA authors the prose):**

```
## 22. bw-upgrade discipline

bw is upstream-tagged. Future bw releases will land features that touch the
substrate at deployment, substrate, or workspace surfaces. The discipline
below names the 5-step process for handling each release + the 3-axis
impact-classification frame that informs filing.

### 22.1 The 5-step process

1. **Trigger.** A new bw release is tagged upstream. Detection is either
   manual (operator visits the releases page) or via the substrate/skills/
   check-bw-release skill (see §22.4 below) run on-demand or via operator-
   scheduled cron. The trigger step is INFORMATIONAL — what fires next is
   POLYBIUS judgment.

2. **Review.** Read the upstream changelog. Classify each feature by impact
   axis (see §22.2). Surface anything load-bearing to PRINCIPAL for
   project-direction before filing.

   - **Verify changelog claims empirically before locking adoption
     decisions.** Changelog prose is the upstream's intent; CLI behavior on
     the install in question is the operational reality. The two can
     diverge — silently. Run the relevant primitives against the local
     install BEFORE writing directive A-decisions that LOCK the adoption
     shape. The verify-then-execute discipline (§4.3) is the universal
     framing; this sub-bullet is the bw-upgrade-specific cut.

     **Worked example (canonical, N=1 anchor for this discipline):**
     `stoa--s6n` 2026-05-17. The bw 0.13.0 changelog described a
     "host-local repository registry; auto-registers repos after successful
     commands." Arc 28's directive A2 B.1 LOCKED `bw registry list` as the
     replacement for substrate/consumer-workspaces.txt. PLINY ran a
     verify-then-execute probe before dispatching DAEDALUS: on this
     Windows install, `bw registry list` returned empty regardless of
     `registry.auto=true`, fresh `bw init`, every invocation path. The
     "silent on failure" branch was firing (confirmed against `gh pr view
     125 -R jallum/beadwork`). The locked premise was empirically
     contradicted; user-tier POLYBIUS adjudicated descope at 02:59:14Z.
     The arc shipped (descoped) intact rather than building against an
     unusable primitive. Cross-ref: stoa--s6n radio-check thread
     (02:00:03Z + 02:03:15Z + 02:59:14Z + 03:00:04Z).

3. **File tickets.** One ticket per impact axis with a concrete action.
   "Track bw 0.13.0" is the §4.8 anti-pattern; a ticket without a concrete
   next step is a handwave. If an axis has no concrete action (e.g., the
   feature is not relevant to any of our deployment / substrate / workspace
   surfaces), name that explicitly in the review note rather than filing a
   placeholder.

4. **Dispatch.** Standard arcs per workspace. Deployment-side arcs typically
   ship at the affected service (Railway-deployed Ariadne, etc.); substrate-
   side arcs ship at the-stoa via the standard gauntlet; workspace-side arcs
   ship at each affected workspace.

5. **Verification.** Existing substrate consumers still work; subprocess
   call-sites in any code (bw_ingest.py-class) verified under the new
   version. The substrate's own `check-substrate-updates` skill catches
   drift at the substrate-deployment layer; per-workspace test suites cover
   subprocess-call-site regressions. The bw-upgrade is COMPLETE when all
   three axes have either filed-and-shipped tickets OR explicit "no action
   needed for this axis" review notes (per Step 3).

### 22.2 The 3-axis impact classification

Every bw release feature falls into one (or more) of three axes:

| Axis | Question | Anchor example (0.12.3 → 0.13.0) |
|---|---|---|
| **Deployment-side** | Does this require a container / service Dockerfile bump, install.sh re-run, or SHA256 update at any deployed environment? | `ariadne--c71` — Railway container Dockerfile bumped from bw 0.12.3 to 0.13.0; BW_SHA256 updated; six gates green including /api/bw subprocess paths. |
| **Substrate-side** | Does this obsolete substrate canon (skill, role-file convention, doc section), enable a new substrate pattern, or warrant a new substrate-canon section? | `stoa--s6n` (this arc) — B.3 + B.4 land as forward-only available primitives in MAJOR_POLYBIUS.md §16.8; B.1 + B.2 were attempted, descoped after empirical probe (see Step 2 sub-bullet). C.1 (this section) and C.2 (check-bw-release skill) generalize the experience. |
| **Workspace-side** | Does this risk subprocess-call-site regression in any code that shells out to bw (bw_ingest.py-class), break workspace-tier conventions, or change exit-code semantics in a way that affects existing scripts? | `ariadne--c71` 22:33:53Z gates 3-6 — verified the bw subprocess paths in ariadne's /api/bw endpoints still parse JSON correctly and return 200s. No regression detected; if any had been, a workspace-side ticket would have been filed. |

A feature MAY touch multiple axes (registry would have touched substrate + workspace — substrate via check.sh source-side change; workspace via the per-workspace registration semantics). When it does, file one ticket per axis touched.

### 22.3 N=1 provenance + accretion path

Per §6.7.1 honest-scope: PRINCIPAL declared this discipline 2026-05-17
(project-direction authority, captured at stoa--s6n thread). §6.7.1
defers to the canon-promotion gate (multiple observations + controlled
comparison + substrate-level pattern); §6.7.1 does not carve out a
separate "PRINCIPAL-declaration shortcut." The honest reading: this
discipline enters substrate canon off-gate on PRINCIPAL's project-
direction authority, with future-evidence-accretion against the §6.7.1
gate still required for promotion to "structural lesson" status.

The supporting evidence at the time of this writing:

- `ariadne--c71` (CLOSED 2026-05-16 at ariadne-core main `b7f92e5`) —
  canonical worked example of the deployment-side axis.
- `stoa--s6n` (this arc) — canonical worked example of the substrate-
  side axis, INCLUDING the Step 2 "verify changelog claims empirically"
  sub-bullet's worked example (the registry descope).
- `ariadne--c71` 22:33:53Z gates 3-6 — adjacent evidence for the
  workspace-side axis (regression-checking subprocess call sites under
  the new version).

Future bw releases (0.14.x, etc.) accrete supporting evidence per
§6.7.1 over time. If the 3-axis classification turns out wrong-shaped
(e.g., a future release surfaces a fourth axis class), future arcs
revise this section. Substrate canon is in NOW because PRINCIPAL named
the discipline today; promotion to "structural lesson" status with
multi-occurrence empirical backing is a future arc's work, not this
one's. (Same N=1 framing as Arc 27's MAJOR_POLYBIUS.md §16.6.)

### 22.4 Operationalizing Step 1 — the check-bw-release skill

`substrate/skills/check-bw-release/` operationalizes Step 1 (Trigger). On-
demand or operator-scheduled cron: queries the bw GitHub releases API for
the current latest tag, compares to a baseline stored at
`substrate/.bw-release-last-check`, and surfaces a "new release detected"
message with the 3-axis classification template (per §22.2) and a
suggested next action ("file tickets per impact axis") when the tags
differ. When tags match, prints a short "current" message.

The skill exists; the operator decides whether to cron it (no cron
defaults per directive A7). Classification + filing is POLYBIUS judgment
(Steps 2-5); the skill does not autonomously file tickets.

### 22.5 Cross-references

- §4.3 (verify-then-execute) — the universal framing the Step 2 sub-
  bullet specializes for bw upgrades.
- §4.8 (fix-now) — the discipline against filing placeholder tickets in
  Step 3.
- §6.7.1 (the N=1 canon-promotion gate this section enters off-gate on
  PRINCIPAL declaration).
- §12 (bw cookbook) — for full bw command syntax used in Step 5
  verification.
- §13 (Windows Python environment) — relevant when check-bw-release's
  Python JSON-parse is invoked at user-tier on Windows.
- MAJOR_POLYBIUS.md §16.8 (bw 0.13.0 available primitives) — the
  substrate-side adoption decision the 5-step process produced for the
  0.12.3 → 0.13.0 release.
- `substrate/skills/check-bw-release/SKILL.md` — Step 1 operationalization.
```

### File 3: `substrate/skills/check-bw-release/SKILL.md`

**New file. Frontmatter (load-bearing per A6 + stoa--uly convention):**

```yaml
---
name: check-bw-release
description: Check for new bw upstream releases and surface the 3-axis impact-classification template when one is found. Queries the bw GitHub releases API for the current latest tag, compares to a baseline stored at substrate/.bw-release-last-check, and prints either a "current" message or a "new release detected" message with changelog pointer + axis template + suggested next action (per operating-disciplines.md §22 bw-upgrade discipline). Single-target skill (checks one upstream feed, not per-workspace). Operator decides whether to cron it; no scheduling defaults. Triggers on requests like "is there a new bw release", "check bw for updates", "bw release check", "new bw version", "did bw upgrade".
author: Denson Smith
---
```

**Sections (the prose ADA writes; this design names the shape + load-bearing content):**

1. **Why this skill exists.** One paragraph. The discipline at `operating-disciplines.md` §22 names a 5-step process; Step 1 (Trigger) is the only step that's mechanical. Without a skill, the operator has to remember to check the releases page periodically; with the skill, the check is one command + the output cues the operator into Steps 2-5. Cross-ref §22 directly.
2. **When to use this skill.** Bullet list. Invoke when: PRINCIPAL asks "is there a new bw release"; operator wants a periodic check; before kicking off a new substrate-adoption arc (sanity-check that the baseline tag is still current). Do **not** invoke for: classifying features into axes (that's §22 Step 2, POLYBIUS judgment); filing tickets (that's §22 Step 3, POLYBIUS judgment); auto-applying upgrades (out of scope; if/when an arc warrants auto-apply, that's a future skill's job).
3. **What the skill ships.** Three lines: SKILL.md, check.sh, `substrate/.bw-release-last-check` (state file written at first invocation).
4. **How to invoke.** Three worked invocations:
   - `substrate/skills/check-bw-release/check.sh` — the standard call.
   - `substrate/skills/check-bw-release/check.sh --force-check` — no-op today; reserved for forward-compat if a future arc adds caching.
   - `substrate/skills/check-bw-release/check.sh --baseline v0.12.3` — override baseline for testing or recovery (if the state file is lost / corrupted).
5. **What the output is telling you.** Two cases:
   - **CURRENT:** "Current bw release: v0.13.0 (baseline matches). No action needed." Skill exits 0.
   - **NEW RELEASE DETECTED:** Multi-line output naming the new tag, the prior baseline, a pointer to the GitHub release notes URL, the 3-axis classification template (verbatim copy of §22.2 axes as a checklist), and a suggested next action ("File one ticket per impact axis touched per operating-disciplines.md §22 Step 3."). Skill exits 0. The "informational tooling, never blocks" exit-code discipline matches `check-substrate-updates`.
6. **How to test.** Three worked invocations against the env-var fixture mechanism (per §2.2):
   - **At-current:** `BW_RELEASE_CHECK_LATEST_OVERRIDE=v0.13.0 BW_RELEASE_CHECK_BASELINE_OVERRIDE=v0.13.0 check.sh` → "current".
   - **New-release-detected:** `BW_RELEASE_CHECK_LATEST_OVERRIDE=v0.99.0 BW_RELEASE_CHECK_BASELINE_OVERRIDE=v0.13.0 check.sh` → "new release detected" + axis template.
   - **Live:** `check.sh` (no overrides, no `--baseline`) → expects "current" today against bw 0.13.0.
7. **State file shape.** One line, the tag. First invocation writes baseline = upstream-latest (no "new release detected" on first run; the skill bootstraps to current). Document explicitly: there is no `--init` flag; first invocation IS the init.
8. **Cron cadence.** Out of scope per A7. Operator picks; the polling-cron-prompt template at `substrate/templates/polling-cron-prompt-template.md` is adaptable if the operator decides to cron-schedule.
9. **What this skill is NOT.**
   - Not an upgrader. Step 1 only.
   - Not a classifier. Axis classification is POLYBIUS judgment.
   - Not a multi-source release tracker. bw only; if/when other upstreams need similar tracking, file a follow-up.
   - Not authenticated. No GitHub token required; rate limit is 60/hour unauthenticated, which is far above any plausible check cadence.
10. **Related.**
    - `operating-disciplines.md` §22 — the discipline this skill operationalizes Step 1 of.
    - `MAJOR_POLYBIUS.md` §16.8 — the substrate-side adoption shape produced by the 0.12.3 → 0.13.0 run-through.
    - `substrate/skills/check-substrate-updates/` — sibling structural model.
    - `ariadne--c71` — deployment-side worked example for the same release.
    - `stoa--s6n` — this arc; substrate-side worked example.

### File 4: `substrate/skills/check-bw-release/check.sh`

**New file. Executable shell script (chmod +x at commit time per `check-substrate-updates` precedent). Structural skeleton (ADA fills in the per-function bodies; this design names the load-bearing shape):**

```bash
#!/usr/bin/env bash
#
# check.sh — check for new bw upstream releases and surface the 3-axis
# impact-classification template when one is found.
#
# Queries the bw GitHub releases API for the current latest tag, compares
# to a baseline stored at substrate/.bw-release-last-check, and prints
# either a "current" message or a "new release detected" message with
# changelog pointer + axis template + suggested next action (per
# operating-disciplines.md §22 bw-upgrade discipline). Single-target
# skill (one upstream feed, not per-workspace). First invocation
# bootstraps the baseline (no "new release detected" on first run);
# subsequent invocations compare upstream-latest to the stored baseline.
#
# Usage:
#   check.sh                                       # standard call
#   check.sh --force-check                         # no-op today; forward-compat reserved
#   check.sh --baseline <tag>                      # override baseline for testing / recovery
#   check.sh -h | --help                           # this help text
#
# Test fixtures (env-var override, single invocation scope):
#   BW_RELEASE_CHECK_LATEST_OVERRIDE=<tag>         # skip API call; use this as upstream-latest
#   BW_RELEASE_CHECK_BASELINE_OVERRIDE=<tag>       # skip state-file read; use this as baseline
#
# Output: human-readable; exit code is always 0 on successful execution.
# Drift is informational, not failure. Same exit-code discipline as
# substrate/skills/check-substrate-updates/check.sh.

set -euo pipefail

# ----- locate substrate (this script lives in <substrate>/skills/check-bw-release/) -----

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SUBSTRATE_DIR="$(cd "${SCRIPT_DIR}/../.." && pwd)"
STATE_FILE="${SUBSTRATE_DIR}/.bw-release-last-check"

# ----- argument parsing -----

FORCE_CHECK=0
BASELINE_OVERRIDE_ARG=""

while [ "$#" -gt 0 ]; do
  case "$1" in
    --force-check)
      FORCE_CHECK=1
      shift
      ;;
    --baseline)
      [ "$#" -ge 2 ] || { echo "check.sh: error: --baseline requires a tag" >&2; exit 2; }
      BASELINE_OVERRIDE_ARG="$2"
      shift 2
      ;;
    -h|--help)
      sed -n '/^# check\.sh/,/^# .*not failure\.$/p' "$0" | sed 's/^# \{0,1\}//'
      exit 0
      ;;
    *)
      echo "check.sh: error: unknown argument: $1 (try --help)" >&2
      exit 2
      ;;
  esac
done

# ----- helpers -----

# fetch_latest_release_tag: echo the latest release tag, or empty on failure.
#
# CITE: queries https://api.github.com/repos/jallum/beadwork/releases/latest
# and parses the .tag_name field. If GitHub rotates the releases endpoint, or
# if jallum/beadwork ever moves to a different org or repo name, this function
# must update both the URL and (if the response shape changes) the parse. The
# cite-at-the-read-site pattern is the durable mitigation for source-side
# coupling — surfaces the linkage at the read site, not at code-review time.
# Same mitigation pattern as check-substrate-updates/check.sh
# apply_substitutions and parse_skill_names_from_install (per Arc 26). See
# operating-disciplines.md §22 Step 2 for the broader "verify changelog
# claims empirically" discipline this skill implements (the registry surprise
# at stoa--s6n 2026-05-17 is the canonical worked example).
#
# Python (not jq): the substrate's established cross-platform dependency is
# Python (see operating-disciplines.md §13 PYTHONUTF8=1 discipline). jq is
# not a guaranteed dependency on consumer workspaces. If a future maintainer
# is tempted to "improve" this to jq, the dependency surface changes and
# this cite-comment is the surface that flags it at the read site.
#
# FAILURE-MODE SYMPTOM: if curl returns non-200 or python returns empty, the
# function echoes empty string; caller treats empty as "could not check" and
# exits with a friendly "could not reach upstream" message. This is
# informational tooling, not blocking — same exit-code discipline as
# check-substrate-updates.
fetch_latest_release_tag() {
  if [ -n "${BW_RELEASE_CHECK_LATEST_OVERRIDE:-}" ]; then
    echo "${BW_RELEASE_CHECK_LATEST_OVERRIDE}"
    return 0
  fi
  curl -fsSL "https://api.github.com/repos/jallum/beadwork/releases/latest" 2>/dev/null \
    | python3 -c "import json,sys;
try:
  print(json.load(sys.stdin).get('tag_name',''))
except Exception:
  pass" 2>/dev/null
}

# read_baseline: echo the stored baseline tag, or empty if absent.
read_baseline() {
  if [ -n "${BW_RELEASE_CHECK_BASELINE_OVERRIDE:-}" ]; then
    echo "${BW_RELEASE_CHECK_BASELINE_OVERRIDE}"
    return 0
  fi
  if [ -n "${BASELINE_OVERRIDE_ARG}" ]; then
    echo "${BASELINE_OVERRIDE_ARG}"
    return 0
  fi
  [ -f "${STATE_FILE}" ] || { echo ""; return 0; }
  tr -d '\n\r' < "${STATE_FILE}"
}

# write_baseline <tag>: persist the tag as the new baseline.
write_baseline() {
  printf '%s\n' "$1" > "${STATE_FILE}"
}

# emit_axis_template <new-tag> <old-tag>: print the 3-axis classification
# template + suggested next action. Verbatim copy of operating-disciplines.md
# §22.2 axes; if §22.2 changes, this template updates to match (cross-ref
# comment).
emit_axis_template() {
  local new="$1"
  local old="$2"
  cat <<EOF

NEW BW RELEASE DETECTED
  Current upstream:  ${new}
  Stored baseline:   ${old}
  Release notes:     https://github.com/jallum/beadwork/releases/tag/${new}

Classify each feature in the changelog by impact axis (per operating-disciplines.md §22.2):

  [ ] DEPLOYMENT-SIDE — Dockerfile bumps, install.sh re-runs, SHA256 updates
                       at any deployed environment (e.g., ariadne--c71).
  [ ] SUBSTRATE-SIDE  — obsoletes substrate canon? enables new substrate
                       pattern? warrants a new section?
  [ ] WORKSPACE-SIDE  — subprocess-call-site regression risk (bw_ingest.py-
                       class)? exit-code semantic changes?

Suggested next action: file one ticket per impact axis TOUCHED (per §22 Step 3).
"No action needed for this axis" is a valid review note for an untouched axis.

Update the baseline once tickets are filed:
  echo '${new}' > ${STATE_FILE}
EOF
}

# emit_current_message <tag>: print the "current" message.
emit_current_message() {
  printf 'Current bw release: %s (baseline matches). No action needed.\n' "$1"
}

# emit_unreachable_message: print the "could not check" message.
emit_unreachable_message() {
  cat <<EOF
check-bw-release: could not reach https://api.github.com/repos/jallum/beadwork/releases/latest
  Check network connectivity and rate limits (60/hour unauthenticated).
  Re-run with --force-check if a future caching mechanism caches a failure.
EOF
}

# ----- main -----

# FORCE_CHECK is a forward-compat no-op today (state file is just a tag, not
# a timestamp; no rate-limiting/caching to bypass). Reserved for if a future
# arc adds caching. Suppress unused-var warning under set -u.
: "${FORCE_CHECK}"

latest="$(fetch_latest_release_tag)"
if [ -z "${latest}" ]; then
  emit_unreachable_message
  exit 0
fi

baseline="$(read_baseline)"

# First invocation: bootstrap the baseline silently. No "new release detected"
# on first run — the skill's job is to surface CHANGES, not initial state.
if [ -z "${baseline}" ]; then
  write_baseline "${latest}"
  emit_current_message "${latest}"
  echo "  (baseline bootstrapped on first invocation)"
  exit 0
fi

if [ "${latest}" = "${baseline}" ]; then
  emit_current_message "${latest}"
  exit 0
fi

emit_axis_template "${latest}" "${baseline}"
exit 0
```

ADA's job: type the file faithfully against this skeleton, run `bash -n` to syntax-check, chmod +x at commit time. The skeleton is concrete enough to type from; no novel decisions remain.

### File 5: `substrate/install.sh` — SKILL_NAMES append

**Insertion locus:** line 144 (current) is `  credential-discipline`; line 145 is `)`. Insert `  check-bw-release` between them:

```bash
# BEFORE (lines 141-145):
SKILL_NAMES=(
  agent-author
  check-substrate-updates
  credential-discipline
)

# AFTER:
SKILL_NAMES=(
  agent-author
  check-substrate-updates
  credential-discipline
  check-bw-release
)
```

Single one-line edit. Smoke beat at §5 confirms the dry-run `install.sh` plan picks it up; the `check-substrate-updates/check.sh parse_skill_names_from_install` parser (already shipped, Arc 26) reads this array live, so the new skill is included in MISSING-detection automatically once the array entry lands.

**No other install.sh changes.** A7 forbids cron-scheduling defaults; the skill registers itself for deployment but does not register a scheduling hook.

---

## §4 — Verification probes (for VERA)

Re-derived from directive Phase B (probes 5/6/7/8/9/10) with project-tier POLYBIUS's translation 03:00:04Z applied. Probes 1-4 dropped (B.1+B.2 descoped). Probe 9 narrowed (only the GitHub API parse site needs a cite-comment now).

**Probe 5 — attachments + recap docs present in §16.8:**
```bash
grep -n "## 16\.8\|### 16\.8\|bw attach\|bw recap" \
  /c/Users/denso/claude_projects/the-stoa-arc-28/substrate/MAJOR_POLYBIUS.md
```
PASS condition: §16.8 heading present; "bw attach" and "bw recap" each appear at least once in §16.8 prose; framing language includes "available primitive" or "forward-only" (NOT "migrate" or "required").

**Probe 6 — bw-upgrade-discipline section present at §22:**
```bash
grep -n "^## 22\.\|bw-upgrade discipline" \
  /c/Users/denso/claude_projects/the-stoa-arc-28/substrate/operating-disciplines.md
```
PASS condition: `## 22. bw-upgrade discipline` heading present; 5 numbered steps; 3-axis table; "verify changelog claims empirically before locking adoption decisions" sub-bullet present under Step 2; N=1 anchor subsection present; cross-ref to `ariadne--c71` + `stoa--s6n` present; cross-ref to §6.7.1 present.

**Probe 7 — check-bw-release skill files present and well-shaped:**
```bash
# SKILL.md frontmatter author check
grep -n "^author: Denson Smith$" \
  /c/Users/denso/claude_projects/the-stoa-arc-28/substrate/skills/check-bw-release/SKILL.md

# check.sh executable
ls -la /c/Users/denso/claude_projects/the-stoa-arc-28/substrate/skills/check-bw-release/check.sh

# check.sh syntax
bash -n /c/Users/denso/claude_projects/the-stoa-arc-28/substrate/skills/check-bw-release/check.sh

# Fixture: at-current
BW_RELEASE_CHECK_LATEST_OVERRIDE=v0.13.0 \
BW_RELEASE_CHECK_BASELINE_OVERRIDE=v0.13.0 \
  /c/Users/denso/claude_projects/the-stoa-arc-28/substrate/skills/check-bw-release/check.sh

# Fixture: new-release-detected
BW_RELEASE_CHECK_LATEST_OVERRIDE=v0.99.0 \
BW_RELEASE_CHECK_BASELINE_OVERRIDE=v0.13.0 \
  /c/Users/denso/claude_projects/the-stoa-arc-28/substrate/skills/check-bw-release/check.sh
```
PASS conditions: frontmatter `author: Denson Smith` exact match; check.sh executable bit set; `bash -n` exits 0; at-current fixture prints "Current bw release: v0.13.0 (baseline matches). No action needed."; new-release-detected fixture prints "NEW BW RELEASE DETECTED" + the 3-axis checklist + the §22 cross-ref + the suggested next action.

**Probe 8 — install.sh SKILL_NAMES append:**
```bash
grep -n "check-bw-release" \
  /c/Users/denso/claude_projects/the-stoa-arc-28/substrate/install.sh
```
PASS condition: line appears exactly once inside the `SKILL_NAMES=(...)` block (between `credential-discipline` and `)`), at the indent level of the existing entries.

**Probe 9 (narrowed) — cite-comment at the GitHub API parse site:**
```bash
grep -n "CITE:\|jallum/beadwork/releases/latest\|tag_name" \
  /c/Users/denso/claude_projects/the-stoa-arc-28/substrate/skills/check-bw-release/check.sh
```
PASS condition: `# CITE:` comment present immediately above `fetch_latest_release_tag()`; comment names the endpoint URL + the parsed field (`tag_name`); comment names the failure-mode symptom; comment cross-refs `operating-disciplines.md` §22 Step 2.

**Probe 10 — CURRENT regression on the existing 4 consumer workspaces:**
```bash
/c/Users/denso/claude_projects/the-stoa-arc-28/substrate/skills/check-substrate-updates/check.sh
```
PASS condition: the existing 4 registered workspaces (per `substrate/consumer-workspaces.txt`) report verdicts as they did pre-arc. The-stoa workspace itself will report DRIFTED against this arc's substrate edits — expected; that drift is the arc's own diff. Other workspaces should be unchanged (this arc does not edit check.sh's input enumeration; B.1 was descoped).

### Authorship discipline probe (CATO cold-read item, surfaced here for VERA cross-check)

```bash
# Any new author-claim fields anywhere in the arc?
grep -rn "^author:\|^authors:\|^owner:\|^creator:\|^maintainer:" \
  /c/Users/denso/claude_projects/the-stoa-arc-28/substrate/skills/check-bw-release/
```
PASS condition: exactly one line, `author: Denson Smith` in `SKILL.md` frontmatter. No other author-claim fields anywhere in the new skill directory. The `check.sh` script has no frontmatter (POSIX shell scripts don't); no author claim required.

---

## §5 — Smoke beats for Phase 4

Per directive Phase C + project-tier POLYBIUS's 03:00:04Z trim (drop check-substrate-updates `bash -n` + the `--workspace` smoke beat — those scripts untouched; drop the `DEPRECATED` grep — N/A). PLINY runs these before opening the PR:

1. **Syntax check on the new shell script:**
   ```bash
   bash -n /c/Users/denso/claude_projects/the-stoa-arc-28/substrate/skills/check-bw-release/check.sh
   ```
   Exit 0 expected.

2. **At-current fixture (live bw 0.13.0 on this install):**
   ```bash
   /c/Users/denso/claude_projects/the-stoa-arc-28/substrate/skills/check-bw-release/check.sh
   ```
   Expected output: "Current bw release: v0.13.0 (baseline matches). No action needed." (assumes baseline written to v0.13.0 by first invocation; subsequent runs against unchanged upstream stay "current").

   **First-invocation variant:** if `substrate/.bw-release-last-check` does not yet exist when the smoke beat runs (the file is gitignore-able state, not committed — see §6 weak point on this), the first run bootstraps the baseline with the "(baseline bootstrapped on first invocation)" suffix line. That's expected on the first smoke run; a second back-to-back run produces the plain "current" message.

3. **New-release-detected fixture:**
   ```bash
   BW_RELEASE_CHECK_LATEST_OVERRIDE=v0.99.0 \
   BW_RELEASE_CHECK_BASELINE_OVERRIDE=v0.13.0 \
     /c/Users/denso/claude_projects/the-stoa-arc-28/substrate/skills/check-bw-release/check.sh
   ```
   Expected output: "NEW BW RELEASE DETECTED" block with v0.99.0 / v0.13.0 / release notes URL / 3-axis checklist / suggested next action.

4. **MAJOR_POLYBIUS.md §16.8 grep:**
   ```bash
   grep -n "bw recap\|bw attach\|## 16\.8\|### 16\.8" \
     /c/Users/denso/claude_projects/the-stoa-arc-28/substrate/MAJOR_POLYBIUS.md
   ```
   Expected: multiple hits inside §16.8.

5. **operating-disciplines.md §22 grep:**
   ```bash
   grep -n "^## 22\.\|bw-upgrade discipline\|verify changelog claims empirically" \
     /c/Users/denso/claude_projects/the-stoa-arc-28/substrate/operating-disciplines.md
   ```
   Expected: `## 22. bw-upgrade discipline` heading, `bw-upgrade discipline` phrase, and the verify-changelog-empirically sub-bullet all present.

6. **install.sh SKILL_NAMES append:**
   ```bash
   grep -n "check-bw-release" \
     /c/Users/denso/claude_projects/the-stoa-arc-28/substrate/install.sh
   ```
   Expected: exactly one hit, inside the `SKILL_NAMES=(...)` block.

7. **install.sh --dry-run includes the new skill (per MAJOR_PLINY.md §5.7):**
   ```bash
   mkdir -p /tmp/arc-28-smoke
   /c/Users/denso/claude_projects/the-stoa-arc-28/substrate/install.sh \
     --target project --project-dir /tmp/arc-28-smoke --dry-run 2>&1 \
     | grep -n "check-bw-release"
   ```
   Expected: at least one line showing `check-bw-release` in the planned deploy. The dry-run plan walks `SKILL_NAMES` per install.sh's existing logic; an entry that doesn't appear here means the array append landed in the wrong spot.

---

## §6 — Self-assessed weak points (for ARGUS)

Four places where ARGUS should look hardest. Honest, scoped to what this design rests on.

### 6.1 — `bw recap` documentation includes a registry-conditional caveat that may age badly

The §16.8 `bw recap` subsection includes a caveat naming this install's empty-registry state ("On Windows the registry has been empirically observed to remain empty regardless of registry.auto=true... When the registry is empty, bw recap returns activity for ONLY the current repo (the cwd-detected one)"). This is honest as of 2026-05-17. **Weak point:** if a future bw release (or a Windows-side fix) makes the registry work, this caveat becomes false-but-still-on-disk and may mislead a future POLYBIUS into thinking `--all` doesn't work when it does.

**Why this shape anyway:** silently omitting the caveat now would be worse — a POLYBIUS hitting an empty `bw recap --all` output on this install would have no on-disk explanation. The §22 discipline's own Step 2 ("verify changelog claims empirically") IS the path that updates this caveat: a future bw-upgrade arc that fixes the registry runs the discipline against the new release and produces a substrate-side ticket that revises §16.8's caveat. Naming the substrate-discipline mitigation in the caveat itself ("cross-ref §22 Step 2") makes the future-update path explicit. ARGUS: is this the right phrasing, or should the caveat be looser ("registry behavior on this install" instead of naming "Windows" specifically)?

### 6.2 — `substrate/.bw-release-last-check` state-file path: gitignored or committed?

The design specifies `substrate/.bw-release-last-check` as the state-file path (substrate-level, mirroring `check-substrate-updates`'s state file). **Weak point:** the design does NOT decide whether the file should be `.gitignore`d or committed. Two failure modes:

- If committed: every check-bw-release run on any machine dirties the working tree with a one-line file edit when upstream advances. That noise mixes with substrate edits and may get caught up in unrelated commits.
- If gitignored: every fresh clone (and every substrate worktree) bootstraps from upstream-latest on first run, which is the friendly default — BUT a CI smoke beat that runs the skill twice in sequence (first run bootstraps; second run reports "current") may behave differently than a smoke beat that runs it once.

**Why this shape anyway:** the design defers to ADA's call at build time — `check-substrate-updates/.substrate-last-check` is in `.gitignore` per the existing precedent (verifiable at build time); following that precedent is the path of least surprise. ADA's discretion to gitignore or commit, with the gitignore default. ARGUS: should this be locked at design time rather than deferred? If locked, which way?

### 6.3 — C.1 N=1 framing borrows §16.6's shape; risk of over-fitting the analogy

§22.3's N=1-provenance-plus-accretion-path subsection is structurally a near-copy of `MAJOR_POLYBIUS.md` §16.6 (Arc 27). **Weak point:** Arc 27's §16.6 was anchoring a discipline PRINCIPAL declared based on lived POLYBIUS-lifecycle experience; this arc's §22.3 anchors a discipline PRINCIPAL declared in response to a single bw release. The substrate-canon-off-gate framing IS the same; the empirical foundation differs in shape. Reading §22.3 as "PRINCIPAL declarations enter substrate canon on a routine basis" overgeneralizes both this case and §16.6.

**Why this shape anyway:** the §6.7.1 canon-promotion gate is the gate that disciplines this. The honest framing names the off-gate entry explicitly + the future-evidence-accretion requirement — which is what the §22.3 prose does. ARGUS should read §22.3 specifically for whether the prose stays tight on the "single release; future releases accrete evidence; if axes wrong-shaped future arcs revise" framing, OR whether it leaks toward "discipline established" framing that overstates confidence. Catch: the design's own §1 problem statement uses "encode a bw-upgrade discipline" — that phrasing may set up the over-fit risk by treating the discipline as more settled than the N=1 anchor warrants.

### 6.4 — The check-bw-release skill is structurally a clone of check-substrate-updates; shared-shape carries shared-defect risk

C.2's design is intentionally clone-shaped against `check-substrate-updates` for operator-muscle-memory reasons (state file convention, `--help` sed extraction, `set -euo pipefail` + while-case argument parsing, env-var fixture override). **Weak point:** any structural defect in the clone-source carries forward. The Arc 26 grep-v-empty-pipeline-exit defect (per `check-substrate-updates/check.sh:494-503` comment) is the kind of defect that would survive copy-and-modify; if this design's skeleton missed a defang that the cloned source had, ADA might re-introduce it without noticing because the skeleton "looks right."

**Why this shape anyway:** the design's skeleton at §3 File 4 is concrete enough that ADA does not re-derive shape; the cite-comment pattern + the fixture mechanism + the `--help` extraction are all explicit. The clone shape IS the lower-risk path; the alternative (novel argument-parsing convention, novel state-file shape, novel `--help` extraction) would compound defect surfaces, not reduce them. ARGUS should specifically read the §3 File 4 skeleton against `check-substrate-updates/check.sh` for any defect-pattern the clone might inherit silently (the grep-v defang at line 500; the empty-array guarded iteration under `set -u` at line 685; the `wc -l | tr -d ' '` BSD/GNU portability idiom). If any of those patterns is implicitly required by the skeleton but not explicitly named, the skeleton has a gap.

---

## §7 — Out of scope (the A7 hard-lock, restated for ADA)

This design deliberately does NOT cover, and ADA must NOT add during build:

- Removing `consumer-workspaces.txt` (the B.1 descope removed the deprecation header too; file stays untouched).
- Adopting bw 0.13.0 features beyond B.3 + B.4. The registry + cross-repo prefix resolution stay un-adopted at the substrate level pending a future arc with empirical evidence.
- Migrating existing on-disk handoff/retro/design artifacts to bw attachments. Forward-only.
- check-bw-release cron-scheduling defaults. Skill ships; operator decides whether to cron.
- Cross-workspace propagation of `check-bw-release`. `install.sh` deploys to consumer workspaces on next `--target project --project-dir <ws>` run; this arc does not propagate proactively.
- Editing prior arcs' retros or directives to fit new conventions.
- Sibling `stoa--32b.1` / `stoa--32b.2` (separate forthcoming arcs).
- Any author-claim field that names anyone other than Denson Smith (A6 IMMUTABLE per `substrate/CLAUDE.md`).

If ADA finds any of the above tempting mid-build, STOP and surface to PLINY before proceeding.

---

End design.
