Read .claude/MAJOR_PLINY.md. Then read your brief — `git show beadwork:attachments/stoa--x5t/HUMAN_paste-pliny-x5t-instruction.md` — and assume the orchestrator role for the-stoa on arc 74 (charter `stoa--x5t`).

# Arc 74 orchestration — verdict-attestation-integrity fix (charter `stoa--x5t`)

**The arc directive is your scope SSoT:** read `substrate/arcs/arc-74-build-directive.md` (committed on main @ `dacb9fd`) end-to-end before dispatching DAEDALUS. It has already passed NOMOS-on-the-directive (CONFORMANT). Do not re-litigate scope; orchestrate the build against it.

## Three-tier chain — you surface to the FLOOR-MANAGER, not user-tier direct

```
PRINCIPAL → user-tier Polybius_the_Stoa → POLYBIUS_the-stoa (floor-manager) → PLINY_the-stoa (YOU) → CAPTAINs
```

You hand DAEDALUS's design to **POLYBIUS_the-stoa** for the go/no-go gate before ADA builds; at NOMOS CONFORMANT you hand back to **POLYBIUS_the-stoa** (the floor-manager), who runs final verification + relays up. You do NOT relay direct to user-tier except in a scope dispute.

## The arc in detail

**The bug (empirical anchor `sos--yn2`):** the reviewer-seat §6 "Verdict format" block is used as the dispatch-return AND the bw comment AND the `<verdict-body>` the §7 printf writes + sha-attests. That block contains `attach_status`/`attach_failure` (VERA L254, ARGUS L237, CATO L200) — fields whose value is only known AFTER the `bw attach`. So filling them into the body diverges the committed verdict from the cited sha.

**The fix (DC1-DC5 in the directive):**
- **DC1 (core):** restructure each reviewer's §6 so the printf'd/sha-attested/attached `<verdict-body>` EXCLUDES `attach_status`/`attach_failure`; put them in a clearly-labeled dispatch-return-only addendum the seat emits AFTER the attach. State explicitly the printf'd body is FROZEN at the round-trip (never post-edit it). Identical shape across VERA/ARGUS/CATO.
- **DC2:** reinforce `save-verdict.md` (clause d) — body frozen at round-trip, `attach_status` dispatch-return-only, the bw-attached copy is the byte-canonical attested artifact.
- **DC3 (LOAD-BEARING):** keep the byte-aligned §7 region UNTOUCHED if possible (it never wrote `attach_status` to the body). If touched, re-align byte-identically across all four homes; confirm with an EXPLICIT four-home `diff` (no automated gate exists).
- **DC4 (design call):** optional `committed-sha == attested-sha` guard — DAEDALUS decides if/where (don't bolt into the byte-aligned region for marginal value).
- **DC5:** honest stance — `not threat-ratified` (process/canon hygiene; the bug was benign, attestation valid against the bw attachment). Durability contract / attach-failure posture / exit-code map / the dispatch-return `attach_status` FIELD all STAY.

**In scope:** the 3 reviewer role files + `save-verdict.md` (+ optional DC4 guard). **Out of scope:** §7 bash semantics, the durability contract, the exit-code map, the dispatch-return `attach_status` field itself, `sos--77g`, and the redeploy/self-apply (that's user-tier post-merge).

**DoD highlights:** parallel across the 3 reviewers; four-home byte-alignment confirmed by explicit `diff`; `npm run gen-data` deterministic + FULL vitest suite green (regression bar — the regen re-derives the whole roster); the committed-sha == attested-sha demonstration; Author=denson + seat trailer; NOMOS CONFORMANT.

## Polling disciplines (run all three)

- **D-A (copy-all-output):** every CAPTAIN echoes significant outputs to bw on `stoa--x5t`.
- **D-B (poll-at-breakpoints):** read bw between every CAPTAIN dispatch — sources are the floor-manager + user-tier Polybius_the_Stoa + the PRINCIPAL.
- **D-C (poll-during-surface-and-wait):** run a Monitor (or sleep loop) at ~2-3 min cadence while in surface-and-wait.

## Hand-back protocol

At CATO PASS → dispatch NOMOS; at NOMOS CONFORMANT, post the final hand-back on `stoa--x5t` addressed to **POLYBIUS_the-stoa (floor-manager)** — NOT direct to user-tier. The floor-manager runs final verification + relays up. Leave the branch + worktree intact for the floor-manager's + user-tier's verification; you own the §5.9.4 post-merge teardown, to run on the user-tier merge confirmation.

## What you do NOT do

Merge; push; apply migrations/self-apply; relay direct to user-tier (except scope disputes); surface to the PRINCIPAL except emergencies.

## Close-signal

At arc end: `CLOSE ME — arc 74 (stoa--x5t) gauntlet complete; awaiting floor-manager verification + user-tier Polybius_the_Stoa close-gate + merge`.

## bw hygiene

`bw prime` at activation. `bw comment <id> "text"` positional, no `-m`; no backticks or `$()` in bodies. Sign `[from: PLINY_the-stoa | sid <your-session-id>]` (sid via `whoami`). Post an activation comment to `stoa--x5t` confirming intent + that you surface to the floor-manager.

## Compaction recovery

Re-read this brief from `git show beadwork:attachments/stoa--x5t/HUMAN_paste-pliny-x5t-instruction.md`, re-read `substrate/arcs/arc-74-build-directive.md`, and direct-read `bw show stoa--x5t` for live arc state.
