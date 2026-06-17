# Arc 61 design — design-rev1.md (CAPTAIN_DAEDALUS)

**Ticket:** `stoa--p41.1` (epic) / charter `stoa--p41`. **Directive:** `substrate/arcs/arc-61-build-directive.md` (FINALIZED, NOMOS-conformant). **Worktree:** `.claude/worktrees/arc-61-build` (branch `arc-61/build`, HEAD `df0ca9d`). **Author:** Denson Smith.

> All paths below are **worktree-relative** (root = `.claude/worktrees/arc-61-build/`). Line numbers are ground-truthed against the worktree at design time but **drift on edit** — ADA must re-anchor on the quoted before-text, not the line number.

---

## 0. O1 fallback verdict (surface-to-POLYBIUS gate) — **RE-HOME PROCEEDS**

The Settled decision is **RE-HOME** `pair-programmer-authoring.md` as a CHIRON-owned module. The directive obliges me to run the fallback test (fold-into-§7-and-retire) and recommend it ONLY IF the module's unique content is thin and mostly subsumed by CHIRON §7.

**Verdict: the fallback does NOT apply. RE-HOME proceeds as the primary path.** The module (`substrate/modules/pair-programmer-authoring.md`, 94 lines) carries substantive content that CHIRON §7 does **not** contain:

- **§11.1 Trigger recognition** (4-signal "two-or-more" test for when a pair-programmer Major is warranted) — CHIRON §7 covers *how to author*, not *when a pair-programmer specifically* is the right answer. §4 of CHIRON gestures at "pair-programmer = lightweight branch" but does not carry the trigger test.
- **§11.2 Walk-through procedure** (the 7-step pair-programmer-specific flow incl. the paste-instruction / fresh-session activation handoff) — distinct from §7's generic author-a-seat procedure. The pair-programmer activation handoff (PRINCIPAL opens a new terminal, pastes a one-liner) is POLYBIUS-operational, not CHIRON-authoring.
- **§11.3 Empirical lineage** (ATTICUS / PYTHAGORAS / CODEX / LEX) — provenance not in §7.
- **§11.4 Asymmetric beadwork visibility** (the task-scoped bw visibility rule for pair-programmers) — wholly absent from CHIRON §7; this is a runtime-coordination discipline, not an authoring mechanic.

The module's unique content is NOT thin and is NOT subsumed by §7. RE-HOME is the correct call and the slim-core discipline (lean role file + detail in a module + FAIL-LOUD recompose) is the right home. **No surface-to-POLYBIUS needed on O1** beyond noting this verdict; PLINY may relay it.

