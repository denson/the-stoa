# Arc 40 — Pass 6 substrate bundle: integrated design

**Ticket:** `stoa--utn` (dispatch); candidates `stoa--3sz` + `stoa--5sr` + `stoa--6wp` LOCKED; `stoa--6n9` + `stoa--t9u` folded under A7. `stoa--dhc` DROPPED — CLOSED by user-tier-polybius @ 2026-05-18T06:47:41Z, PRINCIPAL-ratified (rev1 §25 PRINCIPAL-gate at 06:43:54Z surfaced the SSoT-already-existing finding; PRINCIPAL ratification ~1 min post rev1 commit closed the ticket without substrate work).
**Author (substrate edits):** Denson Smith.
**Designed by:** CAPTAIN_DAEDALUS_the_stoa, 2026-05-18 (rev2 post-ARGUS, post-dhc-closure).
**Inputs consumed:** `substrate/arcs/arc-40-build-directive.md` (A1-A20 LOCKED); ticket bodies for all 6 candidates via `bw show`; `agents/design/arc-24/design.md` (full read, §13.1 + §14.1 R1+R2 + §14.2 r5 for 5sr framing); Arc 37 squash-merge commit `bb12806` body (`git log -1 --format='%B'`) + stat (`git show --stat`); Arc 39 squash-merge commit `f1f222a` body + stat; `substrate/arcs/arc-39-build-directive.md` for bundle-shape precedent; `substrate/MAJOR_PLINY.md` §5.8 (poll-loop canonical site) + §5.10 (signoff-accuracy ship-checklist, lines 424-462) + §5.11 (paste archival); `substrate/MAJOR_POLYBIUS.md` §7.6 (cross-ref-only dhc site); `substrate/operating-disciplines.md` §18 (universal-team framing dhc site) + §28 (Co-Authored-By trailers, lines 1699-1788); `substrate/skills/agent-author/SKILL.md` (no python-vs-jq prose; dhc site found vacant); `substrate/CAPTAIN_VERA.md` §5 (probe-authoring locus for 3sz, A6 γ); `substrate/CAPTAIN_DAEDALUS.md` §6 (design-authoring locus for 5sr, A4); `substrate/install.sh` lines 380-435 (write_substrate_manifest for 6n9) + lines 770-801 (cp -R deploy for t9u); `substrate/skills/check-substrate-updates/check.sh` lines 132-180 + `apply.sh` lines 106-150 (manifest reader sites for 6n9). Web search confirmed `gh pr merge --squash --body` overrides the default Co-Authored-By auto-population per [gh pr merge manual](https://cli.github.com/manual/gh_pr_merge) and [Mergify Discussion #4636](https://github.com/Mergifyio/mergify/discussions/4636).

---

## 1. Frame

### 1.1 Five candidates; one bundle; one A20 recursive shape

Arc 40 is Pass 6 of `SPECIFICATION.md` §13 workplan — the Arc-24-era hygiene follow-ups plus the SEQUENCE-CRITICAL Arc 37 trailer-regression-fix per §13.7. The three LOCKED candidates are not arbitrarily co-located: two are Arc 24 follow-ups (3sz/5sr) that the Arc 24 ship deferred to "Arc 25+" per directive Out-of-scope; the third (6wp) is an Arc 37 regression-fix whose canon Arc 38 + Arc 39 already practiced organically and which this arc codifies so Pass 9/10 stellation arcs can rely on the discipline being in MAJOR_PLINY.md §5.10 rather than inherited from precedent. (A fourth Arc 24 follow-up — `stoa--dhc` python-vs-jq SSoT — was DROPPED mid-design: rev1's §25 PRINCIPAL-gate surfaced that substrate already has SSoT at MAJOR_PLINY.md §5.8.3; user-tier-polybius CLOSED dhc with PRINCIPAL ratification ~1 minute post rev1 commit. dhc has no substrate work to do; see §1.2 imported assumption (2) for the empirical finding that drove the closure.) The A7-discretion fold-in adds two install.sh-adjacent tickets (6n9 manifest format-version; t9u pycache-exclude) whose scope cohesion with the 3 LOCKED candidates is examined below.

The arc carries one structural property that distinguishes it from Arc 35-39's previous trailer-discipline work: **A20 recursive-shape surveillance.** MAJOR_PLINY edits MAJOR_PLINY's own role file (§5.10 ship-checklist gains the 6wp one-liner) pre-merge as part of the very arc PLINY runs end-to-end. Phase 4 squash-merge applies the canon being shipped. This is the first arc where the trailer-preservation canon is *both* the deliverable *and* the operational discipline the shipping arc is graded against. The design must keep this recursion legible to ARGUS audit and CATO review — §10 below names the watchpoints explicitly.

### 1.2 Pre-work: restatement-gate (CAPTAIN_DAEDALUS.md §6.1)

The dispatch brief (rev1) asked: ship one design.md covering 4 LOCKED + 2 optional candidates; pick A3/A4/A5/A6/A7 at design time; make the recursive A20 shape visible; surface PRINCIPAL-gate per §25 if any pick exceeds discretion band. The brief (rev2) narrows scope: dhc CLOSED mid-design per PRINCIPAL ratification of rev1's §25 surface; A5 is VOID; arc covers 3 LOCKED + 2 optional = 5 candidates.

My restatement (rev2): **codify the Arc 37 trailer-regression fix (6wp) into MAJOR_PLINY.md §5.10 as a one-line ship-checklist addition + optional op-disc §28 worked-example pitfall subsection; land two Arc 24 hygiene refinements (5sr DAEDALUS canonical-template wording-alignment; 3sz VERA probe-spec anchor canon); optionally bundle 6n9 + t9u install.sh-adjacent fixes if scope-cohesion holds.** The recursion is the load-bearing operational property: the §5.10 line this arc adds to PLINY's role file IS the discipline by which this arc's Phase 4 squash-merge must be executed.

**Imported assumptions named** (per §6.1 honest-restatement requirement):

1. **The Arc 24 design.md citation by directive A4 is the canonical articulation of the 5sr failure mode**, even though the original 5sr ticket body acknowledges "specific gap not fully spelled out in the close-out comment." I read Arc 24 design.md §14.1 R1+R2 + §14.2 r5 and treat *those* as the load-bearing empirical anchor (canonical-template wording drift across two near-identical inline copies caused an `os.environ['SINCE']` KeyError that would have shipped to ADA as canon). 5sr's framing as "Edit-tool worktree-path discipline" is — on my reading — a slightly miscategorized label for the actual failure: **DAEDALUS authoring two near-identical canonical-template copies across worktree-scoped file paths without a byte-for-byte alignment discipline.** §3 below names the discipline correctly and back-references the Arc 24 anchor.

2. **The dhc directive over-stated the python-vs-jq drift surface — finding ratified and ticket CLOSED mid-design.** The directive cited "3 near-identical drift-risk locations across MAJOR_PLINY.md §5.8 + MAJOR_POLYBIUS.md §7.6 + op-disc §18 + agent-author SKILL.md." I read all four sites end-to-end at rev1 design time: the prose ("**Why python, not jq.** `jq` is not a universal substrate-tier dependency...") exists in ONLY MAJOR_PLINY.md §5.8.3 (line 286). MAJOR_POLYBIUS.md §7.6 cross-references §5.8 without duplicating prose. operating-disciplines.md §18 references §5.8 in its dispatch-sequence table without duplicating prose. substrate/skills/agent-author/SKILL.md has no python-vs-jq prose at all. The Arc 24 design.md §14.1 R1+R2 reference to "rewrote the canonical poll-loop template in BOTH inline locations: §3.1 Step 3 and §6.1 §5.8.3" refers to the Arc 24 DESIGN.md's two inline copies, not to substrate canon. **Substrate already had the python-vs-jq prose as SSoT in MAJOR_PLINY.md §5.8.3.** Rev1 surfaced this finding as a §25 PRINCIPAL-gate at 2026-05-18T06:43:54Z; user-tier-polybius routed the gate to PRINCIPAL; PRINCIPAL ratified the finding; stoa--dhc CLOSED at 2026-05-18T06:47:41Z (~1 minute post rev1 commit). **dhc has no substrate work to do.** Arc 40 scope narrows from 6 candidates to 5; A5 is VOID in §6 sub-decision table; §3.C3 (dhc cite-comments) DROPPED from rev2.

3. **A20 recursion is genuinely novel for trailer-discipline canon.** Arc 35 shipped §28 trailers; Arc 36-39 practiced them; none of those arcs were *the arc shipping the squash-merge-trailer-preservation rule itself* — that ship is Arc 40. PLINY's Phase 4 signoff on stoa--utn must cite the NEW §5.10 wording even though that wording landed in this arc's build. The recursion is empirically observable (Phase 4 happens AFTER the §5.10 edit lands in arc-40/build) and surveillable (the §5.10 wording-as-shipped is what PLINY cites). I treat A20 not as a weak point but as a worked example of self-applied canon during the arc that ships it — §10 below.

The rev2 restatement converges with the (narrowed) brief; no `refused` gate fires. The rev1 PRINCIPAL-gate on assumption (2) discharged outside the design loop via PRINCIPAL ratification of dhc closure; the rev2 design therefore lands 5 candidates rather than 6, with no open PRINCIPAL-gate-eligible picks remaining.

---

## 2. Cross-cutting universal disciplines (apply to all candidates)

### 2.1 §28 Co-Authored-By trailers on every ADA + DAEDALUS commit

Every commit landed inside `.claude/worktrees/arc-40-build/` by ADA or DAEDALUS carries:

```
Co-Authored-By: CAPTAIN_<MNEMONIC>_the-stoa <captain-<mnemonic>@the-stoa.local>
```

Worked examples (verbatim per `substrate/operating-disciplines.md` §28.1 lines 1714-1718):

```
Co-Authored-By: CAPTAIN_DAEDALUS_the-stoa <captain-daedalus@the-stoa.local>
Co-Authored-By: CAPTAIN_ADA_the-stoa <captain-ada@the-stoa.local>
```

Use HEREDOC body. Per A8 LOCKED. The trailer is the seat-identity signal; `Author:` stays PRINCIPAL's `git config user.*` per global `~/.claude/CLAUDE.md` immutable rule.

### 2.2 §5.10 signoff with live-verified state

PLINY's Phase 4 signoff cites live-verified state per §19.6 attestation-honesty — never echoes dispatch-authoring SHAs without re-verification. The cleanup-verification commands per `MAJOR_PLINY.md` §5.10 lines 428-433 are mandatory before the signoff comment is posted: `git branch` + `git ls-remote --heads origin arc-40/build` (branch); `git worktree list` (worktree); `ls substrate/arcs/arc-40/pastes/` + `ls HUMAN_paste-*arc-40*` (paste archival per §5.11 lines 485-486).

### 2.3 §5.11 paste archival on arc close

Per Arc 38 + Arc 39 precedent: directive (`substrate/arcs/arc-40-build-directive.md`) stays at `substrate/arcs/` flat; the 2 activation pastes (`HUMAN_paste-pliny-arc-40-instruction.md` + `HUMAN_paste-polybius-arc-40-instruction.md`) `git mv` into `substrate/arcs/arc-40/pastes/`. `git mv` preserves history-walk-via-follow per §5.11 line 480.

Note for ARGUS: user-tier-polybius raised a "directive-wording-vs-precedent" question at Arc 39 close (POLYBIUS brief §5.11 wording reads "arc-40 directive + both activation pastes"); per ARGUS QA flag #2 at Arc 39, PLINY correctly followed precedent over literal wording. Same pattern stands for Arc 40.

### 2.4 A17 CATO MANDATORY

Pass 9 validate-spec is imminent in Arc 42; cumulative craft scrutiny matters. CATO PASS required before Phase 4 ship per directive A17.

### 2.5 A19 self-applied: Phase 4 squash-merge NO `--body` override

This is the canon Arc 40 ships AND the operational discipline Arc 40 must comply with. Phase 4:

- **Option (a) PREFERRED:** `gh pr merge <N> --squash --delete-branch --subject "..."` — OMIT `--body`. GitHub's default squash body auto-concatenates the source commits' bodies, preserving all `Co-Authored-By:` trailers per `substrate/operating-disciplines.md` §28.3 (lines 1737-1741).
- **Option (b) acceptable:** include `--body` HEREDOC with `Co-Authored-By:` trailers explicitly listed in the body so the override does not strip them.

Anti-pattern (Arc 37 regression at `bb12806`): `gh pr merge <N> --squash --delete-branch --subject "..." --body "<custom summary without trailers>"` — `--body` overrides the default trailer auto-concatenation; the squash-merge commit on main carries NO trailers despite all source commits carrying them correctly. `git log -1 --format='%B' bb12806 | grep -c 'Co-Authored-By'` returns 0 (empirically confirmed at design time via `git show bb12806 --pretty=fuller`).

### 2.6 A13 author frontmatter — applies IF A7 fold-in creates a new substrate-canon file with frontmatter

A7 fold-in (per §6 below) does NOT introduce any new substrate-canon files with YAML frontmatter. 6n9 adds a header line inside an existing manifest format (no frontmatter); t9u modifies install.sh deploy logic (no frontmatter). A13 is therefore not triggered by Arc 40's scope. ARGUS to confirm the trigger remains untriggered if A7 picks shift during revision.

### 2.7 ADA brief preamble (per MAJOR_PLINY.md §5.2 — reproduce verbatim in §2)

ADA: ground-check every concrete example in the design against the shipped code, specifically:

- JSON example shapes (response bodies, request bodies)
- Function/method signatures (parameter names, types, return types)
- Error message text (exact string match)
- Line ranges in path:line citations
- HTTP response codes
- Wire-protocol constants (header names, status codes, envelope keys)

If a design example contradicts the shipped code, the shipped code is canon — flag the design drift but build to ship reality.

For Arc 40 specifically, the candidate-most-at-risk for ground-check is **5sr's worked example** in §3.C2 below (which cites the Arc 24 design.md `os.environ['SINCE']` KeyError verbatim shape). The citation was live-verified at design time but ADA's pre-write read is non-negotiable per §5.2.

---

## 3. Per-candidate scopes

### 3.C1 stoa--6wp [SEQUENCE-CRITICAL] — squash-merge trailer-preservation canon (A2 LOCKED + A3 DAEDALUS-pick)

#### Empirical anchor

Arc 37 PR #17 squash-merged via:

```
gh pr merge 17 --squash --delete-branch --subject "..." --body "<gauntlet-outcome summary>"
```

Squash-merge commit `bb12806` body carries no Co-Authored-By trailers despite all 4 source branch commits (ADA + DAEDALUS) correctly carrying them per §28 canon. Live-verified at design time:

```
$ git log -1 --format='%B' bb12806 | grep -c 'Co-Authored-By'
0

$ git show bb12806 --pretty=fuller --stat | head -8
commit bb12806c67faf031f3989e1a8d5994802326df1b
Author:     Denson <denson@users.noreply.github.com>
AuthorDate: Sun May 17 19:04:58 2026 -0600
Commit:     GitHub <noreply@github.com>
CommitDate: Sun May 17 19:04:58 2026 -0600

    Arc 37: ship 6-candidate substrate architecture canonification batch (#17)
    [no Co-Authored-By trailers]
```

Compare Arc 39 PR #19 squash-merge commit `f1f222a` (which DID use the `--body` HEREDOC pattern with trailers explicit per Arc 38 forward-fix): `git log -1 --format='%B' f1f222a` shows 2 `Co-Authored-By: CAPTAIN_DAEDALUS_the-stoa <captain-daedalus@the-stoa.local>` lines — one per source commit body — because the explicit-trailer-in-body pattern landed them in the squash body.

#### A2 substrate touch — MAJOR_PLINY.md §5.10 one-line ship-checklist addition

A16 hard-lock: no restructuring §5.10 beyond a 1-line addition. The addition lands as a new bullet inside the `**The rule:**` enumerated list at §5.10 lines 428-433. **Proposed wording (canonical):**

> - **Squash-merge `--body` override discipline** — when merging via `gh pr merge --squash`, NEVER pass a custom `--body` that omits the source commits' `Co-Authored-By:` trailers. Either omit `--body` (GitHub's default auto-concatenates source-commit bodies, preserving trailers per `operating-disciplines.md` §28.3) OR include the trailers explicitly in the `--body` HEREDOC. Anti-pattern: a custom `--body` with a clean summary but no trailer lines silently drops the `§28` seat-identity signal on the squash commit. Empirical anchor: Arc 37 `bb12806` (2026-05-17).

**Insertion locus:** between the `**Process / cron / scheduled-job teardown**` bullet (line 433) and the `If a verification command surfaces state inconsistent...` paragraph (line 435). The bullet uses the same shape as the existing four bullets (bold lead-in, em-dash, prose body, parenthetical cross-refs).

**Alternative wordings ARGUS may weigh (per §4.6wp weak point #2 below):**

- Variant W1 (shorter): "**Squash-merge `--body` discipline** — `gh pr merge --squash` with a custom `--body` overrides the default trailer auto-concatenation. Either omit `--body` or include `Co-Authored-By:` trailers explicitly. Empirical anchor: Arc 37 `bb12806`."
- Variant W2 (longer, includes the Arc 38/39 worked counter-example): adds a final sentence "Arc 38 + Arc 39 shipped trailer-clean by following the explicit-trailers-in-HEREDOC pattern; Arc 40 ships the canon."

**DAEDALUS pick: proposed canonical wording above** (the version reproduced first). Rationale: matches the substrate's bullet-shape convention at §5.10 lines 428-433; names both the anti-pattern and both acceptable patterns concretely; cites the empirical anchor inline; cross-refs §28.3 without expanding the bullet beyond one logical unit. Variant W1 elides the both-patterns enumeration which makes the discipline harder to apply correctly; Variant W2 grows the bullet beyond the A16 one-line spirit (the spirit being "minimal §5.10 touch," not literally one ASCII line).

#### A3 DAEDALUS-pick — INCLUDE optional op-disc §28.3.1 pitfall worked-example

**Pick: INCLUDE.** The §28.3 canon (lines 1737-1741) expects trailer preservation by default. The Arc 37 regression is a worked example of how the default expectation can be defeated — naming the mechanism in §28.3.1 makes the canon defensible rather than just stated. The 1-paragraph addition reads at canonical-grade per the directive's "user-tier leans include" framing and matches the §28.5 / §28.6 sub-section pattern already in op-disc §28.

**Proposed substrate touch — new §28.3.1 inserted between §28.3 (line 1742 end) and §28.4 (line 1743 start):**

```markdown
#### 28.3.1 Pitfall — squash-merge `--body` override drops trailers

When `--body` is omitted on `gh pr merge --squash`, GitHub auto-populates the
squash-merge body from the source commits' subject + bodies; this
auto-population preserves `Co-Authored-By:` trailers (§28.3 property). Passing
a custom `--body` REPLACES the auto-populated body wholesale — including the
preserved trailers from the squashed commits' bodies. A `--body "<clean
summary>"` that omits trailer lines therefore silently strips every
seat-identity signal from the squash-merge commit on main.

**Empirical anchor.** Arc 37 PR #17 → squash-merge `bb12806` (2026-05-17).
The merge command was `gh pr merge 17 --squash --delete-branch --subject "..."
--body "<gauntlet-outcome summary>"`. All 4 source commits on `arc-37/build`
carried `Co-Authored-By: CAPTAIN_<MNEMONIC>_the-stoa` trailers per §28.
`bb12806`'s body carries zero (`git log -1 --format='%B' bb12806 | grep -c
'Co-Authored-By'` returns 0). The source branch was deleted as part of the
merge; the trailer chain on `main` was permanently severed for that arc.

**The fix at the merge site.** `MAJOR_PLINY.md` §5.10 ship-checklist bullet
naming this anti-pattern; either omit `--body` (preferred — GitHub
auto-populates trailers from source-commit bodies) or include trailers
explicitly in the `--body` HEREDOC (the pattern Arc 38 + Arc 39 used
organically and shipped trailer-clean by). Arc 40 codifies the discipline so
Pass 9/10 stellation arcs ship trailer-clean by canon, not by precedent.

**Cross-refs:** `MAJOR_PLINY.md` §5.10 (squash-merge ship-checklist
discipline); §28.3 (the default trailer-preservation property this pitfall
defeats); §19.6 (attestation-confabulation — sister discipline shape; both
"cite live-verified state, not assumed").
```

**A16 sanity check:** A16 hard-locks "no restructuring §5.10 beyond the 1-line ship-checklist addition." §28.3.1 is in op-disc, not §5.10 — the hard-lock is not triggered. ARGUS to confirm.

#### Cite-comment discipline per A12

Add cite-comment at MAJOR_PLINY.md §5.10 bullet pointing to op-disc §28.3.1; add cite-comment at op-disc §28.3.1 pointing back to MAJOR_PLINY.md §5.10. The pattern matches Arc 38 / bj5 cite-at-the-read-site discipline (substrate/install.sh:389-394 anchors the convention).

### 3.C2 stoa--5sr — DAEDALUS canonical-template wording-alignment discipline (A4 DAEDALUS-pick)

#### Empirical anchor — what Arc 24 §14.1 R1+R2 + §14.2 r5 actually surfaced

Arc 24's design.md authored two near-identical inline copies of the canonical bw-poll-loop template — one at §3.1 Step 3 (design's primary canonical-template anchor), one at §6.1 §5.8.3 (the MAJOR_PLINY.md drop-in). Both copies appeared in `agents/design/arc-24/design.md` (worktree-scoped path during Arc 24's gauntlet at `.claude/worktrees/arc-24-build/`). On revision-r2 (post-ARGUS-re-audit), §14.2 r5 documents:

> **§3.1 Step 3 (formerly line 154) placed `SINCE="$last"` AFTER the closing quote of `python -c "..."`, making it argv[1] (silently ignored by python in `-c` mode) — `os.environ['SINCE']` raises `KeyError: 'SINCE'` at runtime. The §6.1 §5.8.3 copy (line 447) placed `SINCE="$last"` BEFORE `python -c` (env-var prefix idiom) — works correctly. Two near-identical canonical templates with diverged shell syntax: the exact wording-drift class §8.11 names as Arc 24's most likely defect surfaced inside the design that defines §8.11.**

The failure mode is not literally about Edit-tool worktree paths — the original 5sr ticket label was somewhat miscategorizing. **The actual discipline gap is: when DAEDALUS authors a design.md that carries two or more inline copies of the SAME canonical template (a bash block, a poll-loop, a verdict-format YAML schema, etc.), the copies MUST be byte-for-byte aligned (modulo named slot substitutions) and the discipline is to verify the alignment mechanically before completing the design.** The Arc 24 surfaced empirical anchor demonstrates that without the discipline, ARGUS catches drift on re-audit; with the discipline, the drift is prevented at authoring time.

The "worktree-path" framing in the original 5sr ticket comes from a related-but-distinct observation: the Arc 24 design.md was authored under `.claude/worktrees/arc-24-build/agents/design/arc-24/design.md` (absolute path), Edit-tool operations from inside the worktree resolved against the worktree cwd, and any DAEDALUS authoring multiple inline copies in a single design.md is doing so within a single file under a single worktree — the path-resolution mechanics work correctly; the failure mode is about *content alignment across copies within a single file*, not path resolution across files. I am authoring the new substrate prose to name the actual discipline gap rather than the original ticket's slightly-miscategorized framing. ARGUS to confirm this re-framing is correct or surface for substance-disagreement.

#### Substrate touch — CAPTAIN_DAEDALUS.md new §6.8 subsection

**Insertion locus:** after current §6.7 (PRINCIPAL-gate discipline, line 151 end) and before `---` separator + `## 7. Verdict format` (line 153). The new subsection extends the "Disciplines specific to this seat" section; it parallels the existing §6.5 / §6.6 / §6.7 shape (heading, narrative, optional empirical anchor citation, cross-refs).

**Proposed wording:**

```markdown
### 6.8 Canonical-template wording-alignment discipline

When your design contains TWO OR MORE inline copies of a canonical template
(a bash block, a poll-loop, a verdict-format YAML schema, a code stub
referenced from multiple §-locations within the design), the copies MUST be
byte-for-byte aligned modulo named-slot substitutions. The discipline is to
verify alignment mechanically before completing the design — the canonical
verification is `diff <(sed -n '<start1>,<end1>p' <design.md>) <(sed -n
'<start2>,<end2>p' <design.md>)` returning empty output. If the diff is
non-empty, either the copies disagree (a defect class ARGUS will catch on
re-audit) or one copy is a deliberate variant (in which case the variant must
be named and defended in the surrounding prose — silent variance fails this
gate).

The discipline applies inside a single design.md file specifically — the
failure mode is two near-identical canonical templates authored within one
design where the byte-level alignment was assumed-rather-than-verified.
Cross-file canonical templates (a design.md referencing a template that lives
canonically in a different substrate file) are a separate concern handled by
the substrate's existing single-source-of-truth discipline + cite-at-read-site
convention; this §6.8 covers the within-design case.

**Empirical anchor.** Arc 24 design.md (Phase 1 + Phase 2; surfaced on
ARGUS re-audit per `agents/design/arc-24/design.md` §14.2 r5 line 1147): two
inline copies of the canonical bw-poll-loop template at §3.1 Step 3 and §6.1
§5.8.3. The §3.1 copy placed `SINCE="$last"` after the closing `python -c
"..."` quote (argv position, silently ignored in `-c` mode, runtime
`KeyError: 'SINCE'`); the §6.1 copy placed it before `python -c` (env-var
prefix idiom, works correctly). ARGUS caught the drift on re-audit; the
post-fix recovery aligned both copies byte-for-byte. The empirically-cheap
defense at authoring time is the `diff` mechanical check named above. Source
ticket: `stoa--5sr`. Discipline-shipped arc: Arc 40 (`stoa--utn`).

**Cross-refs:** `agents/design/arc-24/design.md` §14.2 r5 (empirical anchor);
`agents/design/arc-24/design.md` §13.4 (parallel weak point on cross-file
cross-ref drift — separate concern, separate discipline); CAPTAIN_DAEDALUS.md
§6.2 (Self-assessed weak points — author may flag suspected within-design
drift as a weak point if `diff` was not run); operating-disciplines.md §28
(cite-at-read-site discipline — orthogonal mechanism for cross-file SSoT).
```

**Alternative placement considered:** in §6.2 Self-assessed weak points as a sub-bullet of the "Silently smoothing" failure-mode list. Rejected because the discipline is operationally distinct (mechanical `diff` check) rather than a weak-point-flag and deserves its own subsection per Arc 24's empirical-anchor weight.

**A16 sanity check:** A16 hard-locks "no widening 5sr beyond what `agents/design/arc-24/design.md` flagged." The Arc 24 §14.2 r5 + §13.4 surfaces this discipline gap explicitly — the within-design alignment failure mode IS what Arc 24 flagged. The re-framing from "Edit-tool worktree-path discipline" (5sr ticket label) to "canonical-template wording-alignment discipline" (this design's articulation) is a label refinement that narrows scope to the actual Arc 24 anchor; it does not widen. ARGUS to confirm.

### 3.C3 stoa--dhc — VOID (closed mid-design; no substrate work)

stoa--dhc was CLOSED by user-tier-polybius @ 2026-05-18T06:47:41Z with PRINCIPAL ratification, ~1 minute after rev1 commit (76928152). The closure ratified rev1's §25 PRINCIPAL-gate finding (surfaced at 06:43:54Z) that substrate already has SSoT for the python-vs-jq rationale at MAJOR_PLINY.md §5.8.3 — the three downstream sites cited by the dhc ticket (MAJOR_POLYBIUS.md §7.6, operating-disciplines.md §18, substrate/skills/agent-author/SKILL.md) are vacant of duplicate prose. The ticket's underlying intent (close the drift risk) was discharged by the empirical finding itself: there is no drift to close when no duplicate prose exists.

**Substrate work for dhc in Arc 40: none.** A5 sub-decision is VOID in §6 below. Probes p9/p10/p11 (rev1 dhc-specific) are dropped from rev2; probe numbering uses gap-numbering (rev1 IDs preserved for ARGUS/ZENO/VERA calibration traceability) per the rev2 dispatch brief's preferred shape. See §1.2 imported assumption (2) for the full empirical finding; see §7.1 rev2 for the one-line residual note.

Forward-looking: any future arc that adds a SECOND inline python-vs-jq prose block to substrate triggers the cite-at-read-site discipline + the §6.8 within-design alignment discipline (§3.C2 above) as orthogonal defenses.

### 3.C4 stoa--3sz — probe-spec `^last=` anchor canon (A6 DAEDALUS-pick: γ)

#### Empirical anchor

Arc 24 Phase 3 VERA probe-spec defect: a verbatim regex pattern matching `last=` found 2 matches at MAJOR_PLINY.md lines 258 + 273 — one in the python template body, one in the example documentation. The intended single canonical-template-start anchor required the `^` line-start anchor. VERA surfaced this 2026-05-13 in Arc 24 Phase 3 verdict as non-blocking probe-spec imprecision.

#### A6 DAEDALUS-pick

**Pick: γ — CAPTAIN_VERA.md probe-authoring section.** Rationale per directive's "user-tier leans γ": probe-authoring is VERA-specific discipline; lives at VERA seat-canon. Placing the canon at op-disc §18 (subagent-status section, where Arc 24 landed the universal-team framing) would widen the placement to "probe-authoring general guidance" beyond VERA's seat. The 3sz scope is VERA-specific.

#### Substrate touch — CAPTAIN_VERA.md new §5.11 subsection

**Insertion locus:** after current §5.10 (PRINCIPAL-gate discipline, line 173 end) and before `---` separator + `## 6. Verdict format` (line 174). The new subsection extends the "Disciplines specific to this seat" section; parallels §5.7 / §5.8 / §5.9 / §5.10 shape.

**Proposed wording:**

```markdown
### 5.11 Probe-spec regex anchoring discipline

When a probe-spec authored by DAEDALUS matches a canonical template fragment
in substrate prose, the verbatim regex pattern often false-positives because
the substrate prose itself documents the template (canonical template + example
documentation + cross-references all match the same fragment). The probe's
intended single-match returns N matches; the probe "passes" mechanically but
verifies nothing because the assertion is on count rather than location.

**The discipline (at probe-execution time).** Before executing a probe whose
spec contains a verbatim regex matching against substrate prose, examine the
spec for:

1. **Anchoring** — is the pattern anchored with `^` (line start), `$` (line
   end), or a unique surrounding-context substring that disambiguates the
   intended single match from documentation prose?
2. **Expected count** — does the spec name the expected match count
   explicitly (e.g., `expected: exactly 1 match`) or just check non-zero
   (which would pass on N>1)?
3. **Falsifying-evidence clause** — does the spec include an "OR emits with
   wrong shape" clause so a passing-count-but-wrong-content match is caught?

If any of these three is missing, surface the gap in `methodology_concerns:`
rather than executing the underspecified probe and recording a misleading
PASS. The probe author (DAEDALUS) revises the spec; VERA re-executes against
the revised spec on next dispatch.

**Empirical anchor.** Arc 24 Phase 3 (2026-05-13): probe p44 (then p35) used
verbatim regex `last=` against MAJOR_PLINY.md to verify the canonical
poll-loop template start. Two matches found (lines 258 + 273) — one in the
python template body (intended), one in the example documentation
(false-positive). Anchored variant `^last=` returns 1 match. Non-blocking for
Arc 24 ship; promoted to canon here. Source ticket: `stoa--3sz`. Discipline-
shipped arc: Arc 40 (`stoa--utn`).

**Cross-refs:** `MAJOR_PLINY.md` §5.8.3 (the canonical site whose template
fragment the Arc 24 probe under-anchored); CAPTAIN_DAEDALUS.md §6.8 (the
authoring-side sibling discipline for canonical-template wording alignment —
together, §6.8 keeps the authoring side aligned and §5.11 keeps the
verification side honest about what the probe actually verifies);
CAPTAIN_VERA.md §5.7 (verification-complexity quadrant — anchored-probe
discipline is an easy-easy / mechanical refinement, not a quadrant shift).
```

**A16 sanity check:** A16 hard-locks "no widening 3sz probe-discipline to non-probe authoring guidance." The new §5.11 is scoped to probe execution (VERA-side reading of DAEDALUS-authored probe specs); does not widen to non-probe authoring. ARGUS to confirm.

#### Cross-link with 3.C2 (5sr §6.8)

The 5sr §6.8 within-design wording-alignment discipline and the 3sz §5.11 probe-spec anchoring discipline form a coordinated pair: §6.8 (DAEDALUS-side, authoring time) prevents canonical-template copies from drifting; §5.11 (VERA-side, execution time) prevents under-anchored probes from generating false-positive PASS verdicts that would mask drift if it occurred. Both anchor to the same Arc 24 empirical surface (Phase 1+2 design wording drift caught at Phase 3). The cross-refs at the bottom of each subsection make the coordination legible to a cold reader.

### 3.C5 stoa--6n9 — manifest format-version header (A7 fold-in: INCLUDE)

#### Origin + scope

Arc 38 CATO c3 follow-up (2026-05-17). `substrate/install.sh` `write_substrate_manifest` (lines 395-433) declares the format `<deployed-relative-path>\t<token>\t<replacement>` as a comment in the manifest header (line 418) but does NOT emit an explicit format-version line. The manifest readers in `substrate/skills/check-substrate-updates/check.sh` `apply_substitutions_from_manifest` (lines 146-180+) and `apply.sh` (lines 115+) do NOT verify a format-version. Forward-looking robustness: if a future install.sh bumps the format (adds a column, changes separator, rotates the comment-header shape), check.sh + apply.sh readers silently produce wrong substitutions OR skip entries — depending on the rotation shape.

#### Fix shape

- **install.sh `write_substrate_manifest` (lines 415-424):** add an emitted line `# format=v1` between the existing `# DO NOT EDIT MANUALLY...` line (419) and the `#` separator (420). The line is comment-shaped (starts with `#`); existing readers' comment-skip logic (e.g., check.sh line 175 `""|\#*) continue ;;`) safely ignores it under pre-fix readers (idempotent fallback).
- **check.sh `apply_substitutions_from_manifest` (lines 146+):** add a parser pass before the data-row loop that scans the header for `# format=vN` and rejects unknown versions with a clear error: `check.sh: error: .substrate-manifest format=v<N> unknown; this check.sh expects v1. Re-run install.sh to re-deploy with a matching manifest, or update the check-substrate-updates skill.` If no `# format=` line is present (e.g., a manifest written by a pre-fix install.sh), treat as v1 (graceful fallback for already-deployed workspaces).
- **apply.sh `apply_substitutions_from_manifest` (lines 115+):** mirror the check.sh parser pass. Same v1-fallback for pre-fix manifests.
- **Cite-comments at all three sites** (write site + 2 read sites) per A12 — naming the v1 contract and the rotation-discipline (any install.sh that bumps v1→v2 MUST update both readers in same arc, and the readers' version-rejection error names the upgrade path).

#### Worked example (manifest header pre-fix → post-fix)

```
# Pre-fix (Arc 38 ship):
# Stoa substrate deploy manifest — substitutions applied to deployed files.
# Written by install.sh at deploy time. Read by check.sh + apply.sh to normalize.
# Format: <deployed-relative-path>\t<token>\t<replacement>
# DO NOT EDIT MANUALLY. install.sh rewrites this file on every re-run.
#
# tier=user
# deployed_at=...
# substrate_sha=...

# Post-fix (Arc 40 ship):
# Stoa substrate deploy manifest — substitutions applied to deployed files.
# Written by install.sh at deploy time. Read by check.sh + apply.sh to normalize.
# Format: <deployed-relative-path>\t<token>\t<replacement>
# DO NOT EDIT MANUALLY. install.sh rewrites this file on every re-run.
# format=v1
#
# tier=user
# deployed_at=...
# substrate_sha=...
```

The `# format=v1` line is parser-visible (matched by the new check.sh + apply.sh header-scan pass) AND comment-safe (pre-fix readers skip via existing `\#*) continue` rule). Idempotent under re-install. Forward-version-bumps add `# format=v2` + readers reject unknown versions with the named error.

#### A7 fold-in cohesion judgment

6n9 is install.sh-adjacent (touches `write_substrate_manifest` + the 2 manifest readers) and is forward-looking robustness for the manifest format the Arc 38 / bj5 cite-comment discipline already mitigates via the at-write-site `CITE:` comment (substrate/install.sh:389-394). Adding the format-version header makes the same property machine-checkable rather than convention-checkable. Scope cohesion with the 3 LOCKED candidates: medium — install.sh adjacency provides a natural co-location with t9u (also install.sh-adjacent); A1 bundle-shape precedent (Arc 37 at 6 candidates) accommodates the rev2 5-count comfortably.

**A16 sanity check:** A16 hard-locks "If 6n9/t9u folded: no widening beyond literal ticket scopes." 6n9 literal scope per ticket: "Add an explicit format-version header line in the manifest + make `apply_substitutions_from_manifest` parse the version line and reject unknown versions + update install.sh write_substrate_manifest to emit the version line + cite-comments at write site + both read sites naming the version contract." The proposed fix shape above matches the literal scope; no widening. ARGUS to confirm.

### 3.C6 stoa--t9u — install.sh deploy excludes `__pycache__/` (A7 fold-in: INCLUDE)

#### Origin + scope

Arc 39 CATO finding C1 (2026-05-18). install.sh `cp -R` (line 798) copies skill subtrees wholesale; if the source worktree has run a deployed helper at least once, the source has `__pycache__/` + `*.pyc` accumulated. install.sh then copies that pycache into every target tier's deployed `_lib/`. Practically benign (pycache regenerates on import) but pollutes target trees with bytecode the consumer did not author. Source-side `.gitignore __pycache__/+*.pyc` was added in Arc 39 commit `f707bc6` (prevents accidental commit; orthogonal to deploy-side filtering).

#### Fix shape

Per t9u ticket A1 PLINY-lean: **α — post-copy cleanup.** install.sh's skill-deploy loop (lines 786-801) gains one line after the `cp -R` (line 798):

```bash
# Existing (line 796-798):
rm -rf "$dest_skill"
mkdir -p "$dest_skill"
cp -R "$src_skill"/. "$dest_skill"/
# Add post-copy pycache cleanup (Arc 40 / stoa--t9u):
find "$dest_skill" -type d -name __pycache__ -prune -exec rm -rf {} + 2>/dev/null || true
find "$dest_skill" -type f -name '*.pyc' -delete 2>/dev/null || true
```

Two finds rather than one combined: cleaner audit trail per find-class (directory prune for pycache dirs; file delete for stray .pyc files outside pycache dirs). `2>/dev/null || true` defends against find/rm portability variance across Git Bash / macOS / Linux without breaking the deploy on any single platform's find quirks.

Dry-run path (line 790) gets a parallel echo: `[dry-run] post-copy pycache cleanup: $dest_skill (find __pycache__/*.pyc -delete)`.

#### Worked smoke test (probe spec for VERA per §4)

Reproduce the failure mode + verify the fix:

```bash
# Populate source-side pycache by running the deployed helper:
cd substrate/skills/save-verdict/
python _save_verdict.py --help >/dev/null 2>&1 || true
ls _lib/__pycache__/ 2>/dev/null   # should exist after the python invocation

# Deploy to a temp target:
TEMPDIR="$(mktemp -d)"
mkdir -p "$TEMPDIR/test-project"  # mn3 fix-1.5 (Arc 42 stoa--mn3 + CAPTAIN_DAEDALUS.md §6.9 clause 4): install.sh does not auto-create --project-dir
cd <repo-root>
bash substrate/install.sh --target project --project-dir "$TEMPDIR/test-project" 2>&1 | tail -20  # mn3 fix-1.5 (per CAPTAIN_DAEDALUS.md §6.9 clause 4 ground-check shipped install.sh surface): replaced non-existent flags with correct --project-dir

# Verify deployed skill has NO pycache:
ls "$TEMPDIR/test-project/.claude/skills/save-verdict/_lib/__pycache__/" 2>/dev/null
# Expected: "ls: cannot access ...: No such file or directory" (or empty output)

# Cleanup
rm -rf "$TEMPDIR" substrate/skills/save-verdict/_lib/__pycache__/
```

VERA executes the probe per §4 below. ZENO spec-checks the new install.sh lines per ZENO criteria.

#### A7 fold-in cohesion judgment

t9u is install.sh-adjacent (same file as 6n9; complementary forward-looking-robustness pair). User-tier weak lean for fold-in stands. Bundle-shape: 5 candidates after rev2 dhc drop, well within the Arc 37 precedent ceiling of 6. **DAEDALUS pick: INCLUDE both 6n9 + t9u.** Rationale: install.sh adjacency provides natural co-location; both fixes are small (≤30 LOC each); separate arc-cycles for either would cost more than the cohesion-tax of bundling.

**A16 sanity check:** A16 hard-locks "If 6n9/t9u folded: no widening beyond literal ticket scopes." t9u literal scope per ticket: "install.sh runs `find <target>/<skill-name> -name __pycache__ -type d -exec rm -rf {} +` after each cp -R." The proposed fix matches; the additional `find ... -name '*.pyc' -delete` line covers stray .pyc files outside pycache directories which the ticket "Out of scope" deliberately excluded ("Filtering for non-Python artifacts (.DS_Store, *.swp, etc.) — separate concern, separate ticket if needed"). The .pyc-file-delete is a SUB-CASE of Python bytecode cleanup (same defect class as pycache directories — both are Python interpreter-generated artifacts) and is in literal scope. The .DS_Store / *.swp / etc. cases remain out of scope. ARGUS to confirm.

---

## 4. Verification probes (for VERA + ZENO)

Probes are numbered p1-pN; each probe carries quadrant classification per `operating-disciplines.md` §15.

### p1 — A8 trailer check (ADA commit)

**Quadrant:** easy-easy / mechanical.
**Command:** `git log arc-40/build --pretty='%(trailers:key=Co-Authored-By,valueonly)' | grep -E '^CAPTAIN_ADA_the-stoa <captain-ada@the-stoa\.local>$' | wc -l`
**Expected:** ≥1 (at least one ADA build commit on arc-40/build carries the trailer).
**Falsifying evidence:** zero matches — A8 trailer missing on any ADA commit.

### p2 — A8 trailer check (DAEDALUS commit)

**Quadrant:** easy-easy / mechanical.
**Command:** `git log arc-40/build --pretty='%(trailers:key=Co-Authored-By,valueonly)' | grep -E '^CAPTAIN_DAEDALUS_the-stoa <captain-daedalus@the-stoa\.local>$' | wc -l`
**Expected:** ≥1 (at least one DAEDALUS design-commit on arc-40/build carries the trailer; this design.md commit itself, plus any rev cycles).
**Falsifying evidence:** zero matches — A8 trailer missing on any DAEDALUS commit.

### p3 — A2 verification (MAJOR_PLINY.md §5.10 1-line addition)

**Quadrant:** easy-easy / mechanical.
**Command:** `grep -c "Squash-merge .--body. override discipline" substrate/MAJOR_PLINY.md`
**Expected:** exactly 1 (the new bullet's lead-in phrase).
**Falsifying evidence:** 0 (bullet missing) or ≥2 (duplicate insertion).

### p4 — A2 wording-shape verification

**Quadrant:** easy-easy / mechanical.
**Command:** `awk '/^- \*\*Squash-merge/,/Empirical anchor: Arc 37/' substrate/MAJOR_PLINY.md | wc -l`
**Expected:** non-zero AND the captured block contains `bb12806` AND the captured block contains `operating-disciplines.md` §28.3 reference.
**Falsifying evidence:** block absent OR missing the empirical-anchor citation OR missing the §28.3 cross-ref.

### p5 — A3 verification (op-disc §28.3.1 subsection)

**Quadrant:** easy-easy / mechanical.
**Command:** `grep -c "^#### 28\.3\.1 Pitfall — squash-merge .--body. override drops trailers" substrate/operating-disciplines.md`
**Expected:** exactly 1.
**Falsifying evidence:** 0 (subsection missing — A3 INCLUDE not landed) or ≥2 (duplicate).

### p6 — A3 worked-example bb12806 cite

**Quadrant:** easy-easy / mechanical.
**Command:** `awk '/^#### 28\.3\.1/,/^#### 28\.4/' substrate/operating-disciplines.md | grep -c "bb12806"`
**Expected:** ≥1 (the worked example cites bb12806 as the empirical anchor).
**Falsifying evidence:** 0 (cite missing).

### p7 — A4 verification (CAPTAIN_DAEDALUS.md §6.8 subsection)

**Quadrant:** easy-easy / mechanical.
**Command:** `grep -c "^### 6\.8 Canonical-template wording-alignment discipline" substrate/CAPTAIN_DAEDALUS.md`
**Expected:** exactly 1.
**Falsifying evidence:** 0 (subsection missing) or ≥2 (duplicate).

### p8 — A4 Arc-24-anchor cite

**Quadrant:** easy-easy / mechanical.
**Command:** `awk '/^### 6\.8/,/^### 6\.9|^## 7/' substrate/CAPTAIN_DAEDALUS.md | grep -c "agents/design/arc-24/design.md"`
**Expected:** ≥1 (the §6.8 prose cites Arc 24 design.md as empirical anchor).
**Falsifying evidence:** 0 (cite missing).

### p9 / p10 / p11 — DROPPED (rev2; dhc CLOSED mid-design)

Rev1 probes p9 / p10 / p11 verified dhc cite-comment landings at MAJOR_PLINY.md §5.8.3, MAJOR_POLYBIUS.md §7.6, and operating-disciplines.md §18.5 respectively. dhc CLOSED by user-tier-polybius @ 2026-05-18T06:47:41Z with PRINCIPAL ratification; no substrate work for dhc → no probes required. **Gap-numbering preserved** (p9 / p10 / p11 left as placeholders rather than renumbered) so that ARGUS / ZENO / VERA agents already calibrated against rev1 probe IDs retain traceability. Rev2 actual probe sequence: p1-p8, p12-p24 = 21 probes total.

### p12 — A6 verification (CAPTAIN_VERA.md §5.11 subsection)

**Quadrant:** easy-easy / mechanical.
**Command:** `grep -c "^### 5\.11 Probe-spec regex anchoring discipline" substrate/CAPTAIN_VERA.md`
**Expected:** exactly 1.
**Falsifying evidence:** 0 or ≥2.

### p13 — A6 `^last=` anchor canon present

**Quadrant:** easy-easy / mechanical.
**Command:** `awk '/^### 5\.11/,/^### 5\.12|^## 6/' substrate/CAPTAIN_VERA.md | grep -c '\^last='`
**Expected:** ≥1 (the §5.11 prose names the `^last=` anchored variant explicitly per the empirical anchor).
**Falsifying evidence:** 0.

### p14 — A7 fold-in (6n9) install.sh format=v1 emit

**Quadrant:** easy-easy / mechanical.
**Command:** `grep -E '^[[:space:]]+echo "# format=v1"' substrate/install.sh | wc -l`
**Expected:** exactly 1 (write_substrate_manifest emits the version line).
**Falsifying evidence:** 0 (emit missing).

### p15 — A7 fold-in (6n9) deploy-then-grep target manifest

**Quadrant:** easy-easy / empirical (post-build smoke).
**Command:**
```bash
TEMPDIR="$(mktemp -d)" && \
mkdir -p "$TEMPDIR/test-project" && \
bash substrate/install.sh --target project --project-dir "$TEMPDIR/test-project" >/dev/null 2>&1 && \
grep -c '^# format=v1' "$TEMPDIR/test-project/.claude/.substrate-manifest"; \
rm -rf "$TEMPDIR"
```
<!-- mn3 fix-1 (Arc 42 stoa--mn3 + CAPTAIN_DAEDALUS.md §6.9 clause 4): replaced non-existent install.sh flags with correct --project-dir (per §6.9 ground-check); pre-create --project-dir per shipped install.sh behavior -->
**Expected:** 1 (deployed manifest carries the version line).
**Falsifying evidence:** 0 (version line not written).

### p16 — A7 fold-in (6n9) check.sh + apply.sh version parser

**Quadrant:** easy-easy / mechanical.
**Command:** `grep -c 'format=v' substrate/skills/check-substrate-updates/check.sh substrate/skills/check-substrate-updates/apply.sh`
**Expected:** ≥2 (both readers have the version-parser code; at least one match per file).
**Falsifying evidence:** <2 (one reader missing the parser — partial-land defect).

### p17 — A7 fold-in (t9u) install.sh pycache cleanup line present

**Quadrant:** easy-easy / mechanical.
**Command:** `grep -c 'find.*-name __pycache__.*-prune.*-exec rm -rf' substrate/install.sh`
**Expected:** exactly 1.
**Falsifying evidence:** 0 (cleanup line missing).

### p18 — A7 fold-in (t9u) deploy-then-grep target excludes pycache (empirical smoke)

**Quadrant:** easy-easy / empirical (post-build smoke).
**Command:**
```bash
# Populate source-side pycache:
cd substrate/skills/save-verdict && \
python _save_verdict.py --help >/dev/null 2>&1 || true; \
cd - >/dev/null && \
TEMPDIR="$(mktemp -d)" && \
mkdir -p "$TEMPDIR/test-project" && \
bash substrate/install.sh --target project --project-dir "$TEMPDIR/test-project" >/dev/null 2>&1 && \
ls "$TEMPDIR/test-project/.claude/skills/save-verdict/_lib/__pycache__/" 2>&1 | grep -c "No such file"; \
rm -rf "$TEMPDIR" substrate/skills/save-verdict/_lib/__pycache__/
```
<!-- mn3 fix-2 (Arc 42 stoa--mn3 + CAPTAIN_DAEDALUS.md §6.9 clause 4): replaced non-existent install.sh flags with correct --project-dir (per §6.9 ground-check); pre-create --project-dir per shipped install.sh behavior -->
**Expected:** 1 (target tier has NO `__pycache__/`; `ls` returns "No such file" message).
**Falsifying evidence:** 0 (target has pycache — t9u fix did not land or did not work).

### p19 — A20 recursive-shape verification: PLINY signoff cites new §5.10 discipline (softened per ARGUS R5 LOW)

**Quadrant:** easy-easy / mechanical.
**Command:** `bw show stoa--utn 2>&1 | grep -cE '\`--body\`.*override|--body.*override|trailer-discipline|squash-merge.*trailer|squash-merge.*\`--body\`'`
**Expected:** ≥1 in PLINY's Phase 4 signoff comment on stoa--utn (the signoff discharges audit-trail intent by referencing the new §5.10 discipline through any of: the rigid bullet wording, a paraphrase naming `--body` override, a "trailer-discipline" framing, or a "squash-merge ... trailer" framing).
**Falsifying evidence:** 0 — signoff did NOT cite the new §5.10 discipline in any recognizable form, meaning either (a) §5.10 edit did not land OR (b) PLINY did not self-apply the new canon at signoff.
**Rev2 note (per ARGUS R5 LOW):** rev1 used rigid substring matching `"Squash-merge \`--body\` override discipline"` which would FAIL on a paraphrased signoff that nonetheless discharges audit-trail intent. Rev2 softens to alternation regex covering: the rigid bullet wording, the `--body`-override paraphrase, the "trailer-discipline" shorthand, and the "squash-merge ... trailer" framing. Operational property (trailer preservation on the actual squash-merge commit) is separately verifiable via `git log -1 --format='%B' <merge-sha> | grep -c 'Co-Authored-By'` post-merge — that check is the load-bearing safety net; p19 is the audit-trail-cite check.

### p20 — §5.11 paste archival post-arc

**Quadrant:** easy-easy / mechanical.
**Command:**
```bash
ls substrate/arcs/arc-40/pastes/HUMAN_paste-pliny-arc-40-instruction.md \
   substrate/arcs/arc-40/pastes/HUMAN_paste-polybius-arc-40-instruction.md \
   && ls HUMAN_paste-*arc-40*.md 2>&1 | grep -c "No such file"
```
**Expected:** both files exist in the archive; workspace root grep returns ≥1 "No such file" line (workspace root carries no arc-40 pastes after archival).
**Falsifying evidence:** archive files missing OR workspace root still carries arc-40 pastes.

### p21 — §5.10 cleanup (worktree)

**Quadrant:** easy-easy / mechanical.
**Command:** `git worktree list | grep -c arc-40`
**Expected:** 0.
**Falsifying evidence:** ≥1 (worktree still present post-cleanup).

### p22 — §5.10 cleanup (branch local)

**Quadrant:** easy-easy / mechanical.
**Command:** `git branch | grep -c "arc-40/build"`
**Expected:** 0.
**Falsifying evidence:** ≥1.

### p23 — §5.10 cleanup (branch remote)

**Quadrant:** easy-easy / mechanical.
**Command:** `git ls-remote --heads origin arc-40/build | wc -l`
**Expected:** 0.
**Falsifying evidence:** ≥1.

### p24 — A14 source-ticket closure (3 LOCKED + 2 folded = 5 tickets; dhc already CLOSED mid-design)

**Quadrant:** easy-easy / mechanical.
**Command:** `for t in stoa--3sz stoa--5sr stoa--6wp stoa--6n9 stoa--t9u; do bw show "$t" 2>&1 | head -1 | grep -c '^# ✓'; done | paste -sd+ - | bc`  <!-- mn3 fix-3 (Arc 42 stoa--mn3 + CAPTAIN_DAEDALUS.md §6.9 clause 4): bw does NOT emit '^Status:.*closed' lines; the canonical closed-glyph anchor is '# ✓' on line-1 (live ground-checked) -->
**Expected:** 5 (all 5 in-scope source tickets closed; dhc was CLOSED mid-design @ 2026-05-18T06:47:41Z and is excluded from the Arc 40 closure-comment-cycle since no substrate work landed for it).
**Falsifying evidence:** <5 (one or more open).
**Optional strengthening (per A14 closure-comment discipline):** each in-scope ticket's closure comment should reference the Arc 40 merge SHA. Probe variant — `for t in stoa--3sz stoa--5sr stoa--6wp stoa--6n9 stoa--t9u; do bw show "$t" 2>&1 | grep -c "Arc 40.*merge\|<merge-sha-prefix>"; done | paste -sd+ - | bc` expecting ≥5. PLINY-discretion whether to strengthen at execution; bare count check is the load-bearing property.

### Probe count + quadrant summary (rev2)

| Quadrant | Count | Probes |
|---|---|---|
| easy-easy / mechanical | 19 | p1-p8, p12-p14, p16-p17, p19-p24 |
| easy-easy / empirical (post-build smoke) | 2 | p15, p18 |
| Other quadrants | 0 | — |

**Total: 21 probes (rev2).** Rev1 had 24 numbered probes (p1-p24) with summary table mis-stating 23 (off-by-one error in rev1 summary table — corrected here). Rev2 drops p9 / p10 / p11 (dhc CLOSED mid-design) → 24 − 3 = 21 actual. Gap-numbering preserved (rev1 IDs p1-p24 retained as anchors, with p9/p10/p11 marked DROPPED) for ARGUS / ZENO / VERA calibration-traceability across rev1 → rev2.

All probes are easy-easy quadrant; no INCOMPLETE / UNVERIFIABLE quadrant probes. VERA's verdict format applies; CATO's craft-review covers prose voice + cross-ref resolution per A12; ZENO's mechanical spec-check on the install.sh + check.sh + apply.sh wiring per ZENO criteria.

---

## 5. Out of scope (Arc 40-specific)

Per A16 LOCKED + directive Out-of-scope framing:

- **Restructuring MAJOR_PLINY.md §5.10 beyond the 1-line ship-checklist addition.** Per A16; §5.10's broader signoff-accuracy + cross-refs + N=1 provenance prose untouched.
- **Introducing new substrate skills.** Per A16. No new SKILL.md files in arc-40/build.
- **Retroactive sweep of OTHER substrate SKILL.md files beyond Arc 39 M3 widening.** Per A16 (sp1 scope handles cross-substrate utility skills).
- **Re-opening stoa--dhc.** Per PRINCIPAL ratification of the SSoT-already-existing finding @ 2026-05-18T06:47:41Z. The ticket closed mid-design; rev2 does not re-open it. (Rev1 A16 line "Widening dhc lift to non-poll-loop template consolidations" is superseded by the closure.)
- **Widening 3sz probe-discipline to non-probe authoring guidance.** Per A16. The new §5.11 stays VERA-side at probe-execution time.
- **Widening 5sr beyond what `agents/design/arc-24/design.md` flagged.** Per A16. The new §6.8 stays scoped to within-design canonical-template alignment (the actual Arc 24 §14.2 r5 + §13.4 anchor); the directive's "Edit-tool worktree-path discipline" label is a related-but-distinct surface that this arc does not address (no observable failure mode at design time).
- **If 6n9/t9u folded: no widening beyond literal ticket scopes.** Per A16. 6n9 covers manifest format-version only (not other manifest-format changes); t9u covers Python bytecode artifacts only (not other deploy-side filtering — `.DS_Store`, `*.swp`, IDE files, etc.).
- **Retroactive amendment of `bb12806`.** Per 6wp ticket Out-of-scope. The Arc 37 squash-merge stays as-is; the trailer chain on `arc-37/build` source commits is durable in PR #17's source-branch history (recoverable via `gh pr view 17 --json commits`).
- **Building tooling enforcement (pre-commit hook, CI check).** Per 6wp ticket Out-of-scope. Convention is the layer; the §5.10 ship-checklist bullet + §28.3.1 pitfall worked-example are the substrate discipline.
- **Substrate cross-reference automated checker.** Per Arc 24 §13.4 weak point. Arc 25+ follow-up surface; not Arc 40 scope.

---

## 6. DAEDALUS sub-decision summary

| ID | Decision | DAEDALUS pick | Rationale (one line) |
|---|---|---|---|
| A3 | op-disc §28.3.1 trailer-preservation pitfall worked-example | **INCLUDE** | bb12806 worked example is canonical-grade; matches §28.5/§28.6 sub-section pattern |
| A4 | 5sr placement in CAPTAIN_DAEDALUS.md | **new §6.8 after §6.7** | parallels existing §6.5-§6.7 shape; named "Canonical-template wording-alignment discipline" per the actual Arc 24 anchor (re-framed from the original 5sr ticket label) |
| A5 | dhc canonical location | **VOID** | dhc CLOSED by user-tier-polybius @ 2026-05-18T06:47:41Z + PRINCIPAL-ratified; rev1's §25 PRINCIPAL-gate finding (substrate already has SSoT at MAJOR_PLINY.md §5.8.3) ratified; no substrate work in Arc 40 |
| A6 | 3sz placement | **γ — CAPTAIN_VERA.md new §5.11** | probe-authoring is VERA-specific; placement at op-disc §18 would widen beyond seat scope |
| A7 | 6n9 + t9u fold-in | **INCLUDE both** | install.sh adjacency provides natural co-location; both fixes ≤30 LOC; bundle at 5 candidates (rev2 post-dhc-drop) sits comfortably below the Arc 37 precedent ceiling of 6 |

---

## 7. Self-assessed weak points (CAPTAIN_DAEDALUS.md §6.2)

Honest middle per §6.2: I name the brittle spots; ARGUS names the risks I missed.

### 7.1 dhc closure — rev1 PRINCIPAL-gate ratified; no remaining weak point in rev2

Rev1 surfaced "dhc finding may not match PLINY's read of the directive A5 framing" as the load-bearing weak point: the §25 PRINCIPAL-gate at 2026-05-18T06:43:54Z said substrate already has SSoT at MAJOR_PLINY.md §5.8.3 and proposed narrowing the dhc work to cite-comments. Disposition: user-tier-polybius routed the gate to PRINCIPAL; PRINCIPAL ratified the finding; stoa--dhc CLOSED @ 06:47:41Z (~1 min post rev1 commit). The "weak point" is resolved by ratification — rev2 has no open dhc-related risk; A5 is VOID in §6.

### 7.1a Probe-authoring self-application teaching note (per ARGUS R3 NOTED)

ARGUS rev1 audit noted that the (now-dropped) probe p11 violated the §5.11 anchoring discipline this very arc ships via 3sz: p11 used `grep -c "python-vs-jq" substrate/operating-disciplines.md` — a bare substring grep with no `^` / `$` / surrounding-context anchor and no falsifying-evidence clause for wrong-location matches. That is precisely the failure mode §5.11 names. Teaching note for future probe-authoring inside this and successor arcs: **probe-authoring must self-apply §5.11 anchoring discipline 3sz ships** — substring greps without anchors are exactly the failure mode the discipline catches; future probe-authoring is screened by ARGUS / CATO against this self-application property. The dropped p11 is the canonical worked example; the surviving rev2 probes were re-audited for the same shape (see p3, p5, p7, p12 for examples of anchored alternatives using `^### N.M` heading anchors and `awk` range extractions).

### 7.2 A20 recursive-shape carries a circularity I cannot fully foresee

**Weak point:** PLINY's Phase 4 signoff is the canonical observation point for A20 — the signoff must cite the NEW §5.10 wording that THIS arc lands. But the signoff is authored by the very PLINY who is operating under the pre-Arc-40 §5.10 wording until merge happens. Concrete failure mode: PLINY drafts the Phase 4 signoff per the pre-Arc-40 §5.10 wording habits (omits the new bullet's discipline) → executes the squash-merge with `--body` override → drops the trailers AGAIN, despite shipping the canon prohibiting it. The self-application is genuinely novel: Arc 38 + Arc 39 practiced the discipline organically (no canon in the role file required them to); Arc 40 is the first arc where the canon being shipped governs the shipping operation. Worked counter-example: Arc 24 (which shipped the heartbeat-and-read-before-write canon and self-applied it during the gauntlet, documented at §10 of Arc 24 design.md) — that arc's substrate edit was a NEW addition (no prior wording to override); 6wp's edit is a NEW addition too, so the self-application loop should work. But the specific risk is PLINY's Phase 4 reflex defaulting to the Arc-37-era `--body` override pattern even with the new §5.10 bullet in role-file scope.

**Why this shape anyway:** The probe p19 above directly checks the self-application property (PLINY's signoff must cite the new §5.10 wording). Combined with A8 + the A2 substrate edit landing pre-merge, the recursive shape is observable, surveillable, and machine-checkable. ARGUS reading this design's §10 (recursive-shape worked example) + the probe p19 specification together has the full surface for audit. If the self-application fails despite the canon landing pre-merge, that is a 2026-05-18-empirically-novel surface that re-opens the discipline for arc-41+ refinement; the Arc 40 ship is correct to land the canon now even though the self-application carries a unique risk.

### 7.3 A2 wording precision (6wp one-line bullet) — a one-line edit has very little surface to get wrong, but every word matters

**Weak point:** The proposed §5.10 bullet wording was drafted to match the substrate's bullet-shape convention, but small word choices (e.g., "either omit `--body`... OR include the trailers" vs "either omit `--body`... OR include `Co-Authored-By:` trailers explicitly") change what a future PLINY reads at Phase 4. The W1 / W2 variants documented in §3.C1 are honest alternatives ARGUS may prefer for terseness or expanded worked-counter-example. The canonical pick names both acceptable patterns (omit vs include-explicitly) — but a future reader could misread "either ... OR" as "either ... or" (i.e., as if only one option is canonical) and pick the shorter form by default. The wording's load-bearing property is naming BOTH patterns as acceptable; my pick reads this way to me, but ARGUS-cold-read may surface a clearer phrasing.

**Why this shape anyway:** The bullet matches the existing four bullets' shape and length at §5.10 lines 428-433. A more elaborate worked-example exposition belongs in op-disc §28.3.1 (per A3 INCLUDE), where the pitfall-name + Arc 37 anchor + both-patterns-acceptable framing can expand to the paragraph-length §28-subsection shape without straining the §5.10 ship-checklist convention. ARGUS may revise the §5.10 bullet wording in plan critique; the underlying discipline is unambiguous (don't override default trailer auto-concatenation without explicitly preserving trailers).

### 7.4 A7 fold-in scope cohesion — 5 candidates in one arc, well within the upper bound

**Weak point (rev2; softened from rev1):** Arc 37 set the precedent at 6 candidates per arc; Arc 40 with A7 fold-in and the rev2 dhc drop sits at 5. The bundle splits across themes (Arc-24-era hygiene at 3sz/5sr + Arc-37-era trailer-fix at 6wp + install.sh-adjacency at 6n9/t9u). Each candidate is small, no candidate's design substantively depends on another candidate's, and the 5-candidate count sits comfortably below the Arc-37 precedent ceiling. The residual cohesion-tax risk is CATO Phase 3 reading the diverse-theme bundle as scope-creep rather than as a coherent Pass 6 follow-up batch.

**Why this shape anyway:** The directive explicitly authorizes the fold-in under A7 DAEDALUS-discretion with user-tier "weakly leans include." The install.sh adjacency provides a natural co-location for 6n9 + t9u that doesn't require their own arc. Bundling saves ≥1 arc-cycle per candidate (~hours of orchestrator + gauntlet time) for ~30 LOC of additional substrate edits. The cohesion judgment is honest: medium-to-high cohesion (helped by the dhc drop reducing the diverse-theme count), defended by orchestrator-cycle economics + the small per-candidate footprint. CATO Phase 3 may surface scope-disagreement; the substance-disagreement protocol per `operating-disciplines.md` §7.4 is the right venue. **If CATO flags scope concern, the recovery is straightforward: drop 6n9 + t9u to Arc 41 candidates; the 3 LOCKED candidates remain canonical-shape.**

---

## 8. Residual questions for ARGUS (rev2)

Rev1 residual question 1 (A5 disposition) discharged by PRINCIPAL ratification of dhc closure — removed.

1. **A4 re-framing.** The 5sr ticket labels the discipline "Edit-tool worktree-path discipline" but my read of the Arc 24 design.md §14.2 r5 + §13.4 anchors says the actual gap is "within-design canonical-template wording-alignment discipline." The new §6.8 subsection's heading reflects the latter framing. Is this re-framing audit-clean (the design names what Arc 24 actually surfaced) or does it widen 5sr in a way A16 hard-locks against? My read: narrows scope to the actual Arc 24 anchor; the original ticket label was slightly miscategorized but the underlying intent (DAEDALUS discipline closing the Arc 24 wording-drift gap) is preserved.

2. **A20 self-application risk at PLINY's Phase 4.** The probe p19 directly tests whether PLINY's Phase 4 signoff cites the new §5.10 wording. Rev2 softens p19's grep from rigid substring matching to alternation regex (per ARGUS R5 LOW disposition — see §8.4 below); is the softened probe sufficient to detect the recursive-shape failure mode (PLINY shipping the canon while inadvertently violating it at Phase 4), or should the design specify additional surveillance — e.g., a pre-merge VERA-side check that the merge-command string in PLINY's Phase 4 plan-comment is consistent with the new §5.10 bullet? My read: p19 (softened) + the A8 trailer-preservation probe (p1+p2 on arc-40/build commits BEFORE merge) cover the surface; the squash-merge itself is verifiable post-fact via `git log -1 --format='%B' <merge-sha>` on main. ARGUS to confirm or specify additional surveillance.

3. **Cite-comment shape for §28.3.1 → §5.10 cross-link.** The proposed §28.3.1 prose cites MAJOR_PLINY.md §5.10 as the "fix at the merge site." Reverse direction: the §5.10 bullet cites op-disc §28.3.1 as the canonical pitfall reference. Should the cross-link include a bidirectional cite-comment per A12, or is the in-prose paragraph cross-ref sufficient? My read: in-prose cross-refs are sufficient for §-to-§ links of this kind (matches existing precedent at op-disc §28.8 cross-refs and MAJOR_PLINY.md §5.10.2 cross-refs); explicit `<!-- CITE: -->` comments are reserved for code-adjacent (install.sh / check.sh / apply.sh) cross-refs where readers will most often miss the prose-narrative context. ARGUS to confirm.

### 8.4 Rev2 probe-spec self-application note (per ARGUS R3 NOTED + R5 LOW)

Rev2 audits the surviving probe specs against the new §5.11 anchoring discipline 3sz ships. Findings:

- **p19** (rev1) used the rigid substring `"Squash-merge \`--body\` override discipline"` — paraphrased signoffs that discharge audit-trail intent (e.g., "trailer-discipline self-applied via §5.10 squash-merge rule") would FAIL the rev1 p19. Rev2 softens p19 to an alternation regex matching the intent without rigid wording. See p19 spec for the alternation pattern.
- **Other probes (p3, p5, p7, p12, p17)** use `grep -c "^### N.M ..."`-style heading anchors or `awk '/^### N.M/,/^### N.M+1/'` range extractions — these self-apply §5.11 (anchored, with expected-count, with falsifying-evidence clauses). No softening needed.
- **The dropped p11** (dhc-cross-ref grep) was the canonical violation of §5.11; teaching note recorded at §7.1a above.

---

## 9. Follow-ups (out of scope for Arc 40)

Per the directive's Out-of-scope framing + A16 hard-locks, these surface as future-arc candidates:

- **Automated substrate cross-reference checker.** Arc 24 §13.4 named this; Arc 40 surfaces it again as A5's narrower pick relies on cite-comments at multiple sites. Still Arc 25+ follow-up surface.
- **Pre-commit hook / CI check for trailer preservation.** Per 6wp ticket Out-of-scope (convention is the layer). If the Arc 40 self-application surfaces a recurring trailer-drop pattern in post-Arc-40 arcs despite the canon, ticket a tooling-enforcement followup.
- **Cross-substrate utility skill consolidation (sp1 / save-verdict + copy-artifact + transcribe-bw-to-disk shared `_lib/`).** Arc 39 follow-up; explicitly out of Arc 40 scope per A16 "no retroactive sweep of OTHER substrate SKILL.md files beyond Arc 39 M3 widening."
- **A20 recursive-shape pattern accretion for stoa--bbi.** Arc 40 is N=1 for self-applied-canon-during-arc-that-ships-it (matching Arc 24's pattern but with a different discipline class). If Pass 9/10 stellation arcs ship more self-applied disciplines, the pattern accretes per `operating-disciplines.md` §6.7.1 toward "structural lesson" status. Track in stoa--bbi N-evidence column.
- **5sr "Edit-tool worktree-path discipline" original ticket label.** If a future arc surfaces an actual worktree-path discipline gap (e.g., DAEDALUS designs against worktree-local file paths that don't resolve when ADA dispatches in a different worktree), the §6.8 prose can be extended OR a new sub-subsection added. Today, no observable failure mode at design time; this design narrows 5sr to the actual Arc 24 anchor.

---

## 10. A20 recursive-shape surveillance (worked example)

This arc is the first arc where the trailer-preservation canon being shipped (§5.10 bullet + optional §28.3.1) IS the operational discipline the shipping arc itself is graded against. The recursive structure:

| Phase | Operation | Canon source for the operation |
|---|---|---|
| Phase 1 (design.md authoring) | DAEDALUS dispatched; authors this design.md including the §5.10 bullet + §28.3.1 spec | pre-Arc-40 §5.10 (no trailer-preservation bullet); §28.3 (default-behavior-only) |
| Phase 2 (ADA build) | ADA dispatched; lands the §5.10 bullet + §28.3.1 + 5sr §6.8 + 3sz §5.11 + (if A7) 6n9 + t9u install.sh wiring; commits per A8 trailers (dhc dropped per mid-design closure — no substrate work for it) | pre-Arc-40 §5.10 (commits in arc-40/build observable but not yet on main); A8 per directive |
| Phase 3 (VERA + CATO + ZENO review) | Probes p1-p23 execute on arc-40/build state; CATO craft-reads the diff; ZENO mechanical-checks | pre-Arc-40 §5.10 still on main; Arc 40 changes visible only on arc-40/build until merge |
| Phase 4 (PLINY ship) | `gh pr merge` executes; §5.10 bullet + §28.3.1 + other Arc 40 substrate edits land on main; PLINY's Phase 4 signoff comment on stoa--utn cites the NEW §5.10 wording | **NEW Arc 40 §5.10 wording (just landed by Phase 4's own merge operation)** |

**The recursion's load-bearing property:** PLINY's Phase 4 squash-merge MUST follow the new §5.10 bullet's discipline (omit `--body` OR include trailers explicitly) even though the bullet only becomes substrate-canon at the moment of the merge itself. The new canon is observable in PLINY's role-file scope from the moment Phase 2 lands the §5.10 edit in arc-40/build (PLINY can read the file in arc-40/build pre-merge); the new canon is enforced on main from the moment Phase 4 merges. Phase 4's merge operation is the canon's first self-applied execution.

**The three-part Phase 4 surveillance check (per directive A20):**

1. **(a) §5.10 edit committed to arc-40/build pre-merge.** Verifiable: `git log --all -- substrate/MAJOR_PLINY.md` shows the §5.10 bullet edit on arc-40/build BEFORE the merge SHA. Probe coverage: implicit (p3 + p4 verify the edit landed in substrate/MAJOR_PLINY.md by post-merge state).
2. **(b) Deployed file at user-tier matches substrate-tier source after Arc 40 ships.** Verifiable: post-merge, `diff <(git show main:substrate/MAJOR_PLINY.md) <user-tier-deployed-path>/MAJOR_PLINY.md` is empty (modulo deployed substitutions). Probe coverage: not Arc-40-scope (post-merge user-tier substrate-update is the check-substrate-updates skill's job per Arc 38/39 canon).
3. **(c) PLINY's own Phase 4 signoff cites the new §5.10 wording correctly.** Verifiable: PLINY's signoff comment on stoa--utn cites the new wording explicitly (proving PLINY read the new role-file scope during Phase 4 and applied it to the merge operation). Probe coverage: **p19 above**.

The recursion is observable, surveillable, and machine-checkable per the surveillance check + probe p19. ARGUS audits the design's self-awareness here (this §10); CATO craft-reads the recursion's prose framing; VERA executes p19; ZENO spec-checks p19's pass/fail criteria. The pipeline's redundant-checker property covers the recursion at four checkpoints.

**If the recursion fails (probe p19 returns 0 — PLINY's signoff does not cite the new §5.10 wording):** the failure is recoverable and not catastrophic. The §5.10 canon still ships on main; the Phase 4 squash-merge can be examined post-fact to confirm trailer preservation regardless of whether PLINY's signoff prose mentions the discipline by name. The signoff-cite check is the *audit-trail* property; the squash-merge-trailer-preservation is the *operational* property. Both can pass independently; both passing is the canonical Arc 40 ship; only one passing surfaces a substance-disagreement venue per `operating-disciplines.md` §7.4 for adjudication of whether the partial pass is sufficient.

---

## 11. Verdict (this dispatch return)

Per CAPTAIN_DAEDALUS.md §7 verdict format; full block returned in DAEDALUS dispatch response to MAJOR_PLINY (not duplicated here — design.md on disk is the artifact for ARGUS to read; verdict block lives in dispatch return + bw comment per CAPTAIN_DAEDALUS.md §7).

**Heartbeat audit (rev1):** activation heartbeat fired at 06:42:40Z; state-transition heartbeat at read-complete with key dhc finding fired before drafting; completion heartbeat fired immediately before rev1 dispatch return @ 06:46:xx (rev1 commit 76928152). Read-before-write fired before each heartbeat. No comments tagged `[for: DAEDALUS]` surfaced during rev1; no orchestrator interruption during design.

**Heartbeat audit (rev2):** rev2 dispatched after ARGUS audit + dhc closure ratification (~06:47:41Z). Rev2 in-session; no separate dispatch ticket. Revisions per PLINY dispositions: R1 BLOCKING (drop §3.C3, drop p9/p10/p11, update §6/§1.2/§2.7/§7.1/p24, narrow scope 6→5); R2 MEDIUM (probe recount 23→21); R3 NOTED (teaching note §7.1a); R4 MEDIUM (p24 ticket list 6→5 + optional merge-SHA-cite strengthening); R5 LOW (soften p19 grep); R6 LOW (keep t9u *.pyc); R7 LOW (reword §28.3.1 framing). Probe gap-numbering preserved per PLINY-lean for ARGUS/ZENO/VERA traceability across rev1→rev2.

Per A11 IMMUTABLE: all edits credit **Denson Smith**. No author field gets a different name. No exception.

---

*End of design. Per the directive's Phase 1 spec, this surfaces to MAJOR_PLINY for routing to ARGUS Phase 1 audit. ARGUS verdict gates ADA dispatch.*
