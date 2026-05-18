Arc 42 dispatch brief — PLINY_the_stoa.

You picked this up via your polling cron on stoa--utn. Role + cron infrastructure unchanged from priming + Arcs 39+40+41.

**Long gap since Arc 41 ship** (~hours) — expected per priming. user-tier POLYBIUS ran Pass 8 spec-reconciliation (commit 84d7310) + the-stoa project-tier deploy (commit 51e0b9f) + PRINCIPAL ratification (this dispatch). Substrate HEAD = 42d7735 with Arc 42 directive committed.

## Your immediate intent

Build Arc 42 per `substrate/arcs/arc-42-build-directive.md`. **PRINCIPAL-ratified scope (as-drafted):**

- **C1 LOCKED** — build `substrate/skills/validate-spec/` + run it + produce `agents/observation/spec-validation/mechanical-check-results.md`. **Build-then-use** shape — skill doesn't exist; team authors during arc.
- **A7 fold-in DAEDALUS-discretion**: stoa--1lm (§5.11 extension to DAEDALUS-authored probes) + stoa--bn8 (§6.2 polling-cron canon) + stoa--mn3 housekeeping (5 design.md probe fixes) + stoa--6k1 inline (P10 deletion). User-tier weakly leans include-all; DAEDALUS picks based on scope-cohesion judgment.

**This is the FINAL gauntlet arc before Pass 10 stellation behavioral validation.**

## Critical sections to read carefully

1. **A5 LOCKED** — 7 mechanical checks. DAEDALUS CANNOT reframe what counts as PASS. Each check is from §13.11 + has specific evidence-trail expectation.
2. **A20 MOTIVATED-REASONING MITIGATIONS** — this arc authors the team's own falsification criteria. Treat with care; don't auto-PASS items you can't independently verify.
3. **A21 §25 PRINCIPAL-gates** — pre-flagged surfaces:
   - check-6: ariadne/sector-4/railway drift per stoa--3na — PRINCIPAL's a priori interpretation (per ratification at this dispatch) is **LOOSE** (PASS with documented residue; substrate-authoring tier IS clean). Surface to user-tier-polybius only if discovery diverges from this.
   - check-7: any post-Arc-40 squash-merge missing trailers = substance disagreement (Arc 40 §5.10 canon failure).
4. **A26 SELF-APPLICATION TARGET** — validate-spec MUST run against SPECIFICATION.md as part of the arc. Ships with evidence-of-use, not just evidence-of-existence.

## Read first (in order)

1. **`substrate/arcs/arc-42-build-directive.md`** — A1-A26 LOCKED + A20/A21 motivated-reasoning machinery.
2. **All source ticket bodies**: stoa--1lm + stoa--bn8 + stoa--mn3 + stoa--6k1 + stoa--3na (drift context).
3. **`substrate/arcs/arc-41-build-directive.md`** + Arc 41 ship `6b6fb11` — most recent precedent.
4. **`substrate/skills/check-substrate-updates/`** + **`substrate/skills/inspect-script-output/`** — explicit precedent shapes per §13.11.
5. **`SPECIFICATION.md` §13.11** + **§13.13** + **§13.16** — Pass 9 spec + spec-met criteria + definition of done.
6. **`agents/observation/spec-validation/`** — verify directory existence (create if missing per ADA discretion).
7. **`SPECIFICATION.md` §12.1-§12.5** — current state contracts that the mechanical checks validate against.

## Operating mode

- **AUTONOMOUS** per priming + §7.
- §28 trailers + `[from: pliny-the-stoa]` heartbeats per Arc 36 §7.1/§7.7.
- **CATO MANDATORY** per A24 motivated-reasoning mitigation — CATO cold-reads both implementation AND mech-check-results artifact for craft + scope + HONESTY.

## Sequence reminders

- Phase 4 squash-merge per shipped MAJOR_PLINY.md §5.10 canon (no `--body` override).
- §5.10 signoff live-verified per §19.6.
- A19 IMMUTABLE: new `substrate/skills/validate-spec/SKILL.md` carries `author: Denson Smith`.
- A22 closure: C1 + any A10-A13 fold-in tickets close on ship.
- A25 paste archival: 2 activation pastes to `substrate/arcs/arc-42/pastes/`; directive stays at `substrate/arcs/`.

## Self-application surface (per stoa--bbi N-evidence accretion)

- **validate-spec IS itself a DAEDALUS-authored probe set.** If 1lm fold-in lands, validate-spec's check.sh probes must COMPLY with the new §5.11 extension (self-applied canon at design time).
- **mech-check first-run discovers strangeness** — highest motivated-reasoning risk moment. Engage genuinely; don't auto-PASS.
- **bn8 fold-in** = first arc where polling-cron-PLINY pattern is canonical (vs. operational); future arcs cite canon rather than priming-paste annotation.

## On dispatch close

Comment on stoa--utn with `[for: user-tier-polybius] [from: pliny-the-stoa]` tag carrying:
- Clean-PASS verdict OR substance signals per A21
- Cleanup attestation per Arc 38-41 closure precedent
- The mech-check-results.md path + summary of each of the 7 checks' PASS/FAIL with evidence trail
- Stand down to polling — Pass 10 stellation dispatch is PRINCIPAL-driven from a NEW workspace (~/claude_projects/stellation/); your polling cron stays up for any post-Arc-42 cleanup signals.

## Recovery

If `/compact` or `/clear`: re-read this paste from `HUMAN_paste-pliny-arc-42-instruction.md` at project root. Fall back to `/resume` per handoff-author step 6 mandatory.
