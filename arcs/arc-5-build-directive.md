# Arc 5 build directive

**Audience:** the fresh Claude Code session opened in this repo to build Arc 5 deliverables.
**Authored by:** user-tier Chief-of-Staff (POLYBIUS-equivalent) + the PRINCIPAL (Denson Smith).
**Status:** active directive.
**Builds on:** Arc 4 (commit `67d4589`) — MAJOR_POLYBIUS + MAJOR_PLINY re-authored against v2 spec; voice grounded in PRINCIPAL/HUMAN.

**You are MAJOR_PLINY for the agent-substrate Arc 5 engagement.** The user-tier Chief-of-Staff (POLYBIUS-equivalent) wrote this directive; you receive it and execute. Per v2 §4, MAJOR_PLINY is the orchestrator role — top-level Claude Code session at MAJOR rank, runs structured work, communicates back via beadwork or human relay.

Your first action: read `MAJOR_PLINY.md` (this repo, Arc 4's freshly-authored v2-shape file) and assume the orchestrator role.

**Your one job for this engagement:** re-author the 10 CAPTAIN envelope files from v2 spec, with voice grounded in PRINCIPAL/HUMAN throughout. Then return cleanly.

---

## Read first

1. **`plans/three-role-recursive-architecture.md` in user-beadwork — the v2 spec.** Primary source.
   - Read in full: §2 (the five ranks — including reserved COLONEL), §3 (naming convention — including PRINCIPAL framework), §6 (Voice and language discipline subsection — load-bearing for this arc), §9 (the Roster — your authoritative list of what each CAPTAIN does + structural properties like "no Write/Edit — structural"), §10 (build sessions).

2. **Arc 4's freshly-authored MAJOR role files (this repo, `MAJOR_POLYBIUS.md` and `MAJOR_PLINY.md`).** These are v2-voice exemplars. Read them to absorb the voice pattern for v2 — how PRINCIPAL is referenced, how disciplines are woven in, how operational details are framed. The CAPTAIN envelopes you author should match this voice register: workmanlike, role-specific, not chatty.

3. **`u--7yg` design inputs to focus on:**
   - `u--7yg.16` (envelope tool-set gaps) — make sure each CAPTAIN's claimed responsibilities match its actual tool access. Per v2 §9: ARGUS / CATO / CAPTAIN_PLINY have no Write/Edit tool (structural — no-fixes); BARTLEBY / HERALD / CAPTAIN_PLINY have no WebSearch/WebFetch (structural — internal-only scope); none have Agent (sub-agents can't dispatch per `u--7yg.12`).
   - `u--7yg.17` (one-job-per-agent) — important for keeping each CAPTAIN's role narrow and distinct
   - `u--7yg.20` (the terminology fix that motivated v2) — internalize WHY voice matters

4. **The existing v1-shape CAPTAIN envelopes in this repo** (at root: `CAPTAIN_DAEDALUS.md` etc.) — read these for **operational content extraction only.** Each envelope contains role-specific operational detail (artifact shapes, verdict formats, discipline notes) not fully captured in v2 §9. Extract those operational details into your working notes; don't preserve prose verbatim. Then voice-ground the freshly-authored versions.
   - **Risk:** reflexive Colonel-leakage from v1 vocabulary. Mitigate by extracting operational *facts* (e.g., "DAEDALUS produces a 5-section design.md") rather than copying prose.

---

## Deliverables

### 1. Archive the existing v1-shape CAPTAIN envelopes

Move existing files to `v1-historical/`:

```bash
git mv CAPTAIN_DAEDALUS.md v1-historical/CAPTAIN_DAEDALUS.md
git mv CAPTAIN_ARGUS.md v1-historical/CAPTAIN_ARGUS.md
git mv CAPTAIN_ADA.md v1-historical/CAPTAIN_ADA.md
git mv CAPTAIN_VERA.md v1-historical/CAPTAIN_VERA.md
git mv CAPTAIN_CATO.md v1-historical/CAPTAIN_CATO.md
git mv CAPTAIN_STRABO.md v1-historical/CAPTAIN_STRABO.md
git mv CAPTAIN_BARTLEBY.md v1-historical/CAPTAIN_BARTLEBY.md
git mv CAPTAIN_HERALD.md v1-historical/CAPTAIN_HERALD.md
git mv CAPTAIN_CURATOR.md v1-historical/CAPTAIN_CURATOR.md
git mv CAPTAIN_PLINY.md v1-historical/CAPTAIN_PLINY.md
```

Add a brief header note to each archived file pointing at the v2 successor (mirrors what Arc 4 did for MAJOR role files).

### 2. Author 10 fresh CAPTAIN envelopes at repo root

Per v2 §9 roster:

| File | Mnemonic | Descriptive role | Tool restrictions |
|---|---|---|---|
| `CAPTAIN_DAEDALUS.md` | DAEDALUS | ARCHITECT | standard sub-agent toolset |
| `CAPTAIN_ARGUS.md` | ARGUS | PLAN-CRITIC | **no Write/Edit** — structural |
| `CAPTAIN_ADA.md` | ADA | EXECUTOR | standard |
| `CAPTAIN_VERA.md` | VERA | VERIFIER | standard |
| `CAPTAIN_CATO.md` | CATO | REVIEWER | **no Write/Edit** — structural |
| `CAPTAIN_STRABO.md` | STRABO | SCOUT (external/web) | standard, with WebSearch/WebFetch |
| `CAPTAIN_BARTLEBY.md` | BARTLEBY | FILE_CLERK (internal) | **no WebSearch/WebFetch** — structural |
| `CAPTAIN_HERALD.md` | HERALD | INTAKE | **no WebSearch/WebFetch** — structural |
| `CAPTAIN_CURATOR.md` | CURATOR | SYNTHESIST | standard |
| `CAPTAIN_PLINY.md` | PLINY | SPEC-CHECKER | **no Write/Edit** AND **no WebSearch/WebFetch** — structural |

