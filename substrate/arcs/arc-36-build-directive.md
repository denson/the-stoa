# Arc 36 v2 build directive — Coordination hygiene (author tags + cron expiry) — bundled, no deferral (stoa--e39 + stoa--cgn)

**Status:** LOCKED at v2 dispatch authoring (2026-05-17). A1-A17 are not DAEDALUS-revisable; sub-decisions inside A5/A6/A7/A8/A10 are DAEDALUS discretion unless surfaced as PRINCIPAL-gate per `operating-disciplines.md` §25.

**Work-unit:** `stoa--jru` (parent EPIC; closes on ship). **Child tickets:** `stoa--e39` (Part 1, author tags) + `stoa--cgn` (Part 2, cron expiry). Both close on ship per A15.

**v2 revision context (2026-05-17):** the v1 of this directive (commit `28155f7`) scope-recut arc-22 to Part-1-only (e39 author tags) with cgn deferred under gating criteria. PRINCIPAL pre-dispatch reversed that scope-recut under the no-deferrals stance ("I don't want to defer shit or gloss over technical debt. I want a plan to get everything fixed"). v2 restores the original arc-22 bundling: Part 1 + Part 2 ship together. The original arc-22 directive on the `arcs/22-coordination-hygiene` branch carries the architectural decisions for both Parts (LOCKED at arc-22 authoring 2026-05-04 + reviewed by CAPTAIN_ARGUS at the time); v2 of this directive inherits those locks + refreshes the integration surface against current substrate (Arcs 23-35 shifted §7 sub-section structure, added §7.4 informal-bidirectional `[for:]` use, added §28 Co-Authored-By trailer canon, etc.).

---

## A1 — One arc, one gauntlet (LOCKED)

Arc 36 ships as a single end-to-end gauntlet (DAEDALUS → ARGUS → ADA → VERA → CATO → ZENO → PLINY signoff → PR merge). Both Parts ship together. Mirrors Arcs 27-35.

The arc-22 original directive estimated "small arc: 2 Parts × 2 Phases × ~8 deliverables." That estimate was authored 2026-05-04 against the then-substrate; current substrate has more integration surface, so realistic v2 estimate is "small-to-medium arc, ~8-12 deliverables across both Parts." Still single gauntlet.

---

# PART 1 — `[from: <self-seat-slug>]` author-tag canon (stoa--e39)

Inherited architecture from arc-22 directive A2 + A2.5 + A3 (Part 1). Integration surface refreshed.

## A2 — Convention: explicit `[from:]` on POLYBIUS coordination comments (LOCKED from arc-22 A2)

Every POLYBIUS bw comment posted as part of coordination prefixes the body with an author tag. Three forms cover the cases:

- **Self-heartbeat:** `[radio-check <self-seat-slug>]` — already established convention; v2 does not change this form.
- **Cross-seat addressed:** `[for: <recipient-seat-slug>] [from: <sender-seat-slug>]` — both tags mandatory.
- **Own-bw substantive (not addressed to a peer):** `[from: <self-seat-slug>]` — for status updates, gauntlet phase comments, decisions logged in own bw without a specific recipient.

**`[from:]` is NEW canon.** No prior convention requires sender-tag. The reason: a peer reading the timeline can match `[for: <self>]` to "addressed to me" but cannot reliably distinguish "from peer" from "from self" without comparing the timestamp against the seat's own activity log — exactly the inference step that failed in the stoa--e39 empirical (2026-05-04, ~25-min coordination stall during arc-21 §5.4 review handoff). `[from: <self>]` makes attribution explicit at the data layer.

`[for:]` is promoted from cross-tier-upward-only (current `operating-disciplines.md` §7.4) to bidirectional ("addressed comment by sender to recipient" — either direction across the POLYBIUS pair). The directive owns this expansion; current §7.4 wording is updated to reflect.

## A2.5 — Convention scope: POLYBIUS-on-POLYBIUS coordination only (LOCKED from arc-22 A2.5)

The author-tag convention applies to POLYBIUS instances only (user-tier POLYBIUS, project-tier POLYBIUS, sub-project POLYBIUS). PLINY, CAPTAINs, and pair-programmer Majors are NOT required to author-tag their bw comments in Arc 36.

