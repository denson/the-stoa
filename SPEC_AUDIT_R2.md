# SPEC_AUDIT_R2 — second-pass audit of SPECIFICATION.md after fold-in

**Status:** draft 2026-05-17, authored by project-tier POLYBIUS for the-stoa under the spec-audit R2 engagement (paste at `HUMAN_paste-polybius-spec-audit-r2-instruction.md`). Coordination ticket: `stoa--gwm`.

**Audience:** (1) PRINCIPAL for review; (2) user-tier POLYBIUS (the spec author + fold-in author) for next-pass edit.

**Discipline:** ARGUS-overlay — surface concerns; do **not** propose fixes. This is an *iteration audit* on the fold-in commit `4a12358` (+ companion `d0cbc84`), not a fresh end-to-end audit.

**Scope under audit:**
- `SPECIFICATION.md` at commit `4a12358` (post-fold-in).
- `substrate/skills/handoff-author/SKILL.md` at commit `d0cbc84` (mandatory-upgrade companion).
- Live bw state (18 open tickets per `bw list --status open --all` at 2026-05-17T20:25 MDT).
- `git log` (since Arc 35 ship `6414397`, 17 commits chronologically through `26dc371`).
- `docs/validation/stellation-SPECIFICATION.md` (for the X5 / Y1 cross-ref status).

**Method:** project-tier POLYBIUS read SPECIFICATION.md end-to-end against SPEC_AUDIT.md's 49 findings (A1-A5, C1-C4, X1-X8, D1-D4, M1-M6, U1-U5, S-A through S-F, N1-N2, W1-W3, O1-O3, Y1-Y3) and the 4 PRINCIPAL-ratified decisions (C1 / C3+A5 / W1 / C4). Cross-checked the §12.3 enumeration against `bw list --all`. Cross-checked the §13 Pass-N references against the new numbering for stale references. Cross-checked the bb12806 carve-out wording in §13.11 against the source-ticket framing. No sub-CAPTAINs dispatched — single-seat-direct audit per R1 precedent + paste authorization; engagement scope (~30-60 min) fit a direct read.

**N=1 honesty (per op-disc §6.7.1):** The R2 closing observation matches the R1 closing observation almost exactly — the **§12 internal staleness pattern has recurred** at a different inflection point. R1 saw §12.1/§12.2/§12.5 lag the post-Arc-37 substrate while §12.3 was fresh. R2 sees §12.3 lag the post-W1-split state while §12.5+§13.7+§13.8 are fresh. Same shape; different inflection. The §12 staleness pattern is **not closed at spec-edit level**; the fix-shape may be structural rather than per-edit (see §6 closing observation).

---

## Table of contents

