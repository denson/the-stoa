# u--9s2 Phase-1 — CHIRON lens: ownership & boundary architecture

**Seat:** MAJOR_CHIRON_the-stoa (team-architect). **Arc:** stoa--jw5 / u--9s2 Phase 1.
**Co-author seam:** MAJOR_HAMILTON owns the resolution-mechanism internals + provisioning
*sequence* + access-*trigger* flow. This artifact is the complementary **cast / ownership /
isolation-boundary / product-layer** lens. It defines WHO/WHAT owns each piece and WHERE the
structural boundaries fall; HAMILTON defines the ORDER and the CHOREOGRAPHY across them.
DAEDALUS unifies both into the formal Phase-1 design spec.

---

## 0. One-paragraph frame

The builder-deploy cookie-cutter is a **generic, reusable deployable** that turns a terse
per-builder **manifest** into a fully-provisioned, mesh-reachable builder, with each builder
**structurally isolated** from every other. The design's whole job is to draw three boundaries
crisply: (a) **generic cookie-cutter** vs **per-builder declaration** (the manifest seam);
(b) **per-builder isolation** as a derived structural lock, not a convention; (c) **access-layer
SHAPE** (generic, cookie-cutter-owned) vs **product CONTENT** (specific, project-seat-owned).
Get those three boundaries right and the model is composable, extensible, and safe by construction.

---

## 1. The three ownership tiers (the spine of the model)

Everything in this design belongs to exactly one of three tiers. Mis-assigning an item across
tiers is the primary failure mode (e.g. a project-specific key bloating a shared template, or
the cookie-cutter trying to own a builder's curated data).

| Tier | Owns | Authored / changed by | Reuse property |
|---|---|---|---|
| **T1 — Cookie-cutter (generic substrate)** | the UNIVERSAL BASELINE; the **category-template library**; the deterministic **resolution engine**; the **provisioning-spec emitter**; the **access-layer scaffold** (mesh-API + CLI-client-skill *shape*) | substrate arc (CHIRON authors templates/resolver; landing a new category = an arc) | reused **whole**, identical across every builder |
| **T2 — Per-builder manifest (declaration)** | the terse `{category + delta}` for ONE builder | the **project seat** standing up that builder (prospector team, Polybius_the_science_stoa, etc.) | one per builder; the **only** thing that differs per project at the key-model layer |
| **T3 — Per-builder product layer** | the **specific** mesh verbs, the curated **data**, the domain skill bodies | the **project seat** (NOT the cookie-cutter) | bespoke per builder |

**Load-bearing boundary T1↔T2:** the manifest is the **single seam** the cookie-cutter
consumes. The cookie-cutter never reaches into a project; the project never edits the
cookie-cutter — it only authors its manifest. Project-specific keys ride in the **delta** (T2),
never in a T1 template.

**Load-bearing boundary T1↔T3:** the cookie-cutter ships a **working, secured, empty-of-domain**
mesh endpoint + client-skill skeleton. The project seat fills in the verbs and the data. See §5.

---

## 2. The resolved-entry taxonomy (the structural unit that makes provisioning *derivable*)

The composability hinges on a single idea: **every line item — in the baseline, a category
template, or a delta — is a typed ENTRY whose KIND determines its own provisioning path.**
Resolution concatenates entries; provisioning dispatches on `kind`. No per-builder branching logic.

| `kind` | Example | Provisioning path (the kind IS the recipe) | Counts toward SA scope? | Needs `gcloud enable`? |
|---|---|---|---|---|
| `gcp_api` | Gemini embedding, Gemini search (gsearch), Google Maps | enable API + grant SA the API role | yes (API role) | **yes** |
| `gcp_secret` | a key stored in GCP Secret Manager | create/version secret; grant SA `secretAccessor` on **just that secret** | yes (per-secret accessor) | no |
| `railway_var` | `DATABASE_URL`, `NEWSWIRE_OPERATORS`, `TS_AUTHKEY` | set as a Railway service var (value from secrets mgr / keyring) | n/a (Railway-scoped) | no |
| `db_extension` | pgvector (baseline), PostGIS (geo toggle) | enable extension on the builder's DB at db-init | n/a | no |
| `thirdparty_rest_key` | **BLS OEWS API key** | store as secret + inject as Railway var; **no GCP API to enable** | yes (per-secret accessor) | **no** |

**Why this matters for my lens (ownership):** the SA scope is **mechanically the union of the
`scope-bearing` entries** (the `gcp_api` roles + the per-secret `secretAccessor` bindings) in the
*resolved set*. Nobody hand-writes an SA policy. Isolation (§4) is therefore *derived*, not asserted.

**Falsification guard the taxonomy resolves:** `labstat_bls`'s `+BLS OEWS` is a
`thirdparty_rest_key`, NOT a `gcp_api`. Without the taxonomy, a naive "enable every resolved API"
provisioner would try to `gcloud services enable bls-oews` and fail. The taxonomy makes the delta
provision correctly *and* keeps it out of every other builder's scope. (Flagging to HAMILTON:
the provisioning *sequence* branches on `kind`; the taxonomy is the contract between our lenses.)

