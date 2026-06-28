status: completed
ticket: stoa--q7f
verdict: revise
design_artifact_audited: agents/design/stoa--q7f/design-rev1.md
audit_block:
  overall_security_posture: PASS-WITH-CONDITIONS — the core DC1 shape (per-provider scoped pass-through over a closed server-side registry, no caller-supplied URL) is the RIGHT shape and genuinely closes SSRF-by-construction at the architecture level. No blocker, but 4 load-bearing conditions must be folded before this relays up clean.
  risks:
  - id: r1
    description: SSRF is closed-by-construction ONLY if EVERY url_slot is a server-pinned enum/fixed value AND no params value can reach the destination; the design states this as an invariant but provides no enforcement mechanism or probe that FAILS when a future operation adds a free-form slot. The crux (no caller-supplied URL exists) is true for the rev1 vertex op as written, but the property is not mechanically guarded — a future registry op with a free-form url_slot, or a params key interpolated into the URL/host path, silently reopens M1 and nothing catches it.
    evidence: design section1.3 (url_slots are server-pinned enums/fixed values, NOT free caller input), section5/DC6 first bullet (if a future operation accepts a free-form host slot, M1 reopens), section1.5 P-M1 (probes ONE injection attempt on the rev1 op; does not assert the structural invariant no-url_slot-is-caller-derived across the whole registry).
    load_bearing: true
    quadrant_classification: easy-hard
  - id: r2
    description: M2 key-exfil is claimed closed-by-construction at the channel level via an allow-list-shaped redaction pass, but the design own DC6/section6.2 concedes redaction completeness is a residual that depends on the redactor being correct for EVERY provider response shape — which means M2 is NOT closed by construction, it is closed by correct-implementation-of-a-redactor. The two claims contradict. Worse, the design does not resolve DAEDALUS own residual_question 2 — whether some Vertex response shapes (groundingMetadata, streaming/SSE bodies, nested error envelopes) can be allow-listed field-by-field at all, or whether any operation needs opaque pass-through of an upstream body (which would reopen M2 the moment an upstream echoes a token into an un-modelled field). P-M2 tests ONE echo path (an Authorization header in a 401 body); it does not establish that the allow-list covers the full Vertex generateContent/predict response surface.
    evidence: design section1.3 (redaction pass), section1.5 P-M2 (single echo-path probe), DC6 section5 second bullet + section6.2 (a provider that echoes a key in a novel response field the redaction pass does not cover would leak; whether allow-list redaction is implementable for every provider response shape or whether some operations need opaque pass-through reopening the risk, left OPEN). The closed-by-construction claim in section1.1/DC6 is inconsistent with the residual stated in section6.2.
    load_bearing: true
    quadrant_classification: easy-hard
  - id: r3
    description: PREMISE-GAP — the tagged-builder authorization path (App-Capabilities to builders identity class) is relied on as forgery-resistant the-same-way Tailscale-User-Login is, but this EXCEEDS what STRABO verified. STRABO (c)(iv) verified that serve injects+strips the User-* headers AND lists App-Capabilities among injected headers; it did NOT separately verify (a) that for a TAGGED node serve populates a trustworthy App-Capabilities value derived from the ACL grant, (b) that the capability-to-identity-class mapping the core performs is sound, or (c) that App-Capabilities is client-stripped with the SAME guarantee as User-Login. POLYBIUS enrichment (tagged devices do NOT populate user-identity headers, only App-Capabilities) is the SOURCE of this design surface but is itself a one-source web-read flagged needs-vera. The design treats App-Capabilities-is-serve-injected-and-strip-protected-like-user-login as settled; the design own section6.1 admits the EXACT mechanism is the thinnest-grounded design surface, yet still designs ON it without marking it as a premise the build MUST re-verify before the tagged path is trusted.
    evidence: design section0 imported-assumption 1, section1.4 (builder carries Tailscale-App-Capabilities, authorized against the tag/capability), section6.1 (self-flagged); STRABO strabo-dc2-premises.md (c)(iv) lines 167-189 (verifies User-Login strip+reinject explicitly; App-Capabilities listed as injected but its tagged-node population + strip-guarantee NOT separately verified; verification_status needs-vera).
    load_bearing: true
    quadrant_classification: hard-easy
  - id: r4
    description: AUDIT-ORDERING (M5) — write-before-respond is asserted but the threat it must defeat (a call that egresses/acts BEFORE it is recorded, so a crash mid-call leaves no attributable trace) requires the audit write to land before the EGRESS, not merely before the RESPONSE. The design says audit is written BEFORE returning (section1.4) and P-M5 crash-injects after-egress-before-respond, which means the durable record is written AFTER the outbound provider call already happened. A crash or kill in the window between egress and the audit write leaves an executed credentialed external call with NO durable record. For a box holding all keys, the event that most needs attribution (the egress itself) can occur un-audited. The ordering that actually closes M5 is write-INTENT-before-egress (an attempt record) then update-outcome-after; the design specifies a single write-before-respond record, which is write-after-egress.
    evidence: design section1.4 (Every /call produces a durable structured audit record BEFORE returning ... Audit is write-before-respond so a crash cannot drop the record of an attempted call), section1.5 P-M5 (crash-inject after egress-before-respond, the record still exists). The probe own crash-injection point (after egress) demonstrates the gap. The claim a-crash-cannot-drop-the-record-of-an-attempted-call is FALSE for a crash between egress and the single write.
    load_bearing: true
    quadrant_classification: easy-easy
  - id: r5
    description: M3 bind-precondition (the load-bearing crux) is correctly identified and P-M3 is the right probe, but the precondition is stated as a design intention (MUST listen ONLY on a 0600 AF_UNIX socket) with NO build-time INVARIANT that fails the build if a future change binds 0.0.0.0. P-M3 is a design-time probe spec for the FUTURE core service; there is no asserted mechanism that makes a 0.0.0.0 bind un-shippable (e.g. a startup self-check that refuses to serve if the listener is routable, in ADDITION to the P-M3 ss/netstat assertion in CI). As specified, the single most load-bearing security property depends on a future implementer not making one mistake, caught only by a probe that is itself only design-time. NOT-yet-blocker because the build arc is gated and VERA re-runs P-M3, but the design should pin a runtime FAIL-LOUD refuse-to-serve-if-routable self-check, not only an external probe.
    evidence: design section1.4 (The handler MUST listen ONLY on a 0600 AF_UNIX socket ... NEVER 0.0.0.0), section1.5 P-M3 (external ss/netstat probe, design-time), DC6 section5 third bullet (the place the design is most fragile to an implementation slip).
    load_bearing: true
    quadrant_classification: easy-easy
  - id: r6
    description: SHARED-QUOTA fairness (M6) and the per-identity token-bucket are specified, but the design does not address quota accounting for the TAGGED builder identity class as a SINGLE bucket. If all builder-originated calls authenticate under one tag (one App-Capabilities value to one builders identity), the per-identity token-bucket lumps every builder skill/process into a single bucket — one runaway skill exhausts the entire builders share, and the audit log (section1.4 records identity login-or-tag) cannot distinguish WHICH builder skill flooded. Real but bounded fairness/attribution gap, not a security-boundary breach.
    evidence: design section1.4 (M6 per-identity token-bucket; audit identity = login-or-tag). A tag is one identity for the whole builders class; the design does not sub-divide the builders bucket or carry a sub-identity for attribution.
    load_bearing: false
    quadrant_classification: easy-easy
  non_findings:
  - "DC3 emit (section2.5 ProvisioningSpec) — CROSS-CHECKED against live machinery and CONSISTENT: apis=(aiplatform,gemini-embedding,gemini-search) sorted correct; secret_slots GCP_SA_KEY_B64 to mint-via-gcp-console / POSTGRES_PASSWORD to generate-locally / TS_AUTHKEY to mint-via-thirdparty all match _derive_acquisition (spec.py:45-56); sa_scope matches derive_sa_scope scope-bearing union (resolve.py:147-159); railway_vars/db_extensions/needs_postgis all correct. VERA executes; structural shape valid."
  - "No key_bearing_pairing row for Vertex (residual_question 3) — CONFIRMED CORRECT, not a silently-dropped completeness check. check_runtime_completeness (resolve.py:162-177) only flags a missing paired secret for an api_ident that IS in KEY_BEARING_PAIRING; aiplatform is not in the pairing table, so omitting the row asserts NO false invariant. Adding a row would wrongly assert aiplatform is unusable without GCP_SA_KEY_B64 resolved in-set (it is SA/ADC-auth, not API-key-bound). The omission is semantically correct. NOTE: there is then NO mechanical check that GCP_SA_KEY_B64 is present when aiplatform is enabled — acceptable because SA-auth is bootstrapped at startup (DC4), not in-set, but worth one design line stating the SA-key presence is enforced by the startup bootstrap_adc path, not the resolver."
  - "category=none for vertex-gemini/tailscale (residual_question / section6.3) — CORRECT against load_catalog (dataload.py:267-269 explicitly accepts the literal none); both records validate fail-closed. delta.add (not an emergent category) is the honest choice. Not a gap."
  - "detection_hints blocks on both new TOMLs — load_catalog ignores them (reads only service-id/entries/gcp_api/category, dataload.py:245-275); load_detection_hints validates against EXPECTED_HINT_SURFACES (dataload.py:318/364-368). Both blocks use only the 4 allowed surfaces. Structurally valid."
  - "DC3 not-threat-ratified carve-out (section2.7) — CONFIRMED. Two additive catalog records + demo script emit NAMES only against MockProvisioner, touch no real infra/creds/network, frozen resolver byte-identical. A section35.5 process/data change with no runtime attack path. ARGUS confirms the carve-out: NOT threat-ratified. M1..M6 live entirely in the future DC1 core-service build."
  - "Egress is public-internet not tailnet (imported assumption 2 / STRABO nuance 1) — does not exceed STRABO; STRABO (b)(iii) verified userspace serve is inbound-only, core egress to Vertex is public-internet. Correct."
  - "Funnel OFF / no public ingress (section1.4) — matches STRABO (c)(i). M1 external-reachability variant correctly closed."
  threat_coverage_assessment: "PROBE-SPEC ADEQUACY (design-time, section6.9 tier-i): the DC1 threat-to-mitigation map (section1.5) DOES specify a threat-anchored probe (P-M1..P-M6) per named mitigation M1..M6, each asserting BOTH attack-blocked AND legit-unaffected (the (a)/(b) structure). Mechanical presence-check PASSES — no mapless-mitigation smell, no map-present/probe-absent smell, so the section6.9 design-smell does NOT fire. However three probes are specified at a STRENGTH that does not fully exercise the named attack path (tier-ii, surfaced as load-bearing risks for VERA/CATO to confirm at build): P-M1 tests one injection instance not the structural no-caller-url invariant (r1); P-M2 tests one echo path not full-response-surface redaction coverage (r2); P-M5 crash-injection point (after egress) demonstrates the write-after-egress ordering gap (r4). The finding is probe-STRENGTH, routed as r1/r2/r4. THREAT-ENUMERATION completeness (is M1..M6 the full threat set for an all-keys egress box) remains my unmechanized judgment, see hard-hard note in summary."
