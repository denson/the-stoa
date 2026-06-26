# DISCOVERY CO-DESIGN CONVERGED — stoa--jw5 (u--9s2 Phase-1 revision): the key-discovery process

**Arc:** stoa--jw5 / u--9s2 Phase-1 revision (the KEY-MODEL ADDITION from the Grand/PRINCIPAL,
relayed by the FM). **Status:** unified co-design — both lenses folded; convergence-ready.

**Co-authors (complementary lenses, single seam = the CATALOG):**
- **MAJOR_CHIRON** — service→key **catalog** structure/ownership + the **emergent-templates reframe**
  (this file; sole writer). Sections §1, §2, §3, §7 (catalog records), §9.
- **MAJOR_HAMILTON** — **discovery / generation / validation** choreography
  (`discovery-choreography-hamilton.md`, flat sibling in this dir; folded here as §4, §5, §6, §7-pipeline).
- **Next:** DAEDALUS formalizes; a TARGETED gauntlet hardens the addition (resolver/provisioning =
  regression-confirm only).

---

## §2 — THE LOAD-BEARING CONSTRAINT (stated first, held absolutely)

The existing **resolver (design-formal §4 set-algebra)** and **provisioning choreography (§5 S0–S6)**
are gauntlet-CONFORMANT and **STAND UNCHANGED**. The discovery process is **strictly UPSTREAM** of
them — a new front-end that PRODUCES the `{category, delta}` manifest the existing resolver consumes.
The §8 fixtures (**prospector 8 / scienceclaw 6 / labstat_bls 7**) are a **REGRESSION TARGET that
must still be hit**, never re-derived. If any reframe here pressured `resolve()` or the §8 expected
sets, it is a scope breach → STOP + dilemma-classify to PLINY. **Nothing in this design does** — the
pipeline below feeds the unchanged resolver; the category stays a named entry-set the resolver
consumes (only its *provenance* changes); the delta stays the same `{add, omit}` shape.

```
services-called ──discover──▶ catalog lookup ──generate──▶ {category, delta} ──validate──▶
                  (declare +                  (emergent cat +    (fail-closed,
                   scan-validate)              derived delta)     BEFORE S0)
        resolve() [§4 UNCHANGED] ──▶ resolved set ──▶ provision [§5 S0-S6 UNCHANGED]
```

---

## §0 — Frame: the gap this closes

Phase-1 so far took a **hand-authored** `{category, delta}` manifest as input. The directive: the
manifest must be **DISCOVERED / GENERATED from what the builder actually CALLS**, not hand-guessed. A
builder that calls Google Maps + a BLS REST API gets those keys because the system **detected the
calls**, not because a human remembered. Missing a called service = a runtime failure (the
under-provision footgun); provisioning an uncalled service = waste + scope bloat. Discovery makes the
manifest a **derived, verifiable** artifact — and turns the §3.4 runtime-completeness property into
something the model *guarantees by construction* rather than hopes a human declared correctly.

---

## §1 — The service→key CATALOG (CHIRON; DoD item 1)

The **catalog** is the new T1 cookie-cutter asset that maps each external **service** to the typed
credentials it requires. It is the **shared contract**: CHIRON defines its structure; HAMILTON's
generation (§5) reads it.

**Per-service record:**
```yaml
- service-id: <stable-id>          # the key skills DECLARE (HAMILTON §4 `services:` list)
  entries:                          # ALL typed entries this service requires — each is an EXISTING
                                    # design-formal §2/§3 typed entry (kind ∈ {gcp_api, gcp_secret,
                                    # railway_var, db_extension, thirdparty_rest_key}); the catalog
                                    # introduces NO new kind — it MAPS a service to existing entries.
    - { kind: <kind>, name: <NAME> }
    - ...
  gcp_api: <api-id | none>          # denormalized convenience = the subset of `entries` with kind=gcp_api
  category: <emergent-category-tag | none>   # which emergent bundle this service belongs to (provenance)
```

