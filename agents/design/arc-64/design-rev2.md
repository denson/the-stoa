# Arc 64 design-rev2 — skills-housekeeping pass B (verdict/spec/inspection skills → modules + save-verdict Bash-only rewrite)

Author: Denson Smith · Ticket: stoa--p41.2 (Workstream B) · Seat: CAPTAIN_DAEDALUS · Branch: arc-64/build

---

## 0. What rev2 is

rev2 is a **FOLD DELTA over design-rev1.md** (same directory). The floor-manager ADJUDICATED the design-lock: the CORE MECHANISMS are LOCKED and rev2 does NOT re-open them — bw attach (byte-durable, the Arc-62 fix), the Q-A bash assert with the `^[pP]` j2i-fix, the A3 / Q-B `7b1.1` reconciliation, Q-C = C2 (inline-fallback), and the §35.5 process-hardening carve-out. rev2 incorporates the eight adjudicated findings (r1/r2/r3/r4/r8 HIGH, r6/r7 LOW, r5/W2 LOCKED posture) plus the SKILL_NAMES count correction (9→6, not 10→7).

**Read rev1 for every section not named below.** rev1 §1 (problem restatement + imported assumptions A1/A2/A3), §2.1(a)–(d) core procedure, §2.2 wrapper-module shapes, §2.3 repoint, §2.4 7b1.1/Q-B/threat-map, §2.6 app-green mechanism, §2.7 Q-C=C2 rationale, §2.8 threat→mitigation map, §4 weak points, §5 out-of-scope all carry forward UNCHANGED except where a fold below amends them. This file states each amendment with its concrete edit site (file + line/section + the change) so ADA builds against rev2 without re-reading the lock thread.

This rev2 changes **no core mechanism.** Every fold is a coherence repair, a count fix, a tier-uniformity move of an already-locked assert, a clobber-guard, or a durability-contract documentation requirement. If any reviewer reads a core-mechanism change into the below, that is a defect in this prose, not an intended re-litigation — flag it.

---

## 1. Fold r1 + r2 (HIGH — install.sh: two operator-tool dirs must be carve-out-exempt)

**Problem (rev1 prose conflict).** rev1 §1/§2.2 asserted the operator-tool carve-out "already handles" the `validate-spec` / `inspect-script-output` dirs (L1289-1303), while §2.5 hedged "Verify the carve-out covers these two dirs; if it is an explicit list, add them." Ground truth (verified live): the carve-out IS an explicit by-name list (`CARVEOUT_SKILL_DIRS=(check-substrate-updates check-bw-release)` at `install.sh` L1297), and the prune-scan exemption is ALSO an explicit by-name case (`check-substrate-updates|check-bw-release) continue ;;` at L1780). Neither names the two dirs this arc retires-as-operator-tools. So the rev1 "already handles" claim is FALSE — left unfixed, the two retained script dirs (SKILL.md removed, `check.sh`/`_check_runner.py`/`_lib` kept) would be flagged obsolete by `--prune-obsolete` and DELETED in the same install run, and would not be deployed by the carve-out at all → silent operator-tool data-loss + a deploy gap at consumer workspaces.

**rev2 resolution — state it plainly: the build ADDS both dirs to BOTH lists.** No hedge. Concrete edit sites:

- **(a) Carve-out deploy list — `install.sh` L1297.**
  `CARVEOUT_SKILL_DIRS=(check-substrate-updates check-bw-release)`
  → `CARVEOUT_SKILL_DIRS=(check-substrate-updates check-bw-release validate-spec inspect-script-output)`
  Extend the L1285-1296 comment block with a one-line note that Arc 64 added the two verdict-pass-B operator tools by the same mechanism (SKILL.md removed, scripts retained).

- **(b) Prune-scan exemption case — `install.sh` L1780.**
  `      check-substrate-updates|check-bw-release) continue ;;`
  → `      check-substrate-updates|check-bw-release|validate-spec|inspect-script-output) continue ;;`
  Extend the L1771-1779 CITE comment to record the Arc-64 addition (same rationale: substrate-shipped non-skill operator tools, intentionally NOT in SKILL_NAMES, must not be prune-deleted in the run that the carve-out deploys them).

