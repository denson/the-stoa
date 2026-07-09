<!-- author: Denson Smith -->
<!-- seat: CAPTAIN_VERA_the_stoa (VERIFIER) — independent rev6 INV-RESP re-verification -->
<!-- ticket: stoa--q7f | arc-77 | coordination stoa--po5 | u--9s2 Phase-1 increment 2.4 -->

# VERA rev6 INV-RESP re-verify verdict — arc-77 secure-core (stoa--q7f)

Re-verification of ADA's rev6 INV-RESP amendment (recursive NODE grammar OBJECT/SCALAR-recursive-dict-scan/PASS_WHOLE + PASS_WHOLE_ALLOWLIST loader placement guard + copy-safe marker singletons) against the service I falsification-passed at rev4/depth-2. This dispatch adversarially confirms the amendment HOLDS and did not regress — it does NOT merely re-run ADA's tests.

```
status: completed
ticket: stoa--q7f
verdict: pass
design_artifact_verified_against: agents/design/stoa--q7f/design-rev6.md (§5.1a recursive NODE grammar + PASS_WHOLE_ALLOWLIST; §5.2 A3 map; §5.3 DoD; §3.1 seal-audit)
build_verified: arc-77/build @ worktree .claude/worktrees/arc-77-build (0 commits ahead of main; build work working-tree only, nothing committed/pushed)

probes_executed:
- probe_id: SUITE-secure_core
  description: Re-run the FULL P-M1..P-M7 contract INDEPENDENTLY from the per-worktree .venv (confirmed no arc-76 bleed — secure_core AND builder_deploy_core both resolve from the arc-77 worktree __file__).
  command_or_method: .venv/Scripts/python.exe -m pytest agents/secure-core/tests/ -v
  expected: all P-M1..P-M7 GREEN; P-M2 carries the rev6 a.2/a.3/a.4 clauses; any skip judged non-load-bearing.
  observed: 60 passed, 1 skipped (was 50/1 at rev4 — +10 from the rev5/rev6 P-M2 clauses). P-M2 = 15 green incl a.2 (nested depth-3), a.3 (SCALAR-slot direct+list-nested+doubly-nested+shallow-SCALAR-falsifier+legit), a.4 (PASS_WHOLE-misplace refuse + legacy-bare-list refuse + allowlisted-content whole). The ONLY skip = test_pm3a_af_unix_real_listener_mode_checked_when_available (real AF_UNIX os.stat; AF_UNIX absent on the Windows build host) — the 0600-refuse LOGIC arm PASSED (6 wrong modes raise). Unchanged honest Phase-3 residual.
  result: pass
  quadrant_classification: easy-easy (mechanical run-suite/assert-green; the skip is a bounded platform residual)
- probe_id: SUITE-builder_deploy_core
  description: Full regression bar — the recursive-serializer amendment must not break the roster/DC3 suite.
  command_or_method: .venv/Scripts/python.exe -m pytest agents/builder-deploy-core/tests/ -q
  expected: full suite GREEN (105).
  observed: 105 passed in 20.57s.
  result: pass
  quadrant_classification: easy-easy
- probe_id: DEMO-DC3
  description: The DC3 mock-emit demo — value-free ProvisioningSpec + RunLedger + MeshShape.
  command_or_method: .venv/Scripts/python.exe demo/sos_core_emit_demo.py (from builder-deploy-core)
  expected: exit 0; all §2.6 assertions; every secret_slot populated=False (NAMES only).
  observed: exit 0; resolved set == §2.4 golden (8 entries); emitted spec == §2.5 golden slot-NAMES-only; assert_value_free passed on spec / blocked ledger / populated ledger / MeshShape (0600 / af_unix / deny_by_default / funnel_off).
  result: pass
  quadrant_classification: easy-easy
- probe_id: V-M2a2-DEPTH (adversarial — my own DEEPER nesting than ADA planted)
  description: INV-RESP a.2 — plant a credential in UNDECLARED sub-keys at depth 3/4/5 inside the DECLARED recursed OBJECT tree (groundingMetadata.sneaky_depth3; groundingChunks[].web.leaked_depth5; groundingChunks[].undeclared_chunk_key depth-4; groundingSupports[].segment.leaked_seg depth-5; usageMetadata.leaked_usage). Confirm ALL dropped, declared siblings intact.
  command_or_method: VERA adversarial script redact_response(gen_schema, deep-poisoned body) — direct against REAL redact.py.
  expected: SECRET absent from output at ALL depths; every undeclared key at every depth dropped; every declared sibling (web.uri/title, segment.startIndex) intact.
  observed: SECRET absent from caller output at all depths; sneaky_depth3/leaked_depth5/undeclared_chunk_key/leaked_seg/leaked_usage ALL dropped; declared web.uri="u"/title="t" + segment.startIndex=0 intact. The recursive OBJECT node drops undeclared keys by construction at every level (not a depth-2 whole-pass).
  result: pass
  quadrant_classification: easy-easy (by-construction "keep only declared keys" per level; mechanically falsifiable — a depth-2 build emits)
- probe_id: V-M2a3-SCALAR (adversarial — mappings nested DEEPER than the probe plants)
  description: INV-RESP a.3 — smuggle a credential-bearing mapping under a SCALAR-declared field six ways: direct dict, list-nested, doubly-nested, TRIPLY-nested, dict-in-tuple-in-list, deep-mixed [a,[b,[c,{x:{leaked}}]]]. Confirm the recursive dict-scan drops the WHOLE value in every case. AND confirm no over-drop of legit scalars/arbitrarily-deep arrays-of-scalars.
  command_or_method: VERA adversarial script redact_response({f: SCALAR}, {f: <smuggle>}) across 6 smuggle shapes + 6 legit shapes.
  expected: every mapping-bearing value (any depth) DROPPED whole, SECRET absent; every legit scalar/nested-array-of-scalars passes intact (==input).
  observed: all 6 smuggle shapes dropped whole (SCALAR handler is a genuine recursive dict-scan, not shallow); all 6 legit shapes (str/int/bool-null/list-of-str/nested-list-of-scalars/deep-nested-scalars) pass intact. A shallow-SCALAR impl would emit the list-nested case (ADA's test_pm2a3_shallow_scalar_build_FAILS confirms the falsifier); the real impl drops it.
  result: pass
  quadrant_classification: easy-easy (recursive dict-scan; the discriminating list-nested case is directly falsifiable against a shallow build)
- probe_id: V-M2a4-PLACEMENT (adversarial — placement at SPECIFIC fields, message anchored)
  description: INV-RESP a.4 — mark a NON-allowlisted field PASS_WHOLE at three SPECIFIC locations (candidates.finishReason; usageMetadata.totalTokenCount; predictions.embeddings.values) → loader REFUSES TO LOAD, and the LoaderError names THAT field (not candidates.content).
  command_or_method: VERA adversarial script — fresh default_provider_registry() (module-singleton markers, no deepcopy) mutated per field, load_registry, regex-anchor on the quoted `field '<path>'` token (§5.11 — a bare substring match false-positives on the allowlist enumeration `['candidates.content']` printed in every refusal message).
  expected: LoaderError raised each time; the quoted violating field == the planted field; not candidates.content.
  observed: all 3 refuse to load; violating field named == candidates.finishReason / usageMetadata.totalTokenCount / predictions.embeddings.values respectively (fail-CLOSED at load, deny-by-default). NOTE: my FIRST pass logged 4 false FAILs from a naive `"candidates.content" in msg` check (§5.11 anchoring pitfall — the refusal message always prints the allowlist); refined+anchored on the quoted field token → 5/5 PASS. That is a defect in MY probe, not the build.
  result: pass
  quadrant_classification: easy-easy (loader placement guard is a closed deny-by-default check; refinement was an anchored-probe correction, not a quadrant shift)
- probe_id: V-META-DEEPCOPY (the load-bearing meta-check — a.4-passing-for-the-right-reason)
  description: Independently confirm ADA's copy.deepcopy singleton fix (__copy__/__deepcopy__/__reduce__ return self). (1) markers survive copy/deepcopy/pickle as the SAME instance; (2) deepcopy a registry, plant a non-allowlisted PASS_WHOLE at candidates.finishReason, assert the LoaderError names finishReason (the ACTUAL violation) NOT candidates.content; (3) TEETH — a SHATTERED-identity marker (fresh _NodeMarker, simulating a broken __deepcopy__) at content makes the loader misfire AT content, demonstrating exactly the bug the fix closes.
  command_or_method: VERA adversarial script — copy.deepcopy/copy.copy/pickle identity asserts; deepcopy+plant+load_registry with regex-anchored field extraction; shattered-marker construction _NodeMarker("PASS_WHOLE") is not PASS_WHOLE.
  expected: (1) deepcopy(SCALAR) is SCALAR, deepcopy(PASS_WHOLE) is PASS_WHOLE, copy + pickle round-trips singleton; (2) refusal names candidates.finishReason, NOT candidates.content; (3) a shattered content marker misfires at candidates.content (the bug).
  observed: (1) all identity asserts PASS (deepcopy/copy/pickle preserve the singleton for both markers); (2) deepcopy+plant → violating field == candidates.finishReason, NOT candidates.content — a.4 now fails-closed for the RIGHT reason; (3) TEETH confirmed — a fresh _NodeMarker at content misfires with the loader naming candidates.content (finishReason never reached), which is precisely the a.4-passing-for-the-wrong-reason failure the fix eliminates. Fix CONFIRMED right-reason.
  result: pass
  quadrant_classification: easy-easy (identity-compare + anchored message extraction; the teeth-check makes the meta-property directly falsifiable)
- probe_id: V-M2b-NOOVERDROP (legit paths intact incl. content whole-pass)
  description: INV-RESP b — the tightenings must not break legit output: legit nested scalar / list-of-scalars pass; the allowlisted candidates.content whole-passes an ARBITRARY nested model product (parts w/ functionCall.args.deep.nested, inlineData) WITHOUT truncation.
  command_or_method: VERA adversarial script — redact_response(gen_schema, body-with-weird-content); legit scalar/array cases (shared with V-M2a3).
  expected: content == input (whole, untruncated); legit scalars/arrays intact.
  observed: content passed WHOLE — the 3-part model product (text + functionCall w/ deeply-nested args + inlineData BLOB) is byte-identical in the output (PASS_WHOLE did not recurse-truncate it); legit scalar/array-of-scalars intact. The recursion did not over-drop and the allowlisted whole-pass did not break the model deliverable.
  result: pass
  quadrant_classification: easy-easy
- probe_id: V-EMBED-PIN (embeddings=OBJECT deviation — independent web-verify + leak/over-drop)
  description: FM-registered check. ADA built embed's embeddings as a recursed OBJECT {values:SCALAR, statistics:{token_count,truncated}} (not the design's illustrative SCALAR), web-verified vs real Vertex. Independently web-verify the declared sub-keys match the CURRENT real Vertex :predict shape; confirm a legit embeddings passes intact WHILE an undeclared embeddings sub-key (planted credential) DROPS; AND an object smuggled under the SCALAR `values` slot drops whole.
  command_or_method: gsearch (per CLAUDE.md web-verify discipline) on the current text-embedding-005 :predict response shape; VERA adversarial script redact_response(embed_schema, legit + poisoned bodies).
  expected: real Vertex embeddings == {values:[float], statistics:{token_count:int, truncated:bool}}; legit embeddings intact; planted undeclared sub-keys (leaked_emb, statistics.leaked_stat, prediction-level leaked_pred) dropped; object under SCALAR values dropped whole.
  observed: WEB-VERIFY = EXACT match — current text-embedding-005 :predict returns predictions[].embeddings.{statistics:{truncated:bool, token_count:int}, values:[float...]}; ADA's pin is correct (and the design's illustrative SCALAR would over-drop the real embeddings OBJECT and break embed — the drift-to-OBJECT is a correctness fix, V-RESP-GROUNDING-authorized). Legit embeddings passes intact (values + statistics preserved); leaked_emb / statistics.leaked_stat / leaked_pred ALL dropped, declared siblings kept; object smuggled under SCALAR values → whole values dropped, SECRET absent. No leak through the new OBJECT node; no over-drop.
  result: pass
  quadrant_classification: hard-easy (the hard part is discovering the CURRENT real Vertex shape — resolved by gsearch against Google's published schema; falsifying the pin once known is a cheap re-fetch+compare)
- probe_id: V-M7-SEAL (fail-CLOSED seal-audit regression + independent secret-value grep)
  description: Re-confirm the seal-audit gate still holds + fails-closed over the amended tree; independently GREP the whole service tree + config + catalog TOMLs + demo for real secret VALUES (slot NAMES only = pass).
  command_or_method: VERA script — real seal_audit()/scan_findings() over 50 service+config+catalog+demo files (tests/ excluded — attack-input fixtures) + a planted-real-shaped-secret temp file to prove fail-closed; ripgrep for tskey-shaped / base64>=80 / PEM-private-key literals across secure_core + builder_deploy_core.
  expected: 0 findings over the deliverable; SealAuditError raised on the planted secret; ZERO secret VALUES in the tree (only slot NAMES + the seal-audit's own detection regex).
  observed: real seal_audit findings over 50 files = 0 (clean); planted real-shaped tskey + base64 blob in a throwaway temp → SealAuditError (3 findings) — gate fails CLOSED. Independent grep: 0 tskey-shaped literals, 0 base64 blobs >=80 in service/config/catalog, the ONLY "BEGIN PRIVATE KEY" hit is sealaudit.py:40 (the gate's OWN detection regex, a pattern def not a value) + its .pyc. DC3 TOMLs carry GCP_SA_KEY_B64 / TS_AUTHKEY / POSTGRES_PASSWORD as config-key NAMES only.
  result: pass
  quadrant_classification: easy-easy (deterministic shape-match gate; fail-closed on >=100-entropy; the <100 novel-format bound is the acknowledged wp#2 residual)
- probe_id: V-NOREGRESSION (INV-DEST/BIND/LANE/PRINCIPAL + two-phase audit + rate-limit)
  description: Confirm the non-M2 invariants the amendment did not touch still hold + fail-loud (the rev5→rev6 delta was confined to r1+r2 per ARGUS's 156ins/42del mechanical diff).
  command_or_method: the P-M1/P-M3/P-M4/P-M5/P-M6 arms of the secure-core suite re-run (part of SUITE-secure_core), read against the unchanged registry.py INV-DEST/INV-LANE + handler.
  expected: P-M1 (SSRF/DEST) green; P-M3 (BIND) green; P-M4 (cross-lane + a2 unresolvable + a3 multi-cap) green; P-M5 (two-phase audit crash-window) green; P-M6 (rate-limit) green.
  observed: P-M1 9/9, P-M3 7/1-skip, P-M4 9/9 (incl a2 denial-at-resolution + a3 reject-ambiguous), P-M5 5/5 (crash-after-egress leaves durable value-free INTENT), P-M6 4/4 — all green. INV-* remain fail-LOUD (refuse-to-serve / refuse-to-load / 403-zero-egress). No regression from the INV-RESP amendment.
  result: pass
  quadrant_classification: easy-easy
- probe_id: V-FENCE (scope fence + frozen-file integrity)
  description: nothing committed/pushed; frozen resolve.py byte-identical to main; DC3 TOMLs byte-identical to arc-76; author=Denson Smith on the 3 changed files.
  command_or_method: git rev-list --count main..HEAD; git diff main -- resolve.py; git status --porcelain resolve.py; sha256sum the two DC3 TOMLs; head -1 the 3 changed files.
  expected: 0 commits ahead; empty resolve.py diff + clean working tree; DC3 sha256 == prior reference; author=Denson Smith.
  observed: 0 commits ahead of main (build work is working-tree only — only tracked mod is the roster-pin test_dataload.py); resolve.py diff empty + working-tree clean (frozen); vertex-gemini.toml sha256=11c881057f93... , tailscale.toml sha256=5bb085eff7ec... (both byte-identical to the prior VERA/arc-76 reference); author=Denson Smith on redact.py, registry.py, test_pm2_response_redaction.py. arc-76/build + main untouched.
  result: pass
  quadrant_classification: easy-easy

threat_coverage:
- mitigation: M2
  threat: key-exfil via response/log — incl. credential nested at depth>=3 in a declared field (r-rev5), an object smuggled under a SCALAR slot (r1), and a future field mis-marked PASS_WHOLE (r2)
  defeats_via_probe: P-M2
  probe_evidence: SUITE-secure_core P-M2 = 15 green (a.1 undeclared + a.2 nested-depth3 + a.3 SCALAR-slot direct/list/doubly-nested + a.4 PASS_WHOLE-misplace/legacy-bare-list refuse + legit content whole) AND VERA adversarial V-M2a2-DEPTH / V-M2a3-SCALAR / V-M2a4-PLACEMENT / V-META-DEEPCOPY / V-M2b-NOOVERDROP / V-EMBED-PIN — all executed, all HELD.
  attack_path_exercised: caller induces a credential echo in the Vertex response at (a.2) an undeclared sub-key at depth 3/4/5 of a declared recursed OBJECT → DROPPED from caller AND both audit phases; (a.3) an object/dict smuggled under a SCALAR field, direct/list/doubly/triply-nested → whole value DROPPED via recursive dict-scan; (a.4) a non-allowlisted field marked PASS_WHOLE → loader REFUSES TO LOAD naming the actual violating field (deepcopy-singleton fix confirmed right-reason). AND (b) legit: declared nested scalars/list-of-scalars intact, allowlisted candidates.content whole-passes an arbitrary untruncated model product, legit embeddings OBJECT (values+statistics, web-verified vs current Vertex) intact while undeclared embeddings sub-keys drop.
- mitigation: M1
  threat: SSRF / forward-anything egress
  defeats_via_probe: P-M1
  probe_evidence: SUITE-secure_core P-M1 9/9 (every url_slot FIXED/ENUM + disjoint; redirect-off; loader refuses free-form + params-derived slot; caller destination-injection rejected zero-egress; legit reaches only the pinned host). Untouched by the rev6 delta.
  attack_path_exercised: caller supplies attacker host via slots/params → rejected/refused ZERO egress, only pinned *-aiplatform.googleapis.com reachable; legit ENUM selection resolves.
- mitigation: M3
  threat: identity-header forgery via non-loopback bind
  defeats_via_probe: P-M3
  probe_evidence: SUITE-secure_core P-M3 (routable bind → BindError refuse-to-serve; 0600 refuse logic exercised cross-platform, 6 wrong modes raise). Real-AF_UNIX os.stat = the one honest Phase-3 skip. Untouched by the rev6 delta.
  attack_path_exercised: handler configured routable → refuse to serve non-zero, identity surface never exposed; loopback/0600 permitted.
- mitigation: M4
  threat: over-broad authz → cross-lane reach (incl. permissive-default resolve + multi-cap union)
  defeats_via_probe: P-M4
  probe_evidence: SUITE-secure_core P-M4 9/9 (newswire→generate_grounded 403 zero-egress; a2 unmapped-cap/absent-header denied AT RESOLUTION; a3 loader refuses unknown-scope + serve-caps-mismatch + multi-cap non-registered reject-ambiguous; legit science→generate + newswire→embed + registered multi-lane authorized). Untouched by the rev6 delta.
  attack_path_exercised: one lane's tag (or unresolvable/multi-cap principal) reaches another lane's op → 403 ZERO egress at the correct stage with the audited reason; legit paths authorized.
- mitigation: M5
  threat: audit gap
  defeats_via_probe: P-M5
  probe_evidence: SUITE-secure_core P-M5 5/5 (crash after egress leaves durable value-free INTENT carrying lane; params_digest irreversible; value-channel key rejected). Untouched by the rev6 delta.
  attack_path_exercised: crash in egress→outcome window → INTENT of the executed credentialed call survives, value-free, lane-attributed.
- mitigation: M6
  threat: quota exhaustion / DoS
  defeats_via_probe: P-M6
  probe_evidence: SUITE-secure_core P-M6 4/4 (burst → 429; second lane unthrottled — the per-lane bucket is the boundary; per-(lane,skill_id) sub-bucket throttles one skill not its sibling). Untouched by the rev6 delta.
  attack_path_exercised: one lane floods shared quota → its per-lane bucket 429s; a second lane's low-rate traffic is NOT throttled.
- mitigation: M7
  threat: secret-value leakage into code/config/catalog/logs (incl. marker-laundered)
  defeats_via_probe: P-M7
  probe_evidence: SUITE-secure_core P-M7 9/9 + VERA V-M7-SEAL: real seal_audit() over 50 service+config+catalog+demo files = 0 findings; planted real-shaped secret → SealAuditError (fail-closed); independent grep = zero secret VALUES (only the gate's own detection regex + slot NAMES). Seal-audit code untouched by the rev6 delta; re-confirmed against the amended tree.
  attack_path_exercised: a real (or marker-laundered) secret VALUE lands in an artifact → build REFUSES non-zero; slot-names + shape-clean marked-in-fixtures build PASSES.

methodology_concerns:
- (verification-method note, NOT a build defect) My first-pass V-M2a4/V-META probe used a bare `"candidates.content" in msg` substring check to assert the refusal did not misfire at content. It logged 4 false FAILs because the LoaderError message ALWAYS prints the allowlist enumeration `['candidates.content']` — a live instance of the §5.11 regex-anchoring pitfall (verify count/location, not raw substring). Refined by anchoring on the quoted `field '<path>'` token: 5/5 PASS. The loader's behavior is correct; the message correctly quotes the violating field distinctly from the allowlist listing. Optional non-blocking nicety for downstream tooling: the refusal message could format the allowlist so naive greps don't collide, but the quoted `field '...'` token already disambiguates — no remediation needed.
- (carried, unchanged) The AF_UNIX real-listener os.stat integration remains the single honest Phase-3-on-Linux skip; the 0600 fail-loud LOGIC is genuinely exercised cross-platform. Not a regression.
- (carried, unchanged) seal-audit <100-entropy novel-format floor is the acknowledged wp#2 residual of a deterministic shape-match gate (fails closed on >=100 entropy). Not a regression.
- (commit-stage hygiene, carry to the WRITER/NOMOS stage) the worktree-root .venv/ and a builder-deploy-core/build/lib/ pip-build copy are untracked and not gitignored; stage ONLY the deliverable (secure-core/, the two DC3 TOMLs, demo/, design/, verdicts/, the roster-pin test_dataload.py) — exclude .venv/ and build/lib/.

falsifying_evidence_summary:

verification_artifacts_path: agents/verdicts/stoa--q7f/vera-rev6-reverify.md (this verdict). Adversarial probe scripts recorded in the dispatch scratchpad: vera_rev6_adversarial.py (39 checks — 34 direct PASS + 4 §5.11 false-positives reclassified), vera_rev6_a4_refined.py (5/5 anchored A4/META PASS), vera_seal_grep.py (real seal_audit clean + fail-closed proof). Design probe suites at agents/secure-core/tests/ (60/1) + agents/builder-deploy-core/tests/ (105) re-run against REAL code from the per-worktree .venv (no arc-76 bleed).

summary: I re-verified ADA's rev6 INV-RESP amendment INDEPENDENTLY against REAL code from the per-worktree .venv (secure_core AND builder_deploy_core both resolve from the arc-77 worktree — no arc-76 bleed). The whole contract is GREEN: secure-core 60 passed / 1 honest Phase-3 skip (up from 50/1 at rev4 — the +10 are the rev5/rev6 P-M2 a.2/a.3/a.4 clauses), builder_deploy_core 105 passed, DC3 demo exit 0 value-free. Beyond re-running ADA's tests I drove my OWN adversarial probes deeper than the planted ones and the recursive grammar HELD by construction: (a.2) a credential in undeclared sub-keys at depth 3/4/5 of the declared recursed OBJECT tree is dropped at every level while declared siblings stay intact; (a.3) an object smuggled under a SCALAR field — direct, list-nested, doubly-, triply-nested, dict-in-tuple, deep-mixed — has its whole value dropped by a genuine recursive dict-scan, while legit scalars and arbitrarily-deep arrays-of-scalars are NOT over-dropped; (a.4) a non-allowlisted field marked PASS_WHOLE at three specific locations refuses to load, naming the actual violating field. The LOAD-BEARING META-CHECK is confirmed: ADA's copy.deepcopy singleton fix (__copy__/__deepcopy__/__reduce__ return self) makes markers survive deepcopy/copy/pickle as the SAME instance, so a deepcopy+plant of a non-allowlisted PASS_WHOLE at candidates.finishReason now fails-closed naming candidates.finishReason (the ACTUAL violation) — NOT candidates.content — and my TEETH check (a shattered fresh _NodeMarker at content) reproduces the exact a.4-passing-for-the-wrong-reason misfire the fix eliminates. The embeddings=OBJECT deviation is correct: I web-verified (gsearch) the current real Vertex text-embedding-005 :predict shape and it is an EXACT match for ADA's pin {values:[float], statistics:{token_count:int, truncated:bool}} — the design's illustrative SCALAR would over-drop the real embeddings object and break embed, so the drift-to-OBJECT is a V-RESP-GROUNDING-authorized correctness fix; a legit embeddings passes intact while undeclared embeddings sub-keys (and an object smuggled under the SCALAR values slot) drop. No regression: INV-DEST/BIND/LANE/PRINCIPAL, the two-phase audit, rate-limit, and the fail-CLOSED seal-audit all hold and remain fail-loud; the real seal_audit() gate is clean over 50 service+config+catalog+demo files and fails closed on a planted secret, and my independent grep found ZERO secret VALUES anywhere in the deliverable (only the gate's own detection regex + slot NAMES). Scope fence held (0 commits ahead of main, frozen resolve.py + DC3 TOMLs byte-identical to arc-76, author=Denson Smith on all 3 changed files). The one methodology note is about MY probe (a §5.11 substring false-positive on the allowlist enumeration, corrected by anchoring), not the build. Verdict: PASS — the amendment holds by construction, no regression, the deepcopy fix fails-closed for the RIGHT reason, the embeddings pin matches current real Vertex, and no secret value leaks.
```
