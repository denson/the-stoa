# u--9s2 Phase-1 — CO-DESIGN CONVERGED: composable key-provisioning model + per-builder manifest

**Arc:** stoa--jw5 / u--9s2 Phase 1. **Status:** CO-DESIGN CONVERGED — every element below is
jointly agreed **except one explicitly HELD fork** (the isolation UNIT, §6/§11), surfaced UP to
Polybius the Grand per supervisor direction (it corrects a Grand-stated premise; the team does not
close it).

**Co-authors (complementary lenses, single seam):**
- **MAJOR_CHIRON** — cast / ownership / isolation-boundary / product-layer (`design/chiron-ownership-model.md`).
- **MAJOR_HAMILTON** — resolution rule / provisioning choreography / DB-extension / credential+bw seam (`design/choreography-hamilton.md`).
- **Single writer of this unified doc:** CHIRON. **Next:** DAEDALUS formalizes; full gauntlet hardens.

> This is a DESIGN deliverable, not built code. It defines WHAT to provision per builder and HOW the
> model composes; it provisions nothing. PRINCIPAL provisions on Railway/GCP only after the Grand's gate.

---

## 0. The model in one paragraph

A per-builder **manifest** declares `{category, delta}` tersely. A **pure resolution function**
expands it — set-algebra over **typed entries** — into a **resolved set**. The cookie-cutter then
**emits a provisioning spec** (it does not act); a **credential-disciplined applier** (CI via WIF, or
a human one-shot) executes that spec in an **ordered, idempotent, fail-closed, re-runnable** sequence
that lands the builder **isolated**. Category templates are a reusable, additively-extensible library;
the **agent-access layer** (mesh API + CLI client skill) is a fixed scaffold every builder gets. Three
ownership tiers keep it composable: **T1 cookie-cutter** (generic) / **T2 manifest** (per-builder
declaration) / **T3 product** (the project seat's verbs + data).

```
manifest {category, delta} ──resolve (pure fn)──▶ resolved set (typed entries)
   ──emit──▶ provisioning spec ──apply (CI/human, credential-discipline)──▶ live ISOLATED builder
```

---

## 1. Three ownership tiers (the spine)

| Tier | Owns | Authored by | Reuse |
|---|---|---|---|
| **T1 — Cookie-cutter (generic substrate)** | baseline; category-template **library**; the deterministic **resolver**; the provisioning-spec **emitter**; the access-layer **scaffold** (mesh-API + CLI-client-skill *shape*) | substrate arc | reused **whole**, identical per builder |
| **T2 — Per-builder manifest** | the terse `{category, delta}` | the **project seat** standing up that builder | one per builder; the **only** per-project thing at the key layer |
| **T3 — Per-builder product** | the **specific** mesh verbs, curated **data**, domain skill bodies | the **project seat** (NOT the cookie-cutter) | bespoke per builder |

Boundary **T1↔T2** = the manifest (the single seam the cookie-cutter consumes; project-specific keys
ride the **delta**, never a shared template). Boundary **T1↔T3** = the cookie-cutter ships a working,
secured, domain-empty endpoint + client-skill skeleton; the project seat fills verbs + data (§8).

---

## 2. The typed resolved-entry taxonomy (the atomic unit — JOINT CONTRACT)

Every line item — in the baseline, a category template, or a delta — is a typed **entry** whose
`kind` determines its own provisioning path. **Resolution concatenates typed entries; the provisioning
sequence dispatches on `kind`.** This is the load-bearing contract between the two lenses.

| `kind` | Example | Provisioning path (the kind IS the recipe) | Scope-bearing? | `gcloud enable`? |
|---|---|---|---|---|
| `gcp_api` | Gemini embedding, Gemini search, Google Maps, document-parsing | enable API + grant SA the API role | yes (API role) | **yes** |
| `gcp_secret` | a Secret-Manager-held key (e.g. `POSTGRES_PASSWORD`, `MAPS_API_KEY`) | create/version secret; grant SA `secretAccessor` on **just that secret** | yes (per-secret) | no |
| `railway_var` | `DATABASE_URL`, `<BUILDER>_OPERATORS`, `TS_AUTHKEY` | set as a Railway service var (value from secrets mgr / keyring) | n/a | no |
| `db_extension` | pgvector (baseline), PostGIS (geo) | enable extension on the builder's DB at db-init (§7) | n/a | no |
| `thirdparty_rest_key` | **BLS OEWS API key** | store as secret + inject as Railway var; **no GCP API** | yes (per-secret) | **no** |

The SA scope is the **mechanical union of the scope-bearing entries** in the resolved set — never
hand-written (§6). The `thirdparty_rest_key` kind is what makes `labstat_bls`'s `+BLS OEWS` resolve
correctly (secret-only, no `gcloud enable`) — a naïve "enable every resolved API" model breaks here.

---

## 3. The per-builder manifest schema (DoD item 2)

```yaml
builder: <slug>            # join key to stoa--reg (§10); also the SA / project / skill slug
category: <category-name>  # exactly one; looked up in the T1 category library (§1, extensibility §4)
delta:                     # OPTIONAL, terse — the only project-specific keys
  add:  [ { kind: <kind>, name: <NAME> }, ... ]   # project-required entries
  omit: [ { kind: <kind>, name: <NAME> }, ... ]   # standard entries this builder drops
```

Terse by design: a no-delta builder is two lines (`category:` + empty `delta:`). The manifest is the
**only** artifact that differs per project at the key-model layer.

---

## 4. The resolution rule (pure, unambiguous — DoD item 2) + extensibility (DoD item 1)

Baseline, each category template, and the delta are each a **list of typed entries**. Resolution is
pure set-algebra:

```
resolve(manifest) =
    ( ( BASELINE  ∪  CATEGORY_TEMPLATE[manifest.category] )  \  delta.omit )  ∪  delta.add
```

- **Entry identity for set ops:** two entries are equal iff `(kind, name)` match.
- **Precedence (deterministic):** union baseline+template → subtract `omit` → union `add`.
  **`add` wins over `omit`** (an explicit project-required add is never silently removed).
- **Lint:** a `(kind,name)` in BOTH `add` and `omit` is a manifest WARNING (probable author error),
  resolved as **kept** (add-wins) and surfaced — never silently dropped.
- **Purity:** same manifest ⇒ same resolved set, no environment reads — which is exactly what makes
  resolution **testable as a design** (§9) and safe to re-run inside the idempotent choreography.

**Baseline** (`baseline.yaml`): `{gcp_api, gemini-embedding}`, `{gcp_api, gemini-search}`,
`{railway_var, DATABASE_URL}`, `{gcp_secret, POSTGRES_PASSWORD}`, **`{db_extension, pgvector}`**.

**Category templates** (`categories/<name>.yaml`, one record each):
```
geospatial         = [ {gcp_api, google-maps}, {db_extension, postgis} ]
document-consuming = [ {gcp_api, document-parsing} ]          # pgvector already baseline
document/data      = [ {gcp_api, document-parsing} ]          # same shape as document-consuming
```

**pgvector → BASELINE (JOINT-CLOSED, DECIDE-A).** Every builder embeds ⇒ every builder needs the
vector store. This matches the directive §3 ("pgvector is the baseline") and fixes the otherwise-silent
bug where a geospatial builder (whose template lists Maps + PostGIS, not pgvector) would resolve with
no vector store despite embedding. The document-consuming template therefore does **not** re-list
pgvector (set-union would make it harmless either way).

**Extensibility (open–closed, DoD item 1):** adding a category = adding **one record** to
`categories/`. The resolver is category-agnostic (looks up `manifest.category` by name and merges) —
**open for extension, closed for modification**: baseline, resolver, and existing templates never
change when a category is added. A new category lands **via arc** (it is a reusable T1 unit). A
recurring **delta** that appears in **2+ builders** is the trigger to *promote* it into a template (or
a new category) via arc — the governance rule that keeps deltas genuinely project-singular (§13).

---

## 5. The provisioning choreography — emit-then-apply (DoD item 3)

The cookie-cutter **emits a provisioning spec** (the exact, minimal per-builder list of {SA + scope,
APIs, secrets, Railway vars, DB extensions, budget boundary}); a **credential-disciplined applier**
(CI via WIF, or a human one-shot) executes it. **Agents never hold credential values** — the spec
names slots, not values (credential-discipline, railway-keyring-deploy). Every step **dispatches on
the resolved entry's `kind`** (§2).

```
S0  ISOLATION SCAFFOLD  (the per-builder LOCK — precedes any key materialization)
    0a  ensure builder's GCP PROJECT          [under the recommended branch — §6/§11 held fork]
    0b  ensure SA  sa-<builder-slug>@<project>.iam      (bijective: 1 SA ⟷ 1 builder)
    0c  set the BUDGET boundary  =  project budget ALERT + per-service QUOTA hard-cap + opt-in killswitch (§6)
S1  GCP API ENABLEMENT          kind == gcp_api      → gcloud services enable <api> (idempotent) + grant SA the API role
                                                       fail-closed: an enable failure ABORTS the spec
S2  SECRET SLOT MATERIALIZATION kind ∈ {gcp_secret, thirdparty_rest_key}
    2a ensure secret SLOT (Secret Manager / OS keyring)   2b grant SA secretAccessor on JUST that secret
    2c VALUE population = HUMAN / credential-discipline GATE — provision BLOCKS here until slots populated
       (thirdparty_rest_key has NO S1 step — secret-only; the labstat_bls proof)
S3  RAILWAY PROVISIONING        kind == railway_var (+ secret-backed entries as vars)
    db service (baked-init image, §7) + serving service (trigger + serving face) + vars via STDIN only
    + this builder's SA-key-b64 ONLY (never another builder's) + persistent volume at /var/lib/tailscale
S4  DB EXTENSION APPLICATION    kind == db_extension  → baked-init emits exactly the resolved CREATE EXTENSION lines (§7)
S5  AGENT-ACCESS LAYER  (FIXED T1 scaffold — every builder; NOT manifest-resolved — §8)
S6  VERIFY  (idempotent re-run = no-op + health probe): door preflight; each resolved gcp_api enabled;
            each resolved db_extension present; no secret slot unpopulated (else report BLOCKED-on-human)
```

**Properties:** **ordered** (isolation S0 before any key S2 before any serving S3/S5); **idempotent /
re-runnable** (every step create-or-get; a re-run converges to the resolved set and cannot widen
scope); **fail-closed** (any failure ABORTS the remainder; a half-provisioned builder never reaches
S5 serving; the S2c human secret gate is a *block*, not an improvised value).

---

## 6. Per-builder isolation — settled access half + HELD budget half

**Access isolation (team-owned, derived, settled).** SA scope = the mechanical union of scope-bearing
resolved entries (§2). One SA ⟷ one builder (bijective; SA name from the builder slug). `secretAccessor`
bound **per secret**. There is **no code path** that gives builder A's SA builder B's key without
editing A's *manifest* (visible, reviewed) or the *resolver itself* (code-review-visible) — never a
silent config drift. S3 injects only this builder's SA key. This half is closed in-team.

**Budget isolation (capability SETTLED; UNIT is a HELD FORK → Grand).** Verified via STRABO's
independent current-GCP-docs check (2026-06-25, primary sources, VERA-confirmed verbatim):
- GCP has **no per-service-account** budget scope; an SA's spend bills to its **project**.
- Cloud Billing budgets are **alert-only** — *"Setting a budget does not automatically cap … usage or
  spending."* No native hard auto-cap at any scope. *(This refuted CHIRON's first-pass "native
  auto-pause Spend Caps" claim — retracted; HAMILTON's alert-only read was correct.)*
- The kill-switch (budget → Pub/Sub → Cloud Function → detach billing) is documented but
  **reactive/lagging** ("may take several hours"; "doesn't guarantee you won't spend more"; detaching
  billing kills ALL project resources) — a footnote, not a tier.
- The **real-time hard cap** is therefore **per-service QUOTA limits** (e.g. cap Vertex AI embedding
  request/token quota) — load-bearing.
- Sources: `docs.cloud.google.com/billing/docs/how-to/{budgets, disable-billing-with-notifications, notify}`.

⇒ a **hard per-builder budget boundary is only achievable at the project scope**, which **forces** the
isolation unit to be a **per-builder GCP project** — and that **corrects a premise Polybius the Grand
stated** (per-builder SA + budget cap implied shared-project + per-SA scoping). Per supervisor direction
this is a **premise-correction-UP, not a team decision** — see the fork in §11.

---

## 7. DB-extension parameterization (DoD item 4)

The resolved `db_extension` set parameterizes the `db` service:
- **`pgvector`** (`CREATE EXTENSION vector`) — **baseline, always emitted**; bundled in the newswire
  base image (`timescaledb-ha:pg18`).
- **`postgis`** (`CREATE EXTENSION postgis; postgis_topology`) — emitted **iff** `postgis` ∈ resolved
  set (geo-builders only). Same shape as the parameterized API set: a resolved entry drives a concrete action.

**Phase-2-facing note (DECIDE-C):** PostGIS is not in the `timescaledb-ha` bundle, so a geo-builder
needs a **postgis-capable base image** (a small derived `Dockerfile FROM timescaledb-ha:pg18` +
PostGIS). The base image is thus parameterized by `postgis ∈ resolved_set` (geo → postgis image;
non-geo → stock pgvector image). **Recommendation:** the derived Dockerfile. Flagged for the Phase-2 build arc.

---

## 8. The first-class agent-access layer — SHAPE vs CONTENT (DoD item 5)

First-class in the deployable (every builder ships it; the manifest never asks for it), split at a clean line:

**T1 — cookie-cutter owns the SHAPE (generic, identical):** the mesh-API scaffold — `tailscaled` →
`tailscale serve --https=443` → a **0600 AF_UNIX socket** → the in-mesh trigger; identity = the
serve-injected `Tailscale-User-Login` header (never WhoIs-on-loopback); **deny-by-default** policy;
the `<BUILDER>_OPERATORS` + `group:operators` allowlist; Funnel OFF — plus the **CLI-client-skill
template** (`newswire-trigger`-shaped: trigger-over-mesh with **only a tailnet identity**, `--check`
door-probe, counts-only response, redacted-error tail).

**T3 — project seat owns the CONTENT (specific):** which **verbs** the endpoint exposes (newswire's
`/run` = collect+embed; scienceclaw's ingest+search), the curated **data**, the domain skill body.

**The clean line:** the cookie-cutter hands the project seat a working, secured, mesh-reachable
endpoint + a client-skill skeleton with **zero domain verbs**; the project seat adds verbs + data. The
moment a domain verb leaks into T1, the cookie-cutter stops being generic.

---

## 9. The three worked examples — resolved (the falsification test, DoD item 6)

**prospector** `{category: geospatial, delta: {}}`
```
resolve = BASELINE ∪ [{gcp_api,google-maps},{db_extension,postgis}]
  gcp_api: gemini-embedding, gemini-search, google-maps | gcp_secret: POSTGRES_PASSWORD (+MAPS_API_KEY)
  railway_var: DATABASE_URL | db_extension: pgvector, postgis        ✓ "baseline + Maps + PostGIS"
```
**scienceclaw** `{category: document-consuming, delta: {}}`  (coordinate Polybius_the_science_stoa, u--4at)
```
resolve = BASELINE ∪ [{gcp_api,document-parsing}]
  gcp_api: gemini-embedding, gemini-search, document-parsing | db_extension: pgvector
  ✓ "baseline + pgvector + document-parsing"   ("serves all prospector projects" is a T3 product property, not cookie-cutter)
```
**labstat_bls** `{category: document/data, delta: {add: [{thirdparty_rest_key, BLS_OEWS_API_KEY}]}}`
```
resolve = (BASELINE ∪ [{gcp_api,document-parsing}]) ∪ [{thirdparty_rest_key, BLS_OEWS_API_KEY}]
  gcp_api: gemini-embedding, gemini-search, document-parsing   ← BLS adds NO gcp_api
  db_extension: pgvector | thirdparty_rest_key: BLS_OEWS_API_KEY → secret + Railway var; NO gcloud-enable
```
✓ **The load-bearing test.** `BLS_OEWS_API_KEY` rides the **reused** template as one delta entry — a
key no other builder needs — **without bloating the template**; its `kind` makes the sequence skip
API-enablement natively; only `sa-labstat_bls` carries it (isolation). Proves **delta ≠ template bloat**.

---

## 10. stoa--reg alignment (noted, no dependency — DoD item 7)

The per-builder manifest (keyed by **builder slug**) and the `stoa--reg` row (keyed by seat
`ROLE_slug`) are different registries that **merge later**; Phase-1 only NOTES this and has **no
dependency** on the parallel `stoa--reg` liveness fix. The later merge joins on the **builder/project
slug** (both already carry it) — additive.

---

## 11. THE ONE HELD FORK — isolation UNIT (surfaced UP to Polybius the Grand)

Everything above is converged in-team. This single decision is **not** closed below the Grand, because
it corrects his stated premise.

| | **Branch A — per-builder GCP PROJECT (forced-by-evidence RECOMMENDATION)** | **Branch B — shared project + per-SA scoping (matches Grand's stated premise)** |
|---|---|---|
| Access isolation | ✓ (per-SA scope + per-secret accessor) | ✓ (per-SA scope + per-secret accessor) |
| **Hard per-builder budget cap** | ✓ — only branch that delivers it (project budget + per-service quota) | ✗ — **impossible** (no per-SA budget scope; quotas shared project-wide) |
| Premise impact | **corrects** Grand's SA→PROJECT premise | preserves Grand's stated premise |
| Cost | more projects to create/manage | fewer projects; fails the directive's literal "budget cap per builder" |

**Settled evidence forcing the fork:** §6 (STRABO-cited, VERA-confirmed). **Team recommendation:**
Branch A — it is the only branch satisfying the directive's per-builder budget-cap requirement.
**Decision owner:** Polybius the Grand (premise-correction). **Route:** CO-DESIGN CONVERGED package →
FM independent re-confirm → Polybius_the_Stoa → Grand's gate.

---

## 12. Ownership map — who owns each provisioning step

| Step | List owner | Value/execution owner | Note |
|---|---|---|---|
| Manifest authoring | project seat (T2) | — | `{category, delta}` only |
| Resolution | resolver (T1) | **deterministic code, no agent** | pure fn; near-determinism lock |
| GCP project + SA scope | derived = union of scope-bearing entries | PRINCIPAL one-shot / CI via WIF | bijective SA; §6 |
| Railway key set | resolved `railway_var` + secret-backed | secrets-mgr / keyring → service vars | values never touch an agent |
| GCP API enablement | resolved `gcp_api` only | `gcloud services enable` (human/CI) | exactly the resolved APIs |
| Budget boundary | alert + quota + opt-in killswitch | PRINCIPAL sets numbers | unit = held fork (§11) |
| DB extensions | resolved `db_extension` | db-init on builder's own DB | pgvector baseline; PostGIS iff geo |
| Access layer | fixed T1 scaffold | cookie-cutter | SHAPE only; CONTENT = T3 |

---

## 13. Deferred / open (named, not silently dropped)

- **Category-vs-delta graduation rule** — a `(kind,name)` in **2+ builders' deltas** ⇒ promote to a
  template/category via arc (DAEDALUS to ratify).
- **Multi-category builders** — model assumes one `category` per manifest; a geo+doc builder is **not
  yet supported** (would need a category list or richer delta). Out of Phase-1 scope.
- **PostGIS base image** — derived Dockerfile (§7); Phase-2 build concern.
- **`document/data` vs `document-consuming`** — both lenses map them to the same shape; DAEDALUS to
  confirm the template covers "data" or split a 4th category.

---

## 14. DoD coverage (directive §6)

- [x] composable model: baseline / category-template format / delta format / resolution rule / extensibility — §1,§2,§4
- [x] per-builder manifest schema + unambiguous resolution `baseline+category+delta → full set` — §3,§4
- [x] provisioning choreography: per-builder GCP SA scope (isolation), Railway keys, API enablement, budget — §5,§6,§12
- [x] DB-extension parameterization (pgvector baseline + PostGIS toggle) — §7
- [x] first-class agent-access layer (mesh API + CLI skill) with product-layer boundary — §8
- [x] all THREE worked examples expressed + shown to resolve, incl. labstat_bls `+BLS OEWS` on a reused template — §9
- [x] stoa--reg / manifest alignment noted; no liveness-fix dependency — §10
- [~] **isolation UNIT** — settled capability + forced recommendation + fork **surfaced UP to Grand** (not closed in-team) — §11
- [ ] full gauntlet PASS + NOMOS CONFORMANT; FM independent verify; reported up for the Grand's gate — in progress (PLINY driving)

---

## 15. Provenance

Co-designed by **MAJOR_CHIRON_the-stoa** (ownership/boundary lens) + **MAJOR_HAMILTON_the-stoa**
(resolution/choreography lens); unified by CHIRON (single writer). Capability grounding:
CHIRON gsearch + FM gsearch + **STRABO cited primary-docs** (VERA-confirmed). Author: Denson Smith.
