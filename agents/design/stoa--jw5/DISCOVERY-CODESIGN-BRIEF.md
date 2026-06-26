# CO-DESIGN BRIEF (PART 2) — KEY-DISCOVERY PROCESS addition — stoa--jw5 (u--9s2 Phase-1 revision)

**From:** PLINY_the-stoa (orchestrator) | sid 8040be7f
**For:** MAJOR_CHIRON_the-stoa + MAJOR_HAMILTON_the-stoa (co-design)
**Source:** Grand/PRINCIPAL new scope (u--9s2 "KEY-MODEL ADDITION"), relayed by the FM (idx108/109).
**operating-mode:** autonomous. Part 1 (fork-fold) is DONE + FM-verified; the Grand gate CLOSED the
isolation fork (Branch A + per-builder prepaid card = hard cap; M5 moot).

> This is a Phase-1 DESIGN REVISION: design the **SHAPE** of the discovery process now (so the model
> is COMPLETE + verifiable). The IMPLEMENTATION (catalog DATA + scanner + generator code) is **Phase-2**.
> Provision nothing.

---

## 1. The gap the addition closes

The Phase-1 model so far takes a HAND-AUTHORED per-builder manifest `{category, delta}` as its input.
The PRINCIPAL/Grand directive: the manifest must NOT be hand-guessed — it must be **DISCOVERED /
GENERATED from what the builder actually CALLS**. A builder that calls Google Maps + a BLS REST API
should have those keys provisioned because the system DETECTED the calls, not because a human
remembered to declare them. Missing a called service = a runtime failure; provisioning an uncalled
service = waste + scope bloat. Discovery makes the manifest a derived, verifiable artifact.

## 2. THE LOAD-BEARING ARCHITECTURAL CONSTRAINT (read first)

The existing **resolver (§4 set-algebra)** and **provisioning choreography (§5 S0–S6)** are already
gauntlet-CONFORMANT and **STAND UNCHANGED**. The discovery process is **strictly UPSTREAM** of them —
a new front-end that PRODUCES the `{category, delta}` manifest the existing resolver consumes:

```
   services-called  ──discover──▶  ──catalog lookup──▶  GENERATED {category, delta} manifest
        │                                                          │
   (scan or declare)                                               ▼
                                                       resolve()  [UNCHANGED §4]  ──▶ resolved set
                                                                                          │
                                                                          provision [UNCHANGED §5 S0-S6]
```

Design the addition so the existing resolver + fixtures (§8: prospector 8 / scienceclaw 6 /
labstat_bls 7) are a **regression target you must still hit**, NOT something you re-derive. If your
reframe would change resolve() or the §8 expected sets, STOP and surface it — that is a scope breach.

## 3. Scope split (co-design, iterate together)

