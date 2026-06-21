# Arc 70 build directive — Dilemma-detection classifier + deterministic triggers (self-correction doctrine, slice 1)

**Audience:** the fresh Claude Code sessions opened to build Arc 70 (PLINY_the-stoa + the floor-manager POLYBIUS_the-stoa).
**Authored by:** Polybius_the_Stoa (user-level Stoa agent, sid 990b0750-5572-4836-b9c7-18d626a12e96) on behalf of the PRINCIPAL (Denson Smith).
**Status:** DRAFT — pending PRINCIPAL review, then NOMOS-on-the-directive, then committed + launched.
**Builds on:** current the-stoa main. Project-tier charter: **`stoa--y1a`**.
**Design input (READ IT FIRST):** `docs/self-correction-doctrine-DRAFT.md` — the full doctrine. This directive builds **slice 1 (the detection front)** of it.

**You are MAJOR_PLINY for the Arc 70 engagement.** Read `substrate/MAJOR_PLINY.md` and assume the orchestrator role. Open Claude Code in `C:\Users\denso\claude_projects\the-stoa\`.

**Your one job:** build the **detection front** — a composable dilemma-detection *classifier* that runs on two *deterministic* triggers (an explicit user call, and the identified workflow/agent checkpoints), plus the labeled corpus that verifies it. Detection + honest delivery only. **Not** the accountability loop, **not** the auto-detect-circling meta-trigger, **not** graduating the `decision-surface` skill — those are named follow-on arcs (see Out of scope).

**Full gauntlet** (DAEDALUS → ARGUS → ADA → VERA → CATO → NOMOS). **Standard POLYBIUS+PLINY team** — substrate-component design, not a custom agent/workflow, so **no CHIRON/HAMILTON**.

---

## Comms — async with Polybius_the_Stoa via bw (`stoa--*`)

Coordinate on the charter **`stoa--y1a`**. Polybius_the_Stoa (user-level owner) monitors + interjects; the floor-manager runs independent verification at each hand-back and relays up. The PRINCIPAL is NOT the relay — beadwork is. Asymmetric polling: don't poll while working; do poll when waiting. `bw comment <id> "text"` is **positional, no `-m`**. Run `bw prime` at activation. Every seat signs `[from: <NAME> | sid <session-id>]` (sid via the `whoami` skill).

---

## Read first

1. **The doctrine** `docs/self-correction-doctrine-DRAFT.md` — especially §1 (problem-vs-dilemma spine), §2 (detection: triggers-not-a-detector), §3 (lock-spine/free-tact), §4 (the diagnostic tree), §5 (guilt-not-shame), and the **Resolved** section (storage/transparency are arc-2; this arc is detection only).
2. **The charter `stoa--y1a`** (full body — the locked scope + DoD).
3. The substrate surfaces a classifier module would touch: `substrate/modules/` (the composable-module home + `canonical-template-alignment.md` discipline), `substrate/install.sh` (how modules deploy + compose), the orchestrator role files (`substrate/MAJOR_POLYBIUS.md`, `substrate/MAJOR_PLINY.md`), and the author-gate test harness `substrate/hooks/tests/` (the both-directions fixture-corpus pattern to mirror).

---

## The build target (slice 1)

1. **A composable dilemma-detection CLASSIFIER module** — the problem-vs-dilemma check + plain-language explanation + route rule + the lock-spine/free-tact delivery discipline. A `substrate/modules/` unit that composes into the target role files (the §2 "triggers, not a dilemma-detector" stance: the module *is* the judgment the trigger invokes).
2. **Two DETERMINISTIC triggers only:**
   - **(a) explicit call** — the user says "detect dilemma" (+ a small synonym set); the agent runs the classifier.
   - **(b) workflow/agent checkpoints** — the classifier fires when the identified agents engage at their decision points. DAEDALUS scopes the **minimal high-value arc-1 subset** (DC2).
3. **A SEED CORPUS** — labeled problem-cases and dilemma-cases, **both directions**, including **camouflaged dilemmas** (the dangerous ones that look like problems), with a runner. This is the verification artifact (mirror the Arc-69 author-gate fixture pattern).

---

## Design items — DAEDALUS resolves in Phase A (surface at the design hand-back)

- **DC0 — module form + composition homes.** Confirm the classifier is a composed module (works for skill-less CAPTAINs via inline, per the doctrine's skill-vs-module analysis); specify WHICH role files / templates it composes into for slice 1, and the install.sh composition mechanics (project-tier separate-file vs subproject inline). No drive-by changes to unrelated composition.
- **DC1 — the explicit-trigger mechanism.** How "detect dilemma" (+ synonyms) is recognized and routes to the classifier (a disposition line in the orchestrator role? a thin skill? resolve + justify). Must be unambiguous and not over-fire on incidental mentions.
- **DC2 — the workflow-checkpoint subset.** Pick the minimal, highest-leverage set of agent-engagement checkpoints to wire for slice 1 (the doctrine names planning-entry, team spin-up, prioritization/routing, directive-lock — choose the arc-1 subset and justify; defer the rest). Specify the deterministic wiring (in the role files / workflow templates), NOT a heuristic.
- **DC3 — the corpus + pass criteria.** Structure of the labeled fixtures (problem / dilemma / camouflaged-dilemma), the runner, and a **floor accuracy** that is the close-gate bar (the Arc-69 author-gate *suite ran* 29/0, an absolute bar fit for a deterministic gate — a judgment classifier instead needs a stated FLOOR + both-directions controls). Be honest that 100% is not the bar.
- **DC4 — lock-spine/free-tact encoding (LOAD-BEARING).** Write the module so the LOCKED non-negotiables (don't fake certainty; don't cave to pushback; plain language by default; the §4 diagnostic tree + guilt-not-shame on pushback) are enforced and a sycophancy-trained consumer agent cannot collapse them — while the per-user TACT stays free. This is the one genuine design risk; design it explicitly.
- **DC5 — plain-language delivery.** The problem-vs-dilemma explanation surfaced to a user is **plain** (no PROBLEM/DILEMMA jargon), concrete to the issue, protective-not-punting; the framework is taught only on dilemma-avoidance pushback (per §4).

---

## Deliverables (land together)

1. The classifier module + its composition into the slice-1 target surfaces (role files / templates regenerated; `gen-data` re-run).
2. The explicit-trigger + workflow-checkpoint wiring (DC1 + DC2).
3. The seed corpus + its runner (DC3) — both-directions, camouflaged-dilemma controls included.
4. Charter `stoa--y1a` updated with the landing SHA + per-item disposition. No stale refs in touched docs.

---

## Verification / Definition of done

- **Mechanical (close-gate):** the module composes into the target role files (grep/diff proves it); **both triggers fire** correctly (explicit call routes; the wired checkpoints invoke) — exercised, not asserted; the **seed corpus passes both-directions at the DC3 floor**, with the camouflaged-dilemma controls catching and the problem-controls NOT over-firing; the full close-gate suite green (`npm run gen-data` deterministic, `vitest`, author-gate tests, stop-hook tests); **NOMOS CONFORMANT** on the final commit; `Author=PRINCIPAL` + the §28.9 seat trailer.
- **Judgment (honest stance):** corpus-passing is the verifiable proxy; the classifier's judgment **accretes** through dogfood — "good enough to rely on + a regression-guarding corpus," NOT "perfect." Do not over-claim a judgment capability as fully verified (that would be the exact failure this arc exists to prevent).

---

## Out of scope (named follow-on arcs — do NOT fold in)

- **The meta-trigger auto-detect-circling counter** — deferred deliberately, to be designed later from dogfood data (the rounds-since-decision counter), not guessed now.
- **The bw decision-register + complaint-time callback + re-verify gate** — Arc 2 (the accountability / longitudinal loop).
- **Graduating `decision-surface` from DRAFT** — its own arc; see `stoa--ida` (the SKILL_NAMES gap).
- **The broader checkpoint rollout** beyond the DC2 slice-1 subset.

---

## Discipline

- Full gauntlet — substrate canon + tooling; not mechanical. Standard POLYBIUS+PLINY (no CHIRON/HAMILTON).
- Deterministic triggers only — wire the WHEN; the classifier is the WHAT. No heuristic auto-detection in this slice.
- One coherent slice; keep the diff scoped to the detection front (DC0–DC5). No drive-by refactors.
- bw syntax: positional `bw comment`; `bw prime` at activation; `--reason` on close.

## Suggested phasing

- **Phase A — design (DAEDALUS).** Resolve DC0–DC5; the corpus design + the lock-spine/free-tact encoding are the load-bearing pieces. Surface to the floor-manager for a go/no-go before build.
- **Phase B — build (ADA).** The module + composition → the two triggers → the corpus + runner.
- **Phase C — verify (ARGUS/VERA/CATO + NOMOS).** Both-directions corpus at floor; both triggers exercised live; full close-gate suite; ground-truth.
- **Phase D — ship.** Commit + push; update `stoa--y1a` with the SHA + dispositions.

Standby, run.