---

## 3. Ownership map — who owns each provisioning step

The directive's named steps, each assigned an owner and a structural note. Note the split between
**design-time authorship** (a Stoa seat) and **deploy-time execution** (credential-disciplined:
the cookie-cutter EMITS a spec; a human/CI APPLIES it — agents never hold credentials).

| Step | Owner of the LIST | Owner of the VALUES / execution | Structural note |
|---|---|---|---|
| **Manifest authoring** | project seat (T2) | — | declares `{category + delta}` only; terse by design |
| **Resolution** `baseline+category+delta → full set` | cookie-cutter **resolution engine** (T1) | **deterministic code, no agent** | pure function; this is the near-determinism lock — the resolver has ~zero degrees of freedom |
| **GCP SA scoping** (per-builder) | derived = union of scope-bearing resolved entries (§2) | PRINCIPAL one-shot **or** CI via WIF (credential-discipline) | **one SA ⟷ one builder**, scope = *exactly* the resolved set; see §4 |
| **Railway key set** | resolved `railway_var` + secret-backed entries | secrets-mgr / keyring → Railway service vars | values never touch an agent; cookie-cutter emits the var-name list only |
| **GCP API enablement** | resolved `gcp_api` entries only | `gcloud services enable <list>` (human/CI) | exactly the resolved APIs, no superset |
| **Budget cap** | model REQUIRES a per-builder budget boundary; realized as project budget alert + per-service QUOTA hard-cap + opt-in kill-switch (§4 callout) — its **unit** (per-builder project vs shared) is the **held fork** (§9.1) | PRINCIPAL sets the numbers (blast-radius limit) | hard cap only achievable at **project** scope (GCP has no per-SA cap); unit routed to Grand |
| **DB extensions** | resolved `db_extension` entries | enabled at db-init on the builder's own DB | pgvector baseline; PostGIS only if geo template present |

**The cookie-cutter's deploy-time output is a PROVISIONING SPEC, not an action.** It produces the
exact, minimal, per-builder list of {APIs to enable, secrets to create, SA bindings, Railway vars,
DB extensions, budget cap}. A human or CI applies it. This keeps the model inside
`credential-discipline` (agents author; CI/human with bounded creds execute) and inside the
"the model declares WHAT keys exist + WHERE they live, never embeds values" constraint.

---

## 4. The per-builder isolation boundary as a STRUCTURAL ownership lock (not a convention)

The directive's load-bearing LOCK: *an SA never carries another builder's scope.* Modeled
structurally, isolation is **derived and unfalsifiable-by-misconfig**, not a rule someone must
remember to follow:

1. **Bijective identity.** One SA ⟷ one builder. The SA name derives from the builder slug
   (`sa-<builder-slug>@<gcp-project>.iam`). The SA *is* the builder's identity.
2. **Scope = a pure function of the manifest.** SA scope = union of scope-bearing entries in
   *this builder's* resolved set (§2). There is **no code path** that adds builder B's key to
   builder A's SA without first adding it to A's *manifest* — a visible, reviewed, obviously-wrong
   edit. Cross-builder leakage would require editing the **resolver itself**, making it a
   code-review-visible event, never a silent config drift.
3. **Partitioned blast radius — the isolation UNIT (per-builder PROJECT vs shared-project+per-SA) is
   a HELD FORK, see callout.** The *access* half of isolation is settled and team-owned (bijective SA
   + per-secret scope below). The *budget/blast-radius* half turns on a GCP capability that, now
   verified, **forces** the recommendation to **one GCP project per builder** — but that recommendation
   *corrects a premise that came from Polybius the Grand*, so the team does **not** close it; it is
   surfaced UP (see callout + §9.1).
4. **Least-privilege per secret.** `secretAccessor` is bound **per secret**, not project-wide, so
   an SA reads only its own resolved secrets even before the per-project boundary is counted.

> **SETTLED CAPABILITY (STRABO independent current-GCP-docs verification, 2026-06-25 — supersedes my
> first-pass gsearch) — GCP has NO per-service-account spend cap, and Cloud Billing budgets are
> ALERT-ONLY.** Verified findings, primary sources fetched 2026-06-25:
> - **No per-SA budget scope.** Budgets scope only to billing-account / org / folder / **project** /
>   service / resource-label; a service account's spend bills to **its project**, never the SA.
> - **Budgets are alerting-only — no native hard cap at any scope.** Docs verbatim: *"Setting a
>   budget does not automatically cap … usage or spending."* *(This REFUTES my first-pass gsearch
>   claim of "native auto-pause Spend Caps" — STRABO's primary-source check corrected it; I retract
>   that line. HAMILTON's "alert-only" read was the correct one.)*
> - **Kill-switch (budget → Pub/Sub → Cloud Function → detach billing)** is Google-documented but
>   **reactive/lagging** (notifications "may take several hours"; "doesn't guarantee that you won't
>   spend more than your budget"; detaching billing shuts down ALL resources in the project) — a
>   project-level reactive footnote, **not** an isolation tier.
> - **The real-time hard cap** is therefore **per-service QUOTA limits** (e.g. cap the Vertex AI
>   embedding request/token quota), enforced in real time — load-bearing, not a footnote (HAMILTON §5).
> - Sources: `docs.cloud.google.com/billing/docs/how-to/budgets`,
>   `…/disable-billing-with-notifications`, `…/notify`.
>
> **Consequence (FORCED-BY-EVIDENCE RECOMMENDATION, held for Grand):** a *hard per-builder budget
> boundary* is unachievable at SA granularity, so it **forces one GCP project per builder** as the
> isolation unit. **This corrects the directive's stated isolation premise** (Grand's "per-builder
> GCP SA + budget cap" implied shared-project + per-SA scoping). Per supervisor direction
> (Polybius_the_Stoa, 2026-06-25) the team does **NOT** close this — it is a **premise-correction-UP**.
> The design *illuminates + recommends with the cited evidence*; **Polybius the Grand owns the call.**
> The fork, both branches, and the forced recommendation are written up in §9.1.

**The structural claim (the part the team DOES own):** the *access*-isolation is a *consequence of
the derivation pipeline* (manifest → resolved set → SA scope is 1:1 and total) — an SA *cannot* hold
a scope its manifest didn't declare; cross-builder leakage would require editing the resolver itself
(code-review-visible), never a silent config drift. The *budget*-isolation unit rides on top of that
and is the held-fork above. (ref `zeotek_newswire/SECURITY.md`, `u--eq6`, `newswire-builder-setup` §7.)

**Seam impact for HAMILTON (under the recommended branch):** the provisioning *sequence* creates/
selects the per-builder GCP project FIRST, then the SA inside it, then per-secret scope-bind, then
the budget realization = **project budget ALERT + per-service QUOTA (the real hard cap) + opt-in
kill-switch** (HAMILTON §5). The §3 "budget cap" step is a project-level construct, not an SA-level one.

---

## 5. The agent-access layer — SHAPE (cookie-cutter) vs CONTENT (project seat)

The access layer is **first-class in the deployable** (every builder ships it), and it is **split
across two tiers** at a clean line:

**T1 — Cookie-cutter owns the SHAPE (generic, identical everywhere):**
- the **mesh-API scaffold**: `tailscaled` (userspace) → `tailscale serve --https=443` → a **0600
  AF_UNIX socket** → the in-mesh trigger; identity = the serve-injected `Tailscale-User-Login`
  header (never WhoIs-on-loopback); **deny-by-default** Tailscale policy; the **operator-allowlist**
  mechanism (`<BUILDER>_OPERATORS` + `group:operators`); Funnel OFF.
- the **CLI-client-skill template**: a `newswire-trigger`-shaped skeleton the operator's agent
  installs to `~/.claude/skills/` — trigger-over-mesh holding **only a tailnet identity** (no
  Railway token, no SA key), `--check` door-probe, counts-only response handling, redacted-error tail.

**T3 — Project seat owns the CONTENT (specific, bespoke):**
- **which verbs** the endpoint exposes (newswire's `/run` = collect+embed; scienceclaw's
  ingest+search; etc.) and what the counts/response mean,
- the **curated data** the builder serves,
- the **domain body** of the client skill (what the trigger actually does for that product).

**The clean line:** the cookie-cutter hands the project seat a **working, secured, mesh-reachable
endpoint + a client-skill skeleton with ZERO domain verbs**. The project seat adds verbs and data.
The cookie-cutter never knows what a builder *does*; the project seat never re-implements mesh
security. (This is also the boundary that keeps the cookie-cutter reusable: the moment a domain
verb leaks into T1, the cookie-cutter stops being generic.)

*Seam with HAMILTON:* he owns the **trigger FLOW** (the resolve→provision→serve sequence and the
operator-trigger choreography); I own the **WHO-owns-which-half boundary** above. The header-trust
identity + UDS transport are shared facts we both cite (from `newswire-builder-setup` §6).

---

## 6. Category-template library + additive extensibility (open–closed by construction)

**Where category templates live:** in the **cookie-cutter source** as a versioned **template
library** — one named record per category (a `categories/<name>.yaml` directory or a single
`categories.yaml` registry), each declaring its list of typed entries (§2). They are T1: shared,
reused whole, reviewed via arc when a new one lands (a new category is a *reusable substrate unit*,
not a per-project artifact).

**Baseline** is a sibling record (`baseline.yaml`): Gemini embedding + Gemini search (gsearch) +
the DB credential set + **`{db_extension, pgvector}`** (DECIDE-A, JOINT-CLOSED with HAMILTON —
every builder embeds ⇒ every builder needs the vector store, so pgvector is baseline, matching
directive §3's explicit "pgvector is the baseline"; the document-consuming template therefore does
**not** re-list pgvector — set-union would make it harmless either way). Resolution =
`baseline ⊕ categories[manifest.category] ⊕ manifest.delta`.

**The extensibility property (open–closed):**
- **Open for extension:** adding a category = adding **one new record** to the library. Nothing
  existing is touched.
- **Closed for modification:** the resolver, the baseline, and existing category templates do
  **not** change when a category is added. The resolver is **category-agnostic** — it looks up
  `manifest.category` by name and merges; it has no per-category code.

A **delta**, by contrast, lives in the **project's manifest (T2)**, never in the shared library —
that is the entire point of the delta: project-specific keys ride per-builder and never bloat a
shared template. (The `labstat_bls` `+BLS OEWS` case in §7 is the proof.)

**Adding a new category later** (e.g. `timeseries`, `imagery`): author a new
`categories/<name>.yaml` with its typed entries, land it via arc, done — no resolver change, no
existing-template change, no other builder affected.

---

## 7. The three worked examples, in ownership/boundary terms

The model is **falsified if any of these can't be expressed tersely and resolved correctly.**

### 7.1 prospector — geospatial, no delta
```yaml
# manifest (T2, authored by prospector team)
builder: prospector
category: geospatial
delta: {}
```
**Resolves to:** baseline (Gemini-embed `gcp_api`, gsearch `gcp_api`, DB creds `railway_var`)
+ geospatial template (Google Maps `gcp_api`, PostGIS `db_extension`).
**SA `sa-prospector`** scoped to: embed + gsearch + Maps API roles; secretAccessor on the
baseline secrets. **APIs enabled:** embed, gsearch, Maps. **DB:** pgvector + **PostGIS**.
**Budget cap:** prospector's own. **T3 (prospector team):** the geo skills + curated geo data.

### 7.2 scienceclaw — document-consuming, no delta
```yaml
# manifest (T2, authored by Polybius_the_science_stoa — coordinate u--4at)
builder: scienceclaw
category: document-consuming
delta: {}
```
**Resolves to:** baseline (incl. pgvector) + document-consuming template (document-parsing
`gcp_api`). **SA `sa-scienceclaw`** scoped to: embed + gsearch + doc-parsing.
**DB:** pgvector (no PostGIS). **T3 (science stoa):** the doc-ingest skills + the curated corpus
that serves all prospector projects for cross-field discovery. **Boundary note:** "serves all
prospector projects" is a **T3 product-layer** property (a shared *service* the project seat
builds on top), **not** a cookie-cutter concern — the cookie-cutter just gives scienceclaw a
doc-consuming builder; the science stoa makes it a shared discovery service.

