<!-- author: Denson Smith -->
# secure-core — the CONSOLIDATION secure pass-through core

Ticket: `stoa--q7f` (u--9s2 Phase-1 increment 2.4). Design ground-truth:
`agents/design/stoa--q7f/design-rev6.md` (§2 multi-lane authz, §3 seal-audit, §5 invariant + probe
contract incl. §5.1a the INV-RESP recursive NODE grammar), carrying rev2 §1 (INV-DEST/RESP/BIND,
two-phase audit).

The **REAL** credentialed per-provider, multi-lane pass-through the CONSOLIDATION center exposes. A local
skill on any consuming lane names a `provider` + a pre-registered closed `operation`; the core attaches that
provider's **server-side** credential, calls the pinned upstream host, and returns **only** the op's declared
response fields — the credential never leaves the core. Sibling package to `builder_deploy_core` (the
value-free provisioning emitter that stands this core up); this is the runtime service.

This arc **builds + probes LOCALLY / against mocks only** — no real Railway/GCP/Tailscale, no real secrets,
no money (directive §5 scope fence). The tailscaled / `tailscale serve` / uvicorn orchestration is
**represented** for local running; the security invariants are real code, exercised by the threat-anchored
probe suite `P-M1..P-M7`.

## The invariants (each FAIL-LOUD — refuse-to-serve / refuse-to-load / deny-request / fail-build)

| Invariant | Guarantees | Mechanism | Module |
|-----------|------------|-----------|--------|
| `INV-DEST` | No caller-supplied destination is constructable | `url_slots` FIXED/ENUM only; params/skill_id disjoint; redirect-OFF; loader refuses a violating op | `slots.py`, `registry.py`, `egress.py` |
| `INV-RESP` | No credential byte reaches a caller via the response | per-op `response_schema` recursive NODE grammar: OBJECT recurses declared keys (drops every undeclared key at every depth); SCALAR passes a value only if it carries NO mapping at ANY depth (recursive dict-scan, not a shallow check); PASS_WHOLE passes whole but is deny-by-default via `PASS_WHOLE_ALLOWLIST = {"candidates.content"}`; loader refuses to load a non-allowlisted PASS_WHOLE placement or a legacy bare-list node, or an op with no schema | `redact.py`, `registry.py` |
| `INV-BIND` | Identity headers are trustworthy (no routable listener) | 0600 AF_UNIX / loopback; routable bind → refuse to serve (exit non-zero) | `bind.py`, `server.py` |
| `INV-LANE` | Registry+serve config consistent at STARTUP | every scope a known principal; serve caps == `LANE_REGISTRY`; principals disjoint from caller data | `registry.py` |
| `INV-PRINCIPAL` | Every REQUEST resolves by explicit membership or is DENIED | no `.get(cap, DEFAULT)`; unresolvable → 403 no egress audited forbidden **at resolution**; multi-cap non-registered → 403 reject-ambiguous | `identity.py`, `handler.py` |
| seal-audit | No secret VALUE in code/config/catalog/logs | shape-match scan; build FAILS non-zero on any match; exemption only for path-bound + shape-clean marked fixtures; fails CLOSED | `sealaudit.py` |

## Running the probes

```
cd agents/secure-core
python -m pytest tests/ -q          # P-M1..P-M7 + smoke, all green against the REAL code
```

The probes FALSIFY a warnings-only / permissive-default / marker-bypass build: they assert non-zero exit /
refuse-to-serve / 403-no-egress / build-fail, not a log line.
