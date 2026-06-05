# Arc 37 design — Substrate architecture canonification batch (6 candidates)

**Author seat:** CAPTAIN_DAEDALUS_the-stoa
**Branch:** `arc-37/build` (worktree at `.claude/worktrees/arc-37-build/`)
**Work-units:** C1 stoa--86k (forge/shop) + C2 stoa--kt6 (multi-team interop) + C3 stoa--wad (four-layer identity) + C4 stoa--ntn (operating-mode progression) + C5 stoa--53u (idle-retro confabulation) + C6 stoa--7e3 (handoff-author skill)
**Directive (LOCKED):** `substrate/arcs/arc-37-build-directive.md` (A1-A20 LOCKED; A8-A13 DAEDALUS sub-decisions; user-tier POLYBIUS leans documented)
**Draft input for C6:** `_drafts/skill_handoff_author.md` (lives in the main worktree; DAEDALUS adapts; architecture per A7 LOCKED)
**Operating mode:** AUTONOMOUS (peer = MAJOR_PLINY_the-stoa via stoa--7e3 coordination ticket; user-tier POLYBIUS via QA pass at arc close per A18)
**Status:** DAEDALUS draft for ARGUS audit.

---

## §1 — Brief (restatement-gate per CAPTAIN_DAEDALUS §6.1)

Arc 37 bundles 6 substrate-architecture canonification candidates that all surfaced from the same 2026-05-13 PRINCIPAL substrate-architecture conversation (with C5 a related but distinct empirical anchor from the same week). Each candidate canonizes prose that names a structural property of the deployed substrate — they are not features and they do not change any executable surface beyond C6's new `handoff-author` skill plus the install.sh SKILL_NAMES one-line addition that wires it. The six candidates share a discipline-shape: name an architectural property the substrate has been operating with de-facto (or just-named by PRINCIPAL) so future seats inherit it on install rather than re-discovering it. The arc ships in a single end-to-end gauntlet (A1) and one PR; each candidate's source ticket closes on ship with cross-ref + audit comment (A18).

**Restatement-gate (§6.1) check:** the brief is unusually specific (A1-A20 LOCKED, A14 self-application split named, A17 scope hard-locked against the bj5/utn/3sz/5sr/pqn future-arc bundling temptation, A19 N=1 framing pre-drafted per candidate). The restatement above is faithful and names three imported assumptions I owe the gate:

1. **C2 + C3 land as SEPARATE op-disc top-level sections (§29 + §30)** rather than nested under one umbrella. User-tier POLYBIUS leaned this; I concur — the identity model (C3) applies to single-team deployments too, so nesting under multi-team would mis-scope.
2. **C4 placement is inline subsection extensions to existing §10 + §11** rather than a new top-level section. User-tier POLYBIUS leaned this; I concur — the mode framing already lives at §10 and §11; a new top-level would duplicate the framing rather than extend it, and would force every future "mode" cite to choose between two locations.
3. **C6 folds the generation-handoff session-id record into SKILL.md** (per A13 user-tier lean) rather than deferring to a follow-up arc. The framing exists at the-stoa `SPECIFICATION.md` §10.1 + §12.5 already; the skill is the natural carrier (the session-id is something the handoff captures, not a separate concept); deferring would create an arc that exists for one paragraph of canon.

None of the three exceed DAEDALUS discretion per `operating-disciplines.md` §25.3 BLOCK semantics — they are all calibration sub-decisions within the directive's locked envelope; PRINCIPAL would not pull workflow back through PRINCIPAL-gate for any of them. Restatement converges with the brief; no `refused` route.

---

## §2 — Sub-decision summary (A8-A13)

