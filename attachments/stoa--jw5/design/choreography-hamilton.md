# u--9s2 Phase-1 — HAMILTON lens: resolution rule + provisioning choreography

**Seat:** MAJOR_HAMILTON_the-stoa (workflow-architect). **Arc:** stoa--jw5 / u--9s2 Phase 1.
**Co-author seam:** MAJOR_CHIRON owns the cast/ownership/isolation-boundary/product-layer lens
(`design/chiron-ownership-model.md`). This artifact is the complementary **choreography /
sequence / mechanism** lens — the resolution *rule*, the ORDER + idempotency + fail-closed of
provisioning, the DB-extension parameterization, and the credential-discipline + bw seam.
**Contract with CHIRON:** I adopt his **`kind` taxonomy (his §2)** as the atomic resolved-entry
type; my provisioning sequence **dispatches on `kind`**. DAEDALUS unifies both into the formal spec.
**Status:** DRAFT for co-design. Convergence items resolved with CHIRON are marked `✓ JOINT`.

---

## 0. One-paragraph frame

A per-builder **manifest** declares `{category, delta}` tersely. A pure **resolution function**
expands it (set-algebra over CHIRON's typed entries) into a **resolved set**. The cookie-cutter
then **EMITS a provisioning spec** — it does not act. A credential-disciplined applier (CI via
WIF, or a human one-shot) executes that spec in an **ordered, idempotent, fail-closed, re-runnable**
sequence that lands the builder **isolated**. The agent-access layer is a fixed scaffold every
builder gets; the manifest never has to ask for it.

```
manifest {category, delta}  ──resolve (pure fn)──▶  resolved set (typed entries, CHIRON §2)
   ──emit──▶  provisioning spec  ──apply (CI/human, credential-discipline)──▶  live isolated builder
```

---

## 1. The resolution rule (unambiguous — DoD §4 item 2)

Resolution operates over **CHIRON's typed entries** (`kind ∈ {gcp_api, gcp_secret, railway_var,
db_extension, thirdparty_rest_key}`, his §2). Baseline, each category template, and a delta are
each a **list of typed entries**. Resolution is pure set-algebra:

```
resolve(manifest) =
    ( ( BASELINE  ∪  CATEGORY_TEMPLATE[manifest.category] )  \  manifest.delta.omit )
                                                              ∪  manifest.delta.add
```

**Entry identity (for set ops):** two entries are the same iff `(kind, name)` match. `omit`
targets `(kind, name)`; `add` introduces a new `(kind, name)`.

**Precedence (deterministic):**
1. union BASELINE with the category template (idempotent — over-declaration is harmless);
2. subtract `omit`;
3. union `add`. **`add` wins over `omit`** — an explicit project-required add is never silently
   removed by a template-derived omit.
4. A `(kind,name)` present in BOTH `add` and `omit` is a **manifest-lint WARNING** (probable
   author error), resolved as **kept** (add-wins), surfaced to the operator — never silently dropped.

**Why set-algebra is the right primitive (load-bearing):** union is idempotent, so a template
may safely re-list a baseline entry with no effect; this is what makes templates composable and
the directive's §1-vs-§3 wording reconcile (see §2). Resolution is a **pure function** — same
manifest ⇒ same resolved set, no environment reads — which is exactly what makes it *testable as
a design* (directive §5.2) and safe to re-run inside the idempotent choreography.

---

## 2. pgvector → BASELINE  (✓ JOINT — DECIDE A, resolved with CHIRON)

```
BASELINE = [ {gcp_api, gemini-embedding}, {gcp_api, gemini-search},
             {railway_var, DATABASE_URL}, {gcp_secret, POSTGRES_PASSWORD},
             {db_extension, pgvector} ]
