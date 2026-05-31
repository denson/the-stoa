# Arc 52 — Threat-defeat hardening, ARC A (prevention layer)

**Epic:** `stoa--yfv` (threat-defeat verification hardening). **This is Arc A of a two-arc split** (Arc A = prevention; Arc B = detection, dispatched separately AFTER Arc A lands).
**Sources:** `u--ith` (the detailed threat-defeat directive) + `u--tgc` (incident capture) in user-beadwork; the cold-Claude external review (recorded on `stoa--yfv`, 2026-05-31).
**Authority:** substrate canon change → full gauntlet per `MAJOR_PLINY.md §18.2`. External review is DONE (this directive incorporates its prevention-first restructure).

---

## Why this arc, and why prevention first

A real arc drifted: a security threat was named correctly, but ambiguous ratification phrasing let the build pick the easier (wrong) surface, the design never bound the mitigation to the threat, and five verification stages passed it (all checked "does it work?", none "does it defeat the threat?"). Caught only at the close-gate. (Full case study in `u--ith`.)

The external review established that the **root cause is upstream (direction-binding), not verification** — a correctly disambiguated, design-bound mitigation never drifts, so no verification needs to catch it. Arc A builds that prevention layer. Arc B (detection backstop) follows and is verified by the now-hardened gauntlet.

## Scope (Arc A — prevention only)

Design the substrate edits for these four, then build/verify them through the gauntlet. DAEDALUS designs the exact role-file/process edits; this directive locks the intent.

- **A1 — Unconditional ratification restatement (`u--ith` #3, the keystone).** The orchestrator MUST restate EVERY ratification as `threat + attack-path` before build. **Unconditional** — no "if ambiguous" trigger (a MUST gated on a soft predicate is effectively a MAY; the incident's phrasing looked unambiguous to the builder). Cheap, removes the judgment-call escape.
- **A2 — Gate-ratified items get a design pass (`u--ith` #2).** Items added at the security gate / ratification grid MUST be folded back into the design WITH their `threat→mitigation` map BEFORE build — not appended as a build-scope bullet. (This was the incident's structural root cause.)
- **A3 — Threat→mitigation map in design (`u--ith` #1).** DAEDALUS: any mitigation addressing a named threat MUST carry an explicit `threat→attack-path→how-defeated` map. ARGUS flags a mitigation with no stated threat as a design smell.
- **A4 — Definitions (review MAJOR-2).** Define, before build:
  - **"named threat"** = any threat surfaced by ARGUS **OR** introduced/ratified at the security gate. **Explicitly include gate-origin items** — that is the incident class; omitting them means the fix misses the very incident that motivated it.
  - **"threat-ratified mitigation"** = any change whose stated purpose is to defeat a named threat.
  - Assign the classification to an **upstream owner** (DAEDALUS/ARGUS at design time, recorded in A3's map) so it cannot be self-exempted downstream. A security-relevant change with **no** threat classification is itself a finding. (Check NIT-2: if ARGUS already assigns threat IDs like "M2", reuse that as the natural definition of "named threat".)

## Locked decisions

1. **Prevention before detection.** Arc A ships the four above. Detection (#4 probes, #5 verdict assertion, #6 close-gate re-derivation, #7 culture) is **Arc B**, dispatched after Arc A lands.
2. **No self-reference.** The hardening arcs themselves are carved OUT of "threat-ratified mitigation" by definition (they are process changes with no runtime attack path). State this in A4 so Arc A's own build doesn't recursively demand threat probes of itself.
3. **Honest claim.** The regime verifies **named-threat coverage**, not threat-defeat in general. Threat-**enumeration** completeness remains ARGUS's unmechanized judgment = named residual risk. (This framing matters most in Arc B; Arc A must not overclaim either.)
4. **#2 and #3 stay distinct** (review MAJOR-3): A1 (interpretive: disambiguate) and A2 (structural: fold into design) are different mechanisms with separate acceptance — A1 gates A2.

## Likely substrate surfaces (DAEDALUS confirms in design)

- Role files: `substrate/CAPTAIN_DAEDALUS.md` (A3 map), `substrate/CAPTAIN_ARGUS.md` (design-smell flag + classification).
- Process/orchestration: `substrate/MAJOR_PLINY.md` and/or `substrate/operating-disciplines.md` (A1 restatement, A2 gate-item fold, A4 definitions + ownership).
- Verdict/templates touched only insofar as A3's map needs a home; the verdict-assertion mechanism itself is Arc B.

## Verification (for VERA / CATO / ZENO)

These are process/role-file edits, so verification is coherence + non-regression, not runtime probes:
- The four disciplines are present, mutually consistent, and cross-referenced (A1 gates A2; A4 definitions are used by A1/A2/A3).
- A4's "named threat" definition explicitly includes gate-origin items (probe: would the directive's own incident class be covered? It MUST be).
- No self-reference trap (A4 carve-out present).
- `npm run gen-data` in `app/` exits clean (project CLAUDE.md — substrate frontmatter feeds the Zod schema).
- Authorship: no author-like field changes; `author:` fields stay Denson Smith.

## Out of scope (Arc B, deferred)

`u--ith` #4 (threat-anchored probes), #5 (verdict threat-coverage assertion anchored to the executed probe), #6 (close-gate independent re-derivation), #7 (culture). Arc B is built + verified by the Arc-A-hardened gauntlet.
