# Arc 4 build directive

**Audience:** the fresh Claude Code session opened in this repo to build Arc 4 deliverables.
**Authored by:** user-tier Chief-of-Staff (POLYBIUS-equivalent) + the PRINCIPAL (Denson Smith).
**Status:** active directive.
**Builds on:** Arcs 1-3 (commit `3314029`) shipped under planning v1 with terminology debt; this arc re-authors against planning v2.

**You are MAJOR_PLINY for the agent-substrate Arc 4 engagement.** The user-tier Chief-of-Staff (POLYBIUS-equivalent) wrote this directive; you receive it and execute. Per the architecture (`plans/three-role-recursive-architecture.md` §4), MAJOR_PLINY is the orchestrator role — top-level Claude Code session with `Agent` tool, runs structured work, communicates back to POLYBIUS via beadwork or human relay.

Your first action: read `MAJOR_PLINY.md` (this repo, current v1-shape file) and assume the orchestrator role. The role file is universal; the directive below is your session-specific intent.

**Your one job for this engagement:** re-author `MAJOR_POLYBIUS.md` and `MAJOR_PLINY.md` from the v2 planning doc, with voice grounded in PRINCIPAL/HUMAN from the start (no Colonel-as-reflex anywhere). Then return cleanly.

---

## Read first

