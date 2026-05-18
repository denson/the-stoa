Re-read .claude/MAJOR_POLYBIUS.md and assume the project-tier chief-of-staff role for the-stoa. (Post-`/clear`; role refresh from canon file.)

**Your immediate intent for this engagement:** SECOND-PASS SPEC AUDIT (R2). You did the first audit at `SPEC_AUDIT.md` (commit `4f4674e`, ticket `stoa--q58` closed on engagement-end). User-tier POLYBIUS folded findings into SPECIFICATION.md via commit `4a12358` (spec-recon fold-in: 109 insertions / 82 deletions) + companion commit `d0cbc84` (handoff-author SKILL.md C1 fix). PRINCIPAL ratified 4 architectural decisions (C1 / C3+A5 / W1 / C4) that drove the fold-in.

Your job R2 is to verify the fold-in is correct + surface any new issues introduced by the edits. NOT a fresh audit — an iteration audit.

**Operating mode:** Mode 2 (exploration) with ARGUS-discipline overlay (surface concerns; do NOT propose fixes; do NOT execute changes; do NOT dispatch any arc).

---

## What changed since SPEC_AUDIT.md (commit `4a12358`)

**Substantive edits across §12 + §13 + §4.6 + §9.1 + §3.4 + §6.7 + §7.1 + §7.2 + §7.3 + §10.1 + §5.6 + §2.2 + §14:**

- **§12.1** — "35 arcs" → "37 arcs"; Arc 37 substantive line added (with bb12806 trailer regression noted honestly); pre-Arc-25 lineage truncation acknowledged (SPEC_AUDIT O1).
- **§12.2** — refreshed pre-Arc-37 → post-Arc-37 state.
- **§12.3** — open-ticket landscape updated (split Arc 40 → Arc 40 + Arc 41 per W1; stoa--lyw added as filed follow-up).
- **§12.4** — full 16+ commit chronological list since Arc 35 ship; `_drafts/` correctly noted as empty.
- **§12.5** — Arc 37 candidates REMOVED (they shipped); Arc 38/39/40/41 candidates updated; "Generation-handoff session-id record" REMOVED (Arc 37 + Arc 38 SKILL.md upgrade ships it as mandatory canon); stoa--lyw added; meta-agent stays as post-spec future-work.
- **§12 parent header** added (SPEC_AUDIT X4).
- **§13.5 Pass 4 Arc 38** — 3 candidates (TIRO + bj5 + gq1).
- **§13.6 Pass 5 Arc 39** — 2 candidates (utn + ezj).
- **§13.7 Pass 6 Arc 40** — 4 candidates (3sz + 5sr + dhc + 6wp; was 9).
- **§13.8 Pass 7 Arc 41 NEW** — 5 candidates (n2e + 58b + 3ml + ezp + pqn; split from W1).
- **§13.9 Deferred-with-gating** — gets explicit C4 distinguishing-wording vs §11 absorbed-by-X anti-pattern.
- **§13.10 Pass 8 spec-recon** — renumbered + notes the early-execution caveat.
- **§13.11 Pass 9 mech-check** — renumbered + bb12806 carve-out wording per C3/A5 + validate-spec build-vs-use note per M3.
- **§13.12 Pass 10 stellation** — renumbered.
- **§13.13 spec-met criteria** — renumbered; criteria 5+6 reference Pass 9+10.
- **§13.14 out-of-scope** — renumbered; added Arc 41 reference; added stoa--lyw as explicit out-of-scope-for-spec-met.
- **§13.15 mode** — renumbered + added §5.6 cite for "PRINCIPAL's pattern" per U1.
- **§13.16 done** — renumbered.
- **§14 PRINCIPAL editing notes** — §13.2 → §13.13 cross-ref fix per X2; updated candidate-counts note.

**Companion substrate-canon edit:**
- `substrate/skills/handoff-author/SKILL.md` step 6: "(Optional but recommended)" → "(MANDATORY)" per C1 ratification.

**Mechanical fixes addressing SPEC_AUDIT findings:**
- §3.4 — removed "scope-recut-for-spec" stale parenthetical (X7).
- §6.7 — "in flight" → "shipped at fcd68c0" (X6).
- §7.1 — "shipping in stoa--ntn" → "shipped at bb12806" (X6).
- §7.2 — inline gloss for "regresses upward" (A1).
- §7.3 — clarified universal scope vs op-disc §10 autonomous-mode scope (D3).
- §5.6 — "§5.10" → "MAJOR_PLINY.md §5.10" disambiguation (S4).
- §2.2 — TIRO row gets "(per Arc 38 / stoa--ojz; not yet shipped)" qualifier (D1).
- §4.6 — TIRO present-tense paragraphs prefixed with forward-design-language qualifier; "TIRO ships" → "will ship" (D1).
- §9.1 — TIRO delegation note marked "(post-Arc-38)" + until-Arc-38 fallback discipline (D1).
- §10.1 — Each-generation-handoff sentence augmented with mandatory-per-SKILL.md cross-ref + unrecoverable-id handling + lyw invocation-gap cite (D2).

