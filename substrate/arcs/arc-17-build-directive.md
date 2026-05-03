# Arc 17 build directive — POLYBIUS authoring capabilities + agent-authoring skill + skills deployment

**Audience:** the fresh Claude Code session opened to build Arc 17 deliverables.
**Authored by:** user-tier Chief-of-Staff (POLYBIUS-equivalent) + the PRINCIPAL (Denson Smith).
**Status:** active directive.
**Builds on:** Arcs 1-16 + Arc 16.1 (the-stoa main `39f3983`). Substrate is fully v2-voiced + ZENO-renamed + bw-syntax-teaching shipped. This is the second arc in the substrate-completeness sequence (Arcs 16/17/18) surfaced by the explanatory-content work.

**You are MAJOR_PLINY for the the-stoa Arc 17 engagement.** Read `substrate/MAJOR_PLINY.md` and assume the orchestrator role. Open Claude Code in `~/claude_projects/the-stoa/`.

**Your one job:** add three POLYBIUS authoring capabilities to the substrate (pair-programmer Major authoring + pair-programming-for-prototyping methodology + agent-authoring LIEUTENANT skill), extend `install.sh` to deploy LIEUTENANT skills, fold in the install.sh staleness fix from `stoa--w1t`, and update the planning v2 spec §4 to reflect that pair-programmer Majors are an on-demand third class of MAJOR role. Then return cleanly.

This is a medium-sized arc. Comparable to Arc 14 (sub-project spawning). Probably 2-4 hours; phase your work; surface design decisions before locking in.

---

## Comms — direct async with POLYBIUS via bw (proven in Arc 16)

POLYBIUS (user-tier CoS in a separate Claude Code session) and you both communicate via comments on the Arc 17 bw epic in the-stoa repo (prefix `stoa--*`). PRINCIPAL is **not** the relay for routine status — beadwork is.

**Asymmetric polling discipline** (verified working in Arc 16):
- You do NOT poll while you are working
- You DO poll when you are waiting (between phases, after surface, after hand-back) — `CronCreate` with `*/5 * * * *` cadence
- POLYBIUS sets up its own polling cron at engagement start

**bw command syntax** — read `MAJOR_PLINY.md` §6.1 for the full table. Critical: `bw comment <id> "text"` (positional, NO `-m` flag). Run `bw prime` at activation per the updated checklist.

---

## Read first

1. **`docs/case-study/case-study.md`** §3 (paragraph about CAPTAIN_ZENO seat), §3.5 (trust patterns), and especially **§6.5 (Two operational modes — formal gauntlet vs. pair-programming for prototyping)** — the case study explains *why* this arc; §6.5 is the prototyping methodology you'll formalize as substrate §12
2. **`substrate/MAJOR_POLYBIUS.md`** — particularly §4 (disciplines), §5 (onboarding flow), §10 (sub-project spawning, Arc 14 pattern). §11 + §12 will follow §10's structure
3. **`substrate/install.sh`** — current TEMPLATE_NAMES + CAPTAIN_NAMES patterns; you'll add a SKILL_NAMES array + deploy step parallel to the existing template-deploy
4. **`user-beadwork/plans/three-role-recursive-architecture.md`** §4 (current "two MAJOR roles per tier" framing) — needs reframe per the empirical pair-programmer pattern
5. **`stoa--w1t`** ticket — install.sh staleness gap (obsolete deployed files); concrete fix sketch in the ticket; fold into Arc 17's install.sh changes
6. **agent-gauntlet's `skills/` directory** (`~/claude_projects/agent-gauntlet/skills/`) — existing skill SKILL.md shape; the new agent-authoring skill follows this pattern; example skills: `dispatch-lieutenant`, `format-validate`, `runner`, `pulse-review`, `cite-check`

---

## Phase A — Three architectural decisions (locked pre-dispatch by PRINCIPAL)

The build session does NOT need to surface these as Colonel calls — they were settled during the Arc 17 directive review. Recorded here for context + execution:

### A1. Skills deployment shape — LOCKED: always deploy

`install.sh` always deploys all skills in substrate; no opt-out flag. Simpler; matches templates pattern. Skills are universal helpers; opt-out doesn't have a clear use case.

### A2. Agent-authoring skill — LOCKED: drafts go direct to substrate

The `LIEUTENANT_agent_author` skill writes drafts directly to substrate (e.g., `substrate/CAPTAIN_<NEW>.md` or `substrate/MAJOR_<NEW>.md`). POLYBIUS reviews the draft in the working tree and commits when satisfied. No `substrate/drafts/` staging overhead — substrate is git-tracked, so the working-tree-vs-committed boundary IS the review gate.

