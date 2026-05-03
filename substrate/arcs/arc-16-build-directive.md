# Arc 16 build directive — CAPTAIN_PLINY → CAPTAIN_ZENO rename

**Audience:** the fresh Claude Code session opened to build Arc 16 deliverables.
**Authored by:** user-tier Chief-of-Staff (POLYBIUS-equivalent) + the PRINCIPAL (Denson Smith).
**Status:** active directive.
**Builds on:** Arcs 1-15 (full v2 architecture deployed). Arc 16 is the first arc in a small **substrate-completeness sequence** (Arcs 16/17/18) surfaced by the explanatory-content work — gaps the case study + KG spec drafting revealed.

**You are MAJOR_PLINY for the the-stoa Arc 16 engagement.** Read `substrate/MAJOR_PLINY.md` and assume the orchestrator role. Open Claude Code in `~/claude_projects/the-stoa/`.

**Your one job:** rename the embedded mechanical spec-checker seat from `CAPTAIN_PLINY` to `CAPTAIN_ZENO`, propagate across substrate + planning spec + The Stoa app + tests, and refresh the user-tier deploy. Then return cleanly.

This is small. Pure mechanical refactor — no architectural changes. Probably 1-2 hours total. The shared-mnemonic role-collapse trap (CAPTAIN_PLINY vs MAJOR_PLINY) was real enough to warrant a structural rename rather than continuing to "lean against it explicitly in the role files." See the empirical-pattern signal section below.

---

## Read first

1. **The drafts at `the-stoa/docs/case-study/case-study.md` and `kg-spec.md`** — these explain *why* the rename. Particularly the case study's §3 paragraph about CAPTAIN_ZENO and the historical note in parentheses.
2. **`substrate/CAPTAIN_PLINY.md`** — the file you're renaming. Read it end-to-end so you know what it says before you move it.
3. **`substrate/MAJOR_PLINY.md`** §1, §2, §5, §8 (the entire "relationship to CAPTAIN_PLINY" section), §9 — the upstream role file with the most CAPTAIN_PLINY references.
4. **`substrate/MAJOR_POLYBIUS.md`** §4.4 — single mention of CAPTAIN_PLINY in the one-job-per-agent discipline.
5. **`substrate/install.sh`** — the `CAPTAIN_NAMES` array contains `PLINY` as one of the 10 names; needs to become `ZENO`.
6. **`substrate/README.md`** lines 52, 76, 78 — roster mentions.
7. **`app/scripts/gen-data-lib.ts`** + **`app/scripts/gen-data.ts`** — the build-time adapter; understand how it reads substrate filenames.
8. **`app/src/data/__tests__/generated.test.ts`** — generated-data shape invariant tests; reference the CAPTAIN slot containing 10 envelopes including PLINY.
9. **`user-beadwork/plans/three-role-recursive-architecture.md`** §3 (the "Same mnemonic with different ranks is allowed" subsection — lines ~88-95) and §9 (the roster table — line ~376).

---

## Why a rename, not just better disambiguation

Empirical signal: the v1→v2 voice-discipline lesson generalized. Two seats sharing a mnemonic produced reliable confusion *even when role files explicitly disambiguated them.* MAJOR_PLINY.md §8 currently exists as an entire section devoted to disambiguating MAJOR_PLINY from CAPTAIN_PLINY — when a defensive-disambiguation section becomes load-bearing, that's the signal that the underlying naming itself is the problem.

