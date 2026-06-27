---
author: Denson Smith
ticket: stoa--k48 (u--9s2 Phase-2 increment 2.3 — provisioning choreography, ONE pass)
seat: MAJOR_CHIRON_the-stoa (team-architect) | sid 359bb256-a6ca-4322-9298-86eb8cf5d777
co-designer: MAJOR_HAMILTON_the-stoa (S0–S6 workflow mechanics + mock substrate)
authoritative-ground-truth: agents/design/stoa--jw5/design-formal.md §4 (S0–S6), §5.A/§5.B, §6, §7 (SHAPE-vs-CONTENT), §17.3 (tier placement), §27 (tier/ownership)
status: CHIRON design input — folded into the build; hands to PLINY for the DAEDALUS formalization
as_of: 2026-06-27
---

# CHIRON design — the provisioning-choreography OWNERSHIP / TIER model (S0–S6 + §7), the HOME proposal, and the emit-then-apply structure

This is the **WHO-OWNS-WHAT half** of the 2.3 design. HAMILTON owns the *mechanics* (how each
S-step runs, idempotently, fail-closed) and the *mock substrate* (how it is exercised without real
infra). I own the **ownership/tier structure** (what is T1 cookie-cutter built-here vs T3
project-seat-product NOT-built-here), the permanent **HOME** proposal, and the **emit-then-apply**
boundary that keeps credential values out of every agent's hands. Cast and choreography co-constrain;
the tier assignment below is the contract HAMILTON's workflow mechanics implement.

---

## 0. The one load-bearing insight (read first)

**The entire S0–S6 choreography is T1 cookie-cutter MECHANISM, parameterized by a T2-derived resolved
set, and it provisions a DOMAIN-EMPTY builder. ZERO T3 content is built in 2.3.** The only place T3
(the project-seat product — domain verbs + curated data) ever attaches is **AFTER S5**, onto the
secured-but-empty endpoint S5 stands up. The 2.3 boundary is therefore drawn cleanly at S5's hand-off:
*"a working, secured, mesh-reachable, domain-EMPTY endpoint + a client-skill skeleton with zero domain
verbs."* (design-formal §7.) Everything 2.3 builds is generic; nothing 2.3 builds is the product.

This is what makes the §7 SHAPE-vs-CONTENT boundary a *mechanical, testable* line rather than a
judgment call (§3 below).

### The tier vocabulary (from design-formal §17.3, §27 — used verbatim)

| Tier | What it is | Owner | Built in 2.3? |
|---|---|---|---|
| **T1** | cookie-cutter: generic, versioned, reused whole (the catalog, baseline, the resolver/generator/validator/SUGGEST code, the S0–S6 choreography, the §7 SHAPE scaffold + CLI-client TEMPLATE) | substrate / cookie-cutter | **YES — 2.3 is 100% T1** |
| **T2** | *derived*: the `{category, delta}` manifest + the resolved set + the emitted provisioning spec — a pure function of T3 inputs through T1 machinery, human-gated | derived (not authored) | the *machinery that derives it* is T1; the per-builder T2 instances are *emitted*, never hand-built |
| **T3** | the project seat's PRODUCT: which verbs the endpoint exposes, the curated data, the domain skill body, the per-skill `services:` declaration | the project seat | **NO — explicitly NOT built here (2.4+)** |

---

## 1. Per-step ownership/tier table (S0–S6)

For each step: **mechanism tier** (who owns the recipe), **parameterized-by** (what T2-derived input
drives the step), **T3 content?** (does any project-seat product attach here — the answer is *no*
until after S5), and the **value-handling** note (the credential-discipline seam).