CATEGORY_TEMPLATE[geospatial]         = [ {gcp_api, google-maps}, {db_extension, postgis} ]
CATEGORY_TEMPLATE[document-consuming] = [ {gcp_api, document-parsing} ]   # pgvector already baseline
CATEGORY_TEMPLATE[document/data]      = [ {gcp_api, document-parsing} ]   # = doc-consuming shape
```

**The catch that resolves it:** CHIRON's own worked example §7.1 (prospector, geospatial) lists
its DB as **"pgvector + PostGIS"** — but his baseline (§6) and the geospatial template both omit
pgvector, so prospector would silently get *no vector store* despite embedding (baseline). The
only consistent fix: **pgvector is baseline** (every builder embeds ⇒ every builder needs the
vector store). Set-union makes the directive §1 "document-consuming = baseline + pgvector"
wording harmless even if a template redundantly re-lists it. CHIRON's prospector example already
*assumes* this; we make it explicit. **Recommendation stands: pgvector ∈ baseline.**

---

## 3. The three worked examples — resolved (the falsification test, DoD §4 item 6)

**prospector** `{category: geospatial, delta: {}}`
```
resolve = BASELINE ∪ [{gcp_api,google-maps},{db_extension,postgis}]
  gcp_api       : gemini-embedding, gemini-search, google-maps
  gcp_secret    : POSTGRES_PASSWORD ;  railway_var: DATABASE_URL ;  + MAPS_API_KEY (gcp_secret)
  db_extension  : pgvector, postgis
```
✓ "baseline + Maps + PostGIS".

**scienceclaw** `{category: document-consuming, delta: {}}`
```
resolve = BASELINE ∪ [{gcp_api,document-parsing}]
  gcp_api       : gemini-embedding, gemini-search, document-parsing
  db_extension  : pgvector
```
✓ "baseline + pgvector + document-parsing".

**labstat_bls** `{category: document/data, delta: {add: [{thirdparty_rest_key, BLS_OEWS_API_KEY}]}}`
```
resolve = (BASELINE ∪ [{gcp_api,document-parsing}]) ∪ [{thirdparty_rest_key, BLS_OEWS_API_KEY}]
  gcp_api       : gemini-embedding, gemini-search, document-parsing   ← BLS adds NO gcp_api
  db_extension  : pgvector
  thirdparty_rest_key : BLS_OEWS_API_KEY   → store as secret + inject as Railway var; no gcloud-enable
```
✓ **The load-bearing test.** `BLS_OEWS_API_KEY` rides the *reused* template as one delta entry —
a key **no other builder needs** — **without bloating the template**. Because its `kind` is
`thirdparty_rest_key`, the provisioning sequence (§4) **skips GCP API enablement** for it
natively — a naive "enable every resolved API" provisioner would try `gcloud services enable
bls-oews` and fail. CHIRON's taxonomy makes the dispatch correct; my sequence honors it.

---

## 4. The provisioning choreography — EMITTED spec, then applied (DoD §4 item 3)

The cookie-cutter **emits a provisioning spec** (CHIRON §3/§10b): the exact, minimal per-builder
list of {SA + scope, APIs to enable, secrets to create, Railway vars, DB extensions, budget
boundary}. A **credential-disciplined applier** (CI via WIF, or a human one-shot) executes it.
**Agents never hold credential values** — the spec names slots, not values. The sequence below is
the ORDER + idempotency + fail-closed contract the applier follows; **every step dispatches on
the resolved entry's `kind`.**

> **ISOLATION-UNIT HELD ABOVE THE TEAM (FM relay of Polybius_the_Stoa, idx 17/18).** The
> no-per-SA-cap finding *corrects a premise from Polybius the Grand* (his per-builder-SA +
> budget-cap implied shared-project + per-SA scoping). So S0 below is written to the
> **forced-by-evidence RECOMMENDATION** (per-builder project), but the isolation UNIT is **NOT a
> team-closed lock** — it is a surfaced FORK for the Grand (see §5/§8). The sequence is the same
> shape either way; only S0a's boundary granularity changes.

```
S0  ISOLATION SCAFFOLD  (must precede any key materialization)
    0a  ensure builder's ISOLATION BOUNDARY:
          RECOMMENDED (forced by §5 evidence): a per-builder GCP PROJECT (the only unit that
          carries a budget cap; GCP has no per-SA budget scope).
          FORK held for the Grand: shared-project + per-SA scoping — viable ONLY if the Grand
          relaxes the budget-cap requirement (it CANNOT deliver a per-builder cap; §5).
    0b  ensure SA  sa-<builder-slug>@<boundary>.iam   (CHIRON §4 bijective identity: 1 SA ⟷ 1 builder)
    0c  set the BUDGET boundary  (per §5: project-budget alert + per-service quotas as the real-time
        hard cap + opt-in kill-switch — NOT a single native hard "cap" knob; pending STRABO confirm)

