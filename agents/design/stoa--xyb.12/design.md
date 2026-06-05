# Design — Arc A: Ariadne decoupling (stoa--xyb.12)

**Author:** Denson Smith
**Seat:** CAPTAIN_DAEDALUS_the-stoa
**Branch:** `arc-A/build`
**Spec (LOCKED, executed not re-litigated):** `docs/debloat-decisions.md` → "Ariadne decoupling — SETTLED (scope A + optional C; leave B)"

---

## §1 Problem restatement + A/B/C disposition (against actual file state)

**Restatement.** Base Stoa currently encodes the *assumption* that an "Ariadne" search tool is present/being-set-up in the environment (op-disc §21 + MAJOR_POLYBIUS §16.4 are authoring disciplines premised on "PRINCIPAL is setting up Ariadne"; op-disc §16 / bw-fit-matrix name "Ariadne" as *the* read-side projection). The PRINCIPAL has decided Ariadne is an **optional, scale-triggered, per-project add-on**, not part of base Stoa (base Stoa already knows how to take on add-ons via §23 base/custom + §31 component design). This arc removes the *assumption* while preserving every *provenance* anchor (the empirical history that Ariadne work produced these insights is evidence, not a dependency). The split is **per-LINE**: in a single file, framing lines get de-named (A) while empirical-anchor lines that legitimately cite Ariadne provenance are left untouched (B).

**Imported assumptions (named per §6.1):**
1. The ledger says "op-disc §16 → DE-NAME," but op-disc §16 is now a **relocation stub** (Arc 47) — the actual "Ariadne — semantic recall" framing text lives in `modules/bw-fit-matrix.md`. So the §16 de-name is applied **in the module**, and op-disc §16 itself needs no edit. I treat the ledger's "§16" as naming the *content unit* (which now lives in the module), not the stub. ARGUS should confirm this read.
2. Cutting §16.4 and §21 has a **cascade** the ledger does not enumerate line-by-line: MAJOR_POLYBIUS §16.5 and §16.7 contain Ariadne namings / a §21 cross-ref that break or go stale on the cut. I classify these as **A-cascade** (in-scope consequences of the named A-edits) and handle them. ARGUS should confirm I have not over-reached scope.
3. The C-targets are **entangled** with live-ecosystem `ariadne-core-workspace` references that are NOT name-drops (they identify a real peer workspace). I keep C a strictly separable slice and recommend a **minimal** C (or C-skip) on losslessness-of-meaning grounds — see §4.C and §8.

**A/B/C disposition restated:**
- **A (do):** op-disc §21 → CUT (tombstone stub). MAJOR_POLYBIUS §16.4 → CUT. bw-fit-matrix framing (lines 27/32/35) → DE-NAME. Plus the inbound-ref repairs + the A-cascade de-names below.
- **B (leave, guard):** every `ariadne--xxx` ticket id, "originated in ariadne-core-workspace," PR #34, and **specifically the `stoa--vmc` anchor line in bw-fit-matrix.md (line 45)**. Any deletion of a B-anchor = the arc is WRONG.
- **C (optional, separable, low value):** generic-placeholder swaps for example name-drops — handled as an isolated slice so lossless-on-canon is assessable on A alone.

**Threat classification (§6.12, A3):** `not threat-ratified (process / substrate-canon change, no runtime attack path)`. This arc removes a documentation *assumption* + de-names framing prose; it ships no runtime mechanism and exposes no attack surface (§35.5 carve-out for process / role-file hardening). DAEDALUS PROPOSES this classification; ARGUS CONFIRMS it (cannot be self-granted). No A3 threat→mitigation map and no threat-anchored probe are required (§6.13).

**CUT convention adopted (load-bearing): tombstone stub, NOT renumber, NOT number-gap.**
Rationale: the corpus keys cross-references by section *number* (the §0.5 PROVENANCE table has a `§21 empirical` row; MAJOR_POLYBIUS §16.7 cross-refs `§21`; op-disc line 889 states verbatim "do **NOT** renumber"). Renumbering §22–§36 would invalidate dozens of inbound `§N` cross-refs across the corpus — confirmed wrong. A silent number-gap (delete §21 entirely, leave 20→22) loses the audit-time signal that something *was* there. The corpus's established shape for a section whose body has left is the **relocation stub** (§16, §32: heading + number preserved + one-line pointer). A CUT is the terminal case of that same pattern: **preserve `## 21.` + heading-as-tombstone, replace the body with a one-line CUT notice + a §0.5 relocation-index row marking it CUT (not relocated).** This is lossless-on-audit (a reader/grep landing on §21 learns it was cut, why, and where the generic kernel now lives) and renumber-free.

