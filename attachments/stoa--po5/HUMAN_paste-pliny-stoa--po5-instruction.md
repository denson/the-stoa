Read .claude/MAJOR_PLINY.md and assume the orchestrator role for the-stoa.

# Engagement brief v2 — PLINY_the-stoa (orchestrator) — arc-77 / stoa--po5

**This is the RELAUNCH brief (v2, 2026-07-06).** The prior FM+PLINY sessions were closed by the PRINCIPAL before the build started. The composition they held on is **SETTLED**: 2-seat arc (FM + you); **there is NO CHIRON/HAMILTON phase and none will be launched; any CHIRON/HAMILTON briefs still attached to stoa--po5 are VOID.** DAEDALUS's opening design-checkpoint owns the entire design layer. Do not hold on, ask about, or surface the composition — it is not a question.

## What this is
You orchestrate **arc-77** — the **u--9s2 inc 2.4 Phase-1 BUILD** of the secure-core credentialed per-provider pass-through service: the full build gauntlet **DAEDALUS → ARGUS → ADA → VERA → CATO → NOMOS**, sequential, by-the-book (security-critical; no one-pass), verifying at each breakpoint.

**Your first act:** read the arc directive v2 — your authoritative scope:
`git show beadwork:attachments/stoa--po5/arc-77-build-directive.md`
Then the design being built: `agents/design/stoa--q7f/design-rev2.md` (arc-76/build worktree, commit 26698475 — leave that worktree untouched; it is the gated reference) + runbook `docs/secure-core/deployment-plan.md`. DAEDALUS reads design-rev2 in full.

## THE ESCALATION LADDER (PRINCIPAL-directed — strict, one-step-up, no skipping)
1. CAPTAINs escalate to **you** only.
2. **You escalate to POLYBIUS_the-stoa (FM) only** — never to user-tier Polybius_the_Stoa, never to the PRINCIPAL, no exceptions (including scope disputes: those also go to the FM, who carries them up if needed).
3. The FM escalates to user-tier; user-tier alone decides whether anything reaches the PRINCIPAL.
4. Downward: instructions reach you FROM the FM. User-tier will not address you directly.
Your terminal output is a status surface, not an ask-channel — never pose a decision or option list to the PRINCIPAL there.

## The work

### DAEDALUS's opening design-checkpoint (the whole design layer — directive §3A)
DAEDALUS folds — and ARGUS cold-audits — three things:
1. **The CONSOLIDATION reframe:** the core is the canonical center all lanes consume (science sos--373 + newswire store nws-1n7 + future builders). **Multi-consumer identity/authz on the pass-through** (operators via `Tailscale-User-Login` vs the tagged builder via App-Capabilities vs future lanes) is first-class design — the one genuinely-novel delta vs design-rev2's single-consumer shape; ARGUS audits it specifically.
2. **The three mandatory canons** (directive §3–4): seal-every-secret + **fail-closed seal-audit** (u--84m); Railway-setup skill (sos--1bk) as the Phase-2 provisioning reference; the in-harness-workflows canon (`docs/research/anthropic-workflows-report.md`).
3. **The workflow-vs-app-code call, answered inline** (default: application code — a request/response pass-through is not a Stoa Workflow, matching the prior inc's engine=app-code ratification for SUGGEST; name a workflow only if genuinely warranted).

### The build
Build the **REAL** pass-through from design-rev2: Tailscale-serve front, closed `PROVIDER_REGISTRY`, per-provider handlers, response allow-list, two-phase audit, seal-audit gate. Verify by re-running the design's own attack probes against the real code:
- **P-M1..P-M6** PASS against real code.
- **INV-DEST / INV-RESP / INV-BIND** hold, each **fail-loud verified** (violation refuses to start/respond).
- **Seal-audit fail-closed:** build refuses if any secret value appears in code/config/catalog/logs; slot-names-only (`GCP_SA_KEY_B64` SA-auth-not-API-key, `POSTGRES_PASSWORD`, `TS_AUTHKEY`).
Built + probed **locally/against mocks**. Pre-branch hygiene, then an isolated **arc-77/build** worktree off committed main HEAD (the 3 pre-existing uncommitted main changes are user-tier local state — leave untouched, outside your fence).

### Out of scope (SCOPE FENCE — hard)
NO real Railway/GCP/Tailscale provisioning, NO real secrets, NO money, NO touching a live core or the arc-76/build reference, nothing merged/pushed. Phase 2 (provisioning) is separately PRINCIPAL-gated. Any drift toward real infra — stop and escalate to the FM.

### Definition of Done
Pass-through runs locally; P-M1..P-M6 PASS; INV-* fail-loud verified; seal-audit fail-closed PASS; frozen resolver byte-identical; full builder_deploy_core suite green (re-run, not asserted); NOMOS CONFORMANT; authorship=Denson Smith + seat-identity Co-Authored-By trailers; commit on arc-77/build, NOT merged/pushed. Hand-back addressed to **POLYBIUS_the-stoa (FM)**, who verifies and relays up.

## Polling disciplines (all three)
- **D-A (bw-copy-all-output):** every CAPTAIN echoes significant outputs to bw on stoa--po5.
- **D-B (polling-at-breakpoints):** read bw between every CAPTAIN dispatch — your instruction source is the FM.
- **D-C (polling-during-surface-and-wait):** Monitor (or sleep loop) at ~2–3 min cadence during any wait.

## What you do NOT do
Merge. Push to any deployment. Provision real infra / mint secrets / touch a live core. Contact user-tier or the PRINCIPAL (see the ladder — the FM is your only up-channel). Re-open the composition (settled). Solo/one-checker close (AR-7 shape) — the full gauntlet is mandatory; no waiver exists on this arc.

## Close signal
`CLOSE ME — arc-77 (inc 2.4 Phase-1 build) gauntlet complete; awaiting floor-manager verification + user-tier close-gate + Grand Phase-1 gate`

## Compaction-recovery footer
If reset: you are PLINY_the-stoa, orchestrator for arc-77 (stoa--po5), v2 relaunch. Re-read this brief (`git show beadwork:attachments/stoa--po5/HUMAN_paste-pliny-stoa--po5-instruction.md`) + the directive v2 (`beadwork:attachments/stoa--po5/arc-77-build-directive.md`), re-anchor from `bw show stoa--po5` + MAJOR_PLINY.md §5.8, resume the cadence. The escalation ladder above governs.
