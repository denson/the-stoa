---
author: Denson Smith
ticket: stoa--fdf (u--9s2 Phase-2 increment 2.2)
designed-by: CAPTAIN_DAEDALUS_the_stoa (ARCHITECT) — gauntlet stage 1/6
design-ground-truth: agents/design/stoa--jw5/design-formal.md §24–§31 (the SUGGEST front-door, authoritative WHAT/SHAPE)
upstream-2.1-core: agents/builder-deploy-core/ (builder_deploy_core — generate/resolve IMPORTED UNMODIFIED)
prototype-promoted-from: agents/design/stoa--jw5/suggest-check/ (35/35 PASS)
status: DESIGN-rev2 — AUTHORITATIVE artifact for ADA build + VERA verify + NOMOS close-gate (supersedes design-rev1.md)
supersedes: agents/design/stoa--fdf/design-rev1.md
as_of: 2026-06-26
---

# stoa--fdf — build design rev2: the SUGGEST front-door (u--9s2 Phase-2 increment 2.2)

> **rev2 is the authoritative artifact.** It is a full revised design (NOT a delta append): ADA builds
> against this file, VERA verifies against this file's §3 probe spec, NOMOS gates against this file. rev1
> (`design-rev1.md`) is superseded in full. The rev1→rev2 change-log is §0; the substantive changes are
> (1) the **WP-D2 fold** — the RATIFIED byte-unchanged shape: `load_catalog` is NOT edited; its tolerance is
> pinned by a regression test that fails LOUD on a future strict-key hardening (§2.3.1, §3 P5a, §6 WP-D2);
> (2) two **recorded dispositions** (WP-D3 ratified-not-under-delivery, WP-D4 named Layer-N egress residual
> — §0.2, §6); and (3) a **Phase-3/4 customer-repo-privacy escalation** of the Layer-N egress (§8, record-
> only). Everything else is rev1 held verbatim (ARGUS ratified it cold; not re-litigated).

---

## 0. rev1 → rev2 change-log (what moved, and what is held)

This revision folds exactly the one load-bearing item ARGUS surfaced (r1 / WP-D2) and records two
dispositions (r2 / WP-D3, r3 / WP-D4). **No other rev1 content is re-opened** — ARGUS ratified the
safety framing, the §2 import-unmodified constraint at source, SWP-1..4, all five §31 classifications,
and the §4 Decision #1 (application code, no HAMILTON) cold. Those stand verbatim.

### 0.1 The ONE load-bearing fold (ARGUS r1 / WP-D2) — pin `load_catalog`'s tolerance via a REGRESSION TEST; `load_catalog` BYTE-UNCHANGED

rev1 wired `detection_hints` onto catalog records by **relying on** `load_catalog` silently ignoring an
unknown TOML key (the `for key in ("service-id","entries","gcp_api","category")` loop reads only its four
required keys and never rejects extras — dataload.py:245-275). ARGUS verified this tolerance is real
**today** but flagged it as an **accident**: every OTHER load body in the package
(`load_baseline`/`load_kinds`, dataload.py:84-174) is **fail-closed-on-unknown via set-equality** (§2.4.1
discipline), so `detection_hints` would sit as the **one un-contracted additive key** in an otherwise
strict-key package. The natural next hardening — extending fail-closed to `load_catalog` — would reject the
`[detection_hints]` block and silently break the catalog load.

**rev2 fold (RATIFIED fold-shape — orchestrator-chain decision, bw stoa--fdf 2026-06-26T23:50/23:51Z):**
ARGUS's *risk* is real, but ARGUS's *proposed fix* (a strict-key allowlist **ON** `load_catalog`) would
**textually modify the 2.1 core**, which the §2 constraint (§0–§23 textually unchanged) **FORBIDS**.
Polybius_the_Stoa (via PLINY + the FM) RATIFIED a fold-shape that addresses the real risk **without editing
the core**:

1. **`load_catalog` is left BYTE-UNCHANGED.** No allowlist, no edit — the 2.1 core's `dataload.py`
   `load_catalog` is textually identical post-arc (§2-constraint honored; the FM verifies this before ADA).
2. **The tolerance is PINNED by a regression test** in the NEW suggest suite (`test_suggest.py` /
   `test_dataload.py` additive): `load_catalog` MUST continue to admit a catalog record carrying a
   `[detection_hints]` block (load it cleanly, return the unchanged 4-field record shape). **A future
   strict-key hardening of `load_catalog` that would reject `[detection_hints]` fails this test LOUD** —
   turning the rev1 silent-breakage risk into a loud, named regression tripwire instead of an accident.
3. **ALL `detection_hints` validation lives in the NEW `load_detection_hints` loader** (fail-closed §2.4.1
   on the hints body and its sub-keys) — `load_catalog` neither reads nor validates the hints.

This honors §2 (core byte-unchanged) **while** addressing ARGUS's real risk (the silent-break path is now a
loud test failure). Spec: §2.3.1. Probe: §3 P5a (the PIN regression check + the hints NEG check). Weak
point disposition: §6 WP-D2 (now PINNED-by-regression-test, not an open silent reliance).

### 0.2 Two recorded dispositions (not new design — on the record so they are not later mis-read)

- **WP-D3 (ARGUS r2 — ratified NOT under-delivery).** Directive piece #2 ("populate hints **beyond** the
  four §25.3 seed hints") names a verb the 2.2 catalog **cannot satisfy literally**: the 2.1 catalog ships
  **exactly** the four seed-covered services (google-maps, spatial-db, document-parsing, bls-oews) and no
  others (ARGUS verified at source). The faithful and ONLY deliverable of piece #2 is therefore: **(a)
  migrate the four seed-hint sets from the prototype's Python dict (`suggest-check/catalog_hints.py`) into
  real catalog TOML** `[detection_hints]` blocks, **(b) establish the R-3 catalog-authoring discipline**,
  and **(c) establish the `load_detection_hints` validation contract** as the durable mechanism by which
  ANY future cataloged service's hints get authored. This is recorded plainly (§2.3, §6 WP-D3) so NOMOS
  does not later read "only four services got hints" as under-delivery of piece #2 — there is nothing else
  to fill. **Status: ratified-up by PLINY/POLYBIUS; recorded here as the faithful read.**

- **WP-D4 (ARGUS r3 — one named residual).** The REPORTED neuro path (Layer N) sends project-repo excerpts
  to an external LLM — a genuinely-new external-egress surface the gated path never touches and that NONE
  of the gated probes (P1–P8) exercise. It is correctly **gate-inert and REPORTED-only** (cannot
  mis-provision; the §26 gate stands), so it is **NOT a new provisioning trust boundary** and does **not**
  change the §31 not-threat-ratified verdict. But because it is a distinct external-egress surface, it is
  **NAMED as one explicit residual** here (§6 WP-D4, §5 5th-row note) rather than absorbed silently:

  > **Named residual (R-egress):** *Layer-N proposal-channel egress — repo excerpts → external LLM
  > resolution; REPORTED-only, gate-inert, no provisioning authority.* It is on the record; it is not a
  > new provisioning trust boundary (§31 verdict unchanged); it carries no threat-anchored probe (§35.5,
  > §6.13 — REPORTED-only path, no runtime attack path, empty coverage set).

---

## 1. Problem restatement (the §6.1 pre-work gate)

Phase-1 ratified the SUGGEST front-door SHAPE (design-formal §24–§31) and a 35/35-PASS choreography
prototype (`suggest-check/`). Increment **2.1 shipped** the resolution+discovery core as the package
`builder_deploy_core`. This increment (2.2) **promotes the verified prototype into runnable, packaged
code** and builds the three genuinely-new Phase-2 pieces the design names:

1. the **examination/inference engine** (§28 neuro-symbolic shape) that examines a real project, extracts
   the four signal surfaces, matches the §25 `detection_hints`, and **PROPOSES** a catalog-bounded service
   set with per-candidate evidence — recommendation-only / **INERT**;
2. the **`detection_hints` catalog DATA** (§25.3 Phase-2 fill) for the cataloged services;
3. the **confirm-gate** (§26 fail-closed `D := confirm(P)`) built with an **anti-rubber-stamp,
   evidence-rich confirm-contract**;

then wires the confirmed DECLARE (tagged **P3**, §27) to the **UNCHANGED** 2.1 core
(`generate()→resolve()`), regression target **8 / 6 / 7**.

**Imported assumptions I am naming (not smoothing):**

- **(A-import-1, rev2) `load_catalog` admits `detection_hints` today, and that tolerance is PINNED by a
  regression test (the core is BYTE-UNCHANGED).** rev1 relied on `load_catalog` silently tolerating an
  additive key. The RATIFIED rev2 fold-shape (bw 23:50/23:51Z) does **not** edit `load_catalog` (that would
  violate the §2 constraint — §0–§23 textually unchanged); instead it **pins the existing tolerant behavior
  with a regression test** so a future strict-key hardening that would break `detection_hints` fails LOUD.
  The hints DATA ships as an **additive `[detection_hints]` block on the existing catalog records**, loaded
  and validated by a **separate NEW `load_detection_hints` loader**; `load_catalog` is untouched, reads the
  unchanged 4-field record, and `generate()` reads the unchanged catalog and never sees hints. The additive-
  key reliance that was rev1's load-bearing weak point (WP-D2) is now **a loud, named tripwire** instead of
  a silent accident. See §2.3.1.
- **(A-import-2) `generate`/`resolve` take DATA tables as arguments.** The 2.1 public API is
  `generate(services_called, catalog, categories, baseline)` and `resolve(manifest, baseline, library)`;
  the CALLER loads tables via `dataload`. SUGGEST therefore wires by loading the same tables and feeding
  the confirmed DECLARE into the unchanged callables — **no signature change, module-identity preserved.**
- **(A-import-3) The "examine" surface for the gated DoD is a deterministic fixture, not live LLM
  inference.** Per the §28 safety framing the engine's accuracy is REPORTED-not-gated; the gated
  choreography (DoD#1/#6) runs on the **§29.1 project fixtures** (small real repos) through a
  **deterministic symbolic examiner**. The neuro (LLM) component is an additive enrichment path that is
  REPORTED (DoD#9) and never gates the arc. This keeps the gated suite hermetic (no network, no model
  call) — consistent with the 2.1 core's purity discipline.

The restatement **converges** with the directive; no divergence to surface. The one place it adds scope the
directive left implicit is (A-import-1, rev2)/(A-import-3) — the loader-contract wiring mechanism and the
deterministic-examiner split — both named here and carried as weak points for ARGUS.

---

## 2. Approach — the build's shape

### 2.0 The load-bearing constraint (held absolutely, restated)

SUGGEST is **strictly UPSTREAM of DECLARE (§24.0)**. The **§0–§23 mechanism stands textually unchanged**:
`generate`/`resolve`/`validate` are **IMPORTED from `builder_deploy_core` UNMODIFIED** (module-identity,
NOT a copy). V1–V5 are not weakened. The **§8 sets (8/6/7) are a REGRESSION TARGET — hit, not re-derived.**
**SAFETY rests ENTIRELY on the §26 fail-closed confirm gate + the unchanged V1–V5.** The engine's accuracy
is a **USEFULNESS** claim, **NEVER** a safety claim; the design makes **NO suggest-completeness claim** and
**gates nothing on an accuracy number**. A weak or absent engine leaves the system **SAFE** (it only
degrades SUGGEST to a weaker effort-saver).

#### 2.0.1 §2-constraint compliance of the rev2 WP-D2 fold — `load_catalog` is BYTE-UNCHANGED (NOMOS-verifiable; FM-verified pre-ADA)

The RATIFIED rev2 WP-D2 fold-shape (bw 23:50/23:51Z) does **NOT** edit `load_catalog` — precisely so the §2
constraint is honored at the byte level. Stated explicitly for NOMOS and the FM's pre-ADA §2 verify:

- **`load_catalog` is left textually identical to the 2.1 core.** The fold does NOT add an allowlist, a
  strict-key check, or any other edit to `load_catalog` (dataload.py:224-302). A future strict-key hardening
  ON `load_catalog` would have textually modified the core — which the §2 constraint (§0–§23 textually
  unchanged) FORBIDS — so the fold deliberately AVOIDS that path. **The FM verifies `load_catalog` /
  `dataload.py`'s existing functions are byte-unchanged before ADA builds** (a `git diff` over the 2.1
  loader functions shows ONLY the additive `load_detection_hints` function appended, no edit to existing
  functions).
