---
author: Denson Smith
seat: CAPTAIN_DAEDALUS_the_stoa (ARCHITECT)
ticket: stoa--q7f
requirement: sos--373
epic: u--9s2 (Phase-2 increment 2.4 — DESIGN gauntlet)
arc: stoa--q7f (secure Railway core for stoa_of_science)
consumes: agents/research/stoa--q7f/strabo-dc2-premises.md (DC2 + r3 FOLLOW-UP, all PASS / SOUND)
supersedes: agents/design/stoa--q7f/design-rev1.md (kept intact as history)
revises-against: agents/verdicts/stoa--q7f/argus-dc1-security.md (REVISE / PASS-WITH-CONDITIONS, r1-r6)
status: design-rev2 (folds ARGUS r1-r6; shape unchanged — closed-registry per-provider pass-through stays)
build-scope: DESIGN ONLY. ADA builds the DC3 mock-emit ONLY. The core SERVICE is designed-not-built.
---

# Secure Railway core for stoa_of_science — credentialed per-provider API pass-through + pgvector embeddings DB (rev2)

## rev2 changelog — each ARGUS condition r1-r6 → how folded (section ref)

ARGUS returned REVISE (PASS-WITH-CONDITIONS): the DC1 SHAPE is correct (no redesign). The
closed-registry per-provider pass-through is carried forward unchanged. Six conditions folded:

| Cond | ARGUS finding (one line) | How folded in rev2 | Section |
|------|--------------------------|--------------------|---------|
| **r1** | SSRF closed-by-construction but NOT mechanically guarded — a future op with a free-form url_slot or an interpolated `params` value silently reopens M1. | Folded a **build-time STRUCTURAL invariant** (`INV-DEST`) on the `PROVIDER_REGISTRY` schema: every destination component comes ONLY from server-pinned templates/enums; `params` is NEVER interpolated into host/scheme/authority/path. **P-M1 rewritten** to assert the cross-registry invariant (no op CAN introduce a caller destination), not one injection instance. | §1.2.1, §1.5 P-M1 |
| **r2** | M2 over-claims "closed by construction" while conceding redaction completeness is open — contradiction; opaque-body case unresolved; P-M2 tests one echo path. | **Resolved the contradiction with an honest split-claim**: destination + no-caller-URL = closed BY CONSTRUCTION; response redaction = **BUILD-TIME-VERIFIED per-op allow-list** (declared response schema; anything undeclared dropped). Named the opaque/streaming case (SSE) and bounded it WITHOUT reopening M2 (declared-streaming + per-chunk field allow-list; no opaque pass-through permitted). **P-M2 broadened** to the full Vertex response surface. | §1.3.1, §1.5 P-M2, §5 |
| **r3** | Tagged-builder auth premise exceeded what STRABO verified. | STRABO r3 FOLLOW-UP **closed it (cited)**: encoded the exact mechanism — auth keys off **`Tailscale-App-Capabilities`** (NOT User-Login, empty for tagged nodes), control-plane-trusted, strip-protected same as User-Login; grant shape, `--accept-app-caps` serve invocation, **v1.92+** floor. Moved from designed-on-as-settled → verified-premise + ONE build-time VERA encoding confirmation. | §1.4.1, §1.5 P-M3, build-time VERA item V-ENC |
| **r4** | Audit "write-before-respond" is actually write-AFTER-egress — a crash between egress and the single write loses the record of an executed credentialed call. | Folded **two-phase audit**: write a value-free **INTENT record BEFORE egress**, then **UPDATE with outcome AFTER egress**. **P-M5 crash-inject point moved** to between-egress-and-outcome-write; asserts the INTENT record survives (no executed call ever unrecorded). | §1.4.2, §1.5 P-M5 |
| **r5** | M3 0600-bind crux relies on an EXTERNAL probe only; nothing makes a `0.0.0.0` bind un-shippable. | Folded an **IN-PROCESS startup FAIL-LOUD invariant** (`INV-BIND`): the handler asserts its listener is a 0600 AF_UNIX / non-routable socket and **refuses to serve (fail-loud exit)** if it would bind a routable address. **P-M3 augmented** to assert the in-process refuse-if-routable, not only `ss`/`netstat`. | §1.4.3, §1.5 P-M3 |
| **r6** | One tag = one builder identity → per-identity token-bucket lumps all builder skills into one bucket; audit can't attribute which skill flooded. | Folded a **declared `skill_id` field in the closed request envelope** (audited; optionally sub-bucketed). Per-identity bucket stays the security boundary; `skill_id` gives attribution + optional sub-fairness. Stated as the chosen disposition (not deferred). | §1.3 envelope, §1.4.4, §1.5 P-M6 |

**Carried UNCHANGED from rev1** (ARGUS cross-checked CLEAN — do not re-touch): the entire DC3
mock-emit (§2; two catalog TOMLs `vertex-gemini` + `tailscale`, the omitted Vertex
`key_bearing_pairing` row CONFIRMED correct, frozen `resolve.py` byte-identical, `assert_value_free`
passes). One ARGUS-suggested design LINE added (SA-key presence enforced by the startup
`bootstrap_adc` path, not the resolver) — §2.1, additive prose only, no TOML/spec change.

---

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
1. **Tagged-builder identity does NOT populate `Tailscale-User-Login`; it carries
   `Tailscale-App-Capabilities`.** STRABO's r3 FOLLOW-UP verified this against current (2026) Tailscale
   primary docs (§1.4.1 cites it): a TAGGED device has no user identity, so the User-* headers are
   empty/omitted; the identity the core keys builder auth off is `Tailscale-App-Capabilities`,
   **control-plane-resolved from the policy `grants` block (NOT self-asserted)** and **strip-protected /
   re-injected by serve under the SAME guarantee as User-Login** (including the underscore/case
   normalization defense), under the SAME loopback/0600-bind precondition (M3). Version floor
   **Tailscale v1.92+**; `--accept-app-caps` is opt-in and fail-closed. This is no longer a thin premise
   — it is a verified one with a single build-time encoding confirmation (V-ENC).
2. **Egress is public-internet, not tailnet** (STRABO nuance 1). Only operator/builder → core INGRESS
   uses Tailscale serve; the core's calls to Vertex/provider APIs go out the normal public internet.
   Userspace `tailscale serve` is inbound-only; sufficient and correct here.
3. **The core SERVICE is an entirely new runtime service**, a generalization of `newswire-serving`. It
   is NOT in `builder_deploy_core` (a value-free one-shot PROVISIONING emitter). DC3 stands the core up
   via the existing emitter; the service code itself is designed in DC1 and built in a later gated arc.

The restatement converges with the brief. No load-bearing divergence; the assumptions above are
encoded in the design from the start. (Unchanged from rev1 except assumption 1, now verified-not-thin.)

---

## §1 DC1 — The pass-through core shape (the ARGUS security crux)

### §1.1 Threat model (explicit)

