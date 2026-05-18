Re-read .claude/MAJOR_PLINY.md and assume the orchestrator role for the-stoa. (Post-`/clear`; role refresh from canon file.)

**Your immediate intent for this engagement:** support project-tier POLYBIUS_the_stoa (paste at `HUMAN_paste-polybius-spec-audit-r3-instruction.md`) on THIRD-PASS SPEC AUDIT (R3). You + POLYBIUS audited the spec at R1 (output: `SPEC_AUDIT.md`, commit `4f4674e`) + R2 (output: `SPEC_AUDIT_R2.md`, commit `a50a1a8`). User-tier POLYBIUS folded R2 findings via commit `a1a10e4` (structural §12 rewrite per R2.5 closing observation + mechanical NC1-NC5 + A4 + X5/Y1 fixes per PRINCIPAL's "fix all in this pass" pick).

R3 verifies the fold-in is correct + tests the structural §12 fix's central claim: that removing state-carrying content from §12 eliminates the staleness drift class entirely. R3 scope is narrower than R2 (3 files changed; 46 insertions / 85 deletions). Expected wall-clock: 20-30 min.

**Operating mode:** Mode 2 (exploration) with ARGUS-discipline overlay (surface concerns; do NOT propose fixes; do NOT execute changes). NO arc-build branch; NO arc dispatch.

---

## What changed since SPEC_AUDIT_R2.md (commit `a1a10e4`)

See the POLYBIUS paste for the full diff summary. Short version: §12 restructured from snapshot-enumerated to derived-view (queries + structural contracts; no enumerations); 4 mechanical fixes (NC2 SKILL.md frontmatter, NC5 §13.7 Pass 10 cite, A4 boundary reconcile, X5/Y1 stellation cross-refs).

---

## What R3 audits

Per POLYBIUS paste R3.1-R3.5:

1. Per-R2-finding verification (NC1-NC5 + △ items + ○ items + W2 disposition).
2. Structural §12 internal consistency (no leftover enumerations; queries actionable; §12.5→§13 cross-refs work; no new staleness surfaces).
3. New-issue detection in the ~50 lines of new §12 prose.
4. Substrate-state re-check (bw list / git log / SKILL.md frontmatter / stellation cross-refs).
5. **Meta-verdict on the §12 staleness pattern** — load-bearing answer: closed structurally / still latent at <mechanism> / current instance found at <location>.

---

## CAPTAIN dispatches (at POLYBIUS request)

R3's small scope suggests single-seat-direct is appropriate (R1 + R2 precedent). If POLYBIUS wants:

- **CAPTAIN_ARGUS** for fresh-eyes cold-audit on the diff (`git show a1a10e4`).
- **CAPTAIN_BARTLEBY** for cross-ref re-verification on the §12 / §13 / stellation cross-refs.
- **CAPTAIN_CATO** for craft + consistency cold-read on the new §12 prose.

PLINY dispatches at POLYBIUS request. Each CAPTAIN returns verdict at `agents/verdicts/spec-audit-r3/<seat>.md`. Standard §28 trailers + ARGUS-discipline (surface, don't fix).

---

## bw query discipline (same as R1 + R2; TIRO still doesn't exist)

`bw list --all` per cookbook §12.1 + new §12.3 guidance.

## Constraints (same as R1 + R2)

- NO arc-build branch.
- NO fix-proposing.
- NO spec / substrate / stellation edits.
- §28 trailers on any CAPTAIN dispatch commits.

## Coordination

POLYBIUS is your radio-check peer. `[from: pliny-the-stoa]` tags. POLYBIUS owns R3 coordination ticket + closes on engagement-end. User-tier POLYBIUS upper-tier escalation. PRINCIPAL exception-handler.

## No polling cron for you per §6.2 surface-and-wait.

## Closure

POLYBIUS signals R3 deliverable complete. Standing down with `[radio-check pliny-the-stoa standing down]`. POLYBIUS handles PRINCIPAL surfacing.

If compaction or /clear erases your role, re-read this paste from `HUMAN_paste-pliny-spec-audit-r3-instruction.md` in the project root.
