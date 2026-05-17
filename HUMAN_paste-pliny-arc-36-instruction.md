Read .claude/MAJOR_PLINY.md and assume the orchestrator role for the-stoa.

Your immediate intent for this session: Build Arc 36 v2 per the build directive at substrate/arcs/arc-36-build-directive.md. Bundled coordination-hygiene canon — **Part 1: `[from: <self>]` author-tag canon (stoa--e39)** + **Part 2: cron-expiry handling (stoa--cgn)** — shipping together per original arc-22 bundling. Parent EPIC stoa--jru closes on ship. v1 of this directive (commit `28155f7`) had Part-1-only scope-recut; v2 reverses that under PRINCIPAL no-deferrals stance.

**PRECONDITION:** Arc 35 (stoa--kjo) is CLOSED + Pass 1 substrate cleanup landed at `594662e`. the-stoa main at `594662e` (or wherever the v2 dispatch commit lands on top). Local main = origin/main + no orphan arc-build branches verified by user-tier POLYBIUS at v2 dispatch authoring.

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

**Worktree convention per MAJOR_PLINY.md §5.9.4 (directive A17):** create arc-36/build in separate worktree: `git worktree add .claude/worktrees/arc-36-build arc-36/build`. Main worktree stays on main.

**Read first (in order):**

1. **`substrate/arcs/arc-36-build-directive.md`** — load-bearing spec for BOTH Parts. A1-A17 LOCKED. A5/A6/A7/A10 are DAEDALUS sub-decisions.
2. **`bw show stoa--e39`** (Part 1) + **`bw show stoa--cgn`** (Part 2) + **`bw show stoa--jru`** (parent EPIC closing on ship). All three carry context.
3. **`git show arcs/22-coordination-hygiene:substrate/arcs/arc-22-build-directive.md`** — architectural reference for both Parts. A2/A2.5/A3/A4 (Part 1) + A4/A5/A6 (Part 2) LOCKED decisions inherited.
4. **`HUMAN_paste-polybius-arc-36-instruction.md`** in the project root — POLYBIUS's activation paste; same content frame.
5. **`substrate/operating-disciplines.md` §7** entire section (Part 1 insertion surface — A5/A4) + **§11** (Part 2 insertion surface for Option-3-path — A10) + **§28** (Arc 35 Co-Authored-By trailer canon; ADA + DAEDALUS commits must apply).
6. **`substrate/MAJOR_POLYBIUS.md` §7** (Part 1 cross-ref target — A5) + **§18** (user-tier housekeeping; reference).
7. **`substrate/MAJOR_PLINY.md` §5.9 + §5.9.4 + §5.10 + §5.11 + §5.12** — pre-branch hygiene + worktree + signoff-accuracy + paste archival + seat-identity dispatch-brief; all self-applied per A11/A17.
8. **`substrate/templates/polling-cron-prompt-template.md`** — Part 1 STEP 1.5 + Part 2 STEP 7 insertion surface.
9. **`substrate/operating-disciplines.md` §27** (Arc 33 mechanical/agent split — precedent for "prose canon now; mechanical enforcement future if recurs"; A14 cite).
10. **`the-stoa/SPECIFICATION.md` §10.1 + §4.5 + §13** — generational-lineage architecture + the make-the-team-meet-the-spec workplan that this arc is Pass 2 of.

Operating mode for this dispatch: AUTONOMOUS. Run all four phases heads-down. Use stoa--jru for status updates (parent EPIC; both child tickets close alongside per A15). Surface to PRINCIPAL ONCE at end-of-arc with final clean-PASS verdict.

Coordination: the-stoa PROJECT-TIER POLYBIUS is your radio-check peer (paste at HUMAN_paste-polybius-arc-36-instruction.md). User-tier POLYBIUS dispatched + will do QA pass at arc close. Bidirectional radio-check pattern per substrate/operating-disciplines.md §7. **Per A11 self-application, POLYBIUS's own coordination heartbeats on stoa--jru MUST carry `[from: polybius-the-stoa]` per the convention being shipped.**

The architectural decisions A1-A17 are LOCKED in the directive. DAEDALUS treats this directive as primary input; arc-22 Part 1 + Part 2 architecture is inherited. Locked decisions encode:

**Part 1:** A2 `[from:]` convention + bidirectional `[for:]` promotion; A2.5 POLYBIUS-on-POLYBIUS scope; A3 slug normalization; A4 parsing teaching in op-disc.

**Part 2:** A7 spike-first decision matrix (CronList field inspection determines Option 1 vs Option 3 implementation locus); A8 1-day renewal buffer rule (correct under any docs reading); A9 renewal failure-mode acceptance (peer-side radio-check recovers; no watchdog ships).

**Universal:** A11 self-application both Parts; A12 cite-comments; A13 authorship attribution unchanged; A14 out-of-scope hard-locked; A15 source-ticket closure (3 tickets — e39 + cgn + jru); A16 §15 N=1 honesty; A17 pre-branch + worktree + signoff self-applied.

