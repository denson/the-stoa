# author: Denson Smith
# ticket: stoa--q7f (u--9s2 Phase-1 increment 2.4)
# seat-built-by: CAPTAIN_ADA_the_stoa (EXECUTOR)
# design-ground-truth: rev2 §1.5 P-M2 (broadened r2 — FULL Vertex response surface) + rev4 §5.2 M2 row +
#                       design-rev6.md §5.1a (P-M2 EXTENDED — the recursive NODE grammar):
#                         (a.2) rev5 — credential at depth >= 3 in an UNDECLARED sub-key of a DECLARED OBJECT
#                               field -> DROPPED from caller + BOTH audit phases; a depth-2 build FAILS;
#                         (a.3) rev6 r1 — an object/dict (direct, list-nested, doubly-nested) under a SCALAR
#                               field -> DROPPED; a shallow-SCALAR build FAILS; legit scalar + list-of-scalars pass;
#                         (a.4) rev6 r2 — a NON-allowlisted field marked PASS_WHOLE -> loader REFUSES TO LOAD;
#                               the allowlisted candidates.content PASS_WHOLE loads + passes whole.
#                       Threat M2: key-exfil via response/log.
#
# P-M2: inject a mock credential + Authorization/x-goog-api-key into UNDECLARED response fields/headers at
# each surface (candidate-level, top-level, upstream headers, error body) -> assert the caller-facing output
# contains the value at NONE, the error path returns only {status, provider_error_class}, and the two-phase
# audit records carry the secret in NEITHER intent nor outcome. (b) an op with NO response_schema (and a
# legacy bare-list node, and a mis-placed PASS_WHOLE) refuses to load. (c) LEGIT: a real call returns the
# declared payload intact.

from __future__ import annotations

import copy
import json

import pytest

from secure_core.registry import load_registry, default_provider_registry
from secure_core.errors import LoaderError
from secure_core.handler import handle_call
from secure_core.redact import redact_response, SCALAR, PASS_WHOLE, PASS_WHOLE_ALLOWLIST
from secure_core.egress import EgressRecorder, EgressResponse

from conftest import science_headers, PINNED_GEN_HOST

SECRET = "LEAKED_CREDENTIAL_VALUE_do_not_surface_ZZZ"


def _gen_schema() -> dict:
    """The live generate_grounded response_schema (the recursive NODE grammar), for unit-level redaction +
    falsification assertions against the REAL redact_response."""
    return default_provider_registry()["vertex"]["operations"]["generate_grounded"]["response_schema"]


def _shallow_scalar_ok(value) -> bool:
    """A deliberately-WRONG (NON-CONFORMANT) shallow-SCALAR reference: drops only a TOP-LEVEL dict, but passes
    a list-containing-a-dict. Used to PROVE the P-M2(a.3) probe has teeth — a shallow-SCALAR build emits the
    smuggled object the recursive dict-scan drops."""
    return not isinstance(value, dict)


def _poisoned_body() -> dict:
    """A generate body with the SECRET planted into UNDECLARED fields at every surface."""
    return {
        "candidates": [
            {
                "content": {"role": "model", "parts": [{"text": "answer"}]},
                "finishReason": "STOP",
                "groundingMetadata": {"webSearchQueries": ["q"]},
                "leakedKey": SECRET,               # UNDECLARED candidate subfield
                "Authorization": f"Bearer {SECRET}",  # UNDECLARED (header-shaped) subfield
            }
        ],
        "usageMetadata": {
            "promptTokenCount": 1, "candidatesTokenCount": 2, "totalTokenCount": 3,
            "x-goog-api-key": SECRET,              # UNDECLARED subfield
        },
        "apiKey": SECRET,                          # UNDECLARED top-key
        "modelVersion": "gemini-2.5-flash",
    }


def test_pm2a_undeclared_fields_are_dropped_secret_never_reaches_caller(core, audit):
    rec = EgressRecorder()
    rec.set_response(PINNED_GEN_HOST, EgressResponse(status=200, body=_poisoned_body(),
                                                     headers={"x-goog-api-key": SECRET}))
    result = handle_call(core, science_headers(),
                         {"provider": "vertex", "operation": "generate_grounded",
                          "skill_id": "gsearch", "params": {"contents": []}},
                         egress_fn=rec, audit=audit)
    assert result.status == 200
    out = json.dumps(result.body)
    assert SECRET not in out, "the allow-list must drop every undeclared field carrying the secret"
    # only declared subfields survive
    cand = result.body["candidates"][0]
    assert set(cand.keys()) <= {"content", "finishReason", "groundingMetadata"}
    assert set(result.body["usageMetadata"].keys()) <= {
        "promptTokenCount", "candidatesTokenCount", "totalTokenCount"}
    assert "apiKey" not in result.body and "modelVersion" not in result.body


