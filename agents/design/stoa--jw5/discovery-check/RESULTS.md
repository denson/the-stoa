<!-- author: Denson Smith -->
<!-- ticket: stoa--jw5 (u--9s2 Phase-1) -->
<!-- seat-built-by: CAPTAIN_ADA_the_stoa (EXECUTOR) — TARGETED gauntlet stage 3/6 -->
<!-- design-ground-truth: agents/design/stoa--jw5/design-formal.md §16-§23 (KEY-DISCOVERY PROCESS addition) -->

# discovery-check RESULTS — exercising manifest GENERATION (§19 G1–G4) vs the §23.1 examples

**What this harness proves.** The KEY-DISCOVERY PROCESS addition's executable core
(catalog → generation → validation) produces, from each builder's declared
`services:` set, a `{category, delta}` manifest that the **UNCHANGED Part-1
resolver** resolves to the §8 sets **8 / 6 / 7** — i.e. discovery is a purely
upstream front-end and the §2 resolver is untouched.

- **Harness path:** `agents/design/stoa--jw5/discovery-check/`
  - `catalog.py` — §22 seed catalog (service-id → entries + gcp_api + category-tag) + §22 seeded emergent categories. The §3.4 pairing lives in the `google-maps` record (BOTH `(gcp_api, google-maps)` AND `(gcp_secret, MAPS_API_KEY)`).
  - `generate.py` — `generate(services_called, catalog, categories, baseline)` per §19 G1–G4 (deterministic; baseline not discovered; tie-break category-tag asc).
  - `validate.py` — V1–V5 per §20 (V4 **REUSES** `resolve` / `BaselineOmitError` / `check_runtime_completeness` from the unchanged `resolve.py`; never re-implements them).
  - `run.py` — driver: for each of the 3 builders, generate → resolve (UNCHANGED) → assert 8/6/7 + manifest-equivalence to §8 + V1–V5; plus 2 negative probes; plus regression confirmation.
- **`resolve()` is REUSED unmodified:** imported from `../resolution-check/resolve.py` via `sys.path` injection. discovery-check writes NO file (no `open()` calls); `resolve.py` mtime (15:57, Part-1 build) predates all discovery-check files (21:01–21:03). **Feeding the GENERATED manifest into the unchanged `resolve()` and getting 8/6/7 IS the §2-constraint proof.**

## Per-builder generation result (`python discovery-check/run.py` → exit 0)

| builder | declared `services:` | G2 category | GENERATED manifest | resolve() | §8 target | manifest ≡ §8 hand-authored |
|---|---|---|---|---|---|---|
| **prospector** | `[google-maps, spatial-db]` | `geospatial` | `{category: geospatial, delta: {}}` | **8** | §8.1 ✓ | ✓ |
| **scienceclaw** | `[document-parsing]` | `document-consuming` | `{category: document-consuming, delta: {}}` | **6** | §8.2 ✓ | ✓ |
| **labstat_bls** | `[document-parsing, bls-oews]` | `document-consuming` | `{category: document-consuming, delta: {add: [{thirdparty_rest_key, BLS_OEWS_API_KEY}]}}` | **7** | §8.3 ✓ | ✓ |

All 8/6/7 resolved sets are **byte-for-byte equal** to the §8.1/§8.2/§8.3
expected sets (asserted in `run.py` against `fixtures.py`).

### labstat_bls load-bearing (§23.1 / §8.3)
- generated `delta.add == [(thirdparty_rest_key, BLS_OEWS_API_KEY)]` (mechanically derived per G3, not hand-authored);
- (i) resolved contains `(thirdparty_rest_key, BLS_OEWS_API_KEY)` ✓;
- (ii) **no** `(gcp_api, BLS_OEWS_API_KEY)` — the `bls-oews` record is `gcp_api: none`, so NO API is minted ✓;
- (iii) S1 `gcp_api` input = `['document-parsing', 'gemini-embedding', 'gemini-search']` — excludes BLS_OEWS_API_KEY (NO gcloud-enable) ✓.

## V1–V5 validation (§20) — all PASS on every generated manifest
- **V1** every-service-cataloged ✓ — **V2** complete (`resolve(gen) ⊇ called_entries`) ✓ — **V3** minimal (no uncalled non-baseline entry) ✓ — **V4** resolve-well-formed (REUSES §2.6 + §3.4 guards) ✓ — **V5** no-undeclared-drift ✓ (× prospector, scienceclaw, labstat_bls).

## Negative probes (fail-closed)
- **NEG-1** — scanner detects an UNDECLARED `bls-oews` against prospector's declaration → **V5 FAILS** ("shadow service(s) detected but not declared: ['bls-oews']"). Fail-closed drift ✓.
- **NEG-2** — a declared service NOT in the catalog (`totally-uncataloged-svc`) → `generate()` **RAISES `UncatalogedServiceError`** (G1 fail-closed, no emit) AND **V1 FAILS** naming the uncataloged service ✓.

## Regression (the §2 constraint — resolver untouched)
`python resolution-check/run.py` re-run → **exit 0**: §8.1/§8.2/§8.3 still resolve
to 8/6/7 byte-for-byte; §8.4 still raises `BaselineOmitError`; §3.4
runtime-completeness + §5.A SA-scope still hold. The resolver and its fixtures
are textually unchanged by this stage.

## Grounding note (spec faithfulness — NO fudge)
- §23.1 generation produces category `document-consuming` for labstat_bls; §8.3's
  *hand-authored* fixture used the alias `document/data`. Per §22 only
  `geospatial` + `document-consuming` are seeded as emergent categories, so a
  faithful G2 (max-subset over the seeded categories) selects `document-consuming`
  — exactly as §23.1 lines 1318–1322 state. Because `document/data` is a
  byte-identical **alias** of `document-consuming` (§3.2 / WP-4), both resolve to
  the same 7-entry set, so the generated manifest is **equivalent** to the §8.3
  hand-authored manifest (asserted alias-aware in `run.py:_manifests_equivalent`).
  This is a faithful reproduction of §23.1, not a deviation. **No spec discrepancy.**

**Self-report is NOT verification.** VERA re-runs independently next (gauntlet stage 4/6).
