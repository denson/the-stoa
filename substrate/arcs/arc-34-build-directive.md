# Arc 34 build directive — Canonification batch 2 (4 small discipline tightenings)

**Audience:** the fresh Claude Code session opened to build Arc 34 deliverables (MAJOR_PLINY at the-stoa tier).
**Authored by:** user-tier MAJOR_POLYBIUS + the PRINCIPAL (Denson Smith).
**Status:** active directive. **Arc 33 (`stoa--32b.2`) is CLOSED**; precondition satisfied.
**Bw ticket:** `stoa--y14` (the work-unit; bundles C1-C4 candidates).
**Builds on:** Arcs 1-33 (the-stoa main as of `789496b`).

**Your one job:** ship four small discipline tightenings as a single coherent canonification arc. Mirrors the Arc 32 (stoa--ewn) bundling pattern. Each candidate has empirical anchor + clear fix shape + small surface.

One ticket, one coherent push:
- **stoa--y14** (P2) — four candidates C1-C4. Body has empirical anchors + fix-shape options + acceptance + cross-refs + §15 N=1 framing. **DAEDALUS treats ticket body as primary input prose alongside this directive.**

This is small-to-medium scope substrate-canon work — comparable to Arc 32 / stoa--ewn shape (multi-file canon + template touches). Each individual change is small. Single DAEDALUS round expected; ARGUS revisions possible on C1's Option A/B/C pick + C4's Option α/β/γ pick.

---

## Comms — autonomous mode via bw, radio-check protocol

Same shape as Arcs 25-33. PROJECT-TIER POLYBIUS (separate session, activated from `HUMAN_paste-polybius-arc-34-instruction.md`) is your radio-check peer; you communicate via comments on `stoa--y14`. USER-TIER POLYBIUS dispatched this arc + will do QA pass at arc close per PRINCIPAL's pattern.

PRINCIPAL is **not** the relay for routine status — beadwork is.

**bw command syntax** is in `substrate/MAJOR_PLINY.md` §6.1. `bw comment <id> "text"` is positional. `bw close <id> --reason "text"` — `--reason` is a flag.

**Polling discipline** per `substrate/operating-disciplines.md` §7. On dispatch, post init handshake on `stoa--y14` naming cron id + cadence. Heartbeat every ≤30 min.

PLINY in autonomous mode. PRINCIPAL + user-tier POLYBIUS are exception-handlers per Arc 31 §25 escalation triggers — PRINCIPAL-gate clauses are BLOCKS (halt + escalate immediately), not TAGS.

---

## Read first

Before any design or build work, read in order:

1. **`bw show stoa--y14` ticket body in full.** Primary spec. Body has C1-C4 with empirical anchors + fix-shape Options + out-of-scope hard-locks + §15 N=1 framing.

2. **Source tickets folded as candidates:**
   - **`bw show stoa--k36`** (C1 — user-tier-to-main discipline)
   - **`bw show stoa--f37`** (C2 — HUMAN_paste accumulation)
   - **`bw show stoa--3qi`** (C3 — template-title cosmetic)
   - **`bw show stoa--ize`** (C4 source — HITL-paused queue sweep was surfaced via this investigation)

3. **`substrate/MAJOR_POLYBIUS.md`** — current section structure. C1 + C4 may add sections here.

4. **`substrate/MAJOR_PLINY.md` §5.9 + §5.10** (Arc 30 + Arc 32 pre-branch + signoff-accuracy) — C2 may add arc-close discipline alongside.

5. **`substrate/operating-disciplines.md`** — possible cross-ref locus for C1 + C4.

6. **`substrate/templates/paste-instruction-template.md`** — C3 fixes title; C4 may add HITL-paused-queue section if DAEDALUS picks Option γ.

7. **`substrate/templates/handoff-doc-template.md`** — C4 candidate locus for HITL-paused-queue handoff section.

8. **Arc 32 (stoa--ewn) directive at `substrate/arcs/arc-32-build-directive.md`** — the precedent bundling pattern this arc mirrors.

---

## Phase A — Architectural decisions (LOCKED pre-dispatch)

### A1. One arc, four phases, one gauntlet — LOCKED

`stoa--y14` is a coherent single work-unit bundling 4 candidates. Single DAEDALUS design. Single ARGUS audit. Single ADA worktree on `arc-34/build` per §5.9.4 (worktree at `.claude/worktrees/arc-34-build/`). Verifiers (VERA + CATO + ZENO) each one pass. **CATO mandatory** — substrate canon; wording precision matters.

Phasing:

| Phase | Seat(s) | Output |
|---|---|---|
| 1 | DAEDALUS + ARGUS | `agents/design/arc-34/design.md` — integrated design covering C1 user-tier-to-main discipline (Option A/B/C pick), C2 archival convention (Option α/β/γ pick), C3 template-title fix, C4 HITL-paused queue sweep (Option α/β/γ pick). ARGUS cold-audits. |
| 2 | ADA | feature branch `arc-34/build` in separate worktree per §5.9.4. |
| 3 | VERA + CATO + ZENO | parallel verification pass per Phase B acceptance probes. |
| 4 | PLINY + smoke + ship | smoke beats per Phase C. PR opened. PLINY runs `gh pr merge` after clean PASS. `stoa--y14` closes. PLINY signoff per §5.10 (live-verified cleanup claims). **User-tier POLYBIUS does QA pass at arc-close per PRINCIPAL pattern.** Source tickets stoa--k36 + stoa--f37 + stoa--3qi + stoa--ize close with cross-refs at the same time. |

### A2. C1 — User-tier-to-main commit discipline — LOCKED scope; DAEDALUS picks form

Encode what user-tier may direct-commit to main (currently implicit; recurring). Per stoa--y14 body:

- **Option A — explicit discipline section** at MAJOR_POLYBIUS.md (or operating-disciplines.md cross-ref) naming what user-tier may commit directly: directive+activation-paste tracking commits, substrate-tool self-apply (apply.sh-driven), orphan cleanup (worktrees, branches), retro docs at docs/sessions/, bw via orphan branch (always safe).
- **Option B — strict (everything through arc)** — too restrictive; not recommended.
- **Option C — composite: discipline section + CLAUDE.md update acknowledging the exception explicitly.**

User-tier POLYBIUS recommends Option C.

### A3. C2 — HUMAN_paste-*.md archival convention — LOCKED scope; DAEDALUS picks form

Encode arc-close cleanup convention. Per stoa--y14 body:

- **Option α — archive on arc close:** PLINY moves to substrate/arcs/<N>/pastes/ subdirectory.
- **Option β — delete on arc close:** PLINY deletes; recoverable via git history.
- **Option γ — leave + accept.**

User-tier POLYBIUS recommends Option α (parallel to existing substrate/arcs/arc-N-build-directive.md archival pattern). The convention encoding lives at MAJOR_PLINY.md alongside §5.10 (same family: arc-close discipline).

### A4. C3 — Template-title fix — LOCKED scope

Cosmetic fix to substrate/templates/paste-instruction-template.md title to reflect dual PLINY+POLYBIUS targeting (per Arc 32 C2 making cron-hygiene clause dual). DAEDALUS picks exact wording.

### A5. C4 — HITL-paused queue sweep discipline — LOCKED scope; DAEDALUS picks form

Encode periodic-sweep discipline so paused-pre-dispatch tickets don't sit invisibly. Per stoa--y14 body:

- **Option α — POLYBIUS activation checklist addition** at MAJOR_POLYBIUS.md §9 (after `bw prime` step): sweep open epics for HITL-paused indicators; surface findings in first turn.
- **Option β — handoff-doc-template addition** at substrate/templates/handoff-doc-template.md: new "HITL-paused queue" section.
- **Option γ — both (defense in depth).**

User-tier POLYBIUS recommends Option γ.

### A6. Cite-comment discipline — LOCKED

Cross-references between C1/C2/C3/C4 + adjacent canon (§5.9 + §5.10 for C2; §9 activation checklist for C4; existing CLAUDE.md feature-branch rule for C1) should resolve via cite at every read-site. Pattern same as Arc 26 / 28 / 29 / 30 / 31 / 32 / 33 cite-comments.

### A7. Authorship attribution — IMMUTABLE per CLAUDE.md

All edits credit Denson Smith. Arc 34 edits existing files (no new files with fresh author-like field exposure expected; possibly the template fix adds author back). Verify before commit.

### A8. Out of scope — HARD LOCKED (per stoa--y14 body)

Do NOT do in this arc:

- stoa--32b.2 mechanical-script/agent-inspection split — shipped via Arc 33.
- stoa--ize Arc 22 disposition (stoa--jru) — separate forthcoming Arc 36.
- stoa--vz9 universal disciplines promotion — separate forthcoming Arc 37.
- stoa--kjo per-agent git identity — separate forthcoming Arc 35.
- u--7yg.16 envelope tool-set gaps — separate audit; not folded.
- u--7yg.21 .claude/ gitignored — operational truth; not actionable.
- ariadne--1of agent-team-on-beadwork — product epic; separate prioritization.
- s4--bbz sector-4 MVP — paused per PRINCIPAL until stoa work complete.

If you find yourself reaching for any of the above, STOP and surface as substance-disagreement comment on `stoa--y14` (radio-check to user-tier POLYBIUS via [for: user-tier POLYBIUS] tag).

### A9. §15 N=1 honesty — LOCKED per-candidate

