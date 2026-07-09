# author: Denson Smith
# ticket: stoa--q7f (u--9s2 Phase-1 increment 2.4)
# seat-built-by: CAPTAIN_ADA_the_stoa (EXECUTOR)
# design-ground-truth: rev2 §1.5 P-M3 (augmented r5+r3) + rev4 §5.2 M3 row. Threat M3: identity-header
#                       forgery via non-loopback bind.
#
# P-M3: (a) IN-PROCESS — the server configured to bind a routable address EXITS non-zero / refuses to serve
# (INV-BIND fired, not merely a later ss/netstat finding); AF_UNIX-not-0600 refuses; loopback/0600 allowed.
# (b) the real listener is loopback (no routable listener); the App-Capabilities reader normalizes the
# underscore/case variant (no variant bypass) and an unmapped forged cap does not resolve. (c) LEGIT: a
# serve-routed operator (User-Login) AND a tagged-builder (App-Capabilities) each authorize to their class.
#
# PLATFORM NOTE: AF_UNIX is unavailable on the Windows build host; the 0600-AF_UNIX arm of INV-BIND is
# verified by the PURE assert_bind_target_safe below (cross-platform). serve's strip-and-reinject of a
# forged VALID cap is the Phase-2/3 runtime guarantee whose PRECONDITION (INV-BIND loopback/0600) is
# verified here.

from __future__ import annotations

import socket

import pytest

from secure_core.bind import assert_bind_target_safe, assert_listener_safe
from secure_core.errors import BindError
from secure_core.server import build_server
from secure_core.audit import AuditLog
from secure_core.handler import handle_call
from secure_core.identity import resolve_principal

from conftest import (
    science_headers, operator_headers, legit_recorder, PINNED_GEN_HOST,
    SCIENCE_CAP, UNMAPPED_CAP,
)


# ---- (a) IN-PROCESS refuse-if-routable -----------------------------------------------------------
def test_pm3a_routable_bind_refuses_to_serve(core, tmp_path):
    """Building the server on a routable host RAISES BindError (refuse to serve) — no socket is opened."""
    audit = AuditLog(path=str(tmp_path / "a.log"))
    with pytest.raises(BindError, match="routable"):
        build_server(core, egress_fn=legit_recorder(), audit=audit, host="0.0.0.0")


def test_pm3a_pure_bind_check_routable_vs_loopback():
    assert_bind_target_safe(socket.AF_INET, address=("127.0.0.1", 0))  # loopback OK
    for bad in ("0.0.0.0", "::", "10.0.0.5", "100.64.0.7"):
        with pytest.raises(BindError):
            assert_bind_target_safe(socket.AF_INET, address=(bad, 0))


def test_pm3a_af_unix_0600_refuse_logic_is_exercised():
    """The 0600-AF_UNIX refuse arm is GENUINELY EXERCISED cross-platform (NOT a platform-skip). The mode
    check is decoupled from the platform's AF_UNIX constant (unavailable on the Windows build host) via a
    synthetic unix_path+mode, so the fail-loud refuse LOGIC actually runs and is asserted here."""
    from secure_core.bind import assert_unix_mode_0600
    # 0600 -> allowed (no raise), on ANY host
    assert_bind_target_safe(unix_path="/run/core.sock", mode=0o600)
    assert_unix_mode_0600(0o600, unix_path="/run/core.sock")
    # any non-0600 mode -> REFUSE (BindError), exercised on ANY host
    for bad_mode in (0o644, 0o660, 0o777, 0o604, 0o000, 0o640):
        with pytest.raises(BindError, match="0600"):
            assert_bind_target_safe(unix_path="/run/core.sock", mode=bad_mode)
        with pytest.raises(BindError, match="0600"):
            assert_unix_mode_0600(bad_mode, unix_path="/run/core.sock")


def test_pm3a_af_unix_real_listener_mode_checked_when_available():
    """On a host WITH AF_UNIX (the Linux deploy target), assert_listener_safe stats the REAL socket and
    refuses a non-0600 socket. On Windows (no AF_UNIX) this real-socket path is the Phase-3-on-Linux
    residual — the LOGIC arm above is already exercised cross-platform, so the invariant is NOT unverified."""
    if not hasattr(socket, "AF_UNIX"):
        pytest.skip("AF_UNIX unavailable on this host; the refuse LOGIC is exercised cross-platform above, "
                    "the REAL-socket stat is the Linux-deploy (Phase-3) residual")
    import os
    import tempfile
    from secure_core.bind import assert_listener_safe
    path = os.path.join(tempfile.mkdtemp(), "core.sock")
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
        s.bind(path)
        os.chmod(path, 0o644)  # wrong mode
        with pytest.raises(BindError, match="0600"):
            assert_listener_safe(s)
    finally:
        s.close()
        try:
            os.unlink(path)
        except OSError:
            pass


def test_pm3a_real_loopback_listener_passes_inv_bind(core, tmp_path):
    audit = AuditLog(path=str(tmp_path / "a.log"))
    server = build_server(core, egress_fn=legit_recorder(), audit=audit, host="127.0.0.1")
    try:
        assert_listener_safe(server._httpd.socket)  # the real bound socket is INV-BIND-safe
        assert server.host in ("127.0.0.1", "localhost")
    finally:
        server.close()


# ---- (b) no routable listener + no header-variant bypass -----------------------------------------
def test_pm3b_underscore_and_case_variants_read_the_same(core):
    """The App-Capabilities reader normalizes the underscore/case defense — a forged variant name cannot
    sneak a DIFFERENT value past the reader (it reads the same header consistently)."""
    hyphen = {"Tailscale-App-Capabilities": '{"%s": [{}]}' % SCIENCE_CAP}
    underscore = {"Tailscale_App_Capabilities": '{"%s": [{}]}' % SCIENCE_CAP}
    mixed = {"TaIlScAlE-ApP-CaPaBiLiTiEs": '{"%s": [{}]}' % SCIENCE_CAP}
    assert resolve_principal(hyphen, core) == "lane:science"
    assert resolve_principal(underscore, core) == "lane:science"
    assert resolve_principal(mixed, core) == "lane:science"


def test_pm3b_forged_unmapped_cap_does_not_resolve(core):
    from secure_core.errors import Forbidden
    forged = {"Tailscale-App-Capabilities": '{"%s": [{}]}' % UNMAPPED_CAP}
    with pytest.raises(Forbidden, match="no resolvable principal"):
        resolve_principal(forged, core)


# ---- (c) LEGIT — each identity class authorizes to its class -------------------------------------
def test_pm3c_operator_and_builder_each_authorize(core, tmp_path):
    audit = AuditLog(path=str(tmp_path / "a.log"))
    # operator (User-Login on the allowlist) -> embed (operators in scope) authorized
    op_res = handle_call(core, operator_headers(),
                         {"provider": "vertex", "operation": "embed", "skill_id": "emb",
                          "params": {"instances": []}},
                         egress_fn=legit_recorder(), audit=audit)
    assert op_res.status == 200 and op_res.principal == "operators"
    # tagged builder (App-Capabilities) -> generate_grounded (lane:science in scope) authorized
    b_res = handle_call(core, science_headers(),
                        {"provider": "vertex", "operation": "generate_grounded", "skill_id": "gs",
                         "params": {"contents": []}},
                        egress_fn=legit_recorder(), audit=audit)
    assert b_res.status == 200 and b_res.principal == "lane:science"
