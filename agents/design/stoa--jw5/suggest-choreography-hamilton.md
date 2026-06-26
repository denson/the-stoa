# Part 3 — HAMILTON lens: the SUGGEST→confirm→DECLARE choreography + human-confirm gate

**Seat:** MAJOR_HAMILTON_the-stoa (workflow-architect). **Arc:** stoa--jw5 / u--9s2 Phase-1 revision —
the SUGGEST-pillar increment. **For fold into** the unified `suggest-codesign.md` (CHIRON sole writer)
as **§3** (the SUGGEST step) and **§4** (the human-confirm fail-closed gate).
**Shared contract:** CHIRON's catalog + its `detection_hints` (`suggest-codesign.md` §1) — my
examination matches against those hints; the catalog is the candidate-service space.

> **§2 LOAD-BEARING CONSTRAINT (held absolutely).** The gated mechanism is the FULL **§0–§23** of
> design-formal.md (Part-1 resolver/provisioning/§8/maps + Part-2 catalog §17 / DECLARE §18 /
> generation G1–G4 §19 / validation V1–V5 §20 / reframe §21) — **ALL STANDS UNCHANGED**. SUGGEST is
> **strictly UPSTREAM of DECLARE (§18)**: it changes only how the DECLARE `services:` set is
> **PRODUCED** (hand-authored → agent-suggested + human-confirmed). The confirmed set IS the §18
> input the downstream already consumes. The §8 fixtures (8/6/7) are a **REGRESSION TARGET**. No part
> of this pressures `resolve()`/§8/§0–§23 — nothing to dilemma-classify.

```
SUGGEST (agent EXAMINES project → MATCHES detection_hints → PROPOSES service set)   [§3]
   → human-CONFIRM gate (confirm / edit / reject — FAIL-CLOSED)                      [§4]
   → confirmed set IS the DECLARE set  → §18 DECLARE [UNCHANGED] → §19 generate [UNCHANGED]
        → §20 validate V1–V5 [UNCHANGED] → §4 resolve() [UNCHANGED] → provision
```

---

## §3 — The SUGGEST step: examine → match → propose

The SUGGEST agent (a T1 capability, CHIRON §2) turns **"what the project is actually doing"** into a
**proposed** service set, by matching the project against the catalog's `detection_hints` (§1). It runs
in three sub-steps; its output is a **recommendation with evidence**, never a declaration.

```
SUGGEST(project, catalog):
  S-1  EXAMINE — read the project across four signal surfaces (web-verified neuro-symbolic shape, §3.1):
         (i)   manifests / config        — package.json, requirements.txt, pyproject, go.mod,
                                            docker-compose, k8s manifests, .env(.example)   → sdk_imports, config_keys
         (ii)  code outbound-call sites  — SDK init, HTTP clients (fetch/axios/requests/gRPC),
                                            custom wrappers, dynamically-built endpoints       → sdk_imports, url_patterns
         (iii) data-flows / resources    — file types, data kinds (e.g. spatial data), sinks    → data_signals
         (iv)  intent docs               — README / onboarding / OpenAPI / inline docs (a prior to
                                            reconcile against the code signals)                 → cross-check
  S-2  MATCH — for each examined signal, match against CATALOG[*].detection_hints → candidate service-id.
         CANDIDATE SPACE = the catalog (CHIRON §1.2): only a CATALOGED service can be proposed.
         An examined external-service signal with NO catalog match → surface "unknown service <signal>"
         to the human (add-to-catalog path; the §20 V1 "every-service-cataloged" lineage, one layer up).
  S-3  PROPOSE — emit { candidate-services, per-candidate EVIDENCE (which signal matched which hint) }.
         The evidence is what lets the human adjudicate (§4). The proposal is a RECOMMENDATION ONLY —
         it is NOT a DECLARE set and has NO downstream effect until the human-confirm gate (§4) passes.
```

### §3.1 — Honest capability scope (web-verified; usefulness, NOT safety — FM watch-item 2)

The premise "an agent can examine a project and propose a plausible service set" is **web-verified**
(gsearch, current docs 2026-06-26 — not asserted from memory): 2026 agents do this via a
**neuro-symbolic** flow (manifest/config parse + AST/CPG outbound-call analysis + LLM semantic
resolution of dynamically-constructed endpoints + README/OpenAPI reconciliation), and they
**outperform classical static scanners** exactly on the DWP-3 cases — custom wrappers, evolving APIs,
and `${env.GATEWAY_URL}`-style dynamically-built endpoints that declaration-from-memory and pure
static scan miss. **That is the SUGGEST win.**

