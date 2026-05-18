Read .claude/MAJOR_PLINY.md and assume the orchestrator role for the-stoa.

Your immediate intent for this session: Build Arc 38 per the build directive at substrate/arcs/arc-38-build-directive.md. **3-candidate substrate architecture bundle (PRINCIPAL-ratified after 4-pass spec-audit iteration cadence):**

- **C1: stoa--ojz (P2)** — CAPTAIN_TIRO new role file (bw substrate specialist; read-direct + write-advisory split per SPECIFICATION.md §4.6)
- **C2: stoa--bj5 (P2)** — user-tier substrate drift detection (extend check-substrate-updates skill; per-file-marker scheme for substitution-tracking)
- **C3: stoa--gq1 (P3)** — substrate-component design principles (new operating-disciplines.md section; agent-installable distribution model + composability framing)

**PRECONDITION:** Spec-recon cycle (R1-R4 audit iteration) complete + accepted per SPECIFICATION.md §13.10 Pass 8 partial-execution + §13.10 bullet 4 NC8 known-residue parenthetical. the-stoa main at `68c0c12`. Local main = origin/main + no orphan arc-build branches verified by user-tier POLYBIUS at dispatch authoring.

Cron hygiene FIRST (before any substantive work): Run CronList; if any cron is present, CronDelete it. Surface-and-wait per MAJOR_PLINY.md §6.2 (no cron) is the default for PLINY; defense-in-depth.

Pre-branch hygiene per MAJOR_PLINY.md §5.9: before creating arc-N/build, run two checks.

Check 1 (no other arc-build branch in flight):
  git branch | grep -E '^\s*arc-[0-9]+/build$'    # must be empty

Check 2 (local main = origin/main):
  git fetch origin main
  git log --oneline main..origin/main             # must be empty
  git log --oneline origin/main..main             # must be empty

If either check fails, surface to user-tier POLYBIUS (or PRINCIPAL via [for: PRINCIPAL]
tag when user-tier unavailable) with the specific state observed.

**Worktree convention per MAJOR_PLINY.md §5.9.4 (directive A20):** create arc-38/build in separate worktree: `git worktree add .claude/worktrees/arc-38-build arc-38/build`. Main worktree stays on main.

**Read first (in order):**

1. **`substrate/arcs/arc-38-build-directive.md`** — load-bearing spec for all 3 candidates. A1-A20 LOCKED. A5/A8/A11/A13 are DAEDALUS sub-decisions (TIRO install.sh wiring; bj5 per-file-marker scheme; gq1 insertion locus + N-evidence framing).
2. **All 3 source ticket bodies:** `bw show stoa--ojz` (C1) + `bw show stoa--bj5` (C2) + `bw show stoa--gq1` (C3).
3. **`the-stoa/SPECIFICATION.md` §4.6** (TIRO scope-lock PRINCIPAL-ratified 2026-05-17) + **§9.1** (bw tools + specialist-delegation framing) + **§12.5** (Arc 38 candidates context) + **§13.5** (Pass 4 Arc 38 enumeration) + **§14** (PRINCIPAL editing notes — context on structural-§12 shape).
4. **`HUMAN_paste-polybius-arc-38-instruction.md`** in the project root — POLYBIUS's activation paste; same content frame as the directive.
5. **`substrate/CAPTAIN_BARTLEBY.md`** — closest CAPTAIN-shape precedent for TIRO (bounded-toolset specialist that returns structured answers to dispatcher).
6. **`substrate/skills/check-substrate-updates/`** — current skill structure (check.sh / apply.sh / revert.sh / consumer-workspaces.txt) for bj5 extension surface.
7. **`substrate/consumer-workspaces.txt`** — current registry shape for the user-tier addition (bj5).
8. **`substrate/operating-disciplines.md`** — primary canon surface (§12 bw cookbook for TIRO cite; §17 + §23 base-vs-custom for gq1 cross-ref; §27 mechanical/agent split for gq1 cross-ref + canon-pattern precedent; §28 Co-Authored-By trailer self-applied per A15 + gq1 cross-ref; §29 multi-team interop for gq1 cross-ref + alternate insertion-locus β; §30 four-layer identity for sibling Arc 37 canon; §31 NEW for gq1 per user-tier lean for A11 α).
9. **`substrate/MAJOR_POLYBIUS.md` §7** + **`substrate/MAJOR_PLINY.md` §5 + §6** — TIRO cross-ref targets per A6.
10. **`substrate/install.sh`** — TIRO wiring per A5 + bj5 wiring if A8 registry shape requires it.
11. **`substrate/arcs/arc-27-build-directive.md`** (stoa--uly precedent for new skill/agent addition) + **`substrate/arcs/arc-37-build-directive.md`** (most recent 6-candidate bundle precedent for §13.5 Pass 4 framing).
12. **`SPEC_AUDIT_R4.md` + `SPEC_AUDIT_R3.md` + `SPEC_AUDIT_R2.md` + `SPEC_AUDIT.md`** — context on the 4-pass audit-iteration cadence. Arc 38 is the FIRST forward arc after the iteration converged; the audit-cadence framing is informative for understanding the spec's structural shape. stoa--bbi (N=4 substrate-principle-refinement accretion ticket) captures the empirical anchor.
13. **`stoa--6wp`** ticket body + Arc 37 `bb12806` empirical anchor — the squash-merge `--body` regression PLINY must avoid in Phase 4. Arc 38 should ship trailer-clean on the squash-merge body forward of the Arc 37 regression (Arc 40 ships the canon fix later; Arc 38 applies the discipline ahead).

