<!-- author: Denson Smith -->
<!-- ticket: stoa--pj3 (u--9s2 Phase-2 increment 2.1) -->

# builder-deploy-core

The builder-deploy **resolution + discovery CORE** (u--9s2 Phase-2 increment 2.1) — the front-end of
the cookie-cutter that turns a builder's declared `services:` list into a validated `{category, delta}`
manifest and resolves it to its exact typed credential set.

This is the **promotion** of two VERIFIED Phase-1 prototypes (`stoa--jw5` resolution-check 19/19 +
discovery-check) into a real, runnable, packaged Python package with **externalized DATA** and a
**locked regression suite**. The algorithms are frozen as proven; the promotion is structure,
packaging, DATA externalization, and fail-closed load validation — NOT a re-architecture.

## What it is — and what it is NOT

- **Pure software.** Provisions NOTHING. Reads no environment beyond its own `data/` tree — no
  `gcloud`, no Railway, no credentials, no network, no clock, no `os.environ`, no `subprocess`. The
  single permitted filesystem touch is `dataload.py` reading files under `data/` (resolved relative to
  `__file__`, never from an env var or CWD).
- **Zero runtime third-party dependencies.** `requires-python = ">=3.11"`; the core imports
  stdlib-only (`tomllib` is stdlib since 3.11). The test extra adds `pytest`; the core never imports it.
- **NOT a deployer.** The `kind` recipes are named in DATA but never executed. This increment emits and
  validates; it does not apply. The provisioning choreography and any real deploy are out of scope
  (deferred to later increments).

## Layout

```
builder-deploy-core/
├── builder_deploy_core/
│   ├── errors.py        # the 5 exception classes (incl. DataIntegrityError)
│   ├── dataload.py      # THE single filesystem boundary; loads + VALIDATES data/ fail-closed
│   ├── resolution/      # the §2 resolver — the single source of truth
│   │   ├── __init__.py  #   single import-time kind-table population site (§2.1.1)
│   │   ├── resolve.py   #   resolve / resolve_with_lint / derive_sa_scope / check_runtime_completeness
│   │   └── __main__.py  #   `python -m builder_deploy_core.resolution`
│   └── discovery/       # catalog (DATA) + generate (§19) + validate (§20)
│       ├── generate.py
│       ├── validate.py  #   V4 IMPORTS the resolver — never re-implements it (the §2-constraint)
│       └── __main__.py  #   `python -m builder_deploy_core.discovery`
├── data/                # the externalized DATA tables (TOML)
│   ├── baseline.toml    #   the 5 non-omittable baseline entries
│   ├── kinds.toml       #   kind enum + scope-bearing set + key-bearing pairing
│   ├── categories/      #   category templates (geospatial, document-consuming, document-data)
│   └── catalog/         #   service seed records
├── tests/               # the locked regression suite (fixtures-as-DATA, runner-as-code)
└── pyproject.toml
```

## How to run

Reproduce the prototype RESULTS (from this directory):

```sh
python -m builder_deploy_core.resolution   # §8.1/8.2/8.3 -> 8/6/7 + §8.4 BaselineOmitError + §3.4 + §5.A
python -m builder_deploy_core.discovery    # generate -> resolve 8/6/7 + V1-V5 + NEG-1/NEG-2 + §2-constraint
```

Run the locked regression suite (the authoritative pass/fail):

```sh
python -m pytest tests/ -q
```

## The §2-constraint

Discovery's `validate.py` V4 **imports** the single resolver
(`from builder_deploy_core.resolution.resolve import resolve, check_runtime_completeness`) and the
guard (`from builder_deploy_core.errors import BaselineOmitError`). There is **no** copy of the
resolution algorithm anywhere under `discovery/`. The dependency is acyclic and one-directional:
`discovery → resolution`, never the reverse.

## Fail-closed DATA-load validation

`dataload` validates every DATA body on load and raises `DataIntegrityError` (no partial load) on any
invariant violation — baseline set-equality against an in-`dataload` `EXPECTED_BASELINE` SSoT, kinds
enum/scope-bearing/pairing well-typedness, category + catalog well-typedness, and a cross-body
dangling-reference check. A structurally-degraded DATA file (e.g. a `baseline.toml` missing `pgvector`)
fails the LOAD, before the resolver can silently shrink the baseline.

Authored by Denson Smith. MIT-licensed.
