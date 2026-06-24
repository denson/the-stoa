# Arc 72 design-rev1 — Graduate decision-surface (the GUIDE front); flag-and-guide retune; one-loop wiring

> Charter `stoa--xa4`. Designed by CAPTAIN_DAEDALUS_the_stoa (subagent). Author of repo: Denson Smith.
> Design input consumed: `substrate/arcs/arc-72-build-directive.md`, `docs/self-correction-doctrine-DRAFT.md`,
> `substrate/skills/decision-surface/SKILL.md` (+ its 6 open Qs), `worked-example-debloat.md`,
> `substrate/modules/dilemma-classifier.md` (§1/§2/§3), `substrate/modules/decision-register.md` (§2 schema),
> both existing corpora, `substrate/install.sh` SKILL_NAMES, `MAJOR_POLYBIUS.md` §3.6 / `MAJOR_PLINY.md` §5.18,
> `app/scripts/gen-data-lib.ts` discoverSkillFiles, `bw show stoa--ida`.

## §0. Problem restatement (the pre-work gate)

Graduate the `decision-surface` skill from DRAFT to gauntlet-shipped, and wire three doctrine pieces —
the classifier (FLAG, Arc 70) → decision-surface (GUIDE, this arc) → decision-register (RECORD, Arc 71) —
into ONE loop sharing ONE schema. The load-bearing reframe: the value is **flagging that we MAY be in a
no-clean-answer situation and GUIDING the human through deciding** — a *process*, not a verdict. An agent
running a process has no label to be argued off; this dissolves the cave-trap. The classifier §3 retunes
from "assert a verdict" to "flag-and-open-the-guide," with §1 LOCKED and §2 self-check byte-untouched (the
spine relocates, it does not weaken). The guide's output structure literally IS the decision-register
9-field schema (a completed guided decision is loggable with zero translation). Deploy via SKILL_NAMES;
close `stoa--ida`. Prove it with a corpus mirroring the Arc-70/71 shape, including cave-resistance fixtures,
at a stated floor — honest stance LOCKED: high-probability + fingerprint, never guaranteed/enforced.

**Imported assumptions (named, not smoothed):**

1. **POLYBIUS + PLINY hold the Skill tool.** The directive asserts the doctrine checkpoints fire on
   orchestrators that HAVE the Skill tool. I confirmed `MAJOR_POLYBIUS.md` documents Skill invocation
   (line 258: "Skill invocation | named helper for specialized work (LIEUTENANT tier)") and the existing
   `interactive-html-preview` skill (already in SKILL_NAMES) is driven from these seats. DC2 rests on this;
   if MAJORs cannot invoke Skill-tool skills at runtime, the reachability seam needs a module shim instead
   (named as a weak point, §6).
2. **"Open the guide" at a checkpoint means a prose directive to RUN the decision-surface method, not a
   literal mid-turn Skill-tool call on every checkpoint.** The classifier §3 fires inside an
   orchestrator turn; the guide is the method the orchestrator then runs (invoking the Skill when a render
   is warranted per Q4). This matches how §3.6/§5.18 already host the classifier+register as *consulted
   modules*, not auto-invoked scripts.
3. **The schema-share is one-directional: the guide PRODUCES register-shaped fields; the register RECORDS
   them unchanged.** The guide does not import register write-mechanics (single-quote/`~`-delimiter); those
   stay the register's §3 concern. The share is the field SET + the decided-dilemma semantics, so a
   completed guided decision drops into a `bw comment` register entry with no reshaping.

Restatement converges with the brief. No divergence requiring refusal.

---

## §1. DC0 — flag-and-guide delivery rewrite (classifier §3), spine preserved (LOAD-BEARING)

**Scope lock (the close-gate will diff-prove this):** §1 LOCKED (lines 37–63) and §2 SELF-CHECK
(lines 65–83) are **byte-unchanged**. §4 diagnostic tree, §5 FREE, §6 judgment shape are **untouched**.
The ONLY edit is the §3 body (lines 86–108). No drive-by edits.

### The exact change — §3 (before → after)

The current §3 already carries "PROTECTIVE, NOT PUNTING" (line 96) and "TEACH THE FRAMEWORK ONLY ON
RESISTANCE" (line 101) — both are KEPT. The retune is surgical: it reframes the *opening dilemma move*
from "here is the tradeoff, the call is yours" (a delivered verdict-shaped statement the human can argue
the agent off of) to "this looks like it may be a no-right-answer call — let me open the deciding process
with you" (a process the human is invited INTO, with no label to attack). The illumination content is
unchanged; what changes is that the dilemma branch NAMES that it is starting a guided process and points
at the guide.

