# Design — Arc B: op-disc prose consolidation (stoa--xyb.13)

Author: Denson Smith. Seat: CAPTAIN_DAEDALUS_the-stoa. Epic: stoa--xyb. Spec: `docs/debloat-decisions.md`.
Target file: `substrate/operating-disciplines.md` (+ `substrate/CAPTAIN_ADA.md` for §32 re-points). Worktree: `arc-B/build`.

---

## §1 — Disposition restated against actual file state

This is a **lossless-on-canon prose-consolidation** arc. Three mechanical operations against `substrate/operating-disciplines.md`, all matched on **heading text** (line numbers below are read-time hints from baseline `1cb9160`; ADA matches on the `## N.` heading, not the line number):

1. **FOUR-STANCE MERGE** — the four short anti-pattern stances `## 1. Suppress "ship-it" / momentum pressure`, `## 2. Suppress "MVP" / "minimize round-trips"`, `## 3. Suppress "don't gold-plate"`, and `## 5. Suppress plausible-source citation without verification` merge into ONE section. They are **non-contiguous**: `## 4. Suppress "wait for explicit instruction" (passivity)` sits between §3 and §5 and is **carved OUT** of the merge (KEEP standalone, byte-identical to baseline). Merge **target = §1** (rationale in §2 below). §2/§3/§5 become **pointer-stubs** that preserve their heading numbers (no-renumber).

2. **7 TRIMS (lossless)** — §8, §15, §24, §26, §27, §31, §34. Compress provenance/redundant prose; keep every load-bearing RULE. NOTE the actual file state (the from-memory ledger could not see this): **§27 and §31 are ALREADY relocated module-stubs** (Arc 47), so their "trim" is a stub-prose trim, not a body trim. §24 and §26 are ALREADY thin cross-refs (Arc-era). §8 and §15 are the only two with substantial inline bodies. This matters for the losslessness bar — see each sub-section in §3.

3. **§32 STUB-PROSE CUT (markers + module source RETAINED)** — cut the redundant human-facing stub PROSE of `## 32. Test-environment timing discipline — jsdom + animation libraries` down to a minimal tombstone heading, **but RETAIN the `<!-- MODULE-INLINE:jsdom-timing-discipline -->` … `<!-- /MODULE-INLINE:jsdom-timing-discipline -->` marker pair AND the `substrate/modules/jsdom-timing-discipline.md` source file**. Both are **LOAD-BEARING for subproject deploy** (see §4.2 — install.sh Check A/B hard-abort the deploy if either is missing). The module is **confirmed already relocated** (3504 bytes, full discipline present). Update the §0.5 relocation-index row to "stub-prose CUT, markers retained"; re-point the inbound `§32` cross-refs so nothing dangles.

**No-renumber convention (confirmed, Arc-A precedent):** the corpus keys cross-refs by section number. Following Arc A's `## 21. [CUT — ...]` tombstone precedent (line 903), vacated/cut numbers keep their `## N.` heading as a **stub/tombstone**; the section sequence §1…§36 stays intact. **Verified inbound-ref state:** NO substrate file outside `arcs/` cross-references §1/§2/§3/§5 by number; the only internal labeled ref is op-disc line 254 `§1 (suppress momentum pressure)`, which stays valid because §1 IS the merge target and keeps the momentum stance as its lead. This makes the merge low-risk on cross-ref breakage.

