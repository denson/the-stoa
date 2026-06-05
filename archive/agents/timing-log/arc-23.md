# Arc 23 — TIMING_LOG

**Arc:** stoa--pmp (verification-discipline scaffolding + substrate canon updates)
**Dispatched:** 2026-05-12
**Closed:** 2026-05-12
**Merge SHA:** 1ff9f3f (PR #3)
**Authored by:** MAJOR_PLINY (Denson Smith's team)

Per `substrate/MAJOR_POLYBIUS.md` §15 + `substrate/operating-disciplines.md` §6.7.1 (both landing in this arc): observations are single data points, not structural lessons. Substrate-canon promotion requires accreted evidence via a substrate ticket, not this log.

---

## Scope

- 5 phases × 1 gauntlet × ~30 substrate-prose deliverables across ~9 files.
- 8 tickets closed: `stoa--4h7` (Phase 0), `stoa--tp1`, `stoa--fea`, `stoa--nax`, `stoa--148`, `stoa--vmc`, `stoa--rno`, `stoa--14u` (Phases 1-4).
- 1 follow-up ticket filed: `stoa--utn` (deferred save-verdict substrate promotion).

## Estimate vs actual

Estimates were not formally booked at directive-authoring time (the directive landed with phase-by-phase task lists rather than time budgets). Honest scoping: this is N=1 for arc-shape calibration; do not extrapolate to a "Stoa arc baseline" from this data.

**Wall-clock observed (single session, autonomous mode):**

| Phase | Activity | Observed wall-clock |
|---|---|---|
| 0 | bw 0.13.0 upgrade (Windows running-exe lock workaround) | ~5 min |
| 1 | DAEDALUS round-1 + ARGUS round-1 (REVISE) + DAEDALUS revise + ARGUS round-2 (PASS) | ~25 min (DAEDALUS ~8 min ×2; ARGUS ~5 min ×2; orchestrator overhead ~4 min) |
| 2 | ADA build (10 commits across 8 substrate files + 2 probe scripts + 1 user-tier edit) | ~6 min |
| 3 | VERA + CATO + ZENO in parallel | ~5 min (longest pole) |
| 4 | Smoke beats + PR open + PRINCIPAL surface | ~5 min |

Total non-PRINCIPAL: ~45 min. PRINCIPAL surface-and-wait: 1 mid-arc (decision-ratification on save-verdict Option A + §8.4/§8.5 pragma); 1 end-of-arc (ship/no-ship). PRINCIPAL response latency not measured.

## Observations (single arc; not structural lessons)

- **ARGUS round-1 REVISE on 5 risks landed five concrete falsifiable claims.** R2 (save-verdict promotion rests on falsified `_lib/byte_copy.py` assumption — empirically verifiable in <60s of `ls`) was the most consequential — would have shipped a broken substrate skill to every Stoa-deployed project. The "stop guessing, look at the code" reflex caught it the same way the STRABO fabrication that motivated stoa--fea was caught.
- **The verification-complexity framework was self-applied for the first time during its own arc's Phase 3 verification.** VERA classified 117 probes as easy-easy + 5 as hard-easy + 0 as easy-hard or hard-hard. Consistent with design §2.7's prediction for a doc-revision arc.
- **CATO surfaced two minor consistency notes (c1 and c2) without rising to REVISE.** Both captured on `stoa--pmp` as substrate-canon raw material for the next grooming pass — neither was a regression.
- **Windows `bw upgrade --yes` self-replace race blocked the bw 0.13.0 install.** Worked around by manual binary swap. Single observation; if the pattern repeats on the next bw upgrade attempt, file a substrate ticket for an empirical-anchored discipline. Otherwise: tooling residue.
- **Worktree placeholder at `.claude/worktrees/awesome-nash-190573` was empty by structure.** Orchestrator worked from the main repo root and dispatched ADA to create its own worktree at `.claude/worktrees/arc-23-build`. No friction.
- **Directive A5 LOCK literal numbering (§8.3=14u, §8.4=148) was authored without seeing Arc 21's §8.3 = activation-paste.** DAEDALUS surfaced the conflict at design §6.3 + §13.6; ARGUS round-1 R4 verified the falsification of DAEDALUS's `cross-ref-breakage would result` claim; PRINCIPAL ratified the pragma (§8.4=14u, §8.5=148; preserve §8.3) mid-arc. The discipline that surfaced the conflict is verify-then-execute (`u--7yg.10`, `u--7yg.18`); the discipline that resolved it is the bidirectional translation principle (operating-disciplines §8.2).

## Cross-references

- Directive: `substrate/arcs/arc-23-build-directive.md` (commit `0d097c9`).
- Design: `agents/design/arc-23/design.md` (gitignored intermediate spec, 827+ lines, revised round 1).
- Probes: `agents/probes/arc-23/probes.sh` (49) + `agents/probes/arc-23/vera-probes.sh` (73).
- Merge: `1ff9f3f` (PR #3, 2026-05-12).
- Follow-up: `stoa--utn` (save-verdict Python helpers + substrate promotion).
