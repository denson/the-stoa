# Arc 23 build directive — Verification-discipline scaffolding + substrate canon updates

**Audience:** the fresh Claude Code session opened to build Arc 23 deliverables (MAJOR_PLINY).
**Authored by:** project-tier MAJOR_POLYBIUS + the PRINCIPAL (Denson Smith).
**Status:** active directive.
**Bw ticket:** to be filed as the Arc 23 epic; this directive references the eight child tickets by ID (`stoa--4h7`, `stoa--tp1`, `stoa--fea`, `stoa--nax`, `stoa--148`, `stoa--vmc`, `stoa--rno`, `stoa--14u`).
**Builds on:** Arcs 1-22 (the-stoa main `19943ec`). Arc 22 (`stoa--jru`) is out of scope here — that arc stays parked.

**Your one job:** ship the verification-complexity framework (INCOMPLETE / UNVERIFIABLE verdict shapes + 2x2 quadrant classification) as the load-bearing scaffolding of the arc, and ride seven supporting substrate-canon updates along with it as a single coherent push. Eight tickets surfaced together during the 2026-05-12 bw → Ariadne integration + STRABO-fabrication + bw-scaling-wall cluster; this directive bundles them into one comprehensive substrate update so the verification framework ships **with** the disciplines that depend on it (fea inherits tp1, nax + 148 reinforce verifier-side hygiene, vmc + rno land the substrate-canon learnings from the same engagement) rather than as a sequence of patches.

This is a multi-concern arc with ~30 substrate-prose deliverables across 5 Phases. The cluster is internally coherent — every ticket traces to the same 2026-05-12 engagement and converges on the same verifier-tier role files. Per MAJOR_POLYBIUS §5.4, external review is recommended before dispatch (PRINCIPAL routes the directive through cold-Claude-session or external LLM if scope warrants).

---

## Comms — autonomous mode via bw, radio-check protocol

POLYBIUS (substrate-tier CoS, separate Claude Code session) and you both communicate via comments on the Arc 23 epic. PRINCIPAL is **not** the relay for routine status — beadwork is.

**bw command syntax** is in `substrate/MAJOR_PLINY.md` §6.1. Critical: `bw comment <id> "text"` is positional, no `-m` flag. `bw close <id> --reason "text"` — `--reason` is a flag.

**Polling discipline** per `substrate/operating-disciplines.md` §7 (surface-and-wait + radio-check). On dispatch, post an initialization handshake comment on the Arc 23 epic naming your cron id (if you set one up) and your cadence. Heartbeat every ≤30 min unless surface-and-wait-blocked. Cancel your cron the moment a substantive question is resolved.

POLYBIUS is in autonomous mode for this engagement. PRINCIPAL is exception-handler — project-direction calls, ship/no-ship, substance disagreement after one round, authorship/copyright/Denson-final-say content, irreducible ambiguity, peer silence > 60 min, arc closes.

---

## Read first

Before doing any design or build work, read:

1. **`substrate/operating-disciplines.md`** (`19943ec`) — current 14 sections + closer + lineage. You will add new sections §15-§17 (verification-complexity, bw-fit + layered-architecture, fork-over-upstream + agent-time-latency) and add subsections under §6 (redundant-checks: N=1 generalization + estimate-axis separation) and §8 (substrate-edit smoke beats; probe coverage of fallback chains).

2. **`substrate/MAJOR_PLINY.md`** — receives dispatch-protocol updates: new verdict-shape handling (INCOMPLETE / UNVERIFIABLE per tp1), no-narrowing-gauntlet-from-N=1 (per nax), post-STRABO VERA dispatch (per fea), install.sh-deploy-plan smoke-beat requirement (per 14u), fallback-chain probe discipline (per 148).

3. **`substrate/MAJOR_POLYBIUS.md`** — receives: TIMING_LOG / retrospective discipline note that N=1 conclusions are not enshrined as substrate-tier structural lessons (per nax).

4. **`substrate/CAPTAIN_VERA.md`** — receives §5.7 verification-complexity quadrant classification per probe (per tp1) + §5.8 STRABO-claim verification (per fea).

5. **`substrate/CAPTAIN_CATO.md`** — receives §6.7 verification-complexity quadrant per finding (per tp1) + §6.8 empirical environment reproduction for environment-interactive code (per 148).

6. **`substrate/CAPTAIN_ARGUS.md`** — receives §6.6 verification-complexity quadrant per risk (per tp1).

7. **`substrate/CAPTAIN_ZENO.md`** — receives §6.6 verification-complexity quadrant per criterion (per tp1).