This is the most security-sensitive component the team has designed: **a single internet-egress box
that holds ALL provider API keys.** If it is compromised, every provider key is exfiltrable and the box
becomes an open relay. The named threats (M1..M6):

| M# | Named threat | Realized how (attack path) |
|----|--------------|----------------------------|
| M1 | **SSRF / forward-anything egress** | A caller induces the core to make an outbound request to an attacker-chosen URL/host (cloud metadata `169.254.169.254`, internal services, arbitrary exfil endpoint). |
| M2 | **Key-exfil** | A caller gets the core to return a provider key in a response body, error, or log; or routes a provider key to an attacker-controlled destination. |
| M3 | **Identity-header forgery via non-loopback bind** | The pass-through handler listens on a routable address (`0.0.0.0`); a local/colocated process connects directly, bypassing serve, and forges `Tailscale-User-Login` / `Tailscale-App-Capabilities`. |
| M4 | **Over-broad provider/operator authorization** | Any tailnet identity that can reach the core can invoke ANY provider (no per-identity scoping), widening blast radius beyond least-privilege. |
| M5 | **Audit gap** | A pass-through call (who, which provider, which operation, outcome) is not durably recorded, so abuse/compromise is undetectable and unattributable. |
| M6 | **Quota exhaustion / DoS** | A caller (or a runaway skill) floods the core, exhausting the shared Gemini/Vertex quota or the core's resources, denying service to everyone on the shared quota. |

**Honest-claim posture (per ARGUS r2, made precise):** M1 and M3 are **closed BY CONSTRUCTION** (no
destination input exists; no routable listener exists). M2 is **closed BY CONSTRUCTION at the channel
level** (credential attached server-side; no caller-URL) **PLUS a BUILD-TIME-VERIFIED property** for
response redaction (per-op allow-list; §1.3.1) — NOT a by-construction guarantee for the response
surface. M4 is closed by construction (per-op `scopes`). M5/M6 are build-time-verified properties.

### §1.2 The shape decision (DC1.i): **per-provider scoped pass-through, NOT an egress proxy** (unchanged)

**Decision: per-provider endpoints (a closed registry of named provider operations), NOT an
authenticated allowlisted egress proxy.** (Carried from rev1 — ARGUS confirmed the shape.)

An egress proxy — even allowlisted — takes a URL/host from the caller and forwards: a forward-anything
primitive with a filter bolted on, and filters are the classic bypass surface (DNS rebinding,
redirect-following, IP-literal vs hostname, IPv6/decimal encodings). A per-provider design has **no
caller-supplied URL at all**: the caller names a `provider` + `operation` from a **closed, code-defined
registry**; the core holds the URL template, method, allowed parameter schema, and key binding for that
exact operation. SSRF is closed by construction because there is no "destination" input to attack —
only a finite enum of operations the core knows how to perform. Strictly more restrictive than
deny-by-default allowlisting: deny-by-default over a **closed verb set**, not over an open URL space.

This generalizes `newswire-serving`: newswire exposed ONE domain verb (`POST /run`) over the mesh; this
core exposes a **closed set** of provider operations (`POST /call`). The `<VERB>` placeholder in the
existing `MeshShape` scaffold is where this registry plugs in at T3.

### §1.2.1 (r1) Build-time STRUCTURAL invariant `INV-DEST` — the SSRF guard, made mechanical

rev1 stated "no caller-supplied URL" as prose. rev2 makes it a **schema-enforced invariant the build
verifies across the WHOLE registry**, so a future op cannot silently reopen M1:

**`INV-DEST` (PROVIDER_REGISTRY schema invariant):** every component of an outbound destination —
**scheme, host/authority, port, path** — is derived ONLY from a **server-pinned template** whose slots
are **FIXED values or closed ENUMs declared in code**. A registry operation's declared `param_schema`
(the caller-influenced surface) is **structurally forbidden** from contributing to any destination
component:
- `url_slots` accept ONLY `FIXED(<value>)` or `ENUM([...])` slot types. A free-form / open-string slot
  type is **not representable** in the schema (the schema has no "free string url slot" constructor).
- No `param_schema` key may be referenced by a `url_slots` interpolation. The two namespaces are
  **disjoint by construction**: `url_slots` draw only from the server-pinned set; `params` draw only
  from the caller envelope; the registry loader **rejects at startup** any operation whose URL template
  references a name that resolves to a `param_schema` key (cross-namespace reference = fail-loud refuse
  to load).
- The outbound HTTP client is configured **redirect-following OFF** for registry egress (a `3xx` to an
  attacker host is returned as a `provider_error`, never followed) — closes the response-side
  SSRF-via-redirect variant ARGUS flagged in its honest-claim boundary.

`INV-DEST` is enforced two ways, both build-time-verifiable: (1) the registry schema type makes a
caller-derived destination **unconstructable**; (2) a startup loader self-check **refuses to serve**
(fail-loud) if any operation violates the disjointness/redirect rules. This is the cross-registry
invariant P-M1 now asserts (not one injection instance).

### §1.3 The client contract (DC1.ii): a closed, validated request shape — never a raw URL

A local skill names a call to the core with a **closed request envelope**, transported over the mesh to
`https://<core>.<tailnet-domain>/call` (Tailscale serve → 0600 AF_UNIX socket → handler):

```
POST /call
Content-Type: application/json
{
  "provider":  "vertex",                  # MUST match a key in the server-side PROVIDER_REGISTRY
  "operation": "generate_grounded",       # MUST match a registered operation under that provider
  "skill_id":  "gsearch",                 # (r6) declared caller skill — audited + optionally sub-bucketed
  "params":    { ... }                    # validated against that operation's PARAM SCHEMA (closed)
}
```

Rules enforced server-side (the validation gate, before any egress):
- `provider` and `operation` MUST resolve to an entry in the **server-side** `PROVIDER_REGISTRY`
  (code, not caller data). Unknown provider/operation → `400`, no egress, audited as `rejected`.
- `params` MUST validate against that operation's declared **closed param schema** (allowed keys,
  types, value bounds). No key/URL/host/header field is ever accepted from the caller. An unexpected
  param key → `400`, no egress. **`params` is NEVER interpolated into a destination component (`INV-DEST`).**
- `skill_id` (r6) MUST validate against a closed `[a-z0-9_-]{1,64}` shape — it is an **attribution
  label only**, NEVER interpolated into the destination, the credential, or any header (it rides the
  same disjointness fence as `params`). It is audited and MAY drive an optional per-`(identity, skill_id)`
  sub-bucket; the per-identity bucket remains the security boundary (§1.4.4).
- The core constructs the outbound request entirely from the registry entry: URL template + method +
  server-side-attached credential + validated params interpolated into **declared `param_schema` slots
  ONLY** (never destination slots).