- **(c) `save-verdict` stays ABSENT from both lists.** `save-verdict` is fully `git rm`'d — the entire `substrate/skills/save-verdict/` dir (Python writer + `_lib` + `.gitignore` + SKILL.md) is removed (rev1 §1/§2.1). It is NOT an operator tool; it leaves no retained script. So it appears in NEITHER `CARVEOUT_SKILL_DIRS` NOR the prune-exemption case. The prune scan will not flag it (the dir is gone, not present-without-SKILL.md), so no exemption is needed or wanted.

**Amends rev1:** strike the "already handles (L1289-1303)" claims in rev1 §1, §2.2 (last paragraph), and the §2.5 "Verify … if it is an explicit list, add them" hedge. The carve-out does NOT already handle the two dirs; the build adds them, by name, to both the deploy list and the prune-exemption case.

---

## 2. Fold r3 (HIGH — stale canon + dangling pointer at operating-disciplines.md L590)

**Problem.** `operating-disciplines.md` L590 (the "Canonical write-path for INCOMPLETE + UNVERIFIABLE verdict bodies" paragraph, §15.4-adjacent) currently asserts: "The `save-verdict` skill (`substrate/skills/save-verdict/SKILL.md`) validates shape-conformance for both new verdict shapes before writing … Missing-required-field or out-of-enum cases exit 4 BEFORE any file write." After this arc the skill is deleted and §15.4 shape validation moves to SEAT-SIDE discipline (Q-A HYBRID, LOCKED) — so both the mechanism claim and the `skills/save-verdict/SKILL.md` pointer go stale (a dangling pointer to a deleted file + a false "the skill mechanically validates" assertion).

**rev2 resolution — reword L590 to match the Q-A HYBRID (LOCKED).** Concrete edit at `operating-disciplines.md` L590, replacing the paragraph body with prose that states:
1. **§15.4 shape validation is now SEAT-SIDE discipline** — the seat's verdict-format section in its role file is the SSoT for the required-field matrix (INCOMPLETE ⇒ `quadrant_classification` + `coverage_description`; UNVERIFIABLE ⇒ `quadrant_classification` + `sanity_check_performed` + `recommended_next_step`). There is no longer a pre-write mechanical exit-4 on shape; a malformed shape is caught by the seat following its role-file spec and by the downstream gauntlet (NOMOS / PLINY), consistent with Q-A HYBRID.
2. **The threat-coverage empty-binding check IS PRESERVED as a mechanical guard** — an inline bash assert (`^[pP]` regex, exit 4 when a threat-ratified mitigation is declared with no well-formed probe-id) that lives in BOTH the `save-verdict.md` module AND the role-file inline §7 block (see §4 r8 below). This is the one mechanical pre-write guard that survives.
3. **Drop the dead `skills/save-verdict/SKILL.md` pointer; point at `.claude/modules/save-verdict.md`** as the canonical write-path home. Keep the existing cross-ref to `CAPTAIN_VERA.md` / `CAPTAIN_CATO.md` / `CAPTAIN_ARGUS.md` §7 (those sections now carry the inline procedure + module pointer).

Keep the surrounding §15.4 prose (the UNVERIFIABLE/INCOMPLETE definitions, the field lists) intact — only the "Canonical write-path …" paragraph at L590 is reworded.

---

## 3. Fold r4 (HIGH — dangling pointer at MAJOR_PLINY.md §5.14)

**Problem.** `MAJOR_PLINY.md` §5.14 (L248-258, "Arc-worktree dest-pinning for save-verdict") ends: "The skill-side half of this fix is the tightened `cwd` contract in `substrate/skills/save-verdict/SKILL.md` (the skill writes where `--cwd` points; only the dispatcher knows which tree is correct)." After this arc there is no skill and no `--cwd` flag (the Bash module uses a worktree-relative path, not a `--cwd`-driven Python writer) — so that sentence dangles on a deleted file and references a contract that no longer exists.

