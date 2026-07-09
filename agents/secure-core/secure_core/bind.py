# author: Denson Smith
# ticket: stoa--q7f (u--9s2 Phase-1 increment 2.4)
# seat-built-by: CAPTAIN_ADA_the_stoa (EXECUTOR)
# design-ground-truth: rev2 §1.4.3 (INV-BIND) — in-process, fail-loud: the listener MUST be a 0600 AF_UNIX
#                       socket OR a loopback address; ANY routable bind (0.0.0.0, a tailnet IP, a non-
#                       loopback interface) -> log a fatal identity-trust violation + EXIT non-zero (refuse
#                       to serve). A 0.0.0.0 bind is un-shippable.
#
# INV-BIND is provided two ways: `assert_bind_target_safe` is a PURE check on the intended bind parameters
# (fully cross-platform — the probe exercises 0.0.0.0/loopback/AF_UNIX-mode cases without opening a routable
# socket), and `assert_listener_safe` inspects a REAL bound socket at startup. Both RAISE BindError (refuse
# to serve) on violation.
#
# PLATFORM NOTE (build-vs-deploy): AF_UNIX is unavailable on the Windows build host (socket.AF_UNIX absent).
# The DEPLOY target (Linux Railway container) binds a 0600 AF_UNIX socket per the design; the local build
# smoke binds a loopback socket (INV-BIND explicitly permits loopback). The 0600-AF_UNIX arm of INV-BIND is
# fully verified cross-platform by the PURE `assert_bind_target_safe` (P-M3), independent of AF_UNIX
# availability on the host.

from __future__ import annotations

import os
import socket
import stat

from secure_core.errors import BindError

_LOOPBACK = {"127.0.0.1", "::1", "localhost"}


def assert_unix_mode_0600(mode, unix_path=None) -> None:
    """The 0600-AF_UNIX refuse arm, DECOUPLED from the platform's AF_UNIX availability so the fail-loud logic
    is genuinely EXERCISED cross-platform (the Windows build host lacks socket.AF_UNIX, but the mode-refuse
    LOGIC must not be a platform-skip). Raises BindError (refuse to serve) if `mode` is not 0600."""
    if mode is None:
        raise BindError(f"INV-BIND: AF_UNIX bind at {unix_path!r} has no mode to verify (refuse)")
    if (mode & 0o777) != 0o600:
        raise BindError(
            f"INV-BIND violation: AF_UNIX socket {unix_path!r} mode is {oct(mode & 0o777)} != 0600 — "
            f"refusing to serve"
        )


def assert_bind_target_safe(family=None, address=None, unix_path=None, mode=None) -> None:
    """PURE INV-BIND check on the INTENDED bind, BEFORE any socket is opened. Raises BindError (refuse to
    serve) if the target is routable or an AF_UNIX socket that is not 0600.

    - AF_UNIX arm: identified by `unix_path is not None` (the path, NOT the platform AF_UNIX constant, so the
      0600-refuse logic is exercised cross-platform); `mode` MUST be 0600.
    - AF_INET/AF_INET6 arm: `address` host MUST be a loopback literal; 0.0.0.0 / :: / non-loopback -> refuse.
    """
    fam_name = getattr(family, "name", str(family))
    if unix_path is not None or (hasattr(socket, "AF_UNIX") and family == socket.AF_UNIX):
        assert_unix_mode_0600(mode, unix_path=unix_path)
        return
    if family in (socket.AF_INET, getattr(socket, "AF_INET6", object())):
        host = str(address[0] if isinstance(address, (tuple, list)) else address)
        if host not in _LOOPBACK:
            raise BindError(
                f"INV-BIND violation: listener would bind routable address {host!r} ({fam_name}) — the "
                f"identity headers would be forgeable; refusing to serve (exit non-zero)"
            )
        return
    raise BindError(f"INV-BIND: unsupported/unknown socket family {fam_name} — refusing to serve")


def assert_listener_safe(sock: socket.socket) -> None:
    """Inspect a REAL bound socket at startup and refuse to serve if it is routable / not 0600 AF_UNIX. This
    backs the pure check with a runtime guarantee on the actual listener."""
    family = sock.family
    if hasattr(socket, "AF_UNIX") and family == socket.AF_UNIX:
        path = sock.getsockname()
        try:
            mode = stat.S_IMODE(os.stat(path).st_mode)
        except OSError as exc:
            raise BindError(f"INV-BIND: cannot stat AF_UNIX socket {path!r}: {exc}") from exc
        assert_bind_target_safe(socket.AF_UNIX, unix_path=path, mode=mode)
        return
    name = sock.getsockname()
    host = name[0] if isinstance(name, (tuple, list)) else name
    assert_bind_target_safe(family, address=host)