**Load-bearing structural properties** (these are the catalog's contract with the rest of the model):

1. **Every catalog credential is a typed §3 entry (confirms HAMILTON seam-(a)).** The catalog maps
   `service → set of typed entries`; it adds no new entry-kind. So HAMILTON's G1 union (`⋃ entries`)
   is well-typed and flows db_extension / gcp_secret / thirdparty_rest_key / gcp_api through one
   generation path.
2. **A service maps to a SET of entries (1:N), not 1:1.** One service can require several
   credentials. This is what carries the **§3.4 paired-credential rule INTO the catalog (confirms
   HAMILTON seam-(c)):** the `google-maps` record holds BOTH `{gcp_api, google-maps}` AND
   `{gcp_secret, MAPS_API_KEY}`, so a single declared call to google-maps makes G1 pick up both —
   **runtime-completeness becomes a catalog-construction invariant**, not a check the generator must
   remember. (Adding a key-bearing service to the catalog REQUIRES its paired credential in the same
   record; that is the catalog-authoring discipline, enforced at §6-graduation/arc time.)
3. **Baseline is NOT in the catalog.** Baseline (`gemini-embedding`, `gemini-search`, `DATABASE_URL`,
   `POSTGRES_PASSWORD`, `pgvector`) is universal — prepended by the unchanged `resolve()`
   (`BASELINE ∪ …`). The catalog covers only the **non-baseline, discoverable** services. So discovery
   determines the **category + delta** layer only; baseline can never appear in a generated delta
   (which is also why a generated `delta.omit` can never hit a baseline entry — the §2.6
   BaselineOmitError guard is preserved by construction, not re-checked).

---

## §2 — The EMERGENT-TEMPLATES reframe (CHIRON; DoD item 5)

**Before:** category templates were **hand-curated static bundles** (geospatial = {Maps, PostGIS};
document-consuming = {document-parsing}), authored via arc.

**After (the reframe):** a category is an **EMERGENT common service-bundle** — a *named set of
services (and their catalog entries) that frequently co-occurs across builders' services-called sets.*

**The §2-compliance precision (this is the whole reason the reframe is safe):** a category **remains
exactly what the resolver consumes — a named entry-set** (`CATEGORY_TEMPLATE[category]` is still a set
of typed entries, unchanged in shape and in how `resolve()` reads it). **Only its PROVENANCE changes:**

| | Provenance of a category's membership |
|---|---|
| **Before** | a human hand-authored the bundle |
| **After** | the bundle **emerges** from observed co-occurrence, **promoted** to a named category via the §6 graduation rule (now the **EMERGENCE rule**) |

So the resolver, the §3.2 category-template *format*, and the §8 expected sets are **untouched**. (This
confirms HAMILTON seam-(b): G2's `CATEGORY_TEMPLATE[category]` still resolves — a category is still a
named entry-set.)

**The delta becomes DERIVED** (the reframe's data half; mechanized by HAMILTON's G3): the per-builder
delta is no longer hand-authored — it is the mechanical remainder
`delta.add = called_entries \ (BASELINE ∪ category)` and `delta.omit = category_entries \ (called ∪ BASELINE)`.
The delta is now *provably* "the project-specific keys this builder calls beyond the emergent bundle,
plus the bundle-members it does not call."

**The EMERGENCE rule (my "graduation rule → emergence rule" framing):** when a service-bundle recurs
across **≥2 builders' derived call-sets**, it is **promoted** to a named emergent category (or merged
into one) via arc. Categories *grow from observed deltas* rather than being declared up front. This is
the same open-closed governance as the original graduation rule, now driving category **formation**.

**Bootstrapping (the "no population yet" answer):** emergence needs *observation*, which Phase-1
(design-time, no live builder population) lacks. So:
- the **Phase-1 catalog SEEDS** the initial emergent categories — `geospatial` and `document-consuming`
  — from the *known* co-occurrence in the three worked examples (Maps+PostGIS co-occur for geo
  builders; document-parsing for doc builders). These are the first emergent bundles, recorded as the
  initial state.
- the **EMERGENCE rule governs how NEW categories form** as the population grows (Phase-2+).

So "emergent" is the **provenance/governance model**; the seed categories are the concrete initial
state — and they are *exactly* the §3.2 bundles the gauntlet already validated, so the §8 sets hold.

---

## §3 — Ownership / tier placement (CHIRON; supports DoD items 1 + 5)

The reframe is faithful to the existing three-tier model (T1 cookie-cutter / T2 manifest / T3
product) — it shifts the manifest's **provenance**, not the tiers:

| Artifact | Tier | Owner | Note |
|---|---|---|---|
| **The CATALOG** (service→typed-entries) | **T1** | cookie-cutter (substrate) | generic, versioned, reused whole; adding a service = additive arc (open-closed) |
| **Emergent category bundles** | **T1** | cookie-cutter | named entry-sets; membership emerges/promotes via the §6 EMERGENCE rule (arc) |
| **Per-skill `services:` DECLARATION** (HAMILTON §4) | **T3** | the **project seat** | a property of the specific product skill — the project seat knows which services its skills call |
| **The builder's services-called set → GENERATED `{category, delta}` manifest** | **T2** | **derived** (generated, not hand-authored) | the per-builder declaration layer, now mechanically produced at the seam |

