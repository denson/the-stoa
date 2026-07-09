# design-rev1 — stoa--p0e: authorship deny-gate RETIREMENT + report-only attribution ADVISORY

**Author:** Denson Smith · **Arc:** stoa--p0e · **Seat:** CAPTAIN_DAEDALUS_the_stoa (architect)
**Consumes:** `agents/design/stoa--p0e/DAEDALUS-brief.md` (PLINY, authoritative) + the PRINCIPAL RULING — SCOPE RESHAPE (`stoa--p0e` 2026-07-09T09:07:01Z).
**Cite:** `stoa--dps` (PEP 621 false-positive), `stoa--eby`, Arc 46/65/69 hook history.

---

## 1. Problem restatement (pre-work gate, §6.1)

The PRINCIPAL retired all authorship **deny**-gates. This arc must (a) remove the `pretooluse-author-field-audit.sh` deny-hook from the-stoa's own live armed config AND the substrate source/template, archiving (not deleting) the script; (b) build a **report-only, never-blocking, best-effort, diff-scoped** attribution *advisory* whose PRIMARY job is to surface a diff hunk that MODIFIES or DELETES an existing attribution line (the plagiarism/license-breach direction the deny-gate never checked), with a SECONDARY check for NEW non-PRINCIPAL author fields outside vendored paths; (c) propagate both changes (retire the deny-hook, gain the advisory) to consumer workspaces through the existing `install.sh` + `check-substrate-updates` lifecycle, without touching any other repo; (d) preserve the two surviving Bash gates, the Stop/PostToolUse/SessionStart entries, the `CLAUDE.md` authorship doctrine (stays PRIMARY, untouched), the HARD SAFETY CONSTRAINT (deploy inert, arm only via `--enable-hooks` default-OFF, never auto-write a live settings.json), and the no-API-key / no-keyed-CI canon.

