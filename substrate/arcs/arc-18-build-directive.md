# Arc 18 build directive — async polling capability + consent discipline in substrate

**Audience:** the fresh Claude Code session opened to build Arc 18 deliverables (or this seat, if PRINCIPAL chooses direct execution per Arc 16.1 / 17.1 precedent).
**Authored by:** user-tier Chief-of-Staff (POLYBIUS-equivalent) + the PRINCIPAL (Denson Smith).
**Status:** active directive.
**Builds on:** Arcs 1-17 + Arc 16.1 + Arc 17.1 (the-stoa main `be88fe4`). Arc 18 is the third arc in the substrate-completeness sequence (16/17/18). Originally scoped to include bw-syntax teaching; that shipped early in Arc 16.1, narrowing Arc 18 to polling capability + consent.

**Execution mode: direct from POLYBIUS seat (per PRINCIPAL direction).** Arc 16.1 / 17.1 precedent for substrate fix-now from this seat applies; Arc 18 is similarly mechanical. The build-session-framed comms section + activation steps below are kept as-is for record purposes; the actual work runs in the user-tier CoS-equivalent session.

**Your one job:** add async-polling capability awareness + consent discipline to MAJOR_POLYBIUS.md and MAJOR_PLINY.md; reframe planning v2 spec §6.2 (polling vs human-pinged) to acknowledge polling-as-primary for long-running peer-MAJOR coordination; add a polling-consent prompt to `templates/consent-prompts.md`. Then return cleanly.

This is small + mechanical — comparable to Arc 16.1. Substrate-only; no Stoa app touch; no install.sh changes.

---

## Comms — direct async via bw (proven empirically across Arcs 16, 17)

POLYBIUS sets up its own polling cron at engagement start. PLINY follows the surface-and-wait discipline: poll only when surfacing a question and waiting for the response. (This *is* the discipline Arc 18 codifies in substrate.)

bw command syntax discipline: positional comment text (`bw comment <id> "text"`), no `-m` flag — see MAJOR_PLINY.md §6.1 from Arc 16.1.

---

## Read first

1. **MAJOR_POLYBIUS.md** §7 (Communication) and especially **§7.2 (Polling vs human-pinged)** — the current framing reads polling as fallback; Arc 18 reframes it as primary for long-running peer-MAJOR async
2. **MAJOR_PLINY.md** §6 (Communication) and §6.1 (Working with beadwork — Arc 16.1) — the role file PLINY reads at activation; needs the polling capability awareness
3. **planning v2 spec §6.2 (Polling vs human-pinged)** at `user-beadwork/plans/three-role-recursive-architecture.md` — the architecture doc; small co-edit to keep spec ↔ substrate aligned
4. **`substrate/templates/consent-prompts.md`** — pattern for sensitive-action consent prompts; you'll add a polling-setup prompt
5. **The bw comments on `stoa--kyg` (Arc 16) and `stoa--366` (Arc 17)** — empirical evidence the polling pattern works; cite as load-bearing signal in the substrate teaching

---

## Phase A — Three architectural decisions (LOCKED pre-dispatch by PRINCIPAL)

The build session does NOT need to surface these as Colonel calls — they were settled during the Arc 18 directive review:

### A1. Polling cadence default — LOCKED: `*/5 * * * *` (every 5 min)

Both Arc 16 (`d8fcd07a`) and Arc 17 (`30b61219`) used 5-min cadence. Empirically proven; appropriate balance of responsiveness vs token cost. The substrate teaches `*/5 * * * *` as the default; agents can adjust per-engagement if a longer or shorter cadence is justified.

### A2. Consent shape — LOCKED: explicit consent prompt before scheduling

POLYBIUS asks PRINCIPAL before scheduling any polling cron — names the cadence, what gets checked at each fire, expected engagement duration, and the cron's job-id (for cancel-anytime via `CronDelete`). Even with implicit green-light from PRINCIPAL ("set up polling"), the explicit beat ("I'll schedule X with cadence Y, confirm?") is the discipline. Templated prompt in `templates/consent-prompts.md` so the wording is reusable.

### A3. Where polling capability lives in role files — LOCKED: new subsection in §7 / §6 Communication, NOT in §4 / §7 Disciplines

