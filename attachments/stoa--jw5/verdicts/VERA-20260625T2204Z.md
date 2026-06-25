status: completed
ticket: stoa--jw5 (u--9s2 Phase-1)
verdict: pass
design_artifact_verified_against: agents/design/stoa--jw5/design-formal.md
build_verified: agents/design/stoa--jw5/resolution-check/ (resolve.py + fixtures.py + run.py), working tree @ main HEAD 4160b14 (design arc, no branch — pure-logic harness)
probes_executed:
- probe_id: p1
  description: Independently re-implement resolve() from the §2.5 spec (different code path) and confirm it reproduces all three §8 expected sets exactly + agrees with ADA's resolve().
  command_or_method: python vera_probes.py (Part 1 — vera_resolve(), an independent frozenset-based §2.3 implementation NOT copied from resolve.py)
  expected: vera_resolve == §8 expected AND vera_resolve == ada_resolve for §8.1/8.2/8.3 (8/6/7 entries)
  observed: PASS — all three two-impl agreements hold; 8/6/7 exact
  result: pass
  quadrant_classification: easy-easy
- probe_id: p2
  description: Hand-derive the §8.1 prospector (kind,name) set by hand from §3.1 BASELINE ∪ §3.2 geospatial template (delta empty) and compare to resolve()'s output.
  command_or_method: python vera_probes.py (Part 1 — hand_prospector literal set, written by hand, NOT computed by any resolver)
  expected: hand-derived 8-entry set == ada_resolve(§8.1) == §8 expected
  observed: PASS — hand-derived set matches both ADA's output and the §8 expected set byte-for-byte
  result: pass
  quadrant_classification: easy-easy
- probe_id: p3-M4
  description: M4 THREAT-ANCHORED. Drive the baseline-silent-omit / fail-open attack-path by attempting to omit EACH of the 5 §2.6 baseline entries individually, PLUS an omit∩add same-entry (pgvector) case, PLUS a legal category-omit control.
  command_or_method: python vera_probes.py (m4_baseline_omit_fail_closed — 5 baseline-omit drives + omit∩add + postgis-omit control)
  expected: every baseline omit RAISES BaselineOmitError with no set returned (fail-closed); omit∩add same baseline entry STILL raises (guard is step-0); legal category omit (postgis) does NOT raise and drops postgis
  observed: PASS — all 5 baseline omits raise BaselineOmitError (returned=None each); omit∩add(pgvector) still raises; control postgis-omit resolves to a 7-entry set with postgis dropped, no over-blocking
  result: pass
  quadrant_classification: easy-easy
- probe_id: p4-M1
  description: M1 THREAT-ANCHORED. Drive cross-builder lateral movement by deriving SA scope for two distinct builders (prospector vs labstat_bls) at t0 and asserting no entry of one appears in the other's scope, and each scope == exactly the scope-bearing subset of its OWN resolved set.
  command_or_method: python vera_probes.py (m1_cross_builder_lateral — derive_sa_scope on both + cross-membership + overlap assertions)
  expected: (a) builder-B's unique secret BLS_OEWS_API_KEY ABSENT from A's scope AND A's unique google-maps/MAPS_API_KEY ABSENT from B's scope; (b) each scope == own scope-bearing subset (no widen at t0); A∩B overlap == shared baseline scope-bearing set only
  observed: PASS — A_scope excludes BLS_OEWS_API_KEY; B_scope excludes google-maps + MAPS_API_KEY; each scope == own scope-bearing subset; overlap is exactly {gemini-embedding, gemini-search, POSTGRES_PASSWORD} (shared baseline, no builder-specific leak). Verifies §5.A INITIAL-PROVISION (t0) derivation; subtractive prune residual R-1 is honestly Phase-2 (no t0 probe owed).
  result: pass
  quadrant_classification: easy-easy
- probe_id: p5-M3
  description: M3 THREAT-ANCHORED. Drive the enabled-but-keyless 401 attack by constructing a resolved set with (gcp_api,google-maps) but WITHOUT (gcp_secret,MAPS_API_KEY) and asserting check_runtime_completeness FAILS it (the invariant actually catches the gap, not just that the happy path passes).
  command_or_method: python vera_probes.py (m3_keyless_maps_caught — strip MAPS_API_KEY from prospector set, assert ok=False + named missing pairing; full-set positive control)
  expected: keyless set -> ok=False with missing=[((gcp_api,google-maps),(gcp_secret,MAPS_API_KEY))]; full prospector set -> ok=True, no false-positive
  observed: PASS — keyless set fails with exactly the named missing pairing; full set passes clean. M3 key-bearing premise web-reconfirmed (gsearch 2026-06-25): Maps Platform = client-side API key (paired MAPS_API_KEY required); Vertex Gemini + Document AI = ADC/service-account (no minted key) — §3.4 classification is non-stale.
  result: pass
  quadrant_classification: easy-hard
