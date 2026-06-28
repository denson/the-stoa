verdict: CONFORMANT
ticket: stoa--q7f (requirement sos--373; epic u--9s2)
checked_output: the PLINY arc-close for u--9s2 inc 2.4 (DESIGN gauntlet -- secure Railway core for stoa_of_science) = commit 26698475404fcb0add6e1f3f36ead4a548241507 on branch arc-76/build (11 files: design package + DC3 mock-emit). NOT merged to main, NOT pushed (a DESIGN gauntlet that relays UP to the Grand to gate; nothing real provisioned).

divergences: (none)

== Per-item audit (A-E) ==

A. Commit authorship + trailer -- CONFORMANT.
   - git show -s --format=%an<%ae> 26698475 => denson <densonsmith2@gmail.com>. ZERO foreign author.
   - git log -1 --format=%(trailers) => Co-Authored-By: PLINY_the-stoa <pliny_the-stoa@the-stoa.local> + Stoa-Session-Id: 7b08e6ca. Trailer parses; seat-identity layered ON TOP of the PRINCIPAL Author (CLAUDE.md section 28 compliance mechanism, not an Author override).
   - All 11 changed files audited for author-like fields: both catalog TOMLs + the demo carry "# author: Denson Smith"; design-rev1/rev2 + strabo research frontmatter "author: Denson Smith"; verdict .md files carry no author frontmatter (agent verdict artifacts; seat-signing is not an authorship field). No foreign human name in any author/owner/by/copyright position.

B. Gauntlet shape (by-the-book) -- CONFORMANT.
   Full STRABO -> DAEDALUS -> ARGUS -> ADA -> VERA -> CATO -> NOMOS sequence ran, traced on stoa--q7f + on-disk verdicts:
   - STRABO DC2 PASS (three premise clusters web-verified vs current 2026 primary sources, zero design-blockers) + r3 follow-up SOUND (tagged-node App-Capabilities, TS v1.92+). Artifact: agents/research/stoa--q7f/strabo-dc2-premises.md.
   - DAEDALUS rev1 (per-provider closed-registry; SSRF closed by construction) -> ARGUS REVISE (0 blockers / 5 majors / 1 minor; argus-dc1-security.md) -> STRABO r3 -> DAEDALUS rev2 (folds r1-r6 into INV-DEST/INV-RESP/INV-BIND + two-phase audit) -> ARGUS RE-AUDIT clean PASS (argus-dc1-security-reaudit.md). Both ARGUS verdicts on disk.
   - FM (POLYBIUS_the-stoa) rendered explicit FINAL GO for Phase C BEFORE ADA dispatch (charter 11:06:00Z), after independent verify-then-execute. NOT a solo-with-one-checker close (not the AR-7 failure shape).
   - VERA PASS (vera-dc3-emit.md) + CATO PASS-WITH-NITS (cato-dc3-review.md); ADA fixed both nits (c1 rename + c2 prose). All four verdicts present at agents/verdicts/stoa--q7f/.

C. DoD met (from the directive) -- CONFORMANT.
   (i) DC2 premises web-verified with cited primary sources (STRABO artifact present; per-premise citations inline; FM independently spot-checked the load-bearing Tailscale identity-header premise). PASS.
   (ii) DC1 ARGUS cold-audit PASSES on the security crux (gate-relevant artifact = argus-dc1-security-reaudit.md, clean PASS). PASS.
   (iii) DC3 mock-emit value-free, REPRODUCED INDEPENDENTLY by me in the worktree:
        - Changed-file set is EXACTLY the 11 design/research/verdict/2-TOML/demo/test files (git diff-tree --name-status). NONE of resolve.py/spec.py/port.py/mock.py/dataload.py/baseline.toml/kinds.toml is in the set.
        - Frozen-file diff (26698475~1..26698475) EMPTY for all 7 frozen files; resolve.py blob adade158bce45bed51760abe4c511892f641e4c8 == main (byte-identical).
        - 3-wall tripwire holds (re-run): W1 canonical I/O-import grep over provision/ EMPTY; W2 Provisioner.__subclasses__() == [MockProvisioner]; W3 emit_spec signature == [resolved, builder_slug] (no provisioner).
        - assert_value_free passes (demo step 4 spec; step 5 both RunLedgers; step 6 MeshShape) -- demo exit 0, all section 2.6 assertions PASS; blocked_slots == [GCP_SA_KEY_B64, POSTGRES_PASSWORD, TS_AUTHKEY] (slot NAMES only).
        - FULL builder_deploy_core suite GREEN: 105 passed / 0 failed (independently re-run; matches the claimed count). 10 tripwire/value-free tests pass.
   (iv) credential-discipline holds in the design: agent-never-holds-secrets; out-of-package human/CI steps named (SA mint + WIF + Railway secret-set + tagged Tailscale auth-key); builder holds only a tailnet identity (TS_AUTHKEY tagged). PASS.
   (v) ZERO real infra/creds/money: grep over the 3 committed source files for real Railway/gcloud/tailscale CLI invocations or credential-value patterns (ya29./AIza/sk-/BEGIN-key/tskey-auth-) EMPTY. The TOMLs hold slot NAMES only; the demo makes zero real net/cred calls. PASS.

