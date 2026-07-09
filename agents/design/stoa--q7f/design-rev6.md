---
author: Denson Smith
seat: CAPTAIN_DAEDALUS_the_stoa (ARCHITECT)
ticket: stoa--q7f
requirement: sos--373 (science lane) + nws-1n7 (newswire store lane) + future builder lanes
epic: u--9s2 (Phase-1 increment 2.4 — BUILD gauntlet: build the REAL pass-through service)
arc: arc-77 (coordination stoa--po5)
supersedes/builds-on: design-rev5.md (arc-77/build — SHAPE + INV-RESP depth-recursion cleared by ARGUS rev5 re-audit PASS-WITH-CONDITIONS + VERA build-falsification PASS; carried UNCHANGED except the TWO by-construction-generality folds — r1 + r2 — in the rev6 changelog)
consumes: docs/research/anthropic-workflows-report.md (in-harness canon), docs/secure-core/deployment-plan.md (runbook), arc-77-build-directive.md §3A/§4/§5/§6, agents/verdicts/stoa--q7f/argus-rev3-security.md (the ARGUS REVISE verdict rev4 folded), agents/verdicts/stoa--q7f/vera-build-falsification.md (the VERA PASS + the INV-RESP depth-2 finding rev5 folded), agents/verdicts/stoa--q7f/argus-rev5-inv-resp.md (the ARGUS rev5 PASS-WITH-CONDITIONS + the r1 + r2 conditions rev6 folds)
status: design-rev6 (BUILD-facing — the REAL service). Folds the TWO ARGUS-rev5, FM-ratified FOLD-BOTH conditions that complete the by-construction GENERALITY of the recursive INV-RESP node grammar: (r1) the SCALAR node drops any object/dict at ANY depth via a RECURSIVE dict-scan — stated as a by-construction rule and now PROBED by a P-M2 SCALAR-slot clause that FAILS a shallow-SCALAR build; (r2) a server-side `PASS_WHOLE_ALLOWLIST` (this arc `{"candidates.content"}`) enumerates the ONLY fields that may be PASS_WHOLE, and the INV-RESP loader REFUSES TO LOAD (fail-CLOSED at load) any schema marking a non-allowlisted field PASS_WHOLE — now PROBED by a placement clause. NO structural redesign — everything else in rev5 carried VERBATIM (multi-lane authz, INV-PRINCIPAL, seal-audit, INV-DEST/BIND/LANE, the OBJECT-recursion, M1/M3-M7, all other invariants/probes NOT re-litigated).
build-scope: BUILD the REAL pass-through service locally/against mocks; verify by re-running the design's own attack probes against REAL code. NO real infra, NO real secrets, NO money, nothing merged/pushed (directive §5 SCOPE FENCE).
---

# Secure Railway core for the CONSOLIDATION center — credentialed per-provider pass-through, multi-lane (rev6, BUILD-facing)

## rev6 changelog — the two ARGUS-rev5 conditions folded (by-construction GENERALITY completed; SHAPE UNCHANGED)

ARGUS re-audited the rev4→rev5 INV-RESP depth-fold delta and returned **PASS-WITH-CONDITIONS**: the core
OBJECT-node depth recursion closes the scoped VERA depth-2 finding BY CONSTRUCTION, P-M2(a.2) genuinely
falsifies a depth-2 build, the loader refuses a bare-`list` node (fails closed at load), and the delta is
confined to the INV-RESP fold (no rev4 regression). ARGUS surfaced **two load-bearing-uncertain residuals**
— NOT in the scoped VERA finding (which is closed), but in the by-construction GENERALITY the general
recursive form was CHOSEN to deliver (protecting future ops/providers). The FM ratified **FOLD BOTH
this-arc, pre-ADA** (both complete the generality that was the entire rationale for the general recursive
form; there is no r3 lurking in the node grammar — OBJECT recurses [rev5] + SCALAR-object-drop-probed [r1]
+ PASS_WHOLE-placement-guarded [r2] = all three node types fully guarded = a fixed point). rev6 folds
**ONLY** r1 + r2 — everything else in rev5 is carried VERBATIM.

| Cond | ARGUS rev5 finding | Kind | How folded in rev6 | Section |
|------|--------------------|------|--------------------|---------|
| **r1** | The SCALAR no-object-at-any-depth by-construction guarantee is STATED in the grammar but UNPROBED — P-M2(a.2) plants a credential ONLY in an undeclared sub-key of a declared OBJECT node (`groundingMetadata`), never in a dict smuggled under a SCALAR slot. A **shallow-SCALAR** build (drop only a top-level dict; pass a list-containing-a-dict) would PASS P-M2(a.2) while leaving the SCALAR-slot smuggle path open — the credential-bearing dict rides through under a SCALAR leaf. Implementation-fidelity (recursive dict-scan, not a shallow top-level check) + probe-coverage are the open dependencies. | **LOAD-BEARING** (completes the generality; cheap probe-case addition) | **SCALAR made an explicit RECURSIVE-dict-scan by-construction rule.** The SCALAR handler recursively scans into lists / nested containers and refuses to emit ANY mapping (dict) found at ANY depth — only true scalar leaves (str/num/bool/null) and (recursively) arrays-of-scalars pass. A shallow top-level check is **non-conformant** by the stated NODE-grammar rule. **P-M2 EXTENDED** with a SCALAR-slot clause: plant an object/dict (carrying a credential-shaped value) UNDER a SCALAR-declared field — INCLUDING nested inside a list — → assert DROPPED from the caller-facing output AND absent from BOTH audit phases; a shallow-SCALAR build FAILS it. + a legit clause: a legitimate scalar value AND a list of scalars under a SCALAR field pass intact. | §5.1a (SCALAR grammar + P-M2 a.3), §1 (M2 row + honest-claim), §4 (INV-RESP bullet), §5.1/§5.2 (contract + map), §5.3 (DoD), §6 wp#3 |
| **r2** | PASS_WHOLE is an UNAUDITED runtime whole-pass escape hatch: the extended loader guard validates node TYPES only (OBJECT/SCALAR/PASS_WHOLE well-formed); it does NOT restrict WHERE PASS_WHOLE may appear. A FUTURE provider returning a credential IN its response body could have that field mistakenly marked PASS_WHOLE and bypass INV-RESP at runtime with NO mechanical catch — only reviewer convention + the build-time (not runtime) seal-audit. This is EXACTLY the future-provider case the general recursive form was chosen to protect. | **LOAD-BEARING** (mechanizes deny-by-default on the last unguarded node type) | **PASS_WHOLE placement made DENY-BY-DEFAULT.** A server-side, code-level **`PASS_WHOLE_ALLOWLIST`** (this arc `frozenset({"candidates.content"})` — the model product) enumerates the ONLY dotted-path fields that may be PASS_WHOLE. The INV-RESP loader self-check (`_check_inv_resp`) walks the schema node tree and **REFUSES TO LOAD** (`LoaderError`, fail-CLOSED AT LOAD) any `response_schema` marking a field PASS_WHOLE whose dotted path is NOT in the allowlist. A new PASS_WHOLE placement requires an explicit, audited allowlist entry — consistent with the design's deny-by-default philosophy (INV-LANE / INV-PRINCIPAL / seal-audit). **P-M2 EXTENDED** with a placement clause: a schema marking a NON-allowlisted field PASS_WHOLE → the loader REFUSES TO LOAD (a build that loads it anyway FAILS); + a legit clause: the allowlisted `candidates.content` PASS_WHOLE loads AND passes whole. | §5.1a (PASS_WHOLE_ALLOWLIST + loader guard + P-M2 a.4), §1 (M2 row + honest-claim), §4 (INV-RESP bullet), §5.1/§5.2 (contract + map), §5.3 (DoD), §6 wp#3 |
| — | **Everything else in rev5 carried UNCHANGED** — the multi-lane authz (§2), INV-PRINCIPAL, the seal-audit (§3.1) and its r2 constraint, INV-DEST/BIND/LANE, the OBJECT-node recursion (rev5), M1/M3/M4/M5/M6/M7 and P-M1/P-M3..P-M7, the workflow-vs-app-code call (§4), the scope fence, the honest residuals. rev6 re-litigates NONE of them. | (no delta) | Carried from rev5 verbatim. | (all) |

**Classification (6.12 A3 author duty — I PROPOSE, ARGUS CONFIRMS):** both r1 and r2 are **TIGHTENINGS
inside the ALREADY-threat-ratified M2 mitigation** (INV-RESP) — exactly as the rev5 depth-recursion
tightened M2, and as the rev4 r2 constraint tightened the threat-ratified seal-audit. **No new M#**; M2's
existing A3 map row (§5.2) is reused; the threat-anchored probe remains **P-M2** (now further extended with
the SCALAR-slot clause a.3 + the PASS_WHOLE-placement clause a.4, §5.1a) — the probe the verdict's
`defeats_via_probe: V-M2-RESP` cites. Neither fold introduces a new attack path or threat: r1 probes an
attack path (object-under-SCALAR-slot) the rev5 grammar already named but left unprobed; r2 mechanizes a
deny-by-default guard on the PASS_WHOLE escape hatch the rev5 grammar already declared "never a default." The
`PASS_WHOLE_ALLOWLIST` is a bounded, documented guard on the existing carve-out, NOT a new mitigation.

## rev5 changelog — the VERA INV-RESP depth-2 finding folded (SHAPE UNCHANGED)

VERA's independent build-falsification returned **PASS** with ONE consequential, load-bearing finding the FM
ratified **FIX-NOW-this-arc**: the INV-RESP allow-list is **DEPTH-2** — `redact_response` keeps only the
declared sub-keys of a declared field but emits each sub-key's VALUE **WHOLE** and never recurses, so a
credential planted at depth ≥ 3 inside a DECLARED field (an undeclared sub-key of
`candidates[].groundingMetadata`, or a nested field under `candidates[].content`) passes through. **No design
ASSERTION was falsified** (P-M2 was scoped to UNDECLARED fields, all PASS) and the realistic Vertex exfil
surface is closed (the core's ADC bearer is a REQUEST-side `Authorization` header, never present in a Vertex
response body) — but this is the partial opaque-passthrough INV-RESP nominally disallows, and it must hold
**BY CONSTRUCTION** (protecting future ops/providers whose declared nested fields could be credential-adjacent)
before the build relays to the Grand's Phase-1 SECURITY gate. rev5 folds **ONLY** this fix.

| # | VERA finding | Kind | How folded in rev5 | Section |
|---|--------------|------|--------------------|---------|
| **INV-RESP depth-2** | `redact_response` is a depth-2 allow-list: it keeps only declared sub-keys but emits each sub-key VALUE WHOLE and never recurses, so a credential in an UNDECLARED sub-key of a declared field (`groundingMetadata.<x>`, a nested `content` field) at depth ≥ 3 passes through. | **LOAD-BEARING** (hardening; NOT build-blocking — no assertion falsified, realistic surface closed) | **INV-RESP made depth-complete.** `redact_response` recurses to schema depth over a NODE grammar (`OBJECT` / `SCALAR` / `PASS_WHOLE`); the per-op `response_schema` declares nested allowed structure; an undeclared sub-key at ANY depth is DROPPED by construction. `content` is the ONE explicit, documented `PASS_WHOLE` exception (model product — not credential-bearing, the ADC bearer is request-side). The loader REFUSES a legacy depth-2 (bare-`list`) schema node (regression fails closed AT LOAD). M2 honest-claim updated to the recursive form. **P-M2 EXTENDED** with a nested-declared-field clause (credential at depth ≥ 3 in an undeclared sub-key of a declared field → DROPPED + absent from BOTH audit phases; a depth-2 build FAILS it) + a legit clause (declared nested sub-key intact; `content` passes whole). | §5.1a (new), §1 (M2 row + honest-claim), §4 (INV-RESP bullet), §5.1/§5.2 (contract + map), §5.3 (DoD), §6 wp#3 |
| — | **Everything else in rev4 carried UNCHANGED** — the multi-lane authz (§2), INV-PRINCIPAL, the seal-audit (§3.1) and its r2 constraint, INV-DEST/BIND/LANE, M1/M3/M4/M5/M6/M7 and P-M1/P-M3..P-M7, the workflow-vs-app-code call (§4), the scope fence, the honest residuals (D2 real-AF_UNIX = Phase-3; seal-audit <100-entropy floor). rev5 re-litigates NONE of them. | (no delta) | Carried from rev4 verbatim. | (all) |

