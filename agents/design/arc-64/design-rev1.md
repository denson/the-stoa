# Arc 64 design-rev1 — skills-housekeeping pass B (verdict/spec/inspection skills → modules + save-verdict Bash-only rewrite)

Author: Denson Smith · Ticket: stoa--p41.2 (Workstream B) · Seat: CAPTAIN_DAEDALUS · Branch: arc-64/build

---

## 1. Problem restatement

Three skills currently sit on the model-invokable skill menu (`install.sh` `SKILL_NAMES`): `save-verdict`, `validate-spec`, `inspect-script-output`. Pass B moves all three OFF that menu and INTO `substrate/modules/` instruction documents that the relevant seat Reads at the point of need. Two distinct module shapes are needed because the three skills are not the same kind of thing:

- **`save-verdict`** is a *code* skill (a Python writer the verdict-producing CAPTAINs invoke). It is rewritten as a **Bash-only module** with no Python: the seat authors the verdict body via `printf` redirection, runs an inline `sha256sum` round-trip, and **attaches the written verdict to the coordination ticket on beadwork** (`bw attach`) so a worktree teardown cannot destroy it (the Arc-62 verdict-loss fix). The Python script + `_lib` + `.gitignore` are `git rm`'d.
- **`validate-spec` + `inspect-script-output`** are *POLYBIUS-invoked* skills whose `check.sh`/`_check_runner.py` scripts STAY callable. Each becomes an instruction/when-to-use **wrapper module** that points POLYBIUS at the retained script; only the SKILL.md menu-registration is removed.

Coupled with the rehoming: repoint the VERA/ARGUS/CATO "Canonical verdict-save path" sections to the save-verdict module; resolve `stoa--7b1.1` (the read-only-review-seat §4-no-Write vs §7-mandates-save-verdict tension) at the shared layer; drop the 3 entries from `SKILL_NAMES` and deploy the 3 modules; keep the app green (LIEUTENANT delta −3).

