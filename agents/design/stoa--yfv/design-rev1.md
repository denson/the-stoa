# Arc 52 ARC A — Threat-defeat prevention layer (design-rev1)

**Ticket:** `stoa--yfv` (Arc A, prevention). **Seat:** CAPTAIN_DAEDALUS (architect).
**Directive:** `substrate/arcs/arc-52-threat-defeat-prevention-directive.md` (authoritative scope).
**Worktree:** `.claude/worktrees/arc-52-build/`; source canon edited is `substrate/` (re-deploys via `install.sh`).

---

## §1. Problem restatement

A real arc (`origindex-trw` shared-auth, 2026-05-31) drifted: ARGUS named a security threat correctly ("M2"), but the ratification phrasing was ambiguous, so the build picked a plausible-but-wrong surface; the design never bound the mitigation to the threat; five verification stages passed it (all asked "does it work?", none asked "does it defeat M2?"). The external review established the **root cause is upstream direction-binding, not verification** — a correctly disambiguated, design-bound mitigation never drifts. Arc A builds the prevention layer (four disciplines A1–A4); Arc B (detection) is OUT of scope and dispatched later.

**Imported assumptions I am naming (per §6.1):**

1. **"Security gate / ratification grid" has no existing substrate home.** The directive's A1/A2 language ("items added at the security gate / ratification grid") describes the origindex-trw incident's mechanics, but the-stoa substrate has no formal "security gate" object. Recon (Grep across `substrate/`) confirms: "ratification" in this substrate means *PRINCIPAL ratifying a phase transition or a directive's scope* (op-disc §25.3, §10, the HITL phase-ratification flow at PLINY §5.1), and the closest structural analog is the post-ARGUS **HARD STOP** (the floor-manager surface where the design + its risk set are ratified before ADA builds). My design therefore maps "security gate / ratification grid" onto **two concrete substrate moments**: (a) ARGUS's risk surfacing during design critique, and (b) any threat introduced or ratified at the HARD STOP / phase-ratification surface. A1's "restate every ratification" binds to the orchestrator's ratification-relay moment (PLINY §5). This is the load-bearing interpretation ARGUS should scrutinize first (§5 weak point W1).
2. **ARGUS does not yet assign threat IDs.** The incident's "M2" is origindex-trw-local, not a substrate convention. Recon confirms `CAPTAIN_ARGUS.md` has zero matches for `threat`/`M`/`attack`. Per the directive's NIT-2 check, A4 therefore *establishes* the `M<n>` named-threat-ID convention (it does not "reuse" an existing one) and assigns its issuance to ARGUS at critique time + DAEDALUS at design time.
3. **The four disciplines are a cluster, not four scattered edits.** A4's definitions are CONSUMED by A1/A2/A3, so the definitions must live in ONE universal locus both seats and the orchestrator read. The §25 PRINCIPAL-gate discipline is the precedent: a universal `operating-disciplines.md` section + thin per-seat stubs. I follow it exactly.

This restatement converges with the directive; the imported assumptions above are scope the directive left implicit (the "security gate" mapping), surfaced rather than smoothed.

---

## §2. Approach — the four disciplines and their homes

### Structural decision (load-bearing)

A4's definitions are consumed by A1, A2, and A3. Therefore the **definitions + the orchestration mechanics (A1, A2) + the ownership assignment (A4) live in ONE new universal section** at `operating-disciplines.md` **§35** (next free number; §34 is the last). The two CAPTAIN seats carry **thin stubs** that point at §35 for definitions and add only their seat-specific duty:

- DAEDALUS: A3 map-authoring (the `threat → attack-path → how-defeated` map) — folded into the §3 write-to-disk shape + a new §6 stub.
- ARGUS: A3 design-smell flag (mapless mitigation) + A4 classification ownership (issue/confirm the `M<n>` ID) — a new §6 stub.

This mirrors §25 (PRINCIPAL-gate): universal locus + per-seat behavior table + per-seat envelope stubs. It satisfies the directive's coherence requirement ("A4's definitions are USED by A1/A2/A3") structurally — there is exactly one definition home, and every consumer cross-references it.

### How A1 gates A2 (kept distinct per locked decision #4)

A1 and A2 are **different mechanisms with separate acceptance**, sequenced A1→A2:

- **A1 (interpretive — disambiguate).** Before any build, the orchestrator restates EVERY ratification as `threat + attack-path`. This is unconditional: it produces a disambiguated statement of *what threat the ratified item addresses and by what attack path*. Output: a one-line-per-item `threat + attack-path` restatement on the bw record.
- **A2 (structural — fold into design).** Any item that A1's restatement reveals to be a **threat-ratified mitigation** (i.e., its restated purpose is to defeat a named threat) MUST be folded back into the DESIGN with its `threat → mitigation` map BEFORE build — not appended as a build-scope bullet. Output: a design revision (DAEDALUS re-dispatched, or the design amended at the HARD STOP) carrying the A3 map for that item.

**The gate:** A2 cannot fire correctly without A1's output, because A1's restatement is what *classifies* an item as a threat-ratified mitigation (the trigger for A2's fold-in). A1 is the classification step; A2 is the action the classification triggers. An item that skips A1 (no `threat + attack-path` restatement) cannot be assessed for A2 — so A1 is a hard precondition. §35 states this as: "A2's fold-in trigger is evaluated against A1's restatement output; an un-restated ratified item is itself an A1 violation (the build does not proceed)."

### How A4's definitions are consumed by A1/A2/A3

- **A1** consumes "named threat" — it restates every ratification in terms of the threat it addresses; "named threat" is the vocabulary of that restatement.
- **A2** consumes "threat-ratified mitigation" — that definition IS A2's fold-in trigger (only threat-ratified mitigations must be folded into the design).
- **A3** consumes both — DAEDALUS's map binds a *mitigation* (threat-ratified) to a *named threat*; ARGUS's design-smell flag fires when a mitigation addresses a named threat but carries no map.

So §35's definitions are the single shared vocabulary; A1/A2/A3 are three operations over it. This is the directive's coherence requirement, made structural.

---

## §3. Per-discipline edits (exact targets, insertion points, literal text)

### A4 — Definitions + ownership + self-reference carve-out  → `operating-disciplines.md` new §35

**Target file:** `substrate/operating-disciplines.md`.
**Insertion point:** new top-level section **`## 35. Threat-defeat prevention (named-threat coverage)`**, inserted AFTER `## 34. Trigger-payload authoring rule` (ends ~line 1298, before the `---` and `## Agent-regime inverses` closing block at line ~1300). New section goes between line 1299's `---` and the `## Agent-regime inverses` heading — i.e., as the last numbered `##` section, immediately before the closing `Agent-regime inverses` / `Empirical lineage` blocks. **Add the §35 row to the §0.5 relocation index?** NO — §35 is born inline (not relocated); §0.5 only tracks relocated content. (If a future debloat arc relocates §35's detail, that arc adds the row.)

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
  OR (b) introduced or ratified at the security gate (the HARD STOP / phase-ratification
  surface where a design and its risk set are ratified before build). **Gate-origin threats
  are explicitly included** — they are the incident class; omitting them means the fix misses
  the very incident that motivated it. A named threat is assigned a stable ID of the form
  `M<n>` (M1, M2, …) at the moment it is named (ARGUS issues it at critique time; DAEDALUS
  issues it at design time for design-origin threats; whoever introduces a gate-origin threat
  issues the next `M<n>`). The ID travels with the threat through design, build, and verdict.

- **threat-ratified mitigation** — any change whose stated purpose is to defeat a named
  threat. The classification is made by an UPSTREAM OWNER (DAEDALUS or ARGUS, at design time,
  recorded in the A3 threat→mitigation map — §35.4) so it cannot be self-exempted downstream.
  A security-relevant change that carries NO threat classification (neither "defeats M<n>" nor
  an explicit "not threat-ratified" with reason) is itself a finding.

### 35.2 A1 — Unconditional ratification restatement (the keystone)

Before any build proceeds, the orchestrator (PLINY) MUST restate EVERY ratification as
`threat + attack-path`. This is **UNCONDITIONAL** — there is no "if ambiguous" trigger. A MUST
gated on a soft predicate ("restate when ambiguous") is effectively a MAY: the origindex-trw
phrasing looked unambiguous to the builder, so a judgment-gated restatement would not have
fired. The restatement is cheap and removes the judgment-call escape entirely.

Mechanically: for each ratified item the orchestrator writes one line on the bw record of the
form `<item> → addresses <named-threat M<n> | none>; attack-path: <how the threat is realized>`.
"none" is a valid restatement (the item is not threat-ratified) — but it must be stated, not
left implicit. A1's output is the input to A2's classification (§35.3).