**The clean ownership story:** the project seat (T3) declares what its skills call — it owns its own
product; the cookie-cutter (T1) owns service→key knowledge (the catalog) + the emergent categories;
the per-builder manifest (T2) is **generated at the seam** from T3 declarations through the T1 catalog.
**No human hand-guesses the manifest** — the original directive's goal. The reframe REPLACES the
hand-authored T2 manifest with a T2 manifest *generated from T3 declarations via the T1 catalog*; the
tier model is preserved.

**Extensibility (open-closed, unchanged):** adding a new service = one additive T1 catalog record (via
arc); adding/forming a new emergent category = the EMERGENCE rule (via arc). The generator (§5), the
resolver (§4), baseline, and existing records are **closed for modification** — open only for additive
extension.

---

## §4 — The DISCOVERY step (HAMILTON, folded; DoD item 2)

**Recommendation (HAMILTON, web-verified 2026-06-26 — not asserted from memory): explicit DECLARATION
is authoritative; static SCAN is a build-time validator (drift / shadow-API cross-check), not the
generator; a runtime observer is a named Phase-2 layer.**

**Why scan cannot be the source of truth:** static analysis reliably detects *capability* (which SDK
is imported) but is **unreliable for actual service calls** — high false-negatives on dynamic
dispatch, dependency injection, config-driven endpoints (`fetch(${env.PARTNER_API_URL}/…)`), indirect
HTTP wrappers, codegen clients; and false-positives on test/dead code. For this model a false-negative
is precisely the **under-provisioning runtime failure** the addition exists to prevent; a
false-positive is scope bloat. The industry pattern (OWASP **CycloneDX SaaSBOM**) makes an explicit
declaration the design-time **authorized inventory**, with static scan as the **CI drift-detector** and
runtime observability (eBPF/OTel) as the production check.

| Pillar | Binding | Role |
|---|---|---|
| **(1) DECLARE — authoritative** | each skill/component DECLARES `services: [<service-id>, …]` (in its `SKILL.md` frontmatter / manifest-source) | the **source of truth** GENERATION reads |
| **(2) SCAN — validator** | static scan flags any imported SDK / raw HTTP client / known-service reference whose service is **not declared** | a **drift / shadow-API guard** in VALIDATION (V5) — flags, never silently adds |
| **(3) RUNTIME observe — Phase-2** | eBPF / OTel detect actual outbound calls in the deployed builder | **named Phase-2** confirm-in-production; out of Phase-1 scope |

The builder's **services-called set** = the union of `services:` declarations across the skills/
components it ships. (Per-skill `SKILL.md` frontmatter is the natural home — **T3** per §3.)
**Precedence:** DECLARE generates; SCAN validates. A scan-detected-but-undeclared service is a
**VALIDATION ERROR (V5), fail-closed** — it BLOCKS generation until the declaration is reconciled
(added or explicitly waived); scan never auto-promotes (a false-positive would provision an uncalled
key). Fail-closed-to-human is the safe default (consistent with the §5 S2c human gate + §2.6
fail-closed posture).

---

## §5 — The manifest GENERATION choreography (HAMILTON, folded; DoD item 3)

Input: the builder's **services-called set** (from DECLARE). Output: a `{category, delta}` manifest the
**unchanged** resolver consumes. Baseline is NOT discovered — it is prepended by `resolve()`; discovery
determines only the category+delta layer.

```
GENERATE(services_called):
  G1  called_entries := ⋃ over service-id ∈ services_called of CATALOG[service-id].entries
      #   union of typed §3 entries (any kind). A service-id ABSENT from the catalog → V1 error (stop).
  G2  category := best_fit_emergent_category(called_entries)
      #   = the catalog category whose entry-set is the LARGEST SUBSET of called_entries (maximal
      #   coverage, no over-reach). Ties / no cover → category = none (delta carries all).
  G3  delta.add  := called_entries \ (BASELINE ∪ CATEGORY_TEMPLATE[category])
      delta.omit := CATEGORY_TEMPLATE[category] \ (called_entries ∪ BASELINE)
      #   add = called entries beyond baseline+category (the project-specific keys).
      #   omit = category entries the builder does NOT call (trim the emergent bundle to actual calls).
      #          omit can NEVER hit a baseline entry — baseline ∉ catalog/category (§1.3) → §2.6 guard preserved.
  G4  emit { category, delta:{add, omit} }
```

