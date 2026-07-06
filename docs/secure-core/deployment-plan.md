<!-- author: Denson Smith -->

# Secure Service Core — Deployment Plan & Runbook

**Status:** Design approved (gate given). Phase 1 (build the core service) is next. Everything remains mock-only with **zero real infrastructure, credentials, or cost** until the Phase 2 provisioning steps — which require an explicit go and a bounded spend cap.

**Audience & purpose:** Denson Smith (operator) and future deployment sessions. This is a **living document** — it is revised as the deployment proceeds, and becomes the architecture + security documentation submitted to Zeotek for review.

---

## 1. What this is

A **secure service core** for the Science Stoa: a small, always-on server that holds **all external API keys** (Google Vertex / Gemini first, for search and embeddings) plus a **vector database**, so the individual skills on a builder machine never hold a credential. Skills reach the core only over a private Tailscale network.

**The problem it solves.** As the project's skills increasingly need API credentials (~46 of 338 skills), keeping keys on the builder machine is the recurring security risk. The core moves every key server-side and hands it out to no one.

## 2. Architecture at a glance

| Element | What it is |
|---|---|
| **Credentialed per-provider pass-through** | A skill names a provider + a pre-registered call; the core attaches that provider's key, makes the call, and returns only the declared result. The key never leaves the core. |
| **Scoped / deny-by-default** | The core can only reach providers in a closed, server-side registry — there is **no caller-supplied address** — so it cannot be turned into an open relay. The leak / abuse risk (SSRF, key-exfil) is closed by the structure itself, not patched. |
| **pgvector embeddings DB** | Postgres + pgvector on the core: the knowledge-graph store and skill/retrieval embeddings. |
| **Tailscale-only ingress** | The core is reachable only over the private tailnet; a builder holds **only a tailnet identity** — no Railway token, no service-account key, no API keys. |
| **Credential-discipline** | The agent never holds or sees a secret. Minting service accounts and setting secrets is a human / CI step. |

The full approved architecture is in the design document (`design-rev2`).

## 3. The four phases

### Phase 1 — Build the core service · *no real infrastructure, no cost*

The architecture is designed but the service code is not yet built. This phase builds the pass-through service itself — the Tailscale-serve front, the closed provider registry, the per-provider handlers, the response allow-list, and the two-phase audit — and verifies it by **re-running the design's own attack probes against the real code**: no caller-supplied address is constructable; no credential byte reaches a caller; a non-private network binding refuses to start. Built and tested locally / against mocks. Security-critical, so it runs as a full by-the-book review gauntlet.

### Phase 2 — Provision the real infrastructure · *real money starts here*

Stand up the actual cloud resources. **This is the only phase that costs money**, and nothing in it happens without an explicit start and a spend cap already in place.

- Prerequisites: Section 4.
- The agent drives each dashboard to the edge; **you generate every secret privately** (the agent never sees a value); the agent then helps you deploy it.
- Who-does-what credential boundary: Section 5.

### Phase 3 — Deploy + test

Push the built core to Railway, wire Vertex / Gemini through the pass-through, stand up the embeddings DB, and exercise the first slice end-to-end — search and embeddings through the core, from a builder holding only a tailnet identity.

### Phase 4 — Revise the architecture + security documentation for Zeotek

Once the core is real and exercised, revise this document and the security design to reflect the **actual** deployment. That revised pair is the artifact submitted for **Zeotek's external review**.

## 4. Prerequisites (needed before Phase 2)

| Prerequisite | Purpose | Status |
|---|---|---|
| A **GCP project** for the core | Hosts the Vertex service account + API enablement | _to confirm_ |
| A **prepaid card / billing account** | The **hard spend cap** — bounds all real cost | _to confirm_ |
| A **Railway account** | Hosts the `db` (Postgres + pgvector) and `serving` (the core) services | _to confirm_ |
| A **Tailscale tailnet** | The private network the core is reachable on | _to confirm_ |

## 5. Credential-discipline boundary (who does what)

| Secret | Human / you | Agent | Where it lives |
|---|---|---|---|
| **Vertex service-account key** (`GCP_SA_KEY_B64`) | Create the SA in the core's GCP project, grant least-privilege, get the key (or use Workload Identity Federation) | Names the slot only; never decodes or logs it | Railway secret (server-side); decoded to a `0600` temp file at startup |
| **Postgres password** (`POSTGRES_PASSWORD`) | — (the agent generates it into the OS keyring, never printed) | Pipes it into Railway via stdin — never sees the value | Railway secret; private `DATABASE_URL` (in-network only) |
| **Tailscale auth-key** (`TS_AUTHKEY`) | Mint a **reusable, tagged** key in the Tailscale admin console | Names the slot only | Railway secret; consumed by the container at start |

The Railway account token itself lives in the OS keyring (the `railway-keyring-deploy` pattern); the agent reads it only into the Railway CLI subprocess, never into its own view.

## 6. Provisioning checklist (Phase 2 detail)

**Order matters — the repo + Railway services come FIRST; every secret is then minted straight into the existing Railway service var, never stashed locally first.** (An earlier draft had this backwards — minting keys before the destination existed forced an unnecessary keyring detour.)

0. Confirm prerequisites (Section 4); set the spend cap. Confirm the **GitHub repo exists** and the deployable app is **committed + pushed** — Railway clones the repo at that commit and builds it.
1. **Provision the Railway project + both services** — `db` (Postgres + pgvector) and `serving` (the core) — with the secret **names declared** (`GCP_SA_KEY_B64`, `POSTGRES_PASSWORD`, `TS_AUTHKEY`) and values left empty.
2. **Now mint each secret and paste it directly into its Railway service var** — the destination already exists, so there is no local keyring detour:
   - Postgres password → `POSTGRES_PASSWORD` on `db` (or generated locally and piped in via the `railway-keyring-deploy` stdin pattern — never printed).
   - Vertex **service-account key** (SA/ADC, not an API key; least-priv `roles/aiplatform.user`) → base64 → `GCP_SA_KEY_B64` on `serving`.
   - reusable, **tagged** Tailscale auth-key (`tag:stoagen-catalog`) → `TS_AUTHKEY` on `serving`.
3. **Redeploy `serving`** so it picks up the secrets; the container brings up `tailscaled → serve → 0600 UDS trigger → uvicorn` and passes the platform healthcheck.
4. **First slice:** exercise the catalog over the mesh; then wire Vertex / gsearch through the pass-through and point the pgvector store at the knowledge-graph pipeline.

This reuses two already-proven skills — `newswire-builder-setup` and `railway-keyring-deploy` — that carried this exact Tailscale-serve / Railway pattern through to a live deployment, so the mechanics are battle-tested.

## 7. Status & next step

- **Design approved** (gate given); recorded up to the program epic.
- **Next:** Phase 1 — build the core service (no cost). Real provisioning waits on the prerequisites and an explicit start.

---

*This is a living document. It is revised through deployment and testing, and becomes the architecture + security documentation for Zeotek's review.*
