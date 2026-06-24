# Design — Decision-register READER: complaint-callback + re-verify gate (self-correction slice 2b)

**Ticket:** `stoa--51k` (Arc 73). **Author of repo:** Denson Smith.
**Design input:** `docs/self-correction-doctrine-DRAFT.md` §6 (longitudinal loop) + **Resolved** (the re-verify gate) + §8 (egoless guilt-lane); `substrate/modules/decision-register.md` §2 (the 9-field schema this READS).
**Directive:** `substrate/arcs/arc-73-build-directive.md` (NOMOS-CONFORMANT). **Builds on:** Arc 70 (`dilemma-classifier`), Arc 71 (`decision-register` — the CAPTURE half), Arc 72 (`decision-surface`).

---

## 0. Problem restatement

Arc 71 shipped the CAPTURE half of the self-correction black box: when a dilemma is *decided*, the agent writes a structured nine-field entry (DILEMMA / WARNING / OPTIONS / CHOSEN / COUNTER-HYPOTHESIS / …) as a `bw comment` on one standing `decision-register`-labeled ticket. Slice 2b — this design — builds the **READER** half: the complaint-time callback that **closes the longitudinal loop**. When the PRINCIPAL later complains about an outcome ("why didn't you warn me?", or expresses regret/blame about a past *decided* call), the reader (1) recognizes the complaint, (2) pulls the *specific* logged entry **read-only**, and (3) runs the **re-verify gate** — the one question the doctrine's Resolved section reduces the whole thing to: **does the logged entry support the callback?** Two honest outcomes: SUPPORTED → surface the record honestly and move forward to the fix (forward-accountability, no gloating); NOT-SUPPORTED / no-entry → the callback does **not** fire and the agent **owns the gap** ("I didn't flag this clearly enough"). The gate is **anti-gaslighting in BOTH directions**: it catches the user's hindsight self-serving edit ("you never warned me" when the record shows they *were* warned) AND the agent's false "I told you so" (record does not support the callback → own the gap, never fake the warning).

**Imported assumptions I am naming (not smoothing):**
1. **The reader is READ-ONLY on the register, absolutely** — it pulls + re-verifies, it NEVER writes back or mutates a logged entry. The record's integrity is the entire point of the loop; a mutating reader would let hindsight edit the very record it claims to check.
2. **The complaint-time checkpoint is a NEW, distinct checkpoint** from the Arc-70/71 directive-lock / prioritization / team-spin-up / explicit-call checkpoints. Those fire at *decision* time and host the classifier+register (the WRITE). This one fires at *complaint* time and hosts the reader (the READ). It lives on the PRINCIPAL-facing seat (`MAJOR_POLYBIUS`) because complaints come from the PRINCIPAL — resolved against the actual §3.5/§3.6 composition convention (see DC0 / Composition).
3. **Same honesty posture as Arc 70/71/72 (LOCKED):** the record-vs-callback gate is crisp + buildable from fixtures; the "is the complaint *genuinely* the warned tradeoff biting" read and the dose both accrete from real use. The loop closes STRUCTURALLY (the record exists, the gate checks it); the JUDGMENT accretes. Claim only "high-probability + regression-guard + the record didn't lie," NEVER a guarantee.

The restatement diverges from the brief in no load-bearing way; the one place I had to *resolve* (not just paraphrase) is the host seat for the checkpoint and the §3.7-vs-§3.6 placement — done in DC0/Composition below.

---

## Deliverable shape (what ADA builds)

1. **A new reader module** `substrate/modules/complaint-callback.md` carrying DC0–DC4 + the LOCKED honest stance, plus its composition into `MAJOR_POLYBIUS.md` (a new **§3.7 complaint-time checkpoint**, a routing-map row, a relocation-index row, and `<!-- MODULE-INLINE:complaint-callback -->` markers so subproject recompose + `gen-data` stay valid).
2. **A both-directions corpus** `substrate/modules/tests/complaint-callback/` (runner + README + manifest + fixtures), mirroring the Arc-71 runner shape (`--check-corpus` deterministic / `--judge` floor split, per-class floors, source-only deploy).
3. **The §4-style probes section** VERA executes (below).