| Step | Mechanism | Parameterized by (T2-derived) | T3 content here? | Value-handling |
|---|---|---|---|---|
| **S0** isolation scaffold (per-builder GCP project + bijective SA + budget boundary) | **T1** — generic recipe: derive SA name from slug, ensure project, set the §5.B budget boundary | builder slug; isolation UNIT (§5.B Branch A) | **none** — pure infra scaffold | the prepaid CARD (the §5.B hard cap) is **human-provisioned, out-of-band**; the agent emits the *requirement* (a card must back this project), never a card number |
| **S1** GCP API enablement (`kind==gcp_api`) | **T1** — recipe: `enable <api>` + grant SA the API role (idempotent) | the resolved `gcp_api` set | **none** | no secret value; SA role grant only |
| **S2** secret slot materialization (`kind ∈ {gcp_secret, thirdparty_rest_key}`) | **T1** — recipe: ensure SLOT + per-secret `secretAccessor`; **S2c human/credential-discipline GATE** | the resolved secret set | **none** | **THE SEAM.** Emit creates the slot NAME; **S2c BLOCKS** until a human populates the value (never improvised). Agent confirms *populated=true* (a boolean), never reads the value |
| **S3** Railway provisioning (`railway_var` + secret-backed vars) | **T1** — recipe: db service (baked-init image §6) + serving service (the **generic** trigger/serving skeleton); vars via **STDIN only**; **this builder's SA key ONLY** | the resolved `railway_var` set + secret-backed vars | **none** — the serving service is **domain-empty** at S3 (no verbs yet) | values flow human→keyring/secrets-mgr→CLI subprocess via STDIN; never agent stdout/argv/disk |
| **S4** DB extension application (`kind==db_extension`) | **T1** — recipe: baked-init emits the resolved `CREATE EXTENSION` lines (pgvector always; postgis iff resolved — §6) | the resolved `db_extension` set | **none** — extensions are *capability*, not domain schema; domain tables/data are T3 | n/a |
| **S5** agent-access layer (the §7 SHAPE) | **T1, FIXED, every builder** — the mesh-API scaffold + CLI-client TEMPLATE (§3 below) | nothing from the manifest (fixed scaffold) | **THE BOUNDARY** — S5 hands off a domain-EMPTY endpoint; T3 verbs attach *after* S5 (2.4+) | `TS_AUTHKEY` + `<BUILDER>_OPERATORS` are slots/vars, value-free at emit |
| **S6** verify (idempotent re-run = no-op + health probe) | **T1** — recipe: door preflight; assert resolved set PRESENT + runtime-completeness (§3.4) | the resolved set + live builder | **none** — verifies the generic scaffold + resolved infra; domain-verb verification is T3's own concern | reports `BLOCKED-on-human` for any unpopulated slot; never reads values |

**The pattern is uniform:** every S-step's *recipe* is T1; every S-step is *parameterized* by the
T2-derived resolved set (which itself descends from T3 `{category, delta}` declarations through the T1
catalog/resolver — design-formal §27 provenance through-line); and **no step carries T3 domain
content.** The choreography is a generic engine; the product is poured in later, by the project seat,
onto the empty shell S5 leaves behind.

---

## 2. The S5 / §7 SHAPE-vs-CONTENT boundary (the load-bearing line)

This is the boundary the directive calls load-bearing and the one ARGUS/CATO pressure-test. Stated as
an ownership contract:

### T1 — cookie-cutter owns the SHAPE (generic, identical per builder, BUILT HERE)
- mesh-API scaffold: `tailscaled` → `tailscale serve --https=443` → a **0600 AF_UNIX socket** → the
  in-mesh trigger (loopback/UDS only);
- identity = the serve-injected `Tailscale-User-Login` header (**never** WhoIs-on-loopback —
  newswire landmine §6.1);
- **deny-by-default** Tailscale policy; the `<BUILDER>_OPERATORS` env var + `group:operators`
  allowlist double-check; **Funnel OFF** (no public ingress);
- the **CLI-client-skill TEMPLATE** (`newswire-trigger`-shaped, but verb-PARAMETERIZED): trigger
  over the mesh with **only a tailnet identity**, a `--check` door-probe, a counts-only response
  contract, a redacted-error tail. **The template ships a placeholder verb, not `/run`.**

### T3 — project seat owns the CONTENT (specific, the product, NOT BUILT HERE)
- **which verbs** the endpoint exposes (newswire `/run` = collect+embed; scienceclaw = ingest+search);
- the curated **data**; the **domain skill body** that fills the CLI-client template's placeholder.

### The boundary-violation test (mechanical — for ARGUS/CATO, and the DoD #5 §7 boundary probe)
> **grep the entire T1 cookie-cutter for any domain verb.** If a concrete domain verb (`/run`,
> `collect`, `embed`, `ingest`, `search`, or any builder-specific endpoint name) appears anywhere in
> the T1 SHAPE scaffold or the CLI-client TEMPLATE, the cookie-cutter has stopped being generic —
> that is the leak. The template must carry a **placeholder/parameter** (e.g. `<VERB>` /
> `OPERATOR_VERB`), filled only by T3.

This converts "is it generic?" from a judgment into a `grep`-checkable assertion. The newswire reuse
source (`newswire-builder-setup`) is the *worked instance* with `/run` baked in; the 2.3 generalization
is precisely the act of **extracting the verb to a parameter** so the SHAPE survives without the CONTENT.

---

## 3. The emit-then-apply structure (agents never hold credential values)

