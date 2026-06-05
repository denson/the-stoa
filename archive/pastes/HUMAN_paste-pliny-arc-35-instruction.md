Read .claude/MAJOR_PLINY.md and assume the orchestrator role for the-stoa.

Your immediate intent for this session: Build Arc 35 per the build directive at substrate/arcs/arc-35-build-directive.md. Substantive substrate canon arc: **per-CAPTAIN git seat identity via Co-Authored-By trailer** (stoa--kjo, P3). PRINCIPAL pre-dispatch adjudicated the load-bearing fix-shape question (Option β chosen over the ticket's original Option A) on 2026-05-17; directive A2 + A3 + A4 carry the PRINCIPAL picks.

**PRECONDITION:** Arc 34 (stoa--y14) is CLOSED. the-stoa main at `244c1c3`. Local main = origin/main + no orphan arc-build branches verified by user-tier POLYBIUS at dispatch authoring.

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
inherit local-ahead commits into the arc branch (bundled-squash pattern surfaced
on 2026-05-17 as stoa--3cs).

**Worktree convention per MAJOR_PLINY.md §5.9.4 (directive A14):** create arc-35/build in separate worktree: `git worktree add .claude/worktrees/arc-35-build arc-35/build`. Main worktree stays on main.

**Read first (in order):**

1. **`substrate/arcs/arc-35-build-directive.md`** — load-bearing spec. A1-A16 LOCKED architectural decisions. A2/A3/A4 are PRINCIPAL-decided (not DAEDALUS discretion). A5/A6/A7/A8 are DAEDALUS sub-decisions.
2. **`bw show stoa--kjo`** — work-unit ticket. Original proposal was Option A (full Author override); PRINCIPAL pre-dispatch adjudicated to Option β (Co-Authored-By trailer). Directive overrides ticket on fix-shape. DAEDALUS treats this directive as primary input alongside ticket body for context.
3. **`~/.claude/CLAUDE.md`** authorship-attribution section — the absolute "never override Author:" rule that β preserves. A4 lands a cross-ref edit here (NOT a rule weakening — a compliance-with-spirit acknowledgment that substrate's Co-Authored-By trailer is the seat-identity signal).
4. **`HUMAN_paste-polybius-arc-35-instruction.md`** in the project root — POLYBIUS's activation paste; same content frame.
5. **`substrate/operating-disciplines.md` §19.6** (attestation-confabulation; sister-discipline to the read-discipline pairing in A8) + **§25** (PRINCIPAL-gate; A5-A8 sub-decisions escalate here if exceeding DAEDALUS discretion) + **§27** (Arc 33 mechanical/agent split — most recent new top-level section precedent; A6 follows same insertion pattern).
6. **`substrate/MAJOR_PLINY.md` §5.10** (signoff-accuracy; self-applied per A15) + **§5.11** (Arc 34 archival — most recent canon section shape) + **§5.9 / §5.9.4** (pre-branch + worktree; self-applied per A14).
7. **`substrate/MAJOR_POLYBIUS.md` §18** (Arc 34 housekeeping discipline — the section that explicitly exempts POLYBIUS housekeeping commits from per-CAPTAIN tagging per directive A3).
8. **`substrate/CAPTAIN_ADA.md`** authorship-discipline section (currently file-frontmatter discipline only at line ~94; A6 extends with git-trailer discipline).
9. **`substrate/CLAUDE.md`** authorship section (project-tier rule; cross-ref to global; A4-adjacent edit may apply here too if DAEDALUS deems it warranted — surface in design.md).
10. **`substrate/arcs/arc-34-build-directive.md`** — Arc 34 / C2 self-application precedent (paste-archival landed in same gauntlet commit as the canon section); A9 self-application pattern matches.

Operating mode for this dispatch: AUTONOMOUS. Run all four phases heads-down. Use stoa--kjo for status updates. Surface to PRINCIPAL ONCE at end-of-arc with final clean-PASS verdict.

Coordination: the-stoa PROJECT-TIER POLYBIUS is your radio-check peer (paste at HUMAN_paste-polybius-arc-35-instruction.md). User-tier POLYBIUS dispatched + will do QA pass at arc close. Bidirectional radio-check pattern per substrate/operating-disciplines.md §7.

The architectural decisions A1-A16 are LOCKED in the directive. DAEDALUS treats this directive as primary input alongside the stoa--kjo ticket body (which carries the empirical anchor but predates the PRINCIPAL-pick reframing). Locked decisions encode: one-arc one-gauntlet (A1); fix-shape β PRINCIPAL-decided (A2); scope CAPTAINs-only PRINCIPAL-decided (A3); global CLAUDE.md cross-ref fold-in PRINCIPAL-decided (A4); trailer format DAEDALUS pick (A5); canon insertion loci DAEDALUS pick (A6); implementation mechanism DAEDALUS pick (A7); read-discipline pairing DAEDALUS pick (A8); self-application required (A9); cite-comments (A10); file-frontmatter authorship unchanged (A11); out-of-scope hard-locked (A12); §15 N=1 per the empirical anchor (A13); pre-branch + worktree self-applied (A14); signoff-accuracy + attestation-honesty self-applied (A15); source-ticket closure (A16).

**DAEDALUS sub-decisions:**
- **A5 trailer format:** exact name format (`CAPTAIN_ADA_the-stoa` vs `CAPTAIN_ADA_the_stoa` vs other) + exact email format. User-tier POLYBIUS leans underscore-separator with `<project>.local` email.
- **A6 insertion loci:** operating-disciplines.md likely new §28; MAJOR_PLINY.md likely new §5.12; CAPTAIN_ADA.md extends existing authorship-discipline subsection.
- **A7 implementation:** (i) manual trailer in commit message vs (ii) shell helper at substrate/scripts/git-coauthor.sh. User-tier POLYBIUS leans (i) — cheapest, reversible, no install.sh change.
- **A8 read-discipline pairing:** (a) subsection inside §28 vs (b) standalone §29 vs (c) defer to follow-up arc. User-tier POLYBIUS leans (a) — same-arc pairing makes rationale self-contained.

If any pick surfaces as needing PRINCIPAL judgment rather than DAEDALUS discretion, treat as PRINCIPAL-gate per §25 — halt + escalate immediately rather than proceed-then-flag.

**Cite-comment discipline per A10:** cross-refs between new operating-disciplines.md §28 + global ~/.claude/CLAUDE.md + MAJOR_PLINY.md dispatch-section update + CAPTAIN_ADA.md update must resolve via cite at every read-site. Same pattern as Arc 26 / 28 / 29 / 30 / 31 / 32 / 33 / 34 cite-comments.

**CATO is MANDATORY** for this arc (substrate canon work + new top-level operating-disciplines.md section + interaction with global CLAUDE.md rule; wording precision matters; PRINCIPAL adjudicated fix-shape so getting the framing right is load-bearing).

**Authorship attribution for FILE FRONTMATTER is IMMUTABLE per substrate/CLAUDE.md per A11.** Arc 35 changes ONLY git commit metadata convention; file-frontmatter `author:` fields continue to name Denson Smith. SKILL.md files, package.json, etc., are NOT touched. CAPTAIN_ADA.md line 94 discipline ("any file with an author field... names the PRINCIPAL... never anyone else") stands.

**Self-application per A9:** Arc 35's OWN gauntlet build commits (CAPTAIN_ADA inside `.claude/worktrees/arc-35-build/`) MUST carry the Co-Authored-By trailer per the convention being shipped. PLINY signoff verifies this before PR-merging. If ADA's first commit forgets the trailer, surface as substance disagreement and have ADA rev2-rewrite with proper trailers (do NOT proceed-then-fix).

**Phase 4 close handshake per §5.10 + A16:** verify cleanup actually executed; verify global ~/.claude/CLAUDE.md edit landed + pushed (user-tier action — surface to user-tier POLYBIUS for confirmation if PLINY cannot directly verify the global file); verify Arc 35's own gauntlet commits carry the trailer (self-application sanity check); close stoa--kjo with audit comment per A16 (note Option β was PRINCIPAL-reframed from original Option A; cite operating-disciplines.md §28 + the global CLAUDE.md cross-ref); tag `[for: user-tier POLYBIUS]` on stoa--kjo inviting QA pass.

**Self-referential note:** Arc 35 ships the convention that future arcs will be evaluated against — including the empirical-anchor pattern Arc 35 itself addresses. After Arc 35 ships, a future ARGUS reading the squash-merge commit body sees `Co-Authored-By: CAPTAIN_ADA_the-stoa <captain-ada@the-stoa.local>` and knows the commit was authored by a CAPTAIN session, not by PRINCIPAL hand-edit. The stoa--kjo / ariadne--xft.4 misattribution shape becomes structurally preventable. Same substrate-shaping shape as Arcs 24-34.

Check beadwork (stoa-- prefix) — start with: stoa--kjo (the work-unit; substrate/arcs/arc-35-build-directive.md is its load-bearing artifact, on disk at dispatch authoring time, will commit as part of arc-35/build feature branch).

If compaction or /clear erases your role, re-read this paste from HUMAN_paste-pliny-arc-35-instruction.md in the project root.
