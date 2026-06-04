# Debloat decisions — operating-disciplines.md (+ Ariadne decoupling)

Settled decisions from working the debloat **decision surface** (`docs/debloat-decision-surface.html`) with the PRINCIPAL, 2026-06-04. This is the markdown=truth record that drives the execution arcs. **SETTLED** = locked; **OPEN** = awaiting PRINCIPAL. Recorded by user-tier POLYBIUS.

## Method (how these were reached)
- **Grounded, not from-memory:** a fan-out workflow had one agent read each section's real §-text before proposing a disposition. Grounding revised **11 of 34** from-memory calls, overwhelmingly toward KEEP — the from-memory pass was systematically too aggressive (it couldn't see that Arc 47 had already debloated ~8 sections to stubs).
- **Problem rows → the grounded disposition stands. Dilemma rows → the PRINCIPAL's value-call** (the surface refuses to fake a recommendation on those).
- Grounded mix, **final: 4 encode · 11 consolidate · 20 keep · 2 cut** (§1/§2/§3/§5 merge to one section; §4 carved out to KEEP standalone).

## Ariadne decoupling — SETTLED (scope A + optional C; leave B)

**Decision (PRINCIPAL, 2026-06-04):** Ariadne is an **optional, per-project add-on**, not part of base Stoa. Rationale: early on, Windows-git inefficiencies don't matter; eventually a corpus grows large regardless of platform, and at some point the hybrid search + knowledge graph (latest Ariadne) becomes necessary. So it's a scale-triggered add-on. **Base Stoa must not assume an Ariadne-ready environment** — it already knows how to take on additional tools (§23 base/custom, §31 component design). Remove the **assumptions**; keep the **provenance**.

**A — remove / de-name the assumptions (deployed substrate):**
- `operating-disciplines.md` **§21 "Ariadne-search-ready authoring" → CUT.** Its generic kernel (author for retrievability + compaction-recovery) is already covered by §30 + the handoff-author skill; fold a one-liner there only if a unique bit surfaces on read.
- `MAJOR_POLYBIUS.md` **§16.4 "Ariadne-search-ready authoring (forward discipline)" → CUT** (the POLYBIUS-specific twin of §21). Update the `templates/handoff-doc-template.md` §16.4 cross-ref accordingly.
- `operating-disciplines.md` **§16** ("Ariadne — semantic recall…") + `modules/bw-fit-matrix.md` framing (≈ lines 27, 32–35) **→ DE-NAME.** Keep the scale insight (write-side bw + an optional read-side projection); replace "Ariadne" with **"optional read-side projection add-on (hybrid search + KG)."** The specific tool name lives only in the Ariadne add-on's own docs.

**C — genericize example name-drops (optional, low value):** `MAJOR_POLYBIUS.md:576` (ingest-pipeline example), `operating-disciplines.md:43` (`ariadne--xxx` id-format example), `:1139` (`ariadne-core` slug example), `modules/multi-team-interop.md:27` + `modules/bw-upgrade.md:25` ("Railway-deployed Ariadne"), and the `handoff-doc-template.md` example content → swap for a generic placeholder.

**B — LEAVE, do NOT scrub:** every empirical-anchor citation (`ariadne--xxx` tickets, "originated in ariadne-core-workspace," PR #34, etc.). Provenance/evidence, not a dependency. Scrubbing them would falsify the substrate's own history.

> **Execution precision for the arc:** the A-vs-B split is per-LINE judgment. In `bw-fit-matrix.md`, de-name the *framing* (A) but KEEP the `stoa--vmc` anchor line (B). The directive must enumerate exact loci, not "remove Ariadne."

## The 37 dispositions (grounded)

- **ENCODE (4)** — partial: encode the mechanism, keep the judgment in prose.
  - §7 (POLYBIUS coordination → recurring cron-prompt), §11 (autonomous-mode setup → cron machinery in template), §13 (Windows PYTHONUTF8 → session-start env hook), §28 (git seat identity → ship/pre-commit hook; **keep §28.5 don't-infer-authorship as prose**).
- **CONSOLIDATE (11)** — **§1 + §2 + §3 + §5 → ONE merged anti-pattern-stance section (four stances).** Plus individual trims: §8, §15, §24, §26, §27, §31, §34.
- **KEEP (20)** — no-op. §0.5, **§4 (passivity — standalone; see RESOLVED below)**, §6, §9, §10, §12, §14, §16 (*keep but de-name per Ariadne-A*), §17, §18, §19, §20, §22, §23, §25, §29, §30, §33, §35, §36.
- **CUT (2)** — §32 (jsdom — delete the redundant stub; module already relocated), **§21 (Ariadne — per the decoupling decision above).**

Per-row why/recommendation + full §-text live in the surface HTML; this ledger is the settled-disposition index.

## RESOLVED — 37/37 decided (PRINCIPAL, 2026-06-04, via the surface)
- **§1 → CONSOLIDATE (merge), FOUR-stance.** §1/§2/§3/§5 merge into one anti-pattern-stance section.
- **§4 → KEEP, standalone** (carved out of the merge). Rationale (PRINCIPAL): passivity — "wait for explicit instruction" — is the anti-pattern agents (Claude included — PRINCIPAL: *"you do it all the time"*) violate **most often**, and the one that kills autonomous operation outright (an idle agent does zero work). It earns full, emphatic, standalone placement while the lesser stances merge.
- **Captured for the decision-surface skill:** within a cluster of similar rules, what decides merge-vs-keep is *which rule the team actually violates most* — keep the high-violation one emphatic, merge the rest. This is the exact signal I said I lacked when I first called §1 from memory.
- All other 33: grounded call stands; no vetoes.

## Execution — 3 arcs, dependency-ordered
All canon edits run as arcs (feature branch + directive), not direct commits — dispatched to the team (PLINY orchestrates the gauntlet) via bw under epic `stoa--xyb`.

**Arc A — Ariadne decoupling (A + optional C).** op-disc §21 (cut) + §16 (de-name); `MAJOR_POLYBIUS.md` §16.4 (cut); `modules/bw-fit-matrix.md` (de-name framing, KEEP the `stoa--vmc` anchor); `templates/handoff-doc-template.md` (cross-ref); optional-C genericizations. Self-contained; **first.**
**Arc B — op-disc prose consolidation.** four-stance merge (§1/§2/§3/§5; §4 untouched) + 7 trims (§8, §15, §24, §26, §27, §31, §34) + §32 stub cut. All prose to `operating-disciplines.md` (+ a couple modules). **After A** (both edit op-disc; avoid conflict).
**Arc C — encode batch.** §7 (recurring cron-prompt — depends on §34 trim from Arc B), §11 (cron machinery in the polling template), §13 (Windows PYTHONUTF8 session-start env hook), §28 (git-seat-identity ship/pre-commit hook — coordinate with `stoa--w6d`; KEEP §28.5 prose). Each = a running structure + a prose stub. **After B.**
KEEP (20): no-op, no arc.
