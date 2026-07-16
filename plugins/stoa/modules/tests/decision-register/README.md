# decision-register — seed corpus

Seed corpus + runner for the `decision-register` module (`substrate/modules/decision-register.md`),
Arc 71 / `stoa--7gl`. Authored by Denson Smith.

This is the **both-directions regression-guard** for the CAPTURE half of the self-correction black box:
the write-trigger predicate + over-write guard (write on a decided dilemma; withhold on a problem, an
illuminated-but-undecided dilemma, or an incidental mention) AND the DC4 vacuity detector (a hollow
counter-hypothesis is detectably hollow). It mirrors the Arc-70 `run-dilemma-corpus.sh` shape:
manifest-driven, both-directions controls, PASS/FAIL tally, exit-nonzero-on-fail.

## What a fixture looks like

Each fixture is a short scenario file with three top fields (the SSoT-with-WHY pattern — the `WHY:` is
what lets a future editor see *why* a fixture carries its label):

```
SCENARIO: "<the decision context: checkpoint + classifier outcome + what the PRINCIPAL did>"
EXPECT: <write | no-write | write-but-hollow>
WHY: <the rationale for the label>
```

`write` and `write-but-hollow` fixtures additionally carry an `ENTRY:` block — a reference entry with all
nine schema fields as `LABEL: value` lines, so `--check-corpus` can validate the schema + the vacuity check
deterministically on a real exemplar:

```
ENTRY:
DR-ID: …
WHEN: …
CHECKPOINT: …
DILEMMA: …
WARNING: …
OPTIONS: <opt-1> ~ <opt-2> ~ <opt-3>
CHOSEN: …
COUNTER-HYPOTHESIS: …
CONTEXT-LINK: …
```

Classes, under `fixtures/`:

| Class | Count | Label | Tests |
|---|---|---|---|
| `decided/` | 5 | `write` | classifier returned DILEMMA + a path was taken → a well-formed entry must be written |
| `problem/` | 3 | `no-write` | classifier returned PROBLEM (solved) → NO entry (over-write guard, direction 1) |
| `illuminated/` | 4 | `no-write` | DILEMMA illuminated but NOT decided → NO entry (the LOAD-BEARING over-write guard) |
| `incidental/` | 3 | `no-write` | the words appear but no checkpoint / no live decision → NO entry (over-fire guard) |
| `hollow/` | 3 | `write-but-hollow` | a decided dilemma whose entry has an empty/vacuous counter-hypothesis → `--check-corpus` must FLAG it hollow (the DC4 detector negative control) |

## How to run

```bash
# Deterministic structural close-gate (CI-safe — run this before committing):
bash run-decision-register-corpus.sh --check-corpus

# Floor evaluation (run by VERA, the judging agent, against the live model+module):
bash run-decision-register-corpus.sh --judge                 # prints each SCENARIO, label hidden
#   VERA decides write/no-write for each using ONLY the module text, writes <n><TAB><label>, then:
bash run-decision-register-corpus.sh --judge --score calls.tsv
```

`--check-corpus` validates the corpus is **well-formed**: labels valid, each class dir carries its label,
the manifest matches the files on disk (no orphans), no empty `WHY`/`SCENARIO`, every `write`/
`write-but-hollow` fixture's `ENTRY:` block has all nine fields populated (counter-hypothesis excepted) and
OPTIONS splits on ` ~ ` to ≥ 3 options, every `write` fixture's counter-hypothesis is **non-hollow**, and
every `hollow/` fixture's counter-hypothesis **IS** empty-or-on-the-vacuity-denylist (the DC4 detector
negative control — proving the detector catches what it should). It does NOT decide whether a scenario
should-write — it cannot; that is model judgment.

`--judge` is the floor evaluation. It is honest that the **"classifier" is the model+module, not the
script.** `hollow/` is a `--check-corpus` negative control (a should-write that happens to be hollow), not a
`--judge` class, so it is excluded from the judge scoring.

## The FLOOR (per-class)

A single aggregate accuracy could pass by acing the easy class while missing the dangerous over-write
direction — so each direction is gated separately:

| Class | Floor | Why |
|---|---|---|
| decided RECALL (decided/ → write) | **≥ 4/5** | the capture must fire on real decisions; missing them empties the black box |
| illuminated SPECIFICITY (illuminated/ → no-write) | **≥ 3/4** — LOAD-BEARING | the dangerous over-write direction; logging an undecided tradeoff pollutes the 2b-read journal and lets a non-decision masquerade as a warned decision |
| problem SPECIFICITY (problem/ → no-write) | **≥ 2/3** | over-firing on every problem trains the PRINCIPAL to distrust the register |
| incidental SPECIFICITY (incidental/ → no-write) | **≥ 2/3** | same over-fire-corrosion logic as the Arc-70 §3.6(a) guard |

A miss in ANY class exits nonzero.

## Honesty statements (load-bearing — do not erode)

These are the close-gate honesty conditions for this arc. The whole point of the arc is that the
**honesty IS the deliverable**; if the corpus or any verdict erodes these, it has defeated its purpose.

**1. `--judge` is a DOGFOOD PROXY, not capture verification (judge==verifier coupling).**
`--judge` is scored by VERA — the model+module deciding write/no-write on the scenarios. VERA is ALSO the
gauntlet verifier for this arc. A green `--judge` therefore measures whether *this agent, reading this
module* tends to fire/withhold correctly on the seed corpus — it is a dogfood proxy, NOT an independent
measurement of a capture capability. **A green `--judge` must NOT be cited as "the capture trigger is
verified."** Report it as: *VERA-judged on the n=15 seed corpus (decided + the three no-write classes),
per-class floors met, granularity-limited, accreting* — never as "the register fires correctly."

**2. The floors tolerate misses + are granularity-limited.**
n=3–5 per class; one fixture flips a class by a large margin. The floor is a *seed judgment* about where
the bar belongs, revised from dogfood accretion — NOT a calibrated constant. Do not treat "passed the seed
corpus" as validated.

**3. "A path was chosen" is model judgment, not a shell check (A1).**
`--check-corpus` validates corpus well-formedness; it does NOT and CANNOT decide whether a scenario warrants
a write. Whether condition (3) of the predicate — a path was actually chosen — holds is the model's read,
scored only as a `--judge` floor. The deterministic part is the trigger moment + the DILEMMA precondition.

**4. DC4 is a high-probability writing-discipline + a corpus regression-guard, not a non-collapsible gate
(A3).** The vacuity denylist catches the canonical hollow patterns ("we'll see", "time will tell", etc.) in
the corpus; it does NOT make a live weak-but-non-vacuous counter-hypothesis ("the metrics will be bad")
impossible. The denylist is a *seed* list that accretes from real hollow entries, not a closed proof of
vacuity. The module text, this README, and any close verdict may claim ONLY *"high-probability
writing-discipline + a corpus regression-guard against the canonical hollow patterns."* Any phrasing that
DC4 is "enforced" / the counter-hypothesis is "guaranteed concrete" / "non-collapsible" is the exact
fake-certainty this arc exists to kill — reject it. (Non-collapsibility lives in the deferred 2b re-verify
structure, not here.)

## Deploy safety

Source-only. `install.sh` globs `substrate/modules/*.md` **non-recursively**, so this `tests/` subdir never
deploys to any target (the same source-only pattern as `substrate/modules/tests/dilemma-classifier/` and
`substrate/hooks/tests/`). VERA's P8 asserts a dry-run install lists no `modules/tests/decision-register/`
path.

## Prior art

The Arc-70 `dilemma-classifier` corpus (`substrate/modules/tests/dilemma-classifier/`) is the structural
sibling this runner mirrors directly: the same `field()` leading-`LABEL:` parse, the same
`--check-corpus` (deterministic) / `--judge` (judgment) split, the same explicitly-not-100% per-class
floors. The DIFFERENCE: this corpus adds the `ENTRY:`-block schema validation (nine populated fields, ≥ 3
` ~ `-delimited OPTIONS) and the `hollow/` negative control for the DC4 vacuity detector.

Fixtures are FICTIONAL TEST INPUT, not authorship claims — any names, companies, or scenarios in fixture
text are invented.
