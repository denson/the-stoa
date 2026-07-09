status: completed
ticket: stoa--p0e
verdict: revise
design_artifact_audited: agents/design/stoa--p0e/design-rev1.md
overall: PASS-WITH-RISKS (revise) -- core mechanism verified sound; no invariant violated, no safety break; several real completeness/accuracy defects, two of them consumer-facing.

audit_block:
  verified_sound (load-bearing spine -- cold-checked against the repo, not the design self-claims):
  - DISARM MECHANISM: web-verified (gsearch) that Claude Code uses an explicit hook-registration model -- loose scripts in .claude/hooks/ are NOT auto-executed. Removing the settings.json registration disarms the gate; the archived/orphan script is inert. Retirement disarm is correct.
  - HOOKLIB SAFETY (duty 2): CONFIRMED. classify_author_file / extract_author_fields / parse_allow_pairs are called ONLY by the retired gate (pretooluse-author-field-audit.sh:154/161/168) and the author-gate test (archived). stop-self-check.sh sources _hooklib.sh (line 41) but does NOT call the author functions -- it uses only the generic helpers. Leaving the dead functions in place is safe. Design 2.3 claim holds.
  - PROPAGATION MODEL (duty 5): CONFIRMED against check.sh. Skills ARE enumerated (enumerate_deployed recursively finds every file per SKILL_NAMES dir, check.sh:464-472); hooks are NOT enumerated anywhere (enumerate_deployed + enumerate_workspace_substrate_paths); templates ARE enumerated (check.sh:453-456). advisory skill gained -> MISSING -> apply; source template retired -> deployed candidate DRIFTED -> apply; retired hook script -> invisible to check.sh (orphan, W1/M4 correct). Design section 6 holds.
  - DIFF-SCOPING P1/P2 (duty 4): CONFIRMED. P1 removed copyright line matches the copyright form -> PRIMARY fires. P2 new-file all-plus, principal value on allow-list -> zero findings. MUST-FLAG / MUST-NOT split correct.
  - NO THIRD REGISTRATION LAYER: no settings.local.json anywhere in the tree; only .claude/settings.json + the two templates carry the registration.

  risks:
  - id: r1
    description: Retirement completeness -- the design edit list (2.1) touches only .claude/settings.json (armed live config) plus substrate/templates/settings-hooks.json (source), but the-stoa dogfoods its OWN deployed .claude/, which also holds .claude/templates/settings-hooks.json (byte-identical, still carries the registration), .claude/hooks/pretooluse-author-field-audit.sh (deployed script), and .claude/hooks/principal-identity (stale comment). None are in the edit list; P3 does not check them. The safety-critical disarm (live settings.json) IS handled; the residuals rely on an unscheduled post-merge .claude/ regen (install.sh on main, per the slug-basename discipline) that the design never names.
    evidence: design 2.1 + 10 (P3) vs grep hits at .claude/templates/settings-hooks.json and .claude/hooks/pretooluse-author-field-audit.sh in the worktree; P3 asserts only against .claude/settings.json + substrate/templates/settings-hooks.json.
    load_bearing: uncertain
    quadrant_classification: easy-easy
  - id: r2
    description: Design 10 states the advisory test corpus is source-only and does not deploy, mirroring the author-gate source-only posture. FALSE for a skill. install.sh deploys skills via recursive cp -R (install.sh:1338), so the skill tests/ subdir deploys to every consumer .claude/skills/attribution-advisory/tests/. The author-gate posture works ONLY because hooks deploy via a NON-recursive *.sh glob (substrate/hooks/tests/README.md:6-8 says so explicitly). The design conflated the two deploy mechanisms. Self-consistent with check.sh (recursive find enumerates the same files, no drift) and fixtures are inert, but the mechanism model is wrong -- decide whether consumer test-deploy is acceptable or relocate the corpus off the deployed skill path.
    evidence: design 10 claim vs install.sh:1338 (cp -R wholesale) + substrate/hooks/tests/README.md:6-8.
    load_bearing: false
    quadrant_classification: easy-easy
  - id: r3
    description: Design 5 install.sh comment-update scope is incomplete. It names ~1490 and ~85 but misses author-field-gate references at install.sh:689-692, :1471, :1907, and under-specifies the seeded-file comment block :1488-1497. That block is DEPLOYED verbatim into every consumer .claude/hooks/principal-identity and states the commit is denied (line 1492) -- factually FALSE after retirement (the advisory never denies). Stale + actively-wrong consumer-facing documentation; P3 does not catch it.
    evidence: grep author-field/author-gate in install.sh -> lines 85, 689-692, 1471, 1488-1497, 1907; design 5.3 names only ~1490, 5.5 names only ~85.
    load_bearing: uncertain
    quadrant_classification: easy-easy
  - id: r4
    description: substrate/hooks/tests/README.md is titled Author-gate regression corpus and documents the retired author-gate test. Design 2.4/2.5 moves the runner + author fixtures to v1-historical but leaves this README describing a test no longer present (only run-stop-self-check-tests.sh remains). Documentation drift; move it with the archived corpus or rewrite it for the surviving stop-self-check test.
    evidence: substrate/hooks/tests/README.md:1-8 vs design 2.4 (silent on this README).
    load_bearing: false
    quadrant_classification: easy-easy
  - id: r5
    description: PRIMARY name-agnostic detection fires on routine LEGITIMATE attribution edits -- copyright-year bumps, license reformats, PRINCIPAL self-name correction -- since any removed attribution line matches. The naturally-tiny-false-positive-rate claim (4.2) is somewhat optimistic. Acceptable under report-only (the report text says confirm legitimate, e.g. correcting YOUR OWN name) and matches W2/W5. Named for honesty, not a blocker.
    evidence: design 4.2 + 3 report template; the copyright regex _hooklib.sh:191-198 fires on any year+Capitalized-name removed line regardless of the name.
    load_bearing: false
    quadrant_classification: easy-hard
  - id: r6
    description: M1 detection covers only the sub-case where the original attribution appears as a removed minus-prefixed line WITHIN the diff. The classic plagiarism vector -- copying external OSS into a NEW file with the upstream header stripped -- produces no minus attribution line and no plus non-principal field, so BOTH PRIMARY and SECONDARY stay silent (false negative). Inherent limit of diff-scoping. M1 wording (MODIFIES or DELETES an existing line) is correctly scoped so NO overclaim -- but PLINY should not restate M1 as total plagiarism-defeat.
    evidence: design 9 (M1) + 4.2/4.3; diff-scoping cannot see content not in the diff.
    load_bearing: false
    quadrant_classification: hard-hard
  non_findings:
  - No fourth/hidden registration site: verified no settings.local.json and no ~/.claude registration in-tree; only the 2 named files + the deployed candidate (r1) carry it.
  - hooklib pruning risk: DISCHARGED -- design correctly leaves the lib intact; dead functions inert; no surviving caller.
  - Template comment header: design 2.1(b) claim that the _comment does not name the gate specifically is ACCURATE (it is generic).
  - check.sh false-OBSOLETE on the new skill: DISCHARGED -- deploy (cp -R) and enumeration (recursive find) both include the whole skill subtree, so deployed == source, no drift.
  - Advisory never-denies structural guarantee (P4): DISCHARGED -- a skill is never on a PreToolUse path; exit-0 with no deny JSON is treated as allow; P4 static + runtime probes cover it.

  m_item_confirmations:
  - M1 (plagiarism-direction edit) = threat-ratified: CONFIRM. A3 map present (design 9); threat-anchored probes P1 (attack-detected) + P2 (legit-unaffected) spec-d in design 10 -- satisfies op-disc 35 / ARGUS 6.9 clause 4. Scope boundary per r6 noted.
  - M2 (direction-1 regression residual) = not-threat-ratified: CONFIRM (defensible -- the SCOPE RESHAPE ruling de-ratified direction-1 as a runtime-gated threat). NOTE: the SECONDARY check (s1/s2 fixtures) touches the direction-1 surface but is not bound to any M-item probe set; to remove a latent mapless-mitigation ambiguity, either fold s1/s2 under M1 probes or mark SECONDARY explicitly as unratified courtesy. Low severity.
  - M3 (armed consumer live settings.json keeps dead registration) = not-threat-ratified (process/propagation gap): CONFIRM. Verified INHERENT to invariant 8 (never auto-write a live settings.json) -- no mechanical mitigation exists; the retired gate persisting at an un-updated armed consumer is persistence-of-old-control, not a NEW attack path. W1 correctly named.
  - M4 (check-substrate-updates does not enumerate hooks) = not-threat-ratified (process/propagation gap): CONFIRM. Verified against check.sh -- hooks unenumerated in BOTH passes; the orphan script truly cannot be flagged OBSOLETE. Inert without registration.
  - M5 (advisory false-neg/false-pos) = not-threat-ratified (best-effort report-only residual): CONFIRM. Report-only, no runtime attack path.
  - the-retirement-itself = not-threat-ratified (PRINCIPAL-ruled scope reshape): CONFIRM the 35.5 carve-out -- no NEW runtime attack path (direction-2/plagiarism coverage NET INCREASES via the advisory PRIMARY); direction-1 residual explicitly accepted + doctrine-covered. Genuine ARGUS-confirmation, not a PLINY self-grant.

  threat_coverage_assessment: M1 is the sole threat-ratified mitigation. Its A3 map (design 9) is present AND a threat-anchored probe is spec-d in design 10 (P1 + P2). No map-present/probe-absent smell (6.9 clause 4 satisfied). Design-time probe-SPEC adequacy: GOOD, with the r6 boundary -- the spec-d probe exercises the in-diff attack path (the correctly-scoped sub-case); it cannot exercise the external-copy-header-stripped vector. Threat-ENUMERATION completeness stays unmechanized judgment (r6 names the honest boundary).

summary: The design is fundamentally sound and buildable. The three load-bearing spines -- the disarm mechanism (removing the registration disarms; web-verified), the propagation model (skills enumerated, hooks not, templates drifted; verified directly in check.sh), and hooklib safety (surviving gates do not call the author functions) -- all hold under cold verification. Diff-scoping P1-fires / P2-silent is correct and all six M-item classifications are confirmable, with the retirement carve-out a genuine ARGUS confirmation. No invariant is violated and there is no safety regression. The revise verdict rests on completeness/accuracy defects rather than structural breakage: most important is r1 (the-stoa OWN deployed .claude/ residuals -- candidate template still carrying the registration, orphan script, stale seed comment -- neither in the edit list nor checked by P3; the live-config disarm IS handled, but the residuals lean on an unscheduled post-merge .claude/ regen the design never names), then r3 (install.sh comment-update scope incomplete, leaving a consumer-facing seed comment that falsely claims commits are denied) and r2 (the section-10 source-only-tests claim is wrong for a skill deployed via recursive cp -R). None block the build; all are cheap design-revision deltas. Posture: minor revisions.
gap_or_blocker: none
