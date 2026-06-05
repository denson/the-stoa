Read .claude/MAJOR_PLINY.md and assume the orchestrator role (PLINY_the-stoa) for the-stoa. This is a RE-ACTIVATION mid-arc — a prior PLINY session wedged in a watch-loop after surfacing the Arc 59 HARD STOP; you are picking up exactly where it left off.

## Chain of command (READ THIS — load-bearing)
Chain: human-PRINCIPAL (Denson) → **user-tier POLYBIUS = YOUR PRINCIPAL** → you (PLINY) + POLYBIUS_the-stoa (floor-manager) → CAPTAINs. For you, **user-tier POLYBIUS is the principal.** Every surface / escalation / HARD-STOP / design gate / question goes to user-tier POLYBIUS on bw — NEVER to the human directly (no interactive prompts to the human, no surface-and-wait on the human). When "awaiting PRINCIPAL," the principal is user-tier POLYBIUS. They decide what (if anything) reaches Denson; you never reach past them. Full standing directive: `bw show stoa--ikr` (the chain-of-command directive comment).

## Anti-wedge (what broke the prior session)
On every wake, RE-READ the live ticket (`bw show stoa--yfv` newest comments) and ACT on what landed — do NOT regenerate a stale "awaiting greenlight" recap. Arc 59 was greenlit by your principal at 15:21Z over an hour before this restart; the prior session never registered it. If you wake 3x on one ticket without advancing, declare a wedge and surface to user-tier POLYBIUS.

## Before building — branch guard
Confirm `arc-59/build` HEAD = `b643ee9` (directive only). If it shows any other commit, STOP and surface to user-tier POLYBIUS first (an unauthorized build briefly ran from the wrong seat and is being discarded). Build only once the branch is confirmed clean.

## Cron hygiene FIRST
Run `CronList`; `CronDelete` any orphaned cron from the prior session.

## State — Arc 59 (stoa--yfv Arc B) is GREENLIT; dispatch ADA NOW
- The design HARD STOP was surfaced + CLOSE-GATED by user-tier POLYBIUS. **GREENLIT 2026-06-04 (full ship-go on `bw show stoa--yfv`, comment 15:21Z).** Build is cleared.
- The DAEDALUS design is at `agents/design/stoa--yfv/arc-b-design.md` (in the `arc-59-build` worktree, uncommitted) + the ARGUS verdict (RATIFY-WITH-CONDITIONS) at `agents/verdicts/stoa--yfv/`.
- Worktree `arc-59-build` exists; branch `arc-59/build` has the directive committed (b643ee9). NO build edits yet — that's the gap to close.

## Your immediate action: dispatch ADA to build, with the 3 ratified folds
Build in the ratified producer→consumer order **B1(yfv.2) → B2(yfv.1) → B3(yfv.5) → B4(yfv.6)**, folding in:
- **r1 [load-bearing]:** extend `CAPTAIN_CATO.md` §6.1 item-11 so CATO INDEPENDENTLY re-runs the mechanical `id ∈ probes_executed` cross-check (not only tier-ii substance). This makes the phantom-id catch independently enforced, not producing-seat self-policed.
- **r2 [load-bearing]:** qualify the tier-i "mechanical/grep-able" wording in the design's §2.2 — the empty-binding sub-check is skill-tool-enforced (exit-4), but the id-in-executed-set sub-check is SEAT-SIDE grep, not skill-enforced. Word it so no reader assumes tool-strength enforcement that doesn't exist.
- **Q2 [in scope]:** extend `CAPTAIN_ARGUS.md` §6.9 mapless-mitigation smell to also fire on "A3 map present BUT no threat-anchored probe spec'd in design §3."
- (ARGUS r3, non-blocker: keep the 3 inline `threat_coverage:` blocks byte-aligned across VERA/CATO/ARGUS; §6.8 diff is the drift guard.)

## Then the full gauntlet
ADA → VERA → CATO → NOMOS → ZENO. §35.5 reaffirmed: this arc is NOT threat-ratified (no self-trap); p1–p6 are ordinary artifact-conformance probes. Keep the arc diff scoped.

## Surface at arc close
Surface the hand-back to POLYBIUS_the-stoa (floor-manager) → user-tier POLYBIUS, who holds the close-gate + merge. Do NOT autonomous-ship (bucket A canon). The ship-gate criteria user-tier will re-verify: all 3 folds present (esp. r1's CATO independent id-check), the 6 probes actually EXECUTED with expected results (esp. p1a skill exit-4 + p1b role-file grep), gauntlet clean, authorship = Denson Smith.

## Do NOT re-engage these — they are RESOLVED
- **Arc-57 r1 (tool-selector seat-scope)** is DECIDED: POLYBIUS-SOLE stands (PRINCIPAL-confirmed). `stoa--exp` is CLOSED. Ignore any stale Arc-57 interactive prompt entirely.
- After yfv lands: `stoa--h2z` (remediation workflow, needs yfv.1) is the final round arc, then the round (`stoa--ikr`) closes.

## Recovery
If this session compacts, re-read this file + `.claude/MAJOR_PLINY.md` + `bw show stoa--yfv` + `bw show stoa--ikr`.
