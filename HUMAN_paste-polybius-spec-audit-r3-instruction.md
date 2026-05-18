Re-read .claude/MAJOR_POLYBIUS.md and assume the project-tier chief-of-staff role for the-stoa. (Post-`/clear`; role refresh from canon file.)

**Your immediate intent for this engagement:** THIRD-PASS SPEC AUDIT (R3). You did R1 at `SPEC_AUDIT.md` (commit `4f4674e`) + R2 at `SPEC_AUDIT_R2.md` (commit `a50a1a8`). User-tier POLYBIUS folded R2's findings via commit `a1a10e4` (the structural §12 fix per R2.5 closing observation + mechanical NC1-NC5 + A4 + X5/Y1 fixes per PRINCIPAL's "fix all in this pass" pick). R3 verifies the fold-in is correct + tests whether the structural §12 fix actually closed the staleness pattern that R1 + R2 both caught.

R3 scope is narrower than R2 — iteration audit on a smaller delta (3 files changed; 46 insertions / 85 deletions). Expected wall-clock: 20-30 min.

**Operating mode:** Mode 2 (exploration) with ARGUS-discipline overlay (surface concerns; do NOT propose fixes; do NOT execute changes; do NOT dispatch any arc).

---

## What changed since SPEC_AUDIT_R2.md (commit `a1a10e4`)

**Three files edited in one commit:**

### `SPECIFICATION.md` — structural §12 rewrite (the load-bearing change)

§12 was previously enumerated snapshots (37 arcs listed; 18 open tickets listed; commit history listed). R1 + R2 caught the same `§12 internal staleness` pattern at different inflection points. The R2 closing observation surfaced two fix-shape candidates (procedural §12 re-sweep checklist vs structural §12-as-derived-view); PRINCIPAL picked the structural fix.

New §12 shape: derived view. Each subsection describes WHAT COUNTS as the named state-class + the QUERY that returns current state. The spec carries the contracts; current state lives in `bw` + `git log` + `git status` + §13.

- **§12.1 What counts as shipped** — describes shipped-state + git/gh queries; brief reference SHAs for orientation only (Arc 35, Arc 36 v2, Arc 37 ships named).
- **§12.2 What counts as in flight** — describes in-flight-state + 4 queries (git branch / git ls-remote / gh pr list / bw list for engagement coord tickets).
- **§12.3 What counts as open** — describes open-ticket-state + bw query (with explicit `--all` flag + TIRO empirical-anchor cross-ref); bucketing in §13.5-§13.8.
- **§12.4 What counts as working-tree clean** — describes clean-state + git status / ls _drafts/ / git log queries.
- **§12.5 Known gaps** — authored content; gap-list itself lives at §13.5-§13.8 + §13.9 + §13.10.

The R2 findings NC1 + NC3 + NC4 are obsolesced by structural removal (the sections they targeted no longer carry state).

### `SPECIFICATION.md` — mechanical NC5 + A4 fixes

- **§13.7 line 593** (NC5): "Pass 9 stellation dispatch" → "Pass 10 stellation dispatch" (W1 renumber missed; now correct).
- **§13.7 closing line + §13.13 criterion 2 reconciled (A4):** explicit substrate-canon-ticket boundary definition added; cross-ref to §13.13 criterion 2 as the broader operational gate; §13.7 sentence is its narrower echo.

### `substrate/skills/handoff-author/SKILL.md` — NC2 frontmatter fix

Line 4 description bumped: "Optionally records the prior-generation session id" → "Mandatorily records ... (recording is mandatory not optional per 2026-05-17 PRINCIPAL ratification of SPEC_AUDIT C1; if the session id is genuinely unrecoverable, explicitly note the truncation)." Frontmatter description now matches step 6 body which was upgraded at `d0cbc84`.

### `docs/validation/stellation-SPECIFICATION.md` — X5/Y1 cross-ref fixes

4 line-replacements:
- §3 line 3: "§13.7" → "§13.12 (behavioral validation via test-project dispatch)"
- §7 line 7: "§13.7" → "§13.12 (Pass 10 behavioral validation)"
- §9 criterion 6 line 217: "§13.7 Pass 6 observation trail" → "§13.12 Pass 10 observation trail" + explicit artifact path
- §12 line 279: "§13.10" → "§13.15 (Mode + dispatch)"

---

