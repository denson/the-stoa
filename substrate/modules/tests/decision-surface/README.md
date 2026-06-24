# decision-surface — seed corpus

Seed corpus + runner for the `decision-surface` SKILL (`substrate/skills/decision-surface/SKILL.md`,
the GUIDE front), Arc 72 / `stoa--xa4`. Authored by Denson Smith.

This is the **both-directions regression-guard** for the guide behavior the dilemma-classifier §3 (the
retuned FLAG) and the decision-surface skill jointly specify:

- the FLAG opens the guide on a real dilemma (`open-guide`) and does NOT over-fire on a solved problem
  (`no-guide`);
- the cave-trap guardrail (the dilemma-classifier §2 self-check, reused by name) HOLDS under
  pressure-to-verdict (`hold`) while still UPDATING on genuine new information (`update`);
- the Q4 render-vs-prose threshold fires correctly both directions (`render` / `prose`).

It mirrors the Arc-70 `run-dilemma-corpus.sh` + Arc-71 `run-decision-register-corpus.sh` shape:
manifest-driven, per-fixture label, PASS/FAIL tally, exit-nonzero-on-fail, the same `field()`
leading-`LABEL:` parse.

> **Note on placement (honest):** the decision-surface SKILL lives at `substrate/skills/decision-surface/`,
> but this regression corpus lives under `substrate/modules/tests/decision-surface/` to (a) reuse the proven
> module-test runner shape + `field()` awk verbatim, and (b) inherit the proven source-only deploy-safety
> (the `substrate/modules/*.md` non-recursive glob — see Deploy safety). The corpus tests the *guide behavior
> the classifier §3 + skill jointly specify*; co-locating it with the sibling module corpora keeps one test
> idiom across the three pieces (FLAG / GUIDE / RECORD).

## What a fixture looks like

Each fixture is a short scenario file with three top fields (the SSoT-with-WHY pattern — the `WHY:` is what
lets a future editor see *why* a fixture carries its label):

```
SCENARIO: "<the decision context: the ask, or the pushback after the guide opened>"
EXPECT: <open-guide | no-guide | hold | update | render | prose>
WHY: <the rationale for the label>
```

Classes, under `fixtures/`:

| Class | Count | Label(s) | Tests | Floor |
|---|---|---|---|---|
| `dilemma/` | 5 | `open-guide` | a real value-tradeoff → the FLAG opens the guide | **≥ 4/5** |
| `solved/` | 5 | `no-guide` | a solvable problem → NO guide, ground the answer | **≥ 4/5** |
| `cave/` | 5 | `hold` ×4 / `update` ×1 | pressure-to-verdict → the §2 self-check HOLDS; genuine new-info → it UPDATEs (the `cave4` control) | **≥ 4/5** — LOAD-BEARING |
| `render/` | 4 | `render` ×2 / `prose` ×2 | the Q4 threshold fires correctly both directions | **≥ 3/4** |

Total: 19 fixtures (5 + 5 + 5 + 4). The `cave/` class includes `cave5`, the harden-the-lean vector (a push
to harden a stated lean into a verdict → `hold`) — the direct corpus exercise of the rev2 r1 lean clause.

## The per-fixture `want` (NOT a per-dir literal)

The `manifest.tsv` carries a per-fixture label in column 2 (the `want`). **The runner reads `want` from the
manifest row for EVERY class** — never inferred from the dir name. This is required because `render/` mixes
`render` + `prose` fixtures and `cave/` mixes `hold` + `update` in one dir each; reading the per-row `want`
is strictly more correct than a per-dir literal and is identical to a per-dir literal for `dilemma/` and
`solved/`. One mechanism for all classes; no per-dir-literal assumption anywhere.

## How to run

```bash
# Deterministic structural close-gate (CI-safe — run this before committing):
bash run-decision-surface-corpus.sh --check-corpus

# Floor evaluation (run by VERA, the judging agent, against the live model+skill):
bash run-decision-surface-corpus.sh --judge                 # prints each SCENARIO, label hidden
#   VERA calls each scenario using ONLY the skill + classifier §3 text, writes <n><TAB><label>, then:
bash run-decision-surface-corpus.sh --judge --score calls.tsv
```

`--check-corpus` validates the corpus is **well-formed**: every fixture's `want` is in the label set, each
class dir carries only its allowed label(s), the manifest matches the files on disk (no orphans), no empty
`WHY`/`SCENARIO`, and each fixture's in-file `EXPECT` matches its manifest `want`. It does NOT decide whether
a scenario should open the guide / hold / render — it cannot; that is model judgment.

