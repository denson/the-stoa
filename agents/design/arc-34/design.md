# Arc 34 design — Canonification batch 2 (C1-C4)

**Ticket:** `stoa--y14`
**Branch:** `arc-34/build` (created by PLINY in separate worktree at `.claude/worktrees/arc-34-build/` per `MAJOR_PLINY.md` §5.9.4)
**Date:** 2026-05-17
**Status:** rev2 — revision addressing ARGUS NEEDS_REVISION on C2 archive-path navigation accuracy
**Directive:** `substrate/arcs/arc-34-build-directive.md` (A1-A12 LOCKED)
**Authored by:** CAPTAIN_DAEDALUS_the_stoa, on behalf of the PRINCIPAL (Denson Smith).

---

## §1 — Overview

Arc 34 ships four small substrate-canon tightenings (C1-C4) as a single coherent canonification arc — the second instance of the bundling pattern Arc 32 (`stoa--ewn`) established. Each candidate has an empirical anchor surfaced today, a small surface area, and a clear fix shape: **C1** encodes the user-tier-POLYBIUS-to-main commit discipline that has been operating implicitly (~10+ direct-to-main commits per session, recurring); **C2** encodes the arc-close `HUMAN_paste-*.md` archival convention as a forward-only convention (14+ accumulated paste files at workspace root); **C3** is a cosmetic fix to `substrate/templates/paste-instruction-template.md`'s title + first paragraph to reflect Arc 32 C2's dual PLINY+POLYBIUS targeting; **C4** encodes a HITL-paused-queue-sweep discipline (defense in depth: POLYBIUS activation checklist step + handoff-doc-template section) after the empirical anchor of `stoa--jru` sitting paused for ~2 weeks without surfacing.

All four candidates share the theme "encode-as-canon what has been operating ad-hoc, OR add a structural surface to a gap that operated invisibly," and the per-candidate edits are mostly section additions or in-place line edits with no destructive rewrites. The bundling is justified by surface-disjointness (per `MAJOR_PLINY.md` §6.3) — C1 touches MAJOR_POLYBIUS.md + /CLAUDE.md; C2 touches MAJOR_PLINY.md; C3 touches paste-instruction-template.md; C4 touches MAJOR_POLYBIUS.md (a different section than C1) + handoff-doc-template.md. The four edit surfaces do not collide; a single ARGUS cold-read, single ADA build, single VERA+CATO+ZENO pass is appropriate per A1.

---

## §2 — Sub-decisions

This arc has three DAEDALUS sub-decisions (the user-tier POLYBIUS lean is recorded in the directive A2/A3/A5 prose; DAEDALUS confirms each pick with rationale). **C3 is locked scope by A4 — DAEDALUS picks only the exact wording, not a structural option.** All four sub-decisions align with the user-tier lean; no substance disagreement surfaces.

### §2.1 — A2 / C1: Option C (composite — discipline section + /CLAUDE.md cross-ref)

**Pick: Option C.** User-tier POLYBIUS lean confirmed.

**Rationale.** The empirical anchor is recurring (~10+ direct-to-main commits per session, every session). The CLAUDE.md rule "Forward work happens on a feature branch, not on `main`" reads as universal but the operational truth has an implicit exception for user-tier housekeeping. Option B (strict — everything through an arc) is rejected because it would require a full PLINY arc for every small housekeeping change (the dispatch+gauntlet+merge+cleanup overhead is ~30 min vs. ~5 min for a direct commit; the cost-calculus does not justify it for housekeeping). Option A (discipline section only, leaving CLAUDE.md unchanged) is rejected because the CLAUDE.md universal-rule prose is itself part of the brittle pattern — a future POLYBIUS reading CLAUDE.md cold either over-applies (refuses to land any direct-to-main commit) or under-applies (interprets "forward work" narrowly). Option C closes both halves: the substantive enumeration lives in the canon section; the /CLAUDE.md rule explicitly cross-refs the canon section so the universal-rule prose stops being self-contained false-universal.

**Locus pick:** new top-level **§18 in `substrate/MAJOR_POLYBIUS.md`** (sitting after §17 Base-vs-custom and before the closing `---` + `Standby, run.` at the file end). Rationale: the discipline is about how user-tier POLYBIUS operates against the project's main branch — a peer-of-§17 substrate-tier framing (§17 covers base-vs-custom file lifecycle; §18 covers user-tier commit-to-main lifecycle). A §5.x family member was considered (the §5 family is onboarding-shaped) but rejected because the user-tier-to-main discipline fires throughout the engagement, not at onboarding time. A §4.x discipline rejected because §4 is empirically-derived-disciplines-with-anchors; §18 belongs as a structural-framing section sibling to §16 (POLYBIUS session lifecycle) and §17 (base vs custom).

