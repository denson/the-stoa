# Arc 14 build directive — sub-project spawning mechanism

**Audience:** the fresh Claude Code session opened to build Arc 14 deliverables.
**Authored by:** user-tier Chief-of-Staff (POLYBIUS-equivalent) + the PRINCIPAL (Denson Smith).
**Status:** active directive.
**Builds on:** Arcs 1-13 — substrate redesigned, gen-data adapter live, sample.ts retired, components consume v2 types directly, Vitest scaffold + baseline tests, gen-data idempotent, install.sh hardened with backup-before-modify.

**You are MAJOR_PLINY for the the-stoa Arc 14 engagement.** Read `substrate/MAJOR_PLINY.md` and assume the orchestrator role. Open Claude Code in `~/claude_projects/the-stoa/`.

**Your one job for this engagement:** make sub-project spawning a real deployable capability — extend `install.sh` to support `--target subproject`, extend `MAJOR_POLYBIUS.md` with a sub-project spawning procedure, add a fifth scenario to `ONBOARDING.md`, and update templates as needed. Then return cleanly.

This is the **final v2 arc.** After Arc 14 lands, the v2 architecture is fully shipped — substrate (Arcs 1-7) + propagation/consolidation (Arcs 8 + Z) + The Stoa rebuild (Arcs 9-13) + recursive sub-project capability (Arc 14).

Modest scope but architecturally important. The spec has been describing sub-project spawning as a load-bearing capability since v1; Arc 14 makes it real.

---

## Read first

1. **Planning v2 spec** §5 (Tiers — recursive) — defines the sub-project relationship to parent project: shares parent's repo + bw, disambiguates by name suffix
2. **Planning v2 spec** §12 open question 4 — the operational-specifics call you need to settle in Phase A
3. **`substrate/MAJOR_POLYBIUS.md`** — particularly §5 (onboarding flow) and §6 (compact-or-clear recovery); you'll add a sub-project spawning section
4. **`substrate/install.sh`** — the current `--target user|project` modes; you're adding a third
5. **`substrate/ONBOARDING.md`** — the four existing scenarios; you're adding a fifth
6. **`substrate/templates/paste-instruction-template.md`** — may need sub-project-aware extensions
7. **`substrate/templates/consent-prompts.md`** — may need a sub-project consent prompt

---

## Colonel call — surface early in Phase A before locking in

**The sub-project naming/location decision.** Spec §12.4 explicitly defers this to "when the first real sub-project gets spawned" — that moment is now. Three plausible shapes:

- **(a) Subdirectory of parent.** `<parent>/<subproject-slug>/.claude/MAJOR_POLYBIUS_<subproject>.md`, `<parent>/<subproject-slug>/.claude/agents/CAPTAIN_*_<subproject>.md`. Cleanest reading of spec §5 ("reuse parent's repo + bw, disambiguate by suffix"). The sub-project is a real subdirectory in the parent's working tree; bw is shared (same repo, same beadwork branch). Sessions cd into the subdirectory.
- **(b) Sibling directory at parent's level.** `<parent-parent>/<subproject>/.claude/...` configured to point bw at parent's repo. More awkward — the sub-project lives outside the parent's tree but borrows its bw. Probably worse.
- **(c) Naming-convention only.** Everything stays in parent's `.claude/`; sub-project gets `MAJOR_POLYBIUS_<subproject>.md` etc. alongside parent's `MAJOR_POLYBIUS_<project>.md`. No new directory at all. Disambiguation is purely by filename suffix.

PRINCIPAL leans **(a) subdirectory** — matches spec §5's "share parent's repo + bw, disambiguate by suffix" most literally, gives sessions a clean cd-into-this-directory activation pattern, and the directory itself is a useful semantic boundary (the sub-project's working files can live there too). **Surface (a) vs (b) vs (c) decision to PRINCIPAL early in Phase A** before install.sh and MAJOR_POLYBIUS edits cement around it. If a different shape is more workable for what you actually find in the install code, surface that finding.

---

## What Arc 14 is

