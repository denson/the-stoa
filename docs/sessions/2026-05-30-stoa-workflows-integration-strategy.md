# Strategy — the Stoa + dynamic workflows (integration plan + task-type taxonomy)

**Date:** 2026-05-30 · **Author:** Denson Smith · **Seat:** MAJOR_POLYBIUS (the-stoa forge)
**Status:** forward strategy / proposal (not yet ratified canon — N=1 evidence; accrete per `operating-disciplines.md` §6.7.1)

> Provenance: this synthesizes a single working session that (a) compared Claude Code dynamic workflows to the gauntlet, (b) built + battle-tested the `workflow-composer` skill, (c) ran the gauntlet itself as a workflow and caught a real error, (d) prototyped mechanical discipline-enforcement. Source runs: `wf_01ba8f65-6dc` (review), `wf_0c5fa492-e9e` (gauntlet-design), `wf_ee8c98f8-04d` (discipline-gate). Tickets: `stoa--04n`, `stoa--q36`, `stoa--ilt`, `stoa--aox`, `stoa--7b1`, `stoa--xyb`, `stoa--myd`. Skill: `substrate/skills/workflow-composer/SKILL.md`. The "attention-scarcity" thesis referenced below is external source material surfaced this session; it restates the Stoa's own existing north star (`operating-disciplines.md` — "where is human attention required").

---

## 0. The thesis in one line

Generation is abundant; **direction is scarce**. The Stoa+workflow combination exists to spend scarce human direction efficiently — mechanize generation *and* verification so cheaply and in parallel that human attention is reserved for the two things only it can do: **deciding what to build** and **catching what no rule anticipated**.

## 1. How the combination works

**Workflows do not replace the gauntlet. They are an execution substrate for the gauntlet's methodology.** Keep the role files, the disciplines, the verdict philosophy, the multi-checker-convergence value (`stoa--myd`). Move the *orchestration plumbing* onto workflows where the task shape fits. Three layers, with a hard rule about which may be mechanized:

| Layer | Question it answers | Mechanize? | Home |
|---|---|---|---|
| **Inner loop** (the gauntlet) | "Is it well-built / correct?" | **Yes** → workflows | DAEDALUS→ARGUS→ADA→VERA→CATO→ZENO as stage-workflows |
| **Discipline-enforcement** (new) | "Was this *rule* followed?" | **Yes** → gates/checkers | deterministic gate (free) / checker agent / schema field |
| **Outer loop** (user-tier POLYBIUS) | "Is this the *right thing / right direction*?" | **Never** | human + judgment; fed by a review-surface |

The dividing line is the thesis: you can mechanize *"was the discipline followed?"* but never *"is this the right direction?"* — direction is scarce **because** it is not checkable.

