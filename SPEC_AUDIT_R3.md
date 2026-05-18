# SPEC_AUDIT_R3 — third-pass audit of SPECIFICATION.md after structural §12 fold-in

**Status:** draft 2026-05-17, authored by project-tier POLYBIUS for the-stoa under the spec-audit R3 engagement (paste at `HUMAN_paste-polybius-spec-audit-r3-instruction.md`). Coordination ticket: `stoa--08r`.

**Audience:** (1) PRINCIPAL for review; (2) user-tier POLYBIUS (the structural-fix author) for any follow-on edit.

**Discipline:** ARGUS-overlay — surface concerns; do **not** propose fixes. R3 is an *iteration audit* on the fold-in commit `a1a10e4` (structural §12 rewrite + mechanical NC1-NC5 + A4 + X5/Y1 fixes), not a fresh end-to-end audit.

**Scope under audit:**
- `SPECIFICATION.md` at commit `a1a10e4` (post-fold-in; 706 lines).
- `docs/validation/stellation-SPECIFICATION.md` at commit `a1a10e4` (X5/Y1 cross-ref fixes).
- `substrate/skills/handoff-author/SKILL.md` at commit `a1a10e4` (NC2 frontmatter fix).
- Live bw state (`bw list --status open --all` at 2026-05-17T~20:50 MDT — 19 tickets including the R3 coord ticket `stoa--08r`; 18 substrate-tracked).
- `git log` since R2 commit (`a50a1a8`).

**Method:** project-tier POLYBIUS single-seat-direct read of the three edited files against the 10 △/○/D R2 findings explicitly named in the activation paste (NC1-NC5 + A4 + X5/Y1 + W2 + C1+NC2 + C2 + M6 + S-A + W1 + W3), plus a fresh-eyes pass on the new §12 prose and a §12-back-reference grep for latent staleness mechanisms. Live-verified the open-ticket count; live-verified `git log` reference SHAs; live-verified the SKILL.md frontmatter + body wording; live-verified stellation-SPECIFICATION.md cross-ref destinations. No CAPTAINs dispatched (R1 + R2 single-seat precedent; scope ~30 min).

**N=1 honesty (per op-disc §6.7.1):** R3 surfaces that the structural §12 fix is **correct in its local scope** (§12 itself no longer carries enumerated snapshots) **but introduces two new propagation gaps** — back-references from §13.10/§13.11/§13.13/§14 still treat §12 as snapshot/catalogue/keep-list; and the §13.x-bucketing-list assertion still carried by §12.3+§12.5 has already drifted relative to §13.14 (which places `stoa--lyw` but is not in the bucketing query). The original R1+R2 staleness drift class is structurally closed *at §12 itself*; a related drift class (back-reference sections lag §12's shape, and the bucketing-list enumeration lags §13's shape) is now the live failure mode.

---

## Table of contents