### 7.3 labstat_bls — document/data + delta `+BLS OEWS` (the load-bearing delta test)
```yaml
# manifest (T2)
builder: labstat_bls
category: document-consuming      # the doc/data template, reused WHOLE
delta:
  add:
    - { name: BLS_OEWS_API_KEY, kind: thirdparty_rest_key }
```
**Resolves to:** baseline + document-consuming template + **BLS_OEWS_API_KEY**.
**The proof points:**
- the **template is untouched** — BLS OEWS rides in the **delta**, so no other builder sees it;
- **isolation holds** — only `sa-labstat_bls` carries the BLS OEWS secret accessor; `sa-prospector`
  / `sa-scienceclaw` do not;
- the **taxonomy makes it provision correctly** — `kind: thirdparty_rest_key` ⇒ store as secret +
  inject as Railway var, **no `gcloud services enable`** (BLS OEWS is not a GCP API). A naive
  "enable every resolved API" model would break here; ours doesn't.

This case is the falsification test that **delta ≠ template bloat** and that **isolation is real**.

---

## 8. stoa--reg / manifest alignment (noted, not built — per constraint)

The per-builder manifest and the `stoa--reg` seat registry are **different registries that will
later merge** (the manifest↔registry merge is a *later* integration step; Phase-1 does **not**
depend on the parallel `stoa--reg` liveness fix). My lens-note for that later step: the manifest
is keyed by **builder slug** and the registry row is keyed by **seat (`ROLE_slug`)** — the join key
when they merge is the **builder/project slug**, which both already carry. No Phase-1 dependency;
flagging the join key so the later integration is additive.

