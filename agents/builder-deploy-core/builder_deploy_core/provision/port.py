# author: Denson Smith
# ticket: stoa--k48 (u--9s2 Phase-2 increment 2.3 — provisioning choreography)
# seat-built-by: CAPTAIN_ADA_the_stoa (EXECUTOR)
# design-ground-truth: agents/design/stoa--k48/design-rev2.md §3.1 (StepStatus/StepAction) / §4.3 (the
#                       Provisioner ABC — W2) / §6 (MeshShape) / §15.3 (r3/r5 ABC-contract closure)
#
# The abstract provisioning PORT (W2) + the value-free StepAction/StepStatus surface. The engine drives
# THIS port, never a CLI. The ONLY concrete subclass that ships is MockProvisioner (mock.py). A real
# applier would be a NEW concrete subclass that does I/O — it does not exist in the package and would be
# a code-review-visible addition. NO method on this port takes or returns a credential VALUE: the port
# is value-free by TYPE (is_populated -> bool; set_railway_var names a source SLOT; select_base_image
# returns a value-free image tag). This module imports stdlib abc/enum/dataclasses/typing ONLY (W1).

from __future__ import annotations

import abc
import enum
from dataclasses import dataclass, field
from typing import Optional


class ValueLeakError(Exception):
    """HW-1 / DoD#3 — a ProvisioningSpec / RunLedger / StepAction / mock-state leaf holds something
    other than a known value-free leaf (a NAME, slot-ref, slug, api id, boolean, enum). Raised by
    spec.assert_value_free. Homed in provision/ (NOT the frozen errors.py) so the frozen module stays
    byte-unchanged. There are no values in the system to leak (emit is pure; the mock never holds one) —
    this exception is the structural assertion that the surface CANNOT become a value channel."""


class StepStatus(enum.Enum):
    OK = "ok"            # action emitted/created (or create-or-get returned existing)
    BLOCKED = "blocked"  # S2c — slot unpopulated; halts before S3/S5 (fail-closed human gate)
    FAILED = "failed"    # a provisioner action raised (fail_at) — aborts the remainder
    SKIPPED = "skipped"  # idempotent re-run: create-or-get returned existing, no new create


@dataclass(frozen=True)
class StepAction:
    """A single value-free choreography action. Frozen so the ledger is immutable + hashable +
    comparable for golden-file equality. EVERY field is value-free by construction."""

    step: str                  # "S0".."S6" — the step index (ledger monotonicity keys on this)
    op: str                    # the port verb dispatched (CANONICAL vocab = the §4.3 ABC @abstractmethod
                               #   names + the engine-level S6 pseudo-op "verify"; §3.1/§15.3). There is
                               #   NO "require_population" op and NO "verify_*" port method.
    target: str                # the NAME the op acts on: a slug / api id / SLOT NAME / var NAME /
                               #   extension / service. NEVER a value (this is the grep surface).
    status: StepStatus
    # value-free structured detail as (key, name-ref) pairs ONLY — closed leaf shape assert_value_free
    # walks. e.g. (("source_slot","MAPS_API_KEY"),) ; (("sa","sa-prospector"),("secret","MAPS_API_KEY")).
    detail: tuple[tuple[str, str], ...] = ()
    created: bool = True       # False on an idempotent re-run create-or-get (§4 idempotency)


@dataclass(frozen=True)
class MeshShape:
    """The §6/§7 T1 SHAPE descriptor stand_up_mesh_shape returns — a value-free SCAFFOLD spec, not a
    credential. Carries the policy flags + the CLI-client template text + the <VERB> placeholder + the
    generic health route. Domain-EMPTY: zero domain verbs."""

    builder_slug: str
    socket_mode: str           # "0600" — the AF_UNIX UDS file-permission mode
    transport: str             # "af_unix" — loopback/UDS only (no public ingress)
    identity_header: str       # "Tailscale-User-Login" — serve-injected header trust (never WhoIs-on-loopback)
    deny_by_default: bool      # True — policy default-deny
    operators_env: str         # "<BUILDER>_OPERATORS" — the operator allowlist env var (template form)
    operators_group: str       # "group:operators"
    funnel_off: bool           # True — no public ingress
    routes: tuple[str, ...]    # the ONLY concrete route is "health"; the domain endpoint is "<VERB>"
    verb_placeholder: str      # "<VERB>" — the domain endpoint stub token (501-until-T3)
    client_template: str       # the CLI-client-skill template text (counts-only contract, --check door-probe)


class Provisioner(abc.ABC):
    """The abstract provisioning port. The engine drives THIS, never a CLI. The ONLY concrete subclass
    that ships is MockProvisioner (W2). A real applier would be a NEW concrete subclass that does I/O —
    which does not exist in the package and would be a code-review-visible addition.

    CONTRACT (W2 + r3): every verb a §4.5 step dispatches is an @abstractmethod here. The S6 verify is
    engine-level (the choreographer re-reads its own ledger), NOT a port call, so it is deliberately not
    declared. The ABC forces MockProvisioner to implement every dispatched verb, so an undeclared/
    unimplemented port verb is an import-time TypeError (cannot instantiate the mock), not a latent S4
    AttributeError. No method takes or returns a credential value (value-free by type)."""

    @abc.abstractmethod
    def ensure_project(self, slug) -> str: ...

    @abc.abstractmethod
    def ensure_sa(self, slug, project) -> str: ...

    @abc.abstractmethod
    def set_budget_boundary(self, slug, project) -> None: ...

    @abc.abstractmethod
    def enable_api(self, project, api) -> bool: ...          # returns created (False = already enabled)

    @abc.abstractmethod
    def grant_api_role(self, sa, api) -> bool: ...

    @abc.abstractmethod
    def ensure_secret_slot(self, project, name) -> bool: ...      # slot only, NO value

    @abc.abstractmethod
    def grant_secret_accessor(self, sa, secret_name) -> bool: ...  # per-secret, never project-wide

    @abc.abstractmethod
    def is_populated(self, name) -> bool: ...                # the S2c gate read — a BOOLEAN, never a value

    @abc.abstractmethod
    def provision_db_service(self, slug, db_extensions, postgis_base) -> str: ...

    @abc.abstractmethod
    def provision_serving_service(self, slug) -> str: ...

    @abc.abstractmethod
    def set_railway_var(self, service, name, source_slot: Optional[str] = None) -> bool: ...
    #   names a SOURCE slot, never a value

    @abc.abstractmethod
    def apply_db_extension(self, db_service, ext) -> bool: ...

    @abc.abstractmethod
    def select_base_image(self, needs_postgis_base) -> str: ...   # r3 ADDED — S4 dispatches it (§4.5);
    #   returns a value-free base-image TAG/ref, e.g. "base-postgis" | "base-plain"

    @abc.abstractmethod
    def stand_up_mesh_shape(self, slug) -> MeshShape: ...   # the §7 T1 SHAPE; value-free descriptor
