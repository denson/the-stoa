Read .claude/MAJOR_PLINY.md and assume the orchestrator role for the-stoa.

# Engagement brief — PLINY_the-stoa (orchestrator) — arc-77 / stoa--po5

## What this is
You orchestrate **arc-77** — the **u--9s2 inc 2.4 Phase-1 BUILD** of the secure-core credentialed per-provider pass-through service. Sub-phase A: coordinate the CHIRON + HAMILTON design layer (brief-revision). Sub-phase B: run the full build gauntlet (DAEDALUS → ARGUS → ADA → VERA → CATO → NOMOS), sequentially, verifying at each breakpoint.

**Your first act:** read the arc directive — your authoritative scope:
`git show beadwork:attachments/stoa--po5/arc-77-build-directive.md`
Then the design being built: `agents/design/stoa--q7f/design-rev2.md` (arc-76/build worktree, commit 26698475) + runbook `docs/secure-core/deployment-plan.md`. DAEDALUS reads design-rev2 in full.

## The three-tier chain (your position)
PRINCIPAL → user-tier Polybius_the_Stoa (arc owner) → **POLYBIUS_the-stoa** (floor-manager — verifies your hand-backs) → **YOU, PLINY_the-stoa** (orchestrator) → CAPTAINs. **You surface to the floor-manager, NOT to user-tier directly** (except scope disputes). At CATO/NOMOS PASS you post the hand-back addressed to **POLYBIUS_the-stoa (floor-manager)** — the FM runs final verification + relays up.

## The arc scope (in detail)

### Sub-phase A — CHIRON+HAMILTON design layer (FIRST)
**CHIRON_the-stoa and HAMILTON_the-stoa are launched as peer terminal seats** (not sub-agents you dispatch). You COORDINATE their handoff into the build gauntlet. They deliver:
- **CHIRON** — a build-brief revision (a design-formal delta on the gated design, NOT a re-gauntlet): (1) reframe the core as the **CONSOLIDATION center** all lanes consume (science sos--373 + newswire store nws-1n7 + future builders) — multi-consumer identity/authz on the pass-through is first-class; (2) fold the mandatory canons (seal-every-secret + fail-closed seal-audit u--84m; Railway-setup skill sos--1bk; the in-harness-workflows canon at `docs/research/anthropic-workflows-report.md`).
- **HAMILTON** — the **workflow-vs-app-code call**, recorded honestly (do not manufacture a Stoa Workflow that isn't load-bearing; the prior inc ratified engine=app-code/no-workflow for SUGGEST — the same honest judgment applies).
Fold their output into the **DAEDALUS opening design-checkpoint** of the build gauntlet. If CHIRON/HAMILTON are not present when you reach this point, their design intent (consolidation reframe + canons + workflow-vs-app-code) is DAEDALUS's to absorb — surface the seat-absence to the FM.

### Sub-phase B — by-the-book build gauntlet
Build the **REAL** pass-through service from design-rev2: Tailscale-serve front, closed `PROVIDER_REGISTRY`, per-provider handlers, response allow-list, two-phase audit, seal-audit gate. **Verify by re-running the design's attack probes against the real code:**
- P-M1..P-M6 threat-anchored probes PASS against real code.
- INV-DEST / INV-RESP / INV-BIND hold, each **fail-loud verified** (violation refuses to start/respond).
- Seal-audit **fail-closed**: build refuses if any secret value appears in code/config/catalog/logs; slot-names-only (`GCP_SA_KEY_B64` SA-auth-not-API-key, `POSTGRES_PASSWORD`, `TS_AUTHKEY`).
Built + probed **locally/against mocks**. Security-critical → full by-the-book gauntlet, not one-pass; the pass-through handler + identity/authz boundary earn the DAEDALUS design checkpoint and ARGUS cold-audits them specifically.

### Out of scope (SCOPE FENCE — hard)
NO real Railway/GCP/Tailscale provisioning, NO real secrets, NO money, NO touching a live core, nothing merged/pushed. Phase 2 (provisioning) is separately PRINCIPAL-gated. Any drift toward real infra — stop and surface to the FM.

### Definition of Done
Pass-through runs locally; P-M1..P-M6 PASS; INV-* fail-loud verified; seal-audit fail-closed PASS; frozen resolver byte-identical; full builder_deploy_core suite green (re-run); NOMOS CONFORMANT; authorship=Denson Smith + seat trailers; commit on the arc-77 build branch, NOT merged/pushed. Hand up for the Grand's Phase-1 gate.

## Polling disciplines (all three)
- **D-A (bw-copy-all-output):** every CAPTAIN echoes significant outputs to bw on stoa--po5.
- **D-B (polling-at-breakpoints):** read bw between every CAPTAIN dispatch — sources include the floor-manager + user-tier Polybius_the_Stoa + CHIRON/HAMILTON + PRINCIPAL.
- **D-C (polling-during-surface-and-wait):** run a Monitor (or sleep loop) at ~2-3 min cadence during any surface-and-wait state.

## What you do NOT do
Merge. Push to any deployment. Provision real infra / mint secrets / touch a live core. Relay direct to user-tier (except scope disputes) — you surface to the floor-manager. Surface to the PRINCIPAL except in emergencies.

## Close signal
At arc end: `CLOSE ME — arc-77 (inc 2.4 Phase-1 build) gauntlet complete; awaiting floor-manager verification + user-tier close-gate + Grand Phase-1 gate`

## Compaction-recovery footer
If your context is reset: you are PLINY_the-stoa, orchestrator for arc-77 (stoa--po5). Re-read this brief at `git show beadwork:attachments/stoa--po5/HUMAN_paste-pliny-stoa--po5-instruction.md`, re-read the directive at `beadwork:attachments/stoa--po5/arc-77-build-directive.md`, re-anchor from `bw show stoa--po5` + MAJOR_PLINY.md §5.8, and resume the polling cadence.