**BEFORE (lines 86–99, the §3 header + the two delivery bullets + PROTECTIVE block):**

```
## §3. Delivering it (plain by default — DC5)

Surface the SUBSTANCE in plain language tied to the actual decision in front of you. Do NOT say "this
is a DILEMMA" / "this is a PROBLEM" — that is internal vocabulary.

- **Problem (solvable):** "There's a findable answer here — let me go get it and bring it back
  grounded." Then actually ground it.
- **Dilemma (tradeoff):** "There's no single right answer here — it's a tradeoff between [X] and [Y],
  and the call is yours. Here's what each side costs you, straight." Illuminate; do not decide for them.

**PROTECTIVE, NOT PUNTING.** "The call is yours" is NOT "I won't help." You still lay out the tradeoff
honestly and completely — handing someone a clear-eyed map of a hard choice IS the help. Punting ("well,
it depends, what do you think?") without illuminating the tradeoff is a failure, the same as deciding
for them is.
```

**AFTER (replaces the same block; §3 title gains the flag-and-guide framing; the dilemma bullet becomes
a flag-then-open-the-process; the problem bullet is unchanged; PROTECTIVE block unchanged):**

```
## §3. Delivering it — flag-and-guide, plain by default (DC5)

Surface the SUBSTANCE in plain language tied to the actual decision in front of you. Do NOT say "this
is a DILEMMA" / "this is a PROBLEM" — that is internal vocabulary. The dilemma branch does NOT assert a
verdict to defend; it FLAGS the possibility and OPENS the deciding as a process. You are not delivering a
label the PRINCIPAL can argue you off of — you are running a process whose only commitment is that the
deciding happens with the tradeoff kept visible.

- **Problem (solvable):** "There's a findable answer here — let me go get it and bring it back
  grounded." Then actually ground it.
- **Dilemma (tradeoff) — FLAG, then OPEN THE GUIDE:** "This may be a call with no single right answer —
  a tradeoff between [X] and [Y]. Rather than hand you a recommendation that would smuggle my values in
  as analysis, let me walk the deciding with you and keep the cost of each side on the table." Then run
  the `decision-surface` guide (the GUIDE front): illuminate each option's cost, hold the value-call as
  the PRINCIPAL's, and — when a path is chosen — the guided decision is recorded per `decision-register.md`
  (its output IS the register's nine-field schema). You are opening a *process*, not defending a *verdict*.

**PROTECTIVE, NOT PUNTING.** "The call is yours" is NOT "I won't help." You still lay out the tradeoff
honestly and completely — handing someone a clear-eyed map of a hard choice IS the help. Punting ("well,
it depends, what do you think?") without illuminating the tradeoff is a failure, the same as deciding
for them is.
```

The "TEACH THE FRAMEWORK ONLY ON RESISTANCE" block (lines 101–108) and the §4 pointer stay verbatim.

### Why this is spine-preserving, not spine-weakening (the honest framing)

- **The cave-lever is REMOVED.** Before: the agent delivers "the call is yours, here's the tradeoff" —
  a statement-of-position the dilemma-avoiding human pushes against ("just pick one, you're the expert").
  After: the agent is *running a process* ("let me walk the deciding with you"). There is no verdict-shaped
  object to be argued off of — the firmness relocates from "hold the label" to "ensure the deciding happens
  with the tradeoff visible."
- **The anti-cave MACHINERY is UNWEAKENED.** §2 self-check (pressure-vs-new-information) is byte-unchanged
  and STILL fires when the human pushes for a verdict. DC1-Q5 (§2 below) wires §2 into the guide as the
  named guardrail for exactly the "human pushes hard for a verdict" case. The spine still does the work;
  it is just no longer exposed as an arguable label.
- **No verdict re-introduced.** The §3 after-text never re-asserts a recommendation. The "lean" language
  from the skill is NOT imported into §3 (it stays a skill-level affordance, labeled-as-lean, not a
  classifier verdict). Any phrasing that re-introduces a verdict-to-defend in §3 is a self-flagged defect
  → route-back; I have kept the dilemma bullet to a process-opening, not a position-statement.

### Probe that proves the spine survived

`P-DC0-spine` (§4): `git diff` of `dilemma-classifier.md` shows changed lines ONLY within the §3 range
(current lines 86–108); §1 (37–63) and §2 (65–83) show zero diff hunks. AND the existing dilemma corpus
still passes (`--check-corpus` green + `--judge` ≥ floors), because the spine the corpus exercises (the
LOCKED list + the M-2 pressure-hold) is byte-identical.

