# Design — Arc 74 verdict-attestation integrity (`attach_status` is dispatch-return-only; the attested verdict body is frozen at the sha round-trip) — **rev2**

> **supersedes design-rev1.md; folds ARGUS rulings Q1(in-scope)/Q2(adopt)/P2(3-site correction).**
> Read this (rev2) as the single build SSoT — it is a complete standalone design, not a diff against rev1. ADA builds against rev2.

**Charter:** `stoa--x5t` | **Arc:** 74 | **Phase:** A (design, rev2) | **Author seat:** CAPTAIN_DAEDALUS_the-stoa
**Authored on behalf of:** the PRINCIPAL (Denson Smith)
**Scope contract:** `substrate/arcs/arc-74-build-directive.md` (DC1–DC5)
**Builds on:** the-stoa `main` @ dacb9fd (arc-74 directive-tracking commits already on main)
**Critique consumed:** `agents/verdicts/stoa--x5t/ARGUS-2026-06-25T03-40-37Z.md` (PASS, no load-bearing risk) — Q1 ruled IN SCOPE, Q2 full byte-identity adopted, P2 three-site correction mandated (ARGUS + floor-manager concurred).

---

## 0. What rev2 changes vs rev1 (orientation only — the body below is self-contained)

Three folds, all from accepted ARGUS rulings (the floor-manager build-spec at `stoa--x5t` 03:46Z carries the same three):

1. **Q1 fold — DC2(b) P8→manual-diff doc-coherence repair is now COMMITTED, not gated.** rev1 made it conditional on an ARGUS ruling; ARGUS ruled IN SCOPE, so DC2(b) is a mandatory part of the DC2 build instruction (§2.2b). The residual question that gated it is removed from §7.
2. **Q2 fold — the FULL post-fix bw-comment sentence is byte-identical across VERA/ARGUS/CATO** (§2.1d). rev1 left a conditional ("preserve each file's existing trailing-parenthetical convention") pending the ruling. ARGUS adopted full byte-identity. **On-disk correction:** rev1's premise that VERA lacked the §12 parenthetical was STALE — all three current sentences are already byte-identical and all carry the §12 parenthetical (re-confirmed this Phase by `diff`). The fold is therefore expressed as: ADA writes ONE verbatim post-fix replacement sentence into all three, byte-identical; the rev1 "preserve each file's convention" conditional is dropped.
3. **P2 three-site correction — the P2 probe's expected-survivor set is now all THREE legitimate post-fix sites** (§3 P2), with role-file locators. rev1 named only two. The third (the §7 byte-aligned region's `attach_rc`-capture COMMENT, inside the UNTOUCHED 494b442e region) must be in the expected set so VERA does NOT false-route-back on a legitimate surviving occurrence.

Everything else (DC1 mechanism, DC3 region-untouched determination + four-home diff spec, DC4 documented-invariant + P1 demo probe, DC5 not-threat-ratified) is carried forward unchanged from rev1 — those are settled and are NOT re-opened.

---

## 1. Problem restatement

The reviewer-seat **Verdict format** block (`CAPTAIN_VERA.md` §6, `CAPTAIN_ARGUS.md` §7, `CAPTAIN_CATO.md` §7) is used for **three** purposes at once:

1. **the dispatch return** — the block the seat ends its dispatch with;
2. **the `bw comment`** — "post the same block as a `bw comment` on the ticket";
3. **the `<verdict-body>`** — the §7 byte-aligned bash region `printf`s this block to the canonical `.md`, sha256-round-trips it, and `bw attach`es it to beadwork as the byte-canonical attested artifact.

That single block contains two fields — `attach_status` and `attach_failure` — whose values are knowable **only after** the `bw attach` runs. But in the §7 sequence the body is `printf`'d and hashed **before** the attach. So whenever a seat fills `attach_status: OK` into the block and then commits that same block in-tree (the new pattern of tracking verdicts in-tree), the committed in-tree verdict diverges from the cited/attested sha by exactly that one field. This was observed live on `sos--yn2`: in-tree blob `a6a16d9b` vs bw-attached blob `bbf9fe6f`, both pure-LF, differing only at one line (`attach_status` blank-vs-`OK`), a 3-byte delta. `save-verdict.md` clause (d) **already** says `attach_status` belongs in the dispatch return; the role-file §6/§7 format silently contradicts it by embedding the field inside the block that becomes the attested artifact.

