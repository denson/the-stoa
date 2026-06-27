# u--9s2 Phase-2 inc 2.3 — HAMILTON lens: the S0–S6 provisioning choreography + the MOCK substrate + the credential-acquisition deploy-help library

**Seat:** MAJOR_HAMILTON_the-stoa (workflow-architect). **Arc:** stoa--k48 / u--9s2 Phase-2 increment 2.3 — the provisioning choreography (ONE pass; design folded into the build).
**For fold into** DAEDALUS's buildable formalization of the CHIRON+HAMILTON co-design.
**My lane (per brief):** the S0–S6 PROVISIONING WORKFLOW mechanics + the MOCK/DRY-RUN SUBSTRATE (structural TRIPWIRE) + the human-in-the-loop credential-acquisition choreography.
**CHIRON's lane (co-design):** the ownership/tier structure (T1 vs T3, the §7 SHAPE/CONTENT split) + the builder-deploy skill HOME (stoa--wmu A vs B). The S5 SHAPE *contents* are CHIRON's; how S5 *stands them up in the choreography* is mine.

> **Ground truth held unchanged.** This design implements design-formal `stoa--jw5` §4 (S0–S6 emit-then-apply), §5 (isolation), §6 (db-extension), §7 (agent-access SHAPE), §8 (worked examples) and §12 (threat→mitigation M1–M6 / residuals R-1/R-2/R-3) **verbatim** — it does not redesign them. It adds the buildable *mechanics* the Phase-1 design deliberately left to the Phase-2 build arc (§13: "Building the cookie-cutter skill — Phase-2 build arc"). It provisions **nothing real** (TRIPWIRE, directive §1).

---

## 0. The one architectural decision everything else falls out of

**The choreography is a pure EMITTER plus a port-driven ENGINE; the real applier lives OUTSIDE the package, forever.**

design-formal §4 mandates an **emit-then-apply split**: the cookie-cutter EMITS a value-free provisioning spec (slot names, never values); a credential-disciplined applier (CI-via-WIF, or a human one-shot per `railway-keyring-deploy`) executes the credential-bearing steps. I make that split **structural**, and I make it **permanent** (not a 2.3-only scaffold):