**Inputs the skill takes:**
- agent type (pair-programmer Major / specialized CAPTAIN / new LIEUTENANT)
- name / mnemonic
- specialization / domain
- key responsibilities (what the seat does, what it doesn't)
- template basis (which existing agent to base on — closest-fit existing seat)

**Outputs:** draft role file content with proper frontmatter, sections matching existing role files' shape, voice-discipline check (PRINCIPAL/HUMAN throughout, no Colonel leakage, no second-person framing).

### A3. stoa--w1t fold-in shape — LOCKED: detect + flag-gated prune

`install.sh` warns by default about obsolete deployed files; adds a `--prune-obsolete` flag that enables automatic removal. The warning output names the obsolete files explicitly so PRINCIPAL can `rm` them manually if preferred. Auto-remove is too aggressive for installs that touched user-tier directories with mixed content; warn-only without the flag is the safe default.

---

## Deliverables

### 1. MAJOR_POLYBIUS.md §11 — Pair-programmer Major authoring

Add a new §11 to `substrate/MAJOR_POLYBIUS.md` after §10 (Sub-project spawning, Arc 14). Parallel structure to §10. Content:

- **Trigger recognition** — when does POLYBIUS recognize a pair-programmer is the right shape? Substantive domain work (Python, regulation, design, etc.); HUMAN benefits from MAJOR-rank specialist; not gauntlet-shaped (different from PLINY's pipeline); not ad-hoc-shaped (different from a one-off CAPTAIN dispatch). The "fast prototyping team" framing.
- **Walk-through procedure** — discuss task with PRINCIPAL → invoke `LIEUTENANT_agent_author` skill (Deliverable 3) to generate the draft role file → review draft → commit substrate → write paste-instruction → hand off to PRINCIPAL.
- **Empirical lineage** — examples of pair-programmer Majors POLYBIUS has authored: ATTICUS (meta-team editorial in agent-gauntlet), PYTHAGORAS (Python work), CODEX (code at large), LEX (regulation). Light touch — these are illustrative, not a fixed roster.
- **Asymmetric beadwork visibility** for pair-programmers (probably: pair-programmer reads task-specific bw scope; doesn't see broader project bw unless explicitly granted).

### 2. MAJOR_POLYBIUS.md §12 — Pair-programming-for-prototyping methodology

Add §12 after §11 (this arc). Captures the "Two operational modes" framing from case study §6.5. Content:

- **The two-mode framing** — formal gauntlet vs. pair-programming-for-prototyping (parallel to case study)
- **The 7-step prototyping cycle** — POLYBIUS authors pair-programmer → PRINCIPAL pairs → POLYBIUS in the loop → prototype produced → POLYBIUS authors directive → PLINY runs gauntlet → shipped artifact
- **When to use which mode** — trigger patterns (brand-new shape vs established shape; fast iteration vs production rigor; etc.)
- **Cite the empirical claim** — "we started moving much faster when we empowered POLYBIUS to quickly create specialized pair-programmers" — same framing as case study §6.5

### 3. `substrate/skills/agent-author/SKILL.md` — Agent-authoring LIEUTENANT skill

Create a new skill following the existing skill pattern (`agent-gauntlet/skills/<name>/SKILL.md` shape). Content:

- **Skill metadata** — name, description, inputs, outputs
- **Procedure** — POLYBIUS-invoked; takes agent specs; reads a template existing agent role file as basis; generates a draft with substituted content + voice-discipline check; writes draft to substrate (per Phase A2 (i) decision)
- **Voice discipline check** — verify the draft uses PRINCIPAL/HUMAN throughout, no Colonel leakage, no second-person framings (these are the load-bearing voice issues from v1→v2)
- **Template-basis selection guidance** — for a new pair-programmer Major, ATTICUS or a generic pair-programmer template; for a new CAPTAIN, the closest-fit existing CAPTAIN

### 4. `install.sh` extension — deploy LIEUTENANT skills

Add SKILL_NAMES array (parallel to TEMPLATE_NAMES + CAPTAIN_NAMES) listing the skills to deploy. Add a deployment step in install.sh that creates `<DEST>/.claude/skills/<name>/` and copies `SKILL.md` (and any other files in the skill directory). Per A1 lock-in: always deploy, no opt-out flag.

### 5. `install.sh` fix — stoa--w1t staleness detection

Add a step at the end of install.sh (after deployments) that checks the destination for files no longer in the source (obsolete deploys). Per A3 lock-in: warn by default; `--prune-obsolete` flag for removal. Output should be clear: "Obsolete files detected at destination (not in current substrate): [list]. Run with --prune-obsolete to remove, or rm manually." Close ticket `stoa--w1t` after fix lands.

### 6. Planning v2 spec §4 reframe

Update `user-beadwork/plans/three-role-recursive-architecture.md` §4 from "Every tier has two MAJOR roles" to acknowledge pair-programmer Majors:

- The two universal MAJOR roles per tier are still POLYBIUS + PLINY (structural)
- Plus on-demand pair-programmer Majors authored by POLYBIUS per task (per substrate §11/§12)
- Examples of pair-programmer Majors POLYBIUS has authored across projects (ATTICUS, PYTHAGORAS, CODEX, LEX)
- The "two MAJOR roles" framing is preserved as the *structural* base — pair-programmers are dynamic additions, not a third class with its own structural seat

Commit + push to user-beadwork as a separate commit (different repo than the-stoa).

### 7. Smoke test

After all changes:
- `substrate/install.sh --target user --dry-run` runs cleanly with the new skills deployment + staleness detection steps
- `substrate/install.sh --target user` re-deploys skills to user-tier; verify `~/.claude/skills/agent-author/SKILL.md` lands
- `cd app && npm run build` works (TypeScript clean — Stoa app should be unaffected since LIEUTENANT slot work is deferred to Arc 17.1)
- `cd app && npm test` passes (existing tests; no LIEUTENANT-rendering test added in Arc 17)
- `cd app && npm run dev` starts cleanly; existing roster view unchanged
- `bw close stoa--w1t` with reason citing the staleness fix
- Voice audit: `grep -i "colonel" substrate/` returns only deliberate reserved-future-rank references

### 8. Hand-back via bw

Standard hand-back per Arc 16's pattern — `bw close stoa--<epic-id> --reason "..."` plus a final `bw comment <epic-id> "Arc 17 shipped at <sha>; ..."` summarizing what landed.

---

## Definition of done

- MAJOR_POLYBIUS.md §11 + §12 added (pair-programmer authoring + prototyping methodology)
- `substrate/skills/agent-author/SKILL.md` created
- `install.sh` extended (skills deployment + staleness detection per A1 + A3 lock-ins)
- Planning v2 spec §4 reframed (separate user-beadwork commit)
- `stoa--w1t` closed via the install.sh staleness fix
- bw `stoa--*` epic for Arc 17 closed
- Voice audit clean
- Committed + pushed to `the-stoa` main (autonomous-ship per `u--7yg.11`)

---

## Out of scope

- **The Stoa app LIEUTENANT slot rendering** — explicitly deferred to Arc 17.1 follow-up. Arc 17 ships skills to substrate + deploys them to `~/.claude/skills/`; the Stoa app's display of the LIEUTENANT slot stays as-is (whatever it currently shows). Arc 17.1 will be the small follow-up that reads skills via gen-data adapter + renders the slot.
- **Arc 18 (polling capability + consent)** — drafted after Arc 17 lands
- **Renaming or repurposing existing CAPTAINs** — this arc adds capabilities; doesn't modify existing roster
- **Authoring specific pair-programmer Majors** (ATTICUS, PYTHAGORAS, etc.) as canonical substrate files — Arc 17 ships the *capability* + the skill; specific instances stay project-authored
- **Hypergraph work** — separate future arc per case study §10
- **Modifying historical artifacts** — `substrate/v1-historical/`, archived design tool output, etc.
- **Modifying the case study + KG drafts at `docs/case-study/`** — already updated by user-tier CoS to reflect §6.5 (prototyping methodology); do NOT modify these in Arc 17

---

## Voice discipline

After all changes:

```bash
grep -ri "colonel" substrate/ \
  --exclude-dir=v1-historical \
  --exclude-dir=skills/agent-author/templates \
  | head -20
```

Should return only deliberate reserved-future-rank references (the COLONEL slot in spec §2). Any other matches in new content are regressions.

The new `agent-author` skill specifically: voice-discipline check is *part of the skill's own logic* — the skill verifies its draft outputs use PRINCIPAL/HUMAN voice. This is dogfooding the discipline.

---

## Beadwork

`bw` already initialized (`stoa-` prefix). File a new epic:

```bash
cd ~/claude_projects/the-stoa
bw create "[EPIC] Arc 17 — POLYBIUS authoring capabilities + agent-authoring skill + skills deployment" -t epic -p 1
```

File children for: Phase A surfaces (skills deployment shape, agent-authoring I/O, stoa--w1t scope), §11 pair-programmer authoring, §12 prototyping methodology, agent-author skill, install.sh skills deploy, install.sh staleness fix, planning spec §4 reframe, Stoa LIEUTENANT slot, smoke test. Close as you go.

---

## Discipline

- HITL default (planning v2 §7) — supervising via user-tier CoS
- Principal-as-router (`u--7yg.1`) — surface only project-direction calls (Phase A surfaces; possibly Stoa-update scope if it's non-trivial)
- Verify-then-execute (`u--7yg.10`, `u--7yg.18`)
- One job per agent (`u--7yg.17`) — your one job is Arc 17; resist scope creep into Arc 18 (polling) or hypergraph work
- Wait-for-quiescence (`u--7yg.15`)
- Autonomous-ship on clean PASS (`u--7yg.11`)
- Voice discipline (planning v2 §6)
- **Fix-now (MAJOR_POLYBIUS.md §4.8)** — if you find related defects (e.g., agent-author skill surfaces another empirical-pattern gap), fix-now if small; ticket-with-plan if scope-different
- **bw command syntax (MAJOR_PLINY.md §6.1)** — use positional text for `bw comment`; run `bw prime` at activation; use `--reason` for `bw close`. The Arc 16 lesson stays operational.

**Special concern: don't rebuild what already works.** The skill pattern is well-established (existing skills in agent-gauntlet's `skills/` dir); follow it. The install.sh extension pattern is well-established (TEMPLATE_NAMES + CAPTAIN_NAMES); follow it. Arc 17 is mostly mechanical-after-modeled-on-existing.

---

## Suggested phasing

This is medium-sized; phase your work. Phase A's three decisions are LOCKED pre-dispatch (no surface needed):

- **Phase A: install.sh extensions (~30 min).** SKILL_NAMES array + skills deployment + staleness detection per A1 + A3 lock-ins. Mechanical work.
- **Phase B: Author the agent-authoring skill (~45-60 min).** `substrate/skills/agent-author/SKILL.md` with proper structure, voice-discipline logic. Drafts go direct to substrate per A2.
- **Phase C: Add §11 + §12 to MAJOR_POLYBIUS.md (~45 min).** Pair-programmer authoring procedure + prototyping methodology.
- **Phase D: Planning spec §4 reframe (~15 min).** Separate user-beadwork commit.
- **Phase E: Smoke test + voice audit + ship.** Standard.

No Phase A Colonel-call surfaces expected — decisions are locked. If you hit something genuinely ambiguous mid-phase, surface via bw to POLYBIUS (asymmetric polling — POLYBIUS will pick up within ~5 min).

---

## Operating mode

**Human-in-the-loop** (planning v2 §7). Surface for input at:
- (a) Anything genuinely ambiguous mid-phase (no expected Phase A surfaces — decisions locked)
- (b) Work product ready for review (optional — autonomous push for clean self-validation)
- (c) Done

For Arc 17: the architectural calls are locked up front; the rest is mechanical-after-modeled-on-existing. Expect autonomous execution with bw status comments at phase transitions.

---

## How to surface back

Via bw comments on the Arc 17 epic (POLYBIUS will be polling). Use the verified syntax: `bw comment <id> "text"` (positional, no `-m`). If POLYBIUS isn't responding within ~5-10 min and the surface is blocking, fall back to PRINCIPAL via human relay (rare).

For Arc 17: clean ship hand-back includes the §11 + §12 additions + skills deployed + spec reframe; cite the agent-author skill's first invocation as empirical signal if PRINCIPAL would like to test it during Arc 17 itself (recursive — using the new skill to author something else).

---

## After Arc 17

**Arc 17.1** — small follow-up: gen-data adapter reads the deployed skills from substrate; The Stoa app's LIEUTENANT slot renders skill names + descriptions. Mechanical work, well-defined, parallel to existing rank-slot rendering. Drafted by user-tier CoS once Arc 17 lands.

**Arc 18** — polling capability + consent in MAJOR_POLYBIUS / MAJOR_PLINY + spec §6.2 co-edit. Narrower than originally planned (bw-syntax teaching shipped in 16.1).

After Arc 17.1 + Arc 18: case study + KG spec drafts at `docs/case-study/` get committed + pushed (have been waiting on the substrate-completeness sequence to ship).

The agent-author skill from this arc is itself a meta-tool — if the next session needs to author a new agent (e.g., a hypergraph-tier sub-project's pair-programmer when that arc spawns), the skill is what POLYBIUS reaches for. Arc 17 makes future agent-authoring mechanical rather than artisanal.

Standby, run.
