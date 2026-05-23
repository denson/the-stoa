# Arc 6 (Arc 49) — CAPTAIN_DAEDALUS.md debloat cut — design rev1

**Ticket:** stoa--xyb.11 (engagement epic stoa--xyb)
**Author:** Denson Smith (the PRINCIPAL — design synthesis, structural choices, relocation ledger)
**Seat:** CAPTAIN_DAEDALUS_the-stoa
**Builds on:** Arc 44 (composition-layer mechanism: `substrate/modules/` glob deploy + `modules/README.md` 3 channels / 3 relocation classes + op-disc §33 thin rule); Arc 45 (MAJOR_POLYBIUS.md cut — the PROVEN stub/marker/recompose pattern + `recompose_module_inline()` shipped data-driven); Arc 47 (operating-disciplines.md cut — the **index-ONLY non-orchestrator shape** + the SPECIFICATION.md exact-heading-preserve discipline + the **two-set MODULE-OWNERSHIP partition**, Check A global / Checks B/D owned); Arc 48 (MAJOR_PLINY.md cut — the **THIRD owned-set** + **P-OWNERSHIP-NOCOLLIDE** basename-disjointness probe; shipped at install.sh L894–1009).
**Acceptance bar:** LOSSLESS-ON-CANON at ALL tiers (user / project / subproject). CAPTAIN_DAEDALUS.md is the ARCHITECT role file (a CAPTAIN sub-agent envelope) — it deploys at all three tiers via the `CAPTAIN_NAMES` deploy loop (install.sh L1021), suffixed at subproject (`CAPTAIN_DAEDALUS_<subproject>.md`, L1023). ARGUS's primary audit target is LOST CANON for the architect seat.
**Recalibrated criterion (PRINCIPAL-ratified, carried from Arc 47/48):** the lossless-floor is an OUTPUT measured per file, NOT a fixed line target. Falsify on LOSSLESS-COMPLETENESS (every chunk homed + recoverable), NOT a line number. Do NOT cut a load-bearing always-on architect rule to hit a number. The empirical post-cut floor is REPORTED (§3.10), not targeted.

This is the **4th and LAST relocation cut** of the debloat epic (POLYBIUS / op-disc / PLINY done; after this, only the capstone block — stoa--xyb.9 prose-compression + the .9/3na/final-redeploy work). The method (3-bucket relocation), the marker/stub mechanism, the subproject-recompose, the SPECIFICATION.md exact-heading-preserve, and the multi-owner ownership partition are ALL proven. This design REUSES them; it does not re-derive them. The DAEDALUS-specific work is: (a) the ambient-vs-conditional classification for a CAPTAIN role file whose entire CONDITIONAL bulk is concentrated in ONE section (§6 Disciplines); (b) extending install.sh's already-partitioned recompose to a FOURTH owned-set (`DAEDALUS_MODULES`) — with the path-construction wrinkle that DAEDALUS has NO standalone `DEST_*` var (it deploys inside the `CAPTAIN_NAMES` loop); (c) the index-ONLY shape (DAEDALUS is a non-orchestrator CAPTAIN, like op-disc — confirmed against modules/README §4.1).

---

## §1 — Problem restatement (pre-work gate)

`substrate/CAPTAIN_DAEDALUS.md` is **633 lines** — the ARCHITECT role file, dispatched one-shot by MAJOR_PLINY at the head of the gauntlet pipeline. Like the three cuts before it, it grew by empirical-anchor + discipline accretion: §6 ("Disciplines specific to this seat") expanded across arcs into **twelve subsections** (§6.1–§6.11 with several primed variants §6.2.1', §6.9.3', §6.9.3''), and §6 alone is **511 of the 633 lines (81%)**. Most of those subsections are **design-task-type-specific procedures DAEDALUS uses only for a particular KIND of design** — the canonical-code-block-fix discipline (§6.2.1') fires only when a self-catch names a defect in a code design; the credential-flow discipline (§6.6) fires only on credentialed-ops designs; the PRINCIPAL-gate discipline (§6.7) fires only on directive/spec designs with gating clauses; the canonical-template-alignment discipline (§6.8) fires only when a design carries two-or-more inline template copies; the probe-grounding cluster (§6.9 / §6.9.3' / §6.9.3'') fires only when a design authors verification probes; the SSoT-with-WHY discipline (§6.10) fires only on qualitative-acceptance-body designs; the API-docs-don't-generalize discipline (§6.11) fires only on third-party-API designs. None of these is read on EVERY design dispatch. Each carries a multi-paragraph "Empirical anchor" + "Cross-refs" tail (the why-record, read only when someone asks why the rule exists).

The *actionable always-on* architect core — what DAEDALUS needs on every design dispatch — is the seat identity (§1 one-job, §2 brief-shape, §5 voice), the **design-output contract** (§3 what-you-write-to-disk + §4 what-you-do-NOT-write), the **two load-bearing gates** (§6.1 restatement pre-work gate + §6.2 self-assessed-weak-points post-work gate), the always-on cross-cutting reflexes (§6.3 consume-research, §6.4 WebSearch-live-constraints, §6.5 heartbeat-bw), and the closeout machinery (§7 verdict format + §8 authorship + §9 when-wrong). That core is roughly a fifth of the lines. The rest is §6's design-task-type-specific disciplines (CONDITIONAL → disk module) plus the embedded empirical why-record (PROVENANCE → bw cite, travelling WITH the relocated discipline into its module).

This arc applies the proven 3-relocation-class method (CONDITIONAL → disk module; PROVENANCE → bw cite; DUPLICATE → pointer) to CAPTAIN_DAEDALUS section by section, **for the whole file**, and extends the multi-owner subproject-recompose to cover CAPTAIN_DAEDALUS as the FOURTH recompose source (`DAEDALUS_MODULES`). The KEEP bucket is the always-on architect core; the RELOCATE buckets are §6's design-task-type-specific disciplines + their embedded empirical record.

### 1.1 Imported assumptions (named per §6.1 of the seat envelope — real briefs have implicit scope)

