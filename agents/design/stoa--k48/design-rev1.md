---
author: Denson Smith
ticket: stoa--k48 (u--9s2 Phase-2 increment 2.3 — provisioning choreography, ONE pass: design folded into the build)
seat: CAPTAIN_DAEDALUS_the_stoa
formalizes: agents/design/stoa--k48/chiron-ownership-tier-design.md (ownership/tier + §7 SHAPE/CONTENT + emit-then-apply + HOME + jd5)
          + agents/design/stoa--k48/provisioning-choreography-hamilton.md (S0–S6 mechanics + mock substrate + 3-wall TRIPWIRE + deploy-help)
ground-truth-held-unchanged: agents/design/stoa--jw5/design-formal.md §4 (S0–S6) / §5.A/§5.B (isolation) / §6 (db-extension) / §7 (SHAPE/CONTENT) / §8 (worked examples) / §12 (M1–M6 + R-1/R-2/R-3)
builds-on: agents/builder-deploy-core/ (2.1 resolution + 2.2 suggest) — resolve()/derive_sa_scope()/check_runtime_completeness() REUSED BYTE-UNCHANGED (FROZEN SURFACE)
status: FORMAL — single buildable spec for ADA; gauntlet-facing (ARGUS next)
as_of: 2026-06-27
---

# u--9s2 Phase-2 inc 2.3 — FORMAL SPEC: the provisioning choreography (pure emitter + port-driven engine + mock substrate)

This formalizes the TWO reconciled co-design halves into ONE buildable artifact. It does NOT redesign
design-formal §4–§7 or §12 — it makes the Phase-2 build arc's mechanics concrete enough that ADA can
build verbatim and VERA can probe machine-checkably. **It provisions NOTHING real.** The mock substrate
makes a real `gcloud`/`railway`/card call STRUCTURALLY impossible on the test path (the 3-wall TRIPWIRE,
§5). Every fixed point both architects converged on is preserved (§0.2).

---

## 1. Problem restatement (pre-work gate, §6.1)

Build the **provisioning choreography** for the builder-deploy cookie-cutter: given a resolved set
(produced by the 2.1 resolver from a 2.2-suggested, human-confirmed manifest), **emit a value-free
provisioning spec** (slot NAMES only, never values) and **walk the S0–S6 steps** against an **injected
`Provisioner` port** whose ONLY concrete implementation is a zero-I/O `MockProvisioner`. The choreography
provisions a **domain-EMPTY** builder (100% T1 cookie-cutter mechanism; zero T3 product). The real
applier (CI-via-WIF or human keyring one-shot) lives **outside the package forever** — agents never run a
credential-bearing apply. This pass also folds the **stoa--jd5 packaging fix** (move `data/` inside the
importable package). The deliverable is the package code + tests + the three relay-up generators.

**Imported assumptions** (named per §6.1 — explicit scope, not invention):
1. *The resolved set is the choreography's input, unchanged.* `emit_spec` consumes exactly what
   `resolve()` returns (a sorted list of `(kind, name)` tuples). 2.3 adds NO new entry kind and does NOT
   touch `resolve()` / `derive_sa_scope()` / `check_runtime_completeness()` (FROZEN SURFACE — §0.3).
2. *The §8 worked examples (prospector 8 / scienceclaw 6 / labstat_bls 7) are a REGRESSION TARGET, not
   re-derived.* `emit_spec(resolve(M))` over each drives a golden-file fixture.
3. *"Exercised against mock dashboards only" means the deploy-help library is DESIGNED + the per-slot
   PLAN is emitted; no browser opens, no key mints, no keyring writes in 2.3* (§9). The real drive is 2.4.
4. *HOME is HOME-agnostic for this build.* The package stays at the decision-neutral
   `agents/builder-deploy-core` location; the ratified Option-A relocation to
   `substrate/skills/builder-deploy/` is an additive `git mv` at close/2.4 (§0.4) — ADA is NOT blocked on it.

**Restatement-vs-brief:** converges. The one place the brief left me to decide is whether the deploy-help
**library code** ships in 2.3 or only its emitted plan-text; I formalize it as plan-text-only in 2.3 (§9,
HW-2-adjacent), matching the TRIPWIRE ("2.3 emits the PLAN text per slot, not the action"). Flagged for
ARGUS (§13 RQ-3).

---

## 0. Fixed points, frozen surface, HOME (carried forward, do not relitigate)

### 0.1 The one architectural decision (HAMILTON §0, CHIRON §3 — IDENTICAL conclusion)
A **pure EMITTER** + a **port-driven ENGINE**; the real applier lives **outside the package, forever**.
`emit_spec` is pure (no I/O, same property as `resolve()`), value-free (slot NAMES only).
`Choreographer(provisioner).run(...)` walks S0–S6 dispatching each step's actions to the INJECTED port.
The ONLY concrete port shipped is `MockProvisioner`. **No in-agent `RealProvisioner`, ever.**

### 0.2 The converged fixed points (both architects; preserved verbatim here)
1. **2.3 builds 100% T1; zero T3** (CHIRON §0/§1) — the choreography is generic; the product (domain
   verbs + curated data) is NOT built here.
2. **S0–S6 deterministic CODE, no LLM in the loop** (HAMILTON §0) — the only model is the upstream 2.2
   SUGGEST. S0–S6 = "one `kind` = one complete deterministic recipe."
3. **The S5/§7 boundary is `grep`-mechanical** (CHIRON §2; the STRICT canonical version, §8.5 below).
4. **The emit/apply seam** = value-free emit (grep-provable) + credential-disciplined applier + S2c
   BLOCK + emit-only mock path = the structural TRIPWIRE.
5. **value-free 2-mode mock** (HAMILTON §3.1): default → S2c BLOCKS; `populated=<slot-name set>` → S3–S6
   run. `populated` is a `set[str]` of slot NAMES — a value-free boolean membership marker, never a value.
6. **Per-builder isolation** (design-formal §5.A): bijective SA from slug; per-secret `secretAccessor`;
   SA scope = `derive_sa_scope(resolved)` (the mechanical union); never project-wide.
7. **HW-1..HW-4** (HAMILTON §7) carried into §12; HW-4 RESOLVED by the jd5 fold (§11).

### 0.3 FROZEN SURFACE (REUSED byte-unchanged — ADA must NOT edit)
- `builder_deploy_core/resolution/resolve.py` — `resolve` (L69), `resolve_with_lint` (L106),
  `derive_sa_scope` (L147), `check_runtime_completeness` (L162). BYTE-UNCHANGED.
- `builder_deploy_core/resolution/__init__.py` (the import-time kind-table population seam) — UNCHANGED.
- `builder_deploy_core/suggest/*` (2.2) + `builder_deploy_core/discovery/*` (2.1) — UNCHANGED.
- `dataload.py` load functions (`load_baseline`/`load_kinds`/`load_library`/`load_catalog`/
  `load_detection_hints`) — their BODIES are byte-unchanged; the ONLY edit is `_DATA_ROOT`'s one path
  expression (§11 jd5 — `.parent.parent` → `.parent`), which is the data-relocation, not a logic change.