### 35.3 A2 — Gate-ratified items get a design pass (A1 gates A2)

A1 and A2 are DISTINCT mechanisms with SEPARATE acceptance: A1 is interpretive (disambiguate);
A2 is structural (fold into design). **A1 gates A2.**

Any item that A1's restatement classifies as a **threat-ratified mitigation** MUST be folded
back into the DESIGN — with its `threat → mitigation` map (§35.4) — BEFORE build. It is NOT
acceptable to append it as a build-scope bullet (that was the incident's structural root cause:
the gate-added item bypassed design, so no design-time map bound it to the threat). The fold-in
is a design revision: DAEDALUS is re-dispatched, or the design is amended at the HARD STOP, so
the item enters ADA's build with its map already present.

A2's fold-in trigger is evaluated against A1's restatement output. An un-restated ratified item
is an A1 violation and the build does not proceed — that is the gate: A2 cannot classify what A1
has not restated.

### 35.4 A3 — Threat→mitigation map in the design (ownership)

Any mitigation addressing a named threat MUST carry, in the design artifact, an explicit map:

> `M<n> (named threat) → <attack-path: how the threat is realized> → <how-defeated: the specific
> design mechanism that breaks the attack path>`

DAEDALUS authors this map at design time (`CAPTAIN_DAEDALUS.md` §3, §6.x). ARGUS flags any
mitigation that addresses a named threat but carries no map as a **design smell**
(`CAPTAIN_ARGUS.md` §6.x) — a `load_bearing: true` risk, because an unmapped mitigation is
exactly the drift surface the incident demonstrated. The map's owner (DAEDALUS/ARGUS) is the
upstream classifier from §35.1; the classification is recorded IN the map, so it cannot be
self-exempted by a downstream seat.

### 35.5 Honest claim + self-reference carve-out

**Honest claim.** This regime verifies named-threat COVERAGE (every named threat has a mapped
mitigation), not threat-defeat in general. Threat-ENUMERATION completeness — whether the set of
named threats is complete — remains ARGUS's unmechanized judgment and a NAMED RESIDUAL RISK. Do
not represent named-threat coverage as proof that all threats are defeated.

**Self-reference carve-out (load-bearing).** The threat-defeat hardening arcs themselves
(Arc 52 ARC A, ARC B, and any future process-hardening arc of this class) are **carved OUT of
"threat-ratified mitigation" by definition.** They are process / role-file changes with NO
runtime attack path — there is no threat `M<n>` for a process discipline to defeat, so demanding
a `threat → mitigation` map of them would be a category error (and would make Arc A's own build
recursively demand threat probes of itself). A process-hardening change is classified
`not threat-ratified (process change, no runtime attack path)` per §35.1 — that explicit
classification IS the required record; it is not a missing finding.

### 35.6 Per-seat behavior summary (cross-refs)

| Seat | Duty | Cross-ref |
|---|---|---|
| PLINY (orchestrator) | A1: restate every ratification as `threat + attack-path` (unconditional) before build; gate A2's fold-in on A1's output. | `MAJOR_PLINY.md` §5.x |
| DAEDALUS (architect) | A3: author the `M<n> → attack-path → how-defeated` map for every threat-ratified mitigation; issue `M<n>` for design-origin threats; record the not-threat-ratified classification for non-security changes. | `CAPTAIN_DAEDALUS.md` §3, §6.x |
| ARGUS (plan-critic) | A3: flag a mapless mitigation as a design smell (`load_bearing: true`); issue/confirm `M<n>` for critique-surfaced threats; a security-relevant change with no threat classification is a finding. | `CAPTAIN_ARGUS.md` §6.x |
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
- `CAPTAIN_DAEDALUS.md` §3 + §6.x (A3 map authoring); `CAPTAIN_ARGUS.md` §6.x (design-smell +
  classification); `MAJOR_PLINY.md` §5.x (A1 restatement).