**DAEDALUS sub-decisions:**
- **A5 Part 1 insertion locus:** (α) new §7.7 vs (β) extend §7.1 with author-tag subsection. §7.4 wording update inline either way (`[for:]` cross-tier-upward-only → bidirectional). User-tier leans (α). Also: MAJOR_POLYBIUS.md §7 cross-ref shape — body cite vs new subsection. User-tier leans body cite.
- **A6 Part 1 polling-cron-prompt STEP 1.5:** mandatory (parser mechanically executes) vs optional (prose canon sufficient). User-tier leans STEP 1.5 mandatory — the e39 failure was precisely from common-sense reading without mechanical author-attribution.
- **A7 Part 2 spike:** EXECUTE BEFORE Part 2 design.md finalized. Steps: CronCreate throwaway → CronList → inspect fields (start_time/age/created_at vs expires_at/next_fire/valid_until vs neither; CronUpdate exists?) → web-search docs for confirmed expiry duration → CronDelete throwaway → record in design.md + bw comment on stoa--jru.
- **A10 Part 2 implementation locus:** gated by A7 spike result per the decision matrix. Backward/forward fields → Option 1 (STEP 7 in polling-cron-prompt-template.md). Neither → Option 3 (step 1.5 in op-disc §11). CronUpdate exists → surface to user-tier POLYBIUS for adjudication.

If any pick surfaces as needing PRINCIPAL judgment rather than DAEDALUS discretion, treat as PRINCIPAL-gate per §25 — halt + escalate immediately rather than proceed-then-flag.

**Cite-comment discipline per A12:** cross-refs between new §7.7 + §7.4 bidirectional update + §7.1 update + §11 step 1.5 (if Option 3) + MAJOR_POLYBIUS.md §7 cross-ref + polling-cron-prompt-template.md STEP 1.5 + STEP 7 must resolve via cite at every read-site.

**CATO is MANDATORY** for this arc (substrate canon work + new top-level section + template extensions + behavioral protocol changes both Parts; wording precision matters; bundling means more surface area than single-Part arcs).

**Authorship attribution for FILE FRONTMATTER is IMMUTABLE per CLAUDE.md per A13.** Arc 36 changes only operating-disciplines.md + MAJOR_POLYBIUS.md + template prose; no fresh author-like field exposure expected. **Co-Authored-By trailers per §28 apply to all ADA + DAEDALUS commits inside arc-36/build** — Arc 36 v2 is the first forward-arc inheriting §28 as established canon (Arc 35 was the self-applying ship arc).

**Self-application per A11 (LOAD-BEARING):**
- **Part 1:** POLYBIUS's heartbeats carry `[from: polybius-the-stoa]` per convention being shipped. If POLYBIUS's first heartbeat forgets the tag, surface as substance disagreement.
- **Part 2:** POLYBIUS's polling cron applies the Part 2 renewal logic (whichever option A10 picks). For a short arc, the renewal check won't fire during the arc itself, but the cron IS-able to fire it.

**Phase 4 close handshake per §5.10 + A15:**
- Verify cleanup executed (arc-36/build local + remote deleted; worktree removed; PR merged; main fast-forwarded).
- Verify ADA/DAEDALUS commits carry Co-Authored-By trailers per §28.
- Verify Part 1 self-application (POLYBIUS heartbeats carry `[from:]` tags).
- Verify Part 2 self-application (POLYBIUS cron applies the shipped renewal logic).
- Close stoa--e39 (Part 1) + stoa--cgn (Part 2) + stoa--jru (parent EPIC) with cross-refs to merge commit + audit comments (noting Part 2's v2 reversal of v1 deferral; original arc-22 bundling shipped together as PRINCIPAL intended).
- Tag `[for: user-tier-polybius]` on stoa--jru inviting QA pass.

**Self-referential note:** Arc 36 v2 ships both coordination-hygiene fixes that surfaced 2026-05-04 + sat HITL-paused 13 days (rescued by Arc 34 / C4 HITL-paused queue sweep on 2026-05-17). Per the-stoa SPECIFICATION.md §10.1 generational-lineage architecture, this arc creates the successor-generation team — the post-Arc-36 team has structurally-better coordination than the pre-Arc-36 team because the canon delta encodes lessons from the original arc-21 §5.4 review handoff stall. Same substrate-shaping shape as Arcs 24-35.

Check beadwork (stoa-- prefix) — start with: stoa--jru (parent EPIC; substrate/arcs/arc-36-build-directive.md is its load-bearing artifact, on disk at v2 dispatch authoring time, will commit as part of arc-36/build feature branch).

If compaction or /clear erases your role, re-read this paste from HUMAN_paste-pliny-arc-36-instruction.md in the project root.