- The response returned to the caller is the **registry-op's declared response schema** (allow-list;
  §1.3.1) — never the raw upstream body, never upstream headers.

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
        "url_slots": {                                 # (INV-DEST) FIXED / ENUM ONLY — no free-form slot type
          "location": ENUM(["us-central1", "us-east4"]),
          "project":  FIXED("proj-sos_core"),          # server-pinned to the core's OWN GCP project
          "model":    ENUM(["gemini-2.5-flash", "gemini-2.5-pro"]),
        },
        "param_schema": {"contents": ..., "tools": {"google_search": {}}},  # closed; disjoint from url_slots
        "response_schema": {                           # (r2) ALLOW-LIST: only these fields reach the caller
          "candidates": ["content", "finishReason", "groundingMetadata"],
          "usageMetadata": ["promptTokenCount", "candidatesTokenCount", "totalTokenCount"],
        },                                             # anything not listed (incl. any echoed cred/header) is DROPPED
        "stream": False,
        "scopes": ["operators", "builders"],           # which identity classes may call this op
      },
      "embed": {
        "method": "POST",
        "url": ".../publishers/google/models/{model}:predict",
        "url_slots": {"location": ENUM([...]), "project": FIXED("proj-sos_core"), "model": ENUM([...])},
        "param_schema": {"instances": ...},
        "response_schema": {"predictions": ["embeddings"]},   # allow-list
        "stream": False,
        "scopes": ["operators", "builders"],
      },
    },
  },
}
```

The `url_slots` are server-pinned ENUM/FIXED, NOT free caller input — `project` and `location` are
pinned to the core's own GCP project; `model` is a closed enum. The caller cannot steer the
destination. This is `INV-DEST` made concrete.

### §1.3.1 (r2) Response redaction — the HONEST claim, allow-list per op, opaque/streaming bounded

**The contradiction rev1 carried** ("M2 closed by construction" while conceding redaction completeness
is open) is resolved by **splitting the claim**:

- **Closed BY CONSTRUCTION (no further proof needed):** the credential is attached server-side from a
  Railway secret; there is no caller-URL/host (`INV-DEST`); a provider key cannot be *routed* to an
  attacker destination. The *channel* is closed.
- **BUILD-TIME-VERIFIED property (NOT by-construction):** that no key/credential byte reaches the caller
  or the audit log **via the response body**. This rests on the **per-op `response_schema` allow-list**:
  each operation declares the EXACT fields returned to the caller; the response serializer **emits only
  declared fields and DROPS everything else** (allow-list, not deny-list — a key echoed in an
  un-anticipated field is dropped because it was never declared, not because a deny-rule caught it).
  Error bodies are returned as `{status, provider_error_class}` ONLY — never the raw upstream error,
  never upstream headers. This property is **verified at build time by P-M2** against the full Vertex
  response surface; it is honestly a verified property, not a by-construction guarantee.

**(b) Opaque / streaming case — named and bounded WITHOUT reopening M2.** ARGUS asked whether any Vertex
op needs opaque pass-through of an upstream body.
- **No registry op is permitted opaque pass-through.** Opaque pass-through (returning an
  un-field-modelled upstream body) is **forbidden by `INV-DEST`'s sibling rule** `INV-RESP`: an
  operation with no declared `response_schema` **refuses to load** (fail-loud at startup). There is no
  "just forward the body" escape hatch — that would reopen M2.
- **Streaming (SSE) — the one shape that can't be modelled as a single body — is handled as
  declared-streaming with per-chunk field allow-listing.** An operation may set `stream: True` and
  declare a `chunk_schema` (the allow-list applied to EACH decoded SSE `data:` chunk). The core decodes
  each SSE chunk, applies the chunk allow-list, re-serializes ONLY declared fields, and re-emits — the
  caller never receives a raw upstream chunk. Undeclared fields in any chunk are dropped exactly as in
  the unary case. No chunk is ever passed opaque. (The rev1 vertex ops `generate_grounded` / `embed` are
  `stream: False`; `chunk_schema` is specified for the FUTURE streaming-gsearch op so the build has the
  pattern, but rev2 does not introduce a streaming op into the rev1 surface.)

**(c) The honest claim, stated:** *destination + no-caller-URL is closed BY CONSTRUCTION; response
redaction (unary AND streaming) is a BUILD-TIME-VERIFIED property — a per-op allow-list, proven complete
against the actual Vertex response surface by P-M2, with opaque pass-through structurally forbidden.*
This replaces rev1's over-claim.

### §1.4 Auth, audit, rate-limit, shared-quota (DC1.iii)

#### §1.4.1 (r3) Identity at the core (M3/M4) — the tagged-builder path, VERIFIED + encoded

Two identity classes, both resolved from serve-injected, daemon-verified headers (serve strips client
copies and re-injects verified values — STRABO (c)(iv) for User-Login; STRABO r3 FOLLOW-UP Items 1-4
for App-Capabilities):

- **Human operator** (untagged tailnet node): carries `Tailscale-User-Login`. Authorized against an
  operator allowlist (the `<CORE>_OPERATORS` env, generalizing newswire's `NEWSWIRE_OPERATORS`).
- **In-mesh builder** (TAGGED node): **carries NO `Tailscale-User-Login`** (empty/omitted for a tagged
  node — STRABO r3 Item 1). Builder auth **keys off `Tailscale-App-Capabilities`**, a JSON object keyed
  by capability name. The capability is **control-plane-resolved from the policy `grants` block, NOT
  self-asserted** (STRABO r3 Item 2): a node cannot grant itself a capability it was not assigned. The
  core reads the capability, confirms the expected cap key is present, and maps it to the `builders`
  identity class. **Do NOT key builder auth on User-Login** (it is empty for tagged nodes — keying on it
  would fail-open or deny-all).

**The exact mechanism the build MUST encode (STRABO r3 VERDICT, cited):**
- **Grant shape** (modern `grants` block; cap name is reverse-DNS; control-plane-trusted):
  ```json
  "grants": [
    { "src": ["tag:builder"],
      "dst": ["tag:sos-core"],
      "app": { "<domain>/cap/sos-core-client": [ { "role": "builder", "scope": ["provision"] } ] } }
  ]
  ```
- **Serve invocation MUST opt-in** to the capability or the builder gets NO header (fail-closed):
  `tailscale serve --accept-app-caps=<domain>/cap/sos-core-client unix:/run/.../core.sock`
  (the cap name MUST match the grant; absent the flag → no header → builder auth FAILS CLOSED).
- **Version floor: Tailscale v1.92+** (HTTP-header delivery of app capabilities via serve is new in
  v1.92; before that it required the Go `tsnet` library). Pin the deployed TS version ≥ v1.92.
- **Strip guarantee:** `Tailscale-App-Capabilities` is INSIDE serve's strip-and-reinject class, SAME as
  User-Login, INCLUDING the underscore/case-normalization defense (`Tailscale_App_Capabilities`,
  mixed-case) — so it is NOT client-forgeable, **provided the 0600/loopback bind holds** (§1.4.3). M3's
  bind crux therefore covers BOTH identity classes.

**Build-time VERA item `V-ENC` (record, do NOT design around it):** the exact on-the-wire encoding of
the App-Capabilities header value (Q-encoded vs serialized-JSON string) is to be **VERA-confirmed at
build time against the pinned running TS version**. The design requirement is fixed: *the backend
decodes `Tailscale-App-Capabilities` per the SAME header-value rules it uses for the `Tailscale-User-*`
headers, then JSON-parses the result.* (The newswire build hit TS 1.98.x identity-header landmines; pin
the version and re-confirm header name + encoding at build.) This is the SINGLE remaining build-time
confirmation on the r3 path — the premise itself is verified (STRABO r3, HIGH confidence, primary
tailscale.com/kb citations).

Both classes are checked **per operation**: `PROVIDER_REGISTRY[provider].operations[op].scopes` declares
which identity classes may invoke it. An identity outside the op's `scopes` → `403`, no egress, audited.
This is M4 closed: authorization is per-(identity-class, provider, operation), deny-by-default.

#### §1.4.2 (r4) Audit — TWO-PHASE: intent-before-egress, outcome-after

rev1's single "write-before-respond" record was actually written AFTER egress — a crash between the
external call and the write loses the record of an already-executed credentialed call. rev2 folds a
**two-phase audit** so no executed call is ever unrecorded:

1. **INTENT record — written BEFORE egress** (after the validation gate passes, before the outbound
   provider call leaves the box): `{audit_id, ts_intent, identity_class, identity (login or cap),
   skill_id, provider, operation, params_digest, phase: "intent"}`. **Value-free**: `params_digest` is a
   one-way digest of the validated params (for correlation/replay-detection), **never the param values**;
   no credential; no response. This record proves a credentialed egress was ABOUT to happen, with full
   attribution, BEFORE it could happen.
2. **OUTCOME update — written AFTER egress** (keyed by the same `audit_id`): `{audit_id, ts_outcome,
   outcome (ok|rejected|forbidden|provider_error|rate_limited), upstream_status, latency_ms,
   phase: "outcome"}`. Still value-free (no body, no credential).

A crash/kill in the window between egress and the outcome write leaves a **durable INTENT record** of an
executed credentialed call (attributable: who, which skill, which provider/op). The event that most
needs attribution — the egress itself — can NEVER occur un-recorded. Rejected/forbidden/rate_limited
calls (no egress) get an INTENT record with an immediate terminal OUTCOME (they never egressed, so the
window doesn't apply). P-M5 crash-injects in the egress→outcome window and asserts the INTENT record
survives.

#### §1.4.3 (r5) The bind precondition (M3, the crux) — IN-PROCESS fail-loud `INV-BIND`

The handler MUST listen ONLY on a `0600` AF_UNIX socket (or loopback), NEVER `0.0.0.0`.
`tailscale serve --https=443 --accept-app-caps=<domain>/cap/sos-core-client unix:/run/.../core.sock`
(supported TS ≥ 1.94.1; app-caps opt-in needs ≥ v1.92, so the effective floor is **v1.94.1+**). With no
network-reachable listener, the identity headers (BOTH User-Login and App-Capabilities) are trustworthy
because the ONLY path to the handler is through serve, which strips-and-reinjects.

rev1 relied on an EXTERNAL `ss`/`netstat` probe alone. rev2 folds an **IN-PROCESS startup invariant**:

**`INV-BIND` (in-process, fail-loud):** at startup, BEFORE accepting any connection, the handler
**inspects its own listener** and asserts it is a **0600 AF_UNIX socket OR a loopback (`127.0.0.1`/`::1`)
address**. If the listener is bound to ANY routable address (`0.0.0.0`, a tailnet IP, any non-loopback
interface), the handler **logs a fatal identity-trust violation and EXITS non-zero — it refuses to
serve**. A `0.0.0.0` bind is therefore **un-shippable**: it crashes the process at startup rather than
serving a forgeable identity surface. This backs the external CI probe with a runtime guarantee — the
single most load-bearing security property no longer depends on a future implementer not making one
mistake. (For AF_UNIX, `INV-BIND` also asserts the socket file mode is `0600`.)

#### §1.4.4 (r6) Rate-limit + shared-quota (M6) — per-identity boundary + skill_id attribution

Two layers, plus the r6 attribution fold:
- **Per-identity token-bucket rate limit** (e.g. N calls/identity/window), refused `429` + audited
  `rate_limited`. Identity = operator-login OR builder-cap. This is the **security boundary** and is
  unchanged.
- **Shared-quota fairness for Vertex/Gemini:** a core-level concurrency cap + a per-identity share of the
  shared Vertex quota, so one operator/skill cannot starve the shared Gemini quota. Over-cap → `429`,
  not unbounded queue.
- **(r6) `skill_id` attribution + optional sub-bucket:** because one builder tag = one identity, the
  per-identity bucket lumps every builder skill into one bucket. The declared `skill_id` (§1.3 envelope)
  is **audited on every call** (INTENT record) so the log CAN attribute which skill flooded — closing the
  rev1 attribution gap. **Disposition (stated, not deferred):** rev2 ADDS `skill_id` to the envelope +
  audit now (the attribution fix), and specifies an **optional per-`(identity, skill_id)` sub-bucket** as
  a tunable the build MAY enable for intra-builder fairness. The per-identity bucket remains the hard
  security limit regardless of sub-bucketing. Honest residual: `skill_id` is a caller-declared label
  (attribution/fairness, not a security boundary) — a hostile builder could mislabel, but it is the SAME
  trusted tag identity either way, so mislabeling cannot exceed that identity's bucket; it only muddies
  intra-identity attribution. Named follow-up: per-skill HARD quotas would need a server-trusted
  skill identity (out of scope for the first slice; the trusted boundary stays the tag).

**Funnel OFF (no public ingress).** The core has no public door; `serve` is private-tailnet only
(STRABO (c)(i)). M1's external-reachability variant is closed: the box is not internet-reachable inbound.

### §1.5 DC1 threat → mitigation → probe map (the gate-relevant output; 6.12 A3 author duty + 6.13)

Each row: mitigation + a threat-anchored probe (6.13: exercises the named attack path, asserts BOTH
attack-blocked AND legit-unaffected). These are **design-time** specs for the FUTURE core service (built
in the later gated arc); ADA does NOT execute them this gauntlet (DC3 is mock-emit only). They are the
falsifiable checks ARGUS re-audits (the deltas) and VERA/CATO re-run when the core is built. Stable
probe-ids. **Tightened per r1/r2/r4/r5; r3/r6 folds reflected.**

| M# | Mitigation (how — honest claim) | Threat-anchored probe (id) |
|----|----------------------------------|-----------------------------|
| **M1** SSRF | **By construction + `INV-DEST` (r1):** no caller-supplied URL/host; destination built from server-pinned FIXED/ENUM slots; `params`/`skill_id` disjoint from `url_slots`; redirect-following OFF. | **P-M1 (rewritten, r1 — asserts the CROSS-REGISTRY INVARIANT, not one injection):** (a) **STRUCTURAL:** a build-time check enumerates EVERY operation in `PROVIDER_REGISTRY` and asserts (i) every `url_slot` is `FIXED`/`ENUM` (no free-form slot type representable), (ii) no URL-template name resolves to a `param_schema`/`skill_id` key (namespace disjointness), (iii) the egress client has redirect-following OFF — and asserts the startup loader **refuses to serve** (fail-loud exit) on a deliberately-planted violating op (a synthetic op with a free-form host slot / a params-derived host). (b) **INSTANCE:** POST `/call` with `params.url` / `params.project=169.254.169.254` / an extra `endpoint` key → `400`, ZERO non-registry hosts contacted (egress recorder), AND a `3xx`-to-attacker-host from a mock upstream is NOT followed. (c) **LEGIT:** `{vertex, generate_grounded, valid contents}` reaches ONLY the pinned `*-aiplatform.googleapis.com` host, succeeds. |
| **M2** key-exfil | **Channel closed by construction** (server-side cred, no caller-URL); **response redaction = BUILD-TIME-VERIFIED per-op allow-list** (`response_schema`/`chunk_schema`; undeclared dropped; opaque pass-through forbidden — `INV-RESP`). | **P-M2 (broadened, r2 — FULL Vertex response surface):** (a) for EACH of `generateContent` body / `predict` body / `groundingMetadata` field / a streaming SSE chunk sequence / an upstream ERROR body — inject a (mock) credential value AND an `Authorization`/`x-goog-api-key` header into an UNDECLARED response field/header at each surface → assert the caller-facing output contains the value at NONE of them (allow-list dropped it) and the error path returns only `{status, provider_error_class}`; grep the (two-phase) audit records for the mock secret → absent in BOTH intent and outcome records. (b) assert the startup loader **refuses to serve** an op declared with NO `response_schema` (opaque pass-through forbidden, `INV-RESP`). (c) **LEGIT:** a real call returns the declared payload fields intact (redaction did not break the feature). |
| **M3** identity forgery | **By construction:** `INV-BIND` (r5) in-process refuse-to-serve-if-routable + 0600 AF_UNIX; serve strips+reinjects BOTH `Tailscale-User-Login` AND `Tailscale-App-Capabilities` (r3, incl. underscore/case defense). | **P-M3 (augmented, r5+r3):** (a) **IN-PROCESS:** start the handler configured to bind a routable address (`0.0.0.0`) → assert it **EXITS non-zero / refuses to serve** (`INV-BIND` fired), NOT merely that `ss`/`netstat` later shows a bad bind. (b) **EXTERNAL:** with a correct 0600 bind, attempt a direct connection bypassing serve sending a forged `Tailscale-User-Login` AND a forged `Tailscale-App-Capabilities` (hyphen, underscore, mixed-case variants) → connection refused (no routable listener) OR all forged-header variants ignored; `ss`/`netstat` shows the unix socket / loopback, NOT `0.0.0.0`. (c) **LEGIT:** a serve-routed operator call (User-Login) AND a serve-routed tagged-builder call (App-Capabilities) each carry the verified header and are authorized to their class. |
| **M4** over-broad authz | **By construction:** per-(identity-class, provider, operation) `scopes`, deny-by-default. | **P-M4:** (a) an identity authorized for `vertex.embed` calls an op NOT in its scopes → `403`, no egress, audited `forbidden`; a builder (App-Capabilities) and an operator (User-Login) are EACH checked against the op's `scopes`. (b) the same identity calls an in-scope op → authorized, succeeds. |
| **M5** audit gap | **Two-phase (r4):** value-free INTENT record BEFORE egress, OUTCOME update AFTER. | **P-M5 (crash-point moved, r4):** (a) issue ok/rejected/forbidden/rate_limited calls → each produces an INTENT record (correct identity, skill_id, provider, op, params_digest) and a matching OUTCOME; **crash-inject in the window AFTER egress, BEFORE the outcome write** → assert the INTENT record STILL EXISTS (the executed credentialed call is recorded even though it never completed). (b) NO record (intent or outcome) contains param VALUES or any credential byte; `params_digest` is present and is not reversible to values. |
| **M6** quota DoS | Per-identity token-bucket (security boundary) + shared-quota concurrency cap; **(r6)** `skill_id` audited for attribution + optional per-`(identity,skill_id)` sub-bucket. | **P-M6:** (a) one identity bursts > N calls/window → the (N+1)th is `429` `rate_limited`, audited; shared-quota cap holds under load (no unbounded queue). (b) a SECOND identity issuing in-policy low-rate calls is NOT throttled (per-identity; feature unbroken). (c) **(r6 attribution)** two DISTINCT `skill_id`s under the SAME builder identity each appear correctly in the audit log; if the optional sub-bucket is enabled, one runaway `skill_id` is sub-throttled WITHOUT throttling the sibling skill under the same identity. |

---

## §2 DC3 — The cookie-cutter emit (MOCK-ONLY; the ONLY thing ADA builds this gauntlet) — UNCHANGED from rev1

ARGUS cross-checked the entire DC3 emit CLEAN (non-findings: ProvisioningSpec consistent with live
machinery; no-`key_bearing_pairing`-row CONFIRMED correct; `category="none"` correct; detection_hints
structurally valid; not-threat-ratified carve-out CONFIRMED). It is **carried forward byte-for-byte**.
The ONLY rev2 change in §2 is one ADDITIVE prose line ARGUS suggested (§2.1, last bullet).

The core SERVICE is designed in §1. To STAND IT UP, the existing value-free provisioning emitter runs
sos--373's services through `resolve → emit_spec` to produce a names-only `ProvisioningSpec`. The frozen
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
  SA-key slot is emitted as an ordinary `gcp_secret` (scope-bearing → per-secret accessor in
  `derive_sa_scope`), which is exactly right. (Flagged for ARGUS in §6: a deliberate divergence from the
  google-maps pairing — justified because Vertex is SA-auth, not API-key-auth. ARGUS CONFIRMED.)
- **The catalog records must reference a KNOWN category** or `'none'` (`load_catalog` dangling-ref
  check). Vertex/Gemini and Tailscale are not geospatial/document categories; both use **`category =
  "none"`** (explicitly accepted by `load_catalog`) because they are baseline-infra-adjacent direct
  catalog entries, not members of an emergent discovery category.
- **(ARGUS-suggested design line, ADDED rev2):** there is **no mechanical in-set check that
  `GCP_SA_KEY_B64` is present when `aiplatform` is enabled** — and that is correct: Vertex SA presence is
  **enforced by the startup `bootstrap_adc` path** (DC4 — base64 SA-key → 0600 `/tmp` file → ADC at core
  boot; fail-loud if absent), NOT by the resolver's `check_runtime_completeness`. The resolver
  deliberately asserts no false API-key pairing invariant (it is SA-auth); the SA-key's
  must-be-present-at-runtime property lives at the bootstrap boundary, not in the emit/resolve layer.

### §2.2 New catalog record 1 — `data/catalog/vertex-gemini.toml` (EXACT buildable TOML) — UNCHANGED

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

Emit consequence: `aiplatform` joins `apis` (the `gcp_api` set, scope-bearing → API role); `GCP_SA_KEY_B64`
joins `secret_slots` as a `gcp_secret` with `acquisition = "mint-via-gcp-console"` (per
`_derive_acquisition`: a key-bearing `gcp_secret` that is not POSTGRES_PASSWORD / TS_AUTHKEY) and joins
`sa_scope` as a per-secret accessor.

### §2.3 New catalog record 2 — `data/catalog/tailscale.toml` (EXACT buildable TOML) — UNCHANGED

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
"mint-via-thirdparty"` (per `_derive_acquisition`); it is scope-bearing → per-secret accessor in
`sa_scope`; `gcp_api = "none"` means it contributes NO API to `apis` (skips S1 enablement). No
`gcp_secret`, no `key_bearing_pairing`.

