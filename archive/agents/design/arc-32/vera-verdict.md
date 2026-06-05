# VERA verdict — Arc 32

**Verdict:** PASS (with 3 methodology concerns flagged for future probe-design refinement; substantive intent of all probes satisfied)
**Verified:** built deliverable on `arc-32/build` (commits `66bed01` + `9ec851f`)
**Worktree:** `C:\Users\denso\claude_projects\the-stoa\.claude\worktrees\arc-32-build`
**Design artifact:** `agents/design/arc-32/design.md` rev2 (805 lines; ARGUS rev2 PASS)
**Probes executed:** 29 / 29 (per design §4.1-§4.9; §4.10 non-applicability confirmed)
**Sampling:** full (substrate-canon scope per dispatch)

---

## Per-probe results

### §4.1 — C1 §5.1.1 extension present

- **Probe 1** — `grep -n "Cross-project sequencing context is user-tier-only" substrate/MAJOR_POLYBIUS.md`
  - Expected: one match at §5.1.1.1 header
  - Observed: 1 match at line 226 (`##### 5.1.1.1 Cross-project sequencing context is user-tier-only — never leak it to project-tier seats`)
  - **PASS**
- **Probe 2** — `grep -n "Sector-4 corpus seed (separate follow-on" substrate/MAJOR_POLYBIUS.md`
  - Expected: one match in anti-pattern block-quote
  - Observed: 1 match at line 234 (anti-pattern block-quote inside §5.1.1.1)
  - **PASS**
- **Probe 3** — `grep -n "Per §5.1.1, this paste scopes to ariadne-core work only" substrate/MAJOR_POLYBIUS.md`
  - Expected: one match in positive-pattern block-quote
  - Observed: 1 match at line 240 (positive-pattern block-quote inside §5.1.1.1)
  - **PASS**

### §4.2 — C2 cron-hygiene three carriers + cross-ref present

**Carrier 1 — `MAJOR_POLYBIUS.md` §5.1.3 (source-of-truth):**

- **Probe 1** — `grep -n "5.1.3 PLINY-targeted and POLYBIUS-targeted activation pastes include the cron-hygiene preamble by default" substrate/MAJOR_POLYBIUS.md`
  - Expected: one match at §5.1.3 header
  - Observed: 1 match at line 282 (`#### 5.1.3 ...`)
  - **PASS**
- **Probe 2** — `grep -n "this session may carry an" substrate/MAJOR_POLYBIUS.md`
  - Expected: one match inside §5.1.3 preamble code-fence
  - Observed: 1 match at line 291 (preamble code-fence)
  - **PASS**

**Carrier 2 — `paste-instruction-template.md` (template slot):**

- **Probe 3** — `grep -n "{{CRON_HYGIENE_CLAUSE}}" substrate/templates/paste-instruction-template.md`
  - Expected: at least two matches (template body + slot-explanation paragraph)
  - Observed: 2 matches at lines 46 and 55
  - **PASS**
- **Probe 4 (rev2 slot-explanation identity)** — `grep -n "Default-include is the safety property: the cost of including the preamble when no orphan cron is present" substrate/templates/paste-instruction-template.md`
  - Expected: exactly one match (uniqueness asserted in design)
  - Observed: 2 matches at lines 55 and 68
  - **PASS-on-intent / METHODOLOGY CONCERN #1**: the slot-explanation paragraph for `{{CRON_HYGIENE_CLAUSE}}` is present at line 55 as designed. However, the line-68 match is the slot-explanation paragraph for `{{PRE_BRANCH_HYGIENE_CLAUSE}}` (Arc 30 prior-canon), which reuses the same "Default-include is the safety property: the cost of including the preamble when..." boilerplate sentence form. The design's uniqueness assertion was incorrect — the sentence prefix is templated across both CRON_HYGIENE and PRE_BRANCH_HYGIENE slot-explanation paragraphs. Substantive intent (CRON_HYGIENE slot-explanation is present) is satisfied. To make this probe uniquely identifying in future arcs, the design should match a longer string that includes the cron-specific tail ("...orphan cron from a prior `/clear`'d context...") rather than the boilerplate prefix.