**rev2 resolution — the worktree-dest-pin DISCIPLINE survives; only the skill-side `--cwd` sentence is rewritten.** Concrete edit at `MAJOR_PLINY.md` §5.14:
- **KEEP** the load-bearing discipline: the dispatch brief MUST name the **absolute arc-worktree root** (`<repo>/.claude/worktrees/arc-<N>-build`) because a sub-agent inherits the parent session cwd and a relative/defaulted path resolves to the MAIN tree (the Arc-55 observed-live failure). The module's `printf` redirect writes to `<worktree-root>/agents/verdicts/…`, so the brief must still pin the absolute worktree root — the reason the discipline exists is unchanged.
- **REWRITE the final sentence** (L256-258, the `--cwd` / `SKILL.md` clause). Replace:
  > "The skill-side half of this fix is the tightened `cwd` contract in `substrate/skills/save-verdict/SKILL.md` (the skill writes where `--cwd` points; only the dispatcher knows which tree is correct). Anchor: `stoa--xxy`."
  with prose pointing at the module's path-convention:
  > "The seat-side half of this fix is the path convention in `.claude/modules/save-verdict.md` §(a): the verdict lands at `<worktree-root>/agents/verdicts/<ticket-id>/…` via `printf` redirect, where `<worktree-root>` is the absolute arc-worktree root the dispatch brief pins (the module writes to the path the brief names; only the dispatcher knows which tree is correct). Anchor: `stoa--xxy`."
- Update the §5.14 heading reference target from the skill to the module wherever the rename "save-verdict skill → save-verdict module" makes the heading read as skill-specific (the heading "for save-verdict" stays — save-verdict is now a module, not a skill, so no further heading change is required beyond the body rewrite).

---

## 4. Fold r8 (HIGH — Q-A tier-uniformity: the empty-binding assert MUST live in the always-resolvable inline block)

**Problem.** rev1 §2.4 placed the threat-coverage empty-binding bash assert (the `^[pP]` regex, exit 4 — the §35/`stoa--yfv` B2 keystone) in the module's Q-A enforcement detail. But under Q-C = C2 (LOCKED), the module is NOT deployed at subproject tier and a dispatched seat's `Read .claude/modules/save-verdict.md` does not resolve reliably there. If the assert lives module-only, the least-droppable security-property guard silently vanishes at subproject tier — exactly the tier-non-uniformity the directive forbids.

**rev2 resolution — FOLD the ~6-line empty-binding assert INTO the role-file inline §7 block (not module-only).** It joins the printf+sha256+attach steps as a first-class member of the always-resolvable inline procedure, so it resolves at EVERY tier including subproject. The assert (verbatim, the LOCKED `^[pP]` form — this is the j2i-fix, do not alter the regex):

```bash
# Threat-coverage empty-binding guard (op-disc §35 / stoa--yfv B2).
# Only when the verdict declares threat-ratified mitigations:
if [ "${TRM_COUNT:-0}" -gt 0 ]; then
  [ -n "$THREAT_PROBE_IDS" ] || { echo "SAVE-VERDICT FAIL: $TRM_COUNT threat-ratified mitigation(s) declared but no threat-coverage probe-ids (op-disc §35/yfv B2)" >&2; exit 4; }
  IFS=',' read -ra _ids <<< "$THREAT_PROBE_IDS"
  for _id in "${_ids[@]}"; do
    _id="${_id// /}"
    [ -n "$_id" ] || continue
    printf '%s' "$_id" | grep -Eq '^[pP][0-9A-Za-z._-]+$' || { echo "SAVE-VERDICT FAIL: probe-id '$_id' malformed (must match ^[pP][0-9A-Za-z._-]+\$)" >&2; exit 4; }
  done
fi
```

**Where it lives — FOUR byte-identical copies:** the three role-file inline §7 blocks (CAPTAIN_VERA §7, CAPTAIN_ARGUS §7, CAPTAIN_CATO §7) AND `modules/save-verdict.md`. The module is the canonical elaboration (full rationale + Q-A HYBRID spec); the three inline copies are the always-resolvable executable guard.

**Extend the P8 byte-alignment set to include the empty-binding assert.** rev1 §2.7's SSoT-with-byte-alignment discipline (`canonical-template-alignment.md`) covered the printf+sha256+attach block across the four homes. rev2 EXTENDS the byte-aligned region to ALSO cover the empty-binding assert block — so all four copies carry the assert identically and a build-time `diff` (P8) guards it against drift. The byte-aligned shared region is now: **printf-author → inline sha256 round-trip → empty-binding threat-coverage assert → bw attach.** A `diff <(sed -n '<start>,<end>p' CAPTAIN_VERA.md) <(sed -n '<start>,<end>p' CAPTAIN_ARGUS.md)` (and CATO, and the module) over that region must be empty at build time.

