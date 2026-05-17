Read .claude/MAJOR_PLINY.md and assume the orchestrator role for the-stoa.

Your immediate intent for this session: Build Arc 29 per the build directive at substrate/arcs/arc-29-build-directive.md. Foundational substrate arc: encode the **base-vs-custom agent convention** as substrate canon + scope substrate tools (install.sh + check.sh + apply.sh) to respect the convention. PRINCIPAL declared the architectural model on 2026-05-17. Work-unit ticket: **stoa--ads** (P1; 6 deliverables D1-D6).

**PRECONDITION:** Arc 28 (stoa--s6n) is CLOSED. the-stoa main at efffb8b. Local main = origin/main verified by user-tier POLYBIUS at dispatch authoring.

**Cron hygiene FIRST (before any substantive work):** this session is fresh. Run `CronList`; if any cron is present, CronDelete it. PLINY typically uses surface-and-wait per MAJOR_PLINY.md §6.2 (no cron); defense-in-depth: don't trust fresh context.

**Pre-branch hygiene per directive A9:** before creating arc-29/build, verify local main = origin/main:

```
git fetch origin main
git log --oneline main..origin/main      # should be empty
git log --oneline origin/main..main      # should be empty
```

If either log shows commits, surface — don't silently inherit local-ahead commits into the arc branch (bundled-squash pattern surfaced today as stoa--3cs).

**Read first (in order):**

1. **`substrate/arcs/arc-29-build-directive.md`** — load-bearing spec. A1-A9 LOCKED architectural decisions. Treat as primary input prose alongside the ticket body.
2. **`bw show stoa--ads`** — work-unit ticket. Body carries D1-D6 deliverables + acceptance probes + out-of-scope hard-locks + §15 N=1 caveat.
3. **`HUMAN_paste-polybius-arc-29-instruction.md`** in the project root — POLYBIUS's activation paste; same content frame.
4. **`substrate/install.sh`** — current deploy logic. D3 modifies every glob/path point that touches agents/skills/templates directories with base-vs-custom scoping. Carefully identify all the scoping sites.
5. **`substrate/skills/check-substrate-updates/check.sh`** — current scan logic. D4 modifies similarly.
6. **`substrate/skills/check-substrate-updates/apply.sh`** — current apply logic. D5 modifies similarly.
7. **`substrate/MAJOR_POLYBIUS.md`** + **`substrate/operating-disciplines.md`** — current section structures; D1 adds new sections for base-vs-custom architecture. DAEDALUS picks insertion locus.

Operating mode for this dispatch: AUTONOMOUS. Run all four phases heads-down (Phase 1 DAEDALUS + ARGUS — LIKELY ARGUS revisions given architecture-sensitivity; Phase 2 ADA build on feature branch arc-29/build; Phase 3 VERA + CATO + ZENO parallel verification; Phase 4 smoke + PR + merge + close). Use stoa--ads for status updates. Surface to PRINCIPAL ONCE at end-of-arc with the final clean-PASS verdict.

Coordination: the-stoa PROJECT-TIER POLYBIUS is your radio-check peer (activated in a separate Claude Code session, paste at HUMAN_paste-polybius-arc-29-instruction.md). User-tier POLYBIUS dispatched + will do QA pass at arc close. Bidirectional radio-check pattern per substrate/operating-disciplines.md §7. On dispatch, post init handshake on stoa--ads confirming directive + ticket read + pre-branch hygiene verified.

The architectural decisions A1-A9 are LOCKED in the directive. DAEDALUS treats stoa--ads's body as primary input alongside the directive. Locked decisions encode: one-arc one-gauntlet (A1); architectural model with PRINCIPAL's exact phrasing (A2); convention candidates with load-bearing Claude Code auto-discovery empirical question (A3 — subdirectory recommended; DAEDALUS verifies + picks final); files in scope (A4); cite-comment discipline at every scoping site (A5); authorship immutable (A6); out-of-scope hard-locked (A7); §15 N=1 honesty (A8); pre-branch hygiene (A9).

**Load-bearing empirical task in DAEDALUS Phase 1 (per A3):** verify Claude Code's agent auto-discovery actually loads agents from `.claude/agents/custom/CAPTAIN_*.md` subdirectory path. Drop a stub; invoke by name; verify activation. If YES → use subdirectory convention. If NO → fall back to filename suffix `_custom`. Document empirical verification in design.md. This is the load-bearing pick for D2.

**Cite-comment discipline per A5:** wherever D3/D4/D5 scope a path/glob to "base only," place a cite-comment at the modification site referencing the new base-vs-custom canon section. Same pattern as apply_substitutions cite-comment + Arc 26 parse_skill_names_from_install cite-comment + Arc 28 bw-output-parse cite-comments. CATO will verify in cold-read.

**CATO is MANDATORY** for this arc (not optional). Substrate canon work; wording precision matters; future POLYBIUSes read this for life-of-the-substrate.

**Forward awareness:** stoa--32b.1 (PRINCIPAL-gate discipline) is FILED but NOT YET BUILT. If any design clause this arc surfaces names "PRINCIPAL-discretion," treat the NEW way (block + escalate immediately, do NOT proceed-then-flag) per PRINCIPAL's 2026-05-16 declaration. Locked decisions A1-A9 minimize the chance of new PRINCIPAL-discretion clauses surfacing; if one does, escalate immediately.

Authorship attribution is IMMUTABLE per substrate/CLAUDE.md: all edits credit Denson Smith. Arc 29 edits existing files (no fresh author-like field exposure expected). If DAEDALUS surfaces a new skill/template, frontmatter must carry `author: Denson Smith`.

**Phase 4 close handshake:** in addition to standard closure, tag `[for: user-tier POLYBIUS]` comment on stoa--ads inviting QA pass per PRINCIPAL pattern.

**Self-referential note:** Arc 29 encodes the architectural model that governs every future custom-agent work. The convention you ship determines where customizations live across every workspace forever. Same substrate-shaping shape as Arcs 24/25/26/27/28.

Check beadwork (stoa-- prefix) — start with: stoa--ads (the work-unit; substrate/arcs/arc-29-build-directive.md is its load-bearing artifact, on disk at dispatch authoring time, will commit as part of arc-29/build feature branch).

If compaction or /clear erases your role, re-read this paste from HUMAN_paste-pliny-arc-29-instruction.md in the project root.
