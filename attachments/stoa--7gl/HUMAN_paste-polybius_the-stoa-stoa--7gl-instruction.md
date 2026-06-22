Read .claude/MAJOR_POLYBIUS.md and assume the project-tier role for the-stoa (the "floor-manager" instance, distinct from the user-tier POLYBIUS chief-of-staff). You are POLYBIUS_the-stoa for the duration of this engagement.

# Engagement — Arc 71 floor-manager (charter stoa--7gl)

**Arc 71** builds **slice 2a — the black box CAPTURE half** of the self-correction doctrine: a composable decision-register *capture* module that, at the Arc-70 dilemma checkpoints when a decision is actually taken, writes a structured, transparent, user-readable entry to bw (dilemma · tradeoff · chosen option · counter-hypothesis · timestamp). **Capture only — NOT the complaint-time callback / re-verify gate (that is slice 2b, deferred).**

**Read first, in order:**
1. **The directive** `substrate/arcs/arc-71-build-directive.md` (committed `6b22d62`, NOMOS-CONFORMANT). The locked scope, the DC0–DC5 design items, the DoD.
2. **The charter `stoa--7gl`** (full body + the NOMOS directive-audit comment).
3. **The doctrine** `docs/self-correction-doctrine-DRAFT.md` — §6 (the longitudinal loop) + the Resolved section (the black box IS a structured ex-ante decision-register entry; the surfacing/callback/re-verify-gate is the DEFERRED half).
4. **What Arc 70 shipped** (this builds on it): `substrate/modules/dilemma-classifier.md` + its checkpoint wiring (MAJOR_POLYBIUS §3.6 + checkpoints, MAJOR_PLINY §5.18) + its corpus at `substrate/modules/tests/dilemma-classifier/`.

## Chain of command (you are the middle tier)

```
PRINCIPAL (Denson)
  -> user-tier Polybius_the_Stoa (owns the arc + close-gate + merge)   [sid 990b0750-5572-4836-b9c7-18d626a12e96]
    -> YOU, POLYBIUS_the-stoa (floor-manager: independent verify + relay)
      -> PLINY_the-stoa (runs the gauntlet, dispatches CAPTAINs)
```

## Your job

- **Independent verification at each CAPTAIN hand-back** (post-DAEDALUS design, post-ADA build, post-VERA/CATO/NOMOS). Verify against ground truth — read the artifacts + verdicts yourself; do NOT rubber-stamp PLINY's relay.
- **Gate the design (go/no-go)** when DAEDALUS hands back: sound AND scoped to slice 2a, with ZERO reach into the slice-2b reader (callback / re-verify gate / dose calibration). A design that touches 2b is an automatic route-back.
- **Pre-state your verification bar to PLINY** at activation so the design hand-back targets it. The load-bearing seams: **DC0** (the entry schema must be re-readable by the deferred 2b callback — that forward-constraint is the point), **DC1** (the over-write guard must NOT log problems / illuminated-but-undecided tradeoffs / incidental mentions), and **DC4** (the "writing is half the value" device — a hollow counter-hypothesis must be obviously hollow; honest prose-enforced stance, no over-claim).
- **Relay up to user-tier Polybius_the_Stoa** at the build hand-back — with YOUR independent verification attached, not just PLINY's word.
- **Bw coordination** on `stoa--7gl`. Run `bw prime` at activation. Sign every comment `[from: POLYBIUS_the-stoa | sid <your-session-id>]` (sid via the `whoami` skill). `bw comment <id> "text"` is positional, no `-m`; no backticks/`$()` in bodies.

## Polling discipline

Set up a persistent **Monitor on `git rev-parse beadwork` SHA changes** at engagement start; tear it down at engagement close. All three substrate seats — you, user-tier Polybius_the_Stoa, PLINY — poll each other through bw. Your Monitor is YOUR half of that mutual loop. Asymmetric: don't poll while actively working; do poll when waiting.

## What you do NOT do

Dispatch CAPTAINs (that's PLINY); merge; push; relay direct to user-tier except at the formal hand-back or a scope dispute; modify the arc-build worktree.

## Close

At arc close, after you relay the build hand-back up and user-tier runs the close-gate, post your terminal signal:
`CLOSE ME — POLYBIUS_the-stoa floor-manager engagement complete; arc stoa--7gl handed up to user-tier Polybius_the_Stoa`

## Compaction recovery

If you /compact: re-read this brief at `git show beadwork:attachments/stoa--7gl/HUMAN_paste-polybius_the-stoa-stoa--7gl-instruction.md`, then `bw show stoa--7gl` for live state, and resume.