**Amends rev1:** rev1 §2.1(e) ("Q-A enforcement — see §2.4") and §2.4's placement of the assert. The assert is no longer module-elaboration-detail; it is a first-class member of the inline §7 procedure in all three role files, byte-aligned with the module, and inside the P8-guarded region.

---

## 5. Fold r6 (LOW, fix-now — restore the dest-exists clobber guard + overwrite-escape)

**Problem.** The deleted Python writer had an exit-3 dest-exists collision guard (a same-path verdict was not silently clobbered) plus a `--overwrite` escape (an explicit opt-in for a legitimate re-write). rev1's Bash procedure dropped both — so two verdicts resolving to the same canonical path (same ticket + same officer + same-second timestamp) would silently clobber, re-opening a verdict-loss class while we are mid-arc closing a different one. Fix-now (the cost calculus: a 1-line guard now vs. a silent-loss bug later).

**rev2 resolution — restore a `[ -e "$DEST" ]` dest-exists guard (exit 3) + preserve an overwrite-escape.** Folded into the `save-verdict.md` module procedure AND the role-file inline §7 block (inside the byte-aligned region, so P8 covers it). Spec:

```bash
DEST=agents/verdicts/<ticket-id>/<OFFICER>-<ts>.md
mkdir -p "$(dirname "$DEST")"
# Dest-exists collision guard (mirrors the retired Python exit-3): do not silently
# clobber an existing same-path verdict. SAVE_VERDICT_OVERWRITE=1 is the explicit
# opt-in escape (mirrors the Python --overwrite) for a legitimate intentional re-write.
if [ -e "$DEST" ] && [ "${SAVE_VERDICT_OVERWRITE:-0}" != "1" ]; then
  echo "SAVE-VERDICT FAIL: dest exists $DEST (set SAVE_VERDICT_OVERWRITE=1 to re-write)" >&2
  exit 3
fi
printf '%s' '<verdict-body>' > "$DEST"
```

Exit-code map after this fold: **exit 2** = sha256 mismatch (rev1 §2.1c); **exit 3** = dest-exists collision without overwrite-opt-in (NEW, r6); **exit 4** = threat-coverage empty-binding / malformed probe-id (rev1 §2.4, r8). These three exit codes are the module's documented failure contract; they preserve the retired Python writer's exit semantics (2 = integrity, 3 = collision, 4 = shape/coverage) so a reader who knew the Python contract reads the bash one identically.

The dest-exists guard is ALSO inside the P8 byte-aligned region (it is part of the shared write procedure). Updated byte-aligned region: **dest-exists guard → printf-author → inline sha256 round-trip → empty-binding threat-coverage assert → bw attach.**

---

## 6. Fold r5 / W2 (LOCKED posture — attach-failure durability contract, HARDENED + DOCUMENTED as a durable contract)

