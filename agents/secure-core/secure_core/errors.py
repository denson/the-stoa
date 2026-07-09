# author: Denson Smith
# ticket: stoa--q7f (u--9s2 Phase-1 increment 2.4)
# seat-built-by: CAPTAIN_ADA_the_stoa (EXECUTOR)
# design-ground-truth: design-rev4.md §2.1/§2.4 (Forbidden AT RESOLUTION), §3.1 (SealAuditError),
#                       rev2 §1.2.1/§1.3.1/§1.4.3 (LoaderError / INV-DEST/RESP/BIND fail-loud).
#
# Single home for the secure-core exception classes. Each is FAIL-LOUD by design: the invariants refuse
# to serve / refuse to load / deny the request / fail the build — never warn-and-continue.

from __future__ import annotations


class Forbidden(Exception):
    """§2.1/§2.4 (INV-PRINCIPAL) — request-time authorization DENIAL, raised AT RESOLUTION (unresolvable /
    ambiguous principal) OR at the per-op scopes check (out-of-scope principal). The handler maps it to a
    403 with ZERO egress and an audited `forbidden` record carrying `.reason`. The r1-residual requirement:
    resolve_principal RAISES this AT RESOLUTION so the audited reason is `no resolvable principal` — never a
    permissive default.

    Carries a machine-stable `.reason` (e.g. "no resolvable principal", "ambiguous multi-lane principal",
    "out of scope") so the audit record and the P-M4 probe can assert WHERE the denial occurred."""

    def __init__(self, reason: str):
        super().__init__(reason)
        self.reason = reason


class Rejected(Exception):
    """rev2 §1.3 — the validation gate refused the request BEFORE any egress: unknown provider/operation,
    an undeclared param/slot key, a slot value outside its ENUM, malformed envelope. Maps to 400, ZERO
    egress, audited `rejected` with `.reason`."""

    def __init__(self, reason: str):
        super().__init__(reason)
        self.reason = reason


class RateLimited(Exception):
    """rev2 §1.4.4 (M6) — the per-lane token bucket refused the call. Maps to 429, ZERO egress, audited
    `rate_limited`."""

    def __init__(self, reason: str = "rate limited"):
        super().__init__(reason)
        self.reason = reason


class ProviderError(Exception):
    """rev2 §1.3.1 — the upstream provider call failed OR returned a non-success (incl. a 3xx that
    redirect-OFF egress did NOT follow). Returned to the caller as `{status, provider_error_class}` ONLY —
    never the raw upstream body/headers (M2 channel closed)."""

    def __init__(self, provider_error_class: str, upstream_status: int | None = None):
        super().__init__(provider_error_class)
        self.provider_error_class = provider_error_class
        self.upstream_status = upstream_status


class LoaderError(Exception):
    """rev2 §1.2.1/§1.3.1 + rev4 §2.4 — a STARTUP loader self-check REFUSED TO SERVE (fail-loud): an
    INV-DEST violation (a non-FIXED/ENUM url_slot, a params-derived destination), an INV-RESP violation (an
    op with no response_schema — opaque pass-through forbidden), or an INV-LANE violation (an unknown/typo'd
    scope principal, serve caps != LANE_REGISTRY, a lane principal colliding with caller data). load_registry
    raises this; the process exits non-zero rather than serving a weakened surface."""


class BindError(Exception):
    """rev2 §1.4.3 (INV-BIND) — the listener would bind a routable address, or the AF_UNIX socket is not
    0600. The server REFUSES TO SERVE (exits non-zero) rather than expose a forgeable identity surface."""


class SealAuditError(Exception):
    """rev4 §3.1 (M7) — the fail-CLOSED seal-audit found a secret-VALUE shape (or an ambiguous high-entropy
    blob it could not classify) in the build tree / emitted logs. The build FAILS non-zero. `.findings`
    names every offending (path, kind, reason)."""

    def __init__(self, findings):
        self.findings = list(findings)
        super().__init__(
            f"seal-audit FAILED (fail-closed): {len(self.findings)} finding(s): "
            + "; ".join(f"{f.path}::{f.kind}" for f in self.findings)
        )
