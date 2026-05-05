# Arc 22 build directive — Coordination hygiene (bw-timeline parsing + cron expiry handling)

**Audience:** the fresh Claude Code session opened to build Arc 22 deliverables (MAJOR_PLINY_the_stoa).
**Authored by:** user-tier MAJOR_POLYBIUS + the PRINCIPAL (Denson Smith).
**Status:** active directive. Pre-dispatch §5.4 cold review performed by CAPTAIN_ARGUS (subagent dispatched by user-tier POLYBIUS — independent session, no context contamination from authoring). 6 load-bearing findings (F1: empirical-expiry probe, F2: slug normalization vs slot values, F3: `[for:]` expansion ownership, F4: non-POLYBIUS comment scope, F5: matrix coverage gap for forward-looking fields, F6: renewal-failure-mode acceptance) + 4 minor surfaced; all 6 load-bearing findings folded inline before commit. Audit verdict: SURFACE (buildable with author judgment, not structurally broken).
**Bw ticket:** `stoa--pbz2` (parent epic — to be created at dispatch with both children wired as `blocks` deps). Children: `stoa--e39`, `stoa--cgn`.
**Builds on:** Arc 21 (the-stoa main `e2d8b63` + `51397da`). Arc 21 landed the autonomous-mode protocol stack (radio-check, adaptive cadence, unified polling, write boundaries, routing, mode propagation). Arc 22 closes two correctness bugs in that stack that surfaced empirically during arc-21 coordination itself.

**Your one job:** harden the POLYBIUS-pair coordination protocol against two failure modes observed during arc-21:

1. **bw-timeline parsing brittleness** (stoa--e39) — POLYBIUS_the_stoa misread the bw timeline, attributing user-tier POLYBIUS's `[for: POLYBIUS_the_stoa]` comment as their own self-heartbeat. Symptom: ~25-min coordination stall during the §5.4 review handoff. Root cause: timestamp-only parsing without explicit author tags. Fix: explicit author-tag convention on POLYBIUS bw comments + parsing teaching in MAJOR_POLYBIUS + parsing step in the polling-cron-prompt template.

2. **CronCreate 7-day expiry** (stoa--cgn) — CronCreate has a 7-day expiry per Claude Code docs; multi-day autonomous engagements that exceed 7 days will silently lose their polling cron. The surviving peer's radio-check eventually fires, but ~6 days of dead air pass first. Fix: spike CronList output to discover what fields are exposed, then implement renewal logic (in-fire check OR setup-time scheduled renewal — spike result decides).

Both deliverables modify the same surface area (`operating-disciplines.md` §7, `MAJOR_POLYBIUS.md` §7, `templates/polling-cron-prompt-template.md`) — bundling them as one coherent coordination-hygiene patch is strictly cheaper than two sequential arcs.

This is a small arc: 2 Parts × 2 Phases × ~8 deliverables. Much smaller than arc-21. Per MAJOR_POLYBIUS §5.4, external review by a cold reviewer is required for multi-concern directives — performed by user-tier POLYBIUS during authoring (not a separate session round-trip), per the established convention that user-tier POLYBIUS qualifies as cold-reviewer for the-stoa-tier work.

---

## Comms — direct async via bw, autonomous mode

PRINCIPAL is in HITL mode for this engagement (default; not declared autonomous). You (PLINY_the_stoa) work head-down on the deliverables and surface back at end-of-arc with the ship summary, OR mid-arc on universal escalation triggers (substance disagreement, authorship/copyright, irreducible ambiguity, peer-silence > 60 min on coordination tickets).

If you choose to set up a polling cron for self-coordination on `stoa--pbz2`, that is your call — record the cron id in your initialization handshake. If you do not need one (small arc, fits in one session), do not set one up.

bw command syntax: `bw comment <id> "text"` — positional, no `-m` flag. `bw close <id> --reason "text"` — `--reason` is a flag.

---

## Read first

1. **`substrate/operating-disciplines.md`** — the universal-team disciplines doc (current at 285 lines after arc-21). Section §7 (POLYBIUS-pair coordination protocol) is the primary edit surface. You will extend §7.1 (radio-check) with author-tag convention and may add a new §7.7 (bw-timeline parsing teaching).

2. **`substrate/MAJOR_POLYBIUS.md`** — current at 730 lines. §7 is where POLYBIUS-tier-specific bw-handling lives. You will add a subsection on bw-timeline parsing.

3. **`substrate/templates/polling-cron-prompt-template.md`** — current at 135 lines. STEP 1 (substantive read) and STEP 3 (self-radio-check refresh) need parsing logic added. STEP 4 (cadence-tag detection) may grow a renewal sub-step depending on spike result.

4. **The two cluster ticket bodies** — `bw show stoa--e39` and `bw show stoa--cgn`. Both carry the empirical anchor.

5. **Arc 21 ship commit** (`e2d8b63`) — the substrate state your edits build on. You are not modifying arc-21 deliverables; you are extending them.

---

## Phase A — Architectural decisions (LOCKED pre-dispatch by user-tier POLYBIUS)

Settled during directive authoring. Do NOT surface these as design questions.

