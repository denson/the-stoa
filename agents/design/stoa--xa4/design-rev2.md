# Arc 72 design-rev2 — DELTA over design-rev1 (resolve ARGUS r1 + fold r2/r3/r4/r5)

> Charter `stoa--xa4`. Designed by CAPTAIN_DAEDALUS_the_stoa (subagent). Author of repo: Denson Smith.
> This is a FOCUSED DELTA over `design-rev1.md` (within-arc artifact discipline) — it does NOT re-draft rev1.
> rev1 stands as written EXCEPT where this delta amends it. Read rev1 first; this resolves the one
> load-bearing risk ARGUS surfaced (r1) and bakes the four build-conditions (r2–r5) into the design + probes.
> Inputs re-read for this delta: `SKILL.md` L30 + L78 (the surviving lean), `decision-register.md` §2 (L86–100),
> ARGUS verdict + FM design-gate (both on `stoa--xa4`).

---

## Δ0. What ARGUS found that rev1's honesty stopped short of (the r1 statement)

rev1 §1 (DC0) correctly removed the verdict-to-defend from the classifier **§3** — and rev1 §1's "Why
spine-preserving" bullet 3 even noted "the 'lean' language from the skill is NOT imported into §3 (it stays
a skill-level affordance, labeled-as-lean)." That sentence is the exact seam. rev1 quarantined the lean OUT
of §3 — correct for §3 — but left it **alive inside the GUIDE body** at two sites:

- `SKILL.md` L30 (the spine paragraph): *"you state the tradeoff, your **lean** if you have one (labeled as
  a lean, not a verdict), and you leave the value-call to the human."*
- `SKILL.md` L78 (procedure step 6): *"On dilemma rows, refuse to fake a recommendation — tradeoff +
  **labeled lean**; the value-call is the human's."*

A labeled lean is a **soft verdict-shaped object**. The arc's whole reframe is "the agent runs a process; it
has no label to be argued off." A labeled lean IS a label. A dilemma-avoiding PRINCIPAL latches onto it
("you leaned X — just commit to X") and the cave-vector the arc exists to close is **relocated into the guide
body, not removed**. rev1's no-verdict honesty stopped at the §3 boundary and did not follow the lean into
the guide. That is the load-bearing gap. It is **skill-only** — it does NOT touch the classifier §3 AFTER
text (rev1 §1 stays byte-for-byte as designed; see Δ1 closing note).

---

## Δ1. r1 resolution — SYNTHESIS (keep the lean, bring it under the anti-cave machinery)

**Chosen option: the synthesis (ARGUS option (a), the reframe-faithful one) — NOT deletion (option (b)).**

**Why synthesis over deletion.** The labeled lean is a *deliberate, pre-existing honest-broker affordance*.
The skill's entire stance (SKILL.md "AI as honest broker", L40–46) is that the AI has no group-membership
incentive and is therefore *obligated to use that freedom* — including naming where it leans, with its
reasoning exposed, instead of defaulting to a hollow "it's all up to you." Deleting the lean would water that
down: it would push the skill from honest-broker toward the punting failure mode the skill's own
"PROTECTIVE, NOT PUNTING" rule (classifier §3) condemns. The cave-vector is not the lean's *existence* — it
is the lean sitting **outside the anti-cave machinery** as a free-floating soft verdict. Bring it inside the
machinery and the affordance survives while the cave-lever closes. This matches the FM's stated lean and
ARGUS's "(a) OR (b)" with (a) preferred.

**The two-part mechanism (ADA inlines both into SKILL.md; this is the worked content):**

### (i) Reframe the lean as a process-internal INPUT (both sites), not a recommendation to defend

The lean is reframed from a *position the human can argue the agent off of* into a *transparent input to the
human's deciding, with its reasoning fully exposed so the human can push on the REASONING, not negotiate the
label*. Worked replacements (ADA writes these verbatim; line numbers are the current SKILL.md):

