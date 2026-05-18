Re-read .claude/MAJOR_POLYBIUS.md and assume the project-tier chief-of-staff role for the-stoa. (Post-`/clear`; role refresh from canon file.)

**Your immediate intent for this engagement:** FOURTH-PASS SPEC AUDIT (R4). You did R1 (`SPEC_AUDIT.md`, commit `4f4674e`) + R2 (`SPEC_AUDIT_R2.md`, commit `a50a1a8`) + R3 (`SPEC_AUDIT_R3.md`, commit `b858b92`). User-tier POLYBIUS folded R3's findings via commit `edd0de8` — NC6 back-reference propagation (5 cite-fixes at §13.10/§13.11/§13.13/§14) + NC7 bucketing-list restructure (option b — removed the §13.5-§13.8+§13.9+§13.10 enumeration from §12.3/§12.5; replaced with dynamic-walk-of-§13 instruction).

R4 tests whether the propagation fix actually closed both NC6 + NC7 + whether the structural §12 staleness drift class is NOW fully closed (R3 verdict was "STILL LATENT"; this fold-in is the second iteration on the structural fix).

R4 scope is narrow — 1 file changed; 10 insertions / 15 deletions. Expected wall-clock: 15-25 min.

**Operating mode:** Mode 2 (exploration) with ARGUS-discipline overlay (surface concerns; do NOT propose fixes; do NOT execute changes; do NOT dispatch any arc).

---

## What changed since SPEC_AUDIT_R3.md (commit `edd0de8`)

**One file edited (SPECIFICATION.md). Two categories of fix per the R3 NC6 + NC7 findings:**

### NC6 — back-reference propagation (5 cite-fixes)

R3 surfaced 5 sections that still treated §12 as snapshot/catalogue/keep-list after the structural §12 rewrite. Each replaced:

| Section | Old framing (R3 NC6) | New framing |
|---|---|---|
| **§13.10 bullet 3** | "§12 (current state snapshot) updates ..." | "§12 (structural definitions + queries) verified consistent ... QUERIES still return useful answers ..." |
| **§13.10 bullet 4** | "§12.5 ... shrinks as Passes close gaps ..." | "§13.5-§13.10 + §13.14 (which collectively constitute the ticket-placement gap-list per §12.5) reflect post-Pass-7 reality ..." |
| **§13.11 bullets** | "matches §12.3 ... §12.4's catalogue ... §12.4's keep-list" | check against §12.4 clean-state DEFINITION + dynamic-walk-of-§13 placement query |
| **§13.13 criterion 3** | "matches §12.4 catalogue" | "per §12.4's clean-state definition" with explicit components named |
| **§14 PRINCIPAL editing notes** | "§12 Current state — corrections to what's shipped / open / in flight" (treats §12 as state-carrier) | "§12 Current state — does the structural definitions + queries shape match how substrate state should be referenced from this spec?" |

### NC7 — bucketing-list restructure (option b)

§12.3 + §12.5 previously enumerated the bucketing-list as `§13.5-§13.8 + §13.9 + §13.10`. The R3 NC7 finding was that `stoa--lyw` is placed at §13.14 (out of scope for spec-met), so running the bucketing query against the enumerated list produced a false-positive on lyw.

The structural fix (option b): REMOVE the enumeration entirely. §12.3 + §12.5 now instruct the reader / validate-spec skill to "walk §13 end-to-end to find ticket placements" with explicit reasoning that any §12-side enumeration of §13.x ticket-placing sections would itself drift whenever new §13.x sections place tickets.

The bucketing-list enumeration was the LAST residual state-snapshot inside §12.x; with NC7 fix, the §12 staleness drift class should be **fully closed at §12-level** (no enumerations of any kind remain in §12.1-§12.5 that can drift when source-of-truth advances).

---

## What R4 audits (priority order)

### R4.1 Per-R3-finding verification

For each R3 finding, verify the fold-in's disposition is correct:

- **NC6** (5 cite-fixes) — each of the 5 back-references now reads coherently against §12's new structural shape; no remaining "snapshot / catalogue / keep-list" residue at the named cite locations OR anywhere else in §13.x / §14.
- **NC7** (option b restructure) — §12.3 + §12.5 no longer carry the bucketing-list enumeration; the dynamic-walk-of-§13 instruction is actionable (a fresh team or validate-spec skill running it would correctly place all 18 open tickets including stoa--lyw).
- **R3 △ items** (C2 pattern transformation; M6 carried; W3 carried) — verify these are unchanged from R3 (they were carryovers, not fold-in targets).

### R4.2 Structural §12 drift class — is it now fully closed?

The load-bearing R4 test. R3 verdict was "STILL LATENT" with two surfaces (NC6 latent + NC7 current). This fold-in addresses both. Verify the closure:

- **No state-snapshot content anywhere in §12.1-§12.5** — verify §12.x carries ONLY structural contracts + queries + brief disclaimed reference-points. No per-ticket / per-arc / per-commit / per-§13.x enumerations.
- **No back-references in §13.x / §14 / elsewhere that treat §12 as state-carrier** — re-grep for "catalogue" + "keep-list" + "current state snapshot" + "§12 ... updates" + "§12.x ... shrinks" + similar shape-of-state-snapshot language. If any survives, flag it.
- **The §12.3 + §12.5 dynamic-walk-of-§13 instruction is actionable** — walk §13 yourself; can you mechanically place all 18 open tickets without needing a §12-side hint about which §13.x sections to look at?
- **No new latent mechanisms introduced** — the structural rewrite was small (10 insertions, 15 deletions). Did the rewrite introduce ANY new surface that could drift when something advances? If so, name the mechanism.