Justification: peer-silence threshold and self-heartbeat-due timing computations consume `last_self_activity` / `last_peer_activity` timestamps where "self" and "peer" are POLYBIUS instances. Comments by PLINY (gauntlet phase status), CAPTAINs (verdicts, surfaced ambiguities), or pair-programmer Majors do NOT count toward those timestamps — they are SUBSTANCE comments, not coordination-attribution comments. The polling-cron parser correctly classifies them as "non-POLYBIUS, low-confidence attribution" and they do not perturb the timeline computations that the e39 fix targets.

A future arc MAY extend the convention to PLINY/CAPTAIN authoring; that is a deliberate scope expansion, not silently in Arc 36's scope.

## A3 — Slug normalization (LOCKED from arc-22 A2 normalization clause)

Slugs in tags are lowercase, hyphenated, no whitespace: `user-tier-polybius`, `polybius-the-stoa`, `polybius-ariadne-core`. The slug matches the role-file slug used by autonomous-mode-activation-template (arc-21 §B.2 + Arc 35 §28 `<project-slug>` convention).

Display-form strings (`user-tier POLYBIUS`, `POLYBIUS_the_stoa`) continue to appear in prose / heartbeat messages for human-readable framing. Tags use the slug for machine-parseable attribution.

Legacy/untagged comments (pre-Arc 36 history) fall to the parser's low-confidence fallback (see A4).

## A4 — Parsing teaching: universal-team layer in operating-disciplines.md (LOCKED from arc-22 A3)

The canonical text for "how to parse bw timeline by author" lives in `substrate/operating-disciplines.md` §7 (universal-team layer — any seat reading a bw comment timeline needs the same parsing discipline). `substrate/MAJOR_POLYBIUS.md` §7 cross-refs back. The parsing teaching encodes:

1. **POLYBIUS-tagged comments** (`[radio-check <slug>]`, `[for: <slug>] [from: <slug>]`, `[from: <slug>]`) attribute by tag — high confidence.
2. **Untagged comments** fall to author-context-inference — low confidence. Inference shape: "is this comment one I posted? check own activity log / phase-transition records; if not, treat as peer activity but flag as low-confidence."
3. **Non-POLYBIUS comments** (PLINY phase status, CAPTAIN verdicts, pair-programmer outputs) per A2.5 are SUBSTANCE comments — they do not enter the `last_self_activity` / `last_peer_activity` timeline-arithmetic that the parser uses for radio-check / heartbeat thresholds.
4. **Self-misattribution guard.** Never assume the most recent comment is "yours" by timestamp proximity. Always verify by tag OR by own-activity-log comparison.

## A5 — Part 1 insertion locus (DAEDALUS sub-decision)

The parsing teaching lands in `substrate/operating-disciplines.md` §7. DAEDALUS picks the precise section number / heading. Two credible shapes:

- **(α) New §7.7** "bw-timeline parsing: author-attribution via tags" — own subsection inside the existing "Coordinating two POLYBIUS seats async via bw polling" section (§7). Cleanest separation; parallel to existing §7.1-§7.6 numbering.
- **(β) Extend §7.1 "Radio-check protocol"** with an author-tag subsection — closer integration with existing radio-check + heartbeat machinery (which the parsing supports). Less new structure; more dense existing section.

The `[from:]` convention itself (A2) lands in §7.1 or as a body extension on §7.4 (bidirectional `[for:]` update). DAEDALUS picks the exact insertion (current §7.4 wording explicitly says "cross-tier UPWARD requests only" — Arc 36 promotes to bidirectional + adds `[from:]`).

DAEDALUS lean: (α) new §7.7 for the parsing teaching (clean separation; precedent of Arc 33's §27 and Arc 35's §28 as new top-level numbered subsections); §7.4 wording update inline for `[for:]` bidirectional + `[from:]` introduction. Document in `design.md`.

The `MAJOR_POLYBIUS.md` §7 cross-ref shape is also DAEDALUS sub-decision: small body paragraph cite-comment vs new §7.5 subsection. User-tier POLYBIUS leans body paragraph cite-comment (smaller surface; cite-pattern matches Arcs 26-35).