The fix: make `attach_status`/`attach_failure` **dispatch-return-only**, and make the sha-attested verdict body **frozen at the round-trip** — so the attested body NEVER contains a field whose value is knowable only after the attach, and committed-sha == attested-sha holds by construction for any in-tree-tracked verdict.

**Imported assumptions named (per §6.1):**
- I read the directive's "§6" as shorthand. The actual verdict-format section is **VERA §6, ARGUS §7, CATO §7** (verified by heading-line grep + floor-manager + ARGUS independent re-measure). ADA must target the real section numbers, not "§6" literally.
- The directive's reference to a "P8 `diff`" gate is explicitly retired (charter + directive both state: **no automated cross-file gate exists**; byte-identity is enforced ONLY by a manual four-home `diff`). `save-verdict.md` itself still says "P8 `diff`" at exactly two spots (L31, L147 — re-confirmed this Phase that the three role files carry NO "P8" string; only save-verdict.md does). ARGUS ruled the correction IN SCOPE, so DC2(b) corrects both (§2.2b).
- I assume "frozen at the round-trip" means: once `printf '%s' '<verdict-body>'` has run and the sha256 check passed, the on-disk `.md` is never edited again by the seat. This is the load-bearing behavioral statement the fix codifies.
- **rev2 on-disk correction:** rev1 assumed VERA's bw-comment sentence lacked the §12 trailing parenthetical that ARGUS/CATO carry. That premise was STALE — re-checked this Phase, all three current bw-comment sentences are byte-identical and all carry the `(Canonical bw operations reference: `operating-disciplines.md` §12.)` parenthetical (VERA L268 / ARGUS L249 / CATO L214). The Q2 fold (full byte-identity of the *post-fix* replacement sentence) still applies; only the rev1 conditional that referenced the false asymmetry is dropped.

The restatement converges with the brief. No divergence requiring refusal.

---

## 2. Approach

The fix is **structural and prose-only inside the §6/§7 verdict-format sections** of the three reviewer role files, plus a reinforcement + doc-coherence repair in `save-verdict.md`. It does NOT touch the byte-aligned bash region (DC3 — confirmed below; independently re-measured by ARGUS + the floor-manager at sha `494b442e…`). The mechanism: split the one conflated block into **two clearly-labeled blocks** — an **attested verdict body** (everything that goes into `<verdict-body>`) and a **dispatch-return-only addendum** (the two post-attach fields) — and add a verbatim frozen-body statement, identical across all three reviewers.

### 2.0 Why the byte-aligned region needs no change (the keystone)

The byte-aligned region (`SAVE-VERDICT-BYTE-ALIGNED-REGION:BEGIN`…`END`) writes the body via `printf '%s' '<verdict-body>'` — `<verdict-body>` is a **named substitution slot** the seat fills from its verdict-format section. The region has **never** contained `attach_status` as a body field; it only captures `bw attach`'s real exit code into `attach_rc` and leaves a stderr breadcrumb, and it MENTIONS `attach_status` in a COMMENT (describing how the seat sets the dispatch-return field) — that comment is inside the region but is not a body field. The bug lives entirely in **what the seat copies into the `<verdict-body>` slot** — i.e. in the §6/§7 verdict-format block definition, not in the bash. Therefore the fix is to redefine the slot's contents (exclude the two post-attach fields) in prose, and the region stays byte-identical. This is the cleanest possible fix surface and is why DC3's "prefer untouched" is satisfiable.

### 2.1 DC1 — separate the attested body from the dispatch-return addendum (all 3 reviewers)

In each of `CAPTAIN_VERA.md` §6, `CAPTAIN_ARGUS.md` §7, `CAPTAIN_CATO.md` §7, restructure the single verdict-format fenced block as follows.

**(a) Remove `attach_status` and `attach_failure` from the verdict-format fenced block.** These are the lines currently at:
- VERA L254–255
- ARGUS L237–238
- CATO L200–201