1. [Per-finding verification table (R2.1)](#per-finding-verification-table-r21)
2. [New issues found (R2.2)](#new-issues-found-r22)
3. [Substrate-state re-check (R2.3)](#substrate-state-re-check-r23)
4. [PRINCIPAL ratification verification (R2.4)](#principal-ratification-verification-r24)
5. [Self-application verdict (R2.5)](#self-application-verdict-r25)
6. [Closing observation — meta-pattern across both audits](#closing-observation--meta-pattern-across-both-audits)

---

## Per-finding verification table (R2.1)

Verdict legend: **✓** addressed correctly · **△** addressed with new concerns · **○** not addressed / partially addressed · **D** deliberately deferred · **n/a** optional R1 signal, no fix expected.

### Ambiguities (A1-A5)

| R1 ID | Verdict | Verification |
|---|---|---|
| A1 — "regresses upward" gloss | ✓ | §7.2 line 292 carries the inline gloss + cross-ref to op-disc §10. Clean. |
| A2 — §5.7 bundled batch shape choice | D | Deferred to Pass 8 reconciliation per commit message. Acceptable — clarification ask, not canon gap. |
| A3 — absorbed-by-X operational test | D | Deferred to Pass 8. Acceptable — no empirical anchor was required to land. |
| A4 — §12.3 substrate-canon ticket boundary | ○ | NOT addressed. §13.13 criterion 2 still uses "no open P2" gate (line 689); §13.8 closing sentence uses "zero open substrate-canon tickets" gate (line 605); the two vocabularies remain unreconciled. The boundary the R1 finding named is still undrawn. |
| A5 — Pass 8 mech-check carve-out for bb12806 | ✓ | §13.11 line 642 has explicit "EXPLICIT CARVE-OUT for `bb12806`" + forward-only check semantics. Clean. |

### Contradictions (C1-C4)

| R1 ID | Verdict | Verification |
|---|---|---|
| C1 — handoff session-id record (mandatory vs optional vs future-work) | △ | `substrate/skills/handoff-author/SKILL.md` step 6 body says **MANDATORY** (line 44, commit d0cbc84) ✓. §10.1 line 366 reads as mandatory + cross-refs the SKILL.md upgrade ✓. §12.5 "Generation-handoff session-id record" item removed ✓. **New concern:** SKILL.md frontmatter `description:` (line 4) still reads "Optionally records the prior-generation session id for /resume per SPECIFICATION.md §10.1 + §12.5 generational-lineage architecture." The frontmatter description and the body now contradict each other within the same file. See new issue NC2 below. |
| C2 — §12.1/§12.2/§12.5 pre-Arc-37 vs §12.3 post-Arc-37 | △ | The specific R1 instance is addressed: §12.1 refreshed to "37 arcs" + Arc 37 substantive line; §12.2 refreshed to post-Arc-37 + Pass 7 spec-recon as current activity; §12.5 refreshed for Arc 37 ship + Arc 38/39/40/41 candidates. **New concern:** the *pattern* recurred at a different inflection. §12.3 is now stuck at pre-W1-split state while §12.5+§13.7+§13.8 reflect post-W1-split state. See new issues NC1 + NC3 + NC4 below + §5 self-application verdict. |
| C3 — §13.7 Arc 40 vs §13.10 Pass 8 carve-out interaction | ✓ | §13.11 (new Pass 9) line 642 has the carve-out wording explicitly resolving the prior tension. §13.7 line 593 cross-refs the carve-out at "Pass 9 §13.11" (semantically correct for the carve-out itself; see NC5 about the *sibling* Pass-9-vs-Pass-10 reference in the same line). Clean for C3. |
| C4 — gated-deferral vs absorbed-by-X anti-pattern distinguishing | ✓ | §13.9 line 611 has explicit distinguishing prose: "Distinction from §11 anti-pattern 'absorbed-by-X closures': deferral-with-gating has *explicit trigger conditions* + a *filed ticket with a concrete fix-shape* ... The §11 anti-pattern is closure-or-deferral *without* explicit criteria ..." Clean. |

### Cross-ref errors (X1-X8)

| R1 ID | Verdict | Verification |
|---|---|---|
| X1 — §13.13 references nonexistent §10.1.3 | ✓ | §13.14 (renumbered from old §13.13) line 703: "Build the meta-agent for cross-generation lineage analysis (**§10.1 property 3** / §12.5)". Clean. |
| X2 — §14 references §13.2 for "meeting the spec" | ✓ | §14 line 743: "**§13.13 Definition of 'meeting the spec'**". Correct cross-ref. Clean. |
| X3 — §13.10 Pass 8 section text says "Pass 7" | ✓ | §13.11 (new Pass 9 mech-check) line 648: "**Pass 9** produces an artifact at `agents/observation/spec-validation/mechanical-check-results.md`". Cleanly renumbered through the W1 split. |
| X4 — `## §12` parent header missing | ✓ | Line 433: "## §12 Current state (snapshot)" present. Clean. |
| X5 — stellation-SPECIFICATION.md cross-refs into the-stoa SPECIFICATION.md miss two sections | ○ | NOT addressed. The fold-in commit only touched `SPECIFICATION.md`; `docs/validation/stellation-SPECIFICATION.md` was untouched. Verified via `git show --name-only 4a12358 \| tail` — only SPECIFICATION.md changed. Stellation still cross-refs §13.7 for "substrate-validation evidence" (lines 3 + 7 + 217) and §13.10 for "semi-autonomous mode" (line 279). The W1 split has now made the §13.10 cross-ref *worse* in the new numbering: §13.10 is now Pass 8 spec-recon, not mode-and-dispatch (which is §13.15 in the new numbering). Same shape for §13.7: it's now Pass 6 Arc 40 hygiene (a 4-candidate bundle), not validation. The fix-shape requires editing stellation-SPECIFICATION.md as well. |
| X6 — §6.7 + §7.1 mark shipped tickets as "in flight" / "shipping" | ✓ | §6.7 line 272: "shipped at `fcd68c0`"; §7.1 line 280: "shipped Arc 37 / stoa--ntn at `bb12806`". Clean. |
| X7 — §3.4 "(stoa--86k, scope-recut-for-spec)" parenthetical | ✓ | §3.4 line 97: "(shipped Arc 37 as stoa--86k → MAJOR_POLYBIUS.md §19)". Stale framing replaced with shipped-ticket framing. Clean. |
| X8 — duplicate of X3 (count separator) | ✓ | Same as X3. |

### Aspirational-vs-descriptive drift (D1-D4)

| R1 ID | Verdict | Verification |
|---|---|---|
| D1 — §4.6 + §9.1 + §2.2 describe CAPTAIN_TIRO in present tense; TIRO is Arc 38 candidate | ✓ | §2.2 TIRO row marked "*(per Arc 38 / stoa--ojz; not yet shipped)*". §4.6 line 179 prefixed with "*spec'd 2026-05-17; ships in Arc 38 per stoa--ojz; descriptive paragraphs below use present-tense as forward design language*". §4.6 line 187 "TIRO ships" → "TIRO **will ship**". §9.1 line 340: "**Specialist delegation (post-Arc-38):**" + "**Until Arc 38 ships TIRO**" fallback discipline. All three sites carry forward-design qualifiers consistently. Clean. |
| D2 — §10.1 "records the prior generation's session id(s)" overstates shipped-optional | ✓ | §10.1 line 366 now augmented: "**Recording is mandatory per `substrate/skills/handoff-author/SKILL.md` step 6** (upgraded from optional → mandatory 2026-05-17 per SPEC_AUDIT C1 fix); the unrecoverable-id case (terminal closed before capture) is explicitly noted in the handoff so the successor knows the `/resume` option is unavailable for that lineage step. The *invocation* discipline ... is a separate canon gap tracked at `stoa--lyw`." Clean — the descriptive-overstatement was directly addressed by upgrading the underlying canon to match the prose. |
| D3 — §7.3 "universal escalation triggers (any mode)" vs op-disc §10 autonomous-mode scope | ✓ | §7.3 line 296: "Originally canonized at `operating-disciplines.md` §10 for autonomous-mode engagements; in practice the same triggers apply across all modes (in HITL/Mode-1/Mode-2 the triggers fire implicitly because PRINCIPAL is more in-the-loop already; in semi-autonomous they fire as discrete escalation events)." Names the scope-expansion + provides rationale. Clean. |
| D4 — /resume invocation discipline gap | ✓ | `stoa--lyw` filed at P3 ("Resume invocation discipline — successor-decides-vs-spawn-fresh + stale-id handling"); referenced at §10.1 line 366, §12.5 line 528, §13.8 line 605, §13.14 line 705. Properly filed-with-plan. Clean. |

### Missing pieces (M1-M6)

| R1 ID | Verdict | Verification |
|---|---|---|
| M1 — fresh team translation of §13.5 prose into directive | D | Deferred to Pass 8 reconciliation per commit message. The R1 finding pointed at a fresh-team operability gap, which is sanctioned for deferred treatment in the §13.10 re-walk. |
| M2 — audit-driven spec edit unscheduled | ✓ | §13.10 line 627: "**This Pass was partially executed early** (the 2026-05-17 spec-audit + this spec-recon commit consume some of Pass 8's scope). The full Pass 8 reconciliation re-runs after Pass 7 (Arc 41) ships, covering any spec drift accreted during Passes 4-7." Clean — Pass 8 is explicitly named as a partial-now / full-later activity. |
| M3 — `validate-spec` skill named but undefined | ✓ | §13.11 line 633: "**Note:** the skill does NOT yet exist; the team authors it as part of Pass 9 (build-then-use, not use-existing) using `substrate/skills/check-substrate-updates/` and `substrate/skills/inspect-script-output/` as precedent shapes." Clean — build-vs-use ambiguity is explicitly disambiguated. |
| M4 — sub-project-tier deployment unenumerated | D | Deferred to Pass 8. Acceptable. |
| M5 — bw prefix cross-ref to op-disc §29.3 | D | Deferred to Pass 8. Acceptable. |
| M6 — stellation naming-ratification step unscheduled | △ | §13.12 line 654: "Test project: `stellation` (PRINCIPAL ratified the name 2026-05-17) ... PRINCIPAL may rename if preferred at dispatch time; ratification window stays open through Pass 9 completion." Partial fix: ratification timestamp + ongoing-window are now stated, but the **placement** of the optional rename (before/after which Pass) is "anywhere through Pass 9" which is itself an open spread. Probably acceptable, but the R1 finding's "PRINCIPAL-gate is open without a placement" point persists in a softer form. |

### Honest "I don't understand" (U1-U5)

| R1 ID | Verdict | Verification |
|---|---|---|
| U1 — "PRINCIPAL's pattern" citation | ✓ | §13.15 line 717: "User-tier POLYBIUS QA passes happen at end of EACH arc per the established pattern (per §5.6 — QA pass invitation post-merge; live-verification; signoff with notes-for-the-record; follow-up ticket filing)." §5.6 cite added per commit. Clean. |
| U2 — §4.5 "Prior generations sit idle" claim type | D | Deferred to Pass 8. Acceptable — semantic clarification, not canon gap. |
| U3 — §5.5 sequencing preference | D | Deferred to Pass 8. Acceptable. |
| U4 — §10.1 meta-agent output shape | D | Deferred to Pass 8 + §12.5 says meta-agent is post-spec-met work. The output-shape ambiguity persists; will be answered when the meta-agent design ships. Acceptable. |
| U5 — §3.3 skill custom path | D | Deferred to Pass 8. Acceptable. |

### Substrate-state-vs-spec (S-A through S-F)

| R1 ID | Verdict | Verification |
|---|---|---|
| S-A — §12.3 ticket enumeration matches `bw list --all` | △ | Live-verified at 2026-05-17T20:25 MDT: `bw list --status open --all` returns **18 tickets**. §12.3 enumerates 3 (Arc 38) + 2 (Arc 39) + 9 (Arc 40) + 1 (Pass 7) + 2 (deferred) = **17**. **One ticket missing: `stoa--lyw`** (filed today as D4 follow-up; referenced at §10.1 + §12.5 + §13.8 + §13.14 but NOT enumerated at §12.3). See new issue NC1. |
| S-B — §12.4 working-tree state drifts | ✓ | §12.4 line 497 now lists 16+ commits chronologically since Arc 35 (matches `git log` through `4a12358`; the spec authors-of-record correctly call out "Plus this current spec-recon commit"). `_drafts/` now correctly noted as empty. Clean. |
| S-C — Pass 8 check would surface bb12806 trailer-missing commit | ✓ | §13.11 line 642 carves out bb12806 explicitly. Clean. |
| S-D — "35 arcs" vs actual 37 | ✓ | §12.1 line 439: "**37 arcs shipped at main.**" Clean. |
| S-E — `.claude/.substrate-last-check` modified | n/a | Was non-finding; unchanged. |
| S-F — `_drafts/` empty | ✓ | §12.4 line 499 correctly notes empty + cross-refs Arc 37 consumption. Clean. |

### Naming / mnemonic (N1-N2)

| R1 ID | Verdict | Verification |
|---|---|---|
| N1 — TIRO carries "novice" connotation | n/a | Optional R1 surface; no fix prescribed. Mnemonic unchanged in fold-in (intentional per PRINCIPAL's prior ratification of TIRO at §4.6). |
| N2 — stellation good naming | n/a | Optional R1 positive signal; no fix needed. |

### Workplan-shape (W1-W3)

| R1 ID | Verdict | Verification |
|---|---|---|
| W1 — Arc 40 9-candidate bundle | △ | Split applied to §13.7 (Arc 40, 4 candidates: 3sz + 5sr + dhc + 6wp) ✓; §13.8 NEW (Arc 41, 5 candidates: n2e + 58b + 3ml + ezp + pqn) ✓; §12.5 Arc 40/41 candidates listed correctly ✓; §13.13 / §13.14 / §13.15 / §13.16 / §14 renumbered through the new Pass count ✓. **New concern:** the split was NOT propagated to §12.3 (still shows Arc 40 = 9 candidates with no Arc 41 grouping). See NC1. |
| W2 — Pass 4 (Arc 38) mixes scope-shapes | ○ | Not addressed. The Arc 38 bundle still mixes new-seat (TIRO) + tool-extension (bj5) + new-canon-section (gq1). Acceptable — workplan-shape feedback that PRINCIPAL did not ratify a change for. |
| W3 — sequencing puts largest+most-mixed bundle last | △ | Partially addressed by W1: Arc 40 + Arc 41 are now smaller bundles (4 + 5 vs original 9). The largest-bundle is now Arc 41 (5), which still lands last but the friction-surface is smaller than the original 9. The R1 concern's underlying shape (no recovery if last bundle slips) persists in a softer form. |

### Out-of-scope observations (O1-O3)

| R1 ID | Verdict | Verification |
|---|---|---|
| O1 — Pre-Arc-25 bw history truncation in §12.1 | ✓ | §12.1 line 439: "Pre-Arc-25 lineage (Arcs 1-24, plus arc-z-consolidation) covers initial scaffolding through coordination protocol stack development; not enumerated here for brevity." Clean. |
| O2 — stellation prefix not in §9.1 | n/a | R1 framed as "acceptable; surfacing for PRINCIPAL confirmation." Not addressed; not expected to be. |
| O3 — app/ and case-study/ not load-bearing in §12 / §13 | D | Deferred to Pass 8. Acceptable. |

### Cross-coherence with stellation-SPECIFICATION.md (Y1-Y3)

| R1 ID | Verdict | Verification |
|---|---|---|
| Y1 — stellation cross-refs off (already = X5) | ○ | Same as X5 — NOT addressed; commit untouched stellation-SPECIFICATION.md. |
| Y2 — stellation §6 vs the-stoa §11 non-overlap | n/a | Was clean before; unchanged. |
| Y3 — stellation §9 criterion 6 expects §28 trailers | ✓ | §13.7 line 593 explicit sequencing note: "Arc 40 lands BEFORE Pass 9 stellation dispatch so subsequent squash-merges (including stellation's) preserve trailers cleanly." (Note: line 593 cross-refs "Pass 9 stellation dispatch" which is itself a new cross-ref bug — see NC5 — but the underlying Y3 concern about *sequencing* is structurally addressed regardless of the naming bug.) |

---

### Verdict tally

- ✓ addressed correctly: **27**
- △ addressed with new concerns: **6** (C1, C2, M6, S-A, W1, W3)
- ○ not addressed / partially addressed: **4** (A4, X5, Y1, W2)
- D deliberately deferred (sanctioned per §13.10 partial-early-execution framing): **12** (A2, A3, M1, M4, M5, O3, S5*, S1*, S2*, S3*, U2-U5)
- n/a optional R1 signal, no fix expected: **6** (N1, N2, O2, S-E, Y2, plus X8 = X3 duplicate)

*S1-S3 + S5 are Self-applicability-check items from R1's §7; the activation paste's category list didn't separately enumerate them but they are R1 findings — re-included here for completeness.

Total addressed-acceptably (✓ + n/a + D): **45** of 49.
Total carrying concerns (△ + ○): **10** (some overlap with new issues below).

---

## New issues found (R2.2)

The fold-in touched ~190 lines of new/revised content. Five new issues surfaced from R2's fresh-eyes pass on the revised material; all five have the same root cause (W1 split + Pass-N renumber didn't propagate completely).

### NC1 — §12.3 is at pre-W1-split state while §12.5 + §13.7 + §13.8 are at post-W1-split state

**Category:** new contradiction (internal staleness within §12). Same shape as R1's C2 finding but at a different inflection point.

**Concrete drift in §12.3 (lines 458-486):**

| Line | Current text | Should be (per W1 + Pass-N renumber) |
|---|---|---|
| 435 | "per §13.9 Pass 7 reconciliation discipline" | Pass 8 reconciliation is now at §13.10; §13.9 is now deferred-with-gating |
| 456 | "Pass 7 spec-recon ... is the current activity" | Pass 8 spec-recon (renumber bumped 7→8) |
| 469 | "Arc 40 candidates (Pass 6 — small bundled hygiene, **9 candidates**)" enumerates all 9 tickets under one Arc 40 heading | Should split into Arc 40 (4 candidates: 3sz + 5sr + dhc + 6wp) + Arc 41 (5 candidates: n2e + 58b + 3ml + ezp + pqn) per §13.7 + §13.8 |
| 480 | "**Pass 7 spec-reconciliation user-tier housekeeping** (1 candidate; no arc)" | Pass 8 spec-reconciliation (renumber bumped 7→8) |
| 481 | "stoa--6k1 ... handled inline during Pass 7 spec-recon" | Pass 8 spec-recon |
| 484 | "**Deferred-with-gating future-work (2 candidates; per §13.8 below):**" | §13.9 below (§13.8 is now Pass 7 Arc 41) |

The pattern: every renumber + split that landed in §13.7 / §13.8 / §13.10 / §13.11 was correctly bumped at the destination sections but the corresponding *back-references* in §12.3 stayed at the old numbering.

This is the §12 internal staleness pattern from R1, recurring at a different point. The fold-in commit message claims "**§12.3** — open-ticket landscape updated (split Arc 40 → Arc 40 + Arc 41 per W1; stoa--lyw added as filed follow-up)" but `git show 4a12358 -- SPECIFICATION.md` shows no edits to §12.3 lines 458-486 in this commit. The activation paste described an edit that did not actually land.

### NC2 — handoff-author SKILL.md frontmatter description contradicts step 6 body

**Category:** new contradiction (within a single file). Companion to R1's C1.

`substrate/skills/handoff-author/SKILL.md` line 4 (frontmatter `description:` field):

> "Optionally records the prior-generation session id for /resume per SPECIFICATION.md §10.1 + §12.5 generational-lineage architecture."

Line 44 (step 6 body):

> "**Record prior-generation session id(s) for /resume (MANDATORY).** ... Recording is mandatory, not optional ..."

Same file; same artifact; the frontmatter description says "Optionally" and the step 6 body says MANDATORY. Commit `d0cbc84` (which performed the C1 upgrade) bumped the body but did not bump the frontmatter description. The Claude Code skill loader uses the frontmatter description as the triggering signal an agent reads; on first-encounter the skill *describes itself* as optional even though the body's step 6 says mandatory.

R1's C1 finding is therefore *partially* addressed — the canon-shipped-form (the body) is mandatory, but the agent-facing surface (the description) is still optional.

### NC3 — §12.3 missing `stoa--lyw` from open-ticket enumeration

**Category:** new substrate-state-vs-spec mismatch.

`bw list --status open --all` at 2026-05-17T20:25 MDT returns **18 tickets**, including `stoa--lyw` (P3) "Resume invocation discipline (/resume) — successor-decides-vs-spawn-fresh + stale-id handling" (filed today as D4 follow-up per commit message).

§12.3 enumerates **17** tickets across 5 buckets (Arc 38 + Arc 39 + Arc 40 + Pass 7 + Deferred). `stoa--lyw` is referenced at §10.1 + §12.5 + §13.8 + §13.14 but is NOT in §12.3's enumeration. The §13.13 mechanical-check criterion 4 expects `bw list --status open --all` to match §12.3 byte-for-byte — it does not.

(The fold-in commit message claims "stoa--lyw added as filed follow-up" in §12.3; the diff does not show that addition.)

### NC4 — §12.2 header text drifts from §12.3 / §12.5 with respect to Pass-N labeling

**Category:** new cross-ref drift; same root cause as NC1.

§12.2 line 456: "Pass 7 spec-recon ... is the current activity; Arc 38 ready to dispatch once spec-recon completes."

In the new (post-W1-split) numbering, spec-recon is **Pass 8** (§13.10). "Pass 7" is now Arc 41 (§13.8). The §12.2 line carries the old Pass-N for spec-recon.

Same shape as NC1 instances; broken out separately because §12.2 is a different subsection and a fresh team reading §12 to understand "what is happening right now" gets a self-contradictory answer (§12.2 says Pass 7 spec-recon is current; §13.10 says Pass 8 spec-recon is current).

### NC5 — §13.7 line 593 says "Pass 9 stellation dispatch" but stellation dispatch is now Pass 10

**Category:** new cross-ref error from W1 renumber.

§13.7 line 593 (within the Arc 40 C4 stoa--6wp candidate):

> "**Important sequencing: Arc 40 lands BEFORE Pass 9 stellation dispatch so subsequent squash-merges (including stellation's) preserve trailers cleanly.**"

In the new numbering, **Pass 9 is §13.11 mechanical-check**, not stellation dispatch. **Stellation dispatch is Pass 10 (§13.12).** The cross-ref needed to be bumped from "Pass 9" to "Pass 10" when the renumber landed; it wasn't.

(Note: the immediately preceding parenthetical in the same line — "see §12.1 + **Pass 9 §13.11 carve-out** for the historical exception treatment" — IS correct for the new numbering, because Pass 9 §13.11 is the mechanical-check carve-out. The two "Pass 9" references in line 593 mean different things: the first is right, the second is wrong. A fresh reader is going to trip on this.)

---

## Substrate-state re-check (R2.3)

### Bw open-ticket count

`bw list --status open --all` at 2026-05-17T20:25 MDT returns **18 tickets**. The activation paste's expectation ("18 open tickets matching the §12.3 enumeration") is wrong on the §12.3 side — §12.3 enumerates 17 (see NC3). Per-ticket comparison:

| Ticket | bw open | §12.3 listed | §12.5 listed |
|---|---|---|---|
| stoa--ojz | ✓ P2 | ✓ (Arc 38) | ✓ (Arc 38) |
| stoa--bj5 | ✓ P2 | ✓ (Arc 38) | ✓ (Arc 38) |
| stoa--gq1 | ✓ P3 | ✓ (Arc 38) | ✓ (Arc 38) |
| stoa--utn | ✓ P3 | ✓ (Arc 39) | ✓ (Arc 39) |
| stoa--ezj | ✓ P3 | ✓ (Arc 39) | ✓ (Arc 39) |
| stoa--3sz | ✓ P3 | ✓ (Arc 40, 9-bundle) | ✓ (Arc 40, 4-bundle) |
| stoa--5sr | ✓ P3 | ✓ (Arc 40, 9-bundle) | ✓ (Arc 40, 4-bundle) |
| stoa--dhc | ✓ P3 | ✓ (Arc 40, 9-bundle) | ✓ (Arc 40, 4-bundle) |
| stoa--6wp | ✓ P3 | ✓ (Arc 40, 9-bundle) | ✓ (Arc 40, 4-bundle) |
| stoa--n2e | ✓ P3 | ✓ (Arc 40, 9-bundle) | ✓ (Arc 41, 5-bundle) |
| stoa--58b | ✓ P3 | ✓ (Arc 40, 9-bundle) | ✓ (Arc 41, 5-bundle) |
| stoa--3ml | ✓ P4 | ✓ (Arc 40, 9-bundle) | ✓ (Arc 41, 5-bundle) |
| stoa--ezp | ✓ P4 | ✓ (Arc 40, 9-bundle) | ✓ (Arc 41, 5-bundle) |
| stoa--pqn | ✓ P4 | ✓ (Arc 40, 9-bundle) | ✓ (Arc 41, 5-bundle) |
| stoa--6k1 | ✓ P4 | ✓ (Pass 7 spec-recon) | n/a (not in §12.5 future-work) |
| stoa--tvc | ✓ P3 | ✓ (deferred) | n/a |
| stoa--myd | ✓ P4 | ✓ (deferred) | n/a |
| **stoa--lyw** | ✓ P3 | **○ MISSING** | ✓ (lineage follow-up) |
| stoa--gwm (R2 coord) | ✓ P2 | n/a (coord ticket, filed during this audit) | n/a |

The 9-vs-(4+5) split in §12.5 vs §12.3 is the NC1 drift. The missing lyw is the NC3 drift. The R2 coordination ticket `stoa--gwm` is excluded from the substrate count by convention (coord tickets are operational, not substrate-canon).

### Git log

`git log -25 --oneline main` matches §12.4's catalogue through `26dc371` (spec-audit R2 activation pastes). The §12.4 list correctly enumerates 16 commits between `bd3e03a` (substrate cleanup, post-Arc-35) and `d0cbc84` (handoff-author mandatory upgrade) + acknowledges "Plus this current spec-recon commit" for `4a12358` itself. Clean.

The two new commits since SPEC_AUDIT.md (`d0cbc84` + `4a12358`) are both reflected in §12.4. The two newest commits since then (`26dc371` R2 activation pastes + this R2 audit's eventual commit) are not yet in §12.4 — expected behavior since §12.4 was authored at the fold-in commit's point in time.

### Handoff-author SKILL.md mandatory upgrade

`substrate/skills/handoff-author/SKILL.md` step 6 body (line 44) reads "Record prior-generation session id(s) for /resume **(MANDATORY)**" — verified via Grep. **But:** the frontmatter `description:` line 4 still reads "Optionally records" — see NC2. Step 6 mandatory wording is correct; frontmatter description hasn't been bumped to match.

---

## PRINCIPAL ratification verification (R2.4)

### C1 — Handoff session-id record MANDATORY

| Sub-check | Status |
|---|---|
| `substrate/skills/handoff-author/SKILL.md` step 6 body reads MANDATORY | ✓ verified at d0cbc84 line 44 |
| §10.1 reads as describing shipped mandatory canon + cross-refs SKILL.md | ✓ line 366 |
| §12.5 removes "Generation-handoff session-id record" from future-work | ✓ line 533 |
| `stoa--lyw` filed for invocation-discipline gap | ✓ stoa--lyw exists, P3 |
| `stoa--lyw` named correctly at §12.5 + §10.1 + §13.8 + §13.14 | ✓ verified |
| `stoa--lyw` enumerated at §12.3 | **○ MISSING (NC3)** |
| SKILL.md frontmatter description matches step 6 body | **○ STALE "Optionally" (NC2)** |

**Verdict:** **△ partially correct** — the canon-shipped form (SKILL.md step 6 body + §10.1 + §12.5 cleanup + lyw filed) is correct. Two surfaces lagging: SKILL.md frontmatter description still says "Optionally"; §12.3 missing lyw enumeration.

### C3 / A5 — bb12806 carve-out

| Sub-check | Status |
|---|---|
| §13.11 includes the bb12806 carve-out wording | ✓ line 642 |
| Forward-only check semantics (Arc 40 ship onwards) | ✓ "applies forward-only: commits authored AFTER stoa--6wp fix lands ... must carry trailers" |
| "No force-push per CLAUDE.md absolute rule" rationale cited | ✓ "fix is forward-only by structural necessity, not by deferral" + "per CLAUDE.md's no-force-push rule" |
| §12.1 honest documentation of the Arc 37 trailer regression | ✓ line 452 "**Notable defect:** `bb12806` squash-merge body carries empty `%(trailers)`..." |
| §13.11 attestation artifact path includes carve-out | ✓ line 648 "agents/observation/spec-validation/mechanical-check-results.md ... including the explicit `bb12806` carve-out attestation" |

**Verdict:** **✓ correct.** The carve-out is structurally clean. No new concerns at C3/A5 itself; the adjacent NC5 (Pass 9 vs Pass 10 stellation cross-ref) is a separate W1-renumber issue, not a C3/A5 issue.

### W1 — Arc 40 9-bundle split

| Sub-check | Status |
|---|---|
| §13.7 Arc 40 = 4 candidates (3sz + 5sr + dhc + 6wp) | ✓ line 586-593 |
| §13.8 Arc 41 NEW = 5 candidates (n2e + 58b + 3ml + ezp + pqn) | ✓ line 595-603 |
| §12.5 reflects 4-candidate Arc 40 + 5-candidate Arc 41 | ✓ lines 514-525 |
| §13.13 / §13.14 / §13.15 / §13.16 renumbered through new Pass count | ✓ verified |
| §14 "candidate-counts note" updated (Arc 38:3; Arc 39:2; Arc 40:4; Arc 41:5) | ✓ line 742 |
| §13.1 "Passes 1-9" + Pass 10 framing | ✓ line 545 |
| §12.3 reflects the W1 split | **○ STALE — still 9-candidate Arc 40 (NC1)** |
| §12.2 reflects the Pass-N renumber | **○ STALE — "Pass 7 spec-recon" should be Pass 8 (NC4)** |
| §13.7 cross-ref to stellation dispatch Pass | **○ STALE — "Pass 9 stellation dispatch" should be Pass 10 (NC5)** |

**Verdict:** **△ partially correct.** The split was authored cleanly in §13.7 / §13.8 / §12.5 / §13.13-§14 + §14. The split was NOT propagated to §12.2 / §12.3 / §13.7 line 593. The pattern: forward-section authoring landed; back-references and §12 enumeration drifted.

### C4 — Gated-deferral vs absorbed-by-X distinguishing wording

| Sub-check | Status |
|---|---|
| §13.9 carries distinguishing prose | ✓ line 611 |
| Wording explicitly names "explicit trigger conditions" + "filed ticket with concrete fix-shape" | ✓ |
| Wording explicitly contrasts with §11 anti-pattern as "closure-or-deferral without explicit criteria" | ✓ |
| §13.9 sanctioned per §13.13 criterion 1 (cross-ref present) | ✓ "Per §13.13 spec-met criterion 1..." |
| Fresh team reading both §11 + §13.9 can distinguish | ✓ — the two categories are now named as structurally distinct |

**Verdict:** **✓ correct.** C4 cleanly addressed.

---

## Self-application verdict (R2.5)

**Did the fold-in close the §12 internal staleness pattern at spec-edit level?**

**No.** The pattern recurred at a different inflection point.

R1's diagnosis (at SPEC_AUDIT.md closing observation):

> "the spec was authored across the same workday Arcs 36 v2 and 37 shipped, and three subsections (§12.1, §12.2, §12.5) reflect the substrate state *before* Arc 37 ship while one subsection (§12.3) reflects the state *after*."

R2's diagnosis (at this commit `4a12358`):

> the W1 split + Pass-N renumber was authored across §13.7 + §13.8 + §12.5 + §13.13-§14 + §14 reflecting *after* the split, while §12.2 + §12.3 reflect the state *before* the split. Three subsections of §12 are still at three different points in time.

The pattern is identical in shape: §12 subsections fall out of sync with the §13/canon edits they cite. The R1 instance was inflected by Arc 37 shipping mid-authoring; the R2 instance is inflected by the W1 split mid-fold-in.

**Spot-check of additional §12 / §13 staleness in R2:**

- §12.1: refreshed to "37 arcs"; Arc 37 substantive line added; pre-Arc-25 truncation noted. Clean.
- §12.2: "Pass 7 spec-recon ... is the current activity" — STALE (NC4).
- §12.3: Arc 40 = 9 candidates; "Pass 7 spec-reconciliation" header; "per §13.8 below"; lyw missing — STALE (NC1 + NC3).
- §12.4: refreshed; clean.
- §12.5: split + lyw + meta-agent enumeration — clean for the W1 split.
- §13.7 line 593: "Pass 9 stellation dispatch" — STALE (NC5).

The fold-in commit message states: "SPEC_AUDIT closing observation acknowledged: I committed §19.6 attestation-confabulation at the spec level multiple times (the §12 internal staleness pattern); the audit team caught it; this commit fixes it. The recurrence of the failure mode in my own audits + spec-edits is the empirical reinforcement for the §4.6 TIRO specialist seat."

The acknowledgment is honest. The structural fix did not land. The pattern has recurred *within the fix commit itself* — the spec-recon pass that was supposed to close the staleness pattern introduced a new instance of the same staleness pattern at the same family of sections.

**This is a load-bearing finding worth flagging explicitly** (per activation paste §8): the same pattern that R1 found is still present, which may mean the fold-in didn't fully address the root cause and the iteration needs a third pass — *or* the fix-shape needs to be structural rather than per-edit (see §6 closing observation below).

---

## Closing observation — meta-pattern across both audits

Two audits, two passes; one underlying pattern.

**The class of edits that LAND consistently:**
- Per-section wording fixes (X1, X4, X6, X7).
- Atomic cross-ref bumps with a clear before/after (X2, X3).
- New section additions with clear new prose (§13.8 Arc 41, §13.9 distinguishing prose for C4, §13.11 carve-out for C3/A5).
- Forward-design qualifier prefixes (D1's TIRO disclaimers at §2.2 + §4.6 + §9.1).
- Single-citation additions (U1's §5.6 cite at §13.15).

These succeed because the edit is local: one cite, one fix, one verifier.

**The class of edits that DON'T LAND consistently:**
- Structural renumbers/splits where the change must propagate through multiple sections (W1's Pass-N renumber missed §12.2 + §12.3 + §13.7 line 593; W1's candidate-count split missed §12.3).
- Same-content claims in multiple subsections that must update in lockstep (§12.1/§12.2/§12.3/§12.5 all encode some aspect of "what is shipped / what is open / what is in flight" and must agree).
- File-spanning edits where the trigger commit only touches one file but the implication touches another (X5 stellation cross-refs needed editing both files; commit only touched SPECIFICATION.md).

These fail because the edit is distributed: N cites, N fixes, N verifiers — and one miss breaks the consistency.

**The R1+R2 underlying class:** §12-snapshot-style sections that re-encode state described elsewhere develop drift whenever the source-of-truth advances. The §12.x subsections all re-encode some aspect of substrate state that lives canonically in `bw` + `git log` + `_drafts/` + §13. Whenever §13 or the substrate advances, §12 falls behind unless every relevant §12.x is swept against the new state.

**Two fix-shape candidates (surfaced for PRINCIPAL + user-tier POLYBIUS consideration, not proposed):**

1. **Procedural (per-edit):** explicit Pass-N grep + §12 re-walk as a checklist step at the end of every spec-edit commit. The commit message would carry a "§12 re-sweep verdict" attestation. This catches the drift at authoring time at the cost of one extra verification step per commit.

2. **Structural:** restructure §12 so the substrate-state subsections are derived views over `bw` + `git log` + §13, not authored subsections. The spec would carry the structure (what counts as "open" / "in flight" / "shipped") and the queries (which bw filter / which git range), and a `validate-spec` skill (per §13.11) would render the current state on demand. This eliminates the class of drift R1+R2 surfaced because §12 *cannot* be at a different time-point than the substrate it describes.

The procedural fix is cheaper; the structural fix is more durable. Both are out-of-scope for R2 (ARGUS-discipline: surface, do not propose).

**The §4.6 TIRO empirical anchor connection.** The fold-in commit message correctly identifies that the recurrence of this pattern is empirical reinforcement for the TIRO specialist seat. R2 is now a *third* live demonstration on the same workday. TIRO's domain is bw mechanics specifically; the §12 staleness pattern crosses bw + git + §13, so TIRO alone would not catch it — but the underlying generalist-forgets-the-discipline failure mode is the same shape as the audit-completeness failure mode TIRO was authored to absorb. PRINCIPAL + user-tier POLYBIUS may want to weigh whether the §4.6 TIRO scope should be widened to cover "spec internal-state attestation" as a sister sub-domain, or whether a separate specialist seat (or a procedural / structural §12 fix) is the better lever.

---

## Output discipline — closing notes

- **ARGUS-discipline:** surface, do not fix. No SPECIFICATION.md / stellation-SPECIFICATION.md / SKILL.md edits were made by this audit; fix-shape decisions are PRINCIPAL + user-tier POLYBIUS authority.
- **N=1 honesty (per op-disc §6.7.1):** R2 is N=2 of the §12 staleness pattern; R1 was N=1. Two occurrences in two consecutive spec-edit / spec-audit cycles is empirically suggestive but does not yet meet the multi-class-evidence + controlled-comparison gate for substrate-canon promotion. A third independent instance would.
- **Single-checker boundary:** R2 was done single-seat-direct (no ARGUS / CATO / BARTLEBY / ZENO sub-dispatch); the structural multi-checker step is PRINCIPAL + user-tier POLYBIUS review of this artifact.
- **Live-verification applied** (per §19.6 attestation discipline) to: `bw list --status open --all` (18 tickets); `git log` (chronology + commit message of `4a12358`); SKILL.md step 6 body + frontmatter description (grep); SPECIFICATION.md Pass-N references (grep); stellation-SPECIFICATION.md cross-refs to SPECIFICATION.md §13.x (grep); `git show --name-only 4a12358` (verified commit touched only SPECIFICATION.md).

[from: polybius-the-stoa]
