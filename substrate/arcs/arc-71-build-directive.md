# Arc 71 build directive — Decision-register CAPTURE (self-correction doctrine, slice 2a / the black box, capture half)

**Audience:** the fresh Claude Code sessions opened to build Arc 71 (PLINY_the-stoa + the floor-manager POLYBIUS_the-stoa).
**Authored by:** Polybius_the_Stoa (user-level Stoa agent, sid 990b0750-5572-4836-b9c7-18d626a12e96) on behalf of the PRINCIPAL (Denson Smith).
**Status:** DRAFT — pending PRINCIPAL review, then NOMOS-on-the-directive, then committed + launched.
**Builds on:** current the-stoa main (Arc 70 shipped at `8804ab8` + self-apply `8b6ef98`). Project-tier charter: **`stoa--7gl`**.
**Design input (READ IT FIRST):** `docs/self-correction-doctrine-DRAFT.md` — the full doctrine. This directive builds **slice 2a (the black box, capture half)** of it.

**You are MAJOR_PLINY for the Arc 71 engagement.** Read `substrate/MAJOR_PLINY.md` and assume the orchestrator role. Open Claude Code in `C:\Users\denso\claude_projects\the-stoa\`.

**Your one job:** build the **capture half** of the black box — at the deterministic checkpoints where the Arc-70 dilemma-classifier returns DILEMMA *and a choice is actually taken*, write a **structured, transparent, user-readable decision-register entry to bw** (the dilemma, the warning/tradeoff, the chosen option, the counter-hypothesis), plus the both-directions corpus that verifies it fires when it should and not when it shouldn't. **Writing the record only.** **Not** the complaint-time callback, **not** the re-verify gate, **not** dose calibration — those are slice 2b, the deferred reader half (see Out of scope).

**Full gauntlet** (DAEDALUS → ARGUS → ADA → VERA → CATO → NOMOS). **Standard POLYBIUS+PLINY team** — substrate-component design, not a custom agent/workflow, so **no CHIRON/HAMILTON**.

---

## Comms — async with Polybius_the_Stoa via bw (`stoa--*`)

Coordinate on the charter **`stoa--7gl`**. Polybius_the_Stoa (user-level owner) monitors + interjects; the floor-manager runs independent verification at each hand-back and relays up. The PRINCIPAL is NOT the relay — beadwork is. Asymmetric polling: don't poll while working; do poll when waiting. `bw comment <id> "text"` is **positional, no `-m`**; **no backticks or `$()` in comment bodies** (shell substitution mangles them). Run `bw prime` at activation. Every seat signs `[from: <NAME> | sid <session-id>]` (sid via the `whoami` skill).

---

## Read first

1. **The doctrine** `docs/self-correction-doctrine-DRAFT.md` — especially **§6 (the accountability moves / the longitudinal loop)** and the **Resolved** section (the black box is a *structured, ex-ante decision-register entry* in bw — "the act of writing it is half the value" — NOT a raw recording; transparent + user-readable by default; the surfacing/callback/re-verify-gate is the *deferred* half). Also §1 (problem-vs-dilemma spine) and §7/§7.5/§8 for why the record is the keystone.
2. **The charter `stoa--7gl`** (full body — the locked scope + DoD).
3. **What Arc 70 shipped (this builds directly on it):** `substrate/modules/dilemma-classifier.md` (the read this arc records the outcome of), its checkpoint wiring in `substrate/MAJOR_POLYBIUS.md` (§3.6 explicit call + the prioritization/team-spin-up checkpoints) and `substrate/MAJOR_PLINY.md` (§5.18 directive-lock checkpoint), and its corpus + runner at `substrate/modules/tests/dilemma-classifier/` (the both-directions fixture + runner pattern to mirror).
4. The substrate surfaces this touches: `substrate/modules/` (the composable-module home + `canonical-template-alignment.md` discipline), `substrate/install.sh` (module deploy + the two-owner composition mechanics arc 70 exercised), and the verdict-attach / `save-verdict` helper pattern (a precedent for a deterministic bw-write helper, if DC3 wants one).

---

## The build target (slice 2a — capture only)

1. **A composable decision-register CAPTURE module** — given a dilemma-decision (the Arc-70 classifier returned DILEMMA, the tradeoff was illuminated, and the PRINCIPAL chose a path), it writes ONE structured bw entry: **the dilemma, the warning(s)/tradeoff, the option chosen, the counter-hypothesis** (what concretely would prove the choice wrong), and a timestamp / decision-context link. Composes into the target role files (mirror the Arc-70 module-composition mechanics).
2. **The write trigger + over-write guard** — the entry is written when a dilemma-decision is *taken*, at the Arc-70 checkpoint subset + the explicit-call path. It does **NOT** fire on: a problem solved (no dilemma), a dilemma merely *illuminated but not decided*, or an incidental mention. The register records **decisions**, not detected tradeoffs.
3. **The bw-write mechanics** — how the structured entry is actually written (a deterministic template / optional helper, respecting the positional-`bw comment` + no-backtick footguns), **transparent and user-readable by default** (a decision journal on the PRINCIPAL's side, not a hidden dossier). Honest about the single-user-readable vs team-transparent cases.
4. **A both-directions verification corpus** — should-write fixtures (real dilemma + a choice taken → a well-formed entry) and should-NOT-write fixtures (problem / illuminated-not-decided / incidental mention → no entry), with a runner. Mirror the Arc-70 corpus pattern (manifest-driven, both-directions, stated floor, exit-nonzero-on-fail).

---

## Design items — DAEDALUS resolves in Phase A (surface at the design hand-back)

- **DC0 — register home + entry schema (HIGHEST LEVERAGE).** Where the register lives in bw — a comment stream on a single standing decision-register ticket, one ticket per decision, or another construct — and the exact structured fields (dilemma / warning(s) / options-with-costs / chosen / counter-hypothesis / timestamp / context-link). **Design the schema to be *re-readable by the deferred 2b callback*** even though 2b is not built here — that is the load-bearing forward-constraint. Keep it minimal-but-sufficient; we will learn the right shape from real entries (do not over-engineer the schema now).
- **DC1 — the write-trigger predicate + over-write guard.** Precisely when an entry is written: the deterministic "a dilemma-decision was *taken*" condition (classifier returned DILEMMA AND a path was chosen). Specify the guard that prevents logging problems, illuminated-but-undecided tradeoffs, and incidental mentions. This is the analog of the Arc-70 over-fire guard; design it to be corpus-testable.
- **DC2 — composition home + which seats write.** Which role files the capture composes into (the Arc-70 checkpoints live in MAJOR_POLYBIUS + MAJOR_PLINY — confirm same homes), and whether the capture is a **new module** (`decision-register.md`, separating the write from the Arc-70 read) or an extension of `dilemma-classifier.md`. Justify; specify the install.sh composition mechanics (reuse the Arc-70 two-owner pattern if applicable). No drive-by changes to unrelated composition.
- **DC3 — the bw-write mechanics + transparency.** How the entry is deterministically formatted and written (template inline vs a small helper script à la `save-verdict` / the verdict-attach pattern), honoring the bw footguns. How transparency/user-readability is guaranteed (the decision-journal-not-dossier property). Account for single-user vs team deployment.
- **DC4 — the "writing is half the value" device (LOAD-BEARING).** The schema/template must force the agent to actually *name* the tradeoff and a concrete counter-hypothesis at decision-time — a hollow entry (e.g. an empty/vacuous counter-hypothesis) must be *obviously* hollow (the Arc-70 `WHY:`-field analog). Design the structural device that makes the writing discipline real rather than perfunctory. **Honest stance:** template+prose-enforced, NOT a hard non-collapsible gate (same honesty posture Arc 70 shipped — do not over-claim).
- **DC5 — the verification corpus + pass criteria.** Structure of the should-write / should-not-write fixtures, the runner, and a stated **floor** (not 100%) as the close-gate bar, with both-directions controls (should-write entries are well-formed; should-not-write cases produce no over-write). Honest that the classification of "a decision was taken" is model judgment, not a pure shell check (mirror the Arc-70 `--check-corpus` deterministic / `--judge` judgment split).

---

## Deliverables (land together)

1. The capture module + its composition into the slice-2a target surfaces (role files regenerated; `gen-data` re-run).
2. The write-trigger wiring + over-write guard (DC1 + DC2).
3. The bw-write mechanics/template/helper (DC3).
4. The both-directions corpus + runner (DC5).
5. Charter `stoa--7gl` updated with the landing SHA + per-item disposition. No stale refs in touched docs.

---

## Verification / Definition of done

- **Mechanical (close-gate):** the module composes into the target role files (grep/diff proves it); the write **fires at the checkpoints when a dilemma-decision is taken** and a **real structured entry lands in bw** with every field populated — exercised live, not asserted; the **over-write guard holds** (no entry on a problem / illuminated-not-decided / incidental mention); the **both-directions corpus passes at the DC5 floor**; the full close-gate suite green (`npm run gen-data` deterministic, `vitest`, author-gate tests, stop-hook tests, + the new corpus runner); **NOMOS CONFORMANT** on the final commit; `Author=PRINCIPAL` + the §28.9 seat trailer.
- **Judgment (honest stance):** the entry **schema's rightness accretes** through real logged decisions — this is the *minimal-sufficient capture, designed to be read by the deferred 2b callback*, NOT a closed loop. The value is the **writing discipline** (naming the tradeoff + counter-hypothesis at decision-time). Do NOT claim the accountability loop is closed — 2b closes it; claiming otherwise is the exact over-claim this doctrine exists to prevent.

---

## Out of scope (named follow-on arcs — do NOT fold in)

- **The complaint-time CALLBACK** — surfacing the specific logged entry when the PRINCIPAL later complains about an outcome. **Slice 2b.**
- **The RE-VERIFY GATE** — checking the callback against the record (does the logged entry actually support the callback?), and owning the gap when it doesn't ("I didn't flag this clearly enough"). **Slice 2b** — deliberately deferred until real logged entries exist to design it against.
- **Dose calibration off the user's track record** — **Slice 2b.**
- **The meta-trigger auto-detect-circling counter** — still deferred (Arc 4), to be designed from dogfood data.
- **Graduating `decision-surface` from DRAFT** — its own arc; see `stoa--ida` (the SKILL_NAMES gap).
- **The broader checkpoint rollout** beyond the Arc-70/Arc-71 subset.

---

## Discipline

- Full gauntlet — substrate canon + tooling; not mechanical. Standard POLYBIUS+PLINY (no CHIRON/HAMILTON).
- Capture only — write the record; do NOT build any part of the reader (callback / re-verify gate). A design that reaches into 2b is an automatic route-back regardless of quality.
- Deterministic trigger — the WHEN (a dilemma-decision was taken) is a deterministic predicate on the Arc-70 read; the entry CONTENT is the agent's judgment. No heuristic auto-detection in this slice.
- One coherent slice; keep the diff scoped to the capture half (DC0–DC5). No drive-by refactors.
- bw syntax: positional `bw comment`, no backticks/`$()`; `bw prime` at activation; `--reason` on close.

## Suggested phasing

- **Phase A — design (DAEDALUS).** Resolve DC0–DC5; the entry schema (DC0, forward-constrained by the deferred 2b reader) and the "writing is half the value" device (DC4) are the load-bearing pieces. Surface to the floor-manager for a go/no-go before build.
- **Phase B — build (ADA).** The capture module + composition → the write-trigger + over-write guard → the bw-write mechanics → the corpus + runner.
- **Phase C — verify (ARGUS/VERA/CATO + NOMOS).** A real entry lands in bw live; the over-write guard holds both directions at floor; full close-gate suite; ground-truth.
- **Phase D — ship.** Commit + push; update `stoa--7gl` with the SHA + dispositions.

Standby, run.