Each candidate has empirical anchors named in stoa--y14 body. Substrate canon enters off-gate on PRINCIPAL declaration; future-evidence accretion per §6.7.1 gate. Each new canon section must name PRINCIPAL-declaration provenance + empirical anchor + accretion path — same shape as Arc 27 §16.6 / Arc 29 §17.1 / Arc 30 §5.9.3 / Arc 31 §25.6 / Arc 32 §19.6 / §5.10 / §5.9.4 / Arc 33 §27 N=1 framings.

### A10. Pre-branch hygiene per §5.9 + worktree convention per §5.9.4 — SELF-APPLIED

Before creating `arc-34/build`, verify the two-check rule. Use separate worktree at `.claude/worktrees/arc-34-build/` per §5.9.4.

User-tier POLYBIUS confirmed at dispatch authoring: local main = origin/main at `789496b`; no orphan arc-build branches.

### A11. Signoff-accuracy per §5.10 + attestation-honesty per §19.6 — SELF-APPLIED

PLINY's signoff at arc close must live-verify cleanup claims (branch deletion, worktree removal, PR merge); attestations cite live-verified state.

### A12. Source-ticket closure — LOCKED

On Arc 34 ship, close source tickets in addition to stoa--y14:
- stoa--k36 (folded as C1) — close with cross-ref to Arc 34 merge commit
- stoa--f37 (folded as C2) — close with cross-ref
- stoa--3qi (folded as C3) — close with cross-ref
- stoa--ize (the sweep that surfaced C4) — close with cross-ref + note "Arc 22 disposition tracked in Arc 36 / stoa--jru refresh + dispatch"

---

## Phase B — Verify (probes for VERA)

1. **C1 discipline section present** with explicit "what user-tier may direct-commit to main" list + cross-ref to CLAUDE.md (if Option C picked).
2. **C2 archival convention present** with arc-close PLINY discipline; if Option α picked, substrate/arcs/<N>/pastes/ pattern documented.
3. **C3 template-title fixed** to reflect dual PLINY+POLYBIUS targeting.
4. **C4 HITL-paused-queue-sweep encoded** per DAEDALUS Option pick; activation-checklist step + template section as applicable.
5. **Cite-comments resolve** between candidates + adjacent canon.
6. **§15 N=1 framing per candidate** — each section names provenance + empirical anchor + accretion path.
7. **Source tickets closed** with cross-refs (stoa--k36 + stoa--f37 + stoa--3qi + stoa--ize).
8. **CURRENT regression:** check.sh against the-stoa workspace shows expected DRIFTED on edited substrate files.

CATO cold-reads:
- diff for wording drift, scope creep, cite-comment correctness, cross-reference correctness, authorship attribution
- §15 N=1 honesty — no over-generalization in any of the 4 canon sections
- Tone consistency with Arcs 27-33 substrate-canon sections

ZENO checks stoa--y14 deliverables C1-C4 each marked DONE by artifact reference + source-ticket closures verified.

---

## Phase C — Smoke + ship

PLINY's smoke beats before opening PR:

- `grep -n "user-tier.*direct-commit\|direct-commit.*main" substrate/MAJOR_POLYBIUS.md substrate/operating-disciplines.md` — C1 present.
- `grep -n "archive on arc close\|substrate/arcs/.*/pastes/" substrate/MAJOR_PLINY.md` — C2 present.
- `grep -E "PLINY.*POLYBIUS.*activation|POLYBIUS.*PLINY.*activation" substrate/templates/paste-instruction-template.md | head -3` — C3 title fixed.
- `grep -n "HITL-paused\|paused-pre-dispatch.*sweep" substrate/MAJOR_POLYBIUS.md substrate/templates/handoff-doc-template.md` — C4 encoded per DAEDALUS Option pick.
- check.sh against the-stoa — expected DRIFTED on substrate files this arc edits.

PR title: `Arc 34: canonification batch 2 — C1 user-tier-to-main + C2 paste accumulation + C3 template-title + C4 HITL-paused queue sweep`
PR body: cross-ref `stoa--y14`, source tickets `stoa--k36` + `stoa--f37` + `stoa--3qi` + `stoa--ize`, Arc 32 / stoa--ewn precedent, this directive at `substrate/arcs/arc-34-build-directive.md`.

Merge via `gh pr merge` after clean gauntlet PASS. **PLINY signoff per §5.10:** live-verify cleanup. Close `stoa--y14` with `--reason` referencing the merge commit. Close source tickets per A12. Tag `[for: user-tier POLYBIUS]` on `stoa--y14` inviting QA pass.

---

## Honest scope reminder

Small-to-medium substrate-canon arc. Smaller than Arc 33; comparable to Arc 32 (stoa--ewn shape). DAEDALUS round + possible 1 ARGUS revise round; ADA build; full verifier round; smoke + ship per §5.10. ~45-90 min CAPTAIN-agent wall-clock estimated.

End directive.
