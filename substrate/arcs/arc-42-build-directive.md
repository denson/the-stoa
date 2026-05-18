# Arc 42 build directive — Pass 9 validate-spec mechanical-check (build-then-use)

## Context

Arc 42 is Pass 9 of SPECIFICATION.md §13 workplan — the **mechanical-check pass that validates substrate state matches spec**. This is the FINAL gauntlet-arc before Pass 10 stellation behavioral validation. Per §13.11:

> Author + run a `validate-spec` skill following the §27 mechanical-script / agent-inspection split pattern. **Note:** the skill does NOT yet exist; the team authors it as part of Pass 9 (build-then-use, not use-existing) using `substrate/skills/check-substrate-updates/` and `substrate/skills/inspect-script-output/` as precedent shapes.

**This is a BUILD-THEN-USE arc** — the team writes the skill, then runs it, then captures results, in one gauntlet. Similar self-applied shape as Arc 38 TIRO (built + dispatched in same arc) and Arc 39 save-verdict (built + self-applied in same arc).

## Candidates

**C1 LOCKED — validate-spec skill build + first run.** Author `substrate/skills/validate-spec/` (SKILL.md + check.sh + any Python helpers as needed). Run it. Produce the artifact at `agents/observation/spec-validation/mechanical-check-results.md` per §13.11.