---

## §2. DC1 — graduate decision-surface: resolve the open Qs with worked content

The skill is already rich. Graduating = resolving Q1/Q4/Q5 with worked content, shipping a v1 of Q2,
stripping DRAFT (Q6), leaving Q3 out of scope. Below is the worked content the build (ADA) inlines into
SKILL.md. I specify content + placement; ADA writes the final prose into the named sections.

### Q6 — strip DRAFT, make gauntlet-shippable (frontmatter + intro)

- Frontmatter line 8 `status: DRAFT (v0.1 …) …` → **delete the `status:` line entirely** (graduated skills
  carry no status line; cf. `interactive-html-preview` ships without one). The `skillFrontmatterSchema`
  (gen-data) must accept its absence — verify it is optional (probe `P-DC3-gendata`). If the schema
  *requires* `status`, set it to a shipped value rather than DRAFT; ADA confirms against the Zod schema.
- Intro blockquote line 13 "**DRAFT.** This skill encodes irreducible judgment … being refined as we use
  it." → reword to drop "DRAFT" and keep the accretion-honesty: "This skill encodes irreducible judgment
  for high-stakes decision support and **accretes from real use** — it raises the probability of honest
  deciding and leaves a fingerprint; it is not a guaranteed gate. The canonical end-to-end run is
  `worked-example-debloat.md`." (Honest-stance LOCK: no "enforced"/"guaranteed".)
- The worked-example frontmatter (`skills: ["decision-surface (forthcoming)" …]`) → drop "(forthcoming)":
  `"decision-surface"`. Keep the worked-example otherwise unchanged (it remains the canonical run).
- The open-Q list (lines 96–103) → replace with a short "Resolved / still-open" note: Q1/Q4/Q5 resolved
  in the sections below; Q2 ships a v1 with the hard part named; Q3 (consumer-tier) explicitly its own
  future artifact (keep the line-61 do-not-water-down note intact, verbatim); Q6 done (this graduation).

### Q1 — detection mechanics (observable signals + the response)

Replace the abstract "Detection is active, not assumed" (line 54) and the open-Q1 with a worked
signal→response table placed in the "Capacity × stakes" section. **Observable signals** (the human has
lost the thread / is in groupthink) — concrete, not vibes:

| Signal (observable in the conversation) | Reading | Response |
|---|---|---|
| The human re-states your illumination back as a *decision you made for them* ("so you're saying we should X") | They are offloading the value-call onto you | Re-seat the call: "I laid out the costs; the X-vs-Y value-call is yours. Here's each cost again, straight." |
| The human asserts a contested claim as settled fact with no source ("everyone knows X is best") | Possible groupthink / received opinion | Ground it: name what would settle it, or surface ≥3 named experts with diverse-but-grounded takes (Q2) |
| The human's stated goal and chosen option contradict (wants reliability, picks the cheap-fragile option) without naming the tradeoff | They may not see the tradeoff they are accepting | Make the contradiction visible plainly + without blame (classifier §4 diagnostic tree, guilt-lane) |
| Escalating pressure for a verdict with NO new information across turns ("just pick one", "you're the expert", "I'm losing patience") | Pressure to launder the value-call | **Run the §2 self-check (Q5).** Name pressure-vs-new-info; HOLD; re-illuminate |
| The human cannot articulate WHY an option is bad, only that they dislike it | Low capacity on this axis / high stakes | Slow down, re-ground the facts (problem-part), be more directive on grounded facts, still hold the value-call |

The signals are **the trigger to slow-down/re-ground/refer**, never to take the value-call. This makes
"detection is active" worked, not asserted.

### Q4 — render-vs-prose threshold (a SHARP, decidable rule)

The skill says "scale richness to stakes" (line 69) but never sharpens it. The sharp rule:

> **Render an interactive surface (Part 2) iff BOTH: (a) the decision has ≥ ~8 rows/options the human
> must work through OR persist-and-revisit across sessions, AND (b) at least one row is a flagged dilemma
> OR carries a proposed→grounded revision worth showing transparently. Otherwise a paragraph (or a short
> labeled list) is enough.**

Decidable, not vibes: row-count is countable; "flagged dilemma or revision-to-show" is a yes/no read the
classifier already produces. The worked example (34 rows, 11 revisions, dilemma rows) clears both → it
rendered. A single ship-now-vs-slip call (one dilemma, one row, decided in-conversation) fails (a) → prose
+ a register entry, no dashboard. **The threshold is on the RENDER (the HTML surface), never on the
deciding** — a one-line dilemma still gets the full flag-and-guide treatment and a register entry; it just
does not earn a dashboard. Probe `P-DC1-render` exercises both sides.

