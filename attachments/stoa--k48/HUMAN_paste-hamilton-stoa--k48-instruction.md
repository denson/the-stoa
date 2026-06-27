# ACTIVATION — MAJOR_HAMILTON (workflow architect) — arc stoa--k48 (u--9s2 Phase-2 increment 2.3)

Read `.claude/MAJOR_HAMILTON.md` and assume the **workflow-architect** role for the-stoa on arc stoa--k48. You are a design-time terminal seat answering to PLINY_the-stoa (parallel to CHIRON), under POLYBIUS_the-stoa (FM) → Polybius_the_Stoa (user-tier).

Read the authoritative spec from beadwork:
- `git show beadwork:attachments/stoa--k48/u9s2-phase2-inc3-directive.md` — the DIRECTIVE
- `bw show stoa--k48` — the charter

## On activation
Self-record to stoa--reg (`whoami` → `record-seat.ps1`) or confirm the launcher row. Post a presence-announce on stoa--k48.

## Your design focus (ONE pass — your design is folded into the build)
You own the **S0–S6 PROVISIONING WORKFLOW mechanics + the MOCK SUBSTRATE**; CHIRON owns the ownership/tier structure + the HOME. Co-design with CHIRON; PLINY drives the handoff to DAEDALUS who formalizes both.

Deliver:
1. **The S0–S6 workflow** (design-formal §4) — ordered (S0 isolation before any S2 key before any S3/S5 serving), **idempotent/re-runnable** (every step create-or-get), **fail-closed** (any failure aborts the remainder; S2c blocks on an unpopulated slot, never improvises a value). The emit-then-apply split: the workflow EMITS a value-free spec; the applier executes the credential-bearing steps.
2. **THE MOCK / DRY-RUN SUBSTRATE (load-bearing)** — design it so (a) the DoD is **machine-checkable** (the worked examples prospector/scienceclaw/labstat_bls mock-emit their correct value-free spec from the 2.1 resolved set), AND (b) the **TRIPWIRE is STRUCTURALLY honored** — the test path **CANNOT reach real infra** (no real `gcloud`/`railway`/card call is even possible in the mock path). This structural impossibility is the strongest form of the TRIPWIRE.
3. **The human-in-the-loop credential-acquisition choreography** — the deploy-help pattern library (the agent drives a browser to the dashboard edge → a clickable link opens that dashboard in a browser the agent cannot see → the human generates the secret privately → the agent helps deploy via OS-keyring paste-script / Railway-CLI / Railway-UI walkthrough). Build-machine browser+computer-use is available-by-construction (Grand policy); no optional fallback. This is the applier UX shape — it provisions NOTHING real in 2.3.

## Hard constraints (non-negotiable)
- **TRIPWIRE:** the mock substrate must make real-infra reach structurally impossible in the test path; the deploy-help choreography is designed but exercised against mock dashboards only.
- **CREDENTIAL-DISCIPLINE:** value-free emit (slot names); `railway-keyring-deploy` applier (keyring→ENV/STDIN, never stdout/argv/disk); no agent holds values.

## Reuse sources (PATH)
`railway-keyring-deploy` (the keyring-local Railway deploy workflow) is at the **USER-TIER** path `C:\Users\denso\.claude\skills\railway-keyring-deploy\`; `credential-discipline` is in-repo (`.claude/skills/credential-discipline/`). Read both for the workflow reference.

## Surface UP
Route the mock-substrate design + the TRIPWIRE-structural-honoring + any load-bearing workflow decisions UP through PLINY → FM → Polybius_the_Stoa. Hand your design to PLINY for the DAEDALUS formalization.

## Compaction recovery
Re-read `.claude/MAJOR_HAMILTON.md`, this brief (`git show beadwork:attachments/stoa--k48/HUMAN_paste-hamilton-stoa--k48-instruction.md`), `bw show stoa--k48`, the directive.

— authored by Polybius_the_Stoa | sid 990b0750-5572-4836-b9c7-18d626a12e96 | the-stoa
