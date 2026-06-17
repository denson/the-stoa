Read .claude/MAJOR_PLINY.md and assume the orchestrator role for the-stoa.

## The three-tier chain — your position
```
USER-TIER POLYBIUS (chief-of-staff; close-gate + merge)
  ↓
POLYBIUS_the-stoa  ← YOUR surface target (floor-manager; independent verification + relay)
  ↓
PLINY_the-stoa  ← YOU (gauntlet orchestrator)
  ↓
CAPTAINs (DAEDALUS → ARGUS → ADA → VERA → CATO → ZENO/NOMOS)
```
**You surface to POLYBIUS_the-stoa (the floor-manager), NOT direct to user-tier POLYBIUS.** The floor-manager runs independent verification and relays up.

## Engagement
**Arc 61** — land **MAJOR_CHIRON** and execute its coupled cascade.

- **Read the full spec: `substrate/arcs/arc-61-build-directive.md`** (committed, NOMOS-CONFORMANT). It is authoritative — it carries the Settled decisions, deliverables D1–D7, suggested phasing, the verification / definition-of-done, and out-of-scope. Read it before dispatching DAEDALUS.
- **CHARTER:** `stoa--p41` (design-decision history). **Coordination ticket:** `stoa--p41.1`.

**Scope in brief** (the directive is authoritative): land `MAJOR_CHIRON` (review/refine the working-tree draft, don't re-derive); retire the `agent-author` skill (capability is inlined in CHIRON §7); relocate POLYBIUS §11 (the stub + the §3.5 routing-map/relocation-index rows + the §7.6 cross-ref); **re-home `pair-programmer-authoring.md` as a CHIRON-owned module + reassign the `install.sh` recompose ownership-partition POLYBIUS→CHIRON — all FAIL-LOUD checks green at user AND subproject dry-runs (the highest-risk surface)**; fix the 4 dangling `agent-author` refs; deploy `MAJOR_CHIRON` at ALL tiers (suffixed `CHIRON_<slug>`); update `app/src/data/__tests__/generated.test.ts:92`. **Forward work on an `arc-61/build` feature branch — NOT main.**

Design decisions are LOCKED in the directive's "Settled" block (O1 re-home / O2 deploy-everywhere / O3 test-only) — give them to DAEDALUS as fixed; do NOT re-litigate. The single O1 fallback condition is named in the directive (surface to floor-manager first if it triggers).

## Polling disciplines (all three — non-optional)
- **D-A (bw-copy-all-output):** every CAPTAIN echoes significant outputs to bw on `stoa--p41.1`.
- **D-B (polling-at-breakpoints):** read bw between every CAPTAIN dispatch — sources: the floor-manager (POLYBIUS_the-stoa) + user-tier POLYBIUS + PRINCIPAL.
- **D-C (polling-during-surface-and-wait):** run a Monitor (or sleep loop) during surface-and-wait at ~2–3 min cadence.

## Hand-back protocol
At CATO PASS (+ ZENO/NOMOS), post on `stoa--p41.1` addressed to **POLYBIUS_the-stoa (floor-manager)** — NOT direct to user-tier. The floor-manager runs final verification and relays up.

## What you do NOT do
- Do NOT merge, push, or apply the cascade to deployed instances.
- Do NOT relay direct to user-tier POLYBIUS (except genuine scope disputes).
- Do NOT surface to PRINCIPAL except emergencies.

## Close-signal
`CLOSE ME — arc 61 gauntlet complete; awaiting user-tier POLYBIUS close-gate + merge`

## Compaction recovery
Re-read: `git show beadwork:attachments/stoa--p41.1/HUMAN_paste-pliny-arc-61-instruction.md` + `.claude/MAJOR_PLINY.md` + `substrate/arcs/arc-61-build-directive.md` + `bw show stoa--p41.1`.
