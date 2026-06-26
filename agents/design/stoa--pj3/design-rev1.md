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
status: DESIGN — rev1 for ARGUS cold-audit
as_of: 2026-06-26
---

# stoa--pj3 build design (rev1): promote the resolution + discovery prototypes into the real builder-deploy CORE

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
external files read once at load time by a single thin `dataload` module. The §8 / §23 / §8.4 fixtures
become a `pytest`-style regression suite under `tests/` that VERA re-runs, structurally separate from
the existing `app/` JS suite so the two cannot interfere. The package is **runnable** (`python -m
builder_deploy_core.resolution` and `... .discovery` reproduce the prototype RESULTS) and **pure**
(reads no environment beyond its own `data/` tree).

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
│   ├── errors.py                     # ResolutionError, BaselineOmitError, UncatalogedServiceError, ValidationError
│   ├── dataload.py                   # THE ONE filesystem boundary (§2.3 audit point). loads data/ -> in-memory dicts
│   ├── resolution/
│   │   ├── __init__.py
│   │   └── resolve.py                # §2.5 resolve() + resolve_with_lint() + derive_sa_scope (§5.A)
│   │   │                             #   + check_runtime_completeness (§3.4). VERBATIM from the proven prototype,
│   │   │                             #   minus the inlined BASELINE/LIBRARY/KIND tables (now injected from dataload).
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
    │   └── expected/                 #   the 8/6/7 expected resolved sets (the LOCKED regression target)
    ├── test_resolution.py           # §8.1/8.2/8.3 exact-set + §8.4 BaselineOmitError(all 5) + §3.4 + §5.A + §3.3
    └── test_discovery.py            # §23.1 generate→resolve→8/6/7 + equivalence + V1–V5 + NEG-1 + NEG-2 + §2-constraint
