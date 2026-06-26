---
author: Denson Smith
ticket: stoa--pj3 (u--9s2 Phase-2 increment 2.1)
seat: CAPTAIN_DAEDALUS_the_stoa (ARCHITECT)
design-ground-truth:
  - agents/design/stoa--jw5/design-formal.md  (Phase-1 design, §1/§2/§3/§5.A/§17/§19/§20/§22)
  - beadwork:attachments/stoa--pj3/u9s2-phase2-inc1-directive.md  (the authoritative WHAT + DoD §5)
promotes:
  - agents/design/stoa--jw5/resolution-check/  (resolve.py + fixtures.py + run.py — VERIFIED 19/19)
  - agents/design/stoa--jw5/discovery-check/   (catalog.py + generate.py + validate.py + run.py — VERIFIED)
status: DESIGN — rev2 (folds ARGUS r1 + r2 cold-audit findings; rev1 kept intact for provenance)
supersedes: agents/design/stoa--pj3/design-rev1.md
as_of: 2026-06-26
---

# stoa--pj3 build design (rev2): promote the resolution + discovery prototypes into the real builder-deploy CORE

## 0. rev1 → rev2 changelog (what changed, and what is carried verbatim)

This rev2 folds the **two load-bearing findings** from ARGUS's cold-audit verdict
(`agents/verdicts/stoa--pj3/argus-verdict.md`, verdict `revise`). Everything else is carried
**verbatim** from rev1.

- **r1 fix (kinds-table externalization shape — pinned).** rev1 §2.1's "the functions already take
  `baseline`/`library` as parameters — we remove the literal defaults" over-generalized: it is true for
  `resolve()` / `resolve_with_lint()` (which carry the `baseline=BASELINE, library=LIBRARY` default
  seam, prototype L90/L127) but FALSE for `derive_sa_scope` (L168) and `check_runtime_completeness`
  (L183), which read `SCOPE_BEARING_KINDS` and `KEY_BEARING_PAIRING` as **module globals** (L179/L195),
  not parameters. rev2 **pins the refactor shape** (import-time module-global population, NO signature
  change to the two frozen functions) and **states the load-order / fail-closed contract** so a function
  called before load fails-closed instead of silently using empty tables. Corrected text lives in the
  rewritten §2.1 "what moves vs what is frozen" + a new §2.1.1 (r1 refactor contract). WP-4 is replaced
  by WP-4' (the residual after pinning).

- **r2 fix (fail-closed DATA-load-validation contract + probe).** rev1's `dataload` had no fail-closed
  behavior for malformed/incomplete DATA, and the §8/§23 fixtures (loading the same well-formed `data/`
  tree the core ships) would not catch a structurally-degraded file. The worked attack-path: a
  `baseline.toml` missing `pgvector` parses fine, silently shrinks the baseline 5→4, and the §8.4
  `BaselineOmitError` guard stops firing for `pgvector` — a fail-OPEN regression of the exact WP-6 fix.
  rev2 adds a **fail-closed load-validation contract** (new §2.4.1: invariants + a named
  `DataIntegrityError`, no partial load) and a **new load-validation probe P11** (proves the loader
  REJECTS a deliberately-corrupted DATA tree — distinct from P6, which only proves it READS a well-formed
  one). DoD #5 traceability row updated to cite P6 (READ) + P11 (VALIDATE). WP-6 is replaced by WP-6'
  (the residual after the probe).

- **Carried VERBATIM from rev1** (no change — ARGUS explicitly confirmed these): the YAML→TOML decision
  (§2.2; tomllib, `requires-python >=3.11`, JSON fallback reserved); the §35.5 threat carve-out
  classification (§2.7; CONFIRMED, no threat-anchored probe owed); the HOME-defer recommendation (§4;
  LEGITIMATE); the `document-data.toml` SEPARATE-FILE representation (§2.1/§2.2/RQ-3; FAITHFUL to
  design-formal §3.2 — NOT changed to an alias-key); the §2-constraint package edge (§2.3); the purity
  boundary single-`dataload` shape (§2.4); the fixtures-as-DATA suite (§2.6); all of §1, §3 P1–P10, §5
  rows 1–4/6–9, §6, §7, and §8 WP-1/WP-2/WP-3/WP-5. Probe P11 and DoD-row-5's P11 cite are the only §3/§5
  additions; §2.1.1 + §2.4.1 are the only §2 additions; the §2.1 "what moves" paragraph is the only §2
  rewrite.

---

## 1. Problem restatement

Two Phase-1 prototype harnesses are already designed, built, and VERIFIED (resolution-check: 19/19
checks, §8 fixtures 8/6/7 byte-for-byte, §8.4 fail-closed, all 5 baseline entries guarded;
discovery-check: 3 builders generate→resolve to 8/6/7, V1–V5 pass, NEG-1/NEG-2 fail-closed, resolver
reused unmodified). This arc **promotes** them into the real, runnable, packaged builder-deploy
**resolution + discovery CORE** — the front-end of the cookie-cutter that turns a builder's declared
`services:` list into a validated `{category, delta}` manifest and resolves it to its exact typed
credential set. The promotion is **structure, packaging, DATA externalization, and the deployment
HOME** — NOT a re-architecture of the resolver. The algorithms (resolve §2.5, derive_sa_scope §5.A,
runtime-completeness §3.4, kind-dispatch §3.3, generate G1–G4 §19, validate V1–V5 §20) are frozen as
proven; this design moves the currently-Python-hardcoded BASELINE / category library / kind
classifications / service→key catalog out into **real external DATA files** the core reads as data,
fixes the prototype's `sys.path` import hack into a proper package so discovery cleanly imports the
single resolver (the §2-constraint), locks the §8 / §23 / §8.4 fixtures as a re-runnable regression
suite, and **proposes** the skill's permanent deployment HOME for ratification (directive §3 — not to
be silently baked).

**Imported assumptions named** (per §6.1 — a restatement that hides imported scope has smoothed it):
- **(IA-1)** The arc builds on the `arc-75/build` branch in **the-stoa** regardless of which HOME is
  ratified; a later relocation is additive (directive §3 states this explicitly). So this design
  picks an *in-repo build location for 2.1* and treats the *permanent HOME* as a separately-ratified
  decision layered on top. These are two different decisions and I keep them distinct.
- **(IA-2)** "Reads no environment" (§2.3 purity) is read to permit exactly ONE filesystem touch: the
  core reading its **own DATA files** (directive load-bearing requirement #3 names this as the one
  permitted touch). I design that load boundary so it is auditable (one loader module, one DATA root,
  no other `open()`/`os.environ`/network/clock anywhere in the core).
