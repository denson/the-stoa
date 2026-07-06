<!-- author: Denson Smith -->

# arc-77 build directive — u--9s2 inc 2.4 Phase-1: secure-core pass-through service BUILD

**Arc:** arc-77 (fresh build decompose) · **Coordination ticket:** stoa--po5 (the-stoa) · **Design ref:** stoa--q7f
**Owner:** user-tier Polybius_the_Stoa · **Gate authority:** Polybius the Grand (u--9s2)
**Composition:** custom-agent+workflow — POLYBIUS_the-stoa (FM) + PLINY_the-stoa + CHIRON_the-stoa + HAMILTON_the-stoa + the gauntlet CAPTAINs

---

## 0. One-line

Build the REAL credentialed per-provider pass-through service from the gated inc-2.4 design (design-rev2), by-the-book gauntlet, as the CONSOLIDATION secure core every lane consumes — **no real infrastructure, no secrets, no money.**

## 1. Where this sits (context for a cold reader)

- **u--9s2 is the Grand's #1 cross-project priority** (Codex the Cartographer's map converged on u--eif; Grand adopted). Its mandate is **CONSOLIDATION**: the secure core is the **canonical center ALL lanes consume** — the science instance (sos--373), the newswire credential-free STORE (nws-1n7), and every future builder. It is **NOT** a stoa_of_science one-off; build it as the shared center.
- This arc is **Phase 1 of the approved four-phase path** (the PRINCIPAL approved the design + gave the provision-go 2026-06-28; the Grand approved this resume 2026-07-06 on u--o49):
  1. **Phase 1 (THIS ARC) — build the core SERVICE code. No real infra.**
  2. Phase 2 — provision real infra (PRINCIPAL-provisioned GCP project + prepaid-card spend-cap + Railway + Tailscale; agent-guided, PRINCIPAL mints every secret privately). *The first real money/credential action; gated separately.*
  3. Phase 3 — deploy + test the first slice (gsearch through the pass-through; embeddings DB stand-up).
  4. Phase 4 — revise the architecture + security docs = the Zeotek external-review submission.
- **Gate model:** this Phase-1 build relays UP to the Grand to **gate BEFORE Phase 2**. Nothing real happens until the Grand gates Phase 1 AND the PRINCIPAL gives an explicit Phase-2 provision-go. That boundary is intact and load-bearing.

## 2. The design being built (reference — do not re-litigate)

The gated design is **`agents/design/stoa--q7f/design-rev2.md`** (762 lines) on the **arc-76/build** worktree (commit **26698475**, not merged/pushed, intact for reference). The runbook is **`docs/secure-core/deployment-plan.md`**. Both are PRINCIPAL-approved. The build implements that design; it does not redesign it.

**What the service is (design-rev2, DC1 crux):** a per-provider **SCOPED pass-through** over a **closed server-side `PROVIDER_REGISTRY`** — a skill names a provider + a pre-registered call; the core attaches that provider's key, makes the call, returns only the declared result; the key never leaves the core. **No caller-supplied address exists**, so SSRF/open-relay is closed *by construction* (strictly stronger than an egress allowlist). Generalizes newswire-serving: `tailscaled → tailscale serve --https=443 → 0600 AF_UNIX UDS → gated handler → uvicorn`; deny-by-default; Funnel OFF; server-side creds; serve-injected identity (`Tailscale-User-Login` operators / App-Capabilities for the tagged builder). pgvector embeddings DB on the core. Builder holds ONLY a tailnet identity.

**The structural invariants (design-rev2, fail-loud):** `INV-DEST` (no caller-supplied destination constructable), `INV-RESP` (no credential byte reaches a caller — response allow-list), `INV-BIND` (a non-private network binding refuses to start). Plus the **two-phase audit** and the **M1–M6 threat-anchored probes (P-M1..P-M6)**.

## 3. The work — two sub-phases on the floor

### (A) CHIRON+HAMILTON build-brief revision — FIRST, before the build gauntlet

Revise the build brief (design-formal delta, not a re-gauntlet of the gated design) to:

1. **Reframe as the CONSOLIDATION center** — the core serves science (sos--373) + the newswire store (nws-1n7) + future builders, not stoagen alone. Multi-consumer identity/authz on the pass-through (operators vs tagged builders vs future lanes) is a first-class design concern, not a science detail.
2. **Fold the MANDATORY cookie-cutter canon (Grand-ratified 2026-07-06):**
   - **Seal-every-secret + fail-closed seal-audit** (the u--84m lesson made a gate — see §4).
   - **Railway-setup skill (sos--1bk)** as the provisioning-choreography reference the Phase-2 path will use.
   - **In-harness-workflows canon (ratified on u--o49; report at `docs/research/anthropic-workflows-report.md`):** any LLM-adjudication step runs **in-harness on subscription OAuth**, NEVER a keyed CI call, and NOT routed through `CLAUDE_CODE_OAUTH_TOKEN` for a shared pipeline (ToS = individual interactive use). HAMILTON assesses whether any step in this core warrants a Stoa Workflow vs plain application code, and records the call honestly (the prior inc ratified engine=app-code / no-workflow for SUGGEST — the same honest call applies; do not manufacture a workflow that isn't load-bearing).

Relay the revised brief posture to user-tier for awareness; the Grand gates at the built-artifact hand-back, not mid-revision.

### (B) By-the-book build gauntlet — DAEDALUS → ARGUS → ADA → VERA → CATO → NOMOS

Build the **REAL** pass-through service from design-rev2: the Tailscale-serve front, the closed `PROVIDER_REGISTRY`, the per-provider handlers, the response allow-list, the two-phase audit, and the seal-audit gate. Then **verify by re-running the design's own attack probes against the real code**:

- **P-M1..P-M6** threat-anchored probes PASS against real code.
- **INV-DEST / INV-RESP / INV-BIND** hold, each **fail-loud verified** (a violation refuses to start / refuses to respond, it does not warn-and-continue).
- Concretely, at minimum: no caller-supplied address is constructable; no credential byte reaches a caller; a non-private network binding refuses to start.

Built + probed **locally / against mocks**. This is security-critical → **full by-the-book gauntlet**, not one-pass; the pass-through handler + the identity/authz boundary earn the DAEDALUS design checkpoint and ARGUS cold-audits them specifically.

## 4. Seal-audit — the new mandatory fail-closed gate

Extend the design's value-free discipline (slot NAMES only; `assert_value_free`) into a **fail-closed seal-audit**: the build/emit **refuses** if any real secret value appears in code, config, catalog TOMLs, or logs. Every secret slot stays a NAME only — `GCP_SA_KEY_B64` (Vertex SA-auth, NOT an API key), `POSTGRES_PASSWORD`, `TS_AUTHKEY` (tagged, reusable). This is the **u--84m lesson** ("seal every secret; the audit fails closed") made a gate this arc must pass. Fold the Grand's GCP notes (stoa--re9): Vertex SA covers embeddings+search+generative (NOT Maps); no AI-Studio API-key path; prepaid card = the only hard spend cap (Phase-2 concern).

## 5. SCOPE FENCE (hard)

**DESIGN-REVISION + BUILD-CODE + VERIFY-AGAINST-DESIGN only.** NO real Railway/GCP/Tailscale provisioning. NO real secrets (mint nothing). NO touching any live core. NO money. Nothing merged, nothing pushed to any deployment. Any CAPTAIN drift toward real infra — the FM stops it and surfaces up. The Phase-2 provision boundary is a separate PRINCIPAL-gated step; this arc does not cross it.

## 6. Definition of Done

- The pass-through service **exists and runs locally** (against mocks).
- **All P-M1..P-M6 probes PASS** against the real code; **INV-DEST/INV-RESP/INV-BIND** hold and are fail-loud verified.
- **Seal-audit fail-closed PASS** (no secret value anywhere; slot-names-only).
- Frozen resolver byte-identical; the full `builder_deploy_core` suite green (re-run, not asserted).
- **NOMOS CONFORMANT** on the build; **authorship = Denson Smith** with the seat-identity Co-Authored-By trailers (§28); commit on the arc-77 build branch, **NOT merged, NOT pushed**.
- The CHIRON+HAMILTON brief-revision folded the consolidation reframe + the three canons; HAMILTON's workflow-vs-app-code call recorded.
- **Relay the Phase-1 build UP to the Grand** (via user-tier Polybius_the_Stoa) for the Phase-1 gate before Phase 2.

## 7. Chain of command

PRINCIPAL → **user-tier Polybius_the_Stoa** (arc owner; relays to the Grand) → **POLYBIUS_the-stoa** (FM; independent verification + relay) → **PLINY_the-stoa** (orchestrator; dispatches CHIRON/HAMILTON then the gauntlet CAPTAINs) → CAPTAINs. Hand-up at build-complete goes to the FM → user-tier → the Grand. Escalations/scope disputes go UP the same chain, never to the PRINCIPAL directly except emergencies.