```

---

### A1 — Unconditional ratification restatement  → `MAJOR_PLINY.md` new §5.x stub

**Target file:** `substrate/MAJOR_PLINY.md`.
**Insertion point:** §5 (the gauntlet pipeline) carries §5.1 (an INLINE full-body short stub — operating-mode awareness) followed by §5.2–§5.12 (CONDITIONAL module-relocated beat-stubs, each with a §4.2 routing-map row + relocation-index row + MODULE-INLINE markers). Insert a new stub **§5.13 — A1: unconditional ratification restatement** AFTER §5.12 (Per-CAPTAIN seat-identity, ends ~line 228 incl. its MODULE-INLINE markers, before the `---` at line 230 and `## 6. Communication` at line 232). **§5.13 is BORN INLINE (full body, not module-relocated) — it follows the §5.1 precedent, NOT the §5.2–§5.12 relocated pattern.** Rationale: A1 is short and load-bearing (the orchestrator must hold it always-loaded, not load-on-demand — a ratification-restatement rule that only loads at a specific beat would not fire reliably before EVERY build). Because it is born-inline like §5.1, it gets NO MODULE-INLINE markers, NO `.claude/modules/` body file, and NO relocation-index row (the §4.2 relocation index tracks relocated content only; §5.1 has no row there). See W3 for the one routing-map question to confirm at build time.

**Literal text to add:**

```markdown
### 5.13 A1 — Unconditional ratification restatement (threat-defeat prevention)
Before ANY build proceeds, restate EVERY ratification as `threat + attack-path` on the bw
record — UNCONDITIONAL, no "if ambiguous" trigger (a MUST gated on a soft predicate is a MAY).
Each ratified item gets one line: `<item> → addresses <M<n> | none>; attack-path: <…>`. An item
A1 classifies as a threat-ratified mitigation gates A2 (fold it into the DESIGN with its
threat→mitigation map before build, not as a build-scope bullet). Full canon + definitions:
`operating-disciplines.md` §35 (A1 = §35.2; A1-gates-A2 = §35.3; "named threat" /
"threat-ratified mitigation" = §35.1). Anchor: `origindex-trw` / `stoa--yfv`.
```

(§4.2 routing-map row: §5.1 — the born-inline precedent — has NO routing-map row and NO relocation-index row, so §5.13 follows suit and needs neither. The §4.2 routing map keys on a *dispatch beat that loads a module*; §5.13 loads no module, so it has no routing-map entry by construction. Confirmed against the actual §4.2 table (lines 84–121): the table enumerates only the relocated §5.2–§5.12 stubs, not §5.1. See W3.)

---

### A3 (DAEDALUS half) — threat→mitigation map  → `CAPTAIN_DAEDALUS.md` §3 + new §6.x stub

**Target file:** `substrate/CAPTAIN_DAEDALUS.md`.
**Edit 1 — §3 write-to-disk shape (line ~51–55).** §3 enumerates the five design-artifact sections (1 Problem restatement … 5 Out of scope). Add a sentence to item **2 (Approach)** OR a new bullet making the threat→mitigation map a required design element when the design contains a security mitigation. Minimal, surgical edit — append to the §3 list intro or to item 2:

> Insert after §3 item 5 (before the line "You may also commit breadcrumb comments…", ~line 57):
>
> ```markdown
> When the design contains any mitigation that addresses a **named threat** (per
> `operating-disciplines.md` §35.1 — ARGUS-surfaced OR gate-introduced), the Approach section
> MUST carry an explicit threat→mitigation map: `M<n> → <attack-path> → <how-defeated>` (one row
> per named threat). A security-relevant design element with no such map — or no explicit
> "not threat-ratified (reason)" classification — is a design smell ARGUS flags (§35.4). See §6.12.
> ```

