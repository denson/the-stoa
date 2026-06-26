# DIRECTIVE — stoa--reg liveness reconciliation (u--5f0 remainder)

**Arc home (team):** `stoa--fii` (the-stoa beadwork). **User-tier arc:** `u--5f0` (the open remainder).
**Forged by:** Polybius_the_Stoa (sid 990b0750), supervising from user-tier.
**Chain:** PRINCIPAL → Polybius the Grand → Polybius_the_Stoa (supervise) →
POLYBIUS_the-stoa (FM) → PLINY_the-stoa → gauntlet CAPTAINs.
**Composition:** STANDARD (FM + PLINY; **no** CHIRON/HAMILTON — no new agents or
workflows are designed). **Gauntlet:** FULL (DAEDALUS → ARGUS → ADA → VERA → CATO →
NOMOS) — it touches the launcher + `record-seat.ps1` + the registry contract, so it
is substrate-canonical and earns the full gauntlet.

> **Sequencing (Grand):** forge this directive + the two briefs NOW; **launch only
> after the u--9s2 the-stoa seats free up** (reuse the freed POLYBIUS_the-stoa +
> PLINY; do **not** spin a distinct scratch slug). The interim hand-flip already
> holds the registry honest meanwhile, so there is no urgency to launch early.

---

## 1. Mission (the WHAT)

Make the `stoa--reg` seat registry **stop lying.** Today every row is written
`status:alive` and **nothing ever flips it to dead** — `record-seat.ps1` only writes
`alive`. So the registry accretes stale-alive rows and cannot answer "which seats are
actually live," which is the **root cause of losing track of seats**. Add **liveness
reconciliation** so a row reflects reality.

Greenlit scope (Polybius the Grand, 2026-06-25) — **BOTH** mechanisms, not one:

### (1) Stand-down write — graceful death
A seat/team that ends cleanly writes its row `dead`.
- `record-seat.ps1` gains a **`-Status`** parameter (default `alive`; `dead` marks
  the row dead), idempotent on `(seat, machine)` as today — **or** a sibling
  `close-seat.ps1` helper if cleaner. The team picks the shape.
- The **FM / launcher marks the team dead at arc close** (the teardown step calls it
  per seat). This is the graceful path: a seat that stands down records its own death.

### (2) TTL / liveness sweep — abrupt death
For seats that die **without** a graceful stand-down (crash, session-exit, /compact
orphan — the case that bit us): a heuristic sweep.
- Add a **`last_seen`** field (set/refreshed whenever a row is recorded/re-recorded).
- Define a **TTL**. The **launcher folds a sweep in at spin-up**: any row whose
  `last_seen` is older than the TTL is marked **presumed-dead**.

### (3) Honest-claim boundary — EXPLICIT (load-bearing)
A sweep cannot *prove* a seat is dead — a live-but-quiet seat that hasn't re-recorded
looks identical to a dead one. So **sweep-dead is a PRESUMED-dead heuristic, NOT proof
of death.** Document this explicitly in the `stoa--reg` ticket body AND in the tooling,
**mirroring the existing `stoa--reg` audit-only honesty note** (the provenance tag is
forgeable / audit-only). The design SHOULD distinguish a graceful `dead` from a
swept **presumed-dead** so a reader can tell proof from heuristic (e.g. distinct
`status` values, or a `presumed` flag — the team's call).

---

## 2. Constraints & locks

- **Idempotent + race-safe** on `(seat, machine)`, exactly as `record-seat.ps1` is
  today (read-modify-rewrite-attach). The stand-down write replaces, never appends.
- **The registry rows stay AUDIT-ONLY** — this arc does not wire liveness into any
  authz/authentication decision (the `stoa--reg` honest-claim boundary stands).
- **No cross-machine liveness proof** — `last_seen` + TTL is a same-store heuristic;
  presumed-dead is presumed, never asserted as fact.
- **Backward-compatible rows** — older rows that predate `last_seen` must still parse
  (mirror the additive-field discipline Arc 68 used for composition/gauntlet/chain_role).
- **Schema delta is minimal** — `last_seen` + the `status`/presumed semantics only;
  no broader registry rework.

---

## 3. Scope boundary

**IN:** the `-Status`/`close-seat` graceful stand-down write; the `last_seen` field;
the launcher spin-up sweep + a TTL; the presumed-dead-vs-dead representation; the
honest-claim-boundary documentation (ticket + tooling); wiring the FM/launcher
arc-close teardown to mark the team dead; tests/probes for both paths.

**OUT:** any authz/authn use of the rows; cross-machine liveness proof; a registry
schema rework beyond `last_seen` + status semantics; a UI/dashboard.

---

## 4. Definition of Done

- [ ] `record-seat.ps1` can write `status:dead` (graceful), idempotent on `(seat,machine)`.
- [ ] `last_seen` is recorded + refreshed on every record/re-record; older rows still parse.
- [ ] The launcher sweep at spin-up marks TTL-exceeded rows **presumed-dead** — distinct
      from a graceful `dead` (the reader can tell heuristic from proof).
- [ ] The **honest-claim boundary** is documented in the `stoa--reg` ticket body AND the
      tooling (sweep-dead = presumed, NOT proof), mirroring the audit-only note.
- [ ] The FM/launcher **arc-close teardown** marks the team's seats dead (graceful path wired).
- [ ] A **probe demonstrates the registry stops accreting stale-alive rows**: record a
      seat → sweep past TTL → it reads presumed-dead; stand-down → it reads dead.
- [ ] Full gauntlet PASS + NOMOS CONFORMANT; FM independent verify; reported up.
- [ ] Author = Denson Smith; deployed `.claude/` regen on main is the post-merge §18.1
      self-apply (record-seat/launch-team are deployed copies — keep source = substrate SSoT).

---

## 5. Reuse / inputs

`record-seat.ps1` + `launch-team.ps1` (the `team-launcher` skill; both the substrate
source under `substrate/skills/team-launcher/` and the deployed `.claude/` copies —
substrate is the SSoT). The `stoa--reg` ticket contract + its audit-only honest-claim
note (the model to mirror). The `whoami` skill (the sid source). The Arc-68 additive-
field discipline (composition/gauntlet/chain_role) as the pattern for adding `last_seen`.

---

## 6. Flow

1. DAEDALUS designs the mechanism (the `-Status`/close-seat shape, the `last_seen`+TTL
   sweep, the presumed-vs-dead representation, the honest-claim doc).
2. Full gauntlet: ARGUS cold-audit → ADA build → VERA verify (the probe in DoD) →
   CATO → NOMOS.
3. FM independently verifies each hand-back; relays up to Polybius_the_Stoa.
4. Polybius_the_Stoa close-gates + reports up to Polybius the Grand; the deployed
   `.claude/` regen is the post-merge self-apply on main.

---

**Author:** Denson Smith.
