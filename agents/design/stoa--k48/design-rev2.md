---
author: Denson Smith
ticket: stoa--k48 (u--9s2 Phase-2 increment 2.3 — provisioning choreography, ONE pass: design folded into the build)
seat: CAPTAIN_DAEDALUS_the_stoa
supersedes: design-rev1.md
formalizes: agents/design/stoa--k48/chiron-ownership-tier-design.md (ownership/tier + §7 SHAPE/CONTENT + emit-then-apply + HOME + jd5)
          + agents/design/stoa--k48/provisioning-choreography-hamilton.md (S0–S6 mechanics + mock substrate + 3-wall TRIPWIRE + deploy-help)
ground-truth-held-unchanged: agents/design/stoa--jw5/design-formal.md §4 (S0–S6) / §5.A/§5.B (isolation) / §6 (db-extension) / §7 (SHAPE/CONTENT) / §8 (worked examples) / §12 (M1–M6 + R-1/R-2/R-3)
builds-on: agents/builder-deploy-core/ (2.1 resolution + 2.2 suggest) — resolve()/derive_sa_scope()/check_runtime_completeness() REUSED BYTE-UNCHANGED (FROZEN SURFACE)
revises: design-rev1.md — closes ARGUS findings r1 (W1 grep self-collision) / r2 (M3 not threat-anchored) / r3 (port-ABC contract gap, incl r5 label-drift). Everything ARGUS PASSED is carried unchanged.
status: FORMAL rev2 — single buildable spec for ADA; gauntlet-facing (ARGUS hand-back verify)
as_of: 2026-06-27
---

# u--9s2 Phase-2 inc 2.3 — FORMAL SPEC (rev2): the provisioning choreography (pure emitter + port-driven engine + mock substrate)

This formalizes the TWO reconciled co-design halves into ONE buildable artifact. It does NOT redesign
design-formal §4–§7 or §12 — it makes the Phase-2 build arc's mechanics concrete enough that ADA can
build verbatim and VERA can probe machine-checkably. **It provisions NOTHING real.** The mock substrate
makes a real `gcloud`/`railway`/card call STRUCTURALLY impossible on the test path (the 3-wall TRIPWIRE,
§5). Every fixed point both architects converged on is preserved (§0.2).

**rev2 is a FOCUSED revision of rev1.** It closes the 3 ARGUS findings (r1/r2/r3) and changes NOTHING
ARGUS passed. The precise closures are documented in §15 ("rev2 — ARGUS-finding closures"); the affected
spec sections (§3.1, §4.1, §4.3, §4.5, §4.7, §5, §8, §12.B) are updated inline so ADA builds from one
coherent artifact. A reader who only wants the deltas reads §15; a reader who builds reads the whole
artifact (it is self-contained and supersedes rev1).

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
HW-2-adjacent), matching the TRIPWIRE ("2.3 emits the PLAN text per slot, not the action"). ARGUS RQ-3
ruling + PLINY adopted: reference-only is a clean deferral (vendoring rides close/2.4).

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

**rev2 note (r2 closure):** the new M3 threat-anchored probe (§8.12) CALLS `check_runtime_completeness`
on a deliberately-broken resolved set. CALLING the frozen function is not EDITING it — the function body
stays byte-unchanged; the probe constructs its broken set in TEST code (`tests/test_provision.py`), never
in `resolve.py`. PLINY verifies frozen-byte-unchanged by git-diff after rev2 (strict-prefix / same-blob).

A build commit that edits any frozen-surface function body beyond §11's named lines is a regression CATO/
NOMOS flag; ADA verifies with `git diff` (strict-prefix / same-blob check) before commit.

### 0.4 HOME (RATIFIED, do not block)
RATIFIED = Option A-with-graduation-trigger (the-stoa forge-owned; canonical SOURCE
`substrate/skills/builder-deploy/`). The build is formalized against the DECISION-NEUTRAL
`agents/builder-deploy-core` location — HOME-agnostic. The A-home `git mv` is an additive close/2.4 step,
NOT this build. Where the spec needs the builder-deploy SKILL wrapper (SKILL.md + deploy-help placement),
it is formalized HOME-agnostic / relocatable-by-additive-`git mv`; the deploy-help library copy is
DEFERRED to close/2.4 (ARGUS RQ-3 ruling, PLINY adopted — reference-only in 2.3, §9).

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
    tripwire.py      #   THE W1 NO-I/O TOKEN LIST — assembled from FRAGMENTS (r1 closure, §5/§15.1); the
                     #     SSoT both the AST test and render_tripwire_attestation consume. NEVER carries the
                     #     joined alternation literal on a single source line.
    checklist.py     #   render_checklist(spec) -> str  (relay-up #1) + the credential-discipline /
                     #     TRIPWIRE-held attestation derivations (relay-up #2/#3 text generators).
                     #     render_tripwire_attestation() cites the W1 wall STRUCTURALLY via tripwire.py —
                     #     it NEVER embeds the joined token alternation literal (r1 closure, §15.1).
    __main__.py      #   `python -m builder_deploy_core.provision` — dry-run emit + mock walk repro surface