One design refinement carried into D5 below: when the module re-homes to CHIRON, its cross-references back into `MAJOR_POLYBIUS.md` §12 / §11.1 / §4.1 need re-pointing because the module is now CHIRON-hosted but still describes a *POLYBIUS-and-PRINCIPAL* workflow. See D5 §"Module body edits" for the full ref-repoint list (this is broader than the directive's single "~:39" mention — flagged as a weak point too).

---

## 1. Problem restatement

Arc 61 lands a new standing MAJOR seat — **MAJOR_CHIRON, the design-time TEAM-ARCHITECT** — and executes the coupled cascade its arrival forces: the `agent-author` skill retires (its capability now lives inlined in `MAJOR_CHIRON.md` §7, exclusive by construction); POLYBIUS sheds the authoring *tool* but keeps review *literacy*, so POLYBIUS §11 relocates to point authoring at CHIRON; the `pair-programmer-authoring.md` module re-homes POLYBIUS→CHIRON (ownership reassigned in install.sh's FAIL-LOUD subproject-recompose partition); CHIRON deploys at all tiers (user/project/subproject, suffixed `CHIRON_<slug>`); 5 dangling references to the retired skill are fixed; and the Stoa app's one stale test assertion updates while the LIEUTENANT slot stays populated by the other 11 skills. The load-bearing constraint: **the install.sh recompose machinery is FAIL-LOUD (exit 2) and the marker↔module↔ownership-partition coupling must stay internally consistent at BOTH a user-tier and a subproject-tier dry-run — no check may be silenced; the underlying consistency must be correct.**

**Imported assumptions** (named per §6.1): (a) `docs/major-chiron.html` is a **hand-authored** rendered view (no generator script exists in-tree) — "regen" = a manual HTML edit mirroring the .md change, NOT a script run. (b) The floor-manager's three pre-build GAPs (A/B/C) are in-scope corrections to the directive's deliverable list and I fold them in. (c) CHIRON, as a MAJOR, should get a **dedicated `DEST_CHIRON` var** in install.sh's §2 MAJOR-deploy block (parallel to `DEST_POLYBIUS`/`DEST_PLINY`), which is cleaner than the DAEDALUS no-DEST-var workaround and means CHIRON's recompose call needs no `WITH_CAPTAINS` guard (CHIRON is not a CAPTAIN; it deploys unconditionally).

---

## 2. Approach (shape + the load-bearing structural choices)

Three structural decisions drive the whole build:

1. **CHIRON deploys via the MAJOR path, with its own `DEST_CHIRON` var, in install.sh §2** (L924-967 region) — NOT via the CAPTAIN loop. This means: (i) suffixing follows `SUFFIX_MAJORS` exactly like POLYBIUS/PLINY (so `CHIRON_<slug>` at project/subproject falls out for free); (ii) `$DEST_CHIRON` exists *before* the recompose call block (§3b, L1163+), so CHIRON's recompose call needs no special "file doesn't exist yet" handling and no `WITH_CAPTAINS` guard. This is why CHIRON is structurally simpler than DAEDALUS in the recompose machinery despite both being module-owners.

2. **The ownership partition moves exactly one basename: `pair-programmer-authoring` leaves `POLYBIUS_MODULES`, joins a new `CHIRON_MODULES`.** Disjointness (the P-OWNERSHIP-NOCOLLIDE invariant) is preserved because the basename moves wholesale between two sets — it is never in both. The module *file itself does not move* on disk (it stays `substrate/modules/pair-programmer-authoring.md`, the shared dir); only its *marker home* moves (POLYBIUS §11 marker removed; CHIRON §11 marker added) and its *owned-set membership* moves.

3. **The marker pair migrates atomically with the partition entry.** Check A (global existence) is owner-agnostic and unaffected. Check B/D are owned-scoped: after the move, POLYBIUS's owned-set no longer contains `pair-programmer-authoring` AND POLYBIUS no longer has its marker → Check B/D green for POLYBIUS. CHIRON's owned-set contains it AND CHIRON has the marker → Check B/D green for CHIRON. The three edits (remove POLYBIUS marker, add CHIRON marker, move partition entry) are a single atomic set — any one alone breaks a check (that is the FAIL-LOUD design working as intended).

**Threat→mitigation map:** This arc is a **process / role-file / tooling hardening change with no runtime attack path** (§35.5 carve-out). No named threat (ARGUS-surfaced or ratification-origin) is in play. Per §6.12 I PROPOSE the classification **`not threat-ratified (process change: substrate canon + deploy-tooling refactor, no runtime attack path)`** — ARGUS confirms. No A3 map row and no threat-anchored probe (§6.13) are required; the FAIL-LOUD recompose checks are correctness gates, not security mitigations.

---

## D1 — Land `MAJOR_CHIRON.md` (refine draft → final) + regen `docs/major-chiron.html`

**File:** `substrate/MAJOR_CHIRON.md` (present in tree, committed in `f105512`). The draft is strong; refinements are minimal. The one *structural* change (the §11 MODULE-INLINE host stub) is in **D5**, not here — keep D1 to the draft-finalization edits.

**Edit D1.1 — drop the DRAFT banner.** The seat is landing as canon.
- Location: L3, the blockquote beginning `> **DRAFT — v1, 2026-06-16.** First cut for review (working tree, uncommitted).`
- Before: `> **DRAFT — v1, 2026-06-16.** First cut for review (working tree, uncommitted). Charter: ...`
- After: rewrite to a non-draft provenance line, e.g. `> **v1 — landed Arc 61.** Charter: \`stoa--p41\`. Sibling architect: \`MAJOR_HAMILTON\` (\`stoa--yh2\`, separate arc). The agent-author capability (§7) is developed in skill-shape but lives here as instruction, not as a shared \`.claude/skills/\` file — so it is CHIRON's by construction, exclusive without any scoping mechanism.`
- Note: keep the "exclusive by construction" sentence — it is load-bearing rationale.

**Edit D1.2 — §7 sub-bullet that points at the retired skill.** §7's "What this is NOT" / template-basis prose is fine, BUT verify §7 does not itself say "invoke the agent-author skill" anywhere (grep confirms it does not — §7 says "you author seats in-seat, not by invoking a shared skill", L87, which is exactly right). **No edit needed in §7 body**; this is a confirm-clean check, not a change. Listed so ADA explicitly confirms rather than assumes.

**Edit D1.3 — regen `docs/major-chiron.html`.** This is a **hand-authored** rendered view (no generator script in-tree — confirmed: no `render*.ts`/`*.md.html` generator exists). "Regen" = manual HTML edits mirroring the .md deltas:
- File: `docs/major-chiron.html`.
- Mirror Edit D1.1: the draft-banner blockquote is rendered around L78-82 (`<p>` containing "developed in skill-shape but lives here as instruction"). Update to match the new non-draft provenance line.
- Mirror D5's new §11 host stub: add an `<h2 id="s11">` section + nav-bar entry (the nav bar at L70 lists `§5…§8`; extend to include `§11` if the host stub is given a numbered heading — see D5 note on CHIRON section numbering).
- Author field: L6 `<meta name="author" content="Denson Smith" />` — **must stay Denson Smith** (authorship discipline). Confirm unchanged.
- This HTML edit is the highest-tedium, lowest-risk item; VERA verifies by visual diff against the .md, not by a build.

---

## D2 — install.sh: deploy CHIRON at all tiers + add recompose ownership-partition entry

**File:** `substrate/install.sh`.

**Edit D2.1 — add `SRC_CHIRON`.**
- Location: L155-157, the source-var block.
- Before: `SRC_POLYBIUS="${SCRIPT_DIR}/MAJOR_POLYBIUS.md"` / `SRC_PLINY="${SCRIPT_DIR}/MAJOR_PLINY.md"`
- After: add `SRC_CHIRON="${SCRIPT_DIR}/MAJOR_CHIRON.md"` immediately after `SRC_PLINY`.

**Edit D2.1b — add the source-file existence guard (DO NOT MISS — install.sh fails loud on missing sources).**
- Location: `substrate/install.sh` L800-802, the `[ -f "$SRC_POLYBIUS" ] || err …` guard block.
- Before:
  ```
  [ -f "$SRC_POLYBIUS" ]              || err "source file not found: $SRC_POLYBIUS"
  [ -f "$SRC_PLINY" ]                 || err "source file not found: $SRC_PLINY"
  [ -f "$SRC_OPERATING_DISCIPLINES" ] || err "source file not found: $SRC_OPERATING_DISCIPLINES"
  ```
- After: add `[ -f "$SRC_CHIRON" ] || err "source file not found: $SRC_CHIRON"` parallel to the others.
- Rationale: install.sh validates every MAJOR source exists at startup. Without this guard CHIRON deploy would still work (the file exists), but parity with POLYBIUS/PLINY is the discipline AND a future missing-source regression would fail silently for CHIRON. Mirror the existing guards exactly.

**Edit D2.2 — add `DEST_CHIRON` to the §2 MAJOR-deploy block.**
- Location: L932-938, the `if [ "$SUFFIX_MAJORS" -eq 1 ]; then … else … fi` that sets `DEST_POLYBIUS`/`DEST_PLINY`.
- Before:
  ```
  if [ "$SUFFIX_MAJORS" -eq 1 ]; then
    DEST_POLYBIUS="${DEST_DIR}/MAJOR_POLYBIUS${NAME_SUFFIX}.md"
    DEST_PLINY="${DEST_DIR}/MAJOR_PLINY${NAME_SUFFIX}.md"
  else
    DEST_POLYBIUS="${DEST_DIR}/MAJOR_POLYBIUS.md"
    DEST_PLINY="${DEST_DIR}/MAJOR_PLINY.md"
  fi
  ```
- After: add a `DEST_CHIRON` assignment in BOTH branches, parallel:
  ```
  if [ "$SUFFIX_MAJORS" -eq 1 ]; then
    DEST_POLYBIUS="${DEST_DIR}/MAJOR_POLYBIUS${NAME_SUFFIX}.md"
    DEST_PLINY="${DEST_DIR}/MAJOR_PLINY${NAME_SUFFIX}.md"
    DEST_CHIRON="${DEST_DIR}/MAJOR_CHIRON${NAME_SUFFIX}.md"
  else
    DEST_POLYBIUS="${DEST_DIR}/MAJOR_POLYBIUS.md"
    DEST_PLINY="${DEST_DIR}/MAJOR_PLINY.md"
    DEST_CHIRON="${DEST_DIR}/MAJOR_CHIRON.md"
  fi
  ```
  - Rationale: `SUFFIX_MAJORS=1` only at subproject tier (L793) → `CHIRON_<slug>` falls out exactly like POLYBIUS/PLINY. At project tier `NAME_SUFFIX` is `_<project-slug>` but `SUFFIX_MAJORS=0` — **confirm against the existing POLYBIUS/PLINY behavior** that project-tier MAJORs are NOT suffixed (the `else` branch). The directive says "suffixed `CHIRON_<slug>` at project/subproject parallel to POLYBIUS/PLINY" — so whatever POLYBIUS/PLINY do, CHIRON mirrors **exactly**. This edit guarantees that by construction. (Weak point flagged in §WP-2: the directive's prose says "project/subproject" suffix but the code only suffixes when `SUFFIX_MAJORS=1`, which is subproject-only — ADA must mirror POLYBIUS, NOT the directive prose, and the verification confirms parity.)

**Edit D2.3 — deploy CHIRON in the §2 deploy body.**
- Location: L955-967, the dry-run/real deploy of POLYBIUS + PLINY.
- CHIRON carries no `{{USER_TIER_DIR}}` placeholder (only POLYBIUS does), so it follows the PLINY pattern (plain `{{NAME_SUFFIX}}` sed). Add parallel to the PLINY lines:
  - Dry-run branch (after the PLINY dry-run echo at L957): `echo "[dry-run] deploy: $SRC_CHIRON -> $DEST_CHIRON (substitute {{NAME_SUFFIX}} -> '${NAME_SUFFIX}')"`
  - Real branch (after L964 `sed … "$SRC_PLINY" > "$DEST_PLINY"`): `sed "s/{{NAME_SUFFIX}}/${NAME_SUFFIX}/g" "$SRC_CHIRON" > "$DEST_CHIRON"`
  - And `echo "deployed: $DEST_CHIRON"` after L966.
- **Confirm `MAJOR_CHIRON.md` contains no `{{NAME_SUFFIX}}` placeholder today** (grep): the sed is then a defensive no-op, exactly like POLYBIUS/PLINY today (per the L928-931 comment). It is harmless if present, correct if absent.

**Edit D2.4 — add the `CHIRON_MODULES` ownership-partition entry + recompose call.** (This is the D5 ownership reassignment; placed here because the directive folds it under D2.) Detailed in **D5 §"install.sh partition"** below to keep the partition logic in one place. The summary: add `CHIRON_MODULES="pair-programmer-authoring"`, remove `pair-programmer-authoring` from `POLYBIUS_MODULES`, add `DEST_CHIRON` is already set, and add `recompose_module_inline "$DEST_CHIRON" "$CHIRON_MODULES"` to the §3b subproject recompose-call block — **ungated** (CHIRON deploys unconditionally, unlike the WITH_CAPTAINS-gated DAEDALUS call).

**Edit D2.5 — update the §3a recompose machinery header comment** (L1003-1006) that enumerates the recompose owners. Currently: "$DEST_POLYBIUS (Arc 2, 5 owned modules) … $DEST_DAEDALUS (Arc 6/Arc 49, 7 owned modules — the FOURTH owner)". After this arc there is a **FIFTH owner (CHIRON, 1 owned module)** and POLYBIUS drops to **4 owned modules**. Update the comment counts: `$DEST_POLYBIUS (Arc 2, now 4 owned modules)` and add `$DEST_CHIRON (Arc 61, 1 owned module — the FIFTH owner)`; update the "5 POLYBIUS + 12 op-disc + 11 PLINY + 7 DAEDALUS = 35" arithmetic to "4 + 12 + 11 + 7 + 1 = 35" (the total is unchanged — a module moved, none added/removed). Also update the L1027 narrative ("Without the partition, recompose_module_inline "$DEST_POLYBIUS" Check B would false-positive on the 12 op-disc modules") — that example still holds, no edit needed, but the disjointness sentence at L1023-ish referencing the four owned-sets should mention five.

---

## D3 — Retire `agent-author`

**File:** `substrate/skills/agent-author/` + `substrate/install.sh`.

**Edit D3.1 — remove from `SKILL_NAMES`.**
- Location: `substrate/install.sh` L226-238, the `SKILL_NAMES=( … )` array.
- Before: the array's first entry (L227) is `  agent-author`.
- After: delete that line. (Ordering of the remaining 11 is immaterial; `discoverSkillFiles` and the deploy loop iterate set-wise.)

**Edit D3.2 — `git rm -r substrate/skills/agent-author/`.** ADA executes the git removal (not a plain `rm` — it must be staged). The dir contains `SKILL.md` (+ any helpers; ADA confirms contents before removal). **Coupling note:** D3.1 (SKILL_NAMES) and D3.2 (dir removal) must land together — if the dir is removed but `SKILL_NAMES` still lists it, the skill-deploy loop (L5, L262+) errors on the missing `$src_skill`; if `SKILL_NAMES` drops it but the dir lingers, a stale skill dir sits untracked. Same-commit.

---

## D4 — Relocate POLYBIUS §11 (authoring → CHIRON) + routing-map + relocation-index + §7.6 cross-ref

**File:** `substrate/MAJOR_POLYBIUS.md`. (The §11 MODULE-INLINE *marker removal* is D5; D4 is the prose/index edits. They co-land.)

**Edit D4.1 — rewrite the §11 stub body** (L307-311). Today §11 relocates the authoring procedure to `pair-programmer-authoring.md` (a POLYBIUS-owned module). After the arc, POLYBIUS no longer hosts that module (it re-homes to CHIRON) AND POLYBIUS no longer holds the authoring tool. §11 becomes a **pointer to CHIRON**, framed as "POLYBIUS reviews, CHIRON authors."
- Before (L307-311):
  ```
  ## 11. Pair-programmer Major authoring
  Relocated to `.claude/modules/pair-programmer-authoring.md` (CONDITIONAL — loaded at dispatch).
  Routing-map + relocation-index rows in §3.5. Recover the full procedure via `Read .claude/modules/pair-programmer-authoring.md`.
  <!-- MODULE-INLINE:pair-programmer-authoring -->
  <!-- /MODULE-INLINE:pair-programmer-authoring -->
  ```
- After (new prose; marker pair REMOVED — that removal is D5.1):
  ```
  ## 11. Pair-programmer Major authoring — now CHIRON-owned

  Authoring agent envelopes (incl. pair-programmer Majors) is **MAJOR_CHIRON's** capability (the
  TEAM-ARCHITECT; `MAJOR_CHIRON.md` §7). POLYBIUS keeps the **review literacy** — POLYBIUS reviews
  and controls roster composition (the same reviewer-without-the-tool shape as ARGUS-reviews-DAEDALUS)
  — but no longer holds the authoring procedure. The pair-programmer authoring detail (trigger
  recognition, walk-through, lineage, asymmetric bw visibility) lives in the CHIRON-owned module
  `.claude/modules/pair-programmer-authoring.md` (recompose-hosted at `MAJOR_CHIRON.md` §11). When a
  pair-programmer-Major signal fires (§4.1-class project-direction call), POLYBIUS surfaces it and
  routes the authoring to CHIRON; POLYBIUS reviews the draft.
  ```
  - **Critical:** the marker pair is GONE from POLYBIUS after this edit. That is required for Check D (POLYBIUS still has 4 other markers, so `markers_seen > 0` — Check D does not fire; but Check B requires the owned-set no longer list `pair-programmer-authoring`, handled in D5's partition edit). The marker removal and the partition-entry removal are the SAME atomic set.

**Edit D4.2 — routing-map row** (§3.5, L71).
- Before: `| author a pair-programmer Major | \`pair-programmer-authoring.md\` | disk (Read) |`
- After: re-point to CHIRON. Option (chosen): `| author a pair-programmer Major | route to MAJOR_CHIRON (\`MAJOR_CHIRON.md\` §7/§11) | seat |`
  - Rationale: POLYBIUS no longer Reads this module (it is CHIRON-owned). The routing-map answers "at dispatch time, what does this task need?" — the answer is now "route to CHIRON," not "Read a local module." Keep the table shape (3 columns); the Channel column becomes `seat` (route to another seat) rather than `disk (Read)`.

**Edit D4.3 — relocation-index row** (§3.5, L84).
- Before: `| §11 Pair-programmer Major authoring | \`pair-programmer-authoring.md\` (disk module) | CONDITIONAL |`
- After: the relocation index answers "where did the content that used to be here go?" — the content went to CHIRON. `| §11 Pair-programmer Major authoring | re-homed to MAJOR_CHIRON (\`MAJOR_CHIRON.md\` §11 + CHIRON-owned \`pair-programmer-authoring.md\`) | RELOCATED (cross-seat) |`
  - Note the Class changes from `CONDITIONAL` (a POLYBIUS-owned on-demand module) to a cross-seat relocation. If the repo's relocation-index Class vocabulary is constrained (CONDITIONAL/PROVENANCE/DUPLICATE per L82-95), use the closest fit + a parenthetical; ADA confirms the vocabulary. (Weak point WP-3.)

**Edit D4.4 — §7.6 cross-ref** (L260).
- Before: `… ad-hoc dispatches (§2 / §7; rare), or pair-programmer activation flows (§11) — the same orchestrator background-dispatch hygiene applies …`
- After: §11 no longer carries the activation flow (it points to CHIRON). The cross-ref to "(§11)" still resolves to the relocated §11, but the framing "pair-programmer activation flows (§11)" should acknowledge CHIRON authors them: `… or pair-programmer activation flows (now CHIRON-authored; §11) — the same orchestrator background-dispatch hygiene applies …`. Minimal touch; the §11 anchor still exists.

---

## D5 — Re-home `pair-programmer-authoring.md` to CHIRON (the O1 core)

Three coupled sub-edits + the module body edits. **All co-land in the same commit as D4** (the marker move + partition move + POLYBIUS prose are one atomic consistency set).

### D5.1 — remove the §11 MODULE-INLINE marker from POLYBIUS
Folded into **D4.1**: the `<!-- MODULE-INLINE:pair-programmer-authoring -->` / `<!-- /MODULE-INLINE:pair-programmer-authoring -->` pair (L310-311) is deleted as part of rewriting §11. After this, POLYBIUS has 4 markers (onboarding L185, sub-project-spawning L302, pair-programming-prototyping L318, substrate-update-check L373) for its 4 remaining owned modules.

### D5.2 — add a MODULE-INLINE host stub in `MAJOR_CHIRON.md`
CHIRON currently has **zero** MODULE-INLINE markers. Adding its first marker makes it the FIFTH recompose owner.
- File: `substrate/MAJOR_CHIRON.md`.
- Add a new numbered section hosting the module. Recommended placement: a new **§11** after the current §10 (Activation checklist, ends ~L145) and before the `## Tools` block (L147). Section numbering: §1-§10 + Tools today; inserting §11 before Tools keeps Tools last.
- New section text (the slim-core stub shape, mirroring POLYBIUS's relocated-section idiom):
  ```
  ## 11. Pair-programmer Major authoring (detail module)

  Re-homed from `MAJOR_POLYBIUS.md` §11 (Arc 61). CONDITIONAL — loaded at dispatch when authoring a
  pair-programmer Major (the lightweight branch of §4). Recover the full procedure via
  `Read .claude/modules/pair-programmer-authoring.md`. At subproject tier the body is recompose-inlined
  at the marker below.

  <!-- MODULE-INLINE:pair-programmer-authoring -->
  <!-- /MODULE-INLINE:pair-programmer-authoring -->
  ```
- **Check C (balance):** the open/close pair is balanced and full-line. **Check E (no marker in body):** the module source `pair-programmer-authoring.md` must not contain a literal `MODULE-INLINE` line — grep-confirm (it does not today). **Check A (global existence):** `pair-programmer-authoring.md` exists in `SRC_MODULES_DIR` (it stays on disk) → green regardless of owner.
- The CHIRON §11 marker must mirror the .md change in `docs/major-chiron.html` (D1.3) — but the HTML rendered view does NOT carry MODULE-INLINE markers (they're machine-only); render §11 as a normal section without the comment markers.

### D5.3 — install.sh partition reassignment (the ownership move)
- File: `substrate/install.sh`, the §3b owned-set block (L1167-1185).
- **Before** (L1168): `POLYBIUS_MODULES="onboarding sub-project-spawning pair-programmer-authoring pair-programming-prototyping substrate-update-check"`
- **After:** remove `pair-programmer-authoring` from `POLYBIUS_MODULES`:
  `POLYBIUS_MODULES="onboarding sub-project-spawning pair-programming-prototyping substrate-update-check"`
- **Add a new owned-set line** (after the `DAEDALUS_MODULES=` line ~L1171):
  `CHIRON_MODULES="pair-programmer-authoring"`
- **Add the recompose call** in the call sequence (L1174-1176 region, after the three existing unconditional calls and before the WITH_CAPTAINS-gated DAEDALUS call ~L1183):
  `recompose_module_inline "$DEST_CHIRON" "$CHIRON_MODULES"`
  - **UNGATED** — CHIRON deploys unconditionally (it is in the §2 MAJOR-deploy block, always runs), so `$DEST_CHIRON` always exists at subproject tier when the recompose-call block runs. This is UNLIKE DAEDALUS (gated on `WITH_CAPTAINS` because DAEDALUS only deploys inside the CAPTAIN loop). Do **not** wrap CHIRON's call in a `WITH_CAPTAINS` guard.
- **Disjointness invariant (P-OWNERSHIP-NOCOLLIDE):** `pair-programmer-authoring` is removed from `POLYBIUS_MODULES` in the same edit it is added to `CHIRON_MODULES` — it is never in both sets. The five owned-sets stay basename-disjoint. Total owned modules unchanged: 4 (POLYBIUS) + 12 (op-disc) + 11 (PLINY) + 7 (DAEDALUS) + 1 (CHIRON) = 35.

### D5.4 — module body edits (repoint the skill refs — GAP A: FOUR refs, not one)
- File: `substrate/modules/pair-programmer-authoring.md`. The directive named "~:39"; the floor-manager's GAP A correctly identifies **four** skill references (L35-37, L39, L82). All four must repoint to CHIRON §7 (the skill is retired).
  - **L35-37** (within step 2 "Pick the template basis"): `The agent-author skill's "Template-basis selection" section (§"Template-basis selection" in skills/agent-author/SKILL.md) carries the full table.` → repoint to `MAJOR_CHIRON.md` §7's "Template-basis selection" subsection: `CHIRON's agent-author capability (MAJOR_CHIRON.md §7, "Template-basis selection") carries the full table.`
  - **L39** (step 3, the directive's named line): `Invoke the agent-author skill (substrate/skills/agent-author/SKILL.md). Inputs: …` → `Route the authoring to MAJOR_CHIRON, whose agent-author capability (MAJOR_CHIRON.md §7) drafts the role file. Inputs: …` (preserve the input list — it matches §7's "Inputs you fix before drafting").
  - **L82** (§11.3 lineage closing): `Arc 17 ships the *capability* (this section + the agent-author skill) without committing specific instances …` → `Arc 17 shipped the *capability* (this section + the agent-author skill, now CHIRON §7 after Arc 61) without committing specific instances …` — a provenance edit, keeps the Arc-17 history accurate while noting the Arc-61 move.
- **Cross-seat reframe (the O1 refinement flagged in §0):** the module describes a *POLYBIUS-and-PRINCIPAL* workflow but is now CHIRON-hosted. Re-point the POLYBIUS-internal cross-refs so they resolve from CHIRON's vantage. Specifically:
  - L10: `… captured in \`MAJOR_POLYBIUS.md\` §12 (→ \`pair-programming-prototyping.md\`).` — §12 is still POLYBIUS-owned, so this **stays** as a `MAJOR_POLYBIUS.md` ref (correct; the prototyping methodology did NOT move). No edit; confirm.
  - L21: `… (\`MAJOR_POLYBIUS.md\` §4.1).` — §4.1 is the PRINCIPAL-intent / project-direction call, still POLYBIUS. Stays. Confirm.
  - L91: `… (\`MAJOR_POLYBIUS.md\` §7.1) and the parent/sub-project asymmetry (§10.3) …` — POLYBIUS refs, still valid. Stay. Confirm.
  - **Decision:** the module keeps its POLYBIUS cross-refs where they point at *still-POLYBIUS-owned* content (§4.1, §7.1, §10.3, §12). Only the *agent-author skill* refs (the 4 GAP-A sites) repoint to CHIRON. This is the minimal correct change — the module is hosted by CHIRON but legitimately references POLYBIUS's surrounding workflow. (WP-4: this leaves a CHIRON-hosted module with several `MAJOR_POLYBIUS.md` cross-refs; intentional, but ARGUS should confirm none point at *moved* content.)
- **Module header provenance** (L3-6): currently "Relocated from `MAJOR_POLYBIUS.md` §11". Update to note the Arc-61 re-home: `Relocated from MAJOR_POLYBIUS.md §11 (debloat Arc 2), re-homed to MAJOR_CHIRON.md §11 (Arc 61).` Keep the existing provenance cites.

---

## D6 — Fix dangling refs (FIVE sites — GAP B adds the 5th)

The retired skill is referenced from 5 sites. Each repoints to CHIRON §7 (the capability's new home) or is reworded.

| # | File:loc | Before (quoted) | After |
|---|---|---|---|
| D6.1 | `substrate/install.sh:57` (comment) | `# POLYBIUS invokes via the Skill tool — agent-author for drafting new role` | Reword: drop `agent-author` example; e.g. `# POLYBIUS invokes via the Skill tool — handoff-author, team-launcher, etc.` (CHIRON's authoring is NOT a Skill-tool skill — do not list it as one). |
| D6.2 | `substrate/operating-disciplines.md:955` | `… via the agent-author skill or by hand.` | `… via MAJOR_CHIRON's agent-author capability (\`MAJOR_CHIRON.md\` §7) or by hand.` |
| D6.3 | `substrate/skills/check-substrate-updates/SKILL.md:58` | `… deploys to every consumer workspace alongside \`agent-author\`.` | Reword to a non-retired sibling: `… deploys to every consumer workspace alongside \`handoff-author\`.` (pick any skill still in SKILL_NAMES). |
| D6.4 | `substrate/skills/handoff-author/SKILL.md:185` | `- \`substrate/skills/agent-author/\` — sibling skill for agent authoring; handoffs are an output of an agent, not the agent itself.` | `- \`MAJOR_CHIRON.md\` §7 (the agent-author capability) — agent authoring lives in the CHIRON seat; handoffs are an output of an agent, not the agent itself.` |
| D6.5 (GAP B) | `substrate/MAJOR_POLYBIUS.md:618` (§19.7 cross-refs) | `… \`substrate/skills/agent-author/\` (skill for authoring project-team specialists); …` | `… \`MAJOR_CHIRON.md\` §7 (the agent-author capability — authoring project-team specialists); …` |

- **DoD grep scope (GAP C):** the DoD's `grep -rn "agent-author" substrate/ app/` will still match INTENDED CHIRON references (CHIRON §7 is literally "The agent-author capability"; the module header; the repointed refs above). **Scope the verification grep to exclude `substrate/arcs/` and `substrate/v1-historical/`** (the arc directive itself + historical files legitimately say "agent-author"). The grep is a *no-dangling-pointer* check, not a *no-occurrence* check — VERA reads each remaining match and confirms it is an intended CHIRON-capability reference, not a pointer to the retired `skills/agent-author/` dir. See Verification Probes §V5.

---

## D7 — App: update the stale test assertion (O3 — slot stays populated)

**File:** `app/src/data/__tests__/generated.test.ts`.
- **No adapter change** (`gen-data-lib.ts` `discoverSkillFiles` reads all skill dirs; 12→11 after retirement; the slot stays populated). Confirmed: 12 skill dirs today, `toBeGreaterThan(0)` stays true at 11.
- **Edit D7.1 — L92:** `expect(names).toContain("agent-author");`
  - Before: `expect(names).toContain("agent-author");`
  - After: **delete the assertion** (agent-author no longer exists as a skill). The surrounding assertions (L86 `toBeGreaterThan(0)`, L88-90 rank discriminator, L93-95 per-skill rank/kebab/desc) all still hold for the remaining 11. Optionally replace with a still-present skill, e.g. `expect(names).toContain("handoff-author");` — **delete is cleaner** (don't pin to another specific skill that a future arc might also re-home). Recommend delete.
- **Edit D7.2 — comment L84-85:** `// Arc 17 deployed agent-author; Arc 17.1 made the gen-data adapter / read it.` → update to note the Arc-61 retirement: `// Arc 17.1 made the gen-data adapter read all substrate skills as / LIEUTENANTs. (agent-author retired Arc 61; slot stays populated by the / remaining skills.)` Keeps the test's provenance honest.

---

## Recompose machinery — Checks A/B/C/D/E green-after-edit argument

The FAIL-LOUD `recompose_module_inline` (install.sh L1014+) runs once per owner at subproject tier. After the edits, here is why each check stays green for the two affected owners (POLYBIUS and CHIRON; op-disc/PLINY/DAEDALUS untouched).

**The single source of truth driving all checks: `pair-programmer-authoring.md` stays on disk in `substrate/modules/`; its marker pair moves POLYBIUS→CHIRON; its owned-set membership moves POLYBIUS→CHIRON. These three move together (atomic).**

| Check | What it asserts | POLYBIUS after edit | CHIRON after edit |
|---|---|---|---|
| **A** (global existence) | every marker references a real module source (owner-AGNOSTIC, built from filesystem glob) | POLYBIUS's 4 markers (onboarding, sub-project-spawning, pair-programming-prototyping, substrate-update-check) all reference existing sources → GREEN | CHIRON's 1 marker (pair-programmer-authoring) references `substrate/modules/pair-programmer-authoring.md` which **still exists** (file never moved) → GREEN |
| **B** (owned consumed) | every OWNED module has a marker in THIS file | POLYBIUS owned-set = {onboarding, sub-project-spawning, pair-programming-prototyping, substrate-update-check} — `pair-programmer-authoring` REMOVED from owned-set (D5.3) AND its marker REMOVED (D4.1/D5.1); the 4 remaining owned each have their marker → GREEN. *(If the marker were removed but the owned-set entry kept → Check B fires "body would be DROPPED" — which is exactly why the two edits are atomic.)* | CHIRON owned-set = {pair-programmer-authoring}; CHIRON has the marker (D5.2) → consumed=1 → GREEN. *(If the owned-set entry were added but the marker not → Check B fires. Atomic.)* |
| **C** (balance) | markers balanced, full-line, no nesting | POLYBIUS: 4 balanced pairs (the removed pair is cleanly deleted, both lines, no orphan) → GREEN | CHIRON: 1 balanced pair, full-line `^<!-- MODULE-INLINE:pair-programmer-authoring -->$` / `^<!-- /MODULE-INLINE:pair-programmer-authoring -->$` → GREEN |
| **D** (non-empty owner) | NOT (zero markers AND owned-modules-exist) | POLYBIUS has 4 markers (markers_seen=4>0) → Check D does not fire → GREEN | CHIRON has 1 marker (markers_seen=1>0) AND nowned=1 → Check D does not fire → GREEN. *(Check D would fire only if CHIRON had owned modules but ZERO markers — prevented by D5.2 adding the marker.)* |
| **E** (no marker-in-body) | the module BODY has no literal MODULE-INLINE line | unaffected (POLYBIUS's 4 module bodies unchanged) → GREEN | `pair-programmer-authoring.md` body must contain no `^<!-- /?MODULE-INLINE:` line — **grep-confirmed clean today**; the D5.4 body edits add no marker line → GREEN |

**Two NEW failure modes the edit introduces (both prevented by construction):**
1. **`$DEST_CHIRON` undefined when the recompose call runs.** Prevented by D2.2 setting `DEST_CHIRON` in the §2 MAJOR-deploy block (L932-938), which runs *before* the §3b recompose-call block. Plus CHIRON deploys to that path in D2.3 (so the file exists at subproject tier). The call is UNGATED (no WITH_CAPTAINS) because CHIRON always deploys.
2. **CHIRON's recompose call ordered before its deploy.** The §2 MAJOR-deploy block (L924-967) is far above the §3b call block (L1163+), so CHIRON's deployed file exists before recompose. No ordering hazard (unlike DAEDALUS, which deploys in the CAPTAIN loop and needs the call placed after it).

**Why no check needs silencing:** every green-ness above follows from *consistency* (marker present ⟺ module owned ⟺ source exists), not from suppressing a check. The atomic three-move (marker, partition entry, prose) is the mechanism that keeps consistency. ADA must land all three in one commit; landing any subset trips a real FAIL-LOUD check, which is the design working correctly.

---

## Verification probes (exact commands for VERA)

Run from the worktree root `.claude/worktrees/arc-61-build/`. All probes are re-executable; destructive ops use fixed literal paths (none here are destructive).

- **V1 — user-tier dry-run (recompose markers inert, deploy lines present):**
  `bash substrate/install.sh --target user --dry-run 2>&1 | grep -E "MAJOR_CHIRON|deploy: .*CHIRON"`
  EXPECT: a `[dry-run] deploy: …/MAJOR_CHIRON.md` line; NO recompose error (recompose is subproject-only; at user tier the markers are inert, no exit 2). Exit 0.

- **V2 — subproject-tier dry-run (the high-risk probe; all of A/B/C/D/E green):**
  Invoke install.sh with `--target subproject` and the required parent/subproject args (VERA confirms the exact flag set from `substrate/install.sh` usage; the subproject path sets `TARGET=subproject`, `SUFFIX_MAJORS=1`). With `--dry-run`, the recompose function prints `[dry-run] recompose (subproject): … (owned: …)` per owner and returns 0 WITHOUT running the awk checks (the dry-run early-return at L~1045). **So the dry-run proves the CALL WIRING (owner sets, call placement, no undefined var) but NOT the awk checks.** To exercise A/B/C/D/E for real, V3.
  EXPECT (V2): five `[dry-run] recompose (subproject):` lines — POLYBIUS (owned: onboarding sub-project-spawning pair-programming-prototyping substrate-update-check), op-disc, PLINY, CHIRON (owned: pair-programmer-authoring), DAEDALUS. CHIRON line present, `pair-programmer-authoring` NOT in the POLYBIUS line. Exit 0.

- **V3 — REAL subproject recompose (exercises awk Checks A–E; non-dry-run into a throwaway dest):**
  Run a real (`--dry-run` OFF) `--target subproject` install into a disposable scratch parent dir (fixed literal path, e.g. `/tmp/arc61-recompose-probe`), so `recompose_module_inline` actually runs the awk state-machine over the deployed CHIRON_<slug>.md + POLYBIUS_<slug>.md. EXPECT: `recomposed (subproject): …MAJOR_CHIRON_<slug>.md` and `…MAJOR_POLYBIUS_<slug>.md` success lines; exit 0; NO `install.sh: error: recompose:` line. Then assert the recomposed CHIRON file CONTAINS the pair-programmer-authoring body between its markers (`grep -c "Trigger recognition" <recomposed CHIRON>` ≥ 1) and the recomposed POLYBIUS file does NOT (`grep -c "Trigger recognition" <recomposed POLYBIUS>` = 0). This is the probe that actually falsifies "a body got dropped or double-hosted." VERA confirms the subproject invocation form against install.sh L768/L793.

- **V4 — app green:**
  `cd app && npm run gen-data && npm run build && npm test` — all exit 0. The generated.test.ts LIEUTENANT test passes with the L92 assertion removed; `discoverSkillFiles` finds 11 skills; `toBeGreaterThan(0)` holds.

- **V5 — no dangling skill refs (GAP-C-scoped):**
  `grep -rn "agent-author" substrate/ app/ | grep -v "substrate/arcs/" | grep -v "substrate/v1-historical/"`
  EXPECT: every remaining match is an INTENDED CHIRON-capability reference (CHIRON §7 heading/body, the module header provenance, the D6 repointed refs). ZERO matches pointing at the retired `substrate/skills/agent-author/` directory path. Specifically: `grep -rn "skills/agent-author" substrate/ app/ | grep -v arcs/ | grep -v v1-historical/` returns EMPTY (no path-pointer to the deleted dir). Plus `test ! -d substrate/skills/agent-author` (dir is gone) and `grep -c "agent-author" substrate/install.sh` shows SKILL_NAMES entry gone (only the L57 comment, if reworded, or zero).

- **V6 — voice audit (directive DoD):**
  `grep -rni "colonel" substrate/ --exclude-dir=v1-historical` → only deliberate reserved-rank refs.
  `grep -rni "the user" substrate/MAJOR_CHIRON.md` → only the §7 voice-rule definitions (L102-104, which define the rule).

- **V7 — authorship:**
  `grep -n "author" docs/major-chiron.html` → `<meta name="author" content="Denson Smith" />` unchanged; no other person named. CHIRON.md / module / test carry no false author field.

- **V8 — HTML/​.md parity (D1.3):** visual/textual diff of `docs/major-chiron.html` section structure against `substrate/MAJOR_CHIRON.md` — every §1-§11 heading in the .md has a corresponding rendered section; the draft-banner removal mirrored; the new §11 rendered (without MODULE-INLINE comment markers). Manual check by VERA.

---

## Self-assessed weak points (for ARGUS)

- **WP-1 (HIGHEST — dry-run does NOT exercise the awk checks).** `recompose_module_inline`'s dry-run path early-returns BEFORE the awk state-machine (L~1043-1046). So `--dry-run` proves call-wiring (owner sets, undefined-var safety, placement) but NOT Checks A/B/C/D/E themselves. The directive's DoD says "subproject-tier dry-run passes (the recompose FAIL-LOUD checks stay green)" — a dry-run alone CANNOT prove the checks green. **V3 (a real recompose into a throwaway dir) is mandatory to actually exercise A-E.** If ADA/VERA only run the dry-run, a marker/partition inconsistency would pass undetected until a real consumer subproject install. *Why this shape anyway:* the throwaway-real-install is the only way to drive the awk; flagged so VERA doesn't stop at the dry-run. ARGUS should confirm V3 is in the verification plan and the throwaway path is a fixed literal.

- **WP-2 (suffix-parity ambiguity).** The directive prose says CHIRON is "suffixed `CHIRON_<slug>` at project/subproject parallel to POLYBIUS/PLINY," but the install.sh code only suffixes MAJORs when `SUFFIX_MAJORS=1`, which is set ONLY at subproject tier (L793) — at PROJECT tier MAJORs are NOT suffixed (the `else` branch). My D2.2 mirrors POLYBIUS/PLINY exactly (suffix iff `SUFFIX_MAJORS=1`), so CHIRON gets parity by construction — but this means the directive's "project/subproject suffix" prose is imprecise (it's subproject-only suffixing). *Why this shape anyway:* parity-with-POLYBIUS is the safe reading and what the directive actually intends ("parallel to POLYBIUS/PLINY"). ARGUS should confirm ADA mirrors the existing MAJOR behavior, NOT the literal directive prose, and that project-tier non-suffixing is acceptable (it is what POLYBIUS does today).

- **WP-3 (relocation-index Class vocabulary).** D4.3 changes the §11 relocation-index Class from `CONDITIONAL` to a cross-seat relocation, but the index's existing Class vocabulary (L82-95) is CONDITIONAL/PROVENANCE/DUPLICATE — there may be no canonical "RELOCATED (cross-seat)" class. *Why this shape anyway:* the content genuinely moved to a different seat, which none of the three existing classes describes; a parenthetical is the honest representation. ARGUS should rule whether to coin a class, reuse CONDITIONAL with a note, or drop the row (since the module is no longer POLYBIUS-relocated content at all — arguably the row should be DELETED from POLYBIUS's index entirely, since POLYBIUS no longer owns or hosts it). I lean toward DELETE-the-row + a one-line "see CHIRON" pointer; flagged for ARGUS to decide.

- **WP-4 (CHIRON-hosted module with POLYBIUS cross-refs).** The re-homed module keeps several `MAJOR_POLYBIUS.md` cross-refs (§4.1, §7.1, §10.3, §12) because they point at still-POLYBIUS-owned content. This is intentional and minimal, but a CHIRON-hosted module pointing back into POLYBIUS reads slightly odd and risks confusing a future reader about ownership. *Why this shape anyway:* the alternative (duplicating §4.1/§7.1/§10.3/§12 content into CHIRON) is worse — it creates SSoT drift. The cross-refs are correct as long as none point at *moved* content. ARGUS should confirm each surviving POLYBIUS cross-ref still resolves to POLYBIUS-owned content (none of §4.1/§7.1/§10.3/§12 moved in this arc).

- **WP-5 (HTML regen is manual + unverifiable by build).** `docs/major-chiron.html` has no generator; D1.3 is hand-editing. There's no automated check that the HTML matches the .md — V8 is a manual VERA diff. Risk: the HTML drifts from the .md (e.g., §11 added to .md but forgotten in HTML). *Why this shape anyway:* building a renderer is out of scope; the sibling docs are all hand-authored the same way. ARGUS should note the HTML is a known-manual surface and confirm V8 is in the plan; consider a follow-up ticket for a doc-renderer if this recurs.

- **WP-6 (D6.1 reword judgment).** install.sh:57's comment lists `agent-author` as a Skill-tool skill POLYBIUS invokes. After retirement, the natural reword lists a different skill — but I must NOT reword it to say POLYBIUS invokes CHIRON's capability as a skill (CHIRON's authoring is NOT a Skill-tool skill; it's a seat capability). *Why this shape anyway:* the comment is about the Skill TOOL specifically; CHIRON §7 is instruction, not a skill. D6.1 picks a still-extant skill as the example. Low-risk but ARGUS should confirm the reword doesn't reintroduce the "POLYBIUS holds the authoring tool" error the whole arc is removing.

- **WP-7 (decision-surface skill not in SKILL_NAMES — out of scope, flagged).** Recon found `substrate/skills/decision-surface/` exists on disk but is NOT in `SKILL_NAMES` (so it deploys via `discoverSkillFiles` into the app's LIEUTENANT slot but does NOT deploy via install.sh's skill loop). This is a pre-existing inconsistency, NOT caused by this arc, and OUT OF SCOPE per the directive. *Flagged as a follow-up*, not designed-against here. ARGUS/POLYBIUS may want a ticket (fix-now-or-ticket per `stoa--8o4`).

---

## Out of scope (keeps ADA from scope-creep)

- **MAJOR_HAMILTON** (`stoa--yh2`) — separate arc; CHIRON lands independently.
- **The other p41 skill re-homings** (check-substrate-updates/check-bw-release → SessionStart triggers; save-verdict/validate-spec/inspect-script-output → modules; credential-discipline) — separate deliverables, NOT this arc.
- **decision-surface SKILL_NAMES inconsistency** (WP-7) — pre-existing, ticket-not-fix here.
- **A doc-renderer for `docs/*.html`** (WP-5) — would remove the manual-HTML-drift risk but is its own piece of work.
- **Full POLYBIUS canon audit** beyond the §11 cascade — flag-via-ticket, don't expand.
- **`substrate/v1-historical/` + archived arc directives** — legitimately reference the retired skill; excluded from the dangling-ref grep (GAP C).
