# Arc 31 build directive — PRINCIPAL-gate discipline encoded as substrate canon

**Audience:** the fresh Claude Code session opened to build Arc 31 deliverables (MAJOR_PLINY at the-stoa tier).
**Authored by:** user-tier MAJOR_POLYBIUS + the PRINCIPAL (Denson Smith).
**Status:** active directive. **Arc 30 (`stoa--3cs`) is CLOSED**; precondition satisfied.
**Bw ticket:** `stoa--32b.1` (the work-unit; child of `stoa--32b` epic).
**Builds on:** Arcs 1-30 (the-stoa main as of `efb0394`).

**Your one job:** encode the **PRINCIPAL-gate discipline** as substrate canon. PRINCIPAL declared on 2026-05-16: a design clause that names PRINCIPAL as the deciding seat is a BLOCK, not a TAG. Autonomous mode does not get to skip past it. PRINCIPAL-AFK on a PRINCIPAL-gated decision means the workflow waits. The substrate currently conflates "autonomous-mode escalation cadence" (when to surface during routine work) with "PRINCIPAL-gate" (whether PRINCIPAL input is structurally required). This arc separates them and encodes the gate-as-block behavior at every relevant locus.

**Empirical anchor:** Arc 26's VERA Probe 8 (per stoa--dxw + retro §7) — design clause "PRINCIPAL-discretion per design §6" was treated by the entire quality chain (DAEDALUS → ARGUS → ADA → VERA → CATO → ZENO → PLINY → project-tier POLYBIUS) as a post-hoc-disposition marker; probe mutated sector-4 without operator authorization; stoa--501 was the post-hoc cleanup. Until this discipline lands, every future arc with a PRINCIPAL-gated clause is exposed to the same failure mode — and the workaround (manually reminding every activation paste to "treat PRINCIPAL-discretion the NEW way") is brittle.

One ticket, one coherent push:
- **stoa--32b.1** (P2 → effectively P1 for this dispatch) — PRINCIPAL-gate discipline. Body has 5 deliverables (with D5 being the probe-design sub-case DAEDALUS picks to fold vs split).

This is a substantive multi-file substrate-canon arc — comparable to Arc 25 (credential discipline) and Arc 27 (POLYBIUS lifecycle) in scope. Substrate canon edits at operating-disciplines.md + several CAPTAIN envelopes (DAEDALUS, ADA, VERA) + two templates (autonomous-mode-activation + polling-cron-prompt). Expected ARGUS revisions given the architectural sensitivity.

---

## Comms — autonomous mode via bw, radio-check protocol

Same shape as Arcs 25-30. PROJECT-TIER POLYBIUS (separate Claude Code session, activated from `HUMAN_paste-polybius-arc-31-instruction.md`) is your radio-check peer; you communicate via comments on `stoa--32b.1`. USER-TIER POLYBIUS dispatched this arc + will do QA pass at arc close per PRINCIPAL's pattern.

PRINCIPAL is **not** the relay for routine status — beadwork is.

**bw command syntax** is in `substrate/MAJOR_PLINY.md` §6.1. `bw comment <id> "text"` is positional. `bw close <id> --reason "text"` — `--reason` is a flag.

**Polling discipline** per `substrate/operating-disciplines.md` §7. On dispatch, post init handshake on `stoa--32b.1` naming cron id + cadence. Heartbeat every ≤30 min.

PLINY in autonomous mode. PRINCIPAL + user-tier POLYBIUS are exception-handlers — project-direction calls, ship/no-ship, substance disagreement after one round, authorship/copyright/PRINCIPAL-final-say content, irreducible ambiguity, peer silence > 60 min, arc closes.

---

## Read first

Before any design or build work, read in order:

1. **`bw show stoa--32b.1` ticket body in full + the 2026-05-16 sibling cross-ref comment.** Primary spec. Body has problem statement + PRINCIPAL phrasing + the discipline ("a design clause that names PRINCIPAL... is a BLOCK, not a TAG") + 5 deliverables + acceptance probes + out-of-scope + §15 caveat.

