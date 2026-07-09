# author: Denson Smith
# ticket: stoa--q7f (u--9s2 Phase-1 increment 2.4) — MUST-RUN #1: the package imports + the handler starts
# against a local socket (INV-BIND-permitted loopback) and serves a gated request end-to-end.
# seat-built-by: CAPTAIN_ADA_the_stoa (EXECUTOR)

from __future__ import annotations

import json
import urllib.request

from secure_core.server import build_server
from secure_core.audit import AuditLog

from conftest import science_headers, legit_recorder, PINNED_GEN_HOST


def test_package_imports():
    import secure_core  # noqa: F401
    assert hasattr(secure_core, "load_registry")
    assert hasattr(secure_core, "resolve_principal")
    assert hasattr(secure_core, "seal_audit")


def test_handler_starts_and_serves_a_gated_call(core, tmp_path):
    """MUST-RUN #1 — start the real server over a loopback socket (INV-BIND permits loopback), POST a
    valid /call as the science lane, and get a redacted 200 back."""
    audit = AuditLog(path=str(tmp_path / "audit.log"))
    rec = legit_recorder()
    server = build_server(core, egress_fn=rec, audit=audit)
    try:
        body = json.dumps({
            "provider": "vertex",
            "operation": "generate_grounded",
            "skill_id": "gsearch",
            "params": {"contents": []},
        }).encode("utf-8")
        req = urllib.request.Request(
            server.url + "/call",
            data=body,
            method="POST",
            headers={"Content-Type": "application/json", **science_headers()},
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            assert resp.status == 200
            payload = json.loads(resp.read().decode("utf-8"))
        # redacted: declared fields present, undeclared dropped
        assert "candidates" in payload and "usageMetadata" in payload
        assert "modelVersion" not in payload
        assert "safetyRatings" not in payload["candidates"][0]
        # the egress reached ONLY the pinned host
        assert rec.hosts == [PINNED_GEN_HOST]
        # two-phase audit recorded an ok
        assert any(o["outcome"] == "ok" for o in audit.outcomes())
    finally:
        server.close()
