# Arc 63 pass A — design-rev1 (DAEDALUS)

**Ticket:** `stoa--p41.2` (epic; pass A). **Directive:** `substrate/arcs/arc-63-build-directive.md` (NOMOS-CONFORMANT @ b5de0aa). **Author of this design:** Denson Smith (the PRINCIPAL). **Builds against:** main `b5de0aa` (the worktree base).

---

## §1 Problem restatement

Move the two on-demand "check" skills — `check-substrate-updates` and `check-bw-release` — off the orchestrator skill-menu (`install.sh` `SKILL_NAMES`) onto a **deterministic SessionStart `type:"command"` trigger** that runs their CHECK logic once per session-start under disposition-#2 guardrails (THROTTLE ~once/day per workspace, SURFACE-ON-SIGNAL-ONLY, NON-BLOCKING/fail-open), surfacing drift via `additionalContext` *and* a robust P-FALLBACK signal-file; and in the same `install.sh`/`SKILL_NAMES` pass **port the `gauntlet-setup` skill into the substrate**. Keep the Stoa app green, doc-fix the stale "no fix through v2.1.150" SessionStart note, and make it structurally impossible for any build step to write a live `settings.json` (arming stays the operator-gated, default-OFF `--enable-hooks`).

**Imported assumptions (named, per §6.1):**

- **A1 — `check.sh` CHECK logic is reusable as-is by the hook.** Both `check.sh` scripts already (a) exit 0 always, (b) treat drift as informational, (c) locate their own state file two dirs above the script, (d) fail soft on network error. The hook *invokes* them; it does not reimplement them. This assumption is what makes the apply/revert decision (§4) load-bearing: if the check.sh scripts must keep existing on disk to be invokable, the directory they live in must keep existing.
- **A2 — "Retire from the menu" ≠ "delete the capability."** The directive says remove the 2 names from `SKILL_NAMES`. It does NOT say delete the drift-application capability (`apply.sh`/`revert.sh`), which §4 confirms is referenced as load-bearing base-team-sync canon. The restatement scopes #2 as *demote the menu entries, preserve the operator capability*.
- **A3 — both `substrate/` SOURCE and `.claude/` SELF-DEPLOYED copies are in scope.** the-stoa dogfoods its own substrate: every hook / template / README exists as a SOURCE copy (`substrate/...`, glob-discovered/deployed by `install.sh`) AND a self-deployed copy (`.claude/...`). A change that touches only the source copy leaves the repo's own dogfood inconsistent. Every file edit below names both copies.

---

## §2 Approach

### 2.0 The source/deployed duality (governs every file below)

| Artifact | SOURCE copy (deploy origin) | SELF-DEPLOYED copy (the-stoa dogfood) |
|---|---|---|
| SessionStart hook script | `substrate/hooks/sessionstart-substrate-check.sh` (NEW) | `.claude/hooks/sessionstart-substrate-check.sh` (NEW) |
| settings-hooks.json | `substrate/templates/settings-hooks.json` | `.claude/templates/settings-hooks.json` |
| hooks README | `substrate/hooks/README.md` | `.claude/hooks/README.md` |
| gauntlet-setup skill | `substrate/skills/gauntlet-setup/SKILL.md` (NEW) | (deployed by a future `install.sh` run — NOT hand-mirrored; the-stoa does not self-deploy `.claude/skills/gauntlet-setup` in this arc unless ADA runs install; see §2.5 note) |
| install.sh | `substrate/install.sh` | (no self-deployed copy — `install.sh` is the deployer, not a deployed artifact) |

ADA must edit BOTH copies of the hook script, settings-hooks.json, and the README (verbatim-identical, byte-for-byte — confirm with `diff`). Hooks are GLOB-discovered from `substrate/hooks/*.sh` (`install.sh` L170-171), so the NEW hook needs **no `install.sh` edit to be deployed** — but it DOES need the registration entry added to the candidate `settings-hooks.json` (the candidate is what `--enable-hooks` would later merge).

### 2.1 Deliverable #1 — the SessionStart trigger

**New file:** `substrate/hooks/sessionstart-substrate-check.sh` (+ identical `.claude/hooks/` copy). Mirrors `sessionstart-compact-reprime.sh`'s contract: reads the hook event on stdin via `_hooklib.sh`, emits at most one `hookSpecificOutput.additionalContext` JSON object to stdout, FAIL-OPEN (emits nothing on any error). It does NOT block boot.