- **(IA-3)** The directive §3.1/§3.2/§17.1 prose names the DATA homes as `baseline.yaml` /
  `categories/<name>.yaml` / `catalog/<service-id>.yaml`. I read "the directive names `baseline.yaml`
  + `categories/<name>.yaml` + the catalog" as naming the **logical DATA assets and their layout**,
  NOT as mandating the YAML *serialization* — the serialization is the explicit parser-decision the
  directive (load-bearing req #1) tells me to make. I keep the filenames' *role* and the *layout*
  while choosing the on-disk format. This is the load-bearing interpretation; I self-assess it in §9.

---

## 2. Approach

### 2.0 The shape in one paragraph

A single Python package `builder_deploy_core` with two sub-packages — `resolution` (the §2 resolver,
the single source of truth) and `discovery` (catalog + generate + validate, which *imports* resolution
and never re-implements it). All four data bodies that the prototypes hardcode (BASELINE, the category
library, the kind/scope/pairing classifications, the service→key catalog) move into a `data/` tree of
external files read once at load time by a single thin `dataload` module that **validates them
fail-closed** (§2.4.1). The §8 / §23 / §8.4 fixtures become a `pytest`-style regression suite under
`tests/` that VERA re-runs, structurally separate from the existing `app/` JS suite so the two cannot
interfere. The package is **runnable** (`python -m builder_deploy_core.resolution` and `... .discovery`
reproduce the prototype RESULTS) and **pure** (reads no environment beyond its own `data/` tree).

### 2.1 Package / file layout

The 2.1 build location (IA-1) is `agents/builder-deploy-core/` on the arc-75 branch. (Whether this is
the permanent HOME or a way-station to a relocated HOME is the §3 ratification decision — the *layout
below is HOME-independent*: it is a self-contained Python package that relocates as a unit.)

```
agents/builder-deploy-core/
├── README.md                         # author: Denson Smith; what this is, how to run, the §2-constraint statement
├── pyproject.toml                    # author: Denson Smith; package metadata; pins NOTHING at runtime (see §2.4)
├── builder_deploy_core/
│   ├── __init__.py                   # package marker; exports resolve, generate, validate, the error classes
│   ├── errors.py                     # ResolutionError, BaselineOmitError, UncatalogedServiceError, ValidationError, DataIntegrityError
│   ├── dataload.py                   # THE ONE filesystem boundary (§2.3 audit point). loads+VALIDATES data/ -> in-memory dicts (§2.4.1)
│   ├── resolution/
│   │   ├── __init__.py
│   │   └── resolve.py                # §2.5 resolve() + resolve_with_lint() + derive_sa_scope (§5.A)
│   │   │                             #   + check_runtime_completeness (§3.4). VERBATIM from the proven prototype,
│   │   │                             #   minus the inlined BASELINE/LIBRARY tables (now injected via params) and
│   │   │                             #   the inlined KINDS tables (now import-time module globals; see §2.1.1).
│   └── discovery/
│       ├── __init__.py
│       ├── generate.py               # §19 G1–G4 generate() + best_fit_emergent_category()
│       └── validate.py               # §20 V1–V5 validate(); V4 IMPORTS resolution (§2-constraint, §2.3 below)
├── data/
│   ├── baseline.toml                 # §3.1 BASELINE (the 5 non-omittable entries)
│   ├── kinds.toml                    # §3.3 kind enum + scope-bearing set + key-bearing pairing (was hardcoded)
│   ├── categories/
│   │   ├── geospatial.toml           # §3.2 category template
│   │   ├── document-consuming.toml   # §3.2
│   │   └── document-data.toml        # §3.2 alias of document-consuming (filename note in §2.5)
│   └── catalog/
│       ├── google-maps.toml          # §17.1/§22 seed record (carries BOTH gcp_api AND paired gcp_secret)
│       ├── spatial-db.toml           # §22 seed
│       ├── document-parsing.toml     # §22 seed
│       └── bls-oews.toml             # §22 seed (gcp_api: none, category: none)
└── tests/
    ├── conftest.py                   # loads the core + fixtures; provides the resolve/generate/validate handles
    ├── fixtures/                     # the §8/§23 fixtures as DATA (manifests + expected sets) — see §2.6
    │   ├── manifests/                #   prospector / scienceclaw / labstat_bls / badbuilder_pgvector_omit
    │   ├── expected/                 #   the 8/6/7 expected resolved sets (the LOCKED regression target)
    │   └── corrupt-data/             #   §2.4.1 — deliberately-malformed DATA trees for the P11 load-validation probe
    ├── test_resolution.py           # §8.1/8.2/8.3 exact-set + §8.4 BaselineOmitError(all 5) + §3.4 + §5.A + §3.3
    ├── test_discovery.py            # §23.1 generate→resolve→8/6/7 + equivalence + V1–V5 + NEG-1 + NEG-2 + §2-constraint
    └── test_dataload.py             # §2.4.1 fail-closed load-validation — REJECTS each corrupt-data/ tree (P11)
```

**What moves vs what is frozen (r1-corrected — this paragraph is the rev1 rewrite).** The *logic* of
`resolve.py`, `generate.py`, `validate.py` is the proven prototype code transcribed UNCHANGED (the
directive: "harden + package + externalize", not re-derive). The data tables stop being module-level
literals and become DATA loaded by `dataload`, but the **injection mechanism is NOT uniform across the
functions** — and that non-uniformity is the r1 finding ARGUS surfaced. There are exactly two seams:

- **Parameter seam (already exists in the prototype).** `resolve(manifest, baseline, library)` and
  `resolve_with_lint(manifest, baseline, library)` already accept `baseline` / `library` as parameters
  (prototype L90 / L127), defaulted to the inlined `BASELINE` / `LIBRARY` literals. The edit is
  mechanical: **delete the literal defaults**, so the caller MUST pass the `dataload`-loaded baseline +
  library. No signature change.

- **Module-global seam (does NOT pre-exist — the r1 case).** `derive_sa_scope(resolved_set)` (L168)
  and `check_runtime_completeness(resolved_set)` (L183) take ONLY `resolved_set`; they read
  `SCOPE_BEARING_KINDS` (L179) and `KEY_BEARING_PAIRING` (L195) as **module globals**, not parameters.
  Externalizing `kinds.toml` therefore requires a choice rev1 elided. **rev2 pins the shape: keep these
  two functions' signatures UNCHANGED and populate the module globals at import time** (the import-time
  module-global pattern, contract in §2.1.1). The rejected alternative (changing the two frozen
  signatures to accept the kind-tables as parameters) is named + rejected in §2.1.1.

The remaining logic edit is `(c)` the `sys.path` hack in the discovery prototype's `run.py` becoming a
real intra-package import (§2.3). No other logic-byte change.

### 2.1.1 r1 refactor contract: import-time module-global population for the §3.3 kind-tables (PINNED)

**The shape ADA builds (no ambiguity).** `resolution/resolve.py` keeps the two module-level names
`SCOPE_BEARING_KINDS` and `KEY_BEARING_PAIRING` (and `KIND_ENUM`), but they are **no longer literal
assignments**. They are initialized to a **fail-closed sentinel** and populated exactly once from
`dataload` at package import time. `derive_sa_scope` (L168) and `check_runtime_completeness` (L183)
keep their **current signatures verbatim** (`(resolved_set)`) and keep reading the module globals —
zero edit to the two frozen function bodies.

