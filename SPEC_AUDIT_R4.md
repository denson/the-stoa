# SPEC_AUDIT_R4 — fourth-pass audit of SPECIFICATION.md after R3 fold-in (NC6 + NC7)

**Status:** draft 2026-05-17, authored by project-tier POLYBIUS for the-stoa under the spec-audit R4 engagement (paste at `HUMAN_paste-polybius-spec-audit-r4-instruction.md`). Coordination ticket: `stoa--qlo`.

**Audience:** (1) PRINCIPAL for review; (2) user-tier POLYBIUS (the R3 fold-in author) for any follow-on edit.

**Discipline:** ARGUS-overlay — surface concerns; do **not** propose fixes. R4 is an *iteration audit* on commit `edd0de8` (NC6 back-ref propagation + NC7 bucketing-list restructure), not a fresh end-to-end audit.

**Scope under audit:**
- `SPECIFICATION.md` at commit `edd0de8` (post-fold-in; 701 lines after net -5 from R3 numbers).
- Live bw state (`bw list --status open --all` at 2026-05-17 ~21:25 MDT — 19 tickets including R4 coord `stoa--qlo`; 18 substrate-tracked).
- `git log` since R3 commit (`b858b92`).
- Per-R3-finding re-verification on `substrate/skills/handoff-author/SKILL.md` (NC2 R3 regression-check) + `docs/validation/stellation-SPECIFICATION.md` (X5/Y1 R3 regression-check) + §12.1 reference SHAs + bb12806 trailer carve-out.

**Method:** project-tier POLYBIUS single-seat-direct read of the fold-in commit `edd0de8` against R3's 2 new findings (NC6 + NC7) + 3 carryover △ items (C2 + M6 + W3), plus a fresh-eyes pass on the new ~10 lines of prose and a §13-walk-test for the dynamic-walk-of-§13 instruction's actionability. Live-verified bw open-ticket placement walk; live-verified `git log` reference SHAs + trailer states; live-verified SKILL.md + stellation-SPECIFICATION.md (R3-baseline holds). No CAPTAINs dispatched (R1+R2+R3 single-seat precedent; scope ~20 min).

**N=1 honesty (per op-disc §6.7.1):** R4 surfaces that the R3 fold-in correctly closes both R3 findings at their named scope — NC6's 5 back-reference cite-fixes are clean; NC7's option-b restructure removes the §12-side enumeration. The structural §12 staleness drift class is **fully closed at §12-level as the fold-in commit message claims** (no enumerations remain in §12.1-§12.5 that can drift when source-of-truth advances). One new latent surface introduced: §13.10 bullet 4 (one of the NC6 cite-fix targets) carries an enumeration "§13.5-§13.10 + §13.14" of which §13.x sections constitute the ticket-placement gap-list — the same drift mechanism the NC7 fix eliminated from §12.3 + §12.5, relocated to §13.10. The relocation is operationally softer than the original (§13.10 is the spec-recon pass whose explicit job is to be updated to current reality, vs §12 which should never drift) but the *structural drift class* is not zero. Honest meta-verdict: "fully closed at §12-level; relocated-but-softer-form latent mechanism at §13.10 bullet 4." The iteration cadence converged on a residual rather than a binary zero.

---

## Table of contents

