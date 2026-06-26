---
author: Denson Smith
ticket: stoa--pj3 (u--9s2 Phase-2 increment 2.1)
owner: Polybius_the_Stoa (user-tier forge domain) — supervising; reports up to Polybius the Grand at u--9s2
seat-to-launch: POLYBIUS_the-stoa (FM) + PLINY_the-stoa — STANDARD composition, full gauntlet
status: DIRECTIVE — NOMOS-on-directive gate pending before launch
as_of: 2026-06-26
---

# u--9s2 Phase-2 — increment 2.1 DIRECTIVE: builder-deploy resolution + discovery core

## 0. Frame

Phase-1 DESIGN is **complete and on main** (`agents/design/stoa--jw5/design-formal.md`, 31 sections:
Part-1 key-provisioning model §1–15, Part-2 discovery §16–23, Part-3 SUGGEST §24–31). Grand's
Phase-2 BUILD GO (u--9s2, 2026-06-26T19:25:49Z) hands Polybius_the_Stoa the runnable cookie-cutter
to drive via a fresh decompose. **This is increment 2.1 of that decompose** — the foundational,
pure-software, zero-infra core. It is the lowest-risk increment by construction: its design is
already verified, and two prototype harnesses already prove it implementable.

This directive is the **WHAT**. The **HOW** (skill structure, packaging, file layout) is the team's
design, produced by DAEDALUS and gauntlet-checked.

## 1. Deliverable (the WHAT)

Promote the **two Phase-1 VERIFIED prototype harnesses** into the **real, runnable, packaged
builder-deploy skill core** — the resolution + discovery front-end — plus its externalized DATA,
with the design's fixtures locked as a regression suite.

**Source to promote (on main):**
- `agents/design/stoa--jw5/resolution-check/` — `resolve.py` (§2.5 verbatim) + `derive_sa_scope`
  (§5.A) + `check_runtime_completeness` (§3.4); BASELINE (§3.1) + category library (§3.2) as data;
  `BaselineOmitError` / `ResolutionError` (§2.4). **Prototype PASSES** (19/19 checks; §8 fixtures
  8/6/7 byte-for-byte; §8.4 fail-closed; all 5 baseline entries guarded).
- `agents/design/stoa--jw5/discovery-check/` — `catalog.py` (§22 seed catalog) + `generate.py`
  (§19 G1–G4) + `validate.py` (§20 V1–V5). **Prototype PASSES** (3 builders generate→resolve to
  8/6/7; V1–V5 pass; NEG-1 V5 fail-closed; NEG-2 `UncatalogedServiceError` + V1 fail; resolver
  reused unmodified).

**The promotion = harden + package + externalize:** prototype code under a design-scratch dir
becomes the real skill's code; encoded-as-data BASELINE/library/catalog become **externalized DATA
files** (`baseline.yaml`, `categories/<name>.yaml`, the service→key catalog) per §3.1/§3.2/§17/§22;
the §8/§23/§8.4 fixtures become the skill's **locked regression suite**. The resolver MUST remain
the single source of truth (discovery imports it, never re-implements — the §2-constraint).

## 2. Scope

**IN (build here):**
- the resolver `resolve()` (§2) + the typed-entry taxonomy (§3) + SA-scope derivation (§5.A) +
  runtime-completeness (§3.4) + kind-dispatch (§3.3);
- the manifest schema (§1);
- the service→key catalog + emergent-category DATA (§17/§22) + baseline/category-template DATA (§3.1/§3.2);
- the generator G1–G4 (§19, declared `services:` → `{category, delta}`);
- the validator V1–V5 (§20);
- the §8 + §23 + §8.4-negative fixtures as the LOCKED acceptance/regression suite.

**OUT (later increments — do NOT build here):**
- the SUGGEST agent / front-door (§24–31) → **increment 2.2**;
- the provisioning choreography S0–S6 + the real repo→DB→GCP-project/SA→Railway→Tailscale-mesh
  deploy (§4, §6, §7) → **increment 2.3** (CHIRON+HAMILTON design the choreography);
- the scienceclaw acceptance test → **increment 2.4**;
- **ALL real infrastructure** — no `gcloud`, no Railway, no credentials, no network. 2.1 is pure
  software that **reads no environment** (§2.3 purity). This is the hard boundary.

## 3. The one decision to PROPOSE (do not guess)

The builder-deploy skill's **structure + permanent deployment HOME** is undecided. DAEDALUS
**proposes** it (candidates incl. the-stoa as the forge-owned home, vs a standalone builder-tooling
location consumed by builder workspaces); ARGUS critiques; **Polybius_the_Stoa ratifies** (escalates
to Grand if load-bearing). 2.1 builds on an arc branch in the-stoa; a later relocation is additive.
Do not silently bake a home — surface the proposal.