def test_pm2a_secret_absent_from_both_audit_phases(core, audit):
    rec = EgressRecorder()
    rec.set_response(PINNED_GEN_HOST, EgressResponse(status=200, body=_poisoned_body()))
    handle_call(core, science_headers(),
                {"provider": "vertex", "operation": "generate_grounded",
                 "skill_id": "gsearch", "params": {"contents": []}},
                egress_fn=rec, audit=audit)
    blob = "\n".join(audit.as_log_lines())
    assert SECRET not in blob, "no audit record (intent OR outcome) may carry a credential/body"


def test_pm2a_upstream_error_returns_only_status_and_class(core, audit):
    """An upstream error body carrying the secret is returned as {status, provider_error_class} ONLY."""
    rec = EgressRecorder()
    rec.set_response(PINNED_GEN_HOST, EgressResponse(status=500, body={"error": SECRET, "trace": SECRET}))
    result = handle_call(core, science_headers(),
                         {"provider": "vertex", "operation": "generate_grounded",
                          "skill_id": "gsearch", "params": {"contents": []}},
                         egress_fn=rec, audit=audit)
    assert result.status == 502
    assert set(result.body.keys()) == {"status", "provider_error_class"}
    assert SECRET not in json.dumps(result.body)


def test_pm2b_op_with_no_response_schema_refuses_to_load():
    reg = default_provider_registry()
    del reg["vertex"]["operations"]["embed"]["response_schema"]  # opaque pass-through
    with pytest.raises(LoaderError, match="INV-RESP"):
        load_registry(provider_registry=reg)


def test_pm2c_legit_call_returns_declared_fields_intact(core, audit):
    from conftest import legit_recorder
    rec = legit_recorder()
    result = handle_call(core, science_headers(),
                         {"provider": "vertex", "operation": "generate_grounded",
                          "skill_id": "gsearch", "params": {"contents": []}},
                         egress_fn=rec, audit=audit)
    assert result.status == 200
    assert result.body["candidates"][0]["finishReason"] == "STOP"
    assert result.body["usageMetadata"]["totalTokenCount"] == 30


# --------------------------------------------------------------------------------------------------------
# P-M2(a.2) — NESTED-DECLARED-FIELD (rev5): a credential at depth >= 3 in an UNDECLARED sub-key of a DECLARED
# OBJECT field is DROPPED from the caller AND absent from BOTH audit phases. A depth-2 build (which whole-
# passes groundingMetadata's value) EMITS the planted value -> FAILS this clause.
# --------------------------------------------------------------------------------------------------------

def _nested_declared_poison_body() -> dict:
    """A generate body with the SECRET planted at depth >= 3 in UNDECLARED sub-keys of the DECLARED, RECURSED
    groundingMetadata OBJECT field (and one level deeper, under the declared retrievalMetadata OBJECT)."""
    return {
        "candidates": [
            {
                "content": {"role": "model", "parts": [{"text": "answer"}]},
                "finishReason": "STOP",
                "groundingMetadata": {
                    "webSearchQueries": ["q"],                 # declared SCALAR -> kept
                    "leaked_bearer": SECRET,                   # UNDECLARED depth-3 sub-key -> DROPPED
                    "retrievalMetadata": {                     # declared OBJECT -> recursed
                        "webSearchQueries": ["q2"],            # declared SCALAR -> kept
                        "leaked": SECRET,                      # UNDECLARED depth-4 sub-key -> DROPPED
                    },
                },
            }
        ],
        "usageMetadata": {"promptTokenCount": 1, "candidatesTokenCount": 2, "totalTokenCount": 3},
    }


