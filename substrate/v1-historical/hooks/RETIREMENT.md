# Retirement record — authorship deny-gate (`pretooluse-author-field-audit.sh`)

**Retired:** Arc `stoa--p0e` (2026-07-09), per the PRINCIPAL SCOPE-RESHAPE ruling
(`stoa--p0e`, 2026-07-09T09:07:01Z). **Author:** Denson Smith.

> This is HISTORY explaining WHY the retirement is correct. The items below are
> **not fix-targets** — they are the record of what the gate did, why the PRINCIPAL
> judged it net-negative, and what replaced it. Do not "fix" the gate; it is
> retired by decision, not by defect-to-be-patched.

## What was retired

- **The deny-hook:** `pretooluse-author-field-audit.sh` (a `PreToolUse` /
  `Bash(git commit*)` gate) — archived here (not deleted). Its registration was
  removed from `.claude/settings.json` and `substrate/templates/settings-hooks.json`.
- **Its regression corpus:** `run-author-gate-tests.sh` + `fixtures/{tp,fp,control}/`
  — archived here (`substrate/v1-historical/hooks/tests/`).

## What was KEPT

- **`_hooklib.sh` stays** in `substrate/hooks/` — the two surviving Bash gates
  (`pretooluse-clean-tree-before-branch.sh`, `pretooluse-no-dash-m-bw-comment.sh`)
  and the Stop self-check source it. The now-dead author-specific functions
  (`classify_author_file`, `extract_author_fields`, `parse_allow_pairs`) are LEFT
  INTACT: pruning a shared lib for zero runtime benefit risks a subtle break in a
  surviving gate; a future arc may prune them under a proven-zero-caller check.
- **`.claude/hooks/principal-identity`** (the allow-list) stays seeded — the new
  `attribution-advisory` skill's SECONDARY check reuses it.
- **`CLAUDE.md` §4 authorship doctrine** stays PRIMARY, untouched.

## What replaced it

The report-only, never-blocking **`attribution-advisory` skill**
(`substrate/skills/attribution-advisory/`). Its PRIMARY check surfaces a diff hunk
that MODIFIES or DELETES an existing attribution line — the plagiarism /
license-breach direction the deny-gate never checked. It NEVER denies; it writes a
report to `.claude/attribution-advisory-report.md`. Direction-2 (plagiarism)
coverage NET INCREASES via this advisory; the direction-1 residual (an agent
writing a non-PRINCIPAL name into its OWN new artifact) is covered by the doctrine
(PRIMARY) + the advisory's SECONDARY best-effort check.

## Why retirement is correct — the record

1. **`stoa--dps` — the PEP 621 inline-table false-positive.** A `pyproject.toml`
   `authors = [{name = "..."}]` inline-table form parsed as a false author-field
   match, producing a ~3-day false-positive HOLD on legitimate work. The gate
   blocked correct commits.
2. **The Bash-only matcher hole.** The gate registered on `Bash(git commit*)`.
   A commit issued from PowerShell (or any non-Bash shell surface) was never
   matched — the gate had a coverage hole it could not close from its matcher.
3. **The compound `cd && git commit` matcher dodge.** The prefix-anchored `if`
   matcher (`Bash(git commit*)`) did not fire on a compound command that led with
   `cd ... &&` before `git commit`, so the gate was trivially dodge-able. (Dodging
   a gate to get a commit through is itself the footgun the retirement removes —
   the gate created pressure to route around it.)
4. **The empirical (arc-77).** Across arc-77, doctrine-driven authorship audits
   verified authorship correct FOUR times independently. Over the gate's life it
   contributed, net, a false-positive hold (item 1) + a discovered coverage hole
   (items 2–3) — not a caught real violation. The deterministic backstop the gate
   was meant to be was carried, in practice, by the prose doctrine + manual audit.

## Direction it never covered (the reshape's purpose)

The deny-gate only ever checked **direction-1** (an agent writing a NON-PRINCIPAL
name into its OWN new artifact). It never checked **direction-2** — the real harm
the PRINCIPAL named: another author's credit being REPLACED WITH the PRINCIPAL's in
quoted material / imported OSS (plagiarism / license-breach). Retiring the gate and
building the advisory shifts coverage toward the direction that actually matters.

**Cited:** `stoa--dps` (PEP 621 false-positive), `stoa--eby`, Arc 46 / 65 / 69 hook
history, the `stoa--p0e` SCOPE-RESHAPE ruling.