```
                 ┌─────────────────────────── the PACKAGE (builder_deploy_core) ──────────────────────────┐
 resolve()  ──►  │  emit_spec(resolved, slug)  ──►  VALUE-FREE SPEC  (slot names, action plan, ordering)   │
 (2.1, pure)     │       (pure; no I/O)                  │                                                  │
                 │                                       ▼                                                  │
                 │  Choreographer(provisioner).run()  walks S0–S6, dispatching each step's actions to an    │
                 │       INJECTED `Provisioner` PORT.  The ONLY concrete port shipped is MockProvisioner.   │
                 └───────────────────────────────────────┼──────────────────────────────────────────────────┘
                                                          │  the value-free spec crosses the SEAM
                                                          ▼
   ┌──────────────────────────── OUT OF PACKAGE — the real APPLIER (never agent package code) ──────────────────┐
   │  CI-via-WIF (credential-discipline) OR human one-shot (railway-keyring-deploy: OS keyring → ENV/STDIN).     │
   │  Consumes the value-free spec; the human/CI supplies the values at S2c. 2.3 builds NONE of this against     │
   │  real infra; 2.4 (scienceclaw) is the first real run, gated separately by the Grand.                         │
   └─────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

Three consequences, each load-bearing:

1. **`emit_spec` is pure** — same property as `resolve()` (§2.3): reads no environment (no GCP, no network, no clock, no filesystem beyond its inputs). It is the *dry-run output*. Running it can never touch infra **because it has no I/O at all**.
2. **The engine drives a PORT, not a CLI.** `Choreographer.run()` never imports `subprocess`, `socket`, `urllib`, `requests`, `gcloud`, or `railway`. It knows only the abstract `Provisioner` interface. The **only** concrete implementation that ships in the package is `MockProvisioner`. To reach real infrastructure you would have to *write a new concrete provisioner that does I/O* — which does not exist, and would be a code-review-visible addition.
3. **The real applier is out-of-package and credential-disciplined** — CI-via-WIF or the human keyring one-shot. There is **no in-agent `RealProvisioner`** in 2.3 *or* 2.4: per credential-discipline (M2), the agent never runs the credential-bearing apply. The package's permanent job is EMIT (pure) + an engine that can drive a MOCK (for test). This is why the structural TRIPWIRE is not a temporary 2.3 fence — it is the architecture.

This is the **model-cascade decision** for this choreography (my §5 duty): **S0–S6 are deterministic infrastructure steps, so they are DETERMINISTIC CODE — the bottom rung of the cost ladder. There is NO LLM in the S0–S6 loop.** The only place a model appears in the whole builder-deploy story is the *upstream* SUGGEST front-door (2.2, examine→suggest→confirm→declare), which produces the manifest a human confirms; once the manifest exists, resolution and provisioning are pure/deterministic. Putting a model inside S0–S6 would be the opposite of saturation-proven down-tiering — it would inject non-determinism into a step that is, by construction, a deterministic recipe (§3.3: "one `kind` = one complete deterministic recipe").

---

## 1. Module structure (what DAEDALUS formalizes, what ADA builds)

A new `provision/` package under the existing `builder_deploy_core` (the 2.1 core), reusing `resolve()` / `derive_sa_scope()` / `check_runtime_completeness()` unchanged:

```
builder_deploy_core/
  resolution/        # 2.1 — resolve(), derive_sa_scope(), check_runtime_completeness()  [REUSED, byte-unchanged]
  suggest/           # 2.2 — examine→suggest→confirm→declare                              [REUSED, byte-unchanged]
  provision/         # 2.3 — NEW
    __init__.py
    spec.py          #   emit_spec(resolved, builder_slug) -> ProvisioningSpec  (PURE, value-free)
    port.py          #   Provisioner ABC (the abstract port) + the step-action dataclasses
    mock.py          #   MockProvisioner — the ONLY concrete port; in-memory ledger, no I/O
    choreographer.py #   Choreographer(provisioner).run(resolved, slug) -> RunLedger  (walks S0–S6)
    steps.py         #   S0..S6 as pure step functions: (resolved, slug, provisioner) -> [StepAction]
    __main__.py      #   `python -m builder_deploy_core.provision` — dry-run emit + mock walk (repro surface)
  data/ ...          # baseline.toml + categories + catalog  [REUSED]
