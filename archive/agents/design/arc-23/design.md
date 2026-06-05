# Arc 23 — integrated design: verification-discipline scaffolding + substrate canon updates

**Author:** Denson Smith.
**Designed by:** CAPTAIN_DAEDALUS (the-stoa, dispatched by MAJOR_PLINY for Arc 23, 2026-05-12).
**Status:** ready for ARGUS audit. Phase 1 deliverable.
**Source directive:** `substrate/arcs/arc-23-build-directive.md` (Phase A decisions A1-A11 LOCKED pre-dispatch).
**Bw tickets covered:** `stoa--tp1`, `stoa--fea`, `stoa--nax`, `stoa--148`, `stoa--vmc`, `stoa--rno`, `stoa--14u` (and `stoa--4h7` — Phase 0, already closed; the upgrade is independent infrastructure and not a substrate edit).

This design is the spec for ADA's Phase 2 build. All substrate-prose deliverables are reproduced here verbatim or near-verbatim so ARGUS can audit wording and ADA copies forward mechanically. The role-file new-section prose lives in this design at the granularity the directive requires; cross-references between sections are explicit so the four verifier role files stay self-consistent.

The design follows the directive's Phase 1 structure: §1 frame → §2 tp1 (load-bearing framework) → §3 verifier role-file cross-refs → §4 fea → §5 nax → §6 148 → §7 vmc → §8 rno → §9 14u → §10 save-verdict schema → §11 self-referential acknowledgment. §12 collects the design decisions ADA + ARGUS need to see at a glance. §13 carries DAEDALUS's self-assessed weak points and the explicit ARGUS sign-off block.

---

## 1. Frame — the 2026-05-12 cluster as empirical anchor

Eight tickets surfaced together during a single working day's bw → Ariadne integration + STRABO-fabrication + bw-scaling-wall cluster. The shape is internally coherent: every ticket traces to that cluster and converges on the same verifier-tier role files. The directive bundles them into one push so the verification-complexity framework ships **with** the disciplines that depend on it — `stoa--fea` inherits `stoa--tp1`; `stoa--nax` and `stoa--148` reinforce verifier-side hygiene; `stoa--vmc` and `stoa--rno` land substrate canon from the same engagement.

The empirical anchors are concrete and load-bearing:

1. **STRABO fabrication (`stoa--fea`).** STRABO produced a research artifact citing `internal/issue/id.go:128` in jallum/beadwork as `matches = append(matches, matches)` — a fabricated bug. The line has always been `append(matches, id)` or `append(matches, name)` across the file's entire 3-commit history. The claim reached substrate-tier as a candidate "drive-by upstream PR." Only the "stop guessing, look at the code" reflex caught it at the drafting boundary. Cost of catching it: ~10 seconds of curl + grep. Cost of not catching it: a wrong-bug GitHub issue against an actively-maintained upstream, with reputational damage to PRINCIPAL.

2. **Verifier-spins-forever failure mode (`stoa--tp1`).** PRINCIPAL flagged the 2x2 of detection-vs-verification difficulty after seeing `stoa--fea` initially scoped as if all verification were tractable. The framing: "in the NP-hard / hard-to-verify quadrant, a verifying agent without quadrant-awareness may run forever and ever." `stoa--fea`'s verification IS easy (cheap re-fetch + grep) — but a STRABO synthesis claim ("every mature git-as-database project has feature X") is not, and the same verifier dispatched against both shapes needs the framework to know which is which.

3. **N=1 generalization + estimate-axis separation (`stoa--nax`).** During the `ariadne--8fd` arc Phase 4 close-out, CATO caught a load-bearing wire-shape mismatch in a dispatch scoped as ADA+CATO-only. The initial reading was "cold-read is structurally sufficient for this defect class." PRINCIPAL corrected: catching something once isn't catching it every time. Parallel signal during the same engagement: an "8-minute" bulk-seed estimate that was off by ~500× because the estimator profiled agent-team throughput (Axis A) but did not characterize upstream-substrate scaling (Axis B).

4. **CATO empirical-env reproduction + probe-fallback coverage (`stoa--148`).** During cleanup-bundle-2 ship (ariadne PR #34, 2026-05-10), CATO caught a load-bearing bug in `rxn` (`_read_commit_from_dot_git` silently failing inside git worktrees because `.git` is a file, not a directory) by **running** the helper against the live working tree — diff-only review would have missed it. Same arc surfaced the fallback-chain probe-coverage gap: the initial probe set covered the env-var path which silently passed even when dot-git was broken.

5. **bw-fit matrix + layered-architecture framing (`stoa--vmc`).** The `ariadne--8fd` Phase 4 bulk-seed hit an empirical bw scaling wall (~50-80h projected for 11,446 tickets). Root cause confirmed via STRABO source-read against jallum/beadwork main: `TreeFS.Commit` rewrites the entire tree on every commit. Every mature git-as-database project (git-bug, public-inbox, beads-on-Dolt) has built a sidecar projection layer; bw does not.

6. **Fork-over-upstream + agent-time latency (`stoa--rno`).** Two memories saved at workspace tier during the same arc: fork-and-tailor is cheap for AI teams (inverted vs human-dev convention); the latency budget for agent-to-system traffic is per-LLM-turn (5-20s acceptable), not per-human-keystroke (<1s).

7. **install.sh deploy-plan smoke beat (`stoa--14u`).** Arc 21 (e2d8b63) added 3 new templates to `substrate/templates/` but did NOT update `install.sh`'s `TEMPLATE_NAMES` deploy list. Re-installs at deployed tiers silently skipped the new templates. Phase C smoke beats checked template **content** (beats 7-8) but did not check whether install.sh actually deploys the files. Smoke validated source quality but missed the source-to-deploy disconnect.

These seven tickets aren't independent observations stitched together for convenience — they're the same arc's findings, each load-bearing in a distinct way, all converging on substrate hygiene the verifying tier owns.

---

## 2. tp1 — the verification-complexity framework (load-bearing scaffolding)

tp1 is the structural load-bearer of this arc. The framework here is what every other ticket either inherits, reinforces, or extends. Designed first; documented in `operating-disciplines.md` §15 inline (per A4 LOCK); referenced by the four verifier role files; integrated into save-verdict's schema; integrated into PLINY's dispatch protocol.

### 2.1 The 2x2

The framework's core artifact. Reproduced verbatim from the ticket body; this is what ADA copies into `operating-disciplines.md` §15.1.

| | Easy to verify | Hard to verify (often NP-hard) |
|---|---|---|
| **Easy to detect** | Standard probe execution. Fast PASS/FAIL. | Bounded verification + explicit **INCOMPLETE** report. Examples: race conditions, performance-at-scale claims, adversarial security — bug surfaces obviously, proving the fix is sound is intractable in general. |
| **Hard to detect** | Work is in finding what to probe; once found, verification is cheap. Example: the 2026-05-12 STRABO fabrication (claim invisible in the relay; trivially falsified by curl + grep once you knew to look). | Worst case. Concurrency bugs in distributed systems with weak guarantees, halting-problem-shaped claims, synthesis-claim overreach ("every mature project of class X has feature Y"). Verifying exhaustively is computationally or practically intractable. **THIS IS WHERE A VERIFYING AGENT SPINS FOREVER IF NOT AWARE OF THE QUADRANT** — verdict shape **UNVERIFIABLE**. |

### 2.2 The discipline rule (verbatim wording for op-disc §15.2)

**Every verifying CAPTAIN dispatch begins with quadrant classification per claim or probe target.** The classification is brief (one sentence + quadrant label per claim) and explicit (recorded in the verdict artifact). **Verification strategy follows from classification, not from the verifier's energy level.**

The cost of NOT having this awareness is the verifier-spins-forever failure mode: a verifying agent in the hard/hard quadrant attempting exhaustive verification of an intractable claim, consuming unbounded budget, and never returning a useful verdict. The framework's value is that it makes "this claim is in the intractable quadrant" a first-class verdict shape rather than an absent verdict and a hung process.

### 2.3 The four verification strategies (verbatim for op-disc §15.3)

**Easy detect / Easy verify (easy-easy)** — Standard probe execution. Run the probe; PASS/FAIL based on output. No special handling. The default mechanical case.

**Hard detect / Easy verify (hard-easy)** — The work is in IDENTIFYING what needs verifying. Once identified, verification is cheap. The verifier's job is to surface candidate claims for spot-check, then probe each. Example: read STRABO's research artifact for cited claims; each cited claim is a candidate probe; falsify each via re-fetch + check. **Cost is in the discovery, not the verification per se.** This is the quadrant `stoa--fea` lives in for source-code-citation claims.

**Easy detect / Hard verify (easy-hard)** — Symptom is obvious; proving the fix is sound is intractable. Example: an intermittent race condition. The verifier runs a bounded battery of probes (high-iteration stress test, mutation testing, model-checking on a reduced state space). Verdict: **INCOMPLETE** — "verified across N iterations; full state space not exhausted." Operator judgment required on whether the bounded coverage is sufficient.

**Hard detect / Hard verify (hard-hard)** — Both finding the claim AND verifying it are intractable. Examples: distributed-systems liveness properties, security exploits with subtle preconditions, synthesis-claim-overreach at scale. **The verifier MUST NOT attempt full verification autonomously.** Verdict: **UNVERIFIABLE** — "claim is in NP-hard / undecidable / intractable-at-scale territory; surfacing to operator for judgment." Include the verifier's quadrant classification + what bounded check WAS performed + what would be needed for full verification.

### 2.4 The two new verdict shapes (verbatim for op-disc §15.4)

The current pattern across verifying CAPTAINs is PASS / FAIL / NEEDS-REVISIONS (or equivalent: pass / fail / inconclusive for VERA; pass / revise for ARGUS and CATO; pass / drift for ZENO). Two new shapes extend the set without disrupting the existing paths:

**INCOMPLETE** — bounded verification performed against an easy-detect / hard-verify claim. Verdict body MUST include:
- (a) what was checked
- (b) what was NOT checked
- (c) the bound used (iterations / state-space subset / time budget)
- (d) the verifier's confidence interval (e.g., "PASS across 10,000 iterations; full state space estimated at ~10⁹ due to interleaving")

Operator decides whether the bound is sufficient. **INCOMPLETE does NOT gate merge on its own** (per A6 LOCK); both INCOMPLETE and UNVERIFIABLE require operator disposition. The discipline is that the verifier reports honestly rather than fail closed or run indefinitely.

**UNVERIFIABLE** — hard-detect / hard-verify claim. No autonomous full-verification attempt. Verdict body MUST include:
- (a) quadrant classification + one-sentence justification
- (b) any sanity check that WAS performed (within ~1× normal probe budget)
- (c) recommended next step (operator judgment / deferred verification via long-running automated suite / accept-the-risk-with-mitigations / etc.)

UNVERIFIABLE also does not gate merge on its own. The verdict is honest output, not a failure.

### 2.5 Time/cost-box defaults (DAEDALUS PICK per A7; verbatim for op-disc §15.5)

**Bounded verification is bounded, not unlimited.** Two defaults:

- **INCOMPLETE-verdict bounded verification gets a default time/cost box of 10× the dispatch's normal probe budget.** Concretely: if a routine probe-set takes ~30s wall-clock and ~5k tokens, the INCOMPLETE bound is 300s / 50k tokens. Configurable per dispatch (the brief may explicitly authorize a higher bound for a load-bearing INCOMPLETE check). 10× is the anchor from the tp1 elevation comment and reflects the principle that bounded verification is genuinely more work than easy-easy probing — but a 100× or 1000× allowance starts to defeat the purpose of bounding.
- **UNVERIFIABLE pulls the verifier out within ~1× normal probe budget.** A sanity-check is allowed; full verification is not. The verifier confirms the quadrant classification (one or two cheap probes to rule out an easier shape), records what it did, returns.

**Rationale for N=10 (the INCOMPLETE multiplier).** Three considerations:
1. **Asymmetric cost.** A passing INCOMPLETE probe with too-tight a bound is a missed catch; a passing INCOMPLETE probe with too-loose a bound is wasted tokens. Tokens are cheap; missed catches in NP-hard territory are not. The bound errs generous.
2. **Operator-fatigue.** Every INCOMPLETE verdict surfaces to PRINCIPAL or POLYBIUS for disposition. If the bound is too tight, INCOMPLETE verdicts proliferate and the disposition queue saturates. 10× lets the verifier do real bounded work; the disposition queue stays manageable.
3. **Easy escalation path.** If a verifier hits 10× and the verdict is still INCOMPLETE with diminishing returns, the verifier returns INCOMPLETE with the data it has. If the brief explicitly authorizes a higher budget (e.g., 100× for a load-bearing concurrency check), the verifier uses it. The default is the floor of "honest bounded work," not the ceiling.

### 2.6 Six worked examples (for op-disc §15.6)

Worked examples make the framework legible. ADA copies these into op-disc §15.6 verbatim.

**Example 1 — Easy-easy / PASS.** VERA probes `/api/bw/projects/conan-superfan/issues` and expects HTTP 200 with non-empty `issues` array. Direct curl + jq. Pass. Standard mechanical case; the framework adds nothing beyond classification, but the classification step is what makes the framework's other quadrants legible by contrast.

**Example 2 — Hard-easy / FAIL.** VERA reads STRABO research artifact claiming `internal/issue/id.go:128` contains `matches = append(matches, matches)`. Quadrant: **hard-detect** (the work is in finding which of the artifact's many cited claims to verify; the claim's wording does not flag itself as suspicious) / **easy-verify** (curl the file at the cited commit + grep for the cited line; match or fail). FAIL: the line is absent from all three commits of the file's history; the structurally-correct `append(matches, id)` is what's actually there. Falsifying evidence: the three commit SHAs + line excerpts. This is the 2026-05-12 STRABO-fabrication case.

**Example 3 — Easy-hard / INCOMPLETE.** VERA verifies a fix for an intermittent concurrency bug. Quadrant: **easy-detect** (the bug reproduces under load) / **hard-verify** (full state space is intractable to exhaust). Bounded probe: 10,000 iterations of stress test against the fix. Result: PASS across all 10,000 iterations. Verdict **INCOMPLETE**: "PASS across 10,000 iterations; estimated full state space ~10⁹ due to thread-interleaving; bound used was 10× normal probe budget at ~300s wall-clock; confidence interval high for non-systematic recurrence, low for adversarial recurrence." Operator decides whether 10,000 iterations is sufficient for ship.

**Example 4 — Hard-hard / UNVERIFIABLE.** STRABO research synthesis claims "every mature git-as-database project has a sidecar projection layer." Quadrant: **hard-detect** (sample bias in mature-project enumeration; how do you find the counter-examples?) / **hard-verify** (counter-example space is the set of all not-yet-discovered such projects). Verdict **UNVERIFIABLE**: cited 3 examples (git-bug, public-inbox, beads-on-Dolt); sanity-checked each individually (each has a documented sidecar projection layer); but the universal-quantifier synthesis is unbounded — verifier surfaces to operator. Recommended next step: treat the claim as a strong heuristic for the cited cases, not a universal law; document the synthesis as evidence-of-pattern, not evidence-of-completeness.

**Example 5 — ARGUS easy-easy.** Design critique: "config file path is hardcoded at `/etc/foo.conf`." Concrete risk; easy-quadrant. Standard FAIL-equivalent (`load_bearing: true`, evidence-cited). No framework overhead needed; this is just a normal load-bearing risk surfaced and routed back to DAEDALUS for revision.

**Example 6 — ARGUS hard-hard.** Design critique: "does this design account for all possible failure modes." Quadrant: **hard-detect** (failure-mode space is unbounded) / **hard-verify** (proving exhaustion is intractable). ARGUS classifies as hard-hard. Verdict **UNVERIFIABLE** at the design-critique level (not "the design is wrong" — the design may be fine, but ARGUS cannot exhaust the failure-mode space). ARGUS surfaces three specific failure modes considered concretely, notes the unbounded property of "all possible," recommends operator review or deferred adversarial testing as the next step. The verdict is honest output; ARGUS does not pretend to have done what it cannot do.

### 2.7 Self-referential observation

The framework's own discipline applies to verifying this very arc. Each Phase 3 verifier (VERA, CATO, ZENO) classifies each probe per the framework. Most probes in this arc are easy-easy (file contains string; schema accepts example; section heading present; cross-reference resolves). Some are hard-easy (wording-drift across the four verifier role files: the work is in spotting the drift across files; once spotted, the drift is mechanical to check). Almost none are easy-hard or hard-hard (this is a doc arc; the framework's harder quadrants emerge for verifying code-shaped deliverables with concurrency / synthesis claims, not doc revisions). VERA's verdict for this arc becomes the first worked example of the framework in action against a real dispatch, in addition to the synthetic examples in §2.6.

