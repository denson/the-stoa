# SUGGEST CO-DESIGN — stoa--jw5 (u--9s2 Phase-1 revision): the SUGGEST-pillar discovery front-door

**Arc:** stoa--jw5 / u--9s2 Phase-1 revision — the SUGGEST-pillar increment (CONDITION 2 of the
Grand's Part-2 gate). **Status:** CHIRON half authored; HAMILTON choreography half pending fold.

**Co-authors (complementary lenses, shared contract = the CATALOG + its detection hints):**
- **MAJOR_CHIRON** — per-service **detection-hint** catalog fields + the SUGGEST-step **tier/ownership**
  + confirm-gate **placement** (this file; sole writer). §1, §2, §6 (catalog/example-mapping).
- **MAJOR_HAMILTON** — the **SUGGEST→confirm→DECLARE choreography** + the **human-confirm fail-closed
  gate** + the examination flow (what/how the agent reads). To be drafted to
  `suggest-choreography-hamilton.md` (flat sibling) and folded here as §3, §4.
- **Next:** DAEDALUS formalizes the SUGGEST front-door INTO `design-formal.md` as new sections (gated
  §0–§23 mechanism UNTOUCHED); targeted gauntlet hardens; resolver/generation/validation = regression-confirm only.

> **PROCESS NOTE (CHIRON):** authored on the obvious sole-writer-new-file default to honor the Grand's
> GO + the no-delay mandate rather than block on a file-naming round-trip. PLINY may redirect (this
> file vs a fold into `discovery-codesign.md`) — trivial to move; the content stands either way.

---

## §2 — THE LOAD-BEARING CONSTRAINT (stated first, held absolutely)

The gated mechanism is now the **FULL §0–§23** of design-formal.md (Part-1 resolver §2 set-algebra +
provisioning S0-S6 + §8 fixtures + §11 fork + §12.A maps; Part-2 catalog §17 + DECLARE/SCAN discovery
§18 + generation G1-G4 §19 + validation V1-V5 §20 + emergent reframe §21) — **ALL STANDS UNCHANGED**.
The SUGGEST pillar is **strictly UPSTREAM of DECLARE (§18)** — it changes only how the **DECLARE set
is PRODUCED** (from hand-authored to agent-suggested + human-confirmed); it produces the confirmed
`services:` set that §18 already treats as generation's authoritative input. **DECLARE/§18-§23 remain
unchanged.** DAEDALUS formalizes the SUGGEST front-door as NEW sections **§24+** (gated §0–§23 untouched). The §8
fixtures (prospector 8 / scienceclaw 6 / labstat_bls 7) are a **REGRESSION TARGET** that must still
be hit. If any reframe pressured DECLARE-as-generation-input, `resolve()`, or the §8 sets, that is a
scope breach → STOP + dilemma-classify. **Nothing here does.**

```
SUGGEST (agent examines project → proposes service set)
   → human CONFIRMS (fail-closed gate)
   → the confirmed set IS the DECLARE set            [DECLARE pillar, UNCHANGED downstream]
   → SCAN validates drift  → [Phase-2] runtime-observer
   → generation G1-G4 [UNCHANGED] → validation V1-V5 [UNCHANGED] → resolve() [§4 UNCHANGED] → provision
```

---

## §0 — Frame: SUGGEST inverts the declare-primary front-door (the DWP-3 upgrade)

Part-2's discovery made **DECLARE authoritative** but leaned on a human/skill-author to **remember**
every service called — the **DWP-3 gap** (a service reached via runtime-config / dynamic / indirect
paths is invisible to declaration-from-memory *and* static scan). The SUGGEST pillar **inverts** the
front-door: an **agent EXAMINES what the project is actually doing** (purpose, code, data-flows,
intended behavior) and **PROPOSES** the service set; a **human CONFIRMS**; the confirmed suggestion
**BECOMES the DECLARE set.** The agent does the figuring-out "as we go"; the human ratifies.
**Human-in-the-loop at suggest→confirm is the FEATURE, not a gap** — it makes suggest-agent
imperfection safe. This is the DWP-3 **Phase-1 upgrade**: an agent reading the project can infer
services that declaration-from-memory + static scan both miss; the human gate catches over/under-proposal.

---

## §1 — CHIRON: per-service DETECTION-HINT catalog fields (additive, T1)

The SUGGEST agent needs a way to map **"what the project is doing"** → **candidate catalog services**.
The catalog (the T1 service→key structure from Part-2 §17) gains an **additive, per-service
`detection_hints` field** — the recognizable signals the agent matches against the examined project:

```yaml
- service-id: <id>
  entries: [ ... ]            # (Part-2) typed §3 entries
  gcp_api: <...> ; category: <...>
  detection_hints:            # NEW (CHIRON): signals the SUGGEST agent matches against the project
    sdk_imports:   [ <library / SDK / package names that indicate this service> ]
    url_patterns:  [ <hostname / endpoint / API-base-URL patterns the service is called at> ]
    config_keys:   [ <env-var / config-key name patterns this service reads> ]
    data_signals:  [ <data-flow / file-type / resource signals, e.g. spatial-data → a geo service> ]
```

**ADVISORY HINTS, DISTINCT FROM THE HARD RECIPE (the load-bearing distinction).** `detection_hints`
are **advisory inference signals** the SUGGEST agent uses to RECOGNIZE a service in the project — they
are **NOT** the service's provisioning recipe. The hard recipe is the service's **`entries`** (the
typed §17 entries: the actual keys/APIs/extensions to provision) — **unchanged, authoritative,
untouched by this increment.** A hint can be wrong or missing with **zero** effect on what gets
provisioned: hints only feed the *agent's proposal*; the human confirms; and provisioning still runs
off the confirmed service's **`entries`**. So a sloppy hint cannot mis-provision — it can only
mis-*propose*, which the human-confirm gate catches.

**Properties (the catalog-side contract):**
1. **Additive + open-closed.** `detection_hints` is a new optional field on the existing record;
   adding a service includes its hints. The SUGGEST agent and the generation are **hint-agnostic** —
   they consume the catalog; only the agent's *matching pass* reads `detection_hints`. Existing
   records + the resolver + generation are unchanged.
2. **The catalog is the candidate-service SPACE.** The SUGGEST agent proposes only services that
   EXIST in the catalog (an uncataloged signal → "unknown service, add to catalog" — same V1
   lineage). So the catalog bounds what can be suggested; the hints are how the agent recognizes them.
3. **Honest scope (FM watch-item 2).** `detection_hints` are *signals*, not a guarantee — they raise
   the agent's recall (catching runtime-config/indirect cases static-scan misses) but do NOT promise
   completeness. The **human-confirm gate** is what makes hint imperfection safe (§3/§4). The hints'
   data is **Phase-2** (this is SHAPE-only); the field STRUCTURE is the Phase-1 deliverable.
4. **Runtime-completeness preserved.** A hint maps to a service; the service's *entries* (incl. the
   §3.4 paired credential, e.g. google-maps ⇒ MAPS_API_KEY) come from the existing record — so a
   confirmed suggestion still carries the full entry set into the unchanged generation.

