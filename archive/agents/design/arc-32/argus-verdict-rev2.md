# ARGUS verdict — Arc 32 design rev2

**Verdict:** PASS
**Audited:** `agents/design/arc-32/design.md` (805 lines, rev2)
**Auditor:** CAPTAIN_ARGUS_the_stoa, 2026-05-17
**Authored by:** CAPTAIN_ARGUS_the_stoa, on behalf of the PRINCIPAL (Denson Smith).

(Transcribed to disk by PLINY because the ARGUS envelope structurally omits Write/Edit; ARGUS returned findings inline in its verdict block.)

---

## Risk-closure status

### R1 — closed

Rev2 added Edit 3a at design lines 225-235 specifying a single-sentence in-place edit to `operating-disciplines.md` §24 (existing line 1101). Substrate-state verified: the targeted prose `"Today, with PLINY as the only branch-creating seat, the substantive canon lives at MAJOR_PLINY.md §5.9 and the thin cross-ref here suffices."` exists verbatim at ops-disc.md:1101 (live read). The replacement narrows the framing-clause from "PLINY only [paste-activated]" to "PLINY only [branch-creating]" and adds the parenthetical back-pointer `(POLYBIUS is paste-activated but does not create branches under the gauntlet pipeline; see §26 for the broader paste-activation framing)`. Post-edit, §24 and the new §26 (C2) read coherently in either landing order. The §4.6 probe at design lines 692-697 verifies the edit landed by matching the exact replacement phrase. **No new risk introduced.** One minor unflagged observation: §24 line 1099 still references `MAJOR_POLYBIUS.md §5.1.2` only (pre-branch convention); the new sibling §5.1.3 (cron) is not enumerated at §24, but the "see §26 for broader paste-activation framing" back-pointer in the Edit 3a replacement gives a reader landing at §24 a one-hop path to the cron convention. This is acceptable; §24 is scoped to branch-creation and shouldn't enumerate the cron sibling directly.

### R2 — closed

Rev2 added Edit 4b at design lines 398-406 specifying a single-paragraph append to existing §19.4 (at ops-disc.md:841). Substrate-state verified: §19.4's existing closing sentence at line 841 reads *"`MAJOR_PLINY.md` §7.2 and `MAJOR_POLYBIUS.md` §4.3 carry a scope-broadening note pointing here."* The Edit 4b appended paragraph explicitly names §19.6 as the attestation-specific sub-discipline a reader landing via the §7.2/§4.3 back-pointer should follow through to. Cross-checked the actual back-pointers: §7.2 (MAJOR_PLINY.md:512) and §4.3 (MAJOR_POLYBIUS.md:85) both reference `operating-disciplines.md` §19 (root, not §19.4); a reader following either pointer lands at §19 and reads through §19.1 → §19.2 → §19.3 → §19.4 → §19.5 → §19.6 in linear order, so the new Edit 4b paragraph at §19.4 sits squarely in their reading path. The cite-comment at design line 412 has been rewritten to honestly describe the discovery path as "extended at its source via Edit 4b" rather than the rev1 confabulated "transitive inheritance" claim. The §4.6 probe at design lines 685-690 verifies Edit 4b landed by matching the exact appended-paragraph phrase. **No new risk introduced.** Discovery path is now mechanically followable.

### R3 — closed

Rev2 §3.3 (design lines 259-274) and §3.5 (design lines 433-448) BOTH name the canonical post-build order explicitly: `<§5.9.3 close> → <blank> → §5.9.4 → <blank> → §5.10 → <blank> → --- → §6`. ADA reading either subsection sees the same canonical order block. §4.5 (design lines 634-644) adds two relative-ordering probes:

1. `grep -nE "^#### 5\.9\.4 |^### 5\.10 "` with the prose instruction *"VERA: extract both line numbers from the grep output and compare numerically; fail if §5.10 appears at or above §5.9.4"* — mechanically followable.
2. `grep -nE "^### 5\.10 |^## 6\."` with sed-based verification that the line immediately preceding `## 6.` is `---` — followable, though slightly more procedural (VERA must compute "line-before-§6").

Weak point 6 at design lines 775-779 is rewritten as "(a) Cross-ref forward-resolution" + "(b) **Insertion-window collision (rev2 explicit acknowledgment per ARGUS R3)**" — the collision is named explicitly as a structural ordering hazard. **No new risk introduced.** The two probes are sufficient to catch a §5.10-above-§5.9.4 ordering inversion.

### R4 — closed

