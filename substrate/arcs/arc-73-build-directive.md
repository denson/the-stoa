# Arc 73 build directive — Decision-register READER: complaint-callback + re-verify gate (self-correction doctrine, slice 2b)

**Audience:** the fresh Claude Code sessions opened to build Arc 73 (PLINY_the-stoa + the floor-manager POLYBIUS_the-stoa).
**Authored by:** Polybius_the_Stoa (user-level Stoa agent, sid 990b0750-5572-4836-b9c7-18d626a12e96) on behalf of the PRINCIPAL (Denson Smith).
**Status:** DRAFT — pending PRINCIPAL review, then NOMOS-on-the-directive, then committed + launched.
**Builds on:** current the-stoa main (Arc 70 dilemma-classifier + Arc 71 decision-register + Arc 72 decision-surface all shipped + deployed). Project-tier charter: **`stoa--51k`**.
**Design input (READ IT FIRST):** `docs/self-correction-doctrine-DRAFT.md` — §6 (the accountability moves / the longitudinal loop) + the **Resolved** section (the re-verify gate). And `substrate/modules/decision-register.md` (the Arc-71 RECORD this reads — esp. §2 the 9-field schema).

**You are MAJOR_PLINY for the Arc 73 engagement.** Read `substrate/MAJOR_PLINY.md` and assume the orchestrator role. Open Claude Code in `C:\Users\denso\claude_projects\the-stoa\`.

**Your one job:** build the **reader** half of the black box — the complaint-time callback + the **re-verify gate** that completes the longitudinal loop. When the PRINCIPAL complains about an outcome, pull the *specific* logged decision-register entry and ask the one question the gate reduces to: **does the logged entry support the callback?** If yes → surface it honestly (forward-accountability). If no / no entry → the callback does NOT fire and the agent **owns the gap** ("I didn't flag this clearly enough"). **Reading + re-verifying only.** **Not** the per-user dose model (neutral-default v1 only; calibration accretes), **not** the consumer variant, **not** slice 4.

**The load-bearing property:** the gate is anti-gaslighting in **both** directions — it catches the user's hindsight self-serving edit ("you never warned me" when the record shows they were warned) AND the agent's false "I told you so" (the record does NOT support the callback → own the gap, never fake the warning). "I fucked up first" is honest and a **door, not a blanket** — own only what is genuinely the agent's; absorbing *false* blame hands the user the scapegoat they want (collusion). Success is not the user "growing up" today; **success is that the agent didn't lie.**

**Full gauntlet** (DAEDALUS → ARGUS → ADA → VERA → CATO → NOMOS). **Standard POLYBIUS+PLINY team** — substrate-component design (a new module + a corpus), not a custom agent/workflow, so **no CHIRON/HAMILTON**.

---

## Comms — async with Polybius_the_Stoa via bw (`stoa--*`)

Coordinate on the charter **`stoa--51k`**. Polybius_the_Stoa (user-level owner) monitors + interjects; the floor-manager runs independent verification at each hand-back and relays up. The PRINCIPAL is NOT the relay — beadwork is. Asymmetric polling: don't poll while working; do poll when waiting. `bw comment <id> "text"` is **positional, no `-m`**; **no backticks or `$()` in comment bodies**. Run `bw prime` at activation. Every seat signs `[from: <NAME> | sid <session-id>]` (sid via the `whoami` skill).

---

## Read first

1. **The doctrine** `docs/self-correction-doctrine-DRAFT.md` — §6 (the longitudinal loop: surface accurately at complaint-time ONLY when the record is right AND the complaint genuinely is the warned tradeoff biting — re-verify, or it's gaslighting; "I fucked up first" honest + door-not-blanket; forward-accountability not past-blame) + the **Resolved** section (the re-verify gate reduces to "does the logged entry support the callback?"; if not, callback not fired, agent owns the gap) + §8 (why the AI is fit: no ego to feed → it can do clean accountability, guilt-lane not shame-lane).
2. **The charter `stoa--51k`** (the locked scope + DoD).
3. **What this reads (Arc 71, shipped):** `substrate/modules/decision-register.md` — esp. §2 the 9-field schema. `WARNING` + `COUNTER-HYPOTHESIS` are what the gate checks; `DR-ID` is the pull-address; the register lives as a comment stream on one standing `decision-register`-labeled bw ticket.
4. **The sibling modules + their patterns:** `substrate/modules/dilemma-classifier.md` (§4 diagnostic tree to reuse for delivery; §2 self-check pattern; the trigger + over-fire-guard shape) and the Arc-70/71/72 corpus runners under `substrate/modules/tests/` (the both-directions fixture + `--check-corpus`/`--judge` pattern to mirror).

---

## The build target (slice 2b — read + re-verify only)

1. **A complaint-callback + re-verify-gate module** — the reader. Trigger (a complaint about a past decided call) → lookup (pull the specific register entry) → the re-verify gate (does the entry support the callback?) → one of two honest outcomes (surface / own-the-gap) → delivery (forward-accountability, guilt-lane).
2. **A both-directions seed corpus** of entry+complaint fixture PAIRS — callback-SHOULD-fire vs callback-must-NOT-fire (own-the-gap), with the anti-gaslighting controls running BOTH ways.
3. **The loop wiring** — it reads the Arc-71 decision-register (no write-back); the gate keys on the logged `WARNING` + `COUNTER-HYPOTHESIS`.

---

## Design items — DAEDALUS resolves in Phase A (surface at the design hand-back)

- **DC0 — the complaint trigger + over-fire guard.** When does the reader fire? An explicit call ("why didn't you warn me" + a closed synonym set) + a judgment checkpoint for the PRINCIPAL expressing regret/blame about a past *decided* call. The over-fire guard (the Arc-70/71 analog): do NOT fire on every mention of a past decision, on a fresh complaint with no logged decision, or on a general gripe. Corpus-testable.
- **DC1 — the entry lookup.** How the SPECIFIC logged entry is pulled from the register (by `DR-ID`, `CONTEXT-LINK`, or content match against the standing register ticket). Reads only — NO write-back to the register. Resolve the ambiguity case honestly (multiple candidate entries, or none).
- **DC2 — the re-verify gate (LOAD-BEARING).** The record-vs-callback check: *does the logged entry support the callback?* Specify the two outcomes — (a) SUPPORTED → surface honestly; (b) NOT-SUPPORTED / no-entry → callback NOT fired, agent owns the gap. Make it anti-gaslighting BOTH ways (catches the user's hindsight edit AND the agent's false callback). The "door not a blanket" rule: own only what is genuinely the agent's; do NOT absorb false blame. This is the crisp, buildable core (a record-vs-claim check, NOMOS-shaped) + the honest judgment layer.
- **DC3 — the delivery (forward-accountability, guilt-lane).** Reuse the classifier §4 diagnostic tree to read where the PRINCIPAL sits before responding. "I fucked up first" honest; forward to the fix, not past-blame; egoless (no "I told you so" — that is the giver's-dopamine failure, §8). Plain, protective. When the callback IS supported, the move is "you chose the tradeoff; here's how it played out; what now," NOT gloating.
- **DC4 — dose calibration: neutral-default v1 only (scope-guard).** Ship a single neutral default posture. The per-user-track-record tuning is NAMED as accreting and is OUT — we have NO track record yet, and the doctrine says calibrate off the *real* track record, NOT a stereotype, so a dose model invented now would VIOLATE the doctrine. Resolve only "what the neutral default does"; defer the calibration explicitly.
- **DC5 — the verification corpus + honest stance.** Entry+complaint fixture PAIRS; both-directions (callback-fires-honestly vs callback-owns-the-gap); a stated FLOOR (not 100%); `--check-corpus` deterministic / `--judge` judgment split (mirror Arc-70/71/72). **Honest stance (LOCKED):** the record-vs-callback gate is crisp and buildable from fixtures, BUT the "genuinely biting" read and the dose accrete from real use — the loop closes STRUCTURALLY (the record exists and the gate checks it), the JUDGMENT accretes. Claim ONLY "high-probability + regression-guard + the record didn't lie," never a guarantee. Same posture Arc 70/71/72 shipped.

---

## Deliverables (land together)

1. The complaint-callback + re-verify-gate module (DC0–DC4) + its composition into the target role files (`gen-data` re-run).
2. The both-directions entry+complaint corpus + runner (DC5).
3. Charter `stoa--51k` updated with the landing SHA + per-DC disposition; no stale refs.

---

## Verification / Definition of done

- **Mechanical (close-gate):** the module composes into the target role files (grep/diff proves it); the callback **fires on a complaint about a logged decision and the re-verify gate runs** — EXERCISED live, with BOTH outcomes demonstrated (a supported callback surfaces honestly; an unsupported one owns the gap); the over-fire guard holds; the **both-directions corpus passes at the DC5 floor**; the **FULL close-gate suite green INCLUDING ALL THREE existing corpora** (dilemma 19/19 + decision-register 18/18 + decision-surface 19/19 — regression, the reader touches the loop), plus `gen-data` deterministic, `vitest`, author-gate, stop-hook; **NOMOS CONFORMANT**; `Author=PRINCIPAL` + the §28.9 seat trailer.
- **Judgment (honest stance):** the gate's record-vs-callback check is crisp; the "genuinely biting" + dose judgment **accretes** from real use; do NOT fake a dose model from a stereotype; the loop closes structurally, the calibration accretes. Do NOT over-claim (that would be the exact fake-certainty this doctrine kills). Success = the agent did not lie.

---

## Out of scope (named follow-on arcs — do NOT fold in)

- **Per-user dose calibration off the track record** — beyond the neutral-default v1. Accretes from real history; faking it from a stereotype now would violate the doctrine. (The honest deferral.)
- **The consumer-tier variant** — its own artifact.
- **The meta-trigger auto-detect-circling counter** — slice 4.
- **The broader checkpoint rollout** — slice 4.
- **Any write-back / mutation of the decision-register** — the reader reads; it does not edit the record (the record's integrity is the whole point).

---

## Discipline

- Full gauntlet — substrate canon + a new module that reads a shipped module; not mechanical. Standard POLYBIUS+PLINY (no CHIRON/HAMILTON).
- Read-only on the register: the reader pulls + re-verifies; it NEVER writes back or mutates a logged entry. A design that mutates the record is an automatic route-back.
- The honest core: the gate checks the RECORD, not memory. "Own the gap" is a first-class outcome, not a fallback. Anti-gaslighting runs BOTH ways. A design that only catches the user (not the agent's own false callback) is incomplete.
- One coherent slice; keep the diff scoped to the reader (DC0–DC5). Touch the Arc-71 register ONLY as a reader.
- bw syntax: positional `bw comment`, no backticks/`$()`; `bw prime` at activation; `--reason` on close.

## Suggested phasing

- **Phase A — design (DAEDALUS).** Resolve DC0–DC5; the re-verify gate (DC2, both-directions anti-gaslighting) + the own-the-gap honesty are the load-bearing pieces. Surface to the floor-manager for go/no-go before build.
- **Phase B — build (ADA).** The module (trigger + lookup + gate + delivery) → the both-directions corpus + runner.
- **Phase C — verify (ARGUS/VERA/CATO + NOMOS).** Both gate outcomes demonstrated live; over-fire guard holds; read-only-on-register proven; full suite incl ALL THREE existing corpora; ground-truth.
- **Phase D — ship.** Commit + push; update `stoa--51k` with the SHA + dispositions. This COMPLETES the doctrine core (slices 1+2a+2b+3).

Standby, run.
