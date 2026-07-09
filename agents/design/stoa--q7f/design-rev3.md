---
author: Denson Smith
seat: CAPTAIN_DAEDALUS_the_stoa (ARCHITECT)
ticket: stoa--q7f
requirement: sos--373 (science lane) + nws-1n7 (newswire store lane) + future builder lanes
epic: u--9s2 (Phase-1 increment 2.4 — BUILD gauntlet: build the REAL pass-through service)
arc: arc-77 (coordination stoa--po5)
supersedes/builds-on: design-rev2.md (arc-76/build @26698475, gated — shape carried UNCHANGED)
consumes: docs/research/anthropic-workflows-report.md (in-harness canon), docs/secure-core/deployment-plan.md (runbook), arc-77-build-directive.md §3A/§4/§5/§6
status: design-rev3 (BUILD-facing — the REAL service). Folds the CONSOLIDATION reframe (multi-consumer identity/authz), the 3 mandatory canons, and the workflow-vs-app-code call. rev2's DC1 shape + INV-DEST/INV-RESP/INV-BIND + two-phase audit + M1..M6/P-M1..P-M6 are carried BY REFERENCE, not re-litigated.
build-scope: BUILD the REAL pass-through service locally/against mocks; verify by re-running the design's own attack probes against REAL code. NO real infra, NO real secrets, NO money, nothing merged/pushed (directive §5 SCOPE FENCE).
---

# Secure Railway core for the CONSOLIDATION center — credentialed per-provider pass-through, multi-lane (rev3, BUILD-facing)

## rev3 changelog — what is NEW vs rev2, what is CARRIED

rev2 was gated with the DC1 SHAPE correct (closed-registry per-provider SCOPED pass-through). rev3 does
**not** redesign that shape. It makes the service **buildable as the shared center ALL lanes consume**
and folds the arc-77 directive's three mandatory items. Three things are NEW; everything else is carried.

| # | rev3 delta | Kind | Section |
|---|------------|------|---------|
| **1** | **CONSOLIDATION reframe** — multi-consumer (multi-lane) identity/authz on the pass-through. rev2 was framed for a SINGLE builder/consumer; the core is now the canonical center for the science lane (sos--373) + the newswire credential-free STORE (nws-1n7) + future builders. The **one genuinely-novel design delta.** | **FIRST-CLASS NEW** (ARGUS cold-audits specifically) | §2 |
| **2** | **The 3 mandatory canons folded as build requirements:** (a) seal-every-secret + **fail-CLOSED seal-audit** (u--84m, made a build GATE — new named threat **M7**); (b) **Railway-setup skill sos--1bk** as the Phase-2 provisioning-choreography reference (NOT executed this arc); (c) **in-harness-workflows canon** (any LLM adjudication runs in-harness on subscription OAuth, never a keyed CI call). | build requirements | §3 |
| **3** | **The workflow-vs-app-code call, answered INLINE:** the pass-through is deterministic **application code** — no Stoa Workflow warranted. | design decision | §4 |

**Carried UNCHANGED from rev2 (do NOT re-litigate — restated build-facing in §5, not redesigned):**
the closed-registry per-provider SCOPED pass-through over the server-side `PROVIDER_REGISTRY`; `INV-DEST`
(SSRF closed by construction — `url_slots` FIXED/ENUM only, disjoint from `params`/`skill_id`,
redirect-following OFF, loader fail-loud-refuses a violating op); `INV-RESP` (per-op
`response_schema`/`chunk_schema` allow-list; opaque pass-through refuses to load); `INV-BIND` (in-process
startup fail-loud: refuse to serve if bind is routable / socket not 0600); the two-phase audit (value-free
INTENT before egress, OUTCOME after); M1–M6 + the P-M1..P-M6 threat-anchored probe map (rev2 §1.5). rev3
carries these by reference and restates them as the buildable invariant/probe contract ADA implements and
VERA re-runs against REAL code (§5). The DC3 mock-emit (rev2 §2 — the two catalog TOMLs `vertex-gemini` +
`tailscale`, the frozen `resolve.py`) is carried unchanged; the new seal-audit (§3.1) now also scans those
TOMLs.

---

## §0 Problem restatement (6.1 pre-work gate)

Build (this arc, for real, locally/against mocks — no real infra) the credentialed per-provider
pass-through service designed in design-rev2, **as the CONSOLIDATION secure core every lane consumes**, not
as a stoa_of_science one-off. A local skill on any consuming lane names a provider + a pre-registered
closed call; the core attaches that provider's server-side key, calls the external API, and returns only
the declared result — the key never leaves the core. The core is reachable ONLY over Tailscale; each
consuming lane holds ONLY a tailnet identity (no Railway token, no SA key, no API keys). rev2's single
security-crux shape (INV-DEST/RESP/BIND, two-phase audit, M1..M6 probes) is correct and carried; the
**new design work is the multi-lane identity/authz model** that lets distinct lanes (science, newswire,
future) share one core while one lane's tag CANNOT reach another lane's provider/operation
(deny-by-default, cross-lane isolation). The build must also pass a **fail-closed seal-audit** (no secret
VALUE anywhere in code/config/catalog/logs — slot NAMES only). This arc builds and probes the service; it
provisions NOTHING real and mints NO secrets (that is Phase 2, separately PRINCIPAL-gated).

