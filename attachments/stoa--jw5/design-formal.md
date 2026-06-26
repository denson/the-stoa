---
author: Denson Smith
ticket: stoa--jw5 (u--9s2 Phase-1)
seat: CAPTAIN_DAEDALUS_the_stoa (ARCHITECT)
formalizes: agents/design/stoa--jw5/design-codesign.md (CHIRON+HAMILTON CO-DESIGN CONVERGED)
grounding: agents/design/stoa--jw5/strabo-gcp-budget-cap.md + vera-strabo-citations-verdict.md
status: FORMAL — Phase-1 buildable spec; gauntlet-facing
as_of: 2026-06-25
---

# u--9s2 Phase-1 — FORMAL SPEC: composable key-provisioning model + per-builder manifest

This is the **buildable formalization** of the CHIRON+HAMILTON converged co-design. It does not
redesign; it tightens every contract to the point where the Phase-2 build arc can implement
`resolve()` and the choreography verbatim, and where ADA/VERA can probe the worked examples
machine-checkably. **It provisions nothing.** The one decision that was HELD OPEN for Polybius the
Grand — the isolation UNIT (§5.B / §11) — has been **RESOLVED at the Grand's pre-build gate
(2026-06-26): Branch A (per-builder GCP PROJECT), enforced by a per-builder PREPAID CARD + billing
account (the card = hard cap).** That gate outcome is recorded throughout (§11 / §5.B / §12.B /
§12.B.1 / §12.D); M5 is consequently MOOT.

## 0. Problem restatement (pre-work gate)

Design a composable model that tells the PRINCIPAL **exactly which keys / GCP APIs / DB-extensions
to provision per builder**, because that set differs per project and a blind newswire-template copy
provisions the wrong set. The model is a **per-builder manifest** (`{category, delta}`) plus a
**pure resolution function** (`resolve`) that expands it to a typed **resolved set**, plus an
**ordered/idempotent/fail-closed provisioning choreography** that lands each builder **isolated**.
The deliverable is a *design*; provisioning happens later, after the Grand's gate.

**Imported assumptions** (named per §6.1 — these are scope I am making explicit, not inventing):
1. *One category per manifest.* The directive and both lenses assume exactly one `category`;
   multi-category builders are out of Phase-1 scope (§9, WP-3).
2. *`document/data` ≡ `document-consuming` template shape.* The converged doc maps both to
   `[{gcp_api, document-parsing}]`; I formalize them as **one template under an alias** and flag the
   split decision to ARGUS rather than minting a 4th category unilaterally (§9, WP-4).
3. *Resolution is the only testable-as-design surface.* Choreography steps are specified but not
   executed in Phase-1; only `resolve()` over the §8 worked examples is machine-checkable now.

---

## 1. The manifest schema (DoD item 1)

### 1.1 Exact YAML schema

```yaml
# per-builder manifest — exactly one file per builder
builder: <string>          # REQUIRED. builder slug; join key to stoa--reg (§9); = SA/project/skill slug.
                           #   pattern: ^[a-z][a-z0-9_]*$   (lowercase, digits, underscore; leading alpha)
category: <string>         # REQUIRED. exactly ONE category name; MUST exist in the T1 category library (§3.2).
                           #   unknown category name => resolution ERROR (fail-closed, §2.4).
delta:                     # OPTIONAL. terse per-builder add/omit. absent OR empty => no delta.
  add:  [ <entry>, ... ]   # OPTIONAL list of entries this builder REQUIRES beyond its category. default [].
  omit: [ <entry>, ... ]   # OPTIONAL list of standard entries this builder DROPS. default [].
```

### 1.2 The `entry` shape (the atomic unit — §3 taxonomy gives the `kind` enum)

```yaml
# <entry>
{ kind: <kind-enum>, name: <string> }
# kind  REQUIRED. one of: gcp_api | gcp_secret | railway_var | db_extension | thirdparty_rest_key  (§3)
# name  REQUIRED. the entry's identifier within its kind. pattern: ^[A-Za-z0-9._-]+$
#       (e.g. gemini-embedding, POSTGRES_PASSWORD, BLS_OEWS_API_KEY, pgvector)
```

### 1.3 Schema rules (formal, validation-gate)

