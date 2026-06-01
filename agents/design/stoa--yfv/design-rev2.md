# Arc 52 ARC A — Threat-defeat prevention layer (design-rev2)

**Ticket:** `stoa--yfv` (Arc A, prevention). **Seat:** CAPTAIN_DAEDALUS (architect).
**Directive:** `substrate/arcs/arc-52-threat-defeat-prevention-directive.md` (authoritative scope).
**Supersedes:** `design-rev1.md` (committed 87b6e5b) — rev1 preserved for the audit trail; this file is the revision ARGUS-rev2 audits.
**Audited-against:** `agents/verdicts/stoa--yfv/ARGUS-2026-06-01T01-04-29Z.md` (verdict: revise; risks r1–r5).
**Worktree:** `.claude/worktrees/arc-52-build/`; source canon edited is `substrate/` (re-deploys via `install.sh`).

---

## Changes from rev1 (each mapped to the ARGUS risk it closes)

| Change | Closes | What changed |
|---|---|---|
| **(a) Locus-independent "named threat" definition** | **r1 + r4** | §35.1(b) no longer binds gate-origin to "the HARD STOP / phase-ratification surface" (a term with ZERO matches in shipped canon). It now reads "introduced or ratified at **ANY ratification point**" and ENUMERATES the real ones (design-critique pause; PRINCIPAL/floor-manager scope ratification, **including mid-arc**; a ratification grid). Coverage rides on A1's UNCONDITIONAL sweep over every ratification, not on naming one canonical gate. The `HARD STOP` referent is PURGED everywhere it was the load-bearing locus (§35.1, §5.13, probe text, §6 out-of-scope, weak points). The directive-mandated "**gate-origin threats are explicitly included**" clause is KEPT (it is the incident class). |
| **(b) Named pre-ADA gauntlet beat in PLINY §5** | **r2** | §5.13 is restructured to serve **double-duty**: it is BOTH the A1 rule AND a NAMED gauntlet beat ("Pre-ADA ratification-restatement beat") with a concrete WHEN — *after ARGUS's verdict, before the ADA dispatch*. The §5 gauntlet sequence diagram (L130–147) gets an explicit annotation: a ratification-restatement gate sits between ARGUS and ADA. A cold reader can now locate A1's firing moment in the pipeline. |
| **(c) ARGUS CONFIRMS the self-reference carve-out** | **r3** | §35.5 + `CAPTAIN_ARGUS.md` §6.9 now state the carve-out classification ("process change, no runtime attack path") is **proposed by the building seat and CONFIRMED by ARGUS at critique time** (ARGUS already owns A4 classification per §35.1 — no new seat). An unconfirmed or wrong "just a process change" claim is a finding ARGUS catches. The self-assertable exit is closed. |
| **(d) Byte-align the A3 map template** | **r5** | The `M<n> → attack-path → how-defeated` map template now carries the **identical full annotated arrow-chain wording** in all three inline authoring copies (`operating-disciplines.md` §35.4, `CAPTAIN_DAEDALUS.md` §3, `CAPTAIN_DAEDALUS.md` §6.12). rev1's DAEDALUS §3 short-form is replaced with the full form. P5 makes word-identity a build-time check. |

**Preserved CLEAN from rev1 (ARGUS non-findings — do NOT regress):** all four insertion points (op-disc §35-after-§34; PLINY §5.13-after-§5.12; DAEDALUS §6.12-after-§6.11 + §3 at ~L47; ARGUS §6.9-after-§6.8); §25 PRINCIPAL-gate mirror; A1 text UNCONDITIONAL (no soft predicate); A1-gates-A2 as a distinct-mechanism gate; honest-claim does not overclaim; scope clean (NO Arc B detection mechanism); `author:` stays Denson Smith.

---

## §1. Problem restatement

A real arc (`origindex-trw` shared-auth, 2026-05-31) drifted: ARGUS named a security threat correctly ("M2"), but the ratification phrasing was ambiguous, so the build picked a plausible-but-wrong surface; the design never bound the mitigation to the threat; five verification stages passed it (all asked "does it work?", none "does it defeat M2?"). The external review established the **root cause is upstream direction-binding, not verification** — a correctly disambiguated, design-bound mitigation never drifts. Arc A builds the prevention layer (four disciplines A1–A4); Arc B (detection) is OUT of scope and dispatched later.

**The rev1→rev2 root correction (named per §6.1).** rev1 bound the entire gate-origin concept and A1's firing moment to "the HARD STOP / phase-ratification surface." ARGUS r1 established that **"HARD STOP" is dispatch-brief / floor-manager-workflow vocabulary with ZERO matches in shipped substrate**, and the PLINY §5 gauntlet sequence (DAEDALUS→ARGUS→ADA→VERA→CATO) has **no ratification beat between ARGUS and ADA**. A cold reader of the shipped §35.1 could not resolve the referent. rev2's locked resolution makes the design **locus-independent**: it does not name one canonical gate; it makes A1 sweep EVERY ratification unconditionally, and enumerates the real ratification points so gate-origin coverage cannot fall through a locus a reader fails to recognize.

**Imported assumptions I am naming (per §6.1):**

