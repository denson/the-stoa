# Dispatch protocol for INCOMPLETE and UNVERIFIABLE verdicts — instruction module

> Relocated from `MAJOR_PLINY.md` §5.6 (CONDITIONAL — read when a verifier returns INCOMPLETE or
> UNVERIFIABLE). Provenance: debloat Arc 48 cut `agents/design/arc-48/design-rev1.md` + epic
> `bw show stoa--xyb` / cut ticket `bw show stoa--xyb.10`. The slim-core residue is the §5.6 stub +
> routing-map row (verifier returns INCOMPLETE/UNVERIFIABLE) + relocation-index row in §4.2.

When a verifying CAPTAIN (VERA, CATO, ARGUS, ZENO) returns a verdict of **INCOMPLETE** or **UNVERIFIABLE** per the verification-complexity framework (`operating-disciplines.md` §15), PLINY routes by verdict shape — not by collapsing the new shapes back into PASS / FAIL.

**INCOMPLETE verdict received.**

- PLINY does NOT auto-close the ticket. INCOMPLETE is an operator-disposition state, not a ship verdict.
- PLINY surfaces the verdict's `coverage_description:` (what was checked, what was not, bound used, confidence interval) to POLYBIUS via beadwork comment on the dispatch ticket.
- POLYBIUS routes to PRINCIPAL for an operator-judgment-required decision, OR accepts the bound and authorizes proceed, OR requests deeper verification with an explicit higher budget (e.g., "re-run VERA with 100× probe budget; document in the verdict").
- The verdict does NOT gate merge on its own (per `operating-disciplines.md` §15.4 A6 LOCK). Both PASS and INCOMPLETE leave the ticket open until operator disposition.

**UNVERIFIABLE verdict received.**

- PLINY does NOT auto-close the ticket. UNVERIFIABLE is also an operator-disposition state.
- PLINY surfaces the verdict's `quadrant_classification:`, `sanity_check_performed:`, and `recommended_next_step:` to POLYBIUS.
- POLYBIUS routes to PRINCIPAL for operator judgment, OR accepts the risk with documented mitigation (e.g., "ship with the synthesis-claim wording narrowed; track UNVERIFIABLE assertion as deferred follow-up").
- UNVERIFIABLE also does not gate merge on its own.

**Why neither gates merge.** The discipline is that the verifier reports honestly rather than fail closed or run indefinitely. An INCOMPLETE verdict against a routine concurrency check is not a defect; an UNVERIFIABLE verdict against a load-bearing synthesis claim is not a defect either. Both surface decisions that belong with operator judgment. Routing them through PRINCIPAL via POLYBIUS is the gauntlet doing its job.

Cross-refs: `operating-disciplines.md` §15 (the framework); `CAPTAIN_VERA.md` §5.7 (VERA's quadrant discipline); `CAPTAIN_CATO.md` §6.7; `CAPTAIN_ARGUS.md` §6.6; `CAPTAIN_ZENO.md` §6.6.