Each envelope should encode:
- Identity (rank, mnemonic, descriptive role)
- The agent's ONE job (per `u--7yg.17`)
- Toolset assumed available (with structural restrictions noted)
- Inputs the agent expects
- Outputs the agent produces
- How the agent communicates back (verdict format, structured return-payload)
- Disciplines specific to this seat
- Voice consistent with Arc 4's MAJOR role files: workmanlike, role-specific

### 3. README update

Brief update mentioning Arc 5 ship; point at the fresh CAPTAIN envelopes.

---

## Voice discipline (load-bearing — same as Arc 4)

Per v2 §6 "Voice and language discipline" + Arc 4's empirical validation:

1. **Default reference for the human is PRINCIPAL.** When a CAPTAIN's prose talks about "the one being served" or "the human-in-the-loop," use PRINCIPAL.
2. **For specific human references:** HUMAN_<name> formal, or just <name> in dialogue context.
3. **COLONEL only when explicitly discussing the reserved future agent rank.** Will be rare in CAPTAIN-envelope prose. If a CAPTAIN is written to surface output to "the Colonel," that's reflexive leakage — replace with PRINCIPAL.
4. **Read-pass after first draft of each envelope.** Each CAPTAIN gets its own grep-check before merging into the commit.

**Self-check before commit:**

```bash
grep -i "colonel" CAPTAIN_*.md
```

Every result should be a deliberate reference to the reserved future agent rank, not v1 reflex. Arc 4's clean grep produced 4 deliberate refs across 3 files; Arc 5 with 10 files might produce 0–10 deliberate refs depending on how often each role's prose needs to mention the reserved rank (probably 0 for most CAPTAINs — they're internal pipeline workers, not human-facing).

---

## Definition of done

- All 10 fresh CAPTAIN envelopes exist at repo root with v2 voice grounded throughout
- All 10 v1 versions archived at `v1-historical/CAPTAIN_*.md` with header notes
- `grep -i "colonel" CAPTAIN_*.md` self-check passes (no reflexive leakage; any matches are deliberate)
- Each envelope's claimed tool access matches v2 §9 structural restrictions
- README updated mentioning Arc 5 ship
- bw beadwork epic for Arc 5 closed
- All committed to `main` and pushed to origin (autonomous-ship per `u--7yg.11`)

---

## Out of scope

- **Templates** (`templates/paste-instruction-template.md`, etc.) — Arc 6 re-grounds them
- **`install.sh`** — Arc 7
- **Refactoring existing project deploys** — Arc 8
- **The Stoa updates** — Arc 9
- **Sub-project spawning** — Arc 10
- **MAJOR role files** — Arc 4 already shipped them; don't touch

---

## Beadwork

`bw` is initialized in this repo (`as-` prefix). File a new epic for Arc 5:

```
bw create "[EPIC] Arc 5 — re-author 10 CAPTAIN envelopes from v2 spec" -t epic -p 1
```

File children: one per archived file (10), one per re-authored file (10), one for README update, one for voice self-check pass, one for testing pass. That's ~22 children — reasonable for the scope.

Close them as you go. Push beadwork branch when done.

---

## Discipline

Same as Arc 4:

- **HITL default** (v2 §7) — PRINCIPAL supervising via user-tier CoS in Claude Desktop
- **Principal-as-router** (`u--7yg.1`) — surface only project-direction calls
- **Verify-then-execute** (`u--7yg.10`, `u--7yg.18`) — directive vs spec contradictions get surfaced
- **One job per agent** (`u--7yg.17`) — your one job is Arc 5; each CAPTAIN you author has one job
- **Wait-for-quiescence** (`u--7yg.15`) — surface ambiguities; don't barrel forward
- **Autonomous-ship on clean PASS** (`u--7yg.11`) — push to origin is part of the ship sequence
- **Voice discipline** (v2 §6, this directive) — grep-check before commit

---

## Suggested phasing (technical-tier, your call)

Arc 3 authored all 10 envelopes in one pass. Arc 5 is re-authoring (faster than fresh authoring) but still 10 files. Two reasonable phasings:

- **Phase A:** Author the 5 design-pipeline envelopes (DAEDALUS, ARGUS, ADA, VERA, CATO) — these are the most-used + share the most operational structure. Run grep-check, validate pattern.
- **Phase B:** Author the 5 support-roster envelopes (STRABO, BARTLEBY, HERALD, CURATOR, CAPTAIN_PLINY).
- **Phase C:** README update + final grep-check + commit + push.

Or grind all 10 in one pass with grep-check at end. Your call.

If Phase A's pattern validation is clean, no need to surface to the PRINCIPAL between phases — proceed to Phase B autonomously.

---

## Operating mode

**Human-in-the-loop** (per planning v2 §7). Surface for input at:
- (a) ambiguity that needs PRINCIPAL input
- (b) work product ready for review before commit (optional — autonomous push for clean self-validation per `u--7yg.11`)
- (c) done

For Arc 5 specifically: if Phase A's voice grounding works cleanly (grep-check passes, voice register matches Arc 4's MAJOR files), Phase B should proceed autonomously. Surface only if you hit ambiguity.

---

## How to surface back

Either:
- Comment on a beadwork ticket in this repo (`as--*`); user-tier CoS has visibility per `u--7yg.14`
- Write a short hand-back report; PRINCIPAL will relay

Standby, run.
