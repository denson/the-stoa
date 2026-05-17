# ARGUS verdict — Arc 32 design rev1

**Verdict:** REVISE
**Audited:** `agents/design/arc-32/design.md` (655 lines)
**Auditor:** CAPTAIN_ARGUS_the_stoa, 2026-05-17
**Authored by:** CAPTAIN_ARGUS_the_stoa, on behalf of the PRINCIPAL (Denson Smith).

(Transcribed to disk by PLINY because the ARGUS envelope structurally omits Write/Edit; ARGUS returned findings inline in its verdict block.)

---

## Load-bearing risks

### R1 [severity: high] — C2 Carrier 3 (ops-disc §26) contradicts the existing §24's "PLINY only" framing it claims to mirror

Design §3.2 (lines 84-96) frames C2 as "exact mirror" of Arc 30's three-carrier pattern, and the new §26 prose (design lines 202-219) says "today PLINY and POLYBIUS are the only paste-activated seats." **But the existing §24 prose (`substrate/operating-disciplines.md:1101`) explicitly says: *"Today, with PLINY as the only branch-creating seat, the substantive canon lives at `MAJOR_PLINY.md` §5.9…"*** The §24 thin-cross-ref was written under a one-seat-only premise. C2's §26 introduces a two-seat premise (PLINY + POLYBIUS) for paste-activation that quietly invalidates one of the assumptions §24's framing rests on (POLYBIUS sessions ARE paste-activated; they always were). If §26 is right, §24's "PLINY only" framing was always over-narrow — and the design does NOT touch §24's prose to harmonize. Reader landing in §24 vs §26 in the post-build state gets two different mental models of "which seats activate from pastes."

**Why load-bearing:** the C2 canon's correctness depends on a fact (POLYBIUS = paste-activated) that contradicts the de-facto reading of the §24 mirror it cites as template.

### R2 [severity: high] — C4 §3.4 cite-comment line 369 makes a confabulated transitive-inheritance claim about §19.4 back-pointers

Design §3.4 cite-comments (line 369): *"The `MAJOR_PLINY.md` §7.2 and `MAJOR_POLYBIUS.md` §4.3 cross-refs are NOT edited by this arc — those sections already carry a scope-broadening pointer to §19 (per existing §19.4 prose); the new §19.6 inherits the existing back-pointer transitively. No edit needed at §7.2 / §4.3."*

Verified against substrate state: existing §19.4 (`ops-disc.md:837-841`) says *"`MAJOR_PLINY.md` §7.2 and `MAJOR_POLYBIUS.md` §4.3 carry a scope-broadening note pointing **here**"* — "here" = §19 root, not specifically §19.6. A reader at §7.2 / §4.3 who follows the pointer to §19 reads §19.1-§19.5 in current canon; they do NOT mechanically land at §19.6 unless §19's TOC-shape or §19.4's prose is updated.

The "transitive inheritance" claim is structurally false — back-pointers do not auto-extend to new sub-subsections appended after their authoring. C4 either needs (a) a small prose extension of §19.4 to name §19.6 as a sub-discipline, or (b) §7.2 / §4.3 edits to point at §19.6 specifically, or (c) acknowledgment that §19.6 inherits visibility weakly (which the design does not currently acknowledge).

**Why load-bearing:** the C4 cite-comment is the design's only defense of why the §7.2 / §4.3 edits are unneeded; the defense is incorrect on the substrate state.

### R3 [severity: high] — C3 + C5 BOTH insert into the same single-line window between `MAJOR_PLINY.md:388` (§5.9.3 close) and :390 (`---`), with no ordering guarantee in the §4 probes

Design §3.3 (line 241) places §5.10 "between MAJOR_PLINY.md:388 and the `---` at MAJOR_PLINY.md:390." Design §3.5 (line 384) places §5.9.4 "after §5.9.3 closes at MAJOR_PLINY.md:388 and before the new §5.10 (C3, §3.3 above) inserts."