The choreography splits into two halves at a hard credential seam. **The split is also what makes the
TRIPWIRE structurally honorable** (HAMILTON's mock-substrate lane): 2.3 exercises only the EMIT half;
the APPLY half is *designed but never run* against real infra (that is 2.4).

### EMIT — T1, pure, offline, agent-runnable, VALUE-FREE
- `builder-deploy emit <manifest>` → a **provisioning SPEC** artifact enumerating, per resolved entry
  (kind-dispatched §3.3): the operation (enable API / create secret SLOT / set railway var / create
  extension), the **slot NAME**, the SA-scope grant, and the budget-boundary *requirement*.
- The spec is a **pure function of the resolved set** — same property as the 2.1 resolver: deterministic,
  no environment, no network. **It contains slot NAMES only — grep-provable zero credential values**
  (DoD #3). This half is what an AGENT runs.

### APPLY — credential-disciplined, NOT agent-value-holding
Consumes the emitted spec; executes the credential-bearing steps. Two applier modes (both from the
existing skills — reuse, not reinvention):
- **CI-via-WIF** (`credential-discipline` skill, in-repo): GitHub Actions authenticates via Workload
  Identity Federation (no static SA key); a per-service PAT (Railway) lives in GHA encrypted secrets,
  decrypted only at workflow runtime.
- **Human one-shot local** (`railway-keyring-deploy` skill, user-tier): secrets live in the OS keyring;
  read into the CLI subprocess via **ENV** (the token) / **STDIN** (per-service secrets) — never agent
  stdout / argv / transcript / disk.

### The S2c gate is the structural seam
The emit step produces a spec with **unpopulated slots**; the apply step **BLOCKS at S2c** until a
human populates each slot. Population uses the human-in-the-loop credential-acquisition choreography
(HAMILTON's detailed lane): the agent drives a browser to the dashboard edge → a clickable link opens
that dashboard in a browser **the agent cannot see** → the human generates the secret **privately** →
the agent helps deploy via the keyring paste-script / Railway-CLI / Railway-UI pattern. **The agent
confirms `populated=true` (a boolean); it never sees the value.**

### The credential-discipline attestation (the §3-relay-up deliverable, structural form)
1. **Value-free emit** — the emitted spec contains slot names only; grep-provable (DoD #3).
2. **No agent ever holds a credential value** — values flow human → keyring/secrets-mgr → CLI
   subprocess, bypassing every agent's context entirely.
3. **The applier reads values from keyring/WIF**, never from the spec or from an agent.
4. **Per-builder GCP project + prepaid card = the hard spend cap** (§5.B, out-of-band, human-provisioned);
   the GCP-native alert/quota/killswitch menu is the *soft* defense-in-depth layer under the card.

### Why this is the strongest TRIPWIRE form (HAMILTON co-lane)
The mock substrate runs **emit-only mode**: it emits specs against mock resolved sets (the §8 worked
examples), touching zero real infra. The APPLY half's real `gcloud`/`railway`/card calls are **not on
the test path at all** — the test exercises a pure function, so real-infra reach is *structurally
impossible*, not merely *policed*. HAMILTON formalizes the mock layer; the emit/apply split is the
structural property that lets her make the impossibility total.

---

## 4. The permanent builder-deploy skill HOME — PROPOSAL (routes UP; NOT baked)

**Decision (stoa--wmu, deferred from 2.1):** Option A *the-stoa forge-owned home* vs Option B
*standalone builder-tooling location*. A near consumer now exists (scienceclaw at 2.4). Per my brief I
**PROPOSE**; **Polybius_the_Stoa ratifies**; escalate to Grand if load-bearing. I do **not** bake it.

### Recommendation: **Option A now (the-stoa forge-owned, in `substrate/skills/`), with an explicit, documented GRADUATION TRIGGER to B.**

**Why A now:**
1. **B's home does not yet exist; A's does.** Standing up a separate repo + release pipeline for a
   *single* near-consumer (scienceclaw) is premature — the decision-register itself flagged "B stands
   up a home for a consumer that does not yet exist."
2. **A rides the existing arc + install.sh + full-gauntlet lifecycle** — exactly the quality machinery
   this credential-sensitive tooling needs. B would have to re-create that from scratch.
3. **Zero rework penalty for deferring B.** The stoa--wmu premise is that the package layout is
   HOME-independent by construction, so A→B graduation stays an **additive `git mv` + consume-path
   update** whether done now or in a year. Choosing A does not foreclose B.
4. **the-stoa IS the forge.** The substrate's identity is "a recursive agent architecture that builds
   things." The builder-deploy cookie-cutter is the flagship product OF that forge; co-locating it with
   the forge maximizes discoverability while the consumer population is tiny.
5. **It makes the stoa--jd5 packaging fix tractable now** (§5 below) under the substrate-skill deploy
   convention, without committing to a PyPI release story.

**The honest tension (the reason this routes UP, and may warrant Grand):** the builder-deploy product
ultimately serves builders that are **not the-stoa consumers**. A scienceclaw operator should not have
to install the whole the-stoa substrate to get the skill. If the consumer population grows beyond
the-stoa's orbit, **B becomes correct.** Hence the recommendation is A-*with-a-trigger*, not A-forever.

**Proposed GRADUATION TRIGGER (A → B):** graduate to a standalone home when **either** (a) a *second*
non-the-stoa consumer appears, **or** (b) builder-deploy's release cadence needs to diverge from the
substrate's. The move is the additive `git mv` the stoa--wmu premise already counts on.

**Escalation question for Polybius_the_Stoa:** because the HOME choice binds **2.4's real scienceclaw
deploy/consume path** (scienceclaw consumes the skill from wherever HOME is), this is plausibly
load-bearing for the next increment. I recommend Polybius_the_Stoa **ratify A-with-trigger and confirm
with Grand** if Grand considers the 2.4 consume-path binding to be a Grand-gate concern. I surface the
question; I do not decide the escalation.

---

## 5. stoa--jd5 fold (the packaging prerequisite) — recommendation consistent with HOME-A

**The bug (stoa--pj3 CATO c2):** `agents/builder-deploy-core/pyproject.toml:31` declares package-data
as `builder_deploy_core = ["../data/**/*.toml"]` — a **parent-relative glob setuptools will not
honor**, so a `pip install` would not bundle the `data/` tree. In-tree execution works today
(`dataload.py` uses `Path(__file__).parent.parent/data`), which is why it was non-blocking for 2.1.

**Recommended fix (HOME-independent — correct under both A and B):** **move `data/` INSIDE the
importable package** → `builder_deploy_core/data/`, so package-data becomes a normal *intra-package*
glob (`data/**/*.toml` relative to the package) that setuptools honors. `dataload.py` changes from
`Path(__file__).parent.parent/data` to `Path(__file__).parent/data`. Add an **install-then-import smoke
test** (the test CATO's c2 plan named) so the packaging property is regression-guarded.

This fix is **owned by PLINY's build** (NOMOS routed stoa--jd5 fold → PLINY) — I supply the
recommendation, not the edit. It is HOME-independent, so it does not block the HOME ratification; it
just needs to land in the same pass (DoD #8).

---

## 6. Co-design interface with HAMILTON (cast ⟷ choreography contract)

What my tier model HANDS HAMILTON (constraints her S0–S6 mechanics honor):
- **Every S-step recipe is T1** — generic, no per-builder branching beyond kind-dispatch on the
  resolved set. HAMILTON's idempotent/fail-closed mechanics implement T1 recipes.
- **The emit/apply seam is the structural boundary** (§3) — HAMILTON's mock substrate runs emit-only;
  the apply half is designed-not-run. The seam location (S2c block; spec = slot names only) is fixed
  by this design.
- **S5 hands off a domain-EMPTY endpoint** — HAMILTON's S5 mechanics stand up the SHAPE scaffold +
  CLI-client TEMPLATE with a verb PLACEHOLDER; no domain verb anywhere in T1.

What HAMILTON HANDS me (informs the ownership model):
- the mock-substrate shape (emit-only) confirms the EMIT half is the agent-runnable, value-free T1
  surface — which is what lets me assert "2.3 is 100% T1, zero T3."
- the credential-acquisition UX detail (browser-to-edge → unseen-browser → keyring deploy-help) is the
  APPLY-half mechanism behind my S2c seam.

**No overlap, no gap:** I own *what tier each piece is + the SHAPE/CONTENT line + HOME + the emit/apply
boundary*; HAMILTON owns *how each step runs + the mock substrate + the credential-acquisition UX*.
Together they cover design-formal §4–§7 completely.

---

## 7. What I hand PLINY (for the DAEDALUS formalization)

DAEDALUS formalizes THIS (ownership/tier) + HAMILTON's (mechanics + mock) into the single buildable
spec. The fixed points DAEDALUS must preserve:
1. **2.3 builds 100% T1; zero T3** — the choreography is generic; the product is not built here.
2. **The S5/§7 boundary-violation test is `grep`-mechanical** (§2) — it becomes DoD #5's §7 probe.
3. **The emit/apply seam** (§3) — value-free emit (grep-provable, DoD #3); credential-disciplined
   applier; S2c block; emit-only mock path = the structural TRIPWIRE (DoD #6).
4. **HOME = A-with-graduation-trigger** *pending Polybius_the_Stoa ratification* (§4) — DAEDALUS
   should formalize against `substrate/skills/builder-deploy` as the home **iff** ratified; otherwise
   hold the package at its decision-neutral `agents/builder-deploy-core` location.
5. **stoa--jd5 fix = move `data/` into the package** (§5) — HOME-independent, lands this pass.

**Routes UP (not baked):** the HOME proposal (§4) → PLINY → FM → Polybius_the_Stoa to ratify, with the
Grand-escalation question flagged.
