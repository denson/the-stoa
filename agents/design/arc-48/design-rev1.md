# Arc 5 (Arc 48) — MAJOR_PLINY.md debloat cut — design rev1

**Ticket:** stoa--xyb.10 (engagement epic stoa--xyb)
**Author:** Denson Smith (the PRINCIPAL — design synthesis, structural choices, relocation ledger)
**Seat:** CAPTAIN_DAEDALUS_the-stoa
**Builds on:** Arc 44 (composition-layer mechanism: `substrate/modules/` glob deploy + `modules/README.md` 3 channels / 3 relocation classes + op-disc §33 thin rule); Arc 45 (MAJOR_POLYBIUS.md cut — the PROVEN stub/marker/recompose pattern + `recompose_module_inline()` shipped data-driven); Arc 47 (operating-disciplines.md cut — the SPECIFICATION.md exact-heading-preserve discipline + the **two-set MODULE-OWNERSHIP partition** (Check A global / Checks B/D owned), shipped at install.sh L894–1008, **with an explicit forward-note (L1006–1008) for THIS PLINY cut**: "add PLINY_MODULES + a third `recompose_module_inline "$DEST_PLINY" "$PLINY_MODULES"` call — no new code path needed").
**Acceptance bar:** LOSSLESS-ON-CANON at ALL tiers (user / project / subproject). MAJOR_PLINY.md is the ORCHESTRATOR role file — it deploys at all three tiers (suffixed at subproject: `MAJOR_PLINY_<subproject>.md`, install.sh L818–822). ARGUS's primary audit target is LOST CANON for the orchestrator seat.
**Recalibrated criterion (PRINCIPAL-ratified, carried from Arc 47):** the lossless-floor is an OUTPUT measured per file, NOT a fixed line target. Falsify on LOSSLESS-COMPLETENESS (every chunk homed + recoverable), NOT a line number. Do NOT cut a load-bearing always-on orchestrator rule to hit a number. The empirical post-cut floor is REPORTED (§3.10), not targeted.

This is the **3rd relocation cut** of the debloat epic. The method (3-bucket relocation), the marker/stub mechanism, the subproject-recompose, the SPECIFICATION.md exact-heading-preserve, and the two-set ownership partition are ALL proven (Arc 45 POLYBIUS + Arc 47 op-disc). This design REUSES them; it does not re-derive them. The PLINY-specific work is: (a) the ambient-vs-conditional classification for an ORCHESTRATOR role file (§2.6); (b) extending install.sh's already-partitioned recompose to a third owned-set (`PLINY_MODULES`) — the smallest of the three install.sh extensions because Arc 47 left the slot open; (c) the LEAN fold of stoa--lyw (the `/resume` INVOCATION discipline) as a separable slice.

---

## §1 — Problem restatement (pre-work gate)

`substrate/MAJOR_PLINY.md` is **801 lines** — the ORCHESTRATOR role file, paste-activated at the top-level Claude Code session that runs the gauntlet pipeline. Like the POLYBIUS and op-disc cuts before it, it grew by empirical-anchor + provenance accretion: §5 (the gauntlet pipeline) expanded across Arcs 18–42 into twelve subsections (§5.1–§5.12), most of which are **beat-specific procedures PLINY uses only at a particular dispatch type or arc boundary** — background-dispatch hygiene (§5.8) fires only on a `run_in_background` Agent dispatch; pre-branch hygiene (§5.9) fires only at branch creation; signoff-accuracy (§5.10) and paste-archival (§5.11) fire only at arc close; the ADA-brief preambles (§5.2/§5.2.1) fire only at ADA dispatch. None of these is read on every orchestration turn. They sit alongside multi-paragraph "N=1 provenance + accretion path" + "Cross-references" + "Empirical anchor" subsections (§5.9.1/.2/.3, §5.9.4.1, §5.10.1/.2/.3, §5.11.1/.2/.3, the §7.x anchors) that are the empirical why-record, read only when someone asks why a rule exists.

The *actionable always-on* orchestrator core — what PLINY needs on every turn it orchestrates — is the gauntlet overview (§5 preamble + the pipeline diagram + the supporting-CAPTAIN table), the communication-channel overview (§6 table), and the discipline RULES (§7.1–§7.8: one-job, verify-then-execute, autonomous-ship, etc.). That core is roughly a third of the lines. The rest splits into (a) beat-specific procedures only fired SOMETIMES (CONDITIONAL → disk module), (b) the empirical why-record (PROVENANCE → bw cite), and (c) content duplicated in the bw cookbook keep-home (DUPLICATE → pointer).

This arc applies the proven 3-relocation-class method (CONDITIONAL → disk module; PROVENANCE → bw cite; DUPLICATE → pointer) to MAJOR_PLINY section by section, **for the whole file**, and extends the Arc-47 two-set subproject-recompose to cover MAJOR_PLINY as the THIRD recompose source (`PLINY_MODULES`). The KEEP bucket is the always-on orchestrator core; the RELOCATE buckets are the beat-specific procedures, the empirical record, and the one DUPLICATE.

It ALSO folds stoa--lyw LEAN: a new PLINY-seat `/resume` INVOCATION discipline (the successor-decides-vs-spawn-fresh half of the session-lineage model). Per the dispatch this is a SEPARABLE slice (its own design section §1A + its own build step) so ARGUS audits LOSSLESS-ON-CANON on the cut independently of the lyw addition.

### 1.1 Imported assumptions (named per §6.1 of the seat envelope — real briefs have implicit scope)

1. **MAJOR_PLINY IS an orchestrator — it gets BOTH a routing map AND a relocation index.** This is the load-bearing difference from the Arc-47 op-disc cut. op-disc dispatches nothing, so Arc 47 gave it ONLY a relocation index (no routing map). PLINY is the orchestrator: its CONDITIONAL modules are read AT A DISPATCH BEAT (ADA-brief preamble at ADA dispatch; background-dispatch hygiene at a `run_in_background` Agent fire; pre-branch hygiene at branch creation; signoff/paste-archival at arc close). The composition layer (`modules/README.md` §4) pairs a routing map (dispatch-time: task-type/beat → module) WITH a relocation index (audit-time: relocated-content → home → class) precisely for an orchestrator file. So MAJOR_PLINY gets the FULL Arc-45 POLYBIUS shape: a routing map keyed on the dispatch BEAT + a relocation index. (This restores the routing-map half that Arc 47 correctly dropped for a non-orchestrator file; ARGUS should confirm the orchestrator-gets-routing-map call — residual Q1.)

2. **CONDITIONAL content relocates to NEW disk modules under `substrate/modules/`** alongside the 5 Arc-45 POLYBIUS modules + the 12 Arc-47 op-disc modules + README. This arc CREATES + POPULATES the new PLINY modules. Naming + per-module contents are in §2.3.

3. **The shared `substrate/modules/` dir is ALREADY a module-OWNERSHIP partition (Arc 47, two distinct sets); this arc adds the THIRD owned-set.** `recompose_module_inline()` already takes `(role_file, owned_basenames)` and passes the awk TWO `-v` lists: a GLOBAL existence set (Check A, owner-agnostic, from the filesystem glob) and a per-call OWNED set (Checks B/D). Arc 47 wired POLYBIUS's 5 + op-disc's 12. This arc adds `PLINY_MODULES` (the per-call owned-set for `$DEST_PLINY`) + a third call. **The two-set discipline HOLDS unchanged: the PLINY owned-set must NOT narrow Check A's global-existence test, and must NOT collide with the POLYBIUS or op-disc owned-sets** (no shared module basename across the three owners). This is the minimal install.sh extension — Arc 47 left the slot open with a forward-note (L1006–1008).

4. **MAJOR_PLINY deploys at ALL three tiers** (user / project / subproject), suffixed at subproject (`MAJOR_PLINY_<subproject>.md`, install.sh L818–822, L849). At subproject tier the modules dir is NOT deployed (`DEST_MODULES_DIR=""`) AND a subproject seat's `Read .claude/modules/X.md` does not resolve reliably (the Arc-45 probe finding, claude-code #56686/#31546/#29423). So a slim MAJOR_PLINY pointing at modules absent from the subproject's `.claude/` would break losslessness for the orchestrator seat at that tier. The fix is the same recompose-inline the other two files use — MAJOR_PLINY's recompose call runs on `$DEST_PLINY` (the suffixed file at subproject tier) inside the existing `if [ "$TARGET" = "subproject" ]` block. **Note:** `$DEST_PLINY` carries the subproject suffix already (L819), so the recompose runs on the suffixed file with no path change — the recompose operates in place on whatever `$DEST_PLINY` resolves to.

5. **Section numbers AND cited subsection-heading lines are PRESERVED via stubs, NOT renumbered.** MAJOR_PLINY §N is cross-referenced by op-disc, MAJOR_POLYBIUS, CAPTAIN_TIRO, CAPTAIN_ADA, the templates, the hooks, the skills, MAJOR_PLINY's own internal cross-refs, AND `SPECIFICATION.md` via the `validate-spec` exact-heading resolver. The live cross-ref census (§3.1, grepped this design phase across `substrate/` AND run through the shipped `spec_refs.py` against SPECIFICATION.md) shows §5, §5.8, §5.9, §5.9.4, §5.10, §6.1, §6.2, §7, §7.2, §8, §9 are cited from active surfaces — and **§5.10, §6.1, §6.2 are cited from SPECIFICATION.md via the exact-heading mechanical resolver** (all PASS today). Renumbering would break the substrate's cross-ref graph. Every relocated section leaves a numbered stub so top-level `MAJOR_PLINY.md §N` cites resolve; every spec-cited SUBSECTION (§5.10, §6.1, §6.2) leaves its subsection HEADING LINE intact in the stub so the exact-heading resolver still resolves it (the Arc-47 r1 discipline, applied here).

6. **MAJOR_PLINY has NO author-like frontmatter field and the new modules must carry none** (P-AUTH guards). MAJOR_PLINY's content — the synthesis — is the PRINCIPAL's per the immutable authorship rule; cited empirical anchors are attributed to their tickets, which is source-citation not authorship.

7. **The stoa--lyw fold is PLINY-seat-scoped and LEAN.** The lyw ticket sketches touch-points across op-disc + MAJOR_POLYBIUS + MAJOR_PLINY + the handoff-author skill. Per the dispatch, this arc folds ONLY the PLINY-seat `/resume` INVOCATION framing (the orchestrator successor deciding `/resume` vs spawn-fresh). The op-disc + POLYBIUS framing the lyw ticket also sketches is NOT in scope here (noted as a follow-up §9 if genuinely needed). The RECORDING half (handoff-author skill step 6) is already shipped; this fold adds the INVOCATION half lean, as a NEW always-on subsection in MAJOR_PLINY's §4 (Activation) — because deciding `/resume` vs spawn-fresh is an activation-beat decision the orchestrator makes every time a successor session starts.

The restatement converges with the brief. The places it does more than paraphrase: (a) assumption 1 — restoring the routing-map half for an orchestrator file (the explicit divergence from the Arc-47 non-orchestrator shape; surfaced as residual Q1); (b) assumption 7 — placing the lyw INVOCATION fold in §4 (Activation) as ALWAYS-ON rather than as a CONDITIONAL module, because the `/resume`-vs-fresh decision is made at every successor activation, so it fails the ambient-vs-conditional test toward KEEP (surfaced as residual Q4).

---

## §1A — The stoa--lyw LEAN fold (SEPARABLE slice — own design section, own build step)

This section specifies the lyw fold in isolation so ARGUS can audit LOSSLESS-ON-CANON on the cut (§2–§7) independently from this addition. The lyw fold ADDS canon (it does not relocate any); it is not part of the line-reducing cut.

### 1A.1 What lyw asks for (the INVOCATION half)

stoa--lyw (SPEC_AUDIT.md finding D4): the `/resume`-prior-generation pattern is described as a STRUCTURAL property of the team (SPECIFICATION.md §4.5, §10.1, §11 — anti-pattern: "Destroying prior-generation sessions before lineage value is exhausted"), but the substrate has NO shipped section on the INVOCATION half of the lineage. The RECORDING half (write a handoff before `/compact` or close) IS shipped (handoff-author skill step 6 + MAJOR_PLINY §9 final bullet). The undocumented INVOCATION half: when does a successor decide `/resume` vs spawn-fresh-and-paste-activate? what happens if the recorded session id is stale? how does the successor distinguish dormant-but-reachable from genuinely-lost? which prior generation to `/resume` when multiple are recorded across multiple handoffs?

### 1A.2 Where it lands and why (ambient-vs-conditional test → KEEP, lean)

The `/resume`-vs-spawn-fresh decision is made at EVERY successor activation of the orchestrator seat — it is an activation-beat decision, not a sometimes-fired procedure. By the ambient-vs-conditional test (does PLINY need this every time a successor activates? — yes), it is KEEP, placed inline in §4 (Activation) as a NEW lean subsection **§4.1 `/resume` invocation discipline (successor-decides-vs-spawn-fresh)**. Keeping it lean is load-bearing to the debloat thesis — the fold is a decision rule + a fall-through, not an essay. (Residual Q4: confirm §4 placement + always-on KEEP vs a CONDITIONAL `resume-invocation.md` module. I judge KEEP-lean because the decision fires at every activation and the rule is short; a module the successor must know to Read at activation has the same bootstrap problem the §4 activation checklist exists to solve.)

### 1A.3 The lean §4.1 content (the literal ADA writes — ~22 lines, no provenance bloat)