---

## §4 Per-file, per-locus edit plan (each edit tagged A / B-guard / C)

> ADA applies these mechanically. Anchor text is verbatim from current HEAD (`0719047`). `→` separates before/after. Line numbers are HINTS; match on the anchor text.

### 4.1 `substrate/operating-disciplines.md` §21 — CUT (tombstone stub) [A]

**On-read finding (§21 generic kernel) — FOLD-IN REQUIRED, not pure cut.** §21's kernel is "author for retrievability AND compaction-recovery; titles/cross-refs/content-density/alignment-with-compaction-recovery." The ledger says this kernel is "already covered by §30 + the handoff-author skill; fold a one-liner there ONLY if a genuinely unique bit surfaces on read." **I read §8 + §30 + `skills/handoff-author/SKILL.md` and a unique bit DOES surface:** §8 is *brief*-authoring (positive references + scaffolding for a downstream agent); §30 is the identity model (WHAT crosses session boundaries); the handoff-author skill's principle 5 is "cite, don't duplicate." **None of them states the §21 retrievability/compaction-recovery authoring MECHANICS** — write self-contained, well-titled, cross-referenced units that survive being read out of order / out of context / in fragments. That generic discipline (stripped of the Ariadne *vector-retrieval* premise) is independently load-bearing for compaction-recovery and is NOT verbatim-covered elsewhere. → **CUT the Ariadne-premised section; FOLD a compaction-recovery one-liner into §8.** A pure cut would silently lose a real authoring discipline (self-catch §6.2; verified — see §8 weak point 3).

**EDIT 4.1a — fold the compaction-recovery kernel into §8.** Append to the end of `## 8. Authoring downstream artifacts` (after §8.2's Anchor line 230, as a new short sub-discipline `### 8.3`), EXACTLY:

```

### 8.3 Author durable artifacts for compaction-recovery

Whenever you author a durable artifact (bw ticket/comment, design doc, retro entry, commit subject, handoff doc, arc directive), write it so it survives being read **out of order, out of context, or in fragments** after a `/compact` or a fresh session: **titles** are search-friendly (distinct, specific, named-entities, readable without surrounding context — prefer `arc-26 check.sh adds MISSING+OBSOLETE categories` over `update X`); **cross-refs** name related artifacts explicitly (bw IDs, file paths `substrate/...md` §N, commit SHAs); **content density** favors semantic-chunked units (`## §N — <topic>` self-contained sections) over monolithic prose. This is the same discipline that serves a POLYBIUS re-reading the corpus after `/compact` — there is no trade-off. Forward-only: guidance for new artifacts, NOT a mandate to retroactively restructure existing ones (A8). (A project that deploys an optional read-side projection add-on inherits this discipline unchanged — it is the same authoring shape whether the reader is a human after compaction or a retrieval query.)
```

> The fold keeps the generic, durable kernel (the part that is NOT Ariadne-premised) and drops the "PRINCIPAL is setting up Ariadne tools" assumption + the Ariadne-retrieval framing. Sub-number `### 8.3` is the next free sub-number under §8 (currently §8.1, §8.2). If ARGUS prefers the fold land in §6 (compaction-recovery home) instead of §8 (authoring home), §8 is the better fit because the kernel is an *authoring* discipline; §6 is PLINY-recovery *mechanics*. Flagged in §8 weak points.

**EDIT 4.1b — replace the §21 body with a tombstone.** Anchor = the whole section, lines 899–919 (from `## 21. Ariadne-search-ready authoring` through the `**Empirical anchor:**` paragraph ending `...accretes as future arcs author artifacts under this discipline.`), inclusive. Replace with EXACTLY:

```
## 21. [CUT — Ariadne-search-ready authoring]

**CUT (Arc A, `stoa--xyb.12`).** This section encoded an authoring discipline premised on the assumption that an "Ariadne" search tool was being set up for the substrate corpus. Per the PRINCIPAL's 2026-06-04 decoupling decision (`docs/debloat-decisions.md`), Ariadne is an optional per-project add-on, not part of base Stoa. The generic, non-Ariadne-premised kernel (author durable artifacts for compaction-recovery — search-friendly titles, explicit cross-refs, semantic-chunked content density) is folded into §8.3 (authoring downstream artifacts); see also §30 (four-layer identity / what crosses session boundaries) and `substrate/skills/handoff-author/SKILL.md`. Number preserved as a stable cross-reference key (do NOT renumber); empirical provenance retained in §0.5. Original rationale: `bw show stoa--32b.3`.
```

> Section-number convention: heading reads `## 21. [CUT — ...]` so a grep for `## 21.` still lands the reader, and a grep for `Ariadne-search-ready authoring` still resolves to the tombstone (not a dangling miss). The number stays a valid key.

**EDIT 4.1c — §0.5 relocation-index row.** The existing PROVENANCE row at line 77 (`| §21 empirical | bw show stoa--32b.3 (Anchor; rule stays inline) | PROVENANCE |`) — the rule no longer "stays inline." Replace that one row with EXACTLY:

```
| §21 CUT — Ariadne-search-ready authoring (Arc A `stoa--xyb.12`) | generic compaction-recovery kernel → §8.3; provenance `bw show stoa--32b.3` | CUT |
```

> This is the audit-time losslessness-recovery row: a reader auditing §0.5 sees §21 was CUT (not relocated), where the kernel went, and the provenance anchor. Mirrors the existing PROVENANCE-row shape; `CUT` is a new class value (analogous to CONDITIONAL / PROVENANCE / DUPLICATE already in use).

### 4.2 `substrate/operating-disciplines.md` §21 inbound cross-references [A]

Full inbound scan for `§21` across `substrate/` (live canon only; arc directives + worked-examples handled separately below):

**EDIT 4.2a — §21 body's own internal "POLYBIUS-specific framing" line (op-disc:917)** is removed as part of EDIT 4.1a (it's inside the cut section). No separate action; noting it so the scan is complete.