- The 2.1/2.2 test suite — UNCHANGED except the two `test_dataload.py` data-path lines the jd5 move
  forces (§11 step 5). VERA runs the FULL suite (DoD#9).

A build commit that edits any frozen-surface function body beyond §11's named lines is a regression CATO/
NOMOS flag; ADA verifies with `git diff` (strict-prefix / same-blob check) before commit.

### 0.4 HOME (RATIFIED, do not block)
RATIFIED = Option A-with-graduation-trigger (the-stoa forge-owned; canonical SOURCE
`substrate/skills/builder-deploy/`). The build is formalized against the DECISION-NEUTRAL
`agents/builder-deploy-core` location — HOME-agnostic. The A-home `git mv` is an additive close/2.4 step,
NOT this build. Where the spec needs the builder-deploy SKILL wrapper (SKILL.md + deploy-help placement),
it is formalized HOME-agnostic / relocatable-by-additive-`git mv`; the only load-bearing skill-wrapper
decision (does the deploy-help library code ship in 2.3) is FLAGGED for PLINY (§13 RQ-3), not baked.

---

## 2. Module structure (what ADA builds)

A new `provision/` sub-package under `builder_deploy_core`, reusing resolution/ + suggest/ + data/
unchanged:

```
builder_deploy_core/
  resolution/        # 2.1 — resolve(), derive_sa_scope(), check_runtime_completeness()  [FROZEN, byte-unchanged]
  suggest/           # 2.2 — examine→suggest→confirm→declare                              [FROZEN, byte-unchanged]
  discovery/         # 2.1 — generate/validate                                            [FROZEN, byte-unchanged]
  data/              # 2.1 — baseline.toml + kinds.toml + categories/ + catalog/   [MOVED INSIDE pkg by jd5, §11]
  provision/         # 2.3 — NEW
    __init__.py      #   re-export emit_spec, Choreographer, MockProvisioner, Provisioner, render_checklist,
                     #     assert_value_free, ProvisioningSpec, RunLedger, the StepAction dataclasses, StepStatus
    spec.py          #   emit_spec(resolved, builder_slug) -> ProvisioningSpec   (PURE, value-free)
                     #     + the ProvisioningSpec / SlotSpec dataclasses + assert_value_free()
    port.py          #   Provisioner ABC (the abstract port) + the StepAction dataclasses + StepStatus enum
    mock.py          #   MockProvisioner — the ONLY concrete port; in-memory ledger; zero I/O
    choreographer.py #   Choreographer(provisioner).run(resolved, slug) -> RunLedger  (walks S0–S6) + RunLedger
    steps.py         #   S0..S6 as pure step functions: (resolved, slug, spec, provisioner) -> [StepAction]
    checklist.py     #   render_checklist(spec) -> str  (relay-up #1) + the credential-discipline /
                     #     TRIPWIRE-held attestation derivations (relay-up #2/#3 text generators)
    __main__.py      #   `python -m builder_deploy_core.provision` — dry-run emit + mock walk repro surface
```

**Import-discipline (the TRIPWIRE's teeth, W1, §5):** every module under `provision/` imports ONLY
`builder_deploy_core.*` + stdlib `dataclasses` / `enum` / `typing` / `__future__`. It imports **none** of
`subprocess`, `os`, `os.system`, `socket`, `http`, `urllib`, `requests`, `httpx`, `asyncio`, `gcloud`,
`railway`. `mock.py` is pure (records actions into a list; no filesystem, no network). `__main__.py` may
import `sys` (for `sys.exit`) — the W1 grep list (§5) does NOT include `sys`, so this is permitted; the
AST test (§5 W1) whitelists `sys` for `__main__.py` only, exactly as the existing discovery/__main__.py
uses `sys`.

`provision/` does NOT itself read `data/` — it consumes the already-resolved set the caller passes. The
data-tree reachability concern is entirely the jd5 fold's (§11); `provision/` rides the fixed layout.

---

## 3. Dataclass schemas (the new surface — HW-3 mitigation: pinned, not free-form)

All in `port.py` + `spec.py`. Frozen dataclasses (`@dataclass(frozen=True)`) so the spec/ledger are
immutable + hashable + comparable for golden-file equality. **Every field is value-free by construction —
there is no field that can hold a credential value** (HW-1 / DoD#3).

### 3.1 `port.py` — StepStatus + the StepAction dataclasses

```python
class StepStatus(enum.Enum):
    OK       = "ok"        # action emitted/created (or create-or-get returned existing)
    BLOCKED  = "blocked"   # S2c — slot unpopulated; halts before S3/S5 (fail-closed, human gate)
    FAILED   = "failed"    # a provisioner action raised (fail_at) — aborts the remainder
    SKIPPED  = "skipped"   # idempotent re-run: create-or-get returned existing, no new create

@dataclass(frozen=True)
class StepAction:
    step: str                  # "S0".."S6"  (the step index — ledger monotonicity keys on this, §4)
    op: str                    # the port verb, e.g. "ensure_project" | "ensure_sa" | "enable_api" |
                               #   "ensure_secret_slot" | "grant_secret_accessor" | "require_population" |
                               #   "provision_db_service" | "provision_serving_service" | "set_railway_var" |
                               #   "apply_db_extension" | "select_base_image" | "stand_up_mesh_shape" | "verify_*"
    target: str                # the NAME the op acts on: a slug, an api id, a SLOT NAME, a var NAME,
                               #   an extension name, a service name. NEVER a value. (the grep surface)
    status: StepStatus
    detail: tuple[tuple[str, str], ...] = ()   # value-free structured detail as (key, name-ref) pairs ONLY:
                               #   e.g. (("source_slot","MAPS_API_KEY"),) for a railway var sourced from a slot;
                               #   (("sa","sa-prospector"),("secret","MAPS_API_KEY")) for a per-secret grant;
                               #   (("acquisition","mint-via-gcp-console"),) for an S2c plan.
                               #   assert_value_free walks every leaf; all are NAMES/refs, never values.
    created: bool = True       # False on an idempotent re-run create-or-get (§4 idempotency)
```

`detail` is a tuple-of-pairs (not a free dict) so it is frozen/hashable for golden-file equality AND so
`assert_value_free` has a closed leaf shape to walk. The CONVENTION (enforced by `assert_value_free` +
review): every `detail` value is a NAME or a slot-REF, never a credential value — there are no values in
the system to leak (the mock never holds one; emit is pure).

### 3.2 `spec.py` — SlotSpec + ProvisioningSpec

```python
@dataclass(frozen=True)
class SlotSpec:
    name: str                  # the secret-slot NAME (e.g. "MAPS_API_KEY", "POSTGRES_PASSWORD",
                               #   "BLS_OEWS_API_KEY", "TS_AUTHKEY"). NEVER a value.
    kind: str                  # "gcp_secret" | "thirdparty_rest_key" (the §3.3 secret-bearing kinds)
    acquisition: str           # the §9 deploy-help method, DERIVED (HW-2): "mint-via-gcp-console" |
                               #   "mint-via-thirdparty" | "generate-locally" | "mint-via-dashboard"
    populated: bool = False    # emit-time always False (a slot is unpopulated until the human/CI step).
                               #   This is a STATUS boolean, never a value.

@dataclass(frozen=True)
class ProvisioningSpec:
    builder_slug: str
    project: str               # the derived project NAME: f"proj-{slug}" (a name, not a credential)
    sa: str                    # the bijective SA NAME: f"sa-{slug}" (design-formal §5.A)
    apis: tuple[str, ...]      # sorted gcp_api names to enable (S1)
    secret_slots: tuple[SlotSpec, ...]   # sorted-by-name secret slots (S2) — gcp_secret + thirdparty_rest_key
    railway_vars: tuple[str, ...]        # sorted railway_var NAMES (S3) — incl. DATABASE_URL + secret-backed refs
    db_extensions: tuple[str, ...]       # sorted db_extension names (S4) — pgvector always; postgis iff resolved
    sa_scope: tuple[tuple[str, str], ...]# = derive_sa_scope(resolved) (FROZEN call) — the mechanical union
    needs_postgis_base_image: bool       # postgis ∈ resolved (the §6 DECIDE-C base-image select signal)
    budget_boundary_required: bool = True  # the §5.B prepaid-card requirement REPRESENTED (never a card number)
```

The spec is **byte-stable**: every collection is a sorted tuple. `emit_spec` is the SSoT of these names;
`render_checklist` + the attestations + the 2.4 applier all consume this one schema (HW-3).

### 3.3 `choreographer.py` — RunLedger

```python
@dataclass(frozen=True)
class RunLedger:
    builder_slug: str
    actions: tuple[StepAction, ...]      # every action emitted, in execution order (step-index monotonic)
    terminal: StepStatus                 # OK (S6 reached) | BLOCKED (S2c) | FAILED (fail_at)
    blocked_slots: tuple[str, ...] = ()  # slot NAMES reported BLOCKED-on-human at S2c (value-free)
```

---

## 4. Function signatures + behavior (the buildable contracts)

### 4.1 `spec.py::emit_spec` — PURE, value-free (W3)

```python
def emit_spec(resolved, builder_slug):
    """PURE transform: resolved set -> ProvisioningSpec. No provisioner, no I/O (W3).
    resolved: the sorted [(kind, name)] from resolve() (FROZEN).
    builder_slug: the builder slug (^[a-z][a-z0-9_]*$, matching the manifest `builder` pattern).
    Returns a ProvisioningSpec (§3.2). Same input -> byte-identical spec (sorted tuples)."""
```
Behavior (all derivations are pure functions of `resolved` + `builder_slug`):
- `project = f"proj-{slug}"`, `sa = f"sa-{slug}"` (bijective, §5.A).
- `apis` = sorted names where `kind == "gcp_api"`.
- `secret_slots` = sorted-by-name `SlotSpec(name, kind, acquisition=_derive_acquisition(kind, name))`
  for each entry where `kind ∈ {"gcp_secret", "thirdparty_rest_key"}`, `populated=False`.
- `railway_vars` = sorted names where `kind == "railway_var"` (DATABASE_URL always; plus any resolved
  railway_var). Secret-backed vars are S3 actions that reference a `source_slot`, NOT new railway_var
  entries — the §8 sets carry only DATABASE_URL as a railway_var.
- `db_extensions` = sorted names where `kind == "db_extension"`.
- `sa_scope = tuple(derive_sa_scope(resolved))` — the FROZEN call; ADA must call the real function, not
  re-derive the union (a re-derive is a CATO drift flag).
- `needs_postgis_base_image = ("db_extension", "postgis") in set(resolved)`.

`_derive_acquisition(kind, name)` (HW-2 — derive default from kind, optional catalog override; do NOT add
a REQUIRED catalog field that breaks the §8 fixtures):

```
thirdparty_rest_key                      -> "mint-via-thirdparty"
gcp_secret, name == "POSTGRES_PASSWORD"  -> "generate-locally"
gcp_secret, name == "TS_AUTHKEY"         -> "mint-via-dashboard"   # (if ever resolved as gcp_secret)
gcp_secret  (any other, key-bearing)     -> "mint-via-gcp-console" # MAPS_API_KEY
```
The mapping is a pure function of `(kind, name)`. An OPTIONAL catalog `acquisition` override may be
threaded in a Phase-2 follow-up; 2.3 derives it (no catalog schema change — §8 fixtures untouched). This
is the HW-2 resolution: derivation-by-default, never a new required field.

### 4.2 `spec.py::assert_value_free` (HW-1 / DoD#3)

```python
def assert_value_free(obj):
    """Walk a ProvisioningSpec OR a RunLedger OR a StepAction and assert no leaf holds a credential
    value — only NAMES, slot-refs, slugs, api ids, booleans, enums. Raises ValueLeakError naming the
    offending leaf if a leaf is anything other than the known value-free leaf shapes.
    There are no values in the system to leak (emit is pure; the mock never holds one) — this is the
    structural assertion that the surface CANNOT become a value channel."""
```
Walks the spec's tuples + each `SlotSpec` (name/kind/acquisition/populated) + each `StepAction`
(step/op/target/status/detail/created) + the ledger. The `populated` knob on the mock (a `set[str]` of
NAMES) is walked too (HW-1: confirm the mock cannot become a value channel — every member is asserted to
be a known slot NAME, never a value). `ValueLeakError` is a NEW exception in `provision/` (NOT in the
frozen `errors.py` — keep the frozen module byte-unchanged; home it in `port.py` or a `provision/errors.py`).

### 4.3 `port.py::Provisioner` (the ABC — W2)

```python
class Provisioner(abc.ABC):
    """The abstract provisioning port. The engine drives THIS, never a CLI. The ONLY concrete subclass
    that ships is MockProvisioner (W2). A real applier would be a NEW concrete subclass that does I/O —
    which does not exist in the package and would be a code-review-visible addition."""

    @abc.abstractmethod
    def ensure_project(self, slug) -> str: ...
    @abc.abstractmethod
    def ensure_sa(self, slug, project) -> str: ...
    @abc.abstractmethod
    def set_budget_boundary(self, slug, project) -> None: ...
    @abc.abstractmethod
    def enable_api(self, project, api) -> bool: ...        # returns created (False = already enabled)
    @abc.abstractmethod
    def grant_api_role(self, sa, api) -> bool: ...
    @abc.abstractmethod
    def ensure_secret_slot(self, project, name) -> bool: ...   # slot only, NO value
    @abc.abstractmethod
    def grant_secret_accessor(self, sa, secret_name) -> bool: ...  # per-secret, never project-wide
    @abc.abstractmethod
    def is_populated(self, name) -> bool: ...              # the S2c gate read — a BOOLEAN, never a value
    @abc.abstractmethod
    def provision_db_service(self, slug, db_extensions, postgis_base) -> str: ...
    @abc.abstractmethod
    def provision_serving_service(self, slug) -> str: ...
    @abc.abstractmethod
    def set_railway_var(self, service, name, source_slot=None) -> bool: ...  # names a SOURCE slot, never a value
    @abc.abstractmethod
    def apply_db_extension(self, db_service, ext) -> bool: ...
    @abc.abstractmethod
    def stand_up_mesh_shape(self, slug) -> "MeshShape": ...  # the §7 T1 SHAPE; returns a value-free descriptor
```
**No method takes or returns a credential value.** `is_populated` returns a boolean; `set_railway_var`
names a `source_slot`, never a value. This is what makes the port value-free by type.

### 4.4 `mock.py::MockProvisioner` (the ONLY concrete port — W2)

```python
class MockProvisioner(Provisioner):
    def __init__(self, populated=frozenset(), fail_at=None):
        # populated: set[str] of secret-slot NAMES the mock treats as already populated.
        #   value-free membership marker; default frozenset() -> EVERYTHING unpopulated -> S2c BLOCKS.
        # fail_at:  Optional[str] "S<n>:<op>" id at which the mock raises (exercises fail-closed aborts).
        self.populated = frozenset(populated)
        self.fail_at = fail_at
        self.ledger = []          # in-memory list[StepAction]-shaped records; NO I/O
        self._created = set()      # ids already created (create-or-get idempotency)
```
Each method: if `fail_at` matches `"S<n>:<op>"` for the current call → raise `MockProvisionerFailure`
(the engine catches → FAILED). Else record a synthetic deterministic id
(`mock-project-<slug>`, `mock-sa-<slug>`, etc.), return `created=False` if the id is already in
`_created` (idempotency), and return the value-free result. `is_populated(name)` returns
`name in self.populated`. The mock holds **zero credential values** in BOTH modes (HW-1).

### 4.5 `steps.py` — S0..S6 as pure step functions

Each: `def s<n>(resolved, slug, spec, provisioner) -> list[StepAction]`. They dispatch the spec's
already-derived fields to the port and return the actions. Per design-formal §4 + HAMILTON §2:

| Step | dispatch | port calls → StepAction(s) | block/fail |
|---|---|---|---|
| **S0** | fixed | `ensure_project(slug)`; `ensure_sa(slug,project)` (bijective); `set_budget_boundary(slug,project)` (the §5.B card requirement REPRESENTED) | any raise → FAILED, abort remainder; **runs before any S2** |
| **S1** | `gcp_api` | per api: `enable_api` + `grant_api_role` (idempotent) | enable raise → FAILED, abort |
| **S2** | `gcp_secret`+`thirdparty_rest_key` | **2a** `ensure_secret_slot` (slot only); **2b** `grant_secret_accessor` per-secret; **2c** `is_populated(name)` → if False, emit BLOCKED action, set ledger terminal=BLOCKED, **halt before S3** | **S2c BLOCKS** on any unpopulated slot → `BLOCKED-on-human` naming the slot; NEVER improvises a value. `thirdparty_rest_key` has **NO S1 step** (labstat_bls proof) |
| **S3** | `railway_var` + secret-backed | `provision_db_service(slug, db_extensions, postgis_base)`; `provision_serving_service(slug)`; per var `set_railway_var(service, name, source_slot=<slot>)`; inject THIS builder's SA-key-ref ONLY | any raise → FAILED, abort; no cross-builder key ref |
| **S4** | `db_extension` | `apply_db_extension(db_service, ext)` per resolved ext; `select_base_image(needs_postgis_base_image)` | missing required base-image cap → FAILED |
| **S5** | fixed T1 | `stand_up_mesh_shape(slug)` → the §7 T1 SHAPE (§8.5) + the CLI-client template carrying a `<VERB>` PLACEHOLDER + a generic `health` route ONLY; domain-empty | a half-provisioned builder (any S0–S4 abort) NEVER reaches S5 |
| **S6** | fixed | door preflight; assert each resolved `gcp_api` "enabled" in ledger; each `db_extension` "applied"; no slot unpopulated (else BLOCKED); runtime-completeness via `check_runtime_completeness(resolved)` (FROZEN call) | report-only; idempotent re-run = no-op |

### 4.6 `choreographer.py::Choreographer`

```python
class Choreographer:
    def __init__(self, provisioner):
        if provisioner is None:
            raise TypeError("Choreographer requires a Provisioner (no default) — W2")
        self.provisioner = provisioner
    def run(self, resolved, slug) -> RunLedger:
        """Emit the spec, then walk [S0,S1,S2,S3,S4,S5,S6] in fixed order, dispatching to the port.
        Stops at the first FAILED or BLOCKED (fail-closed). Records each action with its step index.
        S0<S2<S3/S5 is then a checkable property of the ledger (action step-indices monotonic)."""
```
The constructor REQUIRING the port (no default) is W2's teeth: a run cannot start without a port, and the
only port in existence is the mock.

### 4.7 `checklist.py` — the three relay-up generators (§10)

```python
def render_checklist(spec) -> str:           # relay-up #1 — PURE transform of the emit
def render_credential_attestation(spec) -> str:  # relay-up #2 — derivation over the spec
def render_tripwire_attestation() -> str:    # relay-up #3 — cites W1/W2/W3 + the grep command
```

---

## 5. The 3-wall structural TRIPWIRE (DoD#6 — VERA grep-verifies all three)

Three independent, machine-checkable walls. None rely on "we remembered not to call gcloud."

- **W1 — no I/O imports anywhere under `provision/`.**
  - AST test `test_tripwire_no_infra_imports`: walk every module under `provision/` with `ast`; assert the
    imported top-level module set ⊆ `{builder_deploy_core.*, dataclasses, enum, typing, abc, __future__}`
    (+ `sys` whitelisted for `__main__.py` ONLY).
  - **Grep attestation (DoD#6, the exact command VERA runs — fixed literal path, no `$VAR`, §6.13/§8.6):**
    ```
    grep -rnE '\b(subprocess|socket|urllib|requests|httpx|gcloud|railway|os\.system|popen)\b' builder_deploy_core/provision/
    ```
    MUST return nothing (exit 1 / empty). *(Authoring note: the regex is anchored on the canonical
    no-I/O token list HAMILTON §3.2 ratified; `os\.system`/`popen` are dotted/literal so the `\b`
    word-boundary on the leading token is correct; `railway`/`gcloud` are bare identifiers. The grep is an
    ATTESTATION corollary of the AST test — the AST test is authoritative, the grep is the
    human-auditable echo. Per §6.9: the AST test is the live round-trip; the grep is ground-checked
    against the actual shipped `provision/` tree at build time.)*
- **W2 — only the mock concrete port exists.** `test_tripwire_only_mock_port`: after
  `import builder_deploy_core.provision`, assert `Provisioner.__subclasses__() == [MockProvisioner]`.
  AND assert `Choreographer(None)` raises `TypeError` (constructor requires a port).
- **W3 — the emit side has no port at all.** `test_tripwire_emit_is_pure`: assert `emit_spec`'s signature
  takes no provisioner (inspect its parameters); assert calling `emit_spec` performs no I/O (it is a pure
  transform — covered structurally by W1 since spec.py is under provision/).

VERA's DoD#6 probe = run the three tests GREEN + run the grep and confirm empty. The relay-up #3
attestation (`render_tripwire_attestation`) cites W1/W2/W3 + the grep command + result.

---

## 6. The S5 §7 T1 SHAPE (CHIRON §2 contents, HAMILTON §2 stand-up)

`stand_up_mesh_shape(slug)` emits the §7 T1 surface (the `MeshShape` value-free descriptor):
- `tailscaled` → `tailscale serve --https=443` → a **0600 AF_UNIX socket** → the in-mesh trigger
  (loopback/UDS only);
- identity = the serve-injected `Tailscale-User-Login` header (**never** WhoIs-on-loopback);
- **deny-by-default** policy + the `<BUILDER>_OPERATORS` env var + `group:operators` allowlist;
- **Funnel OFF** (no public ingress);
- the **CLI-client-skill template** carrying a `<VERB>` PLACEHOLDER + a generic `health` route ONLY
  (counts-only response contract, `--check` door-probe, redacted-error tail); the domain endpoint is a
  `<VERB>` stub (501-not-implemented) until T3.
- **Domain-empty.** Zero domain verbs.

The `MeshShape` descriptor is value-free (template text + policy flags + the placeholder token) — it is a
SCAFFOLD spec, not a credential.

---

## 7. The jd5 fold — see §11. The worked examples — see §8.

## 8. The full test inventory (ADA's fixtures = VERA's probes) mapped to DoD 1–10

All new tests live in `tests/test_provision.py` (+ golden files under `tests/fixtures/provision-specs/`).
The conftest's `data_tables` session fixture + `load_manifest_fixture` are REUSED. Every fixture below is
both ADA's build target and VERA's re-executable probe.

### 8.1 Golden-file emit fixtures (DoD#1 — end-to-end emit, byte-stable)
For each of prospector / scienceclaw / labstat_bls: `emit_spec(resolve(M, baseline, library), slug)`
equals the expected `ProvisioningSpec` (golden file under `tests/fixtures/provision-specs/<name>.toml`,
the spec rendered as sorted value-free fields). Byte-stable (sorted tuples). The §8 resolved sets
(8/6/7) are the REGRESSION TARGET — these fixtures FAIL if `resolve()` ever drifts.
- `test_emit_prospector_golden` — 8-entry resolved → spec with apis {gemini-embedding, gemini-search,
  google-maps}, secret_slots {MAPS_API_KEY (mint-via-gcp-console), POSTGRES_PASSWORD (generate-locally)},
  db_extensions {pgvector, postgis}, needs_postgis_base_image=True, sa_scope == derive_sa_scope(resolved).
- `test_emit_scienceclaw_golden` — 6-entry → no postgis, needs_postgis_base_image=False.
- `test_emit_labstat_bls_golden` — 7-entry → secret_slots includes BLS_OEWS_API_KEY (mint-via-thirdparty);
  apis does NOT include BLS_OEWS_API_KEY (the labstat proof carried into emit).

### 8.2 Ordered / idempotent / fail-closed (DoD#2)
- `test_ledger_step_indices_monotonic` — mode-2 run: action step-indices are non-decreasing S0→S6;
  the first `ensure_secret_slot` (S2) has a step index ≥ the `ensure_sa` (S0); the
  `stand_up_mesh_shape` (S5) ≥ any S2/S3 action. (S0<S2<S3/S5 as a ledger property.)
- `test_idempotent_rerun_no_widen` — two `run()`s against the same mock state; the 2nd adds ZERO
  `created=True` actions (all SKIPPED/created=False). The ADD direction is total.
- `test_s2c_blocks_unpopulated` (NEGATIVE) — `MockProvisioner()` (default, unpopulated): run halts at
  S2c; `ledger.terminal == BLOCKED`; `ledger.blocked_slots` names every secret slot; NO S3/S5 action
  present.
- `test_s0_abort_no_key_materialized` (NEGATIVE) — `MockProvisioner(populated=<all>, fail_at="S0:ensure_sa")`:
  ledger has the failed S0 action, `terminal == FAILED`, and ZERO S2 actions (no key materialized before
  the lock).

### 8.3 value-free emit (DoD#3 / HW-1)
- `test_emit_value_free` — `assert_value_free(spec)` passes for all three examples (no leaf is a value).
- `test_ledger_value_free` — `assert_value_free(ledger)` passes for a mode-2 run (the mock ledger holds
  only names/refs).
- `test_mock_populated_is_value_free` — every member of a `MockProvisioner(populated=...)` set is a known
  slot NAME (HW-1: the mock cannot become a value channel); `assert_value_free` walks the mock state.

### 8.4 per-builder isolation (DoD#4)
- `test_isolation_bijective_sa` — exactly one `ensure_project` + one `ensure_sa` per run; `sa == f"sa-{slug}"`.
- `test_isolation_per_secret_accessor` — every `grant_secret_accessor` action's detail names exactly ONE
  secret, never a project wildcard.
- `test_sa_scope_is_derive_sa_scope` — `spec.sa_scope == tuple(derive_sa_scope(resolved))` (the FROZEN
  call; emit does NOT re-derive the union).
- `test_budget_boundary_present` — the S0 `set_budget_boundary` action is present; `budget_boundary_required`
  is True (the §5.B card requirement REPRESENTED, not created).

### 8.5 SHAPE stands up, domain-empty + THE STRICT §7 BOUNDARY PROBE (DoD#5)
- `test_s5_shape_stands_up` — mode-2 ledger contains `stand_up_mesh_shape`; the emitted MeshShape carries
  the §7 T1 surface (0600 AF_UNIX, `Tailscale-User-Login` header-trust, deny-by-default,
  `<BUILDER>_OPERATORS`, Funnel OFF) and the `<VERB>` placeholder + `health` route.
- `test_s7_boundary_no_domain_verb_leak` (**THE STRICT CANONICAL PROBE — CHIRON co-confirmed; supersedes
  ALL prior wordings, incl any softened "/run allowed as plumbing"**): grep the ENTIRE T1 surface (the
  S5 scaffold text + the CLI-client template, as emitted by `stand_up_mesh_shape` AND any template file
  ADA ships under `provision/`) for ANY domain route/verb token or builder name. The ONLY concrete route
  allowed in T1 is `health`. A hit on ANY of the leak tokens = the leak:
  ```
  LEAK_TOKENS = ["/run", "collect", "embed", "ingest", "search",
                 "newswire", "scienceclaw", "prospector"]
  ```
  **`/run` IS ON THE LEAK LIST.** The domain endpoint is a `<VERB>` placeholder/stub (501-until-T3). The
  test asserts NONE of `LEAK_TOKENS` appears in the emitted T1 surface. *(Authoring note §6.9: the probe
  greps the actual emitted SHAPE string + any shipped template file, not a paraphrase — it round-trips
  against the real `stand_up_mesh_shape` output; the leak-token list is the CHIRON §2 / Polybius_the_Stoa
  STRICT-form list verbatim. The probe scans the WHOLE surface, not just the route table, so a verb
  hidden in a comment or a docstring still trips it — COMPLETENESS clause.)*

### 8.6 TRIPWIRE held (DoD#6) — the three §5 tests + the grep
- `test_tripwire_no_infra_imports` (W1, AST) + the grep attestation.
- `test_tripwire_only_mock_port` (W2) — `Provisioner.__subclasses__() == [MockProvisioner]`;
  `Choreographer(None)` raises.
- `test_tripwire_emit_is_pure` (W3).

### 8.7 the labstat kind-dispatch carried into the choreography (DoD#1 corroborant)
- `test_labstat_skips_s1_for_thirdparty` — labstat_bls run: `BLS_OEWS_API_KEY` appears as an S2 secret
  slot + an S3 railway var, but NEVER in S1 (no `enable_api` action targets it). The §8.3 kind-dispatch
  proof carried into the choreography.

### 8.8 the deploy-help plan dispatch (DoD#7-adjacent, §9)
- `test_deploy_help_plan_dispatch` — for each example, each secret slot's `acquisition` is the correct
  derived method (MAPS_API_KEY→mint-via-gcp-console; BLS_OEWS_API_KEY→mint-via-thirdparty;
  POSTGRES_PASSWORD→generate-locally). The plan is emitted (in the spec / S2c action detail), not executed.

### 8.9 the relay-up generators (DoD#10)
- `test_render_checklist_is_pure_transform` — `render_checklist(spec)` is deterministic; running it twice
  gives identical text; it names every secret slot needing human population at S2c by acquisition method;
  it does NOT contain any value (it is a transform of the value-free spec).
- `test_render_credential_attestation` — the attestation text asserts the four credential-discipline
  points (value-free emit; no agent holds a value; applier reads from keyring/WIF; per-builder card =
  hard cap) and references the spec.
- `test_render_tripwire_attestation` — the attestation cites W1/W2/W3 + the grep command.

### 8.10 jd5 fold regression (DoD#8) — §11
- `test_install_then_import_smoke` (NEW) — build the wheel/sdist (or `pip install .` into a tmp venv);
  import `builder_deploy_core` from OUTSIDE the source tree; call `dataload.load_baseline()` and assert
  it loads the 5 baseline entries (proves `data/` is bundled by the intra-package glob).
- `test_dataload.py` (FROZEN bodies) — stays GREEN after the two data-path lines are updated (§11 step 5).

### 8.11 full suite (DoD#9)
VERA runs the FULL existing the-stoa suite (2.1 + 2.2 + gen-data + app) IN ADDITION to the bespoke
provision probes. The bespoke probes prove the new thing works; the full suite catches what the change
breaks elsewhere — esp. since the jd5 fold edits shared machinery (`dataload._DATA_ROOT` + the data tree
location). This is the gauntlet-verify discipline (full-suite + bespoke).

### DoD → probe map (the 1–10 the directive §5 names)
| DoD | Probe(s) |
|---|---|
| #1 end-to-end emit | §8.1 golden fixtures (prospector/scienceclaw/labstat) + §8.7 |
| #2 ordered/idempotent/fail-closed | §8.2 (monotonic + rerun-no-widen + S2c-blocks + S0-abort) |
| #3 value-free emit | §8.3 (assert_value_free over spec + ledger + mock state) |
| #4 per-builder isolation | §8.4 (bijective SA + per-secret accessor + sa_scope==derive_sa_scope + budget) |
| #5 SHAPE stands up + STRICT §7 boundary | §8.5 (shape stands up + the strict no-domain-verb-leak grep) |
| #6 TRIPWIRE held | §8.6 (W1/W2/W3 tests + grep) |
| #7 deploy-help library DESIGNED, mock-only | §9 + §8.8 (plan dispatch; no real browser/keyring) |
| #8 jd5 fold | §8.10 (install-then-import smoke + test_dataload green) |
| #9 full suite green | §8.11 (FULL suite + bespoke probes) |
| #10 relay-up generators | §8.9 (checklist + 2 attestations) |

---

## 9. The deploy-help library (HAMILTON §4 — DESIGNED in 2.3, exercised against MOCK only)

The human-in-the-loop credential-acquisition UX. In 2.3 the choreography **emits the per-slot deploy-help
PLAN text** (which acquisition method, which edge-URL template, which keyring invocation) — it does NOT
open a real browser, mint a real key, or write a real keyring. The plan rides the spec's `SlotSpec.acquisition`
+ the S2c action detail.

The pattern (the PRINCIPAL's 2026-06-26 default UX): agent drives a browser to the dashboard EDGE → a
clickable link opens the SAME dashboard in a browser the agent CANNOT see → the human mints PRIVATELY →
the agent runs the value-free keyring deploy-help (`keyring_paste` / `keyring_generate` /
`railway_set_secret` / `railway_run` via ENV/STDIN, never stdout/argv/disk).

| acquisition (derived) | slot examples | edge | deploy-help (the PLAN names it; the SCRIPT is the reuse source) |
|---|---|---|---|
| `mint-via-gcp-console` | MAPS_API_KEY | GCP Console → Credentials, this builder's project | `keyring_paste` → `railway_set_secret --var MAPS_API_KEY` (STDIN) |
| `mint-via-thirdparty` | BLS_OEWS_API_KEY | the third party's signup page | `keyring_paste` → `railway_set_secret` (STDIN) |
| `generate-locally` | POSTGRES_PASSWORD | no dashboard | `keyring_generate` (no human sees it) → `railway_set_secret --skip-deploys` before db-init |
| `mint-via-dashboard` | Railway PAT / TS_AUTHKEY | Railway Tokens / Tailscale Keys | `keyring_paste` → `railway_run` (ENV) / `railway_set_secret` (STDIN) |

**Reuse source:** `railway-keyring-deploy` at the USER-TIER path
`C:/Users/denso/.claude/skills/railway-keyring-deploy/` (NOT in-repo). 2.3 emits the PLAN per slot; it
does not bundle or invoke the scripts. **Build decision flagged for PLINY (§13 RQ-3):** whether the
builder-deploy SKILL wrapper in 2.3 should COPY the deploy-help library into the (HOME-agnostic) skill dir,
or only reference the user-tier path in the emitted plan text. I formalize 2.3 as **reference-only**
(plan-text names the user-tier reuse source; no library copy lands this pass) — the copy is a close/2.4
skill-wrapper step, consistent with HOME-agnostic. If PLINY wants the copy in 2.3, it is an additive
skill-dir add that does not touch the package.

---

## 10. The relay-up deliverable generators (DoD#10)

Three PURE generators in `checklist.py`, each a derivation over the value-free spec + the structural walls
(so none can drift from what the choreography actually does):

1. **`render_checklist(spec)` → the PROVISIONING CHECKLIST (relay-up #1).** Exactly what the PRINCIPAL
   provisions for a REAL builder, step + WHEN: per-builder GCP project + prepaid card + billing account +
   Railway + Tailscale + which secret slots need human population at S2c, BY acquisition method (§9). A
   PURE transform of the emit — cannot drift from the choreography.
2. **`render_credential_attestation(spec)` → the credential-discipline attestation (relay-up #2).** A
   derivation: every slot value-free (DoD#3); no agent holds a value (M2); applier reads from keyring/WIF;
   per-builder card = hard cap (§5.B / M5-moot).
3. **`render_tripwire_attestation()` → the TRIPWIRE-held attestation (relay-up #3).** Cites W1/W2/W3 + the
   §5 grep command + result.

The package PRODUCES these as text (files / stdout via `__main__.py`); the ORCHESTRATING seats (PLINY →
FM → Polybius_the_Stoa) LAND them on bw at the relay-up (the script-cannot-run-bw discipline — the
package is deterministic Python, not an Anthropic dynamic-workflow). The emitted value-free spec is the
durable seam artifact; it is WRITTEN to the working tree (or attached with a working-tree-pathed cite) so
the 2.4 applier reads it — per `[[reference-attach-only-artifacts-dangle-worktree-cites]]`.

---

## 11. The jd5 fold (PLINY-owned, folded into THIS pass — the coherent steps)

Move `data/` INSIDE the importable package so setuptools honors an intra-package glob (resolves the
stoa--pj3 CATO c2 parent-relative-glob bug + HAMILTON HW-4 by construction). Exact steps:

1. **`git mv agents/builder-deploy-core/data agents/builder-deploy-core/builder_deploy_core/data`** —
   move the whole tree (baseline.toml, kinds.toml, categories/, catalog/) inside the package.
2. **`dataload.py:25`** — change `_DATA_ROOT = Path(__file__).resolve().parent.parent / "data"` →
   `_DATA_ROOT = Path(__file__).resolve().parent / "data"`. (dataload.py is now `builder_deploy_core/
   dataload.py`; `.parent` is `builder_deploy_core/`, which now holds `data/`.) The comment block at
   lines 22–24 updates to "the package's own data/ subdir" (the data root is now INSIDE the package, not a
   sibling). This is the ONLY logic-adjacent edit to dataload.py; all load-function bodies are byte-unchanged.
3. **`pyproject.toml:31`** — change package-data `builder_deploy_core = ["../data/**/*.toml"]` →
   `builder_deploy_core = ["data/**/*.toml"]` (a normal intra-package glob setuptools honors).
4. **`pyproject.toml:28`** — add `"builder_deploy_core.provision"` to the `packages` list.
5. **`tests/test_dataload.py` lines 61 + 84** (LOAD-BEARING FOLD-COHERENCE EDIT — DAEDALUS catch):
   both read `Path(dataload.__file__).resolve().parent.parent / "data"`. After the move, `dataload.__file__`
   is `builder_deploy_core/dataload.py`, so `.parent.parent` is the PACKAGE ROOT (no longer holds `data/`).
   Change BOTH to `Path(dataload.__file__).resolve().parent / "data"`. WITHOUT this edit `test_dataload.py`
   goes RED (the P6 read-proof + the detection_hints `_REAL_DATA` copytree source both break). The brief's
   "Keep test_dataload.py GREEN (it may reference the data path)" is exactly this.
   *(conftest.py:18–19 comment says "holds builder_deploy_core/ and data/"; `_PKG_ROOT` is only used for
   sys.path, NOT a data read, so it stays FUNCTIONALLY valid — the comment is now slightly stale (data/ is
   inside the package). A one-line comment refresh is OPTIONAL hygiene, not a functional edit; ADA may
   refresh it but it is not load-bearing.)*
6. **`test_install_then_import_smoke`** (NEW, §8.10) — the regression guard CATO's c2 plan named: build +
   install into a tmp venv, import from outside the tree, load baseline — proves `data/` is bundled.

**MANIFEST.in:** none exists today; the intra-package `[tool.setuptools.package-data]` glob (step 3) is
the bundling mechanism — no MANIFEST.in needed for a wheel. (If the sdist smoke test (§8.10) reveals the
sdist drops the data tree, add a `MANIFEST.in` `recursive-include builder_deploy_core/data *.toml` —
flagged as a contingency, not a required step; the wheel path via package-data is the primary.)

---

## 12. Threat→mitigation map (A3 author duty — op-disc §35.4) + carried HW-1..4

This pass adds the CHOREOGRAPHY MECHANICS for design-formal §12's already-ratified M1–M6. It introduces
NO new mitigation mechanism; every `how-defeated` cell names a mechanism that now lives in this spec's
cited §section, realizing the design-formal §12 map at the build surface. DAEDALUS (upstream classifier,
§35.1) PROPOSES; ARGUS CONFIRMS at critique. The build surface is a **process/architecture change**
(pure code + a mock; provisions nothing) — but it REALIZES runtime-relevant mitigations, so each is mapped.

### 12.A Threat-ratified mitigations realized in the 2.3 build (M<n> → attack-path → how-defeated)
| M | Named threat | attack-path | how-defeated (this spec's mechanism + §) |
|---|---|---|---|
| **M1** | Per-builder isolation (cross-builder lateral movement) | a compromised key/over-scoped SA in builder A reads/spends builder B's secrets | **§4.5 S0** bijective `ensure_sa` (one SA ⟷ one builder) + **§4.5 S2** `grant_secret_accessor` per-secret (never project-wide) + **§3.2/§4.1** `sa_scope == derive_sa_scope(resolved)` (FROZEN mechanical union) + **§4.5 S3** injects only THIS builder's SA-key-ref. **Residual R-1 (carried, NOT defeated):** prune-on-removal still Phase-2; t0 initial-provision holds. |
| **M2** | Credential-discipline / agents-never-hold-values | a secret VALUE lands in an agent transcript/argv/disk | **§0.1 emit-then-apply** (value-free spec, slot NAMES only; real applier out-of-package forever) + **§4.5 S2c** human-population BLOCK (never improvises) + **§4.2 assert_value_free** (structural: no leaf can hold a value) + **§4.3/§4.4** the port takes/returns NO value (`is_populated`→bool; `set_railway_var`→source_slot ref) + the **3-wall TRIPWIRE §5** (real applier structurally unreachable on the test path) |
| **M3** | Runtime-completeness (key-bearing API enabled-but-keyless → 401) | Maps resolves enabled-but-keyless → builder deploys, 401s at call | **§4.5 S6** calls `check_runtime_completeness(resolved)` (FROZEN) — for every template-declared (gcp_api,gcp_secret) pairing, asserts the paired secret is resolved + populated |
| **M4** | Non-omittable baseline (baseline necessity silently omitted) | a manifest omits pgvector → silent drop → no vector store → runtime 500s | inherited UPSTREAM of 2.3: `resolve()` (FROZEN) raises `BaselineOmitError`; the §8 resolved sets 2.3 emits against already carry the guard. 2.3 adds no path that can re-introduce a baseline omit. |
| **M6** | Agent-access mesh security (unauthorized mesh access) | unauthorized party reaches a builder's mesh trigger/data | **§6 / §4.5 S5** T1 SHAPE: 0600 AF_UNIX socket + `tailscale serve` header-trust (`Tailscale-User-Login`, never WhoIs-on-loopback) + deny-by-default + `<BUILDER>_OPERATORS` + `group:operators` + Funnel OFF |

### 12.B Threat-anchored verification probes (§6.13 — the EXECUTED probe per named mitigation)
Each threat-ratified mitigation realized here carries a threat-ANCHORED probe (exercises the attack-path,
not the happy path) asserting BOTH (a) attack-blocked AND (b) legit-unaffected:

| M | threat-anchored probe (defeats_via_probe id) | (a) attack-blocked | (b) legit-unaffected |
|---|---|---|---|
| **M1** | `test_isolation_per_secret_accessor` + `test_sa_scope_is_derive_sa_scope` (§8.4) | a `grant_secret_accessor` action NEVER carries a project wildcard / another builder's secret; sa_scope is exactly the resolved union (no extra grant) | the builder's OWN resolved secrets DO get per-secret accessors (isolation didn't break the feature) |
| **M2** | `test_emit_value_free` + `test_ledger_value_free` + `test_mock_populated_is_value_free` (§8.3) + the §5 W1/W2/W3 TRIPWIRE | `assert_value_free` RAISES on any injected value leaf; the port has no value-bearing method; real applier structurally unreachable | a legitimate value-free emit + mock walk PASSES (the discipline didn't break the emit) |
| **M3** | `test_emit_prospector_golden` (the paired MAPS_API_KEY present) + an S6 runtime-completeness assert | an emit that DROPPED MAPS_API_KEY would fail the golden + the S6 check | the complete prospector spec (api + paired key) passes S6 |
| **M4** | (inherited) the FROZEN `test_resolution.py` baseline-omit fixture (§8.4 design-formal) | omitting a baseline entry RAISES BaselineOmitError | a legal category-template omit still resolves |
| **M6** | `test_s7_boundary_no_domain_verb_leak` (§8.5) + `test_s5_shape_stands_up` | the deny-by-default + header-trust SHAPE is present (no WhoIs-on-loopback, Funnel OFF); a domain-verb leak trips the strict grep | the generic `health` route + `<VERB>` placeholder stand up (the SHAPE works) |

### 12.C Not-threat-ratified classifications (so nothing security-relevant carries NO classification — §35.1)
DAEDALUS PROPOSES `not threat-ratified` for each; ARGUS CONFIRMS (§35.5 process-change carve-out — pure
code/mock, no runtime attack path):
| Element (this spec §) | Classification |
|---|---|
| The pure-emitter + port-driven-engine architecture (§0.1, §2) | not threat-ratified (architectural change; the SECURITY it serves is M2, the architecture itself is structure) |
| ProvisioningSpec / StepAction / RunLedger schemas (§3) | not threat-ratified (schema/correctness change, no runtime attack path; HW-3 rides on it) |
| The 2-mode mock (§4.4) | not threat-ratified (test substrate; provisions nothing; HW-1 value-free) |
| The jd5 fold (§11) | not threat-ratified (packaging/correctness change, no runtime attack path) |
| The relay-up generators (§10) | not threat-ratified (reporting/derivation change, no runtime attack path) |
| The deploy-help PLAN emit (§9) | not threat-ratified (plan-text only; M2 covers the value-discipline of the real apply, which 2.3 does NOT run) |

### 12.D Named residuals carried (honestly surfaced, NOT claimed defeated — §35.5)
- **R-1** (M1 stale-grant-until-reconcile) — prune-on-removal is Phase-2 builder-lifecycle; 2.3 is
  initial-provision (t0) emit + mock walk, where M1 holds. NOT defeated here.
- **R-2** (manifest integrity) — manifest authorship is an authz trust boundary; rests on git
  access-control + project-seat review. Upstream of 2.3. NOT a 2.3 mechanism.
- **R-3** (catalog integrity) — the catalog drives every builder's resolved set fleet-wide; rests on
  catalog-authoring discipline at arc time. Upstream of 2.3. NOT a 2.3 mechanism.
- **M5 MOOT** (budget runaway) — the per-builder prepaid card is the out-of-band hard cap (Grand
  pre-build gate); 2.3 REPRESENTS the card requirement at S0 (`set_budget_boundary` / `budget_boundary_required`),
  never creates a card.

### 12.E Carried self-assessed weak points from HAMILTON (HW-1..4) — status in this spec
- **HW-1** (mock `populated` could be a value channel) — RESOLVED structurally: typed `set[str]` of slot
  NAMES; `assert_value_free` walks the mock state; `test_mock_populated_is_value_free` (§8.3).
- **HW-2** (`acquisition` as in-band catalog field) — RESOLVED: `_derive_acquisition(kind, name)` derives
  the default; NO required catalog field added (§4.1); §8 fixtures untouched.
- **HW-3** (emit_spec schema is new surface) — RESOLVED: `ProvisioningSpec` frozen dataclass + golden-file
  fixtures per example (§3.2, §8.1).
- **HW-4** (data reachability under packaging) — RESOLVED by the jd5 fold (§11) + the install-then-import
  smoke test (§8.10).

---

## 13. Self-assessed weak points (for ARGUS to pressure-test)

- **DW-1 — `emit_spec` derivation of project/SA NAMES (`proj-<slug>` / `sa-<slug>`) is a SPEC convention,
  not the design-formal text.** design-formal §5.A says "SA name derived from the builder slug" but does
  not fix the exact string. I chose `sa-<slug>` / `proj-<slug>`. *Risk:* if the real GCP applier (2.4) or
  a downstream consumer expects a different convention (e.g. `sa-<slug>@<project>.iam.gserviceaccount.com`
  fully-qualified), the emitted name needs reshaping. *Why this shape:* the spec is value-free + the NAME
  is a derivation the applier can expand; emitting the bare slug-derived stem keeps emit pure and
  HOME/cloud-agnostic. **ARGUS: confirm the bare stem is the right emit granularity, or that the FQN
  belongs in the applier (2.4), not the emit.**
- **DW-2 — the W1 AST whitelist admits `sys` for `__main__.py`.** The `__main__` repro surface needs
  `sys.exit`. *Risk:* `sys` is a stdlib module; admitting it for one file is a (tiny) widening of the W1
  wall. *Why this shape:* the existing discovery/__main__.py already imports `sys`; `sys.exit` cannot
  reach infra; the grep attestation list (§5) does NOT include `sys` (it lists only I/O-capable tokens),
  so the human-auditable wall is unaffected. **ARGUS: confirm the `sys`-for-__main__ whitelist does not
  weaken W1 (vs. dropping `__main__.py` from the AST scan entirely, which I rejected as a bigger hole).**
- **DW-3 — the strict §7 boundary grep is a SUBSTRING scan, so a legitimate generic token containing a
  leak substring would false-positive.** e.g. a comment with the word "research" contains "search";
  "embedding" contains "embed". *Risk:* the strict probe could trip on innocent prose. *Why this shape:*
  CHIRON's STRICT list is the co-confirmed canonical list; I keep it verbatim rather than soften it. The
  mitigation: the T1 surface is SMALL + cookie-cutter generic, so ADA must author it to avoid the leak
  substrings (use "lookup" not "search", "vectorize" not "embed" in any generic prose) — the probe's
  strictness is the POINT (CHIRON: "/run IS a leak"). **ARGUS: confirm the substring-scan strictness is
  intended (a generic-prose false-positive is ADA's signal to reword, not a probe bug), OR direct a
  word-boundary refinement (`\bsearch\b`) if the false-positive risk outweighs the strictness.** I lean
  KEEP-STRICT (the directive's strict-canonical mandate).
- **DW-4 — the deploy-help library ships as PLAN-TEXT-ONLY in 2.3 (reference-only, §9), not a copied
  library.** *Risk:* if 2.4 expects the library co-located in the skill dir, that copy is deferred to
  close/2.4. *Why this shape:* TRIPWIRE — 2.3 emits the plan, not the action; the library is a user-tier
  reuse source; copying it is a HOME-agnostic skill-wrapper step. **This is RQ-3 for PLINY (a load-bearing
  skill-wrapper decision I flag rather than bake) — see §13 residual-questions.**
- **DW-5 — `set_railway_var(source_slot=...)` models secret-backed vars as actions that NAME a source
  slot, while the §8 resolved sets carry only DATABASE_URL as a `railway_var` entry.** The secret-backed
  vars (the gcp_secret/thirdparty values that become Railway env at deploy) are S3 ACTIONS referencing a
  slot, not `railway_var` ENTRIES in the resolved set. *Risk:* a reader could expect every injected var to
  be a resolved `railway_var` entry. *Why this shape:* the resolved set's `railway_var` kind is for
  explicitly-declared vars (DATABASE_URL); secret injection is a CHOREOGRAPHY step that reads the secret
  SLOTS (S2) and wires them as S3 vars by reference — keeping the value-free seam (the var's SOURCE is a
  slot name, never a value). **ARGUS: confirm the resolved `railway_var` set vs the S3 secret-backed-var
  injection are correctly distinguished, and that no secret-backed var leaks a value.**

**residual_questions_for_argus / PLINY:**
- **RQ-1** (DW-1) — is `sa-<slug>`/`proj-<slug>` the right emit granularity, or does the FQN belong in the
  2.4 applier?
- **RQ-2** (DW-3) — KEEP the strict substring leak-scan (my lean), or refine to word-boundary? The
  directive mandates the strict-canonical probe; I keep it strict and surface the false-positive tradeoff.
- **RQ-3** (DW-4, FLAGGED for PLINY per the brief's HOME-agnostic skill-wrapper clause) — does the
  builder-deploy SKILL wrapper COPY the deploy-help library into the (HOME-agnostic) skill dir in 2.3, or
  is reference-only (my formalization) correct, with the copy deferred to close/2.4? This is the one
  skill-wrapper decision I judged load-bearing enough to flag rather than bake.

**Empty-list defense:** the list is non-empty; the most load-bearing item is DW-3 (the strict §7 boundary
probe's substring strictness) — it is the directive's load-bearing boundary, and I keep it strict per the
co-confirmed canonical mandate while honestly surfacing the false-positive tradeoff for ARGUS to rule.

---

## 14. Out of scope (2.3 boundary)

- **The real applier** (CI-via-WIF / human keyring one-shot RUN against real infra) — out-of-package
  forever; 2.4 is the first real run, Grand-gated separately. 2.3 ships emit + mock only.
- **The T3 product layer** — domain verbs (`/run`, ingest, search), curated data, the domain skill body
  that fills the `<VERB>` placeholder. Owned by project seats (prospector team; Polybius_the_science_stoa
  for scienceclaw). T3 fills the placeholder at 2.4+.
- **The A-home `git mv`** to `substrate/skills/builder-deploy/` — additive close/2.4 step; the build is
  HOME-agnostic at `agents/builder-deploy-core` (§0.4).
- **Copying the deploy-help library into the skill dir** — reference-only in 2.3 (§9, RQ-3); copy deferred
  to close/2.4 unless PLINY rules otherwise.
- **Reconcile/prune-on-removal, manifest-integrity governance, catalog-integrity governance** — the R-1/
  R-2/R-3 Phase-2 residuals (§12.D); upstream of or after 2.3.
- **The PostGIS base-image Dockerfile body** — 2.3 emits the `needs_postgis_base_image` SIGNAL + the
  `select_base_image` action; the actual derived Dockerfile is a 2.4 build concern (design-formal §6
  DECIDE-C).
- **Multi-category builders, per-surface Maps granularity** — design-formal Phase-1 deferrals, unchanged.