**Why import-time globals, not a signature change (the rejected alternative).** Changing
`derive_sa_scope` / `check_runtime_completeness` to `(resolved_set, scope_bearing)` /
`(resolved_set, pairing)` would edit two PROVEN function signatures and force every call site
(`validate.py` V4, `run.py`, the tests) to thread the kind-tables through — a wider diff to frozen
surface than the directive's "freeze the logic" intends, and a new way for a caller to pass the wrong
table. Keeping the signatures and populating the globals from DATA is the **smaller, more faithful**
edit: the functions read the kind-tables exactly as they do today; only the *source* of the globals
moves from a literal to a `dataload` call. (This is the same global-read shape the prototype already
ships; we are swapping the assignment's right-hand side, not the read.)

**The load-order / fail-closed contract (so the import-time pattern is not fragile).** Three rules,
all ADA-buildable and P11/P7-checkable:

1. **Single population site, at import.** `resolution/__init__.py` (the package-import entry for the
   resolution sub-package) calls `dataload.load_kinds()` exactly once and assigns the result into the
   `resolve` module's globals: `resolve.KIND_ENUM, resolve.SCOPE_BEARING_KINDS, resolve.KEY_BEARING_PAIRING
   = dataload.load_kinds()`. Because Python executes a package's `__init__.py` before any of its
   members are usable, `import builder_deploy_core.resolution` (or any `from ...resolution.resolve
   import ...`) guarantees the globals are populated before `derive_sa_scope` /
   `check_runtime_completeness` can be called. `dataload.load_kinds()` runs the §2.4.1 fail-closed
   validation, so a malformed/incomplete `kinds.toml` raises `DataIntegrityError` at import — the
   package does not finish importing with degraded tables.

2. **Fail-closed sentinel, never an empty table.** The module-level initial values are a sentinel that
   is *not a valid empty collection* — concretely `SCOPE_BEARING_KINDS = KEY_BEARING_PAIRING =
   _UNLOADED` where `_UNLOADED` is a module singleton whose membership/iteration raises
   `DataIntegrityError("kind-tables read before dataload populated them")`. This makes "a function
   called before load" fail-CLOSED (raise) rather than silently using an empty set (which would make
   `derive_sa_scope` return `[]` and `check_runtime_completeness` find zero pairings — a silent
   fail-OPEN exactly like the r2 baseline-shrink). The sentinel is the load-order guard's teeth: even
   if some future caller imports `resolve.py` in a way that bypassed `__init__.py` population, the
   first read of the kind-tables raises rather than mis-resolves.

3. **No re-entrancy, no mutation after load.** `load_kinds()` is idempotent-by-replacement (assigns,
   does not append); nothing else writes these globals. There is no per-call reload, no env-driven path,
   no clock — consistent with §2.4 purity.

**Net diff to frozen files under this contract:** `resolve.py` loses the three literal kind-table
assignments (replaced by the `_UNLOADED` sentinel) and loses the `BASELINE`/`LIBRARY` literal defaults
on `resolve`/`resolve_with_lint`; `derive_sa_scope` and `check_runtime_completeness` bodies AND
signatures are **byte-unchanged**. `resolution/__init__.py` gains the single population call. That is
the entire r1 footprint.

### 2.2 DATA-file schemas + chosen format + the parser decision (DoD #5, load-bearing req #1)

**The tension (named head-on, directive load-bearing req #1).** §3.1/§3.2/§17.1 write the DATA as
YAML. YAML has no stdlib parser — it needs PyYAML (third-party). §2.3 demands the core read no
environment and, by spirit, be runnable as **pure software with zero hidden dependency** on a fresh
builder machine. PyYAML being present in *this* DAEDALUS environment is irrelevant (memory lesson:
verify a runtime capability is UNCONDITIONAL + version-floored, not present-in-my-session) — a builder
machine that pip-installs nothing would `ImportError` on `import yaml` and the "pure software"
property would be a lie.

**The decision: TOML, read with stdlib `tomllib`.** Python 3.11+ ships `tomllib` in the standard
library (read-only TOML parser) — confirmed live in this env (`python -c "import tomllib"` → OK on
3.11.4). This gives the directive's intent (real external DATA files the core reads as data, not
hardcoded) with **zero third-party dependency** and **no purity asterisk**. TOML expresses the
`{kind, name}` entry records cleanly (arrays of tables). The `pyproject.toml` declares
`requires-python = ">=3.11"` so the floor is explicit and the property is **unconditional + version-
floored**, not session-incidental.

**Why not the alternatives (named + rejected, §6.2 pair):**
- **YAML + PyYAML pinned dependency** — honors §3.1's literal filenames but reintroduces a third-party
  parser, contradicting §2.3 "pure software that reads no environment" intent and adding an install
  step to every builder machine. Rejected: a pinned dep on a fresh machine is exactly the hidden-
  environment coupling 2.1 is supposed to be free of.
- **JSON + stdlib `json`** — also zero-dependency and stdlib-universal (works <3.11 too). Rejected
  *as the primary* only because JSON has no comments, and the DATA files carry load-bearing WHY
  comments in the design (`# DECIDE-A: pgvector is BASELINE`, the §3.4 pairing rationale) that are
  author-facing documentation; TOML keeps them. **Fallback:** if ARGUS/ratification judges the 3.11
  floor too aggressive for the eventual HOME's consumer base, JSON is the drop-in alternative (same
  schema, same loader shape, `json.load` instead of `tomllib.load`, comments demoted to a sidecar
  `.md`). I flag this as the cheapest pivot. (ARGUS ruled the 3.11 floor acceptable for the in-the-stoa
  2.1 build; JSON correctly reserved for the deferred-HOME consumer-floor case.)
- **Vendor a minimal YAML loader** — keeps the literal `.yaml` extension but ships hand-rolled parser
  code we'd own and test. Rejected: more code + more risk than using a stdlib parser for a format
  that expresses the same data.

**Directive-fidelity note (IA-3):** the directive names `baseline.yaml` + `categories/<name>.yaml`
descriptively. I preserve the **logical assets, the layout, and the filename stems** (`baseline`,
`categories/<name>`, `catalog/<service-id>`) and change only the *extension/serialization* to `.toml`
per the parser decision the directive itself asked me to make. This is a self-assessed
interpretation (§9 WP-1); if ratification wants the literal `.yaml` bytes, the JSON/PyYAML fallbacks
above are the two named pivots. (ARGUS ruled this read SOUND.)

