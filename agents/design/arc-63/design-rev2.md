# Arc 63 pass A — design-rev2 (DAEDALUS)

## Your training data is out of date — search the web (CRITICAL)

When any claim about Claude Code hook behavior, `bw`, or a third-party surface would change this design, web-verify against current docs (gsearch) before inlining it — not memory. (Carried per repo CLAUDE.md propagation rule.)

---

**Ticket:** `stoa--p41.2` (epic; pass A). **Directive:** `substrate/arcs/arc-63-build-directive.md` (NOMOS-CONFORMANT @ b5de0aa). **Author of this design:** Denson Smith (the PRINCIPAL). **Builds against:** `arc-63/build` worktree base. **Supersedes:** design-rev1 (RATIFY-WITH-CONDITIONS, ARGUS `ARGUS-2026-06-17T20-47-06Z.md`). **Adjudication consumed:** floor-manager comments on `stoa--p41.2` (20:52 inline-candidate surface; 20:53 GATE-3 §4-RELOCATE call) + the orchestrator's Option-C brief.

This rev cites rev1 by section rather than re-pasting it (within-arc artifact discipline). It changes ONLY what ARGUS's F1–F4 + the floor-manager's gates require: the apply/revert mechanism (§4 below — **mechanism CORRECTED with a re-surfaced recommendation**), the F1 P-FALLBACK reader (§2.8 — NEW), and the deterministic P-EMPIRICAL surface (§3). Everything else in rev1 (§2.0 duality, §2.1 hook contract minus the path detail, §2.3 gauntlet-setup, §2.4 app-green, §2.5 doc-fix, §2.6 recompose-unaffected, the M1 map) carries forward unchanged unless a §ref below says otherwise.

---

## §1 Problem restatement (carried from rev1 §1, unchanged)

Move `check-substrate-updates` + `check-bw-release` off the orchestrator skill-menu (`SKILL_NAMES`) onto a deterministic SessionStart `type:"command"` trigger that runs their CHECK logic once per session-start under disposition-#2 guardrails (THROTTLE ~once/day, SURFACE-ON-SIGNAL-ONLY, NON-BLOCKING/fail-open), surfacing drift via `additionalContext` AND a P-FALLBACK signal file **that a non-additionalContext carrier actually reads**; in the same `install.sh`/`SKILL_NAMES` pass port `gauntlet-setup` into the substrate; keep the Stoa app green; doc-fix the stale "no fix through v2.1.150" note; and keep it structurally impossible for any build step to write a live `settings.json` (arming stays operator-gated `--enable-hooks`, default OFF).

**Imported assumptions A1–A3:** unchanged from rev1 §1. A1 (the check.sh logic is INVOKED by the hook, not reimplemented) is **reinforced** by this rev's recon: `check-substrate-updates/check.sh` is **1057 lines**, `apply.sh` 556, `revert.sh` 160, `check-bw-release/check.sh` 222 — inlining >1000 lines of drift logic into a SessionStart hook is not viable (it duplicates the logic, loses on-demand `check.sh --workspace X`, and loses apply/revert). The hook MUST invoke an external check.sh that exists on disk at a stable, deployed path. This kills the floor-manager's "inline the check logic into the hook" candidate for the check-substrate side specifically (see §4).

---

## §2 Approach

### 2.0 The source/deployed duality