---

## 9. Self-assessed weak points (for ARGUS/DAEDALUS to pressure-test)

1. **Isolation-UNIT fork — SETTLED capability, HELD decision (routed to Polybius the Grand).**
   *Capability (settled, STRABO cited, §4 callout):* GCP has no per-SA spend cap; budgets are
   alert-only; a hard per-builder budget boundary is only achievable at the **project** scope.
   *The fork this forces:*
   - **Branch A — per-builder GCP PROJECT (forced-by-evidence RECOMMENDATION).** Each builder = its
     own project (its SA, secrets, enabled APIs, project budget alert + per-service quota hard-cap +
     opt-in kill-switch). The only branch that delivers a real per-builder budget boundary. **Cost:**
     correcting Grand's stated isolation premise (SA → PROJECT); more projects to create/manage.
   - **Branch B — shared project + per-SA scoping (matches Grand's stated premise).** Keeps one
     project; per-SA scope gives *access* isolation — but **cannot deliver a per-builder budget cap
     at all** (no per-SA budget scope). Budget control degrades to project-wide quotas shared across
     builders. **Fails the directive's literal "budget cap per builder."**
   *Why it's held, not closed:* per supervisor direction (Polybius_the_Stoa, 2026-06-25), Branch A
   **corrects a premise that came from Polybius the Grand**, so it is a premise-correction-UP — the
   team recommends with cited evidence; **the Grand owns the call.** Surfaced in the CO-DESIGN
   CONVERGED package; not locked below the Grand.
2. **Category vs delta boundary judgment.** When does a recurring delta "graduate" into a new
   category template? Proposed governance rule (for DAEDALUS to ratify): a `(kind,name)` add that
   appears in **2+ builders' deltas** is promoted to the relevant category template (or a new
   category) **via arc** — so deltas stay genuinely project-singular and don't quietly accrete.