2. **`docs/sessions/2026-05-16-substrate-update-architecture-reframe--retro.md` §7** — the load-bearing source for the discipline. Read in full. The retro frames the conflation problem (autonomous-mode escalation vs PRINCIPAL-gate-block) more thoroughly than the ticket body. DAEDALUS treats this as primary input alongside the directive and ticket.

3. **`bw show stoa--dxw` + `bw show stoa--501`** at the-stoa bw store — Arc 26 (the empirical anchor) + the sector-4 cleanup ticket that demonstrated the gap. Closed; reading for context only.

4. **`substrate/operating-disciplines.md`** — full read. Current section structure (especially §10 / §11 around autonomous-mode + escalation triggers). D1 either extends §10/§11 OR adds a new section near them. DAEDALUS picks.

5. **`substrate/CAPTAIN_DAEDALUS.md` + `substrate/CAPTAIN_ADA.md` + `substrate/CAPTAIN_VERA.md`** — three envelope files D2 modifies. Each gets a new section about how the seat handles PRINCIPAL-gated clauses (DAEDALUS surfaces gating at design-time; ADA refuses to build past; VERA refuses to execute probes).

6. **`substrate/templates/autonomous-mode-activation-template.md`** — D3 modifies; pause-on-gate trigger added.

7. **`substrate/templates/polling-cron-prompt-template.md`** — D4 modifies; escalation step for PRINCIPAL-gate.

8. **Activation pastes from Arcs 27-30 at the-stoa root** — observe the ad-hoc "treat PRINCIPAL-discretion the NEW way" workaround that every recent paste has carried. Once this arc ships, future pastes can drop that workaround (the substrate canon handles it).

---

## Phase A — Architectural decisions (LOCKED pre-dispatch)

Settled during PRINCIPAL's 2026-05-16 declaration + ticket evolution. You do NOT surface these as design questions.

### A1. One arc, four phases, one gauntlet — LOCKED

`stoa--32b.1` is a coherent single work-unit. Single DAEDALUS design covering D1-D5. Single ARGUS audit (HIGH chance of revisions given architecture-sensitivity). Single ADA worktree on `arc-31/build`. Verifiers (VERA + CATO + ZENO) each one pass. **CATO mandatory** — substrate canon; wording precision is load-bearing.

Phasing:

| Phase | Seat(s) | Output |
|---|---|---|
| 1 | DAEDALUS + ARGUS | `agents/design/arc-31/design.md` — integrated design covering D1 operating-disciplines section; D2 three CAPTAIN envelope updates; D3 autonomous-mode template pause-on-gate; D4 polling-cron-prompt template escalation step; D5 probe-design sub-case (DAEDALUS picks fold-into-D2-VERA-envelope vs split-as-separate-section). ARGUS cold-audits; ADA does not dispatch until ARGUS PASS. |
| 2 | ADA | feature branch `arc-31/build` covering all substrate edits. |
| 3 | VERA + CATO + ZENO | parallel verification pass per Phase B acceptance probes. |
| 4 | PLINY + smoke + ship | smoke beats (per Phase C). PR opened. PLINY runs `gh pr merge` after clean PASS. `stoa--32b.1` closes. **User-tier POLYBIUS does QA pass at arc-close per PRINCIPAL pattern.** |

### A2. The discipline (locked by PRINCIPAL declaration) — LOCKED

PRINCIPAL declared on 2026-05-16:

> "Something that needs to be surfaced to a human needs to wait until the human comes back not bypassed because the human is afk."

The canon you encode in D1 should carry PRINCIPAL's exact phrasing (block-quote per Arc 27 §16.1 / Arc 29 §17.1 / Arc 30 §5.9 pattern). The substantive content:

- **PRINCIPAL-gate** = a design clause that names PRINCIPAL as the deciding seat for a load-bearing decision. Format examples: "PRINCIPAL-discretion per design §X", "PRINCIPAL ratifies before Phase 2", "blocked-on-PRINCIPAL", any clause where PRINCIPAL input is structurally required for the workflow to proceed correctly.
- **PRINCIPAL-gate is a BLOCK, not a TAG.** The workflow PAUSES at the gate until PRINCIPAL is present + provides the input. Autonomous mode does NOT skip past it.
- **Distinct from autonomous-mode escalation cadence.** Autonomous-mode escalation = WHEN to surface to PRINCIPAL during routine work (cadence discipline). PRINCIPAL-gate = WHETHER PRINCIPAL input is structurally required for this step (authorization discipline). The substrate currently conflates them; this discipline separates them.
- **PRINCIPAL-AFK on a PRINCIPAL-gated decision means the workflow waits.** Not "proceed-then-cleanup." Not "tag-for-disposition-later." Workflow pauses.

### A3. D1 locus pick — LOCKED with one DAEDALUS sub-decision

D1 lives in `operating-disciplines.md`. DAEDALUS picks between:

- **Option α:** Extend existing §10 / §11 (autonomous-mode discipline area) with a new sub-section for PRINCIPAL-gate.
- **Option β:** Add a new top-level section (e.g., §25) near §10/§11 + cross-ref.

Either is defensible. Option β is cleaner separation (gate-vs-cadence is genuinely distinct); Option α is more discoverable (operators looking at autonomous-mode find the gate-rule alongside). DAEDALUS picks based on which framing best surfaces the load-bearing distinction.

### A4. D2 CAPTAIN envelope shape — LOCKED

Each of the three named CAPTAIN envelopes (DAEDALUS, ADA, VERA) gets a new section about how the seat handles PRINCIPAL-gated clauses. Per-seat shape:

- **CAPTAIN_DAEDALUS.md** — when designing a directive/spec that contains a PRINCIPAL-gating clause, the designer MUST surface the gating to PRINCIPAL at design ratification time (not defer to post-build cleanup). The design output should make the gate visible so ARGUS audit can verify it's correctly framed.
- **CAPTAIN_ADA.md** — when implementing a directive that contains a PRINCIPAL-gated clause, ADA refuses to build past the gate without explicit per-execution PRINCIPAL authorization. ADA pauses + surfaces.
- **CAPTAIN_VERA.md** — when executing a probe that contains a PRINCIPAL-gated authorization (probes that would mutate a real workspace are a sub-case), VERA refuses to execute without explicit per-execution authorization. VERA pauses + surfaces. (See A6 for the probe-design sub-case.)

Cross-references between the three envelopes + D1 should resolve cleanly.

### A5. D3 + D4 template updates — LOCKED scope

**D3 — autonomous-mode-activation-template.md:** add a pause-on-gate trigger. The activation-time setup checklist (operating-disciplines.md §11) gains an explicit case: "if downstream encounters a PRINCIPAL-gated clause in the directive or in any sub-dispatch, HALT and escalate immediately rather than proceed-then-flag." DAEDALUS picks exact wording + placement.

**D4 — polling-cron-prompt-template.md:** add a PRINCIPAL-gate detection case to the escalation step. The fire-loop gains a check: "if aggregated state shows a PRINCIPAL-gated clause that hasn't been adjudicated, emit PushNotification + do NOT advance workflow state." DAEDALUS picks exact wording.

### A6. D5 probe-design sub-case — LOCKED scope; DAEDALUS picks fold-vs-split

Probes that would mutate a real workspace are a specific instance of the PRINCIPAL-gate discipline. The substrate-level rule: probes that mutate real workspaces require explicit per-execution operator authorization, NOT a design-time blanket "PRINCIPAL-discretion" clause. Throwaway clones (`git clone --local --shared <workspace> /tmp/<name>-probe`) are the canonical pattern when realistic workspace state is needed.

