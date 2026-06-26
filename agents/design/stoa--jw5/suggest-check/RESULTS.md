# suggest-check — RESULTS (stoa--jw5, u--9s2 Phase-1)

- author: Denson Smith
- seat-built-by: CAPTAIN_ADA_the_stoa (EXECUTOR), gauntlet stage 3/6 (BUILD + exercise)
- design-ground-truth: `agents/design/stoa--jw5/design-formal.md` §24–§31 (the SUGGEST front-door)
- as_of: 2026-06-26
- run: `python run.py` (exit 0 = all held)

> Self-report is NOT verification. VERA re-runs this harness independently and adds the
> fail-closed safety probe at stage 4/6. This file captures what ADA's build produced + ran.

## What this harness exercises

The SUGGEST front-door (§24–§31), which is strictly **UPSTREAM of DECLARE (§18)**:

```
PROJECT signals → suggest() [§24 examine→match catalog detection_hints §25→propose+evidence]
   → proposed set (INERT, recommendation-only)
   → confirm() [§26 FAIL-CLOSED human gate: D := confirm(P), the ONLY PROPOSE→DECLARE edge]
   → confirmed DECLARE set  ═══ IS the §18 DECLARE ═══▶
       generate() [Part-2 §19, UNCHANGED] → resolve() [Part-1 §2, UNCHANGED] → 8/6/7
```

**The §2 constraint (load-bearing):** `generate.py` (Part-2 §19) and `resolve.py` (Part-1 §2) are
imported from `../discovery-check` and `../resolution-check` **UNMODIFIED** — never reimplemented,
never edited. Feeding the confirmed DECLARE into the unchanged `generate()→resolve()` and getting
8/6/7 (== the §23 DECLARE sets byte-for-byte) **IS** the proof that SUGGEST is purely upstream.

## Files (this dir)

- `catalog_hints.py` — the §22 seed catalog EXTENDED with §25 `detection_hints`
  (`sdk_imports`/`url_patterns`/`config_keys`/`data_signals`) for the four §29 services
  (google-maps, spatial-db, document-parsing, bls-oews). `entries` (the hard recipe) byte-identical
  to `discovery-check/catalog.py`; hints are ADVISORY (§25.1).
- `suggest.py` — `suggest(project_signals, catalog) → (proposed, evidence, unknown)` per §24:
  examine 4 surfaces → match detection_hints → propose (catalog-bounded; uncataloged signal → flagged
  "unknown — add to catalog", the §20 V1 lineage). Recommendation-only; reads `detection_hints` only,
  never `entries`.
- `confirm.py` — `confirm(proposed, human_action) → DECLARE | ⊥(INERT)` per §26 FAIL-CLOSED.
  `D := confirm(P)`: CONFIRM → P; EDIT-then-CONFIRM → P'; REJECT / no-response / edits-pending / None /
  any unrecognized action → ⊥ (INERT, fail-closed default). NO auto-promotion path.
- `run.py` — the harness: examine → suggest → confirm → DECLARE → unchanged generate→resolve →
  ASSERT 8/6/7 AND DECLARE == §23, plus the three safety probes.

## Results — ALL 35 checks PASS (exit 0)

### §29.1 — three worked examples VIA SUGGEST (regression target 8/6/7)

| builder | examine signals | suggest()→proposed | confirm | DECLARE (== §23) | generate→resolve |
|---|---|---|---|---|---|
| prospector  (§8.1) | Maps-JS sdk_import + maps url_pattern + spatial-data signal | `[google-maps, spatial-db]` | accept | `[google-maps, spatial-db]` ✓ | **8** ✓ |
| scienceclaw (§8.2) | doc-parse sdk_import + parse url_pattern | `[document-parsing]` | accept | `[document-parsing]` ✓ | **6** ✓ |
| labstat_bls (§8.3) | doc-parse sdk + **BLS url_pattern + BLS config_key** | `[bls-oews, document-parsing]` | accept | `[bls-oews, document-parsing]` ✓ | **7** ✓ |

- Each DECLARE is **byte-identical** to the §23 `services:` set; each carries per-candidate evidence;
  no spurious uncataloged signal in the worked-example examine.
- **labstat_bls load-bearing (the DWP-3 upgrade):** the agent **inferred** `bls-oews` from a BLS
  `url_pattern` (`api.bls.gov`) + `config_key` (`BLS_OEWS_API_KEY`) signal **with NO SDK import** —
  exactly the runtime-config/dynamic case declaration-from-memory might miss. Resolved set contains
  `(thirdparty_rest_key, BLS_OEWS_API_KEY)` and carries **NO** `(gcp_api, BLS_OEWS_API_KEY)`
  (bls-oews is `gcp_api: none` → no `gcloud enable`), reproducing §8.3 exactly.

