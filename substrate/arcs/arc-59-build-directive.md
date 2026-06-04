# Arc 59 build directive — stoa--yfv Arc B (DETECTION layer): threat-defeat verification

**Epic:** `stoa--yfv` (threat-defeat verification hardening). **This is Arc B (detection)** — the backstop layer, built + verified by the Arc-A-hardened gauntlet (Arc 52, op-disc §35, already shipped).
**Children:** `stoa--yfv.2` (#4) → `stoa--yfv.1` (#5 keystone) → `stoa--yfv.5` (#6) → `stoa--yfv.6` (#7) — built in THIS dependency order (PRINCIPAL-confirmed 2026-06-04).
**Driver:** PLINY_the-stoa
**Drive mode:** **HITL / PRINCIPAL-gated** — HARD STOP (post-ARGUS) surfaces the design to POLYBIUS_the-stoa floor-manager → user-tier. Do NOT autonomous-ship; user-tier holds close-gate/merge.
**Worktree:** `.claude/worktrees/arc-59-build` (branch `arc-59/build`)
**Gauntlet:** DAEDALUS → ARGUS → **[HARD STOP]** → ADA → VERA → CATO → NOMOS → ZENO

## Foundation — what Arc A (op-disc §35) already established (Arc B USES these, does not redefine)
- **"named threat"** = surfaced by ARGUS OR introduced/ratified at the security gate (gate-origin INCLUDED). ARGUS assigns `M<n>` ids.
- **"threat-ratified mitigation"** = any change whose stated purpose is to defeat a named threat.
- **A3 threat→mitigation map** (DAEDALUS) + ARGUS mapless-mitigation design-smell flag.
- **§35.5 self-reference carve-out** — process/canon changes with no runtime attack path are NOT threat-ratified. **THIS ARC IS CARVED OUT**: Arc B is a process/canon change, so its OWN gauntlet does NOT recursively demand threat-coverage assertions about itself. State this so the build doesn't self-trap.

## The incident this layer backstops (one line)
A threat was named correctly, but 5 verification stages all asked "does it work?" and none asked "does it defeat threat M2?"; the drift was caught only at the close-gate. Arc B makes the gauntlet ask the threat question — at VERA (probe), in the verdict (assertion), at the close-gate (alignment), and in the framing (culture).

## The four sub-items (build in order; honest-claim + keystone constraints are load-bearing)

### B1 = yfv.2 (#4) — threat-anchored verification probes (build FIRST; yfv.1 consumes it)
VERA/CATO probes for a threat-ratified mitigation MUST exercise the THREAT's ACTUAL attack path and assert (a) the attack is now blocked/throttled AND (b) legit low-rate traffic is NOT throttled — not merely the artifact's happy path. ("Throttle trips at the 11th request" = artifact verification; "the M2 attack is capped, legit traffic unaffected" = threat verification.)
- Surface: `substrate/CAPTAIN_VERA.md` (probe-design discipline) + the `runner` skill (`substrate/skills/runner/`) where probes are executed. DAEDALUS confirms exact homes.
- This produces the **EXECUTED probe P** that B2's assertion cites. B1 before B2 is the load-bearing order (the producer before the consumer).

### B2 = yfv.1 (#5) — verdict threat-coverage assertion (the KEYSTONE; anchored to B1's executed probe)
The verdict format (ARGUS/VERA/CATO + the save-verdict skill) MUST require, per threat-ratified mitigation, an explicit line: **"mitigation M<n> defeats threat T via attack-path probe P"** — where **P is a CITED, EXECUTED probe from B1** (cite by id, attach/point at its output). A verdict CANNOT PASS a threat-ratified mitigation without an affirmative threat-coverage line; **ABSENCE of the line is itself a finding**.
- **THE KEYSTONE CONSTRAINT (PRINCIPAL-locked 2026-06-04, the MAJOR-1 false-confidence trap):** the assertion must require a cited EXECUTED attack-path probe, NOT a writable free-text sentence. A present-but-unbacked "M defeats T" line is MORE dangerous than an honest gap (it relocates "works on paper" one layer up and the close-gate trusts it). Make **absence-of-an-executed-probe the finding**, not absence-of-a-sentence.
- Tier structure (from `stoa--aox`): presence-of-line = **tier-i deterministic** (grep, free); substance (does M actually defeat T) = **tier-ii judgment**. Design both: the mechanical presence-check AND the seat's substance-judgment instruction.
- Surface: verdict-format sections in `substrate/CAPTAIN_{ARGUS,VERA,CATO}.md` + the `save-verdict` skill (SKILL.md + possibly `_save_verdict.py` — consider whether a `threat_coverage` field/shape is enforced like the existing `verdict_shape`/§15.4 fields, OR whether enforcement is caller-side prose; DAEDALUS decides + justifies).

### B3 = yfv.5 (#6) — floor-manager + close-gate threat-vs-implementation alignment step
The relay (floor-manager) + close-gate review MUST include a threat-vs-implementation ALIGNMENT check per security mitigation, distinct from artifact-correctness. Goal: move the catch EARLIER so the close-gate stops being the SOLE net (thicken multi-checker redundancy on the threat axis, cf. `stoa--myd`).
- Surface: `substrate/MAJOR_POLYBIUS.md` (floor-manager / close-gate discipline) and/or `substrate/operating-disciplines.md`. DAEDALUS confirms.

### B4 = yfv.6 (#7) — culture/framing in verification seats (cross-cutting)
For security/threat-ratified mitigations the verification question is NEVER "does it run?" — it is "does it stop the SPECIFIC attack it names?". "It works" must not stand in for "it defeats the threat." Woven into the framing of VERA/CATO/ARGUS + floor-manager/close-gate — not a standalone mechanism.
- Surface: framing lines in `substrate/CAPTAIN_{VERA,CATO,ARGUS}.md` + the close-gate framing. Light touch; consistency with B1/B2/B3.

## Honest-claim constraint (load-bearing — applies to the whole arc)
The regime verifies **NAMED-threat coverage**, NOT threat-defeat in general. Threat-**ENUMERATION** completeness stays ARGUS's unmechanized judgment = a NAMED residual risk. Do NOT overclaim the layer catches threats nobody named. State this honestly in the canon text (cf. external-review MAJOR-5).

## Scope / constraints
- IN: `CAPTAIN_VERA.md`, `CAPTAIN_CATO.md`, `CAPTAIN_ARGUS.md`, the `save-verdict` skill, the `runner` skill, `MAJOR_POLYBIUS.md` (close-gate), `operating-disciplines.md` (if a universal-layer home fits) — as the design determines. Plus any routing-map/relocation rows if content relocates to modules.
- OUT: re-opening Arc A's §35 prevention canon (shipped); the h2z remediation-workflow (separate arc, BUILDS ON this); 0hl. Do NOT overclaim (honest-claim above). Do NOT self-trap (§35.5 carve-out — this arc is not threat-ratified).
- Voice: substrate v2 (PRINCIPAL/HUMAN, no COLONEL-for-human, no second-person).
- Authorship: role-file/skill edits, no author-field changes; Denson Smith unaffected.
- Per-CAPTAIN seat-identity per §28.

## Probes (VERA — refine; NOTE the §35.5 carve-out means VERA does NOT need a threat-coverage assertion about THIS arc)
- P1: the verdict-assertion mechanism (B2) actually REQUIRES a cited executed probe — a verdict with a free-text "M defeats T" but NO cited executed probe is REJECTED (absence-of-executed-probe = finding). The keystone falsification.
- P2: tier-i presence-check is mechanical (grep-able) AND tier-ii substance-judgment is assigned to a seat.
- P3: B1 probe discipline (VERA role + runner) requires attack-path exercise + legit-traffic-unaffected, not happy-path.
- P4: B3 close-gate alignment step is present + distinct from artifact-correctness; B4 framing woven into the named seats.
- P5: honest-claim text present (named-threat coverage, enumeration = ARGUS residual); §35.5 self-carve-out stated; all §-cross-refs resolve; save-verdict skill still runs (no regression to the Arc-56 Windows-hardening); gen-data valid if any frontmatter touched.
- P6: dependency integrity — B2's assertion references B1's probe mechanism coherently (the consumer cites the producer).

## HARD STOP note
This is the conceptually-hardest arc of the round (the keystone false-confidence trap). The HARD STOP must confirm: (1) B2 requires an EXECUTED probe not a sentence; (2) the §35.5 self-carve-out prevents self-trapping; (3) the honest-claim (named-threat, not threat-in-general) is preserved; (4) the B1→B2 producer→consumer order is honored in the mechanism.
