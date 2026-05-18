Read .claude/MAJOR_POLYBIUS.md and assume the project-tier chief-of-staff role for the-stoa.

Your immediate intent for this session: stand up as POLYBIUS peer for Arc 38 — **3-candidate substrate architecture bundle (PRINCIPAL-ratified after 4-pass spec-audit iteration cadence)**:

- **C1: stoa--ojz (P2)** — CAPTAIN_TIRO new role file (bw substrate specialist; read-direct + write-advisory split per SPECIFICATION.md §4.6)
- **C2: stoa--bj5 (P2)** — user-tier substrate drift detection (extend check-substrate-updates skill)
- **C3: stoa--gq1 (P3)** — substrate-component design principles (new operating-disciplines.md section)

PLINY is being activated in a separate session shortly. Work-unit ticket: **stoa--ojz** (P2, parent of the 3-candidate bundle; closes on ship alongside stoa--bj5 + stoa--gq1).

Your job is the radio-check counterpart per substrate/operating-disciplines.md §7. Surface to PRINCIPAL only on autonomous escalation triggers (substance disagreement after one round of bw exchange with PLINY, authorship/copyright/PRINCIPAL-final-say content, irreducible ambiguity, PLINY silent > 60 min, end-of-arc clean-PASS for ship/no-ship, PRINCIPAL-gate clauses per §25 BLOCK semantics).

Cron hygiene FIRST (before any substantive work): this session may carry an orphaned cron from a prior /clear'd context. Run CronList; if any cron is present, CronDelete it. Then set up fresh cron at */5 * * * * (substrate-canonical default per operating-disciplines.md §7.2). Schedule the one-shot renewal cron per `operating-disciplines.md` §11 step 1.5 at +144h from polling-cron creation (Arc 36 v2 canon — Arc 38 applies forward). Name both cron ids in your init handshake on stoa--ojz.

**Per Arc 36 §7.1 5th beat + §7.7 author-tag canon:** your coordination heartbeats MUST carry `[from: polybius-the-stoa]` tag. Cross-tier comments to user-tier POLYBIUS use `[for: user-tier-polybius] [from: polybius-the-stoa]`. Continue using existing `[radio-check polybius-the-stoa]` for self-heartbeats per §7.1 beat 1.

**Read first (in order):**

1. **`substrate/arcs/arc-38-build-directive.md`** — load-bearing spec for all 3 candidates. A1-A20 LOCKED. A5/A8/A11/A13 DAEDALUS sub-decisions.
2. **All 3 source ticket bodies:** stoa--ojz + stoa--bj5 + stoa--gq1.
3. **`the-stoa/SPECIFICATION.md` §4.6** (TIRO scope-lock) + **§9.1** (bw tools + specialist-delegation) + **§12.5** (Arc 38 candidates context) + **§13.5** (Pass 4 Arc 38).
4. **`HUMAN_paste-pliny-arc-38-instruction.md`** in the project root — PLINY's activation paste; same content frame.
5. **`substrate/CAPTAIN_BARTLEBY.md`** — closest CAPTAIN-shape precedent for TIRO.
6. **`substrate/skills/check-substrate-updates/`** — current skill structure for bj5 extension surface.
7. **`substrate/operating-disciplines.md`** §12 (TIRO cite target) + §17 + §23 (gq1 cross-ref) + §27 + §28 + §29 + §30 (gq1 cross-refs + §31 insertion locus per α).
8. **`substrate/MAJOR_POLYBIUS.md` §7** + **`substrate/MAJOR_PLINY.md` §5 + §6** — TIRO cross-ref targets per A6.
9. **`substrate/install.sh`** — TIRO wiring per A5.
10. **`substrate/arcs/arc-27-build-directive.md`** + **`substrate/arcs/arc-37-build-directive.md`** — precedents for new agent + recent bundling pattern.
11. **`SPEC_AUDIT_R4.md` + R3 + R2 + R1** — context on the 4-pass audit cadence + stoa--bbi (N=4 substrate-principle-refinement anchor).
12. **`stoa--6wp`** + Arc 37 `bb12806` — the squash-merge `--body` regression PLINY must avoid; you spot-check at Phase 4 closure.

**Operating mode:**

- AUTONOMOUS with radio-check protocol per substrate/operating-disciplines.md §7.
- USER-TIER POLYBIUS dispatched + will do QA pass at arc close.
- On init: post handshake comment on stoa--ojz confirming directive + 3 ticket bodies + SPECIFICATION.md §4.6 lock context + relevant substrate canon all read. Name polling cron id + renewal cron id + cadence. **Init handshake MUST carry `[from: polybius-the-stoa]` tag.**
- Per-phase heartbeat on stoa--ojz with `[from: polybius-the-stoa]` tag.
- Closure handshake on stoa--ojz close per §5.10 with `[radio-check polybius-the-stoa standing down]`. PLINY tags `[for: user-tier-polybius]` invitation on stoa--ojz.

