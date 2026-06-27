# author: Denson Smith
# ticket: stoa--k48 (u--9s2 Phase-2 increment 2.3 — provisioning choreography)
# seat-built-by: CAPTAIN_ADA_the_stoa (EXECUTOR)
# design-ground-truth: agents/design/stoa--k48/design-rev2.md §3.2 (SlotSpec/ProvisioningSpec) /
#                       §4.1 (emit_spec — PURE, value-free, W3) / §4.2 (assert_value_free — HW-1/DoD#3)
#
# The PURE EMITTER (W3): resolved set -> ProvisioningSpec. NO provisioner parameter, NO I/O. Same input
# -> byte-identical spec (every collection a sorted tuple). value-free by construction: there is NO field
# that can hold a credential value (slot NAMES only). emit_spec calls the FROZEN derive_sa_scope (it does
# NOT re-derive the union). Imports stdlib dataclasses/typing + builder_deploy_core.* ONLY (W1).

from __future__ import annotations

from dataclasses import dataclass

from builder_deploy_core.resolution.resolve import derive_sa_scope


# The §3.3 secret-bearing kinds (a secret SLOT is emitted for these).
_SECRET_KINDS = ("gcp_secret", "thirdparty_rest_key")


@dataclass(frozen=True)
class SlotSpec:
    name: str           # the secret-slot NAME (e.g. "MAPS_API_KEY", "POSTGRES_PASSWORD"). NEVER a value.
    kind: str           # "gcp_secret" | "thirdparty_rest_key"
    acquisition: str    # the §9 deploy-help method, DERIVED (HW-2)
    populated: bool = False  # emit-time always False — a STATUS boolean, never a value


@dataclass(frozen=True)
class ProvisioningSpec:
    builder_slug: str
    project: str                               # derived NAME: f"proj-{slug}"
    sa: str                                    # bijective SA NAME: f"sa-{slug}" (§5.A)
    apis: tuple[str, ...]                      # sorted gcp_api names to enable (S1)
    secret_slots: tuple[SlotSpec, ...]         # sorted-by-name secret slots (S2)
    railway_vars: tuple[str, ...]              # sorted railway_var NAMES (S3)
    db_extensions: tuple[str, ...]             # sorted db_extension names (S4)
    sa_scope: tuple[tuple[str, str], ...]      # = derive_sa_scope(resolved) (FROZEN call)
    needs_postgis_base_image: bool             # postgis in resolved (the §6 base-image select signal)
    budget_boundary_required: bool = True      # the §5.B prepaid-card requirement REPRESENTED


def _derive_acquisition(kind: str, name: str) -> str:
    """HW-2 — derive the §9 deploy-help acquisition method as a PURE function of (kind, name). No new
    required catalog field (the §8 fixtures are untouched). An OPTIONAL catalog override may be threaded
    in a Phase-2 follow-up; 2.3 derives it."""
    if kind == "thirdparty_rest_key":
        return "mint-via-thirdparty"
    # kind == "gcp_secret" from here
    if name == "POSTGRES_PASSWORD":
        return "generate-locally"
    if name == "TS_AUTHKEY":
        return "mint-via-dashboard"  # if ever resolved as a gcp_secret
    return "mint-via-gcp-console"     # any other key-bearing gcp_secret (e.g. MAPS_API_KEY)


def emit_spec(resolved, builder_slug) -> ProvisioningSpec:
    """PURE transform: resolved set -> ProvisioningSpec. No provisioner, no I/O (W3).

    resolved: the sorted [(kind, name)] from resolve() (FROZEN).
    builder_slug: the builder slug (^[a-z][a-z0-9_]*$, matching the manifest `builder` pattern).
    Returns a ProvisioningSpec (§3.2). Same input -> byte-identical spec (sorted tuples)."""
    slug = builder_slug
    rset = list(resolved)

    apis = tuple(sorted(name for (kind, name) in rset if kind == "gcp_api"))

    secret_slots = tuple(
        sorted(
            (
                SlotSpec(
                    name=name,
                    kind=kind,
                    acquisition=_derive_acquisition(kind, name),
                    populated=False,
                )
                for (kind, name) in rset
                if kind in _SECRET_KINDS
            ),
            key=lambda s: s.name,
        )
    )

    railway_vars = tuple(sorted(name for (kind, name) in rset if kind == "railway_var"))
    db_extensions = tuple(sorted(name for (kind, name) in rset if kind == "db_extension"))
    sa_scope = tuple(derive_sa_scope(rset))   # the FROZEN call — never re-derive the union
    needs_postgis = ("db_extension", "postgis") in set(rset)

    return ProvisioningSpec(
        builder_slug=slug,
        project=f"proj-{slug}",
        sa=f"sa-{slug}",
        apis=apis,
        secret_slots=secret_slots,
        railway_vars=railway_vars,
        db_extensions=db_extensions,
        sa_scope=sa_scope,
        needs_postgis_base_image=needs_postgis,
        budget_boundary_required=True,
    )


