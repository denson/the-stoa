<!-- author: Denson Smith -->
<!-- ticket: stoa--q7f (the-stoa coordination) | requirement sos--373 (stoa_of_science) | epic u--9s2 (user-beadwork) -->
<!-- from: Polybius_the_Stoa (user-tier the-stoa forge owner) -->
<!-- status: DRAFT — pending NOMOS-on-directive, then attached to stoa--q7f on beadwork + launched -->

# u--9s2 increment 2.4 (DESIGN) — secure Railway core for stoa_of_science

**Audience:** the fresh Claude Code sessions opened to run this DESIGN gauntlet (PLINY_the-stoa + the floor-manager POLYBIUS_the-stoa).
**Authored by:** Polybius_the_Stoa (user-level Stoa agent, sid 990b0750-5572-4836-b9c7-18d626a12e96) on behalf of the PRINCIPAL (Denson Smith).
**Charter (coordinate here):** `stoa--q7f` (the-stoa). **Requirement:** `sos--373` (read it from the stoa_of_science repo: `cd C:\Users\denso\claude_projects\stoa_of_science && bw show sos--373`). **Epic:** `u--9s2` (user-beadwork; the Grand gates the design there).
**Builds on:** the-stoa `main` @ 376a563.
**Gate model:** this gauntlet produces a DESIGN. The design relays UP to the Grand to gate. **Nothing real is provisioned until the Grand gates the design AND the PRINCIPAL gives an explicit provision-go.** Emit-only / mock throughout.

---

## Why this exists

This is the cookie-cutter's FIRST REAL deployment target (the scienceclaw/stoa_of_science acceptance u--9s2 was built for). stoa_of_science's skills increasingly need external API credentials (~46 of 338 skills; Vertex/Gemini for gsearch first) + a Postgres/pgvector embeddings store. Keeping keys on the builder machine is the security problem we keep hitting. The secure answer is the in-mesh-builder pattern we already shipped (newswire): credentials + DB live on a Railway core; the builder reaches it over Tailscale holding ONLY a tailnet identity.

## The key finding (hold it — it shapes the whole gauntlet)

The **secure pass-through core is an ENTIRELY NEW runtime service.** It is NOT in `builder_deploy_core` and is NOT what the cookie-cutter is. The cookie-cutter is a one-shot, value-free PROVISIONING emitter (resolve→suggest→provision → a names-only spec, mock-only, 3-wall tripwire). It has zero notion of a credentialed proxy / egress / per-provider key-attach / long-running core. So 2.4 is TWO things:

1. **DESIGN a new secure service — the credentialed per-provider pass-through.** Architecturally a GENERALIZATION of `newswire-serving`: Tailscale `serve --https=443` → a `0600` AF_UNIX socket → a gated handler; deny-by-default tailnet policy; Funnel OFF (no public door); credentials server-side in Railway secrets; identity via the serve-injected `Tailscale-User-Login` header (NOT `WhoIs` loopback). The NEW part newswire did not have, and the ARGUS security crux: **per-provider scoping + key-attach** — a skill names a provider/call → the core attaches THAT provider's key → calls the external API → returns the result; the key never leaves the core. SCOPED / per-provider / deny-by-default — NOT an open "forward anything" egress proxy (that is a fat SSRF / key-exfil target).

2. **EMIT the stand-up via the existing cookie-cutter.** Run sos--373's services through resolve→suggest→provision to emit the value-free ProvisioningSpec (mock-only). Postgres+pgvector is ALREADY in the baseline; the new catalog work is small (a Vertex/Gemini entry — **service-account auth, NOT an API key** — plus Tailscale).

## Your one job

Produce a gated-ready DESIGN of the secure core: (a) the pass-through service shape that resolves the ARGUS security crux, (b) the cookie-cutter emit that stands it up (demonstrated mock-only), (c) the credential-discipline boundary, (d) the web-verified third-party premises. Relay the design UP to the Grand. Build NOTHING real.

## Full gauntlet — STRABO → DAEDALUS → ARGUS → ADA (mock-emit ONLY) → VERA → CATO → NOMOS. BY-THE-BOOK.
Standard POLYBIUS+PLINY team (no CHIRON/HAMILTON — a design, not a new agent/workflow). ARGUS's cold-audit of the pass-through security shape is the load-bearing checkpoint. STRABO leads (web-verify the premises) and feeds DAEDALUS.

---

## Comms — async with Polybius_the_Stoa via bw (`stoa--*`)

Coordinate on `stoa--q7f`. Polybius_the_Stoa (user-level owner) monitors + interjects; the floor-manager independently verifies each hand-back + relays up; the PRINCIPAL is NOT the relay — beadwork is. `bw comment <id> "text"` is positional, no `-m`; no backticks or `$()` in bodies. `bw prime` + `whoami` at activation. Every seat signs `[from: <NAME> | sid <session-id>]`.

