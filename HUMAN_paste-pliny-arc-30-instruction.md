Read .claude/MAJOR_PLINY.md and assume the orchestrator role for the-stoa.

Your immediate intent for this session: Build Arc 30 per the build directive at substrate/arcs/arc-30-build-directive.md. Small substrate-canon arc: encode the **PLINY pre-branch hygiene discipline** so the bundled-squash pattern observed twice today never recurs. Work-unit ticket: **stoa--3cs** (P1; bumped today from P3 on N=2 bit-by-it + N=1 worked-when-applied evidence).

**PRECONDITION:** Arc 29 (stoa--ads) is CLOSED. the-stoa main at `140b398`. Local main = origin/main verified by user-tier POLYBIUS at dispatch authoring.

**Cron hygiene FIRST (before any substantive work):** Run `CronList`; if any cron is present, CronDelete it. Surface-and-wait per MAJOR_PLINY.md §6.2 (no cron) is the default for PLINY; defense-in-depth.

**Pre-branch hygiene per directive A8 (recursive: this arc encodes the discipline it is itself applying):** before creating arc-30/build, verify local main = origin/main:

```
git fetch origin main
git log --oneline main..origin/main      # should be empty
git log --oneline origin/main..main      # should be empty
```

If either log shows commits, surface — don't silently inherit local-ahead commits into the arc branch.

**Read first (in order):**

1. **`substrate/arcs/arc-30-build-directive.md`** — load-bearing spec. A1-A8 LOCKED architectural decisions. Primary input alongside ticket.
2. **`bw show stoa--3cs`** — work-unit ticket body (original surfacing from Arc 27 PLINY 2026-05-16) + 2026-05-17 scope-expansion comment (PRINCIPAL's articulated rule + empirical evidence + where canon lives). Both read.
3. **`HUMAN_paste-polybius-arc-30-instruction.md`** in the project root — POLYBIUS's activation paste; same content frame.
4. **`substrate/MAJOR_PLINY.md`** — current arc-workflow / branching guidance section. D1 extends or sits beside.
5. **`substrate/operating-disciplines.md`** — D3 cross-ref or universal-team section locus.
6. **`substrate/templates/paste-instruction-template.md`** — D2 may modify (Option β).
7. **Arc 27/28/29 activation pastes at the-stoa root** — ad-hoc encoded the cron-hygiene + pre-branch hygiene preambles; D2 canonifies the pre-branch one.

Operating mode for this dispatch: AUTONOMOUS. Run all four phases heads-down (Phase 1 DAEDALUS + ARGUS, Phase 2 ADA build on feature branch arc-30/build, Phase 3 VERA + CATO + ZENO, Phase 4 smoke + PR + merge + close). Use stoa--3cs for status updates. Surface to PRINCIPAL ONCE at end-of-arc with final clean-PASS verdict.

Coordination: the-stoa PROJECT-TIER POLYBIUS is your radio-check peer (paste at HUMAN_paste-polybius-arc-30-instruction.md). User-tier POLYBIUS dispatched + will do QA pass at arc close. Bidirectional radio-check pattern per substrate/operating-disciplines.md §7.

The architectural decisions A1-A8 are LOCKED in the directive. DAEDALUS treats stoa--3cs's body + 2026-05-17 scope-expansion comment as primary input alongside the directive. Locked decisions encode: one-arc one-gauntlet (A1); two-check pre-branch rule with PRINCIPAL phrasing (A2); canon locus with DAEDALUS Option α/β/γ pick for D2 (A3); cite-comment discipline (A4); authorship immutable (A5); out-of-scope hard-locked (A6); §15 N=1 honesty (A7); pre-branch hygiene self-applied recursive (A8).

**DAEDALUS sub-decision per A3 for D2:** how to encode the pre-branch hygiene preamble as activation-paste convention:
- **Option α:** Add to MAJOR_POLYBIUS.md §5 (onboarding-flow / paste-instruction area)
- **Option β:** Add to substrate/templates/paste-instruction-template.md as mandatory section
- **Option γ:** Both (more redundant)

Pick one + document rationale. The cron-hygiene preamble is OUT of scope (separate forthcoming arc); just encode pre-branch hygiene here.

**Cite-comment discipline per A4:** cross-references to MAJOR_PLINY §6.1, MAJOR_POLYBIUS §5, etc. should resolve. Same pattern as Arc 26's parse_skill_names_from_install + Arc 28's bw-output-parse + Arc 29's base-vs-custom scoping cite-comments.

**CATO is MANDATORY** for this arc. Substrate canon work.

**Forward awareness:** stoa--32b.1 (PRINCIPAL-gate discipline) is FILED but NOT YET BUILT. If any design clause this arc surfaces names "PRINCIPAL-discretion," treat the NEW way (block + escalate immediately).

Authorship attribution is IMMUTABLE per substrate/CLAUDE.md.

**Phase 4 close handshake:** tag `[for: user-tier POLYBIUS]` comment on stoa--3cs inviting QA pass.

**Self-referential note:** Arc 30 encodes the discipline that prevented Arc 29 from bundling-squash. Arc 29 was the worked-example of the discipline working when applied; this arc canonifies it. The canon governs every future arc's branch creation.

Check beadwork (stoa-- prefix) — start with: stoa--3cs (the work-unit; substrate/arcs/arc-30-build-directive.md is its load-bearing artifact, on disk at dispatch authoring time, will commit as part of arc-30/build feature branch).

If compaction or /clear erases your role, re-read this paste from HUMAN_paste-pliny-arc-30-instruction.md in the project root.