DAEDALUS picks:

- **Fold:** integrate the probe-design sub-rule into CAPTAIN_VERA.md's PRINCIPAL-gate section (D2). Single-locus; tighter.
- **Split:** carve out a separate subsection in operating-disciplines.md (under D1) OR a separate small canon section. Cleaner if probe-design feels distinct from the broader gate discipline.

Either is defensible. Empirical anchor (sector-4 Probe 8) is a VERA probe; folding into VERA envelope is natural; splitting allows broader application if other seats ever run mutation-style probes.

### A7. Cite-comment discipline — LOCKED

Cross-references between D1/D2/D3/D4/D5 should resolve via cite. Cite-comment pattern from Arc 26 / 28 / 29 / 30 applies: at every read-site that references another section, point at the substantive locus.

### A8. Authorship attribution — IMMUTABLE per CLAUDE.md

All edits credit Denson Smith. Arc 31 edits existing files (no new files with fresh author-like field exposure expected). Verify before commit.

### A9. Out of scope — HARD LOCKED

Do NOT do in this arc:

- **Reopening the substrate's existing escalation-triggers list at operating-disciplines.md.** This is additive (PRINCIPAL-gate is a NEW thing alongside escalation), not a rewrite of escalation cadence.
- **Editing Arc 26's VERA Probe 8 retroactively.** It shipped; stoa--501 closed it.
- **Building the inspection-agent pattern (stoa--32b.2).** Separate forthcoming arc.
- **Cron-hygiene canonification.** Separate forthcoming arc (canonification batch).
- **§5.1.1 cross-project context leak extension.** Separate arc.
- **Other CAPTAIN envelopes (CATO, ZENO, BARTLEBY, STRABO, HERALD, CURATOR).** D2 names DAEDALUS + ADA + VERA only; expanding scope here muddies the arc. If the other CAPTAINs need PRINCIPAL-gate awareness, it follows from the operating-disciplines.md canon they all read; their envelopes don't need explicit additions in this arc.
- **MAJOR role files (MAJOR_POLYBIUS, MAJOR_PLINY).** Convention applies via operating-disciplines.md canon; MAJOR-tier role files don't need direct envelope additions unless DAEDALUS surfaces a specific orchestration-level need that's distinct from what D3/D4 already cover.

If you find yourself reaching for any of the above, STOP and surface as substance-disagreement comment on `stoa--32b.1` (radio-check to user-tier POLYBIUS via [for: user-tier POLYBIUS] tag).

### A10. §15 N=1 honesty — LOCKED

N=1 empirical anchor (Arc 26 / sector-4 Probe 8 / stoa--501). PRINCIPAL declared the discipline 2026-05-16 (project-direction authority). Substrate canon enters off-gate on PRINCIPAL's declaration. Supporting evidence accretes when future arcs with PRINCIPAL-gated clauses correctly halt + escalate per the discipline.

The new canon sections must name this provenance — same shape as Arc 27 §16.6 / Arc 29 §17.1 / Arc 30 §5.9 N=1 framing. Do NOT over-generalize beyond what PRINCIPAL named.

### A11. Pre-branch hygiene — LOCKED + self-applied per Arc 30 §5.9

Before creating `arc-31/build`, PLINY runs the two-check rule per the Arc 30 canon you just inherit:

```
Check 1 (no other arc-build branch in flight):
  git branch | grep -E '^\s*arc-[0-9]+/build$'    # must be empty

Check 2 (local main = origin/main):
  git fetch origin main
  git log --oneline main..origin/main             # must be empty
  git log --oneline origin/main..main             # must be empty
```

User-tier POLYBIUS confirmed at dispatch authoring: both checks pass; local main = origin/main at `efb0394`; no other arc-build branches in flight (arc-29/build cleaned up; arc-24/build worktree + branch cleaned up; only `arc-24/build` remote ref remains as harmless tracking debris, not a local branch).

