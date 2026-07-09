# author: Denson Smith
# ticket: stoa--q7f (u--9s2 Phase-1 increment 2.4)
# seat-built-by: CAPTAIN_ADA_the_stoa (EXECUTOR)
# design-ground-truth: design-rev4.md §5.3 step 1 (the transport front:
#                       tailscaled -> tailscale serve --https=443 --accept-app-caps=<caps>
#                       unix:/run/.../core.sock -> 0600 AF_UNIX UDS -> gated handler -> uvicorn) +
#                       rev2 §1.4.3 (INV-BIND) + §1.4.1 (serve strips + reinjects the identity headers).
#
# The transport front, represented for LOCAL/mock running (no real tailnet, no real serve, no real uvicorn
# this arc). `build_server` runs INV-BIND on the INTENDED bind BEFORE opening any socket (a routable target
# -> BindError, refuse to serve — nothing is opened), then binds a loopback socket and serves the gated
# handler via a stdlib HTTP server. In production the same handler sits behind `tailscale serve` on a 0600
# AF_UNIX socket (INV-BIND's AF_UNIX arm); the loopback bind here is the INV-BIND-permitted local
# representation (AF_UNIX is unavailable on the Windows build host — see bind.py PLATFORM NOTE).
#
# The identity headers are consumed as if serve had strip-and-reinjected the daemon-VERIFIED values (real
# serve strip+reinject is Phase 2/3); INV-BIND (loopback/0600) is the precondition that makes those headers
# trustworthy, and it is verified here at startup.

from __future__ import annotations

import json
import socket
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from secure_core.bind import assert_bind_target_safe, assert_listener_safe
from secure_core.handler import handle_call


def _make_handler_class(core, egress_fn, audit, rate_limiter):
    class _Handler(BaseHTTPRequestHandler):
        # quiet logging
        def log_message(self, *args):  # noqa: D401
            return

        def _tailscale_headers(self) -> dict:
            # serve reinjects the verified Tailscale-* headers; we read them here (the local representation
            # trusts them under the INV-BIND loopback/0600 precondition verified at startup).
            out = {}
            for k, v in self.headers.items():
                out[k] = v
            return out

        def do_POST(self):
            if self.path != "/call":
                self._json(404, {"error": "not found"})
                return
            length = int(self.headers.get("Content-Length", 0) or 0)
            raw = self.rfile.read(length) if length else b""
            try:
                envelope = json.loads(raw.decode("utf-8")) if raw else {}
            except ValueError:
                self._json(400, {"error": "malformed envelope"})
                return
            result = handle_call(
                core,
                self._tailscale_headers(),
                envelope,
                egress_fn=egress_fn,
                audit=audit,
                rate_limiter=rate_limiter,
            )
            self._json(result.status, result.body)

        def _json(self, status: int, body: dict):
            payload = json.dumps(body).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)

    return _Handler


class SecureCoreServer:
    """A running gated core over a loopback socket. `.url` is the base URL; `.close()` stops it."""

    def __init__(self, httpd: ThreadingHTTPServer, thread: threading.Thread):
        self._httpd = httpd
        self._thread = thread
        host, port = httpd.server_address[:2]
        self.host = host
        self.port = port
        self.url = f"http://{host}:{port}"

    def close(self):
        self._httpd.shutdown()
        self._httpd.server_close()
        self._thread.join(timeout=5)


def build_server(core, egress_fn, audit, rate_limiter=None, host="127.0.0.1", port=0) -> SecureCoreServer:
    """INV-BIND-guarded build. Refuses to serve (raises BindError) if `host` is routable — BEFORE opening
    any socket. On a loopback host it binds, re-verifies the ACTUAL listener (assert_listener_safe), starts
    the server thread, and returns a SecureCoreServer."""
    # In-process refuse-if-routable (P-M3(a)) — no socket is opened for a routable target.
    assert_bind_target_safe(socket.AF_INET, address=(host, port))

    handler_cls = _make_handler_class(core, egress_fn, audit, rate_limiter)
    httpd = ThreadingHTTPServer((host, port), handler_cls)
    # Back the pre-bind pure check with a runtime guarantee on the real socket.
    assert_listener_safe(httpd.socket)

    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    return SecureCoreServer(httpd, thread)