---

## §2 — CHIRON: tier / ownership of the SUGGEST front-door

| Element | Tier | Owner | Note |
|---|---|---|---|
| The **SUGGEST agent** (examines → proposes) | **T1** | cookie-cutter capability | generic; any builder can run it; reads the T1 catalog(+hints) |
| `detection_hints` catalog fields | **T1** | cookie-cutter | additive; arc-reviewed (R-3 catalog-integrity lineage applies) |
| What the agent **examines** (project purpose/code/data-flows) | **T3** | the project (its product) | the agent reads the project's actual behavior |
| The **human-confirm gate** | human-in-the-loop | the project seat's human / operator | the fail-closed ratification (§3/§4) — the FEATURE |
| The **confirmed DECLARE set** | **T2** | derived (agent-suggested + human-confirmed) | the per-builder declaration, no longer hand-remembered |

**Provenance shift (the through-line):** Part-1 = hand-authored manifest. Part-2 = manifest *derived
from* T3 `services:` declarations through the T1 catalog. **SUGGEST = the declarations themselves are
agent-proposed + human-ratified**, not hand-remembered — closing more of DWP-3 while keeping the
manifest a derived, human-gated artifact. The tier model is preserved throughout; each step pushes
the manifest's provenance one notch further from "a human remembered" toward "derived + ratified."

