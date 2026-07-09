# author: Denson Smith
# ticket: stoa--q7f (u--9s2 Phase-1 increment 2.4)
# seat-built-by: CAPTAIN_ADA_the_stoa (EXECUTOR)
# design-ground-truth: rev2 §1.4.2 (TWO-PHASE audit: value-free INTENT BEFORE egress, OUTCOME AFTER) +
#                       rev4 §2.5 (the INTENT record carries `lane`; a DENIED request is audited `forbidden`
#                       with reason; still value-free — params_digest, never values; no credential; no body).
#
# The two-phase, VALUE-FREE audit log. The INTENT record is written (and flushed durably) BEFORE egress, so
# a crash in the egress->outcome window can never lose the record of an executed credentialed call (P-M5).
# Records hold NAMES / digests / enums ONLY — never a param value, never a credential, never a body.

from __future__ import annotations

import hashlib
import json
import time


def params_digest(params) -> str:
    """A one-way SHA-256 digest of the validated params, for correlation/replay-detection — NEVER the param
    values. Not reversible to the values (P-M5 asserts the raw values do not appear and the digest is a
    fixed-width hex)."""
    canonical = json.dumps(params, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


# The CLOSED set of keys a value-free audit record may carry. If any other key appears, the record became a
# value channel — assert_record_value_free refuses it (belt-and-suspenders on top of the by-construction
# value-freeness).
_INTENT_KEYS = {
    "audit_id", "ts_intent", "phase", "identity_class", "identity", "lane",
    "skill_id", "provider", "operation", "params_digest", "reason",
}
_OUTCOME_KEYS = {"audit_id", "ts_outcome", "phase", "outcome", "upstream_status", "latency_ms"}

# The outcome enum (rev2 §1.4.2).
OUTCOMES = {"ok", "rejected", "forbidden", "provider_error", "rate_limited"}


class AuditLog:
    """An in-memory + optionally file-backed two-phase audit log. When a `path` is given, INTENT records are
    FLUSHED to disk immediately (durable before egress), so a crash in the egress->outcome window leaves the
    INTENT on disk (P-M5)."""

    def __init__(self, path=None, clock=time.time):
        self.records: list[dict] = []
        self._path = path
        self._clock = clock
        if path is not None:
            # Truncate/create the sink so a fresh run starts clean.
            open(path, "w", encoding="utf-8").close()

    # -- phase 1: INTENT (written BEFORE egress) -------------------------------------------------
    def write_intent(
        self,
        audit_id: str,
        identity_class: str,
        identity: str,
        lane,
        skill_id,
        provider,
        operation,
        params,
        reason=None,
    ) -> dict:
        record = {
            "audit_id": audit_id,
            "ts_intent": self._clock(),
            "phase": "intent",
            "identity_class": identity_class,
            "identity": identity,
            "lane": lane if lane is not None else "-",
            "skill_id": skill_id if skill_id is not None else "-",
            "provider": provider if provider is not None else "-",
            "operation": operation if operation is not None else "-",
            "params_digest": params_digest(params) if params is not None else "-",
            "reason": reason if reason is not None else "-",
        }
        assert_record_value_free(record)
        self.records.append(record)
        self._flush(record)  # DURABLE before egress
        return record

    # -- phase 2: OUTCOME (written AFTER egress) --------------------------------------------------
    def write_outcome(self, audit_id: str, outcome: str, upstream_status=None, latency_ms=None) -> dict:
        if outcome not in OUTCOMES:
            raise ValueError(f"unknown audit outcome {outcome!r}")
        record = {
            "audit_id": audit_id,
            "ts_outcome": self._clock(),
            "phase": "outcome",
            "outcome": outcome,
            "upstream_status": upstream_status if upstream_status is not None else "-",
            "latency_ms": latency_ms if latency_ms is not None else "-",
        }
        assert_record_value_free(record)
        self.records.append(record)
        self._flush(record)
        return record

    def _flush(self, record: dict) -> None:
        if self._path is not None:
            with open(self._path, "a", encoding="utf-8") as fh:
                fh.write(json.dumps(record, sort_keys=True) + "\n")
                fh.flush()

    # -- read helpers (probe convenience) --------------------------------------------------------
    def intents(self) -> list[dict]:
        return [r for r in self.records if r.get("phase") == "intent"]

    def outcomes(self) -> list[dict]:
        return [r for r in self.records if r.get("phase") == "outcome"]

    def has_intent(self, audit_id: str) -> bool:
        return any(r["audit_id"] == audit_id for r in self.intents())

    def has_outcome(self, audit_id: str) -> bool:
        return any(r["audit_id"] == audit_id for r in self.outcomes())

    def as_log_lines(self) -> list[str]:
        """The emitted-log view (what seal_audit scans)."""
        return [json.dumps(r, sort_keys=True) for r in self.records]


def assert_record_value_free(record: dict) -> None:
    """Belt-and-suspenders: refuse any audit record that carries a key outside the closed value-free set (a
    param value / credential / body would necessarily arrive under an unexpected key)."""
    phase = record.get("phase")
    allowed = _INTENT_KEYS if phase == "intent" else _OUTCOME_KEYS if phase == "outcome" else None
    if allowed is None:
        raise ValueError(f"audit record has no/unknown phase: {record!r}")
    extra = set(record) - allowed
    if extra:
        raise ValueError(
            f"value-free violation: audit {phase} record carries undeclared key(s) {sorted(extra)} "
            f"(a value channel) — refusing"
        )