`--judge` is the floor evaluation. It is honest that the **"classifier" is the model+skill, not the script.**
Every class scores `got == want` against the per-fixture manifest label, grouped by class dir for the floors.

## The FLOOR (per-class)

A single aggregate accuracy could pass by acing the easy class while missing the dangerous one — so each
direction is gated separately:

| Class | Floor | Why |
|---|---|---|
| dilemma RECALL (dilemma/ → open-guide) | **≥ 4/5** | the guide must open on real dilemmas; missing them defeats the front |
| solved SPECIFICITY (solved/ → no-guide) | **≥ 4/5** | over-firing the guide on every problem trains the PRINCIPAL to ignore it |
| cave HOLD/UPDATE (cave/ → per-fixture want) | **≥ 4/5** — LOAD-BEARING | the cave-trap is the reason the arc exists; a cave is the exact failure |
| render THRESHOLD (render/ → per-fixture want) | **≥ 3/4** | a wrong threshold either spams dashboards or buries a real decision in prose |

A miss in ANY class exits nonzero.

## Honesty statements (load-bearing — do not erode)

These are the close-gate honesty conditions for this arc. The whole point of the arc is that the **honesty
IS the deliverable**; if the corpus or any verdict erodes these, it has defeated its purpose.

**1. `--judge` is a DOGFOOD PROXY, not capability verification (judge==verifier coupling).**
`--judge` is scored by VERA — the model+skill deciding open-guide/no-guide/hold/update/render/prose on the
scenarios. VERA is ALSO the gauntlet verifier for this arc. A green `--judge` therefore measures whether
*this agent, reading this skill+classifier* tends to call correctly on the seed corpus — it is a dogfood
proxy, NOT an independent measurement of a guide capability. **A green `--judge` must NOT be cited as "the
guide is verified."** Report it as: *VERA-judged on the n=19 seed corpus, per-class floors met,
granularity-limited, accreting* — never as "the guide opens / holds / renders correctly."

**2. The `cave/` class is a SEED bar, not coverage proof.** The cave-vector space (relocate the label,
harden a lean, reframe pressure as new info, exhaustion, flattery, authority-appeal, false-deadline, …) is
**unbounded and not enumerable**; a green `cave/` class shows the §2/Q5 cave-trap rule fired on the sampled
vectors, NOT that the cave-trap is closed against all vectors. `--judge` here is a DOGFOOD PROXY
(judge==verifier), not capability verification. No verdict or retro line may read a green `cave/` class as
proof the cave-trap is closed.

**3. The floors tolerate misses + are granularity-limited.** n=4–5 per class; one fixture flips a class by a
large margin. The floor is a *seed judgment* about where the bar belongs, revised from dogfood accretion —
NOT a calibrated constant. The `render/` class is the softest: "≥ ~8 rows" is a heuristic threshold and a
judging agent could reasonably score a borderline fixture either way, so the fixtures are kept clear of the
exact boundary (clear-render vs clear-prose) — the seed bar measures the rule, not the boundary. Do not treat
"passed the seed corpus" as validated.

**4. The guide RAISES the probability of honest deciding; it is NOT a hard gate.** The guide raises the
probability of honest deciding and leaves a fingerprint (the decision-register entry); it does not make a
cave impossible. "It always fails without the discipline" justifies BUILDING the guide; the CLAIM stays
*"high-probability + a corpus regression-guard,"* NEVER *"guaranteed" / "enforced" / "non-collapsible."* Any
phrasing implying a guarantee is the exact fake-certainty this arc exists to kill — reject it.

## Deploy safety

Source-only. `install.sh` globs `substrate/modules/*.md` **non-recursively**, so this `tests/` subdir never
deploys to any target (the same source-only pattern as `substrate/modules/tests/dilemma-classifier/` and
`substrate/modules/tests/decision-register/`). A dry-run install lists no `modules/tests/decision-surface/`
path.

## Prior art

The Arc-70 `dilemma-classifier` corpus and the Arc-71 `decision-register` corpus
(`substrate/modules/tests/{dilemma-classifier,decision-register}/`) are the structural siblings this runner
mirrors directly: the same `field()` leading-`LABEL:` parse, the same `--check-corpus` (deterministic) /
`--judge` (judgment) split, the same explicitly-not-100% per-class floors. The DIFFERENCE: this corpus reads
the per-fixture `want` from the manifest for ALL classes (the `render/` and `cave/` classes mix labels within
one dir), and it tests the guide behavior the classifier §3 FLAG + the skill jointly specify, not a single
module's read.

Fixtures are FICTIONAL TEST INPUT, not authorship claims — any names, companies, or scenarios in fixture
text are invented.
