---
author: Denson Smith
seat: CAPTAIN_STRABO_the_stoa (SCOUT — external web research)
ticket: stoa--q7f
requirement: sos--373
arc: stoa--q7f (u--9s2 inc 2.4 — DESIGN gauntlet, secure Railway core for stoa_of_science)
fetched: 2026-06-28
verification_status: needs-vera
---

# DC2 — Third-party capability-premise verification

**Question.** Do the third-party capability premises the secure-Railway-core design rests on
(Vertex/Gemini auth, Railway platform features, Tailscale serve/ACL/identity) hold against
CURRENT (2026) primary sources — not training memory?

**Design decision fed.** Whether DAEDALUS can design the credentialed per-provider pass-through +
pgvector embeddings core (DC1) on these premises, or whether any premise is a DESIGN-BLOCKER that
forces a different shape. A premise that does not verify must surface, not be papered over.

**Method.** `gsearch` (Vertex-grounded Google search, real source URLs) + direct `WebFetch` on
official docs (ai.google.dev, docs.cloud.google.com, docs.railway.com, tailscale.com/kb). Each
premise tagged VERIFIED / VERIFIED-WITH-NUANCE / UNVERIFIED / CONTRADICTED with the source +
as-of date inline. Verification-complexity quadrant tagged per premise for VERA's sampling
(doc-claim = hard-to-fabricate-easy-to-check where a primary URL is cited).

All citations fetched **2026-06-28**.

---

## Cluster (a) — Vertex / Gemini auth

### (a)(i) Gemini standalone-API-key deprecation timeline — **VERIFIED**
The requirement's claim ("unrestricted standalone keys stopped 2026-06-19; all standard keys
rejected ~Sept 2026") is confirmed against the **primary** Google doc, verbatim:

- 2026-06-19: "The Gemini API will reject requests from **unrestricted standard keys**." Standard
  keys with explicit API restrictions continue functioning temporarily.
- September 2026: "The Gemini API will reject requests from **Standard keys**." Full migration to
  auth keys mandatory.
- New keys created in Google AI Studio are now auth keys by default; **auth keys are "bound
  directly to a Google Cloud service account"** and requests run "under the identity of that bound
  service account."

