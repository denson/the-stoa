# Arc 33 build directive — Mechanical-script / agent-inspection split

**Audience:** the fresh Claude Code session opened to build Arc 33 deliverables (MAJOR_PLINY at the-stoa tier).
**Authored by:** user-tier MAJOR_POLYBIUS + the PRINCIPAL (Denson Smith).
**Status:** active directive. **Arc 32 (`stoa--ewn`) is CLOSED**; precondition satisfied.
**Bw ticket:** `stoa--32b.2` (the work-unit; child of `stoa--32b` epic; sibling to `stoa--32b.1` already shipped as Arc 31).
**Builds on:** Arcs 1-32 (the-stoa main as of `84f1f86`).

**Your one job:** encode the **mechanical-script / agent-inspection split** as a substrate pattern. PRINCIPAL declared on 2026-05-16: "we are spending way too much time trying to get script workflows perfect when the answer is to run the script, then run an agent with a script to check what happened including anything strange and then let polybius fix any of the strangeness with human approval if necessary." This arc gives the substrate a NEW component for the inspection-agent layer + a worked example deployment + a discipline-doc addition documenting the 3-step pattern.

**Why this arc is the structural enforcement layer for Arc 31's §25 prose discipline:** §25 (PRINCIPAL-gate) is currently prose-only — agents read the canon, recognize gates, and pause. Probe 8 Half 2 in Arc 31 confirmed recognition-under-load works at N=1 but is fragile (relies on every future agent reading + recognizing). The inspection-agent layer would MECHANICALLY enforce §25 by inspecting post-execution state for gate violations. Same shape applies to Arc 32's §19.6 (attestation-confabulation) + §5.10 (signoff-accuracy) — mechanical inspection enforces prose discipline.

One ticket, one coherent push:
- **stoa--32b.2** (P2) — the inspection-agent pattern. Body has 4 deliverables + acceptance probes + out-of-scope. **DAEDALUS treats ticket body + the 2026-05-17 scope-refresh comment as primary input prose alongside this directive.** The refresh comment carries updated cross-refs (Arcs 28-32 all relevant), updated DAEDALUS guidance, updated §15 N=1 framing.

This is the BIGGEST architectural arc remaining at the-stoa. Comparable to Arc 29 in scope (multi-file substrate canon + new skill component). DAEDALUS round + likely ARGUS revisions; ADA build; full verifier round; smoke + ship. ~1-2h CAPTAIN-agent estimated.

---

## Comms — autonomous mode via bw, radio-check protocol

Same shape as Arcs 25-32. PROJECT-TIER POLYBIUS (separate session, activated from `HUMAN_paste-polybius-arc-33-instruction.md`) is your radio-check peer; you communicate via comments on `stoa--32b.2`. USER-TIER POLYBIUS dispatched this arc + will do QA pass at arc close per PRINCIPAL's pattern.

PRINCIPAL is **not** the relay for routine status — beadwork is.

**bw command syntax** is in `substrate/MAJOR_PLINY.md` §6.1. `bw comment <id> "text"` is positional. `bw close <id> --reason "text"` — `--reason` is a flag.

**Polling discipline** per `substrate/operating-disciplines.md` §7. On dispatch, post init handshake on `stoa--32b.2` naming cron id + cadence. Heartbeat every ≤30 min.

PLINY in autonomous mode. PRINCIPAL + user-tier POLYBIUS are exception-handlers per Arc 31 §25 escalation triggers — PRINCIPAL-gate clauses are BLOCKS (halt + escalate immediately), not TAGS.

---

## Read first

Before any design or build work, read in order:

1. **`bw show stoa--32b.2` ticket body in full + the 2026-05-17 scope-refresh comment.** Primary spec. Body has the 3-step pattern + 4 deliverables + acceptance + out-of-scope. The scope-refresh comment carries the intervening-arc context + DAEDALUS guidance + updated §15 N=1 framing + cross-refs. Treat both as primary input prose alongside this directive.