**Optional A7 fold-in (DAEDALUS-discretion)**:
- **stoa--1lm (P3)** — extend CAPTAIN_VERA.md §5.11 anchoring discipline to DAEDALUS-authored design.md probes (per Arc 41 DAEDALUS §6.4 proposal + 5-finding mn3 cluster as empirical anchor). Substantive substrate-canon edit; mirrors the §5.11 shape PLINY's MAJOR_PLINY.md §5.10 6wp extension took.
- **stoa--bn8 (P3)** — amend MAJOR_PLINY.md §6.2 to permit polling-cron for multi-arc autonomous engagements (per Arcs 39-41 proto-canon-promotion evidence). Substantive substrate-canon edit.
- **stoa--mn3 housekeeping** — 5 design.md probe-spec fixes (Arc 40 m1+m2 + Arc 41 m_4.5.2+m_4.12.2+m_4.12.3). PLINY-lean per ticket body = α direct-to-main; could fold into 1lm work cohesively since 1lm covers the canon-level extension and mn3 covers the existing-defect cleanup (they're complementary).
- **stoa--6k1 inline** — Probe P10 spec refinement in `agents/design/arc-25/design.md` per §13.10 (handled inline during Pass 8 housekeeping; could be picked up here if not yet done).

User-tier weakly leans **include 1lm + bn8 + mn3 + 6k1**: bundling the canon-extensions + housekeeping with the validate-spec build keeps the FINAL gauntlet-arc comprehensive. But DAEDALUS may judge fold-in increases motivation-reasoning risk (see §A20 below) — in which case ship 1lm + bn8 + mn3 + 6k1 separately as Arc 43 small-bundle.

## Architectural decisions A1-A23 (LOCKED unless flagged DAEDALUS-discretion)

### Bundle structure
- **A1 LOCKED**: single design.md document covering C1 + any A7 fold-ins. Per Arc 37/38/39/40/41 precedent.

### C1 validate-spec skill (LOCKED scope)
- **A2 LOCKED**: skill path = `substrate/skills/validate-spec/`. Mirrors check-substrate-updates / inspect-script-output structure.
- **A3 LOCKED**: SKILL.md frontmatter `author: Denson Smith` per A18 IMMUTABLE.
- **A4 LOCKED**: install.sh SKILL_NAMES += validate-spec (deploys at all 3 tiers).
- **A5 LOCKED — 7 mechanical checks per §13.11**: each check returns PASS/FAIL with evidence trail:
  - **check-1**: every §-reference in SPECIFICATION.md resolves (grep canon file at named section)
  - **check-2**: every cited `stoa--*` ticket id exists in bw with claimed status (use `bw list --all` for completeness; CAPTAIN_TIRO if available)
  - **check-3**: `bw list --status open --all` returns tickets all placed in some §13.x ticket-placing section (no unplaced tickets surface)
  - **check-4**: `git status` shows no uncommitted changes except ignorable auto-modified state files per §12.4
  - **check-5**: `_drafts/` empty OR contains only in-flight-engagement docs per §12.4
  - **check-6**: `check-substrate-updates` returns "no drift" across registered consumer workspaces (per stoa--3na: only the-stoa is guaranteed clean at Arc 42 time; ariadne/sector-4/railway pending separate apply sessions per §13.13 criterion 4 gate evaluation in A21 below)
  - **check-7**: §28 Co-Authored-By trailers on post-Arc-35 squash-merge commits with EXPLICIT CARVE-OUT for `bb12806` (Arc 37); commits authored AFTER Arc 40 ship (dbb5b81 onwards) must carry trailers
- **A6 DAEDALUS-discretion**: skill implementation shape:
  - **(α)** Shell-only (`check.sh` calling git/grep/bw inline) — matches check-substrate-updates precedent
  - **(β)** Shell-orchestrator + Python helpers for complex checks (e.g., spec §-resolution, ticket-status parsing) — matches save-verdict shape
  - **(γ)** Pure Python — heavier but more testable
  - User-tier leans α-or-β. DAEDALUS picks based on per-check complexity.
- **A7 LOCKED — output artifact**: `agents/observation/spec-validation/mechanical-check-results.md` per §13.11. Captures per-check PASS/FAIL + evidence trail + explicit `bb12806` carve-out attestation + execution timestamp + substrate SHA at run-time.

### Inspection-agent triage (per §27 split)
- **A8 DAEDALUS-discretion**: inspection-agent shape:
  - **(δ)** Separate `inspect-spec-validation-output` skill (parallel to `inspect-script-output` skill that ships in substrate)
  - **(ε)** Inline triage block in `validate-spec` SKILL.md instructing POLYBIUS to triage strangeness manually
  - User-tier weakly leans ε (inline triage; defers separate-skill build to future arc if strangeness-frequency justifies)
- **A9 LOCKED**: POLYBIUS triages diagnoses post-validate-spec-run; fix-now items get fixed in-arc OR routed to follow-up tickets; PRINCIPAL escalations surface per §25.

### A7 fold-in candidates (DAEDALUS-discretion)
- **A10 DAEDALUS-discretion**: 1lm fold-in (§5.11 extension to DAEDALUS-authored design.md probes). User-tier weakly leans **include** — substantive substrate-canon edit that complements the validate-spec build (the new validate-spec check.sh DAEDALUS authors is itself a DAEDALUS-authored "probe spec" that should comply with the new §5.11 extension; self-application opportunity).
- **A11 DAEDALUS-discretion**: bn8 fold-in (§6.2 polling-cron canon). User-tier weakly leans **include** — substantive substrate-canon edit; pairs naturally with 1lm.
- **A12 DAEDALUS-discretion**: mn3 housekeeping fold-in (5 design.md probe-spec fixes). User-tier weakly leans **include if 1lm folded** (1lm provides the canon basis; mn3 is the existing-defect cleanup under that canon).
- **A13 DAEDALUS-discretion**: 6k1 inline (P10 probe in arc-25 design.md). User-tier weakly leans **include** — small (1 probe deletion).

### Universal (continued from Arc 41)
- **A14 LOCKED**: §28 Co-Authored-By trailers per Arc 35 canon. Phase 4 squash-merge per MAJOR_PLINY.md §5.10 (shipped Arc 40; now downstream-consumer canon).
- **A15 LOCKED**: §5.10 signoff with live-verified state per §19.6.
- **A16 LOCKED**: `[from: <self-seat-slug>]` author tags per Arc 36 §7.1/§7.7.
- **A17 LOCKED**: cron infrastructure REUSE existing (POLYBIUS: `b6e8630b` / `3c1e575b`; PLINY: `abc905a6` / `6e69c60a`).
- **A18 LOCKED**: cite-comment discipline per Arc 38 A17 — cross-refs in new validate-spec SKILL.md + any 1lm/bn8/mn3/6k1 edits must resolve via cite at every read-site.
- **A19 LOCKED**: A18 IMMUTABLE — new `substrate/skills/validate-spec/SKILL.md` MUST carry `author: Denson Smith` frontmatter.
- **A20 LOCKED — MOTIVATED-REASONING MITIGATION**: this arc authors the team's own falsification criteria. Mitigations:
  - PRINCIPAL ratifies this directive BEFORE dispatch (the LOCKED scope = the falsification criteria; DAEDALUS cannot weaken)
  - Each mechanical check is LOCKED at A5 (DAEDALUS cannot reframe what counts as PASS)
  - user-tier POLYBIUS QA pass at arc close audits the artifact for genuine PASS vs. motivated-PASS (each check verified live independently)
  - First-run-discovers-strangeness is GOOD signal; team must NOT auto-PASS items it cannot independently verify. Strangeness routes to inspection-agent triage (A8/A9) OR PRINCIPAL escalation (A21 §25 gate).
- **A21 LOCKED — Pass-9 specific §25 PRINCIPAL-gates**:
  - check-6 substrate drift sweep: if validate-spec finds ariadne/sector-4/railway drift state per stoa--3na, surface to PRINCIPAL whether to BLOCK ship-clean on drift (interpret §13.13 criterion 4 strictly) OR pass-with-known-residue (interpret loosely; document residue in mech-check-results artifact). PRINCIPAL chooses interpretation.
  - check-7 trailer carve-out: if validate-spec finds ANY post-Arc-40 squash-merge missing trailers, surface as substance disagreement — Arc 40 §5.10 canon should have prevented this; failure indicates canon gap.
  - Any mechanical check that genuinely FAILS surfaces to PRINCIPAL with the failing evidence; PRINCIPAL ratifies fix-now vs document-as-residue vs spec-edit.
- **A22 LOCKED**: A19 source-ticket closure — on Arc 42 ship: close C1 implicitly (Pass 9 done = validate-spec skill exists + ran once + artifact landed); close A10/A11/A12/A13 fold-in tickets if included (1lm + bn8 + mn3 + 6k1). Tag `[for: user-tier-polybius]` on stoa--utn (continuing as dispatch ticket — the long-running engagement coordination ticket through end of sequence).
- **A23 LOCKED**: A20 hard-locks (Arc 42-specific):
  - No restructuring the 7 mechanical checks beyond what A5 LOCKS (motivated-reasoning prevention)
  - No widening A8/A9 inspection-agent shape into a heavier separate skill build (defer to future arc if needed)
  - No building Pass 10 stellation behavioral validation in this arc (separate concern per §13.12)

### Arc-shaping (continued)
- **A24 LOCKED**: CATO MANDATORY per A20 motivated-reasoning mitigation — CATO must cold-read both the validate-spec implementation AND the mech-check-results artifact for craft + scope + honesty.
- **A25 LOCKED**: bw-signal dispatch model — Arc 42 dispatched via bw comment on stoa--utn (`[for: pliny-the-stoa]` + `[for: polybius-the-stoa]` tags); both seats engaged via priming-set polling crons. §5.11 archival of 2 activation pastes to `substrate/arcs/arc-42/pastes/` (directive stays at `substrate/arcs/`; per Arc 41 A16 wording-clarification).
- **A26 LOCKED — SELF-APPLICATION TARGET**: validate-spec skill MUST run against SPECIFICATION.md as part of the arc; the artifact mech-check-results.md captures that first run. **The skill ships with evidence-of-use, not just evidence-of-existence.**

## DAEDALUS sub-decisions summary

| ID | Decision | User-tier lean | DAEDALUS picks |
|---|---|---|---|
| A6 | validate-spec implementation shape | α-or-β (shell or shell+Python) | yes |
| A8 | inspection-agent triage shape | ε (inline triage in SKILL.md) | yes |
| A10 | stoa--1lm fold-in | include | yes |
| A11 | stoa--bn8 fold-in | include | yes |
| A12 | stoa--mn3 housekeeping fold-in | include (if 1lm folded) | yes |
| A13 | stoa--6k1 inline | include (small) | yes |

If DAEDALUS judges the 5-candidate fold-in (C1 + 1lm + bn8 + mn3 + 6k1) increases motivated-reasoning risk OR scope-cohesion-cost, ship C1 alone in Arc 42 + the fold-ins as Arc 43 small-bundle. PRINCIPAL ratifies the directive scope at this surface; DAEDALUS executes within it.

## Self-application observations to watch for stoa--bbi accretion

Arc 42 has rich self-application surface:
- **validate-spec is itself a DAEDALUS-authored probe set** — if 1lm fold-in includes the §5.11 extension to DAEDALUS-authored design.md probes, validate-spec's check.sh probes should COMPLY with the extension. **Self-applied canon at design time.**
- **mech-check first-run discovers strangeness** — this is the highest-risk-of-motivated-reasoning moment. Watch whether team auto-PASSes vs. genuinely engages with first-run strangeness.
- **bn8 fold-in self-application**: if §6.2 polling-cron canon ships, future arcs that use the pattern can cite the canon rather than the priming-paste annotation as authority. Worth noting for Arc 43+.
- **Sequence-end milestone shape**: Arc 42 close = ready-for-stellation milestone. Observe whether the multi-arc autonomous engagement model that ran Arcs 39-41 can also run Arc 42 (the bn8 canon's first test) OR whether build-then-use shape requires PRINCIPAL touchpoints.

## Ship gate

Arc 42 ships when:
- design.md cleared by ARGUS (rev cycles per DAEDALUS judgment; expect 1-2 cycles given build-then-use complexity)
- ADA build complete: validate-spec skill exists at substrate/skills/validate-spec/; install.sh wires it; any A10-A13 fold-ins landed
- ADA runs validate-spec against SPECIFICATION.md; artifact written to `agents/observation/spec-validation/mechanical-check-results.md`
- ZENO mechanical PASS on file-existence + frontmatter + install.sh wiring
- VERA falsification PASS on probes (skill behavior + check outputs match design)
- CATO craft + scope + honesty review PASS (especially the mech-check-results artifact)
- Inspection-agent triage of any strangeness — fix-now items fixed; escalations surfaced per A21
- Phase 4: squash-merge per §5.10; cleanup; paste archival per §5.11
- §5.10 signoff with live-verified state
- Source tickets closed per A22; `[for: user-tier-polybius]` tag on stoa--utn

**After Arc 42 ships clean + user-tier QA pass + PRINCIPAL ratification of the mech-check-results artifact → user-tier POLYBIUS surfaces "ready for stellation dispatch" verdict to PRINCIPAL with §13.13 criteria 1-5 attestation table.**

## What's explicitly out of scope per §13.14

- Building Pass 10 stellation dispatch infrastructure (separate concern; PRINCIPAL drives setup per §13.12)
- Extending validate-spec to non-spec-met checks (e.g., consumer-workspace product-feature validation; non-substrate-canon checks)
- Building meta-agent for cross-generation lineage analysis (§10.1 property 3 / §12.5 — explicitly out per §13.14)
- Shipping deferred-with-gating items (stoa--tvc + stoa--myd per §13.9)
- Building stoa--lyw `/resume` invocation discipline canon (per §13.14; sufficient for spec-met as recording-only)