**Determinism:** `best_fit_emergent_category` is a pure max-subset selection over the catalog; same
services-called + same catalog ⇒ same manifest. The generated manifest is exactly the shape `resolve()`
already validates — the resolver is untouched; only its INPUT is now derived.

---

## §6 — The manifest VALIDATION choreography (HAMILTON, folded; DoD item 4)

The generated manifest is validated **before** it reaches S0 (it produces + certifies the manifest S0
consumes). Validation **reuses the existing §4 guards** plus discovery-specific completeness/minimality:

```
VALIDATE(services_called, generated_manifest):
  V1  EVERY-SERVICE-CATALOGED: every service-id ∈ services_called has a CATALOG record.
      else → ERROR "uncataloged service <id>" (cannot generate a complete manifest; add to catalog).
  V2  COMPLETE (anti-under-provision; the §3.4 runtime-completeness lineage):
      resolve(generated_manifest) ⊇ called_entries — every called service's entries are provisioned.
  V3  MINIMAL (anti-bloat): resolve(generated_manifest) \ BASELINE has NO entry for an uncalled service.
  V4  RESOLVE-WELL-FORMED (reuse §4 guards, unchanged): resolve(generated_manifest) raises NO
      BaselineOmitError (§2.6) AND satisfies §3.4 runtime-completeness (every key-bearing surface has
      its paired credential — e.g. google-maps ⇒ MAPS_API_KEY, which §1.2 guarantees via the catalog).
  V5  NO-UNDECLARED-DRIFT (the scan pillar, §4): no scan-detected call is undeclared.
      else → ERROR "shadow service <id> detected but not declared" (reconcile or waive).
```

