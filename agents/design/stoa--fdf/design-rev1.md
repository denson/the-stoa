---
author: Denson Smith
ticket: stoa--fdf (u--9s2 Phase-2 increment 2.2)
designed-by: CAPTAIN_DAEDALUS_the_stoa (ARCHITECT) — gauntlet stage 1/6
design-ground-truth: agents/design/stoa--jw5/design-formal.md §24–§31 (the SUGGEST front-door, authoritative WHAT/SHAPE)
upstream-2.1-core: agents/builder-deploy-core/ (builder_deploy_core — generate/resolve IMPORTED UNMODIFIED)
prototype-promoted-from: agents/design/stoa--jw5/suggest-check/ (35/35 PASS)
status: DESIGN-rev1 — for ARGUS critique → ADA build
as_of: 2026-06-26
---

# stoa--fdf — build design: the SUGGEST front-door (u--9s2 Phase-2 increment 2.2)

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

- **(A-import-1) The catalog loader tolerates an additive key.** I verified `dataload.load_catalog`
  (2.1 core) reads ONLY `(service-id, entries, gcp_api, category)` per record and does **not** reject
  unknown extra keys. Therefore `detection_hints` ships as an **additive optional TOML block on the
  existing catalog records** and a **separate `load_detection_hints` loader**, with `generate()` reading
  the unchanged catalog (it never sees hints). This is the design's load-bearing wiring choice; if a later
  hardening adds a strict-key check to `load_catalog`, that check must be extended to allow
  `detection_hints` — flagged as weak point WP-D2 (§9).
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
directive left implicit is (A-import-1)/(A-import-3) — the wiring mechanism and the deterministic-examiner
split — both named here and carried as weak points for ARGUS.

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
    dataload.py                    # (+ ADDITIVE) gains load_detection_hints(); load_catalog UNCHANGED
    resolution/ …                  # (UNCHANGED — 2.1 core)
    discovery/ …                   # (UNCHANGED — 2.1 core; generate.py reads entries only)
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
the gated path is hermetic and deterministic; the probabilistic path is reported, never a gate.

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

