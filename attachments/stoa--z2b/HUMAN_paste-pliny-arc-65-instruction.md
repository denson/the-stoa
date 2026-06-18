# Engagement brief — PLINY_the-stoa (orchestrator) — Arc 65 (fix authorship-gate false-positive, z2b)

Read `.claude/MAJOR_PLINY.md` and assume the orchestrator role for the-stoa. You are **PLINY_the-stoa** for this engagement. Run `bw prime` at activation.

## Three-tier chain (your position)

PRINCIPAL → user-tier POLYBIUS (close-gate + merge) → POLYBIUS_the-stoa (floor-manager) → **YOU (orchestrator)** → CAPTAINs. You surface to the **FLOOR-MANAGER**, NOT user-tier direct.

## Scope

Fix `stoa--z2b` — narrow the authorship-gate matcher so it stops false-positiving on `.md` BODY prose, **while still catching a real structured author field naming a non-Denson PERSON** (the regression the gate prevents — it has happened twice; this is CRITICAL per global `~/.claude/CLAUDE.md`).

**SPEC (authoritative) is on beadwork** (it can't be committed to main — it would trip the gate it fixes): `git show beadwork:attachments/stoa--z2b/arc-65-build-directive.md` — read it end-to-end. Ticket: **`stoa--z2b`**.

Fix surface: `substrate/hooks/_hooklib.sh` (`extract_author_fields`) + `substrate/hooks/pretooluse-author-field-audit.sh` (`is_author_encoding_file` / value-check) + the `.claude/hooks/` DEPLOYED mirrors (the-stoa is the forge — land source + deployed together). Root cause: `is_author_encoding_file` matches ALL `*.md`, and `extract_author_fields` pulls any `author|by|owner|...` + `:`/`=` from anywhere in the blob (body prose, code-spans, markdown-bold included). Config-file (JSON/TOML) extraction is safe — keep it.

Deliverables: (1) narrow `.md` matching (frontmatter-only and/or skip code-spans/bold — DAEDALUS rules with ARGUS); (2) a TEST CORPUS — false-positive fixtures that must now PASS (the real z2b instances) + true-positive fixtures that must still BLOCK (a `package.json` author naming a fictional non-Denson person, an SKILL.md frontmatter author naming a non-Denson person, a LICENSE/NOTICE naming a non-Denson person); (3) source+deployed mirror; (4) doc-update the gate header/README. Forward work on an **`arc-65/build`** branch (pre-branch hygiene first).

## Run

Full gauntlet DAEDALUS → ARGUS → ADA → VERA → CATO → NOMOS. **This is a SECURITY gate — the adversarial TRUE-POSITIVE corpus is load-bearing, not a formality.** VERA must drive the attack path (a real author field naming a non-Denson person must STILL be DENIED after the narrowing) — both directions GREEN, not just "false-positives fixed". ARGUS cold-audits for a gap a real violation could slip through. Surface the DESIGN-LOCK to the floor-manager post-ARGUS / pre-ADA: the narrowing strategy (Q-A), body-author-line coverage (Q-B), the optional value heuristic (Q-C), and the corpus design.

Self-test (ironic but real): the fixed gate must ACCEPT this arc's own build-commit prose, AND a live re-probe must show the Arc-61 `**Authored by:**` line commits clean while a `package.json` with a non-Denson author is DENIED (throwaway file, do not pollute main). The gate must still FAIL-OPEN on script error.

NOTE: the build commits land on main normally; only the DIRECTIVE doc is on beadwork (gate chicken-and-egg). After the fix lands, user-tier commits the directive to main.

## Polling (all three disciplines)

- **D-A** (copy-all-output): every CAPTAIN echoes significant outputs to bw on `stoa--z2b`.
- **D-B** (poll-at-breakpoints): read bw between every CAPTAIN dispatch.
- **D-C** (poll-during-surface-and-wait): Monitor/sleep at ~2–3 min during surface-and-wait.

## Hand-back

At CATO/NOMOS PASS, post on `stoa--z2b` addressed to **POLYBIUS_the-stoa (floor-manager)** — NOT user-tier direct.

## You do NOT

Merge, push, apply to deployed instances, arm a live `settings.json`, relay direct to user-tier (except scope disputes), or surface to PRINCIPAL except emergencies.

## Close-signal

`CLOSE ME — arc 65 (stoa--z2b) gauntlet complete; awaiting user-tier POLYBIUS close-gate + merge`.

## Compaction-recovery

Re-fetch: `git show beadwork:attachments/stoa--z2b/HUMAN_paste-pliny-arc-65-instruction.md`. bw syntax: positional `bw comment <id> "text"` (never `-m`).
