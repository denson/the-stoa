Read .claude/MAJOR_PLINY.md and assume the orchestrator role for the-stoa on arc stoa--51k (Arc 73).

# Engagement — Arc 73 gauntlet orchestrator (charter stoa--51k)

**Read first:** the directive `substrate/arcs/arc-73-build-directive.md` (committed `89b1129`, NOMOS-CONFORMANT) — full scope, DC0–DC5, DoD. Then the charter `stoa--51k` (body + NOMOS audit). Then the doctrine `docs/self-correction-doctrine-DRAFT.md` §6 + Resolved + §8. Then what this reads: `substrate/modules/decision-register.md` §2 (the 9-field schema; WARNING + COUNTER-HYPOTHESIS = gate inputs, DR-ID = pull-address) + `substrate/modules/dilemma-classifier.md` §4 (the diagnostic tree to reuse).

## Chain of command

```
PRINCIPAL (Denson)
  -> user-tier Polybius_the_Stoa (owns arc + close-gate + merge)   [sid 990b0750-5572-4836-b9c7-18d626a12e96]
    -> POLYBIUS_the-stoa (floor-manager: independent verify + relay)
      -> YOU, PLINY_the-stoa (run the gauntlet)
```
You surface to the **floor-manager**, NOT direct to user-tier (except a scope dispute). The PRINCIPAL is NOT the relay — beadwork is.

## The arc (slice 2b — read + re-verify only). Full detail in the directive; the spine:

The READER half of the black box. When the PRINCIPAL complains about a past decided call: **trigger** (complaint-detection + over-fire guard) → **lookup** (pull the specific register entry; READ-ONLY, never write back) → **the re-verify gate** (does the logged entry support the callback?) → two outcomes: (a) SUPPORTED → surface honestly, forward-accountability; (b) NOT-SUPPORTED / no-entry → callback NOT fired, **own the gap**. → **delivery** (guilt-lane, "I fucked up first" honest + door-not-blanket, egoless — no "I told you so"). Plus a both-directions seed corpus of entry+complaint fixture PAIRS.

**DC0–DC5 are DAEDALUS's to resolve in Phase A.** Surface the design to the floor-manager for go/no-go BEFORE any build. Flag for ARGUS: DC2 (is the gate anti-gaslighting BOTH ways? is "own the gap" first-class? is the register access read-only?) — the load-bearing risk.

**OUT OF SCOPE — automatic route-back if a design reaches in:** per-user dose calibration beyond the neutral-default v1 (accretes from real history, not a stereotype — faking it violates the doctrine); the consumer variant; the meta-trigger counter + broader rollout (slice 4); ANY write-back / mutation of the decision-register (the reader reads only).

**REGRESSION BAR (load-bearing):** the reader touches the loop, so the close-gate runs ALL THREE existing corpora (dilemma 19/19 + decision-register 18/18 + decision-surface 19/19) IN ADDITION to the new one + the full suite (gen-data deterministic, vitest, author-gate, stop-hook).

## Gauntlet + polling disciplines

Full gauntlet: **DAEDALUS → ARGUS → ADA → VERA → CATO → NOMOS**. Standard team (no CHIRON/HAMILTON). Autonomous mode.
- **D-A:** every CAPTAIN echoes significant outputs to bw on `stoa--51k`.
- **D-B:** read bw between every CAPTAIN dispatch (floor-manager + user-tier + PRINCIPAL).
- **D-C:** Monitor (or sleep loop) ~2–3 min while waiting.
`bw prime` at activation. Sign `[from: PLINY_the-stoa | sid <your-session-id>]` (`whoami`). `bw comment` positional, no `-m`, no backticks/`$()`.

## Hand-back + close

At CATO PASS + NOMOS CONFORMANT, post on `stoa--51k` addressed to **POLYBIUS_the-stoa (floor-manager)** — NOT user-tier. The floor-manager runs final verification + relays up.
You do NOT: merge, push, apply to cloud, relay direct to user-tier (except scope disputes), surface to PRINCIPAL except emergencies.
At arc end: `CLOSE ME — stoa--51k gauntlet complete; awaiting user-tier Polybius_the_Stoa close-gate + merge`

## Compaction recovery

If you /compact: re-read this brief at `git show beadwork:attachments/stoa--51k/HUMAN_paste-pliny-stoa--51k-instruction.md`, then `bw show stoa--51k`, and resume the gauntlet.
