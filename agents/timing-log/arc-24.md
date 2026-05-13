# Arc 24 TIMING_LOG — comms-hygiene substrate DNA

**Engagement:** Arc 24 (stoa--cm3) — closes stoa--odh, stoa--nvl, stoa--ioy.
**Merged:** 2026-05-13 at commit `16146a4` (PR #4, squash). Builds on 7ecdbef (Arc 23 ship).
**Authored by:** Denson Smith. Orchestration: POLYBIUS (this session) + PLINY-stoa (terminal session, deleted post-confabulation).

---

## Estimate vs actual

| Phase | Estimate | Actual | Notes |
|---|---|---|---|
| Directive authoring (POLYBIUS) | ~30-45 min | ~25 min | Smaller than Arc 23 (3 tickets vs 8); reuse of Arc 23 directive template helped. |
| Ticket filing (POLYBIUS) | ~15 min | ~12 min | 3 ticket bodies authored in `_drafts/` then `bw create -d "$(cat ...)"`. |
| Activation paste + epic + dep-wiring | ~5-10 min | ~5 min | Mechanical. |
| Phase 1 design (DAEDALUS + ARGUS) | ~30-60 min | ~5 min from activation to surface | DAEDALUS produced design.md fast; ARGUS audit also fast. The terminal-session PLINY ran phases tighter than Arc 23. |
| Phase 2 ADA build | ~20-40 min | included in the 5-min interval | 4 commits, 14 files, 419 insertions. |
| Phase 3 verification (VERA + CATO + ZENO parallel) | ~15-30 min | ~5 min | 122 probes total at Phase 3 close (VERA 46 + CATO 50 + ZENO 11). |
| Phase 4 smoke + PR open | ~10-15 min | ~1 min | 7 smoke beats all green; PR #4 opened. |
| **Total Arc 24 build (gauntlet)** | **~1.5-3 hours** | **~5 min from dispatch to PR open** | |
| POLYBIUS disposition + merge close-out | ~10 min | ~10 min | Including 3 follow-up tickets + 1 confabulation-failure-mode ticket + this TIMING_LOG + epic close. |

**Two estimation-axis observations (per stoa--nax discipline that landed in Arc 23):**

- **Axis A (agent-team throughput):** wildly underestimated. The terminal-session PLINY ran the full gauntlet in ~5 minutes — substantially faster than Arc 23's ~30-min Phase 1 + ~30-min Phase 2-3 cadence. Possible factors: (1) smaller scope (3 tickets vs 8), (2) fresh CAPTAIN seats reading post-Arc-23 substrate with verification-complexity framework already available, (3) Python-vs-bash poll-loop choice was a one-shot pick rather than design iteration, (4) terminal Claude Code may have different latency characteristics than Desktop.

- **Axis B (upstream-substrate performance):** N/A — this arc was substrate-doc edits only, no upstream substrate at scale. The Axis B observation from Arc 23 (Conan-bulk-seed scaling wall) was already calibrated; Arc 24 didn't re-encounter it.

**Per nax discipline: these observations do NOT extrapolate to structural claims.** "The terminal PLINY is faster than the Desktop PLINY" is an N=1 anecdote, not a substrate truth. Future arcs may show different cadences; the discipline is to not enshrine this single observation as a rule.

## Substantive observations (not structural lessons)

1. **The terminal-session PLINY ran the gauntlet cleanly for real work.** Phase 1-4 heartbeats on stoa--cm3 between 00:06-00:11 UTC reflect competent execution. ADA built 14 files cleanly; all three verifiers PASSED with named follow-ups (none ship-blocking).

2. **Two architectural deviations from directive accepted within locked-shape scope:**
   - (a) Python poll-loop template instead of bash (B4 specified the SHAPE not the language; python is more portable; substantively equivalent).
   - (b) §18+§19 numbering for op-disc additions (consistent with Arc 23 §8.4/§8.5 pragma precedent).
   - (c) agent-author SKILL.md scope-inclusion (A7 left to DAEDALUS discretion).
   All three are honest interpretations within the directive's locked-shape scope; none required POLYBIUS surface for re-disposition.

3. **CATO returned 3 non-blocking follow-up items:** probe-spec needs ^last= anchor (stoa--3sz), python-vs-jq rationale single-source-of-truth lift (stoa--dhc), Edit-tool worktree-path discipline (stoa--5sr). All filed as substrate tickets for Arc 25+.

4. **The Anthropic agent-registry desync mid-flight** (between Arc 24 dispatch and post-restart resume) was a real Claude Code Desktop issue. PRINCIPAL deleted the desync'd session, fired a fresh terminal session with the same activation paste. Recovery was clean: fresh PLINY read stoa--cm3, saw the pre-existing state + my POLYBIUS BLOCKER ACK + the corrective comment on stoa--nvl, and resumed competently.

5. **The retrospective-narrative confabulation** at the end of the terminal session is the real failure-mode datapoint. After surfacing for ship/no-ship at 00:11 UTC and going idle for PRINCIPAL's response, PLINY later confabulated an "Engagement B shipped" narrative describing weeks-old already-merged work as fresh accomplishment. The actual fresh work (Arc 24 PR #4) shipped fine; only the post-completion narrative was confabulated. Filed as stoa--53u — distinct from stoa--ioy's general confabulation discipline because the shape is different (idle-state retrospective-narrative vs tool-call-state ambiguity).

6. **POLYBIUS performed the merge directly** rather than waiting for a fresh PLINY-stoa session. Per workspace convention "PLINY merges, not Denson clicks the button" — strict reading says PLINY should do it; pragmatic reading says any agent with auth + write access can. PRINCIPAL approved the pragmatic path. Worth noting: in deleted-PLINY situations, POLYBIUS handles the mechanical close-out itself rather than spawning a fresh PLINY just to run `gh pr merge`.

## What this arc shipped

- **operating-disciplines.md §18** — universal subagent-status-via-bw section (heartbeat + read-before-write + 60-min floor)
- **operating-disciplines.md §19** — confabulation-under-uncertainty discipline (canonical "uncertain, checking" + 3 equivalents)
- **MAJOR_PLINY.md §5.8** — canonical Python poll-loop template + orchestrator dispatch sequence + TaskOutput-forbidden-on-Agents
- **MAJOR_POLYBIUS.md §7.6** — cross-ref to PLINY's template + POLYBIUS-specific application
- **MAJOR_PLINY.md §7.2** — verify-then-execute scope broadened to general state-vs-claim mismatch (per stoa--ioy)
- **MAJOR_POLYBIUS.md §4.3** — confabulation discipline cross-ref
- **10 CAPTAIN role files** — heartbeat-and-read-before-write subsection in each; Monitor + run_in_background-true forbidden; per-CAPTAIN heartbeat-shape customization
- **substrate/skills/agent-author/SKILL.md** — voice-check row + procedure-step-3 bullet for heartbeat-discipline scaffold in new-CAPTAIN authoring

14 files / 419 insertions / 4 commits / 0 deletions. Authorship attribution A11 IMMUTABLE preserved (CATO verified zero author/owner/etc. field edits in diff).

## Cross-refs for future readers

- Arc 23 TIMING_LOG: `agents/timing-log/arc-23.md` (verification-complexity framework, predecessor arc)
- Arc 24 build directive: `substrate/arcs/arc-24-build-directive.md`
- Arc 24 PLINY activation paste: `HUMAN_paste-pliny-arc-24-instruction.md`
- Arc 24 design artifact (intermediate): `agents/design/arc-24/` (gitignored)
- Three Arc 24 children: stoa--odh, stoa--nvl, stoa--ioy (all closed)
- Three follow-up tickets: stoa--3sz, stoa--dhc, stoa--5sr (Arc 25+ candidates)
- Confabulation-failure-mode ticket: stoa--53u (P2, Arc 25 candidate)
- Coordination primer + role-file extracts drafts: `_drafts/coordination-primer-monitor-and-bw.md`, `_drafts/role-file-coordination-sections.md` (input material consumed by DAEDALUS in this arc)

---

End TIMING_LOG.
