Read .claude/MAJOR_PLINY.md and assume the orchestrator role for the-stoa.

Your immediate intent for this session: Build Arc 36 per the build directive at substrate/arcs/arc-36-build-directive.md. Substrate canon arc (scope-recut from arc-22): **explicit `[from: <self>]` author-tag canon for POLYBIUS-on-POLYBIUS bw coordination** (stoa--e39, P2). User-tier POLYBIUS audit-against-current-substrate (2026-05-17) surfaced that arc-22 / stoa--jru bundled 2 failure modes and 10 arcs have shipped without either recurring; PRINCIPAL adjudicated scope-recut to Part 1 only.

**PRECONDITION:** Arc 35 (stoa--kjo) is CLOSED. the-stoa main at `6414397`. Local main = origin/main + no orphan arc-build branches verified by user-tier POLYBIUS at dispatch authoring.

Cron hygiene FIRST (before any substantive work): Run CronList; if any cron is present, CronDelete it. Surface-and-wait per MAJOR_PLINY.md §6.2 (no cron) is the default for PLINY; defense-in-depth.

Pre-branch hygiene per MAJOR_PLINY.md §5.9: before creating arc-N/build, run two checks.

Check 1 (no other arc-build branch in flight):
  git branch | grep -E '^\s*arc-[0-9]+/build$'    # must be empty

Check 2 (local main = origin/main):
  git fetch origin main
  git log --oneline main..origin/main             # must be empty
  git log --oneline origin/main..main             # must be empty

If either check fails, surface to user-tier POLYBIUS (or PRINCIPAL via [for: PRINCIPAL]
tag when user-tier unavailable) with the specific state observed. Do NOT silently
inherit local-ahead commits into the arc branch.

**Worktree convention per MAJOR_PLINY.md §5.9.4 (directive A13):** create arc-36/build in separate worktree: `git worktree add .claude/worktrees/arc-36-build arc-36/build`. Main worktree stays on main.

**Read first (in order):**

