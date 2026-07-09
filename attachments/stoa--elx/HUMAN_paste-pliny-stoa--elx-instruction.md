# Engagement brief — PLINY_the-stoa (orchestrator) — stoa--elx: bw bootstrap into the install process (arc-75)

Read .claude/MAJOR_PLINY.md and assume the orchestrator role for the-stoa.

## Chain of command (supersedes the directive's comms section on ONE point)

PRINCIPAL → Polybius the Grand → Polybius the Decider (user-tier) → POLYBIUS_the-stoa (FM — **your only up-channel**) → YOU → CAPTAINs. The directive names the retired "Polybius_the_Stoa" as owner — the user-tier seat is now **Polybius the Decider**, reached through the FM only. Everything else in the directive stands.

## Authoritative spec (read in order; do NOT re-derive from memory)

1. `substrate/arcs/arc-75-build-directive.md` on main — DC1–DC8, deliverables, DoD, out-of-scope, phasing. It is your work order.
2. `git show beadwork:attachments/stoa--elx/plan-bw-bootstrap-v2.md` — the Grand-GATED plan; authoritative on conflicts.
3. The stoa--elx comment trail (the Grand's GATED GO + hard conditions).

## Base-drift warning

Directive anchored at main @7d20b5f; you build off CURRENT main **@cfd683d7**. Arc-p0e has since EDITED install.sh (comment fixes, SKILL_NAMES, author-gate retirement) — GROUND-CHECK every cited install.sh/SKILL.md anchor against current main before DAEDALUS designs and before ADA edits. The author deny-gate no longer exists; authorship is enforced by doctrine audits + the attribution advisory (report-only).

## Execution shape (from the directive — BY-THE-BOOK, not one-pass)

- Isolated worktree + `stoa--elx/build` branch off clean main. Pre-branch hygiene disclosure first (the parked arc-76-build worktree is KNOWN and dispositioned LEAVE — do not touch, do not re-ask).
- **Phase A**: DAEDALUS resolves DC1–DC8 (DC2 registry-safe Windows USER PATH append + DC3 two-independent-checks are load-bearing); ARGUS cold-audits the PATH mechanism + supply-chain surface; surface to the FM for go/no-go BEFORE build.
- **Phase B**: ADA builds the one slice — helper + install.sh `--bootstrap-bw` flag + install-stoa canon reversal.
- **Phase C**: VERA real-execution probes (idempotent skip on THIS machine; registry-safe append exercised against a THROWAWAY value — NEVER this machine's real USER PATH; DC3 false-green demonstrably caught; SHA256 fail-closed on a corrupted zip; Unix delegates to upstream; install.sh absent-flag byte-unchanged via dry-run diff) + full app suite (gen-data deterministic + vitest) + CATO + NOMOS.
- **Phase D**: commit(s) Author = Denson Smith + your/ADA seat trailers per §28; update stoa--elx with SHA + per-DC dispositions; hand back to the FM. **NOT merged, NOT pushed — this arc has a SECOND GRAND GATE on the built artifact before any merge.**

## Disciplines

- D-A / D-B (re-read bw immediately before any irreversible-ish act) / D-C; quiesce-cold at gates; supersede-must-revoke; 10-minute liveness on expected pickups; coverage claims precise per-commit.
- bw: positional `bw comment`, no backticks/`$()` in bodies; `bw prime` at activation; sign `[from: PLINY_the-stoa | sid <sid>]`.

## What you do NOT do

Merge; push; mutate this machine's real Windows USER PATH or its working bw; re-implement upstream's Unix installer; wire the u--9s2 call-site; edit the historical arc-19 directive; move install-stoa into substrate/skills; surface to user-tier direct (except scope disputes) or PRINCIPAL ever.

## Close signal

`CLOSE ME — stoa--elx gauntlet complete; awaiting FM verification + user-tier close-gate + the Grand's built-artifact gate`

## Compaction recovery

`git show beadwork:attachments/stoa--elx/HUMAN_paste-pliny-stoa--elx-instruction.md`