D. Scope / PRINCIPAL-gate -- CONFORMANT.
   The design crosses NO gate by itself: it defers ALL real provisioning behind the Grand-gate AND an explicit PRINCIPAL provision-go (directive out-of-scope; commit message states this explicitly). The commit is on arc-76/build (git branch --contains 26698475 => arc-76/build only; git merge-base --is-ancestor 26698475 main => NOT on main), NOT pushed. stoa--q7f is appropriately NOT closed -- it relays UP; the FM/user-tier/Grand own the gate + closure. PRINCIPAL-gate probe (op-disc section 25): no gated operation executed; ratification correctly deferred, not bypassed.

E. The D1 finding integrity -- CONFORMANT.
   The commit design reconciles to shipped reality. resolve.py:78-80 raises ResolutionError(unknown category: <cat>) on an unknown category; "none" is not a library category, so resolve() is structurally forced to raise. Confirmed BY A RUN: demo step 2 imports the real frozen resolve() and prints "[OK] frozen resolve() still rejects category=none (drift D1 confirmed; resolver byte-unchanged)", while the section 2.4 resolved set is composed as sorted(baseline UNION delta.add) directly (== section 2.4 golden, 8 entries) and emit_spec on it == section 2.5 golden. design-rev2 section 2.6 step 2 (L544-558) AND section 4/DC5 step 1 (L617-623) now state the direct composition + carry the FINDING for the Grand at the provision gate. NO remaining claim that resolve() is called on a category=none manifest.

ground_truth_consulted:
   - bw: stoa--q7f (full charter history -- STRABO/DAEDALUS/ARGUS/ADA/VERA/CATO/FM-go comments + the two ARGUS verdicts + VERA/CATO verdicts); sos--373 (stoa_of_science requirement); the directive (git show beadwork:attachments/stoa--q7f/u9s2-phase2-inc4-design-directive.md).
   - git: rev 26698475404fcb0add6e1f3f36ead4a548241507; git show -s --format=%an/%ae + %(trailers); git diff-tree --name-status; git diff 26698475~1..26698475 over the 7 frozen files; git rev-parse 26698475:resolve.py vs main:resolve.py (blob adade158); git branch --contains; git merge-base --is-ancestor 26698475 main.
   - repo (worktree arc-76-build): python -m pytest -q (105 passed/0 failed); W1 grep over provision/; W2 Provisioner.__subclasses__(); W3 emit_spec signature; python demo/sos_core_emit_demo.py (exit 0); real-infra/cred grep over the 2 TOMLs + demo; author-field grep over all 11 committed files; test_dataload.py diff (c1 rename + membership-only roster pins 4->6); design-rev2 section 2.6/section 4 D1 reconciliation prose.

summary: I audited the PLINY arc-close for u--9s2 inc 2.4 (the DESIGN gauntlet for the secure Railway pass-through core, commit 26698475 on arc-76/build) against the directive, requirement sos--373, the full stoa--q7f charter, and the worktree repo. Every checkable claim matches ground truth. The gauntlet ran by-the-book (STRABO -> DAEDALUS -> ARGUS REVISE -> STRABO r3 -> DAEDALUS rev2 -> ARGUS clean RE-AUDIT -> FM GO -> ADA -> VERA PASS -> CATO PASS-WITH-NITS -> both nits fixed), not a solo close. I independently reproduced the load-bearing DoD facts: the changed-file set is exactly the 11 named files with NO frozen-file edit; resolve.py is byte-identical (blob adade158); the 3-wall tripwire holds; the demo exits 0 with all section 2.6 value-free assertions passing; the full builder_deploy_core suite is 105/0 green; the real-infra/credential grep is empty; authorship is Denson Smith zero-foreign with a parsing PLINY seat-trailer. The load-bearing item E (D1 finding integrity) is the only one with prior drift, and it is genuinely reconciled: a live run of the frozen resolve() confirms it rejects category=none, the design now composes baseline UNION delta directly and carries the finding for the Grand at the provision gate in both section 2.6 and section 4. The design crosses no PRINCIPAL gate -- it correctly defers all real provisioning behind the Grand-gate + an explicit provision-go; the commit is not merged to main and not pushed; stoa--q7f is correctly left open to relay UP. Verdict: CONFORMANT. The output may propagate UP to the Grand to gate.