**Classification (6.12 A3 author duty — I PROPOSE, ARGUS CONFIRMS):** the depth fix is a **TIGHTENING inside the
ALREADY-threat-ratified M2 mitigation** (INV-RESP) — exactly as the rev4 r2 constraint tightened the
threat-ratified seal-audit. **No new M#**; M2's existing A3 map row (§5.2) is reused; the threat-anchored probe
remains **P-M2** (now extended, §5.1a) — the probe the verdict's `defeats_via_probe: V-M2-RESP` cites. The
`content` `PASS_WHOLE` exception is a bounded, documented carve-out of the recursion, NOT a new mitigation.

## rev4 changelog — the four ARGUS-rev3 conditions folded (SHAPE UNCHANGED)

ARGUS cold-audited design-rev3 and returned **PASS-WITH-CONDITIONS (REVISE)**: the SHAPE is cleared
(carry from rev2 FAITHFUL, multi-lane reframe sound, honest residual correctly placed, workflow=app-code
correct, all three A3 classifications confirmed, scope fence held). rev4 does **not** redesign anything —
it folds the two load-bearing conditions + the two scope surfaces as precise tightenings. Everything
else is carried from rev3 **verbatim**.

| Cond | ARGUS finding (rev3) | Kind | How folded in rev4 | Section |
|------|----------------------|------|--------------------|---------|
| **r1** | Request-time principal resolution has NO fail-closed invariant/probe for the no-resolvable-principal case; a `LANE_REGISTRY.get(cap, DEFAULT)`-style build would PASS P-M4 yet be cross-lane-broken. INV-LANE guards STARTUP config only; nothing guards REQUEST-TIME resolution. | **LOAD-BEARING** | NEW **`INV-PRINCIPAL`** — a distinct **request-time** fail-closed principal-resolution invariant (sibling to the startup INV-LANE): resolve by **EXPLICIT MEMBERSHIP only**; any unresolvable principal → **403, no egress, audited `forbidden`**, NEVER a default. The `.get(cap, DEFAULT)` shape is explicitly forbidden. §2.1 resolution logic rewritten with the explicit `else → 403`; **P-M4 extended** with a clause that FALSIFIES the permissive-default build (asserts denial on the unmapped-cap AND the absent-header paths). | §2.1, §2.4 (INV-PRINCIPAL), §2.5, §5.1, §5.2 |
| **r2** | `SEAL_AUDIT_SYNTHETIC_` is an UNCONDITIONAL allow-list token = universal bypass; a real-shaped secret carrying the prefix is waved through, reopening M7. P-M7 codifies marked→pass as correct, so the bypass is unprobed. | **LOAD-BEARING** | The synthetic exemption is **constrained to the INTERSECTION** (path-bound AND shape-clean): a marked value is exempt ONLY IF it is (i) located in the designated test-fixtures path AND (ii) does NOT itself match any real-secret shape. **A value matching a real-secret shape is FAILED even when marked**, and a marked value outside the fixtures path is FAILED. **P-M7 extended** with a bypass clause: a real-SHAPED marked secret (outside fixtures and/or matching a real shape) → build STILL FAILS. | §3.1, §5.2 |
| **r3** | Multi-cap resolution under-specified: §2.1 maps cap NAME(s) [plural] → THE lane principal [singular]; the union-vs-first-match-vs-reject-ambiguous rule is unstated and directly determines the cross-lane boundary. | scope (uncertain) | Specify the FAIL-CLOSED rule: **reject-ambiguous by default** — if >1 distinct lane principal resolves and the node is not an explicitly-registered multi-lane node → **DENY 403**; NEVER a silent union. An intentional multi-lane node is an explicit registered exception. Multi-cap header case named in **V-ENC-LANE**. | §2.1, §2.4 (INV-PRINCIPAL clause), §6 wp#4 |
| **r4** | Cross-lane DATA-tenancy in the SHARED pgvector store is silent/unscoped — multi-lane authz closes cross-lane API-EGRESS but not cross-lane DATA isolation in the shared store. | scope-OUT (store-layer, does NOT block this build) | **Explicitly scoped OUT** in §7: store-layer row/tenant isolation (can `lane:newswire` read `lane:science` rows) is a SEPARATE concern tracked in ticket **stoa--exn**; the multi-lane authz closes cross-lane API-EGRESS ONLY. Boundary stated so it is NOT silently assumed closed. **No fix designed** (directive r4 = scope-out only). | §7 |
| — | **ARGUS's other findings need NO change:** carry from rev2 FAITHFUL (nothing weakened; scopes class→lane is a TIGHTENING); workflow-vs-app-code = **application code** CONFIRMED; all three A3 classifications CONFIRMED (seal-audit threat-ratified; DC3 mock-emit + workflow-call NOT-threat-ratified, carve-outs correct not self-asserted); per-lane cap-NAME choice sound; future lane = ZERO access by default; honest-residual placement correct; authorship = Denson Smith; scope fence held. | (no delta) | Carried from rev3 UNCHANGED — these are non-findings ARGUS CLEARED; rev4 re-litigates none of them. | (all) |

---

## rev3 changelog — what was NEW vs rev2, what was CARRIED (retained for lineage)

rev2 was gated with the DC1 SHAPE correct (closed-registry per-provider SCOPED pass-through). rev3 did
**not** redesign that shape. It made the service **buildable as the shared center ALL lanes consume**
and folded the arc-77 directive's three mandatory items. Three things were NEW; everything else carried.

| # | rev3 delta | Kind | Section |
|---|------------|------|---------|
| **1** | **CONSOLIDATION reframe** — multi-consumer (multi-lane) identity/authz on the pass-through. rev2 was framed for a SINGLE builder/consumer; the core is now the canonical center for the science lane (sos--373) + the newswire credential-free STORE (nws-1n7) + future builders. The **one genuinely-novel design delta.** | **FIRST-CLASS NEW** (ARGUS cold-audits specifically) | §2 |
| **2** | **The 3 mandatory canons folded as build requirements:** (a) seal-every-secret + **fail-CLOSED seal-audit** (u--84m, made a build GATE — new named threat **M7**); (b) **Railway-setup skill sos--1bk** as the Phase-2 provisioning-choreography reference (NOT executed this arc); (c) **in-harness-workflows canon** (any LLM adjudication runs in-harness on subscription OAuth, never a keyed CI call). | build requirements | §3 |
| **3** | **The workflow-vs-app-code call, answered INLINE:** the pass-through is deterministic **application code** — no Stoa Workflow warranted. | design decision | §4 |

**Carried UNCHANGED from rev2 (do NOT re-litigate — restated build-facing in §5, not redesigned):**
the closed-registry per-provider SCOPED pass-through over the server-side `PROVIDER_REGISTRY`; `INV-DEST`
(SSRF closed by construction — `url_slots` FIXED/ENUM only, disjoint from `params`/`skill_id`,
redirect-following OFF, loader fail-loud-refuses a violating op); `INV-RESP` (per-op
`response_schema`/`chunk_schema` allow-list; opaque pass-through refuses to load); `INV-BIND` (in-process
startup fail-loud: refuse to serve if bind is routable / socket not 0600); the two-phase audit (value-free
INTENT before egress, OUTCOME after); M1–M6 + the P-M1..P-M6 threat-anchored probe map (rev2 §1.5). rev3/rev4
carry these by reference and restate them as the buildable invariant/probe contract ADA implements and
VERA re-runs against REAL code (§5). The DC3 mock-emit (rev2 §2 — the two catalog TOMLs `vertex-gemini` +
`tailscale`, the frozen `resolve.py`) is carried unchanged; the seal-audit (§3.1) now also scans those
TOMLs.

---

## §0 Problem restatement (6.1 pre-work gate)

Build (this arc, for real, locally/against mocks — no real infra) the credentialed per-provider
pass-through service designed in design-rev2, **as the CONSOLIDATION secure core every lane consumes**, not
as a stoa_of_science one-off. A local skill on any consuming lane names a provider + a pre-registered
closed call; the core attaches that provider's server-side key, calls the external API, and returns only
the declared result — the key never leaves the core. The core is reachable ONLY over Tailscale; each
consuming lane holds ONLY a tailnet identity (no Railway token, no SA key, no API keys). rev2's single
security-crux shape (INV-DEST/RESP/BIND, two-phase audit, M1..M6 probes) is correct and carried; the
**new design work is the multi-lane identity/authz model** that lets distinct lanes (science, newswire,
future) share one core while one lane's tag CANNOT reach another lane's provider/operation
(deny-by-default, cross-lane isolation). The build must also pass a **fail-closed seal-audit** (no secret
VALUE anywhere in code/config/catalog/logs — slot NAMES only). This arc builds and probes the service; it
provisions NOTHING real and mints NO secrets (that is Phase 2, separately PRINCIPAL-gated).

**Imported assumptions (named per 6.1):**

1. **Each consuming LANE joins the tailnet under its OWN tag; a lane's identity at the core is
   control-plane-resolved from the Tailscale policy `grants` block, NOT self-asserted.** This is the direct
   generalization of rev2's STRABO-r3-verified single-builder premise (App-Capabilities is
   control-plane-trusted, strip-and-reinjected by serve under the same guarantee as User-Login, v1.92+
   floor). rev3/rev4 assume the SAME mechanism holds per-lane: a node under `tag:<lane>-core-client`
   receives ONLY the capability its tag was granted, and cannot claim another lane's capability. This is a
   generalization of a verified premise, not a new thin premise — but the **per-lane cap-name → lane
   mapping is the ONE new build-time encoding confirmation** (V-ENC-LANE, §2.4), riding alongside rev2's
   existing V-ENC (App-Capabilities on-the-wire encoding).
2. **The newswire STORE lane (nws-1n7) is a credential-FREE consumer** — it consumes the core for the
   shared embeddings/store surface, NOT for credentialed generative egress. Its lane principal is scoped
   (deny-by-default) to store/embed operations only; it is never in the `scopes` of a credentialed
   generative op. (If a future newswire feature needs a credentialed op, that op's `scopes` is explicitly
   widened to include the newswire lane — an explicit, audited change, never a default.)
3. **rev2's carried invariants are build requirements, not aspirations.** INV-DEST/RESP/BIND are
   fail-loud runtime self-checks the REAL build MUST implement as refuse-to-serve / refuse-to-load, not
   log-and-continue. The build is verified by re-running P-M1..P-M6 against the REAL code (directive §6
   DoD), not against mocks-of-the-check.
4. **No real infrastructure, no secrets, no money** (directive §5). Everything is built + probed locally /
   against mocks; the Phase-2 provision boundary is a separate PRINCIPAL-gated step this arc does not cross.

The restatement converges with the brief and the directive. The one place it makes an implicit scope
explicit: assumption 2 (the newswire lane is credential-free and store-scoped) — the directive names
nws-1n7 as "the newswire credential-free STORE," and rev3/rev4 encode that as a concrete deny-by-default
lane scope rather than leaving it implicit. Flagged for ARGUS in §6.

---

## §1 Threat model (carried from rev2 §1.1, extended for the reframe + the seal-audit)

The core is the most security-sensitive component the team has built: **a single internet-egress box that
holds ALL provider API keys for ALL lanes.** Named threats M1..M6 are carried verbatim from rev2 §1.1; the
reframe **sharpens M4** and the seal-audit canon **adds M7**:

| M# | Named threat | Realized how (attack path) | Status in rev4 |
|----|--------------|----------------------------|----------------|
| M1 | SSRF / forward-anything egress | Caller induces an outbound request to an attacker-chosen host (metadata IP, internal svc, exfil endpoint). | CARRIED (INV-DEST; P-M1) |
| M2 | Key-exfil (via response/log) | Caller gets the core to return a provider key in a body/error/log, or route a key to an attacker destination — **including a credential nested at depth ≥ 3 inside a DECLARED field** (an undeclared sub-key of `groundingMetadata`), **a credential-bearing object/dict smuggled under a SCALAR-declared field** (incl. nested in a list — r1), or **a future credential-bearing field mistakenly marked `PASS_WHOLE`** to bypass the allow-list (r2). | **CARRIED + DEEPENED rev5/rev6** (INV-RESP a RECURSIVE allow-list to schema depth — undeclared sub-keys dropped at EVERY depth; **SCALAR drops any object/dict at ANY depth via a recursive dict-scan — r1**; `content` the one documented whole-passthrough exception, and PASS_WHOLE placement is **deny-by-default via a server-side `PASS_WHOLE_ALLOWLIST` the loader enforces at load — r2**; **P-M2 extended** §5.1a) |
| M3 | Identity-header forgery via non-loopback bind | Handler listens on a routable address; a colocated process connects directly, bypassing serve, forging identity headers. | CARRIED (INV-BIND; P-M3) |
| M4 | **Over-broad provider/operator authorization → CROSS-LANE reach** | A tailnet identity reaches an operation it is not scoped for. **Sharpened by the reframe:** one lane's tag reaches ANOTHER lane's provider/operation (e.g. the credential-free newswire lane reaching a credentialed science-only generative op) — **including via an unresolvable-principal resolving to a permissive DEFAULT, or a multi-cap header silently UNIONing two lanes' access.** | **SHARPENED** (INV-LANE startup config + **INV-PRINCIPAL request-time fail-closed** + per-lane `scopes`; **P-M4 extended** with the cross-lane-denial + the unresolvable-principal + the multi-cap clauses — §2.5) |
| M5 | Audit gap | A credentialed call is not durably + attributably recorded. **Extended:** the record must attribute the **lane**, not just the identity class. | CARRIED + lane field (two-phase audit; P-M5) |
| M6 | Quota exhaustion / DoS | A caller floods the core, exhausting shared Vertex quota / core resources. **Extended:** per-identity bucket is now naturally per-lane (each lane = its own tag = its own bucket). | CARRIED + per-lane bucket (P-M6) |
| **M7** | **Secret-value leakage into code/config/catalog/logs (build-artifact key-exfil)** | A real secret VALUE (SA key, Postgres password, Tailscale auth-key, OAuth token) is committed into the tree, a config, a catalog TOML, or an emitted log — exfiltrable via the repo or logs even though the runtime response surface (M2) is clean. **Including via a real-shaped value laundered through the `SEAL_AUDIT_SYNTHETIC_` marker.** | **NEW** (u--84m canon; fail-CLOSED **seal-audit** gate — §3.1; threat-anchored **P-M7**, now with the marked-bypass clause) |

**Honest-claim posture (carried + extended):** M1 and M3 closed BY CONSTRUCTION (no destination input;
no routable listener). M2 channel closed by construction + response redaction a BUILD-TIME-VERIFIED
**RECURSIVE** allow-list property (rev5/rev6): undeclared keys are dropped at EVERY depth — not just the top
two levels — so a credential nested inside a declared field is dropped by construction; a **SCALAR node drops
any object/dict found at ANY depth via a recursive dict-scan** (rev6 r1), so a credential-bearing object
cannot ride an undeclared sub-key of a dict smuggled under a SCALAR slot; `content` is the ONE documented
whole-passthrough exception (the model product, which is not credential-bearing because the ADC bearer is a
request-side header never present in a response body), and **`PASS_WHOLE` placement is deny-by-default —
enumerated in a server-side `PASS_WHOLE_ALLOWLIST` the loader enforces at load (fail-CLOSED), so a future
credential-bearing field cannot be whole-passed by a mistaken marker** (rev6 r2). **M4 closed by construction at the per-lane granularity** (per-(principal, provider,
operation) `scopes`, deny-by-default; INV-LANE startup loader self-check **AND INV-PRINCIPAL request-time
fail-closed resolution** — §2). M5/M6 build-time-verified. **M7 is a fail-CLOSED build-gate property**
(the seal-audit refuses the build on any secret-value match; absence of a finding is the only pass — §3.1).

---

## §2 THE CONSOLIDATION REFRAME — multi-consumer (multi-lane) identity/authz (FIRST-CLASS NEW; ARGUS cold-audits this)

rev2 §1.4.1 already had two identity CLASSES (human operator via `Tailscale-User-Login`; tagged builder
via `Tailscale-App-Capabilities`) but framed for ONE builder/consumer, with per-op `scopes` a coarse class
list `["operators","builders"]`. The core is now the **canonical center multiple LANES consume**. rev3
designed the multi-lane model concretely enough to BUILD; rev4 tightens the **request-time** resolution to
fail closed (r1) and specifies the **multi-cap** rule (r3).

### §2.1 The lane model — one tag, one control-plane-resolved capability, one lane principal

**A LANE is a consuming context with its own tailnet tag and its own authorization envelope.** Concretely
for this arc:

| Lane | Requirement | Tailnet client tag (illustrative — pinned at build) | Capability (grant) | Lane principal at the core |
|------|-------------|-----------------------------------------------------|--------------------|----------------------------|
| **science** | sos--373 (stoa_of_science skills) | `tag:sos-core-client` | `<domain>/cap/science-core-client` | `lane:science` |
| **newswire** | nws-1n7 (credential-free STORE) | `tag:nws-core-client` | `<domain>/cap/newswire-core-client` | `lane:newswire` |
| **(future)** | any future builder | `tag:<lane>-core-client` | `<domain>/cap/<lane>-core-client` | `lane:<lane>` |
| **operators** | human operators (not a lane) | untagged node → `Tailscale-User-Login` | — (operator allowlist `<CORE>_OPERATORS`) | `operators` (identity class) |

The exact tag strings are pinned at build against the deployed tailnet policy (the runbook uses
`tag:stoagen-catalog` for the core node's own auth-key; the lane CLIENT tags are distinct from the core
NODE tag `tag:sos-core`). The illustrative names above are the shape; V-ENC-LANE (§2.4) confirms the exact
strings.

**How a lane maps to a principal (the load-bearing mechanism):** each lane's client tag is granted a
**per-lane capability NAME** in the Tailscale policy `grants` block. serve **opts into each lane's cap name
explicitly** (`--accept-app-caps=<domain>/cap/science-core-client --accept-app-caps=<domain>/cap/newswire-core-client`,
comma-list vs repeated-flag TBD at build — V-ENC-LANE). The core holds a server-side **`LANE_REGISTRY`**
mapping cap-name → lane principal:

```python
LANE_REGISTRY = {                                   # server-side, code — NOT caller data
  "<domain>/cap/science-core-client":  "lane:science",
  "<domain>/cap/newswire-core-client": "lane:newswire",
}
```

**Request-time principal resolution — FAIL-CLOSED, EXPLICIT MEMBERSHIP ONLY (r1 fold; the guarantee
`INV-PRINCIPAL` §2.4 mechanizes).** At request time the core reads the serve-injected, daemon-verified
`Tailscale-App-Capabilities` header (strip-and-reinjected, control-plane-resolved from `grants` — NOT
self-asserted, per rev2's STRABO-r3 finding) and resolves the caller principal by **explicit membership
only**. The rule, stated precisely so no permissive-default build can pass (this is the exact shape ARGUS
flagged as absent in rev3):

```python
def resolve_principal(headers) -> str:                       # returns a principal OR raises Forbidden (403)
    caps    = parse_app_capabilities(headers)                # -> set[str]; {} if header absent/empty/malformed
    login   = parse_user_login(headers)                      # -> str | None

    # 1. LANE resolution — EXPLICIT MEMBERSHIP. A cap yields a lane principal ONLY IF present AND in
    #    LANE_REGISTRY. NO .get(cap, DEFAULT): a lookup MISS is a DENIAL, never a fallback principal.
    lane_principals = { LANE_REGISTRY[c] for c in caps if c in LANE_REGISTRY }   # miss -> not added, NOT defaulted

    # 3. MULTI-CAP — REJECT-AMBIGUOUS (r3 fold). >1 distinct lane principal resolves AND the node is not an
    #    explicitly-registered multi-lane node -> DENY. NEVER a silent union of two lanes' scopes.
    if len(lane_principals) > 1:
        if frozenset(caps) not in MULTI_LANE_NODES:          # explicit registered exception, deny-by-default otherwise
            raise Forbidden("ambiguous multi-lane principal")   # 403, no egress, audited forbidden
        return MULTI_LANE_NODES[frozenset(caps)]             # the explicitly-registered multi-lane principal
    if len(lane_principals) == 1:
        return next(iter(lane_principals))                   # the one resolved lane principal

    # 2. OPERATOR resolution — EXPLICIT ALLOWLIST. An operator yields `operators` ONLY IF login is on the
    #    <CORE>_OPERATORS allowlist. An unlisted login does NOT yield operators.
    if login is not None and login in CORE_OPERATORS:
        return "operators"

    # 4. NEITHER resolved (absent/empty header, a cap outside LANE_REGISTRY, an unlisted/absent login) ->
    #    DENY. NEVER a default/permissive principal.
    raise Forbidden("no resolvable principal")               # 403, no egress, audited forbidden
```

A node under `tag:nws-core-client` receives ONLY `<domain>/cap/newswire-core-client` (its grant), so it can
only resolve to `lane:newswire`. **It CANNOT resolve to `lane:science`** because the control plane never
emits a capability its tag was not granted. And a caller whose principal does not resolve — absent/empty
`App-Capabilities`, a cap outside `LANE_REGISTRY`, or an unlisted `User-Login` — is **DENIED (403, no
egress, audited `forbidden`)**, NOT resolved to any default. The `LANE_REGISTRY.get(cap, DEFAULT)` shape and
any "empty header → benign default class" shape are **explicitly forbidden**: a lookup miss is a denial.

### §2.2 Why per-lane cap NAMES (not one shared cap with a lane field in the payload)

Two representable options; rev3 chose per-lane cap **names** and recorded why (ARGUS CONFIRMED this choice
sound — a genuinely stronger fail-closed boundary):

- **CHOSEN — per-lane cap name (`<domain>/cap/<lane>-core-client`), mapped by `LANE_REGISTRY`.** The serve
  `--accept-app-caps` opt-in is per-cap-name and **fail-closed**: a lane whose cap name the core did NOT
  opt into gets NO header → auth fails closed. This makes "which lanes does this core serve" an **explicit,
  auditable serve-invocation list** and a fixed server-side cap-name → principal map — no parsing of a
  `lane` sub-field that could be absent/malformed/duplicated.
- **REJECTED — one shared cap name with a `{"lane": "..."}` field in the payload.** It would let a new lane
  be added by a grant change alone (no serve-flag change), which is convenient but WRONG for a security
  boundary: it moves "which lanes are served" out of the explicit fail-closed serve invocation and into a
  payload field the core must parse and trust. The payload IS control-plane-resolved (so the `lane` value
  would be trustworthy), but the fail-closed default is weaker: forget to update a scope and a new lane
  silently rides the shared cap. Per-lane names keep the deny-by-default posture at the serve boundary.

### §2.3 Per-op `scopes` generalized from identity CLASS to lane PRINCIPAL (deny-by-default preserved)

rev2's `scopes: ["operators", "builders"]` (class-level) generalizes to a list of **principals**, where a
principal is either the `operators` class or a `lane:<name>` lane principal:

```python
PROVIDER_REGISTRY["vertex"]["operations"] = {
  "generate_grounded": { ..., "scopes": ["operators", "lane:science"] },            # credentialed generative — science + operators ONLY
  "embed":             { ..., "scopes": ["operators", "lane:science", "lane:newswire"] },  # shared embeddings — both lanes
  # a hypothetical newswire-only store op:
  # "store_fetch":      { ..., "scopes": ["operators", "lane:newswire"] },
}
```

**Deny-by-default, per-(principal, provider, operation):** at request time the core resolves the caller's
principal via `resolve_principal` (§2.1 — fail-closed, explicit-membership) and checks membership in the
op's `scopes`. Not a member → `403`, **no egress**, audited `forbidden`. This is M4 closed at LANE
granularity:

- The **newswire lane calling `generate_grounded`** → principal `lane:newswire` ∉ `["operators","lane:science"]`
  → `403`, no egress. **One lane's tag cannot reach another lane's provider/op.**
- The **science lane calling `embed`** → `lane:science` ∈ scopes → authorized.
- A future lane is **not in ANY existing op's `scopes` until explicitly added** — so onboarding a lane
  grants it ZERO access by default; access is an explicit, audited `scopes` edit per op.
- **An unresolvable principal never reaches the `scopes` check at all** — `resolve_principal` raised
  `Forbidden` first (§2.1 clause 4), so there is no principal to (mis)match against a permissive default.

### §2.4 `INV-LANE` (startup config) + `INV-PRINCIPAL` (request-time) — the invariants guarding the multi-lane authz (fail-loud)

Paralleling INV-DEST/RESP/BIND, the reframe adds **two** structural invariants that make the multi-lane
authz mechanically guarded, not prose. rev3 had `INV-LANE` (a STARTUP config check); rev4 adds the distinct
**request-time** `INV-PRINCIPAL` — the exact gap ARGUS r1 flagged (INV-LANE guards startup config; nothing
guarded request-time resolution).

**`INV-LANE` (registry + serve consistency, in-process fail-loud at STARTUP):**
1. **Every `scopes` entry across the WHOLE `PROVIDER_REGISTRY` resolves to a KNOWN principal** — either
   the `operators` class or a lane principal present in `LANE_REGISTRY`. A `scopes` entry referencing an
   unknown/typo'd `lane:<x>` → the loader **refuses to serve** (fail-loud exit). (Prevents a typo'd scope
   silently denying-all OR — worse — a mis-parse widening access.)