### SAFETY (a) — §29.2 FAIL-CLOSED no-confirm branch (the load-bearing safety case)

The same prospector proposal `[google-maps, spatial-db]`, human does NOT confirm. For **all four**
no-confirm actions — REJECT, no-response, edits-pending, None:

- `confirm()` → **⊥ (INERT)** — NO DECLARE produced (proposal NOT silently promoted), AND
- the INERT result **NEVER reaches `generate()`** — the harness's downstream branch is gated on
  `is_declare(result)` and stays dark; nothing flows to §18/§19/§20/§2/§4 → **nothing provisions**.

This is the structural safety net: the §26 human-confirm gate is the only PROPOSE→DECLARE edge and it
is fail-closed. The `INERT` sentinel is also falsy, so a naive `if declare:` guard fails closed too.

### SAFETY (b) — OVER-PROPOSAL (hallucination) caught by confirm

A scienceclaw project with a stray `maps.googleapis.com` URL (a mock / aspiration the code never
calls, §28) → suggest() **over-proposes** `google-maps`. The human **removes** it in confirm
(EDIT-then-CONFIRM) → DECLARE `[document-parsing]` (no bloat) → resolve **== 6** (§8.2), with **NO**
`google-maps` / `MAPS_API_KEY` over-provisioned. §25.1 holds: a wrong hint can only mis-propose.

### SAFETY (c) — UNDER-PROPOSAL caught by confirm

A labstat_bls project where the agent **misses** the BLS endpoint (too dynamic to trace, §28) →
suggest() proposes only `[document-parsing]`. The human **adds** `bls-oews` in confirm → DECLARE
`[bls-oews, document-parsing]` → resolve **== 7** (§8.3), with `BLS_OEWS_API_KEY` present (no
under-provision).

### REGRESSION — Part-1 + Part-2 re-run, both PASS

- `discovery-check/run.py` → **PASS (exit 0)** — generation §19 still hits 8/6/7; V1–V5 held;
  negative probes fail-closed.
- `resolution-check/run.py` → **PASS (exit 0)** — all §8 fixtures reproduced; §8.4 BaselineOmitError
  raised; runtime-completeness + SA-scope held.

### §2 CONSTRAINT — generate.py + resolve.py REUSED UNMODIFIED

Confirmed two ways:
1. **mtime no-write proof** — pre-build vs post-build mtimes byte-identical:
   `generate.py` 1782442907 · `catalog.py` 1782442882 · `resolve.py` 1782424623 · `fixtures.py` 1782424640
   (and `git status` shows only `suggest-check/` new under this seat).
2. **in-harness provenance** — `resolve.__module__`/`__file__` resolves to `../resolution-check/resolve.py`
   and `generate.__module__`/`__file__` resolves to `../discovery-check/generate.py`.

## Spec discrepancy

**None.** The faithful §24/§25/§26/§29 implementation produced DECLARE sets that, via the UNCHANGED
`generate()→resolve()`, hit the §29/§8 expected 8/6/7 with no fudging. The §22 `bls-oews` record's
`category: none` (per-builder special riding `delta.add`) and the §3.4 `google-maps`+`MAPS_API_KEY`
pairing both reproduce exactly through the unchanged downstream.

## Full run transcript