**Schemas (TOML rendering of the design's records):**

`data/baseline.toml` (§3.1):
```toml
# §3.1 BASELINE — fixed T1, never per-builder. The 5 NON-OMITTABLE entries (§2.6).
[[entry]]
kind = "gcp_api"
name = "gemini-embedding"
# ... gemini-search / DATABASE_URL(railway_var) / POSTGRES_PASSWORD(gcp_secret) / pgvector(db_extension)
```

`data/categories/geospatial.toml` (§3.2): one `[[entry]]` array per template file; the file stem IS
the category name. (`document-data.toml` is the alias-of-`document-consuming` file; §2.5 maps the
on-disk stem `document-data` ↔ the design's category name `document/data` in the loader, since `/` is
not a portable filename char — the loader holds the single stem↔name map so resolve() still sees the
exact design category strings. ARGUS r3: the SEPARATE-FILE representation is FAITHFUL to design-formal
§3.2, which itself encodes `document/data` as a separate top-level key — do NOT change it to an
alias-key.)

`data/kinds.toml` (§3.3 — was `KIND_ENUM` + `SCOPE_BEARING_KINDS` + `KEY_BEARING_PAIRING`):
```toml
kind_enum = ["gcp_api","gcp_secret","railway_var","db_extension","thirdparty_rest_key"]
scope_bearing = ["gcp_api","gcp_secret","thirdparty_rest_key"]
[[key_bearing_pairing]]   # §3.4 in-band pairing
api  = { kind = "gcp_api",    name = "google-maps" }
secret = { kind = "gcp_secret", name = "MAPS_API_KEY" }
```

`data/catalog/google-maps.toml` (§17.1/§22): `service-id`, an `[[entries]]` array (1:N — carries BOTH
the gcp_api AND its paired gcp_secret, the §17.2 construction invariant), `gcp_api`, `category`.

### 2.3 Module dependency graph (the §2-constraint, DoD #6)

The §2-constraint: **discovery's V4 imports the single resolver, never re-implements it.** The
prototype proved this with a `sys.path.insert` hack pointing at `../resolution-check`. The promotion
replaces that with a real package edge:

```
                         dataload.py
                        (the ONE fs boundary; loads+VALIDATES data/ -> dicts, §2.4.1)
                              │ (provides BASELINE, LIBRARY, KINDS, CATALOG, CATEGORIES)
              ┌───────────────┴───────────────┐
              ▼                                ▼
   resolution/resolve.py            discovery/generate.py
   (resolve, resolve_with_lint,     (G1–G4; reads BASELINE for G3,
    derive_sa_scope §5.A,            catalog+categories for G1/G2)
    check_runtime_completeness §3.4;
    KINDS globals populated at
    import via resolution/__init__, §2.1.1)
              ▲                                │
              │  IMPORTS (the §2-constraint)   │ produces {category, delta}
              │                                ▼
              └──────────────────  discovery/validate.py
                                   (V1–V5; V4 calls resolution.resolve +
                                    resolution.check_runtime_completeness +
                                    catches errors.BaselineOmitError — REUSED, never reimplemented)

errors.py  ← imported by all three (single home for the 5 exception classes incl. DataIntegrityError)
```

**The edge that proves the constraint:** `discovery/validate.py` has `from builder_deploy_core.resolution.resolve
import resolve, check_runtime_completeness` and `from builder_deploy_core.errors import BaselineOmitError`.
There is **no** copy of the resolution algorithm anywhere under `discovery/`. The dependency is acyclic
and one-directional: `discovery → resolution`, never the reverse (resolution does not know discovery
exists). `test_discovery.py` keeps the prototype's explicit §2-constraint assertion (resolve's
`__module__` / source file is the resolution package, not a discovery-local copy) as a machine probe.

### 2.4 Purity boundary (DoD #6, directive req #3)

`dataload.py` is the **single** module that performs filesystem I/O, and it touches ONLY files under
the package's own `data/` root (resolved relative to `__file__`, never from an env var or CWD). The
audit property: **grep the core for `os.environ`, `open(`, `socket`, `requests`, `urllib`,
`subprocess`, `time.time`, `datetime.now`, `random` → the only `open(`/`tomllib.load` hits are inside
`dataload.py`, scoped to `data/`; everything else is zero.** This is a concrete, VERA-re-runnable
probe (§3 below), not a claim. `pyproject.toml` declares no runtime dependencies (only `requires-
python = ">=3.11"`); the test extra may add `pytest` but the *core* imports stdlib-only.

### 2.4.1 r2 fail-closed DATA-load-validation contract (new — the r2 fix)

**The gap ARGUS named.** `dataload` had no specified behavior for **malformed or incomplete DATA**,
and the §8/§23 fixtures load the SAME well-formed `data/` tree the core ships — exercising the happy
path only. Worked attack-path: a `data/baseline.toml` missing `pgvector` parses fine, silently shrinks
the resolved baseline 5→4, and the §8.4 `BaselineOmitError` guard stops firing for `pgvector` — a
fail-OPEN regression of the exact WP-6 fix the resolver was hardened for, invisible to fixtures whose
expected sets are themselves loaded from a parallel DATA file (the WP-3 doubled-surface risk compounds
it: one bad edit touching BOTH `data/` and `tests/fixtures/expected/` keeps the suite green against a
wrong target). P6 proves the loader READS the file; it does not prove the loader VALIDATES it.

**The contract: `dataload` validates every DATA body on load and RAISES `DataIntegrityError`
(fail-closed, no partial load) on ANY violation.** Validation runs INSIDE the load functions
(`load_baseline()`, `load_kinds()`, `load_library()`, `load_catalog()`), BEFORE any caller receives a
table; a violation raises and the load returns NOTHING (no degraded dict escapes the boundary). The
invariants, one body at a time:

- **baseline** (the r2-worked surface): the loaded baseline MUST be **exactly the 5 expected
  non-omittable entries** — `{(gcp_api,gemini-embedding), (gcp_api,gemini-search),
  (railway_var,DATABASE_URL), (gcp_secret,POSTGRES_PASSWORD), (db_extension,pgvector)}`. The check is a
  set-equality against a **named, in-`dataload` constant `EXPECTED_BASELINE`** (the §3.1 enumeration,
  the same SSoT the design states). Any missing entry (pgvector dropped), any extra entry, any
  duplicate, any count ≠ 5 → `DataIntegrityError`. This is the direct r2 fix: the pgvector-drop now
  fails the LOAD, never reaching the resolver to silently shrink the baseline. (Rationale for
  full-set-equality, not a length check: a length check passes if one entry is dropped AND a typo'd
  entry is added; set-equality against the named SSoT catches both.)
- **kinds** (`kinds.toml`, the r1 surface): `kind_enum` MUST equal the expected 5-kind set
  `{gcp_api, gcp_secret, railway_var, db_extension, thirdparty_rest_key}`; `scope_bearing` MUST be a
  **non-empty subset of `kind_enum`** equal to the expected `{gcp_api, gcp_secret, thirdparty_rest_key}`;
  every `key_bearing_pairing` row MUST be a well-typed `{api:{kind,name}, secret:{kind,name}}` whose
  `api.kind`/`secret.kind` are in `kind_enum`. Any deviation → `DataIntegrityError`. (This protects the
  §2.1.1 import-time population: a kinds.toml that drops `scope_bearing` or ships an empty list would
  otherwise make `derive_sa_scope` return `[]` — a silent fail-OPEN twin of the baseline-shrink.)
- **categories** (each `categories/*.toml`): non-empty `[[entry]]` array; every entry a well-typed
  `{kind, name}` with `kind ∈ kind_enum` and non-empty `name`; the file stem maps to a known category
  name via the stem↔name table. A category file with zero entries, an entry missing `kind`/`name`, or
  an unknown `kind` → `DataIntegrityError`.