```markdown
### 4.1 `/resume` invocation discipline (successor-decides-vs-spawn-fresh)

A successor orchestrator session starts EITHER by `/resume <session-id>` (continuing a
prior generation) OR by a fresh `claude` + activation paste (spawning new). The handoff
doc the predecessor wrote (handoff-author skill; §9) records the session id + in-flight
state; this is the INVOCATION half of that lineage — how the successor decides.

**Prefer `/resume <id>`** when the prior generation holds load-bearing context NOT captured
in the handoff/bw/canon AND the engagement specifically needs that context (mid-arc pickup;
a long reasoning thread the handoff could only summarize).

**Spawn fresh + activation paste** when ANY of: the new engagement is structurally different
from any prior scope; the recorded session id is stale (terminal closed, session expired);
the lineage value is already fully absorbed into canon + bw + the handoff.

**Stale-id fall-through (load-bearing — do NOT improvise).** If `/resume <id>` errors, do
NOT retry-guess other ids. Fall through to a fresh spawn + activation paste, and record the
lineage truncation in the NEW handoff ("predecessor session <id> unreachable; spawned fresh
from handoff <path>"). The truncation note is what lets the NEXT successor see where the
live-session chain broke vs. where canon carried forward.

**Dormant-vs-lost.** A `/resume <id>` that succeeds → dormant-but-reachable (continue). A
`/resume <id>` that errors → treat as lost (fall through); do not block waiting for it to
become reachable.

**Multi-generation navigation.** When multiple generations are recorded across multiple
handoffs, consult handoffs in REVERSE chronological order; each handoff cites its prior-handoff
lineage (handoff-author convention), so the most-recent handoff is the entry point and the
chain is walkable backward. `/resume` the most-recent reachable generation, not an arbitrary one.

Cross-ref: handoff-author skill step 6 (the RECORDING half — companion to this INVOCATION half);
`operating-disciplines.md` §30 (four-layer identity model). Anchor: stoa--lyw.
```

### 1A.4 lyw verification (folded into the cut's probes — P-LYW)

A dedicated probe (P-LYW, §4) asserts §4.1 exists with the decision rule (`/resume`-prefer + spawn-fresh conditions + stale-id fall-through) and the `Anchor: stoa--lyw` cite. This keeps the lyw slice independently falsifiable.

---

## §2 — Approach (the slim structure)

### 2.1 The slim core shape