2. **The serve `--accept-app-caps` set equals the `LANE_REGISTRY` cap-name set** — every opted-in cap has a
   lane principal home, and every registered lane principal is actually served (no cap opted-in with no
   principal → an unmapped identity; no principal with no served cap → a dead scope). Mismatch → refuse to
   serve. (This is the fail-closed "which lanes are served" consistency check that makes §2.2's chosen
   design mechanical.)
3. **Lane principals are DISJOINT from the operator class and from `params`/`skill_id`** — a lane principal
   is derived ONLY from the control-plane-resolved cap, never from caller envelope data (same disjointness
   fence as INV-DEST). `skill_id` cannot masquerade as a lane.

**`INV-PRINCIPAL` (request-time principal resolution, fail-closed on EVERY request) — NEW (r1 fold):**
The request-time counterpart to INV-LANE. Where INV-LANE guarantees the CONFIG is consistent at startup,
INV-PRINCIPAL guarantees **every request resolves a principal by explicit membership or is DENIED** — no
request path resolves to a permissive default. Precisely:
4. **Explicit-membership resolution only.** A lane principal is yielded ONLY by a cap that is BOTH present
   in the caller's control-plane-resolved `App-Capabilities` AND a key of `LANE_REGISTRY` (`c in
   LANE_REGISTRY` — never `LANE_REGISTRY.get(c, DEFAULT)`). `operators` is yielded ONLY by a `User-Login`
   present in the `<CORE>_OPERATORS` allowlist. The `.get(cap, DEFAULT)` shape and any "absent/empty header
   → benign class" shape are **forbidden** — a miss is a denial, not a fallback.
5. **Unresolvable → DENY (fail-closed).** If NO principal resolves — absent/empty/malformed
   `App-Capabilities`, a cap outside `LANE_REGISTRY`, an unlisted or absent `User-Login` — the request is
   **DENIED: 403, ZERO egress, audited `forbidden`**. Never a default/permissive principal, never a
   fall-through to a lane or to `operators`.
6. **Multi-cap → REJECT-AMBIGUOUS (fail-closed; r3 fold).** If >1 distinct lane principal resolves and the
   node's cap-set is not an explicitly-registered `MULTI_LANE_NODES` entry, the request is **DENIED (403,
   no egress, audited `forbidden`)** — the core NEVER silently UNIONs two lanes' scopes. An intentional
   multi-lane node is a deliberate, registered exception (`MULTI_LANE_NODES: dict[frozenset[cap], principal]`),
   deny-by-default otherwise.

INV-PRINCIPAL is verified the same two ways as its siblings: the `resolve_principal` structure makes an
unresolvable/ambiguous principal representable-but-caught (raises `Forbidden`, never returns a default), and
the **request handler denies (403, no egress) on any `Forbidden`** — it does NOT fall through to a
permissive class. This is the request-time invariant P-M4's NEW unresolvable-principal + multi-cap clauses
now assert (§2.5). INV-LANE (startup) and INV-PRINCIPAL (request-time) together close M4: the config is
consistent at load AND no request resolves to a default at runtime.

### §2.5 Reframe consequences for audit, rate-limit, and the threat-anchored probe

- **Audit (M5) carries the lane.** The two-phase INTENT record (rev2 §1.4.2) adds `lane` (the
  control-plane-resolved lane principal) alongside `identity_class` and `skill_id`, so every credentialed
  egress is attributable to WHICH LANE made it, not just which identity class. A DENIED request (§2.1
  clause 4 / INV-PRINCIPAL) is audited `forbidden` with the reason (`no resolvable principal` /
  `ambiguous multi-lane principal` / out-of-scope) — still value-free (`params_digest`, never values; no
  credential; no body).
- **Rate-limit (M6) is naturally per-lane.** Each lane = its own tag = its own per-identity token bucket,
  so one lane cannot exhaust another lane's bucket. The optional per-`(lane, skill_id)` sub-bucket (rev2
  r6) gives intra-lane fairness. The per-lane (tag) bucket remains the security boundary.
- **Threat-anchored probe P-M4 (extended, §6.13):** the probe exercises the M4 attack path (a caller
  reaching an op it is not scoped for, INCLUDING via a permissive-default resolve or a multi-cap union),
  asserting BOTH halves:
  - **(a) attack-blocked — THREE sub-paths, each must FAIL a broken build:**
    - **(a.1) MAPPED cross-lane denial:** a `lane:newswire`-tagged caller invokes `vertex.generate_grounded`
      (scopes `["operators","lane:science"]`) → `403`, **ZERO egress** (egress recorder empty), audited
      `forbidden` with `lane:newswire` attributed.
    - **(a.2) UNRESOLVABLE-PRINCIPAL denial (NEW — r1; falsifies the permissive-default build):** a caller
      presenting (i) an **unmapped cap** NOT in `LANE_REGISTRY`, and (ii) an **absent/empty
      `App-Capabilities` header with no allowlisted `User-Login`** → **EACH** → `403`, **ZERO egress**,
      audited `forbidden`. The probe asserts denial **on the unmapped/absent path itself** — so a build that
      resolves either to a default/permissive principal (`LANE_REGISTRY.get(cap, DEFAULT)` or empty-header→
      benign-class) **FAILS this probe** (it would return non-403 / non-empty egress). This is the clause
      that catches the exact failure rev3's P-M4 could not.
    - **(a.3) STRUCTURAL loader/refuse (carried):** the startup loader **refuses to serve** on a
      deliberately-planted violating registry (an op whose `scopes` references an unknown `lane:ghost`, and a
      serve invocation whose opted-in caps ≠ `LANE_REGISTRY`) — INV-LANE. PLUS a **multi-cap** structural
      case (r3): a caller whose control-plane caps resolve to >1 lane principal and whose cap-set is NOT a
      registered `MULTI_LANE_NODES` entry → `403`, no egress (asserts reject-ambiguous, NOT a silent union).
  - **(b) legit-unaffected:** a `lane:science`-tagged caller invokes the SAME `generate_grounded` op →
    authorized, reaches only the pinned Vertex host, succeeds; a `lane:newswire`-tagged caller invokes
    `vertex.embed` (a lane it IS scoped for) → authorized; and a registered `MULTI_LANE_NODES` node (if any
    is configured in the probe) resolving its declared principal → authorized for that principal's scopes.
    (The r1/r3 tightenings did not defeat cross-lane isolation by breaking a lane's legitimate in-scope
    access, and did not deny a legitimately-registered multi-lane node.)

**HONEST residual (carried + added to §6 for ARGUS):** the trusted boundary is the **tag → control-plane
capability → lane principal**. `skill_id` remains a **caller-declared attribution label, NOT a security
boundary** — a hostile builder within a lane can mislabel `skill_id` but CANNOT cross to another lane
(different tag, different control-plane capability). Cross-lane isolation rests on the SAME strip-and-reinject
+ INV-BIND (0600/loopback) precondition as rev2's single-builder identity — if that precondition breaks,
ALL lane identities are forgeable, exactly as ALL of rev2's identities were. The reframe adds no NEW trust
assumption beyond "the control plane resolves per-tag caps correctly," which is the verified rev2 premise
applied N times.

---

## §3 The 3 mandatory canons, folded as BUILD requirements

### §3.1 Seal-every-secret + fail-CLOSED seal-audit (u--84m lesson, made a build GATE — mitigates M7)

rev2's `assert_value_free` checks the `ProvisioningSpec`/`RunLedger` OBJECTS. rev3/rev4 extend this into a
broader, **fail-CLOSED seal-audit** the whole BUILD/EMIT must pass — the u--84m lesson ("seal every secret;
the audit fails closed") made a gate:

**`seal_audit(tree_paths, emitted_logs)` — a deterministic build-time gate, fail-CLOSED:**
- **Scans:** every tracked file in the build (service code, config, the catalog TOMLs `vertex-gemini.toml`
  + `tailscale.toml`, any startup/registry config) **PLUS** every emitted log / audit-ledger artifact the
  build produces.
- **Refuses the build (non-zero exit — the build FAILS) on ANY match of a secret-VALUE shape:**
  - A secret NAME bound to a non-empty VALUE (e.g. `GCP_SA_KEY_B64=<nonempty>`, `POSTGRES_PASSWORD: <value>`,
    `TS_AUTHKEY=tskey-...`). The slot NAME alone is allowed (it is a name); a VALUE bound to it is refused.
  - Known secret-value SHAPES: `tskey-auth-...` / `tskey-...` (Tailscale auth-keys); base64 blobs above a
    length/entropy floor resembling an SA-key JSON; `-----BEGIN PRIVATE KEY-----`; `sk-ant-` and
    `sk-ant-oat01-` (Anthropic API / OAuth tokens); Postgres URIs carrying an inline password
    (`postgres://user:<pw>@host`).
- **Constrained synthetic exemption — the ONLY things that may match a secret shape and still PASS
  (r2 fold — closes the universal-bypass ARGUS flagged):** rev3 made `SEAL_AUDIT_SYNTHETIC_` an
  UNCONDITIONAL pass token, so a real-shaped secret carrying the prefix was waved through. rev4 constrains
  the exemption to the **INTERSECTION of two conditions — BOTH must hold, or the value FAILS the build:**
  1. **Path-bound.** The match is located within the **designated test-fixtures path** (e.g.
     `tests/fixtures/seal_audit/` — the exact path pinned at build). A marker-carrying value found ANYWHERE
     ELSE — service code, config, the catalog TOMLs, an emitted log/audit-ledger line — is **NOT exempt and
     FAILS the build**, marker notwithstanding. (A real secret is never legitimately marked-synthetic in
     production code or an emitted log.)
  2. **Shape-clean.** The marked token itself does **NOT** match any real-secret SHAPE. The exemption
     applies to a fixture of the form `SEAL_AUDIT_SYNTHETIC_<obviously-fake-body>` where the body does NOT
     satisfy any real-secret regex (not a valid `tskey-auth-...`, not a base64 blob above the entropy floor,
     not a PEM `BEGIN PRIVATE KEY`, not `sk-ant-...`, not a Postgres URI with an inline password). **A value
     that matches BOTH the marker AND a real-secret shape** (e.g.
     `SEAL_AUDIT_SYNTHETIC_tskey-auth-kX9f...<real-shaped-body>`) **is FAILED even when marked** — the
     marker CANNOT launder a real-shaped value. Precedence rule: **real-secret-shape match FAILS the build
     regardless of the marker** (the shape test is applied to the value with the marker prefix stripped;
     if the remainder matches a real shape, it FAILS).
  - Net rule stated once: a secret-shaped match PASSES **iff** it is `path-bound (in the designated
    fixtures path) AND shape-clean (the demarked body matches no real-secret shape)`. Otherwise it **FAILS
    the build**. The marker is now a **necessary-but-not-sufficient** condition gated behind path + shape,
    NOT a sufficient one. Bare slot NAMES (documented placeholders, no bound value) remain allowed
    everywhere (a name is not a value).