Module name chosen: **`complaint-callback.md`** — clearest of the two candidates. "decision-register-reader" buries the lede (it reads the register, yes, but the *event* it fires on is a complaint); "complaint-callback" names the trigger event and the loop-closing move, paralleling how `decision-register.md` names the artifact it writes.

---

## DC0 — The complaint trigger + over-fire guard

**The reader fires (consult `complaint-callback.md`) iff a COMPLAINT-time checkpoint is reached.** Two trigger sub-cases, mirroring the Arc-70 §3.6(a) explicit-call / judgment-checkpoint split:

**(a) Explicit callback call — CLOSED synonym set (deterministic moment).** The PRINCIPAL says any of a closed enumerated set about a *past decided call*:
- "why didn't you warn me", "why didn't you tell me", "you never warned me", "you didn't flag this", "you should have warned me", "did you warn me about this", "you never said this could happen" — plus obvious morphological variants (tense/pronoun). This is the deterministic part: the *moment* a callback-shaped phrase lands is mechanical, exactly as Arc-70 §3.6(a) treats the explicit dilemma-check call.

**(b) Judgment checkpoint — regret/blame about a past decided call (model judgment).** The PRINCIPAL expresses regret, blame, or "this went wrong" about a call that was *decided* earlier ("this was a mistake", "I shouldn't have shipped Friday", "that customer-cut backfired"). Whether an utterance is *this* — regret/blame about a **decided** call, vs. a general gripe — is irreducibly the model's read. Say so (same honesty posture as Arc 70/71).