# ---------------------------------------------------------------------------
# §4.2 assert_value_free (HW-1 / DoD#3) — the structural value-channel assertion.
# ---------------------------------------------------------------------------
# Known value-free leaf types: str (a NAME/ref/slug/api id), bool, enum (StepStatus). A leaf of any
# other type is the structural smell that the surface became a value channel.
def _assert_leaf(value, where: str) -> None:
    import enum as _enum

    from builder_deploy_core.provision.port import ValueLeakError

    if isinstance(value, bool):
        return
    if isinstance(value, str):
        return
    if isinstance(value, _enum.Enum):
        return
    raise ValueLeakError(
        f"value-free violation at {where}: leaf is {type(value).__name__} (not a name/ref/bool/enum): "
        f"{value!r}"
    )


def assert_value_free(obj) -> None:
    """Walk a ProvisioningSpec OR a RunLedger OR a StepAction OR a SlotSpec OR a MeshShape OR a mock
    `populated` set and assert no leaf holds a credential value — only NAMES, slot-refs, slugs, api ids,
    booleans, enums. Raises ValueLeakError naming the offending leaf otherwise.

    There are no values in the system to leak (emit is pure; the mock never holds one) — this is the
    structural assertion that the surface CANNOT become a value channel (HW-1)."""
    # Imported here to avoid a hard import cycle at module load (choreographer imports spec).
    from builder_deploy_core.provision.choreographer import RunLedger
    from builder_deploy_core.provision.port import StepAction, MeshShape as _Mesh

    if isinstance(obj, ProvisioningSpec):
        _assert_leaf(obj.builder_slug, "spec.builder_slug")
        _assert_leaf(obj.project, "spec.project")
        _assert_leaf(obj.sa, "spec.sa")
        for a in obj.apis:
            _assert_leaf(a, "spec.apis[]")
        for s in obj.secret_slots:
            assert_value_free(s)
        for v in obj.railway_vars:
            _assert_leaf(v, "spec.railway_vars[]")
        for e in obj.db_extensions:
            _assert_leaf(e, "spec.db_extensions[]")
        for (k, n) in obj.sa_scope:
            _assert_leaf(k, "spec.sa_scope[].kind")
            _assert_leaf(n, "spec.sa_scope[].name")
        _assert_leaf(obj.needs_postgis_base_image, "spec.needs_postgis_base_image")
        _assert_leaf(obj.budget_boundary_required, "spec.budget_boundary_required")
        return

    if isinstance(obj, SlotSpec):
        _assert_leaf(obj.name, "slot.name")
        _assert_leaf(obj.kind, "slot.kind")
        _assert_leaf(obj.acquisition, "slot.acquisition")
        _assert_leaf(obj.populated, "slot.populated")
        return

    if isinstance(obj, StepAction):
        _assert_leaf(obj.step, "action.step")
        _assert_leaf(obj.op, "action.op")
        _assert_leaf(obj.target, "action.target")
        _assert_leaf(obj.status, "action.status")
        for pair in obj.detail:
            # detail is a closed tuple-of-(key, name-ref) pairs
            if not (isinstance(pair, tuple) and len(pair) == 2):
                from builder_deploy_core.provision.port import ValueLeakError
                raise ValueLeakError(
                    f"value-free violation at action.detail: not a (key,name) pair: {pair!r}")
            _assert_leaf(pair[0], "action.detail[].key")
            _assert_leaf(pair[1], "action.detail[].name")
        _assert_leaf(obj.created, "action.created")
        return

    if isinstance(obj, RunLedger):
        _assert_leaf(obj.builder_slug, "ledger.builder_slug")
        for a in obj.actions:
            assert_value_free(a)
        _assert_leaf(obj.terminal, "ledger.terminal")
        for s in obj.blocked_slots:
            _assert_leaf(s, "ledger.blocked_slots[]")
        return

    if isinstance(obj, _Mesh):
        for attr in (
            obj.builder_slug, obj.socket_mode, obj.transport, obj.identity_header,
            obj.deny_by_default, obj.operators_env, obj.operators_group, obj.funnel_off,
            obj.verb_placeholder, obj.client_template,
        ):
            _assert_leaf(attr, "mesh_shape.field")
        for r in obj.routes:
            _assert_leaf(r, "mesh_shape.routes[]")
        return

    # A mock `populated` set / frozenset of slot NAMES (HW-1: the mock cannot become a value channel).
    if isinstance(obj, (set, frozenset, tuple, list)):
        for member in obj:
            _assert_leaf(member, "populated-set member")
        return

    from builder_deploy_core.provision.port import ValueLeakError
    raise ValueLeakError(f"assert_value_free: unrecognized object type {type(obj).__name__}: {obj!r}")