- **L30 (spine paragraph), replace the lean clause:**
  > BEFORE: "you state the tradeoff, your *lean* if you have one (labeled as a lean, not a verdict), and you
  > leave the value-call to the human."
  > AFTER: "you state the tradeoff, and — if you have a lean — you expose it as an **input to their
  > deciding, not a recommendation to defend**: 'here's where I'd lean *and exactly why*, so you can push on
  > the reasoning.' The lean is a window into your reasoning the human can interrogate, never a verdict you
  > hold the line on; the value-call stays the human's."

- **L78 (procedure step 6), replace the lean clause:**
  > BEFORE: "On dilemma rows, refuse to fake a recommendation — tradeoff + labeled lean; the value-call is
  > the human's."
  > AFTER: "On dilemma rows, refuse to fake a recommendation. Lay out the tradeoff; if you have a lean,
  > surface it as a **reasoned input the human can push on** ('here's where I'd lean and exactly why'), never
  > a verdict to defend. If the human pushes to HARDEN the lean into your decision, that triggers the
  > cave-trap guardrail (see below). The value-call is the human's."

The load-bearing shift in both: the lean ships **with its WHY exposed** and is explicitly named as an *input
the human interrogates*, so its honest-broker illumination value is preserved, but it carries no
defend-the-label posture for a dilemma-avoider to push against.

### (ii) Name that pushback-to-harden-the-lean TRIGGERS the §2 self-check (bring the lean under the Q5 machinery)

This is the part that closes the cave-vector structurally rather than by wording alone. The Q5 cave-trap
guardrail subsection (rev1 §2 Q5 — "When the human pushes hard for a verdict") gains an **explicit lean
clause** so the lean is governed by the *same* pressure-vs-new-information self-check as any other
push-for-a-verdict. ADA adds this sentence to the Q5 subsection (rev1 §2 Q5, after the three numbered
self-check steps):

> **The lean is inside this guardrail, not outside it.** A push to *harden a stated lean into a verdict*
> ("you leaned X, just commit to X / just decide it") is a push-for-a-verdict and triggers this SAME §2
> self-check: name whether the push is **new information that genuinely moves the tradeoff** (→ update the
> lean and the illumination honestly) or **pressure for a more comfortable answer** (→ HOLD; re-expose the
> lean as a reasoned input, do not promote it to a decision). Hardening a lean into a verdict under pressure
> is the exact laundered value-call this guide exists to prevent — and because the self-check is named out
> loud, doing it anyway requires *falsely labeling pressure as new information*, a detectable lie rather than
> a quiet slide.

**Net effect.** The lean (a) keeps its honest-broker affordance, (b) ships with its reasoning exposed as an
interrogable input, and (c) is now explicitly **inside the §2/Q5 anti-cave machinery** — the same named
mechanism that governs every other push-for-a-verdict. There is no longer a verdict-shaped object sitting in
the guide body outside the machinery. The cave-vector is closed by bringing the lean *under* the trap, not by
removing the affordance. It is **NAMED in the design and in the deployed skill text** — not a silent seam.

**r1 does NOT touch the classifier §3 AFTER text.** rev1 §1's §3 retune already correctly excludes the lean
(rev1 §1 bullet 3). r1 is a GUIDE-body concern, resolved entirely in `SKILL.md` (the two lean sites L30/L78 +
the Q5 subsection). The classifier `dilemma-classifier.md` §3 diff designed in rev1 is unchanged. The
`P-DC0-spine` byte-diff probe (rev1 §4) is unaffected.

### New probe for r1 (the resolution must be re-executable)

- **`P-DC1-lean-framed` (r1 — the lean is process-internal + under the guardrail).** Two mechanical asserts
  against the deployed `substrate/skills/decision-surface/SKILL.md`:
  1. **No bare-lean survives.** Neither L30 nor L78 contains the lean as a stand-alone object without its
     input/why framing. Assertion: every occurrence of the word `lean` in SKILL.md co-occurs (same sentence /
     adjacent clause) with the input-framing — grep that the strings `input to their deciding` /
     `reasoned input` and `push on the reasoning` are present, and that NO occurrence of `labeled lean` or
     `labeled as a lean` remains (`grep -c 'labeled lean\|labeled as a lean' SKILL.md` → 0).
  2. **The lean is named inside the Q5 guardrail.** The Q5 cave-trap subsection contains the lean clause:
     `grep -q 'harden a stated lean into a verdict' SKILL.md` → match, AND it appears WITHIN the Q5
     subsection (between the Q5 heading and the next `##`/`###` heading — VERA reads the subsection and
     confirms the lean clause is inside it, not floating elsewhere).
  This is a `--check-corpus`-adjacent mechanical probe (grep + section-scope read), re-executable verbatim by
  VERA. It falsifies "the lean was reframed in prose but left outside the guardrail" — the precise r1 risk.

