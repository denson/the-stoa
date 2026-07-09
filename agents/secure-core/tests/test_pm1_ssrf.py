# author: Denson Smith
# ticket: stoa--q7f (u--9s2 Phase-1 increment 2.4)
# seat-built-by: CAPTAIN_ADA_the_stoa (EXECUTOR)
# design-ground-truth: rev2 §1.5 P-M1 (rewritten r1 — asserts the CROSS-REGISTRY INVARIANT, not one
#                       injection) + rev4 §5.2 M1 row. Threat M1: SSRF / forward-anything egress.
#
# P-M1 falsifies a build that could construct a caller-steered destination. (a) STRUCTURAL: every url_slot
# FIXED/ENUM, disjointness, redirect-OFF, loader REFUSES a planted violating op. (b) INSTANCE: a caller
# params.url/params.project/extra-key -> 400 ZERO egress; a 3xx-to-attacker NOT followed. (c) LEGIT: a real
# call reaches ONLY the pinned host.

from __future__ import annotations

import pytest

from secure_core.slots import FIXED, ENUM
from secure_core.registry import load_registry, default_provider_registry, _template_names
from secure_core.errors import LoaderError
from secure_core.handler import handle_call
from secure_core.egress import EgressRecorder, EgressResponse

from conftest import science_headers, legit_recorder, PINNED_GEN_HOST


# ---- (a) STRUCTURAL — the cross-registry invariant ------------------------------------------------
def test_pm1a_every_url_slot_is_fixed_or_enum_and_disjoint():
    reg = default_provider_registry()
    for pname, prov in reg.items():
        for oname, op in prov["operations"].items():
            for sname, sval in op["url_slots"].items():
                assert isinstance(sval, (FIXED, ENUM)), f"{pname}.{oname}.{sname} is not FIXED/ENUM"
            names = _template_names(op["url"])
            # every template name is a declared url_slot; none is a param_schema key (disjointness).
            assert names <= set(op["url_slots"]), f"{pname}.{oname}: dangling url name"
            assert not (names & set(op["param_schema"])), f"{pname}.{oname}: param name in destination"
            assert not (set(op["url_slots"]) & set(op["param_schema"])), f"{pname}.{oname}: namespaces overlap"


def test_pm1a_egress_client_has_redirect_following_off():
    from secure_core.egress import _NoRedirect
    import urllib.request
    # the NoRedirect handler returns None from redirect_request (do not follow) — SSRF-via-redirect closed.
    h = _NoRedirect()
    assert h.redirect_request(None, None, 302, "Found", {}, "http://attacker.example") is None
    assert issubclass(_NoRedirect, urllib.request.HTTPRedirectHandler)


def test_pm1a_loader_refuses_a_free_form_url_slot():
    """A url_slot whose value is a plain str (a free-form host) is an INV-DEST violation -> refuse to serve."""
    reg = default_provider_registry()
    reg["vertex"]["operations"]["generate_grounded"]["url_slots"]["location"] = "attacker-controlled"  # free-form
    with pytest.raises(LoaderError, match="INV-DEST"):
        load_registry(provider_registry=reg)


def test_pm1a_loader_refuses_a_params_derived_destination():
    """A url template referencing a param_schema key (a params-derived host) -> refuse to serve."""
    reg = default_provider_registry()
    op = reg["vertex"]["operations"]["embed"]
    op["url"] = "https://{host}-aiplatform.googleapis.com/v1/predict"
    op["url_slots"]["host"] = ENUM(["us-central1"])
    op["param_schema"] = {"instances": list, "host": str}  # host now ALSO a param key -> disjointness broken
    with pytest.raises(LoaderError, match="INV-DEST"):
        load_registry(provider_registry=reg)


# ---- (b) INSTANCE — a caller cannot steer the destination ----------------------------------------
@pytest.mark.parametrize("bad_params", [
    {"url": "http://169.254.169.254/latest/meta-data/"},   # a caller URL
    {"project": "169.254.169.254"},                        # try to override the FIXED project slot via params
    {"contents": [], "endpoint": "http://attacker.example"},  # an extra undeclared key
])
def test_pm1b_caller_destination_input_is_rejected_zero_egress(core, audit, bad_params):
    rec = EgressRecorder()
    result = handle_call(core, science_headers(),
                         {"provider": "vertex", "operation": "generate_grounded",
                          "skill_id": "gsearch", "params": bad_params},
                         egress_fn=rec, audit=audit)
    assert result.status == 400, result
    assert result.egressed is False
    assert rec.hosts == [], "a rejected call must NOT egress to any host"


def test_pm1b_redirect_to_attacker_is_not_followed(core, audit):
    """A 3xx from the (mock) upstream is returned as provider_error and the attacker host is NEVER
    contacted (redirect-OFF)."""
    rec = EgressRecorder()
    rec.set_response(PINNED_GEN_HOST, EgressResponse(status=302, body={},
                                                     redirected_to="http://attacker.example/exfil"))
    result = handle_call(core, science_headers(),
                         {"provider": "vertex", "operation": "generate_grounded",
                          "skill_id": "gsearch", "params": {"contents": []}},
                         egress_fn=rec, audit=audit)
    assert result.status == 502
    assert result.outcome == "provider_error"
    assert rec.hosts == [PINNED_GEN_HOST], "the redirect Location must NOT have been followed"
    assert "attacker.example" not in rec.hosts


# ---- (c) LEGIT — the real call reaches ONLY the pinned host --------------------------------------
def test_pm1c_legit_call_reaches_only_pinned_host(core, audit):
    rec = legit_recorder()
    result = handle_call(core, science_headers(),
                         {"provider": "vertex", "operation": "generate_grounded",
                          "skill_id": "gsearch", "params": {"contents": []}},
                         egress_fn=rec, audit=audit)
    assert result.status == 200
    assert rec.hosts == [PINNED_GEN_HOST]
