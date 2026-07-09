# design-rev2 — stoa--p0e: authorship deny-gate RETIREMENT + report-only attribution ADVISORY

**Author:** Denson Smith · **Arc:** stoa--p0e · **Seat:** CAPTAIN_DAEDALUS_the_stoa (architect)
**Consumes:** `agents/design/stoa--p0e/DAEDALUS-brief.md` (PLINY, authoritative) + the PRINCIPAL RULING — SCOPE RESHAPE (`stoa--p0e` 2026-07-09T09:07:01Z) + ARGUS cold-critique `agents/verdicts/stoa--p0e/argus-design-rev1.md` (revise / PASS-WITH-RISKS, 0 FAIL-BLOCKING) + FM cross-seam placement note (`stoa--p0e` 2026-07-09T19:31:34Z).
**Cite:** `stoa--dps` (PEP 621 false-positive), `stoa--eby`, Arc 46/65/69 hook history, MAJOR_POLYBIUS §18.1 (post-merge on-main `.claude/` regen), memory `install.sh slug = checkout basename → regen .claude/ on main`.

> **rev2 SUPERSEDES rev1 as the ADA-authoritative artifact.** Build from THIS file; you do not need to cross-read design-rev1.md. rev2 carries the full retirement plan, advisory spec, install.sh delta list, and probe spec, and folds the six ARGUS risks (r1–r6) + the M2 SECONDARY-scoping note. ARGUS confirmed the rev1 SHAPE is sound (advisory-as-skill; skills-enumerated / hooks-not; `_hooklib` safe to leave; P1-fires / P2-silent; disarm-by-deregistration web-verified) and all six M-item classifications — that spine is UNCHANGED here; rev2 amends completeness/accuracy only.

**What changed rev1 → rev2 (the fold, at a glance):**
- **r1** (§2.1 + §2.6 NEW + §10 P3): the-stoa's OWN deployed `.claude/` residuals (deployed candidate template, orphan hook script, stale `principal-identity` comment) are now NAMED with an explicit post-merge on-main cleanup step + per-target mechanism + a P3 split (worktree vs post-merge-assert).
- **r3** (§5): ALL FIVE install.sh author-gate comment sites enumerated (rev1 named 2) + the corrected replacement text for the CONSUMER-SEEDED `principal-identity` block (the line that falsely says "the commit is denied").
- **r2** (§10 + §2.4): the "tests are source-only" claim is CORRECTED — a skill's `tests/` DOES deploy (recursive `cp -R`); decision + justification to SHIP it (not exclude).
- **r4** (§2.4): `substrate/hooks/tests/README.md` added to the edit list (retitle/rewrite to describe only the surviving stop-self-check test).
- **r5** (§7 W2b): PRIMARY name-agnostic false-positive on legit edits captured as a named residual (no mechanism change).
- **r6** (§9): M1 kept precisely scoped to IN-DIFF attribution edits; NOT restated as total plagiarism defeat.
- **M2 note** (§9 + §10): SECONDARY explicitly marked UNRATIFIED best-effort courtesy; its s1/s2 fixtures are functional-only, NOT bound to any M-item threat-anchored probe set.

---

## 1. Problem restatement (pre-work gate, §6.1)

The PRINCIPAL retired all authorship **deny**-gates. This arc must (a) remove the `pretooluse-author-field-audit.sh` deny-hook from the-stoa's own live armed config AND the substrate source/template, archiving (not deleting) the script; (b) build a **report-only, never-blocking, best-effort, diff-scoped** attribution *advisory* whose PRIMARY job is to surface a diff hunk that MODIFIES or DELETES an existing attribution line (the plagiarism/license-breach direction the deny-gate never checked), with a SECONDARY check for NEW non-PRINCIPAL author fields outside vendored paths; (c) propagate both changes (retire the deny-hook, gain the advisory) to consumer workspaces through the existing `install.sh` + `check-substrate-updates` lifecycle, without touching any other repo; (d) preserve the two surviving Bash gates, the Stop/PostToolUse/SessionStart entries, the `CLAUDE.md` authorship doctrine (stays PRIMARY, untouched), the HARD SAFETY CONSTRAINT (deploy inert, arm only via `--enable-hooks` default-OFF, never auto-write a live settings.json), and the no-API-key / no-keyed-CI canon; **and (e) — rev2 addition — the-stoa dogfoods its own substrate, so the-stoa's OWN deployed `.claude/` copies (candidate template, deployed hook script, seeded `principal-identity`) must also be reconciled, via the post-merge on-main `.claude/` deploy-regen (NOT on the build branch), with the one residual the regen cannot auto-fix (the never-clobbered `principal-identity` comment) named explicitly.**

