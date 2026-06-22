Read .claude/MAJOR_PLINY.md and assume the orchestrator role for the-stoa on arc stoa--7gl (Arc 71).

# Engagement — Arc 71 gauntlet orchestrator (charter stoa--7gl)

**Read first:** the directive `substrate/arcs/arc-71-build-directive.md` (committed `6b22d62`, NOMOS-CONFORMANT) — it carries the full locked scope, the DC0–DC5 design items, the deliverables, and the DoD. Then the charter `stoa--7gl` (body + NOMOS directive-audit). Then the doctrine `docs/self-correction-doctrine-DRAFT.md` §6 + Resolved. Then what Arc 70 shipped (you build on it): `substrate/modules/dilemma-classifier.md`, its wiring (MAJOR_POLYBIUS §3.6 + checkpoints, MAJOR_PLINY §5.18), and its corpus at `substrate/modules/tests/dilemma-classifier/`.

## Chain of command

```
PRINCIPAL (Denson)
  -> user-tier Polybius_the_Stoa (owns arc + close-gate + merge)   [sid 990b0750-5572-4836-b9c7-18d626a12e96]
    -> POLYBIUS_the-stoa (floor-manager: independent verify + relay)
      -> YOU, PLINY_the-stoa (run the gauntlet)
```
You surface to the **floor-manager**, NOT direct to user-tier (except a scope dispute). The PRINCIPAL is NOT the relay — beadwork is.

## The arc (slice 2a — capture only). Full detail in the directive; the spine:

Build the **capture half** of the black box:
1. A composable **decision-register CAPTURE module** — given a dilemma-decision (Arc-70 classifier returned DILEMMA, tradeoff illuminated, PRINCIPAL chose), write ONE structured bw entry: dilemma · warning(s)/tradeoff · option chosen · counter-hypothesis (what would prove the choice wrong) · timestamp/context-link.
2. The **write trigger + over-write guard** — fires only when a decision is *taken*, at the Arc-70 checkpoint subset + explicit-call path. NO entry on: a problem solved, a dilemma illuminated-but-not-decided, or an incidental mention.
3. The **bw-write mechanics** — deterministic template/helper (honor the positional-`bw comment` + no-backtick footguns), transparent + user-readable by default.
4. A **both-directions corpus** + runner — should-write vs should-not-write fixtures, stated floor, mirroring the Arc-70 corpus pattern.

**DC0–DC5 are DAEDALUS's to resolve in Phase A** (see directive). Surface the design to the floor-manager for go/no-go BEFORE any build. Load-bearing seams to flag for ARGUS: DC0 (schema must be re-readable by the deferred 2b callback), DC1 (the over-write guard), DC4 (the "writing is half the value" device — honest, prose-enforced, no over-claim).

**OUT OF SCOPE — automatic route-back if a design reaches in:** the complaint-time callback, the re-verify gate, dose calibration (all slice 2b); the meta-trigger counter (arc 4); decision-surface graduation (stoa--ida, arc 3); broader rollout.

## Gauntlet + polling disciplines

Full gauntlet: **DAEDALUS → ARGUS → ADA → VERA → CATO → NOMOS**. Standard team (no CHIRON/HAMILTON). Autonomous operating mode.
- **D-A (echo outputs):** every CAPTAIN echoes significant outputs to bw on `stoa--7gl`.
- **D-B (poll at breakpoints):** read bw between every CAPTAIN dispatch — sources: floor-manager + user-tier Polybius_the_Stoa + PRINCIPAL.
- **D-C (poll during surface-and-wait):** run a Monitor (or sleep loop) at ~2–3 min cadence while waiting.
Run `bw prime` at activation. Sign every comment `[from: PLINY_the-stoa | sid <your-session-id>]` (sid via `whoami`). `bw comment` positional, no `-m`, no backticks/`$()`.

## Hand-back + close

At CATO PASS + NOMOS CONFORMANT, post on `stoa--7gl` addressed to **POLYBIUS_the-stoa (floor-manager)** — NOT direct to user-tier. The floor-manager runs final verification + relays up.
You do NOT: merge, push, apply to cloud, relay direct to user-tier (except scope disputes), surface to PRINCIPAL except emergencies.
At arc end: `CLOSE ME — stoa--7gl gauntlet complete; awaiting user-tier Polybius_the_Stoa close-gate + merge`

## Compaction recovery

If you /compact: re-read this brief at `git show beadwork:attachments/stoa--7gl/HUMAN_paste-pliny-stoa--7gl-instruction.md`, then `bw show stoa--7gl` for live state, and resume the gauntlet.
