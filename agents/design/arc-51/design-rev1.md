# Arc 51 (.9 PROSE-COMPRESSION CAPSTONE) — per-rule equivalence design

Ticket: `stoa--xyb.9` · Seat: CAPTAIN_DAEDALUS_the-stoa · Branch: `arc-51/build` (from `cfb11bc`, the SLIM post-cut files) · operating-mode: autonomous

Author note: this design is the PRINCIPAL's synthesis (per `CAPTAIN_DAEDALUS.md` §8). Cited tickets/incidents are provenance, not authorship.

---

## 1. Problem restatement (pre-work gate, §6.1)

Rewrite always-on rule PROSE **in place** across three already-cut role files, dropping NO rule and preserving every nuance — a semantic-equivalence pass, not a relocation pass. Nothing moves off-disk; nothing changes section number; no module is touched. The targets are the chunks upstream seats flagged as carrying genuinely-lossless slack: duplicate prose, thrice-explained relationships, and boilerplate recoverable via an existing Anchor — in `operating-disciplines.md` §8/§19/§28, `MAJOR_PLINY.md` §5.1/§7.2/§9, `CAPTAIN_DAEDALUS.md` §2/§3/§6.5.

**Imported assumptions I am naming explicitly (real briefs have implicit scope):**

1. **"Section-numbers PRESERVE" extends to SUBSECTION headings, not just top-level §-headings.** The brief says "Section-numbers PRESERVE (untouched by prose-compression)." I read this as: every existing `### 19.6.2`, `#### 28.3.1`, etc. heading stays with its number. This forecloses the "consolidate by deleting a subsection heading and folding its body upward" move that a naive de-dup would reach for. The compression therefore happens by shortening a subsection's BODY to a canonical pointer while the heading (and its number) stays. This assumption is load-bearing for the spec_refs probe safety (see §4) and for cross-file cross-refs (several subsections are cited by anchor from other files / the relocation index). If PLINY intended subsection headings to be deletable, that is a re-scope and would change several rows below — flagged as `residual_question_for_argus`.

2. **"Semantic equivalence" is whole-team and includes the cold-dispatched-agent reading path.** A CAPTAIN role file is read cold by a one-shot agent who may NOT read `operating-disciplines.md`. So "this restates op-disc §X, just cross-ref it" is NOT automatically a safe compression for a CAPTAIN file: deliberate per-seat redundancy is a reliability property, not bloat. This directly governs the §6.5 row (see KEEP-FULLER K1).

3. **Reported line-delta is an OUTPUT, not a target.** Per brief: "Smaller line-count is NOT the goal." I report the estimate per file; I do not chase it. Where a terser form risks a nuance, I keep fuller and say so.

The restatement converges with the brief. The three imported assumptions above are the implicit scope I am surfacing rather than smoothing.

---

## 2. How to read the equivalence table

Each row is one compressible chunk:

| column | meaning |
|---|---|
| **§ / lines** | section + live line-range in the post-cut file (`cfb11bc`) |
| **RULE/nuance it carries** | the canon the chunk encodes — what must survive |
| **BEFORE** | the live text (verbatim or line-range; long blocks cited by range + key phrases) |
| **AFTER** | the proposed terser form |
| **EQUIVALENCE CLAIM** | why the terser form provably carries the SAME canon — names the specific nuance and shows it survives |
| **Δ est.** | rough line reduction (reported, not targeted) |

A row is a genuine-compression candidate ONLY when the AFTER provably carries every rule + nuance the BEFORE did. Chunks where a terser form risked a nuance are NOT rows — they are in the KEEP-FULLER list (§3.4) with the at-risk nuance named.

The compression mechanic used throughout the de-dup rows: **single-source-of-truth + pointer.** When a relationship/example/boilerplate is explained in N places, ONE place stays canonical (the one a reader lands at first, or the parent) and the other N−1 shrink to a one-line "see §X" pointer that keeps the heading/number but drops the re-derivation. This is the same mechanic the C-1/C-2 relocation cuts used for Anchors, applied to within-file prose.

---

## 3. The per-rule equivalence table

### 3.1 operating-disciplines.md — §8 (Authoring downstream artifacts)

Per CATO flag, §8 is the LEAST compressible (~15-25L). Two genuine de-dup rows; the bidirectional-translation paragraph is KEEP-FULLER (K2).

**Row 8-A — duplicate "Universality:" paragraph in §8.2**