```

**What moves vs what is frozen:** the *logic* of `resolve.py`, `generate.py`, `validate.py` is the
proven prototype code transcribed UNCHANGED (the directive: "harden + package + externalize", not
re-derive). The ONLY edits to logic files are: (a) the four data tables (`BASELINE`, `LIBRARY`,
`KIND_ENUM`/`SCOPE_BEARING_KINDS`/`KEY_BEARING_PAIRING`, `CATALOG`/`CATEGORIES`) stop being
module-level literals and become arguments injected by `dataload` (the functions already take
`baseline`/`library` as parameters — the prototype defaulted them to the inlined literals; we remove
the literal defaults and require the caller to pass the loaded data); (b) the `sys.path` hack in the
discovery prototype's `run.py` becomes a real intra-package import (§2.3).

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
  `.md`). I flag this as the cheapest pivot.
- **Vendor a minimal YAML loader** — keeps the literal `.yaml` extension but ships hand-rolled parser
  code we'd own and test. Rejected: more code + more risk than using a stdlib parser for a format
  that expresses the same data.

**Directive-fidelity note (IA-3):** the directive names `baseline.yaml` + `categories/<name>.yaml`
descriptively. I preserve the **logical assets, the layout, and the filename stems** (`baseline`,
`categories/<name>`, `catalog/<service-id>`) and change only the *extension/serialization* to `.toml`
per the parser decision the directive itself asked me to make. This is a self-assessed
interpretation (§9 WP-1); if ratification wants the literal `.yaml` bytes, the JSON/PyYAML fallbacks
above are the two named pivots.

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
exact design category strings.)

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
                        (the ONE fs boundary; loads data/ -> dicts)
                              │ (provides BASELINE, LIBRARY, KINDS, CATALOG, CATEGORIES)
              ┌───────────────┴───────────────┐
              ▼                                ▼
   resolution/resolve.py            discovery/generate.py
   (resolve, resolve_with_lint,     (G1–G4; reads BASELINE for G3,
    derive_sa_scope §5.A,            catalog+categories for G1/G2)
    check_runtime_completeness §3.4)
              ▲                                │
              │  IMPORTS (the §2-constraint)   │ produces {category, delta}
              │                                ▼
              └──────────────────  discovery/validate.py
                                   (V1–V5; V4 calls resolution.resolve +
                                    resolution.check_runtime_completeness +
                                    catches errors.BaselineOmitError — REUSED, never reimplemented)

errors.py  ← imported by all three (single home for the 4 exception classes)
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

### 2.5 Runnability

`python -m builder_deploy_core.resolution` and `python -m builder_deploy_core.discovery` reproduce the
two prototype RESULTS.md runs (the `run.py` harness logic moves into `__main__.py` of each sub-package
OR stays as thin `run.py` shims — ADA's call; the design requires only that both are runnable and
print the same PASS lines the prototypes did). The authoritative pass/fail is the `tests/` suite (§2.6).

### 2.6 The locked regression suite (DoD #1/#2/#3/#4)

The §8 + §23 + §8.4-negative fixtures become the skill's **locked acceptance/regression suite**.
Structure decision: **fixtures-as-DATA, runner-as-code.** The manifests and their expected resolved
sets live under `tests/fixtures/` as TOML (manifests) + TOML (expected `(kind,name)` lists), mirroring
the byte-for-byte §8 enumerations. `test_resolution.py` / `test_discovery.py` are thin `pytest`
runners that load the fixtures and assert. WHY fixtures-as-data: the directive locks the §8 *sets*
(8/6/7 byte-for-byte) as the regression target — keeping them as DATA, not buried in Python literals,
makes the locked target auditable and lets VERA diff the expected set against the design's §8 prose
directly. The runner stays code because the *assertions* (exact-set match, raises-BaselineOmitError,
runtime-completeness holds, SA-scope == scope-bearing subset, V1–V5, NEG-1/NEG-2, §2-constraint) are
behavior, not data.

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

### 2.7 Threat→mitigation map (§6.12)

`not threat-ratified (process/tooling change, no runtime attack path)`. This arc promotes pure,
offline, environment-free software (resolution + discovery logic + DATA files) with an explicit §2.3
no-environment / no-network / no-credential boundary; it provisions nothing and is reachable by no
external actor. There is no named threat in the directive, the design-formal sections in scope, or the
prototype RESULTS for 2.1; the live Phase-2 residuals R-1/R-2/R-3 are explicitly deferred to 2.3
(directive §4) and do not bind at t0. Per §35.5 this is the carved-out class (no runtime attack path);
I PROPOSE the `not threat-ratified` classification — ARGUS CONFIRMS it (I cannot self-grant the
carve-out). Accordingly §3 carries no threat-anchored probe (§6.13): the fail-closed probes below
(§8.4 BaselineOmitError, NEG-1/NEG-2) verify the design's *correctness* invariants, not a threat-
defeat.

---

## 3. Verification probes (what would falsify this design)

Each is a concrete command/behavior VERA re-runs. Destructive ops avoided (read-only).

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

**P6 — DATA externalized (DoD #5).** Mutate a copy of `data/baseline.toml` (e.g. add a 6th entry in a
tmp data root) and show the resolved baseline set changes accordingly — proving the resolver READS the
file rather than a hardcoded literal. Also: grep the logic modules (`resolve.py`, `generate.py`,
`validate.py`) for inlined `BASELINE = [` / `LIBRARY = {` / `CATALOG = {` literals → ZERO hits (the
tables now live in `data/`, loaded by `dataload`). Falsifier: a logic module still carrying a data
literal, or the resolver ignoring a changed DATA file.

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
probe confirms the change breaks nothing. (VERA runs the FULL suite IN ADDITION to P1–P8 — bespoke
probes prove the new core works; the full suite catches what it breaks elsewhere.)

**P10 — authorship (DoD #8).** `grep -rn -E "author|owner|creator|maintainer|copyright|by:" agents/builder-deploy-core/`
→ every author-like field reads `Denson Smith`; ZERO foreign name. Falsifier: any foreign author field.

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

**Build 2.1 in the-stoa now (Option A's location), and DEFER the permanent-HOME choice to the point
where a real consumer exists — i.e. when 2.3 (provisioning choreography) or the first real builder
workspace forces the question.** Rationale: (1) the directive already mandates the arc-75/the-stoa
build location and says relocation is additive (IA-1), so building here costs nothing toward a later
move; (2) the package layout in §2.1 is **HOME-independent by construction** — a self-contained Python
package with its own `data/` + `tests/`, relocatable as one unit, so the relocation cost is a `git mv`
+ updated install/consume path, not a redesign; (3) deciding B now optimizes for a consumer set
(builder workspaces) that does not yet exist — premature. **My recommendation is therefore "Option A
location for 2.1, permanent HOME = explicitly DEFERRED, revisited at 2.3 with the standalone-package
(Option B) as the leading candidate once a consumer exists."** Polybius_the_Stoa ratifies; escalate to
Grand if the deferral itself is judged load-bearing.

---

## 5. DoD-#-to-design-element traceability (directive §5, items 1–9)

| DoD # | Requirement | Where this design satisfies it |
|---|---|---|
| **1** | Resolver reproduces §8 (8/6/7 byte-for-byte); §8.4 raises `BaselineOmitError`, no set; guard fires for all 5 baseline entries | §2.1 `resolution/resolve.py` (frozen §2.5 logic) + §2.6 locked suite `test_resolution` (parametrized over all 5) + probes **P1, P2** |
| **2** | Generator: declared `services:` → `{category,delta}` the UNCHANGED resolver resolves to 8/6/7, equivalent to §8 (alias-aware) | §2.1 `discovery/generate.py` (frozen §19 G1–G4) + §2.3 dependency edge + §2.6 `test_discovery` + probe **P3** |
| **3** | V1–V5 pass; NEG-1 (V5 fail-closed) + NEG-2 (`UncatalogedServiceError` + V1 fail) hold | §2.1 `discovery/validate.py` (frozen §20 V1–V5) + §2.6 `test_discovery` + probe **P4** |
| **4** | Resolved-set properties: SA-scope §5.A, runtime-completeness §3.4, kind-dispatch §3.3 | §2.1 `resolve.py` (`derive_sa_scope`, `check_runtime_completeness`) + §2.6 + probe **P5** |
| **5** | DATA externalized: baseline / category templates / catalog are real DATA files (not hardcoded), read as data | §2.1 `data/` tree + §2.2 TOML schemas + parser decision + §2.1 "what moves" (literals → injected) + probe **P6** |
| **6** | Purity (reads no environment beyond own DATA); §2-constraint (discovery imports resolver, never re-implements) | §2.3 dependency graph + §2.4 purity boundary (single `dataload`) + probes **P7, P8** |
| **7** | Full existing the-stoa suite GREEN (gen-data + app build) in addition to bespoke fixtures | §2.1 layout (core lives under `agents/`, outside `app/`; gen-data reads `substrate/`) + probe **P9** (VERA runs full suite + P1–P8) |
| **8** | `author: Denson Smith` on every artifact; ZERO foreign author field | Frontmatter of this doc + every artifact in §2.1 carries `author: Denson Smith` (prototype files already do) + probe **P10** |
| **9** | Home proposal surfaced for ratification, not silently chosen | §4 (Options A/B + tradeoffs + recommendation + IA-1 build-location vs permanent-HOME split); flagged for Polybius_the_Stoa via PLINY→FM |

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
  regress.
- **The permanent HOME relocation itself** — §4 defers the decision; the actual `git mv` to a ratified
  standalone home (if chosen) is a later additive arc, not this build.

---

## 7. Residual questions for ARGUS

- **RQ-1 (format pivot):** is the `requires-python = ">=3.11"` floor (for stdlib `tomllib`) acceptable
  for the eventual HOME's consumer base, or should the JSON fallback (§2.2) be the primary to keep the
  zero-dependency property without a 3.11 floor? I recommend TOML+3.11; flag if the consumer floor is
  unknown enough to prefer JSON.
- **RQ-2 (filename fidelity):** is changing the DATA extension from the directive's literal `.yaml`
  (§3.1/§3.2/§17.1) to `.toml` within the architect's explicit parser mandate (load-bearing req #1) a
  faithful read of the directive, or does it need the literal `.yaml` bytes (→ pivot to vendored-YAML)?
- **RQ-3 (alias filename):** the `document/data` category name contains `/` (not a portable filename
  char). My loader holds a stem↔name map (`document-data.toml` ↔ `document/data`). Is the indirection
  acceptable, or should the alias be represented inside `document-consuming.toml` as an explicit
  alias key rather than a separate file?
- **RQ-4 (runnable entrypoint):** I left `__main__.py`-vs-`run.py` to ADA. Flag if you want the design
  to pin one.

---

## 8. Self-assessed weak points (where this design is thinnest — ARGUS cold-audits next)

- **WP-1 (the YAML→TOML interpretation is the load-bearing judgment call).** The directive's
  §3.1/§3.2/§17.1 literally say `.yaml`. I am reading "names `baseline.yaml`" as descriptive-of-the-
  asset, not prescriptive-of-the-serialization, on the strength of the directive's *own* explicit
  parser-decision mandate (load-bearing req #1) and the §2.3 zero-dependency intent. If ARGUS reads the
  directive as mandating literal YAML bytes, the design's format pivots (JSON or vendored-YAML, both
  named in §2.2). *Why this shape anyway:* §2.3 purity ("pure software that reads no environment") is
  the harder constraint and TOML+stdlib satisfies it with zero asterisk; a pinned PyYAML would make the
  purity claim false on a fresh machine. I'd rather be right on purity and flag the format than honor
  the literal extension and ship a hidden dependency.
- **WP-2 (the permanent-HOME recommendation is a DEFER, which a ratifier may read as ducking the §3
  decision).** Directive §3 asks for a proposal with a recommendation; I recommend *deferring the
  permanent choice* while building in-place. That is a legitimate recommendation (build cost is zero
  either way, consumer set doesn't exist yet) but it is one step removed from "pick A or B." *Why this
  shape anyway:* committing to B now stands up a home for a consumer that doesn't exist; committing to A
  permanently couples builder tooling to substrate-deploy. Deferring with A's *location* + B as the
  *leading future candidate* is the honest call given IA-1 makes relocation additive.
- **WP-3 (fixtures-as-DATA doubles the locked surface).** Moving the §8 expected sets out of Python
  literals into `tests/fixtures/expected/*.toml` means the locked regression target is now ALSO a DATA
  file that could itself drift from the §8 prose. *Why this shape anyway:* it makes the locked target
  auditable (VERA diffs it against §8 directly) and the §8.4/NEG behaviors stay as code assertions; the
  drift risk is mitigated because the *same* TOML loader round-trips both the input manifests and the
  expected sets, and P1/P3 assert against the design's §8 counts (8/6/7) which are independently stated
  in the directive DoD #1. A cheaper alternative (keep expected sets as Python literals in the test) is
  available if ARGUS judges the data-fication of the *target* a net loss.
- **WP-4 (the data-injection refactor touches frozen logic files).** "Freeze the logic" and "remove the
  inlined BASELINE/LIBRARY/CATALOG defaults" are in mild tension — I am editing the logic files (to
  drop literal defaults and require injected data) while claiming the *logic* is unchanged. The edit is
  mechanical (delete the literal, the functions already accept the data as params) but it IS a diff to a
  proven file. *Why this shape anyway:* externalization (DoD #5) is impossible without it, and the
  parameter seam already exists in the prototype (resolve takes `baseline`/`library` args today). VERA's
  P1–P5 re-run the proven behaviors against the externalized data, which is the guard: if the refactor
  changed behavior, the 8/6/7 sets would move. The risk is concentrated and probe-covered, not diffuse.
- **WP-5 (the §2-constraint probe checks the negative weakly).** P8 greps `def resolve` under
  `discovery/` for zero hits — but a determined re-implementation could alias the name or inline the
  algorithm without a `def resolve`. *Why this shape anyway:* the stronger half of P8 (V4's resolve
  callable resolves to the resolution module's `__file__`) is the real guard; the grep is a cheap
  belt-and-suspenders. I flag that the grep alone is not sufficient and the module-identity assertion is
  the load-bearing one.
- **WP-6 (no threat-anchored probe, by §35.5 carve-out).** I classify 2.1 as `not threat-ratified`
  (§2.7) and therefore author no threat-anchored probe. If ARGUS surfaces a named threat I did not see
  (e.g. a DATA-file-tampering surface now that the tables are external + file-loaded), the §35.5
  carve-out would not apply and a threat-anchored probe (e.g. malformed/hostile `data/*.toml` →
  fail-closed, not silent mis-resolution) would be owed. *Why this shape anyway:* 2.1 reads only its
  own bundled, version-controlled DATA (no external/attacker-supplied input, no network, no creds), so
  I assess no runtime attack path at t0 — but DATA-file integrity (R-2-adjacent) is exactly the kind of
  thing a cold audit should pressure-test, so I name it as the most likely place a threat I missed
  would live.