Two new sections targeting the same two-line window — one a depth-4 sub-subsection (`#### 5.9.4`), one a depth-3 top-level subsection (`### 5.10`) — with no `---` separator between them, even though `---` is the existing convention separating §5.9 family from §6.

Design's intended post-build order is §5.9.3 → §5.9.4 → §5.10 → `---` → `## 6.`, which means §5.10 (a `###` peer to §5.1-§5.9) ends up immediately above the `## 6.` boundary with no inter-family blank separator other than the existing `---`. **VERA's §4.5 probes do not enforce relative ordering** between §5.9.4 and §5.10; either insertion order could pass each individual grep yet ship a structurally broken file (e.g., §5.10 nested inside §5.9 family by accident, or §5.9.4 placed AFTER §5.10 such that the §5.9.4-cleanup-references-§5.10-verification cross-ref reads forward not back).

Design weak point 6 acknowledges build-order coupling exists; it does NOT acknowledge this specific insertion-window collision.

**Why load-bearing:** ADA could honestly apply both edits per design and ship a file where §5.9.4 sits BELOW §5.10 (no probe catches it), breaking the §5.9-family / §5.10-peer structural distinction the design's locus rationale rests on.

### R4 [severity: medium-high] — C1 §5.1.1.1 has no separate §15-shaped provenance subsection; pattern inconsistency across C1-C5

Per A10 (directive) and design §2 imported-assumption (line 35) every candidate "names its empirical anchor (N=1 or N=2 today) and explicitly defers to `operating-disciplines.md` §6.7.1 for promotion."

- C2 §5.1.3 has a dedicated final "**Provenance**" paragraph.
- C3 §5.10 has a numbered `#### 5.10.3 N=1 provenance + accretion path`.
- C4 §19.6 has `#### 19.6.4 N=1 provenance + accretion path`.
- C5 §5.9.4 has `#### 5.9.4.1 Empirical anchor and provenance`.
- **C1's §5.1.1.1 folds provenance into a closing inline paragraph** (design line 73) using the variant phrasing "future-evidence accretion per §6.7.1" — verified by design §4.7 (lines 588-593) which explicitly carves a probe-exception for C1.

Inconsistency means C1's N=1 provenance is structurally weaker than the other four: no numbered subsection header, no controlled-comparison field, no explicit "enters substrate canon off-gate on PRINCIPAL's project-direction authority" phrasing that the §4.7 probe enforces for C2-C5. Design weak point 1 defends the depth-5 nesting but does NOT defend the provenance-shape divergence.

Either C1 needs the same provenance subsection-shape (which would push it to depth-6 `######` — structurally unreadable), or the design needs to acknowledge that C1's structural shape (worked-refinement of §5.1.1) genuinely can't carry the same provenance shape and that's a categorical exception.

**Why load-bearing:** A10 LOCKS "per-candidate §15 N=1 honesty" and C1's exception is unflagged.

### R5 [severity: medium] — §4 probe set is loose enough to pass a partially-correct build

Specific gaps:

- **§4.2 line 478-481:** "at least two matches" for `{{CRON_HYGIENE_CLAUSE}}` is correct minimum but VERA executing the probe needs to verify the slot-explanation paragraph specifically — not just any second match. The probe doesn't distinguish.
- **§4.6 line 567-571:** the regex `^### 5\.1\.1\b|^##### 5\.1\.1\.1\b` mixes depths-3 and -5 in one alternation. ripgrep on this is fine but doesn't catch the design's structural-depth claim — could miss `#### 5.1.1.1` (depth-4) typo if ADA accidentally types it that way.
- **§4.7 line 588:** `grep -nE "enters substrate canon off-gate"` expects "at least 4 matches" across THREE files but doesn't break them out per-file — could pass with 4 in one file and 0 in others.
- **§4.3 / §4.4:** no probe verifies the §5.10 ↔ §19.6 reciprocal cross-ref *content* (only that the strings exist somewhere). C3↔C4 reciprocity is the design's weak point 6 + my R2; probe should match the specific reciprocal-cite phrase.