summary: |
  The core architectural decision — a per-provider scoped pass-through over a CLOSED server-side
  PROVIDER_REGISTRY of named operations, with NO caller-supplied URL/host anywhere — is the correct shape
  and genuinely stronger than an allowlisted egress proxy. At the architecture level SSRF IS closed by
  construction for the rev1 vertex operation as written: there is no destination input to attack. The DC3
  mock-emit cross-checks consistent with the live machinery and the no-pairing-row decision is confirmed
  semantically correct. A sound design from a competent architect, honest about most of its own soft spots.
  I return REVISE, not FAIL: no blocker says the shape is wrong, but four load-bearing conditions must be
  folded before this relays up as a clean security verdict, because the design over-claims closed-by-
  construction in two places where the property actually rests on correct-implementation-of-future-code, and
  one place where it rests on a premise one notch past what STRABO verified.
  The single most important load-bearing risk is r2 (key-exfil redaction completeness): the design
  simultaneously claims M2 is closed-by-construction AND concedes (its own section6.2) that redaction
  completeness is an OPEN residual depending on the redactor covering every Vertex response shape — these
  cannot both be true. For a box holding ALL provider keys, a redactor that must be proven complete against an
  evolving upstream response surface is the opposite of closed-by-construction; it is closed-by-correct-
  implementation, and DAEDALUS residual_question 2 (do some responses need opaque pass-through, reopening M2)
  is left unresolved — that must be answered in the design, not deferred to the build. r3 (tagged-builder
  premise-gap) is next: the builders identity class rests on App-Capabilities being serve-injected + tagged-
  node-populated + strip-protected the SAME way Tailscale-User-Login is — STRABO verified the User-Login
  mechanism explicitly but did NOT separately verify the tagged-node App-Capabilities population/strip
  guarantee, and the design designs on it as settled. r1 (SSRF residual: no invariant-probe guarding url_slots
  from caller-influence across the registry) and r4 (audit write-after-egress, not write-before-egress) round
  out the four. r5 (no in-process refuse-to-serve-if-routable invariant backing the M3 bind crux) and r6
  (single-bucket builder quota/attribution) are real but lower; r5 is a NOT-yet-blocker only because the build
  is separately gated and VERA re-runs P-M3.
  HONEST-CLAIM BOUNDARY (hard-hard, section6.6, not a numbered risk): I verified COVERAGE of the named threats
  M1..M6, not threat-ENUMERATION completeness. For an internet-egress box holding every provider key I
  considered but did not exhaust: response-side SSRF-via-redirect-following inside the registry op (the upstream
  302s to a metadata endpoint, does the core HTTP client follow redirects), key confusion across providers
  (could a vertex op be induced to attach a different provider key), and timing/error-class side-channel exfil
  of key bytes. These are UNVERIFIABLE from the design alone and I do NOT represent M1..M6 as a proven-complete
  threat set — the enumeration is DAEDALUS and the gate judgment, surfaced so it is not mistaken for exhausted.
  Net: sound shape, REVISE on four load-bearing conditions; the crux (per-provider closed registry) holds and
  does not need redesign.
gap_or_blocker: none — design artifact read in full; all four cited cookie-cutter ground-truth files resolved and cross-checked.