- **The ONLY `dataload.py` change is the ADDITIVE NEW function `load_detection_hints`.** It is appended as a
  sibling loader; it adds no edit to any existing 2.1 function. Appending a new function does not modify the
  existing `load_catalog`/`load_baseline`/`load_kinds`/`load_library` text — those remain byte-for-byte the
  2.1 core. (If the FM's §2 verify is interpreted strictly enough that even appending a function to
  `dataload.py` is a "core file edit," `load_detection_hints` can instead live in a NEW module
  `builder_deploy_core/suggest/hints_load.py` — DAEDALUS's default is the `dataload.py` sibling for
  cohesion, but the byte-unchanged guarantee on the EXISTING functions holds either way; see §2.3 loader
  note. The FM's call.)
- **V1–V5, the §0–§23 mechanism, and `generate`/`resolve` are textually untouched** — they live in
  `resolve`/`generate`/the discovery+resolution modules, imported unmodified, none of which sees
  `detection_hints`.
- **The 8/6/7 regression target is unaffected.** `generate(D, catalog, categories, baseline)` reads the
  same `catalog`/`categories` `load_catalog` has always produced (unchanged loader, unchanged output). P1
  (8/6/7 byte-identical) and P3 (module-identity) both pass by construction. P7 (full 2.1 suite) asserts
  `load_catalog` still produces the identical 4-record catalog.

**Net:** the §2-frozen surfaces (`generate`/`resolve` + §0–§23) AND `load_catalog` itself are **textually
untouched**. The real risk ARGUS named is addressed by a REGRESSION TEST (§2.3.1) that pins the tolerance,
not by editing the core.

### 2.1 Module layout + file plan (what gets promoted where)

**HOME decision (§4-adjacent, ratified-neutral per directive §6):** the SUGGEST code lands **under the 2.1
package home `agents/builder-deploy-core/`**, as a new sibling sub-package `suggest/` inside
`builder_deploy_core`. Rationale: SUGGEST imports `generate`/`resolve` from this package; co-locating keeps
the import a same-package reference (no path gymnastics), keeps one test suite, and keeps the
`detection_hints` DATA next to the `entries` DATA it advises on (the same catalog records). This is **not**
one of the three §4 decisions routed up — the directive pre-ratifies this home "unless DAEDALUS proposes
otherwise," and I do not propose otherwise. I record it here so ADA/ARGUS see the choice and its reason.

```
agents/builder-deploy-core/
  builder_deploy_core/
    __init__.py                    # (UNCHANGED) 2.1 exports generate/resolve/validate/…
    dataload.py                    # (ADDITIVE ONLY) + load_detection_hints() appended as a sibling loader;
                                   #   load_catalog + ALL existing 2.1 functions BYTE-UNCHANGED (rev2 WP-D2
                                   #   fold pins the tolerance via a regression test, does NOT edit the core, §2.3.1)
    resolution/ …                  # (UNCHANGED — 2.1 core; resolve imported unmodified)
    discovery/ …                   # (UNCHANGED — 2.1 core; generate.py reads entries only, never hints)
    suggest/                       # NEW sub-package — the SUGGEST front-door
      __init__.py                  # exports: suggest, confirm, is_declare, INERT, examine, declare_from_confirm
      suggest.py                   # §24 S-2/S-3: examine output → match detection_hints → propose+evidence
                                   #   PROMOTED from suggest-check/suggest.py (logic verbatim; import path fixed)
      confirm.py                   # §26 fail-closed gate: D := confirm(P); the evidence-rich contract (§2.5)
                                   #   PROMOTED from suggest-check/confirm.py (logic verbatim) + the contract layer
      examine.py                   # NEW §28 engine: the symbolic examiner (deterministic) + the neuro hook
      evidence.py                  # NEW §2.5: the per-candidate evidence record + the gate-presentation contract
      declare.py                   # NEW §27 wiring: confirmed set → P3-tagged DECLARE → generate()→resolve()
  data/
    catalog/
      google-maps.toml             # (+ ADDITIVE [detection_hints] block) — entries/gcp_api/category UNCHANGED
      spatial-db.toml              # (+ ADDITIVE [detection_hints] block)
      document-parsing.toml        # (+ ADDITIVE [detection_hints] block)
      bls-oews.toml                # (+ ADDITIVE [detection_hints] block)
  tests/
    conftest.py                    # (+ ADDITIVE) detection_hints fixture handle; suggest path; fixtures dir
    test_dataload.py               # (UNCHANGED 2.1) + ADDITIVE detection_hints load-validation tests
                                   #   + ADDITIVE load_catalog TOLERANCE-PIN regression test (rev2 WP-D2, P5a) —
                                   #   asserts load_catalog admits [detection_hints]; future strict-key break fails LOUD
    test_discovery.py              # (UNCHANGED 2.1)
    test_resolution.py             # (UNCHANGED 2.1)
    test_suggest.py                # NEW — the SUGGEST probe suite (§3 probe-spec, the 35-check floor + new)
    fixtures/
      suggest-projects/            # NEW §29.1 project fixtures — small REAL repos carrying the §29.1 signals
        prospector/   …            # geo project: Maps-JS import + maps URL + spatial-data flow
        scienceclaw/  …            # doc-consuming: document-parsing SDK import + parse URL
        labstat_bls/  …            # doc/data: document-parsing SDK + BLS REST URL + BLS_OEWS_API_KEY config
        over-proposal/ …           # scienceclaw + a STRAY maps URL (mock/aspiration the code never calls)
        under-proposal/ …          # labstat_bls but the BLS endpoint is built too dynamically to trace
```

**Promotion note (the only logic-byte edits vs the prototype):** the three prototype files
(`suggest.py`, `confirm.py`, `catalog_hints.py`) move into the package. `suggest.py`/`confirm.py` carry
their algorithm **verbatim** — only the import path changes (the prototype's
`from catalog_hints import …` becomes loading `detection_hints` via `dataload`), exactly mirroring how
2.1's `generate.py` was promoted (logic verbatim, only `UncatalogedServiceError` import moved). The
prototype's `catalog_hints.py` (a Python dict) is **NOT** promoted as code — its DATA migrates into the
catalog TOMLs as additive `[detection_hints]` blocks (§2.3), which is the directive's "DATA, not code"
shape for piece #2.

### 2.2 The examination/inference engine (§28 neuro-symbolic) — `examine.py`

The engine produces the `project_signals` dict the verified `suggest()` already consumes:
`{ sdk_imports, url_patterns, config_keys, data_signals }`. It is a **two-layer** design with a hard
boundary between them:

**Layer S (symbolic — deterministic, gated):** examines a project directory and extracts the four signal
surfaces from static evidence, with **no network and no model call**:
- **sdk_imports** — parse each source file's **AST** and collect import nodes (Python `Import`/`ImportFrom`;
  JS/TS `import`/`require`). AST, **not grep** — so commented-out imports and string-literal mentions are
  NOT falsely flagged (the web-verified §28 discipline, gsearch 2026-06-26).
- **url_patterns** — scan string literals in the AST for hostname/endpoint patterns (the outbound-call
  targets). Static literal extraction only; the dynamic-resolution case is the neuro layer's job.
- **config_keys** — collect env-var / config-key reads (`os.environ[...]`, `process.env.*`, `.env` keys).
- **data_signals** — file-type / resource signals (e.g. a `.geojson`, a PostGIS migration, an OCR call).

Layer S is a **pure function of the project directory** (a fixture path). It reads files under that one
directory and nothing else — the same single-filesystem-boundary discipline the 2.1 `dataload` enforces.

