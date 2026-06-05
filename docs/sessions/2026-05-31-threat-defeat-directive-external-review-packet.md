# External review request — "threat-defeat verification hardening" directive

**You are a cold, independent reviewer.** You have no prior context on this project, and that is the point. Your job is to find what is *wrong* with the directive below **before** it is built — cross-change interactions, hidden assumptions, weak phasing, scope errors, mis-prioritization, and anything the authors are too close to see. Be adversarial. Do not be agreeable. If the whole framing is off, say so.

This is a proposal to change a multi-agent software-review pipeline (the "Stoa gauntlet"). You do not need deep knowledge of it — minimal context is below.

---

## Minimal context

The Stoa gauntlet is a fixed pipeline of role-specialized AI agents that review and build a change: **DAEDALUS** (writes the design) → **ARGUS** (cold-audits the design, surfaces risk, proposes no fixes) → **ADA** (builds) → **VERA** (verifies via probes) → **CATO** (cold-reads the diff) → **ZENO** (mechanical spec-check). A human **floor-manager** relays between stages and a final human **close-gate** reviews before merge. Each reviewing seat emits a structured **verdict** (PASS / PARTIAL / FAIL + findings).

## The incident that motivates the directive (case study)

In a real arc (a shared-auth feature across two services):

1. ARGUS correctly named a MAJOR threat, "M2": an attacker sprays garbage user tokens at a stateless map service; each token forces the map service to call the auth service (carrying a **valid service secret**) → 1 DB query per garbage request. An unauthenticated resource-amplification / DoS lever.
2. The human ratified a fix at the security gate: *"add a per-IP throttle to fix M2."*
3. The builder (ADA) built a throttle — **on the wrong surface**: a per-caller-IP counter of *failed service-auth attempts* (someone probing the auth endpoint *without* the secret).
4. Why it does nothing for M2: the map service's calls carry the **valid** secret → they pass service-auth → they never increment the failed-auth throttle. M2 stayed 100% unmitigated. The throttle hardened a different surface (direct unauth probing — already rejected before the DB anyway).
5. **All five post-build stages (VERA, CATO, floor-manager) passed it.** They confirmed the throttle *works as built* (trips at the 11th failed attempt → 429; bounded memory; etc.). **None checked whether it defeats the threat it was created for.**
6. Caught **only** at the final human close-gate cold-read.

**The drift mechanism:** threat named correctly → ratification phrasing was *ambiguous* ("invalid introspections" could mean invalid *user* tokens [the real threat] or invalid *service-auth* [the easier surface]; the build took the easier reading) → the design never bound the mitigation to the named threat (it was a gate-added grid item, not a designed decision) → build drifted → every verification stage checked *artifact-correctness* ("does it work?") instead of *threat-defeat* ("does it stop M2?"). Severity of this instance: **MAJOR but bounded** (a DoS lever, not an auth bypass or data leak). The concern is the *process blind spot* — the same gap could pass something far worse.

## The proposed directive (7 role-by-role changes)

1. **DAEDALUS (design):** any mitigation addressing a named threat MUST carry an explicit *threat→mitigation map* (name the threat, its attack path, and how the mitigation defeats that path). A mitigation with no stated threat is a design smell ARGUS flags.
2. **Gate-ratified items get a design pass (process):** items added at the security gate (not via normal design) MUST be folded back into the design *with* their threat→mitigation map *before* build — not appended as a build-scope bullet. (This was the root cause.)
3. **Disambiguate ratification phrasing (process):** human ratification phrasing is shorthand; the named threat is canonical. Before build, the orchestrator MUST disambiguate ambiguous ratification back to the specific threat + attack path. The build must never silently pick the easier reading.
4. **Threat-anchored probes (VERA/CATO):** for any threat-ratified mitigation, a probe MUST exercise the *threat's actual attack path* and assert it is now blocked, AND that legitimate low-rate traffic is *not* throttled — not merely exercise the artifact's happy path.
5. **[KEYSTONE] Verdict templates require a threat-coverage assertion:** the verdict format MUST require, per threat-ratified mitigation, an explicit line: *"mitigation M defeats threat T via attack-path probe P."* A verdict cannot PASS such a mitigation without this line; its **absence is itself a finding.** This is the mechanical forcing-function intended to catch this at VERA, not the close-gate.
6. **Floor-manager + close-gate alignment step:** the relay + close-gate review MUST include a threat-vs-implementation alignment check per security mitigation, distinct from artifact-correctness.
7. **Culture/framing:** for security mitigations the question is never "does it run?" — it is "does it stop the *specific attack* it names?"

## The proposed build plan (decomposition + sequencing)

One epic, six children, **led by the keystone (#5)**:
- C1 = #5 (verdict threat-coverage assertion) — keystone, built first.
- C2 = #4 (threat-anchored probes).
- C3 = #1 (DAEDALUS threat→mitigation map + ARGUS design-smell).
- C4 = #2 + #3 merged (ratification→design binding) — justified as "shared seam."
- C5 = #6 (floor-manager + close-gate alignment).
- C6 = #7 (culture/framing).

Intended to ship as **one arc**, through the gauntlet itself.

---

## What we want from you (review questions)

Answer these directly and add anything else you find:

1. **Cross-change dependencies.** Does the keystone (#5, "M defeats T via probe P") actually work without #1 (the design naming T) and #4 (the probe P existing)? If #5 ships first but #1/#4 lag, can the assertion be made meaningfully — or does leading with #5 invert the real dependency order?
2. **Root-cause vs symptom.** The directive leads with #5 (post-build *verification*). But the drift's root cause was upstream: ambiguous ratification + unbound design (#2/#3/#1 — *prevention*). Is verification the right keystone, or is direction-binding the higher-leverage fix being under-weighted?
3. **False-confidence in the forcing-function.** #5 makes a threat-coverage *line* mandatory. What stops an agent from writing a plausible-but-wrong assertion (a present-but-false "M defeats T") that passes the mechanical check while the threat stays live — i.e., does #5 reproduce the very "it works on paper" failure one layer up?
4. **MAY vs MUST.** Are the "MUST" requirements placed correctly, or are there spots where the phrasing leaves latitude exactly where a hard constraint is needed (or vice versa — over-constraining low-risk cases)?
5. **Scope / one-arc-vs-split.** Should all 7 changes ship as one arc, or split (e.g., keystone first, process changes later)? Is the C4 merge of #2+#3 sound, or does it bundle two distinct fixes that could land asymmetrically?
6. **Coverage.** Does the 6-child decomposition lose or mis-map anything from the 7 changes?
7. **Over-fit to one incident.** The directive generalizes from a single (bounded) incident. Is it over-engineered for an N=1 event, or appropriately scoped? Where might it add process cost without catching a real future failure?
8. **Anything else wrong** — environment couplings, ordering hazards, definitional gaps (e.g., what counts as a "named threat" / "threat-ratified mitigation"?).

Return a prioritized list of findings (severity + the specific concern +, where you have one, a suggested fix). If you think the directive is sound, say which parts you stress-tested and why they held.