Post-cut, `substrate/MAJOR_PLINY.md` is the **slim always-on orchestrator core**: §1 (what you are) + §2 (what you do) + §3 (what you don't) + §4 (activation, NOW incl. the §4.1 lyw lean fold) + §5 slim (gauntlet pipeline diagram + supporting-CAPTAIN table + the §5.1 operating-mode rule, with the beat-specific §5.2–§5.12 procedures relocated to modules + stubs) + §6 slim (the communication-channel table + the §6.3 bundle-shape rule, with §6.1's DUPLICATE-leaning cookbook framing pointed at op-disc §12 and §6.2's polling procedure relocated) + §7 (the discipline RULES, tightened, empirical → Anchor) + §8 (ZENO historical note, KEEP — short) + §9 (activation checklist, KEEP) + the routing map + the relocation index. The CONDITIONAL beat-procedures move to disk modules; the provenance/empirical multi-paragraph blocks move to bw cites; the DUPLICATE cookbook consolidates to the op-disc §12 pointer.

### 2.2 The always-loaded ROUTING MAP + RELOCATION INDEX (orchestrator file → BOTH, per modules/README.md §4)

Per modules/README.md §4, the composition layer pairs a routing map (dispatch-time) WITH a relocation index (audit-time). **MAJOR_PLINY is an orchestrator, so it gets BOTH** (assumption 1; the Arc-45 POLYBIUS shape). Both are added as a new **§4.2 "Routing map + relocation index"** placed at the end of §4 (Activation) — the natural home, because the orchestrator consults the routing map at the moment it composes a dispatch (which §4 establishes as the activation/dispatch beat). They use the regular column shapes from modules/README.md §4.1/§4.2 so a future enforcement-layer hook is parseable.

- **Routing map (dispatch-time):** keyed on the BEAT, since PLINY's CONDITIONAL content is beat-triggered, not task-type-triggered. Columns: **dispatch beat → module(s) to load → channel.** Rows: ADA dispatch → `ada-brief-preamble.md`; `run_in_background` Agent fire → `background-dispatch-hygiene.md`; arc branch creation → `pre-branch-hygiene.md`; arc close → `arc-close-hygiene.md`; STRABO-for-propagation dispatch → `post-strabo-vera.md`; verifier returns INCOMPLETE/UNVERIFIABLE → `incomplete-unverifiable-routing.md`; etc. (full set in §2.3).
- **Relocation index (audit-time):** the losslessness-recovery artifact ARGUS audits. Columns: **relocated content → new home → class.** Populated from §3.2 (CONDITIONAL) + §3.3/§3.4 (PROVENANCE) + §3.5 (DUPLICATE).

**Why the routing map IS appropriate here (the divergence from Arc 47).** Arc 47 dropped the routing map for op-disc because op-disc dispatches nothing — its CONDITIONAL modules are read by the seat that hits the trigger, so the inline per-stub `Read` pointer was the correct dispatch-time signal. PLINY is the opposite: it IS the dispatcher, and its CONDITIONAL modules are read AT a dispatch beat the orchestrator controls. So the dispatch-time "at this beat, load this module" routing map is exactly the orchestrator artifact modules/README.md §4.1 describes. The per-stub `Read` pointers ALSO remain (point-of-need redundancy), but the routing map is the orchestrator's beat→module index.

### 2.3 The CONDITIONAL module files (CREATED + POPULATED this arc)

Each module is a self-contained reference body; the module's first line is a stable `# <Title>` heading (the recompose keys on it; P-RECOMPOSE asserts it appears) followed by a provenance header citing this design + the stoa--xyb epic (mirroring modules/README.md:14–16 + the Arc-47 modules). **No module carries an author-like field** (P-AUTH). Line ranges are grounded against the LIVE source (re-read this design phase). Module basenames are checked against the existing 17 (5 POLYBIUS + 12 op-disc) for NO collision (assumption 3).

| Module file | Source § (live line range) | What moves in |
|---|---|---|
| `substrate/modules/ada-brief-preamble.md` | §5.2 + §5.2.1 (116–146) | The ADA grounding-check enumeration literal (§5.2) + the credential-discipline cite for credentialed-ops dispatches (§5.2.1). Both fire only at ADA dispatch. (§5.2 empirical `ariadne--m5e`/`stoa--bxx` → Anchor in module.) |
| `substrate/modules/sub-agent-watchdog.md` | §5.3 (148–166) | The stall predicate (3-condition) + wall-clock fallback + on-kill transcript capture + the open question. Fires only when a dispatched CAPTAIN may be stalling. (§5.3 empirical `stoa--dyb` → Anchor in module.) |
| `substrate/modules/per-worktree-venv.md` | §5.4 (168–180) | The Python `pip install -e` per-worktree `.venv` reflex. Fires only on fresh worktree in a Python editable-install project. (§5.4 anchor `ariadne--b93` cross-repo → C-2 child OR cross-repo-fold; see §3.4.) |
| `substrate/modules/post-strabo-vera.md` | §5.5 (182–200) | The post-STRABO VERA citation-verification dispatch loop (sampling policy + route-per-verdict). Fires only on a propagation-bound STRABO dispatch. (§5.5 empirical `stoa--fea` → Anchor in module.) |
| `substrate/modules/incomplete-unverifiable-routing.md` | §5.6 (202–222) | The INCOMPLETE / UNVERIFIABLE verdict routing protocol. Fires only when a verifier returns one of those shapes. (Cross-refs into op-disc §15 + verifier role files preserved in module.) |
| `substrate/modules/smoke-beat-deploy-check.md` | §5.7 (224–235) | The Phase C smoke-beat install.sh deploy-plan check for new substrate files. Fires only at smoke-beat time for substrate-touching arcs. (§5.7 empirical `stoa--14u` → Anchor in module.) |
| `substrate/modules/background-dispatch-hygiene.md` | §5.8 (237–339) | The full §5.8.1–§5.8.8 canonical sequence: ToolSearch-at-start, fire-Agent + task_id-materialize + Monitor, the **canonical bw-poll-loop template (§5.8.3)**, TaskStop-on-completion, PushNotification-orthogonal, the B1–B6 locked decisions, the Anthropic-side-facts table. The single largest relocation (~103 lines). Fires only on a `run_in_background` Agent dispatch. (§5.8.8 empirical `stoa--nvl`/`stoa--cm3` → Anchor in module.) |
| `substrate/modules/pre-branch-hygiene.md` | §5.9 + §5.9.4 (341–432) | The two-check rule (no other arc-build branch in flight; local main == origin/main) + surface-on-failure shape + the §5.9.4 separate-worktree convention + the §5.9.4 cleanup sequence. Fires only at arc-build branch creation. (§5.9.1/.2/.3 + §5.9.4.1 N=1 provenance → Anchors in module; the spec-citer §5.9 top-level + §5.9.4 stub-preserve in slim core — see §2.7.) |
| `substrate/modules/arc-close-hygiene.md` | §5.10 + §5.11 (434–528) | The signoff-accuracy verify-before-claim rule (§5.10) + the HUMAN_paste archival convention (§5.11). Both fire only at arc close, paired (§5.11 is verified BY §5.10's rule). (§5.10.1/.2/.3 + §5.11.1/.2/.3 N=1 provenance → Anchors in module.) **§5.10 is spec-cited → its heading line stays in the slim-core stub (§2.7).** |
| `substrate/modules/seat-identity-brief.md` | §5.12 (530–564) | The per-CAPTAIN seat-identity dispatch-brief field (`seat-identity: CAPTAIN_<MNEMONIC>_<slug>`). Fires only at a worktree-resident CAPTAIN dispatch. (Cross-refs into op-disc §28 + CAPTAIN_ADA §5.5 preserved in module.) |
| `substrate/modules/pliny-polling-pattern.md` | §6.2 (620–666) | The surface-and-wait polling pattern (asymmetric polling; the CronCreate template; the §6.2a multi-arc autonomous mode). Fires only when PLINY has surfaced a question and is waiting, OR in a multi-arc autonomous engagement. (§6.2 empirical Arcs 16/17 + §6.2a `stoa--bn8`/`stoa--bbi` → Anchors in module.) **§6.2 is spec-cited → its heading line stays in the slim-core stub (§2.7).** |

**11 CONDITIONAL module files created + populated this arc.** (None collides with the 17 existing basenames — checked §3.8.)

### 2.4 KEEP-TIGHTEN sections (stay inline; prose tightened; no relocation)

The always-on orchestrator core. Read on every turn PLINY orchestrates (or are short structural anchors a stub would not improve):

- **§1 (what you are, 15–25).** Always-on identity (rank/mnemonic/role + the `Agent`-tool-doesn't-propagate structural fact + the not-POLYBIUS / not-ZENO boundaries). KEEP-TIGHTEN; the `u--7yg.12` runtime-constraint cite stays (it is the load-bearing reason the seat exists).
- **§2 (what you do, 27–37).** The responsibility table. Always-on. KEEP.
- **§3 (what you don't do, 39–46).** The four don'ts (no PRINCIPAL dialog; no cross-session memory by self; no CHIEF-OF-STAFF collapse; no dispatch of an undeployed CAPTAIN). Always-on role boundary. KEEP.
- **§4 (activation, 48–64) + NEW §4.1 (lyw lean fold) + NEW §4.2 (routing map + relocation index).** Always-on — read at every activation. KEEP-TIGHTEN the existing §4 prose; ADD §4.1 (§1A) + §4.2 (§2.2).
- **§5 preamble + pipeline diagram + supporting-CAPTAIN table + build-session-shape note (66–99).** The gauntlet OVERVIEW every turn. KEEP. The §5.1 operating-mode rule (101–114) — KEEP-TIGHTEN (PLINY carries the mode flag in every dispatch; always-on); compress the two parenthetical cross-ref restatements (114) into the §5.1 cross-ref line.
- **§6 communication-channel table + when-you-finish-an-arc bullets (568–585) + §6.3 bundle-shape rule (668–688).** The channel overview + the engagement-composition rule are always-on orchestrator core. KEEP-TIGHTEN. The §6 closeout bullets (the per-arc design-canon audit `stoa--bxx`, the deploy-verification `stoa--s2p`) stay as RULES with empirical → Anchor. §6.3's empirical instances (680–688) compress to an Anchor (`stoa--bxx`).
- **§7 disciplines (692–766).** The discipline RULES are always-on (one-job §7.1; verify-then-execute §7.2 incl. the Arc-24/Arc-39 scope-broadenings; wait-for-quiescence §7.3; autonomous-ship §7.4; within-arc-artifact §7.5; working-tree-audit §7.6; voice §7.7; no-narrowing-gauntlet §7.8). KEEP-TIGHTEN — every rule stays; the multi-paragraph empirical anchors (the §7.2 Arc-9 directive-error story 732, the §7.2 Arc-39 `stoa--ezj` 3-shape detail 714–728, the §7.8 OK/NOT-OK examples) compress: keep the RULE + the OK/NOT-OK contrast (operational), fold the verbose empirical narratives to `Anchor:` cites (`u--7yg.17/.10/.18/.11/.7/.6/.15`, `stoa--nax`, `stoa--ioy`, `stoa--ezj`).
- **§8 (ZENO historical note, 770–772).** KEEP — 3 lines, points at `v1-historical/MAJOR_PLINY.md`. Already tight.
- **§9 (activation checklist, 776–801).** KEEP — the one-page summary is the operational quick-reference read at every activation. KEEP-TIGHTEN; the final `/compact` handoff bullet (799) stays (it pairs with the §4.1 lyw fold — RECORDING half ↔ INVOCATION half).

### 2.5 DUPLICATE relocation (→ pointer)

- **§6.1 (working with beadwork — command syntax, 586–618)** is the ONLY DUPLICATE-class section. It self-declares its keep-home at the top: *"Canonical cookbook: the full bw operations reference ... lives at `operating-disciplines.md` §12 ... The notes below are PLINY-seat-specific framing; for syntax fundamentals, reference §12 first."* The `-m`-isn't-real table + the per-subcommand syntax table + the `bw prime` framing duplicate op-disc §12 (the bw-cookbook keep-home). **Disposition:** consolidate to the op-disc §12 pointer — keep a SLIM §6.1 that retains the PLINY-seat-specific framing that is NOT in §12 (the "run `bw prime` at session start" reflex + the CAPTAIN_TIRO delegation note + the SPECIFICATION.md cite-marker at L618) and points at op-disc §12 for the syntax fundamentals. **§6.1 is spec-cited (SPECIFICATION.md L533) → its heading line stays live (it stays a real KEEP-slim section, not a stub).** The DUPLICATE here is the cookbook BODY (the tables), not the whole section. (This mirrors the modules/README.md §5.3 worked example, which names MAJOR_PLINY §6.1 explicitly as a copy to consolidate to op-disc §12 — that consolidation is finally executed here.)

### 2.6 Ambient-vs-conditional CALLS — flagged for ARGUS

These are the genuine ambient-vs-conditional judgment calls for an ORCHESTRATOR file. rev1 makes a defensible KEEP/RELOCATE call for each.

- **A1 — §5.1 (operating-mode awareness): KEEP inline.** The ambient-vs-conditional test: does PLINY carry the mode flag EVERY dispatch? Yes — every CAPTAIN brief includes `operating-mode:`. So §5.1 is ambient (KEEP), tightened. (Contrast §5.2–§5.12, which fire only at specific beats — RELOCATE.)
- **A2 — §6.1 (bw command syntax): DUPLICATE-not-CONDITIONAL.** §6.1 is NOT a beat-specific procedure (PLINY uses bw on most turns) — but its BODY duplicates op-disc §12. So it is DUPLICATE class (consolidate the body to the §12 pointer), keeping a slim PLINY-framing residue. The spec-cited §6.1 heading stays live (§2.5). (ARGUS: confirm DUPLICATE-with-slim-residue is the right call vs. a fuller KEEP — I judge DUPLICATE because the tables are verbatim-equivalent to §12 and the README §5.3 worked example explicitly names this consolidation.)
- **A3 — §5.7 (smoke-beat) + §5.5 (post-STRABO VERA) + §5.6 (INCOMPLETE/UNVERIFIABLE): RELOCATE despite being orchestrator-pipeline content.** These are pipeline procedures, but each fires only at a specific beat (smoke-beat time / a propagation-STRABO dispatch / a verifier returning an exceptional verdict shape), not every turn. They pass the conditional test → RELOCATE. The slim §5 preamble's pipeline OVERVIEW is what stays always-on; the beat-specific handling moves to modules the routing map points at.
- **A4 — §6.2 vs §6.2a (polling): RELOCATE both to one module.** §6.2 (surface-and-wait) fires only when PLINY has surfaced a question and is waiting; §6.2a (multi-arc autonomous polling-cron) fires only in a multi-arc engagement. Both conditional → one `pliny-polling-pattern.md` module. The spec-cited §6.2 heading stays in the stub (§2.7). (ARGUS A4: §6.2's anti-pattern "do NOT poll between phases when nothing is blocked" is arguably an always-on guard — but it is meaningful only in the context of the polling procedure it bounds, so it travels WITH the procedure to the module; the slim-core §6.2 stub names the anti-pattern in one line so a reader at §6.2 sees the guard before reading the module.)
- **A-note — §5.8 partial vs whole.** §5.8 relocates WHOLE (all of §5.8.1–§5.8.8). The canonical bw-poll-loop template (§5.8.3) is cited by op-disc §18 as "MAJOR_PLINY.md §5.8 (canonical inline)" — meaning §5.8 IS the canonical home for the template. Post-cut the MODULE is the canonical home and the §5.8 stub points to it; op-disc §18's top-level §5.8 cite resolves to the stub. This is lossless (the template moves intact to the module; the cite still resolves). No partial-section split needed. (Contrast Arc-47's §20, which was a genuine partial-section case; §5.8 is not.)

---

## §2.7 — §-numbering coherence + cited-subsection-heading preserve + the recompose marker + the MODULE-OWNERSHIP partition (3rd owned-set)

### 2.7.1 Section-number + cited-subsection-heading PRESERVE via stubs

The slim core PRESERVES section numbers AND every spec-cited subsection heading line (the Arc-47 r1 discipline). Each CONDITIONAL whole-section relocation leaves a stub at its original number (heading + `Read` pointer + paired recompose marker). The spec-cited subsections **§5.10, §6.1, §6.2** keep their heading lines as REAL markdown headings so the `validate-spec` exact-heading resolver still resolves them.

**Three classes of stub apply in this cut:**

1. **Top-level-only CONDITIONAL relocation (no spec-cited subsection)** — §5.3, §5.4, §5.5, §5.6, §5.7, §5.12. Single §-heading stub + marker. Exact shape (mirrors Arc-47 §2.7.1 first literal):
```
### 5.3 Sub-agent watchdog protocol
Relocated to `.claude/modules/sub-agent-watchdog.md` (CONDITIONAL — read when a dispatched CAPTAIN may be stalling). Recover the stall predicate + on-kill capture via `Read .claude/modules/sub-agent-watchdog.md`. Relocation-index row in §4.2.
<!-- MODULE-INLINE:sub-agent-watchdog -->
<!-- /MODULE-INLINE:sub-agent-watchdog -->
```

2. **CONDITIONAL relocation of a section whose body holds spec-cited subsections** — §5.2 (no spec cite, but §5.2.1 named in prose), §5.8 (top-level spec? no — op-disc cites §5.8 top-level only), §5.9 (top-level cited from substrate; §5.9.4 cited from substrate, NOT spec), §5.10 (**§5.10 IS spec-cited**), §5.11. For §5.10 the stub keeps the `### 5.10` heading line as a real heading (it co-locates with §5.11 in the `arc-close-hygiene.md` module). Exact shape for the §5.10/§5.11 combined stub (the module holds both bodies; the stub preserves both numbered headings, §5.10's because it is spec-cited, §5.11's for uniformity + substrate-internal cites):
```
### 5.10 Signoff-accuracy — verify cleanup claims before posting
Relocated → `arc-close-hygiene.md` §5.10 (CONDITIONAL — read at arc close). Recover the verify-before-claim rule via `Read .claude/modules/arc-close-hygiene.md`. Relocation-index row in §4.2.
### 5.11 HUMAN_paste-*.md archival on arc close
Relocated → `arc-close-hygiene.md` §5.11.
<!-- MODULE-INLINE:arc-close-hygiene -->
<!-- /MODULE-INLINE:arc-close-hygiene -->
```
   For §5.9 + §5.9.4 (combined into `pre-branch-hygiene.md`), the stub keeps `### 5.9` and `### 5.9.4` as real heading lines (both are substrate-cited; neither is spec-cited, but both have external substrate citers per §3.1, so the heading lines preserve the substrate-cite resolution):
```
### 5.9 Pre-branch hygiene — the two-check rule before creating an arc-build branch
Relocated → `pre-branch-hygiene.md` §5.9 (CONDITIONAL — read at arc-build branch creation). Relocation-index row in §4.2.
### 5.9.4 Arc-build worktree convention — separate worktree at .claude/worktrees/arc-N-build/
Relocated → `pre-branch-hygiene.md` §5.9.4.
<!-- MODULE-INLINE:pre-branch-hygiene -->
<!-- /MODULE-INLINE:pre-branch-hygiene -->
```

3. **DUPLICATE-with-slim-residue (NOT a stub — stays a live KEEP-slim section)** — §6.1. The `### 6.1` heading stays live (spec-cited, SPECIFICATION.md L533); the body is slimmed to the PLINY-framing residue + the op-disc §12 pointer; NO recompose marker (nothing relocates to a module — the cookbook tables consolidate to the EXISTING op-disc §12 home). §6.2, by contrast, IS a CONDITIONAL relocation: the `### 6.2` heading stays as a stub heading line (spec-cited, L264/573/595) pointing at `pliny-polling-pattern.md`, WITH a recompose marker.

**§6.2 stub (spec-cited subsection heading preserved + §6.2a co-located):**
```
### 6.2 Surface-and-wait polling pattern (Arc 18)
Relocated → `pliny-polling-pattern.md` §6.2 (CONDITIONAL — read when surfacing-and-waiting on POLYBIUS, OR in a multi-arc autonomous engagement). Anti-pattern preserved here: do NOT poll between phases when nothing is blocked. Recover the full pattern + the §6.2a multi-arc mode via `Read .claude/modules/pliny-polling-pattern.md`. Relocation-index row in §4.2.
<!-- MODULE-INLINE:pliny-polling-pattern -->
<!-- /MODULE-INLINE:pliny-polling-pattern -->
```

The resolver's `_heading_pattern_for_anchor` (verified this design phase against the shipped `spec_refs.py` L63–70) matches `### 5.10 …`, `### 6.1 …`, `### 6.2 …` (hash + space + anchor + `[\s.\-:]`) — so the stub heading lines above resolve. A prose-only mention would NOT match (the Arc-47 r1 failure mode). P-SPEC-XREF asserts all three spec-cited PLINY refs stay PASS.

The paired sentinel `<!-- MODULE-INLINE:<module-name> -->` … `<!-- /MODULE-INLINE:<module-name> -->` is the recompose hook (machine-parseable inert HTML comment at user/project tier; idempotency anchor at subproject tier). `<module-name>` is the module basename without `.md`. Same justification as Arc-45/Arc-47 §2.7. The PROVENANCE `Anchor:` cites and the §-stubs for KEEP sections carry NO recompose marker — only the 11 whole-section CONDITIONAL relocations re-inline at subproject tier. §6.1 (DUPLICATE-with-residue) carries NO marker (its body consolidates to op-disc §12, not to a PLINY module).

### 2.7.2 The MODULE-OWNERSHIP partition — the THIRD owned-set (the minimal install.sh extension)

**The mechanism already exists (Arc 47, two distinct sets).** `recompose_module_inline()` (install.sh L894–998) already takes `(role_file, owned_basenames)` and passes the awk TWO `-v` lists: `global_list` (the filesystem glob minus README → `global_exists[]`, backs Check A) and `owned_list` (the per-call arg → `owned[]`/`nowned`/`consumed[]`, backs Checks B/D). Arc 47 wired two call sites (POLYBIUS's 5, op-disc's 12) and left a forward-note (L1006–1008): *"When PLINY is cut: add PLINY_MODULES + a third `recompose_module_inline "$DEST_PLINY" "$PLINY_MODULES"` call — no new code path needed."*

**This arc's extension (the minimal change Arc 47 designed for):**
1. Add `PLINY_MODULES="ada-brief-preamble sub-agent-watchdog per-worktree-venv post-strabo-vera incomplete-unverifiable-routing smoke-beat-deploy-check background-dispatch-hygiene pre-branch-hygiene arc-close-hygiene seat-identity-brief pliny-polling-pattern"` (the 11-module PLINY owned-set) next to the existing `POLYBIUS_MODULES` + `OPDISC_MODULES` (L1002–1003).
2. Add `recompose_module_inline "$DEST_PLINY" "$PLINY_MODULES"` after the existing two calls (replacing the L1006–1008 forward-note comment).
3. **No function-body change.** Check A still tests `name in global_exists` (the GLOBAL set, now 5 + 12 + 11 = 28 module sources minus README); Checks B/D iterate/count the PLINY owned-set for the `$DEST_PLINY` call. The two-set discipline holds unchanged — the PLINY owned-set does NOT narrow Check A (it's a separate list), and does NOT collide with the POLYBIUS/op-disc owned-sets (no shared basename — §3.8).

**Why this is the minimal correct extension.** The Arc-47 design's "data-driven property" claim is realized exactly here: the PLINY cut adds a `PLINY_MODULES` var + a third call, with ZERO new code path in the function. The global-existence Check A picks up the 11 new module sources automatically (it globs the filesystem). The only correctness obligations are: (a) every PLINY module basename in `PLINY_MODULES` has a real source file (Check A guards; P-RECOMPOSE-NEG); (b) every PLINY module has a marker in MAJOR_PLINY (Check B/D guard; P-RECOMPOSE); (c) no basename collision across the three owner-sets (P-OWNERSHIP-NOCOLLIDE, new this arc). Obligation (c) is the one NEW failure surface the third owner introduces — see §6.4.

---

## §3 — The relocation ledger (the losslessness proof artifact)

This ledger is the artifact ARGUS audits for LOST CANON. **One row per relocated chunk.** Every section in the 801-line source either appears as a ledger row with a lossless home OR is a KEEP-TIGHTEN section that stays inline (§3.7 lists those for audit completeness). Line ranges are grounded against the LIVE `substrate/MAJOR_PLINY.md` (re-read this design phase).

### 3.1 Cross-ref-preservation check (which MAJOR_PLINY §N are cited elsewhere — confirmed for stub-preserve)

Grepped live across `substrate/` (active files only — role files, install.sh, hooks, templates, skills, modules) AND `SPECIFICATION.md` at repo root via the shipped `validate-spec` resolver (`spec_refs.py`; arc directives + pastes are frozen history, excluded). Distinct MAJOR_PLINY §N cited from ACTIVE files:

| §N cited | Citing active files (sample) | SPEC-resolver? | Disposition under this cut |
|---|---|---|---|
| §5 | onboarding.md, paste-instruction-template (top-level) | no | KEEP (the §5 preamble/overview stays inline — stub n/a) |
| §5.8 | op-disc §18 (×5, L660–664, "canonical inline"), CAPTAIN_TIRO §206 | no | **RELOCATE → stub preserves §5.8** (top-level; module is canonical home) |
| §5.9 | MAJOR_POLYBIUS, pretooluse-clean-tree-before-branch.sh, onboarding.md, paste-instruction-template (×2) | no | **RELOCATE → stub preserves §5.9** (real heading line — substrate-cited) |
| §5.9.4 | (internal + substrate) | no | **RELOCATE → stub preserves §5.9.4** (real heading line — substrate-cited) |
| §5.10 | inspect-script-output/SKILL.md, **SPECIFICATION.md L448/562/625** | **YES (PASS×3)** | **RELOCATE → stub keeps `### 5.10` REAL HEADING LINE** (spec resolver) |
| §6.1 | CAPTAIN_TIRO §6.1, modules/README.md §261, **SPECIFICATION.md L533** | **YES (PASS)** | **DUPLICATE-slim → `### 6.1` stays LIVE** (spec resolver; body consolidates to op-disc §12) |
| §6.2 | onboarding.md, paste-instruction-template (×2), **SPECIFICATION.md L264/573/595** | **YES (PASS×3)** | **RELOCATE → stub keeps `### 6.2` REAL HEADING LINE** (spec resolver) |
| §7 | install.sh (top-level) | no | KEEP (the §7 disciplines stay inline — stub n/a) |
| §7.2 | (internal + substrate) | no | KEEP (§7.2 verify-then-execute rule stays inline — stub n/a) |
| §8 | (internal) | no | KEEP (§8 ZENO note stays inline — stub n/a) |
| §9 | (internal) | no | KEEP (§9 checklist stays inline — stub n/a) |

**Check result:** every MAJOR_PLINY §N cited from an active substrate file OR from SPECIFICATION.md resolves post-cut. KEEP sections keep their numbers (rule stays inline); top-level/substrate-cited RELOCATE sections leave a numbered §-heading stub; the THREE spec-cited subsections (§5.10, §6.1, §6.2) keep their `###`-heading lines (live for §6.1; stub-heading for §5.10/§6.2) so the exact-heading spec resolver stays GREEN. P-XREF + P-SPEC-XREF assert this.

### 3.1.2 SPECIFICATION.md MAJOR_PLINY cite census (run live via spec_refs.py this design phase)

Ran `python substrate/skills/validate-spec/_lib/spec_refs.py --spec SPECIFICATION.md --repo-root .` against the LIVE source and filtered to MAJOR_PLINY refs. The COMPLETE result:

| MAJOR_PLINY anchor cited in SPEC | spec line(s) | current verdict | top-level or subsection? | rev1 disposition |
|---|---|---|---|---|
| §5.10 | 448, 562, 625 | PASS (×3) | subsection | **stub keeps `### 5.10` heading line** |
| §6.1 | 533 | PASS | subsection | **§6.1 stays LIVE (DUPLICATE-slim) — heading stays live** |
| §6.2 | 264, 573, 595 | PASS (×3) | subsection | **stub keeps `### 6.2` heading line** |
| §N | 7 | FAIL | (reading-note prose) | NOT a real cite — pre-existing FAIL, not a regression |

**The complete at-risk set (would flip PASS→FAIL under a prose-only stub):** **§5.10 (L448/562/625), §6.2 (L264/573/595) = 6 PASS cites across 2 relocated subsection anchors.** §6.1 is DUPLICATE-slim (stays a live section, not stubbed), so its single PASS cite (L533) is preserved by the live `### 6.1` heading — but P-SPEC-XREF asserts it stays PASS regardless (a slim-residue rewrite that accidentally dropped the heading would flip it). **No OTHER PLINY section has a spec-cited SUBSECTION** — §5.8/§5.9/§5.9.4 are cited only from substrate files (not the spec resolver), preserved by their stub heading lines for substrate-cite resolution.

**Pre-existing non-regression:** the `§N` ref at SPECIFICATION.md L7 (the reading-note prose `MAJOR_PLINY.md §N`) FAILs the resolver pre-cut (the resolver builds a pattern for literal anchor `N` which no heading matches). It is a documentation example in the spec's reading-note, not a real cite, and FAILs before AND after this cut. P-SPEC-XREF's assertion is "ZERO MAJOR_PLINY refs flip PASS→FAIL," which this pre-existing FAIL does not violate.

### 3.2 CONDITIONAL relocations (→ disk module; slim-core residue = stub + `Read` pointer + recompose marker + routing-map row + relocation-index row) — 11 modules

| Source (§ + live lines) | Class | New home | Slim-core residue |
|---|---|---|---|
| §5.2 + §5.2.1 (116–146) | CONDITIONAL | `modules/ada-brief-preamble.md` | §5.2 stub (names §5.2.1 in prose) + `<!-- MODULE-INLINE:ada-brief-preamble -->` + routing-map row (ADA dispatch) + index row |
| §5.3 (148–166) | CONDITIONAL | `modules/sub-agent-watchdog.md` | §5.3 stub + marker + routing-map row (CAPTAIN-may-stall) + index row |
| §5.4 (168–180) | CONDITIONAL | `modules/per-worktree-venv.md` | §5.4 stub + marker + routing-map row (fresh worktree, Python editable) + index row |
| §5.5 (182–200) | CONDITIONAL | `modules/post-strabo-vera.md` | §5.5 stub + marker + routing-map row (propagation-STRABO dispatch) + index row |
| §5.6 (202–222) | CONDITIONAL | `modules/incomplete-unverifiable-routing.md` | §5.6 stub + marker + routing-map row (verifier returns INCOMPLETE/UNVERIFIABLE) + index row |
| §5.7 (224–235) | CONDITIONAL | `modules/smoke-beat-deploy-check.md` | §5.7 stub + marker + routing-map row (smoke-beat for substrate arc) + index row |
| §5.8 (237–339) | CONDITIONAL | `modules/background-dispatch-hygiene.md` | §5.8 stub (canonical-home framing in stub) + marker + routing-map row (`run_in_background` Agent fire) + index row |
| §5.9 + §5.9.4 (341–432) | CONDITIONAL | `modules/pre-branch-hygiene.md` | §5.9 + §5.9.4 REAL HEADING-LINE stubs + marker + routing-map row (arc-build branch creation) + index row |
| §5.10 + §5.11 (434–528) | CONDITIONAL | `modules/arc-close-hygiene.md` | §5.10 (**REAL HEADING LINE — spec-cited**) + §5.11 heading-line stubs + marker + routing-map row (arc close) + index row |
| §5.12 (530–564) | CONDITIONAL | `modules/seat-identity-brief.md` | §5.12 stub + marker + routing-map row (worktree-resident CAPTAIN dispatch) + index row |
| §6.2 + §6.2a (620–666) | CONDITIONAL | `modules/pliny-polling-pattern.md` | §6.2 (**REAL HEADING LINE — spec-cited**) stub (names the anti-pattern in prose) + marker + routing-map row (surface-and-wait / multi-arc autonomous) + index row |

**11 CONDITIONAL chunks → 11 new module files.** Largest: `background-dispatch-hygiene.md` (~103 source lines, §5.8.1–§5.8.8) — one coherent procedure, acceptable per op-disc §33 per-module line-count discipline (cf. Arc-47's `autonomous-mode-setup.md` at ~249, accepted). `pre-branch-hygiene.md` (~92) and `arc-close-hygiene.md` (~95) are the next two; each is a coherent paired procedure (open-beat / close-beat).

**§5.8 canonical-home note:** op-disc §18 (L662) cites §5.8 as "canonical inline" for the bw-poll-loop template. Post-cut the MODULE `background-dispatch-hygiene.md` is the canonical home; the §5.8 stub's framing line states this ("the canonical bw-poll-loop template now lives in `background-dispatch-hygiene.md`"). op-disc §18's cite is top-level §5.8 → resolves to the stub. **Recommended (not required this arc):** op-disc §18 L662's parenthetical "(canonical inline)" is now slightly stale (the canonical copy is in the module, re-inlined at subproject tier). It still resolves correctly (top-level §5.8 → stub → module), so it is NOT a cut regression; flagged as a one-line follow-up for the §9 capstone or a future op-disc touch, NOT actioned here (would expand scope into op-disc).

### 3.3 PROVENANCE relocations — C-1 (already-in-bw; content-check then delete-to-Anchor)

The "N=1 provenance + accretion path" + "Cross-references" + "Empirical anchor" subsections relocate to bw cites. The slim core keeps the RULE + a one-line `Anchor: <bw-id>`. **The C-1 content-check gate (modules/README.md §5.2, carried into the build):** before ADA deletes ANY C-1 inline provenance prose, ADA runs `bw show <cited-id>` and content-checks the ticket carries the story. Per-deletion gate. VERA re-executes a sample (P-C1). All ticket ids below resolve-checked live this design phase (§ "Read first" anchors) except the cross-repo `ariadne--b93` (§3.4).

| Source (§ + live lines) | bw id(s) | Slim-core residue |
|---|---|---|
| §5.2 empirical (136) | `stoa--bxx` (+ `ariadne--m5e`/`ariadne--hhb` cross-repo) | Moves WITH §5.2 into `ada-brief-preamble.md`; `Anchor: stoa--bxx` in module (ariadne--* fold into recovery note) |
| §5.3 empirical (166) | `stoa--dyb` (+ ariadne post-mortem path cross-repo) | Moves WITH §5.3 into `sub-agent-watchdog.md`; `Anchor: stoa--dyb` in module |
| §5.5 empirical (200) | `stoa--fea` | Moves WITH §5.5 into `post-strabo-vera.md`; `Anchor: stoa--fea` in module |
| §5.7 anchor (235) | `stoa--14u` | Moves WITH §5.7 into `smoke-beat-deploy-check.md`; `Anchor: stoa--14u` in module |
| §5.8.8 empirical (339) | `stoa--nvl`, `stoa--cm3` (+ `stoa--odh`) | Moves WITH §5.8 into `background-dispatch-hygiene.md`; `Anchor: stoa--nvl (Arc 24 stoa--cm3)` in module |
| §5.9.1/.2/.3 + §5.9.4.1 (371–432) | `stoa--3cs`, `stoa--ads`, `stoa--32b.1/.2`, PR refs | Move WITH §5.9 into `pre-branch-hygiene.md`; `Anchor: stoa--3cs` (+ §5.9.4 `stoa--32b.1`) in module |
| §5.10.1/.2/.3 (450–473) | `stoa--ads` | Move WITH §5.10 into `arc-close-hygiene.md`; `Anchor: stoa--ads` in module |
| §5.11.1/.2/.3 (506–528) | `stoa--f37` | Move WITH §5.11 into `arc-close-hygiene.md`; `Anchor: stoa--f37` in module |
| §6.2 empirical (646) | Arcs 16/17 in-prose | Moves WITH §6.2 into `pliny-polling-pattern.md`; folds into recovery note |
| §6.2a empirical (666) | `stoa--bn8`, `stoa--bbi` | Moves WITH §6.2 into `pliny-polling-pattern.md`; `Anchor: stoa--bn8` in module |
| §6.3 empirical (688) | `stoa--bxx` | KEEP §6.3 rule inline; `Anchor: stoa--bxx` (folds with §6 closeout's stoa--bxx) |
| §6 closeout: design-canon audit (581) | `stoa--bxx` | KEEP §6 closeout rule; `Anchor: stoa--bxx` |
| §6 closeout: deploy-verification (582) | `stoa--s2p` | KEEP §6 closeout rule; `Anchor: stoa--s2p` |
| §7.1 (700) | `u--7yg.17` | KEEP §7.1 rule; `Anchor: u--7yg.17` |
| §7.2 (706–732 narratives) | `u--7yg.10`, `u--7yg.18`, `stoa--ioy` (Arc 24), `stoa--ezj` (Arc 39) | KEEP §7.2 rule + the 3-step probe sequence + OK/NOT-OK; `Anchor: u--7yg.10, u--7yg.18, stoa--ioy, stoa--ezj` (the Arc-9 directive-error narrative + the verbose `stoa--ezj` empirical fold to Anchor) |
| §7.3 (734) | `u--7yg.15` | KEEP §7.3 rule; `Anchor: u--7yg.15` |
| §7.4 (738) | `u--7yg.11` | KEEP §7.4 rule; `Anchor: u--7yg.11` |
| §7.5 (742) | `u--7yg.7` | KEEP §7.5 rule; `Anchor: u--7yg.7` |
| §7.6 (746) | `u--7yg.6` | KEEP §7.6 rule; `Anchor: u--7yg.6` |
| §7.8 (754–766) | `stoa--nax` | KEEP §7.8 rule + OK/NOT-OK; `Anchor: stoa--nax` |

**Counting note:** PROVENANCE rows that "move WITH" a CONDITIONAL section (§5.2/§5.3/§5.5/§5.7/§5.8/§5.9/§5.10/§5.11/§6.2 empiricals — **9 sections' worth**) relocate inside their parent module as a compressed `Anchor:` line; counted under the CONDITIONAL relocation, not separately. The standalone C-1 PROVENANCE chunks (compress-to-Anchor in the KEEP slim core) are: §6.3, §6-closeout-design-audit, §6-closeout-deploy-verify, §7.1, §7.2, §7.3, §7.4, §7.5, §7.6, §7.8 = **10 standalone C-1 chunks.**

### 3.4 C-2 archive-first cases — DEDICATED CHILD TICKETS (Arc-45/Arc-47 precedent)

Provenance with NO clean single `stoa--` home AND that becomes the only surviving copy once cut. Per the Arc-45/Arc-47 adjudication: archive each to a DEDICATED CHILD TICKET (`bw create … --parent stoa--xyb.10 -d "<verbose prose>"`), NOT a bare `bw comment` (a titled child id is discoverable from the relocation-index Anchor; a buried comment is not).

| Source (§ + live lines) | What archives | Slim-core residue |
|---|---|---|
| §5.4 anchor (180) — `ariadne--b93` cross-repo, no `stoa--` mirror | The §5.4 per-worktree-venv reflex empirical (filed in ariadne-core-workspace; `ariadne--b93` does NOT resolve in `stoa--` bw — confirmed this design phase) | C-2 child ticket under stoa--xyb.10; the reflex RULE + detection move WITH §5.4 into `per-worktree-venv.md`; the cross-repo provenance anchor archives to the child ticket; `Anchor: stoa--xyb.10.N (orig ariadne--b93)` in module |

**1 firm C-2 chunk** (§5.4's cross-repo anchor). Rationale: `ariadne--b93` is in a different bw store (ariadne-core-workspace), not visible from the-stoa's `bw show`, so a bare `Anchor: ariadne--b93` would be unrecoverable from this repo's bw. Archiving the §5.4 empirical to a `stoa--xyb.10.N` child ticket (with the `ariadne--b93` origin noted in the description) makes it recoverable from the-stoa's own bw — the Arc-47 cross-repo-fold pattern, escalated to C-2 because there is NO `stoa--` mirror at all (unlike §5.2/§5.3 which have `stoa--bxx`/`stoa--dyb` mirrors). **Per-deletion content-check gate (C-2 analogue):** ADA runs `bw create` FIRST, then `bw show <child-id>` to confirm the description carries the verbose prose, THEN deletes inline. Archive-FIRST, content-CHECK, THEN delete. (P-C2 asserts the child ticket exists + carries the prose + the Anchor cite matches.)

(ARGUS Q5: is §5.4 better as C-2-child or as a cross-repo-fold `Anchor: ariadne--b93` recovery-note like Arc-47 used for `ariadne--sh7`/`railway--*`? I judge C-2-child because §5.4 has NO `stoa--` co-anchor to fold INTO — the whole empirical lives only in the cross-repo ticket, so a bare cross-repo Anchor is unrecoverable from this bw. Arc-47's cross-repo folds always had a `stoa--` primary to attach the cross-repo id to. Confirming.)

### 3.5 DUPLICATE relocations (→ pointer)

| Source (§ + live lines) | Class | Keep-home | Slim-core residue |
|---|---|---|---|
| §6.1 cookbook tables (594–614) | DUPLICATE | `operating-disciplines.md` §12 (the bw-cookbook keep-home) | §6.1 stays a LIVE slim section: KEEP the PLINY-framing residue (`bw prime` reflex 592, CAPTAIN_TIRO delegation 618, the SPECIFICATION.md cite-marker 618) + a one-line pointer to op-disc §12 for syntax fundamentals; DELETE the duplicated `-m`-isn't-real table + per-subcommand syntax table; relocation-index row |

**1 DUPLICATE chunk** (§6.1's cookbook tables). The keep-home (op-disc §12) already exists and is the canonical bw cookbook; §6.1 already self-declares it points there. This consolidation is the one named explicitly in modules/README.md §5.3's worked example (which cites `MAJOR_PLINY.md §6.1` as a copy to consolidate to op-disc §12) — finally executed here. §6.1's heading stays live (spec-cited L533); only the duplicated tables are removed. NO module created (DUPLICATE is never a module — README §5.3).

### 3.6 SPLIT per-line enumeration (cross-ref subsections — deterministic, no ADA guessing)

The "Cross-references" subsections at the tail of KEEP/relocated sections mix LIVE in-file/sibling-file/skill/tool pointers (stay) with PROVENANCE bw-id/empirical lines (fold into the section's `Anchor:`). The rule (Arc-45/Arc-47): **keep every line that points at a §/file/skill/tool a reader follows to OPERATIONAL content; fold every line that says "exists because <ticket/date>" or "Empirical anchor: <ticket>" into the section's Anchor.** Sections whose body relocates whole (§5.2–§5.12, §6.2) carry their cross-refs INTO the module — no SPLIT needed there. SPLIT applies only to the cross-ref tails of KEEP sections.

The KEEP sections with cross-ref tails to SPLIT:

- **§5.1 cross-refs (112–114):** MAJOR_POLYBIUS §13 + op-disc §10 + op-disc §11 (sibling LIVE — keep); the two Arc-37 parenthetical restatements (114) (PROVENANCE/redundant — fold into the §5.1 cross-ref line, compress to one pointer).
- **§7.2 cross-refs (730):** op-disc §19 (in-file-adjacent LIVE — keep); MAJOR_POLYBIUS §4.3.1 (sibling LIVE — keep); the four-discipline-cluster `stoa--ioy`/`stoa--nvl`/`stoa--53u` line (730) (PROVENANCE — fold into §7.2 Anchor).
- **§7.8 cross-refs (766):** op-disc §6 + §6.7.1 + §6.7.2 (in-file-adjacent LIVE — keep); no trailing empirical-only line (the `stoa--nax` anchor is already inline at the §7.8 rule — folds to the §7.8 Anchor).

**3 SPLIT cross-ref tails** (all on KEEP sections; LIVE pointers stay verbatim, the trailing empirical/ticket lines fold into the section's Anchor). P-SPLIT greps the LIVE pointer text (drift-resistant) + asserts the folded bw-ids appear in the §N Anchor, not orphaned as a standalone cross-ref bullet.

### 3.7 KEEP-TIGHTEN (stays inline; listed for audit completeness)

§1 (what-you-are), §2 (what-you-do), §3 (what-you-don't), §4 (activation) + NEW §4.1 (lyw lean fold) + NEW §4.2 (routing map + relocation index), §5 preamble + pipeline diagram + supporting-CAPTAIN table + build-session note + §5.1 (operating-mode, KEEP per A1), §6 channel table + closeout bullets (rules; empirical → Anchor) + §6.1 slim residue (DUPLICATE-slim, heading live) + §6.3 (bundle-shape rule), §7.1–§7.8 (discipline RULES; empirical → Anchors), §8 (ZENO note), §9 (activation checklist). Plus the title/header block (1–13).

### 3.8 Module-OWNERSHIP record (for the install.sh partition — §6.4) — the THREE owner-sets, NO basename collision

| Owner role file | Owned modules (basenames) |
|---|---|
| `MAJOR_POLYBIUS.md` (Arc 45) | `onboarding`, `sub-project-spawning`, `pair-programmer-authoring`, `pair-programming-prototyping`, `substrate-update-check` |
| `operating-disciplines.md` (Arc 47) | `two-polybius-coordination`, `autonomous-mode-setup`, `sub-agent-transcript-discipline`, `bw-fit-matrix`, `oss-dep-and-latency`, `credential-discipline-detail`, `bw-upgrade`, `mechanical-inspection-split`, `multi-team-interop`, `four-layer-identity`, `substrate-component-design`, `jsdom-timing-discipline` |
| `MAJOR_PLINY.md` (THIS arc) | `ada-brief-preamble`, `sub-agent-watchdog`, `per-worktree-venv`, `post-strabo-vera`, `incomplete-unverifiable-routing`, `smoke-beat-deploy-check`, `background-dispatch-hygiene`, `pre-branch-hygiene`, `arc-close-hygiene`, `seat-identity-brief`, `pliny-polling-pattern` |
| (`README.md` — owned by nobody; excluded from every owner-set) | — |

**MAJOR_PLINY owns 11 modules.** **NO basename collides across the three owner-sets** (verified this design phase: the 11 PLINY basenames are disjoint from the 5 POLYBIUS + 12 op-disc = 17 existing — P-OWNERSHIP-NOCOLLIDE asserts this mechanically). The GLOBAL EXISTENCE set for Check A is the full `substrate/modules/*.md` glob (5 + 12 + 11 = 28 modules, minus README), owner-agnostic. The per-call OWNED sets drive Checks B/D: POLYBIUS's 5, op-disc's 12, PLINY's 11.

### 3.9 Ledger summary (chunk counts per class — self-consistent)

- **CONDITIONAL:** 11 relocations (§5.2+§5.2.1, §5.3, §5.4, §5.5, §5.6, §5.7, §5.8, §5.9+§5.9.4, §5.10+§5.11, §5.12, §6.2+§6.2a) → **11 new module files. = 11 CONDITIONAL chunks.**
- **PROVENANCE:** **10 standalone C-1** (§6.3, §6-closeout-design-audit, §6-closeout-deploy-verify, §7.1, §7.2, §7.3, §7.4, §7.5, §7.6, §7.8) + **1 firm C-2** (§5.4 cross-repo → child ticket) + **3 SPLIT** cross-ref tails (§5.1, §7.2, §7.8) = **14 PROVENANCE chunks.** Plus 9 "move-with-CONDITIONAL" provenance Anchors (§5.2/§5.3/§5.5/§5.7/§5.8/§5.9/§5.10/§5.11/§6.2) counted under their parent CONDITIONAL relocation, not separately.
- **DUPLICATE:** **1 chunk** (§6.1 cookbook tables → op-disc §12 pointer; §6.1 heading stays live).
- **KEEP-TIGHTEN:** ~14 section-groups stay inline (listed §3.7), PLUS 2 NEW always-on additions (§4.1 lyw fold + §4.2 routing/index).

**Total relocated chunks: 11 CONDITIONAL + 14 PROVENANCE + 1 DUPLICATE = 26 relocated chunks**, each with a lossless home + recovery path.

### 3.10 Empirical post-cut floor ESTIMATE (reported, not targeted — per recalibrated criterion)

The big movers: 11 CONDITIONAL relocations move ~580 source lines off-disk (§5.2+§5.2.1≈31 + §5.3≈19 + §5.4≈13 + §5.5≈19 + §5.6≈21 + §5.7≈12 + §5.8≈103 + §5.9+§5.9.4≈92 + §5.10+§5.11≈95 + §5.12≈35 + §6.2+§6.2a≈47). The §6.1 DUPLICATE consolidation removes ~21 table lines (keeps ~10 residue lines). The 10 C-1 + 1 C-2 standalone provenance compressions turn ~60 verbose lines into ~12 Anchor lines (net ~48 saved). The §7 empirical-narrative compression (§7.2's Arc-9 + `stoa--ezj` narratives, §7.8's examples) saves ~30. AGAINST these reductions, the cut ADDS ~22 lines (the §4.1 lyw lean fold) + ~30 lines (the §4.2 routing map + relocation index, ~26 rows total across 11 CONDITIONAL + a few PROVENANCE/DUPLICATE index rows). Against 801, the slim core lands an **estimated empirical floor in the ~250–330 line band.** Every line is always-on orchestrator core (what-you-are/do/don't, activation incl. the lyw fold + routing/index, the gauntlet OVERVIEW, the channel table, the discipline RULES, the ZENO note, the checklist). **This is an ESTIMATE; the build REPORTS the actual floor (P-FLOOR).** Do NOT cut a KEEP rule to push the floor lower — the floor is whatever the always-on orchestrator core weighs (recalibrated criterion). A landing materially above ~420 means a KEEP section's prose is still verbose (tighten); a landing below ~200 is suspicious (check for a dropped always-on rule — P-FLOOR falsifier guard).

This floor is COMPARABLE to the POLYBIUS cut's (~300–350) and far below op-disc's (~760–915) — MAJOR_PLINY is structurally closer to POLYBIUS (a role file with a small always-on core + many beat-specific procedures) than to op-disc (a universal layer that must keep a large always-on core inline).

---

## §4 — Verification probes (what would falsify the design's intended behavior)

Concrete probes VERA re-executes. The probe spec is load-bearing. Run all from the worktree root (`C:/Users/denso/claude_projects/the-stoa/.claude/worktrees/arc-48-build`).

### P-FLOOR — empirical floor reported + sanity band
```bash
wc -l substrate/MAJOR_PLINY.md
```
**Pass:** the floor is REPORTED; sanity band ~250–330 (rev1 estimate). **Falsifies if:** > 420 (cut too shallow — a KEEP section's prose is still verbose) or < 200 (suspiciously aggressive — check for a dropped always-on KEEP rule). A 330–420 landing is partial-not-failure. Also run op-disc §33's per-module line-count discipline against each of the 11 new modules (no module is a re-bloat monolith — `background-dispatch-hygiene.md` at ~103 is the largest and is acceptable: one coherent procedure incl. the canonical poll-loop template).

### P-COND — every CONDITIONAL section has a real module home (11 modules)
```bash
for m in ada-brief-preamble sub-agent-watchdog per-worktree-venv post-strabo-vera \
         incomplete-unverifiable-routing smoke-beat-deploy-check background-dispatch-hygiene \
         pre-branch-hygiene arc-close-hygiene seat-identity-brief pliny-polling-pattern; do
  test -s "substrate/modules/$m.md" && echo "OK $m" || echo "MISSING $m"
done
```
**Pass:** all 11 module files exist non-empty. **Falsifies if:** any missing/empty (LOST CANON).

### P-STUB — every relocated section leaves a stub at its original number
```bash
grep -nE '^### (5\.2|5\.3|5\.4|5\.5|5\.6|5\.7|5\.8|5\.9|5\.9\.4|5\.10|5\.11|5\.12|6\.2) ' substrate/MAJOR_PLINY.md
# §6.1 must be a LIVE section (DUPLICATE-slim, KEEP heading), not a stub:
grep -nE '^### 6\.1 ' substrate/MAJOR_PLINY.md && echo "OK §6.1 live (DUPLICATE-slim)" || echo "FAIL §6.1 missing"
```
**Pass:** §5.2, §5.3, §5.4, §5.5, §5.6, §5.7, §5.8, §5.9, §5.9.4, §5.10, §5.11, §5.12, §6.2 headings present (stubs) AND §6.1 heading present (live). **Falsifies if:** any relocated section number GONE, OR §6.1 reduced to a stub/removed.

### P-SPEC-XREF — SPECIFICATION.md MAJOR_PLINY refs do NOT regress (THE blocking-finding probe)
```bash
python substrate/skills/validate-spec/_lib/spec_refs.py --spec SPECIFICATION.md --repo-root . \
  > spec_refs_postcut.jsonl 2>&1
python3 - <<'PY'
import json
# at-risk set: the spec-cited MAJOR_PLINY subsections that PASS pre-cut (census §3.1.2).
atrisk = {('5.10',448),('5.10',562),('5.10',625),('6.1',533),('6.2',264),('6.2',573),('6.2',595)}
seen=set(); fails=[]
for line in open('spec_refs_postcut.jsonl', encoding='utf-8'):
    line=line.strip()
    if not line: continue
    try: r=json.loads(line)
    except: continue
    if r.get('summary'): continue
    tf=(r.get('target_file_resolved') or r.get('target_file_cited') or '')
    if 'MAJOR_PLINY' not in tf: continue
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
**Pass:** all 7 at-risk MAJOR_PLINY refs (§5.10×3, §6.1, §6.2×3) still resolve PASS post-cut (the stub heading lines for §5.10/§6.2 + the live §6.1 heading resolve them) AND none is missing from the resolver output. **Falsifies if:** any at-risk ref FAILs (a stub did not preserve that subsection heading line — the Arc-47-r1-class regression) OR an at-risk ref is absent (the stub heading shape doesn't match the resolver's `_heading_pattern` — verify against the §2.7.1 literals). Note: the pre-existing `§N` FAIL at spec-L7 is NOT in the at-risk set (reading-note prose; FAILs pre- and post-cut; not a regression).

### P-XREF — every MAJOR_PLINY §N cited from an active SUBSTRATE file resolves post-cut
```bash
grep -rhoE 'MAJOR_PLINY(\.md)? §[0-9]+(\.[0-9]+)*' substrate/ \
  --include='*.md' --include='*.sh' --include='*.py' \
  | grep -vE 'substrate/arcs/' | sed -E 's/MAJOR_PLINY(\.md)? §//' | sort -uV
# every distinct cited §N must resolve to a heading (live or stub):
for n in 5 5.8 5.9 5.9.4 5.10 6.1 6.2 7 7.2 8 9; do
  grep -qE "^(#+) §?${n//./\\.}( |\.|—|-|:)" substrate/MAJOR_PLINY.md && echo "OK §$n" || echo "MISSING §$n"
done
```
**Pass:** every cited §N (top-level + subsection) resolves to a heading line (live KEEP, live DUPLICATE-slim for §6.1, or stub heading). **Falsifies if:** any cited §N has no heading (caught more precisely for the 3 spec-cited ones by P-SPEC-XREF). (Note: §5/§7/§8/§9 are top-level KEEP sections — their `## N.` or `# N` headings resolve; §5.8/§5.9/§5.9.4 are stub heading lines.)

### P-C1 — C-1 content-check gate honored (LOST-CANON proof — sampled)
```bash
for id in stoa--bxx stoa--dyb stoa--fea stoa--14u stoa--nvl stoa--3cs stoa--ads stoa--f37 \
          stoa--bn8 stoa--s2p stoa--nax stoa--ioy stoa--ezj; do
  echo "=== $id ==="; bw show "$id" 2>&1 | head -25; done
```
**Pass:** each cited ticket's body materially carries the N=1 story / empirical the deleted inline prose held. **Falsifies if:** any cited ticket is a thin stub not carrying the deleted detail → that deletion dropped canon, classification should have been C-2.

### P-C2 — C-2 archive-first executed BEFORE deletion, in a DEDICATED CHILD TICKET (1 firm: §5.4)
```bash
bw list --all 2>&1 | grep -E 'xyb\.10\.[0-9]'
bw show <child-id-for-§5.4> 2>&1 | grep -iE 'venv|pip install -e|per-worktree|editable|ariadne--b93'
grep -nE 'stoa--xyb\.10\.[0-9]' substrate/modules/per-worktree-venv.md substrate/MAJOR_PLINY.md
```
**Pass:** the §5.4 C-2 child ticket exists (parent = stoa--xyb.10), its description carries the verbose per-worktree-venv provenance + the `ariadne--b93` origin note, and the module's Anchor cites the correct child id. **Falsifies if:** the §5.4 verbose block is gone from source AND not present in a child-ticket description (LOST CANON), OR the cite-back id does not match the created ticket.

### P-SPLIT — SPLIT LIVE cross-refs preserved inline; PROVENANCE folded into Anchors
```bash
grep -nE 'MAJOR_POLYBIUS\.md §13|operating-disciplines\.md §10|operating-disciplines\.md §19|MAJOR_POLYBIUS\.md §4\.3\.1|operating-disciplines\.md §6\.7\.1' substrate/MAJOR_PLINY.md
grep -nE 'Anchor.*stoa--ioy' substrate/MAJOR_PLINY.md   # §7.2 fold
grep -nE 'Anchor.*stoa--nax' substrate/MAJOR_PLINY.md   # §7.8 fold
```
**Pass:** every §3.6 LIVE pointer resolves in the slim core; the PROVENANCE bw-ids appear in the §N Anchor lines (folded). **Falsifies if:** any §3.6 LIVE pointer is missing, OR a PROVENANCE bw-id is still a standalone cross-ref bullet.

### P-ROUTING-INDEX — the routing map AND relocation index exist, are always-loaded core, cover every relocation
```bash
grep -nE 'Routing map' substrate/MAJOR_PLINY.md          # orchestrator → routing map PRESENT (unlike op-disc)
grep -nE 'Relocation index' substrate/MAJOR_PLINY.md     # relocation index PRESENT
grep -nE '^### 4\.2 ' substrate/MAJOR_PLINY.md           # §4.2 home present
for m in ada-brief-preamble sub-agent-watchdog background-dispatch-hygiene pre-branch-hygiene \
         arc-close-hygiene seat-identity-brief pliny-polling-pattern post-strabo-vera \
         incomplete-unverifiable-routing smoke-beat-deploy-check per-worktree-venv; do
  grep -q "$m" substrate/MAJOR_PLINY.md && echo "OK routing/index: $m" || echo "MISSING: $m"
done
```
**Pass:** §4.2 present; a Routing map AND a Relocation index both present (MAJOR_PLINY is an orchestrator → BOTH, per assumption 1 / modules/README.md §4); every CONDITIONAL module appears in a routing-map row + an index row. **Falsifies if:** the routing map is absent (wrong shape for an orchestrator file — assumption 1), OR the relocation index is absent, OR a relocation has no index row.

### P-LYW — the stoa--lyw INVOCATION fold landed (separable slice)
```bash
grep -nE '^### 4\.1 ' substrate/MAJOR_PLINY.md
grep -qiE '/resume.*spawn.fresh|successor.decides' substrate/MAJOR_PLINY.md && echo "OK §4.1 decision rule" || echo "DROPPED decision rule"
grep -qiE 'stale.*id|fall.through|truncation' substrate/MAJOR_PLINY.md && echo "OK stale-id fall-through" || echo "DROPPED stale-id"
grep -qiE 'reverse chronological|multi-generation' substrate/MAJOR_PLINY.md && echo "OK multi-gen nav" || echo "DROPPED multi-gen"
grep -qE 'Anchor: stoa--lyw' substrate/MAJOR_PLINY.md && echo "OK lyw anchor" || echo "DROPPED lyw anchor"
```
**Pass:** §4.1 present with the `/resume`-vs-spawn-fresh decision rule + stale-id fall-through + multi-generation navigation + `Anchor: stoa--lyw`. **Falsifies if:** any of the four lyw load-bearing elements is absent (the lyw slice is incomplete — falsifiable independently of the cut, per the separable-slice requirement).

### P-RECOMPOSE — subproject recompose completeness for MAJOR_PLINY (THE LOST-CANON-at-subproject probe)
Run on a THROWAWAY subproject deploy (per op-disc §25.5: synthetic parent under a tmp path or `git clone --no-local`; do NOT mutate any operator-owned workspace):
```bash
TMP=$(mktemp -d); mkdir -p "$TMP/myproj"
bash substrate/install.sh --target subproject --parent-dir "$TMP" --subproject myproj
# MAJOR_PLINY deploys SUFFIXED at subproject tier (install.sh L819):
RECOMPOSED="$TMP/myproj/.claude/MAJOR_PLINY_myproj.md"

# (a) The 11 PLINY PAIRED markers SURVIVE, each enclosing a NON-EMPTY body:
grep -cE '^<!-- MODULE-INLINE:' "$RECOMPOSED"     # expect 11 PLINY opens
grep -cE '^<!-- /MODULE-INLINE:' "$RECOMPOSED"    # expect 11 PLINY closes
grep -Pzo '(?m)^<!-- MODULE-INLINE:[^\n]*-->\n<!-- /MODULE-INLINE:' "$RECOMPOSED" && echo "FAIL empty pair" || echo "OK no empty pairs"

# (b) EVERY PLINY module body is present (assert each module's first-heading line appears):
for m in ada-brief-preamble sub-agent-watchdog per-worktree-venv post-strabo-vera \
         incomplete-unverifiable-routing smoke-beat-deploy-check background-dispatch-hygiene \
         pre-branch-hygiene arc-close-hygiene seat-identity-brief pliny-polling-pattern; do
  head1=$(head -1 "substrate/modules/$m.md")
  grep -Fq "$head1" "$RECOMPOSED" && echo "OK body present: $m" || echo "MISSING body: $m"
done

# (c) recomposed subproject MAJOR_PLINY is canon-equivalent to full content (NOT the slim band):
wc -l "$RECOMPOSED"   # expect ~800+ (the 11 bodies re-inlined), NOT the ~250-330 slim band

# (d) POLYBIUS + op-disc recompose STILL pass (the third owner-set did not break Arc 45/47):
grep -cE '^<!-- MODULE-INLINE:' "$TMP/myproj/.claude/MAJOR_POLYBIUS_myproj.md"   # expect 5 (Arc-45 markers intact)
grep -cE '^<!-- MODULE-INLINE:' "$TMP/myproj/.claude/operating-disciplines.md"   # expect 12 (Arc-47 markers intact)
```
**Pass:** (a) all 11 PLINY paired markers survive + NO empty pair; (b) all 11 PLINY module first-heading lines appear; (c) recomposed MAJOR_PLINY in the FULL band (~800+); (d) POLYBIUS recompose still inlines its 5 AND op-disc its 12. **Falsifies if:** any PLINY marker pair empty (body dropped → LOST CANON at subproject tier), OR < 11 PLINY markers survive, OR any PLINY body absent, OR recomposed MAJOR_PLINY still in the slim band (recompose silently no-op'd), OR POLYBIUS/op-disc recompose broke (third-owner regression).

### P-RECOMPOSE-NEG — FAIL-LOUD asserted (losslessness depends on the err() firing)
```bash
mv substrate/modules/background-dispatch-hygiene.md substrate/modules/background-dispatch-hygiene.md.bak
bash substrate/install.sh --target subproject --parent-dir "$TMP" --subproject myproj2; echo "exit=$?"
mv substrate/modules/background-dispatch-hygiene.md.bak substrate/modules/background-dispatch-hygiene.md
```
**Pass:** install.sh exits NON-ZERO with a clear Check-A `marker MODULE-INLINE:background-dispatch-hygiene has no module source` error AND does NOT write a partial/slim MAJOR_PLINY to the subproject. **Falsifies if:** exit 0 (silent partial deploy — the LOST-CANON-at-subproject failure). NOTE: because Check A tests the GLOBAL existence set (Arc-47 r3), this fires correctly regardless of which owner's recompose call hits the missing module first.

### P-OWNERSHIP — the THREE-owner partition is correct (no cross-owner Check-B false-positive)
```bash
bash substrate/install.sh --target subproject --parent-dir "$TMP" --subproject myproj3; echo "exit=$?"
```
**Pass:** exit 0 — all three recompose calls pass: POLYBIUS scoped to its 5 (does not trip Check B on op-disc's 12 or PLINY's 11); op-disc scoped to its 12; PLINY scoped to its 11 (does not trip Check B on POLYBIUS's 5 or op-disc's 12). **Falsifies if:** exit 2 with a Check-B `module X.md exists but no MODULE-INLINE:X marker` error — the owned-set partition was mis-applied (e.g., PLINY's call passed the wrong owned-set, or the global glob leaked into Checks B/D).

### P-OWNERSHIP-NOCOLLIDE — no module basename collides across the three owner-sets (NEW this arc)
```bash
python3 - <<'PY'
poly="onboarding sub-project-spawning pair-programmer-authoring pair-programming-prototyping substrate-update-check".split()
opd="two-polybius-coordination autonomous-mode-setup sub-agent-transcript-discipline bw-fit-matrix oss-dep-and-latency credential-discipline-detail bw-upgrade mechanical-inspection-split multi-team-interop four-layer-identity substrate-component-design jsdom-timing-discipline".split()
pliny="ada-brief-preamble sub-agent-watchdog per-worktree-venv post-strabo-vera incomplete-unverifiable-routing smoke-beat-deploy-check background-dispatch-hygiene pre-branch-hygiene arc-close-hygiene seat-identity-brief pliny-polling-pattern".split()
allm = poly+opd+pliny
dupes = {m for m in allm if allm.count(m) > 1}
print("TOTAL basenames:", len(allm), "DISTINCT:", len(set(allm)))
print("COLLISIONS:", sorted(dupes))
print("RESULT:", "PASS" if not dupes else "FAIL")
PY
# AND assert the three owned-set vars in install.sh have no overlap:
grep -nE 'POLYBIUS_MODULES=|OPDISC_MODULES=|PLINY_MODULES=' substrate/install.sh
```
**Pass:** zero collisions across the 28 basenames; install.sh defines all three owned-set vars distinctly. **Falsifies if:** any basename appears in two owner-sets (a marker would be ambiguously owned; Check-B/D semantics would be wrong for the colliding module) — the NEW failure surface the third owner introduces (§2.7.2 obligation c).

### P-AUTH — no author-field regression (CLAUDE.md authorship discipline)
```bash
grep -niE '^(author|owner|creator|by|copyright|maintainer):' substrate/MAJOR_PLINY.md substrate/modules/ada-brief-preamble.md substrate/modules/sub-agent-watchdog.md substrate/modules/per-worktree-venv.md substrate/modules/post-strabo-vera.md substrate/modules/incomplete-unverifiable-routing.md substrate/modules/smoke-beat-deploy-check.md substrate/modules/background-dispatch-hygiene.md substrate/modules/pre-branch-hygiene.md substrate/modules/arc-close-hygiene.md substrate/modules/seat-identity-brief.md substrate/modules/pliny-polling-pattern.md
```
**Pass:** no author-like field names anyone other than Denson Smith (MAJOR_PLINY carries none; the 11 new modules carry none). **Falsifies if:** any new module's provenance header introduces an author field.

### P-KEEP — the always-on KEEP rules are still inline (orchestrator availability-losslessness)
```bash
grep -qiE 'runs structured pipelines and dispatches CAPTAINs|you run the team' substrate/MAJOR_PLINY.md && echo "OK §1 what-you-are" || echo "DROPPED §1"
grep -qiE 'do not converse with the PRINCIPAL directly' substrate/MAJOR_PLINY.md && echo "OK §3 don'ts" || echo "DROPPED §3"
grep -qiE 'DAEDALUS|ARGUS|ADA|VERA|CATO' substrate/MAJOR_PLINY.md && echo "OK §5 gauntlet diagram" || echo "DROPPED §5 pipeline"
grep -qiE 'operating-mode' substrate/MAJOR_PLINY.md && echo "OK §5.1 mode rule" || echo "DROPPED §5.1"
grep -qiE 'verify-then-execute|directive that contradicts the spec' substrate/MAJOR_PLINY.md && echo "OK §7.2 verify-then-execute" || echo "DROPPED §7.2"
grep -qiE 'One job per agent' substrate/MAJOR_PLINY.md && echo "OK §7.1 one-job" || echo "DROPPED §7.1"
grep -qiE 'clean PASS|autonomous.ship' substrate/MAJOR_PLINY.md && echo "OK §7.4 autonomous-ship" || echo "DROPPED §7.4"
grep -qiE 'bundle.*disjoint|surface-disjointness' substrate/MAJOR_PLINY.md && echo "OK §6.3 bundle-shape" || echo "DROPPED §6.3"
grep -qiE 'bw prime' substrate/MAJOR_PLINY.md && echo "OK §6.1 slim residue (bw prime)" || echo "DROPPED §6.1 residue"
grep -qiE 'Activation checklist|one-page summary' substrate/MAJOR_PLINY.md && echo "OK §9 checklist" || echo "DROPPED §9"
```
**Pass:** all always-on KEEP rules resolve inline. **Falsifies if:** any always-on orchestrator rule was relocated off-disk (availability-losslessness violated).

---

## §5 — Build steps (for ADA — ordered; the cut sequence)

**Step 0 (process hazard — DO THIS FIRST).** Confirm cwd is the worktree (`git -C C:/Users/denso/claude_projects/the-stoa/.claude/worktrees/arc-48-build rev-parse --show-toplevel` resolves to the worktree, branch `arc-48/build`). Use ABSOLUTE worktree paths for EVERY Write. After each write, verify it landed in the worktree (`git -C <worktree> status`) and NOT in main (`git -C C:/Users/denso/claude_projects/the-stoa status` should NOT show your edit). The Write-resolves-against-main-root hazard hit prior arcs; this gate catches it before it compounds.

1. **Create the 11 module files** (`substrate/modules/*.md`), populating from the live source line-ranges in §2.3 / §3.2. Each module: stable `# <Title>` first line (P-RECOMPOSE keys on it) → provenance header (cites this design + stoa--xyb epic, mirroring the Arc-47 modules) → relocated content verbatim-tightened, INCLUDING the section's own cross-refs + the compressed `Anchor:` for any move-with provenance (§3.3). Run op-disc §33 per-module line-count discipline. NO author field (P-AUTH). **Verify NO basename collision** with the 17 existing modules (P-OWNERSHIP-NOCOLLIDE — the 11 are disjoint per §3.8).
2. **Execute the C-2 archive-first as a DEDICATED CHILD TICKET** (§3.4): `bw create "Arc 48 C-2 archive: §5.4 per-worktree-venv reflex provenance (orig ariadne--b93)" --parent stoa--xyb.10 -d "<verbose §5.4 prose + ariadne--b93 origin note>"`, BEFORE touching the source. Record the assigned child id. `bw show <child-id>` content-check. Write the module's Anchor cite-back using the ACTUAL id.
3. **Cut the slim core** (`substrate/MAJOR_PLINY.md`):
   - **ADD §4.1 (the lyw lean fold)** per §1A.3 (the literal). ADD `Anchor: stoa--lyw`.
   - **ADD §4.2 (the routing map + relocation index)** per §2.2. Populate the routing map from §3.2's beat column; populate the relocation index from §3.2 + §3.3 + §3.4 + §3.5. **MAJOR_PLINY gets BOTH tables** (orchestrator — P-ROUTING-INDEX asserts both present).
   - For the top-level-only CONDITIONAL sections (§5.3/§5.4/§5.5/§5.6/§5.7/§5.8/§5.12), replace the body with the §2.7.1-class-1 stub + paired `<!-- MODULE-INLINE:<name> -->` … `<!-- /MODULE-INLINE:<name> -->` marker.
   - For §5.2 (+§5.2.1), single §5.2 stub naming §5.2.1 in prose + marker (`ada-brief-preamble`).
   - For §5.9 + §5.9.4 (combined module), keep `### 5.9` AND `### 5.9.4` as REAL HEADING LINES (substrate-cited) + one marker (`pre-branch-hygiene`) per §2.7.1-class-2.
   - For §5.10 + §5.11 (combined module), keep `### 5.10` (**spec-cited — real heading line**) AND `### 5.11` heading lines + one marker (`arc-close-hygiene`) per §2.7.1-class-2.
   - **For §6.2 (spec-cited):** keep `### 6.2` as a REAL HEADING LINE stub (names the anti-pattern in one prose line) + marker (`pliny-polling-pattern`) per the §2.7.1 §6.2 literal. (§6.2a co-locates in the module.)
   - **For §6.1 (DUPLICATE-slim, spec-cited):** do NOT stub it. Keep `### 6.1` LIVE; DELETE the `-m`-isn't-real table + per-subcommand syntax table; KEEP the `bw prime` reflex + CAPTAIN_TIRO delegation + the SPECIFICATION.md cite-marker; ADD a one-line pointer to op-disc §12 for syntax fundamentals. NO marker (body consolidates to the EXISTING op-disc §12 home, not a PLINY module).
   - KEEP-TIGHTEN §1/§2/§3/§4/§5-preamble/§5.1/§6-channel-table/§6.3/§7.1–§7.8/§8/§9 (§3.7). For each standalone C-1 PROVENANCE row (§3.3 — 10 rows), run the `bw show` content-check (gate) THEN delete-to-Anchor. For each SPLIT cross-ref tail (§3.6 — 3 tails), keep LIVE pointers inline verbatim, fold the trailing empirical/ticket lines into the §N Anchor.
4. **Add the install.sh PLINY owned-set + recompose call** (§6 — substrate-tooling source, gauntlet-gated, correctly inside this arc):
   - Add `PLINY_MODULES="ada-brief-preamble sub-agent-watchdog per-worktree-venv post-strabo-vera incomplete-unverifiable-routing smoke-beat-deploy-check background-dispatch-hygiene pre-branch-hygiene arc-close-hygiene seat-identity-brief pliny-polling-pattern"` next to `POLYBIUS_MODULES`/`OPDISC_MODULES` (L1002–1003).
   - Replace the L1006–1008 forward-note comment with `recompose_module_inline "$DEST_PLINY" "$PLINY_MODULES"`.
   - **NO function-body change** — the two-set machinery (Arc 47) handles the third owner unchanged. Update the L887–892 + L1000–1001 comments to say THREE files now recompose.
   - Smoke-test against a throwaway synthetic parent (P-RECOMPOSE + P-RECOMPOSE-NEG + P-OWNERSHIP + P-OWNERSHIP-NOCOLLIDE) before considering the step done.
5. **Cross-ref re-point sweep** (verification, not churn — numbers preserved): run P-XREF + **P-SPEC-XREF** (the validate-spec resolver against SPECIFICATION.md). Confirm every active-file cite + all 7 at-risk SPECIFICATION.md MAJOR_PLINY cites (§5.10×3, §6.1, §6.2×3) still resolve.
6. **Run all probes** (P-FLOOR, P-COND, P-STUB, P-SPEC-XREF, P-XREF, P-C1, P-C2, P-SPLIT, P-ROUTING-INDEX, P-LYW, P-RECOMPOSE, P-RECOMPOSE-NEG, P-OWNERSHIP, P-OWNERSHIP-NOCOLLIDE, P-AUTH, P-KEEP) as a self-check before returning to PLINY. Clean up any temp files (`spec_refs_postcut.jsonl`, recompose `.bak`s, `$TMP`).
7. **Commit** with `Co-Authored-By: CAPTAIN_ADA_the-stoa <captain-ada@the-stoa.local>` per op-disc §28. (The slim-core cut + the 11 modules + the §4.1 lyw fold + the install.sh PLINY owned-set land as one coherent commit, or the install.sh extension as a trailing commit if ADA prefers a clean tooling/canon split — ADA's call; both are this arc. The lyw fold is a SEPARABLE slice for ARGUS audit but need not be a separate commit.)

---

## §6 — install.sh PLINY owned-set + recompose (the minimal tooling extension Arc 47 designed for)

### 6.1 Why MAJOR_PLINY recompose is required (orchestrator losslessness at subproject tier)

MAJOR_PLINY deploys at all 3 tiers (install.sh L817–852), suffixed at subproject (`MAJOR_PLINY_<subproject>.md`, L819). At subproject tier `DEST_MODULES_DIR=""` (no modules deployed) AND a subproject seat's `Read .claude/modules/X.md` does not resolve reliably (the Arc-45 probe finding). So a slim subproject MAJOR_PLINY pointing at 11 modules absent from the subproject's `.claude/` would break losslessness for the orchestrator seat at that tier. The fix is the same recompose-inline POLYBIUS + op-disc use: re-inline the 11 module bodies at their markers at subproject tier. The mechanism (`recompose_module_inline()`, the awk state-machine, the 5 FAIL-LOUD checks A–E, idempotency, the two-set partition) ALREADY EXISTS (Arc 45 + Arc 47, install.sh L894–998) — this arc REUSES it with a third call.

### 6.2 MAJOR_PLINY is `sed`'d ({{NAME_SUFFIX}}), not `cp`'d — recompose runs cleanly on it

MAJOR_PLINY gets a `sed` substitution of `{{NAME_SUFFIX}}` (L849; today a no-op — the source has no placeholder, but the substitution path exists defensively). The recompose runs IN PLACE on the deployed `$DEST_PLINY` regardless. The markers are inert through the sed (the sed substitutes only `{{NAME_SUFFIX}}`, which appears in no marker). `$DEST_PLINY` is written at L849 (BEFORE the L893 recompose block), so it exists when the recompose runs — no reordering needed (unlike op-disc, which Arc 47 deliberately moved before the recompose block; MAJOR_PLINY is already deployed at L849, well before L893).

### 6.3 The slim-core clause that makes the strategy auditable (mirrors Arc-45/Arc-47 §6.3)

The slim core's §4.2 (or a one-line note near the routing map) carries the tier-awareness rule so the strategy is visible to a reader, not buried in install.sh:

> **Subproject-tier module access (per design-arc-48 §6):** at subproject tier the CONDITIONAL module content is re-inlined into this file at deploy time (install.sh recompose at the `<!-- MODULE-INLINE:<name> -->` markers) — subproject seats do NOT `Read .claude/modules/<X>.md` (the path does not resolve reliably; claude-code #56686/#31546/#29423). At user/project tier the `Read` channel applies and the markers are inert. Anchor: stoa--xyb + design-arc-45 §6 probe (the proven mechanism this arc extends to MAJOR_PLINY).

### 6.4 The THIRD owned-set — exact change (the minimal extension; NO function-body change)

The current function (L894–998) already takes `(role_file, owned_basenames)` and runs the two-set awk (Arc 47 r3). The ONLY changes:

**Add the PLINY owned-set + the third call (replacing the L1006–1008 forward-note):**
```bash
POLYBIUS_MODULES="onboarding sub-project-spawning pair-programmer-authoring pair-programming-prototyping substrate-update-check"
OPDISC_MODULES="two-polybius-coordination autonomous-mode-setup sub-agent-transcript-discipline bw-fit-matrix oss-dep-and-latency credential-discipline-detail bw-upgrade mechanical-inspection-split multi-team-interop four-layer-identity substrate-component-design jsdom-timing-discipline"
PLINY_MODULES="ada-brief-preamble sub-agent-watchdog per-worktree-venv post-strabo-vera incomplete-unverifiable-routing smoke-beat-deploy-check background-dispatch-hygiene pre-branch-hygiene arc-close-hygiene seat-identity-brief pliny-polling-pattern"
recompose_module_inline "$DEST_POLYBIUS" "$POLYBIUS_MODULES"
recompose_module_inline "$DEST_OPERATING_DISCIPLINES" "$OPDISC_MODULES"
recompose_module_inline "$DEST_PLINY" "$PLINY_MODULES"
```

**Key precision (the two-set discipline HOLDS for the third owner):**
- **Check A** still tests `name in global_exists` — the GLOBAL set, now 28 module sources (5 + 12 + 11) minus README. A PLINY marker naming any real module resolves; a marker naming a non-existent module FAILs loudly (P-RECOMPOSE-NEG). Owner-agnostic; does NOT narrow with the PLINY owned-set.
- **Checks B/D** iterate/count the PLINY `owned[]`/`nowned` for the `$DEST_PLINY` call. A cross-owner module (op-disc's `autonomous-mode-setup` during PLINY recompose) is not in PLINY's `owned[]`, so Check B does not flag it (P-OWNERSHIP).
- **NO basename collision across the three owner-sets** (P-OWNERSHIP-NOCOLLIDE) — this is the ONE new obligation the third owner introduces. With three owner-sets sharing one `substrate/modules/` dir, a basename present in two owned-set vars would be ambiguously owned (both calls would expect a marker for it, but only the file that authored the marker has one → the other call's Check B would false-fail). The 11 PLINY basenames are disjoint from the 17 existing (§3.8); P-OWNERSHIP-NOCOLLIDE asserts this mechanically as a build-time guard.

**Why this is the minimal correct extension:** the Arc-47 design's "data-driven property" claim is realized exactly here — the PLINY cut adds a `PLINY_MODULES` var + a third call, with ZERO new code path in the function. (Arc 47 left the explicit forward-note for this; this arc executes it.)

### 6.5 Recompose placement + the dry-run path

The third call goes in the SAME `if [ "$TARGET" = "subproject" ]` block as the existing two (after L1005). `$DEST_PLINY` is written at L849, well before the L893 block — so no reordering is needed (contrast op-disc, which Arc 47 moved before the block). The function's existing `$DRY_RUN` guard (L922–925) prints the plan and returns without requiring the file to exist — works unchanged for the third call (it prints `owned:${_owned_basenames}` = the PLINY owned-set). The dry-run plan now shows all THREE owned-sets. FAIL-LOUD semantics (rm-both-files-on-error, L988–994) apply per-call: a PLINY recompose failure removes the partial PLINY tmp AND the slim `$DEST_PLINY`, exits 2, aborts the deploy — install.sh never ships a partial/slim MAJOR_PLINY to a subproject (P-RECOMPOSE-NEG).

### 6.6 Check E (body-contains-a-marker) interaction with MAJOR_PLINY content

Check E (L962) fails if a module BODY contains a literal `<!-- MODULE-INLINE: -->` line (would corrupt recompose). **One caveat for ADA, load-bearing for THIS file:** the §5.8 source (→ `background-dispatch-hygiene.md`) contains the canonical bw-poll-loop template AND the §5.8.2 dispatch pseudocode, which include the literal strings `<task-notification>` and `Monitor({...})` and `<!-- ... -->`-shaped comments? — **VERIFY at build time:** §5.8's body must contain ZERO literal `^<!-- /?MODULE-INLINE:` lines (Check E only matches that exact full-line shape). The §5.8 source uses `<dispatch-ticket>`, `<id>`, `<CAPTAIN>` placeholder shapes and fenced ```` ```bash ```` blocks — none is a `MODULE-INLINE` marker line. The §5.2 ADA-brief preamble (→ `ada-brief-preamble.md`) contains a blockquoted literal with `> Ground-check every concrete example` — no marker. Confirm none of the 11 module bodies carries a literal `MODULE-INLINE` line (Check E catches any ADA-introduced one at deploy; P-RECOMPOSE exercises the happy path).

---

## §7 — Self-assessed weak points (esp. anywhere losslessness is at risk for the orchestrator seat)

1. **The orchestrator-gets-routing-map call (assumption 1) is a DIVERGENCE from the freshest proven pattern (Arc 47 dropped the routing map).** Arc 47 deliberately gave op-disc ONLY a relocation index because op-disc dispatches nothing; this design RESTORES the routing map for MAJOR_PLINY because PLINY IS the dispatcher. *Why this shape anyway:* the routing map is, by modules/README.md §4.1's own definition, an ORCHESTRATOR artifact ("at dispatch time, what does this task need?") — and Arc 45 (the POLYBIUS cut, also an orchestrator) shipped both tables. PLINY's CONDITIONAL modules are beat-triggered at dispatch beats the orchestrator controls (ADA dispatch, `run_in_background` fire, arc close), so a beat→module routing map is exactly the dispatch-time index the orchestrator consults. Dropping it would lose the orchestrator's "at this beat, load this module" guidance and force PLINY to rediscover the beat→module mapping from the per-stub pointers each time. P-ROUTING-INDEX asserts BOTH tables present. The residual risk is that ARGUS may prefer the leaner op-disc shape (index-only) — but op-disc is a non-orchestrator and PLINY is an orchestrator, so the Arc-45 precedent (not the Arc-47 one) governs. Surfaced as residual Q1; this is the single most important structural call.

2. **§6.1 is split DUPLICATE-body / KEEP-heading — an unusual hybrid disposition that ADA could mis-execute by either over-deleting (dropping the spec-cited heading or the PLINY-framing residue) or under-deleting (leaving the duplicated cookbook tables).** §6.1 is the only section in this cut that is neither a clean CONDITIONAL relocation nor a clean KEEP: its BODY (the cookbook tables) is DUPLICATE (consolidate to op-disc §12), but its HEADING is spec-cited (must stay live) and it carries PLINY-framing residue that is NOT in §12 (the `bw prime` reflex, the TIRO delegation). *Why this shape anyway:* the modules/README.md §5.3 worked example explicitly names this exact consolidation (`MAJOR_PLINY.md §6.1` → op-disc §12), so the DUPLICATE classification is canon-directed, not invented; and the spec-cite (L533) + the non-duplicated residue forbid a clean whole-section relocation. P-SPEC-XREF (asserts §6.1 stays PASS), P-STUB (asserts §6.1 stays LIVE not stubbed), and P-KEEP (asserts the `bw prime` residue survives) together exercise the three ways ADA could mis-execute. The residual risk is ADA's judgment on exactly which lines are "PLINY-framing residue" vs "duplicated table" — §3.5 + §2.5 enumerate it (keep 592/618 + the §12 pointer; delete 594–614), but it is the least mechanical deletion in the cut.

3. **§5.8 is the largest relocation (~103 lines) AND contains the canonical bw-poll-loop template that op-disc §18 cites as "canonical inline" — relocating it changes the canonical home from MAJOR_PLINY §5.8 to a module, leaving op-disc §18 L662's "(canonical inline)" parenthetical slightly stale.** *Why this shape anyway:* §5.8 fires only on a `run_in_background` Agent dispatch (passes the conditional test cleanly), and the template moves intact to the module (lossless — re-inlined at subproject tier; Read-accessible at user/project tier); op-disc §18's cite is top-level §5.8 → resolves to the stub → points to the module, so the cite is NOT broken. The "(canonical inline)" wording is now a one-word imprecision (the canonical copy is in the module), but it still RESOLVES correctly and is not a cut regression. I deliberately did NOT action the op-disc §18 wording fix (it would expand scope into op-disc, which this arc does not touch) — flagged as a one-line follow-up (§9) for the capstone or a future op-disc touch. The residual risk is a reader interpreting "(canonical inline)" literally and looking for the template inline in the §5.8 stub; the §5.8 stub's framing line ("the canonical bw-poll-loop template now lives in `background-dispatch-hygiene.md`") mitigates this at the point of confusion.

4. **The estimated floor (~250–330) is the most aggressive of the three cuts relative to source size (801→~290 ≈ 64% reduction vs op-disc's ~58% and POLYBIUS's ~55%) — a reviewer may read it as "cut too deep / a KEEP rule was dropped."** *Why this shape anyway:* MAJOR_PLINY's always-on core is genuinely small (the orchestrator's job is to dispatch + route; the BEAT-specific procedures that bulk out §5 are exactly the CONDITIONAL content the composition layer is designed to relocate), so a deep reduction is the honest output, not over-cutting. P-KEEP independently asserts each load-bearing always-on rule (what-you-are, the gauntlet diagram, operating-mode, verify-then-execute, one-job, autonomous-ship, bundle-shape, the §6.1 `bw prime` residue, the checklist) is still inline; P-FLOOR guards the low end (< 200 = suspicious). The floor is whatever the always-on orchestrator core weighs (recalibrated criterion). The reduction being larger than the prior two cuts is a property of THIS file's CONDITIONAL/always-on ratio, not of over-aggression.

5. **The lyw §4.1 fold places the `/resume` INVOCATION discipline in the always-on §4 (Activation) rather than a CONDITIONAL module — if ARGUS judges it CONDITIONAL, it would belong in a `resume-invocation.md` module + a routing-map row, not inline.** *Why this shape anyway:* the `/resume`-vs-spawn-fresh decision is made at EVERY successor activation, so by the ambient-vs-conditional test it is KEEP (always-on) — and a module the successor must know to Read at activation has the same bootstrap problem the §4 activation checklist solves (the successor reads §4 to learn how to activate; it cannot first read a module to learn whether to `/resume`). Keeping it lean (~22 lines, decision-rule-not-essay) honors the debloat thesis while keeping it inline. The residual risk is a borderline ambient-vs-conditional call (it fires at activation, which is arguably "a specific beat" not "every turn") — but activation is the universal entry beat, and the decision gates whether the session even continues a lineage, so I judge it always-on. Surfaced as residual Q4; the lyw slice is independently falsifiable (P-LYW) regardless of placement, so a placement flip is a localized change.

---

## §8 — Residual questions for ARGUS

1. **The orchestrator-gets-BOTH-tables call (assumption 1; weak point 1).** Does ARGUS concur that MAJOR_PLINY (an orchestrator) gets BOTH a routing map AND a relocation index (the Arc-45 POLYBIUS shape), diverging from Arc-47's index-only op-disc shape — because op-disc dispatches nothing and PLINY IS the dispatcher? Or does ARGUS prefer the leaner index-only shape with per-stub `Read` pointers carrying all the dispatch-time signal? I judge BOTH-tables is correct per modules/README.md §4.1's orchestrator framing + the Arc-45 precedent, but it is the load-bearing structural divergence.

2. **The §6.1 DUPLICATE-body / KEEP-heading hybrid (weak point 2).** Does ARGUS concur §6.1's cookbook TABLES are DUPLICATE (consolidate to op-disc §12 per modules/README.md §5.3's named worked example) while §6.1's HEADING stays live (spec-cited L533) and the PLINY-framing residue (`bw prime`, TIRO delegation) stays? Or should §6.1 be a fuller KEEP (the tables are PLINY-seat-convenience worth keeping inline despite the §12 duplication)? I judge DUPLICATE-with-residue because README §5.3 explicitly names this consolidation.

3. **The §5.4 C-2 disposition (weak point / §3.4).** §5.4's only provenance anchor is the cross-repo `ariadne--b93` (no `stoa--` mirror, does not resolve in the-stoa bw). I classified it C-2 (archive to a `stoa--xyb.10.N` child ticket) rather than a bare cross-repo `Anchor: ariadne--b93` (which would be unrecoverable from this bw). Does ARGUS concur C-2-child is right when there is NO `stoa--` co-anchor to fold the cross-repo id into (unlike Arc-47's cross-repo folds, which always had a `stoa--` primary)?

4. **The lyw §4.1 placement: always-on §4 vs a CONDITIONAL module (weak point 5).** Does ARGUS concur the `/resume` INVOCATION discipline is KEEP-always-on in §4 (Activation) — because the decision fires at every successor activation and a module-the-successor-must-Read-at-activation has a bootstrap problem? Or is it CONDITIONAL (a `resume-invocation.md` module + routing-map row)? I judge always-on-lean; the slice is independently falsifiable either way (P-LYW).

5. **The third-owner NO-COLLIDE obligation (§6.4 obligation c / P-OWNERSHIP-NOCOLLIDE).** The third owner-set introduces the ONE genuinely new failure surface this cut adds beyond Arc 47: a basename present in two owner-set vars would be ambiguously owned. I added P-OWNERSHIP-NOCOLLIDE as a build-time mechanical guard (the 11 PLINY basenames are disjoint from the 17 existing). Does ARGUS concur this is the complete new failure surface, or is there a second three-owner interaction (e.g., the GLOBAL existence set now spanning three owners' worth of modules) I missed? I judge Check A is unaffected (it globs the filesystem, owner-count-agnostic), so NO-COLLIDE is the only new surface.

---

## §9 — Out of scope

- **Cutting any OTHER role file.** This arc cuts MAJOR_PLINY only. (The CAPTAIN role files + the remaining always-on prose-compression are the capstone block — stoa--xyb.9.)
- **Prose-compression of always-on KEEP sections (FLAGGED for stoa--xyb.9, NOT actioned here).** Per the dispatch, the cut is relocation-only; prose-compression of always-on KEEP sections happens in ONE reviewed capstone pass (.9) across all files. Candidates spotted in MAJOR_PLINY's KEEP sections, recommended for ADDITION to stoa--xyb.9: (a) **§5.1 operating-mode** — the two Arc-37 parenthetical cross-ref restatements (L112–114) are verbose-redundant with the §5.1 prose, losslessly compressible to one cross-ref line; (b) **§7.2 verify-then-execute** — the rule is sound but the THREE scope-broadening paragraphs (Arc-24, Arc-39 + the 3-shape failure-mode enumeration L714–728) are dense always-on prose that could tighten ~30% losslessly while keeping every sub-rule; (c) **§9 activation checklist** — overlaps §4's activation prose (the checklist re-states §4's steps); a losslessly-tightened §9 could cross-ref §4 rather than re-state. These are FLAGS for .9, NOT actioned in this cut.
- **The op-disc §18 L662 "(canonical inline)" wording staleness** (weak point 3). §5.8's relocation makes the canonical poll-loop home a module, not MAJOR_PLINY §5.8 inline. op-disc §18's cite still RESOLVES (top-level §5.8 → stub → module), so it is not a regression — but the parenthetical "(canonical inline)" is now imprecise. A one-line op-disc touch (`"(canonical home: background-dispatch-hygiene.md, re-inlined at subproject tier)"`) is the fix; flagged for the .9 capstone or a future op-disc touch, NOT actioned here (would expand scope into op-disc).
- **The op-disc + MAJOR_POLYBIUS framing of the `/resume` invocation discipline** (lyw sketched touch-points 1 + 2). This fold is PLINY-seat-scoped per the dispatch. If the op-disc universal-team framing or the POLYBIUS-seat framing is genuinely needed, it is a follow-up arc (a small lyw-completion arc) — NOT this cut. (lyw's sketch lists these; the dispatch scoped this arc to the PLINY-seat half.)
- **Substrate-self-apply re-sync** of the-stoa's deployed `.claude/MAJOR_PLINY.md` (lags source by this arc + Arc 44/45/46/47). User-tier POLYBIUS housekeeping per MAJOR_POLYBIUS §18.1.
- **Building the enforcement layer** (stoa--xyb.5). The routing-map + relocation-index + MODULE-INLINE marker formats are hook-parseable (designed so), but the hook is not built here.
- **Re-homing op-disc §12 (the bw cookbook keep-home) anywhere.** §6.1's tables consolidate INTO op-disc §12 (the keep-home stays where it is); §12 itself is untouched by this arc.

---

*Self-assessed weak points are in §7. Residual questions for ARGUS are in §8. The stoa--lyw lean fold is the separable slice in §1A (own design section) + §5 Step 3 (own build step) + P-LYW (own probe). This is rev1; ARGUS audits it next (LOST-CANON primary), then ADA reads THIS file to build.*
