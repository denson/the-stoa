# Arc 72 build directive — Graduate decision-surface, the guide front (self-correction doctrine, slice 3)

**Audience:** the fresh Claude Code sessions opened to build Arc 72 (PLINY_the-stoa + the floor-manager POLYBIUS_the-stoa).
**Authored by:** Polybius_the_Stoa (user-level Stoa agent, sid 990b0750-5572-4836-b9c7-18d626a12e96) on behalf of the PRINCIPAL (Denson Smith).
**Status:** DRAFT — pending PRINCIPAL review, then NOMOS-on-the-directive, then committed + launched.
**Builds on:** current the-stoa main (Arc 70 dilemma-classifier + Arc 71 decision-register both shipped + deployed). Project-tier charter: **`stoa--xa4`**.
**Design input (READ IT FIRST):** `docs/self-correction-doctrine-DRAFT.md` (the doctrine) + `substrate/skills/decision-surface/SKILL.md` (the v0.1 DRAFT skill being graduated — and its built-in "Open questions" list, which IS the design agenda) + `substrate/skills/decision-surface/worked-example-debloat.md` (the canonical end-to-end run).

**You are MAJOR_PLINY for the Arc 72 engagement.** Read `substrate/MAJOR_PLINY.md` and assume the orchestrator role. Open Claude Code in `C:\Users\denso\claude_projects\the-stoa\`.

**The reframe driving this arc (load-bearing — hold it through every design choice):** the value is **NOT** the agent *classifying* a thing as dilemma-or-not. It is **flagging that we MAY be in a no-clean-answer situation, and GUIDING the human through deciding** — a *process*, not a verdict. This dissolves the **cave-trap**: an agent defending a classification can be argued off it (a dilemma-avoiding user pushes, a please-trained agent folds, together they launder a hard value-call into a fake clean answer); an agent *running a process* has no label to be argued off of. The firmness relocates from "hold the verdict" to "ensure the deciding actually happens with the tradeoff kept visible." Build everything to serve that.

**Your one job:** graduate the `decision-surface` skill from DRAFT to gauntlet-shipped, retune detection to *flag-and-guide* instead of *classify-and-assert*, and wire the three doctrine pieces — classifier (the FLAG, Arc 70) → decision-surface (the GUIDE, this arc) → decision-register (the RECORD, Arc 71) — into **one loop sharing one schema**. **Not** the consumer-tier variant, **not** the slice-2b reader. Those are named follow-ons.

**Full gauntlet** (DAEDALUS → ARGUS → ADA → VERA → CATO → NOMOS). **Standard POLYBIUS+PLINY team** — substrate-component design (a skill graduation + a module tweak + wiring + a corpus), not a custom agent/workflow, so **no CHIRON/HAMILTON**.

---

## Comms — async with Polybius_the_Stoa via bw (`stoa--*`)

Coordinate on the charter **`stoa--xa4`**. Polybius_the_Stoa (user-level owner) monitors + interjects; the floor-manager runs independent verification at each hand-back and relays up. The PRINCIPAL is NOT the relay — beadwork is. Asymmetric polling: don't poll while working; do poll when waiting. `bw comment <id> "text"` is **positional, no `-m`**; **no backticks or `$()` in comment bodies**. Run `bw prime` at activation. Every seat signs `[from: <NAME> | sid <session-id>]` (sid via the `whoami` skill).

---

## Read first

1. **`substrate/skills/decision-surface/SKILL.md`** — the whole skill, ESPECIALLY its "Open questions" section (the 6 Qs are the design agenda). It is already rich (the problem/dilemma spine, competing-bads, anti-agreeableness honest-broker, capacity×stakes, ground-before-propose, a procedure, Part-2 rendering). Graduating ≠ rewriting — it is *resolving the open Qs + wiring + shipping*.
2. **`substrate/skills/decision-surface/worked-example-debloat.md`** — how the behavior looks in practice.
3. **The doctrine** `docs/self-correction-doctrine-DRAFT.md` — §1 (problem/dilemma spine), §3 (lock-spine/free-tact), §5/§6 (the black box + longitudinal loop), §7/§7.5 (why the guide matters: default-sycophantic AI is a perfect ass-covering machine; the skill is trainable).
4. **What this wires to (both shipped):** `substrate/modules/dilemma-classifier.md` (the FLAG — esp. §2 the self-check, §3 delivery) and `substrate/modules/decision-register.md` (the RECORD — esp. §2 the 9-field schema). The guide is the missing middle that connects them.
5. **The deploy gap:** `bw show stoa--ida` + `substrate/install.sh` SKILL_NAMES (line ~228) — decision-surface is on disk + shown in the app but absent from SKILL_NAMES, so it does not deploy. Graduating closes this.

---

## The build target (slice 3 — the guide front)

1. **Flag-and-guide retune of the classifier** — `substrate/modules/dilemma-classifier.md` §3 delivery: detection **opens the guide** (flags the possibility, runs the process) rather than asserting a verdict to defend. Small + surgical. **Preserve §1 LOCKED + §2 self-check unchanged** — the spine does not weaken; it relocates.
2. **Graduate `decision-surface`** — resolve the load-bearing open questions with WORKED content (signals, thresholds, mechanisms — not just instructions), strip the DRAFT status, make it gauntlet-shippable.
3. **The one-loop wiring + shared schema** — classifier-FLAG → decision-surface-GUIDE → decision-register-RECORD compose into one loop; the fields the guide walks through ARE the decision-register's 9-field schema (the guided decision is what gets logged).
4. **Deploy** — add decision-surface to `install.sh` SKILL_NAMES; resolve the app/install.sh parity; close `stoa--ida`.
5. **A verification corpus** — including cave-resistance fixtures (pressure-to-verdict → the guide holds the tradeoff visible, does NOT cave), mirroring the Arc-70 pressure-fixture pattern.

---

## Design items — DAEDALUS resolves in Phase A (surface at the design hand-back)

- **DC0 — flag-and-guide delivery rewrite (classifier §3), spine preserved (LOAD-BEARING).** Rewrite the dilemma-classifier §3 so detection flags the possibility + opens the guide as a *process*, not a verdict. The §1 LOCKED list and the §2 self-check are UNTOUCHED (show this — diff proves the spine survived). Honest: this REMOVES the cave-lever (no verdict to defend) without weakening the anti-cave machinery (§2 still does the work). No drive-by edits to the rest of the module.
- **DC1 — graduate decision-surface: resolve the open Qs with worked content.** Q1 detection mechanics (concrete, observable signals that a human has lost the thread / is in groupthink, + the response); Q4 render-vs-prose threshold (a sharp rule for when a decision earns an interactive surface vs a paragraph); Q5 dilemma-honesty-under-pressure — **the cave-trap guardrail: reuse the classifier §2 self-check as the named mechanism**, applied to the guide's "human pushes hard for a verdict" case. Q2 expert-referral sourcing: ship a v1 grounded-web-search sub-step; the bias-free-selection hard problem is named + may accrete (do NOT pretend it is fully solved). Strip the DRAFT/status frontmatter. Keep `worked-example-debloat.md` as the canonical run.
- **DC2 — the one-loop wiring + shared schema + skill-vs-module reachability.** Specify how the FLAG opens the GUIDE and the GUIDE feeds the RECORD: the guide's output structure IS the decision-register §2 nine-field schema (a completed guided-decision is loggable with no translation). Resolve the reachability seam honestly: decision-surface is a SKILL (invoked via the Skill tool); the classifier+register are MODULES composed into role files; the doctrine checkpoints fire on POLYBIUS + PLINY (orchestrators that HAVE the Skill tool). Confirm the guide is orchestrator-tier-reachable at those checkpoints (or justify any lightweight module shim). No reach into the Arc-70/Arc-71 module *logic* beyond the §3 retune (DC0).
- **DC3 — deploy: SKILL_NAMES + app/install.sh parity + deploy-safety.** Add `decision-surface` to `install.sh` SKILL_NAMES; resolve the stoa--ida inconsistency (app shows it, install.sh didn't ship it) so the two agree; confirm the skill + its worked-example deploy correctly and gen-data still derives a clean roster. Close `stoa--ida` at ship.
- **DC4 — verification corpus + honest stance.** A corpus that proves: the flag opens the guide on a real dilemma and NOT on a solved problem (both directions); **cave-resistance** (pressure-to-verdict fixtures where the guide must keep the tradeoff on the table and refuse to launder it — the Arc-70 pressure-fixture analog); the render-threshold rule fires correctly. A stated FLOOR (not 100%), `--check-corpus` deterministic / `--judge` judgment split, mirroring the Arc-70/71 corpus shape. **Honest stance (LOCKED):** the guide RAISES the probability of honest deciding + leaves a fingerprint; it is NOT a hard gate (the "it always fails without — the baseline is guaranteed silent caving" framing justifies *building* it, but the *claim* stays "high-probability + regression-guard," never "guaranteed"). Same honesty posture Arc 70/71 shipped.

---

## Deliverables (land together)

1. The flag-and-guide classifier §3 retune (DC0) — spine-diff-clean.
2. The graduated `decision-surface` skill (DC1) — open Qs resolved, DRAFT stripped.
3. The one-loop wiring + shared-schema spec (DC2).
4. SKILL_NAMES + parity + `stoa--ida` closed (DC3).
5. The verification corpus + runner (DC4).
6. Charter `stoa--xa4` updated with the landing SHA + per-item disposition; no stale refs.

---

## Verification / Definition of done

- **Mechanical (close-gate):** the §3 retune preserves the spine (the existing **dilemma corpus still passes**, and a diff shows §1/§2 untouched); decision-surface graduates (DRAFT stripped, the named open Qs resolved with worked content, deployed via SKILL_NAMES, **`stoa--ida` closed**); the one-loop wiring composes (the guide opens at the Arc-70 checkpoints; its output matches the Arc-71 register schema — grep/diff proves it); the new corpus passes at the DC4 floor incl the cave-resistance fixtures; the **FULL close-gate suite green INCLUDING BOTH existing corpora** (dilemma 19/19 + decision-register 18/18 — regression, because this arc edits shared machinery), plus `gen-data` deterministic, `vitest`, author-gate, stop-hook; **NOMOS CONFORMANT**; `Author=PRINCIPAL` + the §28.9 seat trailer.
- **Judgment (honest stance):** the guide **accretes** from real use; it raises the probability of honest deciding and makes a cave detectable — it is NOT a guaranteed gate. Do NOT over-claim (that would be the exact fake-certainty this doctrine kills).

---

## Out of scope (named follow-on arcs — do NOT fold in)

- **The consumer-tier decision-surface variant** (open Q3) — the skill itself says "track it as its own artifact; do not water this one down." Its own future arc.
- **Slice 2b** — the complaint-time callback + the re-verify gate (the deferred reader half of the black box).
- **The meta-trigger auto-detect-circling counter** (arc 4).
- **The broader checkpoint rollout** beyond the existing Arc-70/71 checkpoint set.
- **Rebuilding the Part-2 rendering** — `interactive-html-preview` already ships; decision-surface drives it as-is.

---

## Discipline

- Full gauntlet — substrate canon + a shipped skill + two shipped modules touched; not mechanical. Standard POLYBIUS+PLINY (no CHIRON/HAMILTON).
- The reframe is the spine: flag-and-guide (a process), never classify-and-defend (a verdict). A design that re-introduces a verdict-to-defend is an automatic route-back.
- Touch the Arc-70/71 modules ONLY as DC0/DC2 specify (the §3 retune + the schema-share). No drive-by changes to their logic; the regression bar (both corpora pass) is the guard.
- One coherent slice; keep the diff scoped to the guide front (DC0–DC4).
- bw syntax: positional `bw comment`, no backticks/`$()`; `bw prime` at activation; `--reason` on close.

## Suggested phasing

- **Phase A — design (DAEDALUS).** Resolve DC0–DC4; the flag-and-guide retune (DC0, spine-preserving) and the open-Q resolutions (DC1, esp. Q5 the cave-trap) are the load-bearing pieces. Surface to the floor-manager for go/no-go before build.
- **Phase B — build (ADA).** The §3 retune → the graduated skill → the wiring + shared schema → SKILL_NAMES/parity → the corpus.
- **Phase C — verify (ARGUS/VERA/CATO + NOMOS).** Spine-preserved diff; the guide opens/holds correctly both directions + under pressure; full suite incl BOTH existing corpora; `stoa--ida` closed; ground-truth.
- **Phase D — ship.** Commit + push; update `stoa--xa4` with the SHA + dispositions.

Standby, run.