```

**Import-discipline (the TRIPWIRE's teeth, W1, §5):** every module under `provision/` imports ONLY
`builder_deploy_core.*` + stdlib `dataclasses` / `enum` / `typing` / `abc` / `__future__`. It imports
**none** of `subprocess`, `os`, `os.system`, `socket`, `http`, `urllib`, `requests`, `httpx`, `asyncio`,
`gcloud`, `railway`. `mock.py` is pure (records actions into a list; no filesystem, no network).
`__main__.py` may import `sys` (for `sys.exit`) — the W1 grep list (§5) does NOT include `sys`, so this is
permitted; the AST test (§5 W1) whitelists `sys` for `__main__.py` only, exactly as the existing
discovery/__main__.py uses `sys`.

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
    op: str                    # the port verb actually dispatched. The CANONICAL op vocabulary is EXACTLY
                               #   the set of @abstractmethod names on the §4.3 Provisioner ABC (r3/r5
                               #   closure — op strings are reconciled to the port surface, §15.3):
                               #     "ensure_project" | "ensure_sa" | "set_budget_boundary" | "enable_api" |
                               #     "grant_api_role" | "ensure_secret_slot" | "grant_secret_accessor" |
                               #     "is_populated" | "provision_db_service" | "provision_serving_service" |
                               #     "set_railway_var" | "apply_db_extension" | "select_base_image" |
                               #     "stand_up_mesh_shape"
                               #   PLUS the engine-level S6 verify pseudo-op "verify" (NOT a port call — S6
                               #   re-reads the ledger; see §4.5 S6). There is NO "require_population" op and
                               #   NO "verify_*" port method — the S2c gate read is the port's is_populated
                               #   (a boolean); S6 verify is engine-level (r5 reconciled, §15.3).
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

`op` is a free-form `str` field by TYPE (golden-file equality needs no enum), but its CONTRACTUAL
vocabulary is pinned to the §4.3 ABC method names above + the engine-level `"verify"` (r5 reconciliation,
§15.3) — so no ledger ever names a port verb the ABC does not declare. This keeps the spec internally
consistent: every op a step dispatches (§4.5) is a declared `@abstractmethod` (r3) or the engine `verify`.

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
- `project = f"proj-{slug}"`, `sa = f"sa-{slug}"` (bijective, §5.A; bare slug-derived stem — ARGUS RQ-1
  ruling: the FQN belongs in the 2.4 applier, not the emit).
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

**r3 closure (§15.3):** EVERY port verb dispatched by ANY step in §4.5 is now declared `@abstractmethod`
on this ABC. The previously-undeclared `select_base_image` is added. The S6 `verify` is engine-level (the
choreographer re-reads its own ledger), NOT a port method — so it is intentionally absent from the ABC.
This makes the W2 pin (`Provisioner.__subclasses__() == [MockProvisioner]`) meaningful: the ABC forces
`MockProvisioner` to implement every dispatched verb, so an undeclared/unimplemented port verb is an
import-time `TypeError` (cannot instantiate the mock), not a latent S4 `AttributeError`.

```python
class Provisioner(abc.ABC):
    """The abstract provisioning port. The engine drives THIS, never a CLI. The ONLY concrete subclass
    that ships is MockProvisioner (W2). A real applier would be a NEW concrete subclass that does I/O —
    which does not exist in the package and would be a code-review-visible addition.

    CONTRACT (W2 + r3): every verb a §4.5 step dispatches is an @abstractmethod here. The S6 verify is
    engine-level (ledger re-read), NOT a port call, so it is deliberately not declared."""

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
    def select_base_image(self, needs_postgis_base) -> str: ...   # r3 ADDED — S4 dispatches it (§4.5);
                                                                  #   returns a value-free base-image TAG/ref,
                                                                  #   e.g. "base-postgis" | "base-plain"
    @abc.abstractmethod
    def stand_up_mesh_shape(self, slug) -> "MeshShape": ...  # the §7 T1 SHAPE; returns a value-free descriptor
```
**No method takes or returns a credential value.** `is_populated` returns a boolean; `set_railway_var`
names a `source_slot`, never a value; `select_base_image` returns a value-free image tag. This is what
makes the port value-free by type. The full dispatched-verb audit (every step's port calls vs the ABC) is
in §15.3 — every cell is covered.

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
(`mock-project-<slug>`, `mock-sa-<slug>`, `mock-image-postgis`/`mock-image-plain` for `select_base_image`,
etc.), return `created=False` if the id is already in `_created` (idempotency), and return the value-free
result. `is_populated(name)` returns `name in self.populated`. The mock holds **zero credential values**
in BOTH modes (HW-1). Because the ABC now declares `select_base_image` (r3), the mock MUST implement it
or it is uninstantiable — the W2 test catches an omission at import time.

### 4.5 `steps.py` — S0..S6 as pure step functions

Each: `def s<n>(resolved, slug, spec, provisioner) -> list[StepAction]`. They dispatch the spec's
already-derived fields to the port and return the actions. Per design-formal §4 + HAMILTON §2:

| Step | dispatch | port calls → StepAction(s) | block/fail |
|---|---|---|---|
| **S0** | fixed | `ensure_project(slug)`; `ensure_sa(slug,project)` (bijective); `set_budget_boundary(slug,project)` (the §5.B card requirement REPRESENTED) | any raise → FAILED, abort remainder; **runs before any S2** |
| **S1** | `gcp_api` | per api: `enable_api` + `grant_api_role` (idempotent) | enable raise → FAILED, abort |
| **S2** | `gcp_secret`+`thirdparty_rest_key` | **2a** `ensure_secret_slot` (slot only); **2b** `grant_secret_accessor` per-secret; **2c** `is_populated(name)` → if False, emit BLOCKED action, set ledger terminal=BLOCKED, **halt before S3** | **S2c BLOCKS** on any unpopulated slot → `BLOCKED-on-human` naming the slot; NEVER improvises a value. `thirdparty_rest_key` has **NO S1 step** (labstat_bls proof) |
| **S3** | `railway_var` + secret-backed | `provision_db_service(slug, db_extensions, postgis_base)`; `provision_serving_service(slug)`; per var `set_railway_var(service, name, source_slot=<slot>)`; inject THIS builder's SA-key-ref ONLY | any raise → FAILED, abort; no cross-builder key ref |
| **S4** | `db_extension` | `apply_db_extension(db_service, ext)` per resolved ext; `select_base_image(needs_postgis_base_image)` (now an ABC `@abstractmethod`, r3) | missing required base-image cap → FAILED |
| **S5** | fixed T1 | `stand_up_mesh_shape(slug)` → the §7 T1 SHAPE (§8.5) + the CLI-client template carrying a `<VERB>` PLACEHOLDER + a generic `health` route ONLY; domain-empty | a half-provisioned builder (any S0–S4 abort) NEVER reaches S5 |
| **S6** | fixed | door preflight; assert each resolved `gcp_api` "enabled" in ledger; each `db_extension` "applied"; no slot unpopulated (else BLOCKED); runtime-completeness via `check_runtime_completeness(resolved)` (FROZEN call) | **engine-level `verify` (NOT a port call — re-reads the ledger)**; report-only; idempotent re-run = no-op |

S6 emits its checks as `StepAction(step="S6", op="verify", ...)` engine-level entries — `verify` is the
ONLY op string that is not a port method (r5 reconciled, §15.3); every other op in §3.1's vocabulary is a
declared `@abstractmethod` (§4.3). S6 also calls the FROZEN `check_runtime_completeness(resolved)` and, if
it returns `ok=False`, records the missing pairings as a value-free `verify` action detail
(`(("missing_api","<api>"),("missing_secret","<secret>"))`) — this is the in-choreography read of the
same invariant the §8.12 threat-anchored probe asserts directly against the frozen function.

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

### 4.7 `checklist.py` + `tripwire.py` — the W1 SSoT + the three relay-up generators (§10)

**r1 closure (§15.1):** the W1 no-I/O token list lives in `tripwire.py` as a list of FRAGMENTS, assembled
at runtime — the joined alternation pattern NEVER appears as a literal on any source line. Both the AST
test and `render_tripwire_attestation()` consume this SSoT; the attestation cites the W1 wall
STRUCTURALLY (by listing the AST whitelist + the fragment-built token set + the grep INVOCATION shape)
WITHOUT embedding the bare joined alternation. Result: the W1 grep over the WHOLE `provision/` (including
`checklist.py` and `tripwire.py`) returns EMPTY, AND the attestation still meaningfully cites the W1 command.

```python
# tripwire.py — the W1 SSoT (r1 closure)
# The forbidden-I/O token list, held as FRAGMENTS so no single source line carries the joined
# alternation pattern the W1 grep scans for. The grep over provision/ therefore returns EMPTY even
# though this module DEFINES the list (the bytes "subprocess|socket|...|popen" never appear here).
_W1_FRAGMENTS = (
    ("sub", "process"), ("soc", "ket"), ("url", "lib"), ("requ", "ests"),
    ("ht", "tpx"), ("gcl", "oud"), ("rail", "way"), ("os.sy", "stem"), ("po", "pen"),
)
def w1_forbidden_tokens():
    """Return the forbidden top-level-import token set, assembled at runtime from fragments.
    No source line in provision/ contains the joined alternation, so the W1 grep stays clean."""
    return tuple(a + b for (a, b) in _W1_FRAGMENTS)
