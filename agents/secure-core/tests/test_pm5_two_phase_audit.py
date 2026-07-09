# author: Denson Smith
# ticket: stoa--q7f (u--9s2 Phase-1 increment 2.4)
# seat-built-by: CAPTAIN_ADA_the_stoa (EXECUTOR)
# design-ground-truth: rev2 §1.5 P-M5 (crash-point moved r4) + rev4 §2.5 (INTENT carries lane; value-free)
#                       + §5.2 M5 row. Threat M5: audit gap.
#
# P-M5: (a) each ok/rejected/forbidden/rate_limited call produces an INTENT + matching OUTCOME; a crash in
# the window AFTER egress, BEFORE the outcome write leaves the DURABLE INTENT on disk (the executed
# credentialed call is recorded even though it never completed). (b) NO record carries a param VALUE or a
# credential; params_digest is present, fixed-width, and not reversible; the INTENT carries `lane`.

from __future__ import annotations

import json

import pytest

from secure_core.audit import AuditLog
from secure_core.handler import handle_call
from secure_core.egress import EgressRecorder

from conftest import science_headers, newswire_headers, legit_recorder

SENTINEL_PARAM = "SENSITIVE_PARAM_VALUE_QQQ"


def _gen_call(core, headers, audit, params=None, rec=None, hook=None):
    return handle_call(core, headers,
                       {"provider": "vertex", "operation": "generate_grounded", "skill_id": "gsearch",
                        "params": params if params is not None else {"contents": []}},
                       egress_fn=rec if rec is not None else legit_recorder(), audit=audit,
                       after_egress_hook=hook)


# ---- (a) every terminal state gets INTENT + OUTCOME ----------------------------------------------
def test_pm5a_ok_call_has_intent_and_outcome(core, tmp_path):
    audit = AuditLog(path=str(tmp_path / "a.log"))
    res = _gen_call(core, science_headers(), audit)
    assert res.outcome == "ok"
    assert audit.has_intent(res.audit_id) and audit.has_outcome(res.audit_id)


def test_pm5a_forbidden_call_has_intent_and_terminal_outcome(core, tmp_path):
    audit = AuditLog(path=str(tmp_path / "a.log"))
    res = _gen_call(core, newswire_headers(), audit)  # cross-lane -> forbidden
    assert res.outcome == "forbidden"
    assert audit.has_intent(res.audit_id) and audit.has_outcome(res.audit_id)


# ---- (a) crash in egress->outcome window: DURABLE INTENT survives on disk -------------------------
def test_pm5a_crash_after_egress_before_outcome_leaves_intent(core, tmp_path):
    """Crash-inject AFTER egress, BEFORE the outcome write. The executed credentialed call's INTENT record
    is DURABLE on disk; the OUTCOME is absent (the window). No executed call is ever unrecorded."""
    log_path = tmp_path / "audit.log"
    audit = AuditLog(path=str(log_path))
    captured = {}

    def crash(audit_id):
        captured["id"] = audit_id
        raise RuntimeError("simulated crash in the egress->outcome window")

    rec = legit_recorder()
    with pytest.raises(RuntimeError, match="simulated crash"):
        _gen_call(core, science_headers(), audit, rec=rec, hook=crash)

    # the egress DID happen (the executed credentialed call)
    assert rec.hosts, "egress should have occurred before the crash"
    # re-read the DURABLE on-disk log (as a fresh process would after a crash)
    lines = [json.loads(l) for l in log_path.read_text(encoding="utf-8").splitlines()]
    audit_id = captured["id"]
    intents = [r for r in lines if r["phase"] == "intent" and r["audit_id"] == audit_id]
    outcomes = [r for r in lines if r["phase"] == "outcome" and r["audit_id"] == audit_id]
    assert len(intents) == 1, "the executed call's INTENT must be durable on disk"
    assert outcomes == [], "the OUTCOME was in the crash window — absent, proving the window is real"
    assert intents[0]["lane"] == "lane:science"


# ---- (b) value-free: no param value / credential; params_digest present + irreversible ------------
def test_pm5b_records_are_value_free_and_digest_is_irreversible(core, tmp_path):
    log_path = tmp_path / "audit.log"
    audit = AuditLog(path=str(log_path))
    res = _gen_call(core, science_headers(), audit, params={"contents": [SENTINEL_PARAM]})
    blob = log_path.read_text(encoding="utf-8")
    assert SENTINEL_PARAM not in blob, "a param VALUE must never appear in an audit record"
    intent = audit.intents()[-1]
    digest = intent["params_digest"]
    assert isinstance(digest, str) and len(digest) == 64 and all(c in "0123456789abcdef" for c in digest)
    assert SENTINEL_PARAM not in digest  # one-way; not reversible to the value


def test_pm5b_audit_record_rejects_a_value_channel():
    """The value-free guard refuses any record carrying an undeclared key (a value channel)."""
    from secure_core.audit import assert_record_value_free
    with pytest.raises(ValueError, match="value-free violation"):
        assert_record_value_free({"phase": "intent", "audit_id": "x", "param_value": "leak"})