## What R3 audits (priority order)

### R3.1 Per-R2-finding verification

For each R2 finding (NC1-NC5 + the △ items: C1+NC2, C2, M6, S-A, W1, W3 + the ○ items: A4, X5, Y1, W2), verify the fold-in's disposition is correct:

- **Addressed correctly** — the edit fixes the finding as expected.
- **Addressed with new concerns** — the edit fixes the finding but introduces a different issue.
- **Not addressed / partially addressed** — the edit doesn't fix the R2 finding.
- **Deliberately deferred (W2 only)** — sanctioned per PRINCIPAL non-pick.

The commit message at `a1a10e4` enumerates dispositions. Verify against actual spec edits.

### R3.2 Structural §12 internal consistency (the load-bearing test)

The structural fix's central claim: §12 cannot drift from substrate state because it doesn't carry substrate state. Verify:

- **No leftover enumerations:** §12.1-§12.4 should NOT enumerate specific commits / tickets / branches. (Reference points in §12.1 for orientation are OK; per-ticket lists are not.)
- **Queries are actionable:** for each query listed in §12.x, a fresh team running it gets a useful answer. Run `bw list --status open --all` and verify it matches §12.3's claim that this is the canonical open-ticket query.
- **§12.5 → §13 cross-refs work:** §12.5 says "the gap list lives at §13.5-§13.8 + §13.9 + §13.10." Verify the cross-refs resolve + the §13.x sections actually contain the gap enumeration.
- **No new staleness surfaces introduced:** if the structural §12 rewrite has any NEW content that re-encodes substrate state (e.g., a "reference SHAs for orientation" section that could go stale), flag it.

### R3.3 Fresh-eyes on new §12 prose

The structural rewrite added ~50 lines of new §12 prose. Standard ARGUS-discipline fresh-read for:

- New ambiguities introduced by the rewrite.
- New contradictions between §12 subsections and other sections (especially §13.5-§13.8 which §12.5 cross-refs).
- New cross-ref errors in the structural shape.
- "I don't understand" items in the new §12 prose.

### R3.4 Substrate-state-vs-spec re-check

Re-run the standard live checks:

- `bw list --status open --all` returns N tickets. Verify N matches what §12.3 implies (should be 18 at audit time unless new tickets are filed during R3).
- `git log` matches the spec's reference SHAs in §12.1.
- `substrate/skills/handoff-author/SKILL.md` frontmatter description line 4 now reads "Mandatorily records" (NOT "Optionally records").
- `substrate/skills/handoff-author/SKILL.md` step 6 body line 44 still reads "MANDATORY" (unchanged from d0cbc84).
- stellation-SPECIFICATION.md cross-refs to the-stoa SPECIFICATION.md §13.x all resolve.
- §13.7 line 593 says "Pass 10" not "Pass 9".

### R3.5 Meta-verdict — did the structural fix close the §12 staleness pattern?

The load-bearing question. R1 + R2 both caught the §12 internal staleness pattern at different inflection points. The structural fix's central claim: removing state-carrying content eliminates the drift class entirely.

Test the claim:

- **Look for any §12 surface that still carries state** that could drift when source-of-truth advances. If you find one, the structural fix is incomplete.
- **Look for §12 references in other spec sections** (§13.x, §14, etc.) that imply §12 still carries state. If §13.x reads §12 as a state-snapshot somewhere, the §13.x reference is now wrong (it should read §12 as a query-source).
- **Compare R1 + R2 patterns to current state:** R1 caught §12.1/§12.2/§12.5 lagging post-Arc-37 while §12.3 was fresh. R2 caught §12.3/§12.2 lagging post-W1-split while §12.5/§13.7/§13.8 were fresh. Is there ANY remaining mechanism by which §12 could lag substrate state? If yes, flag the mechanism (even if no current instance exists).

**If R3 surfaces ANY new instance of the §12 staleness pattern** (current OR latent mechanism), that's load-bearing evidence the structural approach is incomplete and the spec needs deeper redesign. **If R3 confirms the pattern is structurally closed**, the spec is ready for Arc 38 dispatch and we have N=2 empirical support for the broader claim that structural fixes succeed where procedural fixes recur (per §4.6 + §27 substrate pattern).

---

## Required R3 output

Produce `SPEC_AUDIT_R3.md` at repo root, structured by:

1. **Per-R2-finding verification table** — one row per R2 finding (NC1-NC5 + △ items + ○ items + W2). Verdict legend same as R2 (✓ / △ / ○ / D / n/a).
2. **Structural §12 internal consistency check** — pass/fail per the R3.2 sub-checks. Brief evidence per check.
3. **New issues found** — fresh items from R3.3, if any. Categorized similarly to R1's category set.
4. **Substrate-state re-check** — like R2's §3, updated for current main + post-fold-in state.
5. **Meta-verdict on the §12 staleness pattern** — the load-bearing answer from R3.5. Be explicit: "closed structurally" vs "still latent at <mechanism>" vs "current instance found at <location>."
6. **Closing observation** — any meta-pattern observable across R1 + R2 + R3, especially the structural-vs-procedural-fix hypothesis.

### Output discipline (same as R1 + R2)

- ARGUS-discipline: surface, do not fix.
- Honest "addressed correctly" entries useful positive signal.
- N=1 honesty per `operating-disciplines.md` §6.7.1.

---

## Constraints (same as R1 + R2)

- DO NOT dispatch any arc.
- DO NOT propose fixes.
- DO NOT edit SPECIFICATION.md or other substrate files.
- DO NOT touch stellation workspace.

## bw query discipline (same as R1 + R2; TIRO still doesn't exist)

CAPTAIN_TIRO is Arc 38 candidate `stoa--ojz`, not yet built. Use `bw list --all` directly per operating-disciplines.md §12.1 cookbook + the new §12.3 explicit guidance.

---

## Sub-dispatch authority

R3 is small scope; single-seat-direct may be appropriate (R1 + R2 did this). PLINY (paste at `HUMAN_paste-pliny-spec-audit-r3-instruction.md`) can dispatch CAPTAINs at your request if a specific check warrants it.

## Coordination

- **PLINY** is your radio-check peer.
- **Coordination ticket:** file a fresh one for R3 (e.g., named "spec-audit R3 engagement coordination"). Use `[from: polybius-the-stoa]` tags. **Close it on engagement-end** (R1 omitted; R2 got it right; maintain the discipline).
- **User-tier POLYBIUS** upper-tier escalation via `[for: user-tier-polybius]`.
- **PRINCIPAL** is exception-handler.

## Polling cron + renewal per Arc 36 v2 §11 step 1.5

Set up your polling cron at `*/5 * * * *`; schedule renewal at +144h. R3 is short (~20-30 min); renewal won't fire; canon application forward is what matters.

## Closure

When `SPEC_AUDIT_R3.md` complete:

1. Commit + push (user-tier housekeeping per §18.1).
2. Post `[from: polybius-the-stoa]` closure comment on R3 coord ticket.
3. Close the R3 coord ticket per engagement-end discipline.
4. Tag `[for: user-tier-polybius]` for handoff.
5. Surface to PRINCIPAL with one-line: "spec audit R3 complete; SPEC_AUDIT_R3.md at repo root; <N> R2 findings verified addressed, <M> remain open, <K> new issues, structural-fix meta-verdict: <closed/latent/recurred>; standing by."
6. Stand down with `[radio-check polybius-the-stoa standing down]`; CronDelete polling + renewal crons.

---

## Self-application

R3 operates under the post-structural-fix spec. The §6 multi-checker discipline + §19.6 attestation-honesty + §7 author-tag convention + §5.10 signoff-accuracy all apply. Single-seat-direct R3 is acceptable (R1 + R2 precedent); multi-checker is PRINCIPAL + user-tier POLYBIUS reviewing R3.

**If R3's meta-verdict is "the structural fix worked,"** that's strong empirical signal for the broader substrate principle that structural fixes succeed where procedural fixes recur. The signal supports the §4.6 TIRO pattern + the §27 mechanical-script / agent-inspection split pattern + this §12 structural rewrite as instances of the same family. Future arcs may want to look for additional opportunities to apply structural fixes to recurring procedural failures.

**If R3's meta-verdict is "the pattern still has a latent mechanism,"** the structural fix is incomplete and the spec needs another iteration. Surface the specific mechanism so user-tier POLYBIUS + PRINCIPAL can decide whether to do another structural pass or accept the latent risk.

If compaction or /clear erases your role, re-read this paste from `HUMAN_paste-polybius-spec-audit-r3-instruction.md` in the project root.