- **Fail-CLOSED posture (the u--84m core):** absence of a finding is the ONLY pass. An ambiguous
  high-entropy match the audit cannot classify is treated as a FAILURE, not waved through — the audit fails
  CLOSED, never open. This is the deterministic, unbypassable floor for the high-risk "secret value in the
  artifact" case (consistent with the PRINCIPAL's "deterministic unbypassable floor for high-risk"
  posture — it is code, not an LLM judgment).

**GCP notes folded (directive §4 / stoa--re9):** the Vertex credential is a **service-account (ADC) key**
`GCP_SA_KEY_B64` — **SA-auth, NOT an API key**; there is **no AI-Studio API-key path** (so the seal-audit
does not expect and must not permit a `GEMINI_API_KEY`-style value). The one Vertex SA covers
**embeddings + search + generative** (NOT Google Maps — Maps is a separate `gcp_api` with its own key,
out of scope here). The **prepaid card is the only hard spend cap** — a **Phase-2 concern**, noted here so
the build does not attempt any spend-cap wiring (there is nothing real to cap this arc).

**Threat-anchored probe P-M7 (§6.13):** exercises the M7 attack path directly, now INCLUDING the marked-
bypass path (r2):
- **(a) attack-blocked — TWO sub-paths, each must FAIL a broken build:**
  - **(a.1) UNMARKED real-shaped value (carried):** plant a real-SHAPED secret VALUE (an unmarked
    `tskey-auth-...` string AND a base64 SA-key-shaped blob) into a catalog TOML and into an emitted log
    line → assert the build `seal_audit` **REFUSES (non-zero, build fails)** at each planted site; grep
    confirms the audit named the offending path.
  - **(a.2) MARKED real-shaped / mis-placed value (NEW — r2; falsifies the marker-bypass build):** plant
    (i) a **real-SHAPED secret carrying the `SEAL_AUDIT_SYNTHETIC_` prefix** (e.g.
    `SEAL_AUDIT_SYNTHETIC_tskey-auth-<real-shaped-body>`) inside the designated fixtures path, AND (ii) a
    **properly-marked obviously-fake value placed OUTSIDE the fixtures path** (in a catalog TOML / an
    emitted log) → assert the build **STILL FAILS** at EACH (the first because the demarked body matches a
    real shape; the second because it is outside the path-bound fixtures dir). A build treating the marker
    as an unconditional pass token would let these through and **FAILS this probe**.
- **(b) legit-unaffected:** with only slot NAMES (documented placeholders) present everywhere, and
  `SEAL_AUDIT_SYNTHETIC_`-marked **obviously-fake, shape-clean** fixtures present **within the designated
  fixtures path**, the build seal-audit **PASSES** (the gate did not break a clean build by flagging the
  legitimate slot names or the properly-placed, shape-clean marked fixtures).

**Classification (6.12 A3 author duty — I PROPOSE, ARGUS CONFIRMS; CONFIRMED in the rev3 audit):** the
seal-audit is a **threat-ratified mitigation** — it mitigates the named threat M7 (secret-value leakage /
build-artifact key-exfil, ratified by the u--84m canon in directive §4). Its A3 map row + threat-anchored
probe are in §5. (Contrast: the DC3 emit itself remains NOT threat-ratified — rev2 §2.7, ARGUS-confirmed —
but the seal-audit GATE over the whole tree/logs is threat-ratified because it breaks a real key-exfil
attack path. The r2 tightening does not change this classification — it closes a bypass IN the already-
threat-ratified mitigation.)

### §3.2 Railway-setup skill (sos--1bk) — the Phase-2 provisioning-choreography reference (NOT executed this arc)

The real provisioning of the core (Railway project + `db`/`serving` services, GCP SA, tagged Tailscale
node, spend cap) is **Phase 2 — separately PRINCIPAL-gated; this arc provisions NOTHING real.** When Phase 2
runs, its provisioning choreography follows **the Railway-setup skill sos--1bk** together with the runbook
§6 order (repo + Railway services FIRST with secret NAMES declared and values empty; THEN mint each secret
straight into the existing Railway service var — never stashed locally first), reusing the already-proven
`newswire-builder-setup` + `railway-keyring-deploy` skills. rev4 names sos--1bk as the reference ONLY;
it does not invoke it, does not stand up anything, and mints no secret. (Directive §5 SCOPE FENCE.)

### §3.3 In-harness-workflows canon (any LLM adjudication runs in-harness on subscription OAuth)

