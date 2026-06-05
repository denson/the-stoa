Read .claude/MAJOR_PLINY.md and assume the orchestrator role for the-stoa.

Your immediate intent for this session: Build Arc 31 per the build directive at substrate/arcs/arc-31-build-directive.md. Substantive multi-file substrate-canon arc: encode the **PRINCIPAL-gate discipline** so the AFK-bypass gap from Arc 26 / sector-4 Probe 8 never recurs. Work-unit ticket: **stoa--32b.1** (P2 by ticket; effectively P1 for this dispatch).

**PRECONDITION:** Arc 30 (stoa--3cs) is CLOSED. the-stoa main at `efb0394`. Local main = origin/main + no orphan arc-build branches verified by user-tier POLYBIUS at dispatch authoring.

**Cron hygiene FIRST (before any substantive work):** Run `CronList`; if any cron is present, CronDelete it. Surface-and-wait per MAJOR_PLINY.md §6.2 (no cron) is the default for PLINY; defense-in-depth.

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

**Read first (in order):**

1. **`substrate/arcs/arc-31-build-directive.md`** — load-bearing spec. A1-A11 LOCKED architectural decisions. Primary input alongside ticket + retro source.
2. **`bw show stoa--32b.1`** — work-unit ticket body. PRINCIPAL phrasing + 5 deliverables + acceptance probes + out-of-scope.
3. **`docs/sessions/2026-05-16-substrate-update-architecture-reframe--retro.md` §7** — LOAD-BEARING SOURCE. Frames the conflation problem (gate vs cadence). DAEDALUS treats this as primary prose input.
4. **`bw show stoa--dxw`** + **`bw show stoa--501`** — Arc 26 + sector-4 cleanup (CLOSED; context).
5. **`HUMAN_paste-polybius-arc-31-instruction.md`** in the project root — POLYBIUS's activation paste; same content frame.
6. **`substrate/operating-disciplines.md`** — D1 locus pick (Option α extend §10/§11 vs Option β new section near them; DAEDALUS picks per A3).
7. **`substrate/CAPTAIN_DAEDALUS.md`** + **`substrate/CAPTAIN_ADA.md`** + **`substrate/CAPTAIN_VERA.md`** — D2 envelope updates; per-seat shape per A4.
8. **`substrate/templates/autonomous-mode-activation-template.md`** + **`substrate/templates/polling-cron-prompt-template.md`** — D3 + D4 template updates.

Operating mode for this dispatch: AUTONOMOUS. Run all four phases heads-down (Phase 1 DAEDALUS + ARGUS — LIKELY ARGUS revisions given architecture-sensitivity; Phase 2 ADA build on feature branch arc-31/build; Phase 3 VERA + CATO + ZENO; Phase 4 smoke + PR + merge + close). Use stoa--32b.1 for status updates. Surface to PRINCIPAL ONCE at end-of-arc with final clean-PASS verdict.

Coordination: the-stoa PROJECT-TIER POLYBIUS is your radio-check peer (paste at HUMAN_paste-polybius-arc-31-instruction.md). User-tier POLYBIUS dispatched + will do QA pass at arc close. Bidirectional radio-check pattern per substrate/operating-disciplines.md §7.

The architectural decisions A1-A11 are LOCKED in the directive. DAEDALUS treats stoa--32b.1's body + retro §7 as primary input alongside the directive. Locked decisions encode: one-arc one-gauntlet (A1); the discipline with PRINCIPAL phrasing (A2); D1 locus α/β pick (A3); CAPTAIN envelope per-seat shape (A4); template updates (A5); probe-design sub-case fold-vs-split DAEDALUS pick (A6); cite-comments (A7); authorship immutable (A8); out-of-scope hard-locked (A9); §15 N=1 honesty (A10); pre-branch hygiene self-applied (A11).

**Cite-comment discipline per A7:** cross-references between D1/D2/D3/D4/D5 should resolve via cite at every read-site. Same pattern as Arc 26's parse_skill_names_from_install + Arc 28's bw-output-parse + Arc 29's base-vs-custom scoping + Arc 30's pre-branch hygiene cross-refs.

**CATO is MANDATORY** for this arc (substrate canon work; wording precision is load-bearing).

**Self-referential note:** Arc 31 IS the arc that encodes the discipline whose absence allowed Arc 26's Probe 8 mutation. Until this arc ships, the workaround (activation pastes reminding PLINY to "treat PRINCIPAL-discretion the NEW way") has been carrying the gap. Once shipped, future pastes can drop that workaround.

Authorship attribution is IMMUTABLE per substrate/CLAUDE.md. Arc 31 edits existing files; no fresh author-like field exposure expected.

**Phase 4 close handshake:** tag `[for: user-tier POLYBIUS]` comment on stoa--32b.1 inviting QA pass.

Check beadwork (stoa-- prefix) — start with: stoa--32b.1 (the work-unit; substrate/arcs/arc-31-build-directive.md is its load-bearing artifact, on disk at dispatch authoring time, will commit as part of arc-31/build feature branch).

If compaction or /clear erases your role, re-read this paste from HUMAN_paste-pliny-arc-31-instruction.md in the project root.