**Edit 2 — new §6 stub §6.12.** Insert AFTER §6.11 (API-docs-don't-generalize, ends ~line 189, before `## 7. Verdict format` at line 191). Match the §6.x stub shape. This one is born INLINE (a short discipline, not a relocated module — no §6.0 relocation-index row, no MODULE-INLINE markers):

```markdown
### 6.12 Threat→mitigation map for named-threat mitigations (A3 author duty)
When a design addresses a named threat (`operating-disciplines.md` §35.1: any threat surfaced by
ARGUS OR introduced/ratified at the security gate — gate-origin EXPLICITLY included), author an
explicit map in the design's Approach section:

> `M<n> (named threat) → <attack-path: how the threat is realized> → <how-defeated: the specific
> design mechanism that breaks that attack path>`

You are the UPSTREAM CLASSIFIER (§35.1): you decide whether a change is a threat-ratified
mitigation and record it IN the map, so it cannot be self-exempted downstream. Issue the next
`M<n>` for design-origin threats; reuse ARGUS's `M<n>` for critique-surfaced ones. A
security-relevant change you judge NOT threat-ratified gets an explicit
`not threat-ratified (<reason>)` line — silence is the finding, not the safe default. Process /
role-file hardening changes (this arc's class) are carved out by definition (§35.5) — classify
them `not threat-ratified (process change, no runtime attack path)`. Full canon: §35.4 + §35.1.
```

---

### A3 (ARGUS half) + A4 classification  → `CAPTAIN_ARGUS.md` new §6.x stub

**Target file:** `substrate/CAPTAIN_ARGUS.md`.
**Insertion point:** insert a new stub **§6.9 — Threat→mitigation design-smell flag** AFTER §6.8 (Credential discipline, ends ~line 161, before `---` and `## 7. Verdict format` at line 165). Match the §6.x shape.

**Literal text to add:**

```markdown
### 6.9 Threat→mitigation design-smell flag (named-threat coverage)
When auditing a design that addresses a security threat, apply
`operating-disciplines.md` §35:

1. **Mapless-mitigation = design smell.** A mitigation that addresses a **named threat**
   (§35.1) but carries NO `M<n> → attack-path → how-defeated` map (§35.4) is a
   `load_bearing: true` risk — `evidence:` cites the design section that mitigates without
   mapping. This is the exact drift surface of the `origindex-trw` incident (right threat,
   wrong-surface mitigation, no binding map).
2. **Classification ownership (A4).** You and DAEDALUS are the UPSTREAM owners who classify a
   change as threat-ratified (§35.1), so it cannot be self-exempted downstream. Issue or confirm
   the `M<n>` ID for any threat you surface in critique (ARGUS does not yet assign threat IDs —
   §35 establishes the `M<n>` convention; you are its issuer at critique time). A
   security-relevant change with NO threat classification — neither `defeats M<n>` nor an
   explicit `not threat-ratified (reason)` — is itself a finding (`load_bearing: true`).
3. **Carve-out is not a gap.** Process / role-file hardening changes are classified
   `not threat-ratified (process change, no runtime attack path)` by definition (§35.5); that
   explicit classification is the required record, NOT a mapless-mitigation finding. Do not flag
   a correctly carved-out process change as a smell.

Honest-claim boundary (§35.5): you verify named-threat COVERAGE; threat-ENUMERATION completeness
stays YOUR unmechanized judgment — surface "the threat set may be incomplete" as a hard-hard
risk (§6.6) where warranted, but do not represent coverage as proof of total threat-defeat.
Full canon: §35.4 (map + smell) + §35.1 (definitions + ownership) + §35.5 (carve-out + honest claim).
```

---

## §4. Probes / verification hooks (for VERA / CATO / ZENO)

These are process/role-file edits → coherence + non-regression checks, not runtime probes. All run from the worktree root.

**Presence + content (the four disciplines exist with the locked properties):**

- **P1 (A4 definitions present, gate-origin INCLUDED).** `grep -n "named threat" substrate/operating-disciplines.md` shows the §35.1 definition; the definition text must contain BOTH "surfaced by ARGUS" AND "introduced or ratified at the security gate" AND "Gate-origin threats are explicitly included". The gate-origin clause is the incident class — its presence is the load-bearing acceptance criterion. **Probe of the probe:** would origindex-trw's gate-added "M2" item classify as a named threat under §35.1? It MUST (it is gate-origin). If the definition omits gate-origin, the fix misses the very incident that motivated it → FAIL.
- **P2 (A1 is UNCONDITIONAL — no soft predicate).** `grep -niE "if ambiguous|when ambiguous|if unclear|when unclear" substrate/MAJOR_PLINY.md substrate/operating-disciplines.md` returns NO match *inside the A1 text* (§5.13, §35.2). Positive check: `grep -n "UNCONDITIONAL\|unconditional" substrate/operating-disciplines.md` (§35.2) and `substrate/MAJOR_PLINY.md` (§5.13) both match. A1 gated on a soft predicate is the defect this arc exists to prevent → its absence is a hard acceptance criterion.
- **P3 (A1 gates A2, stated).** §35.3 contains the literal gate statement ("A2's fold-in trigger is evaluated against A1's restatement output" / "an un-restated ratified item … the build does not proceed"). `grep -n "gates A2\|A1 gates\|un-restated" substrate/operating-disciplines.md`.
- **P4 (A2 = fold into DESIGN, not build-scope bullet).** §35.3 contains "folded back into the DESIGN … BEFORE build" AND the negative "NOT acceptable to append it as a build-scope bullet". `grep -n "build-scope bullet" substrate/operating-disciplines.md`.
- **P5 (A3 map shape present in BOTH seat files + op-disc, byte-aligned).** The `M<n> → attack-path → how-defeated` map template appears in `operating-disciplines.md` §35.4, `CAPTAIN_DAEDALUS.md` §6.12, `CAPTAIN_ARGUS.md` §6.9 (referenced), and `CAPTAIN_DAEDALUS.md` §3. CATO/ZENO check the three authoring copies (op-disc §35.4, DAEDALUS §3, DAEDALUS §6.12) state the SAME three-part shape (`threat → attack-path → how-defeated`) — no drift in the arrow-chain wording (per DAEDALUS §6.8 canonical-template-alignment; this design carries the map template in 3 inline copies — see W2).
- **P6 (A3 ARGUS design-smell flag present + load_bearing).** `grep -n "design smell\|mapless\|load_bearing" substrate/CAPTAIN_ARGUS.md` (§6.9) shows the mapless-mitigation→`load_bearing: true` rule.
- **P7 (A4 ownership = upstream, non-self-exemptable).** §35.1 + DAEDALUS §6.12 + ARGUS §6.9 each state the classifier is DAEDALUS/ARGUS at design time, recorded in the map "so it cannot be self-exempted downstream". `grep -rn "self-exempt" substrate/operating-disciplines.md substrate/CAPTAIN_DAEDALUS.md substrate/CAPTAIN_ARGUS.md`.
- **P8 (A4 self-reference carve-out present).** §35.5 contains "carved OUT of \"threat-ratified mitigation\" by definition" AND "process change, no runtime attack path". `grep -n "carve\|carved OUT\|no runtime attack path" substrate/operating-disciplines.md`. **Probe of the probe:** would Arc 52 ARC A's OWN build be demanded to carry a threat→mitigation map under this canon? It MUST NOT (it is process hardening) → the carve-out's presence is the acceptance criterion that prevents the self-reference trap.
- **P9 (honest claim — no overclaim).** §35.5 contains "named-threat COVERAGE, NOT threat-defeat in general" AND names threat-enumeration completeness as a residual. ARGUS §6.9 + op-disc §35.5 agree. `grep -n "named-threat coverage\|enumeration" substrate/operating-disciplines.md`.

**Coherence (mutual cross-refs resolve):**

- **P10.** Every cross-ref resolves to a real section: §35's per-seat table cites `MAJOR_PLINY.md §5.13`, `CAPTAIN_DAEDALUS.md §3/§6.12`, `CAPTAIN_ARGUS.md §6.9` — each MUST exist after the edits. Reverse: §5.13, DAEDALUS §6.12, ARGUS §6.9 each cite `operating-disciplines.md §35`. ZENO mechanical: for each `§35`/`§5.13`/`§6.12`/`§6.9` reference, the target heading exists.
- **P11 (§35 numbering).** §35 is the next free op-disc section (§34 is current last). `grep -n "^## 3[4-9]\." substrate/operating-disciplines.md` shows §34 then §35 and no collision.

**Non-regression (substrate machinery still valid):**

- **P12.** `cd app && npm run gen-data` exits clean (project CLAUDE.md — substrate frontmatter feeds the Zod schema; these edits touch BODY prose, not frontmatter, so this MUST stay green).
- **P13.** `bash substrate/install.sh --dry-run` (or the repo's smoke-test invocation per op-disc §8.4) deploy-plan check passes — the §35 + stub edits do not break the recompose/MODULE-INLINE machinery (these are born-inline edits with NO new MODULE-INLINE markers, so the recompose surface is unchanged).
- **P14 (authorship — no author-like field touched).** `git diff` on the four edited files shows NO change to any `author`/`owner`/`creator`/`maintainer`/`by`/`copyright` field. All edits are body prose / new sections; no frontmatter author line is in scope. `git diff -- substrate/CAPTAIN_DAEDALUS.md substrate/CAPTAIN_ARGUS.md substrate/MAJOR_PLINY.md substrate/operating-disciplines.md | grep -iE "^[-+].*(author|owner|creator|maintainer|copyright)"` returns no `+`/`-` author-field lines. `author:` stays Denson Smith (immutable, CLAUDE.md authorship rule).

---

## §5. Self-assessed weak points (where ARGUS should scrutinize hardest)

- **W1 (load-bearing — scrutinize FIRST). The "security gate / ratification grid" mapping is my interpretation, not a pre-existing substrate object.** Recon confirmed the substrate has no formal "security gate"; I mapped it onto (a) ARGUS critique-surfacing and (b) the HARD STOP / phase-ratification surface, and bound A1 to PLINY's ratification-relay moment (§5). If POLYBIUS/PRINCIPAL intended a *different* concrete locus for "the security gate" (e.g., a new formal gate object, or CATO's security-review pass), §35.1's gate-origin clause and §5.13's A1 insertion point both move. *Why this shape anyway:* the HARD STOP is the only substrate moment where a design + its ratified risk set are blessed before build — it is the structurally correct binding point, and tying A1 to PLINY's ratification relay is where "restate every ratification" can actually fire. I named the mapping explicitly (§1) so ARGUS audits the binding rather than inheriting it silently.
- **W2 (load-bearing — canonical-template-alignment, my own §6.8). The A3 `threat → attack-path → how-defeated` map template appears in three inline authoring copies in this design (op-disc §35.4, DAEDALUS §3, DAEDALUS §6.12) and is referenced in two more.** Per my own §6.8 discipline, two-or-more inline copies of a canonical template MUST be byte-aligned modulo named slots. I have kept the arrow-chain wording identical across copies, but I did NOT run the `diff <(sed …) <(sed …)` mechanical check because the copies live in three different target FILES (cross-file, which §6.8 explicitly scopes OUT — it covers within-design copies). The within-DESIGN copies (this design-rev1.md states the template ~3 times) I aligned by hand. *Why this shape anyway:* the template genuinely needs to appear in each seat's stub (a reader of ARGUS's stub should not have to chase to op-disc for the shape). ARGUS should confirm the three arrow-chains are word-identical, and P5 makes it a CATO/ZENO check at build time.
- **W3 (non-load-bearing; confirmed against the actual tables). The "no new index row needed" claims rest on §5.13/§35/§6.12/§6.9 being BORN INLINE (not relocated modules).** I read the actual MAJOR_PLINY.md §4.2 routing map + relocation index (lines 84–121): §5.1 (the born-inline precedent) appears in NEITHER table, so §5.13 correctly needs no row in either. Likewise op-disc §0.5 and DAEDALUS §6.0 track *relocated* content only, so born-inline §35 / §6.12 get no row. *Why this shape anyway:* §25 (PRINCIPAL-gate) and §5.1 are both born-inline precedents that carry no index row — this design matches them. The only residual: ADA should re-confirm at build time that no MAJOR_PLINY §4.2 / op-disc §0.5 / DAEDALUS §6.0 / ARGUS table enumerates these new sections (P10/P11 catch any dangling cross-ref). I confirmed the tables rather than asserting from memory.
- **W4 (bounded). I did not run the probes; they are specified, not executed.** Per the DAEDALUS seat (designs, does not build/verify), P1–P14 are VERA/CATO/ZENO's to execute. The line numbers I cite ("~line 1298", "~line 230") are recon-current but approximate; ADA grounds against actual headings at build time (the insertion points are specified by NEIGHBOR SECTION, not absolute line, precisely so a line-number drift does not misplace the edit). *Why this shape anyway:* neighbor-section anchoring is the robust insertion spec; absolute line numbers would rot the moment any earlier edit lands.

---

## §6. Out of scope (Arc B / deferred — one line each)

- **Detection mechanisms** (`u--ith` #4 threat-anchored probes, #5 verdict threat-coverage assertion, #6 close-gate re-derivation, #7 culture) — Arc B; locked decision #1 (prevention before detection).
- **Verdict-template / Zod-schema edits** to carry the threat-coverage assertion — that is B2 (#5), anchored to B1's executed probe; A3's map lives in the design body + role-file prose, not in a verdict template this arc.
- **Threat-ENUMERATION completeness mechanization** — named as ARGUS's residual unmechanized judgment (§35.5); honest-claim locked decision #3 forbids overclaiming it.
- **A formal "security gate" object** — if the team wants one (vs. my HARD-STOP mapping, W1), that is a separate design; this arc binds to the existing HARD STOP.
- **origindex-trw retro-fix** — the incident arc itself is not re-opened; Arc A hardens the process so the next one cannot drift the same way.

---

*Authored for the PRINCIPAL (Denson Smith). No author-like field is touched by these edits.*
