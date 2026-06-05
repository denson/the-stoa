# Arc 4 (Arc 47) — operating-disciplines.md debloat cut — design rev2

**Ticket:** stoa--xyb.8 (engagement epic stoa--xyb)
**Author:** Denson Smith (the PRINCIPAL — design synthesis, structural choices, relocation ledger)
**Seat:** CAPTAIN_DAEDALUS_the-stoa
**Builds on:** Arc 44 (composition-layer mechanism: `substrate/modules/` glob deploy + `modules/README.md` 3 channels / 3 relocation classes + op-disc §33 thin rule); Arc 45 (MAJOR_POLYBIUS.md cut — the PROVEN stub/marker/recompose pattern; `install.sh` `recompose_module_inline()` shipped data-driven); Arc 46 (hooks tier + op-disc §34 trigger-payload rule).
**Acceptance bar:** LOSSLESS-ON-CANON at ALL tiers (user / project / subproject) for the WHOLE TEAM. operating-disciplines.md is the UNIVERSAL layer every seat loads — POLYBIUS, PLINY, every CAPTAIN, every pair-programmer Major. ARGUS's primary audit target is LOST CANON, whole-team.
**Recalibrated criterion (PRINCIPAL-ratified):** the lossless-floor is an OUTPUT measured per file, NOT a fixed line target. Falsify on LOSSLESS-COMPLETENESS (every chunk homed + recoverable), NOT a line number. Do not cut a load-bearing always-on rule to hit a number. The empirical post-cut floor is REPORTED (§3.10), not targeted.

---

## Changes from rev1 (addressing ARGUS r1–r4)

rev1 (committed 00e2707) was audited PASS-WITH-RISKS: lossless-completeness MET whole-team; 1 BLOCKING + 2 SHOULD-FIX + 1 CONSIDER. rev2 is **targeted fixes, NOT a re-cut.** The lossless ledger, section-number PRESERVE via stubs, the module-ownership partition, C-1/C-2 provenance handling (incl the stoa--ntn gate), relocation-index-no-routing-map (Q1 CONCUR), and the recompose extension to op-disc at subproject tier are all HELD from rev1 unchanged except where a finding touches them. The four changes:

- **r1 [BLOCKING] — SPECIFICATION.md cross-ref regression, fixed with the LOSSLESS option.** rev1's §3.1 cross-ref check scoped its grep to `substrate/` and never grepped `SPECIFICATION.md` (repo root), which is a live op-disc cross-ref consumer via the shipped `validate-spec` resolver (`substrate/skills/validate-spec/_lib/spec_refs.py`). That resolver matches cited `§X.Y` against an EXACT HEADING-LINE in the target. rev1's §7 stub only PROSE-named the relocated subsections, so 7 currently-PASSING op-disc references would flip PASS→FAIL. **rev2 fix:** (a) every relocated section's stub PRESERVES the cited subsection HEADING LINES as real markdown headings (heading line + one-line "relocated to <module>" pointer under each); (b) §3.1 cross-ref check AND P-XREF are extended to run `spec_refs.py` against SPECIFICATION.md and assert ZERO op-disc refs flip PASS→FAIL (new probe **P-SPEC-XREF**); (c) I re-ran the live resolver across ALL 13 relocated sections (not just §7) — the COMPLETE at-risk set + which SPECIFICATION.md subsections are cited is reported in §3.1.2. See §2.7.1 (new stub shape) + §3.1.2 (the SPECIFICATION.md cite census) + §4 P-SPEC-XREF.

- **r2 [SHOULD-FIX] — §15 flipped RELOCATE → KEEP.** ARGUS: VERA §5.7 / CATO §6.7 / ZENO §6.6 / ARGUS §6.6 cite `operating-disciplines.md §15` DIRECTLY from their role files, every dispatch — identical mechanics to §25.5, which rev1 KEEPs under principle A3 (read-direct, no orchestrator dispatches the module). rev1's A4 rationale (PLINY names `verification-complexity.md` in the verifier brief) was factually wrong: PLINY does NOT name the module; the verifier seats reach §15 via their own role-file pointers. **rev2 fix:** §15 is now KEEP-TIGHTEN inline (consistent with §25.5/A3). The false A4 rationale is DELETED. The ledger drops the `verification-complexity.md` module → **12 relocated sections, not 13.** The floor estimate is re-stated slightly higher (§3.10). See §2.4 (§15 moves to KEEP-TIGHTEN), §2.6 (A4 removed; A3 generalized to cover §15), §3.2/§3.8/§3.9 (12 modules), §3.10 (floor).

