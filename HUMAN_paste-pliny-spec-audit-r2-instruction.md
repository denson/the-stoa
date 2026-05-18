Re-read .claude/MAJOR_PLINY.md and assume the orchestrator role for the-stoa. (Post-`/clear`; role refresh from canon file.)

**Your immediate intent for this engagement:** support project-tier POLYBIUS_the_stoa (paste at `HUMAN_paste-polybius-spec-audit-r2-instruction.md`) on SECOND-PASS SPEC AUDIT (R2). You + POLYBIUS audited the spec at R1 (output: `SPEC_AUDIT.md`, commit `4f4674e`). User-tier POLYBIUS folded findings via commit `4a12358` + companion `d0cbc84`. R2 verifies the fold-in is correct + surfaces any new issues introduced by the edits. NOT a fresh audit — an iteration audit.

Your job R2 is to dispatch supporting CAPTAINs POLYBIUS requests + handle per-CAPTAIN dispatch mechanics. POLYBIUS may opt for single-seat-direct audit (R1 precedent) or multi-checker dispatch (your call jointly).

**Operating mode:** Mode 2 (exploration) with ARGUS-discipline overlay (surface concerns; do NOT propose fixes; do NOT execute changes). NO arc-build branch; NO arc dispatch.

---

## What changed since SPEC_AUDIT.md (commit `4a12358`)

See the POLYBIUS paste for the full enumerated list of changed sections + the PRINCIPAL-ratified architectural decisions (C1 mandatory / C3+A5 carve-out / W1 split / C4 distinguishing wording).

Summary: 109 insertions + 82 deletions across SPECIFICATION.md; companion 1-line change to substrate/skills/handoff-author/SKILL.md step 6 (optional → mandatory). Plus filed stoa--lyw + closed stoa--q58 (R1 coordination ticket).

---

## What R2 audits

Per POLYBIUS paste R2.1-R2.5:

1. **Per-finding verification** — verify each of the 17 R1 findings is correctly addressed in the fold-in (or correctly deferred per §13.9 gated-deferral discipline).
2. **New-issue detection** — fresh eyes on the ~190 lines of new/revised content for new ambiguities / contradictions / cross-ref errors / aspirational drift.
3. **Substrate-state re-check** — re-run R1's substrate-vs-spec verifications against post-fold-in state.
4. **PRINCIPAL ratification verification** — explicit per-pick verification (C1 + C3/A5 + W1 + C4 each landed correctly).
5. **Self-application verdict** — did the fold-in close the §12 internal staleness pattern, or is it still in evidence?

---

## CAPTAIN dispatches (at POLYBIUS request)

R1 was single-seat-direct. R2 may be too, OR may warrant CAPTAIN dispatch for specific checks:

### CAPTAIN_ARGUS (cold-audit the revised spec sections)

If POLYBIUS wants a fresh-eyes cold audit on the changed sections (~190 lines):

- Dispatch ARGUS with `SPECIFICATION.md` + commit diff `git show 4a12358 -- SPECIFICATION.md` as the artifact + the fold-in commit message as the intent statement.
- Brief: surface load-bearing risks across the new content (ambiguities / contradictions / cross-ref errors / aspirational drift introduced by the edits).
- ARGUS does NOT propose fixes per standard structural property.
- Verdict at `agents/verdicts/spec-audit-r2/argus.md`.

### CAPTAIN_BARTLEBY (cross-ref re-verification)

The §13 renumber (Pass 7-9 → Pass 8-10) introduced many cross-ref updates. Mechanical work to verify they all resolve:

- Dispatch BARTLEBY: "verify every `§N.M` reference in SPECIFICATION.md resolves to an actual section; verify every cited `stoa--*` ticket id resolves via `bw show <id>`; verify every commit SHA cited resolves via `git log`. Special focus on the post-fold-in spec sections (§12, §13, §4.6, §9.1, §3.4, §6.7, §7.1-§7.3, §10.1, §5.6, §2.2, §14)."
- Returns `agents/verdicts/spec-audit-r2/bartleby.md`.

### CAPTAIN_CATO (craft + consistency cold-read on changed sections)

- Dispatch CATO with the diff: "cold-read for craft, hygiene, consistency, scope. Focus on the revised sections; do NOT propose fixes."
- Verdict at `agents/verdicts/spec-audit-r2/cato.md`.

### Direct authoring without CAPTAIN dispatch

POLYBIUS may handle some checks directly — especially R2.1 per-finding verification (which requires comparing against the R1 SPEC_AUDIT.md findings, not just fresh-reading the spec) and R2.3 substrate-state re-check (mechanical bw + git commands).

---

## bw query discipline (same as R1)

CAPTAIN_TIRO still doesn't exist (stoa--ojz, P2; Arc 38 candidate). For completeness audits: `bw list --all` per cookbook §12.1. Friction is empirical-anchor reinforcement.

## Constraints

- DO NOT create `arc-N/build` branch.
- DO NOT propose fixes.
- DO NOT edit SPECIFICATION.md or substrate files.
- DO NOT touch stellation workspace.
- §28 Co-Authored-By trailers on any CAPTAIN dispatch commits per substrate canon.

## Coordination

- POLYBIUS_the_stoa is your radio-check peer. `[from: pliny-the-stoa]` author tags per Arc 36 §7.7.
- R2 coordination ticket filed by POLYBIUS at init.
- User-tier POLYBIUS upper-tier escalation via `[for: user-tier-polybius]`.
- PRINCIPAL exception-handler.

## No polling cron for you per §6.2 surface-and-wait.

## Closure

POLYBIUS signals R2 deliverable complete. Standing down with `[radio-check pliny-the-stoa standing down]`. POLYBIUS handles PRINCIPAL surfacing + R2 coordination ticket closure per engagement-end discipline.

If compaction or /clear erases your role, re-read this paste from `HUMAN_paste-pliny-spec-audit-r2-instruction.md` in the project root.