def test_pm2a2_nested_declared_field_credential_dropped_from_caller(core, audit):
    rec = EgressRecorder()
    rec.set_response(PINNED_GEN_HOST, EgressResponse(status=200, body=_nested_declared_poison_body()))
    result = handle_call(core, science_headers(),
                         {"provider": "vertex", "operation": "generate_grounded",
                          "skill_id": "gsearch", "params": {"contents": []}},
                         egress_fn=rec, audit=audit)
    assert result.status == 200
    assert SECRET not in json.dumps(result.body), \
        "a credential at depth >= 3 in an undeclared sub-key of a declared field must be dropped (a depth-2 " \
        "build whole-passes groundingMetadata and FAILS here)"
    gm = result.body["candidates"][0]["groundingMetadata"]
    assert gm["webSearchQueries"] == ["q"]                    # declared nested SCALAR intact
    assert "leaked_bearer" not in gm                          # undeclared depth-3 dropped
    assert gm["retrievalMetadata"]["webSearchQueries"] == ["q2"]
    assert "leaked" not in gm["retrievalMetadata"]            # undeclared depth-4 dropped


def test_pm2a2_nested_declared_field_credential_absent_from_both_audit_phases(core, audit):
    rec = EgressRecorder()
    rec.set_response(PINNED_GEN_HOST, EgressResponse(status=200, body=_nested_declared_poison_body()))
    handle_call(core, science_headers(),
                {"provider": "vertex", "operation": "generate_grounded",
                 "skill_id": "gsearch", "params": {"contents": []}},
                egress_fn=rec, audit=audit)
    blob = "\n".join(audit.as_log_lines())
    assert SECRET not in blob, "no audit record (intent OR outcome) may carry a nested-declared credential"


def test_pm2a2_probe_has_teeth_depth2_build_would_emit(core):
    """Falsification: a depth-2 (whole-pass the declared sub-key value) redactor EMITS the planted secret."""
    body = _nested_declared_poison_body()
    depth2 = {  # emulate the legacy depth-2 allow-list: keep declared sub-keys, pass each value WHOLE
        "candidates": [
            {k: v for k, v in body["candidates"][0].items()
             if k in {"content", "finishReason", "groundingMetadata"}}
        ]
    }
    assert SECRET in json.dumps(depth2), "the depth-2 form leaks — so the recursive assertion above has teeth"


# --------------------------------------------------------------------------------------------------------
# P-M2(a.3) — SCALAR-SLOT OBJECT SMUGGLE (rev6 r1): an object/dict carrying a credential-shaped value under a
# SCALAR-declared field — DIRECT, LIST-NESTED, and DOUBLY-NESTED — is DROPPED (the recursive dict-scan drops
# the whole object-bearing value). A shallow-SCALAR build (drops only a top-level dict, passes a list-
# containing-a-dict) EMITS the list-nested case -> FAILS this clause. Legit scalar + list-of-scalars pass.
# --------------------------------------------------------------------------------------------------------

def _scalar_slot_smuggle_body() -> dict:
    """SECRET smuggled inside objects placed UNDER SCALAR-declared fields, three ways."""
    return {
        "candidates": [
            {
                "content": {"role": "model", "parts": [{"text": "answer"}]},
                "finishReason": {"leaked_bearer": SECRET},     # DIRECT dict under a SCALAR field -> DROP whole
                "groundingMetadata": {
                    # LIST-NESTED dict under a SCALAR field -> DROP the whole value
                    "webSearchQueries": ["ok", {"leaked_bearer": SECRET}],
                    # DOUBLY-NESTED dict under a SCALAR field -> DROP the whole value
                    "retrievalQueries": [["ok", {"leaked_bearer": SECRET}]],
                },
            }
        ],
        "usageMetadata": {"promptTokenCount": 1, "candidatesTokenCount": 2, "totalTokenCount": 3},
    }


def test_pm2a3_scalar_slot_object_smuggle_dropped_from_caller(core, audit):
    rec = EgressRecorder()
    rec.set_response(PINNED_GEN_HOST, EgressResponse(status=200, body=_scalar_slot_smuggle_body()))
    result = handle_call(core, science_headers(),
                         {"provider": "vertex", "operation": "generate_grounded",
                          "skill_id": "gsearch", "params": {"contents": []}},
                         egress_fn=rec, audit=audit)
    assert result.status == 200
    assert SECRET not in json.dumps(result.body), \
        "a dict smuggled under a SCALAR field (direct/list-nested/doubly-nested) must be dropped whole"
    cand = result.body["candidates"][0]
    assert "finishReason" not in cand                         # direct dict -> whole value dropped
    gm = cand["groundingMetadata"]
    assert "webSearchQueries" not in gm                       # list-nested dict -> whole value dropped
    assert "retrievalQueries" not in gm                       # doubly-nested dict -> whole value dropped