Not as load-bearing individually as R1-R4, but in aggregate the probe set could PASS against a meaningfully-broken post-build state.

### R6 [severity: medium] — C5 §5.9.4 Option-A defense rests on the §5.1.2 default-include analogy, but the analogy obscures a real difference

Design §3.5 line 379: *"Option B …rejected on the same structural reason §5.1.2 rejected per-session paste-suppression."*

The §5.1.2 analogy is: POLYBIUS's session-by-session "will this session plausibly create a branch" is a semantic predicate not always knowable. But §5.1.2's predicate is asked at *paste-fill* time (POLYBIUS knows little about the downstream PLINY session); §5.9.4's predicate is asked at *branch-creation* time by PLINY itself (PLINY knows everything about its own session and whether user-tier POLYBIUS is operating concurrently). The two predicates have meaningfully different knowability profiles.

The empirical anchor (Arc 31 divergence) is N=1 and produced no defect — design weak point 5 names this honestly, but the defense ("§5.1.2 default-include applied to worktree placement") elides the predicate-knowability difference rather than addressing it.

**Why load-bearing:** if Option A's rigidity ever surfaces friction (the symmetric case to the Arc 31 friction), the defense-prose makes it harder for future arcs to revise — the analogy claims the structural reason is the same when it isn't quite.

---

## Non-findings (risks considered, discharged)

- **§3.2 Edit 2a "however" disclaimer (design lines 135).** Honest course-correction documentation, not a contradiction. Not a risk.
- **`MAJOR_POLYBIUS.md` §15 cite-chain confabulation suspicion.** Substrate canon already uses "§15 (N=1 honest-scope discipline)" as a stable nickname. Not a risk despite naming collision with ops-disc §15.
- **§6.7.1 sub-subsection existence.** Verified `ops-disc.md:81` exists. All design cites to §6.7.1 resolve.
- **Authorship audit per §7 / §4.8.** Clean. Only existing `author: Denson Smith` frontmatter in edit set; no new author-like fields.
- **A9 out-of-scope discipline.** Clean. Design §6 enumerates the seven out-of-scope items.
- **Design weak point 7 (§24 bullet-list pre-condition).** Holds at this snapshot. Not flagging.
- **C3 cleanup-categories enumeration (design weak point 3).** Structurally defensible per the design's defense. Not flagging.
- **§19.6 vs §19.2 pattern 2 distinction (design weak point 4).** Defense is structurally legitimate; weak point 4 over-defends. Not flagging.

---

## Summary

The design's overall shape is clean: 5 candidates, each with locus rationale + verbatim prose + cite-comments + per-candidate honest-scope framing. The C3/C5 DAEDALUS sub-decisions (Option α + Option A) are defensible within A4/A6 discretion and do not approach §25 PRINCIPAL-gate territory. Verbatim canon prose tone, three-carrier framing, and §15 N=1 provenance shape all match Arc 30's pattern within reasonable tolerance.

The four high-severity risks are concentrated in **structural-coherence-across-files** failures: R1 (C2's §26 contradicts existing §24's premise about which seats are paste-activated), R2 (C4 confabulates a "transitive inheritance" of back-pointers that the substrate state does not support), R3 (C3+C5 both insert into the same single-line window with no probe-enforced ordering), R4 (C1 quietly diverges from the per-candidate provenance-shape A10 LOCKS). R5/R6 are tightening asks rather than blockers. None of the risks invalidate the arc; all are addressable in a tight DAEDALUS rev2 with targeted prose edits.

**Verdict: REVISE.** Recommend DAEDALUS rev2 addressing R1-R4 (and ideally R5-R6) before ADA dispatch.
