Read .claude/MAJOR_PLINY.md and assume the orchestrator role for the-stoa.

Your immediate intent for this session: Build Arc 28 per the build directive at substrate/arcs/arc-28-build-directive.md. Four phases × one gauntlet × medium-scope substrate-canon work. Part B (B.1-B.4): adopt bw 0.13.0 features at substrate level — registry replaces consumer-workspaces.txt (check.sh migration); cross-repo issue resolution doc; attachments + recap as available primitives. Part C (C.1-C.2): encode bw-upgrade discipline — new operating-disciplines.md section (5-step process + 3 impact axes) + lightweight check-bw-release skill. Closes one ticket: **stoa--s6n** (P1; LOAD-BEARING — the work-unit ticket; body carries full technical scope across 7 deliverables).

**PRECONDITION:** Arc 27 (stoa--32b.3) is CLOSED. ariadne--c71 is CLOSED (Railway container bw 0.13.0 shipped at ariadne-core main b7f92e5 earlier today; the deployment-side empirical anchor). Both verified by user-tier POLYBIUS at dispatch authoring.

**Cron hygiene FIRST (before any substantive work):** this session is fresh. Run `CronList`; if any cron is present, CronDelete it. PLINY typically uses surface-and-wait per MAJOR_PLINY.md §6.2 (no cron); defense-in-depth: don't trust fresh context. Then proceed.

**Read first (in order):**

1. **`substrate/arcs/arc-28-build-directive.md`** — the load-bearing spec. A1-A8 LOCKED architectural decisions; phasing table; reads-list; VERA probes; smoke beats. Treat as primary input prose alongside the ticket body.
2. **`bw show stoa--s6n`** — work-unit ticket. Body carries Part B + Part C + 7 deliverables + acceptance probes + hard-locked out-of-scope.
3. **`bw show ariadne--c71`** (cross-tier read at ariadne-core-workspace) — empirical anchor for the bw-upgrade-discipline (deployment-side axis). C.1 cross-refs this work.
4. **`HUMAN_paste-polybius-arc-28-instruction.md`** in the project root — POLYBIUS's activation paste; same content frame.
5. **`substrate/skills/check-substrate-updates/`** — `SKILL.md` + `check.sh` + `apply.sh`. B.1 modifies check.sh's no-args sweep to replace consumer-workspaces.txt read with `bw registry list` parse. The cite-comment-at-read-site pattern (`apply_substitutions` in check.sh + Arc 26's `parse_skill_names_from_install`) is the model for the new bw-registry parse.
6. **`substrate/consumer-workspaces.txt`** — current registry (4 entries: ariadne-core-workspace, railway_stoa, sector-4, the-stoa). B.1 deprecates with comment header (A4: file kept for one release; removal is follow-up arc).
7. **`substrate/operating-disciplines.md`** — full read; current section count + numbering. C.1 new section locates at appropriate insertion point (DAEDALUS picks).
8. **`substrate/MAJOR_POLYBIUS.md`** — especially §7 (Communication / bw operations), §16 (POLYBIUS lifecycle / multi-artifact handoff). B.2 doc lands in §7 OR §12 (DAEDALUS picks); B.3 + B.4 doc lands in §16.
9. **`substrate/install.sh`** — `SKILL_NAMES` array. Deliverable 7 appends `check-bw-release`.

Operating mode for this dispatch: AUTONOMOUS. Run all four phases heads-down (Phase 1 DAEDALUS + ARGUS, Phase 2 ADA build on feature branch arc-28/build, Phase 3 VERA + CATO + ZENO parallel verification, Phase 4 smoke + PR + merge + close). Use stoa--s6n for status updates as you progress. Surface to PRINCIPAL ONCE at end-of-arc with the final clean-PASS verdict.

Coordination: the-stoa PROJECT-TIER POLYBIUS is your radio-check peer (activated in a separate Claude Code session at the same time as you, paste at HUMAN_paste-polybius-arc-28-instruction.md). User-tier POLYBIUS dispatched the arc + will do QA pass at arc end per PRINCIPAL's 2026-05-16 pattern. Bidirectional radio-check pattern applies per substrate/operating-disciplines.md §7. On dispatch, post init handshake on stoa--s6n confirming directive + ticket + ariadne--c71 cross-ref read + naming your polling cron id if you choose to set one. Heartbeat one-line state on stoa--s6n.

The architectural decisions A1-A8 are LOCKED in the directive. DAEDALUS treats stoa--s6n's body as primary input alongside the directive. Locked decisions encode: one-arc one-gauntlet (A1); Part B sub-deliverables with DAEDALUS-precision-scoping (A2); Part C sub-deliverables (A3); consumer-workspaces.txt deprecation lifecycle (A4); cite-comment discipline at bw-output-parse sites (A5); authorship immutable (A6); out-of-scope hard-locked (A7); §15 N=1 honesty for the discipline encoding (A8).

**Cite-comment discipline:** wherever new code reads bw output formats (B.1's check.sh registry parse; C.2's bw GitHub releases API query), place a cite-comment at the parse site. Same pattern as `apply_substitutions` + Arc 26's `parse_skill_names_from_install`. CATO will check this in cold-read.

**CATO is MANDATORY** for this arc (not optional). Wording-precision in substrate canon matters; future POLYBIUSes read this for life-of-the-substrate.

Authorship attribution is IMMUTABLE per substrate/CLAUDE.md: all edits credit Denson Smith. Arc 28 adds 2 new files: SKILL.md (frontmatter — include `author: Denson Smith` per stoa--uly convention) + check.sh (shell script; no frontmatter). Verify before commit.

**Phase 4 close handshake:** in addition to standard closure, tag `[for: user-tier POLYBIUS]` comment on stoa--s6n inviting QA pass per PRINCIPAL pattern.

**Self-referential note:** Arc 28 is the substrate-side companion to ariadne--c71. The discipline being encoded (C) generalizes from BOTH pieces of work. Same self-referential dynamic as Arcs 24/25/27.

Check beadwork (stoa-- prefix) — start with: stoa--s6n (the work-unit; substrate/arcs/arc-28-build-directive.md is its load-bearing artifact, on disk at dispatch authoring time, will commit as part of arc-28/build feature branch).

If compaction or /clear erases your role, re-read this paste from HUMAN_paste-pliny-arc-28-instruction.md in the project root.