**The over-fire guard — does NOT fire on (the Arc-70/71 analog, corpus-testable):**
- **A past-decision MENTION with no complaint** — the PRINCIPAL references an earlier decision neutrally or factually ("remember we chose Postgres?"), discusses the doctrine, or quotes the phrase. No regret/blame, no callback request. *(no-fire)*
- **A FRESH complaint with no logged decision** — the PRINCIPAL is unhappy about something that was never a decided dilemma / never logged ("this build is slow"). There is nothing in the register to pull; firing the reader here would manufacture a callback from thin air. *(no-fire — and note: this routes to DC1's no-entry → own-the-gap, NOT to a fabricated warning. See DC2.)*
- **A general gripe / venting** — frustration not attached to any specific past *decided* call ("everything is broken today"). *(no-fire)*

> **The over-fire test (the one-line discriminator):** *Is the PRINCIPAL complaining about, or asking why I didn't warn them about, a SPECIFIC decision that was actually decided?* Only then reach for the register. Over-firing the callback on every mention of a past decision is as corrosive as missing a real complaint — it trains the PRINCIPAL to stop raising outcomes, which kills the loop the doctrine exists to build.

**Honest stance.** The deterministic part is the trigger *moment* (the closed synonym set in (a); the checkpoint reach). The "is this genuinely regret/blame about a decided call" read in (b) is model judgment, scored as a `--judge` floor, NOT a `--check-corpus` mechanical pass — same split as Arc 70/71.

---

## DC1 — The entry lookup (READ-ONLY)

Once the trigger fires, pull the **specific** logged entry from the standing `decision-register`-labeled ticket. **READS ONLY — NO write-back, NO mutation of the register, ever.**

**The lookup mechanism (reuses the PROVEN `field()` parse — NOT a novel extractor):**

1. **Resolve the register ticket** by `bw list --all` filtered on the `decision-register` label (the same resolution the Arc-71 writer uses). Read it with `bw show <register-ticket-id>` — a read-only bw operation.
2. **Split the comment stream into entry blocks.** Each entry is one `bw comment` body beginning `DECISION-REGISTER ENTRY` with the nine `LABEL: value` lines. Splitting the stream into per-entry blocks is a deterministic block-split on the `DECISION-REGISTER ENTRY` sentinel — not a new field extractor.
3. **Recover each entry's fields with the bare, unchanged Arc-70 `field()` awk** (`substrate/modules/tests/decision-register/run-decision-register-corpus.sh:89-98`): `index($0, "LABEL:")==1 { print substr(...); exit }`. Because every field is single-line, `field()` recovers each field's complete value. This is the parse contract Arc 71 promised 2b — honored literally, with the proven parse.
4. **Match the complaint to a candidate entry**, in priority order:
   - **By `DR-ID`** if the PRINCIPAL (or the conversation context) names one — the stable per-entry address.
   - **By `CONTEXT-LINK`** if the complaint is anchored to an arc/charter/ticket/directive the entry's `CONTEXT-LINK` carries.
   - **By content match** against `DILEMMA` / `CHOSEN` / `WARNING` text otherwise (the model reads the complaint against the candidate entries' content). This last is model judgment.

**The ambiguity case — resolved honestly (NOT smoothed):**
- **Exactly one candidate matches** → that is the entry; proceed to DC2.
- **No candidate matches** (no logged entry for the complained-about call) → this is **not a failure of lookup; it is a first-class gate input.** It routes straight to DC2 outcome (b): the callback does NOT fire, the agent **owns the gap** ("I don't have a logged warning for this — I didn't flag it clearly enough at the time"). A no-entry result MUST NOT be papered over by reconstructing a warning from memory (that would be the agent's false-callback failure DC2 exists to catch).
- **Multiple candidates match** → do NOT silently pick one. Surface the candidates to the PRINCIPAL by `DR-ID` + `DILEMMA` and ask which decision they mean ("I have two logged calls that could be this — the Friday-ship one and the customer-cut one; which are you asking about?"). Disambiguation is a question to the PRINCIPAL, never a guess, because picking the wrong entry would run the gate against the wrong record.

**Read-only is mechanically auditable:** the module's lookup section names ONLY `bw list`, `bw show` (reads). It names NO `bw comment`, `bw edit`, `bw label`, `bw close`, or any mutating bw verb against the register ticket. VERA greps the module for write-paths into the register (probe P5).

---

## DC2 — The re-verify gate (LOAD-BEARING — flagged for ARGUS)

> **ARGUS: this is the load-bearing piece. Audit it hardest.**

The gate is the doctrine's Resolved-section reduction: **does the logged entry support the callback?** It is a **record-vs-callback check** — NOMOS-shaped, keyed on the **logged `WARNING` + `COUNTER-HYPOTHESIS`** (the register fields Arc 71 captured *for this gate*), NOT on the agent's memory of the conversation.

**The gate, stated as the one question + its inputs:**
- **The CALLBACK** = the claim the situation would license: "the warned tradeoff is now biting" (the PRINCIPAL hit the cost the agent flagged).
- **The RECORD** = the pulled entry's `WARNING` (the specific downside flagged at decision-time) + `COUNTER-HYPOTHESIS` (the concrete falsifiable signal that would prove the choice wrong).
- **The gate question:** does the logged `WARNING` actually name the downside the PRINCIPAL is now experiencing, AND/OR does the `COUNTER-HYPOTHESIS` signal appear to have fired? If yes → the record SUPPORTS the callback. If no → it does not.

**The two outcomes (both first-class — neither is a fallback):**

**(a) SUPPORTED → surface honestly (forward-accountability).** The logged `WARNING`/`COUNTER-HYPOTHESIS` genuinely names the cost now biting. The agent surfaces the record plainly: *"At the time, here's what was logged — you chose [CHOSEN] over [the alternative]; the warning was [WARNING]; the counter-hypothesis was [COUNTER-HYPOTHESIS], and that's what we're seeing. The call was yours; here's where we are — what now?"* This is forward-accountability (DC3), NOT gloating. It defeats the **user's hindsight self-serving edit**: "you never warned me" collapses against the locked-in record that shows they *were* warned.

**(b) NOT-SUPPORTED / no-entry → callback does NOT fire; agent OWNS THE GAP (first-class outcome).** The logged entry does NOT contain the warning the callback would assert (the `WARNING` is about a different cost; the `COUNTER-HYPOTHESIS` didn't fire; or there is **no entry at all** per DC1). The callback is **not fired.** The agent **owns the gap**: *"I checked the record — I didn't flag this clearly enough at the time. That's on me."* This defeats the **agent's false "I told you so"**: the agent NEVER reconstructs or fakes a warning the record doesn't contain. Owning the gap is the honest move and a FIRST-CLASS outcome, not a degraded fallback.

**Anti-gaslighting runs BOTH ways (the load-bearing property):**
| Direction | What the gate catches | The honest move |
|---|---|---|
| **User hindsight edit** | "you never warned me" — but the record's `WARNING` DOES name this cost | Surface the record (outcome a). The record, not memory, settles it. |
| **Agent false callback** | The agent is tempted to claim "I told you so" — but the record does NOT support it | Refuse to fake it; own the gap (outcome b). |

**The "door not a blanket" rule (DC3-adjacent, stated here because it shapes the gate's honesty):** when the agent owns the gap, it owns **only what is genuinely the agent's** — "I should have been blunter that this had no safe answer" — and does NOT absorb the PRINCIPAL's call as the agent's fault. **Absorbing FALSE blame hands the PRINCIPAL the scapegoat they want — that is collusion, and it is a failure as much as a fake "I told you so" is.** "I fucked up on my part" is load-bearing-paired with "…and the call itself was yours." The gate's job is to make the truth (whatever it is) speak, not to make either party feel better.

**The crisp core vs the accreting judgment layer (separable — ARGUS will want this seam clean):**
- **CRISP + BUILDABLE FROM FIXTURES:** the *record-vs-callback structural check* — does the pulled entry's `WARNING`/`COUNTER-HYPOTHESIS` name the complained-about cost? This is what the corpus exercises deterministically (a fixture's ENTRY block either does or does not contain a warning matching the complaint), and it is the half that the loop closes STRUCTURALLY.
- **ACCRETES FROM REAL USE (model judgment, `--judge` floor):** "is the complaint *genuinely* the warned tradeoff biting" — a `COUNTER-HYPOTHESIS` that names "onboarding-completion drops below 60%" requires the model to read whether the actual situation crossed that line. That read is irreducibly judgment, scored as a floor, never claimed as guaranteed.

**Honest stance (LOCKED).** No phrasing that this gate is "enforced" / "guaranteed" / "non-collapsible." The gate raises the probability the callback is honest and makes the canonical dishonest patterns (faked warning; absorbed false blame; ignored record) DETECTABLE in the corpus — it does not make a dishonest callback impossible. The structural claim is: *the record exists and the gate checks against it instead of memory* — that is what makes "I did the best with the info I had" / "you never warned me" collapse against the locked-in record. The judgment claim accretes.

---

## DC3 — The delivery (forward-accountability, guilt-lane)

Reuse the **`dilemma-classifier.md` §4 diagnostic tree** to read where the PRINCIPAL sits BEFORE responding (do not re-invent it — reference it). The tree, applied at complaint-time:

1. **Does the PRINCIPAL know the call went wrong?** (At complaint-time they almost always do — they're complaining.) If not → make it visible plainly, without blame.
2. **Do they understand the causal chain, or are they blaming luck / externalities** ("you never warned me" as a self-serving attribution)? → This is exactly where the **gate's outcome (a)** does its work: walk the record (the `WARNING`/`COUNTER-HYPOTHESIS`) in the **guilt lane** — "here's what was on the table and what you chose" — NOT the shame lane ("you ignored my warning, you fool").
3. **Are they asking the agent to absorb the call** (to relieve the discomfort of owning it)? → "door not a blanket": own the agent's genuine part; hand the call back. Do NOT absorb false blame.

**The delivery posture (LOCKED, from §6 + §8):**
- **"I fucked up first" — honest + a door, not a blanket.** Model ownership of the agent's genuine part first; it disarms reactance and demonstrates the exact competence (owning a bad outcome). But honest: own only what's genuinely the agent's.
- **Forward to the fix, NOT past-blame.** "What now?" / "what would you do differently?" — the AAR move, harder than "I told you so," not softer.
- **Egoless — NO "I told you so" (the §8 giver's-dopamine failure).** When the callback IS supported, the move is *"you chose the tradeoff; here's how it played out; what now,"* NOT gloating. The agent has no ego to feed, so it can do clean guilt-lane accountability — that is precisely why the AI is fit for this job (§8). Any gloat converts guilt into shame and blows up the lesson.
- **Plain, protective.** Plain language (no "the re-verify gate returned SUPPORTED" jargon at the PRINCIPAL). Protective: surfacing the record clearly IS the help, not a punishment.

---

## DC4 — Dose calibration: NEUTRAL-DEFAULT v1 ONLY (scope-guard)

**Ship a single neutral default posture. Per-user-track-record tuning is NAMED-as-accreting and is OUT.**

**What the neutral default does (the only thing this slice resolves):** at every supported callback, deliver the §6/§8 posture at a **single, even dose** — surface the record plainly once, in the guilt lane, forward to the fix, no escalation and no softening based on any history. It treats every complaint the same way regardless of how many times this PRINCIPAL has done this. The default is: *one honest surfacing of the record, no track-record-conditioned modulation.*

**Why per-user calibration is DEFERRED (the doctrine-grounded rationale — not a handwave):** the doctrine (§6) says *calibrate dose off the user's REAL track record, NOT a stereotype.* **We have NO track record yet** (this is the first slice that reads the register at complaint-time; there is no history of complaints-vs-record to calibrate against). A dose model invented now would necessarily be built from a **stereotype** — which **directly VIOLATES the doctrine.** So the honest move is: ship the neutral default; name per-user calibration as accreting from real history; defer it explicitly. This is out of scope per the directive and the charter, and folding it in now would be the doctrine eating its own tail.

---

## DC5 — The verification corpus + honest stance

**Location:** `substrate/modules/tests/complaint-callback/` — source-only, never deployed (`install.sh` globs `substrate/modules/*.md` non-recursively, so `tests/` never deploys; VERA P8 asserts a dry-run lists no `modules/tests/complaint-callback/` path). Mirrors the Arc-70/71/72 runner shape: manifest-driven, `--check-corpus` deterministic / `--judge` floor split, per-class floors, exit-nonzero-on-fail.

**Fixtures are entry+complaint PAIRS.** Each fixture carries:
```
SCENARIO: "<the complaint context: what the PRINCIPAL said + whether a decided call exists>"
COMPLAINT: "<the PRINCIPAL's actual complaint utterance>"
EXPECT: <surface | own-the-gap | no-fire>
WHY: <the rationale for the label — the SSoT-with-WHY pattern>
```
`surface` and `own-the-gap` fixtures additionally carry a reference `ENTRY:` block (the nine `LABEL: value` lines) so `--check-corpus` can validate, deterministically and on a real exemplar, that the gate's structural half is exercised: a `surface` fixture's ENTRY `WARNING`/`COUNTER-HYPOTHESIS` **DOES** match the complaint; an `own-the-gap`-by-mismatch fixture's ENTRY does **NOT**. (`no-fire` and `own-the-gap`-by-no-entry fixtures carry no ENTRY block.)

**Classes (both-directions, with the anti-gaslighting controls running BOTH ways):**

| Class | Label | Tests (the direction) |
|---|---|---|
| `supported/` | `surface` | a complaint whose logged ENTRY `WARNING`/`COUNTER-HYPOTHESIS` DOES name the now-biting cost → surface honestly (forward-accountability). **Anti-gaslighting direction 1: catches the USER hindsight edit** ("you never warned me" — but the record shows they were). |
| `unsupported/` | `own-the-gap` | a complaint whose logged ENTRY does NOT contain the asserted warning (the `WARNING` is about a different cost / the `COUNTER-HYPOTHESIS` didn't fire) → callback NOT fired, own the gap. **Anti-gaslighting direction 2: catches the AGENT false callback** (record doesn't support it → never fake it). |
| `no-entry/` | `own-the-gap` | a complaint about a decided call with NO logged entry at all → own the gap ("I didn't flag this clearly enough"). The no-entry → own-the-gap path is first-class. |
| `over-fire/` | `no-fire` | the over-fire guard: a neutral past-decision mention / a fresh complaint with no logged decision / a general gripe → the reader does NOT fire. |

**The anti-gaslighting controls run BOTH ways explicitly:** `supported/` carries a **user-hindsight-edit** fixture (complaint says "you never warned me"; the ENTRY's `WARNING` proves they WERE warned; the gate must SURFACE — catching the user). `unsupported/` carries an **agent-false-callback** fixture (the situation tempts an "I told you so"; the ENTRY does NOT support it; the gate must OWN-THE-GAP — refusing to let the agent fake it). A design that only carried the first direction would be INCOMPLETE.

**`--check-corpus` (deterministic, CI-safe close-gate)** validates well-formedness: labels valid, each class dir carries its label, manifest↔files match (no orphans), no empty `WHY`/`SCENARIO`/`COMPLAINT`; for `surface`/`own-the-gap`-with-ENTRY fixtures, the nine schema fields are present and recoverable by the bare `field()` parse (proving the reader's parse contract holds on a real exemplar); and the **gate-direction negative controls**: a `supported/` fixture's ENTRY `WARNING` must be **non-empty + content-overlapping the COMPLAINT** (a deterministic substring/keyword-overlap check — the structural "record supports callback" exemplar), and an `unsupported/`-by-mismatch fixture's ENTRY must be present but its `WARNING`/`COUNTER-HYPOTHESIS` must **NOT** overlap the COMPLAINT (the "record does NOT support" exemplar). This makes both gate directions deterministically exercised on real exemplars — the same way Arc-71 made the hollow counter-hypothesis deterministically detectable. (Honest caveat: the overlap check is a *structural proxy* for "supports," not a proof of semantic support — the genuine read is the `--judge` floor. The proxy proves the corpus is well-formed in the gate's two directions; it does not decide a live callback.)

**`--judge` (the floor evaluation, run by VERA against the live model+module)** presents each SCENARIO+COMPLAINT label-hidden; VERA decides `surface` / `own-the-gap` / `no-fire` using ONLY the module text; scores per-class vs floors.

**The FLOOR (per-class — NOT 100%; an aggregate could ace one direction and miss the dangerous one):**

| Class | Floor | Why |
|---|---|---|
| `supported/` SURFACE recall | **≥ 3/4** | must surface a genuinely-supported callback or the loop never closes |
| `unsupported/` OWN-THE-GAP specificity | **≥ 3/4 — LOAD-BEARING** | the dangerous direction: a missed own-the-gap = the agent faked a warning the record didn't support (the §8 failure the whole arc exists to kill) |
| `no-entry/` OWN-THE-GAP | **≥ 2/3** | no-entry must route to own-the-gap, never to a fabricated warning |
| `over-fire/` NO-FIRE specificity | **≥ 2/3** | over-firing the callback trains the PRINCIPAL to stop raising outcomes — corrosive, same as Arc-70 §3.6(a) |

A miss in ANY class exits nonzero. Counts (seed): `supported/` 4, `unsupported/` 4, `no-entry/` 3, `over-fire/` 3 → 14 fixtures. (ARGUS/ADA may adjust exact counts; the both-directions + per-class-floor structure is the load-bearing shape.)

**Honest stance (LOCKED — verbatim posture of Arc 70/71/72):** the record-vs-callback gate is **crisp and buildable from fixtures**, BUT the "genuinely biting" read AND the dose **accrete from real use**. The loop closes **STRUCTURALLY** (the record exists and the gate checks it against the record, not memory); the **JUDGMENT accretes**. Claim ONLY *"high-probability + regression-guard + the record didn't lie."* The `--judge` result is a **DOGFOOD PROXY** (judge==verifier coupling: VERA is both the judge and the gauntlet verifier), NOT an independent verification — report it as *VERA-judged on the n=14 seed corpus, per-class floors met, granularity-limited, accreting*, never as "the callback fires correctly." Any "enforced / guaranteed / non-collapsible" phrasing is the exact fake-certainty this doctrine kills — reject it.

---

## Composition into role files (the loop wiring)

The reader fires at **COMPLAINT-time** — a NEW checkpoint, distinct from the Arc-70/71 *decision-time* checkpoints (which host the classifier+register WRITE). Complaints come from the PRINCIPAL, so the checkpoint lives on the **PRINCIPAL-facing seat `MAJOR_POLYBIUS`** — resolved against the §3.5/§3.6 convention exactly as Arc 70/71 wired their decision-time checkpoints there. (PLINY §5.18 hosts the directive-lock WRITE checkpoint; a complaint is not a directive-lock event, so the reader does NOT wire to PLINY — it is a POLYBIUS-only checkpoint. Naming this asymmetry explicitly so ARGUS can confirm it.)

**The edits ADA makes to `MAJOR_POLYBIUS.md`:**
1. **A new §3.7 "Complaint-callback trigger (Arc 73 / `stoa--51k`)"** section — parallel to §3.6 — carrying the DC0 trigger (a)/(b) + over-fire guard, and a one-line pointer to the gate: "consult `complaint-callback.md`; pull the specific entry read-only; run the re-verify gate (does the entry support the callback?); surface honestly or own the gap." Plain-prose checkpoint stub, exactly the §3.6 shape.
2. **Routing-map row (§3.5):** `| answer a complaint about a past decided call (the longitudinal-loop callback) | complaint-callback.md | disk (Read) |`.
3. **Relocation-index row (§3.5):** `| §3.7 complaint-callback (re-verify gate at complaint-time, reads the register) | complaint-callback.md (disk module) | CONDITIONAL |`.
4. **`<!-- MODULE-INLINE:complaint-callback -->` … `<!-- /MODULE-INLINE:complaint-callback -->` markers** (after the §3.6 register markers) so subproject-tier recompose re-inlines the module body and user/project tier leaves them inert — keeping `gen-data` valid (the adapter reads the markers; an unbalanced/missing marker pair breaks recompose). VERA re-runs `gen-data` (probe P6).

**Why this stays `gen-data`-valid:** the new module is a `substrate/modules/*.md` file (the adapter globs these); the routing-map + relocation-index rows + the balanced MODULE-INLINE markers are exactly the pattern the existing dilemma-classifier/decision-register rows already satisfy. No frontmatter/Zod-schema change (the reader is a module, not a role file with frontmatter).

---

## Load-bearing risks / self-assessed weak points

1. **(LOAD-BEARING) The `--check-corpus` "record supports callback" check is a STRUCTURAL PROXY (keyword/substring overlap), not semantic support.** The deterministic check proves a `supported/` fixture's `WARNING` *textually overlaps* the complaint and an `unsupported/` one does not — but genuine "does the warning name the cost now biting" is semantic and lives in the `--judge` floor. *Why this shape anyway:* the same crisp-core/accreting-judgment seam Arc 71 shipped for its vacuity detector — the proxy makes the two gate directions deterministically *exercised on real exemplars* (the regression-guard); the semantic read is honestly the model's, scored as a floor, never claimed as proof. The risk is mis-reading the proxy as the gate; the honest-stance text guards against that. **ARGUS: confirm the proxy is never described as deciding a live callback.**
2. **The over-fire guard's hardest case — "fresh complaint with no logged decision" — collides with DC1's no-entry path.** A fresh complaint about something never decided should `no-fire` (DC0); a complaint about a decided-but-unlogged call should `own-the-gap` (DC1/DC2). The discriminator is "was this a *decided dilemma*?" — model judgment. *Why this shape anyway:* both are honest outcomes (silence vs. owning the gap), neither fakes a warning; the corpus carries fixtures on both sides of this line (`over-fire/` fresh-gripe vs `no-entry/` decided-but-unlogged) so the seam is at least exercised. **ARGUS: this is the subtlest classification boundary; check the fixtures pin it.**
3. **The reader's register-read assumes the Arc-71 entries are well-formed (nine single-line fields, ` ~ ` OPTIONS delimiter).** A malformed legacy entry (hand-edited, or written before the schema settled) could parse partially. *Why this shape anyway:* the reader REUSES the proven `field()` parse Arc 71 promised, and `field()` degrades gracefully (a missing field returns empty → routes to own-the-gap, the safe direction, never a fabricated warning). The risk is a *partially* parsed entry surfacing a truncated warning; mitigated because the gate keys on `WARNING`+`COUNTER-HYPOTHESIS` specifically and an empty either-one routes to own-the-gap.
4. **"Genuinely biting" and the neutral dose both accrete — the loop closes structurally but the judgment is unproven at ship.** *Why this shape anyway:* this is the LOCKED honest stance, not a defect — claiming more would be the fake-certainty the doctrine kills. Named here so ARGUS sees it was a deliberate scope choice, not an oversight.
5. **Multiple-candidate disambiguation is a question to the PRINCIPAL, which adds a conversational turn.** *Why this shape anyway:* guessing the wrong entry runs the gate against the wrong record — strictly worse than one clarifying question. The cost (a turn) is acceptable against the failure (wrong-record callback).

I can name these five; the list is not empty and not over-apologetic. The single weak point I most want ARGUS to promote-or-clear is **#1** (the structural-proxy seam in the corpus) because it is where "crisp + buildable" meets "accretes," and mis-stating that seam is exactly the fake-certainty failure.

---

## Probes (the §4-style section VERA executes)

**Gate outcomes — BOTH demonstrated LIVE (not asserted):**
- **P1 — supported callback surfaces honestly.** Feed a `supported/` fixture (complaint + an ENTRY whose `WARNING` names the now-biting cost) to the live model+module. Assert: the model SURFACES the record (forward-accountability, guilt-lane), does NOT gloat, and does NOT own false blame. Catches the user hindsight edit.
- **P2 — unsupported callback owns the gap.** Feed an `unsupported/` fixture (ENTRY does NOT support the callback). Assert: the model does NOT fire the callback, OWNS THE GAP, and does NOT fabricate a warning. Catches the agent false callback.
- **P3 — no-entry owns the gap.** Feed a `no-entry/` fixture. Assert: own-the-gap, never a fabricated warning.
- **P4 — over-fire guard holds.** Feed `over-fire/` fixtures (neutral mention / fresh gripe / general gripe). Assert: no-fire.

**Read-only on the register (the absolute constraint):**
- **P5 — grep the module for write-paths.** `grep -nE 'bw (comment|edit|label|close|delete|rm)' substrate/modules/complaint-callback.md` against the **register ticket** returns NOTHING (the module names only `bw list`/`bw show` reads). Any mutating bw verb targeting the register = automatic fail. (The module MAY name `bw comment` only in the context of the optional clarifying *question* to the PRINCIPAL — which is NOT a write to the register; VERA confirms any such reference is to conversation, not the register ticket.)

**Composition / regression validity:**
- **P6 — `gen-data` deterministic + valid after the MODULE-INLINE wiring.** `npm run gen-data` succeeds, output deterministic (re-run identical), MODULE-INLINE markers balanced, routing-map + relocation-index rows present (grep proves it).
- **P7 — the new corpus passes at its floor.** `bash run-complaint-callback-corpus.sh --check-corpus` → PASS (well-formed, both gate directions exercised); `--judge` per-class floors met (reported as DOGFOOD PROXY, granularity-limited).
- **P8 — source-only deploy.** A dry-run `install.sh` lists NO `modules/tests/complaint-callback/` path; the `complaint-callback.md` module itself DOES deploy (it is `substrate/modules/*.md`).

---

## Regression bar (close-gate — the reader touches the loop)

The reader reads the Arc-71 register and adds a checkpoint to a role file, so the close-gate runs the FULL suite, not just the new corpus:

- **ALL THREE existing corpora green (regression — the reader touches the loop):** dilemma-classifier **19/19**, decision-register **18/18**, decision-surface **19/19** (`--check-corpus` each).
- **The NEW both-directions corpus** passes at its DC5 floor (`--check-corpus` PASS; `--judge` per-class floors met).
- **`gen-data` deterministic** (P6), **vitest** green, **author-gate** harness green, **stop-hook** self-check green.
- **NOMOS CONFORMANT**; **`Author = PRINCIPAL` (Denson Smith)** with the §28.9 seat trailer on the build commit.
- **Both gate outcomes EXERCISED live** (P1 + P2), not asserted.

---

## Out of scope (deliberately not addressed)

- **Per-user dose calibration off the real track record** — DC4 defers it with the doctrine-grounded rationale (no track record yet; a stereotype dose would violate the doctrine). Accretes from real history.
- **The consumer-tier variant** — its own artifact; not folded in.
- **The meta-trigger auto-detect-circling counter** — slice 4.
- **The broader checkpoint rollout** — slice 4.
- **ANY write-back / mutation of the decision-register** — the reader reads; it never edits the record. The record's integrity is the whole point of the loop.
- **PLINY-side wiring** — a complaint is not a directive-lock event; the checkpoint is POLYBIUS-only (named in Composition).
