Read .claude/MAJOR_PLINY.md and assume the orchestrator role for the-stoa on arc stoa--xa4 (Arc 72).

# Engagement — Arc 72 gauntlet orchestrator (charter stoa--xa4)

**Read first:** the directive `substrate/arcs/arc-72-build-directive.md` (committed `772c67b`, NOMOS-CONFORMANT) — full scope, DC0–DC4, DoD. Then the charter `stoa--xa4` (body + NOMOS audit). Then `substrate/skills/decision-surface/SKILL.md` (the DRAFT being graduated + its "Open questions" list) + `worked-example-debloat.md`. Then the two shipped modules you wire: `substrate/modules/dilemma-classifier.md` (§2 self-check, §3 delivery) + `substrate/modules/decision-register.md` (§2 nine-field schema). Then the doctrine `docs/self-correction-doctrine-DRAFT.md` (§1/§3/§5/§6/§7).

## Chain of command

```
PRINCIPAL (Denson)
  -> user-tier Polybius_the_Stoa (owns arc + close-gate + merge)   [sid 990b0750-5572-4836-b9c7-18d626a12e96]
    -> POLYBIUS_the-stoa (floor-manager: independent verify + relay)
      -> YOU, PLINY_the-stoa (run the gauntlet)
```
You surface to the **floor-manager**, NOT direct to user-tier (except a scope dispute). The PRINCIPAL is NOT the relay — beadwork is.

## The reframe driving the arc (hold it through every CAPTAIN)

The value is NOT classifying dilemma-vs-not; it is **flagging** we MAY be in a no-clean-answer situation and **guiding** the human through deciding — a *process*, not a verdict. An agent running a process has no label to be argued off of (this dissolves the cave-trap). Firmness relocates from "hold the verdict" to "ensure the deciding happens with the tradeoff visible."

## The arc (slice 3). Full detail in the directive; the spine:

1. **Flag-and-guide retune** of `dilemma-classifier.md` §3 — detection opens the guide (a process), stops asserting a verdict. **§1 LOCKED + §2 self-check UNTOUCHED** (diff must prove the spine survived).
2. **Graduate `decision-surface`** — resolve open Qs with worked content: Q1 detection signals, Q4 render-vs-prose threshold, Q5 dilemma-honesty-under-pressure (reuse the §2 self-check as the cave-trap mechanism); Q2 expert-sourcing ships a v1 grounded-web-search sub-step (accretes); strip DRAFT.
3. **One-loop wiring + shared schema** — the guide's output IS the decision-register 9-field schema; resolve skill-vs-module reachability (decision-surface is a SKILL; the checkpoints fire on POLYBIUS/PLINY who HAVE the Skill tool).
4. **Deploy** — add `decision-surface` to `install.sh` SKILL_NAMES; fix app/install.sh parity; **close `stoa--ida`**.
5. **Corpus** — incl **cave-resistance fixtures** (pressure-to-verdict → guide holds the tradeoff, does NOT cave; the Arc-70 pressure-fixture analog), stated floor, `--check-corpus`/`--judge` split.

**DC0–DC4 are DAEDALUS's to resolve in Phase A.** Surface the design to the floor-manager for go/no-go BEFORE any build. Flag for ARGUS: DC0 (does the §3 retune weaken the spine? — the load-bearing risk) + DC2 (is the schema-share literal, no translation?).

**OUT OF SCOPE — automatic route-back if a design reaches in:** the consumer-tier variant (Q3, its own artifact); slice 2b (callback + re-verify gate); meta-trigger counter (arc 4); broader rollout; rebuilding Part-2 rendering (interactive-html-preview ships, decision-surface drives it).

**REGRESSION BAR (load-bearing):** this arc edits two shipped modules, so the close-gate runs BOTH existing corpora (dilemma 19/19 + decision-register 18/18) IN ADDITION to the new one + the full suite (gen-data deterministic, vitest, author-gate, stop-hook). Editing shared machinery is where regressions hide.

## Gauntlet + polling disciplines

Full gauntlet: **DAEDALUS → ARGUS → ADA → VERA → CATO → NOMOS**. Standard team (no CHIRON/HAMILTON). Autonomous mode.
- **D-A:** every CAPTAIN echoes significant outputs to bw on `stoa--xa4`.
- **D-B:** read bw between every CAPTAIN dispatch (floor-manager + user-tier + PRINCIPAL).
- **D-C:** Monitor (or sleep loop) ~2–3 min while waiting.
`bw prime` at activation. Sign `[from: PLINY_the-stoa | sid <your-session-id>]` (`whoami`). `bw comment` positional, no `-m`, no backticks/`$()`.

## Hand-back + close

At CATO PASS + NOMOS CONFORMANT, post on `stoa--xa4` addressed to **POLYBIUS_the-stoa (floor-manager)** — NOT user-tier. The floor-manager runs final verification + relays up.
You do NOT: merge, push, apply to cloud, relay direct to user-tier (except scope disputes), surface to PRINCIPAL except emergencies.
At arc end: `CLOSE ME — stoa--xa4 gauntlet complete; awaiting user-tier Polybius_the_Stoa close-gate + merge`

## Compaction recovery

If you /compact: re-read this brief at `git show beadwork:attachments/stoa--xa4/HUMAN_paste-pliny-stoa--xa4-instruction.md`, then `bw show stoa--xa4`, and resume the gauntlet.
