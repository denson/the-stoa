---
author: Denson Smith
seat: CAPTAIN_DAEDALUS_the_stoa (ARCHITECT)
ticket: stoa--q7f
requirement: sos--373
epic: u--9s2 (Phase-2 increment 2.4 — DESIGN gauntlet)
arc: stoa--q7f (secure Railway core for stoa_of_science)
consumes: agents/research/stoa--q7f/strabo-dc2-premises.md (DC2, all PASS, two encoded nuances)
status: design-rev1 (for ARGUS cold-audit; DC1 pass-through shape is the crux)
build-scope: DESIGN ONLY. ADA builds the DC3 mock-emit ONLY. The core SERVICE is designed-not-built.
---

# Secure Railway core for stoa_of_science — credentialed per-provider API pass-through + pgvector embeddings DB

## §0 Problem restatement (6.1 pre-work gate)

stoa_of_science's skills increasingly need external API credentials (~46 of 338 skills; Vertex/Gemini
for gsearch first) plus a Postgres/pgvector embeddings store. Keeping API keys on the builder machine
is the recurring security problem. **Design** (do not build) a secure Railway core that holds ALL
provider keys server-side and exposes a **credentialed per-provider pass-through**: a local skill names
a provider + a closed call, the core attaches that provider's key, calls the external API, and returns
the result — the key never leaves the core. The core also hosts a Postgres+pgvector embeddings DB. The
core is reachable ONLY over Tailscale; the builder holds ONLY a tailnet identity (no Railway token, no
SA key, no API keys). This gauntlet produces a **buildable design that relays UP to be gated** — build
nothing real, deploy nothing, mint/set no credentials. ADA builds ONLY the DC3 cookie-cutter mock-emit.

**Imported assumptions (named per 6.1):**
1. **Tagged-builder identity does NOT populate `Tailscale-User-Login`.** Per POLYBIUS's DC2 enrichment
   (independently web-verified against tailscale.com): a TAGGED device (which the in-mesh builder is —
   it joins with a tagged auth-key) does NOT get user-identity headers injected by serve; only
   `Tailscale-App-Capabilities`. So the core's authorization model (DC1.iii) MUST key off the
   tag / App-Capabilities for builder-originated calls, NOT a user-login header. A human operator on a
   user-owned (untagged) tailnet node WOULD carry `Tailscale-User-Login`. The design supports BOTH
   identity classes and is explicit about which authorizes what. This is the single biggest place the
   design diverges from the newswire precedent (which only ever served human operators) — flagged for
   ARGUS in §6.
2. **Egress is public-internet, not tailnet** (STRABO nuance 1). Only operator/builder -> core INGRESS
   uses Tailscale serve; the core's calls to Vertex/provider APIs go out the normal public internet.
   Userspace `tailscale serve` is inbound-only; that is sufficient and correct here.
3. **The core SERVICE is an entirely new runtime service**, a generalization of `newswire-serving`. It
   is NOT in `builder_deploy_core` (which is a value-free one-shot PROVISIONING emitter). DC3 stands the
   core up via the existing emitter; the service code itself is designed in DC1 and built in a later
   gated arc.

The restatement converges with the brief. No load-bearing divergence; the assumptions above are
encoded in the design from the start.

---

## §1 DC1 — The pass-through core shape (the ARGUS security crux)

### §1.1 Threat model (explicit)

This is the most security-sensitive component the team has designed: **a single internet-egress box
that holds ALL provider API keys.** If it is compromised, every provider key is exfiltrable and the box
becomes an open relay. The named threats (M1..M6), each closed BY CONSTRUCTION where possible:

| M# | Named threat | Realized how (attack path) |
|----|--------------|----------------------------|
| M1 | **SSRF / forward-anything egress** | A caller induces the core to make an outbound request to an attacker-chosen URL/host (cloud metadata `169.254.169.254`, internal services, arbitrary exfil endpoint). |
| M2 | **Key-exfil** | A caller gets the core to return a provider key in a response body, error, or log; or routes a provider key to an attacker-controlled destination. |
| M3 | **Identity-header forgery via non-loopback bind** | The pass-through handler listens on a routable address (`0.0.0.0`); a local/colocated process connects directly, bypassing serve, and forges `Tailscale-User-Login` / `Tailscale-App-Capabilities`. |
| M4 | **Over-broad provider/operator authorization** | Any tailnet identity that can reach the core can invoke ANY provider (no per-identity scoping), widening blast radius beyond least-privilege. |
| M5 | **Audit gap** | A pass-through call (who, which provider, which operation, outcome) is not durably recorded, so abuse/compromise is undetectable and unattributable. |
| M6 | **Quota exhaustion / DoS** | A caller (or a runaway skill) floods the core, exhausting the shared Gemini/Vertex quota or the core's resources, denying service to everyone on the shared quota. |

### §1.2 The shape decision (DC1.i): **per-provider scoped pass-through, NOT an egress proxy**

**Decision: per-provider endpoints (a closed registry of named provider operations), NOT an
authenticated allowlisted egress proxy.**