**Imported assumptions (named per 6.1):**

1. **Each consuming LANE joins the tailnet under its OWN tag; a lane's identity at the core is
   control-plane-resolved from the Tailscale policy `grants` block, NOT self-asserted.** This is the direct
   generalization of rev2's STRABO-r3-verified single-builder premise (App-Capabilities is
   control-plane-trusted, strip-and-reinjected by serve under the same guarantee as User-Login, v1.92+
   floor). rev3 assumes the SAME mechanism holds per-lane: a node under `tag:<lane>-core-client` receives
   ONLY the capability its tag was granted, and cannot claim another lane's capability. This is a
   generalization of a verified premise, not a new thin premise — but the **per-lane cap-name → lane
   mapping is the ONE new build-time encoding confirmation** (V-ENC-LANE, §2.4), riding alongside rev2's
   existing V-ENC (App-Capabilities on-the-wire encoding).
2. **The newswire STORE lane (nws-1n7) is a credential-FREE consumer** — it consumes the core for the
   shared embeddings/store surface, NOT for credentialed generative egress. Its lane principal is scoped
   (deny-by-default) to store/embed operations only; it is never in the `scopes` of a credentialed
   generative op. (If a future newswire feature needs a credentialed op, that op's `scopes` is explicitly
   widened to include the newswire lane — an explicit, audited change, never a default.)
3. **rev2's carried invariants are build requirements, not aspirations.** INV-DEST/RESP/BIND are
   fail-loud runtime self-checks the REAL build MUST implement as refuse-to-serve / refuse-to-load, not
   log-and-continue. The build is verified by re-running P-M1..P-M6 against the REAL code (directive §6
   DoD), not against mocks-of-the-check.
4. **No real infrastructure, no secrets, no money** (directive §5). Everything is built + probed locally /
   against mocks; the Phase-2 provision boundary is a separate PRINCIPAL-gated step this arc does not cross.

The restatement converges with the brief and the directive. The one place it makes an implicit scope
explicit: assumption 2 (the newswire lane is credential-free and store-scoped) — the directive names
nws-1n7 as "the newswire credential-free STORE," and rev3 encodes that as a concrete deny-by-default lane
scope rather than leaving it implicit. Flagged for ARGUS in §6.

---

## §1 Threat model (carried from rev2 §1.1, extended for the reframe + the seal-audit)

The core is the most security-sensitive component the team has built: **a single internet-egress box that
holds ALL provider API keys for ALL lanes.** Named threats M1..M6 are carried verbatim from rev2 §1.1; the
reframe **sharpens M4** and the seal-audit canon **adds M7**:

| M# | Named threat | Realized how (attack path) | Status in rev3 |
|----|--------------|----------------------------|----------------|
| M1 | SSRF / forward-anything egress | Caller induces an outbound request to an attacker-chosen host (metadata IP, internal svc, exfil endpoint). | CARRIED (INV-DEST; P-M1) |
| M2 | Key-exfil (via response/log) | Caller gets the core to return a provider key in a body/error/log, or route a key to an attacker destination. | CARRIED (INV-RESP + channel-by-construction; P-M2) |
| M3 | Identity-header forgery via non-loopback bind | Handler listens on a routable address; a colocated process connects directly, bypassing serve, forging identity headers. | CARRIED (INV-BIND; P-M3) |
| M4 | **Over-broad provider/operator authorization → CROSS-LANE reach** | A tailnet identity reaches an operation it is not scoped for. **Sharpened by the reframe:** one lane's tag reaches ANOTHER lane's provider/operation (e.g. the credential-free newswire lane reaching a credentialed science-only generative op). | **SHARPENED** (INV-LANE + per-lane `scopes`; **P-M4 extended** with a cross-lane-denial probe — §2.5) |
| M5 | Audit gap | A credentialed call is not durably + attributably recorded. **Extended:** the record must attribute the **lane**, not just the identity class. | CARRIED + lane field (two-phase audit; P-M5) |
| M6 | Quota exhaustion / DoS | A caller floods the core, exhausting shared Vertex quota / core resources. **Extended:** per-identity bucket is now naturally per-lane (each lane = its own tag = its own bucket). | CARRIED + per-lane bucket (P-M6) |
| **M7** | **Secret-value leakage into code/config/catalog/logs (build-artifact key-exfil)** | A real secret VALUE (SA key, Postgres password, Tailscale auth-key, OAuth token) is committed into the tree, a config, a catalog TOML, or an emitted log — exfiltrable via the repo or logs even though the runtime response surface (M2) is clean. | **NEW** (u--84m canon; fail-CLOSED **seal-audit** gate — §3.1; threat-anchored **P-M7**) |

**Honest-claim posture (carried + extended):** M1 and M3 closed BY CONSTRUCTION (no destination input;
no routable listener). M2 channel closed by construction + response redaction a BUILD-TIME-VERIFIED
allow-list property. **M4 closed by construction at the per-lane granularity** (per-(principal, provider,
operation) `scopes`, deny-by-default; INV-LANE loader self-check — §2). M5/M6 build-time-verified. **M7 is
a fail-CLOSED build-gate property** (the seal-audit refuses the build on any secret-value match; absence of
a finding is the only pass — §3.1).

---

