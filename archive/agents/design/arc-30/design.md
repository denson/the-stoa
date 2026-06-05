# Arc 30 design — PLINY pre-branch hygiene discipline encoded as substrate canon

**Ticket:** `stoa--3cs`
**Branch:** `arc-30/build`
**Date:** 2026-05-17
**Status:** rev3 — ARGUS r6+r7 absorbed; AWAITING ARGUS rev3 audit
**Directive:** `substrate/arcs/arc-30-build-directive.md` (A1-A8 LOCKED)
**Authored by:** CAPTAIN_DAEDALUS_the_stoa, on behalf of the PRINCIPAL (Denson Smith).

---

## §0 — Problem restatement (pre-work gate)

PRINCIPAL articulated on 2026-05-17 that PLINY may create at most one arc-build branch at a time and that local main must equal origin/main before creating one. Today (2026-05-17) the discipline ships in two empirical states: (a) **bit-by-it twice** — PR #46 (multi-project routine) and PR #8 (Arc 28) shipped with bundled-squash, absorbing pre-existing local-ahead commits into the arc PR and producing a misleading squash commit subject and a muddier git history for future POLYBIUSes reading the trail; (b) **worked once when applied** — Arc 29 (PR #9 / `stoa--ads`) shipped clean because the pre-branch check was baked into the activation paste. The discipline is provably effective when applied; what is missing is the canon that makes it apply automatically on every future arc rather than being remembered into each per-arc activation paste.

This arc encodes the discipline as substrate canon so every future PLINY activation inherits it on install, not on POLYBIUS's memory of which arc-recently-shipped-bundled. Three loci (per directive A3): D1 the discipline section in `MAJOR_PLINY.md`; D2 the activation-paste convention; D3 a thin cross-ref in `operating-disciplines.md`. The arc is itself an instance of the discipline — `arc-30/build` was created from clean main at `140b398` per directive A8 (recursive self-application). The hard-locked out-of-scope list (A6) excludes tooling, hooks, retro-edits of PR #46/PR #8 squashes, the cron-hygiene canonification (forthcoming separate arc), and sibling-arc coordination protocols. This design designs only what A1-A8 frame.

**Imported assumptions named (per §6.1 restatement-gate discipline):**

- "PLINY-targeted activation paste" is the right grammatical unit for D2's convention. The substrate has one activation-paste-template artifact (`substrate/templates/paste-instruction-template.md`) that POLYBIUS fills per session; encoding the preamble there carries to every future PLINY paste mechanically. The 2026-05-17 Arc 27/28/29 pastes at the-stoa root are the de-facto-template that's been carrying preambles ad-hoc; canonifying lifts the discipline out of memory into structure.
- The discipline applies in its full form to PLINY; the universal-team layer is THIN because today no other seat creates arc-build branches under the gauntlet pipeline (ADA works on a branch PLINY created; CAPTAINs do not create branches). A cross-ref entry in `operating-disciplines.md` is sufficient; a full universal-team section would over-extend the canon to seats that do not exercise it.
- The `bw show stoa--3cs` 2026-05-17T05:29:51Z scope-expansion comment carries the load-bearing PRINCIPAL phrasing in two flavors: "at most one team working on a repo at any one time" and "pliny can't create more than one branch to work with until the other is committed and merged." Both are quoted verbatim in D1 §5.9 body (under check 1) below — the §5.9.1 subsection carries the "what this fixes" empirical anchor, not the block-quote; per A2 both quoted lines are load-bearing.
- The §15 / §6.7.1 N=1 honesty subsection uses the Arc 27 §16.6 + Arc 29 §17.5 + Arc 28 §22.3 compound-citation shape: discipline enters substrate canon off-gate on PRINCIPAL's project-direction authority; structural-lesson confidence accretes against §6.7.1's three conditions (multiple observations across distinct defect classes; controlled comparison; substrate-level pattern) over future arcs. The N=2 bit-by-it + N=1 worked-when-applied evidence is the today's anchor; future arcs that ship clean accrete further evidence.

---

## §1 — Architectural frame (the load-bearing properties)

### 1.1 What the discipline does and does not do

The discipline is a **two-check pre-branch gate** PLINY runs before `git checkout -b arc-N/build`. It is not a hook, not a script, not enforcement — it is a procedure plus the surface-on-failure behavior. Per directive A6, no mechanical tooling lands in this arc; the discipline-first / tooling-second sequencing matches Arc 29's same-day base-vs-custom convention shape (convention canon first; future arcs may extend tooling). When the two checks pass, PLINY proceeds normally; when either fails, PLINY pauses and surfaces to user-tier POLYBIUS (or PRINCIPAL via `[for: PRINCIPAL]` tag when user-tier unavailable) with the specific state observed and an explicit adjudication ask.

