# Arc 4 (Arc 47) — operating-disciplines.md debloat cut — design rev1

**Ticket:** stoa--xyb.8 (engagement epic stoa--xyb)
**Author:** Denson Smith (the PRINCIPAL — design synthesis, structural choices, relocation ledger)
**Seat:** CAPTAIN_DAEDALUS_the-stoa
**Builds on:** Arc 44 (composition-layer mechanism: `substrate/modules/` glob deploy + `modules/README.md` 3 channels / 3 relocation classes + op-disc §33 thin rule); Arc 45 (MAJOR_POLYBIUS.md cut — the PROVEN stub/marker/recompose pattern; `install.sh` `recompose_module_inline()` shipped data-driven); Arc 46 (hooks tier + op-disc §34 trigger-payload rule).
**Acceptance bar:** LOSSLESS-ON-CANON at ALL tiers (user / project / subproject) for the WHOLE TEAM. operating-disciplines.md is the UNIVERSAL layer every seat loads — POLYBIUS, PLINY, every CAPTAIN, every pair-programmer Major. ARGUS's primary audit target is LOST CANON, whole-team.
**Recalibrated criterion (PRINCIPAL-ratified):** the lossless-floor is an OUTPUT measured per file, NOT a fixed line target. Falsify on LOSSLESS-COMPLETENESS (every chunk homed + recoverable), NOT a line number. Do not cut a load-bearing always-on rule to hit a number. The empirical post-cut floor is REPORTED (§3.10), not targeted.

---

## §1 — Problem restatement (pre-work gate)

`substrate/operating-disciplines.md` is **2156 lines** — the worst offender in the substrate, and uniquely costly because it is the UNIVERSAL-team layer every seat loads on activation. It grew from 2110 at epic start via §33 (Arc 44) + §34 (Arc 46). At 2156 lines it is far over the 25k-token harness read cap (the live file paginates across multiple reads; a CAPTAIN that needs to ground against a single discipline pays the read cost of the whole monolith).

The diagnosis is the same empirical-anchor + provenance accretion the POLYBIUS cut diagnosed, amplified: every discipline §N carries a rule + worked example + a multi-paragraph "N=1 provenance + accretion path" + a "Cross-references" subsection. The *actionable always-on* canon — the rules a seat needs on every turn — is roughly a quarter of the lines. The rest splits into (a) procedures only SOME seats need only SOMETIMES (CONDITIONAL), (b) the why/empirical record (PROVENANCE), and (c) content duplicated elsewhere (DUPLICATE).

This arc applies the Arc-1 debloat method (3 relocation classes — CONDITIONAL → disk module, PROVENANCE → bw cite, DUPLICATE → pointer) to op-disc section by section, **for the whole file**, and extends the Arc-2 subproject-recompose mechanism to cover op-disc as a second recompose source. The KEEP bucket is the universal always-on operational core every seat needs every turn; the RELOCATE buckets are everything genuinely conditional, historical, or duplicated.

### 1.1 Imported assumptions (named per §6.1 of the seat envelope — real briefs have implicit scope)

1. **op-disc is NOT an orchestrator — it gets a RELOCATION INDEX but NOT a routing map.** This is the load-bearing refinement of the Arc-1/Arc-2 pattern for this file (§2.2). The Arc-1 composition layer pairs a routing map (dispatch-time: task-type → module → channel) with a relocation index (audit-time: relocated-content → home → class). The routing map is an ORCHESTRATOR artifact — it answers "at dispatch time, what does this task need?" op-disc does not dispatch anything; its CONDITIONAL modules are read by the SEAT THAT NEEDS THEM at the moment that seat hits the task (a seat entering autonomous mode reads `autonomous-mode-setup.md`; a seat hitting credentialed work reads `credential-discipline-detail.md`). So op-disc carries the relocation index (the losslessness-recovery artifact ARGUS audits) but NO routing map. The per-section stub's "recover via Read" pointer IS the dispatch-time guidance, inline at the point of need — that is the correct shape for a non-orchestrator file. (Flagged for ARGUS as residual Q1.)

2. **CONDITIONAL content relocates to NEW disk modules under `substrate/modules/`** alongside the 5 Arc-2 POLYBIUS modules + README. This arc CREATES + POPULATES the new op-disc modules. Naming + per-module contents are in §2.3.

3. **The shared `substrate/modules/` dir forces a module-OWNERSHIP partition in install.sh** (§2.7 + §6). `recompose_module_inline()` today scopes Check B (module-exists-but-no-marker) to the GLOBAL `substrate/modules/*.md` glob. Once op-disc modules share the dir, POLYBIUS's recompose would FALSE-POSITIVE Check B on the op-disc modules (they carry no POLYBIUS marker). The fix is to scope each recompose call to a per-call OWNED-module-set. This is the load-bearing install.sh extension of this arc.

4. **op-disc deploys at ALL three tiers** (user / project / subproject) — confirmed live at install.sh L964-980 (`cp` to `<DEST_DIR>/operating-disciplines.md`, unconditional, all tiers). At subproject tier the modules dir is NOT deployed (`DEST_MODULES_DIR=""`) AND a subproject seat's `Read .claude/modules/X.md` does not resolve reliably (the Arc-2 probe finding, claude-code #56686/#31546/#29423). So op-disc's CONDITIONAL modules MUST recompose-inline at subproject tier exactly as POLYBIUS's do — op-disc is recompose-eligible and the recompose must run on `$DEST_OPERATING_DISCIPLINES`.

5. **Section numbers are PRESERVED via stubs, NOT renumbered.** op-disc §N is cross-referenced by EVERY role file, every module, the templates, the hooks, the skills, and op-disc's own internal cross-refs. The cross-ref graph (§3.1, grepped live this design phase) shows nearly every top-level §N is cited from an active substrate file. Renumbering would break the entire substrate's cross-ref graph. Every relocated section leaves a numbered stub so all `operating-disciplines.md §N` cites still resolve. (Arc-2 precedent; PRINCIPAL-ratified there as CONCUR.)

6. **op-disc has NO author-like frontmatter field and the new modules must carry none** (P-AUTH guards). op-disc's content — the synthesis — is the PRINCIPAL's per the immutable authorship rule; cited empirical anchors are attributed to their tickets, which is source-citation not authorship.

The restatement converges with the brief. The one place it does more than paraphrase — the routing-map-vs-relocation-index distinction for a non-orchestrator file (assumption 1) — is surfaced as residual Q1 for ARGUS because it is a genuine refinement of the proven pattern, not a re-scope of the cut.

---

## §2 — Approach (the slim structure)

### 2.1 The slim core shape

Post-cut, `operating-disciplines.md` is the **slim universal operational core**: crisp rule per discipline + a one-line cite-back (stub + `Read` pointer for CONDITIONAL; `Anchor:` for PROVENANCE; pointer for DUPLICATE) + ONE always-loaded **relocation index** table (the losslessness-recovery artifact). The CONDITIONAL procedures move to disk modules; the provenance/empirical multi-paragraph blocks move to bw cites; the one DUPLICATE consolidates to a pointer. The always-on rules (the anti-pattern thesis, escalation triggers, heartbeat contract, confabulation discipline, PRINCIPAL-gate rule, credential structural rule, the composition + trigger-payload thin rules) stay inline, tightened.

### 2.2 The always-loaded RELOCATION INDEX (no routing map — op-disc is not an orchestrator)

Per modules/README.md §4, the composition layer pairs a routing map (dispatch-time) with a relocation index (audit-time). **op-disc gets ONLY the relocation index** (assumption 1). The index is added as a new **§0.5 "Relocation index (audit-time — where relocated content went)"** placed immediately after the thesis, BEFORE §1, so the always-loaded recovery table sits at the top of the operational core. It uses the regular index column shape from modules/README.md §4.2 (relocated-content → new-home → class) so a future enforcement-layer hook is parseable. The index is populated in §3 of THIS design.

**Why no routing map:** the routing map answers "at dispatch time, what module does this task need?" — an orchestrator question. op-disc dispatches nothing. The dispatch-time signal a reader needs ("you are entering autonomous mode → read `autonomous-mode-setup.md`") lives INLINE at the §N stub, at the point of need, because the reader arriving at op-disc §11 is the seat that just hit the autonomous-mode trigger. Putting a routing map in op-disc would duplicate the per-stub pointers into a table no orchestrator consults. The stubs ARE the routing, distributed to point-of-need. (This is the refinement ARGUS should pressure-test — residual Q1.)

### 2.3 The CONDITIONAL module files (CREATED + POPULATED this arc)

Each module is a self-contained reference body; the module's first line is a stable `# <Title>` heading (the recompose keys on it; P-RECOMPOSE asserts it appears) followed by a provenance header citing this design + the stoa--xyb epic (mirroring modules/README.md:14-16). **No module carries an author-like field** (P-AUTH). Line ranges are grounded against the LIVE source (re-read this design phase).