But the same sources are explicit that agent inference is **probabilistic, not authoritative**, with
documented failure modes the design must NOT paper over:
- **over-proposal** — pattern-completer **hallucination** (a `/billing` dir or a mock class →
  confidently "Stripe"/"Auth0" though nothing real is wired);
- **under-proposal** — **dynamic resolution** (service-mesh / reflection / metaprogramming) and
  **dead/legacy code** (no reachability proof) → real or phantom services mis-judged;
- **ambiguity** — **mock-vs-active** branches, **internal-microservice-vs-external-SaaS**, and
  **config-placeholder** endpoints that only operational context resolves.

**Therefore the capability is a USEFULNESS claim, not a safety one.** It governs how much SUGGEST
reduces human effort and how many DWP-3 cases it catches — *not* whether the system is safe. **Safety
rests entirely on the §4 human-confirm gate + the unchanged fail-closed V1–V5**, which is precisely the
**human-in-the-loop sign-off the industry treats as essential** for agent-proposed inventories (the
same HITL requirement that governs SBOM/SaaSBOM inventories). The agent's **inference accuracy is
Phase-2 implementation**; Phase-1 specifies only the SHAPE. We do **not** claim suggest completeness:
residual gaps are caught by human-confirm (§4) + the §18 SCAN-drift validator + the Phase-2
runtime-observer.

---

## §4 — The human-confirm FAIL-CLOSED gate (FM watch-item 1, load-bearing)

The gate is the **only** edge from PROPOSE → DECLARE. It is **fail-closed**: a proposal becomes a
DECLARE set **iff** a human ratifies it.

```
CONFIRM(proposal):
  C-1  PRESENT the proposed service set + per-candidate evidence (§3 S-3) to the human (project seat / operator).
  C-2  the human acts:  CONFIRM (accept as-is)  |  EDIT (add / remove services, then confirm)  |  REJECT / no-response.
  C-3  ONLY a CONFIRMED (possibly EDITED) set becomes the DECLARE set.
       The PROPOSE→DECLARE edge passes through C-2 EXCLUSIVELY — there is NO auto-promotion path.
  C-4  FAIL-CLOSED:  REJECT / no-response / edits-pending  ⇒  NO DECLARE set produced
                     ⇒ NO §18 input ⇒ NO §19 generation ⇒ NO resolved set ⇒ NOTHING provisions.
       An unconfirmed proposal is INERT — it never reaches the downstream.
  C-5  FEED: the confirmed set IS the §18 DECLARE `services:` set — the existing generation's
       authoritative input, UNCHANGED. §18–§23 (DECLARE / SCAN / G1–G4 / V1–V5 / resolve) run exactly
       as today on the confirmed DECLARE. SUGGEST adds NO downstream change and weakens NO V1–V5 check.
```

**Why fail-closed + HITL is the safety mechanism (not gold-plating):** the §3.1 failure modes
(hallucinated over-proposal, dynamic/dead-code under-proposal, mock-vs-active & internal-vs-external
ambiguity, config-placeholders) are exactly the cases the web-verified sources say **only a human with
operational context can adjudicate**. The gate converts the agent's probabilistic proposal into a
human-authoritative declaration:
- **over-proposal is caught** — the human REMOVES a hallucinated service before confirming → no scope
  bloat (and provisioning never runs off an unconfirmed entry anyway, CHIRON §1.3: a wrong hint can
  only mis-propose, never mis-provision);
- **under-proposal is caught** — the human ADDS a service the agent missed → no under-provisioning;
- **everything downstream is unchanged** — V1–V5 still run on whatever DECLARE the human confirms (V2
  anti-under-provision, V4 §3.4 runtime-completeness, V1 every-cataloged), so the SUGGEST front-door
  cannot weaken the proven guarantees; it only changes how the DECLARE it gates is produced.

The gate is the structural expression of FM watch-item 2's frame: **safety = this gate, not the
agent's accuracy.** It is symmetric with the existing fail-closed posture (§20 V1–V5, §5 S2c human
secret gate, §2.6 BaselineOmitError) — an ill-formed/unratified input never enters provisioning.

---

## §5 — The three worked examples via SUGGEST (regression target 8 / 6 / 7; matches CHIRON §6)

Each: agent **examines** → matches `detection_hints` → **proposes** (with evidence) → human **confirms**
→ the **same DECLARE set** Part-2 already validated → unchanged §18–§4 → 8/6/7.

