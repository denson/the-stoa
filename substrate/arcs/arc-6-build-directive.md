# Arc 6 build directive

**Audience:** the fresh Claude Code session opened in this repo to build Arc 6 deliverables.
**Authored by:** user-tier Chief-of-Staff (POLYBIUS-equivalent) + the PRINCIPAL (Denson Smith).
**Status:** active directive.
**Builds on:** Arc 4 (commit `67d4589`, MAJOR role files re-authored to v2) + Arc 5 (commit `22780a0`, 10 CAPTAIN envelopes re-authored to v2).

**You are MAJOR_PLINY for the agent-substrate Arc 6 engagement.** The user-tier Chief-of-Staff (POLYBIUS-equivalent) wrote this directive; you receive it and execute. Per v2 §4, MAJOR_PLINY is the orchestrator role. Read `MAJOR_PLINY.md` (this repo, Arc 4's freshly-authored v2-shape file) and assume the orchestrator role.

**Your one job for this engagement:** re-author `ONBOARDING.md` and the three `templates/` files from v2 spec, with voice grounded in PRINCIPAL/HUMAN throughout. Then return cleanly. This is the final substrate-redesign-from-v2 arc; after it ships, the canonical substrate (MAJOR role files + 10 CAPTAINs + ONBOARDING + templates) is fully aligned with v2.

---

## Read first

1. **`plans/three-role-recursive-architecture.md` in user-beadwork — the v2 spec.** Primary source.
   - Read in full: §3 (naming convention + PRINCIPAL framework), §6 (Voice and language discipline), §8 (onboarding flow + custom paste-instruction templating + communication-discipline-during-onboarding subsection — directly relevant to your deliverables).

2. **Arc 4-5's freshly-authored substrate files (this repo):**
   - `MAJOR_POLYBIUS.md` (Arc 4) — voice exemplar; the onboarding flow you describe in ONBOARDING.md should match what POLYBIUS's role file says POLYBIUS does
   - `MAJOR_PLINY.md` (Arc 4) — voice exemplar
   - `CAPTAIN_*.md` (Arc 5, 10 files) — voice exemplars; absorb the per-envelope voice register

3. **The existing v1-shape files you're replacing** (read for operational content extraction only, not prose preservation):
   - `ONBOARDING.md` (existing, at repo root)
   - `templates/paste-instruction-template.md` — has the existing slot conventions (`{{PROJECT_NAME}}`, `{{SESSION_INTENT}}`, etc.) — preserve these slot names; v2 §8 settled the string-substitution mechanism
   - `templates/onboarding-questions.md` — has the interview question floor with rationale per question
   - `templates/consent-prompts.md` — has prompt structure (named action / reversibility / alternative / closed wording)

   **Same risk-mitigation as Arc 5:** extract operational facts (e.g., "consent prompts have 4 fields: named action, reversibility, alternative, closed wording"); do NOT copy prose verbatim. Voice-ground the freshly-authored versions.

4. **`u--7yg` design inputs:**
   - `u--7yg.20` (terminology fix that motivated v2) — re-read to internalize WHY voice matters
   - `u--7yg.13` (three-role architecture, includes the durable-substrate-with-short-prompts discipline corollary)

---

## Deliverables

### 1. Archive the existing v1-shape files

```bash
git mv ONBOARDING.md v1-historical/ONBOARDING.md
git mv templates/paste-instruction-template.md v1-historical/templates/paste-instruction-template.md
git mv templates/onboarding-questions.md v1-historical/templates/onboarding-questions.md
git mv templates/consent-prompts.md v1-historical/templates/consent-prompts.md
```

(create `v1-historical/templates/` directory if needed)

Add header notes pointing at v2 successors, mirroring what Arcs 4-5 did.

### 2. Author fresh `ONBOARDING.md` at repo root

End-to-end walkthrough of the onboarding flow per v2 §8. Same four scenarios as v1 (preserved as the test surface) but voice-grounded:

- **Scenario 1:** First-time PRINCIPAL, intent unclear → POLYBIUS interviews, suggests starting small with project-only deploy
- **Scenario 2:** Returning PRINCIPAL with prior beadwork → POLYBIUS reads existing state, picks up appropriately
- **Scenario 3:** PRINCIPAL who explicitly wants user-tier + project-tier → POLYBIUS confirms with informed consent
- **Scenario 4:** Compact-or-clear recovery — POLYBIUS notices MAJOR_PLINY lost its role, re-issues paste-instruction

Voice register matching Arc 4 + 5: dialogue uses PRINCIPAL where appropriate; specific named human references use the actual name once learned through interview.

### 3. Author fresh `templates/paste-instruction-template.md`

The string-substitution template POLYBIUS fills per session. Per v2 §8, slots:
- `{{PROJECT_NAME}}`, `{{SESSION_INTENT}}`, `{{BW_PREFIX}}`, `{{ROLE_FILE_PATH}}`, `{{PENDING_DIRECTIVES}}`, `{{ON_DISK_PATH}}`

Plus rationale per slot (so a future POLYBIUS reading the template understands WHY each slot is filled the way it is).

Voice-grounded. The template's narrative should refer to MAJOR_PLINY by role, not by mnemonic-only.

### 4. Author fresh `templates/onboarding-questions.md`

The interview floor POLYBIUS uses during onboarding. Per v2 §8:
- Questions about project intent + scope
- Questions to learn the PRINCIPAL's name
- Questions about deployment preferences
- Each question with rationale (so future POLYBIUS reading understands why this question matters)

Voice-grounded. Use PRINCIPAL throughout.

### 5. Author fresh `templates/consent-prompts.md`

Wording POLYBIUS uses when requesting informed consent for sensitive actions. Per v2 §8 + the existing v1 structure:
- Each prompt has: named action / reversibility / alternative / closed wording
- Cover at minimum: modifying user-tier `CLAUDE.md`, running install.sh against project, deploying CAPTAINs, etc.

Voice-grounded.

### 6. README update

Brief update mentioning Arc 6 ship. Note that the substrate redesign from v2 is now complete (Arcs 4-6).

---

## Voice discipline (load-bearing)

Same rules as Arcs 4-5:

1. PRINCIPAL for the human served (descriptive role)
2. HUMAN_<name> formal, or just <name> in dialogue (after onboarding learns name)
3. COLONEL only for the reserved future agent rank — rare in this material
4. Read-pass after first draft of each file; grep-check before commit

**Self-check:**

```bash
grep -i "colonel" ONBOARDING.md templates/*.md
```

Per Arc 5's pattern, occasional deliberate references to the reserved future rank are acceptable (e.g., in voice-discipline negation pointers). The check is "no reflexive leakage," not "zero matches."

**Special concern for ONBOARDING.md:** the scenarios are dialogue-heavy. Dialogue is where reflexive Colonel-leakage from v1 might be hardest to catch — it sounds natural to write "the Colonel asks" because that was v1 voice. Read each scenario specifically scanning for dialogue that should use PRINCIPAL or the named human.

---

## Definition of done

- `ONBOARDING.md` re-authored fresh with v2 voice; 4 scenarios covered
- 3 `templates/*.md` files re-authored with v2 voice; substitution slots + structures preserved
- All 4 v1 versions archived at `v1-historical/`
- `grep -i "colonel" ONBOARDING.md templates/*.md` self-check: any matches are deliberate, not reflexive
- README updated mentioning Arc 6 ship + substrate-redesign-from-v2 complete
- bw beadwork epic for Arc 6 closed
- All committed to `main` and pushed to origin (autonomous-ship per `u--7yg.11`)

---

## Out of scope

- **`install.sh` improvements** — Arc 7 handles Windows portability, deploying templates/, next-step guidance
- **Refactoring existing project deploys** — Arc 8
- **The Stoa updates** — Arc 9
- **Sub-project spawning** — Arc 10
- **Existing arc directives** (`arcs/arc-1-build-directive.md` through `arcs/arc-5-build-directive.md`) — these are historical records of what was directed at the time. Don't retrofit. Future arc directives (Arc 7+) use v2 voice from the start.

---

## Beadwork

`bw` is initialized (`as-` prefix). File a new epic for Arc 6:

```
bw create "[EPIC] Arc 6 — re-author ONBOARDING + templates from v2 spec" -t epic -p 1
```

File children: one per archived file (4), one per re-authored file (4), one for README update, one for voice self-check, one for testing pass. ~11 children.

Close as you go. Push beadwork branch when done.

---

## Discipline

Same as Arcs 4-5:

- HITL default (v2 §7)
- Principal-as-router (`u--7yg.1`) — surface only project-direction calls
- Verify-then-execute (`u--7yg.10`, `u--7yg.18`)
- One job per agent (`u--7yg.17`) — your one job is Arc 6
- Wait-for-quiescence (`u--7yg.15`)
- Autonomous-ship on clean PASS (`u--7yg.11`) — push is part of ship
- Voice discipline (v2 §6) — grep-check before commit

---

## Operating mode

**Human-in-the-loop** (v2 §7). Surface for input at:
- (a) ambiguity that needs PRINCIPAL input
- (b) work product ready for review (optional — autonomous push for clean self-validation)
- (c) done

For Arc 6: the dialogue-heavy ONBOARDING.md is the highest-risk surface for reflexive leakage. If that grep-checks cleanly, the rest should follow naturally.

---

## How to surface back

Either:
- Comment on a beadwork ticket in this repo (`as--*`)
- Write a short hand-back report; PRINCIPAL will relay

Standby, run.
