# author: Denson Smith
# ticket: stoa--k48 (u--9s2 Phase-2 increment 2.3 — provisioning choreography)
# seat-built-by: CAPTAIN_ADA_the_stoa (EXECUTOR)
# design-ground-truth: agents/design/stoa--k48/design-rev2.md §4.4 (MockProvisioner — the ONLY concrete
#                       port, W2) / §3.1 (value-free) / §0.2 fixed-point 5 (the value-free 2-mode mock)
#
# MockProvisioner — the ONLY concrete Provisioner. ZERO I/O: it records synthetic deterministic ids into
# an in-memory list, holds NO credential value in EITHER mode (HW-1), and implements EVERY @abstractmethod
# on the ABC (so it is instantiable — the W2 test catches an omission at import time). Two value-free
# modes: default (everything unpopulated -> S2c BLOCKS) and populated=<slot-name set> (S3-S6 run).
# Imports stdlib only (W1).

from __future__ import annotations

from builder_deploy_core.provision.port import MeshShape, Provisioner


class MockProvisionerFailure(Exception):
    """Raised by the mock when fail_at matches the current call — exercises the fail-closed aborts.
    The choreographer catches it and records a FAILED action (the remainder is aborted)."""


# The CLI-client-skill template the T1 SHAPE carries. Domain-EMPTY: the only concrete route is "health";
# the domain endpoint is a "<VERB>" placeholder (a 501-not-implemented stub until the T3 product fills it).
# Worded domain-neutrally so the strict §7 boundary probe (no domain-verb leak) finds NOTHING: this text
# uses only "health", "<VERB>", and generic scaffold language.
_T1_CLIENT_TEMPLATE = (
    "# T1 CLI-client template (domain-empty scaffold).\n"
    "# The ONLY concrete route is health; the domain endpoint is the <VERB> placeholder (501 until T3).\n"
    "# Response contract: counts-only. Door-probe via --check. Error tail is redacted.\n"
    "routes:\n"
    "  - health        # generic liveness door-probe\n"
    "  - <VERB>        # domain endpoint placeholder — 501 until the T3 product fills it\n"
)


class MockProvisioner(Provisioner):
    def __init__(self, populated=frozenset(), fail_at=None):
        # populated: set[str] of secret-slot NAMES the mock treats as already populated. A value-free
        #   membership marker; default frozenset() -> EVERYTHING unpopulated -> S2c BLOCKS.
        # fail_at: Optional[str] "S<n>:<op>" id at which the mock raises (exercises fail-closed aborts).
        self.populated = frozenset(populated)
        self.fail_at = fail_at
        self.ledger = []        # in-memory record list; NO I/O
        self._created = set()    # ids already created (create-or-get idempotency)

    # -- internal helpers ---------------------------------------------------
    def _maybe_fail(self, step: str, op: str) -> None:
        if self.fail_at and self.fail_at == f"{step}:{op}":
            raise MockProvisionerFailure(f"mock fail_at {self.fail_at}")

    def _created_flag(self, ident: str) -> bool:
        """Return True if this is the first create of ident (idempotent create-or-get)."""
        if ident in self._created:
            return False
        self._created.add(ident)
        return True

    # -- the port surface (every ABC @abstractmethod) -----------------------
    # NOTE: the mock does NOT know the current step for _maybe_fail at call time, so fail_at matching is
    # done by the choreographer/steps which pass the step context. The mock methods here are value-free
    # synthetic-id recorders; fail injection is driven by the steps layer calling _maybe_fail. The mock
    # exposes _maybe_fail/_created_flag for the steps to use deterministically.

    def ensure_project(self, slug) -> str:
        return f"mock-project-{slug}"

    def ensure_sa(self, slug, project) -> str:
        return f"mock-sa-{slug}"

    def set_budget_boundary(self, slug, project) -> None:
        return None

    def enable_api(self, project, api) -> bool:
        return self._created_flag(f"api:{project}:{api}")

    def grant_api_role(self, sa, api) -> bool:
        return self._created_flag(f"api-role:{sa}:{api}")

    def ensure_secret_slot(self, project, name) -> bool:
        return self._created_flag(f"secret-slot:{project}:{name}")

    def grant_secret_accessor(self, sa, secret_name) -> bool:
        return self._created_flag(f"secret-accessor:{sa}:{secret_name}")

    def is_populated(self, name) -> bool:
        return name in self.populated

    def provision_db_service(self, slug, db_extensions, postgis_base) -> str:
        # Returns the synthetic service id (a str, like ensure_project/ensure_sa). The create-or-get
        # idempotency flag is registered ONCE, in the steps layer (steps.py provision_db_service), NOT
        # here — self-registering here AND in steps would make the steps-layer read always-False (c1).
        return f"mock-db-{slug}"

    def provision_serving_service(self, slug) -> str:
        # Same as provision_db_service: the _created_flag is the steps layer's sole responsibility (c1).
        return f"mock-serving-{slug}"

    def set_railway_var(self, service, name, source_slot=None) -> bool:
        return self._created_flag(f"serving-var:{service}:{name}")

    def apply_db_extension(self, db_service, ext) -> bool:
        return self._created_flag(f"db-ext:{db_service}:{ext}")

    def select_base_image(self, needs_postgis_base) -> str:
        return "mock-image-postgis" if needs_postgis_base else "mock-image-plain"

    def stand_up_mesh_shape(self, slug) -> MeshShape:
        return MeshShape(
            builder_slug=slug,
            socket_mode="0600",
            transport="af_unix",
            identity_header="Tailscale-User-Login",
            deny_by_default=True,
            operators_env="<BUILDER>_OPERATORS",
            operators_group="group:operators",
            funnel_off=True,
            routes=("health", "<VERB>"),
            verb_placeholder="<VERB>",
            client_template=_T1_CLIENT_TEMPLATE,
        )