**prospector** (geo project: renders a client-side map; runs spatial queries)
```
EXAMINE → MATCH: Maps-JS sdk_import + maps URL pattern → google-maps ;  spatial-data data_signal → spatial-db
PROPOSE [google-maps, spatial-db] (+evidence) → human CONFIRM → DECLARE [google-maps, spatial-db]
   → (UNCHANGED) {category: geospatial, delta:{}} → resolve() = 8   ✓ §8.1
```
**scienceclaw** (doc-consuming project)
```
EXAMINE → MATCH: document-parsing sdk_import/URL → document-parsing
PROPOSE [document-parsing] → CONFIRM → DECLARE [document-parsing] → {document-consuming, {}} → 6   ✓ §8.2
```
**labstat_bls** (doc/data project calling a BLS OEWS REST endpoint — the load-bearing DWP-3 case)
```
EXAMINE → MATCH: document-parsing → document-parsing ;  BLS-OEWS url_pattern/config_key → bls-oews
   (the agent INFERS bls-oews from the BLS URL/config signal — a service declaration-from-memory could miss)
PROPOSE [document-parsing, bls-oews] (+evidence) → human CONFIRM → DECLARE [document-parsing, bls-oews]
   → {document-consuming, delta.add:[thirdparty_rest_key:BLS_OEWS_API_KEY]} → resolve() = 7   ✓ §8.3
```
✓ **The DWP-3 upgrade demonstrated:** the agent *infers* `bls-oews` from a URL/config signal (then the
human confirms), surfacing a service that declaration-from-memory might have missed — while the
downstream is untouched and 8/6/7 is HIT, not re-derived.

**FAIL-CLOSED no-confirm branch (FM watch-item 1):**
```
agent PROPOSES [google-maps, spatial-db]  →  human does NOT confirm (reject / pending / no response)
   →  NO DECLARE set  →  NO §18 input  →  NO §19 generation  →  NO resolved set  →  NOTHING provisions   [INERT]
```
(Human EDITS instead — add/remove a service then confirm — and the EDITED-confirmed set becomes DECLARE;
same gate, the human's ratified set is authoritative.)

---

## §6 — §2 compliance + the seam with CHIRON

- **§2 held:** §3/§4 are purely upstream of §18 DECLARE; the gated §0–§23 mechanism is textually
  unchanged; the confirmed set is exactly the `services:` shape §18 already consumes; 8/6/7 is a
  regression target hit, not re-derived. No pressure on `resolve()`/§8 → no dilemma to classify.
- **Seam with CHIRON (the shared catalog + detection_hints):** my S-2 MATCH reads CHIRON's §1
  `detection_hints`; my candidate space is bounded by his catalog (§1.2); CHIRON's load-bearing
  advisory-vs-recipe distinction (§1.3) is what makes my gate's "remove a hallucinated service" safe
  (a wrong hint only mis-proposes; provisioning runs off the confirmed service's §17 `entries`). The
  §3.4 paired-credential rule rides in the catalog entry, so a confirmed service carries its full
  entry set (incl. MAPS_API_KEY) into the unchanged generation — prospector still = 8.
- **Co-constraint to confirm with CHIRON:** the `detection_hints` field names I match in S-1/S-2
  (`sdk_imports`, `url_patterns`, `config_keys`, `data_signals`) are exactly his §1 structure — so my
  examination surfaces (i)–(iv) map 1:1 onto his four hint kinds. Confirmed if §1 is unchanged.

## §7 — DoD coverage (my half — Part-3 §5 / brief)

- [x] SUGGEST step specified: examine (4 web-verified neuro-symbolic surfaces) → match detection_hints
      → propose with evidence; candidate space bounded by the catalog — §3
- [x] capability premise web-verified (gsearch, current docs) + framed as USEFULNESS not safety;
      failure modes named; accuracy = Phase-2; no over-claim of completeness — §3.1
- [x] human-confirm FAIL-CLOSED gate: only a confirmed/edited set becomes DECLARE; no-confirm ⇒ inert
      ⇒ nothing provisions; feeds §18 unchanged; does not weaken V1–V5 — §4
- [x] 3 worked examples via SUGGEST → 8/6/7 (incl. labstat_bls bls-oews inference) + the fail-closed
      no-confirm branch — §5
- [x] §0–§23 confirmed UNCHANGED; SUGGEST purely upstream of DECLARE — §6
- [ ] CHIRON folds §3/§4 into the unified `suggest-codesign.md` (sole writer)
- [ ] targeted gauntlet on the addition (DAEDALUS formalize into design-formal.md §24+, gated §0–§23
      untouched → ARGUS → ADA exercise the front-door + regression-confirm 8/6/7 → VERA → CATO → NOMOS)