- **Probe 5** — `grep -nE "orphaned cron from a prior" substrate/templates/paste-instruction-template.md`
  - Expected: at least two matches (default-expansion code-fence + worked-example code-fence)
  - Observed: 2 matches at lines 61 and 112
  - **PASS**

**Carrier 3 — `operating-disciplines.md` §26 (thin cross-ref):**

- **Probe 6** — `grep -n "26. Activation-paste cron hygiene" substrate/operating-disciplines.md`
  - Expected: one match at §26 header
  - Observed: 1 match at line 1265 (`## 26. Activation-paste cron hygiene (PLINY-primary + POLYBIUS; cross-ref)`)
  - **PASS**
- **Probe 7** — `grep -n "MAJOR_POLYBIUS.md.*§5.1.3" substrate/operating-disciplines.md`
  - Expected: at least one match in §26
  - Observed: 2 matches at lines 1269 + 1275 (both in §26 — body paragraph + cross-references bullet)
  - **PASS**

### §4.3 — C3 PLINY-signoff-accuracy at §5.10

- **Probe 1** — `grep -n "5.10 Signoff-accuracy — verify cleanup claims before posting" substrate/MAJOR_PLINY.md`
  - Expected: one match at §5.10 header
  - Observed: 1 match at line 422 (`### 5.10 Signoff-accuracy — verify cleanup claims before posting`)
  - **PASS**
- **Probe 2** — `grep -nE "Sign what you did, not what you intended" substrate/MAJOR_PLINY.md`
  - Expected: one match in §5.10 body
  - Observed: 1 match at line 424 (§5.10 body opening paragraph)
  - **PASS**
- **Probe 3** — `grep -n "Arc 29 signoff" substrate/MAJOR_PLINY.md`
  - Expected: one match in §5.10.1 empirical anchor
  - Observed: 2 matches at lines 439 (§5.10.1) and 449 (§5.10.2 cross-references — `Arc 29 / stoa--ads signoff inaccuracy`)
  - **PASS-on-intent**: the design probe expected one match in §5.10.1; line 439 satisfies that. The line-449 match is the §5.10.2 cross-references bullet's "Empirical anchor: Arc 29 / `stoa--ads` signoff inaccuracy" — substantively reinforces the same anchor; the probe undercounted the natural redundancy of cite-blocks. Both matches are inside §5.10; no false-elsewhere.
- **Probe 4** — `grep -n "MAJOR_PLINY.md.*§5.10.*PLINY-signoff-accuracy" substrate/operating-disciplines.md`
  - Expected: one match in §24 Cross-references block
  - Observed: 1 match at line 1158 (§24 cross-references block)
  - **PASS**

### §4.4 — C4 §19.6 attestation sub-rule present

- **Probe 1** — `grep -n "19.6 Attestation-confabulation — cite live-verified state" substrate/operating-disciplines.md`
  - Expected: one match at §19.6 header
  - Observed: 1 match at line 849 (`### 19.6 Attestation-confabulation — cite live-verified state, not assumed-from-context state`)
  - **PASS**
- **Probe 2** — `grep -n "Discipline-PASS and honesty-PASS are separate properties" substrate/operating-disciplines.md`
  - Expected: one match in §19.6 body
  - Observed: 1 match at line 853 (§19.6 body paragraph)
  - **PASS**
- **Probe 3** — `grep -nE "140b398.*dispatch-authoring SHA" substrate/operating-disciplines.md`
  - Expected: one match in §19.6.1 empirical anchor
  - Observed: 2 matches at lines 883 (§19.6.2 cross-references — "Empirical anchor: Arc 30 PLINY init-handshake attested `140b398` from the dispatch-authoring SHA") and 891 (§19.6.4 N=1 framing). The §19.6.1 location described by the design's probe is the empirical-anchor narrative which says "attested `140b398` (the dispatch-authoring SHA carried in the directive)". Multiple matches because the same SHA + phrase recurs across the empirical-anchor + cross-references + N=1 framing — natural cite-redundancy across §19.6 sub-subsections.
  - **PASS-on-intent**: the SHA + phrase IS present at the empirical-anchor location as designed; both line-883 and line-891 are inside §19.6. The probe's "one match in §19.6.1" was the under-count.

