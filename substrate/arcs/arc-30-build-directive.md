# Arc 30 build directive — PLINY pre-branch hygiene discipline encoded as substrate canon

**Audience:** the fresh Claude Code session opened to build Arc 30 deliverables (MAJOR_PLINY at the-stoa tier).
**Authored by:** user-tier MAJOR_POLYBIUS + the PRINCIPAL (Denson Smith).
**Status:** active directive. **Arc 29 (`stoa--ads`) is CLOSED**; precondition satisfied.
**Bw ticket:** `stoa--3cs` (the work-unit; bumped P3 → P1 today on N=2 + N=1 evidence).
**Builds on:** Arcs 1-29 (the-stoa main as of `140b398`).

**Your one job:** encode the **PLINY pre-branch hygiene discipline** as substrate canon — a two-check rule PLINY runs before creating any arc-build branch, so the bundled-squash pattern observed today twice never recurs. PRINCIPAL articulated the rule on 2026-05-17: "pliny can't create more than one branch to work with until the other is committed and merged" + sync local main with origin before branching.

The discipline provably works when applied — Arc 29 (today) shipped clean because the pre-branch check was baked into the activation paste. Two prior arcs today (PR #46 multi-project routine + PR #8 Arc 28) shipped with the bundled-squash symptom because the check wasn't applied. Encoding the discipline in substrate canon means every future arc gets it without paste-reminders.

One ticket, one coherent push:
- **stoa--3cs** (P1) — pre-branch hygiene discipline encoded in substrate canon. The ticket body + scope-expansion comment carry the full architectural intent.

This is a focused, small-scope substrate arc. Larger than typical doc-only edits because the discipline interacts with several existing patterns (activation pastes, MAJOR_PLINY.md branching guidance, possibly operating-disciplines.md cross-ref). Single DAEDALUS round expected.

---

## Comms — autonomous mode via bw, radio-check protocol

Same shape as Arcs 25-29. PROJECT-TIER POLYBIUS (separate Claude Code session, activated from `HUMAN_paste-polybius-arc-30-instruction.md`) is your radio-check peer; you communicate via comments on `stoa--3cs`. USER-TIER POLYBIUS dispatched this arc + will do QA pass at arc close per PRINCIPAL's pattern.

PRINCIPAL is **not** the relay for routine status — beadwork is.

**bw command syntax** is in `substrate/MAJOR_PLINY.md` §6.1. `bw comment <id> "text"` is positional. `bw close <id> --reason "text"` — `--reason` is a flag.

**Polling discipline** per `substrate/operating-disciplines.md` §7. On dispatch, post init handshake on `stoa--3cs` naming cron id + cadence. Heartbeat every ≤30 min.

PLINY in autonomous mode. PRINCIPAL + user-tier POLYBIUS are exception-handlers — project-direction calls, ship/no-ship, substance disagreement after one round, authorship/copyright/PRINCIPAL-final-say content, irreducible ambiguity, peer silence > 60 min, arc closes.

---

## Read first

Before any design or build work, read in order:

1. **`bw show stoa--3cs` ticket body in full + the 2026-05-17 scope-expansion comment.** Primary spec. Body has the original surfacing from Arc 27 + the proposed discipline shape. The expansion comment carries PRINCIPAL's 2026-05-17 articulation of the two-check rule + N=2 bit-by-it evidence + N=1 worked-when-applied evidence + where the discipline lives in substrate canon. Treat as primary input prose alongside this directive.

2. **`substrate/MAJOR_PLINY.md`** — full read; identify the section(s) where arc-build branching guidance currently lives (likely in an arc-workflow or branching-discipline section). D1 extends or sits beside that section.

3. **`substrate/operating-disciplines.md`** — current section structure. D3 may add a cross-ref OR a universal-team section depending on DAEDALUS's read of whether non-PLINY seats ever create branches.

4. **`substrate/templates/paste-instruction-template.md`** — current paste template. D2 may want to encode the pre-branch hygiene step as a STANDARD PREAMBLE that PLINY-targeted pastes include alongside the cron-hygiene step. DAEDALUS picks the encoding shape.

5. **The Arc 27 / 28 / 29 activation pastes** at the-stoa root (`HUMAN_paste-pliny-arc-27/28/29-instruction.md`) — these are the de-facto-template carrying the cron-hygiene preamble. Arc 29's paste also carried the pre-branch hygiene preamble. Reading them shows the natural shape.

---

## Phase A — Architectural decisions (LOCKED pre-dispatch)

Settled during PRINCIPAL's 2026-05-17 chat declarations + ticket evolution. You do NOT surface these as design questions.

### A1. One arc, four phases, one gauntlet — LOCKED

`stoa--3cs` is a coherent single work-unit. Single DAEDALUS design. Single ARGUS audit. Single ADA worktree on `arc-30/build`. Verifiers (VERA + CATO + ZENO) each one pass. **CATO mandatory** — substrate canon; wording precision matters for life-of-substrate.

Phasing:

| Phase | Seat(s) | Output |
|---|---|---|
| 1 | DAEDALUS + ARGUS | `agents/design/arc-30/design.md` — integrated design covering: D1 MAJOR_PLINY.md new discipline section; D2 activation paste preamble shape (encode as standard? standalone section?); D3 operating-disciplines.md cross-ref or universal section; D4 existing activation paste templates / examples updates if any. ARGUS cold-audits. |
| 2 | ADA | feature branch `arc-30/build` covering all substrate edits. |
| 3 | VERA + CATO + ZENO | parallel verification pass per Phase B acceptance probes. |
| 4 | PLINY + smoke + ship | smoke beats (per Phase C). PR opened. PLINY runs `gh pr merge` after clean PASS. `stoa--3cs` closes. **User-tier POLYBIUS does QA pass at arc-close per PRINCIPAL pattern.** |

### A2. The two-check pre-branch rule — LOCKED (PRINCIPAL-articulated 2026-05-17)

Before PLINY creates a new arc-build branch (e.g., `arc-N/build`), TWO checks:

1. **No other arc-build branch hanging around.** The prior arc's branch must be merged AND deleted before a new one is created. (Per PRINCIPAL: "at most one team working on a repo at any one time"; PLINY may have at most ONE arc-build branch in flight.)
2. **Local main = origin/main.** No unpushed commits.
   ```
   git fetch origin main
   git log --oneline main..origin/main      # must be empty
   git log --oneline origin/main..main      # must be empty
   ```

If either check fails: PLINY pauses + surfaces (via `[for: user-tier POLYBIUS]` tagged comment on the work-unit ticket, OR via `[for: PRINCIPAL]` if user-tier unavailable) with the specific state + asks for adjudication ("push the unpushed commits first? discard them? wait?"). Does NOT silently proceed.

PRINCIPAL phrasing to carry verbatim in the canon section (per Arc 29 §17.1 / Arc 27 §16.1 pattern): block-quote PRINCIPAL's 2026-05-17 articulation. DAEDALUS picks the precise quote; both the "one team per repo at a time" line and "pliny can't create more than one branch to work with until the other is committed and merged" are load-bearing.

### A3. Where the canon lives — LOCKED scope; DAEDALUS scopes locus

**D1 — MAJOR_PLINY.md new discipline section.** DAEDALUS picks insertion locus (likely near existing arc-workflow / branching guidance section, or as new section in the arc-build family). Encodes:
- The two-check rule + the surface-on-failure behavior
- Why (the bundled-squash empirical anchor + the discipline's proven-when-applied evidence)
- §15 N=1 provenance + accretion path

**D2 — activation paste convention.** The Arc 27-29 pastes encoded preambles (cron-hygiene + pre-branch hygiene) ad-hoc. This arc canonifies the pre-branch preamble specifically. DAEDALUS picks the encoding shape:
- **Option α:** Add a new section to MAJOR_POLYBIUS.md (§5 onboarding-flow area, near paste-instruction template) that says "PLINY-targeted activation pastes MUST include the pre-branch hygiene preamble" + reference template.
- **Option β:** Add to `substrate/templates/paste-instruction-template.md` as a mandatory section the template includes.
- **Option γ:** Both (more redundant; clearer).

The cron-hygiene preamble is OUT of scope here (separate forthcoming canonification arc — item 3 of PRINCIPAL's audit list); just encode the pre-branch hygiene preamble in whatever Option DAEDALUS picks.

**D3 — operating-disciplines.md** — DAEDALUS picks whether to add cross-ref OR universal-team section. PLINY is the primary seat that creates branches; other seats RARELY do. If non-PLINY seats ever create branches (e.g., a CAPTAIN doing a hotfix), the discipline applies to them too. Cross-ref minimum; universal section if DAEDALUS judges the wider framing earns its keep.

### A4. Cite-comments — LOCKED

Same pattern as Arc 26's `parse_skill_names_from_install` + Arc 28's bw-output-parse + Arc 29's base-vs-custom scoping cite-comments. Wherever the new discipline-text references existing patterns (e.g., the cron-hygiene preamble next to it, the bw command syntax in §6.1), use cite-cross-references that resolve.

### A5. Authorship attribution — IMMUTABLE per substrate/CLAUDE.md

All edits credit Denson Smith. Arc 30 edits existing role-file + possibly template (no fresh author-like field exposure expected). Verify before commit.

### A6. Out of scope — HARD LOCKED

Do NOT do in this arc:

- **Tooling / pre-branch hook enforcement.** Discipline-first; tooling-second. We don't yet need a mechanical pre-branch git hook — the activation-paste preamble + role-file discipline is sufficient empirically (Arc 29 proved it works).
- **Restructuring of existing PR squashes.** PR #46 + PR #8 shipped with bundled-squash; the bundled content is legit; no unwind.
- **Cron-hygiene canonification.** Separate arc; do not bundle.
- **§5.1.1 cross-project context leak extension.** Separate arc.
- **stoa--32b.1 (PRINCIPAL-gate) and stoa--32b.2 (mechanical-script/agent-split).** Separate arcs.
- **Sibling arc-build branch coordination protocols** (e.g., what if user-tier POLYBIUS needs PLINY to wait while the prior branch is reviewed?). The discipline says "merge + delete prior branch first"; details of how PRINCIPAL/user-tier signal that to PLINY are operator-discretion not substrate-canon.

If you find yourself reaching for any of the above, STOP and surface as substance-disagreement comment on `stoa--3cs` (radio-check to user-tier POLYBIUS via [for: user-tier POLYBIUS] tag).

### A7. §15 N=1 honesty — LOCKED

PRINCIPAL declared the discipline (project-direction authority); substrate canon enters off-gate. N=2 bit-by-it + N=1 worked-when-applied empirical evidence already supports the discipline shape. Future arcs that ship clean (or that surface the check correctly) accrete further evidence. The new canon section must name PRINCIPAL-declaration provenance + the empirical anchor cites + the accretion path against §6.7.1 gate — same shape as Arc 27 §16.6 / Arc 29 §17.1.

### A8. Pre-branch hygiene — SELF-APPLIED (this arc)

**Before creating `arc-30/build`:** verify local main = origin/main per the rule you're about to encode (recursive). User-tier POLYBIUS confirmed at dispatch authoring: local main = origin/main at `140b398`. Should be clean at branch creation time. If somehow ahead, pause + surface (don't silently inherit local-ahead commits — that's the exact pattern this arc encodes against).

Verify per the A2 check:
```
git fetch origin main
git log --oneline main..origin/main      # must be empty
git log --oneline origin/main..main      # must be empty
```

---

## Phase B — Verify (probes for VERA)

1. **Canon section present in MAJOR_PLINY.md** with PRINCIPAL block-quote verbatim + two-check rule explicit + surface-on-failure behavior named.
2. **Activation paste convention encoded per D2 Option pick** (α / β / γ) — DAEDALUS's choice documented + implementation visible.
3. **operating-disciplines.md cross-ref or universal section present per D3.**
4. **§15 N=1 provenance** named (PRINCIPAL-declaration + 2026-05-17 anchor + N=2 + N=1 evidence cites + accretion path).
5. **Cite-comments resolve** — any cross-references to MAJOR_PLINY §6.1, MAJOR_POLYBIUS §5, etc. point at valid sections.
6. **No tooling/hook added** (out of scope per A6) — verify diff is doc-only / canon-only.
7. **Existing arc activation pastes (Arc 27/28/29) not edited** — forward-only; existing pastes stay as the empirical-record.

CATO cold-reads:
- diff for wording drift, scope creep, cite-comment correctness, cross-reference correctness, authorship attribution
- PRINCIPAL's exact phrasing per A2 — block-quote verbatim
- §15 N=1 honesty per A7 — no over-generalization
- Tone consistency with neighboring substrate-canon sections (Arc 27 §16 / Arc 29 §17 / Arc 28 §16 of MAJOR_POLYBIUS.md or wherever DAEDALUS picks)

ZENO checks stoa--3cs deliverables D1-D4 each marked DONE by artifact reference.

---

## Phase C — Smoke + ship

PLINY's smoke beats before opening PR:

- `grep -n "pre-branch\|pre-branch hygiene\|two-check" substrate/MAJOR_PLINY.md` — new section present
- `grep -n "pre-branch\|two-check" substrate/operating-disciplines.md` — cross-ref or universal section present
- `grep -n "git log --oneline main..origin/main\|git log --oneline origin/main..main" substrate/MAJOR_PLINY.md` — explicit check commands present
- `grep -n "pliny can't create more than one branch\|one team per repo\|at most one team" substrate/MAJOR_PLINY.md` — PRINCIPAL block-quote present
- Wherever D2's encoding lives (template file, MAJOR_POLYBIUS.md section, etc.) — verify discoverable via grep
- check.sh against the-stoa workspace — expected DRIFTED on substrate files this arc edits

PR title: `Arc 30: PLINY pre-branch hygiene discipline encoded as substrate canon (closes the bundled-squash gap)`
PR body: cross-ref `stoa--3cs`, prior arcs that exhibited the bundled-squash symptom (PR #46 + PR #8) AND Arc 29 (PR #9) that proved the discipline works when applied, this directive at `substrate/arcs/arc-30-build-directive.md`.

Merge via `gh pr merge` after clean gauntlet PASS. Close `stoa--3cs` with `--reason` referencing the merge commit. Tag `[for: user-tier POLYBIUS]` comment inviting QA pass.

---

## Honest scope reminder

Small substrate-canon arc. Smaller than Arc 28 / Arc 29. Single DAEDALUS round expected; ARGUS revisions possible if section placement / Option α-β-γ pick has tradeoffs DAEDALUS surfaces. PLINY heads-down should run in under an hour wall-clock.

End directive.
