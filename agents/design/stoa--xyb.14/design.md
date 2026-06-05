---
ticket: stoa--xyb.14
arc: Arc C — encode batch (operating-disciplines.md §7/§11/§13/§28)
seat: CAPTAIN_DAEDALUS (ARCHITECT)
author: Denson Smith
operating-mode: autonomous
threat-classification: LIVE (ships runtime mechanism — §28 git hook executes shell at commit time)
consumes: agents/research/arc-C-hook-capabilities/findings.md (STRABO) + docs/debloat-decisions.md (LOCKED ledger) + bw stoa--w6d
---

# Arc C — encode batch design

## Problem restatement (§6.1 pre-work gate)

Encode four mechanical operating-disciplines into *running structures* (a settings env block / a git hook / cron templates) and slim each prose section to a STUB that points at its mechanism — preserving the discipline's *effect* (lossless-on-judgment) while removing the prose that merely *describes* a mechanism an executable can carry. This is a PARTIAL encode: the mechanism moves to a running structure; the judgment prose stays.

**Imported assumption I must name (this is a brief-bug-adjacent finding, surfaced not smoothed):** the brief frames all four (§7, §11, §13, §28) as new-encode work. Grounding against the live worktree shows **§7 and §11's cron mechanisms are ALREADY ENCODED** — Arc 47 relocated §7→`modules/two-polybius-coordination.md` and §11→`modules/autonomous-mode-setup.md`, AND the cron machinery already runs as `templates/polling-cron-prompt-template.md` (STEP 1.5 author-attribution, STEP 4 cadence-switch lock-step renewal rotation) + the renewal-cron machinery inline in the autonomous-mode-setup module. The 7-day-expiry / +144h renewal / jitter / no-catch-up / `durable`-inert caveats the brief asks me to "bake in" are **already baked in and already STRABO-consistent**. The op-disc §7/§11 sections are **already slim stubs** pointing at those modules+template. So for §7/§11 the Arc C work is **verify-already-encoded + confirm no dangling pointer + (optionally) tighten the stub's mechanism-pointer**, NOT a fresh encode. The genuinely-new encode work is **§13 (settings env block)** and **§28 (prepare-commit-msg git hook)**. I designed all four; §7/§11 land as a no-op-with-verification rather than a re-encode (re-encoding a working running structure would be churn that risks the redundant-checker property the gauntlet exists to protect).

If ARGUS or PLINY judges the brief intended a *different* §7/§11 mechanism than the one Arc 47 already shipped, that is the load-bearing divergence to resolve before ADA builds — see `residual_questions_for_argus`.

---

## §1 — Scope + per-section encode plan (mechanism + exact slimmed stub text)

Two encode KINDS ship in this arc, and they MUST NOT be conflated (the single most important structural boundary in this design):

- **Claude-Code settings layer** (§13 env block): a `.claude/settings.json` `env` block. Deployed by `install.sh`. Fired by Claude Code at session start; applies to every spawned subprocess incl. the Bash tool. NO code-execution-at-config-time surface.
- **git layer** (§28 trailer): a `.git/hooks/prepare-commit-msg` shell script. Deployed *as a candidate script* by `install.sh` to `<dest>/.claude/githooks-candidate/`, opt-in-installed per-clone. Fired by *git itself* at commit time. EXECUTES SHELL at every commit → the LIVE attack surface (see §6).

These are different layers, different fire-triggers, different deploy locations, different default-OFF mechanisms. They are NOT the existing `.claude/hooks/*.sh` Claude-Code enforcement hooks (PreToolUse/Stop) — those are a third, separate thing the §28 git hook must not be merged into.

### §13 — Windows PYTHONUTF8 → settings.json `env` block

