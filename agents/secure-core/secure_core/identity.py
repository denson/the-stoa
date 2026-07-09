# author: Denson Smith
# ticket: stoa--q7f (u--9s2 Phase-1 increment 2.4)
# seat-built-by: CAPTAIN_ADA_the_stoa (EXECUTOR)
# design-ground-truth: design-rev4.md §2.1 (resolve_principal pseudocode — EXPLICIT MEMBERSHIP ONLY) +
#                       §2.4 INV-PRINCIPAL (request-time fail-closed) + rev2 §1.4.1 (serve-injected,
#                       daemon-verified headers; strip-and-reinject incl. underscore/case defense).
#
# Request-time principal resolution. INV-PRINCIPAL: every request resolves a principal by EXPLICIT
# MEMBERSHIP or is DENIED — no request path resolves to a permissive default. The r1-residual requirement
# (FM-directed): resolve_principal RAISES Forbidden AT RESOLUTION so the audited denial reason is
# `no resolvable principal` (or `ambiguous multi-lane principal`) — observed at resolution, not merely as a
# downstream 403/zero-egress triple.

from __future__ import annotations

import json

from secure_core.errors import Forbidden

# serve strips-and-reinjects the identity headers; the daemon delivers the VERIFIED values. The core decodes
# App-Capabilities per the SAME header rules it uses for the User-* headers (rev2 V-ENC), then JSON-parses.
# We normalize the header lookup for the underscore/case defense (Tailscale_App_Capabilities, mixed-case).
_APP_CAPS_HEADER = "tailscale-app-capabilities"
_USER_LOGIN_HEADER = "tailscale-user-login"


def _normalize_headers(headers) -> dict:
    """Case- AND underscore-insensitive header map (the strip-and-reinject normalization defense). A client
    copy under any casing/underscore variant is irrelevant here because serve reinjects the verified value;
    we normalize only so the backend reads the canonical name."""
    out = {}
    for k, v in dict(headers).items():
        norm = str(k).lower().replace("_", "-")
        out[norm] = v
    return out


def parse_app_capabilities(headers) -> set:
    """-> set[str] of capability NAMES present in the serve-injected, control-plane-resolved
    `Tailscale-App-Capabilities`. Returns the empty set if the header is absent / empty / malformed (a
    tagged node that was granted NO cap, or an untagged node) — an empty set means NO lane resolves, which
    INV-PRINCIPAL turns into a denial (never a default)."""
    h = _normalize_headers(headers)
    raw = h.get(_APP_CAPS_HEADER)
    if raw is None:
        return set()
    if isinstance(raw, (dict,)):
        obj = raw
    else:
        raw = str(raw).strip()
        if not raw:
            return set()
        try:
            obj = json.loads(raw)
        except (ValueError, TypeError):
            return set()  # malformed -> no cap resolves -> denial (fail-closed)
    if not isinstance(obj, dict):
        return set()
    # App-Capabilities is a JSON object keyed by capability NAME; the keys are the granted caps.
    return {str(k) for k in obj.keys()}


def parse_user_login(headers):
    """-> str | None. The serve-injected `Tailscale-User-Login` (empty/omitted for a TAGGED node)."""
    h = _normalize_headers(headers)
    raw = h.get(_USER_LOGIN_HEADER)
    if raw is None:
        return None
    raw = str(raw).strip()
    return raw or None


def resolve_principal(headers, core) -> str:
    """Return a principal string OR raise Forbidden(403) AT RESOLUTION. EXPLICIT MEMBERSHIP ONLY — there is
    NO `.get(cap, DEFAULT)` and NO `empty-header -> benign class`. Order matches design §2.1:

      1. LANE resolution — a cap yields a lane principal IFF present AND in LANE_REGISTRY (a miss is NOT a
         fallback, it is simply not added).
      2. MULTI-CAP — reject-ambiguous: >1 distinct lane principal AND the cap-set is not a registered
         MULTI_LANE_NODES entry -> DENY (never a silent union).
      3. Single lane principal -> return it.
      4. OPERATOR — a User-Login yields `operators` IFF on the <CORE>_OPERATORS allowlist.
      5. NEITHER resolved -> raise Forbidden("no resolvable principal") — NEVER a default.
    """
    caps = parse_app_capabilities(headers)
    login = parse_user_login(headers)

    # 1. LANE resolution — explicit membership; a lookup MISS is not added (NOT defaulted).
    lane_principals = {core.lane_registry[c] for c in caps if c in core.lane_registry}

    # 2. MULTI-CAP -> reject-ambiguous (fail-closed) unless an explicitly-registered multi-lane node.
    if len(lane_principals) > 1:
        capset = frozenset(caps)
        if capset in core.multi_lane_nodes:
            return core.multi_lane_nodes[capset]  # the explicitly-registered multi-lane principal
        raise Forbidden("ambiguous multi-lane principal")  # 403, no egress, audited forbidden

    # 3. exactly one lane principal resolved.
    if len(lane_principals) == 1:
        return next(iter(lane_principals))

    # 4. OPERATOR — explicit allowlist membership only.
    if login is not None and login in core.operators:
        return "operators"

    # 5. NOTHING resolved -> DENY AT RESOLUTION. Never a default/permissive principal.
    raise Forbidden("no resolvable principal")


def identity_class_of(principal: str) -> str:
    """`operators` -> operator class; `lane:*` -> the lane class. Used for the value-free audit record."""
    return "operators" if principal == "operators" else "lane"