- **catalog** (each `catalog/*.toml`): required keys present (`service-id`, `entries`, `gcp_api`,
  `category`); `entries` a non-empty array of well-typed `{kind, name}`; `kind ∈ kind_enum`; `category`
  either a known category name or the literal `none`. Missing required key / malformed entry / unknown
  kind → `DataIntegrityError`.
- **cross-body** (cheap, catches the r2-adjacent integrity slip): every `category` referenced by a
  catalog record either names a known `categories/*.toml` stem or is `none`; every
  `key_bearing_pairing.api`/`.secret` entry's `name` appears in some loaded body. A dangling reference
  → `DataIntegrityError`.

**Fail-closed, not fail-degraded.** On the FIRST violation in any body, `dataload` raises
`DataIntegrityError` with the offending body + the specific invariant breached (e.g.
`DataIntegrityError("baseline: expected 5 entries, got 4; missing {('db_extension','pgvector')}")`).
No partial table is returned; the import (for `load_kinds` via §2.1.1) or the explicit load call (for
baseline/library/catalog) fails. This is the same fail-closed posture as the resolver's §8.4
`BaselineOmitError` — extended one layer earlier, to the DATA-load boundary.

**Why a separate named error.** `DataIntegrityError` (in `errors.py`) is distinct from
`ResolutionError`/`BaselineOmitError`/`UncatalogedServiceError`/`ValidationError`: those signal a
fail-closed REFUSAL of a builder's *input manifest*; `DataIntegrityError` signals a corrupt *core DATA
asset* — a different failure class (the cookie-cutter's own ground truth is broken, not the builder's
declaration). Keeping them distinct lets P11 assert the precise error and keeps the §8.4 guard's
semantics unmuddied.

### 2.5 Runnability

`python -m builder_deploy_core.resolution` and `python -m builder_deploy_core.discovery` reproduce the
two prototype RESULTS.md runs (the `run.py` harness logic moves into `__main__.py` of each sub-package
OR stays as thin `run.py` shims — ADA's call; the design requires only that both are runnable and
print the same PASS lines the prototypes did). The authoritative pass/fail is the `tests/` suite (§2.6).

### 2.6 The locked regression suite (DoD #1/#2/#3/#4)

The §8 + §23 + §8.4-negative fixtures become the skill's **locked acceptance/regression suite**.
Structure decision: **fixtures-as-DATA, runner-as-code.** The manifests and their expected resolved
sets live under `tests/fixtures/` as TOML (manifests) + TOML (expected `(kind,name)` lists), mirroring
the byte-for-byte §8 enumerations. `test_resolution.py` / `test_discovery.py` / `test_dataload.py` are
thin `pytest` runners that load the fixtures and assert. WHY fixtures-as-data: the directive locks the
§8 *sets* (8/6/7 byte-for-byte) as the regression target — keeping them as DATA, not buried in Python
literals, makes the locked target auditable and lets VERA diff the expected set against the design's §8
prose directly. The runner stays code because the *assertions* (exact-set match, raises-BaselineOmitError,
runtime-completeness holds, SA-scope == scope-bearing subset, V1–V5, NEG-1/NEG-2, §2-constraint,
load-validation-rejects-corrupt) are behavior, not data.

