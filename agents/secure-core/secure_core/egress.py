# author: Denson Smith
# ticket: stoa--q7f (u--9s2 Phase-1 increment 2.4)
# seat-built-by: CAPTAIN_ADA_the_stoa (EXECUTOR)
# design-ground-truth: rev2 §1.2.1 (redirect-following OFF for registry egress — a 3xx to an attacker host
#                       is returned as a provider_error, NEVER followed) + §1.3.1 (server-side credential
#                       attached; no caller URL).
#
# The egress SEAM. `EgressResponse` is the closed shape a provider handler returns to the pipeline. The real
# client (`build_urllib_egress`) is redirect-OFF by construction (a NoRedirect handler) and attaches the
# server-side credential — but it is NEVER exercised against the network this arc (build + probe are
# local/mock only). Probes inject an `EgressRecorder` (records the hosts contacted; a denial path never
# calls egress -> recorder empty -> the "ZERO egress" assertion).

from __future__ import annotations

import urllib.error
import urllib.request
from dataclasses import dataclass, field


@dataclass
class EgressResponse:
    status: int
    body: dict           # the decoded upstream JSON body (allow-list-redacted by the pipeline)
    headers: dict = field(default_factory=dict)  # upstream headers — NEVER forwarded to the caller
    redirected_to: str | None = None  # set when a 3xx was seen; the pipeline treats it as provider_error


class EgressRecorder:
    """A mock egress function that records every host it is asked to contact. Injected by the probes:
      - a denial path never calls it (recorder.hosts == [] -> ZERO egress);
      - a legit path calls it exactly once with the pinned host.
    `response_for` maps a host (or None default) to an EgressResponse; a 3xx response is used to prove
    redirect-OFF (the recorder records ONE call and never follows the Location)."""

    def __init__(self, default_response: EgressResponse | None = None):
        self.hosts: list[str] = []
        self.calls: list[dict] = []
        self._default = default_response or EgressResponse(status=200, body={})
        self._by_host: dict[str, EgressResponse] = {}

    def set_response(self, host: str, response: EgressResponse) -> None:
        self._by_host[host] = response

    def __call__(self, method: str, url: str, headers: dict, body: dict) -> EgressResponse:
        host = _host_of(url)
        self.hosts.append(host)
        self.calls.append({"method": method, "url": url, "host": host})
        return self._by_host.get(host, self._default)


def _host_of(url: str) -> str:
    from urllib.parse import urlparse

    return urlparse(url).hostname or ""


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    """redirect-following OFF: a 3xx is surfaced as an error, never followed (closes SSRF-via-redirect)."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):  # noqa: D401
        return None  # do not follow


def build_urllib_egress(credential_provider):
    """The REAL redirect-OFF egress client. `credential_provider()` returns the server-side credential (an
    ADC bearer token) at call time — the credential is attached HERE, server-side, and never seen by the
    caller. NOT exercised against the network this arc (mock-only build)."""

    opener = urllib.request.build_opener(_NoRedirect)

    def egress(method: str, url: str, headers: dict, body: dict) -> EgressResponse:  # pragma: no cover
        import json as _json

        req_headers = dict(headers)
        req_headers["Authorization"] = f"Bearer {credential_provider()}"  # server-side cred attach
        data = _json.dumps(body).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers=req_headers, method=method)
        try:
            with opener.open(req, timeout=30) as resp:
                status = resp.status
                if 300 <= status < 400:
                    return EgressResponse(status=status, body={}, redirected_to=resp.headers.get("Location"))
                payload = _json.loads(resp.read().decode("utf-8"))
                return EgressResponse(status=status, body=payload, headers=dict(resp.headers))
        except urllib.error.HTTPError as exc:
            return EgressResponse(status=exc.code, body={}, headers={})

    return egress
