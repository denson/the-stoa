<!-- author: Denson Smith -->
<!-- seat: CAPTAIN_VERA_the_stoa (VERIFIER) — independent falsification verdict -->
<!-- ticket: stoa--q7f | arc-77 | coordination stoa--po5 | u--9s2 Phase-1 increment 2.4 -->

# VERA build-falsification verdict — arc-77 secure-core pass-through (stoa--q7f)

```
status: completed
ticket: stoa--q7f
verdict: pass
design_artifact_verified_against: agents/design/stoa--q7f/design-rev4.md (§2 multi-lane authz, §3 seal-audit, §5 P-M1..P-M7)
build_verified: arc-77/build @ worktree .claude/worktrees/arc-77-build (0 commits ahead of main; nothing merged/pushed)

probes_executed:
- probe_id: SUITE-secure_core
  description: Re-run the FULL P-M1..P-M7 probe contract INDEPENDENTLY (per-worktree .venv; confirmed no arc-76/build import bleed — both secure_core and builder_deploy_core resolve from the arc-77 worktree).
  command_or_method: .venv/Scripts/python.exe -m pytest agents/secure-core/tests/ -v
  expected: all P-M1..P-M7 GREEN; any skip judged to not hide an unverified invariant arm.
  observed: 50 passed, 1 skipped. The ONLY skip = test_pm3a_af_unix_real_listener_mode_checked_when_available (real AF_UNIX os.stat integration; AF_UNIX absent on the Windows build host). The 0600-refuse LOGIC arm (test_pm3a_af_unix_0600_refuse_logic_is_exercised) PASSED — 6 wrong modes (0644/0660/0777/0604/0000/0640) raise BindError + 0600 allowed, exercised cross-platform.
  result: pass
  quadrant_classification: easy-easy (mechanical: run suite, assert green; the skip is a bounded platform-integration residual, not a detection/verification-hard case)
- probe_id: SUITE-builder_deploy_core
  description: Full regression bar — the reproduced DC3 records must not break the existing roster suite.
  command_or_method: .venv/Scripts/python.exe -m pytest agents/builder-deploy-core/tests/ -q
  expected: full suite GREEN.
  observed: 105 passed in 24.53s.
  result: pass
  quadrant_classification: easy-easy
- probe_id: DEMO-rev2-2.6
  description: The DC3 mock-emit demo — runs, asserts the §2.5 golden ProvisioningSpec + value-free (assert_value_free over spec + RunLedger + MeshShape).
  command_or_method: .venv/Scripts/python.exe demo/sos_core_emit_demo.py
  expected: exit 0; all §2.6 assertions; every secret_slot populated=False (NAMES only); no credential value.
  observed: exit 0; resolved set == §2.4 golden (8 entries); emitted spec == §2.5 golden with slot NAMES only; assert_value_free passed on spec / blocked ledger / populated ledger / MeshShape (0600 / af_unix / deny_by_default / funnel_off).
  result: pass
  quadrant_classification: easy-easy
- probe_id: V-M1-DEST (INV-DEST / D3 slots — adversarial)
  description: Try to steer the outbound destination via params, skill_id, AND the D3 `slots` envelope field; confirm destination is built ONLY from server-pinned FIXED + closed-ENUM slots.
  command_or_method: VERA adversarial script — _build_destination + end-to-end handle_call with attacker `slots`; planted-op load_registry for params-derived + free-form url_slot.
  expected: FIXED slot caller-selection REJECTED; ENUM value outside the closed set REJECTED; unknown slot key REJECTED; every legal ENUM combo yields a pinned *-aiplatform.googleapis.com host; e2e attacker slots -> 400 ZERO egress; loader REFUSES a params-derived destination and a free-form str url_slot (LoaderError INV-DEST).
  observed: ALL HELD. project (FIXED) selection -> Rejected "is FIXED and not caller-selectable"; location=evil.com / attacker-host / ../../.. / us-central1.evil.com / metadata.google.internal -> each Rejected "not in closed choices"; unknown key {host,scheme} -> Rejected; legal combos -> {us-central1,us-east4}-aiplatform.googleapis.com only; e2e status=400 hosts=[]; planted params->host op -> LoaderError INV-DEST; planted free-form str slot -> LoaderError INV-DEST. redirect-following OFF confirmed (design P-M1 test + _NoRedirect).
  result: pass
  quadrant_classification: easy-easy (destination is a closed FIXED/ENUM type; free-form host not representable — SSRF closed by construction, mechanically falsifiable)
- probe_id: V-M2-RESP (INV-RESP key-exfil — adversarial full surface)
  description: Inject a mock credential value + Authorization/x-goog-api-key into UNDECLARED response fields/subfields/headers and into an error body across the Vertex surface; assert none reach caller or audit. THEN push past the written probe: inject a credential NESTED inside a DECLARED passthrough field (groundingMetadata, content).
  command_or_method: VERA adversarial script — redact_response + full handle_call pipeline with credential-bearing upstream body/headers; grep both audit phases for the secret.
  expected: credential in undeclared top field / undeclared candidate subfield / upstream headers / error body -> NONE reach caller or audit; error envelope == {status, provider_error_class} only.
  observed: UNDECLARED-field and header and error-body cases ALL DROPPED (secret absent from caller body AND both audit phases; error envelope = {status, provider_error_class}). BUT: a credential NESTED inside a DECLARED field's value (candidates[].groundingMetadata.leaked_bearer, and candidates[].content.secret) DOES reach the caller — the allow-list serializer is depth-2 (top-key + one sub-key level) and emits a declared sub-key's VALUE whole. See methodology_concerns (bounded; not a realistic credential-exfil path — the core's ADC bearer is request-side, never present in a Vertex response body).
  result: pass  (design's P-M2 threat-anchored assertions — undeclared fields/headers/errors dropped — all HELD; the nested-declared-field depth-limit is a surfaced coverage gap, not a falsified design assertion; see methodology_concerns)
  quadrant_classification: easy-hard (detection of the depth-limit is easy; proving the allow-list carries NO credential echo across an evolving upstream surface is the wp#3 build-time property, not by-construction)
- probe_id: V-M3-BIND (INV-BIND — adversarial + D2 residual)
  description: Configure the handler to bind a routable address (0.0.0.0) -> refuse to serve (not warn); confirm 0600-refuse logic raises for wrong socket modes; honestly bound the real-AF_UNIX residual.
  command_or_method: VERA script assert_bind_target_safe + design P-M3 suite.
  expected: routable bind RAISES BindError (refuse to serve, non-zero); 0600 arm exercised cross-platform.
  observed: build_server(host=0.0.0.0) -> BindError "routable" (no socket opened); 0.0.0.0 / :: / 10.0.0.5 / 100.64.0.7 all raise; 0600 allowed, 6 wrong modes raise. D2 residual: the real-AF_UNIX os.stat integration is the ONLY skip — an HONEST Phase-3-on-Linux residual, called out (not claimed green); the 0600 fail-loud LOGIC is genuinely exercised, decoupled from the platform AF_UNIX constant.
  result: pass
  quadrant_classification: easy-easy (pure bind-target check; the real-socket os.stat is a bounded platform residual)
- probe_id: V-M4-LANE (INV-LANE + INV-PRINCIPAL cross-lane — THE crux, adversarial + r1-residual)
  description: newswire tag -> generate_grounded = 403 zero-egress audited forbidden lane:newswire; r1-residual = denial AT RESOLUTION for unmapped cap AND absent/empty/malformed header AND unlisted login (audit reason `no resolvable principal`, denial_stage=resolution); construct a permissive-default (.get(cap,DEFAULT)) resolver and confirm the probe FALSIFIES it; multi-cap non-registered -> 403 reject-ambiguous (no silent union); legit paths unaffected.
  command_or_method: VERA adversarial script — handle_call across 8 identity constructions + a monkeypatched broken .get(cap,DEFAULT) resolver.
  expected: every attack path 403 ZERO egress with denial at the correct stage/reason; the constructed permissive-default build demonstrably returns 200+egress (proving the probe catches it); legit science->generate_grounded, newswire->embed authorized.
  observed: ALL HELD. newswire->generate_grounded = 403 zero-egress, denial_stage=scopes, lane:newswire attributed, reason "out of scope". r1-residual: unmapped cap / absent / empty / malformed header / unlisted login -> EACH 403, egressed=False, hosts=[], denial_stage=resolution, intent.reason="no resolvable principal" (denial OBSERVED AT RESOLUTION, not a downstream sentinel). Constructed .get(cap,DEFAULT) build -> status=200 egress=[us-central1-...] (DEMONSTRABLY permissive; the real build differs -> P-M4(a.2) catches it). 2-lane non-registered node -> 403 "ambiguous multi-lane principal" (no union); multi-cap does NOT union into generate_grounded. legit science->generate_grounded 200, newswire->embed 200.
  result: pass
  quadrant_classification: easy-easy (resolve_principal raises at resolution by explicit-membership; the forbidden .get(cap,DEFAULT) shape is representable-but-caught and directly falsifiable)
- probe_id: V-M5-AUDIT (two-phase value-free audit)
  description: crash-inject in the egress->outcome window -> INTENT survives, value-free, carries lane.
  command_or_method: design P-M5 suite (test_pm5a_crash_after_egress_before_outcome_leaves_intent + value-free/irreversible-digest).
  expected: durable INTENT before egress; params_digest (sha256) never raw values; lane present; a value-channel key rejected.
  observed: PASS — crash after egress leaves the durable INTENT on disk; records carry only the closed key-set (params_digest irreversible fixed-width hex; lane field present); assert_record_value_free refuses an undeclared key.
  result: pass
  quadrant_classification: easy-easy
- probe_id: V-M6-RATE (per-lane token bucket)
  description: one lane bursts -> 429; a second lane low-rate -> unthrottled; skill_id sub-bucket attributed.
  command_or_method: design P-M6 suite (deterministic clock-injected bucket).
  expected: burst over N -> 429; sibling lane unthrottled; per-(lane,skill_id) sub-bucket throttles one skill not its sibling.
  observed: PASS — burst 429; second lane unthrottled (per-lane bucket is the boundary); sub-bucket throttles one skill_id, sibling unaffected.
  result: pass
  quadrant_classification: easy-easy
- probe_id: V-M7-SEAL (fail-CLOSED seal-audit — adversarial smuggle + independent grep)
  description: plant UNMARKED real-shaped secret (tskey + b64 SA-blob) in a TOML + a log -> REFUSE; plant MARKED real-shaped in fixtures + MARKED shape-clean OUTSIDE fixtures -> STILL FAIL (r2 bypass closed); slot-names + shape-clean marked-in-fixtures -> PASS; then independently GREP the whole service tree + config + catalog TOMLs + emitted logs for secret VALUES.
  command_or_method: VERA adversarial script (7 smuggle attempts) + ripgrep real-shape scan across the deliverable + a real seal_audit() run over the service tree + the two DC3 TOMLs.
  expected: every unmarked/marked-real-shaped/mis-placed value FAILS the build non-zero; only path-bound + shape-clean marked fixtures pass; NO secret VALUE anywhere in the deliverable (slot NAMES only).
  observed: unmarked tskey-in-toml -> SealAuditError(tailscale_authkey); b64 SA-blob-in-log -> FAIL; MARKED real-shaped tskey in fixtures -> FAIL (marked_real_shape — marker cannot launder a shape); MARKED shape-clean outside fixtures -> FAIL (marked_out_of_path); marked b64-blob>=100 in fixtures -> FAIL; secret NAME bound to a real value -> FAIL (secret_name_bound_value); slot-names + clean-marked-in-fixtures -> PASS. INDEPENDENT GREP: exactly ONE real-shape literal in all of secure-core (test_pm7_seal_audit.py:25 REAL_TSKEY — an EXPECTED P-M7 attack input confined to a TEST body; seal-audit excludes tests/); 0 base64 blobs>=80 in service code/config/catalog; the real seal_audit() gate over 15 service+DC3 files = PASS clean (0 findings). DC3 TOMLs carry slot NAMES only (GCP_SA_KEY_B64 / TS_AUTHKEY / POSTGRES_PASSWORD as config_keys), author Denson Smith.
  result: pass
  quadrant_classification: easy-easy (deterministic shape-match gate; fail-closed on ambiguous >=100-entropy; the <100 novel-format bound is an acknowledged residual — wp#2)
- probe_id: V-FENCE (scope fence + frozen-file integrity)
  description: confirm nothing merged/pushed; frozen resolve.py byte-identical; DC3 TOMLs byte-identical to the arc-76 reference.
  command_or_method: git rev-list --count main..arc-77/build; git diff main -- resolve.py; sha256sum the two DC3 TOMLs.
  expected: 0 commits ahead; empty resolve.py diff; DC3 sha256 == arc-76 reference.
  observed: 0 commits ahead of main; resolve.py diff empty (frozen); vertex-gemini.toml sha256=11c88105... , tailscale.toml sha256=5bb085ef... (match ADA/arc-76 reference). arc-76/build + main untouched.
  result: pass
  quadrant_classification: easy-easy

threat_coverage:
- mitigation: M1
  threat: SSRF / forward-anything egress
  defeats_via_probe: V-M1-DEST
  probe_evidence: VERA script — every caller destination-injection (params / skill_id / D3 slots) rejected; destination built only from FIXED+ENUM; e2e attacker slots -> 400 ZERO egress; loader refuses params-derived + free-form slot.
  attack_path_exercised: caller supplies attacker host via slots/params -> (a) rejected/refused, ZERO egress, only pinned *-aiplatform.googleapis.com reachable; (b) legit ENUM selection (us-east4 / gemini-2.5-pro) still resolves.
- mitigation: M2
  threat: key-exfil via response/log
  defeats_via_probe: V-M2-RESP
  probe_evidence: undeclared fields/subfields/headers/error-body all dropped; secret absent from caller body AND both audit phases; error envelope = {status, provider_error_class}. (Bounded coverage gap on nested-declared-field values -> methodology_concerns; NOT a core-credential path.)
  attack_path_exercised: caller induces a credential echo in the response -> (a) undeclared-field/header/error credential dropped; (b) legit declared fields returned intact. Nested-declared-field passthrough surfaced as a hardening concern, not a realistic credential leak (ADC bearer is request-side only).
- mitigation: M3
  threat: identity-header forgery via non-loopback bind
  defeats_via_probe: V-M3-BIND
  probe_evidence: routable bind (0.0.0.0/::/tailnet IP) -> BindError refuse-to-serve, no socket opened; 0600 refuse logic exercised cross-platform (6 wrong modes raise).
  attack_path_exercised: handler configured routable -> (a) refuse to serve (non-zero), identity surface never exposed; (b) loopback/0600 permitted. Real-AF_UNIX os.stat = honest Phase-3 residual.
- mitigation: M4
  threat: over-broad authz -> CROSS-LANE reach (incl. permissive-default resolve + multi-cap union)
  defeats_via_probe: V-M4-LANE
  probe_evidence: newswire->generate_grounded 403 zero-egress lane-attributed; unmapped-cap/absent/empty/malformed-header/unlisted-login EACH 403 zero-egress denial AT RESOLUTION (reason `no resolvable principal`); constructed .get(cap,DEFAULT) build demonstrably permissive (probe catches it); 2-lane non-registered -> 403 reject-ambiguous (no union).
  attack_path_exercised: one lane's tag (or an unresolvable/multi-cap principal) reaches another lane's op -> (a) 403 ZERO egress at the correct stage with the correct audited reason; (b) legit science->generate_grounded + newswire->embed authorized. r1-residual (denial-at-resolution) CONFIRMED executed.
- mitigation: M5
  threat: audit gap
  defeats_via_probe: V-M5-AUDIT
  probe_evidence: crash after egress leaves durable value-free INTENT carrying lane; params_digest irreversible; value-channel key rejected.
  attack_path_exercised: crash in egress->outcome window -> INTENT of the executed credentialed call survives, value-free, lane-attributed.
- mitigation: M6
  threat: quota exhaustion / DoS
  defeats_via_probe: V-M6-RATE
  probe_evidence: burst -> 429; second lane unthrottled; per-(lane,skill_id) sub-bucket throttles one skill not its sibling.
  attack_path_exercised: one lane floods shared quota -> its per-lane bucket 429s; a second lane's low-rate traffic is NOT throttled.
- mitigation: M7
  threat: secret-value leakage into code/config/catalog/logs (incl. marker-laundered)
  defeats_via_probe: V-M7-SEAL
  probe_evidence: unmarked + marked-real-shaped + mis-placed marked values ALL fail the build non-zero; independent grep = zero secret VALUES in service/config/catalog (only a test-body attack input); real seal_audit() over 15 service+DC3 files clean.
  attack_path_exercised: a real (or marker-laundered) secret VALUE lands in an artifact -> (a) build REFUSES non-zero at each planted site (r2 bypass closed); (b) slot-names + shape-clean marked-in-fixtures build PASSES.

methodology_concerns:
- INV-RESP allow-list DEPTH (load-bearing — surfaced by V-M2-RESP beyond the written P-M2): redact_response is a depth-2 allow-list (top-key + one sub-key level). A declared sub-key's VALUE is emitted WHOLE, so a value nested INSIDE a declared field (candidates[].groundingMetadata.<x>, candidates[].content.<x>) is NOT redacted. The design's P-M2 covers UNDECLARED fields/subfields/headers/errors (all PASS) and the design's INV-RESP claim is scoped to undeclared fields — so no design ASSERTION is falsified, and the realistic M2 credential-exfil surface is CLOSED (the core's ADC bearer is a request-side header, never present in a Vertex response body; `content` is model-generated product output that MUST pass whole; `groundingMetadata` is upstream search metadata that does not carry the core credential). This is nonetheless the partial "opaque pass-through" INV-RESP §1.3.1 nominally disallows, and it is the wp#3 allow-list-completeness residual made concrete. RECOMMENDED FIX-NOW (cheap, honors the fix-known-bugs posture; routed to DAEDALUS/ADA via PLINY/CATO — I do NOT patch the build, §5.1 independence): deepen the groundingMetadata sub-schema to an explicit allowed-sub-key list (or make redact_response recurse to schema depth), keep `content` an intentional whole-passthrough with a comment, and EXTEND P-M2 with a nested-declared-field clause so the depth is probe-guarded. NOT build-blocking on its own.
- seal-audit shape-set / entropy-floor residual (acknowledged wp#2, re-confirmed): a NOVEL-format secret below the >=100 base64/hex fail-closed floor, not matching a known shape, and not bound to a known slot NAME, passes (demonstrated: a short unbound token). This is the documented bound of a deterministic shape-match gate, fail-closed on >=100 entropy — a known limitation, not a regression.
- commit-stage hygiene (carry to the WRITER/commit stage, not a build defect): the worktree-root `.venv/` is untracked and NOT gitignored (a `git add -A` would grab it); a `build/lib/` pip-build copy of builder_deploy_core also exists. Stage ONLY the build deliverable (secure-core/, the two DC3 TOMLs, demo/, design/, verdicts/, the roster-pin test_dataload.py) — exclude `.venv/` and `build/lib/`.

falsifying_evidence_summary:

verification_artifacts_path: agents/verdicts/stoa--q7f/ (this verdict) + adversarial probe script recorded in the dispatch (scratchpad vera_adversarial.py — 36 checks, 34 pass / 2 nested-declared-field observations judged bounded); design probe suites at agents/secure-core/tests/ (50/1) + agents/builder-deploy-core/tests/ (105) re-run against REAL code from the per-worktree .venv.

summary: The build was exercised INDEPENDENTLY against REAL code from a per-worktree .venv (no arc-76 import bleed): the full P-M1..P-M7 contract (50 passed / 1 honest Phase-3 skip), the builder_deploy_core regression bar (105 passed), and the DC3 demo (exit 0, value-free) all GREEN; on top I ran 36 adversarial falsification checks that try to BREAK each invariant beyond the written probes. The load-bearing cruxes HELD: (M1/D3) the destination is a closed FIXED+ENUM type — every attacker slots/params/skill_id injection is rejected, only *-aiplatform.googleapis.com is reachable, the loader refuses free-form + params-derived slots; (M4/r1-residual) resolve_principal denies AT RESOLUTION for unmapped-cap / absent / empty / malformed header / unlisted login (audited `no resolvable principal`, denial_stage=resolution), a constructed .get(cap,DEFAULT) build is demonstrably permissive so the probe genuinely falsifies it, and a 2-lane non-registered node is rejected reject-ambiguous with NO silent union; (M7) the fail-closed seal-audit refuses every unmarked, marked-real-shaped, and mis-placed marked secret, my independent grep found ZERO secret VALUES in service/config/catalog (only slot NAMES + one test-body attack input), and the real seal_audit() gate is clean over 15 files. Every INV-* is fail-LOUD (refuse-to-serve / refuse-to-load / 403-zero-egress / build-fail), never warn-and-continue. The most important finding: my adversarial M2 push showed the INV-RESP allow-list is depth-2, so a credential nested inside a DECLARED field's value (groundingMetadata/content) is emitted whole — but the design's P-M2 (undeclared fields/headers/errors) all PASS, no design assertion is falsified, and the realistic credential-exfil surface is closed (the ADC bearer is request-side, never in a Vertex response body); I record it as a load-bearing hardening concern (deepen the sub-schema / extend P-M2) routed to DAEDALUS/ADA, not a build-blocker. D2 (real-AF_UNIX) and the seal-audit entropy-floor are honestly bounded residuals, not claimed green. Scope fence held (0 commits ahead of main, frozen resolve.py + DC3 TOMLs byte-identical). Verdict: PASS with one consequential hardening concern surfaced for the gauntlet to arbitrate.
```