- **Mechanism:** a `.claude/settings.json` `env` block carrying `"PYTHONUTF8": "1"` (and `"PYTHONIOENCODING": "utf-8"` as belt-and-suspenders). Per current docs (https://code.claude.com/docs/en/settings, re-fetched 2026-06-04): *"Environment variables applied to every session and to subprocesses Claude Code spawns from it."* The Bash tool is such a subprocess → PYTHONUTF8 reaches every Python invocation with zero per-script discipline and zero failure surface. NOT a SessionStart additionalContext emit (sets no env var — the silent-inert trap STRABO Claim 1/2 flags) and NOT a CLAUDE_ENV_FILE SessionStart hook (works, but adds a fail-open hook surface and STRABO flags unconfirmed Windows `export`-syntax parsing — the env block sidesteps both).
- **Slimmed §13 stub text (exact — replaces the current §13 body lines ~529–539):**

  > ## 13. Windows Python environment — PYTHONUTF8 via the settings `env` block
  >
  > Agent-authored helper Python scripts on Windows default to `cp1252` stdout; printing non-ASCII (Greek theta in PDFs, em-dashes, accented citations) crashes with `UnicodeEncodeError`. The substrate fix is a `.claude/settings.json` **`env` block** carrying `PYTHONUTF8=1` (+ `PYTHONIOENCODING=utf-8`), which Claude Code applies to every session and every spawned subprocess including the Bash tool (https://code.claude.com/docs/en/settings, "env" key) — so every Python invocation gets UTF-8 stdout with no per-script discipline. `install.sh` deploys this env block (merged into an existing `settings.json` only with explicit operator consent; otherwise emitted as a candidate + runbook — same default-OFF posture as the enforcement-hook arming, since `settings.json` is operator-owned config). Mechanism + deploy wiring: `substrate/templates/settings-env-block.json` + `install.sh` step 5e. **Residual judgment (kept prose):** the per-machine `setx PYTHONUTF8 1` (PRINCIPAL handles, one-time, covers non-Claude invocations too) and the in-code `sys.stdout.reconfigure(encoding='utf-8')` for shipped CLI binaries (e.g. `ariadne--sh7`) remain complementary — the env block covers Claude-spawned subprocesses; the per-machine + in-code fixes cover invocations outside a Claude session. Detection: `os.name == 'nt'` or PRINCIPAL-flagged Windows deployment. Empirical anchor: `stoa--a5q` (recover via `bw show`).

  Lossless-on-judgment check: the kept prose preserves the per-machine fix + in-code fix + detection + anchor (the *judgment* about WHEN/WHERE each applies). Only the "per-script set PYTHONUTF8 in the bash environment for the invocation" mechanical prose is replaced by the env-block mechanism (the env block makes per-script setting unnecessary inside a Claude session).

### §28 — git seat-identity Co-Authored-By trailer → prepare-commit-msg hook

- **Mechanism:** a `prepare-commit-msg` git hook (candidate script `substrate/githooks/prepare-commit-msg`) that appends the seat trailer via `git interpret-trailers --if-exists=addIfDifferent` and **exits 0 unconditionally** (fail-open). Default-OFF / opt-in: deployed as a *candidate* to `<dest>/.claude/githooks-candidate/prepare-commit-msg`, never auto-installed into any `.git/hooks/`. The seat name is sourced from a session env var (`STOA_SEAT_TRAILER`, set by the seat's activation — coordinates with stoa--w6d, see below); when unset the hook is a clean no-op (still exit 0).
- **Relationship to existing canon (load-bearing — the hook AUGMENTS, does not REPLACE):** §28's trailer is *today* written by hand — ADA writes it verbatim in the commit HEREDOC (`CAPTAIN_ADA.md` §5.5 / :102–108), dispatched by PLINY's brief as a `seat-identity:` field (`MAJOR_PLINY.md` §5.12). That manual discipline STAYS canon. The hook is an *opt-in safety-net* that catches a *missed* trailer; `--if-exists=addIfDifferent` makes it idempotent so it never double-writes a trailer ADA already wrote. The hook does not relax ADA's pre-commit discipline.
- **Slimmed §28.1 stub text (exact — the mechanical trailer-format + worked-examples prose at §28.1 lines ~1133–1148 slims; §28.2–§28.8 judgment prose STAYS; §28.5 STAYS PROSE in full):**

  > ### 28.1 The trailer format + the optional prepare-commit-msg backstop
  >
  > The trailer is `Co-Authored-By: CAPTAIN_<MNEMONIC>_<project-slug> <captain-<mnemonic>@<project-slug>.local>` — name field binds seat-mnemonic + project-slug; email local-part lowercase-hyphen; `.local` TLD (RFC 6762 link-local, non-routable, GitHub renders as text not a fake avatar). ADA writes it verbatim in the commit HEREDOC per `CAPTAIN_ADA.md` §5.5, dispatched by `MAJOR_PLINY.md` §5.12. **Optional backstop:** an opt-in `prepare-commit-msg` git hook (candidate at `substrate/githooks/prepare-commit-msg`, deployed default-OFF by `install.sh` to `<dest>/.claude/githooks-candidate/`, never auto-armed) appends the trailer idempotently via `git interpret-trailers --if-exists=addIfDifferent`, sourcing the seat from the `STOA_SEAT_TRAILER` session env var and **exiting 0 unconditionally** (fail-open — a buggy hook can never abort a commit; `prepare-commit-msg` is NOT suppressed by `--no-verify`, so fail-open is mandatory). The hook is a safety-net for a *missed* manual trailer, not a replacement for the ADA discipline; it never touches `Author:` (stays PRINCIPAL's per the absolute rule). Coordinates with `stoa--w6d` (committer sub-identity): the hook writes the *trailer*; w6d sets the *committer* — the trailer is the squash-merge-surviving signal (§28.3), the committer is the git-blame-readable signal. Mechanism + deploy wiring: `substrate/githooks/prepare-commit-msg` + `install.sh` step 5f.

  (Worked-examples block at §28.1 — the three `Co-Authored-By: CAPTAIN_*_the-stoa` literal lines — moves into the hook script's header comment as the canonical examples + stays as one compact example line in the stub. Lossless: the format spec is preserved; the mechanism now carries the worked examples.)

  **§28.5 STAYS PROSE UNCHANGED** (do-not-infer-authorship from git blame). It is the reading-side authorship-attribution judgment discipline — cannot be a hook (it governs how a *reader* interprets blame output, there is no commit-time mechanism for it). Verbatim-preserved.

### §7 — POLYBIUS-coordination recurring cron-prompt (ALREADY ENCODED — verify + tighten pointer)

- **Mechanism (already shipped, Arc 47):** `substrate/templates/polling-cron-prompt-template.md` is the reusable recurring-CronCreate prompt body for two-POLYBIUS coordination (STEP 1.5 author-attribution per §7.7; STEP 4 cadence-switch). The 7-day-auto-expiry + jitter + no-catch-up + session-scoped caveats are baked into the template's "Cron expiry handling" section + the renewal machinery (§11). `durable:true` is correctly documented as INERT (the renewal one-shot does not rely on it).
- **§7 op-disc state (already slim):** §7 is already a stub pointing at `modules/two-polybius-coordination.md`; §7.7 already cites `templates/polling-cron-prompt-template.md STEP 1.5` as the mechanical encoding. **Arc C action: no re-encode.** Verify (a) the stub→module pointer resolves; (b) §7.7→template STEP 1.5 pointer resolves; (c) the template's expiry caveats remain STRABO-consistent (they are). If ADA wants a tightening: the template's "Cron expiry handling" trailer already names the +144h renewal + the CronList-has-no-expiry-field limitation — no edit needed.

### §11 — cron machinery in the polling-cron template (ALREADY ENCODED — verify)

- **Mechanism (already shipped, Arc 47):** the renewal/expiry machinery lives in `modules/autonomous-mode-setup.md` step 1.5 (the +144h one-shot renewal cron, the 4-step setup dance, the terminating-shape) + `polling-cron-prompt-template.md` STEP 4 (cadence-switch lock-step rotation). All STRABO Claim 4 facts (session-scoped, 7d expiry, durable-inert, jitter, no-catch-up, local-tz) are already encoded as caveats/acceptances.
- **§11 op-disc state (already slim):** §11 is already a stub pointing at `modules/autonomous-mode-setup.md`. **Arc C action: no re-encode.** Verify the stub→module pointer resolves + the module→template cross-refs resolve.

---

## §2 — Each mechanism's concrete artifact (grounded in STRABO + current-doc re-confirmation)

### §13 artifact — `substrate/templates/settings-env-block.json` (NEW FILE)

```json
{
  "_comment": "CANDIDATE Stoa settings 'env' block — Windows PYTHONUTF8 fix (operating-disciplines.md §13). install.sh deploys this to <DEST>/.claude/templates/settings-env-block.json as a CANDIDATE. Merging it into a live .claude/settings.json sets these env vars for every session + every spawned subprocess incl. the Bash tool (https://code.claude.com/docs/en/settings 'env' key). Merge is operator-gated (install.sh --enable-env-block, DEFAULT OFF) and at user tier prints a manual-merge runbook (never auto-writes ~/.claude/settings.json — the running config). No code execution at config time. Cross-platform-safe: PYTHONUTF8 is a no-op on non-Windows Pythons already defaulting to UTF-8.",
  "env": {
    "PYTHONUTF8": "1",
    "PYTHONIOENCODING": "utf-8"
  }
}
```

- **Grounding:** STRABO Claim 1 (settings `env` block is the no-failure-surface primary for §13) + my re-fetch of https://code.claude.com/docs/en/settings 2026-06-04 (exact quote: "applied to every session and to subprocesses Claude Code spawns from it") + my LOCAL probe on this Windows/git env: `PYTHONUTF8=1 python -c "..."` → `enc=utf-8`, Greek theta + em-dash printed clean (the VERA falsifier STRABO named).
- **Why both vars:** `PYTHONUTF8=1` enables UTF-8 mode (covers stdout + filesystem). `PYTHONIOENCODING=utf-8` is the narrower, older mechanism — redundant belt-and-suspenders for Python versions/contexts where UTF-8 mode is partially honored. Harmless together.
- **Color caveat (docs v2.1.143+):** only `NO_COLOR`/`FORCE_COLOR` in an env block are special-cased (passed to subprocesses but don't change Claude's own UI). PYTHONUTF8/PYTHONIOENCODING are not affected — they pass through normally.

### §28 artifact — `substrate/githooks/prepare-commit-msg` (NEW FILE, candidate hook script)

```sh
#!/bin/sh
# Stoa per-CAPTAIN seat-identity trailer — prepare-commit-msg hook.
# operating-disciplines.md §28. CANDIDATE / DEFAULT-OFF / OPT-IN: install.sh
# deploys this to <dest>/.claude/githooks-candidate/prepare-commit-msg; it is
# NEVER auto-installed into any .git/hooks/. To arm per-clone, the operator
# copies it to .git/hooks/prepare-commit-msg (chmod +x) OR points
# core.hooksPath at the candidate dir. See .claude/githooks-candidate/README.md.
#
# FAIL-OPEN CONTRACT (load-bearing): this hook MUST exit 0 on EVERY path.
# prepare-commit-msg aborts the commit on non-zero exit AND is NOT suppressed
# by --no-verify (https://git-scm.com/docs/githooks, re-fetched 2026-06-04) —
# so a non-zero exit would brick EVERY commit including emergency ones. Every
# branch below ends at `exit 0`.
#
# NEVER touches Author: (stays PRINCIPAL's per the absolute never-override rule).
# Appends ONLY the Co-Authored-By trailer (metadata layer, parallel to
# CAPTAIN_ADA.md §5.5 manual discipline; this hook is the opt-in backstop).
#
# Canonical trailer examples (the-stoa project tier):
#   Co-Authored-By: CAPTAIN_ADA_the-stoa <captain-ada@the-stoa.local>
#   Co-Authored-By: CAPTAIN_DAEDALUS_the-stoa <captain-daedalus@the-stoa.local>
#   Co-Authored-By: CAPTAIN_CATO_the-stoa <captain-cato@the-stoa.local>

MSG_FILE="$1"
COMMIT_SOURCE="$2"   # message|template|merge|squash|commit|<empty>

# 1. No seat declared this session -> clean no-op (the manual ADA trailer, if
#    any, is already in MSG_FILE; we add nothing).  STOA_SEAT_TRAILER is set by
#    the seat's autonomous-mode activation (coordinates with stoa--w6d, which
#    sets GIT_COMMITTER_* + a session seat-marker). UNTRUSTED-INPUT NOTE: this
#    is a SESSION-LOCAL env var the seat sets for itself, not commit content,
#    branch name, or any attacker-supplied value (see design §6 threat map).
[ -n "$STOA_SEAT_TRAILER" ] || exit 0

# 2. Skip merge/squash sources (their bodies are machine-generated; trailer
#    preservation there is GitHub's job per §28.3, not this hook's).
case "$COMMIT_SOURCE" in
  merge|squash) exit 0 ;;
esac

# 3. Defensive: MSG_FILE must exist + be writable. If not, no-op (fail-open).
[ -n "$MSG_FILE" ] && [ -f "$MSG_FILE" ] && [ -w "$MSG_FILE" ] || exit 0

# 4. Validate the seat-trailer shape. We ONLY accept a value matching the
#    canonical Co-Authored-By: CAPTAIN_<X>_<slug> <captain-<x>@<slug>.local>
#    shape. A malformed/injected value is REJECTED (no-op) rather than passed
#    to interpret-trailers. This is the no-untrusted-input-execution mitigation:
#    the value is never eval'd, never word-split into a command, only matched +
#    handed to interpret-trailers as a single --trailer literal.
case "$STOA_SEAT_TRAILER" in
  "Co-Authored-By: "*" <"*".local>") : ;;   # shape OK
  *) exit 0 ;;                                # malformed -> no-op, fail-open
esac

# 5. Idempotent append. --if-exists=addIfDifferent: append ONLY if this exact
#    (key,value) pair is not already present anywhere in the message (so a
#    trailer ADA wrote by hand is NOT duplicated), BUT a DIFFERENT CAPTAIN's
#    trailer on the same commit IS appended (multi-CAPTAIN commits work). This
#    is why addIfDifferent, not doNothing (doNothing keys on the trailer KEY
#    'Co-Authored-By' alone, which would wrongly suppress a second distinct
#    CAPTAIN). Verified by local probe 2026-06-04.
if git interpret-trailers \
      --if-exists=addIfDifferent \
      --trailer "$STOA_SEAT_TRAILER" \
      "$MSG_FILE" > "$MSG_FILE.stoa.tmp" 2>/dev/null; then
  mv "$MSG_FILE.stoa.tmp" "$MSG_FILE" 2>/dev/null || rm -f "$MSG_FILE.stoa.tmp"
else
  rm -f "$MSG_FILE.stoa.tmp"   # interpret-trailers failed -> leave msg untouched
fi

exit 0   # UNCONDITIONAL — fail-open contract
```

- **Grounding:** STRABO Claim 3 (prepare-commit-msg runs on `-m`, fails-closed on non-zero, must exit 0) + my re-fetch of https://git-scm.com/docs/githooks 2026-06-04 (exact: "If the exit status is non-zero, git commit will abort" + "it is not suppressed by the --no-verify option") + https://git-scm.com/docs/git-interpret-trailers (`addIfDifferent` = whole-input dedup) + my LOCAL probe on git 2.40.0.windows.1: hook appended trailer on `git commit -m`, exited 0, `git log %(trailers)` walked it; idempotency + multi-CAPTAIN-append both confirmed.
- **STRABO correction I made:** STRABO Claim 3 suggested `--if-exists=doNothing`. That is WRONG for the multi-CAPTAIN case — `doNothing` keys on the trailer KEY only, so a second distinct CAPTAIN on the same commit would be silently dropped. `addIfDifferent` (keys on the full key+value pair) is correct. Confirmed by probe.

### §28 artifact — `substrate/githooks/README.md` (NEW FILE, opt-in runbook)

A short README colocated with the candidate hook: what it does, the fail-open + default-OFF contract, the two arming methods (copy to `.git/hooks/` vs `core.hooksPath`), the Windows line-ending + exec-bit pitfalls (STRABO Claim 3 + my probe saw the CRLF warning), the `STOA_SEAT_TRAILER` env-var contract, and the stoa--w6d coordination note (hook = trailer; w6d = committer).

### §7/§11 artifacts — NONE NEW (already shipped). Verify-only.

---

## §3 — install.sh deploy wiring for each mechanism + the stubs

The deploy posture for both new mechanisms mirrors the EXISTING enforcement-hook posture (`install.sh` step 5c/5d): **candidate-file deploy is inert; arming is a separate explicit operator-gated step, DEFAULT OFF; user-tier never auto-writes the running config.** This is the proven safe pattern; reuse it, do not invent a new one.

### 5e — §13 settings env-block deploy (NEW install.sh step)

- **Candidate deploy (always, inert):** copy `substrate/templates/settings-env-block.json` → `<DEST_TEMPLATES_DIR>/settings-env-block.json`. Inert — a candidate file sets no env var until merged into a live `settings.json`.
- **Arm (DEFAULT OFF, new flag `--enable-env-block`):**
  - PROJECT tier, no existing `settings.json`: write the env block as the new `settings.json` (the `env` key only).
  - PROJECT tier, existing `settings.json`: do NOT auto-merge (a JSON merge could drop operator config) — print the merge instruction naming the candidate + target. Same as `--enable-hooks` project-tier-existing behavior.
  - USER tier: NEVER auto-write `~/.claude/settings.json` (it IS the running config — ARGUS r4 safety discipline). Print the manual-merge runbook. Same as `--enable-hooks` user-tier behavior.
  - Subproject tier: skipped (no `DEST_SETTINGS_JSON` — Arc 46 §11), warn if flag passed.
- **Idempotency:** re-running with the block already present is a no-op (grep the `env` key / the `_comment` marker before writing).

### 5f — §28 prepare-commit-msg git-hook deploy (NEW install.sh step)

- **Candidate deploy (always, inert):** `mkdir -p <DEST>/.claude/githooks-candidate/`; copy `substrate/githooks/prepare-commit-msg` (chmod +x at dest) + `substrate/githooks/README.md`. Inert — a script in `githooks-candidate/` is NOT in any `.git/hooks/` and is never fired by git.
- **NO auto-arm path.** Unlike the settings hooks (which have an `--enable-hooks` arming path into a *target* settings.json), the git hook has **no install.sh arming flag at all** — arming a git hook means writing into a `.git/hooks/` dir, which install.sh must never do (it would arm git-commit behavior in whatever repo install runs against, including the running build worktree). The README's manual two-method runbook is the only arming path. This is *more* conservative than `--enable-hooks` and is deliberate (the git hook is the LIVE-attack-surface mechanism per §6).
- **Subproject tier:** skipped (consistent with the hooks-dir-empty subproject branch).

### Stub deploys (§7/§11/§13/§28)

The op-disc stubs ride the existing `install.sh` op-disc deploy (operating-disciplines.md is copied whole + subproject-recomposed at MODULE-INLINE markers). §13 and §28 are INLINE prose (not relocated modules) — they have NO MODULE-INLINE markers and need none (no module to recompose). The §13/§28 stub edits are plain in-file prose edits to `substrate/operating-disciplines.md`; they deploy with the file. **No new MODULE-INLINE marker is introduced for §13 or §28** (the encode target is a settings/git mechanism, not a relocated prose module — the mechanism is referenced by path, not inlined).

---

## §4 — Stub-points-to-mechanism map (no dangling pointer)

| Slimmed section | Stub points at | Pointer resolves to (must exist post-build) |
|---|---|---|
| op-disc §13 stub | `substrate/templates/settings-env-block.json` + `install.sh` step 5e | NEW file (this arc) + NEW install step (this arc) |
| op-disc §28.1 stub | `substrate/githooks/prepare-commit-msg` + `install.sh` step 5f | NEW file (this arc) + NEW install step (this arc) |
| op-disc §28.5 | (no pointer — STAYS PROSE) | n/a (judgment discipline, no mechanism) |
| op-disc §7 stub | `modules/two-polybius-coordination.md` (EXISTING) + §7.7→`templates/polling-cron-prompt-template.md` STEP 1.5 (EXISTING) | already exists (Arc 47) — verify resolves |
| op-disc §11 stub | `modules/autonomous-mode-setup.md` (EXISTING) → `templates/polling-cron-prompt-template.md` STEP 4 (EXISTING) | already exists (Arc 47) — verify resolves |

**Inbound-pointer integrity (these point AT §13/§28 and must keep resolving after the slim):**
- `CAPTAIN_ADA.md` §5.5 / :102 → `operating-disciplines.md §28` — stub keeps §28 + §28.1 heading; resolves.
- `MAJOR_PLINY.md` §5.12 (`seat-identity-brief.md`) → §28 trailer format — stub keeps the format spec; resolves.
- `modules/bw-upgrade.md`:57 → `operating-disciplines.md §13` (Windows Python env) — stub keeps §13 heading + the PYTHONUTF8 subject; resolves.
- §28.2–§28.8 internal cross-refs (§28.3 squash-merge, §28.5 blame, §28.7 anchor) — all STAY; the slim touches only §28.1's mechanical trailer-format/worked-examples prose. Verify no §28.x cross-ref dangles.

**No-renumber guarantee:** §7, §11, §13, §28 keep their numbers (stable cross-reference keys). §28.1–§28.8 sub-numbers preserved. §28.5 verbatim.

---

## §5 — VERA verification probes

The load-bearing probes RUN the mechanism (not just grep the prose). Stable probe-ids for verdict citation.

- **P1 (§13 env-block reaches a Bash subprocess — LOAD-BEARING, the Windows dry-run STRABO named):**
  Merge the candidate env block into a throwaway `settings.json` in a synthetic target (NOT the running session), or directly export and invoke. Minimal falsifier re-run:
  `PYTHONUTF8=1 PYTHONIOENCODING=utf-8 python -c "import sys,os; assert os.environ.get('PYTHONUTF8')=='1'; print(sys.stdout.encoding); print('θ','—')"`
  PASS = prints `utf-8` + the theta + em-dash with NO `UnicodeEncodeError`. (DAEDALUS pre-confirmed this on the target Windows env 2026-06-04; VERA re-runs to verify the SHIPPED candidate JSON carries the exact keys + that a merged settings.json round-trips.) Probe the JSON validity: `python -c "import json;json.load(open('substrate/templates/settings-env-block.json'))"` (the `_comment` key is valid JSON).

- **P2 (§28 hook fires + applies trailer + does NOT block a normal commit — LOAD-BEARING):**
  In a synthetic temp git repo (NOT the build worktree): install `substrate/githooks/prepare-commit-msg` into `.git/hooks/`, `export STOA_SEAT_TRAILER='Co-Authored-By: CAPTAIN_VERA_the-stoa <captain-vera@the-stoa.local>'`, then `git commit -m "probe"`.
  PASS = commit SUCCEEDS (exit 0 — never blocked), AND `git log -1 --pretty='%(trailers)'` shows the VERA trailer, AND `git log -1 --format='%an %ae'` shows the PRINCIPAL/probe author UNCHANGED (Author never touched). Then re-commit with the SAME trailer already in the message → assert NOT duplicated (idempotency). Then commit with `STOA_SEAT_TRAILER` UNSET → assert commit succeeds with NO seat trailer added (clean no-op). (DAEDALUS pre-confirmed the happy path + idempotency + multi-CAPTAIN on git 2.40.0.windows.1.)

- **P2-threat (§28 THREAT-ANCHORED probe — exercises the named attack path, see §6 A3 map M1; the verdict's `defeats_via_probe:` cites THIS id):**
  - **(a) attack-blocked:** in the synthetic repo, set `STOA_SEAT_TRAILER` to a malicious value attempting shell-metacharacter / multi-line injection, e.g. `STOA_SEAT_TRAILER='Co-Authored-By: x <y.local>$(touch /tmp/pwned)'` AND a newline-injection variant `STOA_SEAT_TRAILER=$'Co-Authored-By: x <y.local>\nexec evil'`. `git commit -m "probe"`. ASSERT: (i) the commit still exits 0 (fail-open holds), (ii) NO command executed — `/tmp/pwned` does NOT exist (`test ! -e /tmp/pwned`), (iii) the malformed value either fails the §4-shape gate (no trailer added) or lands as a single inert `--trailer` literal — never word-split into a command. ASSERT the hook never `eval`s and never expands `$STOA_SEAT_TRAILER` into command position (static check: grep the script for `eval` / unquoted `$STOA_SEAT_TRAILER` in command position → zero hits).
  - **(b) legit-unaffected:** the well-formed `CAPTAIN_VERA` trailer from P2 IS appended (the mitigation did not break the feature). This is the P2 happy path — reuse it as the legit-traffic half.

- **P3 (§7/§11 cron-prompt template is a well-formed CronCreate body — verify-already-encoded):**
  `Read substrate/templates/polling-cron-prompt-template.md`; assert (i) the template body is a complete fire-loop the substitution slots fill into a valid CronCreate `prompt`; (ii) the "Cron expiry handling" section names the 7-day expiry + the +144h renewal + the no-CronList-expiry-field limitation; (iii) the durable-flag is documented INERT, not relied on. Cross-check the renewal machinery in `modules/autonomous-mode-setup.md` step 1.5 names session-scoped + jitter + no-catch-up. PASS = all present (they are — STRABO-consistent; verify-no-regression).

- **P4 (broken-channel facts re-confirmed — STRABO needs-vera):**
  Re-fetch (VERA, fresh): https://code.claude.com/docs/en/settings ("env" applies to subprocesses), https://git-scm.com/docs/githooks (prepare-commit-msg aborts on non-zero + not suppressed by --no-verify), https://code.claude.com/docs/en/scheduled-tasks (7-day expiry, session-scoped, no-catch-up, local-tz, one-shot auto-delete). Confirm STRABO's issue-status assertions (#55889/#16538/#40228 closed-not-planned = broken-behavior-current) still hold; a reopen+fix would only RELAX the avoid-recommendations, not break the design (env block + git hook do not depend on the broken additionalContext channel at all). PASS = no doc contradicts the design's load-bearing claims.

- **P5 (§28.5 prose survives verbatim):**
  `diff` the §28.5 body (lines covering "Read discipline: git blame is line-level; trailers are commit-level" + the "Do NOT infer human authorship from git blame output" block) pre- vs post-build → assert UNCHANGED (the do-not-infer-authorship judgment is fully preserved). PASS = zero diff in §28.5.

- **P6 (no dangling stub pointer):**
  For every pointer in the §4 map: assert the target file/section EXISTS post-build (`test -f substrate/templates/settings-env-block.json`, `test -f substrate/githooks/prepare-commit-msg`, `grep "step 5e"/"step 5f" substrate/install.sh`, `test -f substrate/modules/two-polybius-coordination.md`, `test -f substrate/modules/autonomous-mode-setup.md`, `test -f substrate/templates/polling-cron-prompt-template.md`). For every INBOUND pointer (§4 table): assert the §13/§28/§28.1 headings the cross-refs target still exist. PASS = zero dangling pointer in either direction.

- **P7 (no renumber + authorship Denson Smith):**
  Assert §7/§11/§13/§28 + §28.1–§28.8 numbers unchanged (`grep -n "^## 13\|^## 28\|^### 28.5" substrate/operating-disciplines.md`). Assert every NEW file's author-like field (the JSON `_comment`, the hook header, the READMEs, the design frontmatter) names **Denson Smith** and NO other person; the hook trailer EXAMPLES are CAPTAIN seat-identity metadata (not authorship claims) per §28.4 boundary. PASS = no renumber + author audit clean.

---

## §6 — Threat classification (LIVE) + threat→mitigation map (§6.12 A3)

**Classification: LIVE — this arc ships runtime mechanism. NOT a §35.5 process-change carve-out.** Per-mechanism:

- **§13 settings `env` block — NOT threat-ratified (config-only; no code execution at config time; sets two well-known env var literals).** Proposed classification: `not threat-ratified (declarative config; PYTHONUTF8/PYTHONIOENCODING are static literals, no attacker-supplied input, no shell execution)`. ARGUS confirms.
- **§7/§11 cron templates — NOT threat-ratified (prose/template, already-shipped; no new runtime surface this arc).** Proposed: `not threat-ratified (already-encoded template; verify-only this arc; no new attack path)`. ARGUS confirms.
- **§28 prepare-commit-msg git hook — LIVE runtime mechanism (executes shell at every commit when armed). This carries a real A3 map.**

**A3 threat→mitigation map (§28 hook):**

> **M1 (untrusted-input command execution at commit time)** → *attack-path:* an attacker who can set `STOA_SEAT_TRAILER`, or inject shell-metacharacters / newlines into commit content / branch name that the hook reads, gets that value executed as a command at every commit (the classic git-hook RCE shape) → *how-defeated:* (i) the hook reads ONLY `STOA_SEAT_TRAILER`, a SESSION-LOCAL env var the seat sets for ITSELF — it does NOT read commit content, branch name, file names, or any attacker-supplied surface; (ii) the value is shape-validated against the canonical `Co-Authored-By: ... <...>.local>` pattern and REJECTED (no-op) if malformed; (iii) the value is NEVER `eval`'d and NEVER expanded into command position — it is passed as a single quoted `--trailer "$STOA_SEAT_TRAILER"` literal to `git interpret-trailers`, which treats it as data, not code; (iv) `interpret-trailers` writes to a temp file then `mv`s — no shell interpolation of the value. **Threat-anchored probe: P2-threat** (both halves: attack-blocked = injection attempts execute nothing + commit still succeeds; legit-unaffected = well-formed trailer still appended).

> **M2 (hook bricks normal/emergency commits — availability threat)** → *attack-path:* `prepare-commit-msg` fails-CLOSED (non-zero aborts the commit) AND is NOT suppressed by `--no-verify`, so a buggy/erroring hook would block EVERY commit including emergency ones, with no escape hatch → *how-defeated:* (i) the hook `exit 0` on EVERY code path (the fail-open contract — every branch ends at exit 0, interpret-trailers failure leaves the message untouched and still exits 0); (ii) **default-OFF / opt-in** — the hook is never auto-armed by install.sh into any `.git/hooks/`; it deploys as an inert candidate, so the unarmed default state has zero availability surface; (iii) per-clone arming is operator-explicit (copy or `core.hooksPath`), so the operator who arms it has read the fail-open README. **Threat-anchored probe: P2** (the "commit SUCCEEDS / never blocked" + "STOA_SEAT_TRAILER unset → clean no-op" assertions are the M2-defeat evidence).

> **M3 (Author-field override / authorship-attribution corruption)** → *attack-path:* a commit-time hook that edits identity could overwrite `Author:` (violating the absolute never-override rule) or write a wrong-person trailer → *how-defeated:* (i) the hook appends ONLY a `Co-Authored-By` trailer and NEVER touches `Author:` (it does not call `git config user.*`, does not set `GIT_AUTHOR_*`); (ii) the trailer is seat-identity metadata (§28.4 boundary: metadata layer, not the content-layer author claim) naming a CAPTAIN seat, never a real third person; (iii) the `.local` email is non-routable and GitHub-unmatchable. **Threat-anchored probe: P2** (`git log --format='%an %ae'` Author UNCHANGED assertion) + P7 (author-audit clean).

**stoa--w6d coordination (so the hook does not contradict w6d):** w6d promotes seat identity from *trailer* to *committer* (sets `GIT_COMMITTER_*` so `git blame`/`git log` attribute the seat, Author stays PRINCIPAL). This §28 hook operates on a DIFFERENT layer — the commit-MESSAGE trailer (which `git blame` does NOT read, §28.5). The two compose without conflict: w6d = committer (blame-readable seat); §28 hook = trailer (squash-merge-surviving seat, §28.3). The hook reads `STOA_SEAT_TRAILER`; w6d sets `GIT_COMMITTER_*` + a session seat-marker — the design recommends the seat-marker and `STOA_SEAT_TRAILER` be set together at activation (both seat-identity signals, same source) so a w6d-enabled session also feeds this hook. The hook does NOT presume w6d is shipped (w6d is a separate ticket); when `STOA_SEAT_TRAILER` is unset the hook is a clean no-op, so it ships independently and composes when w6d lands.

---

## §8 — Self-assessed weak points (§6.2 post-work)

- **WP1 (the §7/§11 brief-vs-reality divergence is the biggest one):** I judged §7/§11 already-encoded by Arc 47 and scoped them to verify-only. If the brief's author intended a *new/different* cron mechanism (e.g., a standalone reusable cron-prompt FILE distinct from the polling-cron template, or encoding into a different structure), my scope is wrong and ADA would build the wrong thing. *Why this shape anyway:* re-encoding a working, STRABO-consistent running structure is churn that risks the very property the gauntlet protects; the honest call is verify + surface the divergence to ARGUS rather than silently re-encode. Flagged as the load-bearing residual question.
- **WP2 (Windows env-block round-trip in a REAL merged settings.json is pre-confirmed at the subprocess level but not at the full Claude-Code-session level):** I probed `PYTHONUTF8=1 python ...` directly and confirmed it reaches the subprocess; I did NOT (cannot, from this seat) confirm that Claude Code actually reads a `settings.json` `env` block and propagates it to the Bash tool *in a live session on this exact Windows build*. The docs assert it; the unit-probe confirms the env var works once set; the integration step (settings.json → Claude → Bash tool env) is the gap. *Why this shape anyway:* the docs are explicit + current (re-fetched), the failure mode is benign (if the env block silently didn't propagate, scripts fall back to today's per-script discipline — no regression), and the per-machine `setx` + in-code reconfigure remain as the kept-prose safety net. VERA's P1 should run the full settings.json round-trip if it can spawn a live session. **VERA must dry-run this.**
- **WP3 (`STOA_SEAT_TRAILER` is a new env-var contract not yet set anywhere):** the hook depends on an env var that NO activation currently sets (it's introduced here, to coordinate with w6d which is unbuilt). Until some activation sets it, the armed hook is a permanent no-op. *Why this shape anyway:* default-OFF + clean-no-op-when-unset means the hook ships harmless and becomes useful when w6d (or a follow-up) sets the var; wiring the var into activation is out of scope (it's w6d's seat-marker concern). Named in Out-of-scope.
- **WP4 (git-hook line-ending / exec-bit on Windows):** my probe saw the `LF will be replaced by CRLF` warning; a hook with CRLF line-endings can fail to execute under some shells. *Why this shape anyway:* the README names the pitfall + the candidate ships with LF (enforced via `.gitattributes` recommendation in the README); the fail-open contract means even an exec failure cannot block a commit (git silently skips an unexecutable hook). VERA's P2 should confirm exec on the target.
- **WP5 (STRABO issue-status freshness, MEDIUM confidence):** the #55889/#16538/#40228 closed-not-planned statuses are STRABO's needs-vera medium-confidence claims. *Why this shape anyway:* my design depends on them only NEGATIVELY (I AVOID the broken additionalContext channel entirely) — a reopen+fix would relax, never break. P4 re-confirms.

---

## Out of scope (keeps ADA bounded; frames ARGUS in-dispatch-vs-future)

- **Wiring `STOA_SEAT_TRAILER` (or the w6d session seat-marker) into any activation paste / role file** — that's stoa--w6d's seat-identity-promotion concern; this arc ships the hook that *consumes* the var, default-OFF.
- **The full stoa--w6d committer-sub-identity system** (GIT_COMMITTER_*, .mailmap, the require-via-gate fail-closed enforcement) — separate ticket; this design only states the non-conflicting composition.
- **Auto-arming the git hook into any `.git/hooks/`** — deliberately never done by install.sh (the LIVE-attack-surface mechanism stays operator-explicit).
- **Re-encoding §7/§11 cron mechanics** — already shipped by Arc 47; verify-only here (pending WP1 resolution).
- **The per-machine `setx PYTHONUTF8 1`** — PRINCIPAL-handled one-time env write; substrate cannot do it.
- **Migrating the existing `.claude/hooks/*.sh` Claude-Code enforcement hooks** — untouched; the §28 git hook is a separate layer.