| Module file | Source § (live line range) | What moves in |
|---|---|---|
| `substrate/modules/two-polybius-coordination.md` | §7 (115–252) | §7 intro + §7.1 radio-check + §7.2 adaptive cadence + §7.3 unified poll + §7.4 cross-tier routing + §7.5 write boundaries + §7.7 bw-timeline parsing. (§7.6 empirical lineage → PROVENANCE Anchor, NOT into module — see §3.4.) |
| `substrate/modules/autonomous-mode-setup.md` | §11 (478–726) | The full 7-step setup checklist incl. step 1.5 renewal-cron machinery (the renewal-cron prompt-body template, the 4-step terminating-shape dance, the failure-mode acceptance), steps 2–9. This is the single largest relocation (~249 lines). |
| `substrate/modules/sub-agent-transcript-discipline.md` | §14 (820–833) | §14 full body (kill-time JSONL capture, save target, read-side discipline, open-question). |
| `substrate/modules/verification-complexity.md` | §15 (836–919) | §15 intro + §15.1 2x2 + §15.2 rule + §15.3 four strategies + §15.4 two verdict shapes + §15.5 time/cost box + §15.6 six worked examples + §15.7 self-referential. |
| `substrate/modules/bw-fit-matrix.md` | §16 (920–961) | §16 intro + §16.1 matrix + §16.2 layered architecture + §16.3 decision rule. (§16's empirical anchor → Anchor.) |
| `substrate/modules/oss-dep-and-latency.md` | §17 (962–1001) | §17 intro + §17.1 fork-over-upstream + §17.2 agent-time latency budget. (§17's empirical anchor → Anchor.) |
| `substrate/modules/credential-discipline-detail.md` | §20 (1238–1338) **minus the structural rule + 5-anti-pattern list that stay inline** (see §2.5) | §20.1 canonical pattern diagram + numbered detail, §20.5 Railway-specific notes, §20.6 cross-reference. The §20 intro structural rule, §20.2 five-anti-pattern table, §20.3 refusal-as-signal, §20.4 universal rule STAY INLINE (always-on credential core). |
| `substrate/modules/bw-upgrade.md` | §22 (1363–1424) | §22 intro + §22.1 5-step + §22.2 3-axis + §22.4 check-bw-release skill + §22.5 cross-refs. (§22.3 N=1 provenance → Anchor.) |
| `substrate/modules/mechanical-inspection-split.md` | §27 (1627–1702) | §27 intro + §27.1 declaration + §27.2 3-step + §27.3 when-to-apply/A7 + §27.4 per-seat + §27.5 worked example. (§27.6 N=1 provenance → Anchor; §27.7 cross-refs SPLIT.) |
| `substrate/modules/multi-team-interop.md` | §29 (1825–1906) | §29 intro + §29.1–§29.5. (§29.6 N=1 provenance → Anchor; §29.7 cross-refs SPLIT.) |
| `substrate/modules/four-layer-identity.md` | §30 (1907–1972) | §30 intro + §30.1–§30.4. (§30.5 N=1 provenance → Anchor; §30.6 cross-refs SPLIT.) |
| `substrate/modules/substrate-component-design.md` | §31 (1973–2043) | §31 intro + §31.1 Principle 1 + §31.2 Principle 2. (§31.3 N=2 provenance → Anchor; §31.4 cross-refs SPLIT.) |
| `substrate/modules/jsdom-timing-discipline.md` | §32 (2044–2090) | §32 full body (the discipline + helper contract + empirical anchor + cross-refs — small enough to move whole). |

**13 CONDITIONAL module files created + populated this arc.**

### 2.4 KEEP-TIGHTEN sections (stay inline; prose tightened; no relocation)

The universal always-on operational core. These are read across turns by every seat (or are the keep-home for a DUPLICATE, or are themselves the thin composition/trigger rules):

- **§1–§6 (the anti-pattern thesis + redundancy core, 37–114).** Always-on framing every seat reads; the six anti-patterns ARE the doc's reason for existing. §6.7 carries provenance (the stoa--nax empirical) that compresses to an Anchor; the §6.7.1/§6.7.2 RULES stay (they are operational — the N=1-canon-promotion gate is cited from many sections).
- **§8.1 + §8.2 (positive references only + scaffolding, within 253–373).** Universal authoring discipline (every brief author, every turn that authors a downstream artifact). Rules stay; the §8.1/§8.2/§8.3/§8.5 empirical anchors compress to Anchors. **§8.3 (activation-paste session-state) + §8.4 (install.sh deploy-plan smoke beat) + §8.5 (fallback-chain probe coverage) are CONDITIONAL-leaning** — see §2.6 ambiguity flag; rev1 KEEPS them inline tightened (they are short and operationally cross-cited) and flags the call for ARGUS.
- **§9 (bw storage model, 374–413).** Universal (every bw-using seat). The worktreeconfig fix is operational; the historical regression-window prose (400) + the stoa--7kg lineage (404) compress to an Anchor.
- **§10 (HITL/Autonomous engagement, 414–477).** KEEP-TIGHTEN WHOLE — carries the universal escalation triggers (443) read every autonomous engagement (Arc-2 precedent: the analogous POLYBIUS §13 was KEEP-TIGHTEN, ARGUS CONCUR). The §10 progression-canon provenance paragraph (470) compresses to an Anchor; the rules + trigger-words tables + transition-triggers table stay.
- **§12 (bw cookbook, 727–803).** KEEP — this section is the DUPLICATE keep-HOME itself (every other bw-using file points here; it self-declares "do not duplicate" at 729). It stays inline, whole. (Tighten only obviously verbose prose; do NOT relocate — relocating the keep-home would break every pointer at it.)
- **§13 (Windows Python, 804–819).** KEEP (universal, 16 lines, already tight). Compress the §13 empirical (814) to an Anchor.
- **§18 (subagent status + heartbeat, 1002–1080).** Rules KEEP (the heartbeat contract §18.1 + read-before-write §18.2 + the Monitor/run_in_background prohibitions §18.4 are universal CAPTAIN core, cited from every CAPTAIN role file + TIRO §206). §18.5 dispatch-sequence table stays (operational). §18.7 empirical lineage → Anchor; §18.6 SPLIT (live tool-availability rules stay; the SendMessage empirical-lineage paragraph → Anchor).
- **§19 (confabulation, 1081–1237).** Rules KEEP (§19.1 two halves + §19.2 three patterns + §19.3 contrast + §19.4 relationship — universal always-on, cited from MAJOR_POLYBIUS §223 / TIRO §28,§92). The HEAVY provenance compresses: §19.5 lineage → Anchor; §19.6 attestation-confabulation RULE stays (it is operational + cross-cited §19.6) but §19.6.1 empirical / §19.6.4 N=1 provenance → Anchor; §19.7 idle-retro RULE stays but §19.7.1 empirical / §19.7.5 N=1 provenance → Anchor; §19.6.3 + §19.7.6 cross-refs SPLIT.
- **§20 structural core (intro rule + §20.2 + §20.3 + §20.4, within 1238–1338).** KEEP inline — credential discipline is always-on (the "agents NEVER hold credentials" rule + the 5 rejected anti-patterns a seat must recognize + refusal-as-signal + the universal split). Only the §20.1 worked diagram-detail + §20.5 Railway-specific + §20.6 skill-cross-ref relocate (CONDITIONAL detail). §20.7 lineage → Anchor.
- **§21 (Ariadne-search authoring, 1339–1362).** KEEP-TIGHTEN (universal authoring discipline, 24 lines). §21 empirical (1359) → Anchor.
- **§23 rules (1425–1483).** KEEP (base-vs-custom is cited from install.sh + check.sh + apply.sh at ~10 sites + §216). §23.1 source-of-truth declaration + §23.2 path convention + §23.3 by-seat discipline stay. §23.4 N=1 provenance → Anchor; §23.5 cross-refs SPLIT.
- **§24 (arc-build branch hygiene, 1484–1505).** KEEP — already a thin cross-ref to MAJOR_PLINY §5.9 (22 lines). Compress the §24 empirical-anchor bullet (1502) into the existing cross-ref block.
- **§25 rules (1506–1607).** KEEP (PRINCIPAL-gate is always-on, cited from templates + skills + DAEDALUS/ADA/VERA envelopes). §25.1 declaration + §25.2 two-axis + §25.3 BLOCK-not-TAG + §25.4 per-seat table stay. **§25.5 probe-design sub-case (the `--no-local` throwaway-clone detail) is CONDITIONAL** (only DAEDALUS-at-probe-design + VERA need it) — relocate to a module? See §2.6 ambiguity flag; rev1 KEEPS §25.5 inline (it is the catch-point canon DAEDALUS reads at design time, and DAEDALUS reads op-disc not a module) and compresses only the CVE prose verbosity. §25.6 N=1 provenance → Anchor; §25.7 cross-refs SPLIT.
- **§26 (cron hygiene, 1608–1626).** KEEP — already thin cross-ref to MAJOR_POLYBIUS §5.1.3 (19 lines). Compress the empirical-anchor bullet.
- **§28 rules (1703–1824).** KEEP (Co-Authored-By trailer is cited from global CLAUDE.md + MAJOR_PLINY §5.12 + CAPTAIN_ADA §5.5; the trailer FORMAT §28.1 + scope §28.2 + squash-merge §28.3 + §28.3.1 pitfall + §28.4 frontmatter-boundary + §28.5 read-discipline are all operational). §28.6 future-extension stays (short). §28.7 N=1 provenance → Anchor; §28.8 cross-refs SPLIT.
- **§33 (composition layer, 2091–2116).** KEEP — this IS the thin always-loaded rule the modules/README.md is the detail for. Stays whole.
- **§34 (trigger-payload, 2117–2156).** KEEP — the thin always-loaded rule (just shipped Arc 46). Stays whole.

### 2.5 PROVENANCE relocations (C-1 / C-2 / SPLIT disposition per §3.3 / §3.4 / §3.6)

The "N=1 provenance + accretion path" + "Cross-references" subsections at the tail of disciplines relocate to bw cites. The slim core keeps the RULE + a one-line `Anchor: <bw-id>` cite-back. C-1 (already-in-bw) vs C-2 (not-in-bw) per-row in §3.3 / §3.4; the SPLIT cross-ref subsections get per-line LIVE-vs-PROVENANCE enumeration in §3.6.

### 2.6 Ambient-vs-conditional CALLS I am UNSURE OF — flagged for ARGUS (per the brief's "flag, don't guess" instruction)

These three are genuine ambient-vs-conditional judgment calls. rev1 makes a defensible KEEP/RELOCATE call for each AND flags it so ARGUS adjudicates rather than rubber-stamps:

- **A1 — §7 (two-POLYBIUS coordination): RELOCATE to module, BUT it is the most heavily-cross-cited candidate.** §7.1/§7.2/§7.4/§7.5/§7.7 are cited from `polling-cron-prompt-template.md`, `paste-instruction-template.md`, `autonomous-mode-activation-template.md`, `stop-self-check.sh`, `_hooklib.sh`, MAJOR_PLINY, MAJOR_POLYBIUS, TIRO, onboarding.md. The ambient-vs-conditional test: does EVERY seat need §7 EVERY turn? **No** — §7 fires only when two POLYBIUS seats coordinate async (an autonomous-mode-coordination engagement). CAPTAINs never coordinate two-POLYBIUS. So §7 is genuinely CONDITIONAL. **BUT** the cross-cite density means the STUB must preserve every cited subsection number (§7.1–§7.7) as resolvable anchors, AND the templates/hooks that cite §7.x must still resolve. rev1's call: RELOCATE the §7 BODY to `two-polybius-coordination.md`, leave a §7 stub that lists the subsection numbers (§7.1–§7.7) in the stub prose so `operating-disciplines.md §7.2` etc. still resolve to a real anchor (the stub names them). Flagged because the cross-cite density is the highest of any relocation and a templates/hooks reader following `§7.2` lands on a stub pointer, not the content — ARGUS should confirm that is acceptable (it is the same trade POLYBIUS §5/§10/§11 made, but §7's citers include runtime hook scripts).
- **A2 — §8.3 / §8.4 / §8.5: KEEP inline (rev1) vs relocate-with-§8.** §8.1 + §8.2 are unambiguously KEEP (universal authoring). §8.3 (activation-paste session-state), §8.4 (install.sh deploy-plan smoke beat), §8.5 (fallback-chain probe coverage) are arguably CONDITIONAL (§8.3 only when authoring an activation paste; §8.4 only when an arc adds a deploy-governed file; §8.5 only when authoring a fallback-chain probe set). rev1 KEEPS them inline tightened because (a) they are short, (b) §8.4 is cited operationally and §8.5 is a gauntlet-wide ADA/VERA/CATO discipline, and (c) splitting §8 into "rules stay / sub-procedures go" fragments a coherent section below the line-savings-justifies-a-module threshold. Flagged: ARGUS may prefer a `downstream-authoring-detail.md` module taking §8.3+§8.4+§8.5.
- **A3 — §25.5 (probe-design throwaway-clone sub-case): KEEP inline (rev1) vs relocate.** §25.5 is CONDITIONAL by audience (DAEDALUS-at-probe-design + VERA), but it is the explicit catch-point canon DAEDALUS reads at DESIGN time — and DAEDALUS reads op-disc, not a module dispatched to it. Relocating it to a module would require DAEDALUS to know to Read the module at design time (no orchestrator dispatches DAEDALUS the module — DAEDALUS is dispatched by PLINY with a brief, not with op-disc modules). rev1 KEEPS §25.5 inline (compressing only the CVE-2024-32020 prose) because the catch-point property depends on DAEDALUS encountering it while reading op-disc §25. Flagged: this is the clearest case where "CONDITIONAL by audience" does NOT imply "relocate to module," because the audience reads the file directly rather than via dispatch — ARGUS should confirm the reasoning generalizes (it is the same reason §15 verification-complexity is a closer call than it looks — see A4).
- **A4 (sub-flag) — §15 (verification-complexity): RELOCATE to module (rev1), but the verifier CAPTAINs read it the way DAEDALUS reads §25.5.** §15 is verifier-CAPTAIN-only (VERA/CATO/ARGUS/ZENO), cited from `save-verdict/SKILL.md` + `_save_verdict.py`. The verifier CAPTAINs are dispatched by PLINY; PLINY can name `verification-complexity.md` in the dispatch brief (the routing-map-at-dispatch shape — but op-disc has no routing map; PLINY's routing map would carry it). rev1 RELOCATES §15 (it is large, 84 lines, and genuinely conditional) and notes that the dispatch-time pointer is PLINY's responsibility (PLINY's routing map gains a `dispatch verifier → verification-complexity.md` row in a FUTURE PLINY cut; until then PLINY names it inline per the §15 stub's `Read` pointer). Flagged as the boundary case that distinguishes A3 (KEEP, read-direct-at-design-time) from A4 (RELOCATE, dispatched-with-brief).

---

## §2.7 — §-numbering coherence + the recompose marker + the MODULE-OWNERSHIP partition (the load-bearing install.sh fix)

### 2.7.1 Section-number PRESERVE via stubs (Arc-2 precedent, zero cross-ref churn)

The slim core PRESERVES section numbers. Each CONDITIONAL whole-section relocation leaves a stub at its original number (heading + `Read` pointer + paired recompose marker). §7 stays §7, §11 stays §11, §15 stays §15, §16/§17/§20-detail/§22/§27/§29/§30/§31/§32 stay at their numbers. Every existing cross-ref (`operating-disciplines.md §N` from role files, modules, templates, hooks, skills, install.sh) still resolves to a real anchor. The cross-ref graph confirms this is strongly net-positive (§3.1).

**Exact stub shape (CONDITIONAL relocations) — the literal ADA writes** (mirrors Arc-2 §2.7 verbatim modulo the module name):
```
## 11. Autonomous-mode-setup checklist
Relocated to `.claude/modules/autonomous-mode-setup.md` (CONDITIONAL — read when a seat detects an autonomous-mode trigger that applies to itself).
Recover the full 7-step procedure via `Read .claude/modules/autonomous-mode-setup.md`. Relocation-index row in §0.5.
<!-- MODULE-INLINE:autonomous-mode-setup -->
<!-- /MODULE-INLINE:autonomous-mode-setup -->
```
The paired sentinel `<!-- MODULE-INLINE:<module-name> -->` … `<!-- /MODULE-INLINE:<module-name> -->` is the recompose hook (machine-parseable, inert HTML comment at user/project tier, idempotency anchor at subproject tier). `<module-name>` is the module basename without `.md`. Same justification as Arc-2 §2.7 (machine-parseable not prose; invisible at non-recompose tiers; 1:1 audit). The PROVENANCE `Anchor:` cites and the §-stubs for sections whose RULE stays inline carry NO recompose marker — only the 13 whole-section CONDITIONAL relocations re-inline at subproject tier.

**Sub-section preserve for §7 (A1).** §7's body relocates whole, but §7.1–§7.7 are individually cross-cited. The §7 stub must keep those subsection numbers resolvable. The stub prose names them explicitly:
```
## 7. Coordinating two POLYBIUS seats async via bw polling
Relocated to `.claude/modules/two-polybius-coordination.md` (CONDITIONAL — read when two POLYBIUS seats coordinate async via bw polling). Covers §7.1 radio-check, §7.2 adaptive cadence, §7.3 unified poll, §7.4 cross-tier routing, §7.5 write boundaries, §7.7 bw-timeline parsing. Recover via `Read .claude/modules/two-polybius-coordination.md`.
<!-- MODULE-INLINE:two-polybius-coordination -->
<!-- /MODULE-INLINE:two-polybius-coordination -->
```
A reader following `operating-disciplines.md §7.2` lands on the §7 stub, which names §7.2 and points at the module. At subproject tier the recompose re-inlines the full §7.x bodies so the subsection anchors are live verbatim. (This is the A1 trade-off ARGUS adjudicates.)

### 2.7.2 The MODULE-OWNERSHIP partition (THE load-bearing install.sh extension — §6 specifies it)

**The problem (live-confirmed):** `recompose_module_inline()` (install.sh L871-957) builds `_module_basenames` from the GLOBAL `${SRC_MODULES_DIR}/*.md` glob (minus README, L878-883) and Check B (awk END, L945) asserts EVERY such module was consumed by a marker IN THE ROLE FILE being recomposed. Today all 5 modules are POLYBIUS-owned and all 5 are marked in MAJOR_POLYBIUS.md, so `recompose_module_inline "$DEST_POLYBIUS"` passes. **Once this arc adds 13 op-disc modules to the shared dir, `recompose_module_inline "$DEST_POLYBIUS"` Check B sees 18 modules, finds 13 with no POLYBIUS marker → `err` → aborts the subproject deploy.** This is a hard regression the cut introduces if not fixed.

**The fix:** scope each recompose call to a per-call OWNED-module-set. `recompose_module_inline()` takes a SECOND argument: the space-separated list of module basenames THIS role file owns. Check B/D evaluate against the owned set, not the global glob. Check A still validates against the global module sources (a marker must reference a real module file regardless of owner). §6.4 gives the exact signature + the owned-set lists. This keeps the flat-glob deploy + Read-path convention (no owner-subdirs, no collision with the Arc-29 `modules/custom/` reservation) — the partition lives in the recompose call sites, not the filesystem.

---

## §3 — The relocation ledger (the losslessness proof artifact)

This ledger is the artifact ARGUS audits for LOST CANON, whole-team. **One row per relocated chunk.** Every empirical anchor + every section in the 2156-line source either appears as a ledger row with a lossless home OR is a KEEP-TIGHTEN section that stays inline (§3.7 lists those for audit completeness). Line ranges are grounded against the LIVE `substrate/operating-disciplines.md` (re-read this design phase).

### 3.1 Cross-ref-preservation check (which op-disc §N are cited elsewhere — confirmed for stub-preserve)

Grepped live across `substrate/` (active files only — role files, install.sh, hooks, templates, skills, modules; arc directives + pastes are frozen history, not stub-resolution consumers). Distinct op-disc §N cited from ACTIVE files:

| §N cited | Citing active files (sample) | Disposition under this cut |
|---|---|---|
| §6, §6.7.1 | arc dirs (frozen); §6.7.1 cited internally + by §-promotion gate in many sections | KEEP-TIGHTEN (stub n/a — rule stays inline) |
| §7, §7.1, §7.2, §7.4, §7.5, §7.7 | polling-cron-prompt-template, paste-instruction-template, autonomous-mode-activation-template, stop-self-check.sh, _hooklib.sh (§13→ wait, that's §13), TIRO §176 (§7.7) | **§7 RELOCATE → stub preserves §7 + names §7.1–§7.7** (A1) |
| §8, §9 | onboarding.md (§7.2 — wait that's §7); templates (§8, §9) | KEEP-TIGHTEN (rules stay; stub n/a) |
| §10, §10.1 | arc dirs (frozen) | KEEP-TIGHTEN WHOLE |
| §11 | autonomous-mode-activation-template §40, polling-cron-prompt-template §107/135/144/170/237/259, arc dirs | **§11 RELOCATE → stub preserves §11** |
| §12, §12.1, §12.2, §12.4 | MAJOR_PLINY §618, TIRO (~15 cites), pretooluse-no-dash-m-bw-comment.sh §8, validate-spec spec_refs.py §42 | KEEP (§12 is the DUPLICATE keep-home; stays whole) |
| §13 | check-bw-release/check.sh §94, _hooklib.sh §28 | KEEP-TIGHTEN |
| §15.4 | save-verdict/SKILL.md §126-128, _save_verdict.py §221/232/239 | **§15 RELOCATE → stub preserves §15 + names §15.4** |
| §18, §18.5 | TIRO §206, polling-cron-prompt-template §215 | KEEP (rules stay inline; stub n/a) |
| §19, §19.6, §19.7 | MAJOR_POLYBIUS §223, TIRO §28/§92, MAJOR_PLINY (internal), CAPTAIN_TIRO | KEEP (rules stay inline; stub n/a) |
| §20, §20.3 | BARTLEBY §130, arc dirs | KEEP structural rule inline (stub n/a); detail relocates |
| §22, §22.2 | check-bw-release/check.sh §89/161, SKILL.md §3/§54 | **§22 RELOCATE → stub preserves §22 + names §22.2** |
| §23 | install.sh ×6 (§216/1290/1358/1387/1447/1528), inspect-script-output/check.sh §177/237, check-substrate-updates apply.sh+check.sh ×7 | KEEP (rules stay inline; stub n/a) |
| §24 | pretooluse-clean-tree-before-branch.sh §6 | KEEP (thin cross-ref stays) |
| §25 | autonomous-mode-activation-template §81, inspect-script-output/SKILL.md §3, polling-cron-prompt-template §197 | KEEP rule inline (stub n/a); §25.5 KEEP (A3) |
| §27, §27.2 | inspect-script-output/check.sh §9/§176/§373, SKILL.md §3 | **§27 RELOCATE → stub preserves §27 + names §27.2** |
| §30 | handoff-author/SKILL.md §4 | **§30 RELOCATE → stub preserves §30** |
| §31 | arc dirs (frozen) | **§31 RELOCATE → stub preserves §31** |
| §32 | ADA §185, (VERA/CATO via §32's own cross-refs) | **§32 RELOCATE → stub preserves §32** |

**Check result:** every op-disc §N cited from an active substrate file resolves post-cut — KEEP sections keep their numbers (rule stays inline), RELOCATE sections leave a numbered stub naming the cited subsections. The highest-risk citers are RUNTIME scripts (`stop-self-check.sh`, `_hooklib.sh`, `pretooluse-*.sh`, `_save_verdict.py`) — these cite §N in COMMENTS (human-orientation, not runtime path resolution); confirmed they do not `Read` the §N at runtime (they reference it as provenance). So no stub-vs-content mismatch breaks a runtime script. (P-XREF asserts this.)

### 3.2 CONDITIONAL relocations (→ disk module; slim-core residue = stub + `Read` pointer + recompose marker + relocation-index row)

| Source (§ + live lines) | Class | New home | Slim-core residue |
|---|---|---|---|
| §7 (115–252) | CONDITIONAL | `modules/two-polybius-coordination.md` | §7 stub (names §7.1–§7.7) + `<!-- MODULE-INLINE:two-polybius-coordination -->` + index row |
| §11 (478–726) | CONDITIONAL | `modules/autonomous-mode-setup.md` | §11 stub + `<!-- MODULE-INLINE:autonomous-mode-setup -->` + index row |
| §14 (820–833) | CONDITIONAL | `modules/sub-agent-transcript-discipline.md` | §14 stub + `<!-- MODULE-INLINE:sub-agent-transcript-discipline -->` + index row |
| §15 (836–919) | CONDITIONAL | `modules/verification-complexity.md` | §15 stub (names §15.4) + `<!-- MODULE-INLINE:verification-complexity -->` + index row |
| §16 (920–961) | CONDITIONAL | `modules/bw-fit-matrix.md` | §16 stub + `<!-- MODULE-INLINE:bw-fit-matrix -->` + index row |
| §17 (962–1001) | CONDITIONAL | `modules/oss-dep-and-latency.md` | §17 stub + `<!-- MODULE-INLINE:oss-dep-and-latency -->` + index row |
| §20 detail (§20.1+§20.5+§20.6 within 1238–1338) | CONDITIONAL | `modules/credential-discipline-detail.md` | §20 keeps intro rule + §20.2 + §20.3 + §20.4 INLINE; a `<!-- MODULE-INLINE:credential-discipline-detail -->` marker placed after §20.4 for the relocated detail + index row |
| §22 (1363–1424) | CONDITIONAL | `modules/bw-upgrade.md` | §22 stub (names §22.2) + `<!-- MODULE-INLINE:bw-upgrade -->` + index row |
| §27 (1627–1702) | CONDITIONAL | `modules/mechanical-inspection-split.md` | §27 stub (names §27.2) + `<!-- MODULE-INLINE:mechanical-inspection-split -->` + index row |
| §29 (1825–1906) | CONDITIONAL | `modules/multi-team-interop.md` | §29 stub + `<!-- MODULE-INLINE:multi-team-interop -->` + index row |
| §30 (1907–1972) | CONDITIONAL | `modules/four-layer-identity.md` | §30 stub + `<!-- MODULE-INLINE:four-layer-identity -->` + index row |
| §31 (1973–2043) | CONDITIONAL | `modules/substrate-component-design.md` | §31 stub + `<!-- MODULE-INLINE:substrate-component-design -->` + index row |
| §32 (2044–2090) | CONDITIONAL | `modules/jsdom-timing-discipline.md` | §32 stub + `<!-- MODULE-INLINE:jsdom-timing-discipline -->` + index row |

**13 CONDITIONAL chunks → 13 new module files.**

**§20 special case (partial-section relocation):** §20 is the ONLY partial-section relocation (the structural rule stays, the detail moves). The marker pair is placed AFTER §20.4 (the last inline subsection), enclosing nothing in the slim core; at subproject tier `credential-discipline-detail.md` re-inlines there. The §20 heading itself stays at §20 with the rule; §20.5/§20.6 numbers move INTO the module. The slim core's §20 carries an inline `Read .claude/modules/credential-discipline-detail.md` pointer for the diagram + Railway notes. (Flagged minor: this is the one relocation where the marker is not the whole-section stub shape — ADA places it post-§20.4, not as a §-heading stub. P-RECOMPOSE still covers it.)

### 3.3 PROVENANCE relocations — C-1 (already-in-bw; content-check then delete-to-Anchor)

All ticket ids below RESOLVE live (verified this design phase, 24/24). The slim core keeps the RULE + a one-line `Anchor: <bw-id>`. **The C-1 content-check gate (modules/README.md §5.2, carried into the build):** before ADA deletes ANY C-1 inline provenance prose, ADA runs `bw show <cited-id>` and content-checks the ticket carries the story. Per-deletion gate. VERA re-executes a sample (P-C1).

| Source (§ + live lines) | bw id(s) | Slim-core residue |
|---|---|---|
| §6.7 empirical (93) + §6.7.2 anchor (111) | `stoa--nax` | KEEP §6.7.1/§6.7.2 rules; `Anchor: stoa--nax` |
| §8.1 empirical (272) | 2026-05-04 in-prose | → §3.4 C-2 (no clean ticket) |
| §8.2 empirical (298) | 2026-05-05 in-prose | → §3.4 C-2 (no clean ticket) |
| §8.3 empirical (324) | `stoa--uc7` | KEEP §8.3 rule; `Anchor: stoa--uc7` |
| §8.4 empirical (348) | `stoa--14u` | KEEP §8.4 rule; `Anchor: stoa--14u` |
| §8.5 empirical (370) | `stoa--148` | KEEP §8.5 rule; `Anchor: stoa--148` |
| §9 historical window (400) + lineage (404) | `stoa--7kg`, `stoa--7kg.1` | KEEP §9 rules; `Anchor: stoa--7kg, stoa--7kg.1` |
| §10 progression provenance (470) | `stoa--ntn` | KEEP §10 rules; `Anchor: stoa--ntn` — **NOTE:** stoa--ntn NOT in the 24 verified; ADA must `bw show stoa--ntn` content-check; if it does not resolve/carry → C-2 child ticket (flagged) |
| §12 empirical (800) | `stoa--v2o` | KEEP §12 whole; `Anchor: stoa--v2o` |
| §13 empirical (814) | `stoa--a5q`, `ariadne--sh7` | KEEP §13 rule; `Anchor: stoa--a5q` (ariadne--sh7 cross-repo, fold into recovery note) |
| §15 (relocates whole → module; empirical 838 stays in module) | `stoa--tp1` | Moves WITH §15 into module; `Anchor: stoa--tp1` in the module |
| §16 empirical (958) | `stoa--vmc` | Moves WITH §16 into module; `Anchor: stoa--vmc` in module |
| §17 empirical (998) | `stoa--rno` | Moves WITH §17 into module; `Anchor: stoa--rno` in module |
| §18.7 lineage (1077) | `stoa--odh`, `stoa--nvl`, `stoa--cm3` | KEEP §18 rules; `Anchor: stoa--odh, stoa--nvl (Arc 24 stoa--cm3)` |
| §18.6 SendMessage lineage (1073) | in §18.6 prose | SPLIT §3.6 (live tool-rules stay; lineage → Anchor) |
| §19.5 lineage (1125) | `stoa--ioy`, `stoa--cm3` | KEEP §19.1–§19.4 rules; `Anchor: stoa--ioy (Arc 24 stoa--cm3)` |
| §19.6.1 empirical (1141) + §19.6.4 N=1 (1166) | `stoa--ezj` (intent-probe) + Arc 30 in-prose | KEEP §19.6 rule; `Anchor: stoa--ezj` + Arc-30 anchor folds into recovery note |
| §19.7.1 empirical (1185) + §19.7.5 N=1 (1218) | `stoa--53u` | KEEP §19.7 rule; `Anchor: stoa--53u` |
| §20.7 lineage (1333) | `stoa--p5g` (+ railway--pam, railway--r9z cross-repo) | KEEP §20 rule; `Anchor: stoa--p5g` (railway--* fold into recovery note) |
| §21 empirical (1359) | `stoa--32b.3` | KEEP §21 rule; `Anchor: stoa--32b.3` |
| §22.3 N=1 (1397) | `stoa--s6n` | Moves WITH §22 into module; `Anchor: stoa--s6n` in module |
| §23.4 N=1 (1462) | `stoa--ads` | KEEP §23 rules; `Anchor: stoa--ads` |
| §24 empirical (1502) | `stoa--3cs` | KEEP §24 cross-ref; fold `stoa--3cs` into the existing §24 cross-ref block |
| §25.6 N=1 (1586) | `stoa--dxw`, `stoa--501` | KEEP §25 rules; `Anchor: stoa--dxw, stoa--501` |
| §26 empirical (1623) | in-prose (HUMAN_paste filenames) | KEEP §26 cross-ref; → §3.4 C-2 (no clean ticket) |
| §27.6 N=1 (1676) | `stoa--32b.2`, `stoa--dxw`, `stoa--s6n`, `stoa--ads` | Moves WITH §27 into module; `Anchor: stoa--32b.2` in module |
| §28.7 N=1 (1800) | `stoa--kjo` (+ ariadne--xft.4 cross-repo) | KEEP §28 rules; `Anchor: stoa--kjo` (xft.4 fold into recovery note) |
| §29.6 N=1 (1883) | `stoa--kt6` | Moves WITH §29 into module; `Anchor: stoa--kt6` in module |
| §30.5 N=1 (1949) | `stoa--wad` | Moves WITH §30 into module; `Anchor: stoa--wad` in module |
| §31.3 N=2 (2015) | `stoa--gq1` (+ HUMAN_relay cross-repo) | Moves WITH §31 into module; `Anchor: stoa--gq1` in module |

**Counting note:** PROVENANCE rows that "move WITH" a CONDITIONAL section (§15/§16/§17/§22/§27/§29/§30/§31) are NOT separate provenance chunks — they relocate inside their parent CONDITIONAL block as a compressed `Anchor:` line in the module. They are listed for completeness; the chunk count attributes them to the CONDITIONAL relocation. The standalone C-1 PROVENANCE chunks (compress-to-Anchor in the KEEP slim core) are: §6.7, §8.3, §8.4, §8.5, §9, §10, §12, §13, §18.7, §19.5, §19.6, §19.7, §20.7, §21, §23.4, §24, §25.6, §28.7 = **18 standalone C-1 chunks.**

### 3.4 C-2 archive-first cases — DEDICATED CHILD TICKETS (Arc-2 residual-2 precedent)

Provenance blocks with NO clean single bw home AND that become the only surviving copy once cut. Per the Arc-2 ARGUS adjudication: archive each to a DEDICATED CHILD TICKET (`bw create … --parent stoa--xyb.8 -d "<verbose prose>"`), NOT a bare `bw comment` (a titled child id is discoverable from the relocation-index Anchor; a buried comment is not). Mechanism confirmed live in Arc-2 (`bw create` supports `--parent` + `-d`).

| Source (§ + live lines) | What archives | Slim-core residue |
|---|---|---|
| §8.1 empirical (272) — 2026-05-04 bw-prime "NOT user-beadwork" leak | The verbose 2026-05-04 incident prose | C-2 child ticket; KEEP §8.1 rule + table; `Anchor: stoa--xyb.8.N` |
| §8.2 empirical (298) — 2026-05-05 ariadne team_test over-delegation | The verbose 2026-05-05 incident prose | C-2 child ticket; KEEP §8.2 rules; `Anchor: stoa--xyb.8.M` |
| §26 empirical (1623) — multi-instance HUMAN_paste-pliny-arc-* convergence | The filename-list ad-hoc precedent prose | C-2 child ticket; KEEP §26 cross-ref; `Anchor: stoa--xyb.8.P` |
| §10 progression (470) — IF stoa--ntn fails content-check | the §10 progression provenance prose | CONDITIONAL on ADA's `bw show stoa--ntn` — C-2 ONLY if the ticket does not carry the story (flagged) |

**Per-deletion content-check gate (C-2 analogue):** ADA runs `bw create` FIRST, then `bw show <child-id>` to confirm the description carries the verbose prose, THEN deletes inline. Archive-FIRST, content-CHECK, THEN delete. (P-C2 asserts the child tickets exist + carry the prose + the Anchor cite matches the assigned id.)

**3 firm C-2 chunks** (§8.1, §8.2, §26) + 1 conditional (§10 if stoa--ntn fails).

### 3.5 DUPLICATE relocations (→ pointer)

| Source | Class | Keep-home | Slim-core residue |
|---|---|---|---|
| (none in op-disc) | — | — | — |

**op-disc has ZERO DUPLICATE relocations.** op-disc §12 is the DUPLICATE *keep-home* for the rest of the substrate (MAJOR_POLYBIUS §7.3 and MAJOR_PLINY §6.1 already point AT op-disc §12 — that consolidation happened in Arc 2 / earlier). The keep-home stays inline whole; nothing in op-disc duplicates content found elsewhere. (Confirmed: op-disc §12 self-declares "Role files reference this section; do not duplicate" at 729.) **0 DUPLICATE chunks.**

### 3.6 SPLIT per-line enumeration (cross-ref subsections — deterministic, no ADA guessing)

The "Cross-references" subsections at the tail of KEEP sections mix LIVE in-file/sibling-file/skill/tool pointers (stay inline) with PROVENANCE bw-id/empirical lines (fold into the section's `Anchor:`). The rule (Arc-2 §3.8): **keep every line that points at a §/file/skill/tool a reader follows to OPERATIONAL content; fold every line that says "exists because <ticket/date>" or "source-of-truth is <ticket/doc>" into the section's Anchor.** Sections whose body relocates whole (§22/§27/§29/§30/§31) carry their cross-refs INTO the module — no SPLIT needed there (the cross-refs move with the body). SPLIT applies only to the cross-ref tails of KEEP sections.

The KEEP sections with cross-ref tails to SPLIT: **§19.6.3 (1154–1162), §19.7.6 (1227–1234), §23.5 (1472–1480), §25.7 (1597–1604), §28.8 (1811–1821).** For each, the deterministic call:

- **§19.6.3 (1156–1162):** §19.1/§19.2 (in-file LIVE — keep); MAJOR_PLINY §7.2 + MAJOR_POLYBIUS §4.3 (sibling LIVE — keep); MAJOR_PLINY §5.10 (sibling LIVE — keep); §6.7.1 (in-file LIVE — keep); §19.7 (in-file LIVE — keep); the "Empirical anchor: Arc 30 PLINY init-handshake…" line (1162) (PROVENANCE — fold into §19.6 Anchor).
- **§19.7.6 (1229–1234):** §19.6 + §19.1-§19.5 (in-file LIVE — keep); MAJOR_PLINY §6.2 + MAJOR_POLYBIUS §16 (sibling LIVE — keep); §28 (in-file LIVE — keep); the "Empirical anchor: 2026-05-13 PLINY-stoa Engagement B (stoa--53u)" line (1234) (PROVENANCE — fold into §19.7 Anchor).
- **§23.5 (1474–1480):** MAJOR_POLYBIUS §17 (sibling LIVE — keep); §6.7.1/§8.1/§8.2 (in-file LIVE — keep); install.sh/check.sh/apply.sh (tooling LIVE — keep); MAJOR_POLYBIUS §19 (sibling LIVE — keep); the "stoa--ads (this arc); forthcoming railway_stoa custom team arc" line (1479) (PROVENANCE — fold into §23 Anchor).
- **§25.7 (1599–1604):** §10/§11 (in-file LIVE — keep); §6.7.1 (in-file LIVE — keep); §8.1 (in-file LIVE — keep); DAEDALUS §6.7/ADA §5.8/VERA §5.10 (sibling LIVE — keep); the two template hooks (LIVE — keep); the "stoa--dxw (Arc 26 anchor); stoa--501; retro §7" line (1604) (PROVENANCE — fold into §25 Anchor).
- **§28.8 (1813–1821):** global CLAUDE.md (LIVE — keep); MAJOR_PLINY §5.12 + CAPTAIN_ADA §5.5 (sibling LIVE — keep); §19.6/§25 (in-file LIVE — keep); MAJOR_POLYBIUS §18 (sibling LIVE — keep); MAJOR_PLINY §5.10/§5.11 (sibling LIVE — keep); the "stoa--kjo; 2026-05-04 ariadne--xft.4" lines (1820–1821) (PROVENANCE — fold into §28 Anchor).

**5 SPLIT cross-ref tails** (all on KEEP sections; LIVE pointers stay verbatim, the trailing empirical-anchor/ticket lines fold into the section's existing Anchor). P-SPLIT greps the LIVE pointer text (drift-resistant) + asserts the folded bw-ids appear in the §N Anchor, not orphaned as a standalone cross-ref bullet.

### 3.7 KEEP-TIGHTEN (stays inline; listed for audit completeness)

§1–§6 (anti-pattern thesis + redundancy + §6.7 rules), §8.1/§8.2 (+ §8.3/§8.4/§8.5 per A2), §9 rules, §10 WHOLE, §12 WHOLE (DUPLICATE keep-home), §13, §18 rules (§18.1–§18.5), §19.1–§19.4 + §19.6 rule + §19.7 rule, §20 structural core (intro + §20.2 + §20.3 + §20.4), §21, §23 rules (§23.1–§23.3), §24 (thin cross-ref), §25 rules (§25.1–§25.4 + §25.5 per A3), §26 (thin cross-ref), §28 rules (§28.1–§28.6), §33 WHOLE, §34 WHOLE. Plus the thesis preamble (1–33).

### 3.8 Module-OWNERSHIP record (for the install.sh partition — §6.4)

| Owner role file | Owned modules (basenames) |
|---|---|
| `MAJOR_POLYBIUS.md` (Arc 2) | `onboarding`, `sub-project-spawning`, `pair-programmer-authoring`, `pair-programming-prototyping`, `substrate-update-check` |
| `operating-disciplines.md` (THIS arc) | `two-polybius-coordination`, `autonomous-mode-setup`, `sub-agent-transcript-discipline`, `verification-complexity`, `bw-fit-matrix`, `oss-dep-and-latency`, `credential-discipline-detail`, `bw-upgrade`, `mechanical-inspection-split`, `multi-team-interop`, `four-layer-identity`, `substrate-component-design`, `jsdom-timing-discipline` |
| (`README.md` — owned by nobody; excluded from every owner-set) | — |

This is the data the partitioned `recompose_module_inline()` consumes (§6.4). It is also the canonical answer to "which modules belong to which role file" — recorded here so the future MAJOR_PLINY cut adds a third owner-set without re-deriving the partition.

### 3.9 Ledger summary (chunk counts per class — self-consistent)

- **CONDITIONAL:** 13 relocations (§7, §11, §14, §15, §16, §17, §20-detail, §22, §27, §29, §30, §31, §32) → **13 new module files. = 13 CONDITIONAL chunks.**
- **PROVENANCE:** **18 standalone C-1** (compress-to-Anchor in slim core: §6.7, §8.3, §8.4, §8.5, §9, §10, §12, §13, §18.7, §19.5, §19.6, §19.7, §20.7, §21, §23.4, §24, §25.6, §28.7) + **3 firm C-2** (§8.1, §8.2, §26 → child tickets) + **5 SPLIT** cross-ref tails (§19.6.3, §19.7.6, §23.5, §25.7, §28.8) = **26 PROVENANCE chunks.** (18 + 3 + 5 = 26.) Plus 8 "move-with-CONDITIONAL" provenance Anchors (§15/§16/§17/§22/§27/§29/§30/§31) counted under their parent CONDITIONAL relocation, not separately.
- **DUPLICATE:** **0 chunks** (op-disc §12 is the keep-home for the rest of the substrate; nothing in op-disc duplicates elsewhere).
- **KEEP-TIGHTEN:** ~20 sections stay inline (listed §3.7).

**Total relocated chunks: 13 CONDITIONAL + 26 PROVENANCE + 0 DUPLICATE = 39 relocated chunks**, each with a lossless home + recovery path.

### 3.10 Empirical post-cut floor ESTIMATE (reported, not targeted — per recalibrated criterion)

The big movers: 13 CONDITIONAL relocations move ~1,050 source lines off-disk (§7≈138 + §11≈249 + §14≈14 + §15≈84 + §16≈42 + §17≈40 + §20-detail≈55 + §22≈62 + §27≈76 + §29≈82 + §30≈66 + §31≈71 + §32≈47). The 18 C-1 + 3 C-2 provenance compressions turn ~250 verbose lines into ~25 Anchor lines (net ~225 saved). The KEEP-TIGHTEN prose-tightening saves a further ~50-100. Against 2156, the slim core lands an **estimated empirical floor in the ~700–850 line band** — every line of which is always-on universal core (the anti-pattern thesis, escalation triggers, the heartbeat/confabulation/credential/PRINCIPAL-gate/base-vs-custom/Co-Authored-By rules, the bw cookbook keep-home, the composition + trigger-payload thin rules, the relocation index). **This is an ESTIMATE; the build REPORTS the actual floor (P-FLOOR).** Do NOT cut a KEEP rule to push the floor lower — the floor is whatever the always-on core weighs (recalibrated criterion). A landing materially above ~900 means a KEEP section's prose is still verbose (tighten); a landing below ~600 is suspicious (check for a dropped always-on rule — P-FLOOR falsifier guard).

---

## §4 — Verification probes (what would falsify the design's intended behavior)

Concrete probes VERA re-executes. The probe spec is load-bearing. Run all from the worktree root.

### P-FLOOR — empirical floor reported + sanity band
```bash
wc -l substrate/operating-disciplines.md
```
**Pass:** the floor is REPORTED; sanity band ~700–850 (estimate). **Falsifies if:** > 1000 (cut too shallow — a CONDITIONAL section did not relocate, or KEEP prose untightened) or < 600 (suspiciously aggressive — check for a dropped always-on KEEP rule). A 850–1000 landing is partial-not-failure (KEEP rules are dense always-on core). Also run op-disc §33's per-module line-count discipline against each of the 13 new modules (no module is itself a re-bloat monolith — `autonomous-mode-setup.md` at ~249 lines is the largest and is acceptable: it is one coherent procedure).

### P-COND — every CONDITIONAL section has a real module home
```bash
for m in two-polybius-coordination autonomous-mode-setup sub-agent-transcript-discipline \
         verification-complexity bw-fit-matrix oss-dep-and-latency credential-discipline-detail \
         bw-upgrade mechanical-inspection-split multi-team-interop four-layer-identity \
         substrate-component-design jsdom-timing-discipline; do
  test -s "substrate/modules/$m.md" && echo "OK $m" || echo "MISSING $m"
done
```
**Pass:** all 13 module files exist and are non-empty. **Falsifies if:** any missing/empty (LOST CANON — a relocated section has no home).

### P-STUB — every relocated section leaves a stub at its original number (cross-ref preservation)
```bash
grep -nE '^## (7|11|14|15|16|17|20|22|27|29|30|31|32)\. ' substrate/operating-disciplines.md
```
**Pass:** §7, §11, §14, §15, §16, §17, §20, §22, §27, §29, §30, §31, §32 headings still present. **Falsifies if:** any relocated section number is GONE (would break every cross-ref pointing at it).

### P-XREF — every op-disc §N cited from an active substrate file resolves post-cut
```bash
# Collect cited §N from active files (role files, install.sh, hooks, templates, skills, modules):
grep -rhoE 'operating-disciplines\.md §[0-9]+(\.[0-9]+)*' substrate/ \
  --include='*.md' --include='*.sh' --include='*.py' \
  | grep -vE 'substrate/arcs/' | sort -u
# For each cited top-level §N, assert a heading (stub or live) exists:
for n in 6 7 8 9 10 11 12 13 15 16 18 19 20 22 23 24 25 27 30 31 32; do
  grep -qE "^## ${n}\. " substrate/operating-disciplines.md && echo "OK §$n" || echo "MISSING §$n"
done
```
**Pass:** every cited top-level §N resolves to a heading. The cited SUBSECTIONS (§7.2, §15.4, §22.2, §27.2) resolve either to a live subsection (KEEP) or are named in the parent stub prose (RELOCATE — grep the stub body for the subsection number). **Falsifies if:** any cited §N has no heading, OR a cited subsection of a relocated section is not named in its stub prose.

### P-C1 — C-1 content-check gate honored (LOST-CANON proof — sampled)
```bash
for id in stoa--nax stoa--7kg stoa--p5g stoa--ads stoa--dxw stoa--kjo stoa--53u stoa--ezj stoa--s6n stoa--32b.3; do
  echo "=== $id ==="; bw show "$id" 2>&1 | head -30; done
```
**Pass:** each cited ticket's body materially carries the N=1 story the deleted inline prose held. **Falsifies if:** any cited ticket is a thin stub not carrying the deleted detail → that deletion dropped canon, classification should have been C-2. **Special: assert stoa--ntn** (the §10 progression cite) resolves AND carries the progression story; if not, P-C1 fails and §10 routes to C-2 (the design flagged this).

### P-C2 — C-2 archive-first executed BEFORE deletion, in DEDICATED CHILD TICKETS
```bash
bw list --all 2>&1 | grep -E 'xyb\.8\.[0-9]'
bw show <child-id-for-§8.1> 2>&1 | grep -iE 'bw.prime|user-beadwork|2026-05-04|leak'
bw show <child-id-for-§8.2> 2>&1 | grep -iE 'team_test|over-delegation|2026-05-05'
bw show <child-id-for-§26> 2>&1 | grep -iE 'HUMAN_paste|cron.hygiene|preamble'
# And the slim-core cite-backs point at the child ids:
grep -nE 'stoa--xyb\.8\.[0-9]' substrate/operating-disciplines.md
```
**Pass:** the 3 firm C-2 child tickets exist (parent = stoa--xyb.8), each description carries its verbose provenance, and the slim core's Anchor cites the correct child id. **Falsifies if:** a C-2 verbose block is gone from source AND not present in a child-ticket description (LOST CANON), OR a cite-back id does not match the created ticket.

### P-SPLIT — SPLIT LIVE cross-refs preserved inline; PROVENANCE folded into Anchors
```bash
# LIVE pointers from §3.6 that MUST survive in the slim core (sample the load-bearing ones):
grep -nE 'MAJOR_PLINY\.md §7\.2|MAJOR_POLYBIUS\.md §4\.3|MAJOR_PLINY\.md §5\.10|DAEDALUS\.md §6\.7|CAPTAIN_ADA\.md §5\.5' substrate/operating-disciplines.md
# PROVENANCE bw-ids that MUST be folded into the §N Anchor (not orphaned as a cross-ref bullet):
grep -nE 'Anchor.*stoa--53u' substrate/operating-disciplines.md   # §19.7 fold
grep -nE 'Anchor.*stoa--dxw.*stoa--501' substrate/operating-disciplines.md   # §25 fold
grep -nE 'Anchor.*stoa--kjo' substrate/operating-disciplines.md   # §28 fold
```
**Pass:** every §3.6 LIVE pointer resolves in the slim core; the PROVENANCE bw-ids appear in the §N Anchor lines (folded). **Falsifies if:** any §3.6 LIVE pointer is missing (a LIVE operational pointer was wrongly relocated = dropped canon), OR a PROVENANCE bw-id is still sitting as a standalone cross-ref bullet.

### P-INDEX — the relocation index exists, is always-loaded core, and covers every relocation
```bash
grep -nE '^## 0\.5 |Relocation index' substrate/operating-disciplines.md   # the §0.5 index exists, before §1
# Assert the index has a row for every CONDITIONAL module + every C-2 Anchor:
for m in two-polybius-coordination autonomous-mode-setup verification-complexity credential-discipline-detail \
         bw-upgrade mechanical-inspection-split multi-team-interop four-layer-identity substrate-component-design jsdom-timing-discipline; do
  grep -q "$m" substrate/operating-disciplines.md && echo "OK index-or-stub: $m" || echo "MISSING: $m"
done
```
**Pass:** §0.5 relocation index present before §1; every CONDITIONAL module appears in an index row; NO routing map present (op-disc is not an orchestrator — assert NO `Routing map` heading: `grep -c 'Routing map' substrate/operating-disciplines.md` returns 0). **Falsifies if:** index absent, or a relocation has no index row (audit-recovery broken), OR a routing map was added (wrong shape — see assumption 1 / residual Q1).

### P-RECOMPOSE — subproject recompose completeness for op-disc (THE LOST-CANON-at-subproject probe, whole-team)
Run on a THROWAWAY subproject deploy (per op-disc §25.5: use a synthetic parent dir under a tmp path or `git clone --no-local`; do NOT mutate any operator-owned workspace):
```bash
TMP=$(mktemp -d); mkdir -p "$TMP/myproj"
bash substrate/install.sh --target subproject --parent-dir "$TMP" --subproject myproj
RECOMPOSED="$TMP/myproj/.claude/operating-disciplines.md"

# (a) The 13 op-disc PAIRED markers SURVIVE, each enclosing a NON-EMPTY body:
grep -cE '^<!-- MODULE-INLINE:' "$RECOMPOSED"     # expect 13 op-disc opens (NOT the POLYBIUS file's markers)
grep -cE '^<!-- /MODULE-INLINE:' "$RECOMPOSED"    # expect 13 op-disc closes
grep -Pzo '(?m)^<!-- MODULE-INLINE:[^\n]*-->\n<!-- /MODULE-INLINE:' "$RECOMPOSED" && echo "FAIL empty pair" || echo "OK no empty pairs"

# (b) EVERY op-disc module body is present (assert each module's first-heading line appears):
for m in two-polybius-coordination autonomous-mode-setup sub-agent-transcript-discipline \
         verification-complexity bw-fit-matrix oss-dep-and-latency credential-discipline-detail \
         bw-upgrade mechanical-inspection-split multi-team-interop four-layer-identity \
         substrate-component-design jsdom-timing-discipline; do
  head1=$(head -1 "substrate/modules/$m.md")
  grep -Fq "$head1" "$RECOMPOSED" && echo "OK body present: $m" || echo "MISSING body: $m"
done

# (c) recomposed subproject op-disc is canon-equivalent to full content (NOT the slim band):
wc -l "$RECOMPOSED"   # expect ~1700+ (the 13 bodies re-inlined), NOT the ~700-850 slim band

# (d) POLYBIUS recompose STILL passes (the partition fix did not break Arc-2):
RECOMPOSED_POLY="$TMP/myproj/.claude/MAJOR_POLYBIUS_myproj.md"
grep -cE '^<!-- MODULE-INLINE:' "$RECOMPOSED_POLY"   # expect 5 (the Arc-2 POLYBIUS markers, intact)
```
**Pass:** (a) all 13 op-disc paired markers survive + NO empty pair; (b) all 13 op-disc module first-heading lines appear; (c) recomposed op-disc in the FULL band (~1700+); (d) POLYBIUS recompose still inlines its 5 modules (the ownership partition did not regress Arc-2). **Falsifies if:** any op-disc marker pair is empty (body dropped → LOST CANON at subproject tier), OR < 13 op-disc markers survive, OR any op-disc body absent, OR recomposed op-disc still in the slim band (recompose silently no-op'd — the catastrophic failure), OR POLYBIUS recompose broke (partition regression).

### P-RECOMPOSE-NEG — FAIL-LOUD asserted (whole-team losslessness depends on the err() firing)
```bash
# Deliberately break: rename one op-disc module source, re-run subproject deploy.
mv substrate/modules/autonomous-mode-setup.md substrate/modules/autonomous-mode-setup.md.bak
bash substrate/install.sh --target subproject --parent-dir "$TMP" --subproject myproj2; echo "exit=$?"
mv substrate/modules/autonomous-mode-setup.md.bak substrate/modules/autonomous-mode-setup.md
```
**Pass:** install.sh exits NON-ZERO with a clear `recompose: marker MODULE-INLINE:autonomous-mode-setup has no module source` (Check A) error AND does NOT write a partial/slim op-disc to the subproject. **Falsifies if:** exit 0 (silent partial deploy — the LOST-CANON-at-subproject failure the FAIL-LOUD design exists to prevent).

### P-OWNERSHIP — the module-ownership partition is correct (Check B does NOT false-positive cross-owner)
```bash
# A clean subproject deploy must succeed even though substrate/modules/ holds BOTH owners' modules:
bash substrate/install.sh --target subproject --parent-dir "$TMP" --subproject myproj3; echo "exit=$?"
```
**Pass:** exit 0 — POLYBIUS recompose scoped to its 5-module owned-set passes (does not trip Check B on op-disc's 13 modules); op-disc recompose scoped to its 13-module owned-set passes (does not trip Check B on POLYBIUS's 5). **Falsifies if:** exit 2 with a Check-B `module X.md exists but no MODULE-INLINE:X marker` error — the partition was not applied and the global-glob false-positive fired (the exact regression §2.7.2 names).

### P-AUTH — no author-field regression (CLAUDE.md authorship discipline)
```bash
grep -niE '^(author|owner|creator|by|copyright|maintainer):' substrate/operating-disciplines.md substrate/modules/*.md
```
**Pass:** no author-like field names anyone other than Denson Smith (op-disc carries none; the 13 new modules carry none). **Falsifies if:** any new module's provenance header introduces an author field.

### P-KEEP — the always-on KEEP rules are still inline (whole-team availability-losslessness)
```bash
# Sample the load-bearing always-on rules that MUST NOT have relocated:
grep -qE 'redundancy IS the safety property' substrate/operating-disciplines.md && echo "OK §6 redundancy" || echo "DROPPED §6"
grep -qE 'Universal escalation triggers' substrate/operating-disciplines.md && echo "OK §10 escalation" || echo "DROPPED §10 triggers"
grep -qiE 'agents NEVER hold credentials|five rejected anti-patterns' substrate/operating-disciplines.md && echo "OK §20 credential core" || echo "DROPPED §20 core"
grep -qiE 'BLOCK, not a TAG' substrate/operating-disciplines.md && echo "OK §25 PRINCIPAL-gate" || echo "DROPPED §25 rule"
grep -qiE 'uncertain, checking' substrate/operating-disciplines.md && echo "OK §19 confabulation" || echo "DROPPED §19 rule"
grep -qE 'Co-Authored-By: CAPTAIN' substrate/operating-disciplines.md && echo "OK §28 trailer format" || echo "DROPPED §28"
grep -qiE 'bw cookbook|comment text is positional|-m. does NOT exist|`-m` does NOT exist' substrate/operating-disciplines.md && echo "OK §12 cookbook keep-home" || echo "DROPPED §12"
```
**Pass:** all always-on KEEP rules resolve inline. **Falsifies if:** any always-on rule was relocated off-disk (whole-team availability-losslessness violated — the worst failure for a universal file: a CAPTAIN that needs the credential rule or the escalation triggers cannot get them without a Read it does not know to make).

---

## §5 — Build steps (for ADA — ordered; the cut sequence)

**Step 0 (process hazard — DO THIS FIRST).** Confirm cwd is the worktree (`git -C C:/Users/denso/claude_projects/the-stoa/.claude/worktrees/arc-47-build rev-parse --show-toplevel` resolves to the worktree, branch `arc-47/build`). Use ABSOLUTE worktree paths for EVERY Write (`C:/Users/denso/claude_projects/the-stoa/.claude/worktrees/arc-47-build/...`). After each write, verify it landed in the worktree (`git -C <worktree> status` shows it modified/added there) and NOT in main (`git -C C:/Users/denso/claude_projects/the-stoa status` should NOT show your edit). The Write-resolves-against-main-root hazard hit prior arcs; this gate catches it before it compounds.

1. **Create the 13 module files** (`substrate/modules/*.md`), populating from the live source line-ranges in §2.3 / §3.2. Each module: stable `# <Title>` first line (P-RECOMPOSE keys on it) → provenance header (cites this design + stoa--xyb epic) → relocated content verbatim-tightened, INCLUDING the section's own cross-refs + the compressed `Anchor:` for any move-with provenance (§3.3). Run op-disc §33 per-module line-count discipline. NO author field (P-AUTH).
2. **Execute C-2 archive-first as DEDICATED CHILD TICKETS** (§3.4): `bw create "Arc 47 C-2 archive: §8.1 bw-prime leak provenance (2026-05-04)" --parent stoa--xyb.8 -d "<verbose prose>"` + the §8.2 + §26 equivalents, BEFORE touching the source. Record assigned child ids. `bw show <child-id>` content-check each. Write the slim-core Anchor cite-backs using the ACTUAL assigned ids. **Also `bw show stoa--ntn`** — if it carries the §10 progression story, §10 is C-1 (Anchor cite); if not, archive §10's progression prose as a 4th C-2 child ticket (the design flagged this conditional).
3. **Cut the slim core** (`substrate/operating-disciplines.md`):
   - Add **§0.5 relocation index** (the audit-time table, regular column shape) immediately after the thesis, BEFORE §1. Populate from §3.2 + §3.4. NO routing map (P-INDEX asserts this).
   - For each of the 13 CONDITIONAL sections, replace the body with the stub + paired `<!-- MODULE-INLINE:<name> -->` … `<!-- /MODULE-INLINE:<name> -->` marker (§2.7.1 literal). For §7, the stub names §7.1–§7.7 (A1). For §20, place the marker AFTER §20.4 (partial-section case, §3.2 note).
   - For each standalone C-1 PROVENANCE row (§3.3), run the `bw show` content-check (gate) THEN delete-to-Anchor.
   - For each SPLIT cross-ref tail (§3.6), keep LIVE pointers inline verbatim, fold the trailing empirical/ticket lines into the §N Anchor.
   - Tighten KEEP-TIGHTEN prose (§3.7) — do NOT relocate any KEEP rule (P-KEEP). §12 stays whole (DUPLICATE keep-home). §10/§33/§34 stay whole.
4. **Add the install.sh module-OWNERSHIP partition + op-disc recompose call** (§6 — substrate-tooling source, gauntlet-gated, correctly inside this arc):
   - Refactor `recompose_module_inline()` to take a SECOND arg (the owned-module-set); scope Check B/D to the owned set; Check A stays global (§6.4 exact signature).
   - Call `recompose_module_inline "$DEST_POLYBIUS" "$POLYBIUS_MODULES"` (the Arc-2 5-module set) AND `recompose_module_inline "$DEST_OPERATING_DISCIPLINES" "$OPDISC_MODULES"` (the 13-module set). The op-disc call goes AFTER op-disc is `cp`'d (current L978), inside the `if [ "$TARGET" = "subproject" ]` block (§6.5).
   - Smoke-test against a throwaway synthetic parent (P-RECOMPOSE + P-RECOMPOSE-NEG + P-OWNERSHIP) before considering the step done.
5. **Cross-ref re-point sweep** (verification, not churn — numbers preserved): `grep -rn 'operating-disciplines' substrate/ | grep -oE '§[0-9.]+'` cross-checked against the slim core's headings (P-XREF). Confirm every active-file cite still resolves to a real anchor (stub or live).
6. **Run all probes** (P-FLOOR, P-COND, P-STUB, P-XREF, P-C1, P-C2, P-SPLIT, P-INDEX, P-RECOMPOSE, P-RECOMPOSE-NEG, P-OWNERSHIP, P-AUTH, P-KEEP) as a self-check before returning to PLINY.
7. **Commit** with `Co-Authored-By: CAPTAIN_ADA_the-stoa <captain-ada@the-stoa.local>` per op-disc §28. (The slim-core cut + the 13 modules + the install.sh partition land as one coherent commit, or the install.sh partition as a trailing commit if ADA prefers a clean tooling/canon split — ADA's call; both are this arc.)

---

## §6 — install.sh module-OWNERSHIP partition + op-disc recompose (the load-bearing tooling extension)

### 6.1 Why op-disc recompose is required (whole-team losslessness at subproject tier)

op-disc deploys at all 3 tiers (L964-980, `cp`). At subproject tier `DEST_MODULES_DIR=""` (no modules deployed) AND a subproject seat's `Read .claude/modules/X.md` does not resolve reliably (the Arc-2 probe finding). So a slim subproject `operating-disciplines.md` pointing at 13 modules absent from the subproject's `.claude/` would break losslessness at that tier FOR EVERY SEAT (op-disc is universal). The fix is the same as POLYBIUS: recompose-inline the 13 module bodies at their markers at subproject tier. The mechanism (`recompose_module_inline()`, the awk state-machine, the 5 FAIL-LOUD checks A–E, idempotency) ALREADY EXISTS (Arc-2, install.sh L871-957) and is data-driven — this arc REUSES it, with one signature change (§6.4).

### 6.2 op-disc is `cp`'d, not `sed`'d — recompose runs cleanly on it

POLYBIUS/PLINY get a `sed` substitution ({{NAME_SUFFIX}}/{{USER_TIER_DIR}}); op-disc gets a plain `cp` (L978, no template slots). The recompose runs IN PLACE on the deployed file regardless of how it was written. The op-disc recompose call goes AFTER the `cp` at L978, inside the `if [ "$TARGET" = "subproject" ]` block. (The existing POLYBIUS recompose block is L870-962, BEFORE the op-disc `cp` at L964-980. ADA either (a) moves the op-disc `cp` before the recompose block and adds the op-disc call alongside the POLYBIUS call, or (b) adds a second subproject-gated block after L980 for the op-disc recompose. Option (a) is cleaner — one subproject block; §6.5 specifies it.)

### 6.3 The slim-core clause that makes the strategy auditable (mirrors Arc-2 §6.3)

The slim core's §0.5 (or a one-line note at the top) carries the tier-awareness rule so the strategy is visible to a reader, not buried in install.sh:

> **Subproject-tier module access (per design-arc-47 §6):** at subproject tier the CONDITIONAL module content is re-inlined into this file at deploy time (install.sh recompose at the `<!-- MODULE-INLINE:<name> -->` markers) — subproject seats do NOT `Read .claude/modules/<X>.md` (the path does not resolve reliably; claude-code #56686/#31546/#29423). At user/project tier the `Read` channel applies and the markers are inert. Anchor: stoa--xyb + design-arc-45 §6 probe (the proven mechanism this arc extends to op-disc).

### 6.4 The MODULE-OWNERSHIP partition — exact signature change

The current function (L871) takes ONE arg (`$1` = role file). The fix adds a SECOND arg (the owned-module-set) and scopes Checks B/D to it. Check A (marker references a real module source) stays GLOBAL (a marker must point at a real file regardless of owner) — Check A already reads the body from `${SRC_MODULES_DIR}/<name>.md` directly, so it is naturally global; the change is only to how `_module_basenames` (the Check-B/D owned-set) is built.

**Current (L878-883) — builds the owned-set from the GLOBAL glob:**
```bash
_module_basenames=""
for _src in "${SRC_MODULES_DIR}"/*.md; do
  [ -e "$_src" ] || continue
  _bn="$(basename "$_src" .md)"
  [ "$_bn" = "README" ] && continue
  _module_basenames="${_module_basenames} ${_bn}"
done
```

**Fixed — the owned-set is PASSED IN as `$2`:**
```bash
recompose_module_inline() {
  _role_file="$1"
  _module_basenames="$2"   # space-separated owned-module basenames for THIS role file
  # (README is never in an owned-set by construction — owner-sets list relocated modules only.)
  ...
```

The two call sites (replacing the single `recompose_module_inline "$DEST_POLYBIUS"` at L959):
```bash
POLYBIUS_MODULES="onboarding sub-project-spawning pair-programmer-authoring pair-programming-prototyping substrate-update-check"
OPDISC_MODULES="two-polybius-coordination autonomous-mode-setup sub-agent-transcript-discipline verification-complexity bw-fit-matrix oss-dep-and-latency credential-discipline-detail bw-upgrade mechanical-inspection-split multi-team-interop four-layer-identity substrate-component-design jsdom-timing-discipline"
recompose_module_inline "$DEST_POLYBIUS" "$POLYBIUS_MODULES"
recompose_module_inline "$DEST_OPERATING_DISCIPLINES" "$OPDISC_MODULES"
# NOTE: $DEST_PLINY still NOT recomposed (MAJOR_PLINY not cut yet — zero markers, zero owned modules).
#       When PLINY is cut: add PLINY_MODULES + recompose_module_inline "$DEST_PLINY" "$PLINY_MODULES".
```

**Why this is the minimal correct fix:** Check B ("module exists but no marker in THIS file") and Check D ("zero markers but relocatable modules exist") now evaluate against the OWNED set, so POLYBIUS's recompose only checks its 5 and op-disc's only checks its 13. A cross-owner module (op-disc's `autonomous-mode-setup` during POLYBIUS recompose) is not in `$POLYBIUS_MODULES`, so Check B does not flag it. The data-driven property is preserved: a future PLINY cut adds `PLINY_MODULES` + a third call, no new code path. (This realizes the Arc-2 §6.5 generality note — which anticipated the multi-source case but assumed each role file owns ALL modules; the shared-dir reality requires the per-call partition this §6.4 adds.)

### 6.5 Recompose placement + the dry-run path

Restructure so a SINGLE `if [ "$TARGET" = "subproject" ]` block holds the function definition + both calls, placed AFTER op-disc is deployed:

1. Move the op-disc `cp` (L974-980) to BEFORE the recompose block (so `$DEST_OPERATING_DISCIPLINES` exists when recompose runs), OR keep it where it is and move the recompose block to after L980. Either way: both `$DEST_POLYBIUS` and `$DEST_OPERATING_DISCIPLINES` must be written before their recompose call.
2. The function's existing `$DRY_RUN` guard (L887-890) prints the plan and returns without requiring the file to exist — works unchanged for both calls (it prints `modules:${_module_basenames}` which is now the owned-set). The dry-run plan now shows BOTH the POLYBIUS owned-set and the op-disc owned-set.
3. FAIL-LOUD semantics (the rm-both-files-on-error at L947-953) apply per-call: an op-disc recompose failure removes the partial op-disc tmp AND the slim op-disc, exits 2, aborts the deploy — install.sh never ships a partial/slim op-disc to a subproject. (P-RECOMPOSE-NEG asserts this.)

### 6.6 Check E (body-contains-a-marker) interaction with op-disc content

Check E (L922) fails if a module BODY contains a literal `<!-- MODULE-INLINE: -->` line (would corrupt recompose). op-disc's relocated modules carry NO MODULE-INLINE markers in their bodies (the markers live in the SLIM CORE stubs, not in the module content). **One caveat for ADA:** the `autonomous-mode-setup.md` module body contains the renewal-cron prompt-body template with `<PLACEHOLDER:...>` and `{{...}}` slots — confirm none of those is a literal `<!-- MODULE-INLINE:` string (they are not; they are `<PLACEHOLDER:POLLING_CRON_ID>` and `{{RENEWAL_CRON_ID}}` shapes). Check E only matches `^<!-- /?MODULE-INLINE:` — no op-disc module body contains that. (Residual Q2 for ARGUS: confirm no op-disc module body — especially the credential-discipline-detail diagram or the verification-complexity worked examples — carries a literal `<!-- MODULE-INLINE:` string in a code fence.)

---

## §7 — Self-assessed weak points (esp. anywhere losslessness is at risk for ANY seat)

1. **The module-ownership partition is a NEW signature change to a load-bearing deploy function — highest-risk surface, and a regression here breaks BOTH role files at subproject tier.** `recompose_module_inline()` is the only place a marker/module mismatch can drop a body at the hardest-audited tier, and this arc changes its signature (adds the owned-set arg) AND adds a second caller. A bug in the partition (e.g., Check B accidentally still reading the global glob, or an owned-set typo) either false-positives (aborts a clean deploy — P-OWNERSHIP catches) or false-negatives (a real dropped body passes — P-RECOMPOSE catches). *Why this shape anyway:* the shared `substrate/modules/` dir is a hard constraint (the flat-glob deploy + Read-path convention + the Arc-29 `modules/custom/` reservation all forbid owner-subdirs), so the partition MUST live in the call sites; the change is minimal (one arg, scope two checks), the data-driven property is preserved for the future PLINY cut, and P-OWNERSHIP + P-RECOMPOSE + P-RECOMPOSE-NEG exercise the happy path, the cross-owner non-false-positive, and the FAIL-LOUD path end-to-end against a throwaway target. The residual risk is awk-correctness of the scoped Check B, which VERA's throwaway-target probe exercises.

2. **§7 (two-POLYBIUS coordination) is the most heavily cross-cited relocation, and its citers include RUNTIME hook scripts — a stub-vs-content mismatch is most consequential here.** §7.1–§7.7 are cited from templates, hooks (`stop-self-check.sh`, `_hooklib.sh`), and TIRO. A reader (or a future hook author) following `operating-disciplines.md §7.2` lands on a stub pointer, not the content, at user/project tier (the content is in the module, read via the routing the SEAT does, not the hook). *Why this shape anyway:* §7 is genuinely CONDITIONAL by the ambient-vs-conditional test (only two-POLYBIUS-coordination engagements need it; CAPTAINs never do), so KEEPING 138 lines inline for every seat to satisfy a stub-resolution convenience defeats the cut; the runtime hooks cite §7.x in COMMENTS (provenance orientation), not runtime path resolution (confirmed P-XREF), so no hook BREAKS; the stub names §7.1–§7.7 explicitly so the cross-refs RESOLVE to a real anchor; and at subproject tier the recompose re-inlines the full §7.x bodies. The residual risk is purely reader-ergonomic (a human following §7.2 reads a pointer), which is the same trade every Arc-2 relocation made — flagged as A1 for ARGUS to confirm the higher cross-cite density (incl. runtime scripts) does not change the call.

3. **The routing-map-omission (op-disc gets only a relocation index) is a REFINEMENT of the proven pattern, not a verbatim reuse — if the refinement is wrong, every CONDITIONAL relocation's dispatch-time recovery is under-specified.** Arc-1/Arc-2 paired a routing map WITH the relocation index; this design drops the routing map for op-disc on the reasoning that op-disc is not an orchestrator. If ARGUS judges op-disc DOES need a routing-map-equivalent (e.g., because PLINY should dispatch verifier CAPTAINs WITH `verification-complexity.md` named — the A4 case), then the §15/§16/§17/§22/§27/etc. modules need a dispatch-time home that this design puts only in the per-stub `Read` pointer. *Why this shape anyway:* op-disc structurally does not dispatch — the seat that needs a CONDITIONAL module is the seat reading op-disc at the point of need (autonomous-mode entry, credentialed work, probe design), so the inline per-stub pointer IS the correct dispatch-time signal for a non-orchestrator file; the dispatch-time-via-orchestrator cases (verifier CAPTAINs dispatched by PLINY with `verification-complexity.md`) belong in PLINY's routing map, which is a FUTURE PLINY cut, and until then the §15 stub's `Read` pointer + PLINY naming it inline covers it. This is the single most important judgment call in the design and is surfaced as residual Q1 — ARGUS owns confirming the non-orchestrator pattern is correct, because getting it wrong under-specifies recovery for 13 modules across the whole team.

4. **The estimated floor (~700–850) is materially higher than the POLYBIUS cut's (~300–350) because op-disc's KEEP bucket is genuinely larger — a reviewer expecting a POLYBIUS-shaped ratio may read the floor as "cut too shallow."** op-disc keeps MORE inline than POLYBIUS did: the anti-pattern thesis, the universal escalation triggers, the heartbeat contract, the full confabulation discipline, the credential structural core, the PRINCIPAL-gate rule, the base-vs-custom rules, the Co-Authored-By rules, AND the bw-cookbook keep-home (§12) which is ~77 lines that CANNOT relocate (it is where the rest of the substrate points). *Why this shape anyway:* the recalibrated criterion explicitly forbids cutting always-on rules to hit a number, and op-disc's always-on core IS larger because it is THE universal layer — relocating any of those off-disk would break whole-team availability-losslessness (a CAPTAIN that cannot reach the escalation triggers or the credential rule without a Read it does not know to make). P-FLOOR reports the actual floor and guards both ends (>1000 = untightened KEEP prose; <600 = a dropped always-on rule); P-KEEP independently asserts each load-bearing always-on rule is still inline. The floor is honest output, not a target missed.

5. **§10 progression provenance cites stoa--ntn, which I did NOT verify resolves (it was not in the 24-id sample) — a wrong C-1 classification here silently drops the §10 progression empirical.** §10 is KEEP-TIGHTEN (the rules stay), but its progression-canon provenance paragraph (470) compresses to `Anchor: stoa--ntn`, and if stoa--ntn does not exist or does not carry the story, that compression drops canon. *Why this shape anyway:* the design names this explicitly as a per-deletion gate (P-C1 special + build Step 2 `bw show stoa--ntn`): ADA content-checks it at build time, and if it fails, §10's progression prose routes to a C-2 child ticket (the design pre-authorizes the fallback). The risk is bounded by making the check mandatory and the fallback explicit — no silent drop is possible if the gate runs. Flagged so ARGUS confirms the gate-with-fallback is sufficient rather than requiring design-time verification of every single cite (24/24 sampled resolved; stoa--ntn + the cross-repo ariadne--* / railway--* anchors are the unsampled tail ADA content-checks per-deletion).

---

## §8 — Residual questions for ARGUS

1. **Routing-map omission for a non-orchestrator file (the load-bearing refinement, weak point 3).** Does ARGUS concur that op-disc — which dispatches nothing — correctly gets a relocation index but NO routing map, with the per-stub `Read` pointer serving as the point-of-need dispatch-time signal? Or does the A4 case (verifier CAPTAINs dispatched by PLINY WITH `verification-complexity.md` named) argue for a routing-map-equivalent that this design defers to the future PLINY cut? This is the one place the design refines rather than reuses the proven pattern.

2. **Check E / literal-marker-in-body for op-disc modules (§6.6).** The `autonomous-mode-setup.md` body carries the renewal-cron template with `<PLACEHOLDER:...>` + `{{...}}` slots; the `credential-discipline-detail.md` body carries the canonical-pattern diagram; the `verification-complexity.md` body carries six worked examples with code-fence content. I judge none contains a literal `<!-- MODULE-INLINE:` string (Check E only matches that exact prefix). Does ARGUS see a relocated body that would trip Check E?

3. **The four ambient-vs-conditional calls (A1–A4 in §2.6).** A1 (§7 RELOCATE despite runtime-hook citers), A2 (§8.3/§8.4/§8.5 KEEP vs relocate-with-§8), A3 (§25.5 KEEP because DAEDALUS reads it direct at design time), A4 (§15 RELOCATE because verifier CAPTAINs are dispatched-with-brief). The A3-vs-A4 distinction (read-direct-at-design-time = KEEP; dispatched-with-brief = RELOCATE) is the principle I am least sure generalizes — does ARGUS agree with the boundary, or would it draw it elsewhere (e.g., A3 §25.5 should also relocate, with DAEDALUS's envelope §6.7 carrying the `Read` pointer)?

4. **The §20 partial-section relocation (the only one).** §20 keeps its structural rule + 5-anti-pattern table + refusal-as-signal + universal rule inline; only §20.1-detail + §20.5 + §20.6 relocate, with the marker placed AFTER §20.4. Does ARGUS see a losslessness risk in the partial-section shape (vs. either keeping §20 whole or relocating §20 whole)? The structural rule MUST stay inline (always-on credential core); the Railway-specific detail is genuinely conditional — the partial split is the honest call, but it is the one relocation that does not follow the clean whole-section-stub shape.

---

## §9 — Out of scope

- **Cutting MAJOR_PLINY.md** (next epic arc). The §6.4 partition is designed so the PLINY cut adds `PLINY_MODULES` + a third `recompose_module_inline` call with zero new code path — but that cut is a separate arc.
- **Substrate-self-apply re-sync** of the-stoa's deployed `.claude/operating-disciplines.md` (lags source by this arc + Arc 44/46). User-tier POLYBIUS housekeeping per MAJOR_POLYBIUS §18.1.
- **Building the enforcement layer** (stoa--xyb.5). The relocation-index + MODULE-INLINE marker formats are hook-parseable (designed so), but the hook is not built here.
- **Re-homing op-disc §12 (the bw cookbook) into a module.** §12 is the DUPLICATE keep-home for the rest of the substrate; relocating it would break every pointer at it. It stays inline whole — correctly NOT a CONDITIONAL candidate despite being long.
- **A bw attachment-read primitive.** C-2 here uses `bw create --parent -d` (titled child ticket description), recovered via plain `bw show <child-id>` — the bw-0.13.0 no-attachment-read limitation does not bite this arc.
- **Promoting the inspection-agent / verification-complexity / multi-team modules to CAPTAIN seats.** Out of scope per the respective sections' own A-boundaries; this arc relocates the prose, not the architecture.

---

*Self-assessed weak points are in §7. Residual questions for ARGUS are in §8. This is rev1; the next ARGUS/ADA reads THIS file.*