**Layer N (neuro — LLM, REPORTED-only, NEVER gated):** an **optional enrichment** that resolves
dynamically-built endpoints Layer S cannot trace (`https://{env.TENANT}.api…/v2`-style) and reconciles
README/OpenAPI intent. Layer N's output is **merged into the same `project_signals` dict**, tagged with a
`source: neuro` provenance so REPORTED accuracy (DoD#9) can attribute which signals came from the LLM. **Layer
N is never invoked by the gated suite** (DoD#1/#6 run Layer S on the fixtures); it runs only for the
REPORTED scienceclaw-real-repo baseline (DoD#9). This is the §28 USEFULNESS/safety split made structural:
the gated path is hermetic and deterministic; the probabilistic path is reported, never a gate. **Layer N is
the named R-egress residual (§0.2 WP-D4): repo excerpts → external LLM, REPORTED-only, gate-inert.**

**The engine NEVER reaches `entries`.** `examine()` → `suggest()` read `detection_hints` only. The matched
proposal is **INERT** — it has no downstream effect until the §26 gate ratifies it.

> **Engine API:** `examine(project_dir, *, neuro=False) -> project_signals`. With `neuro=False` (the gated
> default) only Layer S runs. `suggest(examine(project_dir), detection_hints) -> (proposed, evidence,
> unknown)` is the verified prototype function, unchanged.

### 2.3 The `detection_hints` catalog DATA (§25.3 Phase-2 fill) — additive TOML blocks

Each cataloged service's TOML gains an **additive optional** `[detection_hints]` block. The block is
ADVISORY (§25.1): a wrong/missing hint can only mis-PROPOSE, never mis-provision (provisioning rides the
unchanged `entries`). The four §29-exercised services carry the seed hints already proven in the prototype's
`catalog_hints.py` (transcribed into TOML verbatim); the **Phase-2 fill** is making these real catalog DATA
(not a Python dict) and authoring them under the **R-3 catalog-authoring discipline** (arc-reviewed,
§23.4/§31 lineage). Example (google-maps.toml, the `entries`/`gcp_api`/`category` keys UNCHANGED):

```toml
service-id = "google-maps"
gcp_api = "google-maps"
category = "geospatial"

[[entries]]                          # (UNCHANGED — the HARD recipe, §17.1)
kind = "gcp_api"
name = "google-maps"
[[entries]]
kind = "gcp_secret"
name = "MAPS_API_KEY"

[detection_hints]                    # NEW — ADVISORY recognition signals only (§25); load_catalog tolerates
                                     #   it today (byte-unchanged), the tolerance pinned by a regression test (§2.3.1)
sdk_imports  = ["@googlemaps/js-api-loader", "google.maps", "@react-google-maps/api"]
url_patterns = ["maps.googleapis.com", "maps.gstatic.com"]
config_keys  = ["GOOGLE_MAPS_API_KEY", "MAPS_API_KEY", "NEXT_PUBLIC_MAPS_KEY"]
data_signals = ["client-side-map-render", "map-tile-fetch"]
```

**Loader (`dataload.load_detection_hints`)** — ADDITIVE, appended to `dataload.py` as a sibling of
`load_catalog` (or, at the FM's §2-verify call, a new `suggest/hints_load.py` module — §2.0.1), reading the
same `data/catalog/*.toml`. **ALL `detection_hints` validation lives HERE** (the RATIFIED fold-shape:
`load_catalog` is byte-unchanged and does no hints validation). It validates fail-closed (the 2.1 §2.4.1
discipline): each `[detection_hints]` block, if present, is a table whose **keys are a subset of the closed
set `{sdk_imports, url_patterns, config_keys, data_signals}`** (any subset, including empty), each present
key an array of non-empty strings; an **unknown key UNDER `[detection_hints]` raises `DataIntegrityError`**;
a service-id with no block is allowed (the field is optional). It returns `{ service_id: {sdk_imports,
url_patterns, config_keys, data_signals} }` — the structure `suggest()` consumes. The two loaders read the
same files for different keys (hint-agnostic generation, §25.2 invariant 1): `load_catalog` (UNCHANGED)
reads the four record fields and ignores the `detection_hints` block exactly as it does today;
`load_detection_hints` reads + validates ONLY the `detection_hints` block.

> **The Phase-2 "fill beyond the four seeds" — recorded disposition (WP-D3, ratified-up):** the directive's
> piece #2 says populate hints "beyond the four §25.3 seed hints the worked examples exercise." The 2.1
> catalog ships exactly the four cataloged services (google-maps, spatial-db, document-parsing, bls-oews) —
> there are **no other cataloged services to fill** at 2.2 (ARGUS verified at source). The honest Phase-2
> deliverable is therefore: (a) migrate the four seed-hint sets from the prototype Python dict into real
> catalog DATA (TOML) under R-3, and (b) establish the **R-3 catalog-authoring discipline + the
> `load_detection_hints` validation contract** as the durable mechanism by which any future cataloged
> service's hints are authored. **This is the faithful read of piece #2, ratified up so NOMOS does not read
> "only four services got hints" as under-delivery** — there is nothing else to fill. Carried as WP-D3 (§6).

#### 2.3.1 The `load_catalog` tolerance PIN — the rev2 WP-D2 fold (regression test, core BYTE-UNCHANGED)

This is the one load-bearing rev2 change, in the RATIFIED fold-shape (bw 23:50/23:51Z). The risk ARGUS
named is real: `load_catalog` currently admits the `[detection_hints]` block only by a **required-keys-
present check** (it asserts the four required keys are PRESENT, then ignores any other key — dataload.py:
245-275), NOT by the strict-key set-equality the rest of the §2.4.1 package uses; a **future** strict-key
hardening of `load_catalog` would **silently** reject `[detection_hints]` and break the catalog load.

**The fix does NOT edit `load_catalog`** (that would textually modify the §2-frozen core). Instead it
**pins the existing tolerant behavior with a REGRESSION TEST** so the silent-break path becomes a LOUD,
named test failure:

**The PIN (a regression test in the NEW suggest suite — `test_dataload.py` / `test_suggest.py` additive):**
> `test_load_catalog_admits_detection_hints` — load a catalog (the real 4-record catalog, each carrying its
> `[detection_hints]` block) through the **UNCHANGED** `load_catalog`, and assert: **(a)** the load succeeds
> (no `DataIntegrityError`); **(b)** all four records load; **(c)** each record's returned shape is the
> unchanged `{entries, gcp_api, category}` (no `detection_hints` key leaks into the catalog output —
> `load_catalog` still reads only its four fields). **The intent is documented in the test:** *"PINS
> load_catalog's tolerance of the additive [detection_hints] key. If a future strict-key hardening of
> load_catalog rejects [detection_hints], THIS TEST FAILS LOUD — do not silently break the catalog load;
> extend the hardening to admit detection_hints (or move the hints to a separate file) BEFORE landing it."*

**What `load_catalog` does (UNCHANGED, for clarity):** it reads `(service-id, entries, gcp_api, category)`,
validates them per §2.4.1, ignores the `[detection_hints]` block (as it ignores any non-required key today),
and returns the unchanged record shape `{entries, gcp_api, category}` (dataload.py:271-275). No edit.

**ALL `detection_hints` validation lives in `load_detection_hints`** (§2.3): fail-closed on the hints body,
fail-closed on an unknown sub-key under `[detection_hints]`. The catalog's TOLERANCE is pinned by the
regression test; the hints' INTEGRITY is enforced by the new loader. The two together address ARGUS's risk
(no silent break) without touching the core.

**Why this shape (vs ARGUS's proposed allowlist-on-`load_catalog`):** ARGUS's allowlist would have been a
clean contract but would have **textually edited the 2.1 core** (`load_catalog`), violating the §2
constraint (§0–§23 textually unchanged). The orchestrator chain (Polybius_the_Stoa → PLINY → FM) RATIFIED
the byte-unchanged fold-shape: honor §2 by NOT editing the core, and convert the silent-breakage risk into a
loud regression tripwire instead. The §2-frozen surfaces AND `load_catalog` are textually untouched (§2.0.1;
FM verifies before ADA).

### 2.4 The confirm-gate (§26 fail-closed) — `confirm.py`

The verified prototype `confirm.py` is promoted **logic-verbatim**: `D := confirm(P)` with the EXCLUSIVE
definition (`confirm(P)=P` on unedited CONFIRM; `=P'` on EDIT-then-CONFIRM; `=⊥` INERT on
REJECT/no-response/edits-pending/None/anything-unrecognized). The `INERT` sentinel is falsy-on-purpose so a
naive `if declare:` guard also fails closed. `is_declare(result)` is the downstream's mandatory gate before
feeding §18. This is the **fail-closed PROPERTY** the downstream depends on — it is Phase-1-complete and is
NOT a §4 decision. What 2.2 ADDS is the **contract layer** (§2.5).

### 2.5 The anti-rubber-stamp, evidence-rich confirm-contract — `evidence.py` + `confirm.py` (SWP-2)

This is **§4-decision #3**, designed as a **Phase-1-named contract** (not deferred wholesale). The fail-closed
PROPERTY (§2.4) governs WHAT counts as a DECLARE; this contract governs HOW the proposal is PRESENTED so a
human reviews **reasons, not a blind yes/no**. The contract is a **data shape + three invariants** the gate
must satisfy, all machine-checkable (the UX rendering of this shape is the only genuinely-Phase-2-deferred
piece; the contract the UX must honor is named here). See §4 (decision #3) for the full proposal.

### 2.6 Wiring the confirmed DECLARE to the UNCHANGED 2.1 core (§27, P3) — `declare.py`

```
examine(project_dir) ──▶ suggest(signals, detection_hints) ──▶ (proposed P, evidence, unknown)   [INERT]
                                                                      │
                                              §26 gate: D := confirm(P, human_action)   [the ONLY edge]
                                                                      │  (⊥ on no-confirm ⇒ STOP, nothing flows)
                                                                      ▼
                                  D  ═══ tagged P3 (agent-proposed + human-ratified, §27) ═══▶
                                  generate(D, catalog, categories, baseline)  →  resolve(manifest, baseline, library)
                                  (builder_deploy_core — IMPORTED UNMODIFIED — module-identity)  →  8 / 6 / 7
```

`declare.py` loads the same DATA tables via `dataload` (catalog/categories/baseline/library), tags the
confirmed set **P3** (a provenance label on the DECLARE record, §27 — the manifest stays a derived,
human-gated T2 artifact), and feeds `generate()→resolve()`. It **gates on `is_declare()` first**: an INERT
result short-circuits — `generate()` is never called (the §29.2 fail-closed property, made executable).

### 2.7 Threat → mitigation map (§6.12 A3 author duty)

Every SUGGEST element is a process/choreography/structure change with **NO new runtime attack path** — I
PROPOSE every element **`not threat-ratified`** (the §35.5 self-carve-out: process/role-hardening-class
changes with no runtime attack path). The full per-element table is §5 below (restating design-formal §31
for the BUILD). **There is no threat-anchored probe** because SUGGEST defeats no named threat (§6.13 +
§35.5: the layer verifies named-threat COVERAGE; SUGGEST's coverage set is empty — it adds no mitigation).
The §29.2 fail-closed no-confirm branch is the load-bearing **safety probe** (VERA exercises it) but it
verifies the gate's fail-closed PROPERTY, not a threat-defeat — consistent with §35.5. **ARGUS confirmed
every classification (§35.1 — cannot be self-exempted downstream); all five RATIFIED in the rev1 audit.**

**The rev2 WP-D2 fold is NOT a threat mitigation.** The `load_catalog` tolerance-PIN regression test is a
non-threat design-hardening (a data-integrity / regression tripwire), not a defeat of a named runtime attack
path — so it carries no `M<n>` and no threat-anchored probe (it is exercised by the §3 P5a regression/NEG
checks, not a threat-anchored probe). PLINY's A1 ratification-restatement (bw stoa--fdf 2026-06-26T23:46:47Z)
confirmed the A2 gate is VACUOUS for this arc (TRM_COUNT=0); rev2 does not change that.

---

## 3. Verification probes (the machine-checkable spec for VERA)

Each probe is a runnable check VERA re-executes. **P-suite floor: the prototype's 35 checks must still
PASS** (promoted into `test_suggest.py`); the probes below enumerate the DoD §5 gates as named checks.
Probe-ids are stable so the verdict can cite them.

| Probe | DoD | What it asserts (runnable) | Gate? |
|---|---|---|---|
| **P1-choreography** | #1 | For each of {prospector, scienceclaw, labstat_bls}: `confirm(suggest(examine(fixture)), CONFIRM)` == the §23 DECLARE set **byte-identical**; then unchanged `generate(D)→resolve()` len == **8 / 6 / 7** respectively. | GATE |
| **P2a-failclosed-reject** | #2 | prospector proposal, `human_action={reject}` → `confirm()` is `INERT`; `is_declare()` False; `generate()` is NOT called (instrument: a call-counter on the wired path stays 0). | GATE |
| **P2b-failclosed-noresponse** | #2 | same, `{no_response}` → INERT, nothing reaches `generate()`. | GATE |
| **P2c-failclosed-editspending** | #2 | same, `{edits_pending}` → INERT, nothing reaches `generate()`. | GATE |
| **P2d-failclosed-none** | #2 | same, `human_action=None` → INERT, nothing reaches `generate()`. | GATE |
| **P2e-overproposal** | #2 | over-proposal fixture proposes google-maps (stray maps URL); human EDIT removes it → DECLARE==[document-parsing]; `resolve()`==6; NO (gcp_api,google-maps) and NO (gcp_secret,MAPS_API_KEY) in resolved. | GATE |
| **P2f-underproposal** | #2 | under-proposal fixture misses bls-oews; human EDIT adds it → DECLARE==[bls-oews,document-parsing]; `resolve()`==7; (thirdparty_rest_key,BLS_OEWS_API_KEY) present. | GATE |
| **P3-module-identity** | #3 | `builder_deploy_core.discovery.generate.generate` and `…resolution.resolve.resolve` are the IMPORTED 2.1 callables: `generate.__module__`/`resolve.__module__` are the `builder_deploy_core.*` modules; the `suggest/` package defines **no** `generate`/`resolve` of its own (assert absence). | GATE |
| **P4a-evidence-present** | #4 | every proposed service in P1 carries non-empty `evidence[sid]`; each evidence row is `(surface, observed_token, matched_hint)`. | GATE |
| **P4b-contract-shape** | #4 | the §2.5 confirm-contract: the gate-presentation record for each candidate carries {service_id, entries-to-be-provisioned, evidence rows, confidence/source tag}; the anti-rubber-stamp invariants (§4 #3: bulk-accept-blocked, per-candidate-acknowledge, no-response⇒⊥) hold. | GATE |
| **P5a-hints-data + tolerance-pin** | #5 | **(POS)** `dataload.load_detection_hints()` loads the four services' hint sets from the catalog TOMLs; **(PIN, rev2 WP-D2)** the real 4-record catalog (each carrying its `[detection_hints]` block) loads cleanly through the **UNCHANGED** `load_catalog` (no `DataIntegrityError`; all 4 records load) AND `load_catalog`'s returned record shape is unchanged (`{entries, gcp_api, category}`, no `detection_hints` key leaks into the catalog output) — the regression PIN that fails LOUD if a future `load_catalog` hardening rejects `[detection_hints]` (§2.3.1); **(NEG, rev2 WP-D2)** an **unknown sub-key UNDER `[detection_hints]`** (e.g. `[detection_hints].mystery = [...]`) → `load_detection_hints` raises `DataIntegrityError` (all hints validation lives in the new loader; `load_catalog` is NOT edited). | GATE |
| **P5b-p3-provenance** | #5 | the confirmed DECLARE record is tagged **P3** (agent-proposed + human-ratified); the tag is present on the wired DECLARE and distinct from a P1/P2 hand-authored/derived manifest. | GATE |
| **P6-engine-runs-fixtures** | #6 | `examine(fixture_dir)` (Layer S, `neuro=False`) on each §29.1 project fixture extracts the EXPECTED signals (the §29.1 EXAMINE lines), feeding P1; the engine exists, runs, and produces evidence-bearing proposals. | GATE |
| **P7-full-suite** | #7 | the FULL existing the-stoa suite GREEN: `builder-deploy-core` pytest (the 2.1 40-pass floor + the new suggest tests + the new tolerance-pin/hints tests), `npm run gen-data`, `npm run build`, `npm test` (app). Regression — SUGGEST changed nothing downstream; **`load_catalog` and all 2.1 `dataload` functions are byte-unchanged** (the only `dataload` change is the appended `load_detection_hints`); `load_catalog` produces the identical 4-record catalog. | GATE |
| **P8-authorship** | #8 | every new/edited artifact carries `author: Denson Smith`; zero foreign author-like field (grep audit over the new files + edited TOMLs + edited `dataload.py`). | GATE |
| **P9-accuracy-baseline** | #9 | run the engine (Layer S + optional Layer N) against scienceclaw's **actual repo**; report recall/precision + over-/under-proposal rates. **REPORTED, NOT a pass/fail gate** — recorded as a measured baseline (a weak/absent result does NOT fail the arc). | REPORT |

**Probe-spec count: 16 (15 gated checks P1–P8 + 1 reported P9).** The probe COUNT is unchanged from rev1
(P5a bundles the rev2 tolerance-PIN + hints-NEG sub-assertions into the existing P5 data-integrity probe
rather than adding a new probe-id — the pin/NEG are part of the SAME §5 data-load gate, so they live in
P5a). P7 is the full-suite regression (VERA + the close-gate run the project's FULL existing suite IN
ADDITION to the bespoke probes — bespoke proves the new thing works; full-suite catches what the change
breaks elsewhere).

**Probe-grounding notes (§6.9):**
- **P5a tolerance-PIN / hints-NEG (rev2):** grounded against the ACTUAL `load_catalog` structure (BYTE-
  UNCHANGED) — the PIN is a **live round-trip** that loads the real 4-record catalog (with its
  `[detection_hints]` blocks) through `load_catalog(data_root=tmp)` and asserts a clean load + the unchanged
  `{entries, gcp_api, category}` record shape (no false rejection AND no `detection_hints` leak into the
  catalog output). The hints-NEG feeds a synthetic catalog TOML carrying an unknown sub-key under
  `[detection_hints]` through `load_detection_hints(data_root=tmp)` and asserts `DataIntegrityError`,
  mirroring the §2.4.1 fail-closed precedent `load_baseline`/`load_kinds` enforce by set-equality. Both use
  a FIXED literal synthetic-TOML path under a pytest `tmp_path`, no `$VAR` expansion in any destructive op
  (§8.6). The PIN's documented intent (fail-LOUD on a future `load_catalog` strict-key hardening) is the
  rev2 WP-D2 fold made executable WITHOUT editing the core.
- **P3-module-identity** is grounded against the 2.1 core's actual module names
  (`builder_deploy_core.discovery.generate`, `builder_deploy_core.resolution.resolve` — verified at design
  time, not assumed). **P2*-failclosed** instruments the wired path with a **call-counter** (not a grep) so
  "nothing reaches generate()" is asserted by execution, not by reading code.

---

## 4. The THREE §4 decisions — **PROPOSE (routes UP for ratification)**

> **Ratification status note (rev2):** PLINY routed these three §4 decisions UP to POLYBIUS_the-stoa for
> ratification (bw stoa--fdf 2026-06-26T23:47:04Z), GATING the ADA dispatch on (a) that ratification + (b)
> this rev2 in hand. ARGUS confirmed Decision #1 SOUND in the rev1 audit. The PROPOSE text below is held
> verbatim from rev1 (unchanged) as the artifact-of-record for what was routed up.

### §4-Decision #1 — Engine implementation approach: **PROPOSE application code (NOT a Stoa Workflow)**

**PROPOSE — routes up for ratification.** Implement the §28 engine as **plain Python application code**
inside `builder_deploy_core.suggest.examine`, NOT as a Stoa Workflow.

**Reasoning:**
- The gated path (Layer S) is a **deterministic, hermetic, pure-function** examiner — exactly the shape the
  2.1 core already is (pure, single-fs-boundary, no network). It fits the existing package's idiom and its
  test harness with zero new orchestration substrate.
- The §28 flow's only genuinely-agentic step (Layer N, dynamic-endpoint LLM resolution) is **REPORTED-only,
  never gated**, and is a single optional enrichment call — it does not need a multi-step workflow engine to
  realize, and bringing one in would couple the gated suite to a workflow runtime it must stay independent of.
- The directive §6 explicitly reserves the architects (HAMILTON) for the 2.3 provisioning choreography and
  composes 2.2 as STANDARD (FM+PLINY, no HAMILTON at launch). Application code keeps that composition intact.

**> NO LOUD FLAG: I am NOT proposing engine-as-Workflow.** I considered it and rejected it for the reasons
above. If ARGUS or Polybius_the_Stoa judges the Layer-N enrichment substantial enough to warrant a Workflow
realization (and thus MAJOR_HAMILTON + a team re-compose), that is a ratification call that **routes UP to
Polybius_the_Stoa, NOT baked into this design** — but my proposal is that it does **not** warrant it for 2.2,
because the gated deliverable is application code and Layer N is a reported, single-call enrichment.

### §4-Decision #2 — Read-surface scoping (SWP-3): **PROPOSE no new provisioning trust boundary; ONE named egress residual**

**PROPOSE — routes up for ratification.** Scope the agent's read surface and assert SUGGEST adds **no new
provisioning trust boundary beyond the existing R-2 (manifest-integrity) / candidate-R-3 (catalog-integrity)**,
with **one explicitly named non-provisioning egress residual (R-egress, §0.2 WP-D4)**.

**The read surface (exactly what the agent ingests):**
- **READS:** (a) the **catalog `detection_hints`** (T1 advisory DATA — read, never written); (b) the
  **examined project's static material** under one project directory — source files (AST), config/env
  keys, README/OpenAPI (Layer N), data-flow signals. **Layer S reads only files under the one project
  directory** (single-fs-boundary, mirroring 2.1 `dataload`); Layer N additionally may call an LLM with
  excerpts of that same material.
- **WRITES:** nothing provisionable. The agent's only output is the **INERT proposal** (proposed set +
  evidence). It does **not** write the catalog, does **not** write a manifest, does **not** provision.
- **The proposal-channel boundary:** the proposal flows to the §26 gate and **nowhere else**; the ONLY edge
  from PROPOSE → DECLARE is a human-issued CONFIRM (§26 C-3 exclusivity). An unconfirmed proposal is INERT.

**Trust-boundary assertion:** a biased/compromised read or proposal channel can only **mis-PROPOSE**, which
the §26 human gate catches (§25.1: a wrong signal can mis-propose, never mis-provision). Blast radius =
**wasted human-review attention**, NOT over-grant. R-2/R-3 are **unchanged** (the agent reads, does not edit,
the catalog). **The Layer-N excerpt-egress is NAMED as residual R-egress (§0.2 WP-D4): REPORTED-only,
gate-inert, no provisioning authority — on the record, NOT a new provisioning trust boundary.** ARGUS
confirmed (rev1 audit r3): name the egress residual; no trust-boundary change.

### §4-Decision #3 — The anti-rubber-stamp confirm-contract shape (SWP-2): **PROPOSE a Phase-1-named contract**

**PROPOSE — routes up for ratification.** Name the confirm-contract as a **Phase-1 contract** (a data shape
+ three invariants the gate must honor), with only the visual UX rendering deferred to a later Phase-2 UI.

**The contract (data shape):** for each proposed candidate, the gate presents a **`CandidatePresentation`**
record:
```
CandidatePresentation:
  service_id        # the proposed catalog service
  entries_preview   # the HARD recipe this service WOULD provision if confirmed (from §17.1 entries) —
                    #   so the human sees the CONSEQUENCE (e.g. "google-maps ⇒ provisions MAPS_API_KEY")
  evidence          # the per-candidate WHY: [(surface, observed_token, matched_hint), …] — reasons, not yes/no
  source            # provenance per signal: symbolic (Layer S) | neuro (Layer N) — so LLM-inferred candidates
                    #   are visibly flagged as lower-confidence for human scrutiny
```

**The three anti-rubber-stamp invariants (machine-checkable, P4b):**
1. **No bulk blind-accept.** There is **no single "accept all" that bypasses evidence** — CONFIRM requires
   the proposal set to have been *presented with* its `CandidatePresentation` records. (Mechanically: the
   gate's confirm entrypoint requires the presentation to have been materialized; a confirm against an
   un-presented proposal is rejected.)
2. **Per-candidate acknowledgement is the unit.** EDIT operates per-candidate (add/remove a named service);
   the human's ratified set is authoritative (§26.1 P'). Removing a hallucinated candidate or adding a
   missed one is a first-class, low-friction operation (so EDIT is not so painful that under-proposals slip
   through unedited — the SWP-2 risk).
3. **No-response is ⊥, structurally.** The operational shape of "no-response" is **fail-closed by default**:
   absent an explicit CONFIRM, the result is INERT (the existing `confirm()` default-⊥ branch). Whether a
   deployment wires "no-response" as a CI-block, a timeout, or a one-time prompt is a deployment policy, but
   in **every** case the *result* of no-response is ⊥ (this is the contract; the policy is the deployment's).

**What stays Phase-2:** the visual rendering of `CandidatePresentation` (the actual UI/CLI surface). **What
is Phase-1-named here:** the data shape, the three invariants, and the fail-closed-no-response result —
because the downstream safety depends on them, they are a contract, not a UX afterthought. ARGUS confirmed
(rev1 audit) the contract (shape + 3 invariants) is the right Phase-1 boundary.

---

## 5. §31 threat classification for the BUILD (DAEDALUS PROPOSES; ARGUS CONFIRMED — all five RATIFIED)

Restating design-formal §31 for the 2.2 build. Every new build element carries a §35.1 classification.
**ARGUS RATIFIED all five as PROPOSED not-threat-ratified in the rev1 audit (§35.5 carve-out confirmed each;
ARGUS is the §35.1 upstream confirmer — none can be self-exempted downstream).**

| Element (build artifact) | PROPOSED classification (ARGUS-RATIFIED) |
|---|---|
| `detection_hints` catalog DATA (§25; the additive TOML blocks + `load_detection_hints` + the rev2 `load_catalog` tolerance-pin regression test) | **not threat-ratified** (additive ADVISORY structure; §25.1 a wrong/missing hint can only mis-PROPOSE, never mis-provision — no runtime attack path; provisioning rides the unchanged `entries` whose completeness is already M3, §12.A. The rev2 tolerance-pin is a regression tripwire, not a threat-defeat). Process/structure change, §35.5 carve-out. |
| The examine→match→propose engine (§24/§28; `examine.py`+`suggest.py`) | **not threat-ratified** (a READ-ONLY recommendation-producer; output INERT until the §26 gate — no provisioning authority, no runtime attack path). |
| The human-CONFIRM fail-closed gate (§26; `confirm.py` + the §2.5 contract) | **not threat-ratified — a FAIL-CLOSED SAFETY GATE, not a threat-defeating mitigation** (parallel to V1–V5 / §4 S2c). It makes an imperfect *proposal* safe; it defeats no NAMED threat with a runtime attack path; weakens no existing M1–M4/M6 or V1–V5. |
| SUGGEST tier/ownership + P3 provenance (§27; `declare.py`) | **not threat-ratified** (provenance/process change; manifest stays a derived, human-gated T2 artifact — R-2 lineage UNCHANGED, reached one step further upstream; the human gate is the same review locus). |
| The agent reading T3 project behavior (§27/SWP-3; `examine.py` read surface, incl. **Layer N excerpt egress = named residual R-egress, §0.2 WP-D4**) | **not threat-ratified — R-2/R-3-ADJACENT, NOT a distinct threat.** A read-only proposing actor whose output is gated INERT touches no provisioning authority; a biased read can only mis-PROPOSE (caught by §26); blast radius = wasted human-review attention, NOT over-grant. The Layer-N excerpt-egress is **NAMED as residual R-egress** (REPORTED-only, gate-inert, no provisioning authority) — recorded, not a new provisioning boundary. **ARGUS confirmed (rev1 r3).** |

**Why no threat-anchored probe (§6.13 + §35.5 self-carve-out):** every element above is RATIFIED
**not threat-ratified** (process/choreography/structure change, no new runtime attack path) — SUGGEST
DEFEATS no new threat; it produces the §18 DECLARE whose EXISTING mitigations (M1–M4/M6, §12.A) already
carry their threat-anchored probes. The §29.2 fail-closed no-confirm branch (P2a–d) is the load-bearing
**safety probe**, but it verifies the gate's fail-closed PROPERTY, not a threat-defeat (§35.5: the layer
verifies named-threat COVERAGE; threat-ENUMERATION completeness stays ARGUS's residual). The rev2
`load_catalog` tolerance-pin is exercised by P5a's regression/NEG data-integrity checks, not a threat-
anchored probe (it is a non-threat data-integrity hardening). TRM_COUNT=0 for this arc (PLINY A1, bw
23:46:47Z); the A2 gate is vacuous; rev2 does not change that.

---

## 6. Self-assessed weak points (for ARGUS to pressure-test)

Seeded from design-formal §30 (SWP-1..4), specialized to the BUILD. **WP-D1, WP-D5 held verbatim from rev1
(ARGUS ratified). WP-D2 is now PINNED-by-regression-test (the RATIFIED byte-unchanged rev2 fold). WP-D3,
WP-D4 are recorded dispositions (ratified up).**

- **WP-D1 (carries SWP-1) — the gated suite proves CHOREOGRAPHY on fixtures, NOT real-world accuracy.** The
  gated probes (P1/P6) run Layer S on **hand-built §29.1 project fixtures** whose signals are constructed to
  match the seed hints. *Risk:* this proves the front-door wiring, not the engine's recall/precision on a
  messy real repo. *Why this shape anyway:* accuracy = USEFULNESS not safety (§28) — DoD#9 REPORTS the real
  baseline (scienceclaw repo); a weak engine leaves the system SAFE because the §26 gate + V1–V5 make any
  proposal safe regardless of inference quality. **ARGUS confirmed (rev1): a weak/absent engine leaves the
  system SAFE; NO suggest-completeness claim.**

- **WP-D2 (PINNED-by-regression-test in rev2 — `load_catalog` is BYTE-UNCHANGED) — `detection_hints` rides
  on `load_catalog`'s existing tolerance, and that tolerance is pinned by a loud regression test.** rev1
  relied on `load_catalog` silently ignoring an extra TOML key — the one un-contracted additive key in an
  otherwise fail-closed §2.4.1 package (ARGUS r1, load-bearing). ARGUS proposed a strict-key allowlist ON
  `load_catalog`; that was **OVERRULED by the orchestrator chain** (Polybius_the_Stoa → PLINY → FM, bw
  23:50/23:51Z) because editing `load_catalog` would **textually modify the §2-frozen core** (§0–§23
  unchanged). **rev2 RATIFIED resolution:** `load_catalog` is left **byte-unchanged**; the tolerance is
  **pinned by a regression test** (§2.3.1, P5a-PIN) whose documented intent is *"a future strict-key
  hardening of load_catalog that rejects [detection_hints] FAILS THIS TEST LOUD"* — turning the rev1 silent-
  break path into a loud, named tripwire. ALL `detection_hints` validation lives in the new
  `load_detection_hints` loader. *Residual risk (named, minor):* the pin is a TEST, not an enforced loader
  invariant — it protects against a future hardening only if the test is run (it is in the gated P7 suite,
  so it is). The catalog-record key set is still not strict-key-enforced AT LOAD (that would be the core
  edit §2 forbids); the test is the §2-compliant substitute. *Why this shape anyway:* §2 (core byte-
  unchanged) is a hard ratified constraint; the regression test addresses ARGUS's real risk (no silent
  break) without violating it. **P5a-PIN + P7 cover this; the FM verifies `load_catalog`/`dataload`'s
  existing functions are byte-unchanged before ADA.** **ARGUS: confirm the regression-test pin is the right
  §2-compliant resolution of r1 (the silent-break path is now a loud test failure), and that `load_catalog`
  is byte-unchanged.**

- **WP-D3 (recorded disposition — ratified NOT under-delivery) — there are no uncataloged services to fill
  at 2.2.** The 2.1 catalog ships exactly the four services the seeds cover (ARGUS verified at source).
  *Risk:* reading directive piece #2 ("populate hints beyond the four seed hints") literally would imply
  authoring hints for services that don't exist yet — an impossible/over-reaching deliverable. *Faithful
  read (ratified up):* (a) migrate the four seeds from prototype Python-dict into real catalog DATA + (b)
  establish the R-3 authoring discipline + the `load_detection_hints` validation contract as the durable
  fill mechanism. **Recorded so NOMOS does not read "only four got hints" as under-delivery of piece #2 —
  there is nothing else to fill.** ARGUS confirmed (rev1 r2) this is the faithful read, not under-delivery.

- **WP-D4 (recorded disposition — one NAMED residual R-egress) — the REPORTED neuro path sends project
  material to an external LLM.** *Surface:* DoD#9's scienceclaw-real-repo baseline (Layer N on) sends repo
  excerpts to a model — a data-egress surface the gated path never touches and that no gated probe (P1–P8)
  exercises. *Disposition:* **NAMED as residual R-egress** (*Layer-N proposal-channel egress: repo
  excerpts → external LLM; REPORTED-only, gate-inert, no provisioning authority*). *Why not a new trust
  boundary:* Layer N is REPORTED-only and gate-inert (its output cannot mis-provision; the §26 gate stands);
  the egress is a USEFULNESS-baseline activity, not a provisioning one — the §31 verdict is unchanged. **On
  the record, not silently absorbed.** ARGUS confirmed (rev1 r3): name this one residual; no trust-boundary
  change.

- **WP-D5 (the over/under-proposal fixtures are constructed to PASS the safety probe).** The over-/under-
  proposal fixtures (P2e/P2f) are built so the human EDIT yields the correct 6/7. *Risk:* this proves the
  gate CATCHES a constructed mis-proposal, not that the engine's real mis-proposal rate is low. *Why this
  shape anyway:* that is exactly the point — the safety probe proves the GATE is load-bearing (the §28
  safety claim), and the engine's real mis-proposal rate is the REPORTED DoD#9 baseline, deliberately not
  gated. **ARGUS confirmed (rev1): the safety probe correctly tests the gate (not the engine), per §28.**

---

## 7. DoD §5 mapping (gated vs reported)

| DoD # | Element | Probe(s) | Gated? |
|---|---|---|---|
| 1 | CHOREOGRAPHY → 8/6/7 byte-identical DECLARE | P1 | GATE |
| 2 | FAIL-CLOSED SAFETY (4 no-confirm actions + over/under) | P2a–P2f | GATE |
| 3 | §2-CONSTRAINT module-identity | P3 | GATE |
| 4 | CONFIRM-GATE evidence-rich contract present+tested | P4a, P4b | GATE |
| 5 | `detection_hints` DATA + load_catalog tolerance-pin + hints fail-closed + P3 provenance | P5a, P5b | GATE |
| 6 | ENGINE RUNS on fixtures (existence+fixtures, NOT accuracy) | P6 | GATE |
| 7 | REGRESSION — full existing suite green | P7 | GATE |
| 8 | Authorship — author: Denson Smith, zero foreign field | P8 | GATE |
| 9 | accuracy baseline on scienceclaw real repo | P9 | **REPORTED (not gated)** |
| 10 | the §4 decisions surfaced for ratification | §4 (this doc) | surfaced, not baked |

**Load-bearing:** DoD#9 (accuracy) is **REPORTED, never a gate** — the §28 safety framing made executable.
Nothing in this design gates on an accuracy number.

---

## 8. Out of scope (deliberately not designed here)

- **Provisioning choreography S0–S6 + real deploy** — increment 2.3. SUGGEST stops at the confirmed DECLARE
  fed to `generate()→resolve()`; nothing provisions.
- **scienceclaw end-to-end stand-up** — increment 2.4. DoD#9 runs the engine against scienceclaw's repo
  READ-ONLY (a USEFULNESS baseline), which is distinct from standing the project up.
- **ALL real infrastructure** — no gcloud, no Railway, no credentials. Layer N's LLM call (REPORTED path) is
  the only external call and is not infra provisioning.
- **The confirm-gate VISUAL UI** — only the contract (data shape + invariants, §4 #3) is Phase-1-named; the
  rendered surface is a later Phase-2 UI.
- **A strict-key fail-closed hardening of `load_catalog` itself** — DEFERRED, deliberately: editing
  `load_catalog` would textually modify the §2-frozen core (§0–§23 unchanged), which the directive FORBIDS.
  rev2 instead PINS the existing tolerance with a regression test (§2.3.1). A future arc that is permitted to
  edit the 2.1 core can promote the pin into an enforced allowlist; until then the test is the §2-compliant
  guard. (The other loaders already enforce set-equality fail-closed per dataload.py:84-174; `load_catalog`
  is the lone tolerance, now pinned not enforced.)
- **Customer-repo privacy / data-handling of the Layer-N egress (Phase-3/4 escalation, record-only)** —
  WP-D4's named R-egress residual (Layer-N repo-excerpts → external LLM) is **bounded and fine for 2.2**
  (the examined repos are OUR OWN: scienceclaw + the hand-built fixtures, no third-party proprietary code).
  **But when the cookie-cutter later examines a real CUSTOMER repo (Phase-3/4), the same egress becomes a
  privacy / data-handling consideration** — customer proprietary code leaving to an external LLM. This is
  **on the record for NOMOS + future phases** so the escalation is visible before any customer-repo examine
  ships: Phase-3/4 MUST revisit the Layer-N egress as a customer-data boundary (consent / redaction /
  on-prem-model / opt-out), NOT inherit 2.2's "bounded + fine" verdict. NOT a 2.2 blocker (PLINY/POLYBIUS,
  bw 23:51Z: record-only).
- **Any change to `generate`/`resolve`/`validate`/the §0–§23 mechanism** — IMPORTED UNMODIFIED; the §8 sets
  are a regression target, hit not re-derived. **The rev2 fold does NOT edit `load_catalog` or any existing
  2.1 `dataload` function** (the only `dataload` change is the appended `load_detection_hints`; the tolerance
  is pinned by a test, not a core edit — §2.0.1, §2.3.1).

---

## 9. Provenance

Designed by **CAPTAIN_DAEDALUS_the_stoa** (gauntlet stage 1/6, arc stoa--fdf) from the authoritative
Phase-1 SUGGEST design (`agents/design/stoa--jw5/design-formal.md` §24–§31), the 35/35-PASS prototype
(`agents/design/stoa--jw5/suggest-check/`), and the shipped 2.1 core
(`agents/builder-deploy-core/builder_deploy_core`). rev2 folds ARGUS's one load-bearing risk (r1/WP-D2) in
the orchestrator-RATIFIED byte-unchanged shape — `load_catalog` is NOT edited (§2 forbids editing the core);
its tolerance is pinned by a regression test that fails LOUD on a future strict-key hardening — and records
two dispositions (r2/WP-D3 ratified-not-under-delivery, r3/WP-D4 named Layer-N egress residual + its
Phase-3/4 customer-privacy escalation); no other rev1 content is re-litigated (ARGUS ratified it cold).
The §28 neuro-symbolic capability premise was **web-RE-verified at this seat** (gsearch / current docs
2026-06-26: DI-BENCH ACL2025 dependency-inference benchmark, AST import-extraction-not-grep discipline,
evidence-discovery multi-agent loop, dynamic-endpoint LLM resolution — the §6.4 live-constraint check, NOT
memory). This is the build-design that promotes the verified choreography into runnable packaged code and
names the three new Phase-2 pieces + the three §4 decisions. **Author: Denson Smith.**
