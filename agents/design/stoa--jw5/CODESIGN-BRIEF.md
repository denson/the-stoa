# CO-DESIGN BRIEF — stoa--jw5 (u--9s2 Phase 1)

**From:** PLINY_the-stoa (orchestrator) | sid 8040be7f
**For:** MAJOR_CHIRON_the-stoa + MAJOR_HAMILTON_the-stoa (co-design)
**Arc home:** stoa--jw5 (the-stoa beadwork). Directive (the WHAT):
`git show beadwork:attachments/stoa--jw5/u9s2-phase1-directive.md`
**operating-mode:** autonomous (surface to PLINY on the §10 universal escalation triggers only)

> This is a **DESIGN** arc. Deliverable = a *design artifact*, not built code. You design the
> choreography + schema; the gauntlet then hardens it; Polybius the Grand gates the Phase-1
> design **before any build** (a later arc). Provision NOTHING on Railway/GCP.

---

## 1. The deliverable (restated from the directive)

The **composable key/API/extension provisioning MODEL** + the **per-builder MANIFEST schema**
for the builder-deploy cookie-cutter (u--9s2). Composition shape:

- **UNIVERSAL BASELINE** — Gemini EMBEDDING + Gemini SEARCH (gsearch) + the DB credential set.
- **CATEGORY TEMPLATES** — a standard key/API/extension LIST per category, reused *whole* and
  **extensible to new categories**. At minimum: geospatial = baseline + Maps + PostGIS;
  document-consuming = baseline + pgvector + document-parsing.
- **PER-DEPLOYMENT DELTA** — a *short* add/omit list off the category template.
- **MANIFEST (per-builder, terse):** declares `{category + delta}`. The cookie-cutter
  **RESOLVES** `baseline + category template + delta`, then **PROVISIONS** it per-builder,
  ISOLATED (GCP SA scoped to ONLY its own keys + Railway key set + GCP API enablement +
  budget cap).

---

## 2. Scope split (my orchestration call — co-design, not strict sequence)

Cast and choreography co-constrain; **iterate together**, don't hand off once and stop.

### CHIRON (cast / declarative — custom-agent aspect) owns:
- The per-builder **MANIFEST SCHEMA** (terse `{category + delta}` — fields, types, required vs optional).
- The **CATEGORY-TEMPLATE format** (the reusable key/API/extension LIST structure per category)
  + the **extensibility path** (adding a new category is additive, not a rewrite).
- The **DELTA format** (short add/omit list).
- The **UNIVERSAL BASELINE** definition (what every deployment gets).
- The first-class **AGENT-ACCESS-LAYER shape**: mesh API endpoint + CLI client skill over the
  Tailscale mesh (newswire `/query` + `newswire-trigger` is the worked precedent), as part of
  the deployable — and **draw the product-layer boundary** (project seat owns the *specific*
  skills + curated data; cookie-cutter owns the *pattern*).
- The **stoa--reg / manifest alignment note** (manifest↔registry merge is a LATER step; Phase-1
  must NOT depend on the parallel stoa--reg liveness fix).

### HAMILTON (choreography / workflow aspect) owns:
- The **RESOLUTION rule**: `baseline + category + delta → full resolved set`, defined
  **unambiguously** (precedence: how delta-add, delta-omit, and template entries combine;
  conflict handling).