Polling is a communication mechanism (extends bw's reach across sessions), not a behavioral discipline like one-job-per-agent or fix-now. Lives in the Communication section as §7.4 (POLYBIUS) and §6.2 (PLINY) — parallel placement to the existing Arc 16.1 §6.1 / §7.3 "Working with beadwork — command syntax" subsections. Activation checklists in both role files get a small addition: "set up polling cron with PRINCIPAL consent if engagement is long-running."

---

## Deliverables

### 1. MAJOR_POLYBIUS.md §7.4 — Polling capability + cadence

Add a new §7.4 to `substrate/MAJOR_POLYBIUS.md` after §7.3 (Working with beadwork — command syntax, from Arc 16.1) and before §8 (Voice discipline). Content:

- **The capability:** POLYBIUS can set its own polling cron via `CronCreate` (session-only by default, `durable: false`). When polling is active, POLYBIUS reads bw at the configured cadence and surfaces meaningful state transitions back to PRINCIPAL.
- **The default cadence:** `*/5 * * * *` (every 5 minutes) per A1 lock-in. Adjust per-engagement if a longer cadence is justified (low-frequency arc work) or a shorter cadence (active multi-session coordination).
- **Off-minute guidance:** the bw cron tool already jitters recurring tasks; for one-shot tasks landing on `:00` or `:30`, prefer an off-minute (`:07`, `:13`, etc.) to avoid the fleet-wide alignment cost.
- **Job-id management:** `CronList` lists current jobs; `CronDelete <id>` cancels. Polling crons are session-only; they die when the session exits.
- **The consent moment** (cross-reference §5.3 and the new templates/consent-prompts.md addition): POLYBIUS must request PRINCIPAL approval before scheduling any polling cron. The prompt names: cadence, what gets checked at each fire, expected engagement duration, job-id (for cancel-anytime).
- **Cite empirical signal:** Arc 16 cron `d8fcd07a` and Arc 17 cron `30b61219` first operationalized the pattern; both engagements shipped via async POLYBIUS↔PLINY bw comms with no human relay for routine status.

### 2. MAJOR_PLINY.md §6.2 — Surface-and-wait polling pattern

Add a new §6.2 to `substrate/MAJOR_PLINY.md` after §6.1 (Working with beadwork — command syntax, from Arc 16.1) and before §7 (Disciplines). Content:

- **The trigger:** PLINY does NOT poll during heads-down work (focus on the work; POLYBIUS is polling and will pick up phase-transition comments). PLINY DOES poll when she has surfaced a question to POLYBIUS via bw and is waiting for the response to proceed. The trigger is precise: "I sent a comment with a question; I cannot continue without the response; I am now waiting."
- **Setup procedure when the trigger fires:** `CronCreate` with `cron: "*/5 * * * *"`, `recurring: true`, prompt that re-reads the relevant bw ticket and surfaces any new comments. Cancel via `CronDelete <job-id>` the moment POLYBIUS responds and PLINY resumes work.
- **Anti-pattern:** polling between phases when nothing is blocked. Just write the status comment and continue. Don't burn polling tokens defensively.
- **Cite empirical signal:** Arc 16 + Arc 17 shipped via this pattern. PLINY's heads-down work proceeded without polling overhead; POLYBIUS's polling was the channel that surfaced PLINY's status to PRINCIPAL.

### 3. MAJOR_POLYBIUS.md §9 + MAJOR_PLINY.md §9 — activation checklist updates

Both activation checklists get a small addition (one numbered step):

- **MAJOR_POLYBIUS §9** — after the existing `bw prime` step (§9 step 2 from Arc 16.1): "If this engagement is long-running (multi-session arc work, cross-tier coordination), request PRINCIPAL consent and set up a polling cron per §7.4. Defer for short engagements where human-pinged is sufficient."
- **MAJOR_PLINY §9** — after the existing `bw prime` step: "Polling is surface-and-wait per §6.2. Do not schedule a polling cron at activation; schedule one only when you've surfaced a question to POLYBIUS and are waiting for the response."

### 4. `substrate/templates/consent-prompts.md` — Polling-setup consent prompt

Add a new prompt (probably "Prompt 8" or similar; match existing numbering). Content:

- The standard consent-prompt structure: name the action, state what happens, ask binary, wait for answer
- Specifics for polling: cadence, what gets checked at each fire, expected duration, job-id will be reported, cancel via `CronDelete <job-id>`
- Example PRINCIPAL response handling (yes / no / cadence-adjustment)

### 5. Planning v2 spec §6.2 reframe

Update `user-beadwork/plans/three-role-recursive-architecture.md` §6.2 (Polling vs human-pinged):

- **Old framing:** "Preferred: human-pinged. Polling is the autonomous fallback when the PRINCIPAL isn't in the loop."
- **New framing:** "Two patterns serve different needs: human-pinged is preferred when the PRINCIPAL is actively in the loop (low-overhead, immediate); polling is preferred for long-running peer-MAJOR coordination (POLYBIUS↔PLINY async over multi-hour or multi-session arcs) where the PRINCIPAL is not the bottleneck for routine status. PRINCIPAL consent is required before any polling cron is scheduled (see substrate/MAJOR_POLYBIUS.md §7.4)."
- Cite the empirical signals (Arc 16 cron `d8fcd07a`, Arc 17 cron `30b61219`) as the operational evidence the pattern works.

Commit + push to user-beadwork as a separate commit (different repo than the-stoa).

### 6. Smoke test

After all changes:
- `substrate/install.sh --target user --dry-run` runs cleanly with the templates change
- `substrate/install.sh --target user` re-deploys the role files + templates with the new content
- Verify deployed copies have the new sections: `grep "§7.4" ~/.claude/MAJOR_POLYBIUS.md` and `grep "§6.2" ~/.claude/MAJOR_PLINY.md` should hit the new content
- Verify `templates/consent-prompts.md` deployed: `ls ~/.claude/templates/`
- Voice audit: `grep -i "colonel" substrate/MAJOR_POLYBIUS.md substrate/MAJOR_PLINY.md substrate/templates/` returns only deliberate reserved-future-rank references

### 7. Hand-back via bw (if dispatched as build session)

Standard hand-back per Arc 16/17 pattern — `bw close stoa--<epic-id> --reason "..."` plus a final `bw comment <epic-id> "Arc 18 shipped at <sha>; ..."` summarizing what landed.

---

## Definition of done

- MAJOR_POLYBIUS.md §7.4 + §9 activation checklist update
- MAJOR_PLINY.md §6.2 + §9 activation checklist update
- `substrate/templates/consent-prompts.md` polling-consent prompt added
- Planning v2 spec §6.2 reframed (separate user-beadwork commit)
- Smoke test passes (install.sh dry-run + apply; voice audit clean)
- bw `stoa--*` epic for Arc 18 closed
- Committed + pushed to `the-stoa` main (autonomous-ship per `u--7yg.11`)

---

## Out of scope

- **Stoa app changes** — Arc 18 is substrate-only; no display work
- **install.sh changes** — Arc 17 already extended install.sh for skills + staleness; Arc 18 doesn't touch it
- **Authoring or modifying skills** — that's substrate-skill-authoring work, not polling discipline
- **Modifying historical artifacts** — `substrate/v1-historical/`, archived design tool output, etc.
- **Modifying the case study + KG drafts at `docs/case-study/`** — already-current; do NOT modify in Arc 18 (they reference Arc 18's framing already from earlier user-tier CoS work)
- **Adding new disciplines beyond polling/consent** — resist scope creep; if other empirical signals surface, file as `u--7yg.*` children for a future arc

---

## Voice discipline

`grep -i "colonel" substrate/` after work — only deliberate reserved-future-rank references. New prose grounded in PRINCIPAL/HUMAN per spec §6.

The polling-consent prompt specifically: PRINCIPAL is the actor giving consent (or not). The prompt is addressed TO PRINCIPAL by POLYBIUS; voice is POLYBIUS-narrating-its-own-action ("I'll set up X with cadence Y; confirm?").

---

## Beadwork

`bw` initialized (`stoa-` prefix). File a new epic:

```bash
cd ~/claude_projects/the-stoa
bw create "[EPIC] Arc 18 — async polling capability + consent discipline" -t epic -p 1
```

File children for: §7.4 POLYBIUS polling capability, §6.2 PLINY surface-and-wait pattern, activation checklist updates, consent-prompts.md addition, planning spec §6.2 reframe (separate user-beadwork commit), smoke test. Close as you go.

---

## Discipline

- HITL default; surfaces minimal expected (Phase A locked)
- Verify-then-execute (`u--7yg.10`, `u--7yg.18`)
- One job per agent (`u--7yg.17`) — your one job is Arc 18; resist scope creep
- Wait-for-quiescence (`u--7yg.15`)
- Autonomous-ship on clean PASS (`u--7yg.11`)
- Voice discipline (planning v2 §6)
- bw command syntax (`u--7yg.23` / MAJOR_PLINY.md §6.1) — positional comment text; run `bw prime` at activation
- **Dogfood the polling discipline**: if dispatched as a build session, the polling pattern itself is the comm channel for Arc 18 — operational test of the discipline being codified

---

## Suggested phasing

Mechanical-after-modeled-on-existing; phase your work:

- **Phase A: MAJOR_POLYBIUS.md §7.4 + §9 update.** ~30 min doc work.
- **Phase B: MAJOR_PLINY.md §6.2 + §9 update.** ~30 min doc work, parallel to Phase A in structure.
- **Phase C: templates/consent-prompts.md polling prompt.** ~15 min.
- **Phase D: planning v2 spec §6.2 reframe.** ~15 min, separate user-beadwork commit.
- **Phase E: Smoke test + voice audit + ship.** Standard.

If executed from POLYBIUS seat per Arc 16.1 / 17.1 precedent, all five phases run sequentially in this seat — no build-session dispatch needed. If dispatched as build session, Phases A-E run heads-down with bw status comments at transitions.

---

## Operating mode

**Human-in-the-loop**. Surface for input only on:
- (a) Anything genuinely ambiguous mid-phase (no expected Phase A surfaces — decisions locked)
- (b) Work product ready for review (optional)
- (c) Done

For Arc 18: the architectural calls are locked up front; the rest is mechanical-after-modeled-on-Arc-16.1.

---

## After Arc 18

The substrate-completeness sequence (16, 16.1, 17, 17.1, 18) is complete. After Arc 18:

- **Case study + KG spec drafts** at `the-stoa/docs/case-study/` get committed + pushed (have been waiting on the substrate-completeness sequence to ship)
- **Hypergraph work** becomes the next architectural arc — explicitly forward-flagged in the case study as the next major direction
- **POLYBIUS-driven Chrome MCP tour** of The Stoa app — the demo / explanatory content delivery mode

Standby, run.