### CHIRON (catalog structure / ownership + the emergent-templates reframe) owns:
- **The service→key CATALOG structure (T1, versioned):** per service, a record of
  `{ service-id, the key/credential entry(ies) it requires as typed §3 entries (kind+name),
  the GCP API to enable if any, the category it belongs to }`. How the catalog relates to the
  existing §3 taxonomy (every catalog entry's credential is a typed entry) + the §3.2 category
  templates. Where it lives (T1 cookie-cutter source), how it extends (additive, per §6 open-closed).
- **The EMERGENT-TEMPLATES reframe:** category templates were STATIC declared bundles; reframe them as
  **emergent common service-bundles** — a category = a named, frequently-co-occurring set of
  services-called. Define the relationship precisely so it does NOT break the existing model: a
  category remains a named entry-set the resolver consumes; what CHANGES is its PROVENANCE (emergent
  from observed service-bundles, promoted via the §6 graduation rule) rather than hand-declared. The
  per-deployment **delta becomes DERIVED** = (services-called → entries) minus (category's entries).
- **Ownership/tier placement** of the catalog + the discovery declarations (T1 vs T2 vs T3 per the
  existing three-tier model).

### HAMILTON (discovery / generation / validation choreography) owns:
- **The DISCOVERY step (scan-vs-declare):** specify the SHAPE of detecting services-called —
  (A) SCAN the builder's code/skills for external-service usage (static detection), and/or
  (B) each skill DECLARES the services it calls (an in-skill declaration). Recommend the model
  (one, the other, or both with precedence) with reasoning; web-verify any tooling-capability claim
  (do not assert scanner feasibility from memory).
- **The manifest GENERATION choreography:** services-called → catalog lookup → emit the
  `{category, delta}` manifest. The algorithm: map each called service to its catalog entries, pick
  the best-fit emergent category (the largest covering bundle), derive the delta as the remainder.
- **The VALIDATION choreography:** the generated manifest is VALID iff every service-called resolves
  to a catalog entry (no unknown service), the generated manifest is COMPLETE (covers all
  services-called) and MINIMAL (no uncalled service provisioned), and resolve(generated-manifest)
  is well-formed (no BaselineOmitError, runtime-completeness §3.4 holds). Where this sits relative to
  S0–S6 (it runs BEFORE S0 — it produces the manifest S0 consumes).

### Both (shared — the falsification target):
- **The THREE worked examples, re-expressed through discovery:** for prospector / scienceclaw /
  labstat_bls, show `services-called → catalog lookup → GENERATED {category, delta}` and prove the
  generated manifest RESOLVES to the SAME §8 set (8 / 6 / 7). labstat_bls is again load-bearing: a
  call to the BLS OEWS REST API must DISCOVER → generate the `+BLS_OEWS_API_KEY` delta (kind
  thirdparty_rest_key), reproducing the existing §8.3 result. This proves discovery produces the
  manifests the gauntlet already validated — the resolver is untouched.

## 4. Definition of Done (the addition)

- [ ] service→key CATALOG structure specified (per-service record: typed entries + GCP API + category;
      T1 placement; additive extensibility).
- [ ] DISCOVERY step specified (scan and/or declare, with a recommended model + any tooling-capability
      claim web-verified).
- [ ] manifest GENERATION specified (services-called → {category, delta}, unambiguous).
- [ ] manifest VALIDATION specified (complete + minimal + every-service-cataloged + resolve()-well-formed).
- [ ] EMERGENT-TEMPLATES reframe specified (category = emergent bundle; delta = derived; WITHOUT
      changing the resolver or the §8 expected sets — stated explicitly).
- [ ] All THREE worked examples re-expressed via discovery AND shown to GENERATE manifests that resolve
      to the existing 8 / 6 / 7 (regression target hit).
- [ ] The resolver §4 + provisioning §5 confirmed UNCHANGED (regression-confirm, not re-derive).

## 5. Co-design protocol (I DRIVE the cross-handoff)

1. **Output:** a single unified `agents/design/stoa--jw5/discovery-codesign.md`. To avoid
   concurrent-write corruption: **HAMILTON writes its choreography sections to
   `agents/design/stoa--jw5/discovery-choreography-hamilton.md`**; **CHIRON authors the unified
   `discovery-codesign.md`**, folding HAMILTON's sections (CHIRON = single writer of the unified file).
2. **Iterate together.** Post handoffs on stoa--jw5 tagged `[for: CHIRON_the-stoa]` /
   `[for: HAMILTON_the-stoa]` / `[for: PLINY_the-stoa]`. The catalog structure (CHIRON) and the
   generation/validation (HAMILTON) co-constrain — flag any seam change.
3. **Arm an active poll loop while waiting on your sibling** (the cross-handoff stall lesson). I poll
   ~2-3 min and drive; surface convergence to the FM.
4. **Honor the §2 constraint absolutely.** If the reframe pressures resolve() or the §8 sets, that is a
   tradeoff to FRAME for me/the FM (dilemma-classify), not a silent change.
5. **Convergence signal:** when discovery-codesign.md meets all of §4 and both sign off, post
   `DISCOVERY CO-DESIGN CONVERGED — stoa--jw5` tagged `[for: PLINY_the-stoa]`. I then open the
   TARGETED gauntlet (DAEDALUS formalize → ARGUS → ADA exercises manifest-GENERATION vs the 3 examples
   → VERA → CATO → NOMOS; resolver/provisioning = regression-confirm only).

**First action (each):** ACK on stoa--jw5 (confirm seat + your half), then begin. CHIRON — stand up the
`discovery-codesign.md` skeleton (the §4 DoD as section headers + the §2 constraint stated at the top).

— PLINY_the-stoa | sid 8040be7f-a1ba-4917-b953-75947d464abf | the-stoa
