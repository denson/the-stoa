Read .claude/MAJOR_PLINY.md and assume the orchestrator role for the-stoa.

Your immediate intent for this session: Build Arc 37 per the build directive at substrate/arcs/arc-37-build-directive.md. **6-candidate substrate architecture canonification batch:** C1 stoa--86k two-team forge/shop + C2 stoa--kt6 multi-team interop + C3 stoa--wad four-layer identity model + C4 stoa--ntn operating-mode progression + C5 stoa--53u idle-retrospective-narrative confabulation + C6 stoa--7e3 handoff-author skill. Mirrors Arc 32 (5 candidates) + Arc 34 (4 candidates) bundling shape.

**PRECONDITION:** Arc 36 v2 (stoa--jru) is CLOSED at PR #16 squash-merge `fcd68c0` + paste archival `8ced17c`. Pass 1 + Pass 2 substrate cleanup landed. the-stoa main at `679b6bf` (or wherever the dispatch commit lands on top). Local main = origin/main + no orphan arc-build branches verified by user-tier POLYBIUS at dispatch authoring.

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

**Worktree convention per MAJOR_PLINY.md §5.9.4 (directive A20):** create arc-37/build in separate worktree: `git worktree add .claude/worktrees/arc-37-build arc-37/build`. Main worktree stays on main.

**Read first (in order):**

1. **`substrate/arcs/arc-37-build-directive.md`** — load-bearing spec for all 6 candidates. A1-A20 LOCKED. A8-A13 are DAEDALUS sub-decisions (per-candidate section numbers + C6 skill scope).
2. **All 6 source ticket bodies:** `bw show stoa--86k` + `bw show stoa--kt6` + `bw show stoa--wad` + `bw show stoa--ntn` + `bw show stoa--53u` + `bw show stoa--7e3` (+ `_drafts/skill_handoff_author.md` as C6 draft input).
3. **`HUMAN_paste-polybius-arc-37-instruction.md`** in the project root — POLYBIUS's activation paste; same content frame.
4. **`substrate/MAJOR_POLYBIUS.md`** — C1 + C3 + C4 + C6 touch-points (§16 lifecycle; §18 housekeeping; §5.1.1.1 cross-project sequencing).
5. **`substrate/MAJOR_PLINY.md`** — C4 + C5 + C6 touch-points (§5.10 signoff; §5.12 seat-identity-in-dispatch-brief; §6.2 surface-and-wait; §7 verify-then-execute).
6. **`substrate/operating-disciplines.md`** — primary surface for canon edits:
   - §7.4 + §7.5 cross-tier conventions (C2 cite)
   - §10 + §11 HITL/Autonomous + autonomous-mode-setup (C4 extension surface)
   - §17 + §23 base-vs-custom (C1 cite)
   - §19.6 attestation-confabulation (C5 sister)
   - §28 Co-Authored-By trailer (Arc 35 canon; ADA commits apply)
7. **`substrate/install.sh`** — C6 SKILL_NAMES addition surface.
8. **`substrate/skills/check-bw-release/`** + **`substrate/skills/inspect-script-output/`** — precedents for substrate skill shape; C6 follows pattern.
9. **`the-stoa/SPECIFICATION.md` §10.1 + §4.5 + §13** — generational-lineage architecture (C3 + C6 cite); workplan context (Arc 37 is §13.4 Pass 3).

Operating mode for this dispatch: AUTONOMOUS. Run all four phases heads-down. Use one of the 6 source tickets (or a fresh coordination ticket if needed) for status updates. Surface to PRINCIPAL ONCE at end-of-arc with final clean-PASS verdict.

Coordination: the-stoa PROJECT-TIER POLYBIUS is your radio-check peer (paste at HUMAN_paste-polybius-arc-37-instruction.md). User-tier POLYBIUS dispatched + will do QA pass at arc close. Bidirectional radio-check pattern per substrate/operating-disciplines.md §7. **Per Arc 36's §7.1 5th beat + §7.7 author-tag convention, POLYBIUS coordination comments carry `[from: polybius-the-stoa]` per the convention shipped in Arc 36.**

The architectural decisions A1-A20 are LOCKED in the directive. DAEDALUS treats this directive as primary input alongside the 6 source ticket bodies. Locked decisions encode:

- A2 C1 two-team forge/shop behavioral canon (LOCKED scope; MAJOR_POLYBIUS.md section)
- A3 C2 multi-team interoperation unified canon (LOCKED scope; new operating-disciplines.md section)
- A4 C3 four-layer identity model + memories-as-alignment (LOCKED scope; new operating-disciplines.md section + MAJOR_POLYBIUS.md cross-ref)
- A5 C4 operating-mode progression (LOCKED scope; §10 + §11 extensions)
- A6 C5 idle retrospective-narrative confabulation (LOCKED scope; §19.7 sister to §19.6)
- A7 C6 handoff-author skill (LOCKED scope; new substrate/skills/handoff-author/ + install.sh wiring)
- A14 self-application (C6 only meaningfully self-applies; C5 negative-self-applies)
- A15 cite-comments
- A16 authorship attribution unchanged + C6 SKILL.md author: Denson Smith MANDATORY
- A17 out-of-scope hard-locked (no mechanical enforcement; no bj5/utn/3sz/5sr/pqn bundling; no meta-agent build; no memory-introspect skill; no multi-team registry)
- A18 source-ticket closure (all 6 close on ship)
- A19 §15 N=1 honesty per candidate
- A20 pre-branch + worktree + signoff self-applied