**Imported assumptions (named, per §6.1):**
- (A1) The directive's phrase "modules the dispatched specialist Reads at dispatch" applies cleanly only to `save-verdict` (CAPTAIN-facing). `validate-spec`/`inspect-script-output` are **POLYBIUS-facing** (orchestrator-invoked, not CAPTAIN-dispatch). I restate their target as "a module POLYBIUS Reads when triaging a substrate-update / spec-validation run" — the directive's deliverable #2 ("instruction wrappers; scripts retained") confirms this reading, so this is not a re-scope, but it is a sharpening the brief left implicit.
- (A2) "Attach to bw at write" uses `bw attach` (stores file BYTES under `attachments/<ticket>/`, committed to the orphan branch), NOT `bw comment` (which would inline the body as a message). `bw attach` is the byte-durable form the Arc-62 fix needs. Verified live (§3 P1).
- (A3) `7b1.1` names ARGUS/NOMOS/ZENO as the shared layer, but only ARGUS (and CATO, a sibling read-only seat) actually carry BOTH a no-Write §4 AND a save-verdict §7. ZENO/NOMOS are read-only but do NOT save-verdict (their verdicts are dispatch-return + bw breadcrumb only). The reconciliation must therefore (a) carve verdict-authoring out of the no-Write prohibition for the seats that DO save-verdict, and (b) state, for ZENO/NOMOS, that the carve-out is latent (they don't save-verdict today, so nothing changes for them) — keeping the language coherent for all read-only seats together without inventing a save step they don't have.

---

## 2. Approach

### 2.1 `save-verdict` → `substrate/modules/save-verdict.md` (Bash-only)

A module Read by the verdict-producing seat (VERA / ARGUS / CATO) at verdict-write time. Contents:

**(a) Canonical path convention.** Verdict lands at `<worktree-root>/agents/verdicts/<ticket-id>/<OFFICER>-<YYYY-MM-DDTHH-MM-SSZ>.md`. The seat MUST use the absolute arc-worktree root for `<worktree-root>` (sub-agents inherit the parent session cwd; the PLINY dispatch brief carries the worktree path — `MAJOR_PLINY.md` §5.14). Officer name matches `^[A-Z][A-Z0-9_]*$`; ticket-id matches `^[a-zA-Z0-9][a-zA-Z0-9._-]*$` (path-traversal defense preserved as a documented seat check, see Q-A).

**(b) Body authoring via `printf` (uniform across all three seats — the `7b1.1` mechanism).** The module makes `printf` redirection the SINGLE authoring mechanism for VERA, ARGUS, and CATO alike. Today VERA uses the Write tool while ARGUS/CATO use `printf` (NOMOS's UNIFORMITY flag); the module collapses this to `printf` for all three so the procedure is identical regardless of seat toolset. The seat builds the body and writes it directly to the canonical path:

```bash
printf '%s' '<verdict-body>' > agents/verdicts/<ticket-id>/<OFFICER>-<ts>.md
```

Quoting caveat (proven, ARGUS:246 / CATO:212): a single-quoted `printf '%s' '…'` body is literal (no `$`/backtick expansion) but cannot contain a bare apostrophe — escape each embedded apostrophe as `'\''` (close-quote, escaped-apostrophe, reopen-quote). Forbidden: a `cat <<'EOF' … EOF` heredoc (breaks on apostrophes on Windows git-bash) and any `/tmp/…` path (git-bash `/tmp` ≠ Python `/tmp`; not relevant now that Python is gone, but the worktree-relative-path discipline is retained so the verdict lands in the tree it will be attached from).

The module writes the body DIRECTLY to the canonical `.md` (no separate `_body-*.tmp.md` scratch step — that two-step dance existed only to feed the Python `--body-path`; with Python gone, the `printf` target IS the verdict file).

**(c) Inline sha256 round-trip (integrity guarantee preserved, per Q1).** Immediately after the write, the seat re-hashes the on-disk file and compares to a hash of the intended body. `sha256sum` is present in this git-bash (GNU coreutils — verified live, §3 P3):

```bash
DEST=agents/verdicts/<ticket-id>/<OFFICER>-<ts>.md
printf '%s' '<verdict-body>' > "$DEST"
WANT=$(printf '%s' '<verdict-body>' | sha256sum | cut -d' ' -f1)
GOT=$(sha256sum "$DEST" | cut -d' ' -f1)
[ "$WANT" = "$GOT" ] || { echo "SAVE-VERDICT FAIL: sha256 mismatch want=$WANT got=$GOT" >&2; exit 2; }
```

This replaces the Python `write_with_verify` + step-8 re-hash with a single inline assert. Exit-2-on-mismatch preserved as the integrity signal.

**(d) Attach-to-bw-at-write (NET-NEW — the Arc-62 verdict-loss fix).** After the sha256 check passes, the seat attaches the verdict file to the coordination ticket:

```bash
bw attach <ticket-id> "$DEST" --name "verdicts/<OFFICER>-<ts>.md"
```

`bw attach` stores the file's BYTES under `attachments/<ticket-id>/verdicts/<OFFICER>-<ts>.md` and commits to the beadwork orphan branch — surviving any worktree teardown. `--name` mirrors the on-disk canonical sub-path so a reader walking `attachments/<ticket>/verdicts/` sees the same layout as `agents/verdicts/<ticket>/`.

**Attach-failure posture (PLINY's open question — answered):** the attach is **FAIL-LOUD but write-preserving**. The verdict on disk is already integrity-checked (step c); the attach is the durability upgrade. If `bw attach` exits non-zero, the seat surfaces it loudly (`echo "SAVE-VERDICT WARN: bw attach failed (rc=$?); verdict is on disk at $DEST but NOT yet on beadwork" >&2`) and the verdict-write is NOT considered complete — the seat reports the attach failure in its dispatch return so PLINY can retry the attach or escalate. Rationale: a silent attach failure reproduces exactly the Arc-62 loss (verdict on a doomed worktree, not on bw). It does NOT `exit`-hard-fail the whole verdict (the disk artifact is valid and integrity-checked); it fails LOUD so the gap is visible, not silent. This is the §34 fail-loud-on-mismatch posture applied to the durability step.

**(e) Q-A enforcement (§15.4 shape + threat-coverage empty-binding) — see §2.4.**

### 2.2 `validate-spec` + `inspect-script-output` → wrapper modules

Two modules, each a thin instruction/when-to-use wrapper over its RETAINED, callable script (Q2: scripts are NOT dropped). The script files stay on disk at `substrate/skills/validate-spec/check.sh` (+ `_check_runner.py` + `_lib`) and `substrate/skills/inspect-script-output/check.sh`; only the `SKILL.md` menu-registration is removed.

- **`substrate/modules/validate-spec.md`** — POLYBIUS Reads this when asked to "validate the spec / run the mechanical checks". Carries: the when-to-invoke list (lifted from the SKILL.md), the invocation (`bash .claude/skills/validate-spec/check.sh …` — the script path is unchanged; it is no longer model-invokable but stays operator-runnable), the strangeness-triage routing into `operating-disciplines.md` §27 step 3, and the A21 PRINCIPAL-gate escalation note.
- **`substrate/modules/inspect-script-output.md`** — POLYBIUS Reads this as step 2 of the §27 mechanical-script/agent-inspection split. It **coordinates with `mechanical-inspection-split.md`**: that module owns the 3-step pattern canon (§27.1–§27.7); the new module is the *operational pointer* to the worked-example script, and adds a one-line cross-ref `> Pattern canon: mechanical-inspection-split.md §27.2; this module is the run-the-inspection-script operational entry.` `mechanical-inspection-split.md` §27.5 already names `substrate/skills/inspect-script-output/` as the worked example — that reference stays valid (the dir + `check.sh` persist; only `SKILL.md` is removed). I add a back-reference line in `mechanical-inspection-split.md` §27.5 pointing at the new module so the two don't drift.

**Disposition of the two SKILL.md files:** `git rm substrate/skills/validate-spec/SKILL.md` and `git rm substrate/skills/inspect-script-output/SKILL.md` (removing them from the LIEUTENANT discovery surface — gen-data is directory+SKILL.md driven, §2.6). The `check.sh`/`_check_runner.py`/`_lib` files STAY. (Pattern precedent: Arc 63 did exactly this for `check-substrate-updates`/`check-bw-release` — removed SKILL.md, kept the dir as an operator tool. See `generated.test.ts` L91-94 comment.) This is the established "operator-tool carve-out" `install.sh` already handles (L1289-1303).

### 2.3 Repoint VERA / ARGUS / CATO "Canonical verdict-save path" sections

Each of the three sections (VERA:266, ARGUS:246, CATO:212) is rewritten to: `Read .claude/modules/save-verdict.md` and follow its procedure (printf authoring + inline sha256 + bw-attach). The current inline `python …/_save_verdict.py` invocation prose is removed. **BUT** — see Q-C — the procedure cannot be a bare `Read` pointer alone for the subproject tier; the load-bearing printf+sha256+attach steps are ALSO kept inline in each role-file section as the always-resolvable fallback, with the module as the canonical elaboration. The inline section becomes the §2.1 (b)/(c)/(d) procedure in compressed form; the module carries the full rationale + Q-A enforcement detail.

### 2.4 `stoa--7b1.1` resolution + Q-A enforcement (shared read-only-review-seat layer)

**The tension:** ARGUS §4 says "No `Write`, no `Edit`. … cannot modify the design artifact, cannot draft a 'proposed fix' document, cannot land an amendment." CATO §4 is parallel ("cannot modify the diff … cannot draft a 'proposed cleanup'"). §7's Canonical verdict-save path mandates writing a verdict to disk. A literal reading makes §4 forbid the very write §7 requires.

**The mechanism that dissolves it:** the Bash-only module authors via `printf` redirection — a *Bash* operation, NOT the `Write`/`Edit` tool. The seats have no Write/Edit tool (frontmatter omits them); `printf >` is within their existing Bash grant. So §4's "no Write/Edit" and §7's "save the verdict" were never in genuine conflict — §4 forbids the TOOL, §7 is satisfied by a Bash redirect. The resolution makes this explicit rather than leaving it as an apparent contradiction. See Q-B for exact wording.

**Threat→mitigation map (§6.12).** This arc is **process / role-file hardening** — moving skills to modules, rewording role files, adding a durability attach. No runtime attack path. Per §35.5 self-carve-out: `not threat-ratified (process change — skill→module rehoming + verdict-durability + doc-coherence; no runtime attacker, no attack path)`. ARGUS confirms this classification at critique; I cannot self-grant it. Consequently no threat-anchored probe is required (§6.13). The path-traversal regexes the Python enforced are NOT a threat-mitigation in the §35 sense (no attacker supplies the officer/ticket-id — they come from the trusted PLINY brief); they are input-hygiene, preserved as documented seat checks per Q-A.

**Q-A (enforcement loss) — RECOMMENDATION: hybrid.**
- **§15.4 shape validation** (INCOMPLETE/UNVERIFIABLE ⇒ quadrant + coverage/sanity+next-step): **accept seat-side**, documented in the module + already taught in each seat's verdict-format section. Rationale: these are rare verdict shapes, the seat role file already specifies the required fields, and a bash re-implementation of the enum+conditional-field matrix is brittle and duplicates the role-file spec. The Python check was a convenience backstop, not the source of truth (the role file is). Cost: a malformed INCOMPLETE verdict is no longer mechanically rejected at write — but it IS caught by NOMOS/the gauntlet downstream, and the shape is rare.
- **Threat-coverage empty-binding check** (`trm_count > 0 ⇒ ≥1 well-formed probe-id`): **preserve via a lightweight inline bash assert.** Rationale: this is the §35/`stoa--yfv` B2 keystone — a threat-ratified mitigation must not pass without a cited executed probe — and it is a cheap, high-value, single-conditional check. Preserving it keeps the security-property guard mechanical rather than discretionary.

```bash
# Only when the verdict declares threat-ratified mitigations:
if [ "${TRM_COUNT:-0}" -gt 0 ]; then
  [ -n "$THREAT_PROBE_IDS" ] || { echo "SAVE-VERDICT FAIL: $TRM_COUNT threat-ratified mitigation(s) declared but no threat-coverage probe-ids (op-disc §35/yfv B2)" >&2; exit 4; }
  IFS=',' read -ra _ids <<< "$THREAT_PROBE_IDS"
  for _id in "${_ids[@]}"; do
    _id="${_id// /}"
    [ -n "$_id" ] || continue
    printf '%s' "$_id" | grep -Eq '^[pP][0-9A-Za-z._-]+$' || { echo "SAVE-VERDICT FAIL: probe-id '$_id' malformed (must match ^[pP][0-9A-Za-z._-]+\$)" >&2; exit 4; }
  done
fi
```

**CRITICAL (PLINY's Q-A note):** the regex is `^[pP][0-9A-Za-z._-]+$` — **case-insensitive leading p/P**, NOT the Python's lowercase-only `^p[0-9A-Za-z._-]+$`. The lowercase-p constraint IS the live `stoa--j2i` bug (rejects canonical uppercase `P-INJ`); the directive retires `j2i` precisely because this rewrite eliminates it. The bash assert MUST accept uppercase probe-ids. This is the one place the rewrite changes behavior on purpose.

### 2.5 `install.sh` — `SKILL_NAMES` −3 + deploy 3 modules

- Remove `save-verdict`, `validate-spec`, `inspect-script-output` from `SKILL_NAMES` (L228-234; 10 → 7). `credential-discipline` STAYS (out-of-scope/deferred).
- The 3 new module `.md` files land via the existing glob-discovery (`substrate/modules/*.md` → `.claude/modules/`, L1328) at user/project tiers automatically — no new deploy code.
- **Recompose ownership-partition (Q-C):** see §2.7. **Recommendation: NO new recompose ownership** for the 3 modules → no `install.sh` recompose-partition edits, no MODULE-INLINE markers, no Checks-A–E exercise needed. (If ARGUS overturns Q-C, the fallback adds VERA/ARGUS/CATO as recompose owners — a much larger change; spec'd as the rejected alternative in §4.)
- The two retained script dirs (`validate-spec/`, `inspect-script-output/`) with SKILL.md removed are deployed via the operator-tool carve-out already in `install.sh` (L1289-1303, same mechanism Arc 63 used for the check-* dirs). Verify the carve-out covers these two dirs; if it is an explicit list, add them.

### 2.6 App green (LIEUTENANT delta −3)

`discoverSkillFiles` (gen-data-lib.ts L92) is **directory + SKILL.md driven** — it renders each `substrate/skills/<dir>` that contains a `SKILL.md`. Removing the 3 SKILL.md files (save-verdict dir is fully `git rm`'d; validate-spec/inspect-script-output keep their dirs but lose SKILL.md) drops 3 LIEUTENANTs.

- `generated.test.ts` L96 asserts only `slot.skills.length > 0` — no count, no `toContain` for the 3 names (verified: zero references to the 3 names in `app/src/data/__tests__/` or `app/scripts/`). So the test **passes unchanged**; the only edit is refreshing the L90-94 explanatory comment to record the Arc-64 −3 churn (matching the Arc-61/63 comment-maintenance pattern).
- `app/src/data/generated/agents.ts` is auto-generated by `npm run gen-data` — regenerates automatically.
- `app/src/data/display-extras.ts` L85-91 carries a hand-curated `save-verdict` entry (`kind: "skill"`). This is decorative display data NOT asserted against the real skill dirs (many entries there have no backing dir). **Fix-now:** update that entry to `kind: "module"` and adjust the description to "Bash-only verdict-write module (printf author + sha256 + bw-attach)" so the displayed roster doesn't misrepresent save-verdict as a live skill. (`validate-spec`/`inspect-script-output` are not in display-extras — no edit needed there.)
- DoD: `cd app && npm run gen-data && npm run build && npm test` green.

### 2.7 Q-C — recompose coupling determination (LOAD-BEARING)

**Ground truth (verified):**
1. The `install.sh` subproject recompose ownership-partition (L1194-1218) is keyed to FIVE role-file owners: POLYBIUS, OPDISC, PLINY, DAEDALUS, CHIRON. **VERA/ARGUS/CATO are NOT owners and carry ZERO MODULE-INLINE markers** today.
2. VERA/ARGUS/CATO DO deploy at subproject tier (CAPTAIN_NAMES loop, L207-212 / L1164).
3. At subproject tier, `DEST_MODULES_DIR=""` — the modules dir is NOT deployed, and a dispatched seat's `Read .claude/modules/<X>.md` does NOT resolve reliably (claude-code #56686/#31546/#29423; web-verified this arc — subagent module-path resolution is a known defect).

**The decision:** If VERA/ARGUS/CATO §7 became a BARE `Read .claude/modules/save-verdict.md`, that Read would FAIL at subproject tier (module not on disk + path resolution unreliable), and a subproject-tier ARGUS/CATO would have NO save-verdict procedure. Two ways out:

- **Option C1 (recompose-own):** add VERA/ARGUS/CATO as recompose owners — 3 new MODULE-INLINE-markered stubs in the role files, a 3-entry ownership-partition addition, 3 recompose calls, and FAIL-LOUD Checks A–E verified via a REAL (non-dry-run) subproject recompose (Arc-61 lesson: dry-run early-returns before the awk checks). Heavy; adds three new recompose owners for one shared module.
- **Option C2 (RECOMMENDED — inline-fallback, Read-at-dispatch-only):** the load-bearing printf+sha256+attach procedure stays INLINE in each role file's §7 (compressed, §2.3), so it always resolves at every tier including subproject. The new `save-verdict.md` module carries the canonical full procedure + Q-A enforcement + rationale, deployed at user/project tiers and Read there as the elaboration. The role file §7 says: "Follow the inline procedure below; `Read .claude/modules/save-verdict.md` for the full rationale + enforcement detail (user/project tier — at subproject tier the module is not deployed, so the inline procedure is authoritative)." **No MODULE-INLINE markers, no recompose ownership, no Checks-A–E exercise.**

**Recommendation: C2.** Rationale: (1) the printf+sha256+attach core is ~12 lines — small enough to live inline without bloating the role file, unlike the multi-hundred-line modules that justify recompose; (2) it avoids minting three new recompose owners + the FAIL-LOUD machinery for a procedure that must work at subproject tier anyway; (3) it sidesteps the subproject path-resolution defect entirely rather than papering over it; (4) it matches how the procedure ALREADY lives (inline at VERA:266/ARGUS:246/CATO:212 today). The module is the canonical home for the *rationale and the Q-A enforcement spec*; the role file is the always-resolvable home for the *executable steps*. SSoT note: to avoid drift between the inline steps and the module, the module's procedure block and the role-file inline block are byte-aligned (the `canonical-template-alignment.md` discipline applies — a `diff` check during build confirms the shared printf/sha256/attach block matches across all three role files + the module).

### 2.8 Threat→mitigation map

| Item | Classification |
|---|---|
| skill→module rehoming (3 skills) | `not threat-ratified (process change; no runtime attack path)` — ARGUS confirms |
| attach-at-write durability | `not threat-ratified (durability hardening; closes a verdict-LOSS gap, not an attacker path)` — ARGUS confirms |
| threat-coverage empty-binding bash assert | preserves an EXISTING §35/yfv-B2 guard; not a new mitigation (the guard predates this arc; this arc re-homes it from Python to bash, fixing the j2i lowercase-p bug en route) |

No named runtime threat is mitigated by this arc; the §35.5 carve-out applies. ARGUS confirms the classification (§6.12 — I propose, ARGUS confirms).

---

## 3. Verification probes (for VERA)

- **P1 — attach-at-write (load-bearing, NET-NEW).** Drive the module's procedure for a synthetic verdict on a throwaway ticket in the worktree, then `bw show <ticket>` / inspect `attachments/<ticket>/verdicts/` on the beadwork branch and confirm the verdict BYTES are present on beadwork (not just on worktree disk). Assert: the attached bytes sha256-match the on-disk verdict. (Verify-then-assert: do NOT accept "the module says it attaches".)
- **P2 — no-Write-seat authoring.** Confirm a read-only seat (no Write/Edit; Bash only — simulate ARGUS/CATO toolset) can author + write + sha256-verify + attach a verdict end-to-end via `printf` redirection with an embedded apostrophe correctly escaped as `'\''`. This is the `7b1.1` resolution working in practice.
- **P3 — sha256 integrity (negative probe).** Corrupt the on-disk verdict between write and re-hash (append a byte); confirm the inline round-trip exits 2 with the mismatch diagnostic. (Live-confirmed available: `sha256sum` present in this git-bash, round-trip MATCH on a clean write.)
- **P4 — threat-coverage empty-binding (Q-A preserved-check).** With `TRM_COUNT=1` and empty `THREAT_PROBE_IDS`, confirm exit 4. With `TRM_COUNT=1` and `THREAT_PROBE_IDS="P-INJ"` (UPPERCASE), confirm it PASSES — proving the `stoa--j2i` lowercase-p bug is NOT reproduced (regex `^[pP]…`). With a malformed id (`x9`), confirm exit 4.
- **P5 — SKILL_NAMES −3 + no dangling pointers.** `grep -rn "skills/save-verdict\|skills/validate-spec\|skills/inspect-script-output" substrate/ app/` returns only intended module-pointer / operator-tool references (no live invocations of the retired SKILL.md menu entries), excluding `substrate/arcs/` + `substrate/v1-historical/`. `SKILL_NAMES` has 7 entries.
- **P6 — install.sh dry-run + (Q-C=C2) NO real-recompose needed.** `bash substrate/install.sh --target user --dry-run` passes; the 3 modules deploy via glob. Confirm VERA/ARGUS/CATO are NOT in the recompose ownership-partition (C2: no new owners). If ARGUS overturns to C1, this probe escalates to a REAL subproject recompose with Checks A–E green.
- **P7 — app green.** `cd app && npm run gen-data && npm run build && npm test` all green; LIEUTENANT count dropped by 3 from the prior baseline; `generated.test.ts` length>0 still holds.
- **P8 — role-file inline/module byte-alignment (C2 SSoT).** `diff` the shared printf+sha256+attach procedure block across CAPTAIN_VERA/ARGUS/CATO §7 inline + `modules/save-verdict.md` — all four byte-identical (no drift).

---

## 4. Self-assessed weak points

- **(W1, TOP) Q-C=C2 duplicates the procedure across four homes (3 role files + module).** The printf+sha256+attach block lives inline in VERA/ARGUS/CATO §7 AND in the module. That is four copies to keep in sync — exactly the drift surface the `canonical-template-alignment.md` discipline exists for. P8 mechanically guards it at build time, but a FUTURE arc that edits the module without re-aligning the role files (or vice versa) reintroduces drift. *Why this shape anyway:* the alternative (C1 recompose) mints three new recompose owners + the full FAIL-LOUD machinery for a 12-line procedure, and STILL leaves the user/project-tier module as a separate copy — C2's drift is bounded by one mechanical `diff` (P8), C1's complexity is permanent. The byte-alignment check converts an unbounded drift risk into a single build-time assertion.
- **(W2, TOP) The attach-failure posture (FAIL-LOUD-but-write-preserving) is a judgment call ARGUS/PLINY may want stricter.** I chose: integrity-checked disk write + loud-surfaced attach failure reported up, rather than a hard `exit` that discards a valid verdict. A reviewer could argue the whole point of the Arc-62 fix is that a verdict not on bw is a LOST verdict, so the write should hard-fail until the attach succeeds. *Why this shape anyway:* hard-failing discards a valid, integrity-checked artifact and blocks the gauntlet on a transient bw/network hiccup; the loud-surface-and-report path keeps the verdict recoverable (PLINY retries the attach from the on-disk file) while making the durability gap impossible to miss. But this is the most likely thing ARGUS promotes — flagged explicitly as a `residual_question_for_argus`.

## 5. Out of scope

- `credential-discipline` skill — deferred (directive Out-of-scope); STAYS in `SKILL_NAMES`.
- Pass A (SessionStart triggers + gauntlet-setup) — DONE (Arc 63).
- `stoa--9s6` worktree-teardown ownership — separate (attach-at-write reduces its blast radius but does not close it).
- `stoa--z2b` authorship-gate fix — separate; this design uses gate-safe prose.
- A v2 schema model for LIEUTENANT/module display in `display-extras.ts` — out of scope; this arc only corrects the one stale `save-verdict` entry.
- Migrating `validate-spec`/`inspect-script-output` `check.sh` recognition logic into the inspection-agent layer (`mechanical-inspection-split.md` A7 boundary) — separate future arc.