### §2.4 The manifest the core builder resolves (the cookie-cutter INPUT) — UNCHANGED

```
builder slug: sos_core
baseline (always):    (gcp_api, gemini-embedding), (gcp_api, gemini-search),
                      (railway_var, DATABASE_URL), (gcp_secret, POSTGRES_PASSWORD),
                      (db_extension, pgvector)
delta.add (from the two new catalog records):
                      (gcp_api, aiplatform), (gcp_secret, GCP_SA_KEY_B64),
                      (thirdparty_rest_key, TS_AUTHKEY)
```

### §2.5 The expected `ProvisioningSpec` (what `emit_spec` emits — exact, for VERA zero-guesswork) — UNCHANGED

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

Note the **secret-slot NAMES only** — every `populated=False`, no value anywhere. The Vertex SA key, the
Postgres password, and the Tailscale auth-key are all NAMES the human/CI populates out-of-package (DC4),
never values the emitter holds.

### §2.6 The mock-emit demonstration (what ADA builds + runs — exact steps for VERA re-execution) — UNCHANGED

ADA writes a demonstration script (e.g. `agents/builder-deploy-core/demo/sos_core_emit_demo.py`) and the
two catalog TOML files above. The demonstration:

1. Loads the catalog via `dataload.load_catalog()` → asserts both new records load (fail-closed
   validation passes; `vertex-gemini` and `tailscale` present in the returned catalog dict).