1. [Per-R3-finding verification table (R4.1)](#per-r3-finding-verification-table-r41)
2. [Structural §12 drift class closure verification (R4.2)](#structural-12-drift-class-closure-verification-r42)
3. [New issues found (R4.3)](#new-issues-found-r43)
4. [Substrate-state re-check (R4.4)](#substrate-state-re-check-r44)
5. [Meta-verdict on the §12 staleness pattern (R4.5)](#meta-verdict-on-the-12-staleness-pattern-r45)
6. [Closing observation — meta-pattern across R1 + R2 + R3 + R4](#closing-observation--meta-pattern-across-r1--r2--r3--r4)

---

## Per-R3-finding verification table (R4.1)

Verdict legend: **✓** addressed correctly · **△** addressed with new concerns · **○** not addressed / partially addressed · **D** deliberately deferred.

### R3 NC6 — back-reference propagation (5 cite-fixes)

| Cite | R3 framing | Post-fold-in (verified) | Verdict |
|---|---|---|---|
| **§13.10 bullet 3 (line 578)** | "§12 (current state snapshot) updates ..." | "§12 (the structural definitions + queries) is verified consistent with the post-Pass-7 substrate state: the QUERIES in §12.1-§12.4 still return useful answers; the §12.5 dynamic-walk-of-§13 instruction still resolves correctly; reference SHAs in §12.1 still anchor to the intended commits." | ✓ |
| **§13.10 bullet 4 (line 579)** | "§12.5 ... shrinks as Passes close gaps ..." | "§13.5-§13.10 + §13.14 (which collectively constitute the ticket-placement gap-list per §12.5) reflect post-Pass-7 reality — closed Passes are marked DONE; open candidates have current tickets + scope notes; any newly-surfaced gap not already placed in §13.x gets a fresh ticket + a §13.x bucket assignment." | △ — see [NC8 (R4.3) below](#nc8--13.10-bullet-4-carries-new-13.x-enumeration--same-drift-mechanism-nc7-just-eliminated-relocated-to-13.10). The cite is rewritten to match §12's new shape (NC6 intent achieved), but the rewrite introduces a §13.x enumeration of the same drift class NC7 closed at §12. |
| **§13.11 bullets (lines 594-596)** | "matches §12.3 ... §12.4's catalogue ... §12.4's keep-list" | `bw list` bullet: "returns tickets all placed in some §13.x ticket-placing section per the §12.3 + §12.5 dynamic walk (no unplaced tickets surface as §12.x audit findings; the `--all` flag is load-bearing for completeness audits per §4.6 empirical anchor)." `git status` bullet: "shows no uncommitted changes except ignorable auto-modified state files (e.g., `.claude/.substrate-last-check`) per §12.4's clean-state definition." `_drafts/` bullet: "is empty OR contains only docs actively in use by an in-flight engagement per §12.4's clean-state definition." | ✓ All three mechanical-check items now reference §12.4's clean-state DEFINITION (not undefined "catalogue / keep-list"); `bw list` bullet uses dynamic-walk language. Mechanically operationalizable. |
| **§13.13 criterion 3 (line 646)** | "matches §12.4 catalogue" | "per §12.4's clean-state definition: `_drafts/` is empty or contains only docs for an in-flight engagement; `git status` shows no uncommitted changes except ignorable auto-modified state files; no accumulated cleanup debt." | ✓ Names §12.4's clean-state definition components explicitly. Self-contained criterion. |
| **§14 PRINCIPAL editing notes (line 697)** | "§12 Current state — corrections to what's shipped / open / in flight" | "§12 Current state — does the structural definitions + queries shape match how substrate state should be referenced from this spec? Any contracts in §12.1-§12.4 you want sharpened? Any queries that should be added / removed?" | ✓ Treats §12 as structural-contracts seat, not state-carrier. PRINCIPAL's edit invitation now matches §12's actual content. |

**R3 NC6 verdict tally: 4 ✓ + 1 △** (the △ at §13.10 bullet 4 is a NC6-intent-achieved-but-introduces-new-surface; see NC8 below).

### R3 NC7 — bucketing-list restructure (option b)

| Surface | R3 framing | Post-fold-in (verified) | Verdict |
|---|---|---|---|
| **§12.3 line 471** | "any open ticket NOT enumerated in §13.5-§13.8 + §13.9 + §13.10 is an unplaced ticket and surfaces as a §12.3 audit finding" | "Bucketing for the make-the-team-meet-the-spec workplan lives throughout §13. The canonical source-of-truth for which §13.x sections enumerate ticket placements is §13 itself — walk §13 end-to-end to find ticket placements; do NOT rely on a §12-side enumeration of which §13.x sections place tickets (such an enumeration would itself drift whenever new §13.x sections place tickets, as SPEC_AUDIT_R3 NC7 demonstrated empirically). For a current-time accounting of open-tickets-by-bucket: run `bw list --status open --all`; walk §13 looking for any section that enumerates ticket placements ... Any open ticket NOT placed in any §13.x section is an unplaced ticket and surfaces as a §12.3 audit finding (the spec is missing a bucket for it)." | ✓ Enumeration removed; dynamic-walk instruction in place; explicit warning against §12-side enumeration cites R3 NC7. |
| **§12.5 line 485-487** | Per-bullet enumeration (4 bullets pointing at §13.5-§13.8 + §13.9 + §13.10 + Post-spec future-work) + "walk each ticket against §13.5-§13.8 + §13.9 + §13.10's enumerations" | "The canonical gap list lives throughout §13 ... For a current accounting of which gaps exist + which are addressed by which §13.x section: walk all of §13 looking for sections that enumerate ticket placements (per SPEC_AUDIT_R3 NC7, do NOT rely on a §12-side enumeration ...). For the CURRENT list of gaps + their disposition: run `bw list --status open --all`; walk §13 looking for ticket-placing sections; cross-reference each open ticket against the union of §13.x placements. Any open ticket NOT placed in any §13.x section is a §12.5 audit finding (gap is real but not in the plan)." | ✓ Same shape as §12.3 fix; dynamic-walk; explicit NC7 cite. |

**R3 NC7 verdict tally: 2 ✓** (both §12 surfaces restructured cleanly).

### R3 △ carryovers (C2 + M6 + W3)

| R3 ID | Verdict | Verification |
|---|---|---|
| **C2 — §12 staleness drift class transformation** | △ → R4 closes this as the **R4.5 meta-verdict**. The R3 verdict was "the pattern *transformed* rather than fully closing"; this fold-in is the second iteration on the structural fix. The R4 verdict: **fully closed at §12-level**, with one residual relocated-but-softer surface at §13.10 bullet 4 (see NC8). See §5 below for full meta-verdict. | The R3 finding evolves to R4 verdict; not a carryover-untouched. |
| **M6 — stellation naming-ratification window "through Pass 9 completion"** | △ (unchanged from R2 + R3) | §13.12 line 610 still reads: *"PRINCIPAL may rename if preferred at dispatch time; ratification window stays open through Pass 9 completion."* Pass 9 = §13.11 (mechanical-check); Pass 10 = §13.12 (test-project dispatch). Read literally, the ratification deadline (Pass 9 completion) sits BEFORE the activity the rename most affects (Pass 10 dispatch) — internally consistent. The R2 "softer-form spread" persists. No fold-in touched this section; carryover unchanged. |
| **W3 — sequencing puts largest+most-mixed bundle (Arc 41, 5 candidates) last** | △ (unchanged from R2 + R3) | Workplan-shape feedback that PRINCIPAL did not pick to re-sequence. Unchanged at §13.7 + §13.8. Acceptable workplan-shape signal. |

### R3 verdict tally for R3-named items

| Verdict | Count | Items |
|---|---|---|
| ✓ addressed correctly | **6** | NC6 cite-fixes 1, 3, 4, 5; NC7 surfaces 1, 2 |
| △ addressed with new concerns | **3** | NC6 cite-fix 2 (§13.10 bullet 4 — introduces NC8 surface); M6 (carryover from R2+R3); W3 (carryover from R2+R3) |
| ○ not addressed / partially addressed | **0** | (None at the R3-named scope.) |

Total addressed-acceptably (✓ alone): **6** of 9 R3-named cite-or-surface items.
Total carrying concerns (△): **3** — 1 *new* (the §13.10 bullet 4 rewrite introduced a new latent surface; see NC8) + 2 *softer-form carryovers* (M6 + W3).

### R3 NC6 cite-fix 2 — finer characterization

The §13.10 bullet 4 rewrite IS NC6-intent-achieved (it removes "§12 as state-carrier" framing and re-targets the bullet to the §13.x ticket-placement gap-list). But the new prose *itself* enumerates which §13.x sections constitute the gap-list ("§13.5-§13.10 + §13.14") — the same drift mechanism NC7 was eliminating from §12.3 + §12.5. The fix-for-NC6 carries a new instance of the NC7 class of drift. Not a regression on NC6's intent; a side-effect of the rewrite. See NC8 in §3 for full write-up.

---

## Structural §12 drift class closure verification (R4.2)

The R4.2 checklist from the activation paste, applied directly:

### R4.2a — No state-snapshot content anywhere in §12.1-§12.5

✓ **PASS.** Walked §12.1 through §12.5 line by line.

- **§12.1 (line 439-448):** "What counts as shipped" + 3 git/gh queries + "Reference points for orientation (not authoritative; refresh via queries above for current state): Arc 35 ship `6414397`; Arc 36 v2 ship `fcd68c0`; Arc 37 ship `bb12806`." Reference SHAs explicitly disclaimed + serve substantive empirical-anchor role for §13.11 bb12806 carve-out. Acceptable per R3.2a's reference-points-with-disclaimer boundary; no change from R3.
- **§12.2 (line 450-460):** "What counts as in flight" + 4 queries. No enumerations.
- **§12.3 (line 462-471):** "What counts as open" + 3 bw queries + NEW dynamic-walk-of-§13 bucketing prose. **No enumeration of which §13.x sections place tickets** (the R3 NC7 surface is removed).
- **§12.4 (line 473-481):** "What counts as working-tree clean" + 4 queries + ignorable-churn carve-out. No enumerations; no change from R3.
- **§12.5 (line 483-489):** NEW shape — describes canonical gap-list as living throughout §13 + dynamic-walk instruction + CURRENT-list query. **No per-§13.x enumeration; no per-ticket enumeration; no per-arc enumeration.** The previous 4-bullet categorization (§13.5-§13.8 + §13.9 + §13.10 + Post-spec future-work) is REMOVED.

The R3 NC7 surface — the §13.x enumeration inside §12.3 + §12.5 — is now removed. No new enumeration introduced in §12.x.

### R4.2b — No back-references in §13.x / §14 / elsewhere that treat §12 as state-carrier

✓ **PASS** with one fine-grained observation.

Re-grepped for the R3 NC6 shape ("catalogue" + "keep-list" + "current state snapshot" + similar shape-of-state-snapshot language) across SPECIFICATION.md:

- `catalogue|keep-list|snapshot|current state snapshot` matches now occur ONLY at:
  - Line 433 (§12 heading): *"§12 Current state — structure + queries (derived views, not authored snapshots)"* — disclaimer-form usage, legitimate.
  - Line 435 (structural-change paragraph): *"§12 was previously authored as enumerated snapshots..."* — historical description of what changed; legitimate.
  - Line 460 (§12.2 end-clause): *"If all four return empty: nothing is in flight; the substrate is at a stable snapshot."* — describes substrate state semantics, NOT §12-as-state-carrier; legitimate.

**No surviving back-reference treats §12 as a state-carrying section.** NC6 propagation is structurally clean across the 5 cite locations + a sweep grep.

### R4.2c — The §12.3 + §12.5 dynamic-walk-of-§13 instruction is actionable

✓ **PASS.** Walked §13 myself end-to-end to find ticket placements; cross-referenced against live `bw list --status open --all` (18 substrate tickets); placed all 18:

| §13.x | Ticket-placing content | Tickets placed |
|---|---|---|
| §13.2 | Pass 1 housekeeping (DONE) | Historical closures only (stoa--vz9, stoa--cye, stoa--k03 — all closed). |
| §13.3 | Pass 2 Arc 36 v2 (DONE) | Historical closures + 1 follow-up: stoa--pqn (also placed at §13.8). |
| §13.4 | Pass 3 Arc 37 (DONE) | Historical closures only. |
| §13.5 | Pass 4 Arc 38 (3 candidates) | **stoa--ojz, stoa--bj5, stoa--gq1** |
| §13.6 | Pass 5 Arc 39 (2 candidates) | **stoa--utn, stoa--ezj** |
| §13.7 | Pass 6 Arc 40 (4 candidates) | **stoa--3sz, stoa--5sr, stoa--dhc, stoa--6wp** |
| §13.8 | Pass 7 Arc 41 (5 candidates) | **stoa--n2e, stoa--58b, stoa--3ml, stoa--ezp, stoa--pqn** |
| §13.9 | Deferred-with-gating (2 candidates) | **stoa--tvc, stoa--myd** |
| §13.10 | Pass 8 housekeeping inline-handled | **stoa--6k1** |
| §13.11 | Pass 9 mechanical-check (process) | — (no tickets) |
| §13.12 | Pass 10 behavioral validation (process) | — (no tickets) |
| §13.13 | Definition of done (criteria) | — (no tickets) |
| §13.14 | Explicitly out of scope | **stoa--lyw** (placed as "before-spec-met out-of-scope; invocation half operational for future arc after Pass 10") |
| §13.15 | Mode + dispatch (process) | — (no tickets) |
| §13.16 | Definition of done (criteria) | — (no tickets) |

**18 substrate tickets walked; 18 placed. lyw correctly resolves via §13.14 (the R3 NC7 false-positive is gone).** The walk is mechanically actionable without a §12-side hint about which §13.x sections to look at. A fresh team running the §12.3 + §12.5 query against the new prose finds all 18 placements.

### R4.2d — No new latent mechanisms introduced

△ **FAIL — one new latent surface.** See R4.3 NC8 below.

**The structural rewrite is small (10 insertions, 15 deletions across §12.3 + §12.5 + §13.10 + §13.11 + §13.13 + §14)**, and most of it is clean. The §13.10 bullet 4 rewrite (one of the NC6 cite-fixes) replaces the old "§12.5 ... shrinks" framing with a new "§13.5-§13.10 + §13.14 (which collectively constitute the ticket-placement gap-list per §12.5) reflect post-Pass-7 reality" framing. The new prose carries an enumeration of which §13.x sections place tickets — exactly the drift mechanism the NC7 fix at §12.3 + §12.5 was eliminating. The fix-for-NC6 introduces a new instance of the NC7-class of drift, in a different section.

The mechanism is real but is *softer than R3's NC7* on two axes:
1. **Scope:** the enumeration lives in §13.10 (the Pass 8 spec-recon checklist), not in the source-of-truth definition section (§12). §13.10's explicit job is to be updated when the spec drifts from reality.
2. **Severity:** the bullet's last clause ("any newly-surfaced gap not already placed in §13.x gets a fresh ticket + a §13.x bucket assignment") acknowledges that §13.x evolves — the enumeration reads as "current set at authoring time" rather than a hard query specification.

But it IS the same drift class structurally: if §13.17 ever places tickets (e.g., a future arc adds a new ticket-placing section), §13.10 bullet 4's enumeration would need to be updated to include §13.17, exactly as the original §12.3 + §12.5 enumeration would have needed updating to include §13.14.

See NC8 in §3 for the full write-up + fix-shape options.

---

## New issues found (R4.3)

R4 surfaces 1 new finding. The fold-in's NC6 + NC7 fixes correctly close their named scopes; the new surface is a side-effect of the NC6 cite-fix at §13.10 bullet 4.

### NC8 — §13.10 bullet 4 carries new §13.x enumeration ("§13.5-§13.10 + §13.14"), same drift mechanism NC7 just eliminated relocated to §13.10

**Category:** new latent surface introduced by the fold-in (relocated drift class).

**Cite:** §13.10 bullet 4 (line 579, in the Pass 8 spec-recon checklist):

> "§13.5-§13.10 + §13.14 (which collectively constitute the ticket-placement gap-list per §12.5) reflect post-Pass-7 reality — closed Passes are marked DONE; open candidates have current tickets + scope notes; any newly-surfaced gap not already placed in §13.x gets a fresh ticket + a §13.x bucket assignment."

**The drift mechanism.** The enumeration "§13.5-§13.10 + §13.14" claims, in its parenthetical, that these specific §13.x sections "collectively constitute the ticket-placement gap-list per §12.5." But §12.5 (the section this parenthetical references) explicitly says the *opposite*: "do NOT rely on a §12-side enumeration of which §13.x sections place tickets — such an enumeration would itself drift whenever new §13.x sections place tickets."

The §12.5 instruction warns against a §12-side enumeration; §13.10 bullet 4 carries the same shape enumeration in §13 instead. The structural drift mechanism the NC7 fix attempted to eliminate is now in §13.10.

**Why this is the same drift class.** If a future spec edit adds, say, a §13.17 that places tickets — exactly the kind of evolution the NC7 fix was designed to handle gracefully — the §13.10 bullet 4 enumeration would be incomplete (missing §13.17) until manually updated. This is the same shape of drift as the R3 NC7 false-positive on stoa--lyw at §13.14 (the original §12.3 + §12.5 enumeration was incomplete relative to §13.14 ticket placement).

**Why it's softer than R3's NC7.**
1. The enumeration lives in §13.10 (Pass 8 spec-recon), not §12 (source-of-truth definitions). §13.10's job is *to be updated* during each spec-recon pass; drift here is *expected and handled by execution*, vs §12 where drift was *unexpected and misleading to fresh teams*.
2. The bullet's last clause ("any newly-surfaced gap not already placed in §13.x gets a fresh ticket + a §13.x bucket assignment") acknowledges §13.x evolution — the enumeration reads more as a current-time scope hint than a hard query specification.
3. A fresh team executing Pass 8 against this bullet would naturally walk §13 end-to-end (per §12.5's dynamic-walk instruction), find any new ticket-placing sections, and update the bullet as part of the pass. The drift is detected + repaired within the pass.

**Why it's still a finding.**
1. The §12 fix-class shape is "structural eliminate the drift surface entirely." This bullet is "procedural — the drift is here but Pass 8 will catch it." That's a return to procedural-discipline, which the §4.6 TIRO + §27 mechanical/agent split + this §12 rewrite are *all* substrate principles arguing AGAINST.
2. A literal reader of §13.10 bullet 4 might treat the enumeration as authoritative ("Pass 8's scope is these specific sections") and miss new ticket-placing sections that emerged since authoring time. The §12.5 dynamic-walk instruction is in a sibling section, not co-located with the bullet — easy to miss.
3. The R3 NC7 finding's load-bearing claim was "the structural fix is incomplete in propagation if downstream sections re-encode the same enumeration." NC8 confirms that claim still holds: NC7's structural fix at §12 didn't fully propagate to §13.10's re-encoding.

**Fix-shape options (ARGUS-discipline — surfacing the option-space, not recommending).** Three reasonable shapes the fold-in author could choose:

- **(a) Apply NC7-class fix to §13.10 bullet 4:** rewrite the bullet to "walk §13 end-to-end per §12.5's dynamic-walk-of-§13 and verify each ticket-placing section reflects post-Pass-7 reality — closed Passes marked DONE; open candidates carry current tickets + scope notes; any newly-surfaced gap not already placed gets a fresh ticket + §13.x bucket assignment." Removes the enumeration; relies on the dynamic walk.
- **(b) Accept the relocated drift surface:** §13.10 IS the spec-recon pass; drift here is operationally handled. The cost of one bullet that needs occasional updating is low; the benefit of an explicit scope hint at authoring time is real.
- **(c) Promote the dynamic-walk to a §13-spanning property:** add a §13.10 lead-in that says "the dynamic-walk-of-§13 from §12.5 applies to this Pass 8 checklist — walk all of §13 looking for ticket-placing sections; bullet 4 below is the current-at-authoring-time scope hint."

PRINCIPAL + user-tier POLYBIUS own the fix-shape decision per ARGUS-discipline. The author of §13.10 bullet 4 chose to enumerate; if the substrate principle is "structural > procedural" (per §4.6 TIRO etc.), option (a) is the principled choice. If the substrate principle has a carve-out for spec-recon pass checklists, option (b) is acceptable. Option (c) is a middle path.

**Meta-pattern this surfaces.** R3's meta-claim was: "structural fixes narrow drift surface; full closure requires propagation discipline at fix-author time." R4 supports that claim with one more data-point: the R3 fold-in (the propagation pass) itself had a propagation gap (the §13.10 bullet 4 surface). The pattern recurs at one fewer level of abstraction each iteration but does not fully evaporate. See R4.5 meta-verdict + §6 closing observation.

---

## Substrate-state re-check (R4.4)

### Bw open-ticket count + dynamic-walk placement test

`bw list --status open --all` at 2026-05-17 ~21:25 MDT returns **19 tickets** (18 substrate + 1 R4 coord `stoa--qlo`):

| Ticket | P | §13.x placement (walked) | Verdict |
|---|---|---|---|
| stoa--bj5 | P2 | §13.5 (Arc 38 C2) | ✓ placed |
| stoa--ojz | P2 | §13.5 (Arc 38 C1) | ✓ placed |
| **stoa--qlo** | P2 | n/a (R4 coord, excluded by convention) | ✓ (operational, not substrate-canon) |
| stoa--utn | P3 | §13.6 (Arc 39 C1) | ✓ placed |
| stoa--3sz | P3 | §13.7 (Arc 40 C1) | ✓ placed |
| stoa--dhc | P3 | §13.7 (Arc 40 C3) | ✓ placed |
| stoa--5sr | P3 | §13.7 (Arc 40 C2) | ✓ placed |
| stoa--tvc | P3 | §13.9 (deferred-with-gating) | ✓ placed |
| stoa--ezj | P3 | §13.6 (Arc 39 C2) | ✓ placed |
| stoa--gq1 | P3 | §13.5 (Arc 38 C3) | ✓ placed |
| stoa--58b | P3 | §13.8 (Arc 41 C2) | ✓ placed |
| stoa--n2e | P3 | §13.8 (Arc 41 C1) | ✓ placed |
| stoa--6wp | P3 | §13.7 (Arc 40 C4) | ✓ placed |
| **stoa--lyw** | P3 | **§13.14** (out of scope; placed) | ✓ **R3 NC7 false-positive eliminated** — the dynamic-walk finds lyw at §13.14 |
| stoa--3ml | P4 | §13.8 (Arc 41 C3) | ✓ placed |
| stoa--ezp | P4 | §13.8 (Arc 41 C4) | ✓ placed |
| stoa--6k1 | P4 | §13.10 (Pass 8 inline-handled) | ✓ placed |
| stoa--myd | P4 | §13.9 (deferred-with-gating) | ✓ placed |
| stoa--pqn | P4 | §13.8 (Arc 41 C5) (also surfaced at §13.3 as Arc 36 v2 follow-up) | ✓ placed |

**18 substrate tickets; 18 placed.** The R3 NC7 false-positive (lyw) is resolved by the dynamic-walk. No new unplaced tickets surface. The query is mechanically actionable.

### Git log reference SHAs in §12.1 — no regression from R3

✓ All three SHAs resolve and match described arcs (re-verified post-R3-fold-in):
- `6414397` → "Arc 35: per-CAPTAIN git seat identity via Co-Authored-By trailer (stoa--kjo) (#15)" — trailers `[CAPTAIN_DAEDALUS_the-stoa; Claude Opus 4.7; CAPTAIN_ADA_the-stoa]` ✓
- `fcd68c0` → "Arc 36 v2: bundled coordination-hygiene canon (#16)" — trailers `[CAPTAIN_DAEDALUS_the-stoa; CAPTAIN_ADA_the-stoa; Claude Opus 4.7]` ✓
- `bb12806` → "Arc 37: ship 6-candidate substrate architecture canonification batch (#17)" — trailers **empty** ✓ (the §13.11 carve-out remains correctly anchored)

### bb12806 trailer carve-out (§13.11) — no regression from R3

✓ Verified `git log --pretty='%(trailers:key=Co-authored-by,valueonly,separator=; )' bb12806`: empty. §12.1's claim (bb12806 body carries empty `%(trailers)`) and §13.11's "EXPLICIT CARVE-OUT for bb12806" still anchor correctly to verifiable historical commit state.

### Working tree state — no regression from R3

`git status` shows: `M .claude/.substrate-last-check` (auto-modified by substrate-check skill on activation; matches §12.4's ignorable-churn carve-out + §13.11's "ignorable auto-modified state files" check). No other uncommitted changes. Clean per §12.4 + §13.13 criterion 3 definition.

### SKILL.md frontmatter + body agreement — no regression from R3

✓ `substrate/skills/handoff-author/SKILL.md` line 4 still reads: *"**Mandatorily** records the prior-generation session id for /resume per SPECIFICATION.md §10.1 generational-lineage architecture (recording is mandatory not optional per 2026-05-17 PRINCIPAL ratification of SPEC_AUDIT C1; if the session id is genuinely unrecoverable, explicitly note the truncation in the handoff)."*

Body step 6 line 44 still reads: *"Record prior-generation session id(s) for /resume (MANDATORY)."*

Frontmatter + body still agree. R3 NC2 fix holds.

### stellation-SPECIFICATION.md cross-refs — no regression from R3

✓ All four R3-verified cross-refs into SPECIFICATION.md still resolve:
- Line 3: "§13.12 (behavioral validation via test-project dispatch)" → resolves to §13.12 ✓
- Line 7: "§13.12 (Pass 10 behavioral validation)" → resolves to §13.12 ✓
- Line 217: "§13.12 Pass 10 observation trail" → resolves to §13.12 ✓
- Line 279: "§13.15 (Mode + dispatch)" → resolves to §13.15 ✓

R3 X5/Y1 fix holds.

### Git log since R3 commit (`b858b92`)

Three commits since R3 audit landed:
- `edd0de8` — R3 fold-in (the commit audited here).
- `0e56fae` — R4 activation pastes (the paste this engagement reads from).
- (this audit's eventual commit) — to be created on completion.

Chronology matches the activation paste's description. No surprise commits.

---

## Meta-verdict on the §12 staleness pattern (R4.5)

**Did the R3 fold-in fully close the §12 staleness drift class?**

**Fully closed at §12-level (as the fold-in commit message claims), with one residual relocated-but-softer-form latent mechanism at §13.10 bullet 4. The iteration cadence converged on a residual rather than a binary zero.**

Per the activation paste's R4.5 framing, three possible verdicts are offered:

> - **"Fully closed structurally"** — no current instance, no latent mechanism.
> - **"Still latent at <mechanism>"** — yet another surface exists where the pattern could recur.
> - **"Current instance found at <location>"** — the fix introduced a new instance OR an existing instance was missed.

**The honest R4 verdict: "STILL LATENT at §13.10 bullet 4 — softer than R3's NC7 because the surface is in the spec-recon pass whose job is to be updated, but the structural drift class is not zero."**

This is *not* "fully closed structurally" because the §13.10 bullet 4 enumeration is a real new latent surface introduced by the fold-in (see NC8). It is *not* "current instance found" because no false-positive currently exists (walking §13 with the bullet's enumeration matches `bw list` output; lyw is placed at §13.14 which the bullet's enumeration includes).

### What changed at R4 specifically

The R3 verdict was "STILL LATENT" with two surfaces: NC6 latent (back-references stale at 5 cites) + NC7 current (bucketing-list false-positive on lyw). The fold-in addresses both:

- **NC6 latent:** 4 of the 5 cite-fixes land cleanly. The 5th (§13.10 bullet 4) achieves NC6's intent (removes "§12 as state-carrier" framing) but introduces a new latent surface of the NC7 class. Net: NC6 closure is structurally clean at 4 of 5 cites; the 5th has a related residual.
- **NC7 current:** §12.3 + §12.5 enumerations REMOVED; dynamic-walk-of-§13 instruction landed; walking the dynamic-walk against live bw output finds all 18 substrate tickets including lyw at §13.14. Net: NC7 current-instance fully closed.

**The drift surface evolution across the audit cadence:**

| Pass | Drift surface size | Location | Operational shape |
|---|---|---|---|
| Pre-R2 | Huge | §12.1-§12.5 full snapshots (37 arcs listed; 18 tickets listed; commit history listed) | Source-of-truth definitions carry state; high-frequency drift |
| Post-R2 fold-in | Small | §12.3 + §12.5 single enumeration sentence | Source-of-truth definitions carry one residual state item; low-frequency drift; **R3 NC7 caught a current instance** |
| Post-R3 fold-in | Same size | §13.10 bullet 4 single enumeration sentence | Spec-recon pass checklist carries one residual state item; low-frequency drift; **R4 NC8 surfaces this as latent (no current instance)** |

The drift surface SIZE did not shrink between R2 and R3 fold-ins. The drift surface LOCATION moved — from §12 (source-of-truth) to §13.10 (spec-recon pass). The relocation is operationally softer (§13.10's job is to be updated when the spec drifts; §12 should never drift), but structurally the drift class is not zero.

### Compare to R1 + R2 + R3 patterns

- **R1 caught (commit `127f39b`):** §12.1/§12.2/§12.5 lagged substrate state; §12.3 was fresh. Pattern: §12 subsections out of sync with substrate + each other.
- **R2 caught (commit `4a12358`):** §12.3/§12.2 lagged post-W1-split; §12.5/§13.7/§13.8 were fresh. Same pattern at a different inflection.
- **R3 caught (commit `a1a10e4`):** §13.10/§13.11/§13.13/§14 back-references lagged §12's new structural shape; §12.3+§12.5 bucketing-list lagged §13.14 ticket placement. *Inverted-direction same pattern.*
- **R4 catches (commit `edd0de8`):** §13.10 bullet 4 (one of the NC6 cite-fixes) carries new §13.x enumeration of the same class NC7 closed at §12. *Same pattern relocated one section deeper.*

The underlying pattern that survives across all four passes: **when the source-of-truth boundary moves (substrate state, spec section structure, §13.x ticket placement, §12-vs-§13 state-carrier roles), the sections that re-encode any aspect of that source-of-truth drift unless every re-encoding is structurally redirected to the new boundary.**

Each fold-in narrowed the drift surface further:
- R2 fold-in shrunk §12 from full snapshots → single-sentence enumerations.
- R3 fold-in moved the residual enumeration from §12 to §13.10 (smaller-impact location).
- A hypothetical R4 fold-in could remove the §13.10 bullet 4 enumeration entirely (option (a) per NC8) — but the relevant question for substrate canon is whether the pattern will recur at a fifth level.

### The substrate principle test

The activation paste's R4 framing offered: *"If R4's meta-verdict is 'fully closed structurally,' that's substantial empirical signal for the substrate principle. ... If R4's verdict is 'still latent' or 'current instance,' the substrate principle needs refinement — possibly to 'structural fixes narrow drift surface but require propagation iteration to fully close.'"*

R4's verdict is "still latent" (softer-form). The substrate principle refinement R4 supports:

> **"Structural fixes succeed at narrowing the drift surface; full closure requires propagation discipline applied at fix-author time AND iteration to catch propagation gaps the fix-author missed. Each fold-in iteration that catches propagation gaps shrinks the drift surface further but may not fully eliminate the class — the residual converges on a fixed-point that is operationally acceptable rather than structurally zero."**

This is a more nuanced framing than the original "structural > procedural" framing implied. Both halves matter: structural fixes ARE meaningfully better than procedural fixes (R3 + R4 confirm the drift surface shrunk by an order of magnitude across iterations), AND propagation discipline at fix-author time is load-bearing (R3 caught what R2's fix missed; R4 caught what R3's fix missed; a hypothetical R5 might catch a residual the R4-recommended fix missed).

The empirical pattern across R1 → R4 is **convergence to a small residual, not zero**. That's still substantial progress; it's not the binary closure the original structural-fix framing implied.

---

## Closing observation — meta-pattern across R1 + R2 + R3 + R4

Four audits across two workdays on the same spec; one underlying pattern across all four; with meaningful diminishing-return convergence.

### The diminishing-finding pattern

| Pass | Total findings (new + carried) | New findings only | Drift surface (qualitative) |
|---|---|---|---|
| R1 | 49 (fresh-eyes; first-pass) | 49 | huge (§12 full snapshots) |
| R2 | 5 new (verified 49 R1) | 5 | medium (post-W1-split §12 enumerations) |
| R3 | 2 new (verified 13 R2 + carry R1) | 2 | small (single enumeration sentence at §12.3+§12.5) |
| **R4** | **1 new (verified 9 R3 + carry R2)** | **1** | **same-size single enumeration sentence relocated to §13.10 bullet 4** |

The new-finding count converged 49 → 5 → 2 → 1. The drift surface compressed from full snapshots → single enumeration → single enumeration (relocated). Iteration is producing diminishing returns; the audit is approaching a fixed point.

### The fixed-point question

Is the R4 NC8 residual the genuine asymptote of the iteration cadence — the point at which further fold-in iterations would either re-introduce a different residual elsewhere or accept the §13.10 bullet 4 surface as acceptable?

Two empirical predictions to discriminate:

1. **If a hypothetical R5 fold-in adopts NC8 option (a) — rewrite §13.10 bullet 4 to dynamic-walk language — does an R5 audit find another latent surface elsewhere?** If yes, the asymptote is at "one residual enumeration somewhere in the spec; the location moves but the count holds." If no, the iteration genuinely converges to zero.

2. **If PRINCIPAL + user-tier POLYBIUS accept NC8 option (b) — leave §13.10 bullet 4 as-is — does the §13.10 bullet 4 enumeration actually drift in practice?** Over the next 3-6 months as new §13.x sections potentially get added, does the bullet stay current via Pass 8 reconciliation, or does it accumulate stale enumerations that fresh teams have to work around?

Both predictions are testable. The substrate-principle refinement R4 supports doesn't depend on which way the discriminators land; it depends on whether the substrate continues to make progress on the pattern (either via fix-author propagation discipline or via operational tolerance of small drift surfaces).

### What R4 tells us about the iteration cadence as a discipline

R1 (49 findings) → R2 (5 new) → R3 (2 new) → R4 (1 new). The cadence is producing substantive value with diminishing-returns. Each pass closes the prior pass's findings and surfaces a smaller residual. The audit converges; the spec quality improves at each iteration.

The discipline itself — pre-arc spec-audit with ARGUS-discipline overlay; structural-fix-then-iterate-the-audit; surface-don't-fix at audit time; PRINCIPAL + user-tier POLYBIUS own fix-shape decisions — is validated by R1 → R4 as a working spec-quality method. The audit cadence is not "exhaustive on any single pass"; it's "iteratively convergent across multiple passes."

For Arc 38 dispatch decision: the R4 residual (NC8) is small enough that the spec can ship as-is (PRINCIPAL accepts option (b)) OR be fixed in a small R4 fold-in (option (a)) before dispatch. Either choice is defensible; the iteration cadence has converged enough that further audits would have diminishing returns.

The fix-shape decision for NC8 belongs to PRINCIPAL + user-tier POLYBIUS per ARGUS-discipline. R4 surfaces; R4 does not propose.

---

## Output discipline — closing notes

- **ARGUS-discipline:** surface, do not fix. No SPECIFICATION.md edits were made by this audit. Fix-shape decisions for NC8 (and any residual M6 + W3 carryovers) are PRINCIPAL + user-tier POLYBIUS authority.
- **N=1 honesty (per op-disc §6.7.1):** R4 confirms the §12 staleness pattern is *fully closed at §12-level* (the R3 fold-in commit message's claim is correct) with one residual relocated-but-softer-form latent surface at §13.10 bullet 4. This is N=4 of the iteration cadence across consecutive audits; the substrate-principle refinement R4 supports is "structural fixes narrow drift surface; propagation discipline + iteration close the residual asymptotically toward but not strictly at zero." Substrate-canon promotion of the refined principle remains future-arc work (multiple structural-fix arcs needed to test the asymptote prediction).
- **Single-checker boundary:** R4 was done single-seat-direct per R1+R2+R3 precedent (no ARGUS / CATO / BARTLEBY / ZENO sub-dispatch); the structural multi-checker step is PRINCIPAL + user-tier POLYBIUS review of this artifact.
- **Live-verification applied** (per §19.6 attestation discipline) to: `bw list --status open --all` (19 tickets including the R4 coord); §13-walk-test against the 18 substrate tickets (all 18 placed; lyw correctly resolved at §13.14); `git log` reference SHAs at §12.1 (Arc 35 / Arc 36 v2 / Arc 37) re-verified; `git log --pretty='%(trailers)'` on bb12806 + fcd68c0 + 6414397 re-verified (bb12806 carve-out still anchored); SKILL.md frontmatter line 4 + body step 6 line 44 (NC2 R3-baseline re-verified, no regression); stellation-SPECIFICATION.md cross-refs at lines 3 / 7 / 217 / 279 (X5/Y1 R3-baseline re-verified, no regression); §12 internal structure + §13.10 bullet 4 enumeration walk (R4.2 + NC8 verification); fold-in commit `edd0de8` diff stat (10 insertions / 15 deletions confirmed; +0 / -0 elsewhere — scope held to the named ~10-line surface).

[from: polybius-the-stoa]