**Companion bw operations:**
- Filed `stoa--lyw` (P3) — Resume invocation discipline.
- Closed `stoa--q58` (your prior coordination ticket — closed during the fold-in pass per engagement-end discipline).

---

## What R2 audits (priority order)

### R2.1 Per-finding verification (the 17 SPEC_AUDIT findings)

For each of your 17 prior findings (A1-A5, C1-C4, X1-X8, D1-D4, M1-M6, U1-U5, S-A through S-F, N1-N2, W1-W3, O1-O3, Y1-Y3), verify the fold-in's disposition is correct:

- **Addressed correctly** — the edit fixes the finding as expected; no new concerns.
- **Addressed with new concerns** — the edit fixes the finding but introduces a different issue (cite the new issue).
- **Not addressed / partially addressed** — the edit doesn't fix the original finding (cite what's still broken).
- **Deliberately deferred** — the edit explicitly defers the finding to a future pass (verify the deferral is sanctioned per §13.13 criterion 1 and §13.9 gated-deferral discipline; not absorbed-by-X per §11).

The fold-in commit message at `4a12358` enumerates which findings were addressed and which were deferred. Use it as your ground-truth for "what was intended"; verify against the actual spec edits for "what landed."

### R2.2 New-issue detection (fresh eyes on the changed sections)

The edits touched ~190 lines of new/revised content. New issues that the original SPEC_AUDIT.md couldn't have caught:

- **New ambiguities** introduced by the rewrites (especially in §13.9 deferred-with-gating + §13.11 mech-check carve-out + §13 renumber).
- **New contradictions** between revised sections (e.g., §12.1 Arc 37 line vs §13.7 Arc 40 candidates — both reference stoa--6wp and bb12806; do they align?).
- **New cross-ref errors** (the §13 renumber bumped Pass 7-9 → Pass 8-10; the §13.11-§13.16 cross-refs were updated; verify they all resolve cleanly).
- **New aspirational-vs-descriptive drift** introduced by added prose.
- **New "I don't understand" items** in the revised sections.

### R2.3 Substrate-state-vs-spec re-check

Re-run the §12.3 + §12.4 + bb12806 trailer + handoff-author SKILL.md mandatory-upgrade verifications. The substrate has moved (4 new commits since SPEC_AUDIT.md):

- `d0cbc84` — handoff-author SKILL.md mandatory upgrade
- `4a12358` — spec-recon fold-in
- (plus filed stoa--lyw + closed stoa--q58 — bw operations, no main commit)

`bw list --all` should return 18 open tickets matching the §12.3 enumeration. `git log` should match §12.4's catalogue. handoff-author/SKILL.md step 6 should NOT contain "Optional".

### R2.4 PRINCIPAL ratification verification

PRINCIPAL ratified 4 architectural decisions:

- **C1 — Mandatory:** verify SKILL.md step 6 reads as mandatory; verify §10.1 + §12.5 + §14 all reflect this; verify the lyw invocation-discipline ticket exists + is named correctly in §12.5.
- **C3/A5 — Carve-out:** verify §13.11 mech-check spec includes the bb12806 carve-out wording; verify the wording is correct (forward-only check; no force-push); verify §12.1 honestly documents the regression.
- **W1 — Split:** verify §13.7 (Arc 40) has 4 candidates; verify §13.8 (Arc 41) has 5 candidates; verify Pass renumbering (7→8, 8→9, 9→10) is consistent throughout §13 + §14.
- **C4 — Distinguishing wording:** verify §13.9 carries the distinguishing prose; verify it cleanly separates gated-deferral (sanctioned) from absorbed-by-X (anti-pattern).

### R2.5 Self-application sanity check

User-tier POLYBIUS demonstrated the §19.6 attestation-confabulation failure mode multiple times during the day (the "§12 internal staleness" pattern your R1 audit named). Did the fold-in actually fix that pattern, or does the spec still mix temporal states?

- Spot-check §12 sections for any remaining pre-Arc-37 framing.
- Spot-check §13 for "Pass N" references that haven't been renumbered.
- Spot-check any section that should reflect post-Arc-37 substrate state but uses pre-Arc-37 verbiage.

The R1 closing observation was that the pattern accounted for ~40% of findings. R2 should verify the pattern is now closed at spec-edit level (not just acknowledged in commit messages).

---

## Required R2 output categories

Mirror SPEC_AUDIT.md's structure for continuity. Produce `SPEC_AUDIT_R2.md` at repo root, structured by:

1. **Per-finding verification table** — one row per R1 finding (A1-A5, C1-C4, etc.), with disposition: addressed / addressed-with-new-concerns / not-addressed / deliberately-deferred. Brief cite for the verdict.

2. **New issues found** — fresh items from R2.2; categorized by the R1 audit's category set (ambiguities, contradictions, cross-ref errors, aspirational drift, etc.).

3. **Substrate-state re-check** — like R1's §8 Substrate-state-vs-spec mismatches; updated for current main + post-fold-in state.

4. **PRINCIPAL ratification verification** — explicit per-pick verification (C1 / C3+A5 / W1 / C4 each landed correctly).

5. **Self-application verdict** — did the fold-in actually close the §12 internal staleness pattern at spec-edit level, or is the pattern still in evidence?

6. **Closing observation** — any meta-pattern observable across both audits (e.g., classes of edit that consistently land vs classes that don't).

### Output discipline (same as R1)

- ARGUS-discipline: surface, do not fix.
- Honest "addressed correctly with no concerns" entries are useful explicit positive signal.
- N=1 honesty per `operating-disciplines.md` §6.7.1.

---

## Constraints (same as R1)

- **DO NOT dispatch any arc.**
- **DO NOT propose fixes** — surface concerns.
- **DO NOT edit SPECIFICATION.md or other substrate files.**
- **DO NOT touch stellation workspace.**

## bw query discipline (same as R1; TIRO still doesn't exist)

CAPTAIN_TIRO is still an Arc 38 candidate (stoa--ojz, P2). Use `bw list --all` directly per operating-disciplines.md §12.1 cookbook. Friction observed is the empirical anchor reinforcement; cookbook-sufficiency is also useful signal.

---

## Sub-dispatch authority (same as R1)

You may dispatch ARGUS / BARTLEBY / CATO / ZENO via PLINY at your discretion. For R2's smaller scope, single-seat-direct audit may be appropriate (R1 did this); multi-checker dispatch may also be appropriate if R2 surfaces architectural ambiguity. Your call.

## Coordination

- **Project-tier PLINY** is your radio-check peer (paste at `HUMAN_paste-pliny-spec-audit-r2-instruction.md`).
- **Coordination ticket:** file a fresh one for R2 (e.g., `stoa--<hash>` named "spec-audit R2 engagement coordination"). Use `[from: polybius-the-stoa]` author tag per Arc 36 §7.7. **Close it on engagement-end** (the R1 omission was caught + fixed during the fold-in pass — don't repeat).
- **User-tier POLYBIUS** (spec author + fold-in author) is upper-tier escalation via `[for: user-tier-polybius]`.
- **PRINCIPAL** is exception-handler. Surface on: substance disagreement after one round-trip; irreducible ambiguity; engagement-end handoff (POLYBIUS owns; PLINY stands down with closure handshake).

## Polling cron + renewal per Arc 36 v2 §11 step 1.5

- Set up your polling cron at `*/5 * * * *`; name the cron id in the init handshake.
- Schedule the one-shot renewal cron per `operating-disciplines.md` §11 step 1.5 at +144h from polling-cron creation. R2 engagement is short (~30-60 min expected); renewal won't fire; but you ARE applying the canon forward.

## Closure

When SPEC_AUDIT_R2.md is complete:
1. Commit SPEC_AUDIT_R2.md (user-tier housekeeping per §18.1 authority on audit artifacts).
2. Post `[from: polybius-the-stoa]` closure comment on R2 coordination ticket.
3. Close the R2 coordination ticket per engagement-end discipline.
4. Tag `[for: user-tier-polybius]` for the handoff.
5. Surface to PRINCIPAL with one-line: "spec audit R2 complete; SPEC_AUDIT_R2.md at repo root; N R1 findings verified addressed, M remain open, K new issues surfaced; standing by for PRINCIPAL + user-tier POLYBIUS review."
6. Stand down with `[radio-check polybius-the-stoa standing down]`; CronDelete polling + renewal crons.

---

## Self-application

The R2 audit operates under the post-fold-in spec. Same disciplines apply: §6 multi-checker (the multi-checker is PRINCIPAL + user-tier POLYBIUS review of R2; R2's single-seat-direct work is OK per the R1 precedent + meta-acknowledgment), §19.6 attestation-honesty (cite live-verified state), §7 author-tag convention, §5.10 signoff-accuracy.

If R2 surfaces "the same pattern that R1 found is still present," that's a load-bearing finding worth flagging explicitly — it may mean the fold-in didn't fully address the root cause and the iteration needs a third pass.

If compaction or /clear erases your role, re-read this paste from `HUMAN_paste-polybius-spec-audit-r2-instruction.md` in the project root.
