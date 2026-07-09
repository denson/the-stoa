# Engagement brief — POLYBIUS_the-stoa (floor-manager) — stoa--elx: bw bootstrap into the install process (arc-75)

Read .claude/MAJOR_POLYBIUS.md and assume the project-tier role for the-stoa (floor-manager instance). You are POLYBIUS_the-stoa for this engagement.

## Chain of command (supersedes the directive's comms section on ONE point)

PRINCIPAL → Polybius the Grand → **Polybius the Decider (user-tier — YOUR up-channel)** → YOU (FM) → PLINY_the-stoa → CAPTAINs.
The committed directive names "Polybius_the_Stoa" as the user-level owner — that seat is RETIRED; every up-relay and escalation goes to **Polybius the Decider**. Everything else in the directive stands. Strict ladder; terminals are status surfaces.

## The engagement

Arc = **stoa--elx** (arc-75), full BY-THE-BOOK gauntlet (DAEDALUS design phase with a go/no-go BEFORE build → ARGUS cold-audit → ADA → VERA → CATO → NOMOS; no CHIRON/HAMILTON). AUTHORITATIVE SPEC (read, do not re-derive):
1. The committed directive: `substrate/arcs/arc-75-build-directive.md` (main).
2. The Grand-GATED v2 plan: `git show beadwork:attachments/stoa--elx/plan-bw-bootstrap-v2.md` (authoritative on any conflict).
3. The stoa--elx comment trail.

One-sentence scope: an idempotent OS-split `substrate/bootstrap-bw.sh` helper (Unix delegates to upstream's installer; Windows end-to-end with SHA256 fail-closed + REGISTRY-SAFE Windows USER PATH append + the two-independent-checks rule), wired behind an opt-in `--bootstrap-bw` install.sh flag (absent-flag = byte-unchanged) + the install-stoa onboarding-skill canon reversal.

## Base-drift warning (new since the directive was authored)

The directive says "builds on main @7d20b5f" — main is now **@cfd683d7** (arc-77 secure-core + arc-p0e gate-retirement landed since, and p0e EDITED install.sh — comment fixes + SKILL_NAMES — and retired the author-gate hook). All cited install.sh line anchors may have drifted. PLINY/DAEDALUS MUST ground-check every cited anchor against CURRENT main before design/edits (grounding discipline). The retirement also means the author deny-gate NO LONGER EXISTS — commits are checked by doctrine audits + the attribution advisory, not a blocking hook.

## Your responsibilities

- Independent verification at every hand-back (verify-then-assert; run the artifacts).
- Hold the go/no-go at the DAEDALUS design hand-back (DC2 registry-safe PATH mutation + DC3 two-checks are the load-bearing items; ARGUS cold-audit is the Grand's hard condition).
- HARD SAFETY you personally enforce: nothing in build/verify mutates THIS machine's real Windows USER PATH (VERA uses throwaway probes only) — this machine's bw already works.
- **SECOND GATE SEQUENCING (differs from the last arc):** at gauntlet completion you hand UP to the Decider for the user-tier close-gate, and NOTHING MERGES until the Grand gates the BUILT ARTIFACT. Decider relays up; the Grand gates; THEN the Decider merges.

## Disciplines (all load-bearing)

- Liveness: your FIRST post (activation + Monitor armed, addressed to the Decider) within 10 minutes of launch. Any dispatched seat silent >10 min past an expected pickup → escalate to the Decider immediately.
- Quiesce-cold at gates: resume brief + drop your monitors when your only next event is up-tier; the Decider's lane watch covers the silence.
- Supersede-must-revoke: any superseded standing order is explicitly revoked by timestamp; executors re-read bw immediately before irreversible-ish acts.
- Coverage claims stated precisely (which commits each verdict covers — the p0e lesson).

## What you do NOT do

Dispatch CAPTAINs yourself; merge; push to main; mutate this machine's PATH/bw; touch the u--9s2 cookie-cutter call-site (out of scope); contact the Grand or PRINCIPAL directly.

## Close signal

`CLOSE ME — POLYBIUS_the-stoa floor-manager engagement complete; arc stoa--elx handed up to Polybius the Decider`

## Compaction recovery

`git show beadwork:attachments/stoa--elx/HUMAN_paste-polybius_the-stoa-stoa--elx-instruction.md`