Delete them from the fenced ```` ``` ```` verdict block (the block that becomes `<verdict-body>`). The block keeps every other field unchanged (status, ticket, verdict, the seat-specific body fields, summary, gap_or_blocker, etc.). The relative order of all surviving fields is unchanged.

**(b) Add a new, clearly-labeled dispatch-return-only addendum** immediately AFTER the verdict-format fenced block and its "Verdict definitions" / threat-coverage notes, but positioned so it reads as a separate emission AFTER the §7 attach. The addendum carries exactly the two removed fields. It uses this **exact label** (byte-identical across all three reviewers):

> **Dispatch-return-only addendum (emitted AFTER the §7 `bw attach` — NEVER part of the attested verdict body).**

followed by a fenced block containing the two fields verbatim (text unchanged from today — only their HOME moves):

```
attach_status: <OK | FAILED — did `bw attach` of the saved verdict to the coordination ticket succeed? (Canonical verdict-save path / `modules/save-verdict.md`)>
attach_failure: <only if attach_status == FAILED: bw attach exited rc=<n>; verdict integrity-verified on disk at <DEST> (sha256 <hash>); NOT yet on beadwork — orchestrator MUST retry/escalate before treating this verdict as durable>
```

**(c) Add the frozen-body statement** — this sentence, **verbatim and byte-identical across all three reviewer files**, placed in the prose introducing the dispatch-return-only addendum (so it sits at the seam between "what gets attested" and "what gets reported after"):

> **Frozen-body rule:** the verdict body you `printf` as `<verdict-body>` in §7 is FROZEN at the sha256 round-trip — it is the byte-canonical attested artifact and you MUST NOT post-edit it (no post-attach body mutation). `attach_status`/`attach_failure` are knowable only AFTER the attach, so they live ONLY in the dispatch-return addendum below and in your dispatch return — never in the attested body, the `bw attach`ed copy, or the `bw comment` posted from the body.

**(d) Fix the "post the same block as a `bw comment`" instruction so it cannot re-import the bug — FULL byte-identity across all three (Q2 fold, ADOPTED).** Today each of VERA L268 / ARGUS L249 / CATO L214 reads — **byte-identically** (re-confirmed this Phase by `diff`; the rev1 claim that VERA differed was stale):

> Also post the same block as a `bw comment` on the project's beadwork ticket if `bw` is initialized. (Canonical bw operations reference: `operating-disciplines.md` §12.)

Replace it in all three with this **single exact sentence, byte-identical across VERA/ARGUS/CATO** (the §12 parenthetical is carried on all three — they already all carry it, so no asymmetry is introduced):

> Also post the attested verdict body (the frozen `<verdict-body>` from §7 — NOT the dispatch-return-only addendum) as a `bw comment` on the project's beadwork ticket if `bw` is initialized. (Canonical bw operations reference: `operating-disciplines.md` §12.)

The load-bearing change is "the same block" → "the attested verdict body (the frozen `<verdict-body>` from §7 — NOT the dispatch-return-only addendum)", so the comment is byte-equal to the attested artifact and the addendum is excluded from the comment. Because the three current sentences are already identical, this is a straight verbatim replacement of one identical sentence with another identical sentence in all three files — P3 (parallelism) now guards the full sentence, not merely a load-bearing clause.

**Parallelism (automatic route-back if violated):** the addendum label, the frozen-body sentence, the two field-text lines, AND the full bw-comment replacement sentence MUST be byte-identical across VERA/ARGUS/CATO. The surrounding seat-specific verdict fields differ by design (VERA has `probes_executed`, ARGUS has `audit_block`, CATO has `concerns`) — that pre-existing difference is expected and is NOT a parallelism violation. What must be parallel is the *new/replaced* machinery (label + frozen sentence + the relocated two fields + the full bw-comment replacement sentence).

### 2.2 DC2 — `save-verdict.md` reinforcement + P8 doc-coherence repair (Q1 fold: both committed)

`save-verdict.md` clause (d) already states `attach_status` belongs in the dispatch return (L107–112) and the byte-aligned region already does NOT emit it as a body field (the `attach_rc`-capture comment, L70–76). DC2 makes two committed edits:

**(a) clause (d) body-freeze reinforcement.** In clause (d), add a sentence stating plainly:

> The `<verdict-body>` written by the §7 `printf` is FROZEN at the sha256 round-trip: the bw-attached copy is the byte-canonical attested artifact, and `attach_status`/`attach_failure` (dispatch-return-only, this clause) MUST NOT be written into that body — a post-round-trip body edit diverges the committed in-tree verdict from the attested sha (the `stoa--x5t` / `sos--yn2` defect).

This reinforces, does not contradict, the durability contract (the on-disk artifact stays the lossless retry source; the orchestrator close-loop at `MAJOR_PLINY.md` §5.16 is unchanged). It is purely additive — the clause-(d) durability contract, the four locked clauses, the exit-code map, and the attach-failure posture are all untouched in substance.

**(b) Stale "P8 gate" doc-coherence repair — COMMITTED (Q1 ruled IN SCOPE).** `save-verdict.md` L31 and L147 say the region is "guarded at build time by the P8 `diff`" / "the P8 `diff` enforces." The charter + directive establish there is **no P8 / automated cross-file gate** — byte-identity is enforced only by a manual four-home `diff`. Leaving an "automated gate exists" claim in the very module this arc reasons about would actively mislead the next verifier into skipping the mandatory manual diff this arc relies on. ARGUS ruled this IN SCOPE (inside the file DC2 already edits, removes an actively-misleading stale claim this very arc disproves). It is no longer gated — ADA corrects both occurrences as a committed part of DC2:

- **L31** — exact stale claim: `guarded at build time by the P8 `diff` (`canonical-template-alignment.md`).` → corrected to: `kept byte-identical across the four homes by a manual four-home `diff` (`canonical-template-alignment.md`; there is no automated cross-file gate).`
- **L147** — exact stale claim: `- `canonical-template-alignment.md` (the byte-alignment discipline the P8 `diff` enforces over the region above).` → corrected to: `- `canonical-template-alignment.md` (the byte-alignment discipline; the four-home byte-identity is enforced by a manual `diff`, not an automated gate).`

Verified this Phase: these are the ONLY two "P8" occurrences across all four edit-target files (the three role files carry no "P8" string), so DC2(b) is fully bounded to these two sites. Post-fix, zero "P8" strings remain in any of the four files (P5 asserts this).

### 2.3 DC3 — byte-aligned region: UNTOUCHED (determination + four-home diff spec)

**Determination: the §7 `SAVE-VERDICT-BYTE-ALIGNED-REGION` is byte-UNTOUCHED by this fix.** Justification: the region never wrote `attach_status` as a body field (§2.0); it only captures `attach_rc` and mentions `attach_status` in a descriptive comment. The fix changes only the prose definition of the `<verdict-body>` slot and adds a dispatch-return-only addendum OUTSIDE the sentinels. No edit lands between any `BEGIN`/`END` sentinel pair in any of the four homes. (Independently re-measured + CONCURRED by ARGUS and the floor-manager this Phase.)

**Baseline (authoring-time evidence):** all four regions are currently byte-identical — sha256 `494b442ea512949906134c4318786acf7ad6f63785fef19e6afee8bc6d2842cb` (measured this Phase, re-measured by ARGUS + floor-manager). The fix must leave this sha unchanged in all four homes.

**Four-home diff the verifier (VERA/CATO) + close-gate (NOMOS) MUST run by hand** (there is no automated gate). Two equivalent forms — run from the worktree root `C:/Users/denso/claude_projects/the-stoa/.claude/worktrees/arc-74-build`:

Form 1 — pairwise `diff` of the extracted region (canonical, matches `canonical-template-alignment.md` idiom):
```bash
extract() { awk '/SAVE-VERDICT-BYTE-ALIGNED-REGION:BEGIN/{p=1;next} /SAVE-VERDICT-BYTE-ALIGNED-REGION:END/{p=0} p' "$1"; }
diff <(extract substrate/modules/save-verdict.md) <(extract substrate/CAPTAIN_VERA.md)
diff <(extract substrate/modules/save-verdict.md) <(extract substrate/CAPTAIN_ARGUS.md)
diff <(extract substrate/modules/save-verdict.md) <(extract substrate/CAPTAIN_CATO.md)
```
All three `diff`s MUST return empty (identical region across the four homes).

Form 2 — single-command sha equality (the demonstration form):
```bash
for f in substrate/modules/save-verdict.md substrate/CAPTAIN_VERA.md substrate/CAPTAIN_ARGUS.md substrate/CAPTAIN_CATO.md; do
  awk '/SAVE-VERDICT-BYTE-ALIGNED-REGION:BEGIN/{p=1;next} /SAVE-VERDICT-BYTE-ALIGNED-REGION:END/{p=0} p' "$f" | sha256sum