**EDIT 4.2b — MAJOR_POLYBIUS §16.7 cross-ref (MAJOR_POLYBIUS.md:440).** Anchor (within the "Sibling files / skills:" sentence):
`` `operating-disciplines.md` §21 (Ariadne-search-ready authoring, universal-team); §30 (Four-layer identity model `` →
`` `operating-disciplines.md` §30 (Four-layer identity model ``
(Remove the dangling `§21 (Ariadne-search-ready authoring, universal-team); ` clause; §30 cross-ref remains. The §16.4 it paralleled is also being cut.)

**NON-EDITS (B-guard / out-of-live-canon), explicitly enumerated so ARGUS sees the scan was complete:**
- `operating-disciplines.md:77` — handled by EDIT 4.1b (becomes the CUT row).
- `substrate/skills/decision-surface/worked-example-debloat.md:59` — "Every revised row renders the transition transparently, e.g. §21:" — this is an **illustrative example inside a skill's worked-example doc**, not a live cross-ref into op-disc §21's content. It uses §21 as a *sample row label* for the debloat-surface mechanism. **LEAVE** (editing it would falsify the worked example's own historical illustration; it is not a dependency on §21's body). Flagged in §8 as a judgment call.
- `substrate/arcs/arc-28-build-directive.md:42` — "likely after §21 Ariadne-search-ready authoring" — **arc directives are frozen historical records** (a directive is the durable spec of a *past* arc; it is never retroactively edited — §16.4/A8 forward-only convention). **LEAVE.**

### 4.3 `substrate/MAJOR_POLYBIUS.md` §16.4 — CUT [A]

**EDIT 4.3a — remove §16.4 entirely.** Anchor = lines 424–426 inclusive:
```
### 16.4 Ariadne-search-ready authoring (forward discipline)

PRINCIPAL is setting up Ariadne tools to search the substrate corpus across all repos. Write artifacts good both for human re-reading after compaction AND for vector retrieval; the disciplines align: **titles** should be search-friendly (distinct, specific, named-entities, readable out of context); **cross-refs** name related artifacts explicitly (bw IDs, file paths, commit SHAs); **content density** favors semantic-chunked sections (`## §N — <topic>`, each a self-contained retrieval unit) over monolithic prose (canonical example: the retro at `docs/sessions/2026-05-16-substrate-update-architecture-reframe--retro.md`); authoring-for-ingestion and authoring-for-compaction-recovery want the same self-contained, well-titled, cross-referenced units. **Forward guidance** — applies to new artifacts, NOT a mandate to retroactively restructure (A8). Universal-team framing: `operating-disciplines.md` §21.
```
→ **delete these 3 lines** (heading + body + the trailing blank line). Sub-section numbering: §16.5/§16.6/§16.7/§16.8 keep their numbers (do NOT renumber to close the 16.4 gap — same key-stability rule as top-level sections; §16.7 and §16.8 are cross-referenced by number). Leave the `### 16.4` slot as a number-gap is acceptable at the *sub-section* level (16.x sub-numbers are local to §16 and less cross-referenced), BUT to stay consistent with the top-level tombstone convention, **insert a one-line sub-tombstone** in place of the body:

```
### 16.4 [CUT — Ariadne-search-ready authoring]

**CUT (Arc A, `stoa--xyb.12`).** POLYBIUS-twin of the cut op-disc §21; removed under the same Ariadne-decoupling decision (`docs/debloat-decisions.md`). The handoff-authoring discipline that survives is §16.3 (multi-artifact handoff shape) + `substrate/skills/handoff-author/SKILL.md`. Sub-number preserved (do NOT renumber 16.5–16.8).
```

> Decision recorded: sub-tombstone over silent gap, for consistency with the §21 top-level convention and because §16.8 line 444 cross-refs "§16.4" (a tombstone keeps that cross-ref resolving rather than dangling — see EDIT 4.3c).

**EDIT 4.3b — §16.7 self cross-ref to §16.4 list.** Already covered by EDIT 4.2b (same line 440 edit removes the §21 clause; §16.7's "Within this file:" enumeration does NOT list §16.4, verified — no further edit needed there).

**EDIT 4.3c — §16.8 inbound ref to §16.4 (MAJOR_POLYBIUS.md:444).** Anchor:
`(A8 forward-only convention, shared with §16.4).` →
`(A8 forward-only convention, shared with §16.3).`
(Re-point from the cut §16.4 to §16.3, which is the surviving handoff discipline that carries the A8 forward-only convention. The §16.4 tombstone would also resolve, but §16.3 is the substantive home — prefer the live anchor.)

### 4.4 `substrate/MAJOR_POLYBIUS.md` §16.5 — A-cascade de-name [A-cascade]

**EDIT 4.4 — §16.5 Ariadne naming (MAJOR_POLYBIUS.md:430).** Anchor (within the "The lens makes several choices coherent:" sentence):
`Ariadne corpus search is the operational form of "you" being a multi-version collective;` →
`an optional read-side projection add-on (hybrid search + KG) over the corpus is the operational form of "you" being a multi-version collective;`

> Rationale: this is an *assumption*-flavored naming ("Ariadne corpus search is the operational form of...") in the POLYBIUS-as-collective lens — exactly the class of base-Stoa-assumes-Ariadne framing this arc removes. De-named with the ledger's canonical replacement phrase. **Judgment call** (this line is outside the four named loci): flagged in §8. If ARGUS rules this out-of-scope, the fallback is to leave it (it is a softer naming than §16.4/§21) — but de-naming is the consistent application of the decision.

### 4.5 `substrate/modules/bw-fit-matrix.md` — DE-NAME framing, KEEP stoa--vmc anchor [A + B-guard]

The "Ariadne — semantic recall / read-side projection" framing lives here (op-disc §16 is the relocation stub, per Imported Assumption #1). De-name the framing; the scale insight (write-side bw + an optional read-side projection layer + hypergraph) is preserved verbatim except the proper noun.

**EDIT 4.5a — line 27 (the §16.2 lead sentence).** Anchor:
`**bw is the write-side substrate; Ariadne is the read-side projection; hypergraph extends the projection to relational reads.**` →
`**bw is the write-side substrate; an optional read-side projection add-on (hybrid search + KG) is the read-side projection; hypergraph extends the projection to relational reads.**`

**EDIT 4.5b — line 32 (the bullet label + body).** Anchor:
`- **Ariadne (read-side projection).** A sidecar projection layer that mirrors bw's state into a queryable shape (typically SQLite + FTS5 + structured indices). Built for relational reads, full-text search, cross-ticket aggregation, and analytics queries that bw cannot serve fast at scale. The projection is eventually-consistent with bw; bw is the source of truth, Ariadne is the cached query layer.` →
`- **Read-side projection add-on (hybrid search + KG).** An optional sidecar projection layer that mirrors bw's state into a queryable shape (typically SQLite + FTS5 + structured indices). Built for relational reads, full-text search, cross-ticket aggregation, and analytics queries that bw cannot serve fast at scale. The projection is eventually-consistent with bw; bw is the source of truth, the projection is the cached query layer.`

**EDIT 4.5c — line 33 (hypergraph bullet, "sits on top of Ariadne").** Anchor:
`the hypergraph layer sits on top of Ariadne.` →
`the hypergraph layer sits on top of the read-side projection.`

**EDIT 4.5d — line 35 (§16.2 closing "mental model" paragraph).** Anchor:
`The bw → Ariadne integration arc was proving exactly this: the bulk-seed wall was the empirical evidence that bw is for writes, Ariadne is for reads, and the two layers compose.` →
`The bw → read-side-projection integration arc was proving exactly this: the bulk-seed wall was the empirical evidence that bw is for writes, the projection add-on is for reads, and the two layers compose.`

> Note: line 9 ("...the 2026-05 stoa + ariadne integration arcs") and line 45 (the `stoa--vmc` empirical anchor, which contains "the bw → Ariadne integration arcs in ariadne-core-workspace") are **B-anchors (provenance of where the scale insight was empirically proven)** — **LEAVE BOTH.** Specifically line 45 `Empirical anchor: \`Anchor: stoa--vmc\` ...` is the named B-guard line; do NOT touch it. The de-name targets the *framing* (the mental model presented as guidance), not the *provenance* (where it came from).

**EDIT 4.5e — module front-matter relocation note (line 3).** The module header says "Relocated from `operating-disciplines.md` §16". No Ariadne naming there; **no edit.** (Enumerated for scan completeness.)

### 4.6 `substrate/templates/handoff-doc-template.md` §16.4 cross-ref [A]

**EDIT 4.6 — line 69.** Anchor:
`**Authoring discipline:** \`substrate/MAJOR_POLYBIUS.md\` §16.3 (multi-artifact handoff shape) + §16.4 (Ariadne-search-ready authoring).` →
`**Authoring discipline:** \`substrate/MAJOR_POLYBIUS.md\` §16.3 (multi-artifact handoff shape).`
(Remove the `+ §16.4 (Ariadne-search-ready authoring)` clause — §16.4 is cut; §16.3 is the surviving authoring discipline.)

> Note: handoff-doc-template lines 52, 86, 88, 124 contain "dev Ariadne deployment" / "Ariadne deployment as section 2" — these are **B-anchors** (they describe the real `HANDOFF_POLYBIUS_2026-05-16.md` example's actual content); **LEAVE.** Only the §16.4 cross-ref (line 69) is an A-edit here.

### 4.C OPTIONAL — genericize example name-drops (SEPARABLE slice; assess lossless-on-canon on A ALONE) [C]

> **C is a separable commit/slice. The losslessness-on-canon claim in §1 holds on A alone; C is pure cosmetic name-drop reduction and is RECOMMENDED-MINIMAL / SKIPPABLE.** Each C-target below is entangled with live `ariadne-core-workspace` references that are NOT name-drops (they identify a real peer workspace in the multi-team ecosystem). Genericizing one occurrence while real-workspace references remain in the same paragraph produces *inconsistency*, not cleanliness. My recommendation per target:

- **C1 — `operating-disciplines.md:488`** (`ariadne--xxx` in the ticket-id-format example, alongside `stoa--xxx`, `acb--xxx`). **RECOMMEND SKIP.** `ariadne--xxx` here is one of three real-prefix examples illustrating the hash-suffix convention; it is illustrative-of-format, the entire point is showing real project prefixes. Swapping only this one is inconsistent (why keep `stoa--`/`acb--` but not `ariadne--`?). If C is taken anyway: `ariadne--xxx` → `proj--xxx`. Low value.
- **C2 — `operating-disciplines.md:1139`** (`ariadne-core` as one of two slug examples: `the-stoa`, `ariadne-core`). **RECOMMEND SKIP.** Same shape — `ariadne-core` is a real project slug illustrating the `<project-slug>` convention; it is a true example, not an assumption. If taken: `ariadne-core` → `proj-name`. Low value.
- **C3 — `MAJOR_POLYBIUS.md:576`** (ingest-pipeline example: "the Ariadne ingest pipeline at ariadne-core-workspace"). **RECOMMEND SKIP.** This is a *real worked example* of project-shaped work at a real workspace; it sits beside "the case study HTML at the-stoa" and "a Railway deploy at railway_stoa" (both real). Genericizing one of three parallel real examples is inconsistent. If taken: `the Ariadne ingest pipeline at ariadne-core-workspace` → `a domain-ingest pipeline at a peer workspace`. Low value.
- **C4 — `modules/multi-team-interop.md:27`** ("a railway_stoa deploy that serves an API ariadne-core-workspace consumes"). **RECOMMEND SKIP.** `ariadne-core-workspace` appears at lines 38, 62, 80 of the SAME module as live-ecosystem references (the prefix table, the sibling-directory convention, the empirical anchor). Genericizing only line 27 is inconsistent with the rest of the module. If taken: `ariadne-core-workspace consumes` → `a consumer workspace consumes`. Low value.
- **C5 — `modules/bw-upgrade.md:25`** ("Railway-deployed Ariadne, etc."). **RECOMMEND SKIP or TAKE (cleanest of the set).** This is a genuine generic-example slot ("etc.") with no entangled real-workspace dependency in the immediate clause. If taken: `Railway-deployed Ariadne, etc.` → `a deployed runtime service, etc.`. This is the only C-target that is a clean swap; still low value.
- **C6 — `templates/handoff-doc-template.md` example content** (lines 52/86/88/124, "dev Ariadne deployment"). **RECOMMEND SKIP.** These describe the *actual content* of the real canonical example file `HANDOFF_POLYBIUS_2026-05-16.md`; they are effectively B-provenance (they tell the reader what is really in that example file). Genericizing them would make the template lie about its own canonical example. **Treat as B, not C.**

> **C verdict (DAEDALUS recommendation): take only C5 if any; SKIP C1–C4 and C6.** They are entangled with real-ecosystem references; genericizing them produces inconsistency, not losslessness improvement, and risks scrubbing what is effectively provenance. The arc's value is fully delivered by A. ARGUS/PRINCIPAL may overrule toward "take all C" — if so, apply the before/after swaps as written above, as a SEPARATE commit after the A commit.

---

## §5 VERA verification probes

> All probes run from the worktree root `C:/Users/denso/claude_projects/the-stoa/.claude/worktrees/arc-A-build`. Probes assume the A-slice is applied; C-probes gated on whether C was taken.

**P1 — B-anchor integrity (no provenance deleted), incl. the `stoa--vmc` line.** The named B-anchors must survive verbatim. Re-execute:
```
git -C . diff 0719047 HEAD -- substrate/ | grep -E '^-' | grep -iE 'ariadne--|stoa--vmc|PR #34|originated in ariadne-core-workspace|ariadne-core-workspace'
```
**PASS = NO output** (no removed line contains a B-anchor). Specifically assert the `stoa--vmc` line survives:
```
grep -n 'Anchor: stoa--vmc' substrate/modules/bw-fit-matrix.md
```
**PASS = line 45 (the empirical anchor) still present, verbatim.** This is the load-bearing "the arc is WRONG if a B-anchor was scrubbed" guard.

**P2 — no stray "Ariadne" in the de-named framing loci.** After de-naming, the framing in bw-fit-matrix §16.2 and the de-named POLYBIUS §16.5 clause must carry NO "Ariadne":
```
grep -ni 'ariadne' substrate/modules/bw-fit-matrix.md
```
**PASS = ONLY line 9 ("...stoa + ariadne integration arcs") and line 45 (the `stoa--vmc` anchor) match — both B-provenance, explicitly exempted.** Lines 27/32/33/35 must NOT match. (VERA: confirm the two surviving matches are exactly the two provenance lines, not a missed framing line.)
```
sed -n '430p' substrate/MAJOR_POLYBIUS.md | grep -i 'ariadne corpus search'
```
**PASS = NO output** (the §16.5 assumption-naming is gone).

**P3 — §21 / §16.4 inbound-ref integrity (no dangling cross-refs).** No live-canon file may carry a cross-ref to §21 or §16.4 *as a live authoring discipline*:
```
grep -rn '§21 (Ariadne' substrate/MAJOR_POLYBIUS.md substrate/templates/ substrate/operating-disciplines.md
grep -rn '§16.4 (Ariadne' substrate/
grep -rn '+ §16.4' substrate/templates/handoff-doc-template.md
```
**PASS = NO output for all three** (the §16.7 §21 clause, the handoff-template §16.4 clause are removed). Then assert the surviving re-points resolve:
```
grep -n 'shared with §16.3' substrate/MAJOR_POLYBIUS.md   # §16.8 re-point landed
grep -n '## 21. \[CUT' substrate/operating-disciplines.md  # tombstone present
grep -n '### 16.4 \[CUT' substrate/MAJOR_POLYBIUS.md        # sub-tombstone present
```
**PASS = each returns exactly one line.**

**P4 — tombstone + §0.5 row losslessness (audit-time recovery).**
```
grep -n '§21 CUT' substrate/operating-disciplines.md       # the §0.5 CUT row
```
**PASS = one match in the §0.5 table (line ~77 region)**, and the row names the kernel destinations (§8 + §30 + handoff-author skill) + provenance `stoa--32b.3`. Manual spot-check: the §21 tombstone body cites `bw show stoa--32b.3` (provenance preserved) and the kernel destinations.

**P5 — no section renumber (cross-ref key stability).** The top-level section sequence must be unchanged except §21's heading-form:
```
grep -nE '^## [0-9]+\.' substrate/operating-disciplines.md
```
**PASS = sequence is identical to HEAD (0.5,1..36) with §21 now reading `## 21. [CUT — ...]`.** No section 22–36 shifted. Sub-section §16.5–§16.8 numbers unchanged in MAJOR_POLYBIUS.

**P6 — authorship unchanged.** No author-like field touched:
```
git -C . diff 0719047 HEAD -- substrate/ | grep -iE '^[+-].*(author|owner|creator|maintainer|copyright|by:)' | grep -vi 'co-authored-by'
```
**PASS = NO output** (no author-like field added/removed/changed). The only Co-Authored-By in scope is the design commit's seat trailer, which is metadata layered on top of (not replacing) Author = Denson Smith.

**P7 — lossless-on-canon spot-checks (the scale insight + handoff discipline survive).**
- bw-fit-matrix §16.1 matrix table + §16.3 decision rule + the "5k commit wall" scale insight present and unchanged: `grep -n 'TreeFS.Commit\|5k tickets\|write-side substrate' substrate/modules/bw-fit-matrix.md` → matrix/scale insight intact.
- POLYBIUS handoff authoring discipline survives via §16.3: `grep -n '16.3' substrate/templates/handoff-doc-template.md` → cross-ref now points only at §16.3.
- **§8.3 fold landed (the §21 kernel was preserved, not lost):** `grep -n '### 8.3 Author durable artifacts for compaction-recovery' substrate/operating-disciplines.md` → one match; and the new §8.3 body contains "search-friendly", "cross-refs", "semantic-chunked", "compaction" (the preserved mechanics). The §21 tombstone's "folded into §8.3" claim must resolve: `grep -n '§8.3' substrate/operating-disciplines.md` → matches in both the tombstone and the §0.5 row. **(If ARGUS ruled pure-cut instead of fold, this probe is replaced by: §8.3 absent AND the tombstone re-points to "§8 + §30 + handoff-author skill".)**
- op-disc §30 (named in the §21 tombstone "see also") exists and is non-empty: `grep -nE '^## 30\.' substrate/operating-disciplines.md`.

**P8 (C-slice, gated on C taken) — C consistency.** If C was applied, assert no swapped placeholder sits beside an un-swapped real reference in the same paragraph (the entanglement risk). For each C-target taken, manually confirm the paragraph reads consistently. **If C skipped: P8 is N/A — the A-slice losslessness claim is independent of C.**

---

## §8 Self-assessed weak points

- **Weak point: "§16 de-name" is applied in the module, not op-disc §16 (the stub).** The ledger literally says "op-disc §16 → DE-NAME," but the Ariadne framing text was relocated to `modules/bw-fit-matrix.md` in Arc 47; op-disc §16 is now a content-free stub. *Why this shape anyway:* the ledger names the *content unit* (semantic-recall framing), which now lives in the module; de-naming the module is the faithful execution of the intent. If a reviewer insists the literal op-disc §16 stub must change, there is nothing there to de-name — flagged for ARGUS to confirm the read.

- **Weak point: §16.5 / §16.7 de-names are A-cascade, outside the four literally-named loci.** I extended the de-name to MAJOR_POLYBIUS §16.5 ("Ariadne corpus search is the operational form...") and removed the §16.7 §21 cross-ref, because cutting §21/§16.4 leaves them stale/assumption-bearing. *Why this shape anyway:* a CUT that leaves dangling cross-refs and twin assumption-namings is not lossless-on-decoupling — the corpus would still assert "Ariadne corpus search is the operational form of you." But this is scope-judgment, not ledger-literal; ARGUS should rule whether §16.5 de-name is in-scope or should be left (it is the softest naming of the set).

- **Weak point: I REVISED off the ledger's "pure cut" lean to a CUT-plus-fold, because a unique bit surfaced on read.** The ledger says "fold a one-liner ONLY if a genuinely unique bit surfaces on read." I read §8 + §30 + handoff-author and found that the §21 compaction-recovery authoring *mechanics* (search-friendly titles / explicit cross-refs / semantic-chunked durable units) are NOT verbatim-covered: §8 is brief-authoring + scaffolding, §30 is the identity model, handoff-author principle 5 is "cite, don't duplicate." So a pure cut would silently lose a real discipline → I fold §8.3. *Why this shape anyway:* the ledger explicitly licenses exactly this fold-when-unique-bit-surfaces; the bit surfaced; §6.2 self-catch forbids claiming coverage that doesn't exist. The risk is the *inverse* — that ARGUS judges the §8.3 fold redundant (over-preservation). If so, the fallback is the pure cut (just drop EDIT 4.1a; the tombstone EDIT 4.1b's "folded into §8.3" clause then re-points to "§8 + §30 + handoff-author skill" as covering-enough). ARGUS rules: is the compaction-recovery authoring mechanic a genuinely-unique surviving bit (fold) or already-covered (pure cut)?

- **Weak point: the tombstone-stub CUT convention is a DAEDALUS choice, not a pre-existing corpus convention for full CUTs.** The corpus has *relocation* stubs (§16, §32) but no prior *full-CUT* tombstone to copy. *Why this shape anyway:* renumbering is confirmed wrong (line 889 "do NOT renumber" + numeric cross-ref keys), and a silent number-gap loses audit signal; the tombstone is the minimal lossless-on-audit convention consistent with the existing relocation-stub shape. I introduce `CUT` as a §0.5 class value alongside CONDITIONAL/PROVENANCE/DUPLICATE. ARGUS should confirm this is the right convention (vs. e.g. number-gap-with-§0.5-row-only).

- **Weak point: C is entangled with real-ecosystem references; my recommendation is "skip C1–C4/C6, maybe C5."** If the PRINCIPAL wanted aggressive genericization, my minimal-C recommendation under-delivers on C. *Why this shape anyway:* the C-targets cite real workspaces (ariadne-core-workspace is a live peer, not a name-drop); genericizing one occurrence among real-workspace siblings produces inconsistency, and C6 is effectively provenance about a real example file. C is explicitly "optional, low value" in the ledger; I keep it a separable slice so A's losslessness is assessable alone, and recommend minimal. ARGUS/PRINCIPAL may overrule toward full-C; the before/after swaps are all written in §4.C ready to apply.

- **Weak point: `skills/decision-surface/worked-example-debloat.md:59` uses "§21" as a sample-row label and I left it.** If a reader treats that as a live §21 cross-ref it now points at a tombstone. *Why this shape anyway:* it is an illustrative *example of the debloat-surface mechanism* (it shows what a revised row looks like, using §21 as the sample), not a dependency on §21's authoring content; editing it would falsify the worked example's own illustration. Flagged for ARGUS.

---

## Out of scope (deliberate non-edits)

- **Deploying to `.claude/`.** This arc edits `substrate/` source only. The `install.sh` self-apply that propagates these edits to deployed `.claude/` is a SEPARATE downstream housekeeping step (per MAJOR_POLYBIUS §18.1), NOT in this arc's build scope. **Follow-up:** a self-apply commit after the arc lands.
- **Arc directives (`substrate/arcs/*`).** Frozen historical records of past arcs; never retroactively edited (A8 forward-only). Their many `§21` / `Ariadne` references stay.
- **All B-anchors corpus-wide.** Provenance, not dependency. ~40 `ariadne--`/`ariadne-core` references across substrate are provenance/ecosystem and stay.
- **Arc B / Arc C work** (op-disc consolidation, encode batch). Separate arcs in the `stoa--xyb` epic, dependency-ordered after A.
- **Building the read-side projection add-on itself.** This arc removes the *assumption* of it; building/installing the optional add-on is a per-project concern, out of base Stoa.