Operating mode for this dispatch: AUTONOMOUS. Run all four phases heads-down. Use stoa--ojz (work-unit + parent) for status updates. Surface to PRINCIPAL ONCE at end-of-arc with final clean-PASS verdict.

Coordination: the-stoa PROJECT-TIER POLYBIUS is your radio-check peer (paste at HUMAN_paste-polybius-arc-38-instruction.md). User-tier POLYBIUS dispatched + will do QA pass at arc close. Bidirectional radio-check pattern per substrate/operating-disciplines.md §7. **Per Arc 36 §7.1 5th beat + §7.7 author-tag canon, POLYBIUS coordination comments carry `[from: polybius-the-stoa]` per the convention shipped in Arc 36 v2.** PLINY heartbeats over-comply with `[from: pliny-the-stoa]` (per Arc 36 + Arc 37 organic-adoption observation; harmless metadata per A2.5 case 4).

The architectural decisions A1-A20 are LOCKED in the directive. DAEDALUS treats this directive as primary input alongside the 3 source ticket bodies + the SPECIFICATION.md §4.6 TIRO scope-lock. Locked decisions encode:

**TIRO (C1):** A2 read-direct/write-advisory split (PRINCIPAL-locked per §4.6); A3 toolset Bash+Read+Grep+Glob; A4 role file structure mirrors CAPTAIN_BARTLEBY; A5 install.sh wiring DAEDALUS-discretion; A6 cross-refs from MAJOR_POLYBIUS.md + MAJOR_PLINY.md + op-disc §12.

**bj5 (C2):** A7 scope (extend check-substrate-updates skill to user-tier; 2026-05-14 empirical anchor); A8 per-file-marker scheme DAEDALUS-discretion (α/β/γ/δ; user-tier leans γ manifest); A9 user-tier registry shape DAEDALUS-discretion; A10 check.sh + apply.sh + revert.sh extensions LOCKED scope.

**gq1 (C3):** A11 insertion locus DAEDALUS-discretion (α new §31 / β subsection of §29 / γ before §29; user-tier leans α); A12 content shape (Principle 1 agent-installable flow + Principle 2 AI-as-primary-reader + Ariadne worked example + cross-refs); A13 N-evidence framing DAEDALUS-discretion (i Ariadne only / ii Ariadne+Stoa / iii Ariadne+Railway-speculation; user-tier leans ii).

**Universal/self-applied:** A14 self-application (TIRO chicken/egg; bj5 partial; gq1 none); A15 §28 trailers + §5.10 signoff + §5.11 paste archival + §19.6 attestation honesty; A16 `[from:]` author tags + §11 step 1.5 renewal cron; A17 cite-comments; A18 authorship attribution IMMUTABLE (TIRO frontmatter `author: Denson Smith`); A19 source-ticket closure (3 tickets close on ship); A20 pre-branch + worktree + out-of-scope hard-locks.

