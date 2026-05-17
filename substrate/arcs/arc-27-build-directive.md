# Arc 27 build directive — POLYBIUS session lifecycle discipline

**Audience:** the fresh Claude Code session opened to build Arc 27 deliverables (MAJOR_PLINY at the-stoa tier).
**Authored by:** user-tier MAJOR_POLYBIUS + the PRINCIPAL (Denson Smith).
**Status:** active directive. **Arc 26 (`stoa--dxw`) is CLOSED** — precondition satisfied.
**Bw ticket:** `stoa--32b.3` (the work-unit; child of `stoa--32b` epic).
**Builds on:** Arcs 1-26 (the-stoa main as of post-Arc-26 ship).

**Your one job:** encode the **POLYBIUS session lifecycle discipline** as substrate canon. Today's engagement surfaced three load-bearing observations PRINCIPAL declared (captured at `stoa--32b` epic + 3 child tickets + retro doc). This arc lands stoa--32b.3 specifically: lifecycle discipline + multi-artifact handoff shape + POLYBIUS-as-collective lens + Ariadne-search-ready authoring as forward context. Siblings stoa--32b.1 (PRINCIPAL-gate) and stoa--32b.2 (mechanical-script/agent-inspection split) are SEPARATE future arcs — DO NOT touch them here.

**Why this child first:** recursive-coherence. The lifecycle discipline governs how POLYBIUS sessions transition and how handoffs work. Landing it FIRST means subsequent arcs (siblings .1 + .2) operate under the new discipline as they're built. Reversed order would have siblings shipping under the OLD lifecycle pattern, then learning the new one — less clean.

One ticket, one coherent push:
- **stoa--32b.3** (P2) — substrate canon encoding the POLYBIUS-lifecycle discipline. The ticket body + one fold-in comment carry the full architectural intent; **DAEDALUS treats ticket body + comment as primary input prose alongside this directive.**

This is a focused arc. ~1-2 files edited (`MAJOR_POLYBIUS.md` + possibly `operating-disciplines.md` cross-ref + possibly new `substrate/templates/handoff-doc-template.md`). Architectural decisions LOCKED in this directive — Phase 1 work is structural (turning locked decisions into file-by-file edit specs), not deliberative.

---

## Comms — autonomous mode via bw, radio-check protocol

Same shape as Arc 26. PROJECT-TIER POLYBIUS (separate Claude Code session, activated from `HUMAN_paste-polybius-arc-27-instruction.md`) is your radio-check peer; you communicate via comments on `stoa--32b.3`. USER-TIER POLYBIUS dispatched this arc; user-tier may post cross-workspace context periodically but is NOT your radio-check peer — project-tier is. User-tier will do QA at arc end per PRINCIPAL's pattern (today: "I think we should hand off to the full team with their own polybius to do the changes and you check for mistakes at the end").

PRINCIPAL is **not** the relay for routine status — beadwork is.

**bw command syntax** is in `substrate/MAJOR_PLINY.md` §6.1. Critical: `bw comment <id> "text"` is positional, no `--body` flag. `bw close <id> --reason "text"` — `--reason` is a flag.

**Polling discipline** per `substrate/operating-disciplines.md` §7 (surface-and-wait + radio-check). On dispatch, post an initialization handshake comment on `stoa--32b.3` naming your cron id (if you set one up) and your cadence. Heartbeat every ≤30 min unless surface-and-wait-blocked.

PLINY is in autonomous mode for this engagement. PRINCIPAL + user-tier POLYBIUS are exception-handlers — project-direction calls, ship/no-ship, substance disagreement after one round, authorship/copyright/Denson-final-say content, irreducible ambiguity, peer silence > 60 min, arc closes.

