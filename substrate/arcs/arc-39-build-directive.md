# Arc 39 build directive — Pass 5 substrate bundle (2 candidates: utn + ezj)

## Context

Arc 39 is Pass 5 of the SPECIFICATION.md §13 workplan (post-Arc-38 substrate-architecture-batch ship). Two candidates bundled per §13.6:

- **C1: stoa--utn (P3)** — save-verdict skill promotion to substrate, with Python helper authoring (~150-300 LOC). Arc 23 ratified Option A: extend the schema at user-tier SKILL.md only; substrate promotion deferred to this ticket because the user-tier skill is prose-only (no `_save_verdict.py`, no `_lib/byte_copy.py` on disk). Promoting the broken state to substrate would deploy a known-broken skill to every Stoa-deployed project.
- **C2: stoa--ezj (P3)** — PRINCIPAL-intent probe discipline canon. Extends MAJOR_PLINY.md §7.2 (verify-then-execute) + adds POLYBIUS-side analog in MAJOR_POLYBIUS.md + cross-refs operating-disciplines.md §19 (confabulation). Includes the 2026-05-13 category-before-option refinement per the ezj comment thread.

Two candidates bundled per Arc 37/38 precedent (substantial-canon batches; not arbitrary deferral). C1 is Python-authoring shape (new for this seat-team); C2 is canon-prose shape (familiar).

## Architectural decisions A1-A20 (LOCKED unless explicitly flagged DAEDALUS-discretion)

### Bundle structure
- **A1 LOCKED**: single design.md document covering both candidates in one gauntlet. Per Arc 37/38 precedent. Sections: §1 utn / §2 ezj / §3 universal disciplines / §4 probes.

### C1 utn — save-verdict promotion
- **A2 DAEDALUS-discretion**: `_lib/byte_copy.py` scope. Two options:
  - **(α)** Single-skill private helper at `substrate/skills/save-verdict/_lib/byte_copy.py` — cross-skill share deferred to stoa--sp1 (port 7-8 utilities) where copy-artifact + transcribe-bw-to-disk will need the same primitive and can refactor it to a shared location at that time.
  - **(β)** Cross-skill share now at `substrate/skills/_lib/byte_copy.py` — would require also promoting copy-artifact + transcribe-bw-to-disk in this same arc (out of A20 scope as written) OR shipping the shared lib with no other consumers until sp1 ships (creates an unused-shared-lib state).
  - **User-tier leans α** (defer-cross-skill-share). Keeps Arc 39 scope tight; sp1 picks up the broader refactor with full N=3 consumer context.
- **A3 LOCKED**: substrate path = `substrate/skills/save-verdict/` (consistent with check-substrate-updates / handoff-author / agent-author paths).
- **A4 DAEDALUS-discretion**: SKILL.md prose modernization scope:
  - **(i)** Lift user-tier SKILL.md verbatim; modernize prose in a later arc (e.g., sp1 if sp1 broadens scope to include save-verdict prose-modernization, OR a dedicated arc later).
  - **(ii)** Lift-and-modernize at promotion time: drop gauntlet-era refs (`cu5.x`, `Captain Nestor`, "Major Pliny" with old taxonomy), use the-stoa role taxonomy (PRINCIPAL / POLYBIUS / PLINY / CAPTAIN_*), update verdict-path examples to the-stoa's `agents/verdicts/<ticket>/` convention.
  - **User-tier leans ii** (lift-and-modernize). Substrate canon should ship trailer-clean; modernizing at promotion time avoids a second touch later AND removes save-verdict from sp1's scope entirely (narrowing sp1 from 7-8 to 6-7 candidates as a beneficial side-effect).