The structural property the discipline preserves: **arc-build PRs are scoped exactly to arc-scope.** The bundled-squash pattern (PR #46 absorbing 7 pre-existing commits → 23 files instead of 5; PR #8 absorbing similar) is a pure-hygiene / reviewability failure, not a correctness regression — the bundled content is legitimate work that needed to land. But the substrate-readability cost compounds: each bundled squash makes future POLYBIUSes reading git history get a muddier picture of which commit landed which arc's substrate canon. The discipline closes the gap structurally rather than relying on per-arc paste-reminders.

### 1.2 Recursive self-application as honesty signal

This arc was itself created under the discipline it encodes. Per directive A8, PLINY verified local main = origin/main at `140b398` before creating `arc-30/build`; user-tier POLYBIUS independently verified at dispatch authoring. The self-application is not just a coincidence — it is the cheapest possible empirical anchor for the discipline. Same recursive-self-application shape as Arc 24 (heartbeat-discipline edit by agents using heartbeats), Arc 25 (credential-discipline edit by agents handling credentials), and Arc 29 (base-vs-custom edit while creating no custom agents).

### 1.3 The single load-bearing structural choice

The choice that carries the design's weight is **encoding the preamble across three carriers — the substantive canon at `MAJOR_PLINY.md` §5.9 (the discipline itself plus the check-1 and check-2 command lists; source of truth for the commands), the paste-preamble verbatim text at `MAJOR_POLYBIUS.md` §5.1.2 (D2 Option α; canon section POLYBIUS reads when authoring activation pastes), and the paste-preamble verbatim text inside `substrate/templates/paste-instruction-template.md`'s `{{PRE_BRANCH_HYGIENE_CLAUSE}}` expansion (D2 Option β; the actual rendered-into-paste text)** rather than picking just one. Rationale at §3 below; three-way drift weak-point analysis at §6.2. The discipline-redundancy property (three locations that say the same thing) matches the existing pattern of `MAJOR_PLINY.md` §6.1 referencing `operating-disciplines.md` §12 — substrate canon accepts N-carrier redundancy for load-bearing operational disciplines because each carrier has a different reader profile (substantive canon for cold-readers, POLYBIUS-authoring canon for paste-fill judgment, template-expansion for mechanical fill at session start).

---

## §2 — D1: `MAJOR_PLINY.md` new discipline section

### 2.1 Insertion locus — §5.9 (the gauntlet-pipeline family)

**Section number:** `### 5.9 Pre-branch hygiene — the two-check rule before creating an arc-build branch`.

**Insertion point:** insert as a new `### 5.9` subsection inside the §5 family — blank line + `### 5.9 Pre-branch hygiene — the two-check rule before creating an arc-build branch` header, NO `---` separator inside the §5 family. The §5.7 → §5.8 transition (and every prior §5.x → §5.(x+1) transition) uses blank-line + `### 5.x` header only; `---` is reserved for top-level family boundaries, not for subsection transitions inside §5. The current §5.8 ends at line 327 (the `#### 5.8.8 Empirical anchor` block, closing with the Arc 24 substrate ticket reference). The `---` at MAJOR_PLINY.md:329 is the §5/§6 family boundary; that separator stays where it is. §5.9 inserts before it as the new final subsection of §5 — between §5.8.8's closing line and the `---` at line 329.

**Locus rationale (why §5.9, not §6.x, not §7.x, not new top-level section near §5/§6):**

- The §5 family is "The gauntlet pipeline" — every subsection in §5 (§5.1 operating-mode awareness in the dispatch brief, §5.2 ADA brief preamble, §5.3 sub-agent watchdog, §5.4 per-worktree venv reflex, §5.5 post-STRABO VERA dispatch, §5.6 INCOMPLETE/UNVERIFIABLE verdict routing, §5.7 smoke-beat discipline, §5.8 background-dispatch hygiene) is a structural beat of the orchestrator running the gauntlet. **Pre-branch hygiene is a structural beat of the gauntlet — specifically the Phase-0-before-Phase-1 step PLINY runs when standing up a new arc-build.** Subsection numbering is consistent.
- Alternative §6.x (Communication) was rejected because branch creation is not a communication primitive; the surface-on-failure behavior is communication-adjacent but the gate itself is workflow.
- Alternative §7.x (Disciplines) was rejected because §7 is one-job-per-agent / verify-then-execute / autonomous-ship-on-clean-PASS — seat-identity disciplines, not pipeline-step procedures. Wedging pre-branch hygiene into §7 would muddy the existing §7 framing.
- Alternative "new top-level section near §5/§6" was rejected because the new section is not a peer of the gauntlet pipeline — it is part of how the gauntlet starts. Subsection placement preserves the existing top-level structure.

Numbering continues the existing §5.1-§5.8 run. Same shape Arc 21 (`stoa--14u`) used when adding §5.7 and Arc 24 (`stoa--cm3`) used when adding §5.8.

### 2.2 Section prose (verbatim — ADA pastes this as-is)

```markdown
### 5.9 Pre-branch hygiene — the two-check rule before creating an arc-build branch

Before you create a new arc-build branch (`git checkout -b arc-N/build` or equivalent), run two checks. If either fails, pause and surface — do NOT silently inherit local-ahead state into the arc branch.

**The two-check rule (PRINCIPAL-articulated 2026-05-17):**

1. **No other arc-build branch is in flight.** The prior arc's branch must be merged AND deleted before a new one is created. PRINCIPAL's framing:

   > "at most one team working on a repo at any one time"
   >
   > "pliny can't create more than one branch to work with until the other is committed and merged"

   Detection: `git branch | grep -E '^\s*arc-[0-9]+/build$'` should return at most the branch you are about to create (i.e., zero results before creation). Long-running PR branches that have not yet merged are a fail signal.

2. **Local main equals origin/main.** No unpushed commits in either direction.

   ```
   git fetch origin main
   git log --oneline main..origin/main      # must be empty
   git log --oneline origin/main..main      # must be empty
   ```

   Both commands return empty on a clean working tree synchronized with origin. If `main..origin/main` is non-empty, origin has commits local does not — pull or rebase first per operator discretion. If `origin/main..main` is non-empty, local has commits origin does not — push them first under their own PR, NOT bundled into the arc branch.

**On failure of either check, surface — do not silently proceed.** Post a comment on the arc's work-unit ticket tagged `[for: user-tier POLYBIUS]` (or `[for: PRINCIPAL]` when user-tier POLYBIUS is unavailable) naming the specific state observed and the adjudication ask. Worked surfacing shape:

> "Pre-branch check 2 failed: `origin/main..main` shows 3 unpushed commits (`abc1234 chore: ...`, `def5678 docs: ...`, `9abcdef fix: ...`). Recommend pushing these under their own PR first so they do not get absorbed into the arc-N squash. Adjudication ask: (a) push under their own PR first then re-run check; (b) discard if not wanted; (c) something else?"

The surface-on-failure behavior is load-bearing. Silently choosing one of the options (e.g., "I'll just push them") would re-introduce the exact failure mode the discipline closes — operator did not see the state; future POLYBIUS reading the git history sees a bundle they did not authorize.

#### 5.9.1 What this fixes (empirical anchor)

The bundled-squash pattern, observed twice on 2026-05-17:

- **PR #46** (multi-project routine, the-stoa) — squash absorbed 7 pre-existing housekeeping commits; intent was multi-project routine; PR ended up at 23 files instead of the ~5 intended for the routine.
- **PR #8** (Arc 28, the-stoa) — squash absorbed similar pre-existing housekeeping content; intent was Arc 28's bw 0.13.0 substrate adoption; the squash commit subject did not accurately describe the bundled scope.

In both cases the bundled content was legitimate work — no defect, no rollback warranted. The cost is reviewability and substrate-readability: future POLYBIUSes reading git history cannot tell from the squash subject what each arc actually accomplished, and CATO review on each PR was wider than the arc scope justified.

The discipline provably works when applied. Arc 29 (`stoa--ads`, PR #9) shipped clean on 2026-05-17 because the pre-branch check was baked into the Arc 29 activation paste (`HUMAN_paste-pliny-arc-29-instruction.md` — see the "Pre-branch hygiene per directive A9" block). First arc this session without the bundled-squash symptom; first empirical N=1 anchor for the discipline's effectiveness.

#### 5.9.2 Cross-references

- Activation paste convention: `MAJOR_POLYBIUS.md` §5.1 (the POLYBIUS-tier authoring-of-PLINY-pastes section) carries the convention that PLINY-targeted activation pastes include the pre-branch hygiene preamble. The substrate-canonical template `substrate/templates/paste-instruction-template.md` carries the preamble as a mandatory section the template includes. Both of those carriers say the same thing for redundancy with the substantive canon in this §5.9 — the §5.9 prose here is the substantive source of truth; the other two carriers enumerated above are the paste-side redundancy.
- Universal-team layer: `operating-disciplines.md` §24 (cross-ref) carries the brief universal-team framing — today PLINY is the only seat that creates arc-build branches under the gauntlet pipeline; if a future seat ever does (a hotfix CAPTAIN, a sibling-arc CAPTAIN), the discipline applies to that seat too.
- §6.1 (bw command syntax) — the `bw comment` and `[for: ...]` tag conventions used in the surface-on-failure step are documented at `operating-disciplines.md` §12 (bw cookbook) and summarized at §6.1 above.
- `operating-disciplines.md` §6.7.1 (the N=1 canon-promotion gate) — this section enters substrate canon off-gate on PRINCIPAL's 2026-05-17 project-direction declaration; future-evidence accretion per §6.7.1 is the path to "structural lesson" status.
- Empirical anchors: `stoa--3cs` (work-unit ticket carrying the discipline shape + 2026-05-17 scope-expansion comment + N=2 bit-by-it + N=1 worked-when-applied citations), PR #46 + PR #8 (bit-by-it cases), PR #9 (`stoa--ads` / Arc 29 — worked-when-applied case).

#### 5.9.3 N=1 provenance + accretion path

Per `MAJOR_POLYBIUS.md` §15 honest-scope and `operating-disciplines.md` §6.7.1: PRINCIPAL declared this discipline on 2026-05-17 (project-direction authority, captured at `stoa--3cs` thread). §6.7.1 defers to the canon-promotion gate (multiple observations across distinct defect classes + controlled comparison + substrate-level pattern); §6.7.1 does not carve out a separate "PRINCIPAL-declaration shortcut." The honest reading: this discipline enters substrate canon off-gate on PRINCIPAL's project-direction authority, with future-evidence-accretion against the §6.7.1 gate still required for promotion to "structural lesson" status.

The supporting evidence at the time of this writing (2026-05-17):

- **N=2 bit-by-it (defect class: bundled-squash):** PR #46 (multi-project routine; ~7 pre-existing commits absorbed; 23 files instead of ~5) + PR #8 (Arc 28; pre-existing housekeeping absorbed; misleading squash subject). Two observations of the same defect class on the same day; pattern not yet across distinct defect classes per §6.7.1 condition 1.
- **N=1 worked-when-applied (controlled comparison):** Arc 29 (`stoa--ads` / PR #9) shipped clean — the pre-branch check was baked into the activation paste; the bundled-squash symptom did not surface. Single instance of the controlled comparison per §6.7.1 condition 2; accretes as future arcs ship under the discipline.
- **N=1 recursive self-application:** this arc (Arc 30 / `stoa--3cs` / `arc-30/build`) was created from clean main at `140b398` per directive A8; user-tier POLYBIUS verified at dispatch authoring; PLINY verified at branch creation. The discipline applied to its own canonification.

The discipline is in substrate canon NOW because PRINCIPAL named it today and the bit-by-it / worked-when-applied evidence both surfaced today; promotion to "structural lesson" status with multi-arc empirical backing under the encoded canon is a future arcs' work, not this arc's. If the discipline turns out wrong-shaped during future arcs (e.g., the surface-on-failure adjudication ask itself produces operator-friction the discipline should mitigate), future arcs revise this section. Same N=1 framing as Arc 27's §16.6, Arc 28's `operating-disciplines.md` §22.3, and Arc 29's §17.5.
```

### 2.3 What §5.9 does NOT include (out-of-scope inline)

- **No pre-branch git hook implementation.** Per directive A6, discipline-first / tooling-second; the activation-paste preamble + role-file canon is sufficient empirically (Arc 29 proved it works without tooling).
- **No retroactive PR re-shape guidance for PR #46 / PR #8.** The bundled content is legitimate; no unwind; the discipline is forward-only.
- **No cron-hygiene preamble canonification.** Separate forthcoming arc per directive A6; this arc encodes the pre-branch hygiene preamble specifically, leaving the cron-hygiene preamble at its current ad-hoc paste-instruction location.
- **No `MAJOR_POLYBIUS.md` §5.1.1 "positive references only" extension.** Out of scope per directive A6.
- **No sibling-arc-build branch coordination protocols.** The discipline says "merge + delete prior branch first"; HOW PRINCIPAL/user-tier signal that to PLINY is operator-discretion not substrate-canon.

---

## §3 — D2: Activation paste convention encoded (Option γ — both carriers)

**Pick: Option γ — encode in BOTH `MAJOR_POLYBIUS.md` §5.1 AND `substrate/templates/paste-instruction-template.md`.**

### 3.1 Rationale for Option γ over α or β alone

The three options the directive named:

- **Option α** (MAJOR_POLYBIUS.md §5 onboarding-flow area): canon section saying PLINY-targeted activation pastes MUST include the pre-branch hygiene preamble. Reader profile: POLYBIUS at session start when authoring a PLINY activation paste. Doesn't reach the template's actual mechanical fill.
- **Option β** (paste-instruction-template.md): mandatory section the template includes. Reader profile: the template-fill mechanism at session start; POLYBIUS sees it when filling the template. Doesn't reach the POLYBIUS-tier conceptual canon that explains WHY.
- **Option γ:** both.

Option γ matches the substrate's existing redundant-canon pattern (`MAJOR_PLINY.md` §6.1 bw-syntax notes + `operating-disciplines.md` §12 universal bw cookbook — N-carrier canon saying the same thing for different reader contexts). For a discipline that's load-bearing on every arc-build, the three-carrier shape (substantive canon at PLINY §5.9 source-of-truth + POLYBIUS §5.1.2 paste-authoring canon + template expansion at session-start mechanical fill) is the right insurance: if a future template revision drops the preamble, the §5.1.2 canon catches it; if a future POLYBIUS reads only the template at session start, the template carries it; and the §5.9 substantive canon is the cold-read source of truth that both paste carriers cross-reference. The cost of three carriers is two short sections that cross-ref the substantive canon; the benefit is structural redundancy on a discipline whose load-bearingness was demonstrated empirically twice today. The three-way drift surface is the explicit tradeoff named at §6.2.

The substrate redundancy property is itself a §6 (operating-disciplines) principle — "redundancy IS the safety property." Applying it to substrate canon authoring is the same shape applied to substrate canon for redundant gauntlet checking.

### 3.2 Option α — `MAJOR_POLYBIUS.md` §5.1 extension

**Insertion locus:** `MAJOR_POLYBIUS.md` §5.1 currently terminates at line 210 (`...is the answer.` — the paragraph ending the LLM-generation rationale). New subsection §5.1.2 inserts after §5.1.1 (which is the "Positive references only when filling slots" subsection at lines 212-226) and before §5.2 (line 228, "install.sh is template-based"). §5.1.1 is OUT OF SCOPE for this arc per directive A6 — we do NOT edit §5.1.1; we ADD §5.1.2 alongside it.

**Section prose (verbatim — ADA pastes this as-is):**

```markdown
#### 5.1.2 PLINY-targeted activation pastes include the pre-branch hygiene preamble by default

When filling the activation-paste template for a PLINY session, include the pre-branch hygiene preamble by default. The preamble names the two-check rule documented at `MAJOR_PLINY.md` §5.9 and tells PLINY to run the checks before creating the arc-build branch. Default-include means: every PLINY-targeted activation paste carries the preamble unless POLYBIUS explicitly suppresses it for a recognized non-arc engagement.

**The preamble text (verbatim — paste this into every PLINY activation by default):**

```
Pre-branch hygiene per MAJOR_PLINY.md §5.9: before creating arc-N/build, run two checks.

Check 1 (no other arc-build branch in flight):
  git branch | grep -E '^\s*arc-[0-9]+/build$'    # must be empty

Check 2 (local main = origin/main):
  git fetch origin main
  git log --oneline main..origin/main             # must be empty
  git log --oneline origin/main..main             # must be empty

If either check fails, surface to user-tier POLYBIUS (or PRINCIPAL via [for: PRINCIPAL]
tag when user-tier unavailable) with the specific state observed. Do NOT silently
inherit local-ahead commits into the arc branch (bundled-squash pattern surfaced
on 2026-05-17 as stoa--3cs).
```

The preamble is included by default in every PLINY-targeted activation paste. POLYBIUS may suppress to empty ONLY on explicit recognition that the activation will not plausibly create an arc-build branch (e.g., a documented recovery paste for a non-arc engagement POLYBIUS knows is read-only or analysis-only). The cost calculus drives the default: an included preamble PLINY does not need is one paragraph PLINY reads and skips; an omitted preamble PLINY did need is the bundled-squash failure mode this discipline exists to prevent. Substrate-discipline-redundancy IS the safety property — default-include encodes the redundancy structurally rather than relying on POLYBIUS's session-by-session "will this session plausibly create a branch?" judgment, which is a semantic predicate not always knowable at template-fill time.

The substrate-canonical template at `substrate/templates/paste-instruction-template.md` carries the preamble as a template section so the fill mechanism inserts it automatically. The canon section here ensures POLYBIUS understands WHY the preamble is there and does not delete it when refreshing the paste for a compact-or-clear recovery. Mid-arc recovery pastes (a re-paste that picks up an already-created arc-build branch) still carry the preamble by default — PLINY will read it, observe that the branch already exists, and skip the check naturally. The cost of the redundant read is paragraph-scale; the benefit is the redundancy property.

**Cross-references:**

- `MAJOR_PLINY.md` §5.9 — the two-check rule plus the surface-on-failure behavior PLINY runs.
- `substrate/templates/paste-instruction-template.md` — the substrate-canonical template that carries the preamble in its filled output.
- `operating-disciplines.md` §24 — the universal-team layer cross-ref (today PLINY only; future seats that create arc-build branches inherit the same discipline).
- Empirical anchor: `stoa--3cs` (2026-05-17 N=2 bit-by-it + N=1 worked-when-applied).
```

### 3.3 Option β — `substrate/templates/paste-instruction-template.md` extension

**Insertion locus:** `paste-instruction-template.md` currently has Substitution-slots table (lines 13-22), per-slot rationale (lines 28-35), Template block (lines 39-51), Worked example (lines 55-86), Where-the-filled-paste-instruction-lives (lines 89-94), When-to-refresh (lines 96-103), Why-string-substitution (lines 105-117). The template block itself (lines 41-49) is the load-bearing piece — what gets actually pasted.

**Two edits.** Per the template's existing convention, `{{...CLAUSE}}` slots are NOT added to the Substitution-slots table — they are documented as prose-rules next to the slot's expansion. The existing `{{PENDING_DIRECTIVES_CLAUSE}}` follows this pattern (template line 51: a one-line prose rule under the Template block; no table row; no per-slot rationale bullet — the rationale list at template lines 28-35 is for table-listed slots only). `{{PRE_BRANCH_HYGIENE_CLAUSE}}` matches the same shape — it is a derived/expansion clause, not a directly-filled substitution. The two edits below preserve this template-infra convention. Adding `{{PENDING_DIRECTIVES_CLAUSE}}` to the table or its per-slot rationale list is out of scope per directive A6 (template-infra revision adjacent to A6 hard-locks).

**Edit 3.3.a — extend the Template block with the preamble + add a prose-rule for the new clause.** The existing template body is 4 lines (sentence 1: read role file; sentence 2: session intent; sentence 3: bw prefix + pending directives; sentence 4: compact-or-clear recovery). The new template body adds a pre-branch hygiene block between sentence 2 and sentence 3, controlled by a new clause `{{PRE_BRANCH_HYGIENE_CLAUSE}}` that expands per the prose-rule below — matching the existing `{{PENDING_DIRECTIVES_CLAUSE}}` prose-rule pattern.

**Updated Template block (replaces the current template block at lines 41-49):**

```markdown
## Template

```
Read {{ROLE_FILE_PATH}} and assume the orchestrator role for {{PROJECT_NAME}}.

Your immediate intent for this session: {{SESSION_INTENT}}

{{PRE_BRANCH_HYGIENE_CLAUSE}}

Check beadwork ({{BW_PREFIX}}-- prefix) for pending directives from MAJOR_POLYBIUS{{PENDING_DIRECTIVES_CLAUSE}}.

If compaction or /clear erases your role, re-read this paste from {{ON_DISK_PATH}} in the project root.
```

`{{PRE_BRANCH_HYGIENE_CLAUSE}}` expands to the preamble below by default in every PLINY-targeted activation paste — included by default, not gated on POLYBIUS's session-by-session judgment. POLYBIUS may suppress to empty string ONLY on explicit recognition that the activation will not plausibly create an arc-build branch (e.g., a recovery paste for a documented non-arc engagement). Default-include is the safety property: the cost of including the preamble when not branching is one paragraph PLINY reads and skips; the cost of omitting it on a session that pivots to arc work mid-engagement is the bundled-squash pattern this arc exists to prevent. When the clause is suppressed to empty, the surrounding blank lines collapse.

The preamble (the default expansion):

```
Pre-branch hygiene per MAJOR_PLINY.md §5.9: before creating arc-N/build, run two checks.

Check 1 (no other arc-build branch in flight):
  git branch | grep -E '^\s*arc-[0-9]+/build$'    # must be empty

Check 2 (local main = origin/main):
  git fetch origin main
  git log --oneline main..origin/main             # must be empty
  git log --oneline origin/main..main             # must be empty

If either check fails, surface to user-tier POLYBIUS (or PRINCIPAL via [for: PRINCIPAL]
tag when user-tier unavailable) with the specific state observed. Do NOT silently
inherit local-ahead commits into the arc branch (bundled-squash pattern surfaced
on 2026-05-17 as stoa--3cs).
```

`{{PENDING_DIRECTIVES_CLAUSE}}` expands to ` — start with: {{PENDING_DIRECTIVES}}` when pending directives are named; otherwise it expands to empty string and the preceding sentence ends after `MAJOR_POLYBIUS`.
```

**Edit 3.3.b — extend the Worked example (template lines 55-86) to show the preamble in the rendered output.** The existing worked example (template lines 67-76) shows the filled paste without the preamble (because the example pre-dates Arc 30). Update the worked example's filled-paste rendering to include the preamble between "Your immediate intent..." and "Check beadwork..." lines, matching the new template body. Keep the surrounding prose ("Suppose the interview produced..." + "The filled paste-instruction:") intact; only the rendered paste block changes.

**No table-row edit, no per-slot-rationale-bullet edit.** Per the convention noted at the top of §3.3, the new clause is documented via prose-rule next to its expansion (in Edit 3.3.a above), not via the Substitution-slots table or the per-slot rationale list. This keeps the new clause structurally consistent with the existing `{{PENDING_DIRECTIVES_CLAUSE}}` and avoids partial-conversion (where one CLAUSE is in the table and another is in prose).

### 3.4 What Option γ does NOT do

- Does NOT modify the Arc 27/28/29 paste-instruction files at the-stoa root. Those are forward-only empirical record per directive A6.
- Does NOT add a non-PLINY activation-paste preamble. The template is PLINY-specific; POLYBIUS activation pastes have their own template (`substrate/templates/paste-instruction-polybius-template.md` or similar — if a separate template exists). The directive scoped D2 to PLINY-targeted pastes only.
- Does NOT add the cron-hygiene preamble (forthcoming separate arc per directive A6).

---

## §4 — D3: `operating-disciplines.md` cross-ref (universal-team layer thin)

**Pick: thin cross-ref section, not a full universal-team mirror.**

### 4.1 Rationale for thin cross-ref over full universal-team section

Today, under the current gauntlet pipeline, **only PLINY creates arc-build branches**. ADA works on a branch PLINY already created; DAEDALUS / ARGUS / VERA / CATO / ZENO never touch the git branch state at all; CURATOR / HERALD / STRABO / BARTLEBY are read-only or analysis seats. The universal-team framing is therefore THIN: "any seat that ever creates an arc-build branch under this team's gauntlet runs the pre-branch hygiene; today that's only PLINY."

The directive's D3 phrasing was: "Cross-ref minimum; universal section only if you judge wider framing earns its keep." The judgment is that wider framing does NOT earn its keep at this dispatch — there is no second seat doing the discipline; a full mirror would be canon for an empty set. A thin cross-ref records the universal-team framing as a one-line acknowledgement and points readers at the PLINY-tier canon for the substance.

Future arcs that introduce non-PLINY branch-creating seats (e.g., a hotfix CAPTAIN or a sibling-arc CAPTAIN) can promote §24 to a full universal-team section at that point — and the empirical evidence those arcs would surface (a second seat actually doing the discipline) is exactly what `operating-disciplines.md` §6.7.1 needs to promote the discipline to "structural lesson with universal scope." Today, with only PLINY exercising the discipline, the §6.7.1 honest move is thin-cross-ref.

### 4.2 Insertion locus — new §24 cross-ref section

**Insertion point:** at the end of `operating-disciplines.md`, after current §23 ("Base vs custom agents (universal-team framing)") which terminates at the file's natural numbered-disciplines tail before the "Agent-regime inverses (positive framing)" block and the "Empirical lineage" block at the file tail. New §24 inserts as a top-level numbered section between §23's closing `---` separator and the "Agent-regime inverses" block.

Numbering continues the existing §1-§23 run; same insertion pattern Arc 28 used for §22 and Arc 29 used for §23.

### 4.3 Section prose (verbatim — ADA pastes this as-is)

```markdown
## 24. Arc-build branch hygiene (PLINY-primary; cross-ref)

Any seat that creates an arc-build branch (`arc-N/build` or equivalent) under this team's gauntlet runs the two-check pre-branch hygiene rule before `git checkout -b`:

1. **No other arc-build branch in flight.** Prior arc's branch must be merged AND deleted.
2. **Local main = origin/main.** No unpushed commits in either direction.

The full canon — including PRINCIPAL's 2026-05-17 verbatim phrasing, the surface-on-failure adjudication shape, the N=2 bit-by-it + N=1 worked-when-applied empirical anchor, and the §6.7.1 N=1 provenance + accretion path — lives at `MAJOR_PLINY.md` §5.9. The activation-paste convention that carries the preamble into every PLINY arc-build paste lives at `MAJOR_POLYBIUS.md` §5.1.2 plus the substrate-canonical template `substrate/templates/paste-instruction-template.md`.

**Why thin cross-ref, not full universal-team mirror.** Under the current gauntlet pipeline, only PLINY creates arc-build branches. ADA works on a branch PLINY created; verifier and analysis CAPTAINs never touch git branch state. The universal-team framing is recorded here for completeness — if a future seat introduces branch-creating responsibilities (a hotfix CAPTAIN, a sibling-arc CAPTAIN), this section can promote to a full universal-team mirror at that point. Today, with PLINY as the only branch-creating seat, the substantive canon lives at `MAJOR_PLINY.md` §5.9 and the thin cross-ref here suffices.

**Cross-references:**

- `MAJOR_PLINY.md` §5.9 — the full discipline section.
- `MAJOR_POLYBIUS.md` §5.1.2 — the activation-paste authoring convention.
- `substrate/templates/paste-instruction-template.md` — the template that carries the preamble in its filled output.
- §6.7.1 (the N=1 canon-promotion gate this discipline enters off-gate on PRINCIPAL's 2026-05-17 declaration).
- Empirical anchors: `stoa--3cs` (work-unit + 2026-05-17 scope-expansion), PR #46 + PR #8 (bit-by-it N=2), PR #9 / `stoa--ads` (worked-when-applied N=1).
```

### 4.4 What §24 does NOT include

- No verbatim PRINCIPAL block-quote (it lives at `MAJOR_PLINY.md` §5.9 body, under check 1).
- No re-derivation of the empirical anchor (it lives at `MAJOR_PLINY.md` §5.9.1).
- No re-derivation of the N=1 provenance subsection (it lives at `MAJOR_PLINY.md` §5.9.3).
- No surface-on-failure worked example (it lives at `MAJOR_PLINY.md` §5.9).

The thin shape is deliberate. Full mirroring would double the maintenance surface for canon that has only one operating seat; the cross-ref shape lets future arcs revise the substantive canon at `MAJOR_PLINY.md` §5.9 without re-syncing here.

---

## §5 — D4: Existing activation paste templates / examples updates

**Pick: no updates to Arc 27/28/29 paste files at the-stoa root; one substrate-canonical template update (covered by D2 Option β at §3.3 above).**

Per directive A6, the Arc 27/28/29 activation pastes at the-stoa root (`HUMAN_paste-pliny-arc-27-instruction.md`, `HUMAN_paste-pliny-arc-28-instruction.md`, `HUMAN_paste-pliny-arc-29-instruction.md`) are forward-only empirical record and MUST NOT be edited. They are the de-facto-template that carried preambles ad-hoc; once the substrate-canonical template at `substrate/templates/paste-instruction-template.md` carries the preamble per D2, the Arc 27/28/29 pastes remain as historical anchors showing the discipline's pre-canonification shape.

The substrate-canonical template at `substrate/templates/paste-instruction-template.md` is updated per D2 Option β at §3.3 above; D4 does not introduce any additional template / example file changes beyond what §3.3 specifies. The Arc 30 build will produce its own activation-paste file at the-stoa root (`HUMAN_paste-pliny-arc-30-instruction.md` already exists per the directive-tracking commit `316338c` — that file is FORWARD-ONLY empirical record too once Arc 30 dispatches; not edited by this design).

---

## §6 — Self-assessed weak points (post-work gate per CAPTAIN_DAEDALUS_the_stoa.md §6.2)

The points below are brittle spots an ARGUS cold-read should re-pressure-test. The design proceeds despite them; the defenses are short.

### 6.1 The default-include posture for `{{PRE_BRANCH_HYGIENE_CLAUSE}}` accepts paragraph-scale paste bloat to close a silent-bypass surface

The new `{{PRE_BRANCH_HYGIENE_CLAUSE}}` slot defaults to ALWAYS-INCLUDE — every PLINY-targeted activation paste carries the preamble unless POLYBIUS explicitly suppresses it for a recognized non-arc engagement. The cost: every paste, including mid-arc compact-or-clear recoveries against an already-existing branch, carries one paragraph of pre-branch-check prose that PLINY reads and skips when no branch creation is forthcoming. Operator-noise scale: ~12 lines per paste.

**Why this shape anyway (post-rev2 default flip per PLINY adjudication):** the rev1 design had this as default-OMIT-unless-POLYBIUS-judges-applicable, with POLYBIUS's "will this session plausibly create a branch?" judgment at template-fill time. ARGUS pressure-tested that shape and surfaced the structural asymmetry: `{{PENDING_DIRECTIVES_CLAUSE}}` has a STRUCTURAL trigger (content-presence — POLYBIUS knows at fill-time whether pending directives exist), but `{{PRE_BRANCH_HYGIENE_CLAUSE}}` has a SEMANTIC trigger (will-this-session-plausibly-branch) that is not always knowable at fill-time. A mid-arc compact-or-clear paste authored without the preamble can turn into a branch-creating session if the prior arc closes mid-session and the session pivots. The cost of a missed preamble is the bundled-squash this arc exists to prevent; the cost of an always-included preamble is one paragraph PLINY reads and skips. PLINY adjudication: flip the default to ALWAYS-INCLUDE. The structurally-under-defended POLYBIUS-judgment-per-session shape is replaced by structural-redundancy-as-safety; the cost is paragraph-scale paste text PLINY reads and skips when not branching, and the benefit is no silent bypass on a session that pivots to arc work mid-engagement. This matches the substrate's own redundant-canon value system (PLINY §6.1 ↔ operating-disciplines §12; redundancy IS the safety property — applied here to the activation-paste convention itself).

### 6.2 D2 Option γ is THREE carriers — three-way drift surface (not two)

The design carries the preamble in three places, not two: (a) the substantive canon at `MAJOR_PLINY.md` §5.9 (the discipline itself plus check 1's command list and check 2's command list — the source of truth for the commands); (b) the paste preamble verbatim text at `MAJOR_POLYBIUS.md` §5.1.2 (canon section that POLYBIUS reads when authoring activation pastes); (c) the paste preamble verbatim text inside `substrate/templates/paste-instruction-template.md`'s `{{PRE_BRANCH_HYGIENE_CLAUSE}}` expansion (the actual rendered-into-paste text). If a future arc revises one carrier (e.g., swaps the check 1 detection probe from a local `git branch | grep` to a `gh pr list` query) and forgets the other two, canon-vs-paste drift surfaces — two carriers say different things and the redundancy property fails, generating uncertainty about which is canonical.

**Why this shape anyway:** all three carriers cross-reference each other explicitly (§5.9 names the activation-paste convention at the §5.9.2 cross-references block; §5.1.2 names both §5.9 and the template in its cross-references list; the template's prose-rule under the Template block names §5.9 and the §5.1.2 canon section, and the §5.9 cross-references include the template path). Canon-vs-paste drift surfaces on the next CATO cold-read of either carrier — exactly the same property that `MAJOR_PLINY.md` §6.1 ↔ `operating-disciplines.md` §12 already exhibits today (bw command syntax carried in two carriers across two role-files plus three CAPTAIN-file heartbeat references for some commands). The redundant-canon pattern is the substrate's accepted tradeoff: maintenance cost of N-way carrier sync vs. the catch-on-cold-read property that ensures no single forgotten edit silently breaks an arc. Three carriers is one more than two — proportionally one more surface to drift on, but the catch property scales the same way.

### 6.3 The §6.7.1 N=1 framing rests on PRINCIPAL-declaration-authority off-gate

The discipline enters substrate canon today on PRINCIPAL's project-direction declaration alone; §6.7.1 explicitly does not carve out a PRINCIPAL-declaration shortcut. The honest reading (per §5.9.3) is that promotion to "structural lesson" status is a future-arcs' job. ARGUS may surface that as a soft inconsistency — substrate canon is in NOW but the gate it cites does not formally license being in NOW.

**Why this shape anyway:** the exact same N=1 framing was used at Arc 27 §16.6 (POLYBIUS session lifecycle), Arc 28 §22.3 (bw-upgrade discipline), and Arc 29 §17.5 / §23.4 (base-vs-custom convention). The pattern is established substrate norm: PRINCIPAL declares; canon enters off-gate with N=1 provenance named honestly; future arcs accrete evidence against §6.7.1's three conditions. Re-litigating the shape here would put Arc 30 out of step with the canon's own established meta-pattern.

### 6.4 §5.9 sits in the §5 family but the §5 family is about gauntlet-pipeline beats

The §5 family is titled "The gauntlet pipeline" and every prior subsection (§5.1-§5.8) is a beat WITHIN the running pipeline (dispatch brief shape, ADA preamble, sub-agent watchdog, post-STRABO VERA dispatch, etc.). Pre-branch hygiene is a beat BEFORE the pipeline starts — arguably "Phase 0" rather than a §5 subsection. ARGUS may surface that the locus choice stretches the §5 family's scope.

**Why this shape anyway:** §5.7 (smoke-beat discipline) is similarly "Phase C smoke beat" not a pipeline-running beat, and §5.8 (background-dispatch hygiene) covers a workflow surrounding the pipeline (CronCreate, task_id materialization). The §5 family has already absorbed adjacent-but-not-strictly-inside-the-pipeline subsections. A new top-level section (§6.x or §7.x) would either muddy a different family's scope or create a one-subsection top-level (`§6.5 Pre-branch hygiene`) that's structurally awkward. §5.9 is the least-bad locus given the existing structure.

### 6.5 Check 1 detection probe is heuristic, not authoritative

The proposed `git branch | grep -E '^\s*arc-[0-9]+/build$'` heuristic checks the local branch list for arc-N/build-named branches. It does NOT catch (a) arc branches that have been merged + pushed but not deleted locally (false-positive — would surface "in flight" when actually closed); (b) arc branches that exist remotely but not locally (false-negative — would not surface when there is one in flight on origin). The directive cites PRINCIPAL's rule as "at most one team working on a repo at any one time" + "until the other is committed and merged" — what the discipline checks for is the OPERATIONAL state, not just the local-branch state.

**Why this shape anyway:** the canonical operational state is "is there an open PR for an arc-build branch?" — answerable via `gh pr list --state open --head 'arc-*/build'` or similar. That probe is more authoritative but introduces a `gh` dependency that may not be present in every consumer workspace. The local-branch heuristic is a baseline; the surface-on-failure adjudication ask gives the operator the chance to clarify ("yes there's an open PR; no it's safe to proceed because that PR is on a different repo / the merge will land before this arc closes"). A future arc could harden the probe to require `gh` and use the PR-list query; today's discipline accepts the heuristic because it matches what the bit-by-it cases (PR #46 + PR #8) actually were — local-ahead-without-pushed-PR is the bundled-squash precondition the heuristic detects.

### 6.6 The discipline name itself does not specify cleanup ordering

The two-check rule does not say what PLINY should do when checks pass mid-arc and PLINY needs to re-verify (e.g., after a long-running design phase where origin may have advanced). The discipline is "before `git checkout -b`"; once the branch exists, the discipline does not re-fire. If user-tier POLYBIUS lands an unrelated commit on origin/main during a long arc, the local arc branch's eventual merge will resolve that via standard git rebase / merge mechanics — but the discipline's canon section is silent on it.

**Why this shape anyway:** mid-arc origin/main changes are a different problem class (merge conflict / rebase discipline) not "PLINY silently inheriting unpushed local commits at branch creation." The directive's A6 hard-locks "sibling arc-build branch coordination protocols" — what other tiers / projects do during the arc is operator-discretion not substrate-canon. The discipline is scoped narrowly because the empirical evidence is narrow; broader scoping would invite the wider-canon-creep ARGUS should flag.

---

## §7 — Cite-comments resolution (per directive A4)

Every cross-reference in this design's encoded canon points at a section that exists today (or will exist after this arc lands). Inventory:

- `MAJOR_PLINY.md` §5.9 → new section this arc adds. Will exist post-ADA.
- `MAJOR_PLINY.md` §6.1 → exists (line 349-379, "Working with beadwork — command syntax").
- `MAJOR_POLYBIUS.md` §5.1 → exists (line 198, "Custom paste-instruction templating — string substitution").
- `MAJOR_POLYBIUS.md` §5.1.1 → exists (line 212, "Positive references only when filling slots"). NOT edited.
- `MAJOR_POLYBIUS.md` §5.1.2 → new subsection this arc adds. Will exist post-ADA.
- `MAJOR_POLYBIUS.md` §15 → exists (line 776, "Retrospective discipline — N=1 conclusions are not structural lessons").
- `operating-disciplines.md` §6.7.1 → exists (line 81, "The N=1 rule").
- `operating-disciplines.md` §12 → exists (line 450, "bw cookbook").
- `operating-disciplines.md` §24 → new section this arc adds. Will exist post-ADA.
- `substrate/templates/paste-instruction-template.md` → exists; edited per §3.3.

CATO's cold-read should verify each line/section reference resolves in the post-ADA tree.

---

## §8 — Out-of-scope items (for ARGUS's frame)

Per directive A6, the following are HARD-LOCKED out of scope and this design does NOT address them:

- Tooling / pre-branch git hook enforcement (discipline-first; tooling-second; future arc may add).
- Restructuring of PR #46 / PR #8 squashes (bundled content is legitimate; no unwind).
- Cron-hygiene canonification (separate forthcoming arc; this arc encodes pre-branch hygiene only).
- `MAJOR_POLYBIUS.md` §5.1.1 cross-project-context-leak extension (separate arc).
- `stoa--32b.1` (PRINCIPAL-gate discipline) — FILED but NOT YET BUILT; if any design clause needs "PRINCIPAL-discretion," use "block + escalate immediately" wording per directive forward-awareness note.
- `stoa--32b.2` (mechanical-script/agent-split) — separate arc.
- Sibling-arc-build branch coordination protocols (operator-discretion, not substrate-canon).

If ARGUS surfaces a risk in any of the above categories, the right response is "out of scope per A6; route to a follow-up ticket via PLINY" — not "expand this design's scope."

---

## §9 — Residual questions for ARGUS

These are concerns I want ARGUS to evaluate explicitly during cold-audit:

1. **§5.9 locus choice (§6.4 weak point).** Is the §5 family the right home, or should pre-branch hygiene live as a peer-of-§5 top-level section? My read: §5.7 + §5.8 already absorbed adjacent-to-pipeline workflow disciplines; §5.9 fits the same shape. ARGUS may pressure-test by reading the §5 family from §5.1 forward and asking whether §5.9 reads coherently as the next subsection.
2. **D2 Option γ over α-only or β-only (§6.2 weak point).** Three carriers (substantive canon at PLINY §5.9 + paste preamble in POLYBIUS §5.1.2 + paste preamble in template's clause expansion) is the substrate redundant-canon pattern; the three-way drift risk is real. ARGUS may evaluate whether the redundancy property justifies the maintenance cost, or whether one carrier (β — the template) is sufficient because POLYBIUS reads the template at fill time and the §5.1.2 canon is mostly decorative.
3. **§5.9 check 1 heuristic (§6.5 weak point).** `git branch | grep -E '^\s*arc-[0-9]+/build$'` catches the bit-by-it cases (local-ahead-without-pushed-PR) but misses merged-but-not-locally-deleted branches and remote-only branches. ARGUS may pressure-test whether the heuristic is sufficient given the bit-by-it failure mode it actually closes, or whether a stricter probe (with `gh` dependency) is the right shape for canon.
4. **§5.9.3 N=1 framing entering off-gate on PRINCIPAL declaration (§6.3 weak point).** Same shape as Arcs 27/28/29 — established substrate norm. ARGUS may surface this as a soft inconsistency or accept it as canon meta-pattern.
5. **Surface-on-failure worked example (§5.9 prose).** The worked example uses three hypothetical commit SHAs and ask-options. ARGUS may pressure-test whether the example is concrete enough to be useful or risks reading as scripted ceremony; alternatives include using one of the actual PR #46 or PR #8 commit anchors.

---

## §10 — Summary for verdict

**Sub-decision picks (documented):**

- **D1:** new section `MAJOR_PLINY.md` §5.9 (in the §5 gauntlet-pipeline family, after §5.8); carries the two-check rule, PRINCIPAL block-quote (both load-bearing lines), surface-on-failure behavior, N=2 bit-by-it + N=1 worked-when-applied evidence, §15 + §6.7.1 dual-cited N=1 provenance.
- **D2:** Option γ — encode in both `MAJOR_POLYBIUS.md` §5.1.2 (canon section) AND `substrate/templates/paste-instruction-template.md` (new `{{PRE_BRANCH_HYGIENE_CLAUSE}}` clause via prose-rule matching the existing `{{PENDING_DIRECTIVES_CLAUSE}}` convention — template-block update + worked-example update; NO Substitution-slots table row, NO per-slot rationale bullet, per the existing CLAUSE convention). Default is ALWAYS-INCLUDE in every PLINY-targeted activation paste (per PLINY rev2 adjudication absorbing ARGUS r5 — structural redundancy beats POLYBIUS-judgment-per-session for a semantic-triggered clause). Redundant-canon pattern matching the existing PLINY §6.1 ↔ operating-disciplines §12 shape — three-way drift surface accepted with cross-references between all carriers.
- **D3:** thin cross-ref at new `operating-disciplines.md` §24 — universal-team layer recorded but substantive canon points at `MAJOR_PLINY.md` §5.9. Future arcs may promote §24 to a full universal-team mirror when a non-PLINY branch-creating seat surfaces.
- **D4:** no edits to Arc 27/28/29 paste files (forward-only per A6); the substrate-canonical template edit is covered by D2 Option β at §3.3.

**Recursive self-application:** this arc was created on a clean main (`140b398`) per directive A8; PLINY ran the discipline before encoding it. Recursive shape matches Arcs 24/25/29.

**Authorship attribution:** all new prose attributed to the PRINCIPAL (Denson Smith) per substrate/CLAUDE.md. No new author-like fields introduced beyond what already exists in `substrate/templates/paste-instruction-template.md` frontmatter (which already names Denson Smith — verified per directive A5).

**Estimated build size:** ~one §5.9 section (~80 lines of canon prose) + one §5.1.2 subsection (~30 lines) + two edits to `paste-instruction-template.md` (template block with new clause + prose-rule for the clause, worked-example block; ~30 lines net — no table-row, no per-slot rationale bullet per the existing CLAUSE convention) + one §24 section (~25 lines). Total: ~165 lines of canon edits across three files. Single ADA pass expected; CATO cold-read mandatory per directive Phase A1.

End design.