1. **The substrate has no single formal "security gate" object, and rev2 deliberately does not create one.** (The directive §6 defers a formal gate object to a separate design; the floor-manager REJECTED creating one for this arc.) Instead of mapping "the security gate" onto one substrate moment, rev2 treats "ratification point" as a **set** — every moment where a design, a scope item, or a risk set is ratified — and binds coverage to A1's unconditional sweep over that set. This is the core difference from rev1, which picked one locus (HARD STOP) and bound everything to it.
2. **ARGUS does not yet assign threat IDs.** "M2" is origindex-trw-local, not a substrate convention. Per the directive's NIT-2 check, A4 *establishes* the `M<n>` named-threat-ID convention and assigns issuance to ARGUS (critique time) + DAEDALUS (design time). (Unchanged from rev1; ARGUS verified this clean.)
3. **The four disciplines are a cluster.** A4's definitions are CONSUMED by A1/A2/A3, so they live in ONE universal locus (`operating-disciplines.md` §35) with thin per-seat stubs — mirroring §25 (PRINCIPAL-gate). (Unchanged; ARGUS verified the §25 mirror faithful.)

This restatement converges with the directive and the LOCKED rev2 resolution; the imported assumptions are scope the directive left implicit, surfaced rather than smoothed.

---

## §2. Approach — the four disciplines and their homes

### Structural decision (load-bearing, unchanged from rev1, ARGUS-verified)

A4's definitions are consumed by A1, A2, and A3. Therefore the **definitions + orchestration mechanics (A1, A2) + ownership assignment (A4) live in ONE new universal section** at `operating-disciplines.md` **§35** (next free number; §34 is current last). The two CAPTAIN seats carry **thin stubs** pointing at §35:

- DAEDALUS: A3 map-authoring — folded into the §3 write-to-disk shape + a new §6.12 stub.
- ARGUS: A3 design-smell flag (mapless mitigation) + A4 classification/carve-out **confirmation** — a new §6.9 stub.

This mirrors §25 (universal locus + per-seat behavior table + per-seat envelope stubs). ARGUS verified the mirror faithful; rev2 keeps it.

### The locus-independence decision (rev2 core — fixes r1/r4)

**A1 makes coverage locus-independent.** Because A1 restates EVERY ratification UNCONDITIONALLY, the question "is this gate-origin threat covered?" never depends on a reader recognizing a specific canonical gate. Any ratification — wherever it happens — gets restated as `threat + attack-path`; if it names a threat, it is a named threat by §35.1(b), and A2 fires. The §35.1(b) enumeration (design-critique pause; PRINCIPAL/floor-manager scope ratification, including mid-arc; ratification grid) is **illustrative-and-inclusive, not exhaustive**: the binding word is "ANY ratification point," and the list shows the reader the real ones — especially the mid-arc PRINCIPAL scope ratification that r4 identified as the case rev1 could miss.

### How A1 gates A2 (kept distinct per locked decision #4, unchanged, ARGUS-verified)

A1 and A2 are **different mechanisms with separate acceptance**, sequenced A1→A2:

- **A1 (interpretive — disambiguate).** Before any build, the orchestrator restates EVERY ratification as `threat + attack-path`. Unconditional. Output: one line per ratified item on the bw record.
- **A2 (structural — fold into design).** Any item A1's restatement reveals to be a **threat-ratified mitigation** MUST be folded back into the DESIGN with its `threat → mitigation` map BEFORE build — not appended as a build-scope bullet.

**The gate:** A2's fold-in trigger is evaluated against A1's restatement output; an un-restated ratified item is itself an A1 violation and the build does not proceed. A1 classifies; A2 acts on the classification.

### How A4's definitions are consumed by A1/A2/A3 (coherence statement)

