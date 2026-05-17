# Arc 28 build directive — Adopt bw 0.13.0 features at substrate + encode bw-upgrade discipline

**Audience:** the fresh Claude Code session opened to build Arc 28 deliverables (MAJOR_PLINY at the-stoa tier).
**Authored by:** user-tier MAJOR_POLYBIUS + the PRINCIPAL (Denson Smith).
**Status:** active directive. **Arc 27 (`stoa--32b.3`) is CLOSED** + **ariadne--c71 is CLOSED** (Railway container bw 0.12.3 → 0.13.0 shipped at ariadne-core main `b7f92e5`). Both preconditions satisfied.
**Bw ticket:** `stoa--s6n` (the work-unit; independent of `stoa--32b` epic but shares the substrate-canon-adoption theme).
**Builds on:** Arcs 1-27 (the-stoa main as of `7964bef`).

**Your one job:** ship two coupled pieces as a single coherent push. **Part B:** adopt bw 0.13.0 features at substrate level (registry replaces consumer-workspaces.txt; cross-repo issue resolution; attachments + recap as available primitives). **Part C:** encode a bw-upgrade discipline so future bw releases have a clear process — a new operating-disciplines.md section + a lightweight `check-bw-release` skill that operationalizes the trigger step. The two pieces are coupled deliberately per §15 honest-scope: C generalizes from B (the empirical anchor); encoding both together means the discipline gets baked while the empirical surface is fresh.

One ticket, one coherent push:
- **stoa--s6n** (P1) — substrate adoption + discipline encoding. **DAEDALUS treats ticket body as primary input prose alongside this directive.** The body sketches 7 deliverables; this directive locks the architectural decisions DAEDALUS would otherwise re-derive.

This is medium-scope substrate-canon work. Larger than Arc 27 (single-section addition); smaller than Arc 25 (multi-section + multi-CAPTAIN). Single DAEDALUS round expected; rev2 possible if ARGUS surfaces real defects.

---

## Comms — autonomous mode via bw, radio-check protocol

Same shape as Arcs 25/26/27. PROJECT-TIER POLYBIUS (separate Claude Code session, activated from `HUMAN_paste-polybius-arc-28-instruction.md`) is your radio-check peer; you communicate via comments on `stoa--s6n`. USER-TIER POLYBIUS dispatched this arc + will do QA pass at arc close per PRINCIPAL's 2026-05-16 pattern.

PRINCIPAL is **not** the relay for routine status — beadwork is.

**bw command syntax** is in `substrate/MAJOR_PLINY.md` §6.1. Critical: `bw comment <id> "text"` is positional, no `--body` flag. `bw close <id> --reason "text"` — `--reason` is a flag.

**Polling discipline** per `substrate/operating-disciplines.md` §7. On dispatch, post init handshake comment on `stoa--s6n` naming cron id + cadence. Heartbeat every ≤30 min.

PLINY is in autonomous mode. PRINCIPAL + user-tier POLYBIUS are exception-handlers — project-direction calls, ship/no-ship, substance disagreement after one round, authorship/copyright/Denson-final-say content, irreducible ambiguity, peer silence > 60 min, arc closes.

---

## Read first

Before any design or build work, read in order:

1. **`bw show stoa--s6n` ticket body in full.** Primary spec. The body has problem statement + Part B (B.1-B.4 substrate adoption sub-deliverables) + Part C (C.1 discipline doc + C.2 lightweight skill) + 7 deliverables + acceptance probes + hard-locked out-of-scope + §15 N=1 caveat. Treat as primary input prose alongside this directive.

2. **`bw show ariadne--c71`** at the ariadne-core-workspace bw store (cross-tier read; user-tier POLYBIUS confirmed shipped at ariadne-core main `b7f92e5`). The empirical anchor for the bw-upgrade-discipline encoding — the worked example of the deployment-side axis (Dockerfile bump + ingest smoke). C.1 cross-refs this work.