2. **`docs/sessions/2026-05-16-substrate-update-architecture-reframe--retro.md` §8** — the load-bearing source for the pattern. Read in full.

3. **`substrate/operating-disciplines.md` §25** (Arc 31 PRINCIPAL-gate discipline) — directly relevant: inspection-agent layer is the MECHANICAL enforcement of §25's prose. Read in full.

4. **`substrate/operating-disciplines.md` §19.6** (Arc 32 attestation-confabulation) + **`substrate/MAJOR_PLINY.md` §5.10** (Arc 32 signoff-accuracy) — disciplines the inspection-agent could mechanically enforce. Inspection-agent layer is the WHERE that verifies attestation claims at attestation time + verifies cleanup claims at signoff time.

5. **`substrate/skills/check-bw-release/`** (Arc 28) — small inspection-shape skill working precedent. SKILL.md + check.sh together demonstrate the skill-as-inspection-agent shape at small scope (compare current bw release tag to baseline; flag if new).

6. **`substrate/skills/check-substrate-updates/`** (Arcs 26 + 29) — larger inspection-shape skill. The Arc 26 ship was the empirical anchor for "script bloat" (the pattern this arc seeks to inverse). Reading the current state shows what the skill BECAME after Arc 26's make-script-comprehensive approach.

7. **`substrate/MAJOR_POLYBIUS.md` §17** (Arc 29 base-vs-custom convention) — the inspection-agent layer MUST respect base-vs-custom scoping when inspecting workspace state.

---

## Phase A — Architectural decisions (LOCKED pre-dispatch)

Settled during 2026-05-16/17 sessions + ticket evolution + scope-refresh comment. You do NOT surface these as design questions.

### A1. One arc, four phases, one gauntlet — LOCKED

`stoa--32b.2` is a coherent single work-unit. Single DAEDALUS design covering all deliverables. Single ARGUS audit (revisions LIKELY given architecture-sensitivity + multiple DAEDALUS picks below). Single ADA worktree on `arc-33/build` per Arc 32 §5.9.4 (worktree at `.claude/worktrees/arc-33-build/`; recursively self-applies the convention). Verifiers (VERA + CATO + ZENO) each one pass. **CATO mandatory** — substrate canon + new substrate skill; wording precision matters.

Phasing:

| Phase | Seat(s) | Output |
|---|---|---|
| 1 | DAEDALUS + ARGUS | `agents/design/arc-33/design.md` — integrated design covering substrate-component-shape pick (A2), skill naming + worked-example domain (A3), operating-disciplines.md pattern documentation (A4), cross-refs to §25 / §19.6 / §5.10 / §17 (A5). ARGUS cold-audits. |
| 2 | ADA | feature branch `arc-33/build` in separate worktree per §5.9.4. Substrate edits + new skill files. |
| 3 | VERA + CATO + ZENO | parallel verification pass per Phase B acceptance probes. |
| 4 | PLINY + smoke + ship | smoke beats (per Phase C). PR opened. PLINY runs `gh pr merge` after clean PASS. `stoa--32b.2` closes. PLINY signoff per §5.10 (live-verified cleanup claims). **User-tier POLYBIUS does QA pass at arc-close per PRINCIPAL pattern.** |

### A2. Substrate-component-shape pick — LOCKED scope; DAEDALUS picks specific form

**Option α (RECOMMENDED): new substrate-tier skill.** Mirror the shape of `substrate/skills/check-bw-release/` and `substrate/skills/check-substrate-updates/`. POLYBIUS/PLINY-invokable via Skill tool or direct script call. Light to deploy via install.sh's SKILL_NAMES; light to deprecate if pattern doesn't prove out.

