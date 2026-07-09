# DAEDALUS design brief — stoa--p0e: deny-gate RETIREMENT + report-only attribution ADVISORY

**From:** PLINY_the-stoa (orchestrator) · **To:** CAPTAIN_DAEDALUS (architect) · **Arc:** stoa--p0e
**operating-mode:** autonomous · **Worktree root (write here):** `C:\Users\denso\claude_projects\the-stoa\.claude\worktrees\stoa--p0e-build`
**Coordination ticket (echo significant output):** `stoa--p0e`

---

## 0. What changed and why (read first)

An earlier brief on this arc (attached to `stoa--p0e`) asked to *extend* the deterministic author-field deny-gate (CI Action + Sonnet-5 adjudication + wider term list). **That framing is SUPERSEDED.** The PRINCIPAL, via Polybius the Decider (`stoa--p0e` comment 2026-07-09T09:07:01Z — the `[PRINCIPAL RULING — SCOPE RESHAPE: deny-gates RETIRED]`), **RETIRED all authorship deny-gates**. Your design works within that ruling. The invariants below are SETTLED — do NOT reopen them; design *within* them.

**Why the reshape (PRINCIPAL's framing, for your grounding — not a design question):**
- Git identity already records agent work as the PRINCIPAL's (Author + seat trailers). That structural layer stands; no gate needed for it.
- The real harm is the *opposite* direction from what the deny-gate checked: *other* authors' names getting REPLACED WITH the PRINCIPAL's in quoted material / imported OSS (plagiarism / license-breach direction). An allowlist deny-gate both misses that direction AND pressures agents toward it ("fields must say Denson Smith or the commit dies").
- Empirical: arc-77 doctrine-driven seat audits verified authorship correct 4× independently; the deny-hook contributed only a 3-day false-positive hold + a discovered coverage hole.

---

## 1. SETTLED INVARIANTS (do not reopen — design within these)

1. **RETIRE the deny-hook.** Remove the `pretooluse-author-field-audit.sh` *registration* from (a) the live `.claude/settings.json` AND (b) the substrate source/template. The hook SCRIPT is **archived** (substrate `v1-historical/` precedent), **not deleted**.
2. **The other two Bash gates STAY ARMED:** `pretooluse-clean-tree-before-branch.sh` and `pretooluse-no-dash-m-bw-comment.sh`. Do NOT touch them or the Stop/PostToolUse/SessionStart entries.
3. **BUILD the advisory:** report-only, never blocks, best-effort, diff-scoped.
   - **PRIMARY (direction 2):** flag any diff hunk that **MODIFIES or DELETES** an existing author/copyright/license/attribution line. (New files adding "Denson Smith" are normal; changing a line that already carried a name is almost never legitimate → naturally tiny false-positive rate.)
   - **SECONDARY (direction 1):** flag **NEW** author-like fields carrying a **non-PRINCIPAL** name **outside vendored/imported paths**.
   - **Output = a durable report the operator / user-tier reads. NEVER a deny.** "Best-effort that can only help" is the standing bar (nothing-has-to-be-100% ruling carries over).
   - Diff-parsing regex is legitimate here (true external boundary — a diff is a real external artifact).
4. **PROPAGATION via the existing lifecycle:** `install.sh` manifest entries so every consumer workspace retires the deny-hook AND gains the advisory on its next `check-substrate-updates` apply. You design the manifest deltas; you do NOT touch other projects' repos.
5. **WHY-HISTORY, not fix targets:** the retirement record documents (a) `stoa--dps` (PEP 621 inline-table `authors = [{name=...}]` parser false-positive), (b) the Bash-only matcher hole (PowerShell commits ungated), (c) the compound `cd && git commit` matcher dodge — as *history explaining why retirement is the right call*, NOT as bugs to fix. Disposition `stoa--dps` as superseded-by-retirement (ADA does the bw write; you note it in the design). Cite `stoa--eby` where relevant.
6. **DOCTRINE UNTOUCHED:** the `CLAUDE.md` mandatory authorship-audit discipline in every seat stays PRIMARY — nothing in this arc weakens it. Do NOT edit `CLAUDE.md` §4 / the audit discipline.
7. **NO keyed CI, NO API key, NO CLAUDE_CODE_OAUTH_TOKEN** for shared pipelines (ToS canon unchanged). The prior "Sonnet-5 adjudication / CI Action" deltas are DROPPED. The advisory is local/deterministic diff-regex only.
8. **install.sh HARD SAFETY CONSTRAINT preserved:** install.sh deploys scripts INERT; arming is `--enable-hooks` (DEFAULT OFF); never auto-writes a live settings.json. The advisory must respect this same posture (if it's a hook-shaped thing) OR be a plainly operator-invoked reporter that doesn't need arming at all — your call within the invariant.

---

## 2. GROUNDED FILE INVENTORY (PLINY recon — verify, don't trust blindly)

**Retirement targets:**
- **Live armed config:** `.claude/settings.json` (repo root) — the-stoa dogfoods with hooks ARMED. First `PreToolUse.Bash` hook entry is the `pretooluse-author-field-audit.sh` registration (`if: Bash(git commit*)`). Remove that one entry; keep the other two (`Bash(git *)` clean-tree, `Bash(bw comment*)` no-dash-m). This is a live-config edit — falls under install.sh's HARD SAFETY posture conceptually, but here it's the-stoa's own repo config, in-scope per the ruling ("remove … from the live .claude/settings.json").
- **Substrate template (source of truth for consumers):** `substrate/templates/settings-hooks.json` — same first entry (`{{HOOKS_DIR}}/pretooluse-author-field-audit.sh`). Remove it there too. Note this template also carries `startup|resume` substrate-check that the live root settings.json does NOT — do not disturb.
- **The script (ARCHIVE, don't delete):** `substrate/hooks/pretooluse-author-field-audit.sh` (also deployed at `.claude/hooks/pretooluse-author-field-audit.sh`). Archive the substrate copy to `substrate/v1-historical/` (precedent dir exists: currently holds role-file `.md`s + `templates/`; you decide the exact subpath, e.g. `substrate/v1-historical/hooks/`).
- **install.sh manifest:** hooks are **GLOB-discovered** from `substrate/hooks/*.sh` (no HOOK_NAMES list — see install.sh ~line 170). So archiving the script OUT of `substrate/hooks/` auto-removes it from the deploy glob — good, but confirm. `principal-identity` allow-list seeding lives at install.sh ~1479-1502 (`5c`-ish) — decide whether the advisory's SECONDARY (non-PRINCIPAL-name) check still needs it (likely yes) or whether it's retired with the gate. The `--enable-hooks` arming block is `5d` (~1508-1575).

**CRITICAL — must STAY (do not archive):**
- `substrate/hooks/_hooklib.sh` is **sourced by the surviving gates** (`pretooluse-clean-tree-before-branch.sh`, `pretooluse-no-dash-m-bw-comment.sh`, `stop-self-check.sh`, plus the best-effort session hooks). It contains `extract_author_fields` / `classify_author_file` that ONLY the retired gate used — but the FILE is shared. **Leave `_hooklib.sh` in place.** Recommend: leave the now-unused author functions intact (harmless; pruning a shared lib risks breaking a surviving gate — only prune if you can prove zero surviving caller and even then weigh the risk). Call this out as a design decision with your recommendation.

**Test corpus (author-gate-specific):**
- `substrate/hooks/tests/run-author-gate-tests.sh` + `substrate/hooks/tests/fixtures/{tp,fp,control}/` — these test the RETIRED gate. Design what happens to them: archive alongside the script vs. repurpose. The advisory needs its OWN test harness + fixtures (see §3 acceptance). `run-stop-self-check-tests.sh` tests a SURVIVING hook — leave it.

**Reference docs:**
- `substrate/hooks/README.md` — §2 THE AUTHORING RULE (self-contained payload: every trigger states WHY it fired + WHAT to do, inline). The advisory's report output should honor this spirit (each flagged hunk explains why + what to check). §5 SAFETY ARCHITECTURE. Update README to reflect retirement + the new advisory.

---

## 3. WHAT YOUR DESIGN MUST SETTLE (the real design work)

1. **Advisory mechanism + surface (the central open question).** Within invariant 3+8, decide WHAT the advisory *is* and WHERE its report lands. Candidate shapes to weigh (pick + justify, don't just list):
   - a standalone operator-invoked script (`git diff … | advisory`) writing a report file;
   - a report-only Stop-self-check contribution;
   - a non-blocking hook that only ever emits a report (never `deny`).
   The ruling says "a durable report the operator/user-tier reads." Name the exact report path/format and how the operator sees it. Respect: never blocks, best-effort, no API key.
2. **Diff-scoping precisely.** PRIMARY = modify/delete of an existing author/copyright/license/attribution line. Define the regex/term set for "attribution line" and the hunk-classification (a `-` line removing/changing a matched attribution, vs a pure `+` new-file addition). SECONDARY = NEW author-like field with a non-PRINCIPAL name outside vendored/imported paths — define "vendored/imported" path exclusion + how "non-PRINCIPAL" is determined (principal-identity allow-list reuse?).
3. **Archival mechanics** — exact source→dest for the script; confirm glob-deploy consequence; test-corpus disposition.
4. **install.sh deltas** — what lines change so consumers (a) stop deploying/registering the deny-hook and (b) start getting the advisory, all through the normal `--enable-hooks` / apply lifecycle. Keep the HARD SAFETY CONSTRAINT.
5. **check-substrate-updates interaction** — the advisory is a new deployable file; the retired hook is now an OBSOLETE file at a substrate-deployable path in consumer workspaces. Confirm the DRIFTED/MISSING/OBSOLETE three-category detection will correctly surface "retire the deny-hook, gain the advisory" on a consumer's next apply. (You don't build check-substrate-updates; you confirm the deltas play with it.)
6. **README + retirement record** — where the WHY-HISTORY (invariant 5) lives durably.

## 4. ACCEPTANCE BAR (design the probes; VERA will execute)

Your design MUST specify probes that let VERA empirically confirm (this is the SETTLED probe from the brief — bake it into the design):
- **P1 (MUST FLAG):** a synthetic diff that EDITS an existing copyright/author line → advisory flags it.
- **P2 (MUST NOT FLAG):** a normal new-file-by-PRINCIPAL diff (adds "Denson Smith" author field in a fresh file) → advisory stays silent.
- **P3:** the deny-hook is provably retired — no `pretooluse-author-field-audit.sh` registration in live settings.json OR the template; surviving two Bash gates + Stop/PostToolUse/SessionStart intact.
- **P4:** advisory NEVER exits non-zero / never denies (report-only proven).
- Spell out enough probe surface (fixtures + commands) that VERA can falsify each.

## 5. DELIVERABLE

Write `agents/design/stoa--p0e/design-rev1.md` in the worktree. Include:
- The retirement plan (concrete file/line edits) + the advisory design (mechanism, surface, diff-scoping, regex/term set).
- install.sh deltas + check-substrate-updates interaction.
- The probe specification (§4) explicit enough to execute.
- **Self-assessed weak points** (your standard closing section — where is this design most likely wrong / most fragile).
- A short "threats" enumeration (candidate M-items) so PLINY's A1 ratification-restatement beat has material to work from.

Keep it tight (within-arc artifact discipline). Echo a 3-5 line summary of your design + your top weak point to `stoa--p0e` via `bw comment` when done, signed `[from: CAPTAIN_DAEDALUS_the_stoa (subagent) | caller-sid 822aa122-41c9-4a76-9a87-cfe6e4fdf4c5]`. Return your verdict + the design path to PLINY.

**You do NOT build.** Design only. ADA builds after ARGUS critiques + the A1 beat.