The attach-failure posture is LOCKED (floor-manager adjudicated, converged with DAEDALUS's lean): **FAIL-LOUD-but-write-preserving, HARDENED**. rev2 does not change the posture — it folds the four hardening clauses and adds the LOAD-BEARING documentation condition.

**6.1 The hardened posture (four clauses, all LOCKED):**
1. **Structured, first-class ATTACH-FAILED signal in the seat's dispatch return** — NOT a scroll-past stderr echo. A NAMED field the orchestrator parses. rev2 adds it to the verdict-format / dispatch-return block of each verdict-producing seat (VERA / ARGUS / CATO) and to the module: when `bw attach` exits non-zero, the seat's dispatch return carries an explicit field, e.g.:
   ```
   attach_status: FAILED
   attach_failure: bw attach exited rc=<n>; verdict integrity-verified on disk at <DEST> (sha256 <hash>); NOT yet on beadwork — orchestrator MUST retry/escalate before treating this verdict as durable.
   ```
   On success the field is `attach_status: OK` (so absence-of-field is not silently read as success). This is the parseable signal PLINY keys its retry/escalate obligation off — distinct from the rev1 stderr `echo`, which stays as the human-readable breadcrumb but is NOT the load-bearing signal.
2. **Disk artifact preserved + sha256-verified** — the on-disk verdict is already integrity-checked (§2.1c sha256 round-trip); it is the lossless retry source. The attach failure does NOT discard it.
3. **The durability loop CLOSES AT THE ORCHESTRATOR** — an attach-failed verdict is NOT durable/complete. PLINY owns retry/escalate and does NOT advance the gauntlet (or permit teardown) past it until attach succeeds or it is escalated. (Documentation condition in 6.2.)
4. **NOT hard-exit** — the seat does not `exit`-hard-fail the verdict-write on attach failure (that would discard a valid integrity-checked artifact + brittle-block the gauntlet on a transient bw hiccup). In-seat bounded retry (2–3×) is the seat's optional judgment (e.g., retry `bw attach` 2–3× with a short backoff before emitting `attach_status: FAILED`); the seat is NOT required to retry, but the durability loop never depends on it — the orchestrator owns the closing obligation regardless.

**6.2 LOAD-BEARING CONDITION — document the orchestrator retry/escalate obligation as a DURABLE CONTRACT in TWO homes** (so a FUTURE PLINY inherits it, not ephemeral this-session intent):

- **(a) `modules/save-verdict.md`** — a "Durability contract (orchestrator obligation)" subsection stating: a verdict whose `attach_status` is `FAILED` is NOT durable. The dispatching orchestrator (PLINY) MUST, on receiving an `attach_status: FAILED` dispatch return: (i) retry `bw attach <ticket> <DEST>` from the preserved on-disk artifact; (ii) on continued failure, escalate per the universal triggers; (iii) NOT advance the gauntlet to the next seat and NOT permit worktree teardown past this verdict until attach succeeds or the failure is escalated. The on-disk artifact is the retry source and is sha256-verifiable against the `attach_failure` field's recorded hash.

- **(b) `MAJOR_PLINY.md` — a NEW §5.16 "Verdict-attach hand-back handling (durability close at the orchestrator)"** placed after the existing §5.15. There is currently NO hand-back-handling section in MAJOR_PLINY — rev2 ADDS one. It states the same obligation from the orchestrator's seat: on any verdict-producing CAPTAIN dispatch return carrying `attach_status: FAILED`, PLINY retries the attach from the preserved on-disk verdict, escalates on continued failure, and treats the verdict as NON-DURABLE — blocking gauntlet advancement and teardown past it until durable-or-escalated. Cross-reference `modules/save-verdict.md` durability-contract subsection as the seat-side half.

**6.3 SCOPE BOUNDARY (flag the coupling so `stoa--9s6` inherits it).** This arc STATES the invariant: *an attach-failed verdict blocks advancement (and teardown) until it is durable-or-escalated.* This arc does NOT own teardown ORDERING — that is `stoa--9s6` (out of scope, rev1 §5). rev2 adds an explicit coupling note IN the `modules/save-verdict.md` durability-contract subsection: "Teardown-ordering is owned by `stoa--9s6`; whatever teardown sequence 9s6 specifies MUST HONOR this invariant — no worktree teardown may run past a verdict whose `attach_status` is `FAILED` and unescalated." This makes the coupling durable so the 9s6 designer inherits the constraint rather than rediscovering it.

**Amends rev1:** rev1 §2.1(d) "Attach-failure posture" paragraph is REPLACED by §6.1–6.3 above (the rev1 version had only the stderr echo + "reports the attach failure in its dispatch return"; rev2 makes the report a structured first-class `attach_status` field, adds the in-seat bounded-retry option, and adds the TWO-HOME durable-contract documentation + the 9s6 coupling note).

---

## 7. Fold r7 (LOW — documented C2-residual, no fix)

**Accept as a documented C2-residual.** The four-copy SSoT (three role-file inline §7 blocks + the module) is guarded ONLY by the manual P8 build-time `diff`. A regen-time / CI alignment test that re-asserts byte-alignment on every `npm run gen-data` or pre-commit would be stronger, but it is a future-arc nicety, out of scope here. This is inherent to Q-C = C2 (LOCKED): C2 deliberately accepts a bounded drift surface (one mechanical `diff`) in exchange for avoiding three new recompose owners. rev2 records r7 as a **documented residual, no fix** — stated in §8 (weak points) below and carried as a follow-up. P8 is the live guard; the regen-time test is explicitly deferred.

---

## 8. Count correction (9 → 6, not 10 → 7) — fix every reference

**Ground truth (verified live).** `SKILL_NAMES` (`install.sh` L228-238) currently has **9** entries: `credential-discipline`, `inspect-script-output`, `handoff-author`, `save-verdict`, `validate-spec`, `workflow-composer`, `interactive-html-preview`, `team-launcher`, `gauntlet-setup`. (Arc 63 already removed `check-substrate-updates` + `check-bw-release`, so the count is 9, not the 10 rev1 assumed.) Removing the three pass-B entries (`save-verdict`, `validate-spec`, `inspect-script-output`) yields **6**.

**Every count reference rev2 corrects:**
- rev1 §2.5 "Remove … from `SKILL_NAMES` (L228-234; 10 → 7)" → **9 → 6**. (`credential-discipline` STAYS — out of scope.) Resulting 6 entries: `credential-discipline`, `handoff-author`, `workflow-composer`, `interactive-html-preview`, `team-launcher`, `gauntlet-setup`.
- **P7 (app green) asserts the LIEUTENANT count drops by 3** and the resulting roster reflects **6** skill-backed LIEUTENANTs from `SKILL_NAMES` (the gen-data LIEUTENANT surface is directory+SKILL.md driven, not SKILL_NAMES driven — but the −3 delta and the post-state count must be asserted; see §9 P7 below).
- Any other "10"/"7" in rev1 prose (§2.5) is corrected to 9/6.

---

## 9. §3 verification probes (amended for VERA — supersedes rev1 §3 for the named probes)

rev1 §3 P1, P2, P3, P5, P6 carry forward UNCHANGED. rev2 amends P4, P7, P8 and adds the install.sh carve-out assertions:

- **P4 — threat-coverage empty-binding (Q-A preserved-check) + INLINE-block placement (r8).** With `TRM_COUNT=1` and empty `THREAT_PROBE_IDS`, confirm exit 4. With `TRM_COUNT=1` and `THREAT_PROBE_IDS="P-INJ"` (UPPERCASE), confirm it PASSES — proving the `stoa--j2i` lowercase-p bug is NOT reproduced (regex `^[pP]…`). With a malformed id (`x9`), confirm exit 4. **AND (r8): assert the empty-binding assert block physically LIVES IN the role-file inline §7 block of CAPTAIN_VERA / CAPTAIN_ARGUS / CAPTAIN_CATO** (not module-only) — `grep` the `^[pP][0-9A-Za-z._-]+$` assert in each of the three role files, confirming it resolves at subproject tier where the module is absent.
- **P7 — app green + count.** `cd app && npm run gen-data && npm run build && npm test` all green; the LIEUTENANT count drops by **3** from the prior baseline; the roster reflects **6** SKILL_NAMES-backed LIEUTENANTs (NOT 7); `generated.test.ts` `length>0` still holds. (Verify-then-assert: run the FULL suite and read the actual LIEUTENANT count from the regen output — do not assert "−3" from "this arc edited 3 SKILL.md files"; the regen re-derives the whole roster, gen-data-regen-re-derives-whole-roster lesson.)
- **P8 — role-file inline / module byte-alignment, NOW INCLUDING the empty-binding assert (r8) AND the dest-exists guard (r6).** `diff` the shared byte-aligned region — **dest-exists guard → printf-author → inline sha256 round-trip → empty-binding threat-coverage assert → bw attach** — across CAPTAIN_VERA §7 inline + CAPTAIN_ARGUS §7 inline + CAPTAIN_CATO §7 inline + `modules/save-verdict.md`. All four byte-identical over that full region (no drift). The empty-binding assert and the dest-exists guard are explicitly inside the diffed region.
- **P9 (NEW) — install.sh carve-out + prune-exemption cover the two operator-tool dirs (r1/r2).** Confirm `CARVEOUT_SKILL_DIRS` (L1297) contains BOTH `validate-spec` AND `inspect-script-output`; confirm the prune-scan exemption case (L1780) matches BOTH; confirm `save-verdict` is in NEITHER. Drive a `--target user` install (real or dry-run) against a synthetic parent and confirm the two retained script dirs (SKILL.md removed) ARE deployed and are NOT prune-deleted; confirm the `save-verdict` dir is fully absent (no deploy, no dangling reference).
- **P10 (NEW) — no dangling skill pointers after r3/r4 (extends rev1 P5).** `grep -rn "skills/save-verdict" substrate/` returns ZERO live references (excluding `substrate/arcs/` + `substrate/v1-historical/`); `operating-disciplines.md` L590 and `MAJOR_PLINY.md` §5.14 now point at `.claude/modules/save-verdict.md`; no `--cwd` skill-contract sentence remains in §5.14.

---

## 10. Threat→mitigation map (§6.12) — UNCHANGED from rev1, re-affirmed

This arc remains **process / role-file hardening** (skill→module rehoming + verdict-durability + doc-coherence + clobber-guard). No runtime attack path. Per §35.5 self-carve-out (I PROPOSE, ARGUS CONFIRMS):

`not threat-ratified (process change — skill→module rehoming + verdict-durability hardening + doc-coherence repair + dest-exists clobber-guard; no runtime attacker, no attack path)`

No `M<n>` is issued; no threat-anchored probe is required (§6.13). The folds in rev2 introduce no new runtime surface: r1/r2 are deploy-list coherence; r3/r4 are doc-pointer coherence; r6 is a same-path clobber-guard (the path comes from the trusted PLINY brief, not an attacker — input-hygiene, not threat-mitigation, same class as the preserved path-traversal regexes per rev1 §2.4); r5/W2 is a durability contract (closes a verdict-LOSS gap, not an attacker path); r8 relocates an EXISTING §35/yfv-B2 guard from module-only to the always-resolvable inline block (it preserves a guard, mints no new mitigation). ARGUS confirms the carve-out at A1/critique; I cannot self-grant it.

---

## 11. Self-assessed weak points (rev2)

- **(W1, carried from rev1 — Q-C=C2 four-copy SSoT, now FIVE-element region.)** The byte-aligned region (dest-exists guard + printf + sha256 + empty-binding assert + bw attach) lives inline in three role files AND in the module — four copies, and the region grew this rev2 (r6 + r8 folded two more blocks into it). More surface to drift. *Why this shape anyway:* P8 mechanically guards the FULL region at build time with a single `diff`; the alternative (C1 recompose) mints three recompose owners + FAIL-LOUD machinery and STILL leaves the module as a separate copy. C2's drift is bounded by one build-time assertion; folding r6/r8 into the SAME byte-aligned region keeps them under that same single guard rather than scattering them.
- **(W2, r7 documented residual.)** The four-copy alignment is guarded only by the manual/build-time P8 `diff`, not a regen-time/CI test. A future arc editing the module without re-running the build's P8 (or vice versa) reintroduces drift between P8 runs. *Why this shape anyway:* the regen-time alignment test is a real improvement but a separate future-arc deliverable; P8 is the live guard this arc ships, and r7 is recorded as a documented C2-residual (no fix this arc) rather than silently smoothed.
- **(W3, NEW — the `attach_status` field is a new contract two seats + the orchestrator must honor.)** r5/W2 introduces a structured `attach_status` field that VERA/ARGUS/CATO must emit and PLINY must parse + act on. If a future seat-file edit drops the field, the durability loop silently reverts to "fire-and-forget attach." *Why this shape anyway:* the field is documented as a durable contract in BOTH homes (module + MAJOR_PLINY §5.16) precisely so a future PLINY/seat inherits it; the rev1 alternative (stderr echo only) was the weaker, scroll-past form the floor-manager explicitly rejected. The two-home documentation is the mitigation for this weak point.

## 12. Out of scope (carried from rev1, + r5/W2 coupling)

All rev1 §5 out-of-scope items stand. Added/clarified:
- **`stoa--9s6` worktree-teardown ORDERING** — out of scope; rev2 STATES the attach-failed-blocks-teardown invariant (§6.3) and flags the coupling IN the module so 9s6 inherits it, but does not specify the teardown sequence.
- **Regen-time / CI byte-alignment test** (r7) — out of scope; P8 build-time `diff` is the live guard this arc ships.
- **`credential-discipline` skill** — STAYS in `SKILL_NAMES` (now 1 of the 6); out of scope.