The discipline is the-stoa-specific in its examples (the substrate-tool self-apply, the directive-tracking commits, the orphan-cleanup commits all reference operations on the-stoa repo) — but the canon section is universal-shape (POLYBIUS at user-tier in ANY project may operate against that project's main branch the same way). The substrate-shipped form is universal; the §18 prose names the categories abstractly with the-stoa as the worked-example anchor.

### §2.2 — A3 / C2: Option α (archive on arc close to `substrate/arcs/arc-<N>/pastes/`)

**Pick: Option α.** User-tier POLYBIUS lean confirmed.

**Rationale.** The empirical anchor is observable accumulation (24 paste files at workspace root today across arcs 21-34, growing every arc). Option β (delete on arc close) loses the historical record without git-history overhead being free — `git log --follow` against a deleted file is operationally clumsy; the archive path is one `ls` away. Option γ (leave + accept) is rejected because the directory listing degrades as a navigational surface (the cron-hygiene paste from Arc 21 is still in `ls HUMAN_paste-*.md` output today). Option α parallels the existing `substrate/arcs/arc-<N>-build-directive.md` archival pattern AND shares its `arc-<N>` prefix — a future POLYBIUS running `ls substrate/arcs/ | grep arc-27` finds the flat-file directive `arc-27-build-directive.md` AND the subdirectory `arc-27/pastes/` adjacent in the listing, both prefix-keyed on the same arc number.

**Path-shape rev2 note.** Rev1 of this design proposed `substrate/arcs/<N>/pastes/` (bare arc number), which would have placed the pastes subdirectory at `substrate/arcs/27/pastes/` while the directive remained at the flat path `substrate/arcs/arc-27-build-directive.md`. ARGUS surfaced that the bare-number form modeled a false navigation neighborhood: `ls substrate/arcs/27/` would have shown only `pastes/`, with no directive present, forcing a relocate-to-flat-file lookup. Rev2 uses the `arc-<N>` prefix form so directive + paste-subdirectory share the same lexicographic prefix and appear adjacent under `ls substrate/arcs/ | grep arc-<N>`. The fix is structural, not just prose-cosmetic: it solves the actual navigation friction rather than describing it honestly.

**Locus pick:** new sub-subsection **§5.11 in `substrate/MAJOR_PLINY.md`** (sitting after §5.10 Signoff-accuracy — the Arc 32 / `stoa--ewn` ship — and before the §5 family's closing `---` at MAJOR_PLINY.md:462). Rationale: §5 is "The gauntlet pipeline" and §5.10 is the closing-beat signoff-accuracy discipline; §5.11 is the closing-beat-cleanup-action that signoff-accuracy verifies. Same family as §5.9 (pre-branch hygiene at opening), §5.9.4 (worktree convention at branch creation), §5.10 (signoff-accuracy at close), §5.11 (paste archival at close) — all arc-boundary operational hygiene at PLINY's seat. The user-tier POLYBIUS lean named "alongside §5.10 (same family: arc-close discipline)"; §5.11 is the literal "alongside" placement.

**Forward-only convention.** The new §5.11 discipline applies to Arc 34 and forward; it does NOT backfill the 24 historical paste files at workspace root (per A8 hard-lock pattern — "Backfill of pre-Arc-34 existing paste files" is explicitly out of scope). Future user-tier POLYBIUS can file a separate housekeeping ticket for the backfill if PRINCIPAL approves; that is NOT this arc's work.

**Cleanup-sequence extension to §5.10.** §5.10's verification rule covers branch deletion, worktree removal, file cleanup, and process/cron teardown today; the paste-archival action is a new "file cleanup" sub-case that §5.10 must surface for verification (the signoff must verify the pastes are at the archive location AND removed from workspace root). Rather than inserting a new bullet into the §5.10 enumeration mid-arc — which would re-open the Arc 32 / C3 canon prose, a discipline collision — §5.11's own body names the §5.10 verification rule and enumerates the specific check (`ls substrate/arcs/arc-<N>/pastes/` should show both files; `ls HUMAN_paste-*-arc-<N>-*.md` at workspace root should return empty). This keeps §5.10's prose stable and §5.11 self-contained.

### §2.3 — A4 / C3: locked-scope cosmetic fix (DAEDALUS picks exact wording)

**Pick: dual-targeting wording per below.** No structural option to pick (A4 LOCKS scope as cosmetic).

**Current state.** `substrate/templates/paste-instruction-template.md` lines 5-7:

```
# Paste-instruction template — MAJOR_PLINY activation

The template MAJOR_POLYBIUS fills per session to produce the paste-instruction that activates MAJOR_PLINY (the ORCHESTRATOR) in a fresh terminal.
```

**Drift.** Arc 32 / C2 (`stoa--ewn`) extended the template's `{{CRON_HYGIENE_CLAUSE}}` slot to apply to both PLINY-targeted AND POLYBIUS-targeted activation pastes (per `MAJOR_POLYBIUS.md` §5.1.3). The template's title + first paragraph still scope to PLINY-only, which contradicts the body's dual-targeting reality. Three POLYBIUS-targeted pastes (`HUMAN_paste-polybius-arc-32`, `-33`, `-34-instruction.md`) at workspace root today are filled from this template; a future POLYBIUS reading the template cold reads "MAJOR_PLINY activation" and either (a) authors the POLYBIUS paste from a different template they invent, or (b) authors the POLYBIUS paste from this template but is uncertain whether the slot semantics apply.

**Exact wording picked.** Line 5 (title):

```
# Paste-instruction template — MAJOR_PLINY and MAJOR_POLYBIUS activation
```

Line 7 (first paragraph) — extended to name both targets explicitly:

```
The template MAJOR_POLYBIUS fills per session to produce the paste-instruction that activates MAJOR_PLINY (the ORCHESTRATOR), or that user-tier MAJOR_POLYBIUS fills to activate a project-tier MAJOR_POLYBIUS, in a fresh terminal. The static role files (`MAJOR_PLINY.md`, `MAJOR_POLYBIUS.md`) are universal; the wrapper that activates them is session-specific. The filling seat (typically POLYBIUS) fills the slots from its conversation with the PRINCIPAL, writes the filled result to disk under `HUMAN_paste-<target>-instruction.md` (e.g., `HUMAN_paste-orchestrator-instruction.md` for PLINY, `HUMAN_paste-polybius-arc-<N>-instruction.md` for a POLYBIUS-targeted arc dispatch), and hands the PRINCIPAL a one-line pointer.
```

**Wording rationale.** The picked title names both targets coordinately ("and" rather than "/" or "&"); avoids the awkward "PLINY-targeted and POLYBIUS-targeted" phrasing in the title itself. The first paragraph extends rather than rewrites — the substantive verbatim from the original ("the wrapper that activates them is session-specific," "writes the filled result to disk … hands the PRINCIPAL a one-line pointer") is preserved; the dual-targeting reality + the differentiated on-disk filename convention are inlined. The change does NOT touch the substitution-slots table, the slot rationale section, the template body, the worked example, or any other downstream section — only the title + the opening framing paragraph. C3 is genuinely cosmetic; the option-α/β/γ structural decision space ARGUS may ask about (rename the file? split into two templates?) is hard-locked out by A4 ("do NOT split into two templates; do NOT redesign the slot set").

### §2.4 — A5 / C4: Option γ (defense in depth — POLYBIUS activation step + handoff-doc-template section)

**Pick: Option γ.** User-tier POLYBIUS lean confirmed.

**Rationale.** The empirical anchor is `stoa--jru` (Arc 22 coordination hygiene) sitting HITL-paused-pre-dispatch from 2026-05-04 to 2026-05-17 — ~2 weeks of multiple POLYBIUS sessions defaulting to PRINCIPAL's current direction without sweeping the queue. The HITL gate worked correctly (didn't auto-dispatch); the gap was no mechanism to surface "you have an open HITL-paused epic" to PRINCIPAL across the gap.

Option α alone (activation-checklist step) closes the gap at every new POLYBIUS session-start but misses the in-session refresh case — a long-running POLYBIUS session that handed off to itself via Mode 1 compaction recovery (per `MAJOR_POLYBIUS.md` §16.2) doesn't re-run the activation checklist on every `/compact`. Option β alone (handoff-doc-template section) closes the gap at Mode 2 handoff time (rare per §16.2) but misses the fresh-activation case where no prior handoff exists. Option γ (both) is the defense-in-depth shape that fires at BOTH lifecycle points: fresh activation (step) AND handoff authoring (template section). The cost of duplication is small — each carrier is one paragraph; the failure mode of relying on a single carrier is the exact 2-week invisibility pattern stoa--jru exhibited.

**Locus 1 pick:** new step **after `bw prime` (current step 2)** in `substrate/MAJOR_POLYBIUS.md` §9 activation checklist — renumbering current steps 3-7 as 4-8. Rationale: the sweep needs to fire AFTER `bw prime` because `bw prime` is what produces the open-tickets list the sweep reads; the sweep needs to fire BEFORE step 3 (read recent comments on relevant tickets) because the sweep itself adds tickets to "relevant" via HITL-paused recognition. Inserting after step 2 places the sweep at the natural data-flow point.

**Locus 2 pick:** new section **"HITL-paused queue"** in `substrate/templates/handoff-doc-template.md` template body, inserted between the existing **"Where the bw repos live"** section (line 89-91 in the template body) and the existing **"State that shapes POLYBIUS behavior"** section (line 93-95). Rationale: HITL-paused-queue is open-work-state — same conceptual neighborhood as the bw repo table (navigation aid for open work) and the state-shapes-behavior section (open watch-out items). The placement between them keeps the open-work-state cluster contiguous in the rendered handoff.

The carrier 2 template addition needs a new substitution slot — `{{HITL_PAUSED_QUEUE}}` — added to the template's slot table + slot-rationale section + template body in coordinated edits (mirroring how Arc 32 / C2 added `{{CRON_HYGIENE_CLAUSE}}` to the paste-instruction template).

---

## §3 — Per-candidate design

The four candidates are designed independently in §3.1-§3.4. Cross-refs between candidates resolve per A6: C2 cross-refs §5.10 (Arc 32 / `stoa--ewn`'s signoff-accuracy section); C4 carrier 1 cross-refs §16.2 (POLYBIUS session lifecycle modes — to explain why both lifecycle points need a carrier); C4 carrier 2 cross-refs §16.3 (handoff is multi-artifact). C1 stands alone (no cross-refs to other Arc 34 candidates). C3 stands alone (cosmetic fix; references only Arc 32 / C2 § 5.1.3 transitively via the already-canonized `{{CRON_HYGIENE_CLAUSE}}` slot mechanism).

### §3.1 — C1: User-tier-to-main commit discipline (§18 in MAJOR_POLYBIUS.md + /CLAUDE.md cross-ref)

**Target files:**
- `substrate/MAJOR_POLYBIUS.md` — new top-level §18
- `/CLAUDE.md` (project-root, at the worktree's `../../../CLAUDE.md` equivalent of `C:\Users\denso\claude_projects\the-stoa\CLAUDE.md`) — single-line cross-ref edit

**Insertion-point (MAJOR_POLYBIUS.md):** the §17 family closes at `MAJOR_POLYBIUS.md:1121` (the §17.6 Cross-references bullet list end), then `---` separator at line 1122, then `Standby, run.` at line 1125. New §18 inserts BETWEEN the `---` at line 1122 and `Standby, run.` at line 1125 — preceded by a fresh `---` separator so it sits as a top-level peer of §17 rather than appended after the file's closing separator.

Required post-build order in the §17.6-close → file-end window:

```
<MAJOR_POLYBIUS.md:1121 = §17.6 Cross-references close>
<blank line>
---
<blank line>
## 18. User-tier POLYBIUS direct-commit discipline (the-stoa-specific application of the canon)
<C1 body prose>
<blank line>
---
<blank line>
Standby, run.
<EOF>
```

**Locus rationale:**

- §17 (Base vs custom) is the existing "what files the substrate owns vs the workspace owns" canon — a substrate-tier framing of who-owns-what at the file level. §18 extends the framing to who-may-commit-what at the git-ref level — same conceptual layer (substrate-vs-workspace ownership), different unit-of-analysis (file → commit).
- Alternative §4.x discipline rejected because §4 is empirically-derived-disciplines-with-anchors (Principal-as-router antipattern, verify-then-execute, etc.); the user-tier-to-main discipline is operational-framework, not a discipline-against-a-failure-mode.
- Alternative `operating-disciplines.md` universal-team rejected because the discipline is POLYBIUS-specific (no other seat creates direct-to-main commits under the gauntlet pipeline today — PLINY operates on arc-build branches; CAPTAINs do not commit; ZENO does not commit; only user-tier POLYBIUS exercises the direct-to-main path). A thin universal-team cross-ref at operating-disciplines.md is not added because no other seat exercises the discipline today — same shape as Arc 32 §5.10's locus-rationale where C3 was kept PLINY-envelope rather than promoted to universal-team. If a future seat exercises the discipline, a thin cross-ref can be added at that future arc.

**Verbatim canon prose ADA must write — Carrier 1, MAJOR_POLYBIUS.md §18** (paste as new top-level section between the `---` at line 1122 and `Standby, run.` at line 1125, with a preceding fresh `---` separator):

```markdown
## 18. User-tier POLYBIUS direct-commit discipline (the-stoa-specific application of the canon)

User-tier POLYBIUS operating in the-stoa workspace may direct-commit to local main for a bounded set of housekeeping operations. The project-root `CLAUDE.md` rule "Forward work happens on a feature branch, not on `main`" is universal for substantive forward work AND has an explicit exception for user-tier housekeeping as enumerated below. This section names the exception explicitly so future user-tier POLYBIUSes neither over-apply the universal rule (refusing to land hygiene commits that ought to land) nor under-apply it (interpreting "forward work" so narrowly that substantive substrate changes leak into direct-to-main commits).

The discipline is the-stoa-specific in its examples but universal-shape in its structure: ANY project where user-tier POLYBIUS operates against the project's main branch may instantiate the same exception list per that project's `CLAUDE.md`. The shape is "name the exceptions, cross-ref them from the project's CLAUDE.md so the universal-rule prose stops being self-contained false-universal."

### 18.1 What user-tier POLYBIUS MAY direct-commit to main

The following housekeeping operations are bounded, low-risk, and frequent enough that gating them on a full arc dispatch is over-process for the actual surface:

- **Arc directive + activation paste tracking commits.** When user-tier POLYBIUS authors a new arc directive at `substrate/arcs/arc-N-build-directive.md` AND the paired activation pastes at `HUMAN_paste-{pliny,polybius}-arc-N-instruction.md`, the tracking commit that lands these three artifacts on main happens BEFORE the arc dispatches and is structurally distinct from the arc's substantive work (which happens on `arc-N/build`). The tracking commit's purpose is durability + reviewability of the dispatch artifacts themselves; the arc's actual ship is the separate PR-merge commit after the gauntlet.
- **Substrate-tool self-apply commits.** When user-tier POLYBIUS runs `substrate/skills/check-substrate-updates/apply.sh` against the-stoa workspace (the workspace where the substrate canon itself lives — i.e., re-syncing the deployed substrate to its own source canon after an upstream substrate edit), the resulting file edits are mechanical re-deploys; the substantive change already shipped via the arc that authored the source canon. Self-apply commits are recovery-from-drift, not new work.
- **Orphan cleanup commits.** When user-tier POLYBIUS removes a stale worktree directory (e.g., the `.claude/worktrees/arc-27-build/` orphan surfaced during the Arc 34 dispatch), deletes a stale local branch that no longer has a remote counterpart, or removes a stale `.bw/` directory from a non-bw worktree, the cleanup is hygiene against state that should never have persisted.
- **Retrospective docs at `docs/sessions/`.** When user-tier POLYBIUS authors a session retrospective at `docs/sessions/<date>-<slug>--retro.md`, the doc captures past-engagement narrative — it is durable-memory-substrate, not forward-work. The doc's content is not subject to the gauntlet (it is not substrate canon; future POLYBIUSes read it as historical context, not as authoritative discipline).
- **`bw` operations.** All bw commands operate on the orphan `beadwork` branch, not on main (per `operating-disciplines.md` §12 bw cookbook). bw comments, ticket creates, ticket closes, etc. land on the bw branch automatically; they NEVER touch main. The bw operations are listed here for completeness of the "what user-tier may do during a session without dispatching an arc" picture — bw is always safe because it does not interact with the main-vs-arc-build branch distinction at all.

### 18.2 What user-tier POLYBIUS does NOT direct-commit to main (requires an arc)

Anything that PLINY's gauntlet would normally cover requires an arc dispatch:

- **Substrate canon edits.** `substrate/MAJOR_*.md`, `substrate/CAPTAIN_*.md`, `substrate/operating-disciplines.md`, `substrate/templates/*`, `substrate/skills/*`. These are the substrate's source-of-truth; edits ship via the gauntlet (DAEDALUS → ARGUS → ADA → VERA → CATO → ZENO) so the redundant-checker property holds.
- **Substrate tooling source changes.** `substrate/install.sh`, `substrate/skills/check-substrate-updates/check.sh`, `substrate/skills/check-substrate-updates/apply.sh`, and any other source file under `substrate/` that is itself canonical-deploy-mechanism. Tooling regressions break every downstream project; the gauntlet's verification disciplines (VERA probes, CATO cold-read) are load-bearing.
- **App code at `app/`.** The Stoa app's source files (`app/src/`, `app/package.json`, `app/vite.config.ts`, etc.) ship via arc per the project-root `CLAUDE.md` discipline ("substantive forward work on a feature branch"). The `gen-data` adapter, Zod schemas, and UI components are app-tier substantive work.
- **Case-study documents at `docs/case-study/`.** Public-facing narrative + the standalone presentation HTML are brand-defining surface — the `MAJOR_POLYBIUS.md` §4.6 autonomous-ship discipline already gates these.
- **Anything that touches an author-like field.** Per the project-root `CLAUDE.md` authorship-attribution discipline + `MAJOR_POLYBIUS.md` §15 N=1 honest-scope, any change to an `author:` / `owner:` / `creator:` / `by:` / `copyright:` field surfaces to PRINCIPAL before commit regardless of which branch.

### 18.3 Bundled-squash interaction (cross-ref to MAJOR_PLINY.md §5.9)

Direct-to-main housekeeping commits create local-ahead state that interacts with the pre-branch hygiene discipline at `MAJOR_PLINY.md` §5.9. Specifically, §5.9 check 2 (local main = origin/main) fails when user-tier POLYBIUS has just landed a direct-to-main commit and not yet pushed. The discipline is: **push immediately after every direct-to-main commit**, so that local main = origin/main when the next PLINY arc dispatches and the pre-branch hygiene check passes.

The push-immediately discipline is load-bearing because PLINY's check 2 cannot distinguish "operator forgot to push a routine housekeeping commit" from "operator landed something the arc should pick up" — the safe default is for user-tier POLYBIUS to push before standing down or before signaling arc dispatch to PRINCIPAL. The cost of a push is one network round-trip; the cost of bundling unintended pre-existing commits into the arc squash is the bundled-squash failure mode `MAJOR_PLINY.md` §5.9 exists to prevent.

### 18.4 PR-history readability — housekeeping commits visible as standalone

Housekeeping commits land directly on main and appear in `git log` between arc-PR-squash commits. This is a deliberate property, not a failure mode: arc PRs carry coherent scope statements (PR titles like "Arc 33: mechanical-script / agent-inspection split — substrate pattern + worked-example deployment"); housekeeping commits carry small honest subjects ("track arc-34 directive + activation pastes (canonification batch 2)", "narrow .gitignore", etc.). A reader walking the history sees the arc PRs as the substantive ship boundaries and the housekeeping commits as the small-fixes-between-arcs that the user-tier housekeeping discipline authorizes.

The alternative — bundling housekeeping into a "weekly hygiene" PR — was considered and rejected because it would re-introduce the bundled-scope problem that the §5.9 pre-branch hygiene discipline already addresses for arc-build squashes: a bundled-hygiene PR's commit subject cannot accurately describe its mixed contents, and CATO review on it is wider than the discipline's per-fix scope justifies. Per-fix direct-commits to main, each with its own narrow subject, is the readable form.

### 18.5 N=1 provenance + accretion path

Per `MAJOR_POLYBIUS.md` §15 honest-scope and `operating-disciplines.md` §6.7.1: PRINCIPAL declared this discipline on 2026-05-17 (project-direction authority, captured at `stoa--k36` thread + the Arc 34 directive A2 LOCK). §6.7.1 defers to the canon-promotion gate (multiple observations across distinct defect classes + controlled comparison + substrate-level pattern); §6.7.1 does not carve out a separate "PRINCIPAL-declaration shortcut." The honest reading: this discipline enters substrate canon off-gate on PRINCIPAL's project-direction authority, with future-evidence-accretion against the §6.7.1 gate still required for promotion to "structural lesson" status.

The supporting evidence at the time of this writing (2026-05-17):

- **N=multi bit-by-it (the implicit-exception pattern):** every user-tier POLYBIUS session since the substrate's first cross-tier engagement has carried direct-to-main housekeeping commits; ~10+ today's session alone (per `stoa--k36` body). The pattern is well-established as practice; what is new is the canon making the practice explicit.
- **N=0 worked-when-applied (controlled comparison):** no user-tier POLYBIUS session has yet operated under the explicitly-encoded discipline; accretes as future sessions ship under §18 and surface either successful application or fresh failure modes (e.g., a session that direct-commits something §18.2 should have arc-gated).

The discipline is in substrate canon NOW because PRINCIPAL named it today and the implicit-exception pattern is observable across every prior session; promotion to "structural lesson" status with multi-arc empirical backing under the encoded canon is future arcs' work, not this arc's. Same N=1 framing as Arc 27's `MAJOR_POLYBIUS.md` §16.6, Arc 28's `operating-disciplines.md` §22.3, Arc 29's §17.5, Arc 30's `MAJOR_PLINY.md` §5.9.3, Arc 31's `operating-disciplines.md` §25.6, and Arc 32's `MAJOR_PLINY.md` §5.10.3 / §5.9.4.1 / `MAJOR_POLYBIUS.md` §5.1.3 / `operating-disciplines.md` §19.6.4.

### 18.6 Cross-references

- Project-root `CLAUDE.md` — the universal-rule prose "Forward work happens on a feature branch, not on `main`" cross-refs THIS section as the explicit-exception canon (per Arc 34 / C1 Option C composite edit).
- `MAJOR_PLINY.md` §5.9 — pre-branch hygiene check 2 (local main = origin/main); §18.3 above names the push-immediately discipline that keeps check 2 passing.
- `MAJOR_POLYBIUS.md` §15 — N=1 honest-scope, the gate this section's claims pass through.
- `operating-disciplines.md` §6.7.1 — the canon-promotion gate this discipline enters off-gate on PRINCIPAL's project-direction authority.
- `operating-disciplines.md` §12 — bw cookbook; the bw operations §18.1 names operate on the orphan `beadwork` branch, never on main.
- Empirical anchor: `stoa--k36` (2026-05-17 user-tier POLYBIUS end-of-session hygiene audit; folded as C1 in Arc 34).
```

**Verbatim canon prose ADA must write — Carrier 2, project-root `/CLAUDE.md`** (single in-place edit to the "Forward work happens on a feature branch, not on `main`" sentence at line 39 in the worktree's `CLAUDE.md`; the file path is the project's CLAUDE.md, NOT the worktree's `.claude/.../CLAUDE.md`).

**Current state at `/CLAUDE.md` line 39:**

```
Forward work happens on a feature branch, not on `main`. The contributor model lives in `substrate/README.md` and the relevant `stoa--` epic in beadwork. A few load-bearing rules specific to this repo:
```

**Replace with:**

```
Forward work happens on a feature branch, not on `main` — with the explicit user-tier housekeeping exception enumerated at `substrate/MAJOR_POLYBIUS.md` §18 (Arc directive + activation paste tracking commits, substrate-tool self-apply, orphan cleanup, retro docs at `docs/sessions/`, and bw operations on the orphan beadwork branch may direct-commit to main; substrate canon edits, tooling source changes, and app/case-study work require an arc). The contributor model lives in `substrate/README.md` and the relevant `stoa--` epic in beadwork. A few load-bearing rules specific to this repo:
```

**Wording rationale.** The edit extends the existing sentence rather than rewriting it — "Forward work happens on a feature branch, not on `main`" is preserved as the lead, the exception clause inlines after the em-dash, and the cross-ref to §18 names the canonical enumeration locus. The exception clause names the categories in a single parenthetical so a reader scanning CLAUDE.md cold gets the headline list without needing to follow the cross-ref to read the substantive prose. The cross-ref to §18 makes the substrate canon authoritative; CLAUDE.md acknowledges the exception but does not duplicate the canon.

**No other /CLAUDE.md edits.** The authorship-attribution section (CLAUDE.md lines 79-95), the project-layout section, the entry-point routing section, and the SKILL.md handoff are unchanged. The edit is one sentence in one location.

**Cite-comments — C1 cross-refs that must resolve at every read-site:**

- `MAJOR_POLYBIUS.md` §18 references project-root `/CLAUDE.md`, `MAJOR_PLINY.md` §5.9, `MAJOR_POLYBIUS.md` §15, `operating-disciplines.md` §6.7.1, `operating-disciplines.md` §12. All five loci exist in current canon.
- `/CLAUDE.md` line 39 (post-edit) references `substrate/MAJOR_POLYBIUS.md` §18 (created by C1 this arc). Created together; resolves on apply.
- The existing §5.9.2 Cross-references block in `MAJOR_PLINY.md` does NOT need a new bullet for §18 — §18.3's body prose names the §5.9 cross-ref direction; the reverse direction is satisfied by the existing §5.9.2 bullet for `operating-disciplines.md` §24 which already covers the universal-team framing of branch hygiene.

---

### §3.2 — C2: HUMAN_paste-*.md archival convention (§5.11 in MAJOR_PLINY.md)

**Target file:** `substrate/MAJOR_PLINY.md`
**Insertion-point:** new top-level subsection `### 5.11 HUMAN_paste-*.md archival on arc close` inserted after §5.10.3 closes (the existing Arc 32 / C3 N=1 provenance section closing at MAJOR_PLINY.md:460) and before the `---` family-boundary at MAJOR_PLINY.md:462 (which precedes `## 6. Communication` at MAJOR_PLINY.md:464).

Required post-build order in the §5.10.3-close → `---` → §6 window:

```
<MAJOR_PLINY.md:460 = §5.10.3 close>
<blank line>
### 5.11 HUMAN_paste-*.md archival on arc close
<C2 body prose>
<blank line>
---
<blank line>
## 6. Communication
```

§5.11 (depth-3 `###`) MUST appear above the `---` family-boundary so it sits as a top-level peer of §5.1-§5.10 rather than as a §6-family member. The probe in §4.2 enforces this relative ordering.

**Locus rationale:**

- §5 is "The gauntlet pipeline." §5.9 / §5.9.4 / §5.10 are the arc-boundary operational-hygiene subsections (opening: pre-branch + worktree; closing: signoff). §5.11 is the closing-beat cleanup-action that §5.10's signoff-accuracy verifies — same family, same lifecycle point.
- Alternative `operating-disciplines.md` universal-team rejected because the discipline is PLINY-specific (PLINY runs every arc-close cleanup; no other seat does). A thin universal-team cross-ref is not added at `operating-disciplines.md` §24 (the existing Arc 30 thin-cross-ref) because §24 already covers PLINY-as-only-branch-creating-seat — the paste-archival action is part of that same arc-boundary discipline cluster and does not warrant separate universal-team promotion.
- Alternative `substrate/arcs/README.md` rejected because (a) no such README exists today, (b) creating one would scatter the arc-close discipline across two locations, and (c) `substrate/arcs/` is a flat directory of directive files today; adding a README.md changes the directory's signal-to-noise.

**Verbatim canon prose ADA must write** (paste as new subsection between MAJOR_PLINY.md:460 and the `---` at MAJOR_PLINY.md:462):

```markdown
### 5.11 HUMAN_paste-*.md archival on arc close

When an arc closes (PR merged, work-unit ticket closed, signoff posted per §5.10), the arc-specific activation paste files at the workspace root — `HUMAN_paste-pliny-arc-<N>-instruction.md` and `HUMAN_paste-polybius-arc-<N>-instruction.md` — are moved into the arc's archive directory at `substrate/arcs/arc-<N>/pastes/`. Workspace root carries only the live `HUMAN_paste-orchestrator-instruction.md` (the non-arc-scoped default activation paste, refreshed in place per `MAJOR_POLYBIUS.md` §4.5 + §6) and the activation paste files for arcs that are still in flight.

The discipline mirrors and prefix-aligns with the existing `substrate/arcs/arc-<N>-build-directive.md` archival pattern: each arc's directive lives at `substrate/arcs/` as a flat file `arc-<N>-build-directive.md`; this convention places each arc's activation pastes in a sibling `arc-<N>/pastes/` subdirectory under the same parent. Both artifacts share the `arc-<N>` prefix, so a future POLYBIUS looking for "what activated Arc 27" runs `ls substrate/arcs/ | grep arc-27` and finds the flat-file directive `arc-27-build-directive.md` AND the subdirectory `arc-27/` adjacent in the listing. The two artifacts are co-located by prefix at the same `substrate/arcs/` parent level rather than nested inside an arc-number subdirectory (the bare-number form `substrate/arcs/27/` was rejected because it would have hidden the directive — which lives at the flat path — from `ls substrate/arcs/27/`).

**The cleanup action at arc close (PLINY runs after PR merge, before posting signoff per §5.10):**

```
mkdir -p substrate/arcs/arc-<N>/pastes
git mv HUMAN_paste-pliny-arc-<N>-instruction.md substrate/arcs/arc-<N>/pastes/
git mv HUMAN_paste-polybius-arc-<N>-instruction.md substrate/arcs/arc-<N>/pastes/
git commit -m "Arc <N>: archive activation pastes to substrate/arcs/arc-<N>/pastes/"
git push
```

`git mv` preserves the file's git-history continuity so a future reader walking `git log --follow substrate/arcs/arc-<N>/pastes/HUMAN_paste-pliny-arc-<N>-instruction.md` sees the file's full lifecycle from initial dispatch-tracking commit through the archival move. Plain `mv` + `git rm` + `git add` would break this property; `git mv` is load-bearing.

**Signoff-accuracy verification (cross-ref to §5.10):** the §5.10 signoff verifies cleanup claims before posting. The paste-archival action is a new "file cleanup" sub-case §5.10 surfaces. Concretely, before posting the signoff PLINY runs both:

```
ls substrate/arcs/arc-<N>/pastes/                                      # must show both arc-<N> paste files
ls HUMAN_paste-{pliny,polybius}-arc-<N>-instruction.md 2>/dev/null     # must return empty (or "No such file")
```

If either check surfaces inconsistent state, the signoff is NOT posted with the cleanup claim — same rule as §5.10's branch-deletion / worktree-removal verifications. Either complete the archival action, re-verify, then post; or post a signoff that honestly names the state observed.

**Forward-only convention.** This discipline applies to Arc 34 and forward. The ~24 historical paste files at workspace root from Arcs 21-33 are NOT backfilled by this convention — historical pastes are honest artifacts of when they were authored, and a bulk-rename of all of them would (a) muddy the git history for those arcs, (b) require a one-off operational sweep that is itself a separate scope, and (c) gain little for future POLYBIUSes who can still find historical pastes via `git log` + filesystem grep. If a future user-tier POLYBIUS surfaces a real reader-friction case for the historical accumulation, a separate housekeeping ticket can address backfill as its own scoped operation.

#### 5.11.1 Empirical anchor

`stoa--f37` (2026-05-17 user-tier POLYBIUS end-of-session hygiene audit, folded as C2 in Arc 34). Observable state at dispatch authoring: `ls HUMAN_paste-*.md` at workspace root returned 24 files spanning arcs 21-34, including paste files for arcs shipped weeks ago. The directory listing degrades as a navigational surface; a future POLYBIUS cannot distinguish "paste for the arc I am about to dispatch" from "paste for arc 21 shipped weeks ago" without reading filenames carefully. The archival convention restores the workspace-root signal: at workspace root, only live in-flight pastes remain.

#### 5.11.2 Cross-references

- §5.10 — signoff-accuracy. §5.11's cleanup action is verified by §5.10's rule; the verification commands enumerated in §5.11 above are the §5.10 verify-before-claim discipline applied to the paste-archival action.
- §5.9 — pre-branch hygiene. §5.11 fires at the closing arc-boundary; §5.9 fires at the opening. The two are paired (open with verification, close with cleanup-then-verification).
- `MAJOR_POLYBIUS.md` §4.5 — durable-substrate-with-short-prompts. The paste files §5.11 archives are the on-disk substrate the §4.5 discipline authorizes; their archival is the lifecycle-completion of that substrate's purpose.
- `MAJOR_POLYBIUS.md` §15 — N=1 honest-scope, the gate this section's claims pass through.
- `operating-disciplines.md` §6.7.1 — the canon-promotion gate this discipline enters off-gate on PRINCIPAL's project-direction authority.
- Empirical anchor: `stoa--f37` (2026-05-17; folded as C2 in Arc 34).

#### 5.11.3 N=1 provenance + accretion path

Per `MAJOR_POLYBIUS.md` §15 honest-scope and `operating-disciplines.md` §6.7.1: PRINCIPAL articulated this discipline on 2026-05-17 (the Arc 34 directive A3 LOCK; captured at `stoa--f37` thread). §6.7.1 defers to the canon-promotion gate (multiple observations across distinct defect classes + controlled comparison + substrate-level pattern); §6.7.1 does not carve out a separate "PRINCIPAL-declaration shortcut." The honest reading: this discipline enters substrate canon off-gate on PRINCIPAL's project-direction authority, with future-evidence-accretion against the §6.7.1 gate still required for promotion to "structural lesson" status.

The supporting evidence at the time of this writing (2026-05-17):

- **N=1 bit-by-it (defect class: workspace-root accumulation):** 24 paste files at workspace root spanning arcs 21-34; directory listing degrades; future-POLYBIUS reading the listing cannot distinguish in-flight from shipped. Single observation today; pattern not yet across distinct defect classes per §6.7.1 condition 1.
- **N=0 worked-when-applied (controlled comparison):** no arc has yet posted a signoff under the encoded paste-archival convention. Accretes as future arcs ship under §5.11 — each future arc's signoff verifies the archival action; the workspace root stops accumulating; the convention proves out under operational pressure.

The discipline is in substrate canon NOW because PRINCIPAL named it today and the workspace-root accumulation is observable today; promotion to "structural lesson" status with multi-arc empirical backing under the encoded canon is future arcs' work, not this arc's. Same N=1 framing as Arc 27's `MAJOR_POLYBIUS.md` §16.6, Arc 28's `operating-disciplines.md` §22.3, Arc 29's §17.5, Arc 30's `MAJOR_PLINY.md` §5.9.3, Arc 31's `operating-disciplines.md` §25.6, and Arc 32's family (§5.10.3 / §5.9.4.1 / §5.1.3 / §19.6.4).
```

**Build implications (Arc 34 self-application of §5.11 — ADA reads this carefully).** Arc 34 is the arc that ships §5.11 itself, and the two arc-34 paste files at workspace root (`HUMAN_paste-pliny-arc-34-instruction.md`, `HUMAN_paste-polybius-arc-34-instruction.md`) are the first cohort to archive under the new convention. The build sequence for ADA when the canon-prose edit lands:

1. **Create the archive directory in the worktree** — `mkdir -p substrate/arcs/arc-34/pastes` from the worktree root (`C:\Users\denso\claude_projects\the-stoa\.claude\worktrees\arc-34-build\`). The mkdir is per-worktree filesystem state until a commit lands; the empty directory is not tracked by git, so the move-step (next) is what makes the path real.
2. **Move the paste files from workspace root into the new subdirectory** — `git mv HUMAN_paste-pliny-arc-34-instruction.md substrate/arcs/arc-34/pastes/HUMAN_paste-pliny-arc-34-instruction.md` and the same for the polybius paste. Both moves run from the worktree root. The git index records the rename; `git status` shows both files as "renamed."

**Worktree-vs-project-root nuance.** Git worktrees materialize the full project tree at the worktree path; the two arc-34 paste files exist at BOTH `C:\Users\denso\claude_projects\the-stoa\HUMAN_paste-*-arc-34-instruction.md` (the main worktree at the project root) AND `C:\Users\denso\claude_projects\the-stoa\.claude\worktrees\arc-34-build\HUMAN_paste-*-arc-34-instruction.md` (this build worktree's checked-out view). ADA's `git mv` operates on the build worktree's checked-out tree; the commit lands on the `arc-34/build` branch. The main worktree's project-root copies of the pastes remain unmoved on `main` until the arc-34/build branch merges to main — at which point the main worktree's working tree updates per the normal merge mechanics (git brings the deletion-at-old-path + addition-at-new-path through to main's working tree).

This is per-worktree state acting normally, not a bug. ADA does NOT attempt to `git mv` from the project root (that would create a divergent move on main outside the arc-build branch); ADA does NOT manipulate the main worktree's copies of the pastes from inside the build worktree (worktree isolation; tools should not cross-edit other worktrees' working trees). The single operation is `git mv` inside the build worktree, on the arc-34/build branch. Per-arc-build self-application of §5.11 happens once per arc on the arc's own build branch.

3. **Commit the move on the arc-34/build branch** — the move is part of Arc 34's substantive ship (a §5.11 self-application), not a separate housekeeping commit. The canon-edits commit may include the moves; or the moves may land as a paired follow-up commit on the same branch immediately after the canon-edits commit. Either is acceptable; both keep the arc-build's scope coherent.
4. **Verify both probe outputs from §4.2 below pass** before signaling VERA. The §4.2 probes use the post-rev2 paths (`substrate/arcs/arc-34/pastes/`); a wrong-path build (a lingering `substrate/arcs/34/pastes/` from a copy-paste error against rev1) fails the probe and surfaces to VERA as a probe-fail, not a silent pass.

**Self-application probe (Arc 34 specifically).** After the build commit lands on arc-34/build, the following must hold inside the build worktree's checkout:

```
ls substrate/arcs/arc-34/pastes/                                          # must list both arc-34 paste files
ls HUMAN_paste-{pliny,polybius}-arc-34-instruction.md 2>/dev/null         # must return empty at the worktree root
```

The first command confirms the archive landed; the second confirms the workspace root is clean inside the build worktree (the main worktree's pastes are out of scope for this verification — they only move on merge to main).

**Cite-comments — C2 cross-refs that must resolve at every read-site:**

- `MAJOR_PLINY.md` §5.11 references §5.10 (Arc 32 / `stoa--ewn`), §5.9 (Arc 30 / `stoa--3cs`), `MAJOR_POLYBIUS.md` §4.5, `MAJOR_POLYBIUS.md` §15, `operating-disciplines.md` §6.7.1. All five loci exist in current canon.
- **C2 ↔ Arc 32 §5.10 cross-ref:** §5.11 names §5.10's verify-before-claim discipline as the verification gate for paste-archival. The reverse cross-ref direction (§5.10 → §5.11) is intentionally NOT added — §5.10's "file cleanup claims" bullet already names the verification command shape (`ls <path>` / `git status` for tracked files); the paste-archival action is a specific application of that general rule, not a new general rule. Re-opening §5.10's prose to add §5.11 as an enumerated sub-case would dilute §5.10's general framing. The asymmetric cross-ref is intentional (same shape as Arc 32 §5.9.4 → §5.10 from `agents/design/arc-32/design.md` §3.5 cite-comments).

---

### §3.3 — C3: Template-title + first-paragraph cosmetic fix (paste-instruction-template.md)

**Target file:** `substrate/templates/paste-instruction-template.md`
**Insertion-point:** two in-place edits to lines 5 and 7 of the template file. No new sections, no slot changes, no template-body changes.

**Verbatim edits ADA must apply:**

**Edit 3a — line 5 (title):**

Current state (line 5):
```
# Paste-instruction template — MAJOR_PLINY activation
```

Replace with:
```
# Paste-instruction template — MAJOR_PLINY and MAJOR_POLYBIUS activation
```

**Edit 3b — line 7 (first paragraph; the substantive opening framing):**

Current state (line 7):
```
The template MAJOR_POLYBIUS fills per session to produce the paste-instruction that activates MAJOR_PLINY (the ORCHESTRATOR) in a fresh terminal. The static `MAJOR_PLINY.md` role file is universal; the wrapper that activates it is session-specific. POLYBIUS fills the slots from its conversation with the PRINCIPAL, writes the filled result to disk under `HUMAN_paste-orchestrator-instruction.md`, and hands the PRINCIPAL a one-line pointer.
```

Replace with:
```
The template MAJOR_POLYBIUS fills per session to produce the paste-instruction that activates MAJOR_PLINY (the ORCHESTRATOR), or that user-tier MAJOR_POLYBIUS fills to activate a project-tier MAJOR_POLYBIUS, in a fresh terminal. The static role files (`MAJOR_PLINY.md`, `MAJOR_POLYBIUS.md`) are universal; the wrapper that activates them is session-specific. The filling seat (typically POLYBIUS) fills the slots from its conversation with the PRINCIPAL, writes the filled result to disk under `HUMAN_paste-<target>-instruction.md` (e.g., `HUMAN_paste-orchestrator-instruction.md` for PLINY, `HUMAN_paste-polybius-arc-<N>-instruction.md` for a POLYBIUS-targeted arc dispatch), and hands the PRINCIPAL a one-line pointer.
```

**No other template edits.** The line 9 architecture-authority paragraph, the substitution-slots table (lines 13-23), the per-slot rationale (lines 26-35), the template body (lines 41-53), the slot-explanation paragraphs (lines 55-89), the worked example (lines 95-145), the where-the-filled-paste-lives section (lines 150-154), the when-to-refresh section (lines 158-164), and the why-string-substitution section (lines 168-177) are all unchanged. The author frontmatter (`author: Denson Smith` at line 2) is unchanged.

**Wording rationale.** Title uses "and" rather than "/" or "&" to read cleanly out of context (per `MAJOR_POLYBIUS.md` §16.4 Ariadne-search-ready authoring — "Titles matter… distinct, specific, named-entities, no relying on context to disambiguate"). The first paragraph extends rather than rewrites — the substantive structure (template-purpose → role-files-universal → wrapper-specific → filling-action → disk-write → PRINCIPAL-pointer) is preserved; the dual-targeting reality is named directly with worked example filenames so a reader follows the convention without needing to infer it. The differentiated `HUMAN_paste-<target>-instruction.md` filename pattern (with PLINY using the legacy `orchestrator` token for the live in-flight non-arc paste and POLYBIUS using the explicit `polybius-arc-<N>` form for arc dispatch pastes) matches observable practice at workspace root (24 paste files; the convention is empirically stable).

**Cite-comments — C3 cross-refs.** The template's existing references to `MAJOR_POLYBIUS.md` §5.1.3 (the dual-targeting cron-hygiene canon that Arc 32 / `stoa--ewn` shipped) are CARRIED by the existing `{{CRON_HYGIENE_CLAUSE}}` slot-explanation paragraph at template lines 55+; C3 does not add or modify those references. The C3 edit is purely cosmetic; no new cross-refs land.

**§15 N=1 framing applicability:** A4 LOCKED C3 scope as cosmetic. The template title + first paragraph being out-of-date is a follow-up from Arc 32 / CATO F1 finding (per `stoa--3qi` body) — there is no new discipline being canonified, only a wording-drift being corrected. The §6.7.1 N=1 gate does not apply to wording corrections; the gate applies to discipline-promotion. C3 ships as a no-N=1-framing-needed cosmetic correction, named here so ARGUS does not push back asking for a §15 provenance paragraph on C3.

---

### §3.4 — C4: HITL-paused queue sweep (defense-in-depth: MAJOR_POLYBIUS.md §9 step + handoff-doc-template section)

**Target files:**
- `substrate/MAJOR_POLYBIUS.md` — new step in §9 activation checklist (Locus 1)
- `substrate/templates/handoff-doc-template.md` — new section + substitution slot (Locus 2)

#### §3.4.1 — Locus 1: MAJOR_POLYBIUS.md §9 activation checklist new step

**Insertion-point:** new step in the §9 numbered list at `substrate/MAJOR_POLYBIUS.md` lines 489-503. The current list runs 1-7 (lines 491, 492, 499, 500, 501, 502, 503). Insert the new step AFTER current step 2 (the `bw prime` step ending at line 498) and BEFORE current step 3 (the "Read recent beadwork comments" step at line 499). Current steps 3-7 renumber to 4-8.

**Wording rationale for placement.** The sweep needs `bw prime`'s output (the open-tickets list it produces) as input; it must fire AFTER step 2. The sweep produces a list of HITL-paused tickets that should be added to "relevant tickets" for step 3's read; it must fire BEFORE step 3. The natural insertion point is the gap between steps 2 and 3 — the data-flow boundary.

**Verbatim edit ADA must apply** (insert as new numbered step 3 in the §9 list; renumber current 3-7 as 4-8):

```markdown
3. **Sweep open tickets for HITL-paused indicators.** Run a filtered `bw list` (or read `bw prime`'s output if it already enumerated open tickets) and scan ticket titles + body excerpts for HITL-paused phrasing — "TBD by user-tier POLYBIUS once PRINCIPAL approves," "blocked-on-PRINCIPAL," "awaiting PRINCIPAL adjudication," "HITL gate before dispatch," or similar. For each HITL-paused ticket surfaced, decide:
   - **Still validly paused** (the HITL precondition has not been met; the ticket should remain paused) → note + skip.
   - **PRINCIPAL-attention overdue** (the ticket has been paused for a notable duration without any update; PRINCIPAL may not be aware the queue is waiting on them) → SURFACE in this session's first turn to PRINCIPAL. Worked surfacing shape: "I see <N> open HITL-paused ticket(s) waiting on PRINCIPAL: <ticket-id> (<one-line summary>, paused <duration>). Do any of these need attention now, or should they continue to wait?"

   The discipline closes a specific gap: an HITL precondition correctly prevents auto-dispatch, but no mechanism surfaces "you have an open paused-pre-dispatch epic" to PRINCIPAL across the gap between when the ticket was paused and when PRINCIPAL is ready to adjudicate. Empirical anchor: `stoa--jru` (Arc 22 coordination hygiene) sat HITL-paused-pre-dispatch from 2026-05-04 to 2026-05-17 — ~2 weeks across multiple POLYBIUS sessions — without surfacing. The sweep at session-start (this step) plus the handoff-doc-template HITL-paused-queue section (`substrate/templates/handoff-doc-template.md`) is the defense-in-depth pair: this step fires at every fresh activation; the handoff-doc fires at session-handoff. Forward POLYBIUSes hit the sweep at both lifecycle points.
```

The list-item content is dense by §9 standards (most steps are one or two sentences); the density is load-bearing because the surfacing-shape worked example is what distinguishes this step from "and also check for HITL stuff somehow." A future POLYBIUS reading the step cold needs the exact phrasings to scan for AND the worked surfacing template to apply.

**Renumbering of current steps 3-7 as 4-8.** Each step's text is unchanged; only the leading number changes. ADA applies the renumber as part of the same edit transaction. The "Otherwise, ask the PRINCIPAL what they want to work on" step that closes the list (current step 7) becomes step 8.

**Conditional-fire variants discussion (provenance-honest sketch, not in canon).** A future arc may surface that the sweep is too coarse — e.g., a session that just dispatched 3 arcs in the prior 30 minutes does not need to sweep again. The current shape is "sweep at every fresh activation"; refinement to "sweep at every fresh activation unless the session-state cache from the previous session is < 30 min stale" is forward work. For now, the unconditional-sweep shape is the default-include analogue of `MAJOR_POLYBIUS.md` §5.1.2's pre-branch hygiene paste-preamble — "default-include is the safety property: the cost of including [the sweep] when no HITL-paused ticket is present is one `bw list` call returning routine state; the cost of omitting it on a session that does inherit a stale HITL-paused queue is the exact invisibility pattern stoa--jru exhibited."

#### §3.4.2 — Locus 2: handoff-doc-template.md new "HITL-paused queue" section + slot

**Insertion-points (three coordinated edits in the template file):**

**Edit 4a — add `{{HITL_PAUSED_QUEUE}}` row to the Substitution slots table** (`substrate/templates/handoff-doc-template.md` lines 23-38). Insert as a new row AFTER the existing `{{BW_REPO_TABLE}}` row (currently line 34) and BEFORE the existing `{{STATE_SHAPES_BEHAVIOR}}` row (currently line 35). The natural neighborhood: the bw repo table is navigation aid for open work; HITL-paused queue is open-work-state; state-shapes-behavior is open-watch-out items. Verbatim row to insert:

```markdown
| `{{HITL_PAUSED_QUEUE}}` | enumeration of open HITL-paused-pre-dispatch tickets the next session should surface to PRINCIPAL on first turn; empty is fine (explicit "no open HITL-paused tickets" is better than silence) | `- stoa--jru (Arc 22 coordination hygiene, paused 2026-05-04 awaiting PRINCIPAL adjudication of design-rev2; surface on first turn if PRINCIPAL has bandwidth for Arc 22 disposition).` |
```

**Edit 4b — add per-slot rationale paragraph** in the per-slot-rationale section (template lines 42-55). Insert as a new bullet AFTER the existing `{{BW_REPO_TABLE}}` rationale (currently the bullet at line 52) and BEFORE the existing `{{STATE_SHAPES_BEHAVIOR}}` rationale (currently the bullet at line 53). Verbatim bullet:

```markdown
- **`{{HITL_PAUSED_QUEUE}}`** captures open work that is paused awaiting PRINCIPAL adjudication. Per `MAJOR_POLYBIUS.md` §9 step 3, the activated session sweeps for HITL-paused indicators at session-start; the handoff doc's HITL-paused-queue section pre-populates that sweep so the next session does not need to re-derive the queue from scratch. Empirical anchor: `stoa--jru` (Arc 22) sat paused-pre-dispatch from 2026-05-04 to 2026-05-17 because no carrier surfaced the open-paused state to fresh POLYBIUS sessions; both the §9 step (fresh-activation carrier) and this template section (handoff carrier) are the defense-in-depth pair Arc 34 / C4 encodes.
```

**Edit 4c — add new section to the Template body** (template lines 60-110, currently 8 sections in the rendered handoff). Insert the new section BETWEEN the existing `## Where the bw repos live` section (template lines 89-91) and the existing `## State that shapes POLYBIUS behavior` section (template lines 93-95). Verbatim insertion:

```markdown
## HITL-paused queue

{{HITL_PAUSED_QUEUE}}

```

(Two blank lines after the closing slot per the template's between-section convention.)

**Section-order rationale.** The post-edit template body order is: Live-relay-status → One-paragraph-state → Recommendation-menu → Load-bearing-context → Where-the-bw-repos-live → **HITL-paused-queue** → State-that-shapes-POLYBIUS-behavior → Memories-cite-don't-restate → Hygiene-loose-ends → Honest-caveats. HITL-paused-queue sits between two open-work-state sections (bw repo table; state-shapes-behavior) — natural clustering that keeps the open-work-state items contiguous when a reader scans the handoff.

**No template-body slot changes elsewhere.** The `{{LIVE_RELAY_STATUS}}`, `{{ONE_PARAGRAPH_STATE}}`, `{{RECOMMENDATION_MENU}}`, `{{LOAD_BEARING_CONTEXT}}`, `{{BW_REPO_TABLE}}`, `{{STATE_SHAPES_BEHAVIOR}}`, `{{MEMORIES_CITE_DONT_RESTATE}}`, `{{HYGIENE_LOOSE_ENDS}}`, and `{{HONEST_CAVEATS}}` slots are unchanged. The author frontmatter (`author: Denson Smith` at line 2) is unchanged.

#### §3.4.3 — C4 N=1 provenance + accretion path (lives at the MAJOR_POLYBIUS.md §9 step's provenance discussion)

§9 is a numbered checklist; appending a numbered-subsection provenance section beneath a list item is structurally awkward (the next list item becomes the de-facto sibling of the provenance section). The provenance content for C4 — N=1 honest-scope, empirical anchor, accretion path — lives inline within the §9 step 3 prose itself (the "Empirical anchor: `stoa--jru` (Arc 22 coordination hygiene) sat HITL-paused-pre-dispatch from 2026-05-04 to 2026-05-17" sentence and the defense-in-depth pair sentence). The inline-paragraph form mirrors Arc 32 / C1 §5.1.1.1's categorical-exception-from-numbered-subsection shape per `agents/design/arc-32/design.md` §3.1 (depth-5 sub-subsection beneath which depth-6 would be unreadable; C4 has the analogous structural-shape problem of "inside a numbered list item").

**Explicit provenance paragraph (not in canon — captured here for ARGUS / VERA reference):**

> Per `MAJOR_POLYBIUS.md` §15 honest-scope and `operating-disciplines.md` §6.7.1: PRINCIPAL articulated this discipline on 2026-05-17 (the Arc 34 directive A5 LOCK; surfaced via the `stoa--ize` investigation that found `stoa--jru` paused for 2 weeks). §6.7.1 defers to the canon-promotion gate; §6.7.1 does not carve out a separate "PRINCIPAL-declaration shortcut." This discipline enters substrate canon off-gate on PRINCIPAL's project-direction authority. Supporting evidence at the time of this writing (2026-05-17): N=1 bit-by-it (stoa--jru paused 2026-05-04 → 2026-05-17 without surfacing — single observation today, single defect class; pattern not yet across distinct defect classes per §6.7.1 condition 1); N=0 worked-when-applied (no POLYBIUS session has yet operated under the encoded sweep discipline; accretes as future sessions surface paused-pre-dispatch state on first turn under §9 step 3). Same N=1 framing as Arc 32's family.

The §9 step's inline empirical-anchor sentence carries the same provenance content in compressed form ("Empirical anchor: stoa--jru sat HITL-paused-pre-dispatch from 2026-05-04 to 2026-05-17 — ~2 weeks across multiple POLYBIUS sessions — without surfacing"); a reader walking the §9 list reads the anchor and the defense-in-depth pair sentence and has the load-bearing provenance content. The full N=1 + §6.7.1 framing is captured in this design's §3.4.3 above and may be referenced by ARGUS or VERA as the structural justification for the inline-paragraph provenance form.

**Cite-comments — C4 cross-refs that must resolve at every read-site:**

- `MAJOR_POLYBIUS.md` §9 step 3 references `MAJOR_POLYBIUS.md` §9 (parent — the activation checklist itself), `substrate/templates/handoff-doc-template.md` (the carrier-2 locus). Both loci exist (the handoff-doc-template addition is created by C4 Edit 4c this arc).
- `substrate/templates/handoff-doc-template.md` Edit 4b's per-slot rationale references `MAJOR_POLYBIUS.md` §9 (parent activation checklist). Locus exists.
- **C4 ↔ Arc 32 / C2 cross-ref:** intentionally NOT added. Both extend the activation-paste / handoff-doc template family with new slots, but the disciplines fire at different lifecycle points (cron at every activation; HITL-paused sweep at every activation AND handoff). Coupling them would over-link; the structural-pattern analogy (default-include with low-cost-of-noise) is shared but the substantive content is independent.
- **C4 ↔ stoa--ize, stoa--jru:** §9 step 3 names `stoa--jru` as the empirical anchor. The `stoa--ize` ticket (which surfaced the C4 candidate via investigation) is referenced in `stoa--y14` body + the Arc 34 directive A12 but is NOT named in canon prose — `stoa--ize`'s value is the investigation history, not the substantive discipline. Per A8, `stoa--ize` Arc 22 disposition is scoped to Arc 36 / future-arc work; Arc 34 closes `stoa--ize` with cross-ref to the merge commit per A12 + the note "Arc 22 disposition tracked in Arc 36 / stoa--jru refresh + dispatch."

---

## §4 — Verification probes (for VERA)

Each probe is a runnable command + expected match. VERA re-executes against the post-build state on `arc-34/build`.

### §4.1 — C1 §18 canon section present + /CLAUDE.md cross-ref edit landed

**Carrier 1 (substrate/MAJOR_POLYBIUS.md §18):**

```
grep -nE "^## 18\. User-tier POLYBIUS direct-commit discipline" substrate/MAJOR_POLYBIUS.md
```
Expected: exactly one match at the §18 header (depth-2, new top-level section).

```
grep -n "Arc directive + activation paste tracking commits" substrate/MAJOR_POLYBIUS.md
```
Expected: at least one match in §18.1 enumeration (the "MAY direct-commit" list).

```
grep -n "Substrate canon edits" substrate/MAJOR_POLYBIUS.md
```
Expected: at least one match in §18.2 enumeration (the "does NOT direct-commit" list).

```
grep -n "push immediately after every direct-to-main commit" substrate/MAJOR_POLYBIUS.md
```
Expected: exactly one match in §18.3 (bundled-squash interaction discipline).

**Carrier 2 (project-root /CLAUDE.md cross-ref):**

The /CLAUDE.md file lives at the project root, NOT in the worktree's `.claude/` subtree. From the worktree's vantage point, the absolute path is `C:\Users\denso\claude_projects\the-stoa\CLAUDE.md`. VERA runs the probe with the absolute path.

```
grep -n "explicit user-tier housekeeping exception enumerated at .substrate/MAJOR_POLYBIUS.md. §18" C:/Users/denso/claude_projects/the-stoa/CLAUDE.md
```
Expected: exactly one match at the post-edit line 39 (the extended sentence).

```
grep -nE "^Forward work happens on a feature branch" C:/Users/denso/claude_projects/the-stoa/CLAUDE.md
```
Expected: exactly one match — the lead clause is preserved as the start of the post-edit sentence (ARGUS may push back if rev1 wording rewrites rather than extends the lead).

### §4.2 — C2 §5.11 archival convention present + relative ordering + self-application

```
grep -nE "^### 5\.11 HUMAN_paste-\*\.md archival on arc close" substrate/MAJOR_PLINY.md
```
Expected: exactly one match at the §5.11 header (depth-3, peer of §5.10).

```
grep -n "substrate/arcs/arc-<N>/pastes/" substrate/MAJOR_PLINY.md
```
Expected: at least one match in §5.11 (the archive-path pattern). The placeholder `<N>` is literal in the canon (not substituted) so the grep matches verbatim. The `arc-` prefix is load-bearing — a bare-number form (`substrate/arcs/<N>/pastes/`) would indicate a rev1-residue path that the rev2 design explicitly rejected; the probe matches the prefix form only.

**Negative probe — the bare-number form must NOT remain in canon:**

```
grep -nE "substrate/arcs/<N>/pastes/" substrate/MAJOR_PLINY.md
```
Expected: zero matches when the leading `arc-` is absent. (VERA: the positive probe above matches `substrate/arcs/arc-<N>/pastes/`; this negative probe matches the bare-number form. The bare-number form is the rev1 path that ARGUS surfaced as modeling a false navigation neighborhood; any match here indicates rev1 residue and the build is incomplete.) Implementation note: `grep -E "substrate/arcs/<N>/pastes/"` will ALSO match `substrate/arcs/arc-<N>/pastes/` as a substring; VERA uses a tightened regex `grep -nE "substrate/arcs/[^a][^r]?[^c]?<N>/pastes/"` OR more reliably `grep -nE "substrate/arcs/<N>"` (no leading `arc-` before `<N>`) and checks zero matches.

```
grep -n "git mv HUMAN_paste-pliny-arc-" substrate/MAJOR_PLINY.md
```
Expected: at least one match in §5.11 (the cleanup-action code-fence).

```
grep -n "Forward-only convention" substrate/MAJOR_PLINY.md
```
Expected: at least one match in §5.11 (forward-only forwarded from A8 hard-lock pattern).

**Relative-ordering enforcement for the §5.10.3-close → `---` → §6 window:** the post-build state MUST have §5.11 appearing above the family-boundary `---` that opens §6.

```
grep -nE "^### 5\.11 |^## 6\. Communication" substrate/MAJOR_PLINY.md | head -5
```
Expected: at least two matches; the §5.11 line number MUST be strictly less than the §6 line number. (VERA: extract both line numbers from the grep output and compare numerically; fail if §5.11 appears at or above §6.) The `---` separator at the line immediately preceding `## 6.` MUST exist (confirmable via reading the line directly).

**Arc 34 self-application probe (paste-archival actually happened on arc-34/build):** §5.11's discipline is forward-only-starting-with-Arc-34; the first cohort under the canon is Arc 34's own activation pastes. VERA verifies the self-application on the arc-34/build branch.

```
ls substrate/arcs/arc-34/pastes/ | grep HUMAN_paste-
```
Expected: exactly two matches — `HUMAN_paste-pliny-arc-34-instruction.md` and `HUMAN_paste-polybius-arc-34-instruction.md`. (VERA runs from the build worktree root; the absolute path is `C:\Users\denso\claude_projects\the-stoa\.claude\worktrees\arc-34-build\substrate\arcs\arc-34\pastes\`.)

```
ls HUMAN_paste-pliny-arc-34-instruction.md 2>/dev/null
ls HUMAN_paste-polybius-arc-34-instruction.md 2>/dev/null
```
Expected: both commands return empty / "No such file" inside the build worktree. (The main worktree's copies at project root are out of scope for this verification — they relocate on merge to main per normal git mechanics.)

**Git-history continuity probe (rename detected, not delete-then-add):**

```
git log --follow --oneline substrate/arcs/arc-34/pastes/HUMAN_paste-pliny-arc-34-instruction.md | head -5
```
Expected: the file's git history traces back through the rename to the original at-workspace-root commits. A delete-then-add (rather than `git mv`) would surface as only the new commit appearing, with no history continuity — VERA confirms history is preserved.

### §4.3 — C3 template title + first-paragraph dual-targeting edit landed

```
grep -nE "^# Paste-instruction template — MAJOR_PLINY and MAJOR_POLYBIUS activation" substrate/templates/paste-instruction-template.md
```
Expected: exactly one match at line 5 (the post-edit title).

```
grep -n "or that user-tier MAJOR_POLYBIUS fills to activate a project-tier MAJOR_POLYBIUS" substrate/templates/paste-instruction-template.md
```
Expected: exactly one match in the line-7 paragraph (the dual-targeting clause).

```
grep -n "HUMAN_paste-<target>-instruction.md" substrate/templates/paste-instruction-template.md
```
Expected: exactly one match in the line-7 paragraph (the differentiated filename pattern).

**Authorship probe (per A7):**

```
grep -n "^author: Denson Smith" substrate/templates/paste-instruction-template.md
```
Expected: exactly one match at line 2 (frontmatter unchanged).

**Negative probe — the legacy PLINY-only title must NOT remain:**

```
grep -nE "^# Paste-instruction template — MAJOR_PLINY activation$" substrate/templates/paste-instruction-template.md
```
Expected: zero matches (the old title is fully replaced; the literal `$` end-anchor distinguishes from the post-edit title which has "and MAJOR_POLYBIUS activation" appended).

### §4.4 — C4 Locus 1 (MAJOR_POLYBIUS.md §9 step) + Locus 2 (handoff-doc-template) present

**Locus 1:**

```
grep -n "Sweep open tickets for HITL-paused indicators" substrate/MAJOR_POLYBIUS.md
```
Expected: exactly one match in §9 (the new step 3 lead phrase).

```
grep -n "TBD by user-tier POLYBIUS once PRINCIPAL approves" substrate/MAJOR_POLYBIUS.md
```
Expected: exactly one match in §9 step 3 (the example HITL-paused phrasing list).

```
grep -n "stoa--jru.*Arc 22 coordination hygiene" substrate/MAJOR_POLYBIUS.md
```
Expected: at least one match in §9 step 3 (the empirical anchor sentence).

**Renumbering verification — §9 list must have steps numbered 1 through 8 (was 1-7 pre-edit; step 3 inserted, so post-edit 1-8):**

```
grep -nE "^[0-9]+\." substrate/MAJOR_POLYBIUS.md | sed -n '/^[0-9]*:1\./,/^[0-9]*:8\./p' | head -20
```
Expected: the §9 numbered list contains lines starting `1.`, `2.`, `3.`, `4.`, `5.`, `6.`, `7.`, `8.` in that order. (VERA: scope the grep range to the §9 section by finding the §9 header line number and the §10 header line number and confining the search; the simpler grep above may include numbered-list items from other §-sections — VERA scopes carefully.)

A simpler scoped probe — match the renumbered-step lead phrasings that uniquely identify post-edit numbering:

```
grep -nE "^3\. \*\*Sweep open tickets for HITL-paused indicators" substrate/MAJOR_POLYBIUS.md
```
Expected: exactly one match (the new step 3 lead).

```
grep -nE "^4\. \*\*Read recent beadwork comments|^4\. Read recent beadwork comments" substrate/MAJOR_POLYBIUS.md
```
Expected: exactly one match (current step 3 — "Read recent beadwork comments on relevant tickets" — renumbered to 4).

```
grep -nE "^8\. Otherwise, ask the PRINCIPAL" substrate/MAJOR_POLYBIUS.md
```
Expected: exactly one match (current step 7 — "Otherwise, ask the PRINCIPAL what they want to work on" — renumbered to 8).

**Locus 2 (handoff-doc-template.md):**

```
grep -n "{{HITL_PAUSED_QUEUE}}" substrate/templates/handoff-doc-template.md
```
Expected: at least three matches — one in the Substitution slots table (Edit 4a), one in the per-slot rationale section (Edit 4b), one in the template body (Edit 4c).

```
grep -nE "^## HITL-paused queue" substrate/templates/handoff-doc-template.md
```
Expected: exactly one match in the template body (the new section header inserted by Edit 4c).

```
grep -n "stoa--jru" substrate/templates/handoff-doc-template.md
```
Expected: at least one match in the per-slot rationale (Edit 4b) — the empirical anchor reference. May also appear in the Substitution slots table's example value (Edit 4a) — at least two matches acceptable.

**Section-order probe in template body:**

```
grep -nE "^## Where the bw repos live|^## HITL-paused queue|^## State that shapes POLYBIUS behavior" substrate/templates/handoff-doc-template.md
```
Expected: exactly three matches in increasing line-number order — "Where the bw repos live" first, "HITL-paused queue" second, "State that shapes POLYBIUS behavior" third.

### §4.5 — Cite-comments resolve

Per A6, cross-references between candidates and adjacent canon must resolve at every read-site. Per-depth verification probes (mirroring Arc 32 / `agents/design/arc-32/design.md` §4.6 shape):

```
grep -nE "^## 18\b" substrate/MAJOR_POLYBIUS.md
```
Expected: exactly one match at the §18 header (depth-2, new top-level).

```
grep -nE "^### 5\.11\b" substrate/MAJOR_PLINY.md
```
Expected: exactly one match at the §5.11 header (depth-3, peer of §5.10).

**Cross-ref direction probes:**

```
grep -n "MAJOR_POLYBIUS.md.*§18" C:/Users/denso/claude_projects/the-stoa/CLAUDE.md
```
Expected: exactly one match in /CLAUDE.md (the post-edit line 39 cross-ref to §18).

```
grep -n "MAJOR_PLINY.md.*§5.10" substrate/MAJOR_PLINY.md
```
Expected: at least one match (§5.11 references §5.10 for the signoff-accuracy verification gate; the match should be inside §5.11 body, NOT in §5.10's own self-reference).

```
grep -n "MAJOR_POLYBIUS.md.*§9" substrate/templates/handoff-doc-template.md
```
Expected: at least one match in the per-slot rationale (Edit 4b) — the cross-ref to the activation-checklist step.

### §4.6 — §15 N=1 provenance shape per A9 (no over-generalization)

C1 (§18.5), C2 (§5.11.3) MUST each name an empirical anchor + cite §6.7.1 + name the accretion path with the canonical "enters substrate canon off-gate" boilerplate phrasing. C4 (Locus 1's inline provenance) uses a compressed inline form — the structural shape mirrors Arc 32 / C1 §5.1.1.1's categorical exception (provenance content inside a structurally-awkward host: numbered list item analogue of depth-5 sub-subsection). C3 has no §15 framing (cosmetic correction; gate does not apply).

**Per-file boilerplate-phrase probes:**

```
grep -nE "enters substrate canon off-gate" substrate/MAJOR_POLYBIUS.md
```
Expected: at least 1 match (C1 §18.5 provenance section). The match count may be larger if Arc 32's prior §5.1.3 provenance paragraph survives (it does; per the §16.6 / §17.5 N=1 framings shipped earlier).

```
grep -nE "enters substrate canon off-gate" substrate/MAJOR_PLINY.md
```
Expected: at least 1 match (C2 §5.11.3). Prior matches survive from Arc 30 §5.9.3 + Arc 32 §5.10.3 + §5.9.4.1.

**C4 categorical-exception probe** — C4 Locus 1's inline provenance uses the compressed shape (no boilerplate phrase). Verify the structural-shape note is honored by checking the empirical-anchor sentence is present:

```
grep -n "stoa--jru.*paused" substrate/MAJOR_POLYBIUS.md
```
Expected: at least one match in §9 step 3 (the compressed empirical-anchor + duration sentence).

### §4.7 — Authorship audit (per A7)

```
grep -rnE "^author:|^Authored by:|^Author:" substrate/templates/paste-instruction-template.md substrate/templates/handoff-doc-template.md substrate/MAJOR_POLYBIUS.md substrate/MAJOR_PLINY.md C:/Users/denso/claude_projects/the-stoa/CLAUDE.md
```
Expected: only the two pre-existing `author: Denson Smith` frontmatter entries — one at `paste-instruction-template.md` line 2 (unchanged), one at `handoff-doc-template.md` line 2 (unchanged). No other author-like fields added or modified. The /CLAUDE.md edit at line 39 adds no author-like field (the file has no author frontmatter; the edit is in body prose).

### §4.8 — `check.sh` against the-stoa workspace

Per directive Phase B item 8:

```
substrate/skills/check-substrate-updates/check.sh --workspace C:/Users/denso/claude_projects/the-stoa
```
Expected: DRIFTED on the four edited substrate files (`MAJOR_POLYBIUS.md`, `MAJOR_PLINY.md`, `templates/paste-instruction-template.md`, `templates/handoff-doc-template.md`). The workspace-tier handles re-sync on its own activation per `MAJOR_POLYBIUS.md` §14. The /CLAUDE.md edit is not tracked by check.sh (the script scopes to `substrate/`-shipped files per `MAJOR_POLYBIUS.md` §17.2).

### §4.9 — Credential-discipline non-applicability gate (per `CAPTAIN_DAEDALUS_the_stoa.md` §6.6)

This design touches no credentialed operations. No CLI/API gated by tokens, OAuth scopes, or service accounts is invoked. No probe authors any workflow YAML; no probe invokes any credentialed tool. The §6.6 credential-flow probe requirement does not apply to this design.

---

## §5 — Self-assessed weak points

Per `CAPTAIN_DAEDALUS_the_stoa.md` §6.2, these are brittle spots where a specific assumption could break the design under ARGUS cold-read or future maintenance pressure. Each names the spot and the defense for the shape anyway.

**Weak point 1 — C1's §18 lives at MAJOR_POLYBIUS.md as a new top-level section between §17 and the file's `Standby, run.` close.** The choice to place a substantive new top-level section AFTER the existing N=1-framed §16 and §17 sections (which were both shipped under the same off-gate-on-PRINCIPAL-declaration framing today) doubles the count of "new top-level sections shipped via §15 honest-scope" in this file in a single recent window. A reader walking MAJOR_POLYBIUS.md cold may experience the file as having three back-to-back "new substrate disciplines named recently" sections (§16, §17, §18), each with its own §15 framing. *Defense for the shape:* the three sections cover structurally distinct domains — §16 is POLYBIUS session lifecycle; §17 is base-vs-custom file ownership; §18 is user-tier-to-main commit discipline. Each is a different layer of "how does POLYBIUS operate against the substrate's structure," and each is empirically anchored independently. The accretion is honest (each is N=1-declared off-gate); the visual density of three consecutive §15-framed sections is a presentational artifact of the substrate's current accretion rate, not a discipline-quality issue. ARGUS may push back on the visual density; the alternative (folding §18 into §17 or §4) under-promotes a discipline that operates at a different granularity than its candidate parents.

**Weak point 2 — C2's §5.11 forward-only convention does NOT touch the 24 historical paste files at workspace root; AND the rev2 path-shape (`arc-<N>/pastes/`) is the second proposal in this design after rev1's bare-number form (`<N>/pastes/`) was retired by ARGUS audit.** Two coupled risks: (a) backfill-misread — a future user-tier POLYBIUS may rationally interpret §5.11 as "I should backfill all the historical pastes too" and end up doing 24 `git mv` operations in a session-end housekeeping pass, bundling 24 mechanical moves into a direct-to-main commit that is not surface-disjoint from anything else; (b) rev1-residue — if ADA reads this design carelessly and copy-pastes from a stale snippet (e.g., a draft commit message, a beadwork comment from before the rev2 audit), the bare-number form `substrate/arcs/34/pastes/` could land in the build despite rev2's prose using the prefix form, with the residue producing the navigation friction ARGUS surfaced as the original NEEDS_REVISION finding. *Defense for the shape:* (a) §5.11's prose names the forward-only scope explicitly ("This discipline applies to Arc 34 and forward… historical pastes are honest artifacts of when they were authored, and a bulk-rename of all of them would (a) muddy the git history for those arcs, (b) require a one-off operational sweep that is itself a separate scope"); the defense is in the canon itself; a future user-tier POLYBIUS reading §5.11 cold reads the forward-only framing before reading the cleanup-action. (b) The §4.2 negative probe explicitly fails the build on bare-number residue (`grep -nE "substrate/arcs/<N>"` with no leading `arc-` must return zero matches); rev1-residue is catchable at VERA rather than silently passing. ARGUS may push back on (a) asking whether the forward-only framing is strong enough to prevent the bulk-backfill misread, in which case the prose can be tightened with an explicit "do NOT backfill historical pastes" sentence — the rev3 add is one sentence. ARGUS may push back on (b) asking whether the negative probe regex is tight enough; the design's §4.2 probe explanation enumerates the substring-match risk and proposes the tightened regex form, which is verifiable on the post-build state.

**Weak point 3 — C3's title change "MAJOR_PLINY and MAJOR_POLYBIUS activation" arranges the role names in their introduction-order (PLINY first because the template predates the dual-targeting use case), not in their rank-precedence-order or alphabetical-order.** A future reader may experience this as a subtle prioritization signal — "PLINY is the more important target; POLYBIUS is the secondary." *Defense for the shape:* the introduction-order is honest about the template's history (it was authored for PLINY activation; POLYBIUS-targeted activation was a later use case extending the same template). The alternatives — "MAJOR_POLYBIUS and MAJOR_PLINY activation" (alphabetical-ish but reads as elevating POLYBIUS over PLINY), or "MAJOR_PLINY / MAJOR_POLYBIUS activation" (the slash is operationally ambiguous), or "PLINY-targeted and POLYBIUS-targeted activation" (drops the MAJOR rank, which is the substrate's convention for naming seats in titles) — each has its own weakness. The picked form preserves the existing title's structure and adds the second seat in the natural extension position. ARGUS may push back on the ordering; the alternative shapes are enumerated here so ARGUS has the rejected options to compare against.

**Weak point 4 — C4's §9 step 3 inserts a new step in the middle of a numbered list, requiring renumbering of current steps 3-7 as 4-8.** Any future arc that edits §9 (e.g., a future arc adds a step 4.5 or removes step 5) inherits the renumbering surface as a structural property of the list. The discipline of "always renumber when inserting" is implicit in markdown lists but explicit in canon work. *Defense for the shape:* the alternative — appending the new sweep as step 8 instead of inserting at step 3 — places the data-dependent sweep AFTER the "Otherwise, ask the PRINCIPAL" close step, which breaks the natural data-flow ordering (sweep needs to run before PRINCIPAL is asked about session work; the sweep IS the PRINCIPAL-facing data the question depends on). Another alternative — keeping the list at 7 steps and folding the sweep into step 4 ("Read recent beadwork comments… and sweep for HITL-paused indicators") — under-emphasizes the sweep discipline and hides the empirical anchor / surfacing-shape guidance inside a step whose primary intent is something else. Step 3 insertion at the natural data-flow boundary is the right placement; the renumbering cost is mechanical (text replacement); the structural property holds. ARGUS may push back on the step insertion + renumbering; the alternatives lose substantive ordering or visibility.

**Weak point 5 — C4 Locus 2 (handoff-doc-template `{{HITL_PAUSED_QUEUE}}` slot) ships before any handoff has been authored under the slot.** The de-facto template the slotted form was abstracted from (`HANDOFF_POLYBIUS_2026-05-16.md`) does NOT have an HITL-paused-queue section; the new slot fires only on handoffs authored against the post-Arc-34 template. *Defense for the shape:* the slot existence + the per-slot rationale + the template-body section together encode the discipline structurally; future POLYBIUSes filling the template see the slot AND see the rationale AND see where the section renders. The Mode 2 new-session triggers (per `MAJOR_POLYBIUS.md` §16.2) are rare; the slot may not exercise for some calendar time. The N=0-worked-when-applied framing is honest in §3.4.3 above. ARGUS may push back on shipping a slot before its first use; the alternative (defer the slot until the first handoff that needs it) trades structural discipline for empirical anchor — and the §6.7.1 N=1 gate explicitly authorizes off-gate canon promotion on PRINCIPAL's declaration, which the directive A5 LOCK constitutes.

**Weak point 6 — The four candidates' edit surfaces are surface-disjoint per the §1 framing, but C1 + C4 both edit `substrate/MAJOR_POLYBIUS.md`.** ADA must apply C1 (new §18 at file end) and C4 Locus 1 (new step inside §9 list, with renumbering) as two coordinated edits in the same file. The risks: (a) one edit's transaction may inadvertently overwrite or shift line numbers the other edit depends on; (b) VERA's probes citing line numbers (§9 list = lines 489-503 in pre-edit state) may need to recompute against the post-C4-Locus-1 state. *Defense for the shape:* the two C1 + C4 Locus 1 edits target structurally disjoint regions of MAJOR_POLYBIUS.md — §18 inserts at the file end (after line 1121 + 1122 + 1125); §9 step 3 inserts inside lines 489-503. Line numbers shift downstream of every insertion, but the insertion points are character-anchored (not line-number-anchored) in the design above. ADA reading the design applies both edits in either order — line-number references in this design are for orientation; the edit locations are anchored by surrounding-text-match. The Edit-tool's exact-string-match requirement at the worktree level is the structural safety. ARGUS may push back on the two-edit coordination risk; the alternative (separate ADA commits, separate VERA probes per commit) is over-process for two surface-disjoint edits in the same file. The recommended build order: C1 → C4 Locus 1 → C4 Locus 2 → C3 → C2, with C1 applied first because §18 inserts at file end and shifts no line numbers above it; the other edits then apply against stable pre-C1 line numbers for their sections.

**Weak point 7 — C1 Carrier 2 edits the project-root `/CLAUDE.md` file, which lives OUTSIDE the worktree's git-tracked surface from the worktree's vantage point.** The worktree is at `.claude/worktrees/arc-34-build/` under the main worktree; the project-root `/CLAUDE.md` is at `C:\Users\denso\claude_projects\the-stoa\CLAUDE.md`. The worktree's `CLAUDE.md` (which is the `.claude/.../CLAUDE.md` the worktree inherits from main) is NOT what the C1 design targets — the design targets the project-root CLAUDE.md. ADA in the worktree must edit the file at the absolute path, not the relative path. *Defense for the shape:* the C1 Carrier 2 prose names the absolute path explicitly (`C:\Users\denso\claude_projects\the-stoa\CLAUDE.md`) and the §4.1 Carrier 2 probe uses the absolute path. ADA reading the design sees the absolute path in both locations and applies the edit at the correct file. The risk is that ADA in worktree-discipline-mode might assume "edit the CLAUDE.md I see in my pwd" without re-reading the absolute path — which would edit a stale copy of the file in the worktree's `.claude/` subtree that no one reads. ARGUS may push back asking for a stronger explicit warning in the design body; if so, the rev2 add is one cautionary sentence in §3.1. The two probes at §4.1 (one matches the post-edit content; one matches the lead-clause preservation) will catch a wrong-file edit on VERA's pass — both probes use the absolute path; both would fail if ADA edited the wrong file.

**Weak point 8 — All four candidates ship under the §15 N=1 honest-scope framing (or, in C3's case, no §15 framing because it is cosmetic).** The substrate canon's N=1 framing density across recent arcs (Arc 27, 28, 29, 30, 31, 32, and now 34) has produced a pattern where every new discipline section names PRINCIPAL-declaration-off-gate provenance + a "promotion to structural lesson is future arcs' work" disclaimer. A future reader walking the substrate may experience this framing as ritualistic or as load-bearing-not-load-bearing — the framing is honest, but the disclaimer is identical-shape across many sections. *Defense for the shape:* the identical-shape disclaimer IS the honest framing; each new discipline genuinely enters canon off-gate on PRINCIPAL declaration with N=1 or N=0-controlled-comparison empirical backing; the framing is the substrate's discipline against retrospectively re-rationalizing single-observation evidence as multi-observation pattern (per `MAJOR_POLYBIUS.md` §15). The pattern-fatigue risk is real but the alternative (drop the N=1 framing because it has become routine) breaks the discipline. ARGUS may push back on the framing's repetitiveness; the response is "yes, and it is load-bearing precisely because the substrate-canon-promotion gate is structurally distinct from the substrate-canon-enter gate." If ARGUS surfaces a concrete proposal to compress the framing (e.g., a shared `### N=1 provenance` template that all new sections reference rather than re-state), that would be a separate future arc — not Arc 34's scope.

---

## §6 — Out of scope (A8 hard-locked)

Per directive A8, the following are explicitly NOT addressed by this design and any reach for them surfaces as substance-disagreement comment on `stoa--y14` before continuing:

- **stoa--32b.2** (mechanical-script / agent-inspection split) — shipped via Arc 33; CLOSED.
- **stoa--ize Arc 22 disposition** — separate forthcoming Arc 36 / stoa--jru refresh + dispatch. C4 references `stoa--jru` as empirical anchor; does NOT make a disposition decision.
- **stoa--vz9 universal disciplines promotion** — separate forthcoming Arc 37.
- **stoa--kjo per-agent git identity** — separate forthcoming Arc 35.
- **u--7yg.16 envelope tool-set gaps** — separate audit; not folded.
- **u--7yg.21 .claude/ gitignored** — operational truth; not actionable.
- **ariadne--1of agent-team-on-beadwork** — product epic; separate prioritization.
- **s4--bbz sector-4 MVP** — paused per PRINCIPAL until stoa work complete.
- **Backfill of pre-Arc-34 existing paste files** — forward-only convention adoption per A8 hard-lock pattern. The 24 historical paste files at workspace root from Arcs 21-33 stay in place; §5.11 applies to Arc 34 and forward.
- **Editing today's direct-to-main commits** — per `stoa--k36` body's own out-of-scope list; history is history. §18 is forward-only.
- **Other workspaces' similar gaps** — `stoa--k36` body scopes the user-tier-to-main discipline to the-stoa specifically; consumer workspaces have their own CLAUDE.md conventions. §18 names the discipline as "the-stoa-specific application of the canon" in its title; the shape generalizes but the substrate-shipped form is scoped.
- **Splitting paste-instruction-template into two templates** — A4 LOCKED scope. C3 is cosmetic title + paragraph fix only.
- **Redesigning the handoff-doc-template slot set or section ordering beyond the C4 Locus 2 additions** — A5 LOCKED scope. C4 adds one slot + one section at the named insertion point; existing slots / sections unchanged.

---

## §7 — Cite-comment plan (per A6)

Cross-references between Arc 34 candidates and adjacent canon resolve via cite-comments at every read-site. Per-candidate enumeration:

### §7.1 — C1 cite-comments

**Forward cites (from §18 outward):**
- §18 references project-root `/CLAUDE.md` (the post-edit line 39 cross-ref) → /CLAUDE.md line 39 is edited by C1 Carrier 2; cross-ref exists post-build.
- §18 references `MAJOR_PLINY.md` §5.9 → existing canon; cross-ref exists.
- §18 references `MAJOR_POLYBIUS.md` §15 → existing canon; cross-ref exists.
- §18 references `operating-disciplines.md` §6.7.1 → existing canon; cross-ref exists.
- §18 references `operating-disciplines.md` §12 → existing canon; cross-ref exists.

**Reverse cites (into §18 from outside):**
- `/CLAUDE.md` line 39 (post-edit) references `substrate/MAJOR_POLYBIUS.md` §18 → §18 is created by C1 Carrier 1; cross-ref resolves on apply.
- No reverse cite added at `MAJOR_PLINY.md` §5.9 — §5.9 family is branch-creation-discipline; §18 is commit-discipline. The two domains are distinct enough that adding a §5.9 → §18 reverse cite would couple disciplines that operate at different lifecycle points.

### §7.2 — C2 cite-comments

**Forward cites (from §5.11 outward):**
- §5.11 references `MAJOR_PLINY.md` §5.10 (Arc 32 / `stoa--ewn` signoff-accuracy) → existing canon; cross-ref exists.
- §5.11 references `MAJOR_PLINY.md` §5.9 (pre-branch hygiene) → existing canon; cross-ref exists.
- §5.11 references `MAJOR_POLYBIUS.md` §4.5 (durable-substrate-with-short-prompts) → existing canon; cross-ref exists.
- §5.11 references `MAJOR_POLYBIUS.md` §15 → existing canon; cross-ref exists.
- §5.11 references `operating-disciplines.md` §6.7.1 → existing canon; cross-ref exists.

**Reverse cites (into §5.11 from outside):**
- Intentionally NONE. The asymmetric cross-ref pattern (per §3.2 cite-comments) keeps §5.10's prose stable; §5.11's "file cleanup" verification application is named in §5.11 itself, not as a sub-bullet in §5.10's enumeration.

### §7.3 — C3 cite-comments

**No cross-refs added.** C3 is a cosmetic edit to two lines of `paste-instruction-template.md`; the template's existing cross-refs to `MAJOR_POLYBIUS.md` §5.1.3 (via the `{{CRON_HYGIENE_CLAUSE}}` slot mechanism), `MAJOR_PLINY.md` §5.9 (via the `{{PRE_BRANCH_HYGIENE_CLAUSE}}` slot mechanism), and other loci are carried by the template body — none are touched by C3. The new title + new first paragraph reference no external sections.

### §7.4 — C4 cite-comments

**Forward cites (from §9 step 3 outward):**
- §9 step 3 references `substrate/templates/handoff-doc-template.md` (the defense-in-depth pair) → template Edit 4c creates the section; cross-ref resolves on apply.
- §9 step 3 references `stoa--jru` (empirical anchor) → bw ticket; exists.

**Forward cites (from handoff-doc-template per-slot rationale Edit 4b outward):**
- Edit 4b references `MAJOR_POLYBIUS.md` §9 (the activation checklist step that pre-populates the slot) → §9 step 3 is created by C4 Locus 1; cross-ref resolves on apply.
- Edit 4b references `stoa--jru` (empirical anchor) → bw ticket; exists.

**Reverse cites (into Arc 34 / C4 from outside):**
- No reverse cite from `MAJOR_POLYBIUS.md` §16.2 (POLYBIUS session lifecycle modes) → §16.2 is the framing-citation for WHY both lifecycle points need a carrier; §9 step 3 + handoff-doc-template references in this design are the operational instantiations. §16.2's prose is not edited; the conceptual cross-ref is one-way (operational disciplines reference framings; framings do not enumerate every operational discipline they shape).

### §7.5 — Read-site verification (per A6)

For each cite-comment named above, VERA's §4.5 probes confirm the target section header exists at its expected markdown depth (depth-2 for §18; depth-3 for §5.11; depth-3 for §16.2; etc.). Probes that don't match indicate either (a) ADA wrote the section at the wrong depth (e.g., depth-3 `###` instead of depth-2 `##`), (b) ADA's section header text drifted from the design's verbatim (e.g., capitalization, hyphenation, or trailing punctuation), or (c) the cross-ref target section was unexpectedly absent or renamed. All three failure modes are catchable by VERA's grep probes and surface as VERA fail rather than silently passing.

---

End design.
