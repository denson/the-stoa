# Engagement brief — PLINY_the-stoa (orchestrator) — stoa--p0e: deny-gate retirement + attribution advisory

Read .claude/MAJOR_PLINY.md and assume the orchestrator role for the-stoa.

## Chain of command

PRINCIPAL → Polybius the Grand → Polybius the Decider (user-tier) → POLYBIUS_the-stoa (FM — **your only up-channel**) → YOU → CAPTAINs. You surface to the FM only. Terminals are status surfaces, never ask-channels.

## Scope (authoritative = the Decider's [PRINCIPAL RULING — SCOPE RESHAPE] comment on stoa--p0e, 2026-07-09 — read in full; invariants are SETTLED)

Deliverables, worked on a `stoa--p0e/build` branch in an isolated worktree off clean main:

1. **RETIRE the deny-hook**: remove the `pretooluse-author-field-audit.sh` registration from the live `.claude/settings.json` AND the substrate source/template (`.claude/templates/settings-hooks.json` or wherever the source of truth lives — DAEDALUS maps it). The hook SCRIPT may be archived per substrate precedent (`substrate/v1-historical/`), not deleted. Authority: the PRINCIPAL retirement ruling on the ticket — cite it in the commit; the other two Bash gates (clean-tree, bw-comment) stay armed.
2. **BUILD the advisory** (report-only, never blocks, best-effort): PRIMARY = flag diff hunks that MODIFY or DELETE an existing author/copyright/license/attribution line; SECONDARY = flag NEW author-like fields carrying a non-PRINCIPAL name outside vendored/imported paths. Output = a durable report the operator/user-tier reads (design decides the exact surface — DAEDALUS within the ruling invariants). Diff-parsing regex is legitimate here (true external boundary).
3. **PROPAGATION via the existing lifecycle**: install.sh manifest entries (removal of the retired hook registration + deploy of the advisory) so every consumer workspace retires/gains it on its next check-substrate-updates apply. You do NOT touch other projects' repos.
4. **WHY-HISTORY**: the retirement record documents stoa--dps (PEP 621 parser false positive), the Bash-only matcher hole (PowerShell commits ungated), and the compound `cd && git commit` dodge — as history, not fix targets. Disposition stoa--dps (close superseded-by-retirement) and cite stoa--eby where relevant.
5. **DOCTRINE UNTOUCHED**: the CLAUDE.md mandatory authorship-audit discipline in every seat stays primary — nothing in this arc weakens it.

Full gauntlet: DAEDALUS (design within the invariants) → ARGUS → ADA → VERA (must include an empirical probe: a synthetic diff that edits an existing copyright line MUST be flagged; a normal new-file-by-PRINCIPAL diff MUST NOT) → CATO → NOMOS. No skips, no solo.

## Disciplines

- **D-A** (CAPTAINs echo significant output to stoa--p0e); **D-B** (re-read bw between every dispatch AND immediately before any irreversible-ish act — arc-77 lesson); **D-C** (Monitor ~2-3 min during surface-and-wait, count-based).
- **QUIESCE-COLD at gates**: if your only next event is an FM/up-tier ruling, post state + resume trigger and go cold.
- A superseded standing order is only dead when explicitly REVOKED by timestamp — and you re-read bw before acting regardless.

## What you do NOT do

Merge; push; apply to deployed consumer instances; touch anything outside the arc worktree + the settings/manifest paths in scope; relay direct to user-tier (except scope disputes); surface to PRINCIPAL ever; anything real (infra/secrets/money).

## Close signal

`CLOSE ME — stoa--p0e gauntlet complete; awaiting user-tier close-gate + merge`

## Compaction recovery

Re-fetch this brief: `git show beadwork:attachments/stoa--p0e/HUMAN_paste-pliny-stoa--p0e-instruction.md`