Per the ratified canon (`docs/research/anthropic-workflows-report.md` §4): **any LLM-adjudication step runs
IN-HARNESS on subscription OAuth — NEVER a keyed CI call (`ANTHROPIC_API_KEY`), and NOT routed through
`CLAUDE_CODE_OAUTH_TOKEN` for a shared pipeline** (the subscription OAuth token is licensed for individual
interactive use; a shared/automated pipeline through it risks an account ban under Anthropic's ToS).

**Operative consequence for THIS design:** the pass-through **service has NO LLM-adjudication step** — it is
deterministic request/response (§4). So there is nothing in the runtime to route to a keyed call. The
**seal-audit (§3.1) is deterministic code (regex/shape-match over the tree/logs), NOT an LLM call** — which
is exactly correct per the workflows-report §3 design rule: *put the high-risk, must-be-exact decision in a
deterministic code leaf.* Should any FUTURE fuzzy residual arise (e.g. a heuristic body-prose secret-leak
detector BEYOND the deterministic shape-match), it would be a **committed in-harness `.claude/workflows/`
workflow on subscription OAuth (adversarial-verify + voting + schema output), never a keyed CI call** — the
policy-safe key-free home. This arc introduces no such residual; the note fixes the pattern for later.

---

## §4 THE WORKFLOW-VS-APP-CODE CALL (answered inline, honestly)

**CALL: application code — a request/response pass-through. NO Stoa Workflow is warranted.** *(ARGUS
CONFIRMED this call correct in the rev3 audit; carried UNCHANGED.)*

**Reasoning (per the workflows-report §3 design rule):** the report's rule is *put the high-risk,
must-be-exact decision in a deterministic code leaf; wrap only a genuinely LLM-fuzzy residual in a
workflow (to raise its reliability via voting/adversarial-verify).* Every security-load-bearing element of
this service is a **deterministic code leaf with NO fuzzy LLM-adjudication residual**:

- INV-DEST (destination built from FIXED/ENUM slots; disjointness; redirect-OFF) — pure code.
- INV-RESP (per-op response/chunk allow-list serializer, RECURSIVE to schema depth; SCALAR drops any object at any depth via a recursive dict-scan; `content` the one documented whole-passthrough, `PASS_WHOLE` placement deny-by-default via a loader-enforced `PASS_WHOLE_ALLOWLIST`) — pure code.
- INV-BIND (in-process refuse-if-routable / 0600) — pure code.
- INV-LANE (cap-name → lane principal map; per-op `scopes` deny-by-default; loader consistency check) — pure code.
- INV-PRINCIPAL (request-time explicit-membership resolution; unresolvable → 403; reject-ambiguous multi-cap) — pure code.
- The two-phase audit (INTENT-before-egress, OUTCOME-after) — pure code.
- The seal-audit (secret-value shape-match, fail-closed, path-bound + shape-clean exemption) — pure code (§3.3).

There is **no step where an LLM must make a judgment** — the pass-through validates a closed envelope
against a closed registry, attaches a server-side credential, calls a pinned host, and allow-list-filters
the response. A workflow raises the *statistical reliability of a fuzzy verdict*; it **cannot make a
security invariant more exact than the deterministic code already makes it** — using one here would be
strictly worse (it would replace an exact, unbypassable code check with a probabilistic one). This matches
the prior increment's engine=app-code / no-workflow ratification for SUGGEST. **No workflow is manufactured
to have one.**

*(Classification: this call is a build-engine decision, **not threat-ratified** — no runtime attack path;
the threat-relevant consequence, seal-audit-as-deterministic-code, is covered by M7 in §3.1/§5. ARGUS
CONFIRMED the carve-out is correct, not self-asserted.)*

---

## §5 BUILD-facing invariant + probe contract (what ADA implements, VERA re-runs against REAL code)

This restates the carried rev2 invariants/probes (NOT redesigned) PLUS the rev3/rev4 additions, as the
concrete build + verification contract. Directive §6 DoD: all probes PASS against the **REAL** code; INV-*
hold and are **fail-loud verified** (a violation refuses to start / refuses to respond / denies the request
/ fails the build — it does NOT warn-and-continue).

### §5.1 The invariants the build MUST implement as fail-loud (refuse-to-serve / refuse-to-load / deny-request / fail-build)

| Invariant | What it guarantees | Fail-loud mechanism | Carried / new |
|-----------|--------------------|--------------------|--------------|
| `INV-DEST` | No caller-supplied destination is constructable | `url_slots` FIXED/ENUM only; `params`/`skill_id` disjoint; redirect-OFF; loader **refuses to serve** a violating op | CARRIED (rev2 §1.2.1) |
| `INV-RESP` | No credential byte reaches a caller via the response — at ANY depth, incl. objects smuggled under a SCALAR slot or a mis-marked whole-pass field | per-op `response_schema`/`chunk_schema` allow-list applied **RECURSIVELY to schema depth** (an undeclared key dropped at EVERY level); **`SCALAR` drops any object/dict at ANY depth via a recursive dict-scan (r1)**; `content` the one documented `PASS_WHOLE` exception, **`PASS_WHOLE` placement deny-by-default via `PASS_WHOLE_ALLOWLIST` (r2)**; op with no schema, a legacy depth-2 (bare-`list`) node, **OR a non-allowlisted `PASS_WHOLE` field → refuses to load** | CARRIED (rev2 §1.3.1), **DEEPENED rev5 + rev6 (§5.1a)** |
| `INV-BIND` | Identity headers are trustworthy (no routable listener) | in-process startup check: **exits non-zero** if bind is routable / socket not 0600 | CARRIED (rev2 §1.4.3) |
| `INV-LANE` | Registry+serve config is consistent (no unmapped/dead/typo'd principal) at STARTUP | every `scopes` entry resolves to a known principal; serve caps == `LANE_REGISTRY`; principals disjoint from caller data; loader **refuses to serve** on violation | **NEW rev3 (§2.4)** |
| `INV-PRINCIPAL` | Every REQUEST resolves a principal by explicit membership or is DENIED — no permissive default, no silent multi-cap union | explicit-membership resolution (no `.get(cap, DEFAULT)`); unresolvable → **403, no egress, audited forbidden**; >1 lane principal on a non-registered node → **403** (reject-ambiguous); handler denies on `Forbidden`, never falls through | **NEW rev4 (§2.4; r1+r3 fold)** |
| seal-audit | No secret VALUE in code/config/catalog/logs | shape-match scan; **build FAILS non-zero** on any secret-value match; exemption ONLY for path-bound + shape-clean marked fixtures; fails CLOSED | **NEW rev3, constrained rev4 (§3.1; r2 fold)** |

### §5.1a INV-RESP depth-completeness — recursive allow-list to schema depth (rev5 fold; closes the VERA depth-2 finding)

**The finding (VERA V-M2-RESP, FM-ratified FIX-NOW).** `redact_response` (redact.py) is a **DEPTH-2**
allow-list. Its `response_schema` is `{top_key: [allowed_sub_key, ...]}`; for each declared top_key it keeps
only the listed sub-keys but emits each sub-key's VALUE **WHOLE**
(`{k: v for k, v in elem.items() if k in allowed}`) and **never recurses into `v`**. So a credential planted
at depth ≥ 3 inside a DECLARED field — an undeclared sub-key of `candidates[].groundingMetadata`, or a nested
field under `candidates[].content` — is emitted whole. No design ASSERTION is falsified (P-M2 was scoped to
UNDECLARED top/sub fields, all PASS), and the realistic Vertex exfil surface is closed (the core's ADC bearer
is a REQUEST-side `Authorization` header, never present in a Vertex response body; `groundingMetadata` is
upstream search metadata that does not carry the core credential). But it is the partial opaque-passthrough
INV-RESP nominally disallows, and it must hold BY CONSTRUCTION so a FUTURE op/provider with a
credential-adjacent nested declared field is covered before this build relays to the Phase-1 SECURITY gate.

**Choice: the GENERAL RECURSIVE form (brief option a), with `groundingMetadata` a nested OBJECT node as its
concrete instantiation (which subsumes option b).** Why the general form over a one-field `groundingMetadata`
allow-list: it makes INV-RESP hold at ALL depths for ALL ops/providers, not just the one field VERA probed;
whole-passing becomes **OPT-IN and explicit** (a `PASS_WHOLE` marker), so no field can be whole-passed by
accident; and the loader can **REFUSE the legacy depth-2 form**, so a regression fails closed AT LOAD rather
than leaking at runtime. Option (b) alone would re-close only the probed field and leave the next nested
declared field a live hole — exactly the future-op risk the FM named.

**The recursive schema grammar (what ADA implements).** A `response_schema` is a NODE tree; every declared key
maps to an EXPLICIT node — there is no bare `list[str]` "keep these, pass each whole" leaf anymore (that leaf
WAS the depth-2 bug). A node is exactly one of:

1. **OBJECT node** — a `dict[str, node]`. Applied to a **dict** value: keep ONLY the declared keys, each value
   recursively filtered by its child node; every UNDECLARED key is DROPPED. Applied to a **list** value: apply
   the object node **element-wise** (each element is a dict filtered by this node; a non-dict element is
   dropped). Applied to a **scalar** value: structurally unexpected → DROP.
2. **`SCALAR` leaf** — the value passes **iff it contains NO object (dict/mapping) at any depth**: a JSON
   primitive (str/num/bool/null), or an array of (recursively) primitives. A value carrying an object
   anywhere under a `SCALAR` node is structurally unexpected → DROP. **This is a BY-CONSTRUCTION rule of the
   NODE grammar, implemented as a RECURSIVE DICT-SCAN, NOT a shallow top-level check (rev6 r1).** The SCALAR
   handler recurses into every list / nested container under the value and **refuses to emit ANY mapping found
   at ANY depth** — only true scalar leaves and (recursively) arrays-of-scalars pass; the whole value is
   dropped if a mapping is found anywhere in it. **A shallow-SCALAR implementation that drops only a top-level
   dict but passes a list-containing-a-dict (or any array whose elements carry dicts) is NON-CONFORMANT** —
   it leaves the SCALAR-slot smuggle path open (a credential-bearing dict riding through under a SCALAR leaf)
   and FAILS P-M2(a.3) §below. This is what forces every object-bearing field to be an explicit OBJECT node:
   a credential cannot ride an undeclared sub-key of an object smuggled under a `SCALAR` slot, because the
   recursive scan drops the whole object-bearing value.
3. **`PASS_WHOLE` leaf — the ONE explicit, documented whole-passthrough exception** (see below). The value
   passes whole regardless of type. It MUST be declared per-field with a rationale; it is never a default and
   is the ONLY escape from recursion. **`PASS_WHOLE` placement is DENY-BY-DEFAULT (rev6 r2):** a field may be
   `PASS_WHOLE` ONLY IF its dotted path is enumerated in the server-side `PASS_WHOLE_ALLOWLIST` (below), which
   the loader enforces at load — a schema marking any non-allowlisted field `PASS_WHOLE` **refuses to load**.

`redact_response` recurses the node tree in lock-step with the value tree: at each level it keeps only declared
keys and recurses their values; at a `SCALAR` leaf it passes a pure-primitive value (else drops); at a
`PASS_WHOLE` leaf it passes the value whole. **A credential planted in ANY undeclared key at ANY depth is
dropped by the "keep only declared keys" rule at that level — the by-construction property.**

**`content` is an INTENTIONAL, DOCUMENTED whole-passthrough (`PASS_WHOLE`) — a named, bounded exception, NOT an
oversight.** `candidates[].content` is the MODEL PRODUCT (`{parts: [...], role}`, where `parts` may carry
arbitrary model-generated structure — text, inline data, function-call parts). It CANNOT be allow-listed
field-by-field without truncating the model's own output, which is the entire deliverable of `generate_grounded`.
It is declared `PASS_WHOLE` with this rationale inline in the registry. This is sound because `content` is NOT a
credential-bearing surface: the ONLY credential the core holds is the Vertex ADC bearer, which is a REQUEST-side
`Authorization` header attached by the core, and it is NEVER present anywhere in a Vertex response body,
`content` included. The exception is bounded to `content` ALONE; `groundingMetadata` (upstream search metadata)
is NOT `PASS_WHOLE` — it is a recursed OBJECT node, so its undeclared sub-keys ARE dropped.

**`PASS_WHOLE_ALLOWLIST` — the server-side, code-level enumeration of the ONLY fields that may be
`PASS_WHOLE` (rev6 r2; deny-by-default).** The `content` carve-out above is bounded by DOCUMENTATION and
reviewer convention in rev5, but the loader validated node TYPES only, not WHERE `PASS_WHOLE` may appear —
so a FUTURE provider that returns a credential IN its response body could have that field mistakenly marked
`PASS_WHOLE` and bypass INV-RESP at runtime, with no mechanical catch (the seal-audit scans the tree/logs at
BUILD time, never runtime response bodies). This is precisely the future-provider case the general recursive
form was chosen to protect, so the escape hatch must be mechanically bounded, not convention-bounded. rev6
enumerates it in code:

```python
# secure_core/redact.py (or registry.py) — server-side, code, NOT caller data.
# The ONLY dotted-path fields that may be marked PASS_WHOLE. Deny-by-default: a new PASS_WHOLE
# placement requires an explicit, audited entry here (consistent with INV-LANE / INV-PRINCIPAL /
# seal-audit deny-by-default). This arc = the single model-product field.
PASS_WHOLE_ALLOWLIST = frozenset({"candidates.content"})
```

The dotted path is the schema-root-relative field path (the OBJECT node `candidates` applied element-wise to
the list still yields the field path `candidates.content` — list indices are NOT part of the path). The
INV-RESP loader self-check (below) walks the schema node tree and **REFUSES TO LOAD any schema that marks a
field `PASS_WHOLE` whose dotted path is NOT in `PASS_WHOLE_ALLOWLIST`** (fail-CLOSED at load). Adding a new
whole-passed field is thus an explicit, audited allowlist edit — never a silent per-op marker a reviewer
might miss. This makes the escape hatch deny-by-default like every other trust boundary in the design.

**The rewritten `generate_grounded` `response_schema` (registry.py):**

```python
"response_schema": {
    "candidates": {                          # OBJECT node — applied element-wise to the candidates list
        "content": PASS_WHOLE,               # DOCUMENTED exception: the model product; passes whole
                                             #   (not credential-bearing — the ADC bearer is request-side)
        "finishReason": SCALAR,              # enum string leaf
        "groundingMetadata": {               # nested OBJECT node — RECURSED; an undeclared depth>=3 sub-key DROPPED
            "webSearchQueries": SCALAR,      # list[str]
            "retrievalQueries": SCALAR,      # list[str]
            "groundingChunks": {             # OBJECT node (element-wise over the list)
                "web": {"uri": SCALAR, "title": SCALAR},
                "retrievedContext": {"uri": SCALAR, "title": SCALAR, "text": SCALAR},
            },
            "groundingSupports": {
                "segment": {"startIndex": SCALAR, "endIndex": SCALAR, "text": SCALAR},
                "groundingChunkIndices": SCALAR,
                "confidenceScores": SCALAR,
            },
            "searchEntryPoint": {"renderedContent": SCALAR, "sdkBlob": SCALAR},
            "retrievalMetadata": {"webSearchQueries": SCALAR, "googleSearchDynamicRetrievalScore": SCALAR},
        },
    },
    "usageMetadata": {                       # OBJECT node over the dict value
        "promptTokenCount": SCALAR,
        "candidatesTokenCount": SCALAR,
        "totalTokenCount": SCALAR,
    },
}
```

The `groundingMetadata` sub-tree above is the CURRENT Vertex `generateContent` grounding response shape
(web-verified against Google's current published schema as of this rev — an illustrative-but-grounded seed).
The EXACT sub-keys and depth are **pinned at build** against the real Vertex response — a **`V-RESP-GROUNDING`**
build confirmation, the sibling of V-ENC / V-ENC-LANE, so the design does NOT rest on a memorized upstream
shape (the training-data-staleness discipline). What is INVARIANT regardless of the exact sub-keys:
`groundingMetadata` is a nested OBJECT node (NOT `PASS_WHOLE`), so an undeclared sub-key at any declared depth
is dropped by construction. The **`embed`** op's `response_schema` `{"predictions": ["embeddings"]}` is likewise
migrated to the node grammar: `{"predictions": {"embeddings": SCALAR}}` (predictions is a list of objects;
`embeddings` is a primitive vector).

**INV-RESP loader guard extended (registry.py `_check_inv_resp`).** In addition to "an op with no
response_schema refuses to load" (carried), the loader now **RECURSIVELY VALIDATES the schema node types**:
every node must be an OBJECT `dict`, `SCALAR`, or `PASS_WHOLE`. A bare `list` node (the legacy depth-2 form) or
any unrecognized node type → **refuse to load** (`LoaderError`, fail-loud). This makes a regression to the
whole-pass form fail CLOSED at startup, not leak at runtime — the by-construction guard that keeps the fix from
silently rotting. **PASS_WHOLE-placement check (rev6 r2):** the same recursive walk tracks the dotted path to
each node, and for every `PASS_WHOLE` leaf it asserts the dotted path is in `PASS_WHOLE_ALLOWLIST` — a
`PASS_WHOLE` marker on a field whose path is NOT allowlisted → **refuse to load** (`LoaderError`, fail-CLOSED
AT LOAD). So a future op mis-marking a credential-bearing field `PASS_WHOLE` is caught mechanically at startup,
not left to reviewer convention. (The recursive dict-scan for the SCALAR node — rev6 r1 — is a `redact_response`
RUNTIME property, verified by P-M2(a.3); the PASS_WHOLE-placement check is a LOADER property, verified by
P-M2(a.4). Together they close the two node types the rev5 loader validated only for well-formedness.)

**Threat-anchored probe P-M2 (EXTENDED — rev5 + rev6; §6.13).** The probe exercises the M2 attack path (a
credential echoed into the response), now including the NESTED-declared-field depth (rev5), the SCALAR-slot
object smuggle (rev6 r1), and the PASS_WHOLE mis-placement (rev6 r2). It asserts BOTH halves:
- **(a) attack-blocked:**
  - **(a.1) UNDECLARED field/sub-field/header/error-body (carried):** a credential in an undeclared top field,
    an undeclared candidate sub-key, upstream headers, or an error body → DROPPED from the caller body AND
    absent from BOTH audit phases; error envelope == `{status, provider_error_class}` only.
  - **(a.2) NESTED-DECLARED-FIELD (rev5; falsifies a depth-2 build):** plant a credential VALUE at
    **depth ≥ 3 inside a DECLARED, RECURSED field** — an UNDECLARED sub-key of `candidates[].groundingMetadata`
    (e.g. `groundingMetadata.leaked_bearer = "<mock-cred>"`, and a nested `groundingMetadata.retrievalMetadata.leaked`)
    → assert it is **DROPPED from the caller-facing output AND absent from BOTH audit-phase records**. A
    **depth-2 build** (which whole-passes `groundingMetadata`'s value) EMITS the planted value → **FAILS this
    clause**. This is the clause that guards the depth VERA's adversarial push found open. (Structural companion:
    the loader **refuses to load** a legacy bare-`list` `response_schema` node.)
  - **(a.3) SCALAR-SLOT OBJECT SMUGGLE (NEW — rev6 r1; falsifies a shallow-SCALAR build):** plant an
    **object/dict carrying a credential-shaped value UNDER a SCALAR-declared field** — both directly
    (`finishReason = {"leaked_bearer": "<mock-cred>"}`) AND **nested inside a list** under a SCALAR field
    (e.g. a SCALAR-declared `webSearchQueries = ["ok", {"leaked_bearer": "<mock-cred>"}]`, and a doubly-nested
    `[["ok", {"leaked_bearer": "<mock-cred>"}]]`) → assert the planted object (and its credential value) is
    **DROPPED from the caller-facing output AND absent from BOTH audit-phase records** (the recursive dict-scan
    drops the whole object-bearing value). A **shallow-SCALAR build** (drops only a top-level dict but passes a
    list-containing-a-dict) EMITS the planted object under the list-nested case → **FAILS this clause**. This is
    the clause that forces the recursive dict-scan implementation and closes the SCALAR-slot smuggle the rev5
    grammar named but left unprobed.
  - **(a.4) PASS_WHOLE MIS-PLACEMENT (NEW — rev6 r2; falsifies an unaudited-escape-hatch build):** load a
    `response_schema` that marks a **NON-allowlisted field `PASS_WHOLE`** (e.g. a hypothetical future op whose
    `groundingMetadata.rawProviderResponse` — a field NOT in `PASS_WHOLE_ALLOWLIST` — is marked `PASS_WHOLE`)
    → assert the loader **REFUSES TO LOAD** (`LoaderError` / non-zero / refuse-to-serve). A build whose loader
    validates node TYPES only and **loads the mis-marked schema anyway** → **FAILS this clause** (it would load,
    and at runtime whole-pass the credential-bearing field). This is the structural clause that mechanizes the
    PASS_WHOLE escape-hatch deny-by-default at load, closing the future-provider bypass.
- **(b) legit-unaffected:** a DECLARED nested sub-key passes INTACT — `candidates[].groundingMetadata.webSearchQueries`
  (a SCALAR list of strings) is returned unchanged (recursion did not break the grounding feature); **a
  legitimate scalar value AND a legitimate list of scalars under a SCALAR-declared field pass intact** (the
  recursive dict-scan did not over-drop clean scalar/array-of-scalar values — rev6 r1 (b)); AND
  `candidates[].content` passes **WHOLE** — the **allowlisted** `PASS_WHOLE` exception LOADS (the placement
  guard did not break the legit model-product passthrough — rev6 r2 (b)) and is exercised so the model product
  is not truncated. (The depth/SCALAR/PASS_WHOLE tightenings did not defeat M2 by breaking a legitimate
  declared field, a clean scalar value, or the model output.)

### §5.2 Threat → mitigation → threat-anchored probe map (6.12 A3 author duty + 6.13)

Each threat-ratified mitigation carries `M<n> → attack-path → how-defeated`, and its §3 threat-anchored
probe asserts BOTH (a) attack-blocked AND (b) legit-unaffected. **The verdict's `defeats_via_probe:` cites
these probe ids.**

| M# | Mitigation → attack-path → how-defeated | Threat-anchored probe (id) — carried / new |
|----|------------------------------------------|--------------------------------------------|
| **M1** SSRF | INV-DEST → caller tries to steer the outbound host → destination built ONLY from server-pinned FIXED/ENUM slots, `params`/`skill_id` disjoint, redirect-OFF, loader refuses a violating op | **P-M1** (carried rev2 §1.5 — structural + instance + legit) |
| **M2** key-exfil | INV-RESP (**RECURSIVE** allow-list to schema depth) + channel-by-construction → caller tries to read a key from a response/error/log, **including via a credential nested at depth ≥ 3 inside a declared field, an object/dict smuggled under a SCALAR slot (r1), or a future field mis-marked `PASS_WHOLE` (r2)** → server-side cred, no caller-URL, per-op allow-list drops every UNDECLARED key at EVERY depth (recursive); **`SCALAR` drops any object/dict at ANY depth via a recursive dict-scan (r1)**; `content` the one documented `PASS_WHOLE` exception (model product, not credential-bearing), **`PASS_WHOLE` placement deny-by-default via a loader-enforced `PASS_WHOLE_ALLOWLIST` (r2)**; opaque, legacy depth-2 (bare-`list`), **or non-allowlisted `PASS_WHOLE`** schema refuses to load | **P-M2 EXTENDED (rev5 + rev6 — §5.1a):** (a.1) undeclared field/subfield/header/error dropped [carried]; **(a.2)** credential at depth ≥ 3 in an undeclared sub-key of a declared field → DROPPED from caller + BOTH audit phases (FALSIFIES a depth-2 build); **(a.3 NEW — r1)** object/dict (incl. list-nested) under a SCALAR field → DROPPED from caller + BOTH audit phases (FALSIFIES a shallow-SCALAR build); **(a.4 NEW — r2)** non-allowlisted field marked `PASS_WHOLE` → loader REFUSES TO LOAD (FALSIFIES an unaudited-escape-hatch build); (b) declared nested sub-key intact + legit scalar/list-of-scalars intact + allowlisted `content` LOADS + passes whole |
| **M3** identity forgery | INV-BIND → colocated process connects direct, bypassing serve, forging headers → 0600/loopback only; routable bind refuses to serve; serve strips+reinjects both identity headers | **P-M3** (carried rev2 §1.5 — in-process + external + legit) |
| **M4** cross-lane reach | **INV-LANE (startup config) + INV-PRINCIPAL (request-time fail-closed) + per-lane `scopes` (deny-by-default)** → one lane's tag invokes another lane's op, OR an unresolvable principal resolves to a permissive default, OR a multi-cap header silently unions two lanes → mapped principal not in op's `scopes` → 403; unresolvable/ambiguous principal → 403 (explicit-membership, no `.get(cap,DEFAULT)`, reject-ambiguous); loader refuses an inconsistent registry | **P-M4 EXTENDED (rev4 — §2.5):** (a.1) newswire tag → generate_grounded = 403 no egress; **(a.2 NEW — r1)** unmapped cap AND absent/empty header → EACH 403 no egress (FALSIFIES a permissive-default build); (a.3) loader refuses planted violation + **multi-cap non-registered → 403 (r3)**; (b) science tag → same op authorized, newswire → embed authorized, registered multi-lane node authorized |
| **M5** audit gap | two-phase audit + lane attribution → a crash loses the record of an executed credentialed call → value-free INTENT (incl. `lane`) written BEFORE egress, OUTCOME after; a denied request audited `forbidden` with reason | **P-M5** (carried rev2 §1.5 — crash in egress→outcome window; INTENT survives; + `lane` present, value-free) |
| **M6** quota DoS | per-lane (per-tag) token bucket + shared-quota cap → one lane/skill floods the shared quota → per-lane bucket is the boundary; skill_id sub-bucket optional | **P-M6** (carried rev2 §1.5 — burst 429; second lane unthrottled; skill_id attributed) |
| **M7** secret leakage | **fail-CLOSED seal-audit** → a real secret VALUE lands in code/config/catalog/log, OR a real-shaped value is laundered through the `SEAL_AUDIT_SYNTHETIC_` marker → shape-match scan fails the build non-zero; the marker exempts ONLY a path-bound + shape-clean fixture (a real-shaped or mis-placed marked value STILL FAILS); fails closed | **P-M7 EXTENDED (rev4 — §3.1):** (a.1) planted UNMARKED secret VALUE in a TOML + a log → build REFUSES; **(a.2 NEW — r2)** MARKED real-shaped value in fixtures + MARKED value outside fixtures → build STILL FAILS (FALSIFIES the marker-bypass build); (b) slot-names + shape-clean marked fixtures IN the fixtures path → build PASSES |

**Not-threat-ratified (I PROPOSE, ARGUS CONFIRMS; CONFIRMED in the rev3 audit):** the DC3 mock-emit (rev2
§2.7 — data/config addition, no runtime attack path; §35.5 carve-out) and the §4 workflow-vs-app-code call
(build-engine choice, no runtime attack path) carry no threat-anchored probe of their own.

### §5.3 The build + verification steps (directive §6 DoD)

1. Build the REAL service: `tailscaled → tailscale serve --https=443 --accept-app-caps=<per-lane caps>
   unix:/run/.../core.sock → 0600 AF_UNIX UDS → gated handler → uvicorn`; the closed `PROVIDER_REGISTRY`;
   the `LANE_REGISTRY`; the `resolve_principal` request-time resolver (fail-closed, explicit-membership,
   reject-ambiguous); per-provider handlers; the **RECURSIVE** response allow-list serializer (`redact_response`
   recurses to schema depth over the OBJECT/`SCALAR`/`PASS_WHOLE` node grammar; **the `SCALAR` handler is a
   RECURSIVE dict-scan dropping any object/dict at ANY depth — r1**; `content` the one `PASS_WHOLE`
   exception, its placement bounded by the loader-enforced `PASS_WHOLE_ALLOWLIST` = `{"candidates.content"}` — r2);
   the two-phase audit; the seal-audit gate. Vertex registered as the first provider
   (`generate_grounded` + `embed`, both `auth: adc_sa`).
2. Run **P-M1..P-M7** against the REAL code (locally/against mocks) — all PASS, INCLUDING the P-M2(a.2)
   nested-declared-field clause (a credential at depth ≥ 3 in an undeclared sub-key of a declared field →
   DROPPED from caller + BOTH audit phases; a depth-2 build FAILS it), **the NEW P-M2(a.3) SCALAR-slot clause
   (an object/dict — incl. list-nested — under a SCALAR field → DROPPED from caller + BOTH audit phases; a
   shallow-SCALAR build FAILS it) and the NEW P-M2(a.4) PASS_WHOLE-placement clause (a non-allowlisted field
   marked `PASS_WHOLE` → loader REFUSES TO LOAD; a node-types-only loader FAILS it)**, the P-M4(a.2)
   unresolvable-principal clause, and the P-M7(a.2) marked-bypass clause.
3. INV-DEST/RESP/BIND/LANE each **fail-loud verified** (plant a violation → refuse-to-serve/load; not
   warn-and-continue). **INV-RESP depth-completeness verified** (a legacy depth-2 / bare-`list` `response_schema`
   node → refuse-to-load; a depth ≥ 3 undeclared sub-key of a declared field → DROPPED at runtime; `content`
   passes whole). **INV-RESP r1 SCALAR recursion verified** (an object/dict — incl. list-nested — under a
   SCALAR-declared field → DROPPED at runtime; a legit scalar + a list of scalars pass intact; a shallow-SCALAR
   build FAILS P-M2(a.3)). **INV-RESP r2 PASS_WHOLE-placement verified** (a `response_schema` marking a
   non-allowlisted field `PASS_WHOLE` → refuse-to-load; the allowlisted `candidates.content` loads + passes
   whole). **INV-PRINCIPAL request-time fail-closed verified** (unmapped cap / absent header →
   403 no egress; multi-cap non-registered → 403; a `.get(cap, DEFAULT)`-style resolver FAILS P-M4(a.2)).
   Seal-audit **fail-closed verified** (P-M7, incl. the marked-bypass clause a.2).
4. Frozen resolver byte-identical; the FULL `builder_deploy_core` suite green (re-run, not asserted).
5. NOMOS CONFORMANT; authorship = Denson Smith + seat-identity Co-Authored-By trailers; commit on the
   arc-77 build branch — **NOT merged, NOT pushed** (directive §5/§6).

---

## §6 Self-assessed weak points (6.2 post-work; where ARGUS should push hardest)

Carried from rev3 §6 (which carried rev2's five deltas + the multi-consumer authz delta) PLUS the rev4-fold
notes. The **first** one is the genuinely-novel delta ARGUS cold-audits specifically; wp#1 and wp#2 now note
the r1/r2/r3 tightenings that closed the load-bearing rev3 gaps.

1. **[the reframe delta — r1/r3 TIGHTENED] Can per-lane `scopes` actually DENY cross-lane, does an
   unresolvable principal fail CLOSED, and is the multi-cap rule fail-closed?** The whole multi-lane
   isolation rests on: (i) the control plane resolving per-tag caps correctly (a node gets ONLY its tag's
   cap — the rev2 STRABO-r3 premise applied N times); (ii) `LANE_REGISTRY` cap-name → principal being
   server-side + fail-closed; (iii) INV-LANE catching an unknown-principal scope OR a serve-caps ≠
   LANE_REGISTRY mismatch at load; **(iv) NEW — INV-PRINCIPAL making request-time resolution explicit-
   membership-only, so an unmapped cap / absent header / unlisted login → 403 (never a default), and a
   multi-cap header → reject-ambiguous 403 (never a silent union)**; (v) the SAME INV-BIND / strip-and-
   reinject precondition rev2 depends on. **ARGUS should push hardest on:** does **P-M4(a.2)** actually
   FALSIFY a build that resolves an unmapped cap / absent header to a permissive default (it asserts denial
   ON the unmapped/absent path, not only the mapped path)? does the multi-cap **reject-ambiguous** rule
   (INV-PRINCIPAL clause 6) actually deny a 2-lane non-registered node rather than union its scopes? does
   INV-LANE clause 2 still make a lane un-served-by-omission fail CLOSED (no header) at startup? does adding
   a future lane grant it ZERO access by default? And confirm the honest residual is correctly placed:
   `skill_id` is attribution, the tag→cap→lane principal is the trusted boundary, and the reframe adds NO
   new trust assumption beyond rev2's verified per-tag cap resolution.
   *Why this shape anyway:* per-lane cap names put the "which lanes are served" decision at the fail-closed
   serve boundary; deny-by-default per-op `scopes` over lane principals is the least-privilege
   generalization of rev2's class-level scopes; splitting INV-LANE (startup config) from INV-PRINCIPAL
   (request-time resolution) makes BOTH the config-consistency AND the request-resolution mechanically
   guarded like the INV- siblings rather than prose — the exact gap ARGUS r1 flagged.

2. **[seal-audit — r2 TIGHTENED] The seal-audit's shape-match set is a denominator I do not fully control,
   and the synthetic-marker exemption must not reopen the bypass.** It catches known secret SHAPES
   (Tailscale/SA-key/OAuth/Postgres-URI); a NOVEL secret format not in the shape set could slip. The
   fail-CLOSED posture (ambiguous high-entropy → FAIL) is the mitigation for the shape-set gap. The rev4
   tightening (r2) constrains the `SEAL_AUDIT_SYNTHETIC_` exemption to the **intersection** of path-bound
   (in the designated fixtures path) AND shape-clean (the demarked body matches no real-secret shape), so a
   real-shaped or mis-placed marked value STILL FAILS. **ARGUS should push on:** is the constrained
   exemption genuinely closed — does **P-M7(a.2)** falsify a build that still treats the marker as an
   unconditional pass token (it plants a marked real-shaped value AND a marked out-of-path value and asserts
   BOTH still FAIL)? is the fail-closed-on-ambiguous default still genuinely closed (unclassifiable match →
   build FAILS)? is the path-bound + shape-clean rule narrow enough that it cannot itself become a new
   bypass (e.g. can an attacker place a real secret INSIDE the fixtures path and shape-clean it — no,
   because the shape test FAILS a real-shaped body regardless of path)?
   *Why this shape anyway:* a deterministic shape-match + fail-closed-on-ambiguous is the unbypassable floor
   the PRINCIPAL's posture calls for on the high-risk secret-leak case; binding the marker to path-bound +
   shape-clean (rather than an unconditional token) is the minimum needed to let honest test fixtures
   coexist with a fail-closed audit WITHOUT reopening the universal bypass.

3. **[rev5 + rev6 DEEPENED — the depth-2 gap CLOSED, and the SCALAR-slot + PASS_WHOLE-placement generality
   holes now CLOSED] INV-RESP allow-list completeness across the full node grammar.** rev5 made
   `redact_response` **RECURSIVE to schema depth** (the VERA depth-2 finding); **rev6 completes the
   by-construction generality on the other two node types:** (r1) the `SCALAR` node drops any object/dict at
   ANY depth via a **recursive dict-scan** (not a shallow top-level check) — so a credential-bearing object
   cannot ride an undeclared sub-key of a dict smuggled under a SCALAR slot, and P-M2(a.3) FALSIFIES a
   shallow-SCALAR build; (r2) `PASS_WHOLE` placement is **deny-by-default** via a server-side
   `PASS_WHOLE_ALLOWLIST` the loader enforces at load, so a future credential-bearing field cannot be
   whole-passed by a mistaken marker, and P-M2(a.4) FALSIFIES a node-types-only loader. **All three node types
   are now fully guarded (OBJECT recurses + SCALAR-object-drop + PASS_WHOLE-placement) — the fixed point the
   FM named; there is no r3 in the node grammar.** **Two HONEST
   residuals remain, correctly bounded:** (i) the allow-list is a **KEY** allow-list, not a **value-content**
   secret scanner — a declared `SCALAR` leaf's string value (e.g. a grounding `title`) or the `content` product
   passes whole; this is the correct boundary (M2's realistic surface is closed because the ONLY core credential
   is the request-side ADC bearer, never in a response body; value-content artifact scanning is the seal-audit's
   job, M7), NOT a hole to plug in INV-RESP; (ii) Google adding a nested grounding sub-field a legit feature
   wants surfaced requires declaring it in the node schema (a build-time `V-RESP-GROUNDING` re-pin) —
   allow-list-by-omission fails CLOSED (an undeclared new field is dropped, never leaked). **ARGUS should push
   on:** does **P-M2(a.2)** actually falsify a depth-2 build; does **P-M2(a.3)** actually falsify a
   shallow-SCALAR build (assert the list-nested object under a SCALAR field is EMITTED by a shallow build,
   DROPPED by the recursive dict-scan — AND that a legit scalar / list-of-scalars is NOT over-dropped); does
   **P-M2(a.4)** actually falsify a node-types-only loader (assert a non-allowlisted `PASS_WHOLE` field REFUSES
   TO LOAD, while the allowlisted `candidates.content` LOADS + passes whole); is the `content` `PASS_WHOLE`
   exception genuinely bounded to the allowlisted path (is `groundingMetadata` NOT whole-passed)? does the loader
   guard refuse the legacy bare-`list` node (regression fails closed at LOAD)? *Why this shape anyway:* a
   recursive KEY allow-list with a recursive-dict-scan SCALAR node and an explicit, loader-enforced, allowlisted
   OPT-IN whole-pass is the by-construction form that holds for future ops/providers on ALL three node types;
   value-content scanning belongs to the seal-audit layer, not the response serializer; fail-closed-by-omission
   (and deny-by-default PASS_WHOLE placement) is the right posture for an upstream the core does not own.

4. **[carried r3/V-ENC + V-ENC-LANE, multi-cap NAMED per r3] The App-Capabilities on-the-wire encoding, the
   per-lane cap-name → principal mapping, AND the multi-cap header form are the open build-time
   confirmations.** rev2's V-ENC (App-Capabilities Q-encoded vs serialized-JSON) is joined by **V-ENC-LANE**
   (the exact per-lane cap-name strings; the serve comma-list-vs-repeated-flag form for `--accept-app-caps`;
   **and — NEW per r3 — the on-the-wire form when a node's control-plane caps carry MULTIPLE mapped cap
   names**, so the `resolve_principal` multi-cap branch is exercised against the REAL header shape, and any
   intentional `MULTI_LANE_NODES` entry is pinned against the actual multi-cap encoding), confirmed at build
   against the pinned TS version (≥ v1.94.1). *Why this shape anyway:* the newswire build hit TS-version
   identity-header landmines; pinning the version and confirming the exact encoding + cap strings + the
   multi-cap header form at build is the proven discipline, not a design-time guess.

5. **[carried r1/r5-rev2] INV-DEST/INV-RESP/INV-BIND/INV-LANE (and now INV-PRINCIPAL) are loader/startup/
   request self-checks the build must ship as refuse-to-serve/load/deny, not warnings.** A build that ships
   them as log-and-continue silently weakens the guarantee. **ARGUS should confirm
   P-M1(a)/P-M3(a)/P-M4(a.1-a.3)/P-M7(a.1-a.2) actually FALSIFY a warnings-only / permissive-default /
   marker-bypass implementation** (they assert non-zero exit / refuse-to-serve / 403-no-egress / build-fail,
   not a log line). *Why this shape anyway:* in-process fail-loud + a probe that asserts the exit/denial is
   the strongest design-time mechanism without over-building; it is the A3 author duty (6.13).

6. **[carried] The threat-anchored probes P-M1..P-M7 exercise a service built THIS arc but against
   mocks/locally, not real infra.** They are falsifiable and run against REAL code (directive §6), but the
   real serve/socket/TS-version runtime is Phase 2/3. **ARGUS should pressure-test P-M2 (full-response
   redaction), P-M3(a) (in-process refuse-if-routable), P-M4 (cross-lane + unresolvable-principal denial),
   and P-M7 (marked-bypass) hardest** — the four most dependent on the real serve/socket/identity runtime.
   *Why this shape anyway:* the arc's DoD is a built + locally-probed service that relays up to be
   Phase-1-gated; the probes are the verification contract Phase 3 re-runs against the real deployment.

---

## §7 Out of scope (deliberately not addressed; ADA scope-fence + ARGUS frame)

- **Cross-lane DATA-tenancy within the SHARED pgvector store (r4 — explicitly scoped out; NO fix designed
  here).** The multi-lane authz (§2) closes cross-lane **API-EGRESS ONLY** — which lane may CALL which op.
  It does **NOT** address cross-lane **DATA isolation** inside the shared pgvector store: whether
  `lane:newswire` can READ `lane:science` rows (or vice-versa) is a **store-layer row/tenant-isolation**
  concern, NOT closed by the API-egress authz, and it is **NOT silently assumed closed**. It is a SEPARATE
  concern tracked in ticket **stoa--exn** (store-layer cross-lane data tenancy in the shared pgvector
  store). It does **NOT block this pass-through build** — the pass-through service this arc builds is the
  API-egress boundary; store-layer row isolation is a distinct layer (rev2 §4 step 4 notes the shared
  pgvector DB is the common home for BOTH the KG store AND skill/retrieval embeddings, which is exactly why
  the data-tenancy question exists and must be tracked, not assumed). *Reason: directive r4 = scope-out
  only; the boundary is stated explicitly so ADA does not assume store-data isolation is delivered by this
  build, and ARGUS has the in-dispatch-vs-future frame.*
- **ALL real provisioning** — no Railway project, no GCP SA mint, no Railway secret set, no Tailscale node,
  no DB stand-up, no spend cap wired. Phase 2, separately PRINCIPAL-gated. *Reason: directive §5 SCOPE FENCE;
  this arc builds + probes locally/against mocks only.*
- **Real secrets / money** — mint nothing; the prepaid-card spend cap is a Phase-2 concern. *Reason: §5.*
- **The stoa_of_science + newswire CLIENT skills** — theirs; this design specifies the client CONTRACT
  (rev2 §1.3) + the lane identity model (§2) only. *Reason: ownership split (sos--373 / nws-1n7).*
- **Multi-provider registry beyond Vertex** — the design accommodates N providers; only Vertex is wired now.
  *Reason: Vertex is the first provider; others follow the same registry + response-schema + credential
  boundary.*
- **Lanes beyond science + newswire** — the LANE_REGISTRY + per-lane cap model accommodates future lanes,
  but only science + newswire are registered now; a future lane is added by a grant + a `LANE_REGISTRY`
  entry + explicit per-op `scopes` edits (ZERO access by default). *Reason: consolidation center is built
  for the current two consumers; future lanes onboard explicitly, deny-by-default.*
- **Intentional MULTI-LANE nodes beyond the registered-exception mechanism** — the `MULTI_LANE_NODES`
  registry (§2.1/§2.4) is the deny-by-default exception path for a deliberately multi-lane node; none is
  wired this arc (both current lanes are single-cap). *Reason: reject-ambiguous is the default; an
  intentional multi-lane node is an explicit registered exception added when a real need appears.*
- **Hard per-skill quotas** (a server-trusted per-skill identity) — the named r6 follow-up; the trusted
  boundary is the tag/lane. *Reason: per-skill HARD limits need a server-trusted skill identity, out of
  scope now.*
- **A streaming-gsearch op** — the `chunk_schema` pattern is carried (rev2 §1.3.1) so the build has it; no
  streaming op is wired into the Vertex surface this arc. *Reason: rev1/rev2 ops are `stream: False`.*
- **A fuzzy body-prose secret-leak workflow** — the seal-audit is deterministic shape-match this arc; any
  future fuzzy residual would be a committed in-harness workflow (§3.3), not built now. *Reason: no fuzzy
  residual exists in this service.*
