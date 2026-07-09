# author: Denson Smith
# ticket: stoa--q7f (u--9s2 Phase-1 increment 2.4)
# seat-built-by: CAPTAIN_ADA_the_stoa (EXECUTOR)
# design-ground-truth: design-rev4.md §2.3 (deny-by-default per-op scopes over lane principals), §2.5
#                       (audit carries lane; denial audited forbidden with reason), §5.3 (the build steps);
#                       rev2 §1.3 (closed request envelope), §1.2.1 (INV-DEST destination construction),
#                       §1.3.1 (INV-RESP redaction), §1.4.2 (two-phase audit), §1.4.4 (rate limit).
#
# The gated request pipeline: validate -> resolve principal (AT RESOLUTION) -> authorize (scopes) ->
# rate-limit -> INTENT (before egress) -> egress -> OUTCOME (after egress) -> allow-list redact. Every
# refusal is fail-loud: 400/403/429 with ZERO egress and a value-free audit record. The pipeline NEVER
# falls through to a permissive default.

from __future__ import annotations

import uuid
from dataclasses import dataclass, field

from secure_core.errors import Forbidden, Rejected
from secure_core.identity import resolve_principal, identity_class_of
from secure_core.redact import redact_response, error_envelope
from secure_core.slots import FIXED


@dataclass
class CallResult:
    status: int                       # HTTP status: 200 / 400 / 403 / 429 / 502
    body: dict                        # the caller-facing body (redacted / error envelope / rejection)
    audit_id: str
    principal: str | None = None
    outcome: str | None = None        # ok | rejected | forbidden | provider_error | rate_limited
    egressed: bool = False            # did an outbound provider call actually leave the box?
    denial_stage: str | None = None   # where a denial occurred: "resolution" | "scopes" | "validation" | "rate_limit"
    reason: str | None = None
    meta: dict = field(default_factory=dict)


def _build_destination(op: dict, slot_selections: dict) -> str:
    """Construct the outbound URL ENTIRELY from server-pinned FIXED/ENUM url_slots (INV-DEST). A FIXED slot
    ignores any caller selection; an ENUM slot resolves to a validated in-set selection or its default. A
    caller selection for a FIXED slot, an unknown slot, or an ENUM value outside the closed set -> Rejected
    (400). `slot_selections` is the closed `slots` envelope field (disjoint from `params`)."""
    url_slots = op["url_slots"]
    for sel_key in slot_selections:
        if sel_key not in url_slots:
            raise Rejected(f"unknown url_slot selection {sel_key!r}")
        if isinstance(url_slots[sel_key], FIXED):
            raise Rejected(f"url_slot {sel_key!r} is FIXED and not caller-selectable")
    resolved: dict[str, str] = {}
    for name, slot in url_slots.items():
        selection = slot_selections.get(name)
        try:
            resolved[name] = slot.resolve(selection)
        except ValueError as exc:
            raise Rejected(str(exc)) from exc
    return op["url"].format(**resolved)


def _validate_params(op: dict, params) -> dict:
    """params MUST validate against the op's CLOSED param_schema (allowed keys + light type check). An
    undeclared key -> 400. params NEVER contributes to the destination (INV-DEST)."""
    if params is None:
        params = {}
    if not isinstance(params, dict):
        raise Rejected("params must be an object")
    schema = op.get("param_schema", {})
    for key, value in params.items():
        if key not in schema:
            raise Rejected(f"undeclared param key {key!r}")
        expected = schema[key]
        if isinstance(expected, type) and not isinstance(value, expected):
            raise Rejected(f"param {key!r} must be {expected.__name__}")
    return params