### R4.3 Fresh-eyes on the new §13.10 bullet 3-4 + §13.11 bullets + §13.13 criterion 3 + §14 prose

Standard ARGUS-discipline fresh-read on the ~10 lines of new prose for:
- Ambiguities introduced by the rewrite.
- New contradictions between the revised sections and other sections.
- Cross-ref errors.
- "I don't understand" items.

### R4.4 Substrate-state re-check

Re-run live checks:

- `bw list --status open --all` returns N tickets. Walk each against §13 ticket-placing sections per the §12.3 + §12.5 dynamic-walk instruction. Verify no unplaced tickets (lyw should now be discoverable at §13.14 via the walk).
- `git log` matches §12.1's reference SHAs.
- Working tree status matches §12.4's clean-state definition.
- SKILL.md frontmatter + body still agree on MANDATORY (no regression from R3).
- stellation-SPECIFICATION.md cross-refs all still resolve (no regression from R3).

### R4.5 Meta-verdict on the §12 staleness pattern

The load-bearing answer. R3 surfaced "STILL LATENT" because the structural fix transformed rather than closed the drift class. This fold-in addresses both surfaces R3 named. Three possible verdicts:

- **"Fully closed structurally"** — no current instance, no latent mechanism. The drift class is genuinely eliminated. N=2 strong empirical support for the broader "structural > procedural" substrate principle (per §4.6 TIRO + §27 mechanical/agent split + this §12 fix).
- **"Still latent at <mechanism>"** — yet another surface exists where the pattern could recur. Surface the mechanism; the spec needs another iteration OR PRINCIPAL accepts the residual.
- **"Current instance found at <location>"** — the fix introduced a new instance OR an existing instance was missed. The spec needs another iteration.

If R4's verdict is "fully closed," the iteration cadence has converged (R1: 49 findings → R2: 5 → R3: 2 → R4: 0 expected) and the spec is ready for Arc 38 dispatch. If R4's verdict is "still latent" or "current instance," PRINCIPAL + user-tier POLYBIUS decide whether to iterate again or accept the residual and ship.

---

## Required R4 output

Produce `SPEC_AUDIT_R4.md` at repo root, structured by:

1. **Per-R3-finding verification table** — one row per R3 finding (NC6 with 5 sub-rows; NC7; C2 + M6 + W3 carryovers).
2. **Structural §12 drift class closure verification (R4.2)** — pass/fail per sub-check.
3. **New issues found (R4.3)** — fresh items, if any.
4. **Substrate-state re-check (R4.4)** — like R3 §4, updated for current main + post-R3-fold-in state.
5. **Meta-verdict on the §12 staleness pattern (R4.5)** — load-bearing answer: "fully closed structurally" / "still latent at <mechanism>" / "current instance found at <location>."
6. **Closing observation** — meta-pattern across R1+R2+R3+R4. If R4 closes the pattern: what does the closure look like vs the pre-R4 state? If not: what does the residual tell us?

### Output discipline (same as R1+R2+R3)

- ARGUS-discipline: surface, do not fix.
- N=1 honesty per `operating-disciplines.md` §6.7.1.

---

## Constraints (same as prior audits)

- DO NOT dispatch any arc.
- DO NOT propose fixes.
- DO NOT edit SPECIFICATION.md or other substrate files.
- DO NOT touch stellation workspace.

## bw query discipline

`bw list --all` per cookbook + §12.3 explicit guidance. CAPTAIN_TIRO still doesn't exist (Arc 38 candidate stoa--ojz).

---

## Sub-dispatch authority

Single-seat-direct per R1+R2+R3 precedent (smaller scope). PLINY (paste at `HUMAN_paste-pliny-spec-audit-r4-instruction.md`) can dispatch CAPTAINs if needed.

## Coordination

- PLINY is your radio-check peer.
- Coordination ticket: file a fresh one (e.g., "spec-audit R4 engagement coordination"). `[from: polybius-the-stoa]` tags. **Close it on engagement-end** (R1 omitted; R2+R3 corrected; maintain).
- User-tier POLYBIUS upper-tier escalation via `[for: user-tier-polybius]`.
- PRINCIPAL exception-handler.

## Polling cron + renewal per Arc 36 v2 §11 step 1.5

Set up `*/5 * * * *` polling cron + +144h renewal. R4 short; renewal won't fire; canon application forward.

## Closure

When SPEC_AUDIT_R4.md complete:
1. Commit + push.
2. Post `[from: polybius-the-stoa]` closure comment on R4 coord ticket.
3. Close the R4 coord ticket per engagement-end discipline.
4. Tag `[for: user-tier-polybius]` for handoff.
5. Surface to PRINCIPAL with one-line summary including the meta-verdict.
6. Stand down with `[radio-check polybius-the-stoa standing down]`; CronDelete polling + renewal crons.

---

## Self-application

If R4's meta-verdict is "fully closed structurally," that's substantial empirical signal for the substrate principle. The iteration cadence (R1 → R4) will have converged on a single underlying drift class via successive structural narrowings. If R4's verdict is "still latent" or "current instance," the substrate principle needs refinement — possibly to "structural fixes narrow drift surface but require propagation iteration to fully close."

If compaction or /clear erases your role, re-read this paste from `HUMAN_paste-polybius-spec-audit-r4-instruction.md` in the project root.