Justification against M1/M2: an egress proxy — even an allowlisted one — takes a URL (or host) from the
caller and forwards. That is a forward-anything primitive with a filter bolted on; the filter is the
only thing standing between a caller and SSRF, and filters are the classic bypass surface (DNS rebinding,
redirect-following, IP-literal vs hostname, IPv6/decimal encodings). A per-provider design has **no
caller-supplied URL at all**: the caller names a `provider` + an `operation` from a **closed,
code-defined registry**; the core holds the URL template, the method, the allowed parameter schema, and
the key binding for that exact operation. The destination is never caller-influenced. SSRF is closed by
construction because there is no "destination" input to attack — only a finite enum of operations the
core knows how to perform. This is strictly more restrictive than deny-by-default allowlisting: it is
deny-by-default over a **closed verb set**, not over an open URL space.

This generalizes `newswire-serving` exactly: newswire's trigger exposed ONE domain verb (`POST /run`)
over the mesh; this core exposes a **closed set** of provider operations (`POST /call` with a validated
`{provider, operation, params}` body that dispatches into a server-side registry). The newswire
`<VERB>` placeholder in the existing `MeshShape` scaffold is exactly where this registry plugs in at
T3 — the core is the T3 product that fills the domain-empty 501 stub.

### §1.3 The client contract (DC1.ii): a closed, validated request shape — never a raw URL

A local skill names a call to the core with a **closed request envelope**, transported over the mesh to
`https://<core>.<tailnet-domain>/call` (Tailscale serve -> 0600 AF_UNIX socket -> handler):

```
POST /call
Content-Type: application/json
{
  "provider":  "vertex",                  # MUST match a key in the server-side PROVIDER_REGISTRY
  "operation": "generate_grounded",       # MUST match a registered operation under that provider
  "params":    { ... }                    # validated against that operation's PARAM SCHEMA (closed)
}
```

Rules enforced server-side (the validation gate, before any egress):
- `provider` and `operation` MUST resolve to an entry in the **server-side** `PROVIDER_REGISTRY`
  (code, not caller data). Unknown provider/operation -> `400`, no egress, audited as `rejected`.
- `params` MUST validate against that operation's declared **closed param schema** (allowed keys,
  types, value bounds). No key/URL/host/header field is ever accepted from the caller. An unexpected
  param key -> `400`, no egress.
- The core constructs the outbound request entirely from the registry entry: URL template + method +
  the server-side-attached credential + the validated params interpolated into declared slots ONLY.
- The response returned to the caller is the **provider payload**, with a server-side **redaction pass**
  that strips any echoed credential material and any `Authorization`/`x-goog-api-key`-class header from
  error bodies. Errors are returned as `{status, provider_error_class}` — never the raw upstream error
  with headers.

The registry entry shape (server-side, illustrative — built in the later gated arc, NOT now):

```python
PROVIDER_REGISTRY = {
  "vertex": {
    "auth": "adc_sa",                                  # use server-side ADC (SA), never an API key
    "operations": {
      "generate_grounded": {
        "method": "POST",
        "url": "https://{location}-aiplatform.googleapis.com/v1/projects/{project}"
               "/locations/{location}/publishers/google/models/{model}:generateContent",
        "url_slots": {"location": ENUM[...], "project": FIXED, "model": ENUM[...]},  # closed, server-pinned
        "param_schema": {"contents": ..., "tools": {"google_search": {}}},          # closed
        "scopes": ["operators", "builders"],          # which identity classes may call this op
      },
      "embed": { "method": "POST", "url": ".../publishers/google/models/{model}:predict", ... },
    },
  },
}
```

The `url_slots` are server-pinned enums/fixed values, NOT free caller input — `project` and `location`
are pinned to the core's own GCP project; `model` is a closed enum. The caller cannot steer the
destination.

### §1.4 Auth, audit, rate-limit, shared-quota (DC1.iii)

