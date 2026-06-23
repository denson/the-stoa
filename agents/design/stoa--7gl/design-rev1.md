# design-rev1 — Decision-register CAPTURE (self-correction doctrine slice 2a, the black box capture half)

> Arc 71 / charter `stoa--7gl`. Author of repo: Denson Smith.
> Design seat: CAPTAIN_DAEDALUS_the_stoa (subagent). Operating mode: autonomous.
> Design input: `docs/self-correction-doctrine-DRAFT.md` (§5 black-box countermeasure, §6 longitudinal loop, **Resolved**).
> Builds directly on Arc 70 / `stoa--y1a`: `substrate/modules/dilemma-classifier.md` + its checkpoint wiring
> (`MAJOR_POLYBIUS.md` §3.6 a/b/c, `MAJOR_PLINY.md` §5.18) + its corpus/runner (`substrate/modules/tests/dilemma-classifier/`)
> + the `save-verdict.md` bash-write precedent + the `install.sh` two-owner MODULE-INLINE recompose.

---

## §0. Problem restatement (the §6.1 pre-work gate)

Arc 70 shipped the **READ**: a deterministic-trigger + model-judgment classifier that, at fixed checkpoints
(POLYBIUS spin-up / prioritization / explicit-call; PLINY directive-lock), decides whether the decision in
front of the agent is a solvable PROBLEM or a value-TRADEOFF (DILEMMA), and — for a dilemma — illuminates
the tradeoff and hands the call back.

This arc builds the **CAPTURE half of the black box**: at those same Arc-70 checkpoints, *once the classifier
has returned DILEMMA **and a path has actually been chosen***, write **one structured, transparent,
user-readable decision-register entry to bw** recording the dilemma, the warning(s)/tradeoff, the option
chosen, and a concrete counter-hypothesis (what would later prove the choice wrong), with a timestamp and a
context link. Plus the over-write guard (it fires ONLY on a *decided* dilemma, never on a problem, an
illuminated-but-undecided tradeoff, or an incidental mention) and a both-directions verification corpus.

**The doctrine's two load-bearing claims this capture serves:**
1. *"The act of writing it is half the value"* — writing the entry forces the agent to name the tradeoff and a
   falsifiable counter-hypothesis at decision-time, before hindsight can edit them. (DC4.)
2. *Structured ex-ante entry, NOT a raw recording; transparent + user-readable by default.* The schema must be
   **re-readable by the deferred 2b callback** (which is NOT built here) — that is DC0's load-bearing
   forward-constraint.

**Imported assumptions (named per §6.1 — a restatement that hides these has smoothed them):**
- **A1.** "A path was chosen" is, like the Arc-70 read itself, irreducibly model judgment, not a pure shell
  check. The deterministic part is the *trigger moment + the precondition* (classifier already returned
  DILEMMA at a checkpoint); the "was it actually decided" read is the agent's. I mirror the Arc-70
  `--check-corpus` (deterministic) / `--judge` (judgment) honesty split rather than pretending otherwise.
- **A2.** The register's *rightness accretes from real entries* (directive DoD, doctrine Resolved §2). I design
  minimal-but-sufficient and resist over-engineering the schema now.
- **A3.** The honesty posture is non-negotiable and identical to Arc 70: **template + prose-enforced, NOT a
  hard non-collapsible gate.** I do not write "enforced" / "guaranteed" / "non-collapsible" anywhere a reader
  could take the writing-discipline as mechanically guaranteed.

**Convergence check:** the restatement converges with the brief and the directive; no re-scoping. The one place
the brief is implicitly load-bearing — that "decided" is model judgment — I have surfaced as A1 and carried into
DC1/DC5 honestly rather than designing against the ambiguity.

---

## §1. Approach (the design's shape)

The capture is a **new composable module, `decision-register.md`**, that defines (i) the entry schema (DC0),
(ii) the write-trigger predicate + over-write guard (DC1), (iii) the deterministic bw-write mechanics + the
transparency property (DC3), and (iv) the "writing is half the value" structural device (DC4). It composes —
via the **same two-owner MODULE-INLINE pattern Arc 70 uses for `dilemma-classifier`** — into the two seats that
already host the Arc-70 read (POLYBIUS + PLINY). A both-directions corpus + runner (DC5) ships source-only under
`substrate/modules/tests/decision-register/`, mirroring the Arc-70 corpus shape exactly.