---

## §3 — HAMILTON (to fold): the SUGGEST→confirm→DECLARE choreography

*[PENDING FOLD from `suggest-choreography-hamilton.md`. HAMILTON owns: how the agent EXAMINES the
project (purpose/code/data-flows/behavior) and PROPOSES a service set by matching the §1
`detection_hints`; the human-CONFIRM gate; how the confirmed set BECOMES the DECLARE that the existing
generation consumes. CHIRON folds it here verbatim-faithful as sole writer.]*

---

## §4 — HAMILTON (to fold): the human-confirm FAIL-CLOSED gate (FM watch-item 1)

*[PENDING FOLD. The load-bearing safety property: **no human confirmation ⇒ NO DECLARE set ⇒ NO
generation / NO provision.** An unconfirmed suggestion must NOT silently become DECLARE. This must
not weaken the existing fail-closed V1–V5. HAMILTON specifies the gate's mechanics; CHIRON folds.]*

---

## §5 — FM watch-items, addressed

1. **Human-confirm gate = FAIL-CLOSED** (HAMILTON §4): an unconfirmed suggestion never becomes
   DECLARE, never reaches generation/provision. Human-in-the-loop is the FEATURE; it makes
   suggest-agent error safe and does not weaken V1–V5.
2. **Honest capability scope — the capability claim is a USEFULNESS claim, NOT a safety-load-bearing
   one** (CHIRON §1.3 + HAMILTON §3). **Safety rests on the human-confirm gate (§4), not on the
   agent's accuracy.** The agent-inference capability ("an agent can examine a project and propose a
   plausible service set") only determines how *useful* SUGGEST is (how much it reduces human effort /
   catches the DWP-3 runtime-config cases) — it is **not** load-bearing for safety, because an
   imperfect proposal is caught by the human gate and the unchanged fail-closed V1–V5. So the design
   must **not over-claim suggest completeness**: `detection_hints` raise recall; residual gaps are
   covered by human-confirm + SCAN-drift + the Phase-2 runtime-observer; the agent's inference
   accuracy is **Phase-2 implementation**, not a Phase-1 claim. *[HAMILTON: web-verify any load-bearing
   capability premise in your examination flow (gsearch / current docs, not memory) — and frame it as
   usefulness, not safety.]*

---

## §6 — The three worked examples through SUGGEST (regression target: 8 / 6 / 7)

Each shows: agent examines → matches `detection_hints` → proposes → human confirms → **the same
DECLARE set** Part-2 already validated → unchanged generation → 8/6/7.

**prospector** — agent examines a geo project (renders a client-side map; runs spatial queries):
```
matches: Maps-JS sdk_import / maps URL pattern → google-maps ; spatial-data data_signal → spatial-db
PROPOSES [google-maps, spatial-db] → human CONFIRMS → DECLARE [google-maps, spatial-db]
→ (Part-2 generation, UNCHANGED) {category: geospatial, delta:{}} → resolve() = 8   ✓ §8.1
```
**scienceclaw** — agent examines a doc-consuming project:
```
matches: document-parsing sdk_import/URL → document-parsing
PROPOSES [document-parsing] → CONFIRMS → DECLARE [document-parsing] → {document-consuming, delta:{}} → 6  ✓ §8.2
```
**labstat_bls** — agent examines a doc/data project calling a BLS REST endpoint (the DWP-3-class case
declaration-from-memory might miss; the agent infers it from the BLS URL/config signal):
```
matches: document-parsing → document-parsing ; BLS-OEWS url_pattern/config_key → bls-oews
PROPOSES [document-parsing, bls-oews] → CONFIRMS → DECLARE [document-parsing, bls-oews]
→ {document-consuming, delta.add:[thirdparty_rest_key:BLS_OEWS_API_KEY]} → resolve() = 7   ✓ §8.3
```
✓ **The SUGGEST front-door produces the SAME DECLARE sets the gauntlet already validated** — the
downstream generation/validation/resolver are untouched; 8/6/7 is HIT, not re-derived. labstat_bls is
again load-bearing: the agent *inferring* bls-oews from a URL/config signal (then human-confirmed) is
exactly the DWP-3 upgrade — a service declaration-from-memory could have missed is now proposed.

