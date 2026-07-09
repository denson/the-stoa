# author: Denson Smith
# ticket: stoa--q7f (u--9s2 Phase-1 increment 2.4)
# seat-built-by: CAPTAIN_ADA_the_stoa (EXECUTOR)
# design-ground-truth: rev2 §1.4.4 (M6) + rev4 §2.5 — per-lane (per-tag = per-identity) token bucket is the
#                       SECURITY boundary; one lane cannot exhaust another lane's bucket. Optional per-
#                       (identity, skill_id) sub-bucket for intra-lane fairness.
#
# A deterministic token-bucket rate limiter, keyed per-IDENTITY (the lane cap / operator login). The per-
# identity bucket is the hard security limit regardless of sub-bucketing (a hostile skill_id cannot exceed
# its identity's bucket). Clock-injectable for deterministic probes.

from __future__ import annotations

import time


class _Bucket:
    def __init__(self, capacity: int, refill_per_sec: float, clock):
        self.capacity = capacity
        self.refill_per_sec = refill_per_sec
        self._tokens = float(capacity)
        self._last = clock()
        self._clock = clock

    def take(self) -> bool:
        now = self._clock()
        elapsed = now - self._last
        self._last = now
        self._tokens = min(self.capacity, self._tokens + elapsed * self.refill_per_sec)
        if self._tokens >= 1.0:
            self._tokens -= 1.0
            return True
        return False


class RateLimiter:
    """Per-identity token bucket. `identity` is the per-lane key (the cap for a lane, the login for an
    operator). An optional per-(identity, skill_id) sub-bucket is enabled by passing sub_capacity; the
    per-identity bucket ALWAYS applies first as the security boundary."""

    def __init__(
        self,
        capacity: int = 5,
        refill_per_sec: float = 0.0,
        sub_capacity: int | None = None,
        sub_refill_per_sec: float = 0.0,
        clock=time.monotonic,
    ):
        self.capacity = capacity
        self.refill_per_sec = refill_per_sec
        self.sub_capacity = sub_capacity
        self.sub_refill_per_sec = sub_refill_per_sec
        self._clock = clock
        self._buckets: dict[str, _Bucket] = {}
        self._sub: dict[tuple, _Bucket] = {}

    def allow(self, identity: str, skill_id: str | None = None) -> bool:
        """True if the call is admitted; False -> 429 rate_limited. The per-identity bucket is checked
        FIRST (the security boundary); the optional sub-bucket only adds intra-identity fairness and never
        widens the per-identity limit."""
        bucket = self._buckets.get(identity)
        if bucket is None:
            bucket = _Bucket(self.capacity, self.refill_per_sec, self._clock)
            self._buckets[identity] = bucket
        if not bucket.take():
            return False
        if self.sub_capacity is not None and skill_id is not None:
            key = (identity, skill_id)
            sub = self._sub.get(key)
            if sub is None:
                sub = _Bucket(self.sub_capacity, self.sub_refill_per_sec, self._clock)
                self._sub[key] = sub
            if not sub.take():
                return False
        return True