**Locked contents (the regression target, one row per locked behavior):**
- `test_resolution`: prospector→8 / scienceclaw→6 / labstat_bls→7 EXACT; §8.4 raises
  `BaselineOmitError` naming `(db_extension, pgvector)`, no set returned; **the guard fires for all 5
  baseline entries** (parametrized over each of the 5 — the R1-close generalization, DoD #1); §3.4
  runtime-completeness holds (prospector carries BOTH `google-maps` AND `MAPS_API_KEY`); §3.3
  kind-dispatch (labstat_bls `BLS_OEWS_API_KEY` is `thirdparty_rest_key`, mints no `gcp_api`, excluded
  from S1); §5.A SA-scope == scope-bearing subset, no foreign entry.
- `test_discovery`: each of the 3 builders generate→resolve to 8/6/7 EXACT and is manifest-equivalent
  to the §8 hand-authored manifest (alias-aware: `document/data` ≡ `document-consuming`); V1–V5 pass;
  NEG-1 (undeclared shadow → V5 fail-closed); NEG-2 (uncataloged declared → `UncatalogedServiceError`
  + V1 fail); the §2-constraint probe (resolve is the imported resolution callable).
- `test_dataload` (r2 — new): for each corrupt DATA tree under `tests/fixtures/corrupt-data/`, loading
  it raises `DataIntegrityError` naming the breached invariant; the canonical case is
  `baseline-missing-pgvector/` (baseline of 4) → raises, never returns a 4-entry baseline. (Detail in
  P11.)

### 2.7 Threat→mitigation map (§6.12)

`not threat-ratified (process/tooling change, no runtime attack path)`. This arc promotes pure,
offline, environment-free software (resolution + discovery logic + DATA files) with an explicit §2.3
no-environment / no-network / no-credential boundary; it provisions nothing and is reachable by no
external actor. There is no named threat in the directive, the design-formal sections in scope, or the
prototype RESULTS for 2.1; the live Phase-2 residuals R-1/R-2/R-3 are explicitly deferred to 2.3
(directive §4) and do not bind at t0. Per §35.5 this is the carved-out class (no runtime attack path);
I PROPOSE the `not threat-ratified` classification — ARGUS CONFIRMED it. Accordingly §3 carries no
threat-anchored probe (§6.13). The new r2 load-validation contract (§2.4.1) + probe P11 mitigate a
**correctness** fail-closed gap at the DATA-load boundary, NOT a threat: at t0 the DATA is in-repo,
version-controlled, and gauntlet-gated, not attacker-supplied (ARGUS confirmed this is a correctness
surface, not a threat surface). The §8.4 / NEG-1 / NEG-2 / P11 fail-closed probes verify the design's
*correctness* invariants, not a threat-defeat.

---

## 3. Verification probes (what would falsify this design)

Each is a concrete command/behavior VERA re-runs. Destructive ops avoided (read-only; the P11 corrupt
trees are committed fixtures, not mutated in place).

**P1 — resolution exact sets (DoD #1).** `python -m pytest agents/builder-deploy-core/tests/test_resolution.py`
→ all pass; prospector resolves to exactly the 8 §8.1 entries, scienceclaw to the 6 §8.2, labstat_bls
to the 7 §8.3, byte-for-byte. Falsifier: any set count ≠ 8/6/7 or any entry mismatch.

**P2 — baseline-omit guard, all 5 (DoD #1).** The §8.4 test + a parametrization that, for EACH of the
5 baseline entries, builds an omit-that-entry manifest and asserts `resolve()` raises
`BaselineOmitError` naming that entry, returning no set. Falsifier: any baseline entry whose omit does
not fail-closed.

**P3 — generate→resolve→8/6/7 + equivalence (DoD #2).**
`python -m pytest agents/builder-deploy-core/tests/test_discovery.py -k generate` → each builder's
declared `services:` generates a `{category, delta}` that the UNCHANGED resolver resolves to 8/6/7 and
is equivalent to the §8 hand-authored manifest. Falsifier: a generated manifest that resolves to a
different set than its hand-authored twin.

**P4 — V1–V5 + NEG-1 + NEG-2 (DoD #3).** `... test_discovery.py -k "validate or neg"` → V1–V5 pass on
every positive; NEG-1 trips V5 fail-closed; NEG-2 raises `UncatalogedServiceError` and trips V1.
Falsifier: a negative that does not fail-closed, or a positive that fails a V-check.

**P5 — resolved-set properties (DoD #4).** Asserts SA-scope (§5.A) excludes non-scope-bearing kinds;
prospector carries BOTH `(gcp_api, google-maps)` AND `(gcp_secret, MAPS_API_KEY)` (§3.4);
labstat_bls `BLS_OEWS_API_KEY` is `thirdparty_rest_key`, has no `(gcp_api, BLS_OEWS_API_KEY)`, and is
excluded from the S1 gcp_api list (§3.3). Falsifier: any property violated.

**P6 — DATA externalized / READ (DoD #5).** Mutate a copy of `data/baseline.toml` (e.g. add a 6th
entry in a tmp data root) and show the resolved baseline set changes accordingly — proving the resolver
READS the file rather than a hardcoded literal. Also: grep the logic modules (`resolve.py`,
`generate.py`, `validate.py`) for inlined `BASELINE = [` / `LIBRARY = {` / `CATALOG = {` /
`SCOPE_BEARING_KINDS = {` / `KEY_BEARING_PAIRING = {` literals → ZERO hits (the tables now live in
`data/`, loaded by `dataload`; the kind globals are the §2.1.1 `_UNLOADED` sentinel + import-time
population, not a literal). Falsifier: a logic module still carrying a data literal, or the resolver
ignoring a changed DATA file. (Note: the tmp-data-root mutation must keep the baseline at the valid
5-entry set or use a body whose §2.4.1 invariant still holds — adding a 6th entry violates the
baseline set-equality invariant and would now correctly raise `DataIntegrityError`; for the READ proof,
mutate a body without a fixed-set invariant, e.g. add a catalog seed, OR temporarily relax the probe's
expected baseline by editing both the data and `EXPECTED_BASELINE` in the tmp copy. P11 is the
companion that proves VALIDATE.)

**P7 — purity boundary (DoD #6).** `grep -rn -E "os\.environ|(^|[^.])open\(|socket|requests|urllib|subprocess|time\.time|datetime\.now|random" agents/builder-deploy-core/builder_deploy_core/`
→ the only matches are the `tomllib.load`/`open(` calls inside `dataload.py` scoped to `data/`;
everything else zero. Falsifier: any environment read outside `dataload.py`.

**P8 — §2-constraint (DoD #6).** `... test_discovery.py -k constraint` asserts the `resolve` callable
V4 uses resolves to the `builder_deploy_core.resolution.resolve` module (its `__module__` / `__file__`),
NOT a discovery-local copy; AND `grep -rn "def resolve" agents/builder-deploy-core/builder_deploy_core/discovery/`
→ ZERO hits (discovery never defines a resolve). Falsifier: a resolve definition under discovery/, or
V4 binding to a non-resolution callable.

**P9 — full existing suite green (DoD #7).** `cd app && npm run gen-data && npm test && npm run build`
→ the existing the-stoa JS suite (roster derivation + vitest + vite build) stays GREEN. The new core
lives under `agents/builder-deploy-core/` (a Python package), entirely outside `app/`; gen-data reads
`substrate/`, not `agents/` — so the new code is structurally incapable of touching the roster. This
probe confirms the change breaks nothing. (VERA runs the FULL suite IN ADDITION to P1–P8, P10, P11 —
bespoke probes prove the new core works; the full suite catches what it breaks elsewhere.)

**P10 — authorship (DoD #8).** `grep -rn -E "author|owner|creator|maintainer|copyright|by:" agents/builder-deploy-core/`
→ every author-like field reads `Denson Smith`; ZERO foreign name. Falsifier: any foreign author field.

**P11 — DATA load-validation fail-closed (DoD #5; the r2 fix — distinct from P6's READ proof).**
`python -m pytest agents/builder-deploy-core/tests/test_dataload.py` → for each deliberately-corrupted
DATA tree committed under `tests/fixtures/corrupt-data/`, `dataload`'s load function RAISES
`DataIntegrityError` (no partial/degraded table returned). The locked cases, one per §2.4.1 invariant:
- **`baseline-missing-pgvector/`** (the canonical r2 attack-path): a `baseline.toml` with the
  `(db_extension, pgvector)` entry removed (baseline of 4) → `load_baseline()` raises
  `DataIntegrityError` naming the missing pgvector entry; it does NOT return a 4-entry baseline. This
  is the direct proof that the r2 fail-OPEN regression is now caught at load, BEFORE the resolver can
  silently shrink the baseline + stop firing the §8.4 guard for pgvector.
- **`baseline-extra-entry/`** (set-equality, not length): baseline with a 6th spurious entry → raises.
- **`kinds-empty-scope-bearing/`** (the §2.1.1-protecting case): `kinds.toml` with `scope_bearing = []`
  → `load_kinds()` raises (would otherwise make `derive_sa_scope` silently return `[]`).
- **`category-malformed-entry/`**: a category file with an entry missing `name` → raises.
- **`catalog-missing-key/`**: a catalog file missing the required `category` key → raises.
- **`dangling-reference/`** (cross-body): a catalog record naming a non-existent category → raises.

Falsifier: ANY corrupt tree that loads without raising (a degraded/partial table escaping the boundary),
OR a `DataIntegrityError` that does not name the breached invariant. This is the probe that proves the
loader VALIDATES, not merely READS — closing the r2 correctness gap.

---

## 4. The ONE decision PROPOSED for ratification: the skill's structure + permanent HOME (directive §3)

**This is presented as a PROPOSAL with options + tradeoffs, flagged for Polybius_the_Stoa ratification
(PLINY surfaces it up through the floor-manager). It is NOT baked into the build target — 2.1 builds on
arc-75 in the-stoa regardless (IA-1); any relocation is additive.**

### Option A — the-stoa as the forge-owned home

The builder-deploy core lives in the-stoa's substrate (e.g. `substrate/skills/builder-deploy/` or a
sibling forge-owned tooling dir) and is deployed/versioned by the-stoa's `install.sh` lifecycle, the
same way substrate role files and skills are.

- **+ Discoverability:** lands where every other forge asset lives; one repo to find it in.
- **+ Lifecycle:** rides the-stoa's existing arc/gauntlet/install machinery — versioned, gauntlet-
  gated, deployed by the proven `install.sh` mechanism. No new home to stand up.
- **+ Authorship/governance:** the-stoa's authorship + arc discipline already covers it.
- **− Coupling:** binds the builder-deploy core's release cadence to the-stoa substrate lifecycle. A
  builder workspace that wants the core would consume it via the-stoa's deploy path (or vendor a copy),
  which couples builder tooling to a substrate-deploy concept it may not otherwise use.
- **− Conceptual fit:** the-stoa is "the recursive-agent substrate"; the builder-deploy cookie-cutter
  is arguably a *different product* that happens to be incubated here.

### Option B — a standalone builder-tooling location consumed by builder workspaces

The core lives in its own home (a dedicated builder-tooling repo / package) that builder workspaces
consume directly (pip-installable package, or a cloned tooling repo).

- **+ Decoupling:** independent release cadence; builder workspaces consume it without pulling in the
  substrate-deploy concept.
- **+ Conceptual fit:** the cookie-cutter is a product in its own right; a standalone home matches the
  Grand's "runnable cookie-cutter to drive via a fresh decompose" framing (u--9s2).
- **+ Consumer clarity:** a builder workspace's dependency on "the builder-deploy core" is explicit and
  versioned, not "whatever the-stoa happened to deploy."
- **− Relocation cost NOW:** standing up a new home (repo, CI, install path, authorship scaffold)
  before 2.2/2.3 even exist is premature; the consumer set (builder workspaces) does not yet exist.
- **− Discoverability NOW:** a second home to find, with its own bw/arc discipline to bootstrap.

### Recommendation (for ratification, not a fait-accompli)

**Build 2.1 in the-stoa now (a DECISION-NEUTRAL `agents/` location, per ARGUS r4), and DEFER the
permanent-HOME choice to the point where a real consumer exists — i.e. when 2.3 (provisioning
choreography) or the first real builder workspace forces the question.** Rationale: (1) the directive
already mandates the arc-75/the-stoa build location and says relocation is additive (IA-1), so building
here costs nothing toward a later move; (2) the package layout in §2.1 is **HOME-independent by
construction** — a self-contained Python package with its own `data/` + `tests/`, relocatable as one
unit, so the relocation cost is a `git mv` + updated install/consume path, not a redesign; (3) deciding
B now optimizes for a consumer set (builder workspaces) that does not yet exist — premature.
**ARGUS r4 note carried for the ratifier: the 2.1 build location is `agents/builder-deploy-core/`, which
is NEITHER a soft Option-A lean (it is not under `substrate/skills/`, so it does NOT currently ride the
`install.sh` lifecycle) NOR an Option-B standalone home — it is a decision-NEUTRAL arc-build location.
Read "build here now" as "decide later," not "leaning A."** My recommendation is therefore "neutral
`agents/` location for 2.1, permanent HOME = explicitly DEFERRED, revisited at 2.3 with the
standalone-package (Option B) as the leading candidate once a consumer exists." Polybius_the_Stoa
ratifies; escalate to Grand if the deferral itself is judged load-bearing.

---

## 5. DoD-#-to-design-element traceability (directive §5, items 1–9)

| DoD # | Requirement | Where this design satisfies it |
|---|---|---|
| **1** | Resolver reproduces §8 (8/6/7 byte-for-byte); §8.4 raises `BaselineOmitError`, no set; guard fires for all 5 baseline entries | §2.1 `resolution/resolve.py` (frozen §2.5 logic) + §2.6 locked suite `test_resolution` (parametrized over all 5) + probes **P1, P2** |
| **2** | Generator: declared `services:` → `{category,delta}` the UNCHANGED resolver resolves to 8/6/7, equivalent to §8 (alias-aware) | §2.1 `discovery/generate.py` (frozen §19 G1–G4) + §2.3 dependency edge + §2.6 `test_discovery` + probe **P3** |
| **3** | V1–V5 pass; NEG-1 (V5 fail-closed) + NEG-2 (`UncatalogedServiceError` + V1 fail) hold | §2.1 `discovery/validate.py` (frozen §20 V1–V5) + §2.6 `test_discovery` + probe **P4** |
| **4** | Resolved-set properties: SA-scope §5.A, runtime-completeness §3.4, kind-dispatch §3.3 | §2.1 `resolve.py` (`derive_sa_scope`, `check_runtime_completeness`) + §2.1.1 import-time kind-table population + §2.6 + probe **P5** |
| **5** | DATA externalized: baseline / category templates / catalog are real DATA files (not hardcoded), read as data — AND validated fail-closed on load | §2.1 `data/` tree + §2.2 TOML schemas + parser decision + §2.1/§2.1.1 "what moves" (literals → injected params + import-time globals) + **§2.4.1 fail-closed load-validation contract** + probe **P6** (READ) + probe **P11** (VALIDATE) |
| **6** | Purity (reads no environment beyond own DATA); §2-constraint (discovery imports resolver, never re-implements) | §2.3 dependency graph + §2.4 purity boundary (single `dataload`) + probes **P7, P8** |
| **7** | Full existing the-stoa suite GREEN (gen-data + app build) in addition to bespoke fixtures | §2.1 layout (core lives under `agents/`, outside `app/`; gen-data reads `substrate/`) + probe **P9** (VERA runs full suite + P1–P8, P10, P11) |
| **8** | `author: Denson Smith` on every artifact; ZERO foreign author field | Frontmatter of this doc + every artifact in §2.1 carries `author: Denson Smith` (prototype files already do) + probe **P10** |
| **9** | Home proposal surfaced for ratification, not silently chosen | §4 (Options A/B + tradeoffs + recommendation + IA-1 build-location vs permanent-HOME split; ARGUS r4 decision-neutral note); flagged for Polybius_the_Stoa via PLINY→FM |

---

## 6. Out of scope (kept off ADA's plate; deferred per directive §2 OUT)

- **SUGGEST agent / front-door (§24–31)** — increment 2.2. Not designed here.
- **Provisioning choreography S0–S6 + any real repo→DB→GCP→Railway→Tailscale deploy (§4/§6/§7)** —
  increment 2.3 (CHIRON+HAMILTON). The DATA `kind` recipes (§3.3 table) are *named* in DATA but NOT
  *executed*; 2.1 emits/validates, it does not apply.
- **scienceclaw acceptance test** — increment 2.4.
- **ALL real infrastructure** — no gcloud/Railway/credentials/network/clock. Hard boundary (§2.3,
  §2.4, probe P7). If any build step reaches toward infra, STOP and flag — it has crossed the 2.1 line.
- **R-1/R-2/R-3 (prune-on-removal / manifest-integrity / catalog-integrity)** — live Phase-2 residuals
  bound at 2.3 (builder-lifecycle); 2.1 is initial-resolution correctness (t0). Do not attempt; do not
  regress. (Note: §2.4.1's DATA-load validation is NOT R-2 — R-2 is *builder-supplied manifest*
  integrity at lifecycle; §2.4.1 is *core's own DATA asset* integrity at load. Different surface,
  different layer; §2.4.1 does not reach into R-2's scope.)
- **The permanent HOME relocation itself** — §4 defers the decision; the actual `git mv` to a ratified
  standalone home (if chosen) is a later additive arc, not this build.

---

## 7. Residual questions for ARGUS

(rev1 RQ-1/RQ-2/RQ-3/RQ-4 were all DISCHARGED by ARGUS's verdict — TOML+3.11 SOUND, `.yaml`→`.toml`
faithful, `document-data.toml` separate-file faithful, `__main__.py`-vs-`run.py` genuinely ADA's call.
No new residual questions in rev2: the two folded fixes (r1 refactor shape pinned in §2.1.1, r2
fail-closed contract + P11 in §2.4.1/§3) are design DECISIONS, not open questions. The only thing for a
re-read to confirm is that the §2.1.1 import-time-global contract and the §2.4.1 invariant set are
concrete enough for ADA — I assess they are, and name the residual thin spot in WP-4'.)

---

## 8. Self-assessed weak points (where this design is thinnest — ARGUS cold-audits next)

- **WP-1 (the YAML→TOML interpretation is the load-bearing judgment call).** The directive's
  §3.1/§3.2/§17.1 literally say `.yaml`. I am reading "names `baseline.yaml`" as descriptive-of-the-
  asset, not prescriptive-of-the-serialization, on the strength of the directive's *own* explicit
  parser-decision mandate (load-bearing req #1) and the §2.3 zero-dependency intent. If ratification
  reads the directive as mandating literal YAML bytes, the design's format pivots (JSON or vendored-YAML,
  both named in §2.2). *Why this shape anyway:* §2.3 purity ("pure software that reads no environment")
  is the harder constraint and TOML+stdlib satisfies it with zero asterisk; a pinned PyYAML would make
  the purity claim false on a fresh machine. (ARGUS ruled this read SOUND — residual is now only
  ratification's literal-`.yaml` preference, named in RQ-2/§2.2 pivots.)
- **WP-2 (the permanent-HOME recommendation is a DEFER, which a ratifier may read as ducking the §3
  decision).** Directive §3 asks for a proposal with a recommendation; I recommend *deferring the
  permanent choice* while building in-place. *Why this shape anyway:* committing to B now stands up a
  home for a consumer that doesn't exist; committing to A permanently couples builder tooling to
  substrate-deploy. Deferring with a decision-neutral `agents/` *location* + B as the *leading future
  candidate* is the honest call given IA-1 makes relocation additive. (ARGUS ruled the defer LEGITIMATE;
  the r4 decision-neutral framing is now carried explicitly in §4.)
- **WP-3 (fixtures-as-DATA doubles the locked surface).** Moving the §8 expected sets out of Python
  literals into `tests/fixtures/expected/*.toml` means the locked regression target is now ALSO a DATA
  file that could itself drift from the §8 prose. *Why this shape anyway:* it makes the locked target
  auditable (VERA diffs it against §8 directly) and the §8.4/NEG behaviors stay as code assertions; the
  drift risk is mitigated because the *same* TOML loader round-trips both the input manifests and the
  expected sets, and P1/P3 assert against the design's §8 counts (8/6/7) which are independently stated
  in the directive DoD #1. **rev2 partially closes the worst case ARGUS raised under WP-3:** a bad edit
  touching BOTH `data/baseline.toml` and `tests/fixtures/expected/` would keep the resolution suite
  green against a wrong target — but §2.4.1's baseline set-equality (against the in-`dataload` named
  `EXPECTED_BASELINE` SSoT, NOT a fixtures file) now fails the LOAD before the suite runs, so the
  doubled-surface drift can no longer hide a shrunk baseline. A cheaper alternative (keep expected sets
  as Python literals in the test) remains available if ARGUS judges the data-fication of the *target* a
  net loss.
- **WP-4' (the r1 import-time-global pattern adds a load-order surface, now contract-pinned — replaces
  rev1 WP-4).** rev1's WP-4 worried the data-injection refactor touches frozen logic files; rev2 §2.1.1
  pins the shape (import-time module-global population, no signature change to the two frozen functions)
  and the §2.1.1 load-order/fail-closed contract (single population site in `resolution/__init__.py`;
  `_UNLOADED` sentinel that raises on a pre-load read; no mutation after load). The residual thin spot:
  the import-time pattern is correct *as long as the population call in `resolution/__init__.py` is the
  single writer and runs before any kind-table read* — a future refactor that imported `resolve.py`'s
  members by a path bypassing `__init__.py` would hit the `_UNLOADED` sentinel and FAIL-CLOSED (raise),
  which is the designed-for safe failure, but it IS a non-obvious coupling between the sub-package
  `__init__` and the frozen function bodies. *Why this shape anyway:* the alternative (threading the
  kind-tables through `derive_sa_scope`/`check_runtime_completeness` signatures) edits two proven
  signatures + every call site — a wider diff to frozen surface and a new way to pass the wrong table.
  Import-time globals keep the function bodies byte-unchanged; the sentinel makes the load-order risk
  fail-CLOSED, not silent. The coupling is concentrated in one `__init__.py` line and probe-covered
  (P6 grep confirms no literal kind-table; P11 `kinds-empty-scope-bearing` confirms a bad kinds.toml
  fails the load).
- **WP-5 (the §2-constraint probe checks the negative weakly).** P8 greps `def resolve` under
  `discovery/` for zero hits — but a determined re-implementation could alias the name or inline the
  algorithm without a `def resolve`. *Why this shape anyway:* the stronger half of P8 (V4's resolve
  callable resolves to the resolution module's `__file__`) is the real guard; the grep is a cheap
  belt-and-suspenders. (ARGUS concurred: module-identity assertion is the load-bearing guard.)
- **WP-6' (DATA-load fail-closed now CONTRACTED + probed; residual is invariant-COMPLETENESS — replaces
  rev1 WP-6).** rev1's WP-6 named DATA-file integrity as the likeliest missed-defect home but authored
  no probe; ARGUS r2 confirmed the gap. rev2 §2.4.1 specifies a fail-closed `DataIntegrityError`
  contract and P11 proves the loader REJECTS each corrupt tree. The residual thin spot: P11 proves
  rejection for the *enumerated* corrupt cases (baseline-missing/extra, empty scope_bearing, malformed
  category entry, missing catalog key, dangling reference) — it does NOT prove the invariant set is
  *exhaustive*. A malformed DATA shape I did not enumerate (e.g. a TOML type-confusion the loader
  coerces silently, or a duplicate category-stem across two files) could still slip through if §2.4.1's
  invariant list missed it. *Why this shape anyway:* the enumerated invariants cover the r2-worked
  attack-path (baseline shrink) directly and the structurally-adjacent fail-OPEN twins (empty
  scope_bearing, malformed entries, dangling refs); set-equality against named SSoTs (not length checks)
  is deliberately the strongest cheap form. Invariant-COMPLETENESS is the honest residual — exactly the
  kind of thing a cold audit should pressure-test — so I name it as the most likely place a missed gap
  in rev2 would live, and flag that if ARGUS surfaces an un-enumerated corrupt shape, it folds into
  §2.4.1's invariant list + a new P11 case (cheap, additive).