def test_pm2a3_scalar_slot_object_smuggle_absent_from_both_audit_phases(core, audit):
    rec = EgressRecorder()
    rec.set_response(PINNED_GEN_HOST, EgressResponse(status=200, body=_scalar_slot_smuggle_body()))
    handle_call(core, science_headers(),
                {"provider": "vertex", "operation": "generate_grounded",
                 "skill_id": "gsearch", "params": {"contents": []}},
                egress_fn=rec, audit=audit)
    blob = "\n".join(audit.as_log_lines())
    assert SECRET not in blob, "no audit record may carry a SCALAR-slot-smuggled credential"


def test_pm2a3_shallow_scalar_build_FAILS_the_list_nested_case():
    """Falsification with teeth: a SHALLOW-SCALAR build EMITS the list-nested smuggled dict; the REAL recursive
    dict-scan DROPS it. This is the exact discriminating case the design names."""
    list_nested = ["ok", {"leaked_bearer": SECRET}]
    # shallow-SCALAR: top-level is a list (not a dict) -> passes the WHOLE list, leaking the nested dict
    assert _shallow_scalar_ok(list_nested) is True
    assert SECRET in json.dumps(list_nested)
    # REAL recursive redactor: the SCALAR node drops the whole value (a mapping is present at depth 2)
    schema = {"webSearchQueries": SCALAR}
    out = redact_response(schema, {"webSearchQueries": list_nested})
    assert "webSearchQueries" not in out
    assert SECRET not in json.dumps(out)


def test_pm2a3_legit_scalar_and_list_of_scalars_pass_intact():
    """(b) legit-unaffected: the recursive dict-scan does NOT over-drop clean scalar / array-of-scalar values."""
    schema = {"finishReason": SCALAR, "webSearchQueries": SCALAR}
    body = {"finishReason": "STOP", "webSearchQueries": ["alpha", "beta", "gamma"]}
    out = redact_response(schema, body)
    assert out["finishReason"] == "STOP"
    assert out["webSearchQueries"] == ["alpha", "beta", "gamma"]


# --------------------------------------------------------------------------------------------------------
# P-M2(a.4) — PASS_WHOLE MIS-PLACEMENT (rev6 r2): a response_schema marking a NON-allowlisted field
# PASS_WHOLE -> the loader REFUSES TO LOAD (fail-CLOSED at load). A node-types-only loader would load it. The
# allowlisted candidates.content PASS_WHOLE loads + passes whole. The legacy bare-list node also refuses.
# --------------------------------------------------------------------------------------------------------

def test_pm2a4_non_allowlisted_pass_whole_refuses_to_load():
    reg = copy.deepcopy(default_provider_registry())
    # mark a NON-allowlisted field (candidates.finishReason) PASS_WHOLE — well-typed as a node, but a
    # placement violation. A node-types-only loader would accept it; the placement guard REFUSES it.
    reg["vertex"]["operations"]["generate_grounded"]["response_schema"]["candidates"]["finishReason"] = PASS_WHOLE
    with pytest.raises(LoaderError, match="PASS_WHOLE"):
        load_registry(provider_registry=reg)


def test_pm2a4_legacy_bare_list_node_refuses_to_load():
    reg = copy.deepcopy(default_provider_registry())
    # revert one op to the legacy depth-2 bare-list form -> refuse to load (regression fails closed at LOAD)
    reg["vertex"]["operations"]["embed"]["response_schema"] = {"predictions": ["embeddings"]}
    with pytest.raises(LoaderError, match="INV-RESP"):
        load_registry(provider_registry=reg)


def test_pm2a4_allowlisted_content_pass_whole_loads_and_passes_whole(core, audit):
    # (b) legit: candidates.content IS in the allowlist -> the default registry loads (the `core` fixture is
    # proof), and content passes WHOLE (the model product is not truncated).
    assert "candidates.content" in PASS_WHOLE_ALLOWLIST
    from conftest import legit_recorder
    rec = legit_recorder()
    result = handle_call(core, science_headers(),
                         {"provider": "vertex", "operation": "generate_grounded",
                          "skill_id": "gsearch", "params": {"contents": []}},
                         egress_fn=rec, audit=audit)
    assert result.status == 200
    # content passed whole (nested parts structure intact — NOT truncated by the recursion)
    assert result.body["candidates"][0]["content"] == {"role": "model", "parts": [{"text": "grounded answer"}]}