3. **`document/data` vs `document-consuming`.** The directive names labstat_bls "document/data";
   both HAMILTON and I map it onto the `document-consuming` template + delta (HAMILTON's resolution
   §3 treats `document/data` as the same shape). If "data" later implies entries the doc-consuming
   template lacks, that's a delta or a 4th category — DAEDALUS to confirm the template covers it.
4. **Multi-category builders.** The model assumes one `category` per manifest. A future builder
   needing geospatial **and** document-consuming would need either a category list or a richer
   delta. Out of Phase-1 scope by the three worked examples; named here as "not yet supported."
2. **Category vs delta boundary judgment.** When does a recurring delta "graduate" into a new
   category template? The model is silent; that's a governance call (probably: 2+ builders share it
   ⇒ promote to category via arc). Worth an explicit rule so deltas don't quietly accrete.
3. **`document/data` vs `document-consuming`.** The directive names labstat_bls "document/data";
   I mapped it onto the `document-consuming` template + delta. If "data" implies entries the
   doc-consuming template lacks, that's either a delta or a 4th category — DAEDALUS should confirm
   the template list covers it or split it.
4. **Multi-category builders.** The model assumes one `category` per manifest. A future builder
   needing geospatial **and** document-consuming would need either a category list or a richer
   delta. Out of Phase-1 scope by the three worked examples, but worth a named "not yet supported."

---

## 10. Seam summary (what HAMILTON plugs into)

- I define the **resolved-entry taxonomy** (§2) — HAMILTON's provisioning *sequence* dispatches on
  `kind`.
- I define **who owns each step** (§3) — HAMILTON defines the *order* + idempotency/re-runnability.
- I define the **isolation boundary** structurally (§4) — HAMILTON sequences the SA-create +
  scope-bind so it lands isolated.
- I define the **access-layer SHAPE/CONTENT boundary** (§5) — HAMILTON owns the **trigger flow**
  across it.
- I define the **category library + extensibility** (§6) — HAMILTON's resolver reads it.

Co-constrain points to confirm with HAMILTON: (a) the `kind` enum in §2 is the shared contract;
(b) the provisioning spec is an *emitted artifact* (his sequence produces it, a human/CI applies
it — credential-discipline); (c) the access-layer scaffold is one ordered step in his sequence.