**THE FAIL-CLOSED NO-CONFIRM BRANCH (FM watch-item 1).** The same prospector proposal, human does NOT confirm:
```
agent PROPOSES [google-maps, spatial-db]  →  human does NOT confirm (rejects / edits-pending / no response)
  →  NO DECLARE set produced            (the proposal is NOT silently promoted to DECLARE)
  →  NO §18 input  →  NO generation  →  NO resolved set  →  NOTHING provisions     [FAIL-CLOSED]
```
An unconfirmed suggestion is **inert** — it never becomes DECLARE, so it never reaches §19/§20/§4.
This is the safety net for suggest-agent error (over- or under-proposal): the human gate is the
only path from PROPOSE → DECLARE, and it is fail-closed. It does **not** weaken V1–V5 — those still
run on whatever DECLARE the human *does* confirm; the no-confirm branch simply produces no DECLARE
at all. *(Human edits a proposal — add/remove a service before confirming — then the EDITED-confirmed
set becomes DECLARE; same gate, the human's ratified set is authoritative.)*

---

## §7 — §2 compliance + regression confirmation

`resolve()` (§4), generation (G1–G4), and validation (V1–V5) are **textually unchanged** — SUGGEST is
purely upstream of DECLARE; the confirmed DECLARE set is the same `services:` input the existing
pipeline consumes. The §8 sets (8/6/7) are **HIT, not re-derived** (§6). No pressure on DECLARE-shape,
`resolve()`, or §8 → **no dilemma**. The targeted gauntlet regression-confirms the downstream and
exercises the NEW SUGGEST→confirm→DECLARE front-door against the §6 examples.

---

## §8 — DoD coverage (SUGGEST increment)

- [x] SUGGEST→confirm→DECLARE front-door SHAPE specified — §0, §3 (pending HAMILTON fold), §4
- [x] what the agent EXAMINES → PROPOSES, via per-service `detection_hints` catalog fields — §1, §3
- [x] human-CONFIRM **fail-closed** gate (no confirm ⇒ no DECLARE ⇒ no generation) — §4, §5.1
- [x] how the confirmed suggestion FEEDS the EXISTING DECLARE/generation/validation — §2 frame, §6
- [x] tier/ownership + confirm-gate placement (SUGGEST agent T1 / examined project T3 / DECLARE T2) — §2
- [x] honest capability scope (SHAPE-only; agent accuracy = Phase-2; human gate makes it safe) — §1.3, §5.2
- [x] three worked examples via SUGGEST generating the existing DECLARE sets → 8/6/7 regression, **+ the fail-closed no-confirm branch shown** — §6
- [x] resolver §4 + generation G1-G4 + validation V1-V5 confirmed UNCHANGED — §7
- [ ] HAMILTON folds §3/§4 (choreography + fail-closed gate); both architects co-sign CONVERGED
- [ ] targeted gauntlet (DAEDALUS formalize into design-formal.md new sections, gated §0-§23 untouched → … → NOMOS)

---

## §9 — Provenance

Co-designed by **MAJOR_CHIRON_the-stoa** (detection-hint catalog fields + SUGGEST-step tier/ownership)
+ **MAJOR_HAMILTON_the-stoa** (SUGGEST→confirm→DECLARE choreography + human-confirm gate; §3/§4 pending
fold); unified by CHIRON (sole writer). Builds on the gauntlet-CONFORMANT Part-1 + Part-2 design
(`design-formal.md` §0–§23); resolver/generation/validation unchanged. Author: Denson Smith.