- **A5 LOCKED**: install.sh wiring — `SKILL_NAMES` array (substrate/install.sh) += `save-verdict`. Deploys at all 3 tiers (user / project / subproject) per existing skill-deploy loop.
- **A6 DAEDALUS-discretion**: cross-refs from substrate canon to the newly-promoted save-verdict skill. User-tier leans CAPTAIN_VERA + CAPTAIN_CATO + CAPTAIN_ARGUS (the verdict-saving seats per the verdict-class agents), PLUS op-disc §5.7 verdict discussion. ADA/DAEDALUS/ZENO not cited (they don't save verdicts — they consume them or author other artifacts).
- **A7 LOCKED**: per Arc 23 §8.4 substrate-edit smoke-beat discipline + ticket utn deliverable 5: VERA probes exercise `install.sh --dry-run` at all 3 tiers + verify the deployed `_save_verdict.py` is executable + SKILL.md procedure step 9 runs end-to-end against the deployed helper.

### C2 ezj — PRINCIPAL-intent probe discipline canon
- **A8 LOCKED**: canon location = extend MAJOR_PLINY.md §7.2 (verify-then-execute) + add POLYBIUS-side analog in MAJOR_POLYBIUS.md (when relaying work items from PLINY to PRINCIPAL, surface unprobed-intent gaps explicitly) + cross-ref in operating-disciplines.md §19 (confabulation subtype). Per ticket "Substrate touch-point" enumeration.
- **A9 DAEDALUS-discretion**: 2026-05-13 category-before-option refinement scope:
  - **(γ)** Fold-in at canon-time — canon includes both the 3 sub-shapes (deliverable / audience / success-criteria unspecified) AND the category-before-option refinement (probe shape-of-thing before probing which-option-of-N).
  - **(δ)** 3-sub-shapes only; defer category-before-option refinement to a separate future arc.
  - **(ε)** Folded with explicit canonical-probe-sequence (the comment's 3-step sequence: category → shape-within-category → specifics-within-shape).
  - **User-tier leans γ or ε** (fold-in or fold-in-with-explicit-sequence). The refinement is canon-grade per the empirical anchor at 2026-05-13. DAEDALUS picks between γ (looser fold-in) and ε (more structured); user-tier weakly leans ε for clearer canonical phrasing.
- **A10 LOCKED**: cross-refs from new ezj canon — at minimum operating-disciplines.md §19 (confabulation); naming stoa--ioy + stoa--nvl + stoa--53u as the "four-discipline cluster" per ticket framing; refer back to MAJOR_PLINY.md §7.2 base + MAJOR_POLYBIUS.md analog from each direction.

### Universal (continued from Arc 38)
- **A11 LOCKED**: self-application per A14 Arc 38 family:
  - C1 utn: opportunistic — ADA may use the newly-promoted save-verdict skill during the build for its own verdict artifacts (smoke-check beyond the dry-run probes). Not required.
  - C2 ezj: none. Canon-prose-only addition.
- **A12 LOCKED**: §28 Co-Authored-By trailers per Arc 35 canon — all ADA + DAEDALUS commits inside arc-39/build MUST carry trailers. PLINY's PR-merge MUST preserve trailers per stoa--6wp (no `--body` override; let GitHub auto-concatenate OR include in HEREDOC). Spot-check ADA's first commit + spot-check squash-merge body post-merge per Arc 38 forward-fix pattern.
- **A13 LOCKED**: §5.10 signoff with live-verified state per §19.6 attestation-honesty. Never echo dispatch-authoring SHA as verified-at-attestation state. Cleanup attestations cite live-verified state at attestation time.
- **A14 LOCKED**: `[from: pliny-the-stoa]` author tag on all PLINY heartbeats per Arc 36 §7.1 5th beat + §7.7. POLYBIUS_the_stoa coordination uses `[from: polybius-the-stoa]`. Cross-tier comments to user-tier POLYBIUS use `[for: user-tier-polybius] [from: <self>]`.
- **A15 LOCKED**: cron renewal — polling cron + +144h renewal already set up by both project-tier seats at priming (POLYBIUS cron ids `b6e8630b` / `3c1e575b`; PLINY cron ids `abc905a6` / `6e69c60a`). Do NOT recreate; reuse the existing crons. Per §11 step 1.5.
- **A16 LOCKED**: cite-comment discipline per A17 Arc 38 — every cross-ref between new save-verdict / extended MAJOR_PLINY.md §7.2 / extended MAJOR_POLYBIUS.md analog / op-disc §19 cross-ref must resolve via cite at every read-site.
- **A17 LOCKED**: authorship attribution IMMUTABLE per CLAUDE.md global rule. **New file `substrate/skills/save-verdict/SKILL.md` MUST carry `author: Denson Smith` frontmatter** per Arc 27 stoa--uly convention. Verify pre-commit; ZENO mechanical-check confirms in Phase 3.
- **A18 LOCKED**: source-ticket closure per A19 Arc 38 — on Arc 39 ship, close stoa--utn + stoa--ezj with cross-refs to merge commit + audit comments per candidate. Tag `[for: user-tier-polybius]` on stoa--utn (work-unit + parent for this arc).
- **A19 LOCKED**: pre-branch hygiene per §5.9 + worktree convention per §5.9.4. Use separate worktree at `.claude/worktrees/arc-39-build/`. Pre-flight verify: `git branch | grep -E '^\s*arc-[0-9]+/build$'` is empty + local main = origin/main + no orphan arc-build branches.
- **A20 LOCKED**: out-of-scope hard-locks (Arc 39-specific):
  - No promoting copy-artifact / transcribe-bw-to-disk in this arc (sp1 scope; A2 α pick keeps them out).
  - No auto-validation of arbitrary verdict bodies against JSONSchema (per utn out-of-scope; Arc 23 A6 LOCKED).
  - No refactoring existing PASS / FAIL / NEEDS-REVISIONS verdict path (per utn out-of-scope).
  - No widening ezj canon to non-PLINY / non-POLYBIUS seats (the discipline is dispatch-time + relay-time specific).
  - No retroactive modernization of OTHER user-tier obsolete skills (sp1 scope).

### Arc-shaping
- **A21 LOCKED (clarification)**: bw-signal dispatch model — Arc 39 was dispatched via bw comment on stoa--utn (`[for: pliny-the-stoa]` + `[for: polybius-the-stoa]` tags), NOT via PRINCIPAL paste-to-session. PLINY + POLYBIUS_the_stoa picked up the signal via their priming-set polling crons. At close, PLINY comments back on stoa--utn with `[for: user-tier-polybius]` clean-PASS verdict. §5.11 archival of HUMAN_paste-pliny-arc-39 + HUMAN_paste-polybius-arc-39 + this directive to `substrate/arcs/arc-39/pastes/` via git mv.
- **A22 LOCKED**: CATO MANDATORY for this arc per sequence rationale — multi-arc sequence to Pass 9 validate-spec means cumulative craft scrutiny matters; Arc 39 introduces Python-authoring shape (different defect class than canon-edit arcs); extra craft scrutiny justified.

## DAEDALUS sub-decisions summary

| ID | Decision | User-tier lean | DAEDALUS picks at design |
|---|---|---|---|
| A2 | `_lib/byte_copy.py` scope | α (single-skill private) | yes |
| A4 | SKILL.md modernization | ii (lift-and-modernize) | yes |
| A6 | utn cross-refs | VERA + CATO + ARGUS + op-disc §5.7 | yes |
| A9 | ezj category-before-option fold-in | γ or ε (fold-in; ε for explicit sequence) | yes |

Each is DAEDALUS-discretion UNLESS exceeding (e.g., A2 spike reveals copy-artifact / transcribe-bw-to-disk depend on byte_copy in a way that forces β; A9 prose authoring reveals the refinement doesn't fit canon shape cleanly) — then surface as PRINCIPAL-gate per §25.

## Self-application observations to watch for stoa--bbi accretion

Arc 39 ships utn (Python authoring shape) + ezj (canon refinement). Per stoa--bbi refined principle ("structural fixes narrow drift surface but require propagation discipline + iteration"):

- utn first instance of substrate-canon Python skill (vs. shell skills already in substrate). Propagation surfaces: does install.sh handle Python helpers as cleanly as shell? Does the dry-run smoke-check exercise the Python end-to-end? Note any friction as N-evidence accretion.
- ezj canon refinement (category-before-option) is itself a structural-fix-of-detection-class — extending verify-then-execute to PRINCIPAL-intent dependencies. Watch for the canon adoption pattern: does the new discipline propagate organically to MAJOR_POLYBIUS.md analog without prompting? Note as N-evidence.

## Ship gate

Arc 39 ships when:
- design.md cleared by ARGUS (rev cycles per DAEDALUS judgment)
- ADA build complete; ZENO 11/11 PASS on mechanical checks (A18 frontmatter / §28 trailer / install.sh wiring / file existence / etc.)
- VERA falsification PASS on all probes
- CATO craft + scope review PASS
- Phase 4: squash-merge with trailer preservation (forward of bb12806 regression); cleanup verified; pastes archived per §5.11
- §5.10 signoff with live-verified state
- Source tickets closed per A18; `[for: user-tier-polybius]` tag on stoa--utn