2. Builds the resolved set by composing `sorted(baseline ∪ delta.add)` **directly** (the two records'
   entries unioned onto the baseline) → asserts the resolved set equals §2.4 (sorted). **It does NOT route
   this set through `resolve(...)`** and that is correct: the FROZEN `resolve()` is **library-category-
   driven** — it raises `ResolutionError` on an unknown category, and `none` is **not** a library category
   (the library categories are document-consuming / document-data / geospatial). A `category="none"` core
   stand-up has **no library category to resolve against**, so the demo composes `baseline ∪ delta.add`
   directly — which is exactly what `resolve()` would return for an empty-category template. The directly-
   composed set equals §2.4, and `emit_spec` on it equals the §2.5 golden field-for-field. **FINDING (for
   the GRAND at the PROVISION gate, §4 step 1):** the cookie-cutter `resolve()` cannot express a category-
   less manifest; a `category="none"` core stand-up therefore composes `baseline + delta.add` directly
   rather than routing through `resolve()`. The real provision sequence (§4 step 1) inherits this — the
   resolved set fed to the real emit is the direct `baseline ∪ delta.add` composition, NOT a `resolve()`
   call (which would raise on `category="none"`). This is a shipped-machinery property the GRAND should
   confirm at the provision gate, not a design defect: the resolved set is identical either way (an empty-
   category template resolves to baseline + delta), but the code path is the direct composition.
