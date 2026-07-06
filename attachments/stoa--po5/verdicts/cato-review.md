<!-- author: Denson Smith -->
<!-- seat: CAPTAIN_CATO_the_stoa (REVIEWER) — cold-read review of arc-77 rev6 secure-core BUILD -->
<!-- ticket: stoa--q7f | arc-77 | coordination stoa--po5 | u--9s2 Phase-1 increment 2.4 -->

# CATO review verdict — arc-77 secure-core rev6 (stoa--q7f)

Independent cold-read of the arc-77/build deliverable (I did not build and did not verify it): the untracked secure_core/ package (13 modules + tests), the two reproduced DC3 catalog TOMLs, the DC3 demo, and the tracked test_dataload roster-pin. Compared against design-rev6.md as the contract; meta-verified against VERA rev6 re-verify. All findings are NON-BLOCKING nits.

```
status: completed
ticket: stoa--q7f
verdict: pass
diff_reviewed: arc-77/build @ worktree .claude/worktrees/arc-77-build — untracked secure-core/ pkg (13 secure_core modules + tests + pyproject/README/.gitignore) + builder_deploy_core/data/catalog/vertex-gemini.toml + tailscale.toml + builder-deploy-core/demo/sos_core_emit_demo.py + tracked mod builder-deploy-core/tests/test_dataload.py
design_artifact_compared_against: agents/design/stoa--q7f/design-rev6.md (§5.1a recursive NODE grammar + PASS_WHOLE_ALLOWLIST; §2.1/§2.4 INV-LANE/INV-PRINCIPAL; §3.1 seal-audit; §5.1/§5.2/§5.3 contract + map + DoD)
concerns:
- id: c1
  category: hygiene
  description: handler.py imports three symbols never referenced — RateLimited and ProviderError (from secure_core.errors) and ENUM (from secure_core.slots). The rate-limit path returns a CallResult directly rather than raising RateLimited; egress failures are caught as generic Exception rather than ProviderError; _build_destination references only FIXED (ENUM is resolved polymorphically via slot.resolve). Dead imports.
  evidence: agents/secure-core/secure_core/handler.py:19 (RateLimited, ProviderError) and :22 (ENUM)
  severity: recommended-revision
  quadrant_classification: easy-easy
- id: c2
  category: consistency
  description: Stale design-ground-truth citations. README.md, pyproject.toml, and the module headers of identity.py / audit.py / errors.py / sealaudit.py / server.py cite design-rev4.md or design-rev2.md while the active/final design is rev6. Lineage citations to rev2/rev4 are defensible for content that originated there, but the README INV-RESP row under-describes the shipped behavior — it says only "per-op response_schema allow-list; op with no schema refuses to load" and never mentions the rev5/rev6 recursive NODE grammar, SCALAR recursive dict-scan, or PASS_WHOLE_ALLOWLIST this arc ships. redact.py and registry.py (the rev6 delta) correctly cite rev6.
  evidence: agents/secure-core/README.md (INV-RESP table row + design ground-truth line) and pyproject.toml design-ground-truth header
  severity: minor
  quadrant_classification: easy-easy
- id: c3
  category: consistency
  description: The DC3 demo header labels the increment Phase-2 increment 2.4 while every secure_core module header, the design, and the arc label it Phase-1 increment 2.4. A one-word label inconsistency in a carried file (the demo is reproduced DC3, not new this arc).
  evidence: agents/builder-deploy-core/demo/sos_core_emit_demo.py:2
  severity: minor
  quadrant_classification: easy-easy
- id: c4
  category: hygiene
  description: Commit-stage exclusion — NOT a code defect, staging guidance. The worktree-root .venv/ is NOT covered by any .gitignore (secure-core/.gitignore and builder-deploy-core/.gitignore each scope build/ + .venv/ to their OWN subtree, so build/lib IS ignored and the secure-core egg-info/__pycache__/.pytest_cache ARE ignored, confirmed via git check-ignore, but the worktree-ROOT .venv is not). A git add . or -A would wrongly stage the entire .venv site-packages tree (pip, editable-install shims, thousands of files). Stage ONLY the named deliverable paths; do NOT git add . / -A / -f.
  evidence: git status --untracked-files=all shows .venv/Lib/site-packages/... as untracked (not ignored); git check-ignore .venv returns nothing
  severity: recommended-revision
  quadrant_classification: easy-easy
follow_ups:
- The AF_UNIX real-listener os.stat arm (bind.py assert_listener_safe) is skipped on the Windows build host (socket.AF_UNIX absent); the 0600-refuse LOGIC is exercised cross-platform via the pure assert_bind_target_safe. Design-acknowledged Phase-3 real-runtime residual, honestly disclosed by ADA and VERA — a Phase-3 re-run item, not an arc-77 gap. No action this arc.
- The seal-audit shape-match set is a fail-closed floor on >=100-entropy blobs; a novel <100-entropy secret format is the acknowledged design wp#2 residual (fail-closed on ambiguity is the mitigation). A named bound, not a defect.
verifier_coverage_assessment: VERA rev6 re-verify EXERCISED the load-bearing security surface and did NOT overstate. It re-ran the FULL suites from the per-worktree .venv (secure-core 60 passed / 1 honest AF_UNIX skip; builder_deploy_core 105; demo exit 0) AND drove its OWN adversarial probes DEEPER than ADA planted on all three INV-RESP node types: a.2 credential at depth 3/4/5 in undeclared sub-keys of the declared recursed OBJECT (all dropped, declared siblings intact); a.3 an object smuggled under a SCALAR field in six shapes incl triply-nested and dict-in-tuple (whole value dropped by a genuine recursive dict-scan, legit scalars/arrays NOT over-dropped); a.4 a non-allowlisted PASS_WHOLE at three specific fields (loader refuses to load, naming the ACTUAL violating field). The load-bearing META-CHECK on the deepcopy-singleton fix is confirmed with a teeth-check (a shattered fresh marker reproduces the exact a.4-passing-for-the-wrong-reason misfire the fix closes). The embeddings=OBJECT deviation was independently web-verified (gsearch) against current real Vertex text-embedding-005 :predict = exact match. The fail-closed seal-audit was re-confirmed over 50 files + an independent secret-value grep = zero. No-regression on INV-DEST/BIND/LANE/PRINCIPAL + two-phase audit + rate-limit. Item-11 threat-coverage cross-check: VERA threat_coverage carries M1..M7, each with defeats_via_probe P-M<n> bound to a non-empty probe_evidence naming the executed SUITE + adversarial probes — no missing or unbacked line. The two disclosed residuals (AF_UNIX real-listener, <100-entropy novel format) are honest bounds, not silent gaps. No CATO coverage_concern against VERA.
summary: A clean, disciplined, well-documented security build that faithfully implements design-rev6. The load-bearing surfaces are correct on cold-read: redact.py implements the recursive NODE grammar with copy/deepcopy/pickle-safe singleton markers (identity-compare survives the deepcopy a registry probe naturally does), the SCALAR node is a genuine recursive dict-scan (drops any mapping at any depth, not a shallow top-level check), and PASS_WHOLE placement is deny-by-default via a loader-enforced PASS_WHOLE_ALLOWLIST = candidates.content; registry.py _validate_resp_node walks the dotted path and refuses to load a bare-list legacy node OR a non-allowlisted PASS_WHOLE; identity.resolve_principal is explicit-membership-only with no .get(cap, DEFAULT), unresolvable/ambiguous raising Forbidden AT RESOLUTION; handler.py denies fail-loud at every stage with zero egress and a value-free audit record and never falls through to a permissive default; sealaudit.py is fail-closed with the synthetic-marker exemption correctly gated on the INTERSECTION of path-bound AND shape-clean (a real-shaped or mis-placed marked value still fails). The embeddings=OBJECT deviation from the design illustrative SCALAR is RECONCILED, not silent drift: documented inline as a DRIFT NOTE, it is the V-RESP-GROUNDING build-pin the design itself mandates, is web-verified against current Vertex by both ADA and VERA, and preserves INV-RESP by construction (undeclared sub-keys still drop). Authorship is Denson Smith on every author field (the seat-built-by ADA lines are the substrate seat-identity convention layered on top, compliant); zero secret values in the deliverable; no dead code or debug artifacts in the service. The only findings are nits: three unused imports in handler.py (c1, worth a trivial pre-commit sweep), stale rev4/rev2 ground-truth citations with an under-described README INV-RESP row (c2), a Phase-2-vs-Phase-1 label typo in the carried demo (c3), and the commit-stage guidance that .venv/ is not root-gitignored so staging must name the deliverable paths (c4). None block. Posture: PASS — cleared for NOMOS + commit; recommend ADA sweep c1 (and optionally c2/c3) in a trailing touch on arc-77/build before the commit, and stage-by-path per c4.
```