Rev2 §3.1 (design lines 76-78) adds a dedicated "**Categorical exception — C1's provenance shape diverges from C2-C5 by structural necessity**" paragraph naming the depth-6 unreadability constraint (`###### 5.1.1.1.1` would collapse out of most markdown renderers' styling and the TOC). The structural reason is cited: C1 is a worked-refinement of an existing depth-4 §5.1.1, so its §5.1.1.1 is already at depth-5; a peer provenance subsection beneath it would be depth-6. §4.7 probe rationale at design lines 711-713 rewritten to *"This is NOT a probe-author convenience — it is a structural necessity of the worked-refinement-of-existing-section shape C1 uses, named here so the per-candidate A10 check is honest about the divergence."* The A10 LOCK on per-candidate §15 honesty is now honestly satisfied: C1's exception is flagged with its structural reason, not silently accepted. **No new risk introduced.**

### R5 — closed

All four R5 sub-asks tightened:

- **§4.2 slot-explanation paragraph identity probe** added at design lines 542-547 — matches a unique sentence from the slot-explanation paragraph (`"Default-include is the safety property: the cost of including the preamble when no orphan cron is present"`) that does not appear in the source-of-truth section or universal-team cross-ref. Catches the case where `{{CRON_HYGIENE_CLAUSE}}` appears in the body but its slot-explanation paragraph was omitted.
- **§4.6 per-depth probes** at design lines 650-683 — seven separate probes, each pinned to a specific depth (`^##### 5\.1\.1\.1\b`, `^#### 5\.1\.3\b`, `^#### 5\.9\.4\b`, `^### 5\.10\b`, `^### 19\.6\b`, `^## 24\.`, `^## 26\.`). A depth-typo regression at any single candidate fails its specific probe.
- **§4.7 per-file probes** at design lines 717-730 — three separate `grep -nE "enters substrate canon off-gate"` calls against MAJOR_POLYBIUS.md (expects ≥1), MAJOR_PLINY.md (expects ≥2), operating-disciplines.md (expects ≥1). All-in-one-file regression cannot pass.
- **C3↔C4 reciprocal cross-ref content probes** at design lines 699-709 — match the specific canonical reciprocal phrasing in both directions (`"§19.6.*the canonical home for the root-cause discipline"` in MAJOR_PLINY.md and `"§5.10.*PLINY-specific worked example"` in operating-disciplines.md). Wrong-direction or generic-string cites cannot pass.

**No new risk introduced.** Probe set is now tight enough to fail a partially-correct build.

### R6 — closed

Rev2 §3.5 (design lines 422-426) adds a dedicated honest-qualification paragraph at line 424: *"the §5.1.2 analogy is structural-shape (default-include rather than per-session judgment), not identity"* — followed by the predicate-knowability distinction (§5.1.2 = POLYBIUS at paste-fill time, low session knowledge; §5.9.4 = PLINY at branch-creation time, high moment-of-decision knowability but low duration-knowability). The defense is reframed to structural-shape ("the cost of the default is small AND the failure mode the default prevents is structural-coordination-failure") rather than predicate-identity. The line 424 (new) and line 426 (existing) prose are internally consistent: line 424 names moment-of-decision knowability as high; line 426 distinguishes moment-of-decision (high) from duration-knowability (low). No internal contradiction. **No new risk introduced.** Future-arc revision path is acknowledged in line 424's closing clause.

---

## New risks introduced by rev2

None.

The rev2 edits are surgical (in-place sentence narrowing at §24; single-paragraph append at §19.4; targeted prose additions at §3.1, §3.3, §3.5; per-depth + per-file probe splits at §4.6 and §4.7). No structural reshape of the design; no new candidates introduced; no scope-broadening of the A1-A11 LOCKED architectural decisions. Cross-checked against substrate state: both Edit 3a's target line (ops-disc.md:1101) and Edit 4b's target line (ops-disc.md:841) exist verbatim as the design claims. Cross-checked against the rev2 design's internal consistency: weak point 6's two-hazard restructuring, §3.3 + §3.5 canonical-order duplication, §4.5 + §4.6 + §4.7 probe-split additions all hang together cleanly.

---

## Summary

Rev2 closes all six rev1 risks (R1-R4 high; R5-R6 medium) with surgical in-place edits. Each risk's substance is genuinely addressed (not papered over): the §24 contradiction is removed by narrowing the framing-clause to branch-creation; the §19.4 transitive-inheritance confabulation is removed by making the discovery path explicit at §19.4's source; the insertion-window collision is named in both §3.3 and §3.5 with an enforceable probe pair at §4.5; C1's provenance-shape divergence is flagged as a structural-necessity categorical exception; the probe set is tightened along all four R5 sub-asks; and the §5.1.2 analogy is honestly qualified as structural-shape rather than predicate-identity. No new risk introduced. The design is ready for ADA build.

**Verdict: PASS.** No further DAEDALUS revision needed; ADA may dispatch.