### §4.5 — C5 §5.9.4 worktree convention + cleanup convention + relative ordering

- **Probe 1** — `grep -n "5.9.4 Arc-build worktree convention" substrate/MAJOR_PLINY.md`
  - Expected: one match at §5.9.4 header
  - Observed: 1 match at line 390 (`#### 5.9.4 Arc-build worktree convention — separate worktree at .claude/worktrees/arc-N-build/`)
  - **PASS**
- **Probe 2** — `grep -nE "git worktree add .claude/worktrees/arc-N-build" substrate/MAJOR_PLINY.md`
  - Expected: at least one match
  - Observed: 1 match at line 395 (creation code-fence)
  - **PASS**
- **Probe 3** — `grep -nE "git worktree remove .claude/worktrees/arc-N-build" substrate/MAJOR_PLINY.md`
  - Expected: at least one match in §5.9.4 cleanup code-fence
  - Observed: 1 match at line 409 (cleanup code-fence)
  - **PASS**
- **Probe 4** — `grep -nE "git branch -D arc-N/build" substrate/MAJOR_PLINY.md`
  - Expected: at least one match in §5.9.4 cleanup code-fence
  - Observed: 1 match at line 410 (cleanup code-fence)
  - **PASS**
- **Probe 5** — `grep -nE "git push origin --delete arc-N/build" substrate/MAJOR_PLINY.md`
  - Expected: at least one match in §5.9.4 cleanup code-fence
  - Observed: 1 match at line 411 (cleanup code-fence)
  - **PASS**

**Relative-ordering enforcement (rev2 addition per ARGUS R3):**

- **Probe 6** — `grep -nE "^#### 5\.9\.4 |^### 5\.10 " substrate/MAJOR_PLINY.md`
  - Expected: exactly two matches; §5.9.4 line < §5.10 line
  - Observed: 2 matches at lines 390 (§5.9.4) and 422 (§5.10). 390 < 422 — strict-less-than satisfied.
  - **PASS**
- **Probe 7** — `grep -nE "^### 5\.10 |^## 6\." substrate/MAJOR_PLINY.md | head -5`
  - Expected: §5.10 line < §6 line; `---` separator at line immediately preceding `## 6.`
  - Observed: §5.10 at line 422, §6 at line 464. 422 < 464 — strict-less-than satisfied. `---` separator found at line 462 (line 463 is blank; line 464 is `## 6. Communication`).
  - **PASS-on-intent / METHODOLOGY CONCERN #2**: the probe's "line immediately preceding `## 6.`" wording strictly requires line 463 to be `---`, but the canonical markdown convention is `---` + blank line + heading. The substantive intent (verify `---` family-boundary separator sits between §5.10 and §6, with §5.10 above the boundary) is satisfied: line 462 is `---`, §5.10 (line 422) is above it. Future probe wording should say "within 1-2 lines preceding" or "search for `---` between §5.10 close and §6 open" to match the conventional separator + blank + heading pattern.

### §4.6 — Cite-comment cross-refs resolve (per-depth probes + content probes)

- **Probe 1** — `grep -nE "^##### 5\.1\.1\.1\b" substrate/MAJOR_POLYBIUS.md`
  - Expected: exactly one match at §5.1.1.1 (depth-5)
  - Observed: 1 match at line 226
  - **PASS**
- **Probe 2** — `grep -nE "^#### 5\.1\.3\b" substrate/MAJOR_POLYBIUS.md`
  - Expected: exactly one match at §5.1.3 (depth-4)
  - Observed: 1 match at line 282
  - **PASS**