---

## Phase B — Verify (probes for VERA)

1. **D1 PRINCIPAL-gate section present** in operating-disciplines.md with PRINCIPAL block-quote verbatim + two-axis distinction (gate vs cadence) + "BLOCK not TAG" framing explicit.
2. **D2 CAPTAIN envelope updates** present in DAEDALUS + ADA + VERA envelopes with seat-specific wording per A4.
3. **D3 autonomous-mode template pause-on-gate trigger** present.
4. **D4 polling-cron-prompt template PRINCIPAL-gate escalation case** present.
5. **D5 probe-design sub-case** present per DAEDALUS's fold-vs-split pick.
6. **Cite-comments resolve** — cross-references between D1/D2/D3/D4/D5 all point at valid loci.
7. **§15 N=1 framing present** in D1's section — provenance + empirical anchor + accretion path.
8. **Synthetic-directive probe:** construct a small synthetic directive containing "PRINCIPAL-discretion per design §X"; verify that a fresh PLINY/POLYBIUS reading the new canon would correctly identify it as a workflow-pause trigger, not a post-hoc disposition tag.
9. **CURRENT regression:** check.sh against current registered workspaces still reports their expected drift (Arc 31 adds substrate content; the-stoa shows DRIFTED on the edited files; consumer workspaces handle on their own activation per §14).

CATO cold-reads:
- diff for wording drift, scope creep, cite-comment correctness, cross-reference correctness, authorship attribution
- PRINCIPAL's exact phrasing per A2 — block-quote verbatim
- §15 N=1 honesty per A10 — provenance named, no over-generalization
- Two-axis distinction (gate vs cadence) clearly framed; future POLYBIUSes reading must be able to tell which discipline applies in which case

ZENO checks stoa--32b.1 deliverables D1-D5 each marked DONE by artifact reference.

---

## Phase C — Smoke + ship

PLINY's smoke beats before opening PR:

- `grep -n "PRINCIPAL-gate\|BLOCK, not a TAG\|gate is a block" substrate/operating-disciplines.md` — D1 section present.
- `grep -n "PRINCIPAL-gate\|PRINCIPAL-discretion" substrate/CAPTAIN_DAEDALUS.md substrate/CAPTAIN_ADA.md substrate/CAPTAIN_VERA.md` — D2 envelope updates present.
- `grep -n "pause-on-gate\|PRINCIPAL-gate" substrate/templates/autonomous-mode-activation-template.md` — D3 present.
- `grep -n "PRINCIPAL-gate" substrate/templates/polling-cron-prompt-template.md` — D4 present.
- `grep -n "throwaway clone\|probes that mutate" substrate/CAPTAIN_VERA.md substrate/operating-disciplines.md` — D5 present per DAEDALUS pick (one or both files).
- check.sh against the-stoa — expected DRIFTED on substrate files this arc edits.

PR title: `Arc 31: PRINCIPAL-gate discipline encoded as substrate canon (closes the AFK-bypass gap)`
PR body: cross-ref `stoa--32b.1`, parent epic `stoa--32b`, retro §7 (load-bearing source), prior `stoa--dxw` (empirical anchor) + `stoa--501` (post-hoc gap), this directive at `substrate/arcs/arc-31-build-directive.md`.

Merge via `gh pr merge` after clean gauntlet PASS. Close `stoa--32b.1` with `--reason` referencing the merge commit. Tag `[for: user-tier POLYBIUS]` comment inviting QA pass.

---

## Honest scope reminder

Substantive multi-file substrate-canon arc. Comparable to Arc 25 / Arc 27 in scope (multi-section + multi-CAPTAIN + multi-template). DAEDALUS round + likely ARGUS revisions; ADA build; full verifier round; smoke + ship. ~1-2h CAPTAIN-agent wall-clock expected; could be longer if DAEDALUS surfaces fold-vs-split tradeoffs for D5.

End directive.