```

**Import-discipline (the TRIPWIRE's teeth, §3):** `provision/` imports only `builder_deploy_core.*` + stdlib `dataclasses`/`enum`/`typing`. It imports **none** of `subprocess`, `os.system`, `socket`, `http`, `urllib`, `requests`, `asyncio.subprocess`. A test asserts this by AST/grep (§3.2). `mock.py` is also pure — it records actions into a list; it does not even read the filesystem.

---

## 2. The S0–S6 choreography — inputs → outputs → failure (the buildable contract)

Each step is a pure function `step(resolved_set, builder_slug, provisioner) -> list[StepAction]`. The `Choreographer` runs them **in fixed order** and stops at the first failure or BLOCK (fail-closed). Every action is dispatched on the resolved entry's `kind` (§3.3). The engine asserts the **global properties** (§4 design-formal): ordered, idempotent/create-or-get, fail-closed.

| Step | `kind` dispatch | Action(s) emitted (→ provisioner port call) | Failure / block behavior |
|---|---|---|---|
| **S0** isolation scaffold | — (fixed, per-builder) | `ensure_project(slug)` → project id; `ensure_sa(slug)` → **bijective** `sa-<slug>@<project>` principal; `set_budget_boundary(slug)` → the §5.B record (prepaid-card HARD cap + GCP alert/quota SOFT layer, **represented**, not created) | any failure ABORTS before any key materializes (fail-closed); **must run before any S2 key** |
| **S1** API enablement | `kind == gcp_api` | per resolved `gcp_api`: `enable_api(project, api)` + `grant_api_role(sa, api)` (idempotent) | an enable failure ABORTS the remainder; builder never reaches serving |
| **S2** secret slots | `kind ∈ {gcp_secret, thirdparty_rest_key}` | **2a** `ensure_secret_slot(project, name)` (slot only, no value); **2b** `grant_secret_accessor(sa, name)` **per-secret** (never project-wide); **2c** `require_population(name)` → the HUMAN/credential gate | **S2c BLOCKS** on any unpopulated slot → `BLOCKED-on-human` report, halts before S3/S5. **Never improvises a value.** `thirdparty_rest_key` entries have **NO S1 step** (secret-only — the labstat_bls proof) |
| **S3** Railway provisioning | `kind == railway_var` + secret-backed vars | `provision_db_service(slug, db_extensions)` (baked-init image, §6); `provision_serving_service(slug)`; per var: `set_railway_var(service, name, source=<slot-ref>)` **via STDIN-source descriptor only** (the spec names the *source slot*, never a value); inject **this builder's SA-key-ref ONLY**; mount volume at `/var/lib/tailscale` | abort on any var-set/service-create failure; **no cross-builder key ref ever injected** |
| **S4** DB extensions | `kind == db_extension` | `apply_db_extension(db_service, ext)` — emits exactly the resolved `CREATE EXTENSION` lines (pgvector always; postgis iff resolved). PostGIS needs the §6 DECIDE-C base image → `select_base_image(postgis ∈ resolved)` | a missing required base-image capability aborts db-init |
| **S5** agent-access SHAPE | — (fixed T1 scaffold; **NOT** manifest-resolved) | `stand_up_mesh_shape(slug)` → the §7 SHAPE: tailscaled → `tailscale serve --https=443` → 0600 AF_UNIX socket → in-mesh trigger; serve-injected `Tailscale-User-Login` identity; deny-by-default + `<BUILDER>_OPERATORS` allowlist; **Funnel OFF**; + the CLI-client-skill template **carrying a `<VERB>` placeholder, NOT `/run`** (CHIRON §2: the 2.3 generalization of newswire IS extracting the verb to a parameter). **Domain-empty** — zero domain verbs incl. `/run` (the §7 boundary; CHIRON owns the SHAPE contents) | a half-provisioned builder (any S0–S4 abort) NEVER reaches S5 serving (fail-closed) |
| **S6** verify | — | door preflight; assert each resolved `gcp_api` enabled; each resolved `db_extension` present; **no secret slot unpopulated** (else `BLOCKED-on-human`); **runtime-completeness (§3.4):** for every template-declared `(gcp_api, gcp_secret)` pairing, the paired secret is resolved + populated. **Idempotent re-run = no-op** (converges; cannot widen scope) | report-only; PASS or a specific BLOCKED/FAILED report |

**Ordering invariant (engine-enforced):** the `Choreographer` runs `[S0, S1, S2, S3, S4, S5, S6]` as a fixed list and records each action with its step index into the `RunLedger`. **S0 isolation precedes any S2 key precedes any S3/S5 serving** is then a *checkable property of the ledger* (action step-indices are monotonic), not a convention. This is the workflow-architect's topology call: S0–S6 is a **linear pipeline, not a fan-out** — every step consumes the prior step's live state (you cannot enable an API before the project exists; you cannot serve before the secret slots are bound). There is no independent branch to parallelize; the barrier smell-test says a pipeline is correct here.

**Idempotency (create-or-get):** every port method is `ensure_*`/`grant_*` semantics — a second `run()` against the same ledger state emits the same actions and the mock returns the same ids with `created=False`. The engine asserts a re-run adds **zero new** create-actions (the §4 idempotent property; the ADD direction is total). *Subtractive* prune-on-removal is **out of scope** (§13, R-1) — 2.3 is initial-provision correctness (t0), exactly as Phase-1.

---

## 3. THE MOCK / DRY-RUN SUBSTRATE — the structurally-honored TRIPWIRE (load-bearing)

This is the deliverable the directive flags as load-bearing: the mock must make the DoD **machine-checkable** AND make real-infra reach **structurally impossible** in the test path. I get both from the §0 architecture.

### 3.1 What the mock IS

`MockProvisioner` is the only concrete `Provisioner`. It implements every port method as: **record the requested action into an in-memory `ledger: list[StepAction]`, return a synthetic deterministic id** (e.g. `mock-project-<slug>`, `mock-sa-<slug>@mock-project-<slug>`). It performs **no I/O whatsoever** — no subprocess, no network, no file write. It is constructed with two **value-free** knobs:

- `populated: set[str]` — a set of secret-slot NAMES the mock treats as already populated. **This carries NO value** — it is a boolean membership marker ("the human has populated this slot"), never a credential. Default `frozenset()` → **everything is unpopulated** → S2c BLOCKS.
- `fail_at: Optional[str]` — an optional step/action id at which the mock raises, to exercise the fail-closed abort paths (S0 abort, S1 enable-failure, S3 var-set-failure, S4 missing-base-image).

The mock thus drives the choreography in **two value-free modes**:

1. **`MockProvisioner()` (default, unpopulated)** → S2c reports every `gcp_secret`/`thirdparty_rest_key` slot as `BLOCKED-on-human` and **halts before S3/S5**. This proves **DoD#2 fail-closed / S2c blocks** and **DoD#3 value-free** (the BLOCKED report names slots, holds no value).
2. **`MockProvisioner(populated=<all resolved secret slot names>)`** → S2c passes (slots marked populated, still value-free) → S3–S6 run → the ledger lets us assert **DoD#4 isolation**, **DoD#5 SHAPE stands up**, and **S6 idempotency**.

Even in mode 2 the mock holds **zero credential values** — only the value-free "slot is populated" booleans. The structural TRIPWIRE is intact in both modes.

### 3.2 Why real infra is STRUCTURALLY unreachable (the strongest TRIPWIRE form)

Three independent structural walls, each machine-checkable, none relying on "we remembered not to call gcloud":

- **W1 — no I/O imports.** A test (`test_tripwire_no_infra_imports`) walks every module under `provision/` with `ast` and asserts the import set is a subset of `{builder_deploy_core.*, dataclasses, enum, typing, __future__}`. **Grep-provable corollary** (the attestation command, DoD#6): `grep -rnE '\b(subprocess|socket|urllib|requests|httpx|gcloud|railway|os\.system|popen)\b' builder_deploy_core/provision/` returns **nothing**.
- **W2 — only the mock concrete port exists.** A test asserts `Provisioner.__subclasses__()` (after importing the package) `== [MockProvisioner]`. There is no real adapter to inject. The `Choreographer` constructor **requires** a `Provisioner` argument (no default), so a run cannot start without one, and the only one in existence is the mock.
- **W3 — the emit side has no port at all.** `emit_spec` does not take a provisioner; it is a pure transform `resolved → spec`. The dry-run path cannot touch infra because it has no actor that could.

This is "the test path CANNOT reach real infra (no real `gcloud`/`railway`/card call is even possible)" expressed as **three falsifiable code properties**, which is stronger than a behavioral "the test didn't call it" — VERA's TRIPWIRE probe (DoD#6) asserts W1/W2/W3 hold, and the attestation (relay-up #3) cites them.

### 3.3 The machine-checkable DoD mapping (ADA's fixtures = VERA's probes)

Every DoD item resolves to an assertion over `emit_spec(...)` output or the `RunLedger`:

| DoD | Assertion (mock/dry-run) |
|---|---|
| **#1** end-to-end emit | `emit_spec(resolve(M), slug)` for prospector/scienceclaw/labstat_bls equals the expected **value-free spec** (the §8 resolved sets rendered as the per-builder action plan — project+SA, APIs to enable, secret slots, railway vars, db extensions, budget boundary). Byte-stable (deterministic order). |
| **#2** ordered/idempotent/fail-closed | ledger step-indices monotonic (S0<S2<S3/S5); a 2nd `run()` adds 0 create-actions; `fail_at` aborts the remainder; default mock → S2c `BLOCKED-on-human` halts before S3. |
| **#3** value-free emit | `grep`-style assertion: no spec field nor ledger action contains a value — only slot NAMES + source-slot refs. A `assert_value_free(spec)` walks every leaf and asserts none is a secret value (there are none to leak — the mock never had one). |
| **#4** per-builder isolation | ledger has exactly one `ensure_project` and one `ensure_sa` per run, `sa-<slug>` bijective; every `grant_secret_accessor` is per-secret (carries a single secret name, never a project wildcard); the SA scope == `derive_sa_scope(resolved)` (the §5.A mechanical union); the budget-boundary record present. |
| **#5** SHAPE stands up, domain-empty | mode-2 ledger contains the S5 `stand_up_mesh_shape` action; its emitted scaffold has the §7 T1 surface (0600 AF_UNIX, header-trust, deny-by-default, `<BUILDER>_OPERATORS`, Funnel OFF) and **zero domain verbs**. The boundary test is CHIRON's §2 mechanical grep: scan the **entire** emitted T1 scaffold + CLI-client template for ANY domain verb (`/run`, `collect`, `embed`, `ingest`, `search`, or any builder-specific endpoint) — a hit is the leak. T1 ships only the **`<VERB>` placeholder + health**; `/run` is the newswire **T3** fill, not T1. |
| **#6** TRIPWIRE held | W1/W2/W3 (§3.2) — three structural tests + the grep attestation. |
| **#9** full suite green | the new `tests/test_provision_*.py` + the existing 2.1/2.2 suite + gen-data + app — VERA runs the FULL suite (not just the bespoke probes), per the gauntlet-verify discipline. |

### 3.4 Negative fixtures (fail-closed, mirroring §8.4's style)

- `test_s2c_blocks_unpopulated` — default mock → run halts at S2c, ledger ends with `BLOCKED-on-human` naming every secret slot, **no S3/S5 action present**.
- `test_s0_abort_no_key_materialized` — `fail_at="S0:ensure_sa"` → ledger has the failed S0 action and **zero S2 actions** (no key materialized before the lock).
- `test_idempotent_rerun_no_widen` — two runs, 2nd adds zero create-actions.
- `test_labstat_skips_s1_for_thirdparty` — labstat_bls run: `BLS_OEWS_API_KEY` appears in S2 (secret slot) + S3 (railway var) but **never** in S1 (no `enable_api` for it) — the §8.3 kind-dispatch proof carried into the choreography.

---

## 4. The human-in-the-loop credential-acquisition choreography (the deploy-help library)

This is the **applier UX shape** — DESIGNED in 2.3, **exercised against MOCK dashboards only**, provisions nothing real (directive §2). It is the PRINCIPAL's 2026-06-26 default UX, recorded at u--9s2:

```
agent drives a browser to the dashboard EDGE
   → a clickable link opens the SAME dashboard in a browser the agent CANNOT see
       → the human generates/mints the secret PRIVATELY (agent never sees the value)
           → the agent helps DEPLOY via a small repeated-pattern library
               (OS-keyring paste-script  |  Railway-CLI  |  Railway-UI walkthrough)