**DAEDALUS sub-decisions (A8-A13):**
- A8 (C1 MAJOR_POLYBIUS.md section number) — user-tier leans new §19
- A9 (C2 operating-disciplines.md section number) — user-tier leans §29
- A10 (C3 operating-disciplines.md section number) — user-tier leans separate §30 (parallel to §29)
- A11 (C4 placement) — user-tier leans extensions inside existing §10 + §11
- A12 (C5 subsection number) — user-tier leans §19.7
- A13 (C6 fold session-id record into SKILL.md vs defer) — user-tier leans fold

If any pick surfaces as needing PRINCIPAL judgment rather than DAEDALUS discretion, treat as PRINCIPAL-gate per §25 — halt + escalate immediately rather than proceed-then-flag.

**Cite-comment discipline per A15:** cross-refs between the 6 new/extended sections must resolve via cite at every read-site. Same pattern as Arcs 26-36 cite-comments. Specifically:
- C1 ↔ §23 + §17 (base-vs-custom)
- C2 ↔ §7.4 + §7.5 + MAJOR_POLYBIUS.md §5.1.1.1
- C3 ↔ MAJOR_POLYBIUS.md C1 + §10.1 lineage
- C4 ↔ MAJOR_PLINY.md + MAJOR_POLYBIUS.md mode-handling
- C5 ↔ §19.6 + MAJOR_PLINY.md + MAJOR_POLYBIUS.md self-narrative sections
- C6 ↔ MAJOR_POLYBIUS.md + MAJOR_PLINY.md + §10.1 (if A13 folds)

**CATO is MANDATORY** for this arc (substrate canon work + new skill + multiple new sections; wording precision matters; 6-candidate bundle has more surface than any prior arc).

**Authorship attribution is IMMUTABLE per CLAUDE.md** for file frontmatter. C6's new `substrate/skills/handoff-author/SKILL.md` frontmatter MUST carry `author: Denson Smith` per Arc 27 stoa--uly convention. Verify before commit. **Co-Authored-By trailers per §28 apply to all ADA + DAEDALUS commits** in arc-37/build.

**Self-application per A14:**
- C5 negative self-application: do NOT confabulate retrospective narratives of past work during this arc. If scanning closed tickets to ground context, cite them as past-work-evidence, not as own-current-session accomplishment.
- C6 positive self-application: if any seat hits `/compact` or session-close during this arc, invoke the newly-shipped handoff-author skill. Low probability for a 90-180min arc but the canon authorizes it.

**Phase 4 close handshake per §5.10 + A18:**
- Verify cleanup executed (arc-37/build local + remote deleted; worktree removed; PR merged; main fast-forwarded).
- Verify ADA/DAEDALUS commits carry Co-Authored-By trailers per §28.
- Verify C6 SKILL.md frontmatter carries `author: Denson Smith`.
- Verify install.sh SKILL_NAMES includes handoff-author.
- Close all 6 source tickets (stoa--86k + stoa--kt6 + stoa--wad + stoa--ntn + stoa--53u + stoa--7e3) per A18 with cross-refs + audit comments per candidate.
- Tag `[for: user-tier-polybius]` on at least one closed ticket (recommend stoa--7e3 since it's the most architecturally novel).
- Archive activation pastes to `substrate/arcs/arc-37/pastes/` per §5.11.

**Self-referential note:** Arc 37 is the substrate's largest canon batch (6 candidates spanning architecture canon + new skill). Per the-stoa SPECIFICATION.md §10.1 generational-lineage architecture, this arc creates a successor-generation team with substantially more articulated canon (forge/shop framing + multi-team interop + four-layer identity + mode progression + retrospective-narrative discipline + handoff-author skill). After Arc 37 ships + Arc 38 (user-tier drift detection) + Arc 39 (small bundled follow-ups) ship: **zero open substrate-canon tickets at the-stoa**, and the substrate is ready for §13.9 Pass 8 behavioral validation via stellation dispatch.

Check beadwork (stoa-- prefix) — start with: any of the 6 source tickets (substrate/arcs/arc-37-build-directive.md is the load-bearing artifact, on disk at dispatch authoring time, will commit as part of arc-37/build feature branch).

If compaction or /clear erases your role, re-read this paste from HUMAN_paste-pliny-arc-37-instruction.md in the project root.