done
```
All four lines MUST print the identical hash, and that hash MUST equal the pre-fix baseline `494b442e…` (proving UNTOUCHED, not merely internally-consistent).

**If ADA finds it must touch the region** (it should not need to): the change must be re-applied byte-identically to all four homes, and the four-home `diff` above must still return empty. The design's strong preference and determination is UNTOUCHED.

### 2.4 DC4 — committed-sha == attested-sha guard: documented invariant, NO new mechanical check in the region

**Decision: do NOT add a new mechanical gate. Document the invariant in `save-verdict.md` and add a one-line demonstration probe to the arc's verification set (§3 P1).** Rationale (ARGUS CONFIRMED this as a well-justified call that preserves the DoD demonstration):

- The bug's root cause is structural (a field in the wrong block), and DC1 removes it at the source. Once the attested body excludes post-attach fields, committed-sha == attested-sha holds *by construction* for any in-tree-tracked verdict authored under the new format. A standing mechanical guard would be defending against re-introduction of a defect the structure now prevents — low marginal value.
- Bolting a `committed-sha == cited-sha` check into the byte-aligned region is explicitly disallowed by the directive (would force a four-home re-align for marginal value) — and the region runs at *verdict-write* time, before any commit exists, so it structurally cannot compare against a committed sha anyway.
- A close-gate/NOMOS-on-merge assertion would be a real but heavier mechanism. It is **deferred, not adopted**: the in-tree-verdict-tracking pattern is new and not yet universal; a per-arc demonstration probe (§3 P1) plus the documented invariant covers this arc's DoD ("a verdict authored under the NEW format has committed-sha == attested-sha") without standing infrastructure. If in-tree verdict tracking becomes the default across arcs, a NOMOS-on-merge `git cat-file` vs `bw attach`-blob equality assertion is the right home — captured as a follow-up (§5 / DC4-followup), not built here.

**What ADA writes for DC4:** a short invariant note in `save-verdict.md` (adjacent to the clause-(d) reinforcement):

> **Attestation invariant (DC4 / `stoa--x5t`).** Because the attested `<verdict-body>` excludes every field whose value is knowable only after the attach (`attach_status`/`attach_failure`), a verdict tracked in-tree has committed-sha == cited/attested-sha *by construction*. No mechanical gate enforces this beyond the §7 sha256 round-trip; the structural exclusion is the guarantee. A future arc MAY add a NOMOS-on-merge `git cat-file`-vs-attached-blob equality assertion if in-tree verdict tracking becomes universal.

### 2.5 Hand-off contract for ADA (exact edit targets)

| File | Section | Remove from fenced body | Add after the block | Edit in place |
|---|---|---|---|---|
| `substrate/CAPTAIN_VERA.md` | §6 (verdict format, head L225) | `attach_status` (L254) + `attach_failure` (L255) | dispatch-return-only addendum + frozen-body sentence (verbatim §2.1b/c) | bw-comment sentence (L268) → §2.1(d) verbatim replacement |
| `substrate/CAPTAIN_ARGUS.md` | §7 (verdict format, head L217) | `attach_status` (L237) + `attach_failure` (L238) | dispatch-return-only addendum + frozen-body sentence (verbatim §2.1b/c) | bw-comment sentence (L249) → §2.1(d) verbatim replacement |
| `substrate/CAPTAIN_CATO.md` | §7 (verdict format, head L180) | `attach_status` (L200) + `attach_failure` (L201) | dispatch-return-only addendum + frozen-body sentence (verbatim §2.1b/c) | bw-comment sentence (L214) → §2.1(d) verbatim replacement |
| `substrate/modules/save-verdict.md` | clause (d) (L95–127) | — | DC2(a) reinforcement sentence + DC4 invariant note (§2.2a, §2.4) | DC2(b): P8→manual-diff at L31 + L147 (§2.2b verbatim) |

**Scope fences for ADA:**
- Edit ONLY the live `substrate/CAPTAIN_{VERA,ARGUS,CATO}.md` and `substrate/modules/save-verdict.md`. Do NOT touch `substrate/v1-historical/CAPTAIN_*.md` (an archived copy — out of scope, never deployed).
- Line numbers above are from this Phase-A read; they will shift as edits land. ADA anchors on the field text / sentence text, not the raw line number.
- The byte-aligned region (between the sentinels) is NOT edited.

---

## 3. Verification probes

These are concrete, re-executable. Run from the worktree root `C:/Users/denso/claude_projects/the-stoa/.claude/worktrees/arc-74-build`.

- **P1 (DC4 demonstration — the sos--yn2 divergence cannot recur):** Author a throwaway verdict under the NEW format (attested body excludes `attach_status`), `printf`-write it, sha256 it, then simulate the in-tree commit and compare. Concretely: build a sample `<verdict-body>` with NO `attach_status`/`attach_failure`; `printf '%s' "$BODY" > <fixed literal worktree path>`; `A=$(printf '%s' "$BODY" | sha256sum)`; `B=$(sha256sum <file>)`; assert `A == B` AND that appending an `attach_status: OK` line (the OLD bug) changes the sha (proving the field WAS the divergence). Expected: pre-fix-style append diverges; new-format body's committed == attested. **NOTE for VERA:** use a FIXED LITERAL path under the worktree (`agents/verdicts/_probe-stoa--x5t/sample.md`), NOT a `$VAR`-expanded destructive path, per op-disc §8.6 — and clean it up with a literal `rm agents/verdicts/_probe-stoa--x5t/sample.md` (literal path, no expansion).

- **P2 (DC1 field-removal, all 3 — CORRECTED to the three-site expected-survivor set):** `grep -n 'attach_status' substrate/CAPTAIN_VERA.md substrate/CAPTAIN_ARGUS.md substrate/CAPTAIN_CATO.md`. Post-fix, `attach_status` legitimately survives at exactly **THREE sites per role file** — VERA must NOT route back on any of these three. The load-bearing assertion is the NEGATIVE one: zero occurrences of `attach_status`/`attach_failure` **between the verdict-format ```` ``` ```` fences** (the block that feeds `<verdict-body>`). The three legitimate survivors, with their (pre-edit) role-file locators:
  - **(a) the new dispatch-return-only addendum** (added by §2.1b) — a NEW site, outside the verdict-format fenced block, labeled "Dispatch-return-only addendum (emitted AFTER the §7 `bw attach` …)". Carries `attach_status` + `attach_failure` as its two relocated fields.
  - **(b) the §7 byte-aligned region's `attach_rc`-capture COMMENT** — INSIDE the UNTOUCHED 494b442e region: VERA L306–310, ARGUS L287–291, CATO L252–256 ("…the seat SETS the dispatch-return `attach_status` field from the ACTUAL rc…"). This is a comment string, not a body field; it stays verbatim (DC3 region untouched).
  - **(c) the post-region attach-failure-posture PROSE paragraph** — AFTER the region `END` sentinel: VERA L318, ARGUS L299, CATO L264 ("…emit a structured first-class `attach_status: FAILED` field in your dispatch return … on success emit `attach_status: OK`…"). This is the durability-posture prose; it stays.
  - Expected: `grep` returns occurrences ONLY at (a)/(b)/(c) per file; ZERO occurrences inside the verdict-format fenced block. A surviving occurrence at (a), (b), or (c) is NOT a finding and MUST NOT route back.