**Placement:** V1–V5 run as a gate **strictly before S0**, fail-closed — an invalid manifest is
rejected with a named error and never enters provisioning (symmetric with §5's fail-closed property).
**V2 + V4 are the anti-under-provisioning spine** — the discovery-side guarantee of the same property
§3.4 gives the resolver: a builder cannot deploy missing a key for a service it actually calls.

---

## §7 — The three worked examples via discovery (shared falsification target: 8 / 6 / 7)

**Catalog records driving these (CHIRON):**
```yaml
- service-id: google-maps      # client-side Maps-JS surface = api-key-bearing (§3.4)
  entries: [ {kind: gcp_api, name: google-maps}, {kind: gcp_secret, name: MAPS_API_KEY} ]
  gcp_api: google-maps ;  category: geospatial
- service-id: spatial-db
  entries: [ {kind: db_extension, name: postgis} ] ;  gcp_api: none ;  category: geospatial
- service-id: document-parsing
  entries: [ {kind: gcp_api, name: document-parsing} ] ;  gcp_api: document-parsing ;  category: document-consuming
- service-id: bls-oews         # a BLS OEWS REST call — NOT a GCP API
  entries: [ {kind: thirdparty_rest_key, name: BLS_OEWS_API_KEY} ] ;  gcp_api: none ;  category: none
```
**Seeded emergent categories (CHIRON, §2 bootstrap):**
`geospatial = {gcp_api:google-maps, gcp_secret:MAPS_API_KEY, db_extension:postgis}` (google-maps ∪
spatial-db); `document-consuming = {gcp_api:document-parsing}`.
Baseline (universal, prepended by `resolve()`) = 5 entries.

**prospector** — declares `services: [google-maps, spatial-db]`
```
G1 called_entries = {gcp_api:google-maps, gcp_secret:MAPS_API_KEY, db_extension:postgis}
G2 category = geospatial   (its bundle ⊆ called)         G3 delta = {}     (add=∅, omit=∅)
G4 {category: geospatial, delta: {}}  →  resolve() = BASELINE(5) ∪ geospatial(3) = 8   ✓ §8.1
```
**scienceclaw** — declares `services: [document-parsing]`
```
G1 called_entries = {gcp_api:document-parsing}
G2 category = document-consuming   G3 delta = {}
G4 {category: document-consuming, delta: {}}  →  BASELINE(5) ∪ doc-consuming(1) = 6   ✓ §8.2
```
**labstat_bls** — declares `services: [document-parsing, bls-oews]`  (the load-bearing test)
```
G1 called_entries = {gcp_api:document-parsing, thirdparty_rest_key:BLS_OEWS_API_KEY}
G2 category = document-consuming   ({document-parsing} ⊆ called; bls-oews not in it)
G3 delta.add = {thirdparty_rest_key:BLS_OEWS_API_KEY}   (called \ (baseline ∪ category));  omit = ∅
G4 {category: document-consuming, delta:{add:[thirdparty_rest_key:BLS_OEWS_API_KEY]}}
   →  BASELINE(5) ∪ doc-consuming(1) ∪ {BLS_OEWS_API_KEY}(1) = 7   ✓ §8.3
```
✓ **Load-bearing test passes via discovery:** the BLS OEWS REST call is DECLARED → catalog-looked-up
→ GENERATES the `+BLS_OEWS_API_KEY` delta (kind `thirdparty_rest_key`, **no gcloud-enable**),
reproducing the existing §8.3 result. Discovery produced the exact manifests the gauntlet already
validated; the resolver is untouched.

---

## §8 — §2 compliance + regression confirmation (DoD item 7)

- `resolve()` (§4) and provisioning (§5 S0–S6) are **textually unchanged** — discovery is a pure
  upstream front-end that emits the same `{category, delta}` shape they already consume.
- The §8 expected sets (8 / 6 / 7) are **HIT, not re-derived** — §7 generates manifests that resolve
  to exactly those sets.
- The category stays a named entry-set the resolver consumes (§2 reframe changes only provenance); the
  delta stays the `{add, omit}` shape (§2.6 BaselineOmitError guard preserved by §1.3 construction).
- No pressure on `resolve()` or §8 arose → **no dilemma to classify.** The targeted gauntlet need only
  **regression-confirm** the resolver/provisioning, and exercise the NEW manifest-GENERATION against §7.

---

## §9 — The seam contract (CHIRON ⟷ HAMILTON)

The **CATALOG is the single shared contract.** CHIRON's per-service typed-entry structure (§1) feeds
HAMILTON's scan→generate (§5); HAMILTON's services-called set + CHIRON's catalog → the generated
`{category, delta}` manifest. **CHIRON confirms HAMILTON's three co-constraints:**
- **(a)** every catalog credential is a typed §3 entry → §1.1 (no new kind; G1's union is well-typed). ✓
- **(b)** an emergent category is still a named entry-set the resolver consumes (only provenance
  changes) → §2 (the core §2-compliance argument; G2's `CATEGORY_TEMPLATE[category]` still resolves). ✓
- **(c)** the §3.4 paired-credential rule lives in the catalog record → §1.2 (the google-maps record
  carries both its API and MAPS_API_KEY; G1 picks up both; drives prospector=8). ✓

Any change to the catalog structure re-constrains both halves → flag on bw.

---

## §10 — DoD coverage (Part-2 §4)

- [x] service→key CATALOG structure specified (per-service typed entries + GCP API + category; T1
      placement; additive extensibility) — §1, §3, §7
- [x] DISCOVERY step specified (DECLARE-primary + SCAN-validator + runtime-Phase-2; web-verified) — §4
- [x] manifest GENERATION specified (G1–G4, deterministic, services-called → {category, delta}) — §5
- [x] manifest VALIDATION specified (V1–V5: cataloged + complete + minimal + resolve-well-formed +
      no-drift; before S0, fail-closed) — §6
- [x] EMERGENT-TEMPLATES reframe specified (category = emergent bundle, provenance-only change; delta
      = derived; resolver + §8 sets UNCHANGED, stated explicitly) — §2, §8
- [x] all THREE worked examples re-expressed via discovery, generating manifests that resolve to
      8 / 6 / 7 (regression target hit); labstat_bls bls-oews → +BLS_OEWS_API_KEY delta — §7
- [x] resolver §4 + provisioning §5 confirmed UNCHANGED (regression-confirm, not re-derive) — §8

---

## §11 — Provenance

Co-designed by **MAJOR_CHIRON_the-stoa** (catalog structure/ownership + emergent-templates reframe) +
**MAJOR_HAMILTON_the-stoa** (discovery/generation/validation choreography); unified by CHIRON (sole
writer). HAMILTON's discovery recommendation web-verified (static-scan unreliability for actual calls;
OWASP CycloneDX SaaSBOM precedent), 2026-06-26. Builds on the gauntlet-CONFORMANT Phase-1 design
(`design-formal.md`); resolver + provisioning unchanged. Author: Denson Smith.
