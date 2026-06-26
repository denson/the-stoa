# Part 2 — HAMILTON lens: key-discovery / generation / validation choreography

**Seat:** MAJOR_HAMILTON_the-stoa (workflow-architect). **Arc:** stoa--jw5 / u--9s2 Phase-1 revision.
**Co-author seam:** MAJOR_CHIRON owns the service→key CATALOG structure + the emergent-templates
reframe (sole writer of the unified `discovery-codesign.md`). This artifact is the complementary
**discovery / generation / validation choreography** lens. CHIRON defines the catalog my generation
reads; I define how services-called become a `{category, delta}` manifest and how it is validated.

> **§2 LOAD-BEARING CONSTRAINT (held absolutely).** The resolver (§4 set-algebra) and provisioning
> (§5 S0–S6) are gauntlet-CONFORMANT and **STAND UNCHANGED**. Discovery is **strictly UPSTREAM** — a
> front-end that GENERATES the `{category, delta}` manifest the existing resolver consumes. The §8
> fixtures (prospector 8 / scienceclaw 6 / labstat_bls 7) are a **REGRESSION TARGET**, not re-derived.
> If any reframe pressured `resolve()` or the §8 sets I would STOP + dilemma-classify — nothing here
> does; the pipeline below feeds the unchanged resolver.

```
services-called ──discover──▶ catalog lookup ──generate──▶ {category, delta} ──validate──▶ resolve()[§4 UNCHANGED] ──▶ provision[§5 S0-S6 UNCHANGED]
   (declare + scan-validate)                    (emergent cat + derived delta)   (fail-closed, BEFORE S0)
```

---

## 1. The DISCOVERY step — DECLARE-primary + SCAN-as-validator (web-verified recommendation)

**Recommendation: explicit DECLARATION is authoritative; static SCAN is a build-time validator (drift
/ shadow-API cross-check), not the generator. A runtime observer is a named Phase-2 layer.**

**Why (web-verified 2026-06-26, current docs — NOT asserted from memory):** static analysis is
reliable for detecting *capability* (which SDK/library is imported) but **unreliable for detecting
actual service calls** — it suffers high **false-negatives** on dynamic dispatch / dependency
injection, **config-driven endpoints** (`fetch(\`${process.env.PARTNER_API_URL}/...\`)`), indirect
HTTP wrappers, and codegen/declarative clients; and **false-positives** on test/dead code. For our
model a false-negative is the **under-provisioning runtime failure** the whole addition exists to
prevent (a called service whose key was never provisioned → 401/500 at runtime), and a false-positive
is scope bloat. So **scan cannot be the source of truth.** The industry pattern (OWASP CycloneDX
SaaSBOM) makes an **explicit declaration the design-time contract / authorized inventory**, with
static scanning as the **CI drift-detector** and runtime observability (eBPF/OpenTelemetry) as the
production check. This maps onto our model exactly:

| Pillar | Our binding | Role |
|---|---|---|
| **(1) DECLARE — authoritative** | each skill/component DECLARES the services it calls (a `services:` list in its `SKILL.md` frontmatter or a builder manifest-source) | the **source of truth** that GENERATION reads (§2) |
| **(2) SCAN — validator** | static scan flags any imported SDK / raw HTTP client / known-service reference whose service is **not declared** | a **drift / shadow-API guard** in VALIDATION (§3, V5) — flags, does not silently add |
| **(3) RUNTIME observe — Phase-2** | eBPF / OTel detect actual outbound calls in the deployed builder | **named Phase-2** confirm-in-production; out of Phase-1 design scope |