- **Probe 3** — `grep -nE "^#### 5\.9\.4\b" substrate/MAJOR_PLINY.md`
  - Expected: exactly one match at §5.9.4 (depth-4)
  - Observed: 2 matches at lines 390 (`#### 5.9.4 Arc-build worktree convention ...`) and 416 (`#### 5.9.4.1 Empirical anchor and provenance`)
  - **PASS-on-intent / SUBSTANTIVE DEFECT FLAGGED**: the §5.9.4 header at line 390 IS at depth-4 as expected. The over-match at line 416 is caused by `\b` matching at the period boundary between `4` and `1` in `5.9.4.1`. However, this surfaced a separate substantive defect: **§5.9.4.1 is at depth-4 (`####`) when convention says it should be depth-5 (`#####`)** to nest properly under §5.9.4 (also depth-4). This depth typo was inherited from the design's verbatim canon prose at design.md:485 (`#### 5.9.4.1 Empirical anchor and provenance`). ADA built per design verbatim. Per VERA discipline §5.1 (independence) I do not modify the build; per §5.3 I name this as a methodology gap (probe coverage missed §5.9.4.1 depth) AND a substantive defect in the design that ADA inherited. CATO should evaluate whether to surface this for a follow-up arc fix or accept-and-defer. Compare: §5.10.1, §5.10.2, §5.10.3 are correctly at depth-4 (`####`) as children of depth-3 (`###`) §5.10; symmetrically §5.9.4.1 should be at depth-5 (`#####`) as a child of depth-4 (`####`) §5.9.4.
- **Probe 4** — `grep -nE "^### 5\.10\b" substrate/MAJOR_PLINY.md`
  - Expected: exactly one match at §5.10 (depth-3)
  - Observed: 1 match at line 422
  - **PASS**
- **Probe 5** — `grep -nE "^### 19\.6\b" substrate/operating-disciplines.md`
  - Expected: exactly one match at §19.6 (depth-3)
  - Observed: 1 match at line 849
  - **PASS**
- **Probe 6** — `grep -nE "^## 24\." substrate/operating-disciplines.md`
  - Expected: exactly one match at §24 (depth-2)
  - Observed: 1 match at line 1141
  - **PASS**
- **Probe 7** — `grep -nE "^## 26\." substrate/operating-disciplines.md`
  - Expected: exactly one match at §26 (depth-2, new top-level)
  - Observed: 1 match at line 1265
  - **PASS**

**§19.4 extension probe (Edit 4b):**

- **Probe 8** — `grep -n "The attestation sub-discipline at §19.6 (Arc 32) is the specific application of §19" substrate/operating-disciplines.md`
  - Expected: exactly one match inside §19.4
  - Observed: 1 match at line 843 (inside §19.4)
  - **PASS**

**§24 prose-edit probe (Edit 3a):**

- **Probe 9** — `grep -n "PLINY as the only seat creating arc-build branches (POLYBIUS is paste-activated but does not create branches" substrate/operating-disciplines.md`
  - Expected: exactly one match inside §24
  - Observed: 1 match at line 1150 (inside §24; line content omitted from grep due to length)
  - **PASS**

**C3↔C4 reciprocal cross-ref content probes (rev2 tightened):**