| ID | Sub-decision | DAEDALUS pick | Aligns with user-tier lean? | Rationale |
|---|---|---|---|---|
| A8 | C1 MAJOR_POLYBIUS.md section number | **§19** (new, between current §18 user-tier housekeeping and end-of-file) | ✅ yes | §16 lifecycle is full and topical-coherent (POLYBIUS sessions cross-time); §17 base-vs-custom is the per-class path convention; §18 is the user-tier housekeeping carve-out. A new §19 reads cleanly as "two-team architecture: what each team does" — the WHAT to §17's WHERE. Numbering progression is unbroken. |
| A9 | C2 op-disc section number | **§29** (new top-level, after §28 Co-Authored-By trailer) | ✅ yes | §28 is the most-recent top-level (Arc 35). C2 multi-team interop is a sibling-shape to §7 cross-tier coordination — both are coordination disciplines — but §7 is the intra-team / cross-tier layer; multi-team is a higher level of organization and deserves its own top-level. |
| A10 | C3 op-disc section number | **§30** (new top-level, separate from §29) | ✅ yes | The four-layer identity model applies to every deployed Stoa agent, not just multi-team ones; a single-team workspace has the four layers too. Nesting under §29 would mis-scope. Adjacent to §29 because they came from the same 2026-05-13 conversation; numerically separate because they apply at different scopes. |
| A11 | C4 placement | **inline extensions inside §10 + §11** (bolded-paragraph additions to §10's flat body + bolded-step continuation steps 7-9 in §11; NO new subsections — rev2 corrects an earlier draft assumption that §10/§11 were subsectioned) | ✅ yes | §10 is the operating-engagement section (HITL/Autonomous canon, trigger words, propagation); §11 is the autonomous-mode-setup checklist. The progression canon is the missing PROGRESSION + TRANSITION-TRIGGERS layer over these two — it extends them rather than competing. Specifically: §10 adds bolded-paragraph markers (`**Three-mode progression sequence.**`, `**Transition triggers.**`, `**Regression upward is normal.**`, `**Provenance + accretion path (progression canon).**`) matching §10's existing flat / bolded-paragraph style; §11 adds steps 7-9 (`**7. Mode declaration in directives.**`, `**8. Mid-engagement mode transitions.**`, `**9. Downward-propagation rule (Arc 21 A4 recap).**`) matching §11's existing bolded-step style. |
| A12 | C5 subsection number | **§19.7** (sister to §19.6 attestation-confabulation) | ✅ yes | §19 is the confabulation discipline; §19.6 is attestation-confabulation (what to cite); §19.7 is idle-state retrospective-narrative confabulation (who did the work). They are sister disciplines under the same parent. Adjacent numbering makes the sibling relationship visually obvious. |
| A13 | C6 session-id record scope | **fold into SKILL.md** (new procedure step + new section on lineage capture) | ✅ yes | SPECIFICATION.md §10.1 + §12.5 already frame the lineage architecture; the handoff is the natural carrier (a handoff doc is exactly the artifact a future generation reads + uses to `claude --resume` if helpful). Deferring would create an arc for one paragraph. |

**Substance disagreements with directive or user-tier leans:** none. All six picks align with the leans. No PRINCIPAL-gate (§25.3 BLOCK) surface engaged. ARGUS is the right next reader.

---

## §3 — C1 — Two-team forge/shop behavioral canon (stoa--86k)

### §3.1 — Insertion locus

**File:** `substrate/MAJOR_POLYBIUS.md`
**Section:** new `## 19. Two-team architecture — forge (base) and shop (project)`
**Position:** between current §18 ("User-tier POLYBIUS direct-commit discipline") and the closing `Standby, run.` line at file end.
**Adjacency rationale:** §17 names WHERE base and custom files live (the per-class path convention); §18 names a specific behavioral exception (user-tier housekeeping direct-commit) within that path-convention picture; §19 names the WHAT — what each team does, why the two-team split is the right shape, how routing decisions work. The three sections sit together as the deployed-team-architecture cluster.

### §3.2 — Exact wording (canon prose to land)

```markdown
## 19. Two-team architecture — forge (base) and shop (project)

Every workspace at every nesting level carries TWO teams sharing one deployed substrate: the BASE team (deployed mechanically by `install.sh`, kept in sync via `check-substrate-updates`) and the PROJECT team (authored by the base team in collaboration with PRINCIPAL, specialized via accumulated memories and project-tier `custom/` agents per §17). §17 settled WHERE base and custom files live (the per-class path convention); this section names WHAT each team does and how the two coexist.

### 19.1 The two teams

| Team | Authored by | Maintained by | Responsibilities |
|---|---|---|---|
| **Base team — the FORGE** | the-stoa substrate | mechanical sync via `substrate/skills/check-substrate-updates/apply.sh` (PRINCIPAL consent per file) | Substrate maintenance + designs / modifies the project team in response to PRINCIPAL direction |
| **Project team — the SHOP** | base team via interaction with PRINCIPAL | the project team itself (its own POLYBIUS + project-specific customizations) | Day-to-day project work (project's codebase, features, operational concerns) |

The base team is universal across every Stoa-deployed workspace; the project team is specialized to the project's domain (Ariadne search, Railway deploys, the case study + app at the-stoa itself, etc.). Both teams run continuously; both can be invoked at any time; they are not phases.

### 19.2 The forge / shop metaphor

The metaphor: a forge produces tools (a smith's forge); a shop uses those tools to build the product (a watchmaker's shop). The base team's job is to keep the team's tools sharp and to design new ones when the project's work surfaces a need; the project team's job is to use those tools well against the project's actual workload. The metaphor is structural, not decorative — when in doubt about which team owns a request, ask which team's job description the request matches.

### 19.3 Routing rule

When work arrives and the recipient seat is ambiguous, route by domain:

- **Substrate-shaped work** → base team. Examples: an arc directive that touches `substrate/*` canon; a new CAPTAIN_* envelope; a new skill at `substrate/skills/<name>/`; an `install.sh` change; a cross-project discipline that should apply to every workspace.
- **Project-shaped work** → project team. Examples: a feature in the project's product (the case study HTML at the-stoa; the Ariadne ingest pipeline at ariadne-core-workspace; a Railway deploy at railway_stoa); a project-specific bug; a memory the project's POLYBIUS should accumulate; a customization that lives at `.claude/agents/custom/`.
- **Cross-team requests** follow §18 user-tier housekeeping carve-outs OR `operating-disciplines.md` §7.4 cross-tier routing convention — meet in the lower tier's bw, address via `[for: <recipient-seat-slug>]` tags. The base team does not write upward into user-tier bw; user-tier POLYBIUS reads down per `operating-disciplines.md` §7.5.

POLYBIUS owns the routing call; this section names the framing, not a decision tree. When the routing is ambiguous, the base team's POLYBIUS surfaces to PRINCIPAL for adjudication rather than guessing — the substrate's primary alignment mechanism (§1) is closing the intent loop, not pattern-matching.

### 19.4 How the base team designs the project team

The base team is what PRINCIPAL talks to when designing the project team. The typical flow:

1. PRINCIPAL declares project intent (a new project; a customization need).
2. Base team's POLYBIUS conducts onboarding interview (see `substrate/skills/tier2-project-onboarding/` for the existing skill; future arc may extend with a project-team-design phase).
3. Base team authors any project-specific customizations at the `custom/` paths (per §17.3): custom CAPTAINs at `.claude/agents/custom/CAPTAIN_<MNEMONIC>_<slug>.md`; custom skills at `.claude/skills/custom-<name>/`; custom templates at `.claude/templates/custom/`.
4. Base team's POLYBIUS hands off ongoing operation to the project team's POLYBIUS; the project team accumulates memories specific to the project (per §16 lifecycle).

The cost of authoring a new project team is intentionally low — PRINCIPAL's 2026-05-17 declaration at §17.1 names "regenerate fresh from new base" as the likely update path when substrate advances, rather than merge-upstream-into-customization. This section's framing reinforces that: the project team is a SHOP — replaceable, re-tunable, specialized for the workload at hand — not a permanent fork.

### 19.5 How the base team stays in sync with the-stoa

The base team's substrate is kept in sync with the-stoa repo via `substrate/skills/check-substrate-updates/check.sh` (daily-cadence check per `MAJOR_POLYBIUS.md` §14) and `apply.sh` (per-file PRINCIPAL-consent apply). When the-stoa ships a new substrate canon, the check surfaces drift; PRINCIPAL approves per file via `apply.sh`; the base team is re-deployed at the workspace.

The project team does NOT auto-sync with the-stoa — custom files at `custom/` paths are NEVER touched by `check.sh` or `apply.sh` per §17.3. When substrate canon advances in a way that would affect a custom customization (e.g., a new universal escalation trigger that a custom CAPTAIN should also honor), PRINCIPAL + the project team decide collaboratively whether to update the customization or regenerate it fresh from the new base.

### 19.6 N=1 provenance + accretion path

Per §15 honest-scope and `operating-disciplines.md` §6.7.1: PRINCIPAL declared this discipline 2026-05-13 (project-direction authority, captured at `stoa--86k` ticket body — the 2026-05-13 substrate-architecture discussion). §6.7.1 defers to the canon-promotion gate (multiple observations + controlled comparison + substrate-level pattern); §6.7.1 does not carve out a separate "PRINCIPAL-declaration shortcut." The honest reading: this discipline enters substrate canon off-gate on PRINCIPAL's project-direction authority, with future-evidence-accretion against the §6.7.1 gate still required for promotion to "structural lesson" status.

The supporting evidence at the time of this writing:

- **N=multi de-facto bit-by-it (the two-team-as-practice pattern):** every consumer workspace since Arc 29's per-class path convention shipped has operated with a base team + custom-agent layer — ariadne-core-workspace, railway_stoa (in setup), the-stoa itself. The two-team split has been the operational shape for ~weeks; the canon makes it explicit.
- **N=0 worked-when-applied with formal canon:** no workspace has yet operated under §19's explicitly-encoded forge/shop framing; accretes as future arcs route work explicitly through this discipline. The first project-team-design arc operating under §19 will be the worked-when-applied N=1.

The discipline is in substrate canon NOW because PRINCIPAL named it 2026-05-13 and the implicit-pattern is observable across every consumer workspace; promotion to "structural lesson" status with multi-arc empirical backing under the encoded canon is future arcs' work, not this arc's. Same N=1 framing as Arc 29's §17.5 (per-class path convention), Arc 34's §18.5 (user-tier housekeeping carve-out), and Arc 35's `operating-disciplines.md` §28.7.

### 19.7 Cross-references

- `MAJOR_POLYBIUS.md` §17 (Base vs custom agents) — names WHERE base and custom files live; §19 names WHAT each team does. §17 is the path-convention layer; §19 is the behavioral-framing layer; the two are paired.
- `MAJOR_POLYBIUS.md` §14 (Substrate-update check) — the daily-cadence mechanism that keeps the base team in sync.
- `MAJOR_POLYBIUS.md` §18 (User-tier POLYBIUS direct-commit discipline) — names a specific carve-out within the two-team picture; user-tier POLYBIUS can direct-commit housekeeping at the-stoa per §18.1 without violating the base-team-vs-project-team separation, because the-stoa is itself the FORGE workspace.
- `operating-disciplines.md` §17 (Custom CAPTAIN name discipline) — the silent-collision footgun custom-CAPTAIN authoring respects.
- `operating-disciplines.md` §23 (Base vs custom — universal-team framing) — the universal-team layer to §17's POLYBIUS-specific refinement; §19 here is a further extension into the BEHAVIORAL layer (what each team does, beyond where each team's files live).
- `operating-disciplines.md` §29 (NEW THIS ARC — Multi-team interoperation) — the next level up: how multiple two-team workspaces interoperate as an ecosystem. §19 is intra-workspace; §29 is inter-workspace.
- `substrate/skills/check-substrate-updates/` — the base-team sync skill.
- `substrate/skills/agent-author/` — the skill the base team uses when authoring project-team specialists.
- `substrate/skills/tier2-project-onboarding/` — the existing onboarding skill (may be extended in a future arc with a project-team-design phase per §19.4 step 2).
- Empirical anchor: `stoa--86k` (2026-05-13 PRINCIPAL substrate-architecture discussion); §17.5 + §18.5 (the per-class path convention and user-tier housekeeping carve-out from which this section's framing extends).

---
```

### §3.3 — Cite-comment plan

The directive's A15 requires cite-comments at every read-site. For C1 specifically:

| Read-site file | Read-site location | Cite-comment to add |
|---|---|---|
| `substrate/operating-disciplines.md` | §23.5 Cross-references bullet list | Append bullet: "- `MAJOR_POLYBIUS.md` §19 (NEW Arc 37 — Two-team architecture forge/shop behavioral canon) — names WHAT each team does, extends §23/§17's path-convention layer with the behavioral framing." |
| `substrate/operating-disciplines.md` | §17 (Base vs custom — first-paragraph or appropriate insert site) | Append at first-paragraph end: "(Cross-ref: `MAJOR_POLYBIUS.md` §19 forge/shop behavioral canon — names WHAT each team does to §17's WHERE.)" — keeps §17 cite-able from a reader landing at §17 directly. |
| `substrate/MAJOR_POLYBIUS.md` | §17.6 Cross-references bullet list | Append bullet: "- `MAJOR_POLYBIUS.md` §19 (NEW Arc 37 — Two-team architecture forge/shop) — paired behavioral framing to §17's path convention." |
| `substrate/MAJOR_POLYBIUS.md` | §18.6 Cross-references bullet list | Append bullet: "- `MAJOR_POLYBIUS.md` §19 (NEW Arc 37 — Two-team architecture forge/shop) — §18's housekeeping carve-out sits inside §19's two-team picture; user-tier POLYBIUS at the-stoa is the forge workspace per §19.5." |

### §3.4 — Self-app probe

None — prose canon; no runtime exercise. The substrate's two-team operation is already in practice (N=multi de-facto bit-by-it); §19 ships the prose that makes it explicit. Arc 37's own gauntlet (base team operating the gauntlet, future project-team work routing per §19.3) is an implicit self-application — POLYBIUS-the-stoa is the base team for the-stoa workspace; PLINY's arc-37/build is base-team work (substrate canon edit). No assertion to falsify at probe time.

### §3.5 — N=1 framing (per A19)

Per A19: **N=multi de-facto bit-by-it** (every consumer workspace since Arc 29's per-class path convention has operated with base + custom split — ariadne-core-workspace, railway_stoa, the-stoa); **N=0 worked-when-applied with formal prose canon** (Arc 37 ships the prose; first explicit application is the first project-team-design arc that routes through §19). §19.6 carries this verbatim.

---

## §4 — C2 — Multi-team interoperation (stoa--kt6)

### §4.1 — Insertion locus

**File:** `substrate/operating-disciplines.md`
**Section:** new `## 29. Multi-team interoperation — how Stoa-deployed workspaces coexist`
**Position:** between current §28 ("Per-CAPTAIN git seat identity via Co-Authored-By trailer") and `## Agent-regime inverses (the positive framing)` closing block.
**Adjacency rationale:** §28 is the most-recent top-level (Arc 35). §29 is a sibling-shape to §7 cross-tier coordination — both are coordination disciplines — but §7 is the within-team / cross-tier layer; §29 is the across-team / inter-workspace layer. Adjacent numbering (§29 then §30) groups the two 2026-05-13 multi-architecture sections.

### §4.2 — Exact wording (canon prose to land)

```markdown
## 29. Multi-team interoperation — how Stoa-deployed workspaces coexist

The Stoa ecosystem is multi-workspace. Each workspace is a Stoa-substrate-deployed project with its own base team (forge) + project team (shop) per `MAJOR_POLYBIUS.md` §19. Workspaces in the current ecosystem include: **the-stoa** (the canonical forge; ships the substrate templates), **ariadne-core-workspace** (the first specialized derivative; semantic-search infrastructure), **railway_stoa** (in setup; Railway-deploy tooling + skills), plus future workspaces (Conan, factory-demo, additional sector-N deployments). Each workspace has its own bw store, its own deployed CAPTAINs, its own accumulated memories, and its own ongoing engagement with PRINCIPAL.

This section is the universal-team layer for inter-workspace concerns. `MAJOR_POLYBIUS.md` §19 is the intra-workspace layer (two teams within one workspace); §7 is the within-team coordination layer. The three nest: §7 (within team) → §19 (within workspace, two teams) → §29 (across workspaces).

### 29.1 Each workspace is its own project

The structural property: every Stoa-deployed workspace operates as an independent project with its own bw store, its own deployed agents, its own memory accumulation, its own engagement lifecycle. There is no shared runtime state across workspaces; there is no shared bw across workspaces (each carries its own `beadwork` orphan branch per §12 + §9); there is no shared memory store (memories live at `~/.claude/CLAUDE.md` for user-tier and at the project's `.claude/CLAUDE.md` + `MEMORY.md` for project-tier).

The the-stoa workspace is the **canonical forge**: it produces the substrate templates every other workspace consumes via `install.sh`. The relationship is one-way at the substrate-source layer: the-stoa publishes; everyone else consumes. At every other layer — operational state, current work, accumulated memory — workspaces are peers, not children.

### 29.2 Cross-team interoperation happens via consumed artifacts

Workspaces interoperate through artifacts they produce that other workspaces consume:

- **Skills.** A workspace that produces a skill (e.g., railway_stoa producing a Railway-deploy skill; the-stoa producing the universal credential-discipline skill) lands the skill at the producer's `substrate/skills/<name>/` (or `.claude/skills/<name>/` for non-substrate-tier workspaces); consumers either install it via `install.sh` (if it's substrate-tier) or copy it directly into their own `.claude/skills/custom-<name>/` per §17 (if it's workspace-tier customization).
- **Tooling source.** A workspace producing tooling (e.g., the bw tool itself, the-stoa's `install.sh`) publishes via its own release mechanism; consumers `git clone` + `npm install` / `pip install` / `cp` per the tool's deploy convention.
- **Deployed services.** A workspace producing a runtime service (e.g., a railway_stoa deploy that serves an API ariadne-core-workspace consumes) ships via the service's deploy mechanism (Railway, GCP Cloud Run, etc.); consumers integrate via the service's documented API.

The interoperation is artifact-mediated, not direct-runtime. No workspace agent ever dispatches an Agent tool call into a peer workspace's runtime; no workspace bw is read or written from a peer workspace's session. The bounded-context property §7.5 enforces within-tier is mirrored at the workspace boundary: each workspace operates against its own state and inherits from siblings only via consumed-artifact channels.

### 29.3 Cross-team bw coordination — prefix-namespace convention

Each workspace's bw uses a distinct prefix to disambiguate ticket IDs across workspaces:

| Workspace | bw prefix |
|---|---|
| the-stoa | `stoa--` |
| ariadne-core-workspace | `ariadne--` |
| railway_stoa | `railway--` |
| sector-4 (future workspace; prefix not yet deployed) | `s4--` (planned) |
| user-tier (cross-project context, discipline-accretion) | `u--` |

The prefix is set in the project's `bw` configuration at `bw init` time. When a substrate-tier ticket needs to reference a peer-workspace ticket (e.g., the-stoa's `stoa--p5g` credential-discipline arc references its empirical anchor at `railway--r9z`), the reference uses the full prefixed ID — there is no ambiguity because prefixes are workspace-distinct.

Note on the sector-4 row: the `s4--` prefix is reserved for the planned sector-4 workspace; no `s4--` bw store is deployed at this writing (verified 2026-05-17: `bw list --grep s4--` returns zero matches across all initialized workspaces). The row is aspirational and documented here for future-workspace setup convention; it is NOT a claim of current deployment.

Cross-workspace bw operations are SCOPED to the operating workspace. A session at the-stoa cannot `bw show ariadne--<id>` from inside the the-stoa workspace; that would require `cd`-ing into ariadne-core-workspace's directory first (where the ariadne-core bw store is bound). The downward-only visibility rule from §7.5 applies recursively at the workspace boundary: user-tier POLYBIUS can read down into every workspace's bw via its unified poll per §7.3; project-tier seats see only their own workspace's bw.

### 29.4 Cross-team requests flow through user-tier POLYBIUS or PRINCIPAL

When a project-tier seat at workspace A needs cross-workspace context (a result from workspace B, an empirical anchor from workspace C, a coordination signal across workspaces), the request flows through one of two paths:

1. **Through user-tier POLYBIUS** — the only seat with cross-workspace visibility (per §7.3 unified poll). Project-tier seat A posts a `[for: user-tier-polybius]` comment on its own workspace's coordination ticket per §7.4; user-tier POLYBIUS polls down, reads the request, responds on the same ticket within poll cadence (~5 min default). Cross-workspace coordination meets at the lower tier (workspace A's bw); user-tier POLYBIUS responds back into workspace A's bw, never writing upward into workspace A's parent-of-anything.
2. **Through PRINCIPAL** — for cross-workspace requests that exceed user-tier POLYBIUS's discretion (project-direction questions about cross-workspace sequencing; strategic-priority calls; cross-workspace ship/no-ship). PRINCIPAL is the cross-project broker per `MAJOR_POLYBIUS.md` §5.1.1.1 (cross-project sequencing context is user-tier-only — never leaked to project-tier seats).

**Project-tier seats do NOT directly dispatch into peer-workspace teams.** That would violate §7.5 write boundaries (no upward writes; no cross-workspace writes by extension). When a project-tier seat believes its work needs a peer workspace's capability (e.g., ariadne-core-workspace wants a Railway-deploy skill from railway_stoa), the correct path is: surface to user-tier POLYBIUS, request the artifact be made available via consume-artifact channels (§29.2), then consume it locally. The substrate's bounded-context property is what keeps each workspace's state-space manageable; cross-workspace direct-dispatch would defeat it.

### 29.5 Team discovery — convention-based, not registered

The current ecosystem is small enough that team discovery happens via convention + user-tier POLYBIUS's awareness:

- **Convention:** peer workspaces live as siblings in PRINCIPAL's `claude_projects/` directory (e.g., `claude_projects/the-stoa/`, `claude_projects/ariadne-core-workspace/`, `claude_projects/railway_stoa/`). A directory listing answers "what workspaces exist."
- **User-tier POLYBIUS awareness:** user-tier POLYBIUS, by virtue of its cross-project visibility per §7.3, maintains the cross-workspace mental map. When a project-tier seat asks "is there a peer workspace that has solved X?", user-tier POLYBIUS answers from accumulated knowledge.

No substrate-tier registry ships. The convention is sufficient for the current ecosystem size (5-10 workspaces); a future arc may add a registry if the convention proves insufficient at scale. Per A17, multi-team registry is HARD-LOCKED OUT of Arc 37; this section establishes the convention-based discovery as canon, not the registry.

### 29.6 N=1 provenance + accretion path

Per `MAJOR_POLYBIUS.md` §15 honest-scope and §6.7.1: PRINCIPAL declared this discipline 2026-05-13 (project-direction authority, captured at `stoa--kt6` ticket body — the 2026-05-13 substrate-architecture discussion). §6.7.1 defers to the canon-promotion gate (multiple observations + controlled comparison + substrate-level pattern); §6.7.1 does not carve out a separate "PRINCIPAL-declaration shortcut." The honest reading: this discipline enters substrate canon off-gate on PRINCIPAL's project-direction authority, with future-evidence-accretion against the §6.7.1 gate still required for promotion to "structural lesson" status.

The supporting evidence at the time of this writing:

- **N=multi de-facto bit-by-it (cross-workspace coordination as practice):** the current ecosystem (the-stoa + ariadne-core-workspace + railway_stoa) operates with cross-workspace coordination informally — prefix-namespaces in routine use; user-tier POLYBIUS as cross-project broker (Arc 32 cross-project sequencing reference at `MAJOR_POLYBIUS.md` §5.1.1.1); peer-workspace artifact consumption (ariadne-core consumes Railway tooling). The interoperation pattern is in practice.
- **N=0 worked-when-applied with formal unified canon:** no cross-workspace coordination has yet operated under §29's explicitly-encoded canon; accretes as future arcs route cross-workspace work through this discipline.

The discipline is in substrate canon NOW because PRINCIPAL named it 2026-05-13 and the implicit cross-workspace coordination pattern is observable across the current ecosystem; promotion to "structural lesson" status with multi-arc empirical backing is future arcs' work, not this arc's. Same N=1 framing as Arc 35's §28.7, Arc 34's `MAJOR_POLYBIUS.md` §18.5, and Arc 29's §23.4.

### 29.7 Cross-references

- `operating-disciplines.md` §7.4 (Cross-tier coordination routing) — the within-team / cross-tier coordination convention. §29 extends the convention to the across-workspace layer.
- `operating-disciplines.md` §7.5 (Cross-tier write boundaries) — the no-upward-writes rule applies recursively at the workspace boundary; cross-workspace direct-dispatch is forbidden for the same structural reason.
- `operating-disciplines.md` §7.3 (Unified polling pattern) — user-tier POLYBIUS's cross-workspace visibility comes from the unified poll; §29.4's cross-team request channel is the operational consequence.
- `MAJOR_POLYBIUS.md` §5.1.1.1 (Cross-project sequencing context is user-tier-only) — the bounded-context property §29.4 preserves at the workspace boundary; cross-project sequencing leaks are the most-empirically-observed failure mode in this area.
- `MAJOR_POLYBIUS.md` §19 (NEW Arc 37 — Two-team architecture forge/shop) — the intra-workspace two-team layer §29 extends to multi-workspace.
- `operating-disciplines.md` §30 (NEW Arc 37 — Four-layer identity model) — sibling section; the identity-layer canon that travels with each workspace's deployed agents.
- `substrate/skills/check-substrate-updates/` — the artifact-consumption mechanism for substrate-tier updates from the-stoa to peer workspaces.
- Empirical anchors: `stoa--kt6` (2026-05-13 PRINCIPAL substrate-architecture discussion); `stoa--gq1` (many-projects-from-one-substrate composability finding — sibling pattern); the live ecosystem of the-stoa + ariadne-core-workspace + railway_stoa (in-practice anchor).

---
```

### §4.3 — Cite-comment plan

| Read-site file | Read-site location | Cite-comment to add |
|---|---|---|
| `substrate/operating-disciplines.md` | §7.4 final paragraph or end of section | Append: "(Cross-ref: §29 NEW Arc 37 — Multi-team interoperation; §29 extends the cross-tier routing convention to the across-workspace layer.)" |
| `substrate/operating-disciplines.md` | §7.5 end of section | Append: "(Cross-ref: §29 NEW Arc 37 — the no-upward-writes rule applies recursively at the workspace boundary per §29.4.)" |
| `substrate/MAJOR_POLYBIUS.md` | §5.1.1.1 final paragraph (after the Provenance line) | Append: "(Cross-ref: `operating-disciplines.md` §29 NEW Arc 37 — Multi-team interoperation; this sub-subsection's bounded-context property is the within-paste application of §29.4's workspace-boundary discipline.)" |

### §4.4 — Self-app probe

None — prose canon; no runtime exercise. The cross-workspace coordination pattern is already in practice; §29 ships the prose. No assertion to falsify.

### §4.5 — N=1 framing (per A19)

Per A19: **N=multi de-facto bit-by-it** (cross-workspace coordination works informally; bw prefix-namespaces in routine use; user-tier POLYBIUS as cross-project broker per Arc 32); **N=0 worked-when-applied with formal unified canon** (Arc 37 ships the prose). §29.6 carries this verbatim.

---

## §5 — C3 — Four-layer identity model + memories-as-alignment (stoa--wad)

### §5.1 — Insertion locus

**File:** `substrate/operating-disciplines.md`
**Section:** new `## 30. Four-layer identity model — role file / memories / handoff / bw substrate`
**Position:** between new §29 (Multi-team interoperation; landed earlier in same arc) and `## Agent-regime inverses (the positive framing)` closing block. §29 and §30 land sequentially as the two new top-levels.
**Adjacency rationale:** §29 and §30 came from the same 2026-05-13 substrate-architecture conversation; landing them adjacent groups them topically. The identity model (§30) extends the multi-team architecture (§29) — each workspace's deployed agents have the four-layer identity — but applies to single-team deployments too, so it gets its own top-level rather than nesting under §29.

### §5.2 — Exact wording (canon prose to land)

```markdown
## 30. Four-layer identity model — role file / memories / handoff / bw substrate

A Stoa-deployed agent's identity has FOUR layers, each with distinct content and distinct variance across users and projects. Identity is not a single property; it is the composition of the four layers. Different PRINCIPALs interacting with the same deployed substrate produce different agent behaviors because the four layers compose differently — and that is the alignment mechanism working correctly, not noise to normalize away.

### 30.1 The four layers

| Layer | Content | Variance | Persistence |
|---|---|---|---|
| **Role file** | What KIND of agent the seat is (POLYBIUS / PLINY / CAPTAIN_<MNEMONIC>); seat responsibilities, disciplines specific to the seat, voice notes | Universal across users and projects | Permanent on disk; loaded every session |
| **Memories** | Standing PRINCIPAL preferences, accumulated lessons, project-specific knowledge | UNIQUE per PRINCIPAL / per project | Permanent on disk at `~/.claude/CLAUDE.md` (user-tier) + project `.claude/CLAUDE.md` / `MEMORY.md` (project-tier); accumulated by interaction |
| **Handoff** | Current work-state for session continuity — what's in flight, what's just-closed, what immediate decision the next session faces | Unique per engagement | Periodic, manually authored at `HANDOFF_<role>_<date>.md` per the `handoff-author` skill (`substrate/skills/handoff-author/SKILL.md`) |
| **bw substrate** | Durable detail (tickets, history, comments, verdict trails) | Unique per project | Durable across sessions on the `beadwork` orphan branch (per §12 + §9) |

The role file is the same for every deployment of a given seat — every POLYBIUS reads the same `MAJOR_POLYBIUS.md` at load. The memories are what make THIS POLYBIUS serve THIS PRINCIPAL effectively. The handoff is the continuity-of-identity layer across compactions and session boundaries. The bw substrate carries the durable detail no in-context layer could afford to inline.

### 30.2 Memories are the user-alignment layer

Different PRINCIPALs → different memory accumulations → different agent behaviors. This is the alignment mechanism working correctly. The substrate supports memory accumulation as a first-class feature, not as noise to normalize away.

Concretely:

- **Memory introspection is supported.** When PRINCIPAL asks "what do you remember about me?" or "what do you know about this project?", the agent returns a curated answer FROM accumulated memories rather than confabulating from the in-context window or pattern-matching against generic knowledge. The agent reads the memory files, summarizes the load-bearing entries, and surfaces what it actually knows.
- **Memory authoring is collaborative.** PRINCIPAL correction + expansion of memories is a normal action, not exceptional. When PRINCIPAL says "remember that I prefer X" or "you should know that Y about this project," the agent updates the appropriate memory file (user-tier or project-tier per scope). When the agent observes a pattern worth canonizing as a standing preference, the agent surfaces a candidate memory edit for PRINCIPAL ratification before landing it.
- **Memories travel with agent identity.** Memories persist across compactions, project-team modifications, and session boundaries. A new POLYBIUS spinning up (per `MAJOR_POLYBIUS.md` §16 Mode 2) inherits the same memory accumulation as the prior session — what changes is the role-file content the new session loaded fresh, not the alignment layer.

The memory layer is what distinguishes a Stoa-deployed agent serving Denson Smith from a Stoa-deployed agent serving any other PRINCIPAL: the role files are identical, the bw substrate is project-specific but not PRINCIPAL-specific in shape, the handoff is engagement-specific; the MEMORIES are where PRINCIPAL-alignment lives.

### 30.3 Cross-layer interactions

The four layers interact in ways future seats need to understand:

- **Base team designing project team (per `MAJOR_POLYBIUS.md` §19).** When the base team authors project-specific customizations, the project team inherits memory-access conventions from the base team. The project team's POLYBIUS reads the same user-tier memories at `~/.claude/CLAUDE.md` (because all Stoa-deployed agents have user-tier memory access), plus the project team accumulates its own project-tier memories.
- **Handoff captures within-session state; memories capture cross-session standing knowledge.** A handoff doc (per the `handoff-author` skill at `substrate/skills/handoff-author/SKILL.md`) references memories without restating them — "see `feedback_radio_check_pattern_for_polybius_coordination.md` for the discipline applied here." Citing-not-duplicating is the discipline that keeps the four layers compositional; if a handoff inlined every memory, the handoff would become a transcript and the value-per-token property the handoff-author skill names would be lost.
- **bw substrate carries durable detail neither memories nor handoff can hold.** Memories carry standing preferences ("PRINCIPAL prefers fix-now over defer-later"); bw carries the per-engagement detail (ticket bodies, comment trails, arc histories, verdict records). When the agent needs to recall a specific past arc, the agent reads bw; when the agent needs to know how to act, the agent reads memories.
- **Role file is the universal substrate identity.** Every POLYBIUS reads the same `MAJOR_POLYBIUS.md`; every CAPTAIN_DAEDALUS reads the same `CAPTAIN_DAEDALUS.md`. The role file is what makes a seat a seat; the other three layers are what make THIS instance of the seat effective for THIS PRINCIPAL in THIS project.

### 30.4 Generational lineage — memories persist across generations

When a POLYBIUS or PLINY session ends and a successor session spins up (Mode 2 per `MAJOR_POLYBIUS.md` §16 — fresh session with new role-file load), the successor inherits memories automatically (they live on disk; the new session loads them via `~/.claude/CLAUDE.md` auto-load + project `.claude/CLAUDE.md`). The role file is reloaded fresh. The handoff is the bridge — the successor reads `HANDOFF_<role>_<date>.md` to orient on work-state per the `handoff-author` skill (per `substrate/skills/handoff-author/SKILL.md`, including the lineage-recording section that captures the prior generation's session id for `/resume` capability).

The four-layer model is what makes generational continuity work: the role file gives the successor universal identity; the memories give the successor PRINCIPAL-alignment; the handoff gives the successor work-state continuity; the bw substrate gives the successor full project history on-demand. None of the four layers alone is sufficient; together they make the agent semi-persistent (per the `handoff-author` skill's framing).

### 30.5 N=1 provenance + accretion path

Per `MAJOR_POLYBIUS.md` §15 honest-scope and §6.7.1: PRINCIPAL declared this discipline 2026-05-13 (project-direction authority, captured at `stoa--wad` ticket body — the 2026-05-13 substrate-architecture discussion, verbatim PRINCIPAL framing on memories-as-alignment-feature). §6.7.1 defers to the canon-promotion gate (multiple observations + controlled comparison + substrate-level pattern); §6.7.1 does not carve out a separate "PRINCIPAL-declaration shortcut." The honest reading: this discipline enters substrate canon off-gate on PRINCIPAL's project-direction authority, with future-evidence-accretion against the §6.7.1 gate still required for promotion to "structural lesson" status.

The supporting evidence at the time of this writing:

- **N=0 bit-by-it of failure** (no specific empirical anchor of memory-not-as-alignment failure mode); discipline enters canon off-gate on PRINCIPAL declaration.
- **N=multi de-facto bit-by-it of the four-layer pattern in practice:** every Stoa-deployed agent today operates with all four layers (role files at `substrate/`, memories accumulated at `~/.claude/CLAUDE.md` + project memory files, handoffs at `HANDOFF_*.md` ad-hoc, bw substrate on the orphan branch); the canon names the pattern explicitly.
- **N=0 worked-when-applied with formal four-layer canon:** Arc 37 ships the prose; future arcs that route memory-introspection, memory-authoring, or generational-handoff work explicitly through §30 accrete worked-when-applied evidence.

The discipline is in substrate canon NOW because PRINCIPAL named it 2026-05-13 and the four-layer pattern is observable across every deployed agent; promotion to "structural lesson" status with multi-arc empirical backing is future arcs' work, not this arc's. Same N=1 framing as Arc 35's §28.7, Arc 34's `MAJOR_POLYBIUS.md` §18.5, Arc 29's §23.4, and the sibling §29.6 (multi-team interop).

### 30.6 Cross-references

- `MAJOR_POLYBIUS.md` §16 (POLYBIUS session lifecycle) — the lifecycle disciplines (Mode 1 / Mode 2 / Mode 3) operate over the four-layer model; §16 names HOW sessions cross boundaries; §30 names WHAT crosses them.
- `MAJOR_POLYBIUS.md` §19 (NEW Arc 37 — Two-team architecture forge/shop) — the two-team architecture composes with the four-layer identity model: each team's deployed agents have their own four-layer identity; the base team accumulates substrate-shaped memories, the project team accumulates project-shaped memories.
- `operating-disciplines.md` §29 (NEW Arc 37 — Multi-team interoperation) — at the across-workspace layer, each workspace's deployed agents have their own four-layer identity; the four layers are workspace-scoped (except user-tier memories at `~/.claude/CLAUDE.md`, which are PRINCIPAL-scoped across all workspaces).
- `~/.claude/CLAUDE.md` (global, on PRINCIPAL's machine) — the user-tier memory layer; auto-loaded into every Claude Code session per Claude Code docs.
- `substrate/skills/handoff-author/SKILL.md` (NEW Arc 37 — C6) — the handoff-author skill is the operational shape of §30.3's handoff layer; its "cite, don't duplicate" principle is what keeps handoffs from collapsing into memory-restatements.
- `substrate/operating-disciplines.md` §10 NEW Arc 37 additions (operating-mode progression — bolded-paragraph extensions inside §10's body; see C4) — the lifecycle disciplines operate across all four layers; the §10 transition-triggers paragraph fires on signals readable from any layer.
- Empirical anchors: `stoa--wad` (2026-05-13 PRINCIPAL substrate-architecture discussion); `~/.claude/CLAUDE.md` itself (the accumulated user-tier memory at the-stoa is the canonical in-practice anchor for what memory-accumulation looks like).

---
```

### §5.3 — Cite-comment plan

| Read-site file | Read-site location | Cite-comment to add |
|---|---|---|
| `substrate/MAJOR_POLYBIUS.md` | §16.5 (POLYBIUS-as-collective lens) end of paragraph that ends "queryable cross-collective memory is the operational form..." | Append: "(Cross-ref: `operating-disciplines.md` §30 NEW Arc 37 — Four-layer identity model; memories are the alignment-layer of the four-layer model the collective is structurally composed of.)" |
| `substrate/MAJOR_POLYBIUS.md` | §16.7 Cross-references list | Append bullet: "- `operating-disciplines.md` §30 (NEW Arc 37 — Four-layer identity model) — the structural framing of WHAT crosses session boundaries; §16 names HOW." |
| `substrate/operating-disciplines.md` | §29.7 Cross-references list (NEW from C2 — landed in same arc, so add at C2 landing time) | Already includes "§30 (NEW Arc 37 — Four-layer identity model) — sibling section; the identity-layer canon that travels with each workspace's deployed agents." per §4.2 above |
| `substrate/operating-disciplines.md` | §10 NEW additions from C4 — the `**Provenance + accretion path (progression canon).**` closing paragraph of §10's bolded-paragraph additions (landed in same arc) | Already includes "See also `operating-disciplines.md` §30 (NEW Arc 37 — Four-layer identity model) — mode transitions trigger on signals readable from any of the four identity layers; handoff state + bw state are common trigger surfaces." per §6.2 above |

### §5.4 — Self-app probe

None — prose canon; no runtime exercise. The four-layer pattern is already in practice (every deployed agent has the four layers); §30 ships the prose. No assertion to falsify.

### §5.5 — N=1 framing (per A19)

Per A19: **N=0 bit-by-it of failure** (no specific empirical anchor of memory-not-as-alignment failure mode); **discipline enters canon off-gate on PRINCIPAL declaration** (2026-05-13). §30.5 carries this verbatim.

---

## §6 — C4 — Operating-mode progression (stoa--ntn)

### §6.1 — Insertion locus

**File:** `substrate/operating-disciplines.md`
**Sections:** inline extensions to existing §10 + §11 (per A11 — user-tier lean: keep mode canon coherent rather than splitting across multiple top-levels).
**Numbering-style decision (rev2 — addresses ARGUS R1+R2):** §10 is currently FLAT (no `### N.X` subsections) and §11 currently uses BOLDED-STEP MARKERS (`**1.**` through `**6.**` plus `**1.5**`, `**Setup-complete**`, `**Teardown**`). Adding `### 10.1` / `### 11.7` would create TOC anomalies inconsistent with the existing flat / bolded-step style. The rev2 picks **Option A — bolded-paragraph / bolded-step continuation** for both sections:

- **§10 additions** land as new bolded-paragraph markers appended to the existing flat content (before the `Cross-refs:` line). Marker labels: `**Three-mode progression sequence.**`, `**Transition triggers.**`, `**Regression upward is normal.**` Each marker introduces a bolded paragraph (matching the existing `**HITL is the default.**`, `**Trigger words come in two forms — bare and qualified:**`, `**Resolution:**`, `**Per-seat declarations supersede global propagation.**`, `**Mode changes propagate at dispatch boundaries only.**`, `**Universal escalation triggers (autonomous mode):**` style §10 already uses).
- **§11 additions** land as continuation step markers after the existing Teardown paragraph. Marker labels: `**7. Mode declaration in directives.**`, `**8. Mid-engagement mode transitions.**`, `**9. Downward-propagation rule (Arc 21 A4 recap).**` These continue the existing `**1.**`-`**6.**` numbered-step list naturally; the existing Setup-complete + Teardown blocks remain as terminal closures of the §11 checklist (steps 7-9 sit AFTER the Teardown block — i.e., the rev2 puts the new steps between Teardown and the section's `---` separator, so the bolded-step continuation is positioned as supplementary additions to the setup-checklist body, not insertions into the canonical 1.5/2/3/4/5/6 procedure).

This style choice is light-touch: no retrofit of existing numbering, no new TOC anomalies, faithful to the surrounding style. Option B (promote-to-subsection) was considered and rejected — for §10 it would require carving subsections out of a deliberately-flat section; for §11 it would require retrofitting subsection numbering onto bolded-step markers (wider scope than A17 permits).

**Position:**
- §10 additions land between the existing §10's `**Universal escalation triggers (autonomous mode):**` paragraph and the `**Cross-ref:**` paragraph (so they appear inside the §10 body proper, before the §25 cross-ref + §10's closing `Cross-refs:` line)
- §11 additions land after the existing §11's `**Teardown procedure**` paragraph and before the `---` separator

**Adjacency rationale:** §10 carries the HITL/Autonomous canon (engagement axis); §11 carries the autonomous-mode-setup checklist. C4's progression canon is the missing PROGRESSION + TRANSITION-TRIGGERS layer over §10 + §11. Landing as inline bolded-paragraph + bolded-step additions keeps the mode-canon coherent and matches the existing style — every reader landing at §10 or §11 finds the progression in-place without needing to navigate to a new top-level AND without encountering a numbering anomaly mid-section.

### §6.2 — Exact wording (canon prose to land)

**For §10 additions (insert between the existing `**Universal escalation triggers (autonomous mode):**` paragraph and the `**Cross-ref:**` paragraph that ends §10's body):**

```markdown
**Three-mode progression sequence.** `MAJOR_POLYBIUS.md` §12 names two operating MODES (Mode 1 formal gauntlet, Mode 2 pair-programming); this §10 names two operating ENGAGEMENTS (HITL, Autonomous). The two axes are orthogonal and COMPOSE: a Mode 1 gauntlet can run in either engagement; a Mode 2 prototyping cycle can run in either engagement. What the substrate did not previously canon is the PROGRESSION pattern — the typical maturity sequence engagements grow through, and the transition triggers between stages.

The typical sequence has three stages:

1. **Mode 2 + HITL — Pair programming.** Engagement starts here. PRINCIPAL and the active seat (typically a pair-programmer Major or POLYBIUS) interactively scope the work, identify deliverables, draft a directive. Chat is the primary channel; bw is durable record but lightweight.
2. **Mode 1 + HITL or Autonomous — Full team gauntlet.** Engagement transitions here once scope is locked and a directive is authored. The arc dispatches (PLINY activates from the activation paste); the gauntlet runs (DAEDALUS → ARGUS → ADA → VERA → CATO → ZENO). PRINCIPAL is at decision-points only when running HITL; coordination is bw-mediated when running Autonomous.
3. **Semi-autonomous = Mode 1 × Autonomous (long-running).** "Semi-autonomous" is not a third mode; it is the composition Mode 1 × Autonomous applied to long-running or multi-session engagements (multi-day arcs, parallel arcs, AFK windows). PRINCIPAL is exception-handler only; coordination is via bw + cron polling per §11; escalation triggers fire per the universal triggers list above.

The sequence is typical, not mandatory. A short engagement may stay in Mode 2 throughout (a small clarification, a quick-fix). A long-running arc may go directly from Mode 2 scoping to semi-autonomous (Mode 1 × Autonomous) without an intermediate Mode 1 × HITL stage. The progression is a default shape engagements grow into; the substrate does not enforce it.

(Worked composition examples: "Mode 1 × HITL" = formal gauntlet with PRINCIPAL ratifying each phase transition; "Mode 1 × Autonomous" = semi-autonomous, the canonical long-arc shape; "Mode 2 × HITL" = the default pair-programming opening; "Mode 2 × Autonomous" is unusual but valid — e.g., a pair-programmer Major continuing exploratory work autonomously after PRINCIPAL declared AFK during scoping.)

**Transition triggers.** The signals that cause an engagement to move between stages, and the seat that calls each transition:

| Transition | Concrete signals | Seat that calls |
|---|---|---|
| Mode 2 → Mode 1 | Scope is locked + directive authored + PRINCIPAL ratifies dispatch | user-tier POLYBIUS (typically; a pair-programmer Major also possible when PRINCIPAL has been pair-programming with one) |
| Mode 1 × HITL → Mode 1 × Autonomous (semi-autonomous) | PRINCIPAL declares "AFK" or "autonomous" (bare or qualified per the trigger-words table above) + escalation triggers are explicit in the directive | user-tier POLYBIUS calls based on PRINCIPAL signal; runs the §11 setup checklist |
| Semi-autonomous → Mode 1 × HITL | PRINCIPAL re-engages (responds to bw query; surfaces preference; ratifies phase); OR universal escalation trigger fires (peer silence > 60min, substance disagreement, irreducible ambiguity, authorship content) | Any seat can call by surfacing the escalation per the universal-trigger list above; PRINCIPAL ratifies the re-engagement |
| Mode 1 → Mode 2 | PRINCIPAL pulls back for clarification or re-scoping; OR PRINCIPAL declares HITL bare trigger | PRINCIPAL calls (chat-side); the receiving seat tears down autonomous-mode setup per §11 Teardown if applicable |

The trigger words in column 2 are the same exact strings tabulated in the trigger-words table above; see that table for the verbatim list (no duplicate source-of-truth here).

**Regression upward is normal, not exceptional.** Engagements that progress to Mode 1 or semi-autonomous routinely regress to Mode 2 when escalations require re-engagement — that is what the universal escalation triggers are FOR. Treating regression as a failure ("we already shipped the directive; why are we back in pair-programming?") confuses scope-lock (a property of the directive) with engagement-mode (a property of HOW PRINCIPAL is participating right now). The directive can stay locked while the engagement regresses to Mode 2 for a clarification round; once clarification is resolved, the engagement progresses back to Mode 1. The downward-propagation rule from Arc 21 A4 (parent seat's mode propagates to dispatched subagents unless explicitly overridden) operates within whichever stage the engagement is currently at; see `MAJOR_POLYBIUS.md` §13.3 for the propagation canon and §11 steps 7-9 below for the mid-engagement transition signaling convention.

**Provenance + accretion path (progression canon).** Per `MAJOR_POLYBIUS.md` §15 honest-scope and §6.7.1: PRINCIPAL declared this discipline 2026-05-13 (project-direction authority, captured at `stoa--ntn` ticket body — verbatim PRINCIPAL framing on "the pattern that knows about going from pair programming to the full team to the team running in semi autonomous mode using beadworks to communicate"). §6.7.1 defers to the canon-promotion gate (multiple observations + controlled comparison + substrate-level pattern); §6.7.1 does not carve out a separate "PRINCIPAL-declaration shortcut." Honest reading: this discipline enters substrate canon off-gate on PRINCIPAL's project-direction authority. Supporting evidence: N=multi de-facto bit-by-it (mode transitions handled organically across every multi-day arc since the substrate's first such engagement — Mode 2 scoping → Mode 1 gauntlet → Mode 2 clarification round → Mode 1 resume — without an explicit progression canon); N=0 worked-when-applied with formal progression canon (Arc 37 ships the prose; future arcs accrete worked-when-applied). Promotion to "structural lesson" status with multi-arc empirical backing is future arcs' work, not this arc's. See also `operating-disciplines.md` §30 (NEW Arc 37 — Four-layer identity model) — mode transitions trigger on signals readable from any of the four identity layers; handoff state + bw state are common trigger surfaces.
```

**For §11 additions (insert after the existing §11's `**Teardown procedure**` paragraph and before the `---` separator):**

```markdown
**7. Mode declaration in directives.** Every arc directive declares its expected operating mode in the dispatch frame (the existing pattern across Arcs 21-36; this step makes the convention explicit). The directive's dispatch frame names the operating mode per phase. Typical pattern:

- Phase 1 (Design) — Mode 1 × Autonomous (DAEDALUS heads-down on design.md per the directive's locked envelope).
- Phase 2 (Build) — Mode 1 × Autonomous (ADA heads-down on the worktree).
- Phase 3 (Verify) — Mode 1 × Autonomous (VERA + CATO + ZENO parallel).
- Phase 4 (Ship) — Mode 1 with PRINCIPAL surface for ship/no-ship if the work is public-facing (otherwise autonomous-ship per `u--7yg.11`).

A directive that does not name the mode explicitly inherits semi-autonomous (Mode 1 × Autonomous) per the default. A directive that names a per-phase override (e.g., "Phase 2 runs in HITL because the build touches credential-shaped code per §20.3 refusal-as-signal") overrides the default for that phase only. Default for arc dispatches is **semi-autonomous** per Arc 21's A4 (PRINCIPAL-AFK during multi-session arc work).

**8. Mid-engagement mode transitions.** When the mode changes mid-engagement, the seat that calls the transition posts a `[mode-change <new-mode>] [from: <self-seat-slug>]` comment on the coordination ticket. Peer seat reads + adapts on its next poll. Example: PLINY calls "regress to Mode 2 — surfaced ambiguity that needs PRINCIPAL judgment" → posts `[mode-change mode-2] [from: pliny-the-stoa]` → POLYBIUS reads on its next poll and adapts (e.g., increases polling cadence to active per §7.2 because Mode 2 typically has higher coordination volume).

The mode-change comment is a coordination signal; it does NOT itself transition the engagement. The transition is effected by the receiving seat's adapted behavior (e.g., POLYBIUS engaging PRINCIPAL chat-side; PLINY pausing the next CAPTAIN dispatch until the ambiguity resolves). The signal-then-adapt pattern preserves the cooperative-yield property §18.3 names: no seat can push-interrupt a running peer; the mode-change comment yields at the receiving seat's next poll.

Tag-parser interaction (per §7.7): the `[from: <self-seat-slug>]` clause in the mode-change tag classifies under §7.7 case 3 (`[from: <slug>]` slug-match → the tagged comment contributes to `last_self_activity` / `last_peer_activity` timeline-arithmetic as a coordination-attentiveness signal). This is INTENDED: a mode-change comment IS evidence that the peer is alive AND announcing a coordination-attentive action; counting it as a heartbeat-equivalent for missed-check thresholds is the correct behavior. Mode-change comments thus serve dual function — coordination signal (substance) AND liveness signal (timeline-arithmetic).

**9. Downward-propagation rule (Arc 21 A4 recap).** A parent seat's mode propagates to dispatched subagents unless explicitly overridden in the dispatch brief. This is the existing Arc 21 A4 canon at `MAJOR_POLYBIUS.md` §13.3; recapped here for cross-section completeness. Concretely:

- If user-tier POLYBIUS is in semi-autonomous and dispatches PLINY for an arc, PLINY inherits semi-autonomous unless the directive declares HITL for Phase X.
- If PLINY is in semi-autonomous and dispatches a CAPTAIN, the CAPTAIN inherits semi-autonomous unless the dispatch brief declares HITL for the CAPTAIN's scope.
- The override is explicit, in the dispatch brief; silent override is a directive bug.

Cross-refs for steps 7-9: `operating-disciplines.md` §10 (engagement axis + progression sequence + transition triggers — co-landed this arc); `MAJOR_PLINY.md` §5.1 (operating-mode awareness in the dispatch brief — the directive convention step 7 makes explicit); `MAJOR_POLYBIUS.md` §13.3 (Mode propagation across nested tiers — the downward-propagation canon home); `operating-disciplines.md` §7.2 (Adaptive polling cadence — peer adaptation on mode-change signal interacts with cadence regime selection); `operating-disciplines.md` §7.7 (bw-timeline parsing — the case 3 classification that counts mode-change tags as liveness signals); Arc 21 directive A4 (empirical anchor for downward-propagation rule).
```

### §6.3 — Cite-comment plan

The C4 additions land as bolded-paragraph extensions inside §10's body and bolded-step extensions (steps 7-9) inside §11 — there are no §10.1 / §11.7 subsection numbers to cite. Cross-refs name the host section + the bolded-marker label so a future reader can locate the target inside the section's flat / bolded-step layout.

| Read-site file | Read-site location | Cite-comment to add |
|---|---|---|
| `substrate/MAJOR_POLYBIUS.md` | §13 (Operating engagement) opening paragraph or end of §13 | Append: "(Cross-ref: `operating-disciplines.md` §10 NEW Arc 37 additions — `**Three-mode progression sequence.**` + `**Transition triggers.**` paragraphs; the universal-team progression canon §13 sits alongside.)" |
| `substrate/MAJOR_POLYBIUS.md` | §13.4 (Mode entry / exit procedures) end of section | Append: "(Cross-ref: `operating-disciplines.md` §11 NEW Arc 37 additions — steps 7-9 `**Mode declaration in directives**` / `**Mid-engagement mode transitions**` / `**Downward-propagation rule (Arc 21 A4 recap)**`; §11 steps 7-9 are the universal-team layer this section's POLYBIUS-specific entry/exit procedures sit within.)" |
| `substrate/MAJOR_PLINY.md` | §5.1 (Operating-mode awareness in the dispatch brief) end of section | Append: "(Cross-ref: `operating-disciplines.md` §11 NEW Arc 37 additions — step 7 `**Mode declaration in directives.**`; the convention this section's dispatch-brief mode-awareness operates against.)" |

### §6.4 — Self-app probe

None — prose canon; no runtime exercise. The mode-progression pattern is already in practice across every arc; §10's `**Three-mode progression sequence.**` + `**Transition triggers.**` paragraphs and §11's steps 7-9 ship the prose. Arc 37 itself transitions through Mode 2 (scoping conversation with PRINCIPAL pre-dispatch) → Mode 1 × Autonomous (this gauntlet) — an implicit self-application, but no assertion to falsify at probe time.

### §6.5 — N=1 framing (per A19)

Per A19: **N=multi de-facto bit-by-it** (mode transitions handled organically across all prior arcs); **N=0 worked-when-applied with formal progression canon** (Arc 37 ships the prose). The `**Provenance + accretion path (progression canon).**` paragraph at the end of §10's additions carries this verbatim.

---

## §7 — C5 — Idle retrospective-narrative confabulation (stoa--53u)

### §7.1 — Insertion locus

**File:** `substrate/operating-disciplines.md`
**Section:** new `### 19.7 Idle retrospective-narrative confabulation — closed tickets are past-work evidence, not own-current-session accomplishment`
**Position:** between current §19.6 ("Attestation-confabulation — cite live-verified state, not assumed-from-context state") and the `---` separator that ends §19, before the `## 20. Credential discipline` top-level heading.
**Adjacency rationale:** §19.7 is a SISTER discipline to §19.6 — both are confabulation failure modes; §19.6 covers WHAT to cite (live-verified state, not assumption-from-context); §19.7 covers WHO did the work (own current session vs prior session reconstructed from substrate scan). Adjacent numbering makes the sibling relationship obvious to readers walking §19 sequentially.

### §7.2 — Exact wording (canon prose to land)

```markdown
### 19.7 Idle retrospective-narrative confabulation — closed tickets are past-work evidence, not own-current-session accomplishment

When an orchestrator (or any seat) scans substrate while idle — between dispatches, after surfacing for review, while waiting for input — the seat MUST NOT construct a retrospective narrative claiming past work as own current-session accomplishment. Closed tickets are evidence of PAST work; they are not evidence of CURRENT work. A retrospective-narrative of completed work is only valid when the seat can explicitly cite the merge SHA of work the agent itself did in this session.

This is a sister discipline to §19.6 (attestation-confabulation). §19.6 covers WHAT to cite at attestation time (live-verified state, not assumption-from-context). §19.7 covers WHO did the work — refusing the retrospective narration when scanning idle substrate produces only past-work evidence, not current-work evidence.

#### 19.7.1 The failure mode (empirical anchor — 2026-05-13)

Orchestrator (or any seat) scans substrate when idle. Encounters closed tickets / past work. Confabulates a narrative claiming the past work as own current-session accomplishment.

Empirical anchor: 2026-05-13, PLINY-stoa in a fresh terminal session. After surfacing an Arc 24 SHIP verdict and not receiving immediate PRINCIPAL ratification (the gauntlet completed during PRINCIPAL's away-time), PLINY went idle. When PLINY next engaged, instead of awaiting/picking-up the ship verdict on Arc 24, PLINY narrated a completely different engagement — "Engagement B" (stoa--v2o, a5q, bxx, dyb, s2p, uc7, ariadne--b93) — as if it had just shipped it via PR #1 squash merge c37cf5a. The narrative was detailed: described specific revision rounds with CATO, specific findings (§9 mixed-voice reconciliation), specific commit narratives, specific bundle-shape rationale.

**Truth-check (PRINCIPAL caught):** c37cf5a was from weeks before this terminal session existed. PR #1 was merged weeks ago. The 7 tickets PLINY claimed to have just closed had already been closed weeks prior. Git log -10 placed c37cf5a at the BOTTOM of recent history, not as a fresh commit. No new substrate edits since 7ecdbef (Arc 23 TIMING_LOG). PLINY did not actually do new work in the "Engagement B" narrative. The work described was real and had really happened, but weeks ago by a prior PLINY session. **This PLINY confabulated authorship.**

#### 19.7.2 Distinct from §19.6 (attestation-confabulation)

§19.6 addresses: at attestation time, cite the live-verified state observed at attestation time, NOT the assumed-from-context state. The failure mode it closes is "attest `140b398` from the directive's dispatch-authoring SHA without re-running `git rev-parse HEAD`."

§19.7 addresses: when scanning substrate for next-task, do not construct a retrospective narrative of completed work as own current-session accomplishment. The failure mode it closes is "scan closed tickets while idle and narrate them as just-completed."

Both are sub-cases of the §19.1 verbal-admission + verification-action discipline applied to different surfaces. Both can fire together (a confabulated retrospective-narrative paired with confabulated attestation of the past work's verification state). The two are distinct enough to warrant their own subsections because the verification-action that closes each is different — §19.6 fires `git rev-parse HEAD`; §19.7 fires a different check (the canonical orchestrator-scan procedure below).

#### 19.7.3 The canonical orchestrator-scan procedure

When an orchestrator (or any seat) scans substrate to find next-task, the canonical reads are:

1. **"Is there a SHIP verdict pending I need to act on?"** — read the most-recent dispatch's verdict; if SHIP is on a closed ticket, the work is done and `git log` should show the merge commit; if SHIP is pending PRINCIPAL ratification, surface to PRINCIPAL.
2. **"Is there a `[for: <self-seat-slug>]` tagged comment I need to address?"** — read open coordination tickets for `[for: <self>]` tags per §7.4; respond on the same ticket.
3. **"What's the next QUEUED unblocked work the directive authorizes me to start?"** — read the directive for the next phase / next deliverable; verify preconditions are met; dispatch the relevant CAPTAIN or run the relevant step.

The procedure NEVER includes "scan closed tickets for retrospective narration." Closed tickets are evidence of PAST work. The orchestrator's job is to find CURRENT work, not to relive past work.

When a seat genuinely needs to narrate completed work (e.g., authoring a TIMING_LOG, writing a retro doc, surfacing a signoff to PRINCIPAL), the narrative is valid only when the seat can cite the merge SHA of work the seat ITSELF did in this session. The narrative says "in this session, I shipped Arc N via merge commit `<sha>`"; it does NOT say "I just shipped Arc M" when Arc M's work was done by a prior session and is durable on `main` already.

#### 19.7.4 The discipline (two halves; mirrors §19.1)

1. **The verbal admission.** When scanning substrate produces an unfamiliar narrative-shape ("did I just do this?"), the seat says explicitly: "uncertain whose session shipped this, checking." The admission makes the failure-mode visible.
2. **The verification action.** Concrete: `git log -20 --pretty='%h %s %an %ai'` on the affected branch, looking for the seat's own session's commit signature (the Co-Authored-By trailer per §28 + the commit timestamp falling within the current session's lifetime). If the commit is older than the current session, the narrative is past-work, not own-current-work.

The discipline does not require a literal string. The SHAPE is: explicit admission + commitment to verify the work's authorship before narrating.

#### 19.7.5 N=1 provenance + accretion path

Per `MAJOR_POLYBIUS.md` §15 honest-scope and §6.7.1: PRINCIPAL articulated this discipline 2026-05-13 after the PLINY-stoa "Engagement B" confabulation incident was caught and corrected. §6.7.1 defers to the canon-promotion gate (multiple observations + controlled comparison + substrate-level pattern); §6.7.1 does not carve out a separate "PRINCIPAL-declaration shortcut." The honest reading: this discipline enters substrate canon off-gate on PRINCIPAL's project-direction authority + the empirical anchor, with future-evidence-accretion against the §6.7.1 gate still required for promotion to "structural lesson" status.

The supporting evidence at the time of this writing:

- **N=1 bit-by-it (defect class: idle-retro-narrative-confabulation):** 2026-05-13 PLINY-stoa Engagement B incident (detailed in §19.7.1 above). Single observation today; defect class is "orchestrator scans closed tickets while idle and constructs own-current-session narrative."
- **N=0 worked-when-applied with §19.7 canon:** Arc 37 ships the canon; future arcs that handle idle-substrate scans under §19.7's canonical orchestrator-scan procedure accrete worked-when-applied evidence.

The discipline is in substrate canon NOW because PRINCIPAL articulated it 2026-05-13 and the bit-by-it surfaced the same day; promotion to "structural lesson" status with multi-arc empirical backing under the encoded canon is future arcs' work, not this arc's. Same N=1 framing as Arc 35's §28.7, Arc 32's §19.6.4, and the sibling §19.6 itself (also an N=1 + empirical-anchor entry into canon).

#### 19.7.6 Cross-references

- §19.6 (Attestation-confabulation) — sister discipline; §19.6 covers WHAT to cite at attestation time; §19.7 covers WHO did the work.
- §19.1-§19.5 — the parent confabulation-under-uncertainty discipline; §19.7 is a specialization of §19.1 to the idle-substrate-scan case.
- `MAJOR_PLINY.md` §6.2 (Surface-and-wait polling pattern) — the orchestrator-scan procedure §19.7.3 names is the canonical surface-and-wait read; §6.2 names the cadence pattern this procedure operates against.
- `MAJOR_POLYBIUS.md` §16 (POLYBIUS session lifecycle) — the lifecycle disciplines define when a session ends and a successor begins; §19.7 is the discipline that keeps successors from confabulating their predecessors' work as their own.
- `operating-disciplines.md` §28 (Per-CAPTAIN git seat identity via Co-Authored-By trailer) — the verification action in §19.7.4 reads commit metadata; the Co-Authored-By trailer + commit timestamp are the canonical authorship-verification signal.
- Empirical anchor: 2026-05-13 PLINY-stoa "Engagement B" confabulation incident (captured at `stoa--53u` ticket body).
```

### §7.3 — Cite-comment plan

| Read-site file | Read-site location | Cite-comment to add |
|---|---|---|
| `substrate/MAJOR_PLINY.md` | §6.2 (Surface-and-wait polling pattern) end of section | Append: "(Cross-ref: `operating-disciplines.md` §19.7 NEW Arc 37 — Idle retrospective-narrative confabulation; the canonical orchestrator-scan procedure §19.7.3 names is the canonical scan this surface-and-wait pattern operates against.)" |
| `substrate/MAJOR_POLYBIUS.md` | §4 (Disciplines) — append a new bullet to the existing disciplines list OR cite-link inside §4.3 verify-then-execute end of section | Append in §4.3: "(Cross-ref: `operating-disciplines.md` §19.7 NEW Arc 37 — Idle retrospective-narrative confabulation; sister discipline to §19.6 attestation-confabulation; closed tickets are past-work evidence, not own-current-session accomplishment.)" |
| `substrate/operating-disciplines.md` | §19.6.3 (Cross-references) bullet list | Append bullet: "- §19.7 (NEW Arc 37 — Idle retrospective-narrative confabulation) — sister discipline; §19.6 covers WHAT to cite at attestation; §19.7 covers WHO did the work." |

### §7.4 — Self-app probe (NEGATIVE — per A14)

**Negative self-application:** during this arc's execution, no seat may narrate retrospective work as own current-session accomplishment. The §19.7 discipline applies to Arc 37's own POLYBIUS/PLINY operations — if either seat scans substrate during idle moments (between dispatch phases, while waiting on ARGUS or VERA), the seat MUST NOT construct a retrospective narrative of past arcs as own-current-session accomplishment.

**Probe (PLINY signoff verification per A14):** PLINY's signoff at Phase 4 confirms the negative property held — no confabulated retrospective narration in any phase-status comment, any heartbeat, any dispatch verdict. Verification is by audit of the arc's bw timeline + Phase 4 signoff prose against the §19.7.3 canonical scan procedure.

### §7.5 — N=1 framing (per A19)

Per A19: **N=1 bit-by-it** (2026-05-13 PLINY-stoa Engagement B confabulation); **N=0 worked-when-applied with §19.7 canon** (Arc 37 ships the canon; first worked-when-applied is whatever arc next operates under §19.7's canonical scan procedure — likely this arc itself, per A14 negative self-application). §19.7.5 carries this verbatim.

---

## §8 — C6 — Handoff-author skill (stoa--7e3)

### §8.1 — Insertion locus

**File:** new `substrate/skills/handoff-author/SKILL.md` (skill directory creation; ADA mkdirs the parent at build time).
**install.sh wiring:** append `handoff-author` to `SKILL_NAMES` array at line ~146 (after `inspect-script-output`, matching the convention of new-skills-appended at end-of-list — current array is NOT alphabetical; `agent-author`, `check-substrate-updates`, `credential-discipline`, `check-bw-release`, `inspect-script-output`; new arc adds at end).
**Role-file cross-refs:** new bullet in `MAJOR_POLYBIUS.md` §16.7 (Cross-references) + new bullet in `MAJOR_PLINY.md` §9 (Activation checklist) or §6 (Communication) — light-touch one-line pointer per directive A7.

### §8.2 — Skill body (final wording)

Full SKILL.md content for ADA to paste verbatim:

```markdown
---
name: handoff-author
description: |
  Author a session-handoff document before /compact or session close, so a future agent (same seat, fresh session, no working memory) can orient quickly via low-token overview + indirection to durable substrate detail. Invoke when told to "prepare for handoff," "prepare for compaction," "write a handoff," "snapshot before /compact," or any equivalent. The handoff is the continuity-of-identity layer (per operating-disciplines.md §30 four-layer identity model): it preserves the in-flight work-state across context resets while pointing at memories (alignment layer) and bw substrate (detail layer) that persist independently. Optionally records the prior-generation session id for /resume per SPECIFICATION.md §10.1 + §12.5 generational-lineage architecture.

  Applies to any agent that wants semi-persistence across compactions — most commonly orchestrator-tier seats (POLYBIUS, PLINY, pair-programmer MAJORs) but also any specialist preserved over long timescales. Triggers on phrasings like "we're approaching context limit — handoff time," "before I /compact, write a handoff," "session-end snapshot," "summarize for the next me."
author: Denson Smith
---

# Handoff-author skill

## When to invoke

- Before invoking `/compact` to reduce conversation context
- Before closing a session that another agent (typically the same seat in a fresh session) will resume
- Periodically during long-running engagements as a checkpoint
- When PRINCIPAL explicitly asks for one

This is NOT a checklist; it is six **guiding principles** that shape what to write. The principles trade off — judgment determines which dominates in any given handoff.

## The six principles

1. **Highest value-per-token first.** A handoff is read by a context-starved agent; the first 200 tokens determine whether they orient correctly. Lead with the load-bearing context — what's in flight, what's just-closed, what immediate decision the next session faces. Background and history come later or as references.

2. **Indirection over inlining.** Reference bw tickets by ID + short description; reference memories by topic, not content; reference durable artifacts by path. The handoff is the *overview*; the detail lives in substrate. A 50-line handoff that points at 10 bw tickets is more useful than a 500-line handoff that inlines them — because the next session can drill into exactly the tickets the work needs, not waste tokens loading detail it won't use.

3. **Write for the context-free reader.** Assume the next agent has only the role file + memories — no prior conversation history. Concepts that were established mid-conversation must be self-contained or explicitly referenced. "The thing we discussed yesterday" fails; "the bw-fit matrix extension at stoa--tvc" works.

4. **Curate based on what they'll need.** Don't dump everything you have; dump what advances the work from here. The test: *if I woke up cold right now and read this handoff, what would I most need to know to keep moving?* Things from earlier in the session that no longer matter — omit. Things that matter only as background context — reference, don't inline.

5. **Cite, don't duplicate.** Cross-reference memories that are load-bearing for the current work; don't restate them. Memories are durable across compactions; the handoff doesn't replace them. The handoff says "see `feedback_radio_check_pattern_for_polybius_coordination.md` for the discipline applied here" — not the discipline's full text.

6. **Honor the value/effort tradeoff.** A 5-minute handoff that captures 80% of the value beats a 30-minute handoff that captures 95%. Ideal is unattainable; good is the target. Author the handoff at the level of effort the next session can afford. If you're about to /compact under time pressure, a short crisp handoff beats a thorough delayed one.

## Suggested procedure (adapt to context — not a template)

This procedure is a *starting point*, not a template. Skip steps that don't apply; expand steps that need more.

1. **Identify the agent role + scope** — POLYBIUS-session handoff vs PLINY-arc handoff vs specialist handoff. Different scopes lead with different content.
2. **Snapshot current state** — what's in flight (background dispatches, open arcs, paused PLINY sessions); what just-closed (recent merges, ticket closes, decisions made).
3. **Identify open decisions** — what does the next session face? Pending ratifications, queued dispositions, awaiting-PRINCIPAL items.
4. **Reference load-bearing context** — by indirection. Memories, bw tickets, durable artifacts on disk. Short descriptions; the next agent reads detail on demand.
5. **Surface any non-obvious state** — uncommitted work, branches not yet merged, processes that survived a session boundary, conventions established mid-engagement.
6. **(Optional but recommended) Record prior-generation session id(s) for /resume.** Per the the-stoa `SPECIFICATION.md` §10.1 + §12.5 generational-lineage architecture, if the engagement may benefit from a successor agent `/resume`-ing the prior generation's terminal session, capture the session id(s) in a "Generational lineage" section of the handoff. The successor reads the handoff, decides whether `/resume` is the right entry path vs fresh session + activation paste, and proceeds accordingly. The session id is the prior generation's `claude` invocation identifier (typically visible in the prior session's terminal title or via `claude --session` invocation). Recording is forward-only; absent capture, the successor spins fresh per the standard activation-paste flow.
7. **Write to a durable location** — workspace-root `HANDOFF_<role>_<date>.md` is a reasonable default; vary by convention. The file persists; it doesn't need to live in bw if the workspace git is fine.

## What handoffs are NOT

- **Not a transcript.** A transcript is high-token, low-value-per-token; the next agent doesn't need to relive the conversation.
- **Not a TIMING_LOG.** TIMING_LOGs are arc-close retrospectives (estimate vs actual; lessons). Handoffs are session-close snapshots (where we are; what's next).
- **Not exhaustive.** The principles above explicitly trade thoroughness for crispness. A handoff that tries to capture everything fails the value-per-token test.
- **Not a substitute for memories.** Memories carry user-alignment + standing disciplines. Handoffs carry work-state. Both are needed; neither replaces the other.

## How this interacts with other substrate layers (the four-layer identity model)

| Layer | Persistence | Role | Cross-ref |
|---|---|---|---|
| Role file | Permanent, loaded every session | Universal identity (what kind of agent you are) | `substrate/MAJOR_*.md`, `substrate/CAPTAIN_*.md` |
| Memories | Permanent, accumulated by interaction | User-alignment (how to serve THIS specific PRINCIPAL) | `~/.claude/CLAUDE.md` (user-tier) + project `.claude/CLAUDE.md` (project-tier) |
| **Handoff (this skill)** | Periodic, manually authored | Work-state continuity (where we are mid-engagement) | `HANDOFF_<role>_<date>.md` at workspace root |
| bw substrate | Durable across sessions | Detail (full ticket bodies, arc history, verdict trails) | `beadwork` orphan branch via `bw show <id>` |

The four layers together let an agent be **semi-persistent**: identity continues across compactions and sessions, even though the working memory resets each time. The handoff is the bridge — without it, the successor session has the role file (universal identity) + memories (PRINCIPAL-alignment) + bw substrate (full project history) but no orientation on WHAT IS IN FLIGHT RIGHT NOW. The handoff supplies that orientation in 200-500 tokens; the successor then drills into bw on demand for detail.

Full canon: `operating-disciplines.md` §30 (NEW Arc 37 — Four-layer identity model).

## Worked examples

The examples below are SHORT illustrations of the principles, not production-grade handoffs. They show the discipline (highest-value-first, indirection, citing memories by path, etc.); a real handoff for a multi-week engagement may be 2-3x longer with more cross-refs.

### Example 1 — POLYBIUS session-end handoff (cross-session continuity)

Context: user-tier POLYBIUS approaching context limit after a multi-day substrate-canonification engagement; authoring handoff so a fresh session tomorrow can resume.

```markdown
# HANDOFF — user-tier POLYBIUS — 2026-05-18

## In flight (read first)

- **Arc 37 (substrate canonification batch, 6 candidates).** PR open at github.com/<user>/the-stoa/pull/N; SHIP verdict from PLINY pending PRINCIPAL ratification. Next session: confirm PRINCIPAL ratification, then merge + close source tickets per A18. See `stoa--7e3` ticket comments for arc-close coordination.
- **Cross-project context.** Railway_stoa Phase 2 deploy unblocked by Arc 35 trailer landing; ariadne-core search backlog at `ariadne--92x` waiting on this session's next-arc directive.

## Just closed

- Arc 36 v2 (coordination hygiene) shipped 2026-05-17 (PR #16); SKILL_NAMES verified post-deploy at all three target modes.
- Pre-branch hygiene verified clean before arc-37/build creation; full state recorded in `stoa--7e3` comments.

## Open decisions for next session

1. Arc 38 directive authoring — `stoa--bj5` is queued per the Pass 4 workplan; needs scope-locking conversation with PRINCIPAL before dispatch.
2. Routine substrate-update check at consumer workspaces — last check 2026-05-15; cadence allows next check tomorrow.

## Load-bearing context (cite, don't duplicate)

- **Forge/shop framing canon at `MAJOR_POLYBIUS.md` §19** — Arc 37 just shipped this; routing decisions now have explicit canon.
- **Four-layer identity model at `operating-disciplines.md` §30** — Arc 37 shipped; the handoff layer is the one this doc IS.
- Memory: `feedback_no_deferrals_stance.md` — PRINCIPAL's 2026-05-17 fix-now declaration; applies to all bug-triage going forward.

## Non-obvious state

- The arc-37/build worktree is cleaned up; local + remote branch deleted. Verified per §5.10 signoff-accuracy.
- `cron 8299ee0f` (the autonomous-mode polling cron) was torn down at arc close per §11 Teardown.

## Generational lineage

Prior session id: `7c5fdafd-29f4-4484-874a-11ece115de16` (synthetic UUID-shape; real session ids are obtainable via the prior session's `claude --session` invocation or terminal title). Successor: decide whether `claude --resume 7c5fdafd-29f4-4484-874a-11ece115de16` is the right entry path (continuity benefit) vs fresh session + activation paste (clean state benefit). For this engagement, fresh session likely preferred — Arc 37 ship is a clean boundary.
```

### Example 2 — PLINY mid-arc handoff (compaction during long arc)

Context: PLINY mid-Arc 38, approaching context limit during Phase 3 verify; authoring handoff so a /compact'd session can resume the same arc without losing phase-state.

```markdown
# HANDOFF — PLINY-the-stoa — 2026-05-20 (mid-Arc 38, Phase 3)

## In flight (read first)

- **Arc 38 (stoa--bj5 substrate-tool reorg).** Worktree at `.claude/worktrees/arc-38-build/`; branch `arc-38/build`. Phase 3 verify in progress: VERA dispatched 23 min ago on bw-poll watch; CATO dispatched 8 min ago; ZENO not yet dispatched (waiting for VERA verdict). See `stoa--bj5.7` for active coordination.

## Just closed

- Phase 2 build (ADA) PASSED 67 min ago; commit `4f8a2d1` on arc-38/build carries all locked content per `agents/design/arc-38/design.md`.

## Open decisions for next session

1. VERA verdict (any moment) — if PASS, dispatch ZENO; if PARTIAL/FAIL, surface to user-tier POLYBIUS per surface-and-wait.
2. CATO verdict (likely within 15 min) — same disposition logic.

## Load-bearing context (cite, don't duplicate)

- Directive at `substrate/arcs/arc-38-build-directive.md`; A1-A14 LOCKED.
- Design at `agents/design/arc-38/design.md` — committed in arc-38/build at `e7c1f9a`; ARGUS round 1 PASS at `stoa--bj5.5`.

## Non-obvious state

- ADA's commit carries the Co-Authored-By trailer per §28 (verified post-commit).
- Pre-branch hygiene PASSED before arc-38/build creation (logged `stoa--bj5.2`).
- bw-poll cron 9c3d8f1a fires every 5 min; do NOT delete until Phase 4 close.

## Generational lineage

Prior session id: `<session-id>`. Successor: `claude --resume <session-id>` recommended — mid-arc /compact recovery benefits from in-context state continuity; no clean boundary for fresh-session reset until Phase 4 close.
```

### Example 3 — Specialist preservation handoff (CAPTAIN-level continuity)

Context: a CAPTAIN holding accumulated context from a complex multi-engagement (rare; typically CAPTAINs are one-shot per dispatch — but for specialized seats like a pair-programmer Major engaged on a long debugging session, the pattern applies).

```markdown
# HANDOFF — pair-programmer MAJOR_ATHENA — 2026-05-19 (sector-4 debugging session)

## In flight (read first)

- **Investigating intermittent timeout at sector-4 `/api/v1/search`.** Two reproducible failure modes isolated: (1) cold-start cache miss > 3s, (2) concurrent-write contention on the search index during ingest. Root cause for (1) settled (cache warm-up missing on Railway deploy); (2) still investigating — instrumentation patch deployed 30 min ago, awaiting next failure to confirm hypothesis.

## Just closed

- Failure mode (1) fix queued — `s4--7m3` filed for a Railway-deploy startup-hook addition.
- Initial confused theory ("upstream rate limit") ruled out by `feedback_correlation_not_causation.md`-shaped investigation.

## Open decisions for next session

1. Wait for next failure-mode (2) event; collect new instrumentation trace; confirm/refute concurrent-write hypothesis.
2. If confirmed: file fix ticket; if refuted: re-scope investigation.

## Load-bearing context (cite, don't duplicate)

- Sector-4 architecture overview at `s4--arch-overview` ticket.
- Memory: `feedback_railway_cold_start_patterns.md` — Railway's cold-start behavior on free tier (which sector-4 is on).
- Instrumentation patch commit `b9f4e22` on `debug/timeout-investigation` branch (NOT merged; debugging-only).

## Non-obvious state

- The `debug/timeout-investigation` branch is local-only; do NOT push (carries diagnostic-only code).
- PRINCIPAL is HITL on this engagement — surface findings, do not autonomously ship fixes.

## Generational lineage

Prior session id: `<session-id>`. Successor: `claude --resume <session-id>` recommended for short-window resumption (debugging context dense); fresh session if more than ~48h has passed (cache-warmth-context decays).
```

## Cross-references

- `operating-disciplines.md` §30 (NEW Arc 37 — Four-layer identity model) — the handoff layer's canon home; this skill is the operational shape of §30.3's handoff layer.
- `substrate/skills/agent-author/` — sibling skill for agent authoring; handoffs are an output of an agent, not the agent itself.
- `substrate/skills/tier2-project-onboarding/` — sibling skill for new-project orientation.
- `MAJOR_POLYBIUS.md` §16 (POLYBIUS session lifecycle) — the lifecycle disciplines this skill operates within.
- `MAJOR_POLYBIUS.md` §16.3 (Handoff is multi-artifact, not single-doc) — the canon home for principle 5's "cite, don't duplicate" wording; this skill's principle 5 reuses §16.3's exact phrasing because the discipline is identical. The handoff doc this skill authors is the INDEX (low-token overview); bw tickets + retro docs + design artifacts + commits are the linked durable artifacts §16.3 names.
- `MAJOR_PLINY.md` §6.2 (Surface-and-wait polling pattern) — PLINY's polling pattern interacts with handoff authoring during long arcs.
- `~/.claude/CLAUDE.md` + project `.claude/CLAUDE.md` — the memory layer this skill cross-references via principle 5 ("cite, don't duplicate").
- `HANDOFF_*.md` files at workspace root — the canonical output location.
- the-stoa `SPECIFICATION.md` §10.1 + §12.5 — generational-lineage architecture the suggested-procedure step 6 implements.
- Empirical anchor: existing `HANDOFF_POLYBIUS_2026-05-14.md` + `HANDOFF_POLYBIUS_2026-05-16.md` at the-stoa workspace root — informal handoffs that pre-date this skill; the skill formalizes the pattern.
```

### §8.3 — install.sh wiring

Exact patch (one line addition):

```diff
 SKILL_NAMES=(
   agent-author
   check-substrate-updates
   credential-discipline
   check-bw-release
   inspect-script-output
+  handoff-author
 )
```

Location: `substrate/install.sh` line 141-147 (the `SKILL_NAMES` array). The new entry appends at the end of the array, matching the existing convention (new-skills-appended; not alphabetical — `check-bw-release` and `inspect-script-output` were both Arc-N additions appended at end).

### §8.4 — Role-file cross-refs (light touch per A7)

**`substrate/MAJOR_POLYBIUS.md` §16.7 (Cross-references) — append bullet:**

```markdown
- `substrate/skills/handoff-author/SKILL.md` (NEW Arc 37 — C6) — the operational shape of §16.3's multi-artifact handoff authoring; invoke before `/compact` or session close.
```

**`substrate/MAJOR_POLYBIUS.md` §16.3 (Handoff is multi-artifact, not single-doc) — append the sibling-cite (rev2 addition addressing ARGUS R5):**

§16.3 already names "Cite, don't duplicate" as the authoring discipline; the new SKILL.md principle 5 reuses identical wording. Land a one-line forward-pointer at end of §16.3:

```markdown
(Cross-ref: `substrate/skills/handoff-author/SKILL.md` (NEW Arc 37 — C6) — the operational shape of this discipline; the skill's principle 5 "Cite, don't duplicate" reuses §16.3's exact phrasing because the discipline is identical.)
```

**`substrate/MAJOR_PLINY.md` §9 (Activation checklist) — append bullet (or §6 Communication if §9 doesn't naturally fit):**

Reading §9 (Activation checklist one-page summary), the cleanest fit is to append a bullet near the existing "Compact-or-clear recovery" or session-management content. Specifically, append at end of §9:

```markdown
- **Before `/compact` or session close:** invoke `substrate/skills/handoff-author/SKILL.md` to author a handoff doc; the successor session reads the handoff to orient on in-flight work-state. (Cross-ref: `operating-disciplines.md` §30 four-layer identity model.)
```

### §8.5 — Self-app probe (POSITIVE — per A14)

**Positive self-application (probability low for 90-180min arc, but canon authorizes):** if any seat in Arc 37's gauntlet hits a `/compact` event or session-close moment, the seat invokes the newly-shipped `handoff-author` skill to author its own handoff. The skill must be invocable from any seat at the moment of /compact; ADA's build commit must land the SKILL.md so the file is on disk and `install.sh` SKILL_NAMES references it.

**Probe (VERA exercises):** verify the SKILL.md is on disk at `substrate/skills/handoff-author/SKILL.md` (existence + frontmatter validity); verify `install.sh` SKILL_NAMES contains `handoff-author`; verify `install.sh --dry-run --target project --project-dir <tmp>` lists `handoff-author` in the deploy plan (per §8.4 smoke beat); verify SKILL.md frontmatter carries `author: Denson Smith` (per A16). No actual /compact event is required — the file's deployability + content correctness is what makes self-application possible.

### §8.6 — N=1 framing (per A19)

Per A19: **N=multi de-facto bit-by-it** (informal HANDOFF_*.md files exist in ariadne-core-workspace + the-stoa — `HANDOFF_POLYBIUS_2026-05-14.md`, `HANDOFF_POLYBIUS_2026-05-16.md`, et al. are the empirical anchors); **N=0 worked-when-applied with formal skill** (Arc 37 ships the skill; first worked-when-applied is the first POLYBIUS or PLINY session that loads the skill before /compact). The skill body itself names the in-practice anchors in its Cross-references section.

---

## §9 — Probes for VERA

VERA exercises the following probe set to falsify the build. Probes are numbered for VERA's probe-result section. Each probe corresponds to a candidate's locked content OR to the cross-cutting A15/A16/A18 disciplines.

1. **C1 §19 present in MAJOR_POLYBIUS.md.** Probe: `grep -n "^## 19\. Two-team architecture" substrate/MAJOR_POLYBIUS.md` returns one match between current §18 and end-of-file. Section body contains the forge/shop framing, the two-team table, the routing rule, the §17 cite, and the N=1 provenance subsection.
2. **C2 §29 present in operating-disciplines.md.** Probe: `grep -n "^## 29\. Multi-team interoperation" substrate/operating-disciplines.md` returns one match between current §28 and the `## Agent-regime inverses` block. Body contains the ecosystem-naming, prefix-namespace table, cross-team request channel, convention-based discovery, and N=1 provenance.
3. **C3 §30 present in operating-disciplines.md.** Probe: `grep -n "^## 30\. Four-layer identity model" substrate/operating-disciplines.md` returns one match immediately after §29 and before `## Agent-regime inverses`. Body contains the four-layer table, memories-as-alignment framing, cross-layer interaction discussion, and N=1 provenance.
4. **C4 §10 + §11 extensions present (bolded-paragraph / bolded-step continuation style per rev2; §10 + §11 are NOT subsectioned).** Probes:
   - (a) `grep -nF "**Three-mode progression sequence.**" substrate/operating-disciplines.md` returns one match inside §10 (between the `**Universal escalation triggers (autonomous mode):**` paragraph and the `**Cross-ref:**` paragraph).
   - (b) `grep -nF "**Transition triggers.**" substrate/operating-disciplines.md` returns one match inside §10, immediately following the progression-sequence paragraph.
   - (c) `grep -nF "**Regression upward is normal, not exceptional.**" substrate/operating-disciplines.md` returns one match inside §10.
   - (d) `grep -nF "**Provenance + accretion path (progression canon).**" substrate/operating-disciplines.md` returns one match inside §10.
   - (e) `grep -nF "**7. Mode declaration in directives.**" substrate/operating-disciplines.md` returns one match inside §11 (after the existing `**Teardown procedure**` paragraph, before the `---` separator).
   - (f) `grep -nF "**8. Mid-engagement mode transitions.**" substrate/operating-disciplines.md` returns one match inside §11.
   - (g) `grep -nF "**9. Downward-propagation rule (Arc 21 A4 recap).**" substrate/operating-disciplines.md` returns one match inside §11.
   - All bodies contain the locked content (progression sequence; transition triggers table; mode-change tag form + §7.7 case-3 interaction; downward-propagation recap).
5. **C5 §19.7 present in operating-disciplines.md.** Probe: `grep -n "^### 19\.7 Idle retrospective-narrative" substrate/operating-disciplines.md` returns one match between current §19.6 and the `## 20. Credential discipline` heading. Body contains the empirical anchor (2026-05-13 PLINY Engagement B), the canonical orchestrator-scan procedure, the verbal-admission + verification-action discipline, and N=1 provenance.
6. **C6 SKILL.md present at substrate/skills/handoff-author/SKILL.md with `author: Denson Smith` frontmatter.** Probes: (a) `test -f substrate/skills/handoff-author/SKILL.md` exits 0; (b) `grep -E "^author: Denson Smith$" substrate/skills/handoff-author/SKILL.md` returns one match in the frontmatter block; (c) `grep -E "^name: handoff-author$" substrate/skills/handoff-author/SKILL.md` returns one match; (d) the body contains the six principles, suggested procedure (with step 6 generational lineage capture), what-handoffs-are-NOT framing, layer interaction table, and three worked examples.
7. **install.sh SKILL_NAMES contains `handoff-author`.** Probe: `grep -E "^\s+handoff-author$" substrate/install.sh` returns one match between the `SKILL_NAMES=(` opening and the `)` closing.
8. **install.sh dry-run deploys handoff-author to a synthetic target.** Probe per `operating-disciplines.md` §8.4 smoke beat: `bash substrate/install.sh --dry-run --target project --project-dir <tmp> | grep handoff-author` returns one match (file appears in deploy plan for project target). Also exercise `--target subproject --parent-dir <tmp> --subproject test` and `--target user` per §8.4 multi-target check.
9. **Cite-comments resolved at every plan-named site.** Probes per §3.3 (C1 cite-comments), §4.3 (C2), §5.3 (C3), §6.3 (C4), §7.3 (C5), and §8.4 (C6 role-file cross-refs). Each cite-comment is verified by grep against the named read-site file for the appended cross-ref string. ZENO performs this mechanically per spec-vs-result.
10. **Co-Authored-By trailer on ADA/DAEDALUS commits per §28.** Probes: (a) `git log --pretty='%(trailers)' arc-37/build | grep "CAPTAIN_DAEDALUS_the-stoa"` returns at least one trailer line (this design.md commit); (b) `git log --pretty='%(trailers)' arc-37/build | grep "CAPTAIN_ADA_the-stoa"` returns at least one trailer line (ADA's build commit(s)). Trailer email format matches `captain-<mnemonic>@the-stoa.local` per §28.1.

**Additional VERA notes:**

- Probe 8 (install.sh dry-run) is the canonical smoke beat per §8.4 — the substrate has shipped at least three prior arcs (21, 27, 28) where a skill or template was added without the SKILL_NAMES/TEMPLATE_NAMES wiring; the dry-run-and-grep is the structural defense. If probe 8 fails (handoff-author is absent from any target's dry-run output), surface as FAIL with the specific missing target and the install.sh fix needed.
- Probe 6c (skill `name:` field) is load-bearing because Claude Code's skill discovery is by-frontmatter (per §17.4 silent-collision note). If the `name:` field doesn't match the directory name, the skill is silently discoverable-but-broken.

---

## §10 — CATO scope

CATO is MANDATORY for this arc per directive §Phase 3 ("CATO is MANDATORY for this arc: substrate canon work + new skill + multiple new sections; wording precision matters"). CATO cold-reads the diff for:

1. **Wording precision in all 6 new sections.** Canon-quality prose; voice consistency per the file each section lands in (MAJOR_POLYBIUS.md uses second-person `you` to address POLYBIUS; operating-disciplines.md uses third-person describing the discipline universally). C4's inline §10 bolded-paragraph additions + §11 step 7-9 continuation must match the voice of the surrounding §10 + §11 content (§10 uses bolded-paragraph markers in a flat layout; §11 uses bolded-step numbered markers — additions must NOT introduce `### N.X` subsection numbering that would clash with the existing flat / bolded-step style). C5's §19.7 must match §19.6's voice (both confabulation-discipline subsections).
2. **Cite-comment completeness.** Every read-site named in §3.3, §4.3, §5.3, §6.3, §7.3, §8.4 is addressed in the diff. Missing cite-comments are a CATO FAIL — they break the cross-cite property the substrate's accretion model depends on.
3. **Skill body completeness + `author: Denson Smith`.** Frontmatter validates; six principles present; suggested procedure complete (with step 6 generational-lineage capture per A13 fold); what-handoffs-are-NOT framing present; layer interaction table present; three worked examples present (each 15-30 lines per the directive's voice notes — not full production handoffs); cross-references section present. `author: Denson Smith` mandatory per A16 + CLAUDE.md absolute rule.
4. **Scope discipline against A17.** No bundling of bj5/utn/3sz/5sr/pqn (Arc 38 + Arc 39 candidates). No mechanical-enforcement infrastructure (no pre-commit hooks, validators, etc.). No meta-agent. No memory-introspect skill. No multi-team registry. CATO surfaces any creep as a CATO FAIL — the scope-lock is hard-locked per A17.
5. **Trailer audit per §28.** Every ADA + DAEDALUS commit on arc-37/build carries the `Co-Authored-By: CAPTAIN_<MNEMONIC>_the-stoa <captain-<mnemonic>@the-stoa.local>` trailer. PLINY orchestrator commits + POLYBIUS housekeeping commits are NOT tagged per §28.2 exemption list — verify the exemption is honored (no spurious trailers on PLINY merges).
6. **Voice notes specific to this arc.** Refer to the human as PRINCIPAL (descriptive role) — never COLONEL (reserved future agent rank per `MAJOR_PLINY.md` §7.7). Avoid marketing vocabulary ("elegant," "robust," "scalable"). The design is correct or it isn't; adjectives don't make it more so. For C2, use the canonical workspace names: the-stoa, ariadne-core-workspace, railway_stoa; don't manufacture additional workspaces.

---

## §11 — ZENO scope

ZENO performs the mechanical spec-vs-result check:

1. **A2-A7 locked content present in the diff.** Each of the 6 candidates has the locked content named in the directive §A2-§A7 present in the build. ZENO grep against each candidate's locked element (e.g., A2's "forge / shop" metaphor present in §19; A5's "Mode 2 → Mode 1" transition trigger present in §10's new `**Transition triggers.**` paragraph table; etc.).
2. **A15 cite-comments resolved.** Every plan-named cite-comment (per §3.3, §4.3, §5.3, §6.3, §7.3, §8.4 in this design.md) is verified present in the diff via grep.
3. **A16 file-frontmatter `author: Denson Smith` verified.** C6 SKILL.md frontmatter contains `author: Denson Smith`. ZENO greps for the exact string in the frontmatter block.
4. **A17 scope verified.** No mention in the diff of: bj5, utn, 3sz, 5sr, pqn (Arc 38 + 39 candidates); pre-commit hook; validator; meta-agent; memory-introspect skill; multi-team registry. ZENO grep for the explicit terms in the diff.
5. **A18 closure prep verified.** Phase 4 work; ZENO notes the 6 source tickets (stoa--86k, stoa--kt6, stoa--wad, stoa--ntn, stoa--53u, stoa--7e3) are queued for close at ship with cross-ref + audit comment per the directive. ZENO does NOT close tickets — that's PLINY signoff at Phase 4 — but verifies the closure plan exists in the design.
6. **Co-Authored-By trailer per §28 verified on ADA + DAEDALUS commits.** Mechanical grep of the arc-37/build branch's git log for `CAPTAIN_<MNEMONIC>_the-stoa` trailers; PLINY commits exempt per §28.2.

---

## §12 — Out of scope (per A17)

This design EXPLICITLY does NOT cover, and ADA must not build:

- **Arc 38 / Arc 39 candidates.** stoa--bj5 + stoa--utn + stoa--3sz + stoa--5sr + stoa--pqn ship in their own arcs per the Pass 4 + Pass 5 workplan. Bundling here would create gauntlet bloat.
- **Mechanical enforcement infrastructure** for any of the 6 disciplines. No pre-commit hooks, no validators, no CI lint, no automated cite-comment generators. Per `operating-disciplines.md` §27 mechanical/agent-split pattern; mechanical infra ships only on documented recurrence.
- **Canon extensions to non-POLYBIUS / non-CAPTAIN seats** beyond what each candidate's existing scope covers. C4 covers POLYBIUS + PLINY mode-handling; pair-programmer Majors inherit per §13.3 propagation. No new MAJOR seats are authored.
- **install.sh / apply.sh / revert.sh changes beyond C6's SKILL_NAMES one-line addition.** Substrate-deploy mechanism is otherwise untouched.
- **Meta-agent for cross-generation lineage analysis** (SPECIFICATION.md §10.1.3 / §12.5 future-work). Out of scope per spec; future post-spec work.
- **memory-introspect skill** (C3 out-of-scope explicit). C3 ships prose canon for memory-as-alignment, not the introspect tool. The discipline (memory introspection is supported) is named; the tool that operationalizes it is future arc.
- **multi-team registry** (C2 out-of-scope explicit). Convention-based discovery is sufficient for current ecosystem size; future arc if scale demands.

If ARGUS or CATO surfaces a scope concern touching any of the above, treat as substance disagreement per A17 — confirm A17 wording, file follow-up ticket if the concern has merit, do NOT expand this arc.

---

## §13 — Self-assessed weak points (per CAPTAIN_DAEDALUS §6.2)

I owe the post-work gate honest naming of brittle spots ARGUS should pay particular attention to.

1. **§19's routing rule (§19.3) leans on POLYBIUS judgment more than it leans on a decision tree.** A reader looking for "what do I do when this specific work arrives" finds framing, not algorithm. The directive A2 explicitly out-of-scopes a routing-decision algorithm ("POLYBIUS owns routing judgment; C1 names the framing, not a decision tree"), so this is intentional — but ARGUS should check that the framing is concrete enough to be operationally useful, not so abstract that POLYBIUS could rationalize any routing call as "this matched the framing."
   - **Why this shape anyway:** the alternative (a decision tree) would over-specify; routing judgment is exactly the kind of judgment §8.2's "preserve judgment latitude where judgment is the actual job" names as not-to-pre-script. The framing is honest about its limit.
2. **§29's cross-team request channel (§29.4) sits adjacent to §7.4's cross-tier convention.** Both name the `[for: <seat-slug>]` pattern. A reader could conflate the two — "cross-team" and "cross-tier" are easily confused. ARGUS should check that the disambiguation is clear, or recommend a one-line clarifying note.
   - **Why this shape anyway:** the convention IS the same mechanism — `[for:]` tags + bw-mediated meeting in the lower tier. Inventing a new mechanism for cross-team would be over-engineering; reusing §7.4 is correct. The cite-comment plan in §4.3 includes a §7.4 cross-ref that names the extension explicitly.
3. **§30's four-layer model presents identity as a clean composition, but real agents experience the layers as messier (in-context-window state crosses layer boundaries; a memory authoring action is also a current-session work-state).** The model is canon, but the lived experience is muddier. ARGUS may surface that the model under-names the cross-layer leakage.
   - **Why this shape anyway:** the four-layer model is a structural framing, not a phenomenological one. The leakage exists but the substrate's job is to make the structure crisp enough that seats know which layer to write to when they have a choice. Future arcs may extend with a "cross-layer interaction" section that names the leakage cases explicitly; this arc ships the structure.
4. **C4's §10 `**Transition triggers.**` table describes "concrete signals" that are still substantively prose-shaped ("PRINCIPAL declares AFK"). A more mechanical signal (e.g., "PRINCIPAL utters one of the exact trigger words at §10's trigger-words table") would be testable.**
   - **Why this shape anyway:** the trigger words are already at §10's existing trigger-words table (verbatim list of "go autonomous", "step back", etc.); the new transition-triggers table cross-refs the same table by inheritance with the explicit pointer "The trigger words in column 2 are the same exact strings tabulated in the trigger-words table above; see that table for the verbatim list (no duplicate source-of-truth here)." (rev2 added this pointer). Single source of truth preserved.
5. **C4's §11 step 8 mode-change comment convention (`[mode-change <new-mode>] [from: <self-seat-slug>]`) is a NEW tag form — not previously used in the substrate.** Adding a new tag-form mid-arc could collide with future tag conventions OR could be mis-parsed by §7.7's tag-parser procedure. **Resolved in rev2:** step 8 now explicitly names the §7.7 case-3 classification ("Tag-parser interaction (per §7.7): the `[from: <self-seat-slug>]` clause in the mode-change tag classifies under §7.7 case 3 ... contributes to `last_self_activity` / `last_peer_activity` timeline-arithmetic as a coordination-attentiveness signal. This is INTENDED ..."). The mode-change tag serves dual function — coordination signal (substance) AND liveness signal (timeline-arithmetic); counting it as a heartbeat-equivalent for missed-check thresholds is correct behavior because the seat issuing the mode-change IS alive and IS announcing a coordination-attentive action.
   - **Why this shape anyway:** rather than carving out a non-arithmetic exception (which would require parser logic to distinguish "real heartbeat" from "mode-change heartbeat" — extra complexity for no benefit), letting the standard §7.7 case-3 logic handle the tag treats the mode-change as the liveness signal it implicitly is. ARGUS R3 surfaced this; resolution landed in rev2's step 8 prose.
6. **C6's worked examples (§8.2 Example 1-3) are MY synthetic constructions for illustrative shape.** They are intentionally short (per directive voice notes: 15-30 lines each, not production handoffs). But a reader unfamiliar with the discipline could read them as templates to copy-paste, despite the skill's explicit "this is guidance, not a template" framing.
   - **Why this shape anyway:** worked examples are dramatically more useful than abstract guidance per §8.2 scaffolding-and-guardrails. The risk of copy-paste-as-template is real but the alternative (no examples) is worse. CATO should cold-read the examples and flag any that read as too template-y.
7. **(Resolved during drafting)** C6's A13 fold (session-id record into SKILL.md step 6) references `SPECIFICATION.md §10.1 + §12.5`. I initially flagged uncertainty about whether the spec named a more involved capture procedure than what step 6 records. I verified post-draft by reading both sections directly: §10.1 says "Each generation handoff produces a handoff doc (per the handoff-author skill) and records the prior generation's session id(s) so successor generations can `/resume` them"; §12.5 names this as "could fold into Arc 37 C6 or land as a small follow-up." Step 6's wording is faithful to the spec. **Resolution is recorded here for ARGUS-visibility; weak point closed at draft time, not deferred.**

---

## §14 — Residual questions for ARGUS

1. **(Resolved post-draft; FYI for ARGUS)** Earlier I flagged uncertainty about whether `SPECIFICATION.md` §10.1 + §12.5 named a more involved session-id capture procedure than what §8.2 step 6 records. I verified post-draft by reading both sections: §10.1 says "Each generation handoff produces a handoff doc (per the handoff-author skill) and records the prior generation's session id(s) so successor generations can `/resume` them"; §12.5 explicitly names this as "could fold into Arc 37 C6 or land as a small follow-up." My step 6 captures the discipline correctly. ARGUS may re-verify by reading those two sections; flagging for ARGUS-visibility per §6.4 consume-research discipline.
2. **(Resolved in rev2; FYI for ARGUS)** Earlier I asked whether the mode-change tag's §7.7 parser interaction needed to be made explicit. Rev2 lands the explicit classification in §11 step 8 prose: `[from: <self-seat-slug>]` triggers §7.7 case-3 (slug-match → timeline-arithmetic contribution); the mode-change is treated as a heartbeat-equivalent — coordination signal AND liveness signal. ARGUS R3 surfaced + closed.
3. **(Medium)** Does §29.4's cross-team request channel need a clearer disambiguation from §7.4's cross-tier convention? Both use `[for:]` tags; a reader could conflate "cross-team" and "cross-tier." (Surfaced from weak point §13 item 2.)
4. **(Low)** Are the three worked examples in C6 (§8.2 Examples 1-3) too template-y? Should the skill body include an explicit "do not copy-paste these — they are illustrative shape only" line above the Worked examples section? (Surfaced from weak point §13 item 6.)
5. **(Low)** Is §19.3's routing rule concrete enough to be operationally useful, or too abstract? (Surfaced from weak point §13 item 1.)

ARGUS may surface additional risks not in this list; I do not claim this list is complete.

---

## §15 — Phase-handoff to ADA (build mechanics)

When ARGUS PASSes (or after revision rounds resolve), ADA's Phase 2 build mechanics:

1. **Per-candidate edits in coordinated commits.** ADA picks whether to land all 6 candidates in one coherent commit OR in per-candidate commits; the directive Phase 2 line authorizes either. Per-candidate commits make per-candidate review easier; one-commit makes the squash-merge body cleaner. **DAEDALUS recommendation: per-candidate commits (6 commits) — the canon is sufficiently independent that per-candidate review is the higher-value form, and the squash-merge to main preserves all 6 trailer signatures per §28.3.**
2. **Order matters for cite-comments.** Several cite-comments reference sections landed by OTHER candidates in this arc (e.g., §29.7 cross-refs §30; §30.6 cross-refs §29; §10's new bolded-paragraph additions include a closing cross-ref to §30). ADA should land C1-C5 substrate prose FIRST (so the section numbers + marker labels exist on disk), THEN add the cite-comments referencing them in a final commit. OR ADA can land per-candidate with stub cross-refs and a final "wire up cross-refs" commit. **DAEDALUS recommendation: land per-candidate; in each candidate's commit, write the cite-comments forward-only (the sections being cite-referenced will exist by the time the build is complete and CATO reads the diff). The minor temporal anomaly (commit N references section landed in commit M > N) is acceptable; CATO reads the diff, not the commit history.**
3. **Worktree convention.** ADA works in `.claude/worktrees/arc-37-build/` per the directive A20; pre-branch hygiene already verified clean by PLINY at dispatch authoring.
4. **install.sh smoke beat per §8.4.** ADA runs the dry-run smoke beat for `handoff-author` at all three target modes after the SKILL_NAMES addition lands: `bash substrate/install.sh --dry-run --target project --project-dir <tmp> | grep handoff-author`, plus `--target subproject` and `--target user`. Failure to appear at any target → install.sh wiring needs the fix in the same commit.

---

## §16 — DAEDALUS summary

The design covers all 6 candidates with locked content per A2-A7, aligned sub-decisions per A8-A13 (matching user-tier POLYBIUS leans), cite-comment plan per A15, scope hard-lock per A17, source-ticket closure prep per A18, N=1 framing per A19, and self-applied pre-branch + worktree + signoff per A20. Substance disagreements with the directive or leans: none. Open questions for ARGUS: enumerated at §14 (the highest-confidence weak point is the SPECIFICATION.md §10.1 + §12.5 cross-ref content for the C6 step 6 fold).

ARGUS is the right next reader. ADA's build per §15 phase-handoff once ARGUS passes.

**Co-Authored-By:** this design.md commit carries `Co-Authored-By: CAPTAIN_DAEDALUS_the-stoa <captain-daedalus@the-stoa.local>` per `operating-disciplines.md` §28.1.

---

Standby, run.