- `builder`, `category` REQUIRED and non-empty; type `string`.
- `delta` OPTIONAL; if present, `add`/`omit` are OPTIONAL lists, each defaulting to `[]`.
- Every list member MUST be a 2-key map `{kind, name}` — no extra keys (strict; extra key =
  validation ERROR, prevents silent typo'd fields).
- `kind` MUST be a member of the §3 enum; an out-of-enum `kind` = validation ERROR.
- Terseness invariant: a no-delta builder is two meaningful lines (`builder:` + `category:`); `delta`
  may be omitted entirely.

**Terms:** `BASELINE` = the fixed baseline entry set (§3.1). `CATEGORY[c]` = the entry list of
category `c` from the library (§3.2). `delta.add` / `delta.omit` = the manifest's two entry lists.

---

## 2. The resolution rule (the testable core — DoD item 2)

### 2.1 Definition

```
resolve(manifest) =
    ( ( BASELINE  ∪  CATEGORY[manifest.category] )  \  manifest.delta.omit )  ∪  manifest.delta.add
```

### 2.2 Entry identity

Two entries are **equal** iff **`(kind, name)` are both equal**. All set operations (`∪`, `\`) use
this identity. `name` comparison is **case-sensitive** and exact (no normalization) — the schema
`name` pattern is the only constraint. (Phase-2 note: emit a validation WARNING on two entries that
differ only by `name` case, e.g. `pgvector` vs `PGVector`, as a probable author typo — NOT auto-folded.)

### 2.3 Deterministic precedence (implement verbatim)

The operation order is fixed and total:

```
0.  GUARD: if any delta.omit (kind,name) ∈ NON-OMITTABLE BASELINE set (§2.6)
              raise BaselineOmitError   # §2.4, fail-closed — omit may ONLY target category-template entries
1.  S  := BASELINE  ∪  CATEGORY[category]      # union of baseline and the one category template
2.  S  := S  \  delta.omit                      # subtract omits (by (kind,name) identity)
3.  S  := S  ∪  delta.add                       # union adds
4.  return S
```

- **add-wins over omit.** Because `add` is applied (step 3) **after** `omit` (step 2), any
  `(kind,name)` appearing in BOTH `delta.add` and `delta.omit` ends up **KEPT**. An explicit
  project-required add is never silently removed by a stray omit.
- **Determinism / purity.** `resolve` reads **no environment** (no GCP, no network, no clock, no
  filesystem beyond the immutable BASELINE + category library it is given). Same `(manifest, BASELINE,
  library)` ⇒ byte-identical resolved set. The returned set's iteration order, where an
  implementation needs one, MUST be deterministic — sort by `(kind, name)` ascending — so emitted
  specs and test fixtures are stable.

### 2.4 Error and lint conditions (fail-closed)

| Condition | Class | Behavior |
|---|---|---|
| `category` not in library | **ERROR** | `resolve` raises; provisioning aborts (fail-closed). No partial set. |
| entry `kind` not in §3 enum | **ERROR** (schema, §1.3) | reject manifest before resolution. |
| `delta.omit` names a `(kind,name)` ∈ the **NON-OMITTABLE BASELINE set** (§2.6) | **ERROR** (`BaselineOmitError`) | `resolve` raises; provisioning aborts (fail-closed). `omit` may ONLY target category-template entries; targeting a baseline entry is a HARD ERROR — **not** a silent drop, **not** a warning. This is the WP-6 fix (the only former fail-OPEN path). |
| same `(kind,name)` in BOTH `add` and `omit` | **WARNING (lint)** | resolved as **KEPT** (add-wins, §2.3); surfaced to the author; never silently dropped. |
| `delta.omit` names a `(kind,name)` not in `BASELINE ∪ CATEGORY` (and not in the baseline set) | **WARNING (lint)** | no-op subtract; surfaced as "omit had no effect" (probable stale/typo'd omit). |
| `delta.add` duplicates a `(kind,name)` already in `BASELINE ∪ CATEGORY` | **INFO (lint)** | harmless (set-union idempotent); surfaced as "redundant add". |

The **`BaselineOmitError`** check (row 3) is evaluated **before** the omit subtraction (step 2 of
§2.3): if any `delta.omit` entry is a member of the non-omittable baseline set (§2.6), resolution
raises and yields **no resolved set** (fail-closed). This is decided purely from the omit list and the
immutable BASELINE record — no per-entry allowlist to maintain; every current and future baseline
entry is protected automatically. WHY fail-closed: a silent drop (the former bug) removed a
load-bearing entry (e.g. `pgvector` → builder embeds but has no vector store → 500s at runtime); a
silent no-op would let the author believe the entry was removed when it wasn't. Rejection forces the
author to fix the manifest, consistent with the S0–S6 fail-closed property.

Resolution NEVER reads outside its three inputs; every above condition is decidable purely from
`(manifest, BASELINE, library)`, preserving §2.3 purity.

### 2.5 Reference pseudocode (implementable verbatim)

```python
def resolve(manifest, BASELINE, LIBRARY):
    cat = manifest["category"]
    if cat not in LIBRARY:
        raise ResolutionError(f"unknown category: {cat}")            # §2.4 ERROR, fail-closed
    delta = manifest.get("delta") or {}
    adds  = [ (e["kind"], e["name"]) for e in delta.get("add",  []) ]
    omits = [ (e["kind"], e["name"]) for e in delta.get("omit", []) ]

    add_set, omit_set = set(adds), set(omits)

    # step 0: GUARD — omit may ONLY target category-template entries (§2.4 / §2.6).
    # Targeting any baseline entry is a HARD ERROR (fail-closed), not a silent drop, not a warning.
    baseline_set = { (e["kind"], e["name"]) for e in BASELINE }     # the NON-OMITTABLE set, §2.6
    illegal = omit_set & baseline_set
    if illegal:                                                     # WP-6 fix (former fail-OPEN path)
        raise BaselineOmitError(
            f"omit targets non-omittable baseline entry/entries: {sorted(illegal)}")

    for ident in (add_set & omit_set):                              # §2.4 WARNING (add-wins)
        warn(f"entry {ident} in both add and omit; kept (add-wins)")

    s = set(baseline_set)                                           # entries as (kind,name) tuples
    s |= { (e["kind"], e["name"]) for e in LIBRARY[cat] }           # step 1: ∪
    s -= omit_set                                                   # step 2: \ omit  (baseline omits already rejected)
    s |= add_set                                                    # step 3: ∪ add
    return sorted(s)                                                # §2.3 deterministic order
```

### 2.6 The NON-OMITTABLE BASELINE set (the WP-6 guard's protected set)

**Definition.** The non-omittable baseline set is **exactly the `(kind, name)` set of the `baseline.yaml`
record (§3.1)** — computed from the immutable BASELINE input, NOT a separately-maintained allowlist.
For the current baseline (§3.1) it is the **5 entries**:

```
(gcp_api,       gemini-embedding)
(gcp_api,       gemini-search)
(railway_var,   DATABASE_URL)
(gcp_secret,    POSTGRES_PASSWORD)
(db_extension,  pgvector)
```

**Rule.** `delta.omit`'s authority is scoped to the **category-template layer only**. A manifest MAY
omit a category-template entry (e.g. a geo builder dropping `postgis`); it MAY NOT omit any baseline
entry. Any `delta.omit` (kind,name) ∈ this set ⇒ **`BaselineOmitError`**, fail-closed (§2.4, §2.3
step 0). **WHY:** the baseline is the T1 universal floor — *what EVERY deployment needs* (directive §1).
A manifest (T2) shapes the category layer but cannot revoke the universal floor. Because the set is
derived from the baseline record, this generalizes: every **current and future** baseline entry is
automatically non-omittable with no per-entry list to maintain.

---

## 3. The typed-entry taxonomy (DoD item 3)

### 3.1 BASELINE (`baseline.yaml` — fixed T1, never per-builder)

```yaml
baseline:
  - { kind: gcp_api,       name: gemini-embedding }   # every builder embeds
  - { kind: gcp_api,       name: gemini-search }       # gsearch
  - { kind: railway_var,   name: DATABASE_URL }
  - { kind: gcp_secret,    name: POSTGRES_PASSWORD }
  - { kind: db_extension,  name: pgvector }             # DECIDE-A: pgvector is BASELINE (every builder embeds)
```

### 3.2 Category library (`categories/<name>.yaml`)

```yaml
geospatial:
  - { kind: gcp_api,       name: google-maps }
  - { kind: gcp_secret,    name: MAPS_API_KEY }    # runtime-completeness invariant (§3.4): google-maps is API-KEY-bearing
  - { kind: db_extension,  name: postgis }
document-consuming:
  - { kind: gcp_api,       name: document-parsing }     # pgvector already in BASELINE; not re-listed
# 'document/data' is an ALIAS of document-consuming (same shape) — §9 WP-4 flags the split decision.
document/data:
  - { kind: gcp_api,       name: document-parsing }
```

### 3.3 The `kind` enum (each kind IS its provisioning recipe)

| `kind` | Example | Provisioning path (the recipe) | scope-bearing | `gcloud enable` |
|---|---|---|---|---|
| `gcp_api` | gemini-embedding, gemini-search, google-maps, document-parsing | enable API + grant SA the API role | **yes** (API role) | **yes** |
| `gcp_secret` | POSTGRES_PASSWORD, MAPS_API_KEY | create/version secret; grant SA `secretAccessor` on **just that secret** | **yes** (per-secret) | no |
| `railway_var` | DATABASE_URL, `<BUILDER>_OPERATORS`, TS_AUTHKEY | set as Railway service var (value from secrets-mgr/keyring) | no | no |
| `db_extension` | pgvector (baseline), postgis (geo) | enable extension at db-init (§6) | no | no |
| `thirdparty_rest_key` | BLS_OEWS_API_KEY | store as secret + inject as Railway var; **no GCP API** | **yes** (per-secret) | **no** |

**Load-bearing distinction:** `thirdparty_rest_key` is scope-bearing (it gets a per-secret
accessor) but carries **no `gcloud enable`** — a naïve "enable every resolved API" model wrongly
tries to enable `BLS_OEWS_API_KEY`. The `kind`-dispatch (§4) is what makes labstat_bls correct (§8).

**SA scope is derived, never hand-written:** SA scope = the mechanical union of every scope-bearing
entry in the resolved set (the `gcp_api` API-roles + the `gcp_secret`/`thirdparty_rest_key`
per-secret accessors). §5.A.

### 3.4 The runtime-completeness invariant (FM watch-item, folded; closes WP-7)

**INVARIANT.** Every API the running builder actually CALLS must resolve to **BOTH** halves of what
the call needs at runtime: **(1) enablement** (the `gcp_api` entry → `gcloud services enable` + SA
role) **AND (2) its credential** (the `gcp_secret` entry, when that API authenticates with a minted
key rather than SA-role/ADC). An API that is enabled but whose runtime credential is unresolved is a
**runtime-incomplete** resolved set — the builder enables Maps but has no `MAPS_API_KEY` and 401s at
call time. The typed model's whole point is **one `kind` = one complete deterministic recipe**;
overloading `gcp_api` to "sometimes also mint a key" would reintroduce exactly the non-determinism
the taxonomy exists to kill. Therefore the key is an **explicit paired `gcp_secret` entry** in the
template, never an implicit side effect of the `gcp_api` path.

**Per-API key-bearing classification (web-confirmed 2026-06-25, gsearch + FM environment knowledge):**

| `gcp_api` entry | Runtime auth | Paired `gcp_secret`? |
|---|---|---|
| `gemini-embedding`, `gemini-search` | **Vertex AI + ADC / SA-role** (gsearch cut over to Vertex+ADC 2026-06-13 in this env) | **no** (no minted key) |
| `document-parsing` (Document AI) | **SA-role / ADC** | **no** (no minted key) |
| `google-maps` (Maps Platform) | **API key** (client-facing; SA/OAuth not the standard path) | **YES → `MAPS_API_KEY`** |

So in the **current** templates the invariant adds exactly **ONE** paired secret — `MAPS_API_KEY`
under `geospatial` (§3.2). The **general rule** future-proofs the next key-bearing API: when a new
`gcp_api` entry authenticates with a minted key, it ships its paired `gcp_secret` in the same
template/baseline record. **Phase-2 verify (S6):** the key-bearing signal is **in-band** — an API is
key-bearing iff its template declares a paired `(gcp_api, gcp_secret)` entry in the same record
(§3.2, the `google-maps`+`MAPS_API_KEY` pairing). S6 reads that template-declared pairing (NOT an
implied verifier-side table) and asserts the paired `gcp_secret` is resolved + populated —
runtime-completeness is a checkable property of the resolved set against its own templates.

---

## 4. The provisioning choreography — emit-then-apply (DoD item 4)

The cookie-cutter **EMITS a provisioning spec** (the exact minimal per-builder list: SA + derived
scope, APIs, secret slots, Railway vars, DB extensions, budget boundary). A **credential-disciplined
applier** (CI via WIF, or a human one-shot) executes it. **Agents never hold credential values** —
the spec names *slots*, not values (credential-discipline / railway-keyring-deploy). Every step
**dispatches on the resolved entry's `kind`** (§3.3).

> Credential-discipline (load-bearing, §6.6): no key value ever passes through an agent. The emit
> step produces a value-free spec (slot names only). The apply step is CI-via-WIF (no static key) or
> a human one-shot from the local keyring; Railway vars are set via STDIN, never argv/logs.

Each step below is formalized as **inputs → outputs → failure mode**.

### S0 — ISOLATION SCAFFOLD (the per-builder LOCK; precedes any key materialization)

| | |
|---|---|
| **inputs** | builder slug; the chosen isolation UNIT (§5.B HELD FORK — Branch A or B) |
| **0a** | ensure builder's GCP **project** (Branch A) OR target the shared project (Branch B). `inputs`: slug; `outputs`: project id. |
| **0b** | ensure SA `sa-<slug>@<project>.iam` — **bijective: exactly one SA ⟷ one builder**. `outputs`: SA principal. |
| **0c** | set the BUDGET boundary (§5.B menu: project budget ALERT + per-service rate-QUOTAs + opt-in reactive killswitch + Spend-Caps-if-Preview-available). `outputs`: budget/alert/quota objects. |
| **outputs** | live isolated project+SA shell with budget boundary; **no keys yet**. |
| **failure** | any failure ABORTS the whole spec before any key is materialized (fail-closed). |

### S1 — GCP API ENABLEMENT (`kind == gcp_api`)

| | |
|---|---|
| **inputs** | resolved entries where `kind == gcp_api` |
| **action** | `gcloud services enable <api>` (idempotent) **+ grant SA the API role** |
| **outputs** | each resolved `gcp_api` enabled; SA holds each API role |
| **failure** | an enable failure **ABORTS** the remainder (fail-closed); builder never reaches serving |

### S2 — SECRET SLOT MATERIALIZATION (`kind ∈ {gcp_secret, thirdparty_rest_key}`)

| | |
|---|---|
| **inputs** | resolved entries where `kind ∈ {gcp_secret, thirdparty_rest_key}` |
| **2a** | ensure secret **SLOT** (Secret Manager / OS keyring) — slot only, no value |
| **2b** | grant SA `secretAccessor` on **JUST that secret** (per-secret, not project-wide) |
| **2c** | **VALUE population = HUMAN / credential-discipline GATE.** Provision **BLOCKS** here until every slot is populated. `thirdparty_rest_key` entries have **NO S1 step** (secret-only — the labstat_bls proof). |
| **outputs** | populated secret slots; SA `secretAccessor`-bound per secret |
| **failure** | S2c is a **BLOCK, not an improvised value** — an unpopulated slot reports `BLOCKED-on-human` and halts before serving (fail-closed). |

### S3 — RAILWAY PROVISIONING (`kind == railway_var` + secret-backed entries as vars)

| | |
|---|---|
| **inputs** | resolved `railway_var` entries + secret-backed entries to inject as vars |
| **action** | provision `db` service (baked-init image, §6) + `serving` service (trigger + serving face); set vars **via STDIN only**; inject **this builder's SA-key-b64 ONLY** (never another builder's); mount persistent volume at `/var/lib/tailscale` |
| **outputs** | Railway services live with the resolved var set; this builder's SA key present, no other |
| **failure** | abort on any var-set / service-create failure; no cross-builder key ever injected |

### S4 — DB EXTENSION APPLICATION (`kind == db_extension`)

| | |
|---|---|
| **inputs** | resolved `db_extension` entries |
| **action** | baked-init emits exactly the resolved `CREATE EXTENSION` lines (§6); pgvector always, postgis iff resolved |
| **outputs** | each resolved extension present on the builder's own DB |
| **failure** | a missing required base-image capability (e.g. PostGIS, §6 DECIDE-C) aborts db-init |

### S5 — AGENT-ACCESS LAYER (FIXED T1 scaffold — every builder; NOT manifest-resolved — §7)

| | |
|---|---|
| **inputs** | none from the manifest (fixed scaffold) |
| **action** | stand up the mesh-API scaffold + CLI-client-skill skeleton (§7 SHAPE) |
| **outputs** | a working, secured, domain-empty mesh endpoint + client-skill skeleton |
| **failure** | a half-provisioned builder (any S0–S4 abort) NEVER reaches S5 serving (fail-closed) |

### S6 — VERIFY (idempotent re-run = no-op + health probe)

| | |
|---|---|
| **inputs** | the resolved set + the live builder |
| **action** | door preflight; assert each resolved `gcp_api` enabled; each resolved `db_extension` present; **no secret slot unpopulated** (else report `BLOCKED-on-human`); **runtime-completeness (§3.4): for every `gcp_api` declared key-bearing by its template-declared `(api, secret)` pairing (the §3.2 in-band signal), that paired `gcp_secret` is resolved + populated** |
| **outputs** | PASS (converged to resolved set) or a specific BLOCKED/FAILED report |
| **failure** | report-only; a re-run **converges** to the resolved set and **cannot widen scope** |

**S6 scope-completeness — present, NOT no-extra (r1, honesty).** S6 today asserts the resolved set is
**PRESENT** (each resolved `gcp_api` enabled, each `db_extension` present, each secret slot populated,
runtime-completeness). It does **NOT** assert that **no grant beyond the resolved set survives**. The
**stronger property** — `live-state == resolved-set` with **no extra grants beyond the resolved set**
(i.e. a re-provision after a manifest *removal* prunes the dropped entry's `secretAccessor`/role) — is
the **reconcile/prune-on-removal** property, and is the explicit **Phase-2 builder-lifecycle follow-up**
(§5.A, §10 WP-10, §13). It is deferred because prune is a **destructive op against live IAM** on the
re-provision-after-edit / deprovision surface §13 already defers; Phase-1 is **initial-provision
correctness** (t0), where M1 holds completely.

**Global properties (all steps):** **ordered** (S0 isolation before any S2 key before any S3/S5
serving); **idempotent / re-runnable** (every step create-or-get; a re-run converges and cannot
widen scope on the ADD direction — see the S6 reconcile/prune-on-removal residual for the subtractive
direction); **fail-closed** (any failure aborts the remainder; S2c is a block).

---

## 5. Per-builder isolation (DoD item 5) — settled ACCESS half + HELD BUDGET half

### 5.A Access isolation (team-owned, derived, SETTLED — closed in-team)

- **SA scope = mechanical union of scope-bearing resolved entries** (§3.3). Never hand-written.
- **Bijective SA:** exactly one SA ⟷ one builder; SA name derived from the builder slug.
- **Per-secret accessor:** `secretAccessor` bound per secret, never project-wide.
- **No silent cross-builder path:** builder A's SA can only gain builder B's key by editing A's
  *manifest* (visible, reviewed) or the *resolver itself* (code-review-visible) — never config drift.
  S3 injects only this builder's SA key.

**Scope-as-pure-function-of-the-manifest — qualified to ON INITIAL PROVISION (honesty fix, r1).**
On **initial provision** (t0; Phase-1's scope — the design provisions nothing and every §8.x example
is an initial resolution), the SA's resolved scope is a **pure function of the manifest**: the scope
granted is exactly the mechanical union of the manifest's scope-bearing resolved entries, and a re-run
**cannot widen** scope beyond the resolved set (the ADD direction is total — adding a manifest entry
adds exactly its grant, and an idempotent re-run converges to the resolved set). **This add-direction
claim is unchanged and correct.**

What does NOT hold is the **SUBTRACTIVE** direction across a manifest edit. A re-run **after a manifest
*removal*** converges the ADD direction (it grants nothing new) but does **NOT prune a dropped-entry SA
grant**: if a builder's manifest drops an entry, the previously-granted `secretAccessor`/API-role for
that dropped entry **stands until a reconcile** — S6 (§4) today asserts the resolved set is *present*,
not that *no extra grant beyond the resolved set survives*. So scope is a pure function of the manifest
**only at t0**; after a removal-edit the live IAM is a *superset* of the resolved set until reconcile.
Reconcile/prune-on-removal (S6 asserting live-state == resolved-set, no extra grants) is the named
**Phase-2 builder-lifecycle follow-up** (§10 WP-10, §13) — an accepted Phase-1 simplification, because
prune is a destructive op against live IAM on the re-provision-after-edit / deprovision surface §13
already defers.

### 5.B Budget isolation — RESOLVED at the Grand's pre-build gate (2026-06-26)

Grounded by STRABO (current GCP primary docs, 2026-06-25) + VERA-confirmed verbatim. The two-part
premise-correction was carried UP to Polybius the Grand and **RULED at the pre-build gate** — the
record below is updated to the gate outcome:

**Part 1 — the isolation UNIT (the structural fork) — CLOSED = Branch A.** The finest scope ANY
GCP-native dollar-denominated control binds to is the **PROJECT** (no per-SA budget scope exists), so
a per-builder boundary forces a **per-builder GCP project**. The Grand RULED **Branch A** (§11). The
enforcement refinement: a **per-builder PREPAID CARD + per-builder BILLING ACCOUNT** attaches at the
PROJECT level, so one card+billing-account per builder == one project per builder == Branch A,
**enforced by the card** (card exhausted → that builder's billable usage stops).

**Part 2 — the word "budget CAP" — the hard cap exists OUT-OF-BAND, at the prepaid-card layer.** It
is TRUE that there is **NO GA hard-DOLLAR cap among GCP's native budget features** at any granularity
(per-SA OR per-project) — STRABO-cited, VERA-confirmed. But that finding is **superseded** by the
Grand's ruling: the **per-builder prepaid card IS the hard dollar cap.** The GCP-native menu below is
therefore a **SOFT defense-in-depth layer (early-warning / velocity-bounding / reactive backstop) UNDER
the card's hard cap** — not the cap itself:

| # | Control | GA status | What it actually does |
|---|---|---|---|
| (a) | project budget **ALERT** | GA | notify-only; *"does not automatically cap … usage or spending"* (VERA-verbatim) |
| (b) | **Spend Caps** auto-pause | **PRIVATE PREVIEW**, service-limited (Vertex / Maps / Cloud Run) | pauses API traffic (429/503) at project level; canonical docs page 404s — treat as a **preview dependency**, not a GA guarantee |
| (c) | **kill-switch** (budget→Pub/Sub→Cloud Function→detach billing) | GA | **REACTIVE/lagging** (*"may take several hours"*; *"doesn't guarantee you won't spend more"*; detaching billing kills ALL project resources) — a footnote, not a tier |
| (d) | per-service **QUOTAS** | GA, real-time | **RATE/request limits that bound spend VELOCITY, NOT total dollars** (*"aren't designed to act as a project-wide spending cap"*, VERA-verbatim) |

The Grand ruled on the isolation unit **with this honest menu in front of him**: the hard cap is the
per-builder prepaid card (out-of-band), and the (a)–(d) GCP-native controls are the **soft layer
under it** — (a) alert = early-warning, (c) killswitch = reactive backstop, (d) quota = velocity
bound. This is **NOT** a redesign of the budget mechanism (which already splits alert + quota +
opt-in killswitch and is sound) — it is the precision the convergence package carried, now resolved.
**Branch A is CLOSED (§11); the card is the hard cap.**

---

## 6. DB-extension parameterization (DoD item 6)

The resolved `db_extension` set parameterizes the `db` service:

- **`pgvector`** (`CREATE EXTENSION vector`) — **baseline, always emitted**; bundled in the newswire
  base image (`timescaledb-ha:pg18`).
- **`postgis`** (`CREATE EXTENSION postgis; CREATE EXTENSION postgis_topology`) — emitted **iff**
  `{db_extension, postgis}` ∈ resolved set (geo-builders only). Same shape as the parameterized API
  set: a resolved entry drives a concrete `CREATE EXTENSION`.

**Phase-2-facing note (DECIDE-C, base image).** PostGIS is **not** in the `timescaledb-ha` bundle, so
a geo-builder needs a **postgis-capable base image** — a small derived `Dockerfile FROM
timescaledb-ha:pg18` + PostGIS. The base image is thus parameterized by `postgis ∈ resolved_set`
(geo → postgis image; non-geo → stock pgvector image). **Recommendation:** the derived Dockerfile.
**Flagged for the Phase-2 build arc** (not closed here; this is a Phase-2 decision surface).

---

## 7. The agent-access layer — SHAPE vs CONTENT (DoD item 7)

First-class in the deployable (every builder ships it; the manifest never asks for it). The boundary
is drawn at a clean line:

**T1 — cookie-cutter owns the SHAPE (generic, identical per builder):**
- mesh-API scaffold: `tailscaled` → `tailscale serve --https=443` → a **0600 AF_UNIX socket** →
  the in-mesh trigger;
- identity = the serve-injected `Tailscale-User-Login` header (**never** WhoIs-on-loopback);
- **deny-by-default** policy; the `<BUILDER>_OPERATORS` + `group:operators` allowlist; **Funnel OFF**;
- the **CLI-client-skill template** (`newswire-trigger`-shaped): trigger-over-mesh with **only a
  tailnet identity**, `--check` door-probe, counts-only response, redacted-error tail.

**T3 — project seat owns the CONTENT (specific):**
- which **verbs** the endpoint exposes (newswire `/run` = collect+embed; scienceclaw ingest+search);
- the curated **data**; the domain skill body.

**The clean line (formal boundary):** the cookie-cutter hands the project seat a working, secured,
mesh-reachable endpoint + a client-skill skeleton with **zero domain verbs**; the project seat adds
verbs + data. **The moment a domain verb leaks into T1, the cookie-cutter stops being generic** — that
leak is the boundary-violation test for ARGUS/CATO.

---

## 8. The three worked examples — machine-checkable fixtures (DoD item 8)

Each example below gives the **concrete manifest** and the **EXACT expected resolved set** — every
`(kind, name)` enumerated. These ARE ADA's test fixtures and VERA's probes:
`sorted(resolve(manifest)) == EXPECTED` must hold byte-for-byte (entries sorted `(kind, name)` asc).

### 8.1 prospector — `{category: geospatial, delta: {}}`

```yaml
builder: prospector
category: geospatial
delta: {}
```
**Expected resolved set (8 entries):**
```
(db_extension, pgvector)
(db_extension, postgis)
(gcp_api,      gemini-embedding)
(gcp_api,      gemini-search)
(gcp_api,      google-maps)
(gcp_secret,   MAPS_API_KEY)
(gcp_secret,   POSTGRES_PASSWORD)
(railway_var,  DATABASE_URL)
```
*(8 entries; "baseline + Maps(+its key) + PostGIS". BASELINE 5 + geospatial 3 = 8.)* `MAPS_API_KEY`
is an **explicit paired `gcp_secret` entry** in the geospatial template (§3.2) per the
runtime-completeness invariant (§3.4): `google-maps` is API-key-bearing, so its key resolves as a
first-class entry — NOT an implicit side effect of the `gcp_api` path. **This is the
runtime-completeness probe** (ADA/VERA): the prospector resolved set MUST contain BOTH
`(gcp_api, google-maps)` AND `(gcp_secret, MAPS_API_KEY)`.

### 8.2 scienceclaw — `{category: document-consuming, delta: {}}`

```yaml
builder: scienceclaw         # coordinate Polybius_the_science_stoa (u--4at)
category: document-consuming
delta: {}
```
**Expected resolved set (6 entries):**
```
(db_extension, pgvector)
(gcp_api,      document-parsing)
(gcp_api,      gemini-embedding)
(gcp_api,      gemini-search)
(gcp_secret,   POSTGRES_PASSWORD)
(railway_var,  DATABASE_URL)
```
*(6 entries; "baseline + pgvector + document-parsing". BASELINE 5 + doc 1 = 6.)* "Serves all prospector projects" is a T3
PRODUCT property, NOT a cookie-cutter/manifest property.

### 8.3 labstat_bls — `{category: document/data, delta: {add: [{thirdparty_rest_key, BLS_OEWS_API_KEY}]}}` (the load-bearing test)

```yaml
builder: labstat_bls
category: document/data
delta:
  add:
    - { kind: thirdparty_rest_key, name: BLS_OEWS_API_KEY }
```
**Expected resolved set (7 entries):**
```
(db_extension,        pgvector)
(gcp_api,             document-parsing)
(gcp_api,             gemini-embedding)
(gcp_api,             gemini-search)
(gcp_secret,          POSTGRES_PASSWORD)
(railway_var,         DATABASE_URL)
(thirdparty_rest_key, BLS_OEWS_API_KEY)
```
*(7 entries; BASELINE 5 + doc 1 + delta.add 1 = 7.)* **The falsification test.** `BLS_OEWS_API_KEY` rides the **reused** `document/data`
template as one delta entry — a key no other builder needs — **without bloating the template**. Its
`kind == thirdparty_rest_key` makes the choreography **natively skip S1 API-enablement** (no
`gcloud enable BLS_OEWS_API_KEY`); it gets a secret slot (S2) + a Railway var (S3); only
`sa-labstat_bls` carries its accessor (isolation). **Probe assertions for VERA:**
- (i) the resolved set contains `(thirdparty_rest_key, BLS_OEWS_API_KEY)`;
- (ii) it contains **zero** `gcp_api` entry named `BLS_OEWS_API_KEY` (delta added NO API);
- (iii) the choreography's S1 input list (entries with `kind == gcp_api`) does **not** include it.

This proves **delta ≠ template bloat** and that `kind`-dispatch is correct.

### 8.4 baseline-omit-pgvector — NEGATIVE fixture (the WP-6 regression probe; MUST raise)

This is a **fail-closed** fixture: there is **no** expected resolved set — `resolve` MUST **raise
`BaselineOmitError`** (§2.4 / §2.6). It is the concrete target for ADA's guard test and VERA's
regression probe.

```yaml
builder: badbuilder_pgvector_omit
category: document-consuming
delta:
  omit:
    - { kind: db_extension, name: pgvector }   # attempts to drop a BASELINE entry — illegal
```
**Expected behavior (NOT a resolved set):**
```
resolve(...) RAISES BaselineOmitError
  message names the illegal omit target: (db_extension, pgvector)
  -> NO resolved set returned; provisioning aborts (fail-closed)
```
**Probe assertions for ADA/VERA:**
- (i) `resolve` raises `BaselineOmitError` (named — not a generic exception, not a silent 6-entry set);
- (ii) the raise occurs **before** any set is returned (fail-closed — no partial set);
- (iii) the error message identifies `(db_extension, pgvector)` as the offending non-omittable target.

**Why this fixture is load-bearing:** before the WP-6 fix, this exact manifest resolved SILENTLY to a
6-entry set with `pgvector` dropped — the only fail-OPEN path in the design (builder embeds, has no
vector store, 500s at runtime). The fixture pins the now-correct fail-closed behavior so the
regression cannot reappear. It generalizes: omitting ANY of the 5 §2.6 baseline entries must raise
the same named error.

---

## 9. stoa--reg alignment note (DoD item 9)

The per-builder **manifest** (keyed by **builder slug**) and the `stoa--reg` row (keyed by seat
`ROLE_slug`) are different registries that **merge later**. Phase-1 only NOTES this and has **no
dependency** on the parallel `stoa--reg` liveness fix. The later merge joins on the **builder/project
slug** (both registries already carry it) — additive, no Phase-1 work.

---

## 10. Self-assessed weak points (for ARGUS to pressure-test)

Seeded with the carried items per the brief, plus what I surfaced formalizing. Each names the brittle
assumption + why the design holds this shape anyway.

- **WP-1 — "budget cap" is a menu, not a hard dollar cap.** The directive (§1, §3) and Grand's
  premise say "budget cap." STRABO+VERA establish **no GA hard-dollar cap at any granularity**; the
  realizable control is the (a)–(d) menu (§5.B), of which (d) per-service quotas bound spend
  **VELOCITY, not total dollars**, and (b) Spend Caps is **Private Preview**. *Risk:* the design (or a
  downstream reader) could over-claim "hard cap." *Why this shape:* §5.B states the menu honestly and
  routes the correction UP to the Grand rather than papering it over. **ARGUS: confirm no surviving
  "hard cap" over-claim anywhere in the spec.**

- **WP-2 — category-vs-delta graduation governance.** A `(kind,name)` recurring in **2+ builders'
  deltas** is a signal it should be **promoted** into a category/template via arc (§13 of co-design).
  *Risk:* without enforcement, deltas accrete and templates rot into per-project specials. *Why this
  shape:* Phase-1 states the rule (promote-via-arc) but cannot mechanically enforce it — it is a
  governance discipline, not a resolver feature. **ARGUS: is "promote on 2nd occurrence" the right
  threshold, and who owns detecting it?**

- **WP-3 — multi-category builders not supported.** The model assumes exactly **one** `category` per
  manifest (§1.1, imported assumption 1). A geo+doc builder cannot be expressed without a category
  list or a richer delta. *Risk:* a real builder needing two categories forces an awkward all-delta
  manifest (loses the template-reuse benefit). *Why this shape:* no Phase-1 worked example needs it;
  adding a category list now would complicate `resolve` precedence for a hypothetical. **ARGUS: is
  this safe to defer, or does a near-term builder need it?**

- **WP-4 — `document/data` vs `document-consuming` mapping.** I formalized `document/data` as an
  **alias** of `document-consuming` (same shape, §3.2) rather than mint a 4th category. *Risk:* if
  "data" builders genuinely need a different entry set (e.g. a bulk-load extension, a different
  parser), the alias hides a real divergence. *Why this shape:* both lenses mapped them identically
  and no example distinguishes them; aliasing is reversible (split into a 4th category via arc is
  additive, §2 open-closed). **ARGUS/the Grand: confirm one template covers "data," or direct the
  split.**

- **WP-5 — Spend Caps preview-dependency risk.** Menu item (b) (§5.B) is **Private Preview**, the
  canonical docs page **404s**, and it is **service-limited** (Vertex / Maps / Cloud Run). *Risk:* a
  design that leans on Spend Caps for the dollar-cap story inherits a feature that may not GA, may
  change shape, or may not cover a builder's cost-dominant API. *Why this shape:* §5.B labels it a
  preview dependency explicitly and does NOT make the architecture depend on it (the per-project
  conclusion holds without it, per VERA Probe 4). **ARGUS: confirm the design degrades gracefully if
  Spend Caps never GAs.**

- **WP-6 — resolution-rule edge cases (the baseline-omit fail-OPEN path now CLOSED).** Four named
  edges: **add∩omit** (resolved KEPT, add-wins, §2.3/§2.4); **unknown category name** (ERROR,
  fail-closed, §2.4); **empty/absent delta** (no-op, §1.1 default `[]`); and — the former fail-OPEN
  path ARGUS flagged — **omit of a baseline entry** (e.g. `omit (db_extension, pgvector)`). *Original
  risk:* a manifest COULD omit pgvector and `resolve` silently dropped it (no error, no warning — the
  omit-no-effect warn doesn't fire because the entry IS present), shipping a builder that embeds with
  no vector store → 500s at runtime. The only fail-OPEN path in an otherwise fail-closed design.
  *Resolution (architect-unified, folded):* `delta.omit`'s authority is scoped to category-template
  entries ONLY; omitting any entry in the **non-omittable BASELINE set** (§2.6, the 5 baseline.yaml
  entries) raises **`BaselineOmitError`** (fail-closed, §2.4/§2.3 step 0). The §8.4 negative fixture
  pins the regression. The protected set is derived from the baseline record, so it generalizes to
  every future baseline entry. **ARGUS: confirm the guard fires for ALL 5 baseline entries (not just
  pgvector), that the §8.4 fixture is the right regression target, and that no other resolution edge
  remains fail-OPEN.**

- **WP-7 — runtime-completeness of key-bearing APIs (RESOLVED by §3.4 invariant; ARGUS confirm).**
  *Original risk:* a `gcp_api` entry whose runtime call needs a minted key (e.g. `google-maps`) would
  resolve to one API entry while its `MAPS_API_KEY` lived only in the provisioning path — the resolved
  set would under-represent the secrets and a Maps builder could enable-but-401. *Resolution (FM
  watch-item, folded):* the **runtime-completeness invariant** (§3.4) makes `MAPS_API_KEY` an
  **explicit paired `gcp_secret` entry** in the geospatial template (§3.2, §8.1); web-confirmed that
  Maps is the ONLY key-bearing API in the current set (Vertex-family + Document AI are SA-role/ADC,
  no minted key). *Residual for ARGUS:* (i) web-re-confirm the per-API key-bearing classification in
  §3.4 (do not trust my/FM's table — verify each `gcp_api`); (ii) confirm the GENERAL invariant
  (not just the Maps special-case) is the right future-proofing for the next key-bearing API; (iii)
  confirm the S6-verify runtime-completeness check is well-formed.

- **WP-8 — name-identity case sensitivity.** Entry equality is case-sensitive exact `(kind,name)`
  (§2.2). *Risk:* `pgvector` vs `PGVector` in a hand-authored delta would be treated as two distinct
  entries (a duplicate, not a typo-merge). *Why this shape:* normalization risks collapsing
  legitimately-distinct names; I specified a Phase-2 WARNING on case-only differences instead of
  auto-folding. **ARGUS: is the WARNING sufficient, or should names be lowercased-on-ingest?**

- **WP-9 — Maps-surface granularity (r2; ratify-and-proceed, NAMED Phase-2 follow-up).** The umbrella
  `{gcp_api, google-maps}` entry (§3.2) cannot express **which** Maps surface a builder calls. The
  per-surface truth differs: **Maps-JS = API-key**; server-side **Geocoding-v4 / Places-New / Routes
  = SA-role / ADC** (no minted key). *Risk:* a future server-side-only Maps builder would be
  **over-provisioned** a `MAPS_API_KEY` it never uses. *Why this shape (Phase-1 SAFE):* the
  geospatial template ships `MAPS_API_KEY` as the **conservative default** — worst case over-provision,
  **never under-provision** (the dangerous direction). So Phase-1 is safe and this is **NOT a
  blocker** and **NOT redesigned here**. **Phase-2 follow-up (named):** if a server-side-only Maps
  builder appears, split `google-maps` into per-surface entries so the resolved set drops the unused
  `MAPS_API_KEY`. **ARGUS: this is ratify-and-proceed, recorded as a §10/§13 Phase-2 surface, not a
  Phase-1 fix.**

- **WP-10 — reconcile/prune-on-removal NOT in Phase-1 (r1; NAMED Phase-2 builder-lifecycle follow-up).**
  M1's scope-as-pure-function-of-the-manifest property holds **completely on initial provision** (t0)
  but **only the ADD direction holds across a manifest edit**. A re-provision **after a manifest
  *removal*** does NOT prune the dropped entry's `secretAccessor`/API-role grant — the stale grant
  **stands until a reconcile** (§5.A, §12.A M1 residual). *Risk:* a builder whose manifest drops an
  entry keeps a live IAM grant it no longer needs, so live IAM is a **superset** of the resolved set
  until reconcile (a slow-growing over-grant, not an immediate cross-builder breach — M1's blast-radius
  walls still hold). *Why this shape (Phase-1 SAFE):* Phase-1 is **initial-provision correctness**;
  prune is a **destructive op against live IAM** on the re-provision-after-edit / deprovision surface
  §13 already defers, and is unsafe to land without the deprovision lifecycle. The property owed in
  Phase-2 is **S6 asserting `live-state == resolved-set` with no extra grants beyond the resolved set**
  (the reconcile/prune-on-removal property, §4 S6). **ARGUS: this is ratify-and-proceed, recorded as a
  §10/§13 Phase-2 builder-lifecycle surface, not a Phase-1 fix — conditional on M1 being honestly
  qualified (§5.A / §12.A), which it now is.**

**Empty-list defense:** this list is non-empty and the most load-bearing item (WP-1, the hard-cap
over-claim) is the carried premise-correction the whole gauntlet exists to harden.

---

## 11. THE ONE FORK — isolation UNIT — CLOSED at the Grand's pre-build gate (2026-06-26)

**RESOLVED (Grand pre-build gate ruling, 2026-06-26).** This decision was held UP to Polybius the
Grand because it corrected his stated premise. The Grand ruled at the pre-build gate. The fork is
**CLOSED — Branch A (per-builder GCP PROJECT)**, with a critical refinement on the *enforcement*
mechanism that the team had not had in front of it:

- **Structure:** Branch A — **per-builder GCP PROJECT** is structurally correct (per-SA access scope
  inside a per-builder project boundary), exactly as the team recommended.
- **Spend-cap ENFORCEMENT (the refinement):** the hard spend cap is **NOT** a GCP budget feature. It
  is a **per-builder PREPAID CREDIT CARD + per-builder BILLING ACCOUNT** — a long-standing PRINCIPAL
  decision that had never been recorded durably (which is why the team had to re-litigate it). A GCP
  billing account attaches **at the PROJECT level**, so **one billing-account + prepaid card per
  builder == one GCP project per builder == Branch A's structure, enforced by the card.**
- **The CARD is the hard cap:** when a builder's prepaid card is exhausted, that builder's billable
  usage stops. This is the hard-dollar bound the §5.B menu could not provide on its own.
- **GCP budget alerts / quotas / killswitch = a SOFT early-warning + velocity-bounding layer only**,
  sitting UNDER the card's hard cap (defense-in-depth), not the cap itself.

| | **Branch A — per-builder GCP PROJECT** (RULED — enforced by per-builder prepaid card + billing account) | **Branch B — shared project + per-SA scoping** (rejected) |
|---|---|---|
| Access isolation | ✓ per-SA scope + per-secret accessor | ✓ per-SA scope + per-secret accessor |
| Per-builder hard spend cap | ✓ **per-builder prepaid card + billing account = hard cap** (card exhausted → builder's billable usage stops); GCP budget menu = soft early-warning under it | ✗ a per-builder billing account/card **cannot** attach below the project level — fails the per-builder hard-cap intent |
| Premise impact | corrected Grand's SA→PROJECT premise (Grand affirmed) | preserved the (rejected) premise |
| Cost | more projects + one prepaid card/billing account per builder | fewer projects; fails the per-builder hard-cap intent |

**Decision owner:** Polybius the Grand. **Status:** RESOLVED at the pre-build gate (2026-06-26) — no
longer an open fork. **Route taken:** converged package → FM independent re-confirm →
Polybius_the_Stoa → Grand's gate → **ruled Branch A + per-builder prepaid-card/billing-account
enforcement.** Recorded here as the Grand-gate outcome; this is a documentation fold of the gate
decision, not a design change.

---

## 12. Threat→mitigation map (op-disc §35.4 — A3 author duty)

This section BINDS each already-audited, already-ratified mitigation to its named threat with the
§35.4 triple `M<n> (named threat) → attack-path → how-defeated`. **It introduces NO new mechanism**:
every `how-defeated` cell names a mechanism that already lives in the cited §section (validated by
ARGUS, stage 2/6). The M-IDs + facts are PLINY's A1 ratification-restatement (op-disc §35.2, the bw
beat fired between ARGUS and ADA). DAEDALUS (upstream classifier, §35.1) PROPOSES these
classifications; ARGUS CONFIRMS them at the tight maps-pass — they cannot be self-exempted downstream.

### 12.A Threat-ratified mitigations (the defeated set)

| M | Named threat | attack-path (how realized) | how-defeated (specific mechanism + live §) |
|---|---|---|---|
| **M1** | Per-builder isolation LOCK (cross-builder lateral movement) | a compromised key or over-scoped SA in builder A reads / spends / exfiltrates builder B's secrets, data, or budget | **§5.A** derived SA scope = mechanical union of **scope-bearing resolved entries ONLY** + **bijective 1-SA⟷1-builder** + **per-secret `secretAccessor`** (never project-wide) + **§4 S3** injects only THIS builder's SA key; **Branch-A** per-builder GCP project gives a project-level blast-radius wall (§5.B/§11). **Residual (honesty, r1):** M1 holds **completely on initial provision** (t0; Phase-1's scope) — scope is then a pure function of the manifest and cannot widen. A **re-provision after a manifest *removal*** leaves a **stale `secretAccessor`/grant** for the dropped entry **live until reconcile** (the live IAM becomes a superset of the resolved set; S6 asserts present-not-no-extra). Reconcile/prune-on-removal is a **Phase-2 builder-lifecycle residual** (§5.A, §10 WP-10, §13) — an accepted Phase-1 simplification, NOT overclaimed as defeated here. |
| **M2** | Credential-discipline / agents-never-hold-values (credential VALUE exposure to an agent) | a secret VALUE lands in an agent transcript / argv / disk (a provisioning step echoes a key) → exfiltratable from agent context | **§4 emit-then-apply** (cookie-cutter emits a value-free spec naming SLOTS only; CI-via-WIF or human one-shot applies) + **§4 S2c** human secret-population GATE (BLOCK, not an improvised value) + values via **STDIN / OS keyring / Secret Manager only** (never argv/logs) + **§4 S3** injects only this builder's SA key |
| **M3** | Runtime-completeness invariant (key-bearing API enabled-but-keyless → 401 at runtime) | a key-bearing API surface (Maps) resolves enabled-but-keyless → builder deploys, then 401s at call time (silent under-provision / availability) | **§3.4** runtime-completeness invariant: every app-called key-bearing surface resolves to **BOTH** enablement **AND** a **paired `gcp_secret`**; **§4 S6** verifies the **template-declared `(gcp_api, gcp_secret)` pairing** (the §3.2 in-band signal) is resolved + populated |
| **M4** | Non-omittable baseline / BaselineOmitError (baseline necessity silently omitted → fail-open) | a manifest `delta.omit`s a baseline necessity (pgvector) → silent drop → builder embeds but has no vector store → 500s/no-ops at runtime (the lone fail-OPEN path) | **§2.4** `BaselineOmitError` — HARD, fail-closed (omit may target category-template entries ONLY; omit of any baseline entry raises, not a silent drop, not a warning) + **§2.6** the explicit 5-entry non-omittable baseline set (derived from the baseline record → generalizes to all future baseline entries) + **§8.4** negative fixture `badbuilder_pgvector_omit` proves it raises |
| **M6** | Agent-access mesh security (unauthorized mesh access to a builder's trigger/data) | an unauthorized party reaches a builder's mesh trigger / curated data (no-auth, loopback-WhoIs spoof, or Funnel exposure) | **§7 / §4 S5** T1 scaffold: **0600 AF_UNIX socket** + `tailscale serve` **header-trust identity** (`Tailscale-User-Login`, **never** WhoIs-on-loopback) + **deny-by-default** policy + `<BUILDER>_OPERATORS` + `group:operators` allowlist + **Funnel OFF** |

Each `how-defeated` cell was confirmed present in this spec before this section was written — this is a
binding-and-documentation fold, not a redesign. The threat-coverage probes VERA runs for
M1–M4/M6 exercise these named attack-paths (not the happy path); §8.4 is the executed probe for M4.

### 12.B Named residual risk (honestly surfaced, NOT claimed defeated — op-disc §35.5)

| ID | Named threat | attack-path | best-achievable Phase-1 posture (NOT a hard defeat) |
|---|---|---|---|
| **M5 — MOOT (Grand pre-build gate, 2026-06-26)** | Budget runaway — *was:* "no GA hard-dollar cap exists at any granularity" | a runaway loop or a compromised key in builder A burns unbounded spend before the reactive killswitch trips | **MOOTED:** the hard dollar cap exists **out-of-band** = the **per-builder PREPAID CARD + billing account** (card exhausted → builder's billable usage stops). The "no GA GCP-budget hard cap" finding is TRUE but **superseded** by the card. The per-builder GCP project (Branch A) blast-radius + per-service quota (velocity) + reactive killswitch are now the **SOFT layer UNDER the card** (§5.B menu (a)–(d)), not the cap. |
| **R-1** | M1 stale-grant-until-reconcile (subtractive scope NOT pruned) — r1 | a builder's manifest *drops* an entry; the previously-granted `secretAccessor`/API-role is **NOT pruned** on re-provision and stands until reconcile → live IAM is a **superset** of the resolved set (slow-growing over-grant; M1's blast-radius walls still hold, so not an immediate cross-builder breach) | **M1 holds completely at t0 (initial provision)**; the ADD direction is total; the subtractive prune is the **Phase-2 builder-lifecycle property** (S6 `live-state == resolved-set`, §4 S6 / §5.A / §10 WP-10 / §13). Phase-1 = initial-provision correctness; prune is a destructive live-IAM op on the deferred deprovision surface. |
| **R-2** | Manifest integrity (the manifest DRIVES resolved scope → manifest authorship is an authz-relevant trust boundary) — r2 | a malicious or erroneous edit to a builder's manifest *widens* its resolved scope (adds a scope-bearing entry it should not have) → the resolver faithfully grants the broadened scope, because `resolve` trusts its manifest input by construction (§2.3 purity reads the manifest as given) | **Phase-1 rests on repo / git access-control + project-seat review** of manifest edits (a manifest change is a visible, reviewed diff — §5.A's "no silent cross-builder path" depends on exactly this review). **Phase-2 hardening = manifest-approval governance** (e.g. signed/approved manifests, a manifest-change approval gate). NOT a Phase-1 mechanism. |

**M5 is MOOT (Grand pre-build gate ruling, 2026-06-26).** It is TRUE that no GA hard-dollar cap exists
among GCP's native budget features at per-SA OR per-project granularity (§5.B, STRABO-cited,
VERA-confirmed verbatim) — but the Grand ruled the hard cap exists **out-of-band**: a **per-builder
prepaid card + billing account** (the card is the hard cap). The §35.5 named-residual framing is
therefore retired for M5; the runaway threat is bounded by the card, with the §5.B (a)–(d) GCP-native
controls as the soft early-warning/velocity layer under it.

**R-1 (r1)** and **R-2 (r2)** are likewise **§35.5 named residuals**, surfaced-not-defeated. They are
classified here because each is **authz-relevant** and would otherwise carry NO §35.1 classification:
R-1 because the subtractive scope property is an isolation (M1-adjacent) claim the design must NOT
overclaim; R-2 because the manifest DRIVES resolved scope, so manifest integrity is an authorization
trust boundary. Neither is a defeated `M<n>` — both are accepted Phase-1 simplifications named for the
Grand to gate **with them in view**, exactly as M5 is.

### 12.B.1 Relay-UP residual package (the COMPLETE set carried UP to Polybius the Grand)

This package was carried UP and **gated by the Grand at the pre-build gate (2026-06-26)**. Its status
on the two isolation-unit items is now **RESOLVED**; the two manifest-side residuals **REMAIN** as
Phase-2 residuals. Updated status:

- **DECISION (held fork) — CLOSED (Grand pre-build gate, 2026-06-26):** the isolation-UNIT
  premise-correction is **RESOLVED = Branch A** (per-builder GCP **project**), enforced by a
  **per-builder PREPAID CARD + per-builder BILLING ACCOUNT** (card = hard cap). No longer open.
  §5.B / §11 / §12.D.
- **RESOLVED RESIDUAL:**
  - **M5 — budget runaway: MOOT (Grand pre-build gate).** The "no GA GCP-budget hard cap" finding is
    TRUE but superseded by the per-builder prepaid card (the out-of-band hard cap). §5.B / §12.B.
- **STILL-NAMED RESIDUALS (all §35.5 — surfaced, not defeated — UNCHANGED by the Grand ruling, which
  addressed ONLY the isolation-unit fork + M5):**
  - **R-1 — M1 stale-grant-until-reconcile:** subtractive scope not pruned until a Phase-2 reconcile (§5.A / §12.A / §12.B).
  - **R-2 — manifest integrity:** manifest authorship is an authz-relevant trust boundary; Phase-1 rests on git access-control + project-seat review, Phase-2 hardening = manifest-approval governance (§12.B).
  - **R-3 — catalog integrity:** the §17 service→key catalog is a NEW **fleet-wide single-source-of-truth** that drives EVERY builder's provisioning, so a poisoned/erroneous catalog record is a **fleet-wide over-grant** — a **wider blast radius than R-2** (per-builder manifest integrity). DAEDALUS PROPOSED (§23.4 / §23.3 DWP-4), ARGUS CONFIRMED as a §35.5 named residual. Phase-1 rests on **catalog-authoring discipline at arc time** (T1 arc-review + git access-control, §17.3 / §17.4); Phase-2 hardening = **catalog-integrity governance** (§23.4).

The relay-UP residual set carried UP — now reading the **COMPLETE** set after the Grand's pre-build
gate — is **{ held-fork (RESOLVED — Branch A / prepaid card), M5 (MOOT), R-1 (prune-on-removal), R-2
(manifest-integrity), R-3 (catalog-integrity) }**. **{ held-fork, M5 } are RESOLVED** (fork → Branch A
+ prepaid card; M5 → moot at the Grand gate) and **{ R-1, R-2, R-3 } remain the live Phase-2 named
residuals** (R-3 added per ARGUS's stage-2 confirmation of the discovery addition).

### 12.C Not-threat-ratified classifications (recorded so no security-relevant change carries NO classification — op-disc §35.1)

DAEDALUS PROPOSES `not threat-ratified` for each; ARGUS CONFIRMS (§35.1 — cannot be self-exempted).
Each is an architectural / correctness / process change with **no runtime attack path**:

| Element (live §) | Classification |
|---|---|
| Typed-entry taxonomy as joint contract (§3) | not threat-ratified (architectural change — enabling structure, no runtime attack path) |
| Resolution rule: add-wins / `(kind,name)` identity / purity / determinism (§2) | not threat-ratified (correctness change, no runtime attack path; M4 rides on this rule but the rule itself is not a security mitigation) |
| Access-layer SHAPE/CONTENT boundary (§7) | not threat-ratified (architectural/modularity change; the mesh SECURITY is M6, the boundary line itself is structural) |
| DECIDE-A pgvector→baseline (§3.1) | not threat-ratified (folds into M4 — it is the baseline membership M4 protects, not a separate mitigation) |
| Category extensibility / graduation governance | not threat-ratified (process/governance change, no runtime attack path) |
| stoa--reg alignment note (§9) | not threat-ratified (later-merge process note, no runtime attack path) |

### 12.D Held fork — RATIFIED at the Grand's pre-build gate (2026-06-26)

The §11 isolation-UNIT fork was **NOT swept by the A1 beat** — it was surfaced UP to the Grand and
**RULED at the pre-build gate (2026-06-26)**. The isolation GOAL it serves is **M1 (ratified)**; the
unit CHOICE (Branch A vs B) was **surfaced UP rather than closed in-team**, and the Grand's pre-build
gate ruling **CLOSED it = Branch A** (per-builder GCP project, enforced by per-builder prepaid card +
billing account). This was the **post-A1 ratification** anticipated here — now executed. **The fork
is closed; DAEDALUS has recorded the gate outcome (§11 / §5.B / §12.B / §12.B.1).**

---

## 13. Out of scope (Phase-1 boundary)

- **Building the cookie-cutter skill** — Phase-2 build arc. This is a design.
- **Actually provisioning anything on Railway/GCP** — PRINCIPAL, only after the Grand's gate.
- **The per-builder PRODUCT layer (T3)** — specific verbs + curated data; owned by project seats
  (prospector team; Polybius_the_science_stoa for scienceclaw).
- **The PostGIS base-image Dockerfile** — Phase-2 build concern (DECIDE-C, §6).
- **Multi-category builder support** — deferred (WP-3).
- **The stoa--reg ↔ manifest merge** — later integration step; no Phase-1 dependency (§9).
- **Reconcile / prune-on-removal** — the Phase-2 builder-lifecycle property that S6 assert
  `live-state == resolved-set` with **no extra grants beyond the resolved set**, so a re-provision
  after a manifest *removal* prunes the dropped entry's stale `secretAccessor`/API-role grant (r1,
  WP-10, §5.A, §12.A M1 residual). Deferred: prune is a destructive op against live IAM on the
  re-provision-after-edit / deprovision surface this list already defers; Phase-1 = initial-provision
  correctness (t0). Accepted Phase-1 simplification.
- **Per-surface Maps granularity** — splitting umbrella `{gcp_api, google-maps}` into per-surface
  entries (Maps-JS=key vs server-side Geocoding/Places/Routes=SA/ADC) so a server-side-only Maps
  builder drops the unused `MAPS_API_KEY`. Phase-2 follow-up (WP-9, r2); Phase-1 ships the conservative
  paired-key default (over-provision worst case, never under) so this is deferrable, not a Phase-1 fix.

(NOTE: the non-omittable-baseline enforcement, previously a candidate hardening, is now **specified in
§2.4/§2.6** — the WP-6 fix — and is no longer out of scope.)

**Out of scope — the KEY-DISCOVERY PROCESS addition (Part 2, §16–§23; the Phase-2 implementation):**
- **The catalog DATA** beyond the §22 seed records — Phase-2 (§16.1, §17.5). Phase-1 ships the record
  STRUCTURE + the four seed records the §8 fixtures exercise.
- **The static-scanner implementation** (the §20 V5 drift-detector) — Phase-2 (§16.1, §18.4). Phase-1
  ships the declare-primary + scan-validator MODEL + precedence; scan is fail-closed-advisory, never a
  generation input.
- **The generator code** that runs §19 G1–G4 over a populated catalog — Phase-2 (§16.1, §19.4).
  Phase-1 ships the deterministic algorithm + the §23.1 seed self-run.
- **The runtime observer** (eBPF/OTel production call-detection, §18.1 pillar 3) — Phase-2; the named
  closer for the §23.3 DWP-3 no-import-signal gap.
- **Live-population emergence** — promoting NEW categories via the §21.3 ≥2-builder emergence rule
  needs a live builder population; Phase-1 SEEDS `geospatial` + `document-consuming` (§21.5, §22).

---

# PART 2 — THE KEY-DISCOVERY PROCESS (the UPSTREAM front-end that GENERATES the manifest)

> **Scope of Part 2 (added by the u--9s2 Phase-1 revision — the KEY-MODEL ADDITION, Grand/PRINCIPAL).**
> Sections §16–§23 below formalize the **discovery / generation / validation** front-end that
> **PRODUCES** the `{category, delta}` manifest the Part-1 resolver (§2) consumes. **This is strictly
> UPSTREAM of `resolve()`** (§16.0). Formalized by DAEDALUS from the CHIRON+HAMILTON CO-DESIGN
> CONVERGED unified doc (`agents/design/stoa--jw5/discovery-codesign.md`, with HAMILTON's lens at
> `discovery-choreography-hamilton.md`).
>
> **THE LOAD-BEARING CONSTRAINT (held absolutely; §16.0).** The Part-1 resolver (§2 set-algebra),
> provisioning choreography (§4 S0–S6), the §8 worked-example fixtures (prospector 8 / scienceclaw 6 /
> labstat_bls 7), and the §12.A threat-maps are gauntlet-CONFORMANT + Grand-gated and **STAND
> TEXTUALLY UNCHANGED**. Part 2 only adds a front-end that GENERATES the manifest those Part-1
> mechanisms already validate. The §8 sets (8/6/7) are a **REGRESSION TARGET** Part 2 must still hit,
> never re-derive. **Nothing in Part 2 changes `resolve()` (§2) or the §8 sets** — §23 self-runs the
> three examples through generation and confirms 8/6/7.

## 16. The key-discovery front-end — frame + the upstream constraint (Part-2 §0/§2)

### 16.0 The pipeline + the load-bearing constraint (stated first, held absolutely)

Part 1 took a **hand-authored** `{category, delta}` manifest (§1) as its input. The directive: the
manifest must be **DISCOVERED / GENERATED from what the builder actually CALLS**, not hand-guessed. A
builder that calls Google Maps + a BLS REST API gets those keys because the system **detected the
calls**, not because a human remembered to declare them. Missing a called service = a runtime failure
(the under-provision footgun §3.4 exists to prevent); provisioning an uncalled service = waste + scope
bloat. Discovery makes the manifest a **derived, verifiable** artifact.

The discovery process is a **front-end that PRODUCES** the manifest `resolve()` (§2) consumes:

```
services-called ──discover──▶ catalog lookup ──generate──▶ {category, delta} ──validate──▶
   (§18 declare +              (§17 catalog)    (§19 G1-G4:     (§20 V1-V5:
    scan-validate)                              emergent cat +   fail-closed,
                                                derived delta)   BEFORE S0)
                resolve()  [§2 UNCHANGED]  ──▶  resolved set  ──▶  provision [§4 S0-S6 UNCHANGED]
```

**THE CONSTRAINT (held absolutely).** `resolve()` (§2), provisioning (§4 S0–S6), the §8 fixtures, and
the §12.A threat-maps **stand textually unchanged**. The §8 sets (8/6/7) are a **regression target
Part 2 still hits**, never re-derives. Everything Part 2 adds is **upstream of `resolve()`**: it
produces the same `{category, delta}` shape (§1.1) the resolver already validates; the category stays a
named entry-set the resolver consumes (only its *provenance* changes — §21); the delta stays the same
`{add, omit}` shape; the §2.6 `BaselineOmitError` guard is preserved **by construction** (§17.3). **No
pressure on `resolve()` or the §8 sets arose → no dilemma to classify** (§23.2). If any future reframe
DID pressure them, that is a scope breach → STOP + dilemma-classify to PLINY, never a silent change.

### 16.1 Phase-1 vs Phase-2 boundary (SHAPE only — the implementation is Phase-2)

Part 2 specifies the **SHAPE** of discovery — the catalog STRUCTURE, the generation/validation
CHOREOGRAPHY, and the emergent-templates reframe — so the model is **complete + verifiable** now. The
**IMPLEMENTATION is Phase-2** and is named as such throughout:

| Concern | Phase | Where |
|---|---|---|
| Catalog **structure** (record schema, invariants, tier) | **Phase-1** (this spec) | §17 |
| Catalog **DATA** (the populated service→key records beyond the §22 seed) | **Phase-2** | §17.5 |
| Discovery **choreography** (declare-primary + scan-validator model) | **Phase-1** (this spec) | §18 |
| Static **scanner implementation** (the V5 drift-detector code) | **Phase-2** | §18.4 |
| Generation **algorithm** (G1–G4, deterministic) | **Phase-1** (this spec) | §19 |
| Generation **code** (the generator that runs G1–G4) | **Phase-2** | §19.4 |
| Validation **choreography** (V1–V5, fail-closed, before S0) | **Phase-1** (this spec) | §20 |
| Emergent-templates **reframe** (category = emergent bundle; delta derived) | **Phase-1** (this spec) | §21 |
| Runtime **observer** (eBPF/OTel production confirm) | **Phase-2** | §18.1 pillar (3) |

**Phase-1 = the catalog STRUCTURE + the discovery/generation/validation CHOREOGRAPHY + the reframe.**
The catalog DATA, the scanner, the generator code, and the runtime observer are Phase-2 (§13).

---

## 17. The service→key CATALOG (Part-2 DoD item 1; CHIRON lens)

The **catalog** is the new T1 cookie-cutter asset that maps each external **service** to the typed
credentials it requires. It is the **shared contract** at the discovery seam: it defines the structure
the generation step (§19) reads.

### 17.1 Exact per-service record schema

```yaml
# catalog/<service-id>.yaml  (one record per external service)
- service-id: <stable-id>          # REQUIRED. the key skills DECLARE (§18 `services:` list).
                                   #   pattern: ^[a-z][a-z0-9-]*$
  entries:                          # REQUIRED, 1:N. the SET of typed §1.2/§3 entries this service
                                    #   requires. EACH is an EXISTING design-formal entry
                                    #   { kind, name } with kind ∈ the §3.3 enum
                                    #   (gcp_api | gcp_secret | railway_var | db_extension |
                                    #    thirdparty_rest_key). The catalog introduces NO new kind —
                                    #   it MAPS a service to existing typed entries.
    - { kind: <kind-enum>, name: <NAME> }
    - ...                           #   1:N — one service may require several entries (§17.2)
  gcp_api: <api-id | none>          # OPTIONAL denormalized convenience = the subset of `entries`
                                    #   whose kind == gcp_api (the API to `gcloud services enable`).
                                    #   `none` when the service enables no GCP API (e.g. bls-oews).
  category: <emergent-category-tag | none>   # OPTIONAL. the emergent bundle (§21) this service
                                    #   belongs to; `none` if it is a per-builder special (e.g. bls-oews).
```

### 17.2 Load-bearing structural invariants (the catalog's contract with Part 1)

1. **Every catalog credential is a typed §3 entry (no new kind).** The catalog maps `service → set of
   typed entries`; it adds no entry-kind. So the §19 G1 union (`⋃ entries`) is **well-typed** and flows
   `db_extension` / `gcp_secret` / `thirdparty_rest_key` / `gcp_api` through one generation path.
   Confirms HAMILTON seam-(a).

2. **A service maps to a SET of entries (1:N), not 1:1 — this carries the §3.4 paired-credential rule
   INTO the catalog as a CONSTRUCTION INVARIANT.** One service may require several credentials. The
   `google-maps` record holds BOTH `{gcp_api, google-maps}` AND `{gcp_secret, MAPS_API_KEY}` in the
   same record, so a single declared call to `google-maps` makes G1 pick up **both** —
   **runtime-completeness (§3.4) becomes a catalog-construction invariant**, not a check the generator
   must remember. (Catalog-authoring discipline, enforced at §21-emergence/arc time: adding a
   key-bearing service REQUIRES its paired credential in the same record.) Confirms HAMILTON seam-(c)
   and is the cleaner realization of §3.4 than a separate generator check.

3. **Baseline is NOT in the catalog (the §2.6 guard preserved by construction).** Baseline
   (`gemini-embedding`, `gemini-search`, `DATABASE_URL`, `POSTGRES_PASSWORD`, `pgvector` — §3.1) is
   universal: it is prepended by the unchanged `resolve()` (`BASELINE ∪ …`, §2.1). The catalog covers
   ONLY the **non-baseline, discoverable** services. So discovery determines the **category + delta**
   layer only — **a generated `delta.omit` can NEVER target a baseline entry** (the generator never
   sees baseline as a catalog/category member; §19 G3 omit = `category \ called`), so the §2.6
   `BaselineOmitError` guard is **preserved by construction, not re-checked**.

### 17.3 Tier placement

| Catalog artifact | Tier | Owner | Note |
|---|---|---|---|
| **The CATALOG** (service→typed-entries records) | **T1** | cookie-cutter (substrate) | generic, versioned, reused whole; adding a service = additive arc (§17.4 open-closed) |
| **Emergent category bundles** (§21) | **T1** | cookie-cutter | named entry-sets; membership emerges/promotes via the §21 EMERGENCE rule (arc) |

(The per-skill `services:` declaration is **T3** and the generated `{category, delta}` manifest is
**T2 (derived)** — see §18.3 and §21.4; the catalog itself is T1.)

### 17.4 Additive extensibility (open-closed, unchanged from §3's governance)

Adding a new service = **one additive T1 catalog record** (via arc). The generator (§19), the resolver
(§2), baseline (§3.1), and existing records are **closed for modification** — open only for additive
extension. This is the same open-closed governance the Part-1 category library (§3.2) already carries.

### 17.5 Phase-1 vs Phase-2 (catalog)

**Phase-1 (this spec):** the record SCHEMA (§17.1) + the three invariants (§17.2) + tier (§17.3) +
the §22 SEED records (the four services driving the three worked examples). **Phase-2:** the populated
catalog DATA beyond the seed (every other service the builder population calls). The §22 seed is the
concrete initial state; it is exactly the services the §8 fixtures already exercise.

---

## 18. The DISCOVERY step — DECLARE-primary + SCAN-validator (Part-2 DoD item 2; HAMILTON lens)

### 18.1 The model (web-verified recommendation — NOT asserted from memory)

**Recommendation (HAMILTON, web-verified 2026-06-26 against current docs): explicit DECLARATION is
authoritative; static SCAN is a build-time validator (drift / shadow-API cross-check), not the
generator; a runtime observer is a named Phase-2 layer.**

| Pillar | Binding | Role |
|---|---|---|
| **(1) DECLARE — authoritative** | each skill/component DECLARES `services: [<service-id>, …]` in its `SKILL.md` frontmatter (manifest-source) | the **source of truth** GENERATION (§19) reads |
| **(2) SCAN — validator** | static scan flags any imported SDK / raw HTTP client / known-service reference whose service is **not declared** | a **drift / shadow-API guard** in VALIDATION (§20 V5) — **flags, never silently adds** |
| **(3) RUNTIME observe — Phase-2** | eBPF / OTel detect actual outbound calls in the deployed builder | **named Phase-2** confirm-in-production; out of Phase-1 scope |

### 18.2 Why scan cannot be the source of truth (the web-verified reasoning, recorded)

Static analysis reliably detects **capability** (which SDK is imported) but is **unreliable for actual
service calls** — high **false-negatives** on dynamic dispatch, dependency injection, config-driven
endpoints (`fetch(${env.PARTNER_API_URL}/…)`), indirect HTTP wrappers, and codegen/declarative
clients; and **false-positives** on test/dead code. For THIS model a false-negative is precisely the
**under-provisioning runtime failure** the addition exists to prevent (a called service whose key was
never provisioned → 401/500 at runtime); a false-positive is scope bloat. So scan cannot be the
generator's source of truth.

**The industry-pattern lineage (web-verified, recorded for the Grand gate):** OWASP **CycloneDX
SaaSBOM** makes an **explicit declaration the design-time authorized inventory**, with static scanning
as the **CI drift-detector** and runtime observability (eBPF/OpenTelemetry) as the production check.
This model maps onto our three pillars exactly: DECLARE = authorized inventory; SCAN = CI drift-detect
(V5); RUNTIME observe = production confirm (Phase-2). The declaration-burden-on-skill-authors is the
acknowledged cost of this choice (recorded for the Grand gate, §10 WP-list extension §23.3).

### 18.3 The services-called set + tier placement

The builder's **services-called set** = the **union of `services:` declarations** across the skills/
components it ships. Per-skill `SKILL.md` frontmatter is the natural home — **T3** (a property of the
specific product skill; the project seat knows which services its skills call). So: the catalog +
emergent categories are **T1** (§17.3); the per-skill `services:` declaration is **T3**; the generated
`{category, delta}` manifest is **T2 (derived)** (§21.4).

### 18.4 Precedence + Phase-1/Phase-2 (discovery)

**Precedence (deterministic): DECLARE generates; SCAN validates.** A scan-detected-but-undeclared
service is a **VALIDATION ERROR (§20 V5), fail-closed** — it BLOCKS generation until the declaration
is reconciled (added or explicitly waived); **scan never auto-promotes** (a false-positive would
provision an uncalled key; silently trusting scan would mask the very drift V5 exists to surface).
Fail-closed-to-human is the safe default (consistent with the §4 S2c human gate + the §2.6 fail-closed
posture). **Phase-1 (this spec):** the declare-primary + scan-validator MODEL + the precedence.
**Phase-2:** the static-scanner IMPLEMENTATION (the V5 drift-detector code) + the runtime observer.

---

## 19. The manifest GENERATION choreography (G1–G4, deterministic; Part-2 DoD item 3; HAMILTON lens)

Input: the builder's **services-called set** (from DECLARE, §18). Output: a `{category, delta}` manifest
the **unchanged** resolver (§2) consumes. **Baseline is NOT discovered** — it is universal and prepended
by `resolve()` (`BASELINE ∪ …`); generation determines only the **category + delta** layer.

### 19.1 The algorithm

```
GENERATE(services_called):
  G1  called_entries := ⋃  over service-id ∈ services_called  of  CATALOG[service-id].entries
      #   union of typed §3 entries (any kind). A service-id ABSENT from the catalog → V1 error
      #   (§20), fail-closed: STOP, do not emit. (kind-agnostic union — §17.2.1 well-typedness.)

  G2  category := best_fit_emergent_category(called_entries)
      #   = the emergent category (§21) whose entry-set is the LARGEST SUBSET of called_entries
      #   (maximal coverage, no over-reach). Ties / no cover → category = none (delta carries all).

  G3  delta.add  := called_entries  \  (BASELINE ∪ CATEGORY_TEMPLATE[category])
      delta.omit := CATEGORY_TEMPLATE[category]  \  (called_entries ∪ BASELINE)
      #   add  = called entries beyond baseline+category (the project-specific keys).
      #   omit = category entries the builder does NOT call (trim the emergent bundle to actual calls).
      #          omit can NEVER hit a baseline entry — baseline ∉ catalog/category (§17.2.3) →
      #          the §2.6 BaselineOmitError guard is preserved BY CONSTRUCTION.

  G4  emit { category, delta:{add, omit} }
```

### 19.2 Determinism

`best_fit_emergent_category` is a **pure max-subset selection** over the catalog: same services-called +
same catalog ⇒ **byte-identical** manifest. The generated manifest is **exactly the shape `resolve()`
(§2) already validates** — the resolver is untouched; only its INPUT is now derived. (Where a tie must
be broken — two categories of equal maximal coverage — break by category-tag ascending, so generation
stays total + deterministic; no §8 example hits a tie.)

### 19.3 The delta is DERIVED (the reframe's choreography half)

`delta` is no longer hand-authored — it is the **mechanical remainder** `(called_entries) \ (baseline
∪ chosen category)` for adds, and the called-trim `category \ (called ∪ baseline)` for omits. The delta
is now *provably* "the project-specific keys this builder calls beyond the emergent bundle, plus the
bundle-members it does not call." This is the data half of the §21 reframe.

### 19.4 Phase-1 vs Phase-2 (generation)

**Phase-1 (this spec):** the G1–G4 algorithm + its determinism property. **Phase-2:** the generator
CODE that runs G1–G4 over a populated catalog. The §23 self-runs exercise G1–G4 by hand against the
§22 seed to prove the algorithm hits 8/6/7.

---

## 20. The manifest VALIDATION choreography (V1–V5, fail-closed, before S0; Part-2 DoD item 4; HAMILTON lens)

The generated manifest is validated **strictly BEFORE S0** (it produces + certifies the manifest S0
consumes). Validation **REUSES the existing §2 guards** (it does not re-implement them) plus
discovery-specific completeness/minimality checks.

### 20.1 The checks

```
VALIDATE(services_called, generated_manifest):
  V1  EVERY-SERVICE-CATALOGED: every service-id ∈ services_called has a CATALOG record.
      else → ERROR "uncataloged service <id>" (cannot generate a complete manifest; add to catalog).

  V2  COMPLETE (anti-under-provision; the §3.4 / M3 runtime-completeness lineage):
      resolve(generated_manifest)  ⊇  called_entries
      — every called service's typed entries are in the resolved set.
      else → ERROR "service <id> called but not in resolved set".

  V3  MINIMAL (anti-bloat):
      resolve(generated_manifest) \ BASELINE has NO entry for an UNCALLED non-baseline service.
      (Baseline is universal + exempt — always present by definition.)
      else → ERROR "uncalled entry <kind,name> provisioned".

  V4  RESOLVE-WELL-FORMED (REUSE the §2 guards, unchanged):
      resolve(generated_manifest) raises NO BaselineOmitError (§2.6) AND satisfies §3.4
      runtime-completeness (every key-bearing surface has its paired credential — e.g.
      google-maps ⇒ MAPS_API_KEY, which §17.2.2 guarantees via the catalog record).
      else → the existing §2/§4 error fires (discovery did not weaken it).

  V5  NO-UNDECLARED-DRIFT (the scan pillar, §18):
      no scan-detected service-call is undeclared.
      else → ERROR "shadow service <id> detected but not declared" (reconcile declaration or waive).
```

### 20.2 Placement + the anti-under-provisioning spine

**Placement:** V1–V5 run as a gate **strictly before S0** (§4), fail-closed — an invalid manifest is
rejected with a named error and **never enters provisioning** (symmetric with §4's fail-closed
property: a half/ill-formed input never reaches serving). **V2 + V4 are the anti-under-provisioning
spine** — the discovery-side guarantee of the same property §3.4 / M3 gives the resolver: **a builder
cannot deploy missing a key for a service it actually calls.** V4 specifically REUSES the §2.6 +
§3.4 guards rather than re-implementing them, so Part 1's invariants remain the single source of truth.

### 20.3 Phase-1 vs Phase-2 (validation)

**Phase-1 (this spec):** the V1–V5 checks + placement + fail-closed posture. **Phase-2:** the validator
CODE (and the V5 scanner it depends on, §18.4). V4's reuse of §2.6/§3.4 means the Part-1 guard code is
the implementation; only V1–V3/V5 need new Phase-2 code.

---

## 21. The EMERGENT-TEMPLATES reframe (Part-2 DoD item 5; CHIRON lens)

### 21.1 Before → after (the reframe)

**Before:** category templates were **hand-curated static bundles** (geospatial = {Maps, PostGIS};
document-consuming = {document-parsing}), authored via arc (§3.2).

**After:** a category is an **EMERGENT common service-bundle** — *a named set of services (and their
catalog entries) that frequently co-occurs across builders' services-called sets.*

### 21.2 The §2-compliance precision (why the reframe is SAFE — does NOT change the resolver or §8)

A category **REMAINS EXACTLY WHAT THE RESOLVER CONSUMES — a named entry-set.**
`CATEGORY_TEMPLATE[category]` is still a set of typed entries, **unchanged in shape and in how
`resolve()` (§2) reads it.** **ONLY its PROVENANCE changes:**

| | Provenance of a category's membership |
|---|---|
| **Before** | a human hand-authored the bundle |
| **After** | the bundle **emerges** from observed co-occurrence, **promoted** to a named category via the §21.3 EMERGENCE rule |

So **the resolver (§2), the §3.2 category-template FORMAT, and the §8 expected sets (8/6/7) are
UNTOUCHED.** **STATED EXPLICITLY: this reframe does NOT change `resolve()` and does NOT change the §8
sets** — it changes only where a category's membership *comes from*. Confirms HAMILTON seam-(b): G2's
`CATEGORY_TEMPLATE[category]` still resolves because a category is still a named entry-set.

### 21.3 The EMERGENCE rule (the §3-graduation-rule, reframed to drive category FORMATION)

When a service-bundle recurs across **≥2 builders' derived call-sets**, it is **promoted** to a named
emergent category (or merged into one) via arc. Categories *grow from observed deltas* rather than
being declared up front. This is the **same open-closed governance** as the original §3 graduation
rule, now driving category **formation** (not just template extension).

**OWNER of the ≥2-builder emergence-DETECTION (named, Phase-2 governance).** Detecting that a
service-bundle has recurred across ≥2 builders' derived call-sets — and running the promotion arc — is
a **Phase-2 governance responsibility of the project-fleet steward** (the seat that holds the
cross-builder view of the live derived call-sets), executed as an **arc-gated promotion** (additive T1
catalog/category edit under §17.4 open-closed review). The detection requires a live builder population
(§21.5), so it is Phase-2 by construction; Phase-1 SEEDS the initial categories by hand (§21.5, §22)
and this rule names who owns the forward detection+promotion rather than leaving it ownerless. The
threshold (≥2 builders) remains flagged for ARGUS (§23.3 DWP-2 — emergent-category bootstrapping).

### 21.4 The delta is DERIVED + tier placement

The per-builder delta is **no longer hand-authored** — it is the §19 G3 mechanical remainder. The tier
model (T1 cookie-cutter / T2 manifest / T3 product) is **preserved, only the manifest's provenance
shifts**:

| Artifact | Tier | Owner | Note |
|---|---|---|---|
| The CATALOG (service→typed-entries) | **T1** | cookie-cutter | §17.3 |
| Emergent category bundles | **T1** | cookie-cutter | named entry-sets; §21.3 emergence rule (arc) |
| Per-skill `services:` DECLARATION | **T3** | the project seat | a property of the specific product skill (§18.3) |
| The GENERATED `{category, delta}` manifest | **T2 (derived)** | generated, not hand-authored | mechanically produced at the seam from T3 declarations through the T1 catalog |

**The clean ownership story:** the project seat (T3) declares what its skills call; the cookie-cutter
(T1) owns service→key knowledge (the catalog) + the emergent categories; the per-builder manifest (T2)
is **generated at the seam**. **No human hand-guesses the manifest** — the directive's goal. The reframe
REPLACES the hand-authored T2 manifest with a T2 manifest *generated from T3 declarations via the T1
catalog*; the tier model is preserved.

### 21.5 Bootstrapping (the "no live population yet" answer)

Emergence needs *observation*, which Phase-1 (design-time, no live builder population) lacks. So:
- the **Phase-1 catalog SEEDS** the initial emergent categories — `geospatial` and `document-consuming`
  — from the *known* co-occurrence in the three worked examples (Maps+PostGIS co-occur for geo
  builders; document-parsing for doc builders). These are the first emergent bundles, recorded as the
  initial state (§22). **They are EXACTLY the §3.2 bundles the gauntlet already validated, so the §8
  sets hold.**
- the **EMERGENCE rule (§21.3) governs how NEW categories form** as the population grows (Phase-2+).

So "emergent" is the **provenance/governance model**; the §22 seed categories are the concrete initial
state.

---

## 22. The catalog SEED records + emergent categories (driving the §23 worked examples)

**Seed catalog records (Phase-1 initial state; the four services the §8 fixtures exercise):**

```yaml
- service-id: google-maps      # client-side Maps-JS surface = API-key-bearing (§3.4)
  entries: [ {kind: gcp_api, name: google-maps}, {kind: gcp_secret, name: MAPS_API_KEY} ]
  gcp_api: google-maps
  category: geospatial
- service-id: spatial-db
  entries: [ {kind: db_extension, name: postgis} ]
  gcp_api: none
  category: geospatial
- service-id: document-parsing
  entries: [ {kind: gcp_api, name: document-parsing} ]
  gcp_api: document-parsing
  category: document-consuming
- service-id: bls-oews          # a BLS OEWS REST call — NOT a GCP API
  entries: [ {kind: thirdparty_rest_key, name: BLS_OEWS_API_KEY} ]
  gcp_api: none
  category: none                # a per-builder special; rides delta.add, not a category
```

**Seeded emergent categories (§21.5 bootstrap — identical to the §3.2 templates, so §8 holds):**

```
geospatial         = { (gcp_api, google-maps), (gcp_secret, MAPS_API_KEY), (db_extension, postgis) }
                     (= google-maps ∪ spatial-db catalog entries)
document-consuming = { (gcp_api, document-parsing) }
```

`MAPS_API_KEY` rides the `google-maps` record per §17.2.2 (the §3.4 paired-credential rule as a catalog
invariant). Baseline (universal, prepended by `resolve()`) = the §3.1 five entries — **NOT in the
catalog** (§17.2.3).

---

## 23. The three worked examples VIA DISCOVERY — machine-checkable generation fixtures (Part-2 DoD items 6+7)

Each example gives `services-called → GENERATED {category, delta} → resolved set`. **These ARE ADA's
GENERATION fixtures + VERA's generation probes:** `GENERATE(services_called) == EXPECTED_MANIFEST` and
`sorted(resolve(EXPECTED_MANIFEST)) == EXPECTED_SET` (the §8 set) must BOTH hold. The resolved sets are
the §8.1/§8.2/§8.3 sets **byte-for-byte** — Part 2 GENERATES the manifests Part 1 already validates.

### 23.1 The three generation fixtures (self-run below)

**prospector** — declares `services: [google-maps, spatial-db]`
```
G1 called_entries = { (gcp_api,google-maps), (gcp_secret,MAPS_API_KEY), (db_extension,postgis) }
G2 category = geospatial            (its bundle ⊆ called_entries — maximal cover)
G3 delta.add = ∅ ;  delta.omit = ∅  (called == baseline-free geospatial bundle)
G4 GENERATED = { category: geospatial, delta: {} }
   resolve() → BASELINE(5) ∪ geospatial(3) = 8     ✓ §8.1  (regression target HIT)
```

**scienceclaw** — declares `services: [document-parsing]`
```
G1 called_entries = { (gcp_api, document-parsing) }
G2 category = document-consuming    ({document-parsing} ⊆ called)
G3 delta = {}
G4 GENERATED = { category: document-consuming, delta: {} }
   resolve() → BASELINE(5) ∪ document-consuming(1) = 6   ✓ §8.2  (regression target HIT)
```

**labstat_bls** — declares `services: [document-parsing, bls-oews]`  (the load-bearing test)
```
G1 called_entries = { (gcp_api, document-parsing), (thirdparty_rest_key, BLS_OEWS_API_KEY) }
G2 category = document-consuming    ({document-parsing} ⊆ called; bls-oews ∉ any category)
G3 delta.add = { (thirdparty_rest_key, BLS_OEWS_API_KEY) }   (= called \ (baseline ∪ category))
   delta.omit = ∅
G4 GENERATED = { category: document-consuming,
                 delta: { add: [ {kind: thirdparty_rest_key, name: BLS_OEWS_API_KEY} ] } }
   resolve() → BASELINE(5) ∪ document-consuming(1) ∪ {BLS_OEWS_API_KEY}(1) = 7   ✓ §8.3 (target HIT)
```
**Load-bearing:** the BLS OEWS REST call is DECLARED → catalog-looked-up → GENERATES the
`+BLS_OEWS_API_KEY` delta (kind `thirdparty_rest_key`, **NO gcloud-enable** — `gcp_api: none` in its
§22 record), reproducing §8.3 EXACTLY. **The generated `{category: document-consuming, delta:{add:
[BLS_OEWS_API_KEY]}}` is byte-identical to the §8.3 hand-authored manifest** — discovery produces the
manifest the gauntlet already validated; the resolver is untouched.

### 23.2 §2-constraint compliance + regression confirmation

- `resolve()` (§2) + provisioning (§4 S0–S6) are **TEXTUALLY UNCHANGED** — discovery is a pure upstream
  front-end emitting the same `{category, delta}` shape (§1.1) they already consume.
- The §8 sets (8/6/7) are **HIT, not re-derived** — §23.1 generates manifests that resolve to exactly
  those sets; labstat_bls's generated manifest is **byte-identical** to the §8.3 manifest.
- The category stays a named entry-set the resolver consumes (§21.2 changes only provenance); the delta
  stays the `{add, omit}` shape; the §2.6 `BaselineOmitError` guard is preserved by §17.2.3 construction.
- The §12.A threat-maps (M1–M4/M6) are **untouched** — discovery defeats no new threat and weakens no
  existing mitigation (V4 REUSES the §2.6/§3.4 guards). **NO pressure on `resolve()`, the §8 sets, or
  the threat-maps arose → no dilemma to classify.** The targeted gauntlet **regression-confirms** the
  resolver/provisioning and **exercises the NEW manifest-GENERATION** against §23.1.

### 23.3 Self-assessed weak points — DISCOVERY ADDITION (for ARGUS to pressure-test)

These are the Part-2-specific weak points (the Part-1 WP-1…WP-10 in §10 stand unchanged):

- **DWP-1 — scan-validator feasibility is web-verified but Phase-2 implementation.** §18 RECOMMENDS
  declare-primary + scan-validator and web-verifies *why scan cannot be the source of truth*, but the
  V5 static-scanner is Phase-2 unbuilt code (§18.4). *Risk:* the V5 drift-guard's real-world
  effectiveness (its false-positive rate on test/dead code, its false-negative rate on the very dynamic
  patterns §18.2 names) is asserted from the literature, not measured. *Why this shape:* declare is the
  source of truth regardless of scan quality — a weak scanner degrades V5 to a best-effort drift hint,
  it does NOT corrupt generation (which reads DECLARE only). **ARGUS: confirm a weak/absent Phase-2
  scanner leaves generation correct (V5 is advisory-to-fail-closed, never a generation input).**

- **DWP-2 — emergent-category bootstrapping (Phase-1 seeds vs the emergence rule).** §21.5 SEEDS
  `geospatial` + `document-consuming` by hand (design-time, no population), while §21.3's emergence
  rule (≥2 builders → promote) governs Phase-2+. *Risk:* the "emergent" provenance is, in Phase-1,
  still a hand-authored seed — the reframe's emergence property is unexercised until a live population
  exists; the ≥2-builder threshold + its OWNER (who detects co-occurrence and runs the promotion arc)
  are unspecified. *Why this shape:* the seed categories are EXACTLY the §3.2 bundles the gauntlet
  validated, so §8 holds; emergence is the forward governance model, not a Phase-1 mechanism. **ARGUS:
  is ≥2 the right threshold, who owns detection, and is "seed-now-emerge-later" honest provenance or a
  relabel?**

- **DWP-3 — declare-completeness: a service called WITHOUT an SDK import / via raw config.** V5 (§20)
  catches an **imported** SDK / raw-HTTP-client whose service is undeclared. But a service reached
  purely through **runtime config** (a base URL in an env var, a data-driven endpoint table) with **no
  static import signal at all** is invisible to BOTH declare (author forgot) AND scan (nothing to
  detect). *Risk:* such a service is silently absent from services-called → under-provisioned → the
  exact 401/500 the addition exists to prevent — and V5 does NOT catch it. *Why this shape:* this is
  precisely why pillar (3) RUNTIME-observe (§18.1) exists as a named Phase-2 layer (eBPF/OTel see the
  actual outbound call regardless of how it was constructed); Phase-1 rests on declare-discipline +
  scan for the import-bearing majority. **ARGUS: confirm the no-import-signal service is an
  acknowledged Phase-1 gap closed only by the Phase-2 runtime observer — and that V5's scope is
  honestly "import-detectable drift," not "all drift."**

- **DWP-4 — the CATALOG is a new SoT / trust boundary (R-2-adjacent).** §17 makes the catalog the
  authoritative service→key map that generation trusts by construction. *Risk:* a malicious or
  erroneous catalog edit (e.g. adding an over-scoped entry to a service's record, or mis-pairing a
  credential) would propagate to EVERY builder that declares that service — a wider blast radius than
  the per-builder manifest integrity threat R-2 (§12.B) names. The catalog is a **shared** T1 asset, so
  a bad record is a fleet-wide over-grant. *Why this shape:* the catalog is T1 cookie-cutter (§17.3),
  edited only via additive arc (§17.4) under code-review — the same git-access-control + review trust
  model R-2 rests on, but at T1 scope. **ARGUS: is the catalog a NEW authz-relevant trust boundary that
  warrants its own named residual (R-3, catalog-integrity) alongside R-2, given its fleet-wide blast
  radius? — I PROPOSE it is (see §23.4); confirm or downgrade.**

- **DWP-5 — the SCOPE boundary: catalog DATA + scanner + generator = Phase-2 impl, not Phase-1.** §16.1
  draws Phase-1 (catalog STRUCTURE + choreography + reframe) vs Phase-2 (catalog DATA, scanner code,
  generator code, runtime observer). *Risk:* the §23.1 self-runs prove the CHOREOGRAPHY on a 4-record
  SEED; the real generator's correctness over a *populated* catalog (tie-breaking at scale, the
  best-fit max-subset selection on overlapping categories) is unexercised in Phase-1. *Why this shape:*
  Phase-1's job is to prove the model is COMPLETE + the choreography hits 8/6/7; the generator code is a
  Phase-2 build-and-verify surface (§16.1, §13). **ARGUS: confirm the Phase-1/Phase-2 line is drawn at the
  right place — choreography proven now, code verified in Phase-2 — and that the §23.1 seed self-run is
  sufficient Phase-1 evidence.**

### 23.4 Discovery-addition threat classification (op-disc §35.1 — DAEDALUS PROPOSES; ARGUS CONFIRMS)

The discovery addition is an **upstream SHAPE/choreography change**; I classify its security relevance
so no element carries NO §35.1 classification:

| Element (live §) | PROPOSED classification |
|---|---|
| Catalog structure / record schema (§17) | **not threat-ratified** (architectural/enabling structure; no runtime attack path of its own — the runtime-completeness it carries IS already M3, §12.A) |
| DECLARE-primary + SCAN-validator model (§18) | **not threat-ratified** (process/choreography change; V5 drift-guard is a correctness aid, not a runtime mitigation) |
| Generation G1–G4 (§19) | **not threat-ratified** (correctness/derivation change; the BaselineOmitError preservation rides on existing M4, §12.A) |
| Validation V1–V5 (§20) | **not threat-ratified** (V2/V4 are the discovery-side guarantee of the EXISTING M3/M4 properties — §20.2 REUSES the §2.6/§3.4 guards; introduces no new mitigation) |
| Emergent-templates reframe (§21) | **not threat-ratified** (provenance-only change; the resolver + §8 sets + threat-maps are untouched, §21.2) |
| Per-skill T3 `services:` declaration-integrity (§18.3) | **not threat-ratified — R-2 manifest-integrity LINEAGE, NOT a distinct threat.** A poisoned/incorrect T3 `services:` declaration drives the GENERATED manifest's scope (§19 G1 reads DECLARE as the source of truth), so a malicious/erroneous declaration *widens the generated manifest's scope* — which is exactly the **R-2 manifest-integrity** trust boundary (§12.B: a manifest edit that widens resolved scope), reached one step upstream at the declaration rather than the hand-authored manifest. It rests on the **same** git access-control + project-seat-review model R-2 rests on (a `services:` edit is a visible, reviewed T3 diff). It is therefore **R-2 lineage**, NOT a new named residual. (Confirmed by ARGUS at stage 2.) |
| **Catalog as a fleet-wide SoT / trust boundary (§23.3 DWP-4)** | **CANDIDATE NEW residual R-3 (catalog-integrity)** — I PROPOSE this is authz-relevant (a bad catalog record is a fleet-wide over-grant, R-2-adjacent but wider blast radius). It is NOT defeated in Phase-1 (rests on T1 arc-review + git access-control, like R-2). **ARGUS: CONFIRM as a §35.5 named residual R-3, or downgrade to not-threat-ratified if the T1 arc-review model fully subsumes it.** |

**Why no threat-anchored probe (op-disc §35.5 self-carve-out, §6.13):** every Part-2 element above is
PROPOSED **not threat-ratified** (process/choreography/structure change with no NEW runtime attack
path) — discovery DEFEATS no new threat; it generates the manifest whose EXISTING mitigations (M1–M4/M6,
§12.A) already carry their threat-anchored probes. The one CANDIDATE security-relevant element (DWP-4 →
R-3) is PROPOSED a **named residual (surfaced-not-defeated)**, which per §35.5 needs no threat-defeat
probe — only honest naming for the Grand to gate with it in view. **ARGUS confirms or revises all
classifications (§35.1 — cannot be self-exempted downstream).**

---

## 14. DoD coverage (directive §6 + brief's 10 elements)

| # | Element | Where |
|---|---|---|
| 1 | manifest schema (exact YAML, types, required/optional, `{category,delta:{add,omit}}`, entry `{kind,name}`) | §1 |
| 2 | resolution rule (algorithm, identity, precedence, add-wins, lint, purity) | §2 |
| 3 | typed-entry taxonomy (kind enum, provisioning path, scope-bearing, gcloud-enable) | §3 |
| 4 | provisioning choreography S0–S6 (emit-then-apply, kind-dispatch, ordered/idempotent/fail-closed, S2c gate, this-builder's-SA-key-only; per-step in/out/failure) | §4 |
| 5 | per-builder isolation (settled access half + budget half; fork CLOSED at Grand pre-build gate = Branch A + per-builder prepaid card/billing account) | §5 |
| 6 | DB-extension parameterization (pgvector baseline + PostGIS iff geo; DECIDE-C) | §6 |
| 7 | agent-access layer SHAPE vs CONTENT (T1 scaffold vs T3 seat) | §7 |
| 8 | three worked examples as concrete manifests + EXACT resolved sets (machine-checkable; labstat_bls delta proof) | §8 |
| 9 | stoa--reg alignment note (no Phase-1 dependency) | §9 |
| 10 | self-assessed weak points (seeded with carried items) | §10 |
| — | threat→mitigation map (op-disc §35.4 A3: M1–M4/M6 triples + M5 §35.5 residual + not-threat-ratified classifications; binds already-audited mechanisms) | §12 |
| — | isolation-UNIT fork CLOSED at Grand pre-build gate (Branch A + per-builder prepaid card/billing account; M5 mooted) | §5.B, §11, §12.B, §12.D |

**Part-2 DoD coverage (the KEY-DISCOVERY PROCESS addition — u--9s2 Phase-1 revision):**

| # | Part-2 element | Where |
|---|---|---|
| P1 | service→key CATALOG (per-service record: typed §3 entries 1:N + gcp_api + category; baseline NOT in catalog; §3.4 paired-credential as a catalog invariant; T1; additive) | §17, §22 |
| P2 | DISCOVERY step (DECLARE-primary authoritative + SCAN-validator fail-closed + runtime-observer Phase-2; web-verified reasoning + OWASP SaaSBOM lineage) | §18 |
| P3 | manifest GENERATION (G1–G4 deterministic; services-called → catalog → union → best-fit emergent category → derived delta; baseline not discovered) | §19 |
| P4 | manifest VALIDATION (V1–V5: cataloged + COMPLETE + MINIMAL + resolve-well-formed [REUSES §2.6/§3.4] + no-undeclared-drift; before S0, fail-closed) | §20 |
| P5 | EMERGENT-TEMPLATES reframe (category = emergent bundle; provenance-only; delta DERIVED; emergence rule; Phase-1 seeds; STATED: does NOT change resolver or §8 sets) | §21, §22 |
| P6 | tier placement (catalog + emergent categories = T1; per-skill `services:` = T3; generated `{category,delta}` manifest = T2 derived) | §17.3, §18.3, §21.4 |
| P7 | 3 worked examples VIA DISCOVERY (services-called → generated manifest → 8/6/7; machine-checkable generation fixtures; labstat_bls bls-oews → +BLS_OEWS_API_KEY, no gcloud-enable, byte-identical to §8.3) | §23.1 |
| P8 | self-assessed weak points for the discovery addition (DWP-1…DWP-5) + Part-2 threat classification (PROPOSED not-threat-ratified; candidate R-3 catalog-integrity) | §23.3, §23.4 |
| — | §2-constraint compliance + regression confirm (resolver §2 + provisioning §4 + §8 sets + §12.A threat-maps TEXTUALLY UNCHANGED; 8/6/7 HIT not re-derived; no dilemma) | §16.0, §23.2 |

---

## 15. Provenance

Formalized by **CAPTAIN_DAEDALUS_the_stoa** from the CHIRON+HAMILTON CO-DESIGN CONVERGED unified doc
(`design-codesign.md`), grounded by STRABO's primary-GCP-docs check (VERA-confirmed verbatim). No
redesign; formalization + tightening + weak-point surfacing only. The isolation-UNIT fork was carried
UP to Polybius the Grand and **RESOLVED at his pre-build gate (2026-06-26): Branch A + per-builder
prepaid card/billing account; M5 mooted** — recorded in this doc as a documentation-only fold of the
gate decision (no design change; R-1/R-2 remain Phase-2 named residuals).

**Part 2 (§16–§23, the KEY-DISCOVERY PROCESS addition — u--9s2 Phase-1 revision):** formalized by
**CAPTAIN_DAEDALUS_the_stoa** from the CHIRON+HAMILTON **DISCOVERY CO-DESIGN CONVERGED** unified doc
(`agents/design/stoa--jw5/discovery-codesign.md`; HAMILTON's lens at
`discovery-choreography-hamilton.md`), web-verified for the declare-vs-scan recommendation (CHIRON
catalog + emergent-templates reframe; HAMILTON discovery/generation/validation choreography; OWASP
CycloneDX SaaSBOM precedent, 2026-06-26). Discovery is a **strictly upstream front-end** that GENERATES
the `{category, delta}` manifest the Part-1 resolver consumes; **the Part-1 resolver (§2), provisioning
(§4 S0–S6), §8 fixtures (8/6/7), and §12.A threat-maps STAND TEXTUALLY UNCHANGED** — Part 2 added new
sections only (§16.0 load-bearing constraint; §23.1 self-run confirms 8/6/7; §23.2 regression-confirm).
No redesign of Part 1; SHAPE-only addition (catalog STRUCTURE + choreography + reframe; the catalog
DATA / scanner / generator code / runtime observer are Phase-2, §16.1 / §13). **Author: Denson Smith.**