The capture *composes WITH* the Arc-70 read: the read is the precondition (classifier returned DILEMMA at a
checkpoint), the capture is the *appended step* (and a choice was taken → write the entry). No Arc-70 file's
*semantics* change; the only edits to `dilemma-classifier`'s host sections are the addition of a "if decided →
record per `decision-register.md`" pointer at each checkpoint, plus the new marker pair (see DC2 for the exact
composition mechanics and the honest tradeoff on new-module-vs-extension).

There are no named threats in this design — it is process / role-file + tooling hardening with no runtime
attacker and no attack path. **Threat classification (the §6.12 A3 author duty):**
`not threat-ratified (process / role-file + corpus-tooling change — adds a decision-journaling module + a
source-only test corpus; no runtime attacker, no attack path)` per the `operating-disciplines.md` §35.5
self-carve-out. ARGUS confirms this classification at critique; I cannot self-grant the carve-out. No A3
threat→mitigation map and no §6.13 threat-anchored probe apply (the layer verifies named-threat *coverage*,
and there is no named threat to cover here).

---

## §2. DC-by-DC resolution

### DC0 — register home + entry schema (HIGHEST LEVERAGE)

**Home: ONE standing per-project decision-register ticket, entries are its COMMENT STREAM.** Resolved as:

- **A single standing bw ticket per deployment**, titled `Decision register (self-correction black box)`,
  labeled `decision-register`. Each decided dilemma is **one `bw comment` on that ticket**. Discovery is
  deterministic: the writer resolves the register ticket id by `bw list --all` filtered on the
  `decision-register` label (and creates the ticket on first use if absent — see DC3).

**Why a comment-stream on a standing ticket, not the alternatives** (genuine construct tradeoff — costs named):

| Construct | For | Against |
|---|---|---|
| **Comment stream on ONE standing ticket** (chosen) | Single stable address the 2b callback opens once and scans; timestamps are free (`bw comment` records them); naturally append-only/chronological → a decision JOURNAL; cheap to write (one `bw comment`); inherently transparent (it is a normal readable ticket). | A very long stream is coarse to query by topic (mitigated: each entry is self-describing + the context-link; topic indexing is a 2b reader concern, not a capture concern). |
| One ticket PER decision (`--parent` register ticket) | Per-decision dependency/label/close lifecycle; finer-grained 2b lookup. | Heavier write (a `bw create` per dilemma); ticket-sprawl pollutes `bw list`/`ready`/`blocked`; lifecycle states (open/closed) are meaningless for a journal entry; over-engineered for slice 2a (violates A2). |
| A flat file (`docs/…/register.md`) | Trivially greppable. | Loses the bw transparency/timestamp/team-visible property the doctrine names as the whole point ("that store is bw"); a flat file is the *weak* black box the doctrine explicitly contrasts against. |

The comment-stream choice is the minimal-sufficient one that keeps the doctrine's named property (bw =
structured, queryable, timestamped, transparent) without ticket-sprawl. The schema's rightness accretes from
real entries (A2); if topic-query pressure ever appears, promoting to per-decision child tickets is a forward
move 2b can make against real data — not a slice-2a guess.

**The entry schema (the load-bearing forward-constraint: re-readable by the deferred 2b callback).** Each entry
is a single `bw comment` body with a **fixed, line-anchored, machine-parseable field set** — a fenced labeled
block, NOT free prose. The field labels are the parse anchors a future 2b reader keys on (exactly how the
Arc-70 corpus runner's `field()` awk helper extracts `SCENARIO:`/`EXPECT:`/`WHY:` by leading-label match):

```
DECISION-REGISTER ENTRY
DR-ID: <YYYY-MM-DDTHH-MM-SSZ>-<short-slug>
WHEN: <UTC timestamp, ISO-8601>
CHECKPOINT: <explicit-call | prioritization | team-spin-up | directive-lock>
DILEMMA: <the value-tradeoff in one or two plain sentences — what is being traded against what>
WARNING: <the specific downside the agent flagged about the chosen path — the cost the PRINCIPAL is accepting>
OPTIONS: <the live options with their costs, one per line under this label>
CHOSEN: <the option the PRINCIPAL chose>
COUNTER-HYPOTHESIS: <concrete, falsifiable: the specific later observation that would prove this choice wrong>
CONTEXT-LINK: <the arc/charter/ticket id or directive path this decision sits in>
```

Design notes that make this re-readable by 2b WITHOUT building 2b:
- **Leading-label line anchoring.** Every field is `LABEL: value` at line start (multi-line values for
  `OPTIONS` are indented continuation lines under the label). A 2b reader extracts a field by the same
  leading-`LABEL:` match the Arc-70 `field()` awk uses — this is a *proven* parse, not a novel one. The capture
  module SPECIFIES this contract; it does not build the reader. (This is the line the design-gate bar #2 asks
  for: "the design states HOW a future reader parses … WITHOUT building the reader.")
- **`DR-ID` is the stable per-entry address** the 2b callback will pull a SPECIFIC entry by. It is the
  filename-safe UTC timestamp + short slug (same timestamp convention as `save-verdict.md`'s `<ts>`:
  `YYYY-MM-DDTHH-MM-SSZ`, colons → hyphens).
- **`COUNTER-HYPOTHESIS` is the 2b re-verify-gate's future input** (does the logged warning actually support a
  later complaint?). We capture it now in falsifiable form; the gate that *reads* it is 2b. Naming the field +
  its required shape here is the forward-constraint; reading it is out of scope.