```

Build-machine browser+computer-use is **available-by-construction** (Grand policy; no degraded/no-automation fallback path — see `[[project-build-machines-mandate-browser-computer-use]]`).

### 4.1 The pattern library — dispatched per secret-acquisition method

Each S2c-blocked slot maps to one **acquisition pattern**. The method is an in-band property of the slot (derivable from `kind` + a per-catalog `acquisition` field), so the choreography emits the right deploy-help pattern per slot:

| Acquisition method | Slots (examples) | Edge the agent drives to | Clickable link → unseen browser | Deploy-help pattern |
|---|---|---|---|---|
| **mint-via-GCP-console** | `MAPS_API_KEY` (gcp_secret, key-bearing) | GCP Console → APIs & Services → Credentials, for **this builder's project** | link opens the Credentials page; human clicks **Create credentials → API key**, copies it privately | `keyring_paste.py` (getpass, hidden) → keyring slot → `railway_set_secret.py --var MAPS_API_KEY --from <slot>` (STDIN) |
| **mint-via-thirdparty-dashboard** | `BLS_OEWS_API_KEY` (thirdparty_rest_key) | the third party's registration page (e.g. BLS public-data API signup) | link opens the signup; human registers + receives the key by email/page privately | `keyring_paste.py` → keyring → `railway_set_secret.py` (STDIN) |
| **generate-locally** | `POSTGRES_PASSWORD` (gcp_secret, generated) | **no dashboard** — nothing to mint | — | `keyring_generate.py` (script generates a strong random; no human ever sees it) → `railway_set_secret.py --skip-deploys` BEFORE the db-init deploy |
| **mint-Railway-PAT** | Railway account token (the one unavoidable UI step) | Railway dashboard → Account Settings → Tokens | link opens Tokens; human mints + copies privately | `keyring_paste.py` (default slot `ghostbead-railway/api-token`) → every railway call via `railway_run.py` (ENV) |
| **mint-tagged-authkey** | `TS_AUTHKEY` (railway_var, mesh) | Tailscale admin → Settings → Keys (+ the §7 console prerequisites: HTTPS certs ON, Funnel OFF, deny-by-default policy, tagged) | link opens Keys; human mints a **reusable, non-ephemeral, tagged** key privately | `keyring_paste.py` → `railway_set_secret.py --var TS_AUTHKEY` (STDIN) |

**The invariant across every pattern:** the value transits *human → (private browser) → keyring → CLI subprocess (ENV/STDIN)* and **never** the agent's stdout/argv/transcript/disk (M2 / credential-discipline). The agent's role is to *drive to the edge*, *hand the clickable link*, and *run the value-free deploy-help script* — it is blind to the value throughout. The reuse source is `railway-keyring-deploy` (the bundled `keyring_paste.py` / `keyring_generate.py` / `railway_set_secret.py` / `railway_run.py`) at the USER-tier path `~/.claude/skills/railway-keyring-deploy/`.

### 4.2 What "exercised against mock dashboards only" means in 2.3

The choreography in 2.3 **emits the deploy-help plan** for each S2c slot (which pattern, which edge URL template, which keyring-paste invocation) — it does **not** open a real browser, mint a real key, or paste into a real keyring. The mock substrate asserts: for each worked example, the emitted plan dispatches the **correct** pattern per slot (MAPS_API_KEY→mint-via-GCP-console; BLS_OEWS_API_KEY→mint-via-thirdparty; POSTGRES_PASSWORD→generate-locally; etc.) against **placeholder/mock** dashboard URLs. The real drive-the-browser execution is 2.4. This keeps the TRIPWIRE structural: 2.3 produces the *plan text*, not the *action*.

---

## 5. The bw coordination seam (my distinctive deliverable, role §6)

The seam no other seat owns: **how the workflow's value-free output feeds back into the durable bw substrate the next session/applier reads.** Here:

- **The emitted value-free spec IS the durable seam artifact.** It is what crosses from the agent/emit world into the human/CI applier world. It should be **written to the working tree** (or attached on beadwork with a working-tree-pathed cite) so a 2.4 applier reads it — per `[[reference-attach-only-artifacts-dangle-worktree-cites]]`, an attach-only artifact dangles any on-disk cite; the spec is cited by the provisioning checklist, so it lives on disk.
- **The PROVISIONING CHECKLIST (relay-up #1) is the human-rendering of the emit.** `emit_spec` → a `render_checklist(spec)` produces the exact step-by-step "what the PRINCIPAL provisions for a real builder, with WHEN" (per-builder GCP project + prepaid card + billing account + Railway + Tailscale + which secret slots need human population at S2c, by acquisition method §4.1). The checklist is a *pure transform of the emit*, so it cannot drift from what the choreography would actually do.
- **The credential-discipline ATTESTATION (relay-up #2)** is a derivation over the emit: every slot is value-free (DoD#3), the applier is the keyring/WIF path (§4), per-builder project+card is the hard cap (§5.B), no agent holds a value (M2). A pure check over the spec + the §3.2 structural walls.
- **The TRIPWIRE-HELD attestation (relay-up #3)** cites the W1/W2/W3 structural tests + the grep result (§3.2).

The script-cannot-run-bw/git discipline (workflow-composer) applies: this choreography is **deterministic Python code**, not an Anthropic dynamic-workflow, so the bw landing is done by the orchestrating seats (PLINY → FM → Polybius_the_Stoa) at the relay-up, not by the package. The package PRODUCES the three relay-up artifacts as files; the seats LAND them on bw. (Note for the gauntlet itself: the design→build→verify gauntlet *is* a candidate for the workflow-composer pipeline, but that is PLINY's orchestration choice for running the arc, distinct from the provisioning choreography this design specifies.)

---

## 6. Boundary with CHIRON (co-design seam) — open questions routed UP

1. **S5 SHAPE contents vs stand-up.** I specify *how* S5 stands up the mesh-API SHAPE in the choreography (the `stand_up_mesh_shape` action + the domain-empty boundary test). CHIRON owns *what* the T1 SHAPE contains (the §7 SHAPE/CONTENT line). The emitted S5 scaffold's exact surface (entrypoint template, policy template, the CLI-client-skill skeleton) is CHIRON's contents folded into my action. **No overlap if CHIRON delivers the SHAPE inventory and I consume it as the S5 action payload.**
2. **The HOME (stoa--wmu A vs B) — CHIRON proposes, affects my module path.** My `provision/` module is HOME-agnostic (a sub-package of `builder_deploy_core`). But the **stoa--jd5 packaging fix** (PLINY folds) and the skill HOME determine where the *skill* (SKILL.md + the deploy-help library) lives. If HOME=A (the-stoa forge-owned), the skill ships in-repo under `.claude/skills/builder-deploy/`; if HOME=B (standalone), it ships at the standalone tooling home. My emit/choreography code does not move either way. **Flag: the jd5 package-data glob fix (`../data/**/*.toml` → a setuptools-honored layout) interacts with HOME; the correct packaging spec is determinable only once HOME is chosen** (exactly the stoa--jd5 blocker note). I defer to CHIRON's HOME proposal + PLINY's jd5 fold; my only requirement is that `provision/` remains an importable sub-package of `builder_deploy_core` with the data tree reachable.

---

## 7. Self-assessed weak points (for ARGUS to pressure)

- **HW-1 — the `populated` mock knob could be mistaken for a value channel.** It is a value-free name-set, but a careless build could let a value ride it. *Mitigation:* type it `set[str]` (slot names), and `assert_value_free` walks the mock ledger too. **ARGUS: confirm the mock cannot become a value channel.**
- **HW-2 — `acquisition` method as an in-band catalog field.** §4.1 dispatches the deploy-help pattern on a per-slot `acquisition` method. The 2.1 catalog may not carry it yet. *Mitigation:* derive the default from `kind` (gcp_secret-key-bearing→mint-via-GCP-console; thirdparty_rest_key→mint-via-thirdparty; POSTGRES_PASSWORD→generate-locally) and let the catalog override; do **not** mint a new required field that breaks the 2.1 fixtures. **ARGUS: confirm no §8 regression from an added optional field.**
- **HW-3 — emit_spec output schema is new surface.** The value-free spec is a new artifact the checklist + attestations + 2.4 applier all consume. If its schema is loose, the relay-up artifacts drift. *Mitigation:* a `ProvisioningSpec` dataclass with an explicit schema + a golden-file test per worked example. **ARGUS: confirm the spec schema is pinned, not free-form.**
- **HW-4 — `tomllib` data reachability under the chosen HOME — RESOLVED by CHIRON's jd5 recommendation.** The choreography reuses `dataload` which reads `data/` via `Path(__file__).parent.parent/data`; the stoa--jd5 glob fix must keep that reachable post-packaging. *Resolution:* CHIRON §5 recommends moving `data/` **inside** the package (`builder_deploy_core/data/`, `dataload` → `Path(__file__).parent/data`, + an install-then-import smoke test) — a normal intra-package glob setuptools honors, HOME-independent, landing this pass (PLINY's fold). That makes the data tree reachable post-packaging by construction, so my `provision/` module (which only requires the data tree be importable) does not deepen the debt. **ARGUS: confirm the provision module rides the jd5-fixed layout cleanly.**

---

## 8. Reconciliation record (HAMILTON ⟷ CHIRON cross-lane seams — reconciled 2026-06-27)

CHIRON's ownership/tier half (`chiron-ownership-tier-design.md`) and this mechanics/mock half were co-designed concurrently and reconciled. The seams:

1. **emit-then-apply** — IDENTICAL conclusion from both lanes. CHIRON's EMIT=T1-pure-value-free / APPLY=credential-disciplined / S2c-structural-seam (`populated=true` boolean, never the value) == my §0 pure-emitter + port-driven-engine + §3 two-mode value-free mock. CHIRON explicitly endorses "a pure function can't reach real infra = the strongest TRIPWIRE form." No conflict.
2. **Per-step tier** — CHIRON's §1 table asserts every S0–S6 recipe is T1, parameterized by the T2-derived resolved set, with zero T3 content. My §2 choreography mechanics implement exactly those T1 recipes (kind-dispatch on the resolved set, no per-builder branching). No conflict.
3. **S5 SHAPE/CONTENT line — ALIGNED to CHIRON's stricter mechanical test (the one substantive reconciliation).** I had loosely called `/run`+health the generic skeleton; CHIRON's §2 line is correct and stricter — `/run` is a **T3 domain verb**, the T1 CLI-client template ships a **`<VERB>` placeholder**, and the boundary test greps the entire T1 surface for ANY domain verb (incl. `/run`). I adopted it in §2 (S5 row) and §3.3 (DoD#5). My S5 mechanics stand up the scaffold + template with the placeholder; the grep is the DoD#5 §7 probe.
4. **HOME** — CHIRON proposes A-with-graduation-trigger, routes UP to Polybius_the_Stoa (+ Grand-escalation flag, since HOME binds 2.4's scienceclaw consume-path). My module is HOME-agnostic; I concur and add no constraint beyond "`provision/` stays an importable sub-package with the data tree reachable."
5. **stoa--jd5** — CHIRON's "move `data/` inside the package" recommendation resolves my HW-4 (above). PLINY owns the fold; lands this pass.

**Result: no overlap, no gap.** CHIRON owns *what tier each piece is + the SHAPE/CONTENT line + HOME + the emit/apply boundary*; I own *how each S-step runs + the mock substrate + the credential-acquisition UX*. Together we cover design-formal §4–§7 completely. Joint ready-signal posted to PLINY.

---

*Authored by MAJOR_HAMILTON_the-stoa (workflow-architect) | sid 0868c9cc | the-stoa | arc stoa--k48 — for fold into DAEDALUS's buildable formalization.*