## A6 — Part 1 polling-cron-prompt-template parsing step (DAEDALUS sub-decision)

The current `substrate/templates/polling-cron-prompt-template.md` (161 lines) embeds the polling cron's fire-loop body. If DAEDALUS deems the author-attribution step needs to be MECHANICALLY EXECUTED by the cron parser (not just documented in §7.7 prose), insert a STEP 1.5 between current STEP 1 (substantive read) and STEP 2 (current state) explicitly:

- Read each new comment since last fire.
- Parse for `[from: <slug>]` / `[for: <slug>] [from: <slug>]` / `[radio-check <slug>]` tags.
- Attribute each tagged comment to its slug.
- For untagged comments: cross-reference against own self-posted comments via activity log; flag as low-confidence.
- Use only POLYBIUS-attributed comments in the `last_self_activity` / `last_peer_activity` arithmetic.

DAEDALUS picks whether template STEP 1.5 is required (parser executes the discipline) OR optional (prose canon in §7.7 is sufficient; cron parser uses common-sense reading). User-tier POLYBIUS leans STEP 1.5 mandatory — the parser ran into the e39 failure mode precisely because it was doing common-sense reading without mechanical author-attribution.

If STEP 1.5 ships, the template's substitution-slot table grows by `{{SELF_SEAT_SLUG}}` + `{{PEER_SEAT_SLUG}}` per arc-22 A2 slug-form requirement.

---

# PART 2 — Cron-expiry handling (stoa--cgn)

Inherited architecture from arc-22 directive A4 + A5 + A6 (Part 2). Spike-first per A7.

## A7 — Spike-first decision matrix (LOCKED from arc-22 A4)

CronCreate has a documented expiry (arc-22 cited 7 days; current Claude Code docs may have resolved the 3-day-vs-7-day ambiguity that existed at arc-22 authoring). Multi-day autonomous engagements exceeding the expiry silently lose their polling cron; recovery is via peer-side radio-check after the > 60-min peer-silence threshold per arc-21 §C.1, but ~5-6 days of dead air pass first.

**Spike step (run before Part 2 design.md is finalized):**

1. Open a fresh REPL or use the dispatched session itself.
2. `CronCreate` a throwaway session-only cron with a long cadence (e.g., `0 0 * * *` daily) and a no-op prompt.
3. `CronList` and capture the FULL output structure for the new cron. Inspect every field: does it expose `start_time` / `created_at` / `age` (backward-looking) OR `expires_at` / `next_fire` / `valid_until` (forward-looking) OR neither? Does `CronUpdate` or equivalent in-place renewal primitive exist?
4. Search current Claude Code docs for the actual cron expiry duration. Record the empirically-confirmed expiry from whatever authoritative source you find. If docs are still ambiguous, file the ambiguity in design.md + use the SHORTER documented value (conservative).
5. `CronDelete` the throwaway.
6. Record the field list AND the confirmed expiry duration in design.md §Part-2-spike + in your bw comment on `stoa--jru`.

**Decision matrix (LOCKED, expanded with forward-looking row + CronUpdate row):**

| `CronList` exposes | Implementation | Where it lands |
|---|---|---|
| Backward-looking only (start-time / age / created-at) | Option 1 (in-fire check based on age threshold) | `substrate/templates/polling-cron-prompt-template.md` — new STEP 7 between STEP 6 and "End of fire-loop" |
| Forward-looking (expires-at / next-fire / valid-until) | Option 1 (in-fire check based on time-until-expiry — preferred; strictly simpler than backward-looking) | Same location as above; STEP 7 reads `expires_at - now < {{RENEWAL_BUFFER_HOURS}}` instead of `now - start_time > {{RENEWAL_THRESHOLD}}` |
| Both backward AND forward fields exposed | Option 1 with forward-looking comparison (preferred — avoids age-arithmetic fencepost errors) | Same |
| Neither (cron metadata fully opaque) | Option 3 (setup-time scheduled renewal) | `substrate/operating-disciplines.md` §11 — new step 1.5 ("schedule a one-shot renewal cron at +<expiry-1day>") |
| `CronUpdate` or equivalent in-place renewal primitive exists | Surface to user-tier POLYBIUS via `[for: user-tier-polybius] [from: polybius-the-stoa]` on `stoa--jru` | Decision routes through user-tier POLYBIUS; do not pick unilaterally — this is a strictly-better path that may justify scope adjustment |