S1  GCP API ENABLEMENT          dispatch: kind == gcp_api
    for each gcp_api entry:  gcloud services enable <api>   (idempotent no-op if already on)
    + grant sa-<builder> the API's invoke/use role          (scope-bearing → feeds §6 SA scope)
    fail-closed: an enable failure ABORTS the spec; never proceed to S3 serving with a missing API.

S2  SECRET SLOT MATERIALIZATION dispatch: kind ∈ {gcp_secret, thirdparty_rest_key}
    2a  ensure a secret SLOT (Secret Manager for CI-mediated; OS keyring for keyring-local deploy)
    2b  grant sa-<builder> secretAccessor on JUST that secret  (per-secret least-privilege; CHIRON §4.4)
    2c  VALUE population = a HUMAN / credential-discipline step (generated via keyring_generate;
        minted keys — Maps/BLS/gsearch — pasted by the human). The cookie-cutter NEVER embeds a value.
        This is the human GATE in the bw seam (§7) — provision BLOCKS here until slots are populated.
    NOTE: thirdparty_rest_key has NO S1 step (no GCP API) — it is secret-only. (labstat_bls proof.)

S3  RAILWAY PROVISIONING        dispatch: kind == railway_var  (+ secret-backed entries as vars)
    3a  ensure Railway project + `db` service (baked-init image; §6 selects the image by db_extension set)
    3b  ensure Railway `serving` service (the trigger + serving face; newswire entrypoint base)
    3c  set Railway service vars = resolved railway_var slots + the secret-slot names, via STDIN only
        (railway-keyring-deploy) + EXPECTED_DB, <BUILDER>_OPERATORS, TS_AUTHKEY, and the SA-key-b64
        for THIS builder ONLY  (isolation: never another builder's SA key)
    3d  attach the persistent volume at /var/lib/tailscale  (stable mesh identity; newswire §6.7)

S4  DB EXTENSION APPLICATION    dispatch: kind == db_extension
    baked-init emits exactly the resolved CREATE EXTENSION lines (vector always; postgis iff resolved) — §6

S5  AGENT-ACCESS LAYER  (FIXED T1 scaffold — every builder gets it; NOT manifest-resolved)
    5a  deploy the mesh endpoints: POST /run (fixed pipeline) + /query (read-only)
    5b  tailscale serve --https=443 → 0600 unix socket; deny-by-default policy; <BUILDER>_OPERATORS allowlist
    5c  emit the per-builder CLI client skill `<builder>-trigger` (template-gen from newswire-trigger)
        → ~/.claude/skills/        ── SHAPE only; the project seat fills CONTENT (CHIRON §5 product seam)

S6  VERIFY  (idempotent re-run = a no-op + a health probe)
    preflight the /run door; assert each resolved gcp_api enabled; assert each resolved db_extension present;
    assert no secret slot is unpopulated (else report BLOCKED-on-human, do not declare live).
```

**Properties (DoD §4 item 3 "ordering + fail-closed"):**
- **Ordered:** isolation (S0) before any key (S2) before any serving (S3/S5) — a builder can
  never serve before its isolation boundary + budget exist.
- **Idempotent / re-runnable:** every step is create-or-get; re-running converges the live state
  to the resolved set (change the manifest, re-run, the diff applies). A re-run cannot widen scope.
- **Fail-closed:** any step failure ABORTS the remaining spec rather than proceeding partially; a
  half-provisioned builder never reaches S5 serving. The human secret gate (S2c) is a *block*, not
  an improvised value.
- **Isolation invariant (CHIRON §4, sequenced):** S0 creates the per-builder project+SA first; S3c
  injects only this builder's SA key; S2b binds secretAccessor per-secret. SA scope (§6) is the
  mechanical union of scope-bearing resolved entries — never hand-written, never cross-builder.

---

## 5. The budget cap — capability SETTLED (STRABO), isolation-UNIT HELD for the Grand

**The capability is settled** (STRABO + VERA independent current-docs verification, primary
cloud.google.com pages, 2026-06-25):
1. **No per-SA spend cap exists.** Budgets scope to billing-account / org / folder / **project** /
   service / resource-label — never an SA; an SA's spend bills to its **project**.
2. **No GA hard-DOLLAR cap exists at ANY granularity.** Classic Cloud Billing budgets are
   **alerting-only** (docs verbatim: *"Setting a budget does not automatically cap … usage or
   spending."*). A native auto-pause **Spend Caps** feature exists but is **Private Preview,
   service-limited (Vertex/Maps/CloudRun), not GA**. Per-service **quotas** are real-time but cap
   **rate/requests, not dollars**. (Full menu in the note + mechanism below.)
3. **A hard per-builder budget boundary ⇒ one GCP project per builder** (project = finest scope any
   dollar control binds to). The kill-switch (budget → Pub/Sub → Cloud Function → detach-billing) is
   **reactive/lagging** ("may take several hours"), **not** a hard cap.

**ISOLATION-UNIT decision is HELD ABOVE THE TEAM (FM relay of Polybius_the_Stoa, idx 17/18).** The
finding *corrects a premise from Polybius the Grand* (his per-builder-SA + budget-cap implied
shared-project + per-SA scoping). So this section **illuminates + recommends**, it does **not**
close the lock:
- **Forced-by-evidence RECOMMENDATION:** per-builder GCP **project** as the isolation unit (the
  only shape that carries a budget cap at all).
- **The FORK routed UP to the Grand:** per-builder-project *vs* shared-project + per-SA — the
  latter viable **only if** the Grand relaxes the per-builder budget-cap requirement (it cannot
  deliver one). Real cost/quota implications either way.

> **Native-spend-cap discrepancy — RESOLVED toward alert-only, one residual sub-question open.**
> **Updated to VERA's settled verdict (idx 27) + FM honest-precision (idx 29).** VERA re-fetched
> the primary docs: classic Cloud Billing budgets ARE alert-only (my read held on that span), BUT
> a native auto-pause **Spend Caps** feature DOES exist (GCP Next Apr-2026, **Private Preview**,
> service-limited to Vertex/Maps/CloudRun, canonical docs page 404s) — so my earlier absolute "no
> native auto-cap at any scope" was an overreach; CHIRON's discrepancy was real. The architecture
> conclusion (per-builder project) **stands** (Spend Caps is itself project-level). I also retract
> my earlier labeling of per-service **quota** as a dollar "hard cap": VERA confirms quotas are
> **request/rate limits, not dollar caps** — they bound spend **velocity, not total**.

**The budget MECHANISM (sound design — FM-affirmed; carries forward as the realization UNDER the
per-builder-project branch; NOT itself a premise correction). The honest truth: there is NO GA
hard-DOLLAR cap at any granularity — per-builder-project delivers a MENU, not a single cap:**
- **(a) per-project budget ALERT** — GA, but **alerting-only** (does not stop spend); always set.
- **(b) native auto-pause Spend Caps** — a true auto-pause, but **PRIVATE PREVIEW, service-limited**
  (Vertex/Maps/CloudRun), **not GA** → a *preview dependency*, not something to rely on yet.
- **(c) opt-in kill-switch** — budget → Pub/Sub → Cloud Function → detach-billing; GA but
  **reactive/lagging** (billing lags hours; detaching kills ALL project resources) — the GA
  fallback, not a hard cap.
- **(d) per-service QUOTA limits** — GA and real-time, but **rate/request caps, NOT dollar caps**:
  they bound spend *velocity* (e.g. cap the Vertex embedding request/token rate), which contains a
  runaway burn but does not cap total dollars. The load-bearing *velocity* protection.

The spec's "budget boundary" (S0c) = (a) always + (d) on cost-dominant APIs + (c) opt-in + (b) when
it reaches GA. This is the web-verify-tooling-premises discipline applied twice: the directive's
word "budget cap" has **no GA hard-dollar realization** — it maps to this alert/velocity/reactive
menu, with the only auto-pause being a Preview dependency. (FM owns this honest-precision in the
convergence package going UP to the Grand; my mechanism is unchanged, only the labeling is corrected.)

---

## 6. DB-extension parameterization (DoD §4 item 4)

The resolved `db_extension` set parameterizes the `db` service:
- `pgvector` (`CREATE EXTENSION vector`) — **baseline, always emitted** (backs the universal
  embedding store). The newswire base image (`timescaledb-ha:pg18`) bundles pgvector.
- `postgis` (`CREATE EXTENSION postgis; postgis_topology`) — emitted **iff** `postgis` ∈ resolved
  set (geo-builders). Same shape as the parameterized API set: a resolved entry drives a concrete action.

**Image-selection consequence (▶ DECIDE C — flagging, overlaps the build artifact):** PostGIS is
not in the timescaledb-ha bundle, so a geo-builder needs a **postgis-capable base image** (a 2-line
derived `Dockerfile FROM timescaledb-ha:pg18` + PostGIS install). So the base image itself is
parameterized by `postgis ∈ resolved_set`: geo → postgis-capable image; non-geo → the stock
pgvector image. **Recommend the small derived-Dockerfile** (keeps the timescaledb stack; adds
PostGIS only for geo). Flagged because it touches the build artifact a later Phase-2 arc produces.

---

## 7. The bw seam — credential-discipline integration + durable coordination (my distinctive value)

A dynamic-workflow script cannot run `bw`/`git` itself (workflow-composer: the launching seat
lands the verdict). The cookie-cutter likewise **emits** rather than acts. So the seams are explicit:

- **Credential-discipline seam:** the spec declares **WHAT** keys exist + **WHERE** they live
  (Secret Manager slot for CI-mediated; OS keyring entry for keyring-local) and **never a value**.
  CI (WIF, bounded 1-hour creds) or a human one-shot applies; the agent/cookie-cutter holds nothing.
  (Refs: `credential-discipline`, `railway-keyring-deploy`, `zeotek_newswire/SECURITY.md`, u--eq6,
  `newswire-builder-setup` §7.)
- **bw coordination seam:** resolution + the apply return **structured output** (the resolved set;
  per-step verdict: enabled/created, which slots await human values). The **launching seat** turns
  that verdict into a bw ticket update / dependency close / escalation comment. The work graph:
  ```
  manifest-authored ─blocks─▶ resolve ─blocks─▶ emit-spec ─blocks─▶ apply ─blocks─▶ verify ─blocks─▶ live
                                                                       │
                                              HUMAN GATE: secret-value population (S2c)
                                              = a first-class bw dependency that holds `apply`
                                                open until slots are populated — the safe-degrade point.
  ```
- **stoa--reg alignment (noted, no dependency):** the per-builder manifest (keyed by builder slug)
  and the `stoa--reg` row (keyed by seat `ROLE_slug`) are different registries that **merge later**;
  Phase-1 only NOTES this and has **no dependency** on the parallel stoa--reg liveness fix. CHIRON
  §8 names the join key (builder/project slug) — the later merge is additive.

---

## 8. Decision points (consolidated)

| ▶ | Decision | Status |
|---|---|---|
| A | pgvector baseline vs template member | **JOINT-CLOSED (in-team) — baseline.** A within-model correctness fix (CHIRON's §7.1 prospector would resolve with no vector store otherwise); aligns with directive §3. §2 here. |
| B | isolation UNIT (per-builder project vs shared-project + per-SA) | **HELD FORK — routed UP to the Grand, NOT team-closed** (corrects Grand's stated per-SA premise; FM relay idx 17/18). Capability SETTLED by STRABO (no per-SA cap; alert-only). Recommendation: per-builder project. Budget *mechanism* (alert + per-service quota + opt-in killswitch) carries forward under that branch. §5. |
| C | postgis base-image selection | **carried as Phase-2 NOTE — recommend derived Dockerfile for geo** (§6; CHIRON ACK idx 20). |

## 9. DoD coverage (my half — DoD §4)

- [x] resolution rule pure + unambiguous + precedence (add-wins; lint warning) — §1
- [x] resolution exercised vs all three worked examples incl. the labstat_bls delta — §3
- [x] provisioning choreography S0–S6: ordered, idempotent, re-runnable, fail-closed, isolated — §4
- [x] per-builder SA scope = mechanical union of scope-bearing entries; budget boundary tool-grounded — §4,§5
- [x] DB-extension parameterization in-sequence (pgvector baseline + PostGIS toggle) — §6
- [x] credential-discipline integration (declare WHAT/WHERE, never values; emit-then-apply) — §4,§7
- [x] agent-access layer sequenced as a fixed scaffold step; product-layer seam deferred to CHIRON — §4 S5
- [x] stoa--reg alignment noted, no liveness-fix dependency — §7
- [ ] CHIRON folds these sections into the unified `design-codesign.md` (he is single writer)
- [ ] gauntlet hardening (DAEDALUS formalize → ARGUS → ADA/VERA exercise resolution → CATO → NOMOS)