3. **`substrate/MAJOR_POLYBIUS.md`** — especially §7 (Communication / bw operations), §12 (bw cookbook — wait, §12 lives in operating-disciplines.md per Arc 23 reorg; double-check), and §16 (POLYBIUS session lifecycle — Arc 27's load-bearing section; B.3 + B.4 extend it).

4. **`substrate/operating-disciplines.md`** — full read. Current section count + numbering. The new bw-upgrade-discipline section (C.1) inserts at the appropriate locus (likely after §21 Ariadne-search-ready authoring, or as a new section closer to the bw-related disciplines).

5. **`substrate/skills/check-substrate-updates/`** — `SKILL.md` + `check.sh` + `apply.sh`. B.1 modifies `check.sh` to replace consumer-workspaces.txt read with `bw registry list` parse. The cite-comment-at-the-read-site mitigation pattern (apply_substitutions, Arc 26 source-side parsing) is the model the new bw-registry parse should follow.

6. **`substrate/consumer-workspaces.txt`** — current registry contents (4 entries). B.1 deprecates this file; add a deprecation comment + cross-ref to the bw-registry adoption.

7. **`substrate/install.sh`** — `SKILL_NAMES` array (around line 140). B+C adds `check-bw-release` to SKILL_NAMES (deliverable 7).

8. **bw 0.13.0 changelog** — excerpted in `ariadne--c71` body. Most relevant for B: registry / cross-repo resolution / attachments / recap. Most relevant for C: the breadth of features illustrates why the impact-axis classification matters.

---

## Phase A — Architectural decisions (LOCKED pre-dispatch)

Settled during PRINCIPAL's 2026-05-16 chat discussion + ticket evolution. You do NOT surface these as design questions.

### A1. One arc, four phases, one gauntlet — LOCKED

`stoa--s6n` is a coherent single work-unit. Single DAEDALUS design covering Parts B + C. Single ARGUS audit. Single ADA worktree on `arc-28/build`. Verifiers (VERA + CATO + ZENO) each one pass over the integrated diff. **CATO is mandatory** — substrate canon work; wording-precision matters; future POLYBIUSes read this for life-of-the-substrate.

Phasing:

| Phase | Seat(s) | Output |
|---|---|---|
| 1 | DAEDALUS + ARGUS | `agents/design/arc-28/design.md` — integrated design covering check.sh registry-parse migration; consumer-workspaces.txt deprecation pattern; MAJOR_POLYBIUS.md doc extensions for cross-repo + attachments + recap (locate the right sections); operating-disciplines.md new section for bw-upgrade-discipline (locate section number); check-bw-release skill design (state file, GitHub API query, output shape, mocked-tag fixture for tests); install.sh SKILL_NAMES append. ARGUS cold-audits before ADA dispatches. |
| 2 | ADA | feature branch `arc-28/build` covering all substrate edits + the new skill files. |
| 3 | VERA + CATO + ZENO | parallel verification pass per Phase B acceptance probes. CATO cold-reads entire diff for wording drift, scope creep, cross-reference correctness, authorship attribution. ZENO checks spec-vs-result against stoa--s6n's 7 deliverables. |
| 4 | PLINY + smoke + ship | smoke beats (per Phase C below). PR opened. PLINY runs `gh pr merge` after clean PASS. `stoa--s6n` closes. **User-tier POLYBIUS does QA pass at arc-close per PRINCIPAL pattern — PLINY tags `[for: user-tier POLYBIUS]` on stoa--s6n.** |

### A2. Part B sub-deliverables — LOCKED scope; DAEDALUS scopes precision

**B.1 — Registry replaces consumer-workspaces.txt:**
- `check.sh` no-args sweep: replace `read consumer-workspaces.txt` block with `bw registry list` parse. Cite-comment at the parse site points to bw 0.13.0 changelog entry (same cite-comment-at-the-read-site mitigation as `apply_substitutions` + Arc 26's `parse_skill_names_from_install`).
- `--workspace <path>` mode is unchanged (no registry dependency).
- `consumer-workspaces.txt` gains a deprecation comment header: "DEPRECATED — bw 0.13.0's host-local registry obsoletes this file; see SKILL.md / operating-disciplines.md §<bw-upgrade-discipline>. Will be removed in a follow-up arc."
- DAEDALUS sub-decision: does `bw registry list` need parsing for paths only, or does it need handling for additional fields (prefix, registered-time)? Either is defensible; pick one and document rationale.

**B.2 — Cross-repo issue resolution doc:**
- Add a subsection to `MAJOR_POLYBIUS.md` §7 (Communication / bw operations) OR `operating-disciplines.md` §12 (bw cookbook). DAEDALUS picks the right locus.
- Document the pattern: `bw show stoa--abc` resolves prefix to registered repo without `cd`-ing. `bw -C <prefix>` accepts registered prefix as well as path.
- Worked examples: user-tier POLYBIUS reading ariadne-- tickets from any cwd; project-tier POLYBIUS reading sibling stoa-- tickets without navigating.

**B.3 — Attachments as available primitive:**
- Add a subsection to `MAJOR_POLYBIUS.md` §16 (POLYBIUS lifecycle / multi-artifact handoff). Document: `bw attach <ticket-id> <file-path>` stores arbitrary files at `attachments/<ticket-id>/<path>` on the beadwork ref.
- Frame as **available primitive**, NOT forced migration. Existing on-disk handoff/retro/design artifacts stay where they are. Forward-only convention; arc authors may attach future artifacts to the parent ticket OR keep on disk (operator preference).

**B.4 — Recap as available primitive:**
- Add a subsection to `MAJOR_POLYBIUS.md` §16 (POLYBIUS lifecycle) AND/OR §7 (Communication). Document: `bw recap` shows cursor-driven incremental activity across registered repos.
- Worked example: POLYBIUS picking up after compaction can run `bw recap` to see what's happened since its last read-point.
- Forward-only; no forced adoption.

### A3. Part C sub-deliverables — LOCKED scope; DAEDALUS scopes precision

**C.1 — operating-disciplines.md new section: bw-upgrade discipline:**
- 5-step process per stoa--s6n body: Trigger → Review → File tickets → Dispatch → Verification.
- Impact-axis classification: deployment-side / substrate-side / workspace-side. Each axis with examples drawn from the 0.12.3 → 0.13.0 work (deployment = ariadne--c71 Dockerfile; substrate = B.1 registry adoption; workspace = subprocess-call-site regression risk like bw_ingest.py).
- Empirical anchor pointer at the bottom: the 0.12.3 → 0.13.0 work (this arc + ariadne--c71) as the canonical worked example.
- Section number: DAEDALUS picks based on current operating-disciplines.md state. ARGUS confirms placement is consistent with existing section logic.

**C.2 — Lightweight skill: substrate/skills/check-bw-release/:**
- New skill directory with `SKILL.md` + `check.sh` (mirror the shape of `check-substrate-updates`).
- Behavior: query bw GitHub releases API for current latest tag; compare to known-baseline stored in a state file (similar to `.substrate-last-check`); if new release detected, print changelog excerpt + impact-axis classification template + suggested next action.
- State file location: `substrate/.bw-release-last-check` (substrate-level, not per-workspace).
- Operator can cron the check or run on-demand. Skill operationalizes step 1 of the discipline; classification + filing is still operator (POLYBIUS) judgment.
- Tests: mocked-tag fixture for "new release detected" path; current-tag fixture for "current" path. DAEDALUS picks fixture approach (file-based mock, function-injection, env-var override — pick one and document).

### A4. consumer-workspaces.txt deprecation lifecycle — LOCKED

This arc adds a deprecation comment header to the file; **does NOT delete the file**. The bw registry adoption (B.1) makes the txt file functionally obsolete, but the txt file remains as a one-release deprecation marker. A follow-up arc removes the file entirely after operator confidence that bw registry is stable across workspaces.

The deprecation comment header should:
- Name the obsoleting mechanism (bw 0.13.0 host-local registry)
- Cross-ref the SKILL.md update + the operating-disciplines.md bw-upgrade-discipline section
- State the removal-arc condition ("removal follows once registry is verified stable across all consumer workspaces")

### A5. Cite-comment discipline — LOCKED

Wherever new code reads bw output formats (B.1's check.sh registry parse), place a cite-comment at the parse site referencing bw 0.13.0's documented output shape. Same pattern as `apply_substitutions` + Arc 26's `parse_skill_names_from_install`. The cite-comment is the durable mitigation for coupling to bw's CLI output format — surfaces the linkage at the read site, not at code-review time.

For the check-bw-release skill (C.2), the bw GitHub releases API endpoint is the coupling point; cite-comment names the endpoint.

### A6. Authorship attribution — IMMUTABLE per CLAUDE.md

All edits credit Denson Smith. No exception. Arc 28 adds new files: `substrate/skills/check-bw-release/SKILL.md` (frontmatter), `substrate/skills/check-bw-release/check.sh` (no frontmatter; shell script). For SKILL.md frontmatter: include `author: Denson Smith` per the convention adopted at stoa--uly today. Verify all new files before commit.

### A7. Out of scope — HARD LOCKED

Do NOT do in this arc, even if temptation surfaces during build:

- **Removing consumer-workspaces.txt entirely.** One-release deprecation (A4); removal is a follow-up arc.
- **Adopting bw 0.13.0 features beyond B.1-B.4.** Any future-bw-release follow-on adoption is its own ticket.
- **Migrating existing on-disk handoff/retro/design artifacts to bw attachments.** Forward-only convention (A2 B.3).
- **check-bw-release skill cron-scheduling defaults.** Skill exists; operator decides whether to cron.
- **Cross-workspace propagation of the new check-bw-release skill.** Substrate update arc deploys it via install.sh; consumer workspaces get it on next apply.
- **Editing existing arcs' retros or directives to fit any new convention.** Forward-only.
- **The two sibling stoa--32b children (PRINCIPAL-gate, mechanical-script/agent-inspection split).** Separate forthcoming arcs.

If you find yourself reaching for any of the above, STOP and surface as substance-disagreement comment on `stoa--s6n` (radio-check to user-tier POLYBIUS via [for: user-tier POLYBIUS] tag).

### A8. §15 N=1 honesty — LOCKED

The bw-upgrade discipline (C) is encoded with N=1 empirical anchor (this 0.12.3 → 0.13.0 work). PRINCIPAL declared the need for a discipline today (project-direction authority); substrate canon enters off-gate. Future bw releases accrete supporting evidence per §6.7.1 three-condition gate; if the discipline's classification axes turn out wrong-shaped, future arcs revise.

The arc must NAME this provenance in the new C.1 section — same shape as Arc 27's §16.6 ("N=1 provenance + accretion path" subsection). Do NOT over-generalize beyond what PRINCIPAL named.

---

## Phase B — Verify (probes for VERA)

1. **Registry parse regression:** `check.sh` no-args sweep against current registered workspaces returns same set as today's `consumer-workspaces.txt` list (the 4 paths: ariadne-core-workspace, railway_stoa, sector-4, the-stoa).
2. **Registry parse correctness:** modify a workspace's registration locally (e.g., add a fake-path entry via `bw registry add`), run `check.sh`, verify the fake-path shows up in the sweep + reports NOT-FOUND or similar.
3. **Deprecation header presence:** `consumer-workspaces.txt` has the deprecation comment at top; existing entries preserved.
4. **Cross-repo doc:** the new MAJOR_POLYBIUS.md or operating-disciplines.md subsection includes `bw show <prefix>--<id>` example.
5. **Attachments + recap docs:** present in MAJOR_POLYBIUS.md §16 (or designated locus); framed as available primitives, not forced migration.
6. **bw-upgrade-discipline section:** 5 steps + 3 impact axes present; empirical-anchor pointer at the bottom names ariadne--c71 + this arc.
7. **check-bw-release skill:** SKILL.md frontmatter has `author: Denson Smith`; `check.sh` is executable; current-tag fixture returns "current"; mocked-future-tag returns "new release detected" with changelog template.
8. **install.sh SKILL_NAMES:** `check-bw-release` appended.
9. **Cite-comments:** new bw-output-parsing sites carry cite-comment per A5.
10. **CURRENT regression:** check.sh against all 4 workspaces still reports CURRENT (the change is internal to check.sh's source-side input; verdict shape unchanged). Note: the-stoa itself will show DRIFTED on the substrate files this arc edits; that's expected.

CATO cold-reads:
- the diff for wording drift, scope creep, cite-comment correctness, cross-reference correctness, output-format coherence.
- §15 N=1 honesty: verify C.1 names the N=1 + PRINCIPAL-declaration provenance; does NOT over-generalize.
- Authorship discipline: all new files credit Denson Smith.

ZENO checks stoa--s6n deliverables 1-7 each marked DONE by artifact reference.

---

## Phase C — Smoke + ship

PLINY's smoke beats before opening PR:

- `bash -n substrate/skills/check-substrate-updates/check.sh` + `bash -n substrate/skills/check-bw-release/check.sh` — syntax check.
- `check.sh` no-args against current registered workspaces — same 4 workspaces sweep.
- `check.sh --workspace /c/Users/denso/claude_projects/the-stoa` — works.
- `check-bw-release/check.sh` (or however the skill invokes) — returns "current" against bw 0.13.0.
- `grep -n "DEPRECATED" substrate/consumer-workspaces.txt` — header present.
- `grep -n "bw-upgrade discipline" substrate/operating-disciplines.md` — section present.
- `grep -n "bw recap\|bw attach\|bw show.*--" substrate/MAJOR_POLYBIUS.md` — primitives documented.
- `grep -n "check-bw-release" substrate/install.sh` — SKILL_NAMES append.

PR title: `Arc 28: substrate adoption of bw 0.13.0 features + bw-upgrade discipline (registry, cross-repo, attachments, recap; doc + skill)`
PR body: cross-ref `stoa--s6n`, parent epic if any (none — this arc is independent of stoa--32b), prior `ariadne--c71`, this directive at `substrate/arcs/arc-28-build-directive.md`.

Merge via `gh pr merge` after clean gauntlet PASS. Close `stoa--s6n` with `--reason` referencing the merge commit. Tag `[for: user-tier POLYBIUS]` comment inviting QA pass.

---

## Honest scope reminder

Medium-scope substrate-canon work. Larger than Arc 27 (one section + one template + minor); smaller than Arc 25 (multi-section + multi-CAPTAIN envelope). One DAEDALUS round expected; rev2 if ARGUS surfaces real defects. PLINY heads-down should run in ~30-60 min wall-clock. If you find yourself an hour in without a green ADA verdict, surface — something's off.

End directive.