8. **`substrate/CAPTAIN_STRABO.md`** — receives a section noting STRABO output is preliminary until VERA-verified for substrate-tier or upstream-bound propagation (per fea).

9. **`substrate/skills/save-verdict/SKILL.md`** (if present; if absent, locate the actual verdict-skill file or section that defines the verdict enum and corresponding schema). Schema extension: add INCOMPLETE + UNVERIFIABLE to the verdict enum + add quadrant_classification field + add coverage_description (INCOMPLETE) + sanity_check_performed + recommended_next_step (UNVERIFIABLE).

10. **The 8 ticket bodies:** `bw show stoa--4h7`, `stoa--tp1`, `stoa--fea`, `stoa--nax`, `stoa--148`, `stoa--vmc`, `stoa--rno`, `stoa--14u`. Each carries empirical anchors and substrate-touch-point lists. `stoa--tp1` carries a long POLYBIUS elevation comment (2026-05-12 18:24) that DAEDALUS treats as additional spec.

---

## Phase A — Architectural decisions (LOCKED pre-dispatch by POLYBIUS)

Settled during directive authoring. You do NOT need to surface these as design questions.

### A1. One arc, five phases, one gauntlet — LOCKED

Eight tickets cluster into one coherent substrate update. Bundling reduces churn (every ticket touches one or more of: operating-disciplines.md, MAJOR_PLINY.md, the four verifier CAPTAIN role files). Single ARGUS audit covers the integrated design. Single ADA worktree builds the feature branch covering all substrate files. Verifier seats (VERA / CATO / ZENO) each do one pass over the integrated diff.

Phasing:

| Phase | Seat(s) | Output |
|---|---|---|
| 0 | ADA (light) | `stoa--4h7` — bw upgrade to 0.13.0 (substrate infrastructure). Independent prerequisite. Single-step. |
| 1 | DAEDALUS + ARGUS | `agents/design/arc-23/design.md` — integrated design covering all 8 tickets' substrate touch-points. ARGUS cold-audits before ADA dispatches. |
| 2 | ADA | feature branch `arc-23/build` covering all substrate files (operating-disciplines.md additions, the five CAPTAIN role files, MAJOR_PLINY.md, MAJOR_POLYBIUS.md, save-verdict skill schema, install.sh if applicable). |
| 3 | VERA + CATO + ZENO | parallel verification pass over the feature branch. VERA probes per-file content. CATO cold-reads the entire diff for wording drift / schema consistency / cross-references. ZENO checks spec-vs-result (this directive's deliverables list vs the actual diff). |
| 4 | PLINY + smoke + ship | smoke beats (install.sh dry-run, markdown checks, grep beats per substrate file, save-verdict schema validates). PR opened on substrate main. PLINY runs `gh pr merge` after clean PASS. All 8 tickets closed. |

### A2. tp1 is the structural load-bearer — LOCKED

The verification-complexity framework (tp1) is the load-bearing scaffolding of this arc. All other tickets either:
- inherit the framework directly (fea: STRABO claims classified per quadrant before verification; nax + 148: verifier-side hygiene fits the same framework),
- update substrate canon that the framework's documentation references (vmc: bw-fit + layered-architecture; rno: fork-over-upstream + agent-time-latency), or
- are independent infrastructure that the arc can absorb cheaply (4h7: bw upgrade; 14u: smoke-beat discipline for install.sh-deployed files).

DAEDALUS designs tp1 first (load-bearing); the other tickets' designs slot into the framework. The integrated design.md presents tp1's framework FIRST, then walks each supporting ticket showing how it inherits / reinforces / extends the framework.

### A3. Verdict shape naming — LOCKED as INCOMPLETE / UNVERIFIABLE

DAEDALUS does NOT need to pick between INCOMPLETE / UNVERIFIABLE vs alternatives (BOUNDED / DEFERRED). PRINCIPAL approved INCOMPLETE / UNVERIFIABLE on tp1's elevation comment. DAEDALUS implements those names; surface only if a downstream consumer (the save-verdict skill, a role-file cross-reference) requires a different name for technical reasons.

### A4. operating-disciplines.md placement for the verification-complexity framework — LOCKED as inline

The 2x2, the four strategies, the two verdict shapes, the discipline rule all land **inline** in `operating-disciplines.md` as a new section (numbering per A5 below). DAEDALUS does NOT need to create a standalone `verification-complexity.md` doc.

Rationale: tp1's elevation comment estimated the section at <120 lines; everything inheriting from it (the role file cross-refs, save-verdict schema docs) needs to point at a stable anchor. Inline keeps the anchor mechanical (one file).

### A5. operating-disciplines.md section numbering — LOCKED

Current op-disc has §1-§14 + agent-regime closer + empirical lineage. New sections appended:

| Section | Source ticket | Title |
|---|---|---|
| §6.7 (subsection) | stoa--nax | N=1 generalization rule + estimate-axis separation (extending the existing §6 redundancy theme) |
| §8.3 (subsection) | stoa--14u | Substrate-edit smoke beats: install.sh deploy-plan check |
| §8.4 (subsection) | stoa--148 | Probe coverage of fallback chains |
| §15 | stoa--tp1 | Verification-complexity awareness (2x2 + INCOMPLETE / UNVERIFIABLE verdict shapes + four strategies + discipline rule + time/cost-box defaults) |
| §16 | stoa--vmc | bw-fit matrix + bw-as-write-substrate / Ariadne-as-read-projection / hypergraph-as-relational-extension layered-architecture framing |
| §17 | stoa--rno | Fork-over-upstream default for AI-team OSS dependencies + agent-time latency budget |

The "agent-regime inverses" closer stays after §17. Empirical lineage closer stays after that.

### A6. INCOMPLETE / UNVERIFIABLE verdict schema integration — LOCKED in shape, DAEDALUS picks specifics

The save-verdict skill (or whatever the verdict-emitting mechanism is — DAEDALUS surfaces if the skill isn't where expected) extends as:

- Add INCOMPLETE + UNVERIFIABLE to the verdict enum.
- Add a `quadrant_classification` field — required when verdict is INCOMPLETE or UNVERIFIABLE; one of `easy-easy` / `hard-easy` / `easy-hard` / `hard-hard`.
- For INCOMPLETE: require `coverage_description` — free-form prose: what was checked, what was not, bound used (iterations / state-space subset / time budget), confidence interval.
- For UNVERIFIABLE: require `sanity_check_performed` (free-form prose) + `recommended_next_step` (free-form prose).

The existing PASS / FAIL / NEEDS-REVISIONS paths are untouched. DAEDALUS picks: which exact file carries the schema, whether the new fields are JSONSchema-validated or free-form, whether INCOMPLETE / UNVERIFIABLE verdicts gate merge by default (locked answer: NO; both require operator disposition).

### A7. Time / cost-box defaults for INCOMPLETE-verdict verification — DAEDALUS picks concrete numbers

The principle is locked: bounded verification is bounded, not unlimited. Defaults DAEDALUS picks:
- INCOMPLETE-verdict bounded verification gets default time/cost box of N× normal probe budget for the dispatch.
- UNVERIFIABLE pulls the verifier out within a sanity-check budget (~1× normal probe budget).

DAEDALUS picks N (suggested anchor: 10× from tp1's elevation comment; DAEDALUS may justify a different number).

### A8. STRABO-verification routing — LOCKED per fea ticket

STRABO claims intended for substrate-tier or upstream-project propagation get a follow-on VERA dispatch with a citation-verification brief. PLINY scope-decides: full (every citation) vs sampled (random N of citations). DAEDALUS surfaces the sample-N policy (suggested anchor: N=3 for routine; full for upstream-bound).

### A9. nax verifier-side touch-point — LOCKED

`nax` extends operating-disciplines.md §6 (existing redundancy section) with two subsections: N=1 generalization rule, estimate-axis separation (Axis A: agent-team throughput; Axis B: upstream-substrate performance). The two comments on nax (2026-05-12T17:59:55Z and 2026-05-12T18:02:38Z) are spec-equivalent to the ticket body — DAEDALUS reads them as part of the spec.

### A10. Substrate-tier replication of workspace memories (rno) — LOCKED as inline

Two memories inline into operating-disciplines.md as §17 (per A5). Substrate does not currently have an explicit memory-canon mechanism; building one is out of scope for this arc. DAEDALUS picks the prose anchors but the placement is fixed (inline in op-disc).

### A11. Authorship attribution discipline — IMMUTABLE

All edits credit Denson Smith. No author field gets a different name. No exception under any phase.

---

## Phase 0 — bw upgrade (stoa--4h7)

**Independent prerequisite.** Can run before, during, or after Phase 1 design — ADA picks the timing. The upgrade does not block design but it should land before Phase 3 verification so VERA / CATO probe against the upgraded substrate.

Deliverable: bw 0.13.0 installed on the system. `bw --version` reports 0.13.0. Smoke: `bw list` works against the existing the-stoa store; no data loss; existing dependency graph intact.

Single-step. Close ticket with reason on completion. No design needed.

---

## Phase 1 — Design (DAEDALUS + ARGUS)

DAEDALUS produces `agents/design/arc-23/design.md` integrating all 8 tickets. Structure:

1. **Frame** — the 2026-05-12 cluster (STRABO fabrication, scaling wall, verifier-spins-forever) as the empirical anchor.
2. **tp1: verification-complexity framework** — the 2x2, the four strategies, the verdict shapes, the discipline rule, the time/cost-box defaults. Six worked examples (per tp1 elevation comment): easy-easy/PASS, hard-easy/FAIL, easy-hard/INCOMPLETE, hard-hard/UNVERIFIABLE, ARGUS easy-easy, ARGUS hard-hard.
3. **Role file cross-refs (VERA / CATO / ARGUS / ZENO)** — exact wording for each role file's new section. Self-consistent across the four files.
4. **fea: STRABO-verification** — VERA verifies STRABO claims for substrate-tier / upstream-bound propagation. Sampling policy (per A8). Self-tagging policy. CAPTAIN_STRABO addition (claims preliminary until verified).
5. **nax: redundant-checks + N=1 + estimate-axes** — op-disc §6.7 subsections. MAJOR_POLYBIUS TIMING_LOG-discipline note. MAJOR_PLINY no-narrowing-from-N=1 dispatch note.
6. **148: CATO empirical-env reproduction + probe-fallback coverage** — CATO_role §6.8; MAJOR_PLINY (or op-disc §8.4) probe-discipline note.
7. **vmc: bw-fit matrix + layered-architecture** — op-disc §16 verbatim from ticket body.
8. **rno: fork-over-upstream + agent-time-latency** — op-disc §17 verbatim from ticket body.
9. **14u: install.sh-deploy-plan smoke beat** — op-disc §8.3 + MAJOR_PLINY smoke-beat-discipline section (or directive-template update if such a template exists).
10. **save-verdict skill schema extension** — exact JSONSchema (or whatever the skill uses) extension.
11. **Self-referential acknowledgment** — the arc modifies the role files of the verifying CAPTAINs that verify the arc. This is the substrate updating itself in flight; verifiers read the *new* version of their own role files during Phase 3 verification. Not a circular dependency.

ARGUS cold-audits the design when DAEDALUS surfaces it. Looks for: missing quadrants in the 2x2, verdict-shape names that overload existing concepts, missing time/cost-box defaults, missing self-referential acknowledgment, missing PLINY dispatch protocol integration, wording drift across the four verifier role files, schema inconsistency between save-verdict and verdict-shape narrative, missing cross-references, scope creep beyond the eight tickets.

ARGUS verdict gate: ADA does not dispatch until ARGUS returns PASS. If ARGUS returns NEEDS-REVISIONS, DAEDALUS revises and re-surfaces.

---

## Phase 2 — Build (ADA single worktree, feature branch `arc-23/build`)

ADA receives DAEDALUS's design.md + ARGUS PASS verdict. Single worktree on substrate `main` (`19943ec` or later if Phase 0 has landed). Feature branch `arc-23/build`.

Files touched (expected; ADA confirms during build):

| File | Source tickets |
|---|---|
| `substrate/operating-disciplines.md` | tp1 (§15), vmc (§16), rno (§17), nax (§6.7 subsections), 14u (§8.3 subsection), 148 (§8.4 subsection if placed in op-disc) |
| `substrate/MAJOR_PLINY.md` | tp1 (dispatch protocol for INCOMPLETE / UNVERIFIABLE), nax (no-narrowing-from-N=1), fea (post-STRABO VERA dispatch), 14u (smoke-beat discipline), 148 (probe-coverage discipline if placed here) |
| `substrate/MAJOR_POLYBIUS.md` | nax (TIMING_LOG / retrospective discipline) |
| `substrate/CAPTAIN_VERA.md` | tp1 (§5.7 quadrant per probe), fea (§5.8 STRABO-claim verification) |
| `substrate/CAPTAIN_CATO.md` | tp1 (§6.7 quadrant per finding), 148 (§6.8 empirical-env reproduction) |
| `substrate/CAPTAIN_ARGUS.md` | tp1 (§6.6 quadrant per risk) |
| `substrate/CAPTAIN_ZENO.md` | tp1 (§6.6 quadrant per criterion) |
| `substrate/CAPTAIN_STRABO.md` | fea (claims preliminary until VERA-verified) |
| `substrate/skills/save-verdict/...` | tp1 (verdict enum + new fields). ADA locates the actual file. |
| `substrate/install.sh` | only if 14u's smoke-beat discipline lands a deploy-list check mechanism here; DAEDALUS decides during design. If 14u is a pure-doc discipline (in op-disc + MAJOR_PLINY), install.sh is not touched. |

ADA writes probes/tests for each touched file as part of the worktree (per Stoa's normal probe-authoring discipline). Probes are inputs to Phase 3 VERA.

ADA commits incrementally. ADA does NOT merge to substrate main. ADA hands the feature branch to Phase 3.

---

## Phase 3 — Verify (VERA + CATO + ZENO parallel)

VERA, CATO, and ZENO dispatch in parallel on the `arc-23/build` feature branch. Three independent verification streams.

**VERA probes** — content checks per file:
- operating-disciplines.md contains §15 (verification-complexity heading), §16 (bw-fit matrix heading), §17 (fork-over-upstream + agent-time heading), §6.7 (N=1 + estimate-axes subsections), §8.3 (substrate-edit smoke beats), §8.4 (probe coverage fallback chains).
- Each CAPTAIN role file contains its expected new section.
- save-verdict schema validates an example INCOMPLETE verdict and an example UNVERIFIABLE verdict.
- The two example verdicts also validate that the new required fields are enforced (omitting quadrant_classification on INCOMPLETE fails schema).

VERA classifies each probe per the new framework (per tp1) and reports quadrant classification in the verdict — this is the first dispatch where the new framework applies to VERA's own probes. Most probes are easy-easy (file contains string, schema accepts/rejects example). VERA's verdict structure becomes a worked example of the framework in action.

**CATO cold-reads** — entire diff for wording drift across the four verifier role files, schema-vs-narrative consistency, cross-reference correctness, scope creep, authorship attribution (the immutable rule).

**ZENO spec-vs-result** — this directive's deliverables list (the file table in Phase 2) vs the actual files modified in `arc-23/build`. Each deliverable maps to an edit. Each edit maps to a deliverable. No orphans.

All three verifiers may raise NEEDS-REVISIONS; ADA addresses, re-surfaces, verifiers re-verify. Cycle until clean PASS from all three.

---

## Phase 4 — Smoke + Ship (PLINY)

Smoke beats:
1. `bash substrate/install.sh --dry-run --target project --project-dir <test-dir>` lists every modified substrate file in its deploy plan. If any new file was added (e.g., a new save-verdict skill file), it must appear in install.sh's hardcoded deploy lists. **This is the 14u smoke-beat discipline applied to this arc itself.**
2. Same for `--target subproject` and `--target user`.
3. `markdownlint substrate/operating-disciplines.md` and the role files pass (or substrate's actual markdown-validation mechanism).
4. `grep -n "INCOMPLETE\|UNVERIFIABLE" substrate/CAPTAIN_*.md` returns matches in all four verifier role files.
5. `grep -n "quadrant" substrate/operating-disciplines.md` returns the new §15 framework.
6. save-verdict schema validates a sample INCOMPLETE + UNVERIFIABLE verdict; rejects a malformed one.
7. bw 0.13.0 confirmed via `bw --version`.

PLINY opens the PR titled `Arc 23 — verification-discipline scaffolding + substrate canon updates`. PR body summarizes the 8 tickets + the design.md location + the verdict-shape additions + the role-file changes.

After PR is approved (POLYBIUS or PRINCIPAL), PLINY runs `gh pr merge`. PLINY closes each of the 8 tickets with a reason citing the merge commit SHA.

PLINY writes a TIMING_LOG entry capturing estimate vs actual + lessons learned. Per nax (which lands in this very arc), the TIMING_LOG does NOT enshrine N=1 conclusions as structural lessons.

---

## Out of scope (per directive)

- `stoa--jru` Arc 22 (coordination hygiene: bw-timeline parsing + cron expiry) — separate theme, separate arc
- `stoa--vz9` EPIC (operating-disciplines promotion from project CLAUDE.md to substrate) — separate large EPIC
- `stoa--kjo` EPIC (per-agent git identity) — separate large EPIC
- Implementing a halting-problem solver or formal verification tools — out of scope; the discipline is to RECOGNIZE undecidability, not solve it
- Adding new verifying CAPTAIN seats — existing seats inherit the framework
- Building a substrate-memory canon mechanism — `rno` lands the two memories inline in op-disc; a structured memory-canon system is a future arc if warranted
- Forking jallum/beadwork to add a TreeFS-incremental-tree-update patch — the bw-fit matrix documents WHEN bw is the right choice; forking is a future option if a future project genuinely needs bw at > 5k scale
- Refactoring the existing PASS / FAIL / NEEDS-REVISIONS verdict path — the schema extension is additive only

---

## Deliverable summary

8 tickets closed. ~30 substrate-prose edits across ~9 files. One feature branch merged to substrate main. One TIMING_LOG entry. Substrate canon now carries the verification-complexity framework + the four supporting disciplines.

Standby, run.
