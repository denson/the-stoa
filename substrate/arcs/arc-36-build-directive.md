# Arc 36 build directive — explicit `[from: <self>]` author-tag canon for POLYBIUS-on-POLYBIUS bw coordination (stoa--e39)

**Status:** LOCKED at dispatch authoring (2026-05-17). A1-A14 are not DAEDALUS-revisable; sub-decisions inside A5/A6/A7/A8 are DAEDALUS discretion unless surfaced as PRINCIPAL-gate per `operating-disciplines.md` §25.

**Work-unit:** `stoa--e39` (P2, filed 2026-05-04 after project-tier POLYBIUS_the_stoa misread user-tier POLYBIUS's `[for: POLYBIUS_the_stoa]` comment as its own self-heartbeat during the arc-21 §5.4 review handoff — symptom: ~25-min coordination stall; root cause: timestamp-only parsing without robust author-attribution).

## Scope-recut from arc-22 (audit-before-dispatch, 2026-05-17)

User-tier POLYBIUS audit-against-current-substrate (per PRINCIPAL morning sequencing 2026-05-17) surfaced that the original arc-22 / stoa--jru EPIC bundled two failure modes — (1) bw-timeline parsing brittleness via author tags [stoa--e39]; (2) CronCreate 7-day expiry handling [stoa--cgn] — and that since 2026-05-04 (when both were surfaced) the substrate has shipped 10 arcs (Arcs 26-35) without either failure mode recurring empirically. The substrate adapted informally: POLYBIUS comments in Arcs 32-35 routinely use `[radio-check <self-seat>]` and `[for: <upper-tier-seat>]` patterns; the missing canon piece is the `[from: <self>]` half of the addressed-comment pair.

**PRINCIPAL adjudication (2026-05-17):** ship Part 1 (author tags / e39) as Arc 36 because it has informal-adoption signal — canon-locking it codifies what's already working. Defer Part 2 (cron expiry / cgn) to a separate ticket gated on empirical recurrence OR a planned multi-day engagement. Close stoa--jru as scope-recut.

The arc-22 directive at `arcs/22-coordination-hygiene` branch is reference material for Part 1's architecture (A1-A2.5 lock decisions in that directive ARE the architecture this arc ships). DAEDALUS treats arc-22 directive Part 1 as primary architectural input; integration surface refreshed against current substrate (Arcs 23-35 shifted §7 sub-section structure, added §7.4 bidirectional `[for:]` informally, etc.).

## A1 — One arc, one gauntlet (LOCKED)

Arc 36 ships as a single end-to-end gauntlet (DAEDALUS → ARGUS → ADA → VERA → CATO → ZENO → PLINY signoff → PR merge). No sub-arc decomposition. Mirrors Arcs 27-35.

## A2 — Convention: explicit `[from: <self-seat-slug>]` on POLYBIUS coordination comments (LOCKED from arc-22 A2)

Every POLYBIUS bw comment posted as part of coordination prefixes the body with an author tag. Three forms cover the cases:

- **Self-heartbeat:** `[radio-check <self-seat-slug>]` — already established convention; Arc 36 does not change this form.
- **Cross-seat addressed:** `[for: <recipient-seat-slug>] [from: <sender-seat-slug>]` — both tags mandatory.
- **Own-bw substantive (not addressed to a peer):** `[from: <self-seat-slug>]` — for status updates, gauntlet phase comments, decisions logged in own bw without a specific recipient.

**`[from:]` is NEW canon.** No prior convention requires sender-tag. The reason: a peer reading the timeline can match `[for: <self>]` to "addressed to me" but cannot reliably distinguish "from peer" from "from self" without comparing the timestamp against the seat's own activity log — exactly the inference step that failed in the stoa--e39 empirical. `[from: <self>]` makes attribution explicit at the data layer.

`[for:]` is promoted from cross-tier-upward-only (current §7.4) to bidirectional ("addressed comment by sender to recipient" — either direction across the POLYBIUS pair). The directive owns this expansion; current §7.4 wording is updated to reflect.

## A2.5 — Convention scope: POLYBIUS-on-POLYBIUS coordination only (LOCKED from arc-22 A2.5)

The author-tag convention applies to POLYBIUS instances only (user-tier POLYBIUS, project-tier POLYBIUS, sub-project POLYBIUS). PLINY, CAPTAINs, and pair-programmer Majors are NOT required to author-tag their bw comments in Arc 36.

Justification: peer-silence threshold and self-heartbeat-due timing computations consume `last_self_activity` / `last_peer_activity` timestamps where "self" and "peer" are POLYBIUS instances. Comments by PLINY (gauntlet phase status), CAPTAINs (verdicts, surfaced ambiguities), or pair-programmer Majors do NOT count toward those timestamps — they are SUBSTANCE comments, not coordination-attribution comments. The polling-cron parser correctly classifies them as "non-POLYBIUS, low-confidence attribution" and they do not perturb the timeline computations that the e39 fix targets.

A future arc MAY extend the convention to PLINY/CAPTAIN authoring; that is a deliberate scope expansion, not silently in Arc 36's scope.

## A3 — Slug normalization (LOCKED from arc-22 A2)

Slugs in tags are lowercase, hyphenated, no whitespace: `user-tier-polybius`, `polybius-the-stoa`, `polybius-ariadne-core`. The slug matches the role-file slug used by autonomous-mode-activation-template (arc-21 §B.2).

Display-form strings (`user-tier POLYBIUS`, `POLYBIUS_the_stoa`) continue to appear in prose / heartbeat messages for human-readable framing. Tags use the slug for machine-parseable attribution.

Legacy/untagged comments (pre-Arc 36 history) fall to the parser's low-confidence fallback (see A4).

## A4 — Parsing teaching: universal-team layer in operating-disciplines.md (LOCKED from arc-22 A3)

The canonical text for "how to parse bw timeline by author" lives in `operating-disciplines.md` §7 (universal-team layer — any seat reading a bw comment timeline needs the same parsing discipline). `MAJOR_POLYBIUS.md` §7 cross-refs back. The parsing teaching encodes:

1. **POLYBIUS-tagged comments** (`[radio-check <slug>]`, `[for: <slug>] [from: <slug>]`, `[from: <slug>]`) attribute by tag — high confidence.
2. **Untagged comments** fall to author-context-inference — low confidence. Inference shape: "is this comment one I posted? check own activity log / phase-transition records; if not, treat as peer activity but flag as low-confidence."
3. **Non-POLYBIUS comments** (PLINY phase status, CAPTAIN verdicts, pair-programmer outputs) per A2.5 are SUBSTANCE comments — they do not enter the `last_self_activity` / `last_peer_activity` timeline-arithmetic that the parser uses for radio-check / heartbeat thresholds.
4. **Self-misattribution guard.** Never assume the most recent comment is "yours" by timestamp proximity. Always verify by tag OR by own-activity-log comparison.

## A5 — Insertion locus (DAEDALUS sub-decision)

The parsing teaching lands in `substrate/operating-disciplines.md` §7. DAEDALUS picks the precise section number / heading. Two credible shapes:

- **(α) New §7.7** "bw-timeline parsing: author-attribution via tags" — own subsection inside the existing "Coordinating two POLYBIUS seats async via bw polling" section (§7). Cleanest separation; parallel to existing §7.1-§7.6 numbering.
- **(β) Extend §7.1 "Radio-check protocol"** with an author-tag subsection — closer integration with existing radio-check + heartbeat machinery (which the parsing supports). Less new structure; more dense existing section.

The `[from:]` convention itself (A2) lands in §7.1 or as a body extension on §7.4 (bidirectional `[for:]` update). DAEDALUS picks the exact insertion (current §7.4 wording explicitly says "cross-tier UPWARD requests only" — Arc 36 promotes to bidirectional + adds `[from:]`).

DAEDALUS lean: (α) new §7.7 for the parsing teaching (clean separation; precedent of Arc 33's §27 and Arc 35's §28 as new top-level numbered subsections); §7.4 wording update inline for `[for:]` bidirectional + `[from:]` introduction. Document in `design.md`.

## A6 — `MAJOR_POLYBIUS.md` §7 cross-ref (DAEDALUS sub-decision)

`substrate/MAJOR_POLYBIUS.md` §7 (POLYBIUS-tier-specific bw-handling) needs a cross-ref to the new universal-team parsing canon. DAEDALUS picks: small body paragraph cite-comment to operating-disciplines.md §7.7 (or wherever A5 lands), OR a new §7.5 subsection naming the discipline POLYBIUS-tier-specifically. User-tier POLYBIUS leans body paragraph cite-comment (smaller surface; cite-pattern matches Arcs 26-35).

## A7 — `polling-cron-prompt-template.md` parsing step (DAEDALUS sub-decision)

The current `substrate/templates/polling-cron-prompt-template.md` (161 lines) embeds the polling cron's fire-loop body. If DAEDALUS deems the author-attribution step needs to be MECHANICALLY EXECUTED by the cron parser (not just documented in §7.7 prose), insert a STEP 1.5 between current STEP 1 (substantive read) and STEP 2 (current state) explicitly:

- Read each new comment since last fire.
- Parse for `[from: <slug>]` / `[for: <slug>] [from: <slug>]` / `[radio-check <slug>]` tags.
- Attribute each tagged comment to its slug.
- For untagged comments: cross-reference against own self-posted comments via activity log; flag as low-confidence.
- Use only POLYBIUS-attributed comments in the `last_self_activity` / `last_peer_activity` arithmetic.

DAEDALUS picks whether template STEP 1.5 is required (parser executes the discipline) OR optional (prose canon in §7.7 is sufficient; cron parser uses common-sense reading). User-tier POLYBIUS leans STEP 1.5 mandatory — the parser ran into the e39 failure mode precisely because it was doing common-sense reading without mechanical author-attribution.

If STEP 1.5 ships, the template's substitution-slot table grows by `{{SELF_SEAT_SLUG}}` + `{{PEER_SEAT_SLUG}}` per arc-22 A2 slug-form requirement.

## A8 — Self-application (LOCKED)

**Arc 36's own coordination comments must apply the convention.** Project-tier POLYBIUS_the_stoa's bw comments on `stoa--e39` (the work-unit) during this arc carry `[from: polybius-the-stoa]` tags per the convention being shipped. Cross-tier comments addressed to user-tier POLYBIUS use `[for: user-tier-polybius] [from: polybius-the-stoa]`. The arc that ships the convention IS the first worked example of it.

Same self-apply pattern as Arc 35 (per-CAPTAIN trailers on Arc 35's own commits), Arc 34 / C2 (paste-archival in same gauntlet commit), Arc 33 (skill in same arc that defines pattern), Arc 29 (custom/ dir used by arc that defines it).

PLINY signoff verifies that Arc 36's own coordination heartbeats on stoa--e39 carry the `[from:]` tag per §7.1 / §7.4 / §7.7 before PR-merging. If POLYBIUS_the_stoa's first heartbeat forgets the tag, surface as substance disagreement and have POLYBIUS rewrite-with-correction — do NOT let an un-self-applied convention ship.

## A9 — Cite-comment discipline (LOCKED)

Cross-references between operating-disciplines.md §7.1 / §7.4 / §7.7 + MAJOR_POLYBIUS.md §7 cross-ref + polling-cron-prompt-template.md STEP 1.5 (if shipped) resolve via cite at every read-site. Same pattern as Arcs 26 / 28 / 29 / 30 / 31 / 32 / 33 / 34 / 35 cite-comments.

## A10 — Authorship attribution unchanged (LOCKED)

File-frontmatter `author:` fields remain Denson Smith per CLAUDE.md IMMUTABLE rule. Git commit `Author:` remains PRINCIPAL per ~/.claude/CLAUDE.md. Arc 35's Co-Authored-By trailer convention applies to CAPTAIN commits in arc-36/build per §28 — verify ADA + DAEDALUS commits carry seat trailers.

## A11 — Out-of-scope (HARD-LOCKED)

Arc 36 does NOT:

- Extend the convention to non-POLYBIUS seats (PLINY, CAPTAINs, pair-programmer Majors) — A2.5 hard-lock; future arc may extend with explicit scope expansion.
- Address cron-expiry handling (stoa--cgn) — deferred to a separate ticket gated on empirical recurrence OR planned multi-day engagement.
- Modify the radio-check `[radio-check <slug>]` form — that form is already established.
- Retroactively tag past untagged comments — Arc 36 is forward-only; the parser's low-confidence fallback covers legacy history.
- Build a new cron-renewal mechanism, watcher cron, or scheduled-renewal chain — explicitly out of scope per the Arc 22 → Arc 36 scope-recut.
- Touch substrate/install.sh beyond what A7 STEP 1.5 + slot-table extension may require.
- Build mechanical parser enforcement (e.g., a pre-comment hook that rejects un-tagged POLYBIUS comments) — Arc 36 ships prose canon + parser-step template; mechanical enforcement is a future arc following Arc 33's mechanical/agent-split pattern if non-compliance recurs.

If DAEDALUS or any CAPTAIN surfaces a scope concern touching A11, treat as substance disagreement: confirm A11 wording, file follow-up ticket if the concern has merit, do NOT expand this arc.

## A12 — §15 N=1 honesty per the empirical anchor (LOCKED)

Per `MAJOR_POLYBIUS.md` §15 + `operating-disciplines.md` §6.7.1: the author-tag convention enters substrate canon off-gate on the original empirical signal (stoa--e39 misread, 2026-05-04, ~25-min stall) plus the informal-adoption signal from Arcs 32-35 (project-tier POLYBIUS routinely uses `[radio-check <self>]` + `[for: <upper>]`). N=1 bit-by-it (the original misread); N=4-bit-by-it of informal-partial-adoption (the `[radio-check ...]` heartbeats in Arcs 32/33/34/35 — `[from:]` half missing but the pattern is in use); N=0 worked-when-applied with full canon (Arc 36's self-application is the first observation under formal §7.7).

Future-evidence accretion per §6.7.1 — promotion to "structural lesson" status accretes as future arcs ship under §7.7 and surface either successful application or fresh failure modes. Same N=1 framing as Arc 27's §16.6, Arc 28's §22.3, Arc 29's §17.5, Arc 30's §5.9.3, Arc 31's §25.6, Arc 32's §5.9.4, Arc 33's §27, Arc 34's §18 + §5.11 + §9-step-3, Arc 35's §28.

## A13 — Pre-branch + worktree convention self-applied (LOCKED)

Per MAJOR_PLINY.md §5.9 + §5.9.4. PLINY runs the two-check rule before creating `arc-36/build`; builds in `.claude/worktrees/arc-36-build/` (NOT in main worktree). User-tier POLYBIUS confirmed at dispatch authoring: local main = origin/main at `6414397`; no orphan arc-build branches.

## A14 — Signoff-accuracy + attestation-honesty + source-ticket closure (LOCKED)

Per MAJOR_PLINY.md §5.10 + operating-disciplines.md §19.6. PLINY signoff live-verifies cleanup (arc-36/build local + remote deleted; worktree removed; PR merged) AND self-application (POLYBIUS_the_stoa's heartbeats carry `[from:]` per the shipped convention). Attestations cite live-verified state.

**On Arc 36 ship:**
- Close `stoa--e39` (work-unit) with cross-ref to merge commit + audit comment.
- Close `stoa--jru` (Arc 22 EPIC parent) with cross-ref to merge commit + scope-recut audit note: "Part 1 shipped via stoa--e39 as Arc 36; Part 2 (cron expiry / stoa--cgn) deferred with gating criteria per 2026-05-17 PRINCIPAL adjudication."
- Update `stoa--cgn` body via comment with deferral gating criteria (do NOT close — keep open as gated future work).

Tag `[for: user-tier-polybius]` on stoa--e39 inviting QA pass.

## Phase structure

**Phase 1 — Design (DAEDALUS + ARGUS).** DAEDALUS reads this directive + stoa--e39 + arc-22 build directive Part 1 (reference; not primary input) + current operating-disciplines.md §7 entire section + MAJOR_POLYBIUS.md §7 + polling-cron-prompt-template.md + Arc 35 §28 (most recent new-section precedent) + Arc 33 §27 (precedent for prose-canon-without-mechanical-enforcement). Produces design.md covering A5/A6/A7 picks, exact wording for §7.7 + §7.4 update + §7.1 update, MAJOR_POLYBIUS.md §7 cross-ref, polling-cron-prompt-template.md STEP 1.5 (if shipped), self-application plan for A8. ARGUS cold-audits.

**Phase 2 — Build (ADA in `.claude/worktrees/arc-36-build/`).** ADA implements per approved design.md. ADA's commits carry Co-Authored-By trailers per §28 (Arc 35 canon). Self-applies: project-tier POLYBIUS_the_stoa's heartbeats on stoa--e39 during the arc carry `[from: polybius-the-stoa]` per the convention being shipped.

**Phase 3 — Verify (VERA + CATO + ZENO).** VERA exercises probes from design.md (does §7.7 land at expected line range? does §7.4 wording promote `[for:]` to bidirectional? does the polling-cron-prompt-template STEP 1.5 read correctly? does a worked-example heartbeat carry the `[from:]` tag per the convention?). CATO cold-reads the diff for craft + scope + wording. ZENO mechanical spec-vs-result.

**Phase 4 — Ship + close.** Smoke + PR + merge + cleanup + close. PLINY signoff per §5.10 live-verifies. Close stoa--e39 + stoa--jru per A14; comment-update stoa--cgn with deferral gating.

## DAEDALUS sub-decisions summary

- **A5** — insertion locus in operating-disciplines.md (new §7.7 vs extend §7.1; §7.4 bidirectional update inline)
- **A6** — MAJOR_POLYBIUS.md §7 cross-ref shape (body paragraph cite vs new §7.5 subsection)
- **A7** — polling-cron-prompt-template.md STEP 1.5 (mandatory vs optional)

User-tier POLYBIUS leans: A5 (α) new §7.7 + inline §7.4 update; A6 body-paragraph cite; A7 STEP 1.5 mandatory.

If any pick exceeds DAEDALUS discretion, treat as PRINCIPAL-gate per §25 — halt + escalate immediately rather than proceed-then-flag.

## Read order for DAEDALUS

1. This directive (load-bearing spec).
2. `bw show stoa--e39` (work-unit; carries 2026-05-04 empirical anchor + original "what needs to change in substrate" enumeration).
3. `bw show stoa--jru` (parent EPIC being closed as scope-recut; carries the bundling history + audit framing for why Arc 36 ships Part 1 only).
4. `bw show stoa--cgn` (sibling being deferred; reference for what's NOT in Arc 36 scope per A11).
5. `git show arcs/22-coordination-hygiene:substrate/arcs/arc-22-build-directive.md` Part 1 (architectural reference for A2/A2.5/A3/A4 — these locks are inherited from arc-22's Part 1; integration surface refreshed).
6. `substrate/operating-disciplines.md` §7 entire section (current §7.1-§7.6; A5/A4 insertion surface).
7. `substrate/MAJOR_POLYBIUS.md` §7 (A6 cross-ref target).
8. `substrate/templates/polling-cron-prompt-template.md` (A7 insertion surface; 161 lines).
9. `substrate/operating-disciplines.md` §27 (Arc 33 mechanical/agent split — precedent for "ship prose canon now; defer mechanical enforcement to future arc if non-compliance recurs"; A11 hard-lock cites this).
10. `substrate/operating-disciplines.md` §28 (Arc 35 most recent new top-level section precedent; A5 (α) follows same shape).
11. `substrate/arcs/arc-35-build-directive.md` (most recent dispatch precedent; self-application pattern reference for A8).
