# author: Denson Smith
# ticket: stoa--k48 (u--9s2 Phase-2 increment 2.3 — provisioning choreography)
# seat-built-by: CAPTAIN_ADA_the_stoa (EXECUTOR)
# design-ground-truth: agents/design/stoa--k48/design-rev2.md §2 (module structure — the re-export list)
#
# The provision sub-package public surface. Re-exports the buildable contracts so callers do
# `from builder_deploy_core.provision import emit_spec, Choreographer, MockProvisioner, ...`. Imports
# only builder_deploy_core.* + stdlib (W1). The ONLY concrete port re-exported is MockProvisioner.

from __future__ import annotations

from builder_deploy_core.provision.port import (
    MeshShape,
    Provisioner,
    StepAction,
    StepStatus,
    ValueLeakError,
)
from builder_deploy_core.provision.spec import (
    ProvisioningSpec,
    SlotSpec,
    assert_value_free,
    emit_spec,
)
from builder_deploy_core.provision.choreographer import Choreographer, RunLedger
from builder_deploy_core.provision.mock import MockProvisioner, MockProvisionerFailure
from builder_deploy_core.provision.checklist import (
    render_checklist,
    render_credential_attestation,
    render_tripwire_attestation,
)
from builder_deploy_core.provision.tripwire import w1_forbidden_tokens

__all__ = [
    "emit_spec",
    "ProvisioningSpec",
    "SlotSpec",
    "assert_value_free",
    "Provisioner",
    "MockProvisioner",
    "MockProvisionerFailure",
    "Choreographer",
    "RunLedger",
    "StepAction",
    "StepStatus",
    "MeshShape",
    "ValueLeakError",
    "render_checklist",
    "render_credential_attestation",
    "render_tripwire_attestation",
    "w1_forbidden_tokens",
]