### A1. Two Parts, two Phases — LOCKED

Part 1 (e39) and Part 2 (cgn) are independent in scope but both modify `templates/polling-cron-prompt-template.md` and both extend `operating-disciplines.md` §7. Bundling reduces template-edit churn (one round of edits instead of two) and keeps the §7 surface coherent. Phasing: Phase 1 = Part 1 (e39 — author-tag convention + parsing teaching) → Phase 2 = Part 2 (cgn — spike + renewal logic) → Phase 3 = smoke + ship.

Part 1 lands first because its template edits are bounded (insert STEP 1.5: parse author tags). Part 2's template edits depend on the spike outcome, so doing Part 1 first keeps the template in a known-good state during the cgn spike.

### A2. Author-tag convention — LOCKED (with scope ruling and normalization rule)

Every POLYBIUS bw comment posted as part of coordination prefixes the body with an author tag. Three forms cover the cases:

- **Self-heartbeat:** `[radio-check <self-seat-slug>]` — already established; arc-22 does not change this form, but the slug-normalization rule below applies.
- **Cross-seat addressed:** `[for: <recipient-seat-slug>] [from: <sender-seat-slug>]` — both tags mandatory.
- **Own-bw substantive (not addressed to a peer):** `[from: <self-seat-slug>]` — for status updates, gauntlet phase comments, decisions logged in own bw without a specific recipient.

**This is an expansion of the existing convention, not a "make-explicit-what-was-implicit":**

- `[for:]` is currently documented in `operating-disciplines.md` §7.4 for cross-tier UPWARD requests only (project-tier→user-tier). Arc 22 promotes it to bidirectional ("addressed comment by sender to recipient"). The directive owns this expansion.
- `[from:]` is new. No prior convention requires sender-tag.

The reason for the expansion: a peer reading the timeline can match `[for: <self>]` to "addressed to me" but cannot reliably distinguish "from peer" from "from self" without comparing the timestamp against the seat's own activity log — which is exactly the inference step that failed in the e39 empirical. `[from: <self>]` makes attribution explicit at the data layer.

**Slug normalization rule — LOCKED.** Slugs in tags are lowercase, hyphenated, no whitespace: `user-tier-polybius`, `polybius-the-stoa`, `polybius-ariadne-core`. The slug matches the role-file slug used by the autonomous-mode-activation-template (arc-21 §B.2).

The polling-cron-prompt template currently has substitution slots `{{SELF_SEAT_NAME}}` and `{{PEER_SEAT_NAME}}` populated with display-form strings (e.g., `user-tier POLYBIUS`). Arc 22 introduces parallel slots `{{SELF_SEAT_SLUG}}` and `{{PEER_SEAT_SLUG}}` populated with the normalized slug. Tags emitted in the template body use the slug; display-form slots remain for human-readable prose (radio-check messages, heartbeats with state). STEP 1.5 author-attribution matches against the slug, not the display form. Both slots are documented in the substitution-slot table.

Legacy/untagged comments (pre-arc-22 history) fall to STEP 1.5's low-confidence fallback regardless of slug match.

### A2.5. Convention scope: POLYBIUS-on-POLYBIUS coordination — LOCKED

The author-tag convention applies to POLYBIUS instances only (user-tier POLYBIUS, project-tier POLYBIUS, sub-project POLYBIUS). PLINY, CAPTAINs, and pair-programmer Majors are NOT required to author-tag their bw comments in arc-22.

Justification: peer-silence threshold and self-heartbeat-due timing computations consume `last_self_activity` / `last_peer_activity` timestamps where "self" and "peer" are POLYBIUS instances. Comments by PLINY (gauntlet phase status), CAPTAINs (verdicts, surfaced ambiguities), or pair-programmer Majors do NOT count toward those timestamps — they are SUBSTANCE comments, not coordination-attribution comments. The polling-cron parser correctly classifies them as "non-POLYBIUS, low-confidence attribution" and they do not perturb the timeline computations that the e39 fix targets.

`operating-disciplines.md` §7.7 (deliverable 1.2) names this scope explicitly: parsing attributes POLYBIUS-tagged comments by tag, untagged comments by author-context-inference (low confidence), and only POLYBIUS-attributed comments enter the timeline-arithmetic for radio-check / heartbeat thresholds.

A future arc (arc-23 or later) MAY extend the convention to PLINY/CAPTAIN authoring; that's a deliberate scope expansion, not silently in arc-22's scope.

### A3. Parsing teaching lives in operating-disciplines.md, not MAJOR_POLYBIUS — LOCKED

Per the arc-21 §A2 mapping convention: universal patterns go in `operating-disciplines.md`, POLYBIUS-tier-specific framing back-references. bw-timeline parsing is universal — any seat reading a bw comment timeline (PLINY surveying gauntlet status, CAPTAIN reading dispatch-brief context, POLYBIUS doing peer-silence detection) needs the same parsing discipline. So the canonical text lives in `operating-disciplines.md` §7 (extend §7.1 or add §7.7); `MAJOR_POLYBIUS.md` §7 cross-refs back.

### A4. cgn spike-first, design-decision-during-build — LOCKED with constraints

