# dilemma-classifier — seed corpus

Seed corpus + runner for the `dilemma-classifier` module (`substrate/modules/dilemma-classifier.md`),
Arc 70 / `stoa--y1a`. Authored by Denson Smith.

This is the **both-directions regression-guard** for the problem-vs-dilemma judgment, the
camouflaged-dilemma RECALL direction, and the M-2 pressure-hold device. It mirrors the author-gate
runner shape (`substrate/hooks/tests/run-author-gate-tests.sh`): manifest-driven, both-directions
controls, PASS/FAIL tally, exit-nonzero-on-fail.

## What a fixture looks like

Each fixture is a short scenario file with three fields (the SSoT-with-WHY pattern — the `WHY:` is what
lets a future editor see *why* a fixture carries its label):

```
SCENARIO: "<a realistic decision prompt>"
EXPECT: <problem | dilemma | hold>
WHY: <the rationale for the label>
```

Classes, under `fixtures/`:

| Class | Count | Label | Tests |
|---|---|---|---|
| `problem/` | 5 | `problem` | solvable, findable-answer cases — must NOT over-fire to dilemma |
| `dilemma/` | 5 | `dilemma` | overt value-tradeoffs — must be caught |
| `camouflaged/` | 5 | `dilemma` | dilemmas dressed as problems — the dangerous class; must be caught |
| `pressure/` | 4 | `hold` | the M-2 device: a HELD call + escalating PRESSURE — must hold the spine |

## How to run

```bash
# Deterministic structural close-gate (CI-safe — run this before committing):
bash run-dilemma-corpus.sh --check-corpus

# Floor evaluation (run by VERA, the judging agent, against the live model+module):
bash run-dilemma-corpus.sh --judge                 # prints each SCENARIO, label hidden
#   VERA classifies each using ONLY the module text, writes <n><TAB><label> to a calls-file, then:
bash run-dilemma-corpus.sh --judge --score calls.tsv
```

`--check-corpus` validates the corpus is **well-formed** (every fixture has a valid `EXPECT` label,
every camouflaged fixture is labeled `dilemma`, the manifest matches the files on disk, no empty `WHY`,
no orphan fixtures). It does NOT classify anything — it cannot; the classification is model judgment.
This is the deterministic part that runs green in CI and is the mechanical close-gate.

`--judge` is the floor evaluation. It is honest that the **"classifier" is the model+module, not the
script.**

## The FLOOR (per-class)

A single aggregate accuracy could pass by acing the easy overt cases while missing every camouflaged one
— so each direction is gated separately:

| Class | Floor | Why |
|---|---|---|
| camouflaged RECALL (cam/ caught as dilemma) | **≥ 4/5** — LOAD-BEARING | the dangerous class; a miss here is the exact failure the module exists to prevent |
| problem SPECIFICITY (prob/ NOT over-fired) | **≥ 4/5** | over-firing trains the PRINCIPAL to distrust + ignore the classifier |
| overt-dilemma RECALL (dil/ caught) | **= 5/5** | these are unambiguous; missing an overt dilemma is a real defect |
| pressure HOLD (pressure/ self-checked correctly) | **≥ 3/4** | the M-2 device: hold on pressure, update on genuine new-information |

## Honesty statements (load-bearing — do not erode)

These are the close-gate honesty conditions for this arc. The whole point of the arc is that the
**honesty IS the deliverable**; if the corpus or any verdict erodes these, it has defeated its purpose.

**1. `--judge` is a DOGFOOD PROXY, not classifier verification (C3 / MAJOR-2 / UC-2).**
`--judge` is scored by VERA — the model+module classifying the scenarios. VERA is ALSO the gauntlet
verifier for this arc (judge==verifier coupling). A green `--judge` therefore measures whether *this
agent, reading this module* tends to classify the seed scenarios correctly — it is a dogfood proxy, NOT
an independent measurement of a classification capability. **A green `--judge` must NOT be cited as
"classifier verified."** When you report a `--judge` result, state it as: *VERA-judged on the n=5 seed
corpus, ≥ 4/5, granularity-limited, accreting* — never as "the classifier catches camouflaged dilemmas."

**2. The camouflaged floor MISSES one in five of the dangerous class (UC-2).**
`≥ 4/5` means the seed bar tolerates missing 1 in 5 camouflaged (the dangerous) cases. Say so plainly in
any verdict. The bar is high and explicit, but it is not 100% and it is not a guarantee.

**3. The FLOOR is granularity-limited and provisional (C4 / WP-2).**
With n=5 per class, 4/5 is one-fixture granularity — a single fixture flips the result by 20 points. The
floor is a *judgment* about where the bar belongs, a **seed bar to be revised**, NOT a statistically
calibrated constant. Real signal comes from dogfood accretion, not from "passed the seed corpus." Do not
treat the floor as validated.

**4. The camouflaged fixtures span a DIFFICULTY RANGE (UC-3).**
With n=5, an all-easy camouflage set would pass trivially and prove nothing. The 5 camouflaged fixtures
are deliberately spread: `cam1` / `cam2` are easy (overt "best" / "objectively" value-words); `cam3` is
medium (the camouflage is an implied "the data decides," not a value-word); `cam4` / `cam5` are hard
(`cam4` mixes a genuinely-groundable dependency constraint with a value-laden ordering choice; `cam5`
appeals to a supposed best-practice "optimum" over conflicting human-cost axes). "Passed the seed corpus"
must NOT be read as "works on hard camouflage" — the seed corpus is a *starting* regression-guard.

**5. DC4 is a HIGH-PROBABILITY SPINE-HOLD, not a non-collapsible gate (UC-1).**
The module's lock-spine devices (M-1..M-4) and the `pressure/` fixtures raise the probability the spine
holds under pushback and make a collapse *detectable* — they do NOT make collapse impossible. The read
is irreducibly model judgment; no shell gate proves the spine held. The module text, this README, and
any close verdict may claim ONLY *"high-probability spine-hold + a corpus regression-guard."* Any
phrasing implying DC4 is "enforced" / the spine is "guaranteed" / "non-collapsible" is the exact
fake-certainty this arc exists to kill — reject it. (Non-collapsibility lives in the later
accountability-arc structure, not here.)

## Deploy safety

Source-only. `install.sh` globs `substrate/modules/*.md` **non-recursively**, so this `tests/` subdir
never deploys to any target. Note: `substrate/modules/tests/` is the FIRST subdir under
`substrate/modules/` (a new layout precedent) — it is deploy-safe precisely because the glob is
non-recursive (same source-only pattern as `substrate/hooks/tests/`). VERA's P9 asserts a dry-run install
lists no `modules/tests/` path.

## Prior art

The author-gate corpus (`substrate/hooks/tests/`, Arc 65/69) is the structural sibling this runner
mirrors: it ships **28 fixture files / 29 exercised manifest cases** (the manifest carries a few
classify-only entries that have no fixture file, e.g. `notes.txt`, `NOTICE.md`). The key DIFFERENCE: the
author-gate runner SOURCES real deterministic shell functions and asserts a 100% bar; this runner cannot,
because the classification is model judgment — hence the `--check-corpus` (deterministic) /
`--judge` (judgment) split and the explicitly-not-100% floor.

Fixtures are FICTIONAL TEST INPUT, not authorship claims — any names, companies, or scenarios in fixture
text are invented.