**The structural pieces (validated this session):**
- **Gauntlet → stage-workflows**, split at the HITL seams. Stage A (research→design→audit) → **HARD STOP** → Stage B (build→verify→review→spec). The runtime's "no mid-run input" constraint *forces* the pre-build gate — it's ksge's P4 (`stoa--7b1.7`) made structural.
- **CAPTAIN reuse via `agentType`** — our real seats run as workflow agents, tool-restrictions and role disciplines intact (ARGUS still can't write; it returned empty `suggested_fix`).
- **Verdict → `schema`** — typed PASS/PARTIAL/FAIL, validated + retried by the runtime. Retires the `save-verdict` file-write bugs (`stoa--wq0`/`7b1.2`).
- **Review-surface for the outer loop** (`stoa--ilt`) — emit the distilled residue (close calls, low-confidence, filtered-out findings, divergences), not raw output. Protects the scarce outer loop from being starved by context economy.
- **Workflow produces, launcher lands** — the script can't run `bw`/`git`; it returns the verdict, and PLINY/POLYBIUS writes to bw + commits (keeps the ship decision in a judgment seat, `§4.6`).
- **Deploy** — workflows are saved via the runtime `/workflows`→`s` dialog into `.claude/workflows/` (project) or `~/.claude/workflows/` (personal). There is **no `install.sh` deploy for workflows** (a corrected overclaim — see `stoa--04n`).

## 2. When to use what (the calibration — grounded in real cost)

| Tool | Cost (observed) | Use for | Don't use for |
|---|---|---|---|
| **Deterministic gate** (in-script) | **0 tokens** | reducible disciplines: authorship fields, voice grep, pre-branch git, cron | anything needing judgment |
| **Checker agent** (focused) | **~34k tokens / check** | the judgment edge a regex can't reach (prose/meta attribution) | bulk reducible checks (use the gate) |
| **Cheap review workflow** (2 agents) | ~54k / ~1 min | grouping/sanity, decomposition checks | correctness-critical verification |
| **Full gauntlet-workflow** (≥3 seats) | ~200k / ~7 min | correctness-critical design/build | trivial changes |
| **Classic PLINY gauntlet** (no workflow) | per-arc | HITL-mid-pipeline + cross-session arcs | parallel fan-out (it can't) |
| **Mode 2 pairing** (no workflow) | conversational | unknown shape ("I don't know what I want") | known-shape execution |

Headline economic lesson: **deterministic gates are the workhorse (free); agent-checkers are the specialist (~34k each).** And the workflow-gauntlet trades ~4× the tokens for a deeper catch — spend it where correctness matters.

## 3. Task-type taxonomy — coding AND non-coding

**The combination organizes by task *shape*, not by domain.** A code migration and a document-corpus restructure run through identical machinery, because orchestration is about shape, not content. This is why the Stoa is a *direction-scarce-work* machine, not merely a coding tool — and why non-coding work (writing, research, analysis, decisions) often benefits *more*, since its generation is even cheaper and its bottleneck even more purely direction.

| # | Task shape | Mode / workflow shape | Where human attention goes (the gate) | Coding example | Non-coding example |
|---|---|---|---|---|---|
| 1 | **Single-target build** (known shape) | Mode 1 gauntlet as a *linear* stage-workflow (A→HARD STOP→B) | approve the design at the HARD STOP; ship/no-ship | implement a feature; fix a bug | write a specific doc; produce a named analysis |
| 2 | **Fan-out audit** (many items, same check) | `parallel`/`pipeline` fan-out → synthesize → completeness-critic | read the synthesized findings; decide what to act on | audit every endpoint for auth; find all deprecated-API uses | check every doc section for a claim; authorship-audit every marketplace entry |
| 3 | **Migration at scale** (many items, transform each) | `pipeline` + `isolation:'worktree'` → verify each → synthesize | approve the transform on a *sample* before unleashing all | rename a symbol across 500 files; codemod an API | re-template every doc; re-tag a ticket corpus |
| 4 | **Exploration** (unknown shape) | **Mode 2 pairing — NOT a workflow** | continuous: you *are* the direction | spike an approach; prototype a design | draft positioning; sketch a structure |
| 5 | **Decision among options** | judge-panel: `parallel` N options → `parallel` judges → synthesize | **the decision itself** (workflow prepares + scores; human chooses) | pick an architecture among 3; choose a library | pick a strategy; choose a direction |
| 6 | **Review of existing work** | dimensions in `parallel` → adversarially verify each → review-surface | read the review-surface; adjudicate disputed findings | review a PR/diff; security-review | fact-check a report; audit a plan (we did this on `stoa--7b1`) |
| 7 | **Research / synthesis** | multi-modal sweep → fetch → cross-check/vote → synthesize (`/deep-research`) | frame the question; read the cited report | research an API's current behavior; find known-bug fixes | literature synthesis; a cited briefing |
| 8 | **Discipline-enforcement** | gate/checker embedded as a pass-condition in any of the above | none, when it passes — that's the point | authorship/voice/security-pattern gate | authorship/attribution gate on docs; citation-validity gate |

Reading the table: rows 1–3 are *generation* shapes (build/audit/migrate); rows 5–7 are *judgment-support* shapes (decide/review/research); row 4 is the **anti-workflow** (never fan-out to *find* direction); row 8 is the cross-cutting enforcement layer that rides inside the others. In every row, the "where human attention goes" column is the load-bearing design choice — that is the scarce resource being spent.

Two domain-specific notes:
- **Coding** leans on rows 1–3 + 6 + 8, and the gauntlet's correctness checkers (VERA/ZENO) earn their keep because generation is abundant but *not reliably correct* (this session, a generated skill had a category error caught only by the 3-seat gauntlet).
- **Non-coding** leans on rows 5–7 + 8, and the *discipline-enforcement* layer is disproportionately valuable: authorship/attribution, citation validity, and voice/brand consistency are exactly the recurring failure modes of abundant prose generation, and most are deterministically gateable (free).

## 4. Roadmap (phased, mapped to tickets)

- **Phase 0 — DONE (this session).** Three prototypes validated at N=1: review (`wf_01ba…`), gauntlet-design (`wf_0c5f…`, caught a real error), discipline-gate (`wf_ee8c…`). `workflow-composer` skill drafted + tightened to delta-only.
- **Phase 1 — harden the skill into forge canon** (`stoa--04n`). Design is ready (Stage-A done, `agents/design/stoa--04n/design.md`); build = one-line `SKILL_NAMES` add + the 4-location `check.sh` cite fix + `gen-data` guard. Run through the gauntlet (`§18.2`).
- **Phase 2 — bank the proven workflows** as saved commands via the runtime save dialog: a `/gauntlet-design` and a personal `/cold-audit` outer-loop amplifier in `~/.claude/workflows/`.
- **Phase 3 — battle-test the full gauntlet** (Stage A + Stage B) on a real small arc, *alongside* the classic gauntlet; compare context cost + defect parity. This is the decision-grade evidence for "port the gauntlet."
- **Phase 4 — first discipline migration** (`stoa--aox`): wire a deterministic authorship gate into the build-stage workflow; measure the prose-debloat against `stoa--xyb`.
- **Phase 5 — accrete toward canon.** As Phases 1–4 add observations, promote the N=1 disciplines (`stoa--q36`, `stoa--ilt`, `stoa--aox`) per the `§6.7.1` gate. Do not canonize on this session's single data point.

## 5. Guardrails (the don'ts)

1. **Workflows execute direction; they never set it** (`stoa--q36`). Distinguish execution-autonomy (safe) from direction-autonomy (never). A clean workflow-PASS may auto-ship *only* when the direction was human-gated upstream.
2. **Never fan-out to find direction.** Unknown shape → Mode 2 pairing, not a workflow (row 4).
3. **Never starve the outer loop.** Every workflow emits a review-surface (`stoa--ilt`); context economy must not become "PASS, shipped" with nothing for the human to catch.
4. **Who checks the checker.** A wrong gate gives false-green (cf. the `save-verdict` `/tmp` silent-green). Prefer deterministic gates; spot-verify agent-checkers; mechanical enforcement covers only *known* disciplines — the unanticipated stays the outer loop.
5. **Respect the cost.** Don't spin a ~34k-token agent for a check a free regex handles.

## 6. Open questions (honest, for future arcs)

- Exactly where the execution/direction-autonomy line sits in practice (`stoa--q36`).
- Which disciplines are tier-i (deterministic) vs tier-ii (agent) vs stay-human — the migration map (`stoa--aox`).
- Whether a canonical `/gauntlet` workflow should ever ship via the substrate at all, given the runtime's save-dialog model is the only documented deploy path (`stoa--04n`).
- Whether the review-surface generalizes cleanly beyond workflows into a universal substrate principle (`stoa--ilt`).

---

*This is a strategy proposal at N=1, not ratified canon. It records the session's findings and a sequenced path; each phase produces the evidence the next decision needs.*