The architecture has described a recursive three-role pattern across user-tier → project-tier → sub-project-tier since v1. User-tier and project-tier are real and deployable today (`install.sh --target user|project`). Sub-project-tier has been described in the spec but not implemented as a deployable.

Arc 14 closes that loop. Three deliverables:

### Part A: `install.sh --target subproject`

Extend the install script with a third target mode that:
- Takes a `--parent-dir <path>` flag pointing at the parent project's directory (the project that will host the sub-project)
- Takes a `--subproject <slug>` flag naming the sub-project (e.g., `--subproject design-tier`)
- Creates the sub-project directory under the parent (per the (a) Phase-A decision, modulo what you actually settle on)
- Deploys `MAJOR_POLYBIUS.md` and `MAJOR_PLINY.md` to the sub-project's `.claude/` with the `_<subproject>` suffix in the filename and `{{NAME_SUFFIX}}` substitution applied
- Deploys the 10 CAPTAIN envelopes with `_<subproject>` suffix (parallel to project-tier's existing suffix logic)
- Does NOT redeploy `templates/` (parent already has them; sub-project shares parent's runtime tooling)
- Does NOT modify any `CLAUDE.md` (parent's modification, if any, is already in place; sub-project doesn't need its own)
- Does NOT run `bw init` (sub-project shares parent's bw repo)
- Prints next-step guidance specific to the sub-project flow (cd into the new subdirectory, activate POLYBIUS for the sub-project tier)

### Part B: `MAJOR_POLYBIUS.md` extension

Add a section (probably §10 — sub-project spawning, after §9 activation checklist) covering:
- **Trigger recognition** — when does the parent project's POLYBIUS recognize "this should be a sub-project"? Specialization signals from spec §5: own tools, own domain, possibly own human collaborator. Listing the trip-wires.
- **Walk-through procedure** — the parallel to §5's onboarding flow, but for spawning a sub-project rather than installing fresh. Read parent state, propose sub-project shape, get consent (sensitive: creating new directory in parent), run install.sh with subproject target, hand off paste-instruction for sub-project's MAJOR_PLINY.
- **Asymmetric beadwork visibility** (recursive) — parent-project POLYBIUS sees sub-project beadwork tags; sub-project POLYBIUS doesn't see parent's by default. Spec §6 says this; the section makes the practical implications explicit.
- **The hand-off** — the parent's POLYBIUS produces a paste-instruction for the sub-project's POLYBIUS to activate from. The sub-project POLYBIUS, once activated, runs its own onboarding (a smaller version — substrate is already deployed, bw already initialized, just needs to read state and pick up sub-project intent).

### Part C: `ONBOARDING.md` Scenario 5

Add a fifth scenario: **Sub-project spawning.** Use case: **a design tier sub-project — UI design pass on a specific Stoa view with a designer in the human-loop seat.** This is the spec-canonical example: planning v2 §5 explicitly names "design work on a specific UI component spinning up a sub-team with design-specific tools and a designer in the human-loop seat." Hits all three sub-project trigger signals: own tools (design-specific tooling, mockup software, design-system references), own domain (UI/visual design vs architectural code), own human collaborator (a designer rather than the engineering-tier PRINCIPAL). Authority bonus: scenario is illustrating something the architecture spec already names as a canonical sub-project case. Show:
- The parent project's POLYBIUS recognizing the sub-project signal
- The walk-through dialog (parallel to scenarios 1-3 in shape)
- The install.sh invocation
- The paste-instruction handoff
- The sub-project's POLYBIUS picking up cleanly

Match the existing scenarios' format: PRINCIPAL lines in italics, POLYBIUS lines in plain text, tool actions in code blocks.

### Part D: Template extensions (as needed)

- **`paste-instruction-template.md`** — may need a `{{SUBPROJECT_NAME}}` slot (or similar) so paste-instructions for sub-project orchestrators are unambiguous about which tier they're activating into. Surface only if the existing template can't accommodate the sub-project case cleanly.
- **`consent-prompts.md`** — add a sub-project-spawning consent prompt parallel to the existing modify-CLAUDE.md and bw-init prompts. Pattern: state what's being created, name the path, ask binary, wait for answer.

### Part E: Smoke test

Verify end-to-end:
- `./install.sh --target subproject --parent-dir <test-parent> --subproject test-sub` succeeds with no errors
- The expected files land at the expected paths with the expected `_test_sub` suffix
- `--dry-run` works for the new mode
- Parent's `CLAUDE.md` is NOT modified by the subproject install
- bw is NOT re-initialized (running `bw list` from parent or from sub-project shows the same tickets — same repo)
- A tabletop run of Scenario 5 against the live templates produces a coherent paste-instruction (same disciplinary check as scenarios 1-4 in the existing ONBOARDING.md)

---

## Definition of done

- `install.sh` supports `--target subproject --parent-dir <path> --subproject <slug>` with appropriate validation, idempotency (re-running with same flags is safe), dry-run support, and next-step guidance
- `MAJOR_POLYBIUS.md` has a sub-project spawning section that an activated POLYBIUS can run from cold
- `ONBOARDING.md` has Scenario 5 in the same shape as scenarios 1-4
- Templates extended only as needed (do not gold-plate)
- Smoke test passes (install.sh runs cleanly in the new mode; substrate is deployable end-to-end)
- bw `stoa--*` epic for Arc 14 closed
- Voice clean — `grep -i "colonel" substrate/install.sh substrate/MAJOR_POLYBIUS.md substrate/ONBOARDING.md substrate/templates/` shows only the deliberate reserved-future-rank reference (if any)
- Committed + pushed to `the-stoa` main (autonomous-ship per `u--7yg.11`)

---

## Out of scope

- **The Stoa display updates for sub-projects** — defer to a future arc. The Stoa app currently renders the rank ladder for a single project's roster; rendering a parent's roster + a sub-project's roster together is a separate display concern. Arc 14 is the *deployment* mechanism; the visualization can come later when an actual sub-project is in use.
- **Recursive sub-sub-project depth (sub-project spawning sub-projects)** — the spec describes the pattern as recursive, but Arc 14 ships parent → sub-project. Sub-sub-projects fall out of the same install.sh logic naturally (re-run with the sub-project as parent), but explicit testing of N-deep recursion is deferred until empirical signal.
- **Cross-sub-project coordination** — sub-projects of the same parent don't talk to each other in v2; if that turns out to matter, it's a future arc.
- **Rewriting v1 substrate references** — already done in earlier arcs.
- **Modifying types-v2.ts, the gen-data adapter, generated/agents.ts, or any Stoa app code** — Arc 14 is substrate-and-onboarding work, not Stoa work. The Stoa visualization of sub-projects is the explicitly-deferred display concern above.

---

## Voice discipline

`grep -i "colonel" substrate/` after work — any matches should be deliberate (e.g., the COLONEL rank label as the reserved future rank, or v1-historical preservation). The new prose uses v2 vocabulary throughout:

- **PRINCIPAL** for the human served (in role files and onboarding scenarios)
- **HUMAN_<name>** for specific named human references (in conversational examples)
- **MAJOR_POLYBIUS / MAJOR_PLINY / CAPTAIN_<mnemonic>** for agent references
- **Sub-project** as the relationship; **`<subproject>` slug** for the suffix
- COLONEL only when discussing the reserved future agent rank

Scenario 5's PRINCIPAL example name: **Denson** (the actual PRINCIPAL — scenarios 1-3 used invented names Sam/Avery/Jordan because those onboarding flows were generic; Scenario 5 illustrates real sub-project work, so the actual PRINCIPAL's name is appropriate).

---

## Beadwork

`bw` already initialized (`stoa-` prefix). File a new epic:

```bash
cd ~/claude_projects/the-stoa
bw create "[EPIC] Arc 14 — sub-project spawning mechanism (final v2 arc)" -t epic -p 1
```

File children for: Phase A naming-decision surface, install.sh extension, MAJOR_POLYBIUS extension, ONBOARDING Scenario 5, template updates (if any), smoke test, voice audit. Close as you go.

---

## Discipline

- HITL default (planning v2 §7) — supervising via user-tier CoS
- Principal-as-router (`u--7yg.1`) — surface only project-direction calls (Phase A naming decision; possibly any specialization-signal-recognition framing for §10)
- Verify-then-execute (`u--7yg.10`, `u--7yg.18`)
- One job per agent (`u--7yg.17`) — your one job is Arc 14; resist scope creep into Stoa display work, into types-v2 modifications, or into generic install.sh refactoring
- Wait-for-quiescence (`u--7yg.15`)
- Autonomous-ship on clean PASS (`u--7yg.11`)
- Voice discipline (planning v2 §6)

**Special concern:** the `--target subproject` mode introduces a third deployment shape that interacts with the parent's existing deployment. The smoke test specifically verifies the parent's `CLAUDE.md` is NOT touched and bw is NOT re-initialized — those would be regressions on the parent's existing setup. Belt-and-suspenders: dry-run before applying, eyeball the diff on a test parent before declaring the smoke test passed.

---

## Suggested phasing

The arc is mid-sized but has discrete pieces. Phase your work:

- **Phase A: Surface the naming/location decision (Colonel call).** Read spec §5 + §12.4, examine install.sh's existing `--target project` logic, propose the chosen shape with one or two alternatives surfaced. Wait for PRINCIPAL response. ~10-20 min for the surface; PRINCIPAL response unblocks. If shape (a) is chosen, the rest of the arc proceeds against subdirectory-of-parent semantics; if (b) or (c), the install.sh work changes shape.
- **Phase B: Extend install.sh.** Add the `--target subproject` mode, validation, idempotency, dry-run support, next-step guidance. Test against a synthetic parent project.
- **Phase C: Extend MAJOR_POLYBIUS.md.** Add the §10 sub-project spawning section. Voice grounded in PRINCIPAL/HUMAN.
- **Phase D: Add ONBOARDING Scenario 5.** Match the format of scenarios 1-4. Pick a load-bearing-rare use case worth illustrating.
- **Phase E: Update templates if needed.** Only as needed — do not gold-plate.
- **Phase F: Smoke test + voice audit + ship.**

If Phase A's response is the leaning (a) subdirectory, Phases B-F proceed without additional Colonel surfaces unless you hit something genuinely ambiguous (e.g., a specific install.sh implementation detail that has multiple defensible shapes). Otherwise the build is mechanical-after-modeled-on-existing.

---

## Operating mode

**Human-in-the-loop** (planning v2 §7). Surface for input at:
- (a) The naming/location decision (Phase A — required)
- (b) Any non-obvious template extension (Phase E)
- (c) Work product ready for review (optional — autonomous push for clean self-validation)
- (d) Done

For Arc 14: this is mostly mechanical (install.sh extension follows the existing `--target project` pattern; new ONBOARDING scenario follows the existing four). The architectural calls are concentrated in Phase A. Once that decision is settled, the rest is straightforward execution.

---

## How to surface back

Either:
- Comment on a beadwork ticket in this repo (`stoa--*`)
- Write a short hand-back report; PRINCIPAL will relay

For Arc 14: the Phase A surface needs structured response (option choice + brief rationale); the closing hand-back can be short ("Arc 14 shipped at commit <sha>; v2 fully landed").

---

## After Arc 14

The v2 architecture is then fully shipped. The post-v2 arc sequence in the planning spec (§14) ends here. Subsequent work is post-v2 capability arcs — Stoa display refinements, additional skills, additional CAPTAIN envelopes if needed, real sub-project spawnings as work calls for them — but the foundation is complete.

If you ship Arc 14 cleanly, surface that the v2 architecture is now end-to-end deployable: substrate + propagation + Stoa rebuild + sub-project recursion. PRINCIPAL will want to mark that milestone explicitly (planning v2 spec update, retrospective, possibly a v2.1 capture if anything from Arcs 1-14 surfaced empirical revisions to the spec itself).

Standby, run.