**Declaration shape (SHAPE only; data is Phase-2):** a per-skill/component declaration
`services: [<service-id>, …]` where each `service-id` keys CHIRON's catalog. The builder's
**services-called set** = the union of declarations across the skills/components it ships. (The
substrate already carries per-skill `SKILL.md` frontmatter — the natural T2/T3 home for this
declaration; placement is CHIRON's tier call.)

**Scan-vs-declare precedence (deterministic):** DECLARE generates; SCAN validates. A service the
scan detects but the declaration omits is a **VALIDATION ERROR (V5), fail-closed** — it BLOCKS
generation until the declaration is reconciled (added or explicitly waived). We do **not**
auto-promote a scanned service into the manifest: a scan false-positive (test/dead code) would
provision an uncalled key (bloat), and silently trusting scan would mask the declaration drift the
guard exists to surface. Fail-closed-to-human is the safe default (consistent with the §5 S2c human
gate + the §2.4 BaselineOmitError fail-closed posture).

---

## 2. The manifest GENERATION choreography (services-called → {category, delta})

Input: the builder's **services-called set** (from DECLARE, §1). Output: a `{category, delta}`
manifest the **unchanged** resolver consumes. Baseline is NOT discovered — it is universal ("what
every deployment needs") and is prepended by the unchanged `resolve()` (`BASELINE ∪ …`); discovery
determines only the **category + delta** layer from the non-baseline services-called.

```
GENERATE(services_called):
  G1  for each service-id in services_called:  entries(service-id) := CATALOG[service-id].entries
      called_entries := ⋃ entries(service-id)      # union of typed §3 entries (any kind:
                                                    # gcp_api / gcp_secret / db_extension /
                                                    # thirdparty_rest_key / railway_var)
      # FAIL-CLOSED: a service-id absent from the catalog is a V1 error (below) — stop, do not emit.

  G2  category := best_fit_emergent_category(called_entries)
      # CHIRON's emergent-templates: a category is a named, frequently-co-occurring service-bundle.
      # best-fit = the catalog category whose entry-set is the LARGEST SUBSET of called_entries
      # (maximal coverage without over-reach). Ties / no-cover → category = none (delta carries all).

  G3  delta.add  := called_entries  \  (BASELINE ∪ CATEGORY_TEMPLATE[category])
      delta.omit := CATEGORY_TEMPLATE[category]  \  (called_entries ∪ BASELINE)
      # add  = called entries not already supplied by baseline+category (the project-specific keys).
      # omit = category entries the builder does NOT call (trim the emergent bundle to actual calls).
      #        omit NEVER targets a baseline entry (BaselineOmitError, §2.6) — baseline is universal,
      #        always called-by-definition, so it can never appear in omit. Guard preserved.

  G4  emit { category, delta:{add, omit} }
```

**Determinism:** `best_fit_emergent_category` is a pure max-subset selection over the catalog; same
services-called + same catalog ⇒ same manifest. The generated manifest is exactly the shape the
existing resolver already validates — `resolve()` is untouched, only its INPUT is now derived.

**The delta becomes DERIVED (the reframe's choreography half):** `delta` is no longer hand-authored —
it is `(services-called entries) − (baseline ∪ chosen category)` for adds, and the called-trim for
omits. This is the mechanical expression of CHIRON's "delta = services-called minus category."

---

## 3. The VALIDATION choreography (runs BEFORE S0; fail-closed)

The generated manifest is validated *before* it reaches S0. A manifest failing any check never
provisions. Validation **reuses the existing §4 guards** (it does not re-implement them) plus the
discovery-specific completeness/minimality checks:

```
VALIDATE(services_called, generated_manifest):
  V1  EVERY-SERVICE-CATALOGED: every service-id ∈ services_called has a CATALOG entry.
      else → ERROR "uncataloged service <id>" (can't generate a complete manifest; add to catalog).
  V2  COMPLETE (anti-under-provision; the M3 runtime-completeness lineage):
      resolve(generated_manifest) ⊇ called_entries — every called service's entries are provisioned.
      else → ERROR "service <id> called but not in resolved set".
  V3  MINIMAL (anti-bloat): resolve(generated_manifest) \ BASELINE contains NO entry for an
      uncalled service. (Baseline is universal and exempt — it is always present by definition.)
      else → ERROR "uncalled entry <kind,name> provisioned".
  V4  RESOLVE-WELL-FORMED (reuse §4 guards, unchanged): resolve(generated_manifest) raises NO
      BaselineOmitError (§2.6) AND satisfies §3.4 runtime-completeness (every key-bearing surface
      has its paired credential — e.g. google-maps ⇒ MAPS_API_KEY).
      else → the existing §4 error fires (discovery did not weaken it).
  V5  NO-UNDECLARED-DRIFT (the scan pillar, §1): no scan-detected service-call is undeclared.
      else → ERROR "shadow service <id> detected but not declared" (reconcile declaration or waive).
```

**Placement:** V1–V5 run as a gate **strictly before S0** — they produce + certify the manifest S0
consumes. Fail-closed: an invalid manifest is rejected with a named error; it never enters the
provisioning sequence. (Symmetric with the §5 fail-closed property: a half/ill-formed input never
reaches serving.)

**V2 + V4 are the anti-under-provisioning spine** — they are the discovery-side guarantee of the same
property M3 (runtime-completeness) gives the resolver: a builder cannot deploy missing a key for a
service it actually calls.

---

## 4. The three worked examples via discovery (regression target: 8 / 6 / 7)

Baseline (universal, prepended by unchanged `resolve()`): `{gcp_api,gemini-embedding}`,
`{gcp_api,gemini-search}`, `{railway_var,DATABASE_URL}`, `{gcp_secret,POSTGRES_PASSWORD}`,
`{db_extension,pgvector}` = **5 entries**. Discovery determines only category+delta.

**prospector** — declared services-called (non-baseline): `google-maps` (client-side Maps-JS surface),
`spatial-db` (spatial queries).
```
G1 called_entries = { gcp_api:google-maps, gcp_secret:MAPS_API_KEY, db_extension:postgis }
   (google-maps → its gcp_api + the paired MAPS_API_KEY per §3.4; spatial-db → postgis)
G2 best-fit emergent category = geospatial  (bundle {google-maps, MAPS_API_KEY, postgis} ⊆ called)
G3 delta.add = ∅ ; delta.omit = ∅
G4 GENERATED = { category: geospatial, delta: {} }
   resolve() → BASELINE(5) ∪ geospatial(3) = 8 entries   ✓ regression §8.1 (8)
```

**scienceclaw** — declared services-called (non-baseline): `document-parsing`.
```
G1 called_entries = { gcp_api:document-parsing }
G2 best-fit emergent category = document-consuming  (bundle {document-parsing} ⊆ called)
G3 delta = {}
G4 GENERATED = { category: document-consuming, delta: {} }
   resolve() → BASELINE(5) ∪ document-consuming(1) = 6 entries   ✓ regression §8.2 (6)
```

**labstat_bls** — declared services-called (non-baseline): `document-parsing`, **`bls-oews`** (a BLS
OEWS REST call).
```
G1 called_entries = { gcp_api:document-parsing, thirdparty_rest_key:BLS_OEWS_API_KEY }
   (bls-oews → catalog → thirdparty_rest_key:BLS_OEWS_API_KEY, NO gcp_api — the §8.3 fact)
G2 best-fit emergent category = document-consuming  ({document-parsing} ⊆ called; bls-oews not in it)
G3 delta.add = { thirdparty_rest_key: BLS_OEWS_API_KEY }   (called minus baseline∪category)
   delta.omit = ∅
G4 GENERATED = { category: document-consuming, delta: { add: [thirdparty_rest_key:BLS_OEWS_API_KEY] } }
   resolve() → BASELINE(5) ∪ document-consuming(1) ∪ {BLS_OEWS_API_KEY}(1) = 7 entries  ✓ regression §8.3 (7)
```
✓ **Load-bearing test passes via discovery:** the BLS OEWS REST call is DISCOVERED (declared) →
catalog-looked-up → GENERATES the `+BLS_OEWS_API_KEY` delta (kind `thirdparty_rest_key`, no
gcloud-enable), reproducing the existing §8.3 result. The resolver is untouched; discovery produced
the manifest the gauntlet already validated.

---

## 5. The seam with CHIRON + §2-constraint compliance

- **What I consume from CHIRON's catalog:** `CATALOG[service-id] → { entries (typed §3 kind+name),
  gcp_api?, category }`. My G1 reads `entries`; my G2 reads the emergent-category bundles; my G3
  derives the delta. The `kind`-agnostic union (G1) is what lets db_extension (postgis), gcp_secret
  (MAPS_API_KEY), thirdparty_rest_key (BLS), and gcp_api all flow through one generation path.
- **Co-constraint to confirm with CHIRON:** (a) every catalog entry's credential is a typed §3 entry
  (so G1's union is well-typed); (b) the emergent category is still a named entry-set the resolver
  consumes (only its PROVENANCE changes — emergent vs declared — so G2/`CATEGORY_TEMPLATE[category]`
  still resolves); (c) the paired-credential rule (§3.4, google-maps ⇒ MAPS_API_KEY) lives in the
  catalog entry for google-maps, so G1 picks up BOTH automatically.
- **§2 compliance (explicit):** nothing here changes `resolve()` or the §8 expected sets. G1–G4
  produce the SAME `{category, delta}` shapes the resolver already takes; V1–V5 gate the input and
  reuse the existing §4 guards (V4). The 8/6/7 regression is HIT, not re-derived. Discovery is a pure
  upstream front-end.

## 6. DoD coverage (my half — Part-2 §4)

- [x] DISCOVERY step specified (DECLARE-primary + SCAN-validator + runtime-Phase-2), recommendation
      web-verified (static-scan unreliability for actual calls; CycloneDX SaaSBOM precedent) — §1
- [x] manifest GENERATION specified (G1–G4, deterministic, services-called → {category, delta}) — §2
- [x] manifest VALIDATION specified (V1–V5: every-cataloged + complete + minimal + resolve-well-formed
      + no-undeclared-drift; runs BEFORE S0, fail-closed) — §3
- [x] all THREE worked examples re-expressed via discovery, generating manifests that resolve to
      8/6/7 (regression target hit), labstat_bls bls-oews → +BLS_OEWS_API_KEY delta — §4
- [x] resolver §4 + provisioning §5 confirmed UNCHANGED (regression-confirm; §2 compliance) — §5
- [ ] CHIRON folds these sections into the unified `discovery-codesign.md` (sole writer)
- [ ] emergent-templates reframe (CHIRON's half) — catalog structure + category-as-emergent-bundle
- [ ] targeted gauntlet on the addition (DAEDALUS formalize → ARGUS → ADA exercise GENERATION vs the
      3 examples → VERA → CATO → NOMOS; resolver/provisioning = regression-confirm only)