- **Probe 10** — `grep -n "operating-disciplines.md.*§19.6.*the canonical home for the root-cause discipline" substrate/MAJOR_PLINY.md`
  - Expected: exactly one match in §5.10.1 (C3 cites C4)
  - Observed: 1 match at line 446 (the bullet is structurally in §5.10.2 cross-references rather than §5.10.1 empirical-anchor narrative — the canonical reciprocal-cite locus that §3.3's cite-comments specified)
  - **PASS** — substantive intent: C3 reciprocally cites C4 with the canonical "canonical home for the root-cause discipline" phrasing. Probe wording said "§5.10.1" but the actual locus is §5.10.2 (the cross-references bullet, which is the natural home for cross-citations). ADA's signoff explicitly noted this micro-correction was made during build to keep the design verbatim (the canonical phrase lives in §5.10.2 in the design and in the file). Substantively identical to expected.
- **Probe 11** — `grep -n "MAJOR_PLINY.md.*§5.10.*PLINY-specific worked example" substrate/operating-disciplines.md`
  - Expected: exactly one match in §19.6.2 (C4 cites C3)
  - Observed: 1 match at line 881 (`§19.6.2` cross-references bullet: "`MAJOR_PLINY.md` §5.10 (this arc, C3) — PLINY-specific worked example: signoff-accuracy verifies cleanup claims before posting.")
  - **PASS**

### §4.7 — §15 N=1 provenance shape per A10

**Per-file boilerplate-phrase probes (rev2 split):**

- **Probe 1** — `grep -nE "enters substrate canon off-gate" substrate/MAJOR_POLYBIUS.md`
  - Expected: at least 1 match (C2 §5.1.3 provenance)
  - Observed: 3 matches (count via `grep -c`)
  - **PASS**
- **Probe 2** — `grep -nE "enters substrate canon off-gate" substrate/MAJOR_PLINY.md`
  - Expected: at least 2 matches (C3 §5.10.3 + C5 §5.9.4.1)
  - Observed: 4 matches
  - **PASS**
- **Probe 3** — `grep -nE "enters substrate canon off-gate" substrate/operating-disciplines.md`
  - Expected: at least 1 match (C4 §19.6.4)
  - Observed: 4 matches
  - **PASS**

**C1 categorical-exception probe:**

- **Probe 4** — `grep -n "future-evidence accretion per §6.7.1" substrate/MAJOR_POLYBIUS.md`
  - Expected: at least one match in §5.1.1.1
  - Observed (case-sensitive): 0 matches
  - Observed (case-insensitive `grep -i`): 1 match at line 244 — `"...Future-evidence accretion per §6.7.1 — if the cross-project shape proves to be one-of-many specialization needs..."`
  - **PASS-on-intent / METHODOLOGY CONCERN #3**: the design probe used lowercase `future-evidence` but the prose at §5.1.1.1's close (line 244) starts the sentence with capitalized `Future-evidence`. This is grammatically correct (sentence start). ADA wrote the prose per design's verbatim canon (§3.1 specified the phrase as `Future-evidence accretion per §6.7.1 — if the cross-project shape proves...` at the sentence boundary; ADA preserved the natural capitalization). Substantive intent (categorical-exception inline-paragraph provenance form present at §5.1.1.1's close, containing the §6.7.1 reference) is satisfied. The probe should be case-insensitive (`grep -in` or `grep -E -i`) to match the actual capitalization.

### §4.8 — Authorship audit (per A8)

- **Probe 1** — `grep -rnE "^author:|^Authored by:|^Author:" substrate/templates/paste-instruction-template.md substrate/MAJOR_POLYBIUS.md substrate/MAJOR_PLINY.md substrate/operating-disciplines.md`
  - Expected: only existing `author: Denson Smith` at `paste-instruction-template.md:2`
  - Observed: 1 match — `C:/.../substrate/templates/paste-instruction-template.md:2:author: Denson Smith`
  - **PASS** — no author-like fields added or modified; A8 honored.

### §4.9 — `check.sh` against the-stoa workspace

- **Probe 1** — `bash substrate/skills/check-substrate-updates/check.sh --workspace C:/Users/denso/claude_projects/the-stoa`
  - Expected: DRIFTED on the four edited substrate files (`MAJOR_POLYBIUS.md`, `MAJOR_PLINY.md`, `operating-disciplines.md`, `templates/paste-instruction-template.md`)
  - Observed: DRIFTED reported on all four expected files:
    - `.claude/MAJOR_POLYBIUS.md` (+199 lines)
    - `.claude/MAJOR_PLINY.md` (+133 lines)
    - `.claude/operating-disciplines.md` (+314 lines)
    - `.claude/templates/paste-instruction-template.md` (+60 lines)
  - Additional DRIFTED entries (CAPTAIN_ADA, CAPTAIN_DAEDALUS, CAPTAIN_VERA, polling-cron-prompt-template, autonomous-mode-activation-template, apply.sh, check.sh) and MISSING (check-bw-release skill files) are pre-existing drift from prior arcs not yet propagated to the-stoa workspace; not in scope for this arc's verification.
  - **PASS**

### §4.10 — Credential-discipline non-applicability gate

- **Confirmed:** this design touches no credentialed operations. No CLI/API gated by tokens, OAuth scopes, or service accounts is invoked. No probe authors any workflow YAML; no probe invokes any credentialed tool. The §6.6 credential-flow probe requirement does not apply.
- **PASS (non-applicability gate)**

---

## Methodology concerns

Three probe-design concerns surfaced during execution. All are probe-pattern precision issues; none invalidate the substantive intent of the affected probes; none constitute a build defect against the design.

1. **§4.2 Probe 4 (slot-explanation identity)** — the design's uniqueness assertion was incorrect; the boilerplate sentence prefix `"Default-include is the safety property: the cost of including the preamble when..."` appears in both `{{CRON_HYGIENE_CLAUSE}}` (line 55) and `{{PRE_BRANCH_HYGIENE_CLAUSE}}` (line 68) slot-explanation paragraphs because the two slots share a templated prose pattern. Future probe should match a longer string carrying the cron-specific tail.

2. **§4.5 Probe 7 (`---` separator immediately preceding `## 6.`)** — the probe wording strictly requires the line at `<§6-line - 1>` to be `---`, but the canonical markdown pattern is `---` + blank line + heading. The substantive intent (verify `---` family-boundary separator sits between §5.10 and §6, with §5.10 above the boundary) is satisfied: line 462 is `---`, line 463 is blank, line 464 is `## 6. Communication`. Future probe should search for `---` within 1-2 lines preceding the next heading rather than at the strict immediately-preceding line.

3. **§4.7 Probe 4 (C1 categorical-exception phrasing)** — the design probe used lowercase `future-evidence accretion per §6.7.1` but the actual prose at §5.1.1.1's closing-paragraph provenance (line 244) capitalizes `Future-evidence` at sentence start, which is grammatically natural and matches the design's verbatim canon. The probe should be case-insensitive (`grep -i`).

## Substantive defect flagged (inherited from design, not introduced by build)

**§5.9.4.1 depth typo at `MAJOR_PLINY.md:416`** — surfaced incidentally during §4.6 Probe 3 over-match analysis (the `\b` regex matched both `5.9.4` and `5.9.4.1`). §5.9.4.1 is at depth-4 (`#### 5.9.4.1 ...`) when convention says it should be depth-5 (`##### 5.9.4.1 ...`) to nest properly as a child sub-subsection under depth-4 (`####`) §5.9.4. Compare: §5.10.1/§5.10.2/§5.10.3 are correctly at depth-4 as children of depth-3 §5.10. This depth typo was inherited verbatim from the design's canon prose at `design.md:485`. ADA built per design verbatim — no deviation. Per VERA discipline §5.1 (independence-of-verification) I do not modify the build; per §5.3 I surface this as a substantive-defect-against-design that the probe set did not catch. **CATO should evaluate** whether to surface for a follow-up arc fix or accept-and-defer; this seat does not arbitrate scope. Practical impact: §5.9.4.1's header renders as a sibling-of-§5.9.4 in markdown rather than child-of-§5.9.4 in the TOC, but the prose content correctly behaves as the §5.9.4 empirical-anchor + provenance subsection.

---

## Falsification verdict

**Did anything fail?** No substantive falsification of design claims. Every load-bearing canon text the design specified is present at the expected locus with the expected content. All 5 candidates (C1-C5) plus 2 ARGUS-driven edits (Edit 3a + Edit 4b) landed verbatim per design rev2. Relative-ordering (§5.9.4 < §5.10 < `---` < §6) verified by line-number comparison. Reciprocal C3↔C4 cite-phrasings present in both files. Per-file provenance minimums met. Authorship A8 honored. `check.sh` reports expected DRIFTED state on workspace.

**Three methodology concerns** about probe-pattern precision are flagged for design-author improvement (future arcs) but do not change the verdict. **One substantive defect** (§5.9.4.1 depth typo inherited from design) is surfaced for CATO's scope-decision; it is a real defect but did not originate in the build — ADA built per design verbatim.

## Verdict

**PASS** — with 3 methodology concerns documented and 1 substantive design-inherited defect (§5.9.4.1 depth typo) flagged for CATO's scope-decision.
