# Arc 57 build directive — stoa--3c9: orchestration tool-selection discipline (WHEN to recommend)

**Ticket:** `stoa--3c9` (P2, [DESIGN]) — bucket A (substrate-canon, PRINCIPAL-gated)
**Driver:** PLINY_the-stoa
**Drive mode:** **HITL / PRINCIPAL-gated** — surface the DESIGN at the HARD STOP (post-ARGUS) to POLYBIUS_the-stoa floor-manager → user-tier for greenlight BEFORE build. Do NOT autonomous-ship; ship-gate stays with user-tier.
**Worktree:** `.claude/worktrees/arc-57-build` (branch `arc-57/build`)
**Gauntlet:** DAEDALUS → ARGUS → **[HARD STOP]** → ADA → VERA → CATO → NOMOS → ZENO

## The insight (PRINCIPAL direction 2026-06-01)

Workflows JOIN the team's repertoire (subagents / skills / agent-teams / workflow / full gauntlet / Mode-2 pairing). The NEW capability is **routing judgment across the whole repertoire** — POLYBIUS becomes a **tool-SELECTOR** (route HOW work is structured), the operational sibling to its existing role as router (route WHO does it) and to "where is human attention required." The four primitives are a control-vs-flexibility spectrum of ONE idea, not rivals.

This ticket decomposes into three parts; **only parts 2 + 3 are in THIS arc** (part 1 already shipped):
- **Part 1 — HOW TO MAKE** → the `workflow-composer` skill. ALREADY SHIPPED (`stoa--04n` closed; forge-promoted Arc 53). OUT of scope here.
- **Part 2 — WHEN TO RECOMMEND** (THE REAL GAP, the core of this arc) → a **tool-selection / routing discipline** promoted to canon.
- **Part 3 — HOW TO SET UP + RUN** → operational know-how (belongs in the composer skill).

## Primary input (promote this, don't re-derive)

`docs/sessions/2026-05-30-stoa-workflows-integration-strategy.md` — the strategy doc. Its **§2 "When to use what"** calibration table (cost-grounded) and **§3 task-type taxonomy** (the 8-row coding+non-coding task-shape→tool table) ARE the part-2 routing logic. The arc's job is to PROMOTE these from N=1 session-proposal to routing canon — adapted to canonical form, not copy-pasted.

**Honesty constraint (load-bearing):** the strategy doc is explicitly N=1, "not ratified canon — accrete per `operating-disciplines.md` §6.7.1." Promoting to canon is a PRINCIPAL-direction act (this ticket). DAEDALUS MUST be honest in the design about what is N=1-proven (the 3 prototype runs) vs aspirational, and must NOT overclaim cost numbers as settled. The §6.7.1 accretion framing should be preserved in the canon text (this is routing GUIDANCE the team calibrates, not a rigid decision-tree — cf. MAJOR_POLYBIUS.md:568 "names the framing, not a decision tree").

## Part 2 — the design's central open question (DAEDALUS resolves; HARD STOP ratifies)

**WHERE does the routing discipline live?** This is the ticket's named OPEN question. Candidates:
- A new `operating-disciplines.md` § (universal-team layer — the taxonomy is team-knowledge any seat routing work could consult).
- A new `MAJOR_POLYBIUS.md` § (POLYBIUS is the tool-selector seat; it already owns "the routing call" framing at MAJOR_POLYBIUS.md:566-568).
- A split (taxonomy/calibration as universal op-disc knowledge + a POLYBIUS pointer that names POLYBIUS as the seat that applies it).

DAEDALUS: pick one, justify it against the slim-core / module / composition-layer architecture (a long taxonomy table may belong as a module the routing-map points at, NOT inline — weigh this). Consider the §3.5 composition-layer rules (indexes stay inline; CONDITIONAL content relocates to modules). Propose the concrete home + the canonical form (full tables? distilled? a module?).

## Part 3 — operational know-how (in the composer skill)

The HOW-TO-SET-UP-+-RUN operational details belong in `substrate/skills/workflow-composer/SKILL.md` (or confirm they're already there): pre-allowlist commands (the `stoa--x4j` stall-fix — verify it's canonized), args for reuse, "cost: run a small slice first," save-for-reuse locations (`.claude/workflows` forge vs `~/.claude/workflows` user-tier), overnight = remote-routine-NOT-workflow. DAEDALUS: audit what the composer skill ALREADY covers vs what part-3 needs added; add only the gap. Do not duplicate content already in the skill.

## Folded nit (c1 — re-homed from stoa--g38 by POLYBIUS_the-stoa)

While touching the composer skill: `substrate/skills/workflow-composer/SKILL.md:170` (item 8) cites a bare `(§18.2)`. Fix to a file-qualified cite `(MAJOR_POLYBIUS.md §18.2)` to match the L192-196 cross-refs style. Target resolves to MAJOR_POLYBIUS.md:513. NIT-level; rides this arc's skill-content touch (arc-gated per §18.2 — cannot be a direct-commit drive-by).

## Hard constraints / scope
- Substrate-canon edit → full gauntlet, PRINCIPAL-gated. The HARD STOP is MANDATORY (do NOT skip — bucket A).
- IN: the new routing-discipline canon (home TBD by design), `substrate/skills/workflow-composer/SKILL.md` (part 3 + c1), any pointer/routing-map rows the new home requires, and (if DAEDALUS picks a module home) a new `substrate/modules/<name>.md` + its install.sh deploy wiring + the MAJOR_POLYBIUS routing-map/relocation-index rows.
- OUT: re-opening the composer skill's core (part 1, shipped); building any workflow; the yfv/h2z/0hl work (separate arcs). Do NOT promote N=1 cost numbers as hard guarantees.
- Voice discipline: PRINCIPAL/HUMAN, no COLONEL-for-human, no second-person framing (substrate v2 voice).
- Authorship: any author-like field stays Denson Smith.

## Probes (VERA — refine)
- P1 (home coherence): the chosen canon home resolves — all §-cross-refs valid, routing-map/relocation-index rows added if a module, `npm run gen-data` still valid if frontmatter touched.
- P2 (taxonomy fidelity): the promoted taxonomy preserves the 8 task-shapes + the anti-workflow (row 4) + the discipline-enforcement cross-cut (row 8) + the "where human attention goes" column (the load-bearing one).
- P3 (N=1 honesty): the canon text preserves the §6.7.1-accretion framing and does not overclaim.
- P4 (c1 + part-3): SKILL.md:170 cite fixed; part-3 operational gap added without duplicating existing skill content.
- P5 (deploy): if a module is added, install.sh deploys it (smoke against a synthetic target); subproject MODULE-INLINE markers handled if applicable.

## Per-CAPTAIN seat-identity
`seat-identity: CAPTAIN_<MNEMONIC>_the-stoa <captain-<mnemonic>@the-stoa.local>` per §28.