1. **DAEDALUS is a CAPTAIN (architect), NOT an orchestrator — it gets a RELOCATION INDEX ONLY, no routing map.** This is the load-bearing structural call, and it follows the Arc-47 op-disc precedent, NOT the Arc-45/Arc-48 orchestrator precedent. **Basis (modules/README.md §4.1 + §1):** the routing map is an ORCHESTRATOR artifact — it answers "*at dispatch time, what does this task need?*" (§4.1: "Columns: task-type → module(s) to load → channel"), consulted by the seat that COMPOSES a dispatch payload (POLYBIUS / PLINY). modules/README §1 is explicit: "A module is NOT ... the routing map or relocation index themselves (those stay inline in **orchestrator core**)." DAEDALUS dispatches NOTHING — it has no `Agent` tool (the file's own §4 + §6.5 state this: "sub-agents cannot dispatch sub-agents," `Monitor`/`run_in_background` forbidden). DAEDALUS's CONDITIONAL modules are read BY DAEDALUS ITSELF at the moment it hits a particular design-task-type (it reads `credential-flow-design.md` when the brief involves credentialed ops; `probe-grounding.md` when it authors probes). So DAEDALUS carries the relocation index (the losslessness-recovery artifact ARGUS audits) but NO routing map — the per-stub `Read` pointer at each §6.x stub IS the dispatch-time signal, inline at the point of need. This is structurally identical to op-disc (Arc 47, ARGUS Q1 CONCUR): a non-orchestrator file whose CONDITIONAL content is read by the seat-at-point-of-need, not dispatched. **(Surfaced as residual Q1 — confirm the CAPTAIN-gets-index-only call, since this is the first CAPTAIN role file cut and the precedent is op-disc-the-universal-layer, not a prior CAPTAIN.)**

2. **CONDITIONAL content relocates to NEW disk modules under `substrate/modules/`** alongside the 5 POLYBIUS + 12 op-disc + 11 PLINY modules + README (28 module sources today). This arc CREATES + POPULATES the new DAEDALUS modules. Naming + per-module contents are in §2.3. Module basenames are checked against the existing 28 for NO collision (assumption 3; §3.8).

3. **The shared `substrate/modules/` dir is ALREADY a multi-owner partition (Arc 47 two-set + Arc 48 third owner); this arc adds the FOURTH owned-set.** `recompose_module_inline()` (install.sh L895–998) already takes `(role_file, owned_basenames)` and passes the awk TWO `-v` lists: a GLOBAL existence set (Check A, owner-agnostic, from the filesystem glob) and a per-call OWNED set (Checks B/D). Arc 47 wired POLYBIUS's 5 + op-disc's 12; Arc 48 added PLINY's 11. This arc adds `DAEDALUS_MODULES` (the per-call owned-set for the DAEDALUS file) + a fourth call. **The two-set discipline HOLDS unchanged: the DAEDALUS owned-set must NOT narrow Check A's global-existence test, and must NOT collide with the POLYBIUS / op-disc / PLINY owned-sets** (P-OWNERSHIP-NOCOLLIDE across all FOUR owner-sets — extended from Arc 48's three-owner version). **Zero function-body change** — the recompose is data-driven (Arc 47 design's "data-driven property" claim, re-confirmed in Arc 48). The ONE wrinkle (§2.7.2 / §6): DAEDALUS has no standalone `DEST_DAEDALUS` var — it deploys in the `CAPTAIN_NAMES` loop (L1021–1034), so the fourth recompose call needs the DAEDALUS deploy path CONSTRUCTED (either a `DEST_DAEDALUS` var set when the loop deploys DAEDALUS, or the path rebuilt at the call site).

4. **CAPTAIN_DAEDALUS deploys at ALL three tiers** (user / project / subproject), suffixed at every tier via the `CAPTAIN_NAMES` loop (install.sh L1021–1034: `dest="${DEST_AGENTS_DIR}/CAPTAIN_${name}${NAME_SUFFIX}.md"`; at subproject tier `NAME_SUFFIX=_<subproject>`, so the deployed file is `CAPTAIN_DAEDALUS_<subproject>.md` under the subproject's `.claude/agents/`). At subproject tier the modules dir is NOT deployed (`DEST_MODULES_DIR=""`) AND a subproject seat's `Read .claude/modules/X.md` does not resolve reliably (the Arc-45 probe finding, claude-code #56686/#31546/#29423). So a slim subproject CAPTAIN_DAEDALUS pointing at modules absent from the subproject's `.claude/` would break losslessness for the architect seat at that tier. The fix is the same recompose-inline the other three files use — DAEDALUS's recompose call runs on the suffixed deployed file inside the existing `if [ "$TARGET" = "subproject" ]` block, AFTER the `CAPTAIN_NAMES` loop has written `CAPTAIN_DAEDALUS_<subproject>.md`. **Note:** the recompose block (L894) currently runs BEFORE the CAPTAIN deploy loop (L1014–1037) — so the fourth call requires either reordering (deploy CAPTAINs before the recompose block) OR moving the DAEDALUS recompose to after the loop. §6.5 specifies the placement.

5. **Section numbers AND any cross-ref-cited subsection-heading lines are PRESERVED via stubs, NOT renumbered.** The live cross-ref census (§3.1, grepped this design phase across `substrate/` with a BACKTICK-TOLERANT pattern — the naive `\.md\s+§` regex MISSES the common `` `CAPTAIN_DAEDALUS.md` §6.7 `` form where a backtick sits between `.md` and the space) shows the `CAPTAIN_DAEDALUS.md §N` cites from active substrate files are **§6 (top-level), §6.7, §6.8, §6.9, §6.9.3'', §6.11** (from CAPTAIN_ADA, CAPTAIN_VERA, operating-disciplines.md, the op-disc-owned `mechanical-inspection-split.md` module, AND the validate-spec skill which cites §6.9 EIGHT times across its `.py`/`.sh`/SKILL.md files — §6.9 is the most heavily externally-cited DAEDALUS subsection). All are sibling-discipline / tooling cross-refs. **SPECIFICATION.md L553 references `CAPTAIN_DAEDALUS.md §6.8` in prose but the validate-spec resolver does NOT pick it up** (the same backtick-form issue; confirmed live, §3.1.2). Every relocated §6.x section leaves a numbered stub so the substrate-file `CAPTAIN_DAEDALUS.md §6.x` cites still resolve to a real heading line (the Arc-47 r1 discipline applied to the substrate-cite resolution, even though no SPEC resolver cite is at risk here).

6. **CAPTAIN_DAEDALUS has an author-relevant frontmatter `name:` field but NO author-like field; the new modules must carry none** (P-AUTH guards). The YAML frontmatter (`name:`, `description:`, `tools:`, `model:`) is preserved verbatim in the slim core — it is the sub-agent envelope contract, NOT relocatable. DAEDALUS's content — the synthesis — is the PRINCIPAL's per the immutable authorship rule (§8 is itself the authorship-attribution section, KEEP); cited empirical anchors are attributed to their tickets, which is source-citation not authorship.

The restatement converges with the brief. The places it does more than paraphrase: (a) assumption 1 — the index-ONLY call for a CAPTAIN, which the brief flagged for confirmation against modules/README §4.1 (I confirm: index-only, basis above); (b) assumption 3's wrinkle — the no-`DEST_DAEDALUS`-var path-construction detail, which the brief named ("DAEDALUS deploys to all tiers, suffixed") and which I surface as the one genuinely-new install.sh mechanic beyond the proven Arc-48 fourth-call pattern (surfaced as residual Q3); (c) the **recursion note** — DAEDALUS designs the cut of its OWN role file. Per the brief this needs NO special handling: the live agent loads from the DEPLOYED (full, pre-cut) role file, not redeployed until engagement-end, so DAEDALUS's identity is stable while it edits the source. I used the full DAEDALUS envelope (its §6.1 restatement gate, §6.2 self-assessed-weak-points gate, §6.5 heartbeat) to design this cut — the recursion is an authoring convenience, not a correctness hazard.

---

## §2 — Approach (the slim structure)

### 2.1 The slim core shape

Post-cut, `substrate/CAPTAIN_DAEDALUS.md` is the **slim always-on architect core**: the YAML frontmatter (verbatim) + the role-identity header table + §1 (one job) + §2 (the brief) + §3 (what you write to disk — the design-output contract) + §4 (what you do NOT write) + §5 (voice) + §6 slim (the §6.1 restatement gate + §6.2 self-assessed-weak-points gate KEPT inline, with the design-task-type-specific §6.2.1' / §6.6 / §6.7 / §6.8 / §6.9 / §6.9.3' / §6.9.3'' / §6.10 / §6.11 relocated to modules + numbered stubs, and the always-on §6.3 / §6.4 / §6.5 reflexes KEPT inline) + §7 (verdict format, KEEP) + §8 (authorship attribution, KEEP) + §9 (when this file is wrong, KEEP) + ONE always-loaded **relocation index** (the losslessness-recovery artifact; NO routing map — DAEDALUS is not an orchestrator). The CONDITIONAL design-task-type disciplines move to disk modules; their embedded empirical why-record moves WITH them into the module (the `Anchor:` compresses inside the module body); there are NO DUPLICATE relocations (§3.5).

### 2.2 The always-loaded RELOCATION INDEX (no routing map — DAEDALUS is not an orchestrator)

Per modules/README.md §4, the composition layer pairs a routing map (dispatch-time) with a relocation index (audit-time). **DAEDALUS gets ONLY the relocation index** (assumption 1; the Arc-47 op-disc shape). The index is added as a new **§6.0 "Relocation index (audit-time — where relocated §6 disciplines went)"** placed at the TOP of §6, immediately after the §6 heading and before §6.1, so the always-loaded recovery table sits at the head of the Disciplines section it indexes. It uses the regular index column shape from modules/README.md §4.2 (relocated-content → new-home → class) so a future enforcement-layer hook is parseable. The index is populated in §3 of THIS design.

**Why no routing map (the index-vs-routing-map call — confirmed against modules/README §4.1):** the routing map answers "at dispatch time, what module does this task need?" — an orchestrator question. DAEDALUS dispatches nothing (no `Agent` tool; §3/§4/§6.5 of the source state the runtime constraint `u--7yg.12`). The dispatch-time signal a reader needs ("this design touches credentialed ops → read `credential-flow-design.md`") lives INLINE at the §6.x stub, at the point of need, because the reader arriving at DAEDALUS §6.6 IS DAEDALUS, mid-design, having just recognized a credentialed-ops brief. Putting a routing map in DAEDALUS would duplicate the per-stub pointers into a table no orchestrator consults (DAEDALUS does not consult a "beat → module" table — it has no dispatch beats; it has design-task-type recognitions, which the stubs encode at point-of-need). The stubs ARE the routing, distributed to point-of-need. This is the identical reasoning ARGUS CONCURRED for op-disc (Arc 47 Q1). The single distinction from op-disc: op-disc is the universal layer EVERY seat reads, whereas DAEDALUS is read only by the DAEDALUS seat — which makes the index-only call even cleaner here (there is exactly ONE reader, and that reader is the one hitting the design-task-type triggers). **(Residual Q1: this is the first CAPTAIN role file cut; confirm the CAPTAIN-non-orchestrator → index-only generalization holds and should be the standard shape for the future CAPTAIN cuts ARGUS/ADA/VERA/CATO etc.)**

### 2.3 The CONDITIONAL module files (CREATED + POPULATED this arc) — 9 modules

Each module is a self-contained reference body; the module's first line is a stable `# <Title>` heading (the recompose keys on it; P-RECOMPOSE asserts it appears) followed by a provenance header citing this design + the stoa--xyb epic (mirroring modules/README.md:14–16 + the Arc-47/Arc-48 modules). **No module carries an author-like field** (P-AUTH). Line ranges are grounded against the LIVE source (re-read this design phase, §3 §-map). Module basenames are checked against the existing 28 (5 POLYBIUS + 12 op-disc + 11 PLINY) for NO collision (§3.8).

| Module file | Source § (live line range) | What moves in |
|---|---|---|
| `substrate/modules/canonical-code-block-fix.md` | §6.2.1' (108–158) | The fix-location discipline (fix lands at the §2.X canonical code-block ADA reads first, not only at a §11 step-list or §6 flag) + the 3-step discipline + the 4-anchor empirical block (Arc 3 r1 / rev2 o1 / VERA Probe L / Arc 4 WP13) + the cross-refs. Fires only when a §6.2 self-catch names a defect in a CODE design. |
| `substrate/modules/credential-flow-design.md` | §6.6 (187–193) | The CI-mediated credential-flow design rule for credentialed-ops designs (author-workflow-CI-runs; the 5 rejected anti-patterns reference; the verification-probe-must-confirm-CI-structure requirement). Fires only when a brief involves credentialed operations. (Cross-refs into op-disc §20 + credential-discipline SKILL preserved in module.) |
| `substrate/modules/principal-gate-design.md` | §6.7 (195–207) | The PRINCIPAL-gate recognition + surface-at-ratification-time discipline (recognize gating clauses at design time; surface in the design artifact for ARGUS audit; do-NOT-use-post-hoc-disposition-framing) + the §25.5 probe-design throwaway-clone sub-case + the Arc 26 `stoa--dxw`/`stoa--501` empirical. Fires only on directive/spec designs with PRINCIPAL-gating clauses. |
| `substrate/modules/canonical-template-alignment.md` | §6.8 (209–250) | The two-or-more-inline-template-copies byte-alignment discipline (the `diff <(sed -n ...) <(sed -n ...)` mechanical check; within-design scope) + the Arc 24 bw-poll-loop empirical (`stoa--5sr`; Discipline-shipped Arc 40) + the cross-refs. Fires only when a design carries 2+ inline canonical-template copies. **§6.8 is SPEC-prose-referenced + cross-cited (VERA §208, SPEC L553) → its stub keeps the `### 6.8` heading line (§2.7.1).** |
| `substrate/modules/probe-grounding.md` | §6.9 (252–330) + §6.9.3' (332–375) + §6.9.3'' (377–481) | The full probe-grounding cluster: §6.9's 5-clause discipline (anchor the regex / character-class completeness / live round-trip / ground-check against shipped tool surface / enumeration-vs-invocation context) + the 5-anchor `stoa--mn3` empirical; §6.9.3' round-trip-adjacent-prose extension + the stellation Arcs 2-3 anchors; §6.9.3'' live-RT-at-authoring + COMPLETENESS CLAUSE + SIBLING-DEFECT-CLASS EXTENSION + the 60× cost-multiplier math + the 6-anchor canon-promotion block + recursive-self-application surveillance. The single largest relocation (~227 source lines across the three primed subsections). Fires only when a design authors verification probes. **§6.9 is the MOST heavily externally-cited DAEDALUS subsection (8 cites from the validate-spec skill .py/.sh/SKILL.md — it is the discipline-of-record the spec resolver's own grounding comments point at) → its stub keeps the `### 6.9` heading line; §6.9.3'' is also cross-cited (VERA §212/§217) → its stub keeps the `### 6.9.3''` heading line (§2.7.1).** |
| `substrate/modules/ssot-with-why.md` | §6.10 (483–544) | The qualitative-acceptance-anchor SSoT-with-WHY pattern (identify the qualitative-acceptance surface / build the SSoT module-or-section / reference at every consumption site / audit at the §6 anti-pattern surface) + the two worked examples (motion-vocabulary SSoT; three-surface reduced-motion architecture) + the cross-refs. Fires only on qualitative-acceptance-body designs (motion vocab, color palette, error-tone, fallback-ordering). |
| `substrate/modules/api-docs-dont-generalize.md` | §6.11 (546–591) | The API-docs-examples-don't-generalize-to-differently-shaped-elements discipline (identify the target element-type / ground-check the API against the target's attribute surface / narrow-or-reshape when the verb doesn't apply) + the two Pass-10 anchors (attrX/attrY pick; motion layoutId not on SVG) + the cross-refs. Fires only on third-party-API designs. |

**Module count vs subsection count (the one place these differ).** The table lists 7 rows but the §6.9 row carries THREE subsections — the §6.9 cluster (§6.9 + §6.9.3' + §6.9.3'') is consolidated into ONE `probe-grounding.md` module (the three subsections are one coherent probe-grounding discipline; §6.9.3'/§6.9.3'' explicitly "extend §6.9"). So the CONDITIONAL count is **7 module files** covering **9 relocated §6.x subsections** (§6.2.1', §6.6, §6.7, §6.8, §6.9, §6.9.3', §6.9.3'', §6.10, §6.11). The stub-count is per-subsection (each relocated subsection leaves its own numbered stub — §2.7.1); the module-count is 7 (the probe cluster co-locates 3 subsections in one module, like Arc-48's `pre-branch-hygiene.md` co-located §5.9+§5.9.4 and `arc-close-hygiene.md` co-located §5.10+§5.11).

**7 CONDITIONAL module files created + populated this arc, covering 9 relocated §6.x subsections.** Largest: `probe-grounding.md` (~227 source lines, §6.9+§6.9.3'+§6.9.3'') — one coherent probe-grounding discipline, acceptable per op-disc §33 per-module line-count discipline (cf. Arc-47's `autonomous-mode-setup.md` at ~249, accepted; Arc-48's `background-dispatch-hygiene.md` at ~103). `canonical-code-block-fix.md` (~51) and `canonical-template-alignment.md` (~42) are the next.

### 2.4 KEEP-TIGHTEN sections (stay inline; prose tightened; no relocation)

The always-on architect core. Read on every design dispatch DAEDALUS runs:

- **YAML frontmatter (1–6) + role-identity header table (8–20).** The sub-agent envelope contract (`name:`/`description:`/`tools:`/`model:`) + the rank/mnemonic/role table + the "you are a CAPTAIN, you do not have the Agent tool" identity paragraph. KEEP verbatim — frontmatter is structural (the harness reads it), the identity para is always-on. (Tighten nothing in the frontmatter; the identity para is already tight.)
- **§1 (your one job, 24–30).** The singular-output rule (write a buildable design; do NOT build/verify/review/critique) + the writes-plans-not-code rule. Always-on; the load-bearing role boundary every dispatch. KEEP-TIGHTEN.
- **§2 (the brief you receive, 32–45).** The brief-shape contract (design question / artifact path / research input / ticket ID) + the missing-input-refuse rule + the operating-mode flag (hitl/autonomous). Always-on — read at the start of every dispatch to parse the brief. KEEP-TIGHTEN.
- **§3 (what you write to disk, 47–59).** The 5-part design-output contract (problem restatement / approach / verification probes / self-assessed weak points / out of scope) + the breadcrumb-comment reflex. Always-on — this IS the deliverable shape every design follows. KEEP. (Do NOT relocate — this is the architect's core output contract; relocating it would gut the slim core.)
- **§4 (what you do NOT write, 61–68).** The four don'ts (no code/feature-branch commits; no editing the research artifact; no writing ARGUS's critique; no direct CAPTAIN dispatch). Always-on role boundary. KEEP.
- **§5 (voice, 70–77).** The workmanlike-voice rule + the PRINCIPAL-not-Colonel naming rule + the avoid-marketing-vocabulary rule. Always-on authoring discipline read every time DAEDALUS writes prose. KEEP-TIGHTEN.
- **§6.1 (restatement gate — pre-work, load-bearing, 82–89).** The pre-work gate every design opens with (restate the problem; converge-or-diverge; name imported assumptions). Always-on — fires at the START of every design. KEEP. (Explicitly KEEP per the brief's enumerated always-on core.)
- **§6.2 (self-assessed weak points — post-work, load-bearing, 91–106).** The post-work gate every design closes with (audit for brittle spots; silently-smoothing vs over-apologizing failure modes; the empty-list-needs-defense rule; the distinguishing-property-vs-ARGUS framing). Always-on — fires at the END of every design. KEEP. **The two cross-ref pointer lines at 104–106 (the `<!-- cite: ... §6.2.1' -->` + `<!-- cite: ... §6.10 -->` comments pointing to the now-relocated §6.2.1'/§6.10) UPDATE to point at the modules** (the disciplines they reference move to `canonical-code-block-fix.md` / `ssot-with-why.md`; the §6.2 prose keeps the one-line "see <module> for the canonical-code-block-fix discipline that extends self-catch" pointer, repointed at the module + the §6.0 index row). KEEP §6.2 rule; repoint its two extension-cross-refs.
- **§6.3 (consume research; don't re-derive it, 160–162).** Always-on reflex — every dispatch with a research input. KEEP (3 lines, already tight).
- **§6.4 (use WebSearch / WebFetch for live constraints, 164–166).** Always-on reflex — the training-data-is-stale rule that gates every third-party assumption. KEEP (3 lines, already tight).
- **§6.5 (heartbeat-and-read-before-write via bw, 168–185).** The comm contract every dispatch follows (4 beats / read-before-write / `bw comment` positional / Monitor+run_in_background forbidden). Always-on — DAEDALUS heartbeats on every dispatch. KEEP-TIGHTEN (the 4-beat list + the prohibitions are operational; tighten only obvious verbosity).
- **§7 (verdict format, 595–622).** The exact verdict block MAJOR_PLINY parses + the verdict definitions (pass/partial/refused) + the post-as-bw-comment rule. Always-on — every dispatch ends with this block. KEEP. (Do NOT relocate — PLINY parses it every return.)
- **§8 (authorship attribution, immutable, 625–628).** The names-the-PRINCIPAL rule. Always-on (and itself the authorship discipline). KEEP.
- **§9 (when this file is wrong, 631–633).** The field-notes-not-doctrine rule + the surface-via-follow_ups reflex + the standby-run closer. Always-on. KEEP.

### 2.5 DUPLICATE relocations (→ pointer)

**ZERO DUPLICATE relocations.** Unlike MAJOR_PLINY §6.1 (which duplicated the op-disc §12 bw-cookbook keep-home), CAPTAIN_DAEDALUS carries no content that is a verbatim copy of a keep-home elsewhere. §6.5 (heartbeat-bw) CROSS-REFS op-disc §18 / §12 / MAJOR_PLINY §5.8 but does not DUPLICATE them (it carries the DAEDALUS-seat-specific 4-beat contract, which is seat-framing not a cookbook copy — analogous to how Arc-48 kept MAJOR_PLINY §6.1's `bw prime` PLINY-framing residue). §6.6 (credential) and §6.7 (PRINCIPAL-gate) CROSS-REF op-disc §20 / §25 but carry the DAEDALUS-design-time application, not a duplicate of the universal rule. **0 DUPLICATE chunks.** (Confirmed: no DAEDALUS section self-declares "this duplicates <keep-home>; consolidate"; the cross-refs are live pointers to OPERATIONAL content elsewhere, kept inline per the SPLIT rule §3.6.)

### 2.6 Ambient-vs-conditional CALLS — flagged for ARGUS

These are the genuine ambient-vs-conditional judgment calls for the architect file. rev1 makes a defensible KEEP/RELOCATE call for each. The ambient-vs-conditional test (per the brief): **does DAEDALUS need this on EVERY design dispatch (KEEP) or only for a specific design-task-type (RELOCATE)?**

- **A1 — §6.2 (self-assessed weak points): KEEP, but it CROSS-REFS two now-relocated subsections (§6.2.1', §6.10).** §6.2 itself is unambiguously KEEP (the post-work gate fires every design). The wrinkle: §6.2's prose (104–106) carries forward-pointers to §6.2.1' (canonical-code-block-fix, "extends §6.2 self-catch with a fix-location rule") and §6.10 (qualitative-acceptance, "extends §6.2 self-catch to qualitative-acceptance bodies"). Those two TARGETS relocate to modules. **Disposition:** KEEP §6.2's rule + the one-line "extends" pointers, but REPOINT each pointer at the module (`canonical-code-block-fix.md` / `ssot-with-why.md`) + the §6.0 index row, so a reader at §6.2 still learns the extensions exist and where to recover them. (ARGUS A1: confirm repoint-the-extension-pointer is right vs. dropping them — I judge repoint, because the extensions are real always-relevant signposts even though the detailed discipline is conditional.)
- **A2 — §6.6 (credential) + §6.7 (PRINCIPAL-gate): RELOCATE despite being "load-bearing" disciplines.** Both are flagged "load-bearing" in their headings, which could read as always-on. But the ambient-vs-conditional test is decisive: §6.6 fires ONLY when "a brief involves credentialed operations"; §6.7 fires ONLY when "designing a directive or spec that contains a PRINCIPAL-gating clause." Neither fires on a typical design (a feature design, a refactor design, a debloat design like THIS one touches neither). "Load-bearing" describes the SEVERITY when the task-type arises, not the FREQUENCY — these are high-stakes-when-they-fire, but they fire conditionally. So both RELOCATE. (ARGUS A2: confirm "load-bearing" ≠ "always-on" — the severity-vs-frequency distinction. I judge RELOCATE because the design-task-type gate is clear; a feature/refactor/debloat design reads neither.)
- **A3 — §6.5 (heartbeat-bw): KEEP despite being long (~18 lines).** §6.5 is the comm contract DAEDALUS follows on EVERY dispatch (the 4 beats fire every dispatch; read-before-write fires every bw write; the Monitor/run_in_background prohibitions are always-live). It passes the ambient test cleanly (every dispatch). KEEP-TIGHTEN (it is long but every line is always-on operational). Contrast §6.6/§6.7 which are SHORTER but conditional — length is not the test; frequency is.
- **A4 — the §6.9 probe cluster (§6.9 + §6.9.3' + §6.9.3''): RELOCATE all three to ONE module.** §6.9 fires only when a design AUTHORS verification probes (every design HAS a §3-probes section, but the GROUNDING discipline — anchor the regex, live-round-trip, ground-check the tool surface — is read only when the probes contain regex/grep/algorithm against substrate prose or tool output; a design whose probes are simple file-existence checks does not need the 5-clause grounding cluster). The three subsections are one coherent discipline (§6.9.3'/§6.9.3'' explicitly "extend §6.9 clause 3"), so they co-locate in `probe-grounding.md`. (ARGUS A4: is the probe-grounding cluster CONDITIONAL or always-on? Every design writes probes, but not every design writes REGEX/tool-surface probes that need the grounding discipline. I judge CONDITIONAL — the §3-probes-section RULE is in always-on §3; the GROUNDING DETAIL is read only when the probes are regex/tool-shaped. Borderline; surfaced.)

### 2.7 §-numbering coherence + cited-subsection-heading preserve + the recompose marker + the MODULE-OWNERSHIP partition (4th owned-set)

#### 2.7.1 Section-number + cross-ref-cited-subsection-heading PRESERVE via stubs

The slim core PRESERVES the §6.x subsection numbers via stubs. Each relocated §6.x subsection leaves a stub at its original number (heading + `Read` pointer + paired recompose marker). The cross-ref-cited subsections **§6.7, §6.8, §6.9, §6.9.3'', §6.11** (cited from CAPTAIN_ADA / CAPTAIN_VERA / op-disc / the op-disc-owned `mechanical-inspection-split.md` module / the validate-spec skill — substrate-internal resolution; full census + file:line in §3.1) keep their heading lines as REAL markdown headings so the substrate `CAPTAIN_DAEDALUS.md §6.x` cites still resolve. **§6.9 is the heaviest — cited 8× by the validate-spec skill** (`.py`/`.sh`/SKILL.md), so its `### 6.9` stub heading line is the most load-bearing to preserve. (ALL relocated §6.x get a heading-line stub regardless, since each is a numbered subsection; the cross-cited ones — §6.7/§6.8/§6.9/§6.9.3''/§6.11 — are the ones where the heading line is load-bearing for resolution, not just for uniformity. §6 top-level resolves to the KEEP `## 6.` Disciplines heading, untouched.)

**No SPEC-resolver cite is at risk** (§3.1.2 — the resolver matches zero DAEDALUS refs in SPECIFICATION.md), so unlike Arc 47/48 there is NO P-SPEC-XREF at-risk set to preserve a heading FOR. The heading-line preservation here serves the SUBSTRATE-internal cross-ref resolution (ADA/VERA/op-disc cites + human readers following `CAPTAIN_DAEDALUS.md §6.8`), not the validate-spec mechanical resolver. **This is reported, not assumed: P-SPEC-XREF still RUNS (asserting zero DAEDALUS refs flip PASS→FAIL) but its at-risk set is empty — a standing guard against a FUTURE spec cite, not a current obligation.**

**Exact stub shape (relocated §6.x subsection, SINGLE-subsection module — the literal ADA writes)** (mirrors Arc-47 §2.7.1 / Arc-48 §2.7.1-class-1; used for §6.2.1' / §6.6 / §6.7 / §6.8 / §6.10 / §6.11 — each its own module):
```
### 6.6 Credential discipline (load-bearing for designs that touch credentialed ops)
Relocated to `.claude/modules/credential-flow-design.md` (CONDITIONAL — read when a design brief involves credentialed operations against any third-party API or cloud service). Recover the CI-mediated design rule + the 5-anti-pattern reference via `Read .claude/modules/credential-flow-design.md`. Relocation-index row in §6.0.
<!-- MODULE-INLINE:credential-flow-design -->
<!-- /MODULE-INLINE:credential-flow-design -->
```

**Exact stub shape (the §6.9 probe cluster — THREE subsections, ONE module — mirrors Arc-48 §2.7.1-class-2 co-location).** §6.9 + §6.9.3' + §6.9.3'' relocate whole into `probe-grounding.md`; the stub keeps each subsection heading line (so the §6.9.3'' cross-ref from VERA resolves; §6.9 / §6.9.3' for uniformity), with the recompose marker pair at the END so subproject re-inline appends the bodies once (idempotent):
```
### 6.9 Probe-grounding discipline for design.md probes (extends §5.11 to the authoring seat)
Relocated → `probe-grounding.md` §6.9 (CONDITIONAL — read when a design authors verification probes containing regex/grep/algorithm against substrate prose or tool output). Recover the 5-clause discipline via `Read .claude/modules/probe-grounding.md`. Relocation-index row in §6.0.
### 6.9.3' Round-trip prose adjacent to probe-specs (extends 6.9 clause 3)
Relocated → `probe-grounding.md` §6.9.3'.
### 6.9.3'' Live-round-trip probes at authoring time + COMPLETENESS CLAUSE (extends 6.9 clause 3)
Relocated → `probe-grounding.md` §6.9.3''.
<!-- MODULE-INLINE:probe-grounding -->
<!-- /MODULE-INLINE:probe-grounding -->
```

Notes on the stubs:
- The cross-ref-cited subsections that MUST be real heading lines for substrate resolution are **§6.7, §6.8, §6.9, §6.9.3'', §6.11** (the active-file cites — census §3.1; §6.9 is cited 8× by the validate-spec skill, the heaviest). Each keeps its `### 6.x` heading line in the stub. §6.2.1', §6.6, §6.9.3', §6.10 are NOT externally cited but keep heading-line stubs for uniformity + so a human following `CAPTAIN_DAEDALUS.md §6.10` lands on a real anchor.
- A reader following `CAPTAIN_DAEDALUS.md §6.8` (human, or ADA/VERA reading their own cross-ref) lands on the real `### 6.8 Canonical-template wording-alignment discipline` heading line, which points at the module. At subproject tier the recompose re-inlines the full §6.x bodies BELOW the markers; both the stub heading and the re-inlined body heading exist, which is harmless (a reader finds the stub heading first, follows to the body below).
- The §6.0 relocation index sits ABOVE §6.1 (the first KEEP subsection); the relocated §6.x stubs sit at their original positions (§6.2.1' after §6.2, §6.6 after §6.5, etc.). The KEEP subsections (§6.1/§6.2/§6.3/§6.4/§6.5) stay inline at their numbers, interleaved with the stubs in numeric order — exactly as op-disc interleaved KEEP §15 inline among relocated §11/§16/§17 stubs (Arc 47).

The paired sentinel `<!-- MODULE-INLINE:<module-name> -->` … `<!-- /MODULE-INLINE:<module-name> -->` is the recompose hook (machine-parseable inert HTML comment at user/project tier; idempotency anchor at subproject tier). `<module-name>` is the module basename without `.md`. Same justification as Arc-45/47/48 §2.7. The §-stubs for KEEP subsections carry NO recompose marker — only the 7 whole-discipline CONDITIONAL relocations (across 9 stub headings) re-inline at subproject tier.

#### 2.7.2 The MODULE-OWNERSHIP partition — the FOURTH owned-set (+ the no-DEST_DAEDALUS-var wrinkle)

**The mechanism already exists (Arc 47 two-set + Arc 48 third owner).** `recompose_module_inline()` (install.sh L895–998) takes `(role_file, owned_basenames)` and passes the awk TWO `-v` lists: `global_list` (the filesystem glob minus README → `global_exists[]`, backs Check A) and `owned_list` (the per-call arg → `owned[]`/`nowned`/`consumed[]`, backs Checks B/D). Arc 47 wired POLYBIUS's 5 + op-disc's 12; Arc 48 added PLINY's 11 (and the comment block at L887–893 already says "THIS ARC recomposes THREE files"). **This arc's extension (the FOURTH owned-set):**

1. Add `DAEDALUS_MODULES="canonical-code-block-fix credential-flow-design principal-gate-design canonical-template-alignment probe-grounding ssot-with-why api-docs-dont-generalize"` (the 7-module DAEDALUS owned-set) next to the existing three (L1004–1006).
2. Add `recompose_module_inline "$DEST_DAEDALUS" "$DAEDALUS_MODULES"` after the existing three calls (L1007–1009).
3. **No function-body change.** Check A still tests `name in global_exists` (the GLOBAL set, now 5 + 12 + 11 + 7 = **35 module sources** minus README); Checks B/D iterate/count the DAEDALUS owned-set for the DAEDALUS call. The two-set discipline holds unchanged.

**The ONE genuinely-new mechanic (the no-`DEST_DAEDALUS`-var wrinkle).** POLYBIUS / PLINY / op-disc each have a dedicated `DEST_*` var (`$DEST_POLYBIUS` L818, `$DEST_PLINY` L819, `$DEST_OPERATING_DISCIPLINES` L866) written by a dedicated deploy step BEFORE the recompose block. **DAEDALUS does NOT** — it deploys inside the `CAPTAIN_NAMES` loop (L1021–1034), with no standalone path var. Two correctness obligations follow:
   - **(a) Construct the DAEDALUS deploy path for the recompose call.** Set `DEST_DAEDALUS="${DEST_AGENTS_DIR}/CAPTAIN_DAEDALUS${NAME_SUFFIX}.md"` (mirroring the loop's `dest=` at L1023) so the recompose call has a path. `$DEST_AGENTS_DIR` + `$NAME_SUFFIX` are both in scope at the recompose block. (ADA's call: set `DEST_DAEDALUS` once near the other `DEST_*` vars, OR inline the path at the call site — a var is cleaner + mirrors the existing three.)
   - **(b) ORDERING: the CAPTAIN deploy loop must run BEFORE the DAEDALUS recompose call.** The recompose block currently starts at L894 (the `if [ "$TARGET" = "subproject" ]` wrapper) and the CAPTAIN loop is at L1014–1037 — i.e. the recompose block currently runs BEFORE CAPTAINs deploy. The POLYBIUS/PLINY/op-disc recompose works because their files deploy earlier (L849/L851/op-disc-cp). For DAEDALUS, the `CAPTAIN_DAEDALUS_<sub>.md` file does not exist yet when the L894 block runs. **Fix (ADA's choice of two):** (i) MOVE the four recompose calls (L1007–1009 + the new DAEDALUS call) to a NEW `if [ "$TARGET" = "subproject" ]` block placed AFTER the CAPTAIN deploy loop (L1037), keeping the function definition where it is; OR (ii) MOVE the CAPTAIN deploy loop to before the recompose block. Option (i) is cleaner + lower-risk (it relocates only the four call lines, not the deploy loop; the function definition + the POLYBIUS/PLINY/op-disc files already exist by L1037). §6.5 specifies option (i).

This keeps the flat-glob deploy + Read-path convention (no owner-subdirs). The partition lives in the call sites + the two awk lists, not the filesystem — unchanged from Arc 47/48.

---

## §3 — The relocation ledger (the losslessness proof artifact)

This ledger is the artifact ARGUS audits for LOST CANON. **One row per relocated chunk.** Every section in the 633-line source either appears as a ledger row with a lossless home OR is a KEEP-TIGHTEN section that stays inline (§3.7 lists those for audit completeness). Line ranges are grounded against the LIVE `substrate/CAPTAIN_DAEDALUS.md` (re-read this design phase; §-map confirmed via `grep -nE '^#{1,4} '`).

### 3.1 Cross-ref-preservation check (which CAPTAIN_DAEDALUS §N are cited elsewhere — confirmed for stub-preserve)

Grepped live across `substrate/` (active files only — role files, install.sh, hooks, templates, skills, modules) AND `SPECIFICATION.md` at repo root via the shipped `validate-spec` resolver (`spec_refs.py`; arc directives + pastes are frozen history, excluded). **CRITICAL METHOD NOTE:** the naive `CAPTAIN_DAEDALUS(\.md)? §N` regex MISSES the dominant cite form `` `CAPTAIN_DAEDALUS.md` §6.7 `` (a backtick at `0x60` sits between `.md` and the space — confirmed by hex-dump of CAPTAIN_ADA.md L151). The census below uses a BACKTICK-TOLERANT pattern (`CAPTAIN_DAEDALUS(\.md)?\`? §...`) — P-XREF uses the same. The COMPLETE external-cite enumeration (file:line, this design phase):

| §N cited | Citing active files (file:line) | SPEC-resolver? | Disposition under this cut |
|---|---|---|---|
| §6 (top-level) | `modules/mechanical-inspection-split.md`:47 (an op-disc-owned module's cross-ref) | no | **KEEP — `## 6.` heading stays** (the §6 Disciplines heading is preserved; the cite resolves to it) |
| §6.7 | CAPTAIN_ADA.md:145/151, CAPTAIN_VERA.md:170, operating-disciplines.md:1045/1088 | no (SPEC L711 cites "§25" not DAEDALUS §6.7) | **RELOCATE → stub keeps `### 6.7` REAL HEADING LINE** (substrate-cited ×5) |
| §6.8 | CAPTAIN_VERA.md:208, **SPECIFICATION.md L553 (prose, NOT resolver-matched)** | **no** (backtick-form unmatched — §3.1.2) | **RELOCATE → stub keeps `### 6.8` REAL HEADING LINE** (substrate-cited; SPEC prose preserved by the heading title in the module) |
| §6.9 | `validate-spec/_check_runner.py`:15/452, `_lib/bw_tickets.py`:14, `_lib/drift_check.py`:44, `_lib/spec_refs.py`:23/55, `check.sh`:33, `SKILL.md`:125 (**8 cites — the most heavily externally-cited DAEDALUS subsection**) | no (these are CODE-COMMENT cites — "Per CAPTAIN_DAEDALUS.md §6.9 (Probe-grounding discipline)") | **RELOCATE → stub keeps `### 6.9` REAL HEADING LINE** (substrate-cited ×8) |
| §6.9.3'' | CAPTAIN_VERA.md:212/217 | no | **RELOCATE → stub keeps `### 6.9.3''` REAL HEADING LINE** (substrate-cited ×2) |
| §6.11 | CAPTAIN_ADA.md:183/186 | no | **RELOCATE → stub keeps `### 6.11` REAL HEADING LINE** (substrate-cited ×2) |

**No top-level `CAPTAIN_DAEDALUS.md §1`–`§5`/`§7`–`§9` cite exists in any active file** (only the `§6` Disciplines-heading cite from mechanical-inspection-split.md, which resolves to the KEEP `## 6.` heading) — the §N cites are the six §6.x sibling-discipline / tooling cross-refs above (all into sections this cut touches; §6.7/§6.8/§6.9/§6.9.3''/§6.11 RELOCATE → stub-heading-preserved; §6 top-level KEEP). **The validate-spec §6.9 cites are CODE COMMENTS (human-orientation in the skill source), not runtime path resolution** — they do not break at runtime (the skill does not `Read` DAEDALUS §6.9 at runtime; it cites it as the discipline-of-record in a comment), but the stub heading line keeps them resolvable for a human / a future audit following the comment. **Check result:** every `CAPTAIN_DAEDALUS.md §6.x` cited from an active substrate file resolves post-cut — §6 to the KEEP heading, §6.7/§6.8/§6.9/§6.9.3''/§6.11 to their stub heading lines. The KEEP sections (§1–§5, §6.1–§6.5, §7–§9) are otherwise not externally cited, so their numbers are preserved trivially (they stay inline). P-XREF (backtick-tolerant) asserts this.

### 3.1.2 SPECIFICATION.md DAEDALUS cite census (run live via spec_refs.py this design phase)

Ran `python3 substrate/skills/validate-spec/_lib/spec_refs.py --spec SPECIFICATION.md --repo-root .` against the LIVE source and filtered to DAEDALUS refs. **The COMPLETE result: ZERO `CAPTAIN_DAEDALUS.md §N` references are matched by the resolver.**

The resolver's form-(a) regex (`\b([A-Za-z0-9_.\-/]+\.md)\s+§([0-9A-Za-z.\-]+)`) requires `.md` immediately followed by whitespace then `§`. SPECIFICATION.md L553 writes the reference as `` `CAPTAIN_DAEDALUS.md` §6.8 "Canonical-template wording-alignment discipline" `` — the closing **backtick sits between `.md` and the space**, so `\.md\s+§` does not match (verified live this design phase: `_RE_FORM_A.findall` and `_RE_FORM_C.findall` both return `[]` on L553, and a full-SPEC scan finds zero DAEDALUS form-(a)/form-(c) matches). The only CAPTAIN cite the resolver resolves at all is `CAPTAIN_VERA.md §5.11` at SPEC L594 (which is unaffected by this cut).

**The at-risk set (would flip PASS→FAIL): EMPTY.** No DAEDALUS ref resolves PASS today, so none can regress. **P-SPEC-XREF still RUNS** (asserting zero DAEDALUS refs flip PASS→FAIL + the full validate-spec PASS/FAIL totals are unchanged: baseline **PASS=156, FAIL=56** this design phase) — but as a standing guard, not a current obligation. **Reported finding for the capstone (§9 follow-up):** SPEC L553's reference to `CAPTAIN_DAEDALUS.md §6.8` is INVISIBLE to the validate-spec resolver because of the backtick-before-the-§ formatting. That is a pre-existing SPEC formatting nuance (the cite is human-readable but not machine-resolvable), NOT a regression this cut introduces — and the §6.8 heading title ("Canonical-template wording-alignment discipline") is preserved verbatim in `canonical-template-alignment.md`, so the L553 prose reference (which quotes the title) stays accurate. Flagged for a future spec-audit pass (a one-edit fix: `` `CAPTAIN_DAEDALUS.md §6.8` `` → backtick AROUND the whole `File §N` token, OR drop the inner backtick), out of this arc's cut scope.

### 3.2 CONDITIONAL relocations (→ disk module; slim-core residue = stub + `Read` pointer + recompose marker + relocation-index row) — 7 modules, 9 subsections

| Source (§ + live lines) | Class | New home | Slim-core residue |
|---|---|---|---|
| §6.2.1' (108–158) | CONDITIONAL | `modules/canonical-code-block-fix.md` | §6.2.1' stub + `<!-- MODULE-INLINE:canonical-code-block-fix -->` + index row |
| §6.6 (187–193) | CONDITIONAL | `modules/credential-flow-design.md` | §6.6 stub + marker + index row |
| §6.7 (195–207) | CONDITIONAL | `modules/principal-gate-design.md` | §6.7 **REAL HEADING LINE** stub (substrate-cited) + marker + index row |
| §6.8 (209–250) | CONDITIONAL | `modules/canonical-template-alignment.md` | §6.8 **REAL HEADING LINE** stub (substrate-cited + SPEC-prose) + marker + index row |
| §6.9 + §6.9.3' + §6.9.3'' (252–481) | CONDITIONAL | `modules/probe-grounding.md` | §6.9 (**REAL HEADING LINE — substrate-cited 8× by validate-spec skill**) + §6.9.3' + §6.9.3'' (**REAL HEADING LINE — VERA-cited**) stubs + ONE marker + index row |
| §6.10 (483–544) | CONDITIONAL | `modules/ssot-with-why.md` | §6.10 stub + marker + index row |
| §6.11 (546–591) | CONDITIONAL | `modules/api-docs-dont-generalize.md` | §6.11 **REAL HEADING LINE** stub (substrate-cited) + marker + index row |

**7 CONDITIONAL module files; 9 relocated §6.x subsections** (the probe cluster = 3 subsections in 1 module). Largest: `probe-grounding.md` (~227 source lines) — one coherent discipline, acceptable per op-disc §33 (cf. Arc-47 `autonomous-mode-setup.md` ~249).

### 3.3 PROVENANCE relocations — embedded empirical travels WITH the relocated discipline (move-with-CONDITIONAL)

Unlike POLYBIUS / op-disc / PLINY (whose KEEP sections each had a tail "N=1 provenance" block compressing to a standalone `Anchor:` in the slim core), CAPTAIN_DAEDALUS's empirical anchors are **embedded inside the §6.x disciplines that all RELOCATE**. So each discipline's empirical block travels WITH it into its module — there are NO standalone C-1 Anchors left in the slim core (the KEEP sections §1–§5/§6.1–§6.5/§7–§9 carry essentially no empirical-provenance tails to compress; they are rule-prose). The C-1 content-check gate (modules/README §5.2) still applies: before ADA writes each module's compressed `Anchor:` (replacing any verbose in-prose empirical narrative the module-author chooses to compress), ADA runs `bw show <cited-id>` to confirm the ticket carries the story. All ids resolve-checked live this design phase (§3.3.1).

| Source empirical (§ + live lines) | bw id(s) | Disposition |
|---|---|---|
| §6.2.1' 4-anchor block (134–158: Arc 3 r1 / rev2 o1 / VERA Probe L / Arc 4 WP13) | in-prose stellation-Pass-10 narrative anchors (no standalone `stoa--` ticket per anchor) | Moves WITH §6.2.1' into `canonical-code-block-fix.md` VERBATIM (the anchors ARE the empirical record; kept in-module, not compressed — see §3.4 note) |
| §6.7 Arc 26 empirical (205) | `stoa--dxw`, `stoa--501` | Moves WITH §6.7 into `principal-gate-design.md`; `Anchor: stoa--dxw, stoa--501` in module |
| §6.8 Arc 24 empirical (231–240) | `stoa--5sr` (Discipline-shipped Arc 40: `stoa--utn`) | Moves WITH §6.8 into `canonical-template-alignment.md`; `Anchor: stoa--5sr` in module (see §3.3.1 note on `stoa--utn`) |
| §6.9 5-anchor empirical (314–322) | `stoa--mn3` (canon-promotion `stoa--1lm`) | Moves WITH §6.9 into `probe-grounding.md`; `Anchor: stoa--mn3, stoa--1lm` in module |
| §6.9.3' 3-anchor empirical (357–367) | in-prose stellation-Pass-10 narrative anchors | Moves WITH §6.9.3' into `probe-grounding.md` VERBATIM |
| §6.9.3'' 6-anchor empirical (437–471) | in-prose stellation-Pass-10 narrative anchors | Moves WITH §6.9.3'' into `probe-grounding.md` VERBATIM |
| §6.10 2-worked-example block (516–536) | in-prose stellation-Pass-10 narrative (motion-vocab; reduced-motion) | Moves WITH §6.10 into `ssot-with-why.md` VERBATIM |
| §6.11 2-anchor empirical (569–581) | in-prose stellation-Pass-10 narrative anchors | Moves WITH §6.11 into `api-docs-dont-generalize.md` VERBATIM |

**Counting note:** ALL provenance is "move-with-CONDITIONAL" (8 empirical blocks, each travelling inside its parent module). **ZERO standalone C-1 chunks in the slim core** (no KEEP section has a relocatable empirical tail). **The `stoa--`-ticketed empiricals (§6.7 `stoa--dxw`/`stoa--501`, §6.8 `stoa--5sr`, §6.9 `stoa--mn3`/`stoa--1lm`) compress to a one-line `Anchor:` IN the module after the C-1 `bw show` content-check; the in-prose stellation-Pass-10 narrative anchors (§6.2.1', §6.9.3', §6.9.3'', §6.10, §6.11) move VERBATIM into the module** (they have no standalone `stoa--` ticket to cite — they ARE the only record of those Pass-10 stellation anchors, so verbatim preservation in the module IS the lossless home; see §3.4 for why this is move-with-verbatim, NOT a C-2 archive).

#### 3.3.1 C-1 resolve-check (run live this design phase)

`bw show` resolve-checked: `stoa--nax` (✓ redundant-checks), `stoa--tp1` (✓ verification-complexity), `stoa--mn3` (✓ Arc-40 probe-spec defects), `stoa--1lm` (✓ §5.11→DAEDALUS-probes extension), `stoa--5sr` (✓ Arc-24 follow-up), `stoa--utn` (✓ — BUT titled "Promote save-verdict skill" not the §6.8 wording-alignment topic; §6.8 cites `stoa--utn` as "Discipline-shipped arc: Arc 40", a SHIPPED-IN-arc cite not a content cite — the wording-alignment story lives in `stoa--5sr` + agents/design/arc-24/design.md, both preserved; **flagged for ADA: the §6.8 module `Anchor:` is `stoa--5sr` for the empirical + a note that the discipline shipped in Arc 40 alongside `stoa--utn`, NOT `stoa--utn` as the empirical home**), `stoa--dxw` (✓), `stoa--501` (✓), `stoa--ezj`/`stoa--53u`/`stoa--ioy`/`stoa--cm3` (✓ — these are cited in the §6.x cross-refs, travel with their disciplines), `stoa--gq1`/`stoa--kt6`/`stoa--wad` (✓ — cited in op-disc-relocated modules, not DAEDALUS; resolve-checked for completeness). All DAEDALUS-relevant ids resolve and carry their stories (C-1).

### 3.4 C-2 archive-first cases — DEDICATED CHILD TICKETS

**ZERO firm C-2 chunks.** The in-prose stellation-Pass-10 narrative anchors (§6.2.1' 4-anchor / §6.9.3' 3-anchor / §6.9.3'' 6-anchor / §6.10 2-example / §6.11 2-anchor) have NO standalone `stoa--` bw home — BUT they do NOT need a C-2 archive, because **the discipline they anchor RELOCATES WHOLE to its module (CONDITIONAL), and the empirical block travels INSIDE that module verbatim.** C-2 archive is required only when a provenance block "becomes the only surviving copy once cut" AND has no lossless home (POLYBIUS/op-disc/PLINY's C-2 cases were empiricals being DELETED from a KEEP section with no bw ticket). Here the empirical is NOT being deleted — it moves intact into the module. The module IS the surviving copy. So move-with-verbatim is lossless; no separate child ticket is needed. **(Contrast Arc-48 §5.4: that empirical's parent rule ALSO moved to a module, but its only provenance anchor was a CROSS-REPO `ariadne--b93` not resolvable from the-stoa bw, so it was archived to a child ticket for recoverability-from-this-bw. The DAEDALUS in-prose stellation anchors are not cross-repo ids needing resolution — they are narrative descriptions kept verbatim in-module, self-contained.)** ARGUS Q2: confirm move-with-verbatim (not C-2-child) is right for in-prose narrative anchors that have no bw ticket but are preserved intact in the module. I judge yes — the verbatim in-module copy is the lossless home; a child ticket would duplicate, not preserve.

### 3.5 DUPLICATE relocations (→ pointer)

| Source | Class | Keep-home | Slim-core residue |
|---|---|---|---|
| (none in CAPTAIN_DAEDALUS) | — | — | — |

**ZERO DUPLICATE relocations** (§2.5 rationale). No DAEDALUS section is a verbatim copy of a keep-home elsewhere; the §6.5/§6.6/§6.7 cross-refs to op-disc §12/§18/§20/§25 are LIVE pointers to operational content, kept inline per SPLIT (§3.6), not duplicated bodies. **0 DUPLICATE chunks.**

### 3.6 SPLIT per-line enumeration (cross-ref subsections — deterministic, no ADA guessing)

The relocated §6.x disciplines carry their OWN "Cross-refs" subsections (the `<!-- cite: ... -->` comment blocks + the bullet lists at the tail of §6.2.1' / §6.9 / §6.9.3' / §6.9.3'' / §6.10 / §6.11). **These cross-refs travel WITH the discipline INTO the module — no SPLIT needed** (the same rule Arc-47/48 applied: "Sections whose body relocates whole carry their cross-refs INTO the module — no SPLIT needed there"). SPLIT applies only to the cross-ref tails of KEEP sections.

The KEEP sections with cross-ref tails to handle: **§6.2 (104–106)** — the two `<!-- cite: ... §6.2.1' -->` + `<!-- cite: ... §6.10 -->` comment lines + the one-line "See §6.2.1' for ... §6.10 extends ..." prose. These point at the now-relocated §6.2.1' / §6.10. **Disposition (the only SPLIT in this cut):** REPOINT — keep the one-line prose pointer but rewrite each to name the MODULE + the §6.0 index row (`See canonical-code-block-fix.md (relocated §6.2.1') for the fix-location discipline that extends self-catch; ssot-with-why.md (relocated §6.10) extends self-catch to qualitative-acceptance bodies. Relocation-index rows in §6.0.`). The `<!-- cite: -->` comment lines repoint to the module paths. This is a SPLIT-by-repoint (the LIVE pointer stays, repointed at the relocated home) rather than a SPLIT-by-fold (no empirical/ticket line to fold into an Anchor — §6.2 has no empirical tail).

**1 SPLIT cross-ref handling** (§6.2's two extension-pointers, repointed at modules). P-SPLIT greps the repointed pointer text (asserts §6.2 names the two modules + §6.0).

### 3.7 KEEP-TIGHTEN (stays inline; listed for audit completeness)

YAML frontmatter (1–6) + role-identity header table + identity para (8–20), §1 (one job, 24–30), §2 (the brief, 32–45), §3 (what you write to disk, 47–59), §4 (what you do NOT write, 61–68), §5 (voice, 70–77), §6 heading + NEW §6.0 (relocation index), §6.1 (restatement gate, 82–89), §6.2 (self-assessed weak points, 91–106 — rule KEPT, extension-pointers repointed §3.6), §6.3 (consume research, 160–162), §6.4 (WebSearch live constraints, 164–166), §6.5 (heartbeat-bw, 168–185), §7 (verdict format, 595–622), §8 (authorship attribution, 625–628), §9 (when this file is wrong, 631–633).

### 3.8 Module-OWNERSHIP record (for the install.sh partition — §6.4) — the FOUR owner-sets, NO basename collision

| Owner role file | Owned modules (basenames) |
|---|---|
| `MAJOR_POLYBIUS.md` (Arc 45) | `onboarding`, `sub-project-spawning`, `pair-programmer-authoring`, `pair-programming-prototyping`, `substrate-update-check` |
| `operating-disciplines.md` (Arc 47) | `two-polybius-coordination`, `autonomous-mode-setup`, `sub-agent-transcript-discipline`, `bw-fit-matrix`, `oss-dep-and-latency`, `credential-discipline-detail`, `bw-upgrade`, `mechanical-inspection-split`, `multi-team-interop`, `four-layer-identity`, `substrate-component-design`, `jsdom-timing-discipline` |
| `MAJOR_PLINY.md` (Arc 48) | `ada-brief-preamble`, `sub-agent-watchdog`, `per-worktree-venv`, `post-strabo-vera`, `incomplete-unverifiable-routing`, `smoke-beat-deploy-check`, `background-dispatch-hygiene`, `pre-branch-hygiene`, `arc-close-hygiene`, `seat-identity-brief`, `pliny-polling-pattern` |
| `CAPTAIN_DAEDALUS.md` (THIS arc) | `canonical-code-block-fix`, `credential-flow-design`, `principal-gate-design`, `canonical-template-alignment`, `probe-grounding`, `ssot-with-why`, `api-docs-dont-generalize` |
| (`README.md` — owned by nobody; excluded from every owner-set) | — |

**CAPTAIN_DAEDALUS owns 7 modules.** **NO basename collides across the four owner-sets** (verified this design phase: the 7 DAEDALUS basenames are disjoint from the 5 POLYBIUS + 12 op-disc + 11 PLINY = 28 existing; the closest near-collisions are intentional non-collisions — DAEDALUS's `credential-flow-design` vs op-disc's `credential-discipline-detail` are DISTINCT basenames; DAEDALUS's `canonical-template-alignment` + `canonical-code-block-fix` share no basename with any existing — P-OWNERSHIP-NOCOLLIDE asserts this mechanically across all FOUR sets). The GLOBAL EXISTENCE set for Check A is the full `substrate/modules/*.md` glob (5 + 12 + 11 + 7 = **35 modules**, minus README), owner-agnostic. The per-call OWNED sets drive Checks B/D: POLYBIUS's 5, op-disc's 12, PLINY's 11, DAEDALUS's 7.

### 3.9 Ledger summary (chunk counts per class — self-consistent)

- **CONDITIONAL:** 7 module files covering 9 relocated §6.x subsections (§6.2.1', §6.6, §6.7, §6.8, §6.9, §6.9.3', §6.9.3'', §6.10, §6.11) → **7 new module files = 7 CONDITIONAL chunks** (9 stub headings).
- **PROVENANCE:** **0 standalone C-1** + **0 firm C-2** + **1 SPLIT** (§6.2's extension-pointers, repointed) = **1 PROVENANCE chunk.** Plus 8 "move-with-CONDITIONAL" empirical blocks (travelling inside their parent modules; counted under their parent CONDITIONAL relocation, not separately).
- **DUPLICATE:** **0 chunks.**
- **KEEP-TIGHTEN:** ~16 section-units stay inline (listed §3.7), PLUS 1 NEW always-on addition (§6.0 relocation index).

**Total relocated chunks: 7 CONDITIONAL + 1 PROVENANCE + 0 DUPLICATE = 8 relocated chunks**, each with a lossless home + recovery path. (The lowest relocated-chunk count of the four cuts — because DAEDALUS's bloat is concentrated in §6's design-task-type disciplines, not spread across many empirical/cross-ref tails like the larger files.)

### 3.10 Empirical post-cut floor ESTIMATE (reported, not targeted — per recalibrated criterion)

The big movers: 7 CONDITIONAL relocations move ~511 source lines off-disk (the whole of §6.2.1'≈51 + §6.6≈7 + §6.7≈13 + §6.8≈42 + §6.9≈79 + §6.9.3'≈44 + §6.9.3''≈105 + §6.10≈62 + §6.11≈46 = ~449 discipline-body lines, plus the §6 subsection blank-line separators). The §6.2 extension-pointer repoint is net-neutral (~0). The cut ADDS ~12 lines (the §6.0 relocation index: 9 stub-subsection rows + header). Against 633, the slim core lands an **estimated empirical floor in the ~150–200 line band.** Every line is always-on architect core: the frontmatter + identity table, §1–§5 (one-job / brief / design-output contract / what-you-don't-write / voice), §6.0 index + §6.1 restatement gate + §6.2 weak-points gate + §6.3/§6.4/§6.5 reflexes, §7 verdict format, §8 authorship, §9 when-wrong. **This is an ESTIMATE; the build REPORTS the actual floor (P-FLOOR).** Do NOT cut a KEEP rule to push the floor lower — the floor is whatever the always-on architect core weighs (recalibrated criterion). A landing materially above ~260 means a KEEP section's prose is still verbose (tighten) OR a §6.x discipline was wrongly KEPT (re-check the ambient-vs-conditional call); a landing below ~120 is suspicious (check for a dropped always-on rule — P-FLOOR falsifier guard).

This floor is the SMALLEST of the four cuts in absolute terms (DAEDALUS's source is the smallest, 633 vs op-disc 2156 / PLINY 801 / POLYBIUS pre-cut), and the reduction ratio (~633→~175 ≈ 72%) is the most aggressive — comparable to PLINY's ~64% and far above op-disc's ~58%. The reason: DAEDALUS's bloat is unusually concentrated (81% in §6, almost all of it design-task-type-conditional), so a deep reduction is the honest output, not over-cutting. The always-on architect core is genuinely small — the architect's job is a tight contract (read brief → restate → design → self-assess → verdict), and the design-task-type disciplines that bulk out §6 are exactly the CONDITIONAL content the composition layer is designed to relocate.

---

## §4 — Verification probes (what would falsify the design's intended behavior)

Concrete probes VERA re-executes. The probe spec is load-bearing. Run all from the worktree root (`C:/Users/denso/claude_projects/the-stoa/.claude/worktrees/arc-49-build`). All grep/regex patterns were live-round-tripped against the current substrate state this design phase (per the DAEDALUS §6.9 discipline this file's own author follows — the recursion note: I applied my own probe-grounding discipline to these probes).

### P-FLOOR — empirical floor reported + sanity band
```bash
wc -l substrate/CAPTAIN_DAEDALUS.md
```
**Pass:** the floor is REPORTED; sanity band ~150–200 (rev1 estimate). **Falsifies if:** > 260 (cut too shallow — a KEEP section's prose is still verbose OR a §6.x discipline was wrongly KEPT) or < 120 (suspiciously aggressive — check for a dropped always-on KEEP rule). A 200–260 landing is partial-not-failure. Also run op-disc §33's per-module line-count discipline against each of the 7 new modules (no module is a re-bloat monolith — `probe-grounding.md` at ~227 is the largest and is acceptable: one coherent probe-grounding discipline incl. the 5-clause + COMPLETENESS CLAUSE + 6-anchor block).

### P-COND — every CONDITIONAL discipline has a real module home (7 modules)
```bash
for m in canonical-code-block-fix credential-flow-design principal-gate-design \
         canonical-template-alignment probe-grounding ssot-with-why api-docs-dont-generalize; do
  test -s "substrate/modules/$m.md" && echo "OK $m" || echo "MISSING $m"
done
```
**Pass:** all 7 module files exist non-empty. **Falsifies if:** any missing/empty (LOST CANON).

### P-STUB — every relocated §6.x subsection leaves a stub at its original number (9 stub headings)
```bash
grep -nE '^### (6\.2\.1'"'"'|6\.6|6\.7|6\.8|6\.9|6\.9\.3'"'"'|6\.9\.3'"'""'"'|6\.10|6\.11) ' substrate/CAPTAIN_DAEDALUS.md
# KEEP subsections must be LIVE (not stubbed) — assert §6.1/§6.2/§6.3/§6.4/§6.5 have their content:
for n in '6\.1' '6\.2' '6\.3' '6\.4' '6\.5'; do
  grep -qE "^### ${n} " substrate/CAPTAIN_DAEDALUS.md && echo "OK §${n} live (KEEP)" || echo "FAIL §${n} missing/stubbed"
done
```
**Pass:** §6.2.1', §6.6, §6.7, §6.8, §6.9, §6.9.3', §6.9.3'', §6.10, §6.11 headings present (stubs) AND §6.1–§6.5 headings present (live KEEP). **Falsifies if:** any relocated subsection number GONE, OR a KEEP subsection (§6.1–§6.5) reduced to a stub. (NOTE on the `'` in §6.2.1'/§6.9.3'/§6.9.3'': the prime marks are LITERAL apostrophes in the heading text; the grep escapes them via the `'"'"'` shell-quote idiom — ADA/VERA verify the literal apostrophes survive into the stub headings, since the cross-ref `§6.9.3''` from VERA depends on the exact double-prime.)

### P-XREF — every CAPTAIN_DAEDALUS §N cited from an active SUBSTRATE file resolves post-cut (BACKTICK-TOLERANT — the naive regex misses the dominant `` `…md` §N `` form)
```bash
# BACKTICK-TOLERANT enumeration (the \`? after .md catches the `File.md` §N form — §3.1 method note):
grep -rhoE "CAPTAIN_DAEDALUS(\.md)?\`? §[0-9]+(\.[0-9]+)*('+)?" substrate/ \
  --include='*.md' --include='*.sh' --include='*.py' \
  | grep -vE 'substrate/arcs/|substrate/CAPTAIN_DAEDALUS.md' \
  | grep -oE "§[0-9]+(\.[0-9]+)*('+)?" | sort -u
# §6 (top-level KEEP) resolves to the ## 6. heading:
grep -qE '^## 6\. ' substrate/CAPTAIN_DAEDALUS.md && echo "OK §6 (## 6. heading)" || echo "MISSING §6"
# the five substrate-cited RELOCATED §6.x must each resolve to a real heading line (stub):
for n in '6\.7' '6\.8' '6\.9' "6\.9\.3''" '6\.11'; do
  grep -qE "^### ${n}( |$)" substrate/CAPTAIN_DAEDALUS.md && echo "OK §${n}" || echo "MISSING §${n}"
done
```
**Pass:** §6 resolves to the `## 6.` KEEP heading; the five substrate-cited relocated subsections (§6.7, §6.8, §6.9, §6.9.3'', §6.11) each resolve to a real `### 6.x` heading line in the stub; the backtick-tolerant enumeration's EXTERNAL anchors (from non-DAEDALUS files) are a subset of {§6, §6.7, §6.8, §6.9, §6.9.3'', §6.11}. **Falsifies if:** any of the five cited relocated subsections has no heading line (the ADA / VERA / op-disc / validate-spec-skill cross-ref would break — §6.9 especially, cited 8× by the validate-spec skill), OR the enumeration surfaces an EXTERNAL §N cite this design did not account for (a missed cross-ref → re-census). NOTE: the deduped anchor set will ALSO show §6.2/§6.2.1'/§6.4/§6.9.3'/§6.10 — those are DAEDALUS's OWN internal self-cites (the `<!-- cite: -->` blocks); the `grep -v substrate/CAPTAIN_DAEDALUS.md` excludes the file itself, so the EXTERNAL set is the six above. (The §6.9.3' deduped match comes from VERA L212/L217 citing §6.9.3'' — the trailing `'+` is greedy; both resolve to the §6.9.3'' stub heading.)

### P-SPEC-XREF — SPECIFICATION.md DAEDALUS refs do NOT regress (at-risk set EMPTY; standing guard)
```bash
python3 substrate/skills/validate-spec/_lib/spec_refs.py --spec SPECIFICATION.md --repo-root . \
  > spec_refs_postcut.jsonl 2>&1
python3 - <<'PY'
import json
seen=[]; fails=[]; total_pass=total_fail=0
for line in open('spec_refs_postcut.jsonl', encoding='utf-8'):
    line=line.strip()
    if not line: continue
    try: r=json.loads(line)
    except: continue
    if r.get('summary'):
        print("SUMMARY:", r); continue
    v=r.get('verdict')
    if v=='PASS': total_pass+=1
    elif v=='FAIL': total_fail+=1
    tf=(r.get('target_file_resolved') or r.get('target_file_cited') or '')
    if 'DAEDALUS' in tf:
        seen.append((r.get('anchor'), r.get('citing_line_in_spec'), v))
        if v=='PASS': fails.append(('UNEXPECTED-PASS-NOW-MUST-NOT-REGRESS', r.get('anchor'), r.get('citing_line_in_spec')))
print("DAEDALUS refs the resolver matched:", seen)   # expect [] — backtick-form unmatched (census §3.1.2)
print("TOTALS: PASS=%d FAIL=%d"%(total_pass,total_fail))   # expect PASS=156 FAIL=56 (baseline unchanged)
print("RESULT:", "PASS" if (total_pass==156 and total_fail==56) else "CHECK — totals drifted from baseline")
PY
```
**Pass:** the resolver matches ZERO DAEDALUS refs (the at-risk set is empty — census §3.1.2) AND the full PASS/FAIL totals are UNCHANGED from baseline (PASS=156, FAIL=56) — i.e. the cut did not flip ANY ref (DAEDALUS or otherwise) by, e.g., breaking an op-disc/PLINY heading the DAEDALUS cut touches (it doesn't touch them, so totals must hold). **Falsifies if:** any DAEDALUS ref now resolves (the backtick-form became matchable AND regressed — would be a new surface) OR the totals drift from 156/56 (the cut had a cross-file side-effect — investigate). Note: this is a STANDING GUARD; the empty at-risk set means the probe's job is to confirm no NEW DAEDALUS resolution appeared + the global totals held.

### P-RECOMPOSE — subproject recompose completeness for CAPTAIN_DAEDALUS (THE LOST-CANON-at-subproject probe)
Run on a THROWAWAY subproject deploy (per op-disc §25.5: synthetic parent under a tmp path or `git clone --no-local`; do NOT mutate any operator-owned workspace):
```bash
TMP=$(mktemp -d); mkdir -p "$TMP/myproj"
bash substrate/install.sh --target subproject --parent-dir "$TMP" --subproject myproj
# CAPTAIN_DAEDALUS deploys SUFFIXED at subproject tier via the CAPTAIN_NAMES loop (install.sh L1023):
RECOMPOSED="$TMP/myproj/.claude/agents/CAPTAIN_DAEDALUS_myproj.md"

# (a) The 7 DAEDALUS PAIRED markers SURVIVE, each enclosing a NON-EMPTY body:
grep -cE '^<!-- MODULE-INLINE:' "$RECOMPOSED"     # expect 7 DAEDALUS opens
grep -cE '^<!-- /MODULE-INLINE:' "$RECOMPOSED"    # expect 7 DAEDALUS closes
grep -Pzo '(?m)^<!-- MODULE-INLINE:[^\n]*-->\n<!-- /MODULE-INLINE:' "$RECOMPOSED" && echo "FAIL empty pair" || echo "OK no empty pairs"

# (b) EVERY DAEDALUS module body is present (assert each module's first-heading line appears):
for m in canonical-code-block-fix credential-flow-design principal-gate-design \
         canonical-template-alignment probe-grounding ssot-with-why api-docs-dont-generalize; do
  head1=$(head -1 "substrate/modules/$m.md")
  grep -Fq "$head1" "$RECOMPOSED" && echo "OK body present: $m" || echo "MISSING body: $m"
done

# (c) recomposed subproject CAPTAIN_DAEDALUS is canon-equivalent to full content (NOT the slim band):
wc -l "$RECOMPOSED"   # expect ~630+ (the 7 module bodies re-inlined), NOT the ~150-200 slim band

# (d) POLYBIUS + op-disc + PLINY recompose STILL pass (the FOURTH owner-set did not break Arc 45/47/48):
grep -cE '^<!-- MODULE-INLINE:' "$TMP/myproj/.claude/MAJOR_POLYBIUS_myproj.md"   # expect 5 (Arc-45 markers intact)
grep -cE '^<!-- MODULE-INLINE:' "$TMP/myproj/.claude/operating-disciplines.md"   # expect 12 (Arc-47 markers intact)
grep -cE '^<!-- MODULE-INLINE:' "$TMP/myproj/.claude/MAJOR_PLINY_myproj.md"      # expect 11 (Arc-48 markers intact)
```
**Pass:** (a) all 7 DAEDALUS paired markers survive + NO empty pair; (b) all 7 DAEDALUS module first-heading lines appear; (c) recomposed CAPTAIN_DAEDALUS in the FULL band (~630+); (d) POLYBIUS recompose still inlines its 5 AND op-disc its 12 AND PLINY its 11. **Falsifies if:** any DAEDALUS marker pair empty (body dropped → LOST CANON at subproject tier), OR < 7 DAEDALUS markers survive, OR any DAEDALUS body absent, OR recomposed CAPTAIN_DAEDALUS still in the slim band (recompose silently no-op'd — the no-DEST_DAEDALUS-var path was mis-constructed or the call ran before the deploy loop, §2.7.2-b), OR POLYBIUS/op-disc/PLINY recompose broke (fourth-owner regression).

### P-RECOMPOSE-PATH — the no-DEST_DAEDALUS-var path was constructed correctly (NEW this arc — the one new mechanic)
```bash
# Static check: install.sh constructs the DAEDALUS deploy path for the recompose call
grep -nE 'DEST_DAEDALUS=|recompose_module_inline "\$DEST_DAEDALUS"|CAPTAIN_DAEDALUS\$\{NAME_SUFFIX\}' substrate/install.sh
# Ordering check: the DAEDALUS recompose call appears AFTER the CAPTAIN_NAMES deploy loop (L1021)
awk '/for name in "\$\{CAPTAIN_NAMES\[@\]\}"/{loop=NR} /recompose_module_inline "\$DEST_DAEDALUS"/{call=NR} END{print "loop@"loop" call@"call; print (call>loop)?"OK call-after-loop":"FAIL call-before-loop (file not deployed yet)"}' substrate/install.sh
```
**Pass:** install.sh sets `DEST_DAEDALUS` to the suffixed agents-dir path (`${DEST_AGENTS_DIR}/CAPTAIN_DAEDALUS${NAME_SUFFIX}.md`) AND the `recompose_module_inline "$DEST_DAEDALUS"` call appears AFTER the CAPTAIN deploy loop. **Falsifies if:** `DEST_DAEDALUS` is unset/wrong-path (recompose runs on a non-existent file → the FAIL-LOUD rm-on-error fires OR worse, silently no-ops), OR the call precedes the deploy loop (the suffixed file doesn't exist yet → recompose aborts/no-ops — the exact ordering hazard §2.7.2-b names). This probe targets the ONE new install.sh mechanic this arc introduces beyond the proven Arc-48 fourth-call pattern.

### P-RECOMPOSE-NEG — FAIL-LOUD asserted (losslessness depends on the err() firing)
```bash
mv substrate/modules/probe-grounding.md substrate/modules/probe-grounding.md.bak
bash substrate/install.sh --target subproject --parent-dir "$TMP" --subproject myproj2; echo "exit=$?"
mv substrate/modules/probe-grounding.md.bak substrate/modules/probe-grounding.md
```
**Pass:** install.sh exits NON-ZERO with a clear Check-A `marker MODULE-INLINE:probe-grounding has no module source` error AND does NOT write a partial/slim CAPTAIN_DAEDALUS to the subproject. **Falsifies if:** exit 0 (silent partial deploy — the LOST-CANON-at-subproject failure). NOTE: because Check A tests the GLOBAL existence set (Arc-47 r3), this fires correctly regardless of which owner's recompose call hits the missing module first.

### P-OWNERSHIP — the FOUR-owner partition is correct (no cross-owner Check-B false-positive)
```bash
bash substrate/install.sh --target subproject --parent-dir "$TMP" --subproject myproj3; echo "exit=$?"
```
**Pass:** exit 0 — all four recompose calls pass: POLYBIUS scoped to its 5, op-disc to its 12, PLINY to its 11, DAEDALUS to its 7 (none trips Check B on another owner's modules). **Falsifies if:** exit 2 with a Check-B `module X.md exists but no MODULE-INLINE:X marker` error — the owned-set partition was mis-applied (e.g., DAEDALUS's call passed the wrong owned-set, or the global glob leaked into Checks B/D for the DAEDALUS call).

### P-OWNERSHIP-NOCOLLIDE — no module basename collides across the FOUR owner-sets (extended from Arc 48)
```bash
python3 - <<'PY'
poly="onboarding sub-project-spawning pair-programmer-authoring pair-programming-prototyping substrate-update-check".split()
opd="two-polybius-coordination autonomous-mode-setup sub-agent-transcript-discipline bw-fit-matrix oss-dep-and-latency credential-discipline-detail bw-upgrade mechanical-inspection-split multi-team-interop four-layer-identity substrate-component-design jsdom-timing-discipline".split()
pliny="ada-brief-preamble sub-agent-watchdog per-worktree-venv post-strabo-vera incomplete-unverifiable-routing smoke-beat-deploy-check background-dispatch-hygiene pre-branch-hygiene arc-close-hygiene seat-identity-brief pliny-polling-pattern".split()
daed="canonical-code-block-fix credential-flow-design principal-gate-design canonical-template-alignment probe-grounding ssot-with-why api-docs-dont-generalize".split()
allm = poly+opd+pliny+daed
dupes = {m for m in allm if allm.count(m) > 1}
print("TOTAL basenames:", len(allm), "DISTINCT:", len(set(allm)))   # expect 35 / 35
print("COLLISIONS:", sorted(dupes))
print("RESULT:", "PASS" if not dupes else "FAIL")
PY
# AND assert all four owned-set vars in install.sh have no overlap:
grep -nE 'POLYBIUS_MODULES=|OPDISC_MODULES=|PLINY_MODULES=|DAEDALUS_MODULES=' substrate/install.sh
```
**Pass:** zero collisions across the 35 basenames; install.sh defines all four owned-set vars distinctly. **Falsifies if:** any basename appears in two owner-sets (a marker would be ambiguously owned) — the failure surface the fourth owner extends (verify especially `credential-flow-design` vs op-disc's `credential-discipline-detail` are DISTINCT, and DAEDALUS's two `canonical-*` basenames don't collide with each other or anything existing).

### P-AUTH — no author-field regression + frontmatter intact (CLAUDE.md authorship discipline)
```bash
grep -niE '^(author|owner|creator|by|copyright|maintainer):' substrate/CAPTAIN_DAEDALUS.md substrate/modules/canonical-code-block-fix.md substrate/modules/credential-flow-design.md substrate/modules/principal-gate-design.md substrate/modules/canonical-template-alignment.md substrate/modules/probe-grounding.md substrate/modules/ssot-with-why.md substrate/modules/api-docs-dont-generalize.md
# Frontmatter intact (the sub-agent envelope contract MUST survive the cut):
head -6 substrate/CAPTAIN_DAEDALUS.md
grep -qE '^name: CAPTAIN_DAEDALUS\{\{NAME_SUFFIX\}\}' substrate/CAPTAIN_DAEDALUS.md && echo "OK frontmatter name:" || echo "FAIL frontmatter name: dropped/changed"
grep -qE '^tools: Bash, Read, Write, Edit, Grep, Glob, WebSearch, WebFetch' substrate/CAPTAIN_DAEDALUS.md && echo "OK frontmatter tools:" || echo "FAIL frontmatter tools: changed"
```
**Pass:** no author-like field names anyone other than Denson Smith (CAPTAIN_DAEDALUS carries none; the 7 new modules carry none); the YAML frontmatter `name:`/`tools:` survive verbatim (the harness reads them — a dropped frontmatter breaks the sub-agent envelope). **Falsifies if:** any new module's provenance header introduces an author field, OR the frontmatter `name:`/`description:`/`tools:`/`model:` is altered/dropped by the cut.

### P-KEEP — the always-on architect KEEP rules are still inline (architect availability-losslessness)
```bash
grep -qiE 'Write a concrete, buildable design artifact|writes plans, not code' substrate/CAPTAIN_DAEDALUS.md && echo "OK §1 one-job" || echo "DROPPED §1"
grep -qiE 'design question|artifact path|research input' substrate/CAPTAIN_DAEDALUS.md && echo "OK §2 brief" || echo "DROPPED §2"
grep -qiE 'Problem restatement|Verification probes|Self-assessed weak points|Out of scope' substrate/CAPTAIN_DAEDALUS.md && echo "OK §3 design-output contract" || echo "DROPPED §3"
grep -qiE 'Code, feature-branch commits|do not have the .Agent. tool|sub-agents cannot dispatch' substrate/CAPTAIN_DAEDALUS.md && echo "OK §4 what-you-dont-write" || echo "DROPPED §4"
grep -qiE 'Workmanlike|PRINCIPAL.*not .Colonel' substrate/CAPTAIN_DAEDALUS.md && echo "OK §5 voice" || echo "DROPPED §5"
grep -qiE 'Restatement gate|restate the brief' substrate/CAPTAIN_DAEDALUS.md && echo "OK §6.1 restatement-gate" || echo "DROPPED §6.1"
grep -qiE 'Self-assessed weak points|silently smoothing|over-apologizing' substrate/CAPTAIN_DAEDALUS.md && echo "OK §6.2 weak-points-gate" || echo "DROPPED §6.2"
grep -qiE 'Consume research' substrate/CAPTAIN_DAEDALUS.md && echo "OK §6.3 consume-research" || echo "DROPPED §6.3"
grep -qiE 'WebSearch|training data is out of date' substrate/CAPTAIN_DAEDALUS.md && echo "OK §6.4 websearch" || echo "DROPPED §6.4"
grep -qiE 'Heartbeat-and-read-before-write|At dispatch entry' substrate/CAPTAIN_DAEDALUS.md && echo "OK §6.5 heartbeat" || echo "DROPPED §6.5"
grep -qiE 'status: <completed .* refused>|verdict: <pass' substrate/CAPTAIN_DAEDALUS.md && echo "OK §7 verdict-format" || echo "DROPPED §7"
grep -qiE 'Authorship attribution|names .*the PRINCIPAL' substrate/CAPTAIN_DAEDALUS.md && echo "OK §8 authorship" || echo "DROPPED §8"
grep -qiE 'field notes, not doctrine|Standby, run' substrate/CAPTAIN_DAEDALUS.md && echo "OK §9 when-wrong" || echo "DROPPED §9"
```
**Pass:** all always-on KEEP rules resolve inline. **Falsifies if:** any always-on architect rule was relocated off-disk (availability-losslessness violated). The load-bearing trio for this seat: §3 (design-output contract), §6.1 (restatement gate), §6.2 (self-assessed weak points) — a drop of any of these guts the architect identity.

### P-INDEX — the relocation index exists, is always-loaded core, covers every relocation; NO routing map (CAPTAIN, not orchestrator)
```bash
grep -nE '^### 6\.0 |Relocation index' substrate/CAPTAIN_DAEDALUS.md   # the §6.0 index exists, at top of §6
for m in canonical-code-block-fix credential-flow-design principal-gate-design \
         canonical-template-alignment probe-grounding ssot-with-why api-docs-dont-generalize; do
  grep -q "$m" substrate/CAPTAIN_DAEDALUS.md && echo "OK index-or-stub: $m" || echo "MISSING: $m"
done
grep -c 'Routing map' substrate/CAPTAIN_DAEDALUS.md   # expect 0 — DAEDALUS is a CAPTAIN, not an orchestrator
```
**Pass:** §6.0 relocation index present (at top of §6, before §6.1); every CONDITIONAL module appears in an index row (or its stub); NO routing map present (returns 0 — the index-vs-routing-map call, assumption 1 / Q1). **Falsifies if:** index absent, a relocation has no index row, OR a routing map was added (wrong shape for a non-orchestrator CAPTAIN — the Arc-47 op-disc precedent governs, not the Arc-45/48 orchestrator one).

---

## §5 — Build steps (for ADA — ordered; the cut sequence)

**Step 0 (process hazard — DO THIS FIRST).** Confirm cwd is the worktree (`git -C C:/Users/denso/claude_projects/the-stoa/.claude/worktrees/arc-49-build rev-parse --show-toplevel` resolves to the worktree, branch `arc-49/build`). Use ABSOLUTE worktree paths for EVERY Write. After each write, verify it landed in the worktree (`ls <worktree-path>` + `git -C <worktree> status --short`) and NOT in main (`git -C C:/Users/denso/claude_projects/the-stoa status --short` should NOT show your edit). The Write-resolves-against-main-root hazard hit ARGUS last arc; this gate catches it before it compounds. **RECURSION NOTE (carried from the dispatch): you are ADA building the cut of the DAEDALUS role file. No special handling — the live DAEDALUS that produced this design loaded from the DEPLOYED (full, pre-cut) role file; the source you edit is not redeployed until engagement-end.**

1. **Create the 7 module files** (`substrate/modules/*.md`), populating from the live source line-ranges in §2.3 / §3.2. Each module: stable `# <Title>` first line (P-RECOMPOSE keys on it) → provenance header (cites this design + stoa--xyb epic, mirroring the Arc-47/48 modules) → relocated discipline body verbatim-tightened, INCLUDING the discipline's own cross-refs (they travel WITH it — §3.6) + the embedded empirical (move-with; compress the `stoa--`-ticketed ones to `Anchor:` after the C-1 `bw show` gate; keep the in-prose stellation narrative anchors VERBATIM — §3.3). `probe-grounding.md` co-locates §6.9 + §6.9.3' + §6.9.3'' (three subsections, one module). Run op-disc §33 per-module line-count discipline. NO author field (P-AUTH). **Verify NO basename collision** with the 28 existing (P-OWNERSHIP-NOCOLLIDE — the 7 are disjoint per §3.8). **§6.8 Anchor note (§3.3.1):** the `canonical-template-alignment.md` empirical Anchor is `stoa--5sr` (+ a note "discipline shipped Arc 40 alongside stoa--utn"), NOT `stoa--utn` as the empirical home.
2. **No C-2 archive needed** (§3.4 — zero firm C-2; the in-prose narrative anchors move verbatim into their modules, self-contained). Skip the `bw create` step the prior three cuts ran.
3. **Cut the slim core** (`substrate/CAPTAIN_DAEDALUS.md`):
   - PRESERVE the YAML frontmatter (1–6) + role-identity table + identity para (8–20) VERBATIM (P-AUTH frontmatter check).
   - Add **§6.0 relocation index** at the TOP of §6 (immediately after the `## 6. Disciplines...` heading, before §6.1). Populate from §3.2. NO routing map (P-INDEX asserts this).
   - For each relocated §6.x subsection, replace the body with the stub + paired `<!-- MODULE-INLINE:<name> -->` … `<!-- /MODULE-INLINE:<name> -->` marker (§2.7.1 first literal for single-subsection modules: §6.2.1'/§6.6/§6.7/§6.8/§6.10/§6.11; §2.7.1 second literal for the §6.9 cluster — three heading-line stubs, ONE marker, into `probe-grounding.md`).
   - Keep the cross-ref-cited subsection HEADING LINES real (`### 6.7`, `### 6.8`, `### 6.9.3''`, `### 6.11`) so the ADA/VERA/op-disc cross-refs resolve (P-XREF). Preserve the LITERAL apostrophes in §6.2.1'/§6.9.3'/§6.9.3'' headings (P-STUB note).
   - **§6.1–§6.5 STAY INLINE (KEEP):** do NOT stub them. §6.1 (restatement gate) + §6.2 (weak-points gate) + §6.3 (consume-research) + §6.4 (WebSearch) + §6.5 (heartbeat) stay live, interleaved in numeric order among the §6.x stubs. **§6.2's two extension-pointers (104–106) REPOINT** at the modules + §6.0 index (§3.6) — keep the one-line "extends" prose, rewrite to name `canonical-code-block-fix.md` / `ssot-with-why.md`.
   - KEEP-TIGHTEN §1/§2/§3/§4/§5/§6.1/§6.2/§6.3/§6.4/§6.5/§7/§8/§9 (§3.7). NO standalone C-1 deletions (zero standalone provenance in KEEP sections — §3.3). The 1 SPLIT (§6.2 repoint) is the only cross-ref handling in the slim core.
4. **Add the install.sh DAEDALUS owned-set + recompose call** (§6 — substrate-tooling source, gauntlet-gated, correctly inside this arc):
   - Add `DAEDALUS_MODULES="canonical-code-block-fix credential-flow-design principal-gate-design canonical-template-alignment probe-grounding ssot-with-why api-docs-dont-generalize"` next to `POLYBIUS_MODULES`/`OPDISC_MODULES`/`PLINY_MODULES` (L1004–1006).
   - **Construct the DAEDALUS deploy path:** add `DEST_DAEDALUS="${DEST_AGENTS_DIR}/CAPTAIN_DAEDALUS${NAME_SUFFIX}.md"` (mirroring the L1023 loop `dest=`) — set it near the other `DEST_*` vars OR at the recompose call site (§2.7.2-a).
   - **ORDERING (§2.7.2-b):** move the four recompose calls (the three existing + the new DAEDALUS call) into a `if [ "$TARGET" = "subproject" ]` block placed AFTER the `CAPTAIN_NAMES` deploy loop (L1037), so `CAPTAIN_DAEDALUS_<sub>.md` exists when its recompose runs. (Option (i) §6.5 — relocate only the call lines; the function definition stays at L895.) Add `recompose_module_inline "$DEST_DAEDALUS" "$DAEDALUS_MODULES"` as the fourth call.
   - **NO function-body change** — the two-set machinery (Arc 47) handles the fourth owner unchanged. Update the L887–893 + L1000–1001 comments to say FOUR files now recompose.
   - Smoke-test against a throwaway synthetic parent (P-RECOMPOSE + P-RECOMPOSE-PATH + P-RECOMPOSE-NEG + P-OWNERSHIP + P-OWNERSHIP-NOCOLLIDE) before considering the step done.
5. **Cross-ref re-point sweep** (verification, not churn — numbers preserved): run P-XREF + **P-SPEC-XREF** (the validate-spec resolver against SPECIFICATION.md — assert zero DAEDALUS refs matched + totals 156/56 unchanged). Confirm the four substrate-cited §6.x cites (ADA/VERA/op-disc) still resolve to stub heading lines.
6. **Run all probes** (P-FLOOR, P-COND, P-STUB, P-XREF, P-SPEC-XREF, P-RECOMPOSE, P-RECOMPOSE-PATH, P-RECOMPOSE-NEG, P-OWNERSHIP, P-OWNERSHIP-NOCOLLIDE, P-AUTH, P-KEEP, P-INDEX) as a self-check before returning to PLINY. Clean up any temp files (`spec_refs_postcut.jsonl`, recompose `.bak`s, `$TMP`).
7. **Commit** with `Co-Authored-By: CAPTAIN_ADA_the-stoa <captain-ada@the-stoa.local>` per op-disc §28. (The slim-core cut + the 7 modules + the install.sh DAEDALUS owned-set land as one coherent commit, or the install.sh extension as a trailing commit if ADA prefers a clean tooling/canon split — ADA's call; both are this arc.)

---

## §6 — install.sh DAEDALUS owned-set + recompose (the fourth-owner extension + the no-DEST-var wrinkle)

### 6.1 Why CAPTAIN_DAEDALUS recompose is required (architect losslessness at subproject tier)

CAPTAIN_DAEDALUS deploys at all 3 tiers via the `CAPTAIN_NAMES` loop (L1021–1034), suffixed at subproject (`CAPTAIN_DAEDALUS_<subproject>.md`). At subproject tier `DEST_MODULES_DIR=""` (no modules deployed) AND a subproject seat's `Read .claude/modules/X.md` does not resolve reliably (the Arc-45 probe finding). So a slim subproject CAPTAIN_DAEDALUS pointing at 7 modules absent from the subproject's `.claude/` would break losslessness for the architect seat at that tier. The fix is the same recompose-inline POLYBIUS + op-disc + PLINY use: re-inline the 7 module bodies at their markers at subproject tier. The mechanism (`recompose_module_inline()`, the awk state-machine, the 5 FAIL-LOUD checks A–E, idempotency, the two-set partition) ALREADY EXISTS (Arc 45 + 47 + 48, install.sh L894–998) — this arc REUSES it with a fourth call.

### 6.2 CAPTAIN_DAEDALUS is `sed`'d ({{NAME_SUFFIX}}), not `cp`'d — recompose runs cleanly on it

The `CAPTAIN_NAMES` loop `sed`-substitutes `{{NAME_SUFFIX}}` (L1031) into the deployed CAPTAIN file. The recompose runs IN PLACE on the deployed `$DEST_DAEDALUS` regardless. The markers are inert through the sed (the sed substitutes only `{{NAME_SUFFIX}}`, which appears in no marker). **The wrinkle (§2.7.2):** `$DEST_DAEDALUS` is NOT pre-set by a dedicated deploy step (unlike `$DEST_POLYBIUS` L818 / `$DEST_PLINY` L819 / `$DEST_OPERATING_DISCIPLINES` L866) — it deploys inside the loop with a local `dest=` var (L1023). So the recompose call MUST construct the path (`DEST_DAEDALUS="${DEST_AGENTS_DIR}/CAPTAIN_DAEDALUS${NAME_SUFFIX}.md"`) AND run AFTER the loop has written it.

### 6.3 The slim-core clause that makes the strategy auditable (mirrors Arc-45/47/48 §6.3)

The slim core's §6.0 (or a one-line note near the relocation index) carries the tier-awareness rule so the strategy is visible to a reader, not buried in install.sh:

> **Subproject-tier module access (per design-arc-49 §6):** at subproject tier the CONDITIONAL §6 disciplines are re-inlined into this file at deploy time (install.sh recompose at the `<!-- MODULE-INLINE:<name> -->` markers) — subproject seats do NOT `Read .claude/modules/<X>.md` (the path does not resolve reliably; claude-code #56686/#31546/#29423). At user/project tier the `Read` channel applies and the markers are inert. Anchor: stoa--xyb + design-arc-45 §6 probe (the proven mechanism this arc extends to CAPTAIN_DAEDALUS).

### 6.4 The FOURTH owned-set — exact change (the minimal extension; NO function-body change)

The current function (L895–998) already takes `(role_file, owned_basenames)` and runs the two-set awk (Arc 47 r3, extended to a third owner Arc 48). The changes:

**Add the DAEDALUS owned-set + the fourth call:**
```bash
POLYBIUS_MODULES="onboarding sub-project-spawning pair-programmer-authoring pair-programming-prototyping substrate-update-check"
OPDISC_MODULES="two-polybius-coordination autonomous-mode-setup sub-agent-transcript-discipline bw-fit-matrix oss-dep-and-latency credential-discipline-detail bw-upgrade mechanical-inspection-split multi-team-interop four-layer-identity substrate-component-design jsdom-timing-discipline"
PLINY_MODULES="ada-brief-preamble sub-agent-watchdog per-worktree-venv post-strabo-vera incomplete-unverifiable-routing smoke-beat-deploy-check background-dispatch-hygiene pre-branch-hygiene arc-close-hygiene seat-identity-brief pliny-polling-pattern"
DAEDALUS_MODULES="canonical-code-block-fix credential-flow-design principal-gate-design canonical-template-alignment probe-grounding ssot-with-why api-docs-dont-generalize"
DEST_DAEDALUS="${DEST_AGENTS_DIR}/CAPTAIN_DAEDALUS${NAME_SUFFIX}.md"   # no dedicated deploy var — construct it (mirrors L1023 loop dest=)
recompose_module_inline "$DEST_POLYBIUS" "$POLYBIUS_MODULES"
recompose_module_inline "$DEST_OPERATING_DISCIPLINES" "$OPDISC_MODULES"
recompose_module_inline "$DEST_PLINY" "$PLINY_MODULES"
recompose_module_inline "$DEST_DAEDALUS" "$DAEDALUS_MODULES"
```

**Key precision (the two-set discipline HOLDS for the fourth owner):**
- **Check A** still tests `name in global_exists` — the GLOBAL set, now **35 module sources (5 + 12 + 11 + 7) minus README**. A DAEDALUS marker naming any real module resolves; a marker naming a non-existent module FAILs loudly (P-RECOMPOSE-NEG). Owner-agnostic; does NOT narrow with the DAEDALUS owned-set.
- **Checks B/D** iterate/count the DAEDALUS `owned[]`/`nowned` for the `$DEST_DAEDALUS` call. A cross-owner module (op-disc's `credential-discipline-detail` during DAEDALUS recompose) is not in DAEDALUS's `owned[]`, so Check B does not flag it (P-OWNERSHIP).
- **NO basename collision across the four owner-sets** (P-OWNERSHIP-NOCOLLIDE) — the obligation the multi-owner partition carries, extended to the fourth set. The 7 DAEDALUS basenames are disjoint from the 28 existing (§3.8); the near-miss `credential-flow-design` (DAEDALUS) vs `credential-discipline-detail` (op-disc) are distinct basenames — confirmed.

**Why this is the minimal correct extension:** the Arc-47 design's "data-driven property" claim is realized again — the DAEDALUS cut adds a `DAEDALUS_MODULES` var + a `DEST_DAEDALUS` path-construction line + a fourth call, with ZERO new code path in the function. The ONLY genuinely-new mechanic vs Arc 48 is the path construction (DAEDALUS has no dedicated `DEST_*` var) + the ordering (call must follow the deploy loop) — §6.5 + P-RECOMPOSE-PATH cover it.

### 6.5 Recompose placement + the dry-run path (the ordering fix)

The four recompose calls go in a `if [ "$TARGET" = "subproject" ]` block placed AFTER the `CAPTAIN_NAMES` deploy loop (L1037). **This is a change from the current placement** (the recompose block + calls currently sit at L894/L1004–1009, BEFORE the CAPTAIN loop at L1014–1037). The POLYBIUS/PLINY/op-disc files all deploy BEFORE L894 (L849/L851/op-disc-cp), so moving the CALLS later does not break them (their files already exist by L1037). DAEDALUS's file does NOT exist until the loop runs — hence the calls must follow it.

**ADA's two options (option (i) recommended, lower-risk):**
- **(i)** Keep the function definition where it is (L895, inside the existing `if subproject` wrapper) OR hoist it; MOVE only the four `recompose_module_inline` call lines + the four `*_MODULES` vars + the `DEST_DAEDALUS` line to a NEW `if [ "$TARGET" = "subproject" ]` block AFTER L1037. (Relocates ~9 lines; the function body is untouched.)
- **(ii)** Move the entire `CAPTAIN_NAMES` deploy loop (L1014–1037) to BEFORE the recompose block (L894). (Larger move; risks reordering side-effects in the deploy sequence.)

§5 Step 4 specifies option (i). The function's existing `$DRY_RUN` guard (L922–925) prints the plan and returns without requiring the file to exist — works unchanged for the fourth call (it prints `owned:${_owned_basenames}` = the DAEDALUS owned-set). The dry-run plan now shows all FOUR owned-sets. FAIL-LOUD semantics (rm-both-files-on-error) apply per-call: a DAEDALUS recompose failure removes the partial DAEDALUS tmp AND the slim `$DEST_DAEDALUS`, exits 2, aborts the deploy — install.sh never ships a partial/slim CAPTAIN_DAEDALUS to a subproject (P-RECOMPOSE-NEG).

### 6.6 Check E (body-contains-a-marker) interaction with CAPTAIN_DAEDALUS content

Check E fails if a module BODY contains a literal `^<!-- /?MODULE-INLINE:` line (would corrupt recompose). **Caveat for ADA, load-bearing for THIS file:** the §6.8 source (→ `canonical-template-alignment.md`) contains the `diff <(sed -n '...p' <design.md>) <(sed -n '...p' <design.md>)` mechanical-check example AND prose ABOUT canonical templates + markers — VERIFY at build time that §6.8's body contains ZERO literal `^<!-- /?MODULE-INLINE:` full-line shapes (it uses `<!-- cite: ... -->` comment shapes, which are NOT `MODULE-INLINE` markers — Check E only matches the exact `MODULE-INLINE` full-line). The §6.2.1' / §6.9 / §6.9.3' / §6.9.3'' / §6.10 / §6.11 bodies carry `<!-- cite: ... -->` comment lines (the cross-ref pointers) — confirm NONE is a `MODULE-INLINE` line (they are `cite:` shapes). Check E catches any ADA-introduced one at deploy; P-RECOMPOSE exercises the happy path. **Special note:** the `<!-- cite: -->` comment blocks travel INTO the modules (they are the disciplines' own cross-refs — §3.6); they are inert in the module body (not MODULE-INLINE markers), so they recompose-inline harmlessly.

---

## §7 — Self-assessed weak points (esp. anywhere losslessness is at risk for the architect seat)

1. **The CAPTAIN-gets-index-only call (assumption 1) generalizes the Arc-47 op-disc precedent to a NEW file class (a CAPTAIN role file) for the first time — and it is the load-bearing structural call ARGUS audits.** Arc 47 gave op-disc index-only because op-disc dispatches nothing; Arc 45/48 gave POLYBIUS/PLINY both tables because they ARE orchestrators. DAEDALUS is the first CAPTAIN cut, and CAPTAINs are non-orchestrators (no `Agent` tool). *Why this shape anyway:* modules/README §4.1 defines the routing map as an ORCHESTRATOR artifact ("at dispatch time, what does this task need?") and §1 says the routing map "stays inline in orchestrator core"; DAEDALUS structurally cannot dispatch (its own §3/§4/§6.5 cite the runtime constraint `u--7yg.12`), so its CONDITIONAL modules are read by DAEDALUS-at-point-of-need (the seat hitting the design-task-type trigger), making the per-stub `Read` pointer the correct dispatch-time signal — identical to op-disc. The single distinction (op-disc is read by every seat; DAEDALUS by one seat) makes the index-only call CLEANER here, not weaker. P-INDEX asserts the index present + zero routing map. The residual risk is whether ARGUS wants the index-only shape ratified as the STANDARD for all future CAPTAIN cuts (ARGUS/ADA/VERA/CATO etc.) — I judge yes (all CAPTAINs are non-orchestrators), but it is the first instance, so I surface it (residual Q1).

2. **The no-`DEST_DAEDALUS`-var path-construction + ordering is the ONE genuinely-new install.sh mechanic this arc adds beyond the proven Arc-48 fourth-call pattern — and a mis-construction silently no-ops the recompose (LOST CANON at subproject tier).** POLYBIUS/PLINY/op-disc each had a dedicated `DEST_*` var written before the recompose block; DAEDALUS deploys in the `CAPTAIN_NAMES` loop with no such var, AND the recompose block currently runs BEFORE that loop. *Why this shape anyway:* DAEDALUS is a CAPTAIN (agent envelope), deployed by the generic CAPTAIN loop — adding a dedicated `DEST_DAEDALUS` deploy step would special-case one CAPTAIN against the others (churn + asymmetry), so constructing the path at the recompose call site (mirroring the loop's `dest=`) + moving the calls after the loop (option (i), relocating only ~9 call lines) is the minimal correct fix. P-RECOMPOSE-PATH (static: var set + call-after-loop) + P-RECOMPOSE (live: the 7 markers re-inline non-empty bodies) together catch both the path-construction error and the ordering error end-to-end on a throwaway target. This is the single most important install.sh surface — and it is the seat-specific reason DAEDALUS's recompose is NOT a literal copy of Arc-48's PLINY recompose.

3. **The in-prose stellation-Pass-10 narrative anchors (§6.2.1' / §6.9.3' / §6.9.3'' / §6.10 / §6.11) have NO standalone bw ticket and move VERBATIM into their modules — if a module-author "tightens" them into a compressed Anchor pointing at a non-existent ticket, the empirical record is silently lost.** These anchors describe stellation Pass-10 arc findings (Arc 2 r4, Arc 3 r1/rev2, Arc 4 WP13, Arc 5 ARGUS-rev2, etc.) that exist ONLY as narrative in DAEDALUS's own §6 prose — they are not `stoa--` tickets. *Why this shape anyway:* C-2 archive (a child ticket) would DUPLICATE the narrative, not preserve it more recoverably, because the discipline RELOCATES WHOLE and the narrative travels INSIDE the module verbatim — the module IS the surviving copy (§3.4 rationale; contrast Arc-48's §5.4 cross-repo `ariadne--b93` which had NO in-repo home at all). The build step (§5 Step 1) explicitly says "keep the in-prose stellation narrative anchors VERBATIM"; P-RECOMPOSE asserts each module body's first heading appears (a proxy for body presence), and P-COND asserts each module is non-empty. The residual risk is an ADA judgment error compressing a verbatim-narrative anchor into a fake Anchor — flagged so ARGUS confirms the move-with-verbatim disposition (residual Q2) and so VERA spot-checks a sample module body for the narrative anchors' presence.

4. **The estimated floor (~150–200) is the most aggressive reduction ratio of the four cuts (~72%) — a reviewer may read it as "cut too deep / a KEEP rule dropped."** *Why this shape anyway:* DAEDALUS's bloat is unusually concentrated (81% in §6, almost all design-task-type-conditional), so a deep reduction is the honest output. The always-on architect core is genuinely a tight contract (brief → restate → design → self-assess → verdict). P-KEEP independently asserts each of the 13 always-on rules (one-job, brief, the §3 design-output contract, what-you-don't-write, voice, the §6.1 restatement gate, the §6.2 weak-points gate, consume-research, WebSearch, heartbeat, verdict-format, authorship, when-wrong) is still inline; P-FLOOR guards the low end (< 120 = suspicious). The load-bearing trio (§3 design-output contract + §6.1 restatement gate + §6.2 weak-points gate) is the architect identity — P-KEEP guards all three by name. The reduction being the largest of the four is a property of THIS file's CONDITIONAL/always-on ratio, not over-aggression.

5. **The §6.9 cluster co-locates THREE subsections (§6.9 + §6.9.3' + §6.9.3'') in ONE `probe-grounding.md` module — if ADA splits them into three modules (or the stub keeps only one heading line), the §6.9.3'' cross-ref from VERA §212/§217 breaks OR the module count drifts from 7.** *Why this shape anyway:* §6.9.3' and §6.9.3'' explicitly "extend §6.9 clause 3" — they are one coherent probe-grounding discipline, so one module is the right home (mirroring Arc-48's `pre-branch-hygiene.md` co-locating §5.9+§5.9.4 and `arc-close-hygiene.md` co-locating §5.10+§5.11). The stub keeps all THREE heading lines (§2.7.1 second literal) with ONE marker pair, so §6.9.3'' resolves AND the recompose re-inlines all three bodies once. P-COND (7 modules, asserts `probe-grounding` is ONE file), P-STUB (all 3 §6.9.x heading lines present), P-XREF (§6.9.3'' resolves) together catch a wrong split. The residual risk is the literal double-prime in `§6.9.3''` — the heading text must carry exactly two apostrophes for the VERA cross-ref to match; P-STUB's grep escapes them explicitly and flags ADA to verify the literal apostrophes survive.

---

## §8 — Residual questions for ARGUS

1. **The CAPTAIN-gets-index-only call (assumption 1; weak point 1).** Does ARGUS concur that CAPTAIN_DAEDALUS (a non-orchestrator CAPTAIN) gets a relocation INDEX ONLY (the Arc-47 op-disc shape), NOT a routing map (the Arc-45/48 orchestrator shape) — because DAEDALUS dispatches nothing (no `Agent` tool) and its CONDITIONAL modules are read by DAEDALUS-at-point-of-need? And does ARGUS concur this should be the STANDARD shape for the future CAPTAIN role-file cuts (ARGUS/ADA/VERA/CATO etc., all non-orchestrators)? This is the first CAPTAIN cut and the load-bearing structural generalization.

2. **The move-with-verbatim disposition for in-prose narrative anchors (weak point 3; §3.4).** Does ARGUS concur the stellation-Pass-10 narrative anchors (§6.2.1' / §6.9.3' / §6.9.3'' / §6.10 / §6.11 — no standalone `stoa--` ticket) are losslessly homed by moving VERBATIM into their modules (the module IS the surviving copy), NOT by C-2 child-ticket archive? My judgment: C-2 would duplicate not preserve, because the discipline relocates whole and the narrative travels inside it (unlike Arc-48's §5.4 cross-repo anchor which had no in-repo home).

3. **The no-`DEST_DAEDALUS`-var install.sh mechanic (weak point 2; §6.4/§6.5).** Does ARGUS concur the path-construction (`DEST_DAEDALUS="${DEST_AGENTS_DIR}/CAPTAIN_DAEDALUS${NAME_SUFFIX}.md"`) + the ordering fix (move the four recompose calls after the `CAPTAIN_NAMES` deploy loop, option (i)) is the minimal correct extension — vs special-casing a dedicated `DEST_DAEDALUS` deploy step? And is P-RECOMPOSE-PATH (static var-set + call-after-loop check) the right NEW probe to catch the no-op-recompose hazard the missing var introduces?

4. **The §6.2-extension-pointer repoint (§3.6; weak point / A1).** §6.2 (KEEP) carries forward-pointers to the now-relocated §6.2.1' + §6.10. I REPOINT them at the modules (keep the one-line "extends" prose, name the module + §6.0 index). Does ARGUS concur repoint-not-drop is right (the extensions are real always-relevant signposts even though the detailed discipline is conditional)?

5. **The ambient-vs-conditional boundary for §6.6/§6.7 (A2) + the §6.9 probe cluster (A4).** I RELOCATE §6.6 (credential) + §6.7 (PRINCIPAL-gate) despite their "load-bearing" headings (severity-when-fired ≠ frequency-of-firing — they fire only on credentialed-ops / PRINCIPAL-gating designs). I RELOCATE the §6.9 probe-grounding cluster (every design writes probes, but the GROUNDING discipline is read only when probes are regex/tool-shaped). Does ARGUS concur both calls — or is any of §6.6/§6.7/§6.9 actually always-on (read on a typical feature/refactor design)? These are the genuine judgment calls.

---

## §9 — Out of scope

- **Cutting any OTHER CAPTAIN role file** (ARGUS / ADA / VERA / CATO / STRABO / BARTLEBY / HERALD / CURATOR / ZENO / TIRO). This arc cuts CAPTAIN_DAEDALUS only — the LAST relocation cut. The remaining CAPTAIN cuts (if any) + the always-on prose-compression are the capstone block (stoa--xyb.9). The CAPTAIN-gets-index-only call (Q1) is designed to generalize to those future cuts with zero new structural work.
- **Prose-compression of always-on KEEP sections (FLAGGED for stoa--xyb.9, NOT actioned here).** Per the dispatch, the cut is relocation-only; prose-compression of always-on KEEP sections happens in ONE reviewed capstone pass (.9). Candidates spotted in CAPTAIN_DAEDALUS's KEEP sections, recommended for ADDITION to stoa--xyb.9:
  - **§6.5 (heartbeat-bw, ~18 lines)** — the 4-beat list + the read-before-write + the two prohibitions (Monitor / run_in_background) are operational, but the prohibition prose (183–185) restates op-disc §18.4 + cites issue #23154 verbosely; losslessly compressible to a one-line "Monitor + run_in_background forbidden (orphan-bug #23154; op-disc §18.4)" cross-ref. ~6 lines saved.
  - **§3 (what you write to disk, ~13 lines)** — the 5-part contract is load-bearing and must stay, but each part's explanatory clause (e.g. "This is the load-bearing pre-work gate (see §6.1)") could tighten to a bare cross-ref. ~3 lines.
  - **§2 (the brief, ~14 lines)** — the operating-mode-flag paragraph (43) restates op-disc §10's escalation triggers; compressible to a one-line cross-ref. ~3 lines.
  These are FLAGS for .9, NOT actioned in this cut.
- **The SPECIFICATION.md L553 backtick-form cite to `CAPTAIN_DAEDALUS.md §6.8`** (§3.1.2). The cite is human-readable but INVISIBLE to the validate-spec resolver (backtick between `.md` and `§`). NOT a regression this cut introduces (it was unmatched pre-cut); the §6.8 heading title is preserved verbatim in `canonical-template-alignment.md` so the L553 prose stays accurate. A one-edit fix to SPEC L553 (move the backtick to wrap the whole `File §N` token, or drop the inner backtick) is flagged for a future spec-audit pass, out of this arc's cut scope.
- **Substrate-self-apply re-sync** of the-stoa's deployed `.claude/agents/CAPTAIN_DAEDALUS.md` (lags source by this arc + Arc 44/45/46/47/48). User-tier POLYBIUS housekeeping per MAJOR_POLYBIUS §18.1.
- **Building the enforcement layer** (stoa--xyb.5). The relocation-index + MODULE-INLINE marker formats are hook-parseable (designed so), but the hook is not built here.
- **A standalone `DEST_DAEDALUS` deploy step** (special-casing DAEDALUS against the other CAPTAINs in the deploy loop). This cut constructs the path at the recompose call site instead (§6.4) — the deploy loop stays generic.

---

*Self-assessed weak points are in §7. Residual questions for ARGUS are in §8. This is rev1 (the 4th and LAST relocation cut of the debloat epic); ARGUS audits it next (LOST-CANON primary, architect seat), then ADA reads THIS file to build. The recursion note (DAEDALUS designs its own cut) needs no special handling — the live agent loads from the deployed pre-cut file; this design slimmed the source faithfully.*
