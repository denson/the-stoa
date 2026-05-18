# SPEC_AUDIT — fresh-eyes audit of SPECIFICATION.md

**Status:** draft 2026-05-17, authored by project-tier POLYBIUS for the-stoa under the spec-audit engagement (paste at `HUMAN_paste-polybius-spec-audit-instruction.md`). Coordination ticket: `stoa--q58`.

**Audience:** (1) PRINCIPAL for review; (2) user-tier POLYBIUS (the spec's author) for edit.

**Discipline:** ARGUS-overlay — surface concerns; do **not** propose fixes. Fix-shape decisions belong to PRINCIPAL + user-tier POLYBIUS, not to this audit team. Internal contradictions are named; this audit does not pick a side.

**Method:** project-tier POLYBIUS read SPECIFICATION.md end-to-end (incl §14), the paired `docs/validation/stellation-SPECIFICATION.md`, the project-tier `CLAUDE.md`, and the substrate canon files SPECIFICATION.md cross-refs (`substrate/operating-disciplines.md`, `substrate/MAJOR_POLYBIUS.md`, `substrate/MAJOR_PLINY.md`, `substrate/skills/handoff-author/SKILL.md`). Cross-checked §12.3 ticket enumeration against `bw list --all --status open`. Cross-checked §12.4 working-tree state against `git status` + `git log` + `ls _drafts/`. Cross-checked §28 trailer claim on `bb12806` / `fcd68c0` / `6414397` via `git log --pretty='%(trailers)'`. No CAPTAINs dispatched — audit done directly per paste authorization ("you may also do audit work directly without dispatching, where it's cheaper"); engagement scope fit a one-seat direct read.

**N=1 honesty (per op-disc §6.7.1):** the recurring pattern this audit surfaces is **internal staleness across the §12 + §13 family** — specifically, the spec was written 2026-05-17 as Arc 37 was shipping; some sections were updated post-Arc-37, others were not. The pattern accounts for ~40% of the findings below. Where applicable, the pattern is named at the finding rather than re-named at every instance.

---

## Table of contents

1. [Ambiguities](#ambiguities)
2. [Contradictions](#contradictions)
3. [Cross-ref errors](#cross-ref-errors)
4. [Aspirational-vs-descriptive drift](#aspirational-vs-descriptive-drift)
5. [Missing pieces](#missing-pieces)
6. [Honest "I don't understand"](#honest-i-dont-understand)
7. [Self-applicability check (Pass 4 dispatch walk-through)](#self-applicability-check)
8. [Substrate-state-vs-spec mismatches](#substrate-state-vs-spec-mismatches)
9. [Naming / mnemonic feedback](#naming--mnemonic-feedback) *(optional)*
10. [Workplan-shape feedback](#workplan-shape-feedback) *(optional)*
11. [Out-of-scope observations](#out-of-scope-observations) *(optional)*
12. [Cross-coherence with `stellation-SPECIFICATION.md`](#cross-coherence-with-stellation-specificationmd) *(optional)*

---

## Ambiguities

### A1 — "regresses upward" reads paradoxically without inline gloss

**Cite:** §7.2 line 292: "Typical engagement starts in Mode 2 to scope, transitions to Mode 1 for build, may transition to semi-autonomous for long-running phases, **and regresses upward when escalations require re-engagement**."

**Readings:**
- "Upward" toward Mode 2 (highest PRINCIPAL involvement) — the meaning the table at §7.1 implies (Mode 2 sits at the top row).
- "Upward" toward semi-autonomous (the bottom row, but the "highest" maturity) — a fresh reader treating later-in-progression as "higher" gets the opposite direction.

Op-disc §10 line 468 ("**Regression upward is normal, not exceptional**") has the inline gloss that disambiguates and explicitly addresses the paradox. SPEC §7.2 borrows the phrase without the gloss.

### A2 — §5.7 bundled batches: shape choice unspecified

**Cite:** §5.7 line 238: "ADA lands them coordinated (single coherent commit OR commits per candidate)".

**Readings:**
- ADA picks the shape ad-hoc per arc.
- The directive picks the shape (it's a DAEDALUS / directive concern).
- The two options are observationally equivalent for downstream readers and the choice is invisible.

§13.7 Arc 40 bundles 9 candidates without naming the shape; the team activating against §13.5 / §13.6 / §13.7 must pick without spec guidance.

### A3 — "absorbed-by-X closures" anti-pattern lacks an operational test

**Cite:** §11 line 428: "**Glossing over technical debt with 'absorbed-by-X' closures** — if the underlying discipline-gap is real, the canon ships; 'informally working' is not a substitute for canon."

**Readings:**
- A specific past pattern PRINCIPAL has observed and named (an `absorbed-by-` close reason on a bw ticket).
- A general anti-pattern any closure-with-rationalization fits.

The spec doesn't cite the empirical anchor or name the bw close-reason syntax. A fresh team can't operationalize the test "is this closure an absorbed-by-X?" without the example.

### A4 — §12.3 "substrate-canon tickets" boundary unstated

**Cite:** §13.7 line 583: "After Pass 6 (Arc 40) ships: **zero open substrate-canon tickets at the-stoa except deferred-with-gating per §13.8.**"

**Readings:**
- All open bw tickets close (this finding's audit shows the spec-audit engagement just filed `stoa--q58` as a coordination ticket — does that violate "zero"?).
- Only tickets that ship substrate canon close (most non-substrate tickets — coordination, engagement, meta — fall outside the count).

Boundary undrawn between "substrate-canon ticket" and other open-ticket classes. §13.12 criterion 2 ("no deferred-without-plan tickets — no open P2 at the-stoa") tries to draw it (gates on P2), but §13.7 line 583 uses a different gate ("substrate-canon").

### A5 — §13.10 mechanical-check expectations carry implicit grace cases

**Cite:** §13.10 line 616: "§28 Co-Authored-By trailers present on post-Arc-35 squash-merge commits."

**Readings:**
- Strict: every post-Arc-35 squash-merge must carry trailers. (This audit observed `bb12806` Arc 37 squash-merge has **no** trailers — see §8 finding S2 — so Pass 8 would fail on this commit.)
- Lenient: trailers are expected on commits authored *after the §28 discipline + the stoa--6wp bug-fix landed*. The Arc 37 trailer drop is the empirical anchor for stoa--6wp itself, not a Pass-8 failure.

Pass 8's mechanical-check spec doesn't carve out the known-historical-exception, and stoa--6wp ships the fix forward (not backward). Whichever reading PRINCIPAL intends, the spec doesn't say which.

---

## Contradictions

### C1 — Handoff-author session-id record: three sources disagree on whether it's shipped

- **§10.1 property 1 (line 364):** "Each generation handoff produces a handoff doc (per the handoff-author skill) **and records the prior generation's session id(s)** so successor generations can `/resume` them." — reads as mandatory + shipped.
- **§12.5 (lines 514-515):** "Generation-handoff session-id record — the `/resume` lineage pattern in §10.1 requires recording prior-generation session ids so successors can spin them up. handoff-author skill (stoa--7e3) **covers within-handoff content but not the session-id-as-warm-reference pattern**; could fold into Arc 37 C6 or land as a small follow-up." — reads as future-work.
- **`substrate/skills/handoff-author/SKILL.md` step 6:** "**(Optional but recommended)** Record prior-generation session id(s) for /resume. Per the the-stoa `SPECIFICATION.md` §10.1 + §12.5 generational-lineage architecture, if the engagement may benefit from a successor agent `/resume`-ing the prior generation's terminal session, capture the session id(s) in a 'Generational lineage' section of the handoff." — reads as shipped-but-optional.

All three describe the same artifact; the three descriptions are mutually inconsistent (mandatory-shipped vs not-yet vs optional-shipped).

### C2 — §12.1 / §12.2 / §12.5 reflect pre-Arc-37 reality; §12.3 reflects post-Arc-37 reality

- **§12.1 line 433:** "35 arcs shipped at main." — Per §12.3, Arc 36 v2 (PR #16 `fcd68c0`) and Arc 37 (PR #17 `bb12806`) shipped today. Arc count is at minimum 37, and §12.1's bullet list does enumerate Arc 36 v2 but not Arc 37.
- **§12.2 line 449:** "Nothing currently dispatched. **Pass 3 (Arc 37) ready to dispatch when PRINCIPAL ratifies activation.**" — Per §12.3 closed list ("`stoa--86k + stoa--kt6 + stoa--wad + stoa--ntn + stoa--53u + stoa--7e3` (Pass 3 / Arc 37) — closed on `bb12806`"), Pass 3 has shipped.
- **§12.5 (lines 496-502):** "**Arc 37 candidates (substrate architecture batch):**" enumerates all 6 candidates as "no skill...", "not yet canonized", "no canon for ... model", etc. — present-tense not-yet. Per §12.3 same 6 tickets are closed.

Three subsections of §12 are at three different points in time within the same authoring session.

### C3 — §13.7 (Arc 40 plan) and §13.10 (Pass 8 check) interact in a way the spec doesn't resolve

§13.10's mechanical check requires "§28 Co-Authored-By trailers present on post-Arc-35 squash-merge commits." §13.7 C6 (stoa--6wp) ships the fix for the regression that drops the trailers on the Arc 37 squash-merge. Arc 37's squash-merge `bb12806` is post-Arc-35 AND has no trailers; the fix is forward-looking (subsequent PRs preserve trailers via the §5.10 ship-checklist addition). The spec does not state whether Pass 8 reads the Arc 37 commit as a failure-now-fixed or as a known-historical exception. Both readings exist in the prose.

### C4 — "absorbed-by-X" anti-pattern (§11) vs "deferred-with-gating" (§13.8)

§11 anti-pattern list rejects "absorbed-by-X" closures where the discipline-gap is real. §13.8 explicitly preserves two tickets (`stoa--tvc`, `stoa--myd`) with gating criteria as a sanctioned form of deferral. The two are reconcilable (gating-with-criteria is not "informal absorption") but the spec doesn't draw the line; a fresh team reading both could over-apply §11 to refuse §13.8 deferrals, or could under-apply §11 by labeling any deferral "gated."

---

## Cross-ref errors

### X1 — §13.13 references `§10.1.3` which does not exist

**Cite:** §13.13 line 677: "Build the meta-agent for cross-generation lineage analysis (**§10.1.3** / §12.5) — out of scope for spec-meeting; framing is described; implementation is post-spec."

§10.1 has §10.1.1 ("The per-arc shape (mechanics)") and then jumps to §10.2. No §10.1.2 or §10.1.3 exist. The meta-agent content sits as unnumbered property 3 of §10.1 body (lines 374-381).

### X2 — §14 PRINCIPAL editing notes references `§13.2` for "Definition of meeting the spec"

**Cite:** §14 line 716: "**§13.2 Definition of 'meeting the spec'** — are the criteria the right ones?"

§13.2 is "Pass 1 — Working-tree cleanup". The actual "Definition of meeting the spec" lives at §13.12.

### X3 — §13.10 closing line says "Pass 7" inside the "Pass 8" section

**Cite:** §13.10 line 605 heading: "Pass 8 — Mechanical-check pass". §13.10 line 622: "**Pass 7** produces an artifact at `agents/observation/spec-validation/mechanical-check-results.md`".

The artifact path matches Pass 8's scope ("mechanical-check-results.md"). The "Pass 7" is text-vs-heading drift.

### X4 — `## §12` parent header is missing

**Cite:** SPECIFICATION.md TOC walks `## §11 Out of scope` → `### §12.1 What's shipped at the-stoa` with no `## §12 Current state` header in between. (Confirmed via `grep '^#+ §' SPECIFICATION.md`.)

§12.1-§12.5 are H3 subsections without an H2 parent. Possibly intentional, possibly not.

### X5 — stellation-SPECIFICATION.md cross-refs to the-stoa SPECIFICATION.md miss two sections

- **stellation §7 line 7:** "the team's BEHAVIOR while building it is the substrate-validation evidence per the-stoa **SPECIFICATION.md §13.7**." — §13.7 is "Pass 6 — Arc 40 (small bundled hygiene)". Validation framing lives at §13.11 (Pass 9) and §13.12.
- **stellation §9 criterion 6 line 217:** "Substrate-validation evidence (criterion 6) feeds back to the-stoa **SPECIFICATION.md §13.7** Pass 6 observation trail." — Pass 6 has no observation trail; §13.11 does (`agents/observation/spec-validation/test-dispatch-trail.md`).
- **stellation §12 line 279:** "The team operates in semi-autonomous mode per the-stoa **SPECIFICATION.md §13.10**." — §13.10 is "Pass 8 — Mechanical-check pass"; mode-and-dispatch canon lives at §13.14.

### X6 — §6.7 + §7.1 mark shipped tickets as "in flight" / "shipping"

- **§6.7 line 272:** "Author-tag convention (Arc 36 / stoa--e39, **in flight**)" — per §12.3, stoa--e39 closed on `fcd68c0`.
- **§7.1 line 280:** "Three modes (canonized at §10 + §11; full progression canon **shipping in stoa--ntn**)" — per §12.3, stoa--ntn closed on `bb12806`. Verified at op-disc §10 lines 445-471 (progression canon present).

Status tense drift. Same pattern as §12.1 / §12.2 / §12.5 (see C2).

### X7 — §3.4 "(stoa--86k, scope-recut-for-spec)" parenthetical is post-Arc-37 stale

**Cite:** §3.4 line 97: "### §3.4 The two-team-per-project model (stoa--86k, scope-recut-for-spec)"

stoa--86k closed as Arc 37 C1 per §12.3 (canon shipped at `MAJOR_POLYBIUS.md` §19 + op-disc §29). The "scope-recut-for-spec" framing implies the ticket was held for this spec to define; in reality Arc 37 shipped its canon today before the spec finished.

### X8 — `§13.10` claim "Pass 7 produces an artifact" should reference Pass 8 (same as X3, kept here for the cross-ref tally)

(Already enumerated as X3; logged here so a count-of-cross-ref-errors tally sees N=8 distinct items rather than re-merging.)

---

## Aspirational-vs-descriptive drift

### D1 — §4.6 + §9.1 describe CAPTAIN_TIRO in present tense; TIRO is an Arc 38 candidate (open `stoa--ojz`)

**Cite §4.6 line 179:** "**CAPTAIN_TIRO** (bw substrate specialist) **is** the first such seat:" followed by descriptive present-tense ("TIRO does reads directly when delegated... TIRO never writes for another seat... TIRO advises on write syntax...").
**Cite §4.6 line 187:** "**TIRO ships as the structural fix.**" — present-tense "ships."
**Cite §9.1 line 338:** "**Specialist delegation:** for read queries (especially completeness audits) other seats **delegate to CAPTAIN_TIRO** per §4.6." — present-tense "delegate."
**Cite §2.2 table line 54:** TIRO row in the seat table without an "(unbuilt)" or "(Arc 38)" marker.

The activation paste for this audit explicitly flags this gap: "CAPTAIN_TIRO does NOT exist yet — it's a §13.5 Pass 4 Arc 38 candidate (stoa--ojz). The spec's §4.6 + §9.1 reference TIRO as the delegated-bw-query specialist, but you must use bw directly for this audit."

Per §13.12 criterion 1, "every spec section either describes shipped canon or is explicitly marked future work with filed ticket + gating criteria." `stoa--ojz` is filed; the gating is "ship as Arc 38 C1." But the §4.6 and §9.1 prose uses descriptive-present, not marked-future, framing. The §2.2 table row carries no future-work marker.

### D2 — §10.1 "Each generation handoff... records the prior generation's session id(s)" overstates a shipped-optional discipline

See C1 — `handoff-author/SKILL.md` step 6 is explicit "(Optional but recommended)." §10.1 reads as if recording is a property of the system rather than a per-handoff judgment call.

### D3 — §7.3 "Universal escalation triggers (any mode)" — op-disc §10 line 443 scopes the same list to "autonomous mode"

**Cite §7.3 line 296:** "Substance disagreement after one round-trip with peer; authorship/copyright/PRINCIPAL-final-say content; irreducible ambiguity blocking progress; peer silence > 60 min on open coord ticket; arc closure (when shipping public-facing work); PRINCIPAL-gate clauses per §25."
**Cite op-disc §10 line 443:** "**Universal escalation triggers (autonomous mode):** every seat surfaces to PRINCIPAL on (a) substance disagreement after one round with peer, (b) authorship/copyright/PRINCIPAL-final-say content, (c) irreducible ambiguity that blocks progress, (d) peer silence > 60 minutes on an open coordination ticket."

The spec generalizes "(autonomous mode)" to "(any mode)" without naming the scope-expansion or its empirical anchor. In HITL mode the same triggers may already be implicit (PRINCIPAL is in the loop), but the discipline as canonized at op-disc §10 doesn't currently universal-quantify across modes.

### D4 — §4.5 "/resume that session" + §10.1 "previous generations remain queryable indefinitely" — discipline canon not separately shipped

The /resume-prior-generation pattern is described as a structural property of the team across §4.5, §10.1, and §11 (anti-pattern: "Destroying prior-generation sessions before lineage value is exhausted"). Op-disc + role files have no shipped section on this. The handoff-author skill step 6 is the closest shipped artifact, and it covers only the *recording* half; the *invoking* half ("how does a successor decide to `/resume` vs spawn fresh? when is the resume-window closed by external factors like terminal death? what's the failure mode if the recorded session-id is stale?") is undocumented canon.

Per §13.12 criterion 1: no ticket filed for this gap that I could locate via `bw list --all --status open`. §12.5 names "Generation-handoff session-id record" and "Meta-agent for cross-generation lineage analysis" as future-work but neither covers the *invocation discipline* gap.

---

## Missing pieces

### M1 — How does the fresh team translate §13.5 prose into an `arc-38-build-directive.md`?

§13.5 enumerates the three Arc 38 candidates but doesn't enumerate `A1-Ak` LOCKED architectural decisions in the §5.1 directive structure. The team activating against the spec must do that translation. §5.1 lists the directive structure but the spec doesn't say who writes the directive when the spec itself partially specifies it. Adjacent gap: same applies for Arc 39 (§13.6) and Arc 40 (§13.7).

### M2 — The audit-driven spec edit is unscheduled

The activation paste says: "Audit findings inform a future user-tier POLYBIUS edit after PRINCIPAL review." The spec's §13.9 Pass 7 ("Spec accuracy reconciliation") is the post-Pass-6 rewrite. The audit-driven pre-Arc-38 edit is the *same activity at a different time*, and the spec doesn't acknowledge that activity exists. A fresh team reading the spec would not know that Pass 7 has effectively been split into two passes (now and later).

### M3 — `validate-spec` skill is named but undefined

**Cite §13.10 line 607:** "Author + run a `validate-spec` skill following the §27 mechanical-script / agent-inspection split pattern".

The skill doesn't exist (verified `ls substrate/skills/` — no `validate-spec/`). The team is expected to author it as part of Pass 8, but §13.10 phrases it as a tool the team uses rather than a thing the team builds. The build-vs-use ambiguity is small but real.

### M4 — Sub-project-tier deployment is referenced but not enumerated

**Cite §2.4 line 65:** "Sub-project tier (some projects have a workspace + a sub-project, e.g., ariadne-core-workspace / ariadne-core — each gets its own deployed team)".

§3 (substrate / deploy mechanism) describes the project-tier install. The sub-project install is named in `substrate/MAJOR_POLYBIUS.md` §10 (sub-project spawning) but §3 doesn't cross-ref. A fresh reader trying to understand what "sub-project tier" deployment looks like has to leave the spec to find the canon.

### M5 — No `stoa--*` ticket prefix discipline cross-ref to the bw prefix table

**Cite §9.1 line 334:** "Prefix per project: `stoa--`, `ariadne--`, `s4--`, `u--` (user-tier)". The spec doesn't describe how a new project's prefix is chosen, who approves it, or where this list is canonically maintained. Op-disc §29.3 has the prefix-namespace convention. Cross-ref is missing.

### M6 — §13.11 "stellation (or whichever name PRINCIPAL ratifies)" — naming-ratification step unscheduled

The fresh team executes Pass 9 against "the test project" but the test project's name is *ratified by PRINCIPAL* per the parenthetical. The spec doesn't say when the ratification happens. Before Pass 4? Before Pass 9? After Pass 6? The PRINCIPAL-gate is open without a placement.

---

## Honest "I don't understand"

### U1 — §13.14 "User-tier POLYBIUS QA passes happen at end of EACH arc per PRINCIPAL's pattern"

**Cite §13.14 line 690:** "User-tier POLYBIUS QA passes happen at end of EACH arc per PRINCIPAL's pattern."

What is "PRINCIPAL's pattern"? Is this a memory? An op-disc section? A non-canon folkway? A fresh team can't operationalize "per PRINCIPAL's pattern" without a citation. The QA-pass step is enumerated at §5.6 ("User-tier POLYBIUS picks up the QA pass invitation, runs independent live-verification, posts QA-pass signoff with notes-for-the-record, files any follow-up housekeeping tickets, signs off") — the gap is that §13.14 invokes the pattern by name without binding the reader to §5.6.

### U2 — §4.5 "Prior generations sit idle until queried"

**Cite §4.5 line 173:** "Prior generations sit idle until queried — no polling, no budget burn."

This reads as an empirical claim about the Claude Code session-persistence model. Is the claim that:
- (a) `/resume`-able sessions consume no resources at rest (the Claude Code session store holds them dormant);
- (b) the Stoa discipline is to not invoke them (so even if they would burn budget, the team doesn't trigger that);
- (c) both;
- (d) something else, e.g., the model provider's session-lifecycle behavior?

A fresh team operating Pass 9 might want to know which reading is the correct one before deciding whether to leave prior generations idle in the absence of an immediate query need.

### U3 — §5.5 "PLINY dispatches all three concurrently (or sequentially per arc preference)"

How does an arc express its sequencing preference? Is it a directive-LOCKED decision? An ad-hoc PLINY judgment? The §5.1 directive structure doesn't enumerate a "sequencing-preference" slot.

### U4 — §10.1 "meta-agents observe how the generations connect"

**Cite §10.1 (property 3) line 381:** "This is the system reflecting on itself at the corpus level: the substrate evolves not just because each generation observes its own work, but because meta-agents observe how the generations connect."

"Observe how the generations connect" — what is the artifact a meta-agent produces? A retrospective? A canon proposal? A new arc directive? §12.5 acknowledges the meta-agent is unbuilt; the question is what its **output shape** is in the spec's mental model. Without a shape, a future team can't author the meta-agent skill against a known contract.

### U5 — §3.3 "Per-class path convention" claim is non-actionable for skills

**Cite §3.3 line 95:** "Same pattern for skills, templates, etc."

The base / custom split for agents is well-defined (`.claude/agents/` vs `.claude/agents/custom/`). For skills, the substrate-deployed skills live at `substrate/skills/<name>/`; the project-deployed copies live at `.claude/skills/<name>/`. Where do project-custom skills live? `.claude/skills/custom/<name>/`? The spec defers to "same pattern" but the pattern is undocumented for skills specifically.

---

## Self-applicability check

**Walk-through:** can a fresh team execute §13.5 Pass 4 (Arc 38 dispatch) end-to-end as written?

### S1 — Directive-authoring step is missing from the §13.5 procedure

The team reads §13.5 ("C1: stoa--ojz — CAPTAIN_TIRO bw substrate specialist seat..."), §5.1 (Brief → directive), §5.2 (Dispatch). §5.1 says user-tier POLYBIUS (or PLINY for project-scoped work) "authors a build directive at `substrate/arcs/arc-N-build-directive.md` with **LOCKED architectural decisions** (A1-Ak)." §13.5 enumerates candidates but not LOCKED decisions. The team must do that authoring; the team would ask: "do I author the directive, or does user-tier POLYBIUS?" Spec is silent.

### S2 — Activation-paste authoring step is implicit

§5.2: "User-tier POLYBIUS authors two activation pastes". The fresh team is project-tier; if user-tier POLYBIUS is offline (the team is operating semi-autonomously per §13.14), the activation-paste authoring step has no owner. The substrate `paste-instruction-template.md` exists, but the spec doesn't direct the team to it.

### S3 — Toolset enumeration is uneven across candidates

§13.5 C1 (TIRO) prescribes "Toolset: Bash, Read, Grep, Glob." C2 (bj5) and C3 (gq1) do not enumerate toolsets. C2's deliverable is "Bring user-tier substrate into `check-substrate-updates` drift-check scope" — Bash + scripting authority needed but unstated. C3's deliverable is "substrate-component design principles ... operating-disciplines.md new section likely" — DAEDALUS-shaped, no toolset relevant. The unevenness is a small operational gap: a fresh team would ask whether C2 / C3 have toolsets that simply weren't typed, or whether the typing is deliberate signal.

### S4 — "Verify cleanup live per §5.10" in §5.6 — but §5.10 is op-disc, not local

§5.6 line 230: "Verifies cleanup live per **§5.10**" — per the spec preamble convention, bare §N refers to op-disc. Op-disc §5.10 does not exist (op-disc structure tops out at §30). The correct cross-ref is `MAJOR_PLINY.md §5.10` (signoff-accuracy), which §4.3 line 142 names. §5.6's bare §5.10 is a local-vs-op-disc cross-ref ambiguity — minor self-applicability friction.

### S5 — §13.14 "DAEDALUS sub-decisions that hit PRINCIPAL-gate criteria → BLOCK + surface immediately per §25"

§25 is op-disc PRINCIPAL-gate discipline. Op-disc §25.5 is the probe-design sub-case. §13.14 invokes BLOCK semantics correctly but doesn't say how a semi-autonomous team gets a PRINCIPAL response — by chat? bw cross-tier tag? PushNotification? The substrate has crons that PRINCIPAL is not necessarily watching live.

---

## Substrate-state-vs-spec mismatches

### S-A — §12.3 ticket enumeration matches `bw list --all --status open` (17 tickets — clean)

Independent live-verification at 2026-05-17T19:58 MDT via `bw list --status open --all` returns **17 open tickets**. §12.3 enumerates: 3 (Arc 38) + 2 (Arc 39) + 9 (Arc 40) + 1 (Pass 7) + 2 (deferred-with-gating) = 17. Per-id match:

- `stoa--bj5`, `stoa--ojz` (Arc 38 P2 + P2) ✓ — but §12.3 also lists `stoa--gq1` (P3) as Arc 38. bw shows `stoa--gq1` open at P3 ✓.
- `stoa--utn`, `stoa--ezj` (Arc 39 P3+P3) ✓.
- `stoa--3sz`, `stoa--5sr`, `stoa--dhc`, `stoa--n2e`, `stoa--58b`, `stoa--6wp`, `stoa--3ml`, `stoa--ezp`, `stoa--pqn` (Arc 40) ✓.
- `stoa--6k1` (Pass 7) ✓.
- `stoa--tvc`, `stoa--myd` (deferred-with-gating) ✓.

No drift between §12.3 and bw reality. ✓

### S-B — §12.4 working-tree state has multiple drifts

**Cite §12.4 line 490:** "All Pass 1 + Pass 2 work committed + pushed (8 commits since Arc 35: `bd3e03a` substrate cleanup; `127f39b` spec docs; `0e76e5e` case-study PDF preservation; `594662e` §12 post-Pass-1 update; `e71615f` Arc 36 v2 dispatch artifacts; `fcd68c0` Arc 36 v2 PR merge; `8ced17c` Arc 36 v2 paste archival)."

- **Count says 8; list has 7 SHAs.** Off-by-one in the prose.
- **Stale since Arc 37 ship.** `git log` shows 7 additional commits since Arc 35 the spec doesn't list: `28155f7` (Arc 36 directive tracking), `27ddf8e` (Arc 37 directive tracking), `bb12806` (Arc 37 ship), `fa22ab5` (Arc 37 paste archival), `3131fd6` (TIRO add), `4f09cb8` (§12+§13 ticket-accounting pass), `d1f758e` (spec-audit activation pastes).
- **`_drafts/skill_handoff_author.md` no longer present.** §12.4 line 492: "`_drafts/skill_handoff_author.md` remains as the Arc 37 C6 source." `ls _drafts/` returns empty. Arc 37 C6 (`stoa--7e3`) shipped at `bb12806`; the draft was consumed into `substrate/skills/handoff-author/SKILL.md`. (Verified the deployed SKILL.md exists; §10.1 etc. are cross-referenced from its frontmatter.)

### S-C — §13.10 Pass 8 check would surface `bb12806` as a trailer-missing commit

Live-verified via `git log --pretty='%(trailers)' bb12806`: empty output (no trailers). Same query on `fcd68c0` (Arc 36 v2) and `6414397` (Arc 35) returns the expected `Co-authored-by: CAPTAIN_DAEDALUS_the-stoa ...` + `Co-authored-by: CAPTAIN_ADA_the-stoa ...` chain. `bb12806` (Arc 37 squash-merge) is the empirical anchor for stoa--6wp; Pass 8's "post-Arc-35 squash-merge commits" check would fail on it. See A5 + C3 for the spec-side ambiguity this surfaces.

### S-D — §12.1 "35 arcs shipped at main" — actual count is 37

Per `git log --oneline | grep -E '^[a-f0-9]+ Arc'` style scan: Arc 36 v2 (`fcd68c0` PR #16), Arc 37 (`bb12806` PR #17) both shipped on 2026-05-17. §12.1 lists Arc 36 v2 in a separate bullet but the "35 arcs shipped" prose is pre-Arc-36-and-37.

### S-E — `.claude/.substrate-last-check` modified in working tree

`git status` shows `M .claude/.substrate-last-check` (uncommitted). §12.4 line 492 acknowledges this as "auto-modified by substrate-check skill on each run; ignorable churn." ✓ — included for completeness; not an audit finding.

### S-F — `_drafts/` directory exists but is empty; spec acts as if `skill_handoff_author.md` is still there

Already noted in S-B; called out separately for the Pass 8 `_drafts/ contents match §12.4's keep-list` check (§13.10 line 614) — Pass 8 mechanical check would fail because `_drafts/` no longer contains the named keep-item.

---

## Naming / mnemonic feedback

### N1 — "CAPTAIN_TIRO" carries a "novice" connotation that may compete with the expert-specialist role

Latin `tiro` = "novice / new recruit / apprentice." Cicero's literate slave-secretary Marcus Tullius Tiro is the figure the substrate canon presumably means (Tiro invented Tironian notes / shorthand and was a master scribe — apt for a bw-mechanics specialist). A reader who lands on the surface Latin meaning first sees a "novice" seat presented as the expert, which is a small but real surface friction. The audit doesn't prescribe an alternative; only notes that the mnemonic's first-read meaning works against the role unless the reader knows the Marcus Tullius Tiro reference.

### N2 — "stellation" lands well as the test-project name

The project is a constellation viz over bw tickets; "stellation" evokes star formation, polyhedron-extension, and astronomical extension all simultaneously. The metaphor-load is high in a tight name. ✓ — included for explicit-confirmation honesty per paste guidance.

---

## Workplan-shape feedback

### W1 — Arc 40's 9-candidate bundle is the largest in the substrate's history

Per §12.1: Arc 32 (5 candidates), Arc 34 (4), Arc 37 (6). Per §13.7: Arc 40 (9). Per §12.1's Arc 36 v2 line: "5 DAEDALUS rev cycles (most of any arc); design grew 1033 → 2152 lines."

Pattern observation (N=4, not statistically anchored): rev-cycle count appears to correlate with candidate count and design complexity. Arc 40 carries 9 candidates with 1-50 LOC each per §13.7 — per-candidate complexity is low, but cumulative scope (operating-disciplines.md changes across §6, §20, §28.3, MAJOR_PLINY.md §5.10, MAJOR_POLYBIUS.md, CAPTAIN_VERA.md, CAPTAIN_DAEDALUS.md, plus 2 cross-ref edits + 2 SKILL.md author edits + Arc 36 follow-ups) touches 7+ canon files. DAEDALUS-design-doc shape for 9 candidates in one arc may strain ARGUS audit capacity in a way Arc 36's 5-candidate bundle already strained.

The audit does not prescribe split vs no-split; the workplan-shape pattern is the surfaced observation. PRINCIPAL + user-tier POLYBIUS can weigh against precedent.

### W2 — Pass 4 (Arc 38) bundle mixes scope-shapes

Arc 38 bundles:
- C1 (TIRO): new role file + install.sh deploy wiring + cross-refs from 3 substrate files.
- C2 (bj5): tool extension (check-substrate-updates skill scope expansion to user-tier).
- C3 (gq1): substantive new substrate-canon section on substrate-component design principles.

Three different scope-shapes (new-seat, tool-extension, new-canon-section). Arc 37 was unified-shape (6 substrate-canon sections under the substrate-architecture-canonification theme). Arc 38's mixed-shape may make the directive's LOCKED-decision matrix harder to author cleanly; the DAEDALUS design.md may have to span three orthogonal vocabularies.

### W3 — Pass 4 → Pass 5 → Pass 6 sequencing puts the largest+most-mixed bundle (Arc 40) last

Pass-4-then-5-then-6 is the §13 explicit order. Arc 40 (largest + most-cross-ref-heavy) lands AFTER Arc 38 (new seat) and Arc 39 (new substantive discipline). If Pass 6's 9-candidate bundle slips or surfaces friction, the sequencing has no recovery — Pass 7 spec-recon depends on Pass 6 done. An alternative ordering (largest-bundle-first to surface friction early) is structurally available but isn't taken; the spec doesn't say whether the small-last ordering is deliberate.

---

## Out-of-scope observations

### O1 — Pre-existing Tier-0 bw history not enumerated in §12.1 lineage

§12.1 enumerates Arcs 25-36 v2 with one-line characterizations. Arcs 1-24 carry the project from initial scaffolding to credential-discipline — these arcs DO exist (`substrate/arcs/arc-1-build-directive.md` through `arc-24-build-directive.md` present, plus `arc-z-consolidation-build-directive.md`). The §12.1 picture starts at Arc 25 without marking the truncation. A fresh team reading §12.1 might infer Arc 25 is the project's first canonification — it isn't.

### O2 — Stellation has a `bw prefix` (`stell--`) defined in stellation-SPECIFICATION.md §12 but no the-stoa-side mention

This is acceptable (stellation is downstream; its prefix lives in its own spec). Surfacing for PRINCIPAL confirmation that this is intentional — the the-stoa spec's §9.1 prefix list doesn't include `stell--` because stellation is a future test-project not yet a peer Stoa-deployed workspace.

### O3 — `app/` and `docs/case-study/` are mentioned passively in §10.2 / §10.4 but not load-bearing in §12 / §13

§10.2 mentions ariadne-core / sector-4 / railway_stoa as project examples. §10.4 mentions the case-study doc and architecture-kg.html. §12 / §13 do not describe what those artifacts' role is in spec-meeting. (Per §13.13 line 673, "Build product features for any non-validation consumer workspace ... — those are post-spec work motions" — explicitly out-of-scope. Confirming PRINCIPAL intent is that the case-study + app are non-blocking for spec-met.)

---

## Cross-coherence with `stellation-SPECIFICATION.md`

### Y1 — stellation spec is internally consistent within itself; cross-refs INTO the-stoa SPECIFICATION.md are off by section number (already enumerated as X5)

X5 captures the §13.7 / §13.10 mis-pointers (Pass 6 / Pass 8 vs Pass 9 / Pass 9-or-§13.14 targets). No additional findings beyond X5.

### Y2 — stellation §6 "Out of scope" list and the-stoa §11 anti-patterns list are non-overlapping in shape

stellation §6 enumerates product-feature out-of-scope items (no WebGL, no live bw integration, no auth). the-stoa §11 enumerates discipline-anti-patterns. The two are different categories and don't conflict. stellation §7 explicitly extends the-stoa §11 with project-specific anti-patterns (animation gratuity, premature 3D, etc.). The interaction is clean. ✓

### Y3 — stellation §9 validation criterion 6 expects the team to self-apply §28 trailers — which Arc 37 squash-merge has demonstrated can drop them

Per S-C (above): the Arc 37 squash-merge has empty trailer output. stellation §9 criterion 6 ("`git log` shows §28 trailers on CAPTAIN commits") will inherit the same Pass-8-style trailer-check exposure that stoa--6wp captures. If Pass 6 (Arc 40) lands before Pass 9 (test-project dispatch), the fix is in flight when stellation activates and the new project's first squash-merges are protected. If Pass 9 dispatches BEFORE Pass 6 lands, the test team would replicate the regression. The spec's sequencing (§13.7 before §13.11) does in fact put the fix first, so this is a non-issue at the sequencing level — but PRINCIPAL may want to confirm sequencing intent makes stoa--6wp a hard blocker for Pass 9.

---

## Closing observation (audit-level, not category-coded)

The audit's structural N=1 finding is **§12 + §13 internal staleness**: the spec was authored across the same workday Arcs 36 v2 and 37 shipped, and three subsections (§12.1, §12.2, §12.5) reflect the substrate state *before* Arc 37 ship while one subsection (§12.3) reflects the state *after*. §10.1 + §12.5 + the deployed `handoff-author/SKILL.md` are also at three different points (C1).

The pattern is the same shape as op-disc §19.7 idle-retrospective-narrative confabulation (closed-tickets-as-current-accomplishment) — but inverted: here the spec narrates **un-shipped reality as still-future** for canon that has already shipped this same workday. The Arc 37 work was actively happening as user-tier POLYBIUS authored the spec; sections written earlier in the workday have not been refreshed against the close-of-day substrate.

The fix-shape decisions for these findings belong to PRINCIPAL + user-tier POLYBIUS per ARGUS-discipline. This audit does not propose them.

---

## Self-application note (per activation paste §8 "Self-application")

The activation paste asked: "If you catch yourself slipping any of these [§6 multi-checker, §19.6 attestation, §7 author-tag, §5.10 signoff-accuracy] during the audit, that's a piece of audit feedback."

Slip surfaced: **single-checker by design for this engagement.** This audit was done direct by one project-tier POLYBIUS seat without dispatching ARGUS / CATO / BARTLEBY / ZENO sub-CAPTAINs (the activation paste explicitly authorized "you may also do audit work directly without dispatching, where it's cheaper"). The §6 multi-checker discipline is therefore *not* satisfied for this audit; a fresh second-checker (PRINCIPAL or user-tier POLYBIUS in review) is the structural multi-checker step.

Live-verification was applied to substrate-state claims (categories 3 + 8) via `bw list --all`, `git log --pretty='%(trailers)'`, `git status`, `ls _drafts/`, and direct Read of cited canon files; this satisfies the §19.6 attestation-honesty discipline within the single-checker boundary.

[from: polybius-the-stoa]