| field | content |
|---|---|
| § / lines | §8.2, line 232 |
| RULE/nuance | §8.2's universality scope = "anyone authoring downstream briefs / skills / dispatch envelopes / test scenarios / CLI/API documentation — POLYBIUS, PLINY, CAPTAINs, pair-programmer Majors." |
| BEFORE | `Universality: same as §8.1. Anyone authoring downstream briefs / skills / dispatch envelopes / test scenarios / CLI documentation / API documentation — POLYBIUS, PLINY, CAPTAINs, pair-programmer Majors, anyone writing for an agent reader.` |
| AFTER | `Universality: same as §8.1 (anyone authoring downstream briefs / skills / dispatch envelopes / test scenarios / CLI/API documentation — POLYBIUS, PLINY, CAPTAINs, pair-programmer Majors).` |
| EQUIVALENCE CLAIM | The chunk ALREADY says "same as §8.1"; §8.1's own Universality line (line 206) enumerates the identical surface list. The standalone re-enumeration is the redundancy. The AFTER keeps the explicit list inline (so a reader at §8.2 still sees the surfaces without a jump) but drops the trailing "anyone writing for an agent reader" tail, which is a pure restatement of "Anyone authoring downstream briefs… for an agent reader" already in the same sentence. NO surface dropped: POLYBIUS/PLINY/CAPTAINs/pair-programmer-Majors all retained; "CLI documentation / API documentation" → "CLI/API documentation" is a typographic join, same two surfaces. |
| Δ est. | ~0-1L (this is a tightening, not a deletion — kept conservative because §8.1's cross-file citation of the universality surface exists) |

**Row 8-B — §8.2 framing/operational restatement de-dup**

| field | content |
|---|---|
| § / lines | §8.2, line 212 |
| RULE/nuance | "Sparse prompts are aspirational; scaffolded prompts are operational" + "the unit of distribution is text, and the text needs to be richly structured." |
| BEFORE | `This sits in deliberate tension with the maxim that the unit of distribution is "what you copy-paste to your agent." Both are true: the unit IS text, and the text needs to be richly structured to produce reliable execution. Sparse prompts are aspirational; scaffolded prompts are operational.` |
| AFTER | `This sits in deliberate tension with the maxim that the unit of distribution is "what you copy-paste to your agent." Both are true: the text IS the unit, and it must be richly structured. Sparse prompts are aspirational; scaffolded prompts are operational.` |
| EQUIVALENCE CLAIM | "the unit IS text, and the text needs to be richly structured to produce reliable execution" and "Sparse prompts are aspirational; scaffolded prompts are operational" say the same thing twice (richly-structured-text == scaffolded-not-sparse). The AFTER keeps BOTH the "both are true" tension AND the aspirational/operational maxim (the load-bearing aphorism), tightening only the middle clause's "to produce reliable execution" which is implied by "scaffolded prompts are operational" two clauses later. |
| Δ est. | ~0L (wording tighten) — flag for ARGUS: marginal; could be KEEP if ARGUS reads "to produce reliable execution" as load-bearing emphasis. |

**§8 verdict:** least compressible as CATO predicted. Net realistic Δ ≈ 1-3L. The big paragraph (bidirectional-translation) is KEEP-FULLER K2.

---

### 3.2 operating-disciplines.md — §19 (Confabulation-under-uncertainty) — THE DENSEST

Per CATO: the §19.6/§19.7/§7.2 relationship is re-explained 3× (§19.4 + §19.6.2 + §19.7.2); §19.3 restates §19.2's examples verbatim; §19.6.4/§19.7.5 are duplicate N=1-provenance boilerplate.

**Row 19-A — the thrice-explained §19.6-vs-§19.7-vs-§7.2 relationship (the densest single win)**

| field | content |
|---|---|
| § / lines | §19.4 (728-734), §19.6.2 (756-760), §19.7.2 (787-793) |
| RULE/nuance | THREE distinct relationship facts, currently smeared across 3 places: (a) §7.2 verify-then-execute is the orchestrator-tier sibling, narrowly scoped to directive-vs-spec + relayed-PRINCIPAL-statements; §19 broadens to general state-vs-claim, universal-seat. (b) §19.6 (attestation) fires at ATTESTATION time vs §19's execution time — "cite live-verified state not assumed-from-context." (c) §19.7 (idle retrospective) is the SISTER of §19.6: §19.6 = WHAT to cite; §19.7 = WHO did the work. The distinct verification-actions: §19.6 → `git rev-parse HEAD`; §19.7 → `git log` authorship/timestamp check. |
| BEFORE | §19.4 explains §7.2↔§19 (two-discipline cross-ref, neither subsumes) + a §19.6 forward-pointer. §19.6.2 RE-explains §7.2↔§19.6 ("§7.2 targets directives that contradict the spec; §19.6 fires at attestation time… both state-vs-claim sub-cases; both broaden from §19.2 pattern 2") + the §5.10 worked-example pointer. §19.7.2 RE-explains §19.6-vs-§19.7 ("§19.6 = at attestation time cite live state; §19.7 = don't narrate closed tickets as own work… both sub-cases of §19.1… the verification-action that closes each is different — §19.6 fires git rev-parse HEAD; §19.7 fires a different check"). |
| AFTER | Keep §19.4 as the SINGLE canonical home of the relationship-map, expanded to one compact table that names all three relationships once. §19.6.2 → shrink to: "Sibling of §7.2 (verify-then-execute) and parent §19; the relationship-map is at §19.4. §19.6 fires at attestation time (cite live-verified state, not assumed-from-context); verification-action is `git rev-parse HEAD`. PLINY-specific worked example: `MAJOR_PLINY.md` §5.10 (signoff verifies cleanup claims before posting)." §19.7.2 → shrink to: "Distinct from §19.6 per the §19.4 map: §19.6 covers WHAT to cite (live state); §19.7 covers WHO did the work. Both are §19.1 sub-cases; the closing verification-action differs (§19.6 → `git rev-parse HEAD`; §19.7 → the orchestrator-scan / authorship check in §19.7.3-§19.7.4). Both can fire together." |
| EQUIVALENCE CLAIM | Every relationship FACT survives, each stated once in §19.4's map and pointed-to from §19.6.2/§19.7.2 (headings + numbers retained). Nuances individually preserved: (a) "neither subsumes the other" — kept in §19.4 map. (b) "both broaden from §19.2 pattern 2" — kept in §19.4 map. (c) the DISTINCT verification-actions (`git rev-parse HEAD` vs `git log` authorship) — these are the one detail I keep INLINE in BOTH §19.6.2 and §19.7.2 (not just in the map), because a reader landing directly at §19.6 or §19.7 needs the concrete action without a jump; that's the load-bearing operational nuance, and it's cheap (one clause). (d) "both can fire together" — kept inline in §19.7.2. (e) §5.10 worked-example pointer — kept inline in §19.6.2. The compression removes the RE-DERIVATION of the relationship narrative (3 paragraphs → 1 map + 2 pointers), not any fact. |
| Δ est. | ~12-18L |

**Row 19-B — §19.3 verbatim example restatement**

| field | content |
|---|---|
| § / lines | §19.3 (719-726), specifically lines 723-724 |
| RULE/nuance | §19.3's job = the NEGATIVE-exemplar list ("Confabulation sounds like…") + the structural-failure framing (confident-false-statement → corrupted downstream + degraded trust + compounding cost). The two verbatim incident quotes are illustrative, not the rule. |
| BEFORE | Lines 723-724 quote the 2026-05-12 and 2026-04-21 incidents VERBATIM ("The dispatch sentence was a stub I didn't follow through on" — the 2026-05-12 incident, verbatim. / "Defense-in-depth against accidentally allowing `git commit --amend`" — the 2026-04-21 incident, verbatim.). Both incidents are ALREADY anchored in full at §19.2 (lines 709, 717) with the same verbatim quotes embedded. |
| AFTER | Keep the two general-shape exemplars (lines 721-722: "I never did X" / "This is just Y behavior"). Replace the two incident-verbatim bullets with: "— the two incident-verbatim shapes (the 2026-05-12 tool-call-introspection negation; the 2026-04-21 confabulated security-rationale) — full incidents at §19.2." Keep the structural-failure paragraph (line 726) intact. |
| EQUIVALENCE CLAIM | The negative-exemplar PURPOSE survives (the list still shows what confabulation sounds like, including pointers to the two real incident shapes). The verbatim strings live canonically at §19.2 where the incidents are fully narrated; §19.3 re-quoting them verbatim is the redundancy. The structural-failure framing (the actual RULE of §19.3) is untouched. Risk-checked: a reader who wants the exact confabulated string still finds it one section up at §19.2; the "sounds like" list keeps both abstract shapes + the named incident shapes. |
| Δ est. | ~2L |

**Row 19-C — §19.6.4 / §19.7.5 duplicate N=1-provenance boilerplate**

| field | content |
|---|---|
| § / lines | §19.6.4 (771-773), §19.7.5 (814-816) |
| RULE/nuance | N=1 provenance + accretion-path PER discipline: (a) the Anchor ticket; (b) "enters substrate canon off-gate on PRINCIPAL's project-direction authority, future-evidence-accretion against the §6.7.1 gate still required for structural-lesson promotion"; (c) the bit-by-it + worked-when-applied supporting evidence; (d) `bw show <ticket>` recovery. |
| BEFORE | §19.6.4 and §19.7.5 are near-identical boilerplate differing only in {ticket=`stoa--ezj`/`stoa--53u`}, {articulation-date}, {the specific supporting-evidence instances}. Both recite the full off-gate/§6.7.1/§15-honest-scope sentence verbatim. |
| AFTER | Compress each to the slot-specific facts + a pointer to the shared boilerplate. Canonical home for the off-gate boilerplate = §6.7.1 (the gate itself) — which both already cite. AFTER §19.6.4: "Anchor: `stoa--ezj`. PRINCIPAL articulated 2026-05-17 (post Arc 30 init-handshake attestation). N=1 provenance + off-gate accretion path per §6.7.1 + `MAJOR_POLYBIUS.md` §15. Supporting evidence: bit-by-it (Arc 30 attestation-from-context); worked-when-applied (Arc 32 init-handshake attested live state honestly). `bw show stoa--ezj`." AFTER §19.7.5: same shape with {`stoa--53u`, 2026-05-13, Engagement-B incident §19.7.1, N=0-worked-when-applied}. |
| EQUIVALENCE CLAIM | Every per-discipline FACT survives: Anchor ticket, articulation date+trigger, supporting-evidence instances, recovery command — all retained, slot-specific. The REPEATED off-gate/§6.7.1 sentence ("enters substrate canon off-gate on PRINCIPAL's project-direction authority, with future-evidence-accretion against the §6.7.1 gate still required") is compressed to the existing cross-ref "off-gate accretion path per §6.7.1" because §6.7.1 IS the canonical statement of that gate — the boilerplate is recoverable verbatim from the gate it cites. This is the Anchor-compressible pattern CATO named (same as the C-1 cuts). Headings/numbers §19.6.4 + §19.7.5 retained. |
| Δ est. | ~6-9L |

**Row 19-D — §19.6.3 / §19.7.6 cross-reference-list trim (parallel to §28.8, see Row 28-C)**

| field | content |
|---|---|
| § / lines | §19.6.3 (762-769), §19.7.6 (818-826) |
| RULE/nuance | The cross-reference bullets binding §19.6/§19.7 to §19.1, §19.2, §7.2/§4.3, §5.10, §6.7.1, §28, §6.2, §16, etc. |
| BEFORE | §19.6.3 = 6 cross-ref bullets; §19.7.6 = 5 cross-ref bullets + a parenthetical fold-note. Several DUPLICATE inline cross-refs already present in the section body (e.g., §19.6.3's "§7.2 + §4.3 — verify-then-execute… neither subsumes" duplicates §19.6.2's body which Row 19-A already carries; §19.7.6's "§19.6 — sister discipline; §19.6 = WHAT, §19.7 = WHO" duplicates §19.7.2's first line). |
| AFTER | Trim each list to the cross-refs NOT already stated inline in the (post-19-A-compression) section body. Keep: the §19.7.3↔§6.2 polling-pattern ref, the §19.7↔`MAJOR_POLYBIUS.md` §16 lifecycle ref, the §19.6↔§28 git-blame ref (these are NOT restated in body). Drop the bullets that merely repeat the §19.4-map / §19.6.2 / §19.7.2 relationship already carried inline. |
| EQUIVALENCE CLAIM | This row is CONDITIONAL on Row 19-A landing (it relocates the relationship-explanation into §19.4's map + the two pointers). Once 19-A lands, the §19.6.3/§19.7.6 bullets that re-state the relationship are pure duplication and the unique cross-refs (polling-pattern, lifecycle, git-blame) are preserved. EACH dropped bullet is verified to have its target reachable from a surviving inline ref or the §19.4 map. NO cross-ref TARGET becomes unreachable. (This is the highest-risk row — see weak point W2; ARGUS should verify every dropped bullet against a surviving inline ref.) |
| Δ est. | ~4-7L |

**§19 verdict:** densest section, biggest win. Net realistic Δ ≈ 24-41L. Rows 19-A and 19-D are the ones ARGUS should scrutinize hardest.

---

### 3.3 operating-disciplines.md — §28 (Per-CAPTAIN git seat identity)

Per CATO: §28.8 (9 cross-ref bullets) duplicates inline cross-refs; §28.6 speculative scaffolding; §28.3.1 narrative ~30% tightenable. NOTE: §28.3.1 heading is SPEC-CITED (SPECIFICATION.md line 640 cites §28.3.1) — body-prose-only compression; heading must survive.

**Row 28-A — §28.8 cross-reference list de-dup**

| field | content |
|---|---|
| § / lines | §28.8 (1225-1235) |
| RULE/nuance | 9 cross-ref bullets: global CLAUDE.md (never-override-Author), `MAJOR_PLINY.md` §5.12, `CAPTAIN_ADA.md` §5.5, §19.6, §25, `MAJOR_POLYBIUS.md` §18, `MAJOR_PLINY.md` §5.10+§5.11. |
| BEFORE | 7 bullets + a fold-note parenthetical. SEVERAL duplicate inline cross-refs already in the §28 body: §28's intro paragraph (line 1126) ALREADY cites `MAJOR_PLINY.md` §5.12 + `CAPTAIN_ADA.md` §5.5 + global CLAUDE.md's never-override rule; §28.5 (line 1210) ALREADY cites §19.6; §28.2 (line 1156) ALREADY cites `MAJOR_POLYBIUS.md` §18.1; §28.7 (line 1223) ALREADY cites §25 (the gate that adjudicated kjo). |
| AFTER | Trim to cross-refs NOT already stated inline. Keep: §25 (only if §28.7's mention is judged insufficient — see equivalence note), `MAJOR_PLINY.md` §5.10+§5.11 sibling-arc-boundary refs (these are NOT in the §28 body). Drop: global CLAUDE.md bullet (stated at intro line 1126), §5.12 bullet (intro), §5.5 bullet (intro), §19.6 bullet (§28.5 body), `MAJOR_POLYBIUS.md` §18 bullet (§28.2 body). Replace with a one-line: "Cross-refs not already inline above: `MAJOR_PLINY.md` §5.10 (signoff-accuracy) + §5.11 (paste archival) — sibling arc-boundary disciplines; §28 fires throughout the arc-build." |
| EQUIVALENCE CLAIM | EACH dropped bullet's target is verified reachable from a NAMED inline cross-ref earlier in §28 (line numbers cited above). No cross-ref target becomes unreachable; the reader who lands at §28.8 still has every relationship — most of them stated where they're contextually relevant (intro, §28.5, §28.2) rather than re-listed. The §25-adjudication relationship is kept (via §28.7's existing mention OR a one-line bullet if ARGUS judges §28.7's mention too oblique). The fold-note parenthetical (line 1235, "Provenance ticket stoa--kjo… folded into §28.7") stays — it's a unique navigation aid, not a duplicate. |
| Δ est. | ~5-7L |

**Row 28-B — §28.3.1 narrative tighten (body-prose-only; heading spec-cited, retained)**

| field | content |
|---|---|
| § / lines | §28.3.1 (1168-1196) |
| RULE/nuance | The pitfall: `--body` override on `gh pr merge --squash` REPLACES auto-populated body wholesale, silently stripping Co-Authored-By trailers; empirical anchor Arc 37 PR#17→`bb12806` (0 trailers, branch deleted, chain severed); the fix (omit `--body` OR include trailers in `--body` HEREDOC); cross-refs. |
| BEFORE | ~28 lines. The mechanism is stated twice: the opening paragraph (1170-1176) explains "`--body` replaces wholesale including preserved trailers," then "The fix at the merge site" paragraph (1186-1191) re-explains the same auto-populate-vs-override mechanism while giving the fix. |
| AFTER | Tighten the mechanism to one statement; keep the empirical anchor (Arc 37 / `bb12806` / the `grep -c` evidence / branch-deleted-chain-severed) intact; keep the fix (both options) intact; keep cross-refs. Specifically merge the redundant "auto-population preserves trailers / passing custom --body REPLACES" mechanism so it's stated once, then the empirical, then the fix. |
| EQUIVALENCE CLAIM | The RULE (don't pass a trailer-omitting `--body`), the MECHANISM (override replaces wholesale), the EMPIRICAL (Arc 37 `bb12806`, the concrete `grep -c 'Co-Authored-By'` returns 0, the severed chain), the FIX (omit `--body` preferred / HEREDOC-with-trailers alternative), and the CROSS-REFS (§5.10, §28.3, §19.6) all survive. The compression removes the second telling of the auto-populate/override mechanism, not any fact. §28.3.1 HEADING + number retained (spec-cited at SPECIFICATION.md line 640) → spec_refs PASS preserved. |
| Δ est. | ~6-9L |

**Row 28-C — §28.6 speculative future-extension scaffolding**

| field | content |
|---|---|
| § / lines | §28.6 (1212-1219) |
| RULE/nuance | The convention is shape-compatible with other ranks: a future committing MAJOR carries `MAJOR_<MNEMONIC>_<slug>`; currently-non-committing CAPTAINs (BARTLEBY/STRABO/HERALD/CURATOR) inherit §28 if-and-when they commit. Arc 35 does NOT pre-emptively extend to non-committing seats. |
| BEFORE | ~8 lines, two bullets + framing + the "Arc 35 does not pre-emptively extend" line. |
| AFTER | Compress to: "**§28.6 Future arcs may extend.** The convention is shape-compatible with other ranks: a future committing MAJOR carries `MAJOR_<MNEMONIC>_<slug>` <`major-<mnemonic>@<slug>.local>`; currently-non-committing CAPTAINs (BARTLEBY/STRABO/HERALD/CURATOR) inherit §28 if-and-when they begin committing. Not pre-emptively extended — empirical surface today is gauntlet CAPTAINs only." |
| EQUIVALENCE CLAIM | The RULE (shape-compatible, MAJOR-form trailer, non-committing seats inherit on first commit, not pre-emptively extended) survives in full — including the concrete MAJOR trailer format (the one operationally-useful detail). Compression removes the example-elaboration ("a hypothetical hotfix MAJOR, a long-running CURATOR session committing curator-tier artifacts") which is illustrative padding, not rule. The named seat list (BARTLEBY/STRABO/HERALD/CURATOR) is KEPT because it's a concrete enumeration a reader needs. CAUTION (W3): this is the row closest to "cutting a rule" — the §28.6 content is itself low-density speculative scaffolding; I compress rather than cut, keeping the MAJOR-form trailer because it's the one thing a future committing-MAJOR author would need. |
| Δ est. | ~3-4L |

**§28 verdict:** Net realistic Δ ≈ 14-20L. Row 28-C (§28.6) is the one ARGUS should check against "is this still carrying its rule."

---

### 3.4 MAJOR_PLINY.md — §5.1 / §7.2 / §9

**Row P-5.1 — Arc-37 parenthetical xref-restatements**

| field | content |
|---|---|
| § / lines | §5.1 (165, 174) |
| RULE/nuance | §5.1 carries: mode-flag is in every CAPTAIN/Major dispatch; POLYBIUS authors+propagates it; HITL vs autonomous gauntlet pacing; per-seat mode override; cross-refs to `MAJOR_POLYBIUS.md` §13, op-disc §10 + §11. |
| BEFORE | Line 165 parenthetical: "(POLYBIUS authors it; if PRINCIPAL declared autonomous on the engagement, POLYBIUS propagates the flag downward to you)." Line 174 cross-ref parenthetical: "(incl. the Arc 37 step 7 `**Mode declaration in directives.**` convention this section operates against)." |
| AFTER | Line 165: keep "The mode is set by your activation paste (POLYBIUS authors + propagates it)." — collapse the conditional restatement. Line 174: "Cross-refs: `MAJOR_POLYBIUS.md` §13 (POLYBIUS-tier mode declaration + propagation), `operating-disciplines.md` §10 (universal framing) + §11 (autonomous-mode-setup checklist)." — drop the trailing Arc-37-step-7 parenthetical. |
| EQUIVALENCE CLAIM | Line 165: "POLYBIUS authors + propagates it" carries both the authoring AND the downward-propagation; the "if PRINCIPAL declared autonomous" conditional is the GENERAL case (propagation happens whatever the mode), so collapsing the conditional loses no rule. Line 174: the Arc-37-step-7 parenthetical points at op-disc §11's "Mode declaration in directives" convention — which the cross-ref to §11 ALREADY reaches; the parenthetical is a provenance-restatement of where §11 came from (Arc 37), recoverable from §11 itself. No cross-ref target lost. |
| Δ est. | ~1-2L |

**Row P-7.2 — the two scope-broadening paragraphs (Arc-24 + Arc-39)**

| field | content |
|---|---|
| § / lines | §7.2 (299, 301) |
| RULE/nuance | §7.2 = verify-then-execute (directive-vs-spec + relayed-PRINCIPAL). Arc-24 broadening: ANY state-vs-claim mismatch → op-disc §19 (universal-seat). Arc-39 broadening: PRINCIPAL-intent probe (3-step category-first sequence) when queuing/designing on un-probed intent. |
| BEFORE | Line 299 (Arc-24): re-states the §7.2-vs-§19 split ("§7.2 covers 'the directive is wrong'; §19 covers 'I cannot verify my own assumption…'"). This split is ALSO stated canonically at op-disc §19.4 + §19.2 pattern-2. Line 301 (Arc-39): the PRINCIPAL-intent-probe paragraph + the 3-step enumeration (303-307). |
| AFTER | Line 299: tighten to: "**Scope-broadening (Arc 24 / `stoa--ioy`).** Any state-vs-claim mismatch beyond directive-vs-spec (tool-call ambiguity, screenshot evidence, peer report, unfamiliar concept) is covered universal-seat by `operating-disciplines.md` §19. §7.2 = 'the directive is wrong'; §19 = 'I can't verify my own assumption — uncertain, checking.' Both apply here." (already terse; ~0-1L). Line 301 + 3-step list: KEEP the 3-step category-first enumeration verbatim (it's the operational core, see KEEP-FULLER K4); tighten only the surrounding prose ~30% per PLINY's flag — the "queuing a work item on inferred-intent commits the team to a phantom design…" sentence and the "Skipping step 1…" paragraph (307) can each lose ~1 clause without losing the rule. |
| EQUIVALENCE CLAIM | Arc-24 paragraph: the §7.2-vs-§19 split is the load-bearing distinction and is KEPT inline (a PLINY reading §7.2 needs it without a jump); the compression is only of the example-list phrasing. The "the broader case is covered by §19" pointer is retained. Arc-39 paragraph: the 3-step category-first sequence — the actual rule — is KEPT verbatim (K4); only the explanatory wrapper prose tightens. The 2026-05-13 4-option-to-5th category-miss empirical stays (it's in the §7.2 cross-ref line 309 Anchor). NO rule dropped; the "~30% tightenable" is wrapper prose, not the enumeration. |
| Δ est. | ~3-5L |

**Row P-9 — activation-checklist overlap with §4** — **PARTIAL / mostly KEEP-FULLER (K5)**

| field | content |
|---|---|
| § / lines | §9 (353-379) vs §4 (48-63) |
| RULE/nuance | §9 = the one-page activation summary (8 numbered steps + clean-PASS sequence + ambiguity sequence + handoff-before-compact). §4 = the narrative activation (4 steps + re-paste-on-drop). |
| BEFORE | §9 steps 1-2 ("Read MAJOR_PLINY.md, confirm rank/mnemonic/role" + "Read session-specific intent") DUPLICATE §4 steps 1-2 near-verbatim. BUT §9 steps 3-8 (bw prime, git status, surface-and-wait polling, successor /resume, confirm-intent) are RICHER than §4 and carry rules §4 lacks. |
| AFTER | Compress ONLY §9 steps 1-2 to point at §4: "1-2. Read `MAJOR_PLINY.md` + the session intent (per §4 steps 1-2)." Keep §9 steps 3-8 + the clean-PASS / ambiguity / handoff blocks verbatim. |
| EQUIVALENCE CLAIM | §9 is deliberately a "one-page summary" (an index). PLINY flagged "could cross-ref §4 not re-state" — but §9 has MORE than §4, so it canNOT collapse into a pure §4 pointer without losing steps 3-8. The ONLY genuinely-duplicate content is steps 1-2 (read-role + read-intent), which §4 states identically. Compressing JUST steps 1-2 to a §4-pointer preserves the one-page-summary function while removing the verbatim duplication. EVERYTHING ELSE in §9 is KEEP-FULLER (K5) — the summary's value is being a single scannable page; collapsing the unique steps would force a reader to reconstruct the checklist from §4+§6+§7. |
| Δ est. | ~1-2L (deliberately small — this is mostly a KEEP) |

**MAJOR_PLINY verdict:** Net realistic Δ ≈ 5-9L. §9 is intentionally barely-touched (it's an index, not bloat).

---

### 3.5 CAPTAIN_DAEDALUS.md — §2 / §3 / §6.5

**Row D-2 — operating-mode paragraph (restates op-disc §10)**

| field | content |
|---|---|
| § / lines | §2 (43) |
| RULE/nuance | The mode flag is in the dispatch; HITL → may surface mid-task; autonomous → surface only on the universal escalation triggers (the 4: substance-disagreement-after-one-round, authorship/copyright, irreducible ambiguity, peer-silence>60min). |
| BEFORE | "In autonomous mode, surface only on the universal escalation triggers (see `operating-disciplines.md` §10): substance disagreement after one round, authorship/copyright content, irreducible ambiguity, peer silence > 60 min." |
| AFTER | KEEP as-is. See KEEP-FULLER K3. (Listed here so ARGUS sees it was evaluated and rejected for compression.) |
| EQUIVALENCE CLAIM | n/a — KEEP-FULLER K3. The 4 triggers are inlined deliberately so a cold-dispatched DAEDALUS who hasn't read op-disc still knows the autonomous-mode escalation triggers. PLINY flagged it as "restates op-disc §10 (~3L)" but per imported-assumption #2, this per-seat inlining is a reliability property. Replacing the 4-trigger list with a bare "see op-disc §10" would force a cold agent to read op-disc to know when to escalate — a net reliability regression. |
| Δ est. | 0L (KEEP) |

**Row D-3 — design-output-contract explanatory clauses**

| field | content |
|---|---|
| § / lines | §3 (51-55) |
| RULE/nuance | The 5-element design shape: (1) Problem restatement [pre-work gate §6.1], (2) Approach, (3) Verification probes [load-bearing], (4) Self-assessed weak points [pair to ARGUS §6.2], (5) Out of scope. |
| BEFORE | Each numbered element has an explanatory clause. E.g. (3): "Concrete probes (commands, file existence checks, behaviors under specific inputs) VERA can re-execute. The probe spec is load-bearing; 'we'll know when we see it' is not a probe." (5): "The list keeps ADA from scope-creeping during build and gives ARGUS a frame for what risks belong in this dispatch versus a future one." |
| AFTER | Tighten the explanatory tails that RESTATE the element's purpose. (3) keep "Concrete probes (commands, file checks, behaviors under specific inputs) VERA can re-execute — 'we'll know when we see it' is not a probe." (drop "The probe spec is load-bearing;" — the "is not a probe" clause already carries the load-bearingness). (5) keep "Bullet list of related concerns this design deliberately does not address, with one-line reasons — keeps ADA from scope-creeping and gives ARGUS a frame for in-dispatch-vs-future risks." (tighten the two-clause tail to one). |
| EQUIVALENCE CLAIM | Each element's RULE survives: the 5 elements, their order, their load-bearing markers (§6.1 pre-work gate, ARGUS §6.2 pairing), and the concrete probe-shape examples all retained. The compression trims explanatory tails that restate what the element-name + one example already convey. The "is not a probe" anti-example (the load-bearing teaching) is KEPT. |
| Δ est. | ~2-3L |

**Row D-6.5 — heartbeat prohibitions (Monitor / run_in_background)** — **KEEP-FULLER (K1)**

| field | content |
|---|---|
| § / lines | §6.5 (153-155) |
| RULE/nuance | `Monitor` forbidden (orphans the Monitor, issue #23154); `run_in_background: true` on Bash forbidden (same orphan surface); role-collapse-into-ADA framing. |
| BEFORE | Two bold paragraphs (lines 153-155). |
| AFTER | KEEP as-is. See KEEP-FULLER K1. |
| EQUIVALENCE CLAIM | n/a — KEEP-FULLER K1. FINDING (verified this dispatch, two parts): (a) The **`Monitor` forbidden** paragraph is a CANONICAL TEMPLATE replicated BYTE-FOR-BYTE across 12+ CAPTAIN role files — VERIFIED: `diff` of DAEDALUS's vs ADA's `Monitor`-forbidden line returns EMPTY. Per my own §6.8 (canonical-template wording-alignment), compressing ONLY DAEDALUS's copy breaks the cross-file byte-alignment §6.8 mandates — a NET REGRESSION (drift across 12 files to save ~2L in one). Requires a cross-file lockstep arc, OUT OF SCOPE for this 3-file pass. (b) The **`run_in_background` forbidden** paragraph is ALREADY a per-seat VARIANT (VERIFIED: DAEDALUS's "role-collapsed into ADA-shaped work" framing ≠ CATO's "§6.8 empirical-environment probe" framing — `diff` non-empty). So that paragraph is NOT under strict byte-alignment; its keep-reason is the cold-dispatch-reliability argument (imported-assumption #2): a cold CAPTAIN reads its own file, not necessarily op-disc §18.4; issue #23154 lives only in the per-seat copies + op-disc §18.5/modules, NOT in §18.4. Both halves KEEP, on distinct grounds (a=byte-alignment, b=cold-dispatch-reliability). |
| Δ est. | 0L (KEEP — explicitly out of scope; flagged as a follow-up) |

**CAPTAIN_DAEDALUS verdict:** Net realistic Δ ≈ 2-3L. The two PLINY-flagged "restates op-disc" chunks (§2, §6.5) are BOTH KEEP-FULLER on the cold-dispatch-reliability + canonical-template grounds — this is the seat where "it restates op-disc, just cross-ref it" is most often the WRONG move.

---

### 3.6 Roll-up: estimated line delta per file (REPORTED, not targeted)

| file | genuine-compression rows | KEEP-FULLER | est. Δ (lines removed) |
|---|---|---|---|
| operating-disciplines.md (§8/§19/§28) | 8-A, 8-B, 19-A, 19-B, 19-C, 19-D, 28-A, 28-B, 28-C | K2 (bidirectional-translation) | ~39-64L |
| MAJOR_PLINY.md (§5.1/§7.2/§9) | P-5.1, P-7.2, P-9 (partial) | K5 (§9 steps 3-8) | ~5-9L |
| CAPTAIN_DAEDALUS.md (§2/§3/§6.5) | D-3 | K1 (§6.5 template), K3 (§2 triggers) | ~2-3L |
| **total** | **13 compression rows** | **5 KEEP-FULLER** | **~46-76L** |

This lands well short of the §8/§19/§28 "~100-150L" CATO upper estimate — because (a) the brief's subsection-heading-preservation constraint forecloses the biggest single-move dedup (deleting redundant subsection headings), forcing pointer-shrink instead of fold-and-delete, and (b) several flagged chunks are KEEP-FULLER on semantic-equivalence grounds. This is the HONEST semantic-equivalence floor for an in-place pass, reported as the brief asks — not a target to chase.

---

## 4. KEEP-FULLER list (chunks where a terser form risked a nuance)

| # | chunk | the nuance at risk if compressed |
|---|---|---|
| **K1** | DAEDALUS §6.5 Monitor/run_in_background prohibition | `Monitor` paragraph: verified byte-identical across 12+ CAPTAIN files — compressing one copy breaks §6.8 cross-file byte-alignment (net drift); needs a cross-file lockstep arc → out of scope. `run_in_background` paragraph: already a per-seat variant; kept on cold-dispatch reliability (cold CAPTAINs read their own file, not op-disc §18.4; issue #23154 lives only in per-seat copies + §18.5/modules). |
| **K2** | op-disc §8.2 bidirectional-translation paragraph (line 228) | `MAJOR_POLYBIUS.md` §1 (line 55) cross-refs op-disc §8.2 as the canonical HOME of "the bidirectional-translation principle." The paragraph carries FOUR distinct nuances: (a) humans-can't-specify-intent-up-front; (b) reality-can't-be-described-to-humans-up-front; (c) models can't autonomously close the loop — only the COS-tier can; (d) permanent HITL value is STRUCTURAL, not a function of model smartness. POLYBIUS's primary alignment responsibility rests on this. Tightening risks dropping (c) or (d), which are the non-obvious nuances. Kept fuller; at most cosmetic word-tighten with all 4 nuances individually verified present. |
| **K3** | DAEDALUS §2 autonomous escalation-trigger list (line 43) | The 4 triggers inlined for cold-dispatch reliability. A bare "see op-disc §10" forces a cold agent to read op-disc to know when to escalate — a reliability regression. Per-seat inlining is intentional redundancy. |
| **K4** | MAJOR_PLINY §7.2 PRINCIPAL-intent 3-step category-first enumeration (303-307) | The 3-step sequence (category → shape-within-category → specifics-within-shape) is the OPERATIONAL CORE of the Arc-39 discipline — the "skip step 1 = recognizable 2026 failure mode" teaching depends on the explicit steps. Wrapper prose tightens; the enumeration stays verbatim. |
| **K5** | MAJOR_PLINY §9 steps 3-8 + clean-PASS / ambiguity / handoff blocks | §9 is a deliberate one-page scannable INDEX. Steps 3-8 (bw prime, git status, surface-and-wait, successor /resume) are richer than §4 and carry rules §4 lacks. Collapsing them into a §4 pointer destroys the index function. Only the genuinely-duplicate steps 1-2 compress. |

An empty KEEP-FULLER list would be suspicious for a semantic-equivalence pass over universal rules; these 5 are the chunks where "it looks compressible" met "but a specific nuance/reader-path would break."

---

## 5. Verification probes (load-bearing — what VERA re-executes)

These probes falsify the design's intended behavior (semantic equivalence preserved; no rule dropped; probe stays GREEN). ADA implements the rewrite; VERA re-runs these against the post-rewrite files.

**Probe 1 — spec_refs xref stays GREEN (no regression).** Baseline (pre-rewrite, captured this dispatch) = **156 PASS / 56 FAIL** (the 56 FAILs are pre-existing bare-§ refs to non-op-disc anchors; NOT introduced here).
```
PYTHONUTF8=1 python3 substrate/skills/validate-spec/_lib/spec_refs.py --spec SPECIFICATION.md --repo-root .
```
Acceptance: post-rewrite summary line is byte-identical `{"total":212,"pass":156,"fail":56,"strange":0}`. ZERO op-disc PASS→FAIL. Rationale (proven this dispatch): the resolver matches anchors by HEADING-TEXT re-scan (`_find_anchor_in_target`, spec_refs.py L230-240), NOT absolute line number — so body-prose compression is probe-safe; only deleting/renumbering a cited heading or touching SPECIFICATION.md can flip a verdict. The design touches neither.

**Probe 2 — every section + subsection HEADING preserved (number + text).** Capture the heading inventory before/after for all 3 files:
```
diff <(git show cfb11bc:substrate/operating-disciplines.md | grep -nE '^#{1,6} ') <(grep -nE '^#{1,6} ' substrate/operating-disciplines.md | sed 's/^[0-9]*://')
```
(run per-file; line-number prefix stripped so only heading TEXT is compared). Acceptance: heading TEXT set identical pre/post (line numbers may shift; heading text + numbers must not). This enforces the imported-assumption-#1 constraint (subsection headings preserved).

**Probe 3 — no spec-cited heading lost.** Assert each spec-cited heading in my targets still resolves:
```
PYTHONUTF8=1 python3 substrate/skills/validate-spec/_lib/spec_refs.py --spec SPECIFICATION.md --repo-root . | python3 -c "import sys,json; [print('LOST',d['anchor']) for d in (json.loads(l) for l in sys.stdin if l.startswith('{') and 'anchor' in json.loads(l)) if d.get('anchor') in ('19.2','19.6','19.7','28','28.3.1') and d['verdict']!='PASS']"
```
Acceptance: no `LOST` output (§19.2/§19.6/§19.7/§28/§28.3.1 all still PASS).

**Probe 4 — no live cross-file cross-ref broken.** For each subsection-anchor whose BODY was compressed, assert its heading still exists so inbound cross-refs resolve. The live inbound refs found this dispatch (must stay reachable): op-disc §8.1 ← §23.5/§25.3/§25.4; op-disc §8.2 ← `MAJOR_POLYBIUS.md` §1 + op-disc §23.5; op-disc §28.7 ← §0.5 relocation index.
```
grep -nE '^#{1,6} (8\.1|8\.2|8\.3|19\.4|19\.6\.2|19\.6\.3|19\.6\.4|19\.7\.2|19\.7\.5|19\.7\.6|28\.6|28\.7|28\.8) ' substrate/operating-disciplines.md
```
Acceptance: every listed heading present (count matches pre-rewrite).

**Probe 5 — every RULE token survives (semantic-equivalence spot-check).** For the highest-risk compressions, grep for the rule's load-bearing tokens post-rewrite:
- `git rev-parse HEAD` AND `git log` both still present in §19 (the two distinct verification-actions, Row 19-A): `grep -c 'git rev-parse HEAD' substrate/operating-disciplines.md` ≥ baseline; `git log`-authorship-check present in §19.7.
- `bidirectional-translation` + all 4 K2 nuances present in §8.2: assert "humans cannot fully specify" + "reality cannot be fully described" + "COS" + ("structural" OR "not a function of how smart") all present.
- 3-step category-first enumeration present in PLINY §7.2: `grep -cE 'Category:|Shape-within-category|Specifics-within-shape'` = 3.
- §6.5 `Monitor` line byte-identical to sibling CAPTAIN files (K1 alignment held — verified empty this dispatch): `diff <(grep 'Monitor.*is forbidden from this seat' substrate/CAPTAIN_DAEDALUS.md) <(grep 'Monitor.*is forbidden from this seat' substrate/CAPTAIN_ADA.md)` returns empty. (Do NOT assert the `run_in_background` line is cross-file-identical — it is already a per-seat variant by design; assert only that DAEDALUS's `run_in_background` line is UNCHANGED from `cfb11bc`: `diff <(git show cfb11bc:substrate/CAPTAIN_DAEDALUS.md | grep 'run_in_background') <(grep 'run_in_background' substrate/CAPTAIN_DAEDALUS.md)` empty.)

**Probe 6 — app gen-data still parses (substrate frontmatter unbroken).** Per project CLAUDE.md: prose compression touches BODY only, not frontmatter — but assert it:
```
cd app && npm run gen-data
```
Acceptance: exits 0; Zod schema validation clean (no frontmatter regression).

**Probe 7 — no leak to main.** Per brief ("verify no leak to main after each write"):
```
git -C C:/Users/denso/claude_projects/the-stoa status --porcelain
```
Acceptance: main worktree shows no modifications to the three target files (all edits confined to the arc-51/build worktree). ADA + VERA both run this after writes.

---

## 6. Out of scope

- **Cross-file canonical-template compression** of the §6.5 Monitor/run_in_background block across all 12+ CAPTAIN files. That's a separate lockstep arc (compress all copies byte-identically or it violates §6.8). KEEP-FULLER K1; named as a follow-up.
- **Relocation / recompose / module changes.** This is in-place rewrite only, per brief.
- **The pre-existing 56 spec_refs FAILs.** Those are bare-§ refs to `MAJOR_PLINY` anchors (§5.10/§5.11 etc.) that resolve to the op-disc default and don't exist there — a separate concern (either SPECIFICATION.md citation-form fix or the validate-spec default-resolution heuristic). Not touched by prose compression; flagged for a future validate-spec arc.
- **§7.6-Anchor cite NIT** (the `ariadne--m20` cross-repo cite from `stoa--xyb.9`'s description). It's in op-disc §7.6, which is NOT a flagged compression target for THIS capstone (the brief's targets are §8/§19/§28). Left for the ticket's separate fold, OR ARGUS may rule it in-scope; flagged as `residual_question_for_argus`.
- **Renumbering / re-leveling subsection headings** to flatten §19/§28's deep nesting. Tempting (the §19.6.x/§19.7.x depth is part of why the relationship is re-explained), but renumbering would flip spec_refs + break cross-refs. Out of scope by the section-numbers-preserve constraint.

---

## 7. Self-assessed weak points (post-work gate, §6.2)

| # | weak point | why this shape anyway |
|---|---|---|
| **W1** | **Row 19-A (the thrice-explained relationship) is the largest single win AND the one where I'm least sure the nuance survives.** Collapsing 3 explanations into 1 map + 2 pointers assumes a reader landing directly at §19.6 or §19.7 is well-served by a pointer to §19.4's map plus the inline verification-action. If the relationship-nuance (e.g., "neither subsumes the other," "both broaden from §19.2 pattern 2") is load-bearing AT the §19.6/§19.7 reading site (not just discoverable via §19.4), the pointer-shrink under-serves that reader. | I kept the DISTINCT verification-actions (`git rev-parse HEAD` / `git log`) and "both can fire together" INLINE at §19.6.2/§19.7.2 — the operationally load-bearing nuances — and pointed only the relationship-NARRATIVE to §19.4. The map (§19.4) is the right SSoT for a relationship explained 3×. ARGUS should scrutinize this row hardest. |
| **W2** | **Rows 19-D + 28-A (cross-ref-list trims) are CONDITIONAL and the riskiest for silently orphaning a cross-ref.** Both drop bullets on the claim "this target is reachable from a surviving inline ref." If I mis-identified even one inline ref as covering a dropped bullet, a cross-ref target goes unreachable — a silent navigation regression that no probe catches unless Probe 4's heading-existence check happens to cover it. | I verified each dropped bullet against a NAMED inline ref with a cited line number (§28-A lists them: §5.12/§5.5 at line 1126, §19.6 at §28.5/1210, §18.1 at §28.2/1156). But this is human-verifiable-by-reading, not mechanically-provable — exactly the kind of claim ARGUS exists to re-check. I'd rather ship the trim with the verification table than leave 9 duplicate bullets. ARGUS: re-verify each dropped bullet's target reachability. |
| **W3** | **Row 28-C (§28.6 speculative scaffolding) is the row closest to "cutting a rule rather than compressing prose."** §28.6 is itself low-density future-extension content; my compression keeps the MAJOR-form trailer + the named-seat list but drops the example-elaboration. If ARGUS/CATO judge the dropped elaboration ("a hypothetical hotfix MAJOR, a long-running CURATOR session") as load-bearing worked-example rather than padding, this crosses from compression into cut. | I kept the one operationally-useful detail (the `MAJOR_<MNEMONIC>_<slug>` trailer format a future committing-MAJOR author would need) and the concrete seat enumeration. The dropped clause is illustrative, not a rule. But I flag it as the row where "compress vs cut" is closest — defensible as compression, worth a second read. |

Additional honest note: the reported ~46-76L delta is well under CATO's ~100-150L upper estimate. That is NOT under-performance — it's the consequence of the subsection-heading-preservation constraint (imported-assumption #1) foreclosing fold-and-delete, plus the 5 KEEP-FULLER chunks. If PLINY/ARGUS read the gap as "DAEDALUS left compression on the table," the lever is imported-assumption #1: relaxing it (allowing redundant subsection HEADINGS to be deleted where no live cross-ref/spec-cite depends on them, e.g. §19.6.3/§19.7.6 could fold entirely into their parents) would recover ~10-15L more — but at the cost of cross-ref/spec-cite risk. I chose the safe floor and am surfacing the lever rather than silently picking it.