```

The AST test (§5 W1) builds its forbidden set via `w1_forbidden_tokens()` (so the SSoT is shared, not
re-typed). `render_tripwire_attestation()` (below) describes the W1 wall via this SSoT + the grep
invocation TEMPLATE, never the joined literal.

```python
def render_checklist(spec) -> str:           # relay-up #1 — PURE transform of the emit
def render_credential_attestation(spec) -> str:  # relay-up #2 — derivation over the spec
def render_tripwire_attestation() -> str:    # relay-up #3 — cites W1/W2/W3 STRUCTURALLY (r1):
                                             #   W1: "no top-level import of any forbidden-I/O module
                                             #        (the tripwire.w1_forbidden_tokens() set), verified by
                                             #        the AST test AND a grep over provision/ for those
                                             #        tokens (the grep returns empty)." — NO joined literal.
                                             #   W2: only MockProvisioner subclasses Provisioner.
                                             #   W3: emit_spec takes no provisioner.
```

`render_tripwire_attestation()` cites the grep by REFERENCE ("the §5 W1 grep over provision/ for the
forbidden-I/O token set returns empty") and may enumerate the tokens via `w1_forbidden_tokens()` at
RUNTIME if it needs to LIST them in prose — but it builds that list from the fragment SSoT, so the source
of `checklist.py` never contains the joined `tok|tok|...` alternation the grep scans for. (If the rendered
ATTESTATION TEXT lists the tokens pipe-joined, that text is RUNTIME OUTPUT, not source bytes — the grep
scans `provision/` SOURCE, not the attestation's stdout, so it stays clean. §15.1 states the exact grep.)

---

## 5. The 3-wall structural TRIPWIRE (DoD#6 — VERA grep-verifies all three)

Three independent, machine-checkable walls. None rely on "we remembered not to call gcloud."

- **W1 — no I/O imports anywhere under `provision/`.**
  - AST test `test_tripwire_no_infra_imports`: walk every module under `provision/` with `ast`; assert the
    imported top-level module set ⊆ `{builder_deploy_core.*, dataclasses, enum, typing, abc, __future__}`
    (+ `sys` whitelisted for `__main__.py` ONLY). The forbidden token set the test compares against is
    `tripwire.w1_forbidden_tokens()` (the shared SSoT, §4.7) — the AST test is AUTHORITATIVE (a
    string-literal is not an import; the test reasons over the parsed import nodes).
  - **Grep attestation (DoD#6, the exact command VERA runs — fixed literal path, no `$VAR`, §6.13/§8.6):**
    ```
    grep -rnE '\b(subprocess|socket|urllib|requests|httpx|gcloud|railway|os\.system|popen)\b' builder_deploy_core/provision/
    ```
    MUST return nothing (exit 1 / empty). **r1 closure (§15.1):** this now returns EMPTY over the WHOLE
    `provision/` tree — INCLUDING `checklist.py` and `tripwire.py` — because the token list is held as
    FRAGMENTS (`tripwire._W1_FRAGMENTS`, assembled at runtime by `w1_forbidden_tokens()`), so no single
    source line carries the joined `subprocess|...|popen` alternation, and `render_tripwire_attestation()`
    cites the wall STRUCTURALLY rather than embedding the joined literal. *(Authoring note: the regex is
    anchored on the canonical no-I/O token list HAMILTON §3.2 ratified; `os\.system`/`popen` are
    dotted/literal so the `\b` word-boundary on the leading token is correct; `railway`/`gcloud` are bare
    identifiers. The grep is an ATTESTATION corollary of the AST test — the AST test is authoritative, the
    grep is the human-auditable echo. Per §6.9: the AST test is the live round-trip; the grep is
    ground-checked against the actual shipped `provision/` tree at build time. The §15.1 closure adds the
    REQUIREMENT that the grep is run over the WHOLE tree and the source contains no joined literal — so
    AST and grep AGREE, both clean, restoring the grep-is-the-echo-of-the-AST property ARGUS r1 flagged.)*
- **W2 — only the mock concrete port exists.** `test_tripwire_only_mock_port`: after
  `import builder_deploy_core.provision`, assert `Provisioner.__subclasses__() == [MockProvisioner]`.
  AND assert `Choreographer(None)` raises `TypeError` (constructor requires a port). AND (r3-corroborant)
  assert `MockProvisioner` is instantiable — i.e. it implements EVERY `@abstractmethod` incl
  `select_base_image` (an undeclared/unimplemented dispatched verb would make instantiation raise
  `TypeError` at import, which this test would surface).
- **W3 — the emit side has no port at all.** `test_tripwire_emit_is_pure`: assert `emit_spec`'s signature
  takes no provisioner (inspect its parameters); assert calling `emit_spec` performs no I/O (it is a pure
  transform — covered structurally by W1 since spec.py is under provision/).

VERA's DoD#6 probe = run the three tests GREEN + run the grep and confirm empty. The relay-up #3
attestation (`render_tripwire_attestation`) cites W1/W2/W3 + the grep command (by reference + the
fragment-built token set) + result — WITHOUT embedding the joined alternation literal (r1).

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
- `test_s7_boundary_no_domain_verb_leak` (**THE STRICT CANONICAL PROBE — CHIRON co-confirmed; ARGUS RQ-2
  KEEP-STRICT endorsed; supersedes ALL prior wordings, incl any softened "/run allowed as plumbing"**):
  grep the ENTIRE T1 surface (the S5 scaffold text + the CLI-client template, as emitted by
  `stand_up_mesh_shape` AND any template file ADA ships under `provision/`) for ANY domain route/verb token
  or builder name. The ONLY concrete route allowed in T1 is `health`. A hit on ANY of the leak tokens = the
  leak:
  ```
  LEAK_TOKENS = ["/run", "collect", "embed", "ingest", "search",
                 "newswire", "scienceclaw", "prospector"]
  ```
  **`/run` IS ON THE LEAK LIST.** The domain endpoint is a `<VERB>` placeholder/stub (501-until-T3). The
  test asserts NONE of `LEAK_TOKENS` appears in the emitted T1 surface. *(Authoring note §6.9: the probe
  greps the actual emitted SHAPE string + any shipped template file, not a paraphrase — it round-trips
  against the real `stand_up_mesh_shape` output; the leak-token list is the CHIRON §2 / Polybius_the_Stoa
  STRICT-form list verbatim. The probe scans the WHOLE surface, not just the route table, so a verb
  hidden in a comment or a docstring still trips it — COMPLETENESS clause. ARGUS RQ-2: a generic-prose
  false-positive is ADA's signal to REWORD the T1 surface domain-neutrally, not a probe bug.)*

### 8.6 TRIPWIRE held (DoD#6) — the three §5 tests + the grep
- `test_tripwire_no_infra_imports` (W1, AST; forbidden set = `tripwire.w1_forbidden_tokens()`) + the grep
  attestation (now EMPTY over the whole tree incl checklist.py/tripwire.py — r1, §15.1).
- `test_tripwire_only_mock_port` (W2) — `Provisioner.__subclasses__() == [MockProvisioner]`;
  `Choreographer(None)` raises; `MockProvisioner` instantiable (every `@abstractmethod` incl
  `select_base_image` implemented — r3-corroborant).
- `test_tripwire_emit_is_pure` (W3).
- `test_w1_attestation_grep_clean` (NEW, r1 closure — §15.1): assert the §5 W1 grep run over the WHOLE
  `provision/` tree (checklist.py + tripwire.py INCLUDED) returns EMPTY (exit 1 / no matches). This is the
  machine-check that the grep and the AST test AGREE (both clean). VERA re-runs the literal grep; the test
  encodes it so a regression (a future edit re-introducing the joined literal) goes RED in CI, not just at
  VERA's manual grep.

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
- `test_render_tripwire_attestation` — the attestation cites W1/W2/W3 + the grep command BY REFERENCE
  (r1: it cites the wall structurally + the fragment-built token set; it does NOT embed the joined
  alternation literal in the SOURCE). The test also asserts the §5 grep over `provision/` stays empty
  AFTER this generator is added (i.e. adding `render_tripwire_attestation` did not re-introduce a literal)
  — this is the r1 regression guard at the generator's own source.

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

### 8.12 M3 runtime-completeness — THE THREAT-ANCHORED PROBE (DoD#3-adjacent / §12.B; r2 closure, §15.2)
- `test_m3_runtime_completeness_drops_paired_secret` (NEW — the threat-anchored M3 probe, §6.13):
  exercises the M3 ATTACK PATH (a key-bearing `gcp_api` present but its paired `gcp_secret` DROPPED), not
  the happy path. It asserts BOTH halves against the FROZEN `check_runtime_completeness` (CALLED, never
  edited — §0.3):

  **Fixture** (constructed in TEST code, value-free, no `resolve.py` edit):
  ```python
  # The complete prospector-shaped resolved set has the key-bearing pairing google-maps -> MAPS_API_KEY
  # (KEY_BEARING_PAIRING, frozen). Build the ATTACK set by DROPPING the paired secret.
  complete = resolve(prospector_manifest, baseline, library)        # FROZEN resolve; google-maps + MAPS_API_KEY both present
  attack   = [e for e in complete if e != ("gcp_secret", "MAPS_API_KEY")]   # paired secret DROPPED, api kept
  ```
  **(a) attack-blocked:**
  ```python
  ok, missing = check_runtime_completeness(attack)     # FROZEN call
  assert ok is False
  assert ("google-maps", "MAPS_API_KEY") in missing    # the dropped pairing is NAMED as missing
  ```
  **(b) legit-unaffected:**
  ```python
  ok, missing = check_runtime_completeness(complete)    # FROZEN call, complete set
  assert ok is True
  assert missing == []                                  # a complete resolved set passes — the check did
                                                        # not break the legitimate (paired) builder
  ```
  This is the EXECUTED probe the verdict's M3 threat-coverage line cites (`defeats_via_probe:
  test_m3_runtime_completeness_drops_paired_secret`). It falsifies "M3 drifted to the wrong surface": the
  golden (§8.1) proves emit shape; THIS probe proves the runtime-completeness invariant FIRES on the
  attack path and STAYS QUIET on the legit path. The probe constructs the attack set entirely in
  `tests/test_provision.py`; `resolve.py` (incl `check_runtime_completeness`) stays byte-unchanged.
  *(Authoring note §6.9 / §6.13: the probe round-trips against the REAL frozen function + the REAL
  prospector resolved set — the `("google-maps","MAPS_API_KEY")` pairing is the actual KEY_BEARING_PAIRING
  entry, not a paraphrase; if the catalog ever renames that pairing the probe goes RED, which is correct —
  it is pinned to the live frozen surface, not a fixture copy.)*

### DoD → probe map (the 1–10 the directive §5 names)
| DoD | Probe(s) |
|---|---|
| #1 end-to-end emit | §8.1 golden fixtures (prospector/scienceclaw/labstat) + §8.7 |
| #2 ordered/idempotent/fail-closed | §8.2 (monotonic + rerun-no-widen + S2c-blocks + S0-abort) |
| #3 value-free emit + M3 runtime-completeness | §8.3 (assert_value_free over spec + ledger + mock state) + §8.12 (M3 threat-anchored) |
| #4 per-builder isolation | §8.4 (bijective SA + per-secret accessor + sa_scope==derive_sa_scope + budget) |
| #5 SHAPE stands up + STRICT §7 boundary | §8.5 (shape stands up + the strict no-domain-verb-leak grep) |
| #6 TRIPWIRE held | §8.6 (W1/W2/W3 tests + grep + the r1 grep-clean regression guard) |
| #7 deploy-help library DESIGNED, mock-only | §9 + §8.8 (plan dispatch; no real browser/keyring) |
| #8 jd5 fold | §8.10 (install-then-import smoke + test_dataload green) |
| #9 full suite green | §8.11 (FULL suite + bespoke probes) |
| #10 relay-up generators | §8.9 (checklist + 2 attestations, incl the r1 attestation grep-clean guard) |

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

*(r4 authoring note, ARGUS non-load-bearing — folded as a constraint, not a spec change: the table's
deploy-help tokens use the UNDERSCORE forms (`railway_set_secret`, `railway_run`) and CAPITALIZED service
names (`Railway`, `GCP`), which the §5 W1 grep's `\b(...|railway|gcloud|...)\b` word-boundary does NOT
match — bare-lowercase `railway`/`gcloud` would trip it. ADA MUST keep generic prose under `provision/` in
these safe forms. This is the §9 deploy-help PLAN-TEXT discipline; the r1 fragment-SSoT closes the
attestation-self-collision, and this note closes the adjacent prose-fragility ARGUS r4 named. The §8.6
`test_w1_attestation_grep_clean` is the machine guard for both.)*

**Reuse source:** `railway-keyring-deploy` at the USER-TIER path
`C:/Users/denso/.claude/skills/railway-keyring-deploy/` (NOT in-repo). 2.3 emits the PLAN per slot; it
does not bundle or invoke the scripts. **ARGUS RQ-3 ruling, PLINY adopted:** the builder-deploy SKILL
wrapper in 2.3 is **reference-only** (plan-text names the user-tier reuse source; no library copy lands
this pass) — the copy is a close/2.4 skill-wrapper step, consistent with HOME-agnostic.

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
   §5 grep command BY REFERENCE (r1: structural citation via the fragment-built token SSoT, NOT the joined
   alternation literal in source) + result.

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
§35.1) PROPOSES; ARGUS CONFIRMED + RATIFIED (verdict RATIFICATION LIST). The build surface is a
**process/architecture change** (pure code + a mock; provisions nothing) — but it REALIZES runtime-relevant
mitigations, so each is mapped.

### 12.A Threat-ratified mitigations realized in the 2.3 build (M<n> → attack-path → how-defeated)
| M | Named threat | attack-path | how-defeated (this spec's mechanism + §) |
|---|---|---|---|
| **M1** | Per-builder isolation (cross-builder lateral movement) | a compromised key/over-scoped SA in builder A reads/spends builder B's secrets | **§4.5 S0** bijective `ensure_sa` (one SA ⟷ one builder) + **§4.5 S2** `grant_secret_accessor` per-secret (never project-wide) + **§3.2/§4.1** `sa_scope == derive_sa_scope(resolved)` (FROZEN mechanical union) + **§4.5 S3** injects only THIS builder's SA-key-ref. **Residual R-1 (carried, NOT defeated):** prune-on-removal still Phase-2; t0 initial-provision holds. |
| **M2** | Credential-discipline / agents-never-hold-values | a secret VALUE lands in an agent transcript/argv/disk | **§0.1 emit-then-apply** (value-free spec, slot NAMES only; real applier out-of-package forever) + **§4.5 S2c** human-population BLOCK (never improvises) + **§4.2 assert_value_free** (structural: no leaf can hold a value) + **§4.3/§4.4** the port takes/returns NO value (`is_populated`→bool; `set_railway_var`→source_slot ref; `select_base_image`→image tag) + the **3-wall TRIPWIRE §5** (real applier structurally unreachable on the test path; the W1 grep now AGREES with the AST test — r1) |
| **M3** | Runtime-completeness (key-bearing API enabled-but-keyless → 401) | Maps resolves enabled-but-keyless → builder deploys, 401s at call | **§4.5 S6** calls `check_runtime_completeness(resolved)` (FROZEN) — for every template-declared (gcp_api,gcp_secret) pairing, asserts the paired secret is resolved + populated. **Threat-anchored probe §8.12** exercises the drop-the-paired-secret attack path directly against the frozen function (r2). |
| **M4** | Non-omittable baseline (baseline necessity silently omitted) | a manifest omits pgvector → silent drop → no vector store → runtime 500s | inherited UPSTREAM of 2.3: `resolve()` (FROZEN) raises `BaselineOmitError`; the §8 resolved sets 2.3 emits against already carry the guard. 2.3 adds no path that can re-introduce a baseline omit. |
| **M6** | Agent-access mesh security (unauthorized mesh access) | unauthorized party reaches a builder's mesh trigger/data | **§6 / §4.5 S5** T1 SHAPE: 0600 AF_UNIX socket + `tailscale serve` header-trust (`Tailscale-User-Login`, never WhoIs-on-loopback) + deny-by-default + `<BUILDER>_OPERATORS` + `group:operators` + Funnel OFF |

### 12.B Threat-anchored verification probes (§6.13 — the EXECUTED probe per named mitigation)
Each threat-ratified mitigation realized here carries a threat-ANCHORED probe (exercises the attack-path,
not the happy path) asserting BOTH (a) attack-blocked AND (b) legit-unaffected:

| M | threat-anchored probe (defeats_via_probe id) | (a) attack-blocked | (b) legit-unaffected |
|---|---|---|---|
| **M1** | `test_isolation_per_secret_accessor` + `test_sa_scope_is_derive_sa_scope` (§8.4) | a `grant_secret_accessor` action NEVER carries a project wildcard / another builder's secret; sa_scope is exactly the resolved union (no extra grant) | the builder's OWN resolved secrets DO get per-secret accessors (isolation didn't break the feature) |
| **M2** | `test_emit_value_free` + `test_ledger_value_free` + `test_mock_populated_is_value_free` (§8.3) + the §5 W1/W2/W3 TRIPWIRE (+ §8.6 `test_w1_attestation_grep_clean`, r1) | `assert_value_free` RAISES on any injected value leaf; the port has no value-bearing method; real applier structurally unreachable; the W1 grep returns empty AND agrees with the AST test (r1) | a legitimate value-free emit + mock walk PASSES (the discipline didn't break the emit) |
| **M3** | **`test_m3_runtime_completeness_drops_paired_secret` (§8.12 — THREAT-ANCHORED, r2 closure)** | drop the paired `gcp_secret` (`MAPS_API_KEY`) while keeping the key-bearing `gcp_api` (`google-maps`): `check_runtime_completeness(attack)` returns `ok=False` with `("google-maps","MAPS_API_KEY") in missing` (the enabled-but-keyless → 401 attack is REPORTED, not silently shipped) | the COMPLETE prospector resolved set (api + paired key both present) returns `ok=True, missing==[]` — the check did not break the legitimate paired builder |
| **M4** | (inherited) the FROZEN `test_resolution.py` baseline-omit fixture (badbuilder_pgvector_omit, §8.4 design-formal) | omitting a baseline entry RAISES BaselineOmitError | a legal category-template omit still resolves |
| **M6** | `test_s7_boundary_no_domain_verb_leak` (§8.5) + `test_s5_shape_stands_up` | the deny-by-default + header-trust SHAPE is present (no WhoIs-on-loopback, Funnel OFF); a domain-verb leak trips the strict grep | the generic `health` route + `<VERB>` placeholder stand up (the SHAPE works) |

**r2 closure note:** the M3 row previously bound to `test_emit_prospector_golden` (a happy-path
spec-equality assert) + an unnamed S6 assert — ARGUS r2 correctly flagged that as map-present/probe-absent
(§6.9 clause-4). The M3 row now cites `test_m3_runtime_completeness_drops_paired_secret` (§8.12), which
EXERCISES the attack path. The golden (§8.1) stays as the emit-shape regression target; it is no longer
the threat-anchored probe. The verdict's M3 `defeats_via_probe:` is now
`test_m3_runtime_completeness_drops_paired_secret`.

### 12.C Not-threat-ratified classifications (so nothing security-relevant carries NO classification — §35.1)
DAEDALUS PROPOSED `not threat-ratified` for each; ARGUS CONFIRMED (§35.5 process-change carve-out — pure
code/mock, no runtime attack path):
| Element (this spec §) | Classification |
|---|---|
| The pure-emitter + port-driven-engine architecture (§0.1, §2) | not threat-ratified (architectural change; the SECURITY it serves is M2, the architecture itself is structure) |
| ProvisioningSpec / StepAction / RunLedger schemas (§3) | not threat-ratified (schema/correctness change, no runtime attack path; HW-3 rides on it) |
| The 2-mode mock (§4.4) | not threat-ratified (test substrate; provisions nothing; HW-1 value-free) |
| The jd5 fold (§11) | not threat-ratified (packaging/correctness change, no runtime attack path) |
| The relay-up generators (§10) | not threat-ratified (reporting/derivation change, no runtime attack path) |
| The deploy-help PLAN emit (§9) | not threat-ratified (plan-text only; M2 covers the value-discipline of the real apply, which 2.3 does NOT run) |
| The W1 fragment-SSoT / tripwire.py (§4.7, r1) | not threat-ratified (it STRENGTHENS the M2-serving W1 wall's attestation; the W1 wall itself is the M2 mechanism, the fragment-assembly is an attestation-coherence fix with no runtime attack path) |
| The select_base_image ABC declaration (§4.3, r3) | not threat-ratified (port-contract correctness; tightens the W2 mock-only pin, no runtime attack path) |

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

(Carried from rev1; ARGUS ruled RQ-1/RQ-2/RQ-3 — those rulings are now adopted, so DW-1/DW-3/DW-4 are
DOWNGRADED to ruled-and-adopted notes. The remaining open self-assessment for rev2 is the r1 closure's
own residual, DW-6.)

- **DW-1 — `emit_spec` derives bare `proj-<slug>` / `sa-<slug>` stems, not FQNs.** *ARGUS RQ-1 RULING
  (adopted):* the bare stem is CORRECT at the emit; the FQN belongs in the 2.4 applier (keeps the emitter
  pure + HOME/cloud-agnostic; bijectivity preserved one slug→one stem→one FQN). NOT a 2.3 change.
- **DW-3 — the strict §7 boundary grep is a SUBSTRING scan (false-positive on innocent prose).** *ARGUS
  RQ-2 RULING (adopted):* KEEP STRICT — a generic-prose false-positive is ADA's signal to REWORD the T1
  surface domain-neutrally (lookup not search; vectorize not embed), not a probe bug. The strictness is
  the point (`/run` IS a leak). NOT refined to word-boundary.
- **DW-4 — deploy-help ships PLAN-TEXT-ONLY in 2.3 (reference-only).** *ARGUS RQ-3 RULING + PLINY adopted:*
  reference-only is a clean deferral; the library COPY rides the close/2.4 HOME `git mv`. No DoD gap.
- **DW-5 — `set_railway_var(source_slot=...)` models secret-backed vars as actions naming a source slot,
  while the §8 sets carry only DATABASE_URL as a `railway_var` entry.** *ARGUS NON-FINDING (confirmed
  coherent):* the resolved sets carry exactly one `railway_var`=DATABASE_URL each; secret-backed vars are
  correctly S3 ACTIONS naming a `source_slot`, not resolved entries; no value leaks.
- **DW-6 (NEW, rev2 — the r1 closure's own residual) — the W1 grep cleanliness now depends on an AUTHORING
  DISCIPLINE: no source line under `provision/` may carry the joined `tok|tok|...` alternation, and any
  prose naming the railway/gcloud service must use the safe (underscore / capitalized) form.** The
  fragment-SSoT (`tripwire._W1_FRAGMENTS`) removes the attestation self-collision structurally, but a
  FUTURE edit (a new docstring, a new generic-prose line) could re-introduce a bare token. *Mitigation /
  why this shape:* the §8.6 `test_w1_attestation_grep_clean` test ENCODES the grep over the whole
  `provision/` tree as a CI assertion — so a regression goes RED in the suite, not just at VERA's manual
  grep. I judged the fragment-SSoT + the CI grep-guard the right shape (vs. excluding checklist.py from
  the grep scope, which I REJECTED: a scope-exclusion would create exactly the AST-vs-grep DISAGREEMENT
  ARGUS r1 flagged — the grep must scan the WHOLE tree to be the AST test's honest echo). **ARGUS: confirm
  the fragment-SSoT + whole-tree-grep-as-CI-test is the right r1 closure (vs a grep --exclude), and that
  the attestation still meaningfully cites the W1 command when it cites by structural reference rather than
  embedding the joined literal.**

**residual_questions_for_argus:**
- **RQ-4 (NEW, rev2)** — is the r1 fragment-SSoT + whole-tree-grep-CI-guard closure the right mechanism,
  or would ARGUS prefer the grep cite the wall purely by the AST whitelist (dropping any token enumeration
  from the attestation output entirely)? I lean fragment-SSoT (it keeps the attestation able to LIST the
  forbidden tokens at runtime for the human auditor, while keeping the SOURCE clean). RQ-1/RQ-2/RQ-3 are
  RULED + adopted (no longer open).

**Empty-list defense:** the list is non-empty; the most load-bearing rev2 item is DW-6 (the r1 closure's
authoring-discipline residual), mitigated by the §8.6 CI grep-guard.

---

## 14. Out of scope (2.3 boundary)

- **The real applier** (CI-via-WIF / human keyring one-shot RUN against real infra) — out-of-package
  forever; 2.4 is the first real run, Grand-gated separately. 2.3 ships emit + mock only.
- **The T3 product layer** — domain verbs (`/run`, ingest, search), curated data, the domain skill body
  that fills the `<VERB>` placeholder. Owned by project seats (prospector team; Polybius_the_science_stoa
  for scienceclaw). T3 fills the placeholder at 2.4+.
- **The A-home `git mv`** to `substrate/skills/builder-deploy/` — additive close/2.4 step; the build is
  HOME-agnostic at `agents/builder-deploy-core` (§0.4).
- **Copying the deploy-help library into the skill dir** — reference-only in 2.3 (§9, ARGUS RQ-3 ruling);
  copy deferred to close/2.4.
- **The stem→FQN expansion** of `sa-<slug>`/`proj-<slug>` — the 2.4 applier's single deterministic fn
  (ARGUS RQ-1 ruling); 2.3 emits the bare stem.
- **Reconcile/prune-on-removal, manifest-integrity governance, catalog-integrity governance** — the R-1/
  R-2/R-3 Phase-2 residuals (§12.D); upstream of or after 2.3.
- **The PostGIS base-image Dockerfile body** — 2.3 emits the `needs_postgis_base_image` SIGNAL + the
  `select_base_image` action (now an ABC `@abstractmethod`, r3); the actual derived Dockerfile is a 2.4
  build concern (design-formal §6 DECIDE-C).
- **Multi-category builders, per-surface Maps granularity** — design-formal Phase-1 deferrals, unchanged.

---

## 15. rev2 — ARGUS-finding closures (the precise deltas vs design-rev1)

Three load-bearing ARGUS findings (r1/r2/r3, all easy-easy), closed below. Everything ARGUS passed is
carried unchanged. r4/r5 (non-load-bearing) are folded as noted. The frozen surface stays BYTE-UNCHANGED;
the M3 closure CALLS `check_runtime_completeness`, never edits it.

### 15.1 r1 — the W1 grep ATTESTATION self-collision (biggest)
**ARGUS finding:** `render_tripwire_attestation()` in `provision/checklist.py` (§2) was directed (rev1 §5)
to cite the W1 grep command, whose literal contains the bare tokens
`subprocess|socket|urllib|requests|httpx|gcloud|railway|os.system|popen`. The W1 grep over
`builder_deploy_core/provision/` then MATCHED those tokens INSIDE checklist.py → DoD#6 grep returns
NON-EMPTY (FAILS) while the AST test (authoritative; a string-literal is not an import) PASSES. AST and
grep DISAGREE, defeating the design's "the grep is the human-auditable echo of the AST" property.

**Closure mechanism (chosen: FRAGMENT-ASSEMBLY + STRUCTURAL CITATION — rev2 §4.7, §2):**
1. The W1 no-I/O token list moves to a NEW module `provision/tripwire.py` as a tuple of FRAGMENTS
   (`_W1_FRAGMENTS = (("sub","process"), ("soc","ket"), ... ("po","pen"))`), with a `w1_forbidden_tokens()`
   function that JOINS each fragment pair at RUNTIME. The bytes `subprocess|socket|...|popen` (the joined
   alternation the grep scans for) NEVER appear on any source line under `provision/`.
2. The AST test (§5 W1) builds its forbidden set from `tripwire.w1_forbidden_tokens()` (shared SSoT, not
   re-typed) — the AST test stays authoritative (it reasons over parsed import nodes).
3. `render_tripwire_attestation()` cites the W1 wall STRUCTURALLY: it describes "no top-level import of
   any forbidden-I/O module (the `tripwire.w1_forbidden_tokens()` set), verified by the AST test AND a
   grep over `provision/` for those tokens (returns empty)." It cites the grep BY REFERENCE. If the
   rendered attestation TEXT lists the tokens pipe-joined, that is RUNTIME OUTPUT (stdout), not source
   bytes — the grep scans `provision/` SOURCE, so it stays clean.
**Why this shape (vs the two rejected alternatives):**
- *Rejected: grep `--exclude=checklist.py`.* That would create exactly the AST-vs-grep DISAGREEMENT ARGUS
  flagged — the grep must scan the WHOLE tree to be the AST test's honest echo. A scope-exclusion hides
  the collision instead of removing it.
- *Rejected: attestation cites the grep by reference ONLY, no token enumeration ever.* Workable, but it
  removes the attestation's ability to LIST the forbidden tokens for a human auditor. The fragment-SSoT
  keeps that ability (runtime join) while keeping the source clean — strictly more useful, same safety.

**The resulting DoD#6 probe + the EXACT grep VERA runs (fixed literal path, §8.6/§6.13):**
```
grep -rnE '\b(subprocess|socket|urllib|requests|httpx|gcloud|railway|os\.system|popen)\b' builder_deploy_core/provision/
```
MUST return nothing (exit 1 / empty) over the WHOLE `provision/` tree — checklist.py AND tripwire.py
INCLUDED. The new `test_w1_attestation_grep_clean` (§8.6) encodes this grep as a CI assertion so a future
re-introduction of the joined literal goes RED in the suite. Result: the W1 grep and the AST test AGREE
(both clean) WITHOUT weakening either wall — the AST test still authoritatively rejects a real I/O import;
the grep still scans the whole tree; the attestation still meaningfully cites the W1 command.

### 15.2 r2 — the M3 probe was not threat-anchored
**ARGUS finding:** §12.B bound M3 (runtime-completeness; api-enabled-but-keyless → 401) to
`test_emit_prospector_golden` (a HAPPY-PATH spec-equality assert) + an unnamed S6 assert. No probe
exercised the M3 attack path. §6.9 clause-4 map-present/probe-absent smell.

**Closure (rev2 §8.12 + §12.B M3 row):** ADD `test_m3_runtime_completeness_drops_paired_secret` — a
threat-anchored probe that takes the prospector resolved set (key-bearing `gcp_api` `google-maps` + paired
`gcp_secret` `MAPS_API_KEY`), DROPS `MAPS_API_KEY`, and asserts:
- **(a) attack-blocked:** `check_runtime_completeness(attack)` → `ok=False`, `("google-maps","MAPS_API_KEY")
  in missing` (the FROZEN function reports the enabled-but-keyless pairing).
- **(b) legit-unaffected:** `check_runtime_completeness(complete)` → `ok=True`, `missing==[]`.
The §12.B M3 row now cites this probe as `defeats_via_probe`. The probe CALLS the FROZEN
`check_runtime_completeness` (L162) and builds the attack set in `tests/test_provision.py` — it does NOT
edit `resolve.py` (frozen surface untouched, §0.3). The golden (§8.1) stays as the emit-shape regression
target.

### 15.3 r3 — the port-ABC contract gap (incl r5 op-string label drift)
**ARGUS finding (r3):** S4 (§4.5) dispatches `provisioner.select_base_image(...)` but `select_base_image`
was NOT an `@abstractmethod` on the §4.3 `Provisioner` ABC → W2's `__subclasses__()==[MockProvisioner]`
pin did not force the mock to implement it → latent S4 `AttributeError` or an ad-hoc mock method outside
the audited port surface. **ARGUS finding (r5, non-load-bearing, folded here):** §3.1's `StepAction.op`
example list named `require_population` and `verify_*` as ops, but the S2c gate port method is
`is_populated` and there is no `verify_*` port method (S6 verify is engine-level).

**Closure (rev2 §4.3 + §3.1 + the §15.3 audit table):**
1. `select_base_image(self, needs_postgis_base) -> str` is now declared `@abstractmethod` on the ABC
   (§4.3). Because the ABC declares it, `MockProvisioner` MUST implement it or it is uninstantiable — the
   W2 test catches an omission at import time (`test_tripwire_only_mock_port` asserts the mock is
   instantiable).
2. §3.1's `op` vocabulary is reconciled to EXACTLY the ABC method names + the engine-level `"verify"`:
   `require_population` is REMOVED (the gate read is `is_populated`); `verify_*` becomes the single
   engine-level pseudo-op `"verify"` (S6 re-reads the ledger; NOT a port call, so deliberately NOT an ABC
   method).

**Full dispatched-verb audit (every §4.5 step's port calls vs the §4.3 ABC — every cell covered):**
| Step | dispatched port verb(s) | `@abstractmethod` on ABC? |
|---|---|---|
| S0 | `ensure_project`, `ensure_sa`, `set_budget_boundary` | yes / yes / yes |
| S1 | `enable_api`, `grant_api_role` | yes / yes |
| S2 | `ensure_secret_slot`, `grant_secret_accessor`, `is_populated` | yes / yes / yes |
| S3 | `provision_db_service`, `provision_serving_service`, `set_railway_var` | yes / yes / yes |
| S4 | `apply_db_extension`, **`select_base_image`** | yes / **yes (r3 ADDED)** |
| S5 | `stand_up_mesh_shape` | yes |
| S6 | `verify` (engine-level ledger re-read — NOT a port call) + the FROZEN `check_runtime_completeness` call | n/a (intentionally not a port method) |

Every port verb a step dispatches is now a declared `@abstractmethod`; the only non-ABC op string is the
engine-level `"verify"`, explicitly carved out. This makes the W2 mock-only pin meaningful: the ABC forces
the mock to implement every dispatched verb, so the audited port surface IS the complete dispatch set.