def handle_call(
    core,
    headers,
    envelope,
    *,
    egress_fn,
    audit,
    rate_limiter=None,
    after_egress_hook=None,
) -> CallResult:
    """Run the full gated pipeline for one POST /call. `envelope` is the parsed request dict
    {provider, operation, skill_id, params, slots?}. `egress_fn(method, url, headers, body) -> EgressResponse`
    is the (mock or real) provider egress. `after_egress_hook` lets a probe crash-inject in the
    egress->outcome window (P-M5)."""
    audit_id = uuid.uuid4().hex

    # -- envelope shape (before anything else) ---------------------------------------------------
    if not isinstance(envelope, dict):
        audit.write_intent(audit_id, "-", "-", None, None, None, None, None, reason="malformed envelope")
        audit.write_outcome(audit_id, "rejected")
        return CallResult(400, {"error": "malformed envelope"}, audit_id, outcome="rejected",
                          denial_stage="validation", reason="malformed envelope")

    provider = envelope.get("provider")
    operation = envelope.get("operation")
    skill_id = envelope.get("skill_id")
    params = envelope.get("params")
    slot_selections = envelope.get("slots") or {}

    # -- 1. resolve principal AT RESOLUTION (INV-PRINCIPAL, r1-residual) --------------------------
    # A denial here is observed AT RESOLUTION: the audited reason is `no resolvable principal` /
    # `ambiguous multi-lane principal`, BEFORE any op lookup or scopes check. This is the exact clause
    # P-M4(a.2) asserts (a permissive-default resolver would NOT reach this denial).
    try:
        principal = resolve_principal(headers, core)
    except Forbidden as f:
        audit.write_intent(audit_id, "-", "-", None, skill_id, provider, operation, None, reason=f.reason)
        audit.write_outcome(audit_id, "forbidden")
        return CallResult(403, {"error": "forbidden", "reason": f.reason}, audit_id, principal=None,
                          outcome="forbidden", egressed=False, denial_stage="resolution", reason=f.reason)

    id_class = identity_class_of(principal)
    lane = principal if id_class == "lane" else None

    # -- 2. skill_id shape (attribution label only; disjoint fence) -------------------------------
    from secure_core.registry import valid_skill_id
    if skill_id is not None and not valid_skill_id(skill_id):
        audit.write_intent(audit_id, id_class, principal, lane, None, provider, operation, None,
                           reason="invalid skill_id")
        audit.write_outcome(audit_id, "rejected")
        return CallResult(400, {"error": "invalid skill_id"}, audit_id, principal=principal,
                          outcome="rejected", denial_stage="validation", reason="invalid skill_id")

    # -- 3. provider/operation resolve to the CLOSED server-side registry -------------------------
    op = core.get_op(provider, operation)
    if op is None:
        audit.write_intent(audit_id, id_class, principal, lane, skill_id, provider, operation, None,
                           reason="unknown provider/operation")
        audit.write_outcome(audit_id, "rejected")
        return CallResult(400, {"error": "unknown provider/operation"}, audit_id, principal=principal,
                          outcome="rejected", denial_stage="validation", reason="unknown provider/operation")

    # -- 4. authorize: principal in op.scopes? (deny-by-default; M4) ------------------------------
    if principal not in op.get("scopes", []):
        # A cross-lane reach (e.g. lane:newswire -> generate_grounded) lands HERE: out-of-scope -> 403.
        audit.write_intent(audit_id, id_class, principal, lane, skill_id, provider, operation, None,
                           reason="out of scope")
        audit.write_outcome(audit_id, "forbidden")
        return CallResult(403, {"error": "forbidden", "reason": "out of scope"}, audit_id,
                          principal=principal, outcome="forbidden", egressed=False,
                          denial_stage="scopes", reason="out of scope")

    # -- 5. validate params + build the server-pinned destination (INV-DEST) ----------------------
    try:
        params = _validate_params(op, params)
        url = _build_destination(op, slot_selections)
    except Rejected as r:
        audit.write_intent(audit_id, id_class, principal, lane, skill_id, provider, operation, None,
                           reason=r.reason)
        audit.write_outcome(audit_id, "rejected")
        return CallResult(400, {"error": "rejected", "reason": r.reason}, audit_id, principal=principal,
                          outcome="rejected", denial_stage="validation", reason=r.reason)

    # -- 6. rate limit (per-lane bucket; M6) ------------------------------------------------------
    if rate_limiter is not None and not rate_limiter.allow(principal, skill_id):
        audit.write_intent(audit_id, id_class, principal, lane, skill_id, provider, operation, params,
                           reason="rate limited")
        audit.write_outcome(audit_id, "rate_limited")
        return CallResult(429, {"error": "rate_limited"}, audit_id, principal=principal,
                          outcome="rate_limited", egressed=False, denial_stage="rate_limit",
                          reason="rate limited")

    # -- 7. INTENT record — value-free, carries `lane`, written BEFORE egress (durable) -----------
    audit.write_intent(audit_id, id_class, principal, lane, skill_id, provider, operation, params)

    # -- 8. EGRESS (the credentialed outbound call) -----------------------------------------------
    egressed = True
    try:
        resp = egress_fn(op["method"], url, {}, params)
    except Exception as exc:  # noqa: BLE001 — any egress failure is a provider_error, never leaked raw
        audit.write_outcome(audit_id, "provider_error", upstream_status=None)
        return CallResult(502, error_envelope(502, type(exc).__name__), audit_id, principal=principal,
                          outcome="provider_error", egressed=True, denial_stage=None)

    # crash-injection window (P-M5): a crash HERE, after egress and before the OUTCOME write, must leave the
    # durable INTENT record on disk (the executed credentialed call is recorded).
    if after_egress_hook is not None:
        after_egress_hook(audit_id)

    # -- 9. OUTCOME + response redaction (INV-RESP allow-list) ------------------------------------
    if getattr(resp, "redirected_to", None) is not None or not (200 <= resp.status < 300):
        audit.write_outcome(audit_id, "provider_error", upstream_status=resp.status)
        return CallResult(502, error_envelope(resp.status, "upstream_non_success"), audit_id,
                          principal=principal, outcome="provider_error", egressed=True, denial_stage=None,
                          meta={"redirect_not_followed": getattr(resp, "redirected_to", None)})

    redacted = redact_response(op["response_schema"], resp.body)
    audit.write_outcome(audit_id, "ok", upstream_status=resp.status)
    return CallResult(200, redacted, audit_id, principal=principal, outcome="ok", egressed=egressed,
                      denial_stage=None)
