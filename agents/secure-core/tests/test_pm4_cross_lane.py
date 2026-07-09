# author: Denson Smith
# ticket: stoa--q7f (u--9s2 Phase-1 increment 2.4)
# seat-built-by: CAPTAIN_ADA_the_stoa (EXECUTOR)
# design-ground-truth: design-rev4 §2.5 P-M4 EXTENDED (a.1 mapped cross-lane; a.2 NEW unresolvable-principal;
#                       a.3 loader-refuse + multi-cap reject-ambiguous) + §2.1/§2.4 (INV-PRINCIPAL) + §5.2.
#                       Threat M4: over-broad authz -> CROSS-LANE reach.
#
# The load-bearing multi-lane probe. Crucially P-M4(a.2) asserts denial AT RESOLUTION (audit reason
# `no resolvable principal`, denial_stage `resolution`) — the r1-residual VERA hook: a permissive-default
# resolver (`LANE_REGISTRY.get(cap, DEFAULT)` / empty-header->benign-class) would NOT deny at resolution and
# FAILS this probe.

from __future__ import annotations

import pytest

from secure_core.registry import load_registry, default_provider_registry, default_lane_registry
from secure_core.errors import LoaderError, Forbidden
from secure_core.identity import resolve_principal
from secure_core.handler import handle_call
from secure_core.egress import EgressRecorder

from conftest import (
    science_headers, newswire_headers, operator_headers, legit_recorder,
    app_caps_header, SCIENCE_CAP, NEWSWIRE_CAP, UNMAPPED_CAP,
)


def _call(core, headers, audit, operation="generate_grounded", params=None, rec=None):
    rec = rec if rec is not None else EgressRecorder()
    result = handle_call(core, headers,
                         {"provider": "vertex", "operation": operation, "skill_id": "sk",
                          "params": params if params is not None else {"contents": []}},
                         egress_fn=rec, audit=audit)
    return result, rec


# ---- (a.1) MAPPED cross-lane denial --------------------------------------------------------------
def test_pm4_a1_newswire_cannot_call_generate_grounded(core, audit):
    """lane:newswire -> vertex.generate_grounded (scopes operators+lane:science) -> 403, ZERO egress,
    audited forbidden with lane:newswire attributed, denial at the scopes check."""
    result, rec = _call(core, newswire_headers(), audit, operation="generate_grounded")
    assert result.status == 403
    assert result.egressed is False
    assert rec.hosts == []
    assert result.outcome == "forbidden"
    assert result.denial_stage == "scopes"
    intent = audit.intents()[-1]
    assert intent["lane"] == "lane:newswire"
    assert intent["reason"] == "out of scope"
    assert any(o["outcome"] == "forbidden" for o in audit.outcomes())


# ---- (a.2) UNRESOLVABLE-PRINCIPAL denial (NEW r1 — FALSIFIES the permissive-default build) --------
def test_pm4_a2_unmapped_cap_denied_at_resolution(core, audit):
    """An unmapped cap (NOT in LANE_REGISTRY) -> 403, ZERO egress, DENIED AT RESOLUTION with reason
    `no resolvable principal`. A LANE_REGISTRY.get(cap, DEFAULT) build would resolve a default and NOT
    deny here -> it FAILS this assertion."""
    result, rec = _call(core, app_caps_header(UNMAPPED_CAP), audit)
    assert result.status == 403
    assert result.egressed is False
    assert rec.hosts == []
    assert result.denial_stage == "resolution", "denial MUST be observed AT RESOLUTION"
    assert result.reason == "no resolvable principal"
    intent = audit.intents()[-1]
    assert intent["reason"] == "no resolvable principal"  # audited reason = denial at resolution
    assert intent["lane"] == "-"  # no lane resolved (never a default principal)


def test_pm4_a2_absent_header_denied_at_resolution(core, audit):
    """An absent/empty App-Capabilities header with no allowlisted User-Login -> 403 DENIED AT RESOLUTION.
    An empty-header->benign-class build would NOT deny here -> FAILS."""
    for headers in ({}, {"Tailscale-App-Capabilities": ""}, {"Tailscale-User-Login": "unlisted@x.com"}):
        result, rec = _call(core, headers, audit)
        assert result.status == 403, headers
        assert result.egressed is False
        assert rec.hosts == []
        assert result.denial_stage == "resolution", headers
        assert result.reason == "no resolvable principal", headers


def test_pm4_a2_resolve_principal_raises_at_resolution_not_a_default(core):
    """Direct-resolver assertion: resolve_principal RAISES Forbidden at resolution — it never RETURNS a
    default principal for an unmapped cap / absent header."""
    with pytest.raises(Forbidden, match="no resolvable principal"):
        resolve_principal(app_caps_header(UNMAPPED_CAP), core)
    with pytest.raises(Forbidden, match="no resolvable principal"):
        resolve_principal({}, core)


# ---- (a.3) STRUCTURAL loader-refuse + multi-cap reject-ambiguous ----------------------------------
def test_pm4_a3_loader_refuses_unknown_scope_principal():
    reg = default_provider_registry()
    reg["vertex"]["operations"]["embed"]["scopes"].append("lane:ghost")  # unknown principal
    with pytest.raises(LoaderError, match="INV-LANE"):
        load_registry(provider_registry=reg)


def test_pm4_a3_loader_refuses_serve_caps_mismatch():
    """serve --accept-app-caps != LANE_REGISTRY cap set -> refuse to serve (a lane un-served-by-omission
    fails CLOSED at startup)."""
    with pytest.raises(LoaderError, match="INV-LANE"):
        load_registry(accept_app_caps=frozenset({SCIENCE_CAP}))  # newswire cap omitted


def test_pm4_a3_multi_cap_non_registered_rejects_ambiguous(core, audit):
    """A caller whose control-plane caps resolve to >1 lane principal, on a node NOT in MULTI_LANE_NODES ->
    403 reject-ambiguous (never a silent union), denied at resolution."""
    result, rec = _call(core, app_caps_header(SCIENCE_CAP, NEWSWIRE_CAP), audit)
    assert result.status == 403
    assert rec.hosts == []
    assert result.denial_stage == "resolution"
    assert result.reason == "ambiguous multi-lane principal"


# ---- (b) LEGIT — in-scope access unaffected; a registered multi-lane node authorizes --------------
def test_pm4_b_science_generate_and_newswire_embed_authorized(core, audit):
    s_res, _ = _call(core, science_headers(), audit, operation="generate_grounded", rec=legit_recorder())
    assert s_res.status == 200 and s_res.principal == "lane:science"
    n_res, _ = _call(core, newswire_headers(), audit, operation="embed",
                     params={"instances": []}, rec=legit_recorder())
    assert n_res.status == 200 and n_res.principal == "lane:newswire"


def test_pm4_b_registered_multi_lane_node_authorizes():
    """A registered MULTI_LANE_NODES node resolves its declared principal and is authorized for that
    principal's scopes (the r3 tightening did not deny a legitimately-registered multi-lane node)."""
    capset = frozenset({SCIENCE_CAP, NEWSWIRE_CAP})
    core = load_registry(multi_lane_nodes={capset: "lane:science"})
    assert resolve_principal(app_caps_header(SCIENCE_CAP, NEWSWIRE_CAP), core) == "lane:science"
    from secure_core.audit import AuditLog
    result, _ = _call(core, app_caps_header(SCIENCE_CAP, NEWSWIRE_CAP), AuditLog(),
                      operation="generate_grounded", rec=legit_recorder())
    assert result.status == 200 and result.principal == "lane:science"