---

## Read first

1. **The requirement `sos--373`** (in the stoa_of_science repo) — the WHAT, the security posture, and the OPEN DESIGN QUESTIONS it explicitly hands to the cookie-cutter/ARGUS.
2. **The cookie-cutter package** `agents/builder-deploy-core/builder_deploy_core/` — resolve→suggest→provision; the value-free `ProvisioningSpec` (`provision/spec.py`); the 3-wall tripwire (`provision/tripwire.py`, `mock.py`, `port.py`); the catalog shape (`dataload.py` + `data/catalog/*.toml`). Postgres+pgvector is already in `data/` baseline.
3. **The reuse skills** — `newswire-builder-setup` (the in-mesh precedent: the Tailscale-serve/0600-socket/deny-by-default/server-side-credential pattern + its §6 landmine map), `credential-discipline` (agent-never-holds-secrets; WIF; the out-of-package human/CI steps), `railway-keyring-deploy` (keyring-local Railway deploy; the DB-service recipe). (Under `~/.claude/skills/` and `substrate/skills/`.)

---

## Design items — DAEDALUS resolves in Phase A (surface at the design hand-back for go/no-go)

- **DC1 — the pass-through core shape (THE ARGUS SECURITY CRUX; DAEDALUS designs, ARGUS cold-audits).** Resolve sos--373's three open questions: (i) per-provider endpoints vs an authenticated allowlisted egress proxy — pick one and justify it against the SSRF/key-exfil threat; (ii) how a local skill names "which provider / which call" to the core; (iii) auth at the core (Tailscale identity → which operator/skill may use which provider), audit, rate-limit, and shared-quota handling (the shared-Gemini-quota concern). Deny-by-default is non-negotiable: the core only knows how to reach the specific providers we use and attaches the matching key per provider. State the threat model explicitly (it is an internet-egress box holding all keys — the most security-sensitive thing we have built).
- **DC2 — web-verify the third-party premises (STRABO, MANDATORY, before DC1 locks).** Confirm against CURRENT docs/sources, not memory: (a) **Vertex auth** — service-account-only reality + the 2026 standalone-key deprecation timeline (the requirement cites a prior gsearch — re-confirm the dates + that SA is the path for gsearch/Gemini); (b) **Railway** — private networking (`*.railway.internal`), secret store, running `tailscaled`+`tailscale serve` in a container, persistent volumes, pgvector/Timescale image support; (c) **Tailscale** — `serve`/Funnel, tagged auth keys, deny-by-default ACL policy, and the `Tailscale-User-Login` serve-injected-header mechanism (VERSION-SENSITIVE — newswire hit landmines on TS 1.98.x; pin the current behavior). Cite sources. A premise that does not verify is a design-blocker surfaced to the floor-manager, not worked around.
- **DC3 — the cookie-cutter emit (mock-only).** Express sos--373's services as cookie-cutter input and show the value-free `ProvisioningSpec` the existing machinery emits to stand up the core: the Railway services (db = Postgres+pgvector; serving = the pass-through), the Vertex **service-account** secret slot (NOT an API key), Tailscale (`TS_AUTHKEY`, a `thirdparty_rest_key`), the GCP project/SA/budget, secret-slot NAMES only. New catalog entries: a Vertex/Gemini `catalog/*.toml` (gcp_api = aiplatform, gcp_secret = the SA key slot) + a Tailscale entry. The frozen resolver stays byte-identical; the 3-wall tripwire holds; `assert_value_free` passes.
- **DC4 — credential-discipline boundary.** Name precisely the out-of-package HUMAN/CI steps (mint the Vertex SA + WIF binding; set the Railway secrets; mint the tagged Tailscale auth-key) vs what the agent/package may do. The agent NEVER holds or sees a secret. The core holds provider keys server-side; the builder holds ONLY a tailnet identity (no Railway token, no SA key, no API keys). Compose `credential-discipline` (CI/WIF) + `railway-keyring-deploy` (local) + the newswire mesh pattern.
- **DC5 — the first-slice PLAN (design only, do not build).** Name how Vertex/Gemini wires through the pass-through as the first provider + gsearch as the first thin-client skill (this SUPERSEDES sos--g8q's local-keyring approach — gsearch is built ONCE as a core-client, per sos--373). Name the embeddings-DB stand-up + pointing the KG pipeline at it. PLAN it; the BUILD is a follow-on after the gate + provision-go.
- **DC6 — honest stance + threat posture.** This is the most security-sensitive component we have designed (a credentialed internet-egress box). `threat-ratified`. ARGUS owns the security verdict; it is the gate-relevant output. No over-claim: the design closes the SSRF/key-exfil surface BY CONSTRUCTION (deny-by-default, per-provider scoping) — state how, concretely.

---

## Deliverables (the gated design package — land together)

1. **The design artifact** (written to the working tree or attached to `stoa--q7f`) — the pass-through core shape (DC1), the cookie-cutter emit (DC3), the credential-discipline boundary (DC4), the first-slice plan (DC5).
2. **STRABO's cited research** (DC2) — the web-verified premises with current sources.
3. **ARGUS's security verdict** on the pass-through shape (the crux) — the gate-relevant output.
4. **The mock-emit demonstration** (ADA, DC3) — the new catalog entries + the value-free `ProvisioningSpec` for the core, exercised against the MockProvisioner; tripwire-held; no real I/O.
5. Charter `stoa--q7f` updated with dispositions; the design relayed UP to the Grand at `u--9s2`.

## Verification / Definition of done

- **DC2 premises web-verified** with cited current sources (not memory); any unverifiable premise surfaced as a design-blocker, not worked around.
- **DC1 resolves the security crux** — the pass-through shape is locked (per-provider scoped, deny-by-default, the SSRF/key-exfil surface closed by construction), how a skill names a provider/call is specified, auth/audit/rate-limit/shared-quota are addressed. ARGUS's cold-audit PASSES (its verdict is the gate-relevant artifact).
- **The mock-emit (DC3) is value-free** — `assert_value_free` passes; the frozen resolver (`resolve.py`) is byte-identical (blob unchanged); the 3-wall tripwire holds (W1 no-I/O-imports grep EMPTY over provision/; W2 MockProvisioner the only port; W3 emit has no port); **the FULL `builder_deploy_core` test suite is green** (run it as the regression bar — the catalog additions re-derive resolution; per the gen-data-regen + full-suite disciplines).
- **Credential-discipline holds** — the design has agent-never-holds-secrets; the out-of-package human/CI steps are named; the builder holds only a tailnet identity.
- **ZERO real infra / money / credentials touched.** Emit-only / mock. No Railway project, no GCP project, no SA mint, no secret set, no Tailscale node.
- `Author=PRINCIPAL` (Denson Smith) zero-foreign on any commit; **NOMOS CONFORMANT** on the final hand-back.

## Out of scope (do NOT fold in)

- **ALL real provisioning** — deploying the core, minting the Vertex SA, setting Railway secrets, minting the Tailscale auth-key, standing up the DB. This waits for the Grand's gate of the design AND the PRINCIPAL's explicit provision-go (that is the 2.4-PROVISION step, a separate gated action).
- **The core SERVICE code** — DESIGNED (DAEDALUS) but NOT built/deployed this gauntlet (the design may change at the gate). ADA builds ONLY the mock cookie-cutter emit demonstration.
- **The first slice BUILD** (gsearch thin-client, embeddings stand-up) — PLANNED (DC5), built as a follow-on after the gate + provision-go.
- **The stoa_of_science CLIENT skills** — theirs. This design specifies the CLIENT CONTRACT (how a skill names a provider/call); the client skills are built in stoa_of_science.
- **arc-75 (bw-bootstrap)** — parked, separate; not touched here.

## Discipline

- BY-THE-BOOK gauntlet (NOT one-pass) — STRABO research + DAEDALUS design, surfaced for go/no-go; ARGUS cold-audits the pass-through security shape specifically before any mock-build.
- Web-verify every third-party capability premise against CURRENT sources before locking the design (the web-verify-tooling-premises discipline; this design rests heavily on Vertex/Railway/Tailscale capability claims my training cannot be trusted on).
- Emit-only / mock — the 3-wall tripwire holds; `assert_value_free` passes; the frozen resolver stays byte-identical; ZERO real infra/creds/money.
- Run the FULL `builder_deploy_core` suite as the regression bar for the catalog additions.
- bw syntax: positional `bw comment`, no backticks/`$()`; `bw prime` at activation; `--reason` on close.

## Suggested phasing

- **Phase A — research + design.** STRABO web-verifies the premises (DC2); DAEDALUS designs the pass-through shape (DC1) + the cookie-cutter emit (DC3) + the credential boundary (DC4) + the first-slice plan (DC5). Surface to the floor-manager for go/no-go.
- **Phase B — ARGUS cold-audit (the crux).** ARGUS audits the pass-through security shape (SSRF/key-exfil, deny-by-default, per-provider scoping, auth/audit). DAEDALUS revises if needed; re-audit.
- **Phase C — mock-emit (ADA).** Build ONLY the new catalog entries + the value-free `ProvisioningSpec` demonstration, tripwire-held.
- **Phase D — verify (VERA/CATO + NOMOS).** Value-free + tripwire + frozen-resolver + full suite; design coherence; STRABO's citations sound; ARGUS verdict satisfied.
- **Phase E — relay UP to the Grand.** The floor-manager runs final verification + relays the design package up to user-tier POLYBIUS, who relays to the Grand at `u--9s2` to gate. NOTHING real until gated + provision-go.

Standby, run.