**DAEDALUS sub-decisions:** A5 / A8 / A11 / A13. User-tier leans documented in directive; each is DAEDALUS discretion UNLESS exceeding it (e.g., A8 spike reveals a new bw 0.14.0 substitution-tracking primitive that changes the design space) — then surface as PRINCIPAL-gate per §25.

**Cite-comment discipline per A17:** cross-refs between new `substrate/CAPTAIN_TIRO.md` + new operating-disciplines.md §31 (gq1) + extended `substrate/skills/check-substrate-updates/` (bj5) + the 4 cross-ref additions per A6 must resolve via cite at every read-site. Same pattern as Arcs 26-37 cite-comments.

**CATO is MANDATORY** for this arc (substrate canon + new role file + new canon section + tool extension; wording precision matters; first arc forward of the Arc 37 bb12806 trailer regression + spec-audit-iteration cadence — extra craft scrutiny justified).

**Authorship attribution is IMMUTABLE per CLAUDE.md** for file frontmatter. **New role file `substrate/CAPTAIN_TIRO.md` MUST carry `author: Denson Smith` frontmatter** per Arc 27 stoa--uly convention. Verify pre-commit; ZENO mechanical-checks in Phase 3. **Co-Authored-By trailers per §28 apply to all ADA + DAEDALUS commits** in arc-38/build.

**Self-application per A14:**
- C1 TIRO chicken/egg: team uses `bw list --all` directly per cookbook §12.1 + spec §4.6 (same pattern as the spec-audit cadence). Friction observed during arc = empirical-anchor reinforcement; surface as audit-feedback.
- C2 bj5 partial: if ADA runs the extended check-substrate-updates against the-stoa's own user-tier substrate during Phase 3, that's first-worked-example self-application. Opportunistic, not required.
- C3 gq1: no self-application (design-principles canon).

**Phase 4 close handshake per §5.10 + A15 + A19:**
- Verify cleanup executed (arc-38/build local + remote deleted; worktree removed; PR merged; main fast-forwarded).
- Verify §28 Co-Authored-By trailers preserved on squash-merge commit. **DO NOT use `gh pr merge --body` with custom body that overrides GitHub trailer-concatenation per stoa--6wp regression.** Either omit `--body` or include trailers in HEREDOC explicitly.
- Verify TIRO role file frontmatter `author: Denson Smith`.
- Verify install.sh dry-run lists CAPTAIN_TIRO at the canonical agent list.
- Verify bj5 check.sh dry-run runs cleanly against the-stoa's own user-tier substrate (smoke check; doesn't have to surface drift).
- Verify gq1 §31 cross-refs resolve.
- Close 3 source tickets (stoa--ojz + stoa--bj5 + stoa--gq1) per A19 with cross-refs + audit comments per candidate.
- Tag `[for: user-tier-polybius]` on stoa--ojz inviting QA pass.
- Paste archival per §5.11 to substrate/arcs/arc-38/pastes/ via git mv (preserves git log --follow continuity).

**Self-referential note:** Arc 38 is the FIRST forward arc after the SPEC_AUDIT R1-R4 iteration cadence converged. Per stoa--bbi (the N=4 substrate-principle-refinement accretion ticket filed companion to this dispatch), the iteration confirmed "structural fixes narrow drift surface but require propagation discipline + iteration to fully close; the residual converges on a fixed-point that is operationally acceptable rather than structurally zero." Arc 38 ships TIRO — itself a structural-fix instance of the same family — so Arc 38's empirical observations will accrete additional N-evidence on the refined principle. Pay attention to propagation gaps during the gauntlet; the next structural-fix arc benefits from your observations.

Check beadwork (stoa-- prefix) — start with: stoa--ojz (the work-unit; substrate/arcs/arc-38-build-directive.md is its load-bearing artifact, on disk at dispatch authoring time, will commit as part of arc-38/build feature branch).

If compaction or /clear erases your role, re-read this paste from HUMAN_paste-pliny-arc-38-instruction.md in the project root.
