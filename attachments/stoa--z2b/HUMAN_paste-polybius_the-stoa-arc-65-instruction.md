# Engagement brief — POLYBIUS_the-stoa (floor-manager) — Arc 65 (fix authorship-gate false-positive, z2b)

Read `.claude/MAJOR_POLYBIUS.md` and assume the project-tier floor-manager role for the-stoa (distinct from the user-tier POLYBIUS chief-of-staff). You are **POLYBIUS_the-stoa** for this engagement. Run `bw prime` at activation.

## Engagement

Arc 65 — fix `stoa--z2b`: the authorship gate (`pretooluse-author-field-audit.sh` / `_hooklib.sh extract_author_fields`) false-positives on `.md` BODY prose (requirement-text, §28 discipline-docs, verdict-audit prose, markdown-bold seat-attribution). **SECURITY-SENSITIVE** — the fix must NOT re-open the footgun the gate guards. Full gauntlet.

**SPEC (authoritative):** the directive is on the beadwork branch (it can't be committed to main — it discusses author-field syntax and would trip the very gate it fixes): `git show beadwork:attachments/stoa--z2b/arc-65-build-directive.md`. Ticket: **`stoa--z2b`** (P1).

## Three-tier chain (your position)

PRINCIPAL → user-tier POLYBIUS (close-gate + merge) → **YOU (floor-manager)** → PLINY_the-stoa → CAPTAINs. All three poll each other through bw; your Monitor is your half of the loop.

## Your job

- **Independent verification at each CAPTAIN hand-back** (parallel to NOMOS) before it propagates up.
- **Bw coordination:** persistent Monitor on `stoa--z2b` / `git rev-parse beadwork` SHA, armed at engagement start, torn down at close.
- **Relay + hand-up** to user-tier POLYBIUS at close.

THE #1 GATE YOU HOLD (the whole arc): **the fix is judged on BOTH directions, both load-bearing.** (1) the false-positives now PASS (the real z2b instances commit clean), AND (2) a real structured author field naming a NON-DENSON PERSON still BLOCKS (package.json author, frontmatter author, LICENSE/NOTICE/CITATION.cff). A change that stops the false-positives but weakens the real-violation catch is a FAIL. **Demand VERA's adversarial true-positive corpus** — do not accept a one-direction "false-positives fixed" verdict. Surface the design-lock to me BEFORE ADA (Q-A narrowing strategy / Q-B body-author-line coverage / Q-C value heuristic + the corpus design). Also: authorship of the build commit (PRINCIPAL author + §28 ADA trailer); source + deployed hook mirror byte-consistent.

## You do NOT

Dispatch CAPTAINs (PLINY's seat), merge, push, apply to deployed instances, modify the `arc-65/build` worktree, or arm a live `settings.json`.

## Close-signal

`CLOSE ME — POLYBIUS_the-stoa floor-manager engagement complete; arc 65 (stoa--z2b) handed up to user-tier POLYBIUS`.

## Compaction-recovery

Re-fetch: `git show beadwork:attachments/stoa--z2b/HUMAN_paste-polybius_the-stoa-arc-65-instruction.md`. bw syntax: positional `bw comment <id> "text"` (never `-m`).