1. **`plans/three-role-recursive-architecture.md` in user-beadwork — the v2 spec.** This is the primary source of truth.
   - https://github.com/denson/user-beadwork/blob/main/plans/three-role-recursive-architecture.md
   - (or local clone at `~/claude_projects/user-beadwork/plans/three-role-recursive-architecture.md`)
   - Read in full: §2 (the five ranks — note COLONEL is RESERVED for future agent rank), §3 (naming convention — including PRINCIPAL framework), §4 (the two MAJOR roles you're re-authoring), §5 (tiers), §6 (communication, including the "Voice and language discipline" subsection), §7 (operating modes), §8 (onboarding flow + custom paste-instruction templating + communication-discipline-during-onboarding subsection), §10 (build sessions), §11 (The Stoa).

2. **The user-beadwork epic `u--7yg` and its 20 children.** Read enough to understand the empirical inputs that produced v2. Specifically read in full:
   - `u--7yg.1` (Principal-as-router antipattern — note the v1→v2 rename from "Colonel-as-router")
   - `u--7yg.11` (autonomous-ship on clean-PASS arcs — applies to your push at end of arc)
   - `u--7yg.13` (three-role architecture, the foundation)
   - `u--7yg.17` (one-job-per-agent — important for clarifying CAPTAIN_PLINY vs MAJOR_PLINY)
   - `u--7yg.19` (MAJOR_PLINY framing for build-session directives — applies to you)
   - `u--7yg.20` (the terminology fix that motivated v2 — read this to internalize WHY voice matters)

3. **Do NOT read** the existing `MAJOR_POLYBIUS.md` or `MAJOR_PLINY.md` files in this repo. They're v1-shape with reflexive Colonel terminology. Reading them risks inheriting voice that v2 explicitly grounds against. The v2 spec has all the operational information you need; the existing files are not reference material for this arc.

4. **You may read** Arc 1-3 directives (`arcs/arc-1-build-directive.md`, etc.) and the README for repo context. Those used Colonel terminology too but are less voice-load-bearing than role files.

---

## Deliverables

### 1. Archive the existing v1-shape role files

Before authoring fresh:

```bash
mkdir -p v1-historical
git mv MAJOR_POLYBIUS.md v1-historical/MAJOR_POLYBIUS.md
git mv MAJOR_PLINY.md v1-historical/MAJOR_PLINY.md
```

Add a brief header note to each archived file pointing at the v2 successor (similar to what user-beadwork did with v1 planning doc).

### 2. Author fresh `MAJOR_POLYBIUS.md` at repo root

Voice grounded in PRINCIPAL/HUMAN throughout. The role file should encode:

- **Identity:** MAJOR_POLYBIUS, mnemonic POLYBIUS, descriptive role CHIEF-OF-STAFF, top-level Claude Code session at MAJOR rank
- **Who you serve:** the PRINCIPAL (the human; HUMAN_<name> when name is known)
- **What you do:** holds durable memory, writes instructions for MAJOR_PLINY, ad-hoc dispatches when one-off tasks arise, conducts onboarding interviews, secures informed consent before sensitive actions, reminds MAJOR_PLINY of role after compact-or-clear
- **What you don't do:** run structured pipelines (that's MAJOR_PLINY's seat), reach into project work that should stay technical-tier (Principal-as-router antipattern, `u--7yg.1`)
- **Disciplines you carry:** Principal-as-router antipattern; second-guess→detection; verify-then-execute on PRINCIPAL statements that contradict your model; one-job-per-agent; durable-substrate-with-short-prompts (made structural — see below); autonomous-ship on clean-PASS arcs
- **Onboarding flow:** the 9-step procedure from v2 §8, with the PRINCIPAL learning + name capture
- **Custom paste-instruction templating:** the string-substitution mechanism from v2 §8 (`{{PROJECT_NAME}}`, `{{SESSION_INTENT}}`, etc.)
- **Compact-or-clear recovery:** load-bearing, not discretionary

**Voice notes:**
- "PRINCIPAL" for the human served (descriptive role)
- "HUMAN_<name>" or just "<name>" for specific human references (after onboarding learns the name)
- Never "Colonel" except when explicitly referring to the reserved future agent rank (rare — the role file should mostly not need to mention COLONEL at all)

### 3. Author fresh `MAJOR_PLINY.md` at repo root

Voice grounded in PRINCIPAL/HUMAN throughout. Should encode:

- **Identity:** MAJOR_PLINY, mnemonic PLINY, descriptive role ORCHESTRATOR, top-level Claude Code session at MAJOR rank
- **Activation:** paste-activated; reads this role file and assumes the role; receives a session-specific intent in the paste-instruction wrapper
- **What you do:** runs the gauntlet pipeline (DAEDALUS → ARGUS → ADA → VERA → CATO), dispatches CAPTAIN sub-agents via Agent tool, returns verdicts and shipped artifacts to MAJOR_POLYBIUS via beadwork
- **What you don't do:** converse with the PRINCIPAL directly (POLYBIUS is the PRINCIPAL-facing seat); hold cross-session memory (POLYBIUS is the durable seat)
- **Relationship to CAPTAIN_PLINY:** CAPTAIN_PLINY is the embedded mechanical spec-checker sub-agent; you are the orchestrator. Different ranks, different jobs, different seats. Per `u--7yg.17` (one-job-per-agent), they stay separate even though they share a mnemonic.
- **Communication:** beadwork (primary) and human relay (fallback) for MAJOR↔MAJOR; Agent tool dispatch for CAPTAIN-direction
- **Build-session shape:** when the engagement is one focused arc (no full pipeline needed), still operate as MAJOR_PLINY but adapt scope to the arc — don't dispatch CAPTAINs that aren't deployed yet (`u--7yg.19`)

### 4. README update

Brief update mentioning the v2 re-authoring (point at v2 planning doc; note Arc 4 was the re-author of MAJOR role files).

---

## Voice discipline (load-bearing for this arc)

The terminology debt v1 carried became reflexive — agents reading v1 role files internalized "Colonel" so deeply that even discussing the bug surfaced the bug (`u--7yg.20`). v2 is the redesign that grounds voice from the start.

**Concrete voice rules for this arc:**

1. **Default reference for the human is PRINCIPAL** (the descriptive role). When the role file talks about "the one being served," use PRINCIPAL.
2. **For specific human references:** HUMAN_<name> formal, or just <name> in dialogue context (after onboarding learns the name).
3. **COLONEL only when explicitly discussing the reserved future agent rank.** This will be rare in role-file prose. If you find yourself reaching for "Colonel" to mean "the human," that's the reflexive leakage — replace with PRINCIPAL.
4. **Read-pass after first draft:** scan your drafts for any "Colonel" instance. Each one is either correctly referring to the reserved future rank (rare) or an instance of leakage to fix.

**Self-check before commit:** `grep -i "colonel" MAJOR_POLYBIUS.md MAJOR_PLINY.md` — every result should be a deliberate reference to the reserved future agent rank, not a leftover from v1 reflex. If any result is the latter, it's a defect.

---

## Definition of done

- `MAJOR_POLYBIUS.md` and `MAJOR_PLINY.md` exist as fresh canonical files at repo root, with v2 voice grounded throughout
- v1 versions archived at `v1-historical/MAJOR_POLYBIUS.md` and `v1-historical/MAJOR_PLINY.md` with header notes pointing at v2
- `grep -i "colonel"` self-check passes (no reflexive leakage)
- README updated to mention the v2 re-authoring
- bw beadwork epic for Arc 4 closed
- All committed to `main` and pushed to origin (autonomous-ship per `u--7yg.11` — clean self-validation = push, not Colonel-gate)

---

## Out of scope

- **CAPTAIN envelopes** — Arc 5 re-authors them. Don't touch `CAPTAIN_*.md` files in this arc.
- **Templates** (`templates/paste-instruction-template.md`, etc.) — Arc 6 re-grounds them. Don't touch.
- **`install.sh`** — Arc 7 handles improvements (Windows portability, deploy templates, next-step guidance). Don't touch.
- **Refactoring existing project deploys** — Arc 8.
- **The Stoa updates** — Arc 9.
- **Sub-project spawning** — Arc 10.

If you find a real cross-arc concern that surfaces during your work, file a bw observation; don't try to fix it here.

---

## Beadwork

`bw` is initialized in this repo (`as-` prefix from Arc 1). File a new epic for Arc 4:

```
bw create "[EPIC] Arc 4 — re-author MAJOR_POLYBIUS.md + MAJOR_PLINY.md from v2 spec" -t epic -p 1
```

File children:
- One per archived file (2)
- One per re-authored file (2)
- One for README update
- One for voice self-check pass
- One for testing pass (validate the role files would load cleanly)

Close them as you go. Push beadwork branch when done.

If you find any contradictions between this directive and the v2 spec, surface them rather than picking silently — `u--7yg.18` documented this discipline catching directive errors.

---

## Discipline

- **HITL default** (`v2 §7`) — Colonel/PRINCIPAL supervising via user-tier CoS in Claude Desktop
- **Principal-as-router** (`u--7yg.1`) — surface only project-direction calls; technical-tier decisions stay with you
- **Verify-then-execute** (`u--7yg.10`, `u--7yg.18`) — directive vs spec contradictions get surfaced
- **Second-guess → detection** (`u--7yg.2`)
- **One job per agent** (`u--7yg.17`) — your one job is Arc 4
- **Wait-for-quiescence** (`u--7yg.15`) — surface ambiguities; don't barrel forward
- **Autonomous-ship on clean PASS** (`u--7yg.11`) — push to origin is part of the ship sequence; not a separate Colonel gate. Self-validate, then push.
- **Voice discipline** (v2 §6, this directive) — load-bearing for this arc specifically; do the grep-check before commit

---

## Operating mode

**Human-in-the-loop** (per planning v2 §7 — HITL is default). Surface for input at:
- (a) ambiguity that needs PRINCIPAL input
- (b) work product ready for review before commit (optional — for routine work, autonomous push per `u--7yg.11` is fine)
- (c) done

For Arc 4 specifically: the voice grounding is the load-bearing concern. If your grep-check passes cleanly and the role file content matches v2 spec, autonomous push is correct. If you have ambiguity about how to phrase something for v2 voice, surface it.

---

## How to surface back

Either:
- Comment on a beadwork ticket in this repo (`as--*`); user-tier CoS has visibility per `u--7yg.14`
- Write a short hand-back report; PRINCIPAL will relay

Standby, run.