[detection_hints]                    # NEW — ADVISORY recognition signals only (§25)
sdk_imports  = ["@googlemaps/js-api-loader", "google.maps", "@react-google-maps/api"]
url_patterns = ["maps.googleapis.com", "maps.gstatic.com"]
config_keys  = ["GOOGLE_MAPS_API_KEY", "MAPS_API_KEY", "NEXT_PUBLIC_MAPS_KEY"]
data_signals = ["client-side-map-render", "map-tile-fetch"]
```

**Loader (`dataload.load_detection_hints`)** — ADDITIVE to `dataload.py`, sibling of `load_catalog`,
reading the same `data/catalog/*.toml`. It validates fail-closed (the 2.1 §2.4.1 discipline): each
`[detection_hints]` block, if present, is a table whose four keys (any subset) are arrays of non-empty
strings; an unknown key under `[detection_hints]` raises `DataIntegrityError`; a service-id with no block
is allowed (the field is optional). It returns `{ service_id: {sdk_imports, url_patterns, config_keys,
data_signals} }` — the structure `suggest()` consumes. **`load_catalog` is UNCHANGED** and never reads
`detection_hints`; the two loaders read the same files for different keys (hint-agnostic generation,
§25.2 invariant 1).

> **The Phase-2 "fill beyond the four seeds":** the directive's piece #2 says populate hints "beyond the
> four §25.3 seed hints the worked examples exercise." The 2.1 catalog ships exactly the four cataloged
> services (google-maps, spatial-db, document-parsing, bls-oews) — there are **no other cataloged services
> to fill** at 2.2. The honest Phase-2 deliverable is therefore: (a) migrate the four seed-hint sets from
> the prototype Python dict into real catalog DATA (TOML) under R-3, and (b) establish the
> **R-3 catalog-authoring discipline + the `load_detection_hints` validation contract** as the durable
> mechanism by which any future cataloged service's hints are authored. I flag this as weak point WP-D3
> (§9) so ARGUS confirms "fill the four into DATA + establish the authoring contract" is the faithful read
> of piece #2, not an under-delivery.

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
changes with no runtime attack path). The full per-element table is §6 below (restating design-formal §31
for the BUILD). **There is no threat-anchored probe** because SUGGEST defeats no named threat (§6.13 +
§35.5: the layer verifies named-threat COVERAGE; SUGGEST's coverage set is empty — it adds no mitigation).
The §29.2 fail-closed no-confirm branch is the load-bearing **safety probe** (VERA exercises it) but it
verifies the gate's fail-closed PROPERTY, not a threat-defeat — consistent with §35.5. **ARGUS confirms or
revises every classification (§35.1 — cannot be self-exempted downstream), especially the SWP-3 read-actor
classification.**

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
| **P5a-hints-data** | #5 | `dataload.load_detection_hints()` loads the four services' hint sets from the catalog TOMLs; fail-closed on a malformed block (a NEG check: an unknown key under `[detection_hints]` raises `DataIntegrityError`). | GATE |
| **P5b-p3-provenance** | #5 | the confirmed DECLARE record is tagged **P3** (agent-proposed + human-ratified); the tag is present on the wired DECLARE and distinct from a P1/P2 hand-authored/derived manifest. | GATE |
| **P6-engine-runs-fixtures** | #6 | `examine(fixture_dir)` (Layer S, `neuro=False`) on each §29.1 project fixture extracts the EXPECTED signals (the §29.1 EXAMINE lines), feeding P1; the engine exists, runs, and produces evidence-bearing proposals. | GATE |
| **P7-full-suite** | #7 | the FULL existing the-stoa suite GREEN: `builder-deploy-core` pytest (the 2.1 40-pass floor + the new suggest tests), `npm run gen-data`, `npm run build`, `npm test` (app). Regression — SUGGEST changed nothing downstream. | GATE |
| **P8-authorship** | #8 | every new/edited artifact carries `author: Denson Smith`; zero foreign author-like field (grep audit over the new files + edited TOMLs). | GATE |
| **P9-accuracy-baseline** | #9 | run the engine (Layer S + optional Layer N) against scienceclaw's **actual repo**; report recall/precision + over-/under-proposal rates. **REPORTED, NOT a pass/fail gate** — recorded as a measured baseline (a weak/absent result does NOT fail the arc). | REPORT |

**Probe-spec count: 16 (15 gated checks P1–P8 + 1 reported P9).** P7 is the full-suite regression
(VERA + the close-gate run the project's FULL existing suite IN ADDITION to the bespoke probes — bespoke
proves the new thing works; full-suite catches what the change breaks elsewhere).

**Probe-grounding notes (§6.9):** P3-module-identity is grounded against the 2.1 core's actual module
names (`builder_deploy_core.discovery.generate`, `builder_deploy_core.resolution.resolve` — verified at
design time, not assumed). P2*-failclosed instruments the wired path with a **call-counter** (not a grep)
so "nothing reaches generate()" is asserted by execution, not by reading code. P5a's NEG check
(unknown-key → `DataIntegrityError`) is a live round-trip against the new loader, matching the 2.1
§2.4.1 fail-closed precedent.

---

## 4. The THREE §4 decisions — **PROPOSE (routes UP for ratification)**

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

### §4-Decision #2 — Read-surface scoping (SWP-3): **PROPOSE no new trust boundary**

**PROPOSE — routes up for ratification.** Scope the agent's read surface and assert SUGGEST adds **no new
trust boundary beyond the existing R-2 (manifest-integrity) / candidate-R-3 (catalog-integrity)**.

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
the catalog). **I PROPOSE: no new named residual.** ARGUS: CONFIRM SUGGEST adds no new trust boundary beyond
R-2 / candidate-R-3 — OR surface a distinct **"proposal-channel integrity"** residual if the read-and-propose
actor warrants its own naming (e.g. if Layer N sending project excerpts to an external LLM is judged a
distinct data-egress surface worth naming — I judge it REPORTED-only and gate-inert, so not a new *provisioning*
boundary, but I flag it explicitly for ARGUS's call).

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
because the downstream safety depends on them, they are a contract, not a UX afterthought. **ARGUS: confirm
the contract (shape + 3 invariants) is the right Phase-1 boundary — sufficient to defeat rubber-stamping
without over-specifying a UI that is legitimately Phase-2.**

---

## 5. §31 threat classification for the BUILD (DAEDALUS PROPOSES; ARGUS CONFIRMS)

Restating design-formal §31 for the 2.2 build. Every new build element carries a §35.1 classification.

| Element (build artifact) | PROPOSED classification |
|---|---|
| `detection_hints` catalog DATA (§25; the additive TOML blocks + `load_detection_hints`) | **not threat-ratified** (additive ADVISORY structure; §25.1 a wrong/missing hint can only mis-PROPOSE, never mis-provision — no runtime attack path; provisioning rides the unchanged `entries` whose completeness is already M3, §12.A). Process/structure change, §35.5 carve-out. |
| The examine→match→propose engine (§24/§28; `examine.py`+`suggest.py`) | **not threat-ratified** (a READ-ONLY recommendation-producer; output INERT until the §26 gate — no provisioning authority, no runtime attack path). |
| The human-CONFIRM fail-closed gate (§26; `confirm.py` + the §2.5 contract) | **not threat-ratified — a FAIL-CLOSED SAFETY GATE, not a threat-defeating mitigation** (parallel to V1–V5 / §4 S2c). It makes an imperfect *proposal* safe; it defeats no NAMED threat with a runtime attack path; weakens no existing M1–M4/M6 or V1–V5. |
| SUGGEST tier/ownership + P3 provenance (§27; `declare.py`) | **not threat-ratified** (provenance/process change; manifest stays a derived, human-gated T2 artifact — R-2 lineage UNCHANGED, reached one step further upstream; the human gate is the same review locus). |
| The agent reading T3 project behavior (§27/SWP-3; `examine.py` read surface, incl. Layer N excerpt egress) | **not threat-ratified — R-2/R-3-ADJACENT, NOT a distinct threat.** A read-only proposing actor whose output is gated INERT touches no provisioning authority; a biased read can only mis-PROPOSE (caught by §26); blast radius = wasted human-review attention, NOT over-grant. **ARGUS: CONFIRM no new named residual, OR surface a distinct "proposal-channel integrity" residual** if the Layer-N excerpt-egress warrants its own naming. |

**Why no threat-anchored probe (§6.13 + §35.5 self-carve-out):** every element above is PROPOSED
**not threat-ratified** (process/choreography/structure change, no new runtime attack path) — SUGGEST
DEFEATS no new threat; it produces the §18 DECLARE whose EXISTING mitigations (M1–M4/M6, §12.A) already
carry their threat-anchored probes. The §29.2 fail-closed no-confirm branch (P2a–d) is the load-bearing
**safety probe**, but it verifies the gate's fail-closed PROPERTY, not a threat-defeat (§35.5: the layer
verifies named-threat COVERAGE; threat-ENUMERATION completeness stays ARGUS's residual). **ARGUS confirms or
revises ALL classifications — they cannot be self-exempted downstream.**

---

## 6. Self-assessed weak points (for ARGUS to pressure-test)

Seeded from design-formal §30 (SWP-1..4), specialized to the BUILD:

- **WP-D1 (carries SWP-1) — the gated suite proves CHOREOGRAPHY on fixtures, NOT real-world accuracy.** The
  gated probes (P1/P6) run Layer S on **hand-built §29.1 project fixtures** whose signals are constructed to
  match the seed hints. *Risk:* this proves the front-door wiring, not the engine's recall/precision on a
  messy real repo. *Why this shape anyway:* accuracy = USEFULNESS not safety (§28) — DoD#9 REPORTS the real
  baseline (scienceclaw repo); a weak engine leaves the system SAFE because the §26 gate + V1–V5 make any
  proposal safe regardless of inference quality. **ARGUS: confirm a weak/absent engine leaves the system
  SAFE and the design makes NO suggest-completeness claim.**

- **WP-D2 (the additive-key wiring assumption) — `detection_hints` rides on `load_catalog` tolerating an
  extra TOML key.** I verified the 2.1 `load_catalog` reads only its four required keys and ignores extras.
  *Risk:* a future hardening that adds a strict-key/no-extra-keys check to `load_catalog` would reject the
  `[detection_hints]` block and break the catalog load. *Why this shape anyway:* additive-optional on the
  existing record is the §25 design (one record, advisory field appended); the alternative (a separate
  hints file per service) duplicates the service→record mapping and risks drift. **Mitigation in this
  design:** `load_detection_hints` is a SEPARATE loader, and `test_dataload` asserts `load_catalog` still
  produces the identical 4-record catalog post-edit (P7 covers this). **ARGUS: is the additive-key reliance
  acceptable, or should the design add a strict-key allowlist to `load_catalog` that explicitly includes
  `detection_hints` (making the tolerance a contract, not an accident)?**

- **WP-D3 (the Phase-2 "fill" scope) — there are no uncataloged services to fill at 2.2.** The 2.1 catalog
  ships exactly the four services the seeds cover. *Risk:* reading directive piece #2 ("populate hints
  beyond the four seed hints") literally would imply authoring hints for services that don't exist yet —
  an impossible/over-reaching deliverable. *Why this shape anyway:* the faithful read is (a) migrate the
  four seeds from prototype Python-dict into real catalog DATA + (b) establish the R-3 authoring discipline
  + the `load_detection_hints` validation contract as the durable fill mechanism. **ARGUS: confirm this is
  the faithful read of piece #2, not an under-delivery.**

- **WP-D4 (Layer N excerpt egress) — the REPORTED neuro path sends project material to an external LLM.**
  *Risk:* DoD#9's scienceclaw-real-repo baseline (Layer N on) sends repo excerpts to a model — a data-egress
  surface the gated path never touches. *Why this shape anyway:* Layer N is REPORTED-only and gate-inert
  (its output cannot mis-provision; the §26 gate stands); the egress is a USEFULNESS-baseline activity, not
  a provisioning one. **ARGUS: is this an SWP-3 "proposal-channel integrity" residual worth naming, or is
  "read-only, gated-inert, reported-only" sufficient (my proposal)?**

- **WP-D5 (the over/under-proposal fixtures are constructed to PASS the safety probe).** The over-/under-
  proposal fixtures (P2e/P2f) are built so the human EDIT yields the correct 6/7. *Risk:* this proves the
  gate CATCHES a constructed mis-proposal, not that the engine's real mis-proposal rate is low. *Why this
  shape anyway:* that is exactly the point — the safety probe proves the GATE is load-bearing (the §28
  safety claim), and the engine's real mis-proposal rate is the REPORTED DoD#9 baseline, deliberately not
  gated. **ARGUS: confirm the safety probe correctly tests the gate (not the engine), per §28.**

---

## 7. DoD §5 mapping (gated vs reported)

| DoD # | Element | Probe(s) | Gated? |
|---|---|---|---|
| 1 | CHOREOGRAPHY → 8/6/7 byte-identical DECLARE | P1 | GATE |
| 2 | FAIL-CLOSED SAFETY (4 no-confirm actions + over/under) | P2a–P2f | GATE |
| 3 | §2-CONSTRAINT module-identity | P3 | GATE |
| 4 | CONFIRM-GATE evidence-rich contract present+tested | P4a, P4b | GATE |
| 5 | `detection_hints` DATA + P3 provenance | P5a, P5b | GATE |
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
- **Any change to `generate`/`resolve`/`validate`/the §0–§23 mechanism** — IMPORTED UNMODIFIED; the §8 sets
  are a regression target, hit not re-derived.

---

## 9. Provenance

Designed by **CAPTAIN_DAEDALUS_the_stoa** (gauntlet stage 1/6, arc stoa--fdf) from the authoritative
Phase-1 SUGGEST design (`agents/design/stoa--jw5/design-formal.md` §24–§31), the 35/35-PASS prototype
(`agents/design/stoa--jw5/suggest-check/`), and the shipped 2.1 core
(`agents/builder-deploy-core/builder_deploy_core`). The §28 neuro-symbolic capability premise was
**web-RE-verified at this seat** (gsearch / current docs 2026-06-26: DI-BENCH ACL2025 dependency-inference
benchmark, AST import-extraction-not-grep discipline, evidence-discovery multi-agent loop, dynamic-endpoint
LLM resolution — the §6.4 live-constraint check, NOT memory). No redesign of Phase-1; this is the
build-design that promotes the verified choreography into runnable packaged code and names the three new
Phase-2 pieces + the three §4 decisions. **Author: Denson Smith.**