- The **PROVISIONING choreography**, per-builder ISOLATED: GCP SA scoped to ONLY its own keys
  (the per-builder-isolation LOCK — an SA never carries another builder's scope), the Railway
  key set, GCP API enablement for **exactly** the resolved APIs, and a **budget cap**. Specify
  ordering + fail-closed properties.
- The **DB-extension parameterization** (pgvector baseline; PostGIS a per-builder toggle, geo
  only — same shape as the parameterized API set).
- **Credential-discipline integration**: the model declares WHAT keys exist + WHERE they live
  (keyring-local for direct deploy; CI-mediated for CI), and **never embeds values**. Agents
  never hold long-lived credentials. (Refs: `credential-discipline`, `railway-keyring-deploy`,
  `zeotek_newswire/SECURITY.md`, u--eq6, `newswire-builder-setup`.)

### Both (shared — exercises both halves):
- The **THREE worked-example manifests**, expressed concretely AND shown to resolve correctly:
  | builder | category | delta | resolves to (illustrative) |
  |---|---|---|---|
  | prospector | geospatial | — | baseline + Maps + PostGIS |
  | scienceclaw | document-consuming | — | baseline + pgvector + document-parsing (serves all prospector projects for cross-field discovery; coordinate Polybius_the_science_stoa, u--4at) |
  | labstat_bls | document/data | `+BLS OEWS` | baseline + (doc/data template) + BLS OEWS API key |
- **labstat_bls is the load-bearing test** that the delta mechanism is real: a single
  project-specific key rides on a reused template without bloating the template.

---

## 3. Constraints & locks (carry into the design)

- **Per-builder isolation (LOCK):** each GCP SA scoped to ONLY its own builder's keys + budget cap.
- **Agents never hold long-lived credentials** (declare WHAT/WHERE, never values).
- **ONE registry:** manifest must align/merge with `stoa--reg` (merge = later step; no dependency now).
- **Reuse, don't fork:** `newswire-builder-setup` (~60%: Railway + mesh + DB + embed/serving +
  GCP-key-consumption) is the base the model generalizes.
- **Extensible:** category templates are a unit of reuse — new category = additive.

## 4. Definition of Done (the gate must see ALL of these — directive §6)

- [ ] Composable model specified: baseline, category-template format, delta format, resolution
      rule, extensibility path for new categories.
- [ ] Per-builder MANIFEST schema specified (terse `{category + delta}`); resolution
      `baseline + category + delta → full set` unambiguous.
- [ ] PROVISIONING choreography specified: per-builder GCP SA scope (isolation lock), Railway
      key set, GCP API enablement, budget cap — each driven by the resolved set.
- [ ] DB-extension parameterization (pgvector baseline + PostGIS toggle) in the model.
- [ ] First-class agent-access-layer shape (mesh API + CLI client skill over Tailscale) with the
      product-layer boundary drawn.
- [ ] All THREE worked examples expressed as concrete manifests AND shown to resolve correctly
      (including labstat_bls `+BLS OEWS` delta on a reused template).
- [ ] stoa--reg / manifest alignment noted (merge later; no dependency on the liveness fix).

## 5. Co-design protocol (how we run this — I DRIVE the cross-handoff)

1. **Output artifact (single, unified):** `agents/design/stoa--jw5/design-codesign.md`.
   - To avoid concurrent-write corruption: **HAMILTON writes its choreography sections to
     `agents/design/stoa--jw5/choreography-hamilton.md`**; **CHIRON authors the unified
     `design-codesign.md`**, folding in HAMILTON's sections by reference/merge. CHIRON is the
     single writer of the unified file.
2. **Iterate together.** Each posts handoffs to **stoa--jw5** tagged `[for: CHIRON_the-stoa]` /
   `[for: HAMILTON_the-stoa]` / `[for: PLINY_the-stoa]`. Cast & choreography co-constrain — when
   one of you changes a shape that affects the other, say so on bw.
3. **Arm an active poll loop while waiting on your sibling** (the CHIRON↔HAMILTON cross-handoff
   stall lesson — do NOT go idle waiting for the other; poll bw ~2-3 min).
4. **I (PLINY) poll at ~2-3 min and drive the handoffs**, mediate any cast/choreography conflict,
   and surface convergence to the FM. When you hit a genuine fork that needs a value-call, post it
   to me framed as a tradeoff (don't smuggle a value-call into the design).
5. **Convergence signal:** when `design-codesign.md` satisfies all of §4 and both of you sign off,
   post `CO-DESIGN CONVERGED — stoa--jw5` tagged `[for: PLINY_the-stoa]`. I then open the gauntlet
   (DAEDALUS formalizes → ARGUS → ADA exercises resolution vs the 3 examples → VERA → CATO → NOMOS).

**First action for each of you:** ACK on stoa--jw5 (confirm seat + your half of the scope split),
then begin. CHIRON — stand up the `design-codesign.md` skeleton (the §4 DoD as section headers) so
HAMILTON's sections have a home to slot into.

— PLINY_the-stoa | sid 8040be7f-a1ba-4917-b953-75947d464abf | the-stoa