Option 2 (separate watcher cron) is rejected up-front: adds an entirely new coordination dependency (the watcher's own expiry, polling cost, failure modes). Options 1 and 3 keep the renewal logic local to the engagement that owns the cron.

Genuinely-unexpected states (e.g., `CronList` returns no entries, fields are present but undocumented, the empirical expiry probe reveals inconsistency between docs and tool behavior) surface to user-tier POLYBIUS via `[for: user-tier-polybius] [from: polybius-the-stoa]` on `stoa--jru` — do not pick unilaterally.

## A8 — Renewal buffer rule: 1-day from expiry (LOCKED from arc-22 A5)

Renewal fires when **time-until-expiry < 1 day** (24 hours), regardless of whether the empirical expiry is 3 days or 7 days. Expressing the trigger as a buffer-from-expiry rather than an absolute "day 6" makes the rule correct under either docs reading.

The 1-day buffer absorbs:

- A renewal fire that itself hits an error (timeout, quota, transient API failure) — there is a full day to retry on the next fire.
- A POLYBIUS session offline for hours when the renewal would have fired (the renewal catches on the NEXT fire after the session resumes, still well inside the expiry window).
- Clock-skew / time-zone confusion in the cron service.

For a 3-day expiry, this means renewal at +2 days from creation (1-day buffer = 33% of lifetime — generous). For a 7-day expiry, renewal at +6 days (1-day buffer = 14% — tighter but still safe). Both readings get the same protection from this rule.

Implementation:
- STEP 7 (Option 1 path) compares `expires_at - now < 24h` (forward-looking) OR `now - start_time > (expiry_total_hours - 24)` (backward-looking).
- Step 1.5 (Option 3 path) schedules the one-shot renewal at `+(expiry_total - 24h)` from setup.

The build session substitutes the empirically-confirmed `expiry_total_hours` from §A7 spike step 4. Default `{{RENEWAL_BUFFER_HOURS}}` = `24`. Configurable via the substitution slot if a future engagement needs a different buffer.

## A9 — Renewal failure-mode acceptance (LOCKED from arc-22 A6)

Both Option 1 and Option 3 have a residual failure mode the directive accepts in scope rather than mitigating with additional infrastructure:

**Option 1 (in-fire renewal):** if the polling cron fails to fire for the full buffer window (e.g., 24h continuous service outage at the buffer boundary), the cron expires before the next fire can renew it. Recovery: peer-side radio-check fires after the > 60-min peer-silence threshold per arc-21 §C.1; PRINCIPAL is escalated.

**Option 3 (setup-time scheduled renewal chain):** the chain works if "next renewal fires within `expiry_total_hours` of the polling cron's creation." If the chain breaks across a multi-day continuous outage (session offline through BOTH the renewal moment AND the next renewal moment), the polling cron dies. Recovery: same as Option 1 — peer-side radio-check fires; PRINCIPAL is escalated.

**Why we accept this:** the alternative (double-cron belt-and-suspenders, peer-side renewal monitoring, separate watchdog cron) adds the same coordination-dependency problems that disqualified Option 2 in arc-22. The renewal logic remains per-seat unilateral — mirroring the per-seat-unilateral cadence-switching pattern locked in arc-21 §A6. Bounded staleness is acceptable; protocol-induced bugs cost more than the residual.

**The directive must name this acceptance explicitly** in `substrate/operating-disciplines.md` §11 step 1.5 (Option 3 path) OR in the polling-cron-prompt-template.md STEP 7 commentary (Option 1 path). One-line note: "If the renewal mechanism itself fails (Option 1: cron stops firing before buffer; Option 3: chain breaks across a multi-day outage), recovery is via peer-side radio-check escalation per arc-21 §C.1. No additional watchdog ships."

## A10 — Part 2 implementation locus (DAEDALUS sub-decision; gated by A7 spike result)

Depends on the spike result per A7:
- Backward-looking or forward-looking fields exposed → Option 1: implementation lands in `substrate/templates/polling-cron-prompt-template.md` as STEP 7.
- Neither exposed → Option 3: implementation lands in `substrate/operating-disciplines.md` §11 as step 1.5.
- CronUpdate exists → surface to PRINCIPAL via user-tier POLYBIUS for adjudication (DAEDALUS does NOT decide; does not block on this — proceed with Option 1 or 3 as fallback while the adjudication is pending).

DAEDALUS picks the exact prose wording, the substitution-slot additions (`{{RENEWAL_BUFFER_HOURS}}`, `{{EXPIRY_TOTAL_HOURS}}`, etc.), and the cite-comment shape between the template + op-disc §11.

---

# Universal / self-applied decisions (apply to both Parts)

## A11 — Self-application (LOCKED, both Parts)

**Arc 36's own work applies the convention being shipped:**

- **Part 1 self-app:** project-tier POLYBIUS_the_stoa's coordination heartbeats on `stoa--jru` during this arc carry `[from: polybius-the-stoa]` per the convention being shipped. Cross-tier comments to user-tier POLYBIUS use `[for: user-tier-polybius] [from: polybius-the-stoa]`. The arc that ships the convention IS the first worked example.
- **Part 2 self-app:** project-tier POLYBIUS_the_stoa's polling cron (set up per init handshake per `operating-disciplines.md` §7.2) applies the renewal logic that ships in Part 2 (STEP 7 from polling-cron-prompt-template.md OR step 1.5 from op-disc §11, per A10 result). For a short arc (likely under 24h wall-clock), the renewal check will not fire during the arc itself — but the cron's IS-able to fire it, which is the worked example.

PLINY signoff verifies both self-app properties before PR-merging.

Same self-apply pattern as Arc 35 (per-CAPTAIN trailers on own commits), Arc 34 / C2 (paste-archival in same gauntlet commit), Arc 33 (skill in same arc that defines pattern), Arc 29 (custom/ dir used by arc that defines it).

## A12 — Cite-comment discipline (LOCKED)

Cross-references between new operating-disciplines.md §7.7 + §7.4 bidirectional update + §7.1 update + §11 step 1.5 (if Option 3 path) + MAJOR_POLYBIUS.md §7 cross-ref + polling-cron-prompt-template.md STEP 1.5 + STEP 7 must resolve via cite at every read-site. Same pattern as Arcs 26-35 cite-comments.

## A13 — Authorship attribution unchanged (LOCKED)

File-frontmatter `author:` fields remain Denson Smith per `CLAUDE.md` IMMUTABLE rule. Git commit `Author:` remains PRINCIPAL per `~/.claude/CLAUDE.md`. Arc 35's Co-Authored-By trailer convention applies to all CAPTAIN commits in arc-36/build per `operating-disciplines.md` §28 — verify ADA + DAEDALUS commits carry seat trailers.

## A14 — Out-of-scope hard-locked (LOCKED)

Arc 36 v2 does NOT:

- Extend the author-tag convention (Part 1) to non-POLYBIUS seats (PLINY, CAPTAINs, pair-programmer Majors) — A2.5 hard-lock; future arc may extend with explicit scope expansion.
- Modify the radio-check `[radio-check <slug>]` form — that form is already established.
- Retroactively tag past untagged comments — Arc 36 is forward-only; the parser's low-confidence fallback covers legacy history.
- Build a new cron-renewal mechanism beyond what A10's spike result selects (Option 1 or Option 3 only; Option 2 watcher-cron rejected up-front; CronUpdate surfaces to user-tier).
- Build mechanical parser enforcement (e.g., a pre-comment hook that rejects un-tagged POLYBIUS comments) — Arc 36 ships prose canon + parser-step template; mechanical enforcement is a future arc following Arc 33's mechanical/agent-split pattern if non-compliance recurs.
- Touch `substrate/install.sh` beyond what A6 STEP 1.5 + slot-table extension may require + what A10 STEP 7 may require.
- Build cross-tier-write-upward capability — §7.5 write boundary is unchanged.

If DAEDALUS or any CAPTAIN surfaces a scope concern touching A14, treat as substance disagreement: confirm A14 wording, file follow-up ticket if the concern has merit, do NOT expand this arc.

## A15 — Source-ticket closure (LOCKED)

On Arc 36 v2 ship:
- Close `stoa--e39` (Part 1 work-unit) with cross-ref to merge commit + audit comment.
- Close `stoa--cgn` (Part 2 work-unit) with cross-ref to merge commit + audit comment noting the v2 reversal of the v1 deferral.
- Close `stoa--jru` (parent EPIC) with cross-ref to merge commit + audit comment noting that Part 1 + Part 2 shipped together per original arc-22 bundling (no scope-recut; v1's scope-recut was reversed pre-dispatch per PRINCIPAL no-deferrals stance).

Tag `[for: user-tier-polybius]` on `stoa--jru` inviting QA pass.

## A16 — §15 N=1 honesty (LOCKED)

Per `MAJOR_POLYBIUS.md` §15 + `operating-disciplines.md` §6.7.1:

- **Part 1 (author tags):** N=1 bit-by-it (the original stoa--e39 misread, 2026-05-04, ~25-min stall); N=4-bit-by-it of informal-partial-adoption (the `[radio-check ...]` heartbeats in Arcs 32/33/34/35); N=0 worked-when-applied with full canon (Arc 36's self-application is the first observation under formal §7.7).
- **Part 2 (cron expiry):** N=0 bit-by-it of the failure mode in observed practice (engagements have been short; cap hasn't bitten in 13+ days); the concern is structural-not-observed. N=0 worked-when-applied (no arc has yet operated under the renewal canon). Future-evidence accretion per §6.7.1 — promotion to "structural lesson" status accretes as future arcs ship under §7.7 + STEP 7 / step 1.5 and surface either successful application or fresh failure modes.

Same N=1 framing as Arc 27's §16.6, Arc 28's §22.3, Arc 29's §17.5, Arc 30's §5.9.3, Arc 31's §25.6, Arc 32's §5.9.4, Arc 33's §27, Arc 34's §18 + §5.11 + §9-step-3, Arc 35's §28.

## A17 — Pre-branch hygiene + worktree convention + signoff-accuracy (LOCKED, self-applied)

Per `MAJOR_PLINY.md` §5.9 + §5.9.4 + §5.10 + `operating-disciplines.md` §19.6.

PLINY runs the two-check rule before creating `arc-36/build`. Builds in `.claude/worktrees/arc-36-build/` (NOT in main worktree). User-tier POLYBIUS confirmed at v2 dispatch authoring: local main = origin/main at `594662e`; no orphan arc-build branches (v1's arc-36 directive was never dispatched — only the artifacts committed).

PLINY signoff live-verifies cleanup (arc-36/build local + remote deleted; worktree removed; PR merged; main fast-forwarded; both Parts' self-app properties verified). Attestations cite live-verified state, not assumed-from-context (per §19.6). Source-ticket closures (A15) verified live before posting.

---

## Phase structure

**Phase 1 — Design (DAEDALUS + ARGUS).** DAEDALUS reads this directive + `bw show stoa--e39` + `bw show stoa--cgn` + `bw show stoa--jru` + `git show arcs/22-coordination-hygiene:substrate/arcs/arc-22-build-directive.md` (reference for both Parts' inherited architecture) + current operating-disciplines.md §7 + §11 + §28 + MAJOR_POLYBIUS.md §7 + §18 + MAJOR_PLINY.md §5.9 / §5.9.4 / §5.10 / §5.11 / §5.12 + polling-cron-prompt-template.md. Produces design.md covering both Parts.

For Part 2: execute the A7 spike step BEFORE Part 2 design is finalized; record spike results in design.md §Part-2-spike + post spike result as bw comment on stoa--jru. The decision matrix per A7 then determines Part 2 implementation locus.

ARGUS cold-audits. Expected NEEDS_REVISION on at least one of {Part 1 insertion locus, Part 2 spike interpretation, Part 2 implementation locus, cite-comment shape} given the integration surface.

**Phase 2 — Build (ADA in `.claude/worktrees/arc-36-build/`).** ADA implements both Parts per approved design.md. ADA's commits carry Co-Authored-By trailers per §28. Self-applies: project-tier POLYBIUS_the_stoa's heartbeats on stoa--jru carry `[from: polybius-the-stoa]` per Part 1 being shipped.

**Phase 3 — Verify (VERA + CATO + ZENO).** VERA exercises probes from design.md (Parts 1 + 2). CATO cold-reads diff. ZENO mechanical spec-vs-result. CATO is MANDATORY for this arc (substrate canon work + new top-level section + template extensions + behavioral protocol changes; wording precision matters).

**Phase 4 — Ship + close.** Smoke + PR + merge + cleanup + close. PLINY signoff per §5.10 live-verifies all properties from A11 + A17. Close stoa--e39 + stoa--cgn + stoa--jru per A15 with audit comments. Tag `[for: user-tier-polybius]` on stoa--jru.

---

## DAEDALUS sub-decisions summary

- **A5** — Part 1 insertion locus (op-disc §7.7 new vs §7.1 extend; §7.4 bidirectional update inline)
- **A5** — MAJOR_POLYBIUS.md §7 cross-ref shape (body cite vs new subsection)
- **A6** — Part 1 polling-cron-prompt template STEP 1.5 (mandatory vs optional)
- **A7** — Part 2 spike execution + recording (mechanical; not really discretion; just procedure)
- **A10** — Part 2 implementation locus (per A7 spike result decision matrix)

User-tier POLYBIUS leans: A5 (α) new §7.7 + inline §7.4 update; A5 body-paragraph cite; A6 STEP 1.5 mandatory; A10 follows spike result.

If any pick exceeds DAEDALUS discretion, treat as PRINCIPAL-gate per §25 — halt + escalate immediately rather than proceed-then-flag.

---

## Read order for DAEDALUS

1. This directive (load-bearing spec for both Parts).
2. `bw show stoa--e39` (Part 1 work-unit; 2026-05-04 empirical anchor).
3. `bw show stoa--cgn` (Part 2 work-unit; 2026-05-04 CATO surfacing during arc-21 review).
4. `bw show stoa--jru` (parent EPIC; closes on ship; carries the bundling history).
5. `git show arcs/22-coordination-hygiene:substrate/arcs/arc-22-build-directive.md` (architectural reference for both Parts — A2/A2.5/A3/A4 Part 1 + A4/A5/A6 Part 2 LOCKED decisions inherited).
6. `HUMAN_paste-polybius-arc-36-instruction.md` in the project root — POLYBIUS's activation paste; same content frame.
7. `substrate/operating-disciplines.md` §7 entire section (current §7.1-§7.6 — universal-team POLYBIUS-pair canon; A5/A4 insertion surface for Part 1) + §11 (autonomous-mode-setup checklist; A10 Option-3-path insertion surface for Part 2) + §28 (Arc 35 Co-Authored-By trailer canon; ADA + DAEDALUS commits must apply).
8. `substrate/MAJOR_POLYBIUS.md` §7 (POLYBIUS-tier specific bw-handling; A5 cross-ref target) + §18 (user-tier housekeeping commits; reference for A17).
9. `substrate/MAJOR_PLINY.md` §5.9 + §5.9.4 + §5.10 + §5.11 + §5.12 (pre-branch hygiene + worktree convention + signoff-accuracy + paste archival + seat-identity-in-dispatch-brief; all self-applied per A11/A17).
10. `substrate/templates/polling-cron-prompt-template.md` — current 161 lines; A6 + A10 insertion surface.
11. `substrate/operating-disciplines.md` §27 (Arc 33 mechanical/agent split — precedent for "ship prose canon now; defer mechanical enforcement to future arc if non-compliance recurs"; A14 hard-lock cites this).
12. `the-stoa/SPECIFICATION.md` §10.1 + §4.5 (generational lineage architecture — context for why this arc creates the successor-generation team via its canon delta).