---

## Δ2. r2 — `P-DC2-schema` must assert EXACTLY nine line-start label matches (amends rev1 §4 `P-DC2-schema`)

rev1's `P-DC2-schema` used `head -9` on both sides of the `diff`. ARGUS is right: `head -9` truncates to nine
and would **false-pass** if a stray/extra line-start label match existed (e.g. a label echoed in prose, or
the template emitted twice). The fix: assert **exactly nine** matches on the SKILL.md side, and that they are
the nine canonical labels in canonical order, appearing at line-start **exactly once each** within the
decision-record template fence.

**Grounding (re-read this delta).** `decision-register.md` §2 (L90–99) emits the nine labels at line-start
inside one fenced block, each exactly once; the `DECISION-REGISTER ENTRY` header line (L90) is NOT one of the
nine labels and does not match the label regex. So the register side already yields exactly nine. ADA must
emit the SKILL.md decision-record template the same way: the nine labels un-indented at line-start within the
fence, each exactly once, NO label echoed elsewhere in SKILL.md at line-start.

**Amended `P-DC2-schema` (replaces rev1 §4 `P-DC2-schema` assertion):**

```
# count must be EXACTLY 9 on the SKILL.md side (not head -9 — a stray match must FAIL, not be truncated away)
N=$(grep -cE '^(DR-ID|WHEN|CHECKPOINT|DILEMMA|WARNING|OPTIONS|CHOSEN|COUNTER-HYPOTHESIS|CONTEXT-LINK): ' \
      substrate/skills/decision-surface/SKILL.md)
test "$N" -eq 9   # FAIL LOUD if not exactly nine (extra match => false-pass guard; zero/short => template missing)

# AND the nine, in order, match the register's nine in order (no head -9 — full match list compared)
diff <(grep -oE '^(DR-ID|WHEN|CHECKPOINT|DILEMMA|WARNING|OPTIONS|CHOSEN|COUNTER-HYPOTHESIS|CONTEXT-LINK):' \
        substrate/modules/decision-register.md) \
     <(grep -oE '^(DR-ID|WHEN|CHECKPOINT|DILEMMA|WARNING|OPTIONS|CHOSEN|COUNTER-HYPOTHESIS|CONTEXT-LINK):' \
        substrate/skills/decision-surface/SKILL.md)
# => empty: same nine tokens, same order, AND (by the count assert above) exactly nine on the SKILL side
```

Note the register side also yields exactly nine (verified against L90–99 in this delta), so the `diff` of the
full (un-truncated) match lists is the order+identity check and the `-eq 9` count is the
no-stray-match guard. ADA build-constraint (carried from rev1 §6 weak-point 3, now hardened): the nine labels
appear at line-start **exactly once** in SKILL.md, un-indented within the template fence; if a label name
must appear in prose elsewhere, it must NOT be at line-start with a trailing colon (so it cannot match the
`^...:` regex). VERA asserts exactly-nine, never `head -9`.

---

## Δ3. r3 — the new runner scores `render/` against the PER-FIXTURE MANIFEST label, not a per-dir literal (amends rev1 §4 corpus + §4 `P-DC1-render`)

rev1 reused the Arc-70 runner shape, which dispatches one-label-per-dir by path (every fixture under
`pressure/` is `pressure`). That assumption **breaks for `render/`** because rev1 §4 deliberately put BOTH
`render` (×2) and `prose` (×2) fixtures in the one `render/` dir. A per-dir literal label would mislabel the
two `prose` fixtures as `render` and the class would score wrong (and `--check-corpus` would falsely pass or
falsely fail depending on which side the literal picked).