- **P3 (DC1 parallelism — automatic route-back if non-empty):** extract from each of the three files: (i) the new addendum label, (ii) the frozen-body sentence, (iii) the two relocated field lines (the addendum's fenced block), and (iv) the FULL bw-comment replacement sentence (§2.1d). `diff` each pairwise across VERA/ARGUS/CATO. Expected: byte-identical across all three (Q2 fold tightens this to the full bw-comment sentence, not just a load-bearing clause).

- **P4 (DC3 region UNTOUCHED — load-bearing):** run the §2.3 four-home `diff` (Form 1) AND the Form-2 sha loop. Expected: all three `diff`s empty; all four sha lines identical AND equal to the pre-fix baseline `494b442ea512949906134c4318786acf7ad6f63785fef19e6afee8bc6d2842cb`.

- **P5 (DC2 reinforcement + P8 repair present, contract intact):** `grep` `save-verdict.md` for the new frozen-body / invariant sentences (DC2a + DC4) and confirm clause (d)'s existing durability contract + exit-code map + attach-failure posture text is unchanged (only additive). PLUS the DC2(b) assertion: `grep -c 'P8' substrate/modules/save-verdict.md substrate/CAPTAIN_VERA.md substrate/CAPTAIN_ARGUS.md substrate/CAPTAIN_CATO.md` MUST be 0 for every file (both P8 occurrences corrected; no P8 introduced elsewhere), and the L31/L147 corrected wording (§2.2b) is present. Expected: additions present; no deletion of contract prose; zero "P8" strings across the four files.

- **P6 (full-suite regression bar — gen-data + vitest):** `npm run gen-data` twice and confirm deterministic (no diff between runs), then the FULL app test suite green (`npm test` / vitest). Editing role files re-derives the whole roster — run the full suite, NOT a narrow "we edited no schema" claim (per the gen-data-regen + full-suite-verify disciplines). Expected: gen-data deterministic, full suite green, author-gate + stop-hook + any verdict-format/corpus tests green.

- **P7 (no scope leak):** `git diff --stat` against the arc base — the changed-file set MUST be exactly the 3 reviewer role files + `save-verdict.md` (+ this design doc + verdict artifacts). Expected: no other substrate file touched; `v1-historical/` untouched.

**Threat-anchored probe:** NOT APPLICABLE — this arc is `not threat-ratified` (DC5 / §35.5 carve-out: process/role-file hardening, no runtime attacker, no attack path; ARGUS CONCURRED). No A3 map, so no threat-anchored probe is required (§6.13 self-carve-out).

---

## 4. Self-assessed weak points

- **Weak point — P2 is a three-site grep whose "legitimate survivor" set is locator-anchored to line numbers that shift as DC1 edits land.** *Why this shape anyway:* I anchored each of the three sites on stable TEXT ("the seat SETS the dispatch-return `attach_status` field" for site (b); "on success emit `attach_status: OK`" for site (c); the verbatim addendum label for site (a)), not the raw line number — the line numbers are Phase-A snapshots given as a reading aid. The load-bearing assertion is the NEGATIVE one (zero `attach_status` inside the verdict-format fences), which is unambiguous; the three positive survivors are an explicit allow-list so VERA does not false-route-back. P3 + P4 independently re-confirm sites (a) and (b) respectively.
- **Weak point — DC2(b) repairs the "P8" string at two sites, but a future doc-coherence audit could surface other stale "automated gate" phrasings not literally containing "P8".** *Why this shape anyway:* P5's `grep -c 'P8'` proves the literal string is gone; the directive + charter scope DC2(b) to the stale P8-gate claim specifically, and a broader "find every conceivable stale automated-gate phrasing" sweep would expand scope beyond the arc. The two L31/L147 sites are the only ones that assert an automated gate exists; the §7 inline prose already says "do NOT alter it in one home without re-aligning all four" (a manual instruction, not an automated-gate claim) so it needs no change.
- **Weak point — DC4 ships a documented invariant + a per-arc probe, not a standing mechanical gate.** *Why this shape anyway:* DC1 removes the defect structurally (committed==attested holds by construction), so a standing guard defends against re-introduction of a now-structurally-prevented defect — low marginal value, and the directive explicitly warns against bolting a check into the byte-aligned region. The heavier NOMOS-on-merge assertion is the right home IF in-tree verdict tracking becomes universal; deferred as a named follow-up, not silently dropped. ARGUS CONFIRMED this call.
- **Weak point — the addendum's physical placement ("after the block, read as emitted after §7 attach") is described in prose, not pinned to an exact insertion line.** *Why this shape anyway:* the three files have slightly different section tails (definitions, threat-coverage notes, canonical-save-path prose); a single hard line-anchor would not fit all three. ARGUS ruled the semantic anchor SUFFICIENT (Q3). The semantic anchor ("immediately after the verdict-format block and its definitions/notes, before the §7 canonical-save-path prose, labeled as a post-attach emission") plus the verbatim label is precise enough for mechanical execution while fitting all three layouts. P3's parallelism diff catches any drift.

No new weak point is introduced by the three folds. The Q2 fold actually *removes* a weak point rev1 carried (the bw-comment trailing-parenthetical non-parallelism / rev1 weak-point-1) — the post-fix sentence is now fully byte-identical, and on-disk the three current sentences were already identical, so the fold is a clean verbatim replacement with no asymmetry to reconcile.

---

## 5. Out of scope

- The §7 `printf → sha → attach` bash semantics, the durability contract, the exit-code map, and the dispatch-return `attach_status` FIELD itself — all preserved unchanged (the field stays; only its HOME moves out of the attested body). [Directive "Out of scope".]
- `sos--77g` (AST read-only-guard hardening) — a different stoa_of_science follow-up.
- The redeploy/propagation step (the-stoa `.claude/` self-apply + re-running `install.sh` into stoa_of_science) — user-tier post-merge sequence, NOT a build deliverable.
- Any change to verdict CONTENT / probe semantics, or to role files beyond the 3 reviewers + `save-verdict.md`.
- **DC4-followup (named, not built):** a NOMOS-on-merge `git cat-file`-vs-`bw attach`-blob equality assertion, IF in-tree verdict tracking becomes the default across arcs. Documented invariant + per-arc probe suffices for this arc.
- Broader stale-"automated-gate" phrasing audit beyond the two literal "P8" sites — DC2(b) is scoped to the stale P8-gate claim (the only "automated gate exists" assertion in the file); a wider doc-coherence sweep is out of scope.
- `substrate/v1-historical/CAPTAIN_*.md` — archived copies, never deployed; explicitly out of ADA's edit set.

---

## 6. DC disposition summary

| DC | Disposition (rev2) |
|---|---|
| **DC1** | Split the conflated verdict-format block: remove `attach_status`/`attach_failure` from the attested-body fenced block in VERA §6 / ARGUS §7 / CATO §7; add a verbatim dispatch-return-only addendum + verbatim frozen-body sentence (parallel across all three); replace the bw-comment instruction with a single FULL byte-identical sentence pointing at the attested body, not "the same block" (Q2 fold). |
| **DC2** | `save-verdict.md` clause (d) reinforcement (DC2a, additive — body frozen, attached copy byte-canonical, dispatch-return-only fields; durability contract preserved) **PLUS committed P8→manual-diff doc-coherence repair at L31 + L147 (DC2b, Q1 ruled IN SCOPE — no longer gated).** |
| **DC3** | Byte-aligned region **UNTOUCHED** (region never wrote `attach_status` as a body field; fix is prose-only, outside the sentinels). Baseline sha `494b442e…` across all four homes (re-measured by ARGUS + floor-manager); verifier runs the explicit four-home `diff` (Form 1) + sha-equality loop (Form 2) to confirm. |
| **DC4** | Documented invariant in `save-verdict.md` + per-arc demonstration probe (P1). NO new mechanical gate, NO check in the byte-aligned region. NOMOS-on-merge assertion deferred as a named follow-up. ARGUS CONFIRMED. |
| **DC5** | `not threat-ratified` (process/canon hygiene; no runtime attacker, no attack path; §35.5 carve-out; ARGUS CONCURRED). Fix makes committed-sha == attested-sha hold for in-tree-tracked verdicts going forward; does NOT change the durability contract, attach-failure posture, exit-code map, or the dispatch-return `attach_status` field itself. No threat-anchored probe required. |

---

## 7. Residual questions for ARGUS

None. ARGUS's PASS (rev1) ruled all three rev1 residual questions:
- Q1 (DC2b P8→manual-diff scope) → IN SCOPE; folded as committed DC2(b) (§2.2b). Resolved.
- Q2 (bw-comment full-sentence parallelism) → full byte-identity adopted; folded (§2.1d). Resolved (and the on-disk premise corrected: the three current sentences were already identical).
- Q3 (addendum placement) → semantic anchor SUFFICIENT. Carried as designed.

No new question is opened by the folds.
