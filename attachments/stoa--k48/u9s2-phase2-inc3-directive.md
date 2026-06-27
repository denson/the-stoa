---
author: Denson Smith
ticket: stoa--k48 (u--9s2 Phase-2 increment 2.3)
owner: Polybius_the_Stoa (user-tier forge domain) — supervising; reports up to Polybius the Grand at u--9s2
seat-to-launch: POLYBIUS_the-stoa (FM) + PLINY_the-stoa + MAJOR_CHIRON + MAJOR_HAMILTON — composition custom-agent+workflow, full gauntlet
status: DIRECTIVE — NOMOS-on-directive gate pending before launch
as_of: 2026-06-27
---

# u--9s2 Phase-2 — increment 2.3 DIRECTIVE: the provisioning choreography (ONE pass)

## 0. Frame

Phase-1 design + increments 2.1 (resolve/discovery core) + 2.2 (SUGGEST front-door) are SHIPPED to main
and Grand-gated PASS. **2.3 is the provisioning choreography** — the runnable `repo → DB → per-builder
GCP project/SA → Railway → Tailscale-mesh deploy` — and it is **the FIRST real-infra / credentialed
increment.**

**Grand's PROCESS CHANGE (u--9s2, 2026-06-27T03:37:41Z): run 2.3 as ONE pass.** CHIRON+HAMILTON design
the choreography **folded into the build** (no separate pre-build design-gate); relay the COMPLETE
increment (design + build) up for Grand's **single gate**. The single gate IS the credential-discipline +
provisioning-plan + spend-cap review, and it lands BEFORE 2.4's real run.

**This directive is the WHAT.** The HOW — the buildable choreography against `newswire-builder-setup` +
`railway-keyring-deploy` — is CHIRON+HAMILTON's design, gauntlet-built in the same pass.

## 1. The two HARD boundaries (read before anything)

**TRIPWIRE (load-bearing).** 2.3 builds + tests the choreography against **MOCK / throwaway / dry-run
ONLY**. If any build/test step would touch **REAL infrastructure, REAL credentials, or spend REAL
money** — STOP and surface to Polybius_the_Stoa, who flags Grand FIRST. Do **NOT** spend real money or
handle real credentials mid-build. The real customer-builder provisioning (real GCP project + real
prepaid card + real Railway deploy) is **increment 2.4 (scienceclaw)**, gated separately by Grand.

**CREDENTIAL-DISCIPLINE (load-bearing).** No agent ever holds a credential VALUE. The choreography
**emits a value-free provisioning spec** (slot names, never values); a credential-disciplined applier
(CI-via-WIF, or a human one-shot per `railway-keyring-deploy`: secrets in the OS keyring, read into the
CLI subprocess via ENV/STDIN, never agent stdout/argv/transcript/disk) executes the credential-bearing
steps. Per-builder GCP **project** + per-builder **prepaid card/billing** = the **hard spend cap** (NOT a
GCP budget feature) — the locked carry-forward.

## 2. Deliverable (the WHAT)

The runnable **provisioning choreography** as the `builder-deploy` skill — design-formal §4 **S0–S6**,
generalizing the `newswire-builder-setup` skill (~60% done; the reuse source) and reusing
`railway-keyring-deploy` + `credential-discipline`. It consumes the **2.1 resolved set** (+ 2.2 SUGGEST
front-door) and **emits the per-builder provisioning spec**:

- **S0** — isolation scaffold: per-builder GCP **project** + bijective **SA** + the budget boundary
  (§5.B: prepaid-card hard cap + GCP alert/quota soft layer). The LOCK that precedes any key.
- **S1** — GCP API enablement (`kind == gcp_api`): enable + grant SA the API role.
- **S2** — secret slot materialization (`kind ∈ {gcp_secret, thirdparty_rest_key}`): slot + per-secret
  `secretAccessor`; **S2c value population is the HUMAN / credential-discipline GATE** (blocks, never
  improvises a value).
- **S3** — Railway provisioning (`railway_var` + secret-backed vars): db service (baked-init image,
  §6) + serving service; vars via **STDIN only**; this builder's SA key only.
- **S4** — DB extension application (`db_extension`): the resolved `CREATE EXTENSION` set (pgvector
  baseline; postgis iff resolved — §6 base-image DECIDE-C).
- **S5** — agent-access layer (the §7 **SHAPE**, T1, fixed): mesh-API scaffold (`tailscaled` →
  `tailscale serve` → 0600 AF_UNIX socket → in-mesh trigger; serve-injected identity header;
  deny-by-default + `<BUILDER>_OPERATORS` allowlist; Funnel OFF) + the CLI-client-skill template.
  Domain VERBS/data are the project-seat T3 product — NOT built here.
- **S6** — verify (idempotent re-run = no-op + health probe).

**Global properties (§4):** ordered (S0 isolation before any S2 key before any S3/S5 serving),
idempotent/re-runnable, fail-closed (any failure aborts the remainder; S2c blocks).

**The human-in-the-loop credential-acquisition choreography** (the PRINCIPAL's 2026-06-26 design input,
recorded at u--9s2): default UX = the agent drives a browser to the dashboard edge → a clickable link
opens the SAME dashboard in a browser the agent CANNOT see (human generates the secret privately) → the
agent helps DEPLOY via a small repeated-pattern library (OS-keyring paste-script / Railway-CLI /
Railway-UI walkthrough). Build-machine browser+computer-use is available-by-construction (Grand policy);
no optional fallback. **This is design + the value-free applier shape; it provisions NOTHING real in 2.3.**