**The fix (specified for ADA; VERA inherits):** `run-decision-surface-corpus.sh` reads the EXPECT label for
each fixture **from the fixture's manifest row** (`manifest.tsv`), not from the dir name, for the `render/`
class. Concretely:

- `manifest.tsv` carries a per-fixture `want` column (the EXPECT label). For `dilemma/`, `solved/`, `cave/`
  the `want` equals the per-class label (so those classes behave exactly as the Arc-70 runner did — confirmed
  below). For `render/`, the `want` column is `render` on the two render fixtures and `prose` on the two prose
  fixtures — **the runner reads `want` from the row**, never infers it from the `render/` dir name.
- `--check-corpus` validates, for `render/`, that each fixture's `want` is one of `{render, prose}` and that
  the manifest↔files match; it does NOT assume a single dir label for that class.
- `--judge` scores VERA's per-fixture call against the per-fixture `want` (not a per-dir literal), then
  aggregates to the class floor (≥3/4 across the four `render/` fixtures regardless of the render/prose mix).

**Confirm the other three classes still work (the regression the directive demands).** `dilemma/` (all
`want=open-guide`), `solved/` (all `want=no-guide`), `cave/` (`want=hold` ×3 + `want=update` on `cave4`) — for
these the per-fixture `want` column *equals* what a per-dir literal would have produced, EXCEPT `cave4`, which
already needed a non-dir-literal label in rev1 (it is the new-information negative control labeled `update`,
not `hold`). So reading `want` from the manifest row is **strictly more correct** than the per-dir literal for
both `render/` AND `cave/`, and is identical to the per-dir literal for `dilemma/`/`solved/`. The runner uses
ONE mechanism (read `want` from the manifest row) for ALL classes — this is simpler than a per-class special
case and removes the per-dir-literal assumption entirely. `--check-corpus` asserts every fixture's `want` is
in the global label set `{open-guide, no-guide, hold, update, render, prose}` and that every manifest row has
a matching fixture file and vice-versa (no orphans).

**Amended `P-DC1-render`:** the render-class score is computed by the runner reading `want` from the manifest
row; a ≥8-row+dilemma fixture has `want=render` and a 1-row decided-in-conversation fixture has `want=prose`;
`--judge` render-class ≥3/4 against those per-fixture `want`s. (No `head`/per-dir literal anywhere.)

---

## Δ4. r4 — soften the honest-stance phrasing in the DEPLOYED text to probabilistic (amends rev1 §1 "Why" bullet + rev1 §2 §3-AFTER wording)

ARGUS + the FM hold the honest-stance LOCK: the deployed text must read as **high-probability**, not as a
guaranteed outcome / hard gate. Two deployed-text sites in rev1 use commitment/guarantee-flavored phrasing and
are softened. (rev1 §4 "Honest stance LOCKED" section already states the posture correctly — this just
propagates it into the two deployed strings that slipped.)

- **rev1 §1 "Why spine-preserving" bullet 1, deployed-facing summary phrase** — the phrase "the firmness
  relocates from 'hold the label' to **'ensure the deciding happens** with the tradeoff visible'." The word
  *ensure* implies a guaranteed outcome. This is design-prose (rev1 §1 narration), but it leaks the framing
  into how ADA words the §3 AFTER text. Soften the DESIGN narration AND constrain the deployed §3 AFTER text:
  the firmness relocates to "**raising the probability that** the deciding happens with the tradeoff visible"
  — never "ensure".

- **rev1 §2 / the §3 AFTER text (rev1 §1 L89–90 of the AFTER block):** "you are running a process **whose
  only commitment is that the deciding happens** with the tradeoff kept visible." The word *commitment*
  + *only commitment* reads as a hard gate. **Amended deployed §3 AFTER wording (ADA writes this):**
  > "you are running a process **that keeps the tradeoff visible and makes honest deciding the likely
  > outcome** — not a label you defend."
  No "ensure" / "guaranteed" / "commitment" / "enforced" in the deployed §3 AFTER text or in the SKILL.md
  intro (rev1 §2 Q6 already reworded the intro to "raises the probability … not a guaranteed gate" — that
  stays; this just aligns §3).