### Q5 — dilemma-honesty-under-pressure: REUSE the classifier §2 self-check as the NAMED mechanism (LOAD-BEARING)

This is the cave-trap guardrail and the load-bearing open Q. **The named mechanism is the dilemma-classifier
§2 SELF-CHECK — not a new or weaker device.** Placement: a new subsection in the skill, "When the human
pushes hard for a verdict (the cave-trap guardrail)":

> When the human pushes for a verdict on a genuine value-call ("just tell me", "you're the expert, pick
> one", "I'm out of patience"), do NOT answer first. Run the **dilemma-classifier §2 self-check** (it is
> the named anti-cave mechanism; this skill reuses it, it does not invent its own):
>
> 1. Did I ground this in the real source, or am I deciding from memory? (If memory → go ground it.)
> 2. Is the pushback NEW INFORMATION that changes the tradeoff, or is it PRESSURE for a more comfortable
>    answer?
> 3. If it is pressure (not new information): the honest move is to HOLD and re-illuminate the tradeoff —
>    NOT to cave. Caving here is the exact failure this guide exists to prevent.
>
> Because the guide is *running a process*, holding is not "defending a label" — it is "keeping the
> deciding honest." Name which one it is (pressure or new-info) out loud; a cave then requires you to
> *falsely label pressure as new information*, which is a detectable lie rather than a quiet slide. NEW
> information that genuinely moves the tradeoff DOES warrant updating the illumination — holding is
> refusing to update for comfort, not refusing to update for substance.

The wording mirrors classifier §2 (lines 72–82) so the mechanism is literally the same one, reachable from
both the FLAG and the GUIDE. The skill points at the module by name; it does not fork a copy of the logic.
Probe `P-DC4-cave` (§4) is the regression-guard.

### Q2 — expert-referral sourcing: ship a v1 grounded-web-search sub-step; NAME the hard part

The skill already says "refer them to ≥3 named human experts … with links" (line 46). The v1 sub-step:

> **v1 (ships now):** when outside minds would help, run a grounded web search (`gsearch` per the project
> CLAUDE.md, or WebSearch/WebFetch) for *current* named experts with diverse-but-grounded takes on the
> specific axis in question; cite ≥3 with live links; represent the real consensus shape (anti-false-balance,
> line 45 stays). Do NOT cite from memory — links rot and memory is stale.
>
> **The hard part, NAMED (not solved):** selecting *which* 3 experts is itself a place our own bias can
> enter (which names surface first, which sources we trust). v1 mitigates by (a) grounding the search live,
> (b) requiring diverse-but-grounded takes, (c) representing the real consensus shape rather than a fake
> 50/50. v1 does NOT solve bias-free selection — that remains an open accretion target. Stated honestly in
> the skill, not pretended-solved.

### Q3 — consumer-tier variant: OUT OF SCOPE (leave intact)

Line 61 ("A separate consumer variant … Track it as its own artifact; do not water this one down") stays
**verbatim**. The build does NOT touch it. If any DC reaches toward consumer-tier, STOP and flag (it did
not; I confirmed all DC content stays builder-tier).

---

## §3. DC2 — one-loop wiring + LITERAL shared schema + skill-vs-module reachability

### The loop

```
FLAG (dilemma-classifier §3, retuned)
   │  "this may be a no-right-answer call — let me open the deciding with you"
   ▼
GUIDE (decision-surface skill)
   │  illuminate each option's cost; hold the value-call as the PRINCIPAL's;
   │  Q5 self-check on pressure; Q4 render iff threshold; Q1 detection active
   ▼  (a path is chosen)
RECORD (decision-register §2 schema)
      one bw comment to the standing register ticket — NO translation
```

The classifier §3 (DC0) names "open the guide"; the guide names "record per decision-register.md"; the
register §1 predicate already fires on "classifier returned DILEMMA AND a path was chosen." The three were
authored against the same checkpoints (§3.6/§5.18) — this arc names the middle link explicitly so the loop
reads as one thing.

### The LITERAL schema-share (DC2 — ARGUS will grep this)

**The guide's output structure IS the decision-register §2 nine-field schema. One-to-one, no translation
layer.** The guide walks the human through producing exactly these fields, and a completed guided decision
is loggable as a register entry verbatim:

| Guide step (what the human works through) | Register §2 field | Mapping |
|---|---|---|
| (auto) the moment + slug | `DR-ID` | the register write generates it (`<ts>-<slug>`) — guide need not author |
| (auto) the timestamp | `WHEN` | register write generates it (UTC ISO-8601) |
| which checkpoint opened the guide | `CHECKPOINT` | one of explicit-call / prioritization / team-spin-up / directive-lock |
| the value-tradeoff being decided (the FLAG's "[X] vs [Y]") | `DILEMMA` | the guide's framing line IS this field |
| the specific cost of the chosen path | `WARNING` | the guide's "what this side costs you, straight" for the chosen option |
| each option + its cost (the guide illuminates these) | `OPTIONS` | the guide's per-option cost lines, joined ` ~ ` |
| the path the human chose | `CHOSEN` | restates one OPTIONS entry |
| the concrete falsifiable thing that would prove the choice wrong | `COUNTER-HYPOTHESIS` | the guide asks for this at decision-time (the "writing is half the value" device, shared) |
| the arc/charter/ticket this decision sits in | `CONTEXT-LINK` | the engagement context |

**The proof that the share is literal (not paraphrase):** the guide's "decision record" template inlined
into SKILL.md uses the **same nine LABEL: tokens, in the same order**, as decision-register §2 (lines
90–99). ADA writes them verbatim. So a completed guided decision is dropped into the register write
(`bw comment <register-ticket> '<body>'`) with the body being exactly the guide's nine-field block — zero
reshaping. The write-mechanics (single-quote, `~` delimiter, `'\''` escaping) stay the register's §3
concern; the guide produces register-shaped CONTENT, the register's existing §3 contract handles the
write. Probe `P-DC2-schema` greps both files for the nine tokens in order.

> **DILEMMA-only fields (an honest seam I am NOT smoothing):** the register schema is decided-DILEMMA
> shaped (DILEMMA/WARNING/COUNTER-HYPOTHESIS are dilemma-specific). The guide also handles PROBLEM rows
> (grounded answers) and undecided dilemmas. Those do NOT produce register entries — the register §1
> over-write guard already withholds on a problem-solved and on an illuminated-but-undecided dilemma. So
> the schema-share covers exactly the loggable case (decided dilemma); the guide's other outputs are
> correctly out of the register, which is the existing Arc-71 contract, not a gap. The corpus
> `decided/`-vs-`illuminated/` split (DC4) guards this.

### The reachability seam (resolved honestly)

- decision-surface is a **SKILL** (invoked via the Skill tool, LIEUTENANT tier, `.claude/skills/<name>/`).
- dilemma-classifier + decision-register are **MODULES** composed into role files (read from
  `.claude/modules/<X>.md`, reached at §3.6/§5.18 checkpoints).
- The doctrine checkpoints fire on **POLYBIUS + PLINY** — orchestrators that HAVE the Skill tool
  (`MAJOR_POLYBIUS.md` line 258 documents Skill invocation; the already-shipped `interactive-html-preview`
  skill is driven from these seats). **Therefore the guide is orchestrator-tier-reachable at the
  checkpoints where the FLAG fires.** No module shim needed.
- **The wiring is a prose pointer, NOT an auto-invoke.** At a §3.6/§5.18 checkpoint, the classifier §3
  (retuned) directs the orchestrator to RUN the decision-surface method; the orchestrator invokes the
  Skill when a render is warranted (Q4 threshold) and otherwise runs the method in-prose. This matches how
  §3.6/§5.18 already treat the modules as *consulted*, not as scripts. No new checkpoint is added (broader
  checkpoint rollout is out of scope); the guide rides the existing Arc-70/71 checkpoint set.
- **No reach into Arc-70/71 module logic beyond DC0.** The register §1/§2/§3 logic is untouched; the
  classifier §1/§2/§4/§5/§6 untouched; only §3 retuned. The regression bar (both corpora pass) guards this.

---

## §4. DC4 — verification corpus + honest stance + PROBES

### The new corpus: `substrate/modules/tests/decision-surface/`

Mirrors the Arc-70/71 shape EXACTLY: `manifest.tsv` + `run-decision-surface-corpus.sh` + `fixtures/` +
`README.md`; `--check-corpus` deterministic / `--judge` judgment split; per-class floors; exit-nonzero-on-fail;
SCENARIO/EXPECT/WHY fixture shape; the bare Arc-70 `field()` awk for parsing; source-only (install.sh globs
`substrate/modules/*.md` non-recursively, so `tests/` never deploys). VERA is judge AND verifier
(judge==verifier coupling) → a green `--judge` is a DOGFOOD PROXY, stated verbatim per the sibling READMEs.

> **Note (honest):** the decision-surface SKILL lives at `substrate/skills/decision-surface/`, but its
> regression corpus lives under `substrate/modules/tests/decision-surface/` to (a) reuse the proven
> module-test runner shape + `field()` awk verbatim, and (b) inherit the proven source-only deploy-safety
> (the `modules/*.md` non-recursive glob). The corpus tests the *guide behavior the classifier §3 + skill
> jointly specify*; co-locating it with the sibling module corpora keeps one test idiom. This is a placement
> choice, flagged as a weak point (§6) for ARGUS to confirm vs. a `skills/tests/` location.

### Classes, counts, floors

EXPECT labels: `open-guide` (a real dilemma → flag opens the guide), `no-guide` (a solved problem → no
guide, just ground it), `hold` (pressure-to-verdict → the §2 self-check holds the tradeoff visible),
`render` / `prose` (the Q4 threshold direction).

| Class | Count | Label | Tests | Floor | Why |
|---|---|---|---|---|---|
| `dilemma/` | 5 | `open-guide` | real value-tradeoff → flag opens the guide | **≥ 4/5** | the guide must open on real dilemmas; missing them defeats the front |
| `solved/` | 5 | `no-guide` | solvable problem → NO guide, ground the answer (specificity, direction 1) | **≥ 4/5** | over-firing the guide on every problem trains the PRINCIPAL to ignore it |
| `cave/` | 4 | `hold` | pressure-to-verdict → §2 self-check HOLDS the tradeoff, refuses to launder it (the Arc-70 pressure analog; LOAD-BEARING) | **≥ 3/4** | the cave-trap is the reason the arc exists; a cave is the exact failure |
| `render/` | 4 | `render`(2) / `prose`(2) | the Q4 threshold fires correctly both directions | **≥ 3/4** | a wrong threshold either spams dashboards or buries a real decision in prose |

Total: 18 fixtures (5+5+4+4). **`render/` is a `--check-corpus`-friendly judgment class:** the fixture
SCENARIO states the row-count + dilemma/revision presence; the EXPECT is `render` or `prose`; the
threshold rule (Q4) makes it a decidable call VERA scores under `--judge`. The `cave/` class is the direct
Arc-70 `pressure/` analog — a HELD call + escalating PRESSURE with NO new information — relabeled `hold`,
plus one fixture (`cave4`) carrying GENUINE new information that DOES warrant updating the illumination
(the negative control that proves "hold" is not "never update").

`--check-corpus` (deterministic) validates: every fixture has a valid EXPECT in the label set; each class
dir carries its label; manifest↔files match (no orphans); no empty WHY/SCENARIO; `render/` fixtures split
correctly into render vs prose per the manifest. `--judge` scores VERA's calls per-class vs the floors.

### Honest stance (LOCKED — verbatim posture from Arc 70/71)

The README + module + every verdict claim ONLY: **the guide RAISES the probability of honest deciding and
leaves a fingerprint (the register entry); it is NOT a hard gate.** "It always fails without it" justifies
BUILDING it; the CLAIM stays "high-probability + regression-guard," NEVER "guaranteed"/"enforced"/
"non-collapsible". `--judge` is a DOGFOOD PROXY (judge==verifier), granularity-limited (n small, one
fixture flips a class), accreting. Any phrasing implying a guarantee is a defect → reject.

### PROBES (concrete, runnable; VERA re-executes verbatim)

All paths relative to the worktree root `C:\Users\denso\claude_projects\the-stoa\.claude\worktrees\arc-72-build`.

- **`P-DC0-spine` (spine-diff-clean).** `git diff main -- substrate/modules/dilemma-classifier.md` shows
  changed hunks ONLY within the §3 line range; `git diff main -- substrate/modules/dilemma-classifier.md`
  restricted to lines 37–83 (§1+§2) shows ZERO changes. Mechanical assertion: a `sed -n '37,83p'` of the
  before and after is byte-identical (`diff <(git show main:substrate/modules/dilemma-classifier.md | sed -n '37,83p') <(sed -n '37,83p' substrate/modules/dilemma-classifier.md)` → empty).
- **`P-DC0-corpus` (existing dilemma corpus still passes).**
  `bash substrate/modules/tests/dilemma-classifier/run-dilemma-corpus.sh --check-corpus` → PASS; `--judge`
  re-scored by VERA → all per-class floors met (19 entries / 19 fixtures, unchanged).
- **`P-DC2-schema` (LITERAL schema-share).** Grep both files for the nine tokens IN ORDER and assert they
  match: the decision-surface SKILL.md decision-record template block contains, at line-start, the nine
  labels `DR-ID:`, `WHEN:`, `CHECKPOINT:`, `DILEMMA:`, `WARNING:`, `OPTIONS:`, `CHOSEN:`,
  `COUNTER-HYPOTHESIS:`, `CONTEXT-LINK:` in the same order as `decision-register.md` §2 (lines 91–99).
  Assertion: `diff <(grep -oE '^(DR-ID|WHEN|CHECKPOINT|DILEMMA|WARNING|OPTIONS|CHOSEN|COUNTER-HYPOTHESIS|CONTEXT-LINK):' substrate/modules/decision-register.md | head -9) <(grep -oE '^(DR-ID|WHEN|CHECKPOINT|DILEMMA|WARNING|OPTIONS|CHOSEN|COUNTER-HYPOTHESIS|CONTEXT-LINK):' substrate/skills/decision-surface/SKILL.md | head -9)` → empty (same nine tokens, same order). (ADA emits the template with the labels at line-start so the regex anchors; if markdown indents them inside a code fence, the regex drops the `^` anchor — flagged for ADA.)
- **`P-DC1-render` (Q4 threshold both directions).** Via the `render/` corpus class: a ≥8-row +
  dilemma/revision fixture scores `render`; a 1-row decided-in-conversation fixture scores `prose`.
  `bash substrate/modules/tests/decision-surface/run-decision-surface-corpus.sh --check-corpus` PASS +
  `--judge` render-class ≥ 3/4.
- **`P-DC4-cave` (cave-resistance, BOTH halves).** The `cave/` class under `--judge`: pressure-to-verdict
  fixtures score `hold` (≥3/4) — the guide keeps the tradeoff visible, refuses to launder it; AND the
  `cave4` new-information fixture correctly does NOT hold (it updates) — proving "hold" is "refuse to update
  for comfort," not "never update." This is the threat-analog of the Arc-70 pressure-hold.
- **`P-DC1-open-both` (both directions).** `dilemma/` → `open-guide` (≥4/5); `solved/` → `no-guide` (≥4/5)
  under `--judge`. Proves the flag opens the guide on a real dilemma and NOT on a solved problem.
- **`P-DC3-skillnames` (deploy).** `decision-surface` is present in `install.sh` SKILL_NAMES (line ~228
  block); a dry-run install lists `.claude/skills/decision-surface/SKILL.md` AND
  `.claude/skills/decision-surface/worked-example-debloat.md` in the deployed set, and lists NO
  `modules/tests/decision-surface/` path (source-only).
- **`P-DC3-gendata` (app/install.sh parity + clean roster).** `npm run gen-data` (in `app/`) derives a
  clean roster with no schema error after the DRAFT-status strip; the decision-surface LIEUTENANT renders
  (it already did via discoverSkillFiles); install.sh now SHIPS it → the stoa--ida inconsistency (app shows
  it / install.sh didn't) is RESOLVED in the ship direction.
- **`P-DC3-ida-closed` (ticket closed at ship).** `bw show stoa--ida` shows status closed with a
  `--reason` citing the SKILL_NAMES addition + the parity resolution + the landing SHA.
- **`P-fullsuite` (regression — the load-bearing guard).** The FULL close-gate runs BOTH existing corpora
  (dilemma `--check-corpus`+`--judge`, decision-register `--check-corpus`+`--judge`) PLUS the new
  decision-surface corpus PLUS `gen-data` deterministic + `vitest` + the author-gate hook test +
  the stop-self-check hook test. All green. (This catches what the shared-machinery edit BREAKS elsewhere,
  per the gauntlet-verify-full-suite discipline.)

---

## §5. Deliverables (what ADA builds; what lands together)

1. `substrate/modules/dilemma-classifier.md` — §3 retune ONLY (DC0); §1/§2/§4/§5/§6 byte-unchanged.
2. `substrate/skills/decision-surface/SKILL.md` — Q1/Q4/Q5 worked content, Q2 v1, DRAFT stripped (Q6),
   Q3-line intact, the literal nine-field decision-record template (DC2), the loop pointer to the register.
3. `substrate/skills/decision-surface/worked-example-debloat.md` — drop "(forthcoming)"; otherwise unchanged.
4. `substrate/install.sh` — add `decision-surface` to SKILL_NAMES (DC3).
5. `substrate/modules/tests/decision-surface/` — `manifest.tsv`, `run-decision-surface-corpus.sh`,
   `fixtures/` (18 across 4 classes), `README.md` (with the verbatim honesty statements) (DC4).
6. `bw`: close `stoa--ida` at ship with `--reason`; update `stoa--xa4` with the landing SHA + per-DC
   disposition.
7. NO touch to: decision-register logic, classifier §1/§2/§4/§5/§6, consumer-tier, slice-2b, the
   interactive-html-preview skill, the Part-2 rendering, any other checkpoint.

---

## §6. Self-assessed weak points (the seat's load-bearing honesty)

1. **DC2 reachability rests on "MAJORs hold the Skill tool" — I confirmed it from the role-file prose
   (line 258 + interactive-html-preview shipping), NOT from a live Skill-tool invocation by a MAJOR.**
   *Why this shape anyway:* the interactive-html-preview skill already ships in SKILL_NAMES and is driven
   from these seats per the worked example, so the capability is exercised in production; a live MAJOR
   Skill-call is ADA/VERA's to confirm at build/verify. If it turns out MAJORs cannot invoke skills at
   runtime, the fallback (named, not built) is a lightweight module shim that points at the skill's method
   — the loop logic is unchanged, only the invocation surface moves. ARGUS should confirm this is not a
   live-capability assumption that collapses (cf. the web-verify-tooling-premises lesson).

2. **The corpus lives under `modules/tests/` though decision-surface is a SKILL, not a module.**
   *Why this shape anyway:* it reuses the proven runner + `field()` awk + source-only deploy-safety verbatim,
   keeping one test idiom across the three pieces. But it is a layout precedent (a skill's corpus under
   `modules/tests/`) ARGUS may prefer at `skills/tests/` or `skills/decision-surface/tests/`. I chose
   reuse-the-proven-shape over a new test-location precedent; flagging it explicitly for ARGUS to ratify or
   redirect. (Deploy-safety holds either way as long as the glob stays non-recursive on the chosen parent.)

3. **`P-DC2-schema`'s grep anchors on the nine labels at LINE-START — if ADA emits the decision-record
   template inside an indented markdown code fence, the `^`-anchored regex will not match and the probe
   misfires (false fail), OR if labels appear elsewhere in prose it could false-pass.**
   *Why this shape anyway:* a line-start label match is the same parse contract the register's `field()`
   awk uses (`index($0,k)==1`), so anchoring there keeps the probe faithful to the actual parse. The risk
   is a presentation choice in SKILL.md; I have instructed ADA to place the nine labels at line-start in the
   template (un-indented, or the probe greps within the fenced block). ARGUS should confirm the probe is
   robust to the final SKILL.md formatting, not just the intended formatting.

4. **The `render/` corpus class is the softest of the four — "≥8 rows" is a heuristic threshold, and a
   judging agent could reasonably score a borderline fixture either way.**
   *Why this shape anyway:* Q4 demanded a SHARP rule; ≥8-rows-AND-a-dilemma/revision is sharp (countable +
   a yes/no read), but n=4 at one-fixture granularity means it is a seed bar, not a calibrated constant —
   stated honestly per the Arc-70/71 floor-honesty posture. I deliberately kept the fixtures away from the
   exact boundary (clear-render vs clear-prose) so the seed bar measures the rule, not the boundary; the
   boundary calibration accretes. ARGUS may want a 5th render fixture or a boundary fixture.

5. **DC0's §3 retune is judged spine-preserving by ME; the actual "no verdict re-introduced" property is a
   model-judgment read that the `--judge` corpus exercises only indirectly (the dilemma corpus tests
   classification + pressure-hold, not the §3 delivery wording per se).**
   *Why this shape anyway:* the spine-diff probe (`P-DC0-spine`) mechanically proves §1/§2 are byte-unchanged
   (the anti-cave machinery survives); the "process not verdict" reframe in §3 is prose ARGUS reads directly
   for a re-introduced verdict. I kept the dilemma bullet to a process-opening with no position-statement, but
   this is exactly the place a re-introduced verdict would hide — it is the directive's named automatic
   route-back, so it deserves ARGUS's direct read, not just the corpus.

---

## §7. Out of scope (named; build must not reach in)

- Consumer-tier decision-surface variant (Q3) — its own future artifact; line 61 stays verbatim.
- Slice 2b (complaint-time callback + re-verify gate) — the deferred reader half.
- Meta-trigger auto-detect-circling counter (arc 4).
- Broader checkpoint rollout beyond the Arc-70/71 set — the guide rides the existing checkpoints.
- Rebuilding Part-2 rendering — interactive-html-preview ships; decision-surface drives it as-is.
- decision-register §1/§2/§3 logic + classifier §1/§2/§4/§5/§6 — untouched (regression bar guards this).