## §2 THE CONSOLIDATION REFRAME — multi-consumer (multi-lane) identity/authz (FIRST-CLASS NEW; ARGUS cold-audits this)

rev2 §1.4.1 already had two identity CLASSES (human operator via `Tailscale-User-Login`; tagged builder
via `Tailscale-App-Capabilities`) but framed for ONE builder/consumer, with per-op `scopes` a coarse class
list `["operators","builders"]`. The core is now the **canonical center multiple LANES consume**. rev3
designs the multi-lane model concretely enough to BUILD.

### §2.1 The lane model — one tag, one control-plane-resolved capability, one lane principal

**A LANE is a consuming context with its own tailnet tag and its own authorization envelope.** Concretely
for this arc:

| Lane | Requirement | Tailnet client tag (illustrative — pinned at build) | Capability (grant) | Lane principal at the core |
|------|-------------|-----------------------------------------------------|--------------------|----------------------------|
| **science** | sos--373 (stoa_of_science skills) | `tag:sos-core-client` | `<domain>/cap/science-core-client` | `lane:science` |
| **newswire** | nws-1n7 (credential-free STORE) | `tag:nws-core-client` | `<domain>/cap/newswire-core-client` | `lane:newswire` |
| **(future)** | any future builder | `tag:<lane>-core-client` | `<domain>/cap/<lane>-core-client` | `lane:<lane>` |
| **operators** | human operators (not a lane) | untagged node → `Tailscale-User-Login` | — (operator allowlist `<CORE>_OPERATORS`) | `operators` (identity class) |

The exact tag strings are pinned at build against the deployed tailnet policy (the runbook uses
`tag:stoagen-catalog` for the core node's own auth-key; the lane CLIENT tags are distinct from the core
NODE tag `tag:sos-core`). The illustrative names above are the shape; V-ENC-LANE (§2.4) confirms the exact
strings.

**How a lane maps to a principal (the load-bearing mechanism):** each lane's client tag is granted a
**per-lane capability NAME** in the Tailscale policy `grants` block. serve **opts into each lane's cap name
explicitly** (`--accept-app-caps=<domain>/cap/science-core-client --accept-app-caps=<domain>/cap/newswire-core-client`,
comma-list vs repeated-flag TBD at build — V-ENC-LANE). The core holds a server-side **`LANE_REGISTRY`**
mapping cap-name → lane principal:

```python
LANE_REGISTRY = {                                   # server-side, code — NOT caller data
  "<domain>/cap/science-core-client":  "lane:science",
  "<domain>/cap/newswire-core-client": "lane:newswire",
}
```

At request time the core reads the serve-injected, daemon-verified `Tailscale-App-Capabilities` header
(strip-and-reinjected, control-plane-resolved from `grants` — NOT self-asserted, per rev2's STRABO-r3
finding), extracts the capability name(s), and maps to the lane principal via `LANE_REGISTRY`. A node under
`tag:nws-core-client` receives ONLY `<domain>/cap/newswire-core-client` (its grant), so it can only resolve
to `lane:newswire`. **It CANNOT resolve to `lane:science`** because the control plane never emits a
capability its tag was not granted.

### §2.2 Why per-lane cap NAMES (not one shared cap with a lane field in the payload)

Two representable options; rev3 chooses per-lane cap **names** and records why:

- **CHOSEN — per-lane cap name (`<domain>/cap/<lane>-core-client`), mapped by `LANE_REGISTRY`.** The serve
  `--accept-app-caps` opt-in is per-cap-name and **fail-closed**: a lane whose cap name the core did NOT
  opt into gets NO header → auth fails closed. This makes "which lanes does this core serve" an **explicit,
  auditable serve-invocation list** and a fixed server-side cap-name → principal map — no parsing of a
  `lane` sub-field that could be absent/malformed/duplicated.
- **REJECTED — one shared cap name with a `{"lane": "..."}` field in the payload.** It would let a new lane
  be added by a grant change alone (no serve-flag change), which is convenient but WRONG for a security
  boundary: it moves "which lanes are served" out of the explicit fail-closed serve invocation and into a
  payload field the core must parse and trust. The payload IS control-plane-resolved (so the `lane` value
  would be trustworthy), but the fail-closed default is weaker: forget to update a scope and a new lane
  silently rides the shared cap. Per-lane names keep the deny-by-default posture at the serve boundary.

### §2.3 Per-op `scopes` generalized from identity CLASS to lane PRINCIPAL (deny-by-default preserved)

rev2's `scopes: ["operators", "builders"]` (class-level) generalizes to a list of **principals**, where a
principal is either the `operators` class or a `lane:<name>` lane principal:

```python
PROVIDER_REGISTRY["vertex"]["operations"] = {
  "generate_grounded": { ..., "scopes": ["operators", "lane:science"] },            # credentialed generative — science + operators ONLY
  "embed":             { ..., "scopes": ["operators", "lane:science", "lane:newswire"] },  # shared embeddings — both lanes
  # a hypothetical newswire-only store op:
  # "store_fetch":      { ..., "scopes": ["operators", "lane:newswire"] },
}
```

**Deny-by-default, per-(principal, provider, operation):** at request time the core resolves the caller's
principal (operator-login → `operators`; lane cap → `lane:<name>`) and checks membership in the op's
`scopes`. Not a member → `403`, **no egress**, audited `forbidden`. This is M4 closed at LANE granularity:

- The **newswire lane calling `generate_grounded`** → principal `lane:newswire` ∉ `["operators","lane:science"]`
  → `403`, no egress. **One lane's tag cannot reach another lane's provider/op.**
- The **science lane calling `embed`** → `lane:science` ∈ scopes → authorized.
- A future lane is **not in ANY existing op's `scopes` until explicitly added** — so onboarding a lane
  grants it ZERO access by default; access is an explicit, audited `scopes` edit per op.

### §2.4 `INV-LANE` — the new build-time structural invariant guarding the multi-lane authz (fail-loud)

Paralleling INV-DEST/RESP/BIND, the reframe adds a **startup loader self-check** that makes the multi-lane
authz mechanically guarded, not prose:

**`INV-LANE` (registry + serve consistency, in-process fail-loud at startup):**
1. **Every `scopes` entry across the WHOLE `PROVIDER_REGISTRY` resolves to a KNOWN principal** — either
   the `operators` class or a lane principal present in `LANE_REGISTRY`. A `scopes` entry referencing an
   unknown/typo'd `lane:<x>` → the loader **refuses to serve** (fail-loud exit). (Prevents a typo'd scope
   silently denying-all OR — worse — a mis-parse widening access.)
2. **The serve `--accept-app-caps` set equals the `LANE_REGISTRY` cap-name set** — every opted-in cap has a
   lane principal home, and every registered lane principal is actually served (no cap opted-in with no
   principal → an unmapped identity; no principal with no served cap → a dead scope). Mismatch → refuse to
   serve. (This is the fail-closed "which lanes are served" consistency check that makes §2.2's chosen
   design mechanical.)
3. **Lane principals are DISJOINT from the operator class and from `params`/`skill_id`** — a lane principal
   is derived ONLY from the control-plane-resolved cap, never from caller envelope data (same disjointness
   fence as INV-DEST). `skill_id` cannot masquerade as a lane.

INV-LANE is verified two ways (same as its siblings): the `LANE_REGISTRY`/`scopes` types make an unmapped
principal representable-but-caught, and the startup loader **refuses to serve** on any violation. This is
the cross-registry invariant P-M4's structural clause now asserts.

### §2.5 Reframe consequences for audit, rate-limit, and the threat-anchored probe

- **Audit (M5) carries the lane.** The two-phase INTENT record (rev2 §1.4.2) adds `lane` (the
  control-plane-resolved lane principal) alongside `identity_class` and `skill_id`, so every credentialed
  egress is attributable to WHICH LANE made it, not just which identity class. Still value-free
  (`params_digest`, never values; no credential; no body).
- **Rate-limit (M6) is naturally per-lane.** Each lane = its own tag = its own per-identity token bucket,
  so one lane cannot exhaust another lane's bucket. The optional per-`(lane, skill_id)` sub-bucket (rev2
  r6) gives intra-lane fairness. The per-lane (tag) bucket remains the security boundary.