The rename eliminates the role-collapse trap **structurally** rather than continuing to defend against it. After Arc 16 lands, MAJOR_PLINY.md §8 either disappears or radically shrinks (a brief historical-note paragraph, parallel to how the case study's §3 paragraph handles it).

ZENO chosen because Zeno of Citium founded Stoicism (the very thing The Stoa is named after). Mnemonic ties to project name; thematic coherence; distinctive (no collision with other roster mnemonics).

---

## Deliverables

### 1. Rename the substrate file

`substrate/CAPTAIN_PLINY.md` → `substrate/CAPTAIN_ZENO.md`

Use `git mv` to preserve git history. Then update file contents:
- YAML frontmatter `name:` field: `CAPTAIN_PLINY{{NAME_SUFFIX}}` → `CAPTAIN_ZENO{{NAME_SUFFIX}}`
- YAML frontmatter `description:` field: update to reference ZENO and remove the "Distinct seat from MAJOR_PLINY orchestrator" framing (no longer needed structurally)
- Heading `# CAPTAIN_PLINY — Spec-checker` → `# CAPTAIN_ZENO — Spec-checker`
- Mnemonic field in the rank table: `PLINY` → `ZENO`
- `Lives at` field: path update to `CAPTAIN_ZENO{{NAME_SUFFIX}}.md`
- Body opening: `You are CAPTAIN_PLINY...` → `You are CAPTAIN_ZENO...`
- Any other internal CAPTAIN_PLINY references in the body — update all
- Voice check: the body should not have any framing that depends on the shared-mnemonic relationship with MAJOR_PLINY (since that relationship no longer exists)

### 2. Update `substrate/install.sh`

In the `CAPTAIN_NAMES` array, replace `PLINY` with `ZENO`. The order doesn't matter for correctness (the install script uses the array for log output; ordering preference is the gauntlet pipeline shape — DAEDALUS, ARGUS, ADA, VERA, CATO followed by support seats). Place `ZENO` in roughly the same slot `PLINY` occupied (last entry — embedded spec-checker is conceptually deepest in the pipeline).

### 3. Update `substrate/MAJOR_PLINY.md`

- §1, §2, §5: replace any reference to CAPTAIN_PLINY with CAPTAIN_ZENO (semantic content unchanged — same role, different name).
- **§8 "The relationship to CAPTAIN_PLINY"**: collapse to a single brief paragraph (PRINCIPAL locked this in pre-dispatch). Replace the current ~12-line section with a ~3-line historical-note paragraph: "CAPTAIN_ZENO is the spec-checker; this seat was renamed from CAPTAIN_PLINY in Arc 16 to eliminate the role-collapse trap from sharing a mnemonic with MAJOR_PLINY. The full disambiguation that previously lived here is preserved in `substrate/v1-historical/MAJOR_PLINY.md`." Parallel to how the case study handles it. Do NOT delete the section entirely — preserves design provenance for future readers without dwelling.
- §9 (Activation checklist): update any CAPTAIN_PLINY references.

### 4. Update `substrate/MAJOR_POLYBIUS.md`

§4.4 (One job per agent discipline) currently says: "This is the discipline that justifies keeping CAPTAIN_PLINY (the embedded mechanical SPEC-CHECKER sub-agent) separate from MAJOR_PLINY (the orchestrator) — same mnemonic, different ranks, different jobs, different seats."

Rewrite to reflect the rename — the one-job-per-agent discipline still applies (CAPTAIN_ZENO is its own seat for the spec-checker job, distinct from MAJOR_PLINY's orchestrator job, distinct from VERA's verification job), but the shared-mnemonic framing goes away. Something like: "This is the discipline that justifies CAPTAIN_ZENO (the embedded mechanical spec-checker, deep in the pipeline) being its own seat — distinct from MAJOR_PLINY's orchestrator job and from VERA's verification work. Each one-job-per-agent split prevents role-collapse; the rename of this seat from its earlier shared-mnemonic name (CAPTAIN_PLINY) was itself an application of the discipline (Arc 16)."

### 5. Update `substrate/README.md`

- Line 52 (Arc 5 description) — references CAPTAIN_PLINY tool restrictions; update to CAPTAIN_ZENO
- Line 76 (roster table) — file name + mnemonic + the "distinct from MAJOR_PLINY" annotation
- Line 78 (Note on naming) — the entire paragraph becomes obsolete; rewrite or delete. If rewrite: "Note on naming: CAPTAIN_ZENO is the embedded spec-checker (this seat was renamed from CAPTAIN_PLINY in Arc 16 to eliminate the role-collapse trap from sharing a mnemonic with MAJOR_PLINY). NESTOR (the would-be sub-agent dispatcher in earlier designs) does not appear; the role moves to MAJOR_PLINY at the top-level session tier (sub-agents cannot dispatch sub-agents — `u--7yg.12`)."

### 6. Update `substrate/templates/consent-prompts.md` and `substrate/ONBOARDING.md` (if needed)

Grep both files for CAPTAIN_PLINY / captain_pliny references. Update any matches. Likely minor or none.

### 7. Re-run gen-data + verify generated/agents.ts

```bash
cd app
npm run gen-data
```

This re-reads the substrate (now with `CAPTAIN_ZENO.md` instead of `CAPTAIN_PLINY.md`) and regenerates `app/src/data/generated/agents.ts`. The new file should have CAPTAIN_ZENO in the CAPTAIN slot instead of CAPTAIN_PLINY.

Verify the regeneration is byte-clean (no extraneous changes beyond the PLINY→ZENO swap):

```bash
git diff app/src/data/generated/agents.ts
```

### 8. Update `app/src/data/__tests__/generated.test.ts`

The test asserts the CAPTAIN slot contains 10 envelopes including specific named ones. Update any reference to `CAPTAIN_PLINY` / `PLINY` (in CAPTAIN context — be careful not to confuse with MAJOR_PLINY in MAJOR context) → `CAPTAIN_ZENO` / `ZENO`.

Run tests:

```bash
cd app && npm test
```

Should pass cleanly. If any test was hardcoded to expect PLINY in the CAPTAIN slot and you didn't update it, it'll fail loudly. Fix the test expectation, not by reverting the rename.

### 9. Update `app/src/data/__tests__/derive.test.ts` (if needed)

Grep for CAPTAIN_PLINY; update any matches. Likely no matches (derive.test.ts focuses on body-paragraph synthesis, which is name-agnostic), but verify.

### 10. Check `app/src/App.tsx` and `app/src/data/types-v2.ts`

Grep for CAPTAIN_PLINY in both. App.tsx may have routing references (route slugs are filename-based — `/#/agent/CAPTAIN_PLINY` would become `/#/agent/CAPTAIN_ZENO`). types-v2.ts may have JSDoc examples mentioning specific agent names.

Update any matches; verify dev server still works after:

```bash
cd app && npm run dev
```

Then in browser, navigate to `/#/agent/CAPTAIN_ZENO` — should render the new-named seat.

### 11. Update `user-beadwork/plans/three-role-recursive-architecture.md`

Two updates:

- **§3 "Same mnemonic with different ranks is allowed"** subsection (lines ~88-95): the entire subsection becomes obsolete. Replace with a brief historical-note paragraph: "Same mnemonic with different ranks was *previously* allowed in the architecture (PLINY appeared as both MAJOR_PLINY orchestrator and CAPTAIN_PLINY spec-checker), but the role-collapse trap was real enough to warrant structural rename — see Arc 16 (CAPTAIN_PLINY → CAPTAIN_ZENO). The architecture no longer relies on shared mnemonics with disambiguation; structurally distinct names are the discipline."
- **§9 (Roster table — line ~376)**: update CAPTAIN_PLINY → CAPTAIN_ZENO; update the description (no more "distinct from MAJOR_PLINY orchestrator" framing).

Commit + push to user-beadwork as a separate commit (different repo than the-stoa).

### 12. Refresh user-tier deploy

After substrate ships and is committed:

```bash
cd ~/claude_projects/the-stoa
./substrate/install.sh --target user
```

This deploys the renamed file. The OLD `~/.claude/agents/CAPTAIN_PLINY.md` does NOT auto-delete (install.sh doesn't remove obsolete files — known gap; explicitly out of Arc 16 scope).

### 13. Smoke test (with old-file-deletion reminder)

After all changes:
- `git status` shows only intended changes
- `npm run build` works (TypeScript clean)
- `npm test` passes
- `npm run dev` starts cleanly; navigate to `/#/agent/CAPTAIN_ZENO`; renders correctly
- The Stoa team view shows the CAPTAINs roster with ZENO instead of PLINY (the second one — the MAJOR PLINY pill is the orchestrator)
- `grep -ri "CAPTAIN_PLINY\|captain_pliny" the-stoa/substrate the-stoa/app the-stoa/docs --exclude-dir=v1-historical --exclude-dir=design_handoff_character_builder --exclude-dir=node_modules --exclude-dir=dist` returns zero
- Same grep against user-beadwork (excluding v1-historical) returns zero
- `~/.claude/agents/CAPTAIN_ZENO.md` deployed (verify with `ls ~/.claude/agents/ | grep -E "ZENO|PLINY"`)

### 13a. Surface back to PRINCIPAL — explicit reminder for manual file deletion (load-bearing)

After the smoke test passes and Arc 16 ships, the build session's hand-back to PRINCIPAL **must include explicit reminder text in this exact shape**:

> **Manual cleanup needed:** the old user-tier file `~/.claude/agents/CAPTAIN_PLINY.md` is now obsolete (CAPTAIN_ZENO supersedes it) but install.sh does not remove obsolete files (known install.sh gap, out of Arc 16 scope). Please delete manually:
>
> ```bash
> rm ~/.claude/agents/CAPTAIN_PLINY.md
> ```
>
> If this file remains, both CAPTAIN_PLINY (deprecated) and CAPTAIN_ZENO will be deployed at user-tier — confusing state. Verify deletion with `ls ~/.claude/agents/ | grep -E "ZENO|PLINY"` showing only CAPTAIN_ZENO.

This reminder is part of the deliverable, not optional. PRINCIPAL has confirmed (Arc 16 review) that they want this explicit in the hand-back rather than the build session leaving the cleanup as implied PRINCIPAL inference.

---

## Definition of done

- `substrate/CAPTAIN_PLINY.md` renamed to `substrate/CAPTAIN_ZENO.md` via `git mv` (history preserved); content updated
- `substrate/install.sh` `CAPTAIN_NAMES` updated
- `substrate/MAJOR_PLINY.md` §8 collapsed to a brief historical-note paragraph (or deleted entirely); other internal references updated
- `substrate/MAJOR_POLYBIUS.md` §4.4 rewritten without shared-mnemonic framing
- `substrate/README.md` lines 52, 76, 78 updated
- `substrate/templates/consent-prompts.md` and `ONBOARDING.md` checked + updated if needed
- `app/src/data/generated/agents.ts` regenerated via `npm run gen-data`
- `app/src/data/__tests__/generated.test.ts` updated; `npm test` passes
- `app/src/App.tsx` and `app/src/data/types-v2.ts` checked + updated if needed
- `user-beadwork/plans/three-role-recursive-architecture.md` §3 + §9 updated; committed + pushed separately
- User-tier deploy refreshed; PRINCIPAL surfaced that old CAPTAIN_PLINY.md needs manual deletion
- Smoke test passes (build, tests, dev server, voice audit)
- bw `stoa--*` epic for Arc 16 closed
- Committed + pushed to `the-stoa` main (autonomous-ship per `u--7yg.11`)

---

## Out of scope

- **Arc 17 (POLYBIUS authoring capabilities + agent-authoring skill + skills deployment)** — drafted after Arc 16 lands so changes can be authored against the post-rename substrate state
- **Arc 18 (polling capability + consent in role files)** — drafted after Arc 17
- **The case study + KG spec drafts at `docs/case-study/`** — already updated by user-tier CoS to reference CAPTAIN_ZENO; do NOT modify these files in Arc 16
- **Historical artifacts** — `substrate/v1-historical/`, `app/design_handoff_character_builder/`, `app/data-samples/`, `app/agents/`, `substrate/arcs/arc-2/3/4/5/12-1*-build-directive.md`, `user-beadwork/plans/v1-historical/` — preserved snapshots; do NOT modify
- **install.sh hardening for staleness detection** — separate concern; if you observe the gap (old CAPTAIN_PLINY.md deploy needs manual deletion), file as a small ticket but do NOT expand Arc 16 to address it
- **Modifying retrospective at `user-beadwork/retrospectives/v2-arcs-1-14.md`** — checked; no CAPTAIN_PLINY references; leave as-is

---

## Voice discipline

After all changes:

```bash
grep -ri "CAPTAIN_PLINY\|captain_pliny" \
  the-stoa/substrate \
  the-stoa/app \
  the-stoa/docs \
  --exclude-dir=v1-historical \
  --exclude-dir=design_handoff_character_builder \
  --exclude-dir=node_modules \
  --exclude-dir=dist
```

Should return zero. Same against `user-beadwork/` (excluding v1-historical). Any remaining matches are a regression.

`grep -ri "colonel"` audit against substrate role files should still return only deliberate reserved-future-rank references (§4.7 / §8 voice discipline section in MAJOR_POLYBIUS.md).

---

## Beadwork

`bw` already initialized (`stoa-` prefix). File a new epic:

```bash
cd ~/claude_projects/the-stoa
bw create "[EPIC] Arc 16 — CAPTAIN_PLINY → CAPTAIN_ZENO rename" -t epic -p 1
```

File children for: substrate file rename + content, install.sh update, MAJOR_PLINY.md §8 collapse, MAJOR_POLYBIUS.md §4.4 rewrite, README.md updates, templates check, gen-data re-run, test updates, app code check, planning spec updates (separate user-beadwork commit), user-tier refresh + old-file flag, smoke test. Close as you go.

---

## Discipline

- HITL default (planning v2 §7) — supervising via user-tier CoS
- Principal-as-router (`u--7yg.1`) — surface only project-direction calls (probably none for Arc 16; mechanical refactor)
- Verify-then-execute (`u--7yg.10`, `u--7yg.18`) — particularly when deciding which references to update vs leave (preserve historical / archived snapshots)
- One job per agent (`u--7yg.17`) — your one job is Arc 16; resist scope creep into Arc 17 (authoring + skills) or Arc 18 (polling)
- Wait-for-quiescence (`u--7yg.15`)
- Autonomous-ship on clean PASS (`u--7yg.11`)
- Voice discipline (planning v2 §6)
- **Fix-now (`§4.8` in MAJOR_POLYBIUS.md, freshly propagated in Arc 15)** — if you find related defects (e.g., other shared-mnemonic risks, install.sh staleness gap), fix them now in this arc rather than ticketing for later, OR ticket with concrete next-step plan if the fix is genuinely scope-different

**Special concern: don't let the rename leak into v1-historical or other archived directories.** The grep voice audit specifically excludes those because they're frozen snapshots — modifying them would corrupt the design provenance. The smoke test exclusions are load-bearing.

---

## Operating mode

**Human-in-the-loop** (planning v2 §7). Surface for input at:
- (a) Choice between deleting MAJOR_PLINY.md §8 entirely vs collapsing to brief historical note (recommend brief note; surface only if you have a strong reason for full deletion)
- (b) Any cross-repo coordination question (the user-beadwork commit is separate from the-stoa commit; surface if the sequence matters for your shipping plan)
- (c) Work product ready for review (optional — autonomous push for clean self-validation)
- (d) Done

For Arc 16: this is mechanical refactor work with one architectural call (§8 disposition). Otherwise autonomous.

---

## How to surface back

Either:
- Comment on the bw epic in this repo (`stoa--*`)
- Write a short hand-back report; PRINCIPAL will relay

For Arc 16: clean ship hand-back can be one paragraph ("Arc 16 shipped at commit `<sha>`; CAPTAIN_PLINY renamed to CAPTAIN_ZENO across substrate + spec + Stoa + tests; user-tier deploy refreshed; old CAPTAIN_PLINY.md flagged for manual deletion at `~/.claude/agents/CAPTAIN_PLINY.md`; voice audit clean").

---

## After Arc 16

Arc 17 (POLYBIUS authoring capabilities + agent-authoring skill + skills deployment) gets drafted by user-tier CoS once Arc 16 lands. The Arc 17 changes will be authored against the post-rename substrate state to avoid merge conflicts.

After Arc 17: Arc 18 (polling capability + consent discipline in MAJOR_POLYBIUS.md and MAJOR_PLINY.md + small spec §6.2 co-edit).

The case study + KG spec drafts at `docs/case-study/` will be committed + pushed once the substrate-completeness sequence (Arcs 16/17/18) ships, so the drafts ship referencing the latest substrate state.

Standby, run.