- **A1** consumes **"named threat"** — it restates every ratification in terms of the threat it addresses; "named threat" is the vocabulary of that restatement.
- **A2** consumes **"threat-ratified mitigation"** — that definition IS A2's fold-in trigger.
- **A3** consumes **both** — DAEDALUS's map binds a *threat-ratified mitigation* to a *named threat*; ARGUS's design-smell flag fires when a mitigation addresses a named threat but carries no map.
- **A4** (the definitions + ownership + carve-out **confirmation**) is the shared vocabulary the other three operate over; its classification is owned by an UPSTREAM seat (DAEDALUS proposes, ARGUS confirms) so it cannot be self-exempted downstream — **including the carve-out classification itself** (rev2's r3 fix).

So §35's definitions are the single shared vocabulary; A1/A2/A3 are three operations over it, and A4's non-self-exemptable ownership now covers the carve-out path too. This is the directive's coherence requirement, made structural.

---

## §3. Per-discipline edits (exact targets, insertion points, literal text)

### A4 — Definitions + ownership + carve-out (ARGUS-confirmed) → `operating-disciplines.md` new §35

**Target file:** `substrate/operating-disciplines.md`.
**Insertion point:** new top-level section **`## 35. Threat-defeat prevention (named-threat coverage)`**, inserted AFTER `## 34. Trigger-payload authoring rule` (which ends at L1298, followed by the `---` at L1300), and BEFORE `## Agent-regime inverses (the positive framing)` at L1302. So §35 occupies the slot between L1300's `---` and L1302's heading — it is the last NUMBERED `##` section. **No §0.5 relocation-index row** — §35 is born inline (not relocated); the relocation index tracks relocated content only. (Grounded: `grep "^## 3[0-9]\."` shows §30–§34 then `## Agent-regime inverses`; §35 is the next free number, no collision.)

**Literal canon text to add** (faithful spec; ADA may tighten prose but MUST preserve every MUST/definition/owner/carve-out):

```markdown
## 35. Threat-defeat prevention (named-threat coverage)

The gauntlet verifies that built artifacts behave as built. This section adds the
prevention layer that binds a security mitigation to the threat it was created to
defeat, BEFORE build — so a mitigation cannot silently drift to a plausible-but-wrong
surface. The regime verifies **named-threat coverage**, NOT threat-defeat in general:
threat-ENUMERATION completeness (did we name every threat?) remains ARGUS's unmechanized
judgment and a named residual risk (§35.5). Do not overclaim past named-threat coverage.

Empirical anchor: `origindex-trw` shared-auth arc (2026-05-31) — a correctly-named threat
("M2"), ambiguous ratification, a build that picked the easier wrong surface, a design that
never bound mitigation to threat, five verify stages that all asked "does it work?" and none
"does it defeat M2?", caught only at the close-gate. Full case study: `bw show u--ith`
(directive) + `bw show u--tgc` (incident). This section is Arc A (prevention); the detection
backstop is Arc B.

### 35.1 Definitions (the shared vocabulary A1/A2/A3 consume)

- **named threat** — any threat that is EITHER (a) surfaced by ARGUS during design critique,
  OR (b) introduced or ratified at **ANY ratification point** in the arc. A ratification point
  is any moment where a design, a scope item, or a risk set is blessed before or during build —
  the design-critique pause, a PRINCIPAL or floor-manager scope ratification (**including a
  mid-arc scope ratification, outside the design-critique pause**), or a ratification grid.
  This definition is **locus-independent**: coverage does NOT depend on naming one canonical
  gate — it rides on A1's UNCONDITIONAL restatement of EVERY ratification (§35.2), so a threat
  ratified at a moment a reader does not pre-recognize is still swept in. **Gate-origin threats
  are explicitly included** — they are the incident class; omitting them means the fix misses
  the very incident that motivated it. A named threat is assigned a stable ID of the form
  `M<n>` (M1, M2, …) at the moment it is named (ARGUS issues it at critique time; DAEDALUS
  issues it at design time for design-origin threats; whoever introduces a ratified threat at
  any other ratification point issues the next `M<n>`). The ID travels with the threat through
  design, build, and verdict.

- **threat-ratified mitigation** — any change whose stated purpose is to defeat a named
  threat. The classification is PROPOSED by an UPSTREAM OWNER (DAEDALUS at design time, recorded
  in the A3 threat→mitigation map — §35.4) and CONFIRMED by ARGUS at critique time, so it cannot
  be self-exempted downstream. A security-relevant change that carries NO threat classification
  (neither "defeats M<n>" nor an explicit "not threat-ratified" with reason — §35.5) is itself a
  finding.

### 35.2 A1 — Unconditional ratification restatement (the keystone)

Before any build proceeds, the orchestrator (PLINY) MUST restate EVERY ratification as
`threat + attack-path`. This is **UNCONDITIONAL** — there is no "if ambiguous" trigger. A MUST
gated on a soft predicate ("restate when ambiguous") is effectively a MAY: the origindex-trw
phrasing looked unambiguous to the builder, so a judgment-gated restatement would not have
fired. The restatement is cheap and removes the judgment-call escape entirely. A1 fires at a
NAMED gauntlet beat — the pre-ADA ratification-restatement beat (`MAJOR_PLINY.md` §5.13), which
sits between ARGUS's verdict and the ADA dispatch — so the rule has a concrete WHEN a cold
reader can locate, not just an unconditional WHAT.

Mechanically: for each ratified item the orchestrator writes one line on the bw record of the
form `<item> → addresses <named-threat M<n> | none>; attack-path: <how the threat is realized>`.
"none" is a valid restatement (the item is not threat-ratified) — but it must be stated, not
left implicit. A1's output is the input to A2's classification (§35.3). Because A1 restates
EVERY ratification regardless of where it was ratified, named-threat coverage is locus-
independent (§35.1) — it does not depend on identifying one canonical gate.

### 35.3 A2 — Ratified items get a design pass (A1 gates A2)

A1 and A2 are DISTINCT mechanisms with SEPARATE acceptance: A1 is interpretive (disambiguate);
A2 is structural (fold into design). **A1 gates A2.**

Any item that A1's restatement classifies as a **threat-ratified mitigation** MUST be folded
back into the DESIGN — with its `threat → mitigation` map (§35.4) — BEFORE build. It is NOT
acceptable to append it as a build-scope bullet (that was the incident's structural root cause:
the ratified item bypassed design, so no design-time map bound it to the threat). The fold-in
is a design revision: DAEDALUS is re-dispatched, or the design is amended before the ADA
dispatch, so the item enters ADA's build with its map already present.

A2's fold-in trigger is evaluated against A1's restatement output. An un-restated ratified item
is an A1 violation and the build does not proceed — that is the gate: A2 cannot classify what A1
has not restated.

### 35.4 A3 — Threat→mitigation map in the design (ownership)

Any mitigation addressing a named threat MUST carry, in the design artifact, an explicit map:

> `M<n> (named threat) → <attack-path: how the threat is realized> → <how-defeated: the specific
> design mechanism that breaks the attack path>`

DAEDALUS authors this map at design time (`CAPTAIN_DAEDALUS.md` §3, §6.12). ARGUS flags any
mitigation that addresses a named threat but carries no map as a **design smell**
(`CAPTAIN_ARGUS.md` §6.9) — a `load_bearing: true` risk, because an unmapped mitigation is
exactly the drift surface the incident demonstrated. DAEDALUS PROPOSES the classification
(recorded IN the map per §35.1); ARGUS CONFIRMS it at critique time, so it cannot be
self-exempted by a downstream seat.

### 35.5 Honest claim + self-reference carve-out (ARGUS-confirmed)

**Honest claim.** This regime verifies named-threat COVERAGE (every named threat has a mapped
mitigation), not threat-defeat in general. Threat-ENUMERATION completeness — whether the set of
named threats is complete — remains ARGUS's unmechanized judgment and a NAMED RESIDUAL RISK. Do
not represent named-threat coverage as proof that all threats are defeated.

**Self-reference carve-out (load-bearing).** The threat-defeat hardening arcs themselves
(Arc 52 ARC A, ARC B, and any future process-hardening arc of this class) are carved OUT of
"threat-ratified mitigation" when they are process / role-file changes with NO runtime attack
path — there is no threat `M<n>` for a process discipline to defeat, so demanding a
`threat → mitigation` map of them would be a category error (and would make Arc A's own build
recursively demand threat probes of itself). The carve-out is classified
`not threat-ratified (process change, no runtime attack path)` per §35.1.

**The carve-out is NOT self-asserted — ARGUS CONFIRMS it.** The building seat (DAEDALUS at design
time) PROPOSES the `not threat-ratified (process change, no runtime attack path)` classification;
**ARGUS CONFIRMS it at critique time** (ARGUS already owns A4 classification — §35.1; no new seat).
An UNCONFIRMED carve-out, or a carve-out ARGUS judges WRONG (the change does have a runtime attack
path), is a finding ARGUS raises (`load_bearing: true`) — it is the exact self-exemption A4
forbids, applied to the carve-out path. The building seat cannot grant itself the carve-out; only
ARGUS's confirmation makes the classification stand. That ARGUS-confirmed explicit classification
IS the required record; it is not a missing finding.

### 35.6 Per-seat behavior summary (cross-refs)

| Seat | Duty | Cross-ref |
|---|---|---|
| PLINY (orchestrator) | A1: at the pre-ADA ratification-restatement beat, restate every ratification as `threat + attack-path` (unconditional) before the ADA dispatch; gate A2's fold-in on A1's output. | `MAJOR_PLINY.md` §5.13 |
| DAEDALUS (architect) | A3: author the `M<n> → attack-path → how-defeated` map for every threat-ratified mitigation; issue `M<n>` for design-origin threats; PROPOSE the not-threat-ratified / carve-out classification for non-security changes. | `CAPTAIN_DAEDALUS.md` §3, §6.12 |
| ARGUS (plan-critic) | A3: flag a mapless mitigation as a design smell (`load_bearing: true`); issue/confirm `M<n>` for critique-surfaced threats; CONFIRM the carve-out / not-threat-ratified classification — a wrong or unconfirmed claim is a finding. | `CAPTAIN_ARGUS.md` §6.9 |
| ADA (executor) | Builds the mapped mitigation; refuses a threat-ratified item that arrives WITHOUT its A3 map (the fold-in failed upstream). | inherits via universal read |

### 35.7 N=1 provenance + accretion path

Anchor: `u--ith` (threat-defeat directive + full case study) + `u--tgc` (incident capture) +
`origindex-trw` (the arc + floor-manager post-mortem); the-stoa execution home `stoa--yfv`. N=1
(one real incident, right-threat/wrong-surface shape). Per §6.7.1 honest-scope: enters canon on
PRINCIPAL's directive ratification (the Arc 52 restructure-accepted decision, 2026-05-31);
future-evidence accretion against the §6.7.1 gate still required for "structural lesson"
promotion beyond this shape. Adjacent modes NOT covered (named residual): incomplete threat
enumeration (§35.5); mitigation that defeats M<n> but regresses elsewhere; probe
necessary-not-sufficient (Arc B surface). Recover via `bw show u--ith` / `bw show stoa--yfv`.

### 35.8 Cross-references

- §6 (single-checker thinking; redundancy IS the safety property) — the property the incident
  violated (five checkers, only the last asked the threat question).
- §25 (PRINCIPAL-gate discipline) — the universal-locus + per-seat-stub pattern this section
  follows.
- §15 (verification-complexity awareness) — threat-enumeration completeness is a hard-hard
  surface (§35.5 names it as residual rather than mechanizing it).
- `CAPTAIN_DAEDALUS.md` §3 + §6.12 (A3 map authoring); `CAPTAIN_ARGUS.md` §6.9 (design-smell +
  classification + carve-out confirmation); `MAJOR_PLINY.md` §5.13 (A1 restatement beat).
```

---

### A1 — Pre-ADA ratification-restatement beat (double-duty) → `MAJOR_PLINY.md` §5 diagram annotation + new §5.13

**Target file:** `substrate/MAJOR_PLINY.md`.

**Edit 1 — annotate the §5 gauntlet sequence diagram (L130–147)** so the named beat is locatable in the pipeline a cold reader scans first. The shipped diagram (grounded at L130–147) runs DAEDALUS→ARGUS→ADA→VERA→CATO with NO node between ARGUS and ADA. Insert a ratification-restatement gate annotation between the ARGUS block (ends L136) and the ADA block (begins L138):

> Insert between the ARGUS block and the ADA block in the fenced diagram (after the `▼` that currently flows ARGUS→ADA, ~L137):
>
> ```
>    │  ⟶ A1 ratification-restatement beat (§5.13): before dispatching ADA, the
>    │     orchestrator restates EVERY ratification as threat + attack-path
>    │     (unconditional). A threat-ratified item is folded into the DESIGN
>    │     with its threat→mitigation map BEFORE build (A2 gate). op-disc §35.
> ```
>
> (This is a comment-annotation inside the existing fenced block on the ARGUS→ADA edge, NOT a new pipeline stage box — A1 is an orchestrator beat on an existing edge, not a new CAPTAIN seat. It gives r2's "no WHEN" a locatable node.)

**Edit 2 — new stub §5.13 (born inline, double-duty: A1 rule AND named beat).** Insert AFTER §5.12 (Per-CAPTAIN seat-identity, ends with its MODULE-INLINE markers at L228, before the `---` at L230 and `## 6. Communication` at L232). **§5.13 is BORN INLINE (full body)** — it follows the §5.1 precedent, NOT the §5.2–§5.12 relocated pattern. Rationale: A1 is short and load-bearing (the orchestrator must hold it always-loaded; a beat that only loads on-demand would not fire reliably before EVERY build). Born-inline like §5.1 → NO MODULE-INLINE markers, NO `.claude/modules/` body file, NO §4.2 routing-map row, NO relocation-index row (ARGUS verified: §5.1 and §25 are born-inline precedents that carry no such rows).

**Literal text to add:**

```markdown
### 5.13 A1 — Pre-ADA ratification-restatement beat (threat-defeat prevention)
This is a NAMED gauntlet beat with a concrete WHEN: it fires AFTER ARGUS's verdict and
BEFORE the ADA dispatch — the ratification-restatement node annotated on the ARGUS→ADA edge
of the §5 gauntlet diagram. Before ANY build proceeds, restate EVERY ratification as
`threat + attack-path` on the bw record — UNCONDITIONAL, no "if ambiguous" trigger (a MUST
gated on a soft predicate is a MAY). Restate every ratification regardless of WHERE it was
ratified — the design-critique pause, a PRINCIPAL/floor-manager scope ratification (including
mid-arc), or a ratification grid — so coverage is locus-independent (op-disc §35.1). Each
ratified item gets one line: `<item> → addresses <M<n> | none>; attack-path: <…>`. An item A1
classifies as a threat-ratified mitigation gates A2 (fold it into the DESIGN with its
threat→mitigation map before the ADA dispatch, not as a build-scope bullet). Full canon +
definitions: `operating-disciplines.md` §35 (A1 = §35.2; A1-gates-A2 = §35.3; "named threat" /
"threat-ratified mitigation" = §35.1). Anchor: `origindex-trw` / `stoa--yfv`.
```

(§4.2 routing-map row: §5.1 — the born-inline precedent — has NO routing-map row and NO relocation-index row, so §5.13 follows suit and needs neither. The §4.2 routing map keys on a *dispatch beat that loads a module*; §5.13 loads no module, so it has no routing-map entry by construction. ARGUS discharged this in rev1 — §5.1 and §25 confirmed born-inline with no rows.)

---

### A3 (DAEDALUS half) — threat→mitigation map → `CAPTAIN_DAEDALUS.md` §3 + new §6.12 stub

**Target file:** `substrate/CAPTAIN_DAEDALUS.md`.

**Edit 1 — §3 write-to-disk shape (the five design-artifact sections, item 5 ends ~L47).** Insert the following block AFTER §3 item 5 (Out of scope) and BEFORE the "You may also commit breadcrumb comments…" line. **The map template here uses the SAME full annotated form as §35.4 and §6.12 (r5 byte-align fix — rev1's short-form is replaced). The literal text to land is the fenced block below, exactly as written (the `> ` template line is the deployed blockquote, byte-identical to the §35.4 and §6.12 copies):**

```markdown
When the design contains any mitigation that addresses a **named threat** (per
`operating-disciplines.md` §35.1 — ARGUS-surfaced OR ratified at any ratification point,
gate-origin explicitly included), the Approach section MUST carry an explicit
threat→mitigation map (one row per named threat):

> `M<n> (named threat) → <attack-path: how the threat is realized> → <how-defeated: the specific
> design mechanism that breaks the attack path>`

A security-relevant design element with no such map — or no explicit, ARGUS-confirmable
`not threat-ratified (<reason>)` classification — is a design smell ARGUS flags (§35.4). See §6.12.
```

**Edit 2 — new §6 stub §6.12.** Insert AFTER §6.11 (API-docs-examples-don't-generalize, ends L186, before `## 7. Verdict format` at L191). Born INLINE (short discipline, not a relocated module — no §6.0 relocation-index row, no MODULE-INLINE markers). **The map template uses the identical full annotated form (r5 byte-align):**

```markdown
### 6.12 Threat→mitigation map for named-threat mitigations (A3 author duty)
When a design addresses a named threat (`operating-disciplines.md` §35.1: any threat surfaced by
ARGUS OR ratified at any ratification point — gate-origin explicitly included), author an
explicit map in the design's Approach section (one row per named threat):

> `M<n> (named threat) → <attack-path: how the threat is realized> → <how-defeated: the specific
> design mechanism that breaks the attack path>`

You are the UPSTREAM CLASSIFIER who PROPOSES the classification (§35.1): you decide whether a
change is a threat-ratified mitigation and record it IN the map; ARGUS CONFIRMS it at critique
time, so it cannot be self-exempted downstream. Issue the next `M<n>` for design-origin threats;
reuse ARGUS's `M<n>` for critique-surfaced ones. A security-relevant change you judge NOT
threat-ratified gets an explicit `not threat-ratified (<reason>)` line — silence is the finding,
not the safe default. Process / role-file hardening changes (this arc's class) are carved out by
definition (§35.5) — you PROPOSE `not threat-ratified (process change, no runtime attack path)`;
ARGUS CONFIRMS it (you cannot grant yourself the carve-out). Full canon: §35.4 + §35.1 + §35.5.
```

---

### A3 (ARGUS half) + A4 classification + carve-out confirmation → `CAPTAIN_ARGUS.md` new §6.9 stub

**Target file:** `substrate/CAPTAIN_ARGUS.md`.
**Insertion point:** new stub **§6.9 — Threat→mitigation design-smell flag** AFTER §6.8 (Credential discipline, ends L161, before `## 7. Verdict format` at L165). Match the §6.x shape.

**Literal text to add:**

```markdown
### 6.9 Threat→mitigation design-smell flag (named-threat coverage)
When auditing a design that addresses a security threat, apply
`operating-disciplines.md` §35:

1. **Mapless-mitigation = design smell.** A mitigation that addresses a **named threat**
   (§35.1 — any threat surfaced in critique OR ratified at any ratification point) but carries
   NO `M<n> → attack-path → how-defeated` map (§35.4) is a `load_bearing: true` risk —
   `evidence:` cites the design section that mitigates without mapping. This is the exact drift
   surface of the `origindex-trw` incident (right threat, wrong-surface mitigation, no binding
   map).
2. **Classification ownership (A4).** You and DAEDALUS are the UPSTREAM owners: DAEDALUS PROPOSES
   the threat-ratified / not-threat-ratified classification (§35.1); YOU CONFIRM it, so it cannot
   be self-exempted downstream. Issue or confirm the `M<n>` ID for any threat surfaced in critique
   (ARGUS does not yet assign threat IDs — §35 establishes the `M<n>` convention; you are its
   issuer at critique time). A security-relevant change with NO threat classification — neither
   `defeats M<n>` nor an explicit `not threat-ratified (reason)` — is itself a finding
   (`load_bearing: true`).
3. **Confirm the carve-out — do NOT let it be self-asserted.** Process / role-file hardening
   changes are classified `not threat-ratified (process change, no runtime attack path)` (§35.5).
   The building seat PROPOSES this carve-out; YOU CONFIRM it. A carve-out claim you judge WRONG
   (the change DOES have a runtime attack path), or an unconfirmed carve-out, is a finding
   (`load_bearing: true`) — it is the self-exemption A4 forbids, applied to the carve-out path.
   A correctly carved-out, ARGUS-confirmed process change is NOT a mapless-mitigation smell —
   do not flag it as one.

Honest-claim boundary (§35.5): you verify named-threat COVERAGE; threat-ENUMERATION completeness
stays YOUR unmechanized judgment — surface "the threat set may be incomplete" as a hard-hard
risk (§6.6) where warranted, but do not represent coverage as proof of total threat-defeat.
Full canon: §35.4 (map + smell) + §35.1 (definitions + ownership) + §35.5 (carve-out confirmation
+ honest claim).
```

---

## §4. Probes / verification hooks (for VERA / CATO / ZENO)

These are process/role-file edits → coherence + non-regression checks, not runtime probes. All run from the worktree root.

**Presence + content (the four disciplines exist with the locked rev2 properties):**

- **P1 (A4 definition is LOCUS-INDEPENDENT + gate-origin INCLUDED — rev2 r1/r4 fix).** `grep -n "named threat" substrate/operating-disciplines.md` shows the §35.1 definition; the definition text MUST contain ALL of: "surfaced by ARGUS", "**ANY ratification point**", "**locus-independent**", the mid-arc enumeration ("including a mid-arc scope ratification, outside the design-critique pause"), AND "Gate-origin threats are explicitly included". **Negative check (the rev1 defect must be GONE):** `grep -rn "HARD STOP" substrate/` returns ZERO matches (the load-bearing referent is purged). **Probe of the probe (r4):** would a threat ratified by the PRINCIPAL **mid-arc, outside the design-critique pause** classify as a named threat under §35.1? It MUST (it is "any ratification point", and A1's unconditional sweep covers it) — this is the exact case rev1's HARD-STOP binding could miss. If the definition is not locus-independent, FAIL.
- **P2 (A1 is UNCONDITIONAL — no soft predicate; unchanged, ARGUS-verified).** `grep -niE "if ambiguous|when ambiguous|if unclear|when unclear" substrate/MAJOR_PLINY.md substrate/operating-disciplines.md` returns NO match *inside the A1 text* (§5.13, §35.2). Positive: `grep -n "UNCONDITIONAL\|unconditional" substrate/operating-disciplines.md` (§35.2) and `substrate/MAJOR_PLINY.md` (§5.13) both match.
- **P2b (A1 has a NAMED firing BEAT with a locatable WHEN — rev2 r2 fix).** `grep -n "ratification-restatement beat\|before the ADA dispatch\|between ARGUS and ADA\|ARGUS→ADA\|ARGUS's verdict" substrate/MAJOR_PLINY.md` MUST match in BOTH (i) the §5 gauntlet-diagram annotation (the fenced block between the ARGUS and ADA blocks) AND (ii) §5.13. The beat MUST name a concrete WHEN ("after ARGUS's verdict, before the ADA dispatch"). **Probe of the probe:** can a cold reader scanning the §5 pipeline diagram locate WHERE A1 fires? It MUST — the annotation sits on the ARGUS→ADA edge. r2 was "MUST with no canon-anchored beat"; this probe fails if §5.13's WHEN is not also locatable in the §5 sequence.
- **P3 (A1 gates A2, stated; unchanged).** §35.3 contains the gate statement ("A2's fold-in trigger is evaluated against A1's restatement output" / "un-restated ratified item … the build does not proceed"). `grep -n "gates A2\|A1 gates\|un-restated" substrate/operating-disciplines.md`.
- **P4 (A2 = fold into DESIGN, not build-scope bullet; unchanged).** §35.3 contains "folded back into the DESIGN … BEFORE build" AND the negative "NOT acceptable to append it as a build-scope bullet". `grep -n "build-scope bullet" substrate/operating-disciplines.md`.
- **P5 (A3 map template byte-aligned across the 3 inline authoring copies — rev2 r5 fix).** The full annotated map template `M<n> (named threat) → <attack-path: how the threat is realized> → <how-defeated: the specific design mechanism that breaks the attack path>` MUST appear WORD-IDENTICAL in `operating-disciplines.md` §35.4, `CAPTAIN_DAEDALUS.md` §3, AND `CAPTAIN_DAEDALUS.md` §6.12 (the three inline authoring copies — per DAEDALUS §6.8 canonical-template-alignment). **Mechanical check:** extract each copy's template block and confirm the three arrow-chains are byte-identical modulo the surrounding prose. `grep -n "named threat) → <attack-path: how the threat is realized> → <how-defeated:" substrate/operating-disciplines.md substrate/CAPTAIN_DAEDALUS.md` MUST return THREE hits with identical matched text. (rev1's DAEDALUS §3 short-form `M<n> → attack-path → how-defeated` must be GONE.)
- **P6 (A3 ARGUS design-smell flag present + load_bearing; unchanged).** `grep -n "design smell\|mapless\|load_bearing" substrate/CAPTAIN_ARGUS.md` (§6.9) shows the mapless-mitigation→`load_bearing: true` rule.
- **P7 (A4 ownership = upstream PROPOSE + ARGUS CONFIRM, non-self-exemptable).** §35.1 + DAEDALUS §6.12 + ARGUS §6.9 each state DAEDALUS PROPOSES and ARGUS CONFIRMS the classification "so it cannot be self-exempted downstream". `grep -rn "self-exempt\|CONFIRM\|PROPOSE" substrate/operating-disciplines.md substrate/CAPTAIN_DAEDALUS.md substrate/CAPTAIN_ARGUS.md`.
- **P8 (A4 self-reference carve-out is ARGUS-CONFIRMED, not self-asserted — rev2 r3 fix).** §35.5 contains "process change, no runtime attack path" AND "**ARGUS CONFIRMS it**" AND "cannot grant itself the carve-out" / "unconfirmed carve-out … is a finding". ARGUS §6.9 clause 3 contains "building seat PROPOSES … YOU CONFIRM" AND "a carve-out claim you judge WRONG … is a finding". `grep -n "carve\|CONFIRM\|grant itself\|process change, no runtime" substrate/operating-disciplines.md substrate/CAPTAIN_ARGUS.md`. **Probe of the probe (r3):** if a future genuinely-security-relevant arc self-classifies as "process change, no runtime attack path" to escape the map duty, does the canon name WHO catches the wrong claim? It MUST — ARGUS confirms the carve-out, and a wrong claim is an ARGUS finding. If the carve-out is self-assertable with no named cross-check, FAIL. **Also:** would Arc 52 ARC A's OWN build be demanded to carry a threat→mitigation map? It MUST NOT (correctly carved out, ARGUS-confirmed) — the carve-out still prevents the self-reference trap.
- **P9 (honest claim — no overclaim; unchanged).** §35.5 contains "named-threat COVERAGE, NOT threat-defeat in general" AND names threat-enumeration completeness as a residual. `grep -n "named-threat coverage\|enumeration" substrate/operating-disciplines.md`.

**Coherence (mutual cross-refs resolve):**

- **P10.** Every cross-ref resolves: §35's per-seat table cites `MAJOR_PLINY.md §5.13`, `CAPTAIN_DAEDALUS.md §3/§6.12`, `CAPTAIN_ARGUS.md §6.9` — each MUST exist after the edits. Reverse: §5.13, DAEDALUS §6.12, ARGUS §6.9 each cite `operating-disciplines.md §35`. ZENO mechanical: for each `§35`/`§5.13`/`§6.12`/`§6.9` reference, the target heading exists.
- **P11 (§35 numbering).** §35 is the next free op-disc section (§34 is current last). `grep -n "^## 3[4-9]\." substrate/operating-disciplines.md` shows §34 then §35 and no collision.

**Non-regression (substrate machinery still valid):**

- **P12.** `cd app && npm run gen-data` exits clean (substrate frontmatter feeds the Zod schema; these edits touch BODY prose, not frontmatter, so this MUST stay green).
- **P13.** `bash substrate/install.sh --dry-run` (or the repo's smoke-test invocation per op-disc §8.4) deploy-plan check passes — the §35 + stub edits do not break the recompose/MODULE-INLINE machinery (born-inline edits, NO new MODULE-INLINE markers, recompose surface unchanged).
- **P14 (authorship — no author-like field touched).** `git diff` on the four edited files shows NO change to any `author`/`owner`/`creator`/`maintainer`/`by`/`copyright` field. All edits are body prose / new sections. `git diff -- substrate/CAPTAIN_DAEDALUS.md substrate/CAPTAIN_ARGUS.md substrate/MAJOR_PLINY.md substrate/operating-disciplines.md | grep -iE "^[-+].*(author|owner|creator|maintainer|copyright)"` returns no `+`/`-` author-field lines. `author:` stays Denson Smith (immutable).

---

## §5. Self-assessed weak points (where ARGUS-rev2 should scrutinize hardest)

- **W1 (load-bearing — scrutinize FIRST). The §35.1(b) enumeration is illustrative-and-inclusive, not exhaustive — its load-bearing word is "ANY ratification point."** rev2's fix for r1/r4 deliberately does NOT name one canonical gate; it relies on A1's unconditional sweep plus an open-ended "any ratification point" definition with an example list. The risk inverse of rev1's: rev1 was too NARROW (one undefined locus); rev2 could be read as too VAGUE ("what counts as a ratification point?"). *Why this shape anyway:* the floor-manager LOCKED "bind to the existing pre-build ratification moment; no formal gate object," and a closed enumeration would re-introduce exactly r4's failure mode (a real ratification moment the list forgot falls outside coverage). The open "any ratification point" + A1's unconditional sweep is what makes coverage locus-independent. The enumeration names the three real ones (design-critique pause; mid-arc PRINCIPAL/floor-manager scope ratification; ratification grid) to anchor the reader without closing the set. ARGUS should confirm the open framing reads as inclusive (a reader adds a new ratification moment to the swept set) rather than vague (a reader cannot tell whether their moment counts).
- **W2 (load-bearing — A1's firing beat is an annotation on an existing edge, not a new pipeline stage box).** The (b) fix homes the named beat on the ARGUS→ADA edge of the §5 diagram as a comment-annotation + §5.13 stub, NOT a new boxed CAPTAIN stage. *Why this shape anyway:* A1 is an ORCHESTRATOR beat (PLINY restates), not a new seat — adding a stage box would imply a new dispatched CAPTAIN, which is false and would bloat the gauntlet. The floor-manager OK'd a §5 surface expansion, not a new pipeline seat. The residual ARGUS should check: is an edge-annotation a strong enough WHEN to close r2, or does a cold reader still skim past it? P2b makes "locatable in the §5 sequence" the explicit acceptance criterion; I judge the annotation + §5.13's "after ARGUS's verdict, before the ADA dispatch" sufficient, but ARGUS owns the cold-reader test.
- **W3 (load-bearing — the carve-out confirmation adds an ARGUS duty that fires on EVERY process-hardening arc, including recursively on THIS one).** rev2's r3 fix makes ARGUS confirm the carve-out. That means Arc 52 ARC A's own build, when ARGUS-rev2 audits it, should see DAEDALUS PROPOSE `not threat-ratified (process change, no runtime attack path)` and ARGUS CONFIRM it. *Why this shape anyway:* that recursion is correct and desired — it is the system eating its own dogfood, and it is exactly what closes the self-exemption hole (the building seat cannot grant itself the carve-out). The residual: this design (design-rev2.md) IS a process-hardening artifact, so per its own §35.5 it should carry the proposed carve-out classification. **It does:** this whole arc is `not threat-ratified (process change, no runtime attack path)` — ARGUS-rev2 is invited to CONFIRM that classification as the first live exercise of the rule it ratifies. If ARGUS judges any part of these edits to have a runtime attack path, that is a finding by the rule itself.
- **W4 (bounded — byte-alignment is hand-verified within this design; the cross-FILE check is P5's at build time).** Per my own §6.8, two-or-more inline copies of a canonical template must be byte-aligned. The three authoring copies of the full map template (§35.4, DAEDALUS §3, DAEDALUS §6.12) are written word-identical in THIS design. §6.8 scopes the mechanical `diff` check to WITHIN-design copies; these three live in three different TARGET files (cross-file), which §6.8 explicitly hands to the substrate's single-source + cite-at-read-site discipline. *Why this shape anyway:* each seat's stub genuinely needs the template inline (a reader of ARGUS's §6.9 should not chase to op-disc for the shape). I aligned the three by hand and made word-identity P5's explicit build-time check. ARGUS should eyeball the three arrow-chains for the drift r5 caught in rev1 (rev1's DAEDALUS §3 short-form is the specific thing that must be gone).
- **W5 (bounded — line numbers are recon-current but approximate; insertion is neighbor-anchored).** Cited line numbers (op-disc §34 ends L1298 / `---` L1300 / Agent-regime-inverses L1302; PLINY §5.12 ends L228, §6 L232, diagram L130–147; DAEDALUS §6.11 L186, §7 L191; ARGUS §6.8 L161, §7 L165) are grounded against the shipped files in THIS session, but insertion points are specified by NEIGHBOR SECTION, not absolute line — so a line drift from an earlier landed edit does not misplace the edit. *Why this shape anyway:* neighbor-section anchoring is the robust spec; P10/P11 catch any dangling cross-ref at build time.

---

## §6. Out of scope (Arc B / deferred — one line each)

- **Detection mechanisms** (`u--ith` #4 threat-anchored probes, #5 verdict threat-coverage assertion, #6 close-gate re-derivation, #7 culture) — Arc B; locked decision #1 (prevention before detection).
- **Verdict-template / Zod-schema edits** to carry the threat-coverage assertion — that is B2 (#5), anchored to B1's executed probe; A3's map lives in the design body + role-file prose, not a verdict template this arc.
- **Threat-ENUMERATION completeness mechanization** — named as ARGUS's residual unmechanized judgment (§35.5); honest-claim locked decision #3 forbids overclaiming it.
- **A formal "security gate" object** — REJECTED for this arc by the floor-manager (directive §6 defers it to a separate design); rev2 binds to the existing set of ratification points via A1's unconditional sweep, NOT to a new gate object. (This is the rev2 replacement for rev1's HARD-STOP mapping.)
- **origindex-trw retro-fix** — the incident arc itself is not re-opened; Arc A hardens the process so the next one cannot drift the same way.

---

*Authored for the PRINCIPAL (Denson Smith). No author-like field is touched by these edits. This design is itself classified `not threat-ratified (process change, no runtime attack path)` per §35.5 — ARGUS-rev2 is invited to confirm that classification.*
