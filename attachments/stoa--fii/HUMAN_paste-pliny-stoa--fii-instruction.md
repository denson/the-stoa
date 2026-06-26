Read .claude/MAJOR_PLINY.md and assume the orchestrator role for the-stoa.

Then read your directive from the beadwork branch:
git show beadwork:attachments/stoa--fii/stoa-reg-liveness-directive.md

== CHAIN OF COMMAND ==
PRINCIPAL → Polybius the Grand → Polybius_the_Stoa (user-tier, supervising) → POLYBIUS_the-stoa (floor-manager) → YOU (PLINY_the-stoa, orchestrator) → gauntlet CAPTAINs. You surface to the FLOOR-MANAGER, not user-tier (except a scope dispute).

== ARC SCOPE (see the directive for full detail) ==
stoa--reg liveness reconciliation, BOTH mechanisms:
1. STAND-DOWN WRITE (graceful): record-seat.ps1 gains a -Status param (or a close-seat.ps1 helper); the FM/launcher marks the team dead at arc close.
2. TTL/LIVENESS SWEEP (abrupt): add last_seen + a TTL; the launcher folds a sweep at spin-up that marks TTL-exceeded rows PRESUMED-dead.
3. HONEST-CLAIM BOUNDARY (explicit): sweep-dead = a presumed-dead heuristic, NOT proof of death; document it (stoa--reg ticket + tooling), mirroring the stoa--reg audit-only note; represent presumed-dead distinctly from a graceful dead.
Touches record-seat.ps1 + launch-team.ps1 + the stoa--reg contract. Idempotent on (seat,machine); rows stay audit-only; older rows must still parse (additive last_seen, per Arc 68 discipline).

== FLOW ==
FULL gauntlet DAEDALUS → ARGUS → ADA → VERA → CATO → NOMOS. ADA/VERA MUST exercise the DoD probe: record a seat → sweep past TTL → it reads presumed-dead; stand-down → it reads dead (the registry demonstrably stops accreting stale-alive rows).

== POLLING DISCIPLINES (all three) ==
- D-A: every CAPTAIN echoes significant outputs to bw on stoa--fii.
- D-B: read bw between every CAPTAIN dispatch (FM, Polybius_the_Stoa, PRINCIPAL).
- D-C: a Monitor / poll loop at ~2-3 min cadence during surface-and-wait.

== HAND-BACK ==
At gauntlet NOMOS-CONFORMANT, post on stoa--fii addressed to POLYBIUS_the-stoa (floor-manager), NOT direct to user-tier. The FM verifies + relays up.

== WHAT YOU DO NOT DO ==
Merge; push; relay direct to user-tier (except a scope dispute); surface to PRINCIPAL except emergencies.

== CLOSE SIGNAL ==
`CLOSE ME — stoa--fii gauntlet complete; awaiting Polybius_the_Stoa close-gate + merge`.

== COMPACTION RECOVERY ==
Re-read .claude/MAJOR_PLINY.md, then git show beadwork:attachments/stoa--fii/HUMAN_paste-pliny-stoa--fii-instruction.md, then `bw show stoa--fii`.
