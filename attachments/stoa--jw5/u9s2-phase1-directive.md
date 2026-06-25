# DIRECTIVE — u--9s2 Phase 1: composable key-provisioning model + per-builder manifest

**Arc home (team):** `stoa--jw5` (the-stoa beadwork). **User-tier arc:** `u--9s2`.
**Forged by:** Polybius_the_Stoa (sid 990b0750), supervising from user-tier.
**Chain:** PRINCIPAL → Polybius the Grand → Polybius_the_Stoa (supervise) →
POLYBIUS_the-stoa (FM) → PLINY_the-stoa → MAJOR_CHIRON + MAJOR_HAMILTON (design) →
full gauntlet (DAEDALUS → ARGUS → ADA → VERA → CATO → NOMOS).
**Composition:** custom-agent+workflow. **Gauntlet:** required.

> This is a **DESIGN** arc. The deliverable is a *design*, not built code. CHIRON +
> HAMILTON design the choreography; the gauntlet hardens the design; Polybius the
> Grand gates the Phase-1 design **before any build** (a later arc). PRINCIPAL
> provisions **nothing** on Railway/GCP until this model defines what to provision.

---

## 1. Mission (the WHAT)

Design the **composable key/API/extension provisioning model** + the **per-builder
manifest schema** for the builder-deploy cookie-cutter (u--9s2). The model is the
**gate** that tells the PRINCIPAL exactly which keys/APIs/DB-extensions to set up on
Railway/GCP **per project** — because that set **differs by project**, and a blind
newswire-template copy would provision the wrong set (e.g. geo keys for a
document-only project, or vice-versa).