## 4. Locked carry-forwards (from Grand's GO; context for the arc, mostly later-increment)

- per-builder GCP **project** + per-builder **prepaid card/billing** = the **hard spend cap** (NOT a
  GCP budget feature) — a 2.3 provisioning property; noted, not built in 2.1.
- the per-builder key set via the **catalog + SUGGEST + declare** model — 2.1 builds catalog+declare;
  SUGGEST is 2.2.
- **R-1 / R-2 / R-3** (prune-on-removal / manifest-integrity / catalog-integrity) are live Phase-2
  named residuals — addressed in **2.3** (builder-lifecycle + governance). 2.1 is **initial-resolution
  correctness** (t0), where these do not yet bind. Do not attempt them here; do not regress them.

## 5. Definition of Done (machine-checkable)

1. **Resolver:** `resolve()` reproduces §8 — prospector **8**, scienceclaw **6**, labstat_bls **7**
   entries BYTE-FOR-BYTE; §8.4 raises a NAMED `BaselineOmitError` with no set returned; the guard
   fires for **all 5** non-omittable baseline entries (the R1-close generalization).
2. **Generator:** from each builder's declared `services:`, produces the `{category, delta}` manifest
   that the **UNCHANGED resolver** resolves to 8/6/7, manifest-equivalent to the §8 hand-authored
   fixtures (alias-aware: `document/data` ≡ `document-consuming`).
3. **Validator:** V1–V5 pass on every generated manifest; **NEG-1** (undeclared shadow service →
   V5 fail-closed) and **NEG-2** (uncataloged declared service → `UncatalogedServiceError` + V1 fail)
   both hold.
4. **Resolved-set properties:** SA-scope (§5.A) excludes non-scope-bearing kinds; runtime-completeness
   (§3.4) holds (prospector carries BOTH `google-maps` AND `MAPS_API_KEY`); kind-dispatch (§3.3)
   correct (labstat_bls `BLS_OEWS_API_KEY` is `thirdparty_rest_key`, mints no `gcp_api`, excluded
   from the S1 enable list).
5. **DATA externalized:** baseline / category templates / service→key catalog are real DATA files
   (not hardcoded), matching §3.1/§3.2/§17/§22; the resolver/generator read them as data.
6. **Purity:** the core reads NO environment (no gcloud/Railway/network/clock/filesystem beyond its
   own DATA) — §2.3. The §2-constraint holds: discovery imports the resolver, never re-implements it.
7. **Full-suite regression:** the **full existing the-stoa test suite is GREEN** (gen-data roster
   derivation + app build) IN ADDITION to the bespoke fixtures — confirm the new skill code breaks
   nothing in the roster/app. (VERA runs the full suite, not just the bespoke probes.)
8. **Authorship:** `author: Denson Smith` on every artifact; ZERO foreign author field.
9. **Home proposal surfaced:** the §3 skill structure + home decision is presented for ratification,
   not silently chosen.

## 6. Gauntlet + chain

- **CHAIN:** PRINCIPAL → Polybius the Grand → **Polybius_the_Stoa (supervising)** → POLYBIUS_the-stoa
  (FM, independent verify + relay) → PLINY_the-stoa (orchestrator) → CAPTAINs. PLINY surfaces to the
  FM, not to user-tier direct. FM relays up to Polybius_the_Stoa with its own verification attached.
- **COMPOSITION: STANDARD** — POLYBIUS_the-stoa (FM) + PLINY_the-stoa. **NO CHIRON+HAMILTON** — 2.1's
  design is already done in Phase-1; the architects join at **increment 2.3** for the provisioning
  choreography (Grand's "likely CHIRON+HAMILTON to design the provisioning choreography").
- **GAUNTLET: FULL, NO WAIVER** — DAEDALUS (build design + home proposal) → ARGUS (cold-audit) → ADA
  (build) → VERA (re-run §8/§23 fixtures + the FULL suite + threat probes) → CATO (cold-read) →
  NOMOS (audit vs ground truth: design-formal + this directive).
- **Worktree:** the team builds on an arc branch / arc-build worktree off the-stoa main; the
  deliverable merges to main at the user-tier close-gate. (No deployed-`.claude/` self-apply expected —
  2.1 is new tooling, not a substrate role file.)

## 7. Reporting

Polybius_the_Stoa supervises from user-tier and relays the 2.1 deliverable UP to Polybius the Grand's
gate (u--9s2) before increment 2.2 forges. **PRINCIPAL provisions nothing** — 2.1 touches no infra.
