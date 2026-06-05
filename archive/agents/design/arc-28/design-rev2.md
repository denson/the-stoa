# Arc 28 design REV2 — bw 0.13.0 substrate adoption (B.3 + B.4) + bw-upgrade discipline (C.1 + C.2)

**Ticket:** `stoa--s6n`
**Branch:** `arc-28/build`
**Worktree:** `C:\Users\denso\claude_projects\the-stoa-arc-28`
**Directive:** `substrate/arcs/arc-28-build-directive.md` (A1-A8) + `bw show stoa--s6n` 2026-05-17T02:59:14Z user-tier POLYBIUS adjudication + 2026-05-17T03:00:04Z project-tier POLYBIUS translated scope (the two comments override the directive's A2 B.1 / A2 B.2 / A4 wording per forward-only-no-retro-edit convention).
**Authored by:** CAPTAIN_DAEDALUS_the_stoa, on behalf of the PRINCIPAL (Denson Smith).
**Supersedes:** `design.md` (rev1) per the ARGUS verdict at `stoa--s6n` 2026-05-17T03:07:43Z. Rev1 stays on disk as history per substrate convention.

---

## Rev2 changelog — what was revised + why

The ARGUS cold-audit of rev1 (verdict timestamped 2026-05-17T03:07:43Z) returned REVISE with 3 load-bearing risks + 5 advisories. Rev2 is rev1 with surgical revisions to the affected sections; the sections ARGUS ratified stay verbatim.

**Load-bearing revisions (each blocks PASS):**

- **LBR-1 — `curl | python3` pipeline failure-mode contract under `set -euo pipefail`** (resolved at §2.2 + §3 File 4). Picked: explicit defang at the pipeline boundary (`{ ... ; } || true`) — matches the discipline shape of `check-substrate-updates/check.sh:489-500`. The `fetch_latest_release_tag` skeleton now shows the defang explicitly; the FAILURE-MODE cite-comment is re-written to describe what the runtime actually does.
- **LBR-2 — §16.8 `bw recap` caveat misframes default behavior** (resolved at §3 File 1). The caveat now distinguishes documented default (single-repo, works as designed) from `--all` variant (registry-conditional; empty on this install). Phrasing loosened from "Windows" to "this install" per ARGUS residual response.
- **LBR-3 — substrate-only-skill vs per-workspace-skill semantics not picked** (resolved at §2.2 + §3 File 3 + §3 File 4 + §6.1). Picked: **per-workspace deployment semantics**. State file lives at `<workspace>/.claude/.bw-release-last-check` (mirroring the canonical `check-substrate-updates/.substrate-last-check` per-workspace pattern). SKILL.md prose, check.sh SUBSTRATE_DIR computation, and the gitignore answer all align with this pick.

**Advisory revisions (folded for free):**

- **ADV-1 — bw recap flag listing omits `--ascii`** (folded at §3 File 1). Listing now includes `--ascii` (verified via `bw recap --help`).
- **ADV-2 — §6.2 false `.gitignore` precedent claim** (folded at §6.1's rewrite). Rationale re-derived against the actual mechanism: runtime grep filter at `check-substrate-updates/check.sh:489-500`, not a `.gitignore` line.
- **ADV-3 — Probe 9 grep test underspecified vs prose PASS condition** (folded at §4 Probe 9). Grep widened to match the prose claims (failure-mode + §22 cross-ref + endpoint URL + parsed-field name).
- **ADV-4 — "stoa--uly convention" framing overstated** (folded at §3 File 3 frontmatter discussion). Re-framed as "current single-precedent forward adoption (credential-discipline; agent-author and check-substrate-updates SKILL.md predate the convention)." Still adopt for the new SKILL.md (correct); breadth framed honestly.
- **ADV-5 — §2.1 line-number prose accuracy** (folded at §2.1). Line 922 is the end of §16.7 cross-refs; line 926 is the §16 section closer. Prose adjusted to name the correct boundary.

**Ratified sections (unchanged from rev1, by ARGUS verdict):**

- §1 — problem statement (in-scope list matches POLYBIUS translation; descope framing accurate).
- §2.1 — placement decisions (with the ADV-5 line-number fix in this section's prose only).
- §22.3 — N=1 framing inside §3 File 2 (no leak toward overstatement).
- §3 File 2 — operating-disciplines.md §22 structure.
- §3 File 5 — install.sh SKILL_NAMES append.
- §5 — smoke beats (with one beat updated to reflect the per-workspace state-file path picked under LBR-3, and one beat added to cover the explicit defang under LBR-1).
- §6 weak point preserved from rev1 §6.3 — N=1 framing risk.
- §7 — out-of-scope restatement.

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
- The C.2 skill is shaped as a near-clone of `check-substrate-updates` in directory layout, state-file convention, cite-comment policy, and `--help` extraction style — operator muscle memory carries across the two skills. Per LBR-3 resolution, the per-workspace deployment semantics of `check-substrate-updates` are mirrored explicitly (state file at `<workspace>/.claude/.bw-release-last-check`, computed relative to the deployed script's location).

---

## §2 — Architectural decisions

### 2.1 Section-placement decisions

**B.3 + B.4 placement: `MAJOR_POLYBIUS.md` §16.8 (single combined subsection), not split across §16 + §7.**

The directive (A2 B.4) explicitly allowed "and/or §7" for `bw recap`. The B.4 worked example named by the directive — "POLYBIUS picking up after compaction can run `bw recap` to see what's happened since its last read-point" — is a §16 lifecycle event, not a §7 communications-pattern event. `bw attach` (B.3) is unambiguously §16.3 multi-artifact-handoff adjacent. Splitting them would force a reader cross-walking the lifecycle to hop between §7 and §16; combining them at §16.8 keeps the lifecycle-relevant primitives co-located after the existing §16.7 Cross-references.

§16.7 Cross-references ends at line 922 in the on-disk file; line 926 is the §16 section closer (`Standby, run.` plus the surrounding `---` separator). §16.8 inserts AFTER the existing §16.7 cross-refs (after line 922) and BEFORE the §16 closer (line 926). The §16.7 Cross-references subsection itself gains one new bullet pointing at the new §16.8. The §16 closer (`Standby, run.`) is preserved verbatim at file tail.

**C.1 placement: `operating-disciplines.md` §22 (append after §21 Ariadne-search-ready authoring).**

The current operating-disciplines.md terminates at §21 (line 946-967) followed by an `Agent-regime inverses (positive framing)` block + `Empirical lineage` block at file tail (lines 968-991). C.1 inserts as `## 22. bw-upgrade discipline` AFTER §21 and BEFORE the `Agent-regime inverses` block — the file structure of "numbered disciplines, then the inverses block, then the lineage block" stays intact.

The path-of-least-disruption alternative would have been to nestle the discipline under §12 `bw cookbook` as `§12.N`. Rejected: §12 is operational cookbook (commands + worked examples); §22 is a process discipline (the 5-step Trigger→Review→File→Dispatch→Verify shape). Different shape, different reader expectation. §12 gets a forward-pointer added to §22 as a cross-ref (§22 cites §12 for cookbook commands; §12 stays unchanged in this arc per A7's "edit no more than necessary" implicit corollary).

### 2.2 C.2 skill design (concrete picks)

**Deployment semantics: per-workspace (resolves LBR-3).**

The choice was between:

- **Substrate-only:** operator runs `check-bw-release` only at the the-stoa workspace; consumer-workspace copies deployed by `install.sh` are dead weight. State file `substrate/.bw-release-last-check` is the canonical single baseline; consumer-tier copies share that baseline only by re-install or are simply never run.
- **Per-workspace:** consumer copies are first-class; each workspace has its own `<workspace>/.claude/.bw-release-last-check`; SKILL.md prose reads the path relative to the deployed location; baseline drifts independently per workspace.

**Pick: per-workspace.** Three reasons:

1. **Stoa-canonical pattern is per-workspace.** `check-substrate-updates` is per-workspace by design — its state file `<workspace>/.claude/.substrate-last-check` lives at the consumer workspace, one per workspace (verified at `check-substrate-updates/SKILL.md` line 143). The new skill is built as a structural clone of `check-substrate-updates` (per §1 imported assumption #5); cloning the deployment semantics too is the path of least surprise. Operator muscle memory carries across the two skills.
2. **`install.sh` cp -R deploys to consumer workspaces unconditionally** (verified at `install.sh:701-715`). The skill subtree lands at `<workspace>/.claude/skills/check-bw-release/`. Substrate-only semantics would leave dead-weight scripts at every consumer workspace — discoverable, invokable, and confusing if a consumer-tier POLYBIUS ran the deployed copy expecting it to be live. Per-workspace makes the deployed copies first-class with no extra deploy plumbing.
3. **Substrate-only argument ("no meaningful per-workspace differentiation for a single upstream feed") is true today but rotates.** A consumer workspace that has not yet performed a substrate upgrade has a legitimate independent question: "did upstream advance since my last upgrade?" — separable from the-stoa's own baseline. Per-workspace baselines preserve that distinction without coordinating cost.

**Implications fanned out across the design:**

- `SCRIPT_DIR/SUBSTRATE_DIR` walk in `check.sh` computes the state-file path RELATIVE to the script's deployed location. At substrate-tier (this repo), `SCRIPT_DIR=substrate/skills/check-bw-release/`, the walk lands at `substrate/`, and STATE_FILE resolves to `substrate/.bw-release-last-check`. At consumer-tier, `SCRIPT_DIR=<workspace>/.claude/skills/check-bw-release/`, the walk lands at `<workspace>/.claude/`, and STATE_FILE resolves to `<workspace>/.claude/.bw-release-last-check`. The script does not hardcode "substrate" or any other tier-specific path; the deployed location is the source of truth.
- SKILL.md prose names the state-file path RELATIVELY: "the script writes a baseline tag to `.bw-release-last-check` in the directory two levels above the script (i.e., the skills-parent directory — `substrate/` at substrate-tier, `<workspace>/.claude/` at consumer-tier)." No tier-specific hardcoded path in prose.
- The gitignore answer (per §6.1, formerly rev1's §6.2): the state file is filtered at RUNTIME by the same `grep -v` mechanism `check-substrate-updates` uses (verified at `check-substrate-updates/check.sh:489-500`). This is NOT a `.gitignore` answer; rev1's "existing precedent in .gitignore" framing was wrong (per ADV-2). The actual mechanism is runtime filter when other skills (e.g., `check-substrate-updates`) compute uncommitted-changes counts. The state file itself MAY be committed or untracked per consumer-workspace discretion; the substrate's own copy at `substrate/.bw-release-last-check` follows the same convention `substrate/.substrate-last-check` follows (untracked because runtime grep filters it; no `.gitignore` line needed; if it accidentally gets staged it does no harm because it's just a tag).

**LBR-1 resolution: explicit defang at the pipeline boundary in `fetch_latest_release_tag`.**

Picked over the restructured-discipline alternative (separate-capture `output=$(curl ...); rc=$?; ...`). Two reasons:

1. **Match Stoa-canonical pattern.** `check-substrate-updates/check.sh:489-500` already uses the `{ ... ; } || true` defang for the analogous bug class (grep-empty pipeline exit under pipefail). The cite-comment there names the bug class explicitly. The new skill's defang follows the same shape and cites the same precedent — operator reading either script sees the same pattern.
2. **Less code, fewer moving parts.** Explicit-defang adds one line (the `{ ... ; } || true` wrapper); separate-capture changes the call shape (no more pipeline, two assignments, explicit `$?` capture, conditional empty-string set). The defang is the smaller surface to maintain and the closer match to the script-author's mental model of "the pipeline either yields the tag or yields empty; treat empty as could-not-check."

The §3 File 4 skeleton shows the defang explicitly; the FAILURE-MODE cite-comment is re-written to describe what the runtime actually does (the defang catches both curl-non-zero and python-empty-output; the caller-side `[ -z "${latest}" ]` guard fires on the defanged empty string).

**State file format:** plain text, single line, just the tag (e.g., `v0.13.0\n`). Picked over the key=value form `check-substrate-updates` uses because there is exactly ONE piece of state worth persisting (the last-seen tag); a timestamp adds nothing actionable (the file's `mtime` is the timestamp). Simpler is better; the parse code is one `cat | tr -d '\n'`. State-file path: as resolved above by SCRIPT_DIR walk.

**GitHub API endpoint:** `https://api.github.com/repos/jallum/beadwork/releases/latest`. Picked over the `gh release view --latest -R jallum/beadwork` form because `gh` is not a guaranteed dependency on consumer workspaces, while `curl` is a universal substrate-script tool already in use (cf. ariadne's Dockerfile pattern). The API returns JSON; the field to parse is `tag_name` (cite-comment at the parse site per A5). No authentication required for public-repo release reads; rate limit is 60/hour unauthenticated which is far above any plausible check cadence. The endpoint is documented at https://docs.github.com/rest/releases/releases#get-the-latest-release; the cite-comment surfaces the linkage at the read site, same mitigation pattern as `apply_substitutions`.

**Argument parsing:** mirror `check-substrate-updates/check.sh` shape — `set -euo pipefail`, while-case loop over `$@`, support `-h|--help` (extract the head-of-file comment via `sed -n /^# check\.sh/,/^# .*not failure\.$/p $0 | sed 's/^# \{0,1\}//'`). Two flags beyond `--help`:

- `--force-check` — bypass any rate-limiting/cache logic. The skill ships with no rate-limiter (state file is just a tag, not a timestamp), so `--force-check` is a no-op flag reserved for forward-compat if a future arc adds caching. Document it; the spec keeps the flag's surface stable across that future.
- `--baseline <tag>` — override the state file's stored tag for this invocation (testing-side use; lets fixtures inject a stale baseline without writing the state file).

No `--workspace` argument. The skill is single-target by nature (it checks one upstream releases feed, not per-workspace anything from the standpoint of WHAT it checks — the per-workspace dimension is WHERE the baseline lives, not what the check produces). Document explicitly.

**Test fixture mechanism:** environment variable override, **two** vars (one for upstream-latest mocking, one for baseline mocking):

- `BW_RELEASE_CHECK_LATEST_OVERRIDE=<tag>` — when set, skip the API call and use this as the upstream-latest tag. Picked over file-based mock because env-var override is grep-able, stateless (no file to clean up between tests), and idiomatic for shell-script fixtures (Arc 25 credential-discipline uses the same shape per its SKILL.md).
- `BW_RELEASE_CHECK_BASELINE_OVERRIDE=<tag>` — when set, skip reading the state file and use this as the baseline. Test-only; production callers never set it.

Both vars are scoped to a single invocation. Document the mechanism inline in `check.sh` at the env-var read site (cite-comment shape per A5) AND in `SKILL.md` "How to test" section with three worked invocations: (a) at-current (both vars set to v0.13.0 → "current"); (b) new-release-detected (LATEST_OVERRIDE=v0.99.0 + BASELINE_OVERRIDE=v0.13.0 → "new release detected" + axis template); (c) live (no overrides, no `--baseline`, against bw 0.13.0 → expect "current" today).

### 2.3 Cite-comment policy applied to C.2 parse site

A5 narrowed to one surface in this arc: the GitHub releases API JSON parse in `check.sh`. The cite-comment lives at the parse site (not at the top of the file) and names: the endpoint, the field parsed (`tag_name`), the failure-mode actual runtime behavior (not the rev1 wishful-thinking claim), and the §22 cross-ref — same model as `check-substrate-updates/check.sh:135-156` `parse_skill_names_from_install`. Shape spec:

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
  # FAILURE-MODE (actual runtime, post LBR-1 fix per ARGUS verdict
  # 2026-05-17T03:07:43Z): under `set -euo pipefail`, an unguarded
  # `curl | python3` pipeline that fails (curl non-200 OR python parse error)
  # would propagate via pipefail and kill the calling command substitution via
  # `set -e`. The `{ ... ; } || true` defang at the pipeline boundary catches
  # both curl-non-zero and python-non-zero exits; the function then echoes
  # whatever python wrote to stdout (empty string on parse error). The caller's
  # `[ -z "${latest}" ]` guard fires on the defanged empty result and emits the
  # "could not reach upstream" message. Same defang shape as
  # check-substrate-updates/check.sh:489-500 (grep-v empty-pipeline-exit). This
  # is informational tooling, not blocking — drift is not failure.
  ...
}
```

The parse uses Python (`python3 -c "import json,sys; print(json.load(sys.stdin)['tag_name'])"`) rather than `jq`. Python is the substrate's established cross-platform dependency (see `operating-disciplines.md` §13 PYTHONUTF8=1 discipline); `jq` is not. Cite-comment names this trade-off at the parse site so a future maintainer doesn't "improve" it to `jq` without registering the dependency surface.

---

## §3 — File-by-file deliverable plan

### File 1: `substrate/MAJOR_POLYBIUS.md` — add §16.8

**Insertion locus:** after the §16.7 Cross-references list (current line 922) and before the §16 closer block (current line 926). New subsection slots in cleanly before the file's section terminator; the existing `Standby, run.` closer is preserved at the end of §16.

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

  bw recap [WINDOW] [--since DATE] [--all] [--verbose] [--json] [--ascii] [--dry-run]

Summarizes beadwork activity. Default: single-repo (the cwd-detected
repo). With --all: across every registered repo. First-time runs show the
last 24 hours; subsequent runs show activity since the last recap
(cursor-driven). WINDOW tokens accepted: today, yesterday, week,
durations like 15m / 1h / 3h30m / 24h / 2d / 7d / 2w. --since takes
RFC3339 or YYYY-MM-DD. --dry-run shows activity without advancing the
cursor. --ascii uses plain ASCII tree characters (effective with
--verbose).

Use case (forward-only): POLYBIUS picking up after /compact (or a fresh
Mode 1 session-continue per §16.2) can run bw recap to see what has
landed in the current repo since the previous read-point. Pairs with the
handoff doc as a complementary signal: handoff says "what is the current
intent"; recap says "what has happened lately."

Caveat (`--all` only; this install, 2026-05-17): plain `bw recap` (no
`--all`) works as documented — single-repo, cursor-driven, no
dependencies on the registry. The `--all` variant requires the bw
registry to be populated. On this install the registry has been
empirically observed to remain empty regardless of `registry.auto=true`
(per stoa--s6n 2026-05-17T02:00:03Z probe trail; cross-ref §22 Step 2);
`--all` therefore returns no cross-repo activity here. For multi-repo
recap on this install, invoke once per repo via cd-and-recap rather than
relying on `--all`. When/if the registry behavior changes on this
install (or this caveat is found wrong on a different install), the §22
discipline's Step 2 "verify changelog claims empirically" path updates
this caveat — see operating-disciplines.md §22 Step 2.

#### Cross-references

- §16.3 (handoff is multi-artifact, not single-doc) — the conceptual
  parent for bw attach's use case.
- §16.2 Mode 1 (handoff + compaction) — the lifecycle event bw recap
  serves.
- operating-disciplines.md §22 (bw-upgrade discipline) — the broader
  framing under which these primitives were adopted from bw 0.13.0.
- operating-disciplines.md §12 (bw cookbook) — for full bw command
  syntax and per-command flag reference.
```

ADA verbatim-copies the `bw attach` and `bw recap` flag listings from `bw <cmd> --help` to keep them faithful to the installed CLI. The flag listing above already includes `--ascii` per ADV-1; ADA should still verify against `bw recap --help` at build time to catch any flags added or removed by a between-now-and-build minor release. The §16.7 Cross-references subsection gains one new bullet at its end:

```
- **§16.8 (bw 0.13.0 available primitives).** The two forward-only primitives — bw attach and bw recap — adopted from bw 0.13.0 per Arc 28 (stoa--s6n).
```

The §16 section closer (`Standby, run.` plus the surrounding `---` separator at line 926) is preserved verbatim at file tail.

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
the current latest tag, compares to a per-workspace baseline stored at
`.bw-release-last-check` (two levels above the script — `substrate/` at
substrate-tier, `<workspace>/.claude/` at consumer-tier), and surfaces
a "new release detected" message with the 3-axis classification template
(per §22.2) and a suggested next action ("file tickets per impact axis")
when the tags differ. When tags match, prints a short "current" message.

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

**New file. Frontmatter:**

```yaml
---
name: check-bw-release
description: Check for new bw upstream releases and surface the 3-axis impact-classification template when one is found. Queries the bw GitHub releases API for the current latest tag, compares to a per-workspace baseline stored at .bw-release-last-check (in the skills-parent directory — substrate/ at substrate-tier, <workspace>/.claude/ at consumer-tier), and prints either a "current" message or a "new release detected" message with changelog pointer + axis template + suggested next action (per operating-disciplines.md §22 bw-upgrade discipline). Single-target skill (checks one upstream feed); per-workspace baselines (mirrors check-substrate-updates' per-workspace state-file pattern). Operator decides whether to cron it; no scheduling defaults. Triggers on requests like "is there a new bw release", "check bw for updates", "bw release check", "new bw version", "did bw upgrade".
author: Denson Smith
---
```

**On the `author:` field framing (per ADV-4):** the `author: Denson Smith` line is forward-adoption of a current single-precedent convention. Today's existing skills carry it inconsistently: `credential-discipline/SKILL.md` (the Arc 25 worked example) carries it; `agent-author/SKILL.md` and `check-substrate-updates/SKILL.md` do NOT (both predate the convention). The substrate-canon authorship rule is `substrate/CLAUDE.md` (IMMUTABLE: every author-claim field anywhere in the substrate names Denson Smith); the SKILL.md frontmatter `author:` field is one specific surface of that rule, and forward-adoption here is correct. Rev1 framed this as "the stoa--uly convention" which overstated current breadth (1-of-3 existing skills, not a settled pattern); rev2 frames it accurately as forward-adoption of a single precedent under the substrate-canon rule that motivates it. ADA: ship the `author: Denson Smith` line on this SKILL.md; do not retro-add it to the two existing skills that lack it (out of scope for this arc per A7).

**Sections (the prose ADA writes; this design names the shape + load-bearing content):**

1. **Why this skill exists.** One paragraph. The discipline at `operating-disciplines.md` §22 names a 5-step process; Step 1 (Trigger) is the only step that's mechanical. Without a skill, the operator has to remember to check the releases page periodically; with the skill, the check is one command + the output cues the operator into Steps 2-5. Cross-ref §22 directly.
2. **When to use this skill.** Bullet list. Invoke when: PRINCIPAL asks "is there a new bw release"; operator wants a periodic check; before kicking off a new substrate-adoption arc (sanity-check that the baseline tag is still current). Do **not** invoke for: classifying features into axes (that's §22 Step 2, POLYBIUS judgment); filing tickets (that's §22 Step 3, POLYBIUS judgment); auto-applying upgrades (out of scope; if/when an arc warrants auto-apply, that's a future skill's job).
3. **What the skill ships.** Three things: `SKILL.md`, `check.sh`, and a per-workspace state file written at first invocation. State-file location: the skill writes `.bw-release-last-check` in the directory TWO LEVELS ABOVE the script (i.e., the skills-parent directory). At substrate-tier (this repo), that's `substrate/.bw-release-last-check`. At consumer-tier (after `install.sh` deploys the skill subtree), that's `<workspace>/.claude/.bw-release-last-check`. Per-workspace baselines mirror the `check-substrate-updates` pattern (state file at `<workspace>/.claude/.substrate-last-check`); each workspace's baseline drifts independently as that workspace's operator runs the skill. No `.gitignore` line is needed — the state file is filtered at RUNTIME by the same `grep -v` mechanism `check-substrate-updates/check.sh:489-500` uses for its own state file (so it doesn't show up in uncommitted-changes counts that other skills compute). Operators MAY commit the file (no harm; it's just a tag), but the default mode is untracked-and-runtime-filtered.
4. **How to invoke.** Three worked invocations:
   - `<skill-dir>/check.sh` — the standard call. At substrate-tier: `substrate/skills/check-bw-release/check.sh`. At consumer-tier: `<workspace>/.claude/skills/check-bw-release/check.sh`.
   - `<skill-dir>/check.sh --force-check` — no-op today; reserved for forward-compat if a future arc adds caching.
   - `<skill-dir>/check.sh --baseline v0.12.3` — override baseline for testing or recovery (if the state file is lost / corrupted).
5. **What the output is telling you.** Two cases:
   - **CURRENT:** "Current bw release: v0.13.0 (baseline matches). No action needed." Skill exits 0.
   - **NEW RELEASE DETECTED:** Multi-line output naming the new tag, the prior baseline, a pointer to the GitHub release notes URL, the 3-axis classification template (verbatim copy of §22.2 axes as a checklist), and a suggested next action ("File one ticket per impact axis touched per operating-disciplines.md §22 Step 3."). Skill exits 0. The "informational tooling, never blocks" exit-code discipline matches `check-substrate-updates`.
6. **How to test.** Three worked invocations against the env-var fixture mechanism (per §2.2):
   - **At-current:** `BW_RELEASE_CHECK_LATEST_OVERRIDE=v0.13.0 BW_RELEASE_CHECK_BASELINE_OVERRIDE=v0.13.0 check.sh` → "current".
   - **New-release-detected:** `BW_RELEASE_CHECK_LATEST_OVERRIDE=v0.99.0 BW_RELEASE_CHECK_BASELINE_OVERRIDE=v0.13.0 check.sh` → "new release detected" + axis template.
   - **Live:** `check.sh` (no overrides, no `--baseline`) → expects "current" today against bw 0.13.0.
7. **State file shape.** One line, the tag. First invocation writes baseline = upstream-latest (no "new release detected" on first run; the skill bootstraps to current). Document explicitly: there is no `--init` flag; first invocation IS the init.
8. **Per-workspace deployment + baseline independence.** This skill follows the per-workspace deployment pattern of `check-substrate-updates`: `install.sh` deploys the skill subtree to `<workspace>/.claude/skills/check-bw-release/`, and each workspace runs the skill against its own baseline. There is no cross-workspace coordination; an upstream advance is detected independently at each workspace the first time that workspace runs the skill after the advance. The substrate-tier copy at `the-stoa/substrate/skills/check-bw-release/` runs against `substrate/.bw-release-last-check`; consumer copies run against `<workspace>/.claude/.bw-release-last-check`. Operators picking which workspace's baseline to advance is a workspace-local decision.
9. **Cron cadence.** Out of scope per A7. Operator picks; the polling-cron-prompt template at `substrate/templates/polling-cron-prompt-template.md` is adaptable if the operator decides to cron-schedule.
10. **What this skill is NOT.**
    - Not an upgrader. Step 1 only.
    - Not a classifier. Axis classification is POLYBIUS judgment.
    - Not a multi-source release tracker. bw only; if/when other upstreams need similar tracking, file a follow-up.
    - Not authenticated. No GitHub token required; rate limit is 60/hour unauthenticated, which is far above any plausible check cadence.
    - Not a cross-workspace coordinator. Each workspace's baseline drifts independently; if operator wants a single canonical baseline, run the skill only at the substrate-tier copy and ignore consumer-tier copies (the per-workspace pick is "first-class everywhere", not "canonical at one place").
11. **Related.**
    - `operating-disciplines.md` §22 — the discipline this skill operationalizes Step 1 of.
    - `MAJOR_POLYBIUS.md` §16.8 — the substrate-side adoption shape produced by the 0.12.3 → 0.13.0 run-through.
    - `substrate/skills/check-substrate-updates/` — sibling structural model, INCLUDING the per-workspace state-file pattern this skill mirrors.
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
# to a per-workspace baseline stored at .bw-release-last-check (in the
# directory two levels above this script — substrate/ at substrate-tier,
# <workspace>/.claude/ at consumer-tier), and prints either a "current"
# message or a "new release detected" message with changelog pointer +
# axis template + suggested next action (per operating-disciplines.md
# §22 bw-upgrade discipline). Single-target skill (one upstream feed);
# per-workspace baselines (mirrors check-substrate-updates' per-workspace
# state-file pattern). First invocation bootstraps the baseline (no "new
# release detected" on first run); subsequent invocations compare
# upstream-latest to the stored baseline.
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

# ----- locate the skills-parent directory (state-file lives there) -----
#
# The skill is deployed BY install.sh to <workspace>/.claude/skills/check-bw-release/.
# At substrate-tier (the-stoa repo), the script lives at
# substrate/skills/check-bw-release/. In both cases, the skills-parent
# directory (the directory two levels above this script) is the right
# place for the state file:
#   - substrate-tier:  substrate/.bw-release-last-check
#   - consumer-tier:   <workspace>/.claude/.bw-release-last-check
# Per-workspace baselines mirror check-substrate-updates' per-workspace
# state-file pattern; each workspace's baseline drifts independently.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_PARENT_DIR="$(cd "${SCRIPT_DIR}/../.." && pwd)"
STATE_FILE="${SKILLS_PARENT_DIR}/.bw-release-last-check"

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

# fetch_latest_release_tag: echo the latest release tag, or empty string on
# failure (network, parse error, or upstream contract change).
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
# FAILURE-MODE (actual runtime, defang per ARGUS rev1 verdict
# 2026-05-17T03:07:43Z LBR-1): under `set -euo pipefail`, an unguarded
# `curl | python3` pipeline that fails (curl non-200, network unreachable,
# python parse error on unexpected JSON shape, etc.) would propagate via
# pipefail and kill the calling command substitution via `set -e`. The
# `{ ... ; } || true` wrapper at the pipeline boundary catches both
# curl-non-zero and python-non-zero exits; the function then echoes
# whatever python wrote to stdout (empty string on parse error, since
# python's `pass` swallows the exception in the inline script). The
# caller's `[ -z "${latest}" ]` guard fires on the defanged empty result
# and emits the "could not reach upstream" message. Same defang shape as
# check-substrate-updates/check.sh:489-500 (which defangs grep-empty
# pipeline exit under pipefail). This is informational tooling, not
# blocking — drift is not failure.
fetch_latest_release_tag() {
  if [ -n "${BW_RELEASE_CHECK_LATEST_OVERRIDE:-}" ]; then
    echo "${BW_RELEASE_CHECK_LATEST_OVERRIDE}"
    return 0
  fi
  # Defang at the pipeline boundary: catches curl-non-zero AND python-
  # non-zero; downstream sees the python stdout (empty on parse error).
  { curl -fsSL "https://api.github.com/repos/jallum/beadwork/releases/latest" 2>/dev/null \
      | python3 -c "import json,sys;
try:
  print(json.load(sys.stdin).get('tag_name',''))
except Exception:
  pass" 2>/dev/null
  } || true
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

ADA's job: type the file faithfully against this skeleton, run `bash -n` to syntax-check, chmod +x at commit time. The skeleton is concrete enough to type from; no novel decisions remain. The LBR-1 defang is explicit at the pipeline boundary; the cite-comment names what the runtime actually does, not what rev1 wishfully claimed.

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

**No other install.sh changes.** A7 forbids cron-scheduling defaults; the skill registers itself for deployment but does not register a scheduling hook. Per LBR-3 resolution (per-workspace deployment semantics), the existing `cp -R` deploy at `install.sh:701-715` lands the skill subtree at `<workspace>/.claude/skills/check-bw-release/` and the script's SCRIPT_DIR-relative state-file resolution does the right thing without any further install.sh logic.

---

## §4 — Verification probes (for VERA)

Re-derived from directive Phase B (probes 5/6/7/8/9/10) with project-tier POLYBIUS's translation 03:00:04Z applied + ARGUS rev1 verdict ADV-3 (Probe 9 grep alignment) applied. Probes 1-4 dropped (B.1+B.2 descoped). Probe 9 widened to grep what the prose PASS condition actually claims.

**Probe 5 — attachments + recap docs present in §16.8:**
```bash
grep -n "## 16\.8\|### 16\.8\|bw attach\|bw recap" \
  /c/Users/denso/claude_projects/the-stoa-arc-28/substrate/MAJOR_POLYBIUS.md
```
PASS condition: §16.8 heading present; "bw attach" and "bw recap" each appear at least once in §16.8 prose; framing language includes "available primitive" or "forward-only" (NOT "migrate" or "required"); the recap caveat names "--all" specifically (NOT a generic "registry empty → recap broken" claim — per LBR-2, plain `bw recap` works as documented, only `--all` is registry-conditional).

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

**Probe 7b (added in rev2 per LBR-1) — LBR-1 defang behavior under simulated upstream failure:**
```bash
# Force a curl failure by pointing at an unresolvable host via /etc/hosts-style
# override (or just-temporarily breaking network), and confirm the script
# does NOT die mid-pipeline. The defang at the pipeline boundary should
# emit the "could not reach upstream" message and exit 0.
#
# Simplest probe shape (no /etc/hosts mucking): temporarily rename curl on
# PATH or invoke with PATH=/nonexistent so the curl call fails with command-
# not-found. Under set -euo pipefail, an unguarded pipeline would die; the
# defanged pipeline produces empty output, the [ -z "${latest}" ] guard
# fires, and emit_unreachable_message runs.
PATH=/nonexistent \
  /c/Users/denso/claude_projects/the-stoa-arc-28/substrate/skills/check-bw-release/check.sh
echo "exit_code=$?"
```
PASS condition: script does NOT exit non-zero; output contains "could not reach https://api.github.com/repos/jallum/beadwork/releases/latest"; `exit_code=0`. If the script dies with `set -e` propagation (exit code non-zero, no "could not reach" message), the LBR-1 defang regressed — fail the probe and surface to PLINY.

**Probe 8 — install.sh SKILL_NAMES append:**
```bash
grep -n "check-bw-release" \
  /c/Users/denso/claude_projects/the-stoa-arc-28/substrate/install.sh
```
PASS condition: line appears exactly once inside the `SKILL_NAMES=(...)` block (between `credential-discipline` and `)`), at the indent level of the existing entries.

**Probe 9 (widened per ADV-3) — cite-comment at the GitHub API parse site, full content match:**
```bash
# All four content claims the prose PASS condition makes:
grep -n "CITE:\|jallum/beadwork/releases/latest\|tag_name\|FAILURE-MODE\|§22 Step 2\|operating-disciplines\.md §22" \
  /c/Users/denso/claude_projects/the-stoa-arc-28/substrate/skills/check-bw-release/check.sh
```
PASS condition: `# CITE:` comment present immediately above `fetch_latest_release_tag()`; comment names the endpoint URL (`jallum/beadwork/releases/latest`); comment names the parsed field (`tag_name`); comment names the failure-mode symptom (the `FAILURE-MODE` block describes the defang + the caller-side guard); comment cross-refs `operating-disciplines.md §22 Step 2` AND names the `§22 Step 2` shorthand. All five grep alternatives produce at least one hit.

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

Per directive Phase C + project-tier POLYBIUS's 03:00:04Z trim + rev2 additions (one beat added for LBR-1 defang verification; one beat updated for the per-workspace state-file path). PLINY runs these before opening the PR:

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

   **First-invocation variant:** if `substrate/.bw-release-last-check` does not yet exist when the smoke beat runs (the file is runtime-grep-filtered, not gitignored; per §3 File 3 it's untracked-by-default but may be committed at operator discretion), the first run bootstraps the baseline with the "(baseline bootstrapped on first invocation)" suffix line. That's expected on the first smoke run; a second back-to-back run produces the plain "current" message.

3. **New-release-detected fixture:**
   ```bash
   BW_RELEASE_CHECK_LATEST_OVERRIDE=v0.99.0 \
   BW_RELEASE_CHECK_BASELINE_OVERRIDE=v0.13.0 \
     /c/Users/denso/claude_projects/the-stoa-arc-28/substrate/skills/check-bw-release/check.sh
   ```
   Expected output: "NEW BW RELEASE DETECTED" block with v0.99.0 / v0.13.0 / release notes URL / 3-axis checklist / suggested next action.

4. **LBR-1 defang smoke (added in rev2):**
   ```bash
   PATH=/nonexistent \
     /c/Users/denso/claude_projects/the-stoa-arc-28/substrate/skills/check-bw-release/check.sh
   echo "exit_code=$?"
   ```
   Expected: script emits "could not reach https://api.github.com/repos/jallum/beadwork/releases/latest" and exits 0. If exit code is non-zero, the LBR-1 defang regressed — stop and surface to PLINY before opening the PR.

5. **MAJOR_POLYBIUS.md §16.8 grep:**
   ```bash
   grep -n "bw recap\|bw attach\|## 16\.8\|### 16\.8\|--all" \
     /c/Users/denso/claude_projects/the-stoa-arc-28/substrate/MAJOR_POLYBIUS.md
   ```
   Expected: multiple hits inside §16.8; `--all` qualifier appears in the recap caveat (LBR-2 resolution check).

6. **operating-disciplines.md §22 grep:**
   ```bash
   grep -n "^## 22\.\|bw-upgrade discipline\|verify changelog claims empirically" \
     /c/Users/denso/claude_projects/the-stoa-arc-28/substrate/operating-disciplines.md
   ```
   Expected: `## 22. bw-upgrade discipline` heading, `bw-upgrade discipline` phrase, and the verify-changelog-empirically sub-bullet all present.

7. **install.sh SKILL_NAMES append:**
   ```bash
   grep -n "check-bw-release" \
     /c/Users/denso/claude_projects/the-stoa-arc-28/substrate/install.sh
   ```
   Expected: exactly one hit, inside the `SKILL_NAMES=(...)` block.

8. **install.sh --dry-run includes the new skill (per MAJOR_PLINY.md §5.7):**
   ```bash
   mkdir -p /tmp/arc-28-smoke
   /c/Users/denso/claude_projects/the-stoa-arc-28/substrate/install.sh \
     --target project --project-dir /tmp/arc-28-smoke --dry-run 2>&1 \
     | grep -n "check-bw-release"
   ```
   Expected: at least one line showing `check-bw-release` in the planned deploy. The dry-run plan walks `SKILL_NAMES` per install.sh's existing logic; an entry that doesn't appear here means the array append landed in the wrong spot.

---

## §6 — Self-assessed weak points (for ARGUS, rev2 lens)

Three places where ARGUS should look hardest at the rev2 picks. Honest, scoped to what rev2's structural choices rest on. Rev1's §6.1 and §6.2 are resolved into the design and removed; rev1's §6.3 (N=1 framing) is preserved as ratified; rev1's §6.4 (clone-shape defect inheritance) is preserved with a rev2 lens — the specific LBR-1 instance is fixed but the broader risk class persists.

### 6.1 — Per-workspace baseline drift creates a coordination question rev2 deliberately doesn't answer

LBR-3 was resolved by picking per-workspace deployment semantics: each workspace has its own `<workspace>/.claude/.bw-release-last-check`; baselines drift independently. **Weak point:** an operator who runs the skill at workspace A in week 1 and at workspace B in week 2 may see "current" at both invocations — A bootstrapped at week-1's upstream-latest, B bootstrapped at week-2's upstream-latest — and miss that upstream advanced between the two invocations. The "first invocation bootstraps silently" branch is by design (don't surface a "release" the first time the skill runs at any workspace), but the combination of per-workspace baselines + silent bootstrap means there is no global "did upstream advance since the last bw-upgrade arc shipped?" signal that the skill alone produces.

**Why this shape anyway:** the alternative (substrate-only) had its own coordination cost (consumer copies are dead weight; deploying them is a no-op). The actual canonical "did upstream advance since our last bw-upgrade arc?" question is answered by the operator looking at the substrate-tier baseline (`substrate/.bw-release-last-check`) — that's the workspace where bw-upgrade arcs are dispatched. Consumer copies are convenience invocations; their baselines are local-context-only. The mitigation is the documentation at §3 File 3 Section 8 ("Per-workspace deployment + baseline independence") which names this explicitly — but documentation is a soft mitigation. ARGUS: is the §3 File 3 Section 8 prose strong enough, or does the design need a mechanism (e.g., "if substrate-tier baseline differs from this workspace's baseline, mention it" cross-check)? My read: no, that mechanism couples the skill across workspaces and was rejected upstream in the substrate-only-vs-per-workspace decision.

### 6.2 — `bw recap` caveat split between default + `--all` requires reader to read carefully

The §16.8 `bw recap` caveat now distinguishes documented default (single-repo, works as designed) from `--all` variant (registry-conditional). **Weak point:** the caveat asks the reader to hold two pieces of context simultaneously — "plain bw recap is fine; --all has this gotcha." A reader skimming may either (a) read past the `--all` qualifier and remember "bw recap is broken on this install" or (b) read past the caveat entirely and remember "bw recap is fine." Both are misreads; the design relies on careful reading.

**Why this shape anyway:** the alternative (omit the `--all` caveat entirely) loses the empirically-observed gotcha — a future POLYBIUS hitting empty `bw recap --all` output has no on-disk explanation. The alternative (lead with a stronger warning) overstates the problem (plain `bw recap` is not broken). The careful split IS the correct framing; the soft mitigation is the §22 Step 2 cross-ref in the caveat which routes a future POLYBIUS to the discipline that would update this caveat if registry behavior changes. ARGUS: read the caveat prose for whether the `--all only` framing is foregrounded clearly enough — bold? leading-sentence position? — or if the design is OK with the current shape.

### 6.3 — C.1 N=1 framing borrows §16.6's shape; risk of over-fitting the analogy (ratified from rev1)

§22.3's N=1-provenance-plus-accretion-path subsection is structurally a near-copy of `MAJOR_POLYBIUS.md` §16.6 (Arc 27). **Weak point:** Arc 27's §16.6 was anchoring a discipline PRINCIPAL declared based on lived POLYBIUS-lifecycle experience; this arc's §22.3 anchors a discipline PRINCIPAL declared in response to a single bw release. The substrate-canon-off-gate framing IS the same; the empirical foundation differs in shape. Reading §22.3 as "PRINCIPAL declarations enter substrate canon on a routine basis" overgeneralizes both this case and §16.6.

**Why this shape anyway:** the §6.7.1 canon-promotion gate is the gate that disciplines this. The honest framing names the off-gate entry explicitly + the future-evidence-accretion requirement — which is what the §22.3 prose does. ARGUS already ratified this in rev1; preserved here for completeness. Catch: the design's own §1 problem statement uses "encode a bw-upgrade discipline" — that phrasing may set up the over-fit risk by treating the discipline as more settled than the N=1 anchor warrants. (ARGUS rev1 verdict ratified §22.3 prose as "tight against §16.6 Arc 27 template; no leak.")

### 6.4 — The check-bw-release skill is structurally a clone of check-substrate-updates; LBR-1 fixed but the class persists

C.2's design is intentionally clone-shaped against `check-substrate-updates` for operator-muscle-memory reasons. Rev1 named this risk in the abstract; rev1's skeleton then contained an instance of it (LBR-1: the unguarded `curl | python3` pipeline under `set -euo pipefail`). **Weak point:** the specific instance is fixed in rev2 (explicit defang at the pipeline boundary, matching `check-substrate-updates/check.sh:489-500`'s pattern), but the broader class — any future change to the skill that adds a new pipeline or external-command invocation may re-introduce the bug without the author noticing because the skeleton "looks right" — is not structurally prevented. The cite-comment at the parse site names the defang as the durable mitigation surface; the new Probe 7b (LBR-1 defang smoke) is the durable verification surface; but ADA or a future maintainer modifying the script outside those exact surfaces could regress.

**Why this shape anyway:** structural prevention (e.g., a wrapper that runs every external-tool call with `set +e` locally) would add complexity that obscures the script's intent. The clone-shape risk is real but the mitigations (cite-comment + Probe 7b + the `check-substrate-updates/check.sh:489-500` precedent comment) constitute the substrate's "name the bug class, name the mitigation, name the precedent, verify under simulated failure" pattern. ARGUS should specifically read the §3 File 4 skeleton against `check-substrate-updates/check.sh` for any defect-pattern the clone might still inherit silently (the empty-array guarded iteration under `set -u`; the `wc -l | tr -d ' '` BSD/GNU portability idiom — both not directly applicable here as the new script has no arrays-being-iterated and no `wc` calls, but the meta-question of "what pipefail-class bugs may still lurk" is real). The new Probe 7b is the durable mechanism by which the LBR-1-class regression is caught; if a future change introduces a new external-tool pipeline, ADA should add a parallel defang-smoke probe.

---

## §7 — Out of scope (the A7 hard-lock, restated for ADA)

This design deliberately does NOT cover, and ADA must NOT add during build:

- Removing `consumer-workspaces.txt` (the B.1 descope removed the deprecation header too; file stays untouched).
- Adopting bw 0.13.0 features beyond B.3 + B.4. The registry + cross-repo prefix resolution stay un-adopted at the substrate level pending a future arc with empirical evidence.
- Migrating existing on-disk handoff/retro/design artifacts to bw attachments. Forward-only.
- check-bw-release cron-scheduling defaults. Skill ships; operator decides whether to cron.
- Cross-workspace propagation of `check-bw-release`. `install.sh` deploys to consumer workspaces on next `--target project --project-dir <ws>` run; this arc does not propagate proactively.
- Adding `author: Denson Smith` to the two existing SKILL.md files (`agent-author`, `check-substrate-updates`) that lack it. Forward-adopt on the new SKILL.md; retro-edit is out of scope for this arc.
- Editing prior arcs' retros or directives to fit new conventions.
- Sibling `stoa--32b.1` / `stoa--32b.2` (separate forthcoming arcs).
- Any author-claim field that names anyone other than Denson Smith (A6 IMMUTABLE per `substrate/CLAUDE.md`).

If ADA finds any of the above tempting mid-build, STOP and surface to PLINY before proceeding.

---

End design REV2.