The model is a **COMPOSITION mechanism driven by each builder's manifest**, NOT a
fixed table. Shape (Grand's four 2026-06-25 refinements, consolidated):

**CATEGORY-TEMPLATE + PER-DEPLOYMENT-DELTA composition:**

1. **UNIVERSAL BASELINE** — what nearly every deployment needs:
   - Gemini **EMBEDDING** + Gemini **SEARCH** (gsearch), plus the DB credential set.
2. **CATEGORY TEMPLATES** — a standard key/API/extension LIST per category, reused
   *whole*, and **extensible to new categories**. At minimum:
   - **geospatial** = baseline + Google **Maps** + **PostGIS**.
   - **document-consuming** = baseline + **pgvector** + **document-parsing**.
3. **PER-DEPLOYMENT DELTA** — a *short* add/omit list off the category template:
   a few project-specific keys REQUIRED (added) and/or standard keys OMITTED.
4. **MANIFEST (per-builder, terse):** declares `{category + delta}`. The cookie-cutter
   **RESOLVES** the full set as `baseline + category template + delta`, then
   **PROVISIONS** it.

**Provisioning (what the resolved set drives) — per builder, ISOLATED:**
- a per-builder **GCP service account scoped to ONLY its own keys** (the
  per-builder-isolation lock — an SA never carries another builder's scope),
- the **Railway key set** for that builder,
- **GCP API enablement** for exactly the resolved APIs,
- a **budget cap**.

**Parameterized within the model:**
- **DB extensions** — pgvector is the baseline; **PostGIS** is a per-builder toggle
  (geo-builders only), same shape as the parameterized API set.
- **Agent-access layer is FIRST-CLASS in the deployable** (not just the DB): the
  standard mesh-reachable pattern = an **API endpoint + a CLI client skill** over the
  Tailscale mesh (e.g. newswire's `/query` + the `newswire-trigger` skill). The
  *specific* skills + curated data each builder exposes are the **project-seat
  PRODUCT layer** (owned by the project seat), **NOT** the cookie-cutter.

---

## 2. Worked examples the model MUST satisfy

The design is falsified if it cannot express all three tersely:

| builder | category | delta | resolves to (illustrative) |
|---|---|---|---|
| **prospector** | geospatial | — | baseline + Maps + PostGIS |
| **scienceclaw** | document-consuming | — | baseline + pgvector + document-parsing (designed to serve ALL prospector projects for cross-field discovery — coordinate with Polybius_the_science_stoa, u--4at) |
| **labstat_bls** | document/data | `+BLS OEWS` | baseline + (doc/data template) + BLS OEWS API key (a key no other builder needs) |

The `labstat_bls` case is the load-bearing test that the **delta** mechanism is real:
a single project-specific key (BLS OEWS) rides on top of a reused category template
without bloating the template.

---

## 3. Constraints & locks (carry into the design)

- **Per-builder isolation (LOCK).** Each GCP SA is scoped to ONLY its own builder's
  keys + a budget cap. No shared, broadly-scoped SA. (ref `zeotek_newswire/SECURITY.md`,
  `u--eq6`, `newswire-builder-setup`.)
- **Agents never hold long-lived credentials** — `credential-discipline` /
  `railway-keyring-deploy` patterns apply (keyring-local for direct deploy; CI-mediated
  for CI). The model declares WHAT keys exist + WHERE they live, never embeds values.
- **ONE registry.** The per-builder deployment **manifest** must align/merge with the
  `stoa--reg` seat registry (the manifest↔registry merge is a LATER integration step;
  the Phase-1 key-model does NOT depend on the parallel stoa--reg liveness fix).
- **Reuse, don't fork:** `newswire-builder-setup` (~60% — Railway + mesh + DB +
  embed/serving + GCP-key-consumption) is the base the model generalizes; scienceclaw
  + prospector stand-ups feed this generalization rather than forking it.
- **Extensible:** category templates are a unit of reuse — adding a new category later
  must be additive, not a rewrite.

---

## 4. Scope boundary

**IN (this Phase-1 design):** the composable key/API/extension MODEL; the per-builder
MANIFEST schema; the resolution rule (`baseline + category + delta`); the provisioning
choreography (SA-scope + Railway keys + API enablement + budget cap, per-builder
isolated); the DB-extension parameterization; the first-class agent-access-layer shape;
the three worked-example manifests.

**OUT (later arcs / other owners):** building the cookie-cutter skill itself (Phase 2,
gauntlet build); actually provisioning anything on Railway/GCP (PRINCIPAL, only AFTER
the model is gated); the per-builder PRODUCT layer — the specific skills + curated data
(project seats: prospector team, Polybius_the_science_stoa for scienceclaw).

---

## 5. Team & flow

1. **CHIRON (team-architect) + HAMILTON (workflow-architect) co-design** the
   key-provisioning choreography + manifest schema. PLINY actively DRIVES the
   cross-handoff (do not leave the architects to self-sync); architects arm an active
   poll loop while waiting (the CHIRON↔HAMILTON stall lesson).
2. **Full gauntlet** on the design: DAEDALUS (formalize) → ARGUS (cold-audit) → ADA →
   VERA → CATO → NOMOS. (The deliverable is a design artifact; ADA/VERA exercise the
   manifest-resolution against the three worked examples — resolution is testable even
   though it is a design.)
3. **FM** independently verifies at each hand-back; **relays up** to Polybius_the_Stoa.
4. **Polybius_the_Stoa** reports the Phase-1 design UP to Polybius the Grand for the
   **gate before build**.

---

## 6. Definition of Done (Phase-1 design)

- [ ] The composable model is specified: baseline, category-template format, delta
      format, resolution rule, and the extensibility path for new categories.
- [ ] The per-builder **manifest schema** is specified (terse `{category + delta}`),
      with the resolution `baseline + category + delta → full set` defined unambiguously.
- [ ] The **provisioning** choreography is specified: per-builder GCP SA scope (isolation
      lock), Railway key set, GCP API enablement, budget cap — each driven by the
      resolved set.
- [ ] DB-extension parameterization (pgvector baseline + PostGIS toggle) is in the model.
- [ ] The first-class **agent-access-layer** shape (mesh API + CLI client skill over
      Tailscale) is specified as part of the deployable, with the product-layer boundary
      drawn (project seat owns the specific skills/data).
- [ ] All THREE worked examples (prospector, scienceclaw, labstat_bls) are expressed as
      concrete manifests AND shown to resolve correctly — including the labstat_bls
      `+BLS OEWS` delta on a reused template.
- [ ] The stoa--reg / manifest alignment is noted (merge is a later step; no dependency
      on the parallel liveness fix).
- [ ] Full gauntlet PASS + NOMOS CONFORMANT; FM independent verify; reported up for the
      Grand's gate.

---

**Author:** Denson Smith.
