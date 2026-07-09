# author: Denson Smith
# ticket: stoa--q7f (u--9s2 Phase-1 increment 2.4)
# seat-built-by: CAPTAIN_ADA_the_stoa (EXECUTOR)
# design-ground-truth: rev2 §1.5 P-M6 + rev4 §2.5 (per-lane bucket is the security boundary; skill_id
#                       attribution + optional sub-bucket) + §5.2 M6 row. Threat M6: quota exhaustion / DoS.
#
# P-M6: (a) one lane bursts > N -> the (N+1)th is 429 rate_limited, audited; (b) a SECOND lane at low rate
# is NOT throttled (per-lane boundary); (c) two skill_ids under the same identity both appear in the audit;
# with the optional sub-bucket enabled, one runaway skill_id is sub-throttled WITHOUT throttling the sibling.

from __future__ import annotations

from secure_core.audit import AuditLog
from secure_core.ratelimit import RateLimiter
from secure_core.handler import handle_call

from conftest import science_headers, newswire_headers, legit_recorder


def _gen(core, headers, audit, rl, skill_id="gsearch", operation="generate_grounded", params=None):
    return handle_call(core, headers,
                       {"provider": "vertex", "operation": operation, "skill_id": skill_id,
                        "params": params if params is not None else {"contents": []}},
                       egress_fn=legit_recorder(), audit=audit, rate_limiter=rl)


def test_pm6a_burst_over_n_is_rate_limited(core):
    audit = AuditLog()
    rl = RateLimiter(capacity=3, refill_per_sec=0.0)  # frozen bucket, capacity 3
    statuses = [_gen(core, science_headers(), audit, rl).status for _ in range(4)]
    assert statuses == [200, 200, 200, 429], statuses
    assert any(o["outcome"] == "rate_limited" for o in audit.outcomes())


def test_pm6b_second_lane_is_not_throttled(core):
    audit = AuditLog()
    rl = RateLimiter(capacity=3, refill_per_sec=0.0)
    # exhaust the science bucket
    for _ in range(3):
        _gen(core, science_headers(), audit, rl)
    assert _gen(core, science_headers(), audit, rl).status == 429  # science throttled
    # newswire (a different tag = a different bucket) calling embed (in scope) is UNAFFECTED
    n = _gen(core, newswire_headers(), audit, rl, skill_id="emb", operation="embed",
             params={"instances": []})
    assert n.status == 200, "a second lane's bucket must be independent"


def test_pm6c_two_skill_ids_both_attributed(core):
    audit = AuditLog()
    rl = RateLimiter(capacity=10, refill_per_sec=0.0)
    _gen(core, science_headers(), audit, rl, skill_id="skill_a")
    _gen(core, science_headers(), audit, rl, skill_id="skill_b")
    skills = {i["skill_id"] for i in audit.intents()}
    assert {"skill_a", "skill_b"} <= skills


def test_pm6c_sub_bucket_throttles_one_skill_not_the_sibling(core):
    """Optional per-(identity, skill_id) sub-bucket: a runaway skill_id is sub-throttled WITHOUT throttling
    a sibling skill under the SAME identity (per-identity capacity is generous; the sub-bucket bites first)."""
    audit = AuditLog()
    rl = RateLimiter(capacity=100, refill_per_sec=0.0, sub_capacity=2, sub_refill_per_sec=0.0)
    runaway = [_gen(core, science_headers(), audit, rl, skill_id="runaway").status for _ in range(3)]
    assert runaway == [200, 200, 429], runaway  # sub-bucket bit at the 3rd
    sibling = _gen(core, science_headers(), audit, rl, skill_id="sibling")
    assert sibling.status == 200, "the sibling skill under the same identity is NOT throttled"