- probe_id: p6-M2
  description: M2 THREAT-ANCHORED (design-property). Drive credential-VALUE-exposure by asserting the resolution/derivation layer materializes (kind,name) SLOTS only — no resolved/derived entry, no baseline/library record, and no resolve() parameter carries a value/secret field.
  command_or_method: python vera_probes.py (m2_no_credential_value — 2-tuple shape check + value-field grep over BASELINE/LIBRARY + resolve() parameter-name inspection)
  expected: every resolved/derived entry is exactly (kind,name); no record carries value/secret/password field; resolve() has no value-bearing parameter
  observed: PASS — all entries are 2-tuples; zero value-field leaks; resolve() params == [manifest, baseline, library]. NOTE (§5.11): initial naive token-match false-positived on the 'PASSWORD' substring inside the POSTGRES_PASSWORD default value rendered in the stringified signature; corrected to inspect parameter NAMES (not the stringified sig with inlined defaults). The false-positive was in MY probe, not the build; fix recorded in methodology_concerns.
  result: pass
  quadrant_classification: hard-easy
- probe_id: p7-M6
  description: M6 THREAT-ANCHORED (design-property; no live mesh in Phase-1). Confirm the design §7/§4-S5 specifies every required mesh-security element; flag any missing.
  command_or_method: python vera_probes.py (m6_mesh_security_design_property — grep design-formal.md for 6 required needles)
  expected: spec specifies deny-by-default + Tailscale-User-Login header-trust identity + never-WhoIs-on-loopback + 0600 AF_UNIX socket + <BUILDER>_OPERATORS allowlist + Funnel OFF
  observed: PASS — all 6 elements present in §7 / §4 S5. No missing element.
  result: pass
  quadrant_classification: hard-easy
- probe_id: p8
  description: Re-execute ADA's own harness verbatim (independence cross-check — re-run, do not re-derive).
  command_or_method: python run.py
  expected: exit 0, 19/19 checks PASS (8/6/7 exact + §8.4 raises BaselineOmitError + runtime-completeness + kind-dispatch + SA-scope)
  observed: PASS — exit 0, 19/19. §8.4 message "omit targets non-omittable baseline entry/entries: [('db_extension', 'pgvector')]", no set returned.
  result: pass
  quadrant_classification: easy-easy
threat_coverage:
- mitigation: M4
  threat: baseline-necessity silently omitted -> fail-open (builder embeds with no vector store -> 500s)
  defeats_via_probe: p3-M4
  probe_evidence: agents/design/stoa--jw5/resolution-check/vera_probes.py (m4_baseline_omit_fail_closed); observed — all 5 baseline omits RAISE BaselineOmitError returned=None; omit∩add(pgvector) still raises; category-omit control (postgis) legal and drops postgis
  attack_path_exercised: drove delta.omit against each non-omittable baseline entry + the omit∩add bypass attempt. (a) attack BLOCKED — every baseline omit fail-closed, no silent partial set; (b) legit category omit NOT over-blocked — postgis omit resolves cleanly.
- mitigation: M1
  threat: cross-builder lateral movement (builder A's SA reads/spends/exfiltrates builder B's secrets/budget)
  defeats_via_probe: p4-M1
  probe_evidence: agents/design/stoa--jw5/resolution-check/vera_probes.py (m1_cross_builder_lateral); observed — A_scope excludes B's BLS_OEWS_API_KEY, B_scope excludes A's google-maps+MAPS_API_KEY, each scope == own scope-bearing subset, A∩B overlap == shared baseline only
  attack_path_exercised: derived SA scope for prospector and labstat_bls at t0 and probed cross-membership. (a) lateral reach BLOCKED — neither builder's unique scope-bearing entry appears in the other's derived scope; (b) legit shared baseline scope (gemini/POSTGRES_PASSWORD) correctly present in both. §5.A t0 derivation; R-1 subtractive prune honestly Phase-2.
- mitigation: M3
  threat: key-bearing API enabled-but-keyless -> 401 at runtime (silent under-provision)
  defeats_via_probe: p5-M3
  probe_evidence: agents/design/stoa--jw5/resolution-check/vera_probes.py (m3_keyless_maps_caught); observed — keyless set ok=False missing=[((gcp_api,google-maps),(gcp_secret,MAPS_API_KEY))]; full set ok=True no false-positive
  attack_path_exercised: constructed the enabled-but-keyless resolved set (google-maps present, MAPS_API_KEY stripped). (a) gap CAUGHT — runtime-completeness fails it naming the exact missing pairing; (b) full prospector set NOT false-flagged. Premise web-reconfirmed (Maps=API-key, Vertex/DocAI=ADC).