- **Minimal-but-sufficient (A2):** nine fields, all load-bearing, none speculative. No status/severity/category
  taxonomy — those are reader-side concerns that should accrete from real entries, not be guessed now.

### DC1 — write-trigger predicate + over-write guard

**The predicate (deterministic precondition + a judgment read, honest about the split):**

> **WRITE** an entry **iff** all three hold:
> (1) the agent is at an Arc-70 checkpoint (explicit-call / prioritization / team-spin-up / directive-lock) —
>     *deterministic: the checkpoint moment is mechanical, exactly as Arc 70 established;*
> (2) the Arc-70 classifier returned **DILEMMA** (or CAMOUFLAGED-DILEMMA, which resolves to dilemma) on the
>     live decision — *the Arc-70 read; model judgment;*
> (3) **a path was actually chosen** — the PRINCIPAL (or the agent on the PRINCIPAL's behalf within a locked
>     directive) committed to one of the illuminated options — *model judgment (A1).*

The register records **DECISIONS, not detected tradeoffs.** Condition (3) is the over-write guard's heart:
illumination without a choice is NOT a register event.

**The over-write guard (corpus-testable, the Arc-70 over-fire-guard analog) — does NOT fire on:**
- **A problem solved** — classifier returned PROBLEM (condition 2 fails). A grounded answer is not a logged
  tradeoff. *(should-not-write)*
- **A dilemma illuminated but NOT decided** — classifier returned DILEMMA, the tradeoff was laid out, but the
  PRINCIPAL deferred / asked for more / no option was committed (condition 3 fails). The most important guard
  case: the register is a journal of *choices*, and logging an undecided tradeoff would (a) pollute the journal
  the 2b callback reads and (b) let a non-decision masquerade later as a warned decision. *(should-not-write)*
- **An incidental mention** — the words "dilemma" / "tradeoff" appear in conversation but no checkpoint fired and
  no live decision is being classified (condition 1 fails; same shape as the Arc-70 §3.6(a) OVER-FIRE GUARD —
  discussing the doctrine, naming a past classification, quoting the phrase). *(should-not-write)*

**Honest stance (A1):** condition (3) — "a path was actually chosen" — is model judgment, not a shell check.
The deterministic part is the trigger moment + the DILEMMA precondition; the *was-it-decided* read is the
agent's, exactly as "is this a dilemma" is in Arc 70. The corpus (DC5) tests this read as a `--judge` floor,
not a `--check-corpus` mechanical pass. No heuristic auto-detection is introduced (directive Discipline line).

### DC2 — composition home + which seats write

**New module `decision-register.md`, composed two-owner into POLYBIUS + PLINY** (confirmed same homes as
Arc 70). This is a genuine design tradeoff; costs named both directions:

| Option | For | Against |
|---|---|---|
| **New module `decision-register.md`** (chosen) | Clean separation of the READ (Arc-70 classify) from the WRITE (this arc's capture) — the doctrine itself splits "detect" from "log the black box"; the 2b reader will compose against the *register* module, not the *classifier* module, so a clean module boundary now is the seam 2b plugs into; keeps `dilemma-classifier.md` scoped to its one job (the read) rather than swelling it; the new corpus is cleanly its own thing. | A second module + a second marker pair per host file (more composition surface); a reader must follow a pointer from the classifier checkpoint to the register module. |
| Extend `dilemma-classifier.md` | One module, one marker pair, no cross-pointer. | Conflates two jobs (read + write) in one module — the exact one-job-per-thing smell; swells a module whose honesty posture is carefully scoped; couples the 2b reader's future composition to the classifier module; muddies the corpus (read-fixtures + write-fixtures in one runner). |

**The call:** new module. The decisive factor is the **forward seam for 2b** plus one-job-per-module hygiene —
the read and the write are different jobs, the 2b reader composes against the *register*, and conflating them
now buys a marginal composition saving at the cost of a muddier seam exactly where the deferred half plugs in.
This is a value-weighted call, not an obvious one: if you weight "fewest composition markers" highest, the
extension wins. I weight "clean seam for the deferred reader + one job per module" higher, and I am naming that
so ARGUS and the gate can contest the weighting rather than inherit it laundered.

**Which seats write, and where the pointer lands** (no drive-by changes to unrelated composition):
- **POLYBIUS** — at §3.6(b) prioritization and §3.6(c) team-spin-up (the two checkpoints where a dilemma-decision
  is most often *taken*, not just illuminated). §3.6(a) explicit-call also reaches it when the explicit
  classify resolves to a taken decision. Add, at the §3.6 host (adjacent to the existing
  `<!-- MODULE-INLINE:dilemma-classifier -->` pair), a new
  `<!-- MODULE-INLINE:decision-register -->` / `<!-- /MODULE-INLINE:decision-register -->` pair plus a one-line
  pointer: "if the classifier returned DILEMMA AND a path was taken → record per `decision-register.md`."
- **PLINY** — at §5.18 directive-lock: when the locked decision is a dilemma AND the directive commits a path,
  record. Add the second marker pair + pointer adjacent to PLINY's existing `dilemma-classifier` marker.

**install.sh composition mechanics — reuse the Arc-70 two-owner pattern verbatim in shape:**
- `decision-register` becomes the **SECOND two-owner module** (after `dilemma-classifier`). Add `decision-register`
  to BOTH `POLYBIUS_MODULES` (~L1262) and `PLINY_MODULES` (~L1264). Extend the existing TWO-OWNER comment block
  (~L1253–1261) to name `decision-register` alongside `dilemma-classifier` as intentionally non-disjoint
  (same rationale: doctrine multi-seat redundancy; recompose is per-file with that file's own owned-set, so two
  independent marker pairs in two files never collide — runtime-proven by Arc 70).
- The recompose machine (the awk state-machine ~L1145–1206) needs **no change** — it already handles any module
  with a marker pair; Check A (global existence) picks up the new `decision-register.md` source automatically
  from the filesystem glob; Checks B/D are per-file owned-set scoped.
- The `tests/` subdir stays **source-only** — `install.sh` globs `substrate/modules/*.md` non-recursively, so
  `substrate/modules/tests/decision-register/` never deploys (identical to Arc 70's `tests/dilemma-classifier/`;
  VERA's P9-analog asserts a dry-run lists no `modules/tests/decision-register/` path).
- **Byte-alignment discipline (`canonical-template-alignment.md`):** the `decision-register.md` module body is
  inlined into TWO host files at recompose time. The two inlined copies must be byte-identical to the single
  source (the recompose copies the source verbatim, so this holds by construction) — but the **schema block and
  the bw-write template** that appear in the module are a region a build-time `diff` should guard if any copy is
  ever hand-edited. The build adds a P-align-analog `diff` over the schema/template region across the source +
  both recomposed hosts (subproject tier), mirroring the save-verdict P8 `diff`.

### DC3 — bw-write mechanics + transparency

**Mechanics: an inline deterministic template, NOT a helper script — with the bw footguns honored.** Genuine
tradeoff; costs named:

| Option | For | Against |
|---|---|---|
| **Inline template in the module** (chosen) | Resolves at EVERY tier including subproject (the module body recomposes inline; no path-resolution dependency); no second deployable artifact; the write is a single `bw comment` so a helper buys little; the agent fills the fields in context, which IS the DC4 "writing is half the value" device — a helper would risk hiding the field-filling behind a wrapper. | The agent must format the comment body correctly by hand (mitigated: the template is verbatim-copyable + the corpus checks well-formedness). |
| A helper script à la `save-verdict.md` | Deterministic formatting; sha256 round-trip; central footgun-handling. | `save-verdict` exists because it writes a FILE + `bw attach` + integrity round-trip + threat-coverage guard — heavy machinery for a *file* artifact. A register entry is ONE `bw comment` (no file, no attach, no sha256 needed); a helper here is over-engineering (A2) and, worse, would *abstract away the very act of writing the fields* that DC4 needs to stay visible to the agent. |

**The call:** inline template. The decisive factor is DC4 — the writing discipline lives in the agent
*manually naming the tradeoff + counter-hypothesis in the fields*, and a helper that takes those as parameters
would preserve the mechanics while gutting the "act of writing is half the value" property. Plus subproject-tier
resolves the inline body but not a `Read .claude/modules/…` helper path. I weight "keep the field-writing
visible + resolves-at-subproject" over "central formatting"; naming that so it can be contested.

**The bw-write contract (footguns honored — these are LOCKED, from the directive + project memory):**
- `bw comment <register-ticket-id> "<entry body>"` is **POSITIONAL — never `-m`** (memory:
  feedback-validate-bw-syntax; `-m` records the literal string "-m" and drops the message).
- **NO backticks and NO `$()` in the entry body** (memory: feedback-bw-comment-backticks; both are shell command
  substitution even inside double quotes via the Bash tool — they silently mangle/drop the spanned text). The
  schema field values are plain prose; if a decision genuinely involves a code identifier, the template
  instructs writing it WITHOUT backticks (plain text or single-quoted-as-prose).
- **Verify-then-assert (memory: feedback-verify-then-assert):** after the write, the agent re-reads the
  register ticket tail (`bw show <register-ticket-id>`) to confirm the entry landed intact (catches the
  backtick-mangle class). The module states this as a required post-write step.
- **First-use ticket creation:** if no `decision-register`-labeled ticket exists, create it once
  (`bw create "Decision register (self-correction black box)"` then `bw label <id> +decision-register`), then
  comment. The module specifies the lookup-or-create sequence deterministically.

**Transparency (the decision-journal-not-hidden-dossier property — DC3 gate bar #5):**
- The register is a **normal bw ticket** — same store the team already reads; nothing hidden, nothing encrypted,
  no separate dossier. Writing to bw IS the transparency guarantee (the doctrine: "that store is bw … inherently
  transparent to the team").
- **Single-user vs team deployment (honest about both):**
  - *Single-user deployment:* the register is **user-readable by default** — a decision journal on the
    PRINCIPAL's side. The PRINCIPAL can `bw show <register-ticket>` at any time; nothing is gated from them.
  - *Team deployment:* bw is already team-visible, so the register is transparent to the team by construction.
    The honest caveat (named, not smoothed): team-visibility means a register entry is readable by every seat
    with bw access — which is the *intended* transparency, but a deployment that wanted PRINCIPAL-only
    visibility would need a bw-visibility scoping this slice does NOT build (and 2b dose-calibration is where
    per-user track-record reading lands — explicitly out of scope here). For slice 2a the property is
    "transparent by default," and the single-user case is the primary target.

### DC4 — the "writing is half the value" device (LOAD-BEARING)

**The structural device: a `COUNTER-HYPOTHESIS` field that MUST be concrete + falsifiable, with a hollow entry
made OBVIOUSLY hollow — the Arc-70 `WHY:`-field analog, same honesty posture (template + prose-enforced, NOT a
hard gate).**

The Arc-70 corpus uses an SSoT-with-WHY pattern: every fixture carries a `WHY:` that forces the author to name
*why* the label holds, and an empty `WHY` is a `--check-corpus` structural FAIL. I mirror that here at TWO
levels:

1. **In the live entry (the prose-enforced discipline):** the schema's `COUNTER-HYPOTHESIS` field carries an
   explicit in-template instruction (the load-bearing words, in the module): *"State the SPECIFIC, OBSERVABLE
   thing that would later prove this choice was wrong. 'We'll see' / 'it might not work out' / 'time will tell'
   is a HOLLOW counter-hypothesis and defeats the entry — name the concrete signal: a metric crossing a
   threshold, a customer doing X, the cost landing above Y."* Same for `WARNING` (name the specific downside
   being accepted, not "there are risks"). The agent writing the fields IS confronting the tradeoff — that is
   the half-the-value mechanism, and it lives in the act of filling the field, not in a checker.
2. **In the corpus (the regression-guard that makes hollowness DETECTABLE):** the DC5 `--check-corpus`
   deterministic pass FAILs a should-write fixture whose `COUNTER-HYPOTHESIS` or `WARNING` is empty OR matches a
   **vacuity denylist** (case-insensitive substring match against a small list: "we'll see", "time will tell",
   "might not work", "who knows", "hard to say", "could go either way" — and empty/whitespace-only). This is the
   exact Arc-70 "no empty WHY" check, extended to "no vacuous counter-hypothesis." It makes a hollow entry
   *obviously hollow* mechanically in the test corpus.

**Honest stance (A3, LOCKED — directive DC4 + gate bar #4):** this is **template + prose-enforced + a
corpus regression-guard, NOT a hard non-collapsible gate.** A live agent CAN still write a technically-non-empty
but weak counter-hypothesis that slips the denylist; no shell check on a live `bw comment` body proves the
counter-hypothesis is genuinely falsifiable (that read is irreducibly judgment, same as "is this a dilemma").
The device RAISES the probability the writing is real and makes the canonical hollowness patterns DETECTABLE in
the corpus — it does not make a hollow entry impossible. The module text, the README, and any verdict claim
ONLY *"high-probability writing-discipline + a corpus regression-guard against the canonical hollow patterns."*
Any phrasing that DC4 is "enforced" / the counter-hypothesis is "guaranteed concrete" / "non-collapsible" is the
exact fake-certainty this doctrine exists to kill — do not write it. (Non-collapsibility lives in 2b's
re-verify structure, not here.) The vacuity denylist is explicitly a *seed* list that accretes from real
hollow entries (A2), not a closed proof of vacuity.

### DC5 — verification corpus + pass criteria

**Structure: mirror the Arc-70 corpus exactly** — manifest-driven, both-directions, `--check-corpus`
deterministic / `--judge` judgment split, per-class FLOORS (not 100%), exit-nonzero-on-fail, source-only.

Location: `substrate/modules/tests/decision-register/` with `manifest.tsv`, `run-decision-register-corpus.sh`,
`README.md`, `fixtures/`.

**Fixture format (SSoT-with-WHY, extended for the two directions):**

```
SCENARIO: "<the decision context the agent is at — checkpoint + classifier outcome + what the PRINCIPAL did>"
EXPECT: <write | no-write>
WHY: <the rationale for the label>
```

For `EXPECT: write` fixtures, an additional `ENTRY:` block carries a *reference well-formed entry* (all nine
schema fields populated, concrete non-hollow `COUNTER-HYPOTHESIS`) so `--check-corpus` can validate the
schema + the vacuity check deterministically on a real exemplar.

**Classes under `fixtures/`:**

| Class | Count | Label | Tests |
|---|---|---|---|
| `decided/` | 5 | `write` | classifier returned DILEMMA + a path was taken → a well-formed entry must be written |
| `problem/` | 3 | `no-write` | classifier returned PROBLEM (solved) → NO entry (the over-write guard, direction 1) |
| `illuminated/` | 4 | `no-write` | DILEMMA illuminated but NOT decided → NO entry (the LOAD-BEARING over-write guard) |
| `incidental/` | 3 | `no-write` | the words appear but no checkpoint / no live decision → NO entry (over-fire guard) |
| `hollow/` | 3 | `write-but-hollow` | a decided dilemma whose entry has an empty/vacuous counter-hypothesis → `--check-corpus` must FLAG it hollow (the DC4 detectability direction) |

**`--check-corpus` (DETERMINISTIC — the CI-safe close-gate):** validates the corpus is WELL-FORMED only — labels
valid; manifest↔files match (no orphans); every `EXPECT: write` fixture's `ENTRY:` block has all nine schema
fields populated; every `hollow/` fixture's counter-hypothesis IS empty-or-on-the-vacuity-denylist (negative
control for the DC4 detector — proving the detector catches what it should); no empty `WHY`. It does NOT
classify whether a scenario should-write — it cannot; that is model judgment.

**`--judge` (the FLOOR evaluation — run by VERA against the live model+module):** prints each SCENARIO with the
label HIDDEN; the judging agent (VERA), reading ONLY the `decision-register.md` module, decides
`write` / `no-write` for each, emits calls, then `--judge --score <calls>` scores per-class vs the floors.

**FLOORS (per-class; an aggregate could ace the easy class and miss the dangerous one):**

| Class | Floor | Why |
|---|---|---|
| `decided/` RECALL (write when decided) | **≥ 4/5** | the capture must fire on real decisions; missing them empties the black box |
| `illuminated/` SPECIFICITY (NO over-write on undecided) | **≥ 3/4** — LOAD-BEARING | the dangerous over-write direction; logging an undecided tradeoff pollutes the 2b-read journal and lets a non-decision masquerade as a warned decision |
| `problem/` SPECIFICITY (NO over-write on solved) | **≥ 2/3** | over-firing on every problem trains the PRINCIPAL to distrust the register |
| `incidental/` SPECIFICITY (NO over-write on mention) | **≥ 2/3** | same over-fire-corrosion logic as the Arc-70 §3.6(a) guard |

A miss in ANY class exits nonzero.

**Honesty statements (load-bearing — the Arc-70 set, adapted; the honesty IS the deliverable):**
1. **`--judge` is a DOGFOOD PROXY, not capability verification (judge==verifier coupling).** VERA is both the
   judge and the gauntlet verifier; a green `--judge` measures whether *this agent reading this module* tends to
   fire/withhold correctly on the seed corpus — NOT an independent measurement. Report it as *"VERA-judged on the
   n=15 seed corpus, per-class floors met, granularity-limited, accreting"* — never as "the capture trigger is
   verified."
2. **The floors tolerate misses + are granularity-limited.** n=3–5 per class; one fixture flips a class by a
   large margin. The floor is a *seed judgment* about where the bar belongs, revised from dogfood accretion —
   NOT a calibrated constant. Do not treat "passed the seed corpus" as validated.
3. **"A path was chosen" is model judgment, not a shell check (A1).** `--check-corpus` validates corpus
   well-formedness; it does NOT and CANNOT decide whether a scenario warrants a write. That read is the
   model's, scored only as a `--judge` floor.
4. **DC4 is a high-probability writing-discipline + a corpus regression-guard, not a non-collapsible gate
   (A3).** Per DC4 — the denylist catches the canonical hollow patterns in the corpus; it does not make a live
   weak-but-non-vacuous counter-hypothesis impossible. Claim only "high-probability + regression-guard."

**Live close-gate (the build-hand-back bar, restated so the corpus isn't read as the whole gate):** a real
structured entry lands in bw LIVE (exercised, not asserted — `bw comment` to the register ticket, all nine
fields populated, re-read confirms it landed intact); the over-write guard holds both directions at the DC5
floors; full close-gate suite green (`npm run gen-data` deterministic, `vitest`, author-gate tests, stop-hook
tests, + the new `run-decision-register-corpus.sh --check-corpus`); NOMOS CONFORMANT; `Author=PRINCIPAL` + the
§28.9 seat trailer.

---

## §3. Verification probes (what would falsify the design's intended behavior — re-executable by VERA)

> No threat-anchored probe applies: this design carries no named threat (§1 classification:
> `not threat-ratified (process/role-file + corpus-tooling change, no runtime attack path)`). The probes below
> verify capture behavior + composition + honesty, not threat-defeat.

- **P1 — composition lands (both seats).** After build + recompose-dry-run:
  `grep -c "MODULE-INLINE:decision-register" <deployed POLYBIUS>` ≥ 1 AND ≥ 1 in the deployed PLINY; the
  `decision-register.md` source exists under `substrate/modules/`. Falsifies "module composed."
- **P2 — `--check-corpus` deterministic PASS.** `bash substrate/modules/tests/decision-register/run-decision-register-corpus.sh --check-corpus`
  exits 0 with "PASS (well-formed)": all fixtures present, manifest↔files match, every `write` fixture's `ENTRY:`
  has nine populated fields, every `hollow/` fixture's counter-hypothesis is empty-or-on-denylist, no empty WHY.
- **P3 — vacuity detector catches a hollow entry (negative control).** Temporarily add (in a throwaway clone of
  a `write` fixture) a counter-hypothesis of "we'll see" → `--check-corpus` must FAIL it as hollow; restore.
  Falsifies "the DC4 detector actually detects." (Destructive op uses a FIXED literal throwaway path, never a
  `$VAR` expansion, per §3 destructive-op discipline.)
- **P4 — `--judge` floors met (dogfood proxy).** VERA runs `--judge`, classifies the n=15 seed corpus from the
  module text alone, `--judge --score` reports per-class ≥ floor, exit 0. Reported as dogfood proxy per honesty
  statement 1 — NOT as "trigger verified."
- **P5 — live entry lands intact + transparent.** Exercise the write: at a real (or fixture-simulated)
  decided-dilemma, run the module's `bw comment` to the register ticket with all nine fields, then
  `bw show <register-ticket-id>` and confirm every field is present and unmangled (the backtick/`$()`
  verify-then-assert step). Falsifies "the write mechanics produce a parseable entry."
- **P6 — over-write guard holds live (both directions).** Drive an `illuminated/` (undecided) scenario and a
  `problem/` scenario through the module's predicate → NO `bw comment` is emitted to the register. Falsifies "the
  guard prevents over-write."
- **P7 — schema is 2b-re-readable (forward-constraint).** Run the Arc-70 `field()`-style leading-`LABEL:` awk
  extractor against a real landed entry for each of the nine fields → each returns its value. Proves the schema
  is machine-parseable by the proven parse the 2b callback will use (without building 2b).
- **P8 — source-only (no deploy leak).** A dry-run install lists NO `modules/tests/decision-register/` path
  (the non-recursive `modules/*.md` glob). Falsifies "test corpus deploys."
- **P9 — byte-alignment of the recomposed schema/template region.** `diff` the `decision-register.md` schema +
  bw-write template region across the source and both recomposed hosts (subproject tier) → identical. Falsifies
  "an inlined copy drifted."
- **P10 — honesty-posture grep (the deliverable IS the honesty).** `grep -iE "enforced|guaranteed|non-collapsible"`
  over `decision-register.md` + its README returns NO hit that claims the writing-discipline/counter-hypothesis
  is mechanically guaranteed (only honest "high-probability + regression-guard" phrasing). Falsifies "we
  over-claimed."

---

## §4. Self-assessed weak points (§6.2 post-work)

- **WP-1 — "a path was chosen" is the softest read in the design.** Condition (3) of DC1 is model judgment; the
  corpus tests it only as a `--judge` floor on n=5 `decided/` + n=4 `illuminated/` fixtures. *Why this shape
  anyway:* this is the irreducible-judgment boundary the whole doctrine accepts (you cannot shell-check "was it
  decided" any more than "is it a dilemma"); pretending otherwise would be the exact fake-certainty A3 forbids.
  The honest move is the split + the floor + the accretion path, which is what I designed.
- **WP-2 — the vacuity denylist is a seed, not a vacuity proof.** A weak-but-non-vacuous counter-hypothesis
  ("the metrics will be bad") slips the denylist while still being hollow. *Why anyway:* DC4's honest stance is
  exactly "detect the canonical patterns, raise the probability, NOT guarantee" — the denylist is the Arc-70
  empty-WHY analog, designed to accrete; claiming it proves non-hollowness would violate A3.
- **WP-3 — the standing-ticket comment-stream gets coarse at scale for topic-query.** A long stream is hard to
  query by topic. *Why anyway:* topic-indexing is a 2b-reader concern (out of scope); for capture, append-only
  chronological is the right journal shape, and promotion to per-decision tickets is a forward move 2b can make
  against real data rather than a slice-2a guess (A2).
- **WP-4 — team-deployment transparency is "all-seats-readable," which a PRINCIPAL-only deployment would not
  want.** *Why anyway:* the doctrine's named property is bw-transparency, the primary target is single-user, and
  per-user visibility scoping is 2b dose-calibration territory (out of scope) — naming the caveat rather than
  building scoping keeps the slice tight and honest.
- **WP-5 — DC2's new-module-vs-extension call is value-weighted.** I weighted "clean seam for 2b + one-job hygiene"
  over "fewest composition markers." A reviewer who weights composition-minimalism higher could prefer the
  extension. *Why anyway:* I named the weighting explicitly (DC2) rather than laundering it as obvious, so ARGUS
  and the gate can contest the weighting directly; the seam-for-2b argument is the strongest because 2b composes
  against the register, not the classifier.

---

## §5. Out of scope (the 2b boundary — a design reaching in is auto route-back)

- **The complaint-time CALLBACK** — surfacing the specific logged entry when the PRINCIPAL later complains.
  Slice 2b. This design SPECIFIES the schema so 2b can re-read it (DC0 forward-constraint, P7) but builds NO
  reader, NO surfacing, NO callback.
- **The RE-VERIFY GATE** — checking whether a logged entry actually supports a later callback ("does the record
  contain the warning?"). Slice 2b. The `COUNTER-HYPOTHESIS`/`WARNING` fields are captured AS 2b's future input;
  nothing reads or gates on them here.
- **Dose calibration off the user's track record** — slice 2b. (Named as the home for any per-user visibility
  scoping — WP-4.)
- **The long-deliberation meta-trigger auto-detect** — deferred (doctrine Still-open / Arc 4); no
  circling-detection here.
- **Graduating `decision-surface` from DRAFT** — its own arc (`stoa--ida`).
- **Broader checkpoint rollout** beyond the Arc-70/Arc-71 subset — the capture composes ONLY into the existing
  Arc-70 checkpoint homes; no new checkpoints are added.
- **Per-decision-ticket promotion / topic indexing of the register** — a forward move 2b/later can make against
  real entries (WP-3); not built now.
