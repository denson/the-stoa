# Design — Critical-issue → dedicated goal-locked remediation workflow (stoa--h2z)

**Author:** Denson Smith (the PRINCIPAL)
**Stage:** Gauntlet Stage A (design). DESIGN arc — this artifact is the deliverable.
**Operating mode:** HITL. Surfaces at a HARD STOP (floor-manager → user-tier POLYBIUS) for ratification BEFORE any build. There is no build in this arc.
**Consumes (shipped substrate):** `operating-disciplines.md` §35 (Arc A prevention); `CAPTAIN_VERA.md` §5.2/§6, `CAPTAIN_DAEDALUS.md` §6.13, `CAPTAIN_CATO.md` §6.1 item 11, `CAPTAIN_ARGUS.md` §6.9, `MAJOR_POLYBIUS.md` §4.3.2 (Arc B detection); save-verdict `--threat-coverage-probe-ids` / `--threat-ratified-mitigation-count` (B2 keystone).
**Named dependency (NOT an assumption):** `substrate/skills/workflow-composer/SKILL.md` is **SHIPPED CANON** — forge-promoted in Arc 53 (commit `c6ae899`), git-tracked, and wired into `substrate/install.sh:218` inside the `SKILL_NAMES` deploy array. The COMPOSITION guidance (how to author a workflow) is therefore deployable today. Workflow **DEPLOY is built-in runtime infrastructure** (web-verified vs https://code.claude.com/docs/en/workflows, 2026-06-04): a workflow is saved via `/workflows` → select run → press `s` to `.claude/workflows/` (project, repo-shared) OR `~/.claude/workflows/` (personal), and is auto-discovered as a `/<name>` command in future sessions — there is **no registry and no `WORKFLOW_NAMES` array** concept; a workflow is just a file the runtime discovers. `install.sh`'s only possible role is an optional one-line copy to propagate `/defeat-threat` to consumer projects' `.claude/workflows/` (the same pattern as skills/modules) — trivial, NOT "infrastructure that must be built." So the Tier-2 dependency is **NOT missing deploy infra**: it is the **AUTHORING EFFORT** of a gauntlet-faithful `/defeat-threat` workflow. Because the runtime **forbids mid-run human input** (docs: "No mid-run user input… For sign-off between stages, run each stage as its own workflow"), a faithful `/defeat-threat` with a HARD-STOP human ratification must be **SPLIT into stage-workflows** (Stage A → human ratify → Stage B), schema-wired and battle-tested — arc/team-sized work. See §2.5 + §6 HS-1.

---

## 1. Problem restatement

When the gauntlet **detects** a named threat that is surfaced-but-not-yet-defeated, the current regime patches it **inline** — as a sub-item of whatever larger arc was already running (a ratification-grid bullet, a build-scope line). Sub-goals drift: they compete with the arc's "real" deliverable, inherit its framing, and take the easier reading. That is the exact `origindex-trw` M2 failure (`u--ith` / `u--tgc`): a correctly-named threat, a build that picked the easier wrong surface, caught only at the close-gate.

h2z's mechanism: on detection of such a threat, **STOP + SURFACE to the PRINCIPAL** (a security bug is a load-bearing human-attention moment per the "direction is scarce" thesis), then **spawn a DEDICATED, single-purpose remediation workflow whose only goal is to defeat THAT specific named threat M\<n\>.** Because threat-defeat is the *whole* goal of the dedicated workflow — there is no larger deliverable to hide behind — the drift bar is raised to its maximum: the sub-goal can no longer take the easier reading because there is no "real" deliverable competing with it. (This is a goal-lock, not a tool-strength guarantee; see §2.3 for the precise mechanism and its inherited Arc-B residual.) The workflow's single success criterion is the Arc-B threat-coverage assertion: it passes **only if an EXECUTED probe drives the real M\<n\> attack path to blocked** (not a writable sentence — the B2 keystone), which is what closes external-review MAJOR-1 (false-confidence).

**Imported assumptions (named per §6.1):**
- *h2z is the RESPONSE layer, not a third detector.* Arc A (PLINY A1, pre-build) and Arc B (VERA/CATO/POLYBIUS, at verify/relay/close) already DETECT a named-threat-without-a-defeating-probe **within the arc that surfaced it**. h2z does not add a new detector; it reuses their existing detection outputs as a **trigger** and adds the *escalate-into-a-dedicated-arc* response. The novelty is the response shape (dedicated goal-locked workflow), not the detection.
- *Trigger reuses §35.1 classification verbatim — no new "is this critical?" judgment.* The trigger predicate is built entirely on the already-shipped named-threat vocabulary (M\<n\>, ARGUS-confirmed, non-self-exemptable). I import no fuzzy criticality scale. This is the brief's hook, used as the design's spine.
- *h2z ships as a discipline + a workflow PATTERN, with the executable `/defeat-threat` workflow as a separable follow-on deliverable.* See §2.5 + §6 HS-1 — the workflow-composer (composition guidance) is already shipped canon and workflow DEPLOY is built-in runtime infrastructure, so the pattern is authorable today; the executable `/defeat-threat` SCRIPT is separable not because of missing infra but because of **AUTHORING EFFORT**: the runtime forbids mid-run human input, so a gauntlet-faithful `/defeat-threat` with a HARD STOP must be SPLIT into stage-workflows (Stage A → human ratify → Stage B), schema-wired and battle-tested — arc/team-sized. The trigger discipline + pattern degrade gracefully to the classic PLINY-run gauntlet, dispatched as its own dedicated goal-locked arc, with no script required.

---

## 2. Approach

### 2.1 The trigger predicate (the hard design question)

**TRIGGER fires when, at any Arc-B detection surface, a named threat `M<n>` is surfaced-but-not-yet-defeated.** Precisely, the predicate is the disjunction of the two already-shipped Arc-B failure shapes — h2z adds no new condition, it *names the response* to these existing ones:

> **TRIGGER(M\<n\>) := the threat M\<n\> is §35.1-classified (named, ARGUS-confirmable, non-self-exemptable) AND has NO passing threat-coverage binding** — i.e. EITHER
> **(T-a)** a `threat_coverage:` entry for M\<n\> whose `defeats_via_probe:` id is **absent from `probes_executed:`** or whose `probe_evidence:` is **empty** (the VERA §5.2 / §6 finding — "absence-of-an-executed-probe, not absence-of-a-sentence"), OR
> **(T-b)** a mapped/named M\<n\> with **NO threat-anchored probe spec'd at all** (the ARGUS §6.9 item-4 "map-present-but-probe-absent" design smell, OR a mid-arc-ratified threat that bypassed design — the §35.5 named residual "during-build ratification").

**Where it fires (detection sources, in pipeline order):**

| Detection surface (already shipped) | What it emits that h2z reads | Trigger shape |
|---|---|---|
| ARGUS critique (`§6.9`) | mapless-mitigation OR map-present-but-probe-absent design smell (`load_bearing: true`) | T-b (pre-build) |
| PLINY A1 (`§35.2`, pre-ADA beat) | a ratified item restated as `addresses M<n>` but with no design-folded map | T-b (pre-build) |
| VERA verdict (`§5.2/§6`) | `threat_coverage:` entry with `defeats_via_probe:` ∉ `probes_executed:`, or empty `probe_evidence:`; verdict is `fail` | T-a (post-build) |
| CATO (`§6.1 item 11`) | independent cross-check disagrees with VERA's threat-coverage line | T-a (post-build) |
| POLYBIUS §4.3.2 (relay + close-gate) | shipped mitigation's cited probe did not exercise the mapped attack path | T-a (at relay/close) |

**The escalation owner is the floor-manager (PLINY) → user-tier POLYBIUS**, not the detecting CAPTAIN. A CAPTAIN that detects a trigger surfaces it in its verdict (it already does — these are shipped findings); h2z's addition is: **on a triggered finding, PLINY does NOT route the fix back as an inline ADA re-dispatch on the SAME arc; it STOPS, surfaces to the PRINCIPAL, and offers the dedicated remediation workflow** (§2.3). The inline-patch path is exactly the drift surface h2z exists to remove.

### 2.2 STOP + SURFACE (the human-attention gate)

On TRIGGER, PLINY halts the originating arc's threat-fix path (the rest of the arc may proceed or pause per PLINY judgment — h2z scopes only the threat-fix) and surfaces to user-tier POLYBIUS → PRINCIPAL a fixed payload:

```
THREAT-REMEDIATION TRIGGER
threat: M<n>  (ARGUS-confirmed: <yes|pending>)
attack-path: <the A3-map attack-path string, verbatim>
detected-at: <ARGUS critique | PLINY A1 | VERA verdict | CATO | POLYBIUS relay/close>
trigger-shape: <T-a: probe-bound-but-not-executed | T-b: no-threat-anchored-probe>
originating-arc: <ticket-id>
proposed-response: spawn dedicated /defeat-threat remediation workflow with goal = block M<n>
DECISION REQUIRED: authorize remediation workflow? (the goal is locked to defeating M<n>;
  human confirms DIRECTION; agents execute remediation with the goal un-droppable)
```

This is the load-bearing attention moment: the human confirms *direction* (this threat is real, defeat it now), and the agents execute remediation against a goal they structurally cannot re-scope. The PRINCIPAL's authorization is the §25 PRINCIPAL-gate on spawning the workflow.

### 2.3 The remediation workflow shape (the VEHICLE)

The dedicated workflow is **goal-locked**: its single returned success criterion is "M\<n\>'s attack path is driven-to-blocked by an EXECUTED probe." It reuses the gauntlet seats via `agentType` (workflow-composer mapping). Linear sequence for a single threat target (not `pipeline()` — that is for fan-out; per SKILL §"Composition procedure" step 4):

```
goal (LOCKED, the workflow's single returned success criterion):
  "block the M<n> attack path; threat_coverage assertion passes ONLY if an
   EXECUTED probe drives the real attack path to blocked (B2 keystone)."

stage A (design) — same-session, no human mid-stage:
  STRABO   { agentType, schema } → map the M<n> threat surface (attack-path enumeration)
  DAEDALUS { agentType, schema } → mitigation + MANDATORY threat→mitigation map (§35.4):
                                   M<n> → <attack-path> → <how-defeated>
                                   + spec the threat-anchored probe (§6.13): asserts
                                     (a) attack-blocked AND (b) legit-unaffected
  ARGUS    { agentType, schema } → audit: does the design DEFEAT M<n>? (not "is it sound?")
                                   confirm the A3 map binds mitigation→threat; confirm a
                                   threat-anchored probe is SPEC'd (§6.9 item-4 smell if not)
  → return design + audit + review-surface

=== HARD STOP (stage = workflow boundary; the runtime forbids mid-run input) ===
   floor-manager → user-tier POLYBIUS reviews: design defeats M<n>? authorize build?

stage B (build + verify) — same-session, no human mid-stage:
  ADA  { agentType }          → build the mapped mitigation
  VERA { agentType, schema }  → EXECUTE the threat-anchored probe against the REAL attack
                                path (§5.2): observe (a) attack-blocked AND (b) legit-unaffected;
                                emit threat_coverage: { mitigation: M<n>, defeats_via_probe: pX,
                                probe_evidence: <recorded output>, attack_path_exercised: ... }
  CATO { agentType, schema }  → independent cross-check (§6.1 item 11): is defeats_via_probe
                                ∈ probes_executed, and did it drive the MAPPED attack path?
  → return verdict + review-surface

success criterion (the workflow's single returned PASS gate):
  threat_coverage.defeats_via_probe ∈ probes_executed
  AND probe_evidence non-empty
  AND the executed probe exercised the MAPPED attack-path (not a happy-path proxy)
  → else STRUCTURAL FAIL (the workflow cannot return PASS).
```

**Goal-lock mechanism (the anti-drift property — and its precise strength).** The workflow's returned success object has exactly ONE pass gate, the threat-coverage assertion above; there is no "larger deliverable" field for the threat-fix to become a sub-bullet of. Because the goal IS the threat, the *intended* path to PASS is an executed-attack-path probe. **The strength is asymmetric, and the design states it honestly:** only the **empty-binding** sub-check (declared-mitigations ⇒ ≥1 probe-id) is skill-tool-enforced (save-verdict exit-4 for the landing seat). The `defeats_via_probe ∈ probes_executed` AND "the executed probe drove the MAPPED attack path" sub-checks are **seat-side greps** (VERA §5.2/§6, CATO §6.1 item 11, POLYBIUS §4.3.2) — Arc-B's existing enforcement, NOT tool-strength. So the goal-lock **raises the drift bar to its maximum** (no competing deliverable to hide a sub-goal under) but does not make drift *structurally impossible* for the script form: a seat could still emit a probe-id that did not exercise the real attack path, caught by the redundant seat-side net rather than the schema. This is the same residual the shipped Arc B carries and names (WP2); h2z inherits it, does not worsen it. The whole-goal shape is what makes the bar high where a *sub-goal* bullet's bar is low (§4 MAJOR-1 closure).

**`args` parameterization (reuse, not re-author per incident).** Per workflow-composer SKILL §"Parameterizing… with `args`", the `/defeat-threat` workflow is authored **once**; each trigger invokes `Run /defeat-threat on M<n>` → `args = { threat: "M<n>", attack_path: "<from A3 map>", originating_arc: "<ticket>" }`. The same script serves every named threat — h2z is a reusable MECHANISM, not a per-incident hand-authored arc.

### 2.4 Surfaces this design touches (for the future BUILD arc — NOT built here)

| Surface | Change the build arc would make | Why |
|---|---|---|
| `substrate/operating-disciplines.md` | new §36 "Threat-remediation escalation (detect → goal-locked workflow)" — the trigger predicate + STOP+SURFACE + the escalate-don't-inline-patch discipline | the team-wide canon home; references §35 + Arc-B seats |
| `substrate/MAJOR_PLINY.md` | a beat: on a triggered finding, STOP + surface + offer the remediation workflow (do not inline-re-dispatch ADA on the same arc) | PLINY is the escalation owner |
| `substrate/MAJOR_POLYBIUS.md` | the PRINCIPAL-surface payload (§2.2) + the authorize-remediation-workflow gate | POLYBIUS owns the PRINCIPAL channel |
| the stage-split `/defeat-threat` workflow files saved to `.claude/workflows/` (Stage A + Stage B), plus an optional one-line `install.sh` copy to propagate them to consumer projects | the executable `/defeat-threat` workflow (the VEHICLE) | **DEPENDENT on AUTHORING EFFORT, not missing infra — see §2.5 + §6 HS-1.** Workflow deploy is built-in runtime infra (save via `/workflows` press `s`); the missing piece is the substantial, arc-sized work of authoring + battle-testing the stage-split workflow (the runtime forbids mid-run input, forcing the Stage A→ratify→Stage B split). |

### 2.5 Tier-2 is separable by AUTHORING EFFORT, not missing infra (graceful degradation)

**Ground truth at HEAD (web-verified vs https://code.claude.com/docs/en/workflows, 2026-06-04):** the workflow-composer SKILL is SHIPPED CANON (Arc 53 / `c6ae899` / git-tracked / `install.sh:218` inside `SKILL_NAMES`), so the *composition guidance* — how to author a goal-locked workflow — is deployed and usable today. **Workflow DEPLOY is built-in runtime infrastructure, not something h2z must build:** a workflow is saved via `/workflows` → select the run → press `s` to `.claude/workflows/` (project, repo-shared) OR `~/.claude/workflows/` (personal), and the runtime auto-discovers it as a `/<name>` command in future sessions. **There is NO registry and NO `WORKFLOW_NAMES` array** — a workflow is just a file in `.claude/workflows/` the runtime discovers. (The earlier "no `WORKFLOW_NAMES` array / no deploy case in `install.sh`" observation is TRUE but IRRELEVANT: you do not need `install.sh` to run a workflow; `install.sh`'s only possible role is an optional one-line copy to propagate `/defeat-threat` to consumer projects' `.claude/workflows/`, the same pattern as skills/modules — trivial.) `args` parameterization works as §2.3 assumes (docs: "Pass input to a saved workflow"). So what makes Tier-2 separable is **AUTHORING EFFORT**, not a missing deploy mechanism. h2z's build arc therefore has a **two-deliverable split** that degrades gracefully:

- **Tier 1 — discipline + pattern (independent of any script):** the trigger predicate (§2.1), STOP+SURFACE (§2.2), the escalate-don't-inline-patch rule, and the *documented workflow pattern* (§2.3 as a spec) can ship as canon NOW. With no deployable script, the response degrades to **the classic PLINY-run gauntlet dispatched as its own dedicated arc** whose single ratified goal is "defeat M\<n\>" — same goal-lock property, hand-orchestrated by PLINY instead of script-orchestrated. This is the graceful-degradation path, and it is the load-bearing reason Tier-1 is decouplable: **the anti-drift / MAJOR-1-closing property comes from the GOAL being the whole arc, which PLINY enforces with NO script at all.** Tier-1 does not depend on the composer SKILL *or* on the executable workflow; it depends only on PLINY honoring the dedicated-arc-per-threat discipline.
- **Tier 2 — executable `/defeat-threat` workflow (depends on AUTHORING EFFORT, an arc/team-sized build):** the *script* form (the `args`-parameterized, save-once-reuse-per-threat vehicle) is blocked NOT by infra but by the substantial work of authoring it faithfully. The runtime **forbids mid-run human input** (docs: "No mid-run user input… For sign-off between stages, run each stage as its own workflow"), so a gauntlet-faithful `/defeat-threat` carrying the §2.3 HARD STOP cannot be one script: it must be **SPLIT into stage-workflows** (Stage A: STRABO→DAEDALUS→ARGUS → return → human ratifies → Stage B: ADA→VERA→CATO), each schema-wired, with the cross-stage threat-coverage object threaded through `args`, and the whole thing battle-tested. That is arc/team-sized work, properly its own workflow-build arc — the first arc of the **debloat-via-workflows initiative** — not a trivial add to this round.

**RECOMMENDATION (HS-1):** ship h2z's BUILD arc in **Tier 1 first, decoupled** — the discipline + pattern carry the load-bearing anti-drift property and require neither the composer nor an executable script (PLINY hand-orchestrates the dedicated goal-locked arc). Sequence the Tier-2 executable workflow as a *follow-on* arc gated on the **AUTHORING EFFORT** of the stage-split `/defeat-threat` workflow (Stage A→ratify→Stage B, schema-wired + battle-tested) — folded into the debloat-via-workflows initiative as its first arc. This avoids hanging Tier-1 on a Tier-2-only dependency and ships the property that closes MAJOR-1 immediately. Surfaced as a HARD-STOP ratification item (§6 HS-1) for PRINCIPAL decision.

### 2.6 Threat→mitigation map for THIS arc (§35.4 / §6.12 — A3 author duty)

**Classification: `not threat-ratified (process change, no runtime attack path)` — PROPOSED; ARGUS to CONFIRM.**

h2z builds a remediation **MECHANISM** (a trigger discipline + an escalation pattern + an orchestration vehicle), not a runtime mitigation. It introduces no credential flow, no PRINCIPAL-gate beyond the spawn-authorization, no runtime-exploitable surface; the artifacts are canon markdown + an orchestration script that itself runs no privileged operation. No named threat M\<n\> attaches to any change h2z makes — h2z is the machinery that DEFEATS named threats in *other* arcs, the same self-reference class as Arc A and Arc B (§35.5 carve-out: "the threat-defeat hardening arcs themselves… carved out… process / role-file changes with NO runtime attack path"). Per §35.5 the carve-out is **not self-asserted** — I PROPOSE it; ARGUS CONFIRMS at critique time; I cannot self-grant it. Consequently this design's §3 verification probes are NOT threat-anchored probes (none required for a carved-out arc per §6.13) — they falsify the BUILD's correctness, not a runtime threat-defeat.

---

## 3. Verification probes (how a future VERA would falsify the BUILD)

These probes target the **Tier-1 build deliverable** (discipline + pattern as canon). They are runnable grep/file/skill checks against the future build's diff; paths are repo-relative from repo root and use `substrate/...` (the yfv carry-forward). Per-seat patterns are anchored to each seat's file so a probe cannot mechanically pass by matching only one seat's wording (the second yfv carry-forward). Probe-ids are stable so a verdict can cite them.

**Canon-presence (the discipline shipped):**
- **P1 (trigger predicate present, in op-disc):** `grep -n 'surfaced-but-not-yet-defeated' substrate/operating-disciplines.md` → ≥1 hit inside the new §36 block. AND `grep -nc 'TRIGGER' substrate/operating-disciplines.md` increases vs. main (the predicate is defined, not merely referenced).
- **P2 (predicate reuses §35.1, no new criticality scale):** within the new §36 block, `grep -n 'M<n>' substrate/operating-disciplines.md` and `grep -n '§35.1' substrate/operating-disciplines.md` both hit; AND `grep -in 'is this critical\|criticality score\|severity scale' substrate/operating-disciplines.md` → **0 hits in §36** (no fuzzy criticality judgment introduced).
- **P3 (both trigger shapes T-a/T-b present):** in §36, grep finds BOTH `defeats_via_probe` (T-a, the executed-probe-absence shape) AND `map-present-but-probe-absent` OR `no threat-anchored probe` (T-b). A build that ships only one shape fails P3.

**Escalate-don't-inline-patch (the load-bearing rule), anchored per seat:**
- **P4 (PLINY owns escalation — anchored to MAJOR_PLINY.md):** `grep -n 'remediation workflow' substrate/MAJOR_PLINY.md` → ≥1 hit; AND the same file states the inline-re-dispatch is forbidden on TRIGGER (`grep -in 'do not\|don.t' substrate/MAJOR_PLINY.md` near a `remediation`/`inline` mention). Must hit in **MAJOR_PLINY.md specifically**, not only op-disc.
- **P5 (PRINCIPAL-surface payload — anchored to MAJOR_POLYBIUS.md):** `grep -n 'THREAT-REMEDIATION TRIGGER\|DECISION REQUIRED' substrate/MAJOR_POLYBIUS.md` → ≥1 hit; AND `grep -n 'authorize' substrate/MAJOR_POLYBIUS.md` near it (the spawn-authorization gate is in POLYBIUS, the PRINCIPAL-channel owner — not in op-disc).
- **P5-anchor-guard:** P4 and P5 must hit in their *named distinct files* — re-run each grep with the OTHER file path and confirm the seat-specific string does NOT appear there (e.g. `THREAT-REMEDIATION TRIGGER` payload is in POLYBIUS, not PLINY). This is the anti-single-seat-wording guard: a build that drops one identical block into one file and cross-references it must still place each seat's distinct duty in that seat's file.

**Goal-lock / B2 success criterion (the property that closes MAJOR-1):**
- **P6 (success criterion is the executed-probe assertion, not a sentence):** the §36 / pattern spec states the workflow's success gate as `defeats_via_probe ∈ probes_executed` (or equivalent executed-probe binding) — `grep -n 'probes_executed' <the canon file the build chose>` hits within the success-criterion definition. A spec whose success gate is a writable assertion (no executed-probe requirement) fails P6.
- **P7 (cross-ref integrity to the shipped B2 surfaces):** the new canon cites the four shipped Arc-B seat surfaces by section — `grep -n 'CAPTAIN_VERA.md.*§5.2\|CAPTAIN_DAEDALUS.md.*§6.13\|CAPTAIN_ARGUS.md.*§6.9\|MAJOR_POLYBIUS.md.*§4.3.2' <canon file>` → all four resolve (the response layer correctly binds to its detection sources).

**Carve-out + honesty (the §35.5 / MAJOR-3 boundary):**
- **P8 (carve-out classification recorded, ARGUS-confirmable):** `grep -n 'not threat-ratified (process change, no runtime attack path)' <h2z build's design/verdict surface>` → present; AND the build did NOT introduce a threat-anchored probe FOR h2z itself (`grep -in 'threat-anchored probe' <h2z's own verification artifacts>` → describes the pattern it teaches, not a probe defeating an h2z runtime threat — there is none).
- **P9 (honest-claim boundary preserved — no enumeration overclaim):** `grep -in 'enumerat' substrate/operating-disciplines.md` in §36 → states threat-ENUMERATION completeness remains ARGUS's unmechanized residual; AND `grep -in 'all threats\|every threat is defeated\|catches.*unnamed' §36` → **0 hits** (h2z does NOT claim to catch un-named threats). A build that overclaims past named-threat coverage fails P9.

**Dependency-honesty (the Tier-2 separability reason):**
- **P10 (Tier-2 separability named correctly, not assumed):** the h2z canon / design states the executable `/defeat-threat` workflow is separable because of **AUTHORING EFFORT** — specifically that the runtime forbids mid-run human input, forcing a STAGE-SPLIT (Stage A → human ratify → Stage B) for the HARD STOP — NOT because of missing deploy infrastructure (workflow deploy is built-in; there is no `WORKFLOW_NAMES` array to build), and that Tier-1 degrades to a classic PLINY-run dedicated arc with no script. `grep -in 'authoring effort\|stage-split\|stage workflow\|mid-run\|debloat-via-workflows\|degrade' <h2z build surface>` confirms the reason is documented correctly. A build that re-states the stale "depends on workflow-DEPLOY infrastructure / `WORKFLOW_NAMES` array that does not exist" framing fails P10 — `grep -in 'WORKFLOW_NAMES\|deploy infrastructure does not exist\|no .*deploy case' <h2z build surface>` → **0 hits** (the stale infra premise must not survive into the shipped canon).

**Authorship guard:**
- **P11 (authorship):** every file the build touches with an author-like field names `Denson Smith`; `grep -rn 'author:' <changed files>` shows no other name introduced. (Universal §8 guard.)

---

## 4. Self-assessed weak points (feeds ARGUS)

- **WP1 — h2z is a RESPONSE layer riding on Arc-A/Arc-B detection; if those detectors miss a threat, h2z never triggers.** h2z does not enumerate threats — it reacts to threats ARGUS already named (the §35.1/§35.5 honest-claim boundary). A threat no one names is invisible to h2z, exactly as it is to Arc A/B. *Why this shape anyway:* this is the correct boundary, not a bug — claiming h2z catches un-named threats would be the precise overclaim §35.5 forbids and external-review MAJOR-3 warns against. The weak point is real but it is the *designed* limit; P9 enforces that the canon states it explicitly rather than smoothing it.
- **WP2 — The Tier-2 executable workflow's anti-drift property is only as strong as the goal-lock the workflow-composer schema enforces; an LLM seat inside the workflow can still return a plausible-but-false `threat_coverage` body.** The B2 keystone (executed-probe binding) is *skill-tool-enforced only for the empty-binding sub-check* (declared-mitigations ⇒ ≥1 probe-id, exit 4); the `defeats_via_probe ∈ probes_executed` AND "probe drove the MAPPED attack path" sub-checks are **seat-side greps** (VERA/CATO/POLYBIUS §4.3.2), not tool-strength. So a workflow could mechanically satisfy the exit-4 binding with a probe-id that did not exercise the real attack path. *Why this shape anyway:* this is the SAME residual the shipped Arc B already carries and names honestly (`CAPTAIN_VERA.md` §5.2 "do not assume tool-strength enforcement that does not exist") — h2z inherits it, does not worsen it, and the POLYBIUS §4.3.2 relay/close alignment check is the redundant net (`stoa--myd`). The fix is to require the workflow's review-surface to carry the cited probe's recorded output so the HARD-STOP human reviewer re-derives the attack-path-exercised claim — baked into §2.3's return shape. Flagging so ARGUS weighs whether Tier-2 needs more than the inherited Arc-B enforcement.
- **WP3 — The escalate-don't-inline-patch rule could itself cause arc-thrash:** every named-threat finding now spawns a dedicated arc + a PRINCIPAL HARD STOP, which is heavier than an inline ADA re-dispatch. On a high-threat-density arc this is many stops. *Why this shape anyway:* a security bug IS the load-bearing human-attention moment (the "direction is scarce" thesis) — the cost is the point, not waste; and the `args`-parameterized `/defeat-threat` workflow makes each remediation cheap to *run* even if each is a distinct *decision*. But ARGUS should weigh whether PLINY needs a batching discipline (surface N triggered threats in one HARD-STOP payload) vs. one-stop-per-threat. I did NOT design batching (kept the mechanism simple); flagging it as a deliberate omission for ARGUS to promote-or-not.
- **WP4 — The §36-vs-existing-§35 boundary is a smear risk.** h2z's discipline is adjacent to §35 (both are "named-threat" machinery); a future reader could confuse "Arc A binds mitigation→threat before build" with "h2z escalates a surfaced-undefeated threat into a dedicated arc." *Why this shape anyway:* I scoped h2z as a NEW section (§36) that explicitly cites §35 as its detection source rather than amending §35 in place, so the two stay distinguishable (Arc A/B = coverage *within* an arc; h2z = escalation *into a dedicated* arc). P7 enforces the cross-ref. ARGUS should confirm the boundary reads cleanly and recommend whether §36 or a §35.9 sub-section is the better home.

---

## 5. Out of scope (one-line reasons)

- **Threat ENUMERATION completeness** — remains ARGUS's unmechanized residual (§35.5); h2z reacts to named threats, it does not find un-named ones. Designing an enumeration mechanism is a different (likely unmechanizable) problem.
- **Authoring the executable `/defeat-threat` workflow script** — Tier-2 deliverable, separable by AUTHORING EFFORT (the runtime forbids mid-run input → a HARD-STOP-faithful workflow must be SPLIT into Stage A→ratify→Stage B, schema-wired + battle-tested — §2.5 + §6 HS-1); this DESIGN specs its shape, the follow-on workflow-build arc (first arc of the debloat-via-workflows initiative) authors the stage-split script. Workflow DEPLOY is built-in runtime infra — NOT a blocker.
- **The stage-split authoring + battle-testing of `/defeat-threat`** (Stage A / Stage B workflow files + cross-stage `args` threading + optional one-line `install.sh` propagation copy) — the genuine Tier-2 effort; a separate, arc-sized concern from h2z's discipline. The workflow-composer SKILL (composition guidance) is already shipped (Arc 53 / install.sh:218) and workflow deploy is built-in, so h2z does NOT depend on promoting the composer or on building any deploy mechanism — only on the future arc that does the substantial authoring.
- **A batching discipline for multiple simultaneous triggers** — deliberate omission (WP3); candidate follow-up if arc-thrash is observed, not pre-designed.
- **Mitigation-regresses-elsewhere detection** ("M\<n\> defeated but broke surface Y") — the §35.7 named-residual class; h2z's (b)-legit-unaffected probe-half partially covers it but full regression detection is out of scope.
- **Non-security critical issues** (a data-loss bug, a perf cliff) — h2z's trigger is deliberately the §35.1 named-threat classification ONLY, per the brief's hook. Generalizing "critical" to non-threat issues would re-introduce the fuzzy criticality judgment the design rejects; a separate arc if wanted.

---

## 6. HARD-STOP ratification list (floor-manager → user-tier POLYBIUS → PRINCIPAL)

The following required ratification BEFORE any build arc is dispatched. **All five (HS-1…HS-5) were RATIFIED by the PRINCIPAL on 2026-06-04** (recorded inline below per item).

- **HS-1 (build-order / dependency — RATIFIED = Option 1; dependency fact CORRECTED).** **RATIFIED:** ship h2z BUILD in **Tier 1 first (discipline + pattern as canon), decoupled** — Tier-1 ships NOW and closes the round (`stoa--ikr`); the Tier-2 executable `/defeat-threat` workflow becomes the **first arc of the debloat-via-workflows initiative**, NOT this round. *Corrected fact (web-verified vs https://code.claude.com/docs/en/workflows, 2026-06-04):* the workflow-composer SKILL is already shipped canon (Arc 53 / `c6ae899` / `install.sh:218`) AND **workflow DEPLOY is built-in runtime infra** — a workflow is saved via `/workflows` press `s` to `.claude/workflows/` (project) or `~/.claude/workflows/` (personal) and auto-discovered as `/<name>`; there is **no `WORKFLOW_NAMES` array / no registry** to build, and `install.sh` is needed only for an optional one-line propagation copy. The earlier "deploy infra does not exist" premise was FACTUALLY WRONG. *The REAL reason Tier-2 is separable:* **AUTHORING EFFORT** — the runtime forbids mid-run human input, so a gauntlet-faithful `/defeat-threat` with a HARD STOP must be SPLIT into stage-workflows (Stage A → human ratify → Stage B), schema-wired + battle-tested — arc/team-sized. *Why Tier-1 is decouplable:* the anti-drift / MAJOR-1-closing property comes from the GOAL being the whole arc (PLINY-enforceable with NO script), so Tier 1 depends on neither the composer nor any executable workflow; only Tier 2 waits, on its own future authoring arc.
- **HS-2 (§35.5 self-carve classification — I PROPOSE, ARGUS CONFIRMS).** h2z classified `not threat-ratified (process change, no runtime attack path)` (§2.6) — same class as Arc A / Arc B. This means h2z's own build carries NO threat-anchored probe (none exists to author). ARGUS must CONFIRM at critique; I cannot self-grant the carve-out. **Ratify:** is the carve-out correct (h2z has no runtime attack path)?
- **HS-3 (canon home).** §36 (new section) vs. §35.9 (sub-section of the existing threat-defeat block). I recommend §36 (h2z is the *escalation/response* layer, distinct from §35's *coverage-within-arc* layer; keeping them separate avoids the WP4 smear). **Ratify the home** before the build writes it.
- **HS-4 (arc-thrash vs. one-stop-per-threat — WP3).** The escalate-don't-inline-patch rule spawns a dedicated arc + HARD STOP per named threat. I did NOT design batching. **PRINCIPAL/ARGUS decide:** accept one-stop-per-threat (simple, recommended for N=0) vs. require a batching discipline now.
- **HS-5 (the honest-claim boundary — preserve, do not overclaim).** h2z enforces named-threat-DEFEAT as a locked goal; it explicitly does NOT claim to catch un-named threats (enumeration stays ARGUS's residual). Confirm the canon states this boundary (P9) and that the PRINCIPAL-surface payload (§2.2) does not imply broader coverage than "this named threat, defeated."
