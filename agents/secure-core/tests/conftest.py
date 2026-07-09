# author: Denson Smith
# ticket: stoa--q7f (u--9s2 Phase-1 increment 2.4)
# seat-built-by: CAPTAIN_ADA_the_stoa (EXECUTOR)
#
# conftest: makes secure_core importable without an install (sys.path seam) and provides shared probe
# handles — a validated Core, a value-free-ready AuditLog, header builders for each lane/identity, and a
# realistic Vertex response body (so redaction can be proven against the real response surface).

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

_PKG_ROOT = Path(__file__).resolve().parent.parent
if str(_PKG_ROOT) not in sys.path:
    sys.path.insert(0, str(_PKG_ROOT))

from secure_core.registry import CAP_DOMAIN, load_registry, default_lane_registry  # noqa: E402
from secure_core.audit import AuditLog  # noqa: E402
from secure_core.egress import EgressRecorder, EgressResponse  # noqa: E402

SCIENCE_CAP = f"{CAP_DOMAIN}/cap/science-core-client"
NEWSWIRE_CAP = f"{CAP_DOMAIN}/cap/newswire-core-client"
UNMAPPED_CAP = f"{CAP_DOMAIN}/cap/ghost-core-client"  # a cap NOT in LANE_REGISTRY
OPERATOR_LOGIN = "operator@example.com"

# The pinned upstream host the LEGIT egress must reach (and ONLY that host).
PINNED_GEN_HOST = "us-central1-aiplatform.googleapis.com"


def app_caps_header(*caps) -> dict:
    """Build a Tailscale-App-Capabilities header value (a JSON object keyed by cap name), as serve would
    reinject the daemon-verified value."""
    obj = {c: [{}] for c in caps}
    return {"Tailscale-App-Capabilities": json.dumps(obj)}


def science_headers() -> dict:
    return app_caps_header(SCIENCE_CAP)


def newswire_headers() -> dict:
    return app_caps_header(NEWSWIRE_CAP)


def operator_headers(login: str = OPERATOR_LOGIN) -> dict:
    return {"Tailscale-User-Login": login}


@pytest.fixture
def core():
    """A validated Core with the operator allowlist populated (so operator legit paths resolve)."""
    return load_registry(operators=[OPERATOR_LOGIN])


@pytest.fixture
def audit(tmp_path):
    """A file-backed AuditLog (durable INTENT — needed for the P-M5 crash-window durability assertion)."""
    return AuditLog(path=str(tmp_path / "audit.log"))


def legit_generate_body() -> dict:
    """A realistic Vertex generateContent response surface, carrying BOTH declared fields AND undeclared
    ones (modelVersion / responseId / safetyRatings) that the allow-list must drop."""
    return {
        "candidates": [
            {
                "content": {"role": "model", "parts": [{"text": "grounded answer"}]},
                "finishReason": "STOP",
                "groundingMetadata": {"webSearchQueries": ["q"]},
                "safetyRatings": [{"category": "X", "probability": "NEGLIGIBLE"}],  # UNDECLARED -> dropped
            }
        ],
        "usageMetadata": {
            "promptTokenCount": 10,
            "candidatesTokenCount": 20,
            "totalTokenCount": 30,
            "cachedContentTokenCount": 0,  # UNDECLARED -> dropped
        },
        "modelVersion": "gemini-2.5-flash",  # UNDECLARED top-key -> dropped
        "responseId": "abc123",              # UNDECLARED top-key -> dropped
    }


def legit_recorder() -> EgressRecorder:
    """An egress recorder whose pinned-host response is a legit generate body."""
    rec = EgressRecorder(default_response=EgressResponse(status=200, body=legit_generate_body()))
    rec.set_response(PINNED_GEN_HOST, EgressResponse(status=200, body=legit_generate_body()))
    return rec