- **r3 [SHOULD-FIX] — recompose specifies TWO distinct sets.** rev1 §6.4 said "Check A stays global, only Check B/D change," but Check A (install.sh L916 `name in exists`) shares the SAME `exists[]` array that Checks B/D iterate (built from `module_list`, L909). Narrowing `module_list` to the owned-set silently narrows Check A. **rev2 fix:** §6.4 now specifies TWO distinct sets — a GLOBAL EXISTENCE set (Check A: every `substrate/modules/*.md` exists, owner-agnostic) and a per-call OWNED set (Checks B/D: only this file's markers↔modules). The exact awk signature is two `-v` lists, with Check A iterating/testing the global set and Checks B/D iterating/counting the owned set. See §6.4 (rewritten).

- **r4 [CONSIDER] — §20 partial-relocation numbering-order.** rev1 placed the §20 detail-marker AFTER §20.4, so the relocated §20.1 re-inlines after §20.4 at subproject tier (out of numeric order). It is lossless (all content recoverable; external citers §20/§20.3 stay inline — confirmed §3.1.2). **rev2 disposition:** confirmed lossless and left as-is, with the numbering-order note made explicit in §3.2 so ADA does not "fix" it into a re-numbering that would break cross-refs. The §20 detail is genuinely conditional Railway-specific content; placing the marker after §20.4 keeps the always-on structural rule (§20-intro + §20.2 + §20.3 + §20.4) in clean numeric order and isolates the relocated detail at the tail. See §2.6 A-note + §3.2 §20 row.

Everything else is rev1 verbatim-or-tightened. Where a number changed (13→12 modules; floor band), the change is propagated through every section.

---

## §1 — Problem restatement (pre-work gate)

`substrate/operating-disciplines.md` is **2156 lines** — the worst offender in the substrate, and uniquely costly because it is the UNIVERSAL-team layer every seat loads on activation. It grew from 2110 at epic start via §33 (Arc 44) + §34 (Arc 46). At 2156 lines it is far over the 25k-token harness read cap (the live file paginates across multiple reads; a CAPTAIN that needs to ground against a single discipline pays the read cost of the whole monolith).

The diagnosis is the same empirical-anchor + provenance accretion the POLYBIUS cut diagnosed, amplified: every discipline §N carries a rule + worked example + a multi-paragraph "N=1 provenance + accretion path" + a "Cross-references" subsection. The *actionable always-on* canon — the rules a seat needs on every turn — is roughly a quarter of the lines. The rest splits into (a) procedures only SOME seats need only SOMETIMES (CONDITIONAL), (b) the why/empirical record (PROVENANCE), and (c) content duplicated elsewhere (DUPLICATE).

This arc applies the Arc-1 debloat method (3 relocation classes — CONDITIONAL → disk module, PROVENANCE → bw cite, DUPLICATE → pointer) to op-disc section by section, **for the whole file**, and extends the Arc-2 subproject-recompose mechanism to cover op-disc as a second recompose source. The KEEP bucket is the universal always-on operational core every seat needs every turn; the RELOCATE buckets are everything genuinely conditional, historical, or duplicated.

### 1.1 Imported assumptions (named per §6.1 of the seat envelope — real briefs have implicit scope)

1. **op-disc is NOT an orchestrator — it gets a RELOCATION INDEX but NOT a routing map.** This is the load-bearing refinement of the Arc-1/Arc-2 pattern for this file (§2.2). The Arc-1 composition layer pairs a routing map (dispatch-time: task-type → module → channel) with a relocation index (audit-time: relocated-content → home → class). The routing map is an ORCHESTRATOR artifact — it answers "at dispatch time, what does this task need?" op-disc does not dispatch anything; its CONDITIONAL modules are read by the SEAT THAT NEEDS THEM at the moment that seat hits the task (a seat entering autonomous mode reads `autonomous-mode-setup.md`; a seat hitting credentialed work reads `credential-discipline-detail.md`). So op-disc carries the relocation index (the losslessness-recovery artifact ARGUS audits) but NO routing map. The per-section stub's "recover via Read" pointer IS the dispatch-time guidance, inline at the point of need — that is the correct shape for a non-orchestrator file. **(ARGUS Q1 CONCUR rev1 — held.)**

2. **CONDITIONAL content relocates to NEW disk modules under `substrate/modules/`** alongside the 5 Arc-2 POLYBIUS modules + README. This arc CREATES + POPULATES the new op-disc modules. Naming + per-module contents are in §2.3. **(rev2: 12 modules, §15 dropped from the set per r2.)**

3. **The shared `substrate/modules/` dir forces a module-OWNERSHIP partition in install.sh** (§2.7 + §6). `recompose_module_inline()` today scopes Checks B/D to the GLOBAL `substrate/modules/*.md` glob. Once op-disc modules share the dir, POLYBIUS's recompose would FALSE-POSITIVE Check B on the op-disc modules (they carry no POLYBIUS marker). The fix is to scope each recompose call's Checks B/D to a per-call OWNED-module-set while keeping Check A's existence test GLOBAL (rev2 r3 — two distinct sets, §6.4). This is the load-bearing install.sh extension of this arc.

4. **op-disc deploys at ALL three tiers** (user / project / subproject) — confirmed live at install.sh L964–980 (`cp` to `<DEST_DIR>/operating-disciplines.md`, unconditional, all tiers). At subproject tier the modules dir is NOT deployed (`DEST_MODULES_DIR=""`) AND a subproject seat's `Read .claude/modules/X.md` does not resolve reliably (the Arc-2 probe finding, claude-code #56686/#31546/#29423). So op-disc's CONDITIONAL modules MUST recompose-inline at subproject tier exactly as POLYBIUS's do — op-disc is recompose-eligible and the recompose must run on `$DEST_OPERATING_DISCIPLINES`.

5. **Section numbers AND cited subsection-heading lines are PRESERVED via stubs, NOT renumbered.** op-disc §N is cross-referenced by EVERY role file, every module, the templates, the hooks, the skills, op-disc's own internal cross-refs, AND `SPECIFICATION.md` via the `validate-spec` mechanical resolver (rev2 r1 — the surface rev1 missed). The cross-ref graph (§3.1, grepped live this design phase across `substrate/` AND SPECIFICATION.md) shows nearly every top-level §N — and several SUBSECTIONS of §7 — are cited from an active resolution-consuming surface. Renumbering would break the entire substrate's cross-ref graph. Every relocated section leaves a numbered stub so all top-level `operating-disciplines.md §N` cites still resolve; AND every cited SUBSECTION (the §7.1/§7.2/§7.4/§7.5 spec cites) leaves its subsection HEADING LINE intact in the stub so the exact-heading-match resolver still resolves it (rev2 r1). (Arc-2 precedent for the top-level preserve; PRINCIPAL-ratified there as CONCUR. The subsection-heading preserve is the rev2 r1 extension.)

6. **op-disc has NO author-like frontmatter field and the new modules must carry none** (P-AUTH guards). op-disc's content — the synthesis — is the PRINCIPAL's per the immutable authorship rule; cited empirical anchors are attributed to their tickets, which is source-citation not authorship.

The restatement converges with the brief. The one place it does more than paraphrase — the routing-map-vs-relocation-index distinction for a non-orchestrator file (assumption 1) — was surfaced as residual Q1 in rev1 and ARGUS CONCURRED; it is held. The rev2-new load-bearing scope addition is assumption 5's extension: cited subsection-heading lines (not just top-level §N) must be stub-preserved because of the exact-heading-match spec resolver rev1 did not account for.

---

## §2 — Approach (the slim structure)

### 2.1 The slim core shape

Post-cut, `operating-disciplines.md` is the **slim universal operational core**: crisp rule per discipline + a one-line cite-back (stub + `Read` pointer for CONDITIONAL; `Anchor:` for PROVENANCE; pointer for DUPLICATE) + ONE always-loaded **relocation index** table (the losslessness-recovery artifact). The CONDITIONAL procedures move to disk modules; the provenance/empirical multi-paragraph blocks move to bw cites; the one DUPLICATE consolidates to a pointer. The always-on rules (the anti-pattern thesis, escalation triggers, heartbeat contract, confabulation discipline, PRINCIPAL-gate rule, credential structural rule, the verification-complexity framework (rev2 KEEP per r2), the composition + trigger-payload thin rules) stay inline, tightened.

### 2.2 The always-loaded RELOCATION INDEX (no routing map — op-disc is not an orchestrator)

Per modules/README.md §4, the composition layer pairs a routing map (dispatch-time) with a relocation index (audit-time). **op-disc gets ONLY the relocation index** (assumption 1; ARGUS Q1 CONCUR). The index is added as a new **§0.5 "Relocation index (audit-time — where relocated content went)"** placed immediately after the thesis, BEFORE §1, so the always-loaded recovery table sits at the top of the operational core. It uses the regular index column shape from modules/README.md §4.2 (relocated-content → new-home → class) so a future enforcement-layer hook is parseable. The index is populated in §3 of THIS design.

**Why no routing map:** the routing map answers "at dispatch time, what module does this task need?" — an orchestrator question. op-disc dispatches nothing. The dispatch-time signal a reader needs ("you are entering autonomous mode → read `autonomous-mode-setup.md`") lives INLINE at the §N stub, at the point of need, because the reader arriving at op-disc §11 is the seat that just hit the autonomous-mode trigger. Putting a routing map in op-disc would duplicate the per-stub pointers into a table no orchestrator consults. The stubs ARE the routing, distributed to point-of-need. (ARGUS Q1 CONCUR rev1.)

### 2.3 The CONDITIONAL module files (CREATED + POPULATED this arc) — 12 modules (rev2)

Each module is a self-contained reference body; the module's first line is a stable `# <Title>` heading (the recompose keys on it; P-RECOMPOSE asserts it appears) followed by a provenance header citing this design + the stoa--xyb epic (mirroring modules/README.md:14–16). **No module carries an author-like field** (P-AUTH). Line ranges are grounded against the LIVE source (re-read this design phase).

| Module file | Source § (live line range) | What moves in |
|---|---|---|
| `substrate/modules/two-polybius-coordination.md` | §7 (115–252) | §7 intro + §7.1 radio-check + §7.2 adaptive cadence + §7.3 unified poll + §7.4 cross-tier routing + §7.5 write boundaries + §7.7 bw-timeline parsing. (§7.6 empirical lineage → PROVENANCE Anchor, NOT into module — see §3.4.) **rev2 r1:** the §7 stub keeps §7.1/§7.2/§7.3/§7.4/§7.5/§7.7 as REAL HEADING LINES (the BODY moves to the module). |
| `substrate/modules/autonomous-mode-setup.md` | §11 (478–726) | The full 7-step setup checklist incl. step 1.5 renewal-cron machinery (the renewal-cron prompt-body template, the 4-step terminating-shape dance, the failure-mode acceptance), steps 2–9. This is the single largest relocation (~249 lines). |
| `substrate/modules/sub-agent-transcript-discipline.md` | §14 (820–833) | §14 full body (kill-time JSONL capture, save target, read-side discipline, open-question). |
| `substrate/modules/bw-fit-matrix.md` | §16 (920–961) | §16 intro + §16.1 matrix + §16.2 layered architecture + §16.3 decision rule. (§16's empirical anchor → Anchor.) |
| `substrate/modules/oss-dep-and-latency.md` | §17 (962–1001) | §17 intro + §17.1 fork-over-upstream + §17.2 agent-time latency budget. (§17's empirical anchor → Anchor.) |
| `substrate/modules/credential-discipline-detail.md` | §20 (1238–1338) **minus the structural rule + 5-anti-pattern list that stay inline** (see §2.5) | §20.1 canonical pattern diagram + numbered detail, §20.5 Railway-specific notes, §20.6 cross-reference. The §20 intro structural rule, §20.2 five-anti-pattern table, §20.3 refusal-as-signal, §20.4 universal rule STAY INLINE (always-on credential core). |
| `substrate/modules/bw-upgrade.md` | §22 (1363–1424) | §22 intro + §22.1 5-step + §22.2 3-axis + §22.4 check-bw-release skill + §22.5 cross-refs. (§22.3 N=1 provenance → Anchor.) |
| `substrate/modules/mechanical-inspection-split.md` | §27 (1627–1702) | §27 intro + §27.1 declaration + §27.2 3-step + §27.3 when-to-apply/A7 + §27.4 per-seat + §27.5 worked example. (§27.6 N=1 provenance → Anchor; §27.7 cross-refs SPLIT.) |
| `substrate/modules/multi-team-interop.md` | §29 (1825–1906) | §29 intro + §29.1–§29.5. (§29.6 N=1 provenance → Anchor; §29.7 cross-refs SPLIT.) |
| `substrate/modules/four-layer-identity.md` | §30 (1907–1972) | §30 intro + §30.1–§30.4. (§30.5 N=1 provenance → Anchor; §30.6 cross-refs SPLIT.) |
| `substrate/modules/substrate-component-design.md` | §31 (1973–2043) | §31 intro + §31.1 Principle 1 + §31.2 Principle 2. (§31.3 N=2 provenance → Anchor; §31.4 cross-refs SPLIT.) |
| `substrate/modules/jsdom-timing-discipline.md` | §32 (2044–2090) | §32 full body (the discipline + helper contract + empirical anchor + cross-refs — small enough to move whole). |

**12 CONDITIONAL module files created + populated this arc.** (rev1 had 13; **§15 verification-complexity is no longer relocated** — it is KEEP-TIGHTEN per r2.)

### 2.4 KEEP-TIGHTEN sections (stay inline; prose tightened; no relocation)

The universal always-on operational core. These are read across turns by every seat (or are the keep-home for a DUPLICATE, or are themselves the thin composition/trigger rules):

- **§1–§6 (the anti-pattern thesis + redundancy core, 37–114).** Always-on framing every seat reads; the six anti-patterns ARE the doc's reason for existing. §6.7 carries provenance (the stoa--nax empirical) that compresses to an Anchor; the §6.7.1/§6.7.2 RULES stay (they are operational — the N=1-canon-promotion gate is cited from many sections).
- **§8.1 + §8.2 (positive references only + scaffolding, within 253–373).** Universal authoring discipline (every brief author, every turn that authors a downstream artifact). Rules stay; the §8.1/§8.2/§8.3/§8.5 empirical anchors compress to Anchors. **§8.3 (activation-paste session-state) + §8.4 (install.sh deploy-plan smoke beat) + §8.5 (fallback-chain probe coverage) are CONDITIONAL-leaning** — see §2.6 ambiguity flag; rev2 KEEPS them inline tightened (they are short and operationally cross-cited) and holds the rev1 call (ARGUS Q3 concurred A2). 
- **§9 (bw storage model, 374–413).** Universal (every bw-using seat). The worktreeconfig fix is operational; the historical regression-window prose (400) + the stoa--7kg lineage (404) compress to an Anchor.
- **§10 (HITL/Autonomous engagement, 414–477).** KEEP-TIGHTEN WHOLE — carries the universal escalation triggers (443) read every autonomous engagement (Arc-2 precedent: the analogous POLYBIUS §13 was KEEP-TIGHTEN, ARGUS CONCUR). The §10 progression-canon provenance paragraph (470) compresses to an Anchor (stoa--ntn — ARGUS WP4 confirmed it resolves + carries the progression table); the rules + trigger-words tables + transition-triggers table stay.
- **§12 (bw cookbook, 727–803).** KEEP — this section is the DUPLICATE keep-HOME itself (every other bw-using file points here; it self-declares "do not duplicate" at 729). It stays inline, whole. (Tighten only obviously verbose prose; do NOT relocate — relocating the keep-home would break every pointer at it.)
- **§13 (Windows Python, 804–819).** KEEP (universal, 16 lines, already tight). Compress the §13 empirical (814) to an Anchor.
- **§15 (verification-complexity, 836–919) — rev2 NEW KEEP-TIGHTEN (was RELOCATE in rev1).** Per r2: VERA §5.7 / CATO §6.7 / ZENO §6.6 / ARGUS §6.6 cite `operating-disciplines.md §15` DIRECTLY from their role files, every dispatch — identical read-direct mechanics to §25.5 (A3 KEEP). No orchestrator dispatches the module; the verifier seat reaches §15 by reading op-disc, so KEEPING it inline is the consistent call. **Tighten:** the §15.6 six worked examples compress to the two or three most load-bearing ones (the rest fold to a one-line "see Anchor for the full worked set"); §15's empirical anchor (838 — stoa--tp1) compresses to `Anchor: stoa--tp1`. The §15.1 2×2 + §15.2 rule + §15.3 four strategies + §15.4 two verdict shapes (cited from save-verdict/SKILL.md + _save_verdict.py at §15.4) + §15.5 time/cost box + §15.7 self-referential STAY (rules + the cited §15.4 anchor). Net inline ~55–65 lines after tighten.
- **§18 (subagent status + heartbeat, 1002–1080).** Rules KEEP (the heartbeat contract §18.1 + read-before-write §18.2 + the Monitor/run_in_background prohibitions §18.4 are universal CAPTAIN core, cited from every CAPTAIN role file + TIRO §206). §18.5 dispatch-sequence table stays (operational). §18.7 empirical lineage → Anchor; §18.6 SPLIT (live tool-availability rules stay; the SendMessage empirical-lineage paragraph → Anchor).
- **§19 (confabulation, 1081–1237).** Rules KEEP (§19.1 two halves + §19.2 three patterns + §19.3 contrast + §19.4 relationship — universal always-on, cited from MAJOR_POLYBIUS §223 / TIRO §28,§92). The HEAVY provenance compresses: §19.5 lineage → Anchor; §19.6 attestation-confabulation RULE stays (it is operational + cross-cited §19.6) but §19.6.1 empirical / §19.6.4 N=1 provenance → Anchor; §19.7 idle-retro RULE stays but §19.7.1 empirical / §19.7.5 N=1 provenance → Anchor; §19.6.3 + §19.7.6 cross-refs SPLIT.
- **§20 structural core (intro rule + §20.2 + §20.3 + §20.4, within 1238–1338).** KEEP inline — credential discipline is always-on (the "agents NEVER hold credentials" rule + the 5 rejected anti-patterns a seat must recognize + refusal-as-signal + the universal split). Only the §20.1 worked diagram-detail + §20.5 Railway-specific + §20.6 skill-cross-ref relocate (CONDITIONAL detail). §20.7 lineage → Anchor. (rev2 r4: the detail-marker placement after §20.4 is confirmed lossless; see §3.2 §20 row.)
- **§21 (Ariadne-search authoring, 1339–1362).** KEEP-TIGHTEN (universal authoring discipline, 24 lines). §21 empirical (1359) → Anchor.
- **§23 rules (1425–1483).** KEEP (base-vs-custom is cited from install.sh + check.sh + apply.sh at ~10 sites + §216). §23.1 source-of-truth declaration + §23.2 path convention + §23.3 by-seat discipline stay. §23.4 N=1 provenance → Anchor; §23.5 cross-refs SPLIT.
- **§24 (arc-build branch hygiene, 1484–1505).** KEEP — already a thin cross-ref to MAJOR_PLINY §5.9 (22 lines). Compress the §24 empirical-anchor bullet (1502) into the existing cross-ref block.
- **§25 rules (1506–1607).** KEEP (PRINCIPAL-gate is always-on, cited from templates + skills + DAEDALUS/ADA/VERA envelopes). §25.1 declaration + §25.2 two-axis + §25.3 BLOCK-not-TAG + §25.4 per-seat table stay. **§25.5 probe-design sub-case (the `--no-local` throwaway-clone detail) is CONDITIONAL by audience** (only DAEDALUS-at-probe-design + VERA need it), but it is the explicit catch-point canon DAEDALUS reads at DESIGN time — and DAEDALUS reads op-disc not a module. rev2 KEEPS §25.5 inline (it is the catch-point canon; same read-direct logic that now also keeps §15 — see A3 generalized in §2.6) and compresses only the CVE prose verbosity. §25.6 N=1 provenance → Anchor; §25.7 cross-refs SPLIT.
- **§26 (cron hygiene, 1608–1626).** KEEP — already thin cross-ref to MAJOR_POLYBIUS §5.1.3 (19 lines). Compress the empirical-anchor bullet.
- **§28 rules (1703–1824).** KEEP (Co-Authored-By trailer is cited from global CLAUDE.md + MAJOR_PLINY §5.12 + CAPTAIN_ADA §5.5; the trailer FORMAT §28.1 + scope §28.2 + squash-merge §28.3 + §28.3.1 pitfall + §28.4 frontmatter-boundary + §28.5 read-discipline are all operational). §28.6 future-extension stays (short). §28.7 N=1 provenance → Anchor; §28.8 cross-refs SPLIT.
- **§33 (composition layer, 2091–2116).** KEEP — this IS the thin always-loaded rule the modules/README.md is the detail for. Stays whole.
- **§34 (trigger-payload, 2117–2156).** KEEP — the thin always-loaded rule (just shipped Arc 46). Stays whole.

### 2.5 PROVENANCE relocations (C-1 / C-2 / SPLIT disposition per §3.3 / §3.4 / §3.6)

The "N=1 provenance + accretion path" + "Cross-references" subsections at the tail of disciplines relocate to bw cites. The slim core keeps the RULE + a one-line `Anchor: <bw-id>` cite-back. C-1 (already-in-bw) vs C-2 (not-in-bw) per-row in §3.3 / §3.4; the SPLIT cross-ref subsections get per-line LIVE-vs-PROVENANCE enumeration in §3.6.

### 2.6 Ambient-vs-conditional CALLS — flagged for ARGUS (rev2: A4 removed; A3 generalized to cover §15)

These are genuine ambient-vs-conditional judgment calls. rev2 makes a defensible KEEP/RELOCATE call for each. **rev1 had A1–A4; rev2 RESOLVES A4 by flipping §15 to KEEP (r2) and FOLDS §15 into the A3 read-direct principle.** A1/A2/A3 are held (ARGUS Q3 concurred all three).

- **A1 — §7 (two-POLYBIUS coordination): RELOCATE to module, BUT it is the most heavily-cross-cited candidate AND the only one whose SUBSECTIONS are spec-cited.** §7.1/§7.2/§7.4/§7.5/§7.7 are cited from `polling-cron-prompt-template.md`, `paste-instruction-template.md`, `autonomous-mode-activation-template.md`, `stop-self-check.sh`, `_hooklib.sh`, MAJOR_PLINY, MAJOR_POLYBIUS, TIRO, onboarding.md — AND §7.1/§7.2/§7.4/§7.5 are cited from `SPECIFICATION.md` via the validate-spec exact-heading resolver (rev2 r1; census §3.1.2). The ambient-vs-conditional test: does EVERY seat need §7 EVERY turn? **No** — §7 fires only when two POLYBIUS seats coordinate async. CAPTAINs never coordinate two-POLYBIUS. So §7 is genuinely CONDITIONAL (ARGUS A1 CONCUR). **rev2 r1 refinement:** the §7 stub must preserve every cited subsection number as a REAL HEADING LINE (not just prose-name it) so the exact-heading-match spec resolver still resolves §7.1/§7.2/§7.4/§7.5. The stub shape in §2.7.1 does this.
- **A2 — §8.3 / §8.4 / §8.5: KEEP inline (held) vs relocate-with-§8.** §8.1 + §8.2 are unambiguously KEEP (universal authoring). §8.3/§8.4/§8.5 are arguably CONDITIONAL but short, operationally cross-cited, and splitting §8 fragments a coherent section below the line-savings-justifies-a-module threshold. rev2 KEEPS them inline tightened (ARGUS Q3 concurred A2).
- **A3 (generalized in rev2 to cover both §25.5 AND §15) — read-direct-via-role-file content stays inline even when conditional-by-audience.** The principle: a discipline that a specific set of seats reaches by reading op-disc DIRECTLY (via a pointer in their OWN role file), rather than by being dispatched a module, stays INLINE — because relocating it would require those seats to know to `Read` a module that no orchestrator hands them. Two cases now sit on this principle:
  - **§25.5 (probe-design throwaway-clone sub-case):** DAEDALUS reaches it at design time by reading op-disc §25. KEEP.
  - **§15 (verification-complexity) — rev2 NEW under A3:** VERA §5.7 / CATO §6.7 / ZENO §6.6 / ARGUS §6.6 reach §15 by reading op-disc §15 via their own role-file pointers, every dispatch. No orchestrator names `verification-complexity.md` in a brief (rev1's A4 claim was factually wrong — ARGUS r2). So by the SAME read-direct principle as §25.5, §15 is KEEP. **This RESOLVES the rev1 A3-vs-A4 boundary that did not actually distinguish the two cases:** both are read-direct-via-role-file → both KEEP. The boundary is no longer "read-direct (KEEP) vs dispatched-with-brief (RELOCATE)"; it is simply "read-direct-via-role-file → KEEP." (rev2 deletes the false A4 dispatched-with-brief category; no op-disc section actually falls in it.)
- **A-note (was A4 in rev1; now a CONSIDER disposition, r4) — §20 partial-section relocation numbering-order.** §20 is the ONLY partial-section relocation (structural rule stays, Railway-detail moves). The detail-marker sits AFTER §20.4, so the relocated §20.1 re-inlines after §20.4 at subproject tier (out of numeric order). Confirmed lossless: all content recoverable; the only external citers are §20 (SPECIFICATION.md L569 + BARTLEBY §130) and §20.3 (SPECIFICATION.md L568 + MAJOR_POLYBIUS), both of which stay inline (§3.1.2). rev2 leaves the placement as-is (the always-on structural core §20-intro/§20.2/§20.3/§20.4 stays in clean numeric order; the conditional detail is isolated at the tail), with the numbering-order note made explicit so ADA does not "tidy" it into a renumber that would break the §20/§20.3 cross-refs.

---

## §2.7 — §-numbering coherence + cited-subsection-heading preserve + the recompose marker + the MODULE-OWNERSHIP partition

### 2.7.1 Section-number + cited-subsection-heading PRESERVE via stubs (rev2 r1 — the lossless cross-ref fix)

The slim core PRESERVES section numbers AND every cited subsection heading line. Each CONDITIONAL whole-section relocation leaves a stub at its original number (heading + `Read` pointer + paired recompose marker). §7 stays §7, §11 stays §11, §16/§17/§20-detail/§22/§27/§29/§30/§31/§32 stay at their numbers. Every existing top-level cross-ref (`operating-disciplines.md §N` from role files, modules, templates, hooks, skills, install.sh, SPECIFICATION.md) still resolves to a real anchor.

**The rev2 r1 fix — cited subsection HEADING LINES are preserved as real headings, not prose-named.** rev1's stubs only PROSE-named the relocated subsections ("Covers §7.1 radio-check, §7.2 adaptive cadence …"). The `validate-spec` resolver (`spec_refs.py`) resolves a cited `§7.1` by requiring an EXACT HEADING-LINE match (`_heading_pattern_for_anchor`: matches `### 7.1 …`, `## §7.1 …`, or `**§7.1 …**`), and a prose mention does NOT match. So rev1's §7 stub would have flipped 7 currently-PASSING SPECIFICATION.md refs to FAIL. The fix: **the §7 stub keeps the cited subsection heading lines as real markdown headings, with a one-line pointer under each.**

**Exact stub shape (CONDITIONAL whole-section relocation, NO cited subsections) — the literal ADA writes** (mirrors Arc-2 §2.7 verbatim modulo the module name; used for §11, §14, §16, §17, §22, §27, §29, §30, §31, §32 — none of these have spec-cited SUBSECTIONS, only top-level § cites, so a single §-heading stub suffices):
```
## 11. Autonomous-mode-setup checklist
Relocated to `.claude/modules/autonomous-mode-setup.md` (CONDITIONAL — read when a seat detects an autonomous-mode trigger that applies to itself).
Recover the full 7-step procedure via `Read .claude/modules/autonomous-mode-setup.md`. Relocation-index row in §0.5.
<!-- MODULE-INLINE:autonomous-mode-setup -->
<!-- /MODULE-INLINE:autonomous-mode-setup -->
```

**Exact stub shape (CONDITIONAL relocation WITH cited subsections — §7) — the rev2 r1 shape.** §7's body relocates whole, but §7.1/§7.2/§7.4/§7.5 are cited from SPECIFICATION.md via the exact-heading resolver (and §7.1/§7.2/§7.4/§7.5/§7.7 from substrate templates/hooks). The §7 stub keeps each cited subsection as a REAL HEADING LINE so the resolver resolves it; the recompose markers sit at the END so subproject re-inline appends the full bodies once (idempotent), and the heading-only stub lines coexist with the re-inlined bodies (the resolver finds the first matching heading either way):
```
## 7. Coordinating two POLYBIUS seats async via bw polling
Relocated to `.claude/modules/two-polybius-coordination.md` (CONDITIONAL — read when two POLYBIUS seats coordinate async via bw polling). The subsection headings below are stub anchors (cross-ref-resolvable); recover each subsection's BODY via `Read .claude/modules/two-polybius-coordination.md`. Relocation-index row in §0.5.

### 7.1 Radio-check protocol
Relocated → `two-polybius-coordination.md` §7.1.
### 7.2 Adaptive polling cadence
Relocated → `two-polybius-coordination.md` §7.2.
### 7.3 Unified polling pattern
Relocated → `two-polybius-coordination.md` §7.3.
### 7.4 Cross-tier coordination routing
Relocated → `two-polybius-coordination.md` §7.4.
### 7.5 Cross-tier write boundaries
Relocated → `two-polybius-coordination.md` §7.5.
### 7.7 bw-timeline parsing: author-attribution via tags
Relocated → `two-polybius-coordination.md` §7.7.
<!-- MODULE-INLINE:two-polybius-coordination -->
<!-- /MODULE-INLINE:two-polybius-coordination -->
```

Notes on the §7 stub:
- The cited subsections that MUST be real heading lines for spec resolution are **§7.1, §7.2, §7.4, §7.5** (the SPECIFICATION.md cites — census §3.1.2). §7.3 and §7.7 are NOT spec-cited but ARE substrate-cited (§7.7 from TIRO §176; §7.3 internal) — rev2 keeps them as heading lines too for uniformity and to keep the substrate-cite resolution clean. §7.6 (empirical lineage) is NOT cited and relocates to a PROVENANCE Anchor, so it gets NO stub heading (its absence is correct — nothing resolves to §7.6).
- A reader following `operating-disciplines.md §7.2` (human or the spec resolver) lands on the real `### 7.2 Adaptive polling cadence` heading line, which points at the module. At subproject tier the recompose re-inlines the full §7.x bodies BELOW the markers; the resolver matches the FIRST `### 7.2` heading (the stub anchor) — both the stub heading and the re-inlined body heading exist, which is harmless (the resolver returns the first match line; the body is present for the reader). This is the A1 trade-off ARGUS adjudicated as CONCUR, now with the spec-resolution gap closed.
- **Why heading-only stub lines (not the full subsection bodies inline):** keeping the heading line costs ~2 lines per cited subsection (~12 lines for §7) and is the minimal change that keeps the exact-heading resolver GREEN while still relocating the BODY (the bloat). This is strictly cheaper than KEEPing §7 whole (138 lines) and strictly more lossless than rev1's prose-only stub. P-SPEC-XREF asserts ZERO op-disc refs flip PASS→FAIL.

The paired sentinel `<!-- MODULE-INLINE:<module-name> -->` … `<!-- /MODULE-INLINE:<module-name> -->` is the recompose hook (machine-parseable, inert HTML comment at user/project tier, idempotency anchor at subproject tier). `<module-name>` is the module basename without `.md`. Same justification as Arc-2 §2.7. The PROVENANCE `Anchor:` cites and the §-stubs for sections whose RULE stays inline carry NO recompose marker — only the 12 whole-section CONDITIONAL relocations re-inline at subproject tier.

### 2.7.2 The MODULE-OWNERSHIP partition (THE load-bearing install.sh extension — §6 specifies it)

**The problem (live-confirmed):** `recompose_module_inline()` (install.sh L871–957) builds `_module_basenames` from the GLOBAL `${SRC_MODULES_DIR}/*.md` glob (minus README, L878–883) and a single `exists[]` array (built from `module_list`, L909) backs Check A (L916), Check B (L945), and Check D (L944). Today all 5 modules are POLYBIUS-owned and all 5 are marked in MAJOR_POLYBIUS.md, so `recompose_module_inline "$DEST_POLYBIUS"` passes. **Once this arc adds 12 op-disc modules to the shared dir, `recompose_module_inline "$DEST_POLYBIUS"` Check B sees 17 modules, finds 12 with no POLYBIUS marker → `fail` → aborts the subproject deploy.** This is a hard regression the cut introduces if not fixed.

**The fix (rev2 r3 — TWO distinct sets):** scope each recompose call's Checks B/D to a per-call OWNED-module-set, while keeping Check A's existence test against the GLOBAL module set. `recompose_module_inline()` takes a SECOND argument (the owned-module basenames THIS role file owns) AND the awk receives BOTH a global-existence list and the owned list. Check A (marker → real module source) iterates/tests the GLOBAL set (a marker must reference a real module file regardless of owner — its guarantee must NOT narrow with the owned-set). Checks B/D (owned-module-consumed / per-file-marker-presence) iterate/count the OWNED set. §6.4 gives the exact two-list signature. This keeps the flat-glob deploy + Read-path convention (no owner-subdirs, no collision with the Arc-29 `modules/custom/` reservation) — the partition lives in the recompose call sites + the two awk lists, not the filesystem.

---

## §3 — The relocation ledger (the losslessness proof artifact)

This ledger is the artifact ARGUS audits for LOST CANON, whole-team. **One row per relocated chunk.** Every empirical anchor + every section in the 2156-line source either appears as a ledger row with a lossless home OR is a KEEP-TIGHTEN section that stays inline (§3.7 lists those for audit completeness). Line ranges are grounded against the LIVE `substrate/operating-disciplines.md` (re-read this design phase).

### 3.1 Cross-ref-preservation check (which op-disc §N are cited elsewhere — confirmed for stub-preserve)

Grepped live across `substrate/` (active files only — role files, install.sh, hooks, templates, skills, modules) AND `SPECIFICATION.md` at repo root via the `validate-spec` resolver (rev2 r1 — the surface rev1 missed; arc directives + pastes are frozen history, not stub-resolution consumers). Distinct op-disc §N cited from ACTIVE files:

| §N cited | Citing active files (sample) | Disposition under this cut |
|---|---|---|
| §6, §6.7.1 | §6.7.1 cited internally + by §-promotion gate in many sections | KEEP-TIGHTEN (stub n/a — rule stays inline) |
| §7, §7.1, §7.2, §7.4, §7.5, §7.7 | polling-cron-prompt-template, paste-instruction-template, autonomous-mode-activation-template, stop-self-check.sh, _hooklib.sh, TIRO §176 (§7.7), **SPECIFICATION.md §7.1/§7.2/§7.4/§7.5 via validate-spec** | **§7 RELOCATE → stub preserves §7 + §7.1/§7.2/§7.3/§7.4/§7.5/§7.7 as REAL HEADING LINES** (A1 + rev2 r1) |
| §8, §9 | templates (§8, §9) | KEEP-TIGHTEN (rules stay; stub n/a) |
| §10, §10.1 | (internal + templates) | KEEP-TIGHTEN WHOLE |
| §11 | autonomous-mode-activation-template §40, polling-cron-prompt-template (multi), **SPECIFICATION.md §11 (L280, L581) — top-level** | **§11 RELOCATE → stub preserves §11** (top-level heading; no spec-cited subsections) |
| §12, §12.1, §12.2, §12.4 | MAJOR_PLINY §618, TIRO (~15 cites), pretooluse-no-dash-m-bw-comment.sh §8, validate-spec spec_refs.py §42 | KEEP (§12 is the DUPLICATE keep-home; stays whole) |
| §13 | check-bw-release/check.sh §94, _hooklib.sh §28 | KEEP-TIGHTEN |
| §15, §15.4 | save-verdict/SKILL.md §126–128, _save_verdict.py §221/232/239, VERA §5.7 / CATO §6.7 / ZENO §6.6 / ARGUS §6.6, **SPECIFICATION.md §15 (L202) — top-level** | **§15 KEEP-TIGHTEN inline (rev2 r2)** — heading + §15.4 stay live |
| §16 | (internal), **SPECIFICATION.md §16 (L583) — top-level** | **§16 RELOCATE → stub preserves §16** (top-level; no spec-cited subsections) |
| §17 | (internal), **SPECIFICATION.md §17 (L93) — top-level (Arc 29 §17 incidental, resolves to op-disc §17 stub)** | **§17 RELOCATE → stub preserves §17** |
| §18, §18.5 | TIRO §206, polling-cron-prompt-template §215 | KEEP (rules stay inline; stub n/a) |
| §19, §19.6, §19.7 | MAJOR_POLYBIUS §223, TIRO §28/§92, MAJOR_PLINY (internal) | KEEP (rules stay inline; stub n/a) |
| §20, §20.3 | BARTLEBY §130, **SPECIFICATION.md §20 (L569) + §20.3 (L568) — both KEEP inline** | KEEP structural rule + §20.3 inline (stub n/a); §20.1/§20.5/§20.6 detail relocates |
| §22, §22.2 | check-bw-release/check.sh §89/161, SKILL.md §3/§54 | **§22 RELOCATE → stub preserves §22** (no spec cite; §22.2 named in stub prose for substrate citers) |
| §23 | install.sh ×6, inspect-script-output/check.sh, check-substrate-updates apply.sh+check.sh ×7 | KEEP (rules stay inline; stub n/a) |
| §24 | pretooluse-clean-tree-before-branch.sh §6 | KEEP (thin cross-ref stays) |
| §25 | autonomous-mode-activation-template §81, inspect-script-output/SKILL.md §3, polling-cron-prompt-template §197 | KEEP rule inline (stub n/a); §25.5 KEEP (A3) |
| §27, §27.2 | inspect-script-output/check.sh §9/§176/§373, SKILL.md §3, **SPECIFICATION.md §27 (L616, L701) — top-level** | **§27 RELOCATE → stub preserves §27** (top-level; §27.2 named in prose for substrate citers) |
| §30 | handoff-author/SKILL.md §4 | **§30 RELOCATE → stub preserves §30** |
| §31 | **SPECIFICATION.md §31 (L535) — top-level** | **§31 RELOCATE → stub preserves §31** |
| §32 | ADA §185, (VERA/CATO via §32's own cross-refs) | **§32 RELOCATE → stub preserves §32** |

**Check result:** every op-disc §N cited from an active substrate file OR from SPECIFICATION.md resolves post-cut — KEEP sections keep their numbers (rule stays inline), top-level-only RELOCATE sections leave a numbered §-heading stub, and §7 (the only relocation with spec-cited SUBSECTIONS) leaves real subsection HEADING LINES so the exact-heading spec resolver still resolves §7.1/§7.2/§7.4/§7.5. The highest-risk citers are (a) RUNTIME scripts (`stop-self-check.sh`, `_hooklib.sh`, `pretooluse-*.sh`, `_save_verdict.py`) — these cite §N in COMMENTS/MESSAGES (human-orientation, not runtime path resolution; ARGUS WP2 CONCUR) and (b) the validate-spec MECHANICAL resolver against SPECIFICATION.md — these DO resolve by exact heading, handled by the rev2 r1 heading-preserve. (P-XREF + P-SPEC-XREF assert this.)

### 3.1.2 SPECIFICATION.md op-disc cite census (rev2 r1 — re-run live via spec_refs.py against ALL 13 rev1 relocated sections)

Ran `python substrate/skills/validate-spec/_lib/spec_refs.py --spec SPECIFICATION.md --repo-root .` against the LIVE source and filtered to op-disc refs that target a (rev1) relocated section. The COMPLETE result:

| op-disc anchor cited in SPECIFICATION.md | spec line(s) | current verdict | top-level or subsection? | rev2 disposition |
|---|---|---|---|---|
| §7 | 709 | PASS | top-level | §7 stub heading preserves it |
| **§7.1** | 244 | PASS | **subsection** | **§7 stub keeps `### 7.1` heading line (r1)** |
| **§7.2** | 252 | PASS | **subsection** | **§7 stub keeps `### 7.2` heading line (r1)** |
| **§7.4** | 67, 256, 370, 659 | PASS (×4) | **subsection** | **§7 stub keeps `### 7.4` heading line (r1)** |
| **§7.5** | 260 | PASS | **subsection** | **§7 stub keeps `### 7.5` heading line (r1)** |
| §11 | 280, 581 | PASS | top-level | §11 stub heading preserves it |
| §15 | 202 | PASS | top-level | §15 KEEP inline (r2) — heading stays live |
| §16 | 583 | PASS | top-level | §16 stub heading preserves it |
| §17 | 93 | PASS | top-level (Arc 29 §17 incidental) | §17 stub heading preserves it |
| §20 | 569 | PASS | top-level | §20 KEEP inline — heading stays live |
| §20.3 | 568 | PASS | subsection | §20.3 KEEP inline — heading stays live |
| §27 | 616, 701 | PASS | top-level | §27 stub heading preserves it |
| §31 | 535 | PASS | top-level | §31 stub heading preserves it |

**The complete at-risk set (would flip PASS→FAIL under rev1's prose-only stubs):** **§7.1 (L244), §7.2 (L252), §7.4 (L67/256/370/659), §7.5 (L260) = 7 PASS cites across 4 distinct subsection anchors, ALL §7 subsections.** This matches ARGUS's r1 finding exactly. **No OTHER relocated section has a spec-cited SUBSECTION** — §11/§16/§17/§27/§31 are cited only at top-level (preserved by the top-level §-heading stub rev1 already kept), and §14/§22/§29/§30/§32 have ZERO SPECIFICATION.md cites. §20/§20.3 are KEEP inline (safe). So r1's lossless fix is bounded to the §7 stub's subsection heading lines + the new P-SPEC-XREF probe.

**Pre-existing FAILs NOT in scope (not introduced by this cut):** the resolver also reports `§7.1.` (L129, trailing-period anchor) as FAIL today — that is a malformed cite in SPECIFICATION.md (the resolver builds a pattern for literal anchor `7.1.` which no heading matches) and FAILs against the LIVE source before this cut. It is a frozen-spec defect, not a cut regression; P-SPEC-XREF's assertion is "ZERO op-disc refs flip PASS→FAIL," which this pre-existing FAIL does not violate (it was already FAIL). (Noted as follow-up §9 — a one-character fix to SPECIFICATION.md L129 is a spec-edit, out of this arc's scope.)

### 3.2 CONDITIONAL relocations (→ disk module; slim-core residue = stub + `Read` pointer + recompose marker + relocation-index row) — 12 modules (rev2)

| Source (§ + live lines) | Class | New home | Slim-core residue |
|---|---|---|---|
| §7 (115–252) | CONDITIONAL | `modules/two-polybius-coordination.md` | §7 stub + **§7.1/§7.2/§7.3/§7.4/§7.5/§7.7 REAL HEADING LINES (r1)** + `<!-- MODULE-INLINE:two-polybius-coordination -->` + index row |
| §11 (478–726) | CONDITIONAL | `modules/autonomous-mode-setup.md` | §11 stub + `<!-- MODULE-INLINE:autonomous-mode-setup -->` + index row |
| §14 (820–833) | CONDITIONAL | `modules/sub-agent-transcript-discipline.md` | §14 stub + `<!-- MODULE-INLINE:sub-agent-transcript-discipline -->` + index row |
| §16 (920–961) | CONDITIONAL | `modules/bw-fit-matrix.md` | §16 stub + `<!-- MODULE-INLINE:bw-fit-matrix -->` + index row |
| §17 (962–1001) | CONDITIONAL | `modules/oss-dep-and-latency.md` | §17 stub + `<!-- MODULE-INLINE:oss-dep-and-latency -->` + index row |
| §20 detail (§20.1+§20.5+§20.6 within 1238–1338) | CONDITIONAL | `modules/credential-discipline-detail.md` | §20 keeps intro rule + §20.2 + §20.3 + §20.4 INLINE; a `<!-- MODULE-INLINE:credential-discipline-detail -->` marker placed AFTER §20.4 for the relocated detail + index row |
| §22 (1363–1424) | CONDITIONAL | `modules/bw-upgrade.md` | §22 stub (names §22.2 in prose) + `<!-- MODULE-INLINE:bw-upgrade -->` + index row |
| §27 (1627–1702) | CONDITIONAL | `modules/mechanical-inspection-split.md` | §27 stub (names §27.2 in prose) + `<!-- MODULE-INLINE:mechanical-inspection-split -->` + index row |
| §29 (1825–1906) | CONDITIONAL | `modules/multi-team-interop.md` | §29 stub + `<!-- MODULE-INLINE:multi-team-interop -->` + index row |
| §30 (1907–1972) | CONDITIONAL | `modules/four-layer-identity.md` | §30 stub + `<!-- MODULE-INLINE:four-layer-identity -->` + index row |
| §31 (1973–2043) | CONDITIONAL | `modules/substrate-component-design.md` | §31 stub + `<!-- MODULE-INLINE:substrate-component-design -->` + index row |
| §32 (2044–2090) | CONDITIONAL | `modules/jsdom-timing-discipline.md` | §32 stub + `<!-- MODULE-INLINE:jsdom-timing-discipline -->` + index row |

**12 CONDITIONAL chunks → 12 new module files.** (rev1's §15 → `verification-complexity.md` is REMOVED — §15 is KEEP-TIGHTEN per r2.)

**§22/§27 subsection note:** §22.2 and §27.2 are cited from substrate skills/check.sh (`check-bw-release/check.sh §161`, `inspect-script-output/check.sh §176`) but those are COMMENT/MESSAGE citations (not the validate-spec resolver), and §22.2/§27.2 are NOT cited from SPECIFICATION.md (census §3.1.2). So they do NOT require real heading lines for mechanical resolution — naming them in the stub prose (rev1's shape) is sufficient for the human/comment citers. Only §7's subsections need real heading lines (the spec resolver). This keeps the per-section stub minimal: §7 gets the heading-line treatment; §22/§27 keep prose-naming.

**§20 special case (partial-section relocation; rev2 r4 confirmed lossless):** §20 is the ONLY partial-section relocation (structural rule stays, detail moves). The marker pair is placed AFTER §20.4 (the last inline subsection). At subproject tier `credential-discipline-detail.md` re-inlines there — meaning the relocated §20.1 (canonical pattern diagram) physically follows §20.4 in the recomposed file, OUT of numeric order. **This is confirmed lossless (r4):** all §20 content is recoverable; the only external citers are §20 (SPECIFICATION.md L569, BARTLEBY §130) and §20.3 (SPECIFICATION.md L568, MAJOR_POLYBIUS), both of which stay inline at their numbers. The numbering-order wrinkle affects only the relocated Railway-specific DETAIL (§20.1/§20.5/§20.6), which has no external cross-ref. **rev2 disposition: leave as-is.** Placing the marker after §20.4 keeps the always-on structural core (§20-intro/§20.2/§20.3/§20.4) in clean numeric reading order, which is the priority for the universal credential rule; the conditional detail is correctly isolated at the section tail. ADA must NOT renumber §20.1→a higher number to "fix" the order — that would (a) be churn and (b) risk a future cross-ref drift. (P-RECOMPOSE asserts the §20 marker re-inlines a non-empty body; the order is cosmetic.)

### 3.3 PROVENANCE relocations — C-1 (already-in-bw; content-check then delete-to-Anchor)

All ticket ids below RESOLVE live (verified rev1 design phase, 24/24; ARGUS independently spot-checked 17/18 + stoa--ntn, all carry their stories). The slim core keeps the RULE + a one-line `Anchor: <bw-id>`. **The C-1 content-check gate (modules/README.md §5.2, carried into the build):** before ADA deletes ANY C-1 inline provenance prose, ADA runs `bw show <cited-id>` and content-checks the ticket carries the story. Per-deletion gate. VERA re-executes a sample (P-C1).

| Source (§ + live lines) | bw id(s) | Slim-core residue |
|---|---|---|
| §6.7 empirical (93) + §6.7.2 anchor (111) | `stoa--nax` | KEEP §6.7.1/§6.7.2 rules; `Anchor: stoa--nax` |
| §8.1 empirical (272) | 2026-05-04 in-prose | → §3.4 C-2 (no clean ticket) |
| §8.2 empirical (298) | 2026-05-05 in-prose | → §3.4 C-2 (no clean ticket) |
| §8.3 empirical (324) | `stoa--uc7` | KEEP §8.3 rule; `Anchor: stoa--uc7` |
| §8.4 empirical (348) | `stoa--14u` | KEEP §8.4 rule; `Anchor: stoa--14u` |
| §8.5 empirical (370) | `stoa--148` | KEEP §8.5 rule; `Anchor: stoa--148` |
| §9 historical window (400) + lineage (404) | `stoa--7kg`, `stoa--7kg.1` | KEEP §9 rules; `Anchor: stoa--7kg, stoa--7kg.1` |
| §10 progression provenance (470) | `stoa--ntn` | KEEP §10 rules; `Anchor: stoa--ntn` — **ARGUS WP4 confirmed stoa--ntn resolves + carries the progression table; C-1 (not C-2). Per-deletion `bw show` gate still runs at build (Step 2).** |
| §12 empirical (800) | `stoa--v2o` | KEEP §12 whole; `Anchor: stoa--v2o` |
| §13 empirical (814) | `stoa--a5q`, `ariadne--sh7` | KEEP §13 rule; `Anchor: stoa--a5q` (ariadne--sh7 cross-repo, fold into recovery note) |
| **§15 empirical (838)** | `stoa--tp1` | **rev2: §15 KEEP inline; `Anchor: stoa--tp1` STAYS IN THE SLIM CORE at §15 (was "moves with §15 into module" in rev1)** |
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

**Counting note (rev2):** PROVENANCE rows that "move WITH" a CONDITIONAL section now apply to §16/§17/§22/§27/§29/§30/§31 (**7 sections**, was 8 in rev1 — §15's anchor no longer moves; it stays in the slim core). They relocate inside their parent CONDITIONAL block as a compressed `Anchor:` line in the module; counted under the CONDITIONAL relocation, not separately. The standalone C-1 PROVENANCE chunks (compress-to-Anchor in the KEEP slim core) are now: §6.7, §8.3, §8.4, §8.5, §9, §10, §12, §13, **§15 (rev2 NEW standalone — was move-with in rev1)**, §18.7, §19.5, §19.6, §19.7, §20.7, §21, §23.4, §24, §25.6, §28.7 = **19 standalone C-1 chunks** (was 18; +1 because §15's Anchor is now standalone in the slim core).

### 3.4 C-2 archive-first cases — DEDICATED CHILD TICKETS (Arc-2 residual-2 precedent)

Provenance blocks with NO clean single bw home AND that become the only surviving copy once cut. Per the Arc-2 ARGUS adjudication: archive each to a DEDICATED CHILD TICKET (`bw create … --parent stoa--xyb.8 -d "<verbose prose>"`), NOT a bare `bw comment` (a titled child id is discoverable from the relocation-index Anchor; a buried comment is not). Mechanism confirmed live in Arc-2 (`bw create` supports `--parent` + `-d`).

| Source (§ + live lines) | What archives | Slim-core residue |
|---|---|---|
| §8.1 empirical (272) — 2026-05-04 bw-prime "NOT user-beadwork" leak | The verbose 2026-05-04 incident prose | C-2 child ticket; KEEP §8.1 rule + table; `Anchor: stoa--xyb.8.N` |
| §8.2 empirical (298) — 2026-05-05 ariadne team_test over-delegation | The verbose 2026-05-05 incident prose | C-2 child ticket; KEEP §8.2 rules; `Anchor: stoa--xyb.8.M` |
| §26 empirical (1623) — multi-instance HUMAN_paste-pliny-arc-* convergence | The filename-list ad-hoc precedent prose | C-2 child ticket; KEEP §26 cross-ref; `Anchor: stoa--xyb.8.P` |

**Per-deletion content-check gate (C-2 analogue):** ADA runs `bw create` FIRST, then `bw show <child-id>` to confirm the description carries the verbose prose, THEN deletes inline. Archive-FIRST, content-CHECK, THEN delete. (P-C2 asserts the child tickets exist + carry the prose + the Anchor cite matches the assigned id.)

**3 firm C-2 chunks** (§8.1, §8.2, §26). (rev1's conditional 4th — §10 if stoa--ntn fails — is RESOLVED: ARGUS WP4 confirmed stoa--ntn resolves + carries the progression table, so §10 is C-1, not C-2. The build Step-2 `bw show stoa--ntn` per-deletion gate still runs as a belt-and-suspenders check, but no C-2 fallback is expected.)

### 3.5 DUPLICATE relocations (→ pointer)

| Source | Class | Keep-home | Slim-core residue |
|---|---|---|---|
| (none in op-disc) | — | — | — |

**op-disc has ZERO DUPLICATE relocations.** op-disc §12 is the DUPLICATE *keep-home* for the rest of the substrate (MAJOR_POLYBIUS §7.3 and MAJOR_PLINY §6.1 already point AT op-disc §12 — that consolidation happened in Arc 2 / earlier). The keep-home stays inline whole; nothing in op-disc duplicates content found elsewhere. (Confirmed: op-disc §12 self-declares "Role files reference this section; do not duplicate" at 729.) **0 DUPLICATE chunks.**

### 3.6 SPLIT per-line enumeration (cross-ref subsections — deterministic, no ADA guessing)

The "Cross-references" subsections at the tail of KEEP sections mix LIVE in-file/sibling-file/skill/tool pointers (stay inline) with PROVENANCE bw-id/empirical lines (fold into the section's `Anchor:`). The rule (Arc-2 §3.8): **keep every line that points at a §/file/skill/tool a reader follows to OPERATIONAL content; fold every line that says "exists because <ticket/date>" or "source-of-truth is <ticket/doc>" into the section's Anchor.** Sections whose body relocates whole (§22/§27/§29/§30/§31) carry their cross-refs INTO the module — no SPLIT needed there. SPLIT applies only to the cross-ref tails of KEEP sections.

The KEEP sections with cross-ref tails to SPLIT: **§19.6.3 (1154–1162), §19.7.6 (1227–1234), §23.5 (1472–1480), §25.7 (1597–1604), §28.8 (1811–1821).** For each, the deterministic call:

- **§19.6.3 (1156–1162):** §19.1/§19.2 (in-file LIVE — keep); MAJOR_PLINY §7.2 + MAJOR_POLYBIUS §4.3 (sibling LIVE — keep); MAJOR_PLINY §5.10 (sibling LIVE — keep); §6.7.1 (in-file LIVE — keep); §19.7 (in-file LIVE — keep); the "Empirical anchor: Arc 30 PLINY init-handshake…" line (1162) (PROVENANCE — fold into §19.6 Anchor).
- **§19.7.6 (1229–1234):** §19.6 + §19.1–§19.5 (in-file LIVE — keep); MAJOR_PLINY §6.2 + MAJOR_POLYBIUS §16 (sibling LIVE — keep); §28 (in-file LIVE — keep); the "Empirical anchor: 2026-05-13 PLINY-stoa Engagement B (stoa--53u)" line (1234) (PROVENANCE — fold into §19.7 Anchor).
- **§23.5 (1474–1480):** MAJOR_POLYBIUS §17 (sibling LIVE — keep); §6.7.1/§8.1/§8.2 (in-file LIVE — keep); install.sh/check.sh/apply.sh (tooling LIVE — keep); MAJOR_POLYBIUS §19 (sibling LIVE — keep); the "stoa--ads (this arc); forthcoming railway_stoa custom team arc" line (1479) (PROVENANCE — fold into §23 Anchor).
- **§25.7 (1599–1604):** §10/§11 (in-file LIVE — keep); §6.7.1 (in-file LIVE — keep); §8.1 (in-file LIVE — keep); DAEDALUS §6.7/ADA §5.8/VERA §5.10 (sibling LIVE — keep); the two template hooks (LIVE — keep); the "stoa--dxw (Arc 26 anchor); stoa--501; retro §7" line (1604) (PROVENANCE — fold into §25 Anchor).
- **§28.8 (1813–1821):** global CLAUDE.md (LIVE — keep); MAJOR_PLINY §5.12 + CAPTAIN_ADA §5.5 (sibling LIVE — keep); §19.6/§25 (in-file LIVE — keep); MAJOR_POLYBIUS §18 (sibling LIVE — keep); MAJOR_PLINY §5.10/§5.11 (sibling LIVE — keep); the "stoa--kjo; 2026-05-04 ariadne--xft.4" lines (1820–1821) (PROVENANCE — fold into §28 Anchor).

**5 SPLIT cross-ref tails** (all on KEEP sections; LIVE pointers stay verbatim, the trailing empirical-anchor/ticket lines fold into the section's existing Anchor). P-SPLIT greps the LIVE pointer text (drift-resistant) + asserts the folded bw-ids appear in the §N Anchor, not orphaned as a standalone cross-ref bullet. (Note: §15 is now KEEP but its tail is §15.7 self-referential observation + the empirical Anchor — folded into §15's `Anchor: stoa--tp1`; §15 has no separate "Cross-references" subsection requiring a SPLIT row, so the 5-tail count is unchanged.)

### 3.7 KEEP-TIGHTEN (stays inline; listed for audit completeness) — rev2 adds §15

§1–§6 (anti-pattern thesis + redundancy + §6.7 rules), §8.1/§8.2 (+ §8.3/§8.4/§8.5 per A2), §9 rules, §10 WHOLE, §12 WHOLE (DUPLICATE keep-home), §13, **§15 (rev2 NEW KEEP per r2 — heading + §15.1–§15.5 + §15.7 stay; §15.6 worked examples compressed; empirical → Anchor stoa--tp1)**, §18 rules (§18.1–§18.5), §19.1–§19.4 + §19.6 rule + §19.7 rule, §20 structural core (intro + §20.2 + §20.3 + §20.4), §21, §23 rules (§23.1–§23.3), §24 (thin cross-ref), §25 rules (§25.1–§25.4 + §25.5 per A3), §26 (thin cross-ref), §28 rules (§28.1–§28.6), §33 WHOLE, §34 WHOLE. Plus the thesis preamble (1–33).

### 3.8 Module-OWNERSHIP record (for the install.sh partition — §6.4) — rev2: 12 op-disc modules

| Owner role file | Owned modules (basenames) |
|---|---|
| `MAJOR_POLYBIUS.md` (Arc 2) | `onboarding`, `sub-project-spawning`, `pair-programmer-authoring`, `pair-programming-prototyping`, `substrate-update-check` |
| `operating-disciplines.md` (THIS arc) | `two-polybius-coordination`, `autonomous-mode-setup`, `sub-agent-transcript-discipline`, `bw-fit-matrix`, `oss-dep-and-latency`, `credential-discipline-detail`, `bw-upgrade`, `mechanical-inspection-split`, `multi-team-interop`, `four-layer-identity`, `substrate-component-design`, `jsdom-timing-discipline` |
| (`README.md` — owned by nobody; excluded from every owner-set) | — |

**op-disc owns 12 modules** (rev1 had 13; `verification-complexity` removed per r2). This is the data the partitioned `recompose_module_inline()` consumes (§6.4) — the per-call OWNED set for Checks B/D. The GLOBAL EXISTENCE set for Check A is the full `substrate/modules/*.md` glob (5 POLYBIUS + 12 op-disc = 17 modules, minus README), owner-agnostic.

### 3.9 Ledger summary (chunk counts per class — self-consistent) — rev2

- **CONDITIONAL:** 12 relocations (§7, §11, §14, §16, §17, §20-detail, §22, §27, §29, §30, §31, §32) → **12 new module files. = 12 CONDITIONAL chunks.** (rev1: 13; §15 removed.)
- **PROVENANCE:** **19 standalone C-1** (§6.7, §8.3, §8.4, §8.5, §9, §10, §12, §13, §15, §18.7, §19.5, §19.6, §19.7, §20.7, §21, §23.4, §24, §25.6, §28.7) + **3 firm C-2** (§8.1, §8.2, §26 → child tickets) + **5 SPLIT** cross-ref tails (§19.6.3, §19.7.6, §23.5, §25.7, §28.8) = **27 PROVENANCE chunks.** (19 + 3 + 5 = 27; rev1 was 26 — +1 because §15's Anchor is now standalone-in-slim-core rather than move-with.) Plus 7 "move-with-CONDITIONAL" provenance Anchors (§16/§17/§22/§27/§29/§30/§31) counted under their parent CONDITIONAL relocation, not separately (rev1 had 8 — §15 dropped).
- **DUPLICATE:** **0 chunks** (op-disc §12 is the keep-home for the rest of the substrate; nothing in op-disc duplicates elsewhere).
- **KEEP-TIGHTEN:** ~21 sections stay inline (listed §3.7; rev1 was ~20, +§15).

**Total relocated chunks: 12 CONDITIONAL + 27 PROVENANCE + 0 DUPLICATE = 39 relocated chunks**, each with a lossless home + recovery path. (Same total as rev1; §15 moved from CONDITIONAL-relocate to KEEP-with-standalone-Anchor — net one CONDITIONAL down, one standalone-PROVENANCE up.)

### 3.10 Empirical post-cut floor ESTIMATE (reported, not targeted — per recalibrated criterion) — rev2: slightly higher

The big movers: 12 CONDITIONAL relocations move ~970 source lines off-disk (§7≈138 + §11≈249 + §14≈14 + §16≈42 + §17≈40 + §20-detail≈55 + §22≈62 + §27≈76 + §29≈82 + §30≈66 + §31≈71 + §32≈47). **§15 (≈84 source lines) NO LONGER relocates** (rev2 r2) — it stays inline tightened to ~55–65 lines (compress §15.6 worked examples; fold empirical to Anchor), so the slim core carries ~55–65 MORE lines than the rev1 estimate. The 19 C-1 + 3 C-2 provenance compressions turn ~260 verbose lines into ~26 Anchor lines (net ~234 saved). The KEEP-TIGHTEN prose-tightening saves a further ~50–100. Against 2156, the slim core lands an **estimated empirical floor in the ~760–915 line band** (rev1 estimated ~700–850; +~60 for §15 staying inline). Every line is always-on universal core (the anti-pattern thesis, escalation triggers, the heartbeat/confabulation/credential/PRINCIPAL-gate/base-vs-custom/Co-Authored-By/verification-complexity rules, the bw cookbook keep-home, the composition + trigger-payload thin rules, the relocation index). **This is an ESTIMATE; the build REPORTS the actual floor (P-FLOOR).** Do NOT cut a KEEP rule to push the floor lower — the floor is whatever the always-on core weighs (recalibrated criterion). A landing materially above ~1000 means a KEEP section's prose is still verbose (tighten); a landing below ~650 is suspicious (check for a dropped always-on rule — P-FLOOR falsifier guard).

---

## §4 — Verification probes (what would falsify the design's intended behavior)

Concrete probes VERA re-executes. The probe spec is load-bearing. Run all from the worktree root. **rev2 changes: P-COND/P-STUB/P-INDEX drop `verification-complexity` (12 modules); P-XREF extended; new P-SPEC-XREF for r1; P-KEEP adds a §15 inline assertion.**

### P-FLOOR — empirical floor reported + sanity band
```bash
wc -l substrate/operating-disciplines.md
```
**Pass:** the floor is REPORTED; sanity band ~760–915 (rev2 estimate). **Falsifies if:** > 1100 (cut too shallow) or < 650 (suspiciously aggressive — check for a dropped always-on KEEP rule). A 915–1100 landing is partial-not-failure (KEEP rules are dense always-on core; §15 now inline). Also run op-disc §33's per-module line-count discipline against each of the 12 new modules (no module is itself a re-bloat monolith — `autonomous-mode-setup.md` at ~249 lines is the largest and is acceptable: one coherent procedure).

### P-COND — every CONDITIONAL section has a real module home (12 modules)
```bash
for m in two-polybius-coordination autonomous-mode-setup sub-agent-transcript-discipline \
         bw-fit-matrix oss-dep-and-latency credential-discipline-detail \
         bw-upgrade mechanical-inspection-split multi-team-interop four-layer-identity \
         substrate-component-design jsdom-timing-discipline; do
  test -s "substrate/modules/$m.md" && echo "OK $m" || echo "MISSING $m"
done
# rev2 NEGATIVE assertion: verification-complexity.md must NOT exist (§15 is KEEP, not relocated):
test -e substrate/modules/verification-complexity.md && echo "FAIL §15 wrongly relocated" || echo "OK §15 not relocated"
```
**Pass:** all 12 module files exist non-empty AND `verification-complexity.md` does NOT exist (§15 stays inline). **Falsifies if:** any of the 12 missing/empty (LOST CANON), OR `verification-complexity.md` exists (§15 wrongly relocated — contradicts r2).

### P-STUB — every relocated section leaves a stub at its original number (12 sections; §15 NOT a stub)
```bash
grep -nE '^## (7|11|14|16|17|20|22|27|29|30|31|32)\. ' substrate/operating-disciplines.md
# rev2: §15 must be a LIVE section (KEEP), not a stub — assert it has its subsection content:
grep -nE '^### 15\.1 ' substrate/operating-disciplines.md && echo "OK §15 live (KEEP)" || echo "FAIL §15 missing/stubbed"
```
**Pass:** §7, §11, §14, §16, §17, §20, §22, §27, §29, §30, §31, §32 headings present (stubs) AND §15.1 heading present (live KEEP). **Falsifies if:** any relocated section number GONE, OR §15 reduced to a stub (would contradict r2 KEEP).

### P-XREF — every op-disc §N cited from an active SUBSTRATE file resolves post-cut
```bash
grep -rhoE 'operating-disciplines\.md §[0-9]+(\.[0-9]+)*' substrate/ \
  --include='*.md' --include='*.sh' --include='*.py' \
  | grep -vE 'substrate/arcs/' | sort -u
for n in 6 7 8 9 10 11 12 13 15 16 17 18 19 20 22 23 24 25 27 30 31 32; do
  grep -qE "^## ${n}\. " substrate/operating-disciplines.md && echo "OK §$n" || echo "MISSING §$n"
done
```
**Pass:** every cited top-level §N resolves to a heading. Cited SUBSECTIONS (§7.2, §15.4, §22.2, §27.2) resolve either to a live subsection (KEEP: §15.4) or to a real heading line in the stub (§7.x — rev2 r1) or are named in parent stub prose (§22.2, §27.2 — substrate/comment citers only). **Falsifies if:** any cited §N has no heading, OR a spec-cited subsection (§7.x) is not a real heading line (caught more precisely by P-SPEC-XREF).

### P-SPEC-XREF — SPECIFICATION.md op-disc refs do NOT regress (rev2 r1 — THE blocking-finding probe)
```bash
# Run the SHIPPED validate-spec resolver against SPECIFICATION.md (the surface rev1 missed).
# Confirm the invocation first (verified this design phase):
python substrate/skills/validate-spec/_lib/spec_refs.py --spec SPECIFICATION.md --repo-root . \
  > /tmp/spec_refs_postcut.jsonl 2>&1
# Assert: NO op-disc ref that PASSes on the PRE-cut source FAILs on the POST-cut source.
# The at-risk set (census §3.1.2): §7.1 (spec L244), §7.2 (L252), §7.4 (L67/256/370/659), §7.5 (L260).
python3 - <<'PY'
import json
atrisk = {('7.1',244),('7.2',252),('7.4',67),('7.4',256),('7.4',370),('7.4',659),('7.5',260)}
seen=set(); fails=[]
for line in open('/tmp/spec_refs_postcut.jsonl'):
    line=line.strip()
    if not line: continue
    try: r=json.loads(line)
    except: continue
    if r.get('summary'): continue
    tf=r.get('target_file_resolved') or ''
    if 'operating-disciplines' not in tf: continue
    a=r.get('anchor',''); ln=r.get('citing_line_in_spec')
    if (a,ln) in atrisk:
        seen.add((a,ln))
        if r.get('verdict')!='PASS': fails.append((a,ln,r.get('verdict')))
missing = atrisk - seen
print("AT-RISK SEEN:", sorted(seen))
print("AT-RISK FLIPPED-TO-FAIL:", fails)
print("AT-RISK NOT-FOUND (parser drift):", sorted(missing))
print("RESULT:", "PASS" if (not fails and not missing) else "FAIL")
PY
```
**Pass:** all 7 at-risk §7.x refs (§7.1/§7.2/§7.4×4/§7.5) still resolve PASS post-cut (the §7 stub's real heading lines resolve them) AND none is missing from the resolver output. **Falsifies if:** any at-risk ref FAILs (the §7 stub did not preserve that subsection heading line — the exact rev1 BLOCKING regression) OR an at-risk ref is absent from output (the §7 stub heading shape doesn't match the resolver's `_heading_pattern`; ADA used a non-matching shape — verify against the §2.7.1 literal). Note: the pre-existing `§7.1.` FAIL at L129 is NOT in the at-risk set (it FAILs pre- and post-cut; not a regression).

### P-C1 — C-1 content-check gate honored (LOST-CANON proof — sampled; rev2 adds stoa--tp1 for §15)
```bash
for id in stoa--nax stoa--7kg stoa--p5g stoa--ads stoa--dxw stoa--kjo stoa--53u stoa--ezj stoa--tp1 stoa--ntn stoa--32b.3; do
  echo "=== $id ==="; bw show "$id" 2>&1 | head -30; done
```
**Pass:** each cited ticket's body materially carries the N=1 story the deleted inline prose held. **stoa--ntn** (the §10 progression cite) resolves AND carries the progression story (ARGUS WP4 confirmed; re-verify). **stoa--tp1** (the §15 empirical, now standalone in the slim core) resolves + carries the verification-complexity empirical. **Falsifies if:** any cited ticket is a thin stub not carrying the deleted detail → that deletion dropped canon, classification should have been C-2.

### P-C2 — C-2 archive-first executed BEFORE deletion, in DEDICATED CHILD TICKETS (3 firm; rev2: §10 not C-2)
```bash
bw list --all 2>&1 | grep -E 'xyb\.8\.[0-9]'
bw show <child-id-for-§8.1> 2>&1 | grep -iE 'bw.prime|user-beadwork|2026-05-04|leak'
bw show <child-id-for-§8.2> 2>&1 | grep -iE 'team_test|over-delegation|2026-05-05'
bw show <child-id-for-§26> 2>&1 | grep -iE 'HUMAN_paste|cron.hygiene|preamble'
grep -nE 'stoa--xyb\.8\.[0-9]' substrate/operating-disciplines.md
```
**Pass:** the 3 firm C-2 child tickets exist (parent = stoa--xyb.8), each description carries its verbose provenance, and the slim core's Anchor cites the correct child id. **Falsifies if:** a C-2 verbose block is gone from source AND not present in a child-ticket description (LOST CANON), OR a cite-back id does not match the created ticket. (§10 is NOT a C-2 row — stoa--ntn carries it; if the build's `bw show stoa--ntn` belt-check fails, §10 routes to a 4th C-2 child, but ARGUS WP4 makes that unexpected.)

### P-SPLIT — SPLIT LIVE cross-refs preserved inline; PROVENANCE folded into Anchors
```bash
grep -nE 'MAJOR_PLINY\.md §7\.2|MAJOR_POLYBIUS\.md §4\.3|MAJOR_PLINY\.md §5\.10|DAEDALUS\.md §6\.7|CAPTAIN_ADA\.md §5\.5' substrate/operating-disciplines.md
grep -nE 'Anchor.*stoa--53u' substrate/operating-disciplines.md   # §19.7 fold
grep -nE 'Anchor.*stoa--dxw.*stoa--501' substrate/operating-disciplines.md   # §25 fold
grep -nE 'Anchor.*stoa--kjo' substrate/operating-disciplines.md   # §28 fold
```
**Pass:** every §3.6 LIVE pointer resolves in the slim core; the PROVENANCE bw-ids appear in the §N Anchor lines (folded). **Falsifies if:** any §3.6 LIVE pointer is missing, OR a PROVENANCE bw-id is still a standalone cross-ref bullet.

### P-INDEX — the relocation index exists, is always-loaded core, covers every relocation (12 modules)
```bash
grep -nE '^## 0\.5 |Relocation index' substrate/operating-disciplines.md   # the §0.5 index exists, before §1
for m in two-polybius-coordination autonomous-mode-setup credential-discipline-detail \
         bw-upgrade mechanical-inspection-split multi-team-interop four-layer-identity substrate-component-design jsdom-timing-discipline; do
  grep -q "$m" substrate/operating-disciplines.md && echo "OK index-or-stub: $m" || echo "MISSING: $m"
done
grep -c 'Routing map' substrate/operating-disciplines.md   # expect 0 — op-disc is not an orchestrator
```
**Pass:** §0.5 relocation index present before §1; every CONDITIONAL module appears in an index row; NO routing map present (returns 0). **Falsifies if:** index absent, a relocation has no index row, OR a routing map was added (wrong shape — assumption 1 / Q1).

### P-RECOMPOSE — subproject recompose completeness for op-disc (THE LOST-CANON-at-subproject probe, whole-team)
Run on a THROWAWAY subproject deploy (per op-disc §25.5: synthetic parent under a tmp path or `git clone --no-local`; do NOT mutate any operator-owned workspace):
```bash
TMP=$(mktemp -d); mkdir -p "$TMP/myproj"
bash substrate/install.sh --target subproject --parent-dir "$TMP" --subproject myproj
RECOMPOSED="$TMP/myproj/.claude/operating-disciplines.md"

# (a) The 12 op-disc PAIRED markers SURVIVE, each enclosing a NON-EMPTY body:
grep -cE '^<!-- MODULE-INLINE:' "$RECOMPOSED"     # expect 12 op-disc opens
grep -cE '^<!-- /MODULE-INLINE:' "$RECOMPOSED"    # expect 12 op-disc closes
grep -Pzo '(?m)^<!-- MODULE-INLINE:[^\n]*-->\n<!-- /MODULE-INLINE:' "$RECOMPOSED" && echo "FAIL empty pair" || echo "OK no empty pairs"

# (b) EVERY op-disc module body is present (assert each module's first-heading line appears):
for m in two-polybius-coordination autonomous-mode-setup sub-agent-transcript-discipline \
         bw-fit-matrix oss-dep-and-latency credential-discipline-detail \
         bw-upgrade mechanical-inspection-split multi-team-interop four-layer-identity \
         substrate-component-design jsdom-timing-discipline; do
  head1=$(head -1 "substrate/modules/$m.md")
  grep -Fq "$head1" "$RECOMPOSED" && echo "OK body present: $m" || echo "MISSING body: $m"
done

# (c) recomposed subproject op-disc is canon-equivalent to full content (NOT the slim band):
wc -l "$RECOMPOSED"   # expect ~1700+ (the 12 bodies re-inlined), NOT the ~760-915 slim band

# (d) POLYBIUS recompose STILL passes (the partition fix did not break Arc-2):
RECOMPOSED_POLY="$TMP/myproj/.claude/MAJOR_POLYBIUS_myproj.md"
grep -cE '^<!-- MODULE-INLINE:' "$RECOMPOSED_POLY"   # expect 5 (the Arc-2 POLYBIUS markers, intact)
```
**Pass:** (a) all 12 op-disc paired markers survive + NO empty pair; (b) all 12 op-disc module first-heading lines appear; (c) recomposed op-disc in the FULL band (~1700+); (d) POLYBIUS recompose still inlines its 5 modules. **Falsifies if:** any op-disc marker pair empty (body dropped → LOST CANON at subproject tier), OR < 12 op-disc markers survive, OR any op-disc body absent, OR recomposed op-disc still in the slim band (recompose silently no-op'd — catastrophic), OR POLYBIUS recompose broke (partition regression).

### P-RECOMPOSE-NEG — FAIL-LOUD asserted (whole-team losslessness depends on the err() firing)
```bash
mv substrate/modules/autonomous-mode-setup.md substrate/modules/autonomous-mode-setup.md.bak
bash substrate/install.sh --target subproject --parent-dir "$TMP" --subproject myproj2; echo "exit=$?"
mv substrate/modules/autonomous-mode-setup.md.bak substrate/modules/autonomous-mode-setup.md
```
**Pass:** install.sh exits NON-ZERO with a clear Check-A `marker MODULE-INLINE:autonomous-mode-setup has no module source` error AND does NOT write a partial/slim op-disc to the subproject. **Falsifies if:** exit 0 (silent partial deploy — the LOST-CANON-at-subproject failure). **rev2 r3 NOTE:** because Check A now tests the GLOBAL existence set, this fires correctly regardless of which owner's recompose call hits the missing module first.

### P-OWNERSHIP — the module-ownership partition is correct (Check B does NOT false-positive cross-owner)
```bash
bash substrate/install.sh --target subproject --parent-dir "$TMP" --subproject myproj3; echo "exit=$?"
```
**Pass:** exit 0 — POLYBIUS recompose scoped to its 5-module OWNED set passes (does not trip Check B on op-disc's 12 modules); op-disc recompose scoped to its 12-module OWNED set passes (does not trip Check B on POLYBIUS's 5). **Falsifies if:** exit 2 with a Check-B `module X.md exists but no MODULE-INLINE:X marker` error — the owned-set partition was not applied and the global-glob false-positive fired (the exact regression §2.7.2 names).

### P-OWNERSHIP-CHECKA — Check A still global after the two-set split (rev2 r3 — the new precision probe)
```bash
# Verify Check A's existence guarantee did NOT narrow to the owned set: introduce a marker in a role
# file for a module that exists but is NOT in that file's OWNED set, on a throwaway copy. Check A must
# still find the module source (global existence), NOT fail it as "no module source".
# Mechanically: confirm the awk receives a GLOBAL list distinct from the owned list (static check):
grep -nE 'recompose_module_inline\(\)|_module_basenames|_global_basenames|module_list|global_list' substrate/install.sh | head -20
grep -nE 'name in exists|name in global' substrate/install.sh   # Check A must test the GLOBAL set
```
**Pass:** install.sh's `recompose_module_inline()` passes the awk TWO distinct lists (global-existence + owned), and Check A's `name in <global-set>` tests the global one while Checks B/D iterate/count the owned one (§6.4). **Falsifies if:** Check A tests the owned set (the rev1 single-array bug — Check A's "marker → real module source" guarantee silently narrowed to "marker → OWNED module").

### P-AUTH — no author-field regression (CLAUDE.md authorship discipline)
```bash
grep -niE '^(author|owner|creator|by|copyright|maintainer):' substrate/operating-disciplines.md substrate/modules/*.md
```
**Pass:** no author-like field names anyone other than Denson Smith (op-disc carries none; the 12 new modules carry none). **Falsifies if:** any new module's provenance header introduces an author field.

### P-KEEP — the always-on KEEP rules are still inline (whole-team availability-losslessness; rev2 adds §15)
```bash
grep -qE 'redundancy IS the safety property' substrate/operating-disciplines.md && echo "OK §6 redundancy" || echo "DROPPED §6"
grep -qE 'Universal escalation triggers' substrate/operating-disciplines.md && echo "OK §10 escalation" || echo "DROPPED §10 triggers"
grep -qiE 'agents NEVER hold credentials|five rejected anti-patterns' substrate/operating-disciplines.md && echo "OK §20 credential core" || echo "DROPPED §20 core"
grep -qiE 'BLOCK, not a TAG' substrate/operating-disciplines.md && echo "OK §25 PRINCIPAL-gate" || echo "DROPPED §25 rule"
grep -qiE 'uncertain, checking' substrate/operating-disciplines.md && echo "OK §19 confabulation" || echo "DROPPED §19 rule"
grep -qE 'Co-Authored-By: CAPTAIN' substrate/operating-disciplines.md && echo "OK §28 trailer format" || echo "DROPPED §28"
grep -qiE 'bw cookbook|comment text is positional|`-m` does NOT exist' substrate/operating-disciplines.md && echo "OK §12 cookbook keep-home" || echo "DROPPED §12"
# rev2 r2: §15 verification-complexity must stay inline (read-direct by VERA/CATO/ZENO/ARGUS):
grep -qiE 'verification.complexity|the 2x2|two new verdict shapes' substrate/operating-disciplines.md && echo "OK §15 inline (r2)" || echo "DROPPED §15"
```
**Pass:** all always-on KEEP rules resolve inline, INCLUDING §15 (rev2 r2). **Falsifies if:** any always-on rule was relocated off-disk (whole-team availability-losslessness violated), OR §15 is gone (contradicts r2 — verifier seats read it direct).

---

## §5 — Build steps (for ADA — ordered; the cut sequence) — rev2: 12 modules; §15 KEEP; two-set recompose

**Step 0 (process hazard — DO THIS FIRST).** Confirm cwd is the worktree (`git -C C:/Users/denso/claude_projects/the-stoa/.claude/worktrees/arc-47-build rev-parse --show-toplevel` resolves to the worktree, branch `arc-47/build`). Use ABSOLUTE worktree paths for EVERY Write. After each write, verify it landed in the worktree (`git -C <worktree> status`) and NOT in main (`git -C C:/Users/denso/claude_projects/the-stoa status` should NOT show your edit). The Write-resolves-against-main-root hazard hit prior arcs; this gate catches it before it compounds.

1. **Create the 12 module files** (`substrate/modules/*.md`), populating from the live source line-ranges in §2.3 / §3.2. Each module: stable `# <Title>` first line (P-RECOMPOSE keys on it) → provenance header (cites this design + stoa--xyb epic) → relocated content verbatim-tightened, INCLUDING the section's own cross-refs + the compressed `Anchor:` for any move-with provenance (§3.3). Run op-disc §33 per-module line-count discipline. NO author field (P-AUTH). **Do NOT create `verification-complexity.md` (§15 is KEEP — r2).**
2. **Execute C-2 archive-first as DEDICATED CHILD TICKETS** (§3.4): `bw create "Arc 47 C-2 archive: §8.1 bw-prime leak provenance (2026-05-04)" --parent stoa--xyb.8 -d "<verbose prose>"` + §8.2 + §26, BEFORE touching the source. Record assigned child ids. `bw show <child-id>` content-check each. Write the slim-core Anchor cite-backs using the ACTUAL ids. **Also `bw show stoa--ntn`** (belt-check; ARGUS WP4 confirms it carries the §10 progression story → C-1, Anchor cite; the 4th C-2 child is NOT expected).
3. **Cut the slim core** (`substrate/operating-disciplines.md`):
   - Add **§0.5 relocation index** immediately after the thesis, BEFORE §1. Populate from §3.2 + §3.4. NO routing map (P-INDEX asserts this).
   - For the 11 top-level-only CONDITIONAL sections (§11/§14/§16/§17/§22/§27/§29/§30/§31/§32 + §20-detail), replace the body with the stub + paired `<!-- MODULE-INLINE:<name> -->` … `<!-- /MODULE-INLINE:<name> -->` marker (§2.7.1 first literal). For §20, place the marker AFTER §20.4 (partial-section case; do NOT renumber §20.1 — r4).
   - **For §7 (the ONLY section with spec-cited subsections — r1):** use the §2.7.1 SECOND literal — the §7 stub keeps `### 7.1`/`### 7.2`/`### 7.3`/`### 7.4`/`### 7.5`/`### 7.7` as REAL HEADING LINES (each with a one-line "Relocated → module §7.x" pointer), markers at the END. This keeps the exact-heading spec resolver GREEN (P-SPEC-XREF).
   - **§15 STAYS INLINE (r2):** do NOT stub it. Tighten only — compress §15.6 six worked examples to the 2–3 load-bearing ones (rest → "see Anchor for full set"); fold §15's empirical to `Anchor: stoa--tp1`. Keep §15.1–§15.5 + §15.7 + the cited §15.4 heading live.
   - For each standalone C-1 PROVENANCE row (§3.3 — 19 rows incl §15's Anchor), run the `bw show` content-check (gate) THEN delete-to-Anchor.
   - For each SPLIT cross-ref tail (§3.6 — 5 tails), keep LIVE pointers inline verbatim, fold the trailing empirical/ticket lines into the §N Anchor.
   - Tighten KEEP-TIGHTEN prose (§3.7) — do NOT relocate any KEEP rule (P-KEEP). §12 stays whole (DUPLICATE keep-home). §10/§15/§33/§34 stay whole-or-tightened-inline.
4. **Add the install.sh module-OWNERSHIP partition + op-disc recompose call** (§6 — substrate-tooling source, gauntlet-gated, correctly inside this arc):
   - Refactor `recompose_module_inline()` to take a SECOND arg (the owned-module-set) AND pass the awk TWO `-v` lists: a GLOBAL-existence list (the full `substrate/modules/*.md` glob minus README — for Check A) and the OWNED list (the per-call arg — for Checks B/D). Check A tests `name in <global>`; Checks B/D iterate/count `<owned>`. (§6.4 exact signature — r3.)
   - Call `recompose_module_inline "$DEST_POLYBIUS" "$POLYBIUS_MODULES"` (the 5-module owned-set) AND `recompose_module_inline "$DEST_OPERATING_DISCIPLINES" "$OPDISC_MODULES"` (the 12-module owned-set). The op-disc call goes AFTER op-disc is `cp`'d, inside the `if [ "$TARGET" = "subproject" ]` block (§6.5).
   - Smoke-test against a throwaway synthetic parent (P-RECOMPOSE + P-RECOMPOSE-NEG + P-OWNERSHIP + P-OWNERSHIP-CHECKA) before considering the step done.
5. **Cross-ref re-point sweep** (verification, not churn — numbers preserved): `grep -rn 'operating-disciplines' substrate/ | grep -oE '§[0-9.]+'` cross-checked against the slim core's headings (P-XREF). **AND run P-SPEC-XREF** (the validate-spec resolver against SPECIFICATION.md — r1). Confirm every active-file cite + every SPECIFICATION.md op-disc cite still resolves to a real anchor (stub or live).
6. **Run all probes** (P-FLOOR, P-COND, P-STUB, P-XREF, P-SPEC-XREF, P-C1, P-C2, P-SPLIT, P-INDEX, P-RECOMPOSE, P-RECOMPOSE-NEG, P-OWNERSHIP, P-OWNERSHIP-CHECKA, P-AUTH, P-KEEP) as a self-check before returning to PLINY.
7. **Commit** with `Co-Authored-By: CAPTAIN_ADA_the-stoa <captain-ada@the-stoa.local>` per op-disc §28. (The slim-core cut + the 12 modules + the install.sh partition land as one coherent commit, or the install.sh partition as a trailing commit if ADA prefers a clean tooling/canon split — ADA's call; both are this arc.)

---

## §6 — install.sh module-OWNERSHIP partition + op-disc recompose (the load-bearing tooling extension)

### 6.1 Why op-disc recompose is required (whole-team losslessness at subproject tier)

op-disc deploys at all 3 tiers (L964–980, `cp`). At subproject tier `DEST_MODULES_DIR=""` (no modules deployed) AND a subproject seat's `Read .claude/modules/X.md` does not resolve reliably (the Arc-2 probe finding). So a slim subproject `operating-disciplines.md` pointing at 12 modules absent from the subproject's `.claude/` would break losslessness at that tier FOR EVERY SEAT (op-disc is universal). The fix is the same as POLYBIUS: recompose-inline the 12 module bodies at their markers at subproject tier. The mechanism (`recompose_module_inline()`, the awk state-machine, the 5 FAIL-LOUD checks A–E, idempotency) ALREADY EXISTS (Arc-2, install.sh L871–957) and is data-driven — this arc REUSES it, with the two-set signature change (§6.4, r3).

### 6.2 op-disc is `cp`'d, not `sed`'d — recompose runs cleanly on it

POLYBIUS/PLINY get a `sed` substitution ({{NAME_SUFFIX}}/{{USER_TIER_DIR}}); op-disc gets a plain `cp` (L978, no template slots). The recompose runs IN PLACE on the deployed file regardless of how it was written. The op-disc recompose call goes AFTER the `cp` at L978, inside the `if [ "$TARGET" = "subproject" ]` block. (The existing POLYBIUS recompose block is L870–962, BEFORE the op-disc `cp` at L964–980. ADA either (a) moves the op-disc `cp` before the recompose block and adds the op-disc call alongside the POLYBIUS call, or (b) adds a second subproject-gated block after L980 for the op-disc recompose. Option (a) is cleaner — one subproject block; §6.5 specifies it.)

### 6.3 The slim-core clause that makes the strategy auditable (mirrors Arc-2 §6.3)

The slim core's §0.5 (or a one-line note at the top) carries the tier-awareness rule so the strategy is visible to a reader, not buried in install.sh:

> **Subproject-tier module access (per design-arc-47 §6):** at subproject tier the CONDITIONAL module content is re-inlined into this file at deploy time (install.sh recompose at the `<!-- MODULE-INLINE:<name> -->` markers) — subproject seats do NOT `Read .claude/modules/<X>.md` (the path does not resolve reliably; claude-code #56686/#31546/#29423). At user/project tier the `Read` channel applies and the markers are inert. Anchor: stoa--xyb + design-arc-45 §6 probe (the proven mechanism this arc extends to op-disc).

### 6.4 The MODULE-OWNERSHIP partition — exact signature change (rev2 r3: TWO distinct sets)

The current function (L871) takes ONE arg (`$1` = role file) and the awk receives ONE `module_list` (the global glob, L902) that backs a single `exists[]` array (L909) used by Check A (L916), Check B (L945), AND Check D (L944). **rev1's §6.4 incorrectly claimed "Check A stays global, only Check B/D change" — but with a single narrowed list, Check A would silently narrow too** (ARGUS r3). The rev2 fix passes TWO lists and keeps them distinct in the awk.

**Current (L878–883) — builds ONE owned-set from the GLOBAL glob (this set wrongly serves all three checks):**
```bash
_module_basenames=""
for _src in "${SRC_MODULES_DIR}"/*.md; do
  [ -e "$_src" ] || continue
  _bn="$(basename "$_src" .md)"
  [ "$_bn" = "README" ] && continue
  _module_basenames="${_module_basenames} ${_bn}"
done
```

**Fixed — TWO sets: GLOBAL existence (Check A) + OWNED consumption (Checks B/D):**
```bash
recompose_module_inline() {
  _role_file="$1"
  _owned_basenames="$2"   # space-separated OWNED module basenames for THIS role file (Checks B/D)

  # GLOBAL existence set: every real module source (owner-agnostic), for Check A
  # ("a marker must reference a real module file regardless of owner"). Built from the
  # filesystem glob, NOT from $2 — so Check A's guarantee does NOT narrow with the owned-set.
  _global_basenames=""
  for _src in "${SRC_MODULES_DIR}"/*.md; do
    [ -e "$_src" ] || continue
    _bn="$(basename "$_src" .md)"
    [ "$_bn" = "README" ] && continue
    _global_basenames="${_global_basenames} ${_bn}"
  done
  ...
  awk -v modules_dir="${SRC_MODULES_DIR}" \
      -v global_list="${_global_basenames}" \
      -v owned_list="${_owned_basenames}" '
    BEGIN {
      # GLOBAL existence set (Check A): every real module source.
      ng = split(global_list, _g, " ")
      for (i = 1; i <= ng; i++) { if (_g[i] != "") global_exists[_g[i]] = 1 }
      # OWNED consumption set (Checks B/D): only this role file's modules.
      no = split(owned_list, _o, " ")
      for (i = 1; i <= no; i++) { if (_o[i] != "") { owned[_o[i]] = 1; consumed[_o[i]] = 0; nowned++ } }
      in_marker = 0; markers_seen = 0; _aborting = 0
    }
    # ... OPEN-marker rule:
    #   Check A — marker references a real module source (GLOBAL):
    #     if (!(name in global_exists)) fail("marker MODULE-INLINE:" name " has no module source ...")
    #   (body inline + consumed[name]=1 only matters for owned modules; a marker for a real-but-
    #    cross-owner module cannot legitimately appear in this file — see note below.)
    # ... END checks:
    #   Check D (per-file): markers_seen == 0 && nowned > 0  -> owned bodies would be DROPPED.
    #   Check B (owned-consumed): for (m in owned) if (owned[m] && !consumed[m]) fail(... DROPPED ...)
    ' "$_role_file" > "$_tmp" || { rm -f "$_tmp" "$_role_file"; exit 2; }
```

**Key precision (r3):**
- **Check A** tests `name in global_exists` — the GLOBAL set. A marker naming ANY real module resolves; a marker naming a non-existent module FAILs loudly (P-RECOMPOSE-NEG). This guarantee is owner-agnostic and does NOT narrow with `$2`.
- **Checks B/D** iterate/count `owned[]` / `nowned` — the per-call OWNED set. POLYBIUS's recompose checks only its 5; op-disc's checks only its 12. A cross-owner module (op-disc's `autonomous-mode-setup` during POLYBIUS recompose) is not in `owned[]`, so Check B does not flag it (P-OWNERSHIP).
- **The consumed[] tracking** is keyed on the OWNED set (only owned modules are expected to be consumed by THIS file's markers). A legitimate role file contains markers ONLY for its own owned modules, so every OPEN marker's `name` is in `owned[]` AND in `global_exists[]`. If a marker named a real cross-owner module (a mis-authored file), Check A passes (it exists globally) but Check B would NOT flag it as unconsumed (it is not in `owned[]`) — that mis-authoring is out of scope (it cannot arise from this arc's data-driven call sites, which pass each file its own owned-set; noted as a residual in §7).

The two call sites (replacing the single `recompose_module_inline "$DEST_POLYBIUS"` at L959):
```bash
POLYBIUS_MODULES="onboarding sub-project-spawning pair-programmer-authoring pair-programming-prototyping substrate-update-check"
OPDISC_MODULES="two-polybius-coordination autonomous-mode-setup sub-agent-transcript-discipline bw-fit-matrix oss-dep-and-latency credential-discipline-detail bw-upgrade mechanical-inspection-split multi-team-interop four-layer-identity substrate-component-design jsdom-timing-discipline"
recompose_module_inline "$DEST_POLYBIUS" "$POLYBIUS_MODULES"
recompose_module_inline "$DEST_OPERATING_DISCIPLINES" "$OPDISC_MODULES"
# NOTE: $DEST_PLINY still NOT recomposed (MAJOR_PLINY not cut yet — zero markers, zero owned modules).
#       When PLINY is cut: add PLINY_MODULES + recompose_module_inline "$DEST_PLINY" "$PLINY_MODULES".
```

**Why this is the minimal correct fix:** Check B/D evaluate against the OWNED set (no cross-owner false-positive), while Check A retains its owner-agnostic global existence guarantee (no silent narrowing — r3). The data-driven property is preserved: a future PLINY cut adds `PLINY_MODULES` + a third call, no new code path. (This realizes the Arc-2 §6.5 generality note — which anticipated the multi-source case but assumed each role file owns ALL modules; the shared-dir reality requires the per-call OWNED-set + the retained GLOBAL existence set this §6.4 adds.)

### 6.5 Recompose placement + the dry-run path

Restructure so a SINGLE `if [ "$TARGET" = "subproject" ]` block holds the function definition + both calls, placed AFTER op-disc is deployed:

1. Move the op-disc `cp` (L974–980) to BEFORE the recompose block (so `$DEST_OPERATING_DISCIPLINES` exists when recompose runs), OR keep it and move the recompose block to after L980. Either way: both `$DEST_POLYBIUS` and `$DEST_OPERATING_DISCIPLINES` must be written before their recompose call.
2. The function's existing `$DRY_RUN` guard (L887–890) prints the plan and returns without requiring the file to exist — works unchanged for both calls (it prints `modules:${_owned_basenames}` which is now the owned-set). The dry-run plan now shows BOTH the POLYBIUS owned-set and the op-disc owned-set.
3. FAIL-LOUD semantics (the rm-both-files-on-error at L947–953) apply per-call: an op-disc recompose failure removes the partial op-disc tmp AND the slim op-disc, exits 2, aborts the deploy — install.sh never ships a partial/slim op-disc to a subproject. (P-RECOMPOSE-NEG asserts this.)

### 6.6 Check E (body-contains-a-marker) interaction with op-disc content

Check E (L922) fails if a module BODY contains a literal `<!-- MODULE-INLINE: -->` line (would corrupt recompose). op-disc's relocated modules carry NO MODULE-INLINE markers in their bodies (the markers live in the SLIM CORE stubs, not in the module content). **One caveat for ADA:** the `autonomous-mode-setup.md` module body contains the renewal-cron prompt-body template with `<PLACEHOLDER:...>` and `{{...}}` slots — confirm none is a literal `<!-- MODULE-INLINE:` string (they are not; they are `<PLACEHOLDER:POLLING_CRON_ID>` and `{{RENEWAL_CRON_ID}}` shapes). Check E only matches `^<!-- /?MODULE-INLINE:`. (ARGUS Q2 CONCUR — op-disc source has ZERO literal MODULE-INLINE strings; no verbatim-extracted body can carry one; Check E catches any ADA-introduced one at deploy.)

---

## §7 — Self-assessed weak points (esp. anywhere losslessness is at risk for ANY seat)

1. **The §7 stub now carries 6 real subsection heading lines whose EXACT shape must match the validate-spec `_heading_pattern` — a shape-drift here re-introduces the rev1 BLOCKING regression.** rev2's r1 fix depends on ADA writing `### 7.4 Cross-tier coordination routing` (or any heading line the resolver's `_heading_pattern_for_anchor('7.4')` matches) — NOT a prose mention, NOT a deeper heading level that breaks the cited-anchor expectation, NOT a renamed anchor. *Why this shape anyway:* I verified the resolver pattern matches `### 7.4 …`, `#### 7.4 …`, and `### 7.4. …` and REJECTS the prose-only line (design phase, against the live `spec_refs.py`); the §2.7.1 second literal gives ADA the exact shape; and P-SPEC-XREF runs the SHIPPED resolver against SPECIFICATION.md and asserts all 7 at-risk §7.x refs PASS post-cut (catching any shape-drift mechanically). The residual risk is purely ADA transcription fidelity of the 6 heading lines, which P-SPEC-XREF exercises end-to-end. This is the single most important rev2-new surface.

2. **The two-set recompose (Check A global / Checks B/D owned) is a NEW signature change to a load-bearing deploy function — a wiring error swaps which set backs which check.** rev2 r3 splits the single `exists[]` into `global_exists[]` (Check A) and `owned[]` (Checks B/D). If ADA mis-wires (e.g., Check A reads `owned[]`, or Check B iterates `global_exists[]`), the partition either false-positives (aborts a clean cross-owner deploy — P-OWNERSHIP catches) or under-checks (Check A stops guaranteeing global existence — P-OWNERSHIP-CHECKA catches; or Check B re-acquires the cross-owner false-positive). *Why this shape anyway:* the shared `substrate/modules/` dir is a hard constraint (flat-glob deploy + Read-path convention + Arc-29 `modules/custom/` reservation forbid owner-subdirs), so the partition MUST live in the call sites + the two awk lists; the change is minimal (one extra arg, one extra `-v` list, two BEGIN loops); the data-driven property is preserved for the future PLINY cut; and P-OWNERSHIP + P-OWNERSHIP-CHECKA + P-RECOMPOSE + P-RECOMPOSE-NEG exercise the happy path, the Check-A-global guarantee, the cross-owner non-false-positive, and the FAIL-LOUD path against a throwaway target. The residual risk is awk-correctness of the two scoped checks, which VERA's throwaway-target probes exercise.

3. **The routing-map-omission (op-disc gets only a relocation index) is a REFINEMENT of the proven pattern — ARGUS CONCURRED (Q1) in rev1, but it remains the load-bearing structural call.** Arc-1/Arc-2 paired a routing map WITH the relocation index; this design drops the routing map for op-disc because op-disc dispatches nothing. *Why this shape anyway:* op-disc structurally does not dispatch — the seat that needs a CONDITIONAL module is the seat reading op-disc at the point of need (autonomous-mode entry, credentialed work), so the inline per-stub `Read` pointer IS the correct dispatch-time signal for a non-orchestrator file. ARGUS Q1 CONCUR confirms this. The r2 §15-flip actually STRENGTHENS this position: the one section rev1 thought needed dispatch-time routing (§15, via the false A4 "PLINY names the module") turned out to be read-direct like §25.5 — so NO op-disc section needs a routing-map-equivalent, and the relocation-index-only shape is now cleaner than in rev1. Residual risk is low (CONCURRED) but it is still the structural keystone.

4. **The estimated floor (~760–915) is materially higher than the POLYBIUS cut's (~300–350) AND higher than rev1's (~700–850) because §15 now stays inline — a reviewer expecting a deeper cut may read the floor as "cut too shallow."** op-disc keeps MORE inline than POLYBIUS did (the anti-pattern thesis, escalation triggers, heartbeat, full confabulation, credential structural core, PRINCIPAL-gate, base-vs-custom, Co-Authored-By, the §12 bw-cookbook keep-home that CANNOT relocate, AND now §15 verification-complexity per r2). *Why this shape anyway:* the recalibrated criterion explicitly forbids cutting always-on/read-direct rules to hit a number, and §15 is read-direct by 4 verifier seats every dispatch (r2) — relocating it would either drop canon at the point of need or force a module Read no orchestrator hands them. P-FLOOR reports the actual floor and guards both ends (>1100 = untightened KEEP prose; <650 = a dropped always-on rule); P-KEEP independently asserts §15 + each load-bearing always-on rule is still inline. The floor is honest output, not a target missed.

5. **§22.2 / §27.2 are named in stub PROSE (not as heading lines) — correct for their CURRENT citers, but a FUTURE SPECIFICATION.md cite to §22.2 or §27.2 would silently FAIL the validate-spec resolver.** rev2's census (§3.1.2) confirms SPECIFICATION.md cites ONLY §7's subsections among relocated sections; §22.2/§27.2 are cited only from substrate skills/check.sh in COMMENT/MESSAGE form (not the resolver), so prose-naming suffices today. *Why this shape anyway:* adding heading lines for every relocated subsection regardless of citer would bloat every stub for a hypothetical future spec cite; the census-driven approach (real heading lines ONLY where the exact-heading resolver actually consumes them — §7) is the minimal lossless fix. The residual risk is a FUTURE spec cite to §22.2/§27.2 added after this arc — caught by P-SPEC-XREF on the NEXT validate-spec run (the spec-audit gauntlet would flag the new FAIL), not silently. Flagged so ARGUS confirms the census-driven (not blanket) heading-preserve is the right scope — I judge it is, because P-SPEC-XREF is a standing check that catches any future drift.

---

## §8 — Residual questions for ARGUS (rev2 — focused re-confirm)

1. **The §7 stub heading-line shape (r1 fix).** Does ARGUS concur that keeping `### 7.1`/`### 7.2`/`### 7.3`/`### 7.4`/`### 7.5`/`### 7.7` as real heading lines (with the bodies relocated to the module + markers at the end) is the LOSSLESS option that keeps the validate-spec exact-heading resolver GREEN — and that P-SPEC-XREF (running the shipped resolver against SPECIFICATION.md, asserting the 7 at-risk §7.x refs PASS) is the correct mechanical guard? I verified the resolver pattern matches this shape and rejects the rev1 prose-only line.

2. **The census-driven (not blanket) subsection-heading preserve (weak point 5).** rev2 preserves real subsection heading lines ONLY for §7 (the only section with spec-cited subsections per the live census §3.1.2); §22.2/§27.2 stay prose-named (their citers are comment/message, not the resolver). Does ARGUS concur this is the right scope, or should §22.2/§27.2 ALSO get heading lines defensively against a hypothetical future spec cite? I judge census-driven is correct (P-SPEC-XREF is a standing guard that catches future drift), but it is a judgment call on minimal-vs-defensive.

3. **The two-set recompose wiring (r3 fix).** Does ARGUS concur that the §6.4 two-list signature (GLOBAL `global_exists[]` for Check A; OWNED `owned[]`/`nowned`/`consumed[]` for Checks B/D) correctly preserves Check A's owner-agnostic existence guarantee while scoping B/D to the owned set — and that P-OWNERSHIP-CHECKA (asserting Check A still tests the global set) is the right new probe to catch the rev1 single-array narrowing? The residual mis-authored-cross-owner-marker case (§6.4 note) is out of scope (cannot arise from the data-driven call sites) — does ARGUS agree, or want it guarded?

4. **§15 flip to KEEP (r2) — any second-order ledger effect.** Flipping §15 RELOCATE→KEEP changes counts (12 modules, 19 standalone C-1, floor +~60) and moves §15's `Anchor: stoa--tp1` from the module into the slim core. Does ARGUS see any cross-ref or ledger-consistency effect I missed (e.g., a substrate file that cited §15.4 expecting it in a module vs inline)? §15.4 is cited from save-verdict/SKILL.md + _save_verdict.py — both resolve to the inline §15.4 heading either way, so I judge no effect; confirming.

---

## §9 — Out of scope

- **Cutting MAJOR_PLINY.md** (next epic arc). The §6.4 partition is designed so the PLINY cut adds `PLINY_MODULES` + a third `recompose_module_inline` call with zero new code path — but that cut is a separate arc.
- **Fixing the pre-existing `§7.1.` malformed cite at SPECIFICATION.md L129** (trailing-period anchor that FAILs the resolver pre- AND post-cut). It is a one-character spec-edit (`§7.1.` → `§7.1`), out of this arc's op-disc-cut scope; flagged for a future spec-audit pass. P-SPEC-XREF correctly does NOT count it as a regression (it was already FAIL).
- **Substrate-self-apply re-sync** of the-stoa's deployed `.claude/operating-disciplines.md` (lags source by this arc + Arc 44/46). User-tier POLYBIUS housekeeping per MAJOR_POLYBIUS §18.1.
- **Building the enforcement layer** (stoa--xyb.5). The relocation-index + MODULE-INLINE marker formats are hook-parseable (designed so), but the hook is not built here.
- **Re-homing op-disc §12 (the bw cookbook) into a module.** §12 is the DUPLICATE keep-home for the rest of the substrate; relocating it would break every pointer at it. Stays inline whole.
- **A bw attachment-read primitive.** C-2 here uses `bw create --parent -d` (titled child ticket description), recovered via plain `bw show <child-id>` — the bw-0.13.0 no-attachment-read limitation does not bite this arc.
- **Promoting the inspection-agent / multi-team modules to CAPTAIN seats.** This arc relocates the prose, not the architecture.

---

*Self-assessed weak points are in §7. Residual questions for ARGUS are in §8. This is rev2 (addresses ARGUS r1–r4 against rev1); the next ARGUS re-confirm + ADA read THIS file.*
