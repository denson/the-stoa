# Design rev2 — forge-promotion of the workflow-composer skill (stoa--04n / Arc 53)

**Stage:** Gauntlet Stage A (design), DAEDALUS, design-rev2.
**Supersedes/extends:** `agents/design/stoa--04n/design.md` (Stage-A rev1, deploy-wiring half — still valid). This rev2 ADDS the skill-content-currency scope rev1 predated, CORRECTS rev1's cite count (4→5) and post-edit range (198-207→198-208), and CLOSES rev1's worktree-mechanics gap (the untracked-source-commit step).
**Operating mode:** HITL.
**Status:** design complete, ready for ARGUS critique → HARD STOP.

---

## 1. Goal (problem restatement)

Promote the on-disk-but-untracked `substrate/skills/workflow-composer/SKILL.md` into substrate canon so `install.sh` deploys it to every workspace and `check-substrate-updates` drift-checks it like any base skill — AND verify the promoted skill is current as of the 2026-06-01 Workflow docs (the five deltas survive promotion). Promotion has THREE mechanical parts the prior design under-counted: (a) bring the untracked source into the tracked tree (`git add`/commit the dir), (b) wire it into `SKILL_NAMES`, (c) fix the stale `install.sh:140` cites in `check.sh` — at FIVE occurrences, to the post-edit range `198-208`. The skill content is final-as-refreshed: PROMOTE + VERIFY, do NOT re-author (locked decision #1). A missing/wrong delta is a build FINDING to fix, not a content rewrite.

**Imported assumptions (named per §6.1):**
- *Promotion = bring-into-tracked-tree.* The brief states the worktree shares only committed content, so the untracked skill dir is absent from a fresh clone. I treat "promote the skill" as REQUIRING the `git add` step — without it, `SKILL_NAMES` would name a skill that does not exist in the tracked tree and a fresh-clone install would fail the source-existence guard. This is the load-bearing correction rev1 lacked.
- *Cite-fix target is the POST-edit range.* Because the build ADDS one array entry (closing paren moves 207→208), the corrected cite must read `install.sh:198-208`, not the pre-edit `198-207`. Writing the pre-edit range would re-introduce the same staleness class on the next edit.
- *gen-data is a frontmatter guard, not a deploy test* (inherited from rev1's ARGUS MINOR; confirmed: the Zod skill schema requires only `name`+`description`, both present; `author` is an ignored extra field).

## 2. Build-stage change list (for ADA — file:line precision)

All paths relative to the arc-build worktree root (`.claude/worktrees/arc-53-build/`).

### 2.1 Commit the untracked source into the tracked tree (NEW — rev1 gap)
- **`substrate/skills/workflow-composer/SKILL.md`** is UNTRACKED in this worktree (`git ls-files` returns empty; `git status` shows `?? substrate/skills/workflow-composer/`). It was staged byte-faithfully by PLINY (sha256 `03de64e5…073af`).
- **Action:** `git add substrate/skills/workflow-composer/` so the dir + SKILL.md enter the tracked tree and land in the build commit. This is the actual "promotion" — without it, items 2.2/2.3 wire a deploy target that the tracked tree does not contain.
- **Do NOT re-author or re-format the file.** Add it verbatim. Verify post-add sha256 still matches `03de64e5…073af` (probe P0).

### 2.2 Wire into SKILL_NAMES (the deploy edit)
- **File:** `substrate/install.sh`. **Current array:** lines **198-207** (`SKILL_NAMES=(` at 198; entries 199-206: agent-author, check-substrate-updates, credential-discipline, check-bw-release, inspect-script-output, handoff-author, save-verdict, validate-spec; `)` at 207).
- **Action:** append `  workflow-composer` as a new entry between current line 206 (`validate-spec`) and line 207 (`)`). Order is not alphabetized (rev1 verified), so append at the end.
- **Post-edit:** array becomes 9 entries; `SKILL_NAMES=(` stays at 198, entries 199-207, `)` moves to **208**. The literal-anchored array spans **198-208**. (This new range is the cite-fix target in 2.3.)
- No `check.sh` parser edit needed for enrollment: both drift passes live-parse via `parse_skill_names_from_install()` anchored on `^SKILL_NAMES=\(` (rev1 §2, re-confirmed). Adding the name auto-enrolls it.

### 2.3 Fix the stale `install.sh:140` cite at ALL FIVE occurrences (rev1 said 4)
- **File:** `substrate/skills/check-substrate-updates/check.sh`. **Five occurrences** (verified by grep; rev1 + directive enumerated only four — line 236 was missed, the Arc-52 ARGUS MAJOR-2 "same class"):

  | check.sh line | Current stale text (fragment) | Corrected to |
  |---|---|---|
  | 76 | `(which parses install.sh:140-144's SKILL_NAMES array)` | `install.sh:198-208` |
  | 228 | `CITE: parses install.sh:140-144 (SKILL_NAMES array, multi-line form)` | `install.sh:198-208` |
  | 236 | `substrate that has skills (i.e. install.sh:140 region exists but stdout is` | `install.sh:198 region` |
  | 385 | `parse_skill_names_from_install (which parses install.sh:140-144)` | `install.sh:198-208` |
  | 435 | `install.sh:140-144); the find-walk inside each named dir is source-side` | `install.sh:198-208` |

- **Note the two text shapes:** four cites are the range form `install.sh:140-144` → `install.sh:198-208`; ONE cite (236) is the bare-line form `install.sh:140 region` → `install.sh:198 region` (the open-paren line, where the parser begins matching). ADA must not blindly s/140-144/198-208/ — line 236 has no `-144` suffix and must become `198 region`, not `198-208 region`.
- These are stale-comment hygiene (the awk anchors on the literal `^SKILL_NAMES=\(` pattern, not line numbers, so the parser keeps working regardless); the fix keeps the human-facing cites honest after the +1-entry shift.

### 2.4 gen-data guard
- **After 2.1-2.3:** run `npm run gen-data` in `app/` (`tsx scripts/gen-data.ts`). The adapter globs `substrate/skills/<name>/SKILL.md` (independent of `SKILL_NAMES`) and Zod-validates frontmatter (`name`+`description` required; both present). Expect exit 0 and the skill to appear in generated data. This validates frontmatter, NOT the deploy wiring (the deploy wiring is tested by the install/drift probes in §4).

### 2.5 OUT of scope (do NOT touch — locked decisions / scope discipline)
- No `WORKFLOW_NAMES` array, no `.claude/workflows/` deploy/drift case in `check.sh` (locked decision #2). Ship only the SKILL.
- The two OTHER stale check.sh cites (`install.sh:60-69` "pair-programmer ambiguity"; `install.sh:766-770` "prune logic") — pre-existing drift, a DIFFERENT class, NOT shifted-wrong by the +1 add. Candidate follow-up ticket only; do NOT fold into Arc 53.
- The `is_substrate_source_present` skills-branch `[ -e ]` existence-test asymmetry (rev1 MINOR) — latent, candidate follow-up, not this arc.
- `author: Denson Smith` (SKILL.md:7) immutable.

## 3. The 5-delta currency verification map (THING 2 — file:line in worktree SKILL.md)

The promoted skill is final-as-refreshed; this map asserts each delta is PRESENT (and the stale `workflow`-as-live-keyword framing is GONE). Line numbers are the worktree SKILL.md (sha `03de64e5…073af`); they are stable because §2.1 adds it verbatim.

| # | Delta (directive §22) | Lives at (SKILL.md line) | Confirming substance |
|---|---|---|---|
| 1 | Four-primitive framing (agent-teams + subagents, not 3-way) | **§ heading L28; table L30-37** | "four ways… subagents, skills, **agent teams**, workflows"; gauntlet = "agent-teams-for-coordination + subagents-for-execution" |
| 2 | `ultracode` keyword (not pre-v2.1.160 `workflow`) | **L159** | "invocation keyword is **`ultracode`**… the older literal keyword `workflow` applied before v2.1.160" |
| 3 | `args` parameterization | **§ heading L146; body L148-150** | dedicated section "Parameterizing a saved workflow with `args`"; worked case `/defeat-threat` on `stoa--h2z` |
| 4 | Allowlist / `stoa--x4j` stall-fix | **L156** | "Pre-allowlist the commands… not in the tool allowlist still prompt mid-run… exact failure mode of `stoa--x4j`… mandatory for any autonomous/overnight run" |
| 5 | Overnight ≠ workflow (remote routine = unattended vehicle) | **L158; reinforced L185** | "Overnight is NOT a workflow… mechanism is a **remote routine** (claude.ai / `RemoteTrigger`), not a workflow" |

**Stale-framing-GONE assertion:** the only surviving literal `workflow`-as-keyword mention (L159) is explicitly historical ("applied before v2.1.160"), which is correct currency, not stale framing. No line presents `workflow` as the live invocation keyword. (Note: the `workflow()` primitive name appears in L12/L191 referring to the Workflow TOOL's own primitive — that is the tool's API surface, not the invocation keyword, and is correct to retain.)

## 4. Verification probes (VERA-runnable — concrete command + expected result)

Run from the worktree root unless noted. Each is a falsification probe, not a "looks right" check.

**Deploy wiring (THING 1):**
- **P0 (verbatim-promotion):** `git ls-files substrate/skills/workflow-composer/SKILL.md` → returns the path (now tracked). `sha256sum substrate/skills/workflow-composer/SKILL.md` → `03de64e5…073af` (byte-identical to PLINY's staged source; no re-author).
- **P1 (wired):** `grep -n 'workflow-composer' substrate/install.sh` → exactly one hit, inside the `SKILL_NAMES=(` … `)` block (between lines 198 and 208).
- **P2 (count):** `parse_skill_names_from_install` (or `awk` extracting the array) returns **9** names including `workflow-composer`.
- **P3 (dry-run deploy):** dry-run install into a **throwaway** synthetic target (fresh clone per `operating-disciplines.md` §25.5 — NEVER a real workspace) lists the workflow-composer skill deploy; exit 0.
- **P4 (real deploy):** real install into a throwaway target lands `<target>/.claude/skills/workflow-composer/SKILL.md` byte-identical (LF-normalized).
- **P5 (drift MISSING):** a synthetic workspace missing only this skill reports it MISSING (`+`) under Pass 1.
- **P6 (no false OBSOLETE):** a synthetic workspace WITH it deployed does not report it OBSOLETE under Pass 2 (`is_substrate_source_present` classifies it substrate-derived).

**Cite fix (all five):**
- **P7 (zero survivors):** `grep -n 'install\.sh:140' substrate/skills/check-substrate-updates/check.sh` → **0 hits** (all five corrected).
- **P8 (correct replacements):** `grep -n 'install\.sh:198' substrate/skills/check-substrate-updates/check.sh` → **5 hits** at lines 76/228/236/385/435; line 236 reads `install.sh:198 region` (bare line, no `-208`); the other four read `install.sh:198-208`.

**Currency (5 deltas — THING 2):**
- **P9:** `grep -in 'agent team' substrate/skills/workflow-composer/SKILL.md` → hits at L30 + L34 (four-primitive framing present).
- **P10:** `grep -n 'ultracode' SKILL.md` → hit at L159.
- **P11:** `grep -n 'Parameterizing a saved workflow with .args.' SKILL.md` → hit at L146 (args section present).
- **P12:** `grep -in 'allowlist' SKILL.md` → hit at L156; `grep -n 'stoa--x4j' SKILL.md` → hits at L156 + L198.
- **P13:** `grep -in 'remote routine' SKILL.md` → hits at L158 + L185 (overnight≠workflow present).
- **P14 (stale framing gone):** `grep -n 'keyword is .*workflow' SKILL.md` returns ONLY L159 (the historical "applied before v2.1.160" mention); no line presents `workflow` as the live invocation keyword.

**Guards:**
- **P15 (gen-data):** `npm run gen-data` in `app/` exits 0 and the generated data includes a `workflow-composer` skill record.
- **P16 (authorship):** `grep -n 'author:' substrate/skills/workflow-composer/SKILL.md` → `author: Denson Smith` at L7, unchanged. No other author-like field introduced anywhere in the diff.
- **P17 (no-WORKFLOW scope guard):** `grep -c 'WORKFLOW_NAMES' substrate/install.sh` → 0; `grep -ic 'workflows/' substrate/skills/check-substrate-updates/check.sh` → 0 (no workflow-deploy infra leaked in).
- **P18 (out-of-scope cites untouched):** `grep -n 'install\.sh:60-69\|install\.sh:766-770' substrate/skills/check-substrate-updates/check.sh` → unchanged from main (the two pre-existing-drift cites were NOT edited — scope discipline).
- **P19 (diff scope):** `git diff --stat` against the worktree base shows ONLY `substrate/install.sh`, `substrate/skills/check-substrate-updates/check.sh`, the newly-added `substrate/skills/workflow-composer/SKILL.md`, plus any `app/` generated-data file gen-data writes. No other source file changed.

## 5. Threat→mitigation map

**Not threat-ratified (process change, no runtime attack path).** Per `operating-disciplines.md` §35.5, this arc is a skill-promotion + comment-cite-hygiene + deploy-wiring change. It introduces no new credential flow, no PRINCIPAL gate, no runtime-exploitable surface; the skill is guidance markdown and the install/check edits are deploy plumbing. No named threat (ARGUS-surfaced or ratification-origin) attaches to any change here. ARGUS to CONFIRM this classification (I propose; I cannot self-grant the carve-out).

## 6. Self-assessed weak points (feeds ARGUS)

- **WP1 — Line-236 cite shape is the highest-risk build step.** It is the one cite both the directive AND rev1 missed, AND it is the one with a different text shape (`install.sh:140 region`, bare line, not the `140-144` range). The dual trap: ADA could (a) miss line 236 entirely by following the directive's four-line enumeration, or (b) catch it but apply the range form (`198-208 region`) where the bare-line form (`198 region`) is correct. P7 catches (a); P8's explicit "236 reads `198 region`" sub-clause catches (b). *Why this shape anyway:* I made line 236 its own table row with an explicit corrected-text column and a called-out "do not blanket s///" warning precisely because it is the most likely build error; the probes assert the exact post-edit text, not just "no 140 survives."
- **WP2 — Post-edit line numbers in the cite text are a snapshot that the build's own edit invalidates if any OTHER install.sh edit lands first.** The corrected cite `198-208` is only right if §2.2 is the only thing that shifts the SKILL_NAMES region. If ADA were to make an unrelated install.sh edit above line 198 in the same build, 198-208 would itself become stale. *Why this shape anyway:* the arc scope is locked to exactly the SKILL_NAMES append in install.sh, so no other shift is in scope; P1/P2 verify the array's actual post-edit position, so a drift would be caught. But it is structurally a re-stale-able cite (the same class this arc is fixing) — the durable fix (anchor the comment on the literal pattern, not a line range) is explicitly out of scope here and worth a follow-up note.
- **WP3 — The drift probes (P5/P6) and dry-run/real-deploy probes (P3/P4) assume the throwaway-synthetic-target harness behaves identically in a fresh worktree.** I verified the parser anchors and the gen-data glob directly, but I did NOT live-run an actual install into a throwaway target from this worktree (that is VERA's executable job, and §6.5 forbids me from background/build-shaped compute). If the worktree's relative-path assumptions differ from a true fresh clone (e.g. install.sh resolving substrate source paths), P3/P4 could behave differently than rev1 assumed. *Why this shape anyway:* the install/drift mechanics are unchanged by this arc (only the array contents change), so the harness risk is inherited-stable, not arc-introduced; I flag it so VERA runs P3/P4 against a true throwaway clone rather than trusting the worktree as the target.

## 7. Out of scope (one-line reasons)

- `WORKFLOW_NAMES` / `.claude/workflows/` deploy+drift infrastructure — locked decision #2; no battle-tested script to promote; separate later arc.
- The two pre-existing stale check.sh cites (`install.sh:60-69`, `:766-770`) — different drift class, not shifted-wrong by this arc; candidate follow-up ticket.
- `is_substrate_source_present` skills-branch `[ -e ]` existence test — latent rev1 MINOR; candidate follow-up.
- Re-authoring any skill content — locked decision #1; a wrong/missing delta is a build finding to fix in place, not a rewrite.
- Authoring an actual `/gauntlet` or `/defeat-threat` workflow script — downstream arcs (`stoa--h2z` etc.).