The cgn ticket lists three implementation options:

- **Option 1: In-fire renewal check.** Each fire, check if the cron is approaching expiry; CronDelete + CronCreate before threshold.
- **Option 2: Separate watcher cron.** One of the polling crons watches the others' expiry dates.
- **Option 3: Setup-time scheduled renewal.** POLYBIUS schedules a one-shot CronCreate at +6 days from start.

The choice depends on what `CronList` actually exposes AND on the actual expiry duration (current Claude Code docs have a 3-day-vs-7-day discrepancy across pages — the cgn ticket's "7 days" is one source; community docs cite 3 days in places). The spike must empirically confirm both.

**Spike step (expanded):**

1. Open a fresh REPL or use the dispatched session itself.
2. `CronCreate` a throwaway session-only cron with a long cadence (e.g., `0 0 * * *` daily) and a no-op prompt.
3. `CronList` and capture the FULL output structure for the new cron. Inspect every field: does it expose `start_time` / `created_at` / `age` (backward-looking) OR `expires_at` / `next_fire` / `valid_until` (forward-looking) OR neither?
4. Search the current Claude Code docs for the actual cron expiry duration (the cgn ticket says 7 days; recent docs cite 3 days in places). Record the empirically-confirmed expiry from whatever authoritative source you find. If docs are still ambiguous, file the ambiguity in your build log and use the SHORTER documented value (conservative).
5. `CronDelete` the throwaway.
6. Record the field list AND the confirmed expiry duration in your build log (in your bw comment on `stoa--pbz2`).

**Decision matrix (locked, expanded with forward-looking row):**

| `CronList` exposes | Implementation | Where it lands |
|---|---|---|
| Backward-looking (start-time / age / created-at) | Option 1 (in-fire check based on age threshold) | `templates/polling-cron-prompt-template.md` — new STEP 7 between STEP 6 and "End of fire-loop" |
| Forward-looking (expires-at / next-fire / valid-until) | Option 1 (in-fire check based on time-until-expiry) — strictly simpler than backward-looking | Same location as above; STEP 7 reads `expires_at - now < {{RENEWAL_BUFFER_HOURS}}` instead of `now - start_time > {{RENEWAL_THRESHOLD}}` |
| Both backward AND forward fields exposed | Option 1 with forward-looking comparison (preferred — avoids age-arithmetic fencepost errors) | Same |
| Neither (cron metadata fully opaque) | Option 3 (setup-time scheduled renewal) | `operating-disciplines.md` §11 — new step 1.5 ("schedule a one-shot renewal cron at +<expiry-1day>") |
| `CronUpdate` or equivalent in-place renewal primitive exists | Surface to user-tier POLYBIUS via `[for: user-tier-polybius] [from: polybius-the-stoa]` on `stoa--pbz2` | Decision routes through user-tier POLYBIUS; do not pick unilaterally — this is a strictly-better path that may justify scope adjustment |

Option 2 is rejected up-front: separate watcher cron adds an entirely new coordination dependency (the watcher's own expiry, the watcher's polling cost, the watcher's failure modes). Options 1 and 3 keep the renewal logic local to the engagement that owns the cron — strictly simpler.

Genuinely-unexpected states (e.g., `CronList` returns no entries, fields are present but undocumented, the empirical expiry probe reveals inconsistency between docs and tool behavior) surface to user-tier POLYBIUS via `[for: user-tier-polybius] [from: polybius-the-stoa]` on `stoa--pbz2` — do not pick on your own.

### A5. Cron-renewal buffer — LOCKED (expressed as buffer, not absolute day)

Renewal fires when **time-until-expiry < 1 day** (24 hours), regardless of whether the empirical expiry is 3 days or 7 days. Expressing the trigger as a buffer-from-expiry rather than an absolute "day 6" makes the rule correct under either docs reading.

The 1-day buffer absorbs:

- A renewal fire that itself hits an error (timeout, quota, transient API failure) — there is a full day to retry on the next fire.
- A POLYBIUS session offline for hours when the renewal would have fired (the renewal catches on the NEXT fire after the session resumes, still well inside the expiry window).
- Clock-skew / time-zone confusion in the cron service.

For a 3-day expiry, this means renewal at +2 days from creation (1-day buffer = 33% of lifetime — generous). For a 7-day expiry, renewal at +6 days (1-day buffer = 14% — tighter but still safe). Both readings get the same protection from this rule.

Implementation: STEP 7 (Option 1 path) compares `expires_at - now < 24h` (forward-looking) OR `now - start_time > (expiry_total_hours - 24)` (backward-looking). Step 1.5 (Option 3 path) schedules the one-shot renewal at `+(expiry_total - 24h)` from setup. The build session substitutes the empirically-confirmed `expiry_total_hours` from §A4 spike step 4.

Default `{{RENEWAL_BUFFER_HOURS}}` = `24`. Configurable via the substitution slot if a future engagement needs a different buffer.

### A6. Renewal failure-mode acceptance — LOCKED

Both Option 1 and Option 3 have a residual failure mode the directive accepts in scope rather than mitigating with additional infrastructure:

**Option 1 (in-fire renewal):** if the polling cron fails to fire for the full buffer window (e.g., 24h continuous service outage at the buffer boundary), the cron expires before the next fire can renew it. Recovery: peer-side radio-check fires after the > 60-min peer-silence threshold per arc-21 §C.1; PRINCIPAL is escalated.

**Option 3 (setup-time scheduled renewal chain):** the chain works if "next renewal fires within `expiry_total_hours` of the polling cron's creation." If the polling cron is renewed via the chain and the renewal cron's own re-schedule slips by > buffer hours (session offline through BOTH the renewal moment AND the next renewal moment — possible only on a multi-day continuous outage), the polling cron from the previous chain becomes ≥ expiry-old and dies. Recovery: same as Option 1 — peer-side radio-check fires; PRINCIPAL is escalated.

**Why we accept this:** the alternative (double-cron belt-and-suspenders, peer-side renewal monitoring, separate watchdog cron) adds the same coordination-dependency problems that disqualified Option 2. The renewal logic remains per-seat unilateral — mirroring the per-seat-unilateral cadence-switching pattern locked in arc-21 §A6. Bounded staleness is acceptable; protocol-induced bugs cost more than the residual.

**The directive must name this acceptance explicitly** in `operating-disciplines.md` §11 step 1.5 (Option 3 path) OR in the polling-cron-prompt-template.md STEP 7 commentary (Option 1 path). One-line note: "If the renewal mechanism itself fails (Option 1: cron stops firing before buffer; Option 3: chain breaks across a multi-day outage), recovery is via peer-side radio-check escalation per arc-21 §C.1. No additional watchdog ships."

### A7. Voice — LOCKED: PRINCIPAL/HUMAN throughout

All new substrate content uses PRINCIPAL/HUMAN. Voice grep is part of Phase 3 smoke.

---

## Deliverables

### Part 1 — bw-timeline parsing (stoa--e39)

Closes: `stoa--e39`.

#### 1.1 `substrate/operating-disciplines.md` — extend §7.1 with author-tag convention

**Location:** `substrate/operating-disciplines.md` §7.1 (currently lines ~59-68, the four-beat radio-check protocol).

**Required edit:** add a new fifth beat at the end of §7.1, BEFORE the §7.2 header:

```
5. **Author-tag convention (POLYBIUS-on-POLYBIUS coordination).** Every
   coordination comment posted by a POLYBIUS instance carries an explicit
   sender tag. Three forms:
   - Self-heartbeat: `[radio-check <self-seat-slug>]` (form unchanged from
     arc-21; slug-normalization rule below applies).
   - Cross-seat addressed: `[for: <recipient-seat-slug>] [from: <sender-seat-slug>]`.
     Both tags mandatory. This expands the prior `[for:]` convention from
     UPWARD-only (project→user) to bidirectional, and adds the mandatory
     `[from:]` tag which is new in arc-22.
   - Own-bw substantive (not addressed to a specific peer):
     `[from: <self-seat-slug>]`.

   **Slug normalization:** lowercase, hyphenated, no whitespace. Example
   slugs: `user-tier-polybius`, `polybius-the-stoa`, `polybius-ariadne-core`.
   The slug matches role-file naming used by the autonomous-mode-activation-
   template (arc-21 §B.2). Display-form names (e.g., "user-tier POLYBIUS")
   may appear in prose within comment bodies but the LEADING TAG always uses
   the slug.

   **Scope:** this convention applies to POLYBIUS instances. PLINY,
   CAPTAINs, and pair-programmer Majors are not required to author-tag —
   their substantive comments do not enter the timeline-arithmetic that
   drives radio-check / heartbeat thresholds. See §7.7 for parsing.

   The convention exists so peers reading the timeline can attribute each
   POLYBIUS comment to its sender without inferring from timestamp +
   content — the inference step that failed in the e39 empirical.
```

#### 1.2 `substrate/operating-disciplines.md` — new §7.7 "bw-timeline parsing"

**Location:** `substrate/operating-disciplines.md` — append after current §7.6 (Empirical lineage), making §7.6 → §7.7 (parsing) → "Empirical lineage" become §7.8. Renumber §7.6 to §7.8 OR insert §7.7 before §7.6 — your call; pick whichever keeps the section flow most natural.

**Required content (~40-60 lines):**

1. **Framing** (~3 lines): when a POLYBIUS peer reads a bw timeline to compute "last own activity" / "last peer activity" / "missed-check threshold", the attribution step is load-bearing. A misattributed comment causes silent stalls (the e39 empirical).

2. **Parse-by-tag, not by inference.** Every POLYBIUS coordination comment carries a `[from: <seat-slug>]` or `[radio-check <seat-slug>]` tag per §7.1. Read the tag first; do not infer authorship from timestamp, content pattern, or position.

3. **Procedure:**
   - For each comment in the timeline, extract the leading tag.
   - Match the tag's slug against expected POLYBIUS seat slugs (lowercase, hyphenated, whitespace-stripped).
   - If `[radio-check <slug>]`: POLYBIUS heartbeat by `<slug>`.
   - If `[for: <slug-Y>] [from: <slug-X>]`: POLYBIUS comment by `<slug-X>`, addressed to `<slug-Y>`.
   - If `[from: <slug-X>]`: POLYBIUS comment by `<slug-X>`, no specific recipient.
   - If tagged but slug does not match a known POLYBIUS slug (e.g., comment by PLINY or a CAPTAIN that happens to use a tag-like prefix): treat as non-POLYBIUS, do not enter timeline-arithmetic.
   - If untagged: non-POLYBIUS comment (PLINY, CAPTAIN, substance comment, legacy pre-arc-22 POLYBIUS comment) — does NOT enter timeline-arithmetic. May be substance-load-bearing for OTHER reads but not for radio-check/heartbeat computation.

4. **Compute peer-silence threshold and self-heartbeat-due timing from tagged-POLYBIUS comments only.** This is the load-bearing rule: only `[radio-check]` or `[from:]` POLYBIUS-slug-matching comments contribute timestamps to `last_self_activity` / `last_peer_activity`. Non-POLYBIUS comments (PLINY status, CAPTAIN verdicts, etc.) and untagged legacy comments do NOT.

5. **Why non-POLYBIUS comments are excluded:** PLINY/CAPTAIN comments are SUBSTANCE comments (gauntlet phase status, ambiguity surfaces, dispatch results) — not coordination-attribution comments. Including them in `last_peer_activity` would defeat radio-check (peer-silence threshold would never fire because PLINY comments would mask actual POLYBIUS silence). The protocol intentionally tracks POLYBIUS-on-POLYBIUS attentiveness as a separate signal from team activity-volume.

6. **Empirical anchor:** 2026-05-04 — POLYBIUS_the_stoa attributed user-tier POLYBIUS's `[for: POLYBIUS_the_stoa]` comment as own self-heartbeat, blocking the §5.4 review pickup ~25 min. Root cause: timestamp + content-pattern inference instead of explicit-tag parsing. Codification: this section + §7.1 author-tag convention.

7. **Future-scope note:** if a future engagement requires PLINY/CAPTAIN comments to enter coordination-attribution computations (e.g., a new gauntlet-pacing protocol), the author-tag convention is extensible to non-POLYBIUS seats — the parsing rules above generalize. Out of arc-22 scope; surface as a new ticket if/when needed.

#### 1.3 `substrate/MAJOR_POLYBIUS.md` — §7 cross-ref to parsing teaching

**Location:** `substrate/MAJOR_POLYBIUS.md` §7 area (locate the existing bw-handling subsection, likely §7.1 or §7.4 after arc-21).

**Required edit:** add a one-paragraph subsection (or extend an existing one) cross-referencing `operating-disciplines.md` §7.7. Text:

```
**bw-timeline parsing.** When you compute peer-silence freshness or self-
heartbeat-due timing from the bw timeline, parse comments by their leading
author tag (`[from: <seat>]`, `[radio-check <seat>]`, `[for: <Y>] [from:
<X>]`). Do not infer authorship from timestamp or content pattern — that
inference fails when peer comments use varied prefixes. See operating-
disciplines.md §7.7 for the full procedure and the empirical anchor.
```

This is a short pointer, not a duplicate of the universal text. Cross-ref bidirectional: `operating-disciplines.md` §7.7 already cross-refs back to "POLYBIUS-tier specific applications" — no new edit there.

#### 1.4 `substrate/templates/polling-cron-prompt-template.md` — slot expansion + STEP 1.5 parsing

**Location:** `substrate/templates/polling-cron-prompt-template.md` — substitution-slots table + STEP 1 area.

**Required edits:**

1. **Add two new substitution slots** to the slots table (after existing `{{PEER_SEAT_NAME}}`):

   | Slot | Meaning | Example |
   |---|---|---|
   | `{{SELF_SEAT_SLUG}}` | normalized lowercase-hyphenated slug for own seat | `polybius-the-stoa` |
   | `{{PEER_SEAT_SLUG}}` | normalized lowercase-hyphenated slug for peer seat | `user-tier-polybius` |

   Document: display-form slots (`{{SELF_SEAT_NAME}}` / `{{PEER_SEAT_NAME}}`) are used in human-readable prose within comment bodies; SLUG slots are used in the LEADING author tag. Both must be supplied at template substitution time.

2. **Insert STEP 1.5 between STEP 1 (aggregate) and STEP 2 (peer-silence escalation):**

   ```
   STEP 1.5 — author-attribute aggregated comments.
   For each new comment in the aggregated state, extract the leading author
   tag per operating-disciplines.md §7.7:
     - [radio-check <slug>]: POLYBIUS heartbeat by <slug>
     - [for: <slug-Y>] [from: <slug-X>]: POLYBIUS comment by <slug-X> to <slug-Y>
     - [from: <slug-X>]: POLYBIUS comment by <slug-X>
     - other / no tag: non-POLYBIUS or legacy — does NOT enter timeline-arithmetic

   Build two timestamp lists, slug-matching:
     - last_self_activity: most recent comment where author-slug == {{SELF_SEAT_SLUG}}
     - last_peer_activity: most recent comment where author-slug == {{PEER_SEAT_SLUG}}

   These two timestamps drive STEP 2 (peer-silence escalation) and STEP 3
   (self-heartbeat refresh). Slug-matching is whitespace-tolerant and
   case-insensitive on the right-hand side (e.g., a tag accidentally posted
   as `[from: User-Tier-POLYBIUS]` still matches `user-tier-polybius`).
   Without explicit POLYBIUS attribution, neither computation is reliable —
   the e39 empirical.
   ```

3. **Update STEP 2 and STEP 3** to reference `last_peer_activity` / `last_self_activity` from STEP 1.5 (currently they say "Compute time-since-last-{{PEER_SEAT_NAME}}-activity from aggregated state" — replace with "from `last_peer_activity` per STEP 1.5").

4. **Update STEP 3's heartbeat-post line** to use the SLUG slot in the tag:

   ```
   bw comment {{COORDINATION_TICKET}} "[radio-check {{SELF_SEAT_SLUG}}]
   cron {{CRON_ID}} cadence {{CADENCE}} — <one-line state>"
   ```

5. **Update the usage example block** at the bottom of the template to populate both `{{SELF_SEAT_NAME}}` AND `{{SELF_SEAT_SLUG}}` (and the peer counterparts), and to show the radio-check init handshake using the slug form.

#### 1.5 `substrate/templates/autonomous-mode-activation-template.md` — author-tag instruction

**Location:** `substrate/templates/autonomous-mode-activation-template.md` (lands as part of arc-21).

**Required edit:** in the section that names the 6 setup-checklist steps from `operating-disciplines.md` §11, add a sentence to step 2 (radio-check pattern): "All coordination comments use the author-tag convention from `operating-disciplines.md` §7.1 (5th beat) — `[from: <self-seat>]` on every coordination post; `[for: <recipient>] [from: <self>]` on cross-tier-addressed posts."

### Part 2 — CronCreate expiry handling (stoa--cgn)

Closes: `stoa--cgn`.

#### 2.1 Spike: CronList field structure + empirical expiry confirmation

**Location:** any session — recommend doing it inside your dispatched build session.

**Procedure (per §A4 expanded spike):**

1. `CronCreate` a throwaway session-only cron with a long cadence (e.g., `0 0 * * *` daily) and a no-op prompt.
2. `CronList` and capture the FULL output structure — every field returned for the new cron entry. Note especially: backward-looking fields (`start_time`, `created_at`, `age`) vs forward-looking fields (`expires_at`, `next_fire`, `valid_until`) vs both vs neither.
3. **Empirical-expiry confirmation:** search current Claude Code docs (use WebSearch — your training data is out of date per CLAUDE.md) for the actual cron expiry duration. Cross-reference at least two sources: official `code.claude.com/docs/scheduled-tasks` AND community sources. If they disagree, use the SHORTER documented value (conservative) and record the ambiguity in your build log.
4. Check for `CronUpdate` or equivalent in-place renewal primitive in the available tool set (use ToolSearch with `cron` keywords).
5. `CronDelete` the throwaway.
6. Record in your build log on `stoa--pbz2`: (a) the full CronList field list, (b) the empirically-confirmed expiry duration with source citations, (c) presence/absence of CronUpdate-equivalent.

**Decision per §A4 matrix:**

- Backward-looking fields exposed → Option 1 (deliverable 2.2), backward-arithmetic variant.
- Forward-looking fields exposed → Option 1 (deliverable 2.2), forward-arithmetic variant — STRICTLY simpler; prefer this if both forward and backward are present.
- Neither → Option 3 (deliverable 2.3).
- CronUpdate-equivalent exists → surface via `[for: user-tier-polybius] [from: polybius-the-stoa]` on `stoa--pbz2`; this is a strictly-better path that may justify scope adjustment.
- Genuinely-unexpected state (no entries returned, undocumented fields, docs vs tool inconsistency) → surface via the same routing.

#### 2.2 IF Option 1: in-fire renewal check

**Location:** `substrate/templates/polling-cron-prompt-template.md` — append a new STEP 7 between current STEP 6 (escalation triggers) and "End of fire-loop".

**Required edit (forward-looking variant — preferred when `expires_at` or equivalent is exposed):**

```
STEP 7 — cron-renewal check.
Compute time_until_expiry = expires_at - now (or equivalent forward-looking
field per spike).
If time_until_expiry < {{RENEWAL_BUFFER_HOURS}}:
  CronCreate a NEW recurring cron with the same prompt body (this whole
    template; substitute the new {{CRON_ID}} on return).
  Post on {{COORDINATION_TICKET}}: "[from: {{SELF_SEAT_SLUG}}] cron renewed:
    superseded {{CRON_ID}} with <new id>; cadence {{CADENCE}} unchanged."
  CronDelete {{CRON_ID}} (the old cron).
  exit fire-loop (the OLD cron will not fire again; the new cron picks up).
Else: continue.

Why renewal at the buffer boundary: the {{RENEWAL_BUFFER_HOURS}} buffer
absorbs renewal errors, offline windows, and clock skew. Default 24 hours
(§A5). For docs-claimed 3-day expiry this is renewal at +2 days; for
7-day expiry, +6 days. Same protection under either reading.

Failure mode acceptance (§A6): if the cron stops firing for the entire
buffer window (continuous service outage at the boundary), the cron expires
before the next fire can renew it. Recovery: peer-side radio-check
escalation per arc-21 §C.1 — no additional watchdog ships.
```

**Required edit (backward-looking variant — when only `start_time`/`age` is exposed):**

```
STEP 7 — cron-renewal check.
Compute cron_age = now - start_time (or use exposed `age` field directly).
If cron_age > ({{EXPIRY_TOTAL_HOURS}} - {{RENEWAL_BUFFER_HOURS}}):
  [...same body as forward-looking variant from CronCreate onward...]
```

Where `{{EXPIRY_TOTAL_HOURS}}` is filled from spike step 3's empirically-confirmed expiry duration.

**Substitution slots additions:**

| Slot | Meaning | Default |
|---|---|---|
| `{{RENEWAL_BUFFER_HOURS}}` | hours-before-expiry to trigger renewal | `24` |
| `{{EXPIRY_TOTAL_HOURS}}` | empirically-confirmed cron expiry duration in hours | `<from spike>` (e.g., `72` for 3-day, `168` for 7-day) |

**Cross-edit:** update `operating-disciplines.md` §11 step 1 to add a one-line note: "The polling-cron-prompt template handles cron expiry via STEP 7 in-fire renewal — no separate renewal action required at setup. Empirically-confirmed expiry: `<value from spike>`. Failure mode if the renewal mechanism fails recovers via peer-side radio-check (§C.1)."

#### 2.3 IF Option 3: setup-time scheduled renewal

**Location:** `substrate/operating-disciplines.md` §11 step 1 (autonomous-mode-setup checklist, polling-cron substep).

**Required edit:** add a new step 1.5 immediately after step 1:

```
1.5 **Schedule renewal.** CronCreate has a finite expiry (empirically
   confirmed at <value> hours per arc-22 spike). To prevent silent loss of
   the polling cron on multi-day engagements, schedule a one-shot renewal
   cron at +(<expiry> - {{RENEWAL_BUFFER_HOURS}}) from setup-complete:

   - CronCreate cron: `<computed-renewal-time per cron syntax>`,
     recurring: false,
     prompt: "Renew the autonomous-mode polling cron on
     {{COORDINATION_TICKET}}. CronList to find the current polling cron id.
     CronCreate a new recurring cron with the polling-prompt body (re-use
     this template, substituting the new {{CRON_ID}} on return). CronDelete
     the old polling cron. Post [from: {{SELF_SEAT_SLUG}}] cron renewed:
     superseded <old> with <new> on {{COORDINATION_TICKET}}. Then
     CronCreate a new one-shot renewal at +(<expiry> - buffer) from now."
   - The renewal cron itself self-renews via the same procedure (chained
     one-shots).

   Record both cron ids (polling cron + renewal cron) in the radio-check
   initialization handshake on the coordination ticket.

   **Failure mode acceptance (§A6):** the chain works if the next renewal
   fires within the polling cron's expiry window. If the renewal cron
   itself misses its fire AND the next-renewal-after-that also misses
   (continuous outage > buffer hours at the renewal boundary), the polling
   cron from the previous chain dies. Recovery is via peer-side radio-check
   escalation per §7.1 — no additional watchdog ships. This mirrors the
   per-seat-unilateral cadence-switching pattern (arc-21 §A6); bounded
   staleness is acceptable, protocol-induced bugs cost more.
```

Add a parallel one-line note to `templates/polling-cron-prompt-template.md` at the bottom: "Cron expiry is handled by a separate one-shot renewal cron scheduled at autonomous-mode-setup time per `operating-disciplines.md` §11 step 1.5 — no in-fire renewal logic required in this template. Empirically-confirmed expiry: `<value from spike>`."

#### 2.4 `substrate/MAJOR_POLYBIUS.md` — autonomous-mode entry checklist note

**Location:** `substrate/MAJOR_POLYBIUS.md` §13.4 (mode entry / exit procedures, added by arc-21).

**Required edit:** add a one-line note in the autonomous-entry procedure: "Cron 7-day expiry handling per `operating-disciplines.md` §7.X (in-fire) or §11 step 1.5 (setup-time) — confirm renewal mechanism is in place before declaring setup complete." (Substitute the actual section number once Part 2 lands.)

---

## Phase B — Smoke + ship

### B.1 Smoke beats

1. **Voice grep:** `grep -rE '\b[Cc]olonel\b|\bthe user\b' substrate/ | grep -v 'template-slot' | grep -v 'arcs/'` returns zero non-template hits.
2. **Cross-ref resolution:** every new `§7.X` and `§11 step 1.5` cross-ref points to a real section. `grep -n 'operating-disciplines.md §' substrate/` and verify each target exists.
3. **install.sh dry-run:** `bash substrate/install.sh --dry-run --target user 2>&1 | grep -E 'polling-cron|operating-disciplines'` shows both files in the deploy plan. (No new files added in arc-22 — both are existing files extended — so the deploy-plan check is a sanity check, not a coverage check.)
4. **Author-tag convention smoke:** `grep -E '\[from: |\[for: .* \[from: ' substrate/operating-disciplines.md substrate/templates/polling-cron-prompt-template.md` returns the example tags shown in the new content.
5. **Renewal-path smoke (per spike outcome):**
   - Option 1: `grep -n 'STEP 7' substrate/templates/polling-cron-prompt-template.md` returns the new step.
   - Option 3: `grep -n 'step 1.5' substrate/operating-disciplines.md` returns the new step.

### B.2 Ship

```
git add substrate/operating-disciplines.md substrate/MAJOR_POLYBIUS.md substrate/templates/polling-cron-prompt-template.md substrate/templates/autonomous-mode-activation-template.md
git commit -m "Arc 22: bw-timeline parsing convention + cron 7-day expiry handling

Part 1 (stoa--e39) — bw-timeline parsing:
  - operating-disciplines.md §7.1 +5th beat: author-tag convention
    ([from: <seat>] mandatory on coordination comments)
  - operating-disciplines.md §7.7 (new): bw-timeline parsing procedure
  - MAJOR_POLYBIUS.md §7: cross-ref to parsing teaching
  - templates/polling-cron-prompt-template.md: STEP 1.5 author-attribute
  - templates/autonomous-mode-activation-template.md: author-tag instruction

Part 2 (stoa--cgn) — CronCreate 7-day expiry:
  - Spike: CronList exposes <field> [or: does not expose start-time]
  - Selected Option <1 or 3> per arc-22 §A4 decision matrix
  - templates/polling-cron-prompt-template.md: STEP 7 in-fire renewal
    [OR operating-disciplines.md §11 step 1.5: setup-time renewal]
  - MAJOR_POLYBIUS.md §13.4: renewal-mechanism confirm-on-entry note

Closes stoa--e39, stoa--cgn, stoa--pbz2."
```

Push to origin/main on clean PASS. The arc directive itself (`substrate/arcs/arc-22-build-directive.md`) was committed by user-tier POLYBIUS before dispatch — don't include it in your commit.

---

## Out of scope

- **arc-23** (provenance + deploy correctness: stoa--kjo per-agent git identity + stoa--14u install.sh deploy-plan smoke). Sequenced for after arc-22 ships.
- **Negotiated cadence-switching** (per arc-21 §A6 — still LOCKED out).
- **Cloud-cron renewal** (cloud cron is documented limitation per arc-21 §A8; no cloud renewal logic ships).
- **Retroactive tagging of pre-arc-22 bw comments.** The parsing teaching (§7.7) handles legacy untagged comments via low-confidence fallback. No bulk-rewrite migration of existing bw history.
- **Negotiated renewal protocol between paired POLYBIUS seats.** Each seat renews its OWN cron unilaterally (mirror of the per-seat-unilateral cadence-switching pattern in arc-21 §A6). No cross-seat renewal coordination.
- **CronList wrapper utility.** Spike result is read directly; no wrapper module ships.

---

## Surface back when done

```
bw comment stoa--pbz2 "Arc 22 shipped at commit <sha>, pushed to origin/main.

Smoke test passed:
  - Voice grep clean (no Colonel / the user outside templates).
  - Cross-refs all resolve.
  - install.sh dry-run shows both edited files in deploy plan.
  - Author-tag convention examples present.
  - Renewal-path smoke (Option <1 or 3>) clean.

Spike result (Part 2):
  CronList exposes: <field list per spike>
  Selected: Option <1 in-fire | 3 setup-time> per §A4 decision matrix.

Files modified:
  - substrate/operating-disciplines.md (§7.1 +5th beat, §7.7 new)
  - substrate/MAJOR_POLYBIUS.md (§7 cross-ref, §13.4 renewal note)
  - substrate/templates/polling-cron-prompt-template.md (STEP 1.5 +
    [STEP 7 OR end-note pointing to §11 step 1.5])
  - substrate/templates/autonomous-mode-activation-template.md (author-tag)

Closes stoa--e39, stoa--cgn, stoa--pbz2."
```

Then close the children + parent:

```
bw close stoa--e39 --reason "Landed via Arc 22 / stoa--pbz2"
bw close stoa--cgn --reason "Landed via Arc 22 / stoa--pbz2"
bw close stoa--pbz2 --reason "Arc 22 shipped at <sha>"
bw sync
```

---

## Notes for next-session continuity

If the spike reveals an unexpected CronList field structure that warrants a design call beyond the §A4 decision matrix, surface to user-tier POLYBIUS — do not wait for PRINCIPAL. User-tier POLYBIUS qualifies as cold-reviewer for the-stoa-tier work (per saved feedback memory: user-tier-approves-technical-tier-decisions).

The renewal-cron self-renewal procedure (Option 3 path) creates a chain of one-shot renewal crons — each renewal cron's prompt schedules the NEXT renewal at +6 days. If you implement Option 3, verify the chain is robust against a single missed renewal (e.g., session offline at the renewal moment): the polling cron from the previous chain is still valid for up to 7 days from its own creation, so a single missed renewal is recoverable as long as the next renewal fires within the 7-day-from-polling-cron-creation window. Document this in §11 step 1.5.
