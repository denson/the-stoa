---
author: Denson Smith
ticket: stoa--fdf (u--9s2 Phase-2 increment 2.2)
owner: Polybius_the_Stoa (user-tier forge domain) — supervising; reports up to Polybius the Grand at u--9s2
seat-to-launch: POLYBIUS_the-stoa (FM) + PLINY_the-stoa — STANDARD composition, full gauntlet
status: DIRECTIVE — NOMOS-on-directive gate pending before launch
as_of: 2026-06-26
---

# u--9s2 Phase-2 — increment 2.2 DIRECTIVE: the SUGGEST agent (examine → propose → confirm → declare)

## 0. Frame

Phase-1 DESIGN is complete and on main (`agents/design/stoa--jw5/design-formal.md` §24–§31 — the
SUGGEST front-door). Increment **2.1 shipped** (the resolution + discovery core, `builder_deploy_core`
on main at `agents/builder-deploy-core/`). Grand gated 2.1 PASS + GO'd 2.2. **This is increment 2.2** —
the SUGGEST front-door that figures out **which keys a project needs** by examining it, so a human
ratifies rather than remembers. It is **strictly UPSTREAM of DECLARE** (§24.0): it changes only HOW the
DECLARE set is produced; everything downstream (the 2.1 core) is **unchanged**.

This directive is the **WHAT**; the **HOW** (the engine's internals, the gate's UX, the fixture design)
is the team's design.

## 1. Deliverable (the WHAT)

Build the **real SUGGEST front-door**, promoting the Phase-1 VERIFIED choreography prototype
(`agents/design/stoa--jw5/suggest-check/`, **35/35 checks PASS**) into runnable code, and adding the
three Phase-2 pieces the design names (§24.1 / §25.3 / §26.3):

1. **The examination / inference engine** (§24 S-1/S-2, §28) — the genuinely new part. Implements the
   §28 **neuro-symbolic** shape: parse manifests/config + AST/outbound-call scan of the project's code +
   LLM resolution of dynamically-built endpoints + README/OpenAPI reconciliation → extract the four
   signal surfaces (sdk_imports / url_patterns / config_keys / data_signals) → **match the §25
   detection_hints** → **PROPOSE** a catalog-bounded service set **+ per-candidate evidence**.
   Recommendation-only / INERT (reads `detection_hints`, never `entries`).
2. **The `detection_hints` catalog DATA** (§25.3) — populate the additive advisory hint sets for
   cataloged services (beyond the four §25.3 seed hints the worked examples already exercise).
3. **The confirm-gate** (§26) — the fail-closed `D := confirm(P)` human gate built with an
   **anti-rubber-stamp, evidence-rich confirm-contract** (the ARGUS-named carry-forward + SWP-2):
   the gate PRESENTS each proposed service with its cited evidence (WHY it was proposed) so the human
   reviews *reasons*, not a blind yes/no; CONFIRM / EDIT / REJECT captured per §26.1.

The confirmed set **IS the §18 DECLARE set**, fed to the **UNCHANGED** 2.1 core (`generate()` → `resolve()`),
regression target **8 / 6 / 7**.

## 2. Scope

**IN (build here):**
- the examination/inference engine (§28 shape) — extract signals → match `detection_hints` → propose + evidence;
- the `detection_hints` catalog DATA (§25.3 Phase-2 fill);
- the confirm-gate (§26) + the **anti-rubber-stamp evidence-rich confirm-contract**;
- the provenance through-line (§27 — the confirmed DECLARE is **P3**: agent-proposed + human-ratified);
- wiring to the **unchanged** 2.1 core; the §29.1 worked-example **project fixtures** (small real repos
  carrying the §29.1 signals) as the machine-checkable surface for the engine.

**OUT (later increments / unchanged — do NOT build or touch here):**
- the provisioning choreography S0–S6 + the real repo→DB→GCP→Railway→mesh deploy → **increment 2.3**;
- the scienceclaw end-to-end stand-up → **increment 2.4**;
- **ALL real infrastructure** — no gcloud, no Railway, no credentials, no provisioning;
- **the §0–§23 mechanism stands TEXTUALLY UNCHANGED** (§24.0 load-bearing constraint): `resolve()` (§2),
  `generate()` (§19), validation V1–V5 (§20), the catalog `entries`, the §8 fixtures. SUGGEST is **purely
  upstream**: it IMPORTS `generate`/`resolve` from `builder_deploy_core` UNMODIFIED, never reimplements
  them, and **weakens NO V1–V5**. The §8 sets (8/6/7) are a **REGRESSION TARGET — hit, not re-derived.**

## 3. The SAFETY framing (load-bearing — read before the DoD)

Per §28: the engine's **accuracy is a USEFULNESS claim, NEVER a safety claim.** Safety rests **entirely**
on the §26 **fail-closed human-confirm gate** + the unchanged fail-closed V1–V5. A weak or absent
inference engine leaves the system **SAFE** — it only degrades SUGGEST to a weaker effort-saver. The
design makes **NO suggest-completeness claim**. Therefore:

- The DoD **gates** the **choreography**, the **fail-closed safety property**, and the **§2-constraint**
  (all machine-checkable — the prototype's 35 checks are the floor).
- The inference engine's **real-world accuracy (recall/precision)** is a **REPORTED Phase-2
  build-and-measure baseline (§28 / SWP-1), NOT a pass/fail gate.** Do not gate the arc on an accuracy
  number; do measure + report it honestly (incl. over-/under-proposal rates).

## 4. Decisions to PROPOSE (do not guess — surface, like 2.1's HOME)

1. **Engine implementation approach** — application code vs a Stoa **Workflow** realizing the §28
   neuro-symbolic flow. DAEDALUS proposes; **Polybius_the_Stoa ratifies**; **escalate to Grand if it
   implies a composition change** (e.g. it warrants HAMILTON the workflow-architect — in which case we
   re-compose rather than bake it).
2. **Read-surface scoping (SWP-3)** — exactly what project material the agent ingests, and the
   proposal-channel boundary. DAEDALUS scopes; ARGUS confirms SUGGEST adds no new trust boundary beyond
   R-2/candidate-R-3 OR names a distinct "proposal-channel integrity" residual.
3. **The anti-rubber-stamp confirm-contract shape (SWP-2)** — the human-factors contract (evidence
   richness, anti-rubber-stamp, the operational shape of "no-response"). DAEDALUS designs it as a
   **Phase-1-named contract**, not deferred wholesale.

## 5. Definition of Done (machine-checkable gates + reported measures)

**Gated (machine-checkable):**
1. **CHOREOGRAPHY** — examine → suggest → confirm → DECLARE reproduces §29.1: the three builders'
   confirmed DECLARE sets are **byte-identical to §23**, and the **UNCHANGED** `generate()→resolve()`
   yields **8 / 6 / 7**. (Promote the 35-check `suggest-check` prototype to real code.)
2. **FAIL-CLOSED SAFETY** — the §29.2 no-confirm branch: for **all** of {REJECT, no-response,
   edits-pending, None}, `confirm()` → **⊥ INERT**, no DECLARE produced, and **nothing reaches
   `generate()`** (downstream stays dark). **Over-proposal** removed by confirm → no bloat (resolve still
   6, no MAPS_API_KEY). **Under-proposal** added by confirm → no under-provision (resolve 7, BLS key present).
3. **§2-CONSTRAINT** — `generate` + `resolve` are IMPORTED from `builder_deploy_core` UNMODIFIED
   (module-identity assertion, not a copy); the §0–§23 mechanism is textually unchanged; V1–V5 not weakened.
4. **CONFIRM-GATE CONTRACT** — every proposed service carries its **cited detection-hint evidence**; the
   gate surfaces reasons (anti-rubber-stamp contract present + tested); the fail-closed `D := confirm(P)`
   property holds exactly per §26.1.
5. **DATA + PROVENANCE** — `detection_hints` catalog DATA populated (R-3 catalog-authoring discipline);
   the confirmed DECLARE is tagged **P3** (agent-proposed + human-ratified, §27).
6. **ENGINE RUNS (gated on existence + the fixtures, not accuracy)** — the engine examines the §29.1
   **project fixtures** (real small repos) and extracts the expected signals → the proven choreography →
   8/6/7. The engine exists, runs, and produces evidence-bearing proposals.
7. **REGRESSION** — the **full existing the-stoa suite is GREEN** (the 2.1 core's `builder-deploy-core`
   tests + gen-data + app build), AND the 2.1 core probes still pass (SUGGEST changed nothing downstream).
8. **Authorship** — `author: Denson Smith` on every artifact; zero foreign field.

**Reported (NOT gated, per §28):**
9. The inference engine's **accuracy baseline** on a real project — run it against **scienceclaw's actual
   repo** (a USEFULNESS demonstration that also readies 2.4) and report recall/precision + the
   over-/under-proposal it surfaces. This is a measured baseline, not a pass/fail.

10. The §4 decisions are **surfaced for ratification**, not silently baked.

## 6. Gauntlet + chain

- **CHAIN:** PRINCIPAL → Polybius the Grand → **Polybius_the_Stoa (supervising)** → POLYBIUS_the-stoa
  (FM, independent verify + relay) → PLINY_the-stoa (orchestrator) → CAPTAINs. PLINY surfaces to the FM,
  not user-tier direct; the FM relays up with its own verification.
- **COMPOSITION: STANDARD** — FM + PLINY. **NO CHIRON/HAMILTON** at launch — 2.2's design is Phase-1-done
  and §28 gives the engine shape; the architects are reserved for the 2.3 provisioning choreography
  (Grand). **Caveat:** decision §4.1 may route up an "engine-as-workflow" proposal — if I ratify it as
  warranting HAMILTON, we re-compose then, not now.
- **GAUNTLET: FULL, NO WAIVER** — DAEDALUS (build design + the §4 proposals) → ARGUS (cold-audit; confirm
  the SWP-1..4 classifications, esp. "safety = the gate, not the engine's accuracy") → ADA (build) → VERA
  (re-run the choreography + the load-bearing §29.2 fail-closed safety probe + over/under-proposal + the
  FULL existing suite) → CATO (cold-read) → NOMOS (audit vs design-formal §24–31 + this directive).
- **Worktree:** the team builds on an arc branch off main; the deliverable merges at the user-tier
  close-gate. The SUGGEST code lands under the 2.1 package's home (`agents/builder-deploy-core/`, the
  ratified-neutral location) unless DAEDALUS proposes otherwise.

## 7. Reporting

Polybius_the_Stoa supervises from user-tier and relays the 2.2 deliverable UP to Polybius the Grand's
gate (u--9s2) before increment 2.3 forges. **PRINCIPAL provisions nothing** — 2.2 is software + an
examination agent; the build environment has browser/computer-use available by policy, but 2.2's
examination is repo-analysis (no browser-driving is functionally required — that is the 2.3/2.4
credential-acquisition surface). Zero real infra.