```
============================================================================================
stoa--jw5 suggest-check — exercising the SUGGEST->CONFIRM->DECLARE front-door (§24-§31)
design: agents/design/stoa--jw5/design-formal.md §24-§31  |  generate()+resolve() REUSED unmodified
============================================================================================

--- §29.1 SUGGEST FRONT-DOOR: examine -> suggest -> confirm -> DECLARE == §23 -> resolve == 8/6/7 ---
  [PASS] prospector  (§29.1/§8.1): suggest() proposed == §23 service set ['google-maps', 'spatial-db']
  [PASS] prospector  (§29.1/§8.1): every proposed service carries detection-hint evidence
  [PASS] prospector  (§29.1/§8.1): no unknown (uncataloged) signal in the worked-example examine
  [PASS] prospector  (§29.1/§8.1): confirm(accept) -> DECLARE produced (not INERT)
  [PASS] prospector  (§29.1/§8.1): DECLARE == §23 set ['google-maps', 'spatial-db'] (byte-identical)
  [PASS] prospector  (§29.1/§8.1): generate(DECLARE)->resolve() == 8 entries (§8 target HIT)
  [PASS] scienceclaw (§29.1/§8.2): suggest() proposed == §23 service set ['document-parsing']
  [PASS] scienceclaw (§29.1/§8.2): every proposed service carries detection-hint evidence
  [PASS] scienceclaw (§29.1/§8.2): no unknown (uncataloged) signal in the worked-example examine
  [PASS] scienceclaw (§29.1/§8.2): confirm(accept) -> DECLARE produced (not INERT)
  [PASS] scienceclaw (§29.1/§8.2): DECLARE == §23 set ['document-parsing'] (byte-identical)
  [PASS] scienceclaw (§29.1/§8.2): generate(DECLARE)->resolve() == 6 entries (§8 target HIT)
  [PASS] labstat_bls (§29.1/§8.3): suggest() proposed == §23 service set ['bls-oews', 'document-parsing']
  [PASS] labstat_bls (§29.1/§8.3): every proposed service carries detection-hint evidence
  [PASS] labstat_bls (§29.1/§8.3): no unknown (uncataloged) signal in the worked-example examine
  [PASS] labstat_bls (§29.1/§8.3): confirm(accept) -> DECLARE produced (not INERT)
  [PASS] labstat_bls (§29.1/§8.3): DECLARE == §23 set ['bls-oews', 'document-parsing'] (byte-identical)
  [PASS] labstat_bls (§29.1/§8.3): generate(DECLARE)->resolve() == 7 entries (§8 target HIT)

--- §29.1 labstat_bls load-bearing: agent INFERS bls-oews from URL/config (the DWP-3 upgrade) ---
  [PASS] labstat_bls: bls-oews PROPOSED (inferred from BLS url_pattern + config_key, no SDK import)
  [PASS] labstat_bls: bls-oews evidence cites the url_pattern AND/OR config_key signal
  [PASS] labstat_bls: resolved contains (thirdparty_rest_key, BLS_OEWS_API_KEY)
  [PASS] labstat_bls: NO (gcp_api, BLS_OEWS_API_KEY) — bls-oews is gcp_api:none (no gcloud-enable)

--- SAFETY (a): §29.2 FAIL-CLOSED no-confirm branch -> ⊥ INERT -> NOTHING flows downstream ---
  [PASS] no-confirm: suggest() still PROPOSES [google-maps, spatial-db] (proposal is INERT)
  [PASS] no-confirm/REJECT: confirm() -> ⊥ INERT (NO DECLARE produced)
  [PASS] no-confirm/REJECT: INERT NEVER reaches generate() (downstream stays dark)
  [PASS] no-confirm/no-response: confirm() -> ⊥ INERT (NO DECLARE produced)
  [PASS] no-confirm/no-response: INERT NEVER reaches generate() (downstream stays dark)
  [PASS] no-confirm/edits-pending: confirm() -> ⊥ INERT (NO DECLARE produced)
  [PASS] no-confirm/edits-pending: INERT NEVER reaches generate() (downstream stays dark)
  [PASS] no-confirm/None: confirm() -> ⊥ INERT (NO DECLARE produced)
  [PASS] no-confirm/None: INERT NEVER reaches generate() (downstream stays dark)

--- SAFETY (b): OVER-PROPOSAL (hallucinated extra service) -> human REMOVES -> not in DECLARE ---
  [PASS] over-proposal: suggest() OVER-proposes google-maps (hallucinated from a stray maps URL)
  [PASS] over-proposal: human EDIT removes google-maps -> DECLARE == [document-parsing] (no bloat)
  [PASS] over-proposal: resolve(DECLARE) == 6 (§8.2) — NO google-maps/MAPS_API_KEY over-provisioned

--- SAFETY (c): UNDER-PROPOSAL (agent misses a called service) -> human ADDS -> in DECLARE ---
  [PASS] under-proposal: suggest() MISSES bls-oews (only [document-parsing] proposed)
  [PASS] under-proposal: human EDIT adds bls-oews -> DECLARE == [bls-oews, document-parsing]
  [PASS] under-proposal: resolve(DECLARE) == 7 (§8.3) — BLS_OEWS_API_KEY present (no under-provision)

--- §2 CONSTRAINT: generate() + resolve() reused UNMODIFIED (SUGGEST is purely upstream) ---
  [PASS] resolve is the imported Part-1 callable (module from ../resolution-check)
  [PASS] generate is the imported Part-2 callable (module from ../discovery-check)

============================================================================================
RESULT: PASS — SUGGEST->CONFIRM->DECLARE front-door produced the §23 DECLARE sets byte-identical,
        which the UNCHANGED generate()->resolve() resolved to 8/6/7 (§8.1/8.2/8.3);
        FAIL-CLOSED no-confirm branch -> ⊥ INERT -> nothing flowed downstream (§29.2);
        over-proposal removed by confirm (no bloat); under-proposal added by confirm (no under-provision);
        generate.py + resolve.py REUSED UNMODIFIED (SUGGEST is purely upstream of DECLARE).
============================================================================================
```
