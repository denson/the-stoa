# DIRECTIVE (re-forged) — stoa--reg liveness via ON-DEMAND RADIO-CHECK (u--5f0 remainder)

> **SUPERSEDES** the 2026-06-25 "stand-down write + TTL sweep" directive. Per
> Polybius the Grand (u--5f0, 2026-06-26 15:41, dir. PRINCIPAL): **simplify to the
> human-simple model — an on-demand radio-check ping; scrap the passive-liveness
> machinery.** The team designs against THIS scope; the superseded version is dead.

**Arc home (team):** `stoa--fii` (the-stoa beadwork). **User-tier arc:** `u--5f0`.
**Forged by:** Polybius_the_Stoa (sid 990b0750), supervising.
**Chain:** PRINCIPAL → Polybius the Grand → Polybius_the_Stoa → POLYBIUS_the-stoa (FM)
→ PLINY_the-stoa → gauntlet CAPTAINs.
**Composition:** STANDARD (FM + PLINY; no architects). **Gauntlet:** FULL.

---

## 1. Mission

Answer **"which seats are alive NOW"** *on demand*, with **no passive machinery** —
so user-tier / a coordinator stops losing track of seats — via a **radio-check PING
over beadwork**, not a stored/passive registry field.

## 2. Scope (Polybius the Grand, 2026-06-26 — SUPERSEDING)

1. **LIVENESS = an ON-DEMAND radio-check PING.** When user-tier / a coordinator needs
   to know if seats are alive, it **pings them via beadwork** (a bw post the seats see
   on their poll). Seats that **answer** are alive; **non-answerers within a reasonable
   window are PRESUMED dead.** ONLY when we need to know — **NO periodic sweep, NO
   `last_seen`, NO TTL, NO continuous monitoring.**
2. **RECOVERY = relaunch a REPLACEMENT, not resurrect.** A dead seat is not revived;
   user-tier Polybius spins up a fresh replacement (via `team-launcher`).
3. **`stoa--reg` stays the WHO** (the seat roster). The on-demand ping answers
   **WHETHER-alive-NOW.** Do **NOT** bake liveness into a passive registry field.

## 3. Honest-claim boundary (EXPLICIT — load-bearing)

A non-answer within the window = **PRESUMED dead, NOT proof of death** (a seat can be
alive but slow to poll, or between turns). Document this in the `stoa--reg` ticket +
the tooling, mirroring the existing `stoa--reg` audit-only honesty note.

## 4. What is OUT (scrapped from the prior, superseded scope)

Periodic sweep; `last_seen`; TTL; continuous monitoring; **any passive-liveness
registry field.** The `stoa--reg` row schema is **NOT** extended with a liveness
field — liveness is answered by the *live ping*, never stored. (The old `-Status`
stand-down write + TTL sweep are dead; do not build them.)

## 5. Scope IN

- The **radio-check PING protocol**: how user-tier / a coordinator posts the ping over
  beadwork (the convention — e.g. a `[radio-check]` bw post addressed to seats), how a
  seat ANSWERS, the "reasonable window," and how non-answerers are tallied presumed-dead.
- The **RECOVERY** path: relaunch a replacement (`team-launcher`), not resurrect — documented.
- The **doc**: `stoa--reg` stays the roster (WHO); the ping is the on-demand WHETHER;
  the honest-claim boundary.
- A **small helper IF warranted** (a radio-check skill or a documented bw protocol) —
  the team's design; do not over-build (the win is human-simple).
- A **probe**: ping → alive seats answer → silent seats read presumed-dead after the window.

## 6. Definition of Done

- [ ] The radio-check ping protocol is specified (post → seats answer → window → presumed-dead tally).
- [ ] Recovery = relaunch-a-replacement is documented (no resurrection).
- [ ] `stoa--reg` stays the roster; **NO passive liveness field added**; the honest-claim
      boundary documented (non-answer = presumed, not proof).
- [ ] A **probe demonstrates** the radio-check end-to-end.
- [ ] Full gauntlet PASS + NOMOS CONFORMANT; FM independent verify; reported up.
- [ ] Author = Denson Smith; deployed `.claude/` regen on main is the post-merge §18.1 self-apply.

## 7. Reuse / inputs

The **radio-check pattern** (`feedback_radio_check_pattern_for_polybius_coordination`
— the silent-peer detection discipline this generalizes). `stoa--reg` (the roster
contract + its audit-only honest-claim note — the model to mirror). `team-launcher`
(the relaunch path for recovery). bw (the ping channel).

## 8. Flow

DAEDALUS designs the radio-check protocol → full gauntlet (ARGUS/ADA/VERA/CATO/NOMOS;
the probe is VERA's) → FM independent verify each hand-back → relay up to
Polybius_the_Stoa → close-gate + report up to Polybius the Grand.

---

**Author:** Denson Smith.