## 3. The relay-up deliverables (Grand's single gate REQUIRES these)

The completed-2.3 relay-up to Grand MUST include:
1. **The PROVISIONING CHECKLIST** — exactly what the PRINCIPAL provisions for a real builder, step by
   step, with WHEN: per-builder **GCP project** + **prepaid card** + **billing account** + **Railway**
   account + **Tailscale**. (This is the gate that tells the PRINCIPAL precisely what to set up for 2.4.)
2. **The credential-discipline ATTESTATION** — NO agent holds credentials; `railway-keyring-deploy` is
   the local-agent secret path; per-builder project+card = the hard spend cap; the emit step is value-free.
3. **The TRIPWIRE-HELD attestation** — proof the 2.3 build/test touched zero real infra/creds/money
   (the test path is mock/dry-run; no `gcloud`/`railway` against real projects; no real card).

## 4. Decisions to RESOLVE / fold in this pass

1. **The permanent builder-deploy skill HOME** (deferred from 2.1, recorded at `stoa--wmu`). 2.3 has a
   near consumer (scienceclaw at 2.4) — RESOLVE A (the-stoa forge-owned) vs B (standalone
   builder-tooling). CHIRON proposes; Polybius_the_Stoa ratifies; escalate to Grand if load-bearing.
2. **`stoa--jd5`** (the pyproject parent-relative package-data glob) — the named 2.3 packaging
   prerequisite; fold the fix so the skill packages correctly.
3. **The mock/dry-run substrate** — how the choreography is exercised without real infra (a mock
   GCP/Railway layer, or a `--dry-run` emit-only mode). CHIRON+HAMILTON design it so the DoD is
   machine-checkable AND the TRIPWIRE is structurally honored (the test path CANNOT reach real infra).

## 5. Definition of Done (machine-checkable, MOCK-not-real)

1. The choreography runs **end-to-end in dry-run/mock** and emits the correct **value-free provisioning
   spec** for the §8 worked examples (prospector / scienceclaw / labstat_bls) from their 2.1 resolved sets.
2. **S0–S6 ordered / idempotent / fail-closed** (§4 global properties) — verified on the mock substrate;
   S2c blocks on an unpopulated slot (never improvises a value).
3. **Value-free emit** — the emitted spec contains slot NAMES only, zero credential values (grep-provable).
4. **Per-builder isolation** structurally correct — one project ⟷ one builder; SA scope = the mechanical
   union of scope-bearing resolved entries; per-secret accessor; the prepaid-card budget boundary represented.
5. **Agent-access layer SHAPE** scaffold stands up on the mock (domain-empty, secured) — no domain verb leaks (the §7 boundary test).
6. **TRIPWIRE HELD** — the entire test path is mock/dry-run; NO real `gcloud`/`railway`/credential/card
   call anywhere in the build or test (verifiable, attestable).
7. **The §3 relay-up deliverables authored** — provisioning checklist + credential-discipline attestation + TRIPWIRE-held attestation.
8. **HOME resolved** (§4.1) + **stoa--jd5 folded** (§4.2).
9. **Full existing the-stoa suite GREEN** (builder-deploy-core tests + gen-data + app) — the 2.1/2.2 core unbroken.
10. **Authorship** `author: Denson Smith` on every artifact; zero foreign field.

## 6. One pass + gauntlet + chain

- **CHAIN:** PRINCIPAL → Polybius the Grand → **Polybius_the_Stoa (supervising)** → POLYBIUS_the-stoa (FM,
  independent verify + relay) → PLINY_the-stoa (orchestrator) → CAPTAINs. PLINY surfaces to the FM.
- **COMPOSITION: custom-agent+workflow** — FM + PLINY + **MAJOR_CHIRON** (choreography ownership/structure)
  + **MAJOR_HAMILTON** (the S0–S6 provisioning workflow). The architects design **folded into the build**
  (Grand's process change — NO separate pre-build design-gate).
- **GAUNTLET: FULL, NO WAIVER** — DAEDALUS (formalize the CHIRON+HAMILTON design into the buildable spec)
  → ARGUS (cold-audit; pressure the TRIPWIRE + credential-discipline + per-builder isolation) → ADA (build
  against the mock substrate) → VERA (re-run the DoD + the FULL existing suite + a TRIPWIRE probe that no
  real-infra path is reachable) → CATO (cold-read) → NOMOS (audit vs design-formal §4–§7 + this directive).
- **Relay the COMPLETE increment (design + build) UP to Grand's single gate** with the §3 deliverables.

## 7. Dogfood the liveness fix (op-disc §38)

- **Record every seat to `stoa--reg` on spawn** (the launcher does this for the 4 launched seats).
- **WRITE THE STAND-DOWN status on CLOSE** — at the 2.3 close, flip this team's seats to `dead` in the
  registry. The registry was found **stale-lying** because prior teams closed without writing stand-down
  (the 2.2 FM/PLINY rows lied `alive`); make this team's close HONEST. (Recording an observed close is
  honest WHO-roster maintenance, consistent with §38's ping-is-liveness model — not a passive sweep.)

## 8. Reporting

Polybius_the_Stoa supervises from user-tier and relays the COMPLETE 2.3 increment UP to Polybius the
Grand's single gate (u--9s2) — with the §3 provisioning checklist + credential-discipline attestation +
TRIPWIRE-held attestation. **PRINCIPAL provisions NOTHING in 2.3** (mock-only); the real provisioning is
increment 2.4 (scienceclaw), gated separately.