- **Threat-anchored probe P-M4 (extended, §6.13):** the CROSS-LANE-DENIAL probe exercises the M4 attack
  path (a lane reaching another lane's op), asserting BOTH halves:
  - **(a) attack-blocked:** a `lane:newswire`-tagged caller invokes `vertex.generate_grounded`
    (scopes `["operators","lane:science"]`) → `403`, **ZERO egress** (egress recorder empty), audited
    `forbidden` with `lane:newswire` attributed. **PLUS the structural clause:** the startup loader
    **refuses to serve** on a deliberately-planted violating registry (an op whose `scopes` references an
    unknown `lane:ghost`, and a serve invocation whose opted-in caps ≠ `LANE_REGISTRY`).
  - **(b) legit-unaffected:** a `lane:science`-tagged caller invokes the SAME op → authorized, reaches only
    the pinned Vertex host, succeeds; and a `lane:newswire`-tagged caller invokes `vertex.embed` (a lane it
    IS scoped for) → authorized. (The reframe did not defeat cross-lane isolation by breaking a lane's
    legitimate in-scope access.)

**HONEST residual (carried + added to §6 for ARGUS):** the trusted boundary is the **tag → control-plane
capability → lane principal**. `skill_id` remains a **caller-declared attribution label, NOT a security
boundary** — a hostile builder within a lane can mislabel `skill_id` but CANNOT cross to another lane
(different tag, different control-plane capability). Cross-lane isolation rests on the SAME strip-and-reinject
+ INV-BIND (0600/loopback) precondition as rev2's single-builder identity — if that precondition breaks,
ALL lane identities are forgeable, exactly as ALL of rev2's identities were. The reframe adds no NEW trust
assumption beyond "the control plane resolves per-tag caps correctly," which is the verified rev2 premise
applied N times.

---

## §3 The 3 mandatory canons, folded as BUILD requirements

### §3.1 Seal-every-secret + fail-CLOSED seal-audit (u--84m lesson, made a build GATE — mitigates M7)

rev2's `assert_value_free` checks the `ProvisioningSpec`/`RunLedger` OBJECTS. rev3 extends this into a
broader, **fail-CLOSED seal-audit** the whole BUILD/EMIT must pass — the u--84m lesson ("seal every secret;
the audit fails closed") made a gate:

**`seal_audit(tree_paths, emitted_logs)` — a deterministic build-time gate, fail-CLOSED:**
- **Scans:** every tracked file in the build (service code, config, the catalog TOMLs `vertex-gemini.toml`
  + `tailscale.toml`, any startup/registry config) **PLUS** every emitted log / audit-ledger artifact the
  build produces.
- **Refuses the build (non-zero exit — the build FAILS) on ANY match of a secret-VALUE shape:**
  - A secret NAME bound to a non-empty VALUE (e.g. `GCP_SA_KEY_B64=<nonempty>`, `POSTGRES_PASSWORD: <value>`,
    `TS_AUTHKEY=tskey-...`). The slot NAME alone is allowed (it is a name); a VALUE bound to it is refused.
  - Known secret-value SHAPES: `tskey-auth-...` / `tskey-...` (Tailscale auth-keys); base64 blobs above a
    length/entropy floor resembling an SA-key JSON; `-----BEGIN PRIVATE KEY-----`; `sk-ant-` and
    `sk-ant-oat01-` (Anthropic API / OAuth tokens); Postgres URIs carrying an inline password
    (`postgres://user:<pw>@host`).
- **Allow-list (the ONLY things that may match a secret shape):** the bare slot NAMES (documented
  placeholders) and test FIXTURES that carry a reserved obvious-fake marker (e.g. a
  `SEAL_AUDIT_SYNTHETIC_` prefix) so the audit can distinguish a deliberately synthetic test value from a
  real leak. **Anything matching a secret shape that is NOT marked-synthetic FAILS the build.**
- **Fail-CLOSED posture (the u--84m core):** absence of a finding is the ONLY pass. An ambiguous
  high-entropy match the audit cannot classify is treated as a FAILURE, not waved through — the audit fails
  CLOSED, never open. This is the deterministic, unbypassable floor for the high-risk "secret value in the
  artifact" case (consistent with the PRINCIPAL's "deterministic unbypassable floor for high-risk"
  posture — it is code, not an LLM judgment).

**GCP notes folded (directive §4 / stoa--re9):** the Vertex credential is a **service-account (ADC) key**
`GCP_SA_KEY_B64` — **SA-auth, NOT an API key**; there is **no AI-Studio API-key path** (so the seal-audit
does not expect and must not permit a `GEMINI_API_KEY`-style value). The one Vertex SA covers
**embeddings + search + generative** (NOT Google Maps — Maps is a separate `gcp_api` with its own key,
out of scope here). The **prepaid card is the only hard spend cap** — a **Phase-2 concern**, noted here so
the build does not attempt any spend-cap wiring (there is nothing real to cap this arc).

**Threat-anchored probe P-M7 (§6.13):** exercises the M7 attack path directly:
- **(a) attack-blocked:** plant a real-SHAPED secret VALUE (an unmarked `tskey-auth-...` string AND a
  base64 SA-key-shaped blob) into a catalog TOML and into an emitted log line → assert the build
  `seal_audit` **REFUSES (non-zero, build fails)** at each planted site; grep confirms the audit named the
  offending path.
- **(b) legit-unaffected:** with only slot NAMES and `SEAL_AUDIT_SYNTHETIC_`-marked fixtures present, the
  build seal-audit **PASSES** (the gate did not break a clean build by flagging the legitimate slot names
  or the marked synthetic fixtures).

**Classification (6.12 A3 author duty — I PROPOSE, ARGUS CONFIRMS):** the seal-audit is a
**threat-ratified mitigation** — it mitigates the named threat M7 (secret-value leakage / build-artifact
key-exfil, ratified by the u--84m canon in directive §4). Its A3 map row + threat-anchored probe are in §5.
(Contrast: the DC3 emit itself remains NOT threat-ratified — rev2 §2.7, ARGUS-confirmed — but the seal-audit
GATE over the whole tree/logs is threat-ratified because it breaks a real key-exfil attack path.)

### §3.2 Railway-setup skill (sos--1bk) — the Phase-2 provisioning-choreography reference (NOT executed this arc)

The real provisioning of the core (Railway project + `db`/`serving` services, GCP SA, tagged Tailscale
node, spend cap) is **Phase 2 — separately PRINCIPAL-gated; this arc provisions NOTHING real.** When Phase 2
runs, its provisioning choreography follows **the Railway-setup skill sos--1bk** together with the runbook
§6 order (repo + Railway services FIRST with secret NAMES declared and values empty; THEN mint each secret
straight into the existing Railway service var — never stashed locally first), reusing the already-proven
`newswire-builder-setup` + `railway-keyring-deploy` skills. rev3 names sos--1bk as the reference ONLY;
it does not invoke it, does not stand up anything, and mints no secret. (Directive §5 SCOPE FENCE.)

### §3.3 In-harness-workflows canon (any LLM adjudication runs in-harness on subscription OAuth)

Per the ratified canon (`docs/research/anthropic-workflows-report.md` §4): **any LLM-adjudication step runs
IN-HARNESS on subscription OAuth — NEVER a keyed CI call (`ANTHROPIC_API_KEY`), and NOT routed through
`CLAUDE_CODE_OAUTH_TOKEN` for a shared pipeline** (the subscription OAuth token is licensed for individual
interactive use; a shared/automated pipeline through it risks an account ban under Anthropic's ToS).

**Operative consequence for THIS design:** the pass-through **service has NO LLM-adjudication step** — it is
deterministic request/response (§4). So there is nothing in the runtime to route to a keyed call. The
**seal-audit (§3.1) is deterministic code (regex/shape-match over the tree/logs), NOT an LLM call** — which
is exactly correct per the workflows-report §3 design rule: *put the high-risk, must-be-exact decision in a
deterministic code leaf.* Should any FUTURE fuzzy residual arise (e.g. a heuristic body-prose secret-leak
detector BEYOND the deterministic shape-match), it would be a **committed in-harness `.claude/workflows/`
workflow on subscription OAuth (adversarial-verify + voting + schema output), never a keyed CI call** — the
policy-safe key-free home. This arc introduces no such residual; the note fixes the pattern for later.

---

## §4 THE WORKFLOW-VS-APP-CODE CALL (answered inline, honestly)

**CALL: application code — a request/response pass-through. NO Stoa Workflow is warranted.**

**Reasoning (per the workflows-report §3 design rule):** the report's rule is *put the high-risk,
must-be-exact decision in a deterministic code leaf; wrap only a genuinely LLM-fuzzy residual in a
workflow (to raise its reliability via voting/adversarial-verify).* Every security-load-bearing element of
this service is a **deterministic code leaf with NO fuzzy LLM-adjudication residual**:

- INV-DEST (destination built from FIXED/ENUM slots; disjointness; redirect-OFF) — pure code.
- INV-RESP (per-op response/chunk allow-list serializer) — pure code.
- INV-BIND (in-process refuse-if-routable / 0600) — pure code.
- INV-LANE (cap-name → lane principal map; per-op `scopes` deny-by-default; loader consistency check) — pure code.
- The two-phase audit (INTENT-before-egress, OUTCOME-after) — pure code.
- The seal-audit (secret-value shape-match, fail-closed) — pure code (§3.3).

There is **no step where an LLM must make a judgment** — the pass-through validates a closed envelope
against a closed registry, attaches a server-side credential, calls a pinned host, and allow-list-filters
the response. A workflow raises the *statistical reliability of a fuzzy verdict*; it **cannot make a
security invariant more exact than the deterministic code already makes it** — using one here would be
strictly worse (it would replace an exact, unbypassable code check with a probabilistic one). This matches
the prior increment's engine=app-code / no-workflow ratification for SUGGEST. **No workflow is manufactured
to have one.**

*(Classification: this call is a build-engine decision, **not threat-ratified** — no runtime attack path;
the threat-relevant consequence, seal-audit-as-deterministic-code, is covered by M7 in §3.1/§5.)*

---

## §5 BUILD-facing invariant + probe contract (what ADA implements, VERA re-runs against REAL code)

This restates the carried rev2 invariants/probes (NOT redesigned) PLUS the rev3 additions, as the concrete
build + verification contract. Directive §6 DoD: all probes PASS against the **REAL** code; INV-* hold and
are **fail-loud verified** (a violation refuses to start / refuses to respond / fails the build — it does
NOT warn-and-continue).

### §5.1 The invariants the build MUST implement as fail-loud (refuse-to-serve / refuse-to-load / fail-build)

| Invariant | What it guarantees | Fail-loud mechanism | Carried / new |
|-----------|--------------------|--------------------|--------------|
| `INV-DEST` | No caller-supplied destination is constructable | `url_slots` FIXED/ENUM only; `params`/`skill_id` disjoint; redirect-OFF; loader **refuses to serve** a violating op | CARRIED (rev2 §1.2.1) |
| `INV-RESP` | No credential byte reaches a caller via the response | per-op `response_schema`/`chunk_schema` allow-list; op with no schema **refuses to load** | CARRIED (rev2 §1.3.1) |
| `INV-BIND` | Identity headers are trustworthy (no routable listener) | in-process startup check: **exits non-zero** if bind is routable / socket not 0600 | CARRIED (rev2 §1.4.3) |
| `INV-LANE` | One lane's tag cannot reach another lane's op | every `scopes` entry resolves to a known principal; serve caps == `LANE_REGISTRY`; principals disjoint from caller data; loader **refuses to serve** on violation | **NEW (§2.4)** |
| seal-audit | No secret VALUE in code/config/catalog/logs | shape-match scan; **build FAILS non-zero** on any unmarked secret-value match; fails CLOSED | **NEW (§3.1)** |

### §5.2 Threat → mitigation → threat-anchored probe map (6.12 A3 author duty + 6.13)

Each threat-ratified mitigation carries `M<n> → attack-path → how-defeated`, and its §3 threat-anchored
probe asserts BOTH (a) attack-blocked AND (b) legit-unaffected. **The verdict's `defeats_via_probe:` cites
these probe ids.**

| M# | Mitigation → attack-path → how-defeated | Threat-anchored probe (id) — carried / new |
|----|------------------------------------------|--------------------------------------------|
| **M1** SSRF | INV-DEST → caller tries to steer the outbound host → destination built ONLY from server-pinned FIXED/ENUM slots, `params`/`skill_id` disjoint, redirect-OFF, loader refuses a violating op | **P-M1** (carried rev2 §1.5 — structural + instance + legit) |
| **M2** key-exfil | INV-RESP + channel-by-construction → caller tries to read a key from a response/error/log → server-side cred, no caller-URL, per-op allow-list drops undeclared fields, opaque pass-through refuses to load | **P-M2** (carried rev2 §1.5 — full Vertex response surface) |
| **M3** identity forgery | INV-BIND → colocated process connects direct, bypassing serve, forging headers → 0600/loopback only; routable bind refuses to serve; serve strips+reinjects both identity headers | **P-M3** (carried rev2 §1.5 — in-process + external + legit) |
| **M4** cross-lane reach | **INV-LANE + per-lane `scopes` (deny-by-default)** → one lane's tag invokes another lane's op → principal not in op's `scopes` → 403, no egress; loader refuses a registry with unknown-principal scopes / serve-caps ≠ LANE_REGISTRY | **P-M4 EXTENDED (NEW cross-lane clause — §2.5):** (a) newswire tag → generate_grounded = 403 no egress + loader refuses planted violation; (b) science tag → same op authorized, newswire tag → embed authorized |
| **M5** audit gap | two-phase audit + lane attribution → a crash loses the record of an executed credentialed call → value-free INTENT (incl. `lane`) written BEFORE egress, OUTCOME after | **P-M5** (carried rev2 §1.5 — crash in egress→outcome window; INTENT survives; + `lane` present, value-free) |
| **M6** quota DoS | per-lane (per-tag) token bucket + shared-quota cap → one lane/skill floods the shared quota → per-lane bucket is the boundary; skill_id sub-bucket optional | **P-M6** (carried rev2 §1.5 — burst 429; second lane unthrottled; skill_id attributed) |
| **M7** secret leakage | **fail-CLOSED seal-audit** → a real secret VALUE lands in code/config/catalog/log → shape-match scan fails the build non-zero; fails closed | **P-M7 (NEW — §3.1):** (a) planted unmarked secret VALUE in a TOML + a log → build REFUSES; (b) slot-names + marked-synthetic fixtures → build PASSES |

**Not-threat-ratified (I PROPOSE, ARGUS CONFIRMS):** the DC3 mock-emit (rev2 §2.7 — data/config addition,
no runtime attack path; §35.5 carve-out) and the §4 workflow-vs-app-code call (build-engine choice, no
runtime attack path) carry no threat-anchored probe of their own.

### §5.3 The build + verification steps (directive §6 DoD)

1. Build the REAL service: `tailscaled → tailscale serve --https=443 --accept-app-caps=<per-lane caps>
   unix:/run/.../core.sock → 0600 AF_UNIX UDS → gated handler → uvicorn`; the closed `PROVIDER_REGISTRY`;
   the `LANE_REGISTRY`; per-provider handlers; the response allow-list serializer; the two-phase audit; the
   seal-audit gate. Vertex registered as the first provider (`generate_grounded` + `embed`, both
   `auth: adc_sa`).
2. Run **P-M1..P-M7** against the REAL code (locally/against mocks) — all PASS.
3. INV-DEST/RESP/BIND/LANE each **fail-loud verified** (plant a violation → refuse-to-serve/load; not
   warn-and-continue). Seal-audit **fail-closed verified** (P-M7).
4. Frozen resolver byte-identical; the FULL `builder_deploy_core` suite green (re-run, not asserted).
5. NOMOS CONFORMANT; authorship = Denson Smith + seat-identity Co-Authored-By trailers; commit on the
   arc-77 build branch — **NOT merged, NOT pushed** (directive §5/§6).

---

## §6 Self-assessed weak points (6.2 post-work; where ARGUS should push hardest)

Carried from rev2 §6 (the five deltas ARGUS already framed) PLUS the NEW multi-consumer authz weak point.
The **first** one is the genuinely-novel delta ARGUS cold-audits specifically.

1. **[NEW — the reframe delta] Can per-lane `scopes` actually DENY cross-lane, and can one lane's tag reach
   another lane's provider/op?** The whole multi-lane isolation rests on: (i) the control plane resolving
   per-tag caps correctly (a node gets ONLY its tag's cap — the rev2 STRABO-r3 premise applied N times);
   (ii) `LANE_REGISTRY` cap-name → principal being server-side + fail-closed; (iii) INV-LANE catching an
   unknown-principal scope OR a serve-caps ≠ LANE_REGISTRY mismatch at load; (iv) the SAME INV-BIND /
   strip-and-reinject precondition rev2 depends on. **ARGUS should push hardest on:** does INV-LANE clause
   2 (serve caps == LANE_REGISTRY) actually make a lane un-served-by-omission fail CLOSED (no header) rather
   than fall through to a default principal? does P-M4's cross-lane clause FALSIFY a build that resolves an
   unmapped cap to a permissive default instead of denying? does adding a future lane grant it ZERO access
   by default (it should — a new principal is in no existing op's `scopes`)? And confirm the honest residual
   is correctly placed: `skill_id` is attribution, the tag→cap→lane principal is the trusted boundary, and
   the reframe adds NO new trust assumption beyond rev2's verified per-tag cap resolution.
   *Why this shape anyway:* per-lane cap names put the "which lanes are served" decision at the fail-closed
   serve boundary (not a trusted payload field); deny-by-default per-op `scopes` over lane principals is the
   least-privilege generalization of rev2's class-level scopes; INV-LANE makes it mechanically guarded like
   its INV- siblings rather than prose.

2. **[NEW — seal-audit] The seal-audit's shape-match set is a denominator I do not fully control.** It
   catches known secret SHAPES (Tailscale/SA-key/OAuth/Postgres-URI); a NOVEL secret format not in the
   shape set could slip. The fail-CLOSED posture (ambiguous high-entropy → FAIL) is the mitigation, but it
   trades false-negatives for false-positives that could block a clean build. **ARGUS should push on:** is
   the fail-closed default genuinely closed (unclassifiable match → build FAILS, per u--84m), and is the
   marked-synthetic allow-list (`SEAL_AUDIT_SYNTHETIC_`) narrow enough that it cannot become a bypass?
   *Why this shape anyway:* a deterministic shape-match + fail-closed-on-ambiguous is the unbypassable floor
   the PRINCIPAL's posture calls for on the high-risk secret-leak case; a marked-synthetic prefix is the
   minimum needed to let honest test fixtures coexist with a fail-closed audit.

3. **[carried r2] INV-RESP allow-list completeness against an EVOLVING Vertex response surface** — a build-time
   property, not by-construction; Google adding a field a legit feature wants surfaced requires re-proving
   the widened allow-list carries no credential echo. *Why this shape anyway:* allow-list is strictly safer
   than deny-list; opaque pass-through forbidden; P-M2 over the full surface is the right discipline for an
   upstream the core doesn't own.

4. **[carried r3/V-ENC + NEW V-ENC-LANE] The App-Capabilities on-the-wire encoding AND the per-lane cap-name
   → principal mapping are the open build-time confirmations.** rev2's V-ENC (App-Capabilities Q-encoded vs
   serialized-JSON) is joined by **V-ENC-LANE** (the exact per-lane cap-name strings + the serve
   comma-list-vs-repeated-flag form for `--accept-app-caps`), confirmed at build against the pinned
   TS version (≥ v1.94.1). *Why this shape anyway:* the newswire build hit TS-version identity-header
   landmines; pinning the version and confirming the exact encoding + cap strings at build is the proven
   discipline, not a design-time guess.

5. **[carried r1/r5] INV-DEST/INV-RESP/INV-BIND (and now INV-LANE) are loader/startup self-checks the build
   must ship as refuse-to-serve/load, not warnings.** A build that ships them as log-and-continue silently
   weakens the guarantee. **ARGUS should confirm P-M1(a)/P-M3(a)/P-M4(a-structural)/P-M7(a) actually
   FALSIFY a warnings-only implementation** (they assert non-zero exit / refuse-to-serve / build-fail, not a
   log line). *Why this shape anyway:* in-process fail-loud + a probe that asserts the exit is the strongest
   design-time mechanism without over-building; it is the A3 author duty (6.13).

6. **[carried] The threat-anchored probes P-M1..P-M7 exercise a service built THIS arc but against
   mocks/locally, not real infra.** They are falsifiable and run against REAL code (directive §6), but the
   real serve/socket/TS-version runtime is Phase 2/3. **ARGUS should pressure-test P-M2 (full-response
   redaction), P-M3(a) (in-process refuse-if-routable), and P-M4 (cross-lane denial) hardest** — the three
   most dependent on the real serve/socket/identity runtime. *Why this shape anyway:* the arc's DoD is a
   built + locally-probed service that relays up to be Phase-1-gated; the probes are the verification
   contract Phase 3 re-runs against the real deployment.

---

## §7 Out of scope (deliberately not addressed; ADA scope-fence + ARGUS frame)

- **ALL real provisioning** — no Railway project, no GCP SA mint, no Railway secret set, no Tailscale node,
  no DB stand-up, no spend cap wired. Phase 2, separately PRINCIPAL-gated. *Reason: directive §5 SCOPE FENCE;
  this arc builds + probes locally/against mocks only.*
- **Real secrets / money** — mint nothing; the prepaid-card spend cap is a Phase-2 concern. *Reason: §5.*
- **The stoa_of_science + newswire CLIENT skills** — theirs; this design specifies the client CONTRACT
  (rev2 §1.3) + the lane identity model (§2) only. *Reason: ownership split (sos--373 / nws-1n7).*
- **Multi-provider registry beyond Vertex** — the design accommodates N providers; only Vertex is wired now.
  *Reason: Vertex is the first provider; others follow the same registry + response-schema + credential
  boundary.*
- **Lanes beyond science + newswire** — the LANE_REGISTRY + per-lane cap model accommodates future lanes,
  but only science + newswire are registered now; a future lane is added by a grant + a `LANE_REGISTRY`
  entry + explicit per-op `scopes` edits (ZERO access by default). *Reason: consolidation center is built
  for the current two consumers; future lanes onboard explicitly, deny-by-default.*
- **Hard per-skill quotas** (a server-trusted per-skill identity) — the named r6 follow-up; the trusted
  boundary is the tag/lane. *Reason: per-skill HARD limits need a server-trusted skill identity, out of
  scope now.*
- **A streaming-gsearch op** — the `chunk_schema` pattern is carried (rev2 §1.3.1) so the build has it; no
  streaming op is wired into the Vertex surface this arc. *Reason: rev1/rev2 ops are `stream: False`.*
- **A fuzzy body-prose secret-leak workflow** — the seal-audit is deterministic shape-match this arc; any
  future fuzzy residual would be a committed in-harness workflow (§3.3), not built now. *Reason: no fuzzy
  residual exists in this service.*