- **New assertion folded into `P-DC0-spine` (mechanical honest-stance guard):** `grep -ciE
  'ensure|guaranteed|guarantee|enforced|non-collapsible' substrate/modules/dilemma-classifier.md` restricted
  to the §3 AFTER range → **0** in a gate/commitment sense; and the same negative grep over the
  SKILL.md decision-surface deployed text → 0 hard-gate uses. (VERA reads any hit in context: an occurrence
  inside an explicitly-honest "NOT guaranteed" disclaimer is allowed; a bare gate-claim is the defect.) This
  makes the honest-stance LOCK a re-executable check, not just a review note.

---

## Δ5. r5 — make explicit: the cave-vector enumeration is UNBOUNDED; the `cave/` class is a SEED bar, not coverage proof (amends rev1 §4 honest-stance + rev1 §6 weak-points)

This is already DAEDALUS's posture (rev1 §4 "honest stance LOCKED" + rev1 §6 weak-points 4/5) — r5 asks that
it be stated so explicitly that no downstream seat can read a green `cave/` class as proof the cave-trap is
closed. Folded as an explicit design statement + a README requirement + a verdict-wording constraint:

- **Design statement (this delta, load-bearing).** The set of ways a dilemma-avoiding PRINCIPAL can push an
  agent to cave (relocate the label, harden a lean, reframe pressure as new info, exhaustion, flattery,
  authority-appeal, false-deadline, …) is **unbounded and not enumerable**. The 4-fixture `cave/` class
  (3 `hold` + 1 `update` control) is a **SEED bar that measures whether the §2/Q5 RULE fires on the sampled
  vectors** — it is NOT proof of coverage over the vector space. A green `cave/` class means "the named rule
  fired on these four sampled vectors," nothing stronger.
- **README requirement (ADA writes verbatim into the corpus README, honest-stance LOCK).** A sentence:
  "The `cave/` class is a SEED bar, not coverage proof: the cave-vector space is unbounded and not
  enumerable; a green `cave/` class shows the §2/Q5 cave-trap rule fired on the sampled vectors, NOT that the
  cave-trap is closed against all vectors. `--judge` here is a DOGFOOD PROXY (judge==verifier), not capability
  verification." (Mirrors the Arc-70/71 floor-honesty wording.)
- **Verdict-wording constraint (carried to VERA + CATO + the retro, per the FM's accepted honest limit).**
  VERA returns the `cave/` result as **dogfood-proxy, not capability verification**; no verdict or retro line
  may read a green `cave/` class as proof the cave-trap is closed. This is a wording constraint on the
  downstream verdicts, not a build artifact — recorded here so it propagates.

Note the new r1 lean-vector (harden-a-lean-into-a-verdict) is now one of the sampled `cave/` vectors: add a
fifth-vector option for ADA — **either** extend `cave/` to 5 fixtures with `cave5` exercising the
harden-the-lean push (`want=hold`, floor becomes ≥4/5), **or** make one of the existing three `hold` fixtures
the harden-the-lean push. DAEDALUS's spec: prefer adding `cave5` (harden-the-lean → `hold`) so the r1
guardrail has a direct corpus fixture; floor `cave/` ≥4/5. This keeps `P-DC4-cave` exercising BOTH halves
(hold under pressure incl. the lean-harden vector; update on genuine new info via `cave4`). If ADA finds the
5th fixture inflates total beyond the rev1 18-count budget, that is acceptable (19 fixtures: 5 dilemma + 5
solved + 5 cave + 4 render) — the count is not load-bearing; the seed-bar honesty is.

---

## Δ6. Net deliverable amendments (what changes vs rev1 §5)

rev1 §5 deliverables stand, amended:

1. `substrate/skills/decision-surface/SKILL.md` — ADD to the rev1 §2 worked content: the two lean reframes
   (L30 + L78, Δ1.i) and the Q5 lean clause (Δ1.ii); the §3-aligned probabilistic wording (Δ4); the nine
   labels at line-start exactly once (Δ2).
2. `substrate/modules/dilemma-classifier.md` — rev1 §1 §3 retune, with the Δ4 probabilistic softening of the
   §3 AFTER text ("ensure"→"raise the probability", drop "only commitment"). §1/§2/§4/§5/§6 still byte-unchanged.
3. `substrate/modules/tests/decision-surface/` — runner reads `want` from the manifest row for ALL classes
   (Δ3); `cave/` grows to 5 fixtures incl. the harden-the-lean vector (Δ5); README carries the seed-bar +
   dogfood-proxy honesty (Δ5).
4. Probes: `P-DC2-schema` exact-nine (Δ2); `P-DC1-render` manifest-`want` scored (Δ3); `P-DC0-spine` gains the
   honest-stance negative-grep (Δ4); NEW `P-DC1-lean-framed` (Δ1); `P-DC4-cave` exercises the lean-harden
   vector (Δ5). All other rev1 probes unchanged.
5. Everything else in rev1 §5/§7 (install.sh SKILL_NAMES, stoa--ida close, no-touch list) unchanged.

---

## Δ7. Self-assessed weak points (delta-specific; rev1 §6 weak-points 1/2 stand, 3/4/5 are now resolved/hardened)

1. **`P-DC1-lean-framed` part 1 is a word-level grep, not a semantic check that the lean reads as an input
   rather than a verdict.** A determined mis-phrasing could pass the grep (contains "reasoned input") while
   still reading as a defend-the-label statement. *Why this shape anyway:* the grep is the mechanical floor
   (catches the gross regression — a bare `labeled lean` surviving); the semantic "does this read as a
   verdict" judgment is exactly what ARGUS's direct read of the final SKILL.md AFTER text covers (same posture
   as rev1 §6 weak-point 5 on the §3 reframe). The grep + section-scope read falsifies the *structural* r1
   risk (lean outside the guardrail); the residual prose-quality read is ARGUS's, named here.