3. Calls `emit_spec(resolved, "sos_core")` → asserts the `ProvisioningSpec` equals §2.5 EXACTLY
   (golden-file / field-by-field equality; `apis`, `secret_slots`, `sa_scope` sorted as shown).
4. Calls `assert_value_free(spec)` → passes (no `ValueLeakError`).
5. Drives the spec against `MockProvisioner()` (default: everything unpopulated) → asserts S2c BLOCKS
   (the human-gate fail-closed: secret slots unpopulated halts before S3/S5); then against
   `MockProvisioner(populated={"GCP_SA_KEY_B64","POSTGRES_PASSWORD","TS_AUTHKEY"})` → asserts S3-S6 run
   (synthetic ids only, NO value held); `assert_value_free` on the resulting `RunLedger` passes.
6. Calls `mock.stand_up_mesh_shape("sos_core")` → asserts the value-free `MeshShape` (socket_mode
   `0600`, transport `af_unix`, identity_header `Tailscale-User-Login`, deny_by_default True, funnel_off
   True, `<VERB>` placeholder) — the 501-until-T3 scaffold the DC1 core fills at T3.

**Tripwire / frozen-resolver assertions (the regression bar) — UNCHANGED:**
- **W1** (no-I/O imports) grep over `provision/` returns EMPTY (the demo lives OUTSIDE `provision/`,
  under `demo/`, so it does not pollute the W1 surface).
- **W2** MockProvisioner remains the only concrete `Provisioner`.
- **W3** `emit_spec` takes no provisioner and does no I/O.
- **`resolve.py` blob is byte-identical** (`git show HEAD:...resolve.py` hash == working-tree hash).
- **The FULL `builder_deploy_core` test suite is green** (per the gauntlet-verify full-suite discipline).

### §2.7 DC3 threat-coverage note (6.12 self-classification) — UNCHANGED (ARGUS CONFIRMED)

The DC3 work (two additive catalog records + a demonstration) is a **process/data change with no runtime
attack path** — it emits NAMES only against a MockProvisioner, touches no real infra/creds/network.
**PROPOSED classification: NOT threat-ratified (data/config addition, no runtime attack path; §35.5
carve-out — emit-only, value-free, mock).** ARGUS CONFIRMED. The named threats M1..M6 live entirely in
the DC1 core-service design (the future build); DC3 carries no threat-anchored probe of its own beyond
the value-free / tripwire / frozen-resolver assertions above.

---

## §3 DC4 — Credential-discipline boundary (who may do what) — UNCHANGED from rev1

The agent/package NEVER holds or sees a secret value. The boundary, composing `credential-discipline`
(CI/WIF), `railway-keyring-deploy` (local), and the newswire mesh pattern:

| Secret | Minted/set by (OUT-of-package human/CI step) | The agent/package may | The value lives |
|--------|----------------------------------------------|------------------------|-----------------|
| **Vertex SA + key** (`GCP_SA_KEY_B64`) | HUMAN/CI: create the SA in the core's GCP project, grant least-priv (`roles/aiplatform.user` OR the custom `aiplatform.endpoints.predict` role — DC2 (a)(iii)); prefer **WIF** where the runtime supports it, else key JSON → base64 → Railway secret. | emit the SLOT NAME `GCP_SA_KEY_B64`; reference it in the registry as `auth: adc_sa`. NEVER decode/print/log it. | Railway secret (server-side); decoded to a `0600 /tmp` file at core startup (`bootstrap_adc` — the SA-presence enforcement point, §2.1), `GOOGLE_APPLICATION_CREDENTIALS`, never str/repr/logged. |
| **Postgres password** (`POSTGRES_PASSWORD`) | HUMAN/CI: generate locally; set as a Railway secret on `db` + injected into the private `DATABASE_URL`. | emit the SLOT NAME. | Railway secret; `DATABASE_URL` private (`*.railway.internal`), in-network only. |
| **Tailscale auth-key** (`TS_AUTHKEY`) | HUMAN: mint a **reusable, TAGGED** (`tag:sos-core-node`) auth-key in the Tailscale admin console; set as a Railway secret. | emit the SLOT NAME. | Railway secret; consumed by `tailscaled` at container start (userspace, `TS_USERSPACE=true`). |
| **Provider keys** (future providers beyond Vertex) | HUMAN/CI per provider: set as Railway secrets, registered in `PROVIDER_REGISTRY[provider].auth`. | emit the SLOT NAME; reference in the registry. | Railway secret (server-side); attached by the core, never returned to the caller. |

**The builder holds ONLY a tailnet identity** — no Railway token, no SA key, no API keys, no provider
keys. It reaches the core over the mesh with its **tagged** tailnet identity (authorized via
`Tailscale-App-Capabilities`, §1.4.1); every credentialed call runs server-side on the core. The Railway
PAT (for the out-of-package deploy step) lives in the OS keyring per `railway-keyring-deploy`; the agent
never holds it. The recurring "keys on the builder machine" problem is structurally removed.

---

## §4 DC5 — First-slice PLAN (design only; build is a follow-on after the gate + provision-go) — UNCHANGED

The build sequence once the design is gated AND the PRINCIPAL gives provision-go (each a separate gated
action; NOT this gauntlet):

1. **Provision the core (2.4-PROVISION step).** Run the DC3-emitted spec for real (real Railway project
   `proj-sos_core`, real GCP SA, real tagged Tailscale node, real budget cap). Out-of-package human/CI
   does the credential steps (DC4). `db` = Postgres+pgvector; `serving` = the pass-through core service.
   **FINDING for the GRAND at the provision gate (carried from §2.6 step 2):** the resolved set fed to the
   real `emit_spec` is composed as `sorted(baseline ∪ delta.add)` **directly**, NOT via a `resolve()` call.
   The cookie-cutter `resolve()` is library-category-driven and **raises `ResolutionError` on
   `category="none"`** (`none` is not a library category), so a category-less core stand-up cannot route
   through `resolve()`. The resolved set is identical to what an empty-category template would resolve to
   (baseline + delta), so §2.4/§2.5 hold unchanged — but the GRAND should confirm the provision path uses
   the direct composition, not a `resolve()` call, when standing the core up for real.
2. **Wire Vertex/Gemini as the FIRST provider through the pass-through.** Register `vertex` in
   `PROVIDER_REGISTRY` with `generate_grounded` (grounded search — DC2 (a)(iii)) and `embed` operations,
   both `auth: adc_sa`. This is the T3 product that fills the `<VERB>` 501 stub. (Both ops carry a
   declared `response_schema` per `INV-RESP`, §1.3.1.)
3. **Build gsearch as the FIRST thin-client skill — ONCE, as a core-client (SUPERSEDES sos--g8q).**
   gsearch becomes a thin client that POSTs `{provider:"vertex", operation:"generate_grounded",
   skill_id:"gsearch", params:{...}}` to the core over the mesh and returns the grounded result. No API
   key on the builder. (Client skill built in stoa_of_science — this design specifies only the client
   CONTRACT, §1.3.)
4. **Stand up the embeddings DB + point the KG pipeline at it.** The pgvector DB on `db` is the home for
   BOTH the KG pipeline store AND skill/retrieval embeddings. Embedding calls go through the SAME
   pass-through (`{provider:"vertex", operation:"embed"}`), so embedding credentials also never touch the
   builder. Point the KG pipeline's embedding writes at the private `DATABASE_URL` (in-network) and its
   embedding generation at the core's `embed` operation.

Sequencing note (DC2 (b)(i)): Railway private networking is runtime-only — the DB connection from
`serving` to `db` must be established at runtime (start command), not build-time. The volume on `db` is
mounted (no zero-downtime redeploy while mounted — acceptable for the DB; DC2 (b)(iv)).

---

## §5 DC6 — Honest stance + threat posture (revised per r1/r2)

**How the SSRF/key-exfil surface is closed (honest claim, no over-claim):**
- **SSRF (M1): closed by construction + mechanically guarded (`INV-DEST`, r1).** There is no
  caller-supplied URL/host/destination input; the destination is built entirely from server-pinned
  FIXED/ENUM templates; `params`/`skill_id` are disjoint from `url_slots` by schema, the loader
  fail-loud-refuses any op that violates disjointness, and redirect-following is OFF. The rev1 residual
  ("a future op could add a free-form host slot and nothing catches it") is now CLOSED: a free-form
  destination slot is unconstructable in the schema AND a violating op refuses to load. P-M1 asserts the
  cross-registry invariant.
- **Key-exfil (M2): channel closed by construction; response redaction a BUILD-TIME-VERIFIED property
  (r2 — the contradiction resolved).** The credential is attached server-side; there is no caller-URL.
  The response surface is governed by a **per-op allow-list (`response_schema`/`chunk_schema`)**: only
  declared fields reach the caller, everything else (including any echoed credential in an un-anticipated
  field) is DROPPED; opaque pass-through is **forbidden** (`INV-RESP` — an op with no declared response
  schema refuses to load); streaming is declared-streaming with per-chunk allow-listing. rev2 does NOT
  claim this is by-construction for the response body — it is honestly a property **proven at build time
  by P-M2 against the full Vertex response surface** (generateContent / predict / groundingMetadata /
  SSE chunks / error bodies). A misimplemented allow-list serializer is a real build risk VERA owns.
- **Identity (M3): closed by construction IFF the 0600/loopback bind holds — now backed by an in-process
  FAIL-LOUD invariant (`INV-BIND`, r5).** A `0.0.0.0` bind is un-shippable: the handler refuses to serve
  and exits. The strip-and-reinject guarantee covers BOTH `Tailscale-User-Login` and
  `Tailscale-App-Capabilities` (r3, STRABO-verified, incl. the underscore/case defense). The remaining
  build-time confirmation is the App-Capabilities on-the-wire encoding (V-ENC).