**Matcher:** `startup|resume` (NOT `compact` — `compact` is the post-compaction matcher whose `additionalContext` is the still-broken path per #15174; `startup`/`resume` is the supported path, gsearch-confirmed 2026-06-17). Registered as a SECOND object in the existing `SessionStart` array (the `compact` reprime entry stays untouched).

**Logic flow (pseudocode — fail-open at every step):**

```
set -uo pipefail
HOOK_DIR=$(resolve self) || exit 0
. "$HOOK_DIR/_hooklib.sh" 2>/dev/null || exit 0
read_stdin_event
CWD=$(event_field cwd) || CWD=""
[ -n "$CWD" ] || exit 0                      # no workspace -> nothing to check, FAIL-OPEN

# ---- THROTTLE (disposition-#2): cache ~once/day per workspace ----
# NB: .substrate-last-check is ALREADY OWNED by check-substrate-updates/check.sh
# (its own per-workspace state file). The hook MUST use a DISTINCT name to avoid
# corrupting that state. Use .substrate-check-hook-stamp (NEW, hook-owned).
STAMP="$CWD/.claude/.substrate-check-hook-stamp"   # hook-owned throttle stamp (NOT check.sh's state file)
if [ -f "$STAMP" ] && find "$STAMP" -mtime -1 ... matches; then
    # checked within last ~24h -> re-surface the SIGNAL FILE if it still says drift,
    # but do NOT re-run the (network) check. (silent if no signal file present.)
    emit_from_signal_file_if_present "$CWD"   # P-FALLBACK re-surface, cheap
    exit 0
fi

# ---- run the checks (NON-BLOCKING: each backgrounded with a hard timeout,
#      output captured, never allowed to hang boot) ----
SUB_OUT=$(timeout 10 "$CWD/.claude/skills/check-substrate-updates/check.sh" --workspace "$CWD" 2>/dev/null) || SUB_OUT=""
BW_OUT=$(timeout 10  "$CWD/.claude/skills/check-bw-release/check.sh" 2>/dev/null) || BW_OUT=""
#  NOTE: at SUBSTRATE-tier (the-stoa itself) the check.sh paths are
#  substrate/skills/<name>/check.sh; at CONSUMER tier they are
#  .claude/skills/<name>/check.sh. The hook resolves BOTH candidate paths
#  and uses whichever exists (see §4 — this is the load-bearing reason the
#  check.sh scripts must keep existing at a STABLE deployed path).
touch "$STAMP" 2>/dev/null || true            # update throttle stamp regardless of result

# ---- classify drift (SURFACE-ON-SIGNAL-ONLY) ----
DRIFT_LINES=""
echo "$SUB_OUT" | grep -q 'DRIFTED\|MISSING\|OBSOLETE'  && DRIFT_LINES+="substrate drift: run check-substrate-updates/check.sh --workspace . to see it; apply via apply.sh\n"
echo "$BW_OUT"  | grep -q 'NEW BW RELEASE DETECTED'      && DRIFT_LINES+="new bw release: see check-bw-release/check.sh output; classify per op-disc §22\n"

if [ -z "$DRIFT_LINES" ]; then
    rm -f "$CWD/.claude/.substrate-drift-signal" 2>/dev/null   # clear stale signal
    exit 0                                    # SILENT WHEN CURRENT — emit nothing
fi

# ---- drift found: write the P-FALLBACK signal file FIRST (robust carrier) ----
write_signal_file "$CWD/.claude/.substrate-drift-signal" "$DRIFT_LINES"

# ---- then surface via additionalContext (primary, now-working carrier) ----
CONTEXT="Stoa substrate-update check (SessionStart): drift detected.\n${DRIFT_LINES}\nThis is informational, non-blocking. (WHY: the daily substrate/bw drift check ran at session start and found drift. WHAT: surface to the operator/PRINCIPAL; do not auto-apply.)"
emit_additionalContext_json "$CONTEXT"        # stdout MUST start with '{' — no debug pollution
exit 0
```

**Payload authoring rule (README §2 / op-disc §34):** the `additionalContext` and the signal-file body BOTH state WHY (the daily drift check ran and found drift) and WHAT (surface it; don't auto-apply) inline — never a bare pointer.

**stdout discipline (gsearch pitfall):** the script writes ONLY the JSON object to stdout (or nothing). Any diagnostic goes to stderr. A stray pre-`{` byte makes Claude Code treat the whole output as plain text. The `emit_*` helpers must be the only stdout writers.

**Gitignore (fix-now, both copies):** the hook writes two transients — `.claude/.substrate-check-hook-stamp` (throttle) and `.claude/.substrate-drift-signal` (P-FALLBACK signal). Both MUST be added to the `.gitignore` template's substrate-transient list (`install.sh` L566 echo + L584 literal) AND the self-deployed `.gitignore`, alongside the existing `.substrate-last-check` line, so they are never committed.

**Timeout in registration:** `30` is the default; this hook does a network check so it uses an *internal* `timeout 10` per check.sh call (bounded ≈20s worst case) and the registration `timeout` is set to `30` to leave headroom. The internal timeouts are the real NON-BLOCKING guarantee (the registration timeout is a backstop). Document this in the header, mirroring the compact hook's `timeout 10` note.

**Registration block** added to `settings-hooks.json` (both copies) — the `SessionStart` array gains a second entry:

```json
"SessionStart": [
  {
    "matcher": "compact",
    "hooks": [
      { "type": "command", "command": "{{HOOKS_DIR}}/sessionstart-compact-reprime.sh", "timeout": 10 }
    ]
  },
  {
    "matcher": "startup|resume",
    "hooks": [
      { "type": "command", "command": "{{HOOKS_DIR}}/sessionstart-substrate-check.sh", "timeout": 30 }
    ]
  }
]
```

`{{HOOKS_DIR}}` is sed-substituted at `--enable-hooks` deploy time (existing mechanism — no new substitution logic). The block deploys INERT (candidate only); nothing is armed unless an operator runs `--enable-hooks`.

### 2.2 Deliverable #2 — retire the 2 check skills from `SKILL_NAMES` (+ apply/revert fate)

**`install.sh` `SKILL_NAMES` edit (L228-239):**

BEFORE (10 entries):
```
check-substrate-updates   credential-discipline   check-bw-release
inspect-script-output   handoff-author   save-verdict   validate-spec
workflow-composer   interactive-html-preview   team-launcher
```
AFTER (9 entries — remove the two check skills, add gauntlet-setup):
```
credential-discipline   inspect-script-output   handoff-author
save-verdict   validate-spec   workflow-composer
interactive-html-preview   team-launcher   gauntlet-setup
```
Net `SKILL_NAMES`: **−2 (the checks) +1 (gauntlet-setup) = 9 entries.**

**Apply/revert fate — see §4 for the full RECOMMENDATION + rationale.** Headline: **KEEP `check-substrate-updates/` as a directory on disk (check.sh + apply.sh + revert.sh) but RELOCATE it OUT of `substrate/skills/` into a new non-skill operator-tools home `substrate/maintenance/check-substrate-updates/`**, and do the same for `check-bw-release/check.sh` → `substrate/maintenance/check-bw-release/`. This (a) preserves the operator drift-apply capability the hook + canon depend on, (b) removes both directories from `substrate/skills/` so `discoverSkillFiles` stops rendering them as LIEUTENANTs (no stale-LIEUTENANT), and (c) keeps a stable on-disk path for the hook to invoke. The hook's check.sh path resolution (§2.1) targets the relocated path.

### 2.3 Deliverable #3 — port `gauntlet-setup` into the substrate

- **Copy** `~/.claude/skills/gauntlet-setup/SKILL.md` → `substrate/skills/gauntlet-setup/SKILL.md` (verbatim).
- **Add** `gauntlet-setup` to `SKILL_NAMES` (already shown in §2.2 AFTER list).
- **Frontmatter check (done):** the source SKILL.md frontmatter is `name: gauntlet-setup` + `description: …` (no `author` field). The gen-data `skillFrontmatterSchema` is a non-strict `z.object({name, description})` — extra keys are stripped, and the `name` must equal the directory name (`gauntlet-setup` ✓). It will parse clean. (If ADA wishes to add `author: Denson Smith` for consistency with the other check skills, that is OPTIONAL and gen-data-safe — but the source has none, so verbatim copy is the lower-risk default.)
- **Dependency note (flag for ADA, not a blocker):** the ported SKILL.md references `team-launcher/launch-team.ps1`. `team-launcher` is ALREADY in `SKILL_NAMES` (kept), so the reference resolves at consumer tier. No additional port needed.

### 2.4 Deliverable #4 — keep the app green

**Finding (load-bearing):** `discoverSkillFiles` (gen-data-lib.ts:92-110) is **DIRECTORY-driven** — it renders every `substrate/skills/<name>/` containing a `SKILL.md` as a LIEUTENANT, independent of `SKILL_NAMES`. After §2.2 relocation, `substrate/skills/` loses 2 directories (the checks) and gains 1 (gauntlet-setup): net **−1** LIEUTENANT. The test assertion at `generated.test.ts:85-101` is **count-agnostic** (`expect(slot.skills.length).toBeGreaterThan(0)`) and validates per-skill shape (kebab-case name, non-empty description/body, `filename === "SKILL.md"`). gauntlet-setup satisfies every per-skill assertion.

**Exact `generated.test.ts` edits:** **NONE are required for the test to pass** — the count-agnostic assertion stays green at −1, and gauntlet-setup passes the shape checks. The honest answer to deliverable #4 is *no test edit is needed*; the build goes green via `npm run gen-data` re-deriving the roster from the post-arc `substrate/skills/` directory state.

**ONE optional clarity edit (RECOMMENDED, not required):** update the comment at `generated.test.ts:90-92` to reflect the current skill roster reality, so a future reader is not misled by the stale "agent-author retired Arc 61" note being the only roster-churn breadcrumb:

```
// Arc 17.1 made the gen-data adapter read all substrate skills as
// LIEUTENANTs. (agent-author retired Arc 61; the 2 check skills relocated
// out of substrate/skills/ to substrate/maintenance/ in Arc 63 + gauntlet-setup
// ported in; net LIEUTENANT churn handled by re-deriving from the dir.)
// Don't over-specify count — substrate may grow more.
```

The mechanical green path is: `cd app && npm run gen-data && npm run build && npm test` — gen-data re-derives `agents.ts` from the current `substrate/skills/` dir; build + test confirm no schema break and the LIEUTENANT slot stays populated. **Regen re-derives the WHOLE roster** (memory: gen-data-regen-re-derives-whole-roster) — so VERA must assert green from a FULL `npm test` run, not from "this arc edited no MAJOR/CAPTAIN file."

### 2.5 Deliverable #5 — doc-fix the stale SessionStart note

Two surfaces carry "no fix through v2.1.150":

- **`.claude/hooks/README.md` + `substrate/hooks/README.md`** (§6, and §6's table row for `sessionstart-compact-reprime.sh`).
- **`settings-hooks.json` `_comment`** (both copies) — the STAGE 2 sentence: "both ride the upstream-broken additionalContext channel (issues #55889 / #18427 / #15174; no fix through v2.1.150)".

**The fix must be SURGICAL and CORRECT (not a blanket "it's fixed now"):** the gsearch finding is that SessionStart `additionalContext` for `type:"command"` hooks in `.claude/hooks/` was FIXED post-2.1.150 for the `startup`/`resume` matchers; #55889 (PostToolUse/PreToolUse additionalContext) is STILL OPEN, and #15174 (`compact` matcher post-compaction injection) is the narrow case that may still not inject. So:

- The README §6 PostToolUse/PreToolUse paragraph stays (those channels remain best-effort — #55889 open).
- The README §6 SessionStart row gains a NOTE: "SessionStart `additionalContext` for the `startup`/`resume` matchers (the new `sessionstart-substrate-check.sh`) is a WORKING channel as of local v2.1.170 (P-EMPIRICAL probe, design-rev1 §3) — web-verified 2026-06-17 the v2.1.123 regression #55889 was fixed for `type:command` SessionStart hooks. The `compact` matcher (`sessionstart-compact-reprime.sh`) remains best-effort (#15174, post-compaction injection)."
- The `_comment` STAGE 2 sentence is amended to NARROW the broken claim to PostToolUse/PreToolUse + the compact matcher, and to note the new `startup|resume` SessionStart check rides a now-working channel backed by a P-FALLBACK signal file.

This keeps the doc HONEST: it does not over-claim that all additionalContext is fixed (it is not), it pins the working channel to the matchers the gsearch + the P-EMPIRICAL probe actually cover, and it preserves the existing best-effort caveat for the channels still broken.

### 2.6 Recompose / Checks A–E (Arc-61 lesson — confirm, don't assume)

The subproject MODULE-INLINE recompose (`install.sh` L1002+) operates on `substrate/modules/*.md` markers; its Check A global-existence set is built from `SRC_MODULES_DIR/*.md`. **This arc adds NO module** (the new hook is a `*.sh` glob artifact; the ported skill is a `substrate/skills/` dir; the relocated check tools go to `substrate/maintenance/`). No owned-module set changes. Therefore the recompose is unaffected. **CONFIRM via a REAL non-dry-run subproject recompose** (§3 probe RECOMPOSE) — a dry-run early-returns before the awk FAIL-LOUD checks (Arc-61 lesson), so the dry-run cannot prove the checks pass.

### 2.7 Module cross-reference audit (fix-now candidate)

`substrate/modules/substrate-update-check.md:12`, `bw-upgrade.md` (§22.4, lines 15/45/47/57/59), `MAJOR_POLYBIUS.md` (§14/§19/§23 refs at L512/562/624), and `operating-disciplines.md` reference the check skills by their OLD `skills/check-substrate-updates/` and `skills/check-bw-release/` paths. After the §2.2 relocation, these paths are STALE. **Fix-now:** ADA updates every cross-reference to the new `substrate/maintenance/check-substrate-updates/` (and `…/check-bw-release/`) path, in BOTH `substrate/` and `.claude/` copies. This is a named fix-now item (cost-calculus: leaving a dangling `skills/check-substrate-updates/` path in load-bearing canon is exactly the drift the substrate-update-check skill exists to catch). Enumerated for ARGUS as the highest-surface-area edit. If ARGUS judges the relocation too broad for pass A, the FALLBACK is §4-alt (keep the dirs in `substrate/skills/` and accept the stale LIEUTENANTs as a tracked ticket) — but I recommend against it (see §4).

### Threat→mitigation map

The HARD SAFETY CONSTRAINT (no live `settings.json` written) is a **ratified safety constraint** (directive §HARD SAFETY CONSTRAINT, NOMOS-CONFORMANT). Per op-disc §35.1 it is a named, ratification-point constraint, so it carries a map row:

> **M1 (live-settings.json auto-write — gate-origin, ratified)** → *attack path:* a build/install step (or the new hook registration) writes or merges the hook block into a live `.claude/settings.json`, arming PreToolUse/Stop gates into the running session and gating the running team's own operations (no-experiments-on-real-agents violation in spirit). → *how-defeated:* the new hook is a `substrate/hooks/*.sh` glob artifact + a CANDIDATE-only `settings-hooks.json` entry; arming stays the existing operator-gated `--enable-hooks` (DEFAULT OFF, `ENABLE_HOOKS=0`), and at user tier even that prints a manual-merge runbook rather than auto-writing. NO new write-path to a live settings.json is introduced. The §3 NOSETTINGS probe (a grep of the build diff) is the threat-anchored probe that exercises this attack path.

All other changes this arc are **process / tooling-housekeeping changes with no runtime attack path** → classified `not threat-ratified (process change: menu demotion + file relocation + doc-fix + app-test re-derive; no runtime attack surface)` per op-disc §35.5. ARGUS confirms this classification (I cannot self-grant the carve-out).

---

## §3 Verification probes (VERA executes verbatim)

All paths relative to the worktree root `…/arc-63-build/` unless absolute. Each probe states command + expected observable + pass/fail.

### P-EMPIRICAL — SessionStart additionalContext reaches the model on local v2.1.170 (THREAT-ADJACENT, mandatory)

The directive's load-bearing premise. Probe is a THROWAWAY-target test (no live settings.json on a canonical seat — op-disc §25.5).

1. **Confirm version:** `claude --version` → expect `2.1.170` (or note the actual). PASS criterion: record the version; the probe result is pinned to it.
2. **Build a throwaway harness:**
   ```
   TMP=$(mktemp -d); mkdir -p "$TMP/.claude/hooks"
   cat > "$TMP/.claude/hooks/probe-sessionstart.sh" <<'EOF'
   #!/usr/bin/env bash
   printf '{"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":"STOA_PROBE_SENTINEL_7F3A: if you can read this, reply with exactly the token STOA_PROBE_SENTINEL_7F3A and nothing else."}}\n'
   EOF
   chmod +x "$TMP/.claude/hooks/probe-sessionstart.sh"
   cat > "$TMP/.claude/settings.json" <<EOF
   {"hooks":{"SessionStart":[{"matcher":"startup","hooks":[{"type":"command","command":"$TMP/.claude/hooks/probe-sessionstart.sh","timeout":30}]}]}}
   EOF
   ```
   (This writes settings.json ONLY in a `mktemp` throwaway dir — NOT any canonical/live workspace. HARD CONSTRAINT respected: no canonical seat's settings.json is touched.)
3. **Fire a fresh session in the throwaway and capture the model's first reply:**
   ```
   cd "$TMP" && claude -p "What is the sentinel token in your context? Reply with only the token." --max-turns 1 2>&1 | tee /tmp/stoa-probe-out.txt
   ```
   (Use the project-tier startup path so the `startup` matcher fires. If `-p` headless does not fire SessionStart on this build, fall back to an interactive `claude` session and read the first model turn.)
4. **PASS:** the model's reply contains `STOA_PROBE_SENTINEL_7F3A` (it could only know it if `additionalContext` reached the model). **FAIL:** the token is absent → the channel does NOT work on this build → the design's primary carrier is dead and the P-FALLBACK signal-file becomes the SOLE carrier (the design still functions; this probe's failure escalates the doc-fix to "still broken" and is a finding for ARGUS, NOT a design-blocker — that is the whole point of P-FALLBACK).
5. **Teardown:** `rm -rf "$TMP"` (fixed literal-ish var bound to mktemp output; safe).

### P-FALLBACK — the drift-signal file works independent of additionalContext

1. **Run the hook script directly with a synthetic event that forces drift** (env override on the bw-release check + a synthetic substrate-drift):
   ```
   echo '{"hook_event_name":"SessionStart","source":"startup","cwd":"'"$PWD"'"}' \
     | BW_RELEASE_CHECK_LATEST_OVERRIDE=v999.0.0 BW_RELEASE_CHECK_BASELINE_OVERRIDE=v1.0.0 \
       bash .claude/hooks/sessionstart-substrate-check.sh
   ```
2. **PASS (a):** the file `.claude/.substrate-drift-signal` exists and its body names the bw drift + states WHY/WHAT inline (op-disc §34). **PASS (b):** stdout is EITHER a single valid JSON object starting with `{` (additionalContext present) OR empty — never plain-text pollution. Verify `head -c1 stdout == '{'` when non-empty.
3. **Carrier-read check:** confirm the signal file is read by a RELIABLE carrier. The carrier is **the SessionStart hook's own throttle-path re-surface** (re-emits the signal next session without re-running the network check) PLUS **CLAUDE.md guidance** — design names the throttle re-surface as the primary fallback carrier (it re-injects via additionalContext on the next start, and writes the file so an operator/CLAUDE.md-reading agent finds it on disk). PASS: a second hook run within the throttle window (stamp fresh) re-emits the signal-file body without making a network call (assert by setting `BW_RELEASE_CHECK_LATEST_OVERRIDE` to a NON-drift value on the 2nd run and confirming the signal still surfaces from the file, not from a fresh check).
4. **SILENT-WHEN-CURRENT:** run the hook with NO overrides against a current workspace (bootstrap the bw baseline first). PASS: stdout empty, no `.substrate-drift-signal` file (or it is removed). FAIL: any output when current.

### NOSETTINGS — no build step writes a live settings.json (THREAT-ANCHORED for M1)

1. `git -C …/arc-63-build diff --name-only b5de0aa..HEAD` (the arc commit). **PASS:** the changed-files list contains ONLY `substrate/hooks/…`, `.claude/hooks/…`, `substrate/templates/settings-hooks.json`, `.claude/templates/settings-hooks.json`, `substrate/install.sh`, `substrate/skills/gauntlet-setup/…`, `substrate/maintenance/…` (the relocated check tools), the module/canon cross-ref files (§2.7), the `.gitignore` template (in `install.sh`) + self-deployed `.gitignore`, `app/…` (gen-data output + optional test comment), and this design doc. **FAIL:** any `**/settings.json` (a LIVE settings.json, i.e. NOT `settings-hooks.json` and NOT inside a `templates/` candidate path) appears in the diff.
2. **(a) attack-blocked:** `grep -rn '"hooks"' --include=settings.json` over the repo (excluding `templates/`) returns NOTHING new from this arc. **(b) legit-unaffected:** `install.sh --target user --dry-run` still PRINTS the manual-merge runbook for `--enable-hooks` (the operator arming path is intact, just not auto-fired). PASS requires both halves.

### RECOMPOSE — real (non-dry-run) subproject recompose passes Checks A–E

1. Run a REAL subproject recompose against a throwaway parent:
   ```
   PARENT=$(mktemp -d); bash substrate/install.sh --target subproject --parent-dir "$PARENT" --subproject probe63
   ```
   (NOT `--dry-run` — the Arc-61 lesson: dry-run early-returns before the awk FAIL-LOUD Checks A–E.)
2. **PASS:** exit 0, no `err()` abort, the deployed role files recomposed without any "marker/module mismatch" failure. **FAIL:** any non-zero exit or FAIL-LOUD Check abort. Teardown `rm -rf "$PARENT"`.

### APPGREEN — the Stoa app stays green

```
cd app && npm run gen-data && npm run build && npm test
```
**PASS:** gen-data exits 0 (no skill-frontmatter validation error on gauntlet-setup; no name/dir mismatch), build exits 0, ALL tests pass (FULL suite — assert from the full run, not "this arc edited no X"; memory: gen-data-regen-re-derives-whole-roster). The LIEUTENANT test stays green at the −1 count. **FAIL:** any non-zero, or the LIEUTENANT slot empties, or a gauntlet-setup shape assertion fails.

### SKILLNAMES — SKILL_NAMES net −2 +1

`grep -A12 'SKILL_NAMES=(' substrate/install.sh`. **PASS:** 9 entries; `check-substrate-updates` and `check-bw-release` ABSENT; `gauntlet-setup` PRESENT; `team-launcher` still present (gauntlet-setup's dependency). **FAIL:** either check skill still listed, or gauntlet-setup missing, or count ≠ 9.

### LANDING — gauntlet-setup deploys to a consumer .claude/skills

`install.sh --target project --project-dir "$TMP_CONSUMER" --dry-run` → grep stdout for `deploy skill: …/gauntlet-setup/`. **PASS:** the dry-run plans the gauntlet-setup deploy AND does NOT plan a `check-substrate-updates`/`check-bw-release` skill deploy. **FAIL:** gauntlet-setup absent, or a retired check skill still planned for deploy.

### NOSTALE-LIEUTENANT — no half-retired skill dir

`ls substrate/skills/` → **PASS:** no `check-substrate-updates/` and no `check-bw-release/` directory present (they moved to `substrate/maintenance/`); `gauntlet-setup/` present. Confirms `discoverSkillFiles` cannot render a stale check LIEUTENANT. **FAIL:** either check dir still under `substrate/skills/`.

### GITIGNORE — hook transients are ignored

`grep -n 'substrate-check-hook-stamp\|substrate-drift-signal' substrate/install.sh .gitignore`. **PASS:** both names appear in the `install.sh` gitignore template (the echo at ~L566 + the literal list at ~L584) AND in the self-deployed `.gitignore`. Also `git status --porcelain` after a hook run shows NO untracked `.substrate-check-hook-stamp`/`.substrate-drift-signal`. **FAIL:** either transient is committable.

### XREF — no dangling skill-path reference after relocation

`grep -rn 'skills/check-substrate-updates\|skills/check-bw-release' substrate/ .claude/ --include='*.md'` (excluding `substrate/arcs/` historical directives + this design doc). **PASS:** no live canon (modules, MAJOR_POLYBIUS, op-disc, README) still points at the old `skills/` path. **FAIL:** any load-bearing canon file still names the old path.

---

## §4 Apply/revert fate — RECOMMENDATION (the headline design-lock)

**RECOMMENDATION: KEEP `apply.sh` + `revert.sh` (and both `check.sh` scripts) as a live operator capability, but RELOCATE the two skill directories OUT of `substrate/skills/` into a new non-skill home `substrate/maintenance/` — `substrate/maintenance/check-substrate-updates/{check.sh,apply.sh,revert.sh}` and `substrate/maintenance/check-bw-release/check.sh`. Do NOT fold or delete.**

**Rationale:**

1. **The capability is load-bearing canon, not a menu convenience.** `apply.sh`/`revert.sh` are the substrate's **base-team-sync mechanism**: `MAJOR_POLYBIUS.md` §14/§19/§23 + `operating-disciplines.md` §22/§23 + `modules/substrate-update-check.md` all name `check-substrate-updates`'s `check.sh`/`apply.sh`/`revert.sh` as the canonical drift-detect-and-apply tools that keep every consumer's BASE team in sync. Folding/dropping them would silently delete a capability the directive explicitly says NOT to drop, and orphan the canon that depends on it.
2. **The hook needs the check.sh on disk at a stable path.** The SessionStart trigger INVOKES `check.sh` (§2.1 — it does not reimplement the drift logic). The script must keep existing at a stable, deployable path. Folding the logic into the hook would (a) duplicate ~45KB of drift-detection logic, (b) lose the operator's on-demand `check.sh --workspace X` ability, and (c) lose apply/revert entirely.
3. **Relocation (not "leave in skills/") is required to avoid the stale-LIEUTENANT trap.** `discoverSkillFiles` is DIRECTORY-driven (POLYBIUS design-attention, gen-data-lib:92-110). Leaving `check-substrate-updates/` under `substrate/skills/` after removing it from `SKILL_NAMES` produces a HALF-RETIRED skill: gen-data still renders it as a LIEUTENANT (reads the source dir), but `install.sh`'s deploy loop (L1241) skips it (not in `SKILL_NAMES`) — the app shows a skill the substrate no longer deploys. Relocating the dir to `substrate/maintenance/` removes it from gen-data's discovery scope cleanly. The −1 net LIEUTENANT delta the directive states HOLDS exactly under this relocation.
4. **`substrate/maintenance/` has a precedent.** `substrate/githooks/` is already a non-skill operator-script directory that `install.sh` handles specially (candidate-only deploy). `substrate/maintenance/` is the same shape: operator-run tooling, not a model-invoked skill, not a gen-data LIEUTENANT.

**The cost of this recommendation (named honestly):** it touches more files than a bare `SKILL_NAMES` edit — it adds an `install.sh` deploy path for `substrate/maintenance/` (so the relocated tools still reach consumers) and rewrites ~6 canon cross-references (§2.7). That is the highest-surface-area part of pass A. **If ARGUS / the floor-manager judges that too broad for a "housekeeping pass A,"** the documented FALLBACK (§4-alt) is: keep the two dirs in `substrate/skills/` but REMOVE only their `SKILL.md` files (gen-data skips a dir with no SKILL.md — gen-data-lib:100-101 `if (!fs.existsSync(skillMdPath)) continue`), leaving `check.sh`/`apply.sh`/`revert.sh` in place. That is a SMALLER diff (no relocation, no install.sh deploy-path add, fewer xref edits) and ALSO avoids the stale LIEUTENANT — but it leaves orphaned skill dirs (a dir under `skills/` that is not a skill) which is its own smell. **I recommend the relocation; I name §4-alt so the floor-manager can choose the smaller diff if pass-A scope discipline outweighs the tidiness.** This is the explicit design-lock decision for the floor-manager.

---

## §5 Self-assessed weak points (for ARGUS)

1. **P-EMPIRICAL headless-mode uncertainty.** The probe fires `claude -p … --max-turns 1` to capture the model's first reply and assert the sentinel reached it. I am NOT certain `-p` headless mode fires the `SessionStart:startup` hook on v2.1.170 (some headless paths may skip SessionStart). The probe names an interactive fallback, but VERA may need to adapt the exact invocation. **What I want ARGUS to scrutinize:** is there a more deterministic way to assert additionalContext reached the model than reading a sentinel token out of a model reply? (e.g., is there a debug/log surface that shows the injected context?) If the probe is non-deterministic, the P-EMPIRICAL "green" is soft.

2. **The relocation's blast radius vs pass-A scope.** §4's relocation rewrites ~6 load-bearing canon cross-references (modules, MAJOR_POLYBIUS, op-disc) AND adds an `install.sh` deploy path for `substrate/maintenance/`. That is a bigger diff than "housekeeping pass A" implies, and each cross-ref edit is a chance to miss one (the XREF probe catches dangling refs, but a SEMANTICALLY-wrong-but-syntactically-present ref could slip). **What I want ARGUS to scrutinize:** is the relocation worth its blast radius, or is §4-alt (delete only the SKILL.md files, leave the dirs as orphans under skills/) the right pass-A-scoped call? This is the single judgment call I am least sure of.

3. **Throttle stamp collision — FOUND AND RESOLVED in design; ADA must wire the gitignore.** My first draft named the hook throttle stamp `.substrate-last-check` — which is ALREADY OWNED by `check-substrate-updates/check.sh` (verified: that script's `sf="${ws}/.claude/.substrate-last-check"`, L662). A shared name would corrupt one of the two. RESOLVED: the hook uses `.claude/.substrate-check-hook-stamp` (hook-owned, distinct). **Residual ADA action (fix-now):** `.substrate-last-check` is in the `.gitignore` template (install.sh L584) but `.substrate-check-hook-stamp` is NOT — ADA must add it to the gitignore template's substrate-transient list (L566/L584) in BOTH source and the self-deployed `.gitignore`, else the stamp gets committed as repo noise. **Scrutinize:** confirm no OTHER hook-written transient (the signal file `.substrate-drift-signal`) also needs a gitignore line — it does; add both `.substrate-check-hook-stamp` and `.substrate-drift-signal`.

4. **Doc-fix correctness (over-claim risk).** §2.5 deliberately does NOT say "additionalContext is fixed" — it narrows the working claim to SessionStart `startup|resume` and keeps the best-effort caveat for PostToolUse/PreToolUse (#55889 open) + the compact matcher (#15174). If the P-EMPIRICAL probe FAILS, the doc-fix as written would be WRONG (it would claim a working channel that isn't). **Scrutinize:** the doc-fix wording must be GATED on the P-EMPIRICAL result — ADA should write it to match what VERA's probe actually shows, not what the gsearch predicted. I flag this as a sequencing dependency: doc-fix wording finalizes AFTER P-EMPIRICAL runs.

---

## §6 Out of scope (keeps ADA from scope-creep)

- **Pass B (Arc 64):** modules port (`save-verdict`/`validate-spec`/`inspect-script-output` → modules), the save-verdict Bash-only rewrite, the no-Write review-seat tension. Untouched here.
- **`credential-discipline`** — stays in `SKILL_NAMES` unchanged (deferred per directive).
- **Arming the hooks** — no `--enable-hooks` run on any live workspace; the candidate registration deploys INERT. Out of scope by HARD CONSTRAINT.
- **The compact-reprime hook** — untouched. Only a NEW `startup|resume` entry is added to the SessionStart array.
- **bw / GitHub release endpoint changes** — the check.sh scripts' upstream coupling (cite-comments) is unchanged; this arc moves them, it does not modify their logic.
