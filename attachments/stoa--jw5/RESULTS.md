---
author: Denson Smith
ticket: stoa--jw5 (u--9s2 Phase-1)
seat: CAPTAIN_ADA_the_stoa (EXECUTOR)
design: agents/design/stoa--jw5/design-formal.md
as_of: 2026-06-25
status: harness built + exercised; ADA self-report (NOT verification — VERA re-runs)
---

# stoa--jw5 resolution-check — run results

Exercises the design's testable core (`resolve()` per §2.5) against the §8 worked-example
fixtures so the central claim — the resolution rule — is **falsifiable**. **Provisions nothing**
(no gcloud, no Railway, no credentials; pure logic, reads no environment per §2.3).

This is the EXECUTOR's build-confirmation run. It is **not** the gauntlet's verification —
VERA re-runs this harness and adds threat-coverage probes (M1–M4/M6 attack-paths) independently.

## Harness

| file | role |
|---|---|
| `resolve.py` | `resolve(manifest, BASELINE, LIBRARY)` (§2.5 verbatim) + `derive_sa_scope` (§5.A) + `check_runtime_completeness` (§3.4); BASELINE (§3.1) + category library (§3.2) encoded as data; `BaselineOmitError` / `ResolutionError` (§2.4). |
| `fixtures.py` | the 4 §8 manifests + the 3 EXACT expected resolved sets (verbatim from §8). |
| `run.py` | runs all 4 fixtures; asserts exact-match positives, the §8.4 fail-closed raise, runtime-completeness, kind-dispatch, and SA-scope derivation. |

Run: `python run.py` (exit 0 = all checks held). Build-check: `python -m py_compile resolve.py fixtures.py run.py` → exit 0.

## Per-fixture result

| fixture | manifest | expected | got | match |
|---|---|---|---|---|
| §8.1 prospector | `{geospatial, delta:{}}` | 8 entries | 8 entries | **PASS (exact)** |
| §8.2 scienceclaw | `{document-consuming, delta:{}}` | 6 entries | 6 entries | **PASS (exact)** |
| §8.3 labstat_bls | `{document/data, add:[thirdparty_rest_key BLS_OEWS_API_KEY]}` | 7 entries | 7 entries | **PASS (exact)** |
| §8.4 badbuilder_pgvector_omit | `{document-consuming, omit:[db_extension pgvector]}` | RAISE `BaselineOmitError` | raised, no set returned | **PASS (fail-closed)** |

All three positives reproduced **byte-for-byte** from a faithful §2.5 implementation; the
sorted resolved set equals the §8 enumeration exactly.

## Per-check result (19 checks, all PASS)

- **§8.4 negative (3):** (i) raises `BaselineOmitError` (named, not generic) with message
  `omit targets non-omittable baseline entry/entries: [('db_extension', 'pgvector')]`;
  (ii) no resolved set returned (fail-closed — no partial set); (iii) message names
  `(db_extension, pgvector)`.
- **§3.4 runtime-completeness (5):** holds for all 3 positives; prospector contains BOTH
  `(gcp_api, google-maps)` AND `(gcp_secret, MAPS_API_KEY)` (the §8.1 probe).
- **§8.3 kind-dispatch (3):** resolved set contains `(thirdparty_rest_key, BLS_OEWS_API_KEY)`;
  ZERO `(gcp_api, BLS_OEWS_API_KEY)` (delta added no API); S1 `gcp_api` input list
  `['document-parsing','gemini-embedding','gemini-search']` excludes `BLS_OEWS_API_KEY`.
  Proves **delta ≠ template bloat** and `kind`-dispatch correctness.
- **§5.A SA-scope (6):** scope = scope-bearing subset (`gcp_api` + `gcp_secret` +
  `thirdparty_rest_key`); for every builder no entry outside its own resolved set appears in
  its derived scope (`railway_var` / `db_extension` correctly excluded).

## R1-close generalization (FM watch-item)

Beyond §8.4 (pgvector), the `BaselineOmitError` guard was exercised against an `omit` of **each
of the 5 §2.6 non-omittable baseline entries** — all 5 raise:
`(gcp_api, gemini-embedding)`, `(gcp_api, gemini-search)`, `(railway_var, DATABASE_URL)`,
`(gcp_secret, POSTGRES_PASSWORD)`, `(db_extension, pgvector)`. The guard generalizes (it is
derived from the baseline record, §2.6), so it covers every current and future baseline entry.

## Spec discrepancy

**None.** A faithful implementation of the §2.5 algorithm reproduces every §8 expected set
exactly (8 / 6 / 7) and raises the named `BaselineOmitError` on §8.4 — no fudging, no
spec-vs-fixture gap, no algorithm ambiguity surfaced.
