# ADA build brief — stoa--p0e: deny-gate RETIREMENT + report-only attribution ADVISORY

**From:** PLINY_the-stoa (orchestrator) · **To:** CAPTAIN_ADA (executor) · **Arc:** stoa--p0e
**operating-mode:** autonomous
**seat-identity:** `CAPTAIN_ADA_the-stoa <captain-ada@the-stoa.local>` (write this VERBATIM into the `Co-Authored-By:` trailer of every commit — op-disc §28)
**Worktree (build here — `cd` first):** `C:\Users\denso\claude_projects\the-stoa\.claude\worktrees\stoa--p0e-build` (branch `stoa--p0e/build`)

## Authoritative design

Build from **`agents/design/stoa--p0e/design-rev2.md`** (ADA-authoritative; SUPERSEDES rev1; self-contained — you do NOT need to cross-read rev1). It is ARGUS-cold-audited + FM-verified + PLINY-A1-ratified. The edit list below is the FM-AMENDED authoritative scope — where it and rev2 differ (the `principal-identity` placement), THIS BRIEF wins.

## Grounding-check (mandatory — read design examples against shipped reality)

Ground-check every concrete example in the design against the shipped code, specifically:
- JSON example shapes (settings.json hook objects, report format)
- Function/method signatures (any helper you port from `_hooklib.sh`)
- Error message text (exact string match)
- Line ranges in path:line citations (design cites specific install.sh line numbers — VERIFY each before editing; line numbers drift)
- Wire-protocol constants (hook `if:` matcher strings, JSON keys)

If a design example contradicts the shipped code, the shipped code is canon — build to ship reality and flag the drift in your return.

## THE AMENDED ON-BRANCH EDIT LIST (all of this lands on `stoa--p0e/build`)

### Retirement (deny-hook)
1. **`.claude/settings.json`** (repo root, in the worktree): delete the FIRST `PreToolUse.Bash` hook object — the `if: "Bash(git commit*)"` entry whose command ends `pretooluse-author-field-audit.sh` (design §2.1a; verify current line span). KEEP the other two objects (`Bash(git *)` clean-tree; `Bash(bw comment*)` no-dash-m) and all `Stop`/`PostToolUse`/`SessionStart` entries. Post-edit: the `PreToolUse.Bash.hooks` array has exactly 2 objects.
2. **`substrate/templates/settings-hooks.json`**: delete the identical first `{{HOOKS_DIR}}/pretooluse-author-field-audit.sh` object (design §2.1b). Keep everything else incl. the `_comment` header (verified generic — no gate-specific edit needed) and the `startup|resume` substrate-check entry.
3. **Archive the script (git mv, do NOT delete):** `git mv substrate/hooks/pretooluse-author-field-audit.sh substrate/v1-historical/hooks/pretooluse-author-field-audit.sh` (create `substrate/v1-historical/hooks/`). This auto-removes it from the `substrate/hooks/*.sh` deploy glob.
4. **`_hooklib.sh` STAYS untouched** (shared by surviving gates). Leave the now-dead author functions intact (design §2.3 / W4).
5. **Archive the author-gate tests (git mv):** `run-author-gate-tests.sh` + `fixtures/{tp,fp,control}/` → `substrate/v1-historical/hooks/tests/`. KEEP `substrate/hooks/tests/run-stop-self-check-tests.sh` + `fixtures/stop-event-orchestrator.json` (surviving hook). (design §2.4)
6. **Rewrite `substrate/hooks/tests/README.md`** (currently "Author-gate regression corpus") to describe ONLY the surviving `run-stop-self-check-tests.sh` (design §2.4/r4). Optionally carry the old author-gate README content to `substrate/v1-historical/hooks/tests/README.md`.
7. **WHY-HISTORY — new `substrate/v1-historical/hooks/RETIREMENT.md`** (design §2.5): document as HISTORY-NOT-FIX-TARGETS — (i) stoa--dps PEP-621 inline-table false-positive; (ii) the Bash-only matcher hole (PowerShell ungated); (iii) the compound `cd && git commit` matcher dodge; plus the arc-77 empirical (doctrine verified authorship 4× independently; the deny-hook contributed only a false-positive hold + a discovered coverage hole). Cite stoa--dps, stoa--eby.
8. **Update `substrate/hooks/README.md`** (design §2.5 item 2): remove the author-field-audit row from the §4 table; fix the prose that names the gate as a denier (design cites lines ~47, ~98, ~139, §7 ~215 — VERIFY each); add a short "Retired gates (Arc stoa--p0e)" note pointing to `v1-historical/hooks/RETIREMENT.md` + naming the advisory skill. Do NOT delete §7 (the z2b narrowing record) — annotate it as historical-to-the-retired-gate.