Citation: [Google — Gemini API keys (official)](https://ai.google.dev/gemini-api/docs/api-key) — fetched 2026-06-28. (quadrant: easy-to-check — exact dates quoted from a primary Google page.)

### (a)(ii) Vertex AI is service-account / ADC auth (not a standalone API key) — **VERIFIED**
The `google-genai` client authenticates to Vertex with **Application Default Credentials** — a
service-account JSON via `GOOGLE_APPLICATION_CREDENTIALS`, or an attached SA — by constructing
`genai.Client(vertexai=True, project=..., location=...)` and **omitting** the api_key. This is the
documented, production-recommended path and is the exact model the newswire precedent already runs
server-side (`embed/auth.py::bootstrap_adc()` base64 SA-key -> 0600 /tmp file -> ADC). So the
core authenticating to Vertex with an SA (not an API key) is sound and survives the (a)(i)
deprecation.

Citation: [Google — Authentication for Vertex AI / google-genai SDK (ADC vs API key)](https://ai.google.dev/gemini-api/docs/migrate-to-cloud) (gsearch-grounded, google.dev primary) — fetched 2026-06-28; corroborated by the in-mesh newswire precedent (`~/.claude/skills/newswire-builder-setup/SKILL.md` §7). (quadrant: easy-to-check.)

### (a)(iii) Vertex grounded-search surface + SA role — **VERIFIED**
Vertex AI supports **Grounding with Google Search** for Gemini (the `google_search` tool;
responses carry `groundingMetadata`) on the Vertex surface — the right surface for a gsearch-style
call. The SA needs **`roles/aiplatform.user`** (Vertex AI User) to call `generateContent`; Google
also officially documents a **least-privilege custom role** with only
`aiplatform.endpoints.predict` (+ `aiplatform.endpoints.computeTokens`) for an SA that strictly
invokes Gemini — relevant to the credential-discipline / minimal-blast-radius posture.

Citations:
- [Google Cloud — Grounding with Google Search (Vertex AI)](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/grounding/grounding-with-google-search) — fetched 2026-06-28 (301 from `cloud.google.com` -> `docs.cloud.google.com`; note the host move).
- [Google Cloud — Vertex AI access control / aiplatform.user + custom-role least-priv](https://docs.cloud.google.com/vertex-ai/docs/general/access-control) (gsearch-grounded, cloud.google.com primary) — fetched 2026-06-28. (quadrant: easy-to-check.)

**Cluster (a) verdict: PASS.** All three premises verified; the SA-only auth path survives the key
deprecation; the grounded-search surface and SA role exist.

---

## Cluster (b) — Railway

### (b)(i) `*.railway.internal` private DNS / IPv6 mesh — **VERIFIED**
Services receive a private DNS name `SERVICE_NAME.railway.internal` (auto-injected as
`RAILWAY_PRIVATE_DOMAIN`); the private network is IPv6-based. **Runtime-only** — private
networking is NOT available during the build phase (DB migrations must run from the start command,
not the build step). DAEDALUS must keep any cross-service (serving <-> db) connectivity at runtime,
not build-time.

Citation: [Railway — Private Networking](https://docs.railway.com/guides/private-networking) — fetched 2026-06-28. (quadrant: easy-to-check.)

### (b)(ii) Secret / variable store — **VERIFIED**
Service variables and shared (project-level) variables are injected into the container at runtime;
Railway also auto-injects system vars (`RAILWAY_PRIVATE_DOMAIN`, `PORT`, etc.). This is the channel
for `GCP_SA_KEY_B64`, `TS_AUTHKEY`, `DATABASE_URL`, and per-provider keys — matching the newswire
SERVICE_VARS precedent (the agent never holds them; set out-of-package by human/CI per
credential-discipline).

Citation: [Railway — Variables](https://docs.railway.com/guides/variables) (gsearch-grounded, railway.com primary) — fetched 2026-06-28. (quadrant: easy-to-check.)

### (b)(iii) `tailscaled` + `tailscale serve` inside a Railway container — **VERIFIED-WITH-NUANCE**
Running tailscaled inside a Railway container is supported via **userspace-networking**
(`TS_USERSPACE=true`) — **no TUN device required**, which is what makes it work on Railway's
container runtime. This matches the newswire embedded pattern (tailscaled userspace in the serving
container).

**NUANCE (for DAEDALUS — NOT a blocker):** in userspace mode, **`tailscale serve` INBOUND works
out-of-the-box, but OUTBOUND traffic from the container to the rest of the tailnet does NOT
auto-route** (it needs `TS_SOCKS5_SERVER` / `TS_OUTBOUND_HTTP_PROXY_LISTEN`). This is **irrelevant
to this design**: the pass-through's outbound calls (to Vertex / external provider APIs) are normal
**public-internet egress**, not tailnet traffic; only the **operator-agent -> core ingress** uses
`tailscale serve`. So the design needs serve-inbound (verified working) and never needs
tailnet-outbound. DAEDALUS should state this explicitly so a reviewer doesn't mistake it for a gap.

Citations:
- [Tailscale — Run Tailscale in a Docker container / userspace (TS_USERSPACE)](https://tailscale.com/kb/1282/docker) — fetched 2026-06-28.
- [Railway community — Tailscale on Railway userspace pattern + volume at /var/lib/tailscale](https://docs.railway.com) (gsearch-grounded; railway.com + tailscale.com primaries) — fetched 2026-06-28.
- inbound-yes/outbound-needs-proxy nuance: [Tailscale — serve in userspace / outbound proxy](https://tailscale.com/kb/1242/tailscale-serve) (gsearch-grounded) — fetched 2026-06-28. (quadrant: medium — capability claim cross-checked against the live newswire precedent.)

### (b)(iv) Persistent volumes (Postgres data) — **VERIFIED**
Railway supports persistent volumes (one per service) mounted at a path. Caveats DAEDALUS should
encode: **no zero-downtime deploy while a volume is mounted** (brief offline unmount/remount on
redeploy — fine for the db); volumes can grow (live-resize on paid plans) but **cannot shrink**;
~2-3% capacity is filesystem-metadata overhead. The newswire precedent already relies on a volume
at `/var/lib/tailscale` to stabilize the node identity (landmine §6.7) — same mechanism.

Citation: [Railway — Volumes](https://docs.railway.com/guides/volumes) (gsearch-grounded, railway.com primary) — fetched 2026-06-28. (quadrant: easy-to-check.)

### (b)(v) Postgres + pgvector — **VERIFIED**
pgvector runs on Railway via **bring-your-own image** (`pgvector/pgvector` or the
`timescaledb-ha:pgNN` image the newswire uses) + `CREATE EXTENSION vector;` then standard
`vector(N)` columns and `<=>` distance ops. Community HA templates ship pgvector pre-installed.
This matches the requirement's pgvector-in-baseline (NOMOS already confirmed `db_extension` in
`baseline.toml` in-repo). Use the **private** `DATABASE_URL` for in-network (serving -> db)
connections; the public URL only for external GUI access.

Citation: [Railway — pgvector / Postgres image + CREATE EXTENSION vector](https://docs.railway.com/guides/postgresql) (gsearch-grounded, railway.com primary) — fetched 2026-06-28; baked-init precedent: newswire SKILL.md §1 (`FROM timescaledb-ha:pg18`). (quadrant: easy-to-check.)

**Cluster (b) verdict: PASS-WITH-NUANCE.** All five Railway premises verified. The one nuance
(userspace serve = inbound-only, outbound needs a proxy) does not bite this design because the
core's egress is public-internet, not tailnet. No blocker.

---

## Cluster (c) — Tailscale (version-sensitive)

### (c)(i) `tailscale serve` is private; Funnel is a separate opt-in — **VERIFIED**
`tailscale serve` shares a local service **securely within the tailnet** (private). **Funnel** is a
**separate** feature that exposes a service **publicly to the internet** and must be explicitly
opted into. **Funnel OFF => no public ingress** — exactly the requirement's "reached ONLY over
Tailscale" posture. (Matches newswire §2 "Funnel OFF (private mesh only).")

Citation: [Tailscale — Serve (vs Funnel)](https://tailscale.com/kb/1242/tailscale-serve) — fetched 2026-06-28. (quadrant: easy-to-check.)

### (c)(ii) Tagged auth keys (ephemeral / reusable) — **VERIFIED**
An auth key can be **bound to an ACL tag** (`tag:...`), and minted as **reusable** and/or
**ephemeral** and/or **preauthorized**. This is what lets the container join the tailnet as a
tagged node (`tag:newswire-trigger` in the precedent) so ACL grants can target it. Tag ownership is
declared in the policy file (`tagOwners`).

Citations:
- [Tailscale — Auth keys](https://tailscale.com/kb/1085/auth-keys) — fetched 2026-06-28.
- [Tailscale — ACL tags](https://tailscale.com/kb/1068/acl-tags) — fetched 2026-06-28. (quadrant: easy-to-check.)

### (c)(iii) Deny-by-default ACL (grants model) — **VERIFIED**
Tailscale policy is **default-deny**: nothing is permitted until an explicit **grant**
(`src`/`dst`/`ip`) allows it. The current `grants` block is the model (replacing legacy `acls`).
This is the requirement's "deny-by-default, then explicit grants" posture — the precedent's policy
(§4) grants only `group:operators -> tag:newswire-trigger : tcp:443` with no global allow-all.

Citation: [Tailscale — Grants (default-deny policy)](https://tailscale.com/kb/1324/grants) — fetched 2026-06-28. (quadrant: easy-to-check.)

### (c)(iv) `Tailscale-User-Login` serve-injected identity header — **VERIFIED** (the load-bearing one)
`tailscale serve` injects verified identity headers into proxied HTTP requests:
**`Tailscale-User-Login`**, `Tailscale-User-Name`, `Tailscale-User-Profile-Pic`, and
`Tailscale-App-Capabilities`. Critically, **serve STRIPS any client-supplied copies of these
headers before forwarding** ("If Serve finds the following headers on an incoming request, it will
remove them for security reasons, to avoid header spoofing") and re-injects the daemon-verified
values — so the header IS trustworthy. This is the exact mechanism the newswire build settled on
(landmine §6.1: use the serve-injected header, NOT a WhoIs-on-loopback call).

**Version-sensitivity / the newswire landmine — addressed:** the newswire build hit a failure on
**TS 1.98.x** where `WhoIs(127.0.0.1:<peer-port>)` did NOT resolve a serve-HTTPS->loopback
connection (no ProxyMapper mapping) -> denied every operator. The **fix was to abandon WhoIs and
trust the serve-injected header** — which is the **current, documented, recommended** mechanism
(not a version-fragile workaround). So DAEDALUS should design to the **header-trust** model, not
WhoIs. The header approach has a hard precondition the docs spell out and the newswire encoded:
**the backend MUST listen only on loopback / a 0600 AF_UNIX socket** — otherwise an attacker who
reaches the raw port directly can forge `Tailscale-User-Login`. (newswire §6.2: bind a 0600
AF_UNIX socket, `tailscale serve --https=443 unix:/run/.../trigger.sock`, supported TS >= 1.94.1.)

Citations:
- [Tailscale — Serve / identity headers (Tailscale-User-Login; header-stripping)](https://tailscale.com/kb/1242/tailscale-serve) — fetched 2026-06-28.
- [Tailscale — using identity/capability headers; bind backend to localhost best-practice](https://tailscale.com/kb/1312/serve) (gsearch-grounded, tailscale.com primary) — fetched 2026-06-28.
- precedent: `~/.claude/skills/newswire-builder-setup/SKILL.md` §6.1 / §6.2 (TS 1.98.x WhoIs failure; header-trust fix; 0600 AF_UNIX socket, supported TS >= 1.94.1). (quadrant: medium — header NAME quoted from primary doc; version-history corroborated by the precedent's field notes.)

**Cluster (c) verdict: PASS.** All four premises verified against primary Tailscale KB; the
version-sensitive WhoIs landmine is RESOLVED by the header-trust model, which is the current
documented mechanism — DAEDALUS must design to header-trust + loopback/0600-socket binding, not
WhoIs.

---

## DESIGN-BLOCKERS

**None.** Every premise across all three clusters verified against current (2026) primary sources.

Two NUANCES DAEDALUS must encode in the design (each verified, each manageable — neither blocks):

1. **Tailscale serve in userspace = inbound-only.** Outbound container->tailnet does not auto-route.
   Harmless here (the core's egress to Vertex/provider APIs is public-internet, not tailnet; only
   operator->core ingress uses serve). Design must NOT assume the core can reach other tailnet
   nodes without an explicit SOCKS5/HTTP-proxy config — and it doesn't need to.

2. **Identity-header trust requires loopback/0600-socket binding.** `Tailscale-User-Login` is only
   trustworthy because serve strips client copies AND the backend is unreachable except through
   serve. The design MUST bind the trigger/pass-through on loopback or a 0600 AF_UNIX socket (the
   newswire pattern), never `0.0.0.0`, or the whole identity model is forgeable. This is the crux
   ARGUS will cold-audit — flagging it here so it's load-bearing in the design from the start.

## Confidence and gaps

- **Confidence: HIGH.** Every load-bearing claim has a primary-source citation (Google, Railway,
  Tailscale official docs). The two highest-risk premises — Vertex SA-only-auth-survives-deprecation
  and the version-sensitive `Tailscale-User-Login` header — are confirmed against primary docs AND
  corroborated by the live newswire in-mesh precedent.
- **Minor source-host note:** the Vertex grounding/access-control docs now 301-redirect from
  `cloud.google.com` to `docs.cloud.google.com` (host migration in progress). Citations use the
  redirect target. If a citation 404s on re-fetch, try the other host.
- **What would falsify:** Google accelerating the Sept-2026 standard-key cutoff or changing the
  SA-bound-auth-key semantics (re-check ai.google.dev/gemini-api/docs/api-key near Sept 2026);
  Tailscale renaming/removing the `Tailscale-User-Login` header in a future release (the design is
  pinned to the header-trust model, so a header rename is the single point that would force a
  design change — VERA should re-confirm the exact header name at build time and pin the TS version).
- **needs-vera:** this artifact is preliminary until VERA re-fetches the cited URLs and confirms the
  quoted dates/header-names resolve.

---

## r3 FOLLOW-UP — Tailscale tagged-node App-Capabilities identity

**Dispatched by:** PLINY_the-stoa (r3 premise-gap from ARGUS's DC1 cold-audit). DC2's (c)(iv)
verified the **`Tailscale-User-Login`** (human-operator) path explicitly but did NOT separately
verify the **TAGGED in-mesh BUILDER** path — a tagged node has no user login, so the design relies on
`Tailscale-App-Capabilities` (and/or the node TAG) to authorize it. This section closes that gap
against current (2026) Tailscale primary sources. All citations fetched **2026-06-28**.

**Premise under test.** A tagged builder node (automated client, ACL-tagged auth key, NO human user)
can be authenticated at the serve backend via a serve-injected, daemon-verified, forgery-resistant
identity header — the SAME trust model as `Tailscale-User-Login`.

### Item 1 — Does serve inject an identity header for a TAGGED (non-user) source? — **VERIFIED**
A tagged node has **no** user identity (`IsTagged() == true` ⇒ no human owner), so
`Tailscale-User-Login` / `-User-Name` / `-User-Profile-Pic` are **empty/omitted** for it. The header
that identifies/authorizes a tagged caller is **`Tailscale-App-Capabilities`**: serve looks up the
ACL grants for the requesting node, serializes the granted capabilities to JSON, and injects them in
that header. A tagged source WITH an app-capability grant **does** receive
`Tailscale-App-Capabilities` even though its user-login header is empty — this is the documented,
designed behavior for service-account/machine nodes.

- The exact header(s): identity for a tagged source = **`Tailscale-App-Capabilities`** (a JSON object
  keyed by capability name). User-login headers are NOT a usable identity for a tagged node.
- Citations:
  - [Tailscale — Serve (command ref; lists `--accept-app-caps`, "Last validated Jan 26 2026")](https://tailscale.com/kb/1242/tailscale-serve) — fetched 2026-06-28.
  - [Tailscale — Grants: app capabilities](https://tailscale.com/kb/1537/grants-app-capabilities) — fetched 2026-06-28.
  - tagged-node user-login-empty / app-caps-still-injected behavior (gsearch-grounded on tailscale.com primaries): "a device cannot have both a user identity and a tag identity … identity headers … are left empty or omitted … `Tailscale-App-Capabilities` is still injected" — fetched 2026-06-28. (quadrant: easy-to-check — header name + tagged-node behavior quoted from primary docs.)

### Item 2 — How does a tagged node acquire app capabilities; is the value server-trusted or self-asserted? — **VERIFIED (server-trusted)**
App capabilities are **granted in the tailnet policy file (`grants`)** and resolved by the Tailscale
**control plane** — they are NOT self-asserted by the source node. A grant maps a `src` (which may be
`tag:foo`) → a `dst` → an `app` capability (reverse-DNS name, e.g. `example.com/cap/foo`) carrying an
opaque JSON parameter array. Current syntax (the modern `grants` block, replacing legacy `acls`):

```json
"grants": [
  { "src": ["tag:builder"],
    "dst": ["tag:sos-core"],
    "app": { "<domain>/cap/sos-core-client": [ { "role": "builder", "scope": ["provision"] } ] } }
]
```

The control plane treats the parameter JSON as **opaque** ("only validates that the application
capability object is valid JSON … does not do any validation on the parameter content itself") — but
the **binding of capability→tag is policy-derived and admin-managed**, "not self-asserted by source
nodes." So the capability the backend sees is **server-trusted**: a node cannot grant itself a
capability it was not assigned in the policy.

- Citations:
  - [Tailscale — Grants](https://tailscale.com/kb/1324/grants) — fetched 2026-06-28: "capabilities … originate from the tailnet policy file managed by administrators — not self-asserted by source nodes."
  - [Tailscale — Grants: app capabilities (syntax: `src`/`dst`/`app`, reverse-DNS cap name, opaque JSON params)](https://tailscale.com/kb/1537/grants-app-capabilities) — fetched 2026-06-28. (quadrant: easy-to-check.)

### Item 3 — Strip + reinject guarantee for App-Capabilities (the crux) — **VERIFIED**
This is the load-bearing question. **YES — serve strips client-supplied copies of
`Tailscale-App-Capabilities` and reinjects only the daemon-verified value**, the SAME anti-spoofing
guarantee documented for `Tailscale-User-Login`. The strip list covers ALL the Tailscale-* identity
headers as a class, AND defends the underscore/case-normalization bypass:

> "If `tailscale serve` receives an incoming client request that already contains any of these headers,
> it will strip (remove) them before forwarding … only headers generated and verified by the local
> Tailscale daemon reach your application." Sanitization actively removes the hyphenated form
> (`Tailscale-App-Capabilities`), the **underscore** form (`Tailscale_App_Capabilities`), and
> **mixed/upper-case** variants — closing the CGI/WSGI/ASGI underscore-normalization spoof.

App-Capabilities is therefore **inside** the strip guarantee, not outside it — it is NOT forgeable by
a client that sets the header itself, **provided the backend is reachable only through serve** (same
loopback / 0600 AF_UNIX precondition as User-Login: if the backend binds `0.0.0.0` or a tailnet IP, a
peer bypasses serve and forges the header — the docs spell this out explicitly as the bind best
practice). So M3's bind crux covers BOTH identity classes.

- Citations:
  - strip-guarantee text incl. underscore/case-normalization defense + localhost-bind best practice (gsearch-grounded on tailscale.com primaries `kb/1242` and `kb/1537`) — fetched 2026-06-28.
  - [Tailscale — Serve](https://tailscale.com/kb/1242/tailscale-serve) — fetched 2026-06-28 (confirms `--accept-app-caps` and the header-forwarding model on a page validated 2026-01-26). (quadrant: medium — strip-class behavior + underscore defense quoted from primary docs; the single most load-bearing claim, so flagged for VERA re-fetch.)

### Item 4 — Version-sensitivity — **VERIFIED (pin: v1.92+)**
The HTTP-header delivery of app capabilities via serve (`Tailscale-App-Capabilities` +
`--accept-app-caps`) is **new as of Tailscale v1.92** — before v1.92, consuming capabilities required
the Go-specific `tsnet` library; v1.92 brought it to any-language backends over plain HTTP headers.
Two version-/encoding-sensitive design constraints surfaced by this verify (neither in design-rev1):

1. **`--accept-app-caps` is OPT-IN.** By default serve forwards NO app capabilities. The core's serve
   invocation MUST name the capability (reverse-DNS, e.g. `--accept-app-caps=<domain>/cap/sos-core-client`)
   or the tagged builder gets **no** header → auth must FAIL CLOSED.
2. **Encoding.** The header is a serialized-JSON string; backends already handle the `Tailscale-User-*`
   header encoding (User-Name is RFC-2047-style encoded). DAEDALUS should treat the App-Capabilities
   payload as a string to JSON-parse, and decode per the same header-value rules the existing
   `Tailscale-User-*` parsing uses — VERA to confirm the exact on-the-wire encoding at build time
   against the running TS version (the newswire build hit TS 1.98.x identity-header landmines; pin the
   deployed version and re-confirm the header name + encoding then).

- Citations:
  - v1.92-introduced (gsearch-grounded on tailscale.com release-notes + `kb/1242`): "Starting in Tailscale v1.92, Tailscale allows you to pass App Capabilities … via HTTP headers using `tailscale serve` … Previously … required `tsnet`." — fetched 2026-06-28.
  - [Tailscale — Serve (`--accept-app-caps` flag, opt-in)](https://tailscale.com/kb/1242/tailscale-serve) — fetched 2026-06-28. (quadrant: easy-to-check — version + flag from primary docs.)

### r3 VERDICT — **SOUND (not a design-blocker).**
The tagged-node identity path is **forgery-resistant, server-trusted, and strip-protected — the SAME
trust model as `Tailscale-User-Login`**, under the SAME loopback/0600-bind precondition (M3 already
load-bearing in the design and covers both identity classes). The premise the design rests on holds.

**Exact header DAEDALUS must encode:** **`Tailscale-App-Capabilities`** (JSON object, keyed by
capability name; tagged builder's user-login headers will be empty — do NOT key builder auth on
User-Login).

**Exact grants syntax DAEDALUS must encode** (control-plane-trusted; the cap name is reverse-DNS):
```json
"grants": [
  { "src": ["tag:builder"],
    "dst": ["tag:sos-core"],
    "app": { "<domain>/cap/sos-core-client": [ { "role": "builder", "scope": ["provision"] } ] } }
]
```
And the serve invocation MUST opt-in: `tailscale serve --accept-app-caps=<domain>/cap/sos-core-client unix:/run/.../core.sock` (the cap name MUST match the grant; absent the flag → no header → builder auth FAILS CLOSED). Version floor: **Tailscale v1.92+**.

**Confidence: HIGH.** Every item carries a primary tailscale.com/kb citation; the strip-guarantee
(item 3) and v1.92 floor (item 4) are the two VERA should re-confirm at build time against the pinned
running version. This section is preliminary until VERA verification (`verification_status: needs-vera`,
unchanged).