**Restatement-gate note (imported assumptions, named):**
- The ledger says "merge §1+§2+§3+§5 into ONE section" but does not name the target number. I import **target = §1** (defended in §2).
- The ledger's trim list predates Arc 47's relocations; I import the **actual** file state (§27/§31 are stubs, §24/§26 are thin cross-refs) over the ledger's implicit "these are full bodies" framing. This is a convergence, not a re-scope: the disposition (trim) is unchanged; only the magnitude of available trim differs. Flagged as a weak point (§8).
- "Lossless-on-canon" = every load-bearing RULE survives grep-findable; provenance prose and duplicate framing MAY compress. I treat empirical-anchor `bw show <id>` cites as **load-bearing provenance to keep** (they are the substrate's evidence trail, same B-LEAVE principle as Arc A), and treat *narrative restatement* of why-this-anchor-matters as compressible.

---

## §2 — FOUR-STANCE MERGE design + RULE-BY-RULE PRESERVATION MAP

### 2.1 Merge target + vacated-section convention

**Target = §1.** Reasons: (a) §1 is the only one of the four with an inbound labeled internal ref (line 254), which stays valid for free; (b) the natural reading order of the merged section opens on the momentum stance; (c) merging into the lowest number minimizes visual disruption to the §1→§6 head-of-file ordering.

**New §1 heading:** `## 1. Suppress the four human-team anti-pattern stories (momentum / MVP / gold-plating / plausible-citation)`. The merged section carries all four stances as labeled `###` sub-stances so each stance's content stays a self-contained, grep-findable unit (§8.7 compaction-recovery discipline applied to the merge itself).

**Vacated §2/§3/§5 — pointer-stub convention** (mirrors Arc-A §21 tombstone; numbers preserved):

```
## 2. [MERGED → §1] Suppress "MVP" / "minimize round-trips"
Merged into §1 (the four anti-pattern stances) on Arc B (`stoa--xyb.13`). Number preserved as a stable cross-reference key (do NOT renumber). The MVP / minimize-round-trips stance is §1's sub-stance "MVP".
```
(§3 and §5 identical shape, naming their own sub-stance.) §4 is **untouched** between them.

### 2.2 Rule enumeration per stance (baseline text)

**§1 (momentum) — rules:**
- 1a. In human teams momentum was a real cost worth optimizing; with agents a full pipeline cycle (DAEDALUS→ARGUS→ADA→VERA→CATO→ZENO) is minutes — agents don't run out.
- 1b. RULE: momentum pressure is no longer a reason to skip steps; it is just a story the model tells itself to skip work.
- 1c. RULE: if you reason "ship without the full gauntlet to keep momentum" — stop. The gauntlet is what's expensive in human teams; in an agent team it's the cheap thing.

**§2 (MVP / round-trips) — rules:**
- 2a. Round-trips were expensive when they meant scheduling a meeting; agent round-trips cost tokens not days.
- 2b. RULE: optimizing to minimize agent round-trips by cutting verification is a category error.
- 2c. RULE: round-trips are how the team catches its own mistakes; cutting them trades a known small cost for an unbounded cost (a missed defect that lands).

**§3 (gold-plate) — rules:**
- 3a. Adapted from human contexts where extra polish wasted scarce engineering time; with agents "polish" usually means more verification/review/breadcrumbs — the cheap things.
- 3b. RULE: gold-plating those (process) is exactly what the regime makes possible.
- 3c. RULE/distinction: original "don't gold-plate" was about PRODUCT (don't add features no one needed), never PROCESS; in an agent regime polishing the process is free — do it.

**§5 (plausible-source citation) — rules:**
- 5a. A chronic LLM bug: writing "X says Y" where X is real but doesn't say Y.
- 5b. RULE: run the source; if you cannot, flag the citation as unverified and return.
- 5c. RULE/distinction: distinct from POLYBIUS §4.3 / PLINY §7.2 (verify-then-execute, about claims that contradict your model); plausible-source citation is about not making claims at all when you haven't checked. **Both apply.**

### 2.3 Rule-by-rule preservation map

Every enumerated rule lands in the merged §1. Dedup is noted explicitly; **no rule is dropped**. The shared "human-team cost no longer applies to agents" framing (1a/2a/3a) is stated ONCE in the merged preamble and the per-stance bodies reference it — this is a **dedup of framing, not a drop of any rule** (each stance keeps its specific instance: minutes-per-cycle / tokens-not-days / polish-is-cheap).

| Stance rule | Lands in merged §1 at | Dedup note |
|---|---|---|
| 1a momentum-cost-was-real / cycle-is-minutes | preamble (shared framing) + sub-stance "Momentum" ¶1 | framing shared with 2a/3a; momentum's specific "cycle is minutes" instance kept in its sub-stance |
| 1b momentum is a story to skip work | sub-stance "Momentum" ¶1 (bold RULE) | — |
| 1c stop if "ship to keep momentum"; gauntlet is the cheap thing | sub-stance "Momentum" ¶2 | — |
| 2a round-trips-were-meetings / now-tokens-not-days | preamble (shared) + sub-stance "MVP" ¶1 | framing shared; "tokens not days" instance kept |
| 2b minimizing round-trips by cutting verification = category error | sub-stance "MVP" ¶1 (bold RULE) | — |
| 2c round-trips catch mistakes; cutting trades small for unbounded cost | sub-stance "MVP" ¶2 | — |
| 3a human-polish-wasted-time / agent-polish-is-cheap-things | preamble (shared) + sub-stance "Gold-plating" ¶1 | framing shared; "polish = verification/review/breadcrumbs" instance kept |
| 3b gold-plating process is what the regime makes possible | sub-stance "Gold-plating" ¶1 (bold RULE) | — |
| 3c PRODUCT-not-PROCESS distinction; process-polish is free, do it | sub-stance "Gold-plating" ¶2 | — |
| 5a chronic LLM bug "X says Y" where X doesn't say Y | sub-stance "Plausible-citation" ¶1 | — |
| 5b run the source; else flag unverified + return | sub-stance "Plausible-citation" ¶1 (bold RULE) | — |
| 5c distinct-from-verify-then-execute; both apply | sub-stance "Plausible-citation" ¶2 (keeps the POLYBIUS §4.3 / PLINY §7.2 cross-refs verbatim) | — |

### 2.4 Full proposed merged §1 text (ADA builds this verbatim)

```markdown
## 1. Suppress the four human-team anti-pattern stories (momentum / MVP / gold-plating / plausible-citation)

Four anti-pattern "stories" carry over from human-team practice where each one was a rational
optimization, and each one inverts under an agent team. The shared root: in human teams the scarce
resource was engineer-time and scheduling latency, so momentum, minimized round-trips, and avoided
polish all bought something real. With agents a full pipeline cycle (DAEDALUS → ARGUS → ADA → VERA →
CATO → ZENO) is minutes and round-trips cost tokens, not days — so the same stories now just talk the
model out of doing cheap, valuable work. (Passivity — "wait for explicit instruction" — is the fifth
and most-violated such story; it earns its own emphatic section at §4.)

### 1.1 Momentum / "ship-it" pressure
In human teams where each step took weeks, momentum was a real cost worth optimizing. **Momentum
pressure is no longer a reason to skip steps; it is just a story the model tells itself to skip
work.** If you find yourself reasoning "we should ship this without the full gauntlet to keep
momentum" — stop. The gauntlet is what's expensive in human teams; in an agent team, it's the cheap
thing.

### 1.2 "MVP" / "minimize round-trips"
Round-trips were expensive when they meant scheduling a meeting; round-trips between agents cost
tokens, not days. **Optimizing to minimize agent round-trips by cutting verification is a category
error.** Round-trips are how the team catches its own mistakes — cutting them to "go faster" trades a
known small cost (the round-trip) for an unbounded cost (a missed defect that lands).

### 1.3 "Don't gold-plate"
Adapted from human contexts where extra polish wasted scarce engineering time. With agents, "polish"
usually means more verification, more review, more breadcrumbs — the cheap things. **Gold-plating
those is exactly what the regime makes possible.** The original rule was about polishing PRODUCT
(don't add features no one needed); it was never about polishing PROCESS. In an agent regime,
polishing the process is free; do it.

### 1.4 Plausible-source citation without verification
A chronic bug across LLMs: writing "X says Y" where X is real but doesn't actually say Y. **Run the
source. If you cannot, flag the citation as unverified and return.** This is distinct from POLYBIUS
§4.3 / PLINY §7.2 (verify-then-execute), which is about verifying claims that contradict your model;
plausible-source citation is about not making claims at all when you haven't checked. Both apply.
```

**Net-lines effect:** baseline §1+§2+§3+§5 = ~24 content lines across 4 headings + 8 blank separators. Merged = 1 heading + 4 sub-headings + shared preamble, ~30 lines, BUT removes 3 redundant restatements of the shared framing and 3 section separators. Net is roughly flat at the merged-section locus; the line WIN comes from the trims and §32 cut. **This arc's losslessness bar dominates its line-count bar** — the merge is primarily a *coherence* win (four scattered 4-line stances become one teachable section), not a big line cut. Flagged honestly (§8): if the floor-manager expects a large negative delta from the merge alone, that expectation is mis-set; the negative delta lives in §3 + §4.

### 2.5 Downstream framing references to preserve

- op-disc line 13 thesis: "The disciplines below (§1-§31)" — RANGE reference, unaffected (still §1).
- op-disc line 1642 "Agent-regime inverses": **"The six anti-patterns above suppress failure modes."** The six = the content of §1/§2/§3/§4/§5/§6. After merge the *heading count* for stances 1-3-5 drops, but the six anti-pattern *contents* all survive (four in merged §1, passivity in §4, redundancy in §6). **ADA must update this line** to "The anti-pattern stances above (§1 four stories + §4 passivity + §6 redundancy) suppress failure modes" — otherwise "six anti-patterns above" reads as a dangling count. This is a load-bearing edit, listed as a TRIM-adjacent fix (see §3 note) and probed in §5.
- op-disc line 254 `§1 (suppress momentum pressure)` — stays valid (§1 leads with momentum). No change.

---

## §3 — The 7 TRIMS (one sub-section each)

Losslessness bar for every trim: **PRESERVED** rules stay grep-findable in the live section; **CUT** items are redundant restatement or narrative provenance whose removal loses no rule. Empirical-anchor `bw show <id>` cites are PRESERVED (evidence trail).

### 3.1 §8 — Authoring downstream artifacts
Large section (§8.1–§8.7). The load-bearing rules are dense; provenance narration is the trim target.
- **PRESERVED (every rule):** §8.1 positive-references-only rule + the 4-row anti-pattern→discipline table; §8.2 five scaffolding rules + the bidirectional-translation principle paragraph (its canonical home — UNTOUCHED, see the rev2 note below); §8.3 four-state continuum table + decision heuristic + default-bias-toward-lighter (ALL load-bearing — UNTOUCHED, see rev2 note); §8.4 install.sh deploy-plan smoke-beat + the bash beat block + acceptance + fail-handling; §8.5 fallback-chain per-path probe rule + the symmetric ADA/VERA/CATO breakdown + the two pattern tables; §8.6 destructive-probe literal-path hygiene (full — it is cross-referenced from CAPTAIN_DAEDALUS §3 and is load-bearing); §8.7 compaction-recovery authoring rule. All `bw show` anchors kept.
- **CUT (non-load-bearing):** §8.4's "Substrate-canonical implication for Arc 23 itself" paragraph (a one-arc-specific note that Arc 23 doesn't exercise the discipline — historical, not a rule; provenance preserved via the §8.4 anchor). The narrative re-explanation of each empirical anchor MAY compress to the anchor line + one clause (the `bw show` recovers the full story).
- **rev2 correction (DROPPED a phantom cut — ARGUS r2):** the prior design instructed compressing "§8.3's restatement of the bidirectional-translation principle." **That restatement does not exist in §8.3.** I re-read §8.2 + §8.3 + thesis line 29 directly: the bidirectional-translation principle lives at the **thesis (op-disc line 29, which itself points to §8.2)** and in **§8.2 (line 228, "The bidirectional-translation principle" paragraph — its canonical home)**. **§8.3 (lines 234–258) is the four-state session-state continuum** — the table + decision heuristic + default-bias-toward-lighter — and contains NO bidirectional-translation restatement; every line in it is load-bearing rule content. Cutting from §8.3 would drop a real rule. I took **option (b): DROP the §8 bidirectional-translation cut ENTIRELY.** There is no clean lossless trim of the principle: the line-29 thesis statement and the §8.2 canonical-home application are **distinct roles** (thesis preamble vs the authoring-discipline statement), not a redundant duplicate pair — line 29 even cross-references §8.2 as the home, so collapsing either orphans the other. **Named surviving canonical home of the bidirectional-translation principle: §8.2 (line 228), with the thesis pointer at line 29 — both retained verbatim, untouched.** Under no circumstance is anything cut from §8.3.
- **Edit plan:** mechanical paragraph deletion of the §8.4 Arc-23 historical note + per-anchor narrative compression only. **No §8.2 or §8.3 edit.** No rule touched. Est. −5 to −9 lines (smaller than the prior −8 to −14 because the phantom §8.3 cut is dropped).

### 3.2 §15 — Verification-complexity awareness
Large section (§15.1–§15.7). The 2x2, the rule, the four strategies, the two verdict shapes, the time-box defaults are ALL load-bearing (verifier CAPTAINs inherit from here).
- **PRESERVED (every rule):** §15.1 the 2x2 table; §15.2 quadrant-classification-per-claim discipline rule; §15.3 the four verification strategies; §15.4 INCOMPLETE + UNVERIFIABLE verdict shapes with their required-field lists + the save-verdict write-path; §15.5 the 10×/1× time-box defaults + the N=10 rationale; §15.6 worked examples; §15.7 self-referential observation. All anchors kept.
- **CUT (non-load-bearing):** §15.5's three-point "Rationale for N=10" can compress — the rule (10× default, 1× for UNVERIFIABLE, configurable per dispatch) is load-bearing; the three-paragraph justification (asymmetric cost / operator-fatigue / easy-escalation) compresses to a one-line rationale + the anchor (the full reasoning recovers via `bw show stoa--tp1`). §15.6 worked examples: the framework already notes the full six-example set lives in `bw show stoa--tp1`; the three inline examples are the load-bearing legibility set — KEEP all three but trim each example's prose to claim + quadrant + verdict + falsifying-evidence (drop the meta-commentary sentences). §15.7 self-referential observation compresses to 2 sentences.
- **Edit plan:** prose compression within §15.5/§15.6/§15.7 only; §15.1–§15.4 untouched (pure rule content). Est. −10 to −16 lines.

### 3.3 §24 — Arc-build branch hygiene (PLINY-primary; cross-ref)
ALREADY a thin cross-ref (the substantive canon lives at `MAJOR_PLINY.md` §5.9). Trim target = the "Why thin cross-ref" justification paragraph.
- **PRESERVED:** the two-check pre-branch rule (no other arc-build branch in flight; local main = origin/main); all five cross-reference bullets; the empirical anchors line.
- **CUT:** the "Why thin cross-ref, not full universal-team mirror" paragraph compresses to one sentence (only PLINY creates arc-build branches today; promote to full mirror if a future branch-creating seat appears). The rule itself is two bullets and stays verbatim.
- **Edit plan:** compress one paragraph. Est. −4 to −6 lines. NO relocation (already cross-ref; the canon home is MAJOR_PLINY).

### 3.4 §26 — Activation-paste cron hygiene (PLINY-primary + POLYBIUS; cross-ref)
ALREADY a thin cross-ref (canon at `MAJOR_POLYBIUS.md` §5.1.3). Same shape as §24.
- **PRESERVED:** the default-include rule (cron-hygiene preamble at top of every paste; activated session runs `CronList` then `CronDelete` any cron present); all cross-reference bullets; the `stoa--xyb.8.3` anchor.
- **CUT:** the "Why thin cross-ref" paragraph compresses to one sentence.
- **Edit plan:** compress one paragraph. Est. −4 to −6 lines. NO relocation.

### 3.5 §27 — Mechanical-script / agent-inspection split
**ALREADY a relocated module-stub** (`.claude/modules/mechanical-inspection-split.md`). The "trim" here is a stub-prose trim only.
- **PRESERVED:** the `Read .claude/modules/mechanical-inspection-split.md` pointer; the MODULE-INLINE markers (load-bearing for subproject recompose — must NOT be removed); the §0.5 relocation-index pointer; the CONDITIONAL trigger description.
- **CUT:** the stub currently enumerates "(incl. the §27.2 mechanical-script→inspection-agent→POLYBIUS-triage shape), the A7 boundary, per-seat behavior, the worked example, and cross-refs" — this contents-listing can compress to a shorter trigger clause; the module Read recovers the actual contents. Keep enough that the reader knows WHEN to read the module.
- **Edit plan:** compress the stub's contents-enumeration sentence. Est. −1 to −2 lines. Marker block untouched.

### 3.6 §31 — Substrate-component design principles
**ALREADY a relocated module-stub** (`.claude/modules/substrate-component-design.md`). Same as §27.
- **PRESERVED:** the Read pointer; MODULE-INLINE markers; §0.5 pointer; CONDITIONAL trigger.
- **CUT:** the "Covers Principle 1 (7-step agent-installable flow) + Principle 2 (composability-not-demo-inventory)" enumeration compresses to a shorter trigger clause.
- **Edit plan:** compress one sentence. Est. −1 line. Marker block untouched.

### 3.7 §34 — Trigger-payload authoring rule
Short inline section (already compact, ~16 lines).
- **PRESERVED:** the core RULE (every harness-owned trigger payload states inline (a) WHY it fired and (b) WHAT to do; NEVER a bare pointer); the why-pointers-fail-after-compaction reasoning (load-bearing — it is the *justification* that makes the rule stick); the `bw show stoa--xyb.5` enforcement-layer anchor; the `.claude/hooks/README.md` on-demand detail pointer.
- **CUT:** the second paragraph ("This is the load-bearing convention for the enforcement layer … fresh harness-fired input re-injected at the moment of action") restates the compaction reasoning already given in ¶1; compress to a one-clause cross-ref keeping the `bw show stoa--xyb.5` anchor. The "Shipped Arc 46 (debloat Arc 3, Stage 1)" provenance tag stays (one line).
- **Edit plan:** merge the two compaction-reasoning paragraphs into one. Est. −3 to −4 lines. **NOTE the dependency the ledger flags:** Arc C §7 (recurring cron-prompt) "depends on §34 trim from Arc B" — so the §34 trim must leave the trigger-payload rule intact and grep-findable for Arc C to build on. The trim does NOT touch the rule, only the duplicate justification. Safe.

**Trims summary:** 7 sections, est. total −28 to −44 lines (rev2: −3 to −5 lower than the prior estimate because the phantom §8.3 bidirectional-translation cut is dropped — §8 now trims only the §8.4 Arc-23 historical note + per-anchor narrative compression), **zero load-bearing rules dropped**. Two trims (§24/§26) are paragraph compressions of already-thin cross-refs; two (§27/§31) are already-relocated stub compressions; two (§8/§15) are the real body trims; one (§34) is a duplicate-justification merge. No NEW relocations to modules are needed (the ledger hinted "a couple trims relocate to modules" — but the relocatable sections §27/§31 are ALREADY relocated; nothing in the 7 needs a fresh module).

---

## §4 — The §32 STUB-PROSE CUT (markers + module source RETAINED)

### 4.1 Module-relocation confirmation
`substrate/modules/jsdom-timing-discipline.md` exists (3504 bytes) and carries the FULL discipline: the rAF-driven-timing failure mode, the 3-step test-authoring discipline, the disjunctive observable-end-state assertion, the `expectXHidden()` helper contract, the Pass-10 empirical anchor, and cross-refs. **The §32 stub's human-facing PROSE in op-disc is genuinely redundant** — its content is the module's; cutting the prose loses nothing. **The module source file and the MODULE-INLINE markers are NOT redundant** — see §4.2; they are load-bearing for subproject deploy and MUST survive.

### 4.2 The stub-prose cut + marker-retaining tombstone (install.sh Check A/B — LOAD-BEARING)

**This is a stub-PROSE cut, NOT a full delete. Two things MUST survive the cut, both verified against `substrate/install.sh` source (rev2 correction of the prior design's optional framing):**

1. **The module source `substrate/modules/jsdom-timing-discipline.md` MUST NOT be removed.** `install.sh` recompose **Check A** (install.sh:1025) fires `fail()` → `exit 2` if a MODULE-INLINE marker references a module with no source file at `${SRC_MODULES_DIR}/jsdom-timing-discipline.md`. Deleting the module source aborts the entire subproject deploy.

2. **The `<!-- MODULE-INLINE:jsdom-timing-discipline -->` … `<!-- /MODULE-INLINE:jsdom-timing-discipline -->` marker PAIR MUST stay in the §32 location.** `jsdom-timing-discipline` is in the `OPDISC_MODULES` owned-set (install.sh:1115) and is passed to `recompose_module_inline "$DEST_OPERATING_DISCIPLINES" "$OPDISC_MODULES"` (install.sh:1122). Recompose **Check B** (install.sh:1055) fires `fail()` → `exit 2` for any OWNED module that has no matching MODULE-INLINE marker in the deployed op-disc file ("body would be DROPPED at subproject tier"); the trailing handler (install.sh:1061–1062) then `rm`s the partial output AND the slim role file and aborts the deploy. **Dropping the markers HARD-ABORTS every subproject install.** The prior design's "case (b) — markers can be dropped" branch is NON-VIABLE and is removed; markers-in-tombstone is **MANDATORY, not a safe default**.

**The cut:** replace ONLY the §32 stub's redundant human-facing prose with a minimal tombstone heading, number preserved (Arc-A §21 precedent), with the marker pair retained intact and adjacent:

```markdown
## 32. [STUB-PROSE CUT — jsdom + animation timing discipline]

**Stub-prose CUT (Arc B, `stoa--xyb.13`).** The human-facing stub prose was redundant with the relocated module + the §0.5 relocation-index row and is cut. The full discipline lives at `.claude/modules/jsdom-timing-discipline.md` (rAF-driven-timing failure mode + disjunctive observable-end-state assertion + helper contract); read it directly or recover via the §0.5 index. The MODULE-INLINE marker pair below is **LOAD-BEARING and RETAINED** — `install.sh` recompose Check A/B (install.sh:1025/1055) hard-abort the subproject deploy if the marker pair or the module source `substrate/modules/jsdom-timing-discipline.md` is missing; do NOT remove either. Number preserved as a stable cross-reference key (do NOT renumber).

<!-- MODULE-INLINE:jsdom-timing-discipline -->
<!-- /MODULE-INLINE:jsdom-timing-discipline -->
```

The marker pair stays an empty open/close adjacency (no body between them) at user/project tier — `install.sh` re-inlines the module body between them at subproject tier (the same idempotent recompose mechanism §27/§31 rely on). ADA must NOT delete the markers and must NOT delete the module source; this is now a build INVARIANT, not a build-time question.

### 4.3 §0.5 index row update
Baseline row (line 65):
```
| §32 jsdom + animation timing discipline | `.claude/modules/jsdom-timing-discipline.md` (disk module; subproject recompose) | CONDITIONAL |
```
Update to reflect the **stub-prose cut with markers retained** (NOT a full CUT — the module is still a live subproject-recompose target, so the class stays CONDITIONAL, not CUT):
```
| §32 jsdom + animation timing discipline (Arc B `stoa--xyb.13`: stub-prose cut, MODULE-INLINE markers retained) | `.claude/modules/jsdom-timing-discipline.md` (disk module; subproject recompose) | CONDITIONAL |
```
The index row stays (it is the audit-time recovery pointer). The class stays **CONDITIONAL** — flipping it to CUT (as the prior design proposed, mirroring the §21 CUT row) would be wrong: §21 is a genuine full delete, whereas §32 keeps the module + the live recompose markers. The only change is the note that the human-facing stub prose was cut while the marker block survives.

### 4.4 Inbound §32 reference re-point scan
`grep -rn '§32' substrate/ --include='*.md'` excluding `substrate/arcs/` returns these live refs (the floor-manager expected ~3 CAPTAIN-file re-points; actual breakdown below):

| Locus | Current text | Re-point handling |
|---|---|---|
| `CAPTAIN_ADA.md:189` (cite comment) | `operating-disciplines.md §32 — test-environment sibling (jsdom + animation libraries…)` | Re-point to `.claude/modules/jsdom-timing-discipline.md` (the module is now the canonical home). |
| `CAPTAIN_ADA.md:192` (bullet) | `operating-disciplines.md §32 (test-environment sibling — jsdom + animation libraries…)` | Re-point to `.claude/modules/jsdom-timing-discipline.md`. |
| `modules/jsdom-timing-discipline.md:46` (cite comment) | `VERA reads §32 when designing probes…` | Re-point the §32 mention → "VERA reads this module when designing probes…" (the module shouldn't point at its own deleted source-stub). |
| `modules/jsdom-timing-discipline.md:49` (bullet) | `VERA reads §32 when designing probes…` | Same re-point as :46. |
| `operating-disciplines.md:65` (§0.5 row) | the index row | Handled in §4.3 (becomes the CUT row). |

**NOT re-pointed (provenance — keep):** `modules/jsdom-timing-discipline.md:3` and `:6` say "Relocated from `operating-disciplines.md` §32" — that is **historical provenance** (where it came from), not a live pointer to read; KEEP verbatim. Same B-LEAVE principle as Arc A (don't scrub the substrate's own history).

**Total live re-points: 4** (2 in CAPTAIN_ADA.md, 2 internal to the module) + 1 index-row note update (NOT a class-flip — the class stays CONDITIONAL, §4.3). The floor-manager's "~3 CAPTAIN cross-refs" estimate is close — the actual CAPTAIN-file count is 2 (both in ADA); the other 2 are module-internal self-references that would dangle if not fixed. **After re-point: zero live `§32` references resolve to a deleted target** (only the `## 32. [STUB-PROSE CUT —` tombstone heading + the retained MODULE-INLINE marker pair + the two provenance "relocated from §32" mentions remain, all intentional).

---

## §5 — VERA probes

All probes run against the worktree `arc-B/build` post-build. Probe artifacts use fixed literal paths (no `$VAR` in any destructive op; these are read-only greps/diffs — no destructive ops at all). Baseline ref = commit `1cb9160`.

**P1 — Merged-rule survival (every merged rule grep-findable in §1).** For each of the 12 enumerated rules in §2.3, grep the merged §1 body (lines from `## 1.` to the next `## 2.`) for a distinctive phrase:
```bash
sed -n '/^## 1\./,/^## 2\./p' substrate/operating-disciplines.md > /tmp/stoa-merged-s1.txt
grep -q 'story the model tells itself' /tmp/stoa-merged-s1.txt   # 1b
grep -q 'minimize agent round-trips by cutting verification is a category error' /tmp/stoa-merged-s1.txt  # 2b
grep -q 'never about polishing PROCESS\|polishing the process is free' /tmp/stoa-merged-s1.txt  # 3c
grep -q 'flag the citation as unverified and return' /tmp/stoa-merged-s1.txt  # 5b
grep -q 'POLYBIUS §4.3 / PLINY §7.2' /tmp/stoa-merged-s1.txt  # 5c both-apply distinction
```
Acceptance: all 12 distinctive phrases present in the merged-§1 slice. (VERA: full 12-phrase list is the §2.3 table left column → pick one distinctive token per row.)

**P2 — §4 standalone untouched (byte-identical to baseline).**
```bash
git show 1cb9160:substrate/operating-disciplines.md | sed -n '/^## 4\. Suppress "wait for explicit/,/^## 5\./p' | sed '$d' > /tmp/stoa-s4-base.txt
sed -n '/^## 4\. Suppress "wait for explicit/,/^## 5\./p' substrate/operating-disciplines.md | sed '$d' > /tmp/stoa-s4-now.txt
diff /tmp/stoa-s4-base.txt /tmp/stoa-s4-now.txt
```
Acceptance: empty diff. (The `sed '$d'` drops the trailing `## 5.` boundary line so the comparison is §4-body-only; if §5's heading changed to a stub the boundary token `## 5.` still matches.) NOTE: if the §5-stub heading text differs from baseline `## 5. Suppress plausible-source…`, the range terminator still fires on `## 5.` — verify the §4 body bytes, not the terminator.

**P3 — Per-trim load-bearing-rule survival.** One grep per trimmed section's load-bearing rule:
```bash
grep -q 'positive references only\|Reference only POSITIVE' substrate/operating-disciplines.md   # §8.1
grep -q 'quadrant classification' substrate/operating-disciplines.md                              # §15.2
grep -q 'No other arc-build branch in flight' substrate/operating-disciplines.md                  # §24
grep -q 'CronList' substrate/operating-disciplines.md && grep -q 'CronDelete' substrate/operating-disciplines.md  # §26
grep -q 'mechanical-inspection-split.md' substrate/operating-disciplines.md                       # §27 stub pointer
grep -q 'substrate-component-design.md' substrate/operating-disciplines.md                         # §31 stub pointer
grep -q 'state, self-contained inline\|WHY.*it fired.*WHAT to do\|NEVER a bare pointer' substrate/operating-disciplines.md  # §34
```
Acceptance: all present. PLUS: each trimmed section's MODULE-INLINE marker pairs (§27/§31) still balanced:
```bash
grep -c 'MODULE-INLINE:mechanical-inspection-split' substrate/operating-disciplines.md   # expect 2
grep -c 'MODULE-INLINE:substrate-component-design' substrate/operating-disciplines.md     # expect 2
```

**P4 — §32 no-dangling-ref.** After the stub-prose cut + re-points, no live `§32` pointer resolves to a deleted target:
```bash
grep -rn '§32' substrate/ --include='*.md' | grep -v 'substrate/arcs/'
```
Acceptance: the ONLY remaining `§32` mentions are (a) the `## 32. [STUB-PROSE CUT —` tombstone heading, (b) the §0.5 index row (CONDITIONAL, note-updated), (c) the two `Relocated from … §32` provenance lines in the module. ZERO live "read §32 for X" pointers. Specifically: `CAPTAIN_ADA.md` has zero `§32` after re-point (both now point at the module); module lines 46/49 no longer say "reads §32".

**P4b — §32 subproject-deploy safety: MODULE-INLINE marker pair PRESENT + module source exists (LOAD-BEARING — install.sh Check A/B).** The stub-prose cut MUST NOT drop the marker pair or the module source, or subproject deploy hard-aborts (install.sh:1025/1055 → exit 2). Assert both survive:
```bash
# (i) the OPEN+CLOSE marker pair is present in the deployed/source op-disc §32 location (Check B):
grep -c '^<!-- MODULE-INLINE:jsdom-timing-discipline -->$' substrate/operating-disciplines.md      # expect 1 (open)
grep -c '^<!-- /MODULE-INLINE:jsdom-timing-discipline -->$' substrate/operating-disciplines.md     # expect 1 (close)
# (ii) the module SOURCE file still exists (Check A):
test -f substrate/modules/jsdom-timing-discipline.md && echo PRESENT
# (iii) end-to-end: a subproject dry-run recompose does NOT abort (the strongest proof):
bash substrate/install.sh --dry-run --target subproject --parent-dir /tmp/stoa-rev2-parent --subproject probe 2>&1 | grep -iE 'jsdom-timing|error: recompose' ; echo "exit=$?"
```
Acceptance: (i) exactly 1 open + 1 close marker line in op-disc; (ii) module source PRESENT; (iii) the dry-run recompose plan references jsdom-timing WITHOUT a `error: recompose:` Check-A/B abort line (no `exit 2`). This probe is the subproject-deploy-safety guard that the prior design left as an un-inspected build-time question — rev2 makes it a hard VERA assertion. (VERA: a real `--target subproject` recompose, not dry-run, is the gold check if the parent fixture is available; the dry-run plan is the floor.)

**P5 — No-renumber (section sequence stable).** The heading sequence §1…§36 is unbroken except the merged/cut heading FORMS:
```bash
grep -nE '^## [0-9]+[.\[]' substrate/operating-disciplines.md | grep -oE '## [0-9]+' | grep -oE '[0-9]+' > /tmp/stoa-secnums.txt
# expect: 1,2,3,4,5,6,7,8,9,...,36 present (each once); 2/3/5/32 present as stub/tombstone forms
```
Acceptance: every integer 1–36 appears exactly once as a `## N` heading; none skipped, none duplicated, none renumbered. The "Agent-regime inverses" line no longer says "six anti-patterns above" dangling a count (grep the updated phrasing).

**P6 — Authorship unchanged.** No author-like field touched:
```bash
git diff 1cb9160 -- substrate/operating-disciplines.md substrate/CAPTAIN_ADA.md substrate/modules/jsdom-timing-discipline.md | grep -iE '^[+-].*(author|owner|creator|maintainer|copyright|holder|vendor|publisher)' | grep -vE 'Co-Authored-By: CAPTAIN_DAEDALUS'
```
Acceptance: empty (no author-field lines added or removed; the only Co-Authored-By is the seat trailer on the commit, not a file-content change).

**P7 — Net-negative lines (debloat sanity).**
```bash
git diff --stat 1cb9160 -- substrate/operating-disciplines.md
```
Acceptance: net deletions > net insertions for op-disc (debloat invariant). Expect roughly −28 to −48 net on op-disc (rev2: floor lowered from the prior −35 to −55 because the §8.3 phantom cut is dropped AND the §32 change is a prose-cut-to-tombstone that retains the heading + marker pair rather than a clean delete — both add a handful of lines back vs the prior design's assumptions). The debloat invariant (net-negative) still holds; magnitude is secondary to losslessness. (CAPTAIN_ADA.md re-points are net-neutral; the module re-points are net-neutral.)

---

## §6 — Threat classification (§6.12 / A3)

**Proposed: NOT threat-ratified (process / substrate-canon prose change, no runtime mechanism, no attack path).** Per `operating-disciplines.md` §35.5, this arc edits substrate canon PROSE — it merges four advisory anti-pattern stances, compresses provenance narration in seven sections, and deletes a redundant documentation stub. There is no runtime mechanism, no credential flow, no input-handling surface, no security mitigation, and therefore no attack path. No A3 `M<n> → attack-path → how-defeated` map is required, and no threat-anchored probe (§6.13) applies — the §35.5 self-carve-out covers it: the layer verifies named-threat COVERAGE, and this change names no threat.

**I am the upstream classifier proposing this carve-out; I cannot self-grant it.** ARGUS CONFIRMS at critique time. The honest residual: the §34 trim feeds Arc C's enforcement-layer work (cron-prompt triggers), but Arc B itself only preserves the §34 rule — it ships no trigger mechanism. If ARGUS reads the §34/Arc-C dependency as security-adjacent, I defer to ARGUS's classification.

---

## §8 — Self-assessed weak points

- **weak_point:** The merge's line-count win is near-flat at the merged-§1 locus (four 4-line stances → one ~30-line section); a reviewer expecting a large negative delta FROM THE MERGE could read it as "consolidation that didn't consolidate." **why_this_shape_anyway:** The merge's value is coherence (four scattered stances become one teachable "human-team stories that invert" section), not line-count; the negative delta lives in §3 trims + §4 cut. Stated explicitly in §2.4 so the reviewer's expectation is set correctly. The alternative (cramming all four stances into one dense paragraph to maximize line-cut) would sacrifice the per-stance grep-findability that §8.7 requires — rejected.

- **weak_point:** "Redundant" in the §8.4/§15/§34 trims is a judgment call — e.g. §8.4's Arc-23 historical implication note, or §34's second compaction paragraph. A reviewer could judge one of these as load-bearing emphasis rather than redundancy. **why_this_shape_anyway:** I marked each CUT with its surviving canonical home (§8.4's discipline + anchor survive in ¶1 of §8.4; §34's reasoning survives in ¶1) so the rule is never dropped, only de-duplicated; if ARGUS disagrees on a specific CUT, the fix is "keep that paragraph" — a trim-back, not a re-architecture. (rev2: the §8.3 bidirectional-translation CUT that the prior design flagged here was a PHANTOM — that text is not in §8.3; the cut is dropped entirely, §8.2/§8.3 are untouched.) Listed as `residual_questions_for_argus`.

- **weak_point:** (rev2 — RESOLVED, was the prior design's top weak point) The §32 MODULE-INLINE marker handling is no longer a question: it is a verified build INVARIANT. `jsdom-timing-discipline` is in `OPDISC_MODULES` (install.sh:1115) and install.sh recompose Check A (install.sh:1025, module source) + Check B (install.sh:1055, OWNED marker) hard-abort the subproject deploy (`exit 2`, install.sh:1061–1062) if either the marker pair or the module source is dropped. **why_this_shape_anyway:** The design now mandates markers-in-tombstone + module-source-retained (§4.2) and probes both presence + a dry-run recompose that must not abort (P4b). The prior design's "case (b) — drop the markers" branch is removed as non-viable. No residual question remains here.

- **weak_point:** The ledger's trim list assumed full bodies for §27/§31/§24/§26, but the actual file state is already-relocated-stubs / thin-cross-refs, so the realizable trim from those four is small (paragraph compressions). The arc's losslessness is safe but its debloat magnitude is smaller than a naive read of the ledger implies. **why_this_shape_anyway:** Losslessness is the locked bar; magnitude is secondary. I restated the actual state in §1 + §3 so no downstream seat builds against the stale "full bodies" assumption. Net is still negative (§8/§15 bodies + §32 cut carry it).

---

## Verdict block

```
status: completed
ticket: stoa--xyb.13
verdict: pass
design_artifact_path: agents/design/stoa--xyb.13/design.md
restatement: Merge the four non-contiguous anti-pattern stances (§1/§2/§3/§5, §4 carved out and untouched) into one section at §1 with pointer-stubs for the vacated numbers; losslessly trim seven sections (§8/§15/§24/§26/§27/§31/§34) keeping every load-bearing rule; cut the redundant human-facing PROSE of the §32 jsdom stub to a tombstone while RETAINING the MODULE-INLINE marker pair + the module source (both load-bearing for subproject deploy per install.sh Check A/B), update the §0.5 index row note (class stays CONDITIONAL), and re-point inbound §32 refs — all no-renumber, authorship unchanged.
self_assessed_weak_points:
- weak_point: merge's line win is near-flat at the merge locus (coherence win, not line-cut win)
  why_this_shape_anyway: negative delta lives in trims+cut; per-stance grep-findability (§8.7) beats a dense single paragraph
- weak_point: "redundant" in the §8.4/§15/§34 trims is a judgment call
  why_this_shape_anyway: every CUT names its surviving canonical home so no rule drops; disagreement is a trim-back not a re-architecture
- weak_point: §27/§31/§24/§26 are already stubs/thin-refs so realizable trim is small
  why_this_shape_anyway: losslessness is the locked bar; net stays negative via §8/§15 bodies + §32 prose cut
residual_questions_for_argus: (1) Confirm the §35.5 NOT-threat-ratified carve-out (process/canon prose, no runtime/attack path). (2) For the §8.4 Arc-23 historical note and §34 second paragraph CUTs — is either load-bearing emphasis rather than redundancy? (3) Should the line-1642 "six anti-patterns above" rewrite count §1's four sub-stances + §4 + §6, or is a different framing cleaner? (rev2 note: the prior r1 question — "does install.sh recompose jsdom-timing at subproject tier" — is RESOLVED to YES at the source by ARGUS and re-verified here; markers-in-tombstone + module-source-retained is now a hard build invariant, §4.2 + P4b. The prior r2 phantom §8.3 cut is DROPPED.)
summary: Arc B is a lossless-on-canon consolidation of operating-disciplines.md. The primary artifact merges the four non-contiguous anti-pattern stances (§1/§2/§3/§5) into one section at §1 — passivity (§4) carved out and kept byte-identical because it is the most-violated stance — with §2/§3/§5 becoming no-renumber pointer-stubs; a full rule-by-rule preservation map shows all 12 enumerated rules surviving (shared human-team framing de-duplicated, no rule dropped). Seven trims compress provenance narration and duplicate justification while keeping every load-bearing rule grep-findable (§8/§15 are the real body trims; §24/§26/§27/§31 are already-thin and yield paragraph compressions; §34 merges a duplicate justification and preserves the rule Arc C depends on). rev2 surgical corrections to two ARGUS BLOCKING findings: (r1) the §32 jsdom change is a STUB-PROSE cut, NOT a full delete — the MODULE-INLINE marker pair and the module source are RETAINED because install.sh recompose Check A (install.sh:1025) + Check B (install.sh:1055) hard-abort the subproject deploy (exit 2) if either is dropped (jsdom-timing is in OPDISC_MODULES, install.sh:1115); §0.5 row stays CONDITIONAL (note-updated, not flipped to CUT); a new probe P4b asserts the marker pair present + module source exists + a dry-run recompose that does not abort. (r2) the prior design's §8.3 bidirectional-translation CUT targeted a phantom — that restatement is not in §8.3 (the principle lives at thesis line 29 + §8.2 line 228, its canonical home); §8.3 is the all-load-bearing four-state continuum, so the §8 bidi cut is DROPPED entirely and §8.2/§8.3 are untouched. The load-bearing structural choice is merge-into-§1; the four-stance merge, §4 carve-out, line-1642 rewrite, the §15/§24/§26/§27/§31/§34 trims, and no-renumber all PASSED ARGUS and are unchanged.
follow_ups:
- Arc C (§7 cron-prompt) depends on the §34 trim leaving the trigger-payload rule grep-findable — verified preserved here; Arc C can build on it.
- The "six anti-patterns above" framing at line 1642 is a maintenance hazard whenever the head-of-file stance count changes; consider rephrasing to not hard-code a count.
gap_or_blocker: (none)
```