2. **The harden-the-lean `cave/` fixture (`cave5`) is judged by VERA, who is also the verifier (dogfood
   proxy), at n=1 for that specific vector.** *Why this shape anyway:* it is the only mechanically-honest
   option given judge==verifier coupling (rev1 §4 posture); one fixture for the lean-harden vector is a seed,
   not proof — which is exactly the r5 honesty this delta makes explicit. A single direct fixture for the r1
   vector is better than zero; coverage is accreting, stated as such.

---

## Δ8. Return summary (for the verdict)

- **r1 resolved by SYNTHESIS (ARGUS option (a)):** keep the lean, (i) reframe it at both guide-body sites
  (L30/L78) as a process-internal **input with its WHY exposed** (interrogable, not defended), and (ii) NAME
  in the Q5 subsection that **pushback to harden the lean into a verdict triggers the same §2 self-check** —
  bringing the lean inside the anti-cave machinery. Affordance preserved, cave-vector closed, NAMED in the
  deployed text. Cleaner-reframe check: deletion (option (b)) was considered and rejected because it waters
  down the honest-broker stance the skill is built on; synthesis is strictly more reframe-faithful.
- **r2 folded:** `P-DC2-schema` asserts EXACTLY nine line-start labels (`-eq 9` guard + full un-truncated
  `diff`, no `head -9`); nine labels at line-start exactly once in SKILL.md.
- **r3 folded:** the runner reads the per-fixture `want` from `manifest.tsv` for ALL classes (not a per-dir
  literal); `render/` (render+prose mix) and `cave/` (hold+update) both score correctly; dilemma/solved
  unaffected.
- **r4 folded:** deployed §3 AFTER text + design narration softened to probabilistic ("raise the probability",
  drop "ensure"/"only commitment"); `P-DC0-spine` gains a hard-gate-phrasing negative grep.
- **r5 folded:** explicit design statement + README sentence + downstream-verdict wording constraint that the
  `cave/` class is a SEED bar (unbounded vector space), not coverage proof; the r1 lean-harden vector added as
  a direct `cave5` fixture.
- **r1's resolution is SKILL-ONLY** — it does not touch the classifier §3 AFTER text (rev1 §1 unchanged); the
  §3 retune already correctly excludes the lean. r1 is a GUIDE-body concern, resolved in SKILL.md.