**Imported assumptions I am naming (not smoothing):**
- I read the brief's "durable report the operator/user-tier reads" as satisfied by a **skill**, not a hook. Rationale in §3. This is a design *choice* the brief left open ("your call within the invariant"), not a re-scope.
- I assume `python3` is present on substrate targets (same assumption every existing gate makes, `operating-disciplines.md` §13); the advisory FAIL-OPENs to an empty report + exit 0 if it is absent.
- I assume the `.claude/hooks/principal-identity` allow-list continues to be seeded by `install.sh` (it survives the retirement because the advisory's SECONDARY check reuses it — see §5). The retirement does NOT retire the seed.

Restatement converges with the brief; no divergence to escalate.

---

## 2. Retirement plan (concrete file/line edits — ADA executes)

### 2.1 Remove the deny-hook registration (2 files)

**(a) Live armed config — `.claude/settings.json` (repo root).** Delete the FIRST `PreToolUse.Bash` hook object — the `if: "Bash(git commit*)"` entry whose command ends `pretooluse-author-field-audit.sh` (currently lines 8–13, the object bounded by the `{` after `"hooks": [` through its closing `},`). Keep the two remaining objects intact (`Bash(git *)` clean-tree; `Bash(bw comment*)` no-dash-m). Do NOT touch `Stop`, `PostToolUse`, `SessionStart`. Post-edit the `PreToolUse.Bash.hooks` array has exactly 2 objects.

> This directly disarms the-stoa's OWN dogfooded gate — the-stoa is itself an armed workspace (invariant 1a; the dogfood instance of the M3 armed-consumer case, handled here directly because it is in-scope).

**(b) Consumer source-of-truth template — `substrate/templates/settings-hooks.json`.** Delete the identical first entry (the `{{HOOKS_DIR}}/pretooluse-author-field-audit.sh` object, currently lines 8–13). Keep the other two Bash gates, plus `Stop`, `PostToolUse`, both `SessionStart` matchers, and the `_comment` header (do NOT disturb the `startup|resume` substrate-check entry the live root settings.json lacks). The template `_comment` should drop/soften any author-field-gate reference if present (it currently does not name the gate specifically — verify and leave otherwise).

### 2.2 Archive the script (do NOT delete)

`git mv substrate/hooks/pretooluse-author-field-audit.sh substrate/v1-historical/hooks/pretooluse-author-field-audit.sh`

- Create `substrate/v1-historical/hooks/` (the `v1-historical/` precedent dir exists with role-file `.md`s + `templates/`; a `hooks/` subpath is the natural extension).
- **Glob-deploy consequence (confirmed):** `install.sh` deploys hooks by `for src in "${SRC_HOOKS_DIR}"/*.sh` (line ~1438) with `SRC_HOOKS_DIR="${SCRIPT_DIR}/hooks"`. Moving the script OUT of `substrate/hooks/` removes it from that glob → fresh installs stop deploying it. No `HOOK_NAMES` list to edit. **Confirmed against install.sh:163, :1438.**

### 2.3 `_hooklib.sh` — STAYS, functions LEFT INTACT (design decision + recommendation)

Leave `substrate/hooks/_hooklib.sh` in place (sourced by the surviving gates + Stop self-check). The author-specific functions `classify_author_file`, `extract_author_fields`, `parse_allow_pairs` became dead once the gate is archived (grep-confirmed: only the retired gate + `run-author-gate-tests.sh` call them; the surviving gates use the generic helpers `read_stdin_event` / `event_field` / `json_field` / `emit_deny` / `allow`). **Recommendation: LEAVE the dead functions in `_hooklib.sh`.** Pruning a shared lib to remove functions risks a subtle break in a surviving gate for zero runtime benefit (dead code costs nothing at run time). A future arc may prune them under a proven-zero-surviving-caller check; if it does, it must also account for the archived test that sources them. Recorded as a named weak point (§7 W4).

### 2.4 Test corpus disposition

- `git mv substrate/hooks/tests/run-author-gate-tests.sh substrate/v1-historical/hooks/tests/run-author-gate-tests.sh` and move the author-gate fixtures with it: `fixtures/tp/`, `fixtures/fp/`, `fixtures/control/` → `substrate/v1-historical/hooks/tests/fixtures/`.
- **KEEP** `substrate/hooks/tests/run-stop-self-check-tests.sh` + `fixtures/stop-event-orchestrator.json` (they test a SURVIVING hook).
- The advisory gets its OWN fresh corpus (diff fixtures, §6) under `substrate/skills/attribution-advisory/tests/` — the old fixtures are author-*file* fixtures, not *diff* fixtures, so they are archived rather than repurposed (a couple inform the new negatives; see §6).

### 2.5 Retirement record / WHY-HISTORY (invariant 5, must-settle #6)

Two durable homes:
1. **`substrate/v1-historical/hooks/RETIREMENT.md`** (new) — the canonical record. Documents, as *history explaining why retirement is correct, NOT as fix targets*: (i) `stoa--dps` (PEP 621 inline-table `authors = [{name=...}]` parser false-positive → a 3-day false-positive hold); (ii) the Bash-only matcher hole (PowerShell commits ungated); (iii) the compound `cd && git commit` matcher dodge (prefix-anchored `if` matcher); plus the empirical that arc-77 doctrine audits verified authorship correct 4× independently while the deny-hook contributed only a false-positive hold + a discovered coverage hole. Cite `stoa--dps`, `stoa--eby`.
2. **`substrate/hooks/README.md`** — update §4 table (remove the `pretooluse-author-field-audit.sh` row), add a short "Retired gates (Arc — stoa--p0e)" note pointing to `v1-historical/hooks/RETIREMENT.md` + naming the new advisory skill, and annotate §7 (the `.md` frontmatter narrowing) as *historical to the retired gate* (the narrowing lore is preserved via the archived script; the surviving lib functions are dead). Do NOT delete §7 — it is the durable record of the z2b narrowing.
3. ADA does the bw write dispositioning `stoa--dps` as **superseded-by-retirement** (noted here per invariant 5; DAEDALUS does not write bw tickets closed).

---

## 3. Advisory mechanism + surface (must-settle #1) — a report-only SKILL

**Decision: the advisory is a new skill `attribution-advisory` at `substrate/skills/attribution-advisory/`, deploying to `<workspace>/.claude/skills/attribution-advisory/`.** It is a deterministic, operator-invoked, report-only reporter — NOT a hook.

**Why a skill (chosen over the three candidate shapes in the brief):**

| Candidate | Why rejected / chosen |
|---|---|
| Non-blocking PreToolUse/Stop **hook** | Rejected. (1) Needs `--enable-hooks` arming → inherits the whole HARD-SAFETY / armed-consumer complexity for a thing that only *reports*. (2) Hooks are OUTSIDE `check-substrate-updates` enumeration (check.sh has zero `hook` awareness — verified) → a new hook would NOT be surfaced MISSING to consumers, breaking must-settle #5. (3) The report-carrying `additionalContext` channel is upstream-broken (README §6, issues #55889/#18427/#15174) → an unreliable surface. |
| Standalone loose operator script (e.g. under `substrate/hooks/` or a bare `substrate/tools/`) | Rejected as the primary home. A bare `.sh` under `substrate/hooks/` deploys via the glob but (a) conceptually pollutes the "harness-owned hook scripts" dir and (b) is NOT enumerated by `check-substrate-updates` → no MISSING propagation. A new `substrate/tools/` deploy class would need new install.sh + check.sh enumeration work (more scope, same end state as a skill). |
| **Skill** (CHOSEN) | Skills ARE enumerated by `check-substrate-updates` (SKILL_NAMES → `parse_skill_names_from_install` → MISSING detection). Skills need NO `--enable-hooks` arming. Skills are the substrate's established operator-invocable tool home (`whoami`, `inspect-script-output`, `gauntlet-setup` are precedent). One SKILL_NAMES delta rides the entire propagation + invocation + report lifecycle. It cannot ever deny (it is not in any PreToolUse path) — the report-only property is structural, not merely coded. |

**Shape:**
- Entry script `substrate/skills/attribution-advisory/advise.sh` (POSIX `sh` wrapper + a self-contained `python3` diff scanner; mirrors the gate scripts' `set -uo pipefail` + FAIL-OPEN style).
- `SKILL.md` (frontmatter `author: Denson Smith`) documenting invocation + the report path + the never-blocks contract.
- `tests/` corpus (§6).

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
  WHAT TO CHECK: confirm this change is legitimate (e.g. correcting YOUR OWN name);
       otherwise restore the original attribution before committing.

## SECONDARY — a NEW non-PRINCIPAL author-like field (outside vendored paths)
- file: src/foo.py  (added)
  field: author = "Mallory Example"
  WHY: a new author/owner/creator/... field naming someone who is not the PRINCIPAL,
       in a non-vendored path, may be a mis-attribution of the PRINCIPAL's own work.
  WHAT TO CHECK: if this is a CITED source author, move it to prose/citation; if it is
       a legitimate PRINCIPAL identity, add it to .claude/hooks/principal-identity.
```

**Where the operator sees it:** (1) directly — an operator/gauntlet seat runs `advise.sh` and reads the stdout summary + the report file; (2) the report file is the durable artifact the user-tier reads on demand. **Follow-up (out of scope this arc):** wiring `advise.sh` as an automatic step in the gauntlet close-gate (CATO/NOMOS) would touch those role files — deferred to a named follow-up (§8), not built here.

**Report-only / never-deny — structural guarantees (P4):** `advise.sh` (a) is never registered in any settings-hooks.json (it is a skill, not a gate); (b) ALWAYS `exit 0` — it contains no reachable `exit 1` / `exit 2` and no `permissionDecision` emission; (c) even if a future operator mis-registered it as a PreToolUse hook, an exit-0 script that emits no deny JSON is treated as ALLOW → it can never block by construction.

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

### 4.3 SECONDARY classification — NEW non-PRINCIPAL author field outside vendored paths

- Fires when an **added** line (`+` prefix, excluding the `+++` header) introduces an author-like **field assignment** whose extracted VALUE is a person-name NOT on the principal-identity allow-list, AND the target path is NOT vendored/imported.
- **Value extraction:** self-contained port of the `extract_author_fields` field-anchored logic (unquote + trim; skip template placeholders `{{..}}`/`<..>`/`$..`; flatten inline arrays) run over the added-line text only.
- **"Non-PRINCIPAL":** value (lower-cased, trimmed) not equal to any token in `<workspace>/.claude/hooks/principal-identity` (the same allow-list the retired gate read — still deployed, see §5). **FAIL-OPEN:** if the list is absent/empty, SECONDARY is skipped entirely (PRIMARY still runs, name-agnostic). This is the SAFE direction for a report-only tool — an unconfigured allow-list yields no noisy false SECONDARY findings.
- **Vendored/imported path exclusion (static, deterministic):** the added file's path contains any of `node_modules/`, `vendor/`, `third_party/`, `third-party/`, `thirdparty/`, `dist/`, `build/`, `.venv/`, `venv/`, `site-packages/`, `external/`, `deps/`, `.git/`, `v1-historical/`. Static list is the deterministic floor; a `.gitattributes` `linguist-vendored` refinement is a possible later enhancement (not required — noted W5).

### 4.4 Structural limits (accepted, best-effort)
- Line-anchored: a multi-line/wrapped attribution edit, or an attribution smuggled past the field-anchored regex, can be missed (false-negative). Report-only + doctrine-primary → acceptable per nothing-has-to-be-100% (W2).
- A pure `git mv` rename with no content change shows no attribution content lines → correctly silent (a rename does not change attribution text).

---

## 5. install.sh deltas (must-settle #4)

1. **`SKILL_NAMES` array (install.sh ~line 228)** — add `attribution-advisory`. This is the ONE line that (a) deploys the skill to `<dest>/.claude/skills/attribution-advisory/` and (b) makes `check-substrate-updates` enumerate it as source (→ MISSING on consumers → gained on apply). No other deploy plumbing needed (the skill-deploy loop at ~879/~1325 iterates SKILL_NAMES).
2. **Hook glob-deploy (~1438)** — NO code change. Archiving the script out of `substrate/hooks/` (§2.2) auto-removes it from the `*.sh` glob. Fresh installs deploy the 2 surviving gates + `_hooklib.sh` + README + the surviving Stop/PostToolUse/SessionStart scripts, minus the retired gate.
3. **principal-identity seed (step 5c, ~1471–1503)** — **KEEP the seeding** (the advisory SECONDARY reuses it). Update ONLY the comment prose (it currently names "`pretooluse-author-field-audit.sh` gate" at ~1490) to name the advisory instead, e.g. "the attribution-advisory skill's SECONDARY check compares new author-like field values against this list." No behavioral change; keeps the seed's self-documentation truthful post-retirement.
4. **`--enable-hooks` arming (step 5d, ~1521)** — NO change. It still arms the 2 surviving gates. The advisory needs no arming (it is a skill). HARD SAFETY CONSTRAINT preserved verbatim.
5. **Header comment (~85)** — update the note "The author-field gate reads a PRINCIPAL-identity allow-list…" to reflect that the allow-list now feeds the advisory skill (cosmetic accuracy).

---

## 6. check-substrate-updates interaction (must-settle #5) — the honest finding

`check.sh` enumerates DRIFTED / MISSING / OBSOLETE over MAJORs, CAPTAINs, **templates**, and **skills** — verified. **It has ZERO hook awareness** (grep: 0 `hook` matches in `check.sh`). Consequence, per surface:

| Change | Enumerated? | Propagation verdict |
|---|---|---|
| **Advisory skill gained** (`attribution-advisory` in SKILL_NAMES) | YES (skills) | source-present, consumer-absent → **MISSING** → `apply.sh` gains it. **WORKS.** |
| **Registration retired** (`settings-hooks.json` template loses the author-field entry) | YES (templates glob) | consumer's deployed candidate template differs from new source → **DRIFTED** → `apply.sh --all-differing` harvests DRIFTED → the consumer's *candidate* template loses the registration. **WORKS.** |
| **Retired SCRIPT file** at consumer `.claude/hooks/pretooluse-author-field-audit.sh` | **NO** (hooks unenumerated) | NOT flagged OBSOLETE, NOT auto-removed. Becomes an **inert orphan**: with the registration gone from the candidate template, the script has no registration → **never fires as a hook**. Harmless but untidy. |
| **ARMED consumer's LIVE `.claude/settings.json`** (still carries the registration + the script still on disk) | NO (settings.json is operator-owned; never auto-written — HARD SAFETY) | NOT touched by check.sh or install.sh. The template DRIFT is the operator's SIGNAL to manually remove the dead registration from their live settings.json. Documented in the README runbook. Inherent to the HARD SAFETY CONSTRAINT, not a new gap. |

**Net:** the two things that MUST propagate (gain the advisory; retire the *candidate* registration) DO propagate through enumerated surfaces (skills + templates). The two residuals (an inert orphan script; an armed consumer's live settings.json) are (a) harmless-when-registration-gone and (b) governed by the never-auto-write-a-live-settings.json HARD SAFETY invariant. The README retirement runbook (§2.5) instructs armed consumers to remove the dead registration + optionally delete the orphan script. A future arc could add hook enumeration to `check.sh` to auto-flag the orphan OBSOLETE (named follow-up §8). This is my top weak point (§7 W1).

---

## 7. Self-assessed weak points (§6.2)

- **W1 (top) — the orphan-script + armed-live-settings residual is process-mitigated, not mechanically mitigated.** `check-substrate-updates` cannot flag the retired hook OBSOLETE (hooks unenumerated) and cannot touch a live settings.json (HARD SAFETY). An armed consumer who never reads the template-DRIFT signal or the README runbook keeps a dead registration pointing at a still-present script → the retired gate keeps firing there. *Why this shape anyway:* auto-writing a live settings.json to disarm it would violate the HARD SAFETY CONSTRAINT (the arc's own invariant 8); the honest mechanism is the enumerated template DRIFT as a signal + a README runbook, with a named follow-up to teach check.sh hook-awareness. Surfaced as candidate M3/M4 for the A1 beat.
- **W2 — advisory false-negatives (best-effort line-anchored diff scan).** Obfuscated, multi-line, or non-field-shaped attribution edits can slip past. *Why anyway:* report-only + `CLAUDE.md` doctrine stays PRIMARY (untouched) + the nothing-has-to-be-100% ruling — a best-effort surface that can only help is the standing bar; a "100%" claim would be marketing BS.
- **W3 — the attribution term set is now MIRRORED in two places** (`_hooklib.sh extract_author_fields` and the advisory's self-contained scanner). SSoT tension (§6.10). *Why anyway:* the advisory operates on a DIFFERENT surface (a diff, not a file blob) and I chose to decouple the skill from the hooks dir (so the skill does not depend on `.claude/hooks/` being deployed/armed). Mitigation: cite the source list in the scanner + name a follow-up to extract the field list to a shared data file if it ever drifts. If ARGUS judges the coupling acceptable, sourcing `_hooklib.sh` from the skill is a viable alternative that restores one definition.
- **W4 — dead functions left in `_hooklib.sh`.** `classify_author_file`/`extract_author_fields`/`parse_allow_pairs` become unused. *Why anyway:* pruning a lib shared by surviving gates for zero runtime benefit risks a subtle break; the brief recommends leaving them; a future arc prunes under a proven-zero-caller check.
- **W5 — vendored-path exclusion is a static list.** A repo that vendors under a non-listed dir gets a possible false SECONDARY finding. *Why anyway:* report-only (a false SECONDARY is a note to review, not a block), deterministic, and easily widened; a `.gitattributes` refinement is a later enhancement.
- **W6 — report path collision / staleness.** A single overwritten `.claude/attribution-advisory-report.md` means the last run wins; a stale report could mislead. *Why anyway:* a single known path is the simplest durable surface; the report header stamps the scanned range + UTC time so staleness is self-evident. Timestamped reports are a trivial later change if wanted.

No empty-list defense needed — six named weak points.

---

## 8. Out of scope (this design deliberately does not address)

- Wiring `advise.sh` into the gauntlet close-gate (CATO/NOMOS) as an automatic review step — touches those role files; named FOLLOW-UP.
- Teaching `check-substrate-updates`/`check.sh` hook-awareness (to auto-flag the orphan script OBSOLETE) — separate tooling arc; named FOLLOW-UP.
- Extracting the attribution term set to a shared data file (SSoT) — only if W3 drift is observed; named FOLLOW-UP.
- Pruning the dead `_hooklib.sh` functions — future arc under a zero-caller proof.
- Any edit to `CLAUDE.md` §4 authorship doctrine (stays PRIMARY, untouched — invariant 6).
- Any keyed-CI / API-key / Sonnet-adjudication path (dropped — invariant 7).
- Touching other consumer repos (propagation is via the lifecycle only — invariant 4).

---

## 9. Threat→mitigation map (A3 author duty, §6.12) + threat-anchored probe (§6.13)

**M1 (named threat — PRINCIPAL-ratified in the SCOPE RESHAPE ruling as "the real harm … other authors' names getting REPLACED WITH the PRINCIPAL's in quoted material / imported OSS")** — PROPOSE **threat-ratified (detection-mitigation)**:

> `M1 (plagiarism / license-breach direction) → attack-path: a commit diff MODIFIES or DELETES an existing author/copyright/license/attribution line (replacing another author's credit with the PRINCIPAL's, or erasing an upstream attribution) → how-defeated (report-only DETECTION): the advisory's PRIMARY hunk-classifier flags every removed/changed attribution line in the durable report .claude/attribution-advisory-report.md for operator/user-tier review. defeats_via_probe: P1 (attack-detected) + P2 (legit-unaffected).`

The advisory is report-only, so the mitigation is **detection/surfacing**, not prevention; the threat-anchored probe asserts detection fires on the attack path AND stays silent on legitimate traffic.

**Other candidate M-items (for PLINY's A1 restatement beat):**
- **M2 — PROPOSE `not threat-ratified (scope reshape, no new runtime attack path)`:** retiring the deny-gate could let direction-1 regressions (an agent writes a non-PRINCIPAL name into its OWN new artifact) return. Residual covered by `CLAUDE.md` doctrine (PRIMARY, untouched) + the advisory SECONDARY detection. ARGUS confirms the classification.
- **M3 — PROPOSE `not threat-ratified (process/propagation gap, no runtime attack path)`:** an ARMED consumer's live settings.json keeps the dead registration (HARD SAFETY: never auto-written). Mitigation: template-DRIFT signal + README runbook.
- **M4 — PROPOSE `not threat-ratified (process/propagation gap)`:** `check-substrate-updates` does not enumerate hooks → the retired script orphan is not auto-flagged/removed. Mitigation: inert-without-registration (harmless) + README + follow-up.
- **M5 — PROPOSE `not threat-ratified (best-effort report-only residual)`:** advisory false-negative/false-positive. Acceptable per nothing-has-to-be-100%; doctrine stays primary.
- **The retirement itself — PROPOSE `not threat-ratified (PRINCIPAL-ruled scope reshape; removes a control the PRINCIPAL judged net-negative; residual covered by doctrine + advisory)`.** ARGUS confirms (I cannot self-grant the carve-out, §35.5).

---

## 10. Probe specification (§4 acceptance bar — VERA executes)

Fixtures under `substrate/skills/attribution-advisory/tests/fixtures/` (unified-diff `.diff` files). Runner `run-attribution-advisory-tests.sh` (source-only, does not deploy — mirror the author-gate test's source-only posture). All commands run from the worktree root; the advisory is exercised as the REAL `advise.sh` (no reimplementation).

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

### P3 — deny-hook provably retired.
Assert all of:
- `grep -c pretooluse-author-field-audit .claude/settings.json` → `0`
- `grep -c pretooluse-author-field-audit substrate/templates/settings-hooks.json` → `0`
- Both SURVIVING Bash gates still registered in each of the two files: `pretooluse-clean-tree-before-branch.sh` AND `pretooluse-no-dash-m-bw-comment.sh` present; and `stop-self-check.sh` (Stop), `posttooluse-agent-checker-trigger.sh` (PostToolUse), `sessionstart-compact-reprime.sh` + `sessionstart-substrate-check.sh` (SessionStart; the latter template-only) entries intact.
- `test ! -e substrate/hooks/pretooluse-author-field-audit.sh` (removed from source)
- `test -e substrate/v1-historical/hooks/pretooluse-author-field-audit.sh` (archived)
- `substrate/hooks/_hooklib.sh` still present.

### P4 — advisory NEVER denies / NEVER exits non-zero (report-only proven).
Run `advise.sh` against four inputs: `p1` (flagging), `p2` (clean), an empty diff (`printf '' | advise.sh --stdin`), and a malformed diff (`printf 'not a diff\n@@ garbage' | advise.sh --stdin`).
Assert for ALL four: (a) `echo $?` == `0`; (b) neither stdout nor the report file contains the substring `permissionDecision` or `"deny"`.
Static assert: `grep -nE 'exit [12]|permissionDecision|"deny"' substrate/skills/attribution-advisory/advise.sh` → no reachable deny/non-zero-exit path (report-only by construction).

### Supplementary fixtures (recommended, exercise SECONDARY + vendored exclusion)
- `s1-newfile-nonprincipal.diff` — new file adding `author = "Mallory Example"` in a non-vendored path → SECONDARY flags (exit 0).
- `s2-vendored-nonprincipal.diff` — identical field under `node_modules/pkg/package.json` → SECONDARY does NOT flag (vendored exclusion; exit 0).
- `n1-copyright-prose.diff` — an added prose line merely *discussing* copyright (no year+name form) → no finding (negative; borrows the intent of the archived `fp5-copyright-prose` fixture).

VERA additionally runs the project's FULL existing suite (surviving hook tests `run-stop-self-check-tests.sh`, `npm run gen-data` determinism, install.sh dry-run smoke) to confirm the retirement + skill addition breaks nothing elsewhere.