**Imported assumptions I am naming (not smoothing):**
- The brief's "durable report the operator/user-tier reads" is satisfied by a **skill**, not a hook. Rationale in §3. Design choice the brief left open, not a re-scope.
- `python3` is present on substrate targets (same assumption every existing gate makes, `operating-disciplines.md` §13); the advisory FAIL-OPENs to an empty report + exit 0 if absent.
- The `.claude/hooks/principal-identity` allow-list continues to be seeded by `install.sh` (survives retirement — the advisory's SECONDARY check reuses it). Retirement does NOT retire the seed; it only corrects the seed's now-false comment (r3).
- **(rev2) The `.claude/` deploy-regen belongs on MAIN post-merge** because the slug (`NAME_SUFFIX`) derives from the checkout basename — running it in the `stoa--p0e-build` worktree would yield the wrong slug (MAJOR_POLYBIUS §18.1; memory `install.sh slug = checkout basename → regen .claude/ on main`). Confirmed with the FM cross-seam note: the deployed-`.claude/` residual cleanup is a post-merge on-main step the FM executes at the Decider close-gate; ADA does NOT run a `.claude/` regen on the build branch.

Restatement converges with the brief; no divergence to escalate.

---

## 2. Retirement plan (concrete file/line edits — ADA executes)

### 2.1 Remove the deny-hook registration (2 files edited on the BUILD BRANCH)

**(a) Live armed config — `.claude/settings.json` (repo root; git-tracked, carries MAIN absolute paths).** The `PreToolUse` matcher object (`"matcher": "Bash"`, opens ~line 5) holds a `hooks` array of THREE command objects. Delete the FIRST object — the `"if": "Bash(git commit*)"` entry whose `command` ends `pretooluse-author-field-audit.sh` (verified: object bounded by the `{` at **line 8** through its closing `},` at **line 13**; the `command` is at **line 11**). Keep the two remaining objects intact (`"if": "Bash(git *)"` clean-tree at 15–18; `"if": "Bash(bw comment*)"` no-dash-m at 21–24). Do NOT touch `Stop`, `PostToolUse` (Agent matcher), `SessionStart` (compact matcher). Post-edit the `PreToolUse.Bash` matcher's inner `hooks` array has exactly 2 objects.

> This is the safety-critical disarm and it is handled ON THE BUILD BRANCH (git-tracked file, MAIN paths, merges cleanly to main). ARGUS + FM both confirm the live-config disarm is correctly in-scope here. It is a targeted single-object deletion, NOT a `.claude/` regen, so it does not brush the "no regen on the build branch" fence.

**(b) Consumer source-of-truth template — `substrate/templates/settings-hooks.json`.** Delete the identical first command object (the `{{HOOKS_DIR}}/pretooluse-author-field-audit.sh` entry; verified: object at **lines 8–13**, `command` at **line 11**). Keep the other two Bash gates (`pretooluse-clean-tree-before-branch.sh` at 17, `pretooluse-no-dash-m-bw-comment.sh` at 23), plus `Stop` (stop-self-check.sh, 34), `PostToolUse` (posttooluse-agent-checker-trigger.sh, 46), both `SessionStart` matchers (sessionstart-compact-reprime.sh, 58; sessionstart-substrate-check.sh, 68), and the `_comment` header. **Verified: the `_comment` header is generic — it does NOT name the author-field gate specifically (it lists no gate by name), so no `_comment` edit is required** (ARGUS non-finding confirmed). Do NOT disturb the `startup|resume` substrate-check entry the live root settings.json lacks.

### 2.2 Archive the script (do NOT delete)

`git mv substrate/hooks/pretooluse-author-field-audit.sh substrate/v1-historical/hooks/pretooluse-author-field-audit.sh`

- Create `substrate/v1-historical/hooks/` (the `v1-historical/` precedent dir exists with role-file `.md`s + `templates/`; a `hooks/` subpath is the natural extension).
- **Glob-deploy consequence (confirmed):** `install.sh` deploys hooks by `for src in "${SRC_HOOKS_DIR}"/*.sh` with `SRC_HOOKS_DIR="${SCRIPT_DIR}/hooks"`. Moving the script OUT of `substrate/hooks/` removes it from that glob → fresh installs stop deploying it. No `HOOK_NAMES` list to edit (glob-discovered). **Confirmed against install.sh:167–171 (glob rationale) + :1913 (`for s in "${SRC_HOOKS_DIR}"/*.sh`).**

### 2.3 `_hooklib.sh` — STAYS, functions LEFT INTACT (design decision + recommendation)

Leave `substrate/hooks/_hooklib.sh` in place (sourced by the surviving gates + Stop self-check). The author-specific functions `classify_author_file`, `extract_author_fields`, `parse_allow_pairs` became dead once the gate is archived. **ARGUS CONFIRMED (cold-checked):** those three functions are called ONLY by the retired gate (`pretooluse-author-field-audit.sh:154/161/168`) and the archived author-gate test; `stop-self-check.sh` sources `_hooklib.sh` (line 41) but calls only the generic helpers (`read_stdin_event` / `event_field` / `json_field` / `emit_deny` / `allow`), NOT the author functions. **Recommendation: LEAVE the dead functions in `_hooklib.sh`.** Pruning a shared lib for zero runtime benefit risks a subtle break in a surviving gate; a future arc may prune under a proven-zero-caller check. Recorded as W4 (§7).

### 2.4 Test corpus disposition (r2 + r4 folded)

- `git mv substrate/hooks/tests/run-author-gate-tests.sh substrate/v1-historical/hooks/tests/run-author-gate-tests.sh` and move the author-gate fixtures with it: `fixtures/tp/`, `fixtures/fp/`, `fixtures/control/` → `substrate/v1-historical/hooks/tests/fixtures/`.
- **KEEP** `substrate/hooks/tests/run-stop-self-check-tests.sh` + `fixtures/stop-event-orchestrator.json` (they test a SURVIVING hook).
- **(r4 — NEW edit) Rewrite `substrate/hooks/tests/README.md`.** It is currently titled `# Author-gate regression corpus (Arc 65 / stoa--z2b)` and describes the retired author-gate test (the `.md`-narrowing corpus). After the author-gate runner + `tp/fp/control` fixtures move to `v1-historical`, only `run-stop-self-check-tests.sh` + `fixtures/stop-event-orchestrator.json` remain under `substrate/hooks/tests/`. **Retitle + rewrite this README to describe ONLY the surviving stop-self-check test** — its run command (`bash substrate/hooks/tests/run-stop-self-check-tests.sh`), what it guards (the Stop self-check hook), and the same source-only-deploy note that applies to hook tests. The author-gate corpus's WHY-history is preserved via the moved runner in `v1-historical/hooks/tests/` + `RETIREMENT.md` (§2.5) — do NOT lose it, but it no longer belongs in the LIVE `substrate/hooks/tests/README.md`.
  - *(Optional, recommended)* carry a copy of the old author-gate README content to `substrate/v1-historical/hooks/tests/README.md` alongside the moved runner so the archived corpus stays self-documenting.
- The advisory gets its OWN fresh corpus (diff fixtures, §10) under `substrate/skills/attribution-advisory/tests/`. The old author-*file* fixtures are archived rather than repurposed (a couple inform the new negatives).

> **(r2 CORRECTION — read before you reason about the advisory's `tests/`)** The archived author-gate corpus is source-only *because hooks deploy via a NON-recursive `*.sh` glob* (`substrate/hooks/tests/README.md:6–8` states this explicitly). **That posture does NOT carry over to the advisory skill.** A skill deploys via **recursive `cp -R`** (`install.sh:1338` — `cp -R "$src_skill"/. "$dest_skill"/`), so a skill's `tests/` subtree DOES reach every consumer at `<workspace>/.claude/skills/attribution-advisory/tests/`. rev1 §10 wrongly claimed the advisory corpus is "source-only, does not deploy" — that is FALSE for a skill. See §10 for the SHIP-it decision + justification.

### 2.5 Retirement record / WHY-HISTORY (invariant 5, must-settle #6)

Two durable homes:
1. **`substrate/v1-historical/hooks/RETIREMENT.md`** (new) — the canonical record. Documents, as *history explaining why retirement is correct, NOT as fix targets*: (i) `stoa--dps` (PEP 621 inline-table `authors = [{name=...}]` parser false-positive → a 3-day false-positive hold); (ii) the Bash-only matcher hole (PowerShell commits ungated); (iii) the compound `cd && git commit` matcher dodge (prefix-anchored `if` matcher); plus the empirical that arc-77 doctrine audits verified authorship correct 4× independently while the deny-hook contributed only a false-positive hold + a discovered coverage hole. Cite `stoa--dps`, `stoa--eby`.
2. **`substrate/hooks/README.md`** — update §4 table (remove the `pretooluse-author-field-audit.sh` row at **line 85**), fix the prose references that name the gate as a denier: **line 47** (author-field deny bullet), **line 98** ("The PRINCIPAL allow-list the author-field gate reads is `.claude/hooks/principal-identity`" → the advisory skill reads it), **line 139** ("author-field gate denies any value not on the list" → the advisory REPORTS, never denies), and **§7 (line 215, the `.md`-narrowing narrative)** — annotate §7 as *historical to the retired gate* (the narrowing lore is preserved via the archived script; the surviving lib functions are dead). Add a short "Retired gates (Arc — stoa--p0e)" note pointing to `v1-historical/hooks/RETIREMENT.md` + naming the new advisory skill. Do NOT delete §7 — it is the durable record of the z2b narrowing.
3. ADA does the bw write dispositioning `stoa--dps` as **superseded-by-retirement** (noted here per invariant 5; DAEDALUS does not write bw tickets closed).

### 2.6 (rev2 NEW — r1) the-stoa's OWN deployed `.claude/` residuals — NAMED, post-merge on-main cleanup

the-stoa dogfoods its own substrate, so beyond the substrate SOURCE edits (§2.1b–§2.5) and the live `.claude/settings.json` disarm (§2.1a), the-stoa's OWN **deployed** `.claude/` copies still carry the retired gate. **All three are git-tracked** (verified: `git ls-files` returns all three). They are reconciled at the **post-merge on-main `.claude/` deploy-regen** — the FM executes this at the Decider close-gate (FM cross-seam note 2026-07-09T19:31:34Z); **ADA does NOT run a `.claude/` regen on the build branch** (slug derives from the checkout basename → must run on main; running it in the worktree yields the wrong slug and pollutes the branch with deploy output that belongs on main). This section NAMES the targets + per-target mechanism so the close-gate executes the right action for each — critically, one of them is NOT auto-fixed by a plain regen.

| Deployed residual (the-stoa's own `.claude/`) | Still carries | Cleanup mechanism at the post-merge on-main regen |
|---|---|---|
| `.claude/templates/settings-hooks.json` (verified: registration at **line 11**) | the `{{HOOKS_DIR}}/pretooluse-author-field-audit.sh` candidate registration | **AUTO.** Templates deploy verbatim via `cp`; the post-merge regen overwrites this file with the edited substrate template (§2.1b) → registration gone. No manual step. |
| `.claude/hooks/pretooluse-author-field-audit.sh` (deployed orphan script) | the deployed copy of the archived script | **`--prune-obsolete` (recommended).** After §2.2 archival, the hooks-staleness scan (`install.sh:1912–1925`) builds `_src_hook_set` from `substrate/hooks/*.sh` and flags any deployed hook NOT in the set as obsolete; it WARNS by default and DELETES (`rm -rf`) only under `--prune-obsolete` (`install.sh:1928+`). **Recommendation: run the post-merge regen WITH `--prune-obsolete`** to delete the orphan cleanly — the-stoa project tier is a controlled dogfood surface, so the cross-substrate false-positive caveat the warning guards against (a user-tier concern) does not apply. **If `--prune-obsolete` is withheld, the orphan is INERT and harmless:** the registration is gone from both the refreshed candidate template and the live settings.json, and ARGUS web-verified that an unregistered loose script in `.claude/hooks/` is never auto-executed. Inert-orphan is an ACCEPTABLE end-state; deletion is the tidy end-state. |
| `.claude/hooks/principal-identity` (verified: stale comment at **lines 3–5**) | a comment reading "The `pretooluse-author-field-audit.sh` gate compares … the commit is denied" — FALSE after retirement | **NOT auto-fixed by a plain regen — REQUIRES A DISTINCT MANUAL COMMENT EDIT.** `install.sh` NEVER clobbers an existing `principal-identity` (`install.sh:1479–1481`: `if [ -f "$PRINCIPAL_ID_FILE" ]; then log "already exists (not clobbered)"`), and the hooks-staleness scan explicitly CARVES IT OUT (`install.sh:1919`: `principal-identity) continue`). So the regen leaves this file's stale comment UNTOUCHED. The close-gate must apply a targeted comment edit replacing lines 3–5 with the SAME corrected advisory text as the r3 install.sh seed-block fix (§5, the corrected echo block). The allow-list VALUES below the comment (`denson` / email / `Denson Smith`) are unchanged — the advisory's SECONDARY check still reads them. The file is slug-independent + name-only (no absolute paths, no `NAME_SUFFIX`), so the edit is safe on main. |

> **NOTE TO CLOSE-GATE (FM):** the third row is the load-bearing r1 catch. A close-gate that runs only `install.sh --prune-obsolete` and assumes "the regen cleaned everything" will SILENTLY LEAVE the deployed `principal-identity` comment stating that commits are denied. It must be edited by hand. rev2 keeps this on the post-merge on-main step per your cross-seam placement (you reserved the deployed-`.claude/` cleanup for post-merge); I am only surfacing that a plain regen is insufficient for this one file so the manual edit is not skipped. (If you prefer, this single tracked-file comment edit is slug-independent and could equivalently be made on the build branch by ADA and verified by VERA pre-merge — it is not regen output and does not brush the regen fence — but I default to your post-merge placement.)

---

## 3. Advisory mechanism + surface (must-settle #1) — a report-only SKILL

**Decision: the advisory is a new skill `attribution-advisory` at `substrate/skills/attribution-advisory/`, deploying to `<workspace>/.claude/skills/attribution-advisory/`.** It is a deterministic, operator-invoked, report-only reporter — NOT a hook.

**Why a skill (chosen over the three candidate shapes in the brief):**

| Candidate | Why rejected / chosen |
|---|---|
| Non-blocking PreToolUse/Stop **hook** | Rejected. (1) Needs `--enable-hooks` arming → inherits the whole HARD-SAFETY / armed-consumer complexity for a thing that only *reports*. (2) Hooks are OUTSIDE `check-substrate-updates` enumeration (check.sh has zero `hook` awareness — ARGUS-confirmed) → a new hook would NOT be surfaced MISSING to consumers, breaking must-settle #5. (3) The report-carrying `additionalContext` channel is upstream-broken (README §6, issues #55889/#18427/#15174) → an unreliable surface. |
| Standalone loose operator script (under `substrate/hooks/` or a bare `substrate/tools/`) | Rejected as primary home. A bare `.sh` under `substrate/hooks/` deploys via the glob but (a) pollutes the "harness-owned hook scripts" dir and (b) is NOT enumerated by `check-substrate-updates`. A new `substrate/tools/` deploy class needs new install.sh + check.sh enumeration work (more scope, same end state as a skill). |
| **Skill** (CHOSEN) | Skills ARE enumerated by `check-substrate-updates` (`SKILL_NAMES` → `parse_skill_names_from_install` → MISSING detection; ARGUS-confirmed against check.sh:459–472). Skills need NO `--enable-hooks` arming. Skills are the substrate's established operator-invocable tool home (`whoami`, `inspect-script-output`, `gauntlet-setup` are precedent). One `SKILL_NAMES` delta rides the entire propagation + invocation + report lifecycle. It CANNOT ever deny (never on any PreToolUse path) — the report-only property is structural, not merely coded. |

**Shape:**
- Entry script `substrate/skills/attribution-advisory/advise.sh` (POSIX `sh` wrapper + a self-contained `python3` diff scanner; mirrors the gate scripts' `set -uo pipefail` + FAIL-OPEN style).
- `SKILL.md` (frontmatter `author: Denson Smith`) documenting invocation + the report path + the never-blocks contract.
- `tests/` corpus (§10) — **which DOES deploy to consumers; see §10 SHIP decision.**

**Invocation (operator or gauntlet seat):**
```
bash .claude/skills/attribution-advisory/advise.sh            # default: scan `git diff --cached` (staged)
bash .claude/skills/attribution-advisory/advise.sh --range <BASE>..<HEAD>
bash .claude/skills/attribution-advisory/advise.sh --diff-file <path.diff>
git diff <range> | bash .claude/skills/attribution-advisory/advise.sh --stdin
```

**Report surface (durable, single known path):** `<workspace>/.claude/attribution-advisory-report.md`, overwritten per run. Also echoes a one-line summary to stdout (`attribution-advisory: N finding(s) — see .claude/attribution-advisory-report.md` or `... 0 findings (clean)`). The report honors README §2 authoring rule — **each finding states, inline, WHY it fired + WHAT to check**:

```
# Attribution advisory report
scanned: <range/source> · at: <UTC ts> · findings: <N>
(This is a REPORT, not a block. Nothing was prevented. Review each finding below.)

## PRIMARY — an existing attribution line was MODIFIED or DELETED
- file: LICENSE  (hunk @@ -1 +1)
  removed: `Copyright (c) 2024 Jane Doe`
  WHY: modifying/deleting a line that already carried an author/copyright/license
       attribution is almost never legitimate — it is the plagiarism / license-breach
       direction (another author's credit erased or replaced).
  WHAT TO CHECK: confirm this change is legitimate (e.g. correcting YOUR OWN name, a
       routine copyright-year bump, or a license reformat); otherwise restore the
       original attribution before committing.

## SECONDARY — a NEW non-PRINCIPAL author-like field (outside vendored paths)
- file: src/foo.py  (added)
  field: author = "Mallory Example"
  WHY: a new author/owner/creator/... field naming someone who is not the PRINCIPAL,
       in a non-vendored path, may be a mis-attribution of the PRINCIPAL's own work.
  WHAT TO CHECK: if this is a CITED source author, move it to prose/citation; if it is
       a legitimate PRINCIPAL identity, add it to .claude/hooks/principal-identity.
```

*(rev2: the PRIMARY "WHAT TO CHECK" line now explicitly names year-bumps + license reformats as legitimate cases, per r5 — the report text is where the name-agnostic false-positive is dispositioned for the reader.)*

**Where the operator sees it:** (1) directly — an operator/gauntlet seat runs `advise.sh` and reads the stdout summary + the report file; (2) the report file is the durable artifact the user-tier reads on demand. **Follow-up (out of scope this arc):** wiring `advise.sh` as an automatic step in the gauntlet close-gate (CATO/NOMOS) would touch those role files — deferred to a named follow-up (§8), not built here.

**Report-only / never-deny — structural guarantees (P4):** `advise.sh` (a) is never registered in any settings-hooks.json (it is a skill, not a gate); (b) ALWAYS `exit 0` — contains no reachable `exit 1` / `exit 2` and no `permissionDecision` emission; (c) even if a future operator mis-registered it as a PreToolUse hook, an exit-0 script that emits no deny JSON is treated as ALLOW → it can never block by construction.

---

## 4. Diff-scoping (must-settle #2) — regex/term set + hunk classification

The scanner parses a **unified diff** line-by-line, tracking the current `+++ b/<path>` and hunk headers.

### 4.1 Attribution term set (the "attribution line" definition)

Field words (case-insensitive), matched as a whole word followed by a `:` or `=` separator — the `_hooklib.sh extract_author_fields` set, MIRRORED here with a cite (see W3 for the SSoT tension):
`author, authors, owner, creator, created_by, maintainer, maintainers, by, copyright, holder, vendor, publisher` — plus attribution-specific forms the diff surface adds: `license`, `licensed`, `attribution`, `SPDX-License-Identifier`, `@author`, `@copyright`.
Plus two separator-less forms (from `_hooklib` y12 lore):
- Copyright form: `Copyright [(c)|(C)|©] <YEAR|YEAR-range> <CapitalizedName>` (name run anchored to EOL; a 4-digit year required — keeps prose out).
- `SPDX-License-Identifier: <id>`.

### 4.2 PRIMARY classification — modify/delete of an existing attribution (name-agnostic)

- Fires when a **removed** line (`-` prefix, excluding the `---` file header) matches any attribution pattern in 4.1.
- A MODIFY appears as `-<old attribution>` + `+<new>`; the `-` line fires. A pure DELETE appears as `-<attribution>` with no paired `+`; the `-` line fires. Both are caught by "any `-` line matching an attribution pattern."
- **Name-agnostic on purpose** — the brief's rationale: changing a line that already carried a name is almost never legitimate → naturally tiny false-positive rate. PRIMARY does NOT consult the principal-identity list.
- **Never fires on a pure addition:** a `+` attribution line with no matched `-` attribution in the diff is a NEW attribution (SECONDARY's domain, not PRIMARY). A **new file** (old side `/dev/null`, hunk `@@ -0,0`) produces zero `-` content lines → never PRIMARY. This is exactly the P2 silence.
- **(r5 — named residual, no mechanism change):** because PRIMARY is name-agnostic, it DOES fire on routine LEGITIMATE attribution edits — a copyright-year bump (`-Copyright (c) 2024 Denson Smith` / `+... 2025 ...`), a license reformat, or a PRINCIPAL self-name correction. This is EXPECTED and ACCEPTABLE under report-only: the finding is a note to review, the report's "WHAT TO CHECK" line explicitly names these legit cases (§3), and `CLAUDE.md` doctrine stays PRIMARY. The "naturally tiny false-positive rate" claim is honest for the *plagiarism* frame (most attribution-line edits ARE worth a human glance) but is NOT a claim of zero false positives. Captured as W2b (§7).

### 4.3 SECONDARY classification — NEW non-PRINCIPAL author field outside vendored paths

- Fires when an **added** line (`+` prefix, excluding the `+++` header) introduces an author-like **field assignment** whose extracted VALUE is a person-name NOT on the principal-identity allow-list, AND the target path is NOT vendored/imported.
- **Value extraction:** self-contained port of the `extract_author_fields` field-anchored logic (unquote + trim; skip template placeholders `{{..}}`/`<..>`/`$..`; flatten inline arrays) run over the added-line text only.
- **"Non-PRINCIPAL":** value (lower-cased, trimmed) not equal to any token in `<workspace>/.claude/hooks/principal-identity` (the same allow-list the retired gate read — still deployed + still seeded, see §5). **FAIL-OPEN:** if the list is absent/empty, SECONDARY is skipped entirely (PRIMARY still runs, name-agnostic). This is the SAFE direction for a report-only tool — an unconfigured allow-list yields no noisy false SECONDARY findings.
- **Vendored/imported path exclusion (static, deterministic):** the added file's path contains any of `node_modules/`, `vendor/`, `third_party/`, `third-party/`, `thirdparty/`, `dist/`, `build/`, `.venv/`, `venv/`, `site-packages/`, `external/`, `deps/`, `.git/`, `v1-historical/`. Static list is the deterministic floor; a `.gitattributes` `linguist-vendored` refinement is a possible later enhancement (W5).
- **(M2 note — status of SECONDARY):** SECONDARY covers direction-1 (a NEW non-PRINCIPAL author field), which the SCOPE RESHAPE ruling DE-RATIFIED as a runtime-gated threat (M2 = not-threat-ratified). SECONDARY therefore ships as **UNRATIFIED best-effort courtesy** — a functional convenience that surfaces direction-1, NOT a threat-ratified mitigation. It is NOT bound to any M-item threat-anchored probe set; its fixtures (s1/s2, §10) are functional-only (they prove SECONDARY *works*, not that a *named threat* is defeated). See §9.

### 4.4 Structural limits (accepted, best-effort)
- Line-anchored: a multi-line/wrapped attribution edit, or an attribution smuggled past the field-anchored regex, can be missed (false-negative). Report-only + doctrine-primary → acceptable per nothing-has-to-be-100% (W2).
- A pure `git mv` rename with no content change shows no attribution content lines → correctly silent.
- **(r6) The classic plagiarism vector — copying external OSS into a NEW file with the upstream header STRIPPED — produces no `-` attribution line (nothing removed *in this diff*) and no `+` non-PRINCIPAL field (the header is gone, not added), so BOTH PRIMARY and SECONDARY stay silent (structural false-negative).** This is inherent to diff-scoping: the scanner cannot see content that is not in the diff. M1 is scoped to IN-DIFF attribution edits precisely so it does not overclaim this vector (§9).

---

## 5. install.sh deltas (must-settle #4) — r3 folded (ALL sites enumerated)

**Behavioral / manifest deltas:**
1. **`SKILL_NAMES` array (install.sh ~line 228, the `handoff-author` region confirms the array location)** — add `attribution-advisory`. This ONE line (a) deploys the skill to `<dest>/.claude/skills/attribution-advisory/` and (b) makes `check-substrate-updates` enumerate it as source (→ MISSING on consumers → gained on apply). No other deploy plumbing needed (the skill-deploy loop at `install.sh:1338` iterates `SKILL_NAMES` and `cp -R`s each).
2. **Hook glob-deploy** — NO code change. Archiving the script out of `substrate/hooks/` (§2.2) auto-removes it from the `*.sh` glob (`install.sh:1913`). Fresh installs deploy the 2 surviving gates + `_hooklib.sh` + README + the surviving Stop/PostToolUse/SessionStart scripts, minus the retired gate.
3. **principal-identity seed (step 5c, ~1471–1503)** — **KEEP the seeding** (the advisory SECONDARY reuses it). NO behavioral change; correct ONLY the comment prose (see the r3 comment-site enumeration below).
4. **`--enable-hooks` arming (step 5d)** — NO change. It still arms the 2 surviving gates. The advisory needs no arming. HARD SAFETY CONSTRAINT preserved verbatim.

**(r3) Author-gate comment sites — ALL FIVE to correct (rev1 named only two; verified by grep this arc):**

| Site (verified line) | Current text (references the retired gate) | Corrective action |
|---|---|---|
| **:85–86** (header note) | "The author-field gate reads a PRINCIPAL-identity allow-list seeded at `.claude/hooks/principal-identity`." | Reword: "The **attribution-advisory skill's SECONDARY check** reads a PRINCIPAL-identity allow-list seeded at `.claude/hooks/principal-identity`." |
| **:689–693** (`--principal-name` flag comment) | "Seeded into the **author-field gate's allow-list so the gate** recognizes the PRINCIPAL's own authored artifacts and does not false-block." | Reword: "Seeded into the **attribution-advisory allow-list so the advisory's SECONDARY check** recognizes the PRINCIPAL's own authored artifacts and does not false-**report**." |
| **:1471–1478** (seed-write leading comment) | "Write the PRINCIPAL-identity allow-list **the author-field gate reads** … It is the **gate's** CONFIG …" | Reword: "… the allow-list **the attribution-advisory skill reads** … It is the **skill's** CONFIG …" (keep the never-clobber + fail-open prose). |
| **:1488–1497** (the SEEDED `echo` block — DEPLOYED VERBATIM into every consumer `.claude/hooks/principal-identity`) | line 1490 names `pretooluse-author-field-audit.sh`; **line 1492 states "the commit is denied"** — FALSE after retirement (the advisory never denies). | Replace with the corrected echo block below (describes the advisory's SECONDARY check + report-only, NO deny). This is the CONSUMER-FACING falsehood — highest-priority of the five. |
| **:1906–1907** (hooks-staleness carve-out comment) | "`principal-identity` : operator-curated allow-list (**the gate's config**)" | Reword the parenthetical: "(the **attribution-advisory skill's SECONDARY-check config**)". No code change to the carve-out itself — `principal-identity) continue` STAYS (still correctly carved out). |

**Corrected replacement for the seeded `echo` block (install.sh:1488–1497):**
```sh
      echo "# Stoa attribution-advisory — PRINCIPAL identity allow-list."
      echo "# One accepted name or email per line ('#' comments + blanks ignored)."
      echo "# The attribution-advisory skill's SECONDARY check compares NEW author-like"
      echo "# field VALUES (added in a diff, outside vendored paths) against this list;"
      echo "# a value not on the list is REPORTED for review in the advisory report."
      echo "# It is NEVER blocked or denied — the advisory is report-only. This is the"
      echo "# SKILL'S CONFIG, not an author field of any repo artifact. Widen it when a"
      echo "# legit PRINCIPAL identity is missing. An ABSENT or EMPTY list SKIPS the"
      echo "# SECONDARY check (PRIMARY still runs, name-agnostic). Seeded from the"
      echo "# target's global git identity + any --principal-name passed at install."
```
*(This same corrected text is the target text for the-stoa's OWN deployed `.claude/hooks/principal-identity` comment edit at the post-merge close-gate — §2.6 row 3.)*

---

## 6. check-substrate-updates interaction (must-settle #5) — the honest finding

`check.sh` enumerates DRIFTED / MISSING / OBSOLETE over MAJORs, CAPTAINs, **templates**, and **skills** — ARGUS-confirmed. Skills are enumerated by a **recursive `find "${SUBSTRATE_DIR}/skills/${sn}" -type f`** (check.sh:466–472). **It has ZERO hook awareness** (0 `hook` matches in check.sh). Consequence, per surface:

| Change | Enumerated? | Propagation verdict |
|---|---|---|
| **Advisory skill gained** (`attribution-advisory` in SKILL_NAMES) | YES (skills, recursively) | source-present, consumer-absent → **MISSING** → `apply.sh` gains it (whole subtree incl. `tests/`). **WORKS.** |
| **Registration retired** (`settings-hooks.json` template loses the author-field entry) | YES (templates glob) | consumer's deployed candidate template differs from new source → **DRIFTED** → `apply.sh` harvests DRIFTED → the consumer's *candidate* template loses the registration. **WORKS.** |
| **Retired SCRIPT file** at consumer `.claude/hooks/pretooluse-author-field-audit.sh` | **NO** (hooks unenumerated) | NOT flagged OBSOLETE by check.sh, NOT auto-removed. Becomes an **inert orphan**: with the registration gone from the candidate template, the script has no registration → **never fires**. Harmless but untidy. (Consumer `install.sh --prune-obsolete` removes it; see runbook.) |
| **ARMED consumer's LIVE `.claude/settings.json`** (still carries the registration + script on disk) | NO (settings.json is operator-owned; never auto-written — HARD SAFETY) | NOT touched by check.sh or install.sh. The template DRIFT is the operator's SIGNAL to manually remove the dead registration from their live settings.json. Documented in the README runbook. Inherent to the HARD SAFETY CONSTRAINT. |

**Net:** the two things that MUST propagate (gain the advisory; retire the *candidate* registration) DO propagate through enumerated surfaces (skills + templates). The two residuals (an inert orphan script; an armed consumer's live settings.json) are (a) harmless-when-registration-gone and (b) governed by the never-auto-write-a-live-settings.json HARD SAFETY invariant. The README retirement runbook (§2.5) instructs armed consumers to remove the dead registration + optionally `--prune-obsolete` the orphan script. A future arc could add hook enumeration to `check.sh` (named follow-up §8). This is my top weak point (§7 W1).

> **(r2 corollary — the advisory `tests/` and check.sh):** because the deployed skill subtree INCLUDES `tests/` (recursive `cp -R`) AND check.sh enumerates the source skill subtree recursively (`find -type f`), deployed == source for the whole skill including `tests/` → **no drift**. This is exactly why SHIPPING the `tests/` (rather than excluding it) is the mechanism-consistent choice — see §10.

---

## 7. Self-assessed weak points (§6.2)

- **W1 (top) — the orphan-script + armed-live-settings residual is process-mitigated, not mechanically mitigated.** `check-substrate-updates` cannot flag the retired hook OBSOLETE (hooks unenumerated) and cannot touch a live settings.json (HARD SAFETY). An armed consumer who never reads the template-DRIFT signal or the README runbook keeps a dead registration pointing at a still-present script. *Why this shape anyway:* auto-writing a live settings.json to disarm it would violate the HARD SAFETY CONSTRAINT (invariant 8); the honest mechanism is the enumerated template DRIFT as a signal + a README runbook + a named follow-up to teach check.sh hook-awareness. ARGUS CONFIRMED this is persistence-of-old-control, not a NEW attack path (M3/M4 not-threat-ratified).
- **W2 — advisory false-negatives (best-effort line-anchored diff scan).** Obfuscated, multi-line, non-field-shaped, or **external-copy-header-stripped** (r6) attribution edits slip past. *Why anyway:* report-only + `CLAUDE.md` doctrine stays PRIMARY + the nothing-has-to-be-100% ruling. A "100%" claim would be marketing BS.
- **W2b — (r5) advisory false-POSITIVES on legit attribution edits.** PRIMARY is name-agnostic, so a copyright-year bump / license reformat / PRINCIPAL self-name correction fires a PRIMARY finding. *Why anyway:* report-only makes a false PRIMARY a note-to-review, not a block; the report "WHAT TO CHECK" text names these legit cases explicitly; the alternative (name-aware PRIMARY) would reintroduce the allow-list-pressure the SCOPE RESHAPE ruling retired. Accepted; ARGUS confirms (r5, not a blocker).
- **W3 — the attribution term set is MIRRORED in two places** (`_hooklib.sh extract_author_fields` + the advisory scanner). SSoT tension (§6.10). *Why anyway:* the advisory operates on a diff (not a file blob) and is decoupled from the hooks dir (so the skill does not depend on `.claude/hooks/` being deployed/armed). Mitigation: cite the source list in the scanner + a follow-up to extract the field list to a shared data file if it drifts.
- **W4 — dead functions left in `_hooklib.sh`.** *Why anyway:* pruning a shared lib for zero runtime benefit risks a subtle break; the brief recommends leaving them; ARGUS confirmed no surviving caller.
- **W5 — vendored-path exclusion is a static list.** *Why anyway:* report-only (a false SECONDARY is a note, not a block), deterministic, easily widened; a `.gitattributes` refinement is a later enhancement.
- **W6 — report path collision / staleness.** A single overwritten `.claude/attribution-advisory-report.md` means last-run-wins. *Why anyway:* a single known path is the simplest durable surface; the header stamps scanned-range + UTC so staleness is self-evident. Timestamped reports are a trivial later change.
- **W7 — (rev2/r1) the deployed `principal-identity` comment cleanup relies on a manual close-gate edit that a plain regen does NOT perform.** *Why anyway:* `install.sh` never-clobbers an existing `principal-identity` (correct — it protects operator-curated lists); the honest consequence is that the one-time stale-comment fix must be a deliberate edit, which §2.6 NAMES + flags to the close-gate rather than smoothing under "the regen handles it."

No empty-list defense needed — seven named weak points.

---

## 8. Out of scope (this design deliberately does not address)

- Wiring `advise.sh` into the gauntlet close-gate (CATO/NOMOS) as an automatic review step — touches those role files; named FOLLOW-UP.
- Teaching `check-substrate-updates`/`check.sh` hook-awareness (to auto-flag the orphan script OBSOLETE) — separate tooling arc; named FOLLOW-UP.
- Extracting the attribution term set to a shared data file (SSoT) — only if W3 drift is observed; named FOLLOW-UP.
- Pruning the dead `_hooklib.sh` functions — future arc under a zero-caller proof.
- Any edit to `CLAUDE.md` §4 authorship doctrine (stays PRIMARY, untouched — invariant 6).
- Any keyed-CI / API-key / Sonnet-adjudication path (dropped — invariant 7).
- Touching other consumer repos (propagation is via the lifecycle only — invariant 4).
- **(rev2) Running the post-merge on-main `.claude/` deploy-regen itself** — that is the FM's close-gate execution step (§2.6); rev2 NAMES + specifies it, ADA does not run it on the build branch.

---

## 9. Threat→mitigation map (A3 author duty, §6.12) + threat-anchored probe (§6.13)

**M1 (named threat — PRINCIPAL-ratified in the SCOPE RESHAPE ruling as "the real harm … other authors' names getting REPLACED WITH the PRINCIPAL's in quoted material / imported OSS")** — PROPOSE **threat-ratified (detection-mitigation)** *(ARGUS CONFIRMED, unchanged from rev1)*:

> `M1 (plagiarism / license-breach direction) → attack-path: a commit diff MODIFIES or DELETES an existing author/copyright/license/attribution line (replacing another author's credit with the PRINCIPAL's, or erasing an upstream attribution) → how-defeated (report-only DETECTION): the advisory's PRIMARY hunk-classifier flags every removed/changed attribution line in the durable report .claude/attribution-advisory-report.md for operator/user-tier review. defeats_via_probe: P1 (attack-detected) + P2 (legit-unaffected).`

The advisory is report-only, so the mitigation is **detection/surfacing**, not prevention; the threat-anchored probes assert detection fires on the attack path AND stays silent on legitimate traffic.

**(r6) M1 SCOPE BOUNDARY — do NOT overclaim.** M1 covers ONLY the sub-case where the original attribution appears as a **removed `-`-prefixed line WITHIN the diff**. The external-OSS-copied-into-a-new-file-with-header-stripped vector produces NO `-` attribution line and NO `+` non-PRINCIPAL field, so both PRIMARY and SECONDARY stay silent — a structural false-negative inherent to diff-scoping (§4.4). M1's wording ("MODIFIES or DELETES an existing line") is correctly scoped and carries NO overclaim; M1 must NOT be restated as total-plagiarism-defeat (PLINY's A1 beat handles this framing).

**Other candidate M-items (for PLINY's A1 restatement beat — ARGUS CONFIRMED all classifications):**
- **M2 — `not threat-ratified (scope reshape, no new runtime attack path)`:** retiring the deny-gate could let direction-1 regressions (an agent writes a non-PRINCIPAL name into its OWN new artifact) return. Residual covered by `CLAUDE.md` doctrine (PRIMARY, untouched) + the advisory SECONDARY detection. **(M2 note) SECONDARY is UNRATIFIED best-effort courtesy** — it touches the direction-1 surface but is NOT bound to any M-item threat-anchored probe set; its s1/s2 fixtures (§10) are functional-only (prove SECONDARY works), carrying NO `defeats_via_probe` binding. This removes the mapless-mitigation ambiguity ARGUS flagged: SECONDARY is explicitly a convenience, not a threat mitigation.
- **M3 — `not threat-ratified (process/propagation gap, no runtime attack path)`:** an ARMED consumer's live settings.json keeps the dead registration (HARD SAFETY: never auto-written). Mitigation: template-DRIFT signal + README runbook.
- **M4 — `not threat-ratified (process/propagation gap)`:** `check-substrate-updates` does not enumerate hooks → the retired script orphan is not auto-flagged/removed. Mitigation: inert-without-registration (harmless) + README + follow-up.
- **M5 — `not threat-ratified (best-effort report-only residual)`:** advisory false-negative/false-positive (incl. r5 legit-edit false-positives + r6 external-copy false-negative). Acceptable per nothing-has-to-be-100%; doctrine stays primary.
- **The retirement itself — `not threat-ratified (PRINCIPAL-ruled scope reshape; removes a control the PRINCIPAL judged net-negative; residual covered by doctrine + advisory; direction-2/plagiarism coverage NET INCREASES via the advisory PRIMARY)`.** ARGUS CONFIRMED the §35.5 carve-out (a genuine ARGUS confirmation, not a PLINY self-grant).
- **(rev2) The r1 residual cleanup — `not threat-ratified (process change, no runtime attack path)`:** reconciling the-stoa's own deployed `.claude/` copies is dogfood hygiene; no runtime attack path. ARGUS confirms.

---

## 10. Probe specification (§4 acceptance bar — VERA executes)

Fixtures under `substrate/skills/attribution-advisory/tests/fixtures/` (unified-diff `.diff` files). Runner `substrate/skills/attribution-advisory/tests/run-attribution-advisory-tests.sh`. All commands run from the worktree root; the advisory is exercised as the REAL `advise.sh` (no reimplementation).

> **(r2 — corpus deploy posture, CORRECTED + DECIDED)** Unlike hook tests (source-only via a non-recursive `*.sh` glob), a **skill's `tests/` subtree DEPLOYS to consumers** via `install.sh:1338`'s recursive `cp -R`. **DECISION: SHIP the `tests/` corpus (do NOT exclude it from deploy).** Justification: (1) **mechanism-consistency** — check.sh enumerates the source skill subtree recursively (`find -type f`, check.sh:466–472) and flags source-present/deployed-absent as MISSING; excluding `tests/` from deploy while keeping it in source would create a PERMANENT phantom-MISSING drift signal on every consumer's `check-substrate-updates`, unless check.sh AND apply.sh both also learned a `tests/`-exclusion — a cross-cutting tooling change (out of scope, fragile). Shipping keeps deployed == source → zero drift (ARGUS non-finding). (2) **harmless payload** — the fixtures are inert unified-diff `.diff` text + a runner script consumers never auto-invoke (no hook registration, no gauntlet wiring this arc); zero runtime effect. (3) **latent benefit** — a consumer CAN run `run-attribution-advisory-tests.sh` as a self-check of their deployed `advise.sh`. VERA still EXECUTES the probes from SOURCE in the worktree (that is where build+verify happen); the fixtures merely ALSO ride to consumers. rev1 §10's "source-only, does not deploy" claim is RETRACTED.

### P1 — MUST FLAG (threat-anchored, attack-detected half of M1). Probe-id **P1**.
Fixture `p1-edit-copyright.diff`:
```
--- a/LICENSE
+++ b/LICENSE
@@ -1 +1 @@
-Copyright (c) 2024 Jane Doe
+Copyright (c) 2024 Denson Smith
```
Run: `bash substrate/skills/attribution-advisory/advise.sh --diff-file <p1> --report-out <tmp>`
Assert: (a) exit 0; (b) `<tmp>` contains a **PRIMARY** finding naming `LICENSE` and the removed line `Copyright (c) 2024 Jane Doe`; (c) findings count ≥ 1. *This is the executed probe the verdict's `defeats_via_probe:` cites for M1.*

### P2 — MUST NOT FLAG (threat-anchored, legit-unaffected half of M1). Probe-id **P2**.
Fixture `p2-newfile-principal.diff`:
```
--- /dev/null
+++ b/pyproject.toml
@@ -0,0 +1,2 @@
+[project]
+authors = ["Denson Smith"]
```
(Requires a `principal-identity` list containing `Denson Smith` in the test env.)
Run: same invocation on `<p2>`.
Assert: (a) exit 0; (b) `<tmp>` reports **0 findings** — no PRIMARY (no removed attribution line; new file) AND no SECONDARY (value is on the allow-list).

### P3 — deny-hook provably retired (SPLIT: worktree half + post-merge half — r1).

**P3a — worktree / build-branch (VERA executes pre-merge; asserts the substrate SOURCE + the-stoa LIVE settings.json ADA edits on the branch):**
- `grep -c pretooluse-author-field-audit .claude/settings.json` → `0`
- `grep -c pretooluse-author-field-audit substrate/templates/settings-hooks.json` → `0`
- Both SURVIVING Bash gates still registered in each of those two files: `pretooluse-clean-tree-before-branch.sh` AND `pretooluse-no-dash-m-bw-comment.sh` present; and `stop-self-check.sh` (Stop), `posttooluse-agent-checker-trigger.sh` (PostToolUse), `sessionstart-compact-reprime.sh` + `sessionstart-substrate-check.sh` (SessionStart; the latter template-only) entries intact.
- `test ! -e substrate/hooks/pretooluse-author-field-audit.sh` (removed from source)
- `test -e substrate/v1-historical/hooks/pretooluse-author-field-audit.sh` (archived)
- `substrate/hooks/_hooklib.sh` still present.
- **(r3)** `grep -c 'the commit is denied' substrate/install.sh` → `0` (the false seed line corrected); AND `grep -n 'author-field gate\|author-field audit\|pretooluse-author-field-audit' substrate/install.sh` returns NO line that describes it as an *active denier* (the five sites §5 reworded to name the advisory). *(A residual mention inside a HISTORY/retirement context is acceptable; an active-tense "the gate denies" is not.)*
- **(r4)** `substrate/hooks/tests/README.md` no longer titled "Author-gate regression corpus" and no longer references `run-author-gate-tests.sh`; it describes `run-stop-self-check-tests.sh`. `test -e substrate/v1-historical/hooks/tests/run-author-gate-tests.sh` (archived).

**P3b — POST-MERGE on-main (the FM runs after the `.claude/` regen at the Decider close-gate; documented here as regen-handled, NOT a VERA worktree assertion — r1):**
- After the on-main `install.sh` regen: `grep -c pretooluse-author-field-audit .claude/templates/settings-hooks.json` → `0` (deployed candidate template refreshed by `cp`).
- After `install.sh --prune-obsolete`: `test ! -e .claude/hooks/pretooluse-author-field-audit.sh` (orphan deleted) — OR, if `--prune-obsolete` withheld, the orphan is present-but-INERT (accepted end-state; the disarm rests on the registration being gone, not on the file's absence).
- After the manual comment edit (§2.6 row 3): `grep -c 'the commit is denied' .claude/hooks/principal-identity` → `0` AND `grep -c pretooluse-author-field-audit .claude/hooks/principal-identity` → `0` (allow-list VALUES `denson` / email / `Denson Smith` unchanged). **This one is NOT satisfied by the regen alone — it needs the deliberate edit (§2.6 NOTE-TO-CLOSE-GATE).**

### P4 — advisory NEVER denies / NEVER exits non-zero (report-only proven).
Run `advise.sh` against four inputs: `p1` (flagging), `p2` (clean), an empty diff (`printf '' | advise.sh --stdin`), and a malformed diff (`printf 'not a diff\n@@ garbage' | advise.sh --stdin`).
Assert for ALL four: (a) `echo $?` == `0`; (b) neither stdout nor the report file contains the substring `permissionDecision` or `"deny"`.
Static assert: `grep -nE 'exit [12]|permissionDecision|"deny"' substrate/skills/attribution-advisory/advise.sh` → no reachable deny/non-zero-exit path (report-only by construction).

### Supplementary fixtures — FUNCTIONAL ONLY, NOT threat-anchored (M2 note).
These exercise SECONDARY + vendored exclusion. **SECONDARY is UNRATIFIED best-effort courtesy (§4.3/§9), so these carry NO `defeats_via_probe` binding — they prove the feature works, not that a named threat is defeated:**
- `s1-newfile-nonprincipal.diff` — new file adding `author = "Mallory Example"` in a non-vendored path → SECONDARY flags (exit 0).
- `s2-vendored-nonprincipal.diff` — identical field under `node_modules/pkg/package.json` → SECONDARY does NOT flag (vendored exclusion; exit 0).
- `n1-copyright-prose.diff` — an added prose line merely *discussing* copyright (no year+name form) → no finding (negative; borrows the intent of the archived `fp5-copyright-prose` fixture).
- **(r5 negative-control, recommended)** `n2-year-bump.diff` — `-Copyright (c) 2024 Denson Smith` / `+Copyright (c) 2025 Denson Smith` → PRIMARY DOES fire (name-agnostic; documents the accepted r5 false-positive as EXPECTED behavior, with the report "WHAT TO CHECK" line naming the year-bump case). This fixture pins that the false-positive is a KNOWN, documented behavior, not a regression.

VERA additionally runs the project's FULL existing suite (surviving hook test `run-stop-self-check-tests.sh`, `npm run gen-data` determinism, `install.sh --dry-run` smoke) to confirm the retirement + skill addition breaks nothing elsewhere.