- mitigation: M2
  threat: credential VALUE exposure to an agent (a secret value lands in transcript/argv/disk)
  defeats_via_probe: p6-M2
  probe_evidence: agents/design/stoa--jw5/resolution-check/vera_probes.py (m2_no_credential_value); observed — all resolved/derived entries are (kind,name) 2-tuples, zero value-field leaks in BASELINE/LIBRARY, resolve() params == [manifest,baseline,library]
  attack_path_exercised: probed the resolution/derivation layer for ANY place a credential VALUE could be materialized. (a) exposure BLOCKED by construction — model carries only (kind,name) SLOTS; no value field on any entry/record/parameter, consistent with §4 emit-then-apply (value-free spec, slots only); (b) legit slot NAMES still representable.
- mitigation: M6
  threat: unauthorized mesh access to a builder's trigger/data (no-auth, loopback-WhoIs spoof, Funnel exposure)
  defeats_via_probe: p7-M6
  probe_evidence: agents/design/stoa--jw5/resolution-check/vera_probes.py (m6_mesh_security_design_property); observed — all 6 required §7/§4-S5 elements present in design-formal.md
  attack_path_exercised: design-property probe (no live mesh in Phase-1). (a) each named attack vector has a specified defeat — deny-by-default (no-auth), Tailscale-User-Login header-trust + never-WhoIs-on-loopback (spoof), Funnel OFF (exposure), 0600 UDS + <BUILDER>_OPERATORS allowlist; (b) no missing element flagged.
methodology_concerns:
- One self-probe false-positive surfaced and was fixed mid-verification (NOT a build defect): the initial M2 parameter check did `'password' in str(signature)`, which matched the 'PASSWORD' substring inside the POSTGRES_PASSWORD baseline-entry NAME rendered as a default value in the stringified signature. This is the §5.11 anchoring trap (assertion matched data/defaults, not the intended target — a value-bearing PARAMETER). Corrected to inspect `signature.parameters.keys()`. Recorded so CATO can see the probe was hardened, not the build patched.
- M3 key-bearing classification (§3.4) is an external-API assertion (§5.5). gsearch primary hit a 429 on the first attempt; a retry succeeded and reconfirmed the §3.4 table as current (Maps=client API key; Vertex Gemini + Document AI = ADC/SA, no minted key) as of 2026-06-25. Non-stale; no false positive.
- M6 is a design-property (grep) probe, not a live-mesh exercise — correct for Phase-1 (the design provisions nothing; §7/§4-S5 is the T1 scaffold spec). When the Phase-2 build lands the mesh, M6 graduates to a live deny-by-default / identity-spoof probe.
falsifying_evidence_summary:
verification_artifacts_path: agents/design/stoa--jw5/resolution-check/ (ADA: resolve.py + fixtures.py + run.py; VERA-authored: vera_probes.py — independent re-impl + M1-M4/M6 attack-path probes)
summary: I independently verified the stoa--jw5 Phase-1 resolution harness against design-formal.md without trusting ADA's self-report. I re-ran ADA's run.py (19/19 PASS) AND wrote+ran my own vera_probes.py (30 assertions, exit 0) carrying an INDEPENDENT frozenset-based re-implementation of resolve() that agrees with ADA's on all three §8 fixtures, plus a by-hand derivation of the §8.1 prospector 8-entry set that matches byte-for-byte. The resolution rule reproduces 8/6/7 exactly and §8.4 raises BaselineOmitError naming (db_extension,pgvector) with no partial set (fail-closed). The load-bearing catches are the FIVE threat-anchored attack-path probes: M4 (drove omit of EACH baseline entry + the omit∩add bypass — all fail-closed, while a legit category-omit is correctly permitted), M1 (drove cross-builder scope derivation — neither builder's unique scope-bearing entry reaches the other; t0 derivation per §5.A, R-1 prune honestly Phase-2), M3 (drove the enabled-but-keyless Maps set — the invariant CATCHES it naming the missing pairing, not just passing the happy path), M2 (the model carries only (kind,name) slots — no value materialization point), M6 (all six §7/§4-S5 mesh-security elements specified). The single FAIL in my first run was a false-positive in MY OWN probe (§5.11 anchoring trap on the POSTGRES_PASSWORD substring), fixed in the probe — independence preserved, the build was never patched. Residuals M5 (budget runaway — no GA hard-dollar cap), R-1 (M1 stale-grant-until-reconcile), R-2 (manifest integrity) are honestly classified as §35.5 named residuals in §12.B/§12.B.1 and carried UP to the Grand — confirmed present, not silently dropped; no Phase-1 probe owed.