**What this design does NOT claim:** it does not claim invulnerability if the Railway secret store itself
is breached (a Railway-level compromise exposes the keys regardless — platform trust boundary, bounded
by least-priv SA scope + budget cap, not eliminated). It does not claim quota fairness is perfect under
adversarial load — only that single-caller flood and gross shared-quota starvation are bounded by the
rate-limit + concurrency cap, with `skill_id` giving intra-builder attribution (not a hard per-skill
quota — §1.4.4). It does not represent M1..M6 as a proven-COMPLETE threat set: per ARGUS's honest-claim
boundary, response-side redirect SSRF is now closed (`INV-DEST` redirect-OFF), but cross-provider key
confusion and timing/error-class side-channels remain the gate's residual enumeration judgment, not a
mechanized guarantee.

This component is **threat-ratified** (the DC1 core design); ARGUS owns the security verdict. The DC3
emit is **not threat-ratified** (process/data change, no runtime attack path — §2.7).

---

## §6 Self-assessed weak points (6.2 post-work; where ARGUS should push hardest on the DELTAS)

1. **`INV-RESP` allow-list completeness against an EVOLVING Vertex response surface (r2 residual, now
   build-time-verified not by-construction).** The honest claim is explicit that response redaction is a
   build-time property, not a by-construction guarantee. The residual: Google can add a NEW field to
   `generateContent`/`predict`/`groundingMetadata` that a future legit feature wants surfaced; widening
   the allow-list to include it is a change that must be re-proven not to carry a credential echo. **ARGUS
   should confirm the build-time framing is the honest ceiling here (it is — an allow-list over an
   upstream you don't control is closed-by-correct-maintenance, and the design says so).**
   *Why this shape anyway:* allow-list is strictly safer than deny-list, and forbidding opaque
   pass-through (`INV-RESP`) removes the only escape hatch; build-time verification (P-M2) over the full
   surface is the correct discipline for an upstream the core doesn't own.

2. **`skill_id` is caller-declared, not server-trusted (r6 fold).** It gives attribution + optional soft
   sub-fairness but is NOT a security boundary — a hostile builder under the trusted tag could mislabel
   `skill_id`. The per-identity (tag) bucket is the hard limit and is unaffected by mislabeling. **ARGUS
   should confirm this is the right boundary placement (it is — the trusted identity stays the tag; per
   the named follow-up, a hard per-skill quota would need a server-trusted skill identity, out of scope
   for the first slice).**
   *Why this shape anyway:* the requirement gives the builder ONE tagged identity; inventing a
   server-trusted per-skill identity now would be scope creep. Attribution-now + a named follow-up for
   hard per-skill quotas is the honest increment.

3. **`INV-BIND` and `INV-DEST`/`INV-RESP` are startup/loader self-checks the FUTURE build must implement
   (r1/r5 folds).** They convert design intentions into fail-loud runtime invariants, which is the right
   shape, but they are still specified-not-built; a build that ships them as warnings-not-exits, or omits
   the loader self-check, silently weakens the guarantee. **ARGUS should confirm the probes (P-M1 (a)
   structural, P-M3 (a) in-process) actually FALSIFY a warnings-only or missing-self-check
   implementation — they are written to (they assert refuse-to-serve / non-zero exit, not just a log
   line).**
   *Why this shape anyway:* an in-process fail-loud invariant + a probe that asserts the exit is the
   strongest design-time mechanism available without building the service this gauntlet; it is exactly
   the A3 author duty (6.13).

4. **V-ENC: the App-Capabilities on-the-wire encoding is the one open build-time confirmation on the
   otherwise-verified r3 path.** STRABO verified the premise (HIGH confidence, primary citations); the
   exact Q-encoded-vs-serialized-JSON encoding is a VERA build-time item, not a design unknown. **ARGUS
   should confirm this is correctly scoped as a build-time VERA confirmation (not a design gap) — the
   requirement "decode per the same rules as Tailscale-User-* then JSON-parse" is fixed; only the byte
   encoding is to be confirmed against the pinned TS version.**
   *Why this shape anyway:* the newswire build hit TS-version identity-header landmines; pinning the
   version and re-confirming the exact encoding at build is the proven discipline, not something to guess
   at design time.

5. **The threat-anchored probes (P-M1..P-M6) remain design-time specs for a service not built this
   gauntlet.** They are tightened (P-M1 structural-invariant, P-M2 full-surface, P-M3 in-process, P-M5
   intent-survives-crash) and falsifiable, but exercise the FUTURE core; ADA does not run them now.
   **ARGUS should pressure-test P-M2 (full-response-surface redaction) and P-M3 (a) (in-process
   refuse-if-routable) hardest — they are the two load-bearing deltas most dependent on the real
   serve/socket/HTTP runtime.**
   *Why this shape anyway:* the gauntlet's job is a buildable design that relays up to be gated; the
   tightened probes are the verification contract the later build arc executes.

---

## §7 Out of scope (deliberately not addressed; ADA scope-fence + ARGUS frame) — UNCHANGED

- **ALL real provisioning** — no Railway project, no GCP SA mint, no Railway secret set, no Tailscale
  node, no DB stand-up. Waits for the gate + the PRINCIPAL's provision-go. *Reason: design may change at
  the gate; emit-only/mock this gauntlet.*
- **The core SERVICE code** — DESIGNED here (DC1), NOT built. ADA builds ONLY the DC3 mock-emit.
  *Reason: directive scope; the service is a later gated build arc.*
- **The first-slice BUILD** (gsearch thin-client, embeddings stand-up) — PLANNED (DC5), not built.
  *Reason: follow-on after gate + provision-go.*
- **The stoa_of_science CLIENT skills** — theirs. This design specifies the client CONTRACT (§1.3) only.
  *Reason: ownership split per sos--373.*
- **Multi-provider registry beyond Vertex** — the design accommodates it (N-provider registry), but only
  Vertex is specified now. *Reason: Vertex is the first provider; others added per-provider later, each
  following the §1.3 registry shape + §1.3.1 response-schema + §3 credential boundary.*
- **Hard per-skill quotas** (a server-trusted per-skill identity) — the named r6 follow-up. *Reason: the
  first slice's trusted boundary is the tag; per-skill HARD limits need a server-trusted skill identity,
  out of scope now.*
- **A streaming-gsearch op** — the `chunk_schema` pattern is specified (§1.3.1) so the build has it, but
  no streaming op is introduced into the rev1 vertex surface this gauntlet. *Reason: rev1 ops are
  `stream: False`; streaming is a later additive op following the declared-streaming pattern.*
- **arc-75 (bw-bootstrap)** — parked, separate. *Reason: unrelated; not touched here.*
</content>
</invoke>
