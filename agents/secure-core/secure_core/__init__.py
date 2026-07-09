# author: Denson Smith
# ticket: stoa--q7f (u--9s2 Phase-1 increment 2.4)
# seat-built-by: CAPTAIN_ADA_the_stoa (EXECUTOR)
#
# secure_core — the CONSOLIDATION secure pass-through core (design-rev4). Public surface re-exported here
# for probe/consumer convenience; the modules are the source of truth.

from __future__ import annotations

from secure_core.errors import (
    Forbidden,
    Rejected,
    RateLimited,
    ProviderError,
    LoaderError,
    BindError,
    SealAuditError,
)
from secure_core.slots import FIXED, ENUM
from secure_core.registry import (
    Core,
    load_registry,
    default_provider_registry,
    default_lane_registry,
    CAP_DOMAIN,
)
from secure_core.identity import resolve_principal, parse_app_capabilities, parse_user_login
from secure_core.handler import handle_call, CallResult
from secure_core.audit import AuditLog
from secure_core.ratelimit import RateLimiter
from secure_core.bind import assert_bind_target_safe, assert_listener_safe
from secure_core.egress import EgressRecorder
from secure_core.sealaudit import seal_audit, SealFinding, FIXTURES_SEGMENT

__all__ = [
    "Forbidden",
    "Rejected",
    "RateLimited",
    "ProviderError",
    "LoaderError",
    "BindError",
    "SealAuditError",
    "FIXED",
    "ENUM",
    "Core",
    "load_registry",
    "default_provider_registry",
    "default_lane_registry",
    "CAP_DOMAIN",
    "resolve_principal",
    "parse_app_capabilities",
    "parse_user_login",
    "handle_call",
    "CallResult",
    "AuditLog",
    "RateLimiter",
    "assert_bind_target_safe",
    "assert_listener_safe",
    "EgressRecorder",
    "seal_audit",
    "SealFinding",
    "FIXTURES_SEGMENT",
]
