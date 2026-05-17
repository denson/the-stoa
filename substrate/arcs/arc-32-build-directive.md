# Arc 32 build directive — Canonification batch (5 small discipline tightenings)

**Audience:** the fresh Claude Code session opened to build Arc 32 deliverables (MAJOR_PLINY at the-stoa tier).
**Authored by:** user-tier MAJOR_POLYBIUS + the PRINCIPAL (Denson Smith).
**Status:** active directive. **Arc 31 (`stoa--32b.1`) is CLOSED**; precondition satisfied.
**Bw ticket:** `stoa--ewn` (the work-unit; 5 candidates C1-C5).
**Builds on:** Arcs 1-31 (the-stoa main as of `e315ca9`).

**Your one job:** ship five small discipline tightenings as a single coherent canonification arc. Each candidate has empirical anchor + clear fix shape + small surface. Bundled because they share theme (encode-as-canon rather than memory-only) + can ship together with low risk. Most are doc/canon additions or template-slot additions (similar shape to Arc 30's three-carrier framing).

One ticket, one coherent push:
- **stoa--ewn** (P2) — five candidates C1-C5. Body has empirical anchors + fix-shape options + acceptance + cross-refs + §15 N=1 framing. **DAEDALUS treats ticket body + the C5 scope-addition comment as primary input prose alongside this directive.**

This is medium-scope substrate-canon work — comparable to Arc 29 / Arc 31 in spread (multi-file canon edits) but each individual change is small. Expected ARGUS revisions normal given the breadth.

---

## Comms — autonomous mode via bw, radio-check protocol

Same shape as Arcs 25-31. PROJECT-TIER POLYBIUS (separate session, activated from `HUMAN_paste-polybius-arc-32-instruction.md`) is your radio-check peer; you communicate via comments on `stoa--ewn`. USER-TIER POLYBIUS dispatched this arc + will do QA pass at arc close per PRINCIPAL's pattern.

PRINCIPAL is **not** the relay for routine status — beadwork is.

**bw command syntax** is in `substrate/MAJOR_PLINY.md` §6.1. `bw comment <id> "text"` is positional. `bw close <id> --reason "text"` — `--reason` is a flag.

**Polling discipline** per `substrate/operating-disciplines.md` §7. On dispatch, post init handshake on `stoa--ewn` naming cron id + cadence. Heartbeat every ≤30 min.

PLINY in autonomous mode. PRINCIPAL + user-tier POLYBIUS are exception-handlers — project-direction calls, ship/no-ship, substance disagreement after one round, authorship/copyright/PRINCIPAL-final-say content, irreducible ambiguity, peer silence > 60 min, arc closes.

---

## Read first

Before any design or build work, read in order:

1. **`bw show stoa--ewn` ticket body in full + the 2026-05-17 C5 scope-addition comment.** Primary spec. Body has C1-C4 (with empirical anchors + fix shapes); the C5 comment adds the arc-build worktree convention candidate with Option A vs B framing. Treat as primary input prose alongside this directive.

2. **`substrate/MAJOR_POLYBIUS.md`** — current section structure. C1 extends §5.1.1. C2 adds activation-paste convention at §5.1.x (parallel to where Arc 30 §5.1.2 lives).

3. **`substrate/MAJOR_PLINY.md`** — current section structure, especially §5.9 (Arc 30 pre-branch hygiene). C3 (PLINY-signoff-accuracy) may live alongside §5.9 (same family); C5 (worktree convention) may extend §5.9.

4. **`substrate/operating-disciplines.md`** — current section structure, especially §19 (confabulation-under-uncertainty). C4 extends §19. C3 may live here as universal-team if DAEDALUS picks that locus.

5. **`substrate/templates/paste-instruction-template.md`** — current state. C2 adds `{{CRON_HYGIENE_CLAUSE}}` slot mirroring Arc 30's `{{PRE_BRANCH_HYGIENE_CLAUSE}}` pattern.

6. **Recent activation pastes (Arc 27-31 at the-stoa root)** — observe the ad-hoc cron-hygiene preamble that every paste has carried. C2 canonifies this so future pastes get it via template, not paste-author memory.

---

## Phase A — Architectural decisions (LOCKED pre-dispatch)

Settled during 2026-05-17 session + ticket evolution. You do NOT surface these as design questions.

### A1. One arc, four phases, one gauntlet — LOCKED

`stoa--ewn` is a coherent single work-unit. Single DAEDALUS design covering C1-C5. Single ARGUS audit (revisions likely given C5 Option pick + C3 locus pick). Single ADA worktree on `arc-32/build`. Verifiers (VERA + CATO + ZENO) each one pass. **CATO mandatory** — substrate canon; wording precision matters across multiple loci.

Phasing:

| Phase | Seat(s) | Output |
|---|---|---|
| 1 | DAEDALUS + ARGUS | `agents/design/arc-32/design.md` — integrated design covering C1 §5.1.1 extension; C2 cron-hygiene three-carrier encoding (template slot + §5.1.x convention + thin universal-team cross-ref); C3 PLINY-signoff-accuracy (DAEDALUS picks MAJOR_PLINY vs operating-disciplines locus); C4 attestation-confabulation §19 extension; C5 worktree convention (DAEDALUS picks Option A vs B per stoa--ewn C5 comment). ARGUS cold-audits; ADA does not dispatch until ARGUS PASS. |
| 2 | ADA | feature branch `arc-32/build` covering all substrate edits. |
| 3 | VERA + CATO + ZENO | parallel verification pass per Phase B acceptance probes. |
| 4 | PLINY + smoke + ship | smoke beats (per Phase C). PR opened. PLINY runs `gh pr merge` after clean PASS. `stoa--ewn` closes. **User-tier POLYBIUS does QA pass at arc-close per PRINCIPAL pattern.** |

### A2. C1 — §5.1.1 cross-project context leak extension — LOCKED scope; DAEDALUS scopes precision

Extend `substrate/MAJOR_POLYBIUS.md` §5.1.1 with explicit cross-project sequencing sub-discipline:

- **The discipline:** project-tier seats are SCOPED to their project; cross-project sequencing is user-tier-only concern; never leak it down — not even framed as "out of scope" or "separate follow-on," because those phrasings still seed awareness of the resource the §5.1.1 discipline is supposed to exclude.
- **Anti-pattern worked example** (from stoa--ewn body): the "Sector-4 corpus seed (separate follow-on...)" leak from today's ariadne-core pastes.
- **Positive worked example:** if a project-tier activation paste needs to mention an out-of-scope item, name the discipline that excludes it ("per §5.1.1, this paste scopes to <project> work only") rather than enumerating the out-of-scope item itself.

### A3. C2 — Cron-hygiene canon — LOCKED with three-carrier framing (mirror Arc 30)

Mirror Arc 30's three-carrier pattern for the pre-branch hygiene preamble:

- **Carrier 1 — substantive source-of-truth:** new section at `substrate/MAJOR_POLYBIUS.md` §5.1.x (DAEDALUS picks; likely §5.1.3 to follow §5.1.2 pre-branch hygiene paste convention). Encodes when + why cron hygiene check, what it does, surface-on-failure behavior.
- **Carrier 2 — paste convention:** also in `MAJOR_POLYBIUS.md` §5.1.x (or alongside the source-of-truth section). PLINY-targeted AND POLYBIUS-targeted activation pastes include the cron-hygiene preamble by default; can be suppressed only on explicit recognition that the activation will not plausibly need cron management.
- **Carrier 3 — template slot:** `substrate/templates/paste-instruction-template.md` gains `{{CRON_HYGIENE_CLAUSE}}` slot + canonical default expansion. Mirror Arc 30's `{{PRE_BRANCH_HYGIENE_CLAUSE}}` shape exactly (default-include with explicit suppress-on-recognition).
- **Plus thin universal-team cross-ref** at `operating-disciplines.md` (parallel to Arc 30's §24).

Canonical preamble text (DAEDALUS may refine):

```
Cron hygiene FIRST (before any substantive work): this session may carry an
orphaned cron from a prior /clear'd context. Run CronList; if any cron is
present, CronDelete it. Then [set up fresh OR proceed surface-and-wait per
role] as appropriate for the engagement.
```

### A4. C3 — PLINY-signoff-accuracy discipline — LOCKED scope; DAEDALUS picks locus

When PLINY (or any seat) claims cleanup actions in a signoff (branch deletion, worktree removal, file cleanup, etc.), the claim MUST be verified before the signoff is posted. Defense-in-depth: signoffs are forward-anchored to future POLYBIUSes; an inaccurate signoff propagates as false history.

**Empirical anchor:** Arc 29 PLINY signoff claimed "worktree removed, local + remote branches deleted" — neither was actually done. Caught by user-tier POLYBIUS on pre-branch hygiene check for Arc 31. Required destructive ops + cleanup before Arc 31 could dispatch.

**Locus pick (DAEDALUS chooses):**
- **Option α:** `substrate/MAJOR_PLINY.md` (alongside §5.9 pre-branch hygiene; same family — both are arc-close hygiene)
- **Option β:** `substrate/operating-disciplines.md` (universal-team — applies to any seat that posts signoffs)

DAEDALUS picks based on whether the discipline is PLINY-primary or genuinely universal. Lean Option α (PLINY does the vast majority of signoffs); cross-ref from operating-disciplines.md if Option α picked.

### A5. C4 — Attestation-confabulation extension — LOCKED scope

Extend `substrate/operating-disciplines.md` §19 (confabulation-under-uncertainty discipline) with an attestation sub-rule:

- **The discipline:** when attesting that a discipline check PASSED, the attestation MUST cite the live-verified state (the SHA / state observed at attestation time), NOT the assumed-from-context state (e.g., the dispatch-authoring SHA carried in the directive).
- **Discipline-PASS vs honesty-PASS are separate properties; both required.** A check that passes empirically but is attested-by-assumption violates honesty discipline even though it passes substantively.
- **Empirical anchor:** Arc 30 PLINY init-handshakes attested A11 pre-branch hygiene PASS by echoing the dispatch-authoring SHA (`140b398`) rather than re-verifying live at attestation time. Discipline PASS (both diff directions empty), but the attestation form was assumption not verification. PLINY's closure synthesis corrected to `140b398 → 316338c parent` honestly — but the original attestation was confabulated-from-context, not verified-from-state.

### A6. C5 — Arc-build worktree convention — LOCKED scope; DAEDALUS picks Option A vs B

**Option A — require separate worktree (RECOMMENDED).** Encode at `substrate/MAJOR_PLINY.md` §5.9 (extending pre-branch hygiene; same family): `git worktree add .claude/worktrees/arc-N-build arc-N/build` is the canonical pattern. Main worktree stays on main. User-tier POLYBIUS can operate in main concurrently without checkout collision.

**Option B — explicit allow main-worktree checkout.** Acknowledge both patterns; document tradeoffs; let PLINY pick per-arc.

DAEDALUS picks. User-tier POLYBIUS recommends Option A (cleaner separation; matches Arcs 26-30 de-facto pattern; eliminates the checkout-flip-side-effect that surfaced in Arc 31).

If Option A picked, also encode worktree-cleanup convention: at arc close, PLINY runs `git worktree remove .claude/worktrees/arc-N-build && git branch -D arc-N/build && git push origin --delete arc-N/build`. (Same shape as the PLINY-signoff-accuracy discipline in C3 — these reinforce each other.)

### A7. Cite-comment discipline — LOCKED

Cross-references between C1-C5 should resolve via cite. C2 + C5 may cross-ref each other (both are PLINY-facing); C3 + C4 may cross-ref (both are honesty-discipline); C1 stands alone. Pattern same as Arc 26 / 28 / 29 / 30 / 31 cite-comments at every read-site.

### A8. Authorship attribution — IMMUTABLE per substrate/CLAUDE.md

All edits credit Denson Smith. Arc 32 edits existing files (no new files with fresh author-like field exposure expected). Verify before commit.

### A9. Out of scope — HARD LOCKED

Do NOT do in this arc:

- **Bigger items in the backlog.** stoa--32b.2 (script/agent-inspection split), stoa--k36 (user-tier-to-main discipline), stoa--f37 (paste accumulation), stoa--ize (arcs/22 branch). All separate forthcoming arcs.
- **Migration of existing artifacts.** No backfill of historical pastes, no rewriting prior PR descriptions, etc. Forward-only convention adoption.
- **Empirical-premise-verification before LOCKING directives.** Surfaced as audit observation earlier this session; bigger discipline shape (touches directive-authoring); needs its own arc, not a fold-in here.
- **Sibling stoa--32b.0 (the parent epic itself).** Stays as epic-with-children container; this arc closes a child (stoa--ewn) but doesn't touch parent epic structure.

If you find yourself reaching for any of the above, STOP and surface as substance-disagreement comment on `stoa--ewn` (radio-check to user-tier POLYBIUS via [for: user-tier POLYBIUS] tag).

### A10. §15 N=1 honesty — LOCKED per-candidate

Each of C1-C5 has empirical anchors named in the ticket body (and §A2-A6 above). C1 + C3 + C4 + C5 are N=1 or N=2 today; C2 is "encoded ad-hoc many times" (multi-instance pattern). Substrate canon enters off-gate on PRINCIPAL-direction; future arcs accrete further evidence.

Each canon section must name its provenance — same shape as Arc 27 §16.6 / Arc 29 §17.1 / Arc 30 §5.9 / Arc 31 §25.6 N=1 framing. Do NOT over-generalize beyond what's named.

### A11. Pre-branch hygiene per Arc 30 §5.9 — SELF-APPLIED

Before creating `arc-32/build`, verify the two-check rule per Arc 30 canon. User-tier POLYBIUS confirmed at dispatch authoring: local main = origin/main at `e315ca9`; no other arc-build branches in flight. Should be clean at branch creation time.

---

## Phase B — Verify (probes for VERA)

1. **C1 §5.1.1 extension present** with cross-project sequencing sub-discipline + worked-example anti-pattern (sector-4 leak) + worked-example positive-pattern.
2. **C2 cron-hygiene three carriers present:**
   - Source-of-truth section in MAJOR_POLYBIUS.md
   - Paste convention section
   - `{{CRON_HYGIENE_CLAUSE}}` slot in paste-instruction-template.md with canonical default expansion
   - Thin universal-team cross-ref in operating-disciplines.md
3. **C3 PLINY-signoff-accuracy discipline present** at DAEDALUS's picked locus (Option α or β); verify-before-claim rule explicit.
4. **C4 §19 attestation sub-rule present** with live-verified-vs-assumed-from-context distinction + Arc 30 empirical anchor.
5. **C5 worktree convention present** at DAEDALUS's picked Option (A or B); if Option A picked, worktree-cleanup convention also documented.
6. **Cite-comments resolve** — cross-refs between C1-C5 + adjacent canon (Arc 30 §5.9 for C5; §19 for C4) all point at valid loci.
7. **PRINCIPAL provenance + §15 N=1 framing per A10** — each section names empirical anchor + provenance + accretion path.
8. **CURRENT regression:** check.sh against the-stoa workspace shows DRIFTED on edited substrate files (expected; consumer workspaces handle on their own activation per §14).

CATO cold-reads:
- diff for wording drift, scope creep, cite-comment correctness, cross-reference correctness, authorship attribution
- §15 N=1 honesty per A10 — no over-generalization in any of the 5 canon sections
- Tone consistency with Arcs 27-31 substrate-canon sections (PRINCIPAL block-quote style; subsection numbering; cross-ref style)

ZENO checks stoa--ewn C1-C5 each marked DONE by artifact reference.

---

## Phase C — Smoke + ship

PLINY's smoke beats before opening PR:

- `grep -n "cross-project sequencing\|cross-project context" substrate/MAJOR_POLYBIUS.md` — C1 present.
- `grep -n "{{CRON_HYGIENE_CLAUSE}}" substrate/templates/paste-instruction-template.md` — C2 slot present.
- `grep -n "cron hygiene\|orphaned cron" substrate/MAJOR_POLYBIUS.md substrate/operating-disciplines.md` — C2 carriers present.
- `grep -n "signoff\|verify before claim" substrate/MAJOR_PLINY.md substrate/operating-disciplines.md` — C3 at picked locus.
- `grep -n "attestation\|live-verified" substrate/operating-disciplines.md` — C4 in §19.
- `grep -n "worktree add\|.claude/worktrees/arc-" substrate/MAJOR_PLINY.md` — C5 present.
- check.sh against the-stoa — expected DRIFTED on substrate files this arc edits.

PR title: `Arc 32: canonification batch — C1 §5.1.1 extension + C2 cron-hygiene canon + C3 PLINY-signoff-accuracy + C4 attestation-confabulation + C5 worktree convention`
PR body: cross-ref `stoa--ewn`, prior Arc 30 (stoa--3cs; pre-branch hygiene three-carrier pattern C2 mirrors), prior Arc 31 (stoa--32b.1; confabulation discipline C4 extends + worktree convention C5 was surfaced by Arc 31 dispatch), this directive at `substrate/arcs/arc-32-build-directive.md`.

Merge via `gh pr merge` after clean gauntlet PASS. Close `stoa--ewn` with `--reason` referencing the merge commit. Tag `[for: user-tier POLYBIUS]` comment inviting QA pass.

---

## Honest scope reminder

Medium-scope substrate-canon arc. Comparable to Arc 29 / Arc 31 in spread (multi-file canon + template); each individual change small. 5 candidates means more surface area than single-discipline arcs; expect normal ARGUS revisions on C5 Option pick + C3 locus pick. DAEDALUS round + likely 1 ARGUS revise; ADA + verifiers; smoke + ship. ~1-2h CAPTAIN-agent wall-clock estimated.

End directive.