**Option β: CAPTAIN_VERA envelope extension.** Extend VERA with post-mechanical-inspection sub-discipline. VERA already runs probes; "post-mechanical inspection" is a natural extension. Risk: VERA is verifier-of-arc-deliverables; inspection-agent is verifier-of-mechanical-script-outputs; different domains.

**Option γ: new CAPTAIN seat (e.g., CAPTAIN_INSPECTOR).** Heavier — structural pipeline component PLINY dispatches as a phase. Defer to future arc IF the skill pattern proves out and warrants pipeline-level integration.

User-tier POLYBIUS lean: **Option α (new skill)**. Lightest deploy; matches existing inspection-skill precedents; can grow to Option β or γ in a future arc if pattern proves out and demands it.

DAEDALUS picks final form. If picking Option α, document why not β or γ (so future arcs reading this know the deferral rationale).

### A3. Skill naming + worked-example domain — LOCKED scope; DAEDALUS picks

If Option α picked: skill name candidates (DAEDALUS picks):
- `inspect-script-output` (generic; clear)
- `script-output-inspection` (more verbose)
- `post-script-inspection` (clear what triggers it)
- `inspection-agent` (naming honesty; explicit about pattern)

User-tier POLYBIUS lean: `inspect-script-output`. Generic enough to apply across domains; honest about what it does.

**Worked-example domain (LOCKED):** substrate-update flow. Post-`apply.sh` / post-`install.sh` inspection. What "strangeness" means for substrate-update:
- Unauthorized commits to consumer workspaces (e.g., probe-residue from prior gauntlets)
- File states that don't match intent (custom files at base paths; base files modified locally)
- Drift verdict mismatching detailed state (CURRENT verdict but unexpected file mtimes; etc.)
- Cleanup claims that didn't actually execute (per §5.10)
- Attestation claims that don't cite live-verified state (per §19.6)
- PRINCIPAL-gate clauses encountered but not paused-on (per §25)

The worked example operationalizes the 3-step pattern: mechanical apply.sh runs → inspection skill reads result + workspace state → POLYBIUS triages findings (fix-now for routine; surface for PRINCIPAL on gated cases per §25).

### A4. operating-disciplines.md pattern documentation — LOCKED scope; DAEDALUS picks insertion locus