1. **`substrate/arcs/arc-36-build-directive.md`** — load-bearing spec. A1-A14 LOCKED architectural decisions. A5/A6/A7 are DAEDALUS sub-decisions.
2. **`bw show stoa--e39`** — work-unit ticket. Carries 2026-05-04 empirical anchor (POLYBIUS_the_stoa misread user-tier POLYBIUS's `[for:]` comment as own self-heartbeat; ~25-min stall) + the original "what needs to change in substrate" enumeration.
3. **`bw show stoa--jru`** — parent EPIC being closed as scope-recut per A14. Carries the bundling history (Part 1 + Part 2 originally bundled; Part 2 deferred via stoa--cgn).
4. **`bw show stoa--cgn`** — sibling being deferred with gating criteria per A11. Reference for what's NOT in Arc 36 scope.
5. **`git show arcs/22-coordination-hygiene:substrate/arcs/arc-22-build-directive.md`** Part 1 — architectural reference for A2/A2.5/A3/A4. These locks are inherited from arc-22's Part 1; integration surface refreshed per current substrate state.
6. **`HUMAN_paste-polybius-arc-36-instruction.md`** in the project root — POLYBIUS's activation paste; same content frame.
7. **`substrate/operating-disciplines.md` §7** entire section (current §7.1-§7.6 — universal-team POLYBIUS-pair coordination canon; A5/A4 insertion surface).
8. **`substrate/MAJOR_POLYBIUS.md` §7** — POLYBIUS-tier specific bw-handling; A6 cross-ref target.
9. **`substrate/templates/polling-cron-prompt-template.md`** — current 161 lines; A7 insertion surface for STEP 1.5 author-attribution.
10. **`substrate/operating-disciplines.md` §27** (Arc 33 mechanical/agent split — precedent for "ship prose canon now; defer mechanical enforcement to future arc if non-compliance recurs"; A11 hard-lock cites this).
11. **`substrate/operating-disciplines.md` §28** + **`substrate/arcs/arc-35-build-directive.md`** — Arc 35 most recent precedent (new top-level §28 section; self-application via Co-Authored-By trailers verified empirically); A5 (α) + A8 self-application follow same shape.

Operating mode for this dispatch: AUTONOMOUS. Run all four phases heads-down. Use stoa--e39 for status updates. Surface to PRINCIPAL ONCE at end-of-arc with final clean-PASS verdict.

Coordination: the-stoa PROJECT-TIER POLYBIUS is your radio-check peer (paste at HUMAN_paste-polybius-arc-36-instruction.md). User-tier POLYBIUS dispatched + will do QA pass at arc close. Bidirectional radio-check pattern per substrate/operating-disciplines.md §7.

The architectural decisions A1-A14 are LOCKED in the directive. DAEDALUS treats this directive as primary input; arc-22 Part 1 directive (on `arcs/22-coordination-hygiene` branch) is architectural reference. Locked decisions encode: one-arc one-gauntlet (A1); `[from:]` convention + bidirectional `[for:]` (A2); POLYBIUS-on-POLYBIUS-only scope (A2.5); slug normalization (A3); universal-team-layer parsing teaching (A4); insertion locus DAEDALUS (A5); MAJOR_POLYBIUS.md §7 cross-ref DAEDALUS (A6); polling-cron-prompt template STEP 1.5 DAEDALUS (A7); self-application required (A8); cite-comments (A9); file-frontmatter + Author: + Co-Authored-By trailers unchanged (A10); out-of-scope hard-locked (A11); §15 N=1 honesty per empirical anchor + informal-adoption signal (A12); pre-branch + worktree self-applied (A13); signoff-accuracy + attestation-honesty + source-ticket closure with stoa--jru scope-recut close + stoa--cgn gating-criteria comment (A14).

**DAEDALUS sub-decisions:**
- **A5 insertion locus:** (α) new §7.7 vs (β) extend §7.1 with author-tag subsection. §7.4 wording update inline either way (`[for:]` cross-tier-upward-only → bidirectional). User-tier POLYBIUS leans (α) — clean separation; matches Arc 33 §27 / Arc 35 §28 new-section precedent.
- **A6 MAJOR_POLYBIUS.md §7 cross-ref shape:** body paragraph cite-comment vs new §7.5 subsection. User-tier POLYBIUS leans body paragraph cite-comment.
- **A7 polling-cron-prompt template STEP 1.5:** mandatory (parser mechanically executes the discipline) vs optional (prose canon in §7.7 sufficient). User-tier POLYBIUS leans STEP 1.5 mandatory — the parser ran into the e39 failure mode precisely because it was doing common-sense reading without mechanical author-attribution.

If any pick surfaces as needing PRINCIPAL judgment rather than DAEDALUS discretion, treat as PRINCIPAL-gate per §25 — halt + escalate immediately rather than proceed-then-flag.

**Cite-comment discipline per A9:** cross-refs between new §7.7 + §7.4 bidirectional update + §7.1 update + MAJOR_POLYBIUS.md §7 cross-ref + polling-cron-prompt-template STEP 1.5 must resolve via cite at every read-site. Same pattern as Arcs 26-35 cite-comments.

**CATO is MANDATORY** for this arc (substrate canon work + new top-level section + template edit; wording precision matters; scope-recut from arc-22 means the original directive's architecture survives but integration surface has shifted).

**Authorship attribution is IMMUTABLE per substrate/CLAUDE.md** for file frontmatter. Arc 36 changes only operating-disciplines.md + MAJOR_POLYBIUS.md + template prose; no fresh author-like field exposure expected. **Co-Authored-By trailers per §28 (Arc 35 canon) apply to all ADA + DAEDALUS commits inside arc-36/build** — first arc to apply §28 from the start (Arc 35 was the self-applying ship arc; Arc 36 is the first forward-arc that inherits §28 as canon).

**Self-application per A8:** Arc 36's OWN POLYBIUS coordination heartbeats on stoa--e39 (project-tier POLYBIUS_the_stoa's heartbeats during the arc) MUST carry `[from: polybius-the-stoa]` per the convention being shipped. Cross-tier heartbeats addressed to user-tier POLYBIUS use `[for: user-tier-polybius] [from: polybius-the-stoa]`. PLINY signoff verifies this before PR-merging. If POLYBIUS_the_stoa's first heartbeat forgets the tag, surface as substance disagreement and have POLYBIUS rewrite-with-correction — do NOT let an un-self-applied convention ship.

**Phase 4 close handshake per §5.10 + A14:** verify cleanup actually executed; verify ADA/DAEDALUS commits carry Co-Authored-By trailers per §28; verify Arc 36's own POLYBIUS heartbeats carry `[from:]` per the shipped convention (self-application sanity check); close stoa--e39 (work-unit) with cross-ref to merge commit; close stoa--jru (parent EPIC) with scope-recut audit note; update stoa--cgn body via comment with deferral gating criteria (do NOT close — keep open as gated future work); tag `[for: user-tier-polybius]` on stoa--e39 inviting QA pass.

**Self-referential note:** Arc 36 ships the convention that addresses the empirical failure that surfaced in arc-21 (2026-05-04). The substrate has been informally using the `[radio-check ...]` half + `[for: ...]` half across Arcs 32-35; Arc 36 completes the pair with `[from: ...]` + universal parsing canon. After Arc 36 ships, future bw-timeline parsing failures of the e39 shape become structurally preventable. Same substrate-shaping shape as Arcs 24-35.

Check beadwork (stoa-- prefix) — start with: stoa--e39 (the work-unit; substrate/arcs/arc-36-build-directive.md is its load-bearing artifact, on disk at dispatch authoring time, will commit as part of arc-36/build feature branch).

If compaction or /clear erases your role, re-read this paste from HUMAN_paste-pliny-arc-36-instruction.md in the project root.