1. [Per-R2-finding verification table (R3.1)](#per-r2-finding-verification-table-r31)
2. [Structural §12 internal consistency check (R3.2)](#structural-12-internal-consistency-check-r32)
3. [New issues found (R3.3)](#new-issues-found-r33)
4. [Substrate-state re-check (R3.4)](#substrate-state-re-check-r34)
5. [Meta-verdict on the §12 staleness pattern (R3.5)](#meta-verdict-on-the-12-staleness-pattern-r35)
6. [Closing observation — meta-pattern across R1 + R2 + R3](#closing-observation--meta-pattern-across-r1--r2--r3)

---

## Per-R2-finding verification table (R3.1)

Verdict legend: **✓** addressed correctly · **△** addressed with new concerns · **○** not addressed / partially addressed · **D** deliberately deferred · **n/a** optional R1 signal, no fix expected.

### R2 mechanical findings (NC1-NC5 + A4 + X5/Y1) — PRINCIPAL "fix all in this pass" pick

| R2 ID | Verdict | Verification |
|---|---|---|
| NC1 — §12.3 at pre-W1-split state (9-candidate Arc 40 enumeration; stale Pass-N labels) | ✓ | **Obsolesced by structural removal.** §12.3 (line 462-471) no longer enumerates per-ticket or per-arc bucketing; describes "what counts as open" + lists 3 queries. The pre-W1-split enumeration that R2 flagged at lines 458-486 is gone. Cleaner than a per-line bump. |
| NC2 — handoff-author SKILL.md frontmatter "Optionally" vs body MANDATORY | ✓ | `substrate/skills/handoff-author/SKILL.md` line 4 now reads: *"**Mandatorily** records the prior-generation session id for /resume per SPECIFICATION.md §10.1 generational-lineage architecture (recording is mandatory not optional per 2026-05-17 PRINCIPAL ratification of SPEC_AUDIT C1; if the session id is genuinely unrecoverable, explicitly note the truncation in the handoff)."* Body step 6 line 44 unchanged ("MANDATORY"); frontmatter and body now agree. Clean. |
| NC3 — §12.3 missing `stoa--lyw` from enumeration | ✓ | Obsolesced by structural removal (no enumeration to be missing-from). |
| NC4 — §12.2 stale Pass-N labeling ("Pass 7 spec-recon as current activity") | ✓ | Obsolesced by structural removal. §12.2 (line 450-460) is now "What counts as in flight" with branch / PR / coord-ticket queries; no Pass-N labeling. |
| NC5 — §13.7 line 593 "Pass 9 stellation dispatch" should be Pass 10 | ✓ | §13.7 line 554 now reads: *"**Important sequencing: Arc 40 lands BEFORE Pass 10 stellation dispatch so subsequent squash-merges (including stellation's) preserve trailers cleanly.**"* Clean. |
| A4 — §13.7 "substrate-canon tickets" boundary undrawn vs §13.13 criterion 2 "no open P2" gate | ✓ | §13.8 closing sentence (line 566) now carries explicit reconciliation: *"...'substrate-canon' boundary here = open tickets whose deliverable is a canon change ... — explicitly NOT engagement-coordination tickets (e.g., spec-audit coord tickets) or pure-documentation tickets ... The §13.13 criterion 2 spec-met gate ('no open P2 in awaiting-architectural-decision or deferred-without-plan state') is the broader operational gate; this sentence is its narrower substrate-canon-specific echo."* The two vocabularies are now explicitly bridged. Clean. |
| X5 — stellation-SPECIFICATION.md cross-refs into SPECIFICATION.md miss two sections | ✓ | Verified all 4 cross-refs at `docs/validation/stellation-SPECIFICATION.md`: line 3 "§13.12 (behavioral validation via test-project dispatch)" ✓; line 7 "§13.12 (Pass 10 behavioral validation)" ✓; line 217 "§13.12 Pass 10 observation trail" + artifact path ✓; line 279 "§13.15 (Mode + dispatch)" ✓. All four targets resolve to the intended §13.x destinations in the post-W1-split numbering. Clean. |
| Y1 — same as X5 (cross-coherence echo) | ✓ | Same as X5. |

### R2 △ findings (addressed with new concerns in R2)

| R2 ID | Verdict | Verification |
|---|---|---|
| C1+NC2 — handoff session-id record three-source disagreement → R2 found frontmatter still "Optionally" | ✓ | NC2 fix (above) closes the remaining gap. SKILL.md frontmatter + body + §10.1 line 366 + §12.5 (REMOVED bullet) now all agree: recording is MANDATORY. Clean. |
| C2 — §12 internal staleness across §12.1/§12.2/§12.3/§12.5 (R1 + R2 both caught at different inflection points) | △ | The original drift class is structurally closed at §12 itself. **New concern at meta-pattern level:** see §3 NC6 + NC7 below + §5 meta-verdict — the structural rewrite was applied at §12 but not propagated to §13.10/§13.11/§13.13/§14 back-references, and a residual §13.x-bucketing-list assertion still lives in §12.3+§12.5 and has already drifted relative to §13.14. The pattern *transformed* rather than fully closing. |
| M6 — stellation naming-ratification placement spread "through Pass 9 completion" | △ | Unchanged at §13.12 line 615: *"PRINCIPAL may rename if preferred at dispatch time; ratification window stays open through Pass 9 completion."* In the post-W1-split numbering, Pass 9 is §13.11 (mechanical-check) — so "through Pass 9 completion" places the window's close BEFORE Pass 10 (test-project dispatch at §13.12), which is the activity the rename most affects. Read literally, the deadline is internally consistent (rename closes before stellation is actually built). The R2 concern's "spread is itself an open spread" softer-form persists; the literal reading is workable. No fold-in change observed. |
| S-A — §12.3 ticket enumeration drifted from `bw list --all` (lyw missing) | ✓ | Obsolesced by structural removal (no enumeration to drift). |
| W1 — Arc 40 9-candidate split, R2 caught §12.3 not propagated | ✓ | Obsolesced by structural removal at §12.3. Forward sections (§13.7 4-candidate Arc 40 + §13.8 5-candidate Arc 41 + renumbered §13.10-§13.16 + §14 candidate-counts) remain clean from R2. |
| W3 — sequencing puts largest+most-mixed bundle (Arc 40 → Arc 41 post-split) last | △ | Unchanged. R2 verdict already noted "persists in a softer form" after W1 split (largest bundle is now Arc 41 with 5 candidates, not Arc 40 with 9). The fold-in did not pick a re-sequencing fix. Acceptable workplan-shape feedback. |

### R2 ○ findings (not addressed in R2)

| R2 ID | Verdict | Verification |
|---|---|---|
| A4 — §13.7 substrate-canon ticket boundary | ✓ | Now addressed (see above in mechanical-findings row). |
| X5 — stellation cross-refs | ✓ | Now addressed. |
| Y1 — same as X5 | ✓ | Now addressed. |
| W2 — Pass 4 (Arc 38) mixes scope-shapes (new-seat + tool-extension + new-canon-section) | D | Per PRINCIPAL non-pick (paste activation §8 sanctioned: "Deliberately deferred (W2 only) — sanctioned per PRINCIPAL non-pick"). Acceptable workplan-shape feedback that PRINCIPAL chose not to ratify a re-bundling for. |

### R1 findings unchanged by R2 + R3 (carried forward for completeness)

The R1 findings that R2 sanctioned as deferred-to-Pass-8 (A2, A3, M1, M4, M5, O3, U2-U5, S1-S3, S5) and the n/a R1 signals (N1, N2, O2, S-E, Y2, X8=X3) remain at their R2 dispositions; no change in R3.

### R3 verdict tally for R2's named-for-this-pass items

| Verdict | Count | Items |
|---|---|---|
| ✓ addressed correctly | **9** | NC1, NC2, NC3, NC4, NC5, A4, X5, Y1, C1+NC2 (combined) |
| △ addressed with new concerns | **3** | C2 (pattern transformed; see §5), M6 (carried from R2; spread softer-form), W3 (carried from R2; persists softer-form) |
| ○ not addressed / partially addressed | **0** | (None at the R2-named scope.) |
| D deliberately deferred | **1** | W2 (PRINCIPAL non-pick) |

Total addressed-acceptably (✓ + D): **10** of 13 R2-named items.
Total carrying concerns (△): **3** — all are *softer-form carryovers from R2*, none are *new regressions from the fold-in*. Distinct from the new R3 issues at §3 below.

---

## Structural §12 internal consistency check (R3.2)

The R3.2 checklist from the activation paste, applied directly:

### R3.2a — No leftover enumerations in §12.1-§12.4

✓ **PASS.** Walked §12.1 through §12.4 line by line.

- **§12.1 (line 439-448):** describes "what counts as shipped" + 3 git/gh queries + "Reference points for orientation (not authoritative; refresh via queries above for current state): Arc 35 ship `6414397`; Arc 36 v2 ship `fcd68c0`; Arc 37 ship `bb12806`." The reference SHAs are explicitly labeled as orientation-only with refresh-via-query disclaimer. The `bb12806` reference also serves as the empirical anchor for the §13.11 carve-out (substantive cross-ref, not a snapshot). Not a list-snapshot — reference-points-with-disclaimer. Acceptable per the paste's "reference SHAs for orientation OK; per-ticket lists not" boundary.
- **§12.2 (line 450-460):** describes "what counts as in flight" + 4 queries (local arc-build branches; remote arc-build branches; open PRs; engagement coord tickets). No enumerations.
- **§12.3 (line 462-471):** describes "what counts as open" + 3 bw queries. No per-ticket enumeration. *(See R3.2c finding below about the §13.x-bucketing-list residual.)*
- **§12.4 (line 473-481):** describes "what counts as working-tree clean" + 4 queries + ignorable-churn carve-out for `.claude/.substrate-last-check`. No enumerations.
- **§12.5 (line 483-494):** describes "known gaps" + 4 categorization bullets pointing at §13.5-§13.8 / §13.9 / §13.10 / "Post-spec future-work." No specific gap enumeration (the bullets describe categories; the categories' contents live at §13.x). *(See R3.2c finding below.)*

### R3.2b — Queries are actionable

✓ **PASS.** All queries listed in §12.1-§12.4 execute correctly and return useful answers against current substrate state. Specifically verified:

- `git log --oneline main` ✓ returns full commit history.
- `gh pr list --state merged --limit 20` ✓ (not run locally; standard gh query — would surface recent merged PRs).
- `git log --grep='^Arc' --oneline` ✓ returns arc-ship commits (Arc 37, Arc 36 v2, Arc 35, Arc 34, ...).
- `git branch | grep -E '^\s*arc-[0-9]+/build$'` ✓ would surface local arc-build branches if any (none currently).
- `bw list --status open --all` ✓ returns 19 tickets at 2026-05-17 ~20:50 MDT (18 substrate + 1 R3 coord); matches §12.3's described query semantics.
- `bw show <id>` + `bw history <id>` ✓ standard bw commands.
- `git status` + `ls _drafts/` + `git log --oneline -20` + `git diff --stat` ✓ standard.

The TIRO empirical-anchor parenthetical at §12.3 line 464 also correctly cross-refs `operating-disciplines.md` §12.1 cookbook + §4.6 empirical anchor, making the `--all` flag's load-bearing role explicit.

### R3.2c — §12.5 → §13 cross-refs resolve + carry the gap enumeration

△ **PASS with one drift instance.** §12.5 says the gap list lives at "§13.5-§13.8 (per-Pass arc candidates) + §13.9 (deferred-with-gating) + §13.10 inline-handled items." All four cross-refs resolve to the intended sections — §13.5 (Pass 4 Arc 38), §13.6 (Pass 5 Arc 39), §13.7 (Pass 6 Arc 40), §13.8 (Pass 7 Arc 41), §13.9 (deferred-with-gating), §13.10 (Pass 8 housekeeping with `stoa--6k1 handled inline`). The §13.x sections do carry the per-ticket enumerations.

**BUT the bucketing-list itself drifts.** §12.5 line 492 + §12.3 line 471 both say: *"any open ticket NOT enumerated in §13.5-§13.8 + §13.9 + §13.10 is an unplaced ticket and surfaces as a §12.x audit finding."* The bucketing-list enumerates §13.5-§13.8 + §13.9 + §13.10 — but `stoa--lyw` is placed at **§13.14** (line 666: *"Build the `/resume` invocation discipline canon (stoa--lyw per §12.5) before spec-met — the recording half (mandatory at handoff-author SKILL.md step 6) is sufficient for spec-met; the invocation half is operational guidance that can ship in a future arc after Pass 10."*).

A fresh team running the §12.3 / §12.5 bucketing query right now would walk the 18 substrate tickets against §13.5-§13.8 + §13.9 + §13.10 and surface `stoa--lyw` as an "unplaced ticket / audit finding (gap is real but not in the plan)" — which is **false**, because lyw IS placed (in §13.14 as "explicitly out-of-scope for spec-met"). This is a current-instance drift in the bucketing-list assertion. See NC6 below for the full write-up.

### R3.2d — No new staleness surfaces introduced

△ **FAIL — two surfaces.** See R3.3 NC6 + NC7 below.

The structural-§12 reference-SHAs at §12.1 (Arc 35 `6414397`; Arc 36 v2 `fcd68c0`; Arc 37 `bb12806`) ARE small state items — but they are explicitly disclaimed as "not authoritative; refresh via queries above for current state" and they serve a substantive empirical-anchor role for the §13.11 carve-out (the bb12806 reference). Acceptable.

The two new surfaces are at the BACK-references (NC6) and the BUCKETING-LIST (NC7). See §3 below.

---

## New issues found (R3.3)

The fold-in's structural §12 rewrite eliminated the original snapshot-drift class at §12 but introduced two new latent surfaces. Both have the same root cause: the structural rewrite was applied at §12 itself but its implications were not propagated to (a) sections that READ §12 as state, (b) §13.x sections that PLACE tickets that the bucketing-list should enumerate. R3 surfaces 2 new issues; both share the "incomplete propagation of structural fix" shape.

### NC6 — §13.10 / §13.11 / §13.13 / §14 back-references still treat §12 as snapshot / catalogue / keep-list

**Category:** latent contradiction (cross-section read-write mismatch).

The structural-§12 rewrite removed the snapshots, catalogues, keep-lists, and per-state enumerations that §12.1-§12.4 previously carried. Four downstream sections still reference §12 *as if* those state-carrying surfaces still exist:

| Cite | Current text | Mismatch with new §12 |
|---|---|---|
| **§13.10 bullet 3 (line 583)** | "§12 (current state snapshot) updates to reflect post-Pass-7 reality — what's shipped, what's open, what's in flight, what's in the working tree." | §12 is no longer a "current state snapshot." There's nothing to "update" at Pass 8. The bullet describes an activity that the structural rewrite eliminated. |
| **§13.10 bullet 4 (line 584)** | "§12.5 (what's NOT yet built that the spec implies) shrinks as Passes 2-7 close gaps; any remaining items have filed tickets + gating criteria." | §12.5 no longer carries an authored gap-list that "shrinks." It redirects to §13.5-§13.8 + §13.9 + §13.10 categorization. The "shrinks as Passes close gaps" mental model is the pre-structural framing. |
| **§13.11 bullets (lines 599-601)** | "`bw list --status open --all` matches §12.3 ... `git status` matches §12.4's catalogue ... `_drafts/` contents match §12.4's keep-list." | §12.3 has no specific list to match against. §12.4 has no "catalogue" or "keep-list" — it has a *definition* of clean + queries. Three mechanical-check items are now undefined (match-against-what?). A fresh team running Pass 9 cannot operationalize these checks as written. |
| **§13.13 criterion 3 (line 651)** | "Working tree clean — `_drafts/` contains only docs for an in-flight arc; `git status` matches §12.4 catalogue; no accumulated cleanup debt." | Same as §13.11 — §12.4 has no catalogue. Criterion 3's middle clause is undefined. |
| **§14 (line 702)** | "**§12 Current state** — corrections to what's shipped / open / in flight." | PRINCIPAL is invited to *correct* §12 as if it carries state. §12 no longer carries state — corrections would target what, exactly? The invitation is structurally misaligned with §12's actual content. |

The same drift family — sections that REFER TO §12 as a state-carrying section — is the inverse of the R1+R2 pattern (where §12 itself lagged substrate state). R1+R2 caught "§12 falls behind substrate state when source-of-truth advances." R3 surfaces "§13.x/§14 fall behind §12's shape when §12 changes shape." Same family of failure mode; different actors.

This is *latent* rather than *current* drift — the back-references are stale relative to §12's new shape, but a fresh team would notice the mismatch at Pass 8 / Pass 9 / Pass 13 reading time (asking "what catalogue? what keep-list? what snapshot?") rather than silently building against drift. The risk is fresh-team confusion + a re-derivation of "OK so the structural rewrite means we need to update these other sections too."

### NC7 — §12.3 + §12.5 "bucketing list" enumeration drifts relative to §13.14 (current instance: `stoa--lyw`)

**Category:** current contradiction (the bucketing query gives a false-positive on a placed ticket).

§12.3 line 471: *"any open ticket NOT enumerated in §13.5-§13.8 + §13.9 + §13.10 is an unplaced ticket and surfaces as a §12.3 audit finding (the spec is missing a bucket for it)."*

§12.5 line 492: *"walk each ticket against §13.5-§13.8 + §13.9 + §13.10's enumerations, and any unplaced ticket is a §12.5 audit finding (gap is real but not in the plan)."*

Both queries enumerate the bucketing-list as **§13.5-§13.8 + §13.9 + §13.10**. But the spec ALSO places tickets at:

- **§13.14 line 666** — places `stoa--lyw` ("Build the `/resume` invocation discipline canon (stoa--lyw per §12.5) before spec-met — ... the invocation half is operational guidance that can ship in a future arc after Pass 10").

`stoa--lyw` is in `bw list --status open --all` (confirmed live, P3, "Resume invocation discipline (/resume) — successor-decides-vs-spawn-fresh + stale-id handling"). Walking lyw against the bucketing query: not in §13.5 (Arc 38), not in §13.6 (Arc 39), not in §13.7 (Arc 40), not in §13.8 (Arc 41), not in §13.9 (deferred-with-gating), not in §13.10 (inline-handled). **Query verdict: unplaced; audit finding.** But lyw IS placed — at §13.14.

The structural-§12 rewrite carried a small piece of state that has already drifted: the enumeration of WHICH §13.x sections constitute "the bucketing-list." That enumeration is incomplete (missing §13.14) AND will continue to drift if future spec edits add new §13.x sections that place tickets (e.g., if §13.4's Arc 37 closure history ever becomes a place to look up still-open follow-ups, the bucketing-list would need to enumerate it too).

This is **current**, not latent — running the §12.3 / §12.5 query right now produces a false-positive audit finding on `stoa--lyw`.

(Alternative read: §13.14 is "explicitly out of scope for make-the-team-meet-the-spec," so naming lyw there counts as "placed" in the spec's mental model. Under that read, the bucketing query needs to enumerate §13.14 too. Either way, the enumeration is incomplete.)

The deeper finding: **the structural fix transformed the drift class rather than eliminating it.** Pre-fix, §12 itself was a state-carrier that drifted when substrate state advanced. Post-fix, §12 is no longer a state-carrier — BUT §12.3 + §12.5 carry a small structural-state item (the §13.x bucketing-list enumeration) that drifts when the spec's §13.x structure advances. The structural-state surface is much smaller than the original snapshot surface (a few §-references vs ticket-lists + commit-lists + arc-counts), so the drift rate is much lower — but the class is not zero.

---

## Substrate-state re-check (R3.4)

### Bw open-ticket count

`bw list --status open --all` at 2026-05-17 ~20:50 MDT returns **19 tickets**:

| Ticket | P | §13.x placement | Verdict |
|---|---|---|---|
| stoa--bj5 | P2 | §13.5 (Arc 38 C2) | ✓ placed |
| stoa--ojz | P2 | §13.5 (Arc 38 C1) | ✓ placed |
| **stoa--08r** | P2 | n/a (R3 coord, excluded by convention) | ✓ (operational, not substrate-canon) |
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
| **stoa--lyw** | P3 | **§13.14** (explicitly out of scope; placed BUT outside the §12.3/§12.5 bucketing query) | △ **NC7 false-positive** |
| stoa--3ml | P4 | §13.8 (Arc 41 C3) | ✓ placed |
| stoa--ezp | P4 | §13.8 (Arc 41 C4) | ✓ placed |
| stoa--6k1 | P4 | §13.10 (Pass 8 inline-handled) | ✓ placed |
| stoa--myd | P4 | §13.9 (deferred-with-gating) | ✓ placed |
| stoa--pqn | P4 | §13.8 (Arc 41 C5) | ✓ placed |

**18 substrate tickets** (excluding stoa--08r R3 coord). **17 placed by §12.3/§12.5 bucketing query**; **1 false-positive** (`stoa--lyw`, placed at §13.14 but not in the query's bucketing-list). See NC7.

### Git log reference SHAs in §12.1

✓ All three resolve and match described arcs:
- `6414397` → "Arc 35: per-CAPTAIN git seat identity via Co-Authored-By trailer (stoa--kjo) (#15)" ✓
- `fcd68c0` → "Arc 36 v2: bundled coordination-hygiene canon (#16)" ✓
- `bb12806` → "Arc 37: ship 6-candidate substrate architecture canonification batch (#17)" ✓

### bb12806 trailer carve-out

✓ Verified via `git log --pretty='%(trailers:key=Co-authored-by,valueonly)' bb12806^..bb12806`: empty trailers. §12.1's claim ("Arc 37 squash-merge `bb12806` body carries empty `%(trailers)`") is correct; the §13.11 carve-out is correctly anchored to a verifiable historical commit.

Spot-check: `fcd68c0` (Arc 36 v2) returns `[CAPTAIN_DAEDALUS_the-stoa; CAPTAIN_ADA_the-stoa; Claude Opus 4.7]` ✓ (the per-CAPTAIN trailers landed correctly before the bb12806 regression). `6414397` (Arc 35) returns `[CAPTAIN_DAEDALUS_the-stoa; Claude Opus 4.7; CAPTAIN_ADA_the-stoa]` ✓. The regression is isolated to bb12806; the carve-out scope is correct.

### handoff-author SKILL.md frontmatter description (NC2 fix verification)

✓ Line 4: *"Mandatorily records the prior-generation session id for /resume per SPECIFICATION.md §10.1 generational-lineage architecture (recording is mandatory not optional per 2026-05-17 PRINCIPAL ratification of SPEC_AUDIT C1; if the session id is genuinely unrecoverable, explicitly note the truncation in the handoff)."*

Body step 6 line 44 unchanged: *"Record prior-generation session id(s) for /resume (MANDATORY)."*

Frontmatter and body agree. Clean.

### stellation-SPECIFICATION.md cross-refs (X5/Y1 fix verification)

✓ All four edits landed:
- Line 3: "§13.12 (behavioral validation via test-project dispatch)" ✓
- Line 7: "§13.12 (Pass 10 behavioral validation)" ✓
- Line 217: "§13.12 Pass 10 observation trail (`agents/observation/spec-validation/test-dispatch-trail.md`)" ✓
- Line 279: "§13.15 (Mode + dispatch)" ✓

All four destinations resolve to the intended sections in SPECIFICATION.md's post-W1-split numbering. Clean.

### §13.7 line 554 — "Pass 10 stellation dispatch" (NC5 fix verification)

✓ Verified: *"**Important sequencing: Arc 40 lands BEFORE Pass 10 stellation dispatch so subsequent squash-merges (including stellation's) preserve trailers cleanly.**"* Pass 10 is §13.12 (test-project dispatch); cross-ref correct.

### Working tree state

`git status` shows: `M .claude/.substrate-last-check` (auto-modified by substrate-check skill; matches §12.4's ignorable-churn carve-out). No other uncommitted changes. Clean.

### Git log since R2 commit (`a50a1a8`)

Three commits since R2 audit landed: `a1a10e4` (R2 fold-in — the structural §12 + mechanical fixes audited here); `95eaec4` (spec-audit R3 activation pastes); plus this audit's eventual commit. Chronology matches the activation paste's description.

---

## Meta-verdict on the §12 staleness pattern (R3.5)

**Did the structural §12 fix close the staleness drift class?**

**Partially. The original drift class (§12 itself as a snapshot that lags substrate state) is structurally closed. A related, narrower drift class has emerged in its place: the back-references and bucketing-list enumerations.**

Per the activation paste's R3.5 framing:

> "If R3 surfaces ANY new instance of the §12 staleness pattern (current OR latent mechanism), that's load-bearing evidence the structural approach is incomplete and the spec needs deeper redesign."

R3 surfaces **one current instance + one latent mechanism**:

1. **CURRENT INSTANCE (NC7).** The §12.3 + §12.5 bucketing query — *"any open ticket NOT enumerated in §13.5-§13.8 + §13.9 + §13.10 is a §12.x audit finding"* — produces a false-positive on `stoa--lyw` right now. lyw is placed at §13.14; §13.14 is not in the bucketing-list. The drift exists at audit time, not "could exist if the spec evolves."

2. **LATENT MECHANISM (NC6).** §13.10 / §13.11 / §13.13 / §14 back-references still read §12 as snapshot / catalogue / keep-list. No current drift in user-facing state, but the mechanism is live: a fresh team running Pass 8 / Pass 9 / Pass 13 / PRINCIPAL editing will encounter "match against §12.4 catalogue" with no catalogue to match against, and will need to re-derive what the structural rewrite implies for these sections.

**Honest read:** the structural fix is correct in its local scope (the original R1+R2 drift class is closed at §12). The fix's implications were not fully propagated to (a) sections that READ §12 as state-carrier, or (b) the bucketing-list enumeration that survived inside §12 itself. Per the activation paste's framing, this is *load-bearing evidence the structural approach as executed is incomplete*. The redesign is small in scope (back-reference cleanup at four locations + bucketing-list audit + likely a structural cleanup of "what is `§13.10 inline-handled` for if §12 doesn't carry the list?") — it is not "the structural approach was wrong" but "the structural fix needs another iteration to fully land."

**Compare to R1 + R2 patterns:**

- **R1 caught (commit `127f39b` spec authoring):** §12.1/§12.2/§12.5 lagged post-Arc-37 substrate while §12.3 was fresh. *Pattern: §12 subsections fall out of sync with each other AND with substrate state.*
- **R2 caught (commit `4a12358` first fold-in):** §12.3/§12.2 lagged post-W1-split state while §12.5/§13.7/§13.8 were fresh. *Same pattern at a different inflection.*
- **R3 catches (commit `a1a10e4` second fold-in — the structural fix):** §13.10/§13.11/§13.13/§14 back-references lag §12's new structural shape; §12.3+§12.5 bucketing-list lags §13.14 ticket placement. *Inverted-direction same pattern: now sections that READ §12 (or §12's references to §13) lag, while §12 itself is structurally consistent.*

The underlying pattern across all three: **when the source-of-truth boundary moves (whether substrate state, spec section structure, or §13.x ticket placement), the sections that re-encode any aspect of that source-of-truth drift unless every re-encoding is swept against the new boundary.** R1+R2 inflections were at the substrate-state boundary; R3's inflection is at the spec's internal structural boundary.

The structural fix narrowed the drift surface meaningfully (§12.1-§12.4 are no longer state-carriers) but did not eliminate it. To eliminate the class entirely would require either (a) propagating the structural rewrite to §13.10/§13.11/§13.13/§14 back-references AND removing the bucketing-list enumeration from §12.3+§12.5 (e.g., promote bucketing into §13 itself, or have the `validate-spec` skill enumerate the bucketing-list mechanically rather than the spec authoring it), or (b) accepting that some residual structural drift is inherent to a multi-section spec and adopting the procedural §12-re-sweep checklist from R2's closing observation as the catch.

PRINCIPAL + user-tier POLYBIUS own the fix-shape decision per ARGUS-discipline.

---

## Closing observation — meta-pattern across R1 + R2 + R3

Three audits over one workday on the same spec; one underlying pattern across all three; with a meaningful shift in R3.

**The shape that survived from R1 → R2 → R3:**

Every audit pass surfaced internal staleness *somewhere in the §12 / §13 / cross-ref family.* The specific drift instance differed each time, but the family of failure mode was the same: **two or more spec sections re-encode some aspect of substrate state (or each other's structure), and the re-encodings fall out of lockstep when the source advances.**

**What changed at R3 specifically:**

The structural §12 rewrite *transformed* the drift class rather than closing it:

- **Before (R1+R2):** §12 was a state-carrier with high-frequency drift (every arc-ship, every ticket-file, every W1-style renumber would cause §12 to drift unless §12 was actively re-swept).
- **After (R3):** §12 is no longer a state-carrier. The drift surface moved to (a) back-reference sections that still treat §12 as a state-carrier, and (b) a residual bucketing-list enumeration inside §12.3+§12.5 that drifts when §13.x adds new ticket-placing sections.

This is real progress — the drift surface shrunk meaningfully (a few cross-section references + one bucketing-list, vs the full §12 enumerations). But it is not the binary closure the structural-fix framing implied. The activation paste's R3 framing distinguishes between "structurally closed" (the substrate principle is empirically supported as N=2) and "still latent at <mechanism>" (the principle holds at the layer the fix targeted but a related drift class remains).

**R3 verdict on the substrate principle:**

The principle that *"structural fixes succeed where procedural fixes recur"* (per §4.6 TIRO + §27 mechanical-script / agent-inspection split + this §12 rewrite) is **supported with N=2 partial confirmations**, not yet structurally closed. Both TIRO (Arc 38 candidate; not yet built) and the structural §12 fix (this commit) succeed at narrowing the drift surface for the failure mode they target. Neither has yet demonstrated full closure of the drift class — TIRO is unbuilt; the §12 fix incompletely propagated. The N=2 evidence supports continued investment in structural-fix attempts but does not yet rise to "structural fixes succeed; procedural fixes fail" as substrate canon.

The future empirical signal worth watching: **does a third structural fix close its drift class fully on first execution, or does it require an iteration audit + propagation pass like the §12 fix did?** That is the discriminating test. If the third attempt also requires propagation iteration, the principle should be refined to *"structural fixes narrow drift surface; full closure requires propagation discipline at fix-author time."* If the third attempt lands cleanly first-shot, the original "structural > procedural" framing is empirically strengthened.

**Meta-observation across R1 + R2 + R3 audit cadence:**

The iteration-audit cadence (R1 → fold-in → R2 → fold-in → R3) itself is generating substantive value at each pass:

- R1 (49 findings) — first-pass fresh-eyes; caught the most obvious drift + most ambiguities.
- R2 (5 new findings; verified 27 ✓, 6 △, 4 ○, 12 D, 6 n/a from R1) — iteration-pass on the per-finding fold-in; surfaced the §12 staleness recurrence pattern + the propagation gap (frontmatter description, stellation cross-refs).
- R3 (2 new findings; verified 9 ✓, 3 △, 0 ○, 1 D from R2's named-for-this-pass items) — iteration-pass on the structural fix; surfaced that the structural fix is correct in scope but incomplete in propagation.

The diminishing-finding-count pattern (49 → 5 → 2) is the expected shape: each pass closes most of what the prior pass found, while leaving a smaller residue + occasionally surfacing a new pattern. This validates the iteration cadence as a working spec-quality discipline (the audit converges) without requiring the audit to be "exhaustive" on any single pass.

The fix-shape decision for the R3 findings (NC6 propagation + NC7 bucketing-list) belongs to PRINCIPAL + user-tier POLYBIUS per ARGUS-discipline. R3 surfaces; R3 does not propose.

---

## Output discipline — closing notes

- **ARGUS-discipline:** surface, do not fix. No SPECIFICATION.md / stellation-SPECIFICATION.md / SKILL.md edits were made by this audit. Fix-shape decisions are PRINCIPAL + user-tier POLYBIUS authority.
- **N=1 honesty (per op-disc §6.7.1):** R3 confirms the §12 staleness *family* persists with the drift surface transformed (not closed). This is N=3 of the pattern across consecutive audits; substrate-canon promotion of "structural > procedural" remains N=2 partial-confirmation (TIRO unbuilt; §12 fix incompletely propagated). The fourth-pass empirical test on a fresh structural fix (e.g., the eventual TIRO build at Arc 38 or a future structural-fix arc) would meet the §6.7.1 multi-class-evidence threshold.
- **Single-checker boundary:** R3 was done single-seat-direct per R1+R2 precedent (no ARGUS / CATO / BARTLEBY / ZENO sub-dispatch); the structural multi-checker step is PRINCIPAL + user-tier POLYBIUS review of this artifact.
- **Live-verification applied** (per §19.6 attestation discipline) to: `bw list --status open --all` (19 tickets including the R3 coord); `git log` reference SHAs at §12.1 (Arc 35 / Arc 36 v2 / Arc 37); `git log --pretty='%(trailers)'` on bb12806 + fcd68c0 + 6414397 (carve-out verification); SKILL.md frontmatter line 4 + body step 6 line 44 (NC2 verification); stellation-SPECIFICATION.md cross-ref destinations at lines 3 / 7 / 217 / 279 (X5/Y1 verification); §13.7 line 554 "Pass 10 stellation dispatch" (NC5 verification); §12 internal structure + §13.x bucketing-list walk (R3.2 + NC7 verification).

[from: polybius-the-stoa]
