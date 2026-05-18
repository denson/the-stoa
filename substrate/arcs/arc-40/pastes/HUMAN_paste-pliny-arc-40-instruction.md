Arc 40 dispatch brief — PLINY_the_stoa.

You picked this up via your polling cron on stoa--utn. Role + cron infrastructure unchanged from priming + Arc 39.

## Your immediate intent

Build Arc 40 per `substrate/arcs/arc-40-build-directive.md`. **4 LOCKED candidates + optional 6n9/t9u fold-in (DAEDALUS-discretion):**

- **C1: stoa--3sz (P3)** — probe-spec `^last=` anchor canon
- **C2: stoa--5sr (P3)** — DAEDALUS Edit-tool worktree-path discipline (DAEDALUS reads `agents/design/arc-24/design.md` to articulate the gap)
- **C3: stoa--dhc (P3)** — python-vs-jq rationale single-source-of-truth lift
- **C4: stoa--6wp (P3) [BUG, SEQUENCE-CRITICAL]** — squash-merge `--body` override trailer-regression fix; MAJOR_PLINY.md §5.10 ship-checklist + optional op-disc §28.3.1 worked-example
- **Optional fold-in (DAEDALUS-discretion per A7):** stoa--6n9 (manifest format-version) + stoa--t9u (install.sh pycache exclude). Both install.sh-adjacent; user-tier weakly leans include if scope-cohesive.

## Read first (in order)

1. **`substrate/arcs/arc-40-build-directive.md`** — load-bearing spec. A1-A20 LOCKED. A3 / A4 / A5 / A6 / A7 DAEDALUS sub-decisions.
2. **All 4 source ticket bodies:** `bw show stoa--3sz` + `bw show stoa--5sr` + `bw show stoa--dhc` + `bw show stoa--6wp`. Plus stoa--6n9 + stoa--t9u if considering A7 fold-in.
3. **`agents/design/arc-24/design.md`** — required for A4 (5sr failure mode articulation).
4. **`substrate/arcs/arc-39-build-directive.md`** + **Arc 39 ship commit f1f222a** — most recent precedent; trailer-clean pattern held forward of bb12806.
5. **Arc 37 `bb12806` commit** — the empirical anchor 6wp is fixing; live-verify the trailer-loss to ground the worked example if A3 includes op-disc §28.3.1.
6. **`substrate/MAJOR_PLINY.md` §5.10** — the ship-checklist 6wp extends.
7. **`substrate/operating-disciplines.md` §28** — trailer canon; §28.3 is the parent for the optional §28.3.1 pitfall subsection.
8. **`substrate/MAJOR_PLINY.md` §5.8** + **`substrate/MAJOR_POLYBIUS.md` §7.6** + **`substrate/operating-disciplines.md` §18** + **`substrate/skills/agent-author/SKILL.md`** — the 4 sites carrying the python-vs-jq rationale prose that dhc lifts to single-source-of-truth.
9. **`substrate/CAPTAIN_VERA.md`** — probe-authoring section for 3sz placement (A6 γ).
10. **`substrate/CAPTAIN_DAEDALUS.md`** — design-authoring section for 5sr placement.

## Operating mode

- **AUTONOMOUS** per priming + §7.
- §28 trailers + `[from: pliny-the-stoa]` heartbeats per Arc 36 §7.1/§7.7.
- CATO MANDATORY per A17.

## Recursive-shape surveillance (A20)

You are editing your OWN role file (MAJOR_PLINY.md §5.10) pre-merge as part of an arc YOU run end-to-end. Watch for:
- The edit committed to arc-40/build pre-merge (not after).
- The deployed file at user-tier after Arc 40 ships matches the substrate-tier source.
- Your own Phase 4 signoff comment cites the new §5.10 wording correctly (self-application of the new canon during the arc that ships it).

If circularity reveals an issue not foreseen in this directive, surface as substance disagreement per §7.4.

## Sequence reminders

- **6wp is SEQUENCE-CRITICAL** per §13.7 — must ship before Pass 9/10 stellation.
- Phase 4 squash-merge: NO `gh pr merge --body` override (Arc 38 + Arc 39 pattern held organically; Arc 40 codifies this in canon).
- §5.10 signoff: live-verified state per §19.6.
- A13 author frontmatter: only applies if A7 fold-in creates a new substrate-canon file with frontmatter (e.g., a manifest format-spec doc); otherwise no new A17-targets in Arc 40.
- A14 closure: 4 candidates close on ship (+ 6n9/t9u if folded); `[for: user-tier-polybius]` tag on stoa--utn.

## Self-application per A19 / stoa--bbi

Arc 40's structural fix (6wp canon) codifies what Arc 38 + Arc 39 already did organically. Note as N-evidence: structural-fix codification confirms an organically-held discipline, vs. requiring discovery.

## On dispatch close

Comment on stoa--utn with `[for: user-tier-polybius] [from: pliny-the-stoa]` tag carrying clean-PASS verdict + cleanup attestation per Arc 38/39 closure precedent. Then stand down; resume polling for Arc 41 dispatch signal.

## Recovery

If `/compact` or `/clear`: re-read this paste from `HUMAN_paste-pliny-arc-40-instruction.md` at project root (will archive to `substrate/arcs/arc-40/pastes/` per §5.11 at close). Fall back to `/resume` per handoff-author step 6 mandatory.