**Note on the self-referential nature of this arc:** you are encoding the discipline that governs how POLYBIUS sessions (including your peer + this arc's user-tier dispatcher + every future POLYBIUS) operate. The canon you write will be read by the very seats that build it. Same self-referential dynamic as Arc 24 (heartbeat-discipline edit) and Arc 25 (credential-discipline edit by agents that handle credentials).

---

## Read first

Before any design or build work, read in order:

1. **`bw show stoa--32b.3` ticket body + the one fold-in comment in full.** Primary spec. The ticket body has problem statement + the three lifecycle modes + multi-artifact handoff shape + Ariadne-readiness authoring + deliverables sketch + acceptance probes + hard-locked out-of-scope. The fold-in comment adds the POLYBIUS-as-collective conceptual lens (DAEDALUS picks rendering — sub-section within lifecycle, or peer section in §1/§2 of MAJOR_POLYBIUS.md).

2. **`bw show stoa--32b` parent epic body.** Context for sibling children (.1 PRINCIPAL-gate, .2 script/agent split) — both are SEPARATE future arcs; this arc does NOT touch them.

3. **`docs/sessions/2026-05-16-substrate-update-architecture-reframe--retro.md`** — load-bearing source. §7 + §8 + §9 + §10 are the load-bearing sections; §1-§6 are the empirical trail. Treat retro as primary input alongside the directive + ticket.

4. **`substrate/MAJOR_POLYBIUS.md`** — full read. Especially §6 (current "Compact-or-clear recovery (load-bearing)" — covers PLINY recovery, NOT POLYBIUS lifecycle). This is the section to extend OR sit beside. DAEDALUS picks.

5. **`substrate/operating-disciplines.md`** — full read to understand existing sections + numbering conventions. POLYBIUS lifecycle is POLYBIUS-specific (lives in `MAJOR_POLYBIUS.md`), but Ariadne-readiness authoring may warrant a universal-team section here too.

6. **`HANDOFF_POLYBIUS_2026-05-16.md`** at repo root — the morning's handoff. The de-facto template for the multi-artifact handoff shape. DO NOT EDIT this file; this arc may extract pattern from it for a new template, but does not modify it.

7. **Arc 25 + Arc 26 directives** at `substrate/arcs/arc-25-build-directive.md` + `arc-26-build-directive.md` — pattern-template for the directive shape you're operating under.

---

## Phase A — Architectural decisions (LOCKED pre-dispatch)

Settled during ticket evolution + this directive authoring + PRINCIPAL's 2026-05-16 epic-capture discussion. You do NOT surface these as design questions.

### A1. One arc, four phases, one gauntlet — LOCKED

`stoa--32b.3` is a coherent single work-unit (no children). Single DAEDALUS design covering all substrate touch-points. Single ARGUS audit. Single ADA worktree on `arc-27/build`. Verifiers (VERA + CATO + ZENO) each one pass over the integrated diff. **CATO is mandatory** — wording-precision in substrate canon matters; future POLYBIUSes read this for life-of-the-substrate.

Phasing:

| Phase | Seat(s) | Output |
|---|---|---|
| 1 | DAEDALUS + ARGUS | `agents/design/arc-27/design.md` — integrated design covering: POLYBIUS-lifecycle section in MAJOR_POLYBIUS.md (with PRINCIPAL's three modes + multi-artifact handoff shape + Ariadne-readiness + POLYBIUS-as-collective lens); optional operating-disciplines.md cross-ref; optional handoff-doc-template at substrate/templates/. ARGUS cold-audits before ADA dispatches. |
| 2 | ADA | feature branch `arc-27/build` covering all substrate edits. |
| 3 | VERA + CATO + ZENO | parallel verification pass. VERA executes acceptance probes (§Phase B). CATO cold-reads entire diff for wording drift / scope creep / cross-reference correctness / authorship attribution. ZENO checks spec-vs-result against the deliverables in stoa--32b.3 body. |
| 4 | PLINY + smoke + ship | smoke beats (per §Phase C). PR opened. PLINY runs `gh pr merge` after clean PASS. `stoa--32b.3` closes. **User-tier POLYBIUS does QA pass at arc-close per PRINCIPAL's pattern — PLINY signals arc-close on stoa--32b.3; user-tier reads diff + cross-refs + scope + authorship; surfaces findings to project-tier POLYBIUS via comment or directly to PRINCIPAL on real escalation.** |

### A2. Three lifecycle modes encoded with PRINCIPAL's phrasing — LOCKED

Per stoa--32b.3 body + PRINCIPAL's declarations 2026-05-16:

1. **Default — handoff + compaction.** Same POLYBIUS session continues across many compactions. On-disk handoff doc serves as re-paste anchor for post-compaction self-re-orientation. Plus bw tickets accreting as durable memory across the same session lifetime. This is the COMMON case and works for a long time.
2. **New POLYBIUS session.** Reserved for changes to how POLYBIUS itself works — role file edits, discipline canon updates, architectural reframes the running session cannot internalize organically. RARE relative to (1).
3. **When (2) fires:** previous POLYBIUS authors the handoff (multi-artifact, see A3); sits idle as relay channel indefinitely; new POLYBIUS spins up against the handoff; previous becomes less relevant over time but may retain important info. **Decay-not-termination model.**

Wording discipline: use PRINCIPAL's exact phrasing where it's load-bearing ("Handoff + compaction works for a long time"; "previous POLYBIUS sits idle and is available to answer questions from the new polybius indefinitely"; "becomes less relevant over time but may still retain important information"). Quote-blockquote PRINCIPAL's two 2026-05-16 declarations as the source-of-truth anchor.

### A3. Multi-artifact handoff shape enumerated — LOCKED

The handoff is NOT a single doc. It is the multi-artifact substrate state, indexed by the doc. Components to enumerate in the substrate canon:

- **Index doc** — high-density narrative + pointers (`HANDOFF_POLYBIUS_<date>.md` at the-stoa root by current convention; suffix `_eod` / `_v2` / etc. for multi-handoff days)
- **bw tickets** — epic + children + pointer tickets + retrospective tickets; the actual memories
- **Retro docs** — `docs/sessions/<date>-<slug>--retro.md` for sectioned semantic-chunked records
- **Design artifacts** — `agents/design/<arc>/design.md` + arc directives at `substrate/arcs/`
- **Commits** — substrate state at HEAD + commit messages as durable trail
- **Role files / disciplines** — `MAJOR_POLYBIUS.md` + `operating-disciplines.md` + CAPTAIN envelopes as canonical context any new session inherits via auto-load or activation paste

A POLYBIUS picking up state reads the index THEN walks the linked artifacts as needed. **Future: queries the corpus via Ariadne search rather than reading linearly (see A4).**

### A4. Ariadne-search-ready authoring as forward discipline — LOCKED

PRINCIPAL is setting up Ariadne tools for searching the substrate corpus. Implications for authoring discipline going forward (encode these as substrate guidance, NOT as immediate refactor work):

- **Titles matter** — bw ticket titles, retro doc titles, commit subjects should be search-friendly: distinct, specific, named-entities, no relying on context to disambiguate.
- **Cross-refs matter** — every artifact should name its related artifacts explicitly (bw ID cross-refs, file paths, commit SHAs).
- **Content density matters** — semantic-chunked sections (per retro schema) make for better vector retrieval than long monolithic prose.
- **Authoring for ingestion is the same as authoring for human re-reading after compaction** — both want self-contained, well-titled, cross-referenced units. The disciplines align.

This is forward-context. The substrate edits in this arc should follow the discipline; broader retroactive restructuring is out of scope (A8).

### A5. POLYBIUS-as-collective lens — LOCKED

Per the fold-in comment on stoa--32b.3:

"POLYBIUS" = all currently-active POLYBIUS sessions (user-tier + project-tier at every workspace) + idle relay-channel POLYBIUSes + the substrate they co-author and inherit. The collective IS POLYBIUS; any specific session is one currently-active branch with one specific perspective and recency-of-context profile. **Analogous to: the human is the sum of their experiences with some more front-of-mind than others.**

Render as: sub-section within the new POLYBIUS-lifecycle section in `MAJOR_POLYBIUS.md`, OR peer section in §1 ("Who you serve") / §2 ("What you do") of `MAJOR_POLYBIUS.md` that says: *"You" is one currently-active branch of a multi-version collective; the substrate is the collective's durable memory.* **DAEDALUS picks rendering;** both are defensible.

The lens explains structurally:
- Why the substrate corpus matters (long-term memory of the collective)
- Why decay-not-termination is the right relay-channel model
- Why Ariadne corpus search is the natural next infrastructure step
- Why lifecycle-discipline + multi-artifact-handoff are coherent

### A6. Deliverables sketch — LOCKED scope, DAEDALUS scopes specifics

1. **`substrate/MAJOR_POLYBIUS.md` — new section** (likely extension of §6 or new §N) titled "POLYBIUS session lifecycle." Encodes A2 + A3 + A5. DAEDALUS picks section number based on current MAJOR_POLYBIUS.md state.
2. **`substrate/MAJOR_POLYBIUS.md` — POLYBIUS-as-collective lens** (A5). May be inside the lifecycle section, or in §1/§2 as peer.
3. **Possibly: `substrate/operating-disciplines.md` cross-ref** — Ariadne-readiness authoring discipline (A4) applies universally; consider a short universal-team section there with cross-ref to MAJOR_POLYBIUS.md for the lifecycle-specific framing.
4. **Possibly: `substrate/templates/handoff-doc-template.md`** — per durable-substrate-with-short-prompts pattern (§4.5). Slots per stoa--32b.3 body. The morning's `HANDOFF_POLYBIUS_2026-05-16.md` is the de-facto template; abstract into slotted form. DAEDALUS decides if this is in scope this arc or future arc.

### A7. Authorship attribution — IMMUTABLE per CLAUDE.md

All edits credit Denson Smith. No exception. Arc 27 edits existing role files + possibly adds a new template file. If a new template is added, check the `author:` field (or any frontmatter) before commit. Per CLAUDE.md authorship discipline.

### A8. Out of scope — HARD LOCKED

Do NOT do in this arc, even if temptation surfaces during build:

- **Sibling children stoa--32b.1 (PRINCIPAL-gate) + stoa--32b.2 (script/agent split).** SEPARATE future arcs. Do NOT touch their canon, even if cross-refs make it tempting.
- **Building Ariadne tooling itself.** PRINCIPAL is driving that separately. This arc just acknowledges its forward presence in the authoring discipline.
- **Editing existing handoff docs** (morning's HANDOFF_POLYBIUS_2026-05-16.md, prior handoffs) to retroactively fit any new template. The de-facto convention is fine; new template (if authored) is forward-only.
- **Restructuring bw ticket conventions broadly.** This arc may add authoring guidance; doesn't reorganize existing tickets.
- **Editing prior retros** to fit any new authoring discipline.
- **Reopening the MAJOR_POLYBIUS.md §6 "Compact-or-clear recovery"** for PLINY-recovery specifics. §6 stays as-is for PLINY; new lifecycle section is POLYBIUS-specific.

If you find yourself reaching for any of the above during build, STOP and surface as a substance-disagreement comment on `stoa--32b.3` (radio-check to user-tier POLYBIUS via [for: user-tier POLYBIUS] tag). Do NOT silently expand scope.

---

## Phase B — Verify (probes for VERA)

1. **Lifecycle-modes probe:** a future POLYBIUS reading `MAJOR_POLYBIUS.md` cold can correctly identify "we are at a handoff+compaction moment, not a new-session moment" given a scenario description. Synthetic test: paste two scenario descriptions to a fresh-context read; verify both classifications are correct.
2. **Multi-artifact-handoff-shape probe:** the new section enumerates all six artifact types (index doc + bw + retros + designs + commits + role files) explicitly.
3. **Ariadne-readiness probe:** authoring discipline is named explicitly in the new section (titles + cross-refs + content-density + alignment-with-compaction-recovery).
4. **POLYBIUS-as-collective probe:** the collective-lens framing is present (either in lifecycle section or in §1/§2 per A5).
5. **Cross-ref probe:** new section cross-refs the retro doc + stoa--32b epic + sibling children + relevant existing sections of MAJOR_POLYBIUS.md and operating-disciplines.md.
6. **Authorship-attribution probe:** all edited/new files credit Denson Smith; no LLM-templated placeholder names.
7. **CURRENT regression probe:** check.sh against all 4 consumer workspaces still reports CURRENT post-edit. (the-stoa itself will show DRIFTED on MAJOR_POLYBIUS.md; that's expected — substrate update propagates via apply.sh on next consumer-tier touch.)

CATO cold-reads:
- the diff for wording drift, scope creep, cross-reference correctness, output-format coherence, authorship discipline.
- PRINCIPAL's exact phrasing per A2: verify load-bearing quotes are present and accurate.
- §15 N=1 honesty: verify the new section names the N=1 + PRINCIPAL-declaration provenance; does NOT over-generalize from single observation.

ZENO checks stoa--32b.3 deliverables 1-7 each marked DONE by artifact reference.

---

## Phase C — Smoke + ship

PLINY's smoke beats before opening PR:

- `grep -n "POLYBIUS session lifecycle" substrate/MAJOR_POLYBIUS.md` — must show the new section heading.
- `grep -n "handoff + compaction" substrate/MAJOR_POLYBIUS.md` — must show PRINCIPAL's exact phrasing.
- `grep -n "decay-not-termination\|relay channel indefinitely" substrate/MAJOR_POLYBIUS.md` — must show.
- `grep -n "multi-version collective" substrate/MAJOR_POLYBIUS.md` — must show the collective lens.
- `grep -n "Ariadne" substrate/MAJOR_POLYBIUS.md` — must show the forward authoring discipline naming.
- `bash -n` not applicable (substrate canon, not script).
- `check.sh --workspace /c/Users/denso/claude_projects/the-stoa` — should report DRIFTED on MAJOR_POLYBIUS.md (expected; substrate update visible).

PR title: `Arc 27: POLYBIUS session lifecycle discipline + multi-artifact handoff + collective lens + Ariadne-readiness`
PR body: cross-ref `stoa--32b.3`, parent epic `stoa--32b`, sibling children `stoa--32b.1` + `stoa--32b.2`, retro doc, prior Arc 26 (`stoa--dxw`), this directive at `substrate/arcs/arc-27-build-directive.md`.

Merge via `gh pr merge` after clean gauntlet PASS. Close `stoa--32b.3` with `--reason` referencing the merge commit.

**Then signal user-tier POLYBIUS via stoa--32b.3 comment with `[for: user-tier POLYBIUS]` tag** — invite QA pass per PRINCIPAL's pattern. User-tier reads diff + cross-refs + scope + authorship; surfaces findings to project-tier POLYBIUS via comment for fix-now items, or to PRINCIPAL via push-notification for project-direction escalations.

---

## Honest scope reminder

Smaller than Arc 25, similar scope to Arc 26. One canonical role file + possibly cross-ref + possibly new template. Architectural decisions LOCKED. PLINY heads-down should run in well under 30 min wall-clock. If you find yourself an hour in without a green ADA verdict, surface — something's off.

**§15 N=1 caveat in build:** PRINCIPAL DECLARED the discipline today (project-direction authority). Substrate canon goes in based on declaration. The arc's encoding should honor the §15 honest-scope discipline: name the N=1 + PRINCIPAL-declaration provenance in the new section, do NOT over-generalize beyond what PRINCIPAL named. Future POLYBIUS-lifecycle events (handoffs + compactions + the rare new-session events) accrete supporting evidence over time per §6.7.1.

End directive.