---

## 3. Role-file cross-refs — VERA / CATO / ARGUS / ZENO (tp1 inheritance)

Each verifying CAPTAIN's role file gains a new section that operationalizes the framework for that seat. Wording is self-consistent across the four files — they all reference `operating-disciplines.md` §15 as the canonical anchor, they all use the same quadrant labels, they all share the "classify each X per quadrant" rhythm. Differences are role-specific: VERA classifies **probes**; CATO classifies **findings**; ARGUS classifies **risks**; ZENO classifies **criteria**.

The directive (Phase 2 file table) names the section numbers:
- CAPTAIN_VERA.md → §5.7 (quadrant per probe)
- CAPTAIN_CATO.md → §6.7 (quadrant per finding)
- CAPTAIN_ARGUS.md → §6.6 (quadrant per risk)
- CAPTAIN_ZENO.md → §6.6 (quadrant per criterion)

CATO additionally gets §6.8 from `stoa--148` (empirical environment reproduction); VERA additionally gets §5.8 from `stoa--fea` (STRABO-claim verification). Those are §4 and §6 of this design respectively.

### 3.1 CAPTAIN_VERA.md §5.7 — Verification-complexity quadrant per probe (verbatim)

> ### 5.7 Verification-complexity quadrant per probe
>
> Before executing a probe, classify it on the verification-complexity 2x2 (see `operating-disciplines.md` §15 for the full framework). The classification is brief — one sentence per probe naming the detection-vs-verification axes — and explicit, recorded in the verdict's `probes_executed:` block alongside the probe's normal fields.
>
> The four quadrants map to verification strategies as follows:
>
> - **Easy detect / Easy verify (easy-easy)** — VERA's default mechanical case. Code probes (curl + assert; schema check; file existence; grep-against-source) are typically here. Run the probe; PASS / FAIL based on output.
> - **Hard detect / Easy verify (hard-easy)** — research-artifact probes typically live here. The work is in finding the claim to falsify (read STRABO's artifact end-to-end; identify cited claims); falsifying once found is cheap (re-fetch + grep). Cost is in the discovery. See §5.8 for the STRABO-specific protocol.
> - **Easy detect / Hard verify (easy-hard)** — performance / scaling / concurrency probes. Bug surfaces obviously under load; proving the fix is sound is intractable in general. Run a bounded battery (high-iteration stress test, mutation testing, model-checking on a reduced state space); return verdict **INCOMPLETE** with what was checked, what was not, the bound used, and the confidence interval. Default time/cost box is 10× the dispatch's normal probe budget unless the brief authorizes higher.
> - **Hard detect / Hard verify (hard-hard)** — synthesis claims ("every mature project of class X has feature Y"), distributed-systems liveness properties, halting-problem-shaped claims. VERA does NOT attempt full verification autonomously. Within ~1× normal probe budget, confirm the quadrant classification (cheap sanity check) and return verdict **UNVERIFIABLE** with the quadrant + sanity check + recommended next step (operator judgment / deferred long-running suite / accept-risk-with-mitigations).
>
> The quadrant classification protects against the verifier-spins-forever failure mode: a verifier in the hard/hard quadrant attempting exhaustive verification consumes unbounded budget. Honest "I cannot verify this autonomously" is a useful verdict; an absent verdict is not.
>
> Verdict-format integration: the verdict block (§6) gains `quadrant_classification: easy-easy | hard-easy | easy-hard | hard-hard` on each probe. INCOMPLETE-verdict dispatches additionally include `coverage_description:` (what was checked, what was not, bound used, confidence interval); UNVERIFIABLE-verdict dispatches additionally include `sanity_check_performed:` and `recommended_next_step:`. The existing pass / fail / inconclusive paths are unchanged — INCOMPLETE / UNVERIFIABLE extend the set, they do not replace it.

### 3.2 CAPTAIN_CATO.md §6.7 — Verification-complexity quadrant per finding (verbatim)

> ### 6.7 Verification-complexity quadrant per finding
>
> Each finding CATO raises is classified on the verification-complexity 2x2 (see `operating-disciplines.md` §15). The cold-read itself is naturally bounded — CATO reads what it reads — so the classification applies to **findings**, not to the cold-read pass as a whole.
>
> Most CATO findings are easy-quadrant: style / dead code / hygiene / naming-convention drift / commit-message clarity. Standard `revise` routing applies; the quadrant classification is recorded for completeness but adds no special handling.
>
> Hard-quadrant findings get the same routing as VERA's:
>
> - **Easy detect / Hard verify (easy-hard)** — a security finding where the symptom is obvious (e.g., "this function now widens its input scope") but full proof of soundness across all call sites is intractable. CATO surfaces the finding with severity per the §6.1 checklist; if the finding's quadrant is easy-hard AND the diff's coverage of the case is not obviously sufficient, raise a `coverage_concern:` against VERA (the §6.4 meta-verifier discipline) with the quadrant classification attached, framed as "VERA's coverage of this easy-hard case should return verdict **INCOMPLETE** with explicit coverage bound, not silent PASS."
> - **Hard detect / Hard verify (hard-hard)** — a finding about distributed-systems correctness, synthesis-claim overreach in design prose ("the diff handles all failure modes"), or a similar unbounded claim. CATO surfaces the finding as a concern with `severity: recommended-revision` (not blocking on its own — the underlying design / build may still be fine; the issue is the unbounded-claim wording) and the quadrant classification. If the finding's quadrant is hard-hard AND the diff makes a load-bearing synthesis claim, surface as `severity: blocking` with the explicit framing: "the diff asserts a property whose verification is in the **UNVERIFIABLE** quadrant; either narrow the claim or document the bounded coverage."
>
> CATO already has implicit awareness in this territory (the §6.1 checklist already flags "security and blast radius" and "verifier coverage"); the explicit framework removes the ambiguity about which findings get which severity and gives CATO a shared vocabulary with VERA, ARGUS, ZENO when surfacing concerns about verification gaps.
>
> Verdict-format integration: each entry in `concerns:` gains an optional `quadrant_classification: easy-easy | hard-easy | easy-hard | hard-hard` field. The field is required when CATO's reason for the severity rating rests on the quadrant (typical for hard-quadrant findings); omittable when the finding's severity is independent of verification-complexity (typical for easy-quadrant style / hygiene findings).

### 3.3 CAPTAIN_ARGUS.md §6.6 — Verification-complexity quadrant per risk (verbatim)

> ### 6.6 Verification-complexity quadrant per risk
>
> ARGUS design-critique has its own NP-hard quadrant: exhaustive failure-mode enumeration is unbounded. The framework at `operating-disciplines.md` §15 names the discipline; ARGUS applies it per risk raised.
>
> Each entry in `audit_block.risks:` is classified by what verification would cost downstream:
>
> - **Easy detect / Easy verify (easy-easy)** — concrete risks with concrete probes. "Config file path is hardcoded at `/etc/foo.conf`; the design's §3 says runtime should be path-configurable." Standard `load_bearing: true` risk; downstream VERA probe is trivial. ARGUS's quadrant classification is recorded; no special handling.
> - **Easy detect / Hard verify (easy-hard)** — risks where the failure mode is concrete but full verification is intractable. "The design's concurrency model assumes monotonic clocks; the verification of that assumption across all hosts is impractical in the general case." ARGUS surfaces the risk with the quadrant classification; downstream VERA will run an **INCOMPLETE**-verdict bounded probe.
> - **Hard detect / Easy verify (hard-easy)** — risks ARGUS spots that are cheap to verify once spotted. STRABO-fabrication-shaped risks: a citation that may not hold under re-fetch. ARGUS records the risk; downstream VERA runs the cheap re-fetch probe.
> - **Hard detect / Hard verify (hard-hard)** — abstract risks: "does this design account for all possible adversarial inputs," "are there race conditions we haven't anticipated." ARGUS surfaces these honestly without attempting to exhaust the failure-mode space. The risk's `description:` names the concrete instances ARGUS DID consider (typically 3-5); `evidence:` cites where the unbounded property lives in the design; `load_bearing:` is `true` if the unbounded property is structurally load-bearing, `uncertain` otherwise. ARGUS does NOT manufacture a remediation; the §6.1 no-fixes rule still holds. Downstream VERA returns **UNVERIFIABLE** on such risks rather than attempting full verification — this is the `verifier-spins-forever` failure mode the framework's classification step prevents.
>
> The structural point: ARGUS, like VERA, has an **UNVERIFIABLE**-equivalent verdict shape for risks it cannot exhaust. The discipline is to surface honestly rather than either (a) hedge into vagueness ("the design feels fragile") or (b) manufacture a confident exhaustion claim ("the design accounts for all failure modes"). Both fail the seat's value. The classification step is what prevents ARGUS from itself exhibiting `verifier-spins-forever` behavior against hard-hard risks: ARGUS classifies, surfaces, stops.
>
> Verdict-format integration: each entry in `audit_block.risks:` gains an optional `quadrant_classification: easy-easy | hard-easy | easy-hard | hard-hard` field. Required when the risk's `load_bearing:` rating rests on the quadrant; omittable when the risk's severity is independent.

### 3.4 CAPTAIN_ZENO.md §6.6 — Verification-complexity quadrant per criterion (verbatim)

> ### 6.6 Verification-complexity quadrant per criterion
>
> Most ZENO criterion-checks are easy-quadrant: the spec says criterion X is required; the artifact either contains X or it does not. `met | partial | not-met | uncheckable` per the §6.2 discipline. The framework at `operating-disciplines.md` §15 is mostly informational for ZENO.
>
> The narrow case where the framework actively applies: **synthesis claims embedded in specs.** When a spec asserts a universal property ("no information leaks anywhere in the pipeline," "every supported input class is handled," "the implementation is correct under all valid configurations"), full verification is in the UNVERIFIABLE quadrant. ZENO does NOT mark such criteria `met` on the basis of a finite-sample probe. The honest verdict is:
>
> - **`partial`** if a bounded sample was checked and passed — record the sample as evidence; record the unbounded property as a `spec_ambiguity:` if the spec did not explicitly bound the synthesis.
> - **`uncheckable`** if the synthesis claim is genuinely intractable and no bounded interpretation is available — record under `spec_ambiguities:` with the explicit framing "criterion asserts a synthesis claim whose verification is in the UNVERIFIABLE quadrant per `operating-disciplines.md` §15."
>
> ZENO never asserts a synthesis claim has been verified when only a finite-sample probe has been run. The discipline is mechanical: if the spec's words promise more than the artifact's evidence delivers, the criterion is not `met`.
>
> Verdict-format integration: when a criterion's result rests on a synthesis-claim ambiguity, the `evidence:` field cites the quadrant explicitly: `evidence: "spec §X asserts <universal property>; quadrant: hard-hard (UNVERIFIABLE per op-disc §15); bounded check at <sample> passed; full synthesis unbounded."` No new field required; the discipline lives in the evidence prose.

### 3.5 Wording-drift discipline across the four files

The four sections above share five load-bearing strings; cross-file consistency on them is the biggest landmine of this arc:

| String | Where it appears | Constraint |
|---|---|---|
| `operating-disciplines.md §15` | every file's new section | exact text |
| `easy-easy / hard-easy / easy-hard / hard-hard` | VERA §5.7, CATO §6.7, ARGUS §6.6 (full enumeration in the section's strategy-list). ZENO §6.6 references only the specific quadrant labels relevant to its narrow case (`hard-hard` appears in the `evidence:` example string); the full enumeration is not required because ZENO's prose explicitly states "the framework at `operating-disciplines.md` §15 is mostly informational for ZENO." | exact lowercase-hyphenated form where it appears (matches save-verdict schema) |
| `INCOMPLETE` / `UNVERIFIABLE` (bare uppercase) | VERA §5.7, CATO §6.7, ARGUS §6.6 must contain both as bare verdict-shape labels. ZENO §6.6 is structurally lighter: ZENO classifies criteria via `met / partial / not-met / uncheckable`, not via INCOMPLETE / UNVERIFIABLE verdict shapes. ZENO's prose uses the form `UNVERIFIABLE quadrant` (qualifier-attached) when naming the framework's quadrant; incidental bare-uppercase use inside an `evidence:` example string is fine and not a violation. ZENO is exempt from the bare-`INCOMPLETE` requirement entirely. | exact uppercase where it appears in verdict-shape context |
| `verifier-spins-forever` | VERA §5.7 and ARGUS §6.6 (op-disc §15 introduces it). CATO and ZENO do not exhibit the failure mode in the same shape — CATO's cold-read is naturally bounded; ZENO's criterion-check is bounded by the spec. | exact lowercase-hyphenated form where it appears |
| `quadrant_classification:` schema field | VERA §5.7, CATO §6.7, ARGUS §6.6 verdict-format-integration paragraphs (snake_case schema field). ZENO §6.6 is exempt: ZENO's discipline lives in the `evidence:` prose (citing the quadrant by name), not in a new schema field — ZENO's existing `met/partial/not-met/uncheckable` enum is unchanged. | exact snake_case where it appears |

ARGUS's audit should explicitly check these five strings against the four role files **subject to the per-row exemption notes**. Section numbers vary per file (VERA §5.7, CATO §6.7 + §6.8, ARGUS §6.6, ZENO §6.6); the substrings above are stable across all four files where the exemption notes do not apply.

---

## 4. fea — STRABO-verification

Three substrate edits land the discipline that STRABO claims aren't load-bearing until VERA verifies them. Inherits the tp1 framework: STRABO source-code citations are hard-easy probes; STRABO synthesis claims are hard-hard probes.

### 4.1 CAPTAIN_VERA.md §5.8 — STRABO-claim verification (verbatim)

> ### 5.8 STRABO-claim verification
>
> When MAJOR_PLINY dispatches VERA on a STRABO research artifact (typically follow-on to a STRABO dispatch whose output is intended for substrate-tier or upstream-project propagation), the brief names the artifact path + the citation-verification policy (full vs sampled).
>
> Per-claim probe shapes per the framework's hard-easy quadrant (one-sentence quadrant classification + the corresponding mechanical probe; record both in the verdict):
>
> | Claim type | Quadrant | Probe |
> |---|---|---|
> | Source-code citation (file:line at commit) | hard-easy | Re-fetch source at the claimed commit; grep for the claimed line. Match or fail. ~3s cost per claim. |
> | Documentation citation (URL + paragraph) | hard-easy | Re-fetch URL; read surrounding context; confirm STRABO interpretation isn't stretched. Low cost per claim. |
> | Behavioral claim about a tool / library | easy-hard | Re-run the behavior; check it survives across reasonable inputs. INCOMPLETE-verdict if behavior is intermittent / configuration-dependent. |
> | Synthesis claim ("every mature project of class X has feature Y") | hard-hard | UNVERIFIABLE per §5.7. Cited individual examples can be sanity-checked (one cheap probe each); the synthesis claim itself is unbounded and surfaces to operator. |
>
> The first two shapes are cheap and would have caught the 2026-05-12 STRABO fabrication (the case where `internal/issue/id.go:128` was cited as containing code that has never existed in the file's history). The fourth is where STRABO is most likely to overreach; the discipline is to refuse the synthesis-claim verdict autonomously rather than manufacture a confidence number.
>
> **Sampling policy (PLINY scope-decides per dispatch; default below):** VERA verifies citations per the brief's `sampling:` field. The field is YAML-valued; two canonical shapes:
>
> - `sampling: full` — every citation in the artifact. Default for substrate-tier-bound or upstream-project-bound propagation, where a single fabricated citation creates outsize reputational / process-integrity cost.
> - `sampling: 3` (bare integer) — N citations selected by VERA (one from each major claim type if present; prefer the load-bearing claims). Default `N=3` for routine in-project propagation where a sample is sufficient signal; PLINY may set any positive integer per dispatch.
>
> The two valid YAML values are the keyword `full` (string) or a positive integer (number of citations to sample). No other forms are accepted. VERA may surface a `sampling_concern:` in `methodology_concerns:` if the brief's sampling policy is mismatched to the artifact's intended propagation surface (e.g., brief says `sampling: 3` but the artifact is being staged for an upstream GitHub issue). The concern routes to MAJOR_PLINY for scope re-decision.
>
> Verdict feeds back into the artifact as a separate verification block (not by editing STRABO's artifact in place — VERA's §5.1 independence rule). The verification artifact path is `agents/verification/<ticket-id>/strabo-verification-<sha>.md` or as the brief specifies. STRABO's artifact gains a footnote referencing the verification result when PLINY closes the loop; VERA does not edit STRABO's artifact directly.

### 4.2 CAPTAIN_STRABO.md — claims preliminary until VERA-verified (new §6.6)

ADA appends this as a new §6.6 under the existing disciplines section of `CAPTAIN_STRABO.md`. Current STRABO file structure: §1, §2, §3, §4, §5, §6 (disciplines §6.1-§6.5), §7 (verdict format), §8 (when this file is wrong). The new discipline lands as §6.6 under disciplines; ADA preserves the existing §7/§8 numbering.

> ### 6.6 Output is preliminary until VERA-verified (substrate-tier / upstream-bound propagation)
>
> STRABO's research artifact is preliminary until VERA verifies its citations. This is the same pattern as DAEDALUS's designs being preliminary until ARGUS reviews — the SCOUT seat surfaces; the VERIFIER seat falsifies; the orchestrator routes.
>
> The discipline:
>
> - **Self-marking for propagation.** When the brief flags the research as intended for substrate-tier propagation (a substrate-canon update) or upstream-project propagation (a GitHub issue, an upstream PR, a documented bug claim), STRABO adds an explicit `verification_status: needs-vera` tag in the artifact's frontmatter or opening section. This signals to MAJOR_PLINY that a follow-on VERA dispatch is required before the artifact becomes load-bearing.
> - **Per-claim self-classification (encouraged, not required).** When STRABO can cheaply identify a claim's verification-complexity quadrant per `operating-disciplines.md` §15 (e.g., "this is a source-code citation, quadrant hard-easy"), STRABO tags the claim with the quadrant. The tagging speeds VERA's sampling-policy decision and surfaces synthesis claims (hard-hard) for explicit operator disposition rather than letting them slip through as if they were verifiable.
> - **No autonomous propagation.** STRABO does not draft the substrate-canon edit or the upstream GitHub issue itself when its artifact is propagation-intended. The drafting boundary is where the 2026-05-12 STRABO fabrication almost-but-didn't escape — only the substrate-tier "stop guessing, look at the code" reflex caught it. The discipline replaces that reflex with structural routing: the artifact stops at STRABO; the citation-verification dispatch is VERA's job; the drafting is downstream.
>
> Empirical anchor: 2026-05-12 — STRABO claim about `internal/issue/id.go:128` in the project-tier bw scaling research; verified against bw main and v0.13.0 by substrate-tier POLYBIUS at the drafting boundary; claim did not hold up under verification. Cost of catching: ~10 seconds of curl + grep. Cost of not catching: a wrong-bug GitHub issue against an actively-maintained upstream. Substrate ticket: `stoa--fea`.

### 4.3 MAJOR_PLINY.md §5.5 — post-STRABO VERA dispatch (verbatim, new subsection under §5)

ADA inserts this as new §5.5 in MAJOR_PLINY.md (after the existing §5.4 per-worktree virtualenv reflex; renumbers nothing — the next existing section is §6).

> ### 5.5 Post-STRABO VERA dispatch (substrate-tier / upstream-bound propagation)
>
> When a STRABO dispatch produces an artifact intended for substrate-tier or upstream-project propagation (substrate-canon update, GitHub issue against an upstream repo, documented bug claim against an actively-maintained dep), the dispatch loop is **not closed** until a follow-on VERA dispatch verifies the artifact's citations.
>
> The protocol:
>
> 1. **Read STRABO's artifact for the propagation flag.** STRABO self-marks `verification_status: needs-vera` per `CAPTAIN_STRABO.md` §6.6 when the brief flagged the research as propagation-intended. If the flag is absent but the brief's destination indicates substrate-tier / upstream-bound, treat as if flagged.
> 2. **Pick sampling policy.** Per `CAPTAIN_VERA.md` §5.8. The brief's `sampling:` field is YAML-valued: the keyword `full` (string) or a positive integer.
>    - **`sampling: full`** for substrate-tier-bound or upstream-project-bound artifacts. Every citation gets verified. Default for substrate-canon and upstream-PR destinations.
>    - **`sampling: 3`** (bare integer) for routine in-project propagation where a sample is sufficient. Default `N=3` for in-project research feeding a downstream design; PLINY may set any positive integer per dispatch.
> 3. **Dispatch VERA on the artifact** with a citation-verification brief naming the artifact path, the sampling policy, the ticket ID, and any quadrant tags STRABO self-applied. VERA returns a verdict per `CAPTAIN_VERA.md` §6 with one probe per (sampled) claim and `quadrant_classification` recorded per probe.
> 4. **Route per VERA's verdict.**
>    - VERA returns `pass` → STRABO's artifact is canonical; propagation proceeds.
>    - VERA returns `fail` (any citation falsified) → STRABO's artifact is NOT canonical; surface the falsifying evidence to POLYBIUS for routing; do not propagate.
>    - VERA returns `INCOMPLETE` or `UNVERIFIABLE` → operator disposition (per §5.6 below) before propagation. Both verdict shapes surface to POLYBIUS; neither gates merge autonomously.
>
> The discipline is the same redundant-checker property the gauntlet's other pairs enforce: STRABO surfaces; VERA falsifies; PLINY routes. STRABO claims are not load-bearing until VERA verifies them.
>
> Empirical anchor: `stoa--fea` (2026-05-12). The chain that almost-but-didn't fail propagated a STRABO fabrication through to a draft GitHub issue against jallum/beadwork; only the "stop guessing, look at the code" reflex at the drafting boundary caught it. This protocol replaces the reflex with structural routing.

### 4.4 MAJOR_PLINY.md §5.6 — INCOMPLETE / UNVERIFIABLE verdict handling (new subsection)

Lands after §5.5. Required by `stoa--tp1` Section 4 (elevation comment) and referenced from §5.5.4 above.

> ### 5.6 Dispatch protocol for INCOMPLETE and UNVERIFIABLE verdicts
>
> When a verifying CAPTAIN (VERA, CATO, ARGUS, ZENO) returns a verdict of **INCOMPLETE** or **UNVERIFIABLE** per the verification-complexity framework (`operating-disciplines.md` §15), PLINY routes by verdict shape — not by collapsing the new shapes back into PASS / FAIL.
>
> **INCOMPLETE verdict received.**
>
> - PLINY does NOT auto-close the ticket. INCOMPLETE is an operator-disposition state, not a ship verdict.
> - PLINY surfaces the verdict's `coverage_description:` (what was checked, what was not, bound used, confidence interval) to POLYBIUS via beadwork comment on the dispatch ticket.
> - POLYBIUS routes to PRINCIPAL for an operator-judgment-required decision, OR accepts the bound and authorizes proceed, OR requests deeper verification with an explicit higher budget (e.g., "re-run VERA with 100× probe budget; document in the verdict").
> - The verdict does NOT gate merge on its own (per `operating-disciplines.md` §15.4 A6 LOCK). Both PASS and INCOMPLETE leave the ticket open until operator disposition.
>
> **UNVERIFIABLE verdict received.**
>
> - PLINY does NOT auto-close the ticket. UNVERIFIABLE is also an operator-disposition state.
> - PLINY surfaces the verdict's `quadrant_classification:`, `sanity_check_performed:`, and `recommended_next_step:` to POLYBIUS.
> - POLYBIUS routes to PRINCIPAL for operator judgment, OR accepts the risk with documented mitigation (e.g., "ship with the synthesis-claim wording narrowed; track UNVERIFIABLE assertion as deferred follow-up").
> - UNVERIFIABLE also does not gate merge on its own.
>
> **Why neither gates merge.** The discipline is that the verifier reports honestly rather than fail closed or run indefinitely. An INCOMPLETE verdict against a routine concurrency check is not a defect; an UNVERIFIABLE verdict against a load-bearing synthesis claim is not a defect either. Both surface decisions that belong with operator judgment. Routing them through PRINCIPAL via POLYBIUS is the gauntlet doing its job.
>
> Cross-refs: `operating-disciplines.md` §15 (the framework); `CAPTAIN_VERA.md` §5.7 (VERA's quadrant discipline); `CAPTAIN_CATO.md` §6.7; `CAPTAIN_ARGUS.md` §6.6; `CAPTAIN_ZENO.md` §6.6.

---

## 5. nax — redundant-checks + N=1 + estimate-axes

Three substrate edits land the discipline that pipeline redundancy isn't surplus, single observations don't generalize, and agent-throughput and upstream-substrate are separate estimation axes.

### 5.1 operating-disciplines.md §6.7 — N=1 generalization rule + estimate-axis separation (verbatim, two subsections under existing §6)

Per the directive's A5 table, the placement is **§6.7** with two subsections (§6.7.1 and §6.7.2) inside, extending the existing §6 "Suppress single-checker thinking" redundancy theme into the corollary against generalizing from single observations. ADA inserts this after the existing §6 closing paragraph ("If you find yourself reasoning toward 'this deliverable is small, VERA/CATO/ZENO is overkill'…STOP and run the full pipeline.") and before §7 ("Coordinating two POLYBIUS seats").

> ### 6.7 Generalization discipline: N=1 conclusions are not structural lessons
>
> Every CAPTAIN-tier check in the dispatch pipeline (DAEDALUS / ARGUS / ADA / VERA / CATO / ZENO) is structurally redundant by design — multiple seats reading the same artifact from different angles. The §6 discipline names the rule against treating overlapping coverage as substitutable; this subsection names the corollary against generalizing from individual catches.
>
> #### 6.7.1 The N=1 rule
>
> When one check catches a defect (and others would have missed it, or didn't dispatch at all), the right conclusion is **"the pipeline worked"** — not **"we can drop the other checks."** A single observation where "CATO caught X that VERA didn't" or "ADA shipped clean without DAEDALUS" is one data point, not evidence that the missing seat is structurally unnecessary.
>
> Structural claims about the pipeline's safety properties require all of:
>
> 1. **Multiple observations across distinct defect classes.** A single repeated catch of one defect class is not yet a pattern; the catch may be specific to that class's surface area.
> 2. **Controlled comparison.** The same defect class encountered with vs. without the seat in question. Without the comparison, the observation does not separate "the seat was unnecessary" from "the seat was unnecessary FOR THIS CASE."
> 3. **Substrate-level pattern.** Promoted to substrate canon via the normal accretion path (operating-disciplines.md edit), not just a one-off anecdote in a TIMING_LOG.
>
> Until those three conditions hold, the canonical pattern (full gauntlet dispatch) is the default. Per-engagement scope decisions (e.g., "this is mechanical scaffolding, ADA + CATO only") are operational choices made deliberately, not extrapolations from prior catches. The dispatching seat may scope narrowly when the engagement warrants it; the dispatching seat does NOT scope narrowly because "last time we found CATO was sufficient."
>
> Empirical anchor: 2026-05-12, `ariadne--8fd` arc Phase 4 close-out. CATO caught a load-bearing wire-shape mismatch via cold-read in a dispatch scoped as ADA+CATO-only. The initial reading was 'cold-read is structurally sufficient for this defect class.' PRINCIPAL corrected: catching something once isn't catching it every time. The reframe: "CATO caught this defect in this instance" (which is honest) vs. "cold-read alone is sufficient" (which is overreach). Substrate ticket: `stoa--nax`.
>
> #### 6.7.2 Estimate-axis separation
>
> A second corollary surfaces at the same engagement: estimation discipline must separate **agent-team throughput** (Axis A) from **upstream-substrate performance characteristics** (Axis B). The two axes have different empirical bases and different failure modes when conflated.
>
> **Axis A: Agent-team throughput.** Estimates for gauntlet-shaped agent work (DAEDALUS / ADA / VERA / CATO / etc.) held within ~3× during the 2026-05-12 calibration data. Phase 1+2+3+3.5+4+4.5+5 of the relevant arcs came in at 30-90 min of CAPTAIN-agent work against estimates of 1-4 hours. This axis is now empirically calibrated for similar-shape future work — anchor on calibration data from past arcs of the same shape.
>
> **Axis B: Upstream-substrate performance characteristics.** A bulk-seed operation estimated at ~8 min wall-clock came in at ~50-80h projected, because the underlying substrate (bw / TreeFS.Commit) has a scaling pattern that rewrites the entire tree on every commit. The estimate was off by ~500× because the estimator did not profile the substrate at relevant scale before committing. Axis B requires its own characterization: **profile the substrate at relevant scale BEFORE committing, especially for bulk operations.** Do not extrapolate from small-N behavior unless you have also characterized the scaling curve.
>
> **The discipline (when an arc involves both axes):**
>
> 1. Estimate agent-team work (Axis A) — anchor on calibration data from similar-shape past arcs.
> 2. Estimate upstream-substrate performance (Axis B) — profile the substrate at relevant scale before committing. Document the scaling curve in the estimate's evidence.
> 3. Surface both axes separately in the engagement plan so the reviewer can pressure-test each independently.
>
> The N=1 rule (§6.7.1) and the estimate-axis-separation rule (§6.7.2) are complementary disciplines. Both target the same failure mode (drawing structural conclusions from insufficient data), at different layers.
>
> Empirical anchor: 2026-05-12, the bw → Ariadne integration arcs Phase 4 OPERATOR ACTION. Substrate ticket: `stoa--nax` (2026-05-12T17:59:55Z comment captures the axis-separation surface).

### 5.2 MAJOR_PLINY.md §7.8 — no-narrowing-gauntlet-from-N=1 (new subsection)

Lands as new §7.8 in MAJOR_PLINY.md (the disciplines section currently ends at §7.7 voice discipline; this is a new ORCHESTRATOR-specific discipline).

> ### 7.8 No-narrowing-gauntlet-from-N=1 (`stoa--nax`)
>
> When you scope a gauntlet dispatch narrower than the canonical full pipeline (e.g., "this is mechanical scaffolding; ADA + CATO only" or "this is a doc-only edit; skip VERA"), the decision is an **operational choice for this engagement**, not an extrapolation from prior catches. The discipline at `operating-disciplines.md` §6.7.1 names the rule: a single prior catch where "CATO caught X that VERA didn't" is one data point, not evidence that VERA is structurally unnecessary.
>
> Operational scope decisions are routine — not every dispatch needs the full gauntlet. The discipline is about the **justification**, not the existence of the decision:
>
> - **OK:** "This dispatch is a doc-only edit with no probe surface for VERA; scoping to ADA + CATO."
> - **OK:** "This dispatch is one-line config change with explicit probe spec; scoping to ADA + VERA, skipping CATO cold-read."
> - **NOT OK:** "Last arc CATO caught the defect in an ADA+CATO-only dispatch, so this arc can also skip VERA."
>
> The "not OK" form generalizes from N=1. Catching once isn't catching every time. If the project's calibration accretes substrate-level evidence over time that one seat is genuinely redundant for one defect class, that goes into substrate canon via the normal accretion path — not into per-engagement scope decisions.
>
> Cross-ref: `operating-disciplines.md` §6 (single-checker thinking), §6.7.1 (N=1 generalization rule), §6.7.2 (estimate-axis separation).

### 5.3 MAJOR_POLYBIUS.md §15 — TIMING_LOG / retrospective discipline note (new top-level section)

The current MAJOR_POLYBIUS.md ends at §14 (substrate-update check, daily-cadence drift check). The directive specifies a TIMING_LOG / retrospective discipline addition: "TIMING_LOG / retrospective discipline note that N=1 conclusions are not enshrined as substrate-tier structural lessons." This is a distinct concern from §14's substrate-freshness machinery, so ADA inserts it as a new §15 in MAJOR_POLYBIUS.md (after §14, before the closing "Standby, run." line).

> ## 15. Retrospective discipline — N=1 conclusions are not structural lessons
>
> When you author a TIMING_LOG entry or a retrospective after an arc closes, the discipline at `operating-disciplines.md` §6.7.1 applies: a single observation is one data point, not a structural lesson.
>
> Concretely, an arc retrospective may include observations of shape "CATO caught X that VERA missed" or "ADA shipped clean without DAEDALUS"; those are valid honest data. The retrospective MUST NOT promote those observations to structural claims like "cold-read is sufficient for this defect class" or "DAEDALUS is unnecessary for mechanical scaffolding" on the strength of a single occurrence. Honest scoping:
>
> - **OK:** "In this arc, CATO caught the wire-shape mismatch via cold-read. VERA was not dispatched."
> - **OK:** "In this arc, the ADA + CATO scope was deliberate; the engagement shape didn't warrant DAEDALUS."
> - **NOT OK:** "Cold-read is structurally sufficient for wire-shape mismatches" (generalizes from N=1).
> - **NOT OK:** "DAEDALUS is unnecessary for mechanical scaffolding" (generalizes from N=1).
>
> Substrate-level structural claims (the ones that go into operating-disciplines.md or a CAPTAIN role file as canon) accrete via the §6.7.1 three-condition gate: multiple observations, controlled comparison, substrate-level pattern. The retrospective is the **input** to that gate; it is not where the gate's output gets written.
>
> When you spot an observation that might warrant substrate canon promotion, file a substrate ticket (`stoa--xxx`) and accrete the evidence over time. Do not write the substrate claim into the TIMING_LOG itself.
>
> Cross-ref: `operating-disciplines.md` §6.7.1 (the rule), §6.7.2 (estimate-axis separation — also a TIMING_LOG concern when the arc had a substrate-performance component). Empirical anchor: 2026-05-12, `ariadne--8fd` arc close-out, `stoa--nax`.

---

## 6. 148 — CATO empirical-env + probe-fallback (DECISION: probe-coverage in op-disc §8.4)

Two substrate edits land the CATO empirical-environment discipline and the probe-fallback-coverage discipline.

### 6.1 Decision: probe-coverage in op-disc §8.4 vs MAJOR_PLINY.md

The directive lets DAEDALUS pick the placement for the probe-coverage-of-fallback-chains discipline. The options:

- **op-disc §8.4** — universal-team discipline; both CAPTAIN_ADA (probe authoring) and CAPTAIN_VERA (probe coverage check) read it.
- **MAJOR_PLINY.md** — ORCHESTRATOR-specific; lands in PLINY's ADA-brief preamble template.

**Decision: op-disc §8.4.** Two reasons:
1. The discipline applies to both ADA (authoring the probes) and VERA (checking whether the probes cover the fallback chain). PLINY-only placement narrows the audience artificially.
2. The directive's A5 LOCK pre-numbers §8.4 as the probe-coverage subsection. Honoring the lock keeps the cross-ref-from-other-files mechanical: every CAPTAIN can point at op-disc §8.4 from anywhere.

ADA does NOT additionally edit MAJOR_PLINY.md for probe-coverage. The §8.4 entry is the canonical location; PLINY's ADA-brief preamble already includes the §5.2 grounding-check enumeration, which is the analogous "ADA-brief preamble" entry for grounding. If the project finds in practice that ADA needs an explicit preamble inclusion for the §8.4 discipline, a future arc adds it.

### 6.2 CAPTAIN_CATO.md §6.8 — Empirical environment reproduction (verbatim)

Lands as new §6.8 in CAPTAIN_CATO.md after the §6.7 verification-complexity-quadrant section.

> ### 6.8 Empirical environment reproduction for environment-interactive code
>
> CATO's default review pattern is cold-read of the diff plus surrounding source context (§3 read list, §6.1 baseline checklist). This pattern is sound when the change is environment-agnostic; it falls short when the change interacts with environment state — filesystem layout (especially git internals; worktrees vs main checkouts), OS-specific behavior, network conditions, runtime configuration that varies between development and deployment.
>
> The discipline:
>
> **When the diff under review interacts with environment state, CATO empirically probes the change against the live working tree before forming a verdict.** Cold-read of the diff is necessary but not sufficient; the diff's behavior in isolation can be correct, while the diff's behavior in the actual environment can silently fail.
>
> Concrete shapes that trigger empirical reproduction:
>
> - **Filesystem-shape assumptions.** The diff reads from / writes to specific paths whose shape may vary (e.g., `.git/` is a directory in a normal checkout but a file in a worktree).
> - **Git-internal interactions.** The diff parses git output, reads from `.git/`, or assumes a specific git-config state.
> - **OS-specific behavior.** Path separators, encoding defaults, line endings, shell quoting.
> - **Configuration cascades.** The diff reads from an env-var or config file with a fallback chain; the fallback path may behave differently from the primary.
>
> When CATO triggers empirical reproduction, the probe is recorded in the verdict's `concerns:` block (or in a `verifier_coverage_assessment:` note if the empirical run informed the verifier-coverage rating). The cost is small (~30s to set up the probe context); the catch when the cold-read missed an environment-interactive defect is large.
>
> This discipline is sharper than the §6.1 baseline checklist's "security and blast radius" entry: blast-radius is about the diff's effect when correct; empirical reproduction is about the diff's behavior at all when the environment isn't the assumed shape.
>
> Empirical anchor: 2026-05-10 cleanup-bundle-2 ship (ariadne PR #34 / d83cd23). CATO caught a load-bearing bug in `rxn` (`_read_commit_from_dot_git` silently failing inside git worktrees because `.git` is a file, not a directory) by running the helper against the live working tree, not just cold-reading the diff. The diff itself looked correct in isolation; only when CATO probed against the actual working environment did the gap surface. Substrate ticket: `stoa--148` Observation 1.

### 6.3 operating-disciplines.md §8.4 — Probe coverage of fallback chains (verbatim)

Lands as new §8.4 in op-disc after the existing §8.3 activation-paste section. Per A5 LOCK numbering.

Note: the directive's A5 table names §8.3 as the `stoa--14u` smoke-beats subsection and §8.4 as `stoa--148` probe-coverage. The current shipped op-disc already uses §8.3 for "Activation paste — which session-state to use" (added in Arc 21). The directive's A5 numbering appears to have been written without accounting for the Arc 21 §8.3 addition — the prose intent ("new subsections under §8 for 14u and 148") is unambiguous; the specific numbers reflect the directive author's counting at directive-authoring time.

**Decision: §8.4 (14u: install.sh smoke beats) and §8.5 (148: probe coverage); preserve existing §8.3 activation paste.** Rationale:

1. **Design-vs-shipped audit drift.** Renumbering an existing shipped section (Arc 21's §8.3 activation-paste) to honor a downstream lock-table numbering is a substantive change to Arc 21's contract. The shipped substrate names a section §8.3 with specific content; downstream consumers (skills / dispatches / cold-readers) read that anchor. Renumbering it as a side effect of Arc 23's numbering preference is exactly the design-vs-shipped audit pattern that `stoa--bxx`-class tickets exist to prevent. The cost is bounded but real: every future audit of "did Arc 21 ship what its design said" now has to reconcile against the Arc 23 renumbering.
2. **The LOCK's prose intent is preserved by §8.4 / §8.5.** The A5 LOCK's binding scope is "new subsections under §8 for 14u and 148." §8.4 and §8.5 satisfy that scope. The literal numbers (§8.3 / §8.4) in the LOCK table appear to be a counting error — directive A5 also references §8.3 in line 97 and §8.4 in line 98, both as new additions, which is internally inconsistent with an existing shipped §8.3.

**Empirical falsification of an earlier rationale.** A prior draft cited "cross-references to op-disc §8.3 from elsewhere in the substrate would also break" as additional rationale for preservation. Verified via `grep §8\.3 substrate/` (excluding the arc-23 directive itself): zero hits. No substrate file outside this arc's directive references §8.3. The cross-ref-breakage claim is not the load-bearing rationale; design-vs-shipped audit drift is.

Below assumes §8.4 (14u) and §8.5 (148):

> ### 8.5 Probe coverage of fallback chains
>
> When a code path uses fallback resolution — env-var → file → default; configured path → discovered path → built-in default; database read → cache read → recompute — the probe set the deliverable ships with MUST independently exercise each resolution path. Probe coverage that hits only the primary path silently misses bugs in the fallback paths.
>
> The discipline is symmetric across the gauntlet:
>
> - **ADA (authoring probes)** designs the probe set with explicit per-path coverage. Each resolution-path in the fallback chain gets at least one probe that exercises ONLY that path (the others either don't apply or are deliberately broken in the probe's setup).
> - **VERA (executing probes)** records which resolution path each probe exercised. A probe set that exercises only one path's outputs while the chain has three paths surfaces as a `methodology_concerns:` entry ("probe set does not independently exercise the file-fallback path"); VERA does not silently extend the probes' scope.
> - **CATO (reviewing the diff)** flags missing-path probes as a `coverage_concern:` against VERA per the §6.4 meta-verifier discipline. The §6.8 empirical-environment discipline often triggers this case in practice: when CATO empirically probes the diff and discovers a fallback-path behavior the original probe set did not cover.
>
> Common shapes:
>
> | Pattern | Each path gets a probe |
> |---|---|
> | `GIT_COMMIT env-var → .git/HEAD read → 'unknown' default` | (a) env-var set; (b) env-var unset, .git/HEAD readable, returns sha; (c) env-var unset, .git/HEAD unreadable, returns 'unknown' |
> | `--config flag → config file in cwd → config file in home → built-in defaults` | one probe per cascade level |
> | `cache hit → DB read → recompute` | one probe per resolution path |
>
> The 2026-05-10 `rxn` `_resolve_commit_sha()` example showed the failure mode concretely: the initial probe set had an env-var-set probe (PASS) and an env-var-unset path that ASSUMED it exercised dot-git, but dot-git silently returned `'unknown'` inside worktrees → fell through to default `'unknown'` → probe still passed because `'unknown'` was the assertion. CATO's empirical reproduction (§6.8) caught it; ADA then added a probe asserting dot-git happy path (returns actual SHA, not `'unknown'`) and the fix landed.
>
> Empirical anchor: PR #34 / d83cd23, 2026-05-10. Substrate ticket: `stoa--148` Observation 2.

---

## 7. vmc — bw-fit matrix + layered-architecture framing

One substrate edit lands the bw-fit matrix and the bw/Ariadne/hypergraph layered-architecture framing. Verbatim from the ticket body; ADA copies into op-disc §16.

### 7.1 operating-disciplines.md §16 (verbatim, new top-level section)

Per A5 LOCK numbering, the three new top-level sections (§15 tp1, §16 vmc, §17 rno) land between the existing §14 (Sub-agent diagnostic transcript discipline) and the "Agent-regime inverses" closer. The "Empirical lineage" closer stays at the end. §16 lands after §15 (tp1) and before §17 (rno).

> ## 16. bw-fit matrix + layered-architecture framing
>
> When choosing a project's substrate for ticket-shape state, knowledge-shape data, or hybrid use cases, consult this matrix before committing to bw. The matrix codifies the empirical bw scaling characteristics observed across the 2026-05 stoa + ariadne integration arcs.
>
> ### 16.1 The bw-fit matrix
>
> | Use case shape | Fit |
> |---|---|
> | Project-management substrate, incremental over months/years, < ~5k lifetime tickets | bw is the right choice |
> | Agent-team work-tracking with rich metadata + dependencies | bw is the right choice (Stoa's own use) |
> | Investigative workflow with structured evidence + hypotheses | bw is the right choice |
> | Audit trail for a workflow with versioned commits | bw is the right choice |
> | Catalog / reference corpus / knowledge-graph at 10k+ entries | NOT bw — use direct Postgres, beads-on-Dolt, or another DB engine |
> | High-write-rate bulk ingest workloads | NOT bw — even if total corpus is small |
> | Use cases requiring concurrent multi-agent cell-level merge | NOT bw (consider beads-on-Dolt if this is a real requirement) |
>
> The wall: bw's `TreeFS.Commit` rewrites the entire tree on every commit (no incremental tree update). At ~5k tickets and beyond, this becomes superlinear (~21s/ticket observed at 11,446 tickets; ~50-80h projected for full bulk-seed of that corpus). The matrix's "right choice" rows are use cases where the commit-rate stays well below the scaling wall; the "NOT bw" rows are where the scaling wall is structurally load-bearing.
>
> ### 16.2 The layered-architecture framing
>
> **bw is the write-side substrate; Ariadne is the read-side projection; hypergraph extends the projection to relational reads.** Each layer addresses a different read shape; do not force bw to be fast at reads — that is not its job in the stack.
>
> Concretely:
>
> - **bw (write-side).** Authoritative ticket-shape state. Audit-trail-grade durability. Incremental-author-friendly. Best when reads are spot-lookups against known IDs or small-set list operations. Native bw `list` / `show` / `history` are the right APIs at this layer.
> - **Ariadne (read-side projection).** A sidecar projection layer that mirrors bw's state into a queryable shape (typically SQLite + FTS5 + structured indices). Built for relational reads, full-text search, cross-ticket aggregation, and analytics queries that bw cannot serve fast at scale. The projection is eventually-consistent with bw; bw is the source of truth, Ariadne is the cached query layer.
> - **Hypergraph extension.** When the project's read shape includes many-to-many relationships across tickets / artifacts / concepts (knowledge-graph queries; multi-hop traversal; relational joins on derived attributes), the hypergraph layer sits on top of Ariadne. Same eventually-consistent pattern; richer query surface.
>
> The mental model substantive value: for any future Stoa-deployed project that needs both ticket-shape and knowledge-shape data, the projection layer is load-bearing — bw alone won't carry the knowledge-graph use case. The bw → Ariadne integration arc was proving exactly this: the bulk-seed wall was the empirical evidence that bw is for writes, Ariadne is for reads, and the two layers compose.
>
> ### 16.3 Decision rule
>
> When a future POLYBIUS session is considering bw for a project, walk the matrix at §16.1 first:
>
> 1. If the use case falls in a "right choice" row → bw is the right substrate. Standard stoa-deploy applies.
> 2. If the use case falls in a "NOT bw" row → use the alternative named in the matrix row. Document the choice; bw is not the universal answer.
> 3. If the use case spans both (ticket-shape + knowledge-shape, or write-intensive small + read-intensive large), apply the layered architecture from §16.2: bw for the write side, a projection layer for the read side. Don't force one tool to do both jobs.
>
> Empirical anchor: 2026-05-12, the bw → Ariadne integration arcs in ariadne-core-workspace. Project-tier relay at `HUMAN_relay_substrate_bw_scaling_findings_2026-05-12.md`. Research artifacts in `agents/research/bw-scaling-vs-mature-systems/` and `agents/research/bw-create-on-source-read/`. `ariadne--8fd.10` in the project-tier bw store documents the scaling-wall confirmation. Substrate ticket: `stoa--vmc`.

---

## 8. rno — fork-over-upstream + agent-time-latency budget

One substrate edit lands two memories from the same workspace-tier engagement. Verbatim from the ticket body; ADA copies into op-disc §17. Per A10 LOCK, inline placement (no substrate/memory/ directory in this arc).

### 8.1 operating-disciplines.md §17 (verbatim, new top-level section)

Lands after §16 (bw-fit matrix), before the "Agent-regime inverses" closer.

> ## 17. AI-team OSS-dep calculus + agent-time latency budget
>
> Two adjacent disciplines that surface together for any Stoa-deployed project depending on third-party open-source or designing for an agent-driven traffic profile. Replicated from workspace-tier memory files to substrate per `stoa--rno`.
>
> ### 17.1 Fork-over-upstream default for AI-team OSS dependencies
>
> The AI-team OSS calculus is inverted from human-dev convention.
>
> - **For a human dev team:** fork-and-tailor is expensive (maintenance burden, drift from upstream, ongoing sync cost). Upstream-issue-filing is cheap (open ticket, wait, maybe land). Default: file the issue; minimize the fork.
> - **For an AI agent team:** fork-and-tailor is cheap (the agent can carry the diff trivially; sync is also automatable). Upstream-issue-filing is expensive coordination overhead (write the issue with discipline; wait days or weeks; possibly never resolved; blocks the project's roadmap). Default: fork-and-tailor when the dep doesn't fit the specific use case. Upstream-contribute-back is optional and post-hoc.
>
> **The discipline:** when a Stoa-deployed project hits an upstream limitation that a small patch would resolve, the default decision is **fork the dep into the project's own workspace and apply the patch**. Upstream-PR is a downstream optional step, not a precondition. The 2026-05-12 bw arc validated this empirically: a 150 LOC `TreeFS`-incremental-tree-update patch is a small fork-and-tailor surface for the AI team but a substantial upstream coordination job (RFC, maintainer review, possibly multiple rounds, possibly rejected for design-fit reasons). The project-tier choice (pivot the use case rather than fork) was viable in that specific arc because the use-case pivot was cheap; the architectural option to fork was always available and cheap.
>
> Two adjacent considerations:
>
> - **The fork is not a fork in the destructive sense.** It's a local patch applied at install / build time, with the upstream remained as the canonical source. The diff is small; sync from upstream remains automatable.
> - **Upstream contribution stays optional.** If the patch's design happens to be a clean general improvement and the maintainer is responsive, contribute it back. If not, the patch lives in the project's substrate; the project is unblocked.
>
> ### 17.2 Agent-time latency budget for agent-driven traffic
>
> When a system's traffic is 100% agent-to-system (no human keystrokes in the request loop), the latency budget is **per-LLM-turn** (5-20s acceptable per round-trip), not **per-human-keystroke** (<1s expected). Optimizing for human-perceived-instant response is over-optimization for a system that won't be touched by human keystrokes.
>
> Engineering decisions shift on several axes:
>
> | Decision | Human-facing | Agent-facing |
> |---|---|---|
> | 1-2s synchronous ingest API call | unacceptable | acceptable |
> | Bulk operations spread over minutes | unacceptable | acceptable |
> | Async-queue-for-bulk plumbing | required | not needed unless wall-clock is a real bottleneck |
> | UI polish / streaming responses | high priority | lower priority than correctness / coverage |
> | Cold-start latency (process spin-up) | unacceptable | acceptable when the agent's own turn-budget absorbs it |
>
> The implication: for any Stoa-deployed project that has an agent-vs-human-consumer split, the substrate-canonical engineering trade-offs match the consumer profile. A project serving agents only does NOT inherit the human-facing latency budget; it inherits the agent-facing one, and the engineering choices follow.
>
> **Discipline:** when designing a new Stoa-deployed project, ask explicitly: who is the consumer of this traffic — humans, agents, or both? The answer drives the latency budget, the engineering choices, and where polish-effort lands. Same project-tier rule across the team.
>
> Empirical anchor: 2026-05-12, the bw → Ariadne integration arc's Phase 4 OPERATOR ACTION analysis. Workspace-tier memory files at `ariadne-core-workspace/memory/feedback_fork_over_upstream_issue.md` + `project_agent_time_latency_budget.md`. Substrate ticket: `stoa--rno`.

---

## 9. 14u — install.sh deploy-plan smoke beat

Two substrate edits land the discipline that adding new substrate files MUST update install.sh's hardcoded deploy lists, verified via a smoke beat.

Per the §6.1 decision above, the discipline lands at op-disc §8.4 (universal-team layer) and an analogous MAJOR_PLINY smoke-beat-discipline section.

### 9.1 operating-disciplines.md §8.4 — Substrate-edit smoke beats: install.sh deploy-plan check (verbatim)

Lands as new §8.4 in op-disc after the existing §8.3 activation-paste section. (Renumbering note from §6.3 above: existing §8.3 stays; new §8.4 is 14u; new §8.5 is 148.)

> ### 8.4 Substrate-edit smoke beats: install.sh deploy-plan check
>
> When an arc adds a new file under `substrate/templates/`, `substrate/skills/`, or any other location whose deploy is governed by `install.sh`'s hardcoded deploy-list arrays (`TEMPLATE_NAMES`, `CAPTAIN_NAMES`, `SKILL_NAMES`, or successors), the arc's Phase C smoke beats MUST include a beat that verifies install.sh's dry-run lists the new file in its deploy plan.
>
> Without this beat, re-installs at deployed tiers silently skip the new file. The substrate's source has the right content; the deploy mechanism doesn't know about it; downstream consumers run on the previous version forever (or until a human spots the gap during routine post-arc deploy verification, as happened on 2026-05-05 with arc-21's three new templates).
>
> **The smoke beat shape, for each new substrate file the arc adds:**
>
> ```bash
> bash substrate/install.sh --dry-run --target project --project-dir <test-dir> | grep <new-file-name>
> bash substrate/install.sh --dry-run --target subproject --parent-dir <test-parent> --subproject <slug> | grep <new-file-name>
> bash substrate/install.sh --dry-run --target user | grep <new-file-name>
> ```
>
> **Acceptance:** each new file appears in the dry-run deploy plan output for every applicable target mode (some files are mode-specific — e.g., templates skip subproject mode; check the install.sh source for the file class's deploy semantics before asserting which target modes apply).
>
> **If the file does NOT appear:** install.sh's hardcoded list needs updating in the same arc. Surface as a Phase C SMOKE FAIL with the exact missing file name + the install.sh fix needed (e.g., "add `new-template.md` to `TEMPLATE_NAMES` array in install.sh; 1-line addition at line ~110"). Do NOT proceed to ship; fix the install.sh wiring in the same feature branch.
>
> **Substrate-canonical implication for Arc 23 itself.** Per the §10 save-verdict location decision (Option A — user-tier extension), this arc adds no new files under `substrate/templates/` or `substrate/skills/`. The §8.4 discipline is established in the canon for future arcs to apply; Arc 23 itself does not exercise it. The follow-up substrate ticket (per §10.1) for substrate-promotion of save-verdict will be the first arc to exercise §8.4 against itself.
>
> Empirical anchor: Arc 21 commit `e2d8b63` added 3 new templates to `substrate/templates/` without updating install.sh's `TEMPLATE_NAMES`. Re-installs at deployed tiers silently skipped the new templates. Caught only during post-arc routine propagation deploy verification (`51397da` is the 3-line install.sh fix that should have landed in arc 21). Substrate ticket: `stoa--14u`.

### 9.2 MAJOR_PLINY.md §5.7 — Smoke-beat discipline (new subsection)

Lands as new §5.7 in MAJOR_PLINY.md (after §5.5 + §5.6 added in §4 above; existing §6 follows §5.7).

> ### 5.7 Smoke-beat discipline (`stoa--14u`)
>
> When you run Phase C smoke beats for an arc that touched substrate, your beat list MUST include the install.sh deploy-plan check from `operating-disciplines.md` §8.4 for each new substrate file the arc added. The discipline applies to:
>
> - Files added under `substrate/templates/` — covered by `TEMPLATE_NAMES` in install.sh.
> - Files added under `substrate/skills/` — covered by `SKILL_NAMES` in install.sh.
> - New CAPTAIN role files added under `substrate/` — covered by `CAPTAIN_NAMES` in install.sh.
> - Any future install.sh-managed file class.
>
> **The discipline is a Phase C smoke beat, not a Phase 2 build step.** ADA can add the file source in the build; install.sh's deploy-list update is a separate concern that the smoke beat surfaces if missed. If ADA naturally updates install.sh during the build (because the diff is obvious), the smoke beat still runs — it confirms the wiring is correct, even when the wiring was authored intentionally.
>
> Cross-ref: `operating-disciplines.md` §8.4. Empirical anchor: Arc 21 (`stoa--14u`). The discipline applies to this very arc's Phase 4 smoke beats; the smoke beat list in the directive's Phase 4 section already includes the `install.sh --dry-run` + `grep` pattern.

---

## 10. save-verdict skill schema extension

The verdict-emitting mechanism extends to carry INCOMPLETE and UNVERIFIABLE verdicts.

### 10.1 Decision: location of the schema extension

**Recon result (empirical file shape, verified 2026-05-12):**

```
$ ls ~/.claude/skills/save-verdict/
SKILL.md
$ ls ~/.claude/skills/copy-artifact/
SKILL.md
$ ls ~/.claude/skills/transcribe-bw-to-disk/
SKILL.md
```

The three sibling skills at user-tier each contain exactly one file: `SKILL.md`. There is **no** `_save_verdict.py`, no `_lib/byte_copy.py`, no `_lib/` directory anywhere under `~/.claude/skills/`. The SKILL.md prose references those helpers (lines 14, 97, 110, 130) but the helpers do not exist on disk; the skill is currently prose-form only. The references describe an intended structure that has not been built.

`substrate/skills/save-verdict/SKILL.md` does NOT exist. `install.sh`'s `SKILL_NAMES` deploys only `agent-author` and `check-substrate-updates` from `substrate/skills/`; `save-verdict` is a user-tier-only prose-form skill not under substrate's deploy management.

**Three options:**

- **Option A: User-tier extension.** Land the schema extension at `~/.claude/skills/save-verdict/SKILL.md`. Minimal change; no install.sh edit; no new substrate file. Tradeoff: the schema extension does not propagate to other Stoa-deployed projects on next install. Project-tier deployments that rely on save-verdict would not pick up the INCOMPLETE / UNVERIFIABLE schema extension unless their own user-tier already has the updated skill.
- **Option B: Promote save-verdict (prose-form) to substrate.** Copy `SKILL.md` to `substrate/skills/save-verdict/SKILL.md`, add to `SKILL_NAMES`. Tradeoff: ships a skill whose Python helpers are prose-referenced but do not exist on disk — install.sh would deploy a broken skill to every Stoa-deployed project unless the SKILL.md is rewritten to honestly signal "helpers TBD."
- **Option C: Expand Arc 23 scope to author the helpers.** Build `_save_verdict.py` + `_lib/byte_copy.py` as part of this arc, then promote the full skill. Significant scope expansion beyond the directive's stated charter.

**Decision: Option A — user-tier extension; file substrate-promotion follow-up ticket.** Rationale:

1. **Empirical falsification of the Option B premise.** Earlier reasoning assumed `_lib/byte_copy.py` existed and might be shared across user-tier skills. The actual file shape is: no Python helpers exist anywhere. The `_lib/` sharing concern is moot because nothing shares it. The user-tier skill is prose canon, not executable canon.
2. **Promotion of prose-form vapor would deploy a broken skill.** If install.sh's `SKILL_NAMES` gains `save-verdict` and the SKILL.md continues to reference `python skills/save-verdict/_save_verdict.py ...` against a directory that contains only SKILL.md, every Stoa-deployed project gets the broken invocation. The §8.4 smoke beat (grep for skill name in dry-run output) would pass vacuously — name presence, not helper presence.
3. **Directive's "Out of scope" ethos.** The directive states "Refactoring the existing PASS / FAIL / NEEDS-REVISIONS verdict path — the schema extension is additive only." Authoring `_save_verdict.py` from scratch is a substantive build, not an additive schema extension. Out of scope for Arc 23.
4. **The schema extension itself is the load-bearing deliverable.** Option A lands the INCOMPLETE / UNVERIFIABLE schema canon at the user-tier file where future invocations read it. The tier-mismatch concern (user-tier knows, substrate doesn't propagate) is real but bounded: this is currently a single-developer-tier substrate, and the substrate-promotion can be a clean follow-up ticket once the helpers are authored.

**Follow-up substrate ticket (new, post-Arc-23):** open `stoa--<new>` with title "Author save-verdict Python helpers and promote to substrate." Scope: author `_save_verdict.py` (byte-faithful save + sha256 round-trip per the SKILL.md procedure), author `_lib/byte_copy.py` (if cross-skill sharing emerges; otherwise inline), promote SKILL.md + helpers to `substrate/skills/save-verdict/`, add to `install.sh`'s `SKILL_NAMES`, and exercise the §8.4 smoke beat against the substrate promotion. That arc gets to be the worked-example of §8.4 applied to itself — Arc 23 establishes the discipline; the follow-up arc lands the substrate-skill that the discipline applies to.

**Arc 23 scope impact:** with Option A picked, this arc no longer touches `install.sh` for save-verdict (still touches it if any other substrate file is added — none are, per current scope). The §8.4 smoke beat's "this arc itself" application is also moot for Arc 23 — Arc 23 adds prose-only substrate edits, no new substrate files under template / skill / CAPTAIN directories. The discipline is established in the canon for future arcs to apply.

### 10.2 Schema extension specifics (LOCKED in shape per A6; DAEDALUS picks specifics)

The extension is **additive only**. The existing PASS / FAIL / NEEDS-REVISIONS paths are untouched. New fields are required only when the verdict shape requires them.

**Schema diff (free-form prose, not JSONSchema-validated — A6 DAEDALUS PICK):**

The save-verdict skill's input-contract section (the "Request bead fields" block) gains four optional inputs:

```yaml
inputs:
  verdict_shape: <pass | fail | needs-revisions | INCOMPLETE | UNVERIFIABLE>  # optional; default unset (caller's body carries the shape)
  quadrant_classification: <easy-easy | hard-easy | easy-hard | hard-hard>  # REQUIRED when verdict_shape is INCOMPLETE or UNVERIFIABLE
  coverage_description: <free-form prose>  # REQUIRED when verdict_shape is INCOMPLETE; describes what was checked, what was not, bound used, confidence interval
  sanity_check_performed: <free-form prose>  # REQUIRED when verdict_shape is UNVERIFIABLE; describes what cheap check WAS performed within ~1× normal probe budget
  recommended_next_step: <free-form prose>  # REQUIRED when verdict_shape is UNVERIFIABLE; describes recommended operator action
```

**Validation behavior:**

- `verdict_shape` is optional and informational; the skill's primary role is byte-faithful save with sha256 round-trip. The shape's enforcement (e.g., "INCOMPLETE requires coverage_description") is **caller-side**, not skill-side. The skill accepts the inputs, validates that required fields are present for the named shape, fails loud (exit 4) if not, and writes the verdict body.
- **Why caller-side enforcement, not JSONSchema (A6 DAEDALUS PICK).** Three reasons:
  1. **The skill's existing contract is "byte-faithful save."** Adding JSONSchema validation expands the skill's scope from "save what the caller hands over" to "validate semantic shape." This is a different seat's job (FORMAT_VALIDATE per the skill's "What this skill is NOT" section).
  2. **Free-form prose is already the pattern** for coverage / sanity / next-step. JSONSchema for free-form prose adds nothing — it would just check string presence, which a simple input-presence check covers.
  3. **The verdict shape's semantics live in op-disc §15.** The verifying CAPTAIN's role file teaches the seat to produce conformant bodies; the skill saves them. Centralizing the shape validation in the skill would require the skill to embed the framework, which is a tier mismatch.

**Failure modes added to the skill's existing exit-code list:**

- **`verdict_shape: INCOMPLETE` without `coverage_description`** → Exit 4 with diagnostic "INCOMPLETE verdict requires coverage_description per operating-disciplines.md §15.4."
- **`verdict_shape: UNVERIFIABLE` without `sanity_check_performed` OR without `recommended_next_step`** → Exit 4 with diagnostic "UNVERIFIABLE verdict requires sanity_check_performed AND recommended_next_step per operating-disciplines.md §15.4."
- **`verdict_shape: INCOMPLETE | UNVERIFIABLE` without `quadrant_classification`** → Exit 4 with diagnostic "INCOMPLETE / UNVERIFIABLE verdicts require quadrant_classification per operating-disciplines.md §15.4."
- **`quadrant_classification:` value not in the enum** → Exit 4 with diagnostic "quadrant_classification must be one of: easy-easy, hard-easy, easy-hard, hard-hard."

**Gates merge?** No (A6 LOCK). The skill saves the verdict; whether the verdict gates merge is PLINY's dispatch protocol decision (per MAJOR_PLINY.md §5.6 added above).

**File ADA edits (per §10.1 Option A decision):** `~/.claude/skills/save-verdict/SKILL.md` (user-tier file, outside the Stoa repo). The "Input contract" section gains the four new optional inputs. The "Failure modes" section gains the four new exit-4 cases. The "Procedure" section's step 2 (Validate inputs) gains the shape-conformance check.

**Caveat on the edit's executable scope:** the user-tier skill is currently prose-form (no `_save_verdict.py` exists on disk). The schema extension lands in the prose; the executable enforcement of the new exit-4 cases is moot until the Python helper is authored under the follow-up substrate ticket named in §10.1. The schema extension is canon-establishing; the enforcement implementation is downstream.

**No install.sh edit this arc.** No new substrate file is added under `substrate/skills/`; `SKILL_NAMES` is unchanged.

**No save-verdict-specific smoke beat this arc.** The §8.4 discipline applies to future arcs that add substrate files; Arc 23 adds prose-only substrate edits and no new substrate-managed files. Phase 4 smoke beats verify the prose deliverables landed correctly (section-heading presence, cross-reference resolution, wording-discipline checks per §3.5).

---

## 11. Self-referential acknowledgment

This arc modifies the role files of the verifying CAPTAINs (VERA, CATO, ARGUS, ZENO) that will verify the arc. The Phase 3 verification dispatches will read the **new** version of their own role files during verification.

This is not a circular dependency. It is the substrate updating itself in flight, and the design relies on three properties:

1. **Verifiers read what's on disk at dispatch time.** During Phase 3, VERA reads the new `CAPTAIN_VERA.md` (with §5.7 quadrant discipline + §5.8 STRABO-claim verification); CATO reads the new `CAPTAIN_CATO.md` (with §6.7 quadrant per finding + §6.8 empirical-env reproduction); ARGUS reads the new `CAPTAIN_ARGUS.md` (with §6.6 quadrant per risk); ZENO reads the new `CAPTAIN_ZENO.md` (with §6.6 quadrant per criterion). Each verifier's own dispatch is the first worked example of the framework applied to their seat.

2. **The framework's discipline applies to the verifier's own verdict on this arc.** VERA classifies its probes per quadrant in the verdict block, recording the classification in the new `quadrant_classification:` field. Most probes are easy-easy (file contains string; section heading present); a few are hard-easy (wording-drift across the four role files: hard to detect, cheap to verify once spotted). None are easy-hard or hard-hard for this arc's content shape — this is a doc revision arc, not a concurrency or synthesis-claim arc.

3. **The same is true for ARGUS's cold-audit of this very design.** ARGUS reads the new ARGUS role file as part of the design context (the design references the new §6.6 as a deliverable; ARGUS's own role file is being modified by the design ARGUS is auditing). The new §6.6 changes how ARGUS classifies risks; ARGUS's audit-of-this-design applies the new §6.6 to the design's own risks. The audit and the design's content are aligned in the same dispatch round.

The substrate-updating-itself property is intended steady-state behavior, not a bug. The gauntlet runs against it without special-casing. DAEDALUS notes the property here for cold-readers who might otherwise read the Phase 3 dispatches as if the verifiers were reading an older version of their role files.

---

## 12. Design decisions summary (for ARGUS's audit + ADA's build)

The locked-pre-dispatch A1-A11 decisions are documented in the directive; not repeated here. DAEDALUS's specific picks within the locked shape are below.

| Decision | Choice | Rationale | Reference |
|---|---|---|---|
| A6: schema extension validation | Free-form prose (not JSONSchema) | Skill's existing contract is byte-faithful save; semantic validation is a different seat's job | §10.2 |
| A6: gates merge? | No (LOCKED, but reaffirmed): caller-side enforcement of required fields per shape | The skill saves what the caller hands over; PLINY's dispatch protocol decides gating | §10.2 |
| A7: INCOMPLETE time/cost-box default | 10× normal probe budget | tp1 elevation anchor; balances asymmetric cost (missed catches > wasted tokens) and operator-disposition queue | §2.5 |
| A7: UNVERIFIABLE time/cost-box default | ~1× normal probe budget (sanity-check only) | The verifier confirms the quadrant classification, records, returns | §2.5 |
| A8: STRABO-verification sampling | `sampling: full` for substrate-tier-bound or upstream-project-bound; `sampling: 3` (bare integer) for routine in-project | Asymmetric cost: a fabricated citation in an upstream PR is reputational; in-project a sample suffices. YAML-canonical: keyword-or-integer (not `N=3`). | §4.1 |
| save-verdict location | User-tier extension only (`~/.claude/skills/save-verdict/SKILL.md`); file substrate-promotion follow-up ticket | User-tier skill is currently prose-form (no Python helpers on disk — verified empirically); promoting prose-form vapor would deploy a broken skill via install.sh. Authoring helpers is out of scope per directive's additive-only ethos. | §10.1 |
| save-verdict substrate promotion | Deferred to follow-up substrate ticket `stoa--<new>` (author Python helpers + promote) | Empirical recon showed `~/.claude/skills/save-verdict/` contains only `SKILL.md`; no `_save_verdict.py`, no `_lib/`. Earlier "Option B" assumption about `_lib/` sharing was moot. | §10.1 |
| 148 probe-coverage placement | op-disc §8.5 (universal-team layer); not duplicated in MAJOR_PLINY.md | Discipline applies to ADA + VERA + CATO; PLINY-only placement narrows audience | §6.1 |
| 14u smoke-beat placement | Both op-disc §8.4 (universal) AND MAJOR_PLINY §5.7 (orchestrator-specific framing) | Cross-tier discipline: op-disc carries the universal beat shape; PLINY carries the dispatch-time application | §9 |
| op-disc §8.4 / §8.5 numbering | §8.4 = 14u; §8.5 = 148 (preserve existing §8.3 activation-paste) | The A5 LOCK numbering assumed §8 had two subsections; current shipped op-disc has three; preserving §8.3 avoids cross-ref churn | §6.3 |
| nax retrospective discipline placement | MAJOR_POLYBIUS.md new §15 (after §14 substrate-update-check) | TIMING_LOG / retrospective discipline doesn't fit under §14 substrate-freshness; standalone section is honest scoping | §5.3 |
| STRABO claims-preliminary placement | CAPTAIN_STRABO.md §6.6 (under existing disciplines section) | Existing file has §7 verdict-format + §8 closer; new discipline lands under §6 (disciplines) | §4.2 |

---

## 13. DAEDALUS self-assessed weak points + ARGUS sign-off block

Per CAPTAIN_DAEDALUS role file §6.2 — the design author flags brittle assumptions and structural weak points; ARGUS names risks the author missed.

### 13.1 Weak point: tp1's "verifier-in-hard/hard quadrant" prose may not hold up under the pressure test as written

The framework's central justification is "the cost of not having this awareness is a verifying agent spinning forever in the hard/hard quadrant." But the framework's prescription for hard/hard is "verdict UNVERIFIABLE within ~1× normal probe budget" — which means the verifier doesn't actually spin forever, it pulls out fast. The narrative tension is: a verifier WITHOUT the framework spins forever (the failure mode); a verifier WITH the framework returns UNVERIFIABLE quickly (the prescription). The framework's value is the classification step, not the bounded budget.

This is intelligible to a careful reader but mildly counter-intuitive. ARGUS audit should pressure-test whether the §2 prose makes the "the classification step is what prevents the spin, not the budget" point legibly. If readers come away thinking "UNVERIFIABLE = ran out of time," the framework's discipline has been mis-communicated. Suggested ARGUS pressure-test: read §2.2 (the discipline rule) cold and confirm whether the "classify FIRST, then strategy follows from classification" sequence is the load-bearing point. If the prose reads as "strategy depends on time budget," the wording needs sharpening.

**Why this shape anyway:** the prose as written is honest about both the failure mode and the prescription. Smoothing the tension would over-claim (the framework cannot make hard problems easy; it can only make the seat exit honestly). DAEDALUS chose explicit framing over rhetorical smoothing.

### 13.2 Weak point: wording-drift risk across the four verifier role files

The four new sections (VERA §5.7, CATO §6.7, ARGUS §6.6, ZENO §6.6) all reference the same framework, all use the same quadrant labels, all share the same INCOMPLETE / UNVERIFIABLE vocabulary. Cross-file consistency on §3.5's five load-bearing strings is the biggest landmine of this arc.

ADA's build will produce four separate file edits across four files; without explicit string-discipline in the build, drift is the default outcome. §3.5 names the five strings and the constraint; CATO's Phase 3 cold-read should explicitly check the four files against each other.

**Why this shape anyway:** consolidating the four role-file sections into one canonical location (e.g., only in op-disc, with the role files just referencing it) would defeat the "each seat reads its own role file for seat-specific discipline" property. The role files NEED to carry the discipline in their own voice and with their own examples. Cross-file consistency is the cost; the property earned is per-seat legibility.

### 13.3 Weak point: save-verdict user-tier extension creates a substrate-vs-user-tier tier mismatch

§10.1 picks Option A (user-tier extension at `~/.claude/skills/save-verdict/SKILL.md`) after empirical recon falsified the Option B premise (no Python helpers exist on disk; the user-tier skill is prose-form only). The schema extension lands at user-tier; the substrate canon at op-disc §15 references INCOMPLETE / UNVERIFIABLE verdict shapes, but `substrate/skills/save-verdict/` does not exist and will not exist until the follow-up substrate ticket lands.

The tier mismatch is real: substrate doc says INCOMPLETE / UNVERIFIABLE are first-class verdict shapes; the executable enforcement (skill-side validation of required fields per shape) exists only at user-tier; Stoa-deployed projects that get installed-fresh do not automatically receive the save-verdict schema extension unless their developer's user-tier already has it.

**Why this shape anyway:** the alternative (promote prose-form vapor to substrate, deploy a broken skill via install.sh to every Stoa-deployed project) is structurally worse than the tier mismatch. The follow-up substrate ticket named in §10.1 closes the gap properly: author the Python helpers, promote the working skill, exercise §8.4 against the promotion. Arc 23 establishes the canon at op-disc §15 and lands the schema prose at user-tier; the follow-up arc lands the substrate-canonical executable.

**ARGUS pressure-test:** confirm the follow-up ticket scope as documented in §10.1 is concrete enough to be filed (not "track it; plan it" per `u--7yg.fix-bugs-now`). The §10.1 paragraph names the deliverables explicitly (`_save_verdict.py` byte-faithful save + sha256 round-trip; `_lib/byte_copy.py` if cross-skill sharing emerges; install.sh `SKILL_NAMES` add; §8.4 smoke beat applied) — this is a planning-grade scope, not a handwave.

### 13.4 Weak point: STRABO-verification `sampling: 3` for routine in-project

The A8 LOCK suggested N=3 as the routine sampling anchor; DAEDALUS picked it. But "3 of N citations" is a small sample if N=20 and the cited claims are heterogeneous (some hard-easy, some easy-hard, some hard-hard). The discipline names "prefer the load-bearing claims" but does not specify how the verifier identifies load-bearing without reading every claim first (at which point the discovery cost equals the full-sampling cost).

This is genuinely a hard scoping problem. The pragmatic answer is "the verifier reads the artifact end-to-end to identify candidates and samples 3 — full-read is fast, full-verification is not." The framework prose at §4.1 implies this but doesn't say it directly.

**Why this shape anyway:** specifying the exact sampling algorithm is over-engineering for the v0 discipline. The 80/20 case (in-project research with low-stakes propagation) is well-served by `sampling: 3` with verifier judgment. `sampling: full` is the right default for high-stakes propagation. The middle case (heterogeneous N=20 claims with mixed stakes) is a tail case the verifier surfaces via `sampling_concern:` for PLINY scope re-decision.

**Wire shape (canonicalized):** the YAML field is `sampling:` and accepts either the keyword `full` (string) or a positive integer (bare-integer form for sampled mode). An earlier draft used `sampling: N=3`, which embeds an `=` inside a YAML scalar and parses as a string with algebraic-name syntax. The canonical forms `sampling: full` / `sampling: 3` parse cleanly as YAML and read naturally in dispatch briefs.

### 13.5 Weak point: INCOMPLETE time/cost-box at 10× is a number-picked-with-rationale, not number-validated-empirically

The 10× multiplier has rationale (§2.5: asymmetric cost, operator-fatigue, easy escalation path) but no empirical calibration. Future arcs may surface that 10× is too low (verifier hits the bound on routine cases; INCOMPLETE proliferates) or too high (verifier burns tokens on cases that should have escalated earlier).

The framework's recovery is the dispatch brief — PLINY can explicitly authorize a higher bound for a load-bearing case. The bound is the floor, not the ceiling. But the choice of 10× is fundamentally a guess.

**Why this shape anyway:** no calibration data exists yet. Picking N=10 with explicit rationale is honest; picking N=10 and pretending it's empirically validated would be dishonest. Future arcs revise as data accretes.

### 13.6 Weak point: the §8.3 / §8.4 / §8.5 numbering pragma drifts from the A5 LOCK literal numbers

The directive's A5 LOCK table names §8.3 (14u smoke beats) and §8.4 (148 probe coverage). The current shipped op-disc already has §8.3 (activation paste from Arc 21). §6.3 of this design picks §8.4 (14u) / §8.5 (148) to preserve existing §8.3. This is a deviation from the LOCK as literally written, defended on prose-intent grounds.

**Why this shape anyway:** the LOCK's prose intent ("new subsections under §8 for 14u and 148") is satisfied by §8.4 / §8.5. The literal numbering in the A5 table (§8.3 / §8.4) appears to reflect a counting error at directive-authoring time — A5 cannot consistently mean "new §8.3 = 14u" when shipped op-disc already has §8.3 = activation paste. Renumbering the existing Arc 21 §8.3 to honor the LOCK's literal numbers would create design-vs-shipped audit drift against Arc 21's contract: the shipped substrate names a section §8.3 with specific content; reshuffling that anchor as a side effect of Arc 23 is a substantive change to a prior arc's deliverable, not a pure additive extension.

**Empirical note (correcting a prior draft).** An earlier version of this design also cited "cross-references to op-disc §8.3 from elsewhere in the substrate would also break" as supporting rationale. Verified via `grep §8\.3 substrate/` (excluding the arc-23 directive itself): zero hits. No substrate file outside this arc's directive references §8.3. The cross-ref-breakage claim was empirically false. The standing rationale is design-vs-shipped audit drift alone, which IS load-bearing (Arc 21's deliverable contract). DAEDALUS surfaces the deviation; ARGUS confirms the §8.4 / §8.5 pragma is acceptable, or routes back with instruction to renumber Arc 21's §8.3 → §8.5 and land 14u at §8.3, 148 at §8.4 (literal LOCK honoring with the audit-drift cost paid explicitly).

### 13.7 Residual question for ARGUS

- **Does the `stoa--148` probe-coverage discipline at op-disc §8.5 belong under §8 (Authoring downstream artifacts) at all?** §8.1 is positive references, §8.2 is scaffolding for downstream agents, §8.3 is activation paste. Probe coverage of fallback chains is a verifier/executor discipline, not strictly an "authoring downstream artifacts" discipline. ARGUS audit should flag whether §8 is the right home — alternative is a new top-level section. DAEDALUS chose §8 because the directive's A5 LOCK assigned 148 under §8.x and the discipline is genuinely about "authoring [probes] for downstream [verifier] consumption" — but the fit is looser than §8.1-§8.3.

---

## Ready for ARGUS audit — sign-off block

**Revision round 1 (2026-05-12, post-ARGUS-cold-audit REVISE verdict).** Five risks addressed:
- **R1** (string-discipline self-violation at §3.5): tightened verbatim prose in §3.2 (CATO) and §3.3 (ARGUS) to include bare `INCOMPLETE`, bare `UNVERIFIABLE`, and `verifier-spins-forever` per §3.5 row constraints; updated §3.5 rows 3, 4, 5 to record ZENO's structural exemption (ZENO uses `UNVERIFIABLE quadrant` qualifier form; no `quadrant_classification:` schema field; no `verifier-spins-forever` reference). Option (a) picked.
- **R2** (save-verdict promotion rests on falsified assumption): fell back to Option A — user-tier extension only; substrate promotion deferred to a new follow-up ticket once Python helpers are authored. §10.1 documents the empirical file shape (`ls` output) and the planning-grade follow-up scope. §10.2, §9.1 "this arc itself" paragraph, §12 decisions table all updated. Option (a) picked per directive's "additive-only" ethos.
- **R3** (inline draft-state narrative): stripped four "wait/actually/re-reading" passages — three ARGUS cited (§4.2 STRABO renumbering at line 247, §5.1 op-disc §6.7 placement at line 319, §5.3 POLYBIUS §15 placement at line 379) plus one additional ARGUS did not cite (§7.1 op-disc §16 placement at line 484). All four rewritten as clean assertions. Audited the rest of the design for analogous "wait / actually / re-reading" usage; remaining hits at lines 33, 105, 544, 545, 735 are content-legitimate (the word "actually" inside cited prose / "wait" inside quoted material / "re-installs" as compound noun).
- **R4** (§13.6 rationale falsified): kept the §8.4 / §8.5 pragma; rewrote both §6.3 decision rationale and §13.6 weak-point rationale to remove the false cross-ref-breakage claim. Standing rationale is design-vs-shipped audit drift against Arc 21's contract. §6.3 explicitly notes the empirical-falsification correction. Option (a) picked.
- **R5** (sampling `N=3` YAML awkwardness): canonicalized to `sampling: full` (keyword) / `sampling: 3` (bare integer for sampled mode). Updated §4.1, §5.5 PLINY protocol, §13.4 weak point, §12 decisions table. Option (b) picked — cleanest YAML; reads naturally in dispatch briefs.

**§12 decisions summary changed:** R2 changed the save-verdict location decision row (Option B → Option A) and added a new row for the deferred substrate promotion follow-up ticket. R5 changed the sampling-policy decision row's wording (`sampling: N=3` → `sampling: 3`).

```
ticket: stoa--pmp (Arc 23 epic) + child tickets stoa--tp1, fea, nax, 148, vmc, rno, 14u
design_artifact_path: agents/design/arc-23/design.md (this file)
status: completed (revision round 1)
verdict: pass (with self-flagged weak points; see §13)

design_decisions_made:
- A6 schema validation: free-form prose (not JSONSchema); rationale §10.2.
- A7 INCOMPLETE time/cost-box default: 10× normal probe budget; rationale §2.5.
- A7 UNVERIFIABLE time/cost-box default: ~1× normal probe budget (sanity check only); rationale §2.5.
- A8 sampling policy: sampling=full for substrate-tier / upstream-bound, sampling=3 (bare integer) for routine; rationale §4.1.
- save-verdict location: user-tier extension only (Option A); substrate promotion deferred to follow-up ticket; rationale §10.1.
- 148 probe-coverage placement: op-disc §8.5 only (not duplicated in MAJOR_PLINY); rationale §6.1.
- §8 numbering: §8.4 = 14u, §8.5 = 148 (preserve existing §8.3); deviation from A5 LOCK literal numbers documented in §13.6; rationale §6.3.
- nax retrospective discipline placement: MAJOR_POLYBIUS.md new §15 (standalone section, not under §14 substrate-freshness); rationale §5.3.
- STRABO claims-preliminary placement: CAPTAIN_STRABO.md §6.6 (under disciplines section, before §7 verdict format); rationale §4.2.

residual_questions_for_argus:
- Does the tp1 §2 prose make the "classification step is what prevents the spin, not the budget" point legibly? (§13.1)
- Is the four-file wording-drift discipline at §3.5 (with ZENO exemption now recorded) sufficient to prevent drift, or does the build need a stronger string-discipline mechanism? (§13.2)
- Is the §10.1 follow-up substrate ticket scope concrete enough to qualify as planning-grade per `u--7yg.fix-bugs-now`, or does ARGUS see a handwave? (§13.3)
- Is §8 ("Authoring downstream artifacts") the right home for the probe-coverage discipline (§8.5), or does it warrant a new top-level section? (§13.7)
- Is the §8.4 / §8.5 numbering pragma (§13.6) acceptable now that the rationale rests solely on design-vs-shipped audit drift (cross-ref-breakage claim retracted), or should the build renumber existing §8.3 (activation paste) to honor the A5 LOCK literally?

self_assessed_weak_points: (full prose at §13)
- §13.1: tp1 "verifier-spins-forever" prose has a counter-intuitive structure that may mis-read as "UNVERIFIABLE = ran out of time."
- §13.2: wording-drift risk across the four verifier role files; mitigated by §3.5 string-discipline list (with ZENO exemption recorded) but not eliminated.
- §13.3: save-verdict user-tier-only extension creates a substrate-vs-user-tier tier mismatch; closed by the planning-grade follow-up ticket named in §10.1.
- §13.4: STRABO-verification `sampling: 3` routine sampling has under-specified candidate-selection algorithm; YAML wire shape now canonical.
- §13.5: INCOMPLETE time/cost-box at 10× is number-picked-with-rationale, not number-validated-empirically.
- §13.6: §8.3 / §8.4 / §8.5 numbering deviates from A5 LOCK literal numbers; rationale rests on design-vs-shipped audit drift against Arc 21 (cross-ref-breakage claim retracted as empirically false).
- §13.7: §8 ("Authoring downstream artifacts") is a loose home for the probe-coverage discipline; alternative is a new section.

follow_ups (out of scope, surfaced for future arcs):
- File new substrate ticket `stoa--<new>`: "Author save-verdict Python helpers and promote to substrate." Scope per §10.1: `_save_verdict.py` (byte-faithful save + sha256 round-trip), `_lib/byte_copy.py` (if cross-skill sharing emerges), promote SKILL.md + helpers to `substrate/skills/save-verdict/`, add to `install.sh` `SKILL_NAMES`, exercise §8.4 smoke beat against the promotion. That arc is the worked-example of §8.4 applied to its own deliverable.
- Empirical calibration of the INCOMPLETE 10× multiplier across N future arcs that use it; revise op-disc §15.5 if a different N is empirically validated.
- A substrate-level mechanism for cross-file string-discipline (the five load-bearing strings at §3.5) — currently relies on CATO Phase 3 cold-read; a future arc may add a structural check.

summary: |
  Arc 23 lands the verification-complexity framework (INCOMPLETE / UNVERIFIABLE verdict shapes + 2x2 quadrant classification) as load-bearing scaffolding at operating-disciplines.md §15, with four verifier role-file cross-refs (VERA §5.7, CATO §6.7, ARGUS §6.6, ZENO §6.6) integrating the framework per-seat. Six supporting substrate-canon updates ride with it: fea (STRABO-verification via VERA §5.8 + STRABO §6.6 + PLINY §5.5+§5.6), nax (op-disc §6.7 N=1 + estimate-axes + PLINY §7.8 + POLYBIUS §15), 148 (CATO §6.8 empirical-env + op-disc §8.5 probe coverage), vmc (op-disc §16 bw-fit matrix), rno (op-disc §17 fork-over-upstream + agent-time latency), 14u (op-disc §8.4 install.sh smoke beat + PLINY §5.7). save-verdict skill schema extension lands at user-tier (`~/.claude/skills/save-verdict/SKILL.md`); substrate promotion deferred to a planning-grade follow-up ticket once Python helpers are authored (empirical recon confirmed no helpers exist on disk today). The most important weak point is wording-drift across the four verifier role files (§13.2); §3.5 names the five load-bearing strings, the cross-file constraint, and ZENO's structural exemption. The most important load-bearing design decision is the user-tier-only save-verdict extension (§10.1), correcting a prior draft that assumed Python helpers existed.
```