### The FM-AMENDED extra on-branch edit (r1 row 3 — MOVED on-branch per FM 19:49:05Z ruling)
9. **`.claude/hooks/principal-identity`** (in the worktree; git-tracked): the leading comment block (design §2.6 says lines ~1-8/3-5 — VERIFY) currently states the `pretooluse-author-field-audit.sh` gate "the commit is denied" — FALSE after retirement. **Replace that comment block with the corrected advisory text** (the SAME text as the install.sh seed-block fix — design §5, the corrected `echo` block: describes the advisory SECONDARY check, report-only, NEVER denies). **The allow-list VALUES below the comment (`denson` / the email / `Denson Smith`) STAY UNCHANGED.** (FM verified never-clobber `:1480-1481` protects this on-branch edit from the post-merge regen; it's slug-independent + tracked → persists through merge.)

### The advisory (build the skill)
10. **`substrate/skills/attribution-advisory/`** (design §3 + §4 + §10):
    - `advise.sh` — POSIX `sh` wrapper + self-contained `python3` unified-diff scanner. `set -uo pipefail`, FAIL-OPEN, **ALWAYS `exit 0`** (no reachable `exit 1`/`exit 2`, no `permissionDecision`/`"deny"` emission — report-only BY CONSTRUCTION). Flags: `--diff-file <p>`, `--range <B>..<H>`, `--stdin`, default `git diff --cached`, `--report-out <path>` (default `<workspace>/.claude/attribution-advisory-report.md`). PRIMARY = name-agnostic modify/DELETE of an existing attribution line (design §4.2 term set); SECONDARY = NEW non-PRINCIPAL author field outside vendored paths, reusing `.claude/hooks/principal-identity`, FAIL-OPEN if absent (§4.3). Report format per design §3 (each finding states WHY + WHAT-TO-CHECK inline; PRIMARY "WHAT TO CHECK" names legit year-bump/reformat cases per r5).
    - `SKILL.md` — frontmatter **`author: Denson Smith`**; documents invocation + report path + the never-blocks contract.
    - `tests/run-attribution-advisory-tests.sh` + `tests/fixtures/*.diff` — the P1/P2/P3/P4 + supplementary fixtures per design §10 (SHIP the tests/ — do NOT exclude; design §10 r2 decision).
11. **`substrate/install.sh` — SKILL_NAMES + all 5 comment fixes** (design §5):
    - Add `attribution-advisory` to the `SKILL_NAMES` array (VERIFY current location).
    - Correct ALL FIVE author-gate comment sites (design §5 table: ~:85-86, ~:689-693, ~:1471-1478, ~:1488-1497, ~:1906-1907 — VERIFY each line). The **:1488-1497 seeded `echo` block** is highest priority (deploys VERBATIM to every consumer + carries the false "the commit is denied") — replace with the corrected block in design §5. KEEP the `principal-identity` seeding behavior + the `principal-identity) continue` staleness carve-out (code unchanged; only prose corrected).

### bw disposition
12. Disposition **stoa--dps** as superseded-by-retirement: `bw comment stoa--dps "<superseded note citing stoa--p0e retirement>"` then `bw close stoa--dps --reason "superseded by stoa--p0e deny-gate retirement (the PEP-621 false-positive is moot — the gate is retired, not fixed)"` (verify close syntax; if unsure ask via return, don't guess-flag).

## Commit model
- Build + commit on the branch. Logical commit(s); a single squashable commit is fine. **Author stays your configured git identity (the PRINCIPAL's — do NOT override `Author:`).** Every commit ends with the trailer:
  `Co-Authored-By: CAPTAIN_ADA_the-stoa <captain-ada@the-stoa.local>`
- **Cite the PRINCIPAL retirement ruling in the commit message** (per brief scope item 1): reference the stoa--p0e SCOPE-RESHAPE ruling (2026-07-09) as the retirement authority.
- **Do NOT merge, do NOT push, do NOT rebase onto main.** Everything stays on `stoa--p0e/build`.

## Armed-gate SAFETY NOTE (read before you commit)
This session still has the author-field-audit gate ARMED (that's what we're retiring). PLINY verified `classify_author_file` only scans specific config basenames + `*.md` frontmatter + `*.claude-plugin/*` — your `.diff` fixtures and `.sh` scripts are NOT classified/scanned, and the `.md` files you create (SKILL.md/RETIREMENT.md) pass on `author: Denson Smith` or absent frontmatter. So a normal commit will NOT be blocked. **If a commit is UNEXPECTEDLY denied by any gate: STOP and surface it to PLINY in your return — do NOT reshape/split the commit to dodge the matcher** (dodging a gate re-opens the footgun; Stop-hook clause B).

## Out of scope (do NOT do)
- No `.claude/` deploy-regen on the branch (slug derives from checkout basename → wrong slug; that regen is the FM's post-merge on-main step).
- No `CLAUDE.md` §4 authorship-doctrine edit (stays PRIMARY, untouched).
- No API key / no keyed CI / no Sonnet-adjudication (dropped by the ruling).
- Do NOT touch the two surviving Bash gates, `_hooklib.sh` logic, or other projects' repos.

## Return to PLINY
Your build summary + the list of files changed/added/moved + the commit SHA(s) + confirmation each acceptance-relevant item landed (esp. #9 the on-branch principal-identity edit, and the advise.sh always-exit-0 property) + any design-vs-shipped drift you flagged + the stoa--dps disposition result. Echo a 3-5 line summary to `stoa--p0e` (bw comment, positional, no -m, no backticks), signed `[from: CAPTAIN_ADA_the_stoa (subagent) | caller-sid 822aa122-41c9-4a76-9a87-cfe6e4fdf4c5]`. You BUILD; you do NOT verify your own work (VERA/CATO/NOMOS do that next).