**Identity at the core (M3/M4).** Two identity classes, both resolved from serve-injected, daemon-verified
headers (serve strips client copies and re-injects verified values — STRABO (c)(iv)):
- **Human operator** (untagged tailnet node): carries `Tailscale-User-Login`. Authorized against an
  operator allowlist (the `<CORE>_OPERATORS` env, generalizing newswire's `NEWSWIRE_OPERATORS`).
- **In-mesh builder** (TAGGED node): does NOT carry `Tailscale-User-Login` (imported assumption 1);
  carries `Tailscale-App-Capabilities`. Authorized against the **tag/capability**, not a user-login.
  The grant in the Tailscale policy targets `tag:sos-core-client`; the core reads the capability and
  maps it to the `builders` identity class.

Both classes are checked **per operation**: `PROVIDER_REGISTRY[provider].operations[op].scopes` declares
which identity classes may invoke it. An identity outside the op's `scopes` -> `403`, no egress, audited.
This is M4 closed: authorization is per-(identity-class, provider, operation), deny-by-default — an
identity authorized for `vertex.embed` is NOT thereby authorized for any future `provider.dangerous_op`.

**The loopback-bind precondition (M3, the crux).** The handler MUST listen ONLY on a `0600` AF_UNIX
socket (or loopback), NEVER `0.0.0.0`. `tailscale serve --https=443 unix:/run/.../core.sock` (supported
TS >= 1.94.1). With no network-reachable listener, the identity headers are trustworthy because the
ONLY path to the handler is through serve, which strips-and-reinjects. If the handler bound a routable
address, a colocated process could connect directly and forge identity — the entire model collapses.
This is the single load-bearing binding constraint (STRABO nuance 2 / POLYBIUS spot-check).

**Audit (M5).** Every `/call` produces a durable structured audit record BEFORE returning:
`{ts, identity_class, identity (login or tag), provider, operation, outcome (ok|rejected|forbidden|provider_error|rate_limited), upstream_status, latency_ms}`.
NEVER the params values, NEVER any credential, NEVER the response body — names/refs/outcomes only (the
same value-free discipline the provisioner enforces, applied to the runtime audit log). Audit is
write-before-respond so a crash cannot drop the record of an attempted call.

**Rate-limit + shared-quota (M6).** Two layers:
- **Per-identity token-bucket rate limit** at the core (e.g. N calls/identity/window), refused with
  `429` + audited `rate_limited`. Closes single-caller flood.
- **Shared-quota fairness for Vertex/Gemini:** a core-level concurrency cap + a per-identity share of
  the shared Vertex quota, so one operator/skill cannot starve the shared Gemini quota (the explicit
  shared-Gemini-quota concern from sos--373). Over-cap calls are `429`-throttled, not queued unboundedly.

**Funnel OFF (no public ingress).** The core has no public door; `serve` is private-tailnet only.
Verified separate-opt-in (STRABO (c)(i)). M1's external-reachability variant is closed: the box is not
internet-reachable inbound at all.

### §1.5 DC1 threat -> mitigation -> probe map (the gate-relevant output; 6.12 A3 author duty + 6.13)

Each row: mitigation (closed by construction where possible) + a threat-anchored probe (6.13: exercises
the named attack path, asserts BOTH attack-blocked AND legit-unaffected). These probe specs are
**design-time** for the FUTURE core service (built in the later gated arc); ADA does NOT execute them
this gauntlet (DC3 is mock-emit only). They are the falsifiable checks ARGUS evaluates and VERA/CATO
re-run when the core is built. Each has a stable probe-id.

| M# | Mitigation (how closed) | Threat-anchored probe (id) |
|----|-------------------------|-----------------------------|
| **M1** SSRF | **By construction:** no caller-supplied URL/host exists. Destination is built from a closed server-side registry (URL template + server-pinned slots). | **P-M1:** (a) POST `/call` with a `params` that tries to inject a URL/host/redirect (e.g. `params.url`, `params.project=169.254.169.254`, an extra `endpoint` key) -> asserts `400`, NO outbound request leaves the box (egress mock/recorder shows zero non-registry hosts contacted). (b) a legit `{vertex, generate_grounded, {valid contents}}` -> reaches ONLY the pinned `*-aiplatform.googleapis.com` host, succeeds. |
| **M2** key-exfil | **By construction:** credential is attached server-side from Railway secret -> registry; redaction pass strips credential/auth headers from all response + error bodies; audit log is value-free. | **P-M2:** (a) drive an upstream error that echoes an auth header (mock provider returns `401` with the `Authorization` header echoed) -> assert the caller-facing response contains NO credential bytes and NO `Authorization`/`x-goog-api-key` value; grep the audit record for the (mock) secret value -> absent. (b) a legit call returns the provider payload intact (redaction did not break the feature). |
| **M3** identity forgery | **By construction:** handler binds a `0600` AF_UNIX socket; serve strips+reinjects identity; no routable listener. | **P-M3:** (a) attempt a direct connection to the handler bypassing serve (connect to a TCP port / non-serve path) AND send a forged `Tailscale-User-Login` -> assert connection refused (no routable listener) OR header ignored (only serve-injected accepted); `ss`/`netstat` shows the handler bound to the unix socket / loopback, NOT `0.0.0.0`. (b) a real serve-routed operator call carries the verified header and is authorized. |
| **M4** over-broad authz | **By construction:** per-(identity-class, provider, operation) `scopes` check, deny-by-default. | **P-M4:** (a) an identity authorized for `vertex.embed` calls a different op NOT in its scopes -> `403`, no egress, audited `forbidden`. (b) the same identity calls `vertex.embed` (in scope) -> authorized, succeeds. |
| **M5** audit gap | Write-before-respond durable structured record for every call, value-free. | **P-M5:** (a) issue ok / rejected / forbidden / rate_limited calls -> assert each produced exactly one durable audit record with correct outcome, identity, provider, operation; crash-inject after egress-before-respond -> the record still exists (write-before-respond). (b) audit record contains NO param values / NO credential. |
| **M6** quota DoS | Per-identity token-bucket + shared-quota concurrency cap; `429` over-cap. | **P-M6:** (a) one identity bursts > N calls/window -> the (N+1)th is `429` `rate_limited`, audited; under load the shared-quota cap holds (no unbounded queue). (b) a SECOND identity issuing in-policy low-rate calls is NOT throttled (the limit is per-identity; the mitigation did not break the feature for everyone). |

---

## §2 DC3 — The cookie-cutter emit (MOCK-ONLY; the ONLY thing ADA builds this gauntlet)

The core SERVICE is designed above. To STAND IT UP, the existing value-free provisioning emitter runs
sos--373's services through `resolve -> emit_spec` to produce a names-only `ProvisioningSpec`. The frozen
resolver (`resolve.py`) stays **byte-identical**; the 3-wall tripwire holds; `assert_value_free` passes.
The ONLY new code is **two additive catalog TOML records** + a demonstration script. No edit to
`spec.py`, `port.py`, `mock.py`, `resolve.py`, `dataload.py`, `baseline.toml`, or `kinds.toml`.

### §2.1 Why no kinds.toml / baseline.toml / pairing edit is needed (ground-checked against the machinery)

- **pgvector + gemini-search + gemini-embedding + DATABASE_URL + POSTGRES_PASSWORD are ALREADY baseline**
  (`baseline.toml`, confirmed). The embeddings DB needs zero catalog work — it is the baseline.
- **`thirdparty_rest_key` is already an expected kind** (`kinds.toml` `kind_enum`; `EXPECTED_KIND_ENUM`
  in `dataload.py`). Tailscale's `TS_AUTHKEY` slot uses it directly.
- **`gcp_api` + paired `gcp_secret` is the existing pairing shape** (google-maps.toml: `gcp_api =
  "google-maps"` + `[[entries]] gcp_api google-maps` + `[[entries]] gcp_secret MAPS_API_KEY`). The Vertex
  record follows this EXACTLY: `gcp_api = "aiplatform"` + paired `gcp_secret` SA-key slot.
- **The Vertex pairing does NOT need a `kinds.toml [[key_bearing_pairing]]` row.** That table drives
  `check_runtime_completeness` (a `gcp_api` that is key-bearing must have its paired secret resolved).
  Vertex authenticates via a **service-account (ADC)**, not an API key bound 1:1 to the `aiplatform`
  API call. The SA-key `gcp_secret` is the SA credential slot, not a per-API key in the google-maps
  sense. Adding a `key_bearing_pairing` row would be **semantically wrong** (it would assert "the
  aiplatform API is unusable without secret X resolved in the same set"), and it would require editing
  `kinds.toml` — out of scope and unnecessary. **DECISION: no `key_bearing_pairing` row for Vertex.** The
  SA-key slot is emitted as an ordinary `gcp_secret` (scope-bearing -> per-secret accessor in
  `derive_sa_scope`), which is exactly right. (Flagged for ARGUS in §6: this is a deliberate divergence
  from the google-maps pairing — justified because Vertex is SA-auth, not API-key-auth.)
- **The catalog records must reference a KNOWN category** or `'none'` (`load_catalog` dangling-ref
  check). Vertex/Gemini and Tailscale are not geospatial/document categories; both use **`category =
  "none"`** (the spatial-db.toml precedent uses `gcp_api = "none"` + a real category; here we use
  `category = "none"` because these services do not belong to an emergent discovery category — they are
  baseline-infra-adjacent direct catalog entries). `'none'` is explicitly accepted by `load_catalog`.

### §2.2 New catalog record 1 — `data/catalog/vertex-gemini.toml` (EXACT buildable TOML)

```toml
# author: Denson Smith
# §22 seed record — vertex-gemini. The credentialed pass-through's FIRST provider (gsearch + embeddings).
# Vertex is SERVICE-ACCOUNT (ADC) auth, NOT a standalone API key (2026 key-deprecation; DC2 verified).
# So the paired gcp_secret is the SA-KEY SLOT NAME (server-side ADC), not an API key in the google-maps
# sense — hence NO kinds.toml key_bearing_pairing row (that table is for API-key-bound APIs). The
# gcp_api "aiplatform" + paired gcp_secret GCP_SA_KEY_B64 ride the SAME entries shape as google-maps.
# Validated fail-closed by dataload.load_catalog (§2.4.1).

service-id = "vertex-gemini"
gcp_api = "aiplatform"
category = "none"

[[entries]]
kind = "gcp_api"
name = "aiplatform"

[[entries]]
kind = "gcp_secret"
name = "GCP_SA_KEY_B64"

# §25 detection_hints — ADDITIVE, ADVISORY recognition signals only. load_catalog IGNORES this block
# (reads only entries/gcp_api/category — byte-unchanged); load_detection_hints reads + fail-closed-validates.
[detection_hints]
sdk_imports  = ["google.genai", "google-genai", "vertexai", "google.cloud.aiplatform"]
url_patterns = ["aiplatform.googleapis.com", "generativelanguage.googleapis.com"]
config_keys  = ["GCP_SA_KEY_B64", "GOOGLE_APPLICATION_CREDENTIALS", "GOOGLE_CLOUD_PROJECT"]
data_signals = ["embedding-generate", "grounded-search", "gemini-generateContent"]
```

Emit consequence: `aiplatform` joins `apis` (the `gcp_api` set, scope-bearing -> API role); `GCP_SA_KEY_B64`
joins `secret_slots` as a `gcp_secret` with `acquisition = "mint-via-gcp-console"` (per
`_derive_acquisition`: a key-bearing `gcp_secret` that is not POSTGRES_PASSWORD / TS_AUTHKEY) and joins
`sa_scope` as a per-secret accessor.

### §2.3 New catalog record 2 — `data/catalog/tailscale.toml` (EXACT buildable TOML)

```toml
# author: Denson Smith
# §22 seed record — tailscale. The in-mesh transport identity for the secure core. TS_AUTHKEY is a
# thirdparty_rest_key (already an expected kind) — the tagged, reusable auth-key the container joins the
# tailnet with. NO gcp_api (the auth-key is not a GCP surface): gcp_api = "none" -> natively skips S1
# enablement (the spatial-db.toml precedent for a non-GCP service). Validated fail-closed by load_catalog.

service-id = "tailscale"
gcp_api = "none"
category = "none"

[[entries]]
kind = "thirdparty_rest_key"
name = "TS_AUTHKEY"

# §25 detection_hints — ADDITIVE, ADVISORY. load_catalog ignores it; load_detection_hints validates it.
[detection_hints]
sdk_imports  = ["tailscale"]
url_patterns = ["api.tailscale.com", "*.ts.net"]
config_keys  = ["TS_AUTHKEY", "TS_USERSPACE"]
data_signals = ["tailnet-join", "serve-https", "mesh-ingress"]
```

Emit consequence: `TS_AUTHKEY` joins `secret_slots` as a `thirdparty_rest_key` with `acquisition =
"mint-via-thirdparty"` (per `_derive_acquisition`); it is scope-bearing -> per-secret accessor in
`sa_scope`; `gcp_api = "none"` means it contributes NO API to `apis` (skips S1 enablement). No
`gcp_secret`, no `key_bearing_pairing` (a `thirdparty_rest_key` is never API-key-paired by the
google-maps mechanism).

### §2.4 The manifest the core builder resolves (the cookie-cutter INPUT)

The core builder's manifest names a category and adds the two new services via `delta.add`. Because both
new catalog records are `category = "none"`, they are added by explicit `delta.add` of their entries (they
are not pulled in by an emergent category). The baseline already carries pgvector + gemini + DATABASE_URL
+ POSTGRES_PASSWORD. Illustrative manifest (the demonstration constructs this resolved set):

```
builder slug: sos_core
baseline (always):    (gcp_api, gemini-embedding), (gcp_api, gemini-search),
                      (railway_var, DATABASE_URL), (gcp_secret, POSTGRES_PASSWORD),
                      (db_extension, pgvector)
delta.add (from the two new catalog records):
                      (gcp_api, aiplatform), (gcp_secret, GCP_SA_KEY_B64),
                      (thirdparty_rest_key, TS_AUTHKEY)
```

### §2.5 The expected `ProvisioningSpec` (what `emit_spec` emits — exact, for VERA zero-guesswork)

Given the resolved set above and `builder_slug = "sos_core"`, `emit_spec` emits (every collection a
sorted tuple — deterministic):

```
ProvisioningSpec(
  builder_slug = "sos_core",
  project      = "proj-sos_core",
  sa           = "sa-sos_core",
  apis         = ("aiplatform", "gemini-embedding", "gemini-search"),          # sorted gcp_api names
  secret_slots = (
    SlotSpec(name="GCP_SA_KEY_B64",   kind="gcp_secret",          acquisition="mint-via-gcp-console", populated=False),
    SlotSpec(name="POSTGRES_PASSWORD",kind="gcp_secret",          acquisition="generate-locally",     populated=False),
    SlotSpec(name="TS_AUTHKEY",       kind="thirdparty_rest_key", acquisition="mint-via-thirdparty",  populated=False),
  ),                                                                            # sorted by name
  railway_vars = ("DATABASE_URL",),
  db_extensions = ("pgvector",),
  sa_scope = (                                                                  # derive_sa_scope: scope-bearing only, sorted
    ("gcp_api", "aiplatform"), ("gcp_api", "gemini-embedding"), ("gcp_api", "gemini-search"),
    ("gcp_secret", "GCP_SA_KEY_B64"), ("gcp_secret", "POSTGRES_PASSWORD"),
    ("thirdparty_rest_key", "TS_AUTHKEY"),
  ),
  needs_postgis_base_image = False,                                             # no postgis in the set
  budget_boundary_required = True,
)
```

Note the **secret-slot NAMES only** — every `populated=False`, no value anywhere. This is the value-free
spec: the Vertex SA key, the Postgres password, and the Tailscale auth-key are all NAMES the human/CI
populates out-of-package (DC4), never values the emitter holds.

### §2.6 The mock-emit demonstration (what ADA builds + runs — exact steps for VERA re-execution)

ADA writes a demonstration script (e.g. `agents/builder-deploy-core/demo/sos_core_emit_demo.py`) and the
two catalog TOML files above. The demonstration:

1. Loads the catalog via `dataload.load_catalog()` -> asserts both new records load (fail-closed
   validation passes; `vertex-gemini` and `tailscale` present in the returned catalog dict).
2. Builds the resolved set (baseline + the two records' entries via a `category="none"` manifest with
   `delta.add`), calls `resolve(...)` -> asserts the resolved set equals §2.4 (sorted).
3. Calls `emit_spec(resolved, "sos_core")` -> asserts the `ProvisioningSpec` equals §2.5 EXACTLY
   (golden-file / field-by-field equality; `apis`, `secret_slots`, `sa_scope` sorted as shown).
4. Calls `assert_value_free(spec)` -> passes (no `ValueLeakError`).
5. Drives the spec against `MockProvisioner()` (default: everything unpopulated) -> asserts S2c BLOCKS
   (the human-gate fail-closed: secret slots unpopulated halts before S3/S5); then against
   `MockProvisioner(populated={"GCP_SA_KEY_B64","POSTGRES_PASSWORD","TS_AUTHKEY"})` -> asserts S3-S6 run
   (synthetic ids only, NO value held); `assert_value_free` on the resulting `RunLedger` passes.
6. Calls `mock.stand_up_mesh_shape("sos_core")` -> asserts the value-free `MeshShape` (socket_mode
   `0600`, transport `af_unix`, identity_header `Tailscale-User-Login`, deny_by_default True, funnel_off
   True, `<VERB>` placeholder) — the 501-until-T3 scaffold the DC1 core fills at T3.

**Tripwire / frozen-resolver assertions the demonstration + suite must satisfy (the regression bar):**
- **W1** (no-I/O imports) grep over `provision/` returns EMPTY (no new I/O imports; the demo lives
  OUTSIDE `provision/`, under `demo/`, so it does not pollute the W1 surface).
- **W2** MockProvisioner remains the only concrete `Provisioner`.
- **W3** `emit_spec` takes no provisioner and does no I/O.
- **`resolve.py` blob is byte-identical** (`git show HEAD:...resolve.py` hash == working-tree hash).
- **The FULL `builder_deploy_core` test suite is green** (the catalog additions re-derive resolution and
  re-run `load_catalog`; the full suite catches any regression the two records introduce elsewhere — per
  the gauntlet-verify full-suite discipline).

### §2.7 DC3 threat-coverage note (6.12 self-classification)

The DC3 work (two additive catalog records + a demonstration) is a **process/data change with no runtime
attack path** — it emits NAMES only against a MockProvisioner, touches no real infra/creds/network.
**PROPOSED classification: NOT threat-ratified (data/config addition, no runtime attack path; §35.5
carve-out — emit-only, value-free, mock).** ARGUS confirms. The named threats M1..M6 live entirely in the
DC1 core-service design (the future build); DC3 carries no threat-anchored probe of its own beyond the
value-free / tripwire / frozen-resolver assertions above.

---

## §3 DC4 — Credential-discipline boundary (who may do what)

The agent/package NEVER holds or sees a secret value. The boundary, composing `credential-discipline`
(CI/WIF), `railway-keyring-deploy` (local), and the newswire mesh pattern:

| Secret | Minted/set by (OUT-of-package human/CI step) | The agent/package may | The value lives |
|--------|----------------------------------------------|------------------------|-----------------|
| **Vertex SA + key** (`GCP_SA_KEY_B64`) | HUMAN/CI: create the SA in the core's GCP project, grant least-priv (`roles/aiplatform.user` OR the custom `aiplatform.endpoints.predict` role — DC2 (a)(iii)); prefer **WIF** (workload-identity federation, no long-lived key) where the runtime supports it, else a key JSON -> base64 -> set as a Railway secret. | emit the SLOT NAME `GCP_SA_KEY_B64`; reference it in the registry as `auth: adc_sa`. NEVER decode/print/log it. | Railway secret (server-side); decoded to a `0600 /tmp` file at core startup (newswire `bootstrap_adc` pattern), `GOOGLE_APPLICATION_CREDENTIALS`, never str/repr/logged. |
| **Postgres password** (`POSTGRES_PASSWORD`) | HUMAN/CI: generate locally (`acquisition="generate-locally"`); set as a Railway secret on `db` + injected into the private `DATABASE_URL`. | emit the SLOT NAME. | Railway secret; `DATABASE_URL` private (`*.railway.internal`), in-network only. |
| **Tailscale auth-key** (`TS_AUTHKEY`) | HUMAN: mint a **reusable, TAGGED** (`tag:sos-core-node`) auth-key in the Tailscale admin console (`acquisition="mint-via-thirdparty"`); set as a Railway secret. | emit the SLOT NAME. | Railway secret; consumed by `tailscaled` at container start (userspace, `TS_USERSPACE=true`). |
| **Provider keys** (future providers beyond Vertex) | HUMAN/CI per provider: set as Railway secrets, registered in `PROVIDER_REGISTRY[provider].auth`. | emit the SLOT NAME; reference in the registry. | Railway secret (server-side); attached by the core, never returned to the caller. |

**The builder holds ONLY a tailnet identity** — no Railway token, no SA key, no API keys, no provider
keys. It reaches the core over the mesh with its tagged tailnet identity; every credentialed call runs
server-side on the core. The Railway PAT itself (for the out-of-package deploy step) lives in the
OS keyring per `railway-keyring-deploy`; the agent never holds it. This is the whole point of the design:
the recurring "keys on the builder machine" problem is structurally removed.

---

## §4 DC5 — First-slice PLAN (design only; build is a follow-on after the gate + provision-go)

The build sequence once the design is gated AND the PRINCIPAL gives provision-go (each a separate gated
action; NOT this gauntlet):

1. **Provision the core (2.4-PROVISION step).** Run the DC3-emitted spec for real (real Railway project
   `proj-sos_core`, real GCP SA, real tagged Tailscale node, real budget cap). Out-of-package human/CI
   does the credential steps (DC4). `db` = Postgres+pgvector (bring-your-own `pgvector/pgvector` or
   `timescaledb-ha:pgNN` image + `CREATE EXTENSION vector` — DC2 (b)(v)); `serving` = the pass-through
   core service.
2. **Wire Vertex/Gemini as the FIRST provider through the pass-through.** Register `vertex` in
   `PROVIDER_REGISTRY` with `generate_grounded` (grounded search, the gsearch surface — DC2 (a)(iii))
   and `embed` operations, both `auth: adc_sa`. This is the T3 product that fills the `<VERB>` 501 stub.
3. **Build gsearch as the FIRST thin-client skill — ONCE, as a core-client (SUPERSEDES sos--g8q).**
   sos--g8q's local-keyring gsearch is NOT rebuilt; gsearch becomes a thin client that POSTs
   `{provider:"vertex", operation:"generate_grounded", params:{...}}` to the core over the mesh and
   returns the grounded result. sos--g8q becomes dependent on the core. (The thin-client skill itself is
   built in stoa_of_science — it is the CLIENT side; this design specifies only the client CONTRACT,
   §1.3.) No API key on the builder.
4. **Stand up the embeddings DB + point the KG pipeline at it.** The pgvector DB on `db` is the home for
   BOTH the knowledge-graph pipeline store AND skill/retrieval embeddings (split later only if needed —
   sos--373). Embedding calls go through the SAME pass-through (`{provider:"vertex", operation:"embed"}`),
   so embedding credentials also never touch the builder. Point the KG pipeline's embedding writes at the
   private `DATABASE_URL` (in-network) and its embedding generation at the core's `embed` operation.

Sequencing note (DC2 (b)(i)): Railway private networking is runtime-only — the DB connection from
`serving` to `db` must be established at runtime (start command), not build-time. The volume on `db` is
mounted (no zero-downtime redeploy while mounted — acceptable for the DB; DC2 (b)(iv)).

---

## §5 DC6 — Honest stance + threat posture

**How the SSRF/key-exfil surface is closed BY CONSTRUCTION (no over-claim):**
- **SSRF (M1): closed by construction** — there is no caller-supplied URL/host/destination input. The
  caller names a `provider` + `operation` from a closed server-side registry; the destination is built
  entirely from server-pinned templates. This is not "an allowlist that filters URLs" (a filter is a
  bypass surface); it is "no URL input exists." That is a stronger claim and it holds only as long as the
  registry's `url_slots` stay server-pinned enums/fixed — if a future operation accepts a free-form host
  slot, M1 reopens. ARGUS should audit every registry operation's `url_slots` for caller-influence.
- **Key-exfil (M2): closed by construction at the channel level** — credentials are attached server-side
  and the audit log + response path are value-free/redacted. The residual is **redaction completeness**:
  a provider that echoes a key in a novel response field the redaction pass doesn't cover would leak.
  The redaction pass is allow-list-shaped (return only the declared payload fields) rather than
  deny-list-shaped (strip known-bad) to make this robust — but a misimplemented redactor is a real risk.
  ARGUS/VERA should push on P-M2 hard.
- **Identity (M3): closed by construction IFF the loopback/0600-socket bind holds.** This is the single
  load-bearing precondition; if the handler ever binds a routable address, the entire identity model is
  forgeable. The design pins it; the build must enforce it; VERA must verify the actual bind at build
  time (P-M3). This is the place the design is most fragile to an implementation slip.

**What this design does NOT claim:** it does not claim the core is invulnerable if the Railway secret
store itself is breached (a Railway-level compromise exposes the keys regardless — that is the platform's
trust boundary, mitigated by least-priv SA scope + budget cap to bound blast radius, not eliminated). It
does not claim quota fairness is perfect under adversarial load — only that single-caller flood and
gross shared-quota starvation are bounded by the rate-limit + concurrency cap.

This component is **threat-ratified** (the DC1 core design); ARGUS owns the security verdict. The DC3
emit is **not threat-ratified** (process/data change, no runtime attack path — §2.7).

---

## §6 Self-assessed weak points (6.2 post-work; where ARGUS should push hardest)

1. **Tagged-builder identity is the biggest divergence from the newswire precedent and the least-proven
   part.** Newswire only ever served human operators carrying `Tailscale-User-Login`. The in-mesh builder
   is a TAGGED node that does NOT get that header (imported assumption 1) — the design keys builder
   authorization off `Tailscale-App-Capabilities` / the tag. STRABO/POLYBIUS web-verified that tagged
   devices don't populate user-login headers, but the EXACT mechanism for mapping an App-Capabilities
   value to a `builders` identity class (and how serve injects/verifies it for a tagged node) is the
   thinnest-grounded design surface. **ARGUS should push: is the tag/capability path as forgery-resistant
   as the user-login path? Does it ALSO require the 0600-socket bind precondition (it does — but confirm
   serve strips/reinjects App-Capabilities the same way it does user-login).**
   *Why this shape anyway:* the requirement mandates the builder reach the core holding ONLY a tailnet
   identity, and a tagged node is the correct tailnet primitive for a non-human automated client; keying
   off the tag is the only sound option short of giving the builder a user identity (worse).

2. **Redaction-pass completeness (M2 residual).** "Closed by construction" for key-exfil rests on the
   response/error redactor being allow-list-shaped and correct. A provider echoing a key in an
   unanticipated field, or a redactor bug, would leak. **ARGUS should push on whether allow-list
   redaction (return only declared payload fields) is actually implementable for every provider's
   response shape, or whether some operations need to pass through opaque bodies (reopening the risk).**
   *Why this shape anyway:* allow-list redaction is strictly safer than deny-list; the alternative
   (no redaction, trust the provider not to echo) is unacceptable for a box holding all keys.

3. **The `category="none"` catalog choice for Vertex/Tailscale.** These two services don't belong to an
   emergent discovery category, so they're added by explicit `delta.add` rather than pulled in by a
   category. This is correct against `load_catalog` (which accepts `'none'`), but it means the core
   builder's manifest must explicitly add them — they won't be auto-suggested by the discovery layer.
   **ARGUS should confirm this is intended (it is, for an infra-adjacent core) and not a gap in the
   discovery story.**
   *Why this shape anyway:* forcing these into a fake category to make discovery pick them up would
   corrupt the emergent-category semantics; explicit `delta.add` is honest.

4. **No `key_bearing_pairing` row for Vertex (the SA-auth vs API-key-auth divergence).** google-maps pairs
   `gcp_api -> gcp_secret` so `check_runtime_completeness` enforces the API key is present. Vertex is
   SA-auth (ADC), so the SA-key slot is the credential, not a per-API key — adding a pairing row would be
   semantically wrong AND would edit frozen-adjacent `kinds.toml`. **ARGUS should confirm omitting the
   pairing row is correct (the `aiplatform` API is usable via the SA without a per-API-key-in-the-set
   invariant) and not a silently-dropped completeness check.**
   *Why this shape anyway:* the pairing table models API-key-bound APIs; Vertex isn't one. Encoding a
   false pairing to satisfy a pattern would be the actual bug.

5. **The threat-anchored probes (P-M1..P-M6) are design-time specs for a service not built this gauntlet.**
   They are falsifiable and concrete, but they exercise the FUTURE core service; ADA does not run them now
   (DC3 is mock-emit only). The risk: a probe that reads clean on paper may be unimplementable or
   under-specified against the real serve/socket runtime. **ARGUS should pressure-test P-M3 especially
   (the bind-verification probe) — it is the load-bearing one and the most runtime-dependent.**
   *Why this shape anyway:* the gauntlet's job is a buildable design that relays up to be gated; the
   probes are the verification contract the later build arc executes — specifying them now is exactly the
   A3 author duty (6.13).

---

## §7 Out of scope (deliberately not addressed; ADA scope-fence + ARGUS frame)

- **ALL real provisioning** — no Railway project, no GCP SA mint, no Railway secret set, no Tailscale
  node, no DB stand-up. Waits for the Grand's gate + the PRINCIPAL's provision-go (the 2.4-PROVISION
  step). *Reason: the design may change at the gate; emit-only/mock this gauntlet.*
- **The core SERVICE code** — DESIGNED here (DC1), NOT built. ADA builds ONLY the DC3 mock-emit.
  *Reason: directive scope; the service is a later gated build arc.*
- **The first-slice BUILD** (gsearch thin-client, embeddings stand-up) — PLANNED (DC5), not built.
  *Reason: follow-on after gate + provision-go.*
- **The stoa_of_science CLIENT skills** — theirs. This design specifies the client CONTRACT (§1.3) only.
  *Reason: ownership split per sos--373; client skills built in stoa_of_science.*
- **Multi-provider registry beyond Vertex** — the design accommodates it (the registry is N-provider),
  but only Vertex is specified now. *Reason: Vertex is the first provider; others added per-provider
  later, each following the §1.3 registry shape + §3 credential boundary.*
- **arc-75 (bw-bootstrap)** — parked, separate. *Reason: unrelated; not touched here.*