Unchanged from rev1 §2.0, with ONE correction driven by the §4 mechanism change: there is **no relocation**, so the `.claude/skills/check-*/` self-deployed dirs do NOT move (rev1's DOGFOOD-NOTE gap evaporates). The duality table stands; the gauntlet-setup, hook-script, settings-hooks.json, README, and `.gitignore` rows are unchanged.

### 2.1 Deliverable #1 — the SessionStart trigger (carried from rev1 §2.1, with TWO edits)

The hook contract is carried verbatim from rev1 §2.1: matcher `startup|resume` (NOT `compact`), registered as a SECOND object in the candidate `SessionStart` array, fail-open at every step, stdout-only-JSON discipline, internal `timeout 10` per check.sh call, registration `timeout 30`, the `.substrate-check-hook-stamp` throttle stamp (distinct from check.sh's `.substrate-last-check`, verified L662), and the gitignore fix-now for both transients.

**EDIT 1 (resolves F3 — hook check.sh path).** Because §4 keeps the check dirs at `skills/check-*/` (NO relocation), the hook's check.sh invocation path is the EXISTING, UNCHANGED skills path — F3 is **moot, not merely resolved**. The hook resolves the check.sh at:

```
SUB_CHECK="$CWD/.claude/skills/check-substrate-updates/check.sh"   # consumer tier
BW_CHECK="$CWD/.claude/skills/check-bw-release/check.sh"
# the-stoa SUBSTRATE-tier dogfood fallback (script lives under substrate/skills/ not .claude/skills/):
[ -x "$SUB_CHECK" ] || SUB_CHECK="$CWD/substrate/skills/check-substrate-updates/check.sh"
[ -x "$BW_CHECK" ]  || BW_CHECK="$CWD/substrate/skills/check-bw-release/check.sh"
SUB_OUT=$(timeout 10 "$SUB_CHECK" --workspace "$CWD" 2>/dev/null) || SUB_OUT=""
BW_OUT=$(timeout 10  "$BW_CHECK" 2>/dev/null) || BW_OUT=""
```

This is the dual-candidate resolution rev1's §2.1 NOTE PROMISED but its pseudocode didn't implement (the F3 internal inconsistency). It is now implemented: try the consumer `.claude/skills/` path, fall back to the substrate-tier `substrate/skills/` path, use whichever is `-x`. Both paths are STABLE under Option C (no dir moves). At consumer tier the `.claude/skills/check-*/check.sh` path resolves because §4 deploys those dirs there (the carve-out, §4 mechanism).

**EDIT 2 (the F1 P-FALLBACK write half).** The hook still WRITES `.claude/.substrate-drift-signal` on drift (rev1 §2.1 L83). The READ half — the load-bearing F1 fix — is §2.8. The throttle re-surface path (rev1 §2.1 L57) is RETAINED but is no longer claimed as the fallback carrier (that claim was F1's defect — it re-emits via additionalContext). It is now correctly framed as an additionalContext-channel convenience only; the GUARANTEED carrier is the Stop-hook reader (§2.8).

Everything else in rev1 §2.1 (the pseudocode flow, payload-authoring WHY/WHAT rule, stdout discipline, gitignore, timeout) is unchanged.

### 2.2 Deliverable #2 — retire the 2 check skills from `SKILL_NAMES` (+ apply/revert fate)

**`SKILL_NAMES` edit:** unchanged from rev1 §2.2 — remove `check-substrate-updates` + `check-bw-release`, add `gauntlet-setup`. Net **−2 +1 = 9 entries**.

**Apply/revert fate:** see §4 — the mechanism is **CHANGED from rev1's RELOCATE to Option C** (keep dirs at `skills/check-*/`, delete only their SKILL.md, deploy + retain via a targeted install.sh carve-out). The hook's check.sh path (§2.1 EDIT 1) targets the UNCHANGED skills path accordingly.

### 2.3 Deliverable #3 — port `gauntlet-setup` (carried from rev1 §2.3, unchanged)

Copy `~/.claude/skills/gauntlet-setup/SKILL.md` → `substrate/skills/gauntlet-setup/SKILL.md` verbatim; add `gauntlet-setup` to `SKILL_NAMES`. Frontmatter parses clean (`name: gauntlet-setup` matches dir, no `author` field, non-strict `z.object({name,description})`). `team-launcher` dependency stays in `SKILL_NAMES`. ARGUS confirmed this section sound — no change.

### 2.4 Deliverable #4 — keep the app green (carried from rev1 §2.4, with the count rationale updated for Option C)

`discoverSkillFiles` (gen-data-lib.ts:92-110) is DIRECTORY-driven AND **SKILL.md-gated** (L100-101 `if (!fs.existsSync(skillMdPath)) continue` — verified live this rev). Under Option C the two check dirs **stay in `substrate/skills/` but lose their SKILL.md**, so gen-data SKIPS them exactly as a relocation would — the stale-LIEUTENANT trap is closed by the SKILL.md deletion, not by moving the dir. Net `substrate/skills/` LIEUTENANT delta: **−2 (checks lose SKILL.md → skipped) +1 (gauntlet-setup) = −1**, identical to rev1's claimed delta. The directive's −1 holds.

The `generated.test.ts` count-agnostic assertion (L92 `toBeGreaterThan(0)`) stays green at −1; gauntlet-setup passes the shape checks. **No test edit required.** The optional clarity-comment edit at L90-92 is RETAINED but its wording changes (no relocation now):

```
// Arc 17.1 made the gen-data adapter read all substrate skills as
// LIEUTENANTs. (agent-author retired Arc 61; the 2 check skills had their
// SKILL.md removed in Arc 63 — kept as operator tools under skills/check-*/
// but no longer rendered as LIEUTENANTs — + gauntlet-setup ported in; net
// LIEUTENANT churn handled by re-deriving from the dir.)
// Don't over-specify count — substrate may grow more.
```

Green path: `cd app && npm run gen-data && npm run build && npm test`. **Regen re-derives the WHOLE roster** (memory: gen-data-regen-re-derives-whole-roster) — VERA asserts green from a FULL `npm test` run, not from "this arc edited no MAJOR/CAPTAIN file."

### 2.5 Deliverable #5 — doc-fix the stale SessionStart note (carried from rev1 §2.5, unchanged)

Unchanged from rev1 §2.5: surgical narrowing of "no fix through v2.1.150" in `.claude/hooks/README.md` + `substrate/hooks/README.md` §6 and the `settings-hooks.json` `_comment` STAGE 2 sentence — SessionStart `startup|resume` additionalContext is a WORKING channel as of v2.1.170 (gated on the P-EMPIRICAL result, §3); PostToolUse/PreToolUse (#55889 open) + the `compact` matcher (#15174) stay best-effort. **GATING DEPENDENCY (rev1 weak-point 4):** ADA finalizes the doc-fix wording AFTER VERA runs P-EMPIRICAL — write what the probe shows, not what gsearch predicted.

### 2.6 Recompose / Checks A–E (carried from rev1 §2.6, unchanged)

This arc adds NO module (the hook is a `*.sh` glob artifact; gauntlet-setup is a `substrate/skills/` dir; the check tools STAY at `substrate/skills/check-*/` — no `substrate/maintenance/` is created, so even the rev1 relocation-home concern evaporates). The recompose's Check-A owned-module set (`SRC_MODULES_DIR/*.md`) is unchanged → recompose unaffected. **CONFIRM via a REAL non-dry-run subproject recompose** (§3 RECOMPOSE probe — a dry-run early-returns before the awk FAIL-LOUD Checks, Arc-61 lesson).

> **Note vs rev1's F4 caveat:** rev1 worried that `substrate-update-check.md` is a RECOMPOSED module whose xref edit must survive recompose. Under Option C **there is no xref edit** (no path changes — §4), so that caveat is moot. The module's existing `skills/check-substrate-updates/` references stay VALID (the dir is still there).

### 2.7 Module cross-reference audit — MOOT under Option C (was rev1 §2.7, the F4 surface)

**Under Option C this section is a NON-action.** The 74 references across ~14 canon files (×2 for substrate/ + .claude/ copies) to `skills/check-substrate-updates/` and `skills/check-bw-release/` — `MAJOR_POLYBIUS.md`, `operating-disciplines.md`, `modules/{substrate-update-check,bw-upgrade,mechanical-inspection-split,multi-team-interop}.md`, `README.md`, the surviving check SKILL.md siblings — **all stay VALID** because the dirs do not move. The path-bearing refs still resolve; the baseline-location prose in `bw-upgrade.md` ("two levels above this script") stays CORRECT (the `../..` anchor is unchanged — F2 moot, §4). **F4 is eliminated, not mitigated.** The XREF probe (§3) becomes a CONFIRMATION that nothing went stale (expected: zero dangling refs), not a sweep-coverage gate.

This is the single largest reason Option C is the minimal-blast-radius path the directive's housekeeping-pass-A posture asks for: it converts the highest-surface-area edit in the arc (a 74-ref two-copy rewrite + recompose-survival worry) into a no-op.

### 2.8 F1 — the P-FALLBACK reader (NEW; the floor-manager's TOP gate)

**The gap (ARGUS F1, HIGH):** rev1 WROTE `.claude/.substrate-drift-signal` but wired NO non-additionalContext reader. The only fallback was the hook's own throttle re-surface, which re-emits via `additionalContext` — collapsing the fallback onto the very channel it must survive. The directive requires "a RELIABLE carrier reads [the signal file] (the Stop self-check and/or CLAUDE.md) … surfacing must never depend on additionalContext ALONE."

**The fix: wire a reader into `.claude/hooks/stop-self-check.sh` (the Stop self-check).** This is a PROVEN non-additionalContext channel: the Stop hook surfaces text to the model via `decision:"block"` + `reason` (verified in the script header L12-15 — Stop supports `decision`/`reason`, NOT additionalContext). The signal therefore reaches the model on a channel structurally INDEPENDENT of the additionalContext path that P-EMPIRICAL tests. Both the source (`substrate/hooks/stop-self-check.sh`) AND self-deployed (`.claude/hooks/stop-self-check.sh`) copies get the identical edit (rev1 §2.0 duality; ADA `diff`-confirms byte-identical).

**Read contract (concrete):**

- **WHEN read:** every Stop-hook fire, at the point where the script builds `REASON` (currently a fixed A/B/C checklist, L90-94). The reader runs AFTER the infinite-block guard (L85 sentinel check) so it inherits the existing once-per-turn semantics — the drift line surfaces at most once per turn, never loops.
- **WHAT it reads:** `"${CWD}/.claude/.substrate-drift-signal"` where `CWD` is already resolved at L56 (`event_field cwd`). The signal file's body already states WHY/WHAT inline (rev1 §2.1 payload rule), so the reader appends it verbatim as a new checklist clause **(D)**.
- **WHAT it emits:** if the signal file exists and is non-empty, the script appends to `REASON`:
  ```
  (D) SUBSTRATE-DRIFT SIGNAL present (.claude/.substrate-drift-signal): <file body>.
      This is informational/non-blocking — surface it to the PRINCIPAL/operator; do not auto-apply.
      Run check-substrate-updates/check.sh --workspace . (or apply.sh) per the body.
  ```
  Clause (D) rides the SAME `decision:"block"` + `reason` JSON the existing checklist uses — NO new emit channel, NO additionalContext. If the signal file is absent or empty, clause (D) is omitted and the checklist is the unchanged A/B/C (graceful no-op — the Stop hook's behavior for non-drift sessions is byte-identical to today).
- **HOW it clears:** the SessionStart hook already `rm -f`s the signal file when a check finds NO drift (rev1 §2.1 L78). So the signal is self-clearing: next session-start with no drift removes it, and clause (D) stops surfacing. The Stop reader does NOT clear it (clearing is the check's job — a Stop fire is not evidence the drift was resolved). The signal is in `.gitignore` (never committed).
- **FAIL-OPEN preserved:** the read is a guarded `[ -f "$sig" ] && body=$(cat "$sig" 2>/dev/null)`; any failure leaves `REASON` as the unchanged A/B/C and the script proceeds. No new abort path; the existing `|| allow` fail-open semantics are untouched.

**Belt-and-suspenders second reader (CLAUDE.md line — RECOMMENDED, low-cost):** add ONE line to the substrate CLAUDE.md template's POLYBIUS block (the block `install.sh` L1557-1563 appends) AND the-stoa's own `CLAUDE.md`:
> "If `.claude/.substrate-drift-signal` exists on disk, surface its contents to the PRINCIPAL at the start of the next orchestrator turn (substrate-drift was detected at session start; do not auto-apply)."

This gives a SECOND independent carrier (an instruction the agent reads regardless of hooks being armed) so the signal surfaces even on a workspace where `--enable-hooks` was never run (the Stop hook is INERT until armed). The Stop-hook reader is the GUARANTEED carrier WHEN hooks are armed; the CLAUDE.md line covers the hooks-unarmed case. Together they satisfy "never additionalContext ALONE" in BOTH the armed and unarmed states.

**Why not additionalContext re-surface:** the rev1 throttle re-surface is RETAINED only as an additionalContext convenience (it works when additionalContext works, which P-EMPIRICAL is establishing). It is explicitly NOT counted toward the F1 gate. The F1 gate is met by the Stop-hook `reason` reader (+ the CLAUDE.md line), both off-additionalContext.

### Threat→mitigation map (carried from rev1, unchanged — M1 still the sole named threat)

> **M1 (live-settings.json auto-write — gate-origin, ratified)** → *attack path:* a build/install step (or the new hook registration, or the new §2.8 Stop-hook edit) writes/merges a hook block into a live `.claude/settings.json`, arming gates into the running session (no-experiments-on-real-agents violation in spirit). → *how-defeated:* the new SessionStart hook is a `substrate/hooks/*.sh` glob artifact + a CANDIDATE-only `settings-hooks.json` entry; the §2.8 edit modifies an EXISTING already-candidate Stop-hook SCRIPT (not its registration) — it adds no new registration and no new settings.json write-path; the Option-C install.sh carve-out (§4) deploys SCRIPTS to `.claude/skills/`, never a settings.json. Arming stays the operator-gated `--enable-hooks` (DEFAULT OFF, `ENABLE_HOOKS=0`). The §3 NOSETTINGS probe is the threat-anchored probe.

**§2.8 Stop-hook edit — explicit classification:** `not threat-ratified (process change: edits an already-deployed candidate hook SCRIPT body to read an on-disk file and append text to its existing `reason` output; no new runtime attack path, no new registration, no new settings.json write)` per op-disc §35.5. ARGUS confirms (I cannot self-grant the carve-out).

All other changes (menu demotion + SKILL.md deletion + carve-out deploy + doc-fix + app re-derive) remain `not threat-ratified (process/tooling change; no runtime attack surface)` per op-disc §35.5.

---

## §3 Verification probes (VERA executes verbatim)

All paths relative to the worktree root `…/arc-63-build/` unless absolute. Each probe: command + observable + pass/fail. Probes carried unchanged from rev1 are cited; CHANGED/NEW probes are written in full.

### P-EMPIRICAL — SessionStart additionalContext fires, asserted on the DETERMINISTIC surface (mandatory; rewritten per ARGUS + floor-manager)

The directive's load-bearing premise. THROWAWAY-target test — **HARD CONSTRAINT: no live settings.json on any canonical seat; mktemp throwaway only** (op-disc §25.5). claude version is **v2.1.170** (confirmed this rev). ARGUS + gsearch confirmed `claude -p` DOES fire the `startup` matcher, so the probe is RUNNABLE.

**PRIMARY assertion = deterministic (independent of model behavior):**

1. **Build a throwaway harness** with a sentinel-emitting SessionStart `startup` hook (identical to rev1 P-EMPIRICAL step 2 — `mktemp -d`, write `$TMP/.claude/hooks/probe-sessionstart.sh` emitting `{"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":"STOA_PROBE_SENTINEL_7F3A …"}}`, and `$TMP/.claude/settings.json` registering it under `matcher:"startup"`). **This writes settings.json ONLY inside the mktemp throwaway — no canonical seat touched.**
2. **Fire with `--debug hooks` and capture stderr + the transcript:**
   ```
   cd "$TMP" && claude --debug hooks -p "reply with only the word READY" --max-turns 1 \
     > "$TMP/out.txt" 2> "$TMP/debug.txt"
   ```
3. **PRIMARY PASS (deterministic — the gate VERA keys on):** EITHER surface shows the injection independent of what the model says:
   - **(a) debug stderr:** `grep -F 'STOA_PROBE_SENTINEL_7F3A' "$TMP/debug.txt"` OR `grep -iE 'additionalContext|SessionStart.*inject|hook.*output' "$TMP/debug.txt"` shows the SessionStart hook's additionalContext being extracted/injected. **AND/OR**
   - **(b) transcript JSONL:** locate the session transcript (`$TMP/.claude/projects/**/<session>.jsonl` or the `transcript_path` the debug log names) and `grep -F 'STOA_PROBE_SENTINEL_7F3A' <transcript>` — the injected context is recorded in the transcript regardless of whether the model echoed it.
   PASS = (a) OR (b) shows the sentinel/injection event. This asserts the CHANNEL fired, not that the model obeyed.
4. **SECONDARY corroboration (soft — NOT the gate):** `claude -p "What is the sentinel token in your context? Reply with only the token." --max-turns 1` → model reply contains `STOA_PROBE_SENTINEL_7F3A`. Record it as corroboration; a SECONDARY miss with a PRIMARY pass is still an overall PASS (model instruction-following is not the injection test).
5. **FAIL:** neither (a) nor (b) shows the injection → the channel is dead on this build → the doc-fix (§2.5) flips to "still broken" and the P-FALLBACK Stop-hook reader (§2.8) becomes the SOLE carrier (the design still functions — that is the whole point of F1). This is a FINDING for the floor-manager, NOT a design-blocker.
6. **Teardown:** `rm -rf "$TMP"` (var bound to `mktemp -d` output; literal-rooted, safe).

> If `--debug hooks` is not a valid flag form on v2.1.170, VERA falls back to `claude --debug` (full debug) and greps the same stderr tokens; the transcript-JSONL surface (b) is the more portable of the two deterministic surfaces and is sufficient alone for PASS.

### F1-READER — the Stop-hook reads the drift signal off a non-additionalContext channel (NEW; the F1 gate)

1. **Seed a drift signal and fire the Stop hook directly:**
   ```
   TMPW=$(mktemp -d); mkdir -p "$TMPW/.claude/hooks"
   cp .claude/hooks/_hooklib.sh "$TMPW/.claude/hooks/"
   cp .claude/hooks/stop-self-check.sh "$TMPW/.claude/hooks/"
   printf 'substrate drift: run check-substrate-updates/check.sh --workspace . ; apply via apply.sh\n' \
     > "$TMPW/.claude/.substrate-drift-signal"
   echo '{"hook_event_name":"Stop","session_id":"probe","transcript_path":"","cwd":"'"$TMPW"'"}' \
     | bash "$TMPW/.claude/hooks/stop-self-check.sh" > "$TMPW/stop-out.json" 2>/dev/null
   ```
2. **PASS (signal surfaced off additionalContext):** `"$TMPW/stop-out.json"` is a single JSON object with `"decision":"block"` and its `"reason"` string CONTAINS the signal-file body (the `substrate drift:` text) under a clause (D). Assert: `grep -F 'substrate drift' "$TMPW/stop-out.json"` matches AND `grep -F '"decision":"block"' "$TMPW/stop-out.json"` matches AND the output contains NO `additionalContext` key (the carrier is `reason`, not additionalContext). **FAIL:** the signal body is absent from the Stop output, or it surfaces via an additionalContext key.
3. **PASS (graceful no-op when no signal):** remove the signal file (`rm -f "$TMPW/.claude/.substrate-drift-signal"`), re-fire with a FRESH turn-key (new session_id to dodge the per-turn sentinel), confirm the `reason` is the UNCHANGED A/B/C checklist with NO clause (D). **FAIL:** clause (D) appears with no signal file, or the A/B/C checklist is altered.
4. **PASS (fail-open preserved):** make the signal file unreadable (or point cwd at a missing dir) and confirm the script still emits a valid block (or `allow`) and never aborts non-zero. **FAIL:** any non-zero exit / crash.
5. **PASS (dual-copy identical):** `diff substrate/hooks/stop-self-check.sh .claude/hooks/stop-self-check.sh` → byte-identical. **FAIL:** any diff.
6. **Teardown:** `rm -rf "$TMPW"`.

### G-a — TRAP CLOSED: gen-data renders NO orphaned check skill (floor-manager gate)

```
cd app && npm run gen-data
```
Then inspect the generated roster: `grep -c 'check-substrate-updates\|check-bw-release' app/src/data/agents.ts` over the LIEUTENANT-skill entries. **PASS:** the generated data contains NO LIEUTENANT skill named `check-substrate-updates` or `check-bw-release` (their dirs under `substrate/skills/` have no SKILL.md → `discoverSkillFiles` L100-101 skips them); `gauntlet-setup` IS present. **FAIL:** either check skill renders as a LIEUTENANT. (Direct evidence the trap is closed at the gen-data layer — the floor-manager's G-a.)

### G-b — CAPABILITY PRESERVED: check + apply/revert land in a consumer `.claude/` (floor-manager gate)

```
TMPC=$(mktemp -d)
bash substrate/install.sh --target project --project-dir "$TMPC" --dry-run \
  > "$TMPC/dryrun.txt" 2>&1
```
**PASS (all four):**
  (i) `grep -F 'check-substrate-updates' "$TMPC/dryrun.txt"` shows the carve-out planning a deploy of `…/check-substrate-updates/` → `…/.claude/skills/check-substrate-updates/` (carrying `check.sh` + `apply.sh` + `revert.sh`);
  (ii) `grep -F 'check-bw-release' "$TMPC/dryrun.txt"` shows the same for `check-bw-release/` (carrying `check.sh`);
  (iii) `grep -F 'gauntlet-setup' "$TMPC/dryrun.txt"` shows gauntlet-setup deploying via the SKILL_NAMES loop;
  (iv) the dry-run does NOT plan to PRUNE the check dirs as obsolete (the carve-out must also exempt them from the L1712 obsolete-prune scan — see §4).
**FAIL:** the check dirs are absent from the deploy plan (capability orphaned — the exact regression the directive forbids), OR they appear in the obsolete/prune list (would be deleted on `--prune-obsolete`). Teardown `rm -rf "$TMPC"`.

> Real-deploy corroboration (non-dry-run, recommended): repeat with no `--dry-run` against a second mktemp target and `ls "$TMP2/.claude/skills/check-substrate-updates/"` → `check.sh apply.sh revert.sh` present; `ls "$TMP2/.claude/skills/check-bw-release/"` → `check.sh` present; and NO `SKILL.md` in either (confirms the SKILL.md deletion rode through deploy and the consumer dir is a tool-dir, not a skill).

### F2-MOOT — check.sh state-file `../..` anchor is unchanged (resolves F2)

```
grep -n 'SCRIPT_DIR}/\.\./\.\.\|SUBSTRATE_DIR=\|SKILLS_PARENT_DIR=' \
  substrate/skills/check-substrate-updates/check.sh substrate/skills/check-bw-release/check.sh
```
**PASS:** both scripts still compute their anchor as `SCRIPT_DIR/../..` and the scripts STILL live at `substrate/skills/check-*/` (two levels under `substrate/`) and deploy to `.claude/skills/check-*/` (two levels under `.claude/`) — so `../..` resolves to `substrate/` / `<workspace>/.claude/` exactly as before. No edit to the anchor is needed BECAUSE the dirs did not move. **FAIL:** either script's anchor was edited, or either dir moved out of the two-levels-under-root position. (Under Option C, F2 is moot by construction — this probe is the confirmation.)

### F3-MOOT — the hook resolves the check.sh at the unchanged skills path (resolves F3)

`grep -n 'skills/check-substrate-updates/check.sh\|skills/check-bw-release/check.sh' substrate/hooks/sessionstart-substrate-check.sh .claude/hooks/sessionstart-substrate-check.sh`. **PASS:** the hook invokes the check.sh at `.claude/skills/check-*/check.sh` (consumer) with a `substrate/skills/check-*/check.sh` fallback (the-stoa dogfood) — §2.1 EDIT 1 — and BOTH paths exist post-arc (the dirs did not move). **FAIL:** the hook points at any `maintenance/` path, or at a path that does not exist post-arc.

### NOSETTINGS — no build step writes a live settings.json (THREAT-ANCHORED for M1; updated file-list)

1. `git -C …/arc-63-build diff --name-only <base>..HEAD`. **PASS:** the changed-files list contains ONLY `substrate/hooks/sessionstart-substrate-check.sh` (+ `.claude/` copy), `substrate/hooks/stop-self-check.sh` (+ `.claude/` copy — the §2.8 F1 edit), `substrate/templates/settings-hooks.json` (+ `.claude/` copy), `substrate/hooks/README.md` (+ `.claude/` copy), `substrate/install.sh`, `substrate/skills/gauntlet-setup/SKILL.md`, the two `substrate/skills/check-*/SKILL.md` DELETIONS (+ their `.claude/skills/check-*/SKILL.md` deletions), the `.gitignore` template (in `install.sh`) + self-deployed `.claude/.gitignore`, the CLAUDE.md F1 line (template-in-install.sh + the-stoa `CLAUDE.md`), `app/src/data/agents.ts` (gen-data output) + optional `generated.test.ts` comment, and this design doc. **FAIL:** any `**/settings.json` that is a LIVE settings.json (NOT `settings-hooks.json`, NOT under a `templates/` path) appears.
2. **(a) attack-blocked:** `grep -rn '"hooks"' --include=settings.json` over the repo (excluding `templates/`) returns NOTHING new from this arc. **(b) legit-unaffected:** `install.sh --target user --dry-run` still PRINTS the `--enable-hooks` manual-merge runbook (operator arming intact). PASS requires both.

### RECOMPOSE — real (non-dry-run) subproject recompose passes Checks A–E (carried from rev1 §3, unchanged)

```
PARENT=$(mktemp -d); bash substrate/install.sh --target subproject --parent-dir "$PARENT" --subproject probe63
```
**PASS:** exit 0, no `err()`/FAIL-LOUD abort, role files recomposed clean. **FAIL:** any non-zero/abort. Teardown `rm -rf "$PARENT"`.

### APPGREEN — the Stoa app stays green (carried from rev1 §3, unchanged)

`cd app && npm run gen-data && npm run build && npm test` → gen-data 0, build 0, FULL `npm test` all green (assert from the full run — memory: gen-data-regen-re-derives-whole-roster), LIEUTENANT slot non-empty at −1. **FAIL:** any non-zero, empty LIEUTENANT slot, or gauntlet-setup shape failure.

### SKILLNAMES — net −2 +1 (carried from rev1 §3, unchanged)

`grep -A12 'SKILL_NAMES=(' substrate/install.sh` → 9 entries; both check skills ABSENT; gauntlet-setup PRESENT; team-launcher present.

### LANDING — gauntlet-setup deploys to a consumer `.claude/skills` (carried from rev1 §3, unchanged)

`install.sh --target project --project-dir "$TMP_CONSUMER" --dry-run` → grep stdout for `deploy skill: …/gauntlet-setup/`. PASS: gauntlet-setup planned; no check skill planned via the SKILL_NAMES loop (the check dirs deploy via the §4 carve-out instead — see G-b).

### NOSTALE-LIEUTENANT — no half-retired skill dir (REWRITTEN for Option C)

`ls substrate/skills/check-substrate-updates/ substrate/skills/check-bw-release/`. **PASS:** both dirs PRESENT (operator tools retained), and NEITHER contains a `SKILL.md` (confirms the SKILL.md deletion that closes the trap); `check.sh` (both) + `apply.sh` + `revert.sh` (substrate-updates) present. **FAIL:** either dir still carries a `SKILL.md` (trap still open), or either dir is gone (capability dropped). Pairs with G-a (gen-data layer) — this is the on-disk layer.

### GITIGNORE — hook transients are ignored (carried from rev1 §3, unchanged)

`grep -n 'substrate-check-hook-stamp\|substrate-drift-signal' substrate/install.sh .claude/.gitignore`. PASS: both names in the install.sh gitignore template (L566 echo + the L570-591 literal heredoc) AND in self-deployed `.claude/.gitignore`. Also `git status --porcelain` after a hook run shows neither transient untracked.

### XREF — no dangling skill-path reference (REPURPOSED: confirm-clean, not sweep)

`grep -rn 'skills/check-substrate-updates\|skills/check-bw-release' substrate/ .claude/ --include='*.md'` (excluding `substrate/arcs/` + this design doc). **PASS under Option C:** the matches that EXIST are all still VALID (the dirs did not move) — every `skills/check-*` path still resolves on disk. The probe asserts no NEW dangling ref was introduced (expected: the pre-arc ref set, all valid). **FAIL:** any ref points at a path that does NOT exist post-arc (would only happen if something moved — it shouldn't under Option C). This probe is now a regression-guard, not a 74-ref coverage gate.

---

## §4 Apply/revert fate — the headline design-lock (MECHANISM CORRECTED + re-surfaced)

### 4.1 Recommendation: OPTION C (keep dirs at `skills/check-*/`, delete only SKILL.md, deploy via targeted carve-out)

**RECOMMENDATION: keep `check-substrate-updates/{check.sh,apply.sh,revert.sh}` and `check-bw-release/{check.sh}` at their CURRENT path `substrate/skills/check-*/`. DELETE ONLY the two `SKILL.md` files (source + self-deployed copies). Add a TARGETED install.sh carve-out that (a) DEPLOYS those two dirs to consumer `.claude/skills/check-*/` even though they are no longer in `SKILL_NAMES`, and (b) EXEMPTS them from the obsolete-prune scan. Do NOT relocate; do NOT inline; do NOT delete the capability.**

This **departs from the floor-manager's GATE-3 §4-RELOCATE call.** The departure is grounded in recon evidence the floor-manager did not have at decision time, and the floor-manager explicitly invited it: *"confirm or correct my read of install.sh L1241 — if there is a non-SKILL_NAMES deploy mechanism I missed, say so — it may change the cheapest mechanism."* It also sits inside the floor-manager's own escape-hatch framing (*"if preserving consumer capability genuinely forces §4's relocation, take §4 … but you must JUSTIFY why inline+minimal-deploy doesn't suffice"*) — here the justification runs the OTHER way: a cheaper mechanism than relocation exists, so relocation's blast radius is not forced.

### 4.2 Why Option C beats §4-RELOCATE and the inline candidate (the justification)

Scored against the gate criteria {minimal blast radius + capability survives to consumers + trap closed + F2/F3 moot-or-resolved}:

| | §4-RELOCATE (to `maintenance/`) | INLINE the check | **OPTION C (recommended)** |
|---|---|---|---|
| Trap closed | yes (gen-data scope) | yes (no skill dir) | **yes** (gen-data L100-101 skips no-SKILL.md, verified) |
| Capability to consumer | NEW deploy block for `maintenance/` | loses on-demand check.sh + apply/revert | **carve-out deploy block (small)** |
| F2 (`../..` anchor) | **BREAKS** → check.sh surgery + stale bw-upgrade.md prose | breaks (no script) | **MOOT** (dirs don't move; `../..` unchanged) |
| F3 (hook path) | needs repath | n/a (inlined) | **MOOT** (path unchanged) |
| F4 (74-ref xref sweep ×2 copies) | **REQUIRED** (highest-risk edit in the arc) | required (refs point at a gone skill) | **MOOT** (zero path change → zero xref churn) |
| install.sh special-cases | 1 new deploy block | hook rewrite + apply/revert deploy block | **2 small blocks** (deploy carve-out + prune-exempt) |
| Viability | viable but high blast radius | **NOT viable** for check-substrate (1057-line check.sh can't inline; loses apply/revert) | viable |

Decisive points, each evidence-backed this rev:

1. **§4-RELOCATE's blast radius is 74 refs across ~14 canon files, ×2 for the substrate/ + .claude/ copies — NOT rev1's "~6" or ARGUS F4's ~5.** (`grep -rn 'skills/check-*'` this rev.) Each path-bearing ref is a dangling-risk and the XREF probe catches a DANGLING ref but not a SEMANTICALLY-wrong-but-present one (rev1 weak-point 2). For a *housekeeping pass A* this is the opposite of minimal.
2. **§4-RELOCATE BREAKS F2.** Both check.sh scripts anchor state/registry on `SCRIPT_DIR/../..` (check-substrate: `SUBSTRATE_DIR` → `consumer-workspaces.txt` registry; check-bw: `SKILLS_PARENT_DIR` → `.bw-release-last-check` state). Moving to `…/maintenance/check-*/` re-points `../..` at `maintenance/` (wrong) — requiring check.sh edits AND a rewrite of bw-upgrade.md's "two levels above this script" baseline-location prose. Option C leaves `../..` correct at BOTH tiers — **F2 moot by construction.**
3. **The INLINE candidate is not viable for check-substrate-updates.** Its `check.sh` is 1057 lines; inlining duplicates the logic, loses on-demand `check.sh --workspace X`, and loses apply/revert entirely (the directive forbids dropping apply/revert). Inline could at best cover check-bw-release (222 lines) — a partial that still needs a deploy path for check-substrate's apply/revert, i.e. it doesn't actually shrink the problem.
4. **Option C's cost is honest and small: TWO hard-coded install.sh blocks, not one.** The deploy carve-out (deploy the 2 non-SKILL_NAMES dirs to `.claude/skills/check-*/`) PLUS a prune-scan exemption — because the L1712 obsolete-prune scan iterates `DEST_SKILLS_DIR/*/` and flags any dir not in `SKILL_NAMES` and not `custom-`-prefixed as obsolete; under `--prune-obsolete` it would DELETE what the carve-out just deployed, in the same run. Both blocks are small, local, and modeled on the existing `githooks` special-case shape (L1527-1550, a hard-coded block — confirmed NOT a generic mechanism this rev, so RELOCATE would ALSO need a new block; Option C is not uniquely special-cased). The `custom-` prefix convention (L1724-1726) is the in-tree precedent for "a skills/ subdir the substrate tools deliberately skip" — the carve-out is the same shape for two named dirs.

   > **Why not rename the dirs to `custom-check-*` to reuse the existing prune skip for free?** Rejected: `custom-` is the operator-owned namespace; substrate-shipped tools must not masquerade as operator-custom (it would make them invisible to the substrate's own staleness tooling and muddy the base-vs-custom invariant, op-disc §23). A named two-dir carve-out is honest about what these are: substrate-shipped operator tools that are not model-invoked skills.

5. **Option C makes F3 and F4 MOOT** (no path change → hook path unchanged, all 74 refs stay valid) and closes the trap identically (gen-data L100-101). It is strictly lower-risk than RELOCATE on every axis except "number of small install.sh blocks" (2 vs 1), and that one axis is a wash against RELOCATE's 74-ref sweep + F2 surgery.

### 4.3 The install.sh carve-out (spec for ADA — the two blocks)

**Block 1 — deploy carve-out (after the L1241 SKILL_NAMES loop, step 5):** a named array `CARVEOUT_SKILL_DIRS=(check-substrate-updates check-bw-release)` and a small loop that `cp -R`'s each from `${SRC_SKILLS_DIR}/${d}` → `${DEST_SKILLS_DIR}/${d}` (same `rm -rf` pre-prune + `__pycache__` cleanup the main loop uses), guarded by `[ -d "${SRC_SKILLS_DIR}/${d}" ]`. Deploys at project + user + **subproject** tiers (the check tools are workspace-local operator tooling, same as skills — subproject loads from the active project's `.claude/skills/`, L1233). Dry-run prints `[dry-run] deploy operator-tool (carve-out, non-SKILL_NAMES): …/check-*/ -> …/.claude/skills/check-*/`.

**Block 2 — prune-scan exemption (inside the L1712 skills obsolete scan):** extend the `custom-*) continue ;;` case (L1724) with the two carve-out names: `check-substrate-updates|check-bw-release) continue ;;` — so the obsolete scan never flags them. A header CITE explains: these are substrate-shipped operator tools deployed by the Block-1 carve-out, intentionally not in SKILL_NAMES, not custom — skipped by the same mechanism as `custom-*`.

**Source-side validation:** the carve-out dirs are NOT in `SKILL_NAMES`, so the L825-826 hard-abort (`err` on a SKILL_NAMES entry missing SKILL.md) does NOT fire for them — which is exactly why they must leave SKILL_NAMES (a SKILL_NAMES entry with no SKILL.md aborts install.sh; verified L826 this rev). The carve-out has no SKILL.md requirement.

### 4.4 Fallback: §4-RELOCATE (fully specified, if the floor-manager HOLDS GATE-3)

If the floor-manager, seeing this evidence, still elects §4-RELOCATE (e.g. judges a `substrate/skills/` dir-that-isn't-a-skill an unacceptable smell regardless of cost), the RELOCATE spec is: move both dirs `substrate/skills/check-*/` → `substrate/maintenance/check-*/`; ADD an install.sh `maintenance/` deploy block (project+user tiers, mirroring githooks' conditional shape) → consumer `.claude/maintenance/check-*/`; **FIX F2** by re-anchoring both check.sh state/registry computations off an explicit `--workspace`/env path instead of `SCRIPT_DIR/../..` (so the anchor survives the depth change) AND rewrite bw-upgrade.md's "two levels above this script" prose; **FIX F3** by pointing the hook at `.claude/maintenance/check-*/check.sh` (+ substrate-tier fallback); and execute the full 74-ref XREF sweep across BOTH substrate/ + .claude/ copies as the named fix-now, with the XREF probe as the dangling-ref backstop (acknowledging it does not catch semantically-wrong-but-present refs). I do NOT recommend this; I spec it so the floor-manager's gate has a complete alternative to hold.

### 4.5 The decision I am asking the floor-manager to make

Option C vs §4-RELOCATE is a **scope/smell tradeoff the directive delegated to the floor-manager**, and I have new evidence that bears on it. I have written rev2 around Option C (my recommendation) so ADA has a buildable artifact, and fully specced §4-RELOCATE (§4.4) so the floor-manager can hold GATE-3 with a complete alternative. **This is a substance disagreement with GATE-3, surfaced once with full evidence (autonomous-mode escalation discipline, op-disc §10).** I am NOT proceeding to ADA on Option C without the floor-manager's re-ratification of the mechanism — the design-lock re-surface the floor-manager already scheduled is exactly where this resolves.

---

## §5 Self-assessed weak points (for ARGUS)

1. **The carve-out is TWO install.sh special-cases, and special-cases accrete.** Option C adds a deploy carve-out AND a prune-exemption — two hard-coded references to two named dirs. If a third operator-tool-that-isn't-a-skill ever appears, this pattern invites a third pair of edits rather than a generic mechanism. **Why this shape anyway:** a generic "non-skill operator-tools deploy" mechanism is real pass-B-or-later scope (it would touch the deploy loop, the prune scan, AND the gen-data adapter's discovery contract); for two named dirs in a housekeeping pass A, two small modeled-on-githooks blocks are the proportionate cost, and they are far cheaper + lower-risk than RELOCATE's 74-ref sweep. **What I want ARGUS to scrutinize:** is the two-special-case cost genuinely smaller-risk than RELOCATE's one-block-plus-74-ref-sweep, or am I trading a visible mechanical sweep for a subtler "skills/ dir that isn't a skill" debt that bites later?

2. **Option C departs from the floor-manager's GATE-3 §4-RELOCATE decision.** I am recommending against a call the floor-manager already made and ratified. If my blast-radius/F2 evidence is somehow wrong (e.g. many of the 74 refs are name-only and survive a move trivially, shrinking RELOCATE's real cost), the departure is unjustified and re-litigates a settled call. **Why this shape anyway:** the floor-manager EXPLICITLY invited an L1241 correction that "may change the cheapest mechanism," and the GATE-3 call was made on the stated premise that "NEITHER option is complete" — my recon found a third complete option that is cheaper, which is exactly the input the floor-manager asked for. I surface it as a recommendation + a fully-specced RELOCATE fallback, not a unilateral build. **What I want ARGUS to scrutinize:** is my 74-ref count a fair measure of RELOCATE's real blast radius (path-bearing vs name-only refs), and does Option C's "skills/ dir that isn't a skill" smell actually outweigh RELOCATE's mechanical churn? This is the single judgment call I am least sure of.

3. **F1 reader depends on the Stop hook being ARMED at consumer tier.** The Stop-hook `reason` reader (§2.8) is the GUARANTEED non-additionalContext carrier — but the Stop hook is INERT until an operator runs `--enable-hooks`. On an unarmed consumer, the Stop reader does nothing, and the F1 guarantee falls to the CLAUDE.md line alone. **Why this shape anyway:** the CLAUDE.md line is a real second carrier that works hooks-unarmed (the agent reads CLAUDE.md regardless), so "never additionalContext ALONE" holds in BOTH states — armed (Stop reader, strongest) and unarmed (CLAUDE.md line). The directive's P-FALLBACK names "the Stop self-check and/or CLAUDE.md" — I wire BOTH, deliberately, to cover both arming states. **What I want ARGUS to scrutinize:** is a CLAUDE.md instruction a "RELIABLE carrier" by the directive's standard, or does the directive intend a mechanical (hook) carrier such that the unarmed-consumer case is an unmet gap? If ARGUS judges CLAUDE.md insufficient, the residual is "F1 is only fully met where hooks are armed."

4. **P-EMPIRICAL's deterministic surface assumes `--debug hooks` / transcript JSONL expose the injection on v2.1.170.** ARGUS asserted both surfaces exist; I have NOT run them on this exact build. If neither the debug stderr nor the transcript records the additionalContext payload in a greppable form, VERA falls back to the soft model-echo (which ARGUS already flagged as soft). **Why this shape anyway:** the transcript-JSONL surface is the more portable of the two and is standard Claude Code session-record behavior; specifying BOTH surfaces with an OR gives VERA two deterministic shots before the soft fallback. **What I want ARGUS to scrutinize:** is there a known v2.1.170 form of `--debug` that VERA should be told to use explicitly (flag form), so the deterministic assertion doesn't degrade to the soft one in practice?

---

## §6 Out of scope (carried from rev1 §6, unchanged)

- **Pass B (Arc 64):** modules port (`save-verdict`/`validate-spec`/`inspect-script-output`), save-verdict Bash-only rewrite, no-Write review-seat tension. A generic "non-skill operator-tools deploy mechanism" (the principled replacement for the §4.3 two-block carve-out) is pass-B-or-later scope, not pass A.
- **`credential-discipline`** — stays in `SKILL_NAMES` (deferred per directive).
- **Arming any hook** — no `--enable-hooks` on any live workspace; the candidate registration + the §2.8 Stop-hook edit deploy INERT. Out of scope by HARD CONSTRAINT.
- **The compact-reprime hook** — untouched; only a NEW `startup|resume` entry is added to the SessionStart array.
- **bw / GitHub release endpoint changes** — the check.sh upstream coupling is unchanged; this arc deletes their SKILL.md and adds a deploy carve-out, it does not modify their check logic.