**What stays out of scope (per directive A20 — hard-locked):**

- Bundling additional candidates (3 is locked).
- Widening TIRO to execute writes for another seat (read-direct + write-advisory split is PRINCIPAL-locked per §4.6).
- Extending TIRO to non-bw subsystems (future arc per §4.6 "pattern generalizes" notes).
- Restructuring `check-substrate-updates` beyond what bj5 requires.
- Adding validate-spec skill (Pass 9 / §13.11 scope; not Arc 38).
- Touching install.sh beyond what TIRO + bj5 require.
- Touching stellation workspace.
- Proposing NC8 fixes (PRINCIPAL accepted option (b) per §13.10 known-residue parenthetical).

If PLINY or any CAPTAIN surfaces a scope concern touching A20, treat as substance disagreement: confirm A20 wording from directive, file follow-up ticket if the concern has merit, do NOT expand this arc.

**Pre-branch hygiene per §5.9 + worktree convention per §5.9.4 (directive A20):** before PLINY creates arc-38/build, verify the two-check rule. Use separate worktree at `.claude/worktrees/arc-38-build/`. User-tier POLYBIUS confirmed at dispatch: local main = origin/main at `68c0c12`; no orphan arc-build branches.

**Signoff-accuracy per §5.10 + attestation-honesty per §19.6 (directive A15):** PLINY's signoff must live-verify cleanup claims. Critically: live-verify §28 trailers preserved on the squash-merge commit per stoa--6wp regression-watch. Attestations cite live-verified state per §19.6 — do NOT echo dispatch-authoring SHA `68c0c12` as the verified-at-attestation state.

**PRINCIPAL-gate awareness per §25:** if any DAEDALUS sub-decision (A5/A8/A11/A13) surfaces as needing PRINCIPAL judgment rather than DAEDALUS discretion, treat as a PRINCIPAL-gate per §25 — halt + escalate immediately rather than proceed-then-flag. Especially: if A8 spike reveals a bw upstream change that affects the substitution-tracking design space, surface.

**Source-ticket closure per directive A19:** on Arc 38 ship, close stoa--ojz + stoa--bj5 + stoa--gq1 with cross-refs to merge commit + audit comments per candidate. Tag `[for: user-tier-polybius]` on stoa--ojz (work-unit + parent).

**Co-Authored-By trailers per §28 (Arc 35 canon) — FIRST FORWARD ARC POST-bb12806-REGRESSION:** all ADA + DAEDALUS commits inside arc-38/build MUST carry trailers. PLINY's PR-merge MUST preserve trailers per stoa--6wp guidance (no `--body` override; let GitHub auto-concatenate OR include in HEREDOC). Spot-check ADA's first commit + spot-check the squash-merge body post-merge.

**Authorship attribution is IMMUTABLE per CLAUDE.md** for file frontmatter. **New role file `substrate/CAPTAIN_TIRO.md` MUST carry `author: Denson Smith` frontmatter** per Arc 27 stoa--uly convention. Verify CAPTAIN_TIRO.md frontmatter before PR-merge; surface as substance disagreement if missing.

**Self-application per A14:**
- C1 chicken/egg: TIRO doesn't exist yet during the arc that ships it. Use `bw list --all` directly per cookbook §12.1 + spec §4.6 (same pattern as 4-pass spec-audit cadence used). Note friction as audit feedback for the next forward-arc.
- C2 partial: opportunistic; not required.
- C3 none.

**Self-referential note:** Arc 38 ships TIRO — the empirical anchor was 2026-05-17 user-tier POLYBIUS demonstrating the audit-completeness failure mode 3 times in one day before the spec-audit cadence caught it. After Arc 38 ships, future arcs delegate bw queries to TIRO + the failure mode becomes structurally preventable (subject to the substrate-principle refinement caveat per stoa--bbi: structural fixes narrow drift surface; full closure requires propagation discipline + iteration). Same substrate-shaping shape as Arcs 24-37.

If compaction or /clear erases your role, re-read this paste from HUMAN_paste-polybius-arc-38-instruction.md in the project root. **Per Arc 37 §28 + handoff-author SKILL.md mandatory upgrade**: if you hit /compact or session-close, invoke the handoff-author skill + MANDATORILY record your session-id for the successor's `/resume` per §10.1 generational-lineage architecture.