New section in `operating-disciplines.md` documenting the 3-step pattern. DAEDALUS picks insertion locus (likely near §11 autonomous-mode-setup OR as a new top-level section after §26 Arc 32's cron-hygiene cross-ref).

Content (DAEDALUS scopes precision):
- The 3-step pattern: mechanical script → inspection agent → POLYBIUS triage
- When to apply: substrate-update flow, deploy workflows, future script-based workflows
- Cross-ref to §25 (gate discipline governs triage step), §19.6 (attestation-confabulation; inspection enforces), §5.10 (signoff-accuracy; inspection enforces), §17 (base-vs-custom; inspection respects scoping)
- Discipline framing: "when designing a script-based workflow, prefer mechanical-narrow + inspection-agent over make-script-comprehensive"
- Empirical anchor: Arc 26 make-script-comprehensive (the negative example), check-bw-release (Arc 28; positive small-scope example), this arc (positive worked-example deployment)

### A5. Cross-refs — LOCKED

Cross-references between the new substrate component + existing canon must resolve cleanly:
- Inspection-skill SKILL.md → §25 (gate discipline) + §19.6 (attestation) + §5.10 (signoff) + §17 (base-vs-custom) + new operating-disciplines.md section
- New operating-disciplines.md section → all of the above + Arc 26 (empirical anchor) + Arc 28 check-bw-release (small precedent)
- Other CAPTAIN envelopes (VERA particularly) → cross-ref the new skill IF DAEDALUS picks Option α
- MAJOR_POLYBIUS.md / MAJOR_PLINY.md → minimal touch unless DAEDALUS surfaces a real need

### A6. Authorship attribution — IMMUTABLE per CLAUDE.md

All edits credit Denson Smith. Arc 33 adds NEW skill files (SKILL.md + check script likely); the SKILL.md frontmatter MUST carry `author: Denson Smith` per Arc 27 stoa--uly convention. Verify all new files before commit.

### A7. Out of scope — HARD LOCKED

Do NOT do in this arc:

- **Unwinding Arc 26's check.sh additions.** Check.sh stays as-is; this arc adds the INSPECTION-AGENT pattern alongside, not a regression of script-as-implementation.
- **Refactoring check-bw-release skill.** Arc 28 shipped it as positive precedent; this arc references it, doesn't modify it.
- **Building inspection-agents for every existing script.** Worked example + pattern doc; concrete adoption is INCREMENTAL across future arcs.
- **Mechanical enforcement of §25 / §19.6 / §5.10 / §17 as REQUIRED by this arc.** This arc provides the inspection-agent COMPONENT + worked example. Mechanical enforcement of specific disciplines is FUTURE arc work where inspection-skill deployment + the gate / attestation / signoff / scope discipline integrate per use case.
- **CAPTAIN_INSPECTOR new seat.** Option γ is explicitly deferred to future arc.
- **Multi-skill rollout** (inspection-skill for deploy workflows, for ariadne integration, etc.). One worked example (substrate-update flow); future arcs adopt elsewhere.
- **Sibling stoa--32b.1 (PRINCIPAL-gate) revision.** Arc 31 shipped that; not revisited here.
- **Other hygiene tickets (stoa--k36 / stoa--f37 / stoa--ize / stoa--3qi).** Separate.

If you find yourself reaching for any of the above, STOP and surface as substance-disagreement comment on `stoa--32b.2` (radio-check to user-tier POLYBIUS via [for: user-tier POLYBIUS] tag).

### A8. §15 N=1 honesty — LOCKED per refresh comment

Empirical anchors (per refresh comment):
- N=2 bit-by-it of make-script-comprehensive pattern: Arc 26 + Arc 28 (each added more script logic)
- N=1 small-scope precedent: check-bw-release skill (Arc 28) — small inspection-shape skill working without script-bloat
- N=multi cross-discipline benefit: §25 + §19.6 + §5.10 + §17 + §5.9.4 all benefit from mechanical inspection enforcement

The new operating-disciplines.md section must name PRINCIPAL-declaration provenance (2026-05-16) + empirical anchors above + accretion path against §6.7.1 gate. Same shape as Arc 27 §16.6 / Arc 29 §17.1 / Arc 30 §5.9.3 / Arc 31 §25.6 / Arc 32 §19.6 / §5.10 / §5.9.4 N=1 framings.

Do NOT over-generalize beyond what PRINCIPAL named. The pattern is "prefer mechanical-narrow + inspection-agent over make-script-comprehensive WHEN designing script-based workflows" — not "all scripts must have inspection-agents now."

### A9. Pre-branch hygiene per Arc 30 §5.9 + worktree convention per Arc 32 §5.9.4 — SELF-APPLIED

Before creating `arc-33/build`, verify the two-check rule per MAJOR_PLINY.md §5.9. Use separate worktree per §5.9.4: `git worktree add .claude/worktrees/arc-33-build arc-33/build`. Main worktree stays on main; user-tier POLYBIUS can operate concurrently.

User-tier POLYBIUS confirmed at dispatch authoring: local main = origin/main at `84f1f86`; no orphan arc-build branches. Should be clean at branch creation time.

### A10. Signoff-accuracy per Arc 32 §5.10 + attestation-honesty per §19.6 — SELF-APPLIED

PLINY's signoff at arc close must live-verify cleanup claims per §5.10:
- arc-33/build branch deletion: actually executed (git worktree remove + git branch -D + git push origin --delete; verify via git branch + git ls-remote)
- Worktree removal: actually executed (verify via git worktree list)
- PR squash: actually merged (verify via git log)

PLINY's attestations throughout (e.g., A9 init-handshake claim that pre-branch checks PASS) must cite live-verified state per §19.6: cite the SHA observed at attestation time, not the dispatch-authoring SHA `84f1f86` echo.

---

## Phase B — Verify (probes for VERA)

1. **Substrate component present** at DAEDALUS's picked Option (α / β / γ); locus + naming per A2/A3.
2. **Worked-example deployment present** — if Option α picked, the new skill's check script runs against a synthetic substrate-update operation and surfaces a planted strangeness item correctly.
3. **operating-disciplines.md pattern documentation present** with 3-step pattern + when-to-apply + cross-refs + §15 N=1 framing per A8.
4. **Cross-refs resolve** — inspection-skill → §25 / §19.6 / §5.10 / §17 / new section; new section → empirical anchors + cross-refs.
5. **install.sh SKILL_NAMES** includes new skill if Option α picked.
6. **Synthetic-inspection probe:** plant a strangeness item in a test workspace (e.g., a custom file at a base path that violates §17; OR an unauthorized commit residue; OR an unverified-claim attestation); run the new inspection skill; verify it surfaces the planted item with sufficient detail for POLYBIUS triage.
7. **Authorship audit:** new SKILL.md frontmatter has `author: Denson Smith`; no LLM placeholders.
8. **CURRENT regression:** check.sh against the-stoa workspace shows expected DRIFTED on substrate files this arc edits.

CATO cold-reads:
- diff for wording drift, scope creep, cite-comment correctness, cross-reference correctness, authorship attribution
- §15 N=1 honesty per A8 — no over-generalization
- 3-step pattern clarity — future POLYBIUSes reading the canon should be able to identify which step they are at + which seat owns each
- Inspection-skill domain scope — clear what's in-scope for inspection (mechanical-script output) vs out-of-scope (existing CAPTAIN-driven verification)

ZENO checks stoa--32b.2 deliverables D1-D4 each marked DONE by artifact reference.

---

## Phase C — Smoke + ship

PLINY's smoke beats before opening PR:

- `grep -n "mechanical-script\|inspection-agent\|inspection agent" substrate/operating-disciplines.md` — new section present.
- `ls substrate/skills/<new-skill-name>/` — skill files present if Option α picked.
- `grep -n "<new-skill-name>" substrate/install.sh` — SKILL_NAMES append if Option α.
- Synthetic-inspection smoke beat — plant strangeness in test workspace; run new skill; verify surfaces correctly.
- check.sh against the-stoa — expected DRIFTED on substrate files this arc edits.

PR title: `Arc 33: mechanical-script / agent-inspection split — substrate pattern + worked-example deployment`
PR body: cross-ref `stoa--32b.2`, parent epic `stoa--32b`, sibling `stoa--32b.1` (Arc 31 PRINCIPAL-gate), Arcs 28 / 29 / 30 / 32 cross-refs per refresh comment, this directive at `substrate/arcs/arc-33-build-directive.md`.

Merge via `gh pr merge` after clean gauntlet PASS. **PLINY signoff per §5.10:** verify cleanup claims (worktree remove + branch delete local + remote + PR merge) by live state inspection. Close `stoa--32b.2` with `--reason` referencing the merge commit. Tag `[for: user-tier POLYBIUS]` comment inviting QA pass.

---

## Honest scope reminder

Substantive multi-file substrate arc + new substrate component. Comparable to Arc 29 in scope. DAEDALUS round + likely ARGUS revisions (multiple DAEDALUS picks); ADA build (skill files + canon section); full verifier round including synthetic-inspection smoke; smoke + ship. ~1-2h CAPTAIN-agent wall-clock estimated.

The substrate canon side is medium-sized (one new operating-disciplines.md section + cross-refs). The skill side is the heavier piece (new substrate component; mirror existing inspection-skill precedents at check-bw-release / check-substrate-updates).

End directive.
